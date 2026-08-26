#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/'registry/politics2.json').read_text(encoding='utf-8'))

BEGIN='# CMP_POLITICS2_BEGIN popup'
END='# CMP_POLITICS2_END popup'
OPEN_BEGIN='# CMP_POLITICS2_OPEN_BEGIN'
OPEN_END='# CMP_POLITICS2_OPEN_END'


def write(path:Path,text:str):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8-sig')


def country_route(name:str, local_body:str, success:int=1, noeligible:int=-3):
    local=f"cmp_politics2_local_{name}_effect = {{\n{local_body}\n}}\n\n"
    wrap=f'''cmp_politics2_{name}_effect = {{
    remove_variable = cmp_politics2_op_found
    if = {{
        limit = {{ OR = {{ NOT = {{ has_variable = cmp_target_core_mode }} var:cmp_target_core_mode = 1 }} }}
        cmp_politics2_local_{name}_effect = yes
    }}
    else_if = {{
        limit = {{ var:cmp_target_core_mode = 2 }}
        every_country = {{ limit = {{ has_variable = sakuya_mark_country_target }} cmp_politics2_local_{name}_effect = yes }}
    }}
    else_if = {{
        limit = {{ var:cmp_target_core_mode = 3 }}
        every_country = {{ limit = {{ has_variable = cmp_target_group_a_member }} cmp_politics2_local_{name}_effect = yes }}
    }}
    else_if = {{
        limit = {{ var:cmp_target_core_mode = 4 }}
        every_country = {{ limit = {{ has_variable = cmp_target_group_b_member }} cmp_politics2_local_{name}_effect = yes }}
    }}
    else_if = {{
        limit = {{ var:cmp_target_core_mode = 5 }}
        every_country = {{ limit = {{ has_variable = cmp_target_group_c_member }} cmp_politics2_local_{name}_effect = yes }}
    }}
    if = {{
        limit = {{ has_variable = cmp_politics2_op_found }}
        set_variable = {{ name = cmp_politics2_feedback value = {success} }}
    }}
    else = {{ set_variable = {{ name = cmp_politics2_feedback value = {noeligible} }} }}
    remove_variable = cmp_politics2_op_found
}}

'''
    return local+wrap


def char_action(name:str, body:str, commander_only=False):
    extra=' OR = { has_role_of_type = general has_role_of_type = admiral }' if commander_only else ''
    local=f'''cmp_politics2_char_{name}_local_effect = {{
    if = {{
        limit = {{ has_variable = sakuya_mark_character_target{extra} }}
{body}
        root = {{ set_variable = cmp_politics2_op_found }}
    }}
}}

'''
    wrap=f'''cmp_politics2_char_{name}_effect = {{
    remove_variable = cmp_politics2_op_found
    if = {{
        limit = {{ var:cmp_target_core_mode = 9 }}
        every_country = {{ every_scope_character = {{ cmp_politics2_char_{name}_local_effect = yes }} }}
        every_character_in_exile_pool = {{ cmp_politics2_char_{name}_local_effect = yes }}
    }}
    if = {{ limit = {{ has_variable = cmp_politics2_op_found }} set_variable = {{ name = cmp_politics2_feedback value = 1 }} }}
    else = {{ set_variable = {{ name = cmp_politics2_feedback value = -2 }} }}
    remove_variable = cmp_politics2_op_found
}}

'''
    return local+wrap


def gen_modifiers():
    L=['# Cheat Menu Pro v0.3 beta15 - Politics & Characters 2.0\n']
    L += [
'''cmp_politics2_legitimacy = { icon = "gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds" country_legitimacy_base_add = 1 }''',
'''cmp_politics2_authority = { icon = "gfx/interface/icons/timed_modifier_icons/modifier_fist_positive.dds" country_authority_mult = 1 }''',
'''cmp_politics2_bureaucracy = { icon = "gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds" country_bureaucracy_mult = 1 }''',
'''cmp_politics2_influence = { icon = "gfx/interface/icons/timed_modifier_icons/modifier_flag_positive.dds" country_influence_mult = 1 }''',
'''cmp_politics2_character_health = { icon = "gfx/interface/icons/timed_modifier_icons/modifier_statue_positive.dds" character_health_add = 1 }''',
'''cmp_politics2_character_popularity = { icon = "gfx/interface/icons/timed_modifier_icons/modifier_statue_positive.dds" character_popularity_add = 1 }'''
    ]
    for ig in CFG['interest_groups']:
        k=ig['modifier_key']; i=ig['id']
        L.append(f'''cmp_politics2_ig_{i}_approval = {{ icon = "gfx/interface/icons/timed_modifier_icons/modifier_fist_positive.dds" interest_group_{k}_approval_add = 1 }}''')
        L.append(f'''cmp_politics2_ig_{i}_pol_str = {{ icon = "gfx/interface/icons/timed_modifier_icons/modifier_flag_positive.dds" interest_group_{k}_pol_str_mult = 1 }}''')
    write(ROOT/'common/static_modifiers/cmp_politics2_modifiers.txt','\n'.join(L)+'\n')


def gen_effects():
    L=['# Cheat Menu Pro v0.3 beta15 - Politics & Characters 2.0 effects\n\ncmp_politics2_feedback_clear_effect = { remove_variable = cmp_politics2_feedback }\n\n']
    # Government selected parameter + value.
    branches=[]
    params=[('legitimacy','cmp_politics2_legitimacy',1.0),('authority','cmp_politics2_authority',0.01),('bureaucracy','cmp_politics2_bureaucracy',0.01),('influence','cmp_politics2_influence',0.01)]
    vals=[10,25,50,100]
    for pi,(pid,mod,scale) in enumerate(params,1):
        for v in vals:
            mult=v*scale
            branches.append(f'''    if = {{ limit = {{ root.var:cmp_politics2_gov_param = {pi} root.var:cmp_politics2_gov_value = {v} }} remove_modifier = {mod} add_modifier = {{ name = {mod} multiplier = {mult:g} }} root = {{ set_variable = cmp_politics2_op_found }} }}''')
    L.append(country_route('gov_apply','\n'.join(branches)))
    reset='''    remove_modifier = cmp_politics2_legitimacy
    remove_modifier = cmp_politics2_authority
    remove_modifier = cmp_politics2_bureaucracy
    remove_modifier = cmp_politics2_influence
    root = { set_variable = cmp_politics2_op_found }'''
    L.append(country_route('gov_reset',reset))

    # Institution set: selected institution and selected level.
    inst_lines=[]
    for idx,inst in enumerate(CFG['institutions'],1):
        levels=[]
        for level in range(1,6):
            levels.append(f'''            if = {{ limit = {{ root.var:cmp_politics2_inst_level = {level} }} set_institution_investment_level = {{ institution = {inst['key']} level = {level} }} root = {{ set_variable = cmp_politics2_op_found }} }}''')
        inst_lines.append(f'''    if = {{
        limit = {{ root.var:cmp_politics2_inst = {idx} has_institution = {inst['key']} }}
{chr(10).join(levels)}
    }}''')
    L.append(country_route('institution_apply','\n'.join(inst_lines)))

    # Character actions.
    L.append(char_action('immortal_on','        set_character_immortal = yes'))
    L.append(char_action('immortal_off','        set_character_immortal = no'))
    for val in [0.05,0.2,1.0]:
        sid=str(val).replace('.','p')
        L.append(char_action(f'health_{sid}',f'''        remove_modifier = cmp_politics2_character_health
        add_modifier = {{ name = cmp_politics2_character_health multiplier = {val:g} }}'''))
    L.append(char_action('health_reset','        remove_modifier = cmp_politics2_character_health'))
    for val in [5,25,100]:
        L.append(char_action(f'popularity_{val}',f'''        remove_modifier = cmp_politics2_character_popularity
        add_modifier = {{ name = cmp_politics2_character_popularity multiplier = {val} }}'''))
    L.append(char_action('popularity_reset','        remove_modifier = cmp_politics2_character_popularity'))
    for rank in range(1,6):
        L.append(char_action(f'rank_{rank}',f'        set_commander_rank = {rank}',True))
    for role in ['general','admiral']:
        db_role=f'character_role_{role}'
        L.append(char_action(f'role_{role}_add',f'        add_character_role = {db_role}'))
        L.append(char_action(f'role_{role}_remove',f'        remove_character_role = {db_role}'))
    for tr in CFG['traits']:
        tid=tr['id']
        L.append(char_action(f'trait_{tid}_add',f'''        if = {{ limit = {{ NOT = {{ has_trait = {tid} }} }} add_trait = {tid} }}'''))
        L.append(char_action(f'trait_{tid}_remove',f'''        if = {{ limit = {{ has_trait = {tid} }} remove_trait = {tid} }}'''))

    # Interest-group selected type operations on target countries.
    def ig_local(kind,value):
        lines=[]
        for idx,ig in enumerate(CFG['interest_groups'],1):
            mod=f"cmp_politics2_ig_{ig['id']}_{'approval' if kind=='approval' else 'pol_str'}"
            lines.append(f'''    if = {{ limit = {{ root = {{ has_variable = cmp_politics2_ig_{ig['id']} }} }} remove_modifier = {mod}'''+(f''' add_modifier = {{ name = {mod} multiplier = {value:g} }}''' if value!=0 else '')+''' root = { set_variable = cmp_politics2_op_found } }''')
        return '\n'.join(lines)
    for val in [5,10,20,-5,-10,0]:
        sid=('n'+str(abs(val))) if val<0 else str(val)
        L.append(country_route(f'ig_approval_{sid}',ig_local('approval',val)))
    for val in [0.25,0.5,1.0,5.0,-0.5,0.0]:
        sid={0.25:'25',0.5:'50',1.0:'100',5.0:'500',-0.5:'n50',0.0:'0'}[val]
        L.append(country_route(f'ig_strength_{sid}',ig_local('strength',val)))

    # Current-law operations.
    law_ops={
        'law_progress_10':'    if = { limit = { enacting_any_law = yes exists = currently_enacting_law } add_law_progress = 0.10 root = { set_variable = cmp_politics2_op_found } }',
        'law_progress_25':'    if = { limit = { enacting_any_law = yes exists = currently_enacting_law } add_law_progress = 0.25 root = { set_variable = cmp_politics2_op_found } }',
        'law_advance':'    if = { limit = { enacting_any_law = yes exists = currently_enacting_law } add_enactment_phase = 1 root = { set_variable = cmp_politics2_op_found } }',
        'law_setback':'    if = { limit = { enacting_any_law = yes exists = currently_enacting_law } add_enactment_setback = 1 root = { set_variable = cmp_politics2_op_found } }',
        'law_complete':'    if = { limit = { enacting_any_law = yes exists = currently_enacting_law } currently_enacting_law = { save_scope_as = cmp_politics2_current_law } if = { limit = { exists = scope:cmp_politics2_current_law } activate_law = scope:cmp_politics2_current_law.type root = { set_variable = cmp_politics2_op_found } } }',
        'law_cancel':'    if = { limit = { enacting_any_law = yes exists = currently_enacting_law } cancel_enactment = yes root = { set_variable = cmp_politics2_op_found } }',
        'law_clear_modifiers':'    if = { limit = { enacting_any_law = yes exists = currently_enacting_law } clear_enactment_modifier = yes root = { set_variable = cmp_politics2_op_found } }'
    }
    for n,b in law_ops.items(): L.append(country_route(n,b))

    # Power bloc cohesion. Target is the marked country carrying the PB marker.
    for sid,val in [('p25',25),('p50',50),('n25',-25)]:
        L.append(f'''cmp_politics2_bloc_cohesion_{sid}_effect = {{
    remove_variable = cmp_politics2_op_found
    if = {{
        limit = {{ var:cmp_target_core_mode = 11 }}
        every_country = {{
            limit = {{ has_variable = sakuya_mark_power_bloc_target is_in_power_bloc = yes }}
            power_bloc = {{ add_cohesion_number = {val} }}
            root = {{ set_variable = cmp_politics2_op_found }}
        }}
    }}
    if = {{ limit = {{ has_variable = cmp_politics2_op_found }} set_variable = {{ name = cmp_politics2_feedback value = 1 }} }}
    else = {{ set_variable = {{ name = cmp_politics2_feedback value = -4 }} }}
    remove_variable = cmp_politics2_op_found
}}

''')
    L.append('''cmp_politics2_bloc_cohesion_100_effect = {
    remove_variable = cmp_politics2_op_found
    if = {
        limit = { var:cmp_target_core_mode = 11 }
        every_country = {
            limit = { has_variable = sakuya_mark_power_bloc_target is_in_power_bloc = yes }
            power_bloc = { add_cohesion_number = -999999 add_cohesion_number = 100 }
            root = { set_variable = cmp_politics2_op_found }
        }
    }
    if = { limit = { has_variable = cmp_politics2_op_found } set_variable = { name = cmp_politics2_feedback value = 1 } }
    else = { set_variable = { name = cmp_politics2_feedback value = -4 } }
    remove_variable = cmp_politics2_op_found
}
''')
    write(ROOT/'common/scripted_effects/cmp_politics2_effects.txt',''.join(L))


