# Paky76 Rev.A — ST7789 external module interface (PROVISIONAL)

**Status: engineering assumption, NOT validated for fabrication.**

The external 240×240 ST7789 SPI display is attached to the eight-position 2.54 mm header `J_LCD`. This header mapping assumes a breakout marked `GND VCC SCL SDA RES DC CS BLK`, in that order. **Different ST7789 modules have different pin orders and voltage requirements. Do not order a PCB or plug in a display until the exact module part number, pin order, power voltage, and backlight electrical characteristics have been checked.**

| J_LCD pad | Assumed module marking | PCB net | ESP32-S3 GPIO |
|---|---|---|---|
| 1 | GND | GND | — |
| 2 | VCC | +3V3 | — |
| 3 | SCL / SCK | LCD_SCLK | GPIO12 |
| 4 | SDA / DIN | LCD_MOSI | GPIO11 |
| 5 | RES / RST | LCD_RST | GPIO8 |
| 6 | DC / A0 | LCD_DC | GPIO9 |
| 7 | CS | LCD_CS | GPIO10 |
| 8 | BLK / LED | LCD_BL | GPIO7 |

## Required before production

1. Record exact manufacturer, display module part number, pinout photograph and datasheet.
2. Confirm whether the module's logic and supply are 3.3 V compatible.
3. Determine LED/backlight current and whether a transistor/current-limiting stage is necessary; **do not assume direct GPIO drive is acceptable**.
4. Verify connector orientation and physical location against enclosure and cable.
5. Complete native schematic and routing; validate ERC and DRC before generating production outputs.

The current PCB only assigns **net names to pads**. This does **not** mean these nets are connected by copper tracks. The board remains a non-fabrication placement study.
