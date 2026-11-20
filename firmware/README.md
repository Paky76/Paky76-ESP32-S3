# Paky76 Rev.A firmware smoke test

PlatformIO project in `firmware/` for initial display bring-up using the provisional GPIO map. The chosen PlatformIO board is a development-board target, not proof that the custom PCB pinout or boot configuration is correct.

## Planned validation
1. Build firmware with PlatformIO and record compiler output.
2. Verify USB serial programming on actual assembled hardware.
3. Verify ST7789 240x240 display wiring, orientation and backlight interface.
4. Add and test Wi-Fi and BLE startup diagnostics.

No firmware build or hardware test has been completed. Do not connect GPIO7 directly to an unknown high-current backlight load.
