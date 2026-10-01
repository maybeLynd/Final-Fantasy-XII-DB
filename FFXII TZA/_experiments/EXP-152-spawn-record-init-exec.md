---
experiment: EXP-152
title: Spawn-record initializer 0023AC80 executed with the REAL
  callee layer (stats header 0030C470, slot writer 0031A630, gil
  clamp 00323790, pair copy 00327CB0, counter/snapshot 00326030,
  order materializer 00327DE0, validator 00322C50, curve 002F8F20),
  closing EXP-150's largest scripted boundary
contract: ../04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md
method: B
live_game: false
tool: evidence/spawn-record-init-exec/check.py
---
# EXP-152 — spawn-record init `0023AC80`, real callees

**Contract:** `../04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md`
**Scope:** `0023AC80` (0x2CC) executed as shipped bytes — the
spawn-record initializer the installer `0023A570` calls inside the
`b[spawn]&5==0` fresh-spawn arm. Every direct callee runs real except
the disclosed scripted boundary set.
**Method:** NATIVE-REPLAY — shipped bytes under Unicorn; fixtures are
disclosed MODEL-PROVEN plantings of `.data` globals (`02089300` gate,
descriptor cells `02EBF120`/`02EBF130`/`02EBF038`/`02EBF0E0`/
`02EBF0D8`, `02EBF190` context, `01F83530` element base, `02089378`
order rows) and heap blocks. No EXE bytes modified.
**Harness:** `evidence/spawn-record-init-exec/check.py`
**Result:** `evidence/spawn-record-init-exec/result.json` — 22/22
cases, stable across 3 processes.

Scripted boundaries (entry-intercepted, args recorded, disclosed):
`0030C650`/`0030FED0` (EXP-148's own executed bodies, scripted here
when reached as callees), the mutually-recursive stat cluster
`0030F690`/`0030F340`/`0030F5A0` (pulls `00377C20`/`003105D0`/
`0030E360` — separate package surface), deep grant `00323910`
(0x299, 15 calls), `00324100` override, `00317930` slot-search gate,
`00318B40` list op, `0030F9A0`/`0030C410` un/equip and
`0031B860`/`00324470` member-block chain (the last four reachable
only on `r9d!=0`, which `0023AC80` never passes — scripted
defensively).

Everything else runs **real**: `0023AC80`, `0020E600`,
`00861EC0` (memset hook), `0030C470`, `0031A630`, `00323790`,
`00327CB0`, `00326030`, `00327DE0`, `00322C50` (0xA arm through the
real jump table), `002F8F20`.

## Executed semantics

### `0023AC80` `(rcx=rec, edx=sel)` — sel: byte0=idx, byte1=mode

- `memset(rec,0,0x1C8)`; `q[+0x50]=-1`; `w[+0x58]=FFFF`;
  `w[+0x1C3]=FFFF`; `b[+0x1C5]=FF`. Executed even on gate-off and
  mode>=2 paths (`ac80-gate-off`, `ac80-mode2`).
- `d[02089300]==0` → ret 0. Mode>=2 → ret 0.
- Mode 1 (member): `q[02EBF120]` desc → `memb_row =
  20E600(d[desc+0xC]) + w[desc+8]*idx`; null desc leaves `r14=0` →
  **fault `0x23ADA8`** on `w[0x16]` (`ac80-member-nulld`).
- Mode 0 (foe): `q[02EBF130]` → `foe_row` likewise; null desc →
  **fault `0x23AD7B`** on `b[0x2E]` (`ac80-foe-nulld`). count arg =
  `max(b[foerow+0x2E], 1)` (`ac80-foe-cnt0` → 1).
