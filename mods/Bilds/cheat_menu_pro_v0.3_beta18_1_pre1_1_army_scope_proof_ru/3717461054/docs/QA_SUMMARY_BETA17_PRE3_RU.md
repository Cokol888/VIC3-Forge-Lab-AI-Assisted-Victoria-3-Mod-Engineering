# QA Summary — Cheat Menu Pro v0.3 beta17-pre3

## Статус

**STATIC PASS — 0 ошибок, 0 предупреждений.**

Сборка: `CMP-0.3-B17-PRE3-20260820`  
Версия: `0.3-beta17-pre3`  
Baseline: `1.13.*`  
Runtime: **UNVERIFIED**  
Fleet gate: `INHERITED_PRE2.1_RUNTIME_PENDING`

Эта запись подтверждает статическую целостность beta17-pre3. Она **не** заменяет игровой runtime-тест Fleet Selector Click Hotfix и нового Staffing Coverage 2.1.

## Основной release QA

- Brace-checked GUI/common files: **120**, failures: **0**.
- Unique GUI → ScriptedGui refs: **10345**, missing: **0**.
- CMP ScriptedGui → effect refs: **439**, missing: **0**.
- Duplicate `cmp_*` definitions: **0**.
- Workspace visible localization keys: **409**, missing: **0**.
- RU/EN localization files checked: **40**, header/BOM errors: **0**.
- Workspace profiles: **90 / 100 / 115 / 130**, minimum Workspace font: **12 pt**.
- Accessibility validator: **PASS**, errors: **0**, warnings: **0**.

## Staffing Coverage 2.1

- Classified candidates: **132**.
- `SUPPORTED`: **97**.
- `MANUAL`: **5**.
- `UNSUPPORTED`: **30**.
- Staffing profiles: **14**.
- Legacy B6 building selectors classified: **102**.
- Supported entries rendered in all four Workspace profiles: **97**.
- Staffing category counts: `{"primary": 35, "industry": 35, "infrastructure": 11, "public": 2, "military": 6, "services": 6, "ownership": 2}`.
- Operations registry remains **56** buildings; Staffing selection is independent.
- Adaptive targets remain **50 / 75 / 90 / 100%** plus Off.

`generate_staffing2.py --check`, `generate_regions2.py --check`, `generate_workspace_shell.py --check`, `generate_build_identity.py --check` and `validate_registry_coverage.py` all pass deterministically.

## Universal Coverage Contract

Allowed statuses validated exactly as:

`SUPPORTED / READ_ONLY / MANUAL / UNSAFE / UNSUPPORTED`

Objects omitted from the automatic route must now carry an explicit status/reason instead of silently disappearing from the registry.

## Build Identity

Source of truth: `registry/build.json`.

Synchronized into:

- `registry/ui_shell.json`;
- `integration_manifest.json`;
- RU/EN build localization;
- Workspace diagnostics;
- `QA_REPORT.json`.

The stale beta16 UI registry version tag is no longer present.

## Military metric normalization

- Registered/reused military endpoints: **267**.
- Audited unique Workspace ScriptedGui refs per generated military profile: **253**.
- Executable Workspace action endpoints per profile: **123**.
- Historical **239** metric: **deprecated** because its definition mixed reporting layers.

Military profile parity validator: **PASS**.

## Fleet regression gate

The beta17-pre2.1 click hotfix is preserved and still passes the static Military Target contract:

- persistent `Country.GetMilitaryFormationsFleet` picker remains present;
- `MilitaryFormation.GetNameNoFormatting` is used;
- exact `formation` scope handoff remains present;
- obsolete event picker does not leak back into Workspace;
- no silent first-eligible fleet fallback is allowed;
- picker row callback/self-close regression gate remains active.

**Runtime status remains UNVERIFIED until the user confirms the click-path in Victoria 3.**

## Search / Filter discovery

Native SearchBar is intentionally **DEFERRED** as a mandatory dependency. CMP still advertises the broader `1.13.*` baseline, while the native `SearchBar` / `SearchResult` surface is documented from 1.13.9. Current fallback remains category + scroll.

## Required runtime checklist

1. Fleet: click row → green exact-target state → close picker → exact fleet remains selected.
2. Fleet: change target, clear target, +1 day, save/load.
3. Staffing: verify one legacy industrial building.
4. Staffing: verify university/government building.
5. Staffing: verify military building.
6. Staffing: verify Manor House or Financial District.
7. Staffing: verify one Tech & Res building with provider active.
8. Verify Staffing selection does not change the ADD/SET/REMOVE building selection.
9. Verify Adaptive 50/90/100% and no action when selected building is absent from the target state.
10. Smoke Workspace profiles 90/100/115/130.

## Release conclusion

**beta17-pre3 is ready as a static test candidate.** Do not mark beta17 Final or runtime PASS until the inherited fleet gate and the new Staffing routes pass the in-game checklist.
