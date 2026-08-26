# Regions & Buildings 2.0 — current beta17-pre3.1 contract

Building ADD is now a guarded best-effort operation: every next level is checked with `can_construct_building` for absent buildings or `can_queue_building_levels = 1` for existing buildings. Caps/invalid placement stop that building in that state and produce blocked/partial feedback instead of silently overrunning limits.

Building SET no longer uses destructive remove → recreate. It raises when current < target, succeeds without mutation when equal, and blocks lowering as `UNSAFE` when current > target. REMOVE deletes the whole building type; the amount selector is not treated as a partial-remove count.

Operations expose 92 supported buildings and share the Staffing category taxonomy while using independent selector variables. Presets are ADD-only, execute per state, and reset the local blocked guard before every component so one invalid/capped component cannot cancel the rest of the preset.

Adaptive Staffing remains occupancy-gated and uses its separate staffing coverage registry.

Static validation:

```text
python3 tools/generate_regions2.py --check
python3 tools/validate_regions_operations.py
python3 tools/validate_registry_coverage.py
python3 tools/validate_release.py
```
