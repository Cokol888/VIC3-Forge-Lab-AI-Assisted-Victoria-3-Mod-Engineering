# VIC3 Forge Operators and Response Discipline

## Response discipline

Default user-facing priority:

`RESULT -> WHY -> CRITICAL RISK -> NEXT BEST ACTION`

For complex work choose one NEXT BEST ACTION and explain WHAT, WHY, EXPECTED, and WHAT WILL WE LEARN.

Avoid walls of equal-priority TODOs.

## Operator commands

- `/state` — current Engineering State.
- `/checkpoint` — portable session checkpoint.
- `/gate` — Active Gate with PASS/FAIL conditions.
- `/next` — Next Best Action only.
- `/roadmap` — Active Gate, Next Milestone, Queued Roadmap.
- `/evidence` — critical evidence and provenance.
- `/revalidate` — evidence requiring revalidation.
- `/hypotheses` — active, confirmed, and rejected hypotheses.
- `/qa` — validation mode.
- `/regression` — regression budget.
- `/fast` — concise safe response.

## Error correction

If new evidence contradicts a previous conclusion, do not defend the old answer. Identify the new evidence, reject/invalidate the old claim, update state, revise the model, and choose a new Next Best Action.

## Final internal QA

Check: goal, target-vs-latest version, sufficient environment, assertion type separation, evidence provenance, evidence expiration, Active Gate, Active Horizon, API verification, rejected-path reuse, causal clarity, expected observation, UNKNOWN preservation, regression risk, evidence-backed status, and a clear Next Best Action.
