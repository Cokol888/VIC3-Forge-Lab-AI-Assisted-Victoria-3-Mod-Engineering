# Runtime Checklist — beta18-RC1 Full Navy Regression

**Build:** `CMP-0.3-B18-RC1-20260822`  
**Static QA:** PASS  
**Runtime:** RC1 REGRESSION PENDING

## 0. Чистая установка

1. Полностью заменить текущую папку `3717461054` содержимым RC1.
2. Полностью перезапустить Victoria 3.
3. Открыть `Рабочая область → Интерфейс → Справка`.
4. Проверить Build ID: `CMP-0.3-B18-RC1-20260822`.
5. Убедиться, что Diagnostics показывает RC1 regression status и не зависит от старой CMP-метки флота.

## 1. Fleet Composer 2.0

### 1.1 Базовый mixed Fleet
- Row 1: ранний крупный корабль ×1;
- Row 2: Frigate ×3;
- Rows 3–5: 0;
- создать один Fleet;
- ожидается одна formation / 4 Ships.

### 1.2 Duplicate hull
- Row 1: Frigate ×3;
- Row 2: Frigate ×5;
- ожидается один Fleet / 8 Frigates.

### 1.3 Пять строк
- выбрать пять допустимых строк;
- ожидается одна formation, а не пять отдельных Fleets.

### 1.4 Negative cases
- нет отмеченной портовой области → creation blocked;
- закрытый технологией hull → выбор/создание blocked;
- при наличии Tech & Res проверить один T&R hull;
- если Tech & Res временно недоступен, vanilla hulls не должны ломаться.

После каждого основного сценария: immediate → +1 day → save/load.

## 2. Exact Fleet foundation

1. Открыть Fleet picker.
2. Проверить несколько собственных Fleets.
3. Клик по Fleet A должен открыть native panel именно A.
4. Клик по Fleet B должен открыть B.
5. Никакой ghost target после уничтожения/исчезновения старого Fleet.
6. Проверить add-ships к существующему Fleet:
   - Fleet A +1 Ship;
   - Fleet B +3 Ships;
   - изменяется только выбранный Fleet.
7. Если есть пустой Fleet, проверить добавление первого Ship.
8. Fleet с Ship в battle должен соблюдать battle gate.

## 3. Exact Ship selector

1. Выбрать Fleet минимум с 2 Ships одного типа.
2. Выбрать Slot 1 → exact target A.
3. Выбрать Slot 2 → exact target B.
4. Проверить, что одинаковый Ship Type не склеивает два Ship objects.
5. Для Fleet >20 Ships проверить переход на страницу 2.
6. Проверить damaged / healthy, port / sea, battle / out-of-battle bands, если состояния доступны.
7. Если exact Ship исчез/уничтожен, CMP должен требовать новый выбор без silent fallback.

## 4. Flagship

1. Exact Ship A → назначить флагманом.
2. Сверить native Fleet UI.
3. Exact Ship B → назначить флагманом и проверить перенос статуса.
4. Снять флагман.
5. Ship in battle → операция blocked.
6. Hull, которому запрещён flagship → blocked.

## 5. Single Ship Transfer

1. Отметить другую страну с портом.
2. Выбрать exact Ship вне battle, не flagship.
3. Выполнить single transfer.
4. Проверить, что исчез именно выбранный Ship.
5. Проверить receiver native Navy.
6. +1 day.
7. save/load.
8. Проверить source и receiver после загрузки.

Negative:
- receiver отсутствует;
- receiver = player;
- receiver без порта;
- Ship in battle;
- flagship;
- invalid/lost Ship.

## 6. Batch Transfer

### 6.1 Один source Fleet
- добавить 2–3 exact Ships в basket;
- выполнить batch;
- проверить receiver;
- basket и temporary ownership-transfer context должны очиститься.

### 6.2 Несколько source Fleets
- Fleet A → Ship A;
- Fleet B → Ship B;
- при необходимости Fleet C → Ship C;
- выполнить один batch;
- проверить все источники и receiver.

### 6.3 Invalidation
- добавить Ship в basket;
- до выполнения сделать его недоступным для transfer (battle/flagship), если это возможно;
- batch должен стать invalid, а не подменить Ship.

После успешного batch: +1 day → save/load.

## 7. Ship Designer / Retrofit bridge

1. `Логистика → Открыть конструктор кораблей`.
2. Создать/изменить пользовательский Ship Template.
3. Вернуться в CMP и выбрать Fleet.
4. `Открыть штатную карточку флота`.
5. В native UI выбрать Ships.
6. `Change Template → Retrofit`.
7. CMP не должен автоматически менять template до native команды.
8. Проверить очередь/результат retrofit.
9. +1 day → save/load.

## 8. National Supply Ship reserve

Записать исходное native значение и по очереди проверить:

- `+1`;
- `+10`;
- `+50`;
- `+100`.

После каждой операции:
- меняется национальный Supply reserve;
- combat Ship count выбранного Fleet не меняется;
- feedback соответствует операции;
- +1 day не откатывает значение самопроизвольно.

## 9. Supply diagnostics

### Maintenance
Проверить ровно один активный band:
- high ≥75%;
- medium 25–74%;
- low <25%.

### Assigned to selected formation
- Fleet A → записать отображаемый band;
- Fleet B → диагностика должна следовать за B;
- army/no Fleet → безопасное состояние;
- CMP не выполняет прямое назначение Supply Ships formation.

## 10. Состояния Fleet / Ship

Где возможно проверить:

- Fleet in port;
- Fleet at sea;
- Ship damaged;
- Ship in battle;
- Ship destroyed/lost;
- empty Fleet;
- fleet after transfer;
- fleet after retrofit.

Ожидаемый принцип: invalid target блокируется или требует повторный выбор; silent fallback запрещён.

## 11. Workspace profiles

Для `90 / 100 / 115 / 130` проверить:

- Fleet tabs помещаются;
- Catalog;
- Composer;
- Fleet;
- Ships;
- Transfer;
- Logistics;
- picker/scrollbars;
- tooltips;
- кнопки не перекрываются;
- текст не выходит за критические границы.

## 12. Cross-module smoke

После Navy операций проверить коротко:

- Army Builder / Designer;
- Regions / Staffing;
- Target Core country/state marks;
- Economy page opening;
- никаких неожиданных CMP marks/variables в соседних workflows.

## RC1 PASS

RC1 считается Runtime PASS, если:

- все основные Navy workflows выполняются на точных целях;
- single/batch/cross-Fleet transfer корректны;
- native retrofit bridge не конфликтует с CMP;
- Supply reserve/diagnostics корректны;
- +1 day и save/load не создают ghost targets;
- четыре Workspace-профиля пригодны для работы;
- нет silent fallback;
- нет game-breaking ошибок.

После этого допускается **beta18 Final** без новых gameplay-функций.
