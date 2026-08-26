# VIC3 Forge Workflow

## Engineering State

Track goal, state, Definition of Done, environment, design intent, facts, observations, decisions, plans, assumptions, hypotheses, proposed/applied changes, completed/pending tests, regressions, unknowns, blockers, active gate, next milestone, and queued roadmap.

## Active Horizon

Default detailed horizon: `ONE ACTIVE GATE + ONE NEXT MILESTONE`.

Everything else is QUEUED ROADMAP.

An Active Gate defines QUESTION, EVIDENCE REQUIRED, TEST, PASS CONDITION, and FAIL CONDITION.

Do not deeply implement downstream work while its prerequisite gate remains unverified.

## Minimal change set

Before a non-trivial change establish OBJECTIVE, HYPOTHESIS, TARGET OBJECTS, TARGET FILES, CHANGE, EXPECTED OBSERVATION, TEST, ROLLBACK, and REGRESSION RISK.

Minimize blast radius while preserving causal clarity.

## Causal atomicity

A diagnostic iteration should primarily answer one causal question. Do not change independent causes together when results would become ambiguous.

Mechanically linked edits may be batched when cause, hypothesis, and observable result are shared.

## Hypothesis queue

Prioritize using EVIDENCE, LIKELIHOOD, INFORMATION GAIN, TEST COST, BLAST RADIUS, and REVERSIBILITY.

## Iteration ledger

Record HYPOTHESIS, EVIDENCE BEFORE, TEST/CHANGE, EXPECTED, OBSERVED, RESULT, NEW KNOWLEDGE, and STATUS.

STATUS: CONFIRMED, REJECTED, INCONCLUSIVE, BLOCKED.

After two consecutive INCONCLUSIVE iterations, stop repeating the same strategy and reassess.

## Stop rules

Stop or reassess when expected information gain approaches zero or intervention cost/risk rises without stronger causal evidence. Do not random-tune.

## Vanilla first

Prefer `VERIFIED VANILLA PATTERN > VERIFIED SCRIPT PRIMITIVE > NEW COMPOSITION > UNVERIFIED INVENTION`.

## Scope protocol

For complex script logic use `INCOMING SCOPE -> SCOPE TRANSITION -> TRIGGER -> EFFECT -> RESULTING STATE`.

Check root, this, saved scopes, event targets, iterators, nested scopes, and implicit transitions when relevant.

## Debugging ladder

Use relevant layers only:

`FILE EXISTS? -> FILE LOADED? -> PARSER ERRORS? -> OBJECT LOADED? -> OBJECT OVERRIDDEN? -> CORRECT SCOPE? -> TRIGGER TRUE? -> EFFECT EXECUTED? -> STATE CHANGED? -> STATE OVERWRITTEN? -> UI REPRESENTS RESULT?`

Use real debug-mode evidence, error.log, generated script docs, game files, and runtime reproduction when available.

## Context compaction

Compress long sessions into VERIFIED FACTS, DECISIONS, REJECTED PATHS, CURRENT STATE, and ACTIVE GATE. Preserve rejected directions as `REJECTED — reason`.
