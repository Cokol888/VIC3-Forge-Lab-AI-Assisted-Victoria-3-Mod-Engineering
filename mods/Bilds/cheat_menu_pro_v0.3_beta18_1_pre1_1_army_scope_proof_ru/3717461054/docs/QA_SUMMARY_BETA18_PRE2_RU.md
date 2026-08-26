# Cheat Menu Pro v0.3 beta18-pre2 — QA Summary

**Build ID:** `CMP-0.3-B18-PRE2-20260820`  
**Версия:** `0.3-beta18-pre2`  
**Parent:** `0.3-beta18-pre1`  
**Runtime status:** `UNVERIFIED`  
**Статический статус:** `PASS`

## Объём beta18-pre2

- Полный боевой Naval Catalog: **25 hulls** — 20 vanilla + 5 Tech & Res.
- Группы: **9 Capital / 10 Cruiser / 6 Torpedo Craft**.
- Supply Ship: отдельный `READ_ONLY` объект до supply-workflow discovery.
- Каталожное создание нового флота: **25 × 4 = 100** explicit endpoints (`x1/x3/x5/x10`).
- Compatibility mixed composer beta18-pre1: **3 124 / 3 124** ненулевых комбинаций сохранены.
- Native Ship Designer bridge: `PopupManager.ToggleShipDesignerPopup`; CMP не пишет ShipTemplate напрямую.
- Obsolete filter для vanilla: `ShipType.IsObsolete(GetPlayer)`.
- Exact selected-fleet workflow beta17 сохранён как отдельный режим.

## Release QA

По `QA_REPORT.json` и повторным targeted gates:

- status: **PASS**;
- errors: **0**;
- warnings: **0**;
- brace-checked GUI/common/event files: **124**;
- unique GUI → ScriptedGui refs: **10 714**, missing **0**;
- CMP ScriptedGui → effect refs: **682**, missing **0**;
- nested CMP effect → effect refs: **1 015**, missing **0**;
- duplicate `cmp_*` definitions: **0**;
- duplicate CMP localization keys: **0**;
- Navy18 validator: **PASS**;
- Army Final regression validator: **PASS**;
- Regions Operations validator: **PASS**;
- Registry Coverage validator: **PASS**;
- UI/accessibility static validator: **PASS**;
- Workspace profiles 90/100/115/130: static parity **PASS**;
- deterministic build/navy/catalog/workspace codegen: **PASS**.

## Источник vanilla naval contract

Vanilla ship IDs/groups/technology/modification contract закреплён по публичному extract `game/common/ship_types/00_ship_types.txt`, blob SHA:

`0831a667153396240093b3967b1191a58bafa2f5`

Окончательным доказательством поведения остаётся runtime Victoria 3.

## Runtime gate

Сборка **не является beta18-pre2 Runtime PASS**, пока не проверены:

1. ранние vanilla hulls в каталоге;
2. категории и obsolete toggle;
3. открытие штатного Ship Designer из CMP;
4. x1/x3/x5/x10 на нескольких технологических эпохах;
5. закрытые технологии / отсутствующий T&R provider / отсутствие подходящего порта;
6. compatibility mixed composer;
7. exact selected-fleet mode;
8. +1 день и save/load;
9. Workspace 90/100/115/130 в реальном рендере.

Подробный сценарий: `docs/BETA18_PRE2_RUNTIME_CHECKLIST_RU.md`.
