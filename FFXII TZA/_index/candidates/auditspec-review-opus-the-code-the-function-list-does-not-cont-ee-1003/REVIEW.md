# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-code-the-function-list-does-not-cont-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-CODE-THE-FUNCTION-LIST-DOES-NOT-C-6789F` · Package: `_index/candidates/opus-the-code-the-function-list-does-not-cont-ee-1003/` (reviewed at HEAD `e06561376`) · Page: `99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 4 rows. All 4 were read clause by clause against a raw capstone decode of the certified image (SHA256 `73461D08...21F8`), and all 4 are exact.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify-only).** `interior_applier.py` with the venv python printed `VERIFY 4 functions, 20 anchors` / `ALREADY` / `FAILS 0`, exit 0. The page block is the 2026-10-03 heading at line 980, with 4 rows ending at line 989. The page is clean in the working tree.
- **Extents.**
  - `00123F80` has `.pdata` plus a chained fragment `00123FA2`-`00124000`, with its last `ret` at `0012400C`.
  - `0014C221` has no `.pdata`. It starts right after the previous body's `ret` at `0014C220` and ends at `ret` `0014C4E5`, with the next `push rbp` frame at `0014C4E6`.
  - `00172580` is `00172580`-`00172680`.
  - `00349E40` is `00349E40`-`00349ECA`.
  - All 20 anchors are instruction boundaries with the recorded mnemonic.

Per row:

- **`00123F80`**: exact. `00123F90` calls `00123250(rcx)` and `00123F98` calls `001234A0(rsi=rcx)`. Both read `rcx` (`00123258` `[rcx+0x44]`, `001234AA` `[rcx+0x3c]`). `00123F9D`/`00123FA0` take a null `rdx`, and `00124000` returns 0. `00123FAB` is `movsxd rsi,[rcx+4]`, and `jle` skips. Entries are `[rbx+rbp]` = `[rcx+0x58+8i]` (`00123FC0`). `00123FC4`-`00123FCE` stop on a null `[q+0x508]`. `00123FD0`-`00123FD8` skip a null `[p+8i]`, and otherwise call `001243D0(rcx=[q+0x508], rdx=q, r8=[p+8i])`. `001243D0` reads all three (`001243E9`/`001243F0`/`001243FA`). `00123FF3` returns 0.
- **`0014C221`**: exact.
  - **Frame.** An `rbp` frame homes the four argument registers and saves `xmm6`/`xmm7` at `0014C239`/`0014C23E`.
  - **Load and zero.** `0014C256`-`0014C277` load the four rows at `[rcx]` and zero them.
  - **Dequantise.** `pmullw` at `0014C27C`/`0014C285` uses `[rdx]` for `+0`/`+0x20`, and at `0014C280`/`0014C289` uses `[rdx+0x10]` for `+0x10`/`+0x30`.
  - **Two passes.** Each pass is preceded by a `punpck*dq`/`pshufd 0xd8` transpose. The odd terms are `x + pmulhw(x, [03001FD0]=0x8A8C)` and `x + pmulhw(x, [03001FE0]=0x4E7B)` (`0014C2CE`/`0014C2DA`, `0014C2E2`/`0014C2EA`, and again at `0014C39A`-`0014C3DA`).
  - **Rounding.** The second pass adds `[03001FC0]` = word 4 (`0014C3DE`/`0014C3E6`), and `psraw 3` runs at `0014C406`-`0014C415`.
  - **Add and store.** `rdi` = `r8`, `rdx` = `movsxd r9d` (`0014C28E`), `rcx` = 3\*stride. The four `movq` loads at `0014C47A`-`0014C498` are byte-unpacked, added, packed with `packuswb` and stored back (`0014C4BD`-`0014C4CB`). There is no return value.
- **`00172580`**: exact.
  - **Max leaf.** `0017258A` runs `cpuid` 0, and a max leaf below 1 gives `f`=0.
  - **Leaf 1.** `001725A3` runs `cpuid` 1. The `cmove` chain gives edx `0x800000` -> 1 (`shr 0x17; and 1`), edx `0x2000000` -> 2, edx `0x4000000` -> 4, ecx bit 0 -> 8, ecx `0x200` -> 0x10, ecx `0x80000` -> 0x20.
  - **0x40.** `001725FE`-`00172625`: `ecx & 0x18000000 == 0x18000000`, then `xgetbv` with `ecx`=0 and `(dl & 6) == 6`, set 0x40.
  - **0x80.** `00172629`-`0017263B`: max leaf >= 7 (unsigned `jb`), `cpuid` 7 with `ecx` still 0, then `test bl,0x20` and `bts 7`.
  - **Stores.** `00172640`-`00172673` run on every path. `02F974F8` gets `00133B40` if `f & 0x10`, else `00179920`. `02F974F0` gets `00179360` if `f & 0x80`, else `00179320`. There is no return value.
- **`00349E40`**: exact. Three `00267DB0(rbx=r9)` calls at `00349E63`/`00349E6F`/`00349E7A` save `a`=`xmm8`, `b`=`xmm7` and `c`=`xmm6`. I read `00267DB0`: it returns its value in `xmm0`. `00349E8A` calls `0026AD40(rdi=rdx, 1)`, and `0026AD40` reads `dl` (`0026AD53`). `00349E8F`-`00349EAA`: `[rsp+0x20]` = `[01CEBBA8]` = f32 1.0, `xmm1`=c, `xmm2`=b, `xmm3`=a, then the call to `0026A420`. Its result is passed through untouched. `0026A420` tail-jumps to `002E5B00` when `(byte [rcx+3] & 0xE0) == 0x60`. That target reads `xmm1`-`xmm3` and `[rsp+0x28]`, the fifth-argument slot (`002E5B2B`-`002E5B54`), so the stated arguments are consumed.

**4 of 4 exact.** All 20 anchors were checked.

## SWE2-AUDIT-SPEC limits

- I checked body statements against the bytes. Two labels were matched by shape, not proven by provenance: "libvpx two-block dequantise, inverse-DCT and add", and the CPU-feature bit names.
- `00267DB0`, `0026AD40` and `0026A420` were read only as far as the row's argument and return claims. The same goes for the `001243D0` argument reads. The four dispatch targets stored by `00172580` were not reviewed.
