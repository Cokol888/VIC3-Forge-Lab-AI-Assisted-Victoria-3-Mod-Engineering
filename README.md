# VIC3 Forge Lab

**AI-Assisted Victoria 3 Mod Engineering**

VIC3 Forge Lab is a reproducible engineering workspace for developing Victoria 3 mods with AI-assisted system prompts, evidence-driven workflows, runtime validation, regression testing, and traceable releases.

## Core workflow

`system prompt -> engineering state -> evidence -> implementation -> runtime test -> regression -> release`

The repository is designed to keep AI reasoning artifacts, prompt versions, mod source code, test evidence, and release state clearly separated.

## Repository map

- `prompts/` — versioned VIC3 Forge system prompts, component prompts, operator commands, templates, and eval scenarios.
- `mods/` — one isolated engineering workspace per Victoria 3 mod.
- `catalog/` — machine-readable indexes for prompts, mods, compatibility, and releases.
- `research/` — reusable research on game versions, script APIs, vanilla patterns, compatibility, and experiments.
- `references/` — local/reference metadata. Full base-game assets must not be committed.
- `tooling/` — validators, packaging helpers, diff tooling, and scripts.
- `docs/` — architecture, methodology, workflows, conventions, prompt engineering, and mod engineering documentation.
- `archive/` — retired prompts, mods, and experiments.

See [`CATALOG.md`](CATALOG.md) for the human-readable project index.

## Engineering principles

1. Files before assumptions.
2. Target version before latest version.
3. Evidence before claims.
4. Fact, decision, plan, and hypothesis are distinct states.
5. One active gate and one next milestone; the rest stays queued.
6. Version-sensitive evidence expires into `REVALIDATION_REQUIRED` after relevant environment changes.
7. Unknown is not failure.
8. Runtime verification is required before claiming runtime success.
9. Regression is required before `DONE` for material changes.
10. Verified subsystems may be frozen as protected contracts.

## Prompt lineage

The primary system prompt is **VIC3 Forge — Systems & Mechanics Engineering Copilot**.

Current candidate: `prompts/system/vic3-forge/v0.2-rc1.md`

## Mod workspace contract

Each mod should contain:

- `README.md`
- `MANIFEST.yml`
- `ROADMAP.md`
- `CHANGELOG.md`
- `engineering/`
- `tests/`
- `mod/` — deployable Victoria 3 mod root only
- `releases/`

The `mod/` directory mirrors only the Victoria 3 paths required by that mod.

## Status

Repository bootstrap: **ACTIVE**

Primary prompt: **VIC3 Forge v0.2 RC1**

Game-version compatibility is tracked per project and must never be assumed globally.
