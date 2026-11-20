# Production acceptance — Paky76 Rev.A

## Current status: BLOCKED
The CI workflow deliberately fails if the real KiCad schematic or PCB is missing. A successful pipeline alone does not establish electrical or manufacturing safety.

## Selected parts
- Controller family: ESP32-S3; proposed module ESP32-S3-WROOM-1-N8, MPN subject to design confirmation.
- Display: Waveshare 1.3inch LCD Module, SKU 15867, 240x240, ST7789, 8-pin PH2.0.
- Power concept: USB-C 5V -> 3.3V regulator; detailed design not yet approved.

## Required evidence before sending to assembly
1. Complete schematic and reviewed component datasheets.
2. Validated KiCad footprints and netlist.
3. Routed PCB with continuous reference plane and ESP32 antenna keepout.
4. Passing ERC and DRC, including schematic/PCB parity.
5. Gerber, Excellon, fabrication drawing, verified stackup.
6. Assembly BOM with purchasable MPNs, centroid file and assembly drawings.
7. Physical prototype bring-up and USB/display/Wi-Fi verification.

## Primary sources
- https://www.waveshare.com/wiki/1.3inch_LCD_Module
- https://docs.kicad.org/9.0/en/cli/cli.html

No reports, gerbers, or fabrication approval are implied by this document.
