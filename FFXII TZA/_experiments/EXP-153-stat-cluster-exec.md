---
experiment: EXP-153
title: Stat cluster executed REAL inside 0023AC80 (per-bit dispatcher
  0030F690, recompute-check 0030F340, reconcile 0030F5A0, owner scan
  0031B860, can-die leaf chain 00377C20..002EF640) plus 15 direct-call
  cases proving per-body semantics
contract: ../04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md
method: B
live_game: false
tool: evidence/stat-cluster-exec/check.py
---
# EXP-153 — stat cluster `0030F690`/`0030F340`/`0030F5A0`, real

**Contract:** `../04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md`
**Scope:** EXP-152's three scripted stat boundaries promoted to real
execution — `0030C470`'s calls at `0x30C59D`/`0x30C5A5`/`0x30C5AD` now
run shipped bytes, and 15 additional direct-call cases prove each
body's contract standalone. `00377C20` (the "can-die" boundary shared
by EXP-148/149/150) also runs real — it is a 4-leaf chain, not the
400-instruction body earlier surveys reported (they decoded past its
`ret` into neighbors).
**Method:** NATIVE-REPLAY — shipped bytes under Unicorn; fixtures are
disclosed MODEL-PROVEN plantings of `.data` globals (as EXP-152 plus
dirty-mask pair `0208D320`/`0208D324`, object array `0208E688`/count
`0208E6A0`, can-die cells `021654C4`/`02ADD100`) and heap blocks.
No EXE bytes modified.
**Harness:** `evidence/stat-cluster-exec/check.py` (extends the EXP-152
fixture: same 22 integration cases plus `f690norow` and 15 direct-call
cases)
**Result:** `evidence/stat-cluster-exec/result.json` — 37/37 cases,
stable across 3 processes.

New scripted boundaries (entry-intercepted, args recorded, disclosed):
`0030E360` per-bit core (342 insns, stack cookie, self-recursion,
indirect `call rax` — separate package surface), `00300530` stat
apply+notify, `003243F0` unlink+release helper, `00300BC0`/`00300CE0`
reconcile applies. Existing boundaries unchanged: `0030C650`/
`0030FED0` (EXP-148 bodies), `00323910`, `00324100`, `00317930`,
`00318B40`, `0030F9A0`/`0030C410`, `00324470`.

Everything else runs **real**, adding: `0030F690`, `0030F340`,
`0030F5A0`, `0031B860` (+`00236850`/`00236820` array accessors, both
EXP-151-proven patterns), `00377C20`+`003148F0`+`002EF2B0`+`002EF640`.

## Structural corrections

- `0030F340` is ~60 insns ending `0x30F3EB`; it does **not** call
  `0030F690`/`0030F5A0`/itself. `0030F3F0` (flags arg, per-slot loop
  via `00320AB0`) and `0030F4B0` are separate broadcast wrappers that
  dispatch the same triple on flag bits — they are other callers'
  entries, not part of `0023AC80`'s surface, and are not exercised
  here.
- `00377C20` extent is 0x4E: `idx=003148F0()` →
  `max(d[0x2164480+0x1044],0)`; `tbl=q[02ADD100]`; guard
  `tbl && idx<d[tbl+4]`; return `w[tbl+idx*3+8]>>15`
  (**3-byte stride** — the field is addressed `rcx+rax+8` with
  `rcx=idx`, `rax=tbl+idx*2`; `movsxd` index). `002EF640` returns the
  static `0x2164280`; `002EF2B0` adds `0x200`. Executed standalone:
  flag set → 1, clear → 0, OOB → 0, null tbl → 0, negative idx → 0
  (bounds check), last legal index works.
- `0031B860(rcx)`: `rcx==0` → 0; else scans `d[0208E6A0]` rows at
  `q[0208E688]+i*0xF50` for `q[row+0x698]==rcx` — the same array as
  `00327150` but taking the needle as an argument.

## Executed semantics

### `0030C470` tail — how the cluster is driven from `0023AC80`

- `edx = d[0208D320] | d[0208D324]`; `0030F690(rec, edx)` iff nonzero;
  `0030F340(rec)` and `0030F5A0(rec)` unconditionally.
- On a memset record with zero dirty-mask cells all three are no-ops:
  `0030F690` skipped by the gate (`ac80-foe-*`), `0030F340` finds
  computed==stored and returns without `00300530`, `0030F5A0` finds
  both compares equal and calls nothing.
