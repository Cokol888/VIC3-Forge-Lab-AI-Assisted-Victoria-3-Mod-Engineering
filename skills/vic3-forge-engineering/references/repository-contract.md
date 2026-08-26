# Repository Contract

## Canonical repository

`Cokol888/VIC3-Forge-Lab-AI-Assisted-Victoria-3-Mod-Engineering`

## Bootstrap paths

- Human catalog: `CATALOG.md`
- Prompt catalog: `catalog/prompts.yml`
- Mod catalog: `catalog/mods.yml`
- Compatibility catalog: `catalog/compatibility.yml`
- Release catalog: `catalog/releases.yml`
- Current VIC3 Forge pointer: `prompts/system/vic3-forge/current.md`
- Current prompt composition: `prompts/system/vic3-forge/v0.2-rc1.md` unless `current.md` changes
- Third-party boundary: `THIRD_PARTY_NOTICES.md`

## Normalized mod workspace

Resolve mod IDs through `catalog/mods.yml`.

Expected files:

- `mods/<mod-id>/README.md`
- `mods/<mod-id>/MANIFEST.yml`
- `mods/<mod-id>/ROADMAP.md`
- `mods/<mod-id>/CHANGELOG.md`
- `mods/<mod-id>/engineering/STATE.md`
- `mods/<mod-id>/engineering/DECISIONS.md`
- `mods/<mod-id>/engineering/EVIDENCE.md`
- `mods/<mod-id>/engineering/gates/`
- `mods/<mod-id>/tests/`
- `mods/<mod-id>/mod/`

## Cheat Menu Pro special case

Normalized workspace: `mods/cheat-menu-pro/`

Legacy provenance snapshot:
`mods/Bilds/cheat_menu_pro_v0.3_beta18_1_pre1_1_army_scope_proof_ru/3717461054/`

Do not use `mods/Bilds/` for new project structure.

Legacy high-value evidence includes:

- `baseline_manifest.json`
- `registry/build.json`
- `MECHANICS_AUDIT.md`
- `QA_REPORT.json`
- `docs/`
- `registry/`
- `tools/`

Fetch individual legacy files only when a normalized workspace record points to them or the technical question requires them.

## Progressive loading

### Status / continuation
Load:
1. `catalog/mods.yml`
2. mod `MANIFEST.yml`
3. mod `engineering/STATE.md`
4. active gate
5. `ROADMAP.md` only if sequencing is relevant

### Technical claim / research
Additionally load:
- `engineering/EVIDENCE.md`
- exact registry/docs/source supporting the claim

### Implementation
Additionally load:
- exact target source file
- generator/source-of-truth file when generated output is involved
- relevant validator
- decisions/frozen contract affected by the change

### Prompt architecture
Load:
1. `catalog/prompts.yml`
2. `prompts/system/vic3-forge/current.md`
3. current prompt index
4. only relevant component files

Avoid bulk-loading multi-megabyte GUI/generated files unless targeted inspection is necessary.
