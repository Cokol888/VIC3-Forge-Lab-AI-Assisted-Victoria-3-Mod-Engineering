# QA Summary — beta18-pre2.2 Fleet Target Core Repair

**Build ID:** `CMP-0.3-B18-PRE2-2-20260821`  
**Parent:** beta18-pre2.1 Runtime FAIL по exact fleet selection  
**Runtime:** UNVERIFIED

## Изменения

- `cmp_military_target_fleet_select` переведён с country-root + `scope:formation` на `scope = military_formation`.
- Workspace вызывает selector через `GuiScope.SetRoot(MilitaryFormation.MakeScope).End`.
- `cmp_military_target_fleet_entry_selected` также работает непосредственно на formation-root.
- Очистка exact marker теперь ограничена formations текущей страны и не использует глобальный `every_country`.
- Сохранён совместимый legacy variable-list, но exact Fleet Builder resolver по-прежнему требует `cmp_military_target_fleet` и не имеет fallback на первый подходящий флот.
- В picker добавлены runtime probes: direct-root, callback received, exact marker written.

## Static QA

- Full release validator: PASS, 0 errors.
- 124 GUI/common/event files: brace gate PASS.
- 10 832 unique GUI→ScriptedGui references, missing 0.
- Registry / Regions / Army / Navy regression gates: PASS.
- UI/accessibility: PASS, 0 errors / 0 warnings.
- Workspace codegen and Build Identity: deterministic PASS.

## Runtime gate

Сборка не принимается как PASS до проверки жёлтого root-probe, callback, exact marker, смены цели, clear, exact add-ship и save/load.
