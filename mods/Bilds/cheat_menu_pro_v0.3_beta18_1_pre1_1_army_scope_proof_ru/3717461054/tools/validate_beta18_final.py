#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(rel:str)->str:
    return (ROOT/rel).read_text(encoding='utf-8-sig',errors='replace')

def load(rel:str):
    return json.loads((ROOT/rel).read_text(encoding='utf-8'))

def normalize_jomini(text:str)->str:
    out=[]; i=0; n=len(text); in_str=False; esc=False
    while i<n:
        c=text[i]
        if in_str:
            out.append(c)
            if esc: esc=False
            elif c=='\\': esc=True
            elif c=='"': in_str=False
            i+=1; continue
        if c=='"': in_str=True; out.append(c); i+=1; continue
        if c=='#':
            while i<n and text[i]!='\n': i+=1
            continue
        if c.isspace(): i+=1; continue
        out.append(c); i+=1
    return ''.join(out)

def sha(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def main()->int:
    errors=[]; warnings=[]; checks={}
    build=load('registry/build.json'); navy=load('registry/navy18.json'); cat=load('registry/naval_catalog.json'); freeze=load('registry/beta18_final_freeze.json')
    expected={
      'version':'0.3-beta18-final',
      'build_id':'CMP-0.3-B18-FINAL-20260822',
      'parent_version':'0.3-beta18-RC1',
      'runtime_status':'PASS',
      'fleet_gate':'BETA18_RC1_FULL_RUNTIME_PASS; NAVY_REWORK_RELEASED',
    }
    for k,v in expected.items():
        if build.get(k)!=v: errors.append(f'build {k}: {build.get(k)!r} != {v!r}')
    if navy.get('phase')!='beta18-final': errors.append('navy phase must be beta18-final')
    final=navy.get('final',{})
    if final.get('status')!='RELEASED_RUNTIME_PASS': errors.append('final.status must be RELEASED_RUNTIME_PASS')
    if final.get('feature_freeze') is not True: errors.append('Final feature freeze missing')
    if final.get('new_gameplay_mechanics')!=0: errors.append('Final must add zero gameplay mechanics')
    if final.get('runtime_evidence')!='USER_CONFIRMED_FULL_RC1_PASS': errors.append('Final runtime acceptance missing')
    rc1=navy.get('rc1',{})
    if rc1.get('status')!='RUNTIME_PASS': errors.append('RC1 must be promoted to RUNTIME_PASS')
    if rc1.get('release_freeze') is not True or rc1.get('new_gameplay_mechanics')!=0: errors.append('RC1 freeze contract changed')
    expected_matrix={
        'fleet_composer_2_0','exact_fleet','existing_fleet_add_ships','exact_ship','flagship',
        'single_transfer','batch_transfer_same_fleet','batch_transfer_cross_fleet','retrofit_native_bridge',
        'national_supply_reserve','assigned_supply_diagnostics','port_sea_battle_damaged_destroyed',
        'immediate_tick_save_load','workspace_90_100_115_130','no_hidden_fallback','no_ghost_target'
    }
    if set(rc1.get('matrix',[]))!=expected_matrix: errors.append('RC1 regression matrix changed in Final')

    statuses={
      'fleet_target_core':'RUNTIME_PASS',
      'composer2':'RUNTIME_PASS',
      'ship_control':'RUNTIME_PASS',
      'flagship':'RUNTIME_PASS',
      'transfer':'RUNTIME_PASS',
      'retrofit':'RUNTIME_PASS_NATIVE_BRIDGE',
      'naval_logistics':'RUNTIME_PASS',
    }
    for section,value in statuses.items():
        got=navy.get(section,{}).get('status')
        if got!=value: errors.append(f'{section}.status: {got!r} != {value!r}')
    if len(cat.get('combat_hulls',[]))!=25: errors.append('Final must retain 25 combat hulls')
    if navy.get('composer2',{}).get('rows')!=5: errors.append('Final must retain five composer rows')
    if navy.get('ship_control',{}).get('max_slots')!=100: errors.append('Final must retain 100 exact Ship slots')
    if navy.get('transfer',{}).get('batch_max')!=20: errors.append('Final must retain 20-Ship transfer basket')
    if navy.get('naval_logistics',{}).get('supply_add_amounts')!=[1,10,50,100]: errors.append('Final Supply amounts changed')

    # RC1 semantic freeze: gameplay Jomini must be identical modulo comments/whitespace.
    semantic_mismatch=[]
    for rel,expected_hash in freeze.get('semantic_files',{}).items():
        p=ROOT/rel
        if not p.exists():
            semantic_mismatch.append({'file':rel,'reason':'missing'})
            continue
        got=sha(normalize_jomini(p.read_text(encoding='utf-8-sig',errors='replace')).encode('utf-8'))
        if got!=expected_hash: semantic_mismatch.append({'file':rel,'expected':expected_hash,'got':got})
    raw_mismatch=[]
    for rel,expected_hash in freeze.get('raw_data_files',{}).items():
        p=ROOT/rel
        if not p.exists(): raw_mismatch.append({'file':rel,'reason':'missing'}); continue
        got=sha(p.read_bytes())
        if got!=expected_hash: raw_mismatch.append({'file':rel,'expected':expected_hash,'got':got})
    if semantic_mismatch: errors.append(f'{len(semantic_mismatch)} frozen Navy gameplay files changed semantically')
    if raw_mismatch: errors.append(f'{len(raw_mismatch)} frozen Navy data files changed')

    gui=read('generated/workspace_shell.gui.txt')
    for mode in ['catalog','new','existing','shipctrl','transfer','logistics']:
        profiles=sorted(set(re.findall(r'name = "cmp_workspace_navy18_'+mode+r'_([a-z0-9_]+)"',gui)))
        if profiles!=['compact','large','standard','xlarge']: errors.append(f'{mode} profile parity {profiles}')
    for tok in ["InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')",'GuiScope.SetRoot(MilitaryFormation.MakeScope).End']:
        if tok not in gui: errors.append('accepted exact-Fleet route missing '+tok)
    if 'cmp_military_target_fleet' in gui: errors.append('legacy persistent fleet marker leaked into production Workspace')

    comp=read('common/scripted_effects/cmp_navy18_composition_effects.txt')
    ship=read('common/scripted_effects/cmp_navy18_ship_control_effects.txt')
    transfer=read('common/scripted_effects/cmp_navy18_transfer_effects.txt')
    logistics=read('common/scripted_effects/cmp_navy18_logistics_effects.txt')
    for tok in ['create_military_formation = {','save_temporary_scope_as = cmp_navy18_comp2_new_fleet','fleet = scope:cmp_navy18_comp2_new_fleet']:
        if tok not in comp: errors.append('composer contract missing '+tok)
    for tok in ['ordered_scope_ship = {','set_variable = cmp_navy18_exact_ship_target','set_as_flagship = yes','set_as_flagship = no']:
        if tok not in ship: errors.append('exact Ship contract missing '+tok)
    for tok in ['set_ship_owner = scope:cmp_navy18_transfer_receiver','set_ship_owner_multiple = scope:cmp_navy18_transfer_receiver','clear_ownership_transfer_fleet = yes']:
        if tok not in transfer: errors.append('transfer contract missing '+tok)
    if logistics.count('add_supply_ships = {')!=4: errors.append('Supply reserve write count changed')
    if 'num_assigned_supply_ships' not in read('common/scripted_guis/cmp_navy18_logistics_sgui.txt'): errors.append('assigned Supply diagnostic missing')
    active='\n'.join([comp,ship,transfer,logistics])
    for bad in ['kill_ship','damage_ship_hull =','damage_ship_hull_percent =','kill_crew =','kill_crew_percent =','set_ship_template','assign_supply_ships']:
        if bad in active: errors.append('unsupported/destructive Navy write in Final: '+bad)
    for bad in ['onclick = "[RetrofitShips]"','onclick = "[RetrofitShipsAndStation]"','ShipDesignerPopup.SetShipTemplate']:
        if bad in gui: errors.append('unproven direct retrofit/template route in Final: '+bad)

    # No stale pending/candidate wording in current user-facing Navy/build localization.
    loc='\n'.join(read(str(p.relative_to(ROOT))) for lang in ['russian','english'] for p in (ROOT/'localization'/lang).glob('cmp_navy18*_l_*.yml'))
    build_loc='\n'.join(read(str(p.relative_to(ROOT))) for lang in ['russian','english'] for p in (ROOT/'localization'/lang).glob('cmp_build_l_*.yml'))
    for stale in ['RC1 повторно проверяет','RC1 rechecks','RC1:','RC1_REGRESSION_PENDING','full regression pending','регрессионный прогон ожидает']:
        if stale in loc or stale in build_loc: errors.append('stale RC1 pending/candidate localization: '+stale)

    required_docs=['docs/NAVY_BETA18_FINAL_RU.md','docs/QA_SUMMARY_BETA18_FINAL_RU.md','docs/CHANGELOG_BETA18_FINAL_RU.md','docs/ROADMAP_2026-08-22_RU.md']
    for rel in required_docs:
        if not (ROOT/rel).exists(): errors.append('missing Final document '+rel)

    # Hidden legacy fallback retained by policy, but launcher must stay absent.
    ws_src=read('tools/generate_workspace_shell.py')
    m=re.search(r'def render_military_tabs.*?\ndef ',ws_src,re.S)
    if m and 'CMP_WS_MIL_TAB_FLEET_TEMPLATES' in m.group(0): errors.append('legacy Fleet Plans launcher returned')
    if not (ROOT/'common/scripted_effects/cmp_fleet_designer_effects.txt').exists(): warnings.append('legacy fallback removed; confirm rollback policy intentionally changed')

    checks.update({
      'build_id':build.get('build_id'),
      'runtime_status':build.get('runtime_status'),
      'final_status':final.get('status'),
      'rc1_runtime_pass':rc1.get('status')=='RUNTIME_PASS',
      'regression_cases':len(rc1.get('matrix',[])),
      'semantic_freeze_files':len(freeze.get('semantic_files',{})),
      'semantic_mismatches':semantic_mismatch,
      'raw_frozen_data_files':len(freeze.get('raw_data_files',{})),
      'raw_mismatches':raw_mismatch,
      'combat_hulls':len(cat.get('combat_hulls',[])),
      'composer_rows':navy.get('composer2',{}).get('rows'),
      'exact_ship_slots':navy.get('ship_control',{}).get('max_slots'),
      'transfer_batch_max':navy.get('transfer',{}).get('batch_max'),
      'supply_add_amounts':navy.get('naval_logistics',{}).get('supply_add_amounts'),
      'workspace_modes':6,
      'workspace_profiles':4,
      'new_gameplay_mechanics':final.get('new_gameplay_mechanics'),
    })
    out={'status':'PASS' if not errors else 'FAIL','checks':checks,'errors':errors,'warnings':warnings}
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return 0 if not errors else 1

if __name__=='__main__':
    raise SystemExit(main())
