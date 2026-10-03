# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-embedded-lua-and-phyre-object-bindings-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-EMBEDDED-LUA-AND-PHYRE-OBJECT-BINDINGS-EE-1` · Package: `_index/candidates/opus-embedded-lua-and-phyre-object-bindings-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

29 of the 44 rows were read clause by clause against the bytes. All 29 are exact. No row changes.

## SWE2-AUDIT-SPEC checks

- **Mechanical, all 44 rows.** I did not run `interior_applier.py`, because it writes the page. An independent script decoded every function with `disr.py` and found:
  - all 220 anchors are instruction boundaries inside the listed extent, each with the recorded mnemonic;
  - every row's `text` appears verbatim on the page, in the interior table at lines ~1315-1358.
  - Result: 0 failures, which agrees with `interior_applier.out` (FAILS 0).
- **Sample.** I took all even 0-based indices (0, 2, ..., 42). I added 1, 3, 5, 33, 35, 37 and 43 so that every near-identical family has at least one member in the sample, and two where the family has close variants:
  - the index-to-slot resolver prefix: rows 3, 4, 5 and 6;
  - the `string` byte-map trio: rows 24 and 26;
  - `__pairs` / `__ipairs`: row 12;
  - the bit32 extract / replace pair: row 30;
  - the `io.input` / `io.output` pair: rows 35 and 36;
  - the debug `o`/`L` thread-argument pair: row 43.
- **String operands.** I resolved every quoted string from the image bytes. Each one matches its row, for example:
  - `00D6FDE0` "PhyreObject" and `01CCA278` "buffer too large";
  - `01CCA9E0` "wrong number of arguments to 'insert'";
  - `01CCBF50` "_IO_output" and `01CCBFD0` "_IO_input";
  - `008C5880` "r", `008C587C` "w" and `01CEB638` "" (the empty string);
  - `01CCC214` "cur" and `01CCC678` "Lua function expected".

