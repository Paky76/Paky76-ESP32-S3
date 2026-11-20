# Selected display — Rev.A

**Selected:** Waveshare 1.3inch LCD Module, SKU 15867, ST7789, 240x240 IPS.

Official sources:
- https://www.waveshare.com/1.3inch-LCD-Module.htm
- https://www.waveshare.com/wiki/1.3inch_LCD_Module

## Electrical interface
| Display signal | Proposed ESP32-S3 GPIO / net |
|---|---|
| VCC | +3V3 |
| GND | GND |
| DIN | GPIO11 / LCD_MOSI |
| CLK | GPIO12 / LCD_SCLK |
| CS | GPIO10 / LCD_CS |
| DC | GPIO9 / LCD_DC |
| RST | GPIO8 / LCD_RST |
| BL | GPIO7 / LCD_BL |

Waveshare specifies 3.3V/5V power, SPI, an 8-pin PH2.0 connector and 45 x 31 mm module dimensions. For a 3.3 V ESP32-S3 system, design around 3.3 V logic and supply. Verify PH2.0 mating connector orientation and pin-1 numbering against physical parts before PCB release. Verify backlight input behavior and current before direct GPIO drive.

## Release blockers
- Exact ESP32-S3-WROOM-1 orderable MPN and KiCad symbol/footprint verification.
- USB-C, ESD, regulator and supporting components selection.
- Mechanical and mating connector verification.
- Completed schematic, routed PCB and passing ERC/DRC.
- BOM, Gerber, drill, pick-and-place and prototype test.

**No fabrication files are approved.**
