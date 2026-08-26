# Search / Filter Discovery — beta17-pre3

## Решение

Статус: **DEFERRED как обязательная зависимость**.

В Victoria 3 1.13.9 в публичном data-type surface появились `SearchBar` и `SearchResult`, а в наборе изменённых GUI присутствует `gui/shared/search_bar.gui`. Однако текущий CMP baseline зафиксирован шире как `1.13.*`, без доказанного минимального требования `>=1.13.9`.

Поэтому beta17-pre3 не делает native SearchBar обязательным для Workspace. Каталоги сохраняют category + scroll, а внедрение поиска откладывается до одного из двух условий:

1. поддерживаемый minimum baseline официально закреплён как `1.13.9+`; или
2. создан собственный compatibility-safe filter без зависимости от нового native data type.

## Следующий gate

При Technology 2.0 повторить discovery и выбрать один результат:

- `NATIVE` — vanilla SearchBar признан безопасным минимумом;
- `CUSTOM` — используется собственный фильтр;
- `DEFERRED` — категории/scroll остаются до следующего compatibility pass.

## Внешняя опора discovery

- Victoria 3 Modding Digests 1.13.9 — `changes_data_types.md` (`SearchBar`, `SearchResult`).
- Victoria 3 Modding Digests 1.13.9 — `changes_files.md` (`gui/shared/search_bar.gui`).
