# Active Gate — beta18.1-pre1.1 Army Scope Runtime

## Question

Does the exact Army observer/probe path operate correctly at runtime without stale/ghost selection and without changing frozen Navy behavior?

## Evidence required

Runtime observations for the imported build on Victoria 3 `1.13.10` / checksum `2964`.

## Required scenarios

1. No selected Army -> WAIT state.
2. Select Army A -> exact name + ROOT PASS + ARMY PASS.
3. Open Army -> same Army A native panel.
4. Select Army B -> context changes to Army B with no stale Army A state.
5. Select Fleet -> must not be interpreted as Army.
6. Clear military selection -> WAIT state returns.
7. Foreign/ineligible formation where selectable -> owner probe must not report player-owned PASS.
8. `+1 day` smoke.
9. Save/load smoke.
10. Frozen Navy regression smoke.

## PASS condition

All critical Army A/B, negative-state, persistence, and frozen-Navy checks pass with no relevant new runtime error.

## FAIL condition

Any stale exact-object context, false owner classification, wrong selected formation, persistence defect, or Navy regression attributable to `pre1.1`.

## Current status

`RUNTIME_PENDING`

No additional feature work is required to evaluate this gate.
