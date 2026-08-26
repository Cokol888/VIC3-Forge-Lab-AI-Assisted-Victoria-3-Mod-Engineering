# Repository Change Policy

## Before writing

- Fetch the current file and SHA when updating an existing path.
- Preserve unrelated content.
- Prefer small reviewable changes.
- Do not edit generated output without checking its generator/source-of-truth.
- Do not silently change build/runtime status.

## State synchronization

Update only files affected by the change.

### Source implementation prepared
Update source + changelog. Update state to `CODE_PREPARED` or `STATIC_VERIFIED` only after the corresponding evidence exists.

### Static validation completed
Record static evidence. Keep runtime pending if runtime proof is required.

### Runtime gate completed
Record exact environment and observed scenarios; then update gate, evidence, state, and manifest consistently.

### Environment changed
Update manifest/environment and mark dependent evidence `REVALIDATION_REQUIRED`.

### New mod workspace
Start from `mods/_template/`, register it in `catalog/mods.yml`, and create only Victoria 3 directories the mod actually uses.

## Third-party boundary

Before copying or modifying third-party upstream material, read:

- `THIRD_PARTY_NOTICES.md`
- target workspace `upstream/UPSTREAM.md`

Do not apply a repository-wide open-source license to third-party code merely because project-owned prompts/tooling are intended to be open source.

## GitHub Actions

Treat CI validators as static evidence according to what they actually execute. Inspect failed job logs before changing code. Do not retry repeatedly without diagnosing the failure.

## Commit intent

Use concise intent-oriented messages, for example:

- `feat(mod): add exact Army diagnostic gate`
- `fix(navy): preserve frozen fleet selection contract`
- `test(cmp): add runtime regression record`
- `docs(evidence): record 1.13.10 scope proof`
- `chore(repo): normalize legacy workspace`
