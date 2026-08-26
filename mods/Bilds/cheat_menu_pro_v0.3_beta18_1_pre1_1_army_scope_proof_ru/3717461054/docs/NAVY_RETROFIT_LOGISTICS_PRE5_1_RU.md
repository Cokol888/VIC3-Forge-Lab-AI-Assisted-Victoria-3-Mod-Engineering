# beta18-pre5.1 — Retrofit & Naval Logistics

**Build ID:** `CMP-0.3-B18-PRE5-1-20260822`  
**Версия:** `0.3-beta18-pre5.1`  
**Runtime:** `UNVERIFIED`  
**Parent:** `beta18-pre5 Exact Ship Transfers` — transfer runtime gate всё ещё требует отдельного подтверждения.

## 1. Цель этапа

pre5.1 закрывает два последних обязательных функциональных блока перед Navy RC1:

1. безопасную интеграцию с пользовательскими Ship Templates / Retrofit;
2. корректную модель Supply Ships как государственного логистического ресурса.

Amphibious Assistant сознательно перенесён за beta18 Final: он относится уже к применению флота в военных операциях, а не к базовому управлению Navy.

## 2. Retrofit — только native bridge

Victoria 3 1.13 имеет отдельные data types `ShipTemplate`, `ShipTemplateList`, `ShipSelection`, `ShipConstructionQueue` и штатные UI-команды `RetrofitShips`, `RetrofitShipsAndStation`, `CancelRetrofitShips`.

Однако наличие нативной команды не доказывает, что exact Ship marker CMP автоматически является тем же объектом, что и внутренний `ShipSelection` штатного интерфейса. Поэтому pre5.1 не вызывает `RetrofitShips` напрямую и не изобретает `set_ship_template` effect.

Производственный маршрут CMP:

`Ship Designer`  
→ создать / изменить пользовательский шаблон  
→ выбрать Fleet  
→ открыть штатную карточку Fleet  
→ выбрать нужные Ships в штатном списке  
→ `Change Template`  
→ `Retrofit`.

CMP предоставляет две bridge-кнопки:

- **Открыть конструктор кораблей** — `PopupManager.ToggleShipDesignerPopup`;
- **Открыть штатную карточку флота** — `InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')` для текущей selected formation.

Таким образом пользователь получает единый маршрут из CMP, но template-selection и retrofit остаются source of truth Victoria 3.

## 3. Supply Ships — национальный резерв, не Fleet composition

Публичный scripting contract 1.13 определяет `add_supply_ships` как country-effect: он добавляет Supply Ships державе. Vanilla history использует этот же effect для стартового резерва стран с флотом.

Поэтому в CMP нельзя называть действие `+10 судов этому флоту`. pre5.1 вводит отдельный блок:

**Государственный резерв судов снабжения**

с безопасными действиями:

- `+1`;
- `+10`;
- `+50`;
- `+100`.

Каждая кнопка выполняется на `country` scope и использует только `add_supply_ships = { value = N }`.

В pre5.1 не добавляется отрицательное значение и не реализуется SET, потому что отдельный remove/set effect не подтверждён.

## 4. Обеспечение логистики

На country scope используется документированный trigger `supply_ship_maintenance_fulfillment`.

CMP показывает диапазоны:

- высокий уровень — 75%+;
- средний — 25–74%;
- низкий — ниже 25%.

Это диагностический сигнал обеспечения национального Supply Ship pool, а не ручная подмена штатной логистики.

## 5. Сколько Supply Ships назначено выбранному формированию

Victoria 3 1.13.9 предоставляет event target/value `num_assigned_supply_ships` для `military_formation`.

CMP использует его только для чтения и показывает диапазон:

`0 / 1 / 2 / 3 / 4 / 5 / 6–10 / 11–20 / 21–50 / 51+`.

Прямое назначение Supply Ships конкретной formation имеет статус **DEFERRED / UNCONFIRMED**. Ни одна write-команда для этого не выдумывается.

## 6. Что остаётся от pre5

Exact Ship Transfers полностью сохранены как regression surface:

- single `set_ship_owner`;
- batch `set_ship_owner_multiple`;
- `clear_ownership_transfer_fleet` на source country;
- basket до 20 exact Ships;
- battle / flagship / destroyed safety gates.

Но pre5 runtime transfer gate ещё должен быть подтверждён пользователем отдельно. pre5.1 не повышает его статус автоматически.

## 7. Что намеренно не добавлено

- direct `RetrofitShips` из CMP exact Ship selector;
- direct `set ShipTemplate`;
- direct Supply Ship assignment к Fleet;
- уменьшение/SET национального Supply Ship reserve;
- amphibious autopilot;
- auto-attach Fleet ↔ Marines.

Каждый из этих пунктов требует отдельного доказанного engine contract.

## 8. Критерий продвижения в RC1

RC1 разрешён только если runtime подтверждает одновременно:

- pre5 single/batch transfers;
- Ship Designer bridge;
- native fleet/retrofit route;
- Supply Ship reserve increments;
- assigned-supply diagnostics;
- +1 day / save-load;
- Workspace 90/100/115/130.
