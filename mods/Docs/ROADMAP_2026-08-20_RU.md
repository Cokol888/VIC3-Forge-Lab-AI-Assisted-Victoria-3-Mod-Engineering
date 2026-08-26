# Cheat Menu Pro — дорожная карта v2 после beta17 Final

**Дата фиксации:** 20 августа 2026  
**Ревизия:** Roadmap v2 / post-beta17  
**База:** Victoria 3 1.13.*, Workshop snapshot 3717461054  
**Статус beta17:** RELEASED / пользователь не выявил критических ошибок, ломающих игру  
**Следующий рабочий цикл:** beta18 Navy Rework / Final

## 1. Что закрыто к beta17 Final

Beta17 фиксируется как стабильный армейский baseline, а не как окончательный UX армии.

Подтверждено:

- Army Builder создаёт formation и корректные battalion slots;
- manpower/занятость батальонов набираются штатной системой игры и не форсируются CMP;
- Quick Presets, Mixed Templates, Army Designer, Marines и Army Controls прошли статический Army Final audit;
- Regions/Staffing safety pass beta17-pre3.1 принят в runtime;
- persistent exact Fleet Selector сохранён как основа beta18;
- critical game-breaking runtime defects пользователем не выявлены.

Отложено намеренно:

- Army Designer 2.0 с несколькими типами юнитов в одной formation;
- тактические профили Army Controls поверх Expert-параметров;
- расширенный аудит экономики, рынков, областей и государственного производства товаров.

---

# 2. beta18 — Navy Rework / Final

Beta18 не продолжает старый Fleet Builder как набор разрозненных кнопок. Целевая модель: точный выбранный флот + отдельный конструктор нового флота + безопасные операции над существующим флотом.

## beta18-pre1 — Navy Architecture & Composition Foundation

### Цели

- Зафиксировать ship registry и provider contract для Victoria 3 1.13 naval model.
- Разделить `Новый флот` и `Выбранный флот`.
- Ввести multi-ship composition builder: несколько типов и количеств → одна formation.
- Оставить существующий exact Fleet Selector без скрытого fallback.
- Перевести presets из немедленного действия в заполнение composition preview.
- Добавить Navy-specific validator и Build/QA contract.

### Основной UX

`Новый флот`:

- отмеченная собственная портовая область задаёт HQ context;
- для каждого поддерживаемого ship type выбирается собственное количество;
- несколько ненулевых типов создаются одним `create_military_formation`;
- до применения виден итоговый состав;
- закрытая технология блокирует только недоступную конфигурацию, а не подменяет тип корабля.

`Выбранный флот`:

- существующий exact selector;
- legacy add-ships path сохраняется временно как совместимый secondary mode;
- никаких операций над «первым подходящим» флотом.

### Gate

- один mixed fleet создаётся как одна formation;
- marked port required;
- technology gates;
- 0 hidden fallback;
- immediate / +1 day / save-load;
- четыре Workspace-профиля.

## beta18-pre2 — Fleet Builder & Designer 2.0

- расширить composition model на полный проверенный каталог ship types;
- закончить vanilla + Tech & Res coverage;
- профили состава: Escort / Battle / Carrier / Wolfpack / Amphibious Support;
- preview итогового состава и общей роли флота;
- Fleet Designer перестаёт быть отдельной сеткой 75 кнопок и становится слоем presets/configuration поверх одного composition engine;
- ship modifications только после доказанного safe scripting contract.

## beta18-pre3 — Exact Fleet Operations & Transfers

- exact fleet state diagnostics;
- transfer workflow: source fleet → receiver country → ships → post-check;
- использовать только подтверждённые `set_ship_owner` / `set_ship_owner_multiple` semantics;
- battle-state / invalid-target / self-transfer negative cases;
- ownership-transfer cleanup contract;
- уничтоженные/невалидные цели не должны оставлять ghost target.

## beta18-pre4 — Amphibious / Supply / Flagship Discovery

- amphibious assistant как честный checklist, а не фиктивный auto-attach;
- marine capacity diagnostics;
- supply ships: сначала read-only/diagnostic path;
- flagship: только при подтверждённом exact ship selector;
- manual steps маркируются как MANUAL.

## beta18-RC1 — Navy Final Audit

Обязательные runtime-наборы:

