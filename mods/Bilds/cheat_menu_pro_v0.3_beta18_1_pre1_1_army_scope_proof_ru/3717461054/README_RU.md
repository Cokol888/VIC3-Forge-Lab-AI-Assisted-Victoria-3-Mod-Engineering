# Cheat Menu Pro v0.3 beta18.1-pre1 — Military Operations Discovery (RU)

**Build:** `CMP-0.3-B18-1-PRE1-20260823`  
**Parent:** beta18 Final / Navy frozen  
**Scope:** discovery-only, gameplay writes = 0

Новый post-beta18 цикл начат с аудита Marines / Fleet readiness / Naval Invasion. beta18 Navy gameplay surface не меняется. Подробности: `docs/MILITARY_OPERATIONS_DISCOVERY_PRE1_RU.md`.

---

# Cheat Menu Pro v0.3 beta18 Final — Navy Rework (RU)

**Build:** `CMP-0.3-B18-FINAL-20260822`  
**Runtime:** `PASS`  
**Parent:** beta18-RC1 — полный regression подтверждён пользователем

## beta18 Final

- Navy Rework официально выпущен после полного RC1 runtime regression.
- Новых gameplay-механик относительно RC1: **0**.
- Заморожены как Runtime PASS: Fleet Composer 2.0, exact Fleet, add-ships, exact Ship, flagship, single/batch/cross-Fleet transfer, native Retrofit bridge, Supply reserve и assigned-supply diagnostics.
- Ship Templates/Retrofit остаются штатным Victoria 3 workflow без выдуманного direct ShipTemplate write.
- Supply Ships остаются государственным логистическим ресурсом; direct assignment к Fleet не выдумывается.
- Hidden legacy Fleet Plans/fallback source сохранён только для безопасного rollback; production Workspace на него не опирается.
- Amphibious Assistant перенесён в post-beta18 Military Operations.

Документы: `docs/NAVY_BETA18_FINAL_RU.md`, `docs/QA_SUMMARY_BETA18_FINAL_RU.md`, `docs/CHANGELOG_BETA18_FINAL_RU.md`, `docs/ROADMAP_2026-08-22_RU.md`.

---

# Cheat Menu Pro v0.3 beta18-RC1 — Full Navy Regression (RU)

**Build:** `CMP-0.3-B18-RC1-20260822`  
**Runtime:** `RC1_REGRESSION_PENDING`  
**Parent:** beta18-pre5.1 — основные функции приняты, полный regression ещё требуется

## RC1

RC1 не добавляет новые gameplay-механики. Это функциональная заморозка полного Navy Rework перед beta18 Final.

Проверяем единым regression-run: Fleet Composer 2.0, exact Fleet, add-ships, exact Ship, flagship, single/batch/cross-Fleet transfers, native Retrofit bridge, национальный Supply reserve, assigned-supply diagnostics, battle/damaged/lost targets, +1 day, save/load и Workspace 90/100/115/130.

Дополнительно удалены устаревшие pre5 candidate-подсказки, Interface diagnostics больше не зависят от legacy fleet marker, а `tools/validate_beta18_rc1.py` включён в обязательный release gate.

Документы: `docs/NAVY_FULL_REGRESSION_RC1_RU.md`, `docs/BETA18_RC1_RUNTIME_CHECKLIST_RU.md`, `docs/BETA18_RC1_ACCEPTANCE_FORM_RU.md`, `docs/QA_SUMMARY_BETA18_RC1_RU.md`.

---

# Cheat Menu Pro v0.3 beta18-pre5.1 — Retrofit & Naval Logistics (RU)

**Build:** `CMP-0.3-B18-PRE5-1-20260822`  
**Runtime:** `UNVERIFIED`  
**Parent:** beta18-pre5 Exact Ship Transfers — transfer runtime gate ещё требуется

## beta18-pre5.1

- новый Fleet subtab **«Логистика»**;
- native Retrofit bridge: Ship Designer + штатная карточка выбранного Fleet;
- CMP не вызывает `RetrofitShips` и не записывает ShipTemplate напрямую, пока exact Ship CMP не доказан как native `ShipSelection`;
- Supply Ships вынесены в **государственный резерв**, а не маскируются под состав конкретного Fleet;
- безопасные country-actions `+1 / +10 / +50 / +100` через `add_supply_ships`;
- диагностика `supply_ship_maintenance_fulfillment`;
- read-only `num_assigned_supply_ships` для выбранной MilitaryFormation;
- direct Supply assignment к Fleet остаётся DEFERRED;
- Amphibious Assistant перенесён после beta18 Final;
- pre5 transfer сохранён для обязательного runtime regression перед RC1.

Документы: `docs/NAVY_RETROFIT_LOGISTICS_PRE5_1_RU.md`, `docs/BETA18_PRE5_1_RUNTIME_CHECKLIST_RU.md`, `docs/QA_SUMMARY_BETA18_PRE5_1_RU.md`.

---

# Cheat Menu Pro v0.3 beta18-pre5 — Exact Ship Transfers (RU)

**Build:** `CMP-0.3-B18-PRE5-20260822`  
**Runtime:** `UNVERIFIED`  
**Parent:** beta18-pre4 Exact Ship Control & Flagship — Runtime PASS

## beta18-pre5

- одиночная передача exact Ship через `set_ship_owner`;
- transfer basket до 20 exact Ships, в том числе из нескольких source Fleets;
- batch transfer через `set_ship_owner_multiple`;
- обязательный `clear_ownership_transfer_fleet` на source country;
- receiver — отмеченная другая страна с портом;
- destroyed / battle / flagship Ship блокируются;
- beta18-pre4 exact Ship/flagship зафиксирован как Runtime PASS baseline;
- retrofit / amphibious / Supply остаются за следующим runtime gate.

Документы: `docs/NAVY_EXACT_SHIP_TRANSFERS_PRE5_RU.md`, `docs/BETA18_PRE5_RUNTIME_CHECKLIST_RU.md`, `docs/QA_SUMMARY_BETA18_PRE5_RU.md`.

---

# Cheat Menu Pro v0.3 beta18-pre4 — Exact Ship Control & Flagship (RU)

**Build:** `CMP-0.3-B18-PRE4-20260822`  
**Runtime:** `PASS` — подтверждено пользователем  
**Parent:** beta18-pre3 Fleet Composer 2.0 — Runtime PASS

## beta18-pre4

- новый naval subtab **«Корабли»**;
- exact Ship selector: 100 позиций / 5 страниц;
- target хранится на конкретном `ship`, а не на Ship Type;
- диагностика типа, flagship, damage, port, battle, HP и crew bands;
- безопасные exact writes: назначить / снять flagship;
- transfer, damage, kill, crew и supply writes остаются закрыты до следующих gates;
- Fleet Composer 2.0 beta18-pre3 зафиксирован как Runtime PASS baseline.

Документы: `docs/NAVY_EXACT_SHIP_CONTROL_PRE4_RU.md`, `docs/BETA18_PRE4_RUNTIME_CHECKLIST_RU.md`, `docs/QA_SUMMARY_BETA18_PRE4_RU.md`.

---

# Cheat Menu Pro v0.3 beta18-pre3 — Fleet Composer 2.0 (RU)

**Build:** `CMP-0.3-B18-PRE3-20260821`  
**Runtime:** `UNVERIFIED`  
**Parent:** beta18-pre2.4 — Fleet Scope Proof / runtime target-core accepted

## Главное

