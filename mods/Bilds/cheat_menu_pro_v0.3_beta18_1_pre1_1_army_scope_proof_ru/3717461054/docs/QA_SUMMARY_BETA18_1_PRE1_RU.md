# QA Summary — beta18.1-pre1 Military Operations Discovery

**Build:** `CMP-0.3-B18-1-PRE1-20260823`  
**Parent:** beta18 Final  
**Статус:** STATIC PASS / DISCOVERY ONLY  
**Gameplay additions:** 0  
**Workspace additions:** 0

## Discovery surface

- 11 capability records in `registry/military_operations.json`;
- `total_marine_capacity` classified as SUPPORTED_READ_ONLY;
- `invasion_has_marines` and `is_naval_invasion` classified as SUPPORTED_READ_ONLY_NEEDS_INVASION_SCOPE;
- exact Fleet context and assigned-supply diagnostics reuse beta18 Runtime PASS foundations;
- native invasion UI bridge remains DISCOVERY_REQUIRED;
- direct auto-attach Marines and direct start Naval Invasion remain DEFERRED_UNCONFIRMED.

## Freeze gates

- beta18 Final Navy semantic freeze: PASS;
- semantic freeze files: 15, mismatches 0;
- raw frozen data files: 3, mismatches 0;
- legacy Amphibious Builder files frozen: 2;
- new Military Operations gameplay effects: 0;
- new Military Operations ScriptedGui: 0;
- Workspace changes: 0.

## Project regressions

- Build Identity: PASS;
- Registry Coverage: PASS;
- Regions Operations: PASS;
- Army Final: PASS;
- Navy Final freeze: PASS;
- UI/accessibility: PASS;
- full `validate_release.py`: PASS / 0 errors;
- GUI → ScriptedGui refs: 11 360;
- brace-checked GUI/common/event files: 130.

## Promotion gate

`beta18.1-pre2` допускается только после отдельного discovery exact Army/Marine context и native/manual invasion UI route. pre1 не является Amphibious Assistant feature build.
