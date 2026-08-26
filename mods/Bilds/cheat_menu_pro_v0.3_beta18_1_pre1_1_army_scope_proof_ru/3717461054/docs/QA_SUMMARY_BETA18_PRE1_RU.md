# QA Summary — Cheat Menu Pro v0.3 beta18-pre1

## Статус

**STATIC PASS / RUNTIME UNVERIFIED**

Build ID: `CMP-0.3-B18-PRE1-20260820`  
Version: `0.3-beta18-pre1`  
Parent: `0.3-beta17-final` — пользователь принял beta17 как выпущенную; критических game-breaking runtime defects не выявлено.  
Baseline: Victoria 3 `1.13.*`

## Navy Architecture gate

- Verified Tech & Res ship types: **5**.
- Composition amounts: **0 / 1 / 3 / 5 / 10**.
- Independent ship-count selection endpoints: **25**.
- Non-zero composition matrix: **3 124 / 3 124** branches.
- Formation creation contract: **one create_military_formation per branch**.
- Composition presets: **5**.
- New-fleet existing-target fallback: **0**.
- Transfer writes exposed in pre1: **0**.
- Supply-ship writes exposed in pre1: **0**.
- Flagship writes exposed in pre1: **0**.
- Workspace profile parity: **4 / 4**.

## Full release QA

- Status: **PASS**.
- Errors: **0**.
- Warnings: **0**.
- Brace-checked GUI/common/event files: **122**.
- Unique GUI → ScriptedGui refs: **10 614**, missing **0**.
- CMP ScriptedGui → effect refs: **582**, missing **0**.
- Nested CMP effect → effect refs: **915**, missing **0**.
- Duplicate `cmp_*`: **0**.
- UI/accessibility: **PASS, 0 errors / 0 warnings**.
- Navy18 codegen: deterministic `--check` PASS.
- Workspace codegen: deterministic `--check` PASS.
- Build identity: synchronized.

## Provider contract

Pinned source: Workshop snapshot `3472248460` from `529340(1).zip`.

Validated source hashes are recorded in `registry/navy18.json` for:

- ship types;
- Tech & Res ship modifications;
- vanilla-extension ship modifications from the provider;
- ship modification slots.

## Known limitations

1. Full vanilla ship catalog is discovery-required and is not guessed in pre1.
2. Transfer remains beta18-pre3.
3. Amphibious automation remains manual/discovery; CMP does not claim a safe army-to-fleet attach effect.
4. Supply ships remain read-only/discovery until the minimum supported scripting surface is settled.
5. Flagship writes require exact ship selection and remain deferred.
6. SearchBar is not required while baseline remains broad `1.13.*`.

## Required runtime gate

- mixed fleet 2–5 types as one formation;
- port/no-port;
- open/closed technologies;
- five composition presets;
- existing exact-fleet add-ships regression;
- immediate / +1 day / save-load;
- profiles 90/100/115/130.
