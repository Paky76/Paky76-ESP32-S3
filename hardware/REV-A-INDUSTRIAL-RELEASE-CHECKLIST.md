# Paky76 Rev.A — Industrial prototype release checklist

**Current classification: NOT READY FOR FABRICATION.** A successful GitHub Actions *placement study* does not establish that the board is safe, electrically complete, manufacturable or approved.

## Confirmed from generated PCB study
- 50 × 45 mm provisional outline, ESP32-S3-WROOM-1-N8 module, USB-C receptacle, candidate 3.3 V regulator, passive parts and 8-pin ST7789 header.
- Two preliminary copper segments only. Most nets remain unrouted.
- Latest passing placement study CI: 36 unconnected items; 12 drill-size violations; 11 silkscreen overlaps; 5 silkscreen-over-copper; 1 courtyard overlap. Zero reported copper shorts. **65 DRC findings remain.**
- Provisional ST7789 header: GND, 3V3, SCLK, MOSI, RESET, DC, CS, BL. Pin order has **not** been verified against a purchased module.

## Required design work (not completed)
1. Create a **single integrated native KiCad schematic** using actual manufacturer-matched symbols and pin numbers, not the existing logical-interface prototypes. Verify ESP32-S3-WROOM-1-N8, AP2112K-3.3, USB-C and display header pinouts.
2. Decide and document USB-C sink implementation: CC1/CC2 5.1 kΩ to GND, USB D+/D− routing and impedance, ESD protection, VBUS protection/fusing as appropriate, shield strategy and USB boot/programming method.
3. Validate regulator dropout, 5 V input tolerance, worst-case ESP32-S3 Wi-Fi peak current, ST7789 module supply and backlight current, dissipation and capacitor ESR/stability. Confirm 3.3 V rail current budget.
4. Add or explicitly waive accessible RESET/EN and BOOT controls; ensure reliable flashing and recovery. Verify boot strapping and power-up sequencing.
5. Select the **exact ST7789 breakout module**, verify 8-pin order, header orientation and backlight driver; GPIO7 direct LED drive is **not approved** without electrical characterization.
6. Rework ESP32 antenna location and RF keep-out per Espressif's exact module integration guidance; avoid copper and components in antenna region and validate mechanical enclosure clearance.
7. Complete all power, ground, USB, EN/BOOT and SPI copper routing with appropriate return paths, trace widths, vias, decoupling placement and copper zones. Review signal integrity and DFM.
8. Resolve **all** KiCad ERC and DRC violations. In particular, 12 0.20 mm drill violations on the ESP module's exposed pad must be reconciled with footprint documentation and the selected PCB vendor's capability. Do not silently suppress them.
9. Finalize BOM with exact MPN, quantities, approved substitutes, distributor availability, assembly side and orientation; confirm USB and regulator footprint-to-part matches.
10. Perform design review: fabrication stack-up, copper weight, minimum drill, annular rings, solder mask expansion, fiducials, test pads, assembly stencil and panelization.
11. Run ERC/DRC and independent visual checks. Only then export Gerbers, Excellon, pick-and-place, approved BOM, assembly drawing, schematic PDF and firmware programming/test instructions.
12. Order a small pilot build, measure 3.3 V under load, USB enumeration, Wi-Fi/BLE performance, SPI display operation, backlight, power/thermal behavior and repeatability before volume manufacturing.

## Automated production gate
`python3 scripts/manufacturing_readiness.py --drc release/final-drc.txt` **must fail** until native final schematic/PCB, clean reports, approved BOM and engineering sign-off exist. `bash scripts/export_fabrication_package.sh` exports manufacturing outputs **only after** this gate passes.

## External decisions needed
- Exact ST7789 240×240 module manufacturer, product link or clear photo of the 8-pin markings and backside.
- Physical dimensions and connector location required for the enclosure, including USB-C access and display cable length.
- Target assembly vendor (e.g., PCB fab/PCBA service) to validate drilling and component availability.

No file currently in this repository is approved for industrial manufacture.