| # | fn | verdict | decisive instructions |
|---|---|---|---|
| 0 | `005C3CA0` | exact | `005C3CC8` cmp/`jle` on `02CB5D40`; `005C3CDC` cmp -1; `005C3CEC` or 1; stores `005C3CF0`/`CFC`/`D03`; returns `02CB5D28` at `005C3D1A` |
| 1 | `00683DC0` | exact | null branch `00683DD8`→`00683E2E`/`00683E40` jmp `00810620`; `00810240(rcx,0x10)` at `00683DE7`; `00683DF8`/`00683DFF` stores; edx `0xFFF0B9D8` (-1001000) at `00683E0A`; tail `00810F60(-2)` at `00683E29` |
| 2 | `0080F420` | exact | `movsxd` `0080F444`; signed `jle` `0080F44A`; `+5` against `0xF4240-n` at `0080F463`/`0080F467`; slot `rsp+0x38` = entry `[rsp+0x10]` after push+sub 0x20; `jae` `0080F4AD` (stores only when the field is below) |
| 3 | `0080FA50` | exact | resolver as in row 4; `t` read at `0080FAD7` before the call `0080FAE1`; `or 0x40` `0080FAF0`; `add 0x10` `0080FAF9`; jmp `00822BC0` with r8 = r9 = top-0x10 |
| 4 | `0080FBA0` | exact | `cmovb` `0080FBBD`; `== 0x16` `0080FBEA`; `byte [g+0xa]` `0080FBF4`; `(u+1)*16` `0080FBFD`-`0080FC0B`; tt 5/7 `0080FC21`/`0080FC26`; `+0x1a8` `0080FC33`; 0x45 `0080FC53` |
| 5 | `00810DF0` | exact | `t+0x10` stored at `00810E85`, before the call `00810E89`; `00823030` r8 = top-0x10, r9 = top-0x20; `add -0x20` `00810EB2` |
| 6 | `00811950` | exact | tt 2 → `[slot]` (`008119E5`); 7 → `+0x30` (`008119E0`); otherwise 0 (`008119DA`) |
| 8 | `00813450` | exact | `jae` `00813477` (unsigned); size test `0081348A`; both error tests `00813493`/`0081349E`; memcpy `008134C7` (dst new, src p, n u); `p != rcx+0x20` `008134D0` |
| 10 | `008145B0` | exact | t 0/5 test `008145DC`/`008145E1`; non-zero `__metatable` → `jmp 00812960` `00814623`; otherwise returns 1 |
| 12 | `00814950` | exact | `jne` `00814974`; `008148F0` closure; zero `[rsp+0x20]` arg `008149B9`; `0080F3A0(1,3,0)`; returns 3 on both paths |
| 14 | `00814A70` | exact | `setne bpl` `00814AC9` (type != -1); non-zero → `00810620`, `0080FEE0(-2)`, returns 2; flag path `00810730(3)`, `00811180(-2,1)`, returns 1 |
| 16 | `00814F90` | exact | two `008109F0(-1001000,2)`; "_G"; `008135B0(01CCA3F0,0)`; "Lua 5.2", 7; "_VERSION" |
| 18 | `00815540` | exact | `e = len+1` `00815575`; `n==2` `00815580`; `cmovle` max `008155A9`; loop `008155B0`-`008155D7` down to `p+1`; insert message `01CCA9E0` |
| 20 | `008158A0` | exact | `0080F740(n,1)`; field "n"; `n>0` `008158E6`; loop `i>=2` `00815932` |
| 22 | `00815A40` | exact | `008126E0(0x28, "")` `00815A79`; arg 2 positive `00815A8D`; `00815AD0(1,e)` |
| 24 | `008168A0` | exact | reverse index `[rdx+rdi-1]` with `rdx = len-i` (`008168F2`/`008168F5`); `00813560(rsp+0x30, len)`; cookie `00808C40` |
| 26 | `00816A00` | exact | `call [008C2FF0]` `00816A68` on the zero-extended byte; low byte stored `00816A6E` |
| 28 | `00816E50` | exact | `00812740(1,6)`; `0080F7B0(00818490, buf)`; non-zero → "unable to dump given function" |
| 30 | `00818950` | exact | `jns` `008189AF`; `jg` `008189C7`; `f+w > 0x20` `008189E0`; mask `not(-2<<(w-1))` `008189F7`-`00818A02`; `shl` by `cl` `00818A0B`/`00818A0F`; `and`/`or` `00818A12`/`00818A17` |
| 32 | `00825490` | exact | `00812430(1)`; `008136B0(1,"FILE*")`; null → `00810620`; `[p+8]==0` → "closed file", 0xb; otherwise "file", 4 |
| 33 | `00825570` | exact | type -1 → `0080FA50(-1001000,"_IO_output")`; `[p+8]` reloaded, zeroed `008255E1`; `jmp rdx` `008255EE` |
| 34 | `00825770` | exact | `[p+8]=0` `008257C9` before `00813680`; `call [008C2EC8](name, mode)` `008257DC`; `[p]` then `[p+8]=00826370`; failure → `00812A50(0,name)` |
| 35 | `008258A0` | exact | same shape as row 36 with "r" and `01CCBFD0` "_IO_input" |
| 36 | `00825930` | exact | `jle` `00825945`; "w" `008C587C`; `008269F0` then `00810730(1)`; `00810DF0`/`0080FA50` both on `01CCBF50` "_IO_output" |
| 37 | `00825A10` | exact | type -1 → `00810620` `00825A2B`; second type 0 → `_IO_input` path, `00825F20(rcx,0)`; otherwise `008266D0(..,"r")`, `00825F20(rcx,1)` |
| 38 | `00825CA0` | exact | `xorps xmm2` `00825CFF`; `cvttss2si`/`cvtsi2ss`/`ucomiss` with `jp`+`je` (`00825D12`-`00825D24`); dword `[01CCC050+k*4]`; `call [008C2E38]` then `[008C2EB0]` |
| 40 | `00827570` | exact | type 2 → light-userdata error, arg `rax-1` = 1; `00812740(1,7)`; arg 2 positive → `00812740(2,5)`; `00811130(2)`, `008112E0(1)` |
| 42 | `00827DA0` | exact | `008283F0(1,2)`/`(3,4)`; two `0080FF90` checks; `00811BD0(1, a, 3)` with `b` at `[rsp+0x20]` (`00827E25`) |
| 43 | `00828330` | exact | type 8 `00828358`; `o`/`L` select; nil test via `jle` `0082839A`; `sete r14b` `008283B2` (L is rcx) as the default for `00813330` |

## SWE2-AUDIT-SPEC narrowing / notes

No narrowing.

**Notes (non-blocking):**
- **Signedness.** In rows 0 and 2, "above" stands for a **signed** comparison: `jle` at `005C3CCE`, `0080F44A` and `0080F46A`. Where the bytes compare unsigned, the rows say so: row 8 uses "not below" (`jae`) and row 23 writes "(unsigned)". So the wording is consistent, but a reader cannot tell from "above" alone whether a comparison is signed. This changes nothing for the values these paths see.
- **The applier's limit.** As the README says, `interior_applier.py` re-checks only anchors and mnemonics, not sentences. My sample found no sentence defect. The 15 rows outside the sample (7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 39 and 41) passed only the mechanical check.
- **Missing functions.** The package lists 33 functions as `missing`, with no row. This review does not cover them.
