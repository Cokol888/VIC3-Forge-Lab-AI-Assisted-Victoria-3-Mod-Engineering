# VIC3 Forge Lab

**AI-Assisted Victoria 3 Mod Engineering**

VIC3 Forge Lab is a reproducible engineering workspace for developing Victoria 3 mods with AI-assisted system prompts, live-repository skills, evidence-driven workflows, runtime validation, regression testing, and traceable releases.

## Core workflow

`system prompt -> live repository context -> engineering state -> evidence -> implementation -> runtime test -> regression -> release`

The repository keeps AI instructions, project state, mod source, test evidence, and release status explicitly separated.

## Repository map

- `prompts/` — versioned VIC3 Forge system prompts, components, templates, and operator conventions.
- `skills/` — reusable ChatGPT skills that bootstrap live repository context and workflows.
- `mods/` — one normalized engineering workspace per Victoria 3 mod, plus explicitly marked legacy snapshots.
- `catalog/` — machine-readable indexes for prompts, skills, mods, compatibility, and releases.
- `research/` — reusable research on game versions, script APIs, vanilla patterns, compatibility, and experiments.
- `references/` — local/reference metadata. Full base-game assets must not be committed.
- `tooling/` — shared validators, packaging helpers, diff tooling, and scripts when introduced.
- `docs/` — architecture, methodology, workflows, conventions, prompt engineering, and mod engineering documentation.
- `archive/` — retired project-owned prompts, mods, and experiments when needed.

See [`CATALOG.md`](CATALOG.md) for the human-readable project index.

## Engineering principles

1. Files before assumptions.
2. Target version before latest version.
3. Evidence before claims.
4. Fact, decision, plan, and hypothesis are distinct states.
5. One Active Gate and one Next Milestone; the rest stays queued.
6. Version-sensitive evidence becomes `REVALIDATION_REQUIRED` after relevant environment changes.
7. Unknown is not failure.
8. Static PASS is not Runtime PASS.
9. Regression is required before `DONE` for material changes.
10. Verified subsystems may be frozen as protected contracts.

## System prompt

Primary system prompt: **VIC3 Forge — Systems & Mechanics Engineering Copilot**.

Current candidate: `prompts/system/vic3-forge/v0.2-rc1.md`

## ChatGPT Skill

Primary skill: **VIC3 Forge Engineering**.

Source: `skills/vic3-forge-engineering/`

The skill uses the connected GitHub repository as a live control plane. For substantive tasks it resolves the current prompt, target mod manifest, Engineering State, evidence, Active Gate, and exact source files before design or implementation.

## Active mod workspace

`mods/cheat-menu-pro/` is the normalized workspace for the imported Cheat Menu Pro development line.

The historical Workshop-shaped snapshot remains under `mods/Bilds/` only as legacy provenance. New development must not create projects there.

See `THIRD_PARTY_NOTICES.md` before redistributing or relicensing third-party upstream material.

## Mod workspace contract

Each normalized mod should contain:

- `README.md`
- `MANIFEST.yml`
- `ROADMAP.md`
- `CHANGELOG.md`
- `engineering/`
- `tests/`
- `mod/` — deployable project-owned Victoria 3 mod/overlay root
- `releases/` when release artifacts are produced

The `mod/` directory mirrors only the Victoria 3 paths required by that project.

## Validation

Static validators may run in GitHub Actions. Runtime Victoria 3 behavior remains a separate evidence class and must not be inferred from CI alone.

## Status

Repository bootstrap: **ACTIVE**

Primary prompt: **VIC3 Forge v0.2 RC1**

Primary skill: **VIC3 Forge Engineering — release candidate**

Game-version compatibility is tracked per project and must never be assumed globally.
