# beta18 Final — Navy Rework

**Build ID:** `CMP-0.3-B18-FINAL-20260822`  
**Версия:** `0.3-beta18-final`  
**Runtime:** `PASS`  
**Parent:** `beta18-RC1`  
**Дата релиза:** 22.08.2026

## Статус

beta18 Final — релизная фиксация Navy Rework после полного runtime regression RC1. Пользователь подтвердил корректную работу всех основных функций RC1.

Final не вводит новые gameplay-механики относительно RC1. Цель сборки — синхронизировать metadata/docs, зафиксировать runtime-статусы, добавить semantic freeze gate и повторно проверить готовый пакет.

## Выпущенный Navy surface

### Полный каталог кораблей

- 20 vanilla combat hulls Victoria 3 1.13;
- 5 Tech & Res combat hulls;
- 25 боевых типов в едином реестре;
- категории Capital / Cruiser / Torpedo;
- technology/provider gates;
- obsolete-фильтрация vanilla через engine data surface;
- Supply Ship не маскируется под обычный combat hull.

### Fleet Composer 2.0

- 5 независимых строк состава;
- любой из 25 combat hulls в каждой строке;
- количества `0 / 1 / 3 / 5 / 10`;
- одинаковый hull разрешён в нескольких строках;
- все ненулевые строки собираются в один новый Fleet;
- новый Fleet привязан к точному temporary scope после создания;
- ShipTemplate при instant-spawn не выдумывается: используется штатный/default template типа.

### Exact Fleet

- прямой контекст `MilitaryFormation` доказан runtime;
- native Fleet panel bridge открывает точную formation;
- production Workspace не зависит от старого persistent `cmp_military_target_fleet` marker-resolver;
- add-ships работает с точным выбранным Fleet;
- hidden first/eligible Fleet fallback отсутствует.

### Exact Ship / Flagship

- точный объект `Ship` выбирается внутри Fleet;
- до 100 позиционных слотов;
- exact marker хранится на объекте Ship;
- diagnostics: Ship Type, flagship, damage, port/sea, battle, HP/Crew bands;
- exact `set_as_flagship = yes/no` прошёл runtime.

### Transfers

- одиночная передача exact Ship;
- пакетная передача до 20 Ships;
- basket может собираться из нескольких source Fleets;
- batch использует `set_ship_owner_multiple`;
- cleanup выполняется через `clear_ownership_transfer_fleet` на source country;
- battle / destroyed / flagship safety gates;
- receiver не может быть игроком и должен иметь порт.

### Ship Designer / Retrofit

CMP не подменяет штатный Ship Designer и не придумывает direct ShipTemplate write.

Поддерживаемый маршрут:

`Ship Designer → пользовательский template → native Fleet panel → native ShipSelection → Change Template → Retrofit`.

CMP предоставляет native bridge, а выбор шаблона и retrofit остаются source of truth Victoria 3.

### Naval Logistics

- Supply Ships моделируются как национальный reserve/resource;
- безопасные country writes: `+1 / +10 / +50 / +100`;
- `supply_ship_maintenance_fulfillment` используется как country diagnostic;
- `num_assigned_supply_ships` — read-only diagnostic выбранной MilitaryFormation;
- direct assignment Supply Ships конкретному Fleet не выдумывается.

## Что сознательно не входит

- direct ShipTemplate write;
- destructive Ship actions: kill/damage/crew;
- direct Supply Ship assignment к formation;
- автоматический amphibious attach/invasion;
- Amphibious Assistant.

Amphibious Assistant перенесён в post-beta18 Military Operations, где будет проектироваться совместно с Marines/Army/Fleet workflows.

## Final freeze

`registry/beta18_final_freeze.json` хранит semantic SHA-256 принятого RC1 Navy gameplay surface.

Final validator сравнивает active Navy SGUI/effect/Workspace Jomini после удаления комментариев и whitespace вне строк. Любое gameplay semantic drift относительно принятого RC1 блокирует релиз.

Hidden legacy Fleet Plans/fallback source оставлен для rollback safety: launcher скрыт, production Workspace на него не опирается. Физическое удаление после принятого RC1 не выполняется, чтобы не вносить ненужный release-риск.

## Post-beta18

1. Military Operations / Amphibious Assistant.
2. Army Rework 2.0.
3. beta19 Technology 2.0.
4. beta20 Special & Quick.
5. Economy / Markets / Regions Rework.
6. Vanilla CMP Rework.
