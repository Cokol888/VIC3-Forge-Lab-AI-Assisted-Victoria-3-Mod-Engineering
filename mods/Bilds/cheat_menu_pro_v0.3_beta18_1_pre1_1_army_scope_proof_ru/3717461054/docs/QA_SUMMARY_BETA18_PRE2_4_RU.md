# QA Summary — beta18-pre2.4 Fleet Scope Proof & Native Panel Bridge

Статус до runtime: **STATIC PASS / RUNTIME UNVERIFIED**.

## Изменения

- удалён `FormationPanel.SelectFormation(MilitaryFormation.Self)` из generated Workspace;
- row click заменён на vanilla `InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')`;
- root probe упрощён до `scope = military_formation + always = yes`;
- добавлен отдельный owner probe;
- `GetSelectedFormation` оставлен наблюдаемым, а не доказанным source of truth;
- `cmp_fleet_builder_apply_native` больше не дублирует GUI `IsFleet` через scripted trigger;
- custom persistent fleet marker в production Workspace не возвращён.

## Проверки

- Build ID: `CMP-0.3-B18-PRE2-4-20260821`;
- combat hulls: 25;
- catalog create endpoints: 100;
- universal composer branches: 37 924;
- Workspace profiles: 4;
- Navy validator: PASS;
- Registry Coverage: PASS;
- Regions Operations: PASS;
- Army Final regression: PASS;
- UI/accessibility: PASS, 0 errors / 0 warnings;
- full release validator: PASS, 0 errors;
- GUI/common/event brace files: 124;
- GUI -> ScriptedGui refs: 10 829, missing 0.

Runtime evidence remains mandatory.
