# Cheat Menu Pro — Roadmap v11 / beta18 Final Released

**Дата актуализации:** 22.08.2026  
**Статус:** beta17 Final RELEASED; **beta18 Final RELEASED / Runtime PASS**.

## 1. beta18 Final — Navy Rework — RELEASED

Полный RC1 runtime regression подтверждён пользователем. Final не добавляет новых gameplay-механик и фиксирует принятый Navy surface:

- полный каталог 20 vanilla + 5 Tech & Res combat hulls;
- Fleet Composer 2.0;
- exact Fleet;
- existing Fleet add-ships;
- exact Ship;
- flagship;
- single/batch/cross-Fleet transfer;
- native Ship Designer / Retrofit bridge;
- national Supply Ship reserve;
- assigned Supply diagnostics;
- no hidden fallback / no ghost target.

Final защищён semantic freeze относительно принятого RC1.

## 2. Military Operations / Amphibious Assistant

Следующий отдельный функциональный цикл:

- Marines;
- marine capacity;
- Fleet readiness;
- invasion checklist;
- native invasion bridge;
- без fake auto-attach.

Это post-beta18 модуль и не изменяет выпущенный Navy Final baseline без отдельного gate.

## 3. Army Rework 2.0

Navy UX становится референсной архитектурой:

- multi-unit composer → одна Army;
- несколько типов + независимые количества;
- tactical profiles;
- понятные modifier/preset semantics;
- exact formation workflow;
- Expert controls отдельно от role presets.

## 4. beta19 — Technology 2.0

- provider-aware technology catalog;
- dependencies/prerequisites;
- Vanilla / Tech & Res separation;
- безопасные Normal / Expert операции;
- точный feedback;
- Search/filter только после compatibility gate.

## 5. beta20 — Special & Quick

- frequent operations;
- diagnostics;
- expert actions;
- mass operations;
- risk tiers;
- единый confirmation/review слой.

## 6. Economy / Markets / Regions Rework

Отдельный discovery/rework:

- market scope / goods;
- supply/demand / prices;
- state production;
- production methods;
- ownership;
- resource caps;
- infrastructure / market access;
- государственное производство/покупка товаров только при подтверждённом scripting surface.

## 7. Vanilla CMP Rework

Каждая legacy-функция проходит audit:

`label → tooltip → SGUI → effect/modifier → scope → negative states → tick → persistence → result`.

Решение для каждой функции: сохранить / исправить / заменить / Expert / удалить.

## Release discipline

Registry/codegen source of truth; deterministic `--check`; zero missing GUI→SGUI/effect refs; zero duplicate `cmp_*`; RU/EN parity; no guessed scripting surface; static QA + runtime evidence before promotion.
