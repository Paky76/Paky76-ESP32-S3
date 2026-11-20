#!/usr/bin/env python3
"""Fail if KiCad's DRC reports copper short circuits."""
import pathlib
import sys

p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "preview/placement-study-drc.txt")
if not p.is_file():
    sys.exit("FAIL: KiCad DRC report missing")
lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
kinds = ("shorting_items", "shorting_tracks")
counts = {kind: sum(line.lstrip().startswith("[" + kind + "]") for line in lines) for kind in kinds}
for kind, count in counts.items():
    print(f"{kind}: {count}")
if sum(counts.values()):
    sys.exit("FAIL: KiCad detected physical copper short circuits")
print("PASS: no KiCad copper shorts; other DRC issues may remain")