- Exact Fleet context из beta18-pre2.4 зафиксирован как runtime baseline.
- Новый `Конструктор флота 2.0`: **5 независимых строк**, в каждой любой из **25 combat hulls** и количество `0/1/3/5/10`.
- Одинаковый корпус можно выбрать в нескольких строках — количества должны складываться в одном новом флоте.
- Первая ненулевая строка создаёт fleet formation и сохраняет её как temporary scope; остальные строки добавляют корабли именно в этот новый флот.
- Role presets только заполняют строки и не создают флот автоматически.
- Instant spawn остаётся default-template route; пользовательские Ship Templates — штатный Ship Designer / construction workflow.
- Transfer / exact Ship / flagship / supply / retrofit остаются за следующими gates.

Документация: `docs/NAVY_FLEET_COMPOSER_2_0_PRE3_RU.md`; runtime: `docs/BETA18_PRE3_RUNTIME_CHECKLIST_RU.md`.

---

# Cheat Menu Pro v0.3 beta18-pre2.4 — Fleet Scope Proof & Native Panel Bridge (RU)

**Build ID:** `CMP-0.3-B18-PRE2-4-20260821`  
**Parent:** beta18-pre2.3 Runtime FAIL по native selection из standalone Workspace  
**Runtime:** `UNVERIFIED`

## Главное в beta18-pre2.4

- Строка флота больше не вызывает context-dependent `FormationPanel.SelectFormation`; вместо него используется штатный `InformationPanelBar.OpenMilitaryFormationPanelTab` для exact MilitaryFormation.
- У каждой строки два независимых индикатора: жёлтый доказывает bare `MilitaryFormation.MakeScope -> ScriptedGui(always=yes)`, синий доказывает owner-resolution.
- `GetSelectedFormation` теперь только наблюдается и не считается source of truth до runtime-доказательства.
- Custom CMP fleet marker не возвращён в production Workspace.
- Существующий direct add-ships остаётся candidate-path и тестируется только если native selection реально появится.

Runtime checklist: `docs/BETA18_PRE2_4_RUNTIME_CHECKLIST_RU.md`; architecture: `docs/NAVY_SCOPE_PROOF_PRE2_4_RU.md`; QA: `docs/QA_SUMMARY_BETA18_PRE2_4_RU.md`.

---

# Cheat Menu Pro v0.3 beta18-pre2.3 — Native Fleet Selection & Direct Operations Core (RU)

**Build ID:** `CMP-0.3-B18-PRE2-3-20260821`  
**Parent:** beta18-pre2.2 Runtime FAIL по собственному fleet-target marker  
**Runtime:** `UNVERIFIED`

## Главное в beta18-pre2.3

- CMP больше не использует собственную метку выбранного флота как production source of truth.
- Строка флота вызывает штатный `FormationPanel.SelectFormation`; Workspace читает текущий `GetSelectedFormation`.
- «Добавить корабли» выполняется непосредственно с выбранной `MilitaryFormation` как корневым объектом; повторного поиска marker по всем formations нет.
- Пустой собственный Fleet разрешён как цель первого корабля.
- Если существующий Ship выбранного флота в бою, direct add блокируется.
- Legacy marker/resolver сохранён только как fallback source и не вызывается новым Workspace-route.
- Сохранены 25 combat hulls, 100 catalog endpoints и universal composer на 37 924 состава.

Runtime checklist: `docs/BETA18_PRE2_3_RUNTIME_CHECKLIST_RU.md`; architecture: `docs/NAVY_NATIVE_SELECTION_PRE2_3_RU.md`; QA: `docs/QA_SUMMARY_BETA18_PRE2_3_RU.md`.

---

# Cheat Menu Pro v0.3 beta18-pre2.2 — Fleet Target Core Repair (RU)

**Build ID:** `CMP-0.3-B18-PRE2-2-20260821`  
**Parent:** beta18-pre2.1 Runtime FAIL по exact fleet selection  
**Статус:** Static candidate / runtime selector gate обязателен

## Главное в beta18-pre2.2

- Удалён неработающий путь `country ROOT + AddScope(formation)`.
- Selector теперь выполняет ScriptedGui напрямую с `military_formation` как ROOT.
- Очистка exact fleet marker ограничена флотами текущего владельца, без глобального `every_country`.
- Добавлена runtime-диагностика: formation-root probe, callback received, exact marker written.
- Exact Fleet Resolver и остальная Navy-механика не расширяются до PASS этого gate.

# Cheat Menu Pro v0.3 beta18-pre2.1 — Navy Workflow Repair (RU)

**Build:** `CMP-0.3-B18-PRE2-1-20260821`  
**Runtime:** `UNVERIFIED`  
**Parent:** beta18-pre2 Runtime FAIL/SUPERSEDED

## Что исправлено

- «Смешанный флот» больше не T&R-only: полный каталог распределён по Capital / Cruiser / Torpedo, один hull на группу, количества 0/1/3/5/10.
- До трёх выбранных hulls создаются как **один новый флот**; generated contract содержит 37 924 ненулевых composition branches.
- «Выбранный флот» теперь предлагает все **25** боевых hulls, а exact Fleet Selector beta17 сохранён.
- Мгновенное создание честно обозначено как route с **default template** типа. Пользовательский Ship Template применяется через штатный Ship Designer/строительство Victoria 3.
- Старый верхний раздел «Планы флота» скрыт из основного маршрута; legacy backend сохранён только как fallback.
- Role presets стали era-aware fillers и не выполняют действие автоматически.

Подробнее: `docs/NAVY_WORKFLOW_REPAIR_PRE2_1_RU.md`; runtime: `docs/BETA18_PRE2_1_RUNTIME_CHECKLIST_RU.md`; QA: `docs/QA_SUMMARY_BETA18_PRE2_1_RU.md`.

---

# Cheat Menu Pro v0.3 beta18-pre2 — Full Naval Catalog & Native Ship Designer Bridge (RU)

**Build:** `CMP-0.3-B18-PRE2-20260820`  
**Runtime:** `UNVERIFIED`  
**Parent:** beta18-pre1 architecture spike / beta17 Final released baseline

## Главное в beta18-pre2

- Полный боевой naval catalog: **20 vanilla + 5 Tech & Res hulls**; Supply Ship классифицирован отдельно как `READ_ONLY`.
- В Workspace → Флот теперь три режима: **Корабли и шаблоны / Смешанный флот / Выбранный флот**.
- `Корабли и шаблоны` покрывает всю технологическую линейку 1.13: парусные корабли, ironclads, dreadnoughts, cruisers, carrier, torpedo craft, submarine/destroyer и T&R late-game hulls.
- Категории: **Все / Крупные / Крейсеры / Торпедные / Tech & Res**.
- Фильтр устаревших vanilla-корпусов использует runtime `ShipType.IsObsolete` текущей страны, а не ручную таблицу CMP.
- Для каждого из 25 combat hulls есть bounded создание `x1/x3/x5/x10` → **100 explicit new-fleet branches**. Создаётся отдельная formation в собственной отмеченной портовой области; selected existing fleet не используется.
- Штатный Ship Designer открыт через тот же доказанный entry point, который использует vanilla Military panel: `PopupManager.ToggleShipDesignerPopup`. CMP не пишет ShipTemplate напрямую.
- Модель теперь явно разделена: **Ship Type → Ship Template → Ship → Fleet**.
- Создание из каталога использует штатный/default template корпуса. Выбор конкретного пользовательского template переносится в универсальный Fleet Composer 2.0 после отдельного discovery/runtime gate.
- Проверенный mixed Tech & Res composer pre1 сохранён как compatibility path: **3 124** ненулевых состава → одна formation.
- Exact existing-fleet path beta17 сохранён без hidden fallback.
- Старый Fleet Designer переименован в **«Планировщик состава флота (legacy)»**, чтобы не путать его со штатным Ship Designer.
- Transfer / exact ship selector / flagship / supply assignment / retrofit automation пока не открываются как write-actions.

