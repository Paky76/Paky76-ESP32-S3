#!/usr/bin/env python3
"""Check actual copper tracks exist and terminate on intended pads.
This is a limited connectivity audit, not a full DRC or fabrication approval.
"""
import sys
import pcbnew as pcb
b=pcb.LoadBoard("hardware/Paky76-RevA-placement-study.kicad_pcb")
fps={f.GetReference():f for f in b.GetFootprints()}
expected=[
 ("J_USB","A5","R_CC1","1","USB_CC1"),
 ("J_USB","B5","R_CC2","1","USB_CC2"),
 ("R_EN","2","C_EN","1","ESP_EN"),
]
tracks=list(b.GetTracks())
for a,ap,z,zp,net in expected:
    try:
        pa=next(p for p in fps[a].Pads() if p.GetNumber()==ap)
        pz=next(p for p in fps[z].Pads() if p.GetNumber()==zp)
    except (KeyError,StopIteration):
        sys.exit("Missing footprint/pad for %s.%s -> %s.%s"%(a,ap,z,zp))
    if pa.GetNetname()!=net or pz.GetNetname()!=net:
        sys.exit("Incorrect pad net for %s.%s -> %s.%s"%(a,ap,z,zp))
    matching=[t for t in tracks if t.GetNetname()==net and
              ((t.GetStart()==pa.GetPosition() and t.GetEnd()==pz.GetPosition()) or
               (t.GetEnd()==pa.GetPosition() and t.GetStart()==pz.GetPosition()))]
    if not matching:sys.exit("Missing copper segment: %s.%s -> %s.%s"%(a,ap,z,zp))
    print("Copper present:",a,ap,"->",z,zp,net)
print("Audited",len(expected),"individual segments; remaining connections are unrouted.")
