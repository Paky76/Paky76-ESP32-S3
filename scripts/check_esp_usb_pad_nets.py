#!/usr/bin/env python3
"""Check native ESP32-S3 USB/3V3/GND net assignments against expected physical pads.
This is NOT an ERC/DRC or proof of routed connectivity.
"""
import sys
import pcbnew as pcb
board=pcb.LoadBoard("hardware/Paky76-RevA-placement-study.kicad_pcb")
fps={f.GetReference():f for f in board.GetFootprints()}
expected={"U1":{"1":"GND","2":"+3V3","13":"USB_DN","14":"USB_DP"},
          "J_USB":{"A7":"USB_DN","B7":"USB_DN","A6":"USB_DP","B6":"USB_DP"}}
for ref,mapping in expected.items():
    if ref not in fps:sys.exit("Missing footprint "+ref)
    for number,net in mapping.items():
        pads=[p for p in fps[ref].Pads() if p.GetNumber()==number]
        if not pads or any(p.GetNetname()!=net for p in pads):
            sys.exit("Invalid mapping: %s.%s should be %s"%(ref,number,net))
print("Native USB D+/D- and ESP32-S3 pad net names verified.")
print("NOT ROUTED: missing schematic, USB ESD protection, EN/BOOT and final power connections.")
