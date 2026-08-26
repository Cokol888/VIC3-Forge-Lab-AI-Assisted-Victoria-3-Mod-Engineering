# Cheat Menu Pro v0.3 beta17 Final RC1 — Army Final

Дата аудита: 20.08.2026  
Build ID: `CMP-0.3-B17-FINAL-RC1-20260820`  
База: Victoria 3 `1.13.*`, Workshop snapshot `3717461054`  
Статус: static candidate; runtime-приёмка RC1 обязательна.

## Цель этапа

Army Final закрывает армейский домен как проверяемый контракт, а не как набор отдельных кнопок. Повторяемая логика описана в `registry/army_final.json`, а `tools/validate_army_final.py` проверяет Builder, presets, mixed templates, Designer, Marines и Army Controls до общего release-gate.

## 1. Army Builder

- 26 зарегистрированных типов сухопутных подразделений.
- 5 размеров: 1 / 5 / 10 / 25 / 50.
- Полная матрица: **130** точных create-веток.
- Создаётся новая `army` formation через `create_military_formation`.
- HQ и `state_region` берутся из одной отмеченной собственной области; если отмечено несколько, используется детерминированная политика highest-GDP marked owned state.
- Для каждой не-базовой единицы technology gate должен совпадать с `registry/land_units.json`.
- `service_type = regular` проверяется статически во всех 130 ветках.

Army Builder не выбирает существующую армию и не имеет fallback «первая доступная formation».

## 2. Quick presets

Четыре пресета только настраивают Builder, после чего создание остаётся отдельным действием:

- Infantry Corps — 25;
- Artillery Group — 10;
- Mobile Corps — 10;
- Marine Force — 10.

### Исправления Army Final

1. В Mobile Corps были две последовательные ветки `military_drill`: первая выбирала Cuirassiers, поэтому вторая Dragoons была недостижима. RC1 оставляет одну детерминированную ветку Dragoons, совпадающую с tie-break mixed/designer.
2. SGUI Artillery Group не перечислял `blitzkrieg`, хотя effect уже умел выбирать Tech & Res Modern Heavy Tank при `blitzkrieg`. Gate синхронизирован с effect и больше не зависит от косвенного наличия ранней технологии.

Cuirassiers и vanilla Heavy Tank остаются доступны для ручного выбора в Builder; generated templates используют один фиксированный вариант при одинаковом unlock tier, чтобы ветвление было однозначным.

## 3. Mixed templates

Каждый шаблон имеет 50 батальонов:

- Balanced: 25 infantry / 15 artillery / 10 mobile;
- Infantry Heavy: 35 / 10 / 5;
- Breakthrough: 20 / 15 / 15;
- Armored Fist: 15 / 10 / 25.

Для каждого шаблона проверяется **392** комбинации приоритетов: 8 infantry × 7 artillery × 7 mobile. Всего — **1 568** explicit create branches.

Каждая ветка проверяется на:

- ровно три role-группы;
- точное число батальонов;
- принадлежность unit type правильной роли;
- наличие unlock technology выбранной единицы в `limit`;
- уникальность role-signature;
- общий marked-state target.

## 4. Army Template Designer

Designer содержит:

- размеры: 25 / 50 / 75 / 100;
- infantry: 40 / 50 / 60 / 70%;
- artillery: 10 / 20 / 30%;
- mobile: остаток.

Это **48** конфигураций и **17 472** explicit technology branches.

### Зафиксированная integer-rounding семантика

Когда mobile share > 0:

1. infantry = floor(size × infantry%);
2. artillery = floor(size × artillery%);
3. mobile получает остаток, чтобы сумма всегда была ровно size.

Для 70% infantry + 30% artillery mobile намеренно отсутствует. Существующая генерация использует half-even округление infantry и отдаёт остаток artillery. RC1 не меняет уже работающую механику, но впервые фиксирует и проверяет её как контракт.

Для четырёх 70/30-конфигураций ожидается 56 веток (8 infantry × 7 artillery), для остальных — 392.

## 5. Marines / Amphibious Builder

