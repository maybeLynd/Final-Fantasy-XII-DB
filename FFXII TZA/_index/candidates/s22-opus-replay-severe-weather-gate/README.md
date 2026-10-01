# S-22: the severe-weather accuracy gate (RW-5) and the pre-banded weather class (WE-3) executed (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-22's runtime cell lists RW-5's severe-weather gate
and WE-3 among its remaining items. The gate is not in the recipe resolver; it lives in the two step targets:
- step 35 = `003895D0`;
- step 36 = `00389610` (step table `01EFA5C0`).

Each tests context byte `+0x1A` bit `0x04` and then calls `003214A0`, which is `jmp 00263E20`. That returns `[02099DAC]`,
the banded weather gameplay class. Only when the class is 2 does the step scale the accuracy word `[02AEDFE0]`: by 0.8 in
step 35 (constant `008F3108`) and by 0.5 in step 36 (`01CEBB70`).

## What was run

`check.py` is standalone. It maps the whole SHA-asserted image.
- **No application stub, no bridged import.** Every IAT slot is a trap.
- **Allowed set:** the two steps' closures plus `00263E20`.
- **Planted data only:** the context record (`r8`), the class word and the accuracy word.

**5 / 5 pass, and `result.json` is byte-identical over two runs** (md5 `867bbaf3cc23ce50b3d38778aa27afb0`).

| case | contract item | observed |
|---|---|---|
| `R1_bit_clear_class2_scales_08_and_05` | RW-5 | bit clear and class 2: accuracy 100 → **80** (step 35) and 100 → **50** (step 36) |
| `R2_bit4_set_leaves_accuracy` | RW-5 | bit `0x04` of `+0x1A` set: unchanged, with class 2 or class 1 |
| `R3_class_0_or_1_leaves_accuracy` | RW-5 | bit clear but class 0 or 1: unchanged |
| `R4_only_that_bit_gates` | RW-5 (the gate differs from the element bypass) | every other bit of `+0x18..+0x1B` set (byte `+0x1A` = `0xFB`): both steps still scale. **No other context bit, the element bypass included, opens or closes this gate** |
| `W3_the_class_is_read_verbatim_not_rebanded` | WE-3 | `00263E20` returns `[02099DAC]` verbatim for 0, 1, 2 and 5. The consumer reads a class computed elsewhere (EV-5 bands it) and does not re-band it |

*Addressing note:* the gate bit is byte `+0x1A` bit `0x04`. The contract names it "merged context bit 2"
(`AccuracyBoost`). That wording matches if the merged context is counted from `+0x1A`; if it is a dword at `+0x18`, it
is bit 18. This file measures the byte and does not rule on the naming.

## Not covered

- ST-1, ST-2 and ST-6: table facts (extent, distinct targets, unused slots), put to AUDIT-SEM as static structure;
- WE-1's stage order (the pre-affinity stage and `0038B6A0` both reading `ActionDefinition + 0x13`);
- a live game.
