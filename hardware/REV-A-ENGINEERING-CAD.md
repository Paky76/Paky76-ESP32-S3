# Paky76 Rev.A engineering candidate for supplier DFM

Open `Paky76-RevA-engineering.kicad_pro` in KiCad 9. The carrier is 58 × 42 mm with four copper layers, a continuous In1.Cu ground reference and an ESP32-S3-WROOM-1-N8 antenna overhanging the north edge. The files are at the design-for-manufacture review stage. BOM and fabrication approval remain pending.

## Fabrication assumptions

- Evaluate JLCPCB four-layer 1.6 mm controlled-impedance FR-4, with the 3313 stack-up as the starting point for the USB impedance review. Request supplier stack-up confirmation and a 90 Ω differential calculation for the nominal 0.18 mm USB track width and measured gaps. Breakout, ESD fanout and length compensation change the gap locally. Verify impedance against 90 Ω ±10% before authorizing tooling.
- The front-layer copper lengths are 30.950 mm for D− and 31.004 mm for D+. The short connector-orientation branches run on different layers and have additional lengths and via transitions. These copper lengths do not establish total electrical skew, impedance or performance.
- Board minima are 0.20 mm plated drill and 0.42 mm via diameter. JLCPCB publishes manufacturing capability for these dimensions, with an extra-cost option below 0.45 mm via diameter for 0.20 mm drilling. Confirm that option and the assembly treatment of the twelve module ground-pad holes with the quoting engineer. Review paste apertures and solder wicking under U1.
- J1 and U1 use project copies of the KiCad footprints with edge-facing silkscreen strokes removed. The U1 antenna rule area covers all four copper layers. Pad, paste and drill geometry are retained. Original footprints are from the [KiCad footprint library](https://gitlab.com/kicad/libraries/kicad-footprints).
- `bom-reva-dfm.csv` contains a candidate MPN for every assembly position and the external display. Verify stock, acceptable substitutes, centroid rotations and all package land patterns with the supplier. J2 is through hole. Confirm manual or selective soldering and assembly of J1's shield tabs.

## Electrical and mechanical release checks

1. Confirm end-to-end cable continuity and latch orientation on a Waveshare 15867 sample before connecting the display. J2 assumes pins 1–8 map to VCC, GND, DIN, CLK, CS, DC, RST and BL. Record actual supply and BL input current and verify compatible logic thresholds before configuring GPIO7 as an output. The firmware leaves backlight control disabled.
2. Confirm 3.3 V stability under Wi-Fi transmit and display load, using the supplier's populated stack-up, selected production capacitors and a representative USB source. The TLV75733PDBVR LDO dissipates 0.85 W at 5 V in and 500 mA out. Verify effective capacitance and regulator junction temperature from the measured load and board thermal environment. Check startup inrush and host current limits. Reassess topology if margins are inadequate.
3. Verify enclosure fit, USB plug access, connector insertion clearance, display harness routing and the antenna clearance recommended by Espressif. SW1 is reset and SW2 pulls GPIO0 low for USB download mode.
4. For an initial five-unit pilot, inspect polarity and soldering before power-up. With a current-limited supply verify the 3.3 V rail and boot current on each unit. Check USB enumeration and flashing in both plug orientations, reset/recovery, a display color pattern, BLE discovery, Wi-Fi reconnect and transmit under load. Record rail minimum, peak current and regulator temperature at sustained load. Repeat in the enclosure and retain serial logs by unit. Production approval requires documented results and engineering sign-off.

## KiCad verification

```sh
kicad-cli sch erc --exit-code-violations -o /tmp/paky76-erc.txt hardware/Paky76-RevA-engineering.kicad_sch
kicad-cli pcb drc --schematic-parity --exit-code-violations -o /tmp/paky76-drc.txt hardware/Paky76-RevA-engineering.kicad_pcb
```

KiCad 9.0.2 returned zero ERC findings, zero DRC findings, zero unconnected items and zero schematic-parity findings under the stated board rules. Keep the production gate closed until the approved native release sources, BOM, and sign-off are in place.

## Manufacturer references

- [Espressif ESP32-S3 PCB layout](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html)
- [Waveshare SKU 15867](https://www.waveshare.com/1.3inch-LCD-Module.htm)
- [TI TLV757P datasheet](https://www.ti.com/lit/ds/symlink/tlv757p.pdf)
- [TI TPD2EUSB30 datasheet](https://www.ti.com/lit/ds/symlink/tpd2eusb30.pdf)
- [JLCPCB fabrication capabilities](https://jlcpcb.com/capabilities/pcb-capabilities)
- [JLCPCB controlled impedance stack-ups](https://jlcpcb.com/impedance)
