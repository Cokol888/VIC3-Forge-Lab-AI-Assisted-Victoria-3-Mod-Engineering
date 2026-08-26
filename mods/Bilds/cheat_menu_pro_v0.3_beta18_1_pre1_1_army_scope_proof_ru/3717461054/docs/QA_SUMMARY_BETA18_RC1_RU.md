# QA Summary — beta18-RC1 Full Navy Regression

**Build ID:** `CMP-0.3-B18-RC1-20260822`  
**Версия:** `0.3-beta18-RC1`  
**Runtime:** RC1 REGRESSION PENDING

## Release policy

RC1 — функциональная заморозка. Новых gameplay mechanics: **0**.

Core functions pre5/pre5.1 приняты пользователем как рабочие; RC1 повышает требования до полной regression matrix и не считает отдельные basic checks достаточными для Final.

## Frozen Navy surface

- 25 combat hulls;
- Fleet Composer 2.0: 5 rows;
- exact Fleet runtime baseline;
- exact Ship: 100 slots;
- flagship set/unset;
- single transfer;
- batch transfer до 20 Ships;
- native Ship Designer/Retrofit bridge;
- Supply reserve +1/+10/+50/+100;
- assigned Supply read-only diagnostics.

## RC1 static hardening

- `registry/navy18.json` переведён в `beta18-RC1` и содержит 16-part regression matrix;
- stale pre5/pre5.1 candidate wording удаляется из user-facing Navy localization;
- Interface diagnostics больше не читают legacy persistent fleet marker;
- добавлен `tools/validate_beta18_rc1.py`;
- `validate_release.py` вызывает RC1 validator как обязательный gate;
- destructive Ship writes остаются запрещены;
- fake direct ShipTemplate write отсутствует;
- direct Supply assignment к formation отсутствует;
- legacy Fleet Plans source fallback сохранён, но launcher остаётся скрытым.

## Runtime-only gates

Static QA не доказывает:

- фактическое размещение transferred Ships у receiver;
- корректность cross-Fleet batch после тика/save-load;
- native retrofit результата/очереди;
- визуальные значения Supply reserve;
- battle/damaged/destroyed transitions;
- layout/hitboxes в реальном Jomini rendering.

Для этого предназначен `BETA18_RC1_RUNTIME_CHECKLIST_RU.md`.

## Final promotion

`beta18 Final` разрешён только после полного пользовательского Runtime PASS RC1. Final должен быть release/cleanup build, а не новым feature build.

## Результат статического QA RC1

После генерации текущего release-tree:

- `tools/validate_beta18_rc1.py`: **PASS**, 0 errors / 0 warnings;
- `tools/validate_navy18.py`: **PASS**, 0 errors / 0 warnings;
- Registry Coverage: **PASS**;
- Regions Operations: **PASS**;
- Army Final: **PASS**;
- UI/accessibility: **PASS**, 0 errors / 0 warnings;
- full `tools/validate_release.py`: **PASS**, 0 errors / 0 warnings;
- brace-checked GUI/common/event files: **130**;
- unique GUI → ScriptedGui refs: **11 360**, missing 0;
- CMP ScriptedGui → effect refs: **940**, missing 0;
- nested CMP effect refs: **1 276**, missing 0;
- duplicate `cmp_*` definitions: **0**;
- duplicate CMP localization keys: **0**;
- RC1 regression matrix: **16** обязательных групп;
- gameplay additions in RC1: **0**.

Package extraction QA выполняется отдельно после создания ZIP и должен повторить те же gates.

## Feature-freeze verification

Parent `beta18-pre5.1` и RC1 дополнительно сравнены по активным Navy scripted gameplay files. После удаления комментариев и нормализации пробелов semantic differences в 10 Navy SGUI/effect files: **0**. RC1 не меняет саму механику уже принятого Navy surface; изменения относятся к diagnostics, metadata, release gates, локализации и документации.

## Package verification

Финальный RC1 ZIP распаковывается в отдельное чистое дерево и сравнивается с release-tree. Зафиксированный критерий: одинаковое число файлов, `missing = 0`, `extra = 0`, `changed = 0`; после распаковки повторно выполняются deterministic codegen checks, RC1/Navy/Registry/Regions/Army/UI validators и полный `validate_release.py`.
