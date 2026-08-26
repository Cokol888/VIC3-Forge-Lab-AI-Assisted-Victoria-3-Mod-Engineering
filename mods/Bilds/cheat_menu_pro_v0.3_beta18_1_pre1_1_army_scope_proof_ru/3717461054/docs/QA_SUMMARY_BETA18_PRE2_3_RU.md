# QA Summary — beta18-pre2.3 Native Fleet Selection & Direct Operations Core

**Build ID:** `CMP-0.3-B18-PRE2-3-20260821`  
**Static status:** PASS  
**Runtime status:** UNVERIFIED

## Native Fleet Target contract

- selector action: `FormationPanel.SelectFormation(MilitaryFormation.Self)`;
- source of truth: `GetSelectedFormation`;
- production operation root: выбранный `MilitaryFormation.MakeScope`;
- production Workspace references to `cmp_military_target_fleet_select / entry_selected / clear`: **0**;
- `cmp_fleet_builder_apply_native`: `scope = military_formation`;
- native create target: `fleet = scope:cmp_fleet_builder_native_target`;
- production effect contains legacy marker/resolver scan: **0**;
- legacy marker/resolver source is retained as fallback only;
- empty owned Fleet: supported runtime candidate;
- Fleet with any existing Ship in battle: add-ships blocked.

## Full static release QA

- release validator: **PASS, 0 errors**;
- GUI/common/event brace files: **124**, failures **0**;
- unique GUI → ScriptedGui refs: **10 828**, missing **0**;
- CMP ScriptedGui → effect refs: **718**, missing **0**;
- nested CMP effect refs: **1 051**, missing **0**;
- duplicate `cmp_*` definitions: **0**;
- duplicate CMP localization keys: **0**;
- Navy18 validator: **PASS**;
- Registry Coverage: **PASS**;
- Regions Operations: **PASS**;
- Army Final regression: **PASS**;
- UI/accessibility: **PASS, 0 errors / 0 warnings**;
- Workspace profiles: 90 / 100 / 115 / 130 static parity PASS.

## Сохранившаяся Navy-функциональность

- combat hulls: **25** — 20 vanilla + 5 Tech & Res;
- new-fleet catalog endpoints: **100**;
- universal composer groups: 9 Capital / 10 Cruiser / 6 Torpedo;
- mixed composer branches: **37 924**;
- Selected Fleet hull choices: **25**;
- native Ship Designer bridge сохранён;
- transfer / exact Ship / flagship / supply writes не открыты.

Static PASS не заменяет runtime gate. Обязательный A/B exact-target тест описан в `docs/BETA18_PRE2_3_RUNTIME_CHECKLIST_RU.md`.
