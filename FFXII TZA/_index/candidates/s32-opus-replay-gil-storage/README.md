# S-32: gil storage and movement executed as shipped code, with the meter real (OPUS, 2026-09-25, block 347)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
[`CONTRACT-gil-storage-and-movement.md`](../../../13-Rewards-Progression-Economy/CONTRACT-gil-storage-and-movement.md) §13
reads *"None. No experiment executes these bodies."* This harness runs GL-1..GL-5 against:
- the setter `GameState_SetGil` (`00254EE0`);
- the getter `00253690` and its thunk `00309BF0`;
- the console writer `Debug_SetGilToMaximum` (`003058B0`);
- the meter `00316A50`, **real**.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 346. **No application stub
and no stop boundary.**

**Fixtures:** six idle objects at `0x76300000`. `[02092758]` is the game state (gil at `+8`), and `[020927C0]` holds the
meter's counters.

**8 / 8 pass, and `result.json` is byte-identical over three runs** (md5 `46cb73cb3cc8fde9c3db4e4e0f05d22d`).

| case | contract item | observed |
|---|---|---|
| `GL1_clamp_in_the_setter` | GL-1 | See the GL-1 list below |
| `GL2_GL4_meter_kind_and_zero_delta` | GL-2, GL-4 | 100 → 250 meters kind **6** with 150; 250 → 100 meters kind **7** with 150; 400 → 400 calls **no** meter and **still stores** |
| `GL3_delta_before_clamp` | GL-3 | 0 → 200,000,000 meters a gain of **200,000,000** while **99,999,999** is stored |
| `GL2_console_writer_is_metered` | GL-2 | `003058B0` (`mov ecx, 99,999,999; jmp 00254EE0`) from 5 is metered as a gain of 99,999,994, like any writer |
| `GL5_two_getter_entries` | GL-5 | `00253690` and the 5-byte thunk `00309BF0` (`jmp 00253690`) both return the stored value |
| `delta_wraps_to_a_metered_gain` | GL-2, GL-4 (new edge) | 100 → −2,147,483,648 is metered as a **gain** (kind 6) of 2,147,483,548, and **0** is stored |
| `meter_counters_accumulate_and_saturate` | (the meter) | See the meter list below |
| `meter_counters_observed` | (the meter) | Every metered write touches only those two counters |

**GL-1.** Every write lands once at `00254F1F`, clamped to [0, 99,999,999]:
- −5 → 0;
- 100,000,000 → 99,999,999;
- `0x7FFFFFFF` → 99,999,999;
- −`0x80000000` → 0.

**The meter's counters.** Starting from zeroed counters:
- the kind-6 counter at `[020927C0]+0x3860` goes 1,000,000,000 → **`0x7FFFFFFF`**. It saturates and does not wrap.
- the kind-7 counter at `+0x3864` takes 300.

## What the execution adds

1. **The metered delta wraps at the 32-bit edge.**
   - `00254EF1 sub edx, [rax+8]` is 32-bit, so a request of −2,147,483,648 over a balance of 100 yields `+0x7FFFFF9C`.
   - It is **metered as a gain** of 2,147,483,548 while 0 is stored.
   - GL-4's reading "a negative one takes `jle` … `cl = 7`" holds for every delta that does not wrap.
2. **The meter's counters are two saturating dwords.** They sit at `[020927C0] + 0x3848 + kind×4`: `+0x3860` for kind 6 and
   `+0x3864` for kind 7. They accumulate and saturate at `0x7FFFFFFF`. GL-3's "a gained delta far larger than the gil
   stored" therefore accumulates without bound until it saturates.
3. **GL-4 is exact:** a zero delta performs the store with no meter call.

Routed to FABLE (GL-4's wrap edge; §13 can cite this block).

## Not covered

- GL-6's three execution-resource writers (prepare, consume, refund);
- the other ten setter callers;
- what reads the two counters (achievement thresholds; the meter's `.rdata 00D10460` descriptor is read but not analysed);
- a live game.

## GL-6 executed: reserve, commit, give back (OPUS, 2026-09-26)

`gl6.py` runs over this harness (imported unchanged; its cases run first). It executes the three execution-resource
writers as shipped code, with every callee real and no stub:
- **reserve:** `BattleAction_PrepareExecutionResources` `0030EF20(unit, abilityRow)`;
- **give back:** `BattleAction_RefundReservedExecutionResources` `00300280(unit)`;
- **commit:** `BattleAction_ConsumeExecutionResources` `00305640(unit, abilityRow, 0)`.

**Fixtures (planted).**
- A party unit (stats `+5` = 0) with stats `+0x6C` bit 0 set. That is the flag `BattleUnit_UsesGilActionCostChannel`
  (`002F9820`) tests to route the ability's cost to gil.
- The ability is the first shipped `battle_pack` row that `00309060` prices above zero: id 0 (row `+0x0A` = 8, kind
  `+0x1E` = 1), **priced at 100 gil**.
- Gil starts at 1000 through the setter, and the meter counters are zeroed.

| case | asserted |
|---|---|
| reserve | `unit+0xE58` = 100, gil 1000 → 900, the spend counter +100 |
| give back | gil → 1000, `+0xE58` → 0, the gain counter +100 |
| the pair | the balance is unchanged, but **both counters moved by 100**: invisible in the balance and visible twice in the counters, as GL-6 says |
| commit | after a reserve, commit leaves gil at 900, clears `+0xE58`, and meters nothing more |
| after commit | a refund gives nothing back (gil stays 900, gain counter 0) |

**Runs.** 5/5, and two runs give an identical `gl6_result.json` (md5 `7d7050c23643ce7e316a9c40a2f1d04c`).
