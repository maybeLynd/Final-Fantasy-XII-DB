# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-sound-variant-selection-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SOUND-VARIANT-SELECTION-EE-1003` · Package: `_index/candidates/opus-sound-variant-selection-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `18-Audio/Sound-Selection/sound-variant-selection.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 7 rows were checked clause by clause against the bytes; the package has fewer than 15 rows. Every computation, offset, width, branch condition, call target and return value is correct. One wording defect affects three rows (`007CF780`, `007CFE60`, `007D0710`). They say the body writes "the qword `01CB6E80`" (or `01CB6E10`) when it writes that **address** (a `lea`). The same rows, and row `007B0E90`, use "qword `<address>`" to mean the memory at that address, so read the same way these three describe the wrong value. The exact replacements are below. No anchor changes.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify only).** `interior_applier.py` without `--apply` verifies and writes nothing (source lines 99-110). Run under the analysis venv with `-B`: `VERIFY 7 functions, 35 anchors` / `ALREADY` / `FAILS 0`, identical to the committed `.out`.
- **Live page.** Each of the 7 functions has exactly one row in the page's interior table (lines 738-744). The row text equals `rows.json` `text` byte for byte, and all of its anchors appear in the row. The size column matches the extents (0xF9, 0xEC, 0x8E, 0xD1, 0x8E, 0xDE, 0xE3).
- **Anchors.** All 35 are instruction boundaries inside their function with the recorded mnemonic (independent `disr.py` decode). Each lies on the clause it supports.

