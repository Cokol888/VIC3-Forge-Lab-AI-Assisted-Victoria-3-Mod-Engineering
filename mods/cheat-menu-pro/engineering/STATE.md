# Engineering State

## Goal

Continue the post-beta18 Military Operations line without modifying the frozen Navy semantics and without promoting unverified runtime behavior.

## Environment

- Target Victoria 3: `1.13.10`
- Checksum: `2964`
- Imported build: `CMP-0.3-B18-1-PRE1-1-20260823`
- Prompt baseline for future work: `VIC3 Forge v0.2 RC1`

## Current state

`RUNTIME_PENDING`

## Confirmed

- `beta18 Final` Navy is recorded by the project as Runtime PASS and frozen.
- The imported `beta18.1-pre1.1` build has passed its recorded static validation suite.
- `pre1.1` is intentionally read-only for the Army scope proof and adds no new gameplay writes.
- The legacy build registry records `STATIC_PASS_RUNTIME_PENDING`.

## Not yet confirmed

- Runtime transport of exact selected Army into the observer/probes for the imported build.
- Runtime A/B selection isolation.
- Negative Fleet/no-selection behavior.
- Persistence and regression behavior required by the runtime checklist.

## Active Gate

`beta18.1-pre1.1-army-scope-runtime`

See `engineering/gates/beta18.1-pre1.1-army-scope-runtime.md`.

## Next Milestone

`beta18.1-pre2.0-readiness-contract-proof`

## Queued Roadmap

- Exact Fleet operational diagnostics
- Amphibious context matrix
- Readiness engine
- Native workflow proof
- Military Operations regression candidate
- Military Operations final

Queued items are plans, not confirmed contracts.
