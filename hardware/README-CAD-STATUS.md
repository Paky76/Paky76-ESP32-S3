# Real KiCad source — incremental

The file `lcd-interface-prototype.kicad_sch` is a **partial interface schematic** with an embedded eight-pin LCD symbol and signal labels. It is not the ESP32-S3 controller schematic, and its display connector pin order is **not verified** against the chosen Waveshare SKU. The labels are conceptual, not a physical connector pinout.

Do not fabricate from this file. The release workflows intentionally require complete `Paky76-RevA.kicad_sch` and `Paky76-RevA.kicad_pcb` and must continue to fail until real design files are ready. No ERC or DRC has been run on this incremental source.
