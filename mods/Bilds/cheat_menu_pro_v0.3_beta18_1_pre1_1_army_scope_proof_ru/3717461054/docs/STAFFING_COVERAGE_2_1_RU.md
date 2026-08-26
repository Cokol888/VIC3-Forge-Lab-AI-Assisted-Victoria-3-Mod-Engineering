# Staffing Coverage 2.1 — beta17-pre3

## Цель

Раздел «Персонал» больше не использует 56-элементный registry операций ADD/SET/REMOVE как каталог кадрового покрытия. Для Staffing введён отдельный `registry/staffing.json`, чтобы кадровые операции могли охватывать employable buildings, которые не должны автоматически становиться целями строительных операций.

## Зафиксированное покрытие

- Всего классифицировано: **132** объекта.
- `SUPPORTED`: **97**.
- `MANUAL`: **5**.
- `UNSUPPORTED`: **30**.
- Профилей кадрового резерва: **14**.
- Все **56** прежних зданий строительного registry сохранены в `SUPPORTED`.
- Все **102** legacy B6 building-selector ID имеют явную coverage-классификацию: поддержка либо документированное исключение.

## Независимая модель выбора

Workspace Staffing использует собственные country markers `cmp_staffing_sel_*` и собственную UI-категорию `cmp_workspace_staffing_category`.

Выбор здания в «Персонале»:

- не меняет выбранное здание в «Операциях»;
- не запускает ADD/SET/REMOVE;
- не очищает строительный selector;
- сохраняет fallback на старые `sakuya_b6_build_sel_*` только для скрытой legacy-панели.

Если задан новый Staffing marker, legacy marker больше не участвует в разрешении цели.

## Новые поддерживаемые классы

Помимо прежних extraction/agriculture/industry/power/infrastructure добавлены профили:

- `government`;
- `education`;
- `military`;
- `services`;
- `arts`;
- `trade`;
- `ownership`;
- `technology`.

В Workspace 97 поддерживаемых зданий распределены по восьми представлениям: `Все`, `Сырьё`, `Промышленность`, `Инфраструктура`, `Государство`, `Военные`, `Услуги`, `Собственность`.

## Профили резерва

Каждый профиль задаёт детерминированную смесь профессий с суммой весов 1000. Старые шесть смесей сохранены без изменения. Новые профили предназначены для создания кадрового резерва соответствующего класса здания, а не для вычисления точного vacancy-vector текущих production methods.

Это принципиальное ограничение: CMP не утверждает, что создаваемая смесь равна текущему штатному расписанию конкретного PM. После добавления резерва штатный hiring-механизм Victoria 3 определяет фактическое заполнение рабочих мест.

## Явно отложенные объекты

`MANUAL` до отдельного workforce/persistence-аудита:

- `building_company_headquarter`;
- `building_company_regional_headquarter`;
- `building_skyscraper`;
- `building_suez_canal`;
- `building_panama_canal`.

Monument/special buildings и Tech & Res helper `building_modern_state_baseline` имеют `UNSUPPORTED` с записанной причиной; они больше не являются молчаливыми пропусками.

## Adaptive Staffing

Режимы `Off / 50 / 75 / 90 / 100%` сохранены. Occupancy gate теперь проверяет весь новый `SUPPORTED` staffing catalog (97 объектов), при этом применяется выбранный профиль только в state, где действительно существует выбранный тип здания.

## QA-контракт

`tools/validate_registry_coverage.py` проверяет:

- разрешённые статусы `SUPPORTED / READ_ONLY / MANUAL / UNSAFE / UNSUPPORTED`;
- уникальность ID и selection markers;
- provider и profile contract;
- сумму весов профилей;
- допустимые pop types;
- обязательную причину для исключений;
- сохранение всех старых 56 поддерживаемых зданий;
- coverage для всех 102 legacy B6 building selectors;
- синхронизацию Build ID.

`tools/generate_staffing2.py --check`, `generate_regions2.py --check` и общий `validate_release.py` включены в release gate.

## Runtime gate

Static PASS не считается игровым PASS. В Victoria 3 требуется проверить минимум:

1. Старое промышленное здание из прежних 56.
2. Университет или государственную администрацию.
3. Военное здание.
4. Manor House / Financial District.
5. Один Tech & Res объект при активном provider.
6. Отсутствие действия на объекте, которого нет в выбранной области.
7. Adaptive 50/90/100%, +1 день и save/load.
8. Независимость выбора «Персонал» от выбора «Операции».
