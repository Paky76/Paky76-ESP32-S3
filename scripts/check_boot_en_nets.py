#!/usr/bin/env python3
"""Validate preliminary ESP32-S3 EN and GPIO0 boot pull-up pad net assignments."""
import sys
import pcbnew as pcb
b=pcb.LoadBoard("hardware/Paky76-RevA-placement-study.kicad_pcb")
fps={f.GetReference():f for f in b.GetFootprints()}
mapping={
"U1":{"3":"ESP_EN","27":"ESP_GPIO0_BOOT"},
"R_EN":{"1":"+3V3","2":"ESP_EN"},
"C_EN":{"1":"ESP_EN","2":"GND"},
"R_BOOT":{"1":"+3V3","2":"ESP_GPIO0_BOOT"},
}
for ref,pads in mapping.items():
    if ref not in fps:sys.exit("Missing "+ref)
    for number,expected in pads.items():
        matches=[p for p in fps[ref].Pads() if p.GetNumber()==number]
        if len(matches)!=1 or matches[0].GetNetname()!=expected:
            sys.exit("Incorrect EN/BOOT pad net %s.%s expected %s"%(ref,number,expected))
print("Provisional EN and BOOT pad assignments validated.")
print("No reset/boot switches, USB auto-download, trace connectivity or ERC/DRC validated.")
