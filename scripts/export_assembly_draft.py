#!/usr/bin/env python3
"""Export provisional BOM and centroid data from the ACTUAL generated KiCad PCB.
Outputs are engineering drafts, NOT approved for procurement or assembly.
"""
import csv
import os
from pathlib import Path
import pcbnew as pcb

board_path=os.environ.get("PAKY76_BOARD_OUT","hardware/Paky76-RevA-placement-study.kicad_pcb")
out=Path("preview")
out.mkdir(parents=True,exist_ok=True)
board=pcb.LoadBoard(board_path)
parts=sorted(board.GetFootprints(),key=lambda f:f.GetReference())
with (out/"bom-PROVISIONAL.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["Reference","Value","Footprint","MPN","Procurement status","Assembly status"])
    for fp in parts:
        w.writerow([fp.GetReference(),fp.GetValue(),fp.GetFPID().GetLibItemName(),"",
                    "UNVERIFIED - MPN REQUIRED","NOT APPROVED FOR ASSEMBLY"])
with (out/"centroids-PROVISIONAL.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["Designator","Mid X (mm)","Mid Y (mm)","Rotation (deg)","Layer","Status"])
    for fp in parts:
        pos=fp.GetPosition()
        w.writerow([fp.GetReference(),f"{pcb.ToMM(pos.x):.4f}",f"{pcb.ToMM(pos.y):.4f}",
                    f"{fp.GetOrientationDegrees():.2f}",
                    "Bottom" if fp.IsFlipped() else "Top","NOT VALIDATED"])
print(f"Exported {len(parts)} footprints to provisional BOM and centroids; NOT production-ready")
