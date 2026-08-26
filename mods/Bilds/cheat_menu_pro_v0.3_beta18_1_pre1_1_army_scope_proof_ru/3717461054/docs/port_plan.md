# Cheat Menu Pro - EU5 导航栏移植到 VIC3 实施计划

## 目标
将 EU5 Cheat Menu Pro 的全局导航栏系统移植到 Victoria 3 版本。
- 去掉旧的水平标签页系统
- 保留左侧垂直导航栏（9个按钮）+ 背景高亮 + 悬浮预览
- 所有内容面板统一使用"常用功能"的按钮网格布局
- 所有按钮为占位符，无实际功能，文字格式为"主菜单_N_XX"

## 需要修改/创建的文件

### 1. 重写 `gui/main/sakuya_main.gui`
当前为空壳窗口（17行），需重写为完整导航系统（预计约1200行）。

结构：
```
window sakuya_main_window (1280x720, centered, movable)
├── 关闭按钮 (右上角)
├── 窗口标题 (左上角, fontsize=22)
├── 背景高亮系统 (position {80,100}, size {200,460})
│   ├── 默认底层 (bkd.png, 蓝灰色调)
│   └── 9个颜色叠加层 (各按钮独特色调, 淡入/淡出动画)
├── 垂直导航栏 (position {80,110}, size {200,450})
│   └── vbox (spacing=0)
│       └── 9个按钮 (各200x50)
│           ├── 互斥点击逻辑 (Toggle + Clear)
│           ├── 悬浮追踪 (Set/Clear hover变量)
│           ├── 默认文字 (fontsize=16, 非悬浮非点击时可见)
│           ├── 激活文字 (fontsize=16, 悬浮或点击时可见)
│           ├── 悬浮图标 click.png (悬浮且未点击时)
│           ├── 点击图标 down.png (点击时)
│           └── 悬浮预览 (800x460图片, 淡入0.15s/淡出0.35s)
│               └── 预览标题 (fontsize=42, fontsize_min=24)
└── 9个内容面板 (position {280,100}, size {800,460})
    ├── 背景 (main/bk.png, 暖色调)
    ├── 分类标题 (fontsize=20, 居中)
    ├── 小节标题 (fontsize=18, 左对齐)
    └── 滚动按钮网格 (scrollbox)
        └── 4行 × 3列 = 12个占位按钮
            └── 每个 {234,40}, 文字fontsize=14/min=10
```

### 2. 复制 GFX 素材（17个文件）
从 EU5 `main_menu/gfx/interface/sakuya/` 复制到 VIC3 `gfx/interface/sakuya/`：

| 文件 | 用途 |
|------|------|
| `bkd.png` | 导航栏默认背景 |
| `bk2.png` | 按钮1-6,8,9的颜色叠加纹理 |
| `bk_btn7.png` | 按钮7专用叠加纹理 |
| `bk.png` | 按钮8叠加纹理 |
| `click.png` | 悬浮状态图标 |
| `down.png` | 点击状态图标 |
| `main/bk.png` | 内容面板背景 |
| `about/btn1.png` ~ `btn7.png` | 7张悬浮预览图 |
| `about/defult.png` | 按钮8,9的预览图（复用） |

### 3. 重写本地化文件 `localization/simp_chinese/sky_l_simp_chinese.yml`
约146个键值：
- 窗口标题 + 入口按钮提示（2个）
- 导航按钮名称（9个）
- 悬浮预览标题（9个）
- 内容面板分类标题 + 小节标题（18个）
- 占位按钮文字（9面板 × 12按钮 = 108个）

### 4. 无需修改的文件
- `gui/sakuya_button.gui` — 入口按钮，已正常工作
- `gui/scripted_widgets/sakuya_scripted_widgets.txt` — 已注册 sakuya_main_window

## EU5 → VIC3 关键适配

| EU5 | VIC3 | 说明 |
|-----|------|------|
| `text_single` / `text_multi` | `textbox` | 直接替换，属性兼容 |
| `button_regular` | `button` | 使用原生button即可 |
| `scrollbox` + `blockoverride "scrollbox_content"` | 同上 | VIC3完全支持此模式 |
| `using = bg_diseases_situation_overview` | 去掉 | EU5专有，用简单icon替代 |
| `using = layoutpolicy_expanding` | `layoutpolicy_vertical = expanding` | VIC3写法略不同 |
| `GetVariableSystem` | 完全一致 | 无需改动 |
| 动画系统 | 完全一致 | state/duration/alpha/Animation_Curve_Default |

## 实施步骤

### Step 1: 复制GFX素材
将17个纹理文件从EU5 mod复制到VIC3 mod的 `gfx/interface/sakuya/` 目录。

### Step 2: 编写本地化文件
填充约146个键值对，占位按钮文字格式为"主菜单_N_XX"。

### Step 3: 重写 sakuya_main.gui
按以下顺序编写：
1. 窗口外壳（尺寸、可见性、关闭按钮、标题）
2. 背景高亮系统（9个颜色叠加层）
3. 导航栏 vbox（9个按钮，含完整交互逻辑）
4. 9个内容面板（各含背景、标题、滚动按钮网格）

### Step 4: 游戏内测试
验证导航栏渲染、悬浮效果、点击切换、内容面板显示、滚动功能。

## 每个导航按钮的颜色配置

| 按钮 | 纹理 | 颜色RGBA | 色调 |
|------|------|----------|------|
| 1 | bk2.png | {0.3608, 0.2941, 0.2588, 0.5} | 红 |
| 2 | bk2.png | {0.1843, 0.0863, 0.1098, 0.5} | 藏红花 |
| 3 | bk2.png | {0.2443, 0.0763, 0.1298, 0.5} | 黄 |
| 4 | bk2.png | {0.3110, 0.2984, 0.2375, 0.5} | 绿 |
| 5 | bk2.png | {0.6392, 0.5569, 0.4157, 0.5} | 青 |
| 6 | bk2.png | {0.0863, 0.1216, 0.1333, 0.5} | 蓝 |
| 7 | bk_btn7.png | {1, 1, 1, 0.8} | 特殊白 |
| 8 | bk.png | {0.8549, 0.7529, 0.4745, 0.5} | 粉/金 |
| 9 | bk2.png | {0.5, 0.5, 0.5, 0.5} | 灰 |

## 悬浮预览图Y偏移量

| 按钮 | Y偏移 | 标题对齐 | 标题位置 |
|------|-------|----------|----------|
| 1 | -10 | right\|vcenter | {-30, 0} |
| 2 | -60 | right\|vcenter | {-30, 0} |
| 3 | -110 | left\|vcenter | {30, 0} |
| 4 | -160 | left\|vcenter | {30, 0} |
| 5 | -210 | left\|vcenter | {30, 0} |
| 6 | -260 | left\|vcenter | {60, 0} |
| 7 | -310 | center | {0, 0} |
| 8 | -360 | center | {0, 0} |
| 9 | -410 | center | {0, 0} |
