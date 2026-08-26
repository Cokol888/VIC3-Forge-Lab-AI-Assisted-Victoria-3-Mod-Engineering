# Runtime checklist — beta18-pre5 Exact Ship Transfers

**Build:** `CMP-0.3-B18-PRE5-20260822`

## Gate A — Receiver

1. Отметить другую державу через существующий country-target workflow CMP.
2. Убедиться, что у неё есть порт.
3. Открыть `Армия и флот -> Флот -> Передача`.
4. Проверить статус `Получатель готов`.
5. Отдельно проверить: receiver отсутствует; receiver = игрок; receiver без порта.

## Gate B — Single exact Ship

1. Выбрать Fleet доказанным native-маршрутом.
2. В `Корабли` выбрать конкретный не-флагманский Ship вне боя.
3. Перейти в `Передача`.
4. Нажать `Передать выбранный корабль`.
5. Проверить, что именно этот Ship исчез из source Fleet и появился у receiver.
6. Проверить второй Ship того же Ship Type — нельзя перепутать exact object.

## Gate C — Batch в одном Fleet

1. Добавить в basket 2–3 exact Ships одного Fleet.
2. Убедиться, что отображается правильный count.
3. Выполнить batch transfer.
4. Проверить source и receiver.
5. Basket после выполнения должен быть очищен.

## Gate D — Batch из нескольких Fleets

1. Fleet A: добавить exact Ship в basket.
2. Переключиться на Fleet B.
3. Добавить ещё один Ship.
4. Выполнить batch.
5. Оба exact Ship должны перейти одному receiver; остальные Ships обоих Fleets не меняются.

## Gate E — Negative states

- exact Ship в бою — transfer недоступен;
- flagship — transfer недоступен до `Снять флагман`;
- receiver потерял порт после добавления basket — применение блокируется;
- receiver очищен/сменён на игрока — применение блокируется;
- Ship исчез/уничтожен после добавления — batch должен стать invalid, без fallback на другой Ship;
- basket >20 — 21-й Ship не добавляется.

## Gate F — Persistence

1. После successful transfer промотать +1 день.
2. Проверить source/receiver.
3. Save -> load.
4. Повторно проверить ownership и состав Fleets.
5. Отдельно проверить basket, сохранённый до выполнения: marker не должен приводить к передаче другого Ship после load.

## Gate G — UI regression

- Workspace 90 / 100 / 115 / 130;
- Composer 2.0 smoke;
- Exact Ship selector smoke;
- flagship set/unset smoke;
- RU/EN labels и tooltip;
- no silent no-op.

### Критерий PASS

Single и batch transfer адресуют только exact Ships, receiver корректен, ownership сохраняется после +1 day/save-load, invalid states не вызывают скрытого fallback.
