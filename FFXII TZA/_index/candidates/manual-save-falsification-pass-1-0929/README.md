# Consumer check: falsification pass 1 on how-a-manual-save-is-committed (OPUS, 2026-09-29)

corrects: 19-Save-Load-Settings/how-a-manual-save-is-committed.md (the appended SWE2-EC7-113 note: CON-191)
corrects: 19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md (the state list: CON-192)

## What was corrected

- **CON-191.** `00582730` and `005826D0` are the storage queue's kind-7 write and kind-`0x0B` delete enqueues, as the
  page's section 1 already said, not "diagnostic sinks" with a slot/error pair. The page's own sections survive whole.

## Current consumers

- consumer: `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md` names the storage machine, not these two
  helpers' role; it agrees.
- consumer: `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md` numbered the
  submission arm state 5 and the stamp state 7, and wrote `00582730(rdi, path, 8)`; revised-here (`CON-192`). Its
  member table already reads `rdx` / `r8d` as the buffer and the size; it agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-191`, `CON-192`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_manual_save.py` M1. It fails unless both helpers store their
kind (7, `0x0B`) into a stack packet passed to `00582540`, and both kind-7 calls in `00581DA0` pass `rdx` = the image
and `r8d` = 8.

run: verified at 55c9b3929 (BROKEN 0, exit 0), against the certified image `73461d08…`.
