# S-30: the bazaar's refresh, purchase and script-set over the shipped goods table, stub-free (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** S-30's cell says the bazaar contract's bit-0 invariant and FZ-3 *"rest on the 2026-09-12 refresh execution
+ EXP-092's stubbed callees"*.
- **EXP-092's own header says "STUBBED (disclosed): none."** It plants the registry, the family tables and the flag
  array.
- This closer uses **the shipped goods table** and **the storage the shipped rebase binds**. Nothing of the table is
  planted.

## What was run

`check.py` runs over block 348's world (`../s32-opus-replay-level-advance/check.py`, imported: its cases run first, and its
`result.json` md5 `82259cd6…` is unchanged):
- The shipped `battle_pack` binding supplies the bazaar registry `[02EBF058]` (**128 goods rows, stride `0x24`**) and the
  battle-state block `[02EBF190]`.
- The inventory descriptors are bound by the **shipped rebase `0030B6A0`** over that block.
- Every tally is written through the **real mutate `003008A0`** (the byte channel, r9 = 3) and read through the query
  entry `00309F30`.
- **No application stub.**

**The shipped table holds 106 one-time rows with thresholds, 15 repeatable rows and 7 script-only rows** (`+0x14` bit 1)
**with all-zero thresholds.** Rows used:
- row 0: one-time, loot `0x205C` ×2;
- row 87: repeatable, loots `0x20CA` ×2 and `0x20C8` ×3;
- row 99: script-only, zero thresholds.

**12 / 12 pass, and `result.json` is byte-identical over two runs** (md5 `4e6d794bda816e25ff91e673bc3ae282`).

| case | contract item | observed |
|---|---|---|
| `shipped_registry_and_rebase` | — | 128 rows, stride `0x24`, and the rebase returns. Rows 0 / 87 / 99 carry the flags above |
| `refresh_with_zero_tallies_unlocks_nothing` | clauses 3, 4 | the refresh over all 128 rows sets no flag bit |
| `clause4_met_sets_both_bits_on_that_row_only` | clause 4, `flag |= 3` | row 0's tally is set to 2 through the mutate. The refresh sets **both bits** on row 0 and changes no other row |
| `clause2_already_available_is_left_alone` | clause 2 | refreshing again leaves row 0's flag as it is |
| `purchase_clears_bit1_keeps_bit0_zeroes_the_tallies` | §7, bit 0 | `0030B180(0xD000)` returns 1. The flag goes to **`1`**, and the tally is **0** |
| `clause1_one_time_row_stays_unlocked_but_unavailable` | clause 1 | with row 0's tally earned again, the refresh **rejects** it (the flag stays `1`) |
| `repeatable_row_re_unlocks_after_purchase` | clause 1 | row 87: `3` → purchase → `1` → tallies earned again → refresh → **`3`** |
| `clause3_zero_threshold_row_never_unlocks_by_refresh` | clause 3 | row 99 (all thresholds 0) stays `0` after the refresh |
| `script_set_writes_bit1_only_and_keeps_bit0` | §7 script-set | row 99: set 1 → `2`; set 0 → `0`; with bit 0 planted, set 0 → `1` (**bit 0 kept**) |
| `script_set_needs_the_rows_bit1` | §7 script-set | row 0 (no `+0x14` bit 1): script-set changes nothing |
| `bit0_never_cleared_by_refresh_purchase_or_script_set` | the invariant | across the whole sequence, rows 0 and 87 keep bit 0 |
| `purchase_gate_refuses_an_id_past_the_table` | §7 step 0 | `0030B180(0xD000 + 128)` returns 0 and no flag changes |

## Not covered, and one risk recorded in the contract

**FZ-3's save round trip is not executed.** A new §14 item in the contract (OPUS's own) records that the inventory
rebase `0030B6A0` masks all 128 flag bytes with `0xF8` (clearing bit 0) and zeroes the tallies. It also records that
**on a valid restored image the rebase does not run**: `00280140` validates the runtime header (`00255260`, magic
`0x0131F3EA`), and a valid header skips the reset `002EF650` (`00280379 jne 002803B8`). So FZ-3's first mechanism holds on
load, statically.

The "bit 0 is never cleared **anywhere**" universal is a static census claim. What is executed here is that the three
family writers keep it.
