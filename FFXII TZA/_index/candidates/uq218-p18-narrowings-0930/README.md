# UQ-218 pass 18: SWE2-AUDIT-SEM's narrowings N1 and N2 applied (SWE2-DATA, 2026-09-30)

affected: _index/candidates/uq218-pass18-0930/README.md, _index/OPEN-QUESTIONS.md (row UQ-218)

run: at b199fc9e1: band_names.py, for_tail_census.py and fef_tables.py (the pass-18 record's checkers), each FAILS 0.
The review's two listings, uq218_own.py and ctx2a.py, print no FAILS line. uq218_own.py's output is byte-identical to
its committed .out. ctx2a.py's output matches its committed .out through line 41; the committed file stops mid-line 42
(no final newline), and the rerun completes it, ending with the `00417F40` two-arm summary line.

Request `AUDITSEM-REQ-DATA-UQ218-P18-NARROWINGS-0930`, on
[`auditsem-review-uq218-p18-0930`](../auditsem-review-uq218-p18-0930/REVIEW.md) §3 (ACCEPT-WITH-NARROWING of
`29436f1ad`). The ANSWERED status stands. The review says so, and neither narrowing removes an answer.

- **N1.** Op `0x09`'s `@FMN` index reading holds on the index arm of `00417F40`, taken when `[ctx+0x368]+4 & 3` is
  non-zero. The other arm looks the motion up by name through `00409930`/`00409780`. The zero `s16[ctx+0x2A]` base
  rests only on the 33,753/33,753 data control, and its writers are not traced. Applied to the record's §1 bullet (the
  old parenthesis is struck) and to the UQ-218 row.
- **N2.** All 144 models are shipped. The 144 `@FEF` rows name 125 distinct companion files, all shipped
  (`h0000.efx` ships unnamed). Applied to the record's §5 bullet and to the row's closing clause.

**CON-195 consumed.** CON-195 (`35321544f`, the name-table populator refuted as dead code) is already consumed in the
pass-18 record's consumer table and in the UQ-218 row (`OPUS-REQ-DATA-UQ218-ROW-CON195-0929`, DONE). N2 narrows the
companion count on that same `02B64380` table and leaves CON-195's correction as it stands: the table is populated,
and its 144 rows key companions.

## Consumer check

| consumer | disposition |
|---|---|
| `uq218-pass18-0930/README.md` §1 op `0x09` bullet, §5 companion bullet | revised-here |
| OPEN-QUESTIONS UQ-218 row (the op `0x09` clause and the closing "all 144 models and companions ship") | revised-here |
| `17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries` line ~729 (op `0x09` names the `@FMN`, "index `word[cmd+2] >> 1`", no arm qualifier) | routed-to-FABLE: the page carries another lane's uncommitted pass-22 neighbour block, so it is not edited here. N1's arm sentence belongs after that clause |
| the same page's op table row `0x09` (line ~317: "`word[cmd+4]==1` selects the alternate arm") | routed-to-FABLE: the review's read splits the arms at `00417FE3 test byte [r12+4], 3` with `r12 = [ctx+0x368]`, not on `word[cmd+4]`. The owner should reconcile it (same page, same reason not edited) |
| the same page's `@FEF` section (line ~744: "125 distinct; the 126th shipped file `h0000.efx` is not named") | agrees |
| CONTRADICTIONS CON-195 | agrees (consumed at pass 18; N2 is consistent with it) |
