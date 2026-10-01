# GFZ EXTERNAL DEPENDENCIES — 2026-09-01

The handoff ZIP is self-contained for the current continuation state and includes the usable GM160 GZF plus continuation scripts/evidence.

The following are intentionally **not** bundled as game/distribution payloads:

## Authorized FFXII executable

Expected SHA-256:

`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

The game EXE must not be included in GFZ handoff ZIPs. The GZF's embedded original must reproduce this hash when verified with the supplied extraction script.

## Canonical V120 final-replay authority

Expected canonical V120 artifact SHA-256:

`507490534a8bb67e8d3c6deba4d527c23ab9fdd3672494e511db0d9ef0e511a9`

This is needed only at final V121 deterministic replay/canonicalization, not for immediate GN continuation from GM160.

## Ghidra runtime

Required baseline:

- Ghidra 12.1.2
- Java 21

The package contains the GFZ-specific Java/Python scripts but not a full Ghidra installation.

If reconstructing Ghidra from supplied multipart archives in the user's environment, use standard archive handling/system libarchive. **Do not use the 7z CLI.**

## Optional independent challenge tooling

When materially useful:

- GhidraMCP/Bethington 6.0.0
- radare2
- LIEF
- Capstone
- angr
- DynamoRIO
- Cheat Engine/runtime evidence
- LiveLab
- VBF/EBP tooling
- upstream library/source repositories

These can challenge or corroborate semantics, but Ghidra exact-current body identity and persisted GFZ annotation state remain the mutation authority.
