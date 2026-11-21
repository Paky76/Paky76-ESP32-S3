#include <Arduino.h>
#include <Wire.h>
#include <U8g2lib.h>
#include <initializer_list>

constexpr uint8_t kSda = 5;
constexpr uint8_t kScl = 6;
constexpr uint8_t kLeft = 2;
constexpr uint8_t kRight = 1;
constexpr unsigned long kIdleMs = 30000;
constexpr unsigned long kRetryMs = 2000;
constexpr unsigned long kFrameMs = 40;

// Change U8G2_R0 to U8G2_R1/R2/R3 if the fitted module is rotated.
U8G2_SH1107_128X128_F_HW_I2C oled(U8G2_R0, U8X8_PIN_NONE, kScl, kSda);
unsigned long lastInput;
unsigned long lastFrame;
unsigned long lastProbe;
bool displayReady;
bool sleeping;

bool startDisplay() {
  for (uint8_t address : {0x3C, 0x3D}) {
    Wire.beginTransmission(address);
    if (Wire.endTransmission() != 0) {
      continue;
    }
    oled.setI2CAddress(address << 1);
    oled.setBusClock(100000);
    oled.begin();
    oled.setContrast(100);
    Serial.printf("SH1107: risposta I2C a 0x%02X\n", static_cast<unsigned>(address));
    return true;
  }
  Serial.println("OLED non rilevato: controllare alimentazione e fili I2C");
  return false;
}

void drawFace(int offset, bool blink) {
  const int height = blink ? 4 : 34;
  oled.clearBuffer();
  oled.drawRBox(25 + offset, 55 - height / 2, 23, height, blink ? 1 : 8);
  oled.drawRBox(80 + offset, 55 - height / 2, 23, height, blink ? 1 : 8);
  oled.drawRBox(55, 84, 18, 4, 2);
  oled.sendBuffer();
}

void setup() {
  Serial.begin(115200);
  pinMode(kLeft, INPUT_PULLUP);
  pinMode(kRight, INPUT_PULLUP);
  Wire.begin(kSda, kScl, 100000);
  delay(100);
  lastProbe = millis();
  displayReady = startDisplay();
  lastInput = millis();
}

void loop() {
  const unsigned long now = millis();
  if (!displayReady) {
    if (now - lastProbe >= kRetryMs) {
      lastProbe = now;
      displayReady = startDisplay();
      lastInput = now;
    }
    delay(10);
    return;
  }

  const bool left = digitalRead(kLeft) == LOW;
  const bool right = digitalRead(kRight) == LOW;
  if (left || right) {
    lastInput = now;
    if (sleeping) {
      oled.setPowerSave(0);
      sleeping = false;
    }
  }

  if (!sleeping && now - lastInput >= kIdleMs) {
    oled.setPowerSave(1);
    sleeping = true;
  }
  if (!sleeping && now - lastFrame >= kFrameMs) {
    const int offset = left == right ? 0 : (left ? -8 : 8);
    drawFace(offset, now % 4000 > 3820);
    lastFrame = now;
  }
  delay(5);
}
