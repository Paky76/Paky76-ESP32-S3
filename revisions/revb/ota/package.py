#!/usr/bin/env python3
"""Sign a Paky76 app binary with an offline ECDSA P-256 key."""
import argparse
import hashlib
from pathlib import Path
import re
import struct
import subprocess

MAGIC = b"PAKYOTA1"
LIMIT = 0x300000
SIGNATURE_SPACE = 80
HEADER = struct.Struct(">8sIII32s")


def package(image, version, target, private_key):
    if not image or len(image) > LIMIT or image[0] != 0xE9:
        raise ValueError("Serve un firmware.bin ESP32 valido entro 3 MiB.")
    if not 0 < version <= 0xFFFFFFFF or target not in (1, 2):
        raise ValueError("Versione positiva e variante 1 o 2 richieste.")
    markers = set(re.findall(rb"PAKYFW:([0-9]+):([12])\x00", image))
    if markers != {(str(version).encode(), str(target).encode())}:
        raise ValueError("Versione o variante non corrisponde al binario compilato.")
    header = HEADER.pack(MAGIC, target, version, len(image), hashlib.sha256(image).digest())
    signature = subprocess.run(
        ["openssl", "dgst", "-sha256", "-sign", str(private_key)],
        input=header, stdout=subprocess.PIPE, check=True,
    ).stdout
    if not 0 < len(signature) <= SIGNATURE_SPACE:
        raise ValueError("Usa una chiave ECDSA P-256.")
    return header + struct.pack(">H", len(signature)) + signature.ljust(SIGNATURE_SPACE, b"\x00") + image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--firmware", type=Path, required=True)
    parser.add_argument("--version", type=int, required=True)
    parser.add_argument("--target", type=int, choices=(1, 2), required=True)
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.output.open("xb") as out:
        try:
            out.write(package(args.firmware.read_bytes(), args.version, args.target, args.key))
        except (ValueError, OSError, subprocess.CalledProcessError) as exc:
            out.close()
            args.output.unlink(missing_ok=True)
            parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
