#!/usr/bin/env python3
"""Fail the KiCad study CI when native DRC detects physical copper shorts.
Other DRC violations remain advisory until schematic/routing completion.
"""
import pathlib,re,sys
p=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "preview/placement-study-drc.txt")
if not p.exists():sys.exit("FAIL: DRC report is missing")
s=p.read_text(encoding="utf-8",errors="replace")
kinds=("shorting_items","shorting_tracks")
counts={k:len(re.findall(r"^\\["+k+r"\\]:",s,re.MULTILINE)) for k in kinds}
for k,n in counts.items():print(k,n)
if sum(counts.values()):sys.exit("FAIL: copper shorts detected by KiCad DRC")
print("PASS: no physical copper shorts reported (other DRC violations may remain).")
