# Cheat Menu Pro v0.3 beta18.1-pre1 — Military Operations Discovery

**Build:** `CMP-0.3-B18-1-PRE1-20260823`  
**Parent:** beta18 Final / Navy frozen  
**Scope:** discovery-only, gameplay writes = 0

The post-beta18 cycle starts with a Marines / Fleet readiness / Naval Invasion discovery pass. The released beta18 Navy gameplay surface is frozen.

---

# Cheat Menu Pro v0.3 beta18 Final — Navy Rework

**Build:** `CMP-0.3-B18-FINAL-20260822`  
**Runtime:** `PASS`  
**Parent:** beta18-RC1 — full runtime regression accepted

## beta18 Final

- Navy Rework is released after the complete RC1 runtime regression.
- New gameplay mechanics relative to RC1: **0**.
- Runtime-PASS frozen surface: Fleet Composer 2.0, exact Fleet, add-ships, exact Ship, flagship, single/batch/cross-Fleet transfer, native Retrofit bridge, Supply reserve and assigned-supply diagnostics.
- Ship Templates/Retrofit remain on the native Victoria 3 workflow; no invented direct ShipTemplate write is used.
- Supply Ships remain a national logistics resource; direct Fleet assignment is not fabricated.
- Hidden legacy Fleet Plans/fallback source is retained only for rollback safety and is not a production Workspace dependency.
- Amphibious Assistant remains post-beta18 under Military Operations.

---

# Cheat Menu Pro v0.3 beta18-RC1 — Full Navy Regression

**Build:** `CMP-0.3-B18-RC1-20260822`  
**Runtime:** `RC1_REGRESSION_PENDING`  
**Parent:** beta18-pre5.1 — core functions accepted, full regression still required

RC1 is a feature freeze: no new gameplay mechanics. It regresses Fleet Composer 2.0, exact Fleet/add-ships, exact Ship, flagship, single/batch/cross-Fleet transfers, native Retrofit bridge, national Supply reserve, assigned-supply diagnostics, edge states, +1 day/save-load and all four Workspace profiles.

Stale pre5 candidate UI wording is removed, Interface diagnostics no longer depend on the legacy fleet marker, and `tools/validate_beta18_rc1.py` is now part of the mandatory release gate.

---

# Cheat Menu Pro v0.3 beta18-pre5.1 — Retrofit & Naval Logistics

**Build:** `CMP-0.3-B18-PRE5-1-20260822`  
**Runtime:** `UNVERIFIED`  
**Parent:** beta18-pre5 Exact Ship Transfers — transfer runtime gate still requires confirmation

- New **Logistics** Fleet subtab.
- Native Retrofit bridge: Ship Designer plus the native selected-Fleet panel.
- CMP does not invoke `RetrofitShips` or write ShipTemplate directly until exact CMP Ship ↔ native `ShipSelection` binding is proven.
- Supply Ships are modeled as a **national reserve**, not normal Fleet composition.
- `+1 / +10 / +50 / +100` country actions use documented `add_supply_ships`.
- `supply_ship_maintenance_fulfillment` diagnostics.
- Read-only `num_assigned_supply_ships` for the selected MilitaryFormation.
- Direct Supply Ship assignment remains DEFERRED.
- Amphibious Assistant is moved after beta18 Final.
- pre5 transfer remains in the mandatory runtime regression before RC1.

---

# Cheat Menu Pro v0.3 beta18-pre5 — Exact Ship Transfers

**Build:** `CMP-0.3-B18-PRE5-20260822`  
**Runtime:** `UNVERIFIED`  
**Parent:** beta18-pre4 Exact Ship Control & Flagship — Runtime PASS

- Single exact Ship ownership transfer via `set_ship_owner`.
- Persistent transfer basket supports up to 20 exact Ships across source Fleets.
- Batch ownership transfer uses `set_ship_owner_multiple` followed by source-country `clear_ownership_transfer_fleet`.
- Receiver must be a marked non-player country with a port.
- Destroyed, in-battle and flagship Ships are blocked.
- beta18-pre4 exact Ship/flagship is frozen as a runtime-PASS baseline.

---

# Cheat Menu Pro v0.3 beta18-pre4 — Exact Ship Control & Flagship

**Build:** `CMP-0.3-B18-PRE4-20260822`  
**Runtime:** `PASS` — user confirmed  
**Parent:** beta18-pre3 Fleet Composer 2.0 — Runtime PASS

- New **Ships** naval subtab with 100 exact ship positions across five pages.
- Exact target marker is stored on Ship scope rather than Ship Type.
- Ship type / flagship / damage / port / battle / HP / crew diagnostics.
- Safe exact writes: set/unset flagship.
- Transfers and destructive ship writes stay deferred.

---

# Cheat Menu Pro v0.3 beta18-pre3 — Fleet Composer 2.0

**Build:** `CMP-0.3-B18-PRE3-20260821`  
**Runtime:** `UNVERIFIED`  
**Parent:** beta18-pre2.4 runtime-accepted fleet target core

