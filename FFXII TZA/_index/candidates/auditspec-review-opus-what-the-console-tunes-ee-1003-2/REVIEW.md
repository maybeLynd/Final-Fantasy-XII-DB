# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-what-the-console-tunes-ee-1003-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-WHAT-THE-CONSOLE-TUNES-EE-1003-2-A7AD5` · Package: `_index/candidates/opus-what-the-console-tunes-ee-1003-2/` (reviewed at HEAD `a028be1b9`) · Page: `00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 3 rows. All 3 were read clause by clause against a raw capstone decode of the certified image. This session checked the image hash: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. All 3 rows hold as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 3 functions, 15 anchors` / `ALREADY` / `FAILS 0` and exited 0. The rows are already in the page block `## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-what-the-console-tunes-ee-1003-2)`, lines 1291-1297.
- **Counts.** 3 rows with 5 anchors each, 15 anchors in total. Each listing ends in `ret` or a tail `jmp`, followed by int3 padding, and matches its function-table size (0x1BD, 0xCF, 0x1D6).
- **Thunks, IAT slots and table read from the image.**
  - `00861ED2` is `jmp [008C2A00]`, and that IAT slot is VCRUNTIME140 `memcmp`.
  - MSVCP140 slots: `008C25E0` `basic_ios<char>` constructor, `008C25D8` `basic_ostream<char>` constructor (`basic_streambuf*`, `bool`), `008C2798` `basic_streambuf<char>` constructor, `008C27B0` `basic_streambuf<char>::_Init`, `008C26A0` `basic_ios<char>::setstate`, `008C24E0` `basic_ios<char>::clear`, `008C25D0` `basic_ostream<char>` destructor, `008C25E8` `basic_ios<char>` destructor. The row's names for these slots match.
  - The dword table at `002002C0` (image base + 0xE02C0), each + 0x120000: [0] `0020021F`, [1] `0020025D`, [2] `00200264`, [3] `0020026B`, [4] `0020028B`, [5] `002002A6`.

Per row:

- **`001FF4F0`** (`001FF4F0`-`001FF6AC`): exact.
  - `001FF520`/`001FF524`/`001FF528`: walk start qword `[rcx+0x18]`, `h` = `rcx`+8, `b` = `h`.
  - `001FF530`-`001FF537`: `L` = `[k+8]`-`[k]`. In the loop, `001FF540`-`001FF548` form `M` = `[n+0x28]`-`[n+0x20]`, and `001FF54F`-`001FF55E` pick min(L, M) with a signed `cmovge`.
  - `001FF564`: `memcmp([n+0x20], [k], min)`. A nonzero result goes to `js` (`001FF57A`); a zero result orders by `cmp rsi,r14` `jl` / `setg` (M against L, signed). The below case takes `[n]` (`001FF585`); otherwise `001FF57C`/`001FF57F` record `b` = `n` and take `[n+8]`. `001FF588`/`001FF58B` loop until null.
  - `001FF591`-`001FF5DB`: when `b` is not `h`, `memcmp([k], [b+0x20], min(L, M of b))` at `001FF5C5`, a zero result ordering by L against M (`jl`/`setg`); `jns 001FF68E` returns `b`+0x40.
  - `001FF5E1`-`001FF5F8`: `t` = dword 6 at `rbp-0x48` and qword 0 at `rbp-0x40` (t+8); `p` = `rbp-0x38`, three qwords zeroed (p, p+8, p+0x10).
  - `001FF608` `001EDF00(p+0x18, k+0x18)`; `001FF618` `001A4BF0(p, [k], [k+8])`; `001FF626` `001FE6B0(p+0x20, t)`; `001FF647` `001FFD40(rcx, &r, &b, p, low byte of b)` (the byte at `[rsp+0x20]` is `movzx` from the slot holding `b`); `001FF654` `002001F0(p+0x20)`.
  - `001FF65A`-`001FF680`: `[p+0x10]`-`[p]` `jle` 1 (signed) skips, `[p]` null skips, otherwise `call [[p+0x18]+0x18]` with (p+0x18, `[p]`, `sub ecx,edx` low dword).
  - `001FF688` `002001F0(t)`; `001FF68E` returns `r`+0x40.
