#!/usr/bin/env python3
"""Conservative file-presence gate; NOT a replacement for KiCad ERC/DRC."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
required = [
    "hardware/Paky76-RevA.kicad_sch",
    "hardware/Paky76-RevA.kicad_pcb",
    "reports/erc.txt",
    "reports/drc.txt",
    "manufacturing/gerber",
    "manufacturing/drill",
    "manufacturing/bom.csv",
    "manufacturing/positions.csv",
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    print("NOT READY FOR FABRICATION")
    for p in missing:
        print("MISSING:", p)
    raise SystemExit(1)
print("Files exist; engineering review and ERC/DRC pass still REQUIRED.")
raise SystemExit(1)
