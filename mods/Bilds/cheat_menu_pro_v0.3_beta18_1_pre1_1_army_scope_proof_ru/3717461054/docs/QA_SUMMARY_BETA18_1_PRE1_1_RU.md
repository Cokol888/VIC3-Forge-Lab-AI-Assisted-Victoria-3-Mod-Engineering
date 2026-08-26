# QA Summary — beta18.1-pre1.1 Army Scope Proof

**Build:** `CMP-0.3-B18-1-PRE1-1-20260823`  
**Статус:** **STATIC PASS / RUNTIME PENDING**

## Выполнено

- Добавлен только read-only observer выбранной штатным UI Army.
- Добавлены `cmp_ops_army_root_probe` и `cmp_ops_army_owner_probe`.
- Добавлен native reopen bridge для exact selected `MilitaryFormation`.
- Не добавлен недоказанный Army-list accessor.
- Marine count и exact Invasion context оставлены discovery-unresolved.
- Invasion workflow остаётся manual/native.
- Исправлена гранулярность post-Final Navy semantic freeze.

## Safety contract

| Проверка | Результат |
|---|---:|
| Новые gameplay writes | 0 |
| Navy gameplay changes | 0 |
| Persistent Operations markers | 0 |
| Legacy Amphibious Builder drift | 0 |
| Frozen Navy/target raw drift | 0 |
| Navy Workspace scoped blocks | 28/28 identical |
| Workspace profiles | 90/100/115/130 |

## Static validators

- Workspace codegen: PASS
- Build identity: PASS
- Registry coverage: PASS
- UI accessibility: PASS
- beta18 Final Navy scoped freeze: PASS
- Military Operations pre1.1: PASS
- Full release validator: PASS (`0 errors`)

## Runtime gate

Главное доказательство в игре: две разные собственные Army должны независимо давать точное имя, `ROOT PASS`, `ARMY PASS` и открывать свою же штатную карточку. До этого exact Army context имеет статус **STATIC_IMPLEMENTED_RUNTIME_PENDING**.
