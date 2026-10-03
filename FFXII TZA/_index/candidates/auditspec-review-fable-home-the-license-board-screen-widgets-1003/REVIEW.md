# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-license-board-screen-widgets-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-LICENSE-BOARD-SCREEN-WIDGETS` · Package: `_index/candidates/fable-home-the-license-board-screen-widgets-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package is unmodified in the working tree) · Page: `16-UI/License-Board-View/the-license-board-screen-widgets.md`

## SWE2-AUDIT-SPEC verdict: REJECT

All three sentences, sites and anchors are exact. **All three hosts are wrong.**

- Every row is entered from `002C2320`, which this page cites once, in §8a. There it is one of the three bodies that store the dialog reply id `0x11D` (line 216); the other two are the shared Yes/No box and message box. It is not a license-board widget.
- `16-UI/Shared-Dialogs/the-shared-dialog-widgets.md` treats `002C2320` as its own ("`002C2320` on this page", line 243; the geometry-pass row at line 141).
- That page already hosts `003FF9A0` (line 280), homed from `002C2320` + 0x561. `003FF9A0` works on the same `[0209AC30]+0x108` object that `003FF160` creates and `003FF9F0` writes.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 3 functions, 13 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 360 and the three rows (lines 366-368) match `rows.json` byte for byte.
- **rows.json.** 3 rows, 13 anchors. Rejected 0, skipped 0, missing 0.
- **`0027F150` (0x45 B).** `[0209AC30] + 0xD48`. Each word is tested against `0xFFFF` then `0x1000`, and any other value goes to `xor eax, eax`. The loop is `add rax, 0x20` / `cmp rcx, 5` / `jl`, then returns 1. Exact.
- **`003FF160` (0x81 B).**
  - The stack block is `[rsp+0x20]` dword 0, `[rsp+0x28]` = `movsxd ecx`, `[rsp+0x30]` = `movsxd edx`.
  - When `[0209AC30]+0x108` is null: `00244F50(0x190, 003FF360, &block)` at +0x4D, store to `+0x108`, `00246AD0([0208EA28], result)` at +0x6A.
  - Both paths reach `__security_check_cookie` at +0x77 with the cookie `01F44830`.
  - Exact.
- **`003FF9F0` (0x30 B).** A null test on `+0x108`, `ecx` to `+0x178`, `+0x108` re-read, `rdx` to `+0x180`. Exact.
- **entered_from.** `002C2320` + 0x895 (`002C2BB5`), + 0x35F (`002C267F`) and + 0x5E2 (`002C2902`) are direct calls. They are the only callers (raw index).
- **Host fit: the defect.**
  - This page's subject is the main-menu board view's widget tree. `002C2320` appears only as a poster of reply id 285. The page attributes that id to the shared dialogs, and `the-widget-message-protocol.md` (line 449) assigns `002C2320`'s arms to "those screens' pages".
  - Nothing here reads `[0209AC30]+0x108`, `+0xD48` or `003FF360`.
  - `002C2320` is read as a body on `the-shared-dialog-widgets.md` (lines 141, 243, 280) and on `ui-layout-parameters-and-editor-schema.md` ("the id-8 geometry-pass proc").
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC repair

1. Remove all three rows from this package and from the section already on the page (the applier prints `ALREADY`). With no rows left, remove the section heading, its intro and the table header too.
2. Re-home all three **unchanged** on `16-UI/Shared-Dialogs/the-shared-dialog-widgets.md`, beside `003FF9A0`. That page cites `002C2320` in its own text, so the applier's caller check passes there.
