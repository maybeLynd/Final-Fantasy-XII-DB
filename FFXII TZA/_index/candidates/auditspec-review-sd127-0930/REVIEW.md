# SWE2-AUDIT-SPEC review of SD-127, the battle-HUD key base reads (OPUS, 23a99db40): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `23a99db40`, [README](../sd127-hud-key-base-reads-0930/README.md) and `sd127_keys.py`. Measured at HEAD
`b58c633f7`. Package re-runs repeated at `701f1f01a`, identical. Static analysis of the certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD127-0930 | sd127-hud-key-base-reads-0930 | `23a99db40` | ACCEPT-WITH-NARROWING |

**Re-run.** [rerun_sd127_keys.out](rerun_sd127_keys.out) is identical to the committed `.out` (CR ignored). C1 and
K1-K3 PASS, `FAILS 0`. The package dir was clean after the re-run.

**Re-derived independently.** All three scripts use [sdx.py](../auditspec-review-sd141-0930/sdx.py), not retool.py or
`pe`:
- [sd127_indep.py](sd127_indep.py) / [.out](sd127_indep.out);
- [sd127_leas.py](sd127_leas.py) / [.out](sd127_leas.out);
- [sd127_handon.py](sd127_handon.py) / [.out](sd127_handon.out).

The key set is the package's definition, rebuilt from the same page and TSV: 86 keys, from `01E0C348` to `0209E628`.
- **K1 holds for direct reads.**
  - I checked every operand in `01E0BFC0`..`01E0D0FF`, and within 0x40 below each of the 11 HUD keys outside that
    block (`0209ABFC`..`0209E628`). All forms were covered: rip, image-base-relative with any base/index, and abs32.
  - No non-rip operand covers any HUD key.
  - The 13 relocations into the block (`01E0C158`..`01E0C1C0` -> `01E0C120`..`01E0C144`, and the `01E0C590`
    record's `+8`/`+0x10`/`+0x18`) point at no HUD key. The `.rdata` values that read as rva32 hits (for example
    `008F35E0` = `01E0C390`) are DIR64-relocated absolute pointers to `.rdata` (`01CEC390`), not RVAs.
- **K2 holds.** `001AF470` sits in a `.pdata` gap, `001AF470`..`001B018F`. It holds 227 leas, which install 85 HUD
  keys. The one it misses, `01E0CF94`, is installed by `001B455F`/`001B4566` into `[rbx + 0x300]`. Beside it,
  `01E0CF90` goes to `+0x2F8` and `01DF6DE0` to `+0x308` (`001B456D`).
