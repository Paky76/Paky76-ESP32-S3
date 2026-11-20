# Paky76 Rev.A integrated engineering CAD

Open `Paky76-RevA-engineering.kicad_pro` in KiCad 9. The project contains an integrated circuit schematic and a partially routed 58 × 42 mm four-layer carrier PCB. Its dimensions and placement are provisional. The manufacturing gate remains closed.

## Circuit choices

- U1 is the ESP32-S3-WROOM-1-N8. Its antenna overhangs the north carrier edge. Confirm clearance around the antenna in the final housing. In1.Cu provides a ground reference plane.
- J1 uses the HRO TYPE-C-31-M-12 footprint with separate 5.1 kΩ Rd resistors. U3 is a TPD2EUSB30DRTR in the TI DRT-3 package. D+/D− breakout, the ESD connection and the route to GPIO20/GPIO19 remain open. Route against the selected stack-up, with a continuous ground reference and target differential impedance of 90 Ω ±10%.
- U2 is a candidate TLV75733PDBVR 3.3 V LDO. At a nominal 5 V input its dissipation is 1.7 W per ampere of output current, or 0.85 W at 500 mA. The maximum output-current rating alone does not establish thermal headroom. Check host current allowance, input inrush including cable and module capacitance, 3.3 V transient droop, effective ceramic capacitance, PCB thermal resistance and enclosure temperature. Reassess the regulator topology if the resulting margins are inadequate.
- SW1 pulls EN low and SW2 pulls GPIO0 low. The EN time constant is nominally 10 ms. Verify power-up and download mode under actual USB ramp and reconnect conditions.
- J2 is a candidate 2 mm JST PH carrier connector for Waveshare SKU 15867. The schematic maps its pins 1–8 to VCC, GND, DIN, CLK, CS, DC, RST and BL in the order of the published signals. The manufacturer table lists signals without establishing the physical pin numbering of the mating cable. Verify connector compatibility, latch orientation and cable continuity before freezing J2. R5 is a candidate series resistor for a logic-level BL input. Characterize BL voltage, polarity and current before assigning the GPIO as an output. The firmware build deliberately leaves the TFT_eSPI backlight macro undefined during this check.

## Reproduce the engineering checks

```sh
kicad-cli sch erc --exit-code-violations -o /tmp/paky76-erc.txt hardware/Paky76-RevA-engineering.kicad_sch
kicad-cli pcb drc --schematic-parity --exit-code-violations -o /tmp/paky76-drc.txt hardware/Paky76-RevA-engineering.kicad_pcb
```

KiCad 9.0.2 recorded zero ERC findings, zero schematic parity findings, six open USB connections and 19 other DRC findings. The remaining findings include twelve 0.20 mm drills in the module footprint, a footprint-library mismatch warning on U1 and six silkscreen findings. Confirm the fab's drill capabilities and investigate the footprint mismatch before release. No short, track crossing, or copper clearance violation was reported for the routed portions in this run.

Finish USB routing and PCB DFM, approve the BOM and mechanical envelope, and rerun ERC, DRC and schematic parity on the release sources. Run physical pilot tests for power, USB boot and enumeration, LCD, RF and thermal behavior before volume production.

## Manufacturer references

- [Espressif ESP32-S3 PCB layout](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html)
- [Waveshare SKU 15867](https://www.waveshare.com/1.3inch-LCD-Module.htm)
- [TI TLV757P datasheet](https://www.ti.com/lit/ds/symlink/tlv757p.pdf)
- [TI TPD2EUSB30 datasheet](https://www.ti.com/lit/ds/symlink/tpd2eusb30.pdf)
