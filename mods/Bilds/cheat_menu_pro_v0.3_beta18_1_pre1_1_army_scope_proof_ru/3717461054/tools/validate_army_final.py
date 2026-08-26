#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def read(rel): return (ROOT/rel).read_text(encoding='utf-8-sig',errors='replace')
def load(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))

def block(text,name):
    m=re.search(r'(?m)^\s*'+re.escape(name)+r'\s*=\s*\{',text)
    if not m: return None
    start=m.start(); i=m.end()-1; depth=0; ins=False; esc=False
    for j in range(i,len(text)):
        ch=text[j]
        if ins:
            if esc: esc=False
            elif ch=='\\': esc=True
            elif ch=='"': ins=False
            continue
        if ch=='"': ins=True
        elif ch=='{': depth+=1
        elif ch=='}':
            depth-=1
            if depth==0: return text[start:j+1]
    return None

def unit_lines(body):
    return [(u,int(c)) for u,c in re.findall(
        r'combat_unit\s*=\s*\{\s*type\s*=\s*unit_type:(combat_unit_type_[a-z0-9_]+)\s+service_type\s*=\s*regular\s+state_region\s*=\s*scope:[a-z0-9_]+\s+count\s*=\s*(\d+)\s*\}', body)]

def fail(errors,msg): errors.append(msg)

