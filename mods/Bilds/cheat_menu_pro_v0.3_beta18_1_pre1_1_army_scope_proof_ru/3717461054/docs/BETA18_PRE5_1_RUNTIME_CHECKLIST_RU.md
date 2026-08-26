# Runtime Checklist — beta18-pre5.1 Retrofit & Naval Logistics

**Build:** `CMP-0.3-B18-PRE5-1-20260822`  
**Static QA:** PASS  
**Runtime:** UNVERIFIED

## 1. Открытие нового модуля

1. Полностью заменить текущий `3717461054` содержимым beta18-pre5.1.
2. Полностью перезапустить Victoria 3.
3. Открыть `Рабочая область → Армия и флот → Флот → Логистика`.
4. Проверить Build ID.
5. Проверить, что вкладки Fleet помещаются и кликаются в профилях 90 / 100 / 115 / 130.

## 2. Ship Designer / Retrofit bridge

1. Нажать **Открыть конструктор кораблей**.
2. Убедиться, что открывается штатный Ship Designer Victoria 3.
3. Создать или изменить пользовательский Ship Template.
4. Вернуться в CMP.
5. Выбрать собственный Fleet доказанным native Fleet route.
6. Открыть `Логистика` и нажать **Открыть штатную карточку флота**.
7. В штатном списке кораблей выбрать подходящие Ships.
8. Выполнить штатный путь `Change Template → Retrofit`.
9. Убедиться, что CMP сам не выполняет скрытый direct retrofit и не меняет шаблон без команды пользователя.
10. Проверить состояние после +1 дня и после save/load.

**PASS:** CMP корректно приводит пользователя к штатному template/retrofit workflow и не конфликтует с ним.

## 3. Государственный резерв Supply Ships

Записать исходное значение национального Supply Ship reserve в штатном UI игры, если оно доступно.

Последовательно проверить:

- `+1`;
- `+10`;
- `+50`;
- `+100`.

После каждого действия:

1. проверить feedback CMP;
2. проверить изменение штатного значения;
3. промотать +1 день и убедиться, что значение не откатилось самопроизвольно.

**Важно:** операция должна менять национальный reserve, а не количество боевых Ships конкретного Fleet.

## 4. Supply maintenance fulfillment

Проверить, что CMP показывает один и только один статус:

- высокий (75%+);
- средний (25–74%);
- низкий (<25%).

Если удаётся изменить экономические условия так, чтобы fulfillment сменил диапазон, проверить обновление интерфейса после тика.

## 5. Assigned Supply Ships выбранного Fleet

1. Выбрать Fleet через доказанный native route.
2. Открыть `Логистика`.
3. Проверить отображаемый диапазон `Назначено выбранному формированию`.
4. Сверить с native UI/диагностикой Victoria 3, если точное значение доступно.
5. Переключить Fleet A → Fleet B и убедиться, что диагностика меняется вместе с formation.
6. Выбрать армию/убрать выбор и проверить безопасное состояние `Флот не выбран`.

CMP в этом build ничего не назначает formation напрямую — это read-only diagnostic.

## 6. Regression — Exact Ship Transfers pre5

Так как transfer runtime gate ещё не был отдельно принят, обязательно проверить в этой же сборке:

1. single transfer одного exact Ship другой стране с портом;
2. убедиться, что исчез именно выбранный Ship;
3. batch из 2–3 Ships одного Fleet;
4. batch из нескольких source Fleets;
5. flagship / battle Ship должен блокироваться;
6. +1 день;
7. save/load;
8. проверить source и receiver после загрузки.

Если transfers FAIL, pre5.1 не может перейти в RC1 даже при полностью рабочей логистике.

## 7. Regression — уже принятые Navy gates

Короткий smoke:

- Composer 2.0 → один mixed Fleet;
- native Fleet target;
- exact Ship selector;
- flagship set/unset;
- Ship Designer opening.

## Критерий PASS pre5.1

- Retrofit bridge работает и не делает fake direct writes;
- Supply reserve `+1/+10/+50/+100` работает как country resource;
- maintenance diagnostic корректно отображается;
- assigned Supply diagnostic следует за selected formation;
- transfer regression PASS;
- +1 day / save-load PASS;
- Workspace 90/100/115/130 PASS;
- нет silent fallback и ghost target.
