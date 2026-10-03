# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-lua-loader-and-what-it-accepts-ee-1003-3)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-LUA-LOADER-AND-WHAT-IT-ACCEPTS-EE-C82E6` · Package: `_index/candidates/opus-the-lua-loader-and-what-it-accepts-ee-1003-3/` (reviewed at HEAD `f227ff3da`) · Page: `23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 10 rows. All 10 were read clause by clause against a raw capstone decode of the certified image. This session checked the image hash: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. All 10 rows hold as written, including the three OPUS corrections (`00810470`, `0081EFB0`, `0082A7C0`). No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 10 functions, 50 anchors` / `ALREADY` / `FAILS 0` and exited 0. The rows are already in the page block `## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-the-lua-loader-and-what-it-accepts-ee-1003-3)`, lines 685-700.
- **Counts.** There are 10 rows with 5 anchors each, 50 anchors in total. Every listing ends in `ret`, a tail `jmp` or a final non-returning `call`, followed by int3 padding.
- **Constants, strings and thunks read from the image.**
  - `01CCA3C8` is the float -4660.0 (bytes `00a091c5`).
  - The strings are `01CCA320` "multiple Lua VMs detected", `01CCA340` "version mismatch: app. needs %f, Lua core provides %f", `01CCD078` "<goto %s> at line %d jumps into the scope of local '%s'", `01CCD0B0` "labels/gotos" and `01CCD308` "control structure too long". `01CCA380` is "bad conversion number->int; must recompile Lua with proper settings"; the row quotes no text for it.
  - `00861EBA` is `jmp [008C2A68]`, and that IAT slot is VCRUNTIME140 `memcpy`.

Per row:

- **`00810470`** (`00810470`-`0081053F`): exact.
  - `0081047F`: `movsxd rdi, r8d`.
  - The zero path is `0081048D`-`0081049B`: it stores `rdx` with tag 0x16 and adds 0x10.
  - `008104B0`-`008104BB`: `0081A8A0` is called with `rcx` unchanged, gated by `jle` on qword `[[rcx+0x18]+0x18]`.
  - `008104C5` calls `0081ECA0(rbx, edi)`. `008104DE` stores `[c+0x18]`, and `008104E2` adds -16·sext(`n`).
  - The copy loop is `00810500`-`0081051B`. The source is `[rbx+0x10]` (re-read) + 16k, and the destination is `c`+0x20+16k for k = `n`-1 down. The count is `sub edi,1` / `jne` on the 32-bit `n`, which supports the 2^32 + `n` clause.
  - `00810526`-`00810530` store tag 0x66 and advance.
- **`00810730`** (`00810730`-`008107BF`): exact.
  - `00810737`/`00810739` test `edx` with `jle` (signed).
  - `0081074C`/`00810750`: `cmovb` keeps qword `[c]`+16`i` only when it is below the top (unsigned), and otherwise uses `01CCB510`.
  - `0081075B`/`0081075D`: `jle` against 0xFFF0B9D8, then top + 16`i` (`00810766`).
  - `0081076C`/`0081076E`: on equality, `[rcx+0x18]`+0x40.
  - The upvalue path is `00810778`-`0081079E`:
    - `v` = qword `[c]`, and `k` = 0xFFF0B9D8 - `i`.
    - Tag test 0x16 at `0081077D`.
    - Byte `[qword [v]+0xA]` is compared with `jg` (signed) at `0081078E`.
    - The slot is `[v]` + (k-1+2)·16.
  - The push is `008107AA`-`008107BA`.
- **`00810D20`** (`00810D20`-`00810DBD`): exact. The lookup is the same as `00810730` (`00810D27`-`00810D90`). The shift loop is `00810D97`-`00810DB6`: it starts at `p`+0x10, compares with `jae`/`jb` (unsigned) against `[r8+0x10]` re-read on each pass, and copies the qword and the dword down one slot. `00810DB8` subtracts 0x10.
- **`00812890`** (`00812890`-`00812959`): exact.
  - `008128A5`/`008128AF`/`008128B4`: `00811D10(rcx)` is compared with `00811D10(0)`, and on a difference `008128C3` calls `00812960(rbx, 01CCA320)`.
  - `008128CE`-`008128D3`: `ucomiss`, then `jp` to the error and `je` to skip, so a NaN counts as not equal.
  - `008128E5`/`008128DF`/`008128EE`/`008128E9`: r8 = the entry xmm1 as a double, r9 = float `[v]` as a double, then the `008128F3` call.
  - `008128F8`/`00812903`: xmm1 = -4660.0, then `00810640(rbx)`.
  - `00812911`/`00812916`: `00811470(rbx, -1, 0)`, then `cmp rax,-0x1234`.
  - `00812927`/`0081292C`: `00811890(rbx, -1, 0)`, then `cmp eax,0xFFFFEDCC`. Either mismatch goes to `0081293D`, which calls `00812960(rbx, 01CCA380)`.
  - `00812942`-`00812959`: `jmp 00811130` with `edx` = -2.
