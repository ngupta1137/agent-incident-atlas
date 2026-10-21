#!/usr/bin/env python3
"""Validate every incident record in data/incidents against the schema and house rules.

Usage: python scripts/validate.py
Exit code 0 means all records pass. Licensed under MIT.
"""
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "incident.schema.json"
TAXONOMY = ROOT / "schema" / "taxonomy.json"
INCIDENTS = ROOT / "data" / "incidents"
EM_DASH = chr(0x2014)


def text_of(record):
    """Collect every string in a record so style checks cover all fields."""
    out = []

    def walk(node):
        if isinstance(node, str):
            out.append(node)
        elif isinstance(node, dict):
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(record)
    return out


def main():
    errors = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    taxonomy = json.loads(TAXONOMY.read_text(encoding="utf-8"))

    schema_tags = set(schema["$defs"]["failureTag"]["enum"])
    taxonomy_tags = {t["tag"] for t in taxonomy["failure_types"]}
    if schema_tags != taxonomy_tags:
        errors.append(f"schema tags and taxonomy.json differ: {sorted(schema_tags ^ taxonomy_tags)}")

    files = sorted(INCIDENTS.glob("*.json"))
    if not files:
        errors.append("no incident files found")
    seen = set()
    for path in files:
        record = json.loads(path.read_text(encoding="utf-8"))
        for err in sorted(validator.iter_errors(record), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in err.path) or "(root)"
            errors.append(f"{path.name}: {loc}: {err.message[:160]}")
        rid = record.get("id")
        if rid != path.stem:
            errors.append(f"{path.name}: id {rid!r} does not match file name")
        if rid in seen:
            errors.append(f"{path.name}: duplicate id {rid}")
        seen.add(rid)
        if record.get("primary_failure_type") not in record.get("failure_types", []):
            errors.append(f"{path.name}: primary_failure_type must appear in failure_types")
        words = len(record.get("narrative", "").split())
        if not 150 <= words <= 300:
            errors.append(f"{path.name}: narrative is {words} words, need 150 to 300")
        if any(EM_DASH in s for s in text_of(record)):
            errors.append(f"{path.name}: contains an em dash")

    for md in ROOT.glob("*.md"):
        if EM_DASH in md.read_text(encoding="utf-8"):
            errors.append(f"{md.name}: contains an em dash")

    if errors:
        print(f"FAILED with {len(errors)} problem(s):")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK: {len(files)} records valid, schema and taxonomy consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
