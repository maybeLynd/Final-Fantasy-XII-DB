# Register cells: AL-8's evidence tracked, and SWE2-AUDIT-SEM's narrowings carried into GR-19, SD-125, SD-128 and GR-2 (OPUS for SWE2-DATA, 2026-10-01)

FABLE, and with it SWE2-DATA, is inactive; the user authorized OPUS to do every non-ASTRA task.
`register_narrow_1001.py` (in `Tools/work/OPUS/`, copied here) makes these cell edits. Old wording is struck in place,
and each cell's status lead word is untouched.

| row | edit | source |
|---|---|---|
| AL-8 | the cited map `Tools/work/rtti/unit_record_fields.tsv` (gitignored) becomes the byte-identical tracked copy [`al8-unit-record-fields-1001/unit_record_fields.tsv`](../al8-unit-record-fields-1001/unit_record_fields.tsv) (sha256 prefix `1ca6074ae6c4862a`) | documented_rule's T check: the battle-record-kind page was EVIDENCE-UNTRACKED on AL-8 alone |
| GR-19 | "when x is NaN" -> any coordinate (C1); the player-terms sentence restated to what the bytes test (C2) | [`auditsem-review-gr19-gr11-0930`](../auditsem-review-gr19-gr11-0930/REVIEW.md) |
| SD-125 | the in-play sentence gains the `001EDEC0` gate and the bit-8 gate (C1) | [`auditsem-review-sd125-128-0930`](../auditsem-review-sd125-128-0930/REVIEW.md) |
| SD-128 | "fade level" becomes a level read as fade, on channel 11, which is named nowhere (N3) | the same review |
| GR-2 | a narrowing appended: six writers, no producer of 2, the conditional argument-3 join, the refresh limit, the disp_tama and STAY_ wording, nine-copy counts (C1-C5) | [`auditsem-review-gr2-0930`](../auditsem-review-gr2-0930/REVIEW.md) |

`check_questions --db` after the edit:
- cross-check 0 / 0;
- 0 cell-count mismatches;
- the AL-8 copy reads as untracked until this commit tracks it.

run: check_questions.py --db (cross-check 0 / 0, cell counts 0) at publish (FAILS 0)

## Review (OPUS)

The edits are noted to SWE2-DATA under its review request. They discharge the register halves of FABLE's requests
`OPUS-REQ-FABLE-SD125-C1-1001`, `OPUS-REQ-FABLE-GR2-C1C5-1001` and `OPUS-REQ-FABLE-GR19-GR12-C1C4-1001`, and of
`OPUS-REQ-DATA-GR2-NARROW-1001` and `OPUS-REQ-DATA-GR19-CELL-1001`.
