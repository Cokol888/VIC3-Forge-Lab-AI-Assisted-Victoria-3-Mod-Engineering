# QA Summary — beta18-pre3 Fleet Composer 2.0

**Build:** `CMP-0.3-B18-PRE3-20260821`  
**Parent:** beta18-pre2.4 Fleet Scope Proof / Runtime PASS target-core baseline  
**Статус:** STATIC PASS / RUNTIME UNVERIFIED

## Механический контракт

- Full Naval Catalog: **25 combat hulls** — 20 vanilla + 5 Tech & Res.
- Fleet Composer 2.0: **5 независимых строк**.
- Hull choices: 25 на каждую строку, **125 row/hull selection routes**.
- Amounts: `0 / 1 / 3 / 5 / 10`.
- Duplicate hull rows: **ALLOWED**; ожидаемый runtime-результат — additive.
- Bounded anchor branches: **500** (`5 × 25 × 4`).
- Static non-anchor `create_ship` payloads: **2 375**.
- Exact new-fleet scope: `save_temporary_scope_as = cmp_navy18_comp2_new_fleet`.
- Existing Fleet Target Core: **beta18-pre2.4 Runtime PASS baseline**.
- Direct ShipTemplate writes: **0**.
- Transfer / flagship / supply writes: **0**.

## Full release static QA

`validate_release.py` завершён со статусом **PASS**:

- errors: **0**;
- warnings: **0**;
- GUI/common/event brace files: **124**, failures 0;
- unique GUI → ScriptedGui refs: **11 053**, missing 0;
- CMP ScriptedGui → effect refs: **828**, missing 0;
- nested CMP effect → effect refs: **1 161**, missing 0;
- duplicate `cmp_*` definitions: **0**;
- duplicate CMP localization keys: **0**;
- Navy18 validator: **PASS**;
- UI/accessibility validator: **PASS / 0 errors / 0 warnings**;
- Registry Coverage: PASS;
- Regions Operations regression: PASS;
- Army Final regression: PASS;
- deterministic build/navy/catalog/registry/workspace codegen: PASS;
- Workspace profiles: **90 / 100 / 115 / 130**.

## Что Static PASS не доказывает

Главный новый runtime-риск — гибридная схема создания одного флота:

`anchor create_military_formation → temporary exact new-fleet scope → create_ship для остальных строк`.

До runtime нельзя считать доказанными:

- попадание всех non-anchor rows именно в новый anchor fleet;
- аддитивное поведение duplicate hull rows;
- сохранение состава после +1 дня и save/load;
- фактический layout пяти строк и 25-hull picker на всех UI profiles.

Runtime checklist: `docs/BETA18_PRE3_RUNTIME_CHECKLIST_RU.md`.
