# Cheat Menu Pro — Roadmap v10 / beta18 RC1

**Дата актуализации:** 22.08.2026  
**Статус:** beta17 Final RELEASED; beta18-pre2.4/pre3/pre4 Runtime PASS; pre5/pre5.1 core functions accepted; **beta18-RC1 current**.

## 1. beta18-RC1 — Full Navy Regression

Функциональная заморозка. Новые gameplay mechanics не добавляются.

Обязательная regression matrix:

- Fleet Composer 2.0;
- exact Fleet;
- existing Fleet add-ships;
- exact Ship;
- flagship;
- single transfer;
- batch transfer;
- cross-Fleet batch;
- native Ship Designer / Retrofit bridge;
- national Supply Ship reserve;
- assigned Supply diagnostics;
- port / sea / battle / damaged / destroyed;
- immediate / +1 day / save-load;
- Workspace 90 / 100 / 115 / 130;
- no hidden fallback;
- no ghost target.

После Runtime PASS → **beta18 Final**.

## 2. beta18 Final

Final — release/cleanup build, а не feature build:

- только подтверждённые RC1 mechanics;
- metadata/docs cleanup;
- удалить только тот legacy/fallback, для которого доказана parity и отсутствие runtime зависимости;
- полный static QA;
- финальный smoke после package extraction.

## 3. После beta18 Final

### Military Operations / Amphibious Assistant
- Marines;
- marine capacity;
- Fleet readiness;
- invasion checklist;
- native invasion bridge без fake auto-attach.

### Army Rework 2.0
- multi-unit composer → одна Army;
- tactical profiles;
- более понятные modifier/preset mechanics;
- exact formation workflow по образцу Navy.

### Далее
1. beta19 Technology 2.0;
2. beta20 Special & Quick;
3. Economy / Markets / Regions Rework;
4. Vanilla CMP Rework.

## Release discipline

Registry/codegen source of truth; deterministic `--check`; zero missing GUI→SGUI/effect refs; zero duplicate `cmp_*`; RU/EN parity; no guessed scripting surface; static QA + runtime evidence before promotion.
