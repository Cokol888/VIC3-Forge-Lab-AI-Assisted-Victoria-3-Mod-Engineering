# QA Summary — Cheat Menu Pro v0.3 beta17-pre3.1

## Статус

**STATIC PASS — 0 ошибок, 0 предупреждений.**

Build ID: `CMP-0.3-B17-PRE3-1-20260820`  
Версия: `0.3-beta17-pre3.1`  
Baseline: `Victoria 3 1.13.*`  
Runtime: **PASS — подтверждено пользователем 20.08.2026**

## Regions Operations

- Operation buildings: **92** = 55 vanilla + 37 Tech & Res.
- Categories: 8, taxonomy синхронизирована со Staffing.
- Resource-capable building selectors: **19**.
- Generated ADD amounts: **1 / 5 / 10 / 15 / 20 / 25 / 50 / 100**.
- Availability gate: `can_construct_building` + `can_queue_building_levels = 1`.
- SET contract: raise/equal only; lowering blocked as `UNSAFE`; destructive recreate отсутствует.
- REMOVE contract: whole building type only.
- Preset component isolation: PASS:
  - Industrial Core: 6/6 guard resets;
  - Heavy Industry: 6/6;
  - Military Industry: 6/6;
  - Infrastructure Hub: 4/4.
- Operations/Staffing selection variables do not overlap.

## Full release QA

- Brace-checked GUI/common/event files: **120**, failures 0.
- Unique GUI → ScriptedGui refs: **10 551**, missing 0.
- CMP ScriptedGui → effect refs: **550**, missing 0.
- Nested CMP scripted-effect refs: **881**, missing 0.
- Duplicate `cmp_*` definitions: **0**.
- Visible Workspace localization keys: **413**, missing 0.
- Active RU/EN localization files: **40**, BOM/header errors 0.
- Workspace profiles 90/100/115/130: parity PASS.
- Minimum Workspace font: 12 pt.
- Accessibility validator: PASS, 0 errors / 0 warnings.

## Coverage / Diagnostics inherited from pre3

- Staffing inventory: 132 classified objects.
- Staffing SUPPORTED: 97; MANUAL: 5; UNSUPPORTED: 30.
- Staffing profiles: 14.
- Building Operations coverage: 92 SUPPORTED, full 132-object inventory classified.
- Universal statuses: `SUPPORTED / READ_ONLY / MANUAL / UNSAFE / UNSUPPORTED`.
- Military metrics: 267 registered/reused; 253 audited Workspace SGUI refs; 123 executable Workspace actions; old 239 metric deprecated.
- Fleet Selector Click Hotfix contract inherited; beta17-pre3.1 accepted by user in runtime on 20.08.2026.

## Regression fix discovered during audit

The previous preset implementation reused `cmp_regions2_state_blocked` across all components of a preset in one state. If the first/earlier component hit a cap or could not be constructed, later components were skipped even when valid. beta17-pre3.1 resets this local guard before every preset component while preserving aggregate root result flags.

The previous generator also did not guarantee helper definitions for preset-only deltas 15 and 20. They are now part of deterministic codegen and nested effect-reference validation.

## Runtime gate — accepted

- exact fleet selector inherited from pre2.1;
- government/public building operations;
- capped resource building;
- inland Port negative case;
- ADD partial result;
- SET up/equal/down;
- whole-building REMOVE;
- all four presets with mixed availability;
- result footer;
- +1 day and save/load.

Runtime acceptance was confirmed by the user on 20.08.2026; the static report remains the reproducible structural evidence.