def main():
    errors=[]; warnings=[]; checks={}
    cfg=load('registry/army_final.json')
    units=load('registry/land_units.json')['units']
    providers={p['id'] for p in load('registry/providers.json')['providers']}
    by_id={u['id']:u for u in units}; by_type={u['unit_type']:u for u in units}; index={u['id']:i+1 for i,u in enumerate(units)}
    roles=defaultdict(list)
    for u in units: roles[u['role']].append(u['id'])

    # Registry/schema contract.
    if len(units)!=26: fail(errors,f'land unit catalog expected 26, got {len(units)}')
    if len(by_id)!=len(units) or len(by_type)!=len(units): fail(errors,'duplicate land unit ids/types')
    for u in units:
        if u['provider'] not in providers: fail(errors,f"unit {u['id']} unknown provider {u['provider']}")
        if u['role'] not in {'infantry','artillery','mobile','marines'}: fail(errors,f"unit {u['id']} invalid role {u['role']}")
    for role,ids in cfg['template_priority'].items():
        if role in {'same_unlock_tiebreaks'}: continue
        if not isinstance(ids,list): continue
        for uid in ids:
            if uid not in by_id: fail(errors,f'template priority {role} references unknown {uid}')
            elif by_id[uid]['role']!=role: fail(errors,f'template priority {role} contains {uid} role={by_id[uid]["role"]}')
    checks['registry']={'units':len(units),'roles':{k:len(v) for k,v in sorted(roles.items())},'providers':sorted(providers)}

    # Pinned Tech & Res provider audit contract captured from source snapshot 3472248460.
    group_role={'combat_unit_group_infantry':'infantry','combat_unit_group_marines':'marines','combat_unit_group_artillery':'artillery','combat_unit_group_cavalry':'mobile'}
    for c in cfg['tech_res_provider_contract']:
        u=by_id.get(c['id'])
        if not u: fail(errors,f"provider contract unit missing: {c['id']}"); continue
        if u['provider']!='tech_res': fail(errors,f"{c['id']} provider should be tech_res")
        if u['unlock_technology']!=c['unlock_technology']: fail(errors,f"{c['id']} unlock mismatch registry={u['unlock_technology']} provider={c['unlock_technology']}")
        want_role=group_role[c['group']]
        if u['role']!=want_role: fail(errors,f"{c['id']} role mismatch registry={u['role']} provider_group={c['group']}")
    checks['tech_res_provider_contract']={'entries':len(cfg['tech_res_provider_contract']),'status':'PASS' if not errors else 'CHECK_ERRORS'}
    ps=cfg.get('tech_res_provider_snapshot',{})
    if ps.get('workshop_id')!='3472248460' or len(ps.get('files',{}))!=3:
        fail(errors,'Tech & Res provider snapshot identity/hash manifest is incomplete')
    for rel,sha in ps.get('files',{}).items():
        if not re.fullmatch(r'[0-9a-f]{64}',sha): fail(errors,f'invalid provider snapshot SHA-256 for {rel}')
    checks['tech_res_provider_snapshot']={'workshop_id':ps.get('workshop_id'),'source_collection':ps.get('source_collection'),'files':len(ps.get('files',{}))}

    builder_e=read('common/scripted_effects/cmp_army_builder_effects.txt')
    builder_g=read('common/scripted_guis/cmp_army_builder_sgui.txt')
    amounts=cfg['builder']['amounts']
    # Exact builder selection/index/gates and 26x5 spawn matrix.
    spawn_expected=set(); spawn_seen=set()
    for uid,u in by_id.items():
        idx=index[uid]; tech=u.get('unlock_technology')
        av=block(builder_g,f'cmp_army_builder_unit_{uid}_available')
        sel=block(builder_g,f'cmp_army_builder_select_{uid}')
        if not av or not sel: fail(errors,f'builder SGUI missing availability/select for {uid}')
        else:
            gate='always = yes' if not tech else f'has_technology_researched = {tech}'
            if gate not in av: fail(errors,f'builder availability gate mismatch {uid}: expected {gate}')
            if gate not in sel: fail(errors,f'builder select gate mismatch {uid}: expected {gate}')
        selected=block(builder_g,f'cmp_army_builder_unit_{uid}_selected')
        if not selected or f'cmp_army_builder_unit_index = {idx}' not in selected: fail(errors,f'builder selected index mismatch {uid}')
        for amt in amounts:
            name=f'cmp_army_builder_spawn_{uid}_{amt}_effect'; spawn_expected.add(name)
            b=block(builder_e,name)
            if not b: fail(errors,f'missing builder spawn effect {name}'); continue
            spawn_seen.add(name)
            if 'type = army' not in b or 'hq_region = scope:cmp_army_builder_hq_region' not in b: fail(errors,f'{name} formation target contract mismatch')
            if 'service_type = regular' not in b or 'state_region = scope:cmp_army_builder_state_region' not in b: fail(errors,f'{name} combat unit scope/service mismatch')
            ul=unit_lines(b)
            if ul!=[(u['unit_type'],amt)]: fail(errors,f'{name} unit/count mismatch {ul}')
            if tech and f'has_technology_researched = {tech}' not in b: fail(errors,f'{name} missing tech gate {tech}')
    applyb=block(builder_e,'cmp_army_builder_apply_effect') or ''
    refs=set(re.findall(r'\b(cmp_army_builder_spawn_[a-z0-9_]+_\d+_effect)\s*=\s*yes',applyb))
    if refs!=spawn_expected:
        fail(errors,f'builder apply spawn ref mismatch missing={len(spawn_expected-refs)} extra={len(refs-spawn_expected)}')
    resolve=block(builder_e,'cmp_army_builder_resolve_spawn_state_effect') or ''
    for needle in ['ordered_scope_state','has_decree = decree_sakuya_mark_state','order_by = gdp','position = 0','save_scope_as = cmp_army_builder_hq_region','save_scope_as = cmp_army_builder_state_region']:
        if needle not in resolve: fail(errors,f'builder target resolver missing {needle}')
    checks['builder']={'unit_types':len(units),'amounts':amounts,'spawn_endpoints':len(spawn_seen),'expected_spawn_endpoints':len(spawn_expected)}

    # Quick preset priority/gate audit.
    preset_e=read('common/scripted_effects/cmp_army_presets_effects.txt')
    preset_g=read('common/scripted_guis/cmp_army_presets_sgui.txt')
    amount_index={v:i+1 for i,v in enumerate(amounts)}
    preset_checks={}
    for pid,p in cfg['quick_presets'].items():
        b=block(preset_e,f'cmp_army_builder_preset_{pid}_effect')
        g=block(preset_g,f'cmp_army_builder_preset_{pid}')
        if not b or not g: fail(errors,f'quick preset missing {pid}'); continue
        priority=cfg['template_priority'][p['priority_role']]
        found=[int(x) for x in re.findall(r'set_variable\s*=\s*\{\s*name\s*=\s*cmp_army_builder_unit_index\s+value\s*=\s*(\d+)\s*\}',b)]
        expected=[index[x] for x in priority]
        if found!=expected: fail(errors,f'quick preset {pid} priority mismatch found={found} expected={expected}')
        ai=re.search(r'set_variable\s*=\s*\{\s*name\s*=\s*cmp_army_builder_amount_index\s+value\s*=\s*(\d+)\s*\}',b)
        if not ai or int(ai.group(1))!=amount_index[p['amount']]: fail(errors,f'quick preset {pid} amount mismatch')
        needed=sorted({by_id[x].get('unlock_technology') for x in priority if by_id[x].get('unlock_technology')})
        if pid!='infantry_corps':
            for tech in needed:
                if f'has_technology_researched = {tech}' not in g: fail(errors,f'quick preset {pid} SGUI gate misses {tech}')
        preset_checks[pid]={'priority_entries':len(priority),'amount':p['amount'],'techs':needed}
    if preset_e.count('has_technology_researched = military_drill')<1: fail(errors,'mobile preset lost military_drill gate')
    mobile_block=block(preset_e,'cmp_army_builder_preset_mobile_corps_effect') or ''
    if len(re.findall(r'has_technology_researched\s*=\s*military_drill',mobile_block))!=1: fail(errors,'mobile quick preset must have one deterministic military_drill branch')
    checks['quick_presets']=preset_checks

    # Mixed templates: exact 392 role-choice branches each, exact counts, unique role tuple, unlock gate included.
    mixed=read('common/scripted_effects/cmp_army_mixed_presets_effects.txt')
    pat_m=re.compile(r'    if = \{\n        limit = \{ ([^\n]+) \}\n        create_military_formation = \{\n(.*?)\n        \}\n        set_variable = \{ name = cmp_army_mixed_result value = 1 \}\n    \}',re.S)
    branches=list(pat_m.finditer(mixed))
    expected_priority={r:cfg['template_priority'][r] for r in ['infantry','artillery','mobile']}
    expected_types={r:{by_id[x]['unit_type'] for x in ids} for r,ids in expected_priority.items()}
    by_preset=defaultdict(list)
    for m in branches:
        lim,body=m.group(1),m.group(2)
        mm=re.search(r'var:cmp_army_mixed_preset_index\s*=\s*(\d+)',lim)
        if not mm: fail(errors,'mixed branch missing preset index'); continue
        pi=int(mm.group(1)); by_preset[pi].append((lim,body))
    for name,p in cfg['mixed_templates'].items():
        arr=by_preset[p['index']]
        if len(arr)!=392: fail(errors,f'mixed {name} expected 392 branches got {len(arr)}')
        sig=set()
        for lim,body in arr:
            ul=unit_lines(body)
            if len(ul)!=3: fail(errors,f'mixed {name} branch expected 3 unit lines got {len(ul)}'); continue
            role_counts={}; role_units={}
            for typ,cnt in ul:
                u=by_type.get(typ)
                if not u: fail(errors,f'mixed {name} unknown unit type {typ}'); continue
                role_counts[u['role']]=cnt; role_units[u['role']]=u['id']
                tech=u.get('unlock_technology')
                if tech and f'has_technology_researched = {tech}' not in lim: fail(errors,f'mixed {name} branch {u["id"]} lacks unlock gate {tech}')
            if role_counts!=p['counts']: fail(errors,f'mixed {name} counts mismatch {role_counts} != {p["counts"]}')
            for r,uid in role_units.items():
                if by_id[uid]['unit_type'] not in expected_types[r]: fail(errors,f'mixed {name} uses non-priority {uid} in {r}')
            sig.add(tuple(role_units.get(r) for r in ['infantry','artillery','mobile']))
        if len(sig)!=392: fail(errors,f'mixed {name} branch signatures expected 392 unique got {len(sig)}')
    if len(branches)!=1568: fail(errors,f'mixed total branches expected 1568 got {len(branches)}')
    checks['mixed_templates']={'branches':len(branches),'per_preset':{k:len(v) for k,v in sorted(by_preset.items())}}

    # Designer: every composition and role combination is exact.
    designer=read('common/scripted_effects/cmp_army_designer_effects.txt')
    pat_d=re.compile(r'    if = \{\n        limit = \{ ([^\n]+) \}\n        create_military_formation = \{\n(.*?)\n        \}\n        set_variable = \{ name = cmp_army_designer_result value = 1 \}\n    \}',re.S)
    db=list(pat_d.finditer(designer)); configs=defaultdict(list)
    sizes=cfg['designer']['sizes']; infp=cfg['designer']['infantry_percent']; artp=cfg['designer']['artillery_percent']
    for m in db:
        lim,body=m.group(1),m.group(2)
        vals=[]
        for n in ['cmp_army_designer_size_index','cmp_army_designer_inf_index','cmp_army_designer_art_index']:
            mm=re.search(r'var:'+n+r'\s*=\s*(\d+)',lim)
            vals.append(int(mm.group(1)) if mm else None)
        if None in vals: fail(errors,'designer branch missing configuration index'); continue
        configs[tuple(vals)].append((lim,body))
    for si,size in enumerate(sizes,1):
      for ii,ip in enumerate(infp,1):
       for ai,ap in enumerate(artp,1):
        key=(si,ii,ai); arr=configs.get(key,[])
        mobile_pct=100-ip-ap
        if mobile_pct==0:
            ic=round(size*ip/100)
            ac=size-ic
            mc=0
        else:
            ic=size*ip//100
            ac=size*ap//100
            mc=size-ic-ac
        exp_branches=8*7*(7 if mc else 1)
        if len(arr)!=exp_branches: fail(errors,f'designer config {key} expected {exp_branches} branches got {len(arr)}')
        sig=set()
        for lim,body in arr:
            ul=unit_lines(body); role_counts={}; role_units={}
            for typ,cnt in ul:
                u=by_type.get(typ)
                if not u: fail(errors,f'designer {key} unknown unit {typ}'); continue
                role_counts[u['role']]=cnt; role_units[u['role']]=u['id']
                tech=u.get('unlock_technology')
                if tech and f'has_technology_researched = {tech}' not in lim: fail(errors,f'designer {key} {u["id"]} lacks unlock gate {tech}')
            want={'infantry':ic,'artillery':ac}
            if mc: want['mobile']=mc
            if role_counts!=want: fail(errors,f'designer {key} counts {role_counts} != {want}')
            if not mc and 'mobile' in role_units: fail(errors,f'designer {key} zero-mobile branch contains mobile unit')
            sig.add(tuple(role_units.get(r) for r in ['infantry','artillery','mobile']))
        if len(sig)!=exp_branches: fail(errors,f'designer {key} expected {exp_branches} unique signatures got {len(sig)}')
    if len(configs)!=48: fail(errors,f'designer expected 48 configurations got {len(configs)}')
    if len(db)!=cfg['designer']['expected_explicit_branches']: fail(errors,f'designer expected {cfg["designer"]["expected_explicit_branches"]} branches got {len(db)}')
    checks['designer']={'configurations':len(configs),'branches':len(db),'zero_mobile_configurations':sum(1 for k in configs if infp[k[1]-1]+artp[k[2]-1]==100)}

    # Amphibious builder.
    amph=read('common/scripted_effects/cmp_army_amphib_effects.txt'); amph_g=read('common/scripted_guis/cmp_army_amphib_sgui.txt')
    if 'has_port_state = yes' not in (block(amph,'cmp_army_amphib_resolve_port_state_effect') or ''): fail(errors,'amphibious resolver lacks port-state gate')
    am_units=re.findall(r'create_military_formation\s*=\s*\{\s*type\s*=\s*army\s+hq_region\s*=\s*scope:cmp_army_amphib_hq_region\s+combat_unit\s*=\s*\{\s*type\s*=\s*unit_type:(combat_unit_type_[a-z0-9_]+)\s+service_type\s*=\s*regular\s+state_region\s*=\s*scope:cmp_army_amphib_state_region\s+count\s*=\s*(\d+)\s*\}\s*\}',amph)
    if len(am_units)!=8: fail(errors,f'amphibious expected 8 create branches got {len(am_units)}')
    am_counter=Counter((typ,int(cnt)) for typ,cnt in am_units)
    for uid in cfg['template_priority']['marines']:
        for amt in cfg['amphibious_builder']['amounts']:
            if am_counter[(by_id[uid]['unit_type'],amt)]!=1: fail(errors,f'amphibious missing/duplicate {uid} x{amt}')
    if 'cmp_military_target_fleet' in amph or 'transfer' in amph.lower(): fail(errors,'amphibious army builder contains undocumented automatic fleet targeting/transfer')
    for n in ['cmp_army_amphib_ready','cmp_army_amphib_apply']:
        b=block(amph_g,n) or ''
        if 'has_port_state = yes' not in b: fail(errors,f'{n} lacks port gate')
    checks['amphibious']={'create_branches':len(am_units),'amounts':cfg['amphibious_builder']['amounts'],'automatic_fleet_attachment':False}

    # Controls: modifier keys, signs, 10x5 apply grid, target contract, presets, stale variables.
    ctrl=read('common/scripted_effects/cmp_army_controls_effects.txt'); ctrl_g=read('common/scripted_guis/cmp_army_controls_sgui.txt'); mods=read('common/static_modifiers/cmp_army_controls_modifiers.txt')
    if re.search(r'cmp_army_control_[a-z_]+_level',ctrl): fail(errors,'army controls contain stale *_level variables')
    positive=cfg['controls']['positive_values']; reduction=cfg['controls']['reduction_values']
    for p in cfg['controls']['parameters']:
        mb=block(mods,p['modifier'])
        if not mb: fail(errors,f"missing static modifier {p['modifier']}")
        else:
            base=-1 if p['polarity']=='reduction' else 1
            if not re.search(r'\b'+re.escape(p['modifier_key'])+r'\s*=\s*'+re.escape(str(base))+r'(?:\.0+)?\b',mb): fail(errors,f"modifier {p['modifier']} key/base mismatch expected {p['modifier_key']}={base}")
        vals=reduction if p['polarity']=='reduction' else positive
        for vi,val in enumerate(vals,1):
            eb=block(ctrl,f"cmp_army_controls_apply_{p['id']}_{vi}_effect")
            if not eb: fail(errors,f"missing control apply {p['id']} {vi}"); continue
            if f"cmp_army_controls_parameter_index = {p['index']}" not in eb or f"cmp_army_controls_value_index = {vi}" not in eb: fail(errors,f"control indices mismatch {p['id']} {vi}")
            mm=re.search(r'add_modifier\s*=\s*\{\s*name\s*=\s*'+re.escape(p['modifier'])+r'\s+multiplier\s*=\s*([0-9.]+)',eb)
            if not mm or abs(float(mm.group(1))-val)>1e-9: fail(errors,f"control multiplier mismatch {p['id']} {vi}: {mm.group(1) if mm else None} vs {val}")
    resolver=block(ctrl,'cmp_army_controls_resolve_target_effect') or ''
    for needle in ['save_scope_as = cmp_army_controls_target','has_variable = sakuya_mark_country_target']:
        if needle not in resolver: fail(errors,f'controls target resolver missing {needle}')
    mark=read('common/diplomatic_actions/sakuya_mark_diplomatic_actions.txt')
    markb=block(mark,'sakuya_mark_country') or ''
    rem=markb.find('remove_variable = sakuya_mark_country_target'); setp=markb.find('set_variable = sakuya_mark_country_target')
    if rem<0 or setp<0 or rem>setp: fail(errors,'country mark action no longer clears previous mark before setting target')
    for preset,pcfg in cfg['controls']['presets'].items():
        eb=block(ctrl,f'cmp_army_controls_preset_{preset}_effect')
        gb=block(ctrl_g,f'cmp_army_controls_preset_{preset}')
        if not eb or not gb: fail(errors,f'controls preset missing {preset}'); continue
        for p in cfg['controls']['parameters']:
            if 'positive' in pcfg and p['polarity']=='positive': want=pcfg['positive']
            elif 'reduction' in pcfg and p['polarity']=='reduction': want=pcfg['reduction']
            else: want=pcfg.get(p['id'])
            if want is None: fail(errors,f'controls preset {preset} has no value for {p["id"]}'); continue
            mm=re.search(r'add_modifier\s*=\s*\{\s*name\s*=\s*'+re.escape(p['modifier'])+r'\s+multiplier\s*=\s*([0-9.]+)',eb)
            if not mm or abs(float(mm.group(1))-float(want))>1e-9: fail(errors,f'controls preset {preset} {p["id"]} mismatch')
    checks['controls']={'parameters':len(cfg['controls']['parameters']),'apply_endpoints':len(cfg['controls']['parameters'])*5,'presets':list(cfg['controls']['presets']),'stale_level_variables':0,'marked_target_single_mark_contract':True}

    # Mode isolation and no silent exact-army fallback.
    clearb=block(builder_e,'cmp_army_builder_clear_selection_effect') or ''
    for var in ['cmp_army_mixed_preset_index','cmp_army_designer_size_index','cmp_army_amphib_amount_index']:
        if f'remove_variable = {var}' not in clearb: fail(errors,f'builder mode clear does not clear {var}')
    for rel,name in [('common/scripted_effects/cmp_army_mixed_presets_effects.txt','cmp_army_mixed_select_balanced_effect'),('common/scripted_effects/cmp_army_designer_effects.txt','cmp_army_designer_enter_mode_effect'),('common/scripted_effects/cmp_army_amphib_effects.txt','cmp_army_amphib_enter_mode_effect')]:
        b=block(read(rel),name) or ''
        if 'cmp_army_builder_clear_selection_effect = yes' not in b and name=='cmp_army_mixed_select_balanced_effect': fail(errors,'mixed mode no longer clears builder/designer/amphib state through builder clear')
        if name!='cmp_army_mixed_select_balanced_effect':
            for var in ['cmp_army_builder_unit_index','cmp_army_mixed_preset_index']:
                if f'remove_variable = {var}' not in b: fail(errors,f'{name} does not isolate {var}')
    all_army='\n'.join(read(x) for x in ['common/scripted_effects/cmp_army_builder_effects.txt','common/scripted_effects/cmp_army_mixed_presets_effects.txt','common/scripted_effects/cmp_army_designer_effects.txt','common/scripted_effects/cmp_army_amphib_effects.txt'])
    if re.search(r'(?:ordered|random|every)_military_formation',all_army): fail(errors,'Army create workflows unexpectedly target existing military formations')
    checks['isolation']={'create_workflows_target_existing_army':False,'builder_mixed_designer_amphib_selection_isolated':True}

    # Metrics and docs contract.
    army_sgui=list((ROOT/'common/scripted_guis').glob('cmp_army_*_sgui.txt'))
    army_effects=list((ROOT/'common/scripted_effects').glob('cmp_army_*_effects.txt'))
    def top_defs(paths):
        out=[]
        for p in paths: out += re.findall(r'(?m)^\s*(cmp_[a-z0-9_]+)\s*=\s*\{',p.read_text(encoding='utf-8-sig'))
        return out
    sdefs=top_defs(army_sgui); edefs=top_defs(army_effects)
    checks['metrics']={'army_scripted_gui_definitions':len(sdefs),'army_scripted_effect_definitions':len(edefs),'builder_spawn_endpoints':len(spawn_seen),'mixed_branches':len(branches),'designer_branches':len(db),'amphibious_create_branches':len(am_units),'controls_apply_endpoints':50}

    status='PASS' if not errors else 'FAIL'
    report={'status':status,'checks':checks,'errors':errors,'warnings':warnings}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if status=='PASS' else 1

if __name__=='__main__': raise SystemExit(main())
