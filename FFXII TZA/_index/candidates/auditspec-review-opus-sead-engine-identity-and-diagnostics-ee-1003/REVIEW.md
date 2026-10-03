# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-sead-engine-identity-and-diagnostics-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SEAD-ENGINE-IDENTITY-AND-DIAGNOSTICS-56E99` · Package: `_index/candidates/opus-sead-engine-identity-and-diagnostics-ee-1003/` · Page: `18-Audio/sead-engine-identity-and-diagnostics.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 6 rows were read clause by clause against the bytes. Five rows are exact, and so are all 30 anchors. Row `007F3800` needs two clauses replaced (below):

- It lists the four format arguments out of order.
- It calls the second and third dividends "the remainder" and "the rest". The bytes compute both from the quotients truncated to a word and a byte.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. Output: `VERIFY 6 functions, 30 anchors`, `ALREADY`, `FAILS 0`, exit 0. `git status` on the page and the package was clean afterwards (HEAD b5028e7e9).
- `rows.json`: 6 rows, 30 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** was read against a full capstone listing of the certified image (SHA256 73461D08...), with rip targets resolved to their section and IAT name.
  - `007AB240` (334 B), exact.
    - `p`=`[rcx+8]`. A non-null `p` gets one of two releases:
      - When `[p-8]`≠0, `call [[p]]` with `edx`=3 (`007AB26D`).
      - Otherwise `00210EB0(p-8)`.
    - The qwords `+8..+0x20` and dword `+0x2C` are zeroed. `esi`==0 returns 0xF0000000 (`007AB293`).
    - `[+0x28]`=`edx`. The size is `0x18*n` with `cmovo -1`, then `+8` with `cmovb -1`, and goes to `007AD460(8, size, 0)` (`007AB2E6`).
    - `[blk]`=n. The elements from `blk+8` are filled with {`01CB45D8` (`.rdata` address), 0, 0} (`007AB310`). A null result gives a null array.
    - `+8`/`+0x10`=array. The link loop runs n-1 times (`jle` skip) and stores `&e[i]` into `e[i-1]+0x10` (`007AB366`).
    - `+0x18`, `+0x20` and `+0x2C` are zeroed, and the function returns 0.
  - `007BAB30` (334 B), exact. It is the same shape with `r8d`=`rcx`+4=3 and `ecx`=`r8`+5=8 (`007BABC0`/`007BABD0`), and the element pointer `01CB57D8` (`.rdata`).
  - `007E71F0` (234 B), exact.
    - `[rdx]`→`+8`, `[r8]`→`+0x10`, `[r9+8]`→`+0x28` (`007E7227`).
    - The non-zero path: `+0x9C`=1, `[r9]`=`01CB4D48`, return 0.
    - Otherwise `0019C5D0(rsp+0x20, 0x100, 01CB8FA8)` (`007E7241`). The terminator is clamped with `cmp 0xff` / `jl` / `sub 2`, then the newline is written. The NUL index is checked with `jae 0x100` → `00809728`.
    - `OutputDebugStringA` is called through IAT `008C2120`, then `007A5570(2, buf)` (`007E7280`).
    - `+0x9C`=4 (`007E728C`), `[r9]`=`01CB4D48`, return -1.
    - The cookie `01F44830` (`.data`) is checked through `00808C40` on both paths.
  - `007F31F0` (568 B), exact.
    - `ucomiss xmm1,0` / `je` → 0.0 (equal or unordered) (`007F3217`).
    - `r10d`=`[+0x30]`, `jg` (`007F3227`). Otherwise `0019C5D0` with `r9d`=`[+0x30]` on `01CBA280`, then the IAT `008C2120` call and `007A5570(2)` → 0.0.
    - `r8d` dispatch by a `sub 1` chain:
      - 0 → ×`[+0x30]`.
      - 1 → `cvttss2si` as is.
      - 2/3/4 → when byte `+0x18`≠0, × int `+0x24/+0x28/+0x2C`. Otherwise ×`[+0x30]`, then ×0.125 (`00915508`, `.rdata` 3E000000), ×0.5 (`01CEBB70`, 3F000000) or `addss` doubling.
      - Other → 0.
    - `cvttss2si` (`007F3321`).
    - `r9d` dispatch:
      - 0 → /`[+0x30]` (`007F33FC`).
      - 1 → as is.
      - 2/3/4 → /`+0x24/+0x28/+0x2C`. Otherwise /(`[+0x30]`/8), /(`[+0x30]`/2) (signed integer division) or /(2×`[+0x30]`).
      - Other → 0.0.
    - The cookie is checked.
  - `007F3570` (653 B), exact.
    - Byte `+0x18`==0 formats `01CBA220` with `r9d`=0 and the `movsx` word `+0`, byte `+2` and byte `+3`. It logs with 2 and returns `[rcx]`.
    - Otherwise the stack copy is taken. The lexicographic signed compare against `+0xC/+0xE/+0xF` uses `jg` on the word, then the bytes (`007F35BE`), and goes to `01CBA140` with `movsx` word `+0xC` and `007A5570(1)`. The copy is replaced.
    - The strict lexicographic less-than against `+8/+0xA/+0xB` goes to `01CBA1B0` (`007F3625`). An equal copy is not clamped.
    - A copy equal to `+0xC` returns dword `+4`.
    - Otherwise `007F3140(&copy, rcx+8, rcx)` (`007F374A`). The function returns `[+0]` + `movsx`w·`[+0x2C]` + `movsx`b2·`[+0x28]` + `movsx`b3·`[+0x24]` (`007F3774`).
  - `007F3800` (301 B). All clauses except the two replaced below are exact.
    - The dword `[rdx]`=0 (`007F3822`).
    - The error path is taken on byte `+0x18`==0, `[+0]` > `r8d` (`jg`, `007F3837`) or `r8d` > `[+4]` (`jg`).
    - Call `007F2EA0(rdx, rcx)` (`007F389B`), returning `rdx` on both paths, with the cookie check.

## SWE2-AUDIT-SPEC narrowings

`007F3800`, first replacement. Replace

> formats `01CBA0C0` with that byte, both bounds and `r8d` through `0019C5D0`

with

> formats `01CBA0C0` through `0019C5D0` with, in argument order, that byte, dword `+0`, `r8d` and dword `+4`

Why: `r9d`=byte (`007F38A2`), `[rsp+0x20]`=`[rbx]`, `[rsp+0x28]`=`esi` (=`r8d`) and `[rsp+0x30]`=`[rbx+4]` (`007F38AD`..`007F38C4`).

`007F3800`, second replacement. Replace

> splits `r8d` minus dword `+0` by signed division into a quotient by dword `+0x2C` (added to word `+8`), the remainder's quotient by dword `+0x28` (added to byte `+0xA`) and the rest's quotient by dword `+0x24` (added to byte `+0xB`)

with

> divides `d` = `r8d` minus dword `+0` (signed `idiv`) by dword `+0x2C` (the quotient's low word added to word `+8`), then divides `d` minus the sign-extended low word of that quotient times `+0x2C` by dword `+0x28` (low byte added to byte `+0xA`), then divides that value minus the sign-extended low byte of the second quotient times `+0x28` by dword `+0x24` (low byte added to byte `+0xB`)

Why: the dividends are rebuilt from `movsx r8d, ax` (`007F384B`) and `movsx eax, al` (`007F3863`), not from `edx` (the true remainder). The two agree only while each quotient fits its width.

Limits: these are body statements read from static evidence. The draft and OPUS's re-read are not independent review; this record is.