- **Handed-on bases (the request's R2 concern).** I tracked 94 non-installer lea sites with a linear candidate walk,
  covering the block and 0x400 below each outside key. Every direct callee a base is handed to was followed, plus
  one more level:
  - none of these accesses lands on a key (`key hits … (levels 1-2): 0`);
  - the nearest cases are `0209E608` (+0x10 below `OverHeadStatusOffsetX`), which `00285F00` reads to +6 only, and
    `0209AB90` (+0x6C), which `00203170` / `00217060` read to +0x40;
  - not followed: `00267A79 call [r15 + 0x88]` with `rdx = 01E0C32E` (0x1A below `mScrollListHeight`), and
    `call rax` at `00244EF5` / `00246C09` (bases 0x250 or more below a key);
  - also not followed: third-level hand-ons, chiefly of `0209CB90`, a base that ends exactly at
    `MsgWinLogUpCursorOffset` (`0209CC10`, +0x80). The first two levels read it to +2 only.
  - A reviewer-tool fix, recorded here: my first walk stopped at the end of the entry `.pdata` chunk, which missed
    `004006A0`'s `[r14 + 0x18]`. `sdx.chain_end()` now walks the whole chained function, and all counts here are
    from the fixed run.
- **The indexed image-base-relative reads that R1 cannot see.** Five sit in the block. Three cannot be excluded by
  their code:
  - `00266588` in `00266530` (`[r11 + rax*4 + 0x1cec329]`, `r11 = 00120000`, `rax = byte [rbx + 3] & 0x1f`)
    indexes the 8-entry `01E0C328` table.
  - `00266B83` (`.pdata` gap `00266ACF`..`00266C4F`, `r9 = 00120000` at `00266AE7`, `rax = rcx & 0x1f`) indexes
    the same table.

    Both code bounds are 32 entries, so indices 8..31 would read HUD-key bytes up to `01E0C3A5`. K3 names only
    `002679F0` as this table's walker.
  - `002AECA3` / `002AEE26` in `002AEB20` index the byte tables `01E0CE30` / `01E0CE10`. The index is a text byte
    − 0x40. It is either kept below 0x20, or passed through `002AB8F0`, which returns it unchanged outside
    0x20..0x2B (`002AB9DC`). So the code does not bound it below the 0x64 / 0x84 distance to `TargetInfoMoveY`
    (`01E0CE94`).

  The other two are bounded:
  - `0027E122` is reached only by ids 16..19 of `0027E050`'s table (`0027E384`). Its index is 0..3, which stops
    before `01E0C3B0`.
  - The `0209E610` read at `002BDB3B` is bounded 0..4.

**Controls.**

| instrument | control | result |
|---|---|---|
| image-base-relative | K1: SD-121's `0036E414` | found |
| scale-1 base+index | K2: `002AECA3`, `002AEE26` | decoded and flagged indexed |
| the lea census | K3: `004001D0`'s lea of `01E0C590` | found |
| DIR64 | K4: `01F2E330` | found |
| the hand-on follower | T1 / T2: SD-141's `00608999` hand-on and `004001D0` -> `004006A0` | both reported |

**Defects in the package's gates.**
- **C1's R1 control does not test R1.** It checks that the string `0x21b97b0]` occurs in `0036E3B0`'s disassembly,
  not that R1's regex matched it.
- **R1's regex misses operand forms.** It needs a base register and a `*scale` index, so it cannot match scale-1
  base+index or index-only operands. Two such operands occur in the block.
- **R1 counts displacements too narrowly.** It accepts only displacements 0..3 below a key, so an array read that can
  run onto a key is not an R1 hit.
- **R2 sweeps too little.** It covers `01E0C000`..`01E0D100` only, and 11 of the 86 keys lie outside that range.

**Citations checked.** These decode as the README states (`sdx.txt`):
- K3's record reads at `004006DB`, `0040070A`, `00401884`, `0040190A`, `00401D8C`, `00401E33`;
- the table bytes `0,1,1,2,2,3,3,3`;
- `mScrollListHeight` = `01E0C348`.

Three qword rip loads each cover two keys: `0027AE78`, `0027D000` and `002C8743`. That is outside SD-127, which asks
about base pointers, and is noted for the page's rip census.

**Correction wording** (the producer applies).
- **K1 becomes:**

  > No battle-HUD key is read by an image-base-relative operand at its own displacement, by a stored pointer, or
  > through a block lea followed in its function and two callees deep, apart from the indirect calls `00267A79`
  > (`[r15 + 0x88]`, `rdx = 01E0C32E`) and `00244EF5` / `00246C09` (`call rax`), which are not resolved.
  >
  > Indexed table reads next to the keys are not excluded by code:
  > - `00266530` (`00266588`) and the code at `00266B83` index the 8-entry `01E0C328` table with a 5-bit field, so
  >   entries 8..31 would read HUD-key bytes up to `01E0C3A5`;
  > - `002AEB20` (`002AECA3`, `002AEE26`) indexes the 32-byte tables `01E0CE30` / `01E0CE10` with a text byte − 0x40
  >   that is not bounded below `TargetInfoMoveY` (`01E0CE94`).
  >
  > Whether authored data reaches those indices is not checked.
- **In K3,** add `00266530` and `00266B83` as readers of the `01E0C328` table.
- **The R2 limit becomes:**

  > R2 swept `01E0C000`..`01E0D100`. Outside the console installer, the lea targets within 0x40 below a HUD key are
  > K3's two, `001B44A0`'s two (K2), and, outside the block, `0209E608` (+0x10, read to +6 by `00285F00`) and
  > `0209E610` (+0x8, index 0..4 at `002BDB3B`). Neither reaches a key.
- **The modding line becomes:**

  > No HUD code reaches a key through a copied pointer; the open cases are the indexed table reads above.
