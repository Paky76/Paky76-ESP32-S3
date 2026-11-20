#!/usr/bin/env python3
"""Create an EDITABLE placement-only KiCad PCB study. No tracks, not for fabrication."""
import os
import pcbnew as pcb

OUT = os.environ.get("PAKY76_BOARD_OUT", "hardware/Paky76-RevA-placement-study.kicad_pcb")
board = pcb.BOARD()
def mm(x): return pcb.FromMM(x)
def vec(x,y): return pcb.VECTOR2I(mm(x),mm(y))
def add_footprint(lib, name, ref, value, x, y, rotation=0):
    fp=pcb.FootprintLoad("/usr/share/kicad/footprints/"+lib+".pretty", name)
    if fp is None: raise RuntimeError(f"Missing KiCad footprint: {lib}:{name}")
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(vec(x,y))
    fp.SetOrientationDegrees(rotation)
    board.Add(fp)
    return fp
def edge(x1,y1,x2,y2):
    s=pcb.PCB_SHAPE(board)
    s.SetShape(pcb.SHAPE_T_SEGMENT)
    s.SetStart(vec(x1,y1));s.SetEnd(vec(x2,y2))
    s.SetLayer(pcb.Edge_Cuts);s.SetWidth(mm(.05))
    board.Add(s)
# Placement study: dimensions subject to antenna, USB, and enclosure review.
for a,b,c,d in [(100,100,150,100),(150,100,150,145),(150,145,100,145),(100,145,100,100)]: edge(a,b,c,d)
esp=add_footprint("RF_Module","ESP32-S3-WROOM-1","U1","ESP32-S3-WROOM-1-N8",124,115)
lcd=add_footprint("Connector_PinHeader_2.54mm","PinHeader_1x08_P2.54mm_Vertical","J_LCD","DISPLAY_INTERFACE_STUDY_ONLY",143,116)
# These are physical placements, NOT connected electrically.
pcb.SaveBoard(OUT,board)
print("Created",OUT,"footprints:",[(f.GetReference(),f.GetFPID().GetLibItemName()) for f in board.GetFootprints()])
print("WARNING: PCB has no traces, no nets, no USB connector and no power circuit; do not fabricate.")
