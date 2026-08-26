# Evidence Register

Critical imported evidence is preserved in the legacy snapshot and referenced rather than duplicated.

| Claim | Type | Source | Environment | Status |
|---|---|---|---|---|
| Imported build identity is `0.3-beta18.1-pre1.1` | LOCAL_CODE | `legacy:registry/build.json` | Victoria 3 1.13.10 | VERIFIED_LOCAL |
| Imported build static release checks report PASS | LOCAL_TEST | `legacy:QA_REPORT.json` | build `CMP-0.3-B18-1-PRE1-1-20260823` | VERIFIED_LOCAL |
| `beta18 Final` Navy is the accepted frozen parent contract | PROJECT_DECISION / LOCAL_TEST | `legacy:registry/build.json`, `legacy:docs/NAVY_BETA18_FINAL_RU.md` | parent baseline | VERIFIED_LOCAL |
| `pre1.1` exact Army observer/probes are read-only by design | LOCAL_CODE / PROJECT_DECISION | `legacy:docs/MILITARY_OPERATIONS_ARMY_SCOPE_PRE1_1_RU.md` | imported build | VERIFIED_LOCAL |
| `pre1.1` exact Army runtime behavior passes | LOCAL_TEST | runtime checklist | imported build | UNVERIFIED |
| Existing CMP script can enumerate exact Army formation scopes and store them in a variable list | LOCAL_CODE | source collection `529340(1).zip`: `3717461054/events/sakuya_main_04_01_events.txt` | upstream Cheat Menu Pro / Victoria 3 1.13.* | VERIFIED_LOCAL |
| Scope-backed GUI lists and `Scope.GetMilitaryFormation` promotion exist in 1.13-compatible source/docs | LOCAL_CODE / SCRIPT_DOCS | source collection `529340(1).zip`: CMF 1.63.0 GUI; Victoria-3-Modding-Co-op `1.13.x` generated data-type docs | Victoria 3 1.13.* | VERIFIED_LOCAL |
| Self-contained Army picker can be built by composing Army enumeration -> dedicated scope list -> `Scope.GetList` -> `Scope.GetMilitaryFormation` | INFERENCE / PROJECT_PROPOSAL | `engineering/gates/beta18.1-pre2.0-army-list-projection-contract.md` | proposed post-pre1.1 diagnostic | REQUIRES_PROOF |

## Evidence rules

- `STATIC PASS` must not be promoted to `RUNTIME PASS`.
- `PLAN` and roadmap entries are not engine facts.
- Evidence tied to Victoria 3 `1.13.10`, checksum `2964`, or the locked upstream snapshot becomes `REVALIDATION_REQUIRED` when the relevant environment changes.
- Preserve historical evidence when revalidation is required; do not rewrite history to UNKNOWN.
