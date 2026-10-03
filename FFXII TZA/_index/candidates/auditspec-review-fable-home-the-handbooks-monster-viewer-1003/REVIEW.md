# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-handbooks-monster-viewer-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-HANDBOOKS-MONSTER-VIEWER-1003` · Package: `_index/candidates/fable-home-the-handbooks-monster-viewer-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `16-UI/Handbook/the-handbooks-monster-viewer.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Both rows are exact. Both callers are read in this page's section 4, and each body has a single caller.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 2 functions, 10 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 233, and the rows at lines 239 and 240 match `rows.json` byte for byte.
- **rows.json.** 2 rows, 10 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **`003A2C80` (0xFB B): exact.**
  - `lea eax, [r8+0xF]` / `cdq` / `and edx, 0xF` / `add` / `sar 4` is a signed `(r8d+15)/16`.
  - When `r8d` is non-zero and `[02F8F2D0] + n*16 >= [02F8F2D8]` (`jae`, unsigned), it returns without writing.
  - The record is word `02F8F2C6` × 0x28 into `[02F8F2F8]`, and the word is incremented. `+0` = `[02F8F2D0]`; `+8` = the 5th argument (`[rsp+0x50]` after `push` + `sub 0x20`); `+0xB` = `r9b`; `+0xC` = `r8d`; `+0x10` = `rcx`.
  - `+0x20` = `(([02AEF41C]*2) | (call +0x8E != 0 or [02AEF418] != 0)) * 2`.
  - Then `003A2D52 memcpy` (+0xD2) of n×16 bytes from `rdx`, and `[02F8F2D0]` += n×16.
- **`00504700` (0x33 B): exact.** `test byte [rcx+0x244], 0x10` / `je`. When set: `0050471A call 0053D780(rcx, 1, 1)` (+0x1A). Then, in both cases, `0050472E jmp 0053D780(rcx, 1, 0)` (+0x2E).
- **entered_from.** The raw byte scan finds one reference to each: `004781D1` = `004781A0` + 0x31, and `00478006` = `00477F20` + 0xE6.
  - `004781A0` (`RenderModelInstanceContainer_QueueActiveEntryCallback_Mode1`) has no direct caller. It is passed by `00477F5A lea rdx, [004781A0]` inside `00477F20`.
  - `004781A0` calls `003A2C80` with `rcx` = `0016D6A0` (the queued callback), `rdx` = the entry, `r8d` = 0x260 and the 5th argument = `[rcx+4] >> 4`.
- **Host fit.**
  - `00477F20` is "the model-instance container pass" that this page reads (line 106). Its evidence row (line 145) lists `00478006`, which is this call site.
  - Line 119 says "In mode 1 the callback `004781A0` (59 B) instead queues each active entry into the sorted display list with key `+4 >> 4` - **and the draw callback it queues is the image's folded empty function**".
  - `003A2C80` is that queue insert: the display list `[02F8F2F8]` with count `02F8F2C6`, and the payload copied into the frame arena at `02F8F2D0`. `00504700` is the container pass's per-instance call.
  - Both fit, and neither is cited on any other page (repo-wide grep).
- **Advisory (not a defect).** `003A2C80` is the generic insert into the depth-sorted display list that `003A3740` drains. That list is described on `the-vif1-vu1-layer.md` (line 246, "the sorted draw list `[02F8F2F8]`, count `02F8F2C6`") and `the-six-vfx-display-layers.md` (line 46). A cross-reference would show readers that it is shared machinery that has only one direct caller.
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Both callers are also cited outside the section.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