Подробности: `docs/NAVY_REWORK_PRE2_RU.md`  
Runtime checklist: `docs/BETA18_PRE2_RUNTIME_CHECKLIST_RU.md`  
QA: `docs/QA_SUMMARY_BETA18_PRE2_RU.md`

---

# Cheat Menu Pro v0.3 beta18-pre1 — Navy Architecture & Composition Foundation (RU)

**Первый статический кандидат Navy Rework поверх выпущенной beta17 Final.** Новый маршрут разделяет создание нового смешанного флота и операции над точным выбранным существующим флотом.

## Сделано в beta18-pre1

- Новый `registry/navy18.json` фиксирует five-ship Tech & Res provider contract, ship groups, technologies и coverage/discovery state.
- В `Армия и флот → Флот` появились два режима: **Новый флот** и **Выбранный флот**.
- Новый composition builder задаёт отдельное количество `0/1/3/5/10` для каждого из пяти проверенных типов кораблей.
- Любая смешанная конфигурация создаётся **одним** `create_military_formation` с несколькими `ship` blocks — один состав, один флот.
- Сгенерировано и валидируется **3 124** ненулевых composition branches; hidden existing-fleet fallback отсутствует.
- HQ нового флота берётся из собственной отмеченной области с портом; при нескольких отметках используется highest-GDP port state.
- Пять профилей состава (Escort / Battle / Carrier / Wolfpack / Amphibious Support) только заполняют конструктор и не создают флот автоматически.
- Режим **Выбранный флот** сохраняет beta17 exact Fleet Selector и add-ships compatibility path.
- Transfer / flagship / supply writes / auto-attach не открываются преждевременно и остаются за отдельными beta18 gates.
- Native SearchBar отложен до baseline gate 1.13.9+.
- Полный static release QA: **PASS, 0 errors / 0 warnings**.

Подробности: `docs/NAVY_REWORK_PRE1_RU.md`; QA: `docs/QA_SUMMARY_BETA18_PRE1_RU.md`; runtime: `docs/BETA18_PRE1_RUNTIME_CHECKLIST_RU.md`.

---

# Cheat Menu Pro v0.3 beta17 Final — Army Final accepted (RU)

**Выпущенный baseline.** Пользователь завершил runtime smoke RC1 без критических ошибок, ломающих игру; дерево RC1 принято как beta17 Final без дополнительного gameplay-патча. Army UX 2.0 намеренно отложен до завершения beta18 Navy Rework.

## Сделано в beta17 Final RC1

- Новый `registry/army_final.json` фиксирует Builder, unit priorities, mixed templates, Designer, Marines, Army Controls, provider contract и runtime gates.
- `tools/validate_army_final.py` встроен в общий release validator.
- Проверено 26 типов × 5 количеств = **130** Army Builder spawn endpoints.
- Проверено **1 568** mixed-template branches и **17 472** Designer branches во всех 48 конфигурациях.
- Mobile quick preset избавлен от недостижимой второй `military_drill` ветки; tie-break нормализован на Dragoons для совпадения с generated templates.
- Artillery quick preset SGUI получил отсутствовавший `blitzkrieg` gate.
- Army Controls: 10×5 = **50** apply endpoints + 4 presets; удалены 20 мёртвых `*_level` cleanup refs.
- 10 Tech & Res unit entries сверены с pinned provider snapshot `3472248460`.
- Army create workflows статически запрещены от скрытого выбора существующей formation: они создают новую армию в отмеченной собственной области.
- Parent beta17-pre3.1 зафиксирован как runtime PASS пользователя от 20.08.2026.

Подробности: `docs/ARMY_FINAL_RU.md`; QA: `docs/QA_SUMMARY_BETA17_FINAL_RC1_RU.md`.

Принятое ограничение: созданные battalion slots набирают manpower штатной системой игры; CMP не форсирует население. Multi-unit one-formation Designer и тактические Army Controls profiles перенесены в Army Rework 2.0 после beta18.

---

# Cheat Menu Pro v0.3 beta17-pre3.1 — Regions Operations Coverage & Safety Hotfix (RU)

**Накопительный static-кандидат поверх beta17-pre3.** Сборка расширяет «Области → Операции», добавляет проверку доступности каждого уровня строительства и устраняет конфликт шаблонов, при котором недоступность одного компонента могла блокировать оставшуюся часть шаблона в той же области. Fleet Selector Click Hotfix и Staffing Coverage 2.1 сохранены. Runtime-статус остаётся `UNVERIFIED`.

## Сделано в beta17-pre3.1

- Каталог строительных операций расширен с 56 до **92 SUPPORTED** зданий: 55 vanilla + 37 Tech & Res. Добавлены, в частности, Government Administration, University, Barrack, naval/government объекты, сервисные и дополнительные provider-здания.
- «Операции» используют ту же taxonomy категорий, что и «Персонал»: **Все / Сырьё / Промышленность / Инфраструктура / Госсектор / Военные / Услуги / Собственность**. Game-managed ownership/trade/urban объекты не открываются как прямые строительные операции без безопасного контракта.
- Выбор здания для ADD/SET/REMOVE использует независимые `cmp_regions2_sel_*` markers и не пересекается со Staffing `cmp_staffing_sel_*`. Старый B6 selector сохраняется только как совместимый bridge.
- ADD теперь проверяет каждый следующий уровень: для отсутствующего здания — `can_construct_building`, для существующего — `can_queue_building_levels = 1`. При достижении лимита текущая область останавливается на максимально допустимом уровне и возвращает partial/blocked result.
- SET больше не использует destructive remove → recreate. Если текущий уровень ниже цели, он безопасно повышается пошагово; если равен — считается успешным без пересоздания; если выше — снижение блокируется как `UNSAFE`.
- REMOVE явно означает удаление **всего building type** в области; выбранное количество на эту операцию не влияет.
- Шаблоны выполняются в каждой целевой области отдельно и best-effort по каждому компоненту. Guard `cmp_regions2_state_blocked` теперь сбрасывается перед каждым компонентом, поэтому недоступный Port/Resource-capped объект больше не блокирует Steel/Railway/Power и остальные части того же шаблона.
- Исправлен codegen шаблонов: helper'ы **ADD 15** и **ADD 20** теперь генерируются и проверяются вместе с 1/5/10/25/50/100.
- Release QA расширен nested scripted-effect cross-reference: **881** CMP effect refs проверяются не только на SGUI → effect, но и effect → effect; отсутствующих — 0.
- `tools/validate_regions_operations.py` проверяет 92 building operations, category parity, availability gates, safe SET, whole-building REMOVE, preset amounts, selector isolation и per-component preset isolation.

Подробности: `docs/REGIONS_OPERATIONS_SAFETY_PRE3_1_RU.md`, `docs/QA_SUMMARY_BETA17_PRE3_1_RU.md`.

Runtime gate: проверить государственное здание, resource-capped здание, Port во внутренней области, ADD до лимита, SET вверх/равно/вниз, REMOVE, все четыре шаблона на смешанном наборе областей, затем +1 день и save/load.

---

# Cheat Menu Pro v0.3 beta17-pre3 — Coverage & Diagnostics Foundation (RU)

