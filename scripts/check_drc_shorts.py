#!/usr/bin/env python3
"""Block the study workflow on native KiCad copper shorts; not a full DRC gate."""
import pathlib
import re
import sys

p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "preview/placement-study-drc.txt")
if not p.is_file():
    sys.exit("FAIL: KiCad DRC report missing")
report = p.read_text(encoding="utf-8", errors="replace")
kinds = ("shorting_items", "shorting_tracks")
counts = {
    kind: len(re.findall(r"^\\s*\\[" + re.escape(kind) + r"\\]", report, re.MULTILINE))
    for kind in kinds
}
for kind, count in counts.items():
    print(f"{kind}: {count}")
if sum(counts.values()):
    sys.exit("FAIL: KiCad detected physical copper short circuits")
print("PASS: no KiCad copper-short violations; remaining DRC issues are NOT cleared")
