#!/usr/bin/env python3
"""Check that release metadata agrees across files before tagging a release.

Usage:
    python scripts/check_release.py            check version consistency
    python scripts/check_release.py --strict   also fail if the OWNER placeholder is still present

Licensed under MIT.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    problems = []
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    zen = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    m = re.search(r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", cff, re.M)
    cff_version = m.group(1) if m else None
    if not cff_version:
        problems.append("CITATION.cff has no version")

    if zen.get("version") != cff_version:
        problems.append(f".zenodo.json version {zen.get('version')} differs from CITATION.cff {cff_version}")

    m = re.search(r"^## ([0-9]+\.[0-9]+\.[0-9]+)", changelog, re.M)
    if not m or m.group(1) != cff_version:
        problems.append(f"top CHANGELOG.md entry {m.group(1) if m else None} differs from CITATION.cff {cff_version}")

    if not re.search(r"^date-released:\s*\d{4}-\d{2}-\d{2}\s*$", cff, re.M):
        problems.append("CITATION.cff date-released is missing or not YYYY-MM-DD")

    if zen.get("upload_type") != "dataset":
        problems.append(".zenodo.json upload_type must be dataset")

    if "--strict" in sys.argv:
        for name in ["CITATION.cff", "README.md", ".zenodo.json"]:
            if "OWNER" in (ROOT / name).read_text(encoding="utf-8"):
                problems.append(f"{name} still contains the OWNER placeholder")

    if problems:
        print("Release check FAILED:")
        for p in problems:
            print(" -", p)
        return 1
    print(f"Release metadata consistent at version {cff_version}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
