# Economy 2.0 — beta13

## Цель
Убрать скрытые Shift/Alt/ПКМ-сценарии из основных экономических операций и разделить:
1. прямые изменения gamestate;
2. постоянные modifiers;
3. ownership/investment policy overrides.

## Цели
Поддерживаются только страновые цели Unified Target Core:
- Игрок;
- отмеченная страна;
- Group A / B / C.

Для областей, персонажа, флота и блока держав Economy 2.0 явно отключается.

## Прямые операции
- Казна: +10 / +25 / +50 / +100% текущего `gold_reserves_limit`.
- Инвестиционный фонд: те же относительные шаги.
- Очистить долг: `clear_debt = yes`.
- Банкротство: очистка долга + `declared_bankruptcy` на 120 месяцев (совместимо с legacy B2 semantics).
- Спасение: снять `declared_bankruptcy` + добавить 100% лимита золотого резерва.

## Параметры
Economy 2.0 управляет отдельными modifiers и не удаляет legacy modifiers CMP:
- government dividends efficiency;
- minting;
- construction goods cost;
- government wages;
- military wages;
- loan interest;
- consumption tax authority cost;
- private construction allocation;
- government dividend reinvestment;
- government dividend waste;
- building throughput.

Значения: -90 / -75 / -50 / -25 / 0 / +25 / +50 / +100 / +500%.

## Найденный legacy mismatch
В исходной B2 элемент, визуально называемый Tax Income, применяет modifier с `country_government_dividends_efficiency_add`. В Economy 2.0 он называется «Эффективность государственных дивидендов».

## Политика собственности
Явные ON/OFF для:
- force privatization;
- foreign collectivization;
- disable non-company privatization;
- disable nationalization;
- disable nationalization without compensation;
- government buildings protected.

## Ограничения runtime
Статический QA может проверить ссылки, modifier keys из исходного CMP, структуру GUI и codegen. Фактическое влияние на бюджет, investment pool и throughput необходимо проверить после игрового тика и save/load.
