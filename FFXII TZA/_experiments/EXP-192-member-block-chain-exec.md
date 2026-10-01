# EXP-192 — Member-block chain execution (`31A630` r9d!=0 arm)

**Status:** complete — **116/116 cases, stable across 3 independent runs, zero faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; leaf/system callees intercepted at their real addresses and
disclosed below. Synthetic fixtures disclosed; none claim initialized-gameplay
reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-152/EXP-158 executed `0031A630` (slot writer) real but only ever with
`r9d=0`; the contract flagged the `r9d!=0` member-block chain
`0030F9A0`/`0030C410`/`00324470` as "(r9d!=0 only — never passed)". This
experiment drives `31A630(rcx=rec, edx=slot, r8w=newid, r9d=1)` directly and
runs the entire chain as shipped bytes:

- `0031A630` — `edi=r9d`; `si!=0xFFFF` → `317930` slot-search gate (scripted);
  `edi!=0` → `30F9A0(old w[+0x50+slot*2])` then `30C410(si)`; writes
  `w[+0x50+slot*2]=si`; `318B40` list op (scripted); `w` change → `30FED0(0x97)`
  (scripted); `edi!=0` → `31B860` owner scan → `324470(member)` teardown.
- `0030F9A0` (unequip) / `0030C410` (equip) — `cx==0xFFFF` → -1;
  `(cx&0xF000)!=0x1000` → 0; `cx==0x1000` → 0; else
  `3008A0(cx, edx=-1|+1, r8=0, r9=2, a5=0)` — the EXP-158 id resolver, run real.
- `003008A0` → `309F30(id,2)` → class-1 row `0x1EEBD18` `q[+0x50]` validator
  **`002FD8D0`** (real) → `q[+0x48]` mutator **`002FD150`** (real) → `325F40`
  notify (real). Shipped `d[row+0x3C]=0x1A4` bounds member ids to
  `0x1001..0x11A3` (`0x1000` rejected separately).
- `0031B860` — real scan: `236850` count × `236820(i)` rows (0xF50 stride),
  returns first row whose `q[+0x698]==rec`, else 0.
- `00324470` — member teardown: `2ECF10(q[+0x10], d[mbr]>>0x17&1)`;
  `3105D0(mbr)` (EXP-161's unlink, scripted here — proven by EXP-161);
  `q[mbr+0x698]` nonzero → `(d[rec+0x64]|d[rec+0x3C]) & 0x80000003` **nonzero**
  is required to reach `313F60(rec)`; then ret0 → `b[mbr]&2` clear →
  `300E40(mbr,0)`; finally `2E42D0`/`2699D0`/`2ECEC0` on `q[+0x10]` and
  `or d[mbr],0x40`.

## New executed facts

- `30F9A0`/`30C410` are thin class gates: only `0x1xxx` ids with `cx!=0x1000`
  reach `3008A0`; `edx=-1`/`+1` = decrement/increment of the packed member
  word's **count field** (`w>>0xA`), clamped `[0, w&0x3FF]` by `2FD150`'s
  `r9=2` arm. `2FD8D0` is the matching validator (`edx`=0 free / 1 cap /
  2 count / 3 byte-flag).
- Class-1 row `q[+8]` word table ships as 0 (runtime-allocated) — planted as a
  disclosed fixture. `q[+0x30]` bit-array arm is `r9=1` only; `46A630` fires
  only when the `a5` stack flag is set (0 here).
- `324470` gate polarity verified live: **zero** `(d[+0x64]|d[+0x3C]) &
  0x80000003` skips BOTH `313F60` and `300E40`; nonzero → `313F60` runs and
  ret!=0 skips `300E40`; ret0 → `b[mbr]&2` gate → `300E40(mbr,0)`.
- `31A630` ignores `30F9A0`/`30C410` return values; slot write proceeds.

## Disclosed scripted boundaries (unchanged from EXP-152/158)

`317930`, `318B40`, `30FED0`, `2ECF10`, `3105D0`, `313F60`, `300E40`,
`2E42D0`, `2699D0`, `2ECEC0` — captured via the `calls` log at their real
addresses with full register args. `3008A0`/`309F30`/`2FD8D0`/`2FD150`/
`325F40`/`236850`/`236820`/`31B860` ran real.

## Cases (14 new, `a630r9-*`)

`swap` (full chain, both word updates verified), `off` (r9d=0 control —
nothing runs), `oldff` (`30F9A0` → -1, no resolver), `oldfoe` (class gate),
`new1k` (0x1000 equality gate), `nomatch` (owner scan miss → `324470`
skipped), `bit23` (`2ECF10` edx=1), `gate3f` (`313F60` ret1 → `300E40`
skipped), `b2` (bit2 skip), `rec3c` (OR-gate set → `313F60` ret0 → `300E40`
runs), `null` (rcx=0 → -1), `deny` (`317930` ret0 → -1, no writes),
`newff` (FFFF new id clears slot, unequip still runs), `clamp` (equip clamped
at capacity).
