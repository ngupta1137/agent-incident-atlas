# Failure taxonomy

Version 0.1.0. This is the core of the Atlas. Every incident is tagged with one primary failure type and up to two secondary types.

These are **governance** failure types. They describe the control that was missing, not the way the model was wrong. A model that produces a bad answer is expected. The governance failure is whatever allowed that answer to become an action, a record, or a decision that caused harm. This matters for enterprise AI, because you can swap a model in a week but a missing approval step stays missing until someone builds it.

## The three questions

The taxonomy follows one idea. An organization deploying agentic AI has to answer three questions, and each failure type is a failure to answer one of them.

| Lens | Question | Failure types |
|---|---|---|
| **Authorize** | What is the system permitted to do, and who approved that? | FT-01, FT-02, FT-04, FT-08, FT-10 |
| **Prove** | What evidence says the system, its inputs, and its vendors deserve that authority? | FT-05, FT-06, FT-09, FT-11, FT-14 |
| **Revoke** | How is authority taken back, stopped, or undone? | FT-03, FT-07, FT-12, FT-13 |

## How to tag an incident

Two people tagging the same incident should pick the same primary tag. Follow these steps in order.

1. **Write the causal chain** in plain steps, from the first condition to the harm. Do not skip to the model's error.
2. **For each step, name the control** that would have stopped the chain there. If no control comes to mind, the step is not a candidate.
3. **Apply the counterfactual test.** For each candidate control, ask: if this control had existed and worked, would the harm have been prevented or reduced to a minor event? Keep only the candidates that pass.
4. **Pick the primary tag with the earliest-control rule.** Among the candidates that pass, choose the control that would have operated earliest in the chain. A permission that should not have existed (FT-01) comes before an approval step that should have caught its use (FT-02).
5. **Add secondary tags sparingly.** Add up to two more only if that control would also have independently prevented the harm. Do not add a tag because it is related.
6. **Do not tag the model error.** "The model was wrong" is never a tag. Ask what let a wrong output reach harm.

### Commonly confused pairs

| If you are torn between | Use this rule |
|---|---|
| FT-01 and FT-02 | If the agent should not have been able to do the action at all, FT-01. If the agent could legitimately do it, but a person should have approved this instance, FT-02. |
| FT-01 and FT-10 | If the agent was granted wider access to a system of record than the task needed, FT-01. If data from one user, tenant, or session crossed into another through shared memory, a shared index, or a shared context, FT-10. |
| FT-03 and FT-01 | If the access was appropriate when granted and became inappropriate because something changed later, FT-03. If it was never appropriate, FT-01. |
| FT-04 and FT-01 | If the harmful instruction came from content the agent read, FT-04. If the instruction came from a legitimate user or the agent's own plan, it is not FT-04. |
| FT-05 and FT-09 | If the agent acted on correct data that had gone out of date, FT-05. If the data or output was wrong when produced, FT-09. |
| FT-06 and FT-14 | If the change or action came from a third party and the organization had no review right, FT-06. If the organization's own team made the change and shipped it without evaluation, FT-14. |
| FT-07 and FT-13 | If the agent could not decide to stop, FT-07. If people could not make it stop, FT-13. |
| FT-12 and FT-02 | If a human gate was missing, FT-02. If a human gate existed or would not have helped, but the action could not be undone, FT-12. |

---

## FT-01 Over-authorized tool use

**Tag:** `over-authorized-tool-use` | **Lens:** Authorize

**Definition.** The agent held permissions to a tool, dataset, or system that exceeded what its task required, and the harm came through the excess. The agent was usually built on an inherited account, a convenience grant, or a vendor connector that offered only broad scopes. The test is a comparison between the permission the agent held and the permission its written purpose needed. If the first is larger and the harm lives in the difference, tag this.

**Tag when:** the harm could not have occurred with a permission scoped to the stated task.
**Do not tag when:** the permission was appropriate and a person should simply have approved this use (FT-02).

**Example.** An analytics agent described as read-only runs under a shared service account that can write to production tables. Asked to clean a working copy, it deletes rows from a live table.

## FT-02 Missing human-in-the-loop gate

**Tag:** `missing-hitl-gate` | **Lens:** Authorize

**Definition.** An action with significant consequence took effect without a person approving it, although a person should have. The action was within the agent's legitimate scope, so this is about the approval step, not the permission. It also covers gates that existed for human users but did not apply to the agent's path, such as an approval rule that fires in a user interface but not through an API.

**Tag when:** a reasonable control design would have required a named person to approve this instance, and none did.
**Do not tag when:** the agent had no right to perform the action in the first place (FT-01), or a gate existed and a person approved it badly (this is a human judgment failure and out of scope).

