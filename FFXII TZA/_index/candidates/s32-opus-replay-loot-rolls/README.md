# S-32: the loot rolls executed over a shipped foe against an independent LCG model (OPUS, 2026-09-25, block 349)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
[`CONTRACT-loot-rolls-and-the-chain.md`](../../../13-Rewards-Progression-Economy/CONTRACT-loot-rolls-and-the-chain.md) §13
reads *"None of this subsystem's bodies is executed by an experiment."* This harness runs the orchestrator
`Loot_RollDropEntries` (`003180F0`) and its roll bodies:
- slot `003185D0`;
- quantity `003186F0`;
- extra `00318510`;
- profile `00318820`.

It runs them over definition 1 of `grm_e.ard` (slots `2074` / `202B` / `2074` / `2033`, the same id in slots 0 and 2):
- the file is bound by the game's binder `003EA710`;
- the foe is installed by the shipped installer `0023A570`.

Every draw is checked against an independent model of the shared gameplay LCG.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 344. **No application stub
and no stop boundary.**

**Fixtures:**
- six idle objects at `0x76300000`;
- the unit pool with the foe;
- the LCG state `022C256C`, the chain rank `022C3158` and the profile switch `022C3164`, where a case sets them;
- a `0xAB`-filled output buffer of seven 8-byte entries.

400 kills are run on one continuing stream.

**6 / 6 pass, and `result.json` is byte-identical over three runs** (md5 `a9ca574a6a2c838d1236aa3828d11cbd`).

| case | contract item | observed |
|---|---|---|
| `LC1_LC3_one_stream_three_steps` | LC-1, LC-2, LC-3 | All **1,881** writes to `022C256C` (1,600 by the slot roll, 281 by the quantity roll) are **exactly three steps** (`x·0x41C64E6D + 0x3039`) after the previous write. It is one stream, three steps per draw, whichever inlined copy draws |
| `LC4_variable_draws` | LC-4 | One draw per non-empty slot (4), one more per kept slot. The per-kill total ranges over **4 / 5 / 6 / 7** with the outcomes |
| `LC7_prefill_and_bucket_plus_one` | LC-7 | See the LC-7 list below |
| `merge_duplicate_slots` | (new) | See "What the execution adds", item 1 |
| `LC6_rank_is_the_default_profile` | LC-6 | With `022C3164` = 0, every slot roll receives the chain rank `022C3158` (0 / 1 / 2 / 3) as its profile. With it > 0, `00318820` runs first and makes the kill's first draw |
| `extras_not_reached` | LC-4 (extras) | Both extra-item calls return **without drawing** in every kill. See the note in "What the execution adds", item 2 |

**LC-7.** Over the `0xAB` fill, every entry ends as either a valid item with quantity ≥ 1 or exactly `{FFFF, 0}`. Each kept
slot's stored quantity is its bucket, read before `inc eax` at `00318225`, plus one. Every bucket seen was 0, with the kill
counter `022C3160` at 0.

## What the execution adds

1. **Duplicate item ids are MERGED after the rolls.**
   - A pass at `003182A0`–`003182D5` walks the entries from the last back to the first.
   - It adds any entry's quantity into the **earliest** entry with the same id, and clears the later one to `{FFFF, 0}`.
   - Measured on grm_e def 1: in **11** of the 400 kills both slot 0 and slot 2 (id `2074`) were kept. Entry 0 then holds
     quantity 2 and entry 2 is empty, in every case.
   - LC-7's "seven fixed entries … a slot that never rolls is left explicitly empty" is true of the pre-fill. **A kept slot
     can also end empty, when an earlier entry absorbs it.**
   - Static census of the shipped `in` area files: **12** definitions repeat a slot id, and **27** carry an extra whose id
     repeats a slot.
2. **An extra item's roll needs the player to own its condition item.**
   - `00318510` asks `0030B0E0(condition)`, which dispatches through the inventory descriptor table `01EEBCC0` by family
     (`id >> 12`) to the family's count getter `+0x50`. The conditions here are `0x806A` / `0x806C`, family 8.
   - With no owned condition item the extra never draws, which is LC-4's third guard.
   - This world does not build the family storage, so the extra-item draw itself is not covered.

Routed to FABLE (the merge pass; LC-7's wording; §13 can cite this block).

## Not covered

- the extra-item draw (needs the inventory family storage);
- quantity buckets above 0 (the kill counter `022C3160` stayed 0);
- the chain (`00317ED0` / `003183D0`) and the periodic draw `00319530` (LC-5);
- the fallback keep through `0017D340` (LC-6's second route) as a separate case;
- a live game.