- Five independent composition rows.
- Any of 25 combat hulls per row; amount 0/1/3/5/10.
- Duplicate hull rows are allowed and expected to accumulate into one fleet.
- The first non-zero row anchors one new fleet; remaining rows target that exact temporary fleet scope.
- Role presets fill rows only.
- Instant spawn remains default-template; user templates stay on the native Ship Designer/construction route.

---

# Cheat Menu Pro v0.3 beta18-pre2.4 — Fleet Scope Proof & Native Panel Bridge

**Build ID:** `CMP-0.3-B18-PRE2-4-20260821`  
**Runtime:** `UNVERIFIED`

- Exact fleet rows now open Victoria's native military-formation panel instead of calling FormationPanel.SelectFormation from the standalone CMP context.
- Yellow/blue row probes separately prove bare MilitaryFormation root transport and owner resolution.
- GetSelectedFormation is observational only until runtime evidence proves it updates through this bridge.
- No persistent CMP fleet target marker is reintroduced.

---

# Cheat Menu Pro v0.3 beta18-pre2.3 — Native Fleet Selection & Direct Operations Core

**Build ID:** `CMP-0.3-B18-PRE2-3-20260821`  
**Parent:** beta18-pre2.2 runtime failure of the custom fleet-target marker  
**Runtime:** `UNVERIFIED`

- Victoria native `FormationPanel.SelectFormation` owns UI selection; CMP reads `GetSelectedFormation`.
- Existing-fleet add-ships executes directly against the selected `MilitaryFormation`; no production marker rescan.
- Empty owned Fleet is accepted as a first-ship target; a Fleet with an existing ship in battle is blocked.
- Legacy marker/resolver source remains fallback-only.
- Full 25-hull catalog, 100 catalog endpoints and 37,924 universal composer branches are preserved.

---

# Cheat Menu Pro v0.3 beta18-pre2.2 — Fleet Target Core Repair

**Build ID:** `CMP-0.3-B18-PRE2-2-20260821`  
**Parent:** beta18-pre2.1 Runtime FAIL on exact fleet selection  
**Status:** Static candidate / runtime selector gate required

## beta18-pre2.2 highlights

- Removes the failed `country ROOT + AddScope(formation)` path.
- Fleet selection now executes ScriptedGui directly with `military_formation` as ROOT.
- Exact marker cleanup is owner-local instead of global `every_country`.
- Adds runtime diagnostics: formation-root probe, callback received, exact marker written.
- Exact Fleet Resolver and further Navy features remain frozen until this gate passes.

# Cheat Menu Pro v0.3 beta18-pre2.1 — Navy Workflow Repair

**Build:** `CMP-0.3-B18-PRE2-1-20260821`  
**Runtime:** `UNVERIFIED`  
**Parent:** beta18-pre2 Runtime FAIL/SUPERSEDED

- Mixed Fleet now uses the full naval catalog across Capital / Cruiser / Torpedo groups instead of the old five-hull T&R-only path.
- Up to three selected hulls are created as one new fleet; 37,924 non-zero explicit composition branches are generated.
- Selected Fleet exposes all 25 combat hulls while retaining the exact persistent fleet target.
- Instant scripted creation is explicitly documented as using the type default template; user Ship Templates stay on Victoria 3 native Ship Designer/construction workflow.
- Legacy Fleet Plans are hidden from the primary route but kept as source fallback.

---

# Cheat Menu Pro v0.3 beta18-pre2 — Full Naval Catalog & Native Ship Designer Bridge

**Build:** `CMP-0.3-B18-PRE2-20260820`  
**Runtime:** `UNVERIFIED`  
**Parent:** beta18-pre1 architecture spike / beta17 Final released baseline

## beta18-pre2 highlights

- Full combat naval catalog: **20 vanilla + 5 Tech & Res hulls**; Supply Ship is classified separately as `READ_ONLY`.
- Workspace → Fleet now has three modes: **Ships & Templates / Mixed Fleet / Selected Fleet**.
- The full Victoria 3 1.13 progression is represented, from sailing hulls through ironclads/dreadnoughts/cruisers/carriers/torpedo craft to T&R late-game hulls.
- Categories: **All / Capital / Cruisers / Torpedo / Tech & Res**.
- Vanilla obsolescence filtering uses runtime `ShipType.IsObsolete` for the current country rather than a CMP-maintained replacement table.
- Each of 25 combat hulls exposes bounded `x1/x3/x5/x10` new-fleet creation: **100 explicit branches**. Existing Fleet target is never reused by this path.
- The native Ship Designer is opened through the same proven entry point used by vanilla Military panel: `PopupManager.ToggleShipDesignerPopup`. CMP performs no direct ShipTemplate writes.
- Explicit data model: **Ship Type → Ship Template → Ship → Fleet**.
- Catalog creation uses the normal/default hull template; explicit user-template selection is deferred to Fleet Composer 2.0 discovery/runtime gate.
- The verified pre1 T&R mixed composer remains as compatibility mode: **3,124** non-zero compositions → one formation.
- Beta17 exact existing-fleet path is retained with no hidden fallback.
- Legacy Fleet Designer is relabeled **Fleet Composition Planner (legacy)** to avoid collision with the native Ship Designer concept.

