# Changelog — beta18 Final

## Release

`CMP-0.3-B18-FINAL-20260822`

beta18 Final завершает Navy Rework, начатый после beta17 Final.

## Основные изменения beta18

### Naval architecture

- переход от старой unit-like модели к Victoria 3 1.13 `Ship Type → Ship Template → Ship → Fleet`;
- полный combat catalog: 20 vanilla + 5 Tech & Res;
- отдельная классификация Supply Ships;
- native Ship Designer bridge.

### Fleet creation

- ранние, средние и поздние корабли доступны через единый каталог;
- Fleet Composer 2.0: 5 произвольных rows × 25 hulls;
- duplicate hull rows;
- один mixed Fleet вместо нескольких formation;
- role presets работают как fillers, а не как немедленное выполнение.

### Existing Fleet

- несколько итераций selector-а заменены доказанным direct `MilitaryFormation` context;
- native Fleet panel bridge;
- add-ships к точному Fleet;
- устранён production dependency от legacy persistent fleet marker.

### Exact Ship

- exact Ship selector;
- Ship-level diagnostics;
- flagship set/unset;
- lost-target safety.

### Ownership transfer

- single exact Ship transfer;
- batch transfer до 20 Ships;
- cross-Fleet basket;
- receiver and ship-state safety gates;
- ownership-transfer fleet cleanup.

### Retrofit

- пользовательские Ship Templates остаются штатным workflow;
- CMP открывает Ship Designer и exact Fleet panel;
- direct template-write не выдумывается.

### Logistics

- Supply Ships исправлены как country-level reserve;
- `+1/+10/+50/+100`;
- maintenance diagnostics;
- assigned-supply read-only diagnostics.

## RC1 → Final

- новых gameplay-механик: **0**;
- RC1 full runtime regression: **PASS**, подтверждено пользователем;
- metadata/runtime statuses повышены до Final/Runtime PASS;
- добавлен semantic freeze manifest;
- добавлен `tools/validate_beta18_final.py`;
- release gate переключён с RC1 candidate validator на Final validator;
- актуализированы README, audit, roadmap и release docs;
- hidden legacy fallback сохранён только для rollback safety.
