---
id: EXP-157
title: "Stat apply 300530 — delta commit + engaged-bit protocol"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp157_check.py
result: 86/86 (stable x3)
---

# EXP-157 — `300530` stat apply, executed

`00300530` is the body `30F340` calls as `300530(rec, computed-stored, 0,
0x217)` when a recomputed stat differs from the stored value. 222 insns,
ends `0x30089F` — the `0x3008A0` entity-id resolver that follows is a
separate sibling (own package).

## Signature and core

`300530(rec, delta=edx, arg3=r8, notify=r9)`:

```
old  = d[rec+0x48]
new  = clamp(old + delta,
             owner ? d[ownerrow+0x48] : 0,          # floor
             cap)                                    # ceiling
cap  = (d64|d3C) & 0x10000 ? max(old,1)
     : d[rec+0x24] * (flag bit 0x1C ? 2 : 1)
d[rec+0x48] = new     # unless vetoed (below)
```

`arg2` is a **delta onto `d[+0x48]`**, not an absolute value — discovered by
execution (a zeroed fixture clamps every delta to 0 via cap `d[+0x24]`).

## Veto and notify vocabulary

- `notify & 1` → skips the `30B8E0` veto entirely (direct write).
- veto consulted only when `notify&1==0 && r12<=0`
  (`r12 = delta>0`, or `notify>>5&1` when delta==0). Proven: `kb8e0=1` →
  `d48` unchanged.
- `~(notify>>4)&1` → `3283D0` owner msg; `~(notify>>7)&1` → `28F1F0`
  gauge event (both need owner row).
- `notify&4` && `!(notify&0x40)` && owner → `3299B0(row, r13+0x2005, rbp[8])`
  stat message on the mid path.

## Engaged-bit protocol (executed)

After the write, `30E360` toggles `d[rec+0x64]` bit 0 — the engaged flag
(the `0x80000003` mask from EXP-154):

- `delta > 0 && old d48 <= 0` → `e360(rec, arg3, bit0, 0, 0, notify, arm0)`
  — **clear** (revive: stat rose off the floor).
- `delta <= 0 && new d48 <= floor` → `e360(rec, arg3, bit0, -1, -1, notify,
  arm3)` — **set** (floored: r9=-1 routes through the `387730` resolver).
- Otherwise no `e360` — the `3299B0` notify path only.

Proven: `s530-floor` (10−50→0) sets `d64|=1`; `s530-revive` (0→5) fires
arm0; `s530-pos`/`s530-zero` with d48 10→15/10 run no `e360`.

## Real layer added

`300530` itself; leaves `316D70` (15i, per-object lookup returning index
into `d[rbp+idx*8+0x788]` bits), `32A150` (2i), `306F00` (41i →
`263D30`/`2360D0` leaves), `469BB0` (21i → scripted `2FA390`/`46AB10`).
`30B9B0`/`30B8E0` veto pair stay scripted (disclosed).

## Rewritten EXP-153 asserts

`f340-delta`: computed 7, stored 0 → `300530(+7)` → `d48=7`.
`f340-bit1c`: computed 14 → `d48=14` (cap 14 = `d24`×2 via flag `0x1C`).
`f340-bit10`: computed `max(-5,1)=1` vs stored −5 → `d48=1`; unlink path
(`b860` scan + `u43f0` scripted) still verified.

## Boundary disclosure

All fixture recs/owner rows planted; `30B9B0`/`30B8E0` return values are
scripted (their bodies not yet promoted). MODEL-PROVEN evidence only —
no initialized-gameplay claim.
