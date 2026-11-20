#!/usr/bin/env python3
"""Static integrity check for the LCD routing test coupon.

This is NOT KiCad DRC and does not certify manufacturability.
"""
from pathlib import Path
import re
import sys

board = Path(__file__).resolve().parents[1] / "hardware/lcd-routing-test.kicad_pcb"
data = board.read_text(encoding="utf-8")
expected = ("VCC", "GND", "DIN", "CLK", "CS", "DC", "RST", "BL")
issues = []
for n, name in enumerate(expected, 1):
    if not re.search(r'\(net\s+' + str(n) + r'\s+"' + name + r'"\)', data):
        issues.append(f"Missing declared net {n} {name}")
    segment = rf'\(segment\s+\(start 108 {88+(n-1)*2.54:g}\)\s+\(end 132 {88+(n-1)*2.54:g}\).*?\(net {n}\)'
    if not re.search(segment, data, flags=re.S):
        issues.append(f"Missing expected copper segment for net {n} {name}")
if data.count('(pad "') != 16:
    issues.append("Expected exactly 16 through-hole pads")
if data.count('(segment ') != 8:
    issues.append("Expected exactly eight segments")
if issues:
    print("STATIC COUPON CHECK FAILED")
    print("\n".join(issues))
    sys.exit(1)
print("Static coupon net/trace count and coordinate check passed.")
print("NOT a DRC, ERC, physical connector check or production release.")
