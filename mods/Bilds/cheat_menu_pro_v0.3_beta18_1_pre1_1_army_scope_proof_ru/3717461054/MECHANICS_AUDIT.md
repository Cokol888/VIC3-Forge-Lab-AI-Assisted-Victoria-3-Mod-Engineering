# v0.3 beta7 mechanics audit

- Public 1.13 script docs support create_military_formation with multiple combat_unit blocks.
- 1.13 added has_port_state and Marines; all-Marine formations can be attached to fleets in gameplay.
- No public can_build-combat-unit trigger was found in 1.13.9 triggers.log; therefore technology gates remain explicit.
- Designer uses 48 bounded size/share configurations and 17472 explicit technology/unit branches.
- Amphibious Builder uses only T&R Marine tiers whose unlocking_technologies are present in the supplied Tech & Res files.
- Corrected T&R group mapping: combat_unit_type_modern_heavy_tank -> combat_unit_group_artillery; combat_unit_type_modern_light_tanks -> combat_unit_group_cavalry.
- Automatic fleet attachment is not implemented because a safe public scripted attach effect was not confirmed.
- Runtime validation is still required.


## beta8 naval audit
- Victoria 3 1.13 separates `ship` from `combat_unit`; Fleet Builder therefore uses `create_ship`, not combat-unit creation.
- `create_ship` requires an existing `fleet` scope, so beta8 targets the existing CMP marked-navy list instead of fabricating an unreferenced empty fleet.
- Verified Tech & Res ship gates: modern destroyer → `modern_naval_doctrine`; modern cruiser/battleship → `modern_battleships`; modern carrier → `integrated_naval_air_tactics`; modern submarine → `nuclear_submarine`.
- The task-force workflow prepares ships + Marines but deliberately does not claim automatic attachment.
- Runtime validation is still required for instant ship initialization, readiness/crew behavior, and save/load persistence.


## beta10 Target Core Audit

- Active target mode is persisted on the player country.
- Country groups A/B/C are persisted as membership variables on country scopes.
- Group toggle requires a normal marked country and reports add/remove/no-target explicitly.
- Group clear falls back to Player if the cleared group was active.
- Transient clear deliberately does not remove own-state decree marks or A/B/C membership.
- Target validity is evaluated live by scripted GUI; stale target modes are visibly invalid instead of silently executing.
- This beta establishes the core only; legacy action pages remain on their original target routing until migrated.

## Beta11 — Registry / codegen audit

- Registry source of truth added for providers, buildings, resources, land units, ships and operations.
- Fleet Builder migrated to deterministic generation for scripted GUI, scripted effects and its ship-selector GUI block.
- Provider adapters are based on the actual exported detection triggers `community_framework_is_active` and `technres_is_active`.
- Source validation against the supplied Tech & Res files confirms all 5 registered ship types, all 10 registered Tech & Res land units, all 8 resource buildings and all referenced geology traits.
- Generated Fleet Builder still uses explicit technology gates before every create batch; registry migration does not relax technology restrictions.
- Full overlay cross-reference result: 0 missing GUI → ScriptedGui references.
- No runtime semantics were intentionally changed in Fleet Builder beyond adding provider-presence gates; runtime regression remains required in Victoria 3.

## Beta12 — Regions & Buildings 2.0 audit

- Current 1.13.9 generated script docs confirm `create_building level=N` uses `max(existing, scripted)` when the building already exists; it is not exact SET semantics.
- Exact Building SET is therefore implemented as `remove_building` followed by `create_building`, with a UI warning that PM/ownership/reserves can be reset.
- Building ADD uses generated exact current-level branches (0–300) and verifies the resulting state building level. Values above the safety ceiling are reported instead of silently approximated.
- Resource ADD/SET/CLEAR use the current 1.13 resource-potential effects. Existence after ADD/SET and absence after CLEAR are verified where the public trigger surface permits it.
- Tech & Res resource SET clears old registered geology traits and assigns a new one only when the selected value exactly equals a registered tier. ADD deliberately leaves geology traits unchanged.
- Adaptive Staffing uses the real building-scope `occupancy` trigger and only spawns a reserve below the selected threshold.
- Exact per-profession PM vacancy counts are not exposed by the inspected public 1.13.9 scripting surface; profession creation therefore remains registry-profile based and is explicitly labelled as such.
- Regions2 and Adaptive Staffing are generated from registry/config by `tools/generate_regions2.py`; `--check` passes deterministically.
- Full original 3717461054 + beta12 overlay: 0 missing GUI → ScriptedGui references and 0 missing CMP ScriptedGui → effect references.
- Runtime validation remains required for PM/ownership/reserve behavior after exact SET, resource potential values, occupancy gating, and save/load persistence.


