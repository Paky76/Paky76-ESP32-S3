# Paky76 Rev.A — MVP scope frozen (2026-11-20)

## Included
- ESP32-S3-WROOM-1 module with integrated 2.4 GHz Wi-Fi and Bluetooth LE.
- External Waveshare 1.3inch LCD Module (SKU 15867, ST7789, 240x240) on SPI.
- USB-C receptacle for 5 V power and USB 2.0 native programming/data.
- Onboard 3.3 V regulator, EN/reset and BOOT buttons.
- Industrially assembled controller PCB; display remains a separate module.

## Excluded
- Battery, charger, speaker, microphone, camera, sensors and additional accessories.
- Unverified replication of Troko Desk features.

## Proposed firmware connections
LCD_MOSI=GPIO11; LCD_SCLK=GPIO12; LCD_CS=GPIO10; LCD_DC=GPIO9; LCD_RST=GPIO8; LCD_BL=GPIO7.
USB_D-=GPIO19; USB_D+=GPIO20.

## Open items that block fabrication
Exact ESP32-S3-WROOM-1 variant, USB-C and regulator MPNs, 8-pin mating connector orientation, backlight electrical requirements, PCB outline and mounting requirements. These must be resolved against manufacturer documentation and KiCad library footprints.

## Definition of done
Real KiCad schematic and routed PCB; independently reviewed electrical design; passing ERC/DRC and parity; exported Gerber/Excellon/BOM/placement files; physical prototype tested for boot, USB, display, Wi-Fi and Bluetooth LE.

**This file freezes the feature scope, not the manufacturing design.**
