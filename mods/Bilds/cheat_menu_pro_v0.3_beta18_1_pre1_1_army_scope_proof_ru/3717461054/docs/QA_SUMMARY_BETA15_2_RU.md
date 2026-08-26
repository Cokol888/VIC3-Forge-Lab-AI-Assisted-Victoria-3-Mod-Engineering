# QA beta15.2 — сводка

Дата проверки: 2026-08-18.

## Пройдено

- целостность JSON: `integration_manifest.json` и все registry-файлы читаются;
- баланс Jomini-скобок: 45 GUI/common-файлов, ошибок нет;
- `generate_registry.py --check`;
- `generate_regions2.py --check`;
- `generate_economy2.py --check`;
- `generate_population2.py --check`;
- `generate_politics2.py --check`;
- `generate_workspace_shell.py --check`;
- `validate_politics2.py`: PASS;
- `validate_ui_accessibility.py`: PASS;
- рабочая область: минимальные `fontsize` / `fontsize_min` равны 12;
- рабочая область: 50 видимых ключей `CMP_WS_*`, пропусков RU/EN нет;
- рабочая область: основные кнопки не ниже 44 пикселей, `elide = right` отсутствует;
- старый `cmp_target_core_panel` больше не открывается видимыми кнопками.

## Заблокировано отсутствующей базой

`python3 tools/validate_release.py` для одного overlay заканчивается со статусом `FAIL`, потому что не может найти 4 610 GUI→ScriptedGui определений из Workshop-базы `3717461054`. Остальные проверки этого запуска прошли; дополнительных ошибок нет.

Для полного статического результата нужно собрать временный каталог `base snapshot + beta15.2 overlay` и выполнить:

`python3 tools/validate_release.py --overlay <каталог_собранного_overlay>`

## Нужна проверка в игре

- рендер и кликабельность при 2560×1080;
- переключение 90/100/115/130 без закрытия окна;
- прокрутка профиля 130% и неподвижность нижней строки;
- все 11 режимов целей и группы A/B/C;
- открытие Центра целей из верхней строки, Экономики, Населения и Политики;
- повторный smoke-test при 3440×1440;
- сохранение/загрузка постоянных групп целей.
