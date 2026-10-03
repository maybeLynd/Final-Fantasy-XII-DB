# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-selection-the-menu-publishes-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-SELECTION-THE-MENU-PUBLISHES` · Package: `_index/candidates/fable-home-the-selection-the-menu-publishes-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `c6de67245`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `16-UI/the-selection-the-menu-publishes.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Both rows are exact, including the signed clamp. Both bodies have a single caller, the battle-menu window procedure `0027E530`, and this page reads that procedure in an interior-citation row.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 2 functions, 6 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 291, and the rows at lines 297 and 298 match `rows.json` byte for byte.
- **rows.json.** 2 rows, 6 anchors. Rejected 2: `00270F50` ("already cited by" this page) and `003F3080` (already cited by `the-widget-message-protocol.md`). Skipped 0, missing 0, corrections 0.
- **`0039C100` (0x12 B):** `movsxd rax, [02AEE894]` / `lea rcx, [02AEE898]` / `mov eax, [rcx + rax*4]`. Sign-extended index, no compare anywhere. Exact.
- **`0039C120` (0x24 B):**
  - `mov eax, 1` / `cmp ecx, eax` / `cmovge eax, ecx` is a signed lower clamp to 1.
  - `mov ecx, 0x1A` / `cmp eax, ecx` / `cmovg eax, ecx` is a signed upper clamp to 0x1A.
  - `dec eax` / `movsxd` / `[02AEE898 + rcx*4]`. Exact: index `clamped - 1`, which is 0..0x19.
- **entered_from.** The raw byte scan finds one reference to each: `0027E6B8` = `0027E530` + 0x188 and `0027E6C6` = +0x196. The caller converts both results with `cvtdq2ps`, subtracts the second from the first and multiplies by 0.5 (`01CEBB70`).
- **Host fit.**
  - `0027E530` is cited in body statements on this page: line 131 ("a 634-byte **procedure** that cases 15–18 install") and line 257, OPUS's interior row for `0027E530`. It is also cited at lines 4 and 125.
  - Both bodies read the `02AEE898` dword table for that procedure's display arithmetic. No other function reaches either body. They fit.
  - Neither body, nor `02AEE894`/`02AEE898`, is cited on any other page (repo-wide grep).
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Here the caller is also cited four times outside the section.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
