#include <Wire.h>

constexpr int kSda = 5;
constexpr int kScl = 6;
constexpr int kLeft = 2;
constexpr int kRight = 1;
constexpr unsigned long kIdleMs = 30000;
uint8_t oled;
uint8_t screen[8][128];
unsigned long lastInput;
unsigned long lastFrame;
bool sleeping;

void command(uint8_t value) {
  Wire.beginTransmission(oled);
  Wire.write(0x00);
  Wire.write(value);
  Wire.endTransmission();
}

bool findDisplay() {
  for (uint8_t address : {0x3C, 0x3D}) {
    Wire.beginTransmission(address);
    if (Wire.endTransmission() == 0) {
      oled = address;
      return true;
    }
  }
  return false;
}

void flushDisplay() {
  for (uint8_t page = 0; page < 8; page++) {
    command(0xB0 | page);
    command(0x10);
    command(0x02);
    for (uint8_t x = 0; x < 128; x += 16) {
      Wire.beginTransmission(oled);
      Wire.write(0x40);
      Wire.write(screen[page] + x, 16);
      Wire.endTransmission();
    }
  }
}

void drawFace(int look, bool blink) {
  memset(screen, 0, sizeof(screen));
  for (int center : {44 + look, 84 + look}) {
    int height = blink ? 2 : 12;
    for (int y = 29 - height; y <= 29 + height; y++) {
      int width = abs(y - 29) > height - 3 ? 5 : 8;
      for (int x = center - width; x <= center + width; x++) {
        screen[y / 8][x] |= 1 << (y % 8);
      }
    }
  }
  for (int x = 60; x <= 68; x++) screen[5][x] |= 1 << 6;
  flushDisplay();
}

void setup() {
  Serial.begin(115200);
  pinMode(kLeft, INPUT_PULLUP);
  pinMode(kRight, INPUT_PULLUP);
  Wire.begin(kSda, kScl);
  Wire.setClock(100000);
  delay(50);
  if (!findDisplay()) {
    Serial.println("SH1106 non rilevato: controllare alimentazione, I2C, reset e cablaggio.");
    return;
  }
  const uint8_t init[] = {
    0xAE, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40, 0xAD, 0x8B,
    0xA1, 0xC8, 0xDA, 0x12, 0x81, 0x60, 0xD9, 0x22, 0xDB, 0x35,
    0xA4, 0xA6
  };
  for (uint8_t value : init) command(value);
  drawFace(0, false);
  command(0xAF);
  lastInput = millis();
}

void loop() {
  if (!oled) {
    delay(250);
    return;
  }
  const unsigned long now = millis();
  const bool left = digitalRead(kLeft) == LOW;
  const bool right = digitalRead(kRight) == LOW;
  if (left || right) {
    lastInput = now;
    if (sleeping) {
      command(0xAF);
      sleeping = false;
    }
  }
  if (!sleeping && now - lastInput >= kIdleMs) {
    command(0xAE);
    sleeping = true;
  }
  if (!sleeping && now - lastFrame >= 120) {
    drawFace(left == right ? 0 : left ? -8 : 8, (now % 4000) > 3820);
    lastFrame = now;
  }
  delay(10);
}