**Example.** A payables agent changes a supplier's bank details after an emailed request. Company procedure requires a callback to a known number, but the callback lived in the manual process and was never built into the agent's workflow.

## FT-03 Un-revoked access after role change

**Tag:** `unrevoked-access-after-role-change` | **Lens:** Revoke

**Definition.** Access that was appropriate when granted stayed in place after the person, team, project, or the agent's own role changed. The grant outlived the reason for it. This includes delegated tokens that outlive a transfer, temporary elevations never removed, and agent permissions left over from a pilot. Identity lifecycle processes usually cover people and forget agents and their delegations.

**Tag when:** the access was legitimate at some point and a documented event (transfer, departure, end of pilot) should have ended it.
**Do not tag when:** the access was never justified (FT-01).

**Example.** A scheduled agent approves expense exceptions using a manager's delegated rights. The manager moves to another department. The role is removed, the delegation is not, and the agent keeps approving for eleven weeks.

## FT-04 Prompt-injection scope escape

**Tag:** `prompt-injection-scope-escape` | **Lens:** Authorize

**Definition.** Text the agent read from an untrusted source, such as an email, web page, document, or ticket, was treated as an instruction, and the agent used its tools to act outside the scope the operator intended. Two controls were absent: separation between data and instructions, and limits on what the agent's tools may do with content-derived requests, such as an allowlist of recipients.

**Tag when:** an instruction embedded in content the agent processed directly caused the harmful action.
**Do not tag when:** the harmful request came from an authenticated user who was entitled to ask, even if the request was a bad idea.

**Example.** A support agent summarizing inbound email obeys hidden text asking it to forward ticket histories to an outside address, and its send tool accepts any recipient.

## FT-05 Stale-data action

**Tag:** `stale-data-action` | **Lens:** Prove

**Definition.** The agent took an action based on data that was accurate once but no longer reflected reality, and nothing in the workflow checked freshness before acting. Typical causes are a failed refresh job, a lagging replication feed, or a cached snapshot. The data pipeline failed silently and the agent trusted it.

**Tag when:** the same input would have been correct at an earlier time and the agent acted without a freshness check.
**Do not tag when:** the input was wrong when produced (FT-09).

**Example.** A replenishment agent reads a nightly inventory snapshot. The refresh job fails after a migration. For nine days the agent sees low stock that no longer exists and keeps ordering.

## FT-06 Unchecked vendor action

**Tag:** `unchecked-vendor-action` | **Lens:** Prove

**Definition.** An agent run, hosted, or updated by a third party took or recommended an action affecting the organization's customers, records, or systems, and the organization had no contractual right or technical access to review, constrain, or audit it. The vendor's reported metrics were accepted in place of evidence. In enterprise AI, this is the gap between buying a capability and being able to verify what it does under your name.

**Tag when:** the organization could not see or control the vendor-side behavior that caused the harm.
**Do not tag when:** the vendor supplied a component and the organization's own team made the failing change or configuration (FT-14 or another type).

**Example.** A vendor's hosted appeals agent adds generated clinical statements to insurance appeals filed under the hospital's name. The hospital sees only monthly totals of appeals and dollars recovered.

## FT-07 Missing stop criteria

**Tag:** `missing-stop-criteria` | **Lens:** Revoke

**Definition.** The agent had no defined condition under which it must stop, escalate, or hand over, so it repeated an action or pursued an open-ended goal well past the point of usefulness. Missing criteria include a maximum number of attempts, a rule to escalate after repeated failure, and a definition of what "done" means for open-ended tasks.

**Tag when:** the agent itself would have stopped with a defined limit, attempt cap, or completion rule.
**Do not tag when:** the agent stopped as designed but people could not interrupt it from outside (FT-13).

**Example.** A remediation agent restarts a service in response to an alert that restarts cannot fix. It does this about 400 times in five hours, opening a ticket each time.

## FT-08 Cost or latency blowout

**Tag:** `cost-latency-blowout` | **Lens:** Authorize

**Definition.** The agent consumed compute, tokens, tool calls, or time far beyond what was planned, and no limit on spend or duration was set or enforced. This is a failure to authorize a resource budget. It covers runaway invoices and also response times that make a customer-facing agent unusable. Use it when the resource overrun is itself the harm.

**Tag when:** a per-run, per-project, or per-day ceiling would have capped the harm.
**Do not tag when:** a loop was the cause and a stop rule would have fixed it, with cost only a side effect (FT-07).

**Example.** A research agent told to map regulatory changes in 14 jurisdictions "until coverage is complete" uses a premium model and full documents for three days and spends about fourteen times the monthly forecast.

## FT-09 Unvalidated output propagation

**Tag:** `unvalidated-output-propagation` | **Lens:** Prove

