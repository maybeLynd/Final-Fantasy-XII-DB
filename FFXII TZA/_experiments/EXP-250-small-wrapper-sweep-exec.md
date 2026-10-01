# EXP-250 — small-wrapper sweep (`0031B8C0`, `002FA390`/`002F8E90`,
`002FA540`/`00320450`/`00329A20`, `00254850`/`00254940`/`002547D0`)
+ `0046AB10` cap early-out arm

**Status:** complete — **546/546 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `3d2df53a` prefix; 546
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on existing fixtures plus one new
direct-entry case; nothing claims initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..249; one new case `q6dup-cap`).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## What a player sees

This package removes the last synthetic-return stubs around three
everyday gameplay paths:

- **Roster slot → battle unit** (`0031B8C0`): `3138D0`'s mode-toggle
  tail asks "which battle unit sits in roster slot `esi`?" — the stub
  always answered with a live object; shipped code honestly answers
  "nobody" on an empty slot and the toggle write is skipped.
- **Mode-flag probe** (`002FA390` → `002F8E90`): the record-mode
  classifier consulted before stat-notification work.
- **Object-flag tails** (`002FA540` → `00320450` → `00329A20`;
  `00254850`, `00254940` → `002547D0`): bit-clear and bit-set helpers
  wrapping the already-real `002E1C20`/`002E1CA0` slot ops.

## Mechanism exercised (all shipped bytes)

- **`0031B8C0`** (`l31b8c0` ×2, stub `b8c0` removed) — `00263750(rcx)`
  roster lookup → null → ret 0 / nonnull → `00263E30` owner resolve.
  On `u0fc0-fastt`/`u0fc0-mtail` (`ecx=3`, roster slot 3 empty) the
  real body returns **0** → `003138D0`'s `je 0031398D` skips the
  `w[glob+0x5AD0] ^= (w ^ esi) & 1` write — the toggle word keeps its
  planted 3.
- **`002FA390`** (`l2fa390` ×1) → **`002F8E90`** (`l2f8e90` ×1) —
  leaf classifier on `e360-mode-pair`: `rcx==0x40000000`,
  `b[rcx+5]==0`, `b[rcx+4]` outside `0x1B..0x27` → ret 1 →
  `(1 & 7) != 0` → ret 1, identical to the retired `qfa390_ret=1`.
- **`002FA540`** (`l2fa540` ×1) → **`00320450`** (×1) → tail
  **`00329A20`** (×1) — both callees early-out on `b[rcx]&0x10==0`
  on `ce0-drop`; no state change, honest.
- **`00254850`** (`l254850` ×1) — ten `002E1C20` bit-sets on slot 8:
  bits {0,0x20,0x11,1,2,4,5,6,7,9}.
- **`00254940`** (`l254940` ×1) — `002E1C20`/`002E1CA0` select → tail
  **`002547D0`** (×1): bits {1,2,4,5,6,7,9,0xB}.
- **`0046AB10` cap arm** (`q6dup-cap`, new direct-entry case) —
  `d[r8+0x28] = 0x1FF` → `jge 0046AD51` epilogue, **ret 0 before the
  owner scan**: no `l69570`, no ring write, no `s5369c0`. The last
  unexercised `0046AB10` entry arm.

## Corrections of record

- **`u0fc0-fastt` / `u0fc0-mtail` toggle retargeted, not weakened.**
  The old `w[glob+0x5AD0] == 2` pin measured a stub-fed write arm:
  `b8c0` returned `objrow` unconditionally, so `003138D0`'s block ran
  and forced bit0 := `esi&1` (esi=0 → 3→2). The shipped body returns
  null for the empty roster slot and the write genuinely does not
  run — the pin now asserts the unchanged planted value `== 3`, and
  `l31b8c0`'s arg pin (`==3`) is retained. Dead `b8c0_ret` keys
  removed from both case defs.
- **`l69570` presence assert on the `q6dup-*` block is now gated** to
  the three scan/insert cases — `q6dup-cap` exits before the resolver.

## Harness note

Same `on_code` direct-entry convention as EXP-249: `q6dup-cap` proves
execution by the *absence* of side effects (no resolver call, no ring
write, no notify) plus ret 0.

## Not claimed

- `0031B8C0`'s nonnull arm (`00263E30` tail) — needs a planted roster
  slot-3 actor; the two callers never supply one.
- `002F8E90`'s `b[rcx+5]!=0` alternate path and the `0x1B..0x27`
  range-hit ret 2 — one fixture drives one arm.
- `00320450`/`00329A20` deep bodies beyond the `b[rcx]&0x10` gate.
- `00254940`'s `002E1CA0` select arm.
- Remaining stubs `v422c20`, `v427320`, `b6fa0`, `n12f0`, `b1dbdb0`,
  `b1850`, `b1f70`, `s181330`, `b3b02a0` — deferred (heavier or
  need live-arg fixtures).
- `00377C0` query arms `00391D10`/`003920F0`, `00383F10` real (IAT
  slot `008C2C10` → `.rdata` data), `003180F0`/`00319CA0`, live-game
  reachability — `NATIVE-REPLAY`, `live_game: false`.
- `e130`/`0030E130` still ×0.
