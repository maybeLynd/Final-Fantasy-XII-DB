# SWE2-AUDIT-SPEC review of SD-103/SD-104 (sd103-104-context-rows-0930 at c2b5b9927): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS.
Reviewed: `c2b5b9927`, [the record](../sd103-104-context-rows-0930/README.md), `sd103_slots.py` and the new
census `Database/Tools/analysis-kit/gfz-scripts/objflow.py`. Static, the certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD103-104-0930 | [sd103-104-context-rows-0930](../sd103-104-context-rows-0930/README.md) | `c2b5b9927` | ACCEPT |

**Re-run.**
- `sd103_slots.py` at HEAD: C1-C6 PASS, `FAILS 0`, identical to the committed `.out` ignoring CR
  ([rerun_sd103_slots.out](rerun_sd103_slots.out)).
- C1 only reads the committed census output, so I re-ran the census itself:
  `objflow.py --ptr 0209CC40 --static 0209D490 0209E598 --region 0x1060 0x1098` (about 3 minutes;
  [rerun_objflow.out](rerun_objflow.out), [rerun_objflow.tsv](rerun_objflow.tsv)). Both files are identical to
  `sd103_objflow.out` / `.tsv` apart from the per-round timings.
- The census summary: 63 root functions, 3,523 bodies reached, object stores
  `{'INDEXED-BELOW': 5, 'REGION': 1, 'STATE-OTHER': 140}`, one escape (the publish `002B3550`), 0 indirect calls, 0
  depth cuts.

**Re-derived independently** ([sd103_review.py](sd103_review.py), [sd103_review.out](sd103_review.out)).
- **R1, `002B3480`.** Both loops index the context loaded from `[0209CC40]` (`002B34D0`, `002B3514`) with stride 24
  (`lea rcx, [rax + rax*2]`, then `*8`):
  - the first loop uses row `k`, bounded by `[src1+0x1C]`;
  - the second uses row `k + 0x2a` (`002B3506 add rax, 0x2a`, i.e. 42), bounded by `[src2+0x1C]`.

  `call 0x2b5c90` follows at `002B352B`. The sources are `0029CB50` = `[[g]]` and `0029CB60` = `[[g]+0xB0]`.
- **R2, the reader.** `002B5C90` loads `[rbx+0x1060]` at `002B5F53`, `[rbx+0x1078]` at `002B601A` and `[rbx+0x1090]`
  at `002B60A6`.
- **R3, the builder `002432B0`.**
  - `and esi, 0x3ff` is the count;
  - `+0x08` gets the 20-byte record pointer (`00243305`);
  - `+0x00` is rebuilt as `(count<<2 in 0x3fffc) | 2`, then bit 0 = the record's bit 28 (`00243313`-`00243333`);
  - `+0x10` gets 0 or the `002497B0` allocation (`0024338C` / `002433AA`).

  The loop at `00243340` walks the items, with the count as its trip count.
- **R4, the arithmetic.** 24·174 + 0x10 = 0x1060, 24·175 + 0x10 = 0x1078, 24·176 + 0x10 = 0x1090, and 24·42 + 0x10 =
  0x400; 179 rows fit below `+0x10C8`.

SD-103 (source 2's records 132-134) and SD-104 (the row layout, and the 10-bit field as an item count) hold.

**Controls.**
- The census is sensitive to the defect it guards against, an unseen indexed writer: it reports the positive
  (`002432B0`'s two `+0x10` stores as INDEXED-BELOW) and the zero fill.
- C2-C6 are pinned-text checks. R1-R3 confirm the same facts from operands.

**Remarks (no change asked).**
- Neither loop in `002B3480` is capped. A source 1 with more than 42 records would overwrite rows from 42 on. A source 2
  with more than 137 records would run past `+0x10C8`.
- So the record's open limit, whether the shipped source 2 has at least 135 records, is the whole remaining question.
  It is correctly left as a limit.
