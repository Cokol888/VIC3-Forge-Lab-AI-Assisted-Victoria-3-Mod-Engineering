# beta18-pre4 — Exact Ship Control & Flagship

**Build ID:** `CMP-0.3-B18-PRE4-20260822`  
**Parent:** beta18-pre3 Fleet Composer 2.0 — Runtime PASS  
**Статус:** STATIC PASS / RUNTIME UNVERIFIED

## Цель этапа

После принятия Fleet Composer 2.0 следующий уровень naval model — работа не только с `Fleet`, но и с конкретным объектом `Ship` внутри выбранной formation.

Модель beta18 теперь:

`Ship Type → Ship Template → Ship → Fleet`

pre4 впервые делает `Ship` отдельной точной целью CMP.

## Exact Ship Selector

Вкладка `Флот → Корабли` использует уже доказанный native Fleet context beta18-pre2.4. После выбора флота CMP строит 100 позиционных слотов, разбитых на пять страниц по 20.

Контракт выбора:

1. root = выбранная `MilitaryFormation`;
2. выбираются только неуничтоженные ships (`hit_points > 0`);
3. ships упорядочиваются по `power_projection`;
4. выбранная позиция обрабатывается через `ordered_scope_ship`;
5. на exact `ship` ставится `cmp_navy18_exact_ship_target`;
6. позиция хранится на formation только как UI hint; gameplay target — marker самого Ship.

Если порядок ships позже меняется, marker остаётся на ранее выбранном объекте Ship.

## Диагностика exact Ship

Для отмеченного Ship CMP показывает:

- Ship Type;
- flagship / non-flagship;
- damaged / healthy;
- in port / at sea;
- in battle / out of battle;
- hit-points band: 75–100 / 50–75 / 25–50 / <25%;
- crew band: 75–100 / 50–75 / 25–50 / <25%.

До появления доказанного прямого GUI-accessor exact числовые HP/Crew не подменяются выдуманными значениями.

## Flagship write

pre4 открывает только один exact-ship write-family:

- `set_as_flagship = yes`;
- `set_as_flagship = no`.

Действие разрешается только если:

- Fleet принадлежит игроку;
- exact Ship существует;
- Ship не находится в battle;
- для назначения Ship Type отмечен в catalog как `can_be_flagship`;
- повторное назначение уже существующего flagship блокируется.

Transfer, damage, crew modification и destruction остаются закрыты.

## Почему позиционный selector

Публичный 1.13 scripting surface документирует `ship` scope, `{ordered}_scope_ship`, ship triggers и `set_as_flagship`, но мы не считаем доказанным отдельный динамический `MilitaryFormation.GetShips` GUI data-model. Поэтому pre4 не придумывает GUI API и использует подтверждённый script iterator.

Runtime должен доказать, что `ordered_scope_ship + position + power_projection` стабильно выбирает конкретный Ship и marker сохраняется на нужном объекте.

## Следующий этап

Только после Runtime PASS pre4:

`beta18-pre5 → Transfers / Retrofit bridge / Amphibious / Supply`

Transfer будет строиться поверх exact Ship target, а не поверх ship type или всего Fleet.
