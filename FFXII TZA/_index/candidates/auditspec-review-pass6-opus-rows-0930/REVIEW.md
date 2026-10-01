# SWE2-AUDIT-SPEC review of OPUS's 15 pass-6 FALSE-POSITIVE dispositions (92acfd1c4): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30). Reviewed: the 15
`check_banned_evidence.py` rows OPUS authored in `_index/candidates/false-positive-dispositions.tsv` (request at
`92acfd1c4`), measured at HEAD `9b6c5bc93`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-PASS6-OPUS-ROWS-0930 | `false-positive-dispositions.tsv` rows 49-61, 75, 76 | `92acfd1c4` | ACCEPT-WITH-NARROWING |

**State found.** All 15 rows already carry reviewer `SWE2-AUDIT-SPEC`, with hashes that still match. The signatures
come from `1e76d4dae` ("sign all 28 OPUS FALSE-POSITIVE banned-evidence dispositions"). That commit is marked
"Generated with Devin", and no review record was committed with it. This review is the record for those signatures.

**Method.** [pass6_rows.py](pass6_rows.py) / [.out](pass6_rows.out):
- It imports the gate's own `sweep()` and `dispositions.Registry`, so the lines are exactly the gate's.
- For each subject it prints every REVIEW line with context, and whether the row's signature applies.
- 35 REVIEW lines at HEAD, on the 15 pages. The request's 38 was counted at `92acfd1c4`.
- Each line is judged by the pass-6 ruling in `FINAL-AUDIT-PROTOCOL.md`: "unwind data is banned as evidence for
  claims about what the program EXECUTES". The precedents come from the same file:
  - a `.pdata` range used as the extent that puts one address inside a function was repaired as a violation;
  - a `.pdata` entry said to "prove" an extent was repaired as a violation;
  - EH scope/unwind maps for what the exception dispatcher does are not banned.

**Per subject.**

| subject | lines | reading | disposition |
|---|---|---|---|
| `uc1-extent-collision-opus/README.md` | 6 | `.pdata` begin is one of the producer kinds a zero-producer census searches (it widens the search; the zero does not rest on it); the controls prove the scan sees `.pdata` begins; the "native (unwind) extent" is named as metadata beside the decoded instruction extent, and table ownership rests on the reader `007C27F2` | FALSE-POSITIVE |
| `b2b-opus-funclet-section-split/README.md` | 2 | the subject is funclet identity; `.text$x`'s `.pdata` starts are the census population of a section whose content is dispatcher code | FALSE-POSITIVE (dispatcher ruling) |
| `con198-exit-attribution-0930/README.md` | 4 | funclet owners come from the C++ EH unwind maps. A funclet runs only when the dispatcher runs it, so this is a dispatcher fact | FALSE-POSITIVE (dispatcher ruling) |
| `fragment-size-sweep-0929/README.md` | 3 | describes an earlier error; reports a record's own statement; L29 measures the catalogue against its `.pdata` chains ("measured, not corrected here"), a claim about the metadata | FALSE-POSITIVE (the extent use itself is under OPUS-REQ-AUDITSPEC-EXTENT-V4-0930) |
| `heading-full-extent-repair-0929/README.md` | 2 | `.pdata` chain tiling is one of four conjunctive refusal conditions (with catalogue size and the decoded `ret`); it can refuse, not prove | FALSE-POSITIVE |
| `k14-closure-stores-0930/README.md` | 1 | `RtlVirtualUnwind` is an import name in a list | FALSE-POSITIVE |
| `pre-audit-dry-run-0930/README.md` | 4 | meta text about earlier dispositions | FALSE-POSITIVE |
| `uc1-band-257-up/README.md` | 1 | U/X are band classification tests: is a block a standalone MSVC function (build structure), not what code runs | FALSE-POSITIVE |
| `uc1-extent-collision-consumer-check.md` | 2 | same as the first row | FALSE-POSITIVE |
| `uc1-held-rows-opus/README.md` | 2 | "inside the listed function's own unwind range ... This is consistent": corroboration, not support | FALSE-POSITIVE |
| `uc1-pass2-extent-and-tables.md` | 1 | `Unwind@`/`Catch_All@` are names | FALSE-POSITIVE |
| `uq2-caller-route/README.md` | 2 | `.pdata` is excluded from the address-taken scan, which is the exclusion the pass wants | FALSE-POSITIVE |
| `CONTRACT-manager-slot-entry-tables.md` | 2 | "an E8/E9 census over all 35,713 `.pdata` bodies finds exactly 13 call sites" uses `.pdata` as a census population. Re-measured image-wide without it ([slotentry_imagewide.out](slotentry_imagewide.out)): exactly **13** rel32 sites for the eight functions, 0 `jcc`, 0 abs64; the four `.rdata` rva32 hits are chained-unwind copies (begin/end/unwind triples). The claim does not depend on the population | FALSE-POSITIVE |
| `CONTRACT-ppfx-effect-creation.md` | 1 | "nothing observed unwinds it" is an English verb | FALSE-POSITIVE |
| `text-gap-append-0930/README.md` | 2 | L21: "Four addresses are interior to real `.pdata` extents of bodies the list cuts short ... None is data cited as code." As written, the code-not-data conclusion rests on `.pdata` extents, the precedent's violation class. The bytes support it without them: `00121E11` is the second byte of `jmp $` at `00121E10` after `ret` at `00121E0E`; `0036F22E` is `mov eax, edi` in an epilogue ending `ret` at `0036F23A`; `00808ED9` is `mov rbx,[rsp+0x40]` before `ret` at `00808EE3`; `0015AE4A` is in the epilogue the rule-13 script already cites | **use as worded - narrowing below** |

**Result.** Fourteen of the fifteen signatures are sound. The text-gap row is a real use in its present wording, although
nothing it concludes is wrong.

**Controls.** The per-row hash check (signature applies = True for all 15) is the gate's. The one measurement that could
change a verdict, the slot-entry census population, was replaced by a population-free raw sweep and agrees.

**Gate defect (for the report).** `dispositions.py` applies a row when reviewer differs from author and the hash
matches. It does not ask for a review record. 28 rows became "reviewed" in one commit with no record committed with
them (`1e76d4dae`).

**Correction wording** (for OPUS, `text-gap-append-0930/README.md` L21 and `textgap_rule13.py`'s reasons for
`00121E11`/`0036F22E`). Replace "Four addresses are interior to real `.pdata` extents of bodies the list cuts short" with
"Four addresses decode as code inside bodies the list cuts short: `00121E11` is the second byte of `jmp $` at
`00121E10` after the `ret` at `00121E0E`, `0036F22E` is `mov eax, edi` in the epilogue ending `ret` at `0036F23A`,
`00808ED9` and `0015AE4A` are epilogue instructions". The reword changes the evidence hash and lapses the row, which
must then be re-signed.
