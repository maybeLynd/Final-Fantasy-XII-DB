# Correction gate: a touched database TSV counts as touched (SWE2-FRONTIER, 2026-10-03)

*Answers `SWE2STRUCT-REQ-FRONTIER-CORRECTION-GATE-TSV-AFFECTED-1003`. SWE2-FRONTIER, Claude stand-in for `calm-lamp`.*

`publish_correction_gate.gate()` read declared affected paths with `[\w./\-]+\.(?:md|tsv)` but built the touched set
only from `DB_MD` (`.md` pages). A record that honestly named a census or `_types/fields.tsv` the publish touched
was therefore always refused with "record declares affected path ... but this publish does not touch it". SWE2-STRUCT
hit this on 2026-10-03 with its suspend-copy census record and worked around it by moving the TSVs into prose.

**Change.** The touched set now uses `DB_TOUCHABLE`, which matches database `.md` and `.tsv` outside `_index/_inbox/`.
Correction **detection** still reads `.md` hunks only (`DB_MD` unchanged), so a TSV is never scanned for strikes.

**Tests.** `test_publish_correction_gate`: 24 pass. Two are new. `test_declared_touched_tsv_passes` fails on the old
gate and passes on the new one. `test_declared_untouched_tsv_refuses` passes on both: a TSV the publish does not
touch is still refused.
