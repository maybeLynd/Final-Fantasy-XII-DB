# S-22: the step table's two entries and the element-scaling stage executed as shipped code (OPUS, 2026-09-25, block 311)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
- S-22's runtime cell is NOT MET.
- `CONTRACT-formula-step-table.md` §13 and `CONTRACT-environmental-element-scaling.md` §13 both read "None".
- `CONTRACT-preparation-step-family.md` is already differential-tested (its §13). `CONTRACT-weapon-recipes.md`
  (`00385F60`) is **not executed here**.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image. **No application stub and no import.**
- **Allowed set: 19 functions**, made of:
  - the static closures of `0038AAF0`, `0038D280` and `0038B220`;
  - the bodies reached by jumps that `edges.tsv` does not follow: the finalize's conditional tail jump to `00387B00`
    (`0038D32D`), and the getters behind the one-instruction thunks `00321490` → `00263E10`, `003214A0` → `00263E20`
    and `003210E0` → `00263DD0`;
  - the shipped MT19937 behind `00379CD0`.
- **Steps are called through the shipped step table** at `01EFA5C0` (`stepTable[id]`).
- **Fixtures** are planted data only: both combatants' stats blocks, the caster context, the unit table, the action
  table and id, the environment globals and the terrain table.

**9 / 9 pass, and `result.json` is byte-identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `ST1_ST2_ST3_ST5_table_static` | §12 (read from the mapped image) | 202 slots, 152 distinct, 42 no-ops, **seven** multi-id targets, `[113] == [125] == 0038D280`, `[65] == 0038AAF0`, `0016D6A0` = `c2 00 00` |
| `ST3_noops_execute_and_write_nothing` | ST-3 | all 42 no-op ids execute and write nothing |
| `ST4_ST7_recipe_65_113` | ST-4, ST-7 | **prep (id 65) writes exactly `02AEE054` / `58` / `5C`**, plus the generator's own state on its lazy first seed. **It draws the shared MT19937 once**; the draw equals an independent MT19937(5489). The finalize (id 113) writes `02AEE004` = **`trunc((058 − 05C) × 054)`** (461 for the fixture) |
| `ST4_finalize_reads_only_the_scratch` | ST-4 | three different attacker / target pairs with one scratch record give **the same output** (200 = (120 − 40) × 2.5) |
| `ST4_order_is_the_semantics` | ST-4 | finalize-then-prep computes from the zeroed scratch, and the later prep does not revisit it (observed) |
| `ST5_double_finalize` | ST-5 | ids 113 then 125 run the same body; the second pass recomputes the same value from the unchanged scratch (observed) |
| `finalize_arms_observed` | (observed) | a negative `058 − 05C` writes 0. `[02AEDFCC]` set writes −1 and `02AEDFC0 = 1`. The value lands in `02AEE004` or `02AEE008` by `[02AEDFD0]` and ctx `+8` bit `0x1000`, and **`00387B00` (MarkTargetHistoryBit) runs only when it lands in `02AEE008`** |
| `WE4_WE5_bit16_skips_the_stage` | WE-4, WE-5, §12 | bit 16 on the target's mutable byte (`+0x6A`), its derived byte (`+0x7A`) or the caster's merged bitmap (`+0x1C`) **skips everything**: nothing is written and nothing else is entered. With none set, the same action scales |
| `WE2_WE6_rule_table` | WE-2, WE-6 | the executed rule table (below). The writes are the scratch scale `02AEE054` **and a cached unit pointer at `02EBF188`** (qword) |

### The executed element rule table (element × environment class × MWeather class × target terrain class)

All 288 combinations were run (6 elements × 4 × 3 × 4). A factor applies when the condition holds, and two factors
compose (0.5 × 1.2 = 0.6):

| element | ×0.5 | ×1.2 |
|---|---|---|
| Fire | environment 0 | MWeather 2 |
| Lightning | – | environment 0 **or** terrain 0 |
| Ice | – | environment 2 **or** terrain 2 |
| Earth | terrain 0 | environment 1 **or** terrain 1 |
| Water | MWeather 2 | environment 3 **or** terrain 0 |
| Wind | – | MWeather 2 |

The constants are read from the image: `0.5` at `01CEBB70`, `1.2` at `008FCC90`.

## What the execution adds

1. **The element rule table itself.** Neither the contract nor its page lists it. WE-2's "three independent inputs,
   multiplied in sequence" holds: the 0.6 cells are the composition.
2. **WE-6 is not the whole write set.** The stage also stores the target's unit pointer to `02EBF188` (`0038B30F` and
   four more sites), a global the contract does not name.
3. **The static call graph misses these bodies' real reach.** `edges.tsv` gives the finalize a one-function closure
   and the stage no getter, because the reach runs through a conditional tail jump and three thunks. The harness
   allows them explicitly.
4. **The finalize's output routing is observed**, including when the history-bit call runs. It is not a contract
   claim.

## Not covered

- `CONTRACT-weapon-recipes.md` (`00385F60`, a 2,302-byte body with a 38-function closure);
- the interpreter that walks recipes;
- the 150 other step targets;
- a live game.
