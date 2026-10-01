# Consumer check: residue-3 correction on the registry page (SWE2-STRUCT for OPUS, 2026-09-30)

SWE2-STRUCT's residue-3 record (this folder's README, checks G1-G9) struck one sentence of `AG-4`'s 2026-09-18 answer on
the registry page and added a dated correction beside it. Nothing was struck on the FCP page, which carries notes only.

- **Corrects:** in authored-data-table-registry.md, `AG-4`'s answer in §7: "`0055CD40` copies an authored record byte `+0x108` into `+0x558` under `+0x570` bit 10 (`0055CF73`..`0055CF80`) without touching the counts: that is the one path on which a `0xFF` in the data would make the reader dereference slot 50, and its data range is not checked here."
- **Affected:** 02-Resource-And-Asset-Pipeline/authored-data-table-registry.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the registry page's own `0x02EBF198` disposition (the batch-12 note "the path that produces −1 also zeroes the reader's loop count … leaves the byte's data range unchecked") | revised-here (a dated note added after it; the earlier note is not struck) |
  | _index/OPEN-QUESTIONS.md, the `AG-4` row (it carries the same sentence verbatim) | disagrees; routed to SWE2-DATA, the register's owner, with replacement text in the README (not edited) |
  | 16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md, `UQ-155` (lines 224-237: "takes the owner byte `+0x108` as the board index `+0x558`", "the owner's pre-chosen board byte") | agrees (it names the same owner byte and the same board-choice flow) |
  | _index/EVIDENCE-STANDARD.md line 4429 (the `02EBF198` row) | untouched by this correction (its "data-driven index" claim was routed by batch 12) |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2struct-residue3-0930/residue3_check.py (27 checks, FAILS 0, including G6's image-wide census of stores covering `+0x558`/`+0x559` with the two known writers as its control).
- run: residue3_check.py at 4760745aa (FAILS 0, on the worktree)
