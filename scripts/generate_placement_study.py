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
usb=add_footprint("Connector_USB","USB_C_Receptacle_HRO_TYPE-C-31-M-12","J_USB","USB-C_FOOTPRINT_STUDY",125,141)
cc1=add_footprint("Resistor_SMD","R_0603_1608Metric","R_CC1","5.1k",116,137)
cc2=add_footprint("Resistor_SMD","R_0603_1608Metric","R_CC2","5.1k",119,137)
bulk=add_footprint("Capacitor_SMD","C_0805_2012Metric","C_BULK","10uF_PLACEHOLDER",132,135)
dec=add_footprint("Capacitor_SMD","C_0603_1608Metric","C_DECOUPLE","100nF_PLACEHOLDER",135,135)
# Preliminary USB-C sink pad net assignments on the real KiCad pads.
# Only these connector pads are mapped. This is NOT a schematic or routed design.
def net(name):
    n=pcb.NETINFO_ITEM(board,name)
    board.Add(n)
    return n
def assign(fp,number,network):
    pads=[p for p in fp.Pads() if p.GetNumber()==number]
    if not pads:
        raise RuntimeError("Footprint %s missing required pad %s"%(fp.GetReference(),number))
    for p in pads: p.SetNet(network)
gnd=net("GND")
vbus=net("USB_VBUS_5V")
cc1net=net("USB_CC1")
cc2net=net("USB_CC2")
for number in ("A1","A12","B1","B12"):
    assign(usb,number,gnd)
for number in ("A4","A9","B4","B9"):
    assign(usb,number,vbus)
assign(usb,"A5",cc1net)
assign(usb,"B5",cc2net)
assign(cc1,"1",cc1net)
assign(cc1,"2",gnd)
assign(cc2,"1",cc2net)
assign(cc2,"2",gnd)
# USB D+/D- and ESP32 pins are deliberately not connected until the schematic
# and connector symbol/footprint pin-number mapping have been independently reviewed.
# These are physical placements, NOT connected electrically.
pcb.SaveBoard(OUT,board)
print("Created",OUT,"footprints:",[(f.GetReference(),f.GetFPID().GetLibItemName()) for f in board.GetFootprints()])
print("WARNING: Only USB-C CC/GND/VBUS pad nets are assigned. No tracks, regulator or electrical schematic. USB and LCD physical compatibility unverified; do not fabricate.")
