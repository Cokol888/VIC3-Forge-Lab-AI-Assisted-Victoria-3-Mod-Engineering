# Cheat Menu Pro — актуальная дорожная карта

**Дата фиксации:** 20 августа 2026  
**Текущая ветка:** v0.3 beta17  
**Текущий runtime-кандидат:** beta17-pre2.1 — Fleet Selector Click Hotfix  
**База:** Victoria 3 1.13.*, Workshop snapshot 3717461054

## 1. Gate: beta17-pre2.1 — Fleet Selector Runtime

Текущая разработка не считается принятой до проверки нового persistent fleet selector.

Проверяем:

- отображение списка собственных флотов;
- клик по конкретному флоту;
- появление визуального состояния выбранного флота;
- сохранение точной fleet-target;
- повторную смену цели;
- очистку цели;
- отсутствие старого event-picker;
- выполнение операций именно над выбранным флотом;
- +1 игровой день;
- save/load.

### Результат gate

**PASS:** переходим к beta17-pre3.

**FAIL:** выпускается только `beta17-pre2.2` с исправлением конкретного runtime-дефекта.

Новые функции в pre2.2 не добавляются.

---

# 2. beta17-pre3 — Coverage & Diagnostics Foundation

Цель этапа — устранить системный класс ошибок, при котором существующая игровая сущность не попадает в registry/UI и это остаётся незаметным для QA.

## 2.1. Staffing Coverage 2.1

Текущий Staffing перестаёт зависеть от каталога зданий, предназначенного для ADD/SET/REMOVE.

Разделяем:

`building operations registry`

и

`staffing registry`

Staffing registry должен описывать все поддерживаемые employable buildings.

Для каждого сооружения фиксируются:

- building ID;
- provider;
- категория;
- наличие workforce;
- staffing profile;
- поддерживаемые профессии;
- статус поддержки;
- причина исключения, если объект не поддерживается.

Добавляются отдельные staffing-профили для классов, которых сейчас нет в шести существующих профилях:

- government;
- education;
- military;
- services;
- arts;
- trade;
- ownership;
- дополнительные provider-specific категории по результатам inventory.

Adaptive Staffing 50/75/90/100 сохраняется.

## 2.2. Universal Coverage Contract

Для основных сущностей вводится единый статус:

`SUPPORTED`

`READ_ONLY`

`MANUAL`

`UNSAFE`

`UNSUPPORTED`

Контракт применяется как минимум к:

- buildings;
- resources;
- land units;
- ships;
- technologies;
- diplomatic operations;
- character operations;
- Power Bloc operations.

Правило:

**каждая известная сущность должна либо иметь реализацию, либо явное документированное исключение.**

Молчаливое отсутствие объекта из registry считается QA-дефектом.

## 2.3. Registry Schema Validation

Validator должен проверять не только синтаксис JSON, но и семантические обязательства.

Для building:

- уникальный ID;
- provider;
- localization;
- category;
- operation policy;
- staffing status.

Для unit/ship:

- ID;
- provider;
- technology gate;
- role/type;
- поддержка builder;
- selector status.

Для operation:

- scope;
- target type;
- risk tier;
- negative state;
- result contract.

Codegen не должен запускаться при нарушении обязательной schema.

## 2.4. Build Identity

Вводится единый source of truth версии сборки.

Один Build ID должен использоваться одновременно в:

- integration manifest;
- Workspace;
- Help/Diagnostics;
- QA report;
- changelog;
- release metadata.

Убирается ситуация, когда release уже beta17, а отдельная конфигурация UI всё ещё содержит старый beta16 version tag.

## 2.5. Runtime Diagnostics

Добавляется компактный диагностический блок.

Минимальный набор:

- CMP Build ID;
- baseline Victoria;
- Workspace profile;
- active country target;
- active state target;
- active army/fleet target;
- selected provider;
- last operation;
- last result.

Диагностика не должна загромождать обычный Workspace и открывается по запросу.

## 2.6. Military Metrics Cleanup

Устраняется неоднозначность `267 vs 239`.

Метрики разделяются минимум на:

- registered/reused endpoints;
- audited Workspace references;
- unique gameplay operations.

Каждый QA-report должен явно указывать, какую именно метрику он выводит.

## 2.7. Search / Filter Discovery

Проверяем возможность использования штатного Victoria SearchBar.

До подтверждения минимальной поддерживаемой версии игры SearchBar не становится обязательной зависимостью CMP.

Результат discovery:

- `NATIVE` — безопасно используем vanilla SearchBar;
- `CUSTOM` — реализуем собственный фильтр;
- `DEFERRED` — оставляем category + scroll до Technology 2.0.

