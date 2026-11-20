#!/usr/bin/env python3
"""Fail-closed release gate for Paky76 Rev.A manufacturing.
This never treats a successful placement-study CI run as fabrication approval.
"""
import argparse
import csv
from pathlib import Path
import re
import sys

def evaluate(root: Path, drc: Path):
    findings=[]
    def require(condition, message):
        if not condition: findings.append(message)
    sch=root/"hardware/Paky76-RevA.kicad_sch"
    pcb=root/"hardware/Paky76-RevA.kicad_pcb"
    require(sch.is_file(),"BLOCKER: final native KiCad schematic missing")
    require(pcb.is_file(),"BLOCKER: final native KiCad PCB missing (placement study is not final)")
    if not drc.is_file():
        findings.append("BLOCKER: final KiCad PCB DRC report missing")
    else:
        report=drc.read_text(encoding="utf-8",errors="replace")
        issues=re.findall(r"^\s*\[([a-z_]+)\]",report,re.MULTILINE)
        require(not issues,f"BLOCKER: KiCad DRC has {len(issues)} reported violations: "+", ".join(sorted(set(issues))))
        require("DRC report" in report or "DRC" in report or bool(issues),
                "BLOCKER: DRC report content not recognizable")
    erc=root/"release/final-erc.txt"
    require(erc.is_file(),"BLOCKER: final schematic ERC report missing")
    if erc.is_file():
        t=erc.read_text(encoding="utf-8",errors="replace")
        require(not re.search(r"^\s*\[[a-z_]+\]",t,re.MULTILINE),
                "BLOCKER: ERC report contains violations")
    bom=root/"release/approved-bom.csv"
    require(bom.is_file(),"BLOCKER: approved manufacturer BOM with exact MPNs missing")
    if bom.is_file():
        with bom.open(newline="",encoding="utf-8") as f:
            rows=list(csv.DictReader(f))
        require(bool(rows),"BLOCKER: approved BOM empty")
        require(all(row.get("MPN","").strip() and
                    row.get("Approved","").strip().upper()=="YES" for row in rows),
                "BLOCKER: BOM has missing MPN or unapproved part")
    approval=root/"release/engineering-approval.txt"
    require(approval.is_file() and "FABRICATION APPROVED" in approval.read_text(encoding="utf-8",errors="replace") if approval.is_file() else False,
            "BLOCKER: explicit engineering sign-off missing")
    return findings

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=Path("."))
    p.add_argument("--drc",type=Path,default=Path("release/final-drc.txt"))
    p.add_argument("--report",type=Path,default=Path("preview/manufacturing-readiness.txt"))
    a=p.parse_args()
    findings=evaluate(a.root,a.root/a.drc)
    output=("NOT READY FOR FABRICATION\n" if findings else "RELEASE GATE PASSED — independent review still required\n")
    output+="\n".join(findings or ["All machine-readable release conditions satisfied"])+"\n"
    target=a.root/a.report
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(output,encoding="utf-8")
    print(output,end="")
    return 1 if findings else 0

if __name__=="__main__":
    sys.exit(main())