- `w[rec+4]=sel`; `30C470(rec, count, is_member)`.
- Member: 4× `31A630(rec, 0..3, w[+0x16]/w[+0x1C]/FFFF/FFFF, 0)`.
- Foe: `323790(rec, w[foerow+0x44])` gil add; `idx<=6` → ability scan
  of table `q[02EBF038]` rows `i<d[tbl+4]`, granting `323910(rec,i,
  1,1)` per row with `b[row_i+7]&(1<<idx)` (`ac80-foe-scan` → grants
  i=1,2,3; `ac80-foe-idx7` skips the scan entirely); 5× `31A630`
  slots 0..4 from `w[foerow+0xA..0x12]`; `327CB0(rec,
  w[foerow+0x14])`; `326030(q[02EBF190], idx)`;
  `327DE0(q[02EBF190]+8+idx*0x1C8)`; `b[foerow+0x2C]&0x40` →
  `d[rec]|=4` (`ac80-foe` vs `ac80-foe-noflag40`). Ret 1.

### `0030C470` stats header `(rec, count, is_member)`

- `esi=b[rec+5]` (mode byte), `r14d=b[rec+4]` (idx); `b[+0x1C2]=0`.
- Mode 0 re-resolves FOED internally (`rbp=foe_row`; null → fault
  `0x30C4F9`). Copies `w[+0x16]→d[rec+8]`, `w[+0x1A]→w[rec+0xC]`,
  `b[+0x1E/0x21/0x24/0x27]→f[rec+0x10..0x1C]` (cvtdq2ps),
  `b[+0x46]→b[rec+0x20]`, then `324100` scripted override
  (`b[+0x20]=max(cur, ret)`).
- Mode 1 skips stats entirely — `b[rec+0x88]=r8b` only
  (`ac80-member` asserts `d[rec+8]==0`, `b[rec+0x88]==1`).
- Common: `30C650(rec,count,2)` scripted; `d[rec+0x18C] =
  min(2F8F20(count-1), 0x5F5E0FF)` — `2F8F20` is a real leaf
  polynomial (`count-1==0` → 0: `ac80-foe-cnt0` discriminates);
  `d[0208D320]|d[0208D324]` gates `30F690` (`ac80-foe-f690gate`
  proves both directions); `30F340`/`30F5A0` always; `w[rec+0x4C]`
  = 0 on memset'd recs (`b[+0x6C]`/`b[+0x7C]` signed-negative test
  gates `w[+0x28]` load; foe arm is `b[foerow+0x47]*w28/100` via
  `0x51EB851F` magic); `30FED0(rec,0)` scripted.

### `0031A630` slot writer `(rec, slot, val, flag)`

- `rcx==0` → -1. `si==0xFFFF` skips the `317930` gate → direct write.
- Else `317930(rec+0x50, slot, val)` scripted gate: ret 0 → `31A630`
  returns -1 **without writing** (`ac80-member-deny`: slots stay
  FFFF, no `fed0(0x97)`).
- Writes `w[rec+0x50+slot*2]=val`; `318B40` scripted; on CHANGE
  (`!= old`) fires `30FED0(rec,0x97)` — observed order is
  `fed0(0)` (from `30C470`) then `fed0(0x97)`×2 (`ac80-member`,
  `ac80-foe`).

### `00327CB0` pair copy `(rec, pairidx)` + tail `327DE0(rec)`

- `rcx==0` or `b[rec+5]!=0` → ret. **`b[rec+5]` is the mode byte —
  dead gate from `23AC80` (foe mode is 0; member never calls it).**
- `322C50(0xA, pairidx)` real — 0xA arm: `0x5000 <= pairidx <
  0x5000+d[q[02EBF0E0]+4]` (`ac80-foe-pairbad` `0x4000` → ret 0 →
  skip; `ac80-foe-pairnull` null tbl → same skip, no deref).
- Resolves `q[02EBF0E0]` row `pairidx-0x5000`; copies ≤12
  `(w[+i*2], w[+i*2+0x20])` pairs → `w[rec+0x88+i*4]`/`+0x8A+i*4`,
  `bts w[+0xB8],i`; stops BEFORE a write when either src word is
  FFFF; `b[+0xBA]=count`; pads entries count..11 with
  `d=0xFFFFFFFF` and `btr`s the mask (`ac80-foe`: pair0 copied,
  entries 1..11 read `FFFF`, `b[+0xB8]=1`, `b[+0xBA]=1`).
