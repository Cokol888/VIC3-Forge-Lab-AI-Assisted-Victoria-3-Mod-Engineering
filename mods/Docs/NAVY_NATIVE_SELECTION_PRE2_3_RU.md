# beta18-pre2.3 — Native Fleet Selection & Direct Operations Core

**Build ID:** `CMP-0.3-B18-PRE2-3-20260821`  
**Parent:** `0.3-beta18-pre2.2`  
**Статус до игры:** STATIC PASS / RUNTIME UNVERIFIED

## Причина изменения архитектуры

beta18-pre2.2 доказала, что пользовательский список флотов и `MilitaryFormation.MakeScope` доступны из Workspace, но собственная CMP-система `выбрать formation → записать marker → повторно найти marker → выполнить операцию` не дала надёжного runtime-выбора.

В pre2.3 production-path больше не использует `cmp_military_target_fleet` как источник истины. Victoria 3 сама выбирает formation, а CMP использует выбранный объект непосредственно.

Цепочка production-path:

`строка флота → FormationPanel.SelectFormation(MilitaryFormation.Self) → GetSelectedFormation → MilitaryFormation ROOT → операция`

Legacy marker/resolver физически остаётся в исходниках только как fallback до финального parity-аудита и не вызывается из нового Workspace-route.

## Выбор флота

Список по-прежнему строится из `Country.GetMilitaryFormationsFleet`, но клик по строке вызывает штатное действие Victoria 3:

`FormationPanel.SelectFormation(MilitaryFormation.Self)`.

После клика Workspace читает глобальный `GetSelectedFormation`. Имя выбранного флота выводится прямо из `MilitaryFormation`, без сохранения дополнительной CMP-метки.

Диагностика picker теперь проверяет только production-path:

- Victoria 3 сообщает, что выбран именно Fleet;
- выбранный MilitaryFormation успешно преобразуется в ScriptedGui ROOT;
- жёлтая полоса у строки остаётся диагностикой доступности `MilitaryFormation.MakeScope`, а не индикатором собственной CMP-цели.

## Прямое добавление кораблей

`cmp_fleet_builder_apply_native` имеет `scope = military_formation` и принимает только собственный Fleet. Страна-владелец используется для чтения выбранного типа/количества и technology/provider gates.

Effect сохраняет текущий ROOT во временный saved scope только на время одной операции:

`save_scope_as = cmp_fleet_builder_native_target`

и каждый `create_ship` получает:

`fleet = scope:cmp_fleet_builder_native_target`.

После операции временный saved scope очищается. Повторного сканирования всех formations и поиска `cmp_military_target_fleet` в production-path нет.

## Пустой флот

Пустой собственный Fleet считается допустимой целью: отсутствие ships больше не трактуется как отсутствие fleet. Это важно для созданных игрой пустых формирований, в которые пользователь хочет мгновенно добавить первый корабль.

## Боевой gate

Добавление кораблей блокируется, если в выбранном флоте уже есть хотя бы один корабль в бою:

`NOT = { any_scope_ship = { is_in_battle = yes } }`.

Это консервативный runtime-gate. После подтверждения поведения можно отдельно исследовать более точные ограничения Victoria 3.

## Save/load

CMP больше не обещает сохранять UI-selection флота в собственную persistent-переменную. После загрузки:

- если Victoria восстановила выбранную formation, Workspace её использует;
- если не восстановила, Workspace показывает «Флот не выбран» и требует нового выбора.

Ghost marker после уничтоженного/переданного fleet тем самым не является частью production-модели.

## Не входит в pre2.3

- transfer кораблей;
- exact Ship selector;
- flagship write;
- supply ship write;
- автоматический retrofit;
- прямой выбор пользовательского Ship Template для мгновенного `create_ship`;
- расширение Fleet Composer 2.0 сверх уже существующего универсального role-composer.

Эти механики открываются только после Runtime PASS Native Fleet Target Core.
