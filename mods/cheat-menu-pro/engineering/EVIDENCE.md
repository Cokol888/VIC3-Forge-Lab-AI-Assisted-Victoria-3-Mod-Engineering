# Evidence Register

Critical imported evidence is preserved in the legacy snapshot and referenced rather than duplicated.

| Claim | Type | Source | Environment | Status |
|---|---|---|---|---|
| Imported build identity is `0.3-beta18.1-pre1.1` | LOCAL_CODE | `legacy:registry/build.json` | Victoria 3 1.13.10 | VERIFIED_LOCAL |
| Imported build static release checks report PASS | LOCAL_TEST | `legacy:QA_REPORT.json` | build `CMP-0.3-B18-1-PRE1-1-20260823` | VERIFIED_LOCAL |
| `beta18 Final` Navy is the accepted frozen parent contract | PROJECT_DECISION / LOCAL_TEST | `legacy:registry/build.json`, `legacy:docs/NAVY_BETA18_FINAL_RU.md` | parent baseline | VERIFIED_LOCAL |
| `pre1.1` exact Army observer/probes are read-only by design | LOCAL_CODE / PROJECT_DECISION | `legacy:docs/MILITARY_OPERATIONS_ARMY_SCOPE_PRE1_1_RU.md` | imported build | VERIFIED_LOCAL |
| `pre1.1` exact Army runtime behavior passes | LOCAL_TEST | runtime checklist | imported build | UNVERIFIED |

## Evidence rules

- `STATIC PASS` must not be promoted to `RUNTIME PASS`.
- `PLAN` and roadmap entries are not engine facts.
- Evidence tied to Victoria 3 `1.13.10`, checksum `2964`, or the locked upstream snapshot becomes `REVALIDATION_REQUIRED` when the relevant environment changes.
- Preserve historical evidence when revalidation is required; do not rewrite history to UNKNOWN.
