#!/usr/bin/env python3
"""Export exact pad-to-net connectivity from KiCad PCB, including duplicate pad numbers.
This is a PCB pad assignment inventory, NOT an ERC-validated schematic/netlist.
"""
import csv
import os
from pathlib import Path
import pcbnew as pcb

src=os.environ.get("PAKY76_BOARD_OUT","hardware/Paky76-RevA-placement-study.kicad_pcb")
board=pcb.LoadBoard(src)
out=Path("preview")
out.mkdir(exist_ok=True)
rows=[]
for fp in board.GetFootprints():
    for pad in fp.Pads():
        pos=pad.GetPosition()
        rows.append((fp.GetReference(),pad.GetNumber(),pad.GetNetname() or "UNASSIGNED",
                     f"{pcb.ToMM(pos.x):.4f}",f"{pcb.ToMM(pos.y):.4f}",
                     pcb.LayerName(pad.GetLayer())))
rows.sort(key=lambda x:(x[0],x[1],x[3],x[4]))
with (out/"physical-pad-netlist-PROVISIONAL.csv").open("w",newline="",encoding="utf-8") as f:
    writer=csv.writer(f)
    writer.writerow(["Reference","Pad number","Assigned net","X mm","Y mm","Pad primary layer"])
    writer.writerows(rows)
unassigned=[r for r in rows if r[2]=="UNASSIGNED"]
print(f"Physical pad inventory: {len(rows)} pads, {len(unassigned)} unassigned")
if unassigned:
    print("WARNING: unassigned pads include:",", ".join(f"{r[0]}:{r[1]}" for r in unassigned[:25]))
print("This is NOT a completed electrical schematic or proof of copper continuity.")
