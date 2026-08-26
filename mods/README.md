# Mod Workspaces

Each Victoria 3 mod lives in its own isolated workspace:

```text
mods/<mod-id>/
├── README.md
├── MANIFEST.yml
├── ROADMAP.md
├── CHANGELOG.md
├── engineering/
├── tests/
├── mod/
└── releases/
```

## Rules

- `mod/` contains only deployable Victoria 3 mod content.
- Engineering notes, AI checkpoints, evidence, tests, and roadmaps stay outside `mod/`.
- Every mod pins the exact VIC3 Forge prompt version used.
- Every version-sensitive claim records its target Victoria 3 environment.
- Runtime success is not inferred from static code review.
- Base-game files and copyrighted game assets are not vendored into this repository.

## Required MANIFEST fields

- project id/name
- engineering state
- prompt id/version
- target Victoria 3 version/checksum when known
- repository branch/commit where useful
- active gate
- next milestone
- revalidation status
