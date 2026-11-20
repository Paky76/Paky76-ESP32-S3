# Paky76 Rev.A — Hardware requirements

## Confirmed
- ESP32-S3 controller.
- External ST7789 240x240 display module.
- Fully integrated PCB for industrial assembly.
- KiCad schematic, routed PCB, BOM and manufacturing outputs required.

## Open engineering decisions
1. Exact ESP32-S3 module and flash/PSRAM capacity.
2. USB-only or battery supply.
3. Other peripherals: audio, buttons, sensors and LEDs.
4. Exact ST7789 module connector and pinout.
5. Enclosure, mounting and PCB dimensions.
6. Manufacturer and assembly service.

## Proposed, not approved
- ESP32-S3-WROOM module for simplified RF integration.
- USB-C 5 V input and 3.3 V regulation.
- SPI display connections: SCLK, MOSI, CS, DC, RESET and backlight control.

Do not treat proposals as verified electrical design decisions. Check Espressif and display module datasheets before schematic capture.
