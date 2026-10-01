---
experiment: EXP-041
title: GameSettingConfig pointer instruction closure
status: COMPLETE - bounded offline assessment
contract: ../19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md
evidence_class: retained-evidence assessment
method: A - retained-evidence assessment
live_game: false
execution_scope: Retained capture and address-expression assessment plus unchanged implementation AST; no new memory reads from a process.
contract_coverage: Assessment of retained EXP-001 address expressions and tool documentation; no new config observation or repair of historical E8 failures.
tool: evidence/EXP-041-config-pointer-closure/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-041: GameSettingConfig pointer instruction closure

**Status:** bounded offline correction and evidence assessment complete. No live process used.
**Owner:** ASTRA. **Date:** 2026-09-11.

OPUS commit `4d0e7de` corrected the type's instance address: `0x01F82D20` stores a pointer to a
heap-allocated `0x65C`-byte GameSettingConfig. It is not the object itself. The allocation, constructor
and pointer store are cited on the current type row; this package does not redo that native analysis.

The current [runtime probe](../../Tools/analysis-kit/gfz-scripts/runtime_probe.py) still advertised
`--type GameSettingConfig --at 0x01F82D20` alongside the correct `--deref` example. Its `--at` branch
uses the supplied address directly, so that example points typed reads at unrelated static data.
The incorrect example is removed and the pointer/object distinction is stated beside:

```text
runtime_probe.py --deref 0x01F82D20 --type GameSettingConfig
```

Only the module docstring changed. [Before](evidence/EXP-041-config-pointer-closure/runtime-probe-before.py)
and [after](evidence/EXP-041-config-pointer-closure/runtime-probe-after.py) bytes are retained.
[check.py](evidence/EXP-041-config-pointer-closure/check.py) confirms the complete implementation
AST is identical after removing only the module docstring. No runtime behavior or pointer resolver
was changed, and no new runtime observation is claimed.

## Affected evidence boundary

The four retained `EXP-001-gamesetting-frametimebase-*.json` files record `runtime_probe.py --check
EXP-001-gamesetting-frametimebase.tsv`, not the incorrect `--at` example. Their actual stdout uses
bracketed address expressions for the config rows. The TSV has eight explicit dereferences:
E1, E6, E7, E8, E9, E10, E11 and E12. Its records match initial commit `e1fc2df`. The resolver reads
an eight-byte pointer before adding the offset, while a null/unreadable pointer is refused.

This supports **no identified direct-object-address contamination in those four retained files**.
Their stdout truncates address expressions and does not preserve each resolved object address or
the exact instrument source hash. This assessment therefore does not retroactively supply those
missing receipts, revalidate all original provenance, or establish what every historical run did.
The recorded E8 expectation failures and process-absence failures remain failures; the correction
is not an explanation or repair of E8. Raw captures, TSV and historical hash-named sources are untouched.

[Results](evidence/EXP-041-config-pointer-closure/result.json) retain source/capture/TSV hashes,
the eight full expressions and each recorded observation's command, exit code, relevant stdout and
errors. Duplicate top-level `observation` aliases are not counted again when `passes` exists.

## Source pin consequence

[EXP-037](EXP-037-command-observer.md) pins the former runtime probe SHA-256 in its dependency file.
The documentation-only edit changes that hash, so the existing candidate now refuses its source
check before process discovery. This is the intended identity boundary, not a new live-game result.
Its old manifest, dependencies and test receipts are preserved. Before using that candidate with
the corrected source, prepare and record a newly qualified dependency set and rerun its affected
offline controls; do not silently relabel the earlier source identity. Live validation remains pending.

The [manifest](evidence/EXP-041-config-pointer-closure/manifest.json) seals this bounded closure.
Game automation remains paused after the earlier physical Escape stop, pending user preference.
