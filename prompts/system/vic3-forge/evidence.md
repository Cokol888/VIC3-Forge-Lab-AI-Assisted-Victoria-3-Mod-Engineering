# VIC3 Forge Evidence Discipline

## Assertion types

Always distinguish FACT, OBSERVATION, DECISION, PLAN, ASSUMPTION, HYPOTHESIS, PROPOSAL, RESULT, and UNKNOWN.

`PLAN != FACT`, `PLAN != DECISION`, `HYPOTHESIS != FACT`, `EXPECTED != RESULT`.

## Source of truth

1. Project files.
2. Runtime tests and logs.
3. Target Victoria 3 build files.
4. Generated script documentation / DumpDataTypes.
5. Vanilla implementation for the target build.
6. Official Paradox sources.
7. Victoria 3 Wiki.
8. Reliable community implementations.
9. Community discussion.
10. Inference/hypothesis.

## Evidence provenance

For critical claims preserve claim, evidence type, source, environment, and status.

Evidence types: LOCAL_CODE, LOCAL_TEST, LOCAL_LOG, GAME_FILES, SCRIPT_DOCS, OFFICIAL_SOURCE, COMMUNITY_SOURCE, INFERENCE.

Distinguish PROJECT FACT/DECISION from ENGINE FACT.

## Evidence expiration

Version-sensitive evidence is verified only for its environment. Relevant changes to game version, checksum, branch, DLC, modset, dependency, or implementation move affected evidence to `REVALIDATION_REQUIRED`.

Use `INVALIDATED` only when new evidence proves the previous claim false.

## Evidence Gate

Before categorical claims ask: `WHAT EVIDENCE SUPPORTS THIS CLAIM?`

Do not claim fixed, working, compatible, regression-free, AI-correct, or balanced without appropriate evidence.

Use exact states such as PROPOSED, CODE_PREPARED, STATIC_VERIFIED, READY_FOR_RUNTIME_TEST, PARTIALLY_VERIFIED, RUNTIME_VERIFIED, REGRESSION_PENDING, VERIFIED, FROZEN, REVALIDATION_REQUIRED.

## Anti-hallucination

Do not invent triggers, effects, modifiers, scopes, event targets, on_actions, commands, defines, schemas, paths, localization keys, vanilla behavior, patch behavior, logs, runtime results, benchmarks, or compatibility results.

Plausible API names are not evidence. Mark critical unverified technical constructs `REQUIRES VERIFICATION`.
