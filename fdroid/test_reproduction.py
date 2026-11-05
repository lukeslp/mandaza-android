import importlib.util
from hashlib import sha256
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("reproduction", Path(__file__).with_name("verify-reproduction.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReproductionTests(unittest.TestCase):
    def test_only_the_pinned_source_and_exact_bytes_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            apk = Path(directory) / "candidate.apk"
            apk.write_bytes(b"unsigned test fixture")
            revision = "a" * 40
            receipt = {"sourceTag": "fdroid-v1.3.6", "sourceCommit": revision,
                       "applicationId": "app.mandaza.android",
                       "unsignedApkSha256": sha256(apk.read_bytes()).hexdigest()}
            self.assertTrue(module.verify(receipt, apk, revision, "fdroid-v1.3.6")["matchesPublishedReceipt"])
            with self.assertRaisesRegex(ValueError, "checkout"):
                module.verify(receipt, apk, "b" * 40, "fdroid-v1.3.6")
            with self.assertRaisesRegex(ValueError, "checkout"):
                module.verify(receipt, apk, revision, "fdroid-v1.3.7")
            apk.write_bytes(b"different build")
            with self.assertRaisesRegex(ValueError, "differs"):
                module.verify(receipt, apk, revision, "fdroid-v1.3.6")
