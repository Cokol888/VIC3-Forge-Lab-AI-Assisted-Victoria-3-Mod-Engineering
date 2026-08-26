# beta18-pre2.1 — Navy Workflow Repair

Build ID: `CMP-0.3-B18-PRE2-1-20260821`

## Причина hotfix

Runtime beta18-pre2 подтвердил полный каталог и открытие штатного Ship Designer, но выявил три проблемы:

1. мгновенное scripted-создание принимает `ship_type`, а пользовательский Ship Template в этот маршрут не передаётся;
2. «Смешанный флот» оставался T&R-only compatibility composer и в ранней эпохе блокировался технологиями;
3. «Выбранный флот» использовал exact Fleet Selector, но список добавляемых кораблей оставался старым пяти-корпусным T&R registry.

## Исправления

- `registry/ships.json` расширен до полного набора 25 боевых hulls: 20 vanilla + 5 Tech & Res;
- exact existing-fleet add-ships path теперь использует те же 25 hulls;
- mixed composer заменён универсальным трёхгрупповым конструктором: Capital / Cruiser / Torpedo;
- в каждой группе выбирается один hull и количество `0/1/3/5/10`;
- до трёх типов создаются одним `create_military_formation` как один новый флот;
- сгенерировано 37 924 ненулевых composition branches;
- role presets стали era-aware fillers: они выбирают лучший доступный корпус по технологиям и не выполняют создание автоматически;
- старый top-level `Планы флота` скрыт из основного маршрута, но legacy implementation оставлен в исходниках как fallback;
- Ship Designer остаётся native bridge через `PopupManager.ToggleShipDesignerPopup`;
- UI явно разделяет мгновенное создание и template-aware штатный workflow.

## Шаблоны кораблей

CMP не утверждает, что `create_military_formation` или `create_ship` могут принять произвольный пользовательский Ship Template: подтверждённый public effect contract передаёт ship type. Поэтому:

- **Мгновенное создание** — использует штатный/default template корпуса;
- **Пользовательский шаблон** — создаётся в native Ship Designer и применяется через штатный naval construction workflow Victoria 3.

Это намеренное правило `no guessed scripting surface`.

## Отложено

- exact Ship selector;
- direct template selection в instant-spawn, если такой контракт будет доказан;
- ownership transfers;
- flagship writes;
- supply ship writes;
- retrofit automation;
- amphibious auto-attach.