| fn | verdict | decisive bytes |
|---|---|---|
| `007B0E90` | exact | `007B0EA3` null `rdx` → -1. `007B0EB3`/`007B0EC5` signed dword `02EAD3EC`, `jle` → -1. `007B0EC7`/`007B0ECE` entries from qword `02EAD3F8`; `q` = entry `+8`, stride 0x40 (`007B0EFD`). String at `q`+word`[q+2]` (`007B0ED5`/`007B0EDA`) compared bytewise (`007B0EE3`..`007B0EF4`). Match: `+0x24` vs 0.0 (`007B0F29`), `+0x1c` stored (`007B0F3B`). Else `007A9E50(+0x20/+0x24, edx=+0x2c)` (`007B0F4A`..`007B0F58`), ×(`+0x1c`−`+0x18`)+`+0x18` (`007B0F5D`..`007B0F6F`), stored at `007B0F7F`. Returns 0. |
| `007CA560` | exact | `[rsp+0x70]` after `push`+`sub 0x40` = entry `rsp+0x28`, the fifth argument (`007CA56A`). Curve branch `007CA590`..`007CA5C6`. Stores at `007CA5CD`..`007CA5EB`. `[rcx+0x24]`==1 at `007CA5D2`/`007CA5EF`. `comiss xmm7,xmm3`/`jbe`: above → (`xmm1`−start)/\|`+0x28`\| (`007CA5F6`..`007CA606`), else (start−`xmm1`)/\|`+0x2c`\| (`007CA617`..`007CA627`); the mask `00D27AA0` = 0x7fffffff. Stored when `comiss xmm8,q`/`jae` is not taken (`007CA610`, `007CA631`). `eax`=0 at `007CA5CB`. |
| `007CF780` | narrowed | Logic exact: `movsxd rcx,r8d` (`007CF787`); `<9`: `007CF792`..`007CF7A5`; 9..10: pad = (`[h+0x23]`+0x10)&0xf0 (`007CF7B7`..`007CF7C5`), offset dword at `h`+`[h+2]`+pad+idx·4, then +pad +`h` (`007CF7CB`..`007CF7D9`); `>=11`: word `[h+0x46]` (`007CF7EE`..`007CF7F6`). `[rdx]` gets `lea rax,[rip→01CB6E80]` (`007CF79E`/`007CF7E0`/`007CF7F9`): the address. The qword stored at `01CB6E80` is `007CF5F0`. |
| `007CFE60` | narrowed | Logic exact: type 0 → `007CFF1B`..`007CFF2A` (pointer 0); type 1 → `+0xa`/byte +6=1 (`007CFE86`..`007CFE92`) or `+0xc`/2 (`007CFE9A`..`007CFEA6`); type 2 → `+0x12`/`+0x14` (`007CFEC1`..`007CFEE1`); other → `js` (`007CFEEC`) and `cmp byte[h+8],r8d`/`jle` (`007CFEF3`/`007CFEF6`), dword table at `h`+`[h+2]` (`007CFEF8`..`007CFF0D`). `[rdx]` gets the `lea` address `01CB6E10` (its qword is `007CF680`). |
| `007D0710` | narrowed | Logic exact: `js` (`007D0719`), `cmp byte[h+0x43],r8d`/`jle` (`007D071F`..`007D0727`) → 0 (`007D0789`..`007D0799`). Pad when `byte[h]` ≥ 9 unsigned (`007D0729`/`jb`) = (`[h+0x48]`+0x10)&0xf0 (`007D072F`..`007D0738`), else 0. Index b4+b5+b41+b42+r8d (`007D0744`..`007D075F`), `movsxd`, dword at `h`+`[h+2]`+idx·4+pad (`007D0770`), +`h`. `[rdx]` gets the `lea` address `01CB6E10`. |
| `007E6620` | exact | vcall `+0xa8` (`007E6643`), `cmp eax,2` (`007E6649`). `007E5DA0(rcx, rsp+0x20)` (`007E6652`..`007E6662`). `t`=`[rcx+0x30]`, byte `+0x18`, `cmp`/`jge` (`007E6667`..`007E6671`). `+0x538`−=`xmm1` stored (`007E6673`..`007E6685`), `ja` skip when > 0. `007E5E80` (`007E669A`). Import `008C3098` called; `cdq`/`idiv` by (`[t+0x14]`−`[t+0x10]`+1); +`[t+0x10]`; `cvtdq2ps`; ×0.001 (`008C5B2C`); stored (`007E669F`..`007E66CB`). All paths: `movaps xmm1,xmm6`, `007BF0A0` (`007E66DB`..`007E66E1`). Cookie `00808C40`. |
| `007E6960` | exact | `01CB8FA0`→`[rcx]` (`007E6960`/`007E6967`), `01CB4D58`→`+0x20` (`007E697F`). Zero stores `007E6973`..`007E69CB` and `007E6A04`/`007E6A07`: every listed offset and width matches. 1.0 dwords at `007E69D1`..`007E69FD` and `007E6A0B`; qwords `+0x44`/`+0x4c` from a sign-extended positive imm32, so zero-extended (`007E69E6`/`007E69EE`). Loop: byte 0xfe at `+0x6c+i`, dwords at `rdx-4`/`rdx` from `rcx+0x74`, stride 8, 4 iterations (`007E6A20`..`007E6A3D`). Returns `rcx`. |

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing (rows.json `text`, and the page rows at lines 740-742).**

- `007CF780`: replace "writes to the output pair at `rdx` the qword `01CB6E80` followed by" with "writes to the output pair at `rdx` the address `01CB6E80` followed by".
- `007CFE60`: replace "writes the qword `01CB6E10` to `[rdx]`" with "writes the address `01CB6E10` to `[rdx]`".
- `007D0710`: replace "writes the qword `01CB6E10` to `[rdx]`" with "writes the address `01CB6E10` to `[rdx]`".

Reason: each body stores the result of `lea r,[rip→X]`, the address itself. Row `007B0E90` ("starting at qword `02EAD3F8`") and these rows' own "qword `[rcx+8]`" use "qword X" for the memory at X, which here holds `007CF5F0` / `007CF680`. Row `007E6960` ("stores `01CB8FA0` to qword `[rcx]`") already uses the correct form.

**Notes (non-blocking):**
- `007E6620`: "below byte `+0x18`" is a signed `jge` test. This is immaterial here: `007E5DA0` returns a non-negative counter (`xor ebp,ebp` at `007E5DAA`, `inc ebp` at `007E5E3D`, `mov eax,ebp` at `007E5E65`).
- "equals 0.0" on the `ucomiss`/`jne` tests (`007B0E90`, `007CA560`) also routes a NaN down the "equals" arm. This is the usual reading, and no correction is asked for.
- README "Missing: 2" (`007BC8D0`, `007CFD00`) is outside this spot-check.