Details: `docs/NAVY_REWORK_PRE2_RU.md`; runtime: `docs/BETA18_PRE2_RUNTIME_CHECKLIST_RU.md`.

---

# Cheat Menu Pro v0.3 beta18-pre1 — Navy Architecture & Composition Foundation

**First static Navy Rework candidate on the released beta17 Final baseline.** The new route separates creation of a new mixed fleet from operations on an exact selected existing fleet.

## Added in beta18-pre1

- `registry/navy18.json` pins the verified five-ship Tech & Res provider contract, ship groups, technologies, and coverage/discovery state.
- `Army & Fleet → Fleet` now has **New Fleet** and **Selected Fleet** modes.
- The new composition builder gives every verified ship type an independent `0/1/3/5/10` count.
- Every mixed composition is created by **one** `create_military_formation` containing multiple `ship` blocks — one composition, one fleet.
- **3,124** non-zero composition branches are generated and validated; there is no hidden existing-fleet fallback.
- New-fleet HQ comes from a marked owned state with a port; highest-GDP marked port state wins when several are marked.
- Five composition profiles (Escort / Battle / Carrier / Wolfpack / Amphibious Support) populate the builder only and never create immediately.
- **Selected Fleet** retains the beta17 exact Fleet Selector and add-ships compatibility path.
- Transfer / flagship / supply writes / auto-attach remain behind explicit later beta18 gates.
- Native SearchBar is deferred until a 1.13.9+ baseline gate is accepted.
- Full static release QA: **PASS, 0 errors / 0 warnings**.

Details: `docs/NAVY_REWORK_PRE1_RU.md`; QA: `docs/QA_SUMMARY_BETA18_PRE1_RU.md`; runtime checklist: `docs/BETA18_PRE1_RUNTIME_CHECKLIST_RU.md`.

---

# Cheat Menu Pro v0.3 beta17 Final RC1 — Army Final Audit

**Runtime candidate on top of the accepted beta17-pre3.1 build.** Army Final formalizes the Army domain in a registry/validator contract and fixes conflicts found during the full preset/control audit. RC1 still requires runtime acceptance before the final beta17 release.

## beta17 Final RC1

- Added `registry/army_final.json` and mandatory `tools/validate_army_final.py`.
- Audited 26 unit types × 5 amounts = **130** Army Builder spawn endpoints.
- Audited **1,568** mixed-template branches and **17,472** Designer branches across all 48 configurations.
- Removed the unreachable duplicate `military_drill` Mobile preset branch; deterministic tie-break now matches generated templates.
- Added the missing `blitzkrieg` Artillery preset GUI gate.
- Audited Army Controls: 10×5 = **50** apply endpoints plus 4 presets; removed 20 dead `*_level` cleanup refs.
- Cross-checked 10 Tech & Res land units against the pinned `3472248460` provider snapshot.
- Army create workflows are validated to create new formations only; no hidden existing-army fallback is allowed.
- Parent beta17-pre3.1 is recorded as user runtime PASS on 2026-08-20.

See `docs/ARMY_FINAL_RU.md` and `docs/QA_SUMMARY_BETA17_FINAL_RC1_RU.md`.

---

# Cheat Menu Pro v0.3 beta17-pre3.1 — Regions Operations Coverage & Safety Hotfix

**Cumulative static candidate on top of beta17-pre3.** This build expands Regions → Operations, guards every construction level against state availability/caps, and fixes preset component poisoning where one blocked building could prevent the remaining preset components in the same state. Fleet Selector Click Hotfix and Staffing Coverage 2.1 are preserved. Runtime status remains `UNVERIFIED`.

## Added/fixed in beta17-pre3.1

- Building operations expand from 56 to **92 SUPPORTED** entries: 55 vanilla + 37 Tech & Res, including government, university, military/naval, services, and provider-specific buildings.
- Operations now use the same category taxonomy as Staffing: All / Primary / Industry / Infrastructure / Public / Military / Services / Ownership. Game-managed ownership/trade/urban entities remain excluded from direct construction without a safe contract.
- ADD/SET/REMOVE selection uses independent `cmp_regions2_sel_*` markers and does not overlap Staffing `cmp_staffing_sel_*`; legacy B6 remains only as a compatibility bridge.
- ADD checks every next level: `can_construct_building` for an absent building and `can_queue_building_levels = 1` for an existing building. A capped/invalid state stops at the last allowed level and contributes a partial/blocked result.
- SET no longer removes/recreates buildings. Lower → target raises safely; equal is a no-op success; current > target is blocked as `UNSAFE`.
- REMOVE explicitly removes the whole building type; amount selection is not treated as a level count for REMOVE.
- Presets are per-state, best-effort per component. `cmp_regions2_state_blocked` is reset before each component, so a blocked port/resource-capped entry no longer cancels the rest of the preset in that state.
- Preset-only ADD 15/20 helpers are now generated and cross-validated.
- Release QA now validates nested CMP effect → effect references in addition to GUI → SGUI and SGUI → effect.

