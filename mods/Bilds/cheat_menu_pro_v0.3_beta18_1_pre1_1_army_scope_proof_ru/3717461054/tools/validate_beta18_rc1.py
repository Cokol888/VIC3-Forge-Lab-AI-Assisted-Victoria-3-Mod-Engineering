#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(rel):
    return (ROOT/rel).read_text(encoding='utf-8-sig',errors='replace')

def load(rel):
    return json.loads((ROOT/rel).read_text(encoding='utf-8'))

def main():
    errors=[]; warnings=[]; checks={}
    build=load('registry/build.json'); navy=load('registry/navy18.json'); cat=load('registry/naval_catalog.json')
    expected_build={
        'version':'0.3-beta18-RC1',
        'build_id':'CMP-0.3-B18-RC1-20260822',
        'parent_version':'0.3-beta18-pre5.1',
        'runtime_status':'RC1_REGRESSION_PENDING',
    }
    for k,v in expected_build.items():
        if build.get(k)!=v: errors.append(f'build {k}: {build.get(k)!r} != {v!r}')
    if navy.get('phase')!='beta18-RC1': errors.append('navy phase is not beta18-RC1')
    rc1=navy.get('rc1',{})
    if rc1.get('release_freeze') is not True: errors.append('RC1 release freeze missing')
    if rc1.get('new_gameplay_mechanics')!=0: errors.append('RC1 must add zero new gameplay mechanics')
    matrix=set(rc1.get('matrix',[]))
    expected_matrix={
        'fleet_composer_2_0','exact_fleet','existing_fleet_add_ships','exact_ship','flagship',
        'single_transfer','batch_transfer_same_fleet','batch_transfer_cross_fleet','retrofit_native_bridge',
        'national_supply_reserve','assigned_supply_diagnostics','port_sea_battle_damaged_destroyed',
        'immediate_tick_save_load','workspace_90_100_115_130','no_hidden_fallback','no_ghost_target'
    }
    if matrix!=expected_matrix: errors.append(f'RC1 matrix mismatch missing={sorted(expected_matrix-matrix)} extra={sorted(matrix-expected_matrix)}')

    # Frozen accepted foundations / current RC surfaces.
    status_expect={
        ('fleet_target_core','status'):'RUNTIME_PASS',
        ('composer2','status'):'RUNTIME_PASS',
        ('ship_control','status'):'RUNTIME_PASS',
        ('flagship','status'):'RUNTIME_PASS',
        ('transfer','status'):'CORE_RUNTIME_PASS_RC1_REGRESSION',
        ('retrofit','status'):'NATIVE_BRIDGE_CORE_RUNTIME_PASS',
        ('naval_logistics','status'):'CORE_RUNTIME_PASS_RC1_REGRESSION',
    }
    for (section,key),value in status_expect.items():
        got=navy.get(section,{}).get(key)
        if got!=value: errors.append(f'{section}.{key}: {got!r} != {value!r}')
    if len(cat.get('combat_hulls',[]))!=25: errors.append('RC1 must retain 25 combat hulls')
    if navy.get('composer2',{}).get('rows')!=5: errors.append('RC1 must retain five composer rows')
    if navy.get('ship_control',{}).get('max_slots')!=100: errors.append('RC1 must retain 100 exact-Ship slots')
    if navy.get('transfer',{}).get('batch_max')!=20: errors.append('RC1 must retain 20-Ship transfer basket max')
    if navy.get('naval_logistics',{}).get('supply_add_amounts')!=[1,10,50,100]: errors.append('RC1 Supply amounts changed')

    required=[
      'common/scripted_effects/cmp_navy18_composition_effects.txt',
      'common/scripted_effects/cmp_navy18_ship_control_effects.txt',
      'common/scripted_effects/cmp_navy18_transfer_effects.txt',
      'common/scripted_effects/cmp_navy18_logistics_effects.txt',
      'common/scripted_guis/cmp_navy18_composition_sgui.txt',
      'common/scripted_guis/cmp_navy18_ship_control_sgui.txt',
      'common/scripted_guis/cmp_navy18_transfer_sgui.txt',
      'common/scripted_guis/cmp_navy18_logistics_sgui.txt',
      'generated/workspace_shell.gui.txt'
    ]
    for rel in required:
        if not (ROOT/rel).exists(): errors.append('missing RC1 surface: '+rel)

    gui=read('generated/workspace_shell.gui.txt')
    for mode in ['catalog','new','existing','shipctrl','transfer','logistics']:
        profiles=sorted(set(re.findall(r'name = "cmp_workspace_navy18_'+mode+r'_([a-z0-9_]+)"',gui)))
        if profiles!=['compact','large','standard','xlarge']:
            errors.append(f'{mode} profile parity: {profiles}')
    # Proven exact-Fleet route, no production fallback to old CMP fleet marker.
    for tok in ["InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')",'GuiScope.SetRoot(MilitaryFormation.MakeScope).End']:
        if tok not in gui: errors.append('proven exact-Fleet route missing '+tok)
    for tok in ["GetScriptedGui('cmp_military_target_fleet_select')","AddScope('formation', MilitaryFormation.MakeScope)",'FormationPanel.SelectFormation(MilitaryFormation.Self)']:
        if tok in gui: errors.append('deprecated fleet selection route leaked: '+tok)
    if 'cmp_military_target_fleet' in gui: errors.append('legacy persistent fleet marker leaked into production Workspace')

    comp=read('common/scripted_effects/cmp_navy18_composition_effects.txt')
    ship=read('common/scripted_effects/cmp_navy18_ship_control_effects.txt')
    transfer=read('common/scripted_effects/cmp_navy18_transfer_effects.txt')
    logistics=read('common/scripted_effects/cmp_navy18_logistics_effects.txt')
    # Composer exact-new-fleet contract.
    for tok in ['create_military_formation = {','save_temporary_scope_as = cmp_navy18_comp2_new_fleet','fleet = scope:cmp_navy18_comp2_new_fleet']:
        if tok not in comp: errors.append('composer contract missing '+tok)
    # Exact Ship + flagship contract.
    for tok in ['ordered_scope_ship = {','set_variable = cmp_navy18_exact_ship_target','set_as_flagship = yes','set_as_flagship = no']:
        if tok not in ship: errors.append('exact Ship/flagship contract missing '+tok)
    # Transfer contract.
    for tok in ['set_ship_owner = scope:cmp_navy18_transfer_receiver','set_ship_owner_multiple = scope:cmp_navy18_transfer_receiver','clear_ownership_transfer_fleet = yes','cmp_navy18_transfer_batch_target']:
        if tok not in transfer: errors.append('transfer contract missing '+tok)
    if transfer.count('clear_ownership_transfer_fleet = yes')!=1: errors.append('transfer cleanup must have exactly one write site')
    # Supply country reserve only.
    if logistics.count('add_supply_ships = {')!=4: errors.append('Supply reserve must have exactly four add_supply_ships write sites')
    for n in [1,10,50,100]:
        if f'value = {n}' not in logistics: errors.append(f'Supply +{n} payload missing')
    if 'num_assigned_supply_ships' not in read('common/scripted_guis/cmp_navy18_logistics_sgui.txt'):
        errors.append('assigned Supply read diagnostic missing')
    for bad in ['remove_supply_ships','set_supply_ships','assign_supply_ships']:
        if bad in logistics: errors.append('unconfirmed Supply write present: '+bad)

    # Retrofit stays a bridge. ShipSelection and RetrofitShips are native concepts but not direct CMP writes.
    for tok in ['PopupManager.ToggleShipDesignerPopup',"InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')"]:
        if tok not in gui: errors.append('retrofit bridge missing '+tok)
    for bad in ['onclick = "[RetrofitShips]"','onclick = "[RetrofitShipsAndStation]"','ShipDesignerPopup.SetShipTemplate','set_ship_template']:
        if bad in gui or bad in '\n'.join([comp,ship,transfer,logistics]): errors.append('unproven direct retrofit/template write present: '+bad)

    # No destructive Navy writes in RC1.
    active='\n'.join([comp,ship,transfer,logistics])
    for bad in ['kill_ship','damage_ship_hull =','damage_ship_hull_percent =','kill_crew =','kill_crew_percent =']:
        if bad in active: errors.append('destructive Navy write leaked into RC1: '+bad)

    # User-facing Navy text should describe the RC rather than stale pre5 candidate messaging.
    navy_loc='\n'.join(read(str(p.relative_to(ROOT))) for lang in ['russian','english'] for p in (ROOT/'localization'/lang).glob('cmp_navy18*_l_*.yml'))
    for stale in ['beta18-pre5 проверяет','beta18-pre5.1 не добавляет','beta18-pre5 validates','beta18-pre5.1 does not add']:
        if stale in navy_loc: errors.append('stale candidate localization: '+stale)

    # Legacy plan implementation may remain only as source fallback; launcher stays hidden.
    ws_src=read('tools/generate_workspace_shell.py')
    m=re.search(r'def render_military_tabs.*?\ndef ',ws_src,re.S)
    if m and 'CMP_WS_MIL_TAB_FLEET_TEMPLATES' in m.group(0): errors.append('legacy Fleet Plans launcher returned to top tabs')
    if not (ROOT/'common/scripted_effects/cmp_fleet_designer_effects.txt').exists(): errors.append('legacy source fallback was deleted before Final parity')

    checks.update({
      'build_id':build.get('build_id'),
      'release_freeze':rc1.get('release_freeze'),
      'regression_cases':len(matrix),
      'combat_hulls':len(cat.get('combat_hulls',[])),
      'composer_rows':navy.get('composer2',{}).get('rows'),
      'exact_ship_slots':navy.get('ship_control',{}).get('max_slots'),
      'transfer_batch_max':navy.get('transfer',{}).get('batch_max'),
      'supply_add_amounts':navy.get('naval_logistics',{}).get('supply_add_amounts'),
      'workspace_modes':6,
      'workspace_profiles':4,
      'new_gameplay_mechanics':rc1.get('new_gameplay_mechanics'),
    })
    out={'status':'PASS' if not errors else 'FAIL','checks':checks,'errors':errors,'warnings':warnings}
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return 0 if not errors else 1

if __name__=='__main__':
    raise SystemExit(main())
