# S-20: the combo roll executed with the real gameplay MT, against an independent model (OPUS, 2026-09-25, block 346)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
[`CONTRACT-combo-continuation.md`](../../../07-Combat-Action/CONTRACT-combo-continuation.md) §13 reads *"None. No experiment
executes these three bodies."* This harness runs the roll `BattleFormula_RollAndStoreComboCount` (`00388660`). It is
checked against an independent MT19937 model of the body's instructions.
- The gameplay MT is seeded by the shipped seeder `00379CF0` → `00863D30` and drawn by `00379CD0` → `00863BF0`, as in block
  339.
- The foe case uses a foe installed by the shipped installer from `rsn_b.ard` (block 343).

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 345. **No application stub
and no stop boundary.**

**Fixtures:**
- six idle objects at `0x76300000`;
- unit 0, a party member owning battle-state row 0 (`+0x24` max HP, `+0x48` HP, status words, `+0x6B7` the counter);
- unit 1, a foe installed by class 1;
- a context whose `+0x10` object holds the continue flag (`+0x18` bit 1).

**The percent gate `[02AEDFE4]`** is 0 as the world leaves it, so no combo would ever start. It is set to 60 and 100 per
case and then restored. What sets it in the game is not claimed.

**4 / 4 pass, and `result.json` is byte-identical over three runs** (md5 `c6a877ca5cddd5dfec3bb79f1306dd99`), MT seed
20260925.

| case | contract item | observed |
|---|---|---|
| `CB3_first_hit_draws_twelve_not_two` | CB-3, §12 | See the CB-3 list below |
| `CB3_count_rises_as_hp_falls` | CB-3 (new detail) | See the HP-band list below |
| `CB4_progress_against_the_nibble` | CB-4, §12 | Counters 1 and 2 against nibble 3 continue; counters 3 and 5 end. **No case draws the generator** |
| `CB5_foe_record_table_and_cap` | CB-5 | See the CB-5 list below |

**CB-3, first hits.** 60 rolls (counter 0) at gate 60, cycling six HP / status cases.
- **Every flag, nibble and draw count matches the model**: 37 combos and 23 misses.
- A first hit that passes the gate draws the generator **12** times; one that fails draws **once**.
- The low nibble of `+0x12` survives.

**The HP bands.**
- The per-hit probability is **8 / 16 / 32 / 64 %**, as current HP falls below max/4, max/8, max/16.
- Status bit 28 doubles max. Status bit 16 compares HP with itself, so the probability is always 8 %.
- Counts observed: 1 at full HP, 1–3 at 240/1000, 3–9 at 120/1000, 7–9 at 50/1000.

**CB-5, a foe record** (stats `+5` = 1):
- The nibble is written at **`0208DE80` + unit`[+0xEA9]`×0x40**. The party table entry is untouched (`0xEE` survives).
- The count is capped at class`[+0x20]` − 1 = 1. The uncapped model gives 7–8 for the same draws, so the cap binds.
- All 12 rolls at gate 100 match the capped model.

## What the execution adds

1. **CB-3's "draws the generator TWICE" counts call sites, not draws.**
   - The second site, `003887E3`, is inside an **11-iteration loop** (`r14d = 0xB` / `rbp`, `00388803`–`00388807`).
   - So a first hit that passes the gate makes 1 + 11 = **12** draws, and one that fails makes 1.
   - The count is **1 + the successes of those 11 Bernoulli draws**, capped at 11.
2. **The first draw is a percent gate.** `draw % 100 < [02AEDFE4]` (`00388716`); failing it ends with no combo. Its world
   value is 0.
3. **The per-hit probability is an HP band.** 64 / 32 / 16 / 8 % below max/16, /8, /4, and otherwise
   (`00388723`–`003887D6`). Status bit 16 (`0x10000`) replaces max with current HP, and bit 28 doubles max. The statuses'
   names are not claimed.
4. **CB-5's record table is the party one; foes use another.** The per-kind record is `0208D480 + rec[+4]×0x40` only for a
   party record. A foe's is `0208DE80 + unit[+0xEA9]×0x40` (`003886CF`–`003886E1`), and its count is capped by the class
   record's `+0x20` (`00388845`–`0038884D`).

Routed to FABLE.

## Not covered

- the continue `0030FA00` (CB-2, CB-6), which re-commits through `BattleUnit_CommitAction`;
- the reset `003105D0`'s combo-field clear (CB-1's word store);
- the two globals zeroed at `003888A1` / `003888AB` when the flag is set;
- a live game.
