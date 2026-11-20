#!/usr/bin/env python3
"""Check physical board placement geometry using KiCad's actual footprint geometry.
A passing result is NOT electrical DRC or manufacturing approval.
"""
import sys
import pcbnew as pcb

BOARD="hardware/Paky76-RevA-placement-study.kicad_pcb"
b=pcb.LoadBoard(BOARD)
footprints=list(b.GetFootprints())
expected={"U1","J_LCD","J_USB","R_CC1","R_CC2","C_BULK","C_DECOUPLE","U_REG","C_REG_IN","C_REG_OUT"}
actual={f.GetReference() for f in footprints}
if actual != expected:
    sys.exit("Incorrect footprint population: expected %s, found %s"%(sorted(expected),sorted(actual)))
# Read the actual Edge.Cuts bounding box, not nominal size from design notes.
edges=[d for d in b.GetDrawings() if d.GetLayer()==pcb.Edge_Cuts]
if len(edges)!=4:
    sys.exit("Expected four edge segments, found %d"%len(edges))
xs=[];ys=[]
for e in edges:
    xs.extend([e.GetStart().x,e.GetEnd().x])
    ys.extend([e.GetStart().y,e.GetEnd().y])
left,right,bottom,top=min(xs),max(xs),min(ys),max(ys)
print("Board bounds (mm):",*[round(pcb.ToMM(v),3) for v in (left,bottom,right,top)])
failed=False
for f in footprints:
    bb=f.GetBoundingBox(False,False) # Includes reference/value text and graphics; advisory only
    # Bounding box includes silkscreen, not just copper; conservative preliminary test.
    x1,y1,x2,y2=bb.GetLeft(),bb.GetTop(),bb.GetRight(),bb.GetBottom()
    outside=x1<left or y1<bottom or x2>right or y2>top
    print(f.GetReference(),str(f.GetFPID().GetLibItemName()),
          "bounds:",*[round(pcb.ToMM(v),2) for v in (x1,y1,x2,y2)],
          "OUTSIDE_BOARD" if outside else "inside")
    if outside:
        print('  NOTE: footprint overall bounding box may include reference/value text; pad-only check follows')
    for pad in f.Pads():
        pb=pad.GetBoundingBox()
        if pb.GetLeft()<left or pb.GetTop()<bottom or pb.GetRight()>right or pb.GetBottom()>top:
            print('  PAD OUTSIDE:',pad.GetNumber())
            failed=True
if failed: sys.exit("Copper pads extend outside board. Rework placement.")
print("Copper-pad board envelope check passed; body/courtyard and assembly clearance still require review. No electrical DRC verified.")
