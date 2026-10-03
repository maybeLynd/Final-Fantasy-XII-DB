# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-render-event-selection-evidence-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-RENDER-EVENT-SELECTION-EVIDENCE-1` · Package: `_index/candidates/fable-home-render-event-selection-evidence-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `c6de67245`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Both rows are exact. Both bodies have a single caller, `003B0C50`, the footstep-effect selector that this page's handler table names under command `0x18`. A closer host exists; that is an advisory, not a defect.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 2 functions, 8 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 651, and the rows at lines 657 and 658 match `rows.json` byte for byte.
- **rows.json.** 2 rows, 8 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **`002E9860` (0x28 B):** `mov rax, [rcx+0xC0]` / `test` / `je`, then `mov rax, [rax+0x138]` / `test` / `je`. Then `mov eax, [rax+0x90]` / `shr eax, 3` / `and eax, 1`. A null at either level reaches `xor eax, eax`. Exact.
- **`002E98C0` (0x25 B):** the same two null-checked loads, then `movss xmm0, [rax+0xC0]`. A null reaches `xorps xmm0, xmm0`. Exact.
- **entered_from.** The raw byte scan finds one reference to each: `003B0D28` = `003B0C50` + 0xD8 and `003B0D34` = +0xE4. In that arm `ebp` = 0x67. A zero bit skips the float read (`je 003B0D51`). Otherwise the float goes to `xmm6`, and `r14d` = 1.
- **Host fit.**
  - `003B0C50` is cited on this page at line 540, the handler-array table row `0x18 | 00520C80 | 00421E20 + 003B0C50`.
  - The page's subject is render event selection. `003B0C50` picks the effect constant (`0x64`–`0x67`, `0x94`) by ground type, and the two bodies decide the `0x67` arm and supply its float. They belong to that selection, not to a hub.
- **Advisory (not a defect).** `17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md` reads `003B0C50` whole: line 94 ("the footstep effect … `003B0C50`, 656 B, read whole") and line 1143 (the 19-arm ground-type table at `003B0EE0`). That page would be the more natural home if FABLE consolidates. The applier would pass there, because it cites the caller.
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Here the caller is also cited at line 540, outside the section.
- Neither body is cited on any other page (repo-wide grep).
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
