#include <Arduino.h>
#include <ArduinoJson.h>
#include <Preferences.h>
#include <TFT_eSPI.h>
#include <WebServer.h>
#include <WiFi.h>
#include <esp_system.h>
#include <driver/i2s.h>
#include <cctype>
#include <cmath>
#include "setup_page.h"

namespace {
constexpr size_t FRAME_LIMIT = 768;
constexpr unsigned long CONNECT_TIMEOUT_MS = 17000;
constexpr unsigned long AP_TIMEOUT_MS = 20UL * 60 * 1000;
Preferences storage;
WebServer server(80);
TFT_eSPI face;

struct Settings {
  String ssid;
  String password;
  String apn;
  bool open = false;
  int volume = 45;
} config;

String apName;
String setupKey;
String serialLine;
bool discarding = false;
bool apActive = false;
bool attempting = false;
bool reconnectPending = false;
unsigned long apStart = 0;
unsigned long connectStart = 0;
unsigned long reconnectAt = 0;
String lastScreen;

bool loadSettings() {
  JsonDocument stored;
  if (deserializeJson(stored, storage.getString("settings", "{}"))) return false;
  config.ssid = stored["ssid"] | "";
  config.password = stored["password"] | "";
  config.apn = stored["apn"] | "";
  config.open = stored["open"] | false;
  config.volume = stored["volume"] | 45;
  return true;
}

bool enableSetupAp() {
  if (apActive) return true;
  WiFi.mode(WIFI_AP_STA);
  apActive = WiFi.softAP(apName.c_str(), setupKey.c_str());
  if (apActive) apStart = millis();
  return apActive;
}

void connectWifi() {
  if (config.ssid.isEmpty()) {
    WiFi.disconnect(false, false);
    attempting = false;
    enableSetupAp();
    return;
  }
  WiFi.mode(apActive ? WIFI_AP_STA : WIFI_STA);
  WiFi.disconnect(false, false);
  WiFi.begin(config.ssid.c_str(), config.open ? nullptr : config.password.c_str());
  attempting = true;
  connectStart = millis();
}

bool validApn(const String& apn) {
  if (apn.length() > 63) return false;
  for (size_t i = 0; i < apn.length(); ++i) {
    const char c = apn[i];
    if (!isalnum(static_cast<unsigned char>(c)) && c != '.' && c != '-') return false;
  }
  return true;
}

const char* saveSettings(const JsonDocument& request) {
  if (!request["ssid"].is<const char*>() || !request["password"].is<const char*>() ||
      !request["apn"].is<const char*>() || !request["open"].is<bool>() ||
      !request["volume"].is<int>()) return "Campi mancanti o non validi.";
  Settings next;
  next.ssid = request["ssid"].as<String>();
  next.password = request["password"].as<String>();
  next.apn = request["apn"].as<String>();
  next.open = request["open"].as<bool>();
  next.volume = request["volume"].as<int>();
  if (next.ssid.length() > 32) return "SSID fino a 32 byte.";
  if (!validApn(next.apn) || next.volume < 0 || next.volume > 100) return "APN o volume non valido.";
  if (next.open || next.ssid.isEmpty()) next.password = "";
  else if (next.password.isEmpty() && next.ssid == config.ssid && !config.open) next.password = config.password;
  if (!next.ssid.isEmpty() && !next.open && (next.password.length() < 8 || next.password.length() > 63)) {
    return "Password Wi-Fi da 8 a 63 byte, oppure seleziona rete aperta.";
  }
  JsonDocument stored;
  stored["ssid"] = next.ssid;
  stored["password"] = next.password;
  stored["apn"] = next.apn;
  stored["open"] = next.open;
  stored["volume"] = next.volume;
  String encoded;
  serializeJson(stored, encoded);
  if (storage.putString("settings", encoded) != encoded.length()) return "Salvataggio non riuscito.";
  const bool wifiChanged = next.ssid != config.ssid || next.password != config.password || next.open != config.open;
  config = next;
  if (wifiChanged) {
    reconnectPending = true;
    reconnectAt = millis() + 900;
  }
  return nullptr;
}

bool playTestTone(int volume) {
  if (volume < 0 || volume > 100) return false;
  i2s_config_t bus{};
  bus.mode = static_cast<i2s_mode_t>(I2S_MODE_MASTER | I2S_MODE_TX);
  bus.sample_rate = 16000;
  bus.bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT;
  bus.channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT;
  bus.communication_format = I2S_COMM_FORMAT_STAND_I2S;
  bus.dma_buf_count = 4;
  bus.dma_buf_len = 128;
  bus.tx_desc_auto_clear = true;
  i2s_pin_config_t pins{};
  pins.mck_io_num = I2S_PIN_NO_CHANGE;
  pins.bck_io_num = 4;
  pins.ws_io_num = 5;
  pins.data_out_num = 6;
  pins.data_in_num = I2S_PIN_NO_CHANGE;
  if (i2s_driver_install(I2S_NUM_0, &bus, 0, nullptr) != ESP_OK) return false;
  bool ok = i2s_set_pin(I2S_NUM_0, &pins) == ESP_OK;
#ifdef PAKY_AUDIO_ENABLE_GPIO
  if (ok) digitalWrite(PAKY_AUDIO_ENABLE_GPIO, HIGH);
#endif
  int16_t stereo[256];
  int sample = 0;
  for (int block = 0; ok && block < 32; ++block) {
    for (size_t i = 0; i < 128; ++i, ++sample) {
      const float ramp = fminf(1.0f, fminf(sample / 150.0f, (4095 - sample) / 150.0f));
      const int16_t pcm = static_cast<int16_t>(ramp * 75.0f * volume * sinf(sample * 0.1727876f));
      stereo[2*i] = stereo[2*i+1] = pcm;
    }
    size_t written = 0;
    ok = i2s_write(I2S_NUM_0, stereo, sizeof(stereo), &written, pdMS_TO_TICKS(40)) == ESP_OK
         && written == sizeof(stereo);
  }
  if (ok) delay(40);
#ifdef PAKY_AUDIO_ENABLE_GPIO
  digitalWrite(PAKY_AUDIO_ENABLE_GPIO, LOW);
#endif
  i2s_driver_uninstall(I2S_NUM_0);
  return ok;
}

String handle(const String& frame, bool usb) {
  JsonDocument request;
  JsonDocument reply;
  reply["paky"] = 1;
  const char* error = nullptr;
  if (frame.length() > FRAME_LIMIT || deserializeJson(request, frame)) {
    error = "Richiesta non valida.";
  } else {
    const String cmd = request["cmd"] | "";
    if (cmd == "save") error = saveSettings(request);
    else if (cmd == "tone") {
      if (!request["volume"].is<int>() || !playTestTone(request["volume"].as<int>())) error = "Tono non riuscito.";
    } else if (cmd == "ap" && usb) {
      if (!enableSetupAp()) error = "Avvio Wi-Fi di configurazione non riuscito.";
    } else if (cmd != "status") error = "Comando sconosciuto.";
  }
  reply["ok"] = error == nullptr;
  if (error) reply["error"] = error;
  else {
    reply["name"] = "Paky76 Rev.B";
    reply["ssid"] = config.ssid;
    reply["open"] = config.open;
    reply["apn"] = config.apn;
    reply["volume"] = config.volume;
    reply["ip"] = WiFi.status() == WL_CONNECTED ? WiFi.localIP().toString() : "";
    reply["ap"] = apActive ? apName : "";
    reply["apIp"] = apActive ? WiFi.softAPIP().toString() : "";
    if (usb) reply["setupKey"] = setupKey;
    reply["lte"] = "Modem non integrato nel firmware di configurazione";
  }
  String encoded;
  serializeJson(reply, encoded);
  return encoded;
}

bool authenticate() {
  if (server.authenticate("paky", setupKey.c_str())) return true;
  server.requestAuthentication(BASIC_AUTH, "Paky76", "Credenziali richieste");
  return false;
}

void processUsb() {
  for (size_t count = 0; count < 256 && Serial.available(); ++count) {
    const char c = static_cast<char>(Serial.read());
    if (c == '\n') {
      if (!discarding && !serialLine.isEmpty()) Serial.println(handle(serialLine, true));
      serialLine = "";
      discarding = false;
    } else if (c != '\r' && !discarding) {
      if (serialLine.length() < FRAME_LIMIT) serialLine += c;
      else discarding = true;
    }
  }
}

void drawScreen() {
  const String ip = WiFi.status() == WL_CONNECTED ? WiFi.localIP().toString() : "";
  String screen = ip + (apActive ? "AP" : "-");
  if (screen == lastScreen) return;
  lastScreen = screen;
  face.fillScreen(TFT_BLACK);
  face.fillRoundRect(62, 40, 34, 28, 11, TFT_CYAN);
  face.fillRoundRect(144, 40, 34, 28, 11, TFT_CYAN);
  face.drawRoundRect(99, 87, 42, 13, 5, TFT_CYAN);
  face.setTextColor(TFT_WHITE, TFT_BLACK);
  face.setTextDatum(TC_DATUM);
  if (apActive) {
    face.drawString(apName, 120, 125, 2);
    face.drawString(String("Codice ") + setupKey, 120, 148, 2);
    face.drawString(WiFi.softAPIP().toString(), 120, 171, 2);
  }
  if (!ip.isEmpty()) face.drawString(String("IP ") + ip, 120, 200, 2);
}
}  // namespace