**Статический кандидат поверх beta17-pre2.1.** Сборка реализует инфраструктурный этап новой дорожной карты: расширяет Staffing, вводит coverage/schema gate, единый Build ID и диагностический слой. Fleet Selector Click Hotfix сохранён без отката, но его пользовательский runtime-gate всё ещё помечен как `UNVERIFIED`.

## Сделано в beta17-pre3

- «Персонал» отделён от 56-элементного registry строительных операций: новый `registry/staffing.json` классифицирует 132 объекта и выводит **97 SUPPORTED** зданий.
- Добавлены государственные, образовательные, военные, сервисные, художественные, торговые, ownership- и technology-профили — всего **14** кадровых профилей.
- Выбор здания в Staffing использует независимые `cmp_staffing_sel_*` markers и больше не меняет выбор ADD/SET/REMOVE.
- Adaptive Staffing `Off/50/75/90/100` переведён на полный 97-объектный supported catalog.
- Введён общий coverage contract: `SUPPORTED / READ_ONLY / MANUAL / UNSAFE / UNSUPPORTED`; все 102 legacy B6 building selectors имеют явную классификацию.
- `tools/validate_registry_coverage.py` проверяет schema/coverage, provider, профили, веса профессий, причины исключения и сохранение прежних 56 supported buildings.
- Единый Build ID `CMP-0.3-B17-PRE3-20260820` генерируется из `registry/build.json`; устранён старый beta16 tag в UI registry.
- В «Интерфейсе» добавлена компактная диагностика Build ID / baseline / runtime status / exact fleet target.
- Военная отчётность нормализована: 267 registered/reused endpoints, 253 audited Workspace ScriptedGui refs, 123 executable Workspace actions; старая неоднозначная метрика 239 объявлена deprecated.
- Native SearchBar пока не включён в обязательный UX: discovery зафиксирован как `DEFERRED`, пока minimum baseline не подтверждён как Victoria 3 1.13.9+.

Подробности: `docs/STAFFING_COVERAGE_2_1_RU.md`, `docs/COVERAGE_DIAGNOSTICS_FOUNDATION_RU.md`, `docs/SEARCH_FILTER_DISCOVERY_BETA17_PRE3_RU.md`.

Runtime gate: сначала подтвердить унаследованный Fleet Selector Click Hotfix, затем проверить новый Staffing на vanilla/Tech & Res зданиях, независимость selectors, Adaptive Staffing, +1 день и save/load.

---

# Cheat Menu Pro v0.3 beta17-pre2.1 — hotfix клика выбора флота (RU)

**Накопительный hotfix поверх beta17-pre2.** Runtime-тест подтвердил, что постоянный список флотов рендерится корректно, но нажатие строки не сохраняет выбранную цель.

## Исправлено в beta17-pre2.1

- У строки флота оставлен ровно один `onclick`: выполнение `cmp_military_target_fleet_select`. Автоматическое закрытие picker тем же кликом удалено.
- Живое имя строки переключено с `MilitaryFormation.GetNameNoIcon` на `MilitaryFormation.GetNameNoFormatting`, чтобы не создавать форматированную интерактивную ссылку поверх кнопки.
- Текст строки сделан `alwaystransparent = yes`, поэтому pointer input принадлежит родительской кнопке выбора.
- После успешного выбора picker намеренно остаётся открыт: выбранная строка должна получить зелёный маркер; список закрывается отдельным крестиком. Это делает runtime-результат выбора наблюдаемым.
- Release-gate теперь отклоняет возврат двух callback в одной строке, самозакрытие строки, непрозрачный label и форматированное имя в picker.
- Gameplay-эффект выбора, точный маркер `cmp_military_target_fleet`, Fleet Builder/Designer и морские операции не изменялись.

Runtime gate: выбрать строку → увидеть зелёную отметку → закрыть picker → в основной строке должно остаться точное имя флота.

QA: `docs/QA_SUMMARY_BETA17_PRE2_1_RU.md`.

---

# Cheat Menu Pro v0.3 beta17-pre2 — постоянный выбор флота (RU)

**Накопительный предварительный overlay для Workshop-мода `3717461054`.** Эта сборка устраняет неочевидную логику выбора флота в Workspace и уточняет, какие цели используют армейские операции.

## Сделано в beta17-pre2

- Удалено одноразовое событийное окно beta17-pre1: оно выглядело как операция и закрывалось сразу после выбора.
- Добавлен постоянный прокручиваемый список **всех собственных флотов прямо в Workspace** с живыми игровыми названиями и без ограничения в шестнадцать элементов.
- После выбора точное название цели остаётся в строке управления; выбранная строка подсвечивается зелёным.
- Выбор флота теперь только назначает цель; он ничего не создаёт и не изменяет до нажатия отдельной кнопки операции.
- Вкладки «Флот» и «Планы флота» используют общую строку **«Выбрать / изменить» / «Очистить цель»** и три явных состояния: цели нет, цель готова, все корабли цели в бою.
- Сборщик кораблей, пресеты, конструктор флота и десантная группа разрешают действие только для объекта с точным постоянным маркером.
- Удалён скрытый выбор первого подходящего элемента из старого списка; старый список сохраняется только как совместимый мост для исходных операций CMP.
- Уничтожение выбранного флота автоматически делает цель недействительной; очистка целей удаляет и новый маркер, и старый список.
- Для армии явно разделены контексты: сборщик и шаблоны создают новое формирование в отмеченной собственной области, а «Параметры армии» воздействуют на вооружённые силы выбранной страны.
- Детерминированная генерация, RU/EN-паритет и четыре профиля 90/100/115/130 проверяются обновлённым release-gate.

Подробности: `docs/MILITARY_TARGET_UX_RU.md`; QA: `docs/QA_SUMMARY_BETA17_PRE2_RU.md`.

---

# Cheat Menu Pro v0.3 beta16 Final — «Дипломатия и суверенитет» приняты (RU)

**Принятый накопительный overlay для Workshop-мода `3717461054`.** Полный runtime-чек-лист beta16 успешно пройден в Victoria 3 19 августа 2026 года. Финализация меняет только release-документацию и метаданные: GUI, ScriptedGui, локализация и игровая механика побайтово сохранены от протестированной beta16-pre2.1.

## Принято в beta16 Final

- Локализация Fleet Builder корректно загружается после полного перезапуска игры; сырые ключи `CMP_FLEET_*` в проверенном маршруте не отображаются.
- Вкладка «Планы флота» и соседняя морская локализация работают без замеченной регрессии.
- Обе экспертные операции вступления в блок держав и их отрицательные исходы работают в проверенном runtime-маршруте.
- Сброс одноразового подтверждения, поведение после игрового такта и сохранение/загрузка прошли пользовательскую приёмку.
- Все 60 аудированных действий «Дипломатии и суверенитета» сохраняют контракт beta16-pre2.
- Обычное приглашение, выход, принципы и рычаги влияния намеренно остаются отложенными.
- Полный статический base-plus-overlay QA остаётся PASS: 0 ошибок и 0 предупреждений.

Runtime- и static-доказательства: `docs/QA_SUMMARY_BETA16_FINAL_RU.md`.

---

# Cheat Menu Pro v0.3 beta16-pre2.1 — исправление локализации флота (RU)

**Накопительный предварительный overlay для Workshop-мода `3717461054`.** Hotfix восстанавливает все подписи `CMP_FLEET_*` во вкладке «Флот» и сохраняет игровой контракт beta16-pre2 без изменений.

## Исправлено в beta16-pre2.1

