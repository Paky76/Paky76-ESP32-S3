# Paky76 Rev.A — Manufacturing release checklist

**Status: NOT READY FOR FABRICATION.**

- [ ] Select exact orderable component MPNs and verify stock.
- [ ] Draw and peer-review complete KiCad schematic.
- [ ] Run ERC; resolve or document each issue.
- [ ] Assign and verify footprints against datasheets.
- [ ] Define board outline, mounting and enclosure clearances.
- [ ] Route PCB; review return paths, decoupling and antenna keepout.
- [ ] Run DRC; resolve or document each issue.
- [ ] Verify USB-C CC, ESD, power and boot/strapping design.
- [ ] Export Gerber and Excellon drill files.
- [ ] Export assembly BOM with MPNs and pick-and-place positions.
- [ ] Review fabrication stackup, impedance and assembly orientation.
- [ ] Assemble and test a prototype before production release.

Suggested local checks once files exist:

```bash
kicad-cli sch erc hardware/Paky76-RevA.kicad_sch -o reports/erc.txt
kicad-cli pcb drc hardware/Paky76-RevA.kicad_pcb -o reports/drc.txt
```

These commands have not yet been executed. No passing ERC/DRC report is claimed.
