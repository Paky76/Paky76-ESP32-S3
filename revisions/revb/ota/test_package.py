import hashlib
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest

from package import HEADER, SIGNATURE_SPACE, package


class PackageTests(unittest.TestCase):
    def test_signature_and_payload_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            key, pub, sig = [root / name for name in ("private.pem", "public.pem", "signature.der")]
            subprocess.run(["openssl", "genpkey", "-algorithm", "EC", "-pkeyopt",
                            "ec_paramgen_curve:P-256", "-out", key], check=True, capture_output=True)
            subprocess.run(["openssl", "pkey", "-in", key, "-pubout", "-out", pub],
                           check=True, capture_output=True)
            image = b"\xe9" + b"test image PAKYFW:7:2\x00"
            with self.assertRaises(ValueError):
                package(image, 8, 2, key)
            with self.assertRaises(ValueError):
                package(image, 7, 1, key)
            bundle = package(image, 7, 2, key)
            header = bundle[:HEADER.size]
            magic, target, version, length, digest = HEADER.unpack(header)
            self.assertEqual((magic, target, version, length), (b"PAKYOTA1", 2, 7, len(image)))
            siglen = struct.unpack_from(">H", bundle, HEADER.size)[0]
            sig.write_bytes(bundle[HEADER.size + 2:HEADER.size + 2 + siglen])
            command = ["openssl", "dgst", "-sha256", "-verify", str(pub), "-signature", str(sig)]
            self.assertEqual(subprocess.run(command, input=header, capture_output=True).returncode, 0)
            modified = HEADER.pack(magic, target, version + 1, length, digest)
            self.assertNotEqual(subprocess.run(command, input=modified, capture_output=True).returncode, 0)
            payload = bundle[HEADER.size + 2 + SIGNATURE_SPACE:]
            self.assertEqual(hashlib.sha256(payload).digest(), digest)
            self.assertNotEqual(hashlib.sha256(payload + b"x").digest(), digest)

    def test_invalid_firmware_is_rejected_before_signing(self):
        with self.assertRaises(ValueError):
            package(b"missing ESP header", 1, 1, "unused.pem")
