#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(r): return (ROOT/r).read_text(encoding='utf-8-sig',errors='replace')
def load(r): return json.loads((ROOT/r).read_text(encoding='utf-8'))
def block(text,name):
 m=re.search(r'(?m)^'+re.escape(name)+r'\s*=\s*\{',text)
 if not m:return ''
 i=m.end()-1;d=0;ins=False;esc=False
 for j in range(i,len(text)):
  c=text[j]
  if ins:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':ins=False
   continue
  if c=='"':ins=True
  elif c=='{':d+=1
  elif c=='}':
   d-=1
   if d==0:return text[m.start():j+1]
 return ''
def main():
 E=[];W=[];C={}
 cfg=load('registry/navy18.json'); cat=load('registry/naval_catalog.json'); ships=load('registry/ships.json')['ships']
 hulls=cat['combat_hulls']; by={h['id']:h for h in hulls}; c2=cfg.get('composer2',{}); rows=list(range(1,c2.get('rows',0)+1)); amounts=c2.get('amounts',[]); nonzero=[a for a in amounts if a]
 if cfg.get('phase')!='beta18-final':E.append('navy18 phase must be beta18-final')
 rc1=cfg.get('rc1',{})
 if rc1.get('status')!='RUNTIME_PASS':E.append('RC1 status must be RUNTIME_PASS in beta18 Final')
 if rc1.get('release_freeze') is not True:E.append('RC1 release_freeze must be true')
 if rc1.get('new_gameplay_mechanics')!=0:E.append('RC1 must not add new gameplay mechanics')
 expected_rc1={'fleet_composer_2_0','exact_fleet','existing_fleet_add_ships','exact_ship','flagship','single_transfer','batch_transfer_same_fleet','batch_transfer_cross_fleet','retrofit_native_bridge','national_supply_reserve','assigned_supply_diagnostics','port_sea_battle_damaged_destroyed','immediate_tick_save_load','workspace_90_100_115_130','no_hidden_fallback','no_ghost_target'}
 if set(rc1.get('matrix',[]))!=expected_rc1:E.append('RC1 regression matrix mismatch')
 if c2.get('status')!='RUNTIME_PASS':E.append('composer2 status must be RUNTIME_PASS after accepted beta18-pre3')
 if rows!=[1,2,3,4,5]:E.append(f'composer2 rows mismatch {rows}')
 if amounts!=[0,1,3,5,10]:E.append(f'composer2 amounts mismatch {amounts}')
 if c2.get('duplicates')!='ALLOWED_AND_ACCUMULATED':E.append('composer2 duplicate policy mismatch')
 if c2.get('anchor_scope_key')!='cmp_navy18_comp2_new_fleet':E.append('composer2 anchor scope mismatch')
 if len(hulls)!=25 or len(ships)!=25:E.append(f'full hull coverage expected 25 got catalog={len(hulls)} ships={len(ships)}')
 if {h['id'] for h in hulls}!={s['id'] for s in ships}:E.append('ships.json must mirror naval_catalog combat hull IDs')
 expected_groups={'capital':9,'cruiser':10,'torpedo':6}; got_groups={g:sum(h['group']==g for h in hulls) for g in expected_groups}
 if got_groups!=expected_groups:E.append(f'group counts {got_groups}')
 # template contract remains conservative.
 tw=cfg.get('template_workflow',{})
 if tw.get('instant_spawn',{}).get('status')!='SUPPORTED_DEFAULT_TEMPLATE':E.append('instant template contract missing')
 if tw.get('native_designer',{}).get('entry')!='PopupManager.ToggleShipDesignerPopup':E.append('native designer bridge mismatch')
 gui=read('generated/workspace_shell.gui.txt')
 if 'onclick = "[PopupManager.ToggleShipDesignerPopup]"' not in gui:E.append('native designer button missing')
 for t in ['ShipDesignerPopup.CreateTemplate','ShipDesignerPopup.EditTemplate','ShipDesignerPopup.SetShipTemplate']:
  if t in gui:E.append('forbidden direct template write '+t)
 # Full catalog remains 25x4.
 csg=read('common/scripted_guis/cmp_navy18_catalog_sgui.txt'); cef=read('common/scripted_effects/cmp_navy18_catalog_effects.txt')
 catalog_ok=0
 for h in hulls:
  for a in cat['catalog_amounts']:
   ep=f"cmp_navy18_catalog_create_{h['id']}_{a}"
   if not block(csg,ep) or not block(cef,ep+'_effect'):E.append('missing catalog '+ep)
   else:catalog_ok+=1
 if catalog_ok!=100:E.append(f'catalog endpoints {catalog_ok} !=100')
 # Fleet Composer 2.0 endpoints.
 sg=read('common/scripted_guis/cmp_navy18_composition_sgui.txt'); ef=read('common/scripted_effects/cmp_navy18_composition_effects.txt')
 for h in hulls:
  if not block(sg,f"cmp_navy18_comp2_hull_{h['id']}_available"):E.append('composer2 availability missing '+h['id'])
 for r in rows:
  if not block(sg,f'cmp_navy18_comp2_row_{r}_has_hull'):E.append(f'composer2 row {r} has-hull state missing')
  if not block(sg,f'cmp_navy18_comp2_row_{r}_ready'):E.append(f'composer2 row {r} ready state missing')
  for h in hulls:
   hid=h['id']
   for ep in [f'cmp_navy18_comp2_row_{r}_hull_{hid}_selected',f'cmp_navy18_comp2_select_row_{r}_hull_{hid}']:
    if not block(sg,ep):E.append('composer2 endpoint missing '+ep)
  for a in amounts:
   for ep in [f'cmp_navy18_comp2_row_{r}_count_{a}_selected',f'cmp_navy18_comp2_select_row_{r}_count_{a}']:
    if not block(sg,ep):E.append('composer2 endpoint missing '+ep)
 for ep in ['cmp_navy18_comp2_has_any_ship','cmp_navy18_comp2_ready','cmp_navy18_comp2_create_fleet','cmp_navy18_comp2_clear']:
  if not block(sg,ep):E.append('composer2 core SGUI missing '+ep)
 create=block(ef,'cmp_navy18_comp2_create_fleet_effect')
 if not create:E.append('composer2 create effect missing')
 else:
  expected_anchor=len(rows)*len(hulls)*len(nonzero)
  anchor_count=create.count('create_military_formation = {')
  temp_scope_count=create.count('save_temporary_scope_as = cmp_navy18_comp2_new_fleet')
  create_ship_count=len(re.findall(r'(?m)^\s*create_ship\s*=\s*\{',create))
  expected_create_ship=len(rows)*len(hulls)*sum(nonzero)
  if anchor_count!=expected_anchor:E.append(f'composer2 anchor branches {anchor_count}!={expected_anchor}')
  if temp_scope_count!=expected_anchor:E.append(f'composer2 temporary exact-fleet captures {temp_scope_count}!={expected_anchor}')
  if create_ship_count!=expected_create_ship:E.append(f'composer2 static create_ship payloads {create_ship_count}!={expected_create_ship}')
  for tok in ['exists = scope:cmp_navy18_comp2_new_fleet','fleet = scope:cmp_navy18_comp2_new_fleet','cmp_navy18_comp2_anchor_row','hq_region = scope:cmp_navy18_hq_region']:
   if tok not in create:E.append('composer2 creation contract missing '+tok)
  for forbidden in ['cmp_military_target_fleet','ordered_military_formation','sakuya_main_04_01_marked_navy_list']:
   if forbidden in create:E.append('composer2 leaked existing-fleet resolver '+forbidden)
  C['composer2_anchor_branches']=anchor_count; C['composer2_static_create_ship_payloads']=create_ship_count
 # Presets fill variables only and do not create anything.
 for p in cfg['presets']:
  pb=block(ef,f"cmp_navy18_preset_{p['id']}_effect")
  if not pb:E.append('preset effect missing '+p['id'])
  elif 'create_military_formation' in pb or re.search(r'(?m)^\s*create_ship\s*=',pb):E.append('preset executes fleet creation '+p['id'])
 # beta18-pre2.4 exact fleet scope is now accepted baseline.
 core=cfg.get('fleet_target_core',{})
 expected_core={
  'status':'RUNTIME_PASS',
  'selection_action':"InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')",
  'legacy_marker':'FALLBACK_ONLY'
 }
 for k,v in expected_core.items():
  if core.get(k)!=v:E.append(f'fleet_target_core {k} mismatch: {core.get(k)}')
 target_sg=read('common/scripted_guis/cmp_military_target_sgui.txt')
 probe=block(target_sg,'cmp_military_native_fleet_root_probe'); owner_probe=block(target_sg,'cmp_military_native_fleet_owner_probe')
 if 'is_shown = { always = yes }' not in probe:E.append('accepted root probe missing minimal always=yes')
 if 'owner = { is_player = yes }' not in owner_probe:E.append('accepted owner probe missing owner=player')
 for tok in ["InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')",'cmp_military_native_fleet_root_probe','cmp_military_native_fleet_owner_probe']:
  if tok not in gui:E.append('accepted fleet scope route missing '+tok)
 for forbidden in ['FormationPanel.SelectFormation(MilitaryFormation.Self)',"GetScriptedGui('cmp_military_target_fleet_select')","GetScriptedGui('cmp_military_target_fleet_entry_selected')"]:
  if forbidden in gui:E.append('deprecated fleet marker/selection route leaked '+forbidden)
 # Existing-fleet candidate remains available but must not leak legacy marker resolver.
 fsg=read('common/scripted_guis/cmp_fleet_builder_sgui.txt'); fef=read('common/scripted_effects/cmp_fleet_builder_effects.txt')
 for h in hulls:
  sid=h['id']
  if not block(fsg,f'cmp_fleet_builder_select_{sid}'):E.append('existing selector missing '+sid)
 native_eff=block(fef,'cmp_fleet_builder_apply_native_effect')
 if native_eff:
  for forbidden in ['cmp_military_target_fleet','ordered_military_formation','sakuya_main_04_01_marked_navy_list']:
   if forbidden in native_eff:E.append('native existing-fleet effect leaked legacy resolver '+forbidden)
 # Legacy Fleet Plans source retained but launcher hidden.
 mtabs=re.search(r'def render_military_tabs.*?\ndef ',(ROOT/'tools/generate_workspace_shell.py').read_text(encoding='utf-8'),re.S)
 if mtabs and 'CMP_WS_MIL_TAB_FLEET_TEMPLATES' in mtabs.group(0):E.append('legacy Fleet Plans still in top military tabs')
 if not (ROOT/'common/scripted_effects/cmp_fleet_designer_effects.txt').exists():E.append('legacy plans fallback unexpectedly deleted')
 # Deferred writes stay deferred.
 active='\n'.join([sg,ef,csg,cef,fsg,fef])
 for t in ['set_ship_owner','set_ship_owner_multiple','clear_ownership_transfer_fleet','add_supply_ships']:
  if t in active:E.append('dedicated write leaked into core Navy effects '+t)
 # beta18-pre4 exact ship control + flagship gate.
 sc=cfg.get('ship_control',{})
 if sc.get('status')!='RUNTIME_PASS':E.append('ship_control status must be RUNTIME_PASS after accepted beta18-pre4')
 if sc.get('scope')!='ship':E.append('ship_control scope must be ship')
 if sc.get('selector')!='ordered_scope_ship' or sc.get('ordering')!='power_projection':E.append('ship_control ordered selector contract mismatch')
 if sc.get('page_size')!=20 or sc.get('max_slots')!=100:E.append('ship_control page/slot contract mismatch')
 ssg=read('common/scripted_guis/cmp_navy18_ship_control_sgui.txt'); sef=read('common/scripted_effects/cmp_navy18_ship_control_effects.txt')
 for n in range(1,101):
  for ep in [f'cmp_navy18_shipctrl_slot_{n}_available',f'cmp_navy18_shipctrl_slot_{n}_selected',f'cmp_navy18_shipctrl_select_slot_{n}']:
   if not block(ssg,ep):E.append('shipctrl endpoint missing '+ep)
  eb=block(sef,f'cmp_navy18_shipctrl_select_slot_{n}_effect')
  if not eb:E.append(f'shipctrl select effect missing slot {n}')
  else:
   for tok in ['ordered_scope_ship = {','limit = { hit_points > 0 }','order_by = power_projection',f'position = {n-1}','set_variable = cmp_navy18_exact_ship_target']:
    if tok not in eb:E.append(f'shipctrl slot {n} missing '+tok)
 for h in hulls:
  ep=f"cmp_navy18_shipctrl_type_{h['id']}"
  if not block(ssg,ep):E.append('shipctrl type probe missing '+ep)
 for ep in ['cmp_navy18_shipctrl_has_ship','cmp_navy18_shipctrl_target_lost','cmp_navy18_shipctrl_clear','cmp_navy18_shipctrl_set_flagship','cmp_navy18_shipctrl_unset_flagship','cmp_navy18_shipctrl_flagship','cmp_navy18_shipctrl_damaged','cmp_navy18_shipctrl_in_port','cmp_navy18_shipctrl_in_battle']:
  if not block(ssg,ep):E.append('shipctrl core SGUI missing '+ep)
 setflag=block(sef,'cmp_navy18_shipctrl_set_flagship_effect'); unsetflag=block(sef,'cmp_navy18_shipctrl_unset_flagship_effect')
 if 'set_as_flagship = yes' not in setflag:E.append('shipctrl set flagship write missing')
 if 'set_as_flagship = no' not in unsetflag:E.append('shipctrl unset flagship write missing')
 if sef.count('set_as_flagship = yes')!=1 or sef.count('set_as_flagship = no')!=1:E.append('flagship writes must be isolated to one set/one unset effect')
 for forbidden in ['set_ship_owner','set_ship_owner_multiple','clear_ownership_transfer_fleet','add_supply_ships','kill_ship','damage_ship_hull','damage_ship_hull_percent','kill_crew','kill_crew_percent']:
  if forbidden in sef:E.append('shipctrl premature/destructive write '+forbidden)
 if 'every_scope_fleet = {' not in block(sef,'cmp_navy18_shipctrl_clear_owner_marks_effect'):E.append('shipctrl owner mark cleanup must use every_scope_fleet')
 if 'CMP_NAVY18_MODE_SHIPCTRL' not in gui:E.append('shipctrl Workspace tab missing')
 if gui.count('cmp_navy18_shipctrl_set_flagship')<4 or gui.count('cmp_navy18_shipctrl_unset_flagship')<4:E.append('shipctrl flagship action profile parity')
 for n in range(1,101):
  if gui.count(f'cmp_navy18_shipctrl_select_slot_{n}')<4:E.append(f'shipctrl slot workspace parity {n}')
 C.update({'ship_control_slots':100,'ship_control_ordering':'power_projection','ship_control_marker':'ship scope variable','ship_control_diagnostics':['type','flagship','damaged','port','battle','hp-band','crew-band'],'flagship_write':'runtime PASS exact-ship only'})


 # beta18-pre5 exact Ship transfers: one Ship or a persistent basket of up to 20 exact Ships.
 tr=cfg.get('transfer',{})
 if tr.get('status')!='RUNTIME_PASS':E.append('transfer status must be RUNTIME_PASS in beta18 Final')
 if tr.get('source_scope')!='ship':E.append('transfer source scope must be ship')
 if tr.get('receiver')!='sakuya_mark_country_target':E.append('transfer receiver contract mismatch')
 if tr.get('single_effect')!='set_ship_owner' or tr.get('batch_effect')!='set_ship_owner_multiple':E.append('transfer effect family mismatch')
 if tr.get('batch_cleanup')!='source_country.clear_ownership_transfer_fleet=yes':E.append('transfer cleanup contract mismatch')
 if tr.get('batch_marker')!='cmp_navy18_transfer_batch_target' or tr.get('batch_max')!=20:E.append('transfer basket contract mismatch')
 tsg=read('common/scripted_guis/cmp_navy18_transfer_sgui.txt'); tef=read('common/scripted_effects/cmp_navy18_transfer_effects.txt')
 transfer_core=[
  'cmp_navy18_transfer_receiver_ready','cmp_navy18_transfer_receiver_missing','cmp_navy18_transfer_receiver_self','cmp_navy18_transfer_receiver_no_port',
  'cmp_navy18_transfer_exact_eligible','cmp_navy18_transfer_exact_in_batch','cmp_navy18_transfer_has_batch','cmp_navy18_transfer_batch_valid','cmp_navy18_transfer_batch_invalid',
  'cmp_navy18_transfer_add_exact','cmp_navy18_transfer_remove_exact','cmp_navy18_transfer_clear_batch','cmp_navy18_transfer_single','cmp_navy18_transfer_batch',
  'cmp_navy18_transfer_result_added','cmp_navy18_transfer_result_removed','cmp_navy18_transfer_result_single','cmp_navy18_transfer_result_batch','cmp_navy18_transfer_result_cleared'
 ]
 for ep in transfer_core:
  if not block(tsg,ep):E.append('transfer SGUI missing '+ep)
 for n in range(1,21):
  if not block(tsg,f'cmp_navy18_transfer_batch_count_{n}'):E.append(f'transfer batch-count state missing {n}')
 for ep in ['cmp_navy18_transfer_add_exact_effect','cmp_navy18_transfer_remove_exact_effect','cmp_navy18_transfer_clear_batch_effect','cmp_navy18_transfer_resolve_receiver_effect','cmp_navy18_transfer_single_effect','cmp_navy18_transfer_batch_effect']:
  if not block(tef,ep):E.append('transfer effect missing '+ep)
 single=block(tef,'cmp_navy18_transfer_single_effect'); batch=block(tef,'cmp_navy18_transfer_batch_effect'); receiver=block(tef,'cmp_navy18_transfer_resolve_receiver_effect')
 if len(re.findall(r'(?m)^\s*set_ship_owner\s*=\s*scope:cmp_navy18_transfer_receiver\s*$',single))!=1:E.append('single transfer must contain exactly one set_ship_owner write')
 if len(re.findall(r'(?m)^\s*set_ship_owner_multiple\s*=\s*scope:cmp_navy18_transfer_receiver\s*$',batch))!=1:E.append('batch transfer must contain exactly one set_ship_owner_multiple write site')
 if batch.count('clear_ownership_transfer_fleet = yes')!=1:E.append('batch transfer must clear ownership transfer fleet exactly once')
 if 'scope:cmp_navy18_transfer_source_country = {' not in batch:E.append('batch cleanup/write must be rooted in captured source country')
 if batch.find('set_ship_owner_multiple = scope:cmp_navy18_transfer_receiver') > batch.find('clear_ownership_transfer_fleet = yes'):E.append('batch cleanup occurs before ownership writes')
 if 'remove_variable = cmp_navy18_transfer_batch_target' not in batch:E.append('batch transfer must remove basket marker before/with transfer')
 for tok in ['has_variable = sakuya_mark_country_target','NOT = { is_player = yes }','has_port_country = yes','save_temporary_scope_as = cmp_navy18_transfer_receiver']:
  if tok not in receiver:E.append('transfer receiver resolver missing '+tok)
 for tok in ['hit_points > 0','NOT = { is_in_battle = yes }','NOT = { is_flagship = yes }']:
  if tok not in single or tok not in batch:E.append('transfer safe-state gate missing '+tok)
 # Transfer writes are isolated to the dedicated effect file.
 all_nontransfer='\n'.join([sg,ef,csg,cef,fsg,fef,sef])
 for tok in ['set_ship_owner =','set_ship_owner_multiple =','clear_ownership_transfer_fleet = yes']:
  if tok in all_nontransfer:E.append('transfer write leaked outside dedicated transfer effects: '+tok)
 for forbidden in ['kill_ship','damage_ship_hull','damage_ship_hull_percent','kill_crew','kill_crew_percent','add_supply_ships']:
  if forbidden in tef:E.append('transfer destructive/deferred write '+forbidden)
 if 'CMP_NAVY18_MODE_TRANSFER' not in gui:E.append('transfer Workspace tab missing')
 for ep in ['cmp_navy18_transfer_add_exact','cmp_navy18_transfer_remove_exact','cmp_navy18_transfer_clear_batch','cmp_navy18_transfer_single','cmp_navy18_transfer_batch']:
  if gui.count(ep)<4:E.append('transfer Workspace profile parity '+ep)
 for n in range(1,21):
  if gui.count(f'cmp_navy18_transfer_batch_count_{n}')<4:E.append(f'transfer batch-count Workspace parity {n}')
 C.update({'transfer_status':'core runtime pass / RC1 regression','transfer_single':'set_ship_owner','transfer_batch':'set_ship_owner_multiple','transfer_batch_max':20,'transfer_cleanup':'source country','transfer_blocked_states':['dead','battle','flagship']})

 # beta18-pre5.1 Retrofit native bridge + Naval Logistics.
 retrofit=cfg.get('retrofit',{}); logistics=cfg.get('naval_logistics',{}); supply_cfg=cfg.get('supply_ships',{})
 if retrofit.get('status')!='RUNTIME_PASS_NATIVE_BRIDGE':E.append('retrofit status must be RUNTIME_PASS_NATIVE_BRIDGE')
 if retrofit.get('designer_entry')!='PopupManager.ToggleShipDesignerPopup':E.append('retrofit designer bridge mismatch')
 if retrofit.get('fleet_panel_entry')!="InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')":E.append('retrofit native fleet-panel bridge mismatch')
 if retrofit.get('direct_cmp_write')!='DEFERRED_UNPROVEN_BINDING':E.append('retrofit direct-write policy mismatch')
 if logistics.get('status')!='RUNTIME_PASS':E.append('naval logistics status must be RUNTIME_PASS in beta18 Final')
 if logistics.get('national_supply_effect')!='add_supply_ships':E.append('naval logistics supply write mismatch')
 if logistics.get('supply_add_amounts')!=[1,10,50,100]:E.append('naval logistics add amounts mismatch')
 if logistics.get('formation_assigned_target')!='num_assigned_supply_ships':E.append('naval logistics assigned diagnostic mismatch')
 if supply_cfg.get('status')!='SUPPORTED_COUNTRY_RESERVE_WRITE_FORMATION_DIAGNOSTIC':E.append('supply_ships status mismatch')
 lsg=read('common/scripted_guis/cmp_navy18_logistics_sgui.txt'); lef=read('common/scripted_effects/cmp_navy18_logistics_effects.txt')
 for n in [1,10,50,100]:
  for ep in [f'cmp_navy18_supply_add_{n}',f'cmp_navy18_supply_result_{n}']:
   if not block(lsg,ep):E.append('logistics SGUI missing '+ep)
  eb=block(lef,f'cmp_navy18_supply_add_{n}_effect')
  if not eb:E.append(f'logistics supply effect missing +{n}')
  else:
   if eb.count('add_supply_ships = {')!=1:E.append(f'logistics +{n} must contain exactly one add_supply_ships write')
   if f'value = {n}' not in eb:E.append(f'logistics +{n} value mismatch')
 for ep in ['cmp_navy18_supply_maintenance_good','cmp_navy18_supply_maintenance_medium','cmp_navy18_supply_maintenance_bad','cmp_navy18_supply_assigned_0','cmp_navy18_supply_assigned_1','cmp_navy18_supply_assigned_2','cmp_navy18_supply_assigned_3','cmp_navy18_supply_assigned_4','cmp_navy18_supply_assigned_5','cmp_navy18_supply_assigned_6_10','cmp_navy18_supply_assigned_11_20','cmp_navy18_supply_assigned_21_50','cmp_navy18_supply_assigned_51_plus']:
  if not block(lsg,ep):E.append('logistics diagnostic SGUI missing '+ep)
 for tok in ['supply_ship_maintenance_fulfillment >= 0.75','num_assigned_supply_ships = 0','num_assigned_supply_ships >= 51']:
  if tok not in lsg:E.append('logistics documented diagnostic missing '+tok)
 if lef.count('add_supply_ships = {')!=4:E.append('add_supply_ships writes must be isolated to four logistics effects')
 for forbidden in ['set_ship_owner','set_ship_owner_multiple','clear_ownership_transfer_fleet','set_as_flagship','kill_ship','damage_ship_hull','kill_crew','RetrofitShips =','RetrofitShipsAndStation =']:
  if forbidden in lef:E.append('logistics file contains unrelated/unproven write '+forbidden)
 # Supply writes must not leak into all other Navy effect families.
 other_navy_effects='\n'.join([ef,cef,fef,sef,tef])
 if 'add_supply_ships' in other_navy_effects:E.append('add_supply_ships leaked outside dedicated logistics effects')
 # Retrofit stays a native UI bridge; no direct retrofit command is invoked by CMP.
 for tok in ['PopupManager.ToggleShipDesignerPopup',"InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')",'CMP_NAVY18_MODE_LOGISTICS']:
  if tok not in gui:E.append('logistics/retrofit Workspace bridge missing '+tok)
 for forbidden in ['onclick = "[RetrofitShips]"','onclick = "[RetrofitShipsAndStation]"','onclick = "[CancelRetrofitShips]"']:
  if forbidden in gui:E.append('unproven direct native retrofit command exposed '+forbidden)
 for n in [1,10,50,100]:
  if gui.count(f'cmp_navy18_supply_add_{n}')<4:E.append(f'logistics supply +{n} Workspace parity')
 for ep in ['cmp_navy18_supply_assigned_0','cmp_navy18_supply_assigned_6_10','cmp_navy18_supply_assigned_51_plus']:
  if gui.count(ep)<4:E.append('logistics assigned-supply Workspace parity '+ep)
 C.update({'retrofit':'native bridge only','supply_reserve_write':'add_supply_ships country scope','supply_add_amounts':[1,10,50,100],'assigned_supply_diagnostic':'num_assigned_supply_ships','supply_direct_assignment':'deferred'})

 # Four profile parity and 5x25 row selector UI parity.
 for mode in ['catalog','new','existing','shipctrl','transfer','logistics']:
  gotp=sorted(set(re.findall(r'name = "cmp_workspace_navy18_'+mode+r'_([a-z0-9_]+)"',gui)))
  if gotp!=['compact','large','standard','xlarge']:E.append(f'profile parity {mode}={gotp}')
 for r in rows:
  for h in hulls:
   ep=f"cmp_navy18_comp2_select_row_{r}_hull_{h['id']}"
   if gui.count(ep)<4:E.append('composer2 workspace hull parity '+ep)
  for a in amounts:
   ep=f'cmp_navy18_comp2_select_row_{r}_count_{a}'
   if gui.count(ep)<4:E.append('composer2 workspace count parity '+ep)
 if gui.count('cmp_navy18_comp2_create_fleet')<4:E.append('composer2 create action profile parity')
 # Localization parity.
 keys=set(re.findall(r'(?:text|tooltip)\s*=\s*"(CMP_NAVY18_[A-Z0-9_]+)"',gui)); miss=[]
 for lang in ['russian','english']:
  txt='\n'.join(p.read_text(encoding='utf-8-sig',errors='replace') for p in (ROOT/'localization'/lang).glob('*.yml'))
  for k in keys:
   if not re.search(r'(?m)^\s*'+re.escape(k)+r':',txt):miss.append(lang+':'+k)
 if miss:E.append(f'navy localization missing {len(miss)}: '+', '.join(miss[:10]))
 C.update({'combat_hulls':25,'catalog_creation':catalog_ok,'composer2_rows':len(rows),'composer2_row_hull_choices':len(rows)*len(hulls),'composer2_counts':amounts,'composer2_strategy':'anchor create_military_formation + exact temporary fleet + create_ship rows','duplicate_hulls':'allowed/additive','fleet_target_core':'pre2.4 runtime PASS','exact_ship_control':'pre4 runtime PASS','native_designer_bridge':True,'instant_template':'default','legacy_plans_top_tab':False,'workspace_profiles':4,'localization_keys':len(keys)})
 print(json.dumps({'status':'PASS' if not E else 'FAIL','checks':C,'errors':E,'warnings':W},ensure_ascii=False,indent=2));return 0 if not E else 1
if __name__=='__main__':raise SystemExit(main())
