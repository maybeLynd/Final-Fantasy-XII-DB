# EXP-224 — member-block slot accessor tail real (`317930`/`318B40`/`324100`/`323C60`/`3243F0`/`30C650`/`323910`/`308FF0`/`308040`/`308130`)

**Status:** complete — **541/541 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `afa50681` prefix; 541
cases), zero unexpected faults** (the 10 faulted cases are the same
pre-existing intentional-null fixtures that assert the fault —
`ac80-foe-globnull` now correctly reaches its intended `0x327E27`
fault instead of dying early in `2F9AAF`).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..223; no new cases — existing fixtures completed to
native depth and asserts retargeted from scripted keys to real tags)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

Twelve entry-proven scripted entries removed; five bodies that already
carried REAL tags kept them, five new REAL tags added. The package is
the member/foe slot-write accessor chain under `0023AC80` +
`0031A630`, plus the already-supported direct-entry bodies whose
fixtures needed native depth.

| body | semantics | hits |
|------|-----------|------|
| `00317930` (`l317930`) | slot-accept probe `(rec, slots=rec+0x50, cursor, id, a5)`: `w[0x20107E8+cursor*2]` sentinel shortcut → id==FFFF → 0 → `322C50(6,id)` memt range → `a5` → `309EC0(id,0)` free-count≥1 → memt row `b7>>5 == cursor` → cursor==1 arm (`b[row+9]==0x12` or `w[slots]==FFFF` skip, else `b[prev_row+0x11]==b[row+9]`) → `b[rec+5]` / `bt d[foerow(b[rec+4])], b[row+9]` → `323C60` allow. | ×48 |
| `00318B40` (`l318b40`) | slot-pair rebalance `(pair=rec+0x50, written_idx, flag)`: `w[pair]`==FFFF → (flag: `30F9A0`/`30C410`) + **unconditional** `w[pair]=0x1000` normalize; resolve memt row tag `b[+0x11]`; neighbor `w[pair+2]`==FFFF→0xFF else `b[row+9]`; tag mismatch → idx==1: (tag 0x12, or 0xFF with self-tag 0x12) → self-reset `w[pair]=0x1000`; else clear `w[pair+2]`=FFFF. | ×99 |
| `00324100` (`l324100`) | effective grade: `r14d = 324020(rec)` floor; scan `rec+0x194` bits 18..30 — each set bit i → `w[abil_row(i)+8]` → `308FF0(0,id)` → `esi = max`. Returns `max(r14d, esi)`. | ×16 |
| `00324020` (`o4020`) | **popcount** of `rec+0x194` bits 0..17 (three unrolled iterations of six bits; `r9` accumulates +1 per set bit). | ×29 |
| `00323C60` (`s3c60`) | allow-check `(rec,id)`: `322C50(1,id)` auto-class range → `b[rec+5]!=0 || b[rec+4]>6` bypass → memt row `b7&0x10` allow flag → else `323BB0` required-class bitmap (`2F8FA0` over abild) ∩ `rec+0x194`. | ×46 |
| `003243F0` (`l3243f0`) | unlink/release helper — or-mask gate, `3105D0`/`313F60`/`300E40`/`2E42D0`/`2699D0`/`2ECEC0` scripted sinks recorded by arg. | ×1 |
| `0030C650` (`l30c650`) | level-set/stat growth: FOED level row (`b[rec+4]` index), `grwd` (`q[0x2EBF108]`) growth bytes via `2F9A60`/`2F9B20`, own `30FED0` notify. | ×29 |
| `00323910` (`lg3910`) | license grant/revoke: `323D10` type arm, LP cost `b[abil_row+4]` → `d[rec+0x190]`, bit set/clear at `rec+0x194+idx`, `324020`/`324100` grade refresh, `30A310`/`300B80`/`3008A0` rank chain, `fed0`. | ×3 |
| `00308FF0` (`a8ff0`) | ability grade: `id>0x21E`→0; `d138` row (`q[0x2EBF138]`) `b[+0x1E]`∈{5,6} → `b[+0xA]`, else 0. | ×5 |
| `00308040`/`00308130` (`m8040`/`m8130`) | member state accessors behind `308010`'s `b[member+5]` split. | ×3/×1 |
| `00234DA0` (`ld234da0`) | member-slot proximity scan — REAL tag already existed; SCR entry removed. | entry-real |

## Corrections of record

- **`324020` is a popcount, not a "highest set bit +1" scan.** It
  returns the number of set bits among `rec+0x194` bits 0..17. The
  `o324020_ret` fixture keys were replaced by real license bits.
- **`317930`'s `lea ecx,[r8+6]` uses a zeroed `r8`** — the `322C50`
  kind is the constant **6**, not `cursor+6`. (Earlier EXP-224 notes
  claimed a cursor-dependent kind — wrong; the register is cleared at
  `0x31798B` before the `lea`.)
- **`322C50` is a 31-entry kind jump table**, not a fixed member check.
  Kind-6 reads memt (`q[0x2EBF0F8]`): `[0x1000, 0x1000+d[+4])`, null
  desc → empty range → deny. The kind-1 arm auto-resolves the id's
  class via `309440` (`page=id>>12`, `class=d[0x1EEBCC0+page*0x58+0x38]`
  — shipped `page+5`) and re-dispatches; class-7 ids land on the
  `q[0x2EBF098]` range (`m98d` fixture).
