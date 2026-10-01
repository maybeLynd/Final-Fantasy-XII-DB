# Review `OPUS-REQ-AUDITSPEC-REVIEW-BATCH9-0929`: verdict ACCEPT-WITH-NARROWING (CON-198's third exit is not PFXAA's)

Reviewer: SWE2-AUDIT-SPEC (non-author; producer OPUS). This lane was run by the FABLE session's executor `73162e75`
on 2026-09-29.

Reviewed: DA batch 9, ten falsification passes with corrections CON-191..202. The commits are `b05d44b1d`,
`a3ec641b0`, `145617b53`, `35321544f`, `37addad16`, `ae33c5f3e`, `4ecc48c4c` and `5e5fee584`. None of these was
authored or directed by FABLE. The GF/W/EA register rows that CON-198 routes to FABLE are not reviewed here. Image
`73461D08…21F8`, static.

## 1. All eight instruments re-run

Every output is identical to the committed `.out` and prints FAILS 0 (`rerun_summary.txt`).
`falsify_settings_commands.*` were checked equal to their HEAD blobs first, because a peer's index shows them
staged-deleted. That staged deletion is left untouched.

## 2. CON-198: the core holds, but the closure's attribution does not

**Core, re-derived (`con198_core.out`):**

- `0018CFCE lea rcx, [rbx+0x378]` / `0018CFD5 call 00645DB0`.
- `00645DB0` calls the base `006461B0`, zeroes `+0x50..+0x68`, and stamps `00D625D0` (PFXAA) at `00645DD7`.
- `00191DA0` requires `+0x3E8` and `+0x3E9`. A non-zero `+0x4A3` tail-calls the SMAA path `001925D0`. A zero
  `+0x4A3` calls `0065A630` (a `jmp 0065A640`) on `rcx + 0x378`.
- So with post-AA on and SMAA not chosen, the frame runs PFXAA's worker, **not "a plain copy"**. That half of the
  request's question holds.

**The P7 closure, attacked (`p7_attack.py/.out`, which re-executes the falsifier and reuses its own sets):**

- The direct-call upward closure of the 66 stamping bodies (92 in-band bodies) does leave the band at exactly the
  three stated sites.
- **What each exit is:**
  - `0018CFD5 → 00645DB0`: the **construction**. Below it are PFXAA and PPostEffectBase.
  - `0018D0D0 → 00646770`: `0018D0D0` is a `jmp`, reached only from `008965FA`. That is an **exception-unwind
    funclet**, `008965EC: mov rcx, [rdx+0x40]; add rcx, 0x378; jmp 0018D0D0`: the context constructor's cleanup of its
    `+0x378` member. `00646770` stamps PFXAABase and then PPostEffectBase. **This one is PFXAA's.**
  - `0089E870 → 00646AB0`: `0089E870` is `mov rcx, [rdx+0x40]; jmp 00646AB0`, with no direct caller. Its one
    reference is `01DACB14`, inside the MSVC unwind map `{-1, 0089E870}` whose IP-to-state entries
    (`006458A0`/`006458C6`/`00645BAD`) belong to the `.pdata` entry **`006458A0-00645BC0`** (unwind info `01DACAF8`).
    `006458A0` stamps **PDeferredLightingBase**. So this exit is **PDeferredLightingBase's installer's own exception
    cleanup**, destroying its PPostEffectBase subobject (`00646AB0` stamps only PPostEffectBase). **It is not PFXAA's.**
    It counts as an exit only because MSVC places funclets outside the band.
- The non-direct references to closure bodies from outside the band total 198. After classification (section D of
  the output): 36 are slots in the family's own vtables; 81 are inside unwind info; 35 are the per-class `.rdata`
  method-table triples `{0062F080, <installer>, 0063FC60}` (the reflection construct / destroy hooks, which the page's
  own factory-slot section already accounts for); and 46 are coincidences of `00640900`'s rva32 value inside data
  records (44 in `.rdata`, 2 unaligned in `.data`). **No second construction route by call exists.**

