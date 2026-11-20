#!/usr/bin/env python3
"""Verify KiCad native PCB pad net assignments for a USB-C 5 V sink study.
Checks pad numbers and net names, NOT trace routing, ERC or DRC.
"""
import sys
import pcbnew as pcb
b=pcb.LoadBoard("hardware/Paky76-RevA-placement-study.kicad_pcb")
fps={f.GetReference():f for f in b.GetFootprints()}
required={"J_USB","R_CC1","R_CC2"}
if not required.issubset(fps):sys.exit("Missing USB-C or CC footprints")
def check(ref,pad,expected):
    matches=[p for p in fps[ref].Pads() if p.GetNumber()==pad]
    if not matches:sys.exit("Missing pad %s.%s"%(ref,pad))
    for p in matches:
        if p.GetNetname()!=expected:
            sys.exit("Wrong net %s.%s: %r != %r"%(ref,pad,p.GetNetname(),expected))
for n in ("A1","A12","B1","B12"):check("J_USB",n,"GND")
for n in ("A4","A9","B4","B9"):check("J_USB",n,"USB_VBUS_5V")
check("J_USB","A5","USB_CC1")
check("J_USB","B5","USB_CC2")
for ref,net in (("R_CC1","USB_CC1"),("R_CC2","USB_CC2")):
    check(ref,"1",net)
    check(ref,"2","GND")
print("USB-C sink pad net assignment matches expected mapping.")
print("NOT FABRICABLE: pads may be unconnected physically; no schematic, routing, DRC, protection or regulator validated.")