def gen_sgui():
    L=['# Cheat Menu Pro v0.3 beta15 - Politics & Characters 2.0 scripted GUI\n\n']
    country_valid='''OR = { NOT = { has_variable = cmp_target_core_mode } var:cmp_target_core_mode = 1 AND = { var:cmp_target_core_mode = 2 any_country = { has_variable = sakuya_mark_country_target } } AND = { var:cmp_target_core_mode = 3 any_country = { has_variable = cmp_target_group_a_member } } AND = { var:cmp_target_core_mode = 4 any_country = { has_variable = cmp_target_group_b_member } } AND = { var:cmp_target_core_mode = 5 any_country = { has_variable = cmp_target_group_c_member } } }'''
    L.append(f'''cmp_politics2_country_target_valid = {{ scope = country is_valid = {{ is_player = yes {country_valid} }} is_shown = {{ {country_valid} }} }}\n''')
    L.append('''cmp_politics2_character_target_valid = { scope = country is_valid = { is_player = yes var:cmp_target_core_mode = 9 OR = { any_country = { any_scope_character = { has_variable = sakuya_mark_character_target } } any_character_in_exile_pool = { has_variable = sakuya_mark_character_target } } } is_shown = { var:cmp_target_core_mode = 9 } }\n''')
    L.append('''cmp_politics2_commander_target_valid = { scope = country is_valid = { is_player = yes var:cmp_target_core_mode = 9 OR = { any_country = { any_scope_character = { has_variable = sakuya_mark_character_target OR = { has_role_of_type = general has_role_of_type = admiral } } } any_character_in_exile_pool = { has_variable = sakuya_mark_character_target OR = { has_role_of_type = general has_role_of_type = admiral } } } } }\n''')
    L.append('''cmp_politics2_bloc_target_valid = { scope = country is_valid = { is_player = yes var:cmp_target_core_mode = 11 any_country = { has_variable = sakuya_mark_power_bloc_target is_in_power_bloc = yes } } is_shown = { var:cmp_target_core_mode = 11 } }\n''')
    # selection buttons
    for idx,_ in enumerate(CFG['government'],1):
        L.append(f'''cmp_politics2_select_gov_param_{idx} = {{ scope = country is_valid = {{ is_player = yes }} effect = {{ set_variable = {{ name = cmp_politics2_gov_param value = {idx} }} }} }}\ncmp_politics2_gov_param_{idx}_selected = {{ scope = country is_shown = {{ var:cmp_politics2_gov_param = {idx} }} }}\n''')
    for v in [10,25,50,100]:
        L.append(f'''cmp_politics2_select_gov_value_{v} = {{ scope = country is_valid = {{ is_player = yes }} effect = {{ set_variable = {{ name = cmp_politics2_gov_value value = {v} }} }} }}\ncmp_politics2_gov_value_{v}_selected = {{ scope = country is_shown = {{ var:cmp_politics2_gov_value = {v} }} }}\n''')
    L.append('''cmp_politics2_gov_apply = { scope = country is_valid = { is_player = yes has_variable = cmp_politics2_gov_param has_variable = cmp_politics2_gov_value '''+country_valid+''' } effect = { cmp_politics2_gov_apply_effect = yes } }\ncmp_politics2_gov_reset = { scope = country is_valid = { is_player = yes '''+country_valid+''' } effect = { cmp_politics2_gov_reset_effect = yes } }\n''')
    for idx,_ in enumerate(CFG['institutions'],1):
        L.append(f'''cmp_politics2_select_inst_{idx} = {{ scope = country is_valid = {{ is_player = yes }} effect = {{ set_variable = {{ name = cmp_politics2_inst value = {idx} }} }} }}\ncmp_politics2_inst_{idx}_selected = {{ scope = country is_shown = {{ var:cmp_politics2_inst = {idx} }} }}\n''')
    for level in range(1,6):
        L.append(f'''cmp_politics2_select_inst_level_{level} = {{ scope = country is_valid = {{ is_player = yes }} effect = {{ set_variable = {{ name = cmp_politics2_inst_level value = {level} }} }} }}\ncmp_politics2_inst_level_{level}_selected = {{ scope = country is_shown = {{ var:cmp_politics2_inst_level = {level} }} }}\n''')
    L.append('''cmp_politics2_institution_apply = { scope = country is_valid = { is_player = yes has_variable = cmp_politics2_inst has_variable = cmp_politics2_inst_level '''+country_valid+''' } effect = { cmp_politics2_institution_apply_effect = yes } }\n''')
    # character actions
    actions=['immortal_on','immortal_off','health_0p05','health_0p2','health_1p0','health_reset','popularity_5','popularity_25','popularity_100','popularity_reset','role_general_add','role_general_remove','role_admiral_add','role_admiral_remove']
    for a in actions:
        L.append(f'''cmp_politics2_char_{a} = {{ scope = country is_valid = {{ is_player = yes var:cmp_target_core_mode = 9 }} effect = {{ cmp_politics2_char_{a}_effect = yes }} }}\n''')
    for rank in range(1,6):
        L.append(f'''cmp_politics2_char_rank_{rank} = {{ scope = country is_valid = {{ is_player = yes var:cmp_target_core_mode = 9 OR = {{ any_country = {{ any_scope_character = {{ has_variable = sakuya_mark_character_target OR = {{ has_role_of_type = general has_role_of_type = admiral }} }} }} any_character_in_exile_pool = {{ has_variable = sakuya_mark_character_target OR = {{ has_role_of_type = general has_role_of_type = admiral }} }} }} }} effect = {{ cmp_politics2_char_rank_{rank}_effect = yes }} }}\n''')
    for tr in CFG['traits']:
        for op in ['add','remove']:
            L.append(f'''cmp_politics2_char_trait_{tr['id']}_{op} = {{ scope = country is_valid = {{ is_player = yes var:cmp_target_core_mode = 9 }} effect = {{ cmp_politics2_char_trait_{tr['id']}_{op}_effect = yes }} }}\n''')
    # IG selection and actions
    for ig in CFG['interest_groups']:
        iid=ig['id']
        L.append(f'''cmp_politics2_ig_toggle_{iid} = {{ scope = country is_valid = {{ is_player = yes }} effect = {{ if = {{ limit = {{ has_variable = cmp_politics2_ig_{iid} }} remove_variable = cmp_politics2_ig_{iid} }} else = {{ set_variable = cmp_politics2_ig_{iid} }} }} }}\ncmp_politics2_ig_{iid}_selected = {{ scope = country is_shown = {{ has_variable = cmp_politics2_ig_{iid} }} }}\n''')
    anyig='OR = { '+' '.join(f'has_variable = cmp_politics2_ig_{x["id"]}' for x in CFG['interest_groups'])+' }'
    L.append(f'''cmp_politics2_ig_any_selected = {{ scope = country is_shown = {{ {anyig} }} }}\n''')
    for sid in ['5','10','20','n5','n10','0']:
        L.append(f'''cmp_politics2_ig_approval_{sid} = {{ scope = country is_valid = {{ is_player = yes {anyig} {country_valid} }} effect = {{ cmp_politics2_ig_approval_{sid}_effect = yes }} }}\n''')
    for sid in ['25','50','100','500','n50','0']:
        L.append(f'''cmp_politics2_ig_strength_{sid} = {{ scope = country is_valid = {{ is_player = yes {anyig} {country_valid} }} effect = {{ cmp_politics2_ig_strength_{sid}_effect = yes }} }}\n''')
    # laws
    lawvalid='''OR = { AND = { OR = { NOT = { has_variable = cmp_target_core_mode } var:cmp_target_core_mode = 1 } enacting_any_law = yes } AND = { var:cmp_target_core_mode = 2 any_country = { has_variable = sakuya_mark_country_target enacting_any_law = yes } } AND = { var:cmp_target_core_mode = 3 any_country = { has_variable = cmp_target_group_a_member enacting_any_law = yes } } AND = { var:cmp_target_core_mode = 4 any_country = { has_variable = cmp_target_group_b_member enacting_any_law = yes } } AND = { var:cmp_target_core_mode = 5 any_country = { has_variable = cmp_target_group_c_member enacting_any_law = yes } } }'''
    L.append(f'''cmp_politics2_law_target_valid = {{ scope = country is_valid = {{ is_player = yes {lawvalid} }} is_shown = {{ {lawvalid} }} }}\n''')
    for a in ['law_progress_10','law_progress_25','law_advance','law_setback','law_complete','law_cancel','law_clear_modifiers']:
        L.append(f'''cmp_politics2_{a} = {{ scope = country is_valid = {{ is_player = yes {lawvalid} }} effect = {{ cmp_politics2_{a}_effect = yes }} }}\n''')
    # bloc
    for a in ['bloc_cohesion_p25','bloc_cohesion_p50','bloc_cohesion_n25','bloc_cohesion_100']:
        L.append(f'''cmp_politics2_{a} = {{ scope = country is_valid = {{ is_player = yes var:cmp_target_core_mode = 11 any_country = {{ has_variable = sakuya_mark_power_bloc_target is_in_power_bloc = yes }} }} effect = {{ cmp_politics2_{a}_effect = yes }} }}\n''')
    # feedback
    for code,name in [(1,'applied'),(-1,'country_required'),(-2,'character_required'),(-3,'no_eligible'),(-4,'bloc_required')]:
        L.append(f'''cmp_politics2_feedback_{name} = {{ scope = country is_shown = {{ var:cmp_politics2_feedback = {code} }} }}\n''')
    L.append('''cmp_politics2_feedback_clear = { scope = country is_valid = { has_variable = cmp_politics2_feedback } effect = { cmp_politics2_feedback_clear_effect = yes } }\n''')
    write(ROOT/'common/scripted_guis/cmp_politics2_sgui.txt',''.join(L))


def btn(label,sgui,x,y,w=160,h=44,selected=None,tt='CMP_POL2_TT_GENERIC',color='{ 0.42 0.55 0.72 0.96 }',font=12):
    sel=''
    if selected:
        sel=f''' icon = {{ visible = "[GetScriptedGui('{selected}').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" position = {{ 4 {h-5} }} size = {{ {w-8} 3 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}'''
    return f'''            widget = {{ position = {{ {x} {y} }} size = {{ {w} {h} }} button_standard = {{ size = {{ {w} {h} }} enabled = "[GetScriptedGui('{sgui}').IsValid(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" onclick = "[GetScriptedGui('{sgui}').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" tooltip = "{tt}" blockoverride "primary_visible" {{}} blockoverride "primary_texture" {{ texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = {color} }} textbox = {{ size = {{ {w-10} {h-6} }} parentanchor = center maximumsize = {{ {w-10} {h-6} }} fontsize = {font} fontsize_min = 10 align = center|nobaseline elide = right text = "{label}" }} }}{sel} }}'''


def raw_btn(label,onclick,x,y,w=160,h=44,color='{ 0.42 0.55 0.72 0.96 }',font=12,visible=None,tt='CMP_POL2_TT_GENERIC'):
    vis=f' visible = "{visible}"' if visible else ''
    actions = onclick if isinstance(onclick, (list, tuple)) else [onclick]
    onclick_fields = ' '.join(f'onclick = "{action}"' for action in actions)
    return f'''            button_standard = {{{vis} position = {{ {x} {y} }} size = {{ {w} {h} }} {onclick_fields} tooltip = "{tt}" blockoverride "primary_visible" {{}} blockoverride "primary_texture" {{ texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" color = {color} }} textbox = {{ size = {{ {w-10} {h-6} }} parentanchor = center maximumsize = {{ {w-10} {h-6} }} fontsize = {font} fontsize_min = 10 align = center|nobaseline elide = right text = "{label}" }} }}'''


