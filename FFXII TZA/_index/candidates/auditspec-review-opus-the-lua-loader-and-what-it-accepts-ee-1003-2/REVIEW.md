# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-lua-loader-and-what-it-accepts-ee-1003-2)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-LUA-LOADER-AND-WHAT-IT-ACCEPTS-EE-DB14E` · Package: `_index/candidates/opus-the-lua-loader-and-what-it-accepts-ee-1003-2/` · Page: `23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 11 rows were read clause by clause against the bytes. Eight rows are exact, and so are all 55 anchors. Three rows need one clause each replaced (below):

- `0081DC10` states a whole-slot copy where the bytes copy 12 of 16 bytes.
- `0082CB10` attaches the "first/count" clause to the kind-12 rewrite only. It applies to both kinds.
- `00830540` says a 9-bit field moves into an 8-bit field.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. Output: `VERIFY 11 functions, 55 anchors`, `ALREADY`, `FAILS 0`, exit 0. `git status` on the page and the package was clean afterwards (HEAD b5028e7e9).
- `rows.json`: 11 rows, 55 anchors. Rejected 0, skipped 0, missing 0, corrections 3. All three corrections hold at the bytes (`0082BA73`..`0082BA9A`, `0082BB8E`..`0082BC01`, `0082C72A`/`0082C72D`).
- Semantic pass: **every row** was read against a full capstone listing of the certified image (SHA256 73461D08...), with rip targets resolved to their section and IAT name.
  - `008109F0` (164 B), exact.
    - idx>0 → `[ [rcx+0x20] ]`+idx·16, kept by `cmovb` (unsigned) below the top `+0x10`, else `01CCB510` (`.rdata`).
    - `cmp edx,0xFFF0B9D8` (= -1001000) / `jle` (`00810A21`). Above that → top+idx·16. Equal → `[rcx+0x18]`+0x40.
    - Below that: n = -1001000-idx. The function value's type `[f+8]`==0x16 → nil (`00810A43`). n > byte `+0xA` (`jg`) → nil. Otherwise closure+(n+1)·16.
    - `0081F580([slot], r8d)` (`00810A74`). Its qword and type dword are copied to the top, and the top grows by 0x10 (`00810A89`).
  - `00812C10` (765 B), exact.
    - `strlen` of the pattern. The buffer record is {`rsp+0x60`, 0x200, 0, L}.
    - `strstr` through IAT `008C2A08` (`00812C91`, `00812E42`).
    - The growth check is free < need. The new size is 2·size, raised to n+need if smaller. Overflow or a too-small size → `00812960(L, 01CCA278)` (`00812D0C`).
    - Then `00810240`, `memcpy` (thunk `00861EBA`), and `00810D20(L,-2)` if the old storage was not inline.
    - The prefix is copied (`00812D69`), then the whole replacement (`strlen` of `r9`). The scan resumes at hit+patlen.
    - The tail goes through `00813450` + `memcpy`, then `008105C0(L, b, n)` (`00812EBF`). A non-inline buffer → `00810D20(-2)`.
    - The result is `00811530(L,-1,0)`, with the cookie checked.
  - `008135B0` (202 B), exact.
    - `xmm1`=`01CCA3C4` (`.rdata` 0x43FB0000 = 502.0), then `00812890`.
    - `0080F420(L, r8d+0x14)` (`008135D5`). A zero result → `00812960(L, 01CCA240, 01CCA308)` (`008135EF`).
    - The per-entry loop runs while `[e]`≠0:
      - `00810730(L,-nup)` ×nup, skipped by `jle` (`00813625`).
      - `00810470(L, [e+8], nup)` (`0081363A`).
      - `00810DF0(L, -2-nup, [e])`.
    - Tail `jmp 00811130` with `not ebp` (`00813675`).
  - `0081DC10` (183 B). All clauses except the one replaced below are exact.
    - `test al,6` (`0081DC2D`). For bit 2 the source is kept relative to `[+0x38]` around `0081DA20(L,1,-1)` (`0081DC41`).
    - `[+0x28]`=`[[ci+0x10]+0x38]` is written for bit 2 or bit 4.
    - `L->ci`=prev (`0081DC65`). The count is `movsx` word `ci+0x20`.
    - Copy loop: `cmp rbx,[+0x10]` / `jae` (unsigned) and `sub r9d,1` / `jne` (`0081DC87`).
    - Fill loop while `r9d`>0: dword `+8`=0 (`0081DCA0`).
    - Top=`rax`, and the function returns count+1.
  - `008241C0` (145 B), exact.
    - `0081EFB0(L, rdx, r8)` (`008241D9`) with `L`=`[rcx+0x38]`.
    - The push: top+=0x10, the qword is stored, and the type is byte`+8`|0x40 (`008241F7`).
    - `0081FB80(L, [[rcx+0x30]+8], top-0x10)` (`0082420E`).
    - Type 0 → dword value=1 and type=1 (`00824219`). Then `[[L+0x18]+0x18]` > 0 (`jle`) → `0081A8A0` (`00824234`).
    - The top shrinks by 0x10, and the result is returned.
  - `0082B9A0` (408 B), exact.
    - `[B]`≠0 and byte `+0xD` → `0082FB30`, then `0082FD80(fs, j, byte +0xC)`, then `0082FE20(fs, j)`.
    - Byte `+0xE` → `0081EF90([ls+0x38], 01CCBCEC)`, then `0082C310(ls, [ls+0x50]+0x20, s, 0, [[ls+0x30]+0x28])` (`0082BA22`), then `0082A7C0` on the 0x18-byte entry.
    - The `nactvar` arithmetic and the unsigned `ja` loop with the word-indexed store (`0082BA9A`) are as stated.
    - `+0x44` ← `+0x42`, and `[dyd+0x28]`=`movsx` word B`+8`.
    - With a predecessor → `0082C0B0(fs,B)` (`0082BAC6`). Otherwise `jge` return.
    - The format choice: byte`+8`==4 and byte`+0xA`>0 (`ja`).
    - `[ls+0x10]`=0, then `00824330` (`0082BB33`). The extent ends right after this call.
  - `0082BB40` (262 B), exact.
    - Token ≠0x120 (`0082BB59`) → `00824340(ls,0x120)`, then `0081BFF0([ls+0x38], 01CCCFC8, s)`, then `00824330`.
    - Otherwise `00824260`, then `0082C220(ls, saved)` (`0082BB81`).
    - `inc byte [fs+0x42]` (`0082BB8A`). Index = byte+(`[fs+0x3C]`-1) → word → entry`+8` ← `[fs+0x28]`.
    - `00829B10(ls, &rec, 0, [ls+4])` (`0082BBD0`). The second write uses `[fs+0x3C]`+`rec+4` (`0082BC01`).
    - The cookie is checked.
  - `0082C6E0` (470 B; `.pdata` runs to `0082C8B9`, so the listing ends before the last error call), exact.
    - Limit `cmp [rdx+0x18],0x7FFFFFFD` / `jle` (`0082C719`). The error path is as stated, with `[[fs]+0x68]` per the correction.
    - The key record {4, `00830510` result, -1} (`0082C756`).
    - `0082D470` and `0082F8E0` (`0082C790`); `]` is 0x5D.
    - `inc [rdx+0x18]`; `=` is 0x3D.
    - `0082F660` ×2, then `0082F450(fs, 0xA, [[cc+0x10]+4], k, v)` (`0082C7FF`).
    - Byte `+0x44` is restored (`0082C804`), and the cookie is checked.
  - `0082CB10` (301 B). All clauses except the one replaced below are exact.
    - Token-0x104 ≤0x1A (`ja`), with `bt 0x4020007` (`0082CB48`), or token 0x3B → (0,0).
    - `0082D470` (`0082CB6A`), and a 0x2C loop counting the expressions.
    - Kind-12 ≤1 (unsigned) → `00830350(fs,&e,-1)` (`0082CBCF`). Kind 12 with one expression → the code dword `&0xFFFFFFDE|0x1E` (`0082CBF5`).
    - Other kinds: one expression → `0082F780`; several → `0082F860` and byte `+0x42`.
    - `00830120(fs, first, count)` (`0082CC0D`), then token 0x3B → `00824260`.
  - `00830350` (184 B), exact.
    - Kind 12: the xor-mask puts `r8d`+1 into `0x7FC000` (`0083037E`).
    - Kind 13: (code&0x7FFFFF)|((`r8d`+1)<<23) (`008303AB`), then (code&0xFFFFC03F)|(byte `+0x44`<<6) (`008303CF`).
    - `+0x44`+1 > byte `[[rcx]]+0x7A` (`jle`, signed) → ≥0xFA → `00824330([rcx+0x18], 01CCD330)`. Otherwise the store (`008303EC`).
    - `inc` (`008303EF`). Other kinds return.
  - `00830540` (373 B). All clauses except the one replaced below are exact.
    - `edx`==-1 → `ret`.
    - next = (code>>14)-0x1FFFF (`00830598`), and -1 ends the chain.
    - The control is code[i-1] when i≥1 (`jl`) and the `.rdata` table `01CCCCD0`[op] is negative (`008305C2`).
    - Opcode 0x1C:
      - `r11d`≠0xFF and ≠ code>>23 → xor-mask into `0x3FC0` (`008305F2`).
      - Otherwise the rewrite (`0083060D`).
      - Then the jump goes to `ebp`=`r8d`.
    - Other opcodes → `esi` (the 5th argument).
    - |target-i-1| > 0x1FFFF (`jg`) → `00824330(.., 01CCD308)`. Otherwise the field is (code&0x3FFF)|((target-i+0x1FFFE)<<14) (`00830642`).

