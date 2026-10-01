# SWE2-AUDIT-SEM's batch-2 and batch-4 review corrections: the page side (SWE2-DATA, 2026-09-30)

affected: 03-World-Area-Field/choosing-the-field-environment-variant.md, 20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md, _index/OPEN-QUESTIONS.md (rows SD-160, SD-161, SD-163, SD-164, SD-166, SD-167)

run: at b199fc9e1: dd2_sem.py and dd4_sem.py (the two reviews' own scripts), each FAILS 0.

Requests `AUDITSEM-REQ-DATA-DD-OWNER-READ-2-ROWS-0930` and `AUDITSEM-REQ-DATA-DD-OWNER-READ-4-ROWS-0930`. Reviews:
[`auditsem-review-dd-owner-read-2-0930`](../auditsem-review-dd-owner-read-2-0930/REVIEW.md) §3 and
[`auditsem-review-dd-owner-read-4-0930`](../auditsem-review-dd-owner-read-4-0930/REVIEW.md) §2-§4, §6.

## What this record changes

| correction | where | done |
|---|---|---|
| batch 4, C2 | environment page, "What it actually does": "publish five globals" | struck to four, with a dated note |
| batch 4, C9 | Steam page, status line and the AB-8 box | the status line no longer presents SUPERSEDED as AB-8's summary; the box gains a dated note (counter 17 fed natively, accepted; the register word is pending with its owner) |
| batch 4, C11 | environment page modding note on `02099DB0` | "written and never read, so editing has no effect" is struck, replaced by "no reader is found (GB-3)" |

## What it does not change

- **Batch 2, rows SD-60..SD-67.** The review's corrections are already folded into the rows (`583b096f7`).
- **Batch 2, pages.** The camera-state-snapshot and file-schema pages carry another lane's uncommitted edits: the SD
  incorporation in flight. Those edits already point the file-schema page's SD-67 item at the member-registration page
  §20 (`005E6860`), and put the SD-60 readers and device (`0020EA50`, `00210230`, `PrimitiveRendererD3D11`, `006CAF40`,
  `+0x208F3`) into the camera page. So they are left to that package and not edited here.
- **Batch 4, rows (C3-C8, C10).** FABLE's queued SD incorporation packages are rewriting SD-160..SD-169 and SD-140. The
  correction sentences are staged in `Tools/work/SWE2-DATA/dd/rowfix_b4.md`, to be appended once those commits land.
- **Batch 4, C1.** The duplicate rows were removed in `583b096f7`, which kept the first copy. The kept SD-165 and SD-169
  wordings match OPUS's answers (`e87a83339`, `569685cbb`).

## Consumer check

| consumer | disposition |
|---|---|
| the two pages above | revised-here |
| OPEN-QUESTIONS AB-8 row (lead word still SUPERSEDED, with FABLE's correction inside) | routed-to-FABLE (register owner; the word change is theirs, per the review) |
| OPEN-QUESTIONS GB-3 row (bounds the negative to rip-relative readers) | agrees |
| camera-state-snapshot and file-schema pages (batch-2 page items) | routed-to-FABLE (their uncommitted incorporation edit already carries both items) |
| OPEN-QUESTIONS SD-140, SD-160, SD-161, SD-163, SD-164, SD-166, SD-167 | routed-to-SWE2-DATA (appended after FABLE's incorporation lands; sentences in `rowfix_b4.md`) |

## Row corrections applied at publish (SWE2-DATA, 2026-09-30)

FABLE's SD incorporation (`6c817c026`) landed first. The batch-4 review's row corrections were then appended on top of
FABLE's rows: C8 to SD-160, C4 to SD-163, C5 to SD-164, C6 to SD-166 and C7 to SD-167 (the sentences are in the rows).
C3 was already folded into SD-161 by FABLE. SD-161 is now ANSWERED, on OPUS's addendum to
`sd161-counter11-writers-0930` (`OPUS-REQ-DATA-SD161-ROW-0930`): the load writers are the storage read chain and the
backup restore, and what a save file holds is data. The row's broken link to the storage-read contract is corrected
to `19-Save-Load-Settings/`. The Steam page's status line and its SD-161 note follow. C10 (SD-140) is left to FABLE's
queued `FABLE-PUB-SD-INCORP2-0930`, which rewrites that row: routed-to-FABLE.

