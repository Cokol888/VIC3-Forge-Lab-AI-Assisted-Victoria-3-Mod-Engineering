# Coverage & Diagnostics Foundation — beta17-pre3

## Build Identity

Единственный источник версии — `registry/build.json`.

Текущая идентичность:

- Version: `0.3-beta17-pre3`
- Build ID: `CMP-0.3-B17-PRE3-20260820`
- Baseline: `Victoria 3 1.13.*`
- Parent: `0.3-beta17-pre2.1`
- Runtime status: `UNVERIFIED`
- Fleet gate: `INHERITED_PRE2.1_RUNTIME_PENDING`

`tools/generate_build_identity.py` синхронизирует version/build ID в `registry/ui_shell.json`, `integration_manifest.json` и RU/EN build-localization. Release gate проверяет отсутствие рассинхронизации.

## Universal Coverage Contract

`registry/coverage.json` закрепляет общий словарь:

- `SUPPORTED` — маршрут реализован и входит в обычный supported surface;
- `READ_ONLY` — объект доступен только для просмотра/диагностики;
- `MANUAL` — безопасный автоматизированный endpoint не принят, требуется штатный шаг;
- `UNSAFE` — операция технически возможна, но требует отдельного risk contract;
- `UNSUPPORTED` — объект или операция намеренно не поддерживается; причина обязательна.

Цель контракта — заменить молчаливое отсутствие объекта из registry явным инженерным статусом.

## Runtime Diagnostics

Страница «Интерфейс» получила компактный диагностический блок, показывающий:

- Build ID;
- baseline Victoria;
- runtime-статус сборки;
- состояние exact fleet target (`готов` / `не выбран`).

Диагностика является наблюдаемостью, а не доказательством runtime PASS.

## Военная метрика 267 / 239

Старая документация смешивала разные определения. В beta17-pre3 метрика нормализована:

- **267** — historical registered/reused military endpoints из release-каталога;
- **253** — уникальные ScriptedGui references в одном сгенерированном военном Workspace profile;
- **123** — уникальные executable Workspace action endpoints в одном профиле.

Старая цифра **239** объявлена deprecated: она больше не публикуется как конкурирующая «итоговая» метрика без определения.

Паритет всех четырёх профилей проверяется отдельно accessibility/release validator.

## Ограничение выпуска

beta17-pre3 — статический кандидат. Он наследует Fleet Selector Click Hotfix из beta17-pre2.1, но не утверждает, что fleet runtime gate уже пройден. До пользовательского runtime PASS статус Build ID остаётся `UNVERIFIED`.
