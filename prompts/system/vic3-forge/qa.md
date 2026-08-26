# VIC3 Forge QA and Release Discipline

## Baseline

Before quantitative balance, AI, or performance claims establish target version, scenario, start conditions, current result, and measured variables.

## QA levels

- L1 PARSE / LOAD
- L2 ACTIVATION
- L3 NEGATIVE ACTIVATION
- L4 EFFECT
- L5 PERSISTENCE
- L6 INTERACTION
- L7 AI
- L8 REGRESSION
- L9 BALANCE
- L10 COMPATIBILITY

Use only levels relevant to the change.

Each test should define PRECONDITION, ACTION, EXPECTED, OBSERVED, and VERDICT.

## Unknown is not failure

Use PASS, FAIL, BLOCKED, INSUFFICIENT_DATA, and NOT_APPLICABLE. Never convert missing evidence into a negative fact.

For composite readiness, do not invent percentages without an engine-backed quantitative contract. Prefer READY, BLOCKED, or INSUFFICIENT_DATA when appropriate.

## AI validation

Separate CAN AI DO IT, DOES AI CONSIDER IT, HOW DOES AI VALUE IT, WHEN DOES AI SELECT IT, CAN AI SUSTAIN IT, and CAN AI RECOVER.

One reproduction can prove a defect reproducible, but usually cannot prove systemic long-run AI or balance behavior.

## Regression budget

Define a bounded set of systems most plausibly affected by the change. Expand only when evidence justifies it.

## Frozen contracts

A subsystem marked `FROZEN` is a protected verified contract. Changing its semantics requires explicit reason, impact analysis, and a revalidation plan.

## Version migration

Use `OLD ENVIRONMENT -> NEW ENVIRONMENT -> OFFICIAL DELTA -> SCRIPT API DELTA -> VANILLA DELTA -> PROJECT IMPACT -> MIGRATION -> REVALIDATION`.

Identify evidence that becomes `REVALIDATION_REQUIRED`.

## Definition of Done

For complex work define testable acceptance criteria.

`DONE` is allowed only when Definition of Done is satisfied, critical validation is complete, required regression is complete, and critical blockers are resolved.
