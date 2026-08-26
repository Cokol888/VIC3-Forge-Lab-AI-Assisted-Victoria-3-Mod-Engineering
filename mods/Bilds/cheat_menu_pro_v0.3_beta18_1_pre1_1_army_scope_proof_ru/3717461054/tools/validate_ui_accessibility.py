#!/usr/bin/env python3
from __future__ import annotations
import codecs, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / 'gui/main/sakuya_main.gui'
LOC = ROOT / 'localization'

PROFILES = [
    {'resolution': '2560x1080', 'role': 'primary', 'kind': 'static-layout-gate'},
    {'resolution': '3440x1440', 'role': 'secondary-ultrawide', 'kind': 'static-layout-gate'},
    {'density': '90/100/115/130', 'role': 'workspace-reflow', 'kind': 'generated-profile-gate'},
]
CUSTOM_STEMS = [
    'cmp_fleet_builder', 'cmp_fleet_designer',
    'cmp_army_builder', 'cmp_army_designer', 'cmp_army_mixed', 'cmp_army_ux',
    'cmp_population2', 'cmp_economy2', 'cmp_politics2', 'cmp_workspace', 'cmp_navy18',
]
# These words are considered accidental untranslated implementation jargon in visible Russian UI.
FORBIDDEN_RU = [
    r'\beffect\b', r'\btier\b', r'\bformation\b', r'\bruntime\b', r'save/load',
    r'\bscripting\b', r'attach-effect', r'marine capacity', r'unlock-gates',
    r'unlock-определ', r'\boverride\b', r'\bmodifier\b', r'\bTarget Core\b', r'\bclout\b',
]
ALLOW_EQUAL_LATIN_VALUES = set()

def read(path: Path) -> str:
    return path.read_text(encoding='utf-8-sig')

def between(text: str, start: str, end: str) -> str:
    try:
        a = text.index(start)
        b = text.index(end, a)
    except ValueError as e:
        raise RuntimeError(f'missing marker: {e}')
    return text[a:b]

def parse_loc(path: Path) -> dict[str, str]:
    out = {}
    for line in read(path).splitlines():
        m = re.match(r'\s*([^#\s][^:]*):\d*\s+"(.*)"\s*$', line)
        if m:
            out[m.group(1).strip()] = m.group(2)
    return out

def ints(block: str, field: str) -> list[int]:
    return [int(x) for x in re.findall(rf'\b{re.escape(field)}\s*=\s*(\d+)', block)]

