# Runtime checklist — beta18-pre2.1

## 1. Корабли и шаблоны
- Открыть Ship Designer из CMP.
- Создать пользовательский шаблон и убедиться, что CMP не обещает использовать его в instant-spawn.
- Создать Ship of the Line x1 и любой mid/late hull x3.
- Проверить +1 день и save/load.

## 2. Смешанный флот
- Отметить собственную область с портом.
- Ранняя эпоха: выбрать Ship of the Line x1 + Frigate x3; torpedo = 0; создать один флот.
- При доступной технологии: добавить Torpedo Boat x5 и проверить один флот с тремя типами.
- Проверить preset Escort и Battle Group: preset только заполняет выбор.
- Проверить закрытую технологию: кнопка корпуса недоступна, silent fallback отсутствует.

## 3. Выбранный флот
- Выбрать exact fleet через persistent selector.
- Убедиться, что доступны ранние vanilla hulls и late T&R hulls, а не только прежние пять T&R типов.
- Добавить Frigate/Destroyer x1/x3 в выбранный флот.
- Проверить, что корабли добавлены именно в отмеченный флот.
- Проверить состояние, когда все корабли выбранного флота в бою.

## 4. Шаблонный native workflow
- В Ship Designer создать пользовательский template.
- Открыть штатную карточку нужного флота и использовать штатный `+`/очередь строительства.
- Проверить, что именно native workflow предлагает templates.

## 5. Regression
- Army Builder/Designer smoke.
- Regions/Staffing smoke.
- Workspace profiles 90/100/115/130.
