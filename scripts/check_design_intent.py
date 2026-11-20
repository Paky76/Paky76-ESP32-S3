#!/usr/bin/env python3
"""Validate electrical design intent; not a substitute for KiCad ERC/DRC."""
import csv
from collections import Counter
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"hardware"/"electrical-netlist-draft.csv"
rows=list(csv.DictReader(path.open(newline="",encoding="utf-8")))
required={"reference","signal","connection","design_note","status"}
assert rows and required.issubset(rows[0]),"Invalid netlist columns"
gpio=[r["signal"] for r in rows if r["reference"]=="U1" and r["signal"].startswith("GPIO")]
duplicates=[pin for pin,count in Counter(gpio).items() if count>1]
assert not duplicates,f"Duplicate GPIO: {duplicates}"
for signal in ("GPIO0","GPIO19","GPIO20","GPIO7","GPIO8","GPIO9","GPIO10","GPIO11","GPIO12"):
    assert signal in gpio,f"Missing {signal}"
assert {r["signal"] for r in rows if r["reference"]=="J_USB"} >= {"VBUS","CC1","CC2","D+","D-"}
assert len([r for r in rows if r["reference"]=="J_LCD"])==8
print(f"PASS: {len(rows)} design-intent connections; no duplicate MCU GPIOs.")
print("BLOCKED FOR MANUFACTURING: electrical-netlist-draft.csv is not a KiCad schematic or validated PCB.")
