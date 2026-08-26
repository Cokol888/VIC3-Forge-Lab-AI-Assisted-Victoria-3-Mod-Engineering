#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n): return json.loads((ROOT/'registry'/n).read_text(encoding='utf-8'))
def read(p): return p.read_text(encoding='utf-8-sig')
def main():
    errors=[]; checks={}
    buildings=load('buildings.json')['buildings']; staffing=load('staffing.json'); ui=load('ui_shell.json'); cfg=load('regions_buildings.json'); cov=load('coverage.json')['domains']['building_operations']
    ids=[b['id'] for b in buildings]; btypes=[b['building_type'] for b in buildings]; vars_=[b['selection_variable'] for b in buildings]
    for name,xs in [('ids',ids),('building types',btypes),('selection vars',vars_)]:
        if len(xs)!=len(set(xs)): errors.append(f'duplicate operations {name}')
    if set(vars_) & {b['selection_variable'] for b in staffing['buildings']}: errors.append('operations/staffing selection variables overlap')
    if any(not v.startswith('cmp_regions2_sel_') for v in vars_): errors.append('operations selector outside cmp_regions2_sel_* contract')
    categories=ui['building_categories']; staffcats=staffing['categories']
    if [c['id'] for c in categories] != [c['id'] for c in staffcats]: errors.append('Operations categories do not match Staffing category taxonomy')
    if any(c.get('profiles',[]) != next((s.get('profiles',[]) for s in staffcats if s['id']==c['id']),None) for c in categories): errors.append('Operations category profile mapping does not match Staffing')
    cat_counts={c['id']:(len(buildings) if c['id']=='all' else sum(b.get('staffing_profile') in c.get('profiles',[]) for b in buildings)) for c in categories}
    covmap={r['id']:r for r in cov}; staffids={b['id'] for b in staffing['buildings']}
    if set(covmap)!=staffids: errors.append('building_operations coverage does not cover complete known staffing inventory')
    if {i for i,r in covmap.items() if r['status']=='SUPPORTED'}!=set(ids): errors.append('building_operations SUPPORTED coverage differs from buildings registry')
    effects=read(ROOT/'common/scripted_effects/cmp_regions2_effects.txt'); sgui=read(ROOT/'common/scripted_guis/cmp_regions2_sgui.txt'); gui=read(ROOT/'generated/workspace_shell.gui.txt')
    legacy=read(ROOT/'common/scripted_effects/sakuya_cheat_b6_effects.txt')
    for token in ['can_construct_building = $BUILDING$','can_queue_building_levels = 1','cmp_regions2_any_blocked','cmp_regions2_any_unsafe']:
        if token not in effects: errors.append('missing guarded building token: '+token)
    if 'cmp_regions2_clear_new_building_selection_effect = yes' not in legacy.split('sakuya_b6_build_select_building_effect = {',1)[-1][:300]: errors.append('legacy selector does not clear new Operations selector')
    preset_deltas=sorted({d for p in cfg['presets'] for d in p['buildings'].values()}); expected_add=sorted(set(cfg['building_amounts'])|set(preset_deltas))
    for n in expected_add:
        if not re.search(rf'(?m)^cmp_regions2_build_add_{n}_effect\s*=\s*\{{',effects): errors.append(f'missing generated ADD helper {n}')
    refs=set(re.findall(r'\b(cmp_regions2_build_add_[0-9]+_effect)\s*=\s*\{?\s*BUILDING',effects)); defs=set(re.findall(r'(?m)^(cmp_regions2_build_add_[0-9]+_effect)\s*=\s*\{',effects))
    if refs-defs: errors.append('nested Regions scripted-effect refs missing definitions: '+','.join(sorted(refs-defs)))
    # SET must never remove the building before a create/raise. REMOVE is the only allowed building remove path.
    set_blocks=re.findall(r'(?ms)^cmp_regions2_build_set_[0-9]+_effect\s*=\s*\{.*?(?=^cmp_regions2_|\Z)',effects)
    if any('remove_building' in b for b in set_blocks): errors.append('destructive remove_building found inside safe SET helper')
    if 'remove_building = $BUILDING$' not in effects: errors.append('whole-building REMOVE path missing')
    # Workspace must use one direct ScriptedGui selection callback; no shared legacy GUI selection variable.
    for bad in ['sakuya_b6_selected_building','cmp_staffing_supported_building_check']:
        # Bad tokens can occur elsewhere in legacy/global code, but not in generated shell Regions operations contract.
        if bad in gui: errors.append(f'Workspace still coupled to {bad}')
    if "cmp_workspace_building_category_menu_operations" not in gui or "cmp_workspace_building_category_menu_staffing" not in gui: errors.append('category menu instance variables are not separated')
    for b in buildings:
        if f"cmp_regions2_select_building_{b['id']}" not in sgui: errors.append(f'missing building selector SGUI {b["id"]}')
        count=gui.count(f"GetScriptedGui('cmp_regions2_select_building_{b['id']}').Execute")
        if count!=8: errors.append(f'expected 8 Workspace operation selector rows (All + category across 4 profiles) for {b["id"]}, got {count}')
    for bid in cfg['resource_capable_buildings']:
        count=gui.count(f"GetScriptedGui('cmp_regions2_select_resource_{bid}').Execute")
        if count!=4: errors.append(f'expected 4 resource selector rows for {bid}, got {count}')
    preset_isolation={}
    for pi,p in enumerate(cfg['presets'],1):
        for bid in p['buildings']:
            if bid not in ids: errors.append(f'preset {p["id"]} references unsupported operation building {bid}')
        # A cap/availability failure for one preset component must not poison the
        # rest of that preset in the same state. Each component gets a fresh
        # local state_blocked guard while aggregate result flags remain on root.
        m=re.search(rf'(?ms)^  if = \{{ limit = \{{ root = \{{ cmp_regions2_mode_preset = yes var:cmp_regions2_preset_index = {pi} \}} \}}\n(.*?)^  \}}',effects)
        if not m:
            errors.append(f'preset {p["id"]} generated block missing')
            preset_isolation[p['id']]='MISSING'
        else:
            block=m.group(1)
            resets=block.count('remove_variable = cmp_regions2_state_blocked')
            components=len(p['buildings'])
            preset_isolation[p['id']]={'components':components,'guard_resets':resets}
            if resets != components:
                errors.append(f'preset {p["id"]} must reset state_blocked before every component: {resets}/{components}')
            lines=[x.strip() for x in block.splitlines() if x.strip()]
            for i,line in enumerate(lines):
                if re.match(r'cmp_regions2_build_add_[0-9]+_effect\s*=\s*\{',line):
                    if i==0 or lines[i-1] != 'remove_variable = cmp_regions2_state_blocked':
                        errors.append(f'preset {p["id"]} component lacks isolated guard reset before {line}')
    checks.update({'operations_buildings':len(buildings),'providers':{x:sum(b['provider']==x for b in buildings) for x in sorted({b['provider'] for b in buildings})},'categories':cat_counts,'preset_deltas':preset_deltas,'generated_add_amounts':expected_add,'resource_buildings':len(cfg['resource_capable_buildings']),'safe_set':'no remove_building in SET helpers','availability_gate':'can_construct_building + can_queue_building_levels','selection_contract':'independent operations/staffing + legacy bridge','preset_component_isolation':preset_isolation})
    report={'status':'FAIL' if errors else 'PASS','checks':checks,'errors':errors}; print(json.dumps(report,ensure_ascii=False,indent=2)); return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
