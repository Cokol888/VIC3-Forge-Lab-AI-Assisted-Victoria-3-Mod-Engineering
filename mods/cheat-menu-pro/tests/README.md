# Test Evidence

## Imported static QA

The historical static report remains at:

`legacy:QA_REPORT.json`

Interpretation rule:

- the top-level historical `PASS` is evidence of the recorded static suite only;
- it does not promote the imported build to runtime PASS;
- runtime and regression results must be stored separately.

## Runtime

Current required runtime gate:

`engineering/gates/beta18.1-pre1.1-army-scope-runtime.md`

Future runtime reports should be stored under `tests/runtime/` with target game version, checksum, build ID, scenario, expected result, observed result, and verdict.

## Regression

Frozen Navy behavior is a protected regression surface. Future material changes should define a bounded regression budget before implementation is declared DONE.
