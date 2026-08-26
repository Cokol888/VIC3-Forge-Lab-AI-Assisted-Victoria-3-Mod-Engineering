---
name: vic3-forge-engineering
description: Use this skill for design, implementation, debugging, review, migration, QA, regression, balance analysis, or continuation of Victoria 3 mod work managed in the Cokol888/VIC3-Forge-Lab-AI-Assisted-Victoria-3-Mod-Engineering GitHub repository. It retrieves the live VIC3 Forge system prompt, mod manifest, Engineering State, evidence, Active Gate, roadmap, and relevant source files before substantive work, then keeps repository state and engineering claims synchronized. Use when the user references VIC3 Forge, VIC3 Forge Lab, Cheat Menu Pro, a mod/build/gate from this repository, or asks to continue/create Victoria 3 engineering work using the project's prompts and evidence discipline.
---

# VIC3 Forge Engineering

Use the GitHub repository as the live project control plane. Do not substitute remembered chat context for repository state when the repository can resolve the question.

Repository: `Cokol888/VIC3-Forge-Lab-AI-Assisted-Victoria-3-Mod-Engineering`
Default branch: `main`

## Core workflow

1. Resolve the task and target mod/build.
2. Load the minimum live repository context required for the task.
3. Apply the current VIC3 Forge system-prompt rules and the target mod's Engineering State.
4. Inspect exact source/evidence before proposing technical claims or changes.
5. Perform the requested analysis or repository change.
6. Validate claims at the correct evidence level.
7. Update project state files when the user's requested change materially changes state, evidence, roadmap, or implementation.
8. End with one Next Best Action unless the user explicitly asks for a broader roadmap.

Read `references/repository-contract.md` for repository paths and context-loading rules.
Read `references/engineering-workflow.md` for task routing, status discipline, gates, and validation.
Read `references/change-policy.md` before modifying repository content.

## Context bootstrap

For substantive work, use the connected GitHub tool and load context progressively.

Always start with:

- `CATALOG.md` or `catalog/mods.yml` to resolve the project;
- `prompts/system/vic3-forge/current.md` and the referenced current prompt version for VIC3 Forge behavior;
- the target mod's `MANIFEST.yml` and `engineering/STATE.md`.

Then load only what the task needs:

- active gate for runtime/debugging work;
- `engineering/EVIDENCE.md` for technical claims;
- `engineering/DECISIONS.md` for architectural constraints;
- `ROADMAP.md` for sequencing;
- exact source files for implementation/review;
- legacy evidence only when the normalized workspace points to it.

Do not load the entire repository or huge generated files by default. Fetch targeted ranges/files first.

## Source-of-truth discipline

Apply this precedence when repository data is available:

1. Exact current project files and runtime evidence.
2. Target mod `MANIFEST.yml` and Engineering State.
3. Current VIC3 Forge prompt.
4. Locked target-game/upstream evidence in the repository.
5. Official current external sources when repository evidence requires verification.
6. Inference or hypothesis.

Separate `FACT`, `OBSERVATION`, `DECISION`, `PLAN`, `ASSUMPTION`, `HYPOTHESIS`, `RESULT`, and `UNKNOWN`.

Never promote static success to runtime success. Never convert `UNKNOWN` into `FAIL` without evidence.

## Active Horizon

For ongoing engineering work, respect:

`ONE ACTIVE GATE + ONE NEXT MILESTONE + QUEUED ROADMAP`

Do not deeply design later milestones on top of an unresolved gate unless the user explicitly requests a full roadmap or architecture exercise.

## Version and evidence scope

Treat game version, checksum, modset, upstream snapshot, branch, and relevant dependency versions as environment-bound evidence.

When a relevant environment changes, mark dependent conclusions `REVALIDATION_REQUIRED`; do not erase their historical verification.

## Implementation behavior

Before editing source:

- inspect the exact current file;
- inspect related registry/generated-source contract when applicable;
- check frozen contracts and decisions;
- define the minimal causal change set;
- identify static/runtime/regression validation required.

Prefer project-owned normalized workspace paths. Do not create new work under `mods/Bilds/`.

Treat the legacy Workshop-shaped Cheat Menu Pro snapshot as provenance/upstream material. Read `THIRD_PARTY_NOTICES.md` and `mods/cheat-menu-pro/upstream/UPSTREAM.md` before any task that would copy, redistribute, relicense, or directly rewrite legacy upstream content.

## Repository writes

When the user asks to implement or update repository content, make the change rather than only describing it when GitHub write access is available.

Keep state synchronized when relevant:

- implementation/source change;
- `MANIFEST.yml` if build/environment/state changed;
- `engineering/STATE.md` if gate/status/known facts changed;
- `engineering/EVIDENCE.md` when new evidence is established;
- gate/test record when validation occurs;
- `CHANGELOG.md` for meaningful project changes;
- `catalog/mods.yml` only when catalog-level metadata changes.

Do not rewrite historical evidence to make current status look cleaner.

## Validation

Use repository validators and CI as static evidence when applicable. Do not claim that a GitHub Action or local validator proves Victoria 3 runtime behavior unless it actually runs the game and captures the required runtime evidence.

For a failed validation, classify the failure before changing multiple independent causes.

For investigation, prefer a test with high information gain, low blast radius, and good reversibility.

## Default response shape

For simple tasks, answer directly.

For substantial engineering work, prefer:

- **Current state** — only the relevant confirmed state.
- **Evidence / finding** — what supports the conclusion.
- **Change or decision** — what was done or should be done.
- **Validation status** — static/runtime/regression distinction.
- **Next Best Action** — one prioritized next step.

Do not dump the internal Engineering State unless the user asks for `/state`, a checkpoint, or a status report.

## Operator intents

Interpret these project-style commands when present:

- `/state` — show current live Engineering State.
- `/checkpoint` — produce a portable live-repository checkpoint.
- `/gate` — show Active Gate and PASS/FAIL evidence requirements.
- `/next` — return only the Next Best Action.
- `/roadmap` — show Active Gate, Next Milestone, then queued roadmap.
- `/evidence` — show critical evidence with provenance and environment.
- `/revalidate` — identify evidence requiring revalidation.
- `/qa` — switch to validation/review mode.
- `/regression` — build or inspect the bounded regression scope.

## Failure handling

If repository state conflicts with remembered conversation context, state the discrepancy and prefer the live repository unless the user explicitly supplies a newer uncommitted state.

If a required repository file is absent, do not invent it. Continue with safe analysis where possible and identify the missing contract.

If GitHub access is unavailable, say that live repository state could not be verified and downgrade repository-dependent claims accordingly.