- **`0081DA20`** (`0081DA20`-`0081DB12`): exact.
  - The early-out tests are `0081DA45`/`0081DA48` (`h` null) and `0081DA4E`/`0081DA52` (byte +0x49).
  - The offsets are kept in `r14` = `[rcx+0x10]`-`[rcx+0x38]` and `r15` = `[c+8]`-`[rcx+0x38]` (`0081DA70`-`0081DA80`).
  - The record is at `rsp+0x20`: +0 = `edx` (`0081DA84`), +0x28 = `r8d` (`0081DA88`), and +0x78 = `c` (`0081DA8D`, `r11-0x40` = `rsp+0x98`).
  - `0081DA91`/`0081DA97`: `jg` 0x140 (signed) skips the `0081D9A0(rcx, 0x14)` call at `0081DA9E`.
  - The stores before the callback are `0081DAA3`-`0081DABD`. `0081DAC1` is `call rsi`.
  - The restores are `0081DAC3`-`0081DAED`, each from `[rbx+0x38]` re-read.
  - The cookie `01F44830` is checked by `00808C40` (`0081DB04`).
- **`0081EFB0`** (`0081EFB0`-`0081F042`):
  - `0081EFC0`/`0081EFC4`: `ja` 0x28, otherwise a tail `jmp 0081EDC0` with the argument registers unchanged.
  - `0081EFD5`-`0081EFDD`: `lea rax,[r8+1]` / `cmp rax,-0x23` / `ja` to `call 00823710` at `0081F042`, which is the last instruction.
  - `0081EFFC` loads `ebx` = dword `[[rcx+0x18]+0x50]` before the call at `0081F003`. That call is `0081A620(rcx, 0x14, r8+0x21, 0, [rsp+0x20]=0)`. I read `0081A620`: it reads a fifth dword from entry `[rsp+0x28]` at `0081A64C`, so five arguments is right.
  - The stores are `0081F015`-`0081F01C`, and `0081F020` calls `memcpy(s+0x20, rdx, r8)`. `0081F032` writes the zero byte.
  - Exact, as corrected by OPUS.
- **`0082A7C0`** (`0082A7C0`-`0082A911`):
  - Entry caches: `r14` = `d`, `r15` = `g`, `rax` = `f`. `0082A7E0` loads `i` = movsx word `[[f+0x20]+0xA]`.
  - The loop compare is signed (`jge` at `0082A7E9`, `jl` at `0082A897`) against `[r14+0x18]`, re-read on every pass.
  - `0082A81B` calls `0081EEF0([e], [g])`.
  - On a match, `0082A824` re-reads `rbx` = `[rcx+0x50]` and `0082A82D` re-reads `r10` = `[rcx+0x30]`. `0082A838`/`0082A83C` compare with `jb` (unsigned).
  - The error path is `0082A8B6`-`0082A911`. The index is movsxd(byte + dword `[f+0x3C]`). The movsx word comes from `[[[f+0x18]+0x50]]`. The name is `[[[f]+0x30] + 16w]` + 0x20. `0082A8FF` calls `0081BFF0([rcx+0x38], 01CCD078, [e]+0x20, [e+0xC], name)`, and `0081BFF0` is a varargs wrapper (it spills r8/r9 and forwards a va pointer). `0082A907` zeroes `[rcx+0x10]`, and `0082A911` (`00824330`) is the last instruction.
  - The no-error branch calls `0082FDE0(r10, [e+8], [g+8])` at `0082A849`. The shift loop is `0082A860`-`0082A886` (16+8 bytes). `0082A888` decrements the count, and `0082A88B` jumps back to the compare without `inc esi`.
  - Exact, as corrected by OPUS.
