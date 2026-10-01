# EXP-259 — `00422C20` `+0x18` arm through `002ED570` (direct entry)

**Status:** complete — **562/562 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 prefix `a0d627ef`; 562
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on the extended `dcntr` fixture; nothing claims
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..258).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Mechanism exercised (all shipped bytes, `d422c20-18`/`18nul`)

The last `00422C20` resolver arm: `d[elem+0x18]` != -1 →
`0020E600(d[elem+0x10])` → resolved element's `q[+0xD98]` →
**`002ED570(C2, slot)`**.

`002ED570` resolves two **`003AB7F0`-tagged** container bases
(`ptr&3`: `0` = direct pointer, nonzero = `0036B130` handle
resolve — corrected by EXP-260: all nonzero tags take `36B130`,
there is no `2`/`3` null arm):

- `q[C2+0x30]` → stored to `q[C2+0x38]` — row base, stride `0x10`;
  `d[row + slot*0x10]` == -1 → return 0 (the skip arm).
- `q[C2+8]` → stored to `q[C2+0x10]` — sub base, stride `0x20`;
  `d[sub + (slot>>d[C2+0x4C])*0x20 + 0x10]` is the element offset
  resolved by `0020E600`.
- Return `element + (d[C2+0x50] & slot) * d[C2+0x48]` — the
  mask×stride select on the resolved element.
- `00422C20` then writes `d[ret] &= ~8` — the element flag clear.

## Pinned asymmetry

`d[elem+0x18]` is **not retired** — `00422C20` reads it once into
`edi` and never writes `-1` back, unlike `+0xC4`/`+0xC8` (which also
write `w[+0xCC]` on `+0xC4` only). The field stays a live slot
marker after the clear block.

## Cases

- **`d422c20-18`** — row non-`-1`: `q[C2+0x38]`/`q[C2+0x10]` get the
  resolved bases stored, `d[E2]` `0xF`→`7` via `&=~8`, `d[+0x18]`
  stays 1, clear block unchanged.
- **`d422c20-18nul`** — `d[row]`==-1: `2ED570` ret 0, `&=~8` skipped,
  `d[E2]` stays `0xF`, bases still resolved+stored, `d[+0x18]` stays 1.

## Not claimed

- `003AB7F0`'s `&3!=0` (`0036B130` handle-resolve) arm — **closed
  by EXP-260** — `0036B130`'s rejection paths, `002ED570`'s nonzero
  `d[C2+0x4C]` shift / `d[C2+0x50]` mask / `d[C2+0x48]` stride paths —
  **closed by EXP-260** — null `q[C2+0x30]`/`q[C2+8]` cached-base
  arms — **closed by EXP-260** —
  `0041CF00`'s `w[R+0x28]`/`d[R+0xC]&0x1000` arms,
  `0051BA40` mode-0/`b[desc]&2` arms, `005369C0`/`003B02A0` real,
  `q[02EBF188]` consumers, live-game reachability —
  `NATIVE-REPLAY`, `live_game: false`.
