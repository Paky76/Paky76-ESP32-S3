#!/usr/bin/env python3
"""Validate provisional 8-pin ST7789 header mapping on native KiCad PCB."""
import os
import sys
import pcbnew as pcb
board=pcb.LoadBoard(os.environ.get("PAKY76_BOARD_OUT","hardware/Paky76-RevA-placement-study.kicad_pcb"))
headers=[f for f in board.GetFootprints() if f.GetReference()=="J_LCD"]
if len(headers)!=1:sys.exit("Missing or duplicate J_LCD")
expected={"1":"GND","2":"+3V3","3":"LCD_SCLK","4":"LCD_MOSI",
          "5":"LCD_RST","6":"LCD_DC","7":"LCD_CS","8":"LCD_BL"}
for number,network in expected.items():
    pads=[p for p in headers[0].Pads() if p.GetNumber()==number]
    if len(pads)!=1 or pads[0].GetNetname()!=network:
        sys.exit(f"J_LCD pin {number}: expected {network}")
print("PASS: eight provisional ST7789 header nets assigned; exact module pinout NOT verified")
