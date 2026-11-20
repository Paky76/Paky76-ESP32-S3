#!/usr/bin/env python3
"""Export a factual, provisional assembly BOM from the generated KiCad PCB."""
import csv
import os
import pathlib
import pcbnew as pcb

board_path=os.environ.get("PAKY76_BOARD_OUT","hardware/Paky76-RevA-placement-study.kicad_pcb")
board=pcb.LoadBoard(board_path)
out=pathlib.Path("hardware/generated-placement-bom-PROVISIONAL.csv")
out.parent.mkdir(parents=True,exist_ok=True)
rows=[]
for fp in sorted(board.GetFootprints(),key=lambda f:f.GetReference()):
    fpid=fp.GetFPID()
    rows.append({
        "Reference":fp.GetReference(),
        "Value_as_placed":fp.GetValue(),
        "KiCad_footprint":fpid.GetLibNickname()+":"+fpid.GetLibItemName(),
        "X_mm":f"{pcb.ToMM(fp.GetPosition().x):.3f}",
        "Y_mm":f"{pcb.ToMM(fp.GetPosition().y):.3f}",
        "Rotation_deg":f"{fp.GetOrientationDegrees():.1f}",
        "MPN":"NOT_SELECTED",
        "Status":"PROVISIONAL_NOT_FOR_ASSEMBLY",
    })
with out.open("w",newline="",encoding="utf-8") as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(f"Exported {len(rows)} real KiCad footprints to {out}; NOT a procurement BOM")
