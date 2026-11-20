#pragma once

#include <Arduino.h>
#include <HTTPClient.h>
#include <Update.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <esp_ota_ops.h>
#include <mbedtls/pk.h>
#include <mbedtls/sha256.h>
#include <time.h>

#if __has_include("ota_config.local.h")
#include "ota_config.local.h"
#endif
#ifndef PAKY_OTA_PUBLIC_KEY_PEM
#define PAKY_OTA_PUBLIC_KEY_PEM ""
#define PAKY_OTA_URL ""
#define PAKY_OTA_CA_PEM ""
#define PAKY_OTA_NTP ""
#endif

#define PAKY_OTA_STRING_IMPL(x) #x
#define PAKY_OTA_STRING(x) PAKY_OTA_STRING_IMPL(x)

namespace paky_ota {
constexpr uint32_t VERSION = PAKY_FW_VERSION;
#ifdef PAKY_AUDIO_ENABLE_GPIO
constexpr uint32_t TARGET = 2;
constexpr char BUILD_MARKER[] = "PAKYFW:" PAKY_OTA_STRING(PAKY_FW_VERSION) ":2";
#else
constexpr uint32_t TARGET = 1;
constexpr char BUILD_MARKER[] = "PAKYFW:" PAKY_OTA_STRING(PAKY_FW_VERSION) ":1";
#endif
constexpr size_t SIGNED_SIZE = 52;
constexpr size_t SIGNATURE_SPACE = 80;
constexpr size_t HEADER_SIZE = SIGNED_SIZE + 2 + SIGNATURE_SPACE;
constexpr unsigned long INTERVAL_MS = 6UL * 60 * 60 * 1000;

inline bool canUpload() { return strlen(PAKY_OTA_PUBLIC_KEY_PEM) != 0; }
inline bool canDownload() {
  return canUpload() && String(PAKY_OTA_URL).startsWith("https://") && strlen(PAKY_OTA_CA_PEM) != 0;
}
inline uint32_t read32(const uint8_t* p) {
  return (uint32_t(p[0]) << 24) | (uint32_t(p[1]) << 16) | (uint32_t(p[2]) << 8) | p[3];
}
inline bool validSignature(const uint8_t* header) {
  const size_t len = (size_t(header[SIGNED_SIZE]) << 8) | header[SIGNED_SIZE + 1];
  if (!len || len > SIGNATURE_SPACE) return false;
  uint8_t digest[32];
  if (mbedtls_sha256_ret(header, SIGNED_SIZE, digest, 0) != 0) return false;
  mbedtls_pk_context pub;
  mbedtls_pk_init(&pub);
  const bool valid = mbedtls_pk_parse_public_key(&pub,
      reinterpret_cast<const unsigned char*>(PAKY_OTA_PUBLIC_KEY_PEM),
      strlen(PAKY_OTA_PUBLIC_KEY_PEM) + 1) == 0 &&
      mbedtls_pk_can_do(&pub, MBEDTLS_PK_ECDSA) &&
      mbedtls_pk_verify(&pub, MBEDTLS_MD_SHA256, digest, sizeof(digest), header + SIGNED_SIZE + 2, len) == 0;
  mbedtls_pk_free(&pub);
  return valid;
}

struct Install {
  uint8_t header[HEADER_SIZE]{};
  size_t headerRead = 0, expected = 0, received = 0;
  bool writing = false;
  const char* error = nullptr;
  mbedtls_sha256_context sha;

  Install() { mbedtls_sha256_init(&sha); }
  ~Install() { if (writing) Update.abort(); mbedtls_sha256_free(&sha); }
  Install(const Install&) = delete;
  Install& operator=(const Install&) = delete;

  bool fail(const char* reason) {
    if (writing) Update.abort();
    writing = false;
    error = reason;
    return false;
  }

  bool feed(uint8_t* data, size_t size) {
    if (error) return false;
    if (headerRead < HEADER_SIZE) {
      const size_t take = min(size, HEADER_SIZE - headerRead);
      memcpy(header + headerRead, data, take);
      headerRead += take;
      data += take;
      size -= take;
      if (headerRead < HEADER_SIZE) return true;
      if (memcmp(header, "PAKYOTA1", 8) != 0 || read32(header + 8) != TARGET) {
        return fail("Pacchetto o variante hardware incompatibile.");
      }
      if (!canUpload() || !validSignature(header)) return fail("Firma non valida.");
      if (read32(header + 12) <= VERSION) return fail("Versione già installata o precedente.");
      expected = read32(header + 16);
      const auto* slot = esp_ota_get_next_update_partition(nullptr);
      if (!expected || !slot || expected > slot->size) return fail("Firmware oltre la capacità dello slot OTA.");
      if (mbedtls_sha256_starts_ret(&sha, 0) != 0) return fail("Inizializzazione hash non riuscita.");
      if (!Update.begin(expected, U_FLASH)) return fail("Impossibile iniziare la scrittura OTA.");
      writing = true;
    }
    if (!size) return true;
    if (size > expected - received) return fail("Il pacchetto contiene dati in eccesso.");
    if (mbedtls_sha256_update_ret(&sha, data, size) != 0 || Update.write(data, size) != size) {
      return fail("Scrittura OTA non riuscita.");
    }
    received += size;
    return true;
  }

  bool commit() {
    if (error) return false;
    if (!writing || received != expected) return fail("Pacchetto incompleto.");
    uint8_t digest[32];
    if (mbedtls_sha256_finish_ret(&sha, digest) != 0 || memcmp(digest, header + 20, 32) != 0) {
      return fail("Integrità firmware non verificata.");
    }
    if (!Update.end()) return fail("Impossibile attivare il firmware.");
    writing = false;
    return true;
  }

  size_t bundleSize() const { return HEADER_SIZE + expected; }
};

inline bool download() {
  if (!canDownload() || WiFi.status() != WL_CONNECTED || time(nullptr) < 1704067200) return false;
  WiFiClientSecure connection;
  connection.setCACert(PAKY_OTA_CA_PEM);
  connection.setHandshakeTimeout(8);
  HTTPClient http;
  http.setConnectTimeout(5000);
  http.setTimeout(7000);
  http.setFollowRedirects(HTTPC_DISABLE_FOLLOW_REDIRECTS);
  http.useHTTP10(true);
  if (!http.begin(connection, PAKY_OTA_URL)) return false;
  const int status = http.GET();
  const int length = http.getSize();
  const auto* slot = esp_ota_get_next_update_partition(nullptr);
  if (status != 200 || length <= static_cast<int>(HEADER_SIZE) || !slot ||
      static_cast<size_t>(length) > slot->size + HEADER_SIZE) {
    http.end();
    return false;
  }
  Install updater;
  uint8_t buffer[1024];
  auto& stream = http.getStream();
  size_t remaining = static_cast<size_t>(length);
  const unsigned long start = millis();
  while (remaining && millis() - start < 90000) {
    const size_t count = stream.readBytes(buffer, min(remaining, sizeof(buffer)));
    if (!count || !updater.feed(buffer, count)) break;
    remaining -= count;
  }
  const bool installed = remaining == 0 && updater.bundleSize() == static_cast<size_t>(length) && updater.commit();
  http.end();
  return installed;
}
}  // namespace paky_ota