- **`0082C0B0`** (`0082C0B0`-`0082C21A`): exact.
  - `l` = `[[rcx+0x18]+0x50]`+0x10 is kept at `[rsp+0x88]`. Its count (`0082C0E0`, `0082C1AA`) and its array (`0082C110`) are re-read on every pass.
  - `0082C0C8` loads `i` = movsx word `[b+0xA]`.
  - The level clamp is `0082C117`-`0082C13E`: `jbe` (unsigned) and a byte `[b+0xD]` gate, then `0082FD80(rcx, [g+8], byte [b+0xC])`, then the store.
  - Inner setup: `s` = `r13` (`0082C141`), `d` = `rsi`, `k` = `[[s+0x30]+0x20]`, and `g` is re-formed from `[d+0x10]` (`r12`).
  - The scan is `0082C162`-`0082C190`: from movsx word `[k+8]`, compared with `jge`/`jl` (signed) against `[d+0x28]` re-read, calling `0081EEF0([e],[g])`.
  - The match path is `0082C1D8`-`0082C215`. It compares with `jbe` (unsigned), then takes the byte `[k+0xD]` `jne` or `jle` (signed) of `[d+0x28]` against movsx word `[k+8]`. It calls `0082FD80([s+0x30], [g+8], byte [e+0x10])`, then `0082A170(s, i, e)`, and jumps to `0082C198` without `inc ebp`.
- **`0082C310`** (`0082C310`-`0082C3C5`): exact.
  - `0082C32A` loads `n` = movsxd count. `0082C341`/`0082C344` compare `n`+1 against the capacity with `jle` (signed).
  - `0082C367` calls `008235B0([rcx+0x38], [rdx], rdx+0xC, 0x18, 0x7FFF, 01CCD0B0)`, and `0082C36C` stores the array.
  - The entry stores are `0082C385`-`0082C3B2`. The fifth argument is `[rsp+0x60]`, which is entry `rsp`+0x28.
  - `0082C3B7` increments the count, and `eax` = `n`.
- **`0082FB30`** (`0082FB30`-`0082FBE6`): exact.
  - `0082FB3A`/`0082FB42`: `j` is loaded, then set to -1. `0082FB4C` calls `0082F360(rcx, 0x7FFF8017)`.
  - The early returns are at `0082FB54`-`0082FB6D`.
  - The walk is `0082FB80`-`0082FBA0`: `shr` 14, `sub` 0x1FFFF, then stops on an offset of -1 or a next index of -1.
  - The abs is `cdq/xor/sub` at `0082FBAE`-`0082FBB1`, and `0082FBB3`/`0082FBB8` compare with `jg` 0x1FFFF (signed).
  - The patch is `0082FBBA`-`0082FBCA`: AND 0x3FFF, then OR (`j`-`i`+0x1FFFE)<<14.
  - The error path is `0082FBDB`-`0082FBE6`: `00824330([rcx+0x18], 01CCD308)`, the last instruction.

**10 of 10 exact.** All 50 anchors were checked.

## SWE2-AUDIT-SPEC limits

- Body statements were checked against the bytes. Meanings were not reviewed, including the Lua API names the page gives these functions.
- Callee behaviour was read only where a row depends on it: the arity of `0081A620`, the varargs shape of `0081BFF0`, and the IAT name behind `00861EBA`. Callees that a row names only as calls are opaque here: `0081A8A0`, `0081ECA0`, `00811D10`, `00812960`, `00810640`, `00811470`, `00811890`, `00811130`, `0081D9A0`, `0081EDC0`, `00823710`, `0081EEF0`, `0082FDE0`, `00824330`, `0082FD80`, `0082A170`, `008235B0` and `0082F360`. The "(the body ends there)" clauses mean that the call is the body's last instruction before int3 padding. They make no claim that the callee never returns.
- Wording note, not a defect: in `0082A7C0` and `0082C0B0`, "while below" is not labelled signed, but the compares are signed (`0082A7E9`/`0082A897`, `0082C0E3`/`0082C1AD`, `0082C165`/`0082C190`). The starting index is stated as signed, so the sentence is not wrong.
- One package record was cut short, and it is not part of a row. In `rows.json` `corrections`, the `0082A7C0` text ends mid-word ("(same "), and README.md's third correction bullet stops at the same point. This does not affect any row.
- README.md records 1 function as skipped by the session. It is outside this review.
- This review is a non-author read. It does not replace a live check of any behaviour.