Details: `docs/REGIONS_OPERATIONS_SAFETY_PRE3_1_RU.md`; QA: `docs/QA_SUMMARY_BETA17_PRE3_1_RU.md`.

---

# Cheat Menu Pro v0.3 beta17-pre3 — Coverage & Diagnostics Foundation

**Static candidate on top of beta17-pre2.1.** This build implements the infrastructure stage of the updated roadmap: broader Staffing coverage, semantic coverage/schema validation, one Build ID, and compact diagnostics. The Fleet Selector Click Hotfix is preserved, but its user runtime gate remains `UNVERIFIED`.

## Added in beta17-pre3

- Staffing is separated from the 56-building construction-operations registry; `registry/staffing.json` classifies 132 candidates and exposes **97 SUPPORTED** buildings.
- Government, education, military, services, arts, trade, ownership, and technology reserve profiles are added for **14** total staffing profiles.
- Staffing selection uses independent `cmp_staffing_sel_*` markers and no longer mutates ADD/SET/REMOVE building selection.
- Adaptive Staffing `Off/50/75/90/100` now covers the complete 97-building supported catalog.
- Universal coverage contract added: `SUPPORTED / READ_ONLY / MANUAL / UNSAFE / UNSUPPORTED`; all 102 legacy B6 building selectors are explicitly classified.
- `tools/validate_registry_coverage.py` validates schema/coverage, providers, profile weights, exclusion reasons, and preservation of the previous 56 supported buildings.
- Build ID `CMP-0.3-B17-PRE3-20260820` is generated from `registry/build.json`; the stale beta16 tag in the UI registry is removed.
- Interface diagnostics expose Build ID, baseline, runtime status, and exact-fleet-target readiness.
- Military metrics are disambiguated: 267 registered/reused endpoints, 253 audited Workspace ScriptedGui refs, and 123 executable Workspace actions; the historical 239 metric is deprecated.
- Native SearchBar remains deferred until the minimum supported Victoria version is proven to be 1.13.9+.

Runtime gate: validate the inherited fleet click hotfix first, then test new Staffing coverage, selector independence, Adaptive Staffing, +1 day, and save/load.

---

# Cheat Menu Pro v0.3 beta17-pre2.1 — Fleet Selector Click Hotfix

**Cumulative hotfix on top of beta17-pre2.** Runtime testing confirmed that the persistent fleet list renders correctly, but clicking a row does not persist the selected target.

## Fixed in beta17-pre2.1

- Fleet rows now expose exactly one `onclick`: execute `cmp_military_target_fleet_select`. Immediate picker close on the same click has been removed.
- Dynamic row labels now use `MilitaryFormation.GetNameNoFormatting` instead of `MilitaryFormation.GetNameNoIcon` so the label is not a formatted interactive game-link over the button.
- The row textbox is `alwaystransparent = yes`, leaving pointer input to the parent selection button.
- The picker intentionally stays open after selection so the green exact-target marker can be observed before the user closes it explicitly.
- The release gate now rejects multiple row callbacks, self-closing rows, non-transparent labels and formatted fleet names in the picker.
- The selection gameplay effect, exact `cmp_military_target_fleet` marker, Fleet Builder/Designer and naval operations are unchanged.

Runtime gate: click a fleet row → see its green marker → close the picker → the exact fleet name must remain in the target row.

QA: `docs/QA_SUMMARY_BETA17_PRE2_1_RU.md`.

---

# Cheat Menu Pro v0.3 beta17-pre2 — Persistent Fleet Selector

**Cumulative preview overlay for Workshop item `3717461054`.** This build removes ambiguous Fleet targeting in Workspace and documents the target context of every Army workflow.

## Added in beta17-pre2

- Removed the beta17-pre1 one-shot event window, which looked like an operation and closed immediately after selection.
- Added a persistent scrollable list of **all owned fleets inside Workspace**, using live formation names with no sixteen-fleet cap.
- The exact target name remains visible after selection, and the selected row carries a green marker.
- Selecting a fleet only establishes a target; it does not create or modify anything until a separate operation button is pressed.
- Fleet and Fleet Plans now share explicit Select/Change, Clear Target, no-target, ready and all-ships-in-battle states.
- Fleet Builder, presets, Fleet Designer and Amphibious Task Force resolve only the formation carrying the persistent exact-target marker.
- Removed silent first-eligible fallback from the legacy list while preserving that list as a compatibility bridge for original CMP operations.
- Destroyed targets become invalid automatically; target cleanup removes both the new marker and the legacy list.
- Clarified Army target semantics: builders/templates create a new formation in a marked owned state, while Army Controls affect the selected country's armed forces.
- Deterministic generation, RU/EN parity and all four 90/100/115/130 profiles are covered by the updated release gate.

Details: `docs/MILITARY_TARGET_UX_RU.md`; QA: `docs/QA_SUMMARY_BETA17_PRE2_RU.md`.

---

# Cheat Menu Pro v0.3 beta16 Final — Diplomacy & Sovereignty accepted