void setup() {
  Serial.begin(115200);
#ifdef PAKY_AUDIO_ENABLE_GPIO
  pinMode(PAKY_AUDIO_ENABLE_GPIO, OUTPUT);
  digitalWrite(PAKY_AUDIO_ENABLE_GPIO, LOW);
#endif
  face.init();
  face.setRotation(0);
  storage.begin("paky-setup", false);
  loadSettings();
  setupKey = storage.getString("setupKey", "");
  if (setupKey.length() != 12) {
    char secret[13];
    snprintf(secret, sizeof(secret), "%08lx%04lx",
             static_cast<unsigned long>(esp_random()),
             static_cast<unsigned long>(esp_random() & 0xffff));
    setupKey = secret;
    storage.putString("setupKey", setupKey);
  }
  char name[18];
  snprintf(name, sizeof(name), "Paky76-%04X", static_cast<unsigned>(ESP.getEfuseMac() & 0xffff));
  apName = name;
  WiFi.persistent(false);
  WiFi.setAutoReconnect(true);
  connectWifi();
  const char* headers[] = {"X-Paky-Setup"};
  server.collectHeaders(headers, 1);
  server.on("/", HTTP_GET, [] {
    server.sendHeader("Location", "/setup");
    server.send(302);
  });
  server.on("/setup", HTTP_GET, [] {
    if (!authenticate()) return;
    server.sendHeader("Cache-Control", "no-store");
    server.send_P(200, "text/html; charset=utf-8", SETUP_PAGE);
  });
  server.on("/api/config", HTTP_POST, [] {
    if (server.header("X-Paky-Setup") != "1") {
      server.send(403);
      return;
    }
    if (!authenticate()) return;
    server.sendHeader("Cache-Control", "no-store");
    server.send(200, "application/json", handle(server.arg("plain"), false));
  });
  server.begin();
}

void loop() {
  processUsb();
  server.handleClient();
  const unsigned long now = millis();
  if (reconnectPending && static_cast<long>(now - reconnectAt) >= 0) {
    reconnectPending = false;
    connectWifi();
  }
  if (attempting && WiFi.status() == WL_CONNECTED) attempting = false;
  else if (attempting && now - connectStart >= CONNECT_TIMEOUT_MS) {
    attempting = false;
    enableSetupAp();
  }
  if (apActive && now - apStart >= AP_TIMEOUT_MS) {
    WiFi.softAPdisconnect(true);
    apActive = false;
  }
  drawScreen();
  delay(5);
}
