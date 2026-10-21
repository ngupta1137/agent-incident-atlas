# Field guide

This document explains every field in `incident.schema.json` (schema version 0.1.0). The schema enforces structure. This guide explains what good content looks like.

## Identity and provenance

| Field | Required | Notes |
|---|---|---|
| `schema_version` | yes | Always `"0.1.0"` for this release. |
| `id` | yes | `AIA-<year>-<NNN>`, for example `AIA-2026-021`. Must match the file name. Maintainers assign the final number at merge. |
| `seed` | yes | `true` only for maintainer-written illustrative records. Every community submission is `false`. |
| `provenance` | yes | `composite-illustration` (seed only), `first-hand-participant`, `public-reporting-reconstruction`, or `contributor-composite`. Seed records must use the first value and community records must not. |

## What happened

| Field | Required | Notes |
|---|---|---|
| `title` | yes | A plain sentence about the event. No names of companies, products, or people. |
| `date` | yes | `YYYY-MM`, `YYYY-MM-DD`, or `{ "start": ..., "end": ... }` for failures that ran over a period. Use month precision unless the day matters to the analysis. |
| `sector` | yes | Coarse sector of the deploying organization. Pick the broadest value that is still true. |
| `agent_type` | yes | The job the agent was doing. Classify by function, not by vendor or framework. |
| `autonomy_level` | yes | `recommend-only`, `act-with-approval`, `act-with-review`, or `act-autonomously`. Describe the authority the agent had in the failing workflow, not the best case across the product. |
| `narrative` | yes | 150 to 300 words. Chronological. Say what the agent was set up to do, what it did, how the harm followed, and how it was noticed and stopped. Describe facts, not fault. |

## How it is classified

| Field | Required | Notes |
|---|---|---|
| `failure_types` | yes | One to three tags from `taxonomy.md`. Use a secondary tag only when its control was also missing and would independently have changed the outcome. |
| `primary_failure_type` | yes | One tag from `failure_types`. Apply the counterfactual and tie-break rules in `taxonomy.md`. Two reviewers should land on the same value. |

## Consequences

| Field | Required | Notes |
|---|---|---|
| `business_impact.severity` | yes | `low`, `moderate`, `high`, or `critical`. The definitions are in the schema description. |
| `business_impact.categories` | yes | One or more of `financial`, `operational`, `regulatory`, `customer`, `reputational`, `data-exposure`, `safety`. |
| `business_impact.description` | yes | Ranges and aggregates only, for example "low six figures" or "about 2,000 customers". |
| `root_cause` | yes | The system or process condition that allowed the failure. "The model hallucinated" is not a root cause. Ask why that output could reach harm. |
| `governance_gap.control_category` | yes | One of eleven control families, listed in the schema. |
| `governance_gap.missing_control` | yes | A control someone could build, for example "Out-of-band human verification before any change to payment destination". |
| `governance_gap.description` | yes | Why the control was missing: never designed, designed but not built, built but bypassed, or built but unowned. |
| `detection.method` | yes | How the failure was first noticed. |
| `detection.time_to_detect` | yes | Elapsed time from first harmful action to detection. Use `unknown` if it cannot be established. |
| `lessons_learned` | yes | Two to five changes another organization could make. Write each as an action, not a summary of the incident. |

## Rules that the schema cannot express

`scripts/validate.py` also checks these:

1. The file name equals `<id>.json`.
2. `primary_failure_type` appears in `failure_types`.
3. The narrative is 150 to 300 words.
4. IDs are unique across the dataset.
5. The tag list in the schema matches `schema/taxonomy.json`.
6. No em dashes in record text.
