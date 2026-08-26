# beta18.1-pre1 — Military Operations Discovery

**Build ID:** `CMP-0.3-B18-1-PRE1-20260823`  
**Parent:** `beta18 Final — Navy Rework`  
**Статус:** DISCOVERY / no gameplay writes

## Цель

Первый post-beta18 цикл не добавляет автоматическое морское вторжение. Он фиксирует доказанный data/scripting surface для будущего Assistant:

`Army / Marines ↔ Fleet ↔ marine capacity ↔ Supply Ships ↔ Naval Invasion ↔ native UI`.

Главный принцип остаётся тем же, который стабилизировал Navy Rework: сначала scope/data/native-bridge discovery, затем UI, затем runtime gate, и только после этого gameplay writes.

## Подтверждённый read-only surface Victoria 3 1.13

### Country marine capacity

`total_marine_capacity` — значение на country scope, возвращающее общую вместимость морпехов всех флотов державы.

Статус CMP: **SUPPORTED_READ_ONLY**.

Это подходит для общего индикатора готовности страны, но само по себе не сообщает, какой конкретный Fleet будет использоваться для операции.

### Invasion diagnostics

`invasion_has_marines` — trigger на invasion scope: есть ли среди армий вторжения морские пехотинцы.

`is_naval_invasion` — trigger на invasion scope: является ли операция морским вторжением.

Статус CMP: **SUPPORTED_READ_ONLY / NEEDS_INVASION_SCOPE**.

Пока CMP не имеет доказанного exact Invasion selector/bridge, эти triggers нельзя честно выводить как состояние «текущей операции».

### Exact Fleet foundation

Из beta18 Final переиспользуется доказанный runtime-контекст `MilitaryFormation` и native Fleet panel bridge. Никакой новый persistent Fleet marker для Military Operations не вводится.

Доступные Fleet diagnostics для будущего Assistant включают:

- количество кораблей в бою;
- назначенные Supply Ships;
- выход кораблей за максимальную дистанцию до порта;
- уже доказанный exact Fleet context.

### Marines

Текущий проектный registry содержит только два отдельно проверенных Tech & Res marine unit type. Поэтому существующий Amphibious Builder нельзя автоматически объявлять универсальной моделью Marine forces Victoria 3.

До отдельного Army/Combat Unit discovery marine coverage имеет статус **PARTIAL_PROVIDER_BOUND**.

## Аудит текущей Amphibious-механики CMP

В beta18 Final уже существует legacy `cmp_army_amphib_*`.

Она:

- выбирает количество 5/10/25/50;
- ищет отмеченную портовую область;
- создаёт отдельную Army;
- использует два Tech & Res marine tiers;
- не связывает созданную Army с exact Fleet;
- не является invasion readiness assistant.

Решение pre1: **не удалять и не расширять**. Код заморожен побайтово до Army Rework 2.0.

Также старый `cmp_fleet_taskforce_prepare` не используется как foundation нового Assistant, потому что появился до доказанной beta18 exact-Fleet архитектуры.

## Native invasion UI

В 1.13 присутствуют отдельные GUI-файлы `invasion_planner.gui` / `invasion_panel.gui`, но наличие GUI не доказывает конкретный callable bridge из standalone CMP Workspace.

Статус: **DISCOVERY_REQUIRED**.

До подтверждения entry point пользовательский маршрут будет классифицироваться как MANUAL/NATIVE, а не заменяться выдуманной кнопкой.

## Что запрещено в pre1

- auto-attach Army к Fleet;
- direct start naval invasion;
- fake invasion target selection;
- изменение beta18 Navy effects;
- расширение legacy Amphibious Builder;
- новые gameplay writes.

## Результат discovery

Текущая архитектура позволяет уверенно строить read-only readiness layer вокруг Country + exact Fleet, но exact Invasion и универсальный exact Army/Marine context ещё требуют отдельного discovery.

Следующий технический шаг — подтвердить:

1. точный Army formation context по аналогии с beta18 Fleet;
2. способ подсчёта/классификации Marines в выбранной Army;
3. native invasion UI bridge или зафиксировать MANUAL route;
4. какие readiness-показатели можно читать без изменения gameplay-state.