## Beta13 — Economy 2.0 audit

- Economy 2.0 separates direct gamestate operations (treasury/investment pool/debt/bankruptcy) from persistent modifiers and ownership policy switches.
- New economy actions route through Target Core country modes: player, marked country, and groups A/B/C. Non-country target modes are invalid instead of silently executing.
- The legacy label “Tax Income” was found to drive `country_government_dividends_efficiency_add`; Economy 2.0 labels this mechanic as government dividends efficiency.
- Economy2 codegen is deterministic and legacy Economy remains available for regression comparison.


## Beta14 — Population & UI accessibility audit

- 1.13.9 effect docs confirm direct population operations used here: `set_pop_literacy`, `set_pop_qualifications`, `set_pop_wealth`, `change_pop_culture`, `change_pop_religion`, `kill_population_in_state`, and state loyalist/radical effects.
- Population 2.0 accepts state target modes only and preserves the original dense POP page as Legacy UI.
- Destructive culture/religion mass actions require an explicit confirmation flag.
- Migration and working-adult share are isolated Population 2.0 state modifiers and can be cleared without touching unrelated CMP/game modifiers.
- UI Accessibility static gates: 2560×1080 primary, 3440×1440 secondary; Army/Fleet minimum font and fallback font >=10, Population primary font >=11/fallback >=10.
- Fleet ship selector is generated as two columns with 268×44 buttons.
- Visible RU/EN audit covers Fleet Builder/Designer, Army Builder/Designer/Mixed/UX, and Population 2.0; key parity and untranslated-English detection pass.
- Static QA cannot verify actual Jomini rendering, UI scale, mouse hitboxes, or clipping; runtime screenshots/tests remain required.

## Beta15 — Politics & Characters 2.0 audit

- Politics2 consolidates new safe controls over legacy B3/B5/B9 without deleting legacy functions.
- Country operations route through Target Core Player / Marked Country / Group A/B/C and reject non-country targets.
- Government modifiers are isolated `cmp_politics2_*` modifiers; reset does not remove legacy CMP modifiers.
- Institution level operations affect only countries that already own the selected institution.
- Character health/popularity are explicitly labelled modifier bonuses, not exact SET operations. Immortality, commander rank, roles and quick traits use direct character effects.
- Biological age is read-only: no safe direct SET-age effect was confirmed in the inspected 1.13.x surface.
- IG approval and political-strength operations are separated; UI explicitly avoids calling political-strength multipliers a fixed clout value.
- Law operations target only active enactments; group targets skip ineligible countries instead of silently failing the whole batch.
- Power Bloc migration is deliberately limited to cohesion; membership/principles/leverage remain legacy until destructive-semantics audit.
- `docs/VANILLA_REWORK_AUDIT_SEED_RU.md` starts the post-roadmap legacy audit and records already confirmed misleading semantics such as B2 `Tax Income` -> government dividends efficiency.



## v0.3 beta15.1 — UI Accessibility Rework

- Runtime feedback at 2560×1080 showed beta14/15 2.0 panels were still too dense despite passing the original static font gate.
- Economy 2.0 is now a three-tab master/detail-style panel (Money / Modifiers / Ownership) instead of one dense matrix.
- Politics 2.0, Population 2.0 and Army/Fleet receive a second typography/control-size pass.
- Fleet ship selector remains two-column but grows to 268×48 controls.
- Static layout validation is treated as necessary but insufficient; real Jomini pixel rendering remains a runtime release gate.
- No game mechanics were intentionally changed in this hotfix; it is a presentation/accessibility rework on top of beta15.

## beta17-pre3.1 — Regions Operations Coverage & Safety audit

- The beta12 destructive exact-SET contract is superseded for the new Workspace route: SET now raises/equal only and blocks lowering as `UNSAFE`; `remove_building` is reserved for explicit whole-building REMOVE.
- Building ADD checks every next level using state-scope `can_construct_building` for absent buildings and building-scope `can_queue_building_levels = 1` for existing buildings.
- Direct Operations coverage expands to 92 buildings while the full 132-object building inventory remains explicitly classified by coverage status.
- Operations and Staffing use disjoint selection variables; legacy B6 selectors remain a compatibility bridge only.
- Presets are per-state, per-component best effort. A blocked component no longer poisons later components because `cmp_regions2_state_blocked` resets before every preset building while aggregate root result flags persist.
- Preset-only deltas 15 and 20 are generated explicitly; nested CMP effect -> effect references are now a release-level cross-reference gate.
- Static QA can prove reference integrity and declared guards, but runtime tests remain required for actual engine cap behavior, state placement restrictions, result feedback, tick and save/load.

