# Cheat Menu Pro — Roadmap v13 / Military Operations Scope Proof

**Дата:** 23.08.2026  
**Статус:** beta18 Final RELEASED / Runtime PASS; **beta18.1-pre1.1 Army Scope Proof — STATIC PASS / RUNTIME PENDING**.

## 1. beta18 Final — Navy Rework — FROZEN

Принятый Navy gameplay surface не меняется. Post-Final builds используют гранулярный semantic freeze: frozen Navy SGUI/effects/data + 28 accepted Navy/Fleet Workspace blocks.

## 2. beta18.1-pre1 — Military Operations Discovery — STATIC PASS

Подтверждены базовые read-only элементы:

- country `total_marine_capacity`;
- invasion `invasion_has_marines`;
- invasion `is_naval_invasion`;
- exact Fleet foundation;
- Fleet supply/battle/range diagnostics;
- необходимость отдельного Army/Marine/Invasion discovery.

## 3. beta18.1-pre1.1 — Army Scope Proof — CURRENT

Реализовано без gameplay writes:

- native-selected Army observer;
- exact `MilitaryFormation` name;
- `MilitaryFormation.MakeScope` root probe;
- `is_army + owner` probe;
- native panel reopen bridge;
- no Army marker;
- no guessed Army-list accessor.

Runtime gate:

- Army A / Army B exactness;
- root/owner probes;
- Fleet negative state;
- +1 day / save-load;
- Workspace 90/100/115/130;
- Navy smoke regression.

## 4. beta18.1-pre1.2 — Marine + Invasion Scope Discovery

Только после pre1.1 Runtime PASS:

- доказать self-contained Army list accessor либо оставить native-selection contract;
- доказать traversal/classification/count Marines в exact Army;
- доказать exact Invasion scope/selector;
- найти callable native invasion bridge либо окончательно закрепить MANUAL/NATIVE route;
- определить readiness metrics, которые можно читать без gameplay writes.

## 5. beta18.1-pre2 — Amphibious Readiness Assistant

Только после discovery gates:

- exact Army + exact Fleet context;
- Marine count/capacity diagnostics;
- Fleet battle/range/supply readiness;
- явные причины `READY / NOT READY / UNKNOWN`;
- invasion diagnostics только при доказанном scope;
- native/manual invasion route;
- no fake auto-attach.

## 6. beta18.1-RC / Final — Military Operations

- полный runtime regression;
- +1 day / save-load;
- Workspace 90/100/115/130;
- no hidden fallback / no ghost target;
- freeze принятого Operations surface.

## 7. Army Rework 2.0

Navy architecture остаётся референсом:

- multi-unit composer → one Army;
- exact Army context;
- tactical role profiles;
- Expert modifier controls;
- universal Marine coverage только после combat-unit discovery.

## 8. Далее

1. beta19 Technology 2.0;
2. beta20 Special & Quick;
3. Economy / Markets / Regions Rework;
4. Vanilla CMP Rework.
