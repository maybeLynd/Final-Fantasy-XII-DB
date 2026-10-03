# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-ppfx-function-identification-ee-1003-2)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-PPFX-FUNCTION-IDENTIFICATION-EE-1003-1AAFC` · Package: `_index/candidates/opus-ppfx-function-identification-ee-1003-2/` · Page: `17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The narrowing is on one row, `006E04F0`. That row states the gates of its first two logs. Its last three logs are written as unconditional, but each sits behind the same two-dword gate. The other three rows are exact.

## SWE2-AUDIT-SPEC narrowing

- **`006E04F0`, final clause.** Replace

  > a negative result of either call is logged (`00D8FE38`/`00D8FE80` or `00D8FED8`/`00D8FF20`, with `0071B3C0`) and returned, the second after calling `rcx`'s vtable slot `+0x30`; on success it calls `007224B0` with 0, logs `00D8FF80`/`00D8FFB0` and returns 0.

  with

  > a negative result of either call is logged when the dwords `01F3BA80` and `01F3BA90` are both non-zero (`00D8FE38`/`00D8FE80` or `00D8FED8`/`00D8FF20`, with `0071B3C0`) and returned, the second after calling `rcx`'s vtable slot `+0x30`; on success it calls `007224B0` with the slot's object and 0, logs `00D8FF80`/`00D8FFB0` when the dwords `01F3BA80` and `02EA0B40` are both non-zero, and returns 0.

  Sites: the gate on the 00721030 failure log is `006E0695 cmp [01F3BA80], 1` / `jb` and `006E069E cmp [01F3BA90], 1` / `jb`. The gate on the vtable-call failure log is `006E06EF` / `006E06F8`. The gate on the success log is `006E0741 cmp [01F3BA80], 1` / `jb` and `006E074A cmp [02EA0B40], 1` / `jb`. `007224B0` takes `rcx` = qword `[rbx]`, the slot's object (`006E0739`), and `edx` = 0. The anchors are unchanged.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 4 functions, 20 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 4 rows, 20 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against a full linear decode of the certified image (SHA256 73461D08..., capstone, function-list extents):
  - `006E04F0` (668 B; frame `rsp` = entry - 0x88, so the 5th..9th arguments are at `rsp+0xB0..0xD0`). Entry log gated `jb` on `[01F3BA80]` and `[02EA0B40]` < 1, i.e. both non-zero. `rdx` null -> `006E0550 mov eax, 0x80070057`. Slot `rbx` = `006E0370(rcx)`. When `[rbx]` is non-null, `006E0370(rdx)` is called and byte `[[slot]]` is tested, then a log gated on `01F3BA80` and `01F3BA90`; after that `[rbx]` is re-read, `006E1130` is called (`006E05B2`) and the slot is cleared. Allocation: `edx` = `lea [r9+0x76]` with `r9d` = 0xAA, giving 0x120; `rcx` = qword `[01F3BA68]` (.data, the correction holds); `r8` = `00D8FE18`; the 5th argument is `00D8FE00` (`006E05E2`). `00720FB0` is called only for a non-null result (it also receives `rdx` = `00D8FE00`). The result goes to the slot and `rdx` goes to `[rsi+0x18]`. A null qword `+0x20` of `006E0370(rdx)`'s object -> `je 006E0550`. `0071BA60(ecx` = 7th, `edx` = 8th, `r8` = `&[rsp+0x98]`, `r9` = `&[rsp+0x30])`. The descriptor at `rsp+0x48` holds 0, `r8d`, `r9d`, 6th, 5th, out1, out2, 9th, as stated, and goes to `00721030(rcx` = slot object, `006E068A)`. `jns` -> clear byte `01F3CB3C`, then `call [vtbl+0]` (`006E06E7`) with `rdx` = the `+0x20` qword. A negative result is logged behind the gate and returned; on the second failure `[[rsi]+0x30]` is called on `rsi` = original `rcx` first. Success -> `007224B0`, a gated log, 0. The only defect is the gates omitted in the final clause (above).
  - `006E07A0` exact (278 B): entry and exit logs are both gated by `cmp ... ,1` / `jb` on `01F3BA80` and `02EA0B40`, so "at least 1 (unsigned)" is exact. `rdi` = `006E0370([rcx+0x18])` slot object, or 0 when that qword is null (`006E07F8`). `rsi` = `006E0370(rcx)`; an empty slot goes to the exit log. Byte `[rdi]` non-zero -> a log gated on `01F3BA80` and `01F3BA90`. `sub dword [obj+8], 1` (`006E0847`) / `jne`; at zero, `call [vtbl+0x20]` with `edx` = 0 (`006E085C`), then `006DA8A0(qword [01F3BA68], obj)` (`006E0865`). The slot is cleared (`006E086A`) on both the zero and non-zero paths, which matches the row's "then clears the slot". Returns `xor eax, eax`.
  - `00722900` exact (299 B; frame = entry - 0x68, so the 5th..9th arguments are at `rsp+0x90..0xB0`). `bt edx, 0x14` (`00722917`, bit 0x100000) `jb` -> else-path; byte `[02EA18B1]` zero -> else-path. Call `00722C80(rcx` = 5th qword, `edx`, `xmm1` = 6th float, `r8d` = 7th, `r9` = 8th, stack = 9th) (`00722954`); `xor ebx, ebx` / `test` / `cmovs ebx, eax` (`0072295D`) returns the result if negative, else 0. Else-path: `test cl, 0x10` -> `00722800(ecx` = `r8d`, `rdx` = `r9`, `xmm2` = 6th, `r9d` = 7th, stack = 9th) (`007229AB`), `js` returns it. Loop `ebx` = 0..7 (`cmp ebx, 8` / `jb`, unsigned): `bt edi, ebx` set -> `007226E0(ecx` = index, `edx` = `ebp`, `r8d` = `r14d`, `r9` = 5th, stack: 6th float, 7th, 8th) (`007229F1`); `js` returns the first negative; falling out gives `xor eax, eax`.
  - `0078A120` exact (273 B; frame = entry - 0x48, so the 5th argument is at `rsp+0x70` and the 7th at `rsp+0x80`). A null out-pointer gives `0078A14E mov eax, 0x80070057`. Then `[out]` = 0; `007906C0(rdx, qword [rcx+0x30], movzx byte 7th)` (`0078A16D`); a null result -> 0x80004005. `006DA880(qword [01F3BA68], 0xE8, 00DAEE68, 0x55C, 0)` (`0078A1A2`); `00789900(obj, rcx)` runs only when the result is non-null; the object or null is stored to `[out]`; `007897D0(obj, res)` (`0078A1C8`); `0078A4F0(res)` (`0078A1D2`); `jns` -> 0. On a negative result: `00DAEEC0`, then `00DAEF10` with `0071B3C0(code)`, both under the `01F3BA80`/`01F3BA90` gate, and the code is returned.
  - Anchors: all twenty are instruction boundaries strictly inside their bodies and decode to the recorded mnemonics.
- Limits hold: body statements only, static evidence; the cloud draft and OPUS's re-read are not independent review, this record is.
