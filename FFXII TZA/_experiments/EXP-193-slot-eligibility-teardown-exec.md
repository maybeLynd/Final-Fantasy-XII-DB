# EXP-193 — Slot-eligibility, pair-rebalance, teardown/trampoline execution

**Status:** complete — **156/156 cases, stable across 3 independent runs, zero
unexpected faults** (one disclosed expected fault: `l8b40-nomemt` @`318BE0`
on a null descriptor).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; leaf/system callees intercepted at their real addresses and
disclosed below. Synthetic fixtures disclosed; none claim initialized-gameplay
reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
the EXP-192 driver; 116 inherited + 40 new `g7930-*`/`l8b40-*`/`u43f0-*`/
`w4450-*`/`r71d0`/`g8010-*`/`o4100-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

Executes the small scripted boundaries remaining in the battle-unit
construction contract, all as shipped bytes:

- `00317930` — slot eligibility/search (gates `31A630`'s `r9d!=0` chain).
- `00318B40` — slot-pair/list reconciliation after a slot write.
- `003243F0` — unlink+teardown body; `00324450` — its `0x40`-gated wrapper.
- `00308010` — `b[rec+5]` dispatch predicate (`308130` vs `308040` arm).
- `00324100` — `324020` + licence-bit max-scan returning `308FF0`-computed.
- `003271D0` — global status-byte accessor `b[0x02EBF190+0x5AA4]`.

## New executed facts

### `00317930` — slot eligibility predicate

- `r8` slot index must be `0..4` (slot 5 → ret 0).
- Shortcut table `w[0x00D107E8 + slot*2]` = `[0x1000,FFFF,FFFF,FFFF,FFFF]` —
  slot 0 accepts `0x1000` (empty-member sentinel) and slots 1–4 accept
  `0xFFFF` (clear) **before** the `322C50` range check; `0xFFFF` on any other
  slot → ret 0.
- `r8d` is **zeroed** at `31798B`, so `322C50(6, id)` — kind 6 always, not
  slot+6. Kind 6 validates `id` against the member-table descriptor
  `q[0x02EBF0F8]` range `0x1000..0x1000+d[+4]`; `0x3xxx` ids → 0. A null
  descriptor fails the range check first (ret 0 — no fault path reachable).
- If the caller's `d[rsp+0x60]` flag is set, `309EC0(id,0)` runs real →
  `q[row+0x50]` = `2FD8D0` mode-0 free-count; zero free → ret 0, nonzero →
  continue.
- Member row resolve: `20E600(d[memt+0xC]) + w[memt+8]*(id-0x1000)`. Gate:
  `b[row+7]>>5` must equal the slot tag `esi`.
- `esi==1` sub-check: compares `b[row+9]` to slot-0's row `b[+0x11]`
  (mismatch → 0).
- `esi!=1`, `rec` nonnull: `b[rec+5]!=0` short-circuits ret 1 **before** the
  foe test; otherwise `bt d[foerow], b[row+9]` — bit set → ret 0.
- Final `323C60(rec, id)` — **nonzero = allow** (verified: stub ret 0 →
  `jne` not taken → ret 0; ret 1 → `eax=1`).

### `00318B40` — pair reconciliation

- `rcx` = word array (`w[+0x50]` slot pairs), `edx` = written slot, `r8` =
  update flag.
- `w0==FFFF` → reset to `0x1000` before reconcile.
- Tag match (`b[row+7]>>5` equal on both slots) → no un/equip calls.
- Mismatch/`0xFFFF` partner → `30F9A0`/`30C410` (real) per displaced id, i.e.
  the EXP-192 chain: class gate → `3008A0` → `309F30` → `2FD8D0`/`2FD150`
  (all real). `0x1000` ids skip the resolver (gate `cx==0x1000` → 0).
- `r8=0` → pure reconcile, no equip/unequip calls.
- Null `q[0x02EBF0F8]` descriptor → expected fault at `318BE0` reading
  `d[0+4]`-equivalent — disclosed.

### `003243F0` / `00324450`

- `3243F0` = `3105D0(mbr)` then the full `324470` teardown tail:
  `2ECF10(q[+0x10], d[mbr]>>0x17&1)` → `q[mbr+0x698]` nonzero →
  `(d[rec+0x64]|d[rec+0x3C]) & 0x80000003` nonzero required for `313F60(rec)`;
  ret0 → `b[mbr]&2` clear → `300E40(mbr,0)`; `2E42D0`/`2699D0`/`2ECEC0` on
  `q[+0x10]`; `or d[mbr],0x40`.
- `324450`: `b[mbr]&0x40` gate — set → `3243F0` (run real via `realx`) then
  clear; clear → no-op.

### `00308010` / `00324100` / `003271D0`

- `308010`: `b[rec+5]==0` → `308130(rec)`; else → `308040(rec)` (verified
  null-698/null-rec variants land the `308040` arm).
- `324100`: null `rcx` → 0; else `324020(rec)` (ret 3 in fixture) +
  13-iteration scan over `b[rec+0x194+(edi>>3)]` bit `edi&7`, tracking max
  set index → `a308ff0(abilrow, w[row+8])` when bits set; returns 3/7/9 per
  licence bitmap fixture.
- `3271D0`: returns `b[0x02EBF190+0x5AA4]` (0x5A fixture → 0x5A).

## Disclosed scripted boundaries

`00323C60` (final eligibility — ret stubbed both ways), `00308130`/`00308040`,
`00308FF0` (`ret` 3/7/9 per case), `00324020` (ret 3 base), `0030FED0`,
`003105D0`/`002ECF10`/`00313F60`/`00300E40`/`002E42D0`/`002699D0`/`002ECEC0`
(inside `3243F0` — `3105D0` proven by EXP-161). All captured in the `calls`
log with full register args.

## Cases (40 new)

`g7930-*` (14): `t0sent`/`clr`/`clr0`/`slot5` (shortcut/range gates), `ok`,
`tagmm`, `k8rng` (0x3010 out-of-range), `free0`/`free1` (`309EC0`+`2FD8D0`
real), `s1eq`/`s1ne` (slot-1 tag compare), `foebit`, `b5` (short-circuit),
`c60` (`323C60` deny), `nomemt` (null desc → `322C50` range fail).
`l8b40-*` (8): `ffinit`, `match`, `s0clr`, `s1reset`, `s1tag12`, `s1clr`,
`noflag`, `nomemt` (expected fault @`318BE0`).
`u43f0-*` (5): `gate0`, `698z`, `3f`, `3fskip`, `b2`.
`w4450-*` (2): `set`/`clear` (0x40 gate + real `3243F0`).
`r71d0` (1). `g8010-*` (4): `b5z`, `b5nz`, `698z`, `null`.
`o4100-*` (5): `null`, `base`, `lic`, `liclow`, `noabil`.