- создание mixed fleet;
- существующий exact fleet;
- добавление кораблей;
- presets;
- transfer обеим сторонам;
- порт / море / бой;
- повреждённые и уничтоженные ships;
- immediate / +1 day / save-load;
- negative technology/target states;
- Workspace 90/100/115/130.

После PASS выпускается **beta18 Final**.

---

# 3. Army Rework 2.0 — после beta18 Final

Армейский rework использует проверенный UX-паттерн Navy Composition Builder.

## Army Designer 2.0

Целевая модель:

`Тип юнита | количество` × несколько строк → **одна** `create_military_formation`.

Пример:

- Infantry ×5
- Artillery ×5
- Mobile ×5
- итог: одна армия / 15 battalion slots.

Требования:

- multi-select;
- отдельные количества;
- preview состава;
- один create effect;
- technology gates для каждой позиции;
- без искусственного форсирования manpower.

## Army Controls 2.0

Основной режим — комплексные тактические профили, построенные только из подтверждённых modifiers:

- Наступление;
- Оборона;
- Мобильная война;
- Экономия;
- Элитный/Extreme профиль;
- Сброс.

Текущие 10 ручных параметров сохраняются как **Expert mode**.

Каждый профиль показывает понятное описание эффекта и полный numerical detail в tooltip/help.

---

# 4. beta19 — Technology 2.0

- provider-aware technology catalog;
- prerequisites и dependencies;
- Vanilla / Tech & Res separation;
- normal / Expert operations;
- precise feedback;
- RU/EN parity;
- SearchBar только если minimum supported baseline подтверждён как 1.13.9+; иначе custom/deferred filter.

---

# 5. beta20 — Special & Quick

- высокочастотные операции;
- cleanup;
- diagnostics;
- expert actions;
- массовые действия;
- risk tiers;
- единый review/confirmation screen для destructive/high-risk действий.

---

# 6. Post-beta20 High-Priority Rework Track — Economy / Markets / Regions

Эта линия уже признана необходимой по runtime-наблюдениям, но её точный version number определяется отдельным discovery после военного/technology цикла.

## Economy & Markets Rework

Будущий аудит должен покрыть:

- market scope и market_goods;
- supply/demand и price-state semantics;
- импорты/экспорты;
- государственное производство и ownership;
- государственные buy/sell/production mechanics, где scripting surface реально позволяет это контролировать;
- инвестиции, субсидии и финансовые последствия;
- отсутствие смешения «деньги страны» и «реальное производство/товарный баланс».

## Regions & Production Rework

- production methods;
- state goods;
- building ownership;
- resource potentials/caps;
- infrastructure and market access;
- state-level production diagnostics;
- presets должны учитывать реальные ограничения state/building/market, а не только registry composition.

До discovery этот блок не получает выдуманных direct effects.

---

# 7. Vanilla CMP Rework

После основных domain rework каждая legacy-функция проходит доказательный audit:

`label → tooltip → SGUI → effect/modifier → scope → negative states → tick → persistence → result`

Решение для каждой функции:

- сохранить;
- исправить;
- заменить;
- перенести в Expert;
- удалить.

Legacy физически удаляется только после parity/runtime smoke.

---

# 8. Неизменяемые инженерные контракты

- registry = source of truth;
- deterministic codegen;
- `--check` без diff;
- 0 missing GUI→SGUI;
- 0 missing SGUI→effect;
- 0 missing nested effect→effect;
- 0 duplicate `cmp_*`;
- RU/EN parity и localization BOM/header gate;
- no silent no-op;
- no guessed scripting surface;
- entity coverage status: SUPPORTED / READ_ONLY / MANUAL / UNSAFE / UNSUPPORTED;
- UI-only hotfix не смешивается с новой gameplay-механикой;
- runtime: click path / immediate / +1 day / save-load / negative cases;
- release: changelog / QA summary / known limitations / ZIP / SHA-256.

# 9. Актуальная последовательность

**beta17 Final — RELEASED**
→ **beta18-pre1 Navy Architecture & Composition Foundation**
→ **beta18-pre2 Fleet Builder & Designer 2.0**
→ **beta18-pre3 Exact Fleet Operations & Transfers**
→ **beta18-pre4 Amphibious / Supply / Flagship Discovery**
→ **beta18-RC1 / Final**
→ **Army Rework 2.0**
→ **beta19 Technology 2.0**
→ **beta20 Special & Quick**
→ **Economy / Markets / Regions Rework (version TBD after discovery)**
→ **Vanilla CMP Rework**
