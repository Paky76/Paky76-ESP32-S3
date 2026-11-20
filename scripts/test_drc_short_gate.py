#!/usr/bin/env python3
"""Regression-test the DRC copper short gate using synthetic KiCad text reports."""
import pathlib
import subprocess
import sys
import tempfile

gate = pathlib.Path(__file__).with_name("check_drc_shorts.py")
cases = (
    ("no_shorts", "[unconnected_items]: Unconnected pads\n", 0),
    ("short_items", "[shorting_items]: Items shorted\n", 1),
    ("short_tracks", "[shorting_tracks]: Tracks shorted\n", 1),
    ("indented_short", "  [shorting_items]: Shorted\n", 1),
)
with tempfile.TemporaryDirectory() as d:
    path = pathlib.Path(d) / "drc.txt"
    for name, report, expected in cases:
        path.write_text(report, encoding="utf-8")
        result = subprocess.run([sys.executable, str(gate), str(path)], capture_output=True, text=True)
        actual = int(result.returncode != 0)
        if actual != expected:
            sys.exit(f"FAIL {name}: expected failure={expected}, got {actual}: {result.stderr}")
        print(f"PASS {name}")