- **Tail-calls `327DE0(rec)`** — first of two `327DE0` runs.

### `00326030` slot snapshot `(glob, idx)` — real

- `d[glob+idx*4+0x7370]=0` (cursor clear).
- `r8=glob+8+idx*0x1C8` when `idx<=0x27`, else `r8=0` → **`movups
  [0x88]` fault `0x326057`** (`ac80-foe-oidx28`; `0x27` passes —
  `ac80-foe-oidx27`).
- Copies the slot row's 0x34-byte pair block `+0x88..0xBB` into the
  `0x5B10` chain at `glob+idx*0x9C+0x5B10`, `+0x5B44`, `+0x5B78` —
  **three copies filling cursor positions `idx*3`,`idx*3+1`,
  `idx*3+2`**. The layout is boundary-tight: 40 slots × 3 blocks ×
  0x34 fills `0x5B10..0x7370` exactly, ending where the cursor array
  begins.

### `00327DE0` order-row materializer `(row)` — real, runs twice

- `b[row+4]` = order-table index → `ordrow = 02089378 + idx*0x170`
  (canonical .data writes observed).
- Cursor = `d[glob+oidx*4+0x7370]`; `blk = glob+0x5B10 +
  (cursor+oidx*3)*0x34`; per set bit `i` of `w[blk+0x30]`:
  pair `(w[blk+i*4], w[blk+i*4+2])` (skip on FFFF) → resolve
  `q[02EBF0D8]` row `bp-0x6000` → writes ordrow entry `i*0x18`
  fields: `b[+0x10]→+0x26`, `w[+8]→+0x28`, `w[+0x18]→+0x2A`,
  `b[+0x11]→+0x2C`, `w[+0xA]→+0x2E`, `w[+0x1A]→+0x30`,
  `b[+0x12]→+0x32`, `w[+0xC]→+0x34`, `w[+0x1C]→+0x36`
  (`ac80-foe-ordrow` materializes 2 entries from mask 3).
- First call `(rec)` reads the chain BEFORE `326030` fills it —
  the pipeline order in `23AC80` is `327CB0`→`327DE0(rec)` →
  `326030` (snapshot) → `327DE0(slotrow)`. Null `q[02EBF190]`
  faults inside the FIRST call at `0x327E27` on
  `d[0+idx*4+0x7370]` — before `326030` is reached
  (`ac80-foe-globnull`).

### Unreachable-via-`20E600` arms (documented, not executed)

`20E600` is `eax = ecx + q[01F83530]` — with `elemb != 0` it cannot
return 0, so `23AC80`'s `r8=0 → b[7]` scan arm (`0x23AE68`) and
`30C470`'s null-rbp stat arm have no path through this caller.
`327DE0`'s resolve-fail → `w[rax+8]` on rax=0 IS reachable if the
`02EBF0D8` desc resolves a null row base — left as a noted edge;
`ordd` null → `r8=0` → same `0x327EDF` fault.

## Fault boundaries proven

| case | fault PC | cause |
|---|---|---|
| `ac80-member-nulld` | `0x23ADA8` | `w[r14+0x16]` on r14=0 |
| `ac80-foe-nulld` | `0x23AD7B` | `b[rbp+0x2E]` on rbp=0 |
| `ac80-foe-oidx28` | `0x326057` | `movups [r8+0x88]` on r8=0 |
| `ac80-foe-globnull` | `0x327E27` | `d[0+idx*4+0x7370]` inside `327DE0` (via `327CB0` tail) |

## Limits

- Fixtures are MODEL-PROVEN plantings; `live_game: false`. Nothing
  here proves the live game reaches `23AC80` with these fixtures —
  it proves the function's executed contract on planted inputs.
- `323910`'s grant effects, the `30F690/30F340/30F5A0` stat
  cluster, `30C650`/`30FED0` internals and the `31A630` r9d-arm
  remain scripted boundaries — args recorded in `result.json`.
- `b[rec+0x6C]`/`b[rec+0x7C]` signed tests in `30C470` always take
  the non-negative arm on a memset'd rec (fixture-inherent).