- **`002001F0`** (`002001F0`-`002002BE`): exact.
  - `002001FF`-`0020021D`: `movsxd` of dword `[rcx]`, `cmp eax,5` `ja` (unsigned) to the return at `002002B9`, table at +0xE02C0, `jmp rdx`.
  - Tag 0 (`0020021F`): `p` null returns; `0020022C`-`0020024F` test `[p+0x10]`-`[p]` with `jle` 1 (signed) and `[p]` null, then `call [[p+0x18]+0x18]` with (p+0x18, `[p]`, low-dword difference); then `00809950(p, 0x20)` by the tail `jmp` at `002002B4`.
  - Tags 1, 2, 5 (`0020025D`, `00200264`, `002002A6`): `edx` = 4, 8, 1, then `002002AB` loads `p` with no null test and tail-jumps to `00809950`.
  - Tag 3 (`0020026B`): `p` null returns; `0020027B` `00200140(p, [p+0x18])`; tail `00809950(p, 0x38)`.
  - Tag 4 (`0020028B`): `p` null returns; `00200297` `001C36F0(p)`; tail `00809950(p, 0x20)`.
- **`00202930`** (`00202930`-`00202B05`): exact. `rbp` = `rsp`+0x100, so `s` = `rsp+0x20` and `b` = `rsp+0x28` = s+8.
  - `0020296C`/`00202973` store `008F3F50` at `[s]` before `0020297C` calls the `basic_ios` constructor on `rbp-0x38` = s+0xA8.
  - `0020299A`: `basic_ostream` constructor with (s, b, 0, 0).
  - `002029A1`-`002029C5`: `d` = movsxd dword `[[s]+4]`; `008F3F48` stored at s+`d`; `d`-0xA8 at `[rsp+rcx+0x1C]` = s+`d`-4.
  - `002029D7` `basic_streambuf` constructor on `b`; `002029DE`/`002029E5` store `008F3EC8` at `[b]`; `002029EA`/`002029EE` zero bytes `rbp-0x5C` = b+0x7C and `rbp-0x67` = b+0x71; `002029F7` `_Init(b)`; `002029FD` zeroes qword b+0x80; `00202A05`/`00202A0C` copy qword `01F81140` to b+0x74; `00202A10` zeroes qword b+0x68.
  - `00202A18`-`00202A2A`: `0019B990(b, [rdx], 2, 0x40)` (`r8d` = 0x40-0x3E). Null goes to `setstate(i, 2, 0)` at `00202A4C`, else `clear(i, 0, 0)` at `00202A59`, with `i` = s+`d`.
  - `00202A5F`-`00202AA2`: when qword b+0x80 is non-null, `00202A76` calls `00201460(rcx, s, movzx r8b, movzx r9b)`, then `0019B8C0(b)` at `00202A80`, and on null `setstate(i, 2, 0)` at `00202AA2`.
  - `00202AA9`-`00202AC6` re-store `008F3F48` and `d`-0xA8; `00202ACF` `0019B400(b)`; `00202AD9` `basic_ostream` destructor on `rsp+0x30` = s+0x10; `00202AE3` `basic_ios` destructor on s+0xA8.

**3 of 3 exact.** All 15 anchors were checked.

## SWE2-AUDIT-SPEC limits

- Body statements were checked against the bytes. Meanings were not reviewed.
- Callee behaviour was read only where a row depends on it: the thunk and IAT name behind `00861ED2` (the ordering clauses read its result as a byte comparison) and the eight MSVCP140 slot names in `00202930`. Callees that a row names only as calls are opaque here: `001EDF00`, `001A4BF0`, `001FE6B0`, `001FFD40`, `00809950`, `00200140`, `001C36F0`, `0019B990`, `00201460`, `0019B8C0` and `0019B400`. The vtable call targets are not resolved.
- `008F3F50`, `008F3F48`, `008F3EC8` and `01F81140` are stated as stored or copied values only; the rows give them no meaning, and none was reviewed.
- This review is a non-author read. It does not replace a live check of any behaviour.
