# Military Operations — Marine/Invasion Scope Discovery pre1.2

**Версия:** `0.3-beta18.1-pre1.2`  
**Build ID:** `CMP-0.3-B18-1-PRE1-2-20260824`  
**Базовая версия Victoria 3:** `1.13.10`  
**Статус:** `STATIC_PASS_RUNTIME_PENDING`  
**Родитель:** `0.3-beta18.1-pre1.1` — Army Scope Proof  
**Политика:** `0 gameplay writes`, `0 Navy gameplay changes`, `0 persistent markers`.

## 1. Цель этапа

`pre1.2` расширяет доказанный в `pre1.1` read-only Army-context, но не пытается выдать недоказанный API за рабочий контракт. На этом этапе решаются две отдельные задачи:

1. Добавить безопасную проверку наличия положительной десантной вместимости страны через документированный `total_marine_capacity`.
2. Подготовить read-only проверки `invasion` scope для будущего exact Invasion bridge, не подключая их к Workspace, пока источник конкретного текущего вторжения не доказан.

Это принципиально отличается от автоматизации вторжения: CMP ничего не создаёт, не запускает, не выбирает цель и не связывает Army с Fleet.

## 2. Что подтверждено источниками

### 2.1. `invasion` является полноценным script scope

Экспорт `event_scopes.log` ветки Victoria 3 `1.13.x` содержит отдельный `invasion` scope с поддержкой triggers/effects/scope changes и сохранения переменных. Прямой экспорт `1.13.10` перепроверен по Modding-Digests.

### 2.2. `invasion_has_marines`

Документация определяет trigger как проверку, есть ли хотя бы один marine combat unit в армиях scoped invasion. Следовательно, этот trigger пригоден только после получения настоящего `invasion` root. Он не является Army-level счётчиком.

### 2.3. `is_naval_invasion`

Документированный trigger проверяет, является ли scoped invasion морским вторжением. Он подготовлен как отдельный gate перед `invasion_has_marines`.

### 2.4. `total_marine_capacity`

Документация определяет значение как **общую marine capacity по всем флотам страны**. Поэтому в `pre1.2` оно используется только как country-level сигнал `> 0`.

CMP намеренно **не** трактует его как:

- число морпехов выбранной Army;
- количество батальонов морской пехоты;
- готовность конкретной Army к вторжению;
- capacity выбранного Fleet.

### 2.5. `Scope.GetInvasion` / `Scope.AccessInvasion`

Экспорт `data_types_script.txt` содержит promotions `Scope.GetInvasion` и `Scope.AccessInvasion`. Это подтверждает возможность типизировать **уже существующий invasion scope** в GUI-объект `Invasion`.

Это не решает главную проблему: API не создаёт и не находит «текущее выбранное вторжение». Нужен отдельный доказанный источник scope.

## 3. Что пока НЕ доказано

Статус `DISCOVERY_UNRESOLVED` сохранён для:

- точного country accessor списка Army (`GetMilitaryFormationsArmy` не используется);
- точного `MilitaryFormation → combat unit` traversal для выбранной Army;
- универсального счётчика морпехов выбранной Army;
- источника exact current Invasion object/scope в общем Workspace;
- callable native Invasion planner bridge;
- direct start naval invasion;
- автоматического Army ↔ Fleet bind.

Любые имена наподобие `GetSelectedInvasion`, `GetCurrentInvasion`, `Country.GetInvasions`, `StartNavalInvasion` и `InvasionPlannerPopup.Set` считаются недоказанными и валидатором запрещены в production Workspace/generator.

## 4. Реализация pre1.2

### 4.1. Сохранён exact Army observer

Из `pre1.1` без изменения семантики сохранены:

- `GetSelectedFormation.IsArmy`;
- `datacontext = [GetSelectedFormation]`;
- exact `MilitaryFormation.GetNameNoFormatting`;
- `MilitaryFormation.MakeScope` → read-only ScriptedGui;
- `is_army = yes`;
- `owner = { is_player = yes }`;
- штатное повторное открытие exact MilitaryFormation через `InformationPanelBar.OpenMilitaryFormationPanelTab(...)`.

### 4.2. Добавлен country Marine-capacity probe

Новый endpoint:

`cmp_ops_country_marine_capacity_probe`

Контракт:

```text
scope = country
is_shown = {
    total_marine_capacity > 0
}
```

Workspace вызывает его только с `GetPlayer.MakeScope`. UI имеет два безопасных состояния:

- **«ДЕСАНТНАЯ ВМЕСТИМОСТЬ: ЕСТЬ»** — условие `> 0` истинно;
- **«НЕ ПОДТВЕРЖДЕНА»** — положительное значение не подтверждено.

Второе состояние намеренно не утверждает, что значение точно равно `0`: это boolean-probe, а не числовой getter.

### 4.3. Подготовлены, но НЕ подключены invasion probes