**Definition.** The output of one model or agent was passed to a downstream agent, system, or decision as if it were verified, and no schema, range, consistency, or reasonableness check sat between them. The first output was wrong when produced. The failure is that the handoff trusted it. This is the main multi-agent failure mode.

**Tag when:** a simple check at the handoff would have caught the bad value.
**Do not tag when:** the output was correct when produced and later went out of date (FT-05).

**Example.** An extraction agent swaps day and month in some certificate dates. A compliance agent reads the table and clears lots whose certificates have already expired.

## FT-10 Cross-context data leakage

**Tag:** `cross-context-data-leakage` | **Lens:** Authorize

**Definition.** Information belonging to one user, customer, tenant, or session appeared in another's interaction because the agent's memory, retrieval index, or context was shared across them. The only barrier was an instruction in the prompt, which is not a control. Enforcement has to sit in the retrieval or storage layer.

**Tag when:** the leak path is a shared store, shared memory, or shared context spanning separate parties.
**Do not tag when:** the agent was simply granted wide access to one system of record (FT-01).

**Example.** A support agent answers from a ticket index covering all customers. It quotes endpoint names and a renewal date from another customer's ticket in its reply.

## FT-11 Missing audit trail

**Tag:** `missing-audit-trail` | **Lens:** Prove

**Definition.** The organization could not reconstruct what the agent did, what it saw, or which version of the prompt and model produced a decision. Logs captured outcomes but not inputs, versions, or reasoning steps. The harm arrives later, when someone must explain, contest, or reproduce a decision and cannot.

**Tag when:** the harm is an inability to explain, reproduce, attribute, or defend an agent action.
**Do not tag when:** logs existed and nobody read them (this is a monitoring gap, tag the control that would have acted on what the logs showed).

**Example.** A benefits agency's agent tiers cases. When an appeal asks why 300 cases were deprioritized, the agency cannot recover the documents, prompt version, or model version used.

## FT-12 Irreversible action with no rollback

**Tag:** `irreversible-action-no-rollback` | **Lens:** Revoke

**Definition.** The agent took an action that could not be undone, or could be undone only at large cost, and the workflow had no staging, dry run, canary release, or undo path. Sent messages, canceled non-refundable bookings, deleted records without backups, and public postings are the common cases. The size of the harm comes from the lack of reversal.

**Tag when:** the action was final and a staged rollout or dry run would have limited the damage.
**Do not tag when:** the action was reversible but nobody tried (a process failure, not a control gap).

**Example.** An outreach agent sends 14,000 students incorrect financial aid status messages in one batch. Messages cannot be recalled and there was no small pilot batch first.

## FT-13 Missing kill switch

**Tag:** `missing-kill-switch` | **Lens:** Revoke

**Definition.** People knew the agent was misbehaving and could not stop it quickly. There was no pause control owned by the business or operations team, so disabling the agent needed a code change, a change-board approval, or the one engineer who knew how. The time between noticing and stopping is the harm.

**Tag when:** detection happened well before containment and the delay came from the lack of a fast, owned stop mechanism.
**Do not tag when:** nobody noticed for a long time (this is a detection gap, tag the monitoring control that was missing).

**Example.** A support agent tells customers they have a 90 day return window after a knowledge base error. Staff spot it within an hour. Removing the agent takes nine hours because it needs an approved engineering change.

## FT-14 Unevaluated change release

**Tag:** `unevaluated-change-release` | **Lens:** Prove

**Definition.** The organization's own team changed a prompt, model version, tool definition, retrieval source, or configuration and released it to production without running an evaluation that would have shown the regression. The release path allowed edits to bypass the checks that code changes normally pass. For agentic AI, a prompt edit is a production change and needs a gate like any other.

**Tag when:** a regression test or evaluation gate on the change would have caught the failure.
**Do not tag when:** a vendor made the change and the organization had no review right (FT-06).

**Example.** A business analyst edits an agent prompt to make summaries shorter. The edit goes live the same afternoon. The summaries start dropping exclusion clauses, and the regression set was never run.

---

## What this taxonomy leaves out

- **Model quality errors on their own.** Hallucinations, reasoning mistakes, and bias are real, but they are not governance types. They appear here only through the control that failed to contain them.
- **Malicious insiders and conventional intrusions.** The Atlas covers agent failures, not general security incidents.
- **Human judgment errors inside a working gate.** If a person reviewed properly and made a bad call, that is outside this taxonomy.

## Changing the taxonomy

The taxonomy has a version. To propose a new type, open an issue with at least three incidents that no existing type separates cleanly, a one paragraph definition, and a rule that distinguishes it from its nearest neighbor. Changes to a definition increment the minor version and are recorded in `CHANGELOG.md`.
