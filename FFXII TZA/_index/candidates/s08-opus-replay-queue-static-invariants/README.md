# S-08: the request queue's four "static" invariants executed as shipped code (OPUS, 2026-09-25, block 330)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** `CONTRACT-resource-request-queue.md` §13's owner
verdicts (2026-09-25) left four invariants **standing as static**: I1 (the constructor's field list), I4's counter wrap,
I6 (offset truncation) and I7 (recycling does not sanitize). This harness executes all four on the shipped bodies.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from block 328. These bodies run as shipped: the
constructor `0032E450`, the requester `0032E870` (its fifth and sixth arguments on the stack) and the recycler
`0032EC40`.

There is **no application stub and no stop boundary.** No case lets the free list run dry, so the requester never
enters its pump / pacer stall. A hook on the pump `0032E070` confirms it is never entered; I3 is replay-confirmed
elsewhere.

**Fixtures:**
- two dirty fills of the pool `022C31C0`;
- the counter `01EED498` where a case sets it;
- request descriptors `{+0 offset, +8 argument, +0x10 completion, +0x18 cancellation}`.

**4 / 4 pass, and `result.json` is byte-identical over three runs** (md5 `73bbd63bd14d2ed6551bf9ba8e18731f`).

| case | contract item | observed |
|---|---|---|
| `I1_constructor_field_list` | I1 | Over pools filled `0xAA` and `0x55`, `0032E450` changes **only** these bytes in every slot: `+0x10..+0x21` (links, then the zeroed word at `+0x20`), `+0x28..+0x2B`, `+0x58..+0x5B` (= the slot index) and `+0x64..+0x67` (= −1). Every other byte survives |
| `I4_counter_wrap_signed` | I4 | Counter `0xFFFFFF` gives id `3FFFFFC0` (`(0xFFFFFF << 6) + slot` in 32 bits); the counter resets to 1, and the next id is `0x41`. A corrupted `0x7FFFFFFF` gives id `FFFFFFC2` and counter `0x80000000`; `0x80000005` gives id **`0x143`** and counter `0x80000006`. The compare is signed (`cmovg`), not a clamp |
| `I6_offset_truncates_toward_zero` | I6 | The slot's `+0x2C` is the descriptor offset truncated **toward zero** to a `0x800` multiple: `0x1234`→`0x1000`, `0x7FF`→0, −1→0, `−0x7FF`→0, `−0x801`→`−0x800`, `−0x1234`→`−0x1000`, `0x7FFFFFFF`→`0x7FFFF800`, `−0x80000000` unchanged |
| `I7_recycle_does_not_sanitize` | I7 | `0032EC40` changes only the recycled slot's next link (`+0x10`), its id (`+0x64` = −1) and the neighbour's previous link (`+0x18`). The argument, kind, index, byte count, offset, both callbacks, the destination and an unobserved planted qword at `+0x68` all survive |

## What the execution adds

1. **I1, I4's wrap, I6 and I7 move from static to executed.** Together with §13's replay-confirmed I2, I3, I4-encoding
   and I5, every one of the contract's seven invariants is now executed.
2. **I4's corrupted-counter domain is concrete.**
   - A counter at or above `0x80000000` never resets. The signed compare keeps it.
   - It produces ids that are **negative** (`0x7FFFFFFF` → `FFFFFFC2`) or that **alias normal ids**: counter
     `0x80000005` yields `0x143`, the id counter 5 yields for the same slot.

   This is about corrupted input only, as the contract says. Normal construction starts the counter at 1.

## Not covered

- the pump's I/O path (external completion);
- a live game.

## I2 and I3 executed (OPUS, 2026-09-26)

`i2i3.py` runs over this harness (imported unchanged; its cases run first). The constructor, requester and recycler run
as shipped, and for I3 so do the pump `0032E070` and the whole stall.

**I2: every slot is on exactly one list.** The lists are the free list (head `022C51D0`) and the pending list (head
`022C51C0`, tail `022C51C8`; links `+0x10` / `+0x18`), walked after each step. The pending counts run 0, 3, 4, 3, 2, 1
through these steps:
- construction;
- three enqueues with flag 0, which insert at the **head** (pending `[2, 1, 0]`);
- one with flag 1, which inserts at the **tail** (`[2, 1, 0, 3]`);
- recycling a middle, the head and the last slot.

At every step the two lists are disjoint and cover all 64 slots.

**I3: no slot means a blocking retry.**
- **Setup.** All 64 slots hold zero-byte requests. A 65th request enters the stall: the pump runs once and drains all
  64 itself, then the pacer, then the free-head re-test.
- **Result.** It returns id `0x1040` (slot 0), leaving the lists at 63 free / 1 pending, still disjoint.
- **Declared fixtures:**
  - *Pacer OS bridges:* `GetCurrentThread` returns the pseudo-handle −2; `Get/SetThreadPriority`, `SwitchToThread` and
    `Sleep` return non-blocking values. These are named, like `world.py`'s `OSRET`.
  - *Concurrent producer:* the pacer spins at `0035EBB0` until the frame counter `[022CA5E0]` reaches a target, and in
    the game the frame thread advances it. A hook at that poll advances it by one per poll (one poll was needed). That
    is the other thread's effect; no shipped instruction is changed.

**Not covered:** the pump's real I/O path (these requests have zero bytes). I5 is below.

**Runs.** 2/2, and two runs give an identical `i2i3_result.json` (md5 `14d420406940c2ea260cf8a75e86b87b`).

## I5 executed: chunking is gate-dependent (OPUS, 2026-09-26)

`i5.py` runs over this harness (imported unchanged). It drives the chunk-aware enqueue `0032E620(kind, id, dest, bytes,
desc)`, its gate `003EB0D0` (is a BGM stream active: byte `+0x31` of the stream descriptor `02B5E0E0`) and the requester, all
as shipped. The pool is filled with `0xAA` before construction, so the slot fields the constructor leaves alone (`+0x30`,
`+0x34`) carry a known pattern.

| case | slot after the enqueue |
|---|---|
| gate clear, `0x123456` bytes | part `+0x28` = `0x123456` (whole); chunk `+0x22` = 0; cap `+0x30` / remaining `+0x34` still `AAAAAAAA` |
| gate set, `0x123456` bytes | chunk 1; cap `0x80000`; remaining `0x123456`; first part `0x80000` |
| gate set, `0x1000` bytes | chunk 1; cap `0x80000`; remaining `0x1000`; first part `0x1000` |
| gate set, null descriptor | the local descriptor is zeroed; still chunked (cap `0x80000`, remaining `0x123456`) |

**Runs.** 4/4, and two runs give an identical `i5_result.json` (md5 `08d9f1ce79f3cc04950b4e851441ba94`).

## The pump's state machine, section 7, executed row by row (OPUS, 2026-09-26, `pump_states.py`)

AUDIT-SEM's S-08 cell keeps one item open: *"the pump's real I/O path"*. `pump_states.py` imports `check.py`, whose
cases run first and unchanged. It then drives the pump `0032E070` through every row of the contract's §7. **No
application stub.**

**What the pump reads of the outside world**, measured from its callees:
- **The device word.** The in-flight getter `0046DFE0` returns 2 when `[0215EFF4]` is −1. The result getter `0046E0E0`
  returns that word, and its sign picks state 5 or 6.
- **The issue.** Issuing goes through `0046E030` → `002DF780`, the file layer (open, async read, close). This is the
  *"external read behavior"* that §7 and §9 set apart.

**Planted data only:**
- The file entry for (kind `0x24`, index 3) is planted **absent** (−1 at `02F73B6C`). So `002DF780` returns at
  `002DF7B9` without a file call, and `0046E030` still reports the issue accepted.
- Completion is the planted device word. The time is the frame counter `[022CA5E0]` = 1000.
- The request's callbacks (`+0x40` done/error, `+0x48` cancel, `+0x50` part) are small recording functions, the
  "scripted external responses" of §9.

**8 / 8 pass; `pump_states_result.json` is byte-identical over two runs (md5 `32bc3d9c…`).**

| case | §7 row | observed |
|---|---|---|
| `S1_issue_stamps_time_then_2_then_3_and_waits` | 1, 2, 3 | one issue: `+8` = 1000, then state 2 (`+0` += the second reading = 1000), then state 3. With the device in flight the pump returns, **the request still at the head** |
| `S5_delivered_calls_done_with_1_and_recycles` | 5, chunk 0 | device `0x1000`: `+0x40(0x77, ctx, 1)`, state 0, the slot recycled |
| `S6_failed_reports_only_when_part_is_minus1` | 6, chunk 0 | device −5: `+0x40(0x77, ctx, 0)` **only when `+0x28` = −1**; with `+0x28` = `0x1000` there is no call. Recycled either way |
| `S4_cancel_zeroes_count_only_with_a_callback` | 4 | with a cancel callback, `+0x48(0x77)` runs and `+0x28` is zeroed. **Without one, `+0x28` keeps `0x1000`.** Recycled either way |
| `C1_part_1_requeues_with_min_cap_aligned_offset_state1` | 5, chunk 1, part returns 1 | remaining `0x100000` − `0x80000`; offset and destination advance. The requeued part, captured when it is re-issued, has state 1, progress 0, `+0x28` = min(cap, remaining) = `0x80000`, offset `0x90000` (aligned down to `0x800`) and accumulator 0. **The same pump call then carries it through 1 → 2 → 3 → 5 and retires it**, as §9 says one pump can |
| `C2_part_2_keeps_state5_and_reprobes_without_subtracting` | part returns 2 | progress 2, state 5 kept. The next pump re-probes the part callback first, and the remaining count is **not** subtracted again |
| `C3_part_3_is_not_a_release_the_next_pass_subtracts_again` | part returns 3 | progress 3, state 5. The next pump **subtracts the previous part again** (`0xC0000` → `0x80000`) |
| `CE_last_part_calls_done_and_recycles` | 5, chunk 1, remaining ≤ part | the done helper, then recycle |

**Not covered:** the file layer `002DF780` and below (open, async read, close), which is the external read itself.
