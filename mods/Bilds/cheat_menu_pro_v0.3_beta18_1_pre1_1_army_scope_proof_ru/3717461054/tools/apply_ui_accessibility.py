#!/usr/bin/env python3
from __future__ import annotations
import argparse,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GUI=ROOT/'gui/main/sakuya_main.gui'
RU_FILES=[
 ROOT/'localization/russian/cmp_fleet_builder_l_russian.yml',
 ROOT/'localization/russian/cmp_fleet_designer_l_russian.yml',
 ROOT/'localization/russian/cmp_army_builder_l_russian.yml',
 ROOT/'localization/russian/cmp_army_designer_l_russian.yml',
]
MARK='# CMP_UI_ACCESSIBILITY_B14'
MARK15='# CMP_UI_ACCESSIBILITY_B15_1'

def patch_gui(text:str)->str:
    first_apply = MARK not in text
    # Army builder readability: only the Army Builder scroll block, before Fleet Builder.
    a=text.index('name = "cmp_army_builder_scroll_area"')
    f=text.index('# CMP v0.3-beta8 Fleet Builder',a)
    seg=text[a:f]
    seg=seg.replace('fontsize_min = 7','fontsize_min = 10').replace('fontsize_min = 8','fontsize_min = 10').replace('fontsize_min = 9','fontsize_min = 10')
    seg=seg.replace('fontsize = 8 ','fontsize = 10 ').replace('fontsize = 9 ','fontsize = 11 ')
    seg=seg.replace('fontsize = 11 fontsize_min = 7','fontsize = 12 fontsize_min = 10')
    seg=seg.replace('fontsize = 10 fontsize_min = 8','fontsize = 11 fontsize_min = 10')
    seg=seg.replace('fontsize = 11 align = center','fontsize = 12 align = center')
    seg=seg.replace('fontsize = 10 align = center','fontsize = 11 align = center')
    text=text[:a]+seg+text[f:]
    # Fleet heading/readability. Structural relocation is applied once; sizing normalization is idempotent.
    f=text.index('# CMP v0.3-beta8 Fleet Builder')
    end=text.index('# CMP v0.3-beta5 Simple Army Controls',f)
    seg=text[f:end]
    if first_apply:
        # Ship selector parent becomes a 3-row vbox; generator fills rows.
        seg=seg.replace('widget = { position = { 160 1768 } size = { 560 118 } vbox = { spacing = 4','widget = { position = { 160 1768 } size = { 560 226 } vbox = { spacing = 5',1)
        seg=seg.replace('widget = { size = { 548 40 } hbox = { spacing = 5\n# CMP_REGISTRY_BEGIN fleet_ship_selector','widget = { size = { 548 142 } vbox = { spacing = 4\n# CMP_REGISTRY_BEGIN fleet_ship_selector',1)
        # Shift everything after ship panel by +108.
        ys=[1892,1940,2018,2050,2120,2188,2256,2324,2390,2424,2494,2538,2562,2600,2736,2770]
        for y in sorted(ys,reverse=True):
            seg=seg.replace(f'position = {{ 160 {y} }}',f'position = {{ 160 {y+108} }}')
        # Increase scroll content to retain reachability at 2560x1080.
        text_before=text[:f]
        text_before=text_before.replace('widget = { size = { 742 2840 }','widget = { size = { 742 3040 }',1)
        text=text_before+seg+text[end:]
    # General fleet readability in its now-shifted block.
    f=text.index('# CMP v0.3-beta8 Fleet Builder')
    end=text.index('# CMP v0.3-beta5 Simple Army Controls',f)
    seg=text[f:end]
    repl={
      'fontsize = 18 fontsize_min = 11':'fontsize = 20 fontsize_min = 14',
      'fontsize = 16 align = left':'fontsize = 17 align = left',
      'fontsize = 15 align = left':'fontsize = 16 align = left',
      'fontsize = 14 align = left':'fontsize = 15 align = left',
      'fontsize = 12 align = left':'fontsize = 13 align = left',
      'fontsize = 11 align = center':'fontsize = 13 align = center',
      'fontsize = 10 align = center':'fontsize = 12 align = center',
      'fontsize = 9 align = center':'fontsize = 11 align = center',
      'fontsize = 8 align = center':'fontsize = 10 align = center',
      'fontsize = 10 fontsize_min = 8':'fontsize = 12 fontsize_min = 10',
      'fontsize = 9 fontsize_min = 7':'fontsize = 11 fontsize_min = 10',
      'fontsize = 8 fontsize_min = 7':'fontsize = 10 fontsize_min = 9',
    }
    for x,y in repl.items(): seg=seg.replace(x,y)
    # Primary fleet controls larger, while preserving widths.
    seg=seg.replace('size = { 250 38 } tooltip = "CMP_FLEET_MARK_TT"','size = { 250 44 } tooltip = "CMP_FLEET_MARK_TT"')
    seg=seg.replace('size = { 242 34 } parentanchor','size = { 242 38 } parentanchor')
    seg=seg.replace('size = { 390 38 } tooltip = "CMP_FLEET_APPLY_TT"','size = { 390 44 } tooltip = "CMP_FLEET_APPLY_TT"')
    seg=seg.replace('size = { 150 38 } onclick = "[GetScriptedGui(\'cmp_fleet_builder_clear\')','size = { 150 44 } onclick = "[GetScriptedGui(\'cmp_fleet_builder_clear\')')
    seg=seg.replace('size = { 548 36 } tooltip = "CMP_TASKFORCE_PREPARE_TT"','size = { 548 44 } tooltip = "CMP_TASKFORCE_PREPARE_TT"')
    # Amount buttons are touch-friendly height.
    seg=seg.replace('size = { 90 36 }','size = { 90 42 }').replace('size = { 84 32 }','size = { 84 36 }')
    # Preset buttons: still one row but substantially more legible.
    seg=seg.replace('size = { 132 36 } tooltip = "CMP_FLEET_PRESET_','size = { 132 42 } tooltip = "CMP_FLEET_PRESET_')
    seg=seg.replace('size = { 126 32 } parentanchor','size = { 126 36 } parentanchor')
    # Designer primary selection buttons.
    seg=seg.replace('size = { 170 36 }','size = { 170 42 }').replace('size = { 164 32 }','size = { 164 36 }')
    # Add a static marker used by accessibility validator.
    if first_apply: seg=seg.replace('# CMP v0.3-beta8 Fleet Builder',MARK+'\n            # CMP v0.3-beta8 Fleet Builder',1)
    text=text[:f]+seg+text[end:]

    # beta15.1 second readability pass. Runs once structurally and is then idempotent.
    second_apply = MARK15 not in text
    a=text.index('name = "cmp_army_builder_scroll_area"')
    f=text.index('# CMP v0.3-beta8 Fleet Builder',a)
    army=text[a:f]
    def bump_fonts(block):
        import re
        fmap={8:11,9:12,10:12,11:13,12:14,13:14,14:15,15:16,16:17,17:18,18:20,20:22}
        block=re.sub(r'fontsize\s*=\s*(\d+)',lambda m:f"fontsize = {fmap.get(int(m.group(1)), int(m.group(1)))}",block)
        block=re.sub(r'fontsize_min\s*=\s*(\d+)',lambda m:f"fontsize_min = {max(11,int(m.group(1)))}",block)
        return block
    army=bump_fonts(army)
    text=text[:a]+army+text[f:]

    f=text.index('# CMP v0.3-beta8 Fleet Builder')
    end=text.index('# CMP v0.3-beta5 Simple Army Controls',f)
    fleet=text[f:end]
    # The generated ship selector has its own accessibility sizes and must stay
    # byte-stable for registry/codegen --check. Protect it from the generic bump.
    ss_a=fleet.index('# CMP_REGISTRY_BEGIN fleet_ship_selector')
    ss_b=fleet.index('# CMP_REGISTRY_END fleet_ship_selector', ss_a)+len('# CMP_REGISTRY_END fleet_ship_selector')
    ship_selector=fleet[ss_a:ss_b]
    fleet=fleet[:ss_a]+'__CMP_SHIP_SELECTOR_PROTECTED__'+fleet[ss_b:]
    fleet=bump_fonts(fleet)
    fleet=fleet.replace('__CMP_SHIP_SELECTOR_PROTECTED__',ship_selector,1)
    if second_apply:
        fleet=fleet.replace('widget = { position = { 160 1768 } size = { 560 226 }','widget = { position = { 160 1768 } size = { 560 238 }',1)
        fleet=fleet.replace('widget = { size = { 548 142 } vbox = { spacing = 4','widget = { size = { 548 154 } vbox = { spacing = 4',1)
        # New generated ship rows are 50px high. Keep later Fleet sections separated.
        def shift_after_ship(m):
            y=int(m.group(1))
            return f'position = {{ 160 {y+12} }}' if y >= 2000 else m.group(0)
        fleet=re.sub(r'position = \{ 160 (\d+) \}',shift_after_ship,fleet)
        text_before=text[:f].replace('widget = { size = { 742 3040 }','widget = { size = { 742 3100 }',1)
        text=text_before+fleet+text[end:]
    else:
        text=text[:f]+fleet+text[end:]

    # Larger primary Fleet controls and rows at the 2560x1080 target.
    f=text.index('# CMP v0.3-beta8 Fleet Builder'); end=text.index('# CMP v0.3-beta5 Simple Army Controls',f)
    fleet=text[f:end]
    for old,new in [
        ('size = { 250 44 }','size = { 250 48 }'),('size = { 242 38 }','size = { 242 42 }'),
        ('size = { 390 44 }','size = { 390 48 }'),('size = { 150 44 }','size = { 150 48 }'),
        ('size = { 90 42 }','size = { 90 46 }'),('size = { 84 36 }','size = { 84 40 }'),
        ('size = { 132 42 }','size = { 132 46 }'),('size = { 126 36 }','size = { 126 40 }'),
        ('size = { 170 42 }','size = { 170 46 }'),('size = { 164 36 }','size = { 164 40 }'),
        ('size = { 548 44 }','size = { 548 48 }')]:
        fleet=fleet.replace(old,new)
    if MARK15 not in text:
        fleet=fleet.replace('# CMP v0.3-beta8 Fleet Builder',MARK15+'\n            # CMP v0.3-beta8 Fleet Builder',1)
    text=text[:f]+fleet+text[end:]
    return text

