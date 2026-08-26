# Cheat Menu Pro — beta18-pre1 Navy Architecture & Composition Foundation

## Назначение

Beta18 начинается как переработка морского домена под модель Victoria 3 1.13, где корабли являются отдельными объектами. Старый Fleet Builder не удаляется сразу: он сохраняется как совместимый режим работы с **точно выбранным существующим флотом**, а создание нового флота получает отдельный composition workflow.

## Пользовательская модель

### Новый флот

1. Отметить собственную область с портом.
2. Выбрать независимое количество для нескольких поддерживаемых типов кораблей.
3. При необходимости загрузить один из шаблонов состава.
4. Проверить выбранные количества и technology status.
5. Нажать **«Создать один флот»**.

Все ненулевые строки передаются в **один** `create_military_formation = { type = fleet ... }` с несколькими `ship` blocks. Это предотвращает армейскую UX-проблему «один тип → одна formation».

Если отмечено несколько собственных портовых областей, используется область с наибольшим GDP. Отсутствие портовой области блокирует создание.

### Выбранный флот

- Используется persistent exact Fleet Selector beta17.
- Добавление кораблей выполняется только в formation с точным marker `cmp_military_target_fleet`.
- Скрытого выбора первого подходящего флота нет.
- Этот путь временно сохраняет beta17 add-ships semantics и будет расширен в beta18-pre3.

## Поддерживаемый каталог pre1

На pre1 включены только пять ship types, подтверждённых локальным Tech & Res snapshot `3472248460`:

- Modern Destroyer;
- Modern Cruiser;
- Modern Battleship;
- Nuclear Carrier;
- Nuclear Submarine.

Для каждого registry фиксирует `ship_type`, `ship_group`, unlock technology, возможность быть flagship, поддержку modifications и число modification slots.

Полный vanilla ship catalog **не угадывается**: локальная Workshop-коллекция не содержит полного base-game `00_ship_types.txt`. Его расширение является обязательным discovery для beta18-pre2.

## Composition engine

Количество на строку: `0 / 1 / 3 / 5 / 10`.

Пять строк дают 3 125 состояний; all-zero не создаёт флот. Генератор детерминированно формирует **3 124** ненулевые конфигурации. Каждая конфигурация имеет один formation-create call и ровно тот набор `ship` blocks, который выбран пользователем.

Пример логического результата:

- Destroyer ×5
- Cruiser ×3
- Battleship ×1

→ один новый флот из 9 кораблей.

## Шаблоны состава

- Escort;
- Battle Group;
- Carrier Group;
- Wolfpack;
- Amphibious Support.

Шаблон **только заполняет composition state**. Создание запускается отдельной кнопкой, поэтому пользователь может изменить состав после загрузки preset.

## Что намеренно не входит в pre1

- ownership transfer;
- запись supply ships;
- назначение flagship;
- exact ship selector;
- автоматический attach армии к флоту;
- полный vanilla ship catalog;
- обязательный native SearchBar.

Эти функции имеют отдельные beta18 gates. Неподтверждённый scripting surface не заменяется догадкой.

## SearchBar compatibility

Документированный `SearchBar` / `SearchResult` и `gui/shared/search_bar.gui` появляются в Victoria 3 1.13.9. CMP пока объявляет baseline `1.13.*`, поэтому pre1 не делает SearchBar обязательной зависимостью.

## Runtime gate beta18-pre1

- один тип корабля → одна fleet formation;
- 2–5 типов одновременно → всё в одной fleet formation;
- no port → честная блокировка;
- закрытая технология → create недоступен;
- каждый preset → заполнение без немедленного create;
- несколько отмеченных портовых областей → детерминированный highest-GDP choice;
- Selected Fleet compatibility path не регрессировал;
- immediate / +1 day / save-load;
- profiles 90/100/115/130.
