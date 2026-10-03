# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-message-window-layout-readers-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-MESSAGE-WINDOW-LAYOUT-READERS` · Package: `_index/candidates/fable-home-the-message-window-layout-readers-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package is unmodified in the working tree) · Page: `16-UI/Message-Windows/the-message-window-layout-readers.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 3 rows are exact against the bytes. Each body is entered from a message-window function that this page reads, and each acts on the window object or its line records.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 3 functions, 15 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 315 and the three rows (lines 321-323) match `rows.json` byte for byte.
- **rows.json.** 3 rows, 15 anchors. Rejected 0, skipped 0, missing 0.
- **`002A2BB0` (0x3D B).**
  - The null `rcx` path returns 0.
  - Then `movsx rax, byte [rcx+0x3B8]` / `cmp dword [0209C4D0 + rax*8], ecx` / `sete` / `je` returns 0. Only the low 32 bits of `rcx` are compared.
  - Then `cmp qword [rcx], 0` / `jne` returns 1, else `test byte [rcx+0x7C], 0xF`.
  - Exact.
- **`002A7D30` (0xE7 B).**
  - Bit 4: `and` then store, `movzx` byte `+0x2F` to word `+0x16`, `call 002A7A60` at +0x19.
  - Bit 0x10: `+0x4C + +0x48` to `+0x24`, and `+0x54 + +0x50` to `+0x28`.
  - Bit 8: four `movsx` word (`+0x38..+0x3E`) + `movzx` byte (`+0x34..+0x37`) float sums, `cvttss2si`, stored to bytes `+0x20..+0x23`.
  - The body re-reads `[rcx+8]` after the call. `002A7A60` never writes `rcx`, so the sentence is right to treat `rcx` as unchanged.
  - Exact.
- **`002A84B0` (0x37 B).** A null return, then `and eax, 0x3FF` / `or eax, 0x19064C00` / store `+0x7C`, then `00247570(rcx, 00916490)` at +0x24 and `00244F00(rcx)` at +0x2C. Exact.
- **entered_from.**
  - `0035E070` + 0x62 = `0035E0D2`.
  - `002A36A0` + 0x50 = `002A36F0`, inside a loop over the window's `+0x3F0`-counted 0x60-stride records at `+0x3F8`.
  - `002A7F70` + 0x51 = `002A7FC1`, with a second site at `002A8056`.
  - These are the only callers (raw index).
- **Host fit.**
  - `0035E070` is the page's message-window reader (lines 51, 69, 123), and the page scans the `0209C4D0` records (line 291).
  - `002A36A0` is "the state-byte loop the window refresh drives" (line 267).
  - `002A7F70` is the `MsgWinSignalLeftOffset` reader (line 59).
  - Apart from `_index/ADDRESS-INDEX.md`, no other page cites the three bodies.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not defects)

- `002A84B0`'s second site (`002A7F70` + 0xE6, `002A8056`) could be added to its row.