Созданы только read-only ScriptedGui endpoints:

- `cmp_ops_invasion_root_probe` — `scope = invasion`, `always = yes`;
- `cmp_ops_invasion_naval_probe` — `is_naval_invasion = yes`;
- `cmp_ops_invasion_marines_probe` — `invasion_has_marines = yes`.

Workspace их не вызывает. `validate_military_operations_pre1_2.py` специально падает, если обнаружит `GetScriptedGui('cmp_ops_invasion_...')` в production Workspace или generator.

Так мы фиксируем известную часть контракта, но не симулируем отсутствующий exact Invasion source.

## 5. Release-gate

Исправлен post-Final validator routing:

- `pre1.1` продолжает проверяться историческим `validate_military_operations_pre1.py`;
- `pre1.2` проверяется новым `validate_military_operations_pre1_2.py`;
- Navy freeze продолжает проверяться независимо.

Новый validator требует:

- `0 gameplay writes`;
- `0 Navy gameplay changes`;
- `0 persistent markers`;
- сохранение exact Army observer;
- корректный country Marine-capacity probe;
- наличие трёх unbound invasion probes;
- отсутствие guessed Invasion/Army APIs;
- отсутствие Military Operations effects-файла;
- байтовую неизменность legacy Amphibious Builder;
- post-Final Navy semantic freeze.

## 6. Статический QA

Результат текущей сборки:

- `validate_military_operations_pre1_2.py` — **PASS**;
- `validate_release.py` — **PASS**;
- `validate_ui_accessibility.py` — **PASS**;
- GUI references — `11 363`;
- brace-checked Jomini/GUI files — `131`;
- русская локализация — forbidden implementation jargon hits `0`;
- Navy scoped Workspace blocks — `28`;
- Navy scoped semantic SHA-256 — `8d402e4837c8b98f253da65a17096e25367c99d352ed6f1be9852fb1e6a533b1`;
- legacy Amphibious effects SHA-256 — `95e8ae03ca9d83c949f1fc41ce9901e6e11f558fd512bb4f1471d7ce7a8f691e`;
- legacy Amphibious SGUI SHA-256 — `ccb1d02c9c4d25f6eb1a7857b1c4a8e41d90405d8b9a057f84475c518644adb4`.

Статический PASS **не является runtime PASS**.

## 7. Runtime-checklist

### A. Regression exact Army

1. Открыть CMP → «Армия и флот 2.0» → «Операции».
2. До выбора Army должно отображаться состояние ожидания.
3. Открыть штатную Army A, вернуться в CMP.
4. Проверить exact имя Army A, КОРЕНЬ: УСПЕХ и АРМИЯ: УСПЕХ.
5. Нажать «Открыть армию»: должна открыться именно Army A.
6. Повторить с Army B.
7. Выбрать Fleet: он не должен приниматься за Army.

### B. Country Marine capacity

1. В стране, где `total_marine_capacity > 0`, ожидается «ДЕСАНТНАЯ ВМЕСТИМОСТЬ: ЕСТЬ».
2. В состоянии без подтверждённой положительной capacity ожидается «НЕ ПОДТВЕРЖДЕНА».
3. UI не должен выводить это как число морпехов выбранной Army.

### C. Invasion safety

1. В UI должно быть явно указано: invasion probes готовы, но не подключены.
2. CMP не должен автоматически открывать/заполнять/запускать Naval Invasion.
3. Выбор цели, Army и Fleet остаётся штатным ручным процессом.

### D. Regression

- `+1 day`;
- save/load;
- Workspace 90/100/115/130;
- Navy smoke: exact Fleet → exact Ship → native panel / transfer / logistics без изменения поведения.

## 8. Условие перехода к pre1.3

Следующий этап — **Exact Invasion Context Proof**. Он начинается только после runtime-проверки pre1.2 и только при наличии source-proven способа получить конкретный current Invasion object/scope из штатного UI/data context.

Если такой bridge будет доказан, `pre1.3` свяжет prepared probes с exact invasion scope. Если нет, архитектура останется read-only и следующий Amphibious Readiness Assistant будет строиться на exact Army + exact Fleet + штатном ручном Invasion workflow, без искусственного Invasion marker.

## 9. Источники

- Victoria 3 Hotfix `1.13.10`, 12.08.2026 — naval mission UI/tooltips и исправление naval invasion, зависавших на 99%.
- Victoria-3-Modding-Co-op / Modding-Digests — `1.13.x` script documentation.
- `changes_script_docs.md` — `invasion_has_marines`, `is_naval_invasion`, `total_marine_capacity`.
- `event_scopes.log` — `invasion` scope.
- `data_types_script.txt` — `Scope.GetInvasion`, `Scope.AccessInvasion`.

Для implementation-решений использовались экспортированные engine docs; отсутствие найденного API не трактовалось как доказательство отсутствия API. Недоказанные имена не добавлялись в production-код.
