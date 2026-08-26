# Roadmap — 24.08.2026 — Military Operations after beta18

## Зафиксированная база

### beta18 Final — Navy Rework

Статус: **RELEASED / RUNTIME PASS / FROZEN**.

Новые Military Operations этапы не имеют права менять принятые Fleet/Ship/Transfer/Retrofit/Logistics semantics. Контроль: 28 scoped Navy blocks, semantic SHA-256 `8d402e4837c8b98f253da65a17096e25367c99d352ed6f1be9852fb1e6a533b1`.

## Этап 1 — beta18.1-pre1.1 — Exact Army Scope Proof

Статически реализовано:

- native `GetSelectedFormation` observer;
- `IsArmy`;
- exact Army name;
- `MilitaryFormation.MakeScope`;
- player owner/is_army probes;
- native exact formation reopen.

Статус в текущей линии: **сохранено, runtime regression требуется вместе с pre1.2**.

## Этап 2 — beta18.1-pre1.2 — Marine/Invasion Scope Discovery

Статус: **STATIC PASS / RUNTIME PENDING**.

Реализовано:

- country-level `total_marine_capacity > 0`;
- корректная семантика UI: positive / not confirmed, без выдуманного числового значения;
- `invasion` root probe;
- `is_naval_invasion` probe;
- `invasion_has_marines` probe;
- source registry для `Scope.GetInvasion/AccessInvasion`;
- invasion probes намеренно UNWIRED;
- build-specific validator routing.

Не реализовано и не должно появиться без нового доказательства:

- `GetMilitaryFormationsArmy`;
- selected Army Marine count;
- exact current Invasion source;
- direct Naval Invasion start;
- Army ↔ Fleet auto-bind.

## Этап 3 — beta18.1-pre1.3 — Exact Invasion Context Proof

Начинается после runtime PASS реализованной части pre1.2.

### Discovery

1. Найти в экспортированных data-type/GUI docs или в доказанном vanilla UI path конкретный источник `Invasion` object/scope.
2. Проверить, что источник относится к выбранному/открытому пользователем вторжению, а не к произвольной коллекции или stale context.
3. Найти только документированный способ передать этот object в ScriptedGui.
4. Если доступен native planner/panel open bridge — доказать callable signature отдельно.

### Implementation при успешном discovery

1. Exact Invasion observer.
2. Root transport probe.
3. `is_naval_invasion`.
4. `invasion_has_marines`.
5. Native reopen/manual planner bridge, только если подтверждён.
6. `0 gameplay writes`, пока direct scripting contract не потребуется и не будет отдельно согласован.

### Fail-safe

Если exact Invasion source не доказан, `pre1.3` не будет выпускать фиктивный selector/marker. Prepared probes остаются unbound.

## Этап 4 — Amphibious Readiness Assistant

Предпочтительная архитектура: **read-only assistant**, а не скрытая автоматизация.

Входы, которые должны быть доказаны независимо:

- exact Army;
- exact Fleet;
- Marine presence/capability с корректной семантикой;
- fleet logistics/readiness;
- exact Invasion, если доступен; иначе native manual invasion workflow.

Выходы:

- готовность армии;
- готовность флота;
- десантная вместимость страны/флота только в доказанной семантике;
- наличие Marines в exact Invasion только при exact invasion scope;
- объяснение блокеров;
- кнопки перехода в штатные панели.

## Отдельная ветка — Army 2.0 picker

Self-contained Army picker остаётся отдельной задачей. Он не должен строиться на guessed `GetMilitaryFormationsArmy`. Возможные пути:

- source-proven country Army accessor;
- vanilla data-model reuse;
- native panel selection observer как fallback без списка CMP.

До доказательства accessor текущий native-selected Army observer остаётся правильной архитектурой.

## Runtime gate pre1.2

Перед переходом к pre1.3 проверить:

- Army A / Army B exact selection/reopen;
- Fleet rejection;
- country Marine capacity positive / not-confirmed states;
- отсутствие invasion auto-actions;
- +1 day;
- save/load;
- Workspace 90/100/115/130;
- Navy smoke regression.
