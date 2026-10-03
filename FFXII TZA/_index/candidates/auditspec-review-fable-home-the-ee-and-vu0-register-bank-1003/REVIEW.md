# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-ee-and-vu0-register-bank-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-EE-AND-VU0-REGISTER-BANK-1003` · Package: `_index/candidates/fable-home-the-ee-and-vu0-register-bank-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package is unmodified in the working tree) · Page: `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md`

## SWE2-AUDIT-SPEC verdict: REJECT

The sentence, site and anchors are exact. **The host is wrong.**

- `003AC870` resets two cells of the character light pool: the light scale `02B3F51C` to 1.0, and its enable byte `02B3F503` to 0. `17-Presentation-Rendering/Character-Rendering/how-a-character-is-lit.md` describes exactly that pair: "while the byte `02B3F503` is set the colour is scaled by the global `02B3F51C`", lines 111-112.
- This page cites the caller `00376470` once, in the census of C routines with at most four register-bank accesses (line 172, "`00376470` `Rvf00×2 Wvf01`").
- The body touches no EE or VU0 register, so the section heading is false for it.

The only row is mis-homed.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 2 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 408 and the row (line 414) matches `rows.json` byte for byte.
- **rows.json.** 1 row, 2 anchors. Rejected 2 (`006AA200`, `006AA600`, both "already cited by" `the-fifteen-modules-registered-before-main.md`), skipped 0, missing 0.
- **`003AC870` (0x18 B).** `movss xmm0, [01CEBBA8]` / `movss [02B3F51C], xmm0` / `mov byte [02B3F503], 0` / `ret`. Exact.
- **entered_from.** `00376470` + 0x82 = `003764F2`, `call 003AC870`. It is the only caller (raw index). It runs just before the per-record batch over `02ADBB50` (8 records of 0x90 B).
- **What the cells are.** `ripscan` puts `02B3F500`-`02B3F518` in the light-pool family (`003AB960`, `003ABB60`, `003ABCA0`, `003ABD20`, `003AC110`). Other pages read them that way: `how-a-character-is-lit.md` (the class filter `02B3F501`, the scale `02B3F51C` and enable `02B3F503`), `how-a-status-shows-on-a-character.md` (lines 312-327, the list `02B3F508`, scale `02B3F518`, enable `02B3F502`) and `the-world-tick-and-the-field-frame.md` (lines 1563-1564).
- **Host fit.** This page is about the PS2 register bank at `022D8F10`-`022D949F`. The caller is cited only for its vf accesses, and the body does not touch the bank. Apart from this row, no page cites `003AC870`.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC repair

1. Remove the row from this package and from the section already on the page (the applier prints `ALREADY`). With no rows left, remove the section heading, its intro and the table header too.
2. Re-home the row **unchanged** on `22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md` (AUDITED). That page reads `00376470` as a body ("Interior citation — frontier hubs `00376470`", line 1216) and already hosts its other callee `00376AC0` (line 1489). Optionally, add "(the light scale and enable byte read by `how-a-character-is-lit.md`)" to the sentence.
