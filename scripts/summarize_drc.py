#!/usr/bin/env python3
"""Summarize native KiCad DRC report without implying fabrication readiness."""
import collections
import pathlib
import re
import sys
path=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "preview/placement-study-drc.txt")
if not path.is_file():
    print("DRC report unavailable; no validation can be inferred.")
    sys.exit(1)
lines=path.read_text(encoding="utf-8",errors="replace").splitlines()
counts=collections.Counter()
for line in lines:
    m=re.match(r"^\s*\[([a-zA-Z0-9_]+)\]",line)
    if m:counts[m.group(1)]+=1
print("=== KiCad DRC issue types (preliminary placement study) ===")
for name,n in counts.most_common():
    print("%-38s %d"%(name,n))
print("Total parsed issues:",sum(counts.values()))
if not counts:
    print("No bracketed issue entries found; inspect raw report before interpreting.")
print("REPORT ONLY: this PCB lacks a completed schematic and most copper routes.")
