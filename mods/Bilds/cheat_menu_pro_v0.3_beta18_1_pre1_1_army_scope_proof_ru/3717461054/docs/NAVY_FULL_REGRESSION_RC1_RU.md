# beta18-RC1 — Full Navy Regression

**Build ID:** `CMP-0.3-B18-RC1-20260822`  
**Версия:** `0.3-beta18-RC1`  
**Parent:** `beta18-pre5.1`  
**Статус:** STATIC PASS / RC1 RUNTIME REGRESSION PENDING

## Цель RC1

RC1 не вводит новые игровые механики. Это заморозка функциональности Navy Rework перед `beta18 Final` и полный регрессионный прогон уже реализованной цепочки:

`Ship Type → Ship Template/native workflow → Fleet Composer → exact Fleet → exact Ship → Flagship → Transfer → Retrofit bridge → Supply Ships`.

Пользователь подтвердил работу основных функций pre5/pre5.1; RC1 нужен для проверки edge-cases, взаимодействия модулей, +1 day, save/load и всех профилей Workspace.

## Замороженный production surface

### Fleet Composer 2.0

- 25 combat hulls;
- 5 независимых строк;
- количества `0 / 1 / 3 / 5 / 10`;
- duplicate hulls разрешены;
- все ненулевые строки создают один Fleet;
- instant creation использует default template Ship Type.

### Exact Fleet

- direct `MilitaryFormation` row context;
- native bridge `InformationPanelBar.OpenMilitaryFormationPanelTab`;
- production Workspace не использует старый `cmp_military_target_fleet` marker-resolver как source of truth.

### Exact Ship / Flagship

- 100 positional slots / 5 страниц;
- selection через `ordered_scope_ship`;
- exact marker хранится на `ship`;
- `set_as_flagship = yes/no` — единственная штатная exact-Ship операция pre4 кроме transfer-семейства.

### Transfers

- single: `set_ship_owner`;
- batch: `set_ship_owner_multiple`;
- до 20 exact Ships;
- batch может собираться из нескольких source Fleets;
- после batch вызывается `clear_ownership_transfer_fleet` на source country;
- dead / battle / flagship Ship блокируются;
- receiver должен быть другой страной с портом.

### Retrofit

CMP не выполняет fake direct ShipTemplate write. Production route остаётся native:

`Ship Designer → template → native Fleet panel → native ShipSelection → Change Template → Retrofit`.

`RetrofitShips`, `RetrofitShipsAndStation`, `CancelRetrofitShips` существуют в native UI surface Victoria 3, но CMP не связывает их напрямую со своим exact Ship marker без отдельного доказательства equivalence с `ShipSelection`.

### Naval Logistics

- Supply Ships — национальный reserve/resource;
- writes: `add_supply_ships +1/+10/+50/+100` на country scope;
- country diagnostic: `supply_ship_maintenance_fulfillment`;
- selected formation read-only diagnostic: `num_assigned_supply_ships`;
- direct assignment Supply Ships конкретному Fleet не реализуется без подтверждённого write contract.

## RC1 hardening

В RC1 дополнительно:

- убраны устаревшие пользовательские тексты `pre5 candidate`;
- Diagnostics больше не используют старый persistent Fleet marker как индикатор готовности;
- добавлен отдельный `tools/validate_beta18_rc1.py`;
- full release validator запускает RC1 validator как обязательный gate;
- `registry/navy18.json` содержит frozen RC1 regression matrix;
- gameplay additions в RC1: **0**.

## Не входит в RC1

- Amphibious Assistant;
- direct ShipTemplate write;
- direct Supply Ship assignment к formation;
- damage/kill/crew Ship actions;
- новые Fleet/Ship mechanics.

Amphibious Assistant остаётся post-beta18 задачей Military Operations Rework.

## Условие beta18 Final

`beta18 Final` выпускается только после runtime PASS полного RC1 checklist: Composer, exact Fleet, add-ships, exact Ship, flagship, single/batch/cross-Fleet transfer, retrofit bridge, Supply reserve/diagnostics, battle/damaged/destroyed states, +1 day, save/load и Workspace 90/100/115/130.
