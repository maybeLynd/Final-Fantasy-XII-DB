# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-ppfx-function-identification-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-PPFX-FUNCTION-IDENTIFICATION-EE-1003` · Package: `_index/candidates/opus-ppfx-function-identification-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 3 rows. The request asks for at least 15 rows, so all 3 were checked. Each was checked clause by clause against an independent decode (`disr.py`). Every clause holds, and every anchor is an instruction boundary inside its body with the recorded mnemonic. No row changes.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify-only).** I read the source first: without `--apply` it writes nothing. `interior_applier.py -B` printed `VERIFY 3 functions, 15 anchors` / `ALREADY` / `FAILS 0`, exit 0. The page holds two interior blocks, dated 2026-10-02 and 2026-10-03, so their headings differ. `ALREADY` was matched on the 2026-10-03 block (page lines 746-754), which holds exactly these three rows. The page is clean in the working tree and committed at `HEAD`.
- **Extents.** All listings end in `ret`, with branch targets inside and no jump table.

| fn | verdict | decisive bytes |
|---|---|---|
| `006FE080` | exact | `006FE08D` stores `[+0x500]` first. `006FE080`/`006FE093`: when byte `+0xd09` is zero, it jumps to `006FE14C`, which stores `+0x508` and returns edx. `006FE0A3`/`006FE0A9` store `+0x504` and `+0x50c`. Step rule: `006FE0A0`/`006FE0B5`/`006FE0B7` (equal to `+0x4d0` gives `+0x4d4`), else `006FE0BC`-`006FE0CC` (`inc`, `lea ecx,[rdx-1]; add ecx,[+0x36c]; cmp; cmova r10d`, unsigned). `006FE0D0`/`006FE0D8` `cmp [+0xd10],2; jl` (signed ≥2), then `006FE0DA` store `+0x504` and step. `006FE100`-`006FE11C`: `+0xd0c==2`, qwords `+0xa88` and `+0x148` zero, then `006FE11E` store `+0x50c` and step. That step's equal branch stores `+0x508` and returns at `006FE12D`/`006FE134`; otherwise it falls to `006FE14C`. The `+0x4d0`/`+0x4d4` values are loaded once into `r10d`/`edx`. The function writes only `+0x500..+0x50c`, so no store aliases them. |
| `00724F50` | exact | `00724F54` reads the counter `02EA198C`. Zero skips the modulo (`00724F5E`). The signed remainder comes from magic `0x51eb851f`, `sar 5` plus sign fix-up, and `imul 0x64` (`00724F60`-`00724F78`). `00724F7A` tests remainder 25. `00724F7F`-`00724F8F` `cmp [01F3BA80],1; jb` and `cmp [01F3BA8C],1; jb` (both non-zero). `00724F91`-`00724F9D` call `006DF480(00D9C530, 0x1627)`. `00724FA2`/`00724FA9` call `006DF480(00D9C368)` with edx not reloaded. The counter is incremented on both paths (`00724FAE` `inc [mem]`; `00724FBE`/`00724FC6` store `r8d+1`). Both paths return `0x80004001`. |
| `00724FF0` | exact | The same shape at +0xA0: counter `02EA1990` (`00724FF4`), remainder test `0072501A`, flags `0072501F`-`0072502F`, `006DF480(00D9CA20, 0x16d6)` at `0072503D`, `006DF480(00D9C578)` at `00725049`, increment at `0072504E`/`00725066`, return `0x80004001`. |

**3 of 3 exact.** All 15 anchors were checked.

## SWE2-AUDIT-SPEC narrowing / notes

No narrowing.

Notes (non-blocking):
- The rows agree with the page's own identification table (lines 234-236). Line 0x1627 sits with `00D9C368` "IGPUDevice::ApplyRenderState_DepthFunc() is not supported." and 0x16D6 sits with `00D9C578` "...ApplyRenderState_AlphaFunc() is not supported." (raw `.rdata` reads). The rows cite the addresses only, which is correct for body statements.
