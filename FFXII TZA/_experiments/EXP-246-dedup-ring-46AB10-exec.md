# EXP-246 — dedup-ring inserter `46AB10` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `25a8ffb1` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; one new disclosed fixture (`q6desc` — a small
desc block at `q[0x2EBF018]`); no claim of initialized-gameplay
reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..245; asserts retargeted, none weakened).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

- **`0046AB10`** (`l6ab10`, ×12 — `q6ab10` stub removed) — the dedup
  ring inserter the stat-change notifiers (`46A800`/`46A630`/`469E80`)
  tail into. Flow: `d[r8+0x28] >= 0x1FF` cap early-out → `q[r8+8]`
  non-null → scripted `31B860` owner scan → `469570(edi=edx,
  q[r8], q[r8+8])` resolver → `q[0x2EBF018]` desc → two `20E600`
  index resolves (`elemb + d[desc+0xC]`, raw add) → `rcx = elem +
  w[desc+8]*edi` → `b[rcx+4]&1` chooses **dedup scan** (10×0x20 ring
  `0x2EBB560`, `q[e+8]==rsi && w[e]==edi` → `32A150` timestamp
  compare → refresh) or **insert** at `ring[d[0x2EBB54C]*0x20]`:
  `w[+0]=di`, `q[+8]=rsi`, `d[+4]=32A150()`, `q[+0x10]/+0x18`=0,
  cursor `(d[0x2EBB54C]+1) mod 10` via the 0x66666667 magic divide,
  then scripted `5369C0` insert-notify.

- **`00469570`** (`l69570`, ×12) — the resolver: `q[0x2EBF018]`==0
  (BSS on non-`q6desc` cases) → runs scripted `31B860` on both
  struct fields, stores misses to `q[0x2EBF188]`, returns **1**
  ("no dedup record exists — proceed to insert").  **Correction of
  record:** the first EXP-246 draft misread this as "0 == not found
  -> skip"; the shipped epilogue at `0x469685` is `mov eax,1`, so a
  null desc *permits* insertion — which is why the initial run
  faulted at `0x46ABB3` (`test byte [rcx+4]` with rcx=0 →
  unmapped read) rather than early-outing.

## New boundary / fixture

- **`005369C0`** scripted (`s5369c0`, ×12) — the insert-notify tail:
  0x240-byte frame with a stack-passed arg (`[rsp+0x64]`) that
  `46AB10` never writes; its sole caller is `0x46AC66`.  Recorded
  as a boundary rather than run real.

- **`q6desc` fixture** — plants `q[0x2EBF018]` = fresh desc block
  with `d[+0xC]`=`idx` (default 0) and `w[+8]`=`width` (default 0),
  so `rcx = elemb + idx + width*edi` lands inside the harness-owned
  element pool (`q[0x1FE3530]`, always planted).  Applied to the 12
  calling cases only: `e360-mode-pair`, `s8a0-flag4`,
  `s8a0-flag4clr`, `c650-{one,multi,clamp,mp,full}`, `d228-{ecap,
  lp5,fp,lvl}`.

## Shipped-computed pins

On `e360-mode-pair` (rcx=0x40000000, edx=18): `q[0x2EBB568]` ==
`0x40000000` (rsi stored at ring+8), `w[0x2EBB560]` == 18 (id),
`d[0x2EBB564]` == 0 (`32A150` timestamp on BSS `d[0x208D45C]`),
`d[0x2EBB54C]` == 1 (cursor advanced 0→1 mod 10), `q[0x2EBF188]` ==
0 (`469570` miss store), `s5369c0` ×1.

## Count adjustments (real-called scripted boundaries)

`31B860` stays scripted (`b860`) — real `46AB10`/`469570` now call it
through the planted struct fields: `q[r8+8]` non-null → in-body scan;
`q[r8]`==0 skips `469570`'s first lookup; `q[r8+8]` non-null → second
lookup.  Exactly **+2** per calling case — `c650-one` pin 3→5,
`c650-multi` pin 5→7, comments updated.

## Assert hygiene fix

The `s8a0-` assert block never defined `byr`/`rargs` — the lambdas
leaked from whichever sibling block last ran, bound to that case's
`w`.  Previously harmless (no `byr` use in the block); the EXP-246
retarget exposed it.  `s8a0-` now defines both locally.

## Not claimed

- Dedup-scan *hit* arm (`0x46ABD4` match → `32A150` timestamp
  compare → refresh at `0x46AC6B`): ring ships BSS-zero, every case
  inserts a fresh entry — the hit arm needs a pre-seeded ring row.
- `5369C0`'s real notify body — scripted boundary, stack-arg fragile.
- `d[r8+0x28] >= 0x1FF` cap early-out — no case exceeds 0x1FF.
- Live-game reachability — `NATIVE-REPLAY`, `live_game: false`.
- `e130`/`30E130` still ×0.
