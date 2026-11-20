#!/usr/bin/env python3
"""Export Rev.B evidence for Eurocircuits review after strict CAD checks."""
import argparse
import csv
from pathlib import Path
import re
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile


def references(path, column, required):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not {column, *required}.issubset(reader.fieldnames or []):
            raise ValueError(f"{path.name}: columns required: {column}, {', '.join(required)}")
        refs = set()
        for row in reader:
            if any(not (row.get(key) or "").strip() for key in (column, *required)):
                raise ValueError(f"{path.name}:{reader.line_num}: empty required field")
            for ref in re.split(r"[\s,;]+", row[column].strip()):
                if ref in refs:
                    raise ValueError(f"{path.name}: duplicate reference {ref}")
                refs.add(ref)
        if not refs:
            raise ValueError(f"{path.name}: no populated components")
        return refs


def assemble(kicad, output, layers):
    root = Path(__file__).resolve().parents[1]
    sch = root / "hardware/Paky76-RevB.kicad_sch"
    pcb = root / "hardware/Paky76-RevB.kicad_pcb"
    cfg = root / "hardware/Paky76-RevB.kicad_pro"
    bom = root / "hardware/bom-revb-pcba.csv"
    missing = [str(path.relative_to(root)) for path in (sch, pcb, cfg, bom)
               if not path.is_file() or not path.stat().st_size]
    if missing:
        raise ValueError("Rev.B CAD or BOM missing: " + ", ".join(missing))
    if output.exists():
        raise ValueError(f"Output already exists: {output}")

    def cli(*args):
        subprocess.run([kicad, *map(str, args)], check=True)

    with tempfile.TemporaryDirectory(prefix="paky76-revb-") as work:
        work = Path(work)
        reports = work / "checks"
        reports.mkdir()
        cli("sch", "erc", "--exit-code-violations", "-o", reports / "ERC.txt", sch)
        cli("pcb", "drc", "--schematic-parity", "--exit-code-violations",
            "--severity-exclusions", "--severity-error", "--severity-warning",
            "-o", reports / "DRC.txt", pcb)

        cpl = work / "CPL.csv"
        cli("pcb", "export", "pos", "--format", "csv", "--units", "mm", "--exclude-dnp", "-o", cpl, pcb)
        bom_refs = references(bom, "Reference", ("MPN", "Description"))
        positions = references(cpl, "Ref", ("PosX", "PosY", "Rot", "Side"))
        if bom_refs != positions:
            raise ValueError(f"BOM/CPL mismatch: BOM only {sorted(bom_refs - positions)}, CPL only {sorted(positions - bom_refs)}")
        (work / "BOM.csv").write_bytes(bom.read_bytes())

        copper = ["F.Cu", *(f"In{n}.Cu" for n in range(1, layers - 1)), "B.Cu"]
        layer_list = ",".join(copper + ["F.Mask", "B.Mask", "F.Paste", "B.Paste",
                                        "F.Silkscreen", "B.Silkscreen", "Edge.Cuts"])
        cli("pcb", "export", "gerbers", "-l", layer_list, "-o", str(work / "gerber") + "/", pcb)
        cli("pcb", "export", "drill", "--excellon-separate-th", "-o", str(work / "drill") + "/", pcb)
        expected = {".gtl", ".gbl", ".gm1", *(f".g{n}" for n in range(1, layers - 1))}
        actual = {file.suffix for file in (work / "gerber").iterdir()}
        if not expected.issubset(actual):
            raise ValueError(f"Incomplete Gerber set: {sorted(expected - actual)}")
        (work / "README.txt").write_text(
            "Paky76 Rev.B. For Eurocircuits PCB/PCBA Visualizer and DFM review.\n"
            "Confirm stack-up, layer mapping, via treatment, component sourcing, and CPL orientation.\n"
            "Engineering sign-off and physical validation are required for release to production.\n",
            encoding="utf-8",
        )
        with ZipFile(output, "x", ZIP_DEFLATED) as archive:
            for path in sorted(work.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(work))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--copper-layers", type=int, choices=(4, 6), required=True)
    parser.add_argument("--kicad-cli", default="kicad-cli")
    opts = parser.parse_args()
    try:
        assemble(opts.kicad_cli, opts.output, opts.copper_layers)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"BUILD BLOCKED: {exc}\n")


if __name__ == "__main__":
    main()
