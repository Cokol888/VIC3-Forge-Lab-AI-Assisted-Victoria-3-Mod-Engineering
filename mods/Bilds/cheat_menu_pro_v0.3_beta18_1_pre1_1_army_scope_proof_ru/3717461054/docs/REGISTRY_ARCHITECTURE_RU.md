# CMP v0.3-beta11 — архитектура Registry / Code Generation

## Зачем это сделано

До beta11 добавление одного нового типа ресурса, здания, юнита или корабля требовало синхронно править несколько Jomini-файлов и огромный `sakuya_main.gui`. Это создаёт риск рассинхронизации GUI → scripted GUI → effect и усложняет обновления Workshop-модов.

Beta11 вводит декларативный слой. Источник истины теперь хранится в `registry/*.json`, а повторяющийся игровой код генерируется скриптом `tools/generate_registry.py`.

## Registry

- `providers.json` — источники контента и detection triggers.
- `buildings.json` — 56 зданий, которые уже поддерживает Staffing Assistant, с профилем штата.
- `resources.json` — 8 ресурсов Tech & Res, building type, building group и геологические tiers/traits.
- `land_units.json` — 26 сухопутных юнитов, роль, provider и unlock technology.
- `ships.json` — 5 проверенных современных корпусов Tech & Res, роль и unlock technology.
- `operations.json` — каталог операций и этап roadmap, который станет владельцем генерации.
- `fleet_builder.json` — количества, пресеты и amphibious-support package Fleet Builder.

## Что уже реально генерируется

Beta11 не ограничивается документацией. Из registry генерируются production-файлы:

1. `common/scripted_guis/cmp_fleet_builder_sgui.txt`
2. `common/scripted_effects/cmp_fleet_builder_effects.txt`
3. `common/scripted_triggers/cmp_provider_triggers.txt`
4. ряд выбора типа корабля внутри `gui/main/sakuya_main.gui`
5. `generated/registry_manifest.json` и справочная документация

GUI-блок ограничен маркерами `CMP_REGISTRY_BEGIN/END fleet_ship_selector`; generator обновляет только этот участок и не переписывает весь 8+ МБ GUI-файл.

## Provider contract

Provider описывает `id`, источник, Workshop ID и detection trigger. В текущем стеке:

- CMF: `community_framework_is_active`
- Tech & Res: `technres_is_active`

Tech & Res сам экспортирует `REPLACE_OR_CREATE:technres_is_active = { always = yes }`, поэтому CMP не определяет присутствие мода по косвенным признакам.

## Workflow разработчика

1. Изменить JSON registry.
2. Запустить `python3 tools/generate_registry.py`.
3. Запустить `python3 tools/generate_registry.py --check`.
4. На полном overlay 3717461054 запустить `python3 tools/validate_release.py --overlay <path>`.
5. Только после PASS упаковывать релиз.

Generated-файлы нельзя редактировать вручную: следующая генерация перезапишет изменения.

## Следующий потребитель — beta12

В beta12 эти же registry будут использованы для Regions & Buildings 2.0: `ADD/SET/REMOVE` уровней зданий, `ADD/SET/CLEAR` ресурсов, Tech & Res geology provider и PM-aware Staffing. Главная цель — убрать ручные OR-цепочки на десятки зданий из Staffing/Resource pipeline.