## SWE2-AUDIT-SPEC narrowings

`0081DC10`. Replace

> copies 16-byte values from `rdx` to the frame's function slot (`[frame]`) onward

with

> copies the value qword and type dword (the first 12 bytes) of each 16-byte slot from `rdx` to the frame's function slot (`[frame]`) onward

Why: the loop moves `qword [rdx]` and `dword [rdx+8]` (`0081DC84`..`0081DC8D`). Bytes `+0xC..+0xF` of each slot are not copied.

`0082CB10`. Replace

> when the record's kind dword is 12 or 13 it calls `00830350` with -1 and, for kind 12 with a single expression, rewrites the code dword the record indexes (array at `+0x18` of the function record's first qword) by clearing bits `0x21` and setting `0x1E`, passing byte `+0x42` as first and -1 as count;

with

> when the record's kind dword is 12 or 13 it calls `00830350` with -1, for kind 12 with a single expression rewrites the code dword the record indexes (array at `+0x18` of the function record's first qword) by clearing bits `0x21` and setting `0x1E`, and for both kinds passes byte `+0x42` as first and -1 as count;

Why: `0082CBF8`/`0082CBFC` (byte `+0x42`, `or edi,-1`) are reached from both the kind-13 and the kind-12 paths. The draft's participle attaches them to the kind-12 rewrite only.

`00830540`. Replace

> or rewrites it to opcode 0x1B with that top field moved into `0x3FC0` and the `0x7FC000` field kept

with

> or rewrites it to opcode 0x1B with that top field shifted down by 17 (its low eight bits forming the `0x3FC0` field, its top bit ORed into bit 14) and the `0x7FC000` field kept

Why: `((code & 0xFFB7FFFF) | 0x360000) >> 17` (`00830603`..`0083060D`) moves bits 23..31 (9 bits) to bits 6..14, and `0x3FC0` holds only 8 of them. The original sentence is right only when bit 31 is clear.

Limits: these are body statements read from static evidence. The draft and OPUS's re-read are not independent review; this record is.
