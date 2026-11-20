#include <Arduino.h>
#include <TFT_eSPI.h>
// Prototype-only pin assignment; validate exact breakout before powering.
static TFT_eSPI tft;
void setup() {
  Serial.begin(115200);
  pinMode(TFT_BL, OUTPUT);
  digitalWrite(TFT_BL, HIGH); // Only for compatible 3.3 V BL logic input.
  tft.init();
  tft.setRotation(0);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.setTextDatum(MC_DATUM);
  tft.drawString("PAKY76", 120, 105, 4);
  tft.drawString("Rev.A prototype", 120, 140, 2);
  Serial.println("Display smoke test initialized");
}
void loop() { delay(1000); }
