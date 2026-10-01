# S-18: the battle-locomotion turn limiter executed as shipped code, BL-1..BL-6 as properties (OPUS, 2026-09-25, block 307)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** The contract is
`06-Movement-And-Navigation/CONTRACT-battle-locomotion-turn-limiter.md`, with one entry, `003364D0`.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image. **Nothing is substituted:** the body calls only its wrap leaf
  `0033CB70` (real) and no import. Entering any other function fails a case.
- **Fixtures** are planted data only: the flag block (`+0x21`, `+0x38`, `+0x3C`) and the motion state (`+0xE0`, both
  rates, `+0x170`).
- **The checks are properties stated from the contract, not a transcription of the body.** The error is the shortest
  signed angle, computed in double precision. Every case keeps it at least 0.5° from 20°, 45°, 120° and 180°.
- **The three constants** are read at the compare operands: 45° `0.7853982`, 120° `2.0943952`, 20° `0.3490659` (BL-1).

**2 / 2 pass, and `result.json` is byte-identical over three runs.**

### Single-call grid: 21,120 calls, 0 violations

The grid covers:
- 5 headings × 22 signed errors (5°–175°);
- `fl38` × `fl3C` × six `fl21` values, including foreign bits `0x80` / `0x01`;
- four `+0x170` values × two rate pairs (one large enough to snap).

| property | contract | exercised |
|---|---|---|
| flag clear and error ≤ 45° → returns the current heading bit-exact and writes nothing | BL-2, §10 | 3,840 |
| error > 45° raises `fl38` bit 3 | BL-1 | 17,280 turning |
| above 120°, the latch sets **only** with `+0x170 & 0x1C == 0x1C` | BL-3 | 1,440 set, 1,440 blocked |
| 20°–120° keeps the latch as it was | BL-4 | 4,800 with the latch at 1 |
| ≤ 20° releases it | BL-4 | 960 from 1 |
| within the rate → result is **exactly** `desired`, and bit 3 and the latch are clear | BL-6 | 5,040 |
| otherwise one step of the selected rate toward `desired` | BL-2 / BL-4 | 8,400 |
| above 120° with a direction already set, `current ± rate` in **that** direction | §14 (committed-direction latch) | 3,840 |
| exactly one of `fl21` bits 1 / 2, matching the step's sign; other bits preserved | BL-5 | every turning call |

**Negative control.** A scratch copy whose expected latch ignores BL-3's three-bit condition (a port "that selects
the rate from the angle alone") **fails**: 1,440 BL-3 violations, plus the rate, direction and snap errors that follow
from them. The properties discriminate.

### Histories (the result fed back as the next heading)

| history | contract | observed |
|---|---|---|
| 50° off, flags clear | BL-2 hysteresis | turns, **is still turning below 45°**, and snaps to `desired` |
| 40° off, flags clear | BL-2 | never turns; the heading is unchanged |
| 150° off with the three bits | BL-4 path dependence | latch set at 150° and **kept at 115°, 98°, 81°, 64°, 47° and 30°** (fast, 17.2° steps). Released at 12.5°, then slow 5.7° steps, then the snap |
| 60° off, turning, latch clear | BL-4 | one **slow** step |
| both long histories | BL-6 | end with `result == desired` and both flags clear |

## Not covered

- the callers in the step-solver family;
- `0033CB70`'s large-magnitude divide path (`0033CBCD`) is not targeted, and whether any case here reaches it was not
  recorded;
- a live game.
