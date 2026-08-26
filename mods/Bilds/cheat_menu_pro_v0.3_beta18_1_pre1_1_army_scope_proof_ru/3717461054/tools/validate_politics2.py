#!/usr/bin/env python3
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
