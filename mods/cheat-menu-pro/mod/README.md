# Deployable Mod / Overlay Root

This directory is reserved for the normalized, project-owned deployable mod/overlay tree.

The historical full Workshop snapshot is intentionally **not duplicated here**.

Before populating this directory:

1. establish the desired upstream/overlay distribution model;
2. verify redistribution rights for any third-party source copied into the public repository;
3. prefer project-owned changed files, generated outputs, and required metadata;
4. preserve upstream hashes and provenance in `../upstream/`;
5. run static and runtime validation before release.

When populated, this directory should mirror only the Victoria 3 paths actually required by the distributable project.
