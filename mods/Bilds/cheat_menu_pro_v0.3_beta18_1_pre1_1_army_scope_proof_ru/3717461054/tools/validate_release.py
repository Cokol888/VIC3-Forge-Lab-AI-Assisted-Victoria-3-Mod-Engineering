#!/usr/bin/env python3
"""Static validation for CMP beta11+.
Use a full base-mod overlay for cross-reference checks:
  python3 tools/validate_release.py --overlay /path/to/full/3717461054+patch
"""
from __future__ import annotations
import argparse, io, json, re, subprocess, sys
from functools import lru_cache
from pathlib import Path

PATCH_ROOT=Path(__file__).resolve().parents[1]

@lru_cache(maxsize=None)
def read(p): return p.read_text(encoding='utf-8-sig',errors='replace')

def strip_comments_strings(s):
    # Release validation needs structural Jomini text, not literal contents.
    # Strip quoted strings and then comments using compiled C-level regex operations;
    # this is materially faster for multi-megabyte generated Workspace GUI files.
    s = re.sub(r'"(?:\\.|[^"\\])*"', '""', s)
    return re.sub(r'(?m)#.*$', '', s)

@lru_cache(maxsize=None)
def cleaned(p): return strip_comments_strings(read(p))

def brace_balance_cleaned(t):
    bal=0; minbal=0
    for c in t:
        if c=='{': bal+=1
        elif c=='}': bal-=1; minbal=min(minbal,bal)
    return bal,minbal