## v0.3 beta17 Final RC1 — Army Final audit

- Parent `beta17-pre3.1` is the accepted runtime baseline. RC1 isolates the Army Final audit and keeps Navy Final as a separate beta18 domain.
- Army Builder is audited as an explicit create-new-formation workflow: 26 registered land unit types x 5 amounts = 130 spawn endpoints. The destination is the marked owned state selected by the existing GDP-ordered state resolver; Army Final does not silently operate on an arbitrary existing formation.
- Quick presets use deterministic role priority and explicit technology gates. A duplicated `military_drill` mobile branch was removed; generated mobile presets now consistently prefer Dragoons over Cuirassiers at that shared unlock. The artillery preset SGUI now exposes the existing `blitzkrieg` branch for Tech & Res Modern Heavy Tanks.
- Mixed templates contain 1,568 explicit technology/unit branches across four presets. Army Designer contains 17,472 branches across 48 bounded size/share configurations. Counts, role sums, uniqueness and unlock gates are statically validated.
- Designer rounding is now an explicit contract: configurations with a mobile remainder floor infantry/artillery and assign the remainder to mobile; zero-mobile 70/30 layouts preserve the existing half-even infantry rounding and assign the remainder to artillery.
- Amphibious Builder exposes 8 create branches (2 Tech & Res Marine tiers x 4 amounts), requires the marked state to have a port, and does not claim unsupported automatic fleet attachment.
- Army Controls expose 10 parameters x 5 values = 50 apply endpoints for Player or one marked country. Twenty dead `_level` cleanup-variable references were removed because those variables are never written by the current control system.
- Tech & Res Army mappings are pinned to the supplied Workshop 3472248460 provider snapshot. The audit verifies the registered roles/groups/unlock technologies against three hashed provider source files before accepting the registry contract.
- `tools/validate_army_final.py` is part of the release gate and checks Builder, quick presets, mixed templates, Designer, Marines, Controls, target isolation, technology gates, provider hashes and absence of hidden existing-formation fallbacks.
- RC1 remains `UNVERIFIED` until runtime Army tests cover representative Builder/preset/designer/marine/control paths immediately, after +1 day and after save/load on Workspace profiles 90/100/115/130.

## beta18-pre1 — Navy Architecture & Composition Foundation

- Beta17 Final accepted by user as released baseline; no critical game-breaking runtime defects were reported.
- Victoria 3 1.13 standalone ship model is treated as the beta18 source model: new fleets are created with `create_military_formation = { type = fleet ... ship = { ... } }` rather than modelling ships as combat units.
- `registry/navy18.json` pins five verified Tech & Res ship types, ship groups, unlock technologies, flagship capability, modification-slot counts and provider snapshot hashes.
- New-fleet composition uses five independent counts `0/1/3/5/10`; all 3,124 non-zero combinations are explicitly generated and validated.
- Every combination produces exactly one fleet formation containing every selected non-zero `ship` block. The new-fleet path never resolves `cmp_military_target_fleet` and never falls back to a first eligible existing fleet.
- New fleet HQ is resolved from the highest-GDP marked owned state with a port, mirroring the proven marked-state/HQ pattern used by Army creation while adding ownership/port guards.
- Composition presets populate state only and do not create immediately. User review/edit remains possible before the separate create action.
- Existing exact-fleet add-ships remains a compatibility surface. Ownership transfer, supply-ship writes, flagship writes and automatic amphibious attachment are not exposed in pre1.
- Full vanilla ship catalog remains `DISCOVERY_REQUIRED`: the supplied Workshop snapshot does not pin the complete base-game ship-type definitions, so pre1 does not invent IDs or unlock gates.
- Native SearchBar remains deferred because the documented SearchBar/SearchResult surface enters in Victoria 3 1.13.9 while the mod baseline remains 1.13.*.
- `tools/validate_navy18.py` is a mandatory release gate; full static QA passes with 0 errors / 0 warnings. Runtime mixed-fleet, technology, port, +1 day and save/load validation remains required.


## beta18-pre2 — Full Naval Catalog & Native Designer Bridge

- Full combat catalog: 20 vanilla + 5 Tech & Res hulls; Supply Ship = READ_ONLY.
- Source snapshot for vanilla 00_ship_types: blob `0831a667153396240093b3967b1191a58bafa2f5`.
- Native Ship Designer bridge uses proven vanilla `PopupManager.ToggleShipDesignerPopup`; no direct ShipTemplate writes by CMP.
- 25 × 4 = 100 bounded new-fleet creation endpoints.
- Vanilla obsolete visibility delegates to runtime `ShipType.IsObsolete(GetPlayer)`.
- pre1 mixed T&R composer remains 3,124/3,124 combinations.
- Existing-fleet exact target remains isolated from new-fleet catalog creation.
- Transfers, flagship and supply writes remain deferred.


