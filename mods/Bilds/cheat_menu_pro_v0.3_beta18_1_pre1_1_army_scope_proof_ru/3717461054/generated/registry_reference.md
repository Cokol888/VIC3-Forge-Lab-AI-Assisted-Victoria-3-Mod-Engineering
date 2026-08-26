# CMP beta11 — Registry / Code Generation

Beta11 introduces a declarative data layer before the next CMP refactoring stages.

- Providers: **3**
- Staffing Assistant buildings: **92**
- Land unit types: **26**
- Ship types: **25**
- Tech & Res resources: **8**
- Registered operations: **11**

## Production codegen path

`cmp_fleet_builder_sgui.txt`, `cmp_fleet_builder_effects.txt`, provider-detection adapters and the Fleet Builder ship selector in `sakuya_main.gui` are generated from the JSON registries.

This is the first production codegen path. Beta12 can consume the same registries for Regions/Buildings/Resources/Staffing.
