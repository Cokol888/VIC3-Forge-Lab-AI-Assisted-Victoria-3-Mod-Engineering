# Runtime checklist — beta18-pre2.4 Fleet Scope Proof

## A. Чистый старт

1. Полностью заменить папку `3717461054` этой сборкой.
2. Полностью перезапустить Victoria 3.
3. Открыть `Рабочая область -> Армия и флот -> Флот -> Выбранный флот`.
4. Открыть список флотов.

## B. Scope proof до клика

Для каждой строки флота проверить правую часть:

- жёлтая полоса видна -> bare `MilitaryFormation.MakeScope -> ScriptedGui(always=yes)` PASS;
- синяя полоса видна -> `owner = player` на том же MilitaryFormation ROOT PASS.

Зафиксировать отдельно четыре состояния:

1. yellow PASS / blue PASS;
2. yellow PASS / blue FAIL;
3. yellow FAIL / blue FAIL;
4. любое другое неожиданное состояние.

Скриншот здесь важнее дальнейших операций.

## C. Native panel bridge

1. Нажать `Fleet A`.
2. Проверить, что Victoria открыла штатную карточку именно Fleet A.
3. При необходимости закрыть/сдвинуть CMP, чтобы увидеть штатную карточку.
4. Вернуться в picker и посмотреть верхний статус `GetSelectedFormation`.
5. Повторить для Fleet B.

Ожидаемое доказательство:

- exact native panel = A после клика A;
- exact native panel = B после клика B;
- отдельно фиксируем, изменился ли `GetSelectedFormation`.

## D. Direct add-ships — только если GetSelectedFormation PASS

Если верхний статус действительно сообщает выбранный Fleet:

1. Fleet A -> выбрать доступный hull -> x1 -> добавить.
2. Проверить, что меняется только A.
3. Fleet B -> x3 -> добавить.
4. Проверить, что меняется только B.
5. Пустой Fleet -> x1, если такой fleet существует.
6. Fleet с кораблём в бою -> действие должно быть заблокировано.

Если GetSelectedFormation не обновляется, этот раздел пропускается: это не FAIL add-ships, а недоказанный selection bridge.

## E. После доказательства

Только после exact-target PASS:

- +1 игровой день;
- save/load;
- повтор A/B;
- профили 90/100/115/130.

## Классификация результата

### PASS-1
Yellow + Blue PASS, native panel exact, GetSelectedFormation обновляется.

Следующий шаг: direct operations core можно использовать как production foundation.

### PASS-2
Yellow + Blue PASS, native panel exact, GetSelectedFormation НЕ обновляется.

Следующий шаг: отказаться от global selection и строить операции непосредственно от row MilitaryFormation ROOT / action-time target.

### PARTIAL
Yellow PASS, Blue FAIL.

Следующий шаг: исследовать owner/context link, не менять Fleet Composer.

### FAIL
Yellow FAIL.

Следующий шаг: не использовать `MilitaryFormation.MakeScope` из standalone picker; переносить exact workflow в vanilla military panel hook/bridge.
