# Cheat Menu Pro — VIC3 Forge Workspace

This directory is the normalized engineering workspace for the historical Cheat Menu Pro development line currently preserved under the legacy Workshop-shaped path.

## Current imported baseline

- Project version: `0.3-beta18.1-pre1.1`
- Build ID: `CMP-0.3-B18-1-PRE1-1-20260823`
- Target Victoria 3 version: `1.13.10`
- Upstream Workshop ID: `3717461054`
- Imported state: `STATIC_VERIFIED / RUNTIME_PENDING`
- Parent Navy contract: `beta18 Final / Runtime PASS / Frozen`

## Workspace policy

New engineering work should use this workspace as the control plane.

The existing legacy snapshot is retained unchanged for provenance and reproducibility. Do not duplicate the full upstream tree into this workspace until redistribution rights and the desired source/overlay model are explicitly resolved.

## Layout

- `MANIFEST.yml` — machine-readable project identity and state.
- `ROADMAP.md` — Active Gate, Next Milestone, and queued roadmap.
- `CHANGELOG.md` — normalized workspace history.
- `upstream/` — upstream identity and immutable provenance metadata.
- `engineering/` — state, decisions, evidence, regressions, gates, and provenance.
- `tests/` — static/runtime/regression evidence index.
- `mod/` — future deployable project-owned mod/overlay root.

## Legacy source

Historical snapshot:

`../Bilds/cheat_menu_pro_v0.3_beta18_1_pre1_1_army_scope_proof_ru/3717461054/`

Important legacy evidence includes:

- `registry/build.json`
- `baseline_manifest.json`
- `MECHANICS_AUDIT.md`
- `QA_REPORT.json`
- `docs/`
- `registry/`
- `tools/`

## Current Active Gate

Runtime verification of `beta18.1-pre1.1 — Army Scope Proof`.

The workspace must not promote this build to Runtime PASS until the exact Army runtime checklist is completed and recorded.
