# QA Summary — Cheat Menu Pro v0.3 beta17 Final RC1

## Статус

**STATIC CANDIDATE.** Полный runtime gate RC1 требуется до beta17 Final.

Build ID: `CMP-0.3-B17-FINAL-RC1-20260820`  
Версия: `0.3-beta17-final-rc1`  
Parent: `0.3-beta17-pre3.1` — user runtime PASS 20.08.2026  
Baseline: Victoria 3 `1.13.*`

## Army Final audit

- Land-unit registry: **26** units.
- Builder amounts: 5; spawn matrix: **130** endpoints.
- Army ScriptedGui definitions: **209**.
- Army scripted-effect definitions: **278**.
- Quick presets: 4.
- Mixed templates: 4 × 392 = **1 568** create branches.
- Designer: 48 configurations; **17 472** create branches.
- Designer zero-mobile configurations: 4.
- Amphibious Builder: 2 verified marine tiers × 4 amounts = **8** branches.
- Army Controls: 10 parameters × 5 values = **50** apply endpoints; 4 presets.
- Stale `cmp_army_control_*_level` variables: **0**.
- Existing-army silent fallback in Army create workflows: **0**.

## Defects corrected during Final audit

1. Mobile quick preset contained two identical `military_drill` conditions, making the second branch unreachable. Normalized to one Dragoons tie-break consistent with mixed/designer templates.
2. Artillery quick preset SGUI omitted `blitzkrieg` although the effect had a Modern Heavy Tank `blitzkrieg` branch. Gate aligned.
3. Army Controls reset code contained 20 dead `*_level` cleanup references for variables never set by the subsystem. Removed.
4. Designer integer rounding was undocumented. Existing 70/30 zero-mobile behavior is now formalized and exhaustively validated.
5. Manifest naming of the fourth control preset is normalized around the actual endpoint `god`, with visible label `Extreme`.

## Provider contract

Tech & Res unit roles and unlock technologies are pinned to the audited `3472248460` source snapshot. No new vanilla unit assumptions were added.

## Required runtime gate

- Builder immediate / +1 day / save-load;
- all quick presets;
- all four mixed templates;
- representative Designer configs including 70/30 zero-mobile;
- Marines coastal positive / inland negative;
- Army Controls self/marked, apply/reset/presets;
- negative technology/target states;
- profiles 90/100/115/130.

Static PASS does not substitute for engine/runtime behavior.
