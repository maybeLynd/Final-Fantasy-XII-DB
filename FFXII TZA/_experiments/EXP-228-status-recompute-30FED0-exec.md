# EXP-228 — status recompute `30FED0` real (bitmap build + diff dispatch + member tail)

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `73bde5c4` prefix; 542
cases), zero unexpected faults** (the 20 fault records across 10
cases are the same pre-existing intentional-null fixtures that assert
the fault).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..227; no new cases — existing `fed0` call sites now
execute the shipped body and asserts retargeted to the real tag)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Body promoted real this round

`0030FED0` (`fed0`, **×196 — the largest scripted call**) — the status
recompute invoked after every stat/field change (`edx` flags are OR'd
with `0x202` internally: bit9 suppresses `30E130`'s recompute
recursion). ~594 insns `0x30FED0..0x3105C0`.

| body | semantics | hits |
|------|-----------|------|
| `0030FED0` (`l30fed0`) | **Bitmap build** into a 16-byte stack map: `b[rec+5]==0` → `row = 20E600(d[FOED+0xC]) + w[FOED+8]*b[rec+4]`, bits 0-63 = `d[row+0x50]`/`d[row+0x54]`; `b[rec+5]==1` → `31B860(rec)` owner → OR `owner+0xE80` bitfield. **Equip slots:** 5 words `w[rec+0x50..0x58]`, each gated `322C50(6,id)` (member-range) → `row = 20E600(d[MEMT+0xC]) + w[MEMT+8]*(id-0x1000)` → `31E9A0(row)==3` and `b[row+0x1A]!=0xFF` → `bts`. **License loop** `i<0x169` over `rec+0x194` bits: `row = 20E600(d[ABILD+0xC]) + w[ABILD+8]*i` → `323890(b[row+5])==2` → each `w[row+8..0x16]` `!=0xFFFF` → `bts`. **Diff:** 16-byte loop `added = new&~old` / `removed = ~new&old` vs `rec+0x78` → per set bit `edi<0x80`: `30E130(rec, edi, 0, flags|0x202, 3)` for added / `mode 1` for removed (scripted `e130`). **Notify:** `2FEF30(rec,0,0)` (scripted `fef30`). **Member tail** (`b[rec+5]==1`): `31B860` ×2 — `bt d[owner+0xE90],i` `i<0x20` → `30E360(rec,0,i,0,flags,5)` per set bit; then `b[q[owner+0x6A0]]&0x80` selects copy direction `ownerctx+0x78..0x7C` ↔ `rec+0x40..0x44`. **Field tail:** `d[+0x48]` clamp vs `d[+0x24]` (`flags&0x10000` → min 1; `bt flags,0x1C` doubles), `w[+0x4C]`/`w[+6]` vs `w[+0x28]` under `b[+0x6C]`-sign + `b[+0x7C]` gates with `b[+0x37]` multiplier → `30E060(rec, flags|0x202)` (`n0e060`, real). | ×196 |
| `0031E9A0` (`l31e9a0`) + `0031E9F0` (`l31e9f0`) | equip/status row classifier: `b[row+9]` ≤0x1A indexes the shipped `.rdata` jump table at `0x1FEA50/0x1FEA74` → class 0-8 → mapped to {0,1,2,3}; ret==3 = equipment-bearing row. Runs raw under `memt` rows (`b[row+9]`=0 → class 0 → not equipment). | ×61 |

## Scripted boundaries added

- `0030E130` → `e130` (`e130_ret` case key) — the status-bit modifier
  `(tgt, bit, r8d, r9d=flags, mode)` documented in EXP-148. **Fired 0
  times**: under every current fixture the computed bitmap equals
  `rec+0x78` (all desc-row masks, `owner+0xE80`, equip `b[+0x1A]`, and
  `323890==2` license rows resolve to zeros) — the diff loops, mode-3
  and mode-1 dispatch arms were executed as shipped bytes but with an
  empty operand set. No depth claimed beyond what ran.
- `002FEF30` → `fef30` (`fef30_ret` case key) — the once-per-run
  notify (EXP-100). ×196 recorded.

## Corrections of record

- `31B860` call-count pins +1 on five cases (`a630r9-off` 0→1,
  `a630r9-nomatch` 1→2, `c650-one` 1→2, `c650-multi` 3→4,
  `g3910-e5` 1→2): real `30FED0` tails into `30E060`, which calls
  `31B860` unconditionally at `0x30E084` — the stub hid it.
- `a630r9-nomatch` `e6820` pin 2→4: `30E060`'s `31B860` ran the full
  `236850`/`236820` OBJARR element scan a second time.
- EXP-148's record of the dispatch says mode 3 only; the body actually
  runs **two** dispatch arms — `rsp+0x50` (added bits, mode 3) and
  `rsp+0x60` (removed bits, mode 1) — from `new^old` vs `rec+0x78`.

## Member-arm coverage actually exercised

- `ac80-member*` / `ac80-foe-f690*` (`b[rec+5]==1` + `objlink`):
  4× `b860` per `fed0` (head owner resolve + two tail resolves +
  `30E060`'s internal one), owner `+0xE80` bitmap OR, `q[owner+0x6A0]`
  field sync — all real.
- `f3f0-*` cases plant `d[owner+0xE90]` bits → real `30E360` mode-5
  dispatch ×4-5 per `fed0` from inside the member tail.
- `l31e9a0`/`l31e9f0` ×61: member-range equip slot ids passed
  `322C50(6,·)` and were classified real on `memt` rows.
- `l323890` ×33: license-bit rows classified real (`b[row+5]`=0 →
  class ≠2 → skipped; no planted `abil` row reaches the word fold).

## Fixture notes

No new fixtures were required. The three descriptor cells the body
locks — `0x02EBF0F8` (`memt`), `0x02EBF038` (`abild`), `0x02EBF130`
(`foed`) — were already planted by the EXP-193/194 plumbing
(`mkdesc`: `w[desc+8]`=stride, `d[desc+0xC]`=`elemb` offset resolved by
`20E600`). `q[objrow+0x6A0]` was already planted under `objlink`
(0x100 buf, bit7 clear → the `rec`→ctx copy arm). `rec` is 0x400 —
covers the `+0x194` license-bitmap scan; `elemb` 0x90000 covers all
desc offsets (`foed` 0x20000, `abild` 0x30000, `memt` 0x60000).
Shipped-null `q[0x1F83530]` (`20E600` base) stays zero — row addresses
resolve to `elemb + off` directly.

## Boundaries (unchanged disclosures)

`30E130`/`2FEF30` scripted (newly intercepted — previously hidden
inside the `fed0` stub); `fed0`'s own recursion through `30E130` is
ship-blocked by flags bit9 (`flags|0x202`) and additionally stubbed.
`30C970`, `319420`, `319140`, `8632B0`, `2EB0D0`, `46AB10`,
`426130`/`427320` remain scripted. `live_game: false` — synthetic
fixtures do not establish initialized-gameplay reachability.

## Regression triage

537/542 first run → 541/542 → **542/542**. All 5 failures were
count-pins where the real `30FED0`→`30E060`→`31B860` chain surfaced a
call the stub hid; one `e6820` pin absorbed the second element scan.
No assertion weakened; each pin documents the shipped caller.
