# EXP-245 — mask classifier `23B040` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `df9917f4` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; no new fixture — the path runs on
shipped-BSS-zero state; none claim initialized-gameplay
reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..244; asserts retargeted, none weakened).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

- **`0023B040`** (`lb040`, ×3 — `b040` stub removed) — the
  `300FC0`-tail eligibility classifier: builds a `ebx` mask of
  conditions (`b[0x2089340]&0x40` epoch bit → `esi`, the
  `&0x600`/`0x400000000000`/`0x8800403B`/`0x8800003B` masks,
  `b[row+0x6B7]`, `bt d[row],0x18` → `w[+0x714]>0x21E` /
  `b[+0x6B4]>=9`, rec-flags `+0x64|+0x3C & 0x80000003`), then
  publishes through three tail writers and tail-jumps to `26BD40`.

- **`00303EC0`** (`l303ec0`, ×3) — `ret 30D9A0()==2` (real
  `l30d9a0`).
- **`002E8100`** (`l2e8100`, ×0), **`00322600`** (`l322600`, ×0),
  **`00322920`** (`l322920`, ×0) — the deep-path helpers
  REAL-listed so a row-resolving fixture surfaces them with args:
  `2E8100` resolves `3588B0(ecx)` → `q[+0xC0]` chain → `w[+0]`/
  `d[+0]` checks; `322600`/`322920` are pure `(ecx-K)<range &&
  bt(mask)` bitset tests.

- **Tail publishers** (`l3592c0`/`l359200`/`l26bd40`, ×3 each):
  `3592C0(1, (ebx>>2)&1)` — `bts`/`btr` bit 1 of `b[0x22C8005]`;
  `359200(ebx&1, 1)` — bit 1 of `d[0x22C8000]`, and on nonzero
  resolves `3588B0(d[0x22C7FE0])`; `26BD40((~ebx>>1)&1)` —
  `setne b[0x209A2C5]`. All BSS cells.

## Path taken under fixtures

All three callers (`u0fc0-s400`, `u0fc0-s200`, `u0fc0-mtail`) run
the same route: `g272f0` unplanted → `d[0x2089340]&0x40`==0 →
`esi=ebx=0`; `303EC0` → `30D9A0()!=2` → eax=0 continue;
`313F60()`→0; `3272A0()` → `3590D0` ctx-id + `b[0x2089340]&0x10`
gate + `3588B0`/`263E30` chain — **no ctx chain planted** →
rdi=0 → early-out `0x23B1BB` → tail publishes with `ebx=0`:
`b[0x22C8005]` `&=~2`, `d[0x22C8000]` `&=~2`, `b[0x209A2C5]`=1.

The deep arms (`2E8100` id lookup, `322600`/`322920` kind tests,
`3135C0`/`3137F0`/`31B770` second-row chain, all the mask folds)
are gated behind `3272A0` returning a live row — none did, so
`l2e8100`/`l322600`/`l322920` stay ×0; disclosed, not claimed.

## Retargets

All seven `by("b040")` sites → `byr("lb040")` (`u0fc0-s400`/`s200`/
`mtail` ×1 positives, `def`/`m1`/`caps`/`s800` negatives). No
`_ret` plants existed (`b040` had no retkey). Fault census
unchanged at 20.

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `317E50` (`b7e50` ×0), `20CE60`, `427320`/
`422C20` (×1 each), `3377C0` (`v3377c0` ×19), `2E8FD0` (`v2e8fd0`
×1), `3B02A0`, `46AB10`, `210EC0`, `1CCB20`, `3180F0`, `319CA0`,
`426130`, `238BF0`, `36C140`, `36C1D0`, the `23B040` deep arms
(`2E8100`/`322600`/`322920` — need a `3272A0`-resolving fixture)
remain scripted or unexplored. `live_game: false`.
