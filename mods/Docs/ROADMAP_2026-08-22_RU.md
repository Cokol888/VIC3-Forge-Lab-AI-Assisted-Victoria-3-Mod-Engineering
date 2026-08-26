# Cheat Menu Pro — Roadmap v9 / Navy finalization

**Дата актуализации:** 22.08.2026  
**Статус:** beta17 Final RELEASED; beta18-pre2.4 Runtime PASS; beta18-pre3 Runtime PASS; beta18-pre4 Runtime PASS; beta18-pre5 transfer candidate; beta18-pre5.1 current candidate.

## 1. Принятые Navy foundations

### beta18-pre2.4 — Exact Fleet foundation — Runtime PASS

- direct `MilitaryFormation` context доказан;
- native fleet panel bridge работает;
- custom fleet marker больше не production foundation.

### beta18-pre3 — Fleet Composer 2.0 — Runtime PASS

- 5 произвольных строк;
- 25 combat hulls;
- duplicate hulls;
- один mixed Fleet;
- vanilla + Tech & Res;
- technology/provider gates.

### beta18-pre4 — Exact Ship Control & Flagship — Runtime PASS

- exact Ship selector;
- два Ships одного типа различаются как объекты;
- Ship state diagnostics;
- exact flagship set/unset;
- lost-target safety.

## 2. beta18-pre5 — Exact Ship Transfers — runtime gate ещё требуется

- single exact Ship → `set_ship_owner`;
- basket до 20 exact Ships;
- batch → `set_ship_owner_multiple`;
- cleanup через `clear_ownership_transfer_fleet` на source country;
- cross-Fleet batch;
- battle / destroyed / flagship safety;
- receiver ≠ player и имеет порт.

pre5 остаётся candidate, пока пользователь не подтвердит runtime single/batch transfer.

## 3. beta18-pre5.1 — Retrofit & Naval Logistics — текущий candidate

### Retrofit

- native Ship Designer bridge;
- native Fleet panel bridge;
- понятный маршрут `Template → Fleet → ShipSelection → Change Template → Retrofit`;
- `RetrofitShips` существует в native UI API, но CMP не вызывает его напрямую до доказанного exact Ship ↔ native ShipSelection binding;
- fake direct ShipTemplate write запрещён.

### Naval Logistics

- Supply Ships моделируются как национальный reserve/resource;
- country effect `add_supply_ships`;
- `+1 / +10 / +50 / +100`;
- `supply_ship_maintenance_fulfillment` diagnostics;
- `num_assigned_supply_ships` read-only для выбранной MilitaryFormation;
- direct assignment к formation — DEFERRED / UNCONFIRMED.

### Scope cut

**Amphibious Assistant переносится после beta18 Final.** Он станет частью будущего Military Operations Rework вместе с Army/Marines/Fleet workflows, а не блокером Navy Final.

## 4. beta18-RC1 — Full Navy Regression

RC1 начинается только после runtime PASS pre5 + pre5.1.

Regression matrix:

- Fleet Composer 2.0;
- exact Fleet;
- exact Ship;
- flagship;
- single transfer;
- batch / cross-Fleet transfer;
- Ship Designer / native retrofit bridge;
- national Supply Ship reserve;
- assigned-supply diagnostics;
- port / sea / battle / damaged / destroyed;
- immediate / +1 day / save-load;
- Workspace 90 / 100 / 115 / 130;
- no hidden fallback / no ghost target.

После PASS выпускается **beta18 Final**.

## 5. После beta18 Final

1. **Military Operations / Amphibious Assistant**
   - Marines;
   - marine capacity;
   - Fleet readiness;
   - invasion checklist;
   - native invasion bridge без fake auto-attach.
2. **Army Rework 2.0**
   - multi-unit composer → одна Army;
   - tactical profiles;
   - Expert controls.
3. **beta19 Technology 2.0**.
4. **beta20 Special & Quick**.
5. **Economy / Markets / Regions Rework**.
6. **Vanilla CMP Rework**.

## Release discipline

Registry/codegen source of truth; deterministic `--check`; zero missing GUI→SGUI/effect refs; zero duplicate `cmp_*`; RU/EN parity; no guessed scripting surface; static QA + runtime evidence before promotion.
