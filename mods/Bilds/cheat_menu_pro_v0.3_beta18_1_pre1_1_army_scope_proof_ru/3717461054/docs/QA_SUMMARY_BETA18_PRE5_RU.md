# QA Summary — beta18-pre5 Exact Ship Transfers

**Build:** `CMP-0.3-B18-PRE5-20260822`  
**Static status:** PASS  
**Runtime status:** UNVERIFIED

## Закрытый baseline

- beta18-pre2.4 Fleet Target Core — Runtime PASS;
- beta18-pre3 Fleet Composer 2.0 — Runtime PASS;
- beta18-pre4 Exact Ship Control & Flagship — Runtime PASS.

## Новый pre5 contract

- receiver: existing marked country target;
- receiver gates: not player + has port;
- single exact Ship: `set_ship_owner`;
- batch exact Ships: `set_ship_owner_multiple`;
- batch cleanup: `clear_ownership_transfer_fleet` on source country;
- transfer basket: Ship-scope marker, max 20;
- cross-fleet basket supported;
- battle / flagship / destroyed Ship blocked;
- destructive Ship effects and Supply writes absent.

## Static QA

- Navy18 validator: PASS, 0 errors / 0 warnings;
- Registry Coverage: PASS;
- Regions Operations regression: PASS;
- Army Final regression: PASS;
- UI/accessibility: PASS, 0 errors / 0 warnings;
- full release validator: PASS, 0 errors;
- GUI/common/event brace-checked files: 128;
- unique GUI -> ScriptedGui refs: 11 340;
- generator determinism: build/navy/catalog/ship-control/transfer/registry/workspace PASS.

Runtime evidence remains mandatory before promotion to pre5.1 / RC path.
