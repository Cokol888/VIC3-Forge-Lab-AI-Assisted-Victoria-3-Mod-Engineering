# beta18-pre5 — Exact Ship Transfers

**Build ID:** `CMP-0.3-B18-PRE5-20260822`  
**Parent:** beta18-pre4 Exact Ship Control & Flagship — Runtime PASS  
**Статус:** STATIC PASS / RUNTIME UNVERIFIED

## Цель

После подтверждения exact Ship selector и flagship-механики beta18-pre4 новый этап открывает первую ownership-write семантику над конкретными кораблями.

Контракт:

`Fleet -> exact Ship -> receiver Country -> transfer -> verify source/receiver`.

## Подтверждённый scripting contract

Victoria 3 1.13 предоставляет три специализированных эффекта:

- `set_ship_owner = country` — передача одного Ship;
- `set_ship_owner_multiple = country` — последовательная передача нескольких Ships в единый ownership-transfer fleet;
- `clear_ownership_transfer_fleet = yes` — очистка временного transfer fleet после batch-операции.

Для batch cleanup используется страна-источник. Это соответствует публичному treaty implementation, где после серии `set_ship_owner_multiple` `clear_ownership_transfer_fleet` вызывается на `source_country`.

## Получатель

Receiver использует существующую persistent country target `sakuya_mark_country_target`.

Обязательные условия:

- получатель существует;
- получатель не является державой игрока;
- у получателя есть порт (`has_port_country = yes`).

Workspace показывает отдельные состояния: receiver ready / missing / self / no port.

## Одиночная передача

Источник — exact Ship marker, доказанный в beta18-pre4.

Передача блокируется, если Ship:

- уничтожен / `hit_points <= 0`;
- находится в бою;
- является флагманом.

Flagship блокируется намеренно: пользователь сначала снимает статус уже доказанной кнопкой beta18-pre4, затем выполняет ownership transfer.

Операция использует только `set_ship_owner`.

## Пакетная передача

Exact Ship можно добавить в transfer basket. Marker `cmp_navy18_transfer_batch_target` хранится непосредственно на Ship object.

- максимум: 20 Ships;
- basket может содержать Ships из нескольких собственных Fleets;
- переключение Fleet не очищает basket;
- повторное добавление exact Ship блокируется;
- Ship можно удалить из basket или очистить basket целиком.

При применении batch:

1. повторно проверяется receiver;
2. повторно проверяются все marked Ships;
3. exact-ship UI markers очищаются;
4. каждый basket Ship передаётся через `set_ship_owner_multiple`;
5. на source country выполняется `clear_ownership_transfer_fleet = yes`;
6. basket count очищается.

## Почему нет автоматического post-check PASS

Scripting effect подтверждает команду ownership transfer, но до runtime мы не заявляем, что интерфейс может безопасно доказать конечное размещение каждого переданного Ship у receiver. Поэтому result сообщает о выполненной команде и требует проверить source/receiver в игре.

Это соответствует `no guessed scripting surface`.

## Не входит в pre5

- retrofit automation / direct ShipTemplate write;
- amphibious auto-attach;
- supply ship write;
- kill/damage/crew effects;
- передача flagship без предварительного снятия статуса.

Эти направления открываются только после Runtime PASS transfer gate.
