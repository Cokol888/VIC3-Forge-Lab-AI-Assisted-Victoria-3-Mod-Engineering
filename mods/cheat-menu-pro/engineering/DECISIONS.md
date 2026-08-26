# Engineering Decisions

## ADR-001 — Preserve legacy snapshot as provenance

**Status:** Accepted

The existing Workshop-shaped snapshot remains unchanged at its current legacy path. The normalized workspace references it rather than duplicating it.

Reason: preserve reproducibility and provenance while avoiding another copy of third-party upstream content.

## ADR-002 — Separate static and runtime status

**Status:** Accepted

A global QA `PASS` cannot imply runtime success. Project state records static, runtime, and regression status separately.

## ADR-003 — Protect beta18 Final Navy as a frozen contract

**Status:** Accepted

Military Operations work must not modify the accepted beta18 Final Navy semantics without explicit impact analysis and revalidation.

## ADR-004 — One Active Gate, one Next Milestone

**Status:** Accepted

Detailed engineering remains focused on the current runtime gate and the immediately following contract-proof milestone. Later roadmap items remain queued.

## ADR-005 — New development uses VIC3 Forge v0.2 RC1

**Status:** Accepted

The imported legacy baseline predates the normalized repository workflow. New reasoning and development should use `prompts/system/vic3-forge/v0.2-rc1.md` as the control-plane prompt.
