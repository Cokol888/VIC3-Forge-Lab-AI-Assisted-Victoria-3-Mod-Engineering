# Next Milestone Gate — beta18.1-pre2.0 Army List Projection Contract

> This is a **next-milestone discovery gate**, not the current Active Gate. The Active Gate remains `beta18.1-pre1.1-army-scope-runtime` until runtime evidence closes it.

## Question

Can Cheat Menu Pro build a self-contained Army picker by composing already evidenced Victoria 3 contracts instead of inventing an undocumented country GUI accessor such as `GetMilitaryFormationsArmy`?

## Evidence before test

### FACT — project-side Army enumeration already exists

The upstream Cheat Menu Pro source already enumerates country military formations with `ordered_military_formation` / `every_military_formation`, filters them with `is_army = yes`, saves exact formation scopes, and stores them in a variable list with `add_to_variable_list`.

Relevant upstream source:

- `events/sakuya_main_04_01_events.txt`
- existing list: `sakuya_main_04_01_marked_army_list`

This proves script-side exact Army scope collection. It does **not** prove a self-contained GUI picker.

### FACT — scope-backed GUI lists are an established 1.13 pattern

The Community Mod Framework 1.13 source uses scope variable lists as GUI data models through `Scope.GetList(...)` and promotes list entries back to typed objects such as `Scope.GetCharacter`.

Its debug GUI also uses `Scope.GetMilitaryFormation` to promote a generic `Scope` to `MilitaryFormation`.

### FACT — 1.13 data-type documentation exposes MilitaryFormation promotion

Victoria 3 1.13 generated data-type documentation exposes both `Scope.AccessMilitaryFormation` and `Scope.GetMilitaryFormation` returning `MilitaryFormation`.

## Hypothesis

A self-contained CMP Army list can be implemented as the following composition:

`country military formations -> is_army filter -> dedicated variable list of exact formation scopes -> GUI Scope.GetList -> Scope.GetMilitaryFormation -> MilitaryFormation row UI`

This is **SUPPORTED COMPOSITION / REQUIRES PROOF**, not an engine fact and not runtime verified.

## Design constraints

1. Do not add or guess `GetMilitaryFormationsArmy` or any symmetric undocumented accessor.
2. Do not reuse `sakuya_main_04_01_marked_army_list` as the new Operations selection contract; it belongs to legacy marker semantics.
3. Use a dedicated Operations-owned diagnostic list if implementation proceeds.
4. Keep beta18 Final Navy semantics untouched.
5. Do not interpret list projection as proof of exact selection, persistence, or readiness semantics.
6. Do not promote the current build beyond `RUNTIME_PENDING` from static evidence.

## Minimal probe

After the current Army Scope Runtime gate is closed, prepare a bounded diagnostic implementation that:

1. refreshes a dedicated Army scope list from the player country;
2. includes only `is_army = yes` military formations;
3. exposes the list to a GUI `dynamicgridbox`/equivalent data model through `GetList(...)`;
4. converts each row scope with `Scope.GetMilitaryFormation`;
5. shows the exact formation name;
6. provides a read-only native-panel open action for that exact row;
7. introduces no Fleet semantics and no amphibious gameplay automation.

## Static PASS condition

- Exact source references resolve.
- No guessed Army-list accessor exists in generated GUI.
- Every row is rooted in `Scope.GetMilitaryFormation`.
- Refresh/list code is isolated under Operations-owned names.
- Existing Navy freeze validator remains PASS.
- No unrelated Army/Navy gameplay effects are changed.

## Runtime PASS condition

1. Player with 0 Armies -> empty/explicit empty state.
2. Player with Army A/B/C -> all expected Armies render exactly once.
3. No Fleet appears in the Army list.
4. Row names match native Army names.
5. Opening Army B opens exactly Army B in the native panel.
6. Creating/removing/reorganizing an Army and refreshing cannot leave a stale/ghost row.
7. `+1 day` smoke does not mutate Armies.
8. Save/load followed by refresh reconstructs valid rows without stale saved targets.
9. Existing exact selected-Army observer remains correct.
10. Frozen beta18 Final Navy regression smoke remains PASS.

## FAIL condition

Any of the following rejects or revises the hypothesis:

- `GetList` cannot expose military-formation scope entries in the CMP GUI context;
- `Scope.GetMilitaryFormation` is invalid for the stored entries;
- list refresh creates persistent stale/ghost formation references;
- exact-row native-panel opening resolves the wrong formation;
- the implementation requires coupling to legacy marked-Army semantics;
- frozen Navy behavior regresses.

## Current status

`CONTRACT_CANDIDATE_READY`

No build/source implementation has been promoted by this document. Runtime proof is still required.