**Accepted cumulative overlay for Workshop item `3717461054`.** The complete beta16 runtime checklist passed in Victoria 3 on 19 August 2026. This finalization changes release documentation and metadata only; it preserves the exact beta16-pre2.1 GUI, ScriptedGui, localization and gameplay trees that were tested.

## Accepted in beta16 Final

- Fleet Builder localization loads correctly after a full game restart; no raw `CMP_FLEET_*` labels remain in the tested flow.
- Fleet Plans and adjacent naval localization show no reported regression.
- Both expert Power Bloc membership actions and their negative-result paths work in the tested runtime flow.
- One-action confirmation reset, game-tick behavior and save/load persistence passed user acceptance.
- All 60 audited Diplomacy & Sovereignty actions retain the beta16-pre2 contract.
- Normal invitations, leaving, principles and leverage remain intentionally deferred.
- Full static base-plus-overlay QA remains PASS with zero errors and warnings.

Runtime and static evidence: `docs/QA_SUMMARY_BETA16_FINAL_RU.md`.

---

# Cheat Menu Pro v0.3 beta16-pre2.1 — Fleet localization hotfix

**Cumulative preview overlay for Workshop item `3717461054`.** This hotfix restores every `CMP_FLEET_*` label in the Fleet Workspace while retaining the beta16-pre2 gameplay contract.

## Fixed in beta16-pre2.1

- Removed a duplicate UTF-8 BOM from both Fleet Builder localization files.
- Restored the `l_russian:` and `l_english:` headers as the first decoded line so Victoria 3 loads all 42 Fleet/Task Force keys per language.
- Added a release gate that requires exactly one UTF-8 BOM and the correct language header in all 32 active RU/EN localization files.
- Changed no GUI geometry, ScriptedGui endpoint or gameplay effect.

QA: `docs/QA_SUMMARY_BETA16_PRE2_1_RU.md`.

## Inherited from beta16-pre2

- Added two explicitly labelled expert actions: force the player country or marked country into the marked Power Bloc.
- Added a one-action confirmation gate that clears after execution, tab change, result cleanup or Workspace close.
- Added preconditions that reject countries already belonging to any Power Bloc and postconditions that report success only after actual membership is observed.
- Added distinct results for missing bloc, missing country, existing membership and rejected join commands.
- Preserved the four verified cohesion actions and all 58 beta16-pre1 diplomacy actions, for 60 audited actions total.
- Kept normal invitations, leaving, principles and leverage deferred; the old “invite” endpoints are not invitations and remain hidden.
- Added RU/EN help describing the bypassed invitation/leverage/acceptance/cooldown flow and the DLC/slot/time constraints on deferred controls.

Details: `docs/DIPLOMACY_SOVEREIGNTY_2_RU.md`; beta16-pre2 QA: `docs/QA_SUMMARY_BETA16_PRE2_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.8 — Workspace convergence

**Cumulative overlay for Workshop item `3717461054`.** beta15.8 consolidates the completed Workspace migration without changing gameplay effects.

## Added in beta15.8

- Kept exactly one visible legacy-menu entry: **WORKSPACE**.
- Added a shared Help directory with seven section routes in every 90/100/115/130 profile.
- Added an explicit **Home** reset for navigation, help layers, tabs and list filters.
- Home preserves the selected interface profile, gameplay targets, ScriptedGui selections and operation results.
- Standardized Workspace close behavior on the existing `close_window` shortcut; no unverified custom binding was introduced.
- Standardized English military terminology on **Army & Fleet**.
- Extended deterministic launcher, header, help-route, reset-state, shortcut, localization and accessibility gates.
- Kept all legacy panels as source-level emergency fallbacks and left `common/` byte-identical to accepted beta15.7.

Details: `docs/WORKSPACE_CONVERGENCE_RU.md`; QA: `docs/QA_SUMMARY_BETA15_8_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.7 — Army & Fleet in Workspace

**Cumulative overlay for Workshop item `3717461054`.** beta15.7 migrates the existing Army/Fleet builders, templates and controls into the shared Workspace without changing gameplay effects.

## Added in beta15.7

- Enabled **Army & Fleet** in all four 90/100/115/130 Workspace profiles.
- Added five compact top-level surfaces: **Army / Army Templates / Army Controls / Fleet / Fleet Templates**.
- Added 44 content-only scrolling layouts plus 32 persistent military help layouts.
- Reused 267 existing military ScriptedGui endpoints with deterministic four-profile parity.
- Split all 26 land units into Infantry & Marines, Artillery, and Cavalry & Armor filters.
- Kept full localized unit/ship names and technology details in hover help when dense labels are shortened.
- Integrated Army Builder, quick/mixed/custom templates, Marines, Army Controls, Fleet Builder, Fleet Designer and Amphibious Task Force into one navigation hierarchy.
- Kept technology gates, marked-state/fleet requirements, battle eligibility and results explicit.
- Kept the post-creation army-to-fleet attachment as a persistent, clearly labeled manual game-UI step.
- Retained the legacy Army/Fleet panels as emergency fallbacks; `common/` is byte-identical to accepted beta15.6.

