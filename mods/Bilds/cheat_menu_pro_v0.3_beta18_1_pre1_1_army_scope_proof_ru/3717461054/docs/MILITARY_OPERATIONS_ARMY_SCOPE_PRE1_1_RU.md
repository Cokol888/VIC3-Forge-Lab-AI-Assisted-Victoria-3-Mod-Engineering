# beta18.1-pre1.1 — Army Scope Proof

**Build ID:** `CMP-0.3-B18-1-PRE1-1-20260823`  
**Версия:** `0.3-beta18.1-pre1.1`  
**Parent:** `0.3-beta18.1-pre1`  
**Victoria 3 baseline:** `1.13.10`  
**Статус до игры:** **STATIC PASS / RUNTIME PENDING**

## 1. Цель

`pre1.1` решает только одну задачу: доказать безопасный **exact Army context** до разработки Amphibious Readiness Assistant.

Архитектурный принцип beta18 сохраняется:

`native object → exact scope proof → diagnostics → runtime PASS → только затем новые операции`.

Сборка **не** создаёт отдельный Army marker, **не** добавляет Army/Fleet/Invasion gameplay writes и **не** пытается угадать недоказанные GUI API.

## 2. Что подтверждено источниками

Публичный scripting surface Victoria 3 1.13 содержит:

- `invasion_has_marines` — invasion-trigger, проверяющий наличие marine combat unit среди армий вторжения;
- `is_naval_invasion` — invasion-trigger;
- `total_marine_capacity` — country-level marine capacity;
- отдельные iterators `*_scope_army` и `*_scope_fleet`.

Hotfix `1.13.10` от 12.08.2026 отдельно исправляет зависание naval invasions на 99%, проблему уничтожения Army при reroute transport fleet во время посадки на naval invasion и улучшает naval mission UI/tooltips. Это усиливает решение CMP не подменять штатный invasion workflow недоказанной автоматизацией.

Источники discovery:

- Victoria-3-Modding-Co-op / Modding-Digests — `1.13.x` script-doc diffs;
- Victoria 3 Hotfix 1.13.10 — Steam Community / Steam patch notes.

## 3. Реализованный read-only Army observer

В верхней части страницы **«Армия и флот 2.0»** добавлена кнопка **«Операции»**.

Порядок проверки:

1. В штатном интерфейсе Victoria 3 открыть нужную Army.
2. Вернуться в CMP → **Армия и флот 2.0 → Операции**.
3. CMP наблюдает `GetSelectedFormation.IsArmy`.
4. При Army-context показывает точное имя через `MilitaryFormation.GetNameNoFormatting`.
5. CMP передаёт `MilitaryFormation.MakeScope` в два read-only ScriptedGui probe.
6. Кнопка **«Открыть армию»** повторно открывает штатную карточку той же `MilitaryFormation` через общий `InformationPanelBar.OpenMilitaryFormationPanelTab` bridge.

CMP ничего не сохраняет в gameplay-state и не создаёт собственную цель.

## 4. Два runtime-probe

### ROOT probe

`cmp_ops_army_root_probe`

```text
scope = military_formation
is_shown = { always = yes }
```

Назначение: доказать транспорт exact `MilitaryFormation.MakeScope → ScriptedGui` для выбранной Army.

### ARMY/OWNER probe

`cmp_ops_army_owner_probe`

```text
scope = military_formation
is_shown = {
    is_army = yes
    owner = { is_player = yes }
}
```

Назначение: доказать, что переданный root действительно является собственной Army игрока, а не просто произвольным MilitaryFormation.

Оба endpoint являются **read-only**: `effect`, `is_valid`, marker/write-команды отсутствуют.

## 5. Что намеренно не реализовано

### Self-contained Army picker

Точное имя country GUI accessor для списка Army не считается доказанным. Поэтому `GetMilitaryFormationsArmy` и любые симметрично придуманные аналоги **не генерируются**.

До отдельного доказательства Army выбирается штатным интерфейсом Victoria 3, а CMP только наблюдает exact native selection.

### Marine count выбранной Army

