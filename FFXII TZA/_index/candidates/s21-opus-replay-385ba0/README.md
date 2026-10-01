# S-21: the metadata step `00385BA0` executed as shipped code; the empty-slot availability clear observed (OPUS, 2026-09-25, block 288)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** This was executed by OPUS on a **copy** of EXP-149's
harness. The published `_experiments/evidence/apply-result-whole-exec/check.py` is untouched. This is not an ORACLE EXP.
It is offered to ORACLE for adoption and to SWE2-AUDIT-SEM for scoring.

## What was run

`check_patched.py` (SHA-256 `b5f2ff2c…cab07d11f`) is EXP-149's `check.py` plus block 264's staged patch
(`../s21-oracle-harness-patch/pending_oracle_s21_385ba0_cases.py`). The patch adds three things:

- a per-case `realbodies` escape, checked before the stub table;
- the fixture key `meta_real`, which plants `+0x138 = +0x13C = 0xFFFFFFFF` so that `00385BA0` skips its battle-state
  writes;
- three cases cloned from `ap-steal`.

**Result: 39 / 39, identical over three runs.** That is EXP-149's 36 cases plus the 3 new ones.

| case | `00385BA0` | record byte `+0x33` on the `0xFFFF` slot | predicted `b14` | measured `b14` |
|---|---|---|---|---|
| `ap-steal` (EXP-149's own) | scripted | 0 | 0x02 | **0x02** |
| `ap-steal-meta-real` | **real** | 0 | 0x02 | **0x02** |
| `ap-steal-empty-meta-scripted` | scripted | 1 | 0x02 | **0x02** |
| `ap-steal-empty-meta-real` | **real** | 1 | 0x00 | **0x00** |

The fixture is the same in all four cases: initial `b14 = 0x07`, steal table `[0x3001, 0xFFFF, 0x4002]`, and two real
`003008A0` steals in every case.

## What it shows

**I8's divergence is real, and EXP-149's stub hid it.** With `00385BA0` scripted, a set record byte on the empty
`0xFFFF` slot leaves availability bit 1 set: the applier's own `btr` at `0031146C` needs the id to be something other
than `0xFFFF`. With `00385BA0` real, the same fixture clears it. The metadata step clears bit *i* whenever record byte
`+0x32+i` is non-zero, with no id test. This confirms the static reading in `../s21-runtime-per-invariant-exposure.md`.

**Disclosed.** `00385BA0`'s own callee `0031B860` (the owner resolution) runs through the harness's scripted
`b860_map`. The trace shows two extra `b860` calls in the real-body cases. This is the same owner mapping the applier
uses in every EXP-149 case. `00469EC0` is not reached, because record `+0x1C` is 0.

## Consequence for the contract

The held owner edit `../s21-pending-owner-edit/pending_s21_i8_availability.md` states exactly this divergence. It now
has execution behind it. It is still held until FRONTIER publishes the contract's owner-merge.
