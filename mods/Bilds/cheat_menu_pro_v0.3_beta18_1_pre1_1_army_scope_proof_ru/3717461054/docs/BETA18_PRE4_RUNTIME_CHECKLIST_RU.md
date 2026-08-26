# Runtime checklist — beta18-pre4 Exact Ship Control & Flagship

## A. Regression baseline

Перед Exact Ship убедиться:

1. Fleet picker beta18-pre2.4 по-прежнему открывает правильный native Fleet.
2. Fleet Composer 2.0 beta18-pre3 создаёт один mixed Fleet.
3. Каталог и Existing Fleet add-ships не регрессировали.

## B. Exact Ship Selector — малый флот

Использовать Fleet из 4–8 кораблей.

1. Открыть `Армия и флот → Флот → Корабли`.
2. Выбрать нужный Fleet через штатный picker.
3. На странице 1 позиции `1..N` должны быть доступны, `N+1` — заблокирована.
4. Нажать `1`.
5. Должно появиться `Точный корабль выбран` и конкретный Ship Type.
6. Проверить состояния damage / port / battle / HP / crew.
7. Нажать `2`: target должен перейти на второй Ship, а предыдущий exact marker перестать считаться выбранным.

## C. Несколько одинаковых Ship Type

Нужен Fleet минимум с двумя одинаковыми hulls.

1. Выбрать slot первого такого Ship.
2. Запомнить его статус и при возможности назначить flagship.
3. Выбрать другой slot того же Ship Type.
4. CMP должен считать выбранным другой exact Ship, несмотря на одинаковый тип.

Главная проверка pre4: selector адресует Ship-object, а не только Ship Type.

## D. Pagination

Для Fleet >20 ships:

- page 1: slots 1–20;
- page 2: 21–40;
- далее до page 5 / slot 100;
- недоступные позиции должны быть disabled.

## E. Flagship

### Назначение

1. Выбрать не-флагманский Ship вне battle и с разрешённым `can_be_flagship` type.
2. Нажать `Назначить флагманом`.
3. Status должен переключиться на `Флагман`.
4. Проверить native Fleet card Victoria 3.

### Смена

1. Выбрать другой допустимый Ship.
2. Назначить его flagship.
3. Проверить, что Victoria корректно перенесла flagship state.

### Снятие

1. Выбрать текущий flagship.
2. Нажать `Снять флагман`.
3. Status должен перейти в `Не флагман`.

### Negative cases

- Ship in battle → write disabled;
- hull с `can_be_flagship = false` → назначение disabled;
- exact Ship не выбран → actions disabled;
- уничтоженная exact target → сообщение о потерянной цели, без операции над другим Ship.

## F. Persistence

1. Выбрать exact Ship.
2. +1 день.
3. Проверить marker/status.
4. Save/load.
5. Повторно выбрать Fleet, если native UI selection не сохранилась.
6. Проверить, сохранилась ли exact Ship variable. Оба результата приемлемы только если CMP не выбирает другой Ship молча.

## G. UI profiles

Smoke:

- 90%;
- 100%;
- 115%;
- 130%.

Проверить 5 page buttons, 20 slot buttons, diagnostics и flagship actions без перекрытий.

## Runtime PASS

pre4 принимается только если:

- exact slot выбирает конкретный Ship;
- одинаковые Ship Type различаются как отдельные Ship objects;
- marker не перескакивает молча;
- flagship set/unset работает именно на exact selected Ship;
- negative cases безопасны;
- +1 day/save-load не создают ghost target.