- Удалён дублирующий UTF-8 BOM из русского и английского файлов Fleet Builder.
- Заголовки `l_russian:` и `l_english:` снова являются первой декодированной строкой, поэтому Victoria 3 загружает все 42 ключа флота/десантной группы для каждого языка.
- Добавлен release-gate: ровно один UTF-8 BOM и правильный языковой заголовок проверяются во всех 32 активных RU/EN-файлах локализации.
- Геометрия интерфейса, ScriptedGui-endpoint’ы и игровые эффекты не изменялись.

QA: `docs/QA_SUMMARY_BETA16_PRE2_1_RU.md`.

## Унаследовано от beta16-pre2

- Добавлены два явно подписанных экспертных действия: принудительно включить державу игрока или отмеченную страну в отмеченный блок.
- Перед действиями требуется одноразовое подтверждение; оно сбрасывается после операции, смены вкладки, очистки результата или закрытия Workspace.
- Страна должна находиться вне любого блока; успех выводится только после фактической проверки членства.
- Отдельно сообщаются отсутствие блока, отсутствие страны, уже существующее членство и отклонённая движком команда.
- Сохранены четыре проверенных действия со сплочённостью и все 58 операций beta16-pre1 — всего 60 аудированных действий.
- Обычное приглашение, выход, принципы и рычаги влияния остаются отложенными. Старые кнопки «пригласить» скрыты, поскольку фактически выполняют прямое вступление.
- Справка RU/EN объясняет обход обычного влияния, согласия и сроков, а также DLC-, слотовые и временные ограничения отложенных механик.

Подробности: `docs/DIPLOMACY_SOVEREIGNTY_2_RU.md`; QA beta16-pre2: `docs/QA_SUMMARY_BETA16_PRE2_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.8 — сведение Workspace (RU)

**Накопительный overlay для Workshop-мода `3717461054`.** beta15.8 сводит завершённую миграцию рабочей области в единый UI/UX-контракт без изменения игровых эффектов.

## Сделано в beta15.8

- В старом меню оставлена ровно одна видимая точка входа: **«РАБОЧАЯ ОБЛАСТЬ»**.
- Во все профили 90/100/115/130 добавлен общий каталог справки с маршрутами к семи разделам.
- Добавлен явный **«Сброс»** навигации, справочных слоёв, вкладок и фильтров списков.
- «Сброс» сохраняет профиль интерфейса, игровые цели, выбранные параметры ScriptedGui и результаты операций.
- Закрытие Workspace унифицировано на существующей команде `close_window`; неподтверждённые пользовательские сочетания не добавлялись.
- Расширены детерминированные проверки точки входа, заголовка, маршрутов справки, безопасного сброса, закрытия, локализации и доступности.
- Все прежние панели сохранены в исходниках как аварийный резерв; каталог `common/` побайтово совпадает с принятой beta15.7.

Подробности: `docs/WORKSPACE_CONVERGENCE_RU.md`; QA: `docs/QA_SUMMARY_BETA15_8_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.7 — «Армия и флот» в Workspace (RU)

**Накопительный overlay для Workshop-мода `3717461054`.** beta15.7 переносит существующие сборщики, шаблоны и параметры армии/флота в общую рабочую область без изменения игровых эффектов.

## Сделано в beta15.7

- Пункт **«Армия и флот»** включён во всех четырёх профилях 90/100/115/130.
- Добавлены пять верхних поверхностей: **«Армия» / «Шаблоны армии» / «Параметры армии» / «Флот» / «Шаблоны флота»**.
- Сгенерированы 44 компоновки с прокруткой только содержимого и 32 закрепляемые справочные компоновки.
- Повторно использованы 267 существующих военных ScriptedGui-точек с детерминированной паритетностью четырёх профилей.
- Все 26 типов сухопутных войск распределены по фильтрам «Пехота и морпехи», «Артиллерия», «Кавалерия и бронетехника».
- Для сокращаемых подписей войск и кораблей доступны полные локализованные названия и требования исследований в подсказках.
- В общую навигацию сведены сборщик армии, быстрые/смешанные/настраиваемые шаблоны, морпехи, армейские параметры, сборщик флота, конструктор флота и подготовка десанта.
- Требования исследований, отмеченных областей/флота, доступности вне боя и результат остаются явными.
- Ручное прикрепление созданной армии к флоту постоянно обозначено как следующий шаг в обычном интерфейсе игры.
- Старые панели армии и флота сохранены как аварийный резерв; каталог `common/` побайтово совпадает с принятой beta15.6.

Подробности: `docs/MILITARY_IN_SHELL_RU.md`; QA: `docs/QA_SUMMARY_BETA15_7_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.6 — «Политика и персонажи» в Workspace (RU)

**Накопительный overlay для Workshop-мода `3717461054`.** beta15.6 переносит существующую механику «Политики и персонажей 2.0» в общую рабочую область без изменения игровых эффектов.

## Сделано в beta15.6

- Пункт **«Политика»** включён во всех четырёх профилях 90/100/115/130.
- Добавлены пять поверхностей с независимой прокруткой: **«Правительство» / «Персонажи» / «Группы» / «Законы» / «Блок»**.
- Состояние требуемой цели меняется по контексту активной вкладки; навигация и результат остаются закреплёнными.
- Все 86 уникальных точек выбора и действий перенесены с полной паритетностью четырёх профилей.
- Длинные описания вынесены в составные подсказки и 24 прокручиваемые справочные компоновки.
- Постоянные предупреждения сохранены для удаления военных ролей, прямого изменения принятия законов и относительной природы политической силы.
- Результат последней операции и его очистка встроены в закреплённую нижнюю строку.
- Отдельная кнопка старой панели Politics удалена; сама панель остаётся в исходниках как аварийный резерв.
- Каталог `common/` побайтово совпадает с принятой beta15.5.1.

Подробности: `docs/POLITICS_IN_SHELL_RU.md`; QA: `docs/QA_SUMMARY_BETA15_6_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.5.1 — фильтр категорий зданий (RU)

**Накопительный hotfix для Workshop-мода `3717461054`.** beta15.5.1 добавляет категории в списки зданий «Областей и сооружений 2.0», не меняя игровые эффекты beta15.5.

## Сделано в beta15.5.1

- Добавлен раскрывающийся селектор: Все / Добыча / Аграрные / Лёгкая промышленность / Тяжёлая промышленность / Энергетика / Инфраструктура.
- Один фильтр используется в «Операциях» и «Персонале» и сохраняется до конца игровой сессии.
- Все 56 зданий распределены по категориям без пропусков и дубликатов.
- Смена категории не сбрасывает выбранное здание, операцию, значение или результат.
- Ресурсный список не фильтруется, поскольку это отдельная уже сокращённая выборка.
- Категории и раскрывающиеся меню сгенерированы для профилей 90/100/115/130.
- Добавлены RU/EN-подсказки с назначением и количеством объектов каждой категории.
- Расширен regression-gate распределения, компоновок, селекторов и endpoint-паритетности.

Подробности: `docs/BUILDING_CATEGORIES_RU.md`; QA: `docs/QA_SUMMARY_BETA15_5_1_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.5 — «Население и общество» в Workspace (RU)

**Накопительный overlay для Workshop-мода `3717461054`.** beta15.5 переносит существующую механику «Население и общество 2.0» в общую рабочую область без изменения игровых эффектов.

## Сделано в beta15.5

- Пункт **«Население»** включён во всех четырёх профилях 90/100/115/130.
- Добавлены четыре поверхности с независимой прокруткой: **«Население» / «Профессии» / «Благосостояние» / «Общество»**.
- Цель-область, навигация и результат закреплены; прокручивается только содержимое активной вкладки.
- Все 59 уникальных endpoint’ов выбора и действий перенесены с полной паритетностью профилей.
- Длинные описания убраны из постоянного слоя в составные подсказки и пять закрепляемых справочных карточек на профиль.
- Подтверждение массовой смены культуры/религии и постоянное предупреждение об опасном действии сохранены.
- Результат последней операции отображается в закреплённой нижней строке.
- Старая панель Population 2.0 сохранена как аварийный резерв.
- Добавлены проверки вкладок, endpoint-контрактов, справки, локализации, размеров контролов и переполнения.

Подробности: `docs/POPULATION_IN_SHELL_RU.md`; QA: `docs/QA_SUMMARY_BETA15_5_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.4 — «Области и сооружения» в Workspace (RU)

