# beta18-pre3 — Fleet Composer 2.0

**Build ID:** `CMP-0.3-B18-PRE3-20260821`  
**Parent:** `0.3-beta18-pre2.4`  
**Статус до игры:** STATIC CANDIDATE / RUNTIME UNVERIFIED

## Основание перехода

beta18-pre2.4 закрыла главный инфраструктурный блок Navy Rework: пользователь подтвердил работу row-level `MilitaryFormation` scope и штатного перехода к карточке конкретного флота. Exact Fleet Target Core фиксируется как runtime baseline; новый этап больше не меняет этот механизм.

## Цель pre3

Заменить ограниченный role-composer формата `1 Capital + 1 Cruiser + 1 Torpedo` на настоящий многопозиционный конструктор:

`Корпус × количество` × до пяти независимых строк → **один новый флот**.

Каждая строка:

- выбирает любой из 25 боевых корпусов;
- имеет собственное количество `0 / 1 / 3 / 5 / 10`;
- проверяет provider и технологию выбранного корпуса;
- может повторять корпус из другой строки.

Повтор разрешён намеренно. Например:

- Frigate ×3;
- Frigate ×5;

должны дать один новый флот с 8 фрегатами, если runtime подтверждает аддитивную обработку.

## Почему новая реализация не использует полный перебор составов

Старая промежуточная модель генерировала десятки тысяч полных комбинаций. Для пяти строк по 25 корпусов такой подход становится непрактичным.

Подтверждённый effect contract `create_military_formation` допускает несколько `ship` блоков и предоставляет `save_scope_as` / `save_temporary_scope_as`. В pre3 используется этот механизм:

1. определяется первая ненулевая строка;
2. она создаёт новую formation типа `fleet`;
3. `save_temporary_scope_as = cmp_navy18_comp2_new_fleet` сохраняет точный объект только внутри текущей операции;
4. остальные ненулевые строки добавляют корабли через `create_ship` именно в этот временный fleet scope;
5. persistent CMP target для нового флота не создаётся.

Так мы сохраняем один exact fleet и избегаем комбинаторного generated-кода для всех возможных пятирядных составов.

### Статический объём

- 5 строк;
- 25 hull choices на строку;
- 125 row/hull selection routes;
- 5 количеств на строку;
- 500 bounded anchor branches (`5 × 25 × 4` ненулевых количества);
- 2 375 статических `create_ship` payloads для non-anchor строк;
- полный каталог: 20 vanilla + 5 Tech & Res combat hulls.

## UX

Во вкладке `Конструктор флота 2.0` пользователь видит пять одинаковых строк.

Для каждой строки:

1. `Выбрать / изменить корпус`;
2. выбранный корпус или `Корпус не выбран`;
3. количество `0 / 1 / 3 / 5 / 10`.

Выбор корпуса открывает отдельный scroll-picker из всех 25 combat hulls. Закрытые технологиями/provider варианты остаются видимыми, но disabled. После выбора picker возвращает пользователя к пятистрочному составу.

## Presets

Escort / Battle / Carrier / Wolfpack / Amphibious Support больше не являются отдельными create-effects. Они только заполняют часть пяти строк лучшими доступными корпусами текущей эпохи. Пользователь видит результат и отдельно нажимает `Создать один флот`.

## Ship Templates

Контракт не меняется:

- instant scripted route использует default template Ship Type;
- пользовательский Ship Template создаётся в штатном Ship Designer;
- native construction/retrofit остаётся template-aware маршрутом;
- CMP не придумывает неподтверждённый direct template parameter.

## Что pre3 намеренно не делает

- exact Ship selector;
- flagship writes;
- ship transfers;
- supply ship writes;
- direct retrofit automation;
- amphibious auto-attach;
- собственное persistence нового fleet target.

Эти функции остаются за pre4/pre5 после runtime PASS Fleet Composer 2.0.