## beta18-pre3 — Fleet Composer 2.0

- beta18-pre2.4 exact Fleet row scope/native panel bridge: Runtime PASS baseline.
- 5 arbitrary composition rows × 25 combat hulls × amounts 0/1/3/5/10.
- Anchor creation: 500 bounded `create_military_formation` branches.
- `save_temporary_scope_as = cmp_navy18_comp2_new_fleet` captures the exact newly-created Fleet.
- Non-anchor rows use `create_ship` only against that temporary Fleet scope; no legacy fleet marker/resolver.
- Duplicate hull rows allowed; runtime must prove additive result.
- Presets are composition fillers only.
- Custom ShipTemplate remains native/manual; no guessed template argument.
- Transfers / exact Ship / flagship / supply writes remain deferred.


## beta18-pre4 — Exact Ship Control & Flagship

- beta18-pre3 Fleet Composer 2.0: Runtime PASS.
- Exact Ship candidate uses `ordered_scope_ship`, non-destroyed filter and `power_projection` ordering.
- Selected exact object receives `cmp_navy18_exact_ship_target` on Ship scope.
- 100 slot selectors / five UI pages.
- Diagnostics: type, flagship, damage, port, battle, HP band, crew band.
- `set_as_flagship = yes/no` enabled only as exact-ship writes.
- transfer / kill / damage / crew / supply writes remain deferred.


## beta18-pre5.1 — Retrofit & Naval Logistics audit

- Retrofit is implemented as a native UI bridge, not as an invented script write. Victoria 3 exposes ShipTemplate/ShipSelection and native Retrofit commands, but CMP exact Ship markers are not assumed to equal native ShipSelection.
- Workspace exposes the proven native Ship Designer entry and selected-Fleet panel route; the user completes Change Template / Retrofit in Victoria 3 native ship workflow.
- Supply Ships are treated as a country-level reserve because `add_supply_ships` is a country effect; CMP exposes only positive bounded increments 1/10/50/100.
- `supply_ship_maintenance_fulfillment` is used for national logistics diagnostics.
- `num_assigned_supply_ships` is read from MilitaryFormation only; no unproven direct assignment write exists.
- Amphibious Assistant is explicitly deferred past beta18 Final and removed from the Navy RC blocker list.
- beta18-pre5 transfer remains runtime-unverified and must pass regression together with pre5.1 before Navy RC1 promotion.


## beta18-RC1 — Full Navy Regression audit

- RC1 is a gameplay feature freeze: `new_gameplay_mechanics = 0`.
- Accepted foundations are retained: exact MilitaryFormation row scope, Fleet Composer 2.0, exact Ship and flagship.
- User reported core pre5/pre5.1 functions working; RC1 expands acceptance to single/batch/cross-Fleet transfer, retrofit bridge, Supply reserve/diagnostics, edge states, tick/save-load and all Workspace profiles.
- Production Workspace no longer reports readiness through the legacy persistent `cmp_military_target_fleet` marker.
- Transfer writes remain isolated to `set_ship_owner`, `set_ship_owner_multiple` and source-country `clear_ownership_transfer_fleet`.
- Supply writes remain country-scoped `add_supply_ships` only; formation assignment stays read-only via `num_assigned_supply_ships`.
- Direct ShipTemplate writes and destructive Ship hull/crew effects remain outside RC1.
- `tools/validate_beta18_rc1.py` is mandatory from the full release validator.


## beta18 Final — Navy Rework release audit

- beta18-RC1 full runtime regression accepted by the user: all tested Navy functions work correctly.
- Final is a release/cleanup build with `new_gameplay_mechanics = 0`.
- Runtime-PASS frozen surface: Fleet Composer 2.0, exact MilitaryFormation routing, existing-Fleet add-ships, exact Ship selection, flagship set/unset, single/batch/cross-Fleet transfers, native Retrofit bridge, national Supply reserve and assigned-supply diagnostics.
- `registry/beta18_final_freeze.json` pins semantic SHA-256 hashes of the RC1 Navy gameplay surface; Final validation rejects semantic drift.
- Direct ShipTemplate writes, destructive hull/crew actions and direct Supply assignment to formation remain outside the supported contract.
- Hidden legacy Fleet Plans/fallback source is retained for rollback safety but is not a production Workspace route.
- Amphibious Assistant moves to post-beta18 Military Operations.