- `ac80-foe-f690gate` (`d[0208D320]=1`, owner row linked): `0030F690`
  runs real — `0031B860` owner scan traced, bit-0 fixup evaluates
  `d[rec+0x64]|d[rec+0x3C] & 0x80000003` = 0 (memset) so `00377C20` is
  never reached and `q[objrow]` bit26 is **not** cleared — then
  `0030E360(rec, 0, 0, 0)` fires for the set bit and `0030FED0(rec,
  0x217)` tails. `ac80-foe-f690norow` (no linked row) still fires
  `0030E360` — the fixup is skipped but the per-bit call is not.

### `0030F690` `(rcx=rec, edx=mask)` — per-bit dispatcher

- `for bit in 0..31`: `bt mask,bit` unset → skip. Bit 0 extra work:
  `row=0031B860(rec)`; if found, `bp=q[row+0x698]`; `bp==0` OR
  `((d[bp+0x64]|d[bp+0x3C]) & 0x80000003)==0` OR `00377C20()!=0` →
  skip, else `and q[row], ~0x4000000` (clears bit 26 of the owner
  object's flag qword — NOT the record's).
- Every set bit then calls `0030E360(rec, 0, bit, 0)` (scripted here;
  `f690-bits13` → args `[1,3]`).
- `0030FED0(rec, 0x217)` fires unconditionally after the loop —
  including mask==0 (`f690-mask0`).
- Direct-call proof: `f690-bit0-clear` (rec flag + can-die=0) clears
  bit26; `f690-bit0-candie` (can-die=1) vetoes the clear;
  `f690-bit0-noflg` never reaches `00377C20`; `f690-bit0-norow`
  (`0031B860`→0) skips the whole fixup.

### `0030F340` `(rcx=rec)` — recompute-check

- `flags = d[rec+0x3C] | d[rec+0x64]`.
- `bt flags,0x10` set → `computed = max(d[rec+0x48], 1)`; else
  `computed = d[rec+0x24]`, doubled iff `bt flags,0x1C`.
- `computed == d[rec+0x48]` → ret (`f340-equal`, zero calls).
- Else, unlink gate first: `b[rec+5]==0` (mode byte) && `b[rec+4]` in
  `[0x1B,0x27]` && `d[rec+0x48] <= 0` → `row=0031B860(rec)` →
  `003243F0(row)` scripted (`f340-bit10`: stored −5, idx 0x1C →
  `u43f0(objrow)` then `c530(rec, 6, 0, 0x217)`).
- Then `00300530(rec, computed−stored, 0, 0x217)` scripted
  (`f340-delta` → delta 7; `f340-bit1c` → delta 14).

### `0030F5A0` `(rcx=rec)` — reconcile

- Section 1: `gated = (b[rec+0x6C]<0 || b[rec+0x7C]<0) ? 0 :
  movsx w[rec+0x28]`; `if gated != movsx w[rec+0x4C]` →
  `00300CE0(rec, gated−w4C, 0x217)`; then if `gated > movsx w[rec+6]`
  → `00300BC0(rec, gated−w6, 0x217)`.
- Section 2: `gmax = gated ? (b[rec+0x37] ? w28*b37 : w28) : 0`;
  `if gmax != movsx w[rec+6]` → `00300BC0(rec, gmax−w6, 0x217)`.
- `edx` deltas are 32-bit stores (recorded `0xFFFFFFCE` for −50).
- `f5a0-hp` (w28=100, w4C=50, w6=0) → `h0ce0(50)` + `h0bc0(100)` ×2;
  `f5a0-gated` (`b[+0x6C]=0x80`) → `h0ce0(−50)` only;
  `f5a0-b37` (w28=10, b37=3, w6=20, w4C=10) → `h0bc0(10)` only;
  `f5a0-equal` → ret, zero calls.

## Limits

- Fixtures are MODEL-PROVEN plantings; `live_game: false`. Through
  `0023AC80` the record's `+0x3C`/`+0x64` flag pair is always memset
  to 0 — the bit-0 clear and `00377C20` paths are proven only via
  direct-call cases, which is disclosed in each case name.
- `0030E360`'s per-bit effects, `00300530`'s apply semantics,
  `003243F0`'s unlink body (contains `003105D0`/`00313F60`/`00300E40`/
  `002E42D0`/`002699D0`/`002ECEC0`), and the broadcast wrappers
  `0030F3F0`/`0030F4B0` remain scripted boundaries — args recorded in
  `result.json`.
