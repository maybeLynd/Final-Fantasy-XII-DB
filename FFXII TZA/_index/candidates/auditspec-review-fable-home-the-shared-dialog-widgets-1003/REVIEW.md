# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-shared-dialog-widgets-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-SHARED-DIALOG-WIDGETS-1003` · Package: `_index/candidates/fable-home-the-shared-dialog-widgets-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `16-UI/Shared-Dialogs/the-shared-dialog-widgets.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Both sentences are exact, including FABLE's correction to `003FF9A0`. `00270230` fits, and so does `003FF9A0`.

*Reconciled by the SWE2-AUDIT-SPEC parent before publication (2026-10-03).* The first draft of this record called `002C2320` "the license-board screen procedure" and moved `003FF9A0` to `the-license-board-screen-widgets.md`. A sibling review, `auditspec-review-fable-home-the-license-board-screen-widgets-1003`, routed the opposite way, so both premises were checked:
- `002C2320` has no direct caller in the call index. The UI atlas row (`16-UI/Menu-Screen-Atlas/members/ui_atlas_all.tsv`) gives it as the **"menu list + action list"** widget procedure (subtree 98, installed by `002C2280`), a shared menu widget.
- The license-board page names it (line 216) only as one of the three bodies that post the shared-dialog reply id 285, alongside the Yes/No box `002CDF20` and the message box `002CE370`.
- This page treats it as its own function (lines 141 and 243).

So `003FF9A0` is correctly homed here. The sibling review's REJECT stands: it moves the license-board page's three `002C2320` callees (`0027F150`, `003FF160`, `003FF9F0`) here, next to `003FF9A0`.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 2 functions, 10 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 273, and the rows at lines 279 and 280 match `rows.json` byte for byte.
- **rows.json.** 2 rows, 10 anchors. Rejected 0, skipped 0, missing 0. Corrections 1 (`003FF9A0`, "+0x170 of the +0x108 pointer"; the corrected text is the one on the page).
- **`00270230` (0x2D B): exact.**
  - `xmm0` = `xmm2` + `[rdx]` goes to `[rcx]`; `xmm1` = `xmm3` + `[rdx+4]` goes to `+4`.
  - `xmm2` + `[rdx+8]` goes to `+8`; `xmm3` + `[rdx+0xC]` goes to `+0xC`.
- **`003FF9A0` (0x47 B): exact.**
  - `mov rcx, [[0209AC30]+0x108]` / `je ret`. Then `rcx = [rcx+0x170]`, `r9d` = `r8d` = `edx` = 0, and `003FF9C6 call 002D4840` (+0x26).
  - Then `rcx` = `[[0209AC30]+0x108]` re-read, and `003FF9DD jmp 002470D0` (+0x3D).
- **entered_from.** The raw byte scan finds one reference to each: `0028D767` = `0028D460` + 0x307, and `002C2881` = `002C2320` + 0x561.
- **Host fit.**
  - **`00270230`.** It fits. `0028D460` is one of this page's layout-key readers, a body row at line 139 (`m2DSideCursorCenterX`/`Y`, "the side cursor's centre subtracted from the anchor point"). The body offsets that cursor's rectangle by the two passed floats, and it has no other caller.
  - **`003FF9A0`: the defect.**
    - On this page `002C2320` appears only as "`002C9BF0` (→`002C2320` geometry pass)" in a layout-reader row (line 141) and in the pass-22 Items/License neighbour sentence (line 243).
    - `the-license-board-screen-widgets.md` line 216 reads it: "Only three bodies store `0x11D` into a message — `002C2899`, `002CE103`, `002CE417` — in `002C2320`, the Yes/No box `002CDF20` and the message box `002CE370`".
    - The same commit `410ec4476` homed `0027F150`, `003FF160` and `003FF9F0`, three more single-call callees of `002C2320` (+0x895, +0x35F, +0x5E2), on that page (rows at lines 366–368). `003FF9F0` is the function immediately after `003FF9A0`.
    - The `0209AC30` block whose `+0x108` widget this body drives is the battle modal-state singleton (`battle-runtime-mode-ladder.md` lines 895 and 909). Its license-board slot `+0x320` is set by `0055C690` (`the-license-board-grid-build-and-its-change-sweep.md` line 368).
    - Nothing ties the body to the shared dialogs.
- **Advisory (tool).** The applier's caller test is a substring test. The parenthetical "→`002C2320`" was enough to qualify this page.

## SWE2-AUDIT-SPEC advisory (not a defect)

- Correct the README's row count and regenerate `homing_applier.out`. The first draft's N1 (re-home `003FF9A0`) is withdrawn; see the reconciliation above.

Limits: static evidence only. A cloud draft plus FABLE's re-read is not independent review; this record is.
