#!/usr/bin/env python3
"""Build data/atlas.json and data/atlas.csv from data/incidents/*.json.

Usage:
    python scripts/build_exports.py          write the exports
    python scripts/build_exports.py --check  fail if the exports are out of date (used in CI)

Licensed under MIT.
"""
import csv
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCIDENTS = ROOT / "data" / "incidents"
TAXONOMY = ROOT / "schema" / "taxonomy.json"
OUT_JSON = ROOT / "data" / "atlas.json"
OUT_CSV = ROOT / "data" / "atlas.csv"

COLUMNS = [
    "id", "seed", "provenance", "title", "date_start", "date_end", "sector", "agent_type",
    "autonomy_level", "primary_failure_type", "authority_lens", "failure_types", "severity",
    "impact_categories", "control_category", "missing_control", "detection_method",
    "time_to_detect", "narrative_words", "narrative", "business_impact_description",
    "root_cause", "governance_gap_description", "lessons_learned", "schema_version",
]


def load():
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(INCIDENTS.glob("*.json"))]


def flatten(r, lens_by_tag):
    d = r["date"]
    start, end = (d, d) if isinstance(d, str) else (d["start"], d["end"])
    return {
        "id": r["id"],
        "seed": str(r["seed"]).lower(),
        "provenance": r["provenance"],
        "title": r["title"],
        "date_start": start,
        "date_end": end,
        "sector": r["sector"],
        "agent_type": r["agent_type"],
        "autonomy_level": r["autonomy_level"],
        "primary_failure_type": r["primary_failure_type"],
        "authority_lens": lens_by_tag[r["primary_failure_type"]],
        "failure_types": ";".join(r["failure_types"]),
        "severity": r["business_impact"]["severity"],
        "impact_categories": ";".join(r["business_impact"]["categories"]),
        "control_category": r["governance_gap"]["control_category"],
        "missing_control": r["governance_gap"]["missing_control"],
        "detection_method": r["detection"]["method"],
        "time_to_detect": r["detection"]["time_to_detect"],
        "narrative_words": len(r["narrative"].split()),
        "narrative": r["narrative"],
        "business_impact_description": r["business_impact"]["description"],
        "root_cause": r["root_cause"],
        "governance_gap_description": r["governance_gap"]["description"],
        "lessons_learned": " | ".join(r["lessons_learned"]),
        "schema_version": r["schema_version"],
    }


def render():
    taxonomy = json.loads(TAXONOMY.read_text(encoding="utf-8"))
    lens_by_tag = {t["tag"]: t["lens"] for t in taxonomy["failure_types"]}
    records = load()
    as_json = json.dumps(records, indent=2, ensure_ascii=False) + "\n"
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    for r in records:
        writer.writerow(flatten(r, lens_by_tag))
    return as_json, buf.getvalue()


def main():
    as_json, as_csv = render()
    if "--check" in sys.argv:
        stale = []
        if not OUT_JSON.exists() or OUT_JSON.read_text(encoding="utf-8") != as_json:
            stale.append(OUT_JSON.name)
        if not OUT_CSV.exists() or OUT_CSV.read_text(encoding="utf-8") != as_csv:
            stale.append(OUT_CSV.name)
        if stale:
            print("Out of date:", ", ".join(stale), "- run python scripts/build_exports.py")
            return 1
        print("Exports are up to date.")
        return 0
    OUT_JSON.write_text(as_json, encoding="utf-8")
    OUT_CSV.write_text(as_csv, encoding="utf-8", newline="")
    print(f"Wrote {OUT_JSON.name} and {OUT_CSV.name} ({len(load())} records).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
