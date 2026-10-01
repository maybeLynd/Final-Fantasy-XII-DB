# EXP-233 — node teardown `2EB0D0` + `269D60` + `427xxx` flag writers real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `875e09ae` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..232; no new cases — the `kb0d0` scripted sink now
executes the shipped body; `k99b0-kick`'s `0xDEAD` sentinel node
replaced by a real `objc0` buffer; asserts retargeted to real tags +
shipped-write pins).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

The `2EB430` family's node teardown — `kb0d0` was the ×26 scripted
sink the object-release chain feeds. Signature
`(rcx=ent, rdx=node, r8d=msg, r9d=arm, stack: -1.0)`:

| body | semantics | hits |
|------|-----------|------|
| `002EB0D0` (`l2eb0d0`) | `rdx` null → ret (24 of 26 calls); `d[node]==-1` → bail. Live node: `269D60(node,0,0)` flag fold → `b[+0x11]&0x10` → `2EDCC0(w[node],bit)` [gated off] → `b[+0x11]&=0xEF` → ecarr arm: `row = q[0x22C6F28] + w[node]*0x740`, `d[row+0x284]!=0` → `427320(row,msg)` [scripted] → `d[+0x14]`==0.0 → set -1.0 → `w[+0x2A]` sign dispatch `427880`/`4272C0`/`4278B0` [−,≥0-lower,≥0-upper] → reset writes (`d[+0x14/18/1C]`=-1.0, `w[+0x2A]`=FFFF) → `r9!=0` arm `427860(row)` else float-gated `4270A0`/`4272E0` → tail `4272A0(row,(b[+0x11]>>3)&1)` → `b[+0x11]&8` → `314D30` [gated off] → `b[+0x11]&=0xF7`. | ×26 |
| `00269D60` (`l269d60`) | flag leaf: `b[+0x29] = (b & 0xFC) \| (edx!=0) \| (r8!=0)*2`. | ×2 |
| `004278B0` (`l4278b0`) | `d[+0x294] \|= 0x400000; d[+0x3C4] = edx`. | ×1 |
| `00427860` (`l427860`) | `d[+0x294] &= 0xFFFDFADF \|= 0x80`. | ×1 |
| `004272A0` (`l4272a0`) | `d[+0x294] \|= 0x1000; w[+0x3B6] = dx`. | ×1 |

## `427320` — the disclosed scripted boundary (`v427320`, ×1)

`00427320`(row, edi=msgid) is the heavyweight equipment/visual-set
applier: `3E55F0(row)`/`3E7D10(d[row+0x6A4],3)` gate, `edi`-switch
jump table (`0xF000`/`0x2005`/`0x2006` arms + `(edi>>12)&0xF`
dispatch into `422DE0`/`2ED570`/`20E600`/`3E1610`/`420890`/`423790`/
`3DD740`/`20E620`/`423230`/`423170`/`3DC7D0` subtree). Fires once
real-reachable on `u43f0-ec` as `v427320(elem2, 0x1001)` — recorded,
not executed. Needs the visual-set ctx classified before promotion.

## Fixture correction

`k99b0-kick` carried `ent_q={0xC0: 0xDEAD}` — a sentinel that proved
the scripted call got the pointer. Real `2EB0D0` would deref it and
fault at `0x2EB0E8`; swapped to `objc0={}` (the existing
`q[objent+0xC0]` link-object fixture — `self.objc0` now stashed for
asserts). The zeroed node exercises the full non-ecarr path: `w`=0 →
all row gates `je`-out on the null `q[0x22C6F28]` base (0*0x740+0).

## Shipped-value pins added

`k99b0-kick`: node `d[+0x14/18/1C]`=-1.0 (`0xBF800000`), `w[+0x2A]`=
FFFF, `b[+0x11]`=0, `b[+0x29]`=0. `u43f0-ec`: elem2 `d[+0x294]`=
**0x401080** (the real `4278B0`→`427860`→`4272A0` fold),
`w[+0x3B6]`=0, `d[+0x3C4]`=0, `v427320(elem2, 0x1001)` recorded,
c0-node reset writes.

## Corrections of record

Assert retargets only: three `by("kb0d0")` sites → `byr("l2eb0d0")`
(`k99b0-low` absence, `k99b0-kick` args rdx `0xDEAD`→`w.objc0`,
`u0fc0-def` args). Zero regression failures.

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `290B90` (`s290b90` ×34), `317E50` (`b7e50`
×0), `20CE60` (`v20ce60` ×0), `427320` (`v427320` ×1 — new),
`319490`, `2E42D0`, `46AB10`, `426130` remain scripted.
`2EDCC0`/`314D30`/`427880`/`4272C0`/`4270A0`/`4272E0` unlisted
(gated arms, never reached under fixtures). `live_game: false`.

## Regression triage

**542/542 first run — zero regressions.** 24 of 26 calls are `rdx=0`
early-outs (observably identical to the stub); the two live-node
paths (`k99b0-kick` new fixture, `u43f0-ec` pre-existing `objc0` +
`ecarr`) execute deeper shipped code and their writes are now pinned.
