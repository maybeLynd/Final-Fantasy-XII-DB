# EXP-248 — `3377C0` deep scaffolding: fallback tail `337700` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `992180aa` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn over an extended `n30`/entity-pool fixture on
`d228-pos`/`d228-pos2` only; no other case's state changed; nothing
claims initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..247; asserts extended with deep-path trace pins —
all new pins are *additions*, none weakened).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## What a player sees

When a battle unit's position changes, `319490` broadcasts to the
spatial system. EXP-247 proved the broadcast's entry guards run shipped
code. This package drives the guards *open* on the two position cases
and lets the real body walk its first real stage: position fetch,
entity-index resolve, context class-table lookup, eligibility gate —
then, with the query result set empty, the fallback tail that asks the
zone's occupancy/grid structures "where did this thing end up?"

## Bodies executed as shipped bytes this round

- **`00265090`** (`l265090` ×4 — twice per case) — position/radius
  fetch: `b[s+3]&0xE0==0x60` gate → `3DA710` tail copying
  `float[t+0x50]`→pos, `float[t+0x54]`→radius.
- **`003DA710`** (`l3da710` ×4) — the two-dword copy leaf.
- **`0031ABE0`** (`l31abe0` ×29 — 27 pre-existing silent-real callers
  surfaced by REAL-listing + 2 new) — `b[0x2089340]&0x10` gate (the
  `g272f0` mask EXP-247 already plants) → `3588B0` resolve.
- **`002EA7F0`** (`l2ea7f0` ×2) — eligibility gate; on `ctx0` hits
  `f[c138+0xF0]==0` → ret 0 → fallback path.
- **`00337700`** (`l37700` ×2) — the empty-result fallback: second
  `265090` fetch → `391410` → `384130` → `383F10`.
- **`00391410`** (`l391410` ×2) — grid pass: `383840` resolves
  `q[0x2AEDFB0]` (unplanted → null → early-out ret 0 — honest: no
  zone grid in this fixture).
- **`00383840`** (`l383840` ×2) — `ret q[0x2AEDFB0]` accessor.
- **`00384130`** (`l384130` ×2) — xz-pack helper, runs unconditionally.
- **`003588B0`**/`00263FF0` — already REAL-listed; the new fixture
  gives `3588B0` its first *live* resolve here (`l263ff0` ×11 total).

## Fixture planted (pos/pos2 only)

`n30` node widened to `size=0xF00` (covers `+0xEA9`), `b[n30]=8`,
`q[n30+0x10]=s` context link (`b[s+3]=0x60`, `q[s+0xB8]=t`,
`float[t+0x50]=1.0`, `float[t+0x54]=0.5`), `b[n30+0xEA9]=1` selects
entity-pool row 1, `oar4={1:{cid:0x12340000}}` plants that row's
`+0x698` record + `+8` context id, `clstab={4:["ctx0"]}` lets
`3588B0` resolve `cid`'s class nibble through the planted class table.

**Correction of record — fixture collision:** the first suite run
faulted inside `312280` (`mov rax,[rdx+0x698]` on a clobbered row)
because `oar4` slot 0 collided with `objlink`'s default source-object
row 0. Fixed by moving the deep entity to slot 1 and indexing it via
`b[n30+0xEA9]=1` — both rows now coexist.

## Scripted boundary — `383F10` stays scripted

`383F10` is a nav-grid cell walk whose inner helper calls through IAT
slot `q[0x8C2C10]`, which holds RVA `0x1CCF034` — `.rdata` bytes, not
code (unbound in this image). It cannot execute as shipped bytes, so
`s383f10` records the boundary and returns the shipped early-exit
value `0xFF` (the value its real `w[hdr+4] > vec.x` early-out arm
returns). `s383f10` ×2, disclosed.

## Path taken — disclosed

`3377C0`: guards pass → `265090` fetches pos/radius from the planted
`s`/`t` → `236820(b[n30+0xEA9]=1)` → `oar4` row 1 → `d[row+8]` cid
→ `31ABE0` → `3588B0` resolves `0x12340000` → `ctx0` → `2EA7F0` ret 0
→ empty result set → **`337700` fallback**: `265090` again →
`391410` early-outs (grid null) → `384130` → `s383f10`=0xFF →
ret 0. `l377c0` still ×19 total (17 rcx=0 callers unchanged).

## Assert additions

`d228-pos`/`d228-pos2` now pin the deep trace: `l265090`/`l3da710`
×2 each, `l31abe0`/`l3588b0`(via `cid` arg)/`l2ea7f0`/`l37700`/
`l391410`/`l383840`/`l384130` present, `s383f10` ×1 with ret `0xFF`,
and `s80f0`/`s9ca0` remain ×0 (the `312280` broadcast arms still
cannot fire — ret 0 is the honest outcome on this fixture).

## Not claimed

- `391D10`/`3920F0` spatial *query* arms and the per-entity loop
  (`263E30`/`314EB0`/`313F80`) — ×0, need populated query containers.
- `383F10` real body — unbound IAT slot, remains scripted.
- `336390`/`32A6A0`/`26E100` — unreached behind the null grid.
- `3180F0`/`319CA0` — still scripted ×0.
- Live-game reachability — `NATIVE-REPLAY`, `live_game: false`.
- `e130`/`30E130` still ×0.
