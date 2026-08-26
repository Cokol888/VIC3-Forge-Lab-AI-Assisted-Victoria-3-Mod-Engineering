# UI Accessibility Foundation — beta14

Static layout profiles: **2560×1080 primary**, **3440×1440 secondary ultrawide**. Main new controls target 44–52 px heights. The audited Army/Fleet/Population blocks use minimum font sizes of 10, Population 2.0 uses a base minimum of 11, and Fleet ship selection is a two-column 268×44 layout. `tools/validate_ui_accessibility.py` checks these constraints plus EN/RU localization parity. Actual rendered QA still requires Victoria 3 at the target resolution/UI scale.