**Накопительный overlay для Workshop-мода `3717461054`.** beta15.4 переносит «Области и сооружения 2.0» и кадрового помощника в общую рабочую область без изменения игровых эффектов.

## Сделано в beta15.4

- Пункт **«Области»** включён в навигацию всех четырёх профилей 90/100/115/130.
- Добавлены отдельные поверхности **«Операции» / «Персонал»**.
- Для 56 зданий и 19 ресурсных объектов сделаны двухколоночные прокручиваемые списки; настройки и целевые кнопки остаются закреплёнными.
- Полное локализованное название каждого сокращённого элемента доступно в hover-подсказке.
- Перенесены ADD/SET/REMOVE зданий, ADD/SET/CLEAR ресурсов, четыре шаблона, шесть размеров кадрового резерва и пять режимов занятости.
- Опасное предупреждение точной операции `Задать` всегда видно рядом с настройками.
- Для каждого профиля добавлены пять закрепляемых прокручиваемых тем справки и нижняя строка результата Regions/Staffing.
- Старая панель Regions сохранена как аварийный резерв.
- Добавлены проверки профильной паритетности, endpoint-контрактов, подсказок, локализации и переполнения.

Подробности: `docs/REGIONS_IN_SHELL_RU.md`; QA: `docs/QA_SUMMARY_BETA15_4_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.3.1.1 — Interface Text Hotfix (RU)

**Накопительный overlay для Workshop-мода `3717461054`.** beta15.3.1.1 устраняет последнее подтверждённое переполнение текста на странице «Интерфейс», не меняя механику и геометрию остальных страниц.

## Исправлено в beta15.3.1.1

- Длинная техническая строка больше не выводится постоянно и не выходит за правую границу рабочей области.
- На странице остаётся короткая инструкция по выбору плотности интерфейса.
- Кнопка `i` открывает составную tooltip-подсказку и закрепляемую прокручиваемую справочную карточку.
- Отдельная справочная компоновка генерируется для профилей 90/100/115/130.
- При закрытии рабочей области открытая справка корректно сбрасывается.
- Добавлен regression-gate, запрещающий возвращать длинные технические описания в постоянный слой страницы.

QA: `docs/QA_SUMMARY_BETA15_3_1_1_RU.md`.

## Унаследовано от beta15.3.1

- Старый фиксированный tray целей полностью удалён; вместо него оставлена одна кнопка **«РАБОЧАЯ ОБЛАСТЬ»**.
- Отдельная кнопка `ЭКОНОМИКА 2.0` в старом интерфейсе удалена, поэтому справа больше нет независимого переполняющего элемента.
- В Economy Shell длинные описания заменены короткими видимыми подписями; полный смысл перенесён в составные hover-подсказки.
- Добавлены четыре закрепляемые справочные карточки: обзор, деньги, модификаторы, собственность. Каждая карточка прокручивается и генерируется для профилей 90/100/115/130.
- Активная цель, необходимость выбрать цель и результат последней операции по-прежнему видимы без наведения.
- Техническая строка миграции убрана из нижней части левой навигации.
- Экономические эффекты, значения, цели и правила постоянства не изменялись.

QA: `docs/QA_SUMMARY_BETA15_3_1_RU.md`.

## Унаследовано от beta15.3

- Пункт **«Экономика»** включён в навигацию Shell; разделы «Деньги», «Модификаторы» и «Собственность» перенесены в общую область содержимого.
- Для профилей 90/100/115/130 генерируются отдельные Economy-компоновки: 12 прокручиваемых разделов и 46 уникальных endpoint’ов с полной паритетностью.
- Статус страновой цели и переход в Центр целей находятся внутри страницы экономики.
- Результат последней операции отображается в закреплённой нижней строке Shell.
- Видимая кнопка `ECON 2.0` теперь открывает Shell; прежнее окно оставлено в файлах как аварийный fallback.
- Без изменения игровой механики сохранены 11 параметров, 9 значений, 6 политик, 8 операций казны/инвестфонда и 3 операции долга/банкротства.

Подробности: `docs/ECONOMY_IN_SHELL_RU.md`; QA: `docs/QA_SUMMARY_BETA15_3_RU.md`.

## Унаследованное исправление beta15.2.1

- Восстановлены все 5 387 строк `common/scripted_guis/sakuya_cheat_b4_sgui.txt`: beta15.2 обрывалась посреди команды и теряла последние 1 029 строк.
- Сохранены оба завершающих вызова `clear_ownership_transfer_fleet` для Victoria 3 1.13.
- Добавлен `baseline_manifest.json` для проверенного поддерева `529340/3717461054`.
- Полная проверка базы с overlay завершена успешно: 10 127 GUI-ссылок, 106 GUI/common-файлов, отсутствующие ScriptedGui-определения и ошибки не обнаружены.

Подробности: `docs/QA_SUMMARY_BETA15_2_1_RU.md`.

## Унаследовано от beta15.2

В beta15.2 появился общий каркас, в который перенесены Центр целей и профили интерфейса. Экономика, Области, Население, Политика, Армия и Флот пока доступны через прежнее меню до своих отдельных этапов миграции.

## Что сделано в beta15.2

- Добавлена рабочая область `1120×660`: постоянная шапка, левое меню, прокручиваемая область содержимого и закреплённая нижняя строка результата.
- Центр целей заново собран внутри общей области: видимый текст не меньше 12 пунктов, основные кнопки высотой `44–56 пикселей`, главные подписи не обрезаются через `elide = right`.
- Работают четыре профиля перестроения: **90% Компактный / 100% Обычный / 115% Крупный / 130% Очень крупный**. Для каждого профиля генератор создаёт отдельную геометрию; непроверенное динамическое масштабирование корневого элемента не используется.
- В рабочей области появилась страница **«Интерфейс»** для мгновенного переключения профиля.
- Старое окно целей сохранено в пакете как аварийный запасной вариант, но все видимые точки входа теперь открывают новую рабочую область.
- Добавлены `registry/ui_shell.json`, детерминированная проверка `tools/generate_workspace_shell.py --check`, RU/EN parity и отдельные accessibility-проверки каркаса.

## Текущие границы

- Это **основа каркаса**, а не завершение всей миграции beta15.2. Отключённые пункты слева показывают страницы, которые ещё предстоит перенести.
- Для полной проверки ссылок GUI→ScriptedGui нужен локальный snapshot базового Workshop-мода. Проверка одного overlay не может разрешить определения, принадлежащие базе.
- Геометрию, кликабельность и переполнение всё ещё необходимо проверить в Victoria 3 при 2560×1080 и 3440×1440.

Подробности: `docs/WORKSPACE_SHELL_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.1 — UI Accessibility Rework (RU)

**Накопительный hotfix поверх beta15, основанный на реальном тесте интерфейса при игровом разрешении 2560×1080.** Механики Politics 2.0, Population 2.0, Economy 2.0, Army/Fleet Builders и предыдущих beta сохранены.