def patch_ru(path:Path,text:str)->str:
    reps={
      'Перед каждой партией effect повторно проверяет требуемую технологию.':'Перед каждой партией эффект повторно проверяет требуемую технологию.',
      '#P Отмеченный флот: OK#!':'#P Отмеченный флот: ГОТОВО#!',
      'Beta8 использует':'Бета 8 использует',
      'Beta: проверьте':'Бета: проверьте',
      'В beta7 используется':'В бета 7 используется',
      'в beta7 не скриптуется':'в бета 7 не скриптуется',
      'В beta7 исправлен':'В бета 7 исправлен',
      'T&R Modern / Advanced':'T&R: современный / продвинутый',
      'T&R Modern Heavy Tank':'T&R: современный тяжёлый танк',
      'Modern Light Tanks':'современные лёгкие танки',
      'Требуется технология Nuclear Submarine.':'Требуется технология «Ядерная подводная лодка».',
      'в документированном 1.13 scripting API нет подтверждённого безопасного attach-effect.':'в документированном API скриптов 1.13 нет подтверждённого безопасного эффекта привязки.',
      'без их актуальных unlock-определений.':'без их актуальных условий разблокировки.',
      'транспортной и marine capacity.':'транспортной вместимостью и вместимостью морской пехоты.',
      'через 1 день и после save/load.':'через 1 день и после сохранения/загрузки.',
      'поддерживаемый tier.':'поддерживаемый уровень.',
      'конкретного tier':'конкретного уровня',
      'после runtime-проверки.':'после проверки в игре.',
      'полностью морскую formation.':'полностью морское армейское соединение.',
      'Vanilla low/mid/high Marines':'Базовые морпехи низкого/среднего/высокого уровня',
      'unlock-gates':'условия разблокировки',
    }
    for a,b in reps.items(): text=text.replace(a,b)
    return text

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); args=ap.parse_args()
    current_gui=GUI.read_text(encoding='utf-8-sig')
    expected_gui=patch_gui(current_gui)
    if args.check:
        bad=[]
        if expected_gui != current_gui: bad.append('gui accessibility transform is stale')
        if MARK not in current_gui: bad.append('gui accessibility marker missing')
        for p in RU_FILES:
            t=p.read_text(encoding='utf-8-sig')
            if patch_ru(p,t)!=t: bad.append(str(p.relative_to(ROOT)))
        if bad: print('FAIL ui accessibility',*bad,sep='\n'); return 1
        print('PASS ui accessibility + RU cleanup'); return 0
    GUI.write_text(expected_gui,encoding='utf-8-sig')
    for p in RU_FILES:
        p.write_text(patch_ru(p,p.read_text(encoding='utf-8-sig')),encoding='utf-8-sig')
    print('PASS applied beta14 accessibility')
    return 0
if __name__=='__main__': raise SystemExit(main())
