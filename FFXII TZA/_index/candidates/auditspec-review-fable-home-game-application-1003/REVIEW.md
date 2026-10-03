# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-game-application-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-GAME-APPLICATION-1003` · Package: `_index/candidates/fable-home-game-application-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `e0e99b7c6`; the package is unmodified in the working tree) · Page: `00-Engine-Core-Runtime/Application-Root/game-application.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact against the bytes. The body is a flag setter that the PauseMenu handler `00229590`, read on this page, calls on its open and close arms.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 2 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 2483 and the row (line 2489) matches `rows.json` byte for byte.
- **rows.json.** 1 row, 2 anchors. Rejected 1 (`001A49C0`, "already cited by" this page; the page does cite it), skipped 0, missing 0.
- **`0025A880` (0xE B), read in full.** `xor eax, eax` / `test ecx, ecx` / `setne al` / `mov [02098354], eax` / `ret`. The sentence is exact. Both anchors (`0025A884` setne, `0025A887` the store) are on it.
- **entered_from.** `00229590` + 0x293 = `00229823`, `call 0025A880`, with `ecx = [rbp+0xC4]`. The raw index has two more sites: `00229887` in the same handler, where `ecx` = 0 after `[rbp+0xC4]` takes the getter `0025A850()` at `0022987A`, and a tail `jmp` at `003503C2` (`003503B0`). `0025A850` is the only reader of `02098354` (`ripscan`).
- **Host fit.** The page reads `00229590` as the PauseMenu message handler (line 264, and the `00229590` exclusive-subtree section at line 676 with its bool-setter adapters). The handler saves the flag through `0025A850`, clears it through this body on open (`00229887`) and restores it on close (`00229823`). That is the same pattern as the subtree's other setters. Apart from `_index/ADDRESS-INDEX.md`, no other page cites `0025A880`.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not defects)

- The save, clear and restore through `0025A850` and `[rbp+0xC4]` is the useful fact about this flag. It could join the subtree table at line 676 as one line.
- README: "No page cited these 2 functions" counts the rejected `001A49C0`, which this page does cite.
