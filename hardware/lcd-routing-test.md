# LCD signal routing test coupon

This is an **independent routed PCB test coupon**, not the ESP32-S3 controller PCB. It has two 8-pin 2.54 mm headers and eight individual F.Cu copper traces connecting corresponding numbered pins. Net names follow the Waveshare 1.3inch LCD module signal names VCC/GND/DIN/CLK/CS/DC/RST/BL. It can be inspected in KiCad as a routing example, but it is **not directly compatible with the PH2.0 cable**, has not been checked with KiCad DRC and must not be sent for production.

Manufacturer: https://www.waveshare.com/wiki/1.3inch_LCD_Module

The real Rev.A still requires a validated MCU, USB-C power, regulator, matching display connector, board routing and release validation.