`invasion_has_marines` доказывает, что движок умеет классифицировать marine combat units внутри invasion context, но этого недостаточно для честного утверждения, что CMP уже имеет доказанный универсальный путь:

`selected Army → combat units → marine classification → count`.

Статус: **DISCOVERY_UNRESOLVED**.

### Exact Invasion context / callable UI bridge

Наличие штатного invasion UI и invasion triggers не доказывает конкретный standalone callable bridge из CMP Workspace.

До доказательства маршрут остаётся **MANUAL / NATIVE**. CMP не выполняет:

- start naval invasion;
- target selection;
- Army ↔ Fleet auto-attach;
- fake Invasion marker.

## 6. Post-Final Navy freeze исправлен архитектурно

Исторический `registry/beta18_final_freeze.json` сохранён и по-прежнему является доказательством принятого beta18 Final.

Проблема старого gate: он содержал semantic hash **всего** `generated/workspace_shell.gui.txt`. Поэтому любое независимое post-beta18 UI-добавление формально нарушало Navy freeze.

`pre1.1` добавляет `registry/beta18_postfinal_navy_freeze.json`:

- все frozen Navy SGUI/effects/data по-прежнему проверяются против beta18 Final;
- Workspace проверяется по изолированному Navy surface;
- защищаются 28 named blocks: Fleet picker + `catalog/new/existing/shipctrl/transfer/logistics` для профилей 90/100/115/130;
- baseline semantic SHA-256: `8d402e4837c8b98f253da65a17096e25367c99d352ed6f1be9852fb1e6a533b1`.

Это разрешает независимый Operations UI, но не разрешает semantic drift принятого Navy UX.

## 7. Static QA

Перед упаковкой подтверждено:

- `tools/generate_workspace_shell.py --check` — PASS;
- `tools/generate_build_identity.py --check` — PASS;
- `tools/validate_navy_freeze.py` — PASS;
- `tools/validate_military_operations_pre1.py` — PASS;
- `tools/validate_registry_coverage.py` — PASS;
- `tools/validate_ui_accessibility.py` — PASS;
- `tools/validate_release.py` — PASS;
- `0` новых gameplay writes;
- `0` Navy gameplay changes;
- `0` persistent Operations markers;
- legacy `cmp_army_amphib_*` — byte-identical;
- accepted Navy/target files — byte-identical;
- scoped Navy Workspace surface — semantic-identical, 28/28 blocks.

## 8. Runtime checklist

### Exact Army

1. Открыть CMP без выбранной Army → панель должна показать состояние ожидания.
2. Открыть Army A штатным интерфейсом.
3. Открыть CMP → «Операции».
4. Проверить точное имя Army A.
5. Проверить `ROOT PASS`.
6. Проверить `ARMY PASS`.
7. Нажать **«Открыть армию»** → должна открыться именно Army A.
8. Повторить для Army B с другим названием.
9. Проверить, что Army A и Army B не смешиваются и отсутствует hidden fallback.

### Negative states

10. Выбрать Fleet → Operations panel не должна трактовать его как Army.
11. Убрать military selection → должен вернуться WAIT-state.
12. Проверить иностранное/недоступное формирование, если штатный UI позволяет его выбрать: owner probe не должен выдавать player-owned PASS.

### Persistence/UI regression

13. `+1 day` — observer не должен менять Army.
14. Save → load → повторно выбрать Army и проверить probes.
15. Проверить Workspace 90/100/115/130.
16. Smoke Navy: exact Fleet picker, exact Ship и Logistics должны открываться как в beta18 Final.

## 9. Gate следующего этапа

`pre1.1` повышается до **RUNTIME PASS** только после прохождения checklist выше.

После этого отдельным discovery-gate проверяются:

1. self-contained Army list accessor;
2. универсальный Marine count/classification для exact Army;
3. exact Invasion context;
4. callable native invasion bridge либо окончательная классификация маршрута как MANUAL/NATIVE.

Только после этих доказательств открывается `beta18.1-pre2 — Amphibious Readiness Assistant`.
