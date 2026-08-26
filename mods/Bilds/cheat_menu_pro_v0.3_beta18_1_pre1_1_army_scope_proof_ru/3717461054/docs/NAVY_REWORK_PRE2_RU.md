# Navy Rework beta18-pre2 — Full Naval Catalog & Native Designer Bridge

## Архитектурное решение

beta18-pre2 исправляет главный пробел pre1: новый флот больше не начинается с каталога только из пяти late-game Tech & Res кораблей. Naval domain моделируется четырьмя разными сущностями:

`Ship Type → Ship Template → Ship → Fleet`.

### Полный каталог

`registry/naval_catalog.json` содержит 25 боевых hulls:

- 9 Capital: 8 vanilla + Modern Battleship T&R;
- 10 Cruisers: 8 vanilla + Modern Cruiser + Modern Carrier;
- 6 Torpedo Craft: 4 vanilla + Modern Destroyer + Modern Submarine;
- Supply Ship — отдельный `READ_ONLY` объект до supply-workflow discovery.

Vanilla IDs, группы и technology gates закреплены по публичному extract `00_ship_types.txt` (blob SHA `0831a667153396240093b3967b1191a58bafa2f5`). Tech & Res остаётся закреплён локальным snapshot `3472248460`. Эти источники используются для discovery/static contract; runtime Victoria 3 остаётся окончательным доказательством.

### Obsolete

CMP не поддерживает вторую ручную таблицу obsolescence. В каталоге vanilla-row фильтруется через `ShipType.IsObsolete(GetPlayer)`, поэтому loaded game/provider semantics остаются источником истины. Переключатель «Показывать устаревшие» снимает этот фильтр.

### Native Ship Designer bridge

В vanilla Military panel вход в редактор шаблонов выполняется `PopupManager.ToggleShipDesignerPopup`. beta18-pre2 использует именно этот route и feature gate `HasDlcFeature('ship_designer')`.

CMP **не вызывает** `ShipDesignerPopup.CreateTemplate`, `EditTemplate` или `SetShipTemplate`: это преднамеренно оставлено штатному UI. Таким образом не создаётся конкурирующий второй Ship Designer и не угадывается write-семантика.

### Catalog creation

Каждый combat hull имеет четыре bounded операции: `x1 / x3 / x5 / x10`. Всего 25 × 4 = 100 explicit ScriptedGui/effect pairs. Операция:

1. проверяет provider и unlock technology;
2. требует собственную отмеченную область с портом;
3. resolve'ит её region как HQ;
4. выполняет ровно один `create_military_formation` типа `fleet`;
5. добавляет один `ship` block выбранного hull и count;
6. не читает `cmp_military_target_fleet` и не использует `create_ship` existing-fleet path.

Этот путь создаёт корабли с обычным/default template движка. Exact selection пользовательского ShipTemplate — отдельная задача Fleet Composer 2.0.

### Что сохранено из pre1

Пяти-hull T&R mixed composer остаётся как compatibility/regression path: 3 124 ненулевых combinations, каждая создаёт одну mixed fleet formation. Exact selected-fleet add-ships beta17 также сохраняется.

### Следующие этапы

- beta18-pre3: универсальный Fleet Composer 2.0 поверх всех hulls + template-selection discovery + preview;
- beta18-pre4: Existing Fleet & Exact Ship Control;
- beta18-pre5: Transfers / Retrofit / Amphibious / Supply;
- beta18-RC1/Final: полный Navy runtime matrix.