def tab(label,val,x):
    vis=f"[GetVariableSystem.HasValue('cmp_politics2_tab', '{val}')]"
    return raw_btn(label,f"[GetVariableSystem.Set('cmp_politics2_tab', '{val}')]",x,70,136,42,visible=None,tt='CMP_POL2_TT_TAB')+f'''\n            icon = {{ visible = "{vis}" position = {{ {x+4} 108 }} size = {{ 128 3 }} color = {{ 0.35 0.95 0.45 1 }} texture = "gfx/interface/buttons/expand_button_bg_dropdown.dds" alwaystransparent = yes }}'''


def scale_politics_panel(block:str, factor:float=1.20)->str:
    """Scale only the generated Politics 2.0 popup for 2560x1080 readability.

    The popup already uses tabs, so uniform scaling increases physical text/button size
    without increasing information density. The outer origin is reset after scaling so
    the larger panel remains centered inside the CMP window.
    """
    import re
    def pair(m):
        field=m.group(1); a=int(m.group(2)); b=int(m.group(3))
        return f"{field} = {{ {round(a*factor)} {round(b*factor)} }}"
    block=re.sub(r'\b(position|size|maximumsize)\s*=\s*\{\s*(\d+)\s+(\d+)\s*\}', pair, block)
    def fs(m):
        n=int(m.group(1)); return f"fontsize = {max(12, round(n*1.16))}"
    def fmin(m):
        n=int(m.group(1)); return f"fontsize_min = {max(11, round(n*1.12))}"
    block=re.sub(r'fontsize\s*=\s*(\d+)',fs,block)
    block=re.sub(r'fontsize_min\s*=\s*(\d+)',fmin,block)
    # Restore a deliberate outer position after uniform scaling.
    block=block.replace('position = { 264 180 }\n        size = { 912 642 }','position = { 140 82 }\n        size = { 912 642 }',1)
    return block

