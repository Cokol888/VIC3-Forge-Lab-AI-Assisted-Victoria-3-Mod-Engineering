#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def read(rel): return (ROOT/rel).read_text(encoding='utf-8-sig',errors='replace')
def sha(rel): return hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()

def main():
    errors=[]; warnings=[]; checks={}
    build=load('registry/build.json'); ops=load('registry/military_operations.json')
    if build.get('version')!='0.3-beta18.1-pre1.1': errors.append('unexpected build version')
    if build.get('build_id')!='CMP-0.3-B18-1-PRE1-1-20260823': errors.append('unexpected build id')
    if build.get('parent_version')!='0.3-beta18.1-pre1': errors.append('parent must be beta18.1-pre1')
    if build.get('baseline_victoria')!='1.13.10': errors.append('pre1.1 baseline must be Victoria 3 1.13.10')
    if build.get('fleet_gate')!='BETA18_FINAL_RUNTIME_PASS; NAVY_REWORK_FROZEN': errors.append('Navy freeze gate missing')
    if ops.get('phase')!='beta18.1-pre1.1': errors.append('operations phase mismatch')
    scope=ops.get('pre1_scope',{})
    if scope.get('new_gameplay_writes')!=0: errors.append('pre1.1 must add zero gameplay writes')
    if scope.get('navy_gameplay_changes')!=0: errors.append('pre1.1 must add zero Navy gameplay changes')
    if scope.get('new_persistent_markers')!=0: errors.append('pre1.1 must add zero persistent markers')
    if scope.get('workspace_change_type')!='READ_ONLY_ARMY_SCOPE_PROBE': errors.append('unexpected Workspace change type')

    caps={x['id']:x for x in ops.get('capabilities',[])}
    required={
      'country_total_marine_capacity':'SUPPORTED_READ_ONLY',
      'invasion_has_marines':'SUPPORTED_READ_ONLY_NEEDS_INVASION_SCOPE',
      'is_naval_invasion':'SUPPORTED_READ_ONLY_NEEDS_INVASION_SCOPE',
      'exact_fleet_context':'RUNTIME_PASS_REUSED_FROM_BETA18',
      'native_invasion_ui_bridge':'DISCOVERY_REQUIRED',
      'direct_auto_attach_marines':'DEFERRED_UNCONFIRMED',
      'direct_start_naval_invasion':'DEFERRED_UNCONFIRMED',
      'native_selected_army_observer':'STATIC_IMPLEMENTED_RUNTIME_PENDING',
      'exact_army_make_scope_probe':'STATIC_IMPLEMENTED_RUNTIME_PENDING',
      'country_army_list_accessor':'DISCOVERY_UNRESOLVED',
      'selected_army_marine_count':'DISCOVERY_UNRESOLVED',
    }
    for key,status in required.items():
        if caps.get(key,{}).get('status')!=status: errors.append(f'capability {key} status mismatch')

    # Preserve the released Navy semantics through the scoped post-Final freeze validator.
    freeze_validator=ROOT/'tools/validate_navy_freeze.py'
    if not freeze_validator.exists(): errors.append('missing post-Final Navy freeze validator')
    else:
        cp=subprocess.run([sys.executable,str(freeze_validator)],capture_output=True,text=True)
        if cp.returncode: errors.append('post-Final Navy freeze validator failed')

    # Legacy amphibious code must remain byte-identical during Operations discovery.
    legacy=ops.get('legacy_audit',{}).get('existing_amphibious_builder',{})
    for rel,expected in legacy.get('sha256',{}).items():
        if not (ROOT/rel).exists(): errors.append('missing legacy amphibious file '+rel)
        elif sha(rel)!=expected: errors.append('legacy amphibious discovery freeze changed '+rel)

    sgui_path=ROOT/'common/scripted_guis/cmp_military_operations_sgui.txt'
    if not sgui_path.exists(): errors.append('missing read-only Military Operations SGUI')
    else:
        sgui=read('common/scripted_guis/cmp_military_operations_sgui.txt')
        for token in ['cmp_ops_army_root_probe','scope = military_formation','always = yes','cmp_ops_army_owner_probe','is_army = yes','owner = { is_player = yes }']:
            if token not in sgui: errors.append('Army scope probe missing '+token)
        for forbidden in ['effect =','is_valid =','save_scope_as','set_variable','create_military_formation','add_combat_unit','start_invasion']:
            if forbidden in sgui: errors.append('write/mutation surface leaked into read-only Army probe: '+forbidden)
    if (ROOT/'common/scripted_effects/cmp_military_operations_effects.txt').exists():
        errors.append('pre1.1 must not add Military Operations gameplay effects')

    gui=read('generated/workspace_shell.gui.txt')
    required_gui=[
      'name = "cmp_workspace_operations_discovery"',
      '[GetSelectedFormation.IsArmy]',
      'datacontext = "[GetSelectedFormation]"',
      'MilitaryFormation.GetNameNoFormatting',
      "InformationPanelBar.OpenMilitaryFormationPanelTab(MilitaryFormation.Self, 'default')",
      "GetScriptedGui('cmp_ops_army_root_probe').IsShown(GuiScope.SetRoot(MilitaryFormation.MakeScope).End)",
      "GetScriptedGui('cmp_ops_army_owner_probe').IsShown(GuiScope.SetRoot(MilitaryFormation.MakeScope).End)",
    ]
    for token in required_gui:
        if token not in gui: errors.append('read-only Army observer missing '+token)
    # Do not guess the unresolved self-contained Army list accessor.
    for forbidden in ['GetMilitaryFormationsArmy','cmp_ops_army_target','cmp_military_operations_effects','StartNavalInvasion','start_naval_invasion']:
        if forbidden in gui: errors.append('unproven Operations surface leaked into Workspace: '+forbidden)

    for rel in ['docs/NAVY_BETA18_FINAL_RU.md','registry/beta18_final_freeze.json','registry/beta18_postfinal_navy_freeze.json']:
        if not (ROOT/rel).exists(): errors.append('missing baseline/freeze document '+rel)

    checks.update({
      'build_id':build.get('build_id'),
      'baseline_victoria':build.get('baseline_victoria'),
      'capabilities':len(caps),
      'new_gameplay_writes':scope.get('new_gameplay_writes'),
      'navy_gameplay_changes':scope.get('navy_gameplay_changes'),
      'new_persistent_markers':scope.get('new_persistent_markers'),
      'legacy_amphib_files_frozen':len(legacy.get('sha256',{})),
      'army_observer':caps.get('native_selected_army_observer',{}).get('status'),
      'army_scope_probe':caps.get('exact_army_make_scope_probe',{}).get('status'),
      'army_list_accessor':caps.get('country_army_list_accessor',{}).get('status'),
      'marine_count':caps.get('selected_army_marine_count',{}).get('status'),
      'native_invasion_bridge':caps.get('native_invasion_ui_bridge',{}).get('status'),
    })
    out={'status':'PASS' if not errors else 'FAIL','checks':checks,'errors':errors,'warnings':warnings}
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
