# beta18-RC1 — Freeze Diff against beta18-pre5.1

RC1 объявлен feature-freeze build.

Сравнение активных Navy scripted gameplay files с parent `beta18-pre5.1` выполнено после удаления комментариев и нормализации пробелов.

Результат:

- сравнено Navy `common/scripted_effects` + `common/scripted_guis`: **10 файлов**;
- semantic gameplay differences: **0**;
- новые gameplay mechanics: **0**.

RC1 меняет главным образом:

- build/registry metadata;
- user-facing RC wording;
- Interface diagnostics (удалена зависимость статуса от legacy Fleet marker);
- release validators;
- QA/runtime documentation;
- roadmap.

Таким образом RC1 предназначен для проверки и стабилизации уже принятого Navy surface, а не для расширения механик.
