#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry/ui_shell.json"
ECONOMY_REGISTRY = ROOT / "registry/economy2.json"
BUILDINGS_REGISTRY = ROOT / "registry/buildings.json"
STAFFING_REGISTRY = ROOT / "registry/staffing.json"
REGIONS_REGISTRY = ROOT / "registry/regions_buildings.json"
POPULATION_REGISTRY = ROOT / "registry/population2.json"
POLITICS_REGISTRY = ROOT / "registry/politics2.json"
DIPLOMACY_REGISTRY = ROOT / "registry/diplomacy2.json"
LAND_UNITS_REGISTRY = ROOT / "registry/land_units.json"
SHIPS_REGISTRY = ROOT / "registry/ships.json"
FLEET_REGISTRY = ROOT / "registry/fleet_builder.json"
NAVY18_REGISTRY = ROOT / "registry/navy18.json"
NAVAL_CATALOG_REGISTRY = ROOT / "registry/naval_catalog.json"
OUTPUT = ROOT / "generated/workspace_shell.gui.txt"
GUI = ROOT / "gui/main/sakuya_main.gui"
START = "# CMP_WORKSPACE_SHELL_BEGIN"
END = "# CMP_WORKSPACE_SHELL_END"
INSERT_BEFORE = "    # CMP v0.3 beta10 - Unified Target Controller popup"
LAUNCHER_START = "# CMP_WORKSPACE_LAUNCHER_BEGIN"
LAUNCHER_END = "# CMP_WORKSPACE_LAUNCHER_END"
LEGACY_TRAY_START = "    # CMP v0.3 beta1: explicit global target status bar"
LEGACY_TRAY_END = "    widget = {\n        name = sakuya_main_begining"

DOMAIN_HELP_VARIABLES = [
    "cmp_workspace_economy_help",
    "cmp_workspace_interface_help",
    "cmp_workspace_regions_help",
    "cmp_workspace_population_help",
    "cmp_workspace_politics_help",
    "cmp_workspace_diplomacy_help",
    "cmp_workspace_military_help",
]

NAVIGATION_STATE_VARIABLES = [
    "cmp_economy2_tab",
    "cmp_workspace_regions_tab",
    "cmp_workspace_regions_mode",
    "cmp_population2_tab",
    "cmp_workspace_politics_tab",
    "cmp_workspace_diplomacy_tab",
    "cmp_workspace_diplomacy_confirm",
    "cmp_workspace_military_tab",
    "cmp_workspace_army_category",
    "cmp_workspace_fleet_builder_mode",
    "cmp_workspace_army_template_tab",
    "cmp_workspace_fleet_template_tab",
    "cmp_workspace_fleet_picker",
    "cmp_workspace_navy_catalog_category",
    "cmp_workspace_navy_show_obsolete",
    "cmp_workspace_navy_ship_page",
    "cmp_workspace_building_category",
    "cmp_workspace_staffing_category",
    "cmp_workspace_building_category_menu_operations",
    "cmp_workspace_building_category_menu_staffing",
]


def line(lines: list[str], indent: int, text: str = "") -> None:
    lines.append("    " * indent + text)


def button(lines: list[str], indent: int, *, x: int, y: int, width: int, height: int,
           label: str, font: int, action: str | None = None, enabled: bool = True,
           color: str = "0.42 0.50 0.62 0.98", tooltip: str | None = None,
           enabled_when: str | None = None, actions: list[str] | None = None,
           elide: bool = False, name: str | None = None, label_transparent: bool = False) -> None:
    state = f' enabled = "{enabled_when}"' if enabled_when else (" enabled = no" if not enabled else "")
    click_actions = ([action] if action else []) + (actions or [])
    action_text = "".join(f' onclick = "[{item}]"' for item in click_actions)
    tooltip_text = f' tooltip = "{tooltip}"' if tooltip else ""
    name_text = f' name = "{name}"' if name else ""
    line(lines, indent, f'button_standard = {{{name_text} position = {{ {x} {y} }} size = {{ {width} {height} }}{state}{action_text}{tooltip_text}')
    line(lines, indent + 1, 'blockoverride "primary_visible" {}')
    line(lines, indent + 1, f'blockoverride "primary_texture" {{ texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = {{ {color} }} }}')
    elide_text = " elide = right" if elide else ""
    transparent_text = ' alwaystransparent = yes' if label_transparent else ''
    line(lines, indent + 1, f'textbox = {{ size = {{ {width - 12} {height - 8} }} parentanchor = center maximumsize = {{ {width - 12} {height - 8} }} fontsize = {font} fontsize_min = 12 align = center|nobaseline{elide_text}{transparent_text} text = "{label}" }}')
    line(lines, indent, "}")


def selected_line(lines: list[str], indent: int, *, x: int, y: int, width: int, effect: str) -> None:
    line(lines, indent, f'icon = {{ visible = "[GetScriptedGui(\'{effect}\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" position = {{ {x + 3} {y} }} size = {{ {width - 6} 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')


def variable_selected_line(lines: list[str], indent: int, *, x: int, y: int, width: int,
                           variable: str, value: str, default: bool = False) -> None:
    if default:
        visible = (f"[Or(Not(GetVariableSystem.Exists('{variable}')), "
                   f"GetVariableSystem.HasValue('{variable}', '{value}'))]")
    else:
        visible = f"[GetVariableSystem.HasValue('{variable}', '{value}')]"
    line(lines, indent, f'icon = {{ visible = "{visible}" position = {{ {x + 3} {y} }} size = {{ {width - 6} 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')


def economy_action_button(lines: list[str], indent: int, *, x: int, y: int, width: int,
                          height: int, label: str, font: int, effect: str,
                          tooltip: str = "CMP_ECO2_TT_GENERIC",
                          color: str = "0.42 0.50 0.62 0.98",
                          selected: str | None = None) -> None:
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    button(lines, indent, x=x, y=y, width=width, height=height, label=label, font=font,
           action=f"GetScriptedGui('{effect}').Execute({scope})",
           enabled_when=f"[GetScriptedGui('{effect}').IsValid({scope})]",
           tooltip=tooltip, color=color)
    if selected:
        selected_line(lines, indent, x=x, y=y + height - 4, width=width, effect=selected)


def page_visible(page: str) -> str:
    if page == "target":
        return "[Or(Not(GetVariableSystem.Exists('cmp_workspace_page')), GetVariableSystem.HasValue('cmp_workspace_page', 'target'))]"
    return f"[GetVariableSystem.HasValue('cmp_workspace_page', '{page}')]"


def clear_variable_actions(variables: list[str]) -> list[str]:
    return [f"GetVariableSystem.Clear('{variable}')" for variable in variables]


def close_help_actions() -> list[str]:
    return clear_variable_actions(DOMAIN_HELP_VARIABLES + ["cmp_workspace_global_help"])


def navigation_actions(page: str) -> list[str]:
    return [f"GetVariableSystem.Set('cmp_workspace_page', '{page}')"] + close_help_actions()


def reset_view_actions() -> list[str]:
    # The view reset is intentionally UI-only: it does not touch the selected
    # interface profile, Target Core state, ScriptedGui selections or results.
    return (["GetVariableSystem.Set('cmp_workspace_page', 'target')"] +
            close_help_actions() + clear_variable_actions(NAVIGATION_STATE_VARIABLES))


def render_navigation(lines: list[str], profile: dict) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    y = 82
    entries = [
        ("CMP_WS_NAV_TARGET", "target", True),
        ("CMP_WS_NAV_ECONOMY", "economy", True),
        ("CMP_WS_NAV_REGIONS", "regions", True),
        ("CMP_WS_NAV_POPULATION", "population", True),
        ("CMP_WS_NAV_POLITICS", "politics", True),
        ("CMP_WS_NAV_DIPLOMACY", "diplomacy", True),
        ("CMP_WS_NAV_MILITARY", "military", True),
        ("CMP_WS_NAV_INTERFACE", "interface", True),
    ]
    for label, page, enabled in entries:
        actions = navigation_actions(page) if enabled else None
        color = "0.45 0.62 0.82 0.98" if enabled else "0.27 0.29 0.34 0.90"
        button(lines, 2, x=14, y=y, width=194, height=height, label=label, font=font,
               actions=actions, enabled=enabled, color=color,
               tooltip=None if enabled else "CMP_WS_NAV_PENDING_TT")
        if enabled:
            line(lines, 2, f'icon = {{ visible = "{page_visible(page)}" position = {{ 17 {y + height - 4} }} size = {{ 188 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')
        y += height + 8


def render_launcher() -> str:
    return "\n".join([
        f"    {LAUNCHER_START}",
        '    # beta16-pre2: accepted legacy launchers converge on this single stable entry point.',
        '    button_standard = {',
        '        name = "cmp_workspace_launcher"',
        '        position = { 828 126 }',
        '        size = { 258 28 }',
        '        onclick = "[GetVariableSystem.Set(\'cmp_workspace_shell\', \'open\')]"',
        '        tooltip = "CMP_WS_OPEN_TT"',
        '        blockoverride "primary_visible" {}',
        '        blockoverride "primary_texture" { texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.45 0.62 0.82 0.98 } }',
        '        textbox = { size = { 246 24 } parentanchor = center maximumsize = { 246 24 } font = "OpenSans" fontsize = 12 fontsize_min = 10 align = center|nobaseline text = "CMP_WS_OPEN" }',
        '    }',
        f"    {LAUNCHER_END}",
    ])


def render_target_page(lines: list[str], registry: dict, profile: dict) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    columns = profile["target_columns"]
    gap = 8
    content_w = 838
    button_w = (content_w - gap * (columns - 1)) // columns

    line(lines, 2, f'widget = {{ visible = "{page_visible("target")}" position = {{ 238 76 }} size = {{ 864 514 }}')
    line(lines, 3, 'scrollarea = { name = "cmp_workspace_target_scroll" size = { 864 514 } scrollbarpolicy_horizontal = always_off scrollbar_vertical = { using = vertical_scrollbar }')
    line(lines, 4, 'scrollwidget = {')
    line(lines, 5, 'widget = { size = { 844 980 }')
    line(lines, 6, f'textbox = {{ position = {{ 4 0 }} size = {{ 820 36 }} maximumsize = {{ 820 36 }} fontsize = {font + 6} fontsize_min = 14 align = left text = "CMP_WS_TARGET_TITLE" }}')
    line(lines, 6, f'textbox = {{ position = {{ 4 38 }} size = {{ 820 54 }} maximumsize = {{ 820 54 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_TARGET_DESC" }}')
    line(lines, 6, f'textbox = {{ position = {{ 4 98 }} size = {{ 820 28 }} maximumsize = {{ 820 28 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_TARGET_SCOPE" }}')

    start_y = 132
    for index, target in enumerate(registry["target_modes"]):
        row, col = divmod(index, columns)
        x = 4 + col * (button_w + gap)
        y = start_y + row * (height + gap)
        button(lines, 6, x=x, y=y, width=button_w, height=height, label=target["label"], font=font,
               action=f"GetScriptedGui('{target['effect']}').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)",
               color="0.42 0.50 0.62 0.98", tooltip="CMP_WS_TARGET_MODE_TT")
        selected_line(lines, 6, x=x, y=y + height - 4, width=button_w, effect=target["selected"])

    target_rows = (len(registry["target_modes"]) + columns - 1) // columns
    status_y = start_y + target_rows * (height + gap) + 4
    line(lines, 6, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_target_core_active_valid\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" position = {{ 4 {status_y} }} size = {{ 820 32 }} maximumsize = {{ 820 32 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_ACTIVE_VALID" }}')
    line(lines, 6, f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_target_core_active_valid\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End))]" position = {{ 4 {status_y} }} size = {{ 820 32 }} maximumsize = {{ 820 32 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_ACTIVE_INVALID" }}')
    groups_title_y = status_y + 42
    line(lines, 6, f'textbox = {{ position = {{ 4 {groups_title_y} }} size = {{ 820 30 }} maximumsize = {{ 820 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_GROUPS_TITLE" }}')
    line(lines, 6, f'textbox = {{ position = {{ 4 {groups_title_y + 32} }} size = {{ 820 48 }} maximumsize = {{ 820 48 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_GROUPS_DESC" }}')

    group_columns = profile["group_columns"]
    group_w = (content_w - gap * (group_columns - 1)) // group_columns
    group_y = groups_title_y + 88
    clear_w = max(72, int(group_w * 0.30))
    toggle_w = group_w - clear_w - 6
    for index, group in enumerate(registry["groups"]):
        row, col = divmod(index, group_columns)
        x = 4 + col * (group_w + gap)
        y = group_y + row * (height + gap)
        button(lines, 6, x=x, y=y, width=toggle_w, height=height, label=group["label"], font=font,
               action=f"GetScriptedGui('{group['toggle']}').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)",
               color="0.50 0.62 0.78 1", tooltip="CMP_WS_GROUP_TOGGLE_TT")
        selected_line(lines, 6, x=x, y=y + height - 4, width=toggle_w, effect=group["selected"])
        button(lines, 6, x=x + toggle_w + 6, y=y, width=clear_w, height=height, label="CMP_WS_CLEAR", font=font,
               action=f"GetScriptedGui('{group['clear']}').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)",
               color="0.72 0.42 0.46 1", tooltip="CMP_WS_GROUP_CLEAR_TT")

    group_rows = (len(registry["groups"]) + group_columns - 1) // group_columns
    note_y = group_y + group_rows * (height + gap) + 14
    line(lines, 6, f'textbox = {{ position = {{ 4 {note_y} }} size = {{ 820 64 }} maximumsize = {{ 820 64 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_TARGET_NOTE" }}')
    line(lines, 5, "}")
    line(lines, 4, "}")
    line(lines, 3, "}")
    line(lines, 2, "}")


def render_interface_page(lines: list[str], registry: dict, profile: dict) -> None:
    font = profile["font_size"]
    height = max(48, profile["button_height"])
    line(lines, 2, f'widget = {{ visible = "{page_visible("interface")}" position = {{ 238 76 }} size = {{ 864 514 }}')
    line(lines, 3, f'textbox = {{ position = {{ 4 0 }} size = {{ 700 36 }} maximumsize = {{ 700 36 }} fontsize = {font + 6} fontsize_min = 14 align = left text = "CMP_WS_INTERFACE_TITLE" }}')
    button(lines, 3, x=768, y=0, width=56, height=height, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_interface_help', 'open')",
           tooltip="CMP_WS_INTERFACE_HELP_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 3, f'textbox = {{ position = {{ 4 {height + 2} }} size = {{ 720 44 }} maximumsize = {{ 720 44 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_INTERFACE_SUMMARY" }}')
    y = height + 62
    for candidate in registry["profiles"]:
        active = candidate["id"] == profile["id"]
        color = "0.38 0.72 0.45 0.98" if active else "0.42 0.50 0.62 0.98"
        button(lines, 3, x=4, y=y, width=214, height=height, label=candidate["label"], font=font,
               action=f"GetVariableSystem.Set('cmp_ui_scale_profile', '{candidate['id']}')", color=color,
               tooltip="CMP_WS_PROFILE_TT")
        line(lines, 3, f'textbox = {{ position = {{ 234 {y} }} size = {{ 590 {height} }} maximumsize = {{ 590 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{candidate["description"]}" }}')
        y += height + 16
    render_interface_help(lines, profile)
    line(lines, 2, "}")


