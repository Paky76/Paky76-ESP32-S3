#!/usr/bin/env python3
"""Check ESP32-S3 physical pad mapping for proposed ST7789 GPIO signals.
LCD header pin order is deliberately not assumed.
"""
import sys
import pcbnew as pcb
b=pcb.LoadBoard("hardware/Paky76-RevA-placement-study.kicad_pcb")
f=next((f for f in b.GetFootprints() if f.GetReference()=="U1"),None)
if f is None:sys.exit("Missing ESP32 module U1")
expected={"19":"LCD_MOSI","20":"LCD_SCLK","18":"LCD_CS",
          "17":"LCD_DC","12":"LCD_RST","7":"LCD_BL",
          "40":"GND","41":"GND"}
for pin,net in expected.items():
    pads=[p for p in f.Pads() if p.GetNumber()==pin]
    if not pads or any(p.GetNetname()!=net for p in pads):
        sys.exit("Invalid ESP32-S3 pad %s: expected %s"%(pin,net))
print("ESP32-S3 module pad mapping for proposed LCD SPI signals verified.")
print("WARNING: ST7789 module connector pin order, backlight electrical interface, routing and DRC are NOT validated.")
