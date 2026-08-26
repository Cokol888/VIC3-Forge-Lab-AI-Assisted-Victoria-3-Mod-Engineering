# Economy in Global UI Shell — beta15.3

## Scope

beta15.3 migrates the existing Economy 2.0 interface into the shared workspace. It does not change ScriptedGui names, effects, modifier keys, target routing or persistence semantics.

The visible `ECON 2.0` entry and shell navigation both open `cmp_workspace_page = economy`. The old `cmp_economy2_popup` definition remains in the package as an emergency fallback, but no visible button toggles it.

## Inventory preserved

- country target modes: Player, Marked Country and Groups A/B/C;
- four treasury additions and four Investment Pool additions;
- Clear debt, Bankruptcy and Rescue bankruptcy;
- 11 economic modifier parameters;
- nine explicit modifier values from -90% through +500%;
- Apply, Reset selected and Reset all;
- six ownership/investment policy overrides with explicit ON/OFF;
- all existing feedback states.

The shell exposes 46 unique Economy action/selection endpoints. Each endpoint is emitted in all four interface profiles and retains `IsValid` plus `Execute` bindings.

## Layout

The page keeps the shell's fixed header, navigation and feedback footer. Only the selected Economy tab scrolls:

- Money: treasury, Investment Pool, debt and bankruptcy;
- Modifiers: parameter grid, value grid and apply/reset actions;
- Ownership: six readable policy rows with explicit ON/OFF.

Profile reflow rules:

| Profile | Parameter columns | Value columns | Primary control height |
| --- | ---: | ---: | ---: |
| 90% Compact | 3 | 5 | 44 px |
| 100% Standard | 3 | 5 | 48 px |
| 115% Large | 2 | 4 | 52 px |
| 130% Extra large | 2 | 3 | 56 px |

## Static acceptance

- 12 Economy scroll layouts: three tabs × four profiles;
- 46 unique endpoints with full four-profile parity;
- minimum shell text 12 and minimum primary control height 44 px;
- no `elide = right` inside the workspace;
- no visible `Toggle('cmp_economy2_panel')` entry;
- RU/EN localization parity;
- full base-plus-overlay validation passes with zero missing GUI → ScriptedGui references.

## Required in-game QA

Test every tab at 2560×1080 and 3440×1440, with special attention to 130% scrolling, long Russian policy labels, target validity changes, destructive bankruptcy actions and feedback persistence after a game tick.
