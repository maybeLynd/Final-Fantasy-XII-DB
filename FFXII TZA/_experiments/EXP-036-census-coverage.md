---
experiment: EXP-036
title: Census checker success without applicable evidence
status: REPRODUCED — isolated validator coverage gap; owner repair pending
contract: none - census coverage of the checker corpus; a Method A tooling record that executes no shipping game code. Checked BOTH directions 2026-09-13: it names no contract and no contract names it
date_designed: 2026-09-11
method: A - offline instrument preparation
live_game: false
---

# EXP-036 — zero disagreements does not measure checked coverage

The census width checker is being used to verify recently populated type rows.
Its missing-file branch prints a notice and continues; missing usable widths and
malformed rows are skipped. This review asks whether its exit code distinguishes
successful comparison from inability to compare a declared field. It does not
change OPUS's actively owned source or the canonical type store.

[reproduce.py](evidence/EXP-036-census-coverage/reproduce.py) snapshots the exact tool,
creates separate temporary roots and runs it unchanged. The matching/mismatch
controls have one declared BattleUnit+0x100 and one valid dword-access row; only the
declared size changes between4 and1. Other configured censuses contain headers.
The missing-input case removes the applicable BattleUnit census; malformed evidence
replaces its row with an invalid short line; the last case leaves only the fields
header. All temporary roots are isolated and removed after their child exits.

| Fixture | Declared fields | Exit code | Outcome |
|---|---:|---:|---|
| Matching dword | 1 | 0 | Valid matching control |
| Declared byte vs dword | 1 | 1 | Positive MISMATCH control |
| Applicable census missing | 1 | 0 | No comparison possible |
| Applicable row malformed | 1 | 0 | No usable width evidence |
| No declared fields | 0 | 0 | Zero applicable comparisons |

The last three still print zero rows disagreeing. That count need not be numerically
false, but neither it nor exit0 proves the declared fields were checked. The missing
file is mentioned in stdout; malformed/no-evidence skips lack a checked/unchecked
denominator. This is an input/completeness boundary, not evidence that any particular
production field width is wrong. Positive mismatch detection works in its control.

The source remained byte-identical throughout the run. The [result](evidence/EXP-036-census-coverage/result.json)
preserves each exit/stdout/stderr and source hash; the [manifest](evidence/EXP-036-census-coverage/manifest.json)
preserves the checker snapshot and harness. These are synthetic validation fixtures,
not original-game evidence.

Return to OPUS: report checked/unchecked declarations and malformed input, and
distinguish missing applicable evidence or zero comparisons from a successful
coverage verdict. Preserve valid mismatch reporting. A repair should rerun these
discriminating fixtures and the actual store with explicit incompleteness where
appropriate. No broad type rewrite follows from this instrument finding.