Details: `docs/MILITARY_IN_SHELL_RU.md`; QA: `docs/QA_SUMMARY_BETA15_7_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.6 — Politics & Characters in Workspace

**Cumulative overlay for Workshop item `3717461054`.** beta15.6 migrates the existing Politics & Characters 2.0 mechanics into the shared Workspace without changing gameplay effects.

## Added in beta15.6

- Enabled **Politics** in all four 90/100/115/130 Workspace profiles.
- Added five content-only scrolling surfaces: **Government / Characters / Groups / Laws / Power Bloc**.
- Added context-sensitive target readiness while navigation and results remain fixed.
- Reused all 86 unique Politics selection and action endpoints with full four-profile parity.
- Moved long explanations into composite tooltips and 24 persistent scrollable help layouts.
- Kept permanent warnings for military-role removal, direct law-enactment changes and relative political-strength semantics.
- Integrated the latest Politics result and result reset into the fixed Workspace footer.
- Removed the separate legacy Politics launcher while retaining the generated fallback panel in source.
- Kept the entire `common/` gameplay tree byte-identical to accepted beta15.5.1.

Details: `docs/POLITICS_IN_SHELL_RU.md`; QA: `docs/QA_SUMMARY_BETA15_6_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.5.1 — Building Category Filter

**Cumulative hotfix for Workshop item `3717461054`.** beta15.5.1 adds a category selector to the Regions & Buildings 2.0 building lists without changing beta15.5 gameplay effects.

- Seven choices: All, Extraction, Agriculture, Light Industry, Heavy Industry, Power and Infrastructure.
- One session-persistent category is shared by Operations and Staffing.
- All 56 registered buildings are assigned exactly once with no gaps or duplicates.
- Changing category preserves the selected building, operation, value and result.
- Resource mode retains its dedicated compact list.
- Category menus and filtered layouts are generated for all 90/100/115/130 profiles.
- RU/EN tooltips describe every category and its object count.
- Deterministic distribution, layout, selector and endpoint regression gates are included.

QA: `docs/QA_SUMMARY_BETA15_5_1_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.5 — Population & Society in Workspace

**Cumulative overlay for Workshop item `3717461054`.** beta15.5 migrates the existing Population & Society 2.0 mechanics into the shared Workspace without changing gameplay effects.

## Added in beta15.5

- Enabled **Population** in all four 90/100/115/130 Workspace profiles.
- Added four independently scrolling surfaces: **Population / Professions / Welfare / Society**.
- Kept state target, navigation and result fixed while only the active tab content scrolls.
- Migrated all 59 unique selection and action endpoints with complete profile parity.
- Moved long descriptions into composite tooltips and five persistent help cards per profile.
- Preserved the mass culture/religion confirmation gate and a permanent destructive-action warning.
- Integrated operation feedback into the fixed Workspace footer.
- Retained the legacy Population 2.0 panel as an emergency fallback.
- Added deterministic tab, endpoint, help, localization, control-size and overflow regression gates.

QA: `docs/QA_SUMMARY_BETA15_5_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.4 — Regions & Buildings in Workspace

**Cumulative overlay for Workshop item `3717461054`.** beta15.4 migrates Regions & Buildings 2.0 and the Staffing Assistant into the shared Workspace without changing their gameplay effects.

## Added in beta15.4

- Enabled **Regions** in Workspace navigation for all four 90/100/115/130 profiles.
- Added separate **Operations / Staffing** surfaces.
- Added two-column, content-only scrolling pickers for 56 buildings and 19 resource-capable buildings; configuration and target actions remain fixed.
- Kept full localized object names available in hover tooltips when a dense picker label is shortened.
- Integrated Building ADD/SET/REMOVE, Resource ADD/SET/CLEAR, four regional presets, six staffing reserve sizes and five occupancy modes.
- Kept the destructive exact-SET warning visible beside the controls.
- Added five persistent scrollable help topics per profile and fixed-footer Regions/Staffing result feedback.
- Retained the legacy Regions panel as an emergency fallback.
- Added deterministic profile-parity, endpoint, tooltip, localization and overflow regression gates.

QA: `docs/QA_SUMMARY_BETA15_4_RU.md`.

---

# Cheat Menu Pro v0.3 beta15.3.1.1 — Interface Text Hotfix

**Cumulative overlay for Workshop item `3717461054`.** beta15.3.1.1 removes the last confirmed Interface-page text overflow without changing gameplay mechanics or the geometry of other pages.

## Fixed in beta15.3.1.1

- Removed the long implementation paragraph from the always-visible Interface layer.
- Added a compact runtime-safe profile-selection summary.
- Added an `i` control with a composite tooltip and persistent scrollable help card.
- Generated one Interface help layout for every 90/100/115/130 profile.
- Closing the Workspace now clears both Economy and Interface help state.
- Added a regression gate forbidding long implementation strings in the permanent Interface layout.

QA: `docs/QA_SUMMARY_BETA15_3_1_1_RU.md`.

