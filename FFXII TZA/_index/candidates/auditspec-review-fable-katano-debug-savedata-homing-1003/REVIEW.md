# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-katano-debug-savedata-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-KATANO-DEBUG-SAVEDATA-HOMING-1003` · Package: `_index/candidates/fable-katano-debug-savedata-homing-1003/` · Page: `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/katano-debug-savedata.md` (commit b7c6eb07d)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 5 functions, 25 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 5 row(s), 25 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...), call offsets resolved:
  - `001C1C00` exact: `[rcx]` = 0 first; n = `dword [rdx] & 0x7FFFFFFF`; `0017D260(n*8, 8)` and `001C19A0(result, qword [rdx+8], n)` when non-null; qword `+8` = the result (0 when skipped); `cmovne` stores n only for a non-null result; returns `rcx`.
  - `001C1E70` exact: 0x28 bytes copied (one 16-byte move plus qwords `+0x10`/`+0x18`/`+0x20`), `001C1C00` at `+0x44` on `+0x28`, qword `+0x38` = `001C26B0(qword [rdx+0x38] - (byte & 1))`, `0067ACF0` at `+0x69` on `+0x40`, nine 16-byte moves `+0x58`..`+0xE7`, bytes `+0xE8`..`+0xEA`, dwords `+0xEC`..`+0xFC`, 16 bytes at `+0x100`, dwords `+0x110`..`+0x124`; returns `rcx`.
  - `0063AD30` exact: bit 31 clear -> n > 1 (unsigned `jbe`) `001C2720(qword [rdx+8], n)`; n == 1 `00584730` when the qword is non-null with bit 0 clear; n == 0 nothing; every path zeroes qword `+8` and dword `[rdx]`; `al` = 1.
  - `0063DCA0` exact: `r9 == rdx` -> stores; `r9 == rcx+8` -> `00584730(qword [r9])` when non-null with bit 0 clear; else bit 31 of `[rcx]` clear -> `001C2720(r9, [rsp+0x60])` (the 5th argument); then `[rcx]` = `r8d` and, unless `rdx == rcx+8`, qword `+8` = `rdx`.
  - `0063DE10` exact: `r8d` negative -> 5 (`jns`); n = low 31 bits; old pointer = qword `+8` (n > 1), `rcx+8` (n == 1), 0 (n == 0); `r8d` == 1 -> `00584730` when n == 1 and non-null with bit 0 clear, qword `+8` = `001C26B0(qword [rdx] - (byte & 1))`, pointer `rcx+8`, count 1; otherwise `rdx` and `r8d | 0x80000000` (`bts`); both call `0063DCA0` at `+0xB3` with (`rcx`, pointer, count, old, n at `[rsp+0x20]`); returns 0.
- Limits hold: body statements only, static evidence; the draft and FABLE's re-read are not independent review, this record is.
