# S-06: the developer console's dispatcher executed as shipped code for every command id (OPUS, 2026-09-25, block 315)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-06's runtime cell is NOT MET with the gap "runtime
evidence". `CONTRACT-developer-tuning-console.md` has no execution. This narrow OPUS harness runs its dispatcher
`001D1660` for all command ids, in both directions.

## What was run

`check.py`:
- **Call shape.** It calls the dispatcher through its real caller shape, `001CD040`. `0017DB90` passes the settings
  object as `rcx`, the direction in `dl` and the id in `r8d`; `001CD040` sets `r8b = !dl` and `r9d = id` and
  tail-jumps into `001D1660`.
- **Image.** It maps the whole SHA-asserted image. **No application stub.**
- **Allowed set.** The dispatcher's static closure (2,137 functions).
- **Imports.** Every IAT slot is trapped; memcpy / memmove / memset / malloc / free are bridged by name. An arm that
  reaches any other import, or an unplanted object, **stops and is reported as stopped**.
- **Fixtures** are planted data only: the settings object `DeveloperConsoleSettings01F81428` (block 314) behind
  `[01F81428]`, and zeroed `PostProcessParamContext` / `BootSingleton01F7F598` blocks behind their cells so the lazy
  getters return them.
- **Recorded per call:** the arm the jump at `001D16AE` selects (`r9`), and every non-stack write.

**All checks pass, and `result.json` is byte-identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `I1_I3_table_static` | I-1, I-3 | 282 entries at `001D4C1C`, all inside the body, **227 distinct**, **56 on `001D4BFA`** |
| `I2_out_of_range_is_a_noop` | I-2 | ids 0..11, 294..299, −1 and `0x7FFFFFFF`, both directions: **no arm is selected and nothing is written** (the unsigned bound) |
| `I3_shared_arm_does_nothing` | I-3 | all 56 ids reach `001D4BFA` and **write nothing** |
| `dispatch_selects_the_table_arm` | I-1 | for every id 12..293 the jump lands on `table[id − 12]` |
| `I4_float_steps_observed` | I-4 | from a zero start, the value a float-stepping arm writes is its step. **56 arms step by exactly 0.01**, then 0.1 (7), 0.02 (7), 0.001 (6), 0.05 (5), 1.0 (4), 0.005 (4), 0.03 (3), 0.005556 (2) |
| `postcondition_observed` | postcondition | of the 282 ids, 219 complete under the fixture. They split into 56 no-ops, 3 other arms that write nothing, 41 that write **only the settings object**, 12 that write only `PostProcessParamContext`, and 107 that write other globals or several places. 63 stop at an unplanted object or a trapped import (listed per id in `result.json`) |

`result.json` carries the per-id table: label, arm, and for each direction completion, write destinations, float
values and the stop point.

## What the execution adds to the contract

1. **I-4 holds at runtime, not only as a constant count.** The hundredth is the step of 56 arms. Two runtime steps,
   **0.005** (4 arms) and **0.005556** (2 arms), are not in I-4's literal table. They are computed values, not loaded
   constants, and a reimplementation copying the constant table would miss them.
2. **The postcondition's "moved one value in the settings block" is narrower than the arms.** Only 41 of the 160
   writing arms confine themselves to the settings object. The rest write the post-process context (the contract's
   "33 arms" relationship) or other globals, for example `02CB8148` / `02CB8150` for ids 30 / 31.
3. **I-2 and I-3 are confirmed by execution.**

## Not covered

- the 63 arms that reach loaders, iostreams or objects not planted;
- the renderer `001CD0E0` and the other contract entries (`001A9930`, `00193D50`, `001DF340`), except as reached by
  arms;
- a live game.
