# Regions Operations Coverage & Safety — beta17-pre3.1

## 1. Причина hotfix

Runtime-обратная связь выявила три системных проблемы в «Области → Операции»:

1. строительный каталог был уже Staffing-каталога и не показывал ряд государственных/военных/сервисных зданий;
2. ADD и шаблоны не проверяли фактический лимит/доступность каждого следующего уровня;
3. один недоступный компонент шаблона мог поставить `cmp_regions2_state_blocked` и тем самым остановить оставшиеся компоненты в той же области.

beta17-pre3.1 исправляет эти проблемы без изменения Target Core, Staffing 2.1 и Fleet Selector.

## 2. Каталог Operations

`registry/buildings.json` содержит 92 объекта со статусом `SUPPORTED` для прямых building operations:

- 55 vanilla;
- 37 Tech & Res.

Категории совпадают с Staffing taxonomy:

- All;
- Primary;
- Industry;
- Infrastructure;
- Public;
- Military;
- Services;
- Ownership.

Категория может быть пустой в Operations, если соответствующие объекты существуют в общем coverage inventory, но прямое create/remove управление ими считается game-managed/unsafe. Это не считается пропуском coverage: статус остаётся явным в `registry/coverage.json`.

## 3. Независимость выбора

Operations и Staffing больше не используют общий selector state:

- Operations: `cmp_regions2_sel_*`;
- Staffing: `cmp_staffing_sel_*`.

Переключение вкладки/категории Staffing не должно менять выбранное здание ADD/SET/REMOVE и наоборот. Legacy B6 selection остаётся только compatibility bridge; новый selector при использовании старого пути очищается предсказуемо.

## 4. ADD и лимиты доступности

Каждый добавляемый уровень проходит отдельный guard:

- если здания ещё нет: `can_construct_building = $BUILDING$` на state scope;
- если здание уже существует: building-scope `can_queue_building_levels = 1`.

Таким образом ADD +25 означает «добавить до 25 уровней, пока каждый следующий уровень разрешён», а не безусловное создание +25.

Если лимит достигнут после частичного успеха, root сохраняет одновременно success и blocked flag, а итог становится partial result.

## 5. SET

Старая beta12-семантика destructive recreate отменена.

Текущий контракт:

- current < target → пошагово повышать с теми же availability/cap guards;
- current = target → успех без изменения здания;
- current > target → `UNSAFE`, никаких `remove_building` и recreate.

Причина: публичный `create_building level=N` не является безопасным способом уменьшения существующего здания, а remove/recreate может потерять runtime-состояние.

## 6. REMOVE

REMOVE удаляет выбранный building type целиком. Amount selector не трактуется как число удаляемых уровней.

Это намеренно отделено от SET/ADD, чтобы UI не создавал ложное ожидание «REMOVE 5 уровней».

## 7. Presets

Четыре шаблона остаются ADD-only:

- Industrial Core;
- Heavy Industry;
- Military Industry;
- Infrastructure Hub.

Каждый шаблон применяется отдельно к каждой target state. Внутри state каждый building component получает собственный `cmp_regions2_state_blocked` guard reset.

Это означает:

- Port может быть заблокирован во внутренней области;
- Railway/Construction/Power того же Infrastructure Hub всё равно продолжают выполняться;
- resource/level cap одного здания не блокирует остальные компоненты;
- итоговый result честно показывает partial/blocked, если хотя бы один компонент не смог выполниться полностью.

Также генератор теперь создаёт ADD helper'ы для всех реально используемых delta: 1 / 5 / 10 / 15 / 20 / 25 / 50 / 100.

## 8. Static QA contract

`tools/validate_regions_operations.py` проверяет:

- 92 operation buildings;
- provider/category coverage;
- Operations/Staffing selector disjointness;
- наличие `can_construct_building` и `can_queue_building_levels`;
- отсутствие destructive `remove_building` внутри SET helpers;
- whole-building REMOVE path;
- generated ADD helper'ы для всех preset delta;
- все preset building IDs;
- per-component preset guard reset;
- четыре profile-layout selector parity;
- resource selector parity.

`tools/validate_release.py` дополнительно проверяет nested `cmp_*_effect` references, поэтому отсутствующий helper внутри другого scripted effect теперь является release-blocking ошибкой.

## 9. Runtime checklist

1. Public: Government Administration / University — ADD 1 и ADD 5.
2. Military: Barrack/Naval building в подходящей и неподходящей области.
3. Infrastructure: Port во внутренней области — blocked без остановки остальных компонентов Infrastructure Hub.
4. Resource-capped building — ADD должен остановиться на лимите, а не превысить его.
5. SET: ниже цели / ровно цель / выше цели.
6. REMOVE: проверить, что удаляется building type целиком и UI не обещает частичное удаление.
7. Каждый из четырёх presets на 2–3 разных областях с разными ограничениями.
8. Проверить result footer для full success / partial / blocked / unsafe.
9. +1 день.
10. save/load.

До прохождения этого набора версия остаётся `UNVERIFIED` по runtime.
