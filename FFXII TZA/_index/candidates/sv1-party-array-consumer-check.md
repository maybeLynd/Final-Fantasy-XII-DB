# Affected-consumer check: SV-1, the party-stats array in the development saves, and a correction (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: SV-1 in `_index/OPEN-QUESTIONS.md` and `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/katano-debug-savedata.md`.
The corrected sentence is OPUS's own first narrowing (a6ea12736): "the bytes past the development size +0x5A70 are the
slot-map / sequence / transition / result-echo tail (+0x5A70..+0x5B10, 160 B)". It was pending review, not accepted.

**The ruling** (`_index/candidates/sv1-party-array/sv1_party_array.py`, 3 checks):
- All three development generations carry `BattleStatsRecord[40]`. The discriminator is byte `+4`, the definition row
  index, which runs 0..39 across consecutive records.
  - Generation A: image `+0x2208`, stride `0x1C4`.
  - Generation B: the same place, stride `0x190`.
  - Generation C: image `+0x15FC`, stride `0x140`.
- The shipped stride `0x1C8` finds no run in generation A.

**The correction.**
- Generation A's post-array fields sit `0xA0` = 40 × 4 lower than shipped. The slot maps at shipped `+0x5A48` / `+0x5A5A`
  are found at `+0x59A8` / `+0x59BA`, and the shipped offsets hold zeros.
- So the 160 B are the record growth (`0x1C4` to `0x1C8`), not a shipped tail. That tail existed in development at
  `+0x59D0..+0x5A70`.
- The sum is unchanged: 6,560 = 160 + 6,400 gambit bytes. "6,400 of the 6,560 are gambit data" stands.

**Regression.** P3 fails when the shift is set to 0, the tail reading, and passes at `0xA0` (mutation run by OPUS
before publishing).

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` SV-1 | narrowing prepended; the wrong clause struck in place, marked CORRECTED | revised-here |
| `katano-debug-savedata.md` SV-1 box | the same narrowing added; the same clause struck | revised-here |
| `_index/candidates/sv1-battle-block-tail/sv1_battle_block_tail.py` | kept unchanged as history: its four checks (block size `0x5A70`, the zero mirror tail, the gambit rows, the zero CRC slots) remain true. Only its docstring's tail attribution is superseded, by P3 here | agrees |
| `_types/fields.tsv` BattleSystemState / BattleStatsRecord rows | read, not changed; the shipped layout is not in question | agrees |

Run receipt: executed at 02cc89e7e - `sv1_party_array.py` (3 checks, FAILS 0) and `sv1_battle_block_tail.py` (4 checks,
FAILS 0).
