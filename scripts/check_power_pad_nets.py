#!/usr/bin/env python3
"""Validate tentative regulator and capacitor pad nets in the KiCad placement study.
Logical pin checks only; not electrical safety or fabrication approval.
"""
import sys
import pcbnew as pcb
board=pcb.LoadBoard("hardware/Paky76-RevA-placement-study.kicad_pcb")
footprints={f.GetReference():f for f in board.GetFootprints()}
expected={
 "U_REG":{"1":"USB_VBUS_5V","2":"GND","3":"USB_VBUS_5V","5":"+3V3"},
 "C_REG_IN":{"1":"USB_VBUS_5V","2":"GND"},
 "C_REG_OUT":{"1":"+3V3","2":"GND"},
 "C_BULK":{"1":"USB_VBUS_5V","2":"GND"},
 "C_DECOUPLE":{"1":"+3V3","2":"GND"},
}
for ref,pins in expected.items():
    if ref not in footprints:sys.exit("Missing footprint: "+ref)
    for number,net in pins.items():
        pads=[p for p in footprints[ref].Pads() if p.GetNumber()==number]
        if len(pads)!=1:sys.exit("Expected exactly one pad %s.%s"%(ref,number))
        if pads[0].GetNetname()!=net:
            sys.exit("Wrong net for %s.%s: %s expected %s"%(ref,number,pads[0].GetNetname(),net))
print("Provisional power pad assignments match declared net mapping.")
print("IMPORTANT: regulator datasheet, power rating, copper routing, DRC, thermal performance and schematic remain unverified.")