Проверены только два реально присутствующих в pinned Tech & Res provider tiers:

- Modern Tier Marines — `amphibious_warfare`;
- Advanced Tier Marines — `high_performance_apparel`.

Размеры: 5 / 10 / 25 / 50, всего **8** create branches.

Создание разрешено только при наличии отмеченной собственной области с `has_port_state = yes`. Автоматическое прикрепление созданной армии к флоту не выполняется: этот шаг остаётся честно обозначенным manual game-UI step.

## 6. Army Controls

Контракт:

- цели: игрок или одна отмеченная страна;
- 10 параметров;
- 5 значений на параметр;
- **50** apply endpoints;
- presets: Balanced / Rapid / Economy / Extreme (`cmp_army_controls_preset_god`).

Параметры:

1. offense;
2. defense;
3. morale recovery;
4. mobilization speed;
5. experience gain;
6. army movement speed;
7. supply consumption reduction;
8. military goods cost reduction;
9. military wages reduction;
10. war exhaustion from casualties reduction.

Положительные значения: +10 / +25 / +50 / +100 / +500%.  
Снижения: -10 / -25 / -50 / -75 / -90%.

Mark contract проверяется по `sakuya_mark_country`: перед установкой новой цели старый country mark очищается. Поэтому `every_country` resolver Army Controls имеет один валидный marked target в штатном маршруте.

### Cleanup

Удалены 20 старых `cmp_army_control_*_level` cleanup refs. Такие переменные нигде не устанавливались и не участвовали в механике; они создавали ложное впечатление дополнительного state contract.

## 7. Tech & Res provider audit

10 T&R unit entries сопоставлены с pinned provider snapshot `3472248460`:

- infantry group: Modern/Advanced Mechanized Infantry;
- marine group: Modern/Advanced Tier Marines;
- artillery group: Self-Propelled Artillery, Rocket Artillery, Modern Heavy Tank;
- cavalry/mobile group: Modern Light Tanks, Main Battle Tanks, Giant Death Robot.

Проверены group и `unlocking_technologies`. В частности, Modern Heavy Tank остаётся artillery, Modern Light Tanks — mobile/cavalry.

Vanilla gates в RC1 намеренно не переизобретаются: они сохраняются из уже принятого project registry; переход на другую Victoria baseline требует отдельного compatibility audit.

## 8. Новый обязательный release-gate

`tools/validate_army_final.py` теперь вызывается из `tools/validate_release.py` и проверяет:

- land-unit schema и provider refs;
- T&R pinned provider contract;
- 130 Builder spawn endpoints;
- quick preset priority/gates;
- 1 568 mixed branches;
- 48 Designer configurations / 17 472 branches;
- 8 Marine create branches;
- 10×5 Army Controls matrix и 4 presets;
- single-mark country target contract;
- mode isolation Builder / Mixed / Designer / Marines;
- отсутствие hidden existing-army fallback;
- отсутствие stale Army Controls variables.

## 9. Runtime checklist RC1

1. Builder: по одному vanilla и T&R unit; 1 и 50; проверить выбранную область.
2. Technology negative case: закрытая единица не должна исполняться.
3. Quick presets: Infantry / Artillery / Mobile / Marines.
4. Mixed: все четыре шаблона, состав сразу и после +1 дня.
5. Designer: минимум 25/40/10, 50/50/20, 75/60/30, 100/70/30; последний вариант должен иметь только infantry + artillery.
6. Marines: coastal marked state PASS; inland marked state negative.
7. Controls: Self и Marked Country; один positive и один reduction parameter; Reset Parameter / Reset All.
8. Presets Controls: Balanced / Rapid / Economy / Extreme.
9. Save/load: одна созданная formation и один applied control modifier.
10. Профили Workspace 90 / 100 / 115 / 130: короткий smoke Army / Templates / Controls.

## 10. Критерий beta17 Final

После runtime PASS RC1 выпускается beta17 Final без смешивания с Navy Final. Если найден дефект, создаётся узкий `beta17-final-rc2` только по найденной армейской проблеме.
