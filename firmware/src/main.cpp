#include <Arduino.h>
#include <WiFi.h>
#include <TFT_eSPI.h>

// REV.A bring-up firmware. Display connector and backlight must be verified
// electrically before connecting the external LCD module.
static TFT_eSPI tft;
static uint32_t lastReportMs = 0;

void setup() {
  Serial.begin(115200);
  delay(300);
  Serial.println("\nPAKY76 Rev.A - bring-up");
  Serial.printf("Chip: %s, revision: %u\n", ESP.getChipModel(), ESP.getChipRevision());
  Serial.printf("Flash size: %u bytes\n", ESP.getFlashChipSize());
  Serial.printf("Free heap: %u bytes\n", ESP.getFreeHeap());

  // No backlight GPIO is driven until its electrical interface is verified.
  WiFi.mode(WIFI_STA);
  Serial.printf("Wi-Fi MAC: %s\n", WiFi.macAddress().c_str());
  Serial.println("BLE radio supported by ESP32-S3; BLE test pending.");
  tft.init();
  tft.setRotation(0);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.setTextDatum(MC_DATUM);
  tft.drawString("PAKY76", 120, 105, 4);
  tft.drawString("Rev.A - bring-up", 120, 140, 2);
  Serial.println("LCD initialization attempted (not hardware verified).");
}

void loop() {
  if (millis() - lastReportMs >= 5000) {
    lastReportMs = millis();
    Serial.printf("Uptime: %lu ms; heap: %u bytes\n",
                  (unsigned long)millis(), ESP.getFreeHeap());
  }
  delay(100);
}
