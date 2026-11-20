#!/usr/bin/env python3
"""Generate an editable but electrically INCOMPLETE KiCad PCB study. NOT FOR FABRICATION."""
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
reg=add_footprint("Package_TO_SOT_SMD","SOT-23-5","U_REG","AP2112K-3.3TRG1_CANDIDATE",137,140)
reg_in=add_footprint("Capacitor_SMD","C_0805_2012Metric","C_REG_IN","10uF_CANDIDATE",133,140)
reg_out=add_footprint("Capacitor_SMD","C_0805_2012Metric","C_REG_OUT","10uF_CANDIDATE",141,140)
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
v33=net("+3V3")
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
# Candidate AP2112K SOT-23-5: 1 VIN, 2 GND, 3 EN, 4 NC, 5 VOUT.
for pin,network in (("1",vbus),("2",gnd),("3",vbus),("5",v33)):
    assign(reg,pin,network)
for capacitor,rail in ((reg_in,vbus),(reg_out,v33),(bulk,vbus),(dec,v33)):
    assign(capacitor,"1",rail)
    assign(capacitor,"2",gnd)
# Route two short CC1/CC2 copper segments from the actual footprint pad centres.
# This is deliberately only a partial routing experiment; clearance/DRC still required.
def route_pad_to_pad(source,source_number,target,target_number,network,width_mm=0.2):
    start=[p for p in source.Pads() if p.GetNumber()==source_number]
    end=[p for p in target.Pads() if p.GetNumber()==target_number]
    if len(start)!=1 or len(end)!=1:
        raise RuntimeError("Ambiguous pad number in copper route")
    track=pcb.PCB_TRACK(board)
    track.SetStart(start[0].GetPosition())
    track.SetEnd(end[0].GetPosition())
    track.SetWidth(mm(width_mm))
    track.SetLayer(pcb.F_Cu)
    track.SetNet(network)
    board.Add(track)
route_pad_to_pad(usb,"A5",cc1,"1",cc1net)
route_pad_to_pad(usb,"B5",cc2,"1",cc2net)
# USB D+/D- and ESP32 pins are deliberately not connected until the schematic
# and connector symbol/footprint pin-number mapping have been independently reviewed.
# These are physical placements, NOT connected electrically.
pcb.SaveBoard(OUT,board)
print("Created",OUT,"footprints:",[(f.GetReference(),f.GetFPID().GetLibItemName()) for f in board.GetFootprints()])
print("WARNING: USB-C and provisional regulator pad nets assigned. Only two CC tracks; no validated schematic or regulator routing. USB and LCD physical compatibility unverified; do not fabricate.")