## Inherited from beta15.3.1

- Replaced the fixed-width legacy target tray with one stable **WORKSPACE** launcher.
- Removed the separate legacy `ECON 2.0` launcher from the old workspace.
- Replaced long always-visible Economy descriptions with compact labels and composite hover tooltips.
- Added four persistent scrollable help cards—overview, money, modifiers and ownership—for every 90/100/115/130 profile.
- Kept active-target state and the latest operation result visible without requiring a tooltip.
- Removed the technical migration note from the visible navigation.
- Preserved all Economy gameplay effects, values, targets and persistence semantics.

QA: `docs/QA_SUMMARY_BETA15_3_1_RU.md`.

## Inherited from beta15.3

- Enabled **Economy** in shell navigation and migrated Money, Modifiers and Ownership into the shared content viewport.
- Added profile-specific Economy reflow for 90/100/115/130: 12 generated scroll layouts and 46 unique action/selection endpoints with full profile parity.
- Kept the active country-target status and Target Center shortcut inside the Economy page.
- Moved Economy result feedback into the shell's fixed footer.
- Changed the visible `ECON 2.0` entry point to open the shell directly; the legacy popup remains in the files as an emergency fallback.
- Preserved all 11 economic parameters, 9 values, 6 policy overrides, 8 treasury/investment actions and 3 debt/bankruptcy actions without gameplay-effect changes.

Details: `docs/ECONOMY_IN_SHELL.md`; QA: `docs/QA_SUMMARY_BETA15_3_RU.md`.

## Inherited fix from beta15.2.1

- Restored all 5,387 lines of `common/scripted_guis/sakuya_cheat_b4_sgui.txt`; beta15.2 ended mid-command and omitted the final 1,029 lines.
- Preserved both Victoria 3 1.13 `clear_ownership_transfer_fleet` finalization calls.
- Added `baseline_manifest.json` for the verified `529340/3717461054` source subtree.
- Completed full base-plus-overlay validation: 10,127 GUI references across 106 GUI/common files, with zero missing ScriptedGui definitions and zero validation errors.

QA details: `docs/QA_SUMMARY_BETA15_2_1_RU.md`.

## Inherited from beta15.2

beta15.2 introduced the shared workspace and migrated Target Center plus interface profiles. Existing Economy, Regions, Population, Politics and Military pages remain available through the legacy menu until their dedicated migrations.

## What changed in beta15.2

- Added a `1120×660` Workspace Shell with a stable header, left navigation, scrollable content viewport and fixed footer.
- Rebuilt Target Center inside the shell: user-facing text is at least 12 pt, primary controls are `44–56 px` high, and primary labels do not use `elide = right`.
- Added four real reflow profiles: **90% Compact / 100% Standard / 115% Large / 130% Extra large**. Each profile is generated as separate geometry; no unverified runtime root-scale binding is used.
- Added **Interface** inside the shell for immediate profile switching.
- Retained the old Target popup in the package as an emergency fallback, but all visible Target entry points now open the new shell.
- Added `registry/ui_shell.json`, deterministic `tools/generate_workspace_shell.py --check`, RU/EN parity and dedicated shell accessibility gates.

## Known boundaries

- This is the **shell foundation**, not the completion of the full beta15.2 migration. Disabled navigation entries show the pages scheduled for later shell migration.
- Full GUI→ScriptedGui overlay validation still requires a local snapshot of the base Workshop mod. Patch-only validation cannot resolve references owned by that base.
- Pixel-perfect and click-target QA must still be performed inside Victoria 3 at 2560×1080 and 3440×1440.

Details: `docs/WORKSPACE_SHELL.md`.

---

# Cheat Menu Pro v0.3 beta15.1 — UI Accessibility Rework

**Cumulative hotfix on top of beta15, driven by runtime feedback at a 2560×1080 game resolution.** Existing Politics 2.0, Population 2.0, Economy 2.0, Army/Fleet Builders and previous beta mechanics are retained.

## Highlights

- **2560×1080 is now the primary layout target**; 3440×1440 is the secondary ultrawide profile.
- **Economy 2.0 is reorganized into three large tabs:** Money / Modifiers / Ownership. The panel is now `1040×700`, with more prominent target and action controls.
- Modifier values are split into two readable rows instead of one dense row of micro-buttons.
- **Politics 2.0** is enlarged to `912×642` and its typography/controls are scaled up without changing mechanics.
- **Fleet Builder** ship selectors are now `268×48` in the existing two-column layout.
- Army/Fleet and Population 2.0 receive a second typography/readability pass.
- Visible RU/EN localization QA now covers Economy/Politics/Population/Army/Fleet and catches untranslated technical leftovers.

See `docs/UI_ACCESSIBILITY_RU.md` for the current layout standard.

---

# Cheat Menu Pro v0.3 beta15 — Politics & Characters 2.0

**Cumulative patch for Workshop mod `3717461054`.** Includes beta1–beta14.

## Beta15

