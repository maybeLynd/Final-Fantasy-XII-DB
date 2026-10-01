# S-46: I4 executed — the shared LCG is seeded with the count of areas entered (OPUS, 2026-09-25, block 336)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-46's exposure note (block 295) found no
application stub on any RNG invariant, and **one invariant unexecuted: I4, the area-count seeding**, of
`CONTRACT-which-generator-serves-which-roll.md`. This harness executes it on the shipped area init `002342F0` and the
shipped draw `00328370`.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 335. `002342F0` runs as
shipped with no application stub, five times in a row, with the master flag `d[02089300]` set to 1, 1, 0, 1, 1. After
each run the shipped draw `00328370` is called three times.

**Stop boundary** (recorded, nothing substituted): `00239960`, the first call after the seeding and the battle-flag
reset. From there the area init re-initialises the party's spawn records (`0023AC80` → `00327DE0`), which is S-14 /
S-17's machinery and needs party data this world does not hold.

The counter `0208E6B0` starts at the image's 0, and the harness never writes it. Before each run the LCG state is set
to `0xDEADBEEF`, so a skipped seeding is visible.

**2 / 2 pass, and `result.json` is byte-identical over three runs** (md5 `d73e568ffd33e593c8377118545db150`).

| case | contract item | observed |
|---|---|---|
| `I4_area_count_seeding` | I4, §7 | From counter 0, each area init with the master flag set seeds the LCG with the **pre-increment count, 0, 1, 2, 3**, and stores count + 1. With the flag clear the init returns at once: **no seed, no count** (the LCG keeps `DEADBEEF`, the counter stays 2). After every run the draws equal the contract's three-step XOR recurrence from that seed |
| `I4_same_count_same_stream` | I4, §9 | The stream depends only on the count: seed 1 reproduces run 2's draws, and seed 2 does not |

For example, seed 0 gives the first draws 1012484, 1716955679 and 1792309082, both from the model and from `00328370`.

## What the execution adds

1. **I4 is executed**, so all of S-46's invariants now have execution. The seed is the number of flagged area inits
   since process start, pre-increment, and the master flag gates both the seeding and the counting.
2. **§7's draw recurrence is checked against the shipped draw.** It uses the ANSI constants, takes three steps per
   call, and assembles 11 + 10 + 10 bits with XOR.

## Not covered

- the rest of the area init after the seeding (spawn and party re-initialisation, S-14 / S-17);
- I4's "never reset", which is a static census (the counter has exactly two touching instructions);
- a live game.
