#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/'registry/build.json'
UI=ROOT/'registry/ui_shell.json'
MANIFEST=ROOT/'integration_manifest.json'
LOC_EN=ROOT/'localization/english/cmp_build_l_english.yml'
LOC_RU=ROOT/'localization/russian/cmp_build_l_russian.yml'

def dump_json(obj): return json.dumps(obj,ensure_ascii=False,indent=2)+'\n'
def outputs():
    b=json.loads(BUILD.read_text(encoding='utf-8'))
    ui=json.loads(UI.read_text(encoding='utf-8')); ui['version']=b['version']; ui['build_id']=b['build_id']
    mf=json.loads(MANIFEST.read_text(encoding='utf-8')); mf['version']=b['version']; mf['name']=b['name']; mf['build_identity']={k:b[k] for k in ['build_id','baseline_victoria','workshop_snapshot','parent_version','runtime_status','fleet_gate']}
    en='''l_english:\n CMP_BUILD_ID:0 "Build ID: {build_id}"\n CMP_BUILD_VERSION:0 "Version: {version}"\n CMP_BUILD_BASELINE:0 "Victoria baseline: {baseline}"\n CMP_BUILD_RUNTIME_STATUS:0 "Runtime status: {runtime}"\n CMP_BUILD_NAVY_RC_STATUS:0 "Navy beta18 Final: Runtime PASS / released"\n'''.format(build_id=b['build_id'],version=b['version'],baseline=b['baseline_victoria'],runtime=b['runtime_status'])
    ru='''l_russian:\n CMP_BUILD_ID:0 "Build ID: {build_id}"\n CMP_BUILD_VERSION:0 "Версия: {version}"\n CMP_BUILD_BASELINE:0 "База Victoria: {baseline}"\n CMP_BUILD_RUNTIME_STATUS:0 "Runtime-статус: {runtime}"\n CMP_BUILD_NAVY_RC_STATUS:0 "Navy beta18 Final: Runtime PASS / релиз"\n'''.format(build_id=b['build_id'],version=b['version'],baseline=b['baseline_victoria'],runtime=b['runtime_status'])
    return {UI:dump_json(ui),MANIFEST:dump_json(mf),LOC_EN:en,LOC_RU:ru}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); args=ap.parse_args(); out=outputs()
    if args.check:
        stale=[]
        for p,t in out.items():
            enc='utf-8-sig' if p.suffix=='.yml' else 'utf-8'
            if not p.exists() or p.read_text(encoding=enc)!=t: stale.append(str(p.relative_to(ROOT)))
        if stale: print('STALE: '+', '.join(stale),file=sys.stderr); return 1
        print('PASS: build identity is synchronized'); return 0
    for p,t in out.items(): p.write_text(t,encoding='utf-8-sig' if p.suffix=='.yml' else 'utf-8')
    print('generated build identity from registry/build.json'); return 0
if __name__=='__main__': raise SystemExit(main())
