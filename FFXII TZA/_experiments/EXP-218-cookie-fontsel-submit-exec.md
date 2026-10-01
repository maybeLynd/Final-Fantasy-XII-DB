# EXP-218 — cookie leaf, font-record select, `?`-arm quad submitter, ctx soft-reset

**Status:** complete — **525/525 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`bb2d38d23d244cb8995e20ed51c8883a9de6c255c929be8a73ecc4c725c8d416`),
zero unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..217; 525 inherited cases, none new — promotion round)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

| body | semantics |
|------|-----------|
| `00808C40` | `__security_check_cookie`: `cmp rcx, q[0x1F44830]` → `rol rcx,0x10` → `test cx,0xFFFF` → `ret`; mismatch → `809654` report path. The image's own cookie global satisfies the check — the failure path is never taken, now verified as real code on every cookie-protected exit (fires inside real `20E600`/`2AC5F0`/`2AFDC0` epilogues). |
| `0039C4A0` | font-record select (7 insns): `ecx==0` → `q[0x2AEE800]`; `ecx!=0` → `q[0x2AEE808]`, falling back to `q[0x2AEE800]` when null. Both globals fixture-planted with the resolved `s39c4a0_ret` so existing callers observe the identical record. |
| `002B1ED0` | ctx metric soft-reset (19 insns): `d[rcx+0x44]&0x800` selects the method pair — set: `17F980()`→`f[0209CC70]`, `17F960()`→`f[0209CC74]`; clear: `17F8A0()`/`17F880()` into the **same** two cells. The three unmapped sources are new float-returning scripted stubs (`f980v`/`f960v`/`f8a0v`). |
| `002AFDC0` | `?`-arm quad submitter (~0x4B0 body): builds quad command records into the `q[0209CC50]` publish cursor (`q[+8]=6`/`q[+0x18]=6` headers + RGBA bytes + float coords from `sprt` metrics), flushes via real `2B4730(1)`, then runs the device emit tail. |
| `002DD8B0` | vertex-format leaf (17 insns): `cvtdq2ps` int→float converts, writes corner coords into the vertex block at `rcx` (`rsp+0x70` inside `2AFDC0`'s frame). |

## New scripted boundaries (disclosed emit sinks)

`002DD860`×2 (quad-corner emit), `00181560` (deep emit tail), and the
six device-state wrappers `001819A0`, `00181870`, `00181460`,
`001816B0`, `00181910`, `00181330` — each funnels through the
render-device singleton getter `001B1C00` (`return q[0x1F811E8]`) into
device methods (`1B2410` writes `dev+0x3930`-region state, `1B06D0`,
`1FBD80`). `2AFDC0`'s own `17FC90` glyph-quad call was already scripted.

## Corrections of record

- **Dead assert block since EXP-216:** the assert `elif` chain's
  prefix tuple never listed `b4730-`/`b1fb0-`, so both direct-entry
  cases ran **zero asserts** — vacuous PASS in EXP-216/217. Fixed by
  adding both prefixes; the asserts now execute.
- **EXP-216 slot model was wrong** (unverifiable while the asserts
  were dead): the `2B4730` ebx-tail restores from the **ring-pair
  array itself** — `0x2EBEFC0 + d[0x2EBEFF0]*24`, indexed by the
  just-flipped selector — not `0x2EDF9C0 + d[0x2EDF050]*24`. Real
  post-flush state: `q[0209CC48]` = `&ring_entry` (`0x2EBEFD8` for
  slot1), `q[0209E5A0]`/`q[0209CC50]` reload from that slot's reset
  pair (`ringbuf+0x800`/`+0x10`). The `0x2EDF9C8`/`slotcur` plant was
  dead weight and is removed.
- **Stale-closure bug:** `s3c60-scan`'s `byr("cookie")` assert ran in
  a section that bound `by` but never `byr` — the lambda closed over
  the *previous* case's `rargs`. Bound fresh `rargs`/`byr` there.
- **`2AFDC0`'s emit tail is unconditional** after `s181560`: two
  `2DD860` corner emits → `181560` → `2DD8B0` vertex format → the six
  `181xxx` device ops → `808C40`. First live run faulted on
  `mov [rcx+0x3930]` inside `1B2410` (rcx = the unplanted render-device
  singleton) — resolved by scripting the device-op layer rather than
  fabricating the ~0x3B00-byte device object.
- **`2B1ED0` both arms write the same destinations** —
  `f[0209CC70]`/`f[0209CC74]`; `d44&0x800` selects the source methods,
  not the cells.
- `2AFDC0`'s `2B4730` call passes `ecx=1` unconditionally → the
  ebx-tail restore always runs after the submitter's flush.

## Verified outputs (asserted)

- `c5f0-f3f` (`?` arm): real `2AE450` → real `2AFDC0` → real
  `2B4730`/`3A1DB0`/`36F360` → real `2DD8B0`; record headers
  `q[listcur+0x38]==6`/`q[listcur+0x48]==6`; ring flip `d[02EBEFF0]=1`;
  `q[0209CC48]=0x2EBEFD8`; cursors reload `q[0209CC50]=ringbuf+0x810`;
  all eight emit-tail sinks fire exactly once; sprite metrics
  `f[0209CC60]=128`/`f[0209CC64]=24`/`f[0209CC68]=128`; `b[ctxo+0x10FC]`,
  `b[e312+0xA9]`, `d[aux]`, cursor advance.
- `c5f0-f21` (hi-mode `2B1ED0` reach): `s17f980`/`s17f960` fire;
  `f[0209CC70]=9.0`/`f[0209CC74]=8.0` from planted `f980v`/`f960v`.
- `s3c60-scan`: real `cookie` leaf fires once inside `20E600`'s
  epilogue.
- `b4730-flush`/`b4730-noflip`, `b1fb0-c5`/`b1fb0-dec`: previously dead
  asserts now live and passing (entry tags aren't recorded for
  direct-entry cases — `on_code` skips `addr==self.entry` — entry
  asserts removed in favour of the downstream state checks).

## Still scripted / not claimed

`17FC90`/`17F7C0` glyph emit internals, `2DD860`/`181560` +
`181xxx`/`1Bxxxx` render-device subtree, `2AEB20` catch-all, `17Fxxx`
font shims, `2AC2F0` decoder. No live-game claim — `NATIVE-REPLAY`,
`live_game: false`.

## Verification

`python check.py` → 525/525 pass, zero unexpected faults; three
independent runs → byte-identical `result.json` SHA256
`bb2d38d23d244cb8995e20ed51c8883a9de6c255c929be8a73ecc4c725c8d416`.
