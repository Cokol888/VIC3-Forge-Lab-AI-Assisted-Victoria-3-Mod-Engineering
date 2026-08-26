# Regions & Buildings 2.0 — актуальный контракт beta17-pre3.1

## 1. Здания

### ADD
`ADD N` означает «попытаться добавить до N уровней» в каждой целевой области.

Перед каждым уровнем выполняется availability gate:

- отсутствующее здание: `can_construct_building`;
- существующее: `can_queue_building_levels = 1`.

При достижении level/resource potential cap операция останавливается для этого здания и области. Если часть уровней уже добавлена, результат считается partial, а не silent success.

### SET
SET больше не использует destructive remove → recreate.

- current < target: безопасное повышение до target с per-level guards;
- current = target: успех без изменения;
- current > target: блокировка `UNSAFE`.

Без подтверждённого безопасного direct decrease CMP не уничтожает существующее здание ради точного меньшего уровня.

### REMOVE
Удаляет выбранный building type целиком. Amount selector не является числом удаляемых уровней.

## 2. Каталог Operations

В beta17-pre3.1 прямые operations поддерживают 92 здания. Категории синхронизированы со Staffing: All / Primary / Industry / Infrastructure / Public / Military / Services / Ownership.

Объекты, которыми управляет сама игра и для которых прямой create/remove не имеет безопасного контракта, остаются явно классифицированы в coverage registry и не выдаются как поддерживаемые operations.

## 3. Ресурсы

- `ADD N`: увеличить существующий potential; если potential отсутствует — создать и довести до N.
- `SET N`: удалить прежний potential, создать заново и довести до N.
- `CLEAR`: удалить potential.

Для Tech & Res SET использует `registry/resources.json`; geology traits синхронизируются только для зарегистрированных точных tier values.

## 4. Региональные шаблоны

Шаблоны используют ADD, а не SET:

- Industrial Core: Tooling +10, Steel +10, Motors +5, Power +10, Railway +10, Construction +5.
- Heavy Industry: Steel +20, Motors +10, Chemicals +10, Explosives +5, Power +10, Railway +10.
- Military Industry: Arms +15, Artillery +10, Munitions +15, Steel +10, Explosives +10, Railway +5.
- Infrastructure Hub: Railway +20, Port +10, Construction +10, Power +10.

Каждый компонент проверяется независимо. Недоступный Port или достигший cap ресурс не останавливает остальные компоненты шаблона в той же области. Итоговый footer сообщает partial/blocked состояние.

## 5. Adaptive Staffing

Staffing использует отдельный 132-object coverage inventory и 97 SUPPORTED employable buildings. Operations и Staffing selectors независимы.

`occupancy` остаётся реальным gate. Профессии создаются по registry profile, потому что точный per-profession vacancy vector активных PM не подтверждён публичным scripting surface.

## 6. Codegen / QA

```text
python3 tools/generate_regions2.py --check
python3 tools/validate_regions_operations.py
python3 tools/validate_registry_coverage.py
python3 tools/validate_release.py
```

Release QA проверяет GUI→SGUI, SGUI→effect и nested effect→effect references, selector isolation, category/profile parity и четыре Workspace профиля.
