# QA beta17-pre2.1 — hotfix клика выбора флота

## Подтверждённый runtime-дефект beta17-pre2

Постоянный список `Country.GetMilitaryFormationsFleet` появился и корректно показал собственный флот, но нажатие строки не оставило выбранную цель: после закрытия Workspace по-прежнему отображал «Флот не выбран». Скриншот взаимодействия также показывает штатную карточку военного формирования поверх picker.

## Изменение

- У каждой динамической строки теперь ровно один callback: `cmp_military_target_fleet_select`.
- Самозакрытие picker тем же click-path удалено; закрытие выполняется отдельной кнопкой X.
- Видимое имя строки использует `MilitaryFormation.GetNameNoFormatting`.
- Дочерний textbox имеет `alwaystransparent = yes`, чтобы pointer input не перехватывался текстом.
- После успешного выбора зелёный `cmp_military_target_fleet_entry_selected` marker остаётся видимым внутри picker.
- Backend выбора и морские gameplay effects не менялись.

## Статический QA

- `generate_workspace_shell.py --check`: PASS.
- `validate_ui_accessibility.py`: PASS, 0 ошибок и 0 предупреждений.
- `validate_release.py`: PASS, 0 ошибок.
- 120 GUI/script-файлов: баланс скобок PASS.
- 10 142 уникальных GUI→ScriptedGui ссылок: пропусков 0.
- Release contract требует четыре picker-строки, по одному selection callback, без self-close и с прозрачным unformatted label.

## Runtime gate pre2.1

1. Открыть «Армия и флот → Флот → Выбрать / изменить флот».
2. Нажать строку флота. Picker **не должен закрыться**.
3. Строка должна получить зелёный маркер.
4. Закрыть picker крестиком. В основной строке должно отображаться точное имя флота вместо «Флот не выбран».
5. Повторно открыть picker: та же строка должна оставаться зелёной.
6. Выбрать другой флот, если доступен; зелёный marker должен перейти на него.
7. Нажать «Очистить цель»: статус должен вернуться к «Флот не выбран».
8. Только после этого проверять Fleet Builder/Designer, тик и save/load.

Если шаг 2 не ставит зелёный marker, следующий дефект уже локализуется не в input/close-path, а в передаче `formation` scope в ScriptedGui.
