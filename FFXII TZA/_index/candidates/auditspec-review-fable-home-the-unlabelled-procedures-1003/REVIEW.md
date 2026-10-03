# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-unlabelled-procedures-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-UNLABELLED-PROCEDURES-1003` · Package: `_index/candidates/fable-home-the-unlabelled-procedures-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `16-UI/Unlabelled-Panes/the-unlabelled-procedures.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 4 rows are exact. Each body has a single caller, the handbook text pane `005701B0`. This page has a section on that pane and names its `00181B90`–`00181DD0` markup-parser family, and three of the bodies lie inside that range.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 4 functions, 17 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 282, and the rows at lines 288–291 match `rows.json` byte for byte.
- **rows.json.** 4 rows, 17 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **`00181BD0` (0x3C B):** `00181BD6 call 001EBA40` (+0x6) / `mov rbx, [rax+0x278]` / `je ret`. Then `00181BE7 call 001B6C40` (+0x17) / `je ret`. Then `00181BF1 call 001B6C40` (+0x21) → `rcx`, `rdx` = `rbx`, and `00181C01 jmp 001B68D0` (+0x31). Exact.
- **`00181D50` and `00181D80` (0x2B B each):** `xmm0` = `xmm1` = 1.0 (`01CEBBA8`), then the call at +0x11 to `00182BE0`. Its result is stored at `[001EBA40() + 0x270]` (`+0x278` for `00181D80`); the getter is the call at +0x19. Exact.
- **`0056FEA0` (0x44 B):** `00577A00([rcx+0xC0])` at +0x10, then `00244F00` on `[+0x140]` at +0x21 and on `[+0x150]` at +0x32, each null-checked. Then `jmp 00244F00` with `rcx` at +0x3F. Exact.
- **entered_from.** The raw byte scan finds exactly one reference to each, all in `005701B0`:
  - `00570350` = +0x1A0;
  - `0057025F` = +0xAF;
  - `00570264` = +0xB4;
  - `00570339` = +0x189.
- **Host fit.**
  - Line 49 has the classification row "`005701B0` … **handbook text pane** — calls the `00181B90`–`00181DD0` markup-parser family".
  - Line 83, in the section for `005701B0`, says its call set is "the `00181B90`–`00181DD0` block plus `001846B0`/`001846F0` — a self-contained text/markup family no other screen touches — and the quest-list cluster … `00577A00`".
  - `00181BD0`, `00181D50` and `00181D80` are inside that block. `0056FEA0` is the pane's teardown into the named `00577A00` cluster.
  - All four fit, and none is cited on any other page (repo-wide grep).
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Here the caller is also cited at lines 9, 49, 81 and 159.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
