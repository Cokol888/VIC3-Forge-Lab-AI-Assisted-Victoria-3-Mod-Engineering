# Contributing

## Change types

Keep prompt changes, mod-code changes, test-evidence changes, and documentation changes separable whenever possible.

## Prompt changes

A prompt revision should document:

- motivation;
- affected rules/modules;
- expected behavior change;
- eval scenario or real failure case that justifies the change;
- compatibility/revalidation impact.

Do not promote a prompt candidate solely because it is longer or more detailed.

## Mod changes

Material mod changes should include:

- objective and hypothesis;
- changed objects/files;
- expected observation;
- validation status;
- regression scope;
- updated `MANIFEST.yml` when state/environment changed.

## Evidence

Do not record expected behavior as observed behavior. Pin version-sensitive evidence to its environment.

## Pull requests

Prefer small, reviewable, reversible changes. Avoid mixing unrelated experiments in one PR.
