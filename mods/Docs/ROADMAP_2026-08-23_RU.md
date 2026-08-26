# Cheat Menu Pro — Roadmap v12 / Post-beta18 Military Operations

**Дата:** 23.08.2026  
**Статус:** beta18 Final RELEASED / Runtime PASS; **beta18.1-pre1 Military Operations Discovery current**.

## 1. beta18 Final — Navy Rework — FROZEN

Любой post-Final build обязан проходить semantic freeze Navy. Новые Operations/Army/Technology изменения не должны менять принятый Navy gameplay surface без отдельного bugfix gate.

## 2. beta18.1-pre1 — Military Operations Discovery

Без gameplay writes.

Discovery map:

- exact Army formation context;
- Marine unit coverage;
- country `total_marine_capacity`;
- exact Fleet readiness;
- Supply diagnostics;
- invasion scope (`invasion_has_marines`, `is_naval_invasion`);
- native invasion UI bridge;
- unsupported/deferred auto-attach / auto-invasion.

## 3. beta18.1-pre2 — Amphibious Readiness Assistant

Только после pre1 discovery PASS:

- exact Army + exact Fleet selection;
- Marine count/capacity diagnostics;
- Fleet battle/range/supply readiness;
- понятные причины NOT READY;
- target/invasion diagnostics только при доказанном scope;
- native/manual invasion bridge;
- no fake auto-attach.

## 4. beta18.1-RC / Final — Military Operations

- runtime regression Army/Fleet readiness;
- +1 day / save-load;
- Workspace 90/100/115/130;
- no hidden fallback;
- freeze accepted Operations surface.

## 5. Army Rework 2.0

Navy architecture becomes the reference:

- multi-unit composer → one Army;
- exact Army context;
- tactical role profiles;
- Expert modifier controls;
- universal Marine coverage after combat-unit discovery.

## 6. Далее

1. beta19 Technology 2.0;
2. beta20 Special & Quick;
3. Economy / Markets / Regions Rework;
4. Vanilla CMP Rework.
