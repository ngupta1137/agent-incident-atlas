# Contributing an incident

Thank you for adding to the Atlas. This guide covers what you may submit, how to anonymize it, what reviewers look for, and how to open the pull request.

The Atlas exists so the industry can study how agentic AI actually fails in production. A record is only useful if it is specific about the missing control, and only safe if nobody can be identified from it. Both matter.

## Before you write anything

1. **Confirm you may share it.** If you learned about the event through your job, check your confidentiality obligations and get approval where your employer requires it. Contributions about your own employer's systems are your responsibility to clear. If you are unsure, do not submit. You can submit a contributor-composite instead (see below).
2. **Check that it is in scope.** The Atlas covers failures of agentic AI systems, meaning systems that take actions through tools, other systems, or other agents. Chatbots that only produce text are in scope when the text was acted on as a decision. General security intrusions with no agent involved are out of scope.
3. **Check for an existing record** that already covers the same event or the same failure path.

## Anonymization rules

A reviewer must not be able to identify the organization, the people, the product, or the system from your record. Apply every rule.

1. **No company names.** This includes the deploying organization, customers, suppliers, partners, and competitors. Use a coarse sector from the schema.
2. **No product or vendor names.** Describe the function: "a hosted appeals agent", "the identity system's reset function". Do not name models, frameworks, or platforms.
3. **No personal names.** No employees, customers, executives, or contractors. Use roles: "an analyst", "the on-call lead".
4. **No identifying system details.** No account names, hostnames, endpoint names, table names, repository names, ticket numbers, or internal tool names. Say what kind of thing it was, not what it was called.
5. **Aggregate numbers.** Use ranges and rounded figures: "low six figures", "about 2,000 customers", "roughly nine days". Do not give exact amounts, exact counts, or exact timestamps that could be matched to a news story or a filing.
6. **Month precision for dates.** Use `YYYY-MM` unless the day is essential to the analysis.
7. **No unique stories.** If the event was reported publicly or is distinctive enough that insiders would recognize it, generalize the unusual details or submit a contributor-composite.
8. **No security-sensitive detail.** Do not include working exploit text, payloads, unpatched vulnerability specifics, or steps that would help someone repeat an attack. Describe the class of weakness and the missing control. If the event involves an unpatched flaw in a product, disclose it to the vendor first and wait for a fix before you submit.
9. **No blame.** Describe conditions and controls, not individuals. Do not speculate about motives.
10. **No allegations.** State what happened and what is known. Mark anything uncertain as uncertain.

## Provenance

Set `provenance` honestly:

| Value | Use when |
|---|---|
| `first-hand-participant` | You were involved in the event or its response. |
| `public-reporting-reconstruction` | You rebuilt the event from published sources. Add the source types (not links to identifying material) in the pull request description. |
| `contributor-composite` | You merged several real events into one to prevent identification. Say so in the pull request description. |

`composite-illustration` and `"seed": true` are reserved for the maintainers' illustrative records. Community submissions always use `"seed": false`.

## The review bar

Reviewers accept a record when all of these hold.

1. **It validates.** `python scripts/validate.py` passes.
2. **It is anonymized.** Two reviewers read it independently and neither can identify the organization, product, or people.
3. **The narrative is plain and factual.** 150 to 300 words, in order, with no names, no blame, and no hype.
4. **The tags pass the counterfactual test.** For each tag, if that control had existed and worked, the harm would have been prevented or become minor. The primary tag is the one whose control would have operated earliest. State your reasoning in the pull request.
5. **The governance gap is specific.** `missing_control` names a control someone could build. "Better oversight" and "the AI made a mistake" are rejected. The description says why the control was missing: never designed, designed but not built, built but bypassed, or built but unowned.
6. **The root cause is a system condition.** Not a model quality complaint and not a person.
7. **The lessons are actions.** Each one is a change another organization could make.
8. **Provenance is credible.** The reviewer can reasonably believe the record reflects a real pattern. Reviewers may ask questions. They will not ask for identifying details.
9. **Tagging agrees.** Two maintainers tag the incident independently from your narrative. If their primary tags differ from yours, the narrative may be missing the fact that decides it, or the taxonomy needs a clearer rule. Either outcome is useful, and both are discussed openly in the pull request.

Records are declined, or sent back with questions, when they are marketing in disguise, name or imply an identifiable organization, repeat an existing record, or have no specific governance gap.

## How to submit

1. Fork the repository and create a branch named `incident/<short-topic>`.
2. Copy `notebooks/02_postmortem_template.ipynb` and work through it with your own notes. It validates your record as you go.
3. Save your record as `data/incidents/AIA-<year>-<NNN>.json`. Use the next unused number. Maintainers may renumber at merge.
4. Set `"seed": false` and a valid `provenance`.
5. Run:
   ```bash
   pip install -r requirements.txt
   python scripts/validate.py
   python scripts/build_exports.py
   ```
6. Commit the new file and the updated `data/atlas.json` and `data/atlas.csv`.
7. Open a pull request and fill in the template (below). Continuous integration runs the same checks.

You may also open an issue to discuss a possible record before writing it up, without sharing any details you are not comfortable sharing publicly.

## Pull request template

The same text lives in `.github/PULL_REQUEST_TEMPLATE.md` and loads automatically.

```markdown
## Incident summary
One sentence, anonymized.

## Provenance
- [ ] first-hand-participant
- [ ] public-reporting-reconstruction (source types: ...)
- [ ] contributor-composite (events merged: ...)

## Anonymization checklist
- [ ] No company, vendor, or product names
- [ ] No personal names
- [ ] No identifying system details (accounts, endpoints, tools, tickets)
- [ ] Numbers are aggregate or ranges, dates are month precision
- [ ] No exploit details or unpatched vulnerability specifics
- [ ] I have the right to share this, and any employer approval is in place

## Tagging rationale
Primary tag and why its control passes the counterfactual test:
Secondary tags (if any) and why each independently passes:
Tags I considered and rejected, and why:

## Governance gap
The specific control that was missing, in one sentence:

## Checks
- [ ] `python scripts/validate.py` passes
- [ ] `python scripts/build_exports.py` was run and the exports are committed
- [ ] `"seed": false`

## Licensing
- [ ] I agree to license this record under CC-BY-4.0
```

## Corrections and takedowns

If you believe a record identifies you or your organization, or contains an error, open an issue or contact the maintainer. Records that raise an identification concern are removed first and reviewed afterward.

## Improving the taxonomy or schema

Open an issue with at least three incidents that no existing type separates cleanly, a one paragraph definition, and a rule that distinguishes the proposed type from its nearest neighbor. Changes are recorded in `CHANGELOG.md`.

## Code contributions

Fixes to scripts and notebooks are welcome. Keep dependencies small, keep scripts runnable with the packages in `requirements.txt`, and make sure `python scripts/validate.py` and `python scripts/build_exports.py --check` pass. Code contributions are licensed under MIT.

## Conduct

Be direct and be kind. Critique records and controls, never people. Do not post identifying details in issues or pull requests, even to correct a record.
