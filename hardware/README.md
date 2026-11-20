# Hardware design workspace — Rev.A

Target: ESP32-S3-WROOM-1-based controller with external Waveshare 1.3inch LCD Module (ST7789, 240x240).

**No KiCad schematic or PCB has yet passed validation.** Do not send this directory to a board manufacturer.

## Provisional net allocation
| Net | ESP32-S3 GPIO | Peripheral |
|---|---:|---|
| LCD_MOSI | 11 | ST7789 DIN |
| LCD_SCLK | 12 | ST7789 CLK |
| LCD_CS | 10 | ST7789 CS |
| LCD_DC | 9 | ST7789 DC |
| LCD_RST | 8 | ST7789 RST |
| LCD_BL | 7 | ST7789 BL (driver TBD) |
| USB_DN | 19 | USB D- |
| USB_DP | 20 | USB D+ |

Verify the exact Waveshare module pin sequence and mating connector orientation before routing. GPIO7 must not be connected directly to a high-current backlight load without checking the module's BL interface.

## Design blocks to capture in KiCad
1. U1 ESP32-S3-WROOM-1, validated footprint and antenna keepout.
2. J1 USB-C receptacle, USB2.0 D+/D-, CC resistors and ESD.
3. U2 3.3 V regulator sized for ESP32-S3 radio bursts and display.
4. Boot/reset circuitry, EN pull-up and programming access.
5. LCD 8-pin PH2.0 mating connector, pin-1 orientation checked.
6. Power decoupling, test points, mounting and mechanical outline.

Manufacturing deliverables are gated on actual KiCad ERC/DRC and independent review.
