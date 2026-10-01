# EXP-237 — `b[+3]&0xE0==0x60` gate pair `2E9780` + `26D6F0` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `a136ab9a` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..236; no new cases — the `b9780`/`b6f0` scripted
sinks now execute the shipped bodies; asserts retargeted to real
tags).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

`002E9780` (`l2e9780`, ×8) — the entity-flag probe every `300FC0`
teardown tail calls once per u0fc0 case with `(rcx=ent, edx=1)`:

```text
if b[rcx+3] & 0xE0 != 0x60:      ret 0
node = q[rcx+0xC0];  if !node:   ret 0
ret (b[node+0x11] >> 6) & 1
```

`0026D6F0` (`l26d6f0`, ×8) — the float/param update sibling, same
gate, called with `(rcx=ent, xmm1=param, r8d=mode)`:

```text
if b[rcx+3] & 0xE0 != 0x60:      ret            ; pure early-out
desc = q[rcx+0xB8];  f[q[desc+0xF0]+0x24] = xmm1
if mode==1 and f[desc+0xD0] != xmm1:            b[rcx+0xC] |= 0x10
f[desc+0xD0] = xmm1
if q[rcx+0xC0] and q[node+0x138]:
    f[rcx2+0x30+0x98] = xmm1 * const * const * const
flags = 2E9BB0(rcx) & ~4                        ; still scripted b9bb0
if b[rcx+0x12] <= 3:
    if xmm1 == 0.0:   flags |= 4
    else:
        if rcx == (3590D0() ? 3588B0(eax) : 0): flags |= 0x400
        if mode == 1:                           flags &= ~8
2EC5B0(rcx, flags)                              ; still scripted bc5b0
ret                                             ; no retkey
```

## Why the whole package is the early-out arm

All eight calls sit in the `u0fc0-*` family on `ent` = `w.objent` —
the `0x400`-byte entity buffer `objlink` allocates and only
`ent_b`/`ent_q` keys fill. None of the u0fc0 cases plant `ent_b`, so
`b[ent+3]`=0 → `&0xE0`≠`0x60` → both bodies take the gate-fail
branch on every call: `2E9780` returns 0 (matches the never-planted
`b9780_ret` default), `26D6F0` restores regs and returns (no
retkey). Observable behavior identical to the stubs; what changed
is that the *shipped gate* now decides, so a future fixture that
plants `b[ent+3]=0x60..0x7F` exercises the real pass arm — whose
`2E9BB0`/`2EC5B0` callees stay scripted (`b9bb0`/`bc5b0`, both ×0)
and would surface as boundary records rather than unmapped writes.

## Shipped-value pins

`byr("l2e9780")` ×1 and `byr("l26d6f0")` ×1 on `u0fc0-def`, rcx ==
`ent` each — the only case asserting them. The other seven u0fc0
cases exercise the same real gate without pins (calls-only
coverage). No counter/write pins: the early-out writes nothing.

## Corrections of record

Assert retargets only: `by("b9780")` → `byr("l2e9780")`,
`by("b6f0")` → `byr("l26d6f0")` (one site each, `u0fc0-def`).
`b9780_ret`/`s39bad0_ret`-style keys untouched — no case plants
`b9780_ret`. Zero regression failures — **542/542 first run**.
Census: `l2e9780` ×8, `l26d6f0` ×8, stale `b9780`/`b6f0` 0,
`b9bb0`/`bc5b0` ×0 disclosed.

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `290B90` (`s290b90` ×34), `317E50` (`b7e50`
×0), `20CE60` (`v20ce60` ×0), `427320` (`v427320` ×1), `422C20`
(`v422c20` ×1), `3377C0` (`v3377c0` ×19), `28EF70`/`28EF00` (×1/×0),
`2E9BB0`/`2EC5B0` (this pair's pass-arm callees, ×0), `3B02A0`,
`46AB10`, `210EC0`, `1CCB20`, `39BAD0`, `3180F0`, `319CA0`,
`426130` remain scripted. `live_game: false`.
