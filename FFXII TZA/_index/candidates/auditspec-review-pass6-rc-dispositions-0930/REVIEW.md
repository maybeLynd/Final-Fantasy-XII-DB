# SWE2-AUDIT-SPEC review of the five pass-6 dispositions on SWE2-ORACLE's rc records (rows 64-68): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30). Reviewed: SWE2-ORACLE's
pass-6 owner reading of the 8 TO READ lines on five ORACLE records. The disposition rows are OPUS's (`23f18aae2`,
`_index/candidates/false-positive-dispositions.tsv` rows 64-68). Measured at HEAD `9b6c5bc93`.

| request | record | commit | verdict |
|---|---|---|---|
| ORACLE-REQ-AUDITSPEC-PASS6-RC-DISPOSITIONS-0930 | `false-positive-dispositions.tsv` rows 64-68 | `23f18aae2` | ACCEPT |

**State found.** The five rows' reviewer column already reads `SWE2-AUDIT-SPEC`, and their hashes match. They were filled
by `1e76d4dae`, a Devin-generated commit that committed no review record. This record is that record. No row needs
editing.

**Method.** [pass6_rc_rows.py](pass6_rc_rows.py) / [.out](pass6_rc_rows.out) prints each page's REVIEW lines, using the
gate's own `sweep()` and `Registry`. There are 8 lines, and every signature applies. The only risk a census-population use
carries is a missed reference in code outside `.pdata`. So each claim was re-measured image-wide, with no `.pdata`
population, using this lane's loader: raw E8/E9 rel32, `jcc`, rip-relative, image-base-relative, abs64 and rva32
([imagewide_refs.out](imagewide_refs.out)).

| page | lines | reading | re-measured without `.pdata` | disposition |
|---|---|---|---|---|
| `rc11-arena-ten-0930` | L19, L49 | `riprefs.py` runs over `.pdata` fragments (a population); L49 names `.pdata` records and three chained-unwind copies as NON-references | `003EE2D0` ← `003EE1F2`; `003ED8A0` ← `003EE39B`; `003A9EF0` ← `003EDAA0`; `00504350` ← `003AA109`, `00500A20`; `00500980` ← `003A9F42`. No `jcc`, rip, image-base or abs64 reference to any of the five. The only rva32 hits are `.pdata` entries and, for `003A9EF0`, three `.rdata` chained-unwind copies. "None has another reference" holds without the population | FALSE-POSITIVE |
| `rc12-footer-channels-runstate-0930` | L10, L242 | the population is chain roots **plus** a linear sweep of every `.text` run no `.pdata` entry covers, so it is complete for `.text` | not needed | FALSE-POSITIVE |
| `rc20-float-push-verbs-0930` | L15, L31 | step 1 keeps raw hits that decode inside a chain-root body; C5 proves a `.pdata`-less thunk is still found | `00267F60`: 58 raw rel32 sites image-wide, all decodable, 0 `jcc`, no rip or image-base reference; the record's "58 in 38 functions" is the whole set | FALSE-POSITIVE |
| `rc22-as7-pages-0930` | L79 | "`.pdata`-less setter" describes `002CEE00`; the only-writer claim rests on the store census (`002CEE1A`) | not needed | FALSE-POSITIVE |
| `rc8-cascade-count-0930` | L16 | the `memsweep` population is chain roots plus leaf bodies from `functions.tsv`; the result is a decoded pointer-flow analysis | not needed (the unlisted-code limit is UC-1's, not a `.pdata` use) | FALSE-POSITIVE |

**Controls.** The image-wide sweeps re-find every caller the records name, which is a positive control for each. A
`.pdata`-only population would have been caught by a leaf-code reference. None exists for these targets.

**Correction wording:** none needed.