## Главное в beta15.1

- **2560×1080 закреплено как основной layout-target**, 3440×1440 — как вторичный ultrawide-профиль.
- **Экономика 2.0 полностью переразложена:** вместо одной плотной таблицы теперь три крупные вкладки — **Деньги / Модификаторы / Собственность**. Окно увеличено до `1040×700`, цель и основные действия стали заметнее.
- Значения экономических модификаторов больше не идут одной длинной строкой из микрокнопок: они разбиты на две строки с крупными зонами клика.
- **Политика 2.0** увеличена до `912×642`; шрифты и управляющие элементы масштабированы без изменения механики.
- **Fleet Builder:** кнопки выбора кораблей увеличены до `268×48`, двухколоночная раскладка сохранена.
- **Army/Fleet:** выполнен второй accessibility-pass; основные подписи и контролы заметно крупнее.
- **Population 2.0:** увеличена типографика и минимальный размер читаемого текста.
- RU-проверка расширена на Economy/Politics/Population/Army/Fleet: валидатор ловит не только отсутствующие ключи, но и оставшийся технический английский текст.
- Старые/Legacy CMP-функции пока не удаляются: их полный механический и текстовый реинжиниринг остаётся отдельной фазой Vanilla Rework после основных этапов roadmap.

## Что обязательно проверить в игре

1. Открыть **Экономика 2.0** при 2560×1080 и проверить, читается ли основной текст без напряжения и не обрезаются ли русские подписи.
2. Переключить все три вкладки Economy 2.0 и проверить расположение кнопок при используемом UI Scale.
3. Открыть **Политика 2.0**, **Население 2.0**, Army Builder и Fleet Builder; обратить внимание на размеры основных кнопок и scroll-area.
4. Если возможно, сделать скриншот Economy 2.0 и одного из Military-экранов — это даст объективный следующий runtime-pass.

Подробный стандарт: `docs/UI_ACCESSIBILITY_RU.md`.

---

# Cheat Menu Pro v0.3 beta15 — Politics & Characters 2.0 (RU)

**Накопительный релиз поверх Workshop-мода `3717461054`.** Включает beta1–beta14.

## Главное в beta15

- Новый единый контроллер **«Политика 2.0»** поверх legacy B3/B5/B9: Правительство / Персонажи / Группы интересов / Законы / Блок держав.
- Страновые действия работают через Target Core: Игрок / отмеченная страна / Group A/B/C; неверный тип цели больше не является silent no-op.
- Правительство: легитимность, authority, bureaucracy, influence и точный уровень 1–5 для семи существующих институтов.
- Персонажи: бессмертие, явные бонусы здоровья/популярности, ранг командира, роли General/Admiral, быстрые traits. Биологический возраст намеренно read-only: безопасный direct SET-age не подтверждён.
- IG: approval и **political strength** с честным пояснением, что это не фиксированный clout.
- Законы: +10/+25% checkpoint, следующая фаза, setback, немедленно принять, отменить, очистить enactment modifiers.
- Power Bloc: в новый безопасный слой пока перенесена только cohesion; membership/principles/leverage ждут Vanilla Rework.
- Сохраняется accessibility-стандарт beta14: 2560×1080 основной профиль, 3440×1440 второй профиль, крупные контролы, RU/EN parity.
- Добавлен первый системный **Vanilla Rework Audit Seed**: старые функции CMP будем проверять по цепочке `label → tooltip → SGUI → effect/modifier → scope → persistence → результат после тика/save-load`.

Подробности: `docs/POLITICS_2_RU.md` и `docs/VANILLA_REWORK_AUDIT_SEED_RU.md`.

---

# Cheat Menu Pro v0.3 beta14 — Population & Society + UI Accessibility (RU)

**Текущий накопительный релиз.** Накладывается на копию Workshop-мода `3717461054` и включает все предыдущие функции beta1–beta13.

## Главное в beta14

- Новый крупный интерфейс **«Население и общество 2.0»** с четырьмя страницами: Население, Профессии, Благосостояние, Общество.
- Базовая статическая цель верстки: **2560×1080**; вторичная ultrawide-проверка: **3440×1440**. Реальный рендер всё равно необходимо проверить в самой Victoria 3.
- Fleet Builder переразложен: пять кораблей теперь идут двумя колонками с кнопками `268×44`, основные Army/Fleet/Population шрифты имеют минимальный размер не ниже 10.
- Для Army/Fleet/Population введён отдельный аудит локализации: наличие ключа, RU/EN parity и поиск оставшихся английских видимых строк.
- Старый плотный POP-интерфейс CMP сохранён как **«Старый POP-интерфейс»** и доступен отдельной кнопкой.
- Population 2.0 использует только явные state-targets из Target Core: отмеченные свои области, все инкорпорированные области или отмеченные иностранные области.
- Поддержаны добавление/удаление населения, точная грамотность, профессиональные когорты, квалификации, богатство, лоялисты/радикалы, миграция, доля работающих взрослых, подтверждаемая ассимиляция/религиозная конверсия и три массовых пресета.

Подробности: `docs/POPULATION_2_RU.md` и `docs/UI_ACCESSIBILITY_RU.md`.

---


Накопительный патч для Workshop-мода 3717461054. Включает beta10 и все предыдущие этапы интеграции.

## Новое
- Конструктор собственного смешанного шаблона: размер 25 / 50 / 75 / 100 батальонов.
- Доля пехоты: 40 / 50 / 60 / 70%; артиллерии: 10 / 20 / 30%; мобильные войска получают остаток до 100%.
- Для каждой роли выбирается лучший поддерживаемый тип, технология которого уже изучена. Создание использует только явные unit_type ветки, без недокументированной динамической подстановки.
- Новый «Конструктор морской пехоты»: 5 / 10 / 25 / 50 батальонов, только в отмеченной своей области с портом. Поддержаны проверенные T&R Modern Marines ($amphibious_warfare$) и Advanced Marines ($high_performance_apparel$).
- Исправлен bug автоподбора beta5/6: T&R Modern Heavy Tank относится к artillery group, а Modern Light Tanks — к cavalry/mobile group. Quick presets и mixed templates теперь соблюдают эти группы.

## Ограничение по vanilla Marines
Victoria 3 1.13 добавила отдельные low/mid/high Marine tiers, а Tech & Res действительно ссылается на их IDs. Но точные текущие unlocking_technologies ванильных tier'ов отсутствуют в переданном архиве и не найдены в актуальной публичной script documentation. Поэтому beta7 их не спавнит, чтобы не обходить технологический прогресс.

## Проверка в игре
1. Отметьте свою область.
2. Military → Конструктор армии → «Конструктор шаблона».
3. Размер 50 → Пехота 50% → Артиллерия 20% → создать. Ожидаемый состав: 25 / 10 / 15 батальонов по ролям.
4. Проверьте типы ролей: после Blitzkrieg мобильная роль должна выбрать Modern Light Tanks, а не Modern Heavy Tank.
5. Для морпехов отметьте область с портом, выберите 10 → создать.
6. Промотайте день, затем save/load и проверьте manpower / organization / сохранность formation.

Автоматическое прикрепление морской formation к флоту пока не выполняется: в 1.13 это поддерживается игровой механикой, но безопасный публичный scripted effect для attach-to-fleet не подтверждён.


## v0.3 beta8 — Fleet Builder / десантная группа

