# S-19: the separation pass executed as shipped code — P-1..P-7, and P-3 corrected (OPUS, 2026-09-25, block 337)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-19's exposure note (block 302) found that the
separation pass (P-1..P-7) was unexecuted; `CONTRACT-separation-pass.md` §13 says *"No experiment executes these six
bodies"*. This harness executes all six.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from block 336. The world runs the body-pool
initialiser `003DAE30`. `world.py` gains faithful named bridges for the CRT's double `sqrt`, `_isnan` and `_finite`,
which the resolver imports.

**Bodies** are allocated by the shipped pool allocator `003DA8A0` and registered by the shipped `003DB020`. Each tick
is the shipped sequence: reset `003DAA40` → registration → the pass `003DAC70(00314F30)`, which runs the pair set
`003DAAB0`, the visit `003DAB50` and the resolver `00314F50`. The clear `003DA9F0` runs directly. **No application stub
and no stop boundary.**

**Fixtures:**
- the bodies' authored fields: layer, weight, position, heights, radii, masks, owner;
- the registration radii;
- the two globals `02B40530` / `02B40534`, whose conjunction `003B7730` gates the registration's cell step.

**8 / 8 pass, and `result.json` is byte-identical over three runs** (md5 `82885e5ee3da0cab97c5a836d79104d0`).

| case | contract item | observed |
|---|---|---|
| `P2_each_pair_once` | P-2 | Three mutually overlapping bodies: the resolver runs for (0,1), (0,2) and (1,2), **once each** |
| `P5_order_dependent` | P-5 | The first pair sees zero accumulators. **A later pair's resolver entry already holds a push written by an earlier pair in the same pass** |
| `P1_unregistered_not_active` | P-1 | After the reset, a body that did not register has `+7` = 0 and no cell bit |
| `P3_remembered_pairs_visited_only_under_candidates` | P-3 | See below: **the contract's P-3 holds only in part** |
| `P4_mode_selects_active_test` | P-4 | With B not active: push mode (1) refuses; **query mode (0) skips the active test** and the pair resolves |
| `P4_layer_and_owner_refusals` | P-4 | Different layers refuse; equal non-zero owner bytes refuse; two zero owners do pair |
| `P7_three_weight_outcomes` | P-7 | Equal mask bytes share the push (−0.75 / +0.75), and **both** contact counters advance with both immovable markers clear. A strictly greater or smaller mask byte puts the **whole** push (1.5) on one body, and advances **that body's** counter and marker only |
| `P6_clear_extent` | P-6 | `003DA9F0` zeroes exactly `+0xE8..+0xEE` and `+0x100..+0x10B` |

### P-3, measured

P-3 says the visit walks *"the candidate bits **and every bit still set in the body's own `+0x18`**"*, so *"a contact is
retried next tick even after the two bodies stop sharing a cell"*.

The shipped visit `003DAB50` walks the **candidate set**, byte by byte (`003DAB94`–`003DAC48`):
- It skips a zero candidate byte, or a zero qword, entirely.
- Inside a non-zero candidate byte it steps bit by bit **only while candidate bits remain** (`shr rbp, 1` / `jne`
  at `003DAC11`).
- At each step it calls the resolver if the candidate bit **or** the remembered bit is set (`003DABCF`–`003DABDD`).

Measured:

| case | calls | A's remembered bits after |
|---|---|---|
| (a) remembered B, no candidate | **none** | B's bit **persists** (`2`) |
| (b) remembered B below candidate C, in the same byte | (A,B), then (A,C) | B dropped (refused: not active), C kept (`4`) |
| (c) remembered C above the only candidate B | (A,B) only | **C is never visited and persists** beside the new pair (`6`) |

So **a remembered pair is retried only when a higher candidate bit lies in the same byte**. Otherwise it is neither
retried nor forgotten, and a stale bit can persist indefinitely.

In (b), the walk also **initiates from an unregistered body still on the allocated list**: B, carrying last tick's cell
bits, gets C as a candidate, and the resolver refuses (B, C).

## What the execution adds

1. **P-1, P-2, P-4, P-5, P-6 and P-7 are executed.** In particular P-5's order dependence (the contract's "single most
   important thing") is observed at the resolver's entry.
2. **P-3 is corrected by execution**, as the table above shows. Routed to FABLE.
3. **P-7's one-sided outcomes put the whole separation on one body**, and that body's counters record it.

## Not covered

- the consumption of the push by the integrator (`002E5180` / `002E5380`), P-6's other subsystem;
- the cell geometry of `0046AD20` beyond this world's (all bodies land in all cells);
- a live game.