def render_interface_help(lines: list[str], profile: dict) -> None:
    font = profile["font_size"]
    profile_id = profile["id"]
    line(lines, 3, 'widget = { name = "cmp_workspace_interface_help_card" visible = "[GetVariableSystem.Exists(\'cmp_workspace_interface_help\')]" position = { 32 72 } size = { 792 420 }')
    line(lines, 4, 'icon = { size = { 792 420 } texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = { 0.045 0.055 0.075 0.998 } }')
    line(lines, 4, 'icon = { position = { 2 2 } size = { 788 416 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.98 } alwaystransparent = yes }')
    line(lines, 4, f'textbox = {{ position = {{ 20 14 }} size = {{ 680 36 }} maximumsize = {{ 680 36 }} fontsize = {font + 4} fontsize_min = 14 align = left text = "CMP_WS_INTERFACE_HELP_TITLE" }}')
    line(lines, 4, 'close_button = { position = { 736 10 } size = { 42 42 } onclick = "[GetVariableSystem.Clear(\'cmp_workspace_interface_help\')]" }')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_interface_help_{profile_id}" position = {{ 20 60 }} size = {{ 752 338 }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, f'textbox = {{ size = {{ 720 26 }} maximumsize = {{ 720 26 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_DIAGNOSTICS_TITLE" }}')
    line(lines, 6, f'textbox = {{ position = {{ 0 30 }} size = {{ 720 24 }} maximumsize = {{ 720 24 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_BUILD_ID" }}')
    line(lines, 6, f'textbox = {{ position = {{ 0 54 }} size = {{ 720 24 }} maximumsize = {{ 720 24 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_BUILD_BASELINE" }}')
    line(lines, 6, f'textbox = {{ position = {{ 0 78 }} size = {{ 720 24 }} maximumsize = {{ 720 24 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_BUILD_RUNTIME_STATUS" }}')
    line(lines, 6, f'textbox = {{ position = {{ 0 102 }} size = {{ 720 24 }} maximumsize = {{ 720 24 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_BUILD_NAVY_RC_STATUS" }}')
    line(lines, 6, f'textbox = {{ position = {{ 0 142 }} size = {{ 720 620 }} maximumsize = {{ 720 620 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_INTERFACE_HELP" }}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_global_help(lines: list[str], profile: dict) -> None:
    font = profile["font_size"]
    height = min(52, profile["button_height"])
    profile_id = profile["id"]
    routes = [
        ("CMP_WS_NAV_TARGET", "target", None, None),
        ("CMP_WS_NAV_ECONOMY", "economy", "cmp_workspace_economy_help", "overview"),
        ("CMP_WS_NAV_REGIONS", "regions", "cmp_workspace_regions_help", "overview"),
        ("CMP_WS_NAV_POPULATION", "population", "cmp_workspace_population_help", "overview"),
        ("CMP_WS_NAV_POLITICS", "politics", "cmp_workspace_politics_help", "overview"),
        ("CMP_WS_NAV_DIPLOMACY", "diplomacy", "cmp_workspace_diplomacy_help", "overview"),
        ("CMP_WS_NAV_MILITARY", "military", "cmp_workspace_military_help", "overview"),
        ("CMP_WS_NAV_INTERFACE", "interface", "cmp_workspace_interface_help", "open"),
    ]
    line(lines, 2, f'widget = {{ name = "cmp_workspace_global_help_card_{profile_id}" visible = "[GetVariableSystem.Exists(\'cmp_workspace_global_help\')]" position = {{ 238 76 }} size = {{ 864 514 }}')
    line(lines, 3, 'icon = { size = { 864 514 } texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = { 0.045 0.055 0.075 0.998 } }')
    line(lines, 3, 'icon = { position = { 2 2 } size = { 860 510 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.98 } alwaystransparent = yes }')
    line(lines, 3, f'textbox = {{ position = {{ 20 14 }} size = {{ 730 36 }} maximumsize = {{ 730 36 }} fontsize = {font + 4} fontsize_min = 14 align = left text = "CMP_WS_GLOBAL_HELP_TITLE" }}')
    line(lines, 3, 'close_button = { position = { 808 10 } size = { 42 42 } onclick = "[GetVariableSystem.Clear(\'cmp_workspace_global_help\')]" }')
    line(lines, 3, f'textbox = {{ position = {{ 20 58 }} size = {{ 814 54 }} maximumsize = {{ 814 54 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_GLOBAL_HELP_SUMMARY" }}')
    for index, (label, page, help_variable, help_value) in enumerate(routes):
        row, col = divmod(index, 2)
        x = 20 + col * 407
        y = 122 + row * (height + 8)
        actions = navigation_actions(page)
        if help_variable and help_value:
            actions.append(f"GetVariableSystem.Set('{help_variable}', '{help_value}')")
        button(lines, 3, x=x, y=y, width=395, height=height, label=label, font=font,
               actions=actions, tooltip="CMP_WS_GLOBAL_HELP_ROUTE_TT",
               color="0.45 0.62 0.82 0.98",
               name=f"cmp_workspace_global_help_route_{page}_{profile_id}")
    footer_y = 122 + 4 * (height + 8) + 6
    line(lines, 3, f'textbox = {{ position = {{ 20 {footer_y} }} size = {{ 814 72 }} maximumsize = {{ 814 72 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_GLOBAL_HELP_FOOTER" }}')
    line(lines, 2, '}')


def render_economy_tabs(lines: list[str], profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    tabs = [
        ("CMP_WS_ECO_TAB_MONEY", "direct", "CMP_WS_ECO_HELP_MONEY_TT"),
        ("CMP_WS_ECO_TAB_MODIFIERS", "modifiers", "CMP_WS_ECO_HELP_MODIFIERS_TT"),
        ("CMP_WS_ECO_TAB_POLICIES", "policies", "CMP_WS_ECO_HELP_POLICIES_TT"),
    ]
    gap = 8
    width = (820 - gap * 2) // 3
    for index, (label, tab, tooltip) in enumerate(tabs):
        x = 4 + index * (width + gap)
        button(lines, 3, x=x, y=y, width=width, height=height, label=label, font=font,
               action=f"GetVariableSystem.Set('cmp_economy2_tab', '{tab}')",
               tooltip=tooltip, color="0.40 0.53 0.68 0.97")
        visible = (f"[Or(Not(GetVariableSystem.Exists('cmp_economy2_tab')), "
                   f"GetVariableSystem.HasValue('cmp_economy2_tab', 'direct'))]" if tab == "direct"
                   else f"[GetVariableSystem.HasValue('cmp_economy2_tab', '{tab}')]")
        line(lines, 3, f'icon = {{ visible = "{visible}" position = {{ {x + 4} {y + height - 4} }} size = {{ {width - 8} 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')


def render_economy_direct(lines: list[str], economy: dict, profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    visible = "[Or(Not(GetVariableSystem.Exists('cmp_economy2_tab')), GetVariableSystem.HasValue('cmp_economy2_tab', 'direct'))]"
    line(lines, 3, f'widget = {{ visible = "{visible}" position = {{ 4 {y} }} size = {{ 840 {514 - y} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_economy_direct_{profile["id"]}" size = {{ 840 {514 - y} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, "scrollwidget = {")
    line(lines, 6, 'widget = { size = { 820 526 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_WS_ECO_MONEY_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_economy_help', 'money')",
           tooltip="CMP_WS_ECO_HELP_MONEY_TT", color="0.48 0.58 0.72 0.98")
    money_width = (800 - 8 * 3) // 4
    cursor_y = 52
    for section, effect_prefix, tooltip in [
        ("CMP_ECO2_TREASURY", "cmp_economy2_treasury_add", "CMP_ECO2_TT_TREASURY"),
        ("CMP_ECO2_INVESTMENT", "cmp_economy2_investment_add", "CMP_ECO2_TT_INVESTMENT"),
    ]:
        line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "{section}" }}')
        cursor_y += 34
        for index, step in enumerate(economy["money_steps_percent_of_reserve_cap"]):
            x = index * (money_width + 8)
            economy_action_button(lines, 7, x=x, y=cursor_y, width=money_width, height=height,
                                  label=f"CMP_ECO2_CAP_{step}", font=font,
                                  effect=f"{effect_prefix}_{step}", tooltip=tooltip)
        cursor_y += height + 18
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_ECO2_DEBT_SECTION" }}')
    cursor_y += 38
    debt = [
        ("CMP_ECO2_CLEAR_DEBT", "cmp_economy2_clear_debt", "CMP_ECO2_TT_CLEAR_DEBT", "0.42 0.62 0.48 0.96"),
        ("CMP_ECO2_BANKRUPTCY", "cmp_economy2_declare_bankruptcy", "CMP_ECO2_TT_BANKRUPTCY", "0.72 0.38 0.42 0.96"),
        ("CMP_ECO2_RESCUE", "cmp_economy2_rescue_bankruptcy", "CMP_ECO2_TT_RESCUE", "0.46 0.64 0.50 0.96"),
    ]
    debt_width = (800 - 16) // 3
    for index, (label, effect, tooltip, color) in enumerate(debt):
        economy_action_button(lines, 7, x=index * (debt_width + 8), y=cursor_y,
                              width=debt_width, height=height, label=label, font=font,
                              effect=effect, tooltip=tooltip, color=color)
    line(lines, 6, "}")
    line(lines, 5, "}")
    line(lines, 4, "}")
    line(lines, 3, "}")


def render_economy_modifiers(lines: list[str], economy: dict, profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    visible = "[GetVariableSystem.HasValue('cmp_economy2_tab', 'modifiers')]"
    param_columns = 3 if profile["density_percent"] <= 100 else 2
    gap = 8
    content_width = 800
    param_width = (content_width - gap * (param_columns - 1)) // param_columns
    param_rows = (len(economy["parameters"]) + param_columns - 1) // param_columns
    value_columns = profile["target_columns"]
    value_width = (content_width - gap * (value_columns - 1)) // value_columns
    value_rows = (len(economy["values"]) + value_columns - 1) // value_columns
    content_height = 64 + param_rows * (height + gap) + 42 + value_rows * (height + gap) + height + 70
    line(lines, 3, f'widget = {{ visible = "{visible}" position = {{ 4 {y} }} size = {{ 840 {514 - y} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_economy_modifiers_{profile["id"]}" size = {{ 840 {514 - y} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, "scrollwidget = {")
    line(lines, 6, f'widget = {{ size = {{ 820 {content_height} }}')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_WS_ECO_MODIFIERS_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_economy_help', 'modifiers')",
           tooltip="CMP_WS_ECO_HELP_MODIFIERS_TT", color="0.48 0.58 0.72 0.98")
    cursor_y = 52
    for index, parameter in enumerate(economy["parameters"]):
        row, col = divmod(index, param_columns)
        x = col * (param_width + gap)
        py = cursor_y + row * (height + gap)
        economy_action_button(lines, 7, x=x, y=py, width=param_width, height=height,
                              label=parameter["loc_key"], font=font,
                              effect=f"cmp_economy2_select_parameter_{parameter['id']}",
                              tooltip="CMP_ECO2_TT_PARAM", color="0.42 0.55 0.72 0.96",
                              selected=f"cmp_economy2_parameter_{parameter['id']}_selected")
    cursor_y += param_rows * (height + gap) + 8
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_ECO2_VALUE_TITLE" }}')
    cursor_y += 36
    for index, value in enumerate(economy["values"]):
        row, col = divmod(index, value_columns)
        x = col * (value_width + gap)
        vy = cursor_y + row * (height + gap)
        economy_action_button(lines, 7, x=x, y=vy, width=value_width, height=height,
                              label=f"CMP_ECO2_VALUE_{value['id'].upper()}", font=font,
                              effect=f"cmp_economy2_select_value_{value['id']}",
                              tooltip="CMP_ECO2_TT_VALUE",
                              selected=f"cmp_economy2_value_{value['id']}_selected")
    cursor_y += value_rows * (height + gap) + 12
    actions = [
        ("CMP_ECO2_APPLY", "cmp_economy2_apply_selected", "CMP_ECO2_TT_APPLY", "0.38 0.68 0.44 0.96"),
        ("CMP_ECO2_RESET_SELECTED", "cmp_economy2_reset_selected", "CMP_ECO2_TT_RESET_SELECTED", "0.64 0.52 0.32 0.96"),
        ("CMP_ECO2_RESET_ALL", "cmp_economy2_reset_all", "CMP_ECO2_TT_RESET_ALL", "0.72 0.38 0.42 0.96"),
    ]
    action_width = (content_width - gap * 2) // 3
    for index, (label, effect, tooltip, color) in enumerate(actions):
        economy_action_button(lines, 7, x=index * (action_width + gap), y=cursor_y,
                              width=action_width, height=height, label=label, font=font,
                              effect=effect, tooltip=tooltip, color=color)
    line(lines, 6, "}")
    line(lines, 5, "}")
    line(lines, 4, "}")
    line(lines, 3, "}")


def render_economy_policies(lines: list[str], economy: dict, profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    visible = "[GetVariableSystem.HasValue('cmp_economy2_tab', 'policies')]"
    row_height = height + 10
    content_height = 64 + len(economy["policies"]) * row_height + 40
    line(lines, 3, f'widget = {{ visible = "{visible}" position = {{ 4 {y} }} size = {{ 840 {514 - y} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_economy_policies_{profile["id"]}" size = {{ 840 {514 - y} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, "scrollwidget = {")
    line(lines, 6, f'widget = {{ size = {{ 820 {content_height} }}')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_WS_ECO_POLICIES_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_economy_help', 'policies')",
           tooltip="CMP_WS_ECO_HELP_POLICIES_TT", color="0.48 0.58 0.72 0.98")
    for index, policy in enumerate(economy["policies"]):
        py = 52 + index * row_height
        line(lines, 7, f'textbox = {{ position = {{ 0 {py} }} size = {{ 520 {height} }} maximumsize = {{ 520 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{policy["loc_key"]}" }}')
        economy_action_button(lines, 7, x=536, y=py, width=124, height=height,
                              label="CMP_ECO2_ON", font=font,
                              effect=f"cmp_economy2_policy_{policy['id']}_enable",
                              tooltip="CMP_ECO2_TT_POLICY_ON", color="0.38 0.68 0.44 0.96")
        economy_action_button(lines, 7, x=676, y=py, width=124, height=height,
                              label="CMP_ECO2_OFF", font=font,
                              effect=f"cmp_economy2_policy_{policy['id']}_disable",
                              tooltip="CMP_ECO2_TT_POLICY_OFF", color="0.68 0.42 0.44 0.96")
    line(lines, 6, "}")
    line(lines, 5, "}")
    line(lines, 4, "}")
    line(lines, 3, "}")


def render_economy_page(lines: list[str], economy: dict, profile: dict) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    line(lines, 2, f'widget = {{ visible = "{page_visible("economy")}" position = {{ 238 76 }} size = {{ 864 514 }}')
    line(lines, 3, f'textbox = {{ position = {{ 4 0 }} size = {{ 430 34 }} maximumsize = {{ 430 34 }} fontsize = {font + 6} fontsize_min = 14 align = left text = "CMP_ECO2_TITLE" }}')
    button(lines, 3, x=446, y=0, width=56, height=height, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_economy_help', 'overview')",
           tooltip="CMP_WS_ECO_HELP_OVERVIEW_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 3, f'textbox = {{ position = {{ 4 40 }} size = {{ 498 30 }} maximumsize = {{ 498 30 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_ECO_FLOW" }}')
    button(lines, 3, x=610, y=0, width=214, height=height, label="CMP_WS_ECO_TARGET", font=font,
           action="GetVariableSystem.Set('cmp_workspace_page', 'target')",
           tooltip="CMP_ECO2_TARGET_TT", color="0.45 0.62 0.82 0.97")
    line(lines, 3, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_economy2_target_valid\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" position = {{ 610 {height + 2} }} size = {{ 214 28 }} maximumsize = {{ 214 28 }} fontsize = {font} fontsize_min = 12 align = center text = "CMP_WS_ECO_TARGET_READY" }}')
    line(lines, 3, f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_economy2_target_valid\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End))]" position = {{ 610 {height + 2} }} size = {{ 214 28 }} maximumsize = {{ 214 28 }} fontsize = {font} fontsize_min = 12 align = center text = "CMP_WS_ECO_TARGET_REQUIRED" }}')
    tab_y = max(82, height + 34)
    render_economy_tabs(lines, profile, y=tab_y)
    content_y = tab_y + height + 10
    render_economy_direct(lines, economy, profile, y=content_y)
    render_economy_modifiers(lines, economy, profile, y=content_y)
    render_economy_policies(lines, economy, profile, y=content_y)
    render_economy_help(lines, profile)
    line(lines, 2, "}")


def render_economy_help(lines: list[str], profile: dict) -> None:
    font = profile["font_size"]
    profile_id = profile["id"]
    line(lines, 3, 'widget = { name = "cmp_workspace_economy_help_card" visible = "[GetVariableSystem.Exists(\'cmp_workspace_economy_help\')]" position = { 32 72 } size = { 792 420 }')
    line(lines, 4, 'icon = { size = { 792 420 } texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = { 0.045 0.055 0.075 0.998 } }')
    line(lines, 4, 'icon = { position = { 2 2 } size = { 788 416 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.98 } alwaystransparent = yes }')
    line(lines, 4, f'textbox = {{ position = {{ 20 14 }} size = {{ 680 36 }} maximumsize = {{ 680 36 }} fontsize = {font + 4} fontsize_min = 14 align = left text = "CMP_WS_HELP_TITLE" }}')
    line(lines, 4, 'close_button = { position = { 736 10 } size = { 42 42 } onclick = "[GetVariableSystem.Clear(\'cmp_workspace_economy_help\')]" }')
    topics = [
        ("overview", "CMP_WS_ECO_HELP_OVERVIEW"),
        ("money", "CMP_WS_ECO_HELP_MONEY"),
        ("modifiers", "CMP_WS_ECO_HELP_MODIFIERS"),
        ("policies", "CMP_WS_ECO_HELP_POLICIES"),
    ]
    for topic, key in topics:
        line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_economy_help_{topic}_{profile_id}" visible = "[GetVariableSystem.HasValue(\'cmp_workspace_economy_help\', \'{topic}\')]" position = {{ 20 60 }} size = {{ 752 338 }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
        line(lines, 5, 'scrollwidget = {')
        line(lines, 6, f'textbox = {{ size = {{ 720 760 }} maximumsize = {{ 720 760 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "{key}" }}')
        line(lines, 5, '}')
        line(lines, 4, '}')
    line(lines, 3, '}')


def render_population_tabs(lines: list[str], profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    tabs = [
        ("CMP_POP2_TAB_POP", "population", "CMP_WS_POP_HELP_POPULATION_TT"),
        ("CMP_POP2_TAB_PROF", "professions", "CMP_WS_POP_HELP_PROFESSIONS_TT"),
        ("CMP_POP2_TAB_WELFARE", "welfare", "CMP_WS_POP_HELP_WELFARE_TT"),
        ("CMP_POP2_TAB_SOCIETY", "society", "CMP_WS_POP_HELP_SOCIETY_TT"),
    ]
    gap = 8
    width = (820 - gap * 3) // 4
    for index, (label, tab, tooltip) in enumerate(tabs):
        x = 4 + index * (width + gap)
        button(lines, 3, x=x, y=y, width=width, height=height, label=label, font=font,
               action=f"GetVariableSystem.Set('cmp_population2_tab', '{tab}')",
               tooltip=tooltip, color="0.40 0.53 0.68 0.97")
        visible = (f"[Or(Not(GetVariableSystem.Exists('cmp_population2_tab')), "
                   f"GetVariableSystem.HasValue('cmp_population2_tab', 'population'))]" if tab == "population"
                   else f"[GetVariableSystem.HasValue('cmp_population2_tab', '{tab}')]")
        line(lines, 3, f'icon = {{ visible = "{visible}" position = {{ {x + 4} {y + height - 4} }} size = {{ {width - 8} 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')


def render_population_main(lines: list[str], population: dict, profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    visible = "[Or(Not(GetVariableSystem.Exists('cmp_population2_tab')), GetVariableSystem.HasValue('cmp_population2_tab', 'population'))]"
    line(lines, 3, f'widget = {{ visible = "{visible}" position = {{ 4 {y} }} size = {{ 840 {514 - y} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_population_population_{profile["id"]}" size = {{ 840 {514 - y} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 820 470 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_POP2_POP_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_population_help', 'population')",
           tooltip="CMP_WS_POP_HELP_POPULATION_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 52 }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_POP_AMOUNT_TITLE" }}')
    gap = 8
    amount_width = (800 - gap * 5) // 6
    for index, item in enumerate(population["amounts"]):
        x = index * (amount_width + gap)
        economy_action_button(lines, 7, x=x, y=84, width=amount_width, height=height,
                              label=item["loc"], font=font,
                              effect=f"cmp_pop2_select_amount_{item['id']}",
                              tooltip="CMP_POP2_TT_AMOUNT",
                              selected=f"cmp_pop2_amount_{item['id']}_selected")
    action_y = 84 + height + 10
    action_width = (800 - gap) // 2
    economy_action_button(lines, 7, x=0, y=action_y, width=action_width, height=height,
                          label="CMP_POP2_ADD", font=font, effect="cmp_pop2_add_population",
                          tooltip="CMP_POP2_TT_ADD", color="0.38 0.68 0.44 0.96")
    economy_action_button(lines, 7, x=action_width + gap, y=action_y, width=action_width, height=height,
                          label="CMP_POP2_REMOVE", font=font, effect="cmp_pop2_remove_population",
                          tooltip="CMP_POP2_TT_REMOVE", color="0.72 0.38 0.42 0.96")
    literacy_title_y = action_y + height + 22
    line(lines, 7, f'textbox = {{ position = {{ 0 {literacy_title_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_POP2_LITERACY_TITLE" }}')
    literacy_y = literacy_title_y + 36
    literacy_width = (800 - gap * 4) // 5
    for index, item in enumerate(population["literacy"]):
        x = index * (literacy_width + gap)
        economy_action_button(lines, 7, x=x, y=literacy_y, width=literacy_width, height=height,
                              label=item["loc"], font=font,
                              effect=f"cmp_pop2_select_literacy_{item['id']}",
                              tooltip="CMP_POP2_TT_LITERACY",
                              selected=f"cmp_pop2_literacy_{item['id']}_selected")
    economy_action_button(lines, 7, x=0, y=literacy_y + height + 10, width=800, height=height,
                          label="CMP_POP2_SET_LITERACY", font=font,
                          effect="cmp_pop2_set_literacy", tooltip="CMP_POP2_TT_SET_LITERACY",
                          color="0.38 0.68 0.44 0.96")
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_population_professions(lines: list[str], population: dict, profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    line(lines, 3, f'widget = {{ visible = "[GetVariableSystem.HasValue(\'cmp_population2_tab\', \'professions\')]" position = {{ 4 {y} }} size = {{ 840 {514 - y} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_population_professions_{profile["id"]}" size = {{ 840 {514 - y} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    gap = 8
    profession_columns = 2
    profession_width = (800 - gap) // profession_columns
    profession_rows = (len(population["professions"]) + profession_columns - 1) // profession_columns
    content_height = 62 + profession_rows * (height + gap) + 44 + height + 10 + height + 54 + height + 10 + height + 24
    line(lines, 6, f'widget = {{ size = {{ 820 {content_height} }}')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_POP2_PROF_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_population_help', 'professions')",
           tooltip="CMP_WS_POP_HELP_PROFESSIONS_TT", color="0.48 0.58 0.72 0.98")
    cursor_y = 52
    for index, item in enumerate(population["professions"]):
        row, col = divmod(index, profession_columns)
        x = col * (profession_width + gap)
        py = cursor_y + row * (height + gap)
        economy_action_button(lines, 7, x=x, y=py, width=profession_width, height=height,
                              label=item["loc"], font=font,
                              effect=f"cmp_pop2_select_profession_{item['id']}",
                              tooltip="CMP_POP2_TT_PROF",
                              selected=f"cmp_pop2_profession_{item['id']}_selected")
    cursor_y += profession_rows * (height + gap) + 4
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_POP_AMOUNT_TITLE" }}')
    cursor_y += 34
    amount_width = (800 - gap * 5) // 6
    for index, item in enumerate(population["amounts"]):
        x = index * (amount_width + gap)
        economy_action_button(lines, 7, x=x, y=cursor_y, width=amount_width, height=height,
                              label=item["loc"], font=font,
                              effect=f"cmp_pop2_select_amount_{item['id']}",
                              tooltip="CMP_POP2_TT_AMOUNT",
                              selected=f"cmp_pop2_amount_{item['id']}_selected")
    cursor_y += height + 10
    economy_action_button(lines, 7, x=0, y=cursor_y, width=800, height=height,
                          label="CMP_POP2_SPAWN_PROF", font=font,
                          effect="cmp_pop2_spawn_profession", tooltip="CMP_POP2_TT_SPAWN_PROF",
                          color="0.38 0.68 0.44 0.96")
    cursor_y += height + 20
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_POP2_QUAL_TITLE" }}')
    cursor_y += 36
    qualification_width = (800 - gap * 3) // 4
    for index, item in enumerate(population["qualifications"]):
        x = index * (qualification_width + gap)
        economy_action_button(lines, 7, x=x, y=cursor_y, width=qualification_width, height=height,
                              label=item["loc"], font=font,
                              effect=f"cmp_pop2_select_qualification_{item['id']}",
                              tooltip="CMP_POP2_TT_QUAL",
                              selected=f"cmp_pop2_qualification_{item['id']}_selected")
    cursor_y += height + 10
    economy_action_button(lines, 7, x=0, y=cursor_y, width=800, height=height,
                          label="CMP_POP2_APPLY_QUAL", font=font,
                          effect="cmp_pop2_set_qualification", tooltip="CMP_POP2_TT_APPLY_QUAL",
                          color="0.38 0.68 0.44 0.96")
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_population_welfare(lines: list[str], population: dict, profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    line(lines, 3, f'widget = {{ visible = "[GetVariableSystem.HasValue(\'cmp_population2_tab\', \'welfare\')]" position = {{ 4 {y} }} size = {{ 840 {514 - y} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_population_welfare_{profile["id"]}" size = {{ 840 {514 - y} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 820 570 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_POP2_WELFARE_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_population_help', 'welfare')",
           tooltip="CMP_WS_POP_HELP_WELFARE_TT", color="0.48 0.58 0.72 0.98")
    gap = 8
    wealth_width = (800 - gap * 3) // 4
    cursor_y = 52
    for index, item in enumerate(population["wealth"]):
        x = index * (wealth_width + gap)
        economy_action_button(lines, 7, x=x, y=cursor_y, width=wealth_width, height=height,
                              label=item["loc"], font=font,
                              effect=f"cmp_pop2_select_wealth_{item['id']}",
                              tooltip="CMP_POP2_TT_WEALTH",
                              selected=f"cmp_pop2_wealth_{item['id']}_selected")
    cursor_y += height + 10
    economy_action_button(lines, 7, x=0, y=cursor_y, width=800, height=height,
                          label="CMP_POP2_SET_WEALTH", font=font,
                          effect="cmp_pop2_set_wealth", tooltip="CMP_POP2_TT_SET_WEALTH",
                          color="0.38 0.68 0.44 0.96")
    cursor_y += height + 20
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_POP2_POLITICS_TITLE" }}')
    cursor_y += 36
    social_width = (604 - gap * 2) // 3
    social_rows = [
        ("CMP_WS_POP_LOYALISTS", "cmp_pop2_loyalists", "CMP_POP2_TT_LOYALISTS", "0.38 0.68 0.44 0.96"),
        ("CMP_WS_POP_RADICALS", "cmp_pop2_radicals", "CMP_POP2_TT_RADICALS", "0.72 0.38 0.42 0.96"),
        ("CMP_WS_POP_RADICALS_DOWN", "cmp_pop2_reduce_radicals", "CMP_POP2_TT_RADICALS_DOWN", "0.52 0.62 0.40 0.96"),
    ]
    for label, prefix, tooltip, color in social_rows:
        line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 188 {height} }} maximumsize = {{ 188 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{label}" }}')
        for index, item in enumerate(population["social_steps"]):
            x = 196 + index * (social_width + gap)
            economy_action_button(lines, 7, x=x, y=cursor_y, width=social_width, height=height,
                                  label=item["loc"], font=font,
                                  effect=f"{prefix}_{item['id']}", tooltip=tooltip, color=color)
        cursor_y += height + 10
    economy_action_button(lines, 7, x=0, y=cursor_y, width=800, height=height,
                          label="CMP_POP2_NEUTRALIZE", font=font,
                          effect="cmp_pop2_neutralize", tooltip="CMP_POP2_TT_NEUTRALIZE",
                          color="0.64 0.52 0.32 0.96")
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_population_society(lines: list[str], population: dict, profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    line(lines, 3, f'widget = {{ visible = "[GetVariableSystem.HasValue(\'cmp_population2_tab\', \'society\')]" position = {{ 4 {y} }} size = {{ 840 {514 - y} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_population_society_{profile["id"]}" size = {{ 840 {514 - y} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 820 720 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_POP2_SOCIETY_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_population_help', 'society')",
           tooltip="CMP_WS_POP_HELP_SOCIETY_TT", color="0.48 0.58 0.72 0.98")
    gap = 8
    cursor_y = 52
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_POP2_MIGRATION_TITLE" }}')
    cursor_y += 36
    migration_width = (800 - gap * 3) // 4
    for index, item in enumerate(population["migration"]):
        x = index * (migration_width + gap)
        economy_action_button(lines, 7, x=x, y=cursor_y, width=migration_width, height=height,
                              label=item["loc"], font=font,
                              effect=f"cmp_pop2_migration_{item['id']}", tooltip="CMP_POP2_TT_MIGRATION")
    cursor_y += height + 18
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_POP2_WORKFORCE_TITLE" }}')
    cursor_y += 36
    workforce_width = (800 - gap * 2) // 3
    for index, item in enumerate(population["workforce"]):
        x = index * (workforce_width + gap)
        economy_action_button(lines, 7, x=x, y=cursor_y, width=workforce_width, height=height,
                              label=item["loc"], font=font,
                              effect=f"cmp_pop2_workforce_{item['id']}", tooltip="CMP_POP2_TT_WORKFORCE")
    cursor_y += height + 10
    economy_action_button(lines, 7, x=0, y=cursor_y, width=800, height=height,
                          label="CMP_POP2_CLEAR_SOC", font=font,
                          effect="cmp_pop2_clear_society_modifiers", tooltip="CMP_POP2_TT_CLEAR_SOC",
                          color="0.64 0.52 0.32 0.96")
    cursor_y += height + 20
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_POP2_IDENTITY_TITLE" }}')
    cursor_y += 36
    economy_action_button(lines, 7, x=0, y=cursor_y, width=800, height=height,
                          label="CMP_POP2_CONFIRM", font=font,
                          effect="cmp_pop2_toggle_society_confirmation", tooltip="CMP_POP2_TT_CONFIRM",
                          color="0.72 0.52 0.30 0.96", selected="cmp_pop2_society_confirmed")
    cursor_y += height + 8
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 32 }} maximumsize = {{ 800 32 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_POP_IDENTITY_WARNING" }}')
    cursor_y += 38
    identity_width = (800 - gap) // 2
    economy_action_button(lines, 7, x=0, y=cursor_y, width=identity_width, height=height,
                          label="CMP_POP2_ASSIMILATE", font=font,
                          effect="cmp_pop2_assimilate", tooltip="CMP_POP2_TT_ASSIMILATE",
                          color="0.72 0.38 0.42 0.96")
    economy_action_button(lines, 7, x=identity_width + gap, y=cursor_y, width=identity_width, height=height,
                          label="CMP_POP2_CONVERT_REL", font=font,
                          effect="cmp_pop2_convert_religion", tooltip="CMP_POP2_TT_CONVERT",
                          color="0.72 0.38 0.42 0.96")
    cursor_y += height + 20
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_POP2_PRESETS_TITLE" }}')
    cursor_y += 36
    preset_width = (800 - gap * 2) // 3
    presets = [
        ("CMP_POP2_PRESET_INDUSTRIAL", "cmp_pop2_preset_industrial", "CMP_POP2_TT_PRESET_INDUSTRIAL"),
        ("CMP_POP2_PRESET_EDUCATED", "cmp_pop2_preset_educated", "CMP_POP2_TT_PRESET_EDUCATED"),
        ("CMP_POP2_PRESET_STABLE", "cmp_pop2_preset_stable", "CMP_POP2_TT_PRESET_STABLE"),
    ]
    for index, (label, effect, tooltip) in enumerate(presets):
        economy_action_button(lines, 7, x=index * (preset_width + gap), y=cursor_y,
                              width=preset_width, height=height, label=label, font=font,
                              effect=effect, tooltip=tooltip, color="0.42 0.58 0.72 0.96")
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_population_help(lines: list[str], profile: dict) -> None:
    font = profile["font_size"]
    profile_id = profile["id"]
    line(lines, 3, 'widget = { name = "cmp_workspace_population_help_card" visible = "[GetVariableSystem.Exists(\'cmp_workspace_population_help\')]" position = { 32 72 } size = { 792 420 }')
    line(lines, 4, 'icon = { size = { 792 420 } texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = { 0.045 0.055 0.075 0.998 } }')
    line(lines, 4, 'icon = { position = { 2 2 } size = { 788 416 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.98 } alwaystransparent = yes }')
    line(lines, 4, f'textbox = {{ position = {{ 20 14 }} size = {{ 680 36 }} maximumsize = {{ 680 36 }} fontsize = {font + 4} fontsize_min = 14 align = left text = "CMP_WS_POP_HELP_TITLE" }}')
    line(lines, 4, 'close_button = { position = { 736 10 } size = { 42 42 } onclick = "[GetVariableSystem.Clear(\'cmp_workspace_population_help\')]" }')
    topics = [
        ("overview", "CMP_WS_POP_HELP_OVERVIEW"),
        ("population", "CMP_WS_POP_HELP_POPULATION"),
        ("professions", "CMP_WS_POP_HELP_PROFESSIONS"),
        ("welfare", "CMP_WS_POP_HELP_WELFARE"),
        ("society", "CMP_WS_POP_HELP_SOCIETY"),
    ]
    for topic, key in topics:
        line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_population_help_{topic}_{profile_id}" visible = "[GetVariableSystem.HasValue(\'cmp_workspace_population_help\', \'{topic}\')]" position = {{ 20 60 }} size = {{ 752 338 }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
        line(lines, 5, 'scrollwidget = {')
        line(lines, 6, f'textbox = {{ size = {{ 720 820 }} maximumsize = {{ 720 820 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "{key}" }}')
        line(lines, 5, '}')
        line(lines, 4, '}')
    line(lines, 3, '}')


def render_population_page(lines: list[str], population: dict, profile: dict) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    line(lines, 2, f'widget = {{ visible = "{page_visible("population")}" position = {{ 238 76 }} size = {{ 864 514 }}')
    line(lines, 3, f'textbox = {{ position = {{ 4 0 }} size = {{ 360 34 }} maximumsize = {{ 360 34 }} fontsize = {font + 6} fontsize_min = 14 align = left text = "CMP_POP2_TITLE" }}')
    button(lines, 3, x=372, y=0, width=56, height=height, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_population_help', 'overview')",
           tooltip="CMP_WS_POP_HELP_OVERVIEW_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 3, f'textbox = {{ position = {{ 4 40 }} size = {{ 498 30 }} maximumsize = {{ 498 30 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_POP_FLOW" }}')
    button(lines, 3, x=610, y=0, width=214, height=height, label="CMP_POP2_TARGETS", font=font,
           action="GetVariableSystem.Set('cmp_workspace_page', 'target')",
           tooltip="CMP_POP2_TARGET_TT", color="0.45 0.62 0.82 0.97")
    line(lines, 3, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_pop2_target_valid\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" position = {{ 610 {height + 2} }} size = {{ 214 28 }} maximumsize = {{ 214 28 }} fontsize = {font} fontsize_min = 12 align = center text = "CMP_WS_POP_TARGET_READY" }}')
    line(lines, 3, f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_pop2_target_valid\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End))]" position = {{ 610 {height + 2} }} size = {{ 214 28 }} maximumsize = {{ 214 28 }} fontsize = {font} fontsize_min = 12 align = center text = "CMP_WS_POP_TARGET_REQUIRED" }}')
    tab_y = max(82, height + 34)
    render_population_tabs(lines, profile, y=tab_y)
    content_y = tab_y + height + 10
    render_population_main(lines, population, profile, y=content_y)
    render_population_professions(lines, population, profile, y=content_y)
    render_population_welfare(lines, population, profile, y=content_y)
    render_population_society(lines, population, profile, y=content_y)
    render_population_help(lines, profile)
    line(lines, 2, '}')


def politics_tab_visible(tab: str) -> str:
    if tab == "government":
        return ("[Or(Not(GetVariableSystem.Exists('cmp_workspace_politics_tab')), "
                "GetVariableSystem.HasValue('cmp_workspace_politics_tab', 'government'))]")
    return f"[GetVariableSystem.HasValue('cmp_workspace_politics_tab', '{tab}')]"


def render_politics_tabs(lines: list[str], profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    tabs = [
        ("CMP_WS_POL_TAB_GOV", "government", "CMP_WS_POL_HELP_GOVERNMENT_TT"),
        ("CMP_WS_POL_TAB_CHAR", "characters", "CMP_WS_POL_HELP_CHARACTERS_TT"),
        ("CMP_WS_POL_TAB_IG", "interest_groups", "CMP_WS_POL_HELP_IG_TT"),
        ("CMP_WS_POL_TAB_LAW", "laws", "CMP_WS_POL_HELP_LAWS_TT"),
        ("CMP_WS_POL_TAB_BLOC", "bloc", "CMP_WS_POL_HELP_BLOC_TT"),
    ]
    gap = 7
    width = (820 - gap * 4) // 5
    for index, (label, tab, tooltip) in enumerate(tabs):
        x = 4 + index * (width + gap)
        button(lines, 3, x=x, y=y, width=width, height=height, label=label, font=font,
               action=f"GetVariableSystem.Set('cmp_workspace_politics_tab', '{tab}')",
               tooltip=tooltip, color="0.40 0.53 0.68 0.97")
        line(lines, 3, f'icon = {{ visible = "{politics_tab_visible(tab)}" position = {{ {x + 4} {y + height - 4} }} size = {{ {width - 8} 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')


def render_politics_government(lines: list[str], politics: dict, profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    area_height = 514 - y
    line(lines, 3, f'widget = {{ visible = "{politics_tab_visible("government")}" position = {{ 4 {y} }} size = {{ 840 {area_height} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_politics_government_{profile["id"]}" size = {{ 840 {area_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 820 1010 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_POL2_GOV_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_politics_help', 'government')",
           tooltip="CMP_WS_POL_HELP_GOVERNMENT_TT", color="0.48 0.58 0.72 0.98")
    cursor_y = 54
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_POL_GOV_PARAMETER" }}')
    cursor_y += 36
    gap = 8
    width = (800 - gap) // 2
    params = [
        ("CMP_POL2_GOV_LEGIT", 1), ("CMP_POL2_GOV_AUTH", 2),
        ("CMP_POL2_GOV_BUREAU", 3), ("CMP_POL2_GOV_INFL", 4),
    ]
    for index, (label, number) in enumerate(params):
        row, col = divmod(index, 2)
        economy_action_button(lines, 7, x=col * (width + gap), y=cursor_y + row * (height + gap),
                              width=width, height=height, label=label, font=font,
                              effect=f"cmp_politics2_select_gov_param_{number}",
                              tooltip="CMP_POL2_TT_GOV_PARAM",
                              selected=f"cmp_politics2_gov_param_{number}_selected")
    cursor_y += 2 * (height + gap) + 8
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_POL_GOV_VALUE" }}')
    cursor_y += 36
    value_width = (800 - gap * 3) // 4
    for index, value in enumerate([10, 25, 50, 100]):
        economy_action_button(lines, 7, x=index * (value_width + gap), y=cursor_y,
                              width=value_width, height=height, label=f"CMP_POL2_VALUE_{value}", font=font,
                              effect=f"cmp_politics2_select_gov_value_{value}",
                              tooltip="CMP_POL2_TT_GOV_VALUE",
                              selected=f"cmp_politics2_gov_value_{value}_selected")
    cursor_y += height + 10
    economy_action_button(lines, 7, x=0, y=cursor_y, width=width, height=height,
                          label="CMP_POL2_APPLY", font=font, effect="cmp_politics2_gov_apply",
                          tooltip="CMP_POL2_TT_GOV_APPLY", color="0.38 0.68 0.44 0.96")
    economy_action_button(lines, 7, x=width + gap, y=cursor_y, width=width, height=height,
                          label="CMP_POL2_RESET", font=font, effect="cmp_politics2_gov_reset",
                          tooltip="CMP_POL2_TT_GOV_RESET", color="0.68 0.46 0.36 0.96")
    cursor_y += height + 22
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_POL2_INST_TITLE" }}')
    cursor_y += 36
    for index, institution in enumerate(politics["institutions"]):
        row, col = divmod(index, 2)
        economy_action_button(lines, 7, x=col * (width + gap), y=cursor_y + row * (height + gap),
                              width=width, height=height, label=institution["loc"], font=font,
                              effect=f"cmp_politics2_select_inst_{index + 1}",
                              tooltip="CMP_POL2_INST_SELECT_TT",
                              selected=f"cmp_politics2_inst_{index + 1}_selected")
    cursor_y += 4 * (height + gap) + 8
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_POL_INST_LEVEL" }}')
    cursor_y += 36
    level_width = (800 - gap * 4) // 5
    for index, level_number in enumerate(range(1, 6)):
        economy_action_button(lines, 7, x=index * (level_width + gap), y=cursor_y,
                              width=level_width, height=height, label=f"CMP_POL2_LEVEL_{level_number}", font=font,
                              effect=f"cmp_politics2_select_inst_level_{level_number}",
                              tooltip="CMP_POL2_INST_LEVEL_TT",
                              selected=f"cmp_politics2_inst_level_{level_number}_selected")
    cursor_y += height + 10
    economy_action_button(lines, 7, x=0, y=cursor_y, width=800, height=height,
                          label="CMP_POL2_INST_APPLY", font=font,
                          effect="cmp_politics2_institution_apply",
                          tooltip="CMP_POL2_INST_APPLY_TT", color="0.38 0.68 0.44 0.96")
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_politics_characters(lines: list[str], politics: dict, profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    area_height = 514 - y
    line(lines, 3, f'widget = {{ visible = "{politics_tab_visible("characters")}" position = {{ 4 {y} }} size = {{ 840 {area_height} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_politics_characters_{profile["id"]}" size = {{ 840 {area_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 820 1120 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_POL2_CHAR_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_politics_help', 'characters')",
           tooltip="CMP_WS_POL_HELP_CHARACTERS_TT", color="0.48 0.58 0.72 0.98")
    gap = 8
    width = (800 - gap) // 2
    cursor_y = 54
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_POL_CHAR_IMMORTALITY" }}')
    cursor_y += 36
    for index, (label, effect) in enumerate([
        ("CMP_POL2_IMMORTAL_ON", "cmp_politics2_char_immortal_on"),
        ("CMP_POL2_IMMORTAL_OFF", "cmp_politics2_char_immortal_off"),
    ]):
        economy_action_button(lines, 7, x=index * (width + gap), y=cursor_y, width=width, height=height,
                              label=label, font=font, effect=effect, tooltip="CMP_POL2_TT_IMMORTAL")
    cursor_y += height + 18
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_POL_CHAR_HEALTH" }}')
    cursor_y += 36
    health = [
        ("CMP_POL2_HEALTH_5", "cmp_politics2_char_health_0p05"),
        ("CMP_POL2_HEALTH_20", "cmp_politics2_char_health_0p2"),
        ("CMP_POL2_HEALTH_100", "cmp_politics2_char_health_1p0"),
        ("CMP_POL2_HEALTH_RESET", "cmp_politics2_char_health_reset"),
    ]
    for index, (label, effect) in enumerate(health):
        row, col = divmod(index, 2)
        economy_action_button(lines, 7, x=col * (width + gap), y=cursor_y + row * (height + gap),
                              width=width, height=height, label=label, font=font,
                              effect=effect, tooltip="CMP_POL2_TT_HEALTH",
                              color="0.68 0.46 0.36 0.96" if index == 3 else "0.42 0.50 0.62 0.98")
    cursor_y += 2 * (height + gap) + 10
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_POL_CHAR_POPULARITY" }}')
    cursor_y += 36
    popularity = [
        ("CMP_POL2_POPULARITY_5", "cmp_politics2_char_popularity_5"),
        ("CMP_POL2_POPULARITY_25", "cmp_politics2_char_popularity_25"),
        ("CMP_POL2_POPULARITY_100", "cmp_politics2_char_popularity_100"),
        ("CMP_POL2_POPULARITY_RESET", "cmp_politics2_char_popularity_reset"),
    ]
    for index, (label, effect) in enumerate(popularity):
        row, col = divmod(index, 2)
        economy_action_button(lines, 7, x=col * (width + gap), y=cursor_y + row * (height + gap),
                              width=width, height=height, label=label, font=font,
                              effect=effect, tooltip="CMP_POL2_TT_POPULARITY",
                              color="0.68 0.46 0.36 0.96" if index == 3 else "0.42 0.50 0.62 0.98")
    cursor_y += 2 * (height + gap) + 10
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_POL_CHAR_RANK" }}')
    cursor_y += 36
    rank_width = (800 - gap * 4) // 5
    for index, rank in enumerate(range(1, 6)):
        economy_action_button(lines, 7, x=index * (rank_width + gap), y=cursor_y,
                              width=rank_width, height=height, label=f"CMP_POL2_RANK_{rank}", font=font,
                              effect=f"cmp_politics2_char_rank_{rank}", tooltip="CMP_POL2_RANK_TT")
    cursor_y += height + 18
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_POL_CHAR_ROLES" }}')
    cursor_y += 36
    roles = [
        ("CMP_POL2_ROLE_GENERAL_ADD", "cmp_politics2_char_role_general_add"),
        ("CMP_POL2_ROLE_GENERAL_REMOVE", "cmp_politics2_char_role_general_remove"),
        ("CMP_POL2_ROLE_ADMIRAL_ADD", "cmp_politics2_char_role_admiral_add"),
        ("CMP_POL2_ROLE_ADMIRAL_REMOVE", "cmp_politics2_char_role_admiral_remove"),
    ]
    for index, (label, effect) in enumerate(roles):
        row, col = divmod(index, 2)
        economy_action_button(lines, 7, x=col * (width + gap), y=cursor_y + row * (height + gap),
                              width=width, height=height, label=label, font=font, effect=effect,
                              tooltip="CMP_POL2_ROLE_TT",
                              color="0.72 0.38 0.42 0.96" if "remove" in effect else "0.42 0.50 0.62 0.98")
    cursor_y += 2 * (height + gap) + 6
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 44 }} maximumsize = {{ 800 44 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_POL_ROLE_WARNING" }}')
    cursor_y += 50
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_POL_CHAR_TRAITS" }}')
    cursor_y += 36
    for index, trait in enumerate(politics["traits"]):
        row_y = cursor_y + index * (height + gap)
        line(lines, 7, f'textbox = {{ position = {{ 0 {row_y} }} size = {{ 316 {height} }} maximumsize = {{ 316 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{trait["loc"]}" }}')
        economy_action_button(lines, 7, x=324, y=row_y, width=230, height=height,
                              label="CMP_WS_POL_ADD", font=font,
                              effect=f"cmp_politics2_char_trait_{trait['id']}_add",
                              tooltip="CMP_POL2_TRAIT_ADD_TT", color="0.38 0.68 0.44 0.96")
        economy_action_button(lines, 7, x=562, y=row_y, width=238, height=height,
                              label="CMP_POL2_REMOVE_SHORT", font=font,
                              effect=f"cmp_politics2_char_trait_{trait['id']}_remove",
                              tooltip="CMP_POL2_TRAIT_REMOVE_TT", color="0.72 0.38 0.42 0.96")
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_politics_interest_groups(lines: list[str], politics: dict, profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    area_height = 514 - y
    line(lines, 3, f'widget = {{ visible = "{politics_tab_visible("interest_groups")}" position = {{ 4 {y} }} size = {{ 840 {area_height} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_politics_interest_groups_{profile["id"]}" size = {{ 840 {area_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 820 850 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_POL2_IG_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_politics_help', 'interest_groups')",
           tooltip="CMP_WS_POL_HELP_IG_TT", color="0.48 0.58 0.72 0.98")
    gap = 8
    width = (800 - gap) // 2
    cursor_y = 54
    for index, group in enumerate(politics["interest_groups"]):
        row, col = divmod(index, 2)
        economy_action_button(lines, 7, x=col * (width + gap), y=cursor_y + row * (height + gap),
                              width=width, height=height, label=group["loc"], font=font,
                              effect=f"cmp_politics2_ig_toggle_{group['id']}",
                              tooltip="CMP_POL2_IG_SELECT_TT",
                              selected=f"cmp_politics2_ig_{group['id']}_selected")
    cursor_y += 4 * (height + gap) + 10
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_POL_IG_APPROVAL" }}')
    cursor_y += 36
    action_width = (800 - gap * 2) // 3
    approval = [
        ("CMP_POL2_PLUS5", "5"), ("CMP_POL2_PLUS10", "10"), ("CMP_POL2_PLUS20", "20"),
        ("CMP_POL2_MINUS5", "n5"), ("CMP_POL2_MINUS10", "n10"), ("CMP_POL2_RESET", "0"),
    ]
    for index, (label, suffix) in enumerate(approval):
        row, col = divmod(index, 3)
        economy_action_button(lines, 7, x=col * (action_width + gap), y=cursor_y + row * (height + gap),
                              width=action_width, height=height, label=label, font=font,
                              effect=f"cmp_politics2_ig_approval_{suffix}",
                              tooltip="CMP_POL2_IG_APPROVAL_TT")
    cursor_y += 2 * (height + gap) + 10
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_POL2_IG_STRENGTH" }}')
    cursor_y += 36
    strength = [
        ("CMP_POL2_PLUS25P", "25"), ("CMP_POL2_PLUS50P", "50"), ("CMP_POL2_PLUS100P", "100"),
        ("CMP_POL2_PLUS500P", "500"), ("CMP_POL2_MINUS50P", "n50"), ("CMP_POL2_RESET", "0"),
    ]
    for index, (label, suffix) in enumerate(strength):
        row, col = divmod(index, 3)
        economy_action_button(lines, 7, x=col * (action_width + gap), y=cursor_y + row * (height + gap),
                              width=action_width, height=height, label=label, font=font,
                              effect=f"cmp_politics2_ig_strength_{suffix}",
                              tooltip="CMP_POL2_IG_STRENGTH_TT")
    cursor_y += 2 * (height + gap) + 8
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 50 }} maximumsize = {{ 800 50 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_POL_IG_WARNING" }}')
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_politics_laws(lines: list[str], profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    area_height = 514 - y
    line(lines, 3, f'widget = {{ visible = "{politics_tab_visible("laws")}" position = {{ 4 {y} }} size = {{ 840 {area_height} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_politics_laws_{profile["id"]}" size = {{ 840 {area_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 820 560 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_POL2_LAW_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_politics_help', 'laws')",
           tooltip="CMP_WS_POL_HELP_LAWS_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 54 }} size = {{ 800 50 }} maximumsize = {{ 800 50 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_POL_LAW_WARNING" }}')
    gap = 8
    width = (800 - gap) // 2
    actions = [
        ("CMP_POL2_LAW_PROGRESS10", "cmp_politics2_law_progress_10", "0.42 0.50 0.62 0.98"),
        ("CMP_POL2_LAW_PROGRESS25", "cmp_politics2_law_progress_25", "0.42 0.50 0.62 0.98"),
        ("CMP_POL2_LAW_ADVANCE", "cmp_politics2_law_advance", "0.42 0.50 0.62 0.98"),
        ("CMP_POL2_LAW_SETBACK", "cmp_politics2_law_setback", "0.72 0.48 0.32 0.96"),
        ("CMP_POL2_LAW_COMPLETE", "cmp_politics2_law_complete", "0.72 0.38 0.42 0.96"),
        ("CMP_POL2_LAW_CANCEL", "cmp_politics2_law_cancel", "0.72 0.38 0.42 0.96"),
        ("CMP_POL2_LAW_CLEAR_MODS", "cmp_politics2_law_clear_modifiers", "0.68 0.46 0.36 0.96"),
    ]
    for index, (label, effect, color) in enumerate(actions):
        row, col = divmod(index, 2)
        economy_action_button(lines, 7, x=col * (width + gap), y=114 + row * (height + gap),
                              width=width, height=height, label=label, font=font,
                              effect=effect, tooltip="CMP_POL2_LAW_ACTION_TT", color=color)
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_politics_bloc(lines: list[str], profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    area_height = 514 - y
    line(lines, 3, f'widget = {{ visible = "{politics_tab_visible("bloc")}" position = {{ 4 {y} }} size = {{ 840 {area_height} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_politics_bloc_{profile["id"]}" size = {{ 840 {area_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 820 460 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 44 }} maximumsize = {{ 730 44 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_POL2_BLOC_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_politics_help', 'bloc')",
           tooltip="CMP_WS_POL_HELP_BLOC_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 54 }} size = {{ 800 46 }} maximumsize = {{ 800 46 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_POL_BLOC_LIMIT" }}')
    gap = 8
    width = (800 - gap) // 2
    actions = [
        ("CMP_POL2_PLUS25", "cmp_politics2_bloc_cohesion_p25"),
        ("CMP_POL2_PLUS50", "cmp_politics2_bloc_cohesion_p50"),
        ("CMP_POL2_MINUS25", "cmp_politics2_bloc_cohesion_n25"),
        ("CMP_POL2_SET100", "cmp_politics2_bloc_cohesion_100"),
    ]
    for index, (label, effect) in enumerate(actions):
        row, col = divmod(index, 2)
        economy_action_button(lines, 7, x=col * (width + gap), y=110 + row * (height + gap),
                              width=width, height=height, label=label, font=font,
                              effect=effect, tooltip="CMP_POL2_BLOC_TT")
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_politics_help(lines: list[str], profile: dict) -> None:
    font = profile["font_size"]
    profile_id = profile["id"]
    line(lines, 3, 'widget = { name = "cmp_workspace_politics_help_card" visible = "[GetVariableSystem.Exists(\'cmp_workspace_politics_help\')]" position = { 32 72 } size = { 792 420 }')
    line(lines, 4, 'icon = { size = { 792 420 } texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = { 0.045 0.055 0.075 0.998 } }')
    line(lines, 4, 'icon = { position = { 2 2 } size = { 788 416 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.98 } alwaystransparent = yes }')
    line(lines, 4, f'textbox = {{ position = {{ 20 14 }} size = {{ 680 36 }} maximumsize = {{ 680 36 }} fontsize = {font + 4} fontsize_min = 14 align = left text = "CMP_WS_POL_HELP_TITLE" }}')
    line(lines, 4, 'close_button = { position = { 736 10 } size = { 42 42 } onclick = "[GetVariableSystem.Clear(\'cmp_workspace_politics_help\')]" }')
    topics = [
        ("overview", "CMP_WS_POL_HELP_OVERVIEW"),
        ("government", "CMP_WS_POL_HELP_GOVERNMENT"),
        ("characters", "CMP_WS_POL_HELP_CHARACTERS"),
        ("interest_groups", "CMP_WS_POL_HELP_IG"),
        ("laws", "CMP_WS_POL_HELP_LAWS"),
        ("bloc", "CMP_WS_POL_HELP_BLOC"),
    ]
    for topic, key in topics:
        line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_politics_help_{topic}_{profile_id}" visible = "[GetVariableSystem.HasValue(\'cmp_workspace_politics_help\', \'{topic}\')]" position = {{ 20 60 }} size = {{ 752 338 }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
        line(lines, 5, 'scrollwidget = {')
        line(lines, 6, f'textbox = {{ size = {{ 720 900 }} maximumsize = {{ 720 900 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "{key}" }}')
        line(lines, 5, '}')
        line(lines, 4, '}')
    line(lines, 3, '}')


def render_politics_page(lines: list[str], politics: dict, profile: dict) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    line(lines, 2, f'widget = {{ visible = "{page_visible("politics")}" position = {{ 238 76 }} size = {{ 864 514 }}')
    line(lines, 3, f'textbox = {{ position = {{ 4 0 }} size = {{ 420 36 }} maximumsize = {{ 420 36 }} fontsize = {font + 6} fontsize_min = 14 align = left text = "CMP_POL2_TITLE" }}')
    button(lines, 3, x=432, y=0, width=56, height=height, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_politics_help', 'overview')",
           tooltip="CMP_WS_POL_HELP_OVERVIEW_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 3, f'textbox = {{ position = {{ 4 40 }} size = {{ 500 30 }} maximumsize = {{ 500 30 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_POL_FLOW" }}')
    button(lines, 3, x=610, y=0, width=214, height=height, label="CMP_POL2_TARGETS", font=font,
           action="GetVariableSystem.Set('cmp_workspace_page', 'target')",
           tooltip="CMP_POL2_TARGETS_TT", color="0.45 0.62 0.82 0.97")
    target_tabs = [
        ("government", "cmp_politics2_country_target_valid"),
        ("characters", "cmp_politics2_character_target_valid"),
        ("interest_groups", "cmp_politics2_country_target_valid"),
        ("laws", "cmp_politics2_law_target_valid"),
        ("bloc", "cmp_politics2_bloc_target_valid"),
    ]
    for tab, predicate in target_tabs:
        tab_visible = politics_tab_visible(tab)[1:-1]
        ready = f"[And({tab_visible}, GetScriptedGui('{predicate}').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End))]"
        required = f"[And({tab_visible}, Not(GetScriptedGui('{predicate}').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)))]"
        line(lines, 3, f'textbox = {{ visible = "{ready}" position = {{ 610 {height + 2} }} size = {{ 214 28 }} maximumsize = {{ 214 28 }} fontsize = {font} fontsize_min = 12 align = center text = "CMP_WS_POL_TARGET_READY" }}')
        line(lines, 3, f'textbox = {{ visible = "{required}" position = {{ 610 {height + 2} }} size = {{ 214 28 }} maximumsize = {{ 214 28 }} fontsize = {font} fontsize_min = 12 align = center text = "CMP_WS_POL_TARGET_REQUIRED" }}')
    tab_y = max(88, height + 36)
    render_politics_tabs(lines, profile, y=tab_y)
    content_y = tab_y + height + 10
    render_politics_government(lines, politics, profile, y=content_y)
    render_politics_characters(lines, politics, profile, y=content_y)
    render_politics_interest_groups(lines, politics, profile, y=content_y)
    render_politics_laws(lines, profile, y=content_y)
    render_politics_bloc(lines, profile, y=content_y)
    render_politics_help(lines, profile)
    line(lines, 2, '}')


def military_tab_visible(tab: str) -> str:
    if tab == "army_builder":
        return ("[Or(Not(GetVariableSystem.Exists('cmp_workspace_military_tab')), "
                "GetVariableSystem.HasValue('cmp_workspace_military_tab', 'army_builder'))]")
    return f"[GetVariableSystem.HasValue('cmp_workspace_military_tab', '{tab}')]"


def military_subtab_visible(variable: str, tab: str, default: str) -> str:
    if tab == default:
        return (f"[Or(Not(GetVariableSystem.Exists('{variable}')), "
                f"GetVariableSystem.HasValue('{variable}', '{tab}'))]")
    return f"[GetVariableSystem.HasValue('{variable}', '{tab}')]"


def render_military_tabs(lines: list[str], profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    tabs = [
        ("CMP_WS_MIL_TAB_ARMY", "army_builder", "CMP_WS_MIL_HELP_ARMY_TT"),
        ("CMP_WS_MIL_TAB_ARMY_TEMPLATES", "army_templates", "CMP_WS_MIL_HELP_TEMPLATES_TT"),
        ("CMP_WS_MIL_TAB_CONTROLS", "army_controls", "CMP_WS_MIL_HELP_CONTROLS_TT"),
        ("CMP_WS_MIL_TAB_FLEET", "fleet_builder", "CMP_WS_MIL_HELP_FLEET_TT"),
    ]
    gap = 7
    width = (820 - gap * 3) // 4
    for index, (label, tab, tooltip) in enumerate(tabs):
        x = 4 + index * (width + gap)
        button(lines, 3, x=x, y=y, width=width, height=height, label=label, font=font,
               action=f"GetVariableSystem.Set('cmp_workspace_military_tab', '{tab}')",
               tooltip=tooltip, color="0.40 0.53 0.68 0.97")
        line(lines, 3, f'icon = {{ visible = "{military_tab_visible(tab)}" position = {{ {x + 4} {y + height - 4} }} size = {{ {width - 8} 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')


def render_military_subtabs(lines: list[str], profile: dict, *, y: int, variable: str,
                            tabs: list[tuple[str, str, str]], default: str) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    gap = 8
    width = (800 - gap * (len(tabs) - 1)) // len(tabs)
    for index, (label, tab, tooltip) in enumerate(tabs):
        x = index * (width + gap)
        button(lines, 5, x=x, y=y, width=width, height=height, label=label, font=font,
               action=f"GetVariableSystem.Set('{variable}', '{tab}')",
               tooltip=tooltip, color="0.40 0.53 0.68 0.97")
        line(lines, 5, f'icon = {{ visible = "{military_subtab_visible(variable, tab, default)}" position = {{ {x + 4} {y + height - 4} }} size = {{ {width - 8} 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')


def render_fleet_target_row(lines: list[str], indent: int, profile: dict, *, y: int) -> int:
    """Render Victoria-native selected formation as the existing-fleet source of truth."""
    font = profile["font_size"]
    height = profile["button_height"]
    button(lines, indent, x=0, y=y, width=426, height=height, label="CMP_MIL_TARGET_FLEET_SELECT", font=font,
           action="GetVariableSystem.Toggle('cmp_workspace_fleet_picker')",
           tooltip="CMP_MIL_TARGET_FLEET_SELECT_TT", color="0.45 0.62 0.82 0.97")
    # GetSelectedFormation remains an observed native value in pre2.4; it is no longer assumed to update from the custom picker.
    line(lines, indent, f'widget = {{ visible = "[GetSelectedFormation.IsFleet]" datacontext = "[GetSelectedFormation]" position = {{ 438 {y} }} size = {{ 362 {height} }}')
    line(lines, indent + 1, f'textbox = {{ size = {{ 362 {height} }} maximumsize = {{ 362 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline elide = right text = "[MilitaryFormation.GetNameNoFormatting]" tooltip = "[MilitaryFormation.GetNameNoFormatting]" }}')
    formation_root = "GuiScope.SetRoot(MilitaryFormation.MakeScope).End"
    line(lines, indent + 1, f'icon = {{ visible = "[GetScriptedGui(\'cmp_military_native_fleet_ready\').IsShown({formation_root})]" position = {{ 0 {height - 4} }} size = {{ 356 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes tooltip = "CMP_MIL_NATIVE_FLEET_READY_TT" }}')
    line(lines, indent + 1, f'icon = {{ visible = "[GetScriptedGui(\'cmp_military_native_fleet_blocked_battle\').IsShown({formation_root})]" position = {{ 0 {height - 4} }} size = {{ 356 4 }} color = {{ 0.95 0.35 0.35 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes tooltip = "CMP_MIL_NATIVE_FLEET_BATTLE_TT" }}')
    line(lines, indent, '}')
    line(lines, indent, f'textbox = {{ visible = "[GetSelectedFormation.IsArmy]" position = {{ 438 {y} }} size = {{ 362 {height} }} maximumsize = {{ 362 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_MIL_NATIVE_FLEET_ARMY_SELECTED" }}')
    line(lines, indent, f'textbox = {{ visible = "[Not(Or(GetSelectedFormation.IsFleet, GetSelectedFormation.IsArmy))]" position = {{ 438 {y} }} size = {{ 362 {height} }} maximumsize = {{ 362 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_MIL_TARGET_FLEET_NONE" }}')
    return y + height + 12


def render_military_fleet_picker(lines: list[str], profile: dict) -> None:
    """Render exact fleet rows with a vanilla panel-open bridge and independent scope probes."""
    font = profile["font_size"]
    height = profile["button_height"]
    profile_id = profile["id"]
    formation_scope = "GuiScope.SetRoot(MilitaryFormation.MakeScope).End"
    line(lines, 3, 'widget = { name = "cmp_workspace_fleet_picker" visible = "[GetVariableSystem.Exists(\'cmp_workspace_fleet_picker\')]" position = { 34 64 } size = { 792 438 }')
    line(lines, 4, 'icon = { size = { 792 438 } texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = { 0.035 0.045 0.065 0.998 } }')
    line(lines, 4, 'icon = { position = { 2 2 } size = { 788 434 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.98 } alwaystransparent = yes }')
    line(lines, 4, f'textbox = {{ position = {{ 20 14 }} size = {{ 680 34 }} maximumsize = {{ 680 34 }} fontsize = {font + 4} fontsize_min = 14 align = left text = "CMP_MIL_TARGET_FLEET_PICKER_TITLE" }}')
    line(lines, 4, 'close_button = { position = { 736 10 } size = { 42 42 } onclick = "[GetVariableSystem.Clear(\'cmp_workspace_fleet_picker\')]" }')
    line(lines, 4, f'textbox = {{ position = {{ 20 54 }} size = {{ 742 44 }} maximumsize = {{ 742 44 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_MIL_NATIVE_PICKER_DESC" }}')
    line(lines, 4, f'textbox = {{ visible = "[GetSelectedFormation.IsFleet]" position = {{ 20 100 }} size = {{ 360 22 }} maximumsize = {{ 360 22 }} fontsize = {max(12,font-1)} fontsize_min = 12 align = left|nobaseline text = "CMP_MIL_NATIVE_SELECTION_OK" }}')
    line(lines, 4, f'textbox = {{ visible = "[Not(GetSelectedFormation.IsFleet)]" position = {{ 20 100 }} size = {{ 360 22 }} maximumsize = {{ 360 22 }} fontsize = {max(12,font-1)} fontsize_min = 12 align = left|nobaseline text = "CMP_MIL_NATIVE_SELECTION_WAIT" }}')
    line(lines, 4, 'widget = { visible = "[GetSelectedFormation.IsFleet]" datacontext = "[GetSelectedFormation]" position = { 392 100 } size = { 360 22 }')
    line(lines, 5, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_military_native_fleet_root_probe\').IsShown(GuiScope.SetRoot(MilitaryFormation.MakeScope).End)]" size = {{ 360 22 }} maximumsize = {{ 360 22 }} fontsize = {max(12,font-1)} fontsize_min = 12 align = right|nobaseline text = "CMP_MIL_NATIVE_ROOT_OK" }}')
    line(lines, 4, '}')
    line(lines, 4, f'textbox = {{ visible = "[Not(GetSelectedFormation.IsFleet)]" position = {{ 392 100 }} size = {{ 360 22 }} maximumsize = {{ 360 22 }} fontsize = {max(12,font-1)} fontsize_min = 12 align = right|nobaseline text = "CMP_MIL_NATIVE_ROOT_WAIT" }}')
    line(lines, 4, 'widget = { datacontext = "[GetPlayer]" position = { 20 128 } size = { 752 286 }')
    line(lines, 5, f'textbox = {{ visible = "[IsDataModelEmpty(Country.GetMilitaryFormationsFleet)]" position = {{ 0 16 }} size = {{ 728 50 }} maximumsize = {{ 728 50 }} multiline = yes autoresize = no fontsize = {font + 1} fontsize_min = 12 align = center text = "CMP_MIL_TARGET_FLEET_PICKER_EMPTY" }}')
    line(lines, 5, f'scrollarea = {{ name = "cmp_workspace_fleet_picker_scroll_{profile_id}" size = {{ 752 286 }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 6, 'scrollwidget = {')
    line(lines, 7, 'flowcontainer = { direction = vertical spacing = 8 minimumsize = { 724 296 } maximumsize = { 724 -1 } datamodel = "[Country.GetMilitaryFormationsFleet]"')
    line(lines, 8, 'item = {')
    button(lines, 9, x=0, y=0, width=716, height=height, label="[MilitaryFormation.GetNameNoFormatting]", font=font,
           action="InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')",
           tooltip="[MilitaryFormation.GetNameNoFormatting]", color="0.43 0.55 0.70 0.98", elide=True, label_transparent=True)
    # Yellow = the bare MakeScope -> ScriptedGui transport works. Blue = the same root can resolve owner=player.
    line(lines, 9, f'icon = {{ visible = "[GetScriptedGui(\'cmp_military_native_fleet_root_probe\').IsShown({formation_scope})]" position = {{ 704 6 }} size = {{ 6 {max(16,height-12)} }} color = {{ 0.92 0.74 0.25 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes tooltip = "CMP_MIL_TARGET_FLEET_SCOPE_PROBE_TT" }}')
    line(lines, 9, f'icon = {{ visible = "[GetScriptedGui(\'cmp_military_native_fleet_owner_probe\').IsShown({formation_scope})]" position = {{ 694 6 }} size = {{ 6 {max(16,height-12)} }} color = {{ 0.30 0.72 0.96 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes tooltip = "CMP_MIL_TARGET_FLEET_OWNER_PROBE_TT" }}')
    line(lines, 8, '}')
    line(lines, 7, '}')
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')



def render_military_operations_discovery(lines: list[str], profile: dict) -> None:
    """Read-only exact Army proof using the native selected MilitaryFormation.

    pre1.1 intentionally does not guess a Country.GetMilitaryFormationsArmy accessor.
    The user selects an Army in native Victoria 3 UI; CMP observes GetSelectedFormation,
    transports MilitaryFormation.MakeScope into read-only ScriptedGui probes and can reopen
    the exact native MilitaryFormation panel. No marker and no gameplay write is created.
    """
    font = profile["font_size"]
    height = profile["button_height"]
    formation_root = "GuiScope.SetRoot(MilitaryFormation.MakeScope).End"
    line(lines, 3, 'widget = { name = "cmp_workspace_operations_discovery" visible = "[GetVariableSystem.Exists(\'cmp_workspace_operations_discovery\')]" position = { 34 64 } size = { 792 438 }')
    line(lines, 4, 'icon = { size = { 792 438 } texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = { 0.035 0.045 0.065 0.998 } }')
    line(lines, 4, 'icon = { position = { 2 2 } size = { 788 434 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.98 } alwaystransparent = yes }')
    line(lines, 4, f'textbox = {{ position = {{ 20 14 }} size = {{ 680 34 }} maximumsize = {{ 680 34 }} fontsize = {font + 4} fontsize_min = 14 align = left text = "CMP_OPS_PRE1_1_TITLE" }}')
    line(lines, 4, 'close_button = { position = { 736 10 } size = { 42 42 } onclick = "[GetVariableSystem.Clear(\'cmp_workspace_operations_discovery\')]" }')
    line(lines, 4, f'textbox = {{ position = {{ 20 54 }} size = {{ 742 62 }} maximumsize = {{ 742 62 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_OPS_PRE1_1_DESC" }}')
    line(lines, 4, f'textbox = {{ visible = "[Not(GetSelectedFormation.IsArmy)]" position = {{ 20 128 }} size = {{ 752 44 }} maximumsize = {{ 752 44 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_OPS_PRE1_1_NO_ARMY" }}')
    line(lines, 4, 'widget = { visible = "[GetSelectedFormation.IsArmy]" datacontext = "[GetSelectedFormation]" position = { 20 128 } size = { 752 230 }')
    line(lines, 5, f'textbox = {{ size = {{ 530 40 }} maximumsize = {{ 530 40 }} fontsize = {font + 2} fontsize_min = 12 align = left|nobaseline elide = right text = "[MilitaryFormation.GetNameNoFormatting]" tooltip = "[MilitaryFormation.GetNameNoFormatting]" }}')
    button(lines, 5, x=548, y=0, width=204, height=height, label="CMP_OPS_PRE1_1_OPEN_NATIVE", font=font,
           action="InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')",
           tooltip="CMP_OPS_PRE1_1_OPEN_NATIVE_TT", color="0.45 0.62 0.82 0.97")
    line(lines, 5, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_ops_army_root_probe\').IsShown({formation_root})]" position = {{ 0 64 }} size = {{ 752 34 }} maximumsize = {{ 752 34 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_OPS_PRE1_1_ROOT_OK" }}')
    line(lines, 5, f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_ops_army_root_probe\').IsShown({formation_root}))]" position = {{ 0 64 }} size = {{ 752 34 }} maximumsize = {{ 752 34 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_OPS_PRE1_1_ROOT_BAD" }}')
    line(lines, 5, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_ops_army_owner_probe\').IsShown({formation_root})]" position = {{ 0 104 }} size = {{ 752 34 }} maximumsize = {{ 752 34 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_OPS_PRE1_1_OWNER_OK" }}')
    line(lines, 5, f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_ops_army_owner_probe\').IsShown({formation_root}))]" position = {{ 0 104 }} size = {{ 752 34 }} maximumsize = {{ 752 34 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_OPS_PRE1_1_OWNER_BAD" }}')
    line(lines, 5, f'textbox = {{ position = {{ 0 150 }} size = {{ 752 70 }} maximumsize = {{ 752 70 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_OPS_PRE1_1_LIMITS" }}')
    line(lines, 4, '}')
    line(lines, 4, f'textbox = {{ position = {{ 20 372 }} size = {{ 752 48 }} maximumsize = {{ 752 48 }} multiline = yes autoresize = no fontsize = {max(12,font-1)} fontsize_min = 12 align = left text = "CMP_OPS_PRE1_1_INVASION_MANUAL" }}')
    line(lines, 3, '}')

def render_army_creation_target_row(lines: list[str], indent: int, profile: dict, *, y: int) -> int:
    """Show that creation workflows target a marked state, not an existing army."""
    font = profile["font_size"]
    height = profile["button_height"]
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    button(lines, indent, x=0, y=y, width=286, height=height, label="CMP_MIL_ARMY_STATE_TARGET_OPEN", font=font,
           action="GetVariableSystem.Set('cmp_workspace_page', 'target')",
           tooltip="CMP_MIL_ARMY_STATE_TARGET_TT", color="0.45 0.62 0.82 0.97")
    line(lines, indent, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_army_builder_has_marked_state_check\').IsShown({scope})]" position = {{ 302 {y} }} size = {{ 498 {height} }} maximumsize = {{ 498 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_MIL_ARMY_STATE_TARGET_READY" }}')
    line(lines, indent, f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_army_builder_has_marked_state_check\').IsShown({scope}))]" position = {{ 302 {y} }} size = {{ 498 {height} }} maximumsize = {{ 498 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_MIL_ARMY_STATE_TARGET_NONE" }}')
    return y + height + 12


def render_effect_choices(lines: list[str], indent: int, profile: dict, *, y: int,
                          items: list[tuple[str, str, str | None]], columns: int,
                          tooltip: str, width: int = 800) -> int:
    font = profile["font_size"]
    height = profile["button_height"]
    gap = 8
    button_width = (width - gap * (columns - 1)) // columns
    for index, (label, effect, selected) in enumerate(items):
        row, col = divmod(index, columns)
        x = col * (button_width + gap)
        py = y + row * (height + gap)
        economy_action_button(lines, indent, x=x, y=py, width=button_width, height=height,
                              label=label, font=font, effect=effect, tooltip=tooltip,
                              selected=selected)
    return y + ((len(items) + columns - 1) // columns) * (height + gap)


def render_military_army_builder(lines: list[str], units: list[dict], profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    area_height = 514 - y
    visible = military_tab_visible("army_builder")
    line(lines, 3, f'widget = {{ visible = "{visible}" position = {{ 4 {y} }} size = {{ 840 {area_height} }}')
    line(lines, 4, f'textbox = {{ size = {{ 500 30 }} maximumsize = {{ 500 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_MIL_UNIT_PICKER" }}')
    button(lines, 4, x=746, y=0, width=54, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'army_builder')",
           tooltip="CMP_WS_MIL_HELP_ARMY_TT", color="0.48 0.58 0.72 0.98")
    categories = [
        ("CMP_ARMY_BUILDER_INFANTRY", "infantry", {"infantry", "marines"}),
        ("CMP_ARMY_BUILDER_ARTILLERY", "artillery", {"artillery"}),
        ("CMP_ARMY_BUILDER_CAVALRY", "mobile", {"mobile"}),
    ]
    gap = 7
    cat_width = (510 - gap * 2) // 3
    for index, (label, category, _) in enumerate(categories):
        x = index * (cat_width + gap)
        button(lines, 4, x=x, y=46, width=cat_width, height=height, label=label, font=font,
               action=f"GetVariableSystem.Set('cmp_workspace_army_category', '{category}')",
               tooltip="CMP_WS_MIL_CATEGORY_TT", color="0.40 0.53 0.68 0.97")
        line(lines, 4, f'icon = {{ visible = "{military_subtab_visible("cmp_workspace_army_category", category, "infantry")}" position = {{ {x + 4} {46 + height - 4} }} size = {{ {cat_width - 8} 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')
    scroll_y = 46 + height + 8
    scroll_height = area_height - scroll_y
    for _, category, roles in categories:
        category_units = [item for item in units if item["role"] in roles]
        content_height = max(scroll_height, ((len(category_units) + 1) // 2) * (height + 8) + 12)
        line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_military_army_picker_{category}_{profile["id"]}" visible = "{military_subtab_visible("cmp_workspace_army_category", category, "infantry")}" position = {{ 0 {scroll_y} }} size = {{ 510 {scroll_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
        line(lines, 5, 'scrollwidget = {')
        line(lines, 6, f'widget = {{ size = {{ 490 {content_height} }}')
        unit_width = (478 - 8) // 2
        for index, item in enumerate(category_units):
            row, col = divmod(index, 2)
            x = col * (unit_width + 8)
            py = row * (height + 8)
            unit_id = item["id"]
            loc = f"CMP_ARMY_UNIT_{unit_id.upper()}"
            tooltip = f"CMP_ARMY_UNIT_TT_{unit_id.upper()}"
            scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
            button(lines, 7, x=x, y=py, width=unit_width, height=height, label=loc, font=font,
                   action=f"GetScriptedGui('cmp_army_builder_select_{unit_id}').Execute({scope})",
                   enabled_when=f"[GetScriptedGui('cmp_army_builder_unit_{unit_id}_available').IsShown({scope})]",
                   tooltip=tooltip, elide=True)
            selected_line(lines, 7, x=x, y=py + height - 4, width=unit_width,
                          effect=f"cmp_army_builder_unit_{unit_id}_selected")
        line(lines, 6, '}')
        line(lines, 5, '}')
        line(lines, 4, '}')
    line(lines, 4, f'icon = {{ position = {{ 520 0 }} size = {{ 2 {area_height} }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = {{ 0.30 0.37 0.48 0.95 }} alwaystransparent = yes }}')
    line(lines, 4, f'textbox = {{ position = {{ 536 0 }} size = {{ 264 30 }} maximumsize = {{ 264 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_ARMY_BUILDER_AMOUNT" }}')
    amount_items = [(f"CMP_ARMY_AMOUNT_{value}", f"cmp_army_builder_select_amount_{value}", f"cmp_army_builder_amount_{value}_selected") for value in [1, 5, 10, 25, 50]]
    cursor_y = 38
    amount_width = (264 - 8 * 4) // 5
    for index, (label, effect, selected) in enumerate(amount_items):
        row, col = divmod(index, 5)
        economy_action_button(lines, 4, x=536 + col * (amount_width + 8), y=cursor_y + row * (height + 8),
                              width=amount_width, height=height, label=label, font=font,
                              effect=effect, tooltip="CMP_ARMY_BUILDER_AMOUNT_TT", selected=selected)
    cursor_y += height + 14
    for predicate, yes_key, no_key in [
        ("cmp_army_builder_has_marked_state_check", "CMP_MIL_ARMY_STATE_TARGET_READY", "CMP_MIL_ARMY_STATE_TARGET_NONE"),
        ("cmp_army_builder_has_unit_check", "CMP_ARMY_BUILDER_UNIT_OK", "CMP_ARMY_BUILDER_UNIT_BAD"),
        ("cmp_army_builder_has_amount_check", "CMP_ARMY_BUILDER_AMOUNT_OK", "CMP_ARMY_BUILDER_AMOUNT_BAD"),
    ]:
        scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
        line(lines, 4, f'textbox = {{ visible = "[GetScriptedGui(\'{predicate}\').IsShown({scope})]" position = {{ 536 {cursor_y} }} size = {{ 264 28 }} maximumsize = {{ 264 28 }} fontsize = {font} fontsize_min = 12 align = left text = "{yes_key}" }}')
        line(lines, 4, f'textbox = {{ visible = "[Not(GetScriptedGui(\'{predicate}\').IsShown({scope}))]" position = {{ 536 {cursor_y} }} size = {{ 264 28 }} maximumsize = {{ 264 28 }} fontsize = {font} fontsize_min = 12 align = left text = "{no_key}" }}')
        cursor_y += 30
    economy_action_button(lines, 4, x=536, y=cursor_y + 4, width=264, height=height,
                          label="CMP_ARMY_BUILDER_APPLY", font=font, effect="cmp_army_builder_apply",
                          tooltip="CMP_ARMY_BUILDER_APPLY_TT", color="0.38 0.68 0.44 0.96")
    economy_action_button(lines, 4, x=536, y=cursor_y + height + 12, width=264, height=height,
                          label="CMP_ARMY_BUILDER_CLEAR", font=font, effect="cmp_army_builder_clear",
                          tooltip="CMP_WS_MIL_RESET_TT", color="0.68 0.40 0.43 0.96")
    line(lines, 3, '}')


def render_military_army_templates(lines: list[str], profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    area_height = 514 - y
    variable = "cmp_workspace_army_template_tab"
    line(lines, 3, f'widget = {{ visible = "{military_tab_visible("army_templates")}" position = {{ 4 {y} }} size = {{ 840 {area_height} }}')
    tabs = [
        ("CMP_WS_MIL_SUB_QUICK", "quick", "CMP_WS_MIL_HELP_TEMPLATES_TT"),
        ("CMP_WS_MIL_SUB_MIXED", "mixed", "CMP_WS_MIL_HELP_TEMPLATES_TT"),
        ("CMP_WS_MIL_SUB_DESIGNER", "designer", "CMP_WS_MIL_HELP_TEMPLATES_TT"),
        ("CMP_WS_MIL_SUB_MARINES", "marines", "CMP_WS_MIL_HELP_MARINES_TT"),
    ]
    render_military_subtabs(lines, profile, y=0, variable=variable, tabs=tabs, default="quick")
    render_army_creation_target_row(lines, 4, profile, y=height + 8)
    content_y = height * 2 + 28
    content_height = area_height - content_y
    # Quick role presets
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_military_army_template_quick_{profile["id"]}" visible = "{military_subtab_visible(variable, "quick", "quick")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 800 430 }')
    line(lines, 7, f'textbox = {{ size = {{ 720 36 }} maximumsize = {{ 720 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_ARMY_BUILDER_QUICK_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'army_templates')",
           tooltip="CMP_WS_MIL_HELP_TEMPLATES_TT", color="0.48 0.58 0.72 0.98")
    quick = [
        ("CMP_ARMY_PRESET_INFANTRY", "cmp_army_builder_preset_infantry_corps", None),
        ("CMP_ARMY_PRESET_ARTILLERY", "cmp_army_builder_preset_artillery_group", None),
        ("CMP_ARMY_PRESET_MOBILE", "cmp_army_builder_preset_mobile_corps", None),
        ("CMP_ARMY_PRESET_MARINE", "cmp_army_builder_preset_marine_force", None),
    ]
    cursor_y = render_effect_choices(lines, 7, profile, y=50, items=quick, columns=2,
                                     tooltip="CMP_WS_MIL_QUICK_PRESET_TT")
    cursor_y += 12
    economy_action_button(lines, 7, x=0, y=cursor_y, width=396, height=height,
                          label="CMP_ARMY_BUILDER_APPLY", font=font, effect="cmp_army_builder_apply",
                          tooltip="CMP_ARMY_BUILDER_APPLY_TT", color="0.38 0.68 0.44 0.96")
    economy_action_button(lines, 7, x=404, y=cursor_y, width=396, height=height,
                          label="CMP_ARMY_BUILDER_CLEAR", font=font, effect="cmp_army_builder_clear",
                          tooltip="CMP_WS_MIL_RESET_TT", color="0.68 0.40 0.43 0.96")
    line(lines, 6, '}'); line(lines, 5, '}'); line(lines, 4, '}')
    # Mixed templates
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_military_army_template_mixed_{profile["id"]}" visible = "{military_subtab_visible(variable, "mixed", "quick")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 800 500 }')
    line(lines, 7, f'textbox = {{ size = {{ 720 36 }} maximumsize = {{ 720 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_ARMY_MIXED_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'army_templates')",
           tooltip="CMP_WS_MIL_HELP_TEMPLATES_TT", color="0.48 0.58 0.72 0.98")
    mixed = [
        ("CMP_ARMY_MIXED_BALANCED", "cmp_army_mixed_select_balanced", "cmp_army_mixed_balanced_selected"),
        ("CMP_ARMY_MIXED_INFANTRY", "cmp_army_mixed_select_infantry_heavy", "cmp_army_mixed_infantry_heavy_selected"),
        ("CMP_ARMY_MIXED_BREAKTHROUGH", "cmp_army_mixed_select_breakthrough", "cmp_army_mixed_breakthrough_selected"),
        ("CMP_ARMY_MIXED_ARMOR", "cmp_army_mixed_select_armored_fist", "cmp_army_mixed_armored_fist_selected"),
    ]
    cursor_y = render_effect_choices(lines, 7, profile, y=50, items=mixed, columns=2,
                                     tooltip="CMP_WS_MIL_MIXED_TT") + 12
    economy_action_button(lines, 7, x=0, y=cursor_y, width=396, height=height,
                          label="CMP_ARMY_MIXED_CREATE", font=font, effect="cmp_army_mixed_apply",
                          tooltip="CMP_ARMY_MIXED_CREATE_TT", color="0.38 0.68 0.44 0.96")
    economy_action_button(lines, 7, x=404, y=cursor_y, width=396, height=height,
                          label="CMP_ARMY_MIXED_CLEAR", font=font, effect="cmp_army_mixed_clear",
                          tooltip="CMP_WS_MIL_RESET_TT", color="0.68 0.40 0.43 0.96")
    line(lines, 6, '}'); line(lines, 5, '}'); line(lines, 4, '}')
    # Army designer
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_military_army_template_designer_{profile["id"]}" visible = "{military_subtab_visible(variable, "designer", "quick")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 800 690 }')
    line(lines, 7, f'textbox = {{ size = {{ 720 36 }} maximumsize = {{ 720 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_ARMY_DESIGNER_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'army_templates')",
           tooltip="CMP_WS_MIL_HELP_TEMPLATES_TT", color="0.48 0.58 0.72 0.98")
    cursor_y = 48
    groups = [
        ("CMP_ARMY_DESIGNER_SIZE", [(f"CMP_ARMY_DESIGNER_SIZE_{v}", f"cmp_army_designer_select_size_{v}", f"cmp_army_designer_size_{v}_selected") for v in [25, 50, 75, 100]], 4, "CMP_WS_MIL_DESIGNER_TT"),
        ("CMP_ARMY_DESIGNER_INF", [(f"CMP_ARMY_DESIGNER_INF_{v}", f"cmp_army_designer_select_inf_{v}", f"cmp_army_designer_inf_{v}_selected") for v in [40, 50, 60, 70]], 4, "CMP_WS_MIL_DESIGNER_TT"),
        ("CMP_ARMY_DESIGNER_ART", [(f"CMP_ARMY_DESIGNER_ART_{v}", f"cmp_army_designer_select_art_{v}", f"cmp_army_designer_art_{v}_selected") for v in [10, 20, 30]], 3, "CMP_WS_MIL_DESIGNER_TT"),
    ]
    for title, items, columns, tooltip in groups:
        line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "{title}" }}')
        cursor_y = render_effect_choices(lines, 7, profile, y=cursor_y + 32, items=items, columns=columns, tooltip=tooltip) + 10
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 40 }} maximumsize = {{ 800 40 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_MIL_MOBILE_REMAINDER" }}')
    cursor_y += 46
    economy_action_button(lines, 7, x=0, y=cursor_y, width=396, height=height,
                          label="CMP_ARMY_DESIGNER_CREATE", font=font, effect="cmp_army_designer_apply",
                          tooltip="CMP_ARMY_DESIGNER_CREATE_TT", color="0.38 0.68 0.44 0.96")
    economy_action_button(lines, 7, x=404, y=cursor_y, width=396, height=height,
                          label="CMP_ARMY_DESIGNER_CLEAR", font=font, effect="cmp_army_designer_clear",
                          tooltip="CMP_WS_MIL_RESET_TT", color="0.68 0.40 0.43 0.96")
    line(lines, 6, '}'); line(lines, 5, '}'); line(lines, 4, '}')
    # Marines
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_military_army_template_marines_{profile["id"]}" visible = "{military_subtab_visible(variable, "marines", "quick")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 800 520 }')
    line(lines, 7, f'textbox = {{ size = {{ 720 36 }} maximumsize = {{ 720 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_ARMY_AMPH_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'marines')",
           tooltip="CMP_WS_MIL_HELP_MARINES_TT", color="0.48 0.58 0.72 0.98")
    marine_items = [(f"CMP_ARMY_AMPH_AMOUNT_{v}", f"cmp_army_amphib_select_amount_{v}", f"cmp_army_amphib_amount_{v}_selected") for v in [5, 10, 25, 50]]
    cursor_y = render_effect_choices(lines, 7, profile, y=52, items=marine_items, columns=4,
                                     tooltip="CMP_WS_MIL_MARINE_AMOUNT_TT") + 10
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    for predicate, yes_key, no_key in [
        ("cmp_army_amphib_tech_ready", "CMP_ARMY_AMPH_TECH_OK", "CMP_ARMY_AMPH_TECH_NO"),
        ("cmp_army_amphib_port_ready", "CMP_ARMY_AMPH_PORT_OK", "CMP_ARMY_AMPH_PORT_NO"),
    ]:
        line(lines, 7, f'textbox = {{ visible = "[GetScriptedGui(\'{predicate}\').IsShown({scope})]" position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "{yes_key}" }}')
        line(lines, 7, f'textbox = {{ visible = "[Not(GetScriptedGui(\'{predicate}\').IsShown({scope}))]" position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "{no_key}" }}')
        cursor_y += 30
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y + 2} }} size = {{ 800 44 }} maximumsize = {{ 800 44 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_MIL_MANUAL_ATTACH_WARNING" }}')
    cursor_y += 54
    economy_action_button(lines, 7, x=0, y=cursor_y, width=396, height=height,
                          label="CMP_ARMY_AMPH_CREATE", font=font, effect="cmp_army_amphib_apply",
                          tooltip="CMP_ARMY_AMPH_CREATE_TT", color="0.38 0.68 0.44 0.96")
    economy_action_button(lines, 7, x=404, y=cursor_y, width=396, height=height,
                          label="CMP_ARMY_AMPH_CLEAR", font=font, effect="cmp_army_amphib_clear",
                          tooltip="CMP_WS_MIL_RESET_TT", color="0.68 0.40 0.43 0.96")
    line(lines, 6, '}'); line(lines, 5, '}'); line(lines, 4, '}')
    line(lines, 3, '}')


def render_military_army_controls(lines: list[str], profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    area_height = 514 - y
    line(lines, 3, f'widget = {{ visible = "{military_tab_visible("army_controls")}" position = {{ 4 {y} }} size = {{ 840 {area_height} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_military_army_controls_{profile["id"]}" size = {{ 840 {area_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 820 1040 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 36 }} maximumsize = {{ 730 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_ARMY_CONTROL_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'army_controls')",
           tooltip="CMP_WS_MIL_HELP_CONTROLS_TT", color="0.48 0.58 0.72 0.98")
    cursor_y = 48
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_ARMY_CONTROL_TARGET_TITLE" }}')
    cursor_y += 32
    targets = [
        ("CMP_ARMY_CONTROL_TARGET_SELF", "cmp_army_controls_select_target_self", "cmp_army_controls_target_self_selected"),
        ("CMP_ARMY_CONTROL_TARGET_MARKED", "cmp_army_controls_select_target_marked", "cmp_army_controls_target_marked_selected"),
    ]
    cursor_y = render_effect_choices(lines, 7, profile, y=cursor_y, items=targets, columns=2,
                                     tooltip="CMP_WS_MIL_CONTROL_TARGET_TT") + 10
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    line(lines, 7, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_army_controls_has_marked_country\').IsShown({scope})]" position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_MIL_MARKED_COUNTRY_OK" }}')
    line(lines, 7, f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_army_controls_has_marked_country\').IsShown({scope}))]" position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_MIL_MARKED_COUNTRY_NONE" }}')
    cursor_y += 36
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_ARMY_CONTROL_PARAM_TITLE" }}')
    cursor_y += 32
    params = [
        "offense", "defense", "morale_recovery", "mobilization", "experience",
        "movement", "supply", "goods_cost", "wages", "war_exhaustion",
    ]
    param_items = [(f"CMP_ARMY_CONTROL_PARAM_{item.upper()}", f"cmp_army_controls_select_parameter_{item}", f"cmp_army_controls_parameter_{item}_selected") for item in params]
    cursor_y = render_effect_choices(lines, 7, profile, y=cursor_y, items=param_items, columns=2,
                                     tooltip="CMP_WS_MIL_CONTROL_PARAM_TT") + 10
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_ARMY_CONTROL_VALUE_TITLE" }}')
    cursor_y += 32
    values = [(f"CMP_WS_MIL_CONTROL_VALUE_{i}", f"cmp_army_controls_select_value_{i}", f"cmp_army_controls_value_{i}_selected") for i in range(1, 6)]
    cursor_y = render_effect_choices(lines, 7, profile, y=cursor_y, items=values, columns=5,
                                     tooltip="CMP_WS_MIL_CONTROL_VALUE_TT") + 10
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_ARMY_CONTROL_PRESETS_TITLE" }}')
    cursor_y += 32
    presets = [
        ("CMP_ARMY_CONTROL_PRESET_BALANCED", "cmp_army_controls_preset_balanced", None),
        ("CMP_ARMY_CONTROL_PRESET_RAPID", "cmp_army_controls_preset_rapid", None),
        ("CMP_ARMY_CONTROL_PRESET_ECONOMY", "cmp_army_controls_preset_economy", None),
        ("CMP_ARMY_CONTROL_PRESET_GOD", "cmp_army_controls_preset_god", None),
    ]
    cursor_y = render_effect_choices(lines, 7, profile, y=cursor_y, items=presets, columns=2,
                                     tooltip="CMP_WS_MIL_CONTROL_PRESET_TT") + 12
    actions = [
        ("CMP_ARMY_CONTROL_APPLY", "cmp_army_controls_apply", "0.38 0.68 0.44 0.96"),
        ("CMP_ARMY_CONTROL_RESET_PARAM", "cmp_army_controls_reset_parameter", "0.68 0.46 0.36 0.96"),
        ("CMP_ARMY_CONTROL_RESET_ALL", "cmp_army_controls_reset_all", "0.72 0.38 0.42 0.96"),
    ]
    action_width = (800 - 16) // 3
    for index, (label, effect, color) in enumerate(actions):
        economy_action_button(lines, 7, x=index * (action_width + 8), y=cursor_y,
                              width=action_width, height=height, label=label, font=font,
                              effect=effect, tooltip="CMP_WS_MIL_CONTROL_ACTION_TT", color=color)
    line(lines, 6, '}'); line(lines, 5, '}'); line(lines, 4, '}'); line(lines, 3, '}')


def render_fleet_creation_target_row(lines: list[str], indent: int, profile: dict, *, y: int) -> int:
    """Show the marked owned port used as HQ context for a NEW fleet."""
    font = profile["font_size"]
    height = profile["button_height"]
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    button(lines, indent, x=0, y=y, width=286, height=height, label="CMP_NAVY18_PORT_OPEN", font=font,
           action="GetVariableSystem.Set('cmp_workspace_page', 'target')",
           tooltip="CMP_NAVY18_PORT_TT", color="0.45 0.62 0.82 0.97")
    line(lines, indent, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_has_marked_port_state\').IsShown({scope})]" position = {{ 302 {y} }} size = {{ 498 {height} }} maximumsize = {{ 498 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_NAVY18_PORT_READY" }}')
    line(lines, indent, f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_navy18_has_marked_port_state\').IsShown({scope}))]" position = {{ 302 {y} }} size = {{ 498 {height} }} maximumsize = {{ 498 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_NAVY18_PORT_NONE" }}')
    return y + height + 12


def render_military_fleet_builder(lines: list[str], ships: list[dict], fleet: dict, navy18: dict,
                                  profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    area_height = 514 - y
    variable = "cmp_workspace_fleet_builder_mode"
    catalog = json.loads(NAVAL_CATALOG_REGISTRY.read_text(encoding="utf-8"))
    line(lines, 3, f'widget = {{ visible = "{military_tab_visible("fleet_builder")}" position = {{ 4 {y} }} size = {{ 840 {area_height} }}')
    tabs = [
        ("CMP_NAVY18_MODE_CATALOG", "catalog", "CMP_NAVY18_CATALOG_DESC"),
        ("CMP_NAVY18_MODE_COMPOSER", "new", "CMP_NAVY18_CREATE_TT"),
        ("CMP_NAVY18_MODE_EXISTING", "existing", "CMP_NAVY18_EXISTING_DESC"),
        ("CMP_NAVY18_MODE_SHIPCTRL", "shipctrl", "CMP_NAVY18_SHIPCTRL_DESC"),
        ("CMP_NAVY18_MODE_TRANSFER", "transfer", "CMP_NAVY18_TRANSFER_DESC"),
        ("CMP_NAVY18_MODE_LOGISTICS", "logistics", "CMP_NAVY18_LOGISTICS_DESC"),
    ]
    render_military_subtabs(lines, profile, y=0, variable=variable, tabs=tabs, default="catalog")
    content_y = height + 10
    content_height = area_height - content_y
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"

    # beta18-pre2: full 1.13 hull catalog + native Ship Designer bridge.
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_navy18_catalog_{profile["id"]}" visible = "{military_subtab_visible(variable, "catalog", "catalog")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 800 2300 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 36 }} maximumsize = {{ 730 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_NAVY18_CATALOG_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'fleet_builder')",
           tooltip="CMP_WS_MIL_HELP_FLEET_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 42 }} size = {{ 800 56 }} maximumsize = {{ 800 56 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_CATALOG_DESC" }}')
    cursor_y = render_fleet_creation_target_row(lines, 7, profile, y=104)
    # Directly mirror the proven vanilla panel_military.gui entry point. Template writes stay inside native UI.
    button(lines, 7, x=0, y=cursor_y, width=800, height=height, label="CMP_NAVY18_CATALOG_DESIGNER", font=font,
           action="PopupManager.ToggleShipDesignerPopup", enabled_when="[HasDlcFeature('ship_designer')]",
           tooltip="CMP_NAVY18_CATALOG_DESIGNER_TT", color="0.48 0.58 0.72 0.98")
    cursor_y += height + 8
    line(lines, 7, f'textbox = {{ visible = "[Not(HasDlcFeature(\'ship_designer\'))]" position = {{ 0 {cursor_y} }} size = {{ 800 38 }} maximumsize = {{ 800 38 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_CATALOG_NO_DLC" }}')
    cursor_y += 44
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_NAVY18_CATALOG_GROUPS" }}')
    cursor_y += 32
    categories=[('CMP_NAVY18_CAT_ALL','all'),('CMP_NAVY18_CAT_CAPITAL','capital'),('CMP_NAVY18_CAT_CRUISER','cruiser'),('CMP_NAVY18_CAT_TORPEDO','torpedo'),('CMP_NAVY18_CAT_TECH_RES','tech_res')]
    gap=6; bw=(800-gap*(len(categories)-1))//len(categories)
    for i,(label,val) in enumerate(categories):
        x=i*(bw+gap)
        button(lines,7,x=x,y=cursor_y,width=bw,height=height,label=label,font=font,
               action=f"GetVariableSystem.Set('cmp_workspace_navy_catalog_category', '{val}')",
               tooltip="CMP_NAVY18_CATALOG_GROUPS",color="0.42 0.50 0.62 0.98")
        variable_selected_line(lines,7,x=x,y=cursor_y+height-4,width=bw,variable='cmp_workspace_navy_catalog_category',value=val,default=(val=='all'))
    cursor_y += height + 8
    # Obsolete toggle: actual vanilla ShipType.IsObsolete is evaluated at runtime. T&R late hulls remain visible.
    button(lines,7,x=0,y=cursor_y,width=396,height=height,label="CMP_NAVY18_SHOW_OBSOLETE",font=font,
           action="GetVariableSystem.Set('cmp_workspace_navy_show_obsolete', 'yes')",tooltip="CMP_NAVY18_SHOW_OBSOLETE_TT",
           enabled_when="[Not(GetVariableSystem.Exists('cmp_workspace_navy_show_obsolete'))]")
    button(lines,7,x=404,y=cursor_y,width=396,height=height,label="CMP_NAVY18_HIDE_OBSOLETE",font=font,
           action="GetVariableSystem.Clear('cmp_workspace_navy_show_obsolete')",tooltip="CMP_NAVY18_SHOW_OBSOLETE_TT",
           enabled_when="[GetVariableSystem.Exists('cmp_workspace_navy_show_obsolete')]")
    cursor_y += height + 10
    line(lines,7,f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 42 }} maximumsize = {{ 800 42 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_CATALOG_DEFAULT_TEMPLATE" }}')
    cursor_y += 48

    for hull in catalog['combat_hulls']:
        sid=hull['id']; key=f"CMP_NAVY18_HULL_{sid.upper()}"; tt=f"CMP_NAVY18_HULL_{sid.upper()}_TT"
        group=hull['group']; provider=hull['provider']; stype=hull['ship_type']
        category_expr=(f"Or(Not(GetVariableSystem.Exists('cmp_workspace_navy_catalog_category')), GetVariableSystem.HasValue('cmp_workspace_navy_catalog_category', 'all'), "
                       f"GetVariableSystem.HasValue('cmp_workspace_navy_catalog_category', '{group}')" +
                       (", GetVariableSystem.HasValue('cmp_workspace_navy_catalog_category', 'tech_res')" if provider=='tech_res' else "") + ")")
        if provider=='vanilla':
            obsolete_expr=f"Or(GetVariableSystem.Exists('cmp_workspace_navy_show_obsolete'), Not(GetShipType('{stype}').IsObsolete(GetPlayer)))"
            visible=f"[And({category_expr}, {obsolete_expr})]"
        else:
            visible=f"[{category_expr}]"
        line(lines,7,f'widget = {{ visible = "{visible}" position = {{ 0 {cursor_y} }} size = {{ 800 {height} }}')
        line(lines,8,f'textbox = {{ position = {{ 0 6 }} size = {{ 286 {height-8} }} maximumsize = {{ 286 {height-8} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline elide = right text = "{key}" tooltip = "{tt}" }}')
        amounts=catalog['catalog_amounts']; agap=5; abw=(500-agap*(len(amounts)-1))//len(amounts)
        for i,n in enumerate(amounts):
            economy_action_button(lines,8,x=300+i*(abw+agap),y=0,width=abw,height=height,label=f"CMP_NAVY18_CATALOG_COUNT_{n}",font=font,
                                  effect=f"cmp_navy18_catalog_create_{sid}_{n}",tooltip=tt)
        line(lines,7,'}')
        cursor_y += height + 6
    line(lines,7,f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_TITLE" }}')
    cursor_y += 30
    line(lines,7,f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 46 }} maximumsize = {{ 800 46 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_READONLY" tooltip = "CMP_NAVY18_HULL_SUPPLY_SHIP_TT" }}')
    line(lines,6,'}'); line(lines,5,'}'); line(lines,4,'}')

    # beta18-pre3 Fleet Composer 2.0: five arbitrary hull rows, one exact new fleet.
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_navy18_new_{profile["id"]}" visible = "{military_subtab_visible(variable, "new", "catalog")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 800 1450 }')
    by_hull = {h['id']: h for h in catalog['combat_hulls']}
    all_hulls = catalog['combat_hulls']
    amounts = navy18['composer2']['amounts']
    rows = range(1, navy18['composer2']['rows'] + 1)

    # Main composition surface. Hull selection opens a row-local picker without touching gameplay state.
    line(lines, 7, 'widget = { visible = "[Not(GetVariableSystem.Exists(\'cmp_workspace_navy_comp2_picker_row\'))]" position = { 0 0 } size = { 800 1450 }')
    line(lines, 8, f'textbox = {{ size = {{ 730 36 }} maximumsize = {{ 730 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_NAVY18_NEW_TITLE" }}')
    button(lines, 8, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'fleet_builder')",
           tooltip="CMP_WS_MIL_HELP_FLEET_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 8, f'textbox = {{ position = {{ 0 42 }} size = {{ 800 58 }} maximumsize = {{ 800 58 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_NEW_DESC" }}')
    cursor_y = render_fleet_creation_target_row(lines, 8, profile, y=106)
    line(lines, 8, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 42 }} maximumsize = {{ 800 42 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_INSTANT_DEFAULT_NOTE" }}')
    cursor_y += 48
    line(lines, 8, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_NAVY18_COMPOSITION" }}')
    cursor_y += 34

    for r in rows:
        line(lines, 8, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 180 28 }} maximumsize = {{ 180 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_NAVY18_COMP2_ROW_{r}" }}')
        cursor_y += 30
        button(lines, 8, x=0, y=cursor_y, width=300, height=height, label="CMP_NAVY18_COMP2_SELECT_HULL", font=font,
               action=f"GetVariableSystem.Set('cmp_workspace_navy_comp2_picker_row', '{r}')",
               tooltip="CMP_NAVY18_COMP2_PICK_DESC", color="0.42 0.50 0.62 0.98")
        # Selected hull name is read directly from country composer variables through ScriptedGui state.
        line(lines, 8, f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_navy18_comp2_row_{r}_has_hull\').IsShown({scope}))]" position = {{ 312 {cursor_y + 7} }} size = {{ 488 {height - 10} }} maximumsize = {{ 488 {height - 10} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline elide = right text = "CMP_NAVY18_COMP2_NO_HULL" }}')
        for h in all_hulls:
            hid=h['id']; key=f"CMP_NAVY18_HULL_{hid.upper()}"; tt=f"CMP_NAVY18_HULL_{hid.upper()}_TT"
            line(lines, 8, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_comp2_row_{r}_hull_{hid}_selected\').IsShown({scope})]" position = {{ 312 {cursor_y + 7} }} size = {{ 488 {height - 10} }} maximumsize = {{ 488 {height - 10} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline elide = right text = "{key}" tooltip = "{tt}" }}')
        cursor_y += height + 5
        line(lines, 8, f'textbox = {{ position = {{ 0 {cursor_y + 8} }} size = {{ 176 {height - 8} }} maximumsize = {{ 176 {height - 8} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_NAVY18_GROUP_COUNT" }}')
        gap=6; bw=(614-gap*(len(amounts)-1))//len(amounts)
        for i,a in enumerate(amounts):
            x=186+i*(bw+gap)
            economy_action_button(lines,8,x=x,y=cursor_y,width=bw,height=height,label=f"CMP_NAVY18_COUNT_{a}",font=font,
                                  effect=f"cmp_navy18_comp2_select_row_{r}_count_{a}",tooltip=f"CMP_NAVY18_COMP2_ROW_{r}",selected=f"cmp_navy18_comp2_row_{r}_count_{a}_selected")
        cursor_y += height + 10

    line(lines, 8, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 32 }} maximumsize = {{ 800 32 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_COMP2_DUPLICATES" }}')
    cursor_y += 36
    line(lines, 8, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_comp2_ready\').IsShown({scope})]" position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_COMP2_READY" }}')
    line(lines, 8, f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_navy18_comp2_ready\').IsShown({scope}))]" position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_COMP2_BAD" }}')
    cursor_y += 34
    economy_action_button(lines,8,x=0,y=cursor_y,width=396,height=height,label="CMP_NAVY18_CREATE",font=font,effect="cmp_navy18_comp2_create_fleet",tooltip="CMP_NAVY18_CREATE_TT",color="0.38 0.68 0.44 0.96")
    economy_action_button(lines,8,x=404,y=cursor_y,width=396,height=height,label="CMP_NAVY18_CLEAR",font=font,effect="cmp_navy18_comp2_clear",tooltip="CMP_WS_MIL_RESET_TT",color="0.68 0.40 0.43 0.96")
    cursor_y += height + 14
    line(lines,8,f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_NAVY18_PRESETS" }}'); cursor_y += 32
    preset_items=[(p["loc_key"],f"cmp_navy18_preset_{p['id']}",None) for p in navy18['presets']]
    cursor_y=render_effect_choices(lines,8,profile,y=cursor_y,items=preset_items,columns=2,tooltip="CMP_NAVY18_PRESET_TT")+10
    line(lines, 7, '}')

    # Row-local hull picker. All 25 combat hulls are visible; unavailable technologies/providers are disabled.
    for r in rows:
        line(lines, 7, f'widget = {{ visible = "[GetVariableSystem.HasValue(\'cmp_workspace_navy_comp2_picker_row\', \'{r}\')]" position = {{ 0 0 }} size = {{ 800 1040 }}')
        line(lines, 8, f'textbox = {{ size = {{ 600 36 }} maximumsize = {{ 600 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_NAVY18_COMP2_PICK_TITLE" }}')
        line(lines, 8, f'textbox = {{ position = {{ 610 5 }} size = {{ 180 30 }} maximumsize = {{ 180 30 }} fontsize = {font + 1} fontsize_min = 12 align = right text = "CMP_NAVY18_COMP2_ROW_{r}" }}')
        line(lines, 8, f'textbox = {{ position = {{ 0 42 }} size = {{ 800 52 }} maximumsize = {{ 800 52 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_COMP2_PICK_DESC" }}')
        button(lines,8,x=0,y=100,width=800,height=height,label="CMP_NAVY18_COMP2_BACK",font=font,
               action="GetVariableSystem.Clear('cmp_workspace_navy_comp2_picker_row')",tooltip="CMP_NAVY18_COMP2_BACK",color="0.48 0.58 0.72 0.98")
        py0=100+height+12; hw=(800-8)//2
        for j,h in enumerate(all_hulls):
            hid=h['id']; row,col=divmod(j,2); x=col*(hw+8); py=py0+row*(height+7)
            key=f"CMP_NAVY18_HULL_{hid.upper()}"; tt=f"CMP_NAVY18_HULL_{hid.upper()}_TT"
            button(lines,8,x=x,y=py,width=hw,height=height,label=key,font=font,
                   actions=[f"GetScriptedGui('cmp_navy18_comp2_select_row_{r}_hull_{hid}').Execute({scope})", "GetVariableSystem.Clear('cmp_workspace_navy_comp2_picker_row')"],
                   enabled_when=f"[GetScriptedGui('cmp_navy18_comp2_hull_{hid}_available').IsShown({scope})]",tooltip=tt,elide=True)
            selected_line(lines,8,x=x,y=py+height-4,width=hw,effect=f"cmp_navy18_comp2_row_{r}_hull_{hid}_selected")
        line(lines, 7, '}')

    line(lines,6,'}'); line(lines,5,'}'); line(lines,4,'}')

    # Existing fleet compatibility path from beta17: exact selector + add ships.
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_navy18_existing_{profile["id"]}" visible = "{military_subtab_visible(variable, "existing", "catalog")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 800 1450 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 36 }} maximumsize = {{ 730 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_FLEET_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'fleet_builder')",
           tooltip="CMP_WS_MIL_HELP_FLEET_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 42 }} size = {{ 800 48 }} maximumsize = {{ 800 48 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_EXISTING_DESC" }}')
    cursor_y = render_fleet_target_row(lines, 7, profile, y=96) + 6
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_FLEET_SHIP_TITLE" }}')
    cursor_y += 34
    ship_width = (800 - 8) // 2
    for index, item in enumerate(ships):
        row, col = divmod(index, 2); x = col * (ship_width + 8); py = cursor_y + row * (height + 8); ship_id=item["id"]
        button(lines, 7, x=x, y=py, width=ship_width, height=height, label=item["loc_key"], font=font,
               action=f"GetScriptedGui('cmp_fleet_builder_select_{ship_id}').Execute({scope})",
               enabled_when=f"[GetScriptedGui('cmp_fleet_builder_ship_{ship_id}_available').IsShown({scope})]",
               tooltip=item["loc_key"], elide=True)
        selected_line(lines, 7, x=x, y=py + height - 4, width=ship_width, effect=f"cmp_fleet_builder_ship_{ship_id}_selected")
    cursor_y += ((len(ships)+1)//2)*(height+8)+8
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_FLEET_AMOUNT_TITLE" }}'); cursor_y += 34
    amount_items=[(f"CMP_FLEET_AMOUNT_{item['value']}",f"cmp_fleet_builder_select_amount_{item['value']}",f"cmp_fleet_builder_amount_{item['value']}_selected") for item in fleet["amounts"]]
    cursor_y=render_effect_choices(lines,7,profile,y=cursor_y,items=amount_items,columns=4,tooltip="CMP_WS_MIL_FLEET_AMOUNT_TT")+10
    line(lines,7,f'widget = {{ visible = "[GetSelectedFormation.IsFleet]" datacontext = "[GetSelectedFormation]" position = {{ 0 {cursor_y} }} size = {{ 396 {height} }}')
    button(lines,8,x=0,y=0,width=396,height=height,label="CMP_FLEET_APPLY",font=font,
           action="GetScriptedGui('cmp_fleet_builder_apply_native').Execute(GuiScope.SetRoot(MilitaryFormation.MakeScope).End)",
           enabled_when="[GetScriptedGui('cmp_fleet_builder_apply_native').IsValid(GuiScope.SetRoot(MilitaryFormation.MakeScope).End)]",
           tooltip="CMP_FLEET_APPLY_NATIVE_TT",color="0.38 0.68 0.44 0.96")
    line(lines,7,'}')
    line(lines,7,f'widget = {{ visible = "[Not(GetSelectedFormation.IsFleet)]" position = {{ 0 {cursor_y} }} size = {{ 396 {height} }}')
    button(lines,8,x=0,y=0,width=396,height=height,label="CMP_FLEET_APPLY",font=font,
           enabled=False, tooltip="CMP_FLEET_APPLY_NATIVE_NO_TARGET_TT",color="0.32 0.34 0.38 0.90")
    line(lines,7,'}')
    economy_action_button(lines,7,x=404,y=cursor_y,width=396,height=height,label="CMP_FLEET_CLEAR",font=font,effect="cmp_fleet_builder_clear",tooltip="CMP_WS_MIL_RESET_TT",color="0.68 0.40 0.43 0.96")
    line(lines,6,'}'); line(lines,5,'}'); line(lines,4,'}')

    # beta18-pre4 Exact Ship Control. Fleet source remains Victoria-native; only the selected ship gets a CMP marker.
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_navy18_shipctrl_{profile["id"]}" visible = "{military_subtab_visible(variable, "shipctrl", "catalog")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 800 1320 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 36 }} maximumsize = {{ 730 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_NAVY18_SHIPCTRL_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'fleet_builder')",
           tooltip="CMP_WS_MIL_HELP_FLEET_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 42 }} size = {{ 800 56 }} maximumsize = {{ 800 56 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_DESC" }}')
    cursor_y = render_fleet_target_row(lines, 7, profile, y=104) + 2
    line(lines, 7, f'textbox = {{ visible = "[Not(GetSelectedFormation.IsFleet)]" position = {{ 0 {cursor_y} }} size = {{ 800 40 }} maximumsize = {{ 800 40 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_SELECT_FLEET_FIRST" }}')
    line(lines, 7, f'widget = {{ visible = "[GetSelectedFormation.IsFleet]" datacontext = "[GetSelectedFormation]" position = {{ 0 {cursor_y} }} size = {{ 800 1100 }}')
    formation_root = "GuiScope.SetRoot(MilitaryFormation.MakeScope).End"
    line(lines, 8, f'textbox = {{ size = {{ 800 44 }} maximumsize = {{ 800 44 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_ORDER_NOTE" }}')
    ship_y = 50
    line(lines, 8, f'textbox = {{ position = {{ 0 {ship_y + 8} }} size = {{ 170 {height - 8} }} maximumsize = {{ 170 {height - 8} }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_PAGE" }}')
    page_count = navy18['ship_control']['max_slots'] // navy18['ship_control']['page_size']
    page_w = (620 - 6 * (page_count - 1)) // page_count
    for page in range(1, page_count + 1):
        x = 180 + (page - 1) * (page_w + 6)
        button(lines, 8, x=x, y=ship_y, width=page_w, height=height, label=f"CMP_NAVY18_SHIPCTRL_PAGE_{page}", font=font,
               action=f"GetVariableSystem.Set('cmp_workspace_navy_ship_page', '{page}')", tooltip="CMP_NAVY18_SHIPCTRL_PAGE")
        variable_selected_line(lines, 8, x=x, y=ship_y + height - 4, width=page_w,
                               variable='cmp_workspace_navy_ship_page', value=str(page), default=(page == 1))
    ship_y += height + 12
    slot_gap = 6; slot_cols = 5; slot_w = (800 - slot_gap * (slot_cols - 1)) // slot_cols
    for page in range(1, page_count + 1):
        vis = (f"[Or(Not(GetVariableSystem.Exists('cmp_workspace_navy_ship_page')), GetVariableSystem.HasValue('cmp_workspace_navy_ship_page', '1'))]" if page == 1 else f"[GetVariableSystem.HasValue('cmp_workspace_navy_ship_page', '{page}')]" )
        line(lines, 8, f'widget = {{ visible = "{vis}" position = {{ 0 {ship_y} }} size = {{ 800 {4 * (height + 7)} }}')
        start=(page-1)*20+1
        for offset in range(20):
            n=start+offset; row,col=divmod(offset,slot_cols); x=col*(slot_w+slot_gap); py=row*(height+7)
            button(lines, 9, x=x, y=py, width=slot_w, height=height, label=f"CMP_NAVY18_SHIPCTRL_SLOT_{n}", font=font,
                   action=f"GetScriptedGui('cmp_navy18_shipctrl_select_slot_{n}').Execute({formation_root})",
                   enabled_when=f"[GetScriptedGui('cmp_navy18_shipctrl_select_slot_{n}').IsValid({formation_root})]",
                   tooltip="CMP_NAVY18_SHIPCTRL_SLOT_TT")
            line(lines, 9, f'icon = {{ visible = "[GetScriptedGui(\'cmp_navy18_shipctrl_slot_{n}_selected\').IsShown({formation_root})]" position = {{ {x+3} {py+height-4} }} size = {{ {slot_w-6} 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')
        line(lines,8,'}')
    ship_y += 4 * (height + 7) + 10
    line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_shipctrl_has_ship\').IsShown({formation_root})]" position = {{ 0 {ship_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font+1} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_SELECTED" }}')
    line(lines,8,f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_navy18_shipctrl_has_ship\').IsShown({formation_root}))]" position = {{ 0 {ship_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font+1} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_NONE" }}')
    line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_shipctrl_target_lost\').IsShown({formation_root})]" position = {{ 0 {ship_y+28} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_LOST" }}')
    ship_y += 62
    line(lines,8,f'textbox = {{ position = {{ 0 {ship_y} }} size = {{ 90 28 }} maximumsize = {{ 90 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_TYPE" }}')
    for h in catalog['combat_hulls']:
        line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_shipctrl_type_{h["id"]}\').IsShown({formation_root})]" position = {{ 94 {ship_y} }} size = {{ 706 28 }} maximumsize = {{ 706 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_HULL_{h["id"].upper()}" }}')
    ship_y += 36
    # Status matrix, all based on the exact Ship marker.
    status_rows=[
        ('cmp_navy18_shipctrl_flagship','CMP_NAVY18_SHIPCTRL_FLAGSHIP','cmp_navy18_shipctrl_not_flagship','CMP_NAVY18_SHIPCTRL_NOT_FLAGSHIP'),
        ('cmp_navy18_shipctrl_damaged','CMP_NAVY18_SHIPCTRL_DAMAGED','cmp_navy18_shipctrl_healthy','CMP_NAVY18_SHIPCTRL_HEALTHY'),
        ('cmp_navy18_shipctrl_in_port','CMP_NAVY18_SHIPCTRL_IN_PORT','cmp_navy18_shipctrl_at_sea','CMP_NAVY18_SHIPCTRL_AT_SEA'),
        ('cmp_navy18_shipctrl_in_battle','CMP_NAVY18_SHIPCTRL_IN_BATTLE','cmp_navy18_shipctrl_not_in_battle','CMP_NAVY18_SHIPCTRL_NOT_IN_BATTLE'),
    ]
    for left_ep,left_key,right_ep,right_key in status_rows:
        line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'{left_ep}\').IsShown({formation_root})]" position = {{ 0 {ship_y} }} size = {{ 396 28 }} maximumsize = {{ 396 28 }} fontsize = {font} fontsize_min = 12 align = left text = "{left_key}" }}')
        line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'{right_ep}\').IsShown({formation_root})]" position = {{ 404 {ship_y} }} size = {{ 396 28 }} maximumsize = {{ 396 28 }} fontsize = {font} fontsize_min = 12 align = left text = "{right_key}" }}')
        ship_y += 30
    for prefix,keyprefix in [('hp','HP'),('crew','CREW')]:
        for state,suffix in [('excellent','EXCELLENT'),('worn','WORN'),('critical','CRITICAL'),('near_loss','NEAR_LOSS')]:
            line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_shipctrl_{prefix}_{state}\').IsShown({formation_root})]" position = {{ 0 {ship_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_{keyprefix}_{suffix}" }}')
        ship_y += 30
    line(lines,8,f'textbox = {{ position = {{ 0 {ship_y} }} size = {{ 800 40 }} maximumsize = {{ 800 40 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_SCOPE_NOTE" }}')
    ship_y += 48
    button(lines,8,x=0,y=ship_y,width=258,height=height,label="CMP_NAVY18_SHIPCTRL_SET_FLAGSHIP",font=font,
           action=f"GetScriptedGui('cmp_navy18_shipctrl_set_flagship').Execute({formation_root})",
           enabled_when=f"[GetScriptedGui('cmp_navy18_shipctrl_set_flagship').IsValid({formation_root})]",
           tooltip="CMP_NAVY18_SHIPCTRL_FLAGSHIP_TT",color="0.38 0.68 0.44 0.96")
    button(lines,8,x=271,y=ship_y,width=258,height=height,label="CMP_NAVY18_SHIPCTRL_UNSET_FLAGSHIP",font=font,
           action=f"GetScriptedGui('cmp_navy18_shipctrl_unset_flagship').Execute({formation_root})",
           enabled_when=f"[GetScriptedGui('cmp_navy18_shipctrl_unset_flagship').IsValid({formation_root})]",
           tooltip="CMP_NAVY18_SHIPCTRL_FLAGSHIP_TT",color="0.55 0.50 0.38 0.96")
    button(lines,8,x=542,y=ship_y,width=258,height=height,label="CMP_NAVY18_SHIPCTRL_CLEAR",font=font,
           action=f"GetScriptedGui('cmp_navy18_shipctrl_clear').Execute({formation_root})",
           enabled_when=f"[GetScriptedGui('cmp_navy18_shipctrl_clear').IsValid({formation_root})]",
           tooltip="CMP_NAVY18_SHIPCTRL_CLEAR_TT",color="0.68 0.40 0.43 0.96")
    ship_y += height + 8
    button(lines,8,x=0,y=ship_y,width=258,height=height,label="CMP_NAVY18_TRANSFER_ADD_BATCH",font=font,
           action=f"GetScriptedGui('cmp_navy18_transfer_add_exact').Execute({formation_root})",
           enabled_when=f"[GetScriptedGui('cmp_navy18_transfer_add_exact').IsValid({formation_root})]",
           tooltip="CMP_NAVY18_TRANSFER_BATCH_TT",color="0.42 0.58 0.72 0.98")
    button(lines,8,x=271,y=ship_y,width=258,height=height,label="CMP_NAVY18_TRANSFER_REMOVE_BATCH",font=font,
           action=f"GetScriptedGui('cmp_navy18_transfer_remove_exact').Execute({formation_root})",
           enabled_when=f"[GetScriptedGui('cmp_navy18_transfer_remove_exact').IsValid({formation_root})]",
           tooltip="CMP_NAVY18_TRANSFER_BATCH_TT",color="0.55 0.50 0.38 0.96")
    button(lines,8,x=542,y=ship_y,width=258,height=height,label="CMP_NAVY18_MODE_TRANSFER",font=font,
           action="GetVariableSystem.Set('cmp_workspace_fleet_builder_mode', 'transfer')",
           tooltip="CMP_NAVY18_TRANSFER_DESC",color="0.48 0.58 0.72 0.98")
    ship_y += height + 10
    for ep,key in [('cmp_navy18_shipctrl_result_selected','CMP_NAVY18_SHIPCTRL_RESULT_SELECTED'),('cmp_navy18_shipctrl_result_flagship_set','CMP_NAVY18_SHIPCTRL_RESULT_FLAGSHIP_SET'),('cmp_navy18_shipctrl_result_flagship_unset','CMP_NAVY18_SHIPCTRL_RESULT_FLAGSHIP_UNSET')]:
        line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'{ep}\').IsShown({formation_root})]" position = {{ 0 {ship_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "{key}" }}')
    line(lines,7,'}')
    line(lines,6,'}'); line(lines,5,'}'); line(lines,4,'}')

    # beta18 Final Exact Ship Transfers surface: exact Ship marker + marked country receiver + optional 20-ship basket.
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_navy18_transfer_{profile["id"]}" visible = "{military_subtab_visible(variable, "transfer", "catalog")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 800 1050 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 36 }} maximumsize = {{ 730 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_NAVY18_TRANSFER_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'fleet_builder')",
           tooltip="CMP_NAVY18_TRANSFER_DESC", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 42 }} size = {{ 800 68 }} maximumsize = {{ 800 68 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_DESC" }}')
    transfer_y = render_fleet_target_row(lines, 7, profile, y=116) + 2
    line(lines, 7, f'textbox = {{ visible = "[Not(GetSelectedFormation.IsFleet)]" position = {{ 0 {transfer_y} }} size = {{ 800 40 }} maximumsize = {{ 800 40 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_SELECT_FLEET_FIRST" }}')
    line(lines, 7, f'widget = {{ visible = "[GetSelectedFormation.IsFleet]" datacontext = "[GetSelectedFormation]" position = {{ 0 {transfer_y} }} size = {{ 800 850 }}')
    formation_root = "GuiScope.SetRoot(MilitaryFormation.MakeScope).End"
    ty = 0
    line(lines,8,f'textbox = {{ position = {{ 0 {ty} }} size = {{ 190 30 }} maximumsize = {{ 190 30 }} fontsize = {font+1} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_RECEIVER" }}')
    button(lines,8,x=200,y=ty,width=250,height=height,label="CMP_NAVY18_TRANSFER_OPEN_TARGETS",font=font,
           action="GetVariableSystem.Set('cmp_workspace_page', 'target')",tooltip="CMP_NAVY18_TRANSFER_RECEIVER_TT",color="0.48 0.58 0.72 0.98")
    line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_transfer_receiver_ready\').IsShown({formation_root})]" position = {{ 462 {ty} }} size = {{ 338 {height} }} maximumsize = {{ 338 {height} }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_NAVY18_TRANSFER_RECEIVER_READY" }}')
    ty += height + 6
    for ep,key in [('cmp_navy18_transfer_receiver_missing','CMP_NAVY18_TRANSFER_RECEIVER_MISSING'),('cmp_navy18_transfer_receiver_self','CMP_NAVY18_TRANSFER_RECEIVER_SELF'),('cmp_navy18_transfer_receiver_no_port','CMP_NAVY18_TRANSFER_RECEIVER_NO_PORT')]:
        line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'{ep}\').IsShown({formation_root})]" position = {{ 0 {ty} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "{key}" }}')
    ty += 34
    line(lines,8,f'textbox = {{ position = {{ 0 {ty} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font+1} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_EXACT_TITLE" }}')
    ty += 32
    line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_transfer_exact_eligible\').IsShown({formation_root})]" position = {{ 0 {ty} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_EXACT_READY" }}')
    line(lines,8,f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_navy18_transfer_exact_eligible\').IsShown({formation_root}))]" position = {{ 0 {ty} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_EXACT_BAD" }}')
    ty += 30
    line(lines,8,f'textbox = {{ position = {{ 0 {ty} }} size = {{ 90 28 }} maximumsize = {{ 90 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SHIPCTRL_TYPE" }}')
    for h in catalog['combat_hulls']:
        line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_shipctrl_type_{h["id"]}\').IsShown({formation_root})]" position = {{ 94 {ty} }} size = {{ 706 28 }} maximumsize = {{ 706 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_HULL_{h["id"].upper()}" }}')
    ty += 36
    button(lines,8,x=0,y=ty,width=258,height=height,label="CMP_NAVY18_TRANSFER_ADD_BATCH",font=font,
           action=f"GetScriptedGui('cmp_navy18_transfer_add_exact').Execute({formation_root})",
           enabled_when=f"[GetScriptedGui('cmp_navy18_transfer_add_exact').IsValid({formation_root})]",
           tooltip="CMP_NAVY18_TRANSFER_BATCH_TT",color="0.42 0.58 0.72 0.98")
    button(lines,8,x=271,y=ty,width=258,height=height,label="CMP_NAVY18_TRANSFER_REMOVE_BATCH",font=font,
           action=f"GetScriptedGui('cmp_navy18_transfer_remove_exact').Execute({formation_root})",
           enabled_when=f"[GetScriptedGui('cmp_navy18_transfer_remove_exact').IsValid({formation_root})]",
           tooltip="CMP_NAVY18_TRANSFER_BATCH_TT",color="0.55 0.50 0.38 0.96")
    button(lines,8,x=542,y=ty,width=258,height=height,label="CMP_NAVY18_TRANSFER_CLEAR_BATCH",font=font,
           action=f"GetScriptedGui('cmp_navy18_transfer_clear_batch').Execute({formation_root})",
           enabled_when=f"[GetScriptedGui('cmp_navy18_transfer_clear_batch').IsValid({formation_root})]",
           tooltip="CMP_NAVY18_TRANSFER_BATCH_TT",color="0.68 0.40 0.43 0.96")
    ty += height + 12
    line(lines,8,f'textbox = {{ position = {{ 0 {ty} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font+1} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_BATCH_TITLE" }}')
    ty += 32
    line(lines,8,f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_navy18_transfer_has_batch\').IsShown({formation_root}))]" position = {{ 0 {ty} }} size = {{ 390 28 }} maximumsize = {{ 390 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_BATCH_EMPTY" }}')
    line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_transfer_batch_valid\').IsShown({formation_root})]" position = {{ 0 {ty} }} size = {{ 390 28 }} maximumsize = {{ 390 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_BATCH_READY" }}')
    line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_transfer_batch_invalid\').IsShown({formation_root})]" position = {{ 0 {ty} }} size = {{ 390 44 }} maximumsize = {{ 390 44 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_BATCH_INVALID" }}')
    line(lines,8,f'textbox = {{ position = {{ 404 {ty} }} size = {{ 210 28 }} maximumsize = {{ 210 28 }} fontsize = {font} fontsize_min = 12 align = right text = "CMP_NAVY18_TRANSFER_BATCH_COUNT" }}')
    for n in range(1, navy18['transfer']['batch_max'] + 1):
        line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_transfer_batch_count_{n}\').IsShown({formation_root})]" position = {{ 620 {ty} }} size = {{ 180 28 }} maximumsize = {{ 180 28 }} fontsize = {font+1} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_BATCH_COUNT_{n}" }}')
    ty += 52
    line(lines,8,f'textbox = {{ position = {{ 0 {ty} }} size = {{ 800 58 }} maximumsize = {{ 800 58 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_WARNING" }}')
    ty += 66
    button(lines,8,x=0,y=ty,width=396,height=height,label="CMP_NAVY18_TRANSFER_SINGLE",font=font,
           action=f"GetScriptedGui('cmp_navy18_transfer_single').Execute({formation_root})",
           enabled_when=f"[GetScriptedGui('cmp_navy18_transfer_single').IsValid({formation_root})]",
           tooltip="CMP_NAVY18_TRANSFER_SINGLE_TT",color="0.62 0.46 0.32 0.98")
    button(lines,8,x=404,y=ty,width=396,height=height,label="CMP_NAVY18_TRANSFER_BATCH",font=font,
           action=f"GetScriptedGui('cmp_navy18_transfer_batch').Execute({formation_root})",
           enabled_when=f"[GetScriptedGui('cmp_navy18_transfer_batch').IsValid({formation_root})]",
           tooltip="CMP_NAVY18_TRANSFER_BATCH_ACTION_TT",color="0.68 0.40 0.43 0.96")
    ty += height + 10
    for ep,key in [('cmp_navy18_transfer_result_added','CMP_NAVY18_TRANSFER_RESULT_ADDED'),('cmp_navy18_transfer_result_removed','CMP_NAVY18_TRANSFER_RESULT_REMOVED'),('cmp_navy18_transfer_result_single','CMP_NAVY18_TRANSFER_RESULT_SINGLE'),('cmp_navy18_transfer_result_batch','CMP_NAVY18_TRANSFER_RESULT_BATCH'),('cmp_navy18_transfer_result_cleared','CMP_NAVY18_TRANSFER_RESULT_CLEARED')]:
        line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'{ep}\').IsShown({formation_root})]" position = {{ 0 {ty} }} size = {{ 800 40 }} maximumsize = {{ 800 40 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "{key}" }}')
    ty += 46
    line(lines,8,f'textbox = {{ position = {{ 0 {ty} }} size = {{ 800 44 }} maximumsize = {{ 800 44 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_TRANSFER_SCOPE_NOTE" }}')
    line(lines,7,'}')
    line(lines,6,'}'); line(lines,5,'}'); line(lines,4,'}')

    # beta18 Final Retrofit & Naval Logistics surface: native template bridge + national Supply Ship reserve.
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_navy18_logistics_{profile["id"]}" visible = "{military_subtab_visible(variable, "logistics", "catalog")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 800 1120 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 36 }} maximumsize = {{ 730 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_NAVY18_LOGISTICS_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'fleet_builder')",
           tooltip="CMP_NAVY18_LOGISTICS_DESC", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 42 }} size = {{ 800 72 }} maximumsize = {{ 800 72 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_LOGISTICS_DESC" }}')
    ly = 122
    line(lines,7,f'textbox = {{ position = {{ 0 {ly} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font+2} fontsize_min = 12 align = left text = "CMP_NAVY18_RETROFIT_TITLE" }}'); ly += 34
    line(lines,7,f'textbox = {{ position = {{ 0 {ly} }} size = {{ 800 48 }} maximumsize = {{ 800 48 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_RETROFIT_STATUS" }}'); ly += 54
    button(lines,7,x=0,y=ly,width=396,height=height,label="CMP_NAVY18_RETROFIT_OPEN_DESIGNER",font=font,
           action="PopupManager.ToggleShipDesignerPopup",enabled_when="[HasDlcFeature('ship_designer')]",
           tooltip="CMP_NAVY18_RETROFIT_OPEN_DESIGNER_TT",color="0.48 0.58 0.72 0.98")
    # The native Fleet panel is opened only from the actual selected MilitaryFormation data context.
    line(lines,7,f'widget = {{ visible = "[GetSelectedFormation.IsFleet]" datacontext = "[GetSelectedFormation]" position = {{ 404 {ly} }} size = {{ 396 {height} }}')
    button(lines,8,x=0,y=0,width=396,height=height,label="CMP_NAVY18_RETROFIT_OPEN_FLEET",font=font,
           action="InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')",
           tooltip="CMP_NAVY18_RETROFIT_OPEN_FLEET_TT",color="0.48 0.58 0.72 0.98")
    line(lines,7,'}')
    ly += height + 6
    line(lines,7,f'textbox = {{ visible = "[Not(GetSelectedFormation.IsFleet)]" position = {{ 0 {ly} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_RETROFIT_SELECT_FLEET" }}'); ly += 32
    line(lines,7,f'textbox = {{ position = {{ 0 {ly} }} size = {{ 800 76 }} maximumsize = {{ 800 76 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_RETROFIT_FLOW" }}'); ly += 86

    line(lines,7,f'textbox = {{ position = {{ 0 {ly} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font+2} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_RESERVE_TITLE" }}'); ly += 34
    line(lines,7,f'textbox = {{ position = {{ 0 {ly} }} size = {{ 800 52 }} maximumsize = {{ 800 52 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_RESERVE_DESC" }}'); ly += 58
    line(lines,7,f'textbox = {{ position = {{ 0 {ly} }} size = {{ 240 28 }} maximumsize = {{ 240 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_MAINT_TITLE" }}')
    country_root = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    line(lines,7,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_supply_maintenance_good\').IsShown({country_root})]" position = {{ 250 {ly} }} size = {{ 550 28 }} maximumsize = {{ 550 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_MAINT_GOOD" }}')
    line(lines,7,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_supply_maintenance_medium\').IsShown({country_root})]" position = {{ 250 {ly} }} size = {{ 550 28 }} maximumsize = {{ 550 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_MAINT_MEDIUM" }}')
    line(lines,7,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_supply_maintenance_bad\').IsShown({country_root})]" position = {{ 250 {ly} }} size = {{ 550 28 }} maximumsize = {{ 550 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_MAINT_BAD" }}'); ly += 36
    supply_amounts = navy18['naval_logistics']['supply_add_amounts']
    sgap=8; sw=(800-sgap*(len(supply_amounts)-1))//len(supply_amounts)
    for i,n in enumerate(supply_amounts):
        economy_action_button(lines,7,x=i*(sw+sgap),y=ly,width=sw,height=height,label=f"CMP_NAVY18_SUPPLY_ADD_{n}",font=font,
                              effect=f"cmp_navy18_supply_add_{n}",tooltip="CMP_NAVY18_SUPPLY_ADD_TT",color="0.38 0.68 0.44 0.96")
    ly += height + 8
    line(lines,7,f'textbox = {{ position = {{ 0 {ly} }} size = {{ 180 28 }} maximumsize = {{ 180 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_RESULT_PREFIX" }}')
    for n in supply_amounts:
        line(lines,7,f'textbox = {{ visible = "[GetScriptedGui(\'cmp_navy18_supply_result_{n}\').IsShown({country_root})]" position = {{ 190 {ly} }} size = {{ 610 28 }} maximumsize = {{ 610 28 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_RESULT_{n}" }}')
    ly += 38

    line(lines,7,f'textbox = {{ position = {{ 0 {ly} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font+2} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_SELECTED_TITLE" }}'); ly += 34
    line(lines,7,f'textbox = {{ position = {{ 0 {ly} }} size = {{ 800 52 }} maximumsize = {{ 800 52 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_SELECTED_DESC" }}'); ly += 58
    line(lines,7,f'textbox = {{ visible = "[Not(GetSelectedFormation.IsFleet)]" position = {{ 0 {ly} }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_NO_FLEET" }}')
    line(lines,7,f'widget = {{ visible = "[GetSelectedFormation.IsFleet]" datacontext = "[GetSelectedFormation]" position = {{ 0 {ly} }} size = {{ 800 42 }}')
    logistics_root = "GuiScope.SetRoot(MilitaryFormation.MakeScope).End"
    line(lines,8,f'textbox = {{ position = {{ 0 0 }} size = {{ 330 30 }} maximumsize = {{ 330 30 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_SUPPLY_ASSIGNED_LABEL" }}')
    for ep,key in [
        ('cmp_navy18_supply_assigned_0','CMP_NAVY18_SUPPLY_ASSIGNED_0'),('cmp_navy18_supply_assigned_1','CMP_NAVY18_SUPPLY_ASSIGNED_1'),('cmp_navy18_supply_assigned_2','CMP_NAVY18_SUPPLY_ASSIGNED_2'),('cmp_navy18_supply_assigned_3','CMP_NAVY18_SUPPLY_ASSIGNED_3'),('cmp_navy18_supply_assigned_4','CMP_NAVY18_SUPPLY_ASSIGNED_4'),('cmp_navy18_supply_assigned_5','CMP_NAVY18_SUPPLY_ASSIGNED_5'),('cmp_navy18_supply_assigned_6_10','CMP_NAVY18_SUPPLY_ASSIGNED_6_10'),('cmp_navy18_supply_assigned_11_20','CMP_NAVY18_SUPPLY_ASSIGNED_11_20'),('cmp_navy18_supply_assigned_21_50','CMP_NAVY18_SUPPLY_ASSIGNED_21_50'),('cmp_navy18_supply_assigned_51_plus','CMP_NAVY18_SUPPLY_ASSIGNED_51_PLUS')]:
        line(lines,8,f'textbox = {{ visible = "[GetScriptedGui(\'{ep}\').IsShown({logistics_root})]" position = {{ 340 0 }} size = {{ 120 30 }} maximumsize = {{ 120 30 }} fontsize = {font+1} fontsize_min = 12 align = left text = "{key}" }}')
    line(lines,8,f'textbox = {{ position = {{ 470 0 }} size = {{ 330 30 }} maximumsize = {{ 330 30 }} fontsize = {font} fontsize_min = 12 align = right elide = right text = "[MilitaryFormation.GetNameNoFormatting]" tooltip = "[MilitaryFormation.GetNameNoFormatting]" }}')
    line(lines,7,'}'); ly += 48
    line(lines,7,f'textbox = {{ position = {{ 0 {ly} }} size = {{ 800 54 }} maximumsize = {{ 800 54 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_NAVY18_LOGISTICS_SCOPE_NOTE" }}')
    line(lines,6,'}'); line(lines,5,'}'); line(lines,4,'}')
    line(lines,3,'}')


def render_military_fleet_templates(lines: list[str], profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    area_height = 514 - y
    variable = "cmp_workspace_fleet_template_tab"
    line(lines, 3, f'widget = {{ visible = "{military_tab_visible("fleet_templates")}" position = {{ 4 {y} }} size = {{ 840 {area_height} }}')
    tabs = [
        ("CMP_WS_MIL_SUB_FLEET_DESIGNER", "designer", "CMP_WS_MIL_HELP_FLEET_TEMPLATES_TT"),
        ("CMP_WS_MIL_SUB_TASKFORCE", "taskforce", "CMP_WS_MIL_HELP_TASKFORCE_TT"),
    ]
    render_military_subtabs(lines, profile, y=0, variable=variable, tabs=tabs, default="designer")
    render_fleet_target_row(lines, 4, profile, y=height + 8)
    content_y = height * 2 + 28
    content_height = area_height - content_y
    # Fleet designer
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_military_fleet_template_designer_{profile["id"]}" visible = "{military_subtab_visible(variable, "designer", "designer")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 800 900 }')
    line(lines, 7, f'textbox = {{ size = {{ 720 36 }} maximumsize = {{ 720 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_FD_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'fleet_templates')",
           tooltip="CMP_WS_MIL_HELP_FLEET_TEMPLATES_TT", color="0.48 0.58 0.72 0.98")
    cursor_y = 48
    groups = [
        ("CMP_FD_SIZE", [(f"CMP_FD_SIZE_{v}", f"cmp_fleet_designer_select_size_{v}", f"cmp_fleet_designer_size_{v}_selected") for v in [10, 20, 40]], 3),
        ("CMP_FD_ESCORT", [(f"CMP_FD_E{v}", f"cmp_fleet_designer_select_escort_{v}", f"cmp_fleet_designer_escort_{v}_selected") for v in [20, 40, 60]], 3),
        ("CMP_FD_CARRIER", [(f"CMP_FD_C{v}", f"cmp_fleet_designer_select_carrier_{v}", f"cmp_fleet_designer_carrier_{v}_selected") for v in [0, 10, 20]], 3),
        ("CMP_FD_SUB", [(f"CMP_FD_S{v}", f"cmp_fleet_designer_select_sub_{v}", f"cmp_fleet_designer_sub_{v}_selected") for v in [0, 20, 40]], 3),
    ]
    for title, items, columns in groups:
        line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "{title}" }}')
        cursor_y = render_effect_choices(lines, 7, profile, y=cursor_y + 32, items=items, columns=columns,
                                         tooltip="CMP_WS_MIL_FLEET_DESIGNER_TT") + 8
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 38 }} maximumsize = {{ 800 38 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_MIL_CAPITAL_REMAINDER" }}')
    cursor_y += 44
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_FD_PROFILES" }}')
    cursor_y += 32
    profiles = [
        ("CMP_FD_BATTLE", "cmp_fleet_designer_profile_battle", None),
        ("CMP_FD_CARRIER_PROFILE", "cmp_fleet_designer_profile_carrier", None),
        ("CMP_FD_ESCORT_PROFILE", "cmp_fleet_designer_profile_escort", None),
        ("CMP_FD_WOLFPACK", "cmp_fleet_designer_profile_wolfpack", None),
        ("CMP_FD_AMPHIB", "cmp_fleet_designer_profile_amphibious", None),
    ]
    cursor_y = render_effect_choices(lines, 7, profile, y=cursor_y, items=profiles, columns=2,
                                     tooltip="CMP_WS_MIL_FLEET_PROFILE_TT") + 10
    economy_action_button(lines, 7, x=0, y=cursor_y, width=396, height=height,
                          label="CMP_FD_APPLY", font=font, effect="cmp_fleet_designer_apply",
                          tooltip="CMP_FD_APPLY_TT", color="0.38 0.68 0.44 0.96")
    economy_action_button(lines, 7, x=404, y=cursor_y, width=396, height=height,
                          label="CMP_FD_CLEAR", font=font, effect="cmp_fleet_designer_clear",
                          tooltip="CMP_WS_MIL_RESET_TT", color="0.68 0.40 0.43 0.96")
    line(lines, 6, '}'); line(lines, 5, '}'); line(lines, 4, '}')
    # Amphibious task force
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_military_fleet_template_taskforce_{profile["id"]}" visible = "{military_subtab_visible(variable, "taskforce", "designer")}" position = {{ 0 {content_y} }} size = {{ 820 {content_height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {'); line(lines, 6, 'widget = { size = { 800 560 }')
    line(lines, 7, f'textbox = {{ size = {{ 720 36 }} maximumsize = {{ 720 36 }} fontsize = {font + 3} fontsize_min = 13 align = left text = "CMP_TASKFORCE_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=40, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'taskforce')",
           tooltip="CMP_WS_MIL_HELP_TASKFORCE_TT", color="0.48 0.58 0.72 0.98")
    marine_items = [(f"CMP_ARMY_AMPH_AMOUNT_{v}", f"cmp_army_amphib_select_amount_{v}", f"cmp_army_amphib_amount_{v}_selected") for v in [5, 10, 25, 50]]
    cursor_y = render_effect_choices(lines, 7, profile, y=52, items=marine_items, columns=4,
                                     tooltip="CMP_WS_MIL_MARINE_AMOUNT_TT") + 12
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    line(lines, 7, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_fleet_taskforce_ready\').IsShown({scope})]" position = {{ 0 {cursor_y} }} size = {{ 800 34 }} maximumsize = {{ 800 34 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_TASKFORCE_READY" }}')
    line(lines, 7, f'textbox = {{ visible = "[Not(GetScriptedGui(\'cmp_fleet_taskforce_ready\').IsShown({scope}))]" position = {{ 0 {cursor_y} }} size = {{ 800 44 }} maximumsize = {{ 800 44 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_TASKFORCE_NOT_READY" }}')
    cursor_y += 52
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 54 }} maximumsize = {{ 800 54 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_MIL_MANUAL_ATTACH_WARNING" }}')
    cursor_y += 64
    economy_action_button(lines, 7, x=0, y=cursor_y, width=800, height=height,
                          label="CMP_TASKFORCE_PREPARE", font=font, effect="cmp_fleet_taskforce_prepare",
                          tooltip="CMP_TASKFORCE_PREPARE_TT", color="0.38 0.68 0.44 0.96")
    line(lines, 6, '}'); line(lines, 5, '}'); line(lines, 4, '}'); line(lines, 3, '}')


def render_military_help(lines: list[str], profile: dict) -> None:
    font = profile["font_size"]
    profile_id = profile["id"]
    line(lines, 3, 'widget = { name = "cmp_workspace_military_help_card" visible = "[GetVariableSystem.Exists(\'cmp_workspace_military_help\')]" position = { 32 72 } size = { 792 420 }')
    line(lines, 4, 'icon = { size = { 792 420 } texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = { 0.045 0.055 0.075 0.998 } }')
    line(lines, 4, 'icon = { position = { 2 2 } size = { 788 416 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.98 } alwaystransparent = yes }')
    line(lines, 4, f'textbox = {{ position = {{ 20 14 }} size = {{ 680 36 }} maximumsize = {{ 680 36 }} fontsize = {font + 4} fontsize_min = 14 align = left text = "CMP_WS_MIL_HELP_TITLE" }}')
    line(lines, 4, 'close_button = { position = { 736 10 } size = { 42 42 } onclick = "[GetVariableSystem.Clear(\'cmp_workspace_military_help\')]" }')
    topics = [
        ("overview", "CMP_WS_MIL_HELP_OVERVIEW"),
        ("army_builder", "CMP_WS_MIL_HELP_ARMY"),
        ("army_templates", "CMP_WS_MIL_HELP_TEMPLATES"),
        ("army_controls", "CMP_WS_MIL_HELP_CONTROLS"),
        ("fleet_builder", "CMP_WS_MIL_HELP_FLEET"),
        ("fleet_templates", "CMP_WS_MIL_HELP_FLEET_TEMPLATES"),
        ("marines", "CMP_WS_MIL_HELP_MARINES"),
        ("taskforce", "CMP_WS_MIL_HELP_TASKFORCE"),
    ]
    for topic, key in topics:
        line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_military_help_{topic}_{profile_id}" visible = "[GetVariableSystem.HasValue(\'cmp_workspace_military_help\', \'{topic}\')]" position = {{ 20 60 }} size = {{ 752 338 }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
        line(lines, 5, 'scrollwidget = {')
        line(lines, 6, f'textbox = {{ size = {{ 720 980 }} maximumsize = {{ 720 980 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "{key}" }}')
        line(lines, 5, '}'); line(lines, 4, '}')
    line(lines, 3, '}')


def render_military_page(lines: list[str], units: list[dict], ships: list[dict], fleet: dict,
                         navy18: dict, profile: dict) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    line(lines, 2, f'widget = {{ visible = "{page_visible("military")}" position = {{ 238 76 }} size = {{ 864 514 }}')
    line(lines, 3, f'textbox = {{ position = {{ 4 0 }} size = {{ 420 36 }} maximumsize = {{ 420 36 }} fontsize = {font + 6} fontsize_min = 14 align = left text = "CMP_WS_MIL_TITLE" }}')
    button(lines, 3, x=432, y=0, width=56, height=height, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_military_help', 'overview')",
           tooltip="CMP_WS_MIL_HELP_OVERVIEW_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 3, f'textbox = {{ position = {{ 4 40 }} size = {{ 500 30 }} maximumsize = {{ 500 30 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_MIL_FLOW" }}')
    button(lines, 3, x=496, y=0, width=106, height=height, label="CMP_OPS_PRE1_1_OPEN", font=font,
           action="GetVariableSystem.Set('cmp_workspace_operations_discovery', 'open')",
           tooltip="CMP_OPS_PRE1_1_OPEN_TT", color="0.50 0.55 0.72 0.97")
    button(lines, 3, x=610, y=0, width=214, height=height, label="CMP_WS_MIL_TARGETS", font=font,
           action="GetVariableSystem.Set('cmp_workspace_page', 'target')",
           tooltip="CMP_WS_MIL_TARGETS_TT", color="0.45 0.62 0.82 0.97")
    tab_y = max(88, height + 36)
    render_military_tabs(lines, profile, y=tab_y)
    content_y = tab_y + height + 10
    render_military_army_builder(lines, units, profile, y=content_y)
    render_military_army_templates(lines, profile, y=content_y)
    render_military_army_controls(lines, profile, y=content_y)
    render_military_fleet_builder(lines, ships, fleet, navy18, profile, y=content_y)
    render_military_fleet_templates(lines, profile, y=content_y)
    render_military_fleet_picker(lines, profile)
    render_military_operations_discovery(lines, profile)
    render_military_help(lines, profile)
    line(lines, 2, '}')



def render_selected_building_name(lines: list[str], indent: int, buildings: list[dict],
                                  profile: dict, *, x: int, y: int, width: int,
                                  staffing: bool = False) -> None:
    font = profile["font_size"]
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    if staffing:
        line(lines, indent, f"textbox = {{ visible = \"[Not(GetScriptedGui('cmp_staffing_workspace_selection_ready').IsShown({scope}))]\" position = {{ {x} {y} }} size = {{ {width} 30 }} maximumsize = {{ {width} 30 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = \"CMP_WS_RB_NOT_SELECTED\" }}")
        for building in buildings:
            line(lines, indent, f"textbox = {{ visible = \"[GetScriptedGui('cmp_staffing_workspace_{building['id']}_selected').IsShown({scope})]\" position = {{ {x} {y} }} size = {{ {width} 30 }} maximumsize = {{ {width} 30 }} fontsize = {font + 1} fontsize_min = 12 align = left|nobaseline text = \"{building['building_type']}\" }}")
        return
    line(lines, indent, f"textbox = {{ visible = \"[Not(GetScriptedGui('cmp_regions2_has_selected_building_check').IsShown({scope}))]\" position = {{ {x} {y} }} size = {{ {width} 30 }} maximumsize = {{ {width} 30 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = \"CMP_WS_RB_NOT_SELECTED\" }}")
    for building in buildings:
        line(lines, indent, f"textbox = {{ visible = \"[GetScriptedGui('cmp_regions2_building_{building['id']}_selected').IsShown({scope})]\" position = {{ {x} {y} }} size = {{ {width} 30 }} maximumsize = {{ {width} 30 }} fontsize = {font + 1} fontsize_min = 12 align = left|nobaseline text = \"{building['building_type']}\" }}")

def building_category_visible(category_id: str, variable: str = "cmp_workspace_building_category") -> str:
    if category_id == "all":
        return (f"[Or(Not(GetVariableSystem.Exists('{variable}')), "
                f"GetVariableSystem.HasValue('{variable}', 'all'))]")
    return f"[GetVariableSystem.HasValue('{variable}', '{category_id}')]"



def render_regions_category_filter(lines: list[str], categories: list[dict],
                                   profile: dict, *, instance: str) -> None:
    font = profile["font_size"]
    button_height = profile["button_height"]
    variable = "cmp_workspace_staffing_category" if instance == "staffing" else "cmp_workspace_building_category"
    menu_variable = f"cmp_workspace_building_category_menu_{instance}"
    current_x = 176
    current_width = 160
    for category in categories:
        line(lines, 5, f"widget = {{ visible = \"{building_category_visible(category['id'], variable)}\" position = {{ {current_x} 0 }} size = {{ {current_width} 44 }}")
        button(lines, 6, x=0, y=0, width=current_width, height=44,
               label=category["label"], font=font,
               action=f"GetVariableSystem.Toggle('{menu_variable}')",
               tooltip=category["tooltip"], color="0.42 0.55 0.72 0.97", label_transparent=True)
        line(lines, 5, '}')
    rows = (len(categories) + 1) // 2
    menu_height = 16 + rows * (button_height + 6)
    line(lines, 5, f"widget = {{ name = \"cmp_workspace_building_category_menu_{instance}_{profile['id']}\" visible = \"[GetVariableSystem.Exists('{menu_variable}')]\" position = {{ 0 50 }} size = {{ 392 {menu_height} }}")
    line(lines, 6, f'icon = {{ size = {{ 392 {menu_height} }} texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = {{ 0.045 0.055 0.075 0.998 }} }}')
    line(lines, 6, f'icon = {{ position = {{ 2 2 }} size = {{ 388 {menu_height - 4} }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = {{ 0.35 0.42 0.52 0.98 }} alwaystransparent = yes }}')
    gap = 8
    width = (360 - gap) // 2
    for index, category in enumerate(categories):
        row, col = divmod(index, 2)
        x = 16 + col * (width + gap)
        y = 8 + row * (button_height + 6)
        button(lines, 6, x=x, y=y, width=width, height=button_height,
               label=category["label"], font=font,
               actions=[f"GetVariableSystem.Set('{variable}', '{category['id']}')", f"GetVariableSystem.Clear('{menu_variable}')"],
               tooltip=category["tooltip"], color="0.40 0.53 0.68 0.99", label_transparent=True)
        variable_selected_line(lines, 6, x=x, y=y + button_height - 4,
                               width=width, variable=variable,
                               value=category["id"], default=category["id"] == "all")
    line(lines, 5, '}')

def render_regions_building_scroll(lines: list[str], buildings: list[dict], profile: dict,
                                   *, height: int, mode: str, instance: str,
                                   category_id: str | None = None) -> None:
    button_height = profile["button_height"]; profile_id = profile["id"]
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    name = f"cmp_workspace_regions_{instance}_{mode}_picker_{profile_id}" if category_id is None or category_id == "all" else f"cmp_workspace_regions_{instance}_{mode}_picker_{profile_id}_{category_id}"
    category_variable = "cmp_workspace_staffing_category" if instance == "staffing" else "cmp_workspace_building_category"
    visible = building_category_visible(category_id, category_variable) if category_id else None
    visible_text = f' visible = "{visible}"' if visible else ""
    line(lines, 5, f'scrollarea = {{ name = "{name}"{visible_text} position = {{ 0 52 }} size = {{ 412 {height - 52} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 6, 'scrollwidget = {')
    gap = 8; columns = 2; button_width = (392 - gap) // columns
    rows = (len(buildings) + columns - 1) // columns; content_height = max(height - 52, rows * (button_height + gap) + 8)
    line(lines, 7, f'widget = {{ size = {{ 392 {content_height} }}')
    if not buildings:
        line(lines, 8, f'textbox = {{ position = {{ 8 12 }} size = {{ 368 80 }} maximumsize = {{ 368 80 }} multiline = yes autoresize = no fontsize = {profile["font_size"]} fontsize_min = 12 align = left text = "CMP_WS_RB_CATEGORY_EMPTY" }}')
    for index, building in enumerate(buildings):
        row, col = divmod(index, columns); x = col * (button_width + gap); py = row * (button_height + gap)
        if instance == "staffing":
            endpoint=f"cmp_staffing_select_{building['id']}"; enabled_when=f"[GetScriptedGui('{endpoint}').IsValid({scope})]"
            button(lines, 8, x=x, y=py, width=button_width, height=button_height,
                   label=building["building_type"], font=profile["font_size"], action=f"GetScriptedGui('{endpoint}').Execute({scope})",
                   enabled_when=enabled_when, tooltip=building["building_type"], color="0.40 0.53 0.68 0.97", elide=True, label_transparent=True)
            selected_line(lines, 8, x=x, y=py + button_height - 4, width=button_width, effect=f"cmp_staffing_workspace_{building['id']}_selected")
        else:
            endpoint=f"cmp_regions2_select_{mode}_{building['id']}" if mode in {"building","resource"} else None
            button(lines, 8, x=x, y=py, width=button_width, height=button_height,
                   label=building["building_type"], font=profile["font_size"], action=f"GetScriptedGui('{endpoint}').Execute({scope})",
                   enabled_when=f"[GetScriptedGui('{endpoint}').IsValid({scope})]", tooltip=building["building_type"],
                   color="0.40 0.53 0.68 0.97", elide=True, label_transparent=True)
            selected_line(lines, 8, x=x, y=py + button_height - 4, width=button_width, effect=f"cmp_regions2_building_{building['id']}_selected")
    line(lines, 7, '}'); line(lines, 6, '}'); line(lines, 5, '}')

def render_regions_building_picker(lines: list[str], buildings: list[dict], profile: dict,
                                   *, y: int, height: int, mode: str,
                                   categories: list[dict] | None = None,
                                   always_visible: bool = False,
                                   instance: str = "operations") -> None:
    font = profile["font_size"]
    default = mode == "building"
    visible = ("[Or(Not(GetVariableSystem.Exists('cmp_workspace_regions_mode')), "
               "GetVariableSystem.HasValue('cmp_workspace_regions_mode', 'building'))]" if default
               else f"[GetVariableSystem.HasValue('cmp_workspace_regions_mode', '{mode}')]" )
    if always_visible:
        visible = "[GetVariableSystem.Exists('cmp_workspace_shell')]"
    if instance == "staffing":
        title = "CMP_WS_STAFF_PICK_BUILDING"
        help_topic = "staffing"
    else:
        title = "CMP_WS_RB_PICK_BUILDING" if mode == "building" else "CMP_WS_RB_PICK_RESOURCE"
        help_topic = "buildings" if mode == "building" else "resources"
    line(lines, 4, f'widget = {{ visible = "{visible}" position = {{ 4 {y} }} size = {{ 412 {height} }}')
    title_width = 168 if categories and mode == "building" else 330
    line(lines, 5, f'textbox = {{ size = {{ {title_width} 44 }} maximumsize = {{ {title_width} 44 }} fontsize = {font + 2} fontsize_min = 12 align = left|nobaseline text = "{title}" }}')
    button(lines, 5, x=344, y=0, width=48, height=44, label="CMP_WS_INFO", font=font,
           action=f"GetVariableSystem.Set('cmp_workspace_regions_help', '{help_topic}')",
           tooltip=f"CMP_WS_RB_HELP_{help_topic.upper()}_TT", color="0.48 0.58 0.72 0.98")
    if categories and mode == "building":
        for category in categories:
            if category["id"] == "all":
                category_buildings = buildings
            elif instance == "staffing":
                category_buildings = [item for item in buildings if item["profile"] in category.get("profiles", [])]
            else:
                category_buildings = [item for item in buildings if item["staffing_profile"] in category.get("profiles", [])]
            render_regions_building_scroll(lines, category_buildings, profile,
                                           height=height, mode=mode, instance=instance,
                                           category_id=category["id"])
        render_regions_category_filter(lines, categories, profile, instance=instance)
    else:
        render_regions_building_scroll(lines, buildings, profile, height=height,
                                       mode=mode, instance=instance)
    line(lines, 4, '}')

def render_regions_preset_picker(lines: list[str], regions: dict, profile: dict,
                                 *, y: int, height: int) -> None:
    font = profile["font_size"]
    button_height = profile["button_height"]
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    line(lines, 4, f'widget = {{ visible = "[GetVariableSystem.HasValue(\'cmp_workspace_regions_mode\', \'preset\')]" position = {{ 4 {y} }} size = {{ 412 {height} }}')
    line(lines, 5, f'textbox = {{ size = {{ 330 38 }} maximumsize = {{ 330 38 }} fontsize = {font + 2} fontsize_min = 12 align = left|nobaseline text = "CMP_WS_RB_PICK_PRESET" }}')
    button(lines, 5, x=344, y=0, width=48, height=38, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_regions_help', 'presets')",
           tooltip="CMP_WS_RB_HELP_PRESETS_TT", color="0.48 0.58 0.72 0.98")
    for index, preset in enumerate(regions["presets"]):
        py = 48 + index * (button_height + 10)
        preset_id = preset["id"]
        button(lines, 5, x=0, y=py, width=392, height=button_height,
               label=f"CMP_RB2_PRESET_{preset_id.upper()}", font=font,
               actions=[
                   f"GetScriptedGui('cmp_regions2_select_mode_preset').Execute({scope})",
                   f"GetScriptedGui('cmp_regions2_select_preset_{preset_id}').Execute({scope})",
               ], tooltip="CMP_WS_RB_PRESET_TT", color="0.40 0.53 0.68 0.97")
        selected_line(lines, 5, x=0, y=py + button_height - 4, width=392,
                      effect=f"cmp_regions2_preset_{preset_id}_selected")
    line(lines, 4, '}')


def render_regions_targets(lines: list[str], indent: int, profile: dict, *, y: int,
                           staffing: bool = False) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    line(lines, indent, f'textbox = {{ position = {{ 0 {y} }} size = {{ 396 24 }} maximumsize = {{ 396 24 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_RB_TARGET_TITLE" }}')
    y += 26
    gap = 6
    width = (396 - gap * 2) // 3
    if staffing:
        targets = [
            ("CMP_WS_RB_TARGET_MARKED_SHORT", "cmp_staffing_apply_player_marked", "CMP_STAFF_TT_TARGET_MARKED"),
            ("CMP_WS_RB_TARGET_INCORP_SHORT", "cmp_staffing_apply_player_incorporated", "CMP_STAFF_TT_TARGET_INCORPORATED"),
            ("CMP_WS_RB_TARGET_FOREIGN_SHORT", "cmp_staffing_apply_marked_country", "CMP_STAFF_TT_TARGET_FOREIGN"),
        ]
    else:
        targets = [
            ("CMP_WS_RB_TARGET_MARKED_SHORT", "cmp_regions2_apply_player_marked", "CMP_WS_RB_TARGET_MARKED_TT"),
            ("CMP_WS_RB_TARGET_INCORP_SHORT", "cmp_regions2_apply_incorporated", "CMP_WS_RB_TARGET_INCORP_TT"),
            ("CMP_WS_RB_TARGET_FOREIGN_SHORT", "cmp_regions2_apply_foreign", "CMP_WS_RB_TARGET_FOREIGN_TT"),
        ]
    for index, (label, effect, tooltip) in enumerate(targets):
        button(lines, indent, x=index * (width + gap), y=y, width=width, height=height,
               label=label, font=font, action=f"GetScriptedGui('{effect}').Execute({scope})",
               enabled_when=f"[GetScriptedGui('{effect}').IsValid({scope})]",
               tooltip=tooltip, color="0.38 0.68 0.44 0.96")



def render_regions_operations_config(lines: list[str], buildings: list[dict], regions: dict,
                                      profile: dict, *, y: int, height: int) -> None:
    font = profile["font_size"]
    button_height = profile["button_height"]
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    normal_visible = "[Not(GetVariableSystem.HasValue('cmp_workspace_regions_mode', 'preset'))]"
    line(lines, 4, f'widget = {{ visible = "{normal_visible}" position = {{ 428 {y} }} size = {{ 416 {height} }}')
    line(lines, 5, f'textbox = {{ size = {{ 396 24 }} maximumsize = {{ 396 24 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_RB_SELECTED" }}')
    render_selected_building_name(lines, 5, buildings, profile, x=0, y=24, width=396)
    line(lines, 5, f'textbox = {{ position = {{ 0 52 }} size = {{ 396 22 }} maximumsize = {{ 396 22 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_RB_OPERATION_TITLE" }}')
    operations = [
        ("CMP_WS_RB_OP_ADD", "add", "CMP_WS_RB_OP_ADD_TT", "0.38 0.68 0.44 0.96"),
        ("CMP_WS_RB_OP_SET", "set", "CMP_WS_RB_OP_SET_TT", "0.72 0.50 0.28 0.96"),
        ("CMP_WS_RB_OP_CLEAR", "remove", "CMP_WS_RB_OP_CLEAR_TT", "0.68 0.40 0.43 0.96"),
    ]
    gap = 6
    op_width = (396 - gap * 2) // 3
    op_y = 74
    for index, (label, op, tooltip, color) in enumerate(operations):
        economy_action_button(lines, 5, x=index * (op_width + gap), y=op_y,
                              width=op_width, height=button_height, label=label, font=font,
                              effect=f"cmp_regions2_select_operation_{op}", tooltip=tooltip,
                              color=color, selected=f"cmp_regions2_operation_{op}_selected")
    warning_y = op_y + button_height + 4
    line(lines, 5, f"textbox = {{ visible = \"[GetScriptedGui('cmp_regions2_operation_set_selected').IsShown({scope})]\" position = {{ 0 {warning_y} }} size = {{ 396 38 }} maximumsize = {{ 396 38 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = \"CMP_WS_RB_SET_WARNING\" }}")
    amount_label_y = warning_y + 42
    amount_visible = f"[Not(GetScriptedGui('cmp_regions2_operation_remove_selected').IsShown({scope}))]"
    line(lines, 5, f'widget = {{ visible = "{amount_visible}" position = {{ 0 {amount_label_y} }} size = {{ 396 {button_height + 30} }}')
    line(lines, 6, f'textbox = {{ size = {{ 396 22 }} maximumsize = {{ 396 22 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_RB_AMOUNT_TITLE" }}')
    amount_y = 24
    amount_gap = 5
    amount_width = (396 - amount_gap * 5) // 6
    for index, amount in enumerate(regions["building_amounts"]):
        economy_action_button(lines, 6, x=index * (amount_width + amount_gap), y=amount_y,
                              width=amount_width, height=button_height,
                              label=f"CMP_RB2_AMOUNT_{amount}", font=font,
                              effect=f"cmp_regions2_select_amount_{amount}",
                              tooltip="CMP_WS_RB_AMOUNT_TT",
                              selected=f"cmp_regions2_amount_{amount}_selected")
    line(lines, 5, '}')
    line(lines, 5, f"textbox = {{ visible = \"[GetScriptedGui('cmp_regions2_operation_remove_selected').IsShown({scope})]\" position = {{ 0 {amount_label_y} }} size = {{ 396 54 }} maximumsize = {{ 396 54 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = \"CMP_WS_RB_REMOVE_ALL_INFO\" }}")
    render_regions_targets(lines, 5, profile, y=amount_label_y + button_height + 38)
    line(lines, 4, '}')
    line(lines, 4, f"widget = {{ visible = \"[GetVariableSystem.HasValue('cmp_workspace_regions_mode', 'preset')]\" position = {{ 428 {y} }} size = {{ 416 {height} }}")
    line(lines, 5, f'textbox = {{ size = {{ 396 30 }} maximumsize = {{ 396 30 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_RB_PRESET_READY" }}')
    line(lines, 5, f'textbox = {{ position = {{ 0 36 }} size = {{ 396 82 }} maximumsize = {{ 396 82 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_RB_PRESET_SUMMARY" }}')
    render_regions_targets(lines, 5, profile, y=124)
    line(lines, 4, '}')

def render_staffing_config(lines: list[str], staffing: dict, regions: dict,
                           profile: dict, *, y: int, height: int) -> None:
    font = profile["font_size"]
    button_height = profile["button_height"]
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    buildings=[b for b in staffing["buildings"] if b["status"] == "SUPPORTED"]
    line(lines, 4, f'widget = {{ position = {{ 428 {y} }} size = {{ 416 {height} }}')
    line(lines, 5, f'textbox = {{ size = {{ 396 24 }} maximumsize = {{ 396 24 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_RB_SELECTED" }}')
    render_selected_building_name(lines, 5, buildings, profile, x=0, y=24, width=396, staffing=True)
    for pid, meta in staffing["profiles"].items():
        if any(b["profile"] == pid for b in buildings):
            line(lines, 5, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_staffing_profile_{pid}_check\').IsShown({scope})]" position = {{ 0 52 }} size = {{ 396 24 }} maximumsize = {{ 396 24 }} fontsize = {font} fontsize_min = 12 align = left text = "{meta["label"]}" }}')
    line(lines, 5, f'textbox = {{ position = {{ 0 78 }} size = {{ 396 22 }} maximumsize = {{ 396 22 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_STAFF_AMOUNT_TITLE" }}')
    amounts = [1000, 5000, 10000, 25000, 50000, 100000]
    gap = 5
    width = (396 - gap * 5) // 6
    amount_y = 102
    for index, amount in enumerate(amounts):
        economy_action_button(lines, 5, x=index * (width + gap), y=amount_y,
                              width=width, height=button_height, label=str(amount), font=font,
                              effect=f"cmp_staffing_select_amount_{amount}",
                              tooltip="CMP_STAFF_TT_AMOUNT",
                              selected=f"cmp_staffing_amount_{amount}_selected_check")
    threshold_label_y = amount_y + button_height + 8
    line(lines, 5, f'textbox = {{ position = {{ 0 {threshold_label_y} }} size = {{ 396 22 }} maximumsize = {{ 396 22 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_STAFF_ADAPTIVE_LABEL" }}')
    threshold_y = threshold_label_y + 24
    thresholds = [("OFF", "off"), ("50", "50"), ("75", "75"), ("90", "90"), ("100", "100")]
    threshold_gap = 5
    threshold_width = (396 - threshold_gap * 4) // 5
    for index, (loc_suffix, effect_suffix) in enumerate(thresholds):
        economy_action_button(lines, 5, x=index * (threshold_width + threshold_gap), y=threshold_y,
                              width=threshold_width, height=button_height,
                              label=f"CMP_STAFF_ADAPTIVE_{loc_suffix}", font=font,
                              effect=f"cmp_staffing_select_adaptive_{effect_suffix}",
                              tooltip="CMP_WS_STAFF_THRESHOLD_TT",
                              selected=f"cmp_staffing_adaptive_{effect_suffix}_selected")
    render_regions_targets(lines, 5, profile, y=threshold_y + button_height + 8, staffing=True)
    line(lines, 4, '}')

def render_regions_help(lines: list[str], profile: dict) -> None:
    font = profile["font_size"]
    profile_id = profile["id"]
    line(lines, 3, 'widget = { name = "cmp_workspace_regions_help_card" visible = "[GetVariableSystem.Exists(\'cmp_workspace_regions_help\')]" position = { 32 72 } size = { 792 420 }')
    line(lines, 4, 'icon = { size = { 792 420 } texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = { 0.045 0.055 0.075 0.998 } }')
    line(lines, 4, 'icon = { position = { 2 2 } size = { 788 416 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.98 } alwaystransparent = yes }')
    line(lines, 4, f'textbox = {{ position = {{ 20 14 }} size = {{ 680 36 }} maximumsize = {{ 680 36 }} fontsize = {font + 4} fontsize_min = 14 align = left text = "CMP_WS_RB_HELP_TITLE" }}')
    line(lines, 4, 'close_button = { position = { 736 10 } size = { 42 42 } onclick = "[GetVariableSystem.Clear(\'cmp_workspace_regions_help\')]" }')
    topics = [
        ("overview", "CMP_WS_RB_HELP_OVERVIEW"),
        ("buildings", "CMP_WS_RB_HELP_BUILDINGS"),
        ("resources", "CMP_WS_RB_HELP_RESOURCES"),
        ("presets", "CMP_WS_RB_HELP_PRESETS"),
        ("staffing", "CMP_WS_RB_HELP_STAFFING"),
    ]
    for topic, key in topics:
        line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_regions_help_{topic}_{profile_id}" visible = "[GetVariableSystem.HasValue(\'cmp_workspace_regions_help\', \'{topic}\')]" position = {{ 20 60 }} size = {{ 752 338 }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
        line(lines, 5, 'scrollwidget = {')
        line(lines, 6, f'textbox = {{ size = {{ 720 820 }} maximumsize = {{ 720 820 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "{key}" }}')
        line(lines, 5, '}')
        line(lines, 4, '}')
    line(lines, 3, '}')


def render_regions_page(lines: list[str], buildings: list[dict], staffing: dict, regions: dict,
                        categories: list[dict], profile: dict) -> None:
    font = profile["font_size"]
    button_height = profile["button_height"]
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    line(lines, 2, f'widget = {{ visible = "{page_visible("regions")}" position = {{ 238 76 }} size = {{ 864 514 }}')
    line(lines, 3, f'textbox = {{ position = {{ 4 0 }} size = {{ 394 38 }} maximumsize = {{ 394 38 }} fontsize = {font + 6} fontsize_min = 14 align = left text = "CMP_WS_RB_TITLE" }}')
    button(lines, 3, x=406, y=0, width=52, height=button_height, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_regions_help', 'overview')",
           tooltip="CMP_WS_RB_HELP_OVERVIEW_TT", color="0.48 0.58 0.72 0.98")
    sub_gap = 8
    sub_width = (358 - sub_gap) // 2
    sub_x = 466
    button(lines, 3, x=sub_x, y=0, width=sub_width, height=button_height,
           label="CMP_RB2_SUBMODE_OPERATIONS", font=font,
           actions=["GetVariableSystem.Set('cmp_workspace_regions_tab', 'operations')",
                    "GetVariableSystem.Clear('cmp_workspace_building_category_menu_operations')"],
           tooltip="CMP_WS_RB_OPERATIONS_TT", color="0.40 0.53 0.68 0.97")
    variable_selected_line(lines, 3, x=sub_x, y=button_height - 4, width=sub_width,
                           variable="cmp_workspace_regions_tab", value="operations", default=True)
    button(lines, 3, x=sub_x + sub_width + sub_gap, y=0, width=sub_width, height=button_height,
           label="CMP_RB2_SUBMODE_STAFF", font=font,
           actions=["GetVariableSystem.Set('cmp_workspace_regions_tab', 'staffing')",
                    "GetVariableSystem.Clear('cmp_workspace_building_category_menu_staffing')"],
           tooltip="CMP_WS_RB_STAFFING_TT", color="0.40 0.53 0.68 0.97")
    variable_selected_line(lines, 3, x=sub_x + sub_width + sub_gap, y=button_height - 4,
                           width=sub_width, variable="cmp_workspace_regions_tab", value="staffing")

    operations_visible = ("[Or(Not(GetVariableSystem.Exists('cmp_workspace_regions_tab')), "
                          "GetVariableSystem.HasValue('cmp_workspace_regions_tab', 'operations'))]")
    line(lines, 3, f'widget = {{ visible = "{operations_visible}" size = {{ 864 514 }}')
    line(lines, 4, f'textbox = {{ position = {{ 4 {button_height + 2} }} size = {{ 820 26 }} maximumsize = {{ 820 26 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_RB_FLOW" }}')
    mode_y = button_height + 32
    gap = 8
    mode_width = (820 - gap * 2) // 3
    modes = [
        ("CMP_RB2_MODE_BUILDING", "building", True, f"GetScriptedGui('cmp_regions2_select_mode_building').Execute({scope})"),
        ("CMP_RB2_MODE_RESOURCE", "resource", False, f"GetScriptedGui('cmp_regions2_clear').Execute({scope})"),
        ("CMP_RB2_MODE_PRESET", "preset", False, f"GetScriptedGui('cmp_regions2_select_mode_preset').Execute({scope})"),
    ]
    for index, (label, mode, default, endpoint) in enumerate(modes):
        x = 4 + index * (mode_width + gap)
        actions = [f"GetVariableSystem.Set('cmp_workspace_regions_mode', '{mode}')"]
        if endpoint:
            actions.append(endpoint)
        button(lines, 4, x=x, y=mode_y, width=mode_width, height=button_height,
               label=label, font=font, actions=actions,
               tooltip=f"CMP_WS_RB_MODE_{mode.upper()}_TT", color="0.40 0.53 0.68 0.97")
        variable_selected_line(lines, 4, x=x, y=mode_y + button_height - 4,
                               width=mode_width, variable="cmp_workspace_regions_mode",
                               value=mode, default=default)
    content_y = mode_y + button_height + 8
    content_height = 514 - content_y
    resource_ids = set(regions["resource_capable_buildings"])
    resources = [item for item in buildings if item["id"] in resource_ids]
    render_regions_building_picker(lines, buildings, profile, y=content_y,
                                   height=content_height, mode="building",
                                   categories=categories)
    render_regions_building_picker(lines, resources, profile, y=content_y,
                                   height=content_height, mode="resource")
    render_regions_preset_picker(lines, regions, profile, y=content_y,
                                 height=content_height)
    render_regions_operations_config(lines, buildings, regions, profile, y=content_y,
                                     height=content_height)
    line(lines, 3, '}')

    line(lines, 3, 'widget = { visible = "[GetVariableSystem.HasValue(\'cmp_workspace_regions_tab\', \'staffing\')]" size = { 864 514 }')
    staffing_content_y = button_height + 42
    staffing_content_height = 514 - staffing_content_y
    line(lines, 4, f'textbox = {{ position = {{ 4 {button_height + 2} }} size = {{ 760 30 }} maximumsize = {{ 760 30 }} fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_STAFF_FLOW" }}')
    button(lines, 4, x=776, y=button_height, width=48, height=38, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_regions_help', 'staffing')",
           tooltip="CMP_WS_RB_HELP_STAFFING_TT", color="0.48 0.58 0.72 0.98")
    staffing_buildings = [b for b in staffing['buildings'] if b['status'] == 'SUPPORTED']
    render_regions_building_picker(lines, staffing_buildings, profile, y=staffing_content_y,
                                   height=staffing_content_height, mode="building",
                                   categories=staffing['categories'], always_visible=True,
                                   instance="staffing")
    render_staffing_config(lines, staffing, regions, profile, y=staffing_content_y,
                           height=staffing_content_height)
    line(lines, 3, '}')
    render_regions_help(lines, profile)
    line(lines, 2, '}')


def diplomacy_tab_visible(tab: str) -> str:
    if tab == "relations":
        return ("[Or(Not(GetVariableSystem.Exists('cmp_workspace_diplomacy_tab')), "
                "GetVariableSystem.HasValue('cmp_workspace_diplomacy_tab', 'relations'))]")
    return f"[GetVariableSystem.HasValue('cmp_workspace_diplomacy_tab', '{tab}')]"


def diplomacy_guard(kind: str) -> str:
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    country = f"GetScriptedGui('sakuya_b7_has_marked_country_check').IsShown({scope})"
    if kind == "player":
        return f"[GetScriptedGui('sakuya_b7_fx_player_independent').IsShown({scope})]"
    if kind == "home":
        home = f"GetScriptedGui('sakuya_b7_has_marked_home_state_check').IsShown({scope})"
        return f"[And({country}, {home})]"
    if kind == "foreign":
        foreign = f"GetScriptedGui('sakuya_b7_has_marked_foreign_state_check').IsShown({scope})"
        return f"[{foreign}]"
    if kind == "power_bloc":
        return f"[GetScriptedGui('cmp_politics2_bloc_target_valid').IsValid({scope})]"
    return f"[{country}]"


def diplomacy_action_button(lines: list[str], indent: int, *, x: int, y: int,
                            width: int, height: int, label: str, font: int,
                            endpoint: str, tooltip: str, guard: str = "country",
                            color: str = "0.42 0.50 0.62 0.98") -> None:
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    button(lines, indent, x=x, y=y, width=width, height=height,
           label=label, font=font,
           action=f"GetScriptedGui('{endpoint}').Execute({scope})",
           enabled_when=diplomacy_guard(guard), tooltip=tooltip, color=color)


def render_diplomacy_tabs(lines: list[str], diplomacy: dict, profile: dict, *, y: int) -> None:
    font = profile["font_size"]
    height = profile["button_height"]
    gap = 8
    width = (820 - gap * (len(diplomacy["tabs"]) - 1)) // len(diplomacy["tabs"])
    for index, tab in enumerate(diplomacy["tabs"]):
        x = 4 + index * (width + gap)
        button(lines, 3, x=x, y=y, width=width, height=height,
               label=tab["label"], font=font,
               actions=[f"GetVariableSystem.Set('cmp_workspace_diplomacy_tab', '{tab['id']}')",
                        "GetVariableSystem.Clear('cmp_workspace_diplomacy_help')",
                        "GetVariableSystem.Clear('cmp_workspace_diplomacy_confirm')"],
               tooltip=f"CMP_WS_DIP_TAB_{tab['id'].upper()}_TT",
               color="0.40 0.53 0.68 0.97")
        line(lines, 3, f'icon = {{ visible = "{diplomacy_tab_visible(tab["id"])}" position = {{ {x + 4} {y + height - 4} }} size = {{ {width - 8} 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')


def render_diplomacy_relations(lines: list[str], diplomacy: dict, profile: dict,
                               *, y: int, height: int) -> None:
    font = profile["font_size"]
    control_h = profile["button_height"]
    profile_id = profile["id"]
    line(lines, 3, f'widget = {{ visible = "{diplomacy_tab_visible("relations")}" position = {{ 4 {y} }} size = {{ 840 {height} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_diplomacy_relations_{profile_id}" size = {{ 840 {height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 820 430 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 40 }} maximumsize = {{ 730 40 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_WS_DIP_REL_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_diplomacy_help', 'relations')",
           tooltip="CMP_WS_DIP_HELP_RELATIONS_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 48 }} size = {{ 800 42 }} maximumsize = {{ 800 42 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_DIP_REL_HINT" }}')
    width = (800 - 24) // 4
    start_y = 98
    for index, action in enumerate(diplomacy["relations"]):
        row, col = divmod(index, 4)
        diplomacy_action_button(lines, 7, x=col * (width + 8), y=start_y + row * (control_h + 8),
                                width=width, height=control_h, label=action["label"], font=font,
                                endpoint=action["endpoint"], tooltip=action["tooltip"])
    obligation_y = start_y + 2 * (control_h + 8) + 14
    line(lines, 7, f'textbox = {{ position = {{ 0 {obligation_y} }} size = {{ 800 32 }} maximumsize = {{ 800 32 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_DIP_OBLIGATION_TITLE" }}')
    obligation_y += 36
    obligation_w = (800 - 8) // 2
    for index, action in enumerate(diplomacy["obligations"]):
        diplomacy_action_button(lines, 7, x=index * (obligation_w + 8), y=obligation_y,
                                width=obligation_w, height=control_h, label=action["label"], font=font,
                                endpoint=action["endpoint"], tooltip=action["tooltip"])
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_diplomacy_subjects(lines: list[str], diplomacy: dict, profile: dict,
                              *, y: int, height: int) -> None:
    font = profile["font_size"]
    control_h = profile["button_height"]
    profile_id = profile["id"]
    row_h = 30 + control_h + 10
    content_h = 122 + len(diplomacy["subject_types"]) * row_h + 2 * (control_h + 8)
    line(lines, 3, f'widget = {{ visible = "{diplomacy_tab_visible("subjects")}" position = {{ 4 {y} }} size = {{ 840 {height} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_diplomacy_subjects_{profile_id}" size = {{ 840 {height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, f'widget = {{ size = {{ 820 {content_h} }}')
    line(lines, 7, f'textbox = {{ size = {{ 730 40 }} maximumsize = {{ 730 40 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_WS_DIP_SUBJECT_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_diplomacy_help', 'subjects')",
           tooltip="CMP_WS_DIP_HELP_SUBJECTS_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 46 }} size = {{ 800 58 }} maximumsize = {{ 800 58 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_DIP_SUBJECT_WARNING" }}')
    button_w = (800 - 8) // 2
    cursor_y = 108
    for subject in diplomacy["subject_types"]:
        line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "{subject["label"]}" }}')
        action_y = cursor_y + 30
        diplomacy_action_button(lines, 7, x=0, y=action_y, width=button_w, height=control_h,
                                label="CMP_WS_DIP_SUB_FORWARD", font=font,
                                endpoint=subject["forward"], tooltip=subject["tooltip"])
        diplomacy_action_button(lines, 7, x=button_w + 8, y=action_y, width=button_w, height=control_h,
                                label="CMP_WS_DIP_SUB_REVERSE", font=font,
                                endpoint=subject["reverse"], tooltip=subject["tooltip"])
        cursor_y += row_h
    line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 32 }} maximumsize = {{ 800 32 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_DIP_AUTONOMY_TITLE" }}')
    cursor_y += 36
    action_w = (800 - 8) // 2
    for index, action in enumerate(diplomacy["subject_actions"]):
        row, col = divmod(index, 2)
        guard = "player" if action["endpoint"] == "sakuya_b7_fx_player_independent" else "country"
        diplomacy_action_button(lines, 7, x=col * (action_w + 8), y=cursor_y + row * (control_h + 8),
                                width=action_w, height=control_h, label=action["label"], font=font,
                                endpoint=action["endpoint"], tooltip=action["tooltip"], guard=guard,
                                color="0.62 0.43 0.47 0.97" if "independent" in action["endpoint"] else "0.42 0.50 0.62 0.98")
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_diplomacy_treaties(lines: list[str], diplomacy: dict, profile: dict,
                              *, y: int, height: int) -> None:
    font = profile["font_size"]
    control_h = profile["button_height"]
    profile_id = profile["id"]
    row_h = 30 + control_h + 10
    content_h = 112 + len(diplomacy["treaties"]) * row_h
    line(lines, 3, f'widget = {{ visible = "{diplomacy_tab_visible("treaties")}" position = {{ 4 {y} }} size = {{ 840 {height} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_diplomacy_treaties_{profile_id}" size = {{ 840 {height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, f'widget = {{ size = {{ 820 {content_h} }}')
    line(lines, 7, f'textbox = {{ size = {{ 730 40 }} maximumsize = {{ 730 40 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_WS_DIP_TREATY_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_diplomacy_help', 'treaties')",
           tooltip="CMP_WS_DIP_HELP_TREATIES_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 46 }} size = {{ 800 54 }} maximumsize = {{ 800 54 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_DIP_TREATY_HINT" }}')
    button_w = (800 - 8) // 2
    cursor_y = 104
    for treaty in diplomacy["treaties"]:
        line(lines, 7, f'textbox = {{ position = {{ 0 {cursor_y} }} size = {{ 800 28 }} maximumsize = {{ 800 28 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "{treaty["label"]}" }}')
        action_y = cursor_y + 30
        diplomacy_action_button(lines, 7, x=0, y=action_y, width=button_w, height=control_h,
                                label="CMP_WS_DIP_CREATE", font=font,
                                endpoint=treaty["create"], tooltip=treaty["tooltip"],
                                color="0.40 0.60 0.48 0.97")
        diplomacy_action_button(lines, 7, x=button_w + 8, y=action_y, width=button_w, height=control_h,
                                label="CMP_WS_DIP_REMOVE", font=font,
                                endpoint=treaty["remove"], tooltip=treaty["tooltip"],
                                color="0.62 0.43 0.47 0.97")
        cursor_y += row_h
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_diplomacy_sovereignty(lines: list[str], diplomacy: dict, profile: dict,
                                 *, y: int, height: int) -> None:
    font = profile["font_size"]
    control_h = profile["button_height"]
    profile_id = profile["id"]
    line(lines, 3, f'widget = {{ visible = "{diplomacy_tab_visible("sovereignty")}" position = {{ 4 {y} }} size = {{ 840 {height} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_diplomacy_sovereignty_{profile_id}" size = {{ 840 {height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 820 520 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 40 }} maximumsize = {{ 730 40 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_WS_DIP_SOV_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_diplomacy_help', 'sovereignty')",
           tooltip="CMP_WS_DIP_HELP_SOVEREIGNTY_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ position = {{ 0 46 }} size = {{ 800 62 }} maximumsize = {{ 800 62 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_DIP_SOV_WARNING" }}')
    button_w = (800 - 8) // 2
    start_y = 116
    for index, action in enumerate(diplomacy["sovereignty"]):
        row, col = divmod(index, 2)
        diplomacy_action_button(lines, 7, x=col * (button_w + 8), y=start_y + row * (control_h + 10),
                                width=button_w, height=control_h, label=action["label"], font=font,
                                endpoint=action["endpoint"], tooltip=action["tooltip"], guard=action["guard"],
                                color="0.62 0.43 0.47 0.97")
    note_y = start_y + 3 * (control_h + 10) + 12
    line(lines, 7, f'textbox = {{ position = {{ 0 {note_y} }} size = {{ 800 76 }} maximumsize = {{ 800 76 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_DIP_SOV_DEFERRED" }}')
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_diplomacy_power_bloc(lines: list[str], diplomacy: dict, profile: dict,
                                *, y: int, height: int) -> None:
    font = profile["font_size"]
    control_h = profile["button_height"]
    profile_id = profile["id"]
    line(lines, 3, f'widget = {{ visible = "{diplomacy_tab_visible("power_bloc")}" position = {{ 4 {y} }} size = {{ 840 {height} }}')
    line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_diplomacy_power_bloc_{profile_id}" size = {{ 840 {height} }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
    line(lines, 5, 'scrollwidget = {')
    line(lines, 6, 'widget = { size = { 820 660 }')
    line(lines, 7, f'textbox = {{ size = {{ 730 40 }} maximumsize = {{ 730 40 }} fontsize = {font + 3} fontsize_min = 13 align = left|nobaseline text = "CMP_WS_DIP_BLOC_TITLE" }}')
    button(lines, 7, x=744, y=0, width=56, height=44, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_diplomacy_help', 'power_bloc')",
           tooltip="CMP_WS_DIP_HELP_BLOC_TT", color="0.48 0.58 0.72 0.98")
    line(lines, 7, f'textbox = {{ visible = "{diplomacy_guard("power_bloc")}" position = {{ 0 48 }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_DIP_BLOC_READY" }}')
    line(lines, 7, f'textbox = {{ visible = "[Not({diplomacy_guard("power_bloc")[1:-1]})]" position = {{ 0 48 }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_DIP_BLOC_REQUIRED" }}')
    line(lines, 7, f'textbox = {{ position = {{ 0 82 }} size = {{ 800 30 }} maximumsize = {{ 800 30 }} fontsize = {font + 1} fontsize_min = 12 align = left text = "CMP_WS_DIP_BLOC_COHESION_TITLE" }}')
    width = (800 - 24) // 4
    scope = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
    for index, action in enumerate(diplomacy["power_bloc_safe"]):
        button(lines, 7, x=index * (width + 8), y=114,
               width=width, height=control_h, label=action["label"], font=font,
               actions=[f"GetScriptedGui('cmp_diplomacy2_feedback_clear').Execute({scope})",
                        f"GetScriptedGui('{action['endpoint']}').Execute({scope})"],
               enabled_when=diplomacy_guard("power_bloc"), tooltip=action["tooltip"],
               color="0.42 0.50 0.62 0.98")
    membership_title_y = 132 + control_h
    line(lines, 7, f'textbox = {{ position = {{ 0 {membership_title_y} }} size = {{ 800 32 }} maximumsize = {{ 800 32 }} fontsize = {font + 2} fontsize_min = 12 align = left text = "CMP_WS_DIP_BLOC_MEMBERSHIP_TITLE" }}')
    warning_y = membership_title_y + 36
    line(lines, 7, f'textbox = {{ position = {{ 0 {warning_y} }} size = {{ 800 72 }} maximumsize = {{ 800 72 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_DIP_BLOC_MEMBERSHIP_WARNING" }}')
    confirm_y = warning_y + 78
    button(lines, 7, x=0, y=confirm_y, width=800, height=control_h,
           label="CMP_WS_DIP_BLOC_CONFIRM", font=font,
           action="GetVariableSystem.Toggle('cmp_workspace_diplomacy_confirm')",
           tooltip="CMP_WS_DIP_BLOC_CONFIRM_TT", color="0.68 0.48 0.30 0.98")
    line(lines, 7, f'icon = {{ visible = "[GetVariableSystem.Exists(\'cmp_workspace_diplomacy_confirm\')]" position = {{ 3 {confirm_y + control_h - 4} }} size = {{ 794 4 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}')
    member_y = confirm_y + control_h + 10
    member_w = (800 - 8) // 2
    confirm_guard = "[GetVariableSystem.Exists('cmp_workspace_diplomacy_confirm')]"
    for index, action in enumerate(diplomacy["power_bloc_membership"]):
        button(lines, 7, x=index * (member_w + 8), y=member_y,
               width=member_w, height=control_h, label=action["label"], font=font,
               actions=[f"GetScriptedGui('{action['endpoint']}').Execute({scope})",
                        "GetVariableSystem.Clear('cmp_workspace_diplomacy_confirm')"],
               enabled_when=confirm_guard, tooltip=action["tooltip"],
               color="0.68 0.40 0.43 0.98")
    deferred_y = member_y + control_h + 18
    line(lines, 7, f'textbox = {{ position = {{ 0 {deferred_y} }} size = {{ 800 118 }} maximumsize = {{ 800 118 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_DIP_BLOC_DEFERRED" }}')
    line(lines, 6, '}')
    line(lines, 5, '}')
    line(lines, 4, '}')
    line(lines, 3, '}')


def render_diplomacy_help(lines: list[str], profile: dict) -> None:
    font = profile["font_size"]
    profile_id = profile["id"]
    topics = ["overview", "relations", "subjects", "treaties", "sovereignty", "power_bloc"]
    line(lines, 3, 'widget = { name = "cmp_workspace_diplomacy_help_card" visible = "[GetVariableSystem.Exists(\'cmp_workspace_diplomacy_help\')]" position = { 32 72 } size = { 792 420 }')
    line(lines, 4, 'icon = { size = { 792 420 } texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = { 0.045 0.055 0.075 0.998 } }')
    line(lines, 4, 'icon = { position = { 2 2 } size = { 788 416 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.98 } alwaystransparent = yes }')
    line(lines, 4, f'textbox = {{ position = {{ 20 14 }} size = {{ 680 36 }} maximumsize = {{ 680 36 }} fontsize = {font + 4} fontsize_min = 14 align = left text = "CMP_WS_DIP_HELP_TITLE" }}')
    line(lines, 4, 'close_button = { position = { 736 10 } size = { 42 42 } onclick = "[GetVariableSystem.Clear(\'cmp_workspace_diplomacy_help\')]" }')
    for topic in topics:
        if topic == "overview":
            visible = ("[Or(Not(GetVariableSystem.Exists('cmp_workspace_diplomacy_help')), "
                       "GetVariableSystem.HasValue('cmp_workspace_diplomacy_help', 'overview'))]")
        else:
            visible = f"[GetVariableSystem.HasValue('cmp_workspace_diplomacy_help', '{topic}')]"
        line(lines, 4, f'scrollarea = {{ name = "cmp_workspace_diplomacy_help_{topic}_{profile_id}" visible = "{visible}" position = {{ 20 60 }} size = {{ 752 338 }} scrollbarpolicy_horizontal = always_off scrollbar_vertical = {{ using = vertical_scrollbar }}')
        line(lines, 5, 'scrollwidget = {')
        line(lines, 6, f'textbox = {{ size = {{ 720 680 }} maximumsize = {{ 720 680 }} multiline = yes autoresize = no fontsize = {font} fontsize_min = 12 align = left text = "CMP_WS_DIP_HELP_{topic.upper()}" }}')
        line(lines, 5, '}')
        line(lines, 4, '}')
    line(lines, 3, '}')


def render_diplomacy_page(lines: list[str], diplomacy: dict, profile: dict) -> None:
    font = profile["font_size"]
    control_h = profile["button_height"]
    line(lines, 2, f'widget = {{ visible = "{page_visible("diplomacy")}" position = {{ 238 76 }} size = {{ 864 514 }}')
    line(lines, 3, f'textbox = {{ position = {{ 4 0 }} size = {{ 430 38 }} maximumsize = {{ 430 38 }} fontsize = {font + 6} fontsize_min = 14 align = left text = "CMP_WS_DIP_TITLE" }}')
    line(lines, 3, f'textbox = {{ visible = "{diplomacy_guard("country")}" position = {{ 438 4 }} size = {{ 176 30 }} maximumsize = {{ 176 30 }} fontsize = {font} fontsize_min = 12 align = right text = "CMP_WS_DIP_TARGET_READY" }}')
    line(lines, 3, f'textbox = {{ visible = "[Not({diplomacy_guard("country")[1:-1]})]" position = {{ 438 4 }} size = {{ 176 30 }} maximumsize = {{ 176 30 }} fontsize = {font} fontsize_min = 12 align = right text = "CMP_WS_DIP_TARGET_REQUIRED" }}')
    button(lines, 3, x=628, y=0, width=132, height=control_h, label="CMP_WS_DIP_TARGETS", font=font,
           actions=navigation_actions("target"), tooltip="CMP_WS_DIP_TARGETS_TT",
           color="0.45 0.62 0.82 0.98")
    button(lines, 3, x=768, y=0, width=56, height=control_h, label="CMP_WS_INFO", font=font,
           action="GetVariableSystem.Set('cmp_workspace_diplomacy_help', 'overview')",
           tooltip="CMP_WS_DIP_HELP_OVERVIEW_TT", color="0.48 0.58 0.72 0.98")
    tab_y = control_h + 8
    render_diplomacy_tabs(lines, diplomacy, profile, y=tab_y)
    content_y = tab_y + control_h + 10
    content_h = 514 - content_y
    render_diplomacy_relations(lines, diplomacy, profile, y=content_y, height=content_h)
    render_diplomacy_subjects(lines, diplomacy, profile, y=content_y, height=content_h)
    render_diplomacy_treaties(lines, diplomacy, profile, y=content_y, height=content_h)
    render_diplomacy_sovereignty(lines, diplomacy, profile, y=content_y, height=content_h)
    render_diplomacy_power_bloc(lines, diplomacy, profile, y=content_y, height=content_h)
    render_diplomacy_help(lines, profile)
    line(lines, 2, '}')


def render_footer(lines: list[str], profile: dict) -> None:
    font = profile["font_size"]
    height = min(52, profile["button_height"])
    line(lines, 2, 'icon = { position = { 222 596 } size = { 898 2 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.95 } alwaystransparent = yes }')
    line(lines, 2, f'widget = {{ visible = "{page_visible("target")}" position = {{ 238 604 }} size = {{ 864 56 }}')
    feedback = [
        ("cmp_target_core_feedback_selected", "CMP_TC_FEEDBACK_SELECTED"),
        ("cmp_target_core_feedback_group_added", "CMP_TC_FEEDBACK_ADDED"),
        ("cmp_target_core_feedback_group_removed", "CMP_TC_FEEDBACK_REMOVED"),
        ("cmp_target_core_feedback_group_cleared", "CMP_TC_FEEDBACK_GROUP_CLEARED"),
        ("cmp_target_core_feedback_transient_cleared", "CMP_TC_FEEDBACK_TRANSIENT_CLEARED"),
        ("cmp_target_core_feedback_no_marked_country", "CMP_TC_FEEDBACK_NO_COUNTRY"),
    ]
    for effect, label in feedback:
        line(lines, 3, f'textbox = {{ visible = "[GetScriptedGui(\'{effect}\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" position = {{ 0 0 }} size = {{ 620 48 }} maximumsize = {{ 620 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{label}" }}')
    button(lines, 3, x=640, y=0, width=210, height=height, label="CMP_WS_CLEAR_TRANSIENT", font=font,
           action="GetScriptedGui('cmp_target_core_clear_transient').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)",
           color="0.72 0.42 0.46 1", tooltip="CMP_TC_CLEAR_TRANSIENT_TT")
    line(lines, 2, "}")
    line(lines, 2, f'widget = {{ visible = "{page_visible("interface")}" position = {{ 238 604 }} size = {{ 864 56 }} textbox = {{ size = {{ 850 48 }} maximumsize = {{ 850 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_WS_INTERFACE_FOOTER" }} }}')
    line(lines, 2, f'widget = {{ visible = "{page_visible("economy")}" position = {{ 238 604 }} size = {{ 864 56 }}')
    line(lines, 3, f'textbox = {{ size = {{ 850 48 }} maximumsize = {{ 850 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_WS_ECONOMY_FOOTER" }}')
    feedback = [
        ("applied", "CMP_ECO2_FB_APPLIED"), ("reset", "CMP_ECO2_FB_RESET"),
        ("treasury", "CMP_ECO2_FB_TREASURY"), ("investment", "CMP_ECO2_FB_INVESTMENT"),
        ("debt", "CMP_ECO2_FB_DEBT"), ("bankruptcy", "CMP_ECO2_FB_BANKRUPTCY"),
        ("rescue", "CMP_ECO2_FB_RESCUE"), ("policy_on", "CMP_ECO2_FB_POLICY_ON"),
        ("policy_off", "CMP_ECO2_FB_POLICY_OFF"), ("no_target", "CMP_ECO2_FB_NO_TARGET"),
        ("wrong_scope", "CMP_ECO2_FB_WRONG_SCOPE"),
    ]
    for effect, label in feedback:
        line(lines, 3, f'textbox = {{ visible = "[GetScriptedGui(\'cmp_economy2_feedback_{effect}\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" size = {{ 850 48 }} maximumsize = {{ 850 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{label}" }}')
    line(lines, 2, "}")
    line(lines, 2, f'widget = {{ visible = "{page_visible("regions")}" position = {{ 238 604 }} size = {{ 864 56 }}')
    operations_visible = ("[Or(Not(GetVariableSystem.Exists('cmp_workspace_regions_tab')), "
                          "GetVariableSystem.HasValue('cmp_workspace_regions_tab', 'operations'))]")
    line(lines, 3, f'widget = {{ visible = "{operations_visible}" size = {{ 864 56 }}')
    region_feedback = [
        ("cmp_regions2_result_success", "CMP_RB2_RESULT_SUCCESS"),
        ("cmp_regions2_result_no_target", "CMP_RB2_RESULT_NO_TARGET"),
        ("cmp_regions2_result_partial", "CMP_RB2_RESULT_PARTIAL"),
        ("cmp_regions2_result_add_limit", "CMP_RB2_RESULT_ADD_LIMIT"),
        ("cmp_regions2_result_failed", "CMP_RB2_RESULT_FAILED"),
        ("cmp_regions2_result_blocked", "CMP_RB2_RESULT_BLOCKED"),
        ("cmp_regions2_result_unsafe", "CMP_RB2_RESULT_UNSAFE"),
    ]
    region_predicates = [f"GetScriptedGui('{effect}').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)" for effect, _ in region_feedback]
    region_any = region_predicates[0]
    for predicate in region_predicates[1:]:
        region_any = f"Or({region_any}, {predicate})"
    line(lines, 4, f'textbox = {{ visible = "[Not({region_any})]" size = {{ 672 48 }} maximumsize = {{ 672 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_WS_RB_FOOTER_IDLE" }}')
    for effect, label in region_feedback:
        line(lines, 4, f'textbox = {{ visible = "[GetScriptedGui(\'{effect}\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" size = {{ 672 48 }} maximumsize = {{ 672 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{label}" }}')
    button(lines, 4, x=690, y=0, width=160, height=height,
           label="CMP_RB2_CLEAR", font=font,
           action="GetScriptedGui('cmp_regions2_clear').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)",
           tooltip="CMP_WS_RB_CLEAR_TT", color="0.68 0.40 0.43 0.96")
    line(lines, 3, "}")
    line(lines, 3, 'widget = { visible = "[GetVariableSystem.HasValue(\'cmp_workspace_regions_tab\', \'staffing\')]" size = { 864 56 }')
    staffing_feedback = [
        ("cmp_staffing_result_applied", "CMP_STAFF_RESULT_APPLIED"),
        ("cmp_staffing_result_no_below_target", "CMP_STAFF_RESULT_NO_BELOW"),
    ]
    staffing_any = f"Or(GetScriptedGui('{staffing_feedback[0][0]}').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End), GetScriptedGui('{staffing_feedback[1][0]}').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End))"
    line(lines, 4, f'textbox = {{ visible = "[Not({staffing_any})]" size = {{ 850 48 }} maximumsize = {{ 850 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_WS_STAFF_FOOTER_IDLE" }}')
    for effect, label in staffing_feedback:
        line(lines, 4, f'textbox = {{ visible = "[GetScriptedGui(\'{effect}\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" size = {{ 850 48 }} maximumsize = {{ 850 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{label}" }}')
    line(lines, 3, "}")
    line(lines, 2, "}")
    line(lines, 2, f'widget = {{ visible = "{page_visible("population")}" position = {{ 238 604 }} size = {{ 864 56 }}')
    population_feedback = [
        ("cmp_pop2_feedback_added", "CMP_POP2_FB_ADDED"),
        ("cmp_pop2_feedback_removed", "CMP_POP2_FB_REMOVED"),
        ("cmp_pop2_feedback_literacy", "CMP_POP2_FB_LITERACY"),
        ("cmp_pop2_feedback_profession", "CMP_POP2_FB_PROF"),
        ("cmp_pop2_feedback_qualification", "CMP_POP2_FB_QUAL"),
        ("cmp_pop2_feedback_wealth", "CMP_POP2_FB_WEALTH"),
        ("cmp_pop2_feedback_neutralized", "CMP_POP2_FB_NEUTRAL"),
        ("cmp_pop2_feedback_assimilated", "CMP_POP2_FB_ASSIM"),
        ("cmp_pop2_feedback_religion", "CMP_POP2_FB_RELIGION"),
        ("cmp_pop2_feedback_society_clear", "CMP_POP2_FB_SOC_CLEAR"),
        ("cmp_pop2_feedback_industrial", "CMP_POP2_FB_INDUSTRIAL"),
        ("cmp_pop2_feedback_educated", "CMP_POP2_FB_EDUCATED"),
        ("cmp_pop2_feedback_stable", "CMP_POP2_FB_STABLE"),
        ("cmp_pop2_feedback_loyalists", "CMP_POP2_FB_LOYAL"),
        ("cmp_pop2_feedback_radicals", "CMP_POP2_FB_RADICAL"),
        ("cmp_pop2_feedback_radicals_down", "CMP_POP2_FB_RADICAL_DOWN"),
        ("cmp_pop2_feedback_migration", "CMP_POP2_FB_MIGRATION"),
        ("cmp_pop2_feedback_workforce", "CMP_POP2_FB_WORKFORCE"),
        ("cmp_pop2_feedback_no_target", "CMP_POP2_FB_NO_TARGET"),
        ("cmp_pop2_feedback_wrong_target", "CMP_POP2_FB_WRONG_TARGET"),
    ]
    population_predicates = [f"GetScriptedGui('{effect}').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)" for effect, _ in population_feedback]
    population_any = population_predicates[0]
    for predicate in population_predicates[1:]:
        population_any = f"Or({population_any}, {predicate})"
    line(lines, 3, f'textbox = {{ visible = "[Not({population_any})]" size = {{ 850 48 }} maximumsize = {{ 850 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_WS_POP_FOOTER_IDLE" }}')
    for effect, label in population_feedback:
        line(lines, 3, f'textbox = {{ visible = "[GetScriptedGui(\'{effect}\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" size = {{ 850 48 }} maximumsize = {{ 850 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{label}" }}')
    line(lines, 2, "}")
    line(lines, 2, f'widget = {{ visible = "{page_visible("politics")}" position = {{ 238 604 }} size = {{ 864 56 }}')
    politics_feedback = [
        ("cmp_politics2_feedback_applied", "CMP_POL2_FB_APPLIED"),
        ("cmp_politics2_feedback_country_required", "CMP_POL2_FB_COUNTRY"),
        ("cmp_politics2_feedback_character_required", "CMP_POL2_FB_CHARACTER"),
        ("cmp_politics2_feedback_no_eligible", "CMP_POL2_FB_NO_ELIGIBLE"),
        ("cmp_politics2_feedback_bloc_required", "CMP_POL2_FB_BLOC"),
    ]
    politics_predicates = [f"GetScriptedGui('{effect}').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)" for effect, _ in politics_feedback]
    politics_any = politics_predicates[0]
    for predicate in politics_predicates[1:]:
        politics_any = f"Or({politics_any}, {predicate})"
    line(lines, 3, f'textbox = {{ visible = "[Not({politics_any})]" size = {{ 672 48 }} maximumsize = {{ 672 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_WS_POL_FOOTER_IDLE" }}')
    for effect, label in politics_feedback:
        line(lines, 3, f'textbox = {{ visible = "[GetScriptedGui(\'{effect}\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" size = {{ 672 48 }} maximumsize = {{ 672 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{label}" }}')
    button(lines, 3, x=690, y=0, width=160, height=height,
           label="CMP_WS_POL_CLEAR", font=font,
           action="GetScriptedGui('cmp_politics2_feedback_clear').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)",
           tooltip="CMP_WS_POL_CLEAR_TT", color="0.68 0.40 0.43 0.96")
    line(lines, 2, "}")
    line(lines, 2, f'widget = {{ visible = "{page_visible("diplomacy")}" position = {{ 238 604 }} size = {{ 864 56 }}')
    bloc_visible = diplomacy_tab_visible("power_bloc")
    line(lines, 3, f'widget = {{ visible = "[Not({bloc_visible[1:-1]})]" size = {{ 864 56 }}')
    diplomacy_feedback = [
        ("cmp_b7_feedback_success_check", "CMP_B7_STATUS_OK"),
        ("cmp_b7_feedback_no_target_check", "CMP_B7_STATUS_NO_TARGET"),
        ("cmp_b7_feedback_subject_conflict_check", "CMP_B7_STATUS_SUBJECT_CONFLICT"),
        ("cmp_b7_feedback_subject_invalid_check", "CMP_B7_STATUS_SUBJECT_INVALID"),
        ("cmp_b7_feedback_treaty_invalid_check", "CMP_B7_STATUS_TREATY_INVALID"),
        ("cmp_b7_feedback_no_matching_treaty_check", "CMP_B7_STATUS_NO_TREATY"),
        ("cmp_b7_feedback_not_subject_check", "CMP_B7_STATUS_NOT_SUBJECT"),
        ("cmp_b7_feedback_state_transfer_failed_check", "CMP_B7_STATUS_STATE_TRANSFER_FAILED"),
        ("cmp_b7_feedback_treaty_port_attempted_check", "CMP_B7_STATUS_TREATY_PORT_ATTEMPTED"),
    ]
    diplomacy_predicates = [f"GetScriptedGui('{effect}').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)" for effect, _ in diplomacy_feedback]
    diplomacy_any = diplomacy_predicates[0]
    for predicate in diplomacy_predicates[1:]:
        diplomacy_any = f"Or({diplomacy_any}, {predicate})"
    line(lines, 4, f'textbox = {{ visible = "[Not({diplomacy_any})]" size = {{ 672 48 }} maximumsize = {{ 672 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_WS_DIP_FOOTER_IDLE" }}')
    for effect, label in diplomacy_feedback:
        line(lines, 4, f'textbox = {{ visible = "[GetScriptedGui(\'{effect}\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" size = {{ 672 48 }} maximumsize = {{ 672 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{label}" }}')
    button(lines, 4, x=690, y=0, width=160, height=height,
           label="CMP_WS_DIP_CLEAR", font=font,
           action="GetScriptedGui('cmp_b7_feedback_clear').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)",
           tooltip="CMP_WS_DIP_CLEAR_TT", color="0.68 0.40 0.43 0.96")
    line(lines, 3, "}")
    line(lines, 3, f'widget = {{ visible = "{bloc_visible}" size = {{ 864 56 }}')
    bloc_feedback = [
        ("cmp_diplomacy2_feedback_joined", "CMP_WS_DIP_BLOC_FB_JOINED"),
        ("cmp_diplomacy2_feedback_bloc_required", "CMP_WS_DIP_BLOC_FB_NO_BLOC"),
        ("cmp_diplomacy2_feedback_country_required", "CMP_WS_DIP_BLOC_FB_NO_COUNTRY"),
        ("cmp_diplomacy2_feedback_already_member", "CMP_WS_DIP_BLOC_FB_ALREADY"),
        ("cmp_diplomacy2_feedback_join_failed", "CMP_WS_DIP_BLOC_FB_FAILED"),
        ("cmp_politics2_feedback_applied", "CMP_POL2_FB_APPLIED"),
        ("cmp_politics2_feedback_bloc_required", "CMP_POL2_FB_BLOC"),
    ]
    bloc_predicates = [f"GetScriptedGui('{effect}').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)" for effect, _ in bloc_feedback]
    bloc_any = bloc_predicates[0]
    for predicate in bloc_predicates[1:]:
        bloc_any = f"Or({bloc_any}, {predicate})"
    line(lines, 4, f'textbox = {{ visible = "[Not({bloc_any})]" size = {{ 672 48 }} maximumsize = {{ 672 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "CMP_WS_DIP_BLOC_FOOTER_IDLE" }}')
    for effect, label in bloc_feedback:
        line(lines, 4, f'textbox = {{ visible = "[GetScriptedGui(\'{effect}\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" size = {{ 672 48 }} maximumsize = {{ 672 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{label}" }}')
    button(lines, 4, x=690, y=0, width=160, height=height,
           label="CMP_WS_DIP_CLEAR", font=font,
           actions=["GetScriptedGui('cmp_politics2_feedback_clear').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)",
                    "GetScriptedGui('cmp_diplomacy2_feedback_clear').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)",
                    "GetVariableSystem.Clear('cmp_workspace_diplomacy_confirm')"],
           tooltip="CMP_WS_DIP_CLEAR_TT", color="0.68 0.40 0.43 0.96")
    line(lines, 3, "}")
    line(lines, 2, "}")
    line(lines, 2, f'widget = {{ visible = "{page_visible("military")}" position = {{ 238 604 }} size = {{ 864 56 }}')
    sections = [
        (military_tab_visible("army_builder"), "CMP_WS_MIL_FOOTER_IDLE_ARMY", [
            ("cmp_army_builder_result_created_check", "CMP_ARMY_BUILDER_RESULT_OK"),
            ("cmp_army_builder_result_failed_check", "CMP_ARMY_BUILDER_RESULT_FAIL"),
        ]),
        (f"[And({military_tab_visible('army_templates')[1:-1]}, {military_subtab_visible('cmp_workspace_army_template_tab', 'quick', 'quick')[1:-1]})]", "CMP_WS_MIL_FOOTER_IDLE_TEMPLATE", [
            ("cmp_army_builder_result_created_check", "CMP_ARMY_BUILDER_RESULT_OK"),
            ("cmp_army_builder_result_failed_check", "CMP_ARMY_BUILDER_RESULT_FAIL"),
        ]),
        (f"[And({military_tab_visible('army_templates')[1:-1]}, {military_subtab_visible('cmp_workspace_army_template_tab', 'mixed', 'quick')[1:-1]})]", "CMP_WS_MIL_FOOTER_IDLE_TEMPLATE", [
            ("cmp_army_mixed_result_created", "CMP_ARMY_MIXED_RESULT_OK"),
            ("cmp_army_mixed_result_failed", "CMP_ARMY_MIXED_RESULT_FAIL"),
        ]),
        (f"[And({military_tab_visible('army_templates')[1:-1]}, {military_subtab_visible('cmp_workspace_army_template_tab', 'designer', 'quick')[1:-1]})]", "CMP_WS_MIL_FOOTER_IDLE_TEMPLATE", [
            ("cmp_army_designer_result_created", "CMP_ARMY_DESIGNER_OK"),
            ("cmp_army_designer_result_failed", "CMP_ARMY_DESIGNER_FAIL"),
        ]),
        (f"[And({military_tab_visible('army_templates')[1:-1]}, {military_subtab_visible('cmp_workspace_army_template_tab', 'marines', 'quick')[1:-1]})]", "CMP_WS_MIL_FOOTER_IDLE_MARINES", [
            ("cmp_army_amphib_result_created", "CMP_ARMY_AMPH_OK"),
            ("cmp_army_amphib_result_failed", "CMP_ARMY_AMPH_FAIL"),
        ]),
        (military_tab_visible("army_controls"), "CMP_WS_MIL_FOOTER_IDLE_CONTROLS", [
            ("cmp_army_controls_result_applied", "CMP_ARMY_CONTROL_RESULT_APPLIED"),
            ("cmp_army_controls_result_reset", "CMP_ARMY_CONTROL_RESULT_RESET"),
            ("cmp_army_controls_result_preset", "CMP_ARMY_CONTROL_RESULT_PRESET"),
            ("cmp_army_controls_result_failed", "CMP_ARMY_CONTROL_RESULT_FAILED"),
        ]),
        (f"[And({military_tab_visible('fleet_builder')[1:-1]}, {military_subtab_visible('cmp_workspace_fleet_builder_mode', 'new', 'new')[1:-1]})]", "CMP_WS_MIL_FOOTER_IDLE_FLEET", [
            ("cmp_navy18_result_created", "CMP_NAVY18_RESULT_CREATED"),
            ("cmp_navy18_result_preset", "CMP_NAVY18_RESULT_PRESET"),
            ("cmp_navy18_result_failed", "CMP_NAVY18_RESULT_FAIL"),
        ]),
        (f"[And({military_tab_visible('fleet_builder')[1:-1]}, {military_subtab_visible('cmp_workspace_fleet_builder_mode', 'existing', 'new')[1:-1]})]", "CMP_WS_MIL_FOOTER_IDLE_FLEET", [
            ("cmp_fleet_builder_result_created", "CMP_FLEET_RESULT_OK"),
            ("cmp_fleet_builder_result_preset", "CMP_FLEET_RESULT_PRESET"),
            ("cmp_fleet_builder_result_failed", "CMP_FLEET_RESULT_FAIL"),
        ]),
        (f"[And({military_tab_visible('fleet_templates')[1:-1]}, {military_subtab_visible('cmp_workspace_fleet_template_tab', 'designer', 'designer')[1:-1]})]", "CMP_WS_MIL_FOOTER_IDLE_FLEET_TEMPLATE", [
            ("cmp_fleet_designer_result_ok", "CMP_FD_RESULT_OK"),
            ("cmp_fleet_designer_result_fail", "CMP_FD_RESULT_FAIL"),
        ]),
        (f"[And({military_tab_visible('fleet_templates')[1:-1]}, {military_subtab_visible('cmp_workspace_fleet_template_tab', 'taskforce', 'designer')[1:-1]})]", "CMP_WS_MIL_FOOTER_IDLE_TASKFORCE", [
            ("cmp_fleet_builder_result_taskforce", "CMP_TASKFORCE_RESULT"),
            ("cmp_fleet_builder_result_failed", "CMP_FLEET_RESULT_FAIL"),
        ]),
    ]
    for visible, idle, feedback in sections:
        line(lines, 3, f'widget = {{ visible = "{visible}" size = {{ 864 56 }}')
        predicates = [f"GetScriptedGui('{effect}').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)" for effect, _ in feedback]
        any_result = predicates[0]
        for predicate in predicates[1:]:
            any_result = f"Or({any_result}, {predicate})"
        line(lines, 4, f'textbox = {{ visible = "[Not({any_result})]" size = {{ 850 48 }} maximumsize = {{ 850 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{idle}" }}')
        for effect, label in feedback:
            line(lines, 4, f'textbox = {{ visible = "[GetScriptedGui(\'{effect}\').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" size = {{ 850 48 }} maximumsize = {{ 850 48 }} fontsize = {font} fontsize_min = 12 align = left|nobaseline text = "{label}" }}')
        line(lines, 3, '}')
    line(lines, 2, '}')


def render_profile(registry: dict, economy: dict, buildings: list[dict], staffing: dict, regions: dict,
                   population: dict, politics: dict, diplomacy: dict, units: list[dict], ships: list[dict],
                   fleet: dict, navy18: dict, profile: dict) -> str:
    profile_id = profile["id"]
    if profile_id == "standard":
        visible = "[Or(Not(GetVariableSystem.Exists('cmp_ui_scale_profile')), GetVariableSystem.HasValue('cmp_ui_scale_profile', 'standard'))]"
    else:
        visible = f"[GetVariableSystem.HasValue('cmp_ui_scale_profile', '{profile_id}')]"
    lines: list[str] = []
    line(lines, 1, f'widget = {{ name = "cmp_workspace_shell_{profile_id}" visible = "{visible}" size = {{ 1120 660 }}')
    line(lines, 2, 'icon = { size = { 1120 660 } texture = "gfx/interface/backgrounds/big_header_pattern.dds" color = { 0.055 0.065 0.085 0.992 } }')
    line(lines, 2, 'icon = { position = { 2 2 } size = { 1116 656 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.16 0.19 0.25 0.96 } alwaystransparent = yes }')
    line(lines, 2, 'icon = { position = { 220 66 } size = { 2 530 } texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = { 0.35 0.42 0.52 0.95 } alwaystransparent = yes }')
    line(lines, 2, f'textbox = {{ position = {{ 20 14 }} size = {{ 620 38 }} maximumsize = {{ 620 38 }} fontsize = {profile["font_size"] + 8} fontsize_min = 16 align = left text = "CMP_WS_TITLE" }}')
    line(lines, 2, f'textbox = {{ position = {{ 654 17 }} size = {{ 224 34 }} maximumsize = {{ 224 34 }} fontsize = {profile["font_size"]} fontsize_min = 12 align = right text = "{profile["label"]}" }}')
    button(lines, 2, x=888, y=10, width=80, height=44, label="CMP_WS_HOME", font=profile["font_size"],
           actions=reset_view_actions(), tooltip="CMP_WS_HOME_TT",
           color="0.40 0.49 0.62 0.98", name=f"cmp_workspace_home_{profile_id}")
    button(lines, 2, x=976, y=10, width=80, height=44, label="CMP_WS_HELP_TITLE", font=profile["font_size"],
           actions=clear_variable_actions(DOMAIN_HELP_VARIABLES) + ["GetVariableSystem.Set('cmp_workspace_global_help', 'open')"],
           tooltip="CMP_WS_GLOBAL_HELP_TT", color="0.48 0.58 0.72 0.98",
           name=f"cmp_workspace_global_help_{profile_id}")
    close_actions = close_help_actions() + ["GetVariableSystem.Clear('cmp_workspace_building_category_menu_operations')",
                                            "GetVariableSystem.Clear('cmp_workspace_building_category_menu_staffing')",
                                            "GetVariableSystem.Clear('cmp_workspace_diplomacy_confirm')",
                                            "GetVariableSystem.Clear('cmp_workspace_shell')"]
    close_action_text = ''.join(f' onclick = "[{action}]"' for action in close_actions)
    line(lines, 2, f'close_button = {{ position = {{ 1068 10 }} size = {{ 44 44 }}{close_action_text} shortcut = "close_window" }}')
    render_navigation(lines, profile)
    render_target_page(lines, registry, profile)
    render_economy_page(lines, economy, profile)
    render_regions_page(lines, buildings, staffing, regions, registry["building_categories"], profile)
    render_population_page(lines, population, profile)
    render_politics_page(lines, politics, profile)
    render_diplomacy_page(lines, diplomacy, profile)
    render_military_page(lines, units, ships, fleet, navy18, profile)
    render_interface_page(lines, registry, profile)
    render_global_help(lines, profile)
    render_footer(lines, profile)
    line(lines, 1, "}")
    return "\n".join(lines)


def render(registry: dict, economy: dict, buildings: list[dict], staffing: dict, regions: dict,
           population: dict, politics: dict, diplomacy: dict, units: list[dict], ships: list[dict],
           fleet: dict, navy18: dict) -> str:
    sections = [START, '    widget = { name = "cmp_workspace_shell" visible = "[GetVariableSystem.Exists(\'cmp_workspace_shell\')]" position = { 40 30 } size = { 1120 660 }']
    sections.extend(render_profile(registry, economy, buildings, staffing, regions, population, politics, diplomacy,
                                   units, ships, fleet, navy18, profile)
                    for profile in registry["profiles"])
    sections.extend(["    }", END, ""])
    return "\n".join(sections)


def inject(gui_text: str, block: str) -> str:
    if START in gui_text and END in gui_text:
        before, rest = gui_text.split(START, 1)
        _, after = rest.split(END, 1)
        return before + block.rstrip("\n") + after
    if INSERT_BEFORE not in gui_text:
        raise RuntimeError(f"insertion anchor missing: {INSERT_BEFORE}")
    return gui_text.replace(INSERT_BEFORE, block + "\n" + INSERT_BEFORE, 1)


def inject_launcher(gui_text: str, launcher: str) -> str:
    if LAUNCHER_START in gui_text and LAUNCHER_END in gui_text:
        before, rest = gui_text.split(LAUNCHER_START, 1)
        _, after = rest.split(LAUNCHER_END, 1)
        return before + launcher.strip() + after
    if LEGACY_TRAY_START not in gui_text or LEGACY_TRAY_END not in gui_text:
        raise RuntimeError("legacy tray boundaries missing")
    before, rest = gui_text.split(LEGACY_TRAY_START, 1)
    _, after = rest.split(LEGACY_TRAY_END, 1)
    return before + launcher + "\n" + LEGACY_TRAY_END + after


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the beta16-pre2 Diplomacy & Sovereignty workspace shell and inject it into the main GUI.")
    parser.add_argument("--check", action="store_true", help="fail if generated artifacts are stale")
    args = parser.parse_args()
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    economy = json.loads(ECONOMY_REGISTRY.read_text(encoding="utf-8"))
    buildings = json.loads(BUILDINGS_REGISTRY.read_text(encoding="utf-8"))["buildings"]
    staffing = json.loads(STAFFING_REGISTRY.read_text(encoding="utf-8"))
    regions = json.loads(REGIONS_REGISTRY.read_text(encoding="utf-8"))
    population = json.loads(POPULATION_REGISTRY.read_text(encoding="utf-8"))
    politics = json.loads(POLITICS_REGISTRY.read_text(encoding="utf-8"))
    diplomacy = json.loads(DIPLOMACY_REGISTRY.read_text(encoding="utf-8"))
    units = json.loads(LAND_UNITS_REGISTRY.read_text(encoding="utf-8"))["units"]
    ships = json.loads(SHIPS_REGISTRY.read_text(encoding="utf-8"))["ships"]
    fleet = json.loads(FLEET_REGISTRY.read_text(encoding="utf-8"))
    navy18 = json.loads(NAVY18_REGISTRY.read_text(encoding="utf-8"))
    block = render(registry, economy, buildings, staffing, regions, population, politics, diplomacy,
                   units, ships, fleet, navy18)
    launcher = render_launcher()
    gui_text = GUI.read_text(encoding="utf-8-sig")
    expected_gui = inject(inject_launcher(gui_text, launcher), block)

    if args.check:
        failures = []
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != block:
            failures.append(str(OUTPUT.relative_to(ROOT)))
        if gui_text != expected_gui:
            failures.append(str(GUI.relative_to(ROOT)))
        if failures:
            print("STALE: " + ", ".join(failures), file=sys.stderr)
            return 1
        print("PASS: workspace shell artifacts are deterministic")
        return 0

    OUTPUT.write_text(block, encoding="utf-8")
    GUI.write_text(expected_gui, encoding="utf-8-sig")
    print(f"generated {OUTPUT.relative_to(ROOT)} and updated {GUI.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
