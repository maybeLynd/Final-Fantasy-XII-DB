# EXP-251 — `0031B8C0` nonnull arm + `00311CF0` unit-mode publish

**Status:** complete — **546/546 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `943cc4c7` prefix; 546
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on two extended fixtures; nothing claims
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..250; `ctx4` gains `None` = empty roster slot and
`n30` gains `q698` = linked flag node).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## What a player sees

`00300FC0`'s mode tail asks "which battle unit sits in roster slot
3?" and — when a unit answers — issues it command `0x113` through the
real command path: the mode word on the unit, the `0x4000` queued
bit, the `0x8000` pending marker, and the `w[glob+0x5AD0]` toggle the
UI polls. EXP-250 had the lookup returning "nobody" on an empty
slot; this package populates roster slot 3 and the class table so the
entire notify chain runs shipped end to end.

## Mechanism exercised (all shipped bytes)

- **`00263750(3)`** — `q[0209A1F0+3*8]`; `ctx4=[ctx0,None,None,
  actor]` plants slots 0 and 3 only (new `None` skip).
- **`0031B8C0`** → `00263E30(actor)` = `q[actor+0x30]` = the unit —
  nonnull for the first time on this path.
- **`003138D0`**: `w[unit+0xBA0]`/`w[+0x714]` ≠ `0x113` →
  `ebx = d[unit+8] = 0x12340000` → **`0031B7E0`** — `b[02089340]&0x10`
  set via `g272f0` → **`003588B0(0x12340000)` → `00263FF0` class-4
  row → `ctx0`** (`clstab={4:["ctx0"]}`) → `00263E30(ctx0)` =
  `q[ctx0+0x30]` = **rdi, the target unit**. `ebx!=0` so the second
  `0031B7E0` runs and re-resolves nonnull → `00311CF0(rdi, cid,
  0x113, 0)`.
- **`00311CF0`** (`l311cf0`, promoted — `b1cf0` boundary removed; it
  never fired in the suite so no prior case is affected):
  - `q[rdi+0x698]` planted (`n30.q698`, zeroed) →
    `(d[+0x64]|d[+0x3c]) & 0x80000003 == 0` → no `00377C20` arm.
  - `si==0x113` and `w[rdi+0x714]!=0x113` → **`w[glob+0x5AD0] &=
    0xFFFE`** — the second toggle writer; planted `3` → `2`.
  - `(d[node+0x64]|d[+0x3c]) & 0x8800203B == 0` →
    **`w[rdi+0xBA0] = 0x113`**, `d[rdi+0x6B0] &= ~2`.
  - `edi=cid≠0` → **`d[rdi+0xBB8] = 0x12340000`** (skips the `|=2` +
    `0x22C1DB8` byte store).
  - **`w[rdi+0xBA4] |= 0x8000`**, **`q[rdi] |= 0x4000`**; stack arg 0
    skips the `+0x748`/`+0x6F8` writes.
  - Tail `00317E60` → `003590D0()` (mctxid unplanted → cid 0 →
    `003588B0` miss) → `0025AAD0(1,0)` → ret. Bounded.
- Back in `003138D0`, the xor `w[glob+0x5AD0] ^= (w^esi)&1` (esi=0)
  holds the word at `2`. Pinned `==2` — the pre-EXP-250 value, now
  produced by two shipped writers in sequence.

All pins assert the real writes: `l311cf0` args `[rdi, 0x12340000,
_, 0x113]`, `w[rdi+0xBA0]==0x113`, `d[rdi+0xBB8]==0x12340000`,
`w[rdi+0xBA4]&0x8000`, `q[rdi]&0x4000`, toggle `==2`. `u0fc0-mtail`'s
`flg` pin updated `0x100`→`0x110` — `flg` IS `d[02089340]` and the
case now plants `g272f0=0x10` on top of the fixture's `0x100`.

## Chain recorded

`l31b8c0 → l263750 → l263e30 → l31b7e0 → l3588b0 → l263ff0 →
l263e30 → l31b7e0 → l3588b0 → l263ff0 → l263e30 → l311cf0 →
(317E60, 25AAD0 — silent-real)`

on both `u0fc0-fastt` and `u0fc0-mtail`.

## Not claimed

- `00311CF0`'s `edi==0` arm (`d[unit+0x6B0]|=2`, `0x22C1DB8` indexed
  byte store, `d[+0xBB8]=d[unit+8]`), its `[rsp+0x50]`-nonzero stack
  arg arm (`d[+0x748]=edi`, `q[+0x6F8]=01EEC2D0`), the `00377C20`
  gated arm, the `0x8800203B` skip, `q[unit+0x698]==0` early-out
  (`ret 0xFFFFFFFE`), and the other caller `00311B20`.
- `00317E60`'s `b[rax]&8` arm → `0033C9B0(rax+0x80)` (needs
  `mctxid`+clstab hit on the notify path).
- `w[unit+0xBA0]`/`w[+0x714]==0x113` skip arms of `003138D0`,
  `ecx>3` out-of-range arm of `00263750`.
- Remaining stub census (`v422c20`, `v427320`, `b6fa0`, `n12f0`,
  `b1dbdb0`, `b1850`, `b1f70`, `s181330`, `b3b02a0`), `00383F10`
  real, `00377C0` query arms, live-game reachability —
  `NATIVE-REPLAY`, `live_game: false`.
- `e130`/`0030E130` still ×0.
