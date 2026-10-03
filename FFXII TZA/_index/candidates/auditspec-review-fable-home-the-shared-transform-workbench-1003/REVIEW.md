# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-shared-transform-workbench-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-SHARED-TRANSFORM-WORKBENCH-10` · Package: `_index/candidates/fable-home-the-shared-transform-workbench-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `e0e99b7c6`; the package is unmodified in the working tree) · Page: `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact against the bytes. The body writes the very bit that this page's `003B24C0` reads and that its `003B1710` pump gates on, in the `02EBE5E0` table the page describes. The host fits on data.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 736 and the row (line 742) matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0.
- **`003B2750` (0x4F B), read in full.**
  - `and eax, 0xF0000000` / `cmp eax, 0x70000000` / `jne ret`.
  - The scan runs from `02EBE5E0` with `add rax, 0x30` / `cmp rax, r11` (`02EBEBE0`) / `jl`. 0x600 / 0x30 = 32 records.
  - `test edx, edx` / `je ret` comes before `cmp edx, ecx`, so a zero key stops the scan without a write.
  - A full scan leaves `r8d` = 0x20, and `cmp r8d, 0x20` / `je ret` then writes nothing.
  - On a match, `and byte [r9+0x20], 0xFE` / `and r10b, 1` / `or byte [r9+0x20], r10b`.
  - Every clause holds. All 5 anchors are on these instructions.
- **entered_from.** `0036E9B0` + 0x32 = `0036E9E2`, a tail `jmp 003B2750` with `edx` = `setne(r8d)` and `ecx` = dword `+0` of the clamped (`0..0x1F`) 24-byte record at `022D94B0`. It is the only caller (raw E8/E9 index).
- **Host fit.**
  - The page cites `0036E9B0` as the end of the `022D94B0` reader family ("one tight family (`0036DDC0`–`0036E9B0`)", BQ-17, line 314), and `0036E9B0` does read `022D94B0`.
  - The data match is stronger. The page's SWE2-EC7-89 note says `003B24C0` returns `byte[slot + 0x20] & 1` from the same tag-checked `02EBE5E0` scan. The SWE2-EC7-90 note says the pump `003B1710` gates each slot on that bit. This body is the setter.
  - Apart from an inbox note, no other page cites `003B2750`.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not defects)

- The caller is cited only as the endpoint of a span. The host is right because of the `02EBE5E0` bit, not because of that citation. One extra clause, "the bit `003B24C0` returns", would put the reason in the row itself.
