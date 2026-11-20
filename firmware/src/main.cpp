#include <Arduino.h>
#include <WiFi.h>
#include <TFT_eSPI.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

// Paky76 Rev.A - initial ESP32-S3 Wi-Fi/BLE/display bring-up.
// LCD wiring, 3.3 V supply and display backlight are NOT validated.
static TFT_eSPI tft;
static uint32_t lastReportMs = 0;
static bool bleStarted = false;

static void startBle() {
  BLEDevice::init("PAKY76-RevA");
  BLEServer *server = BLEDevice::createServer();
  BLEAdvertising *advertising = BLEDevice::getAdvertising();
  advertising->setScanResponse(true);
  advertising->start();
  bleStarted = true;
  (void)server;
  Serial.println("BLE advertising started: PAKY76-RevA");
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\nPAKY76 Rev.A - Wi-Fi/BLE/LCD bring-up");
  Serial.printf("Chip: %s, revision: %u\n", ESP.getChipModel(), ESP.getChipRevision());
  Serial.printf("Flash: %u bytes, heap: %u bytes\n",
                ESP.getFlashChipSize(), ESP.getFreeHeap());

  WiFi.mode(WIFI_STA);
  Serial.printf("Wi-Fi STA MAC: %s\n", WiFi.macAddress().c_str());
  startBle();

  // IMPORTANT: do not drive TFT_BL until the backlight electrical
  // interface has been verified against the exact display module.
  tft.init();
  tft.setRotation(0);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.setTextDatum(MC_DATUM);
  tft.drawString("PAKY76", 120, 105, 4);
  tft.drawString("WiFi + BLE", 120, 140, 2);
  Serial.println("LCD initialization attempted; physical test pending.");
}

void loop() {
  if (millis() - lastReportMs >= 5000) {
    lastReportMs = millis();
    Serial.printf("Uptime=%lu ms; heap=%u; BLE=%s\n",
                  (unsigned long)millis(), ESP.getFreeHeap(),
                  bleStarted ? "advertising" : "not started");
  }
  delay(100);
}
