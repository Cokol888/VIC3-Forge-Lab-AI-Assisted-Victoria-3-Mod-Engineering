# beta18-pre2.4 — Fleet Scope Proof & Native Panel Bridge

**Build ID:** `CMP-0.3-B18-PRE2-4-20260821`  
**Parent:** `0.3-beta18-pre2.3`  
**Статус до игры:** STATIC PASS / RUNTIME UNVERIFIED

## Причина hotfix

Runtime beta18-pre2.3 показал, что список собственных флотов формируется корректно, но клик из standalone Workspace не приводит к ожидаемому `GetSelectedFormation`. Одновременно row-level scope probe не подтверждался.

pre2.4 разделяет эти две неизвестные на независимые проверки и больше не предполагает, что `FormationPanel.SelectFormation` доступен из контекста CMP.

## Новый picker contract

Строка флота использует подтверждённый vanilla bridge:

`InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')`

Этот маршрут должен открыть штатную карточку именно того флота, по строке которого нажал пользователь.

CMP не записывает marker и не закрывает picker автоматически.

## Два независимых scope-probe

Для каждой строки отображаются два вертикальных индикатора справа.

### Жёлтый

Проверяет только транспорт объекта из GUI в ScriptedGui:

`MilitaryFormation.MakeScope -> GuiScope.SetRoot -> scripted_gui(scope = military_formation) -> always = yes`

В probe намеренно нет owner, battle-state, fleet-type и других условий.

Если жёлтого индикатора нет, direct `MilitaryFormation.MakeScope` из row context не доказан.

### Синий

На том же root дополнительно проверяет:

`owner = { is_player = yes }`

Если жёлтый есть, а синего нет, сам root передаётся, но owner-resolution не проходит ожидаемый контракт.

## GetSelectedFormation

В pre2.4 `GetSelectedFormation` остаётся только наблюдаемым состоянием. CMP не считает его source of truth, пока runtime не докажет, что открытие штатной карточки из нашего Workspace действительно обновляет этот глобальный accessor.

Поэтому верхние статусы picker отвечают на отдельный вопрос: изменился ли `GetSelectedFormation` после native panel bridge.

## Existing-fleet add-ships

`cmp_fleet_builder_apply_native` сохранён как кандидат и по-прежнему имеет `scope = military_formation`, но его production-кнопка доступна только когда GUI уже сообщает `GetSelectedFormation.IsFleet`.

Внутри ScriptedGui больше нет дублирующей проверки `is_fleet = yes`; остаются:

- владелец = игрок;
- выбран корпус;
- выбрано количество;
- provider/technology gate;
- отсутствие кораблей выбранной formation в бою.

До runtime PASS pre2.4 эта операция не считается доказанной.

## Что не входит

- новый Fleet Composer;
- transfer;
- exact Ship selector;
- flagship;
- supply ship writes;
- retrofit automation;
- persistent CMP fleet marker.

Следующая механика открывается только после доказательства exact fleet context.
