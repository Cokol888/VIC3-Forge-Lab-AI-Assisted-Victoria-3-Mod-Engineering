# CMP beta11 — Registry / Code Generation

Beta11 вводит декларативный слой данных перед дальнейшим рефакторингом CMP.

- Провайдеры: **3**
- Здания Staffing Assistant: **92**
- Типы сухопутных юнитов: **26**
- Типы кораблей: **25**
- Ресурсы Tech & Res: **8**
- Зарегистрированные операции: **11**

## Что уже генерируется

`cmp_fleet_builder_sgui.txt`, `cmp_fleet_builder_effects.txt`, адаптеры provider detection и строка выбора кораблей в `sakuya_main.gui` генерируются из JSON registry.

Это первый production-путь codegen. Следующий этап (beta12) сможет использовать те же registry для Regions/Buildings/Resources/Staffing.
