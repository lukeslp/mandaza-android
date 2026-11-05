#!/usr/bin/env python3
"""Compare a source rebuild with a published upstream reproducibility receipt."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess


def verify(receipt, apk, source_revision, tag):
    if not re.fullmatch(r"fdroid-v\d+\.\d+\.\d+", tag):
        raise ValueError("Expected an Android F-Droid release tag")
    if receipt.get("sourceTag") != tag or receipt.get("sourceCommit") != source_revision:
        raise ValueError("The checkout does not match the published source tag/commit")
    if receipt.get("applicationId") != "app.mandaza.android":
        raise ValueError("Receipt belongs to a different Android app")
    expected = receipt.get("unsignedApkSha256", "")
    if not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError("Receipt has no valid unsigned APK digest")
    actual = sha256(apk.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"Unsigned APK differs from the published receipt: {actual}")
    return {"sourceCommit": source_revision, "sourceTag": tag,
            "unsignedApkSha256": actual, "matchesPublishedReceipt": True,
            "scope": "Upstream CI byte comparison; official F-Droid builder acceptance is separate"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--apk", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    args = parser.parse_args()
    revision = subprocess.check_output(["git", "-C", str(args.source), "rev-parse", "HEAD"], text=True).strip()
    result = verify(json.loads(args.receipt.read_text()), args.apk, revision, args.tag)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
