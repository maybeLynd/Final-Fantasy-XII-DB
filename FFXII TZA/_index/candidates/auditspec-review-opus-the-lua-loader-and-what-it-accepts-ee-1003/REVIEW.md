# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-the-lua-loader-and-what-it-accepts-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-LUA-LOADER-AND-WHAT-IT-ACCEPTS-EE-1003` · Package: `_index/candidates/opus-the-lua-loader-and-what-it-accepts-ee-1003/` · Page: `23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh, verify only (no `--apply`): exit 0, `VERIFY 44 functions, 220 anchors` / `ALREADY` / `FAILS 0`.
- `rows.json`: 44 rows, 220 anchors. README reports 0 rejected and 0 missing.
- Semantic pass: **16 of 44 rows** read clause by clause against the resolved disassembly of the certified image (SHA256 `73461D08...21F8`, rip targets resolved by `disr.py`). The sample includes every corrected row except `00811470`/`00811640`, whose correction is identical to the checked `008113D0`/`00811530`. Import slots were resolved from the IAT: getenv, fopen, freopen, getc, ferror, fclose, _errno, strerror, __acrt_iob_func, memmove. Every quoted string was read from the image: `_CLIBS`, `LUA_PATH_5_2`/`LUA_PATH`/`LUA_CPATH_5_2`/`LUA_CPATH`, `LUA_NOENV`, both default paths, `;;`/`;\1;`/`\1`, the 10-byte config `5C 0A 3B 0A 3F 0A 21 0A 2D 0A`, `_LOADED`, `_PRELOAD`, `searchers`, `C stack overflow`, both coroutine messages, `loop in settable`, `index`, `=stdin`, `@%s`, `r`, `rb`, `open`, `reopen`, `read`, `cannot %s %s: %s`, `C levels`, `%s expected`, `syntax error`, `EASTL basic_string`. The `0082D130` jump table (index bytes `0082D2C0`, offsets `0082D290`) was decoded separately.
  - `001600D0`: length `008FCDA4-008FCDA0+1` = 5; `jbe 1` → one-byte buffer `02EBA2E0`; memmove 4 bytes of `true`; tail `jmp 00808B90(008A80A0)`. Exact.
  - `00682E30` (corrected): the `je` at `00682E9A` reads ZF from `sub rbx, rax`, i.e. the cleared pointer; tail insert before the sentinel at `[+0x10]+0x90`; byte-compare skip on an equal non-null name. Exact.
  - `008113D0` / `00811530` (corrected): `v` = `[[rcx+0x20]]`, `0x16` test on `[v+8]`, base `[v]`, signed `jg` bound on byte `[[v]+0xA]`, slot `[v]+((0xFFF0B9D8-idx)+1)*16`; positive index uses unsigned `cmovb` against `[rcx+0x10]`. `008113D0` follows the truth rule (tag 0, or tag 1 with dword 0). In `00811530`, a type nibble other than 4 goes to `00823280` with the slot in `rdx`, then `0081A8A0` (signed `jle`) and `0080F300`. Exact.
  - `0081E5A0` (corrected): `jb` 200 on word `+0x46`; the three messages; byte 0 → `0081DCD0(rcx, rdx-0x10, -1)` else tail `008216A0`; byte 1 with a null `c+0x38` reaches `0081DC10` with the incoming `rdx` (`0081E6E0` → `0081E6FE`). Exact.
  - `008233F0` (corrected): `jbe` at `008234AD` sends at-or-below to the line hook; `0081DA20(rcx,3,-1)` for the count event; `jns` on byte `c+0x22` is the bit-0x80 test; the yield tail is as listed. Exact.
  - `00828D30` (corrected): `00812B70(REG,"_CLIBS")`, `__gc` metatable, `0080F740(rcx,0,2)`, setfuncs `01CCC940` (0 upvalues). The env path is getenv → `LUA_NOENV` toboolean → two gsubs → `00810D20(-2)`. `008109F0(REG,2)` / `00810730(-2)` / `008135B0(01CCC970,1)`; `settop(-2)`; returns 1. Exact.
  - `0082F000` (corrected): the fifth argument of both `00830540` calls is `r15d`/`r12d` (`0x4003` = false load, `0x800003` = true load, else -1); the controlling-instruction test is a signed `jl` on byte `01CCCCD0[op]`; the final `{6, r8d, -1, -1}`. Exact.
  - `005850F0`, `00585270` (sibling): `+0x18` = second-called result, `+0x20` = first (`0062FFC0` first in the sibling); `rcx+1-(rcx&1)` sets bit 0; unsigned two-key compare, `shr edx,31` picks child `+0`/`+8`; parent+1 stored. Exact.
  - `00823030`: 100-round loop counted only on non-function handlers; fasttm guard (bit 2 of `+0xA`); barrier condition (`0x40`, `&3`, bit 4); four pushes then the stack check; `0081D900(rcx, top-0x40, 0, bit0 of [ci+0x22])`. Exact.
  - `00812FA0`: the BOM match with partial bytes kept in `rsp+0x40`; `#` line skip then append 0xA; the `0x1B` reopen; `00810180(rcx, 008120F0, &state, tostring(-1), mode)`; ferror path returns 7. Exact.
  - `00829810`: unsigned `sub 7 / ja` kind check; conflict retarget (`+0xF`/`+0xE`, word `+0xC` with `movsx`); `cmove` picks 0 for kind 7, else 5; `00829E10(fs, nCcalls+r8d, 200, "C levels")`; signed `jle` before lowering `fs+0x44` by `n-r8d`. Exact.
  - `006853C0`: an empty `r9` string becomes null (`cmove`); unsigned bounds; `02E41058` set around each call and cleared after; memcpy `00861EBA`; slot returned only when it is still the last. Exact.
  - `0082AAD0`: fifth argument at `[rsp+0x90]` (3 pushes + `0x50`); `0082F470(fs,0x21,edx,0x1FFFE)` / `0082FB30`; loop op 0x20 versus `0082F450(fs,0x22,edx,0,r9d)` + `0082F960` + `0082F470(fs,0x23,edx+2,0x1FFFE)`. Exact.
  - `0082D130`: the jump table gives 0x3B, 0x10B, 0x116, 0x103, 0x108, 0x111, 0x109, 0x10D, 0x11D, 0x112, {0x102, 0x10A} → the listed arms, and all 215 other tokens in range `0x3B..0x11D` → `0082A660`; `ja` default; epilogue `fs+0x44 = fs+0x42`, word `+0x46` += 0xFFFF. Exact.
- Non-blocking notes (no change required; neither clause states anything false):
  - The four index-resolution rows (`008113D0` family) partition the index as positive / "negative above" / equal / below. Index 0 also takes the "above" arm (`[rcx+0x10]` + 0), which the wording leaves unstated.
  - In `00823030`, "copies the 16-byte value" is two stores, qword `+0` and dword `+8`, the value and type of the 16-byte slot.
- Limits hold: body statements only, static evidence. A local draft plus OPUS's re-read is not independent review; this record is. 28 rows were not read by this reviewer.
