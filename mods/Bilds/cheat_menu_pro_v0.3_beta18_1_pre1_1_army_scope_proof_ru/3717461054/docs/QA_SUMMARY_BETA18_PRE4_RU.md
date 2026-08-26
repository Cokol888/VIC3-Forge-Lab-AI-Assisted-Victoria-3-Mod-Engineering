# QA Summary — beta18-pre4 Exact Ship Control & Flagship

**Build:** `CMP-0.3-B18-PRE4-20260822`  
**Parent Runtime:** beta18-pre3 PASS  
**Static:** PASS  
**Runtime:** UNVERIFIED

## Exact Ship contract

- combat hulls: **25**;
- exact ship slots: **100**;
- pages: **5 × 20**;
- selector: `ordered_scope_ship`;
- filter: non-destroyed ships (`hit_points > 0`);
- ordering: `power_projection`;
- exact marker: `cmp_navy18_exact_ship_target` on `ship` scope;
- Ship Type probes: **25/25**;
- diagnostics: flagship / damage / port / battle / HP band / crew band;
- `set_as_flagship = yes`: **1 isolated write**;
- `set_as_flagship = no`: **1 isolated write**;
- ownership transfer writes in pre4 ship-control module: **0**;
- destructive ship writes: **0**;
- supply writes: **0**.

## Regression baseline

- beta18-pre2.4 exact Fleet context: Runtime PASS baseline retained;
- beta18-pre3 Fleet Composer 2.0: Runtime PASS baseline retained;
- full naval catalog: 25 hulls / 100 bounded instant-create endpoints;
- Army Final / Regions / Registry Coverage: PASS.

## Full release QA

- `validate_release.py`: **PASS / 0 errors / 0 warnings**;
- brace-checked GUI/common/event files: **126**;
- unique GUI → ScriptedGui refs: **11 302**, missing 0;
- CMP ScriptedGui → effect refs: **931**, missing 0;
- nested CMP effect refs: **1 265**, missing 0;
- duplicate `cmp_*` definitions: **0**;
- duplicate CMP localization keys: **0**;
- Navy18 validator: PASS;
- UI/accessibility: PASS;
- deterministic Build / Navy / Catalog / Ship Control / Registry / Workspace codegen: PASS.

Static PASS не заменяет runtime. Главный beta18-pre4 gate — доказать, что позиционный selector отличает отдельные Ship objects одного типа и `set_as_flagship` применяется только к exact selected Ship.
