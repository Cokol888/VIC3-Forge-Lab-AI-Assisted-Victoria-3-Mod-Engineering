# QA Summary — beta18-pre5.1 Retrofit & Naval Logistics

**Build ID:** `CMP-0.3-B18-PRE5-1-20260822`  
**Версия:** `0.3-beta18-pre5.1`  
**Static status:** PASS  
**Runtime:** UNVERIFIED

## Реализованный contract

- Retrofit: native bridge only;
- прямые ShipTemplate/Retrofit writes CMP: 0;
- national Supply Ship write: `add_supply_ships`;
- количества: `+1 / +10 / +50 / +100`;
- formation Supply diagnostic: `num_assigned_supply_ships`;
- direct formation Supply assignment: DEFERRED;
- Amphibious Assistant: перенесён за beta18 Final.

## Статический QA

Итог `QA_REPORT.json`:

- status: **PASS**;
- errors: **0**;
- warnings: **0**;
- brace-checked GUI/common/event files: **130**;
- unique GUI → ScriptedGui refs: **11 361**, missing 0;
- CMP ScriptedGui → effect refs: **940**, missing 0;
- nested CMP effect refs: **1 276**, missing 0;
- duplicate `cmp_*` definitions: **0**;
- duplicate CMP localization keys: **0**;
- four Workspace profiles: PASS;
- Registry Coverage: PASS;
- Regions Operations regression: PASS;
- Army Final regression: PASS;
- UI/accessibility: PASS / 0 errors / 0 warnings;
- Navy18 validator: PASS.

## Navy regression metrics

- combat hulls: 25;
- Catalog create routes: 100;
- Fleet Composer 2.0: 5 rows / 125 hull choices;
- Composer anchor branches: 500;
- static non-anchor `create_ship` payloads: 2 375;
- Exact Ship slots: 100;
- flagship: pre4 Runtime PASS baseline;
- transfer: candidate runtime verify;
- transfer basket max: 20.

## pre5.1 safety assertions

- `add_supply_ships` write sites изолированы в dedicated logistics effects;
- четыре разрешённых amount-effects и только они;
- `num_assigned_supply_ships` используется read-only;
- CMP не вызывает `RetrofitShips` напрямую;
- CMP не изобретает `set_ship_template`;
- Supply Ships не выдаются за обычный combat-hull Fleet composition;
- native Fleet panel bridge сохранён.

## Release gate

Static PASS не повышает build до Navy RC1. Необходим runtime checklist, включая transfer regression pre5.

## Package verification

Release ZIP был распакован в отдельное чистое дерево и побайтово сравнивался с release-tree. Критерий выпуска: `missing = 0`, `extra = 0`, `changed = 0`. После распаковки повторно выполняются deterministic codegen checks, Navy/Registry/Regions/Army/UI validators и полный `validate_release.py`.