def defs(paths):
    d={}
    for p in paths:
        # Stream the cleaned text instead of allocating two full splitline lists.
        # This matters for generated Navy effect files with hundreds of thousands of lines.
        depth=0
        for clean in io.StringIO(cleaned(p)):
            if depth==0:
                m=re.match(r'\s*([A-Za-z0-9_:.]+)\s*=\s*\{', clean)
                if m:
                    d.setdefault(m.group(1),[]).append(str(p))
            depth += clean.count('{') - clean.count('}')
    return d

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--overlay',type=Path,default=PATCH_ROOT); args=ap.parse_args()
    root=args.overlay
    result={'status':'PASS','checks':{},'errors':[],'warnings':[]}
    build_identity_gen=PATCH_ROOT/'tools/generate_build_identity.py'
    if build_identity_gen.exists():
        cp0=subprocess.run([sys.executable,str(build_identity_gen),'--check'],capture_output=True,text=True)
        result['checks']['build_identity_codegen_check']=cp0.stdout.strip()
        if cp0.returncode: result['errors'].append('build identity check failed: '+cp0.stdout+cp0.stderr)
    staffing_gen=PATCH_ROOT/'tools/generate_staffing2.py'
    if staffing_gen.exists():
        cps=subprocess.run([sys.executable,str(staffing_gen),'--check'],capture_output=True,text=True)
        result['checks']['staffing2_codegen_check']=cps.stdout.strip()
        if cps.returncode: result['errors'].append('Staffing Coverage 2.1 codegen check failed: '+cps.stdout+cps.stderr)
    coverage_validator=PATCH_ROOT/'tools/validate_registry_coverage.py'
    if coverage_validator.exists():
        cpc=subprocess.run([sys.executable,str(coverage_validator)],capture_output=True,text=True)
        try: coverage_report=json.loads(cpc.stdout)
        except Exception: coverage_report={'status':'FAIL','stdout':cpc.stdout,'stderr':cpc.stderr}
        result['checks']['registry_coverage']=coverage_report
        if cpc.returncode or coverage_report.get('status')!='PASS': result['errors'].append('registry coverage validator failed')

    regions_validator=PATCH_ROOT/'tools/validate_regions_operations.py'
    if regions_validator.exists():
        cpr=subprocess.run([sys.executable,str(regions_validator)],capture_output=True,text=True)
        try: regions_report=json.loads(cpr.stdout)
        except Exception: regions_report={'status':'FAIL','stdout':cpr.stdout,'stderr':cpr.stderr}
        result['checks']['regions_operations']=regions_report
        if cpr.returncode or regions_report.get('status')!='PASS': result['errors'].append('Regions operations validator failed')
    army_validator=PATCH_ROOT/'tools/validate_army_final.py'
    if army_validator.exists():
        cpa=subprocess.run([sys.executable,str(army_validator)],capture_output=True,text=True)
        try: army_report=json.loads(cpa.stdout)
        except Exception: army_report={'status':'FAIL','stdout':cpa.stdout,'stderr':cpa.stderr}
        result['checks']['army_final']=army_report
        if cpa.returncode or army_report.get('status')!='PASS': result['errors'].append('Army Final validator failed')
    navy_validator=PATCH_ROOT/'tools/validate_navy18.py'
    if navy_validator.exists():
        cpn=subprocess.run([sys.executable,str(navy_validator)],capture_output=True,text=True)
        try: navy_report=json.loads(cpn.stdout)
        except Exception: navy_report={'status':'FAIL','stdout':cpn.stdout,'stderr':cpn.stderr}
        result['checks']['navy18']=navy_report
        if cpn.returncode or navy_report.get('status')!='PASS': result['errors'].append('Navy18 validator failed')
    build_meta=json.loads((PATCH_ROOT/'registry/build.json').read_text(encoding='utf-8'))
    if build_meta.get('version')=='0.3-beta18-final':
        final_validator=PATCH_ROOT/'tools/validate_beta18_final.py'
        if final_validator.exists():
            cpf=subprocess.run([sys.executable,str(final_validator)],capture_output=True,text=True)
            try: final_report=json.loads(cpf.stdout)
            except Exception: final_report={'status':'FAIL','stdout':cpf.stdout,'stderr':cpf.stderr}
            result['checks']['beta18_final']=final_report
            if cpf.returncode or final_report.get('status')!='PASS': result['errors'].append('beta18 Final validator failed')
    else:
        freeze_validator=PATCH_ROOT/'tools/validate_navy_freeze.py'
        if freeze_validator.exists():
            cpf=subprocess.run([sys.executable,str(freeze_validator)],capture_output=True,text=True)
            try: freeze_report=json.loads(cpf.stdout)
            except Exception: freeze_report={'status':'FAIL','stdout':cpf.stdout,'stderr':cpf.stderr}
            result['checks']['navy_final_freeze']=freeze_report
            if cpf.returncode or freeze_report.get('status')!='PASS': result['errors'].append('post-Final Navy freeze validator failed')
        ops_validator=PATCH_ROOT/'tools/validate_military_operations_pre1.py'
        if ops_validator.exists():
            cpo=subprocess.run([sys.executable,str(ops_validator)],capture_output=True,text=True)
            try: ops_report=json.loads(cpo.stdout)
            except Exception: ops_report={'status':'FAIL','stdout':cpo.stdout,'stderr':cpo.stderr}
            result['checks']['military_operations_pre1']=ops_report
            if cpo.returncode or ops_report.get('status')!='PASS': result['errors'].append('Military Operations pre1 validator failed')
    # Generator determinism on patch root.
    cp=subprocess.run([sys.executable,str(PATCH_ROOT/'tools/generate_registry.py'),'--check'],capture_output=True,text=True)
    result['checks']['registry_codegen_check']=cp.stdout.strip()
    if cp.returncode: result['errors'].append('registry/codegen check failed: '+cp.stdout+cp.stderr)
    regions_gen=PATCH_ROOT/'tools/generate_regions2.py'
    if regions_gen.exists():
        cp2=subprocess.run([sys.executable,str(regions_gen),'--check'],capture_output=True,text=True)
        result['checks']['regions2_codegen_check']=cp2.stdout.strip()
        if cp2.returncode: result['errors'].append('regions2 codegen check failed: '+cp2.stdout+cp2.stderr)
    economy_gen=PATCH_ROOT/'tools/generate_economy2.py'
    if economy_gen.exists():
        cp3=subprocess.run([sys.executable,str(economy_gen),'--check'],capture_output=True,text=True)
        result['checks']['economy2_codegen_check']=cp3.stdout.strip()
        if cp3.returncode: result['errors'].append('economy2 codegen check failed: '+cp3.stdout+cp3.stderr)

    population_gen=PATCH_ROOT/'tools/generate_population2.py'
    if population_gen.exists():
        cp4=subprocess.run([sys.executable,str(population_gen),'--check'],capture_output=True,text=True)
        result['checks']['population2_codegen_check']=cp4.stdout.strip()
        if cp4.returncode: result['errors'].append('population2 codegen check failed: '+cp4.stdout+cp4.stderr)
    politics_gen=PATCH_ROOT/'tools/generate_politics2.py'
    if politics_gen.exists():
        cp5=subprocess.run([sys.executable,str(politics_gen),'--check'],capture_output=True,text=True)
        result['checks']['politics2_codegen_check']=cp5.stdout.strip()
        if cp5.returncode: result['errors'].append('politics2 codegen check failed: '+cp5.stdout+cp5.stderr)
    navy_gen=PATCH_ROOT/'tools/generate_navy18.py'
    if navy_gen.exists():
        cpn0=subprocess.run([sys.executable,str(navy_gen),'--check'],capture_output=True,text=True)
        result['checks']['navy18_codegen_check']=cpn0.stdout.strip()
        if cpn0.returncode: result['errors'].append('Navy18 codegen check failed: '+cpn0.stdout+cpn0.stderr)
    navy_catalog_gen=PATCH_ROOT/'tools/generate_navy18_catalog.py'
    if navy_catalog_gen.exists():
        cpn1=subprocess.run([sys.executable,str(navy_catalog_gen),'--check'],capture_output=True,text=True)
        result['checks']['navy18_catalog_codegen_check']=cpn1.stdout.strip()
        if cpn1.returncode: result['errors'].append('Navy18 catalog codegen check failed: '+cpn1.stdout+cpn1.stderr)
    navy_shipctrl_gen=PATCH_ROOT/'tools/generate_navy18_ship_control.py'
    if navy_shipctrl_gen.exists():
        cpn2=subprocess.run([sys.executable,str(navy_shipctrl_gen),'--check'],capture_output=True,text=True)
        result['checks']['navy18_ship_control_codegen_check']=cpn2.stdout.strip()
        if cpn2.returncode: result['errors'].append('Navy18 ship control codegen check failed: '+cpn2.stdout+cpn2.stderr)
    navy_transfer_gen=PATCH_ROOT/'tools/generate_navy18_transfer.py'
    if navy_transfer_gen.exists():
        cpn3=subprocess.run([sys.executable,str(navy_transfer_gen),'--check'],capture_output=True,text=True)
        result['checks']['navy18_transfer_codegen_check']=cpn3.stdout.strip()
        if cpn3.returncode: result['errors'].append('Navy18 transfer codegen check failed: '+cpn3.stdout+cpn3.stderr)
    navy_logistics_gen=PATCH_ROOT/'tools/generate_navy18_logistics.py'
    if navy_logistics_gen.exists():
        cpn4=subprocess.run([sys.executable,str(navy_logistics_gen),'--check'],capture_output=True,text=True)
        result['checks']['navy18_logistics_codegen_check']=cpn4.stdout.strip()
        if cpn4.returncode: result['errors'].append('Navy18 logistics codegen check failed: '+cpn4.stdout+cpn4.stderr)
    workspace_gen=PATCH_ROOT/'tools/generate_workspace_shell.py'
    if workspace_gen.exists():
        cp6=subprocess.run([sys.executable,str(workspace_gen),'--check'],capture_output=True,text=True)
        result['checks']['workspace_codegen_check']=cp6.stdout.strip()
        if cp6.returncode: result['errors'].append('workspace shell codegen check failed: '+cp6.stdout+cp6.stderr)

    jfiles=(list((root/'common').rglob('*.txt')) + list((root/'events').rglob('*.txt')) +
            list((root/'gui').rglob('*.gui')))
    bad=[]
    for p in jfiles:
        bal,minbal=brace_balance_cleaned(cleaned(p))
        if bal!=0 or minbal<0: bad.append({'file':str(p.relative_to(root)),'balance':bal,'min_balance':minbal})
    result['checks']['brace_files_checked']=len(jfiles); result['checks']['brace_failures']=bad
    if bad: result['errors'].append(f'{len(bad)} files have brace-balance problems')

    # beta18 Final freezes the runtime-PASS fleet/composer/exact-ship/transfer/retrofit/logistics surface accepted in RC1. Picker rows open the exact vanilla
    # MilitaryFormation panel, while bare MakeScope and owner probes independently prove
    # whether row MilitaryFormation can cross the GUI -> ScriptedGui boundary.
    # GetSelectedFormation remains observational until runtime proves it updates here.
    target_event=PATCH_ROOT/'events/cmp_military_target_events.txt'
    target_effect=PATCH_ROOT/'common/scripted_effects/cmp_fleet_builder_effects.txt'
    target_sgui=PATCH_ROOT/'common/scripted_guis/cmp_military_target_sgui.txt'
    fleet_sgui=PATCH_ROOT/'common/scripted_guis/cmp_fleet_builder_sgui.txt'
    workspace_gui=read(PATCH_ROOT/'generated/workspace_shell.gui.txt')
    target_contract=[]
    if target_event.exists():
        target_contract.append('obsolete one-shot fleet picker event still present')
    if 'trigger_event' in read(PATCH_ROOT/'common/scripted_effects/cmp_military_target_effects.txt'):
        target_contract.append('fleet picker still launches a one-shot event')
    for token in ['Country.GetMilitaryFormationsFleet', 'MilitaryFormation.GetNameNoFormatting',
                  "InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')", 'GetSelectedFormation',
                  'GuiScope.SetRoot(MilitaryFormation.MakeScope).End',
                  "GetScriptedGui('cmp_fleet_builder_apply_native')",
                  "GetVariableSystem.Exists('cmp_workspace_fleet_picker')"]:
        if token not in workspace_gui: target_contract.append(f'native fleet target token missing: {token}')
    for forbidden in [
        "AddScope('formation', MilitaryFormation.MakeScope)",
        "GetScriptedGui('cmp_military_target_fleet_select')",
        "GetScriptedGui('cmp_military_target_fleet_entry_selected')",
        "GetScriptedGui('cmp_military_target_fleet_clear')",
        'cmp_military_target_fleet_open', 'cmp_military_target.1'
    ]:
        if forbidden in workspace_gui:
            target_contract.append(f'legacy fleet target path leaked into production Workspace: {forbidden}')
    # Native fleet-panel open is intentionally reused by the RC1 Retrofit bridge.
    # Picker row parity is validated by native_rows below; do not globally require exactly four calls.
    if workspace_gui.count("InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')") < 4:
        target_contract.append('fleet picker must render at least one native panel-open row per Workspace profile')
    if 'FormationPanel.SelectFormation(MilitaryFormation.Self)' in workspace_gui:
        target_contract.append('context-dependent FormationPanel.SelectFormation leaked into pre2.4 Workspace')
    # Native bridge row must remain click-through and must not silently write CMP target state.
    native_rows=re.findall(r"button_standard = \{[^\n]*InformationPanelBar\.OpenMilitaryFormationPanelTab\(MilitaryFormation\.Self, 'default'\)[^\n]*\n(?:.*\n){0,4}?\s*textbox = \{[^\n]*MilitaryFormation\.GetNameNoFormatting[^\n]*\}",workspace_gui)
    if len(native_rows)!=4:
        target_contract.append(f'expected 4 native panel fleet picker rows, found {len(native_rows)}')
    else:
        for row in native_rows:
            if row.count('onclick =') != 1:
                target_contract.append('native panel fleet picker row must expose exactly one onclick callback')
            if "GetVariableSystem.Clear('cmp_workspace_fleet_picker')" in row:
                target_contract.append('native panel fleet picker row closes itself before diagnostics can be observed')
            if 'alwaystransparent = yes' not in row:
                target_contract.append('native panel fleet picker label can intercept parent-button clicks')
    target_sgui_text=read(target_sgui)
    for token in ['cmp_military_native_fleet_root_probe','cmp_military_native_fleet_owner_probe','cmp_military_native_fleet_ready',
                  'cmp_military_native_fleet_blocked_battle','scope = military_formation']:
        if token not in target_sgui_text: target_contract.append(f'native target ScriptedGui token missing: {token}')
    root_probe=re.search(r'cmp_military_native_fleet_root_probe\s*=\s*\{(.*?)\n\}',target_sgui_text,re.S)
    owner_probe=re.search(r'cmp_military_native_fleet_owner_probe\s*=\s*\{(.*?)\n\}',target_sgui_text,re.S)
    if not root_probe or 'is_shown = { always = yes }' not in root_probe.group(1): target_contract.append('root probe must be minimal always=yes')
    if not owner_probe or 'owner = { is_player = yes }' not in owner_probe.group(1): target_contract.append('owner probe missing owner=player proof')
    fleet_sgui_text=read(fleet_sgui)
    native_sgui=re.search(r'cmp_fleet_builder_apply_native\s*=\s*\{(.*?)\n\}',fleet_sgui_text,re.S)
    if not native_sgui:
        target_contract.append('native existing-fleet apply ScriptedGui missing')
    else:
        body=native_sgui.group(1)
        for token in ['scope = military_formation','is_player = yes',
                      'NOT = { any_scope_ship = { is_in_battle = yes } }',
                      'cmp_fleet_builder_apply_native_effect = yes']:
            if token not in body: target_contract.append(f'native existing-fleet SGUI gate missing: {token}')
    fleet_effect_text=read(target_effect)
    native_eff=re.search(r'cmp_fleet_builder_apply_native_effect\s*=\s*\{(.*?)\n\}',fleet_effect_text,re.S)
    if not native_eff:
        target_contract.append('native existing-fleet effect missing')
    else:
        body=native_eff.group(1)
        for token in ['save_scope_as = cmp_fleet_builder_native_target','owner = {',
                      'fleet = scope:cmp_fleet_builder_native_target',
                      'clear_saved_scope = cmp_fleet_builder_native_target']:
            if token not in body: target_contract.append(f'native existing-fleet effect missing: {token}')
        for forbidden in ['cmp_military_target_fleet','ordered_military_formation','sakuya_main_04_01_marked_navy_list']:
            if forbidden in body: target_contract.append(f'native existing-fleet effect leaked legacy resolver: {forbidden}')
    result['checks']['military_target_contract']=target_contract
    if target_contract: result['errors'].append(f'{len(target_contract)} Military Target UX contract failures')

    sgui_paths=list((root/'common/scripted_guis').glob('*.txt'))
    sdefs=defs(sgui_paths)
    gui_refs=[]
    for p in (root/'gui').rglob('*.gui'):
        gui_refs += re.findall(r"GetScriptedGui\('([^']+)'\)",read(p))
    missing=sorted(set(gui_refs)-set(sdefs))
    result['checks']['unique_gui_sgui_refs']=len(set(gui_refs)); result['checks']['missing_gui_sgui_refs']=missing
    if missing: result['errors'].append(f'{len(missing)} GUI->ScriptedGui references missing')

    effect_paths=list((root/'common/scripted_effects').glob('*.txt'))
    edefs=defs(effect_paths)
    # Cross-check nested CMP scripted-effect calls as well as SGUI -> effect.
    # This catches generator defects where one scripted effect calls another
    # helper that was never generated (for example preset-only ADD amounts).
    nested_cmp_effect_refs=set()
    for p in effect_paths:
        nested_cmp_effect_refs.update(re.findall(r'\b(cmp_[a-z0-9_]+_effect)\s*=\s*(?:yes|\{)', cleaned(p)))
    missing_nested_cmp_effects=sorted(nested_cmp_effect_refs-set(edefs))
    result['checks']['nested_cmp_effect_refs']=len(nested_cmp_effect_refs)
    result['checks']['missing_nested_cmp_effects']=missing_nested_cmp_effects
    if missing_nested_cmp_effects:
        result['errors'].append(f'{len(missing_nested_cmp_effects)} nested CMP scripted-effect refs missing')

    fleet_sgui=read(PATCH_ROOT/'common/scripted_guis/cmp_fleet_builder_sgui.txt')
    fleet_effect_refs=sorted(set(re.findall(r'\b(cmp_fleet(?:_builder|_taskforce)_[a-z0-9_]+_effect)\s*=\s*yes',fleet_sgui)))
    missing_effects=sorted(set(fleet_effect_refs)-set(edefs))
    result['checks']['fleet_sgui_effect_refs']=len(fleet_effect_refs); result['checks']['missing_fleet_effects']=missing_effects
    if missing_effects: result['errors'].append(f'{len(missing_effects)} generated Fleet SGUI->effect refs missing')
    cmp_sgui_effect_refs=set()
    for p in sgui_paths:
        if p.name.startswith('cmp_'):
            cmp_sgui_effect_refs.update(re.findall(r'\b(cmp_[a-z0-9_]+_effect)\s*=\s*yes',read(p)))
    missing_cmp_effects=sorted(cmp_sgui_effect_refs-set(edefs))
    result['checks']['cmp_sgui_effect_refs']=len(cmp_sgui_effect_refs)
    result['checks']['missing_cmp_sgui_effects']=missing_cmp_effects
    if missing_cmp_effects: result['errors'].append(f'{len(missing_cmp_effects)} CMP SGUI->effect refs missing')

    cmp_dups={k:v for k,v in {**sdefs,**edefs}.items() if k.startswith('cmp_') and len(v)>1}
    result['checks']['duplicate_cmp_definitions']=cmp_dups
    if cmp_dups: result['errors'].append(f'{len(cmp_dups)} duplicate cmp_ definitions')

    ships=json.loads((PATCH_ROOT/'registry/ships.json').read_text(encoding='utf-8'))['ships']
    gui=read(PATCH_ROOT/'gui/main/sakuya_main.gui')
    result['checks']['fleet_gui_marker_begin']=gui.count('# CMP_REGISTRY_BEGIN fleet_ship_selector')
    result['checks']['fleet_gui_marker_end']=gui.count('# CMP_REGISTRY_END fleet_ship_selector')
    if result['checks']['fleet_gui_marker_begin']!=1 or result['checks']['fleet_gui_marker_end']!=1:
        result['errors'].append('fleet ship selector generation markers are not exactly 1/1')
    missing_ship_gui=[s['id'] for s in ships if f"cmp_fleet_builder_select_{s['id']}" not in gui]
    result['checks']['missing_ship_gui_entries']=missing_ship_gui
    if missing_ship_gui: result['errors'].append('ships missing from generated GUI: '+','.join(missing_ship_gui))

    loc_errors=[]
    for lang in ['english','russian']:
        txt='\n'.join(read(p) for p in (PATCH_ROOT/'localization'/lang).glob('*.yml'))
        for s in ships:
            if not re.search(rf'(?m)^\s*{re.escape(s["loc_key"])}:',txt): loc_errors.append(f'{lang}:{s["loc_key"]}')
    result['checks']['registry_ship_localization_missing']=loc_errors
    if loc_errors: result['errors'].append(f'{len(loc_errors)} ship localization keys missing')

    # CMP localization keys must be unique within each active language. Duplicate
    # keys make load order decide the visible text and are therefore a release defect.
    cmp_loc_duplicates={}
    for lang in ['english','russian']:
        seen={}
        for lp in sorted((PATCH_ROOT/f'localization/{lang}').glob('*.yml')):
            for lineno,line_text in enumerate(read(lp).splitlines(),1):
                lm=re.match(r'\s*(CMP_[A-Za-z0-9_.-]+):(?:\d+)?\s+',line_text)
                if lm:
                    seen.setdefault(lm.group(1),[]).append(f'{lp.name}:{lineno}')
        dups={k:v for k,v in seen.items() if len(v)>1}
        if dups: cmp_loc_duplicates[lang]=dups
    result['checks']['duplicate_cmp_localization_keys']=cmp_loc_duplicates
    if cmp_loc_duplicates: result['errors'].append('duplicate CMP localization keys detected')

    # New Regions & Buildings / Adaptive Staffing localization parity.
    gui_patch=read(PATCH_ROOT/'gui/main/sakuya_main.gui')
    new_loc_keys=sorted(set(re.findall(r'text\s*=\s*"(CMP_(?:RB2|STAFF_ADAPTIVE|STAFF_RESULT)_[A-Z0-9_]+)"',gui_patch)))
    new_loc_missing=[]
    for lang in ['english','russian']:
        texts='\n'.join(read(p) for p in (PATCH_ROOT/f'localization/{lang}').glob('*.yml'))
        for key in new_loc_keys:
            if not re.search(rf'(?m)^\s*{re.escape(key)}:',texts): new_loc_missing.append(f'{lang}:{key}')
    result['checks']['regions2_localization_keys']=len(new_loc_keys)
    result['checks']['regions2_localization_missing']=new_loc_missing
    if new_loc_missing: result['errors'].append(f'{len(new_loc_missing)} Regions2/Staffing localization keys missing')

    # Economy 2.0 localization and generated endpoints.
    eco_gui_keys=sorted(set(re.findall(r'(?:text|tooltip)\s*=\s*"(CMP_ECO2_[A-Z0-9_]+)"',gui_patch)))
    eco_missing=[]
    for lang in ['english','russian']:
        texts='\n'.join(read(p) for p in (PATCH_ROOT/f'localization/{lang}').glob('*.yml'))
        for key in eco_gui_keys:
            if not re.search(rf'(?m)^\s*{re.escape(key)}:',texts): eco_missing.append(f'{lang}:{key}')
    result['checks']['economy2_localization_keys']=len(eco_gui_keys)
    result['checks']['economy2_localization_missing']=eco_missing
    if eco_missing: result['errors'].append(f'{len(eco_missing)} Economy2 localization keys missing')
    eco_sgui=PATCH_ROOT/'common/scripted_guis/cmp_economy2_sgui.txt'
    if eco_sgui.exists():
        eco_refs=sorted(set(re.findall(r'\b(cmp_economy2_[a-z0-9_]+_effect)\s*=\s*yes',read(eco_sgui))))
        eco_missing_eff=sorted(set(eco_refs)-set(edefs))
        result['checks']['economy2_sgui_effect_refs']=len(eco_refs)
        result['checks']['economy2_missing_effects']=eco_missing_eff
        if eco_missing_eff: result['errors'].append(f'{len(eco_missing_eff)} Economy2 SGUI->effect refs missing')

    # Population 2.0 localization parity and dedicated UI accessibility gate.
    pop_gui_keys=sorted(set(re.findall(r'(?:text|tooltip)\s*=\s*"(CMP_POP2_[A-Z0-9_]+)"',gui_patch)))
    pop_missing=[]
    for lang in ['english','russian']:
        texts='\n'.join(read(p) for p in (PATCH_ROOT/f'localization/{lang}').glob('*.yml'))
        for key in pop_gui_keys:
            if not re.search(rf'(?m)^\s*{re.escape(key)}:',texts): pop_missing.append(f'{lang}:{key}')
    result['checks']['population2_localization_keys']=len(pop_gui_keys)
    result['checks']['population2_localization_missing']=pop_missing
    if pop_missing: result['errors'].append(f'{len(pop_missing)} Population2 localization keys missing')

    # Politics & Characters 2.0 dedicated validation.
    pol_validator=PATCH_ROOT/'tools/validate_politics2.py'
    if pol_validator.exists():
        cp=subprocess.run([sys.executable,str(pol_validator)],cwd=PATCH_ROOT,text=True,capture_output=True)
        try:
            import ast
            pol_report=ast.literal_eval(cp.stdout.strip()) if cp.stdout.strip() else {'status':'FAIL'}
        except Exception:
            pol_report={'status':'FAIL','stdout':cp.stdout,'stderr':cp.stderr}
        result['checks']['politics2']=pol_report
        if cp.returncode!=0 or pol_report.get('status')!='PASS':
            result['errors'].append('Politics2 validator failed')

    ui_validator=PATCH_ROOT/'tools/validate_ui_accessibility.py'
    if ui_validator.exists():
        cp=subprocess.run([sys.executable,str(ui_validator)],cwd=PATCH_ROOT,text=True,capture_output=True)
        try: ui_report=json.loads(cp.stdout)
        except Exception: ui_report={'status':'FAIL','stdout':cp.stdout,'stderr':cp.stderr}
        result['checks']['ui_accessibility']=ui_report
        if cp.returncode!=0 or ui_report.get('status')!='PASS':
            result['errors'].append('UI accessibility validator failed')

    # beta17-pre3 build identity and normalized military metrics.
    build_meta=json.loads((PATCH_ROOT/'registry/build.json').read_text(encoding='utf-8'))
    result['checks']['build_identity']={k:build_meta.get(k) for k in ['version','build_id','baseline_victoria','runtime_status','fleet_gate']}
    military_marker="widget = { visible = \"[GetVariableSystem.HasValue('cmp_workspace_page', 'military')]\""
    mpos=workspace_gui.find('text = "CMP_WS_MIL_TITLE"')
    mstart=workspace_gui.rfind(military_marker,0,mpos) if mpos>=0 else -1
    military_refs=[]; military_exec=[]
    if mstart>=0:
        level=0; in_str=False; esc=False; mend=None
        for i,ch in enumerate(workspace_gui[mstart:],mstart):
            if in_str:
                if esc: esc=False
                elif ch=='\\': esc=True
                elif ch=='"': in_str=False
                continue
            if ch=='"': in_str=True; continue
            if ch=='{': level+=1
            elif ch=='}':
                level-=1
                if level==0: mend=i+1; break
        if mend:
            mblock=workspace_gui[mstart:mend]
            military_refs=sorted(set(re.findall(r"GetScriptedGui\('([^']+)'\)",mblock)))
            military_exec=sorted(set(re.findall(r"GetScriptedGui\('([^']+)'\)\.Execute",mblock)))
    result['checks']['military_metrics']={
        'registered_reused_endpoints':267,
        'audited_workspace_scripted_gui_refs':len(military_refs),
        'executable_workspace_action_endpoints':len(military_exec),
        'historical_239_metric':'deprecated; replaced by explicit definitions above',
        'profile_basis':'single generated Workspace profile; parity checked separately'
    }

    registries={}
    for p in sorted((PATCH_ROOT/'registry').glob('*.json')):
        data=json.loads(p.read_text(encoding='utf-8')); key=next((k for k in ['providers','buildings','units','ships','resources','operations','amounts','parameters','policies'] if k in data),None)
        registries[p.name]=len(data[key]) if key and isinstance(data[key],list) else 'config'
    result['checks']['registries']=registries

    if result['errors']: result['status']='FAIL'
    out=PATCH_ROOT/'QA_REPORT.json'; out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'errors':len(result['errors']),'gui_refs':result['checks'].get('unique_gui_sgui_refs'),'brace_files':len(jfiles),'registries':registries},ensure_ascii=False))
    if result['errors']:
        for e in result['errors']: print('ERROR',e)
        return 1
    return 0

if __name__=='__main__': raise SystemExit(main())
