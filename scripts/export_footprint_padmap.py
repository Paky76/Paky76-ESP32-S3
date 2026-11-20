#!/usr/bin/env python3
"""Export real pad coordinates/numbers from installed KiCad footprint libraries.
Mechanical source of truth for pin-to-pad routing; does not establish electrical pin functions.
"""
import csv,os,pcbnew as pcb
board=pcb.LoadBoard("hardware/Paky76-RevA-placement-study.kicad_pcb")
out="hardware/generated-footprint-padmap.csv"
os.makedirs(os.path.dirname(out),exist_ok=True)
with open(out,"w",newline="") as file:
    writer=csv.writer(file)
    writer.writerow(["reference","footprint","pad_number","x_mm","y_mm","layers","net"])
    for fp in sorted(board.GetFootprints(),key=lambda f:f.GetReference()):
        for pad in sorted(fp.Pads(),key=lambda p:(p.GetNumber(),p.GetPosition().x,p.GetPosition().y)):
            pos=pad.GetPosition()
            writer.writerow([fp.GetReference(),str(fp.GetFPID().GetLibItemName()),pad.GetNumber(),
                             round(pcb.ToMM(pos.x),4),round(pcb.ToMM(pos.y),4),
                             str(pad.GetLayerSet().FmtBin()),pad.GetNetname()])
print("Exported physical pad map:",out)
print("WARNING: no pin functions, nets, traces or ERC/DRC are established.")
