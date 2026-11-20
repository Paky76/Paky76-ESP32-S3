# Paky76 Rev.A — USB-C power and native USB design rules

**Design intent only; NOT a released schematic.**

- Sink-only USB-C receptacle. Each CC pin (CC1 and CC2) requires its own 5.1 kΩ pull-down to ground. Do not short CC1 and CC2 together.
- USB D+ and D− connect to ESP32-S3 GPIO20 and GPIO19 respectively; confirm pin mapping against the selected ESP32-S3-WROOM-1 datasheet and USB-C receptacle footprint.
- Connect duplicate USB-C A/B D+ pads together and duplicate A/B D− pads together as required by the chosen receptacle.
- Select an appropriate USB ESD protection device, placed close to the connector; verify capacitance and working voltage.
- 5 V VBUS requires input protection and a selected 3.3 V regulator sized for ESP32-S3 transmit peaks and LCD load. The regulator's stability and capacitors must follow its own datasheet.
- EN must have a valid power-on/reset network. GPIO0 must have a safe boot strap and BOOT button. Avoid unverified loads on strapping pins.
- Observe ESP32-S3-WROOM-1 antenna keep-out, power-plane guidance and placement recommendations in Espressif hardware design guidelines.
- The ST7789 module backlight connection is not approved for direct GPIO drive without verifying its circuitry and current.

## Manufacturer references
- Espressif ESP32-S3 hardware design guidelines: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/
- USB Type-C specifications and connector manufacturer's datasheet
- Waveshare 1.3inch LCD Module: https://www.waveshare.com/wiki/1.3inch_LCD_Module

## Release blocker
This is an engineering checklist, not a verified CAD drawing. Do not fabricate until schematic, PCB and KiCad ERC/DRC have passed and physical prototype testing is complete.