- **`309EC0` page-1 dispatch is shipped-authored**: `q[0x1EEBD18+8]`
  word table, `+0x50` handler `002FD8D0`; mode-0 returns `cap−count`
  (free). `a630r9-clamp` (3/3) therefore genuinely **vetoes** —
  `31A630` returns `−1` with no writes, not the scripted-era success.
- **`31A630` calls `318B40` after every write**, including the
  FFFF-sentinel arm (which skips `317930` entirely). `318B40`'s
  `w[pair]`==FFFF init-to-`0x1000` is unconditional — so a denied slot
  array still gets `w[slots0]` normalized `FFFF→0x1000` whenever a
  sentinel write lands. `ac80-member-deny` now asserts this.
- **Real `30C650` emits its own `fed0(*,0)`** — the ac80-member fed0
  sequence is `[0, 0, 0x97, 0x97]` (c470 zero, c650 zero, two slot
  writes), not `[0, 0x97, 0x97]`.
- **`2F9A60`/`2F9B20` take a base-passthrough arm on growth byte 0**
  (`comiss 0.01, 0` → skip the RNG/div arm) — shared zero-row `grwd`
  fixture is stat-neutral.
- **`g7930-ok` under real depth:** `323C60` contributes its own
  `322C50` + memt/foed resolves → `v2c50`×2, `e600`×6 (was stub-era
  1/4). `g7930-s1eq` `e600`×8.

## Fixtures added

- `memt`/`memt_rows` — `q[0x2EBF0F8]` member-id table; row index is
  `id−0x1000`; row bytes: `b7 = cursor_class<<5 | 0x10` (slot-cursor
  class + `323C60` allow flag), `b9`/`b11` pair tags.
- `m98d` — `q[0x2EBF098]` kind-7 (`0x2xxx`) range desc for `322C50`'s
  class-7 arm.
- `grwd`/`grwrows` — `q[0x2EBF108]` growth desc (shared `GRWD`
  constant, zero rows); `c228()` now defaults `grwd` since `312280`
  guests reach real `30C650`.
- `d138`/`d138_rows` — `q[0x2EBF138]` grade rows (existed; now wired
  into `o4100-*`/`g3910-grade*`).
- `GRWMEMT`/`GRWMEMT_FOE`/`GRWMEMT_MEM`/`GRWM98` shared specs;
  foe-path slot ids re-ranged `0x501/0x502`→`0x1101/0x1102` (real
  kind-6 range rejects the old stub-fiction ids).
- Dead scripted keys removed: `s7930_ret` default, `s323c60_ret`,
  `o324020_ret`, `a308ff0_ret`.
- Assert retargets: `s323c60`→`s3c60`, `o324020`→`o4020`,
  `a308ff0`→`a8ff0`, `m308130`/`m308040`→`m8130`/`m8040`,
  `l8b40`→`l318b40`, `s7930`→`l317930`, `c650`→`l30c650`,
  `g3910`→`lg3910`, `u43f0`→`l3243f0` (all via `rargs`).

## Scripted boundaries retained

`0030FED0` (`fed0` ×173 — the status-recompute body), `00316A50`
(`s6a50`), `0030F9A0`/`0030C410` (`uf9a0`/`ec410` un/equip pair),
`003008A0` (`a08a0`), `0031B860` (`b860`), `00324470` (`m4470`),
`003105D0`/`00313F60`/`00300E40`/`002E42D0`/`002699D0`/`002ECEC0`
(teardown sinks), `00317ED0`/`00319490`→`003377C0`/`003180F0`/
`00319CA0` (entity-context chain), `0046AB10`, allocator sinks.
`u43f0-*`/`w4450-*` direct-entry cases exercise `3243F0`'s scripted
sinks as disclosed boundaries. None claim initialized-gameplay
reachability.

## Verification

- Suite: `python check.py` → **541/541**, run 3× fresh — `result.json`
  SHA256 prefix `afa50681` identical.
- Twelve SCR entries removed; zero leftover scripted hits for the
  promoted set (`s7930`/`l8b40`/`c650`/`g3910`/`u43f0`/`s323c60`/
  `o324020`/`a308ff0`/`m308130`/`m308040` all absent).
- Fault census: 10, all intentional-null fixtures asserting their
  fault: `0x23ADA8` (memd), `0x23AD7B` (foed), `0x326057` (oidx28),
  `0x327E27` (globnull), `0x318BE0` (l8b40-nomemt), `0x30904A`
  (a8ff0-nodesc), `0x30C757` (c650-nolvl), `0x30105A` (u0fc0-norec),
  `0x301150` (l01140-norec), `0x31BA57` (d228-globn).
- Suite regression during landing: 52 fails → 20 → 0, each classified
  as fixture gap (missing desc/row), semantic correction
  (`a630r9-clamp` veto, `324020` popcount, `fed0` seq, `318B40`
  normalize), or count pin (`v2c50`/`e600` under deeper native depth).
  No assertion weakened without shipped-body evidence.