---

# 3. beta17 Final — Army Final

После инфраструктурного pre3 завершается собственно армейский домен.

Аудит:

- Army Builder;
- presets;
- mixed templates;
- Army Designer;
- Marines;
- Army Controls;
- target scopes;
- technology gates;
- Tech & Res units;
- массовые операции.

Основное правило:

Builder создаёт новую formation в явно заданном контексте.

Army Controls не должны молча работать с «первой подходящей армией».

Selector конкретной существующей армии добавляется только тогда, когда существует операция, которой действительно требуется exact formation target.

### Runtime Gate

Проверяется:

- создание армии;
- фактический состав;
- technology prerequisites;
- результат сразу;
- +1 день;
- save/load;
- отрицательные состояния;
- все Workspace profiles 90/100/115/130;
- отсутствие undocumented fallback.

После PASS выпускается **beta17 Final**.

---

# 4. beta18 — Navy Final

Финальный морской аудит.

Состав:

- Fleet Selector;
- Fleet Builder;
- Fleet Designer;
- templates;
- ship additions;
- transfers;
- task/fleet operations;
- amphibious workflow;
- состояния кораблей;
- naval technology gates.

Selector развивается до информативной строки:

`Название · HQ · количество кораблей · состояние`

где scripting surface позволяет получить данные безопасно.

Ручной attach армии к флоту сохраняется как честный manual step, пока безопасный direct effect не подтверждён.

### Runtime Gate

- exact fleet target;
- состав до действия;
- состав после действия;
- +1 день;
- transfer обеим сторонам;
- уничтоженные/занятые корабли;
- save/load;
- negative states.

---

# 5. beta19 — Technology 2.0

Новый technology/culture controller.

Основные задачи:

- technology catalog;
- prerequisites;
- provider detection;
- Vanilla / Tech & Res separation;
- безопасные операции;
- обычный и Expert режим;
- точный feedback;
- RU/EN parity.

Если Search/Filter discovery прошёл успешно, Technology 2.0 становится первым обязательным крупным потребителем нового поиска, после чего механизм переносится на здания и военные каталоги.

---

# 6. beta20 — Special & Quick

Собираются:

- частые операции;
- cleanup;
- diagnostics;
- expert actions;
- debug-функции;
- массовые действия.

Вводится единая классификация риска.

Для destructive/high-risk операций проектируется единый review/confirmation screen:

`Цель → действие → параметр → ожидаемое последствие → подтверждение`

No silent no-op остаётся обязательным правилом.

---

# 7. После beta20 — Vanilla CMP Rework

Каждая legacy-функция проходит доказательный аудит:

`label`

→ `tooltip`

→ `ScriptedGui`

→ `effect/modifier`

→ `scope`

→ `negative states`

→ `tick`

→ `persistence`

→ `result`

Для каждой функции принимается одно решение:

- сохранить;
- исправить;
- заменить;
- перенести в Expert;
- удалить.

Legacy-файлы физически удаляются только после полного parity/runtime smoke.

---

# 8. Следующий UX/Engineering backlog

После стабилизации основных доменов:

### P1

- глобальный поиск и фильтры;
- избранное;
- единый risk confirmation;
- сохранение Workspace profile;
- структурированный bug report.

### P2

- CI/release automation;
- compatibility adapters;
- performance profiling;
- provider compatibility matrix.

### P3

- variable-map based Target Core evolution;
- расширяемый provider API;
- contextual onboarding;
- визуальная полировка.

---

# 9. Неизменяемые release gates

Каждая сборка обязана выполнять:

- registry является source of truth;
- deterministic codegen;
- повторный `--check` не создаёт diff;
- 0 missing GUI → ScriptedGui;
- 0 missing ScriptedGui → effect;
- 0 duplicate `cmp_*`;
- balance/braces PASS;
- RU/EN parity;
- ровно корректная локализация/BOM;
- no silent no-op;
- неподтверждённый scripting surface не угадывается;
- UI-only hotfix не смешивается с новой gameplay-механикой;
- runtime click-path;
- immediate result;
- +1 day;
- save/load;
- negative states;
- changelog;
- QA summary;
- known limitations;
- ZIP;
- SHA-256.

# Текущий приоритет

`beta17-pre2.1 runtime`
→ при необходимости `pre2.2`
→ **beta17-pre3 Coverage & Diagnostics**
→ **beta17 Final**
→ **beta18 Navy Final**
→ **beta19 Technology 2.0**
→ **beta20 Special & Quick**
→ **Vanilla CMP Rework**