**Narrowed wording (OPUS applies it).** Change both the page (`the-phyre-post-effect-class-family.md`, the CON-198
note: "all three are this `PFXAA` (its constructor and two destructor paths)"; §P7 row: "all three are `PFXAA`'s")
and the CON-198 row to:

> Following every vtable-stamping body's direct callers out of the family's code band finds exactly three exits.
> One is a construction: `0018CFD5` → `00645DB0`, the PFXAA at `context + 0x378`. The other two are
> exception-unwind funclets, not constructions:
> - `008965EC`: the context constructor's cleanup of that member (→ `0018D0D0` → `00646770`, the PFXAABase
>   destructor chain);
> - `0089E870`: the cleanup funclet of PDeferredLightingBase's installer `006458A0`, whose unwind map is at
>   `01DACB10` (→ `00646AB0`, PPostEffectBase).

The conclusion is unchanged: **the only construction by code is the one PFXAA.** P7 asserts only the exits' shapes,
so its docstring claim "all three are PFXAA's" is untested. The regression should assert each funclet's owner.

## 3. The other corrections, re-derived independently

| row | check | result |
|---|---|---|
| **CON-195** (`con195_197_202.out`) | every edge of `0017D000 → 0017D4C0 → 0022A0B0 → 003325C0 → 003325D0 → 0041E3A0 → 00409F80 (0041E40B) → 0040A230 (00409F84)` is in the raw rel32 index | holds. `003325C0` is a leaf thunk with no `.pdata` entry (`lea rcx, [022C6F30]; jmp 003325D0`, called from `0022A401`), so my root-lookup FAIL on that edge is the instrument, not the chain |
| **CON-196** (`con191_196_sample.out`) | all **144** rip `lea` targets in `0040A230` | each is an `.rdata` `PS2Data … obj_finish … .cm` string, matching CON-195's 144 seeded paths |
| **CON-197** | `005FD050` | a thread-safe local-static initialiser (`_Init_thread_header` `008092FC` / construct `00615840` / `atexit` / footer). Both exits return `02CC0410` (`005FD0BF mov rax, rbx` with `rbx = 02CC0410`, and `005FD0C4 lea rax, [02CC0410]`) |
| **CON-192** | the table `00582020`, indexed by state − 1 (`00581DE3 dec r8d`, `00581DFA`) | states 1..8 → `00581E06`, `…E46`, `…E76`, `…E9E` ×3, `00581EB0`, `00581FA8`, as stated |
| **CON-193** | template bytes `35 00 00 00 00 04 62 00` | dword1 `0x00620400`, bits 10, 17, 21, 22 |
| **CON-194** | `002DDD70` | a non-zero word `0215E6DC` returns its bit 0; otherwise it returns NOT bit 12 of `*(0215E6E0)` |
| **CON-202** | raw callers of `00249320` | `0039342C`, `00394048`, `003F492D`, `00404107`, rooted in `003933F0`, `00393FF0`, `003F4840`, `00404060`. No call from `003939B0`. This agrees with this lane's OV-31 review |

CON-199..201 are reproduced by P2, P10 and P12 in the re-run and were not otherwise re-derived. The four surviving
pages (navigation mesh, amap / gmap / menuquest, nonempty PRF) were checked by re-running their falsifiers only.

## Verdict: **ACCEPT-WITH-NARROWING**

All twelve corrections stand as corrections. The one narrowing is CON-198's closure attribution, with the exact
wording in §2. Nothing here routes to ASTRA.

## Files

`p7_attack.py/.out`, `p7_exits.out`, `p7_triples.out`, `con198_core.out`, `con195_197_202.py/.out`,
`con191_196_sample.py/.out` and `rerun_summary.txt`. The loader and disassembler come from the OV-31 and batch-8
review folders, and the `.pdata` root from `../auditspec-review-ddres-b1-0930/disp_4a2.py`.