Вкладка «Конструктор армии» расширена вниз и теперь содержит конструктор флота. Он работает с уже отмеченным собственным флотом CMP и использует штатный эффект Victoria 3 1.13 `create_ship`. В первой безопасной версии доступны только пять корпусов Tech & Res, для которых unlock-технологии подтверждены непосредственно в исходниках мода: Modern Destroyer (`modern_naval_doctrine`), Modern Cruiser / Modern Battleship (`modern_battleships`), Modern Carrier (`integrated_naval_air_tactics`), Modern Submarine (`nuclear_submarine`).

Доступны количества +1/+3/+5/+10 и четыре пресета: эскортная, боевая, авианосная и подводная группы. Технология проверяется и в UI, и повторно внутри effect. Начиная с beta17-pre1 Workspace принимает только один флот с точным маркером и не выбирает первый элемент старого списка.

«Десантная оперативная группа» использует выбранное в Marine Builder количество морпехов, создаёт в отмеченном флоте все доступные проверенные корабли поддержки (эсминцы, крейсера/линкор, при наличии технологии авианосец), затем создаёт all-Marine formation в отмеченной портовой области. Автоматическое прикрепление армии к флоту не выполняется: в проверенной публичной 1.13 script documentation не найден безопасный attach-effect, поэтому последний шаг выполняется штатным UI игры.

### Runtime test
1. Отметьте один свой флот через существующий CMP Navy selector.
2. Откройте Military → Конструктор армии → Конструктор флота.
3. Выберите открытый технологиями тип корабля и +1, нажмите «Добавить корабли».
4. Проверьте состав флота сразу, через сутки и после save/load.
5. Выберите количество морпехов выше в Amphibious Builder, отметьте свою портовую область и нажмите «Подготовить десантную группу».
6. Проверьте появление кораблей поддержки и отдельной all-Marine formation, после чего прикрепите её к флоту штатным UI.


## v0.3-beta9 — Конструктор шаблона флота

Добавлен настраиваемый Fleet Template Designer: размер 10/20/40 кораблей, доля охранения 20/40/60%, авианосцев 0/10/20%, подлодок 0/20/40%. Остаток формирует линейные силы и делится между современными крейсерами и линкорами.

Пять профилей: Линейный флот, Авианосная ударная, Эскорт конвоев, Волчья стая, Десантный флот. Профиль только заполняет параметры; финальное создание остаётся отдельной кнопкой. Все роли повторно проверяют технологии перед `create_ship`.


## v0.3-beta10 — Единый контроллер целей

Нажмите **«ЦЕЛИ»** в верхней строке CMP. Откроется центральный Target Controller с активным контекстом: игрок, отмеченная страна, группы A/B/C, свои отмеченные области, все инкорпорированные области, чужие отмеченные области, персонаж, флот или блок держав.

Группы A/B/C — постоянные: отметьте страну стандартным CMP-маркером и нажмите «Вкл/выкл A/B/C». Членство хранится в gamestate и рассчитано на сохранение/загрузку. Одна страна может входить в несколько групп.

Кнопка «Очистить временные отметки» очищает страну, чужие области, персонажа, блок держав и списки выбранных армий/флотов. Метки своих областей через decree и группы A/B/C намеренно сохраняются.

Важно: beta10 создаёт **ядро**, а не мгновенно переписывает все старые страницы CMP. Новые системы будут использовать этот контекст сразу, а legacy-страницы мигрируют поэтапно, чтобы не ломать проверенные механики.

## v0.3-beta11 — Registry + Code Generation Foundation

Beta11 вводит декларативные registry (`registry/*.json`) для провайдеров, 56 зданий Staffing Assistant, 26 сухопутных юнитов, 5 кораблей, 8 ресурсов Tech & Res и каталога операций.

Fleet Builder теперь является первым production-блоком, который **не поддерживается вручную**: его scripted GUI, scripted effects, provider adapters и строка выбора кораблей внутри `sakuya_main.gui` генерируются `tools/generate_registry.py`.

Для проверки генерации:

`python3 tools/generate_registry.py --check`

Для полного статического теста нужен overlay оригинального 3717461054 + патча:

`python3 tools/validate_release.py --overlay <путь>`

Подробная схема находится в `docs/REGISTRY_ARCHITECTURE_RU.md`.

### Для игрока

Новых обязательных действий в интерфейсе beta11 не добавляет: Fleet Builder должен вести себя как в beta10. Изменение архитектурное и предназначено для того, чтобы beta12+ расширялись без ручного копирования сотен однотипных Jomini-веток.

## v0.3-beta12 — Regions & Buildings 2.0

Во вкладке B6 `Персонал` теперь есть явный переключатель **Персонал / Операции**.

### Операции
- **Здание → ДОБАВИТЬ**: увеличивает текущий уровень на 1/5/10/25/50/100 без удаления существующего здания. Точная ветка генерируется для текущих уровней 0–300; выше 300 операция не угадывает результат и показывает ограничение.
- **Здание → ЗАДАТЬ**: выставляет точный уровень 1/5/10/25/50/100 через `remove_building` → `create_building`. Это точная операция, но она может сбросить состояние самого объекта здания (PM, владение, денежные резервы и т.п.), поэтому используется осознанно.
- **Здание → УДАЛИТЬ**: удаляет выбранный тип здания и проверяет, что его уровень стал 0.
- **Ресурс → ДОБАВИТЬ**: увеличивает resource potential.
- **Ресурс → ЗАДАТЬ**: пересоздаёт resource potential с выбранным точным значением.
- **Ресурс → ОЧИСТИТЬ**: удаляет potential.
- Для ресурсов Tech & Res `ЗАДАТЬ` дополнительно синхронизирует geology trait, если выбранное число точно совпадает с зарегистрированным tier. Для нестандартных чисел trait не придумывается. Специализированная панель T&R остаётся главным способом выставить полный набор геологических tier'ов.

### Региональные шаблоны
- Промышленный центр
- Тяжёлая промышленность
- Военная промышленность
- Инфраструктурный узел

Шаблоны используют ADD-семантику, то есть стараются сохранить существующее состояние зданий вместо полного пересоздания.

### Adaptive Staffing
У Staffing Assistant появился порог фактической занятости: **Выкл. / <50% / <75% / <90% / <100%**. В адаптивном режиме кадровый резерв создаётся только в тех целевых областях, где выбранное предприятие реально существует и его `occupancy` ниже порога. Размер кадрового резерва и временный +500% hiring-attractiveness работают как раньше.

Важно: adaptive staffing использует реальную итоговую занятость здания, но распределение создаваемых профессий пока остаётся registry-profile based. Публичный scripting surface 1.13 не предоставляет точный числовой vacancy-vector по профессиям активных PM, поэтому beta12 не выдаёт приблизительный профиль за точный PM-calculation.

### Проверка в игре
1. Выберите существующий Steel Mill уровня 10 в отмеченной области → Операции → Здание → ДОБАВИТЬ 5. Ожидается уровень 15 без пересоздания.
2. На том же здании → ЗАДАТЬ 5. Ожидается точный уровень 5; после этого проверьте PM/ownership/reserves, потому что SET намеренно пересоздаёт объект.
3. Выберите Copper Mine → Ресурс → ЗАДАТЬ 25. Ожидается copper potential 25 + соответствующий T&R geology trait.
4. Выберите нестандартное для T&R значение, например Copper 100. Потенциал должен быть 100, geology trait не должен ложно назначаться.
5. Staffing → порог <90% → +1K → отмеченная область. При occupancy >=90% действие должно сообщить, что подходящего предприятия ниже порога нет; при occupancy <90% должен появиться кадровый резерв.
6. После каждого сценария промотайте день и сделайте save/load.

Подробности: `docs/REGIONS_BUILDINGS_2_RU.md`.