- New Politics 2.0 controller over legacy B3/B5/B9: Government / Characters / Interest Groups / Laws / Power Bloc.
- Country actions route through Target Core (Player / Marked Country / Group A/B/C).
- Government modifiers and institution levels, character tools, IG approval/political strength, current-law enactment operations, and safe Power Bloc cohesion.
- Biological age remains read-only because a safe direct SET-age effect was not confirmed.
- Beta14 accessibility standard remains mandatory: 2560×1080 primary, 3440×1440 secondary, larger controls and RU/EN parity.
- Vanilla Rework audit seed added for systematic legacy CMP review after the main roadmap stages.

See `docs/POLITICS_2.md`.

---

# Cheat Menu Pro v0.3 beta14 — Population & Society + UI Accessibility

**Current cumulative release.** Apply over a copy of Workshop mod `3717461054`; it includes beta1–beta13 functionality.

## Beta14 highlights

- New accessibility-first **Population & Society 2.0** UI with Population, Professions, Welfare, and Society pages.
- Static primary layout target: **2560×1080**; secondary ultrawide target: **3440×1440**. Real rendering still requires in-game Victoria 3 QA.
- Fleet Builder ship picker is now two-column with `268×44` controls; audited Army/Fleet/Population fonts have a minimum size of 10.
- Dedicated visible-localization gate checks key parity and accidental untranslated English strings in RU UI.
- Original dense CMP POP page remains available as **Legacy POP UI**.
- Population 2.0 accepts explicit state targets from Target Core only.
- Supports population add/remove, exact literacy, profession cohorts, qualifications, wealth, loyalists/radicals, migration, working-adult share, confirmed assimilation/religion conversion, and three mass presets.

See `docs/POPULATION_2_RU.md` and `docs/UI_ACCESSIBILITY_RU.md`.

---


Cumulative patch for Workshop mod 3717461054; includes beta6.

New: bounded custom mixed-army designer (size 25/50/75/100, infantry 40/50/60/70%, artillery 10/20/30%, mobile remainder), verified T&R Marine builder requiring a marked port state, and corrected T&R role mapping (Modern Heavy Tank = artillery group; Modern Light Tanks = cavalry/mobile group).

Vanilla 1.13 low/mid/high Marine IDs are referenced by Tech & Res, but their exact current unlock gates are not present in the supplied files, so beta7 deliberately does not spawn them.

Runtime validation remains required for manpower linkage, organization, save/load, and manual fleet attachment behavior.


## v0.3 beta8 — Fleet Builder / Amphibious Task Force

The Army Builder scroll now also contains a Fleet Builder. It targets an already marked player fleet and uses Victoria 3 1.13 `create_ship`. Beta8 intentionally exposes only the five Tech & Res hulls whose unlocking technologies are verified directly from the supplied mod source. Technology gates are checked both in UI and again in scripted effects.

The Amphibious Task Force action combines the selected Marine amount with available verified support hulls in the marked fleet, then creates the all-Marine formation in a marked port state. Army-to-fleet attachment remains a normal-game UI step because no supported scripted attach effect was confirmed in the public 1.13 script documentation.


## v0.3-beta9 — Fleet Template Designer

Adds a bounded fleet designer: size 10/20/40, escort 20/40/60%, carriers 0/10/20%, submarines 0/20/40%; the remainder is capital/line strength split between modern cruisers and battleships. Five profiles prefill the designer but do not create ships until Apply is pressed.


## v0.3-beta10 — Unified Target Controller

Click **TARGETS** in the global status bar to open the new Target Controller. It stores one active target context and persistent country groups A/B/C. Transient CMP marks can be cleared from one place without deleting own-state decree marks or persistent groups. Legacy pages are migrated to this core incrementally rather than rewritten all at once.

## v0.3-beta11 — Registry + Code Generation Foundation

Beta11 adds declarative JSON registries for providers, 56 Staffing buildings, 26 land units, 5 ships, 8 Tech & Res resources and the operation catalog.

Fleet Builder is the first production path migrated to code generation: scripted GUI, scripted effects, provider adapters and the ship-selector block inside `sakuya_main.gui` are generated by `tools/generate_registry.py`.

Use `python3 tools/generate_registry.py --check` for deterministic generation validation. See `docs/REGISTRY_ARCHITECTURE.md` for the extension contract.

## v0.3-beta12 — Regions & Buildings 2.0

B6 Staffing now has an explicit **Staffing / Operations** submode. Operations provide Building ADD / exact SET / REMOVE, Resource ADD / exact SET / CLEAR, four additive regional presets, Tech & Res geology synchronization for exact registered tiers, and occupancy-gated Adaptive Staffing (Off / <50 / <75 / <90 / <100%).

Building ADD preserves the existing building and is exact for existing levels 0–300. Building SET is intentionally implemented as remove → recreate because the engine's `create_building level=N` does not lower an already higher building; SET can therefore reset building-object state such as PM/ownership/reserves. Adaptive Staffing reads actual building occupancy but still uses registry staffing profiles for profession proportions because the public script surface does not expose an exact per-profession vacancy vector.

See `docs/REGIONS_BUILDINGS_2.md` for mechanics and runtime tests.
