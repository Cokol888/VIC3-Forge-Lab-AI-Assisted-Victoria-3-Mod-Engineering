# Changelog

## Military Operations discovery — 2026-08-27

- Preserved `beta18.1-pre1.1` as `RUNTIME_PENDING`; no runtime claims were promoted.
- Confirmed existing Cheat Menu Pro script-side Army enumeration can collect exact Army formation scopes into variable lists.
- Confirmed a Victoria 3 1.13-compatible GUI pattern for scope-backed lists and `Scope.GetMilitaryFormation` promotion.
- Added `engineering/gates/beta18.1-pre2.0-army-list-projection-contract.md` as a next-milestone contract candidate for a self-contained Army picker without guessed GUI accessors.
- Kept beta18 Final Navy semantics frozen and unchanged.

## Workspace migration — 2026-08-27

- Created normalized `mods/cheat-menu-pro/` engineering workspace.
- Preserved the existing Workshop-shaped snapshot as immutable legacy provenance.
- Added upstream identity lock with archive and canonical tree hashes.
- Imported build identity `0.3-beta18.1-pre1.1` / `CMP-0.3-B18-1-PRE1-1-20260823`.
- Separated static, runtime, and regression statuses.
- Imported beta18 Final Navy as a frozen project contract.
- Defined Army Scope Runtime Verification as the Active Gate.
- Defined Readiness Contract Proof as the Next Milestone.
- Future engineering baseline set to VIC3 Forge v0.2 RC1.

Historical feature/build changelogs remain in the legacy snapshot under `docs/` and the historical README files.