def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    gui = read(GUI)

    for marker in ['# CMP_UI_ACCESSIBILITY_B14', '# CMP_UI_ACCESSIBILITY_B15_1', '# CMP_POP2_BEGIN', '# CMP_POP2_END',
                   '# CMP_WORKSPACE_LAUNCHER_BEGIN', '# CMP_WORKSPACE_LAUNCHER_END',
                   '# CMP_WORKSPACE_SHELL_BEGIN', '# CMP_WORKSPACE_SHELL_END',
                   '# CMP_REGISTRY_BEGIN fleet_ship_selector', '# CMP_REGISTRY_END fleet_ship_selector',
                   '# CMP_POP2_LEGACY_RETURN_BEGIN', '# CMP_POP2_LEGACY_RETURN_END']:
        if gui.count(marker) != 1:
            errors.append(f'marker {marker!r}: expected 1, got {gui.count(marker)}')

    try:
        army = between(gui, '# CMP v0.3-beta4 Army Builder', '# CMP v0.3-beta8 Fleet Builder')
        fleet = between(gui, '# CMP v0.3-beta8 Fleet Builder', '# CMP v0.3-beta5 Simple Army Controls')
        pop = between(gui, '# CMP_POP2_BEGIN', '# CMP_POP2_END')
        economy = between(gui, '# CMP_ECONOMY2_BEGIN popup', '# CMP_ECONOMY2_END popup')
        politics = between(gui, '# CMP_POLITICS2_BEGIN popup', '# CMP_POLITICS2_END popup')
        workspace = between(gui, '# CMP_WORKSPACE_SHELL_BEGIN', '# CMP_WORKSPACE_SHELL_END')
        ship_selector = between(gui, '# CMP_REGISTRY_BEGIN fleet_ship_selector', '# CMP_REGISTRY_END fleet_ship_selector')
    except RuntimeError as e:
        print(json.dumps({'status':'FAIL','errors':[str(e)]}, ensure_ascii=False, indent=2))
        return 1

    blocks = {'army': army, 'fleet': fleet, 'population2': pop, 'economy2': economy, 'politics2': politics, 'workspace': workspace}
    font_stats = {}
    thresholds = {'army': (11, 11), 'fleet': (11, 11), 'population2': (12, 11), 'economy2': (12, 10), 'politics2': (12, 11), 'workspace': (12, 12)}
    for name, block in blocks.items():
        fs = ints(block, 'fontsize')
        fmin = ints(block, 'fontsize_min')
        min_fs = min(fs) if fs else None
        min_fmin = min(fmin) if fmin else None
        font_stats[name] = {'min_fontsize': min_fs, 'min_fontsize_min': min_fmin, 'font_entries': len(fs)}
        need_fs, need_fmin = thresholds[name]
        if min_fs is None or min_fs < need_fs:
            errors.append(f'{name}: fontsize minimum {min_fs}, expected >= {need_fs}')
        if min_fmin is None or min_fmin < need_fmin:
            errors.append(f'{name}: fontsize_min minimum {min_fmin}, expected >= {need_fmin}')

    # Fleet ship picker should be two-column, 48px high, generated for 5 ships with selected/unselected states.
    big_ship_buttons = len(re.findall(r'button_standard\s*=\s*\{\s*size\s*=\s*\{\s*268\s+48\s*\}', ship_selector))
    ship_keys = sorted(set(re.findall(r'text\s*=\s*"(CMP_NAVY18_HULL_[A-Z0-9_]+)"', ship_selector)))
    expected_ship_states = len(json.loads(read(ROOT / 'registry/ships.json'))['ships']) * 2
    if big_ship_buttons != expected_ship_states:
        errors.append(f'fleet ship selector: expected {expected_ship_states} x 268x48 button states, got {big_ship_buttons}')
    if len(ship_keys) != len(json.loads(read(ROOT / 'registry/ships.json'))['ships']):
        errors.append(f'fleet ship selector: expected full-catalog ship localization keys, got {len(ship_keys)}')

    # Population primary interaction controls: the generated page must have plenty of >=44px controls.
    pop_large_controls = len(re.findall(r'button_standard\s*=\s*\{[^{}]{0,160}?size\s*=\s*\{\s*\d+\s+(?:44|46|48|50|52)\s*\}', pop, re.S))
    if pop_large_controls < 20:
        warnings.append(f'population2: only {pop_large_controls} large controls detected (expected >=20)')

    # Static scroll reachability gate: content height set for 1080p-oriented scrolling.
    if 'widget = { size = { 742 3100 }' not in gui:
        errors.append('army/fleet scroll content height 3100 missing')

    # Economy 2.0 must use the new three-tab, large-control layout.
    for token in ["cmp_economy2_tab', 'direct", "cmp_economy2_tab', 'modifiers", "cmp_economy2_tab', 'policies"]:
        if token not in economy: errors.append(f'economy2 tab missing: {token}')
    if len(re.findall(r'size\s*=\s*\{\s*320\s+48\s*\}', economy)) < 3:
        errors.append('economy2: expected three 320x48 primary tabs')
    if 'size = { 1040 700 }' not in economy:
        errors.append('economy2: large 1040x700 panel missing')

    # Politics 2.0 is uniformly enlarged from the beta15 baseline.
    if 'size = { 912 642 }' not in politics:
        errors.append('politics2: enlarged 912x642 panel missing')

    # beta15.6 Workspace Shell: four generated reflow profiles, migrated Economy,
    # Regions, Population and Politics, category-filtered lists and a fixed footer.
    profile_ids = ['compact', 'standard', 'large', 'xlarge']
    building_registry = json.loads(read(ROOT / 'registry/buildings.json'))['buildings']
    regions_registry = json.loads(read(ROOT / 'registry/regions_buildings.json'))
    staffing_registry = json.loads(read(ROOT / 'registry/staffing.json'))
    staffing_supported = [item for item in staffing_registry['buildings'] if item.get('status') == 'SUPPORTED']
    population_registry = json.loads(read(ROOT / 'registry/population2.json'))
    ui_registry = json.loads(read(ROOT / 'registry/ui_shell.json'))
    for profile_id in profile_ids:
        if f'name = "cmp_workspace_shell_{profile_id}"' not in workspace:
            errors.append(f'workspace: missing generated profile {profile_id}')
        if f"cmp_ui_scale_profile', '{profile_id}" not in workspace:
            errors.append(f'workspace: missing selector for profile {profile_id}')
    # Only dense object-picker labels may elide; every one exposes the full
    # localized object name or a full technology-aware unit tooltip. Primary
    # actions never elide.
    # Every building appears in the default list and once in its category for
    # both Operations and Staffing. Resource entries retain one dedicated list.
    land_units_registry = json.loads(read(ROOT / 'registry/land_units.json'))['units']
    ships_registry = json.loads(read(ROOT / 'registry/ships.json'))['ships']
    fleet_registry = json.loads(read(ROOT / 'registry/fleet_builder.json'))
    # Operations and Staffing now have independent registries. Each object appears
    # once in the unfiltered picker and once in exactly one category-filtered picker.
    expected_building_elisions = (
        len(building_registry) * 2 + len(staffing_supported) * 2 +
        len(regions_registry['resource_capable_buildings'])
    ) * len(profile_ids)
    navy18_registry = json.loads(read(ROOT / 'registry/navy18.json'))
    naval_catalog_registry = json.loads(read(ROOT / 'registry/naval_catalog.json'))
    composer_rows = navy18_registry['composer2']['rows']
    combat_hulls = len(naval_catalog_registry['combat_hulls'])
    # Fleet Composer 2.0 renders every hull twice per row: selected-name state on the main
    # surface and one row-local picker button. It also has one elided "no hull" label per row.
    expected_navy_hull_elisions = (
        len(ships_registry) + combat_hulls + composer_rows * combat_hulls * 2 + composer_rows
    ) * len(profile_ids)
    expected_military_elisions = len(land_units_registry) * len(profile_ids)
    expected_dynamic_formation_elisions = 7 * len(profile_ids)  # pre1.1 adds one native-selected exact Army observer per profile
    expected_picker_elisions = expected_building_elisions + expected_military_elisions + expected_navy_hull_elisions + expected_dynamic_formation_elisions
    picker_elisions = workspace.count('elide = right')
    picker_name_tooltips = len(re.findall(r'tooltip = "building_[a-z0-9_]+"', workspace))
    military_unit_tooltips = len(re.findall(r'tooltip = "CMP_ARMY_UNIT_TT_[A-Z0-9_]+"', workspace))
    navy_hull_tooltips = len(re.findall(r'tooltip = "CMP_NAVY18_HULL_[A-Z0-9_]+(?:_TT)?"', workspace))
    dynamic_formation_tooltips = (workspace.count('tooltip = "[MilitaryFormation.GetNameNoIcon]"') +
                                  workspace.count('tooltip = "[MilitaryFormation.GetNameNoFormatting]"'))
    all_picker_tooltips = picker_name_tooltips + military_unit_tooltips + navy_hull_tooltips + dynamic_formation_tooltips
    if (picker_elisions != expected_picker_elisions or
            picker_name_tooltips != expected_building_elisions or
            military_unit_tooltips != expected_military_elisions or
            navy_hull_tooltips < expected_navy_hull_elisions or
            dynamic_formation_tooltips != expected_dynamic_formation_elisions):
        errors.append(f'workspace: picker elision/full-name-tooltip contract failed: elide={picker_elisions}, all_tooltips={all_picker_tooltips}, building={picker_name_tooltips}/{expected_building_elisions}, military={military_unit_tooltips}/{expected_military_elisions}, navy_hulls={navy_hull_tooltips}/{expected_navy_hull_elisions}, dynamic_formations={dynamic_formation_tooltips}/{expected_dynamic_formation_elisions}, expected={expected_picker_elisions}')
    if re.search(r'\bscale\s*=', workspace):
        errors.append('workspace: unverified runtime scale binding is forbidden; use generated reflow profiles')
    if 'scrollarea = { name = "cmp_workspace_target_scroll"' not in workspace:
        errors.append('workspace: target content-only scroll area missing')
    if 'position = { 222 596 } size = { 898 2 }' not in workspace:
        errors.append('workspace: fixed footer separator missing')
    if workspace.count('size = { 1120 660 }') < 5:
        errors.append('workspace: safe 1120x660 shell geometry missing')
    launcher_count = gui.count('name = "cmp_workspace_launcher"')
    if launcher_count != 1:
        errors.append(f'workspace launcher: expected exactly one, got {launcher_count}')
    if 'name = "cmp_ui_target_bar"' in gui:
        errors.append('workspace launcher: fixed-width legacy target tray is still present')
    if re.search(r'position\s*=\s*\{\s*1068\s+126\s*\}[^\n]*CMP_ECO2_OPEN', gui):
        errors.append('workspace launcher: separate legacy Economy entry is still present')
    if "Toggle('cmp_target_core_panel')" in gui:
        errors.append('workspace: a visible entry point still opens the legacy Target popup')
    if "Toggle('cmp_economy2_panel')" in gui:
        errors.append('workspace: a visible entry point still opens the legacy Economy popup')
    if "Toggle('cmp_politics2_panel')" in gui:
        errors.append('workspace: a visible entry point still opens the legacy Politics popup')
    # beta15.8 convergence: the header, help directory, reset semantics and
    # close behavior must be identical across every generated profile.
    home_lines = re.findall(r'button_standard\s*=\s*\{\s*name\s*=\s*"cmp_workspace_home_[^"]+"[^\n]+', workspace)
    global_help_buttons = re.findall(r'button_standard\s*=\s*\{\s*name\s*=\s*"cmp_workspace_global_help_(?:compact|standard|large|xlarge)"[^\n]+', workspace)
    global_help_cards = re.findall(r'name\s*=\s*"cmp_workspace_global_help_card_(?:compact|standard|large|xlarge)"', workspace)
    global_help_routes = re.findall(r'name\s*=\s*"cmp_workspace_global_help_route_(?:target|economy|regions|population|politics|diplomacy|military|interface)_(?:compact|standard|large|xlarge)"', workspace)
    if len(home_lines) != 4:
        errors.append(f'workspace convergence: expected four Home controls, got {len(home_lines)}')
    if len(global_help_buttons) != 4 or len(global_help_cards) != 4:
        errors.append(f'workspace convergence: global Help profile parity failed: buttons={len(global_help_buttons)}, cards={len(global_help_cards)}')
    if len(global_help_routes) != 32 or len(set(global_help_routes)) != 32:
        errors.append(f'workspace convergence: expected 32 unique Help routes, got {len(global_help_routes)}/{len(set(global_help_routes))}')
    home_contract = '\n'.join(home_lines)
    if 'cmp_ui_scale_profile' in home_contract or 'GetScriptedGui' in home_contract:
        errors.append('workspace convergence: Home must not change profile or gameplay ScriptedGui state')
    for variable in ['cmp_workspace_page', 'cmp_workspace_global_help', 'cmp_economy2_tab',
                     'cmp_workspace_regions_tab', 'cmp_population2_tab',
                     'cmp_workspace_politics_tab', 'cmp_workspace_military_tab',
                     'cmp_workspace_diplomacy_tab',
                     'cmp_workspace_building_category_menu_operations',
                     'cmp_workspace_building_category_menu_staffing']:
        if home_contract.count(variable) != 4:
            errors.append(f'workspace convergence: Home reset parity failed for {variable}')
    workspace_shortcuts = re.findall(r'\bshortcut\s*=\s*"([^"]+)"', workspace)
    if workspace_shortcuts != ['close_window'] * 4:
        errors.append(f'workspace convergence: shortcut contract must be four close_window bindings, got {workspace_shortcuts}')
    for forbidden_toggle in ["Toggle('cmp_target_core_panel')", "Toggle('cmp_economy2_panel')",
                             "Toggle('cmp_regions2_panel')", "Toggle('cmp_population2_panel')",
                             "Toggle('cmp_politics2_panel')", "Toggle('cmp_army_builder_panel')",
                             "Toggle('cmp_fleet_builder_panel')"]:
        if forbidden_toggle in gui:
            errors.append(f'workspace convergence: accepted legacy launcher remains: {forbidden_toggle}')
    workspace_button_heights = [
        int(height) for width, height in re.findall(
            r'button_standard\s*=\s*\{[^\n]*?size\s*=\s*\{\s*(\d+)\s+(\d+)\s*\}', workspace
        ) if int(width) > 56
    ]
    if not workspace_button_heights or min(workspace_button_heights) < 44:
        errors.append(f'workspace: primary button height minimum {min(workspace_button_heights) if workspace_button_heights else None}, expected >= 44')

    # beta15.3.1 density hotfix: compact visible labels, persistent contextual help,
    # and essential target/result state kept outside tooltip-only content.
    for key in ['CMP_ECO2_DESC', 'CMP_ECO2_DIRECT_DESC', 'CMP_ECO2_MOD_DESC', 'CMP_ECO2_POLICY_DESC']:
        if f'text = "{key}"' in workspace:
            errors.append(f'workspace density: long always-visible description remains: {key}')
    if 'CMP_WS_MIGRATION_NOTE' in workspace:
        errors.append('workspace density: technical migration note remains visible')
    for key in ['CMP_WS_ECO_TAB_MONEY', 'CMP_WS_ECO_TAB_MODIFIERS', 'CMP_WS_ECO_TAB_POLICIES']:
        if workspace.count(f'text = "{key}"') != 4:
            errors.append(f'workspace density: compact tab label parity failure for {key}')
    if workspace.count('name = "cmp_workspace_economy_help_card"') != 4:
        errors.append('workspace help: expected one Economy help card per profile')
    if workspace.count('multiline = yes autoresize = no') < 24:
        errors.append('workspace help: expected Economy help plus multiline Interface summary/help layouts')
    for profile_id in profile_ids:
        for topic in ['overview', 'money', 'modifiers', 'policies']:
            name = f'name = "cmp_workspace_economy_help_{topic}_{profile_id}"'
            if workspace.count(name) != 1:
                errors.append(f'workspace help: missing {topic}/{profile_id} scroll layout')
    for key in ['CMP_WS_ECO_TARGET_READY', 'CMP_WS_ECO_TARGET_REQUIRED', 'CMP_WS_ECONOMY_FOOTER']:
        if workspace.count(f'text = "{key}"') != 4:
            errors.append(f'workspace state: visible profile parity failure for {key}')

    # beta15.3.1.1: runtime screenshot showed the implementation note escaping
    # the Interface viewport. Keep only a short summary visible and move technical
    # details into a persistent scrollable help card.
    for key in ['CMP_WS_INTERFACE_DESC', 'CMP_WS_PROFILE_IMPL_NOTE']:
        if f'text = "{key}"' in workspace:
            errors.append(f'workspace interface: long always-visible text remains: {key}')
    if workspace.count('text = "CMP_WS_INTERFACE_SUMMARY"') != 4:
        errors.append('workspace interface: compact summary profile parity failure')
    if workspace.count('name = "cmp_workspace_interface_help_card"') != 4:
        errors.append('workspace interface: expected one persistent help card per profile')
    for profile_id in profile_ids:
        if workspace.count(f'name = "cmp_workspace_interface_help_{profile_id}"') != 1:
            errors.append(f'workspace interface: missing scrollable help layout for {profile_id}')

    economy_registry = json.loads(read(ROOT / 'registry/economy2.json'))
    economy_scrolls = {
        tab: len(re.findall(rf'name = "cmp_workspace_economy_{tab}_(?:compact|standard|large|xlarge)"', workspace))
        for tab in ['direct', 'modifiers', 'policies']
    }
    for tab, count in economy_scrolls.items():
        if count != 4:
            errors.append(f'workspace economy: expected four {tab} scroll layouts, got {count}')
    economy_endpoints = [
        *(f"cmp_economy2_select_parameter_{item['id']}" for item in economy_registry['parameters']),
        *(f"cmp_economy2_select_value_{item['id']}" for item in economy_registry['values']),
        *(f"cmp_economy2_policy_{item['id']}_{state}" for item in economy_registry['policies'] for state in ['enable', 'disable']),
        *(f"cmp_economy2_treasury_add_{step}" for step in economy_registry['money_steps_percent_of_reserve_cap']),
        *(f"cmp_economy2_investment_add_{step}" for step in economy_registry['money_steps_percent_of_reserve_cap']),
        'cmp_economy2_clear_debt', 'cmp_economy2_declare_bankruptcy', 'cmp_economy2_rescue_bankruptcy',
        'cmp_economy2_apply_selected', 'cmp_economy2_reset_selected', 'cmp_economy2_reset_all',
    ]
    economy_endpoint_counts = {endpoint: workspace.count(f"GetScriptedGui('{endpoint}')") for endpoint in economy_endpoints}
    bad_economy_endpoints = {endpoint: count for endpoint, count in economy_endpoint_counts.items() if count != 8}
    if bad_economy_endpoints:
        errors.append(f'workspace economy: endpoint profile parity failure: {bad_economy_endpoints}')

    # beta15.5.1 Regions & Buildings: category-filtered two-column object lists
    # scroll independently; configuration, warning and targets stay fixed.
    for profile_id in profile_ids:
        for picker in ['operations_building', 'operations_resource', 'staffing_building']:
            name = f'name = "cmp_workspace_regions_{picker}_picker_{profile_id}"'
            if workspace.count(name) != 1:
                errors.append(f'workspace regions: missing {picker}/{profile_id} picker scroll')
        for topic in ['overview', 'buildings', 'resources', 'presets', 'staffing']:
            name = f'name = "cmp_workspace_regions_help_{topic}_{profile_id}"'
            if workspace.count(name) != 1:
                errors.append(f'workspace regions help: missing {topic}/{profile_id} scroll layout')
    if workspace.count('name = "cmp_workspace_regions_help_card"') != 4:
        errors.append('workspace regions: expected one persistent help card per profile')
    if workspace.count('text = "CMP_WS_RB_SET_WARNING"') != 4:
        errors.append('workspace regions: persistent SET warning profile parity failure')
    if workspace.count('text = "CMP_WS_RB_FOOTER_IDLE"') != 4:
        errors.append('workspace regions: fixed result footer profile parity failure')
    if workspace.count("cmp_workspace_page', 'regions") < 8:
        errors.append('workspace regions: enabled navigation/profile visibility parity failure')
    for key in ['CMP_RB2_HINT', 'CMP_STAFF_HINT', 'CMP_STAFF_ADAPTIVE_HINT']:
        if f'text = "{key}"' in workspace:
            errors.append(f'workspace regions density: long always-visible description remains: {key}')

    resource_ids = set(regions_registry['resource_capable_buildings'])

    # beta17-pre3.1: Operations and Staffing share the same functional category
    # taxonomy, while retaining independent selector and category state.
    operation_categories = ui_registry.get('building_categories', [])
    staffing_categories = staffing_registry.get('categories', [])
    if [c.get('id') for c in operation_categories] != [c.get('id') for c in staffing_categories]:
        errors.append('workspace building operations categories: taxonomy differs from Staffing')
    operation_profile_to_category = {}
    for category in operation_categories[1:]:
        for profile in category.get('profiles', []):
            if profile in operation_profile_to_category:
                errors.append(f'workspace building operations categories: profile {profile} assigned to multiple categories')
            operation_profile_to_category[profile] = category['id']
    operation_category_counts = {
        category['id']: sum(1 for item in building_registry if item.get('staffing_profile') in category.get('profiles', []))
        for category in operation_categories[1:]
    }
    if len(operation_categories) != 8 or not operation_categories or operation_categories[0].get('id') != 'all':
        errors.append('workspace building operations categories: expected All plus seven coverage categories')
    if sum(operation_category_counts.values()) != len(building_registry):
        errors.append(f'workspace building operations categories: distribution mismatch: {operation_category_counts}')

    staffing_profile_to_category = {}
    for category in staffing_categories[1:]:
        for profile in category.get('profiles', []):
            if profile in staffing_profile_to_category:
                errors.append(f'workspace staffing categories: profile {profile} assigned to multiple categories')
            staffing_profile_to_category[profile] = category['id']
    staffing_category_counts = {
        category['id']: sum(1 for item in staffing_supported if staffing_profile_to_category.get(item['profile']) == category['id'])
        for category in staffing_categories[1:]
    }
    if len(staffing_categories) != 8 or not staffing_categories or staffing_categories[0].get('id') != 'all':
        errors.append('workspace staffing categories: expected All plus seven coverage categories')
    supported_profiles = {item['profile'] for item in staffing_supported}
    if set(staffing_profile_to_category) != supported_profiles:
        errors.append(f'workspace staffing categories: profile coverage mismatch: mapped={sorted(staffing_profile_to_category)}, supported={sorted(supported_profiles)}')
    if sum(staffing_category_counts.values()) != len(staffing_supported):
        errors.append(f'workspace staffing categories: distribution mismatch: {staffing_category_counts}')

    category_scroll_failures = []
    for profile_id in profile_ids:
        for instance in ['operations', 'staffing']:
            menu_name = f'name = "cmp_workspace_building_category_menu_{instance}_{profile_id}"'
            if workspace.count(menu_name) != 1:
                category_scroll_failures.append(menu_name)
        for category in operation_categories[1:]:
            name = f'name = "cmp_workspace_regions_operations_building_picker_{profile_id}_{category["id"]}"'
            if workspace.count(name) != 1:
                category_scroll_failures.append(name)
        for category in staffing_categories[1:]:
            name = f'name = "cmp_workspace_regions_staffing_building_picker_{profile_id}_{category["id"]}"'
            if workspace.count(name) != 1:
                category_scroll_failures.append(name)
    if category_scroll_failures:
        errors.append(f'workspace building categories: missing generated layouts: {category_scroll_failures}')
    category_menu_count = workspace.count('name = "cmp_workspace_building_category_menu_')
    category_filtered_scroll_count = sum(
        workspace.count(f'name = "cmp_workspace_regions_operations_building_picker_{profile_id}_{category["id"]}"')
        for profile_id in profile_ids for category in operation_categories[1:]
    ) + sum(
        workspace.count(f'name = "cmp_workspace_regions_staffing_building_picker_{profile_id}_{category["id"]}"')
        for profile_id in profile_ids for category in staffing_categories[1:]
    )
    expected_filtered_scrolls = len(profile_ids) * ((len(operation_categories) - 1) + (len(staffing_categories) - 1))
    if category_menu_count != 8 or category_filtered_scroll_count != expected_filtered_scrolls:
        errors.append(f'workspace building categories: layout totals menu={category_menu_count}/8, filtered_scroll={category_filtered_scroll_count}/{expected_filtered_scrolls}')

    operation_category_selector_failures = {
        category['id']: workspace.count(f"GetVariableSystem.Set('cmp_workspace_building_category', '{category['id']}')")
        for category in operation_categories
        if workspace.count(f"GetVariableSystem.Set('cmp_workspace_building_category', '{category['id']}')") != 4
    }
    staffing_category_selector_failures = {
        category['id']: workspace.count(f"GetVariableSystem.Set('cmp_workspace_staffing_category', '{category['id']}')")
        for category in staffing_categories
        if workspace.count(f"GetVariableSystem.Set('cmp_workspace_staffing_category', '{category['id']}')") != 4
    }
    category_selector_failures = {
        'operations': operation_category_selector_failures,
        'staffing': staffing_category_selector_failures,
    }
    if operation_category_selector_failures or staffing_category_selector_failures:
        errors.append(f'workspace building categories: selector profile parity failure: {category_selector_failures}')
    if "cmp_workspace_building_category_menu'" in workspace:
        errors.append('workspace building categories: obsolete shared category menu variable remains')
    for menu_variable in ['cmp_workspace_building_category_menu_operations', 'cmp_workspace_building_category_menu_staffing']:
        if workspace.count(menu_variable) < 4:
            errors.append(f'workspace building categories: {menu_variable} profile parity incomplete')

    building_endpoint_counts = {}
    for item in building_registry:
        endpoint = f"cmp_regions2_select_building_{item['id']}"
        count = workspace.count(f"GetScriptedGui('{endpoint}')")
        building_endpoint_counts[endpoint] = count
        if count != 16:
            errors.append(f'workspace regions: building endpoint {endpoint} count {count}, expected 16 (Execute + IsValid in All + category across four profiles)')
        if item['id'] in resource_ids:
            resource_endpoint = f"cmp_regions2_select_resource_{item['id']}"
            resource_count = workspace.count(f"GetScriptedGui('{resource_endpoint}')")
            building_endpoint_counts[resource_endpoint] = resource_count
            if resource_count != 8:
                errors.append(f'workspace regions: resource endpoint {resource_endpoint} count {resource_count}, expected 8 (Execute + IsValid across four profiles)')
    regions_action_endpoints = [
        *(f"cmp_regions2_select_operation_{op}" for op in ['add', 'set', 'remove']),
        *(f"cmp_regions2_select_amount_{amount}" for amount in regions_registry['building_amounts']),
        *(f"cmp_staffing_select_amount_{amount}" for amount in [1000, 5000, 10000, 25000, 50000, 100000]),
        'cmp_staffing_select_adaptive_off',
        *(f"cmp_staffing_select_adaptive_{amount}" for amount in regions_registry['staffing_occupancy_targets']),
    ]
    bad_regions_actions = {
        endpoint: workspace.count(f"GetScriptedGui('{endpoint}')")
        for endpoint in regions_action_endpoints
        if workspace.count(f"GetScriptedGui('{endpoint}')") != 8
    }
    if bad_regions_actions:
        errors.append(f'workspace regions: four-profile selector endpoint parity failure: {bad_regions_actions}')
    target_endpoint_expectations = {
        'cmp_regions2_apply_player_marked': 16,
        'cmp_regions2_apply_incorporated': 16,
        'cmp_regions2_apply_foreign': 16,
        'cmp_staffing_apply_player_marked': 8,
        'cmp_staffing_apply_player_incorporated': 8,
        'cmp_staffing_apply_marked_country': 8,
    }
    bad_regions_targets = {
        endpoint: workspace.count(f"GetScriptedGui('{endpoint}')")
        for endpoint, expected in target_endpoint_expectations.items()
        if workspace.count(f"GetScriptedGui('{endpoint}')") != expected
    }
    if bad_regions_targets:
        errors.append(f'workspace regions: target endpoint parity failure: {bad_regions_targets}')

    # beta15.5 Population & Society: four compact tabs, a fixed target/result
    # layer and persistent scrollable help. Existing scripted gameplay endpoints
    # are reused without changing their implementation.
    population_scrolls = {
        tab: len(re.findall(rf'name = "cmp_workspace_population_{tab}_(?:compact|standard|large|xlarge)"', workspace))
        for tab in ['population', 'professions', 'welfare', 'society']
    }
    for tab, count in population_scrolls.items():
        if count != 4:
            errors.append(f'workspace population: expected four {tab} scroll layouts, got {count}')
    for profile_id in profile_ids:
        for topic in ['overview', 'population', 'professions', 'welfare', 'society']:
            name = f'name = "cmp_workspace_population_help_{topic}_{profile_id}"'
            if workspace.count(name) != 1:
                errors.append(f'workspace population help: missing {topic}/{profile_id} scroll layout')
    if workspace.count('name = "cmp_workspace_population_help_card"') != 4:
        errors.append('workspace population: expected one persistent help card per profile')
    if workspace.count('text = "CMP_WS_POP_FOOTER_IDLE"') != 4:
        errors.append('workspace population: fixed result footer profile parity failure')
    if workspace.count("cmp_workspace_page', 'population") < 8:
        errors.append('workspace population: enabled navigation/profile visibility parity failure')
    if workspace.count("GetScriptedGui('cmp_pop2_target_valid')") != 8:
        errors.append('workspace population: fixed state-target status parity failure')
    for key in ['CMP_POP2_DESC', 'CMP_POP2_POP_DESC', 'CMP_POP2_LITERACY_DESC',
                'CMP_POP2_PROF_DESC', 'CMP_POP2_QUAL_DESC', 'CMP_POP2_WELFARE_DESC',
                'CMP_POP2_SOCIETY_DESC']:
        if f'text = "{key}"' in workspace:
            errors.append(f'workspace population density: long always-visible description remains: {key}')

    population_endpoints = [
        *(f"cmp_pop2_select_amount_{item['id']}" for item in population_registry['amounts']),
        *(f"cmp_pop2_select_literacy_{item['id']}" for item in population_registry['literacy']),
        *(f"cmp_pop2_select_profession_{item['id']}" for item in population_registry['professions']),
        *(f"cmp_pop2_select_qualification_{item['id']}" for item in population_registry['qualifications']),
        *(f"cmp_pop2_select_wealth_{item['id']}" for item in population_registry['wealth']),
        *(f"cmp_pop2_loyalists_{item['id']}" for item in population_registry['social_steps']),
        *(f"cmp_pop2_radicals_{item['id']}" for item in population_registry['social_steps']),
        *(f"cmp_pop2_reduce_radicals_{item['id']}" for item in population_registry['social_steps']),
        *(f"cmp_pop2_migration_{item['id']}" for item in population_registry['migration']),
        *(f"cmp_pop2_workforce_{item['id']}" for item in population_registry['workforce']),
        'cmp_pop2_add_population', 'cmp_pop2_remove_population', 'cmp_pop2_set_literacy',
        'cmp_pop2_spawn_profession', 'cmp_pop2_set_qualification', 'cmp_pop2_set_wealth',
        'cmp_pop2_neutralize', 'cmp_pop2_clear_society_modifiers',
        'cmp_pop2_toggle_society_confirmation', 'cmp_pop2_assimilate',
        'cmp_pop2_convert_religion', 'cmp_pop2_preset_industrial',
        'cmp_pop2_preset_educated', 'cmp_pop2_preset_stable',
    ]
    population_endpoint_counts = {
        endpoint: workspace.count(f"GetScriptedGui('{endpoint}')")
        for endpoint in population_endpoints
    }
    amount_endpoints = {f"cmp_pop2_select_amount_{item['id']}" for item in population_registry['amounts']}
    bad_population_endpoints = {
        endpoint: count for endpoint, count in population_endpoint_counts.items()
        if count != (16 if endpoint in amount_endpoints else 8)
    }
    if bad_population_endpoints:
        errors.append(f'workspace population: endpoint profile parity failure: {bad_population_endpoints}')

    # beta15.6 Politics & Characters: five compact tabs, tab-dependent target
    # status, content-only scrolling and persistent help. Existing Politics 2.0
    # gameplay endpoints are reused without changing their effects.
    politics_registry = json.loads(read(ROOT / 'registry/politics2.json'))
    politics_tabs = ['government', 'characters', 'interest_groups', 'laws', 'bloc']
    politics_scrolls = {
        tab: len(re.findall(rf'name = "cmp_workspace_politics_{tab}_(?:compact|standard|large|xlarge)"', workspace))
        for tab in politics_tabs
    }
    for tab, count in politics_scrolls.items():
        if count != 4:
            errors.append(f'workspace politics: expected four {tab} scroll layouts, got {count}')
    for profile_id in profile_ids:
        for topic in ['overview', 'government', 'characters', 'interest_groups', 'laws', 'bloc']:
            name = f'name = "cmp_workspace_politics_help_{topic}_{profile_id}"'
            if workspace.count(name) != 1:
                errors.append(f'workspace politics help: missing {topic}/{profile_id} scroll layout')
    if workspace.count('name = "cmp_workspace_politics_help_card"') != 4:
        errors.append('workspace politics: expected one persistent help card per profile')
    if workspace.count('text = "CMP_WS_POL_FOOTER_IDLE"') != 4:
        errors.append('workspace politics: fixed result footer profile parity failure')
    if workspace.count("cmp_workspace_page', 'politics") < 8:
        errors.append('workspace politics: enabled navigation/profile visibility parity failure')
    if workspace.count('text = "CMP_WS_POL_ROLE_WARNING"') != 4:
        errors.append('workspace politics: destructive role warning profile parity failure')
    if workspace.count('text = "CMP_WS_POL_IG_WARNING"') != 4:
        errors.append('workspace politics: political-strength warning profile parity failure')
    if workspace.count('text = "CMP_WS_POL_LAW_WARNING"') != 4:
        errors.append('workspace politics: law warning profile parity failure')
    for key in ['CMP_POL2_DESC', 'CMP_POL2_GOV_DESC', 'CMP_POL2_CHAR_DESC',
                'CMP_POL2_IG_DESC', 'CMP_POL2_IG_STRENGTH_NOTE',
                'CMP_POL2_LAW_DESC', 'CMP_POL2_BLOC_DESC', 'CMP_POL2_BLOC_NOTE',
                'CMP_POL2_AGE_NOTE']:
        if f'text = "{key}"' in workspace:
            errors.append(f'workspace politics density: long always-visible description remains: {key}')
    politics_endpoints = [
        *(f"cmp_politics2_select_gov_param_{number}" for number in range(1, 5)),
        *(f"cmp_politics2_select_gov_value_{value}" for value in [10, 25, 50, 100]),
        'cmp_politics2_gov_apply', 'cmp_politics2_gov_reset',
        *(f"cmp_politics2_select_inst_{number}" for number in range(1, 8)),
        *(f"cmp_politics2_select_inst_level_{number}" for number in range(1, 6)),
        'cmp_politics2_institution_apply',
        'cmp_politics2_char_immortal_on', 'cmp_politics2_char_immortal_off',
        'cmp_politics2_char_health_0p05', 'cmp_politics2_char_health_0p2',
        'cmp_politics2_char_health_1p0', 'cmp_politics2_char_health_reset',
        'cmp_politics2_char_popularity_5', 'cmp_politics2_char_popularity_25',
        'cmp_politics2_char_popularity_100', 'cmp_politics2_char_popularity_reset',
        *(f"cmp_politics2_char_rank_{number}" for number in range(1, 6)),
        'cmp_politics2_char_role_general_add', 'cmp_politics2_char_role_general_remove',
        'cmp_politics2_char_role_admiral_add', 'cmp_politics2_char_role_admiral_remove',
        *(f"cmp_politics2_char_trait_{trait['id']}_{action}"
          for trait in politics_registry['traits'] for action in ['add', 'remove']),
        *(f"cmp_politics2_ig_toggle_{group['id']}" for group in politics_registry['interest_groups']),
        *(f"cmp_politics2_ig_approval_{suffix}" for suffix in ['5', '10', '20', 'n5', 'n10', '0']),
        *(f"cmp_politics2_ig_strength_{suffix}" for suffix in ['25', '50', '100', '500', 'n50', '0']),
        'cmp_politics2_law_progress_10', 'cmp_politics2_law_progress_25',
        'cmp_politics2_law_advance', 'cmp_politics2_law_setback',
        'cmp_politics2_law_complete', 'cmp_politics2_law_cancel',
        'cmp_politics2_law_clear_modifiers',
        'cmp_politics2_bloc_cohesion_p25', 'cmp_politics2_bloc_cohesion_p50',
        'cmp_politics2_bloc_cohesion_n25', 'cmp_politics2_bloc_cohesion_100',
        'cmp_politics2_feedback_clear',
    ]
    politics_endpoint_counts = {
        endpoint: workspace.count(f"GetScriptedGui('{endpoint}')")
        for endpoint in politics_endpoints
    }
    bad_politics_endpoints = {
        endpoint: count for endpoint, count in politics_endpoint_counts.items()
        if count != (8 if endpoint == 'cmp_politics2_feedback_clear' else
                     12 if endpoint.startswith('cmp_politics2_bloc_cohesion_') else 8)
    }
    if bad_politics_endpoints:
        errors.append(f'workspace politics: endpoint profile parity failure: {bad_politics_endpoints}')
    politics_target_expected = {
        'cmp_politics2_country_target_valid': 16,
        'cmp_politics2_character_target_valid': 8,
        'cmp_politics2_law_target_valid': 8,
        'cmp_politics2_bloc_target_valid': 32,
    }
    bad_politics_targets = {
        endpoint: workspace.count(f"GetScriptedGui('{endpoint}')")
        for endpoint, expected in politics_target_expected.items()
        if workspace.count(f"GetScriptedGui('{endpoint}')") != expected
    }
    if bad_politics_targets:
        errors.append(f'workspace politics: target-status parity failure: {bad_politics_targets}')

    # beta16-pre2 Diplomacy & Sovereignty: five compact tabs and six persistent
    # help topics. Locally verified B7 operations and Power Bloc cohesion remain;
    # two direct membership actions add one-use confirmation and postconditions.
    diplomacy_registry = json.loads(read(ROOT / 'registry/diplomacy2.json'))
    diplomacy_tabs = ['relations', 'subjects', 'treaties', 'sovereignty', 'power_bloc']
    diplomacy_scrolls = {
        tab: len(re.findall(rf'name = "cmp_workspace_diplomacy_{tab}_(?:compact|standard|large|xlarge)"', workspace))
        for tab in diplomacy_tabs
    }
    for tab, count in diplomacy_scrolls.items():
        if count != 4:
            errors.append(f'workspace diplomacy: expected four {tab} scroll layouts, got {count}')
    diplomacy_help_topics = ['overview', 'relations', 'subjects', 'treaties', 'sovereignty', 'power_bloc']
    for profile_id in profile_ids:
        for topic in diplomacy_help_topics:
            name = f'name = "cmp_workspace_diplomacy_help_{topic}_{profile_id}"'
            if workspace.count(name) != 1:
                errors.append(f'workspace diplomacy help: missing {topic}/{profile_id} scroll layout')
    if workspace.count('name = "cmp_workspace_diplomacy_help_card"') != 4:
        errors.append('workspace diplomacy: expected one persistent help card per profile')
    if workspace.count("cmp_workspace_page', 'diplomacy") < 8:
        errors.append('workspace diplomacy: enabled navigation/profile visibility parity failure')
    if workspace.count('text = "CMP_WS_DIP_SOV_WARNING"') != 4:
        errors.append('workspace diplomacy: destructive state-transfer warning profile parity failure')
    if workspace.count('text = "CMP_WS_DIP_BLOC_DEFERRED"') != 4:
        errors.append('workspace diplomacy: deferred Power Bloc scope notice profile parity failure')
    if workspace.count('text = "CMP_WS_DIP_BLOC_MEMBERSHIP_WARNING"') != 4:
        errors.append('workspace diplomacy: forced-membership warning profile parity failure')
    if workspace.count('text = "CMP_WS_DIP_BLOC_CONFIRM"') != 4:
        errors.append('workspace diplomacy: forced-membership confirmation profile parity failure')
    if workspace.count("GetVariableSystem.Toggle('cmp_workspace_diplomacy_confirm')") != 4:
        errors.append('workspace diplomacy: expected one confirmation toggle per profile')
    if workspace.count("GetVariableSystem.Clear('cmp_workspace_diplomacy_confirm')") != 40:
        errors.append('workspace diplomacy: one-action confirmation reset contract changed')
    diplomacy_endpoints = [
        *(item['endpoint'] for item in diplomacy_registry['relations']),
        *(item['endpoint'] for item in diplomacy_registry['obligations']),
        *(item[direction] for item in diplomacy_registry['subject_types'] for direction in ['forward', 'reverse']),
        *(item['endpoint'] for item in diplomacy_registry['subject_actions']),
        *(item[action] for item in diplomacy_registry['treaties'] for action in ['create', 'remove']),
        *(item['endpoint'] for item in diplomacy_registry['sovereignty']),
        *(item['endpoint'] for item in diplomacy_registry['power_bloc_safe']),
        *(item['endpoint'] for item in diplomacy_registry['power_bloc_membership']),
    ]
    if len(diplomacy_endpoints) != 60 or len(set(diplomacy_endpoints)) != 60:
        errors.append(f'workspace diplomacy: registry must expose 60 unique audited actions, got {len(diplomacy_endpoints)}/{len(set(diplomacy_endpoints))}')
    diplomacy_endpoint_counts = {
        endpoint: workspace.count(f"GetScriptedGui('{endpoint}')")
        for endpoint in diplomacy_endpoints
    }
    diplomacy_endpoint_expected = {
        endpoint: (4 if endpoint.startswith('cmp_diplomacy2_membership_') else
                   12 if endpoint.startswith('cmp_politics2_bloc_cohesion_') else
                   8 if endpoint == 'sakuya_b7_fx_player_independent' else 4)
        for endpoint in diplomacy_endpoints
    }
    bad_diplomacy_endpoints = {
        endpoint: {'count': diplomacy_endpoint_counts[endpoint], 'expected': expected}
        for endpoint, expected in diplomacy_endpoint_expected.items()
        if diplomacy_endpoint_counts[endpoint] != expected
    }
    if bad_diplomacy_endpoints:
        errors.append(f'workspace diplomacy: endpoint profile parity failure: {bad_diplomacy_endpoints}')
    forbidden_diplomacy_endpoint_fragments = [
        'sakuya_b6_fx_leverage', 'sakuya_b6_fx_join', 'sakuya_b6_fx_invite', 'principle_',
        'sakuya_b7_fx_annex_country', 'sakuya_b7_fx_switch_country',
    ]
    leaked_diplomacy_endpoints = [
        fragment for fragment in forbidden_diplomacy_endpoint_fragments
        if re.search(rf"GetScriptedGui\('[^']*{re.escape(fragment)}", workspace)
    ]
    if leaked_diplomacy_endpoints:
        errors.append(f'workspace diplomacy: unverified/deferred endpoints leaked into UI: {leaked_diplomacy_endpoints}')
    if workspace.count("GetScriptedGui('cmp_b7_feedback_clear')") != 4:
        errors.append('workspace diplomacy: B7 result-clear profile parity failure')
    if workspace.count("GetScriptedGui('cmp_diplomacy2_membership_player_join')") != 4:
        errors.append('workspace diplomacy: player forced-membership endpoint profile parity failure')
    if workspace.count("GetScriptedGui('cmp_diplomacy2_membership_country_join')") != 4:
        errors.append('workspace diplomacy: marked-country forced-membership endpoint profile parity failure')
    membership_effects = (ROOT / 'common/scripted_effects/cmp_diplomacy2_effects.txt').read_text(encoding='utf-8-sig')
    if membership_effects.count('join_power_bloc = scope:cmp_diplomacy2_bloc_leader_scope') != 2:
        errors.append('workspace diplomacy: expected exactly two audited direct-join commands')
    for value in ['value = 1', 'value = -1', 'value = -2', 'value = -3', 'value = -4']:
        if value not in membership_effects:
            errors.append(f'workspace diplomacy: missing membership feedback state {value}')
    for endpoint in [
        'cmp_diplomacy2_feedback_joined',
        'cmp_diplomacy2_feedback_bloc_required',
        'cmp_diplomacy2_feedback_country_required',
        'cmp_diplomacy2_feedback_already_member',
        'cmp_diplomacy2_feedback_join_failed',
    ]:
        if workspace.count(f"GetScriptedGui('{endpoint}')") != 8:
            errors.append(f'workspace diplomacy: feedback profile parity failure for {endpoint}')

    # beta15.7 Army & Navy: five compact top-level tabs, role-filtered unit
    # lists, four army-template submodes, two fleet-template submodes and
    # persistent help. All controls reuse the established ScriptedGui contract.
    military_scroll_patterns = {
        'army_picker': r'name = "cmp_workspace_military_army_picker_(?:infantry|artillery|mobile)_(?:compact|standard|large|xlarge)"',
        'army_templates': r'name = "cmp_workspace_military_army_template_(?:quick|mixed|designer|marines)_(?:compact|standard|large|xlarge)"',
        'army_controls': r'name = "cmp_workspace_military_army_controls_(?:compact|standard|large|xlarge)"',
        'fleet_builder_new': r'name = "cmp_workspace_navy18_new_(?:compact|standard|large|xlarge)"',
        'fleet_builder_existing': r'name = "cmp_workspace_navy18_existing_(?:compact|standard|large|xlarge)"',
        'fleet_shipctrl': r'name = "cmp_workspace_navy18_shipctrl_(?:compact|standard|large|xlarge)"',
        'fleet_transfer': r'name = "cmp_workspace_navy18_transfer_(?:compact|standard|large|xlarge)"',
        'fleet_logistics': r'name = "cmp_workspace_navy18_logistics_(?:compact|standard|large|xlarge)"',
        'fleet_templates': r'name = "cmp_workspace_military_fleet_template_(?:designer|taskforce)_(?:compact|standard|large|xlarge)"',
        'fleet_picker': r'name = "cmp_workspace_fleet_picker_scroll_(?:compact|standard|large|xlarge)"',
    }
    expected_military_scrolls = {
        'army_picker': 12, 'army_templates': 16, 'army_controls': 4,
        'fleet_builder_new': 4, 'fleet_builder_existing': 4, 'fleet_shipctrl': 4, 'fleet_transfer': 4, 'fleet_logistics': 4, 'fleet_templates': 8, 'fleet_picker': 4,
    }
    military_scrolls = {name: len(re.findall(pattern, workspace)) for name, pattern in military_scroll_patterns.items()}
    if military_scrolls != expected_military_scrolls:
        errors.append(f'workspace military: active-content scroll layout mismatch: {military_scrolls}')
    military_help_topics = ['overview', 'army_builder', 'army_templates', 'army_controls',
                            'fleet_builder', 'fleet_templates', 'marines', 'taskforce']
    for profile_id in profile_ids:
        for topic in military_help_topics:
            name = f'name = "cmp_workspace_military_help_{topic}_{profile_id}"'
            if workspace.count(name) != 1:
                errors.append(f'workspace military help: missing {topic}/{profile_id} scroll layout')
    if workspace.count('name = "cmp_workspace_military_help_card"') != 4:
        errors.append('workspace military: expected one persistent help card per profile')
    if workspace.count("cmp_workspace_page', 'military") < 8:
        errors.append('workspace military: enabled navigation/profile visibility parity failure')
    if workspace.count('text = "CMP_WS_MIL_MANUAL_ATTACH_WARNING"') != 8:
        errors.append('workspace military: manual-attachment warning must remain visible in Marines and Task Force for every profile')
    for key in ['CMP_ARMY_BUILDER_DESC', 'CMP_ARMY_MIXED_DESC', 'CMP_ARMY_DESIGNER_DESC',
                'CMP_ARMY_CONTROL_DESC', 'CMP_FLEET_DESC', 'CMP_FD_DESC',
                'CMP_TASKFORCE_DESC']:
        if f'text = "{key}"' in workspace:
            errors.append(f'workspace military density: long always-visible description remains: {key}')

    military_bad_endpoints = {}
    military_expected_endpoints = {}
    def expect_endpoint(endpoint: str, expected: int) -> None:
        military_expected_endpoints[endpoint] = expected
        count = workspace.count(f"GetScriptedGui('{endpoint}')")
        if count != expected:
            military_bad_endpoints[endpoint] = {'count': count, 'expected': expected}

    for item in land_units_registry:
        unit_id = item['id']
        expect_endpoint(f'cmp_army_builder_select_{unit_id}', 4)
        expect_endpoint(f'cmp_army_builder_unit_{unit_id}_available', 4)
        expect_endpoint(f'cmp_army_builder_unit_{unit_id}_selected', 4)
    for value in [1, 5, 10, 25, 50]:
        expect_endpoint(f'cmp_army_builder_select_amount_{value}', 8)
        expect_endpoint(f'cmp_army_builder_amount_{value}_selected', 4)
    for endpoint in ['cmp_army_builder_preset_infantry_corps', 'cmp_army_builder_preset_artillery_group',
                     'cmp_army_builder_preset_mobile_corps', 'cmp_army_builder_preset_marine_force']:
        expect_endpoint(endpoint, 8)
    expect_endpoint('cmp_army_builder_apply', 16)
    expect_endpoint('cmp_army_builder_clear', 16)
    for profile_name in ['balanced', 'infantry_heavy', 'breakthrough', 'armored_fist']:
        expect_endpoint(f'cmp_army_mixed_select_{profile_name}', 8)
        expect_endpoint(f'cmp_army_mixed_{profile_name}_selected', 4)
    for endpoint in ['cmp_army_mixed_apply', 'cmp_army_mixed_clear']:
        expect_endpoint(endpoint, 8)
    for value in [25, 50, 75, 100]:
        expect_endpoint(f'cmp_army_designer_select_size_{value}', 8)
        expect_endpoint(f'cmp_army_designer_size_{value}_selected', 4)
    for value in [40, 50, 60, 70]:
        expect_endpoint(f'cmp_army_designer_select_inf_{value}', 8)
        expect_endpoint(f'cmp_army_designer_inf_{value}_selected', 4)
    for value in [10, 20, 30]:
        expect_endpoint(f'cmp_army_designer_select_art_{value}', 8)
        expect_endpoint(f'cmp_army_designer_art_{value}_selected', 4)
    for endpoint in ['cmp_army_designer_apply', 'cmp_army_designer_clear']:
        expect_endpoint(endpoint, 8)
    for value in [5, 10, 25, 50]:
        expect_endpoint(f'cmp_army_amphib_select_amount_{value}', 16)
        expect_endpoint(f'cmp_army_amphib_amount_{value}_selected', 8)
    for endpoint in ['cmp_army_amphib_apply', 'cmp_army_amphib_clear']:
        expect_endpoint(endpoint, 8)
    control_params = ['offense', 'defense', 'morale_recovery', 'mobilization', 'experience',
                      'movement', 'supply', 'goods_cost', 'wages', 'war_exhaustion']
    for param in control_params:
        expect_endpoint(f'cmp_army_controls_select_parameter_{param}', 8)
        expect_endpoint(f'cmp_army_controls_parameter_{param}_selected', 4)
    for value in range(1, 6):
        expect_endpoint(f'cmp_army_controls_select_value_{value}', 8)
        expect_endpoint(f'cmp_army_controls_value_{value}_selected', 4)
    for endpoint in ['cmp_army_controls_select_target_self', 'cmp_army_controls_select_target_marked',
                     'cmp_army_controls_preset_balanced', 'cmp_army_controls_preset_rapid',
                     'cmp_army_controls_preset_economy', 'cmp_army_controls_preset_god',
                     'cmp_army_controls_apply', 'cmp_army_controls_reset_parameter',
                     'cmp_army_controls_reset_all']:
        expect_endpoint(endpoint, 8)
    for item in ships_registry:
        ship_id = item['id']
        expect_endpoint(f'cmp_fleet_builder_select_{ship_id}', 4)
        expect_endpoint(f'cmp_fleet_builder_ship_{ship_id}_available', 4)
        expect_endpoint(f'cmp_fleet_builder_ship_{ship_id}_selected', 4)
    for item in fleet_registry['amounts']:
        value = item['value']
        expect_endpoint(f'cmp_fleet_builder_select_amount_{value}', 8)
        expect_endpoint(f'cmp_fleet_builder_amount_{value}_selected', 4)
    # beta18-pre3 Fleet Composer 2.0 uses five row-local full-catalog hull pickers.
    for preset in navy18_registry['presets']:
        expect_endpoint(f"cmp_navy18_preset_{preset['id']}", 8)
    rows = range(1, navy18_registry['composer2']['rows'] + 1)
    composer_amounts = navy18_registry['composer2']['amounts']
    for hull in naval_catalog_registry['combat_hulls']:
        sid = hull['id']
        # Same availability endpoint is reused by each of 5 row pickers in all 4 profiles.
        expect_endpoint(f'cmp_navy18_comp2_hull_{sid}_available', navy18_registry['composer2']['rows'] * 4)
    for row in rows:
        expect_endpoint(f'cmp_navy18_comp2_row_{row}_has_hull', 4)
        for hull in naval_catalog_registry['combat_hulls']:
            sid = hull['id']
            expect_endpoint(f'cmp_navy18_comp2_select_row_{row}_hull_{sid}', 4)
            # One selected-name state on the main surface + one selected line in the row picker.
            expect_endpoint(f'cmp_navy18_comp2_row_{row}_hull_{sid}_selected', 8)
        for value in composer_amounts:
            expect_endpoint(f'cmp_navy18_comp2_select_row_{row}_count_{value}', 8)
            expect_endpoint(f'cmp_navy18_comp2_row_{row}_count_{value}_selected', 4)
    expect_endpoint('cmp_navy18_comp2_create_fleet', 8)
    expect_endpoint('cmp_navy18_comp2_clear', 8)
    expect_endpoint('cmp_navy18_has_marked_port_state', 16)
    expect_endpoint('cmp_navy18_comp2_ready', 8)
    # beta18-pre4 Exact Ship Control renders one 100-slot exact selector per Workspace profile.
    for slot in range(1, navy18_registry['ship_control']['max_slots'] + 1):
        expect_endpoint(f'cmp_navy18_shipctrl_select_slot_{slot}', 8)
        expect_endpoint(f'cmp_navy18_shipctrl_slot_{slot}_selected', 4)
    for hull in naval_catalog_registry['combat_hulls']:
        expect_endpoint(f"cmp_navy18_shipctrl_type_{hull['id']}", 8)
    shipctrl_expected = {
        'cmp_navy18_shipctrl_has_ship': 8,
        'cmp_navy18_shipctrl_target_lost': 4,
        'cmp_navy18_shipctrl_clear': 8,
        'cmp_navy18_shipctrl_set_flagship': 8,
        'cmp_navy18_shipctrl_unset_flagship': 8,
        'cmp_navy18_shipctrl_flagship': 4,
        'cmp_navy18_shipctrl_not_flagship': 4,
        'cmp_navy18_shipctrl_damaged': 4,
        'cmp_navy18_shipctrl_healthy': 4,
        'cmp_navy18_shipctrl_in_port': 4,
        'cmp_navy18_shipctrl_at_sea': 4,
        'cmp_navy18_shipctrl_in_battle': 4,
        'cmp_navy18_shipctrl_not_in_battle': 4,
    }
    for endpoint, expected in shipctrl_expected.items():
        expect_endpoint(endpoint, expected)
    # beta18-pre5 Exact Ship Transfers: marked receiver + single Ship + cross-fleet basket.
    transfer_expected = {
        'cmp_navy18_transfer_receiver_ready': 4,
        'cmp_navy18_transfer_receiver_missing': 4,
        'cmp_navy18_transfer_receiver_self': 4,
        'cmp_navy18_transfer_receiver_no_port': 4,
        'cmp_navy18_transfer_exact_eligible': 8,
        'cmp_navy18_transfer_has_batch': 4,
        'cmp_navy18_transfer_batch_valid': 4,
        'cmp_navy18_transfer_batch_invalid': 4,
        'cmp_navy18_transfer_add_exact': 16,
        'cmp_navy18_transfer_remove_exact': 16,
        'cmp_navy18_transfer_clear_batch': 8,
        'cmp_navy18_transfer_single': 8,
        'cmp_navy18_transfer_batch': 8,
        'cmp_navy18_transfer_result_added': 4,
        'cmp_navy18_transfer_result_removed': 4,
        'cmp_navy18_transfer_result_single': 4,
        'cmp_navy18_transfer_result_batch': 4,
        'cmp_navy18_transfer_result_cleared': 4,
    }
    for endpoint, expected in transfer_expected.items():
        expect_endpoint(endpoint, expected)
    for value in range(1, navy18_registry['transfer']['batch_max'] + 1):
        expect_endpoint(f'cmp_navy18_transfer_batch_count_{value}', 4)
    # beta18-pre5.1 Retrofit & Naval Logistics.
    for value in navy18_registry['naval_logistics']['supply_add_amounts']:
        expect_endpoint(f'cmp_navy18_supply_add_{value}', 8)
        expect_endpoint(f'cmp_navy18_supply_result_{value}', 4)
    for endpoint in [
        'cmp_navy18_supply_maintenance_good','cmp_navy18_supply_maintenance_medium','cmp_navy18_supply_maintenance_bad',
        'cmp_navy18_supply_assigned_0','cmp_navy18_supply_assigned_1','cmp_navy18_supply_assigned_2','cmp_navy18_supply_assigned_3','cmp_navy18_supply_assigned_4','cmp_navy18_supply_assigned_5',
        'cmp_navy18_supply_assigned_6_10','cmp_navy18_supply_assigned_11_20','cmp_navy18_supply_assigned_21_50','cmp_navy18_supply_assigned_51_plus'
    ]:
        expect_endpoint(endpoint, 4)
    for hull in naval_catalog_registry['combat_hulls']:
        for value in naval_catalog_registry['catalog_amounts']:
            expect_endpoint(f"cmp_navy18_catalog_create_{hull['id']}_{value}", 8)
    # beta18-pre2.4 picker uses the vanilla military-formation panel bridge plus independent row scope proofs.
    # Selected-formation direct apply remains gated until runtime proves GetSelectedFormation updates in this context.
    for endpoint, count in {
        'cmp_fleet_builder_apply_native': 8,
        'cmp_fleet_builder_clear': 8,
        'cmp_military_native_fleet_root_probe': 8,
        'cmp_military_native_fleet_owner_probe': 4,
        'cmp_military_native_fleet_ready': 16,
        'cmp_military_native_fleet_blocked_battle': 16,
    }.items():
        expect_endpoint(endpoint, count)
    for token in ['Country.GetMilitaryFormationsFleet', 'MilitaryFormation.GetNameNoFormatting',
                  "InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')",
                  'GetSelectedFormation', 'GuiScope.SetRoot(MilitaryFormation.MakeScope).End']:
        if workspace.count(token) < 4:
            errors.append(f'workspace military: native fleet-selection token missing: {token}')
    if 'FormationPanel.SelectFormation(MilitaryFormation.Self)' in workspace:
        errors.append('workspace military: context-dependent FormationPanel.SelectFormation leaked into pre2.4')
    for forbidden in [
        "AddScope('formation', MilitaryFormation.MakeScope)",
        "GetScriptedGui('cmp_military_target_fleet_select')",
        "GetScriptedGui('cmp_military_target_fleet_entry_selected')",
        "GetScriptedGui('cmp_military_target_fleet_clear')",
        'cmp_military_target_fleet_open', 'cmp_military_target.1',
        'sakuya_main_04_01_mark_navy_player_all'
    ]:
        if forbidden in workspace:
            errors.append(f'workspace military: legacy fleet target path leaked into production shell: {forbidden}')
    for group, values in [('size', [10, 20, 40]), ('escort', [20, 40, 60]),
                          ('carrier', [0, 10, 20]), ('sub', [0, 20, 40])]:
        for value in values:
            expect_endpoint(f'cmp_fleet_designer_select_{group}_{value}', 8)
            expect_endpoint(f'cmp_fleet_designer_{group}_{value}_selected', 4)
    for endpoint in ['cmp_fleet_designer_profile_battle', 'cmp_fleet_designer_profile_carrier',
                     'cmp_fleet_designer_profile_escort', 'cmp_fleet_designer_profile_wolfpack',
                     'cmp_fleet_designer_profile_amphibious', 'cmp_fleet_designer_apply',
                     'cmp_fleet_designer_clear', 'cmp_fleet_taskforce_prepare']:
        expect_endpoint(endpoint, 8)
    if military_bad_endpoints:
        errors.append(f'workspace military: endpoint profile parity failure: {military_bad_endpoints}')

    loc_report = {}
    untranslated = []
    forbidden_hits = []
    localization_header_errors = []
    localization_files_checked = 0
    for language in ['english', 'russian']:
        expected_header = f'l_{language}:'
        for path in sorted((LOC / language).glob('*.yml')):
            localization_files_checked += 1
            raw = path.read_bytes()
            if not raw.startswith(codecs.BOM_UTF8):
                localization_header_errors.append(f'{path.relative_to(ROOT)}: missing UTF-8 BOM')
                continue
            body = raw[len(codecs.BOM_UTF8):]
            if body.startswith(codecs.BOM_UTF8):
                localization_header_errors.append(f'{path.relative_to(ROOT)}: duplicate UTF-8 BOM')
                continue
            try:
                first_line = body.decode('utf-8').splitlines()[0]
            except (UnicodeDecodeError, IndexError):
                localization_header_errors.append(f'{path.relative_to(ROOT)}: invalid or empty UTF-8 localization')
                continue
            if first_line != expected_header:
                localization_header_errors.append(
                    f'{path.relative_to(ROOT)}: expected header {expected_header!r}, got {first_line!r}'
                )
    if localization_header_errors:
        errors.append(f'localization encoding/header failures: {len(localization_header_errors)}')
    for stem in CUSTOM_STEMS:
        en_path = LOC / 'english' / f'{stem}_l_english.yml'
        ru_path = LOC / 'russian' / f'{stem}_l_russian.yml'
        if not en_path.exists() or not ru_path.exists():
            errors.append(f'localization file missing for {stem}')
            continue
        en, ru = parse_loc(en_path), parse_loc(ru_path)
        missing_ru = sorted(set(en) - set(ru))
        missing_en = sorted(set(ru) - set(en))
        same_englishish = []
        for k, val in en.items():
            if k in ru and ru[k] == val and re.search(r'[A-Za-z]{4}', val) and k not in ALLOW_EQUAL_LATIN_VALUES:
                same_englishish.append(k)
        for k, val in ru.items():
            for pat in FORBIDDEN_RU:
                if re.search(pat, val, flags=re.I):
                    forbidden_hits.append({'file': stem, 'key': k, 'pattern': pat, 'value': val})
        loc_report[stem] = {
            'english_keys': len(en), 'russian_keys': len(ru),
            'missing_ru': missing_ru, 'missing_en': missing_en,
            'same_englishish': same_englishish,
        }
        if missing_ru or missing_en:
            errors.append(f'{stem}: localization key parity failure')
        if same_englishish:
            untranslated.extend((stem, k) for k in same_englishish)
    if untranslated:
        errors.append(f'visible localization appears untranslated: {untranslated}')
    if forbidden_hits:
        errors.append(f'forbidden English implementation jargon in RU visible strings: {len(forbidden_hits)} hits')

    workspace_gui_keys = sorted(set(re.findall(r'(?:text|tooltip)\s*=\s*"(CMP_WS_[A-Z0-9_]+)"', gui)))
    workspace_loc_missing = []
    for language in ['english', 'russian']:
        all_keys = set()
        for path in (LOC / language).glob('*.yml'):
            all_keys.update(parse_loc(path))
        for key in workspace_gui_keys:
            if key not in all_keys:
                workspace_loc_missing.append(f'{language}:{key}')
    if workspace_loc_missing:
        errors.append(f'workspace: {len(workspace_loc_missing)} visible localization keys missing')

    for language in ['english', 'russian']:
        loc = parse_loc(LOC / language / f'cmp_workspace_l_{language}.yml')
        nested_contract = {
            'CMP_WS_ECO_HELP_OVERVIEW_TT': '$CMP_ECO2_DESC$',
            'CMP_WS_ECO_HELP_MONEY_TT': '$CMP_ECO2_DIRECT_DESC$',
            'CMP_WS_ECO_HELP_MODIFIERS_TT': '$CMP_ECO2_MOD_DESC$',
            'CMP_WS_ECO_HELP_POLICIES_TT': '$CMP_ECO2_POLICY_DESC$',
            'CMP_WS_INTERFACE_HELP_TT': '$CMP_WS_INTERFACE_DESC$',
            'CMP_WS_INTERFACE_HELP': '$CMP_WS_PROFILE_IMPL_NOTE$',
            'CMP_WS_RB_HELP_BUILDINGS': '$CMP_RB2_HINT$',
            'CMP_WS_RB_HELP_STAFFING': '$CMP_STAFF_HINT$',
            'CMP_WS_POP_HELP_OVERVIEW': '$CMP_POP2_DESC$',
            'CMP_WS_POP_HELP_POPULATION': '$CMP_POP2_POP_DESC$',
            'CMP_WS_POP_HELP_PROFESSIONS': '$CMP_POP2_PROF_DESC$',
            'CMP_WS_POP_HELP_WELFARE': '$CMP_POP2_WELFARE_DESC$',
            'CMP_WS_POP_HELP_SOCIETY': '$CMP_POP2_SOCIETY_DESC$',
            'CMP_WS_POL_HELP_OVERVIEW': '$CMP_POL2_DESC$',
            'CMP_WS_POL_HELP_GOVERNMENT': '$CMP_POL2_GOV_DESC$',
            'CMP_WS_POL_HELP_CHARACTERS': '$CMP_POL2_CHAR_DESC$',
            'CMP_WS_POL_HELP_IG': '$CMP_POL2_IG_DESC$',
            'CMP_WS_POL_HELP_LAWS': '$CMP_POL2_LAW_DESC$',
            'CMP_WS_POL_HELP_BLOC': '$CMP_POL2_BLOC_DESC$',
            'CMP_WS_MIL_HELP_ARMY': '$CMP_ARMY_BUILDER_DESC$',
            'CMP_WS_MIL_HELP_TEMPLATES': '$CMP_ARMY_DESIGNER_DESC$',
            'CMP_WS_MIL_HELP_CONTROLS': '$CMP_ARMY_CONTROL_DESC$',
            'CMP_WS_MIL_HELP_FLEET': '$CMP_MIL_TARGET_FLEET_SELECT_TT$',
            'CMP_WS_MIL_HELP_FLEET_TEMPLATES': '$CMP_FD_DESC$',
            'CMP_WS_MIL_HELP_MARINES': '$CMP_ARMY_AMPH_DESC$',
            'CMP_WS_MIL_HELP_TASKFORCE': '$CMP_TASKFORCE_DESC$',
        }
        for key, nested in nested_contract.items():
            if nested not in loc.get(key, ''):
                errors.append(f'workspace help: {language}:{key} missing nested localization {nested}')
        if '$CMP_STAFF_ADAPTIVE_HINT$' not in loc.get('CMP_WS_RB_HELP_STAFFING', ''):
            errors.append(f'workspace help: {language}:CMP_WS_RB_HELP_STAFFING missing nested adaptive-staffing help')

    report = {
        'status': 'PASS' if not errors else 'FAIL',
        'profiles': PROFILES,
        'note': 'Static layout/readability gate only; real rendered QA still requires Victoria 3 at the listed resolutions/UI scales.',
        'font_stats': font_stats,
        'fleet_ship_selector': {'large_button_states_268x48': big_ship_buttons, 'ship_keys': ship_keys},
        'population_large_controls_detected': pop_large_controls,
        'workspace_visible_localization_keys': len(workspace_gui_keys),
        'workspace_localization_missing': workspace_loc_missing,
        'workspace_economy_scrolls': economy_scrolls,
        'workspace_economy_endpoints': len(economy_endpoint_counts),
        'workspace_economy_endpoint_parity_failures': bad_economy_endpoints,
        'workspace_regions_building_endpoints': len(building_endpoint_counts),
        'workspace_regions_selector_endpoint_parity_failures': bad_regions_actions,
        'workspace_regions_target_endpoint_parity_failures': bad_regions_targets,
        'workspace_picker_elisions_with_full_name_tooltips': {
            'total': picker_elisions,
            'buildings': picker_name_tooltips,
            'military_units': military_unit_tooltips,
            'navy_hulls': navy_hull_tooltips,
        },
        'workspace_building_operation_category_counts': operation_category_counts,
        'workspace_staffing_category_counts': staffing_category_counts,
        'workspace_staffing_supported_buildings': len(staffing_supported),
        'workspace_building_category_menus': category_menu_count,
        'workspace_building_category_filtered_scrolls': category_filtered_scroll_count,
        'workspace_building_category_layout_failures': category_scroll_failures,
        'workspace_building_category_selector_failures': category_selector_failures,
        'workspace_population_scrolls': population_scrolls,
        'workspace_population_endpoints': len(population_endpoint_counts),
        'workspace_population_endpoint_parity_failures': bad_population_endpoints,
        'workspace_politics_scrolls': politics_scrolls,
        'workspace_politics_endpoints': len(politics_endpoint_counts),
        'workspace_politics_endpoint_parity_failures': bad_politics_endpoints,
        'workspace_politics_target_parity_failures': bad_politics_targets,
        'workspace_diplomacy_scrolls': diplomacy_scrolls,
        'workspace_diplomacy_endpoints': len(diplomacy_endpoint_counts),
        'workspace_diplomacy_endpoint_parity_failures': bad_diplomacy_endpoints,
        'workspace_diplomacy_deferred_endpoint_leaks': leaked_diplomacy_endpoints,
        'workspace_military_scrolls': military_scrolls,
        'workspace_military_endpoints_checked': len(military_expected_endpoints),
        'workspace_military_endpoint_parity_failures': military_bad_endpoints,
        'workspace_convergence': {
            'single_launcher': launcher_count,
            'home_controls': len(home_lines),
            'global_help_buttons': len(global_help_buttons),
            'global_help_cards': len(global_help_cards),
            'global_help_routes': len(global_help_routes),
            'shortcuts': workspace_shortcuts,
            'home_preserves_profile_and_gameplay_state': ('cmp_ui_scale_profile' not in home_contract and 'GetScriptedGui' not in home_contract),
        },
        'localization': loc_report,
        'localization_files_checked': localization_files_checked,
        'localization_header_errors': localization_header_errors,
        'forbidden_ru_hits': forbidden_hits,
        'errors': errors,
        'warnings': warnings,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

if __name__ == '__main__':
    raise SystemExit(main())