def gen_gui_panel():
    L=[BEGIN,
'''    widget = {
        visible = "[GetVariableSystem.Exists('cmp_politics2_panel')]"
        position = { 220 150 }
        size = { 760 535 }
        icon = { size = { 760 535 } alpha = 0.96 texture = "gfx/interface/sakuya/bkmask2.png" alwaystransparent = yes }
        textbox = { position = { 20 14 } size = { 580 34 } maximumsize = { 580 34 } fontsize = 20 fontsize_min = 14 align = left text = "CMP_POL2_TITLE" }
        textbox = { position = { 20 44 } size = { 600 22 } maximumsize = { 600 22 } fontsize = 11 fontsize_min = 10 align = left text = "CMP_POL2_DESC" }
        close_button = { position = { 708 10 } size = { 38 38 } onclick = "[GetVariableSystem.Clear('cmp_politics2_panel')]" }
''']
    for i,(lab,val) in enumerate([('CMP_POL2_TAB_GOV','gov'),('CMP_POL2_TAB_CHAR','char'),('CMP_POL2_TAB_IG','ig'),('CMP_POL2_TAB_LAW','law'),('CMP_POL2_TAB_BLOC','bloc')]):
        L.append(tab(lab,val,20+i*142))
    # target button and feedback
    L.append(raw_btn('CMP_POL2_TARGETS',["[GetVariableSystem.Set('cmp_workspace_page', 'target')]", "[GetVariableSystem.Set('cmp_workspace_shell', 'open')]"],20,120,180,38,'{ 0.45 0.62 0.82 0.96 }',11,tt='CMP_POL2_TARGETS_TT'))
    L += [
'''        textbox = { position = { 216 127 } size = { 300 26 } maximumsize = { 300 26 } fontsize = 11 fontsize_min = 10 align = left text = "CMP_POL2_TARGET_HINT" }''',
'''        textbox = { visible = "[GetScriptedGui('cmp_politics2_feedback_applied').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" position = { 520 124 } size = { 210 28 } maximumsize = { 210 28 } fontsize = 11 align = right text = "CMP_POL2_FB_APPLIED" }''',
'''        textbox = { visible = "[GetScriptedGui('cmp_politics2_feedback_country_required').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" position = { 470 124 } size = { 260 28 } maximumsize = { 260 28 } fontsize = 10 align = right text = "CMP_POL2_FB_COUNTRY" }''',
'''        textbox = { visible = "[GetScriptedGui('cmp_politics2_feedback_character_required').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" position = { 470 124 } size = { 260 28 } maximumsize = { 260 28 } fontsize = 10 align = right text = "CMP_POL2_FB_CHARACTER" }''',
'''        textbox = { visible = "[GetScriptedGui('cmp_politics2_feedback_no_eligible').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" position = { 470 124 } size = { 260 28 } maximumsize = { 260 28 } fontsize = 10 align = right text = "CMP_POL2_FB_NO_ELIGIBLE" }''',
'''        textbox = { visible = "[GetScriptedGui('cmp_politics2_feedback_bloc_required').IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]" position = { 470 124 } size = { 260 28 } maximumsize = { 260 28 } fontsize = 10 align = right text = "CMP_POL2_FB_BLOC" }''']

    # Government tab
    L.append('''        widget = { visible = "[Or(Not(GetVariableSystem.Exists('cmp_politics2_tab')), GetVariableSystem.HasValue('cmp_politics2_tab', 'gov'))]" position = { 20 168 } size = { 720 350 }''')
    L += ['''            textbox = { size = { 700 26 } maximumsize = { 700 26 } fontsize = 15 align = left text = "CMP_POL2_GOV_TITLE" }''','''            textbox = { position = { 0 28 } size = { 700 36 } maximumsize = { 700 36 } fontsize = 11 fontsize_min = 10 align = left text = "CMP_POL2_GOV_DESC" }''']
    params=[('CMP_POL2_GOV_LEGIT',1),('CMP_POL2_GOV_AUTH',2),('CMP_POL2_GOV_BUREAU',3),('CMP_POL2_GOV_INFL',4)]
    for i,(lab,idx) in enumerate(params): L.append(btn(lab,f'cmp_politics2_select_gov_param_{idx}',(i%2)*350,72+(i//2)*50,338,44,f'cmp_politics2_gov_param_{idx}_selected','CMP_POL2_TT_GOV_PARAM'))
    for i,v in enumerate([10,25,50,100]): L.append(btn(f'CMP_POL2_VALUE_{v}',f'cmp_politics2_select_gov_value_{v}',i*174,178,164,44,f'cmp_politics2_gov_value_{v}_selected','CMP_POL2_TT_GOV_VALUE'))
    L.append(btn('CMP_POL2_APPLY','cmp_politics2_gov_apply',0,230,338,48,None,'CMP_POL2_TT_GOV_APPLY','{ 0.38 0.68 0.44 0.96 }',13))
    L.append(btn('CMP_POL2_RESET','cmp_politics2_gov_reset',350,230,338,48,None,'CMP_POL2_TT_GOV_RESET','{ 0.58 0.48 0.36 0.96 }',13))
    L += ['''            textbox = { position = { 0 294 } size = { 700 24 } maximumsize = { 700 24 } fontsize = 14 align = left text = "CMP_POL2_INST_TITLE" }''']
    L.append(raw_btn('CMP_POL2_OPEN_INST',"[GetVariableSystem.Toggle('cmp_politics2_inst_panel')]",0,322,688,44,'{ 0.45 0.62 0.82 0.96 }',12,tt='CMP_POL2_INST_TT'))
    L.append('''        }''')

    # institution subpanel overlay
    L.append('''        widget = { visible = "[GetVariableSystem.Exists('cmp_politics2_inst_panel')]" position = { 20 168 } size = { 720 350 }
            icon = { size = { 720 350 } alpha = 0.98 texture = "gfx/interface/sakuya/bkmask2.png" alwaystransparent = yes }
            textbox = { position = { 8 4 } size = { 600 28 } maximumsize = { 600 28 } fontsize = 15 align = left text = "CMP_POL2_INST_TITLE" }
''')
    for i,inst in enumerate(CFG['institutions'],1):
        x=((i-1)%2)*350; y=38+((i-1)//2)*48
        L.append(btn(inst['loc'],f'cmp_politics2_select_inst_{i}',x,y,338,42,f'cmp_politics2_inst_{i}_selected','CMP_POL2_INST_SELECT_TT'))
    y=238
    for i,lv in enumerate(range(1,6)): L.append(btn(f'CMP_POL2_LEVEL_{lv}',f'cmp_politics2_select_inst_level_{lv}',i*112,y,104,42,f'cmp_politics2_inst_level_{lv}_selected','CMP_POL2_INST_LEVEL_TT'))
    L.append(btn('CMP_POL2_INST_APPLY','cmp_politics2_institution_apply',0,288,450,48,None,'CMP_POL2_INST_APPLY_TT','{ 0.38 0.68 0.44 0.96 }',13))
    L.append(raw_btn('CMP_POL2_BACK',"[GetVariableSystem.Clear('cmp_politics2_inst_panel')]",462,288,226,48,'{ 0.58 0.48 0.36 0.96 }',12,tt='CMP_POL2_BACK_TT'))
    L.append('''        }''')

    # Character tab
    L.append('''        widget = { visible = "[GetVariableSystem.HasValue('cmp_politics2_tab', 'char')]" position = { 20 168 } size = { 720 350 }
            textbox = { size = { 700 26 } maximumsize = { 700 26 } fontsize = 15 align = left text = "CMP_POL2_CHAR_TITLE" }
            textbox = { position = { 0 28 } size = { 700 38 } maximumsize = { 700 38 } fontsize = 11 fontsize_min = 10 align = left text = "CMP_POL2_CHAR_DESC" }
''')
    L.append(btn('CMP_POL2_IMMORTAL_ON','cmp_politics2_char_immortal_on',0,72,220,44,None,'CMP_POL2_TT_IMMORTAL'))
    L.append(btn('CMP_POL2_IMMORTAL_OFF','cmp_politics2_char_immortal_off',230,72,220,44,None,'CMP_POL2_TT_IMMORTAL'))
    L.append(btn('CMP_POL2_HEALTH_RESET','cmp_politics2_char_health_reset',460,72,228,44,None,'CMP_POL2_TT_HEALTH','{ 0.58 0.48 0.36 0.96 }'))
    for i,(lab,sid) in enumerate([('CMP_POL2_HEALTH_5','0p05'),('CMP_POL2_HEALTH_20','0p2'),('CMP_POL2_HEALTH_100','1p0')]): L.append(btn(lab,f'cmp_politics2_char_health_{sid}',i*230,124,220,44,None,'CMP_POL2_TT_HEALTH'))
    for i,(lab,sid) in enumerate([('CMP_POL2_POPULARITY_5','5'),('CMP_POL2_POPULARITY_25','25'),('CMP_POL2_POPULARITY_100','100')]): L.append(btn(lab,f'cmp_politics2_char_popularity_{sid}',i*230,176,220,44,None,'CMP_POL2_TT_POPULARITY'))
    L.append(btn('CMP_POL2_POPULARITY_RESET','cmp_politics2_char_popularity_reset',0,228,220,44,None,'CMP_POL2_TT_POPULARITY','{ 0.58 0.48 0.36 0.96 }'))
    L.append(raw_btn('CMP_POL2_OPEN_CHAR_ADV',"[GetVariableSystem.Toggle('cmp_politics2_char_advanced')]",230,228,458,44,'{ 0.45 0.62 0.82 0.96 }',12,tt='CMP_POL2_CHAR_ADV_TT'))
    L += ['''            textbox = { position = { 0 286 } size = { 688 50 } maximumsize = { 688 50 } fontsize = 10 fontsize_min = 10 align = left text = "CMP_POL2_AGE_NOTE" }''','''        }''']
    # char advanced
    L.append('''        widget = { visible = "[GetVariableSystem.Exists('cmp_politics2_char_advanced')]" position = { 20 168 } size = { 720 350 }
            icon = { size = { 720 350 } alpha = 0.98 texture = "gfx/interface/sakuya/bkmask2.png" alwaystransparent = yes }
            textbox = { position = { 8 4 } size = { 600 28 } maximumsize = { 600 28 } fontsize = 15 align = left text = "CMP_POL2_CHAR_ADV_TITLE" }
''')
    # rank
    for i,r in enumerate(range(1,6)): L.append(btn(f'CMP_POL2_RANK_{r}',f'cmp_politics2_char_rank_{r}',i*136,38,128,42,None,'CMP_POL2_RANK_TT'))
    for i,(lab,sg) in enumerate([('CMP_POL2_ROLE_GENERAL_ADD','cmp_politics2_char_role_general_add'),('CMP_POL2_ROLE_GENERAL_REMOVE','cmp_politics2_char_role_general_remove'),('CMP_POL2_ROLE_ADMIRAL_ADD','cmp_politics2_char_role_admiral_add'),('CMP_POL2_ROLE_ADMIRAL_REMOVE','cmp_politics2_char_role_admiral_remove')]): L.append(btn(lab,sg,(i%2)*344,90+(i//2)*48,334,42,None,'CMP_POL2_ROLE_TT'))
    for i,tr in enumerate(CFG['traits']):
        x=(i%2)*344; y=190+(i//2)*48
        # add on left side of each cell, remove small X-like button
        L.append(btn(tr['loc'],f"cmp_politics2_char_trait_{tr['id']}_add",x,y,270,42,None,'CMP_POL2_TRAIT_ADD_TT'))
        L.append(btn('CMP_POL2_REMOVE_SHORT',f"cmp_politics2_char_trait_{tr['id']}_remove",x+276,y,58,42,None,'CMP_POL2_TRAIT_REMOVE_TT','{ 0.72 0.38 0.42 0.96 }',11))
    L.append(raw_btn('CMP_POL2_BACK',"[GetVariableSystem.Clear('cmp_politics2_char_advanced')]",462,326,226,38,'{ 0.58 0.48 0.36 0.96 }',11,tt='CMP_POL2_BACK_TT'))
    L.append('''        }''')

    # IG tab
    L.append('''        widget = { visible = "[GetVariableSystem.HasValue('cmp_politics2_tab', 'ig')]" position = { 20 168 } size = { 720 350 }
            textbox = { size = { 700 26 } maximumsize = { 700 26 } fontsize = 15 align = left text = "CMP_POL2_IG_TITLE" }
            textbox = { position = { 0 28 } size = { 700 38 } maximumsize = { 700 38 } fontsize = 11 fontsize_min = 10 align = left text = "CMP_POL2_IG_DESC" }
''')
    for i,ig in enumerate(CFG['interest_groups']): L.append(btn(ig['loc'],f"cmp_politics2_ig_toggle_{ig['id']}",(i%2)*350,72+(i//2)*46,338,40,f"cmp_politics2_ig_{ig['id']}_selected",'CMP_POL2_IG_SELECT_TT'))
    L += ['''            textbox = { position = { 0 260 } size = { 690 24 } maximumsize = { 690 24 } fontsize = 13 align = left text = "CMP_POL2_IG_ACTIONS" }''']
    L.append(raw_btn('CMP_POL2_OPEN_IG_ACTIONS',"[GetVariableSystem.Toggle('cmp_politics2_ig_actions')]",0,292,688,44,'{ 0.45 0.62 0.82 0.96 }',12,tt='CMP_POL2_IG_ACTIONS_TT'))
    L.append('''        }''')
    L.append('''        widget = { visible = "[GetVariableSystem.Exists('cmp_politics2_ig_actions')]" position = { 20 168 } size = { 720 350 }
            icon = { size = { 720 350 } alpha = 0.98 texture = "gfx/interface/sakuya/bkmask2.png" alwaystransparent = yes }
            textbox = { position = { 8 4 } size = { 690 28 } maximumsize = { 690 28 } fontsize = 15 align = left text = "CMP_POL2_IG_ACTIONS" }
            textbox = { position = { 8 36 } size = { 690 32 } maximumsize = { 690 32 } fontsize = 10 align = left text = "CMP_POL2_IG_STRENGTH_NOTE" }
''')
    appr=[('CMP_POL2_PLUS5','5'),('CMP_POL2_PLUS10','10'),('CMP_POL2_PLUS20','20'),('CMP_POL2_MINUS5','n5'),('CMP_POL2_MINUS10','n10'),('CMP_POL2_RESET','0')]
    for i,(lab,sid) in enumerate(appr): L.append(btn(lab,f'cmp_politics2_ig_approval_{sid}',(i%3)*230,82+(i//3)*48,220,42,None,'CMP_POL2_IG_APPROVAL_TT'))
    L.append('''            textbox = { position = { 0 184 } size = { 690 24 } maximumsize = { 690 24 } fontsize = 13 align = left text = "CMP_POL2_IG_STRENGTH" }''')
    strength=[('CMP_POL2_PLUS25P','25'),('CMP_POL2_PLUS50P','50'),('CMP_POL2_PLUS100P','100'),('CMP_POL2_PLUS500P','500'),('CMP_POL2_MINUS50P','n50'),('CMP_POL2_RESET','0')]
    for i,(lab,sid) in enumerate(strength): L.append(btn(lab,f'cmp_politics2_ig_strength_{sid}',(i%3)*230,214+(i//3)*48,220,42,None,'CMP_POL2_IG_STRENGTH_TT'))
    L.append(raw_btn('CMP_POL2_BACK',"[GetVariableSystem.Clear('cmp_politics2_ig_actions')]",462,316,226,38,'{ 0.58 0.48 0.36 0.96 }',11,tt='CMP_POL2_BACK_TT'))
    L.append('''        }''')

    # Law tab
    L.append('''        widget = { visible = "[GetVariableSystem.HasValue('cmp_politics2_tab', 'law')]" position = { 20 168 } size = { 720 350 }
            textbox = { size = { 700 26 } maximumsize = { 700 26 } fontsize = 15 align = left text = "CMP_POL2_LAW_TITLE" }
            textbox = { position = { 0 28 } size = { 700 50 } maximumsize = { 700 50 } fontsize = 11 fontsize_min = 10 align = left text = "CMP_POL2_LAW_DESC" }
''')
    lawbuttons=[('CMP_POL2_LAW_PROGRESS10','cmp_politics2_law_progress_10'),('CMP_POL2_LAW_PROGRESS25','cmp_politics2_law_progress_25'),('CMP_POL2_LAW_ADVANCE','cmp_politics2_law_advance'),('CMP_POL2_LAW_SETBACK','cmp_politics2_law_setback'),('CMP_POL2_LAW_COMPLETE','cmp_politics2_law_complete'),('CMP_POL2_LAW_CANCEL','cmp_politics2_law_cancel'),('CMP_POL2_LAW_CLEAR_MODS','cmp_politics2_law_clear_modifiers')]
    for i,(lab,sg) in enumerate(lawbuttons): L.append(btn(lab,sg,(i%2)*350,92+(i//2)*54,338,48,None,'CMP_POL2_LAW_ACTION_TT','{ 0.45 0.62 0.82 0.96 }' if i<4 else '{ 0.72 0.48 0.32 0.96 }',12))
    L.append('''        }''')

    # Bloc tab
    L.append('''        widget = { visible = "[GetVariableSystem.HasValue('cmp_politics2_tab', 'bloc')]" position = { 20 168 } size = { 720 350 }
            textbox = { size = { 700 26 } maximumsize = { 700 26 } fontsize = 15 align = left text = "CMP_POL2_BLOC_TITLE" }
            textbox = { position = { 0 28 } size = { 700 50 } maximumsize = { 700 50 } fontsize = 11 fontsize_min = 10 align = left text = "CMP_POL2_BLOC_DESC" }
''')
    for i,(lab,sg) in enumerate([('CMP_POL2_PLUS25','cmp_politics2_bloc_cohesion_p25'),('CMP_POL2_PLUS50','cmp_politics2_bloc_cohesion_p50'),('CMP_POL2_MINUS25','cmp_politics2_bloc_cohesion_n25'),('CMP_POL2_SET100','cmp_politics2_bloc_cohesion_100')]): L.append(btn(lab,sg,(i%2)*350,100+(i//2)*58,338,50,None,'CMP_POL2_BLOC_TT','{ 0.45 0.62 0.82 0.96 }',13))
    L += ['''            textbox = { position = { 0 232 } size = { 688 70 } maximumsize = { 688 70 } fontsize = 11 fontsize_min = 10 align = left text = "CMP_POL2_BLOC_NOTE" }''','''        }''']
    L.append('''    }''')
    L.append(END)
    block='\n'.join(L)+'\n'
    return scale_politics_panel(block)


def gen_localization():
    en={
'CMP_POL2_TITLE':'Politics & Characters 2.0','CMP_POL2_DESC':'Large-control UI for government, characters, interest groups, laws and power blocs.','CMP_POL2_TAB_GOV':'Government','CMP_POL2_TAB_CHAR':'Characters','CMP_POL2_TAB_IG':'Interest Groups','CMP_POL2_TAB_LAW':'Laws','CMP_POL2_TAB_BLOC':'Power Bloc','CMP_POL2_TARGETS':'Open TARGETS','CMP_POL2_TARGETS_TT':'Select Player, Marked Country, Group A/B/C, Character or Power Bloc in Target Core.','CMP_POL2_TARGET_HINT':'Country tabs use Player / Marked Country / Groups A-B-C.','CMP_POL2_GOV_TITLE':'Government controls','CMP_POL2_GOV_DESC':'Select a parameter and magnitude. Legitimacy uses points; Authority, Bureaucracy and Influence use percentages.','CMP_POL2_GOV_LEGIT':'Legitimacy','CMP_POL2_GOV_AUTH':'Authority','CMP_POL2_GOV_BUREAU':'Bureaucracy','CMP_POL2_GOV_INFL':'Influence','CMP_POL2_VALUE_10':'10','CMP_POL2_VALUE_25':'25','CMP_POL2_VALUE_50':'50','CMP_POL2_VALUE_100':'100','CMP_POL2_APPLY':'Apply','CMP_POL2_RESET':'Reset','CMP_POL2_TT_GOV_PARAM':'Choose the government parameter controlled by Politics 2.0.','CMP_POL2_TT_GOV_VALUE':'For Legitimacy this is points. For Authority/Bureaucracy/Influence this is percent.','CMP_POL2_TT_GOV_APPLY':'Replaces the Politics 2.0 modifier for the selected parameter on all country targets.','CMP_POL2_TT_GOV_RESET':'Removes Politics 2.0 government modifiers only. Legacy CMP modifiers are preserved.','CMP_POL2_INST_TITLE':'Institutions','CMP_POL2_OPEN_INST':'Open institution levels','CMP_POL2_INST_TT':'Set an existing institution to level 1-5. Countries without that institution are skipped.','CMP_POL2_INST_COLONIAL':'Colonial Affairs','CMP_POL2_INST_SCHOOLS':'Education','CMP_POL2_INST_WELFARE':'Social Security','CMP_POL2_INST_WORKPLACE':'Workplace Safety','CMP_POL2_INST_POLICE':'Police','CMP_POL2_INST_HEALTH':'Health System','CMP_POL2_INST_HOME':'Home Affairs','CMP_POL2_INST_SELECT_TT':'Select institution.','CMP_POL2_LEVEL_1':'Level 1','CMP_POL2_LEVEL_2':'Level 2','CMP_POL2_LEVEL_3':'Level 3','CMP_POL2_LEVEL_4':'Level 4','CMP_POL2_LEVEL_5':'Level 5','CMP_POL2_INST_LEVEL_TT':'Select exact institution investment level.','CMP_POL2_INST_APPLY':'Set institution level','CMP_POL2_INST_APPLY_TT':'Applies to eligible country targets that already have the selected institution.','CMP_POL2_BACK':'Back','CMP_POL2_BACK_TT':'Return to the previous Politics 2.0 view.','CMP_POL2_CHAR_TITLE':'Marked character','CMP_POL2_CHAR_DESC':'Uses Target Core Character mode. Actions affect the CMP-marked character only.','CMP_POL2_IMMORTAL_ON':'Immortality ON','CMP_POL2_IMMORTAL_OFF':'Immortality OFF','CMP_POL2_TT_IMMORTAL':'Uses the native set_character_immortal effect.','CMP_POL2_HEALTH_5':'Health +0.05','CMP_POL2_HEALTH_20':'Health +0.20','CMP_POL2_HEALTH_100':'Health +1.00','CMP_POL2_HEALTH_RESET':'Reset health boost','CMP_POL2_TT_HEALTH':'Replaces the Politics 2.0 character_health_add modifier.','CMP_POL2_POPULARITY_5':'Popularity +5','CMP_POL2_POPULARITY_25':'Popularity +25','CMP_POL2_POPULARITY_100':'Popularity +100','CMP_POL2_POPULARITY_RESET':'Reset popularity','CMP_POL2_TT_POPULARITY':'Replaces the Politics 2.0 character_popularity_add modifier.','CMP_POL2_OPEN_CHAR_ADV':'Roles, rank and quick traits','CMP_POL2_CHAR_ADV_TT':'Open advanced marked-character controls.','CMP_POL2_CHAR_ADV_TITLE':'Roles, commander rank and quick traits','CMP_POL2_RANK_1':'Rank 1','CMP_POL2_RANK_2':'Rank 2','CMP_POL2_RANK_3':'Rank 3','CMP_POL2_RANK_4':'Rank 4','CMP_POL2_RANK_5':'Rank 5','CMP_POL2_RANK_TT':'Sets commander rank. Enabled only for a marked general or admiral.','CMP_POL2_ROLE_GENERAL_ADD':'Add General role','CMP_POL2_ROLE_GENERAL_REMOVE':'Remove General role','CMP_POL2_ROLE_ADMIRAL_ADD':'Add Admiral role','CMP_POL2_ROLE_ADMIRAL_REMOVE':'Remove Admiral role','CMP_POL2_ROLE_TT':'Adds or removes the native character role. Removing an active military role is destructive.','CMP_POL2_TRAIT_AMBITIOUS':'Ambitious','CMP_POL2_TRAIT_CHARISMATIC':'Charismatic','CMP_POL2_TRAIT_BRAVE':'Brave','CMP_POL2_TRAIT_INNOVATIVE':'Innovative','CMP_POL2_TRAIT_METICULOUS':'Meticulous','CMP_POL2_TRAIT_PERSISTENT':'Persistent','CMP_POL2_REMOVE_SHORT':'Remove','CMP_POL2_TRAIT_ADD_TT':'Adds the selected native character trait if absent.','CMP_POL2_TRAIT_REMOVE_TT':'Removes the selected native character trait if present.','CMP_POL2_AGE_NOTE':'Age is read-only in beta15: the validated 1.13.x effect surface exposes career-length changes but no direct safe biological set-age effect.','CMP_POL2_IG_TITLE':'Interest Group controls','CMP_POL2_IG_DESC':'Select one or several standard IG types. Actions apply those IG-specific country modifiers to country targets.','CMP_POL2_IG_ARMED_FORCES':'Armed Forces','CMP_POL2_IG_DEVOUT':'Devout','CMP_POL2_IG_INDUSTRIALISTS':'Industrialists','CMP_POL2_IG_INTELLIGENTSIA':'Intelligentsia','CMP_POL2_IG_LANDOWNERS':'Landowners','CMP_POL2_IG_PETTY_BOURGEOISIE':'Petty Bourgeoisie','CMP_POL2_IG_RURAL_FOLK':'Rural Folk','CMP_POL2_IG_TRADE_UNIONS':'Trade Unions','CMP_POL2_IG_SELECT_TT':'Toggle this Interest Group type in the Politics 2.0 selection.','CMP_POL2_IG_ACTIONS':'Approval and political strength','CMP_POL2_OPEN_IG_ACTIONS':'Open IG actions','CMP_POL2_IG_ACTIONS_TT':'Requires at least one selected Interest Group type and a country target.','CMP_POL2_IG_STRENGTH':'Political strength multiplier','CMP_POL2_IG_STRENGTH_NOTE':'This modifies IG political strength, not a direct fixed clout percentage. Clout remains a relative result of political strength.','CMP_POL2_PLUS5':'+5','CMP_POL2_PLUS10':'+10','CMP_POL2_PLUS20':'+20','CMP_POL2_MINUS5':'-5','CMP_POL2_MINUS10':'-10','CMP_POL2_PLUS25P':'+25%','CMP_POL2_PLUS50P':'+50%','CMP_POL2_PLUS100P':'+100%','CMP_POL2_PLUS500P':'+500%','CMP_POL2_MINUS50P':'-50%','CMP_POL2_IG_APPROVAL_TT':'Replaces the Politics 2.0 approval modifier for every selected IG type.','CMP_POL2_IG_STRENGTH_TT':'Replaces the Politics 2.0 political-strength multiplier for every selected IG type.','CMP_POL2_LAW_TITLE':'Current law enactment','CMP_POL2_LAW_DESC':'Only countries currently enacting a law are eligible. Group targets skip countries with no active enactment.','CMP_POL2_LAW_PROGRESS10':'Checkpoint progress +10%','CMP_POL2_LAW_PROGRESS25':'Checkpoint progress +25%','CMP_POL2_LAW_ADVANCE':'Advance enactment phase','CMP_POL2_LAW_SETBACK':'Add setback','CMP_POL2_LAW_COMPLETE':'Complete current law','CMP_POL2_LAW_CANCEL':'Cancel enactment','CMP_POL2_LAW_CLEAR_MODS':'Clear enactment modifiers','CMP_POL2_LAW_ACTION_TT':'Uses native law-enactment effects on eligible country targets. Complete/Cancel directly change current enactment state.','CMP_POL2_BLOC_TITLE':'Power Bloc cohesion','CMP_POL2_BLOC_DESC':'Requires Target Core Power Bloc mode and a valid marked bloc.','CMP_POL2_PLUS25':'+25','CMP_POL2_PLUS50':'+50','CMP_POL2_MINUS25':'-25','CMP_POL2_SET100':'Set to 100','CMP_POL2_BLOC_TT':'Changes cohesion of the marked Power Bloc using native cohesion effects.','CMP_POL2_BLOC_NOTE':'Beta15 intentionally keeps Power Bloc controls narrow. Membership, principles and leverage remain in legacy CMP until their semantics are audited for Vanilla Rework.','CMP_POL2_FB_APPLIED':'APPLIED','CMP_POL2_FB_COUNTRY':'COUNTRY TARGET REQUIRED','CMP_POL2_FB_CHARACTER':'MARKED CHARACTER REQUIRED','CMP_POL2_FB_NO_ELIGIBLE':'NO ELIGIBLE TARGET','CMP_POL2_FB_BLOC':'POWER BLOC TARGET REQUIRED','CMP_POL2_TT_GENERIC':'Politics & Characters 2.0','CMP_POL2_TT_TAB':'Switch Politics 2.0 section.','CMP_POL2_OPEN':'Politics 2.0','CMP_POL2_OPEN_TT':'Open the redesigned Characters / Government / IG / Laws / Power Bloc controller.'}
    ru={
'CMP_POL2_TITLE':'\u041f\u043e\u043b\u0438\u0442\u0438\u043a\u0430 \u0438 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0438 2.0','CMP_POL2_DESC':'\u041a\u0440\u0443\u043f\u043d\u044b\u0439 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441: \u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u043e, \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0438, \u0433\u0440\u0443\u043f\u043f\u044b \u0438\u043d\u0442\u0435\u0440\u0435\u0441\u043e\u0432, \u0437\u0430\u043a\u043e\u043d\u044b \u0438 \u0431\u043b\u043e\u043a \u0434\u0435\u0440\u0436\u0430\u0432.','CMP_POL2_TAB_GOV':'\u041f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u043e','CMP_POL2_TAB_CHAR':'\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0438','CMP_POL2_TAB_IG':'\u0413\u0440\u0443\u043f\u043f\u044b \u0438\u043d\u0442\u0435\u0440\u0435\u0441\u043e\u0432','CMP_POL2_TAB_LAW':'\u0417\u0430\u043a\u043e\u043d\u044b','CMP_POL2_TAB_BLOC':'\u0411\u043b\u043e\u043a \u0434\u0435\u0440\u0436\u0430\u0432','CMP_POL2_TARGETS':'\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0426\u0415\u041b\u0418','CMP_POL2_TARGETS_TT':'\u0412 Target Core \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0438\u0433\u0440\u043e\u043a\u0430, \u043e\u0442\u043c\u0435\u0447\u0435\u043d\u043d\u0443\u044e \u0441\u0442\u0440\u0430\u043d\u0443, \u0433\u0440\u0443\u043f\u043f\u0443 A/B/C, \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0430 \u0438\u043b\u0438 \u0431\u043b\u043e\u043a.','CMP_POL2_TARGET_HINT':'\u0412\u043a\u043b\u0430\u0434\u043a\u0438 \u0441\u0442\u0440\u0430\u043d: \u0438\u0433\u0440\u043e\u043a / \u043e\u0442\u043c\u0435\u0447\u0435\u043d\u043d\u0430\u044f / A-B-C.','CMP_POL2_GOV_TITLE':'\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u043e\u043c','CMP_POL2_GOV_DESC':'\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440 \u0438 \u0432\u0435\u043b\u0438\u0447\u0438\u043d\u0443. \u041b\u0435\u0433\u0438\u0442\u0438\u043c\u043d\u043e\u0441\u0442\u044c — \u043e\u0447\u043a\u0438; \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442, \u0431\u044e\u0440\u043e\u043a\u0440\u0430\u0442\u0438\u044f \u0438 \u0432\u043b\u0438\u044f\u043d\u0438\u0435 — \u043f\u0440\u043e\u0446\u0435\u043d\u0442\u044b.','CMP_POL2_GOV_LEGIT':'\u041b\u0435\u0433\u0438\u0442\u0438\u043c\u043d\u043e\u0441\u0442\u044c','CMP_POL2_GOV_AUTH':'\u0410\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442','CMP_POL2_GOV_BUREAU':'\u0411\u044e\u0440\u043e\u043a\u0440\u0430\u0442\u0438\u044f','CMP_POL2_GOV_INFL':'\u0412\u043b\u0438\u044f\u043d\u0438\u0435','CMP_POL2_VALUE_10':'10','CMP_POL2_VALUE_25':'25','CMP_POL2_VALUE_50':'50','CMP_POL2_VALUE_100':'100','CMP_POL2_APPLY':'\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c','CMP_POL2_RESET':'\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c','CMP_POL2_TT_GOV_PARAM':'\u0412\u044b\u0431\u043e\u0440 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u0430 Politics 2.0.','CMP_POL2_TT_GOV_VALUE':'\u0414\u043b\u044f \u043b\u0435\u0433\u0438\u0442\u0438\u043c\u043d\u043e\u0441\u0442\u0438 — \u043e\u0447\u043a\u0438. \u0414\u043b\u044f \u0430\u0432\u0442\u043e\u0440\u0438\u0442\u0435\u0442\u0430/\u0431\u044e\u0440\u043e\u043a\u0440\u0430\u0442\u0438\u0438/\u0432\u043b\u0438\u044f\u043d\u0438\u044f — \u043f\u0440\u043e\u0446\u0435\u043d\u0442\u044b.','CMP_POL2_TT_GOV_APPLY':'\u0417\u0430\u043c\u0435\u043d\u044f\u0435\u0442 \u0442\u043e\u043b\u044c\u043a\u043e \u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 Politics 2.0 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u0433\u043e \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u0430.','CMP_POL2_TT_GOV_RESET':'\u0423\u0434\u0430\u043b\u044f\u0435\u0442 \u0442\u043e\u043b\u044c\u043a\u043e \u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u044b Politics 2.0; legacy-\u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u044b CMP \u043d\u0435 \u0437\u0430\u0442\u0440\u0430\u0433\u0438\u0432\u0430\u044e\u0442\u0441\u044f.','CMP_POL2_INST_TITLE':'\u0418\u043d\u0441\u0442\u0438\u0442\u0443\u0442\u044b','CMP_POL2_OPEN_INST':'\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0443\u0440\u043e\u0432\u043d\u0438 \u0438\u043d\u0441\u0442\u0438\u0442\u0443\u0442\u043e\u0432','CMP_POL2_INST_TT':'\u0422\u043e\u0447\u043d\u043e \u0443\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442 \u0443\u0440\u043e\u0432\u0435\u043d\u044c 1–5 \u0443\u0436\u0435 \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u044e\u0449\u0435\u0433\u043e \u0438\u043d\u0441\u0442\u0438\u0442\u0443\u0442\u0430; \u0441\u0442\u0440\u0430\u043d\u044b \u0431\u0435\u0437 \u043d\u0435\u0433\u043e \u043f\u0440\u043e\u043f\u0443\u0441\u043a\u0430\u044e\u0442\u0441\u044f.','CMP_POL2_INST_COLONIAL':'\u041a\u043e\u043b\u043e\u043d\u0438\u0430\u043b\u044c\u043d\u044b\u0435 \u0434\u0435\u043b\u0430','CMP_POL2_INST_SCHOOLS':'\u041e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u0435','CMP_POL2_INST_WELFARE':'\u0421\u043e\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0435 \u043e\u0431\u0435\u0441\u043f\u0435\u0447\u0435\u043d\u0438\u0435','CMP_POL2_INST_WORKPLACE':'\u041e\u0445\u0440\u0430\u043d\u0430 \u0442\u0440\u0443\u0434\u0430','CMP_POL2_INST_POLICE':'\u041f\u043e\u043b\u0438\u0446\u0438\u044f','CMP_POL2_INST_HEALTH':'\u0417\u0434\u0440\u0430\u0432\u043e\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u0435','CMP_POL2_INST_HOME':'\u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0435 \u0434\u0435\u043b\u0430','CMP_POL2_INST_SELECT_TT':'\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0438\u043d\u0441\u0442\u0438\u0442\u0443\u0442.','CMP_POL2_LEVEL_1':'\u0423\u0440\u043e\u0432\u0435\u043d\u044c 1','CMP_POL2_LEVEL_2':'\u0423\u0440\u043e\u0432\u0435\u043d\u044c 2','CMP_POL2_LEVEL_3':'\u0423\u0440\u043e\u0432\u0435\u043d\u044c 3','CMP_POL2_LEVEL_4':'\u0423\u0440\u043e\u0432\u0435\u043d\u044c 4','CMP_POL2_LEVEL_5':'\u0423\u0440\u043e\u0432\u0435\u043d\u044c 5','CMP_POL2_INST_LEVEL_TT':'\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0442\u043e\u0447\u043d\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0438\u043d\u0432\u0435\u0441\u0442\u0438\u0446\u0438\u0439 \u0432 \u0438\u043d\u0441\u0442\u0438\u0442\u0443\u0442.','CMP_POL2_INST_APPLY':'\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0443\u0440\u043e\u0432\u0435\u043d\u044c','CMP_POL2_INST_APPLY_TT':'\u041f\u0440\u0438\u043c\u0435\u043d\u044f\u0435\u0442\u0441\u044f \u043a \u043f\u043e\u0434\u0445\u043e\u0434\u044f\u0449\u0438\u043c \u0441\u0442\u0440\u0430\u043d\u0430\u043c, \u0433\u0434\u0435 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u0438\u043d\u0441\u0442\u0438\u0442\u0443\u0442 \u0443\u0436\u0435 \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u0435\u0442.','CMP_POL2_BACK':'\u041d\u0430\u0437\u0430\u0434','CMP_POL2_BACK_TT':'\u0412\u0435\u0440\u043d\u0443\u0442\u044c\u0441\u044f \u043d\u0430 \u043f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0438\u0439 \u044d\u043a\u0440\u0430\u043d Politics 2.0.','CMP_POL2_CHAR_TITLE':'\u041e\u0442\u043c\u0435\u0447\u0435\u043d\u043d\u044b\u0439 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436','CMP_POL2_CHAR_DESC':'\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442 \u0440\u0435\u0436\u0438\u043c \u00ab\u041f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u00bb Target Core. \u0414\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u0437\u0430\u0442\u0440\u0430\u0433\u0438\u0432\u0430\u044e\u0442 \u0442\u043e\u043b\u044c\u043a\u043e \u043e\u0442\u043c\u0435\u0447\u0435\u043d\u043d\u043e\u0433\u043e CMP \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0430.','CMP_POL2_IMMORTAL_ON':'\u0411\u0435\u0441\u0441\u043c\u0435\u0440\u0442\u0438\u0435: \u0412\u041a\u041b','CMP_POL2_IMMORTAL_OFF':'\u0411\u0435\u0441\u0441\u043c\u0435\u0440\u0442\u0438\u0435: \u0412\u042b\u041a\u041b','CMP_POL2_TT_IMMORTAL':'\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442 \u0448\u0442\u0430\u0442\u043d\u044b\u0439 \u044d\u0444\u0444\u0435\u043a\u0442 set_character_immortal.','CMP_POL2_HEALTH_5':'\u0417\u0434\u043e\u0440\u043e\u0432\u044c\u0435 +0,05','CMP_POL2_HEALTH_20':'\u0417\u0434\u043e\u0440\u043e\u0432\u044c\u0435 +0,20','CMP_POL2_HEALTH_100':'\u0417\u0434\u043e\u0440\u043e\u0432\u044c\u0435 +1,00','CMP_POL2_HEALTH_RESET':'\u0421\u0431\u0440\u043e\u0441 \u0431\u043e\u043d\u0443\u0441\u0430 \u0437\u0434\u043e\u0440\u043e\u0432\u044c\u044f','CMP_POL2_TT_HEALTH':'\u0417\u0430\u043c\u0435\u043d\u044f\u0435\u0442 \u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 Politics 2.0 character_health_add.','CMP_POL2_POPULARITY_5':'\u041f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u043e\u0441\u0442\u044c +5','CMP_POL2_POPULARITY_25':'\u041f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u043e\u0441\u0442\u044c +25','CMP_POL2_POPULARITY_100':'\u041f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u043e\u0441\u0442\u044c +100','CMP_POL2_POPULARITY_RESET':'\u0421\u0431\u0440\u043e\u0441 \u043f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u043e\u0441\u0442\u0438','CMP_POL2_TT_POPULARITY':'\u0417\u0430\u043c\u0435\u043d\u044f\u0435\u0442 \u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 Politics 2.0 character_popularity_add.','CMP_POL2_OPEN_CHAR_ADV':'\u0420\u043e\u043b\u0438, \u0440\u0430\u043d\u0433 \u0438 \u0431\u044b\u0441\u0442\u0440\u044b\u0435 \u0447\u0435\u0440\u0442\u044b','CMP_POL2_CHAR_ADV_TT':'\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0440\u0430\u0441\u0448\u0438\u0440\u0435\u043d\u043d\u043e\u0435 \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043e\u0442\u043c\u0435\u0447\u0435\u043d\u043d\u044b\u043c \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0435\u043c.','CMP_POL2_CHAR_ADV_TITLE':'\u0420\u043e\u043b\u0438, \u0440\u0430\u043d\u0433 \u043a\u043e\u043c\u0430\u043d\u0434\u0438\u0440\u0430 \u0438 \u0431\u044b\u0441\u0442\u0440\u044b\u0435 \u0447\u0435\u0440\u0442\u044b','CMP_POL2_RANK_1':'\u0420\u0430\u043d\u0433 1','CMP_POL2_RANK_2':'\u0420\u0430\u043d\u0433 2','CMP_POL2_RANK_3':'\u0420\u0430\u043d\u0433 3','CMP_POL2_RANK_4':'\u0420\u0430\u043d\u0433 4','CMP_POL2_RANK_5':'\u0420\u0430\u043d\u0433 5','CMP_POL2_RANK_TT':'\u0423\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442 \u0440\u0430\u043d\u0433 \u043a\u043e\u043c\u0430\u043d\u0434\u0438\u0440\u0430. \u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u0434\u043b\u044f \u043e\u0442\u043c\u0435\u0447\u0435\u043d\u043d\u043e\u0433\u043e \u0433\u0435\u043d\u0435\u0440\u0430\u043b\u0430 \u0438\u043b\u0438 \u0430\u0434\u043c\u0438\u0440\u0430\u043b\u0430.','CMP_POL2_ROLE_GENERAL_ADD':'\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0440\u043e\u043b\u044c \u0433\u0435\u043d\u0435\u0440\u0430\u043b\u0430','CMP_POL2_ROLE_GENERAL_REMOVE':'\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0440\u043e\u043b\u044c \u0433\u0435\u043d\u0435\u0440\u0430\u043b\u0430','CMP_POL2_ROLE_ADMIRAL_ADD':'\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0440\u043e\u043b\u044c \u0430\u0434\u043c\u0438\u0440\u0430\u043b\u0430','CMP_POL2_ROLE_ADMIRAL_REMOVE':'\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0440\u043e\u043b\u044c \u0430\u0434\u043c\u0438\u0440\u0430\u043b\u0430','CMP_POL2_ROLE_TT':'\u0414\u043e\u0431\u0430\u0432\u043b\u044f\u0435\u0442 \u0438\u043b\u0438 \u0443\u0434\u0430\u043b\u044f\u0435\u0442 \u0448\u0442\u0430\u0442\u043d\u0443\u044e \u0440\u043e\u043b\u044c \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0430. \u0423\u0434\u0430\u043b\u0435\u043d\u0438\u0435 \u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0439 \u0432\u043e\u0435\u043d\u043d\u043e\u0439 \u0440\u043e\u043b\u0438 — \u0440\u0430\u0437\u0440\u0443\u0448\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435.','CMP_POL2_TRAIT_AMBITIOUS':'\u0410\u043c\u0431\u0438\u0446\u0438\u043e\u0437\u043d\u044b\u0439','CMP_POL2_TRAIT_CHARISMATIC':'\u0425\u0430\u0440\u0438\u0437\u043c\u0430\u0442\u0438\u0447\u043d\u044b\u0439','CMP_POL2_TRAIT_BRAVE':'\u0425\u0440\u0430\u0431\u0440\u044b\u0439','CMP_POL2_TRAIT_INNOVATIVE':'\u041d\u043e\u0432\u0430\u0442\u043e\u0440','CMP_POL2_TRAIT_METICULOUS':'\u0421\u043a\u0440\u0443\u043f\u0443\u043b\u0435\u0437\u043d\u044b\u0439','CMP_POL2_TRAIT_PERSISTENT':'\u0423\u043f\u043e\u0440\u043d\u044b\u0439','CMP_POL2_REMOVE_SHORT':'\u0423\u0434\u0430\u043b.','CMP_POL2_TRAIT_ADD_TT':'\u0414\u043e\u0431\u0430\u0432\u043b\u044f\u0435\u0442 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u0443\u044e \u0448\u0442\u0430\u0442\u043d\u0443\u044e \u0447\u0435\u0440\u0442\u0443, \u0435\u0441\u043b\u0438 \u0435\u0435 \u043d\u0435\u0442.','CMP_POL2_TRAIT_REMOVE_TT':'\u0423\u0434\u0430\u043b\u044f\u0435\u0442 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u0443\u044e \u0447\u0435\u0440\u0442\u0443, \u0435\u0441\u043b\u0438 \u043e\u043d\u0430 \u0435\u0441\u0442\u044c.','CMP_POL2_AGE_NOTE':'\u0412\u043e\u0437\u0440\u0430\u0441\u0442 \u0432 beta15 \u0442\u043e\u043b\u044c\u043a\u043e \u0434\u043b\u044f \u0447\u0442\u0435\u043d\u0438\u044f: \u0432 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043d\u043e\u043c API 1.13.x \u0435\u0441\u0442\u044c \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u0441\u0440\u043e\u043a\u0430 \u043a\u0430\u0440\u044c\u0435\u0440\u044b, \u043d\u043e \u043d\u0435\u0442 \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0433\u043e \u043f\u0440\u044f\u043c\u043e\u0433\u043e SET \u0431\u0438\u043e\u043b\u043e\u0433\u0438\u0447\u0435\u0441\u043a\u043e\u0433\u043e \u0432\u043e\u0437\u0440\u0430\u0441\u0442\u0430.','CMP_POL2_IG_TITLE':'\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0433\u0440\u0443\u043f\u043f\u0430\u043c\u0438 \u0438\u043d\u0442\u0435\u0440\u0435\u0441\u043e\u0432','CMP_POL2_IG_DESC':'\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043e\u0434\u043d\u0443 \u0438\u043b\u0438 \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u043e \u0441\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0445 \u0433\u0440\u0443\u043f\u043f. \u0414\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u043f\u0440\u0438\u043c\u0435\u043d\u044f\u044e\u0442 IG-\u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u044b \u043a \u0441\u0442\u0440\u0430\u043d\u0430\u043c-\u0446\u0435\u043b\u044f\u043c.','CMP_POL2_IG_ARMED_FORCES':'\u0412\u043e\u043e\u0440\u0443\u0436\u0435\u043d\u043d\u044b\u0435 \u0441\u0438\u043b\u044b','CMP_POL2_IG_DEVOUT':'\u0414\u0443\u0445\u043e\u0432\u0435\u043d\u0441\u0442\u0432\u043e','CMP_POL2_IG_INDUSTRIALISTS':'\u041f\u0440\u043e\u043c\u044b\u0448\u043b\u0435\u043d\u043d\u0438\u043a\u0438','CMP_POL2_IG_INTELLIGENTSIA':'\u0418\u043d\u0442\u0435\u043b\u043b\u0438\u0433\u0435\u043d\u0446\u0438\u044f','CMP_POL2_IG_LANDOWNERS':'\u0417\u0435\u043c\u043b\u0435\u0432\u043b\u0430\u0434\u0435\u043b\u044c\u0446\u044b','CMP_POL2_IG_PETTY_BOURGEOISIE':'\u041c\u0435\u043b\u043a\u0430\u044f \u0431\u0443\u0440\u0436\u0443\u0430\u0437\u0438\u044f','CMP_POL2_IG_RURAL_FOLK':'\u0421\u0435\u043b\u044c\u0441\u043a\u0438\u0435 \u0436\u0438\u0442\u0435\u043b\u0438','CMP_POL2_IG_TRADE_UNIONS':'\u041f\u0440\u043e\u0444\u0441\u043e\u044e\u0437\u044b','CMP_POL2_IG_SELECT_TT':'\u0412\u043a\u043b\u044e\u0447\u0438\u0442\u044c/\u0432\u044b\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u044d\u0442\u043e\u0442 \u0442\u0438\u043f \u0433\u0440\u0443\u043f\u043f\u044b \u0432 \u0432\u044b\u0431\u043e\u0440\u0435 Politics 2.0.','CMP_POL2_IG_ACTIONS':'\u041e\u0434\u043e\u0431\u0440\u0435\u043d\u0438\u0435 \u0438 \u043f\u043e\u043b\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0441\u0438\u043b\u0430','CMP_POL2_OPEN_IG_ACTIONS':'\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f \u0441 \u0433\u0440\u0443\u043f\u043f\u0430\u043c\u0438','CMP_POL2_IG_ACTIONS_TT':'\u041d\u0443\u0436\u043d\u0430 \u0445\u043e\u0442\u044f \u0431\u044b \u043e\u0434\u043d\u0430 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u0430\u044f \u0433\u0440\u0443\u043f\u043f\u0430 \u0438 \u0441\u0442\u0440\u0430\u043d\u0430-\u0446\u0435\u043b\u044c.','CMP_POL2_IG_STRENGTH':'\u041c\u043d\u043e\u0436\u0438\u0442\u0435\u043b\u044c \u043f\u043e\u043b\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0439 \u0441\u0438\u043b\u044b','CMP_POL2_IG_STRENGTH_NOTE':'\u041c\u0435\u043d\u044f\u0435\u0442\u0441\u044f \u043f\u043e\u043b\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f \u0441\u0438\u043b\u0430 IG, \u0430 \u043d\u0435 \u0444\u0438\u043a\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u043f\u0440\u043e\u0446\u0435\u043d\u0442 \u0432\u043b\u0438\u044f\u043d\u0438\u044f. \u0412\u043b\u0438\u044f\u043d\u0438\u0435 (clout) \u043e\u0441\u0442\u0430\u0435\u0442\u0441\u044f \u043e\u0442\u043d\u043e\u0441\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u043c \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u043c.','CMP_POL2_PLUS5':'+5','CMP_POL2_PLUS10':'+10','CMP_POL2_PLUS20':'+20','CMP_POL2_MINUS5':'-5','CMP_POL2_MINUS10':'-10','CMP_POL2_PLUS25P':'+25%','CMP_POL2_PLUS50P':'+50%','CMP_POL2_PLUS100P':'+100%','CMP_POL2_PLUS500P':'+500%','CMP_POL2_MINUS50P':'-50%','CMP_POL2_IG_APPROVAL_TT':'\u0417\u0430\u043c\u0435\u043d\u044f\u0435\u0442 \u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043e\u0434\u043e\u0431\u0440\u0435\u043d\u0438\u044f Politics 2.0 \u0434\u043b\u044f \u043a\u0430\u0436\u0434\u043e\u0439 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u0439 IG.','CMP_POL2_IG_STRENGTH_TT':'\u0417\u0430\u043c\u0435\u043d\u044f\u0435\u0442 \u043c\u043d\u043e\u0436\u0438\u0442\u0435\u043b\u044c \u043f\u043e\u043b\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0439 \u0441\u0438\u043b\u044b Politics 2.0 \u0434\u043b\u044f \u043a\u0430\u0436\u0434\u043e\u0439 \u0432\u044b\u0431\u0440\u0430\u043d\u043d\u043e\u0439 IG.','CMP_POL2_LAW_TITLE':'\u0422\u0435\u043a\u0443\u0449\u0435\u0435 \u043f\u0440\u0438\u043d\u044f\u0442\u0438\u0435 \u0437\u0430\u043a\u043e\u043d\u0430','CMP_POL2_LAW_DESC':'\u041f\u043e\u0434\u0445\u043e\u0434\u044f\u0442 \u0442\u043e\u043b\u044c\u043a\u043e \u0441\u0442\u0440\u0430\u043d\u044b, \u0433\u0434\u0435 \u0441\u0435\u0439\u0447\u0430\u0441 \u043f\u0440\u0438\u043d\u0438\u043c\u0430\u0435\u0442\u0441\u044f \u0437\u0430\u043a\u043e\u043d. \u0412 \u0433\u0440\u0443\u043f\u043f\u0430\u0445 A/B/C \u0441\u0442\u0440\u0430\u043d\u044b \u0431\u0435\u0437 \u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0433\u043e \u043f\u0440\u043e\u0446\u0435\u0441\u0441\u0430 \u043f\u0440\u043e\u043f\u0443\u0441\u043a\u0430\u044e\u0442\u0441\u044f.','CMP_POL2_LAW_PROGRESS10':'\u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441 \u044d\u0442\u0430\u043f\u0430 +10%','CMP_POL2_LAW_PROGRESS25':'\u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441 \u044d\u0442\u0430\u043f\u0430 +25%','CMP_POL2_LAW_ADVANCE':'\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0430\u044f \u0444\u0430\u0437\u0430','CMP_POL2_LAW_SETBACK':'\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043d\u0435\u0443\u0434\u0430\u0447\u0443','CMP_POL2_LAW_COMPLETE':'\u041d\u0435\u043c\u0435\u0434\u043b\u0435\u043d\u043d\u043e \u043f\u0440\u0438\u043d\u044f\u0442\u044c \u0437\u0430\u043a\u043e\u043d','CMP_POL2_LAW_CANCEL':'\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c \u043f\u0440\u0438\u043d\u044f\u0442\u0438\u0435','CMP_POL2_LAW_CLEAR_MODS':'\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440\u044b \u043f\u0440\u0438\u043d\u044f\u0442\u0438\u044f','CMP_POL2_LAW_ACTION_TT':'\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442 \u0448\u0442\u0430\u0442\u043d\u044b\u0435 \u044d\u0444\u0444\u0435\u043a\u0442\u044b \u043f\u0440\u0438\u043d\u044f\u0442\u0438\u044f \u0437\u0430\u043a\u043e\u043d\u0430. \u00ab\u041f\u0440\u0438\u043d\u044f\u0442\u044c\u00bb \u0438 \u00ab\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c\u00bb \u043d\u0435\u043f\u043e\u0441\u0440\u0435\u0434\u0441\u0442\u0432\u0435\u043d\u043d\u043e \u043c\u0435\u043d\u044f\u044e\u0442 \u0442\u0435\u043a\u0443\u0449\u0438\u0439 \u043f\u0440\u043e\u0446\u0435\u0441\u0441.','CMP_POL2_BLOC_TITLE':'\u0421\u043f\u043b\u043e\u0447\u0435\u043d\u043d\u043e\u0441\u0442\u044c \u0431\u043b\u043e\u043a\u0430 \u0434\u0435\u0440\u0436\u0430\u0432','CMP_POL2_BLOC_DESC':'\u041d\u0443\u0436\u0435\u043d \u0440\u0435\u0436\u0438\u043c \u00ab\u0411\u043b\u043e\u043a \u0434\u0435\u0440\u0436\u0430\u0432\u00bb \u0432 Target Core \u0438 \u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043d\u043e \u043e\u0442\u043c\u0435\u0447\u0435\u043d\u043d\u044b\u0439 \u0431\u043b\u043e\u043a.','CMP_POL2_PLUS25':'+25','CMP_POL2_PLUS50':'+50','CMP_POL2_MINUS25':'-25','CMP_POL2_SET100':'\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c 100','CMP_POL2_BLOC_TT':'\u041c\u0435\u043d\u044f\u0435\u0442 \u0441\u043f\u043b\u043e\u0447\u0435\u043d\u043d\u043e\u0441\u0442\u044c \u043e\u0442\u043c\u0435\u0447\u0435\u043d\u043d\u043e\u0433\u043e \u0431\u043b\u043e\u043a\u0430 \u0448\u0442\u0430\u0442\u043d\u044b\u043c \u044d\u0444\u0444\u0435\u043a\u0442\u043e\u043c cohesion.','CMP_POL2_BLOC_NOTE':'\u0412 beta15 \u0441\u043e\u0437\u043d\u0430\u0442\u0435\u043b\u044c\u043d\u043e \u043e\u0441\u0442\u0430\u0432\u043b\u044f\u0435\u043c \u0437\u0434\u0435\u0441\u044c \u0442\u043e\u043b\u044c\u043a\u043e \u0441\u043f\u043b\u043e\u0447\u0435\u043d\u043d\u043e\u0441\u0442\u044c. \u0427\u043b\u0435\u043d\u0441\u0442\u0432\u043e, \u043f\u0440\u0438\u043d\u0446\u0438\u043f\u044b \u0438 leverage \u043e\u0441\u0442\u0430\u044e\u0442\u0441\u044f \u0432 legacy CMP \u0434\u043e \u0430\u0443\u0434\u0438\u0442\u0430 Vanilla Rework.','CMP_POL2_FB_APPLIED':'\u041f\u0420\u0418\u041c\u0415\u041d\u0415\u041d\u041e','CMP_POL2_FB_COUNTRY':'\u041d\u0423\u0416\u041d\u0410 \u0421\u0422\u0420\u0410\u041d\u0410-\u0426\u0415\u041b\u042c','CMP_POL2_FB_CHARACTER':'\u041d\u0423\u0416\u0415\u041d \u041e\u0422\u041c\u0415\u0427\u0415\u041d\u041d\u042b\u0419 \u041f\u0415\u0420\u0421\u041e\u041d\u0410\u0416','CMP_POL2_FB_NO_ELIGIBLE':'\u041d\u0415\u0422 \u041f\u041e\u0414\u0425\u041e\u0414\u042f\u0429\u0415\u0419 \u0426\u0415\u041b\u0418','CMP_POL2_FB_BLOC':'\u041d\u0423\u0416\u0415\u041d \u0411\u041b\u041e\u041a-\u0426\u0415\u041b\u042c','CMP_POL2_TT_GENERIC':'\u041f\u043e\u043b\u0438\u0442\u0438\u043a\u0430 \u0438 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0438 2.0','CMP_POL2_TT_TAB':'\u041f\u0435\u0440\u0435\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0440\u0430\u0437\u0434\u0435\u043b Politics 2.0.','CMP_POL2_OPEN':'\u041f\u043e\u043b\u0438\u0442\u0438\u043a\u0430 2.0','CMP_POL2_OPEN_TT':'\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u043d\u043e\u0432\u044b\u0439 \u043a\u043e\u043d\u0442\u0440\u043e\u043b\u043b\u0435\u0440 \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u0436\u0435\u0439, \u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u0430, IG, \u0437\u0430\u043a\u043e\u043d\u043e\u0432 \u0438 \u0431\u043b\u043e\u043a\u0430.'}

    # Russian visible strings are intentionally fully localized; technical implementation
    # identifiers stay in source/docs, not in the player-facing UI.
    ru.update({
        'CMP_POL2_TARGETS_TT':'В контроллере целей выберите игрока, отмеченную страну, группу A/B/C, персонажа или блок держав.',
        'CMP_POL2_TT_GOV_PARAM':'Выберите параметр, которым управляет раздел «Политика 2.0».',
        'CMP_POL2_TT_GOV_APPLY':'Заменяет только наш модификатор выбранного параметра у всех подходящих стран-целей.',
        'CMP_POL2_TT_GOV_RESET':'Удаляет только модификаторы «Политика 2.0»; старые модификаторы CMP не затрагиваются.',
        'CMP_POL2_BACK_TT':'Вернуться на предыдущий экран «Политика 2.0».',
        'CMP_POL2_CHAR_DESC':'Использует режим «Персонаж» контроллера целей. Действия затрагивают только отмеченного персонажа CMP.',
        'CMP_POL2_TT_IMMORTAL':'Включает или выключает штатное бессмертие персонажа.',
        'CMP_POL2_TT_HEALTH':'Заменяет только наш бонус к здоровью персонажа; это не точная установка внутреннего значения здоровья.',
        'CMP_POL2_TT_POPULARITY':'Заменяет только наш бонус к популярности персонажа.',
        'CMP_POL2_AGE_NOTE':'Возраст в beta15 только для чтения: проверенный интерфейс скриптов 1.13.x позволяет менять длительность карьеры, но безопасной прямой установки биологического возраста не подтверждено.',
        'CMP_POL2_IG_DESC':'Выберите одну или несколько стандартных групп интересов. Действия применяют отдельные модификаторы этих групп к странам-целям.',
        'CMP_POL2_IG_SELECT_TT':'Включить или выключить этот тип группы интересов в выборе «Политика 2.0».',
        'CMP_POL2_IG_STRENGTH_NOTE':'Меняется политическая сила группы интересов, а не фиксированный процент влияния. Итоговое влияние остаётся относительным результатом распределения политической силы.',
        'CMP_POL2_IG_APPROVAL_TT':'Заменяет наш модификатор одобрения для каждой выбранной группы интересов.',
        'CMP_POL2_IG_STRENGTH_TT':'Заменяет наш множитель политической силы для каждой выбранной группы интересов.',
        'CMP_POL2_BLOC_DESC':'Нужен режим «Блок держав» в контроллере целей и корректно отмеченный блок.',
        'CMP_POL2_BLOC_TT':'Меняет сплочённость отмеченного блока штатным эффектом игры.',
        'CMP_POL2_BLOC_NOTE':'В beta15 здесь намеренно оставлена только сплочённость. Членство, принципы и рычаги влияния остаются в старом интерфейсе CMP до отдельной переработки базовых функций.',
        'CMP_POL2_TT_TAB':'Переключить раздел «Политика 2.0».',
        'CMP_POL2_OPEN_TT':'Открыть новый контроллер персонажей, правительства, групп интересов, законов и блока держав.'
    })

    for lang,data in [('english',en),('russian',ru)]:
        hdr='l_english:' if lang=='english' else 'l_russian:'
        lines=[hdr]
        for k,v in data.items():
            esc=v.replace('"','\\"').replace('\n','\\n')
            lines.append(f' {k}: "{esc}"')
        write(ROOT/f'localization/{lang}/cmp_politics2_l_{lang}.yml','\n'.join(lines)+'\n')


def patch_gui(panel:str):
    p=ROOT/'gui/main/sakuya_main.gui'; text=p.read_text(encoding='utf-8-sig')
    # replace panel marker or insert before Economy popup marker.
    if BEGIN in text and END in text:
        a=text.index(BEGIN); b=text.index(END,a)+len(END); text=text[:a]+panel.rstrip()+text[b:]
    else:
        anchor='# CMP_ECONOMY2_BEGIN popup'
        pos=text.find(anchor)
        if pos<0: pos=text.rfind('}')
        text=text[:pos]+panel+'\n'+text[pos:]
    # beta15.6 migrates the public Politics entry into the unified Workspace.
    # The legacy panel remains generated as a fallback implementation, but no
    # second launcher competes with the single Workspace entry point.
    open_block=f'''{OPEN_BEGIN}
    # Politics 2.0 launcher migrated to the Workspace navigation in beta15.6.
{OPEN_END}'''
    if OPEN_BEGIN in text and OPEN_END in text:
        a=text.index(OPEN_BEGIN); b=text.index(OPEN_END,a)+len(OPEN_END); text=text[:a]+open_block+text[b:]
    else:
        anchor='# CMP v0.3 beta1: explicit global target status bar'
        pos=text.find(anchor)
        if pos<0: raise RuntimeError('target bar anchor not found')
        text=text[:pos]+open_block+'\n\n    '+text[pos:]
    p.write_text(text,encoding='utf-8-sig')


def gen_docs():
    audit='''# Vanilla Rework audit seed (beta15)\n\nThis is the first structured inventory for the later legacy/vanilla CMP rework. It does not remove legacy functions yet.\n\n## Confirmed audit items\n\n- B2 `Tax Income` label maps to `country_government_dividends_efficiency_add`, so the visible name does not describe the actual mechanic. Economy 2.0 already corrected this.\n- B3/B5 use dense `Shift/Alt/Ctrl/RMB` modifier semantics; the operation and magnitude are hidden in tooltips instead of being explicit controls.\n- B5 political-strength modifiers are often perceived as direct clout controls. Politics 2.0 explicitly labels them as political-strength multipliers because clout is a relative result.\n- B3 law modification has powerful direct effects (`activate_law`, `cancel_enactment`, `add_enactment_phase`, `add_enactment_setback`) but legacy UI does not consistently explain eligibility and persistence.\n- Character health/popularity in legacy B3 are modifiers, not direct SET values. Politics 2.0 labels them as boosts.\n- Power Bloc legacy functions are broad and partly destructive; beta15 only promotes cohesion to the new UI until membership/principles/leverage are audited.\n\n## Vanilla Rework rule\n\nFor every legacy control record: visible label -> tooltip -> ScriptedGui -> effect/modifier -> scope -> persistence -> eligibility -> post-tick result -> save/load result. Misleading labels are renamed before visual redesign.\n'''
    write(ROOT/'docs/VANILLA_REWORK_AUDIT_SEED.md',audit)
    audit_ru='''# Стартовый аудит Vanilla Rework (beta15)\n\nЭто первый структурированный список для будущей переработки старых функций CMP. В beta15 legacy-функции пока не удаляются.\n\n## Уже подтверждено\n\n- Старая B2-кнопка `Tax Income` фактически использует `country_government_dividends_efficiency_add`, то есть меняет эффективность государственных дивидендов, а не налоговые поступления. В Economy 2.0 название уже исправлено.\n- B3/B5 активно используют скрытые Shift/Alt/Ctrl/ПКМ-семантики: операция и величина спрятаны в tooltip вместо явного выбора.\n- Модификаторы B5 политической силы легко принять за прямую установку clout. Politics 2.0 прямо пишет, что меняется political strength, а clout остается относительным результатом.\n- B3 умеет напрямую завершать/отменять закон и менять фазы/неудачи, но старый UI не всегда объясняет допустимость действия и последствия.\n- Здоровье и популярность персонажа в B3 реализованы через modifier, а не через точный SET. В Politics 2.0 они подписаны как бонусы.\n- Legacy Power Bloc содержит много широких и потенциально разрушительных операций. В новый UI beta15 перенесена только сплоченность; членство, принципы и leverage останутся в legacy до отдельного аудита.\n\n## Правило Vanilla Rework\n\nДля каждой старой функции фиксируем: видимое название -> tooltip -> ScriptedGui -> effect/modifier -> scope -> постоянство -> условия доступности -> результат после тика -> результат после save/load. Сначала исправляем смысл и описание, затем внешний вид.\n'''
    write(ROOT/'docs/VANILLA_REWORK_AUDIT_SEED_RU.md',audit_ru)


def gen_validator():
    code=r'''#!/usr/bin/env python3
from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parents[1]
def read(p): return p.read_text(encoding='utf-8-sig',errors='replace')
gui=read(ROOT/'gui/main/sakuya_main.gui')
sgui=read(ROOT/'common/scripted_guis/cmp_politics2_sgui.txt')
eff=read(ROOT/'common/scripted_effects/cmp_politics2_effects.txt')
errors=[]
if gui.count('# CMP_POLITICS2_BEGIN popup')!=1 or gui.count('# CMP_POLITICS2_END popup')!=1: errors.append('Politics2 GUI markers')
refs=set(re.findall(r"GetScriptedGui\('([^']+)'\)",gui[gui.find('# CMP_POLITICS2_BEGIN popup'):gui.find('# CMP_POLITICS2_END popup')]))
defs=set(re.findall(r'(?m)^\s*(cmp_politics2_[a-z0-9_]+)\s*=\s*\{',sgui))
missing=sorted(x for x in refs if x.startswith('cmp_politics2_') and x not in defs)
if missing: errors.append('missing SGUI '+','.join(missing[:10]))
effrefs=set(re.findall(r'\b(cmp_politics2_[a-z0-9_]+_effect)\s*=\s*yes',sgui))
effdefs=set(re.findall(r'(?m)^\s*(cmp_politics2_[a-z0-9_]+_effect)\s*=\s*\{',eff))
missinge=sorted(effrefs-effdefs)
if missinge: errors.append('missing effects '+','.join(missinge[:10]))
# localization parity
keys=set(re.findall(r'(?:text|tooltip)\s*=\s*"(CMP_POL2_[A-Z0-9_]+)"',gui))
for lang in ['english','russian']:
    txt=read(ROOT/f'localization/{lang}/cmp_politics2_l_{lang}.yml')
    miss=[k for k in keys if not re.search(rf'(?m)^\s*{re.escape(k)}:',txt)]
    if miss: errors.append(f'{lang} missing {len(miss)} loc keys')
# readability gate for our panel
panel=gui[gui.find('# CMP_POLITICS2_BEGIN popup'):gui.find('# CMP_POLITICS2_END popup')]
fonts=[int(x) for x in re.findall(r'fontsize\s*=\s*(\d+)',panel)]
mins=[int(x) for x in re.findall(r'fontsize_min\s*=\s*(\d+)',panel)]
if fonts and min(fonts)<10: errors.append(f'fontsize below 10: {min(fonts)}')
if mins and min(mins)<10: errors.append(f'fontsize_min below 10: {min(mins)}')
print({'status':'PASS' if not errors else 'FAIL','gui_sgui_refs':len(refs),'effect_refs':len(effrefs),'loc_keys':len(keys),'min_font':min(fonts) if fonts else None,'errors':errors})
sys.exit(1 if errors else 0)
'''
    (ROOT/'tools/validate_politics2.py').write_text(code,encoding='utf-8')


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); args=ap.parse_args()
    before={p: p.read_bytes() for p in [ROOT/'common/static_modifiers/cmp_politics2_modifiers.txt',ROOT/'common/scripted_effects/cmp_politics2_effects.txt',ROOT/'common/scripted_guis/cmp_politics2_sgui.txt',ROOT/'localization/english/cmp_politics2_l_english.yml',ROOT/'localization/russian/cmp_politics2_l_russian.yml'] if p.exists()}
    gen_modifiers(); gen_effects(); gen_sgui(); gen_localization(); panel=gen_gui_panel(); patch_gui(panel); gen_docs(); gen_validator()
    if args.check:
        changed=[]
        for p,b in before.items():
            if p.read_bytes()!=b: changed.append(str(p.relative_to(ROOT)))
        # A check on an already generated tree must be stable. First-run files are allowed only outside release QA.
        if changed:
            print('CHANGED '+', '.join(changed)); return 1
        print('PASS politics2 codegen deterministic')
    else: print('generated Politics & Characters 2.0')
    return 0
if __name__=='__main__': raise SystemExit(main())
