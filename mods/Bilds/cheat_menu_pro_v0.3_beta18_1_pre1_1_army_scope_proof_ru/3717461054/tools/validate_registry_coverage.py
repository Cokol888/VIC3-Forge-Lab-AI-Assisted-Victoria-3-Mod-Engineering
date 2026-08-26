#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REG=ROOT/'registry'
ALLOWED={'SUPPORTED','READ_ONLY','MANUAL','UNSAFE','UNSUPPORTED'}
POP_TYPES={'laborers','farmers','machinists','engineers','clerks','shopkeepers','academics','bureaucrats','soldiers','officers','aristocrats','capitalists','clergymen','peasants'}

def load(n): return json.loads((REG/n).read_text(encoding='utf-8'))
def main():
    errors=[]; checks={}
    build=load('build.json'); ui=load('ui_shell.json'); manifest=json.loads((ROOT/'integration_manifest.json').read_text(encoding='utf-8'))
    for k in ['version','build_id','baseline_victoria','workshop_snapshot','parent_version','runtime_status']:
        if not build.get(k): errors.append(f'build.json missing {k}')
    if ui.get('version')!=build.get('version') or ui.get('build_id')!=build.get('build_id'): errors.append('ui_shell build identity mismatch')
    if manifest.get('version')!=build.get('version') or manifest.get('build_identity',{}).get('build_id')!=build.get('build_id'): errors.append('integration manifest build identity mismatch')
    staff=load('staffing.json'); providers={p['id'] for p in load('providers.json')['providers']}; profiles=staff['profiles']; entries=staff['buildings']
    ids=[e['id'] for e in entries]; btypes=[e['building_type'] for e in entries]; sel=[e['selection_variable'] for e in entries]
    for name,vals in [('staffing ids',ids),('staffing building types',btypes),('staffing selection variables',sel)]:
        if len(vals)!=len(set(vals)): errors.append(f'duplicate {name}')
    for pid,p in profiles.items():
        if sum(p.get('weights',{}).values())!=1000: errors.append(f'profile {pid} weights != 1000')
        bad=set(p.get('weights',{}))-POP_TYPES
        if bad: errors.append(f'profile {pid} unknown pop types: {sorted(bad)}')
    for e in entries:
        if e['status'] not in ALLOWED: errors.append(f"staffing {e['id']} invalid status {e['status']}")
        if e['provider'] not in providers: errors.append(f"staffing {e['id']} unknown provider {e['provider']}")
        if e['status']=='SUPPORTED':
            if e.get('profile') not in profiles: errors.append(f"staffing {e['id']} supported without valid profile")
            if not e['selection_variable'].startswith('cmp_staffing_sel_'): errors.append(f"staffing {e['id']} is not independently selected")
        elif not e.get('reason'): errors.append(f"staffing {e['id']} excluded without reason")
    base=load('buildings.json')['buildings']; smap={e['id']:e for e in entries}
    missing_base=[b['id'] for b in base if b['id'] not in smap]
    unsupported_base=[b['id'] for b in base if b['id'] in smap and smap[b['id']]['status']!='SUPPORTED']
    if missing_base: errors.append('building operations absent from staffing coverage: '+','.join(missing_base))
    if unsupported_base: errors.append('previously supported staffing regressed: '+','.join(unsupported_base))
    legacy=Path(ROOT/'common/scripted_guis/sakuya_cheat_b6_sgui.txt').read_text(encoding='utf-8-sig')
    legacy_ids=set(re.findall(r'(?m)^sakuya_b6_build_select_([a-z0-9_]+)\s*=\s*\{',legacy))
    missing_legacy=sorted(legacy_ids-set(ids))
    if missing_legacy: errors.append('legacy building selectors without coverage status: '+','.join(missing_legacy))
    coverage=load('coverage.json')
    if set(coverage.get('allowed_statuses',[]))!=ALLOWED: errors.append('coverage allowed status contract mismatch')
    domains=coverage.get('domains',{})
    specs=[('resources','resources.json','resources'),('land_units','land_units.json','units'),('ships','ships.json','ships'),('operations','operations.json','operations')]
    for domain,fn,key in specs:
        expected={x['id'] for x in load(fn)[key]}; rows=domains.get(domain,[]); actual={x['id'] for x in rows}
        if expected!=actual: errors.append(f'{domain} coverage mismatch missing={sorted(expected-actual)} extra={sorted(actual-expected)}')
        for row in rows:
            if row['status'] not in ALLOWED: errors.append(f"{domain}:{row['id']} invalid coverage status")
    op_rows=domains.get('building_operations',[]); op_map={x['id']:x for x in op_rows}; supported_ops={x['id'] for x in base}
    if set(op_map)!=set(ids): errors.append(f"building_operations full coverage mismatch missing={sorted(set(ids)-set(op_map))} extra={sorted(set(op_map)-set(ids))}")
    if {i for i,r in op_map.items() if r.get('status')=='SUPPORTED'}!=supported_ops: errors.append('building_operations SUPPORTED set does not match buildings.json')
    for row in op_rows:
        if row.get('status') not in ALLOWED: errors.append(f"building_operations:{row.get('id')} invalid coverage status")
        if row.get('status')!='SUPPORTED' and not row.get('reason'): errors.append(f"building_operations:{row.get('id')} exclusion without reason")
    for b in base:
        if b.get('operation_status')!='SUPPORTED': errors.append(f"building registry {b['id']} operation_status is not SUPPORTED")
        if b.get('operation_policy')!='guarded_direct': errors.append(f"building registry {b['id']} operation_policy is not guarded_direct")
        if not b.get('selection_variable','').startswith('cmp_regions2_sel_'): errors.append(f"building registry {b['id']} selector is not cmp_regions2 independent")
    cov_staff={x['id']:x['status'] for x in domains.get('staffing',[])}
    if set(cov_staff)!=set(ids): errors.append('staffing coverage.json set mismatch')
    for e in entries:
        if cov_staff.get(e['id'])!=e['status']: errors.append(f"staffing coverage status mismatch {e['id']}")
    supported=sum(e['status']=='SUPPORTED' for e in entries); manual=sum(e['status']=='MANUAL' for e in entries); unsupported=sum(e['status']=='UNSUPPORTED' for e in entries)
    checks.update({'build_id':build['build_id'],'staffing_total':len(entries),'staffing_supported':supported,'staffing_manual':manual,'staffing_unsupported':unsupported,'legacy_selectors_covered':len(legacy_ids),'profiles':len(profiles),'building_operations_supported':len(base),'building_operations_covered':len(op_rows),'status_contract':sorted(ALLOWED)})
    report={'status':'FAIL' if errors else 'PASS','checks':checks,'errors':errors}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
