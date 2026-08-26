# Workspace Shell — beta15.3 Economy migration

## Scope

beta15.3 keeps the shared CMP workspace and migrates Economy 2.0 without changing gameplay effects. Target Center, Economy and Interface Profiles now run inside the shell. Regions & Buildings, Population, Politics and Military remain in the legacy layout until their dedicated migrations.

The shell is deliberately bounded to `1120×660` inside the existing `1200×720` CMP root:

- header: title, current profile and close action;
- left navigation: migrated pages are enabled, pending pages are visibly disabled;
- content viewport: only page content scrolls;
- footer: feedback and destructive cleanup stay reachable while content scrolls.

## Interface profiles

The game-facing safety decision is to avoid an unverified dynamic `scale` binding. `registry/ui_shell.json` defines four profiles and `tools/generate_workspace_shell.py` emits a separate reflowed layout for each one:

| Profile | Density | Text | Primary controls | Target columns |
|---|---:|---:|---:|---:|
| Compact | 90% | 12 pt | 44 px | 5 |
| Standard | 100% | 13 pt | 48 px | 5 |
| Large | 115% | 15 pt | 52 px | 4 |
| Extra large | 130% | 17 pt | 56 px | 3 |

The profile changes immediately through `cmp_ui_scale_profile`. Standard is the default when the variable does not exist.

## Deterministic generation

Regenerate after editing `registry/ui_shell.json`:

`python3 tools/generate_workspace_shell.py`

Check that both the standalone artifact and injected GUI block are current:

`python3 tools/generate_workspace_shell.py --check`

The generated block is delimited by `CMP_WORKSPACE_SHELL_BEGIN/END` in `gui/main/sakuya_main.gui`.

## Static acceptance gates

- exactly four generated profiles;
- minimum workspace `fontsize` and `fontsize_min` of 12;
- minimum primary button height of 44 px;
- no `elide = right` in the workspace;
- no runtime `scale =` binding;
- Target content scroll area exists;
- Economy provides Money, Modifiers and Ownership scroll areas in every profile;
- all 46 Economy action/selection endpoints have four-profile parity;
- footer separator remains outside the scroll area;
- no visible entry point toggles `cmp_target_core_panel`;
- no visible entry point toggles `cmp_economy2_panel`;
- RU/EN key parity for `cmp_workspace`.

## Required in-game QA

1. Test 2560×1080 at the player's normal Victoria 3 UI scale.
2. Open Targets from the top bar and from Economy, Population and Politics.
3. Exercise all eleven target scopes and Groups A/B/C.
4. Open Economy and test Money, Modifiers and Ownership with every supported country target.
5. Switch 90/100/115/130 profiles without closing the shell.
6. Check the 130% Economy scroll reachability and fixed feedback footer.
7. Repeat the smoke test at 3440×1440.
8. Save/load and confirm that gameplay target groups still persist; the visual profile is currently session-scoped.

Full cross-reference validation requires the base `3717461054` snapshot overlaid with this patch.
