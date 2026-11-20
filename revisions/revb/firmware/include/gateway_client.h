#pragma once

#include <Arduino.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <time.h>

#if __has_include("gateway_config.local.h")
#include "gateway_config.local.h"
#endif

#ifndef PAKY_GATEWAY_URL
#define PAKY_GATEWAY_URL ""
#define PAKY_GATEWAY_TOKEN ""
#define PAKY_GATEWAY_NTP ""
#define PAKY_GATEWAY_CA_PEM ""
#endif

namespace paky_gateway {
constexpr size_t MAX_REPLY_BYTES = 24576;

inline bool configured() {
  return String(PAKY_GATEWAY_URL).startsWith("https://") &&
         strlen(PAKY_GATEWAY_TOKEN) >= 24 && strlen(PAKY_GATEWAY_CA_PEM) != 0;
}

inline void startClock() {
  if (configured() && strlen(PAKY_GATEWAY_NTP) != 0) configTime(0, 0, PAKY_GATEWAY_NTP);
}

inline String ask(const String& prompt, String& error) {
  if (!configured()) {
    error = "Gateway HTTPS da configurare nel firmware.";
    return {};
  }
  if (WiFi.status() != WL_CONNECTED) {
    error = "Collega Paky76 al Wi-Fi prima di usare il gateway.";
    return {};
  }
  if (time(nullptr) < 1704067200) {
    error = "Ora non sincronizzata. Controlla il server NTP configurato.";
    return {};
  }
  WiFiClientSecure connection;
  connection.setCACert(PAKY_GATEWAY_CA_PEM);
  connection.setHandshakeTimeout(8);
  HTTPClient http;
  http.setConnectTimeout(5000);
  http.setTimeout(30000);
  http.setFollowRedirects(HTTPC_DISABLE_FOLLOW_REDIRECTS);
  http.useHTTP10(true);
  if (!http.begin(connection, PAKY_GATEWAY_URL)) {
    error = "URL del gateway non valido.";
    return {};
  }
  http.addHeader("Authorization", String("Bearer ") + PAKY_GATEWAY_TOKEN);
  http.addHeader("Content-Type", "application/json");
  JsonDocument payload;
  payload["prompt"] = prompt;
  String body;
  serializeJson(payload, body);
  const int status = http.POST(body);
  String result;
  if (status == 401) error = "Token del dispositivo rifiutato.";
  else if (status != 200) error = "Gateway o modello non raggiungibile.";
  else if (http.getSize() <= 0 || static_cast<size_t>(http.getSize()) > MAX_REPLY_BYTES) {
    error = "Risposta del gateway senza lunghezza valida.";
  } else {
    JsonDocument reply;
    if (deserializeJson(reply, http.getStream())) error = "Risposta del gateway non valida.";
    else {
      result = reply["text"] | "";
      if (result.isEmpty()) error = "Il gateway non ha restituito testo.";
    }
  }
  http.end();
  return result;
}
}  // namespace paky_gateway
