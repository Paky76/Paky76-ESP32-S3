#!/usr/bin/env bash
# Paky76 Rev.A production export. FAIL CLOSED: do not run on placement study.
set -euo pipefail
cd "$(dirname "$0")/.."
BOARD="hardware/Paky76-RevA.kicad_pcb"
SCHEMATIC="hardware/Paky76-RevA.kicad_sch"
mkdir -p release/gerbers release/drill
test -s "$BOARD" && test -s "$SCHEMATIC"
kicad-cli sch erc -o release/final-erc.txt "$SCHEMATIC"
kicad-cli pcb drc -o release/final-drc.txt "$BOARD"
python3 scripts/manufacturing_readiness.py --drc release/final-drc.txt --report release/manufacturing-readiness.txt
kicad-cli pcb export gerbers -l F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts -o release/gerbers/ "$BOARD"
kicad-cli pcb export drill -o release/drill/ "$BOARD"
kicad-cli pcb export pos --format csv --units mm --side front -o release/pick-place-front.csv "$BOARD"
kicad-cli pcb export pos --format csv --units mm --side back -o release/pick-place-back.csv "$BOARD"
printf 'Production export completed. Human engineering review and supplier DFM still required.\n'
