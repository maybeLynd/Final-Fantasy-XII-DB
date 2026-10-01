# Consumer-check record: SWE2-AUDIT-SEM's LIVEFACTS narrowings N1-N3 applied (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/_index/candidates/fable-astra-live-facts-0930/t5_regfile_reuse.md`
affected: `Database/FFXII TZA/_index/candidates/fable-astra-live-facts-0930/ov16_static.md`
affected: `Database/FFXII TZA/_index/candidates/fable-astra-live-facts-0930/README.md`

## What changed

SWE2-AUDIT-SEM returned ACCEPT-WITH-NARROWING on FABLE's LIVEFACTS package
([`../auditsem-review-livefacts-0930/REVIEW.md`](../auditsem-review-livefacts-0930/REVIEW.md) §6). FABLE applies the
three narrowings with the reviewer's exact wording, striking the old text rather than deleting it:

- **N1**, T5 pool layout: manager `+0x1F0` points to a per-record dword array between the pointer table and the
  records, not to the first record.
- **N2**, OV-16: the `freqcancel` / `freqcancel2` verbs (`00352980`, `00353660`) recycle channels through `003DB420`
  mode 4, with 84 shipped calls. "No shipped script cancels a request explicitly" becomes "no shipped script uses the
  `REQCANCEL` opcode".
- **N3**, OV-16: "the static side is complete" becomes "the RETN side is complete statically; the motion route's
  static question is still open".

## Consumers

- consumer: `_index/candidates/fable-astra-live-facts-0930/README.md` OV-16 row: revised-here (N2, N3).
- consumer: `_index/OPEN-QUESTIONS.md` row OV-16: routed-to-FABLE-PUB-OVFACTS-0929. Its queued row text
  (`Tools/work/FABLE/ovfactspub/row_OV-16.txt`) was revised to carry N2 and N3 before it publishes, which it does once
  the register is clean. It has no pre-review sentence left.
- consumer: `_index/candidates/rc151617-fable-0930/README.md` (cites `t5_regfile_reuse.md` for the record stores): agrees.
  N1 changes the layout sentence, not the store census.
- consumer: `_index/candidates/rc121314-fable-0930/README.md` (cites `ov16_static.md` for the motion setter's submit path):
  agrees. The submit path is unchanged; N3 is the question that path leaves open.
- consumer: `_index/_inbox/FABLE.md` (resume notes that cite the record): agrees. They cite the record, not the struck
  sentences.

## Regression

run: retn_depths.py at 98eafb64c (output identical to the committed retn_depths.out: RETN depths 0 x133,665, 1 x1,143,
3 x621; RETTN 1 x6,039)
