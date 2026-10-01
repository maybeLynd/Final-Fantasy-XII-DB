# S-48: the authored ramp channels executed as shipped code; the delta is a reciprocal product (OPUS, 2026-09-25, block 321)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-48's exposure note (block 301) found every invariant
of `CONTRACT-authored-command-ramp-channels.md` **unexecuted**. This harness runs all six entries in one persistent world.

## What was run

`check.py`, with `world.py` from blocks 318 / 319:
- **The world.** `world.py` now also has **`Session`**: build the world once, then call shipped functions in the same
  memory with the same hooks and bridges. There is **no application stub**, and imports go only through named bridges.
- **One allocation is replaced by a fixture.** The reset `003B6890` allocates the 0x8C00-byte table (160 × 0xE0) from
  engine heap 6 (`0036C1D0`, then `0036A100`). That heap belongs to the engine's boot, and its allocator **halts**
  unbuilt (`0036C000: jmp 0036C000`). So `[02B40528]` is planted to a 0x8C00 buffer, and `003B6890` takes its own
  already-allocated path and runs its reset body.
- **Everything else is real:** the four setters, and the per-tick advance over the table.

**All checks pass, and `result.json` is byte-identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `reset_003B6890` | entry | runs to its return over the planted table |
| `P1_identity_guard_writes_nothing` | §4.1 | with a wrong generation in the id, **all four setters** return and leave the 0xE0-byte record byte-identical |
| `P2_steps_zero_is_immediate` | §4.2 | an in-flight 50-step ramp is cancelled: counter 0, value = target |
| `P3_delta_and_no_clamp` / `P3b` | §2, §4.3 | 0 → 0.1 in 3 steps **ends at `0.10000000894`, not 0.1**, with the counter at 0: nothing clamps. The delta for 0 → 0.3 in 3 steps is **`0.10000000894`, the reciprocal product `(target − value) × (1/steps)`**, not `0.10000000149`, the quotient §2 writes |
| `P4_paused_does_not_accumulate` | §4.4 | a paused slot (`+0x41` bit 0), or the global gate `[02B40524]`, leaves counter and value untouched; the next open tick steps once |
| `P5_byte_counter` | §4.5 | 255 steps stores 255 in the byte counter |
| `S2_S3_channel_layout` | §2, §3 | after one tick: classes `0x0D` / `0x0F` move the pairs `+0x50/+0x54` and `+0x58/+0x5C`; `0x0E` moves `+0x70`; `0x10` moves `+0x78`. The fifth channel (`+0x43`, `+0x98`) advances with no setter |

## What the execution adds

1. **§2's formula is off in the last bit.** Every setter computes `1.0 / steps` first (`divss` of the constant 1.0 by
   the byte), then multiplies (`mulss`), for example `003B69CC`–`003B69EC`. `(target − value) / steps` in `f32`
   differs whenever the reciprocal rounds; measured: 0.3 over 3 steps gives `0.10000000894` against `0.10000000149`.
   A reimplementation using the division drifts from the original by one ulp per step.
2. **§4.3 shown by execution:** a ramp's end value is not its target (0.1 over 3 steps ends at `0.10000000894`).
3. **The reset's table allocation needs the engine heap**, whose allocator halts when that heap is not built.

## Not covered

- the engine heap-6 allocation inside `003B6890`;
- the authored-command dispatch that calls the setters;
- a live game.
