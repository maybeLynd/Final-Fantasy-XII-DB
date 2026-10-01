# S-32: the defeat-rewards body executed over shipped foes and shipped party rows (OPUS, 2026-09-25, block 344)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-32's exposure note (block 305 era) covers only the award
contract, and says the other four contracts have no runtime coverage. This harness runs
`BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`, 857 B) against
[`CONTRACT-defeat-rewards-sequence.md`](../../../13-Rewards-Progression-Economy/CONTRACT-defeat-rewards-sequence.md)
DR-1..DR-6.
- **The foes** are installed by the shipped installer `0023A570` (class 1, block 343) from shipped area files, bound by the
  game's binder `003EA710`.
- **The recipients** are three party units on battle-state rows 0–2, found through the real slot maps. Map 0 = {0, 1, 2},
  and maps 1–4 are built by the refresher `003266C0`.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 343. **No application
stub.**

Area files, from `ps2data/plan_master/in/plan_map/…`:

| file | sha256 | gil terms |
|---|---|---|
| `bds_a.ard` | `f52f5dd2…ac9b5d` | def 0: gil 0 |
| `rsn_b.ard` | `41ac8746…bcd992` | def 0: flat 8, per level 3 |

Each file is rewritten fresh before every bind, because the binder relocates its tables in place.

**One stop boundary: the message poster `0046AB10`.**
- It is reached from the gil notifier `00469E80` with event `0x26` for a positive gil delta, and from the level advance
  `0030C650` with event 4 on a level change.
- It leads into the font/painter surface (`001B5FA0` = the text singleton `[01F811F8]`), which this world does not build.
- The run ends there and the arguments are recorded.
- **A zero-gil kill without a level change never reaches it, and `00312280` runs to its return.**

**Fixtures:**
- six idle objects, at `0x76300000` clear of the pool. `[02092758]+8` holds gil and `[020927C0]` is the game-state block.
- the unit pool: unit 0 is the foe, units 1–3 own rows 0–2 (`+4` type, `+0x1C2` level, `+0x18C` EXP, `+0x190` LP);
- a zeroed spawn pool;
- the master flag.

**6 / 6 pass, and `result.json` is byte-identical over three runs** (md5 `a6bdf87ebbb2793408317c171aa43b02`).

| case | contract item | observed |
|---|---|---|
| `DR1_order_to_the_return` | DR-1 | See the DR-1 list below |
| `DR2_null_recipient_calls` | DR-2 | After the loop, `002F8BB0` and `002F90C0` are called with `rcx = 0` (`003124BC` / `003124C6`). EXP(NULL) = **1,253**, the same as each recipient's share, and LP(NULL) = 1. Both go to the presentation call `0028FB80` (edx = EXP, r8 = LP) |
| `DR3_level_walk_is_a_search` | DR-3 | See the DR-3 table below |
| `DR4_gil_reads_the_defeated_units_span` | DR-4 | See the DR-4 table below |
| `DR5_status12_converts_lp_to_gil` | DR-5 | A zero-gil foe, and recipient 0 at level 20 holding id 12 in **either** layer. That recipient receives **no** LP (the others get 1), and the gil accumulator gains 5 × 20 × 1 = **100**. So a zero-gil kill now pays gil and reaches the poster. Without id 12 the same recipient gains 1 LP and the run returns |
| `DR6_report_exceeds_stored_gain` | DR-6 | Old gil 99,999,995 and award 8. The setter `00254EE0` receives **100,000,003** and stores **99,999,999** (a gain of 4). The notifier receives requested − old = **8** and posts event `0x26` |

**DR-1.** bds_a def 0 (gil 0) runs to its return in this first-occurrence order:
1. `00317ED0`, `003171C0`;
2. nine slot lookups (`00320AB0`);
3. per recipient: EXP, LP, the threshold walk, `00316A50` and the advance `0030C650`;
4. EXP(NULL) and LP(NULL);
5. presentation `0028FB80`;
6. gil read, set and notify;
7. `00265020`, then item placement `00319490`;
8. retirement `00317090`.

Each recipient gains **1,253** EXP (3,760 / 3) and 1 LP.

**DR-3.** Each run ends at the poster (event 4) inside the advance, after the walk and after the level store:

| recipient 0 before | threshold calls | advance calls | level after |
|---|---:|---|---:|
| level 10, 250,000 EXP | 23 | **one**, target 32 | 32 (+22 from one kill) |
| level 98, the EXP cap | 2 | one, target **99** | 99 |

**DR-4.** Gil = (foe `+0x1C2` − foe `+0x88`) × `[unit+0xE78]+0x30` + `[unit+0xE70]+0x30` = 8 + 3 × span:

| foe span | recipients' level | gil |
|---:|---:|---:|
| 0 | 10 | **8** |
| 5 | 10 | **23** |
| 5 | 50 | **23** |

Each run ends at the poster with event `0x26`.

## What the execution adds

1. **The gil term reads the DEFEATED unit's level span, not the recipient's level.**
   - §3 lists `+0x1C2` under *recipient*, as *"read by the walk AND by the gil term"*.
   - Measured: the gil term reads `[defeated + 0x698] + 0x1C2 − +0x88` (`0031251D`–`00312532`). Recipient levels 10 and 50
     give the same gil.
   - The recipient's `+0x1C2` enters gil only through DR-5's conversion (`00312415`).
2. **The reward tables are the ARD base and per-level rows.** `+0xE70` / `+0xE78` are the rows block 343 measured: the
   `[02EBF148]` row by `def+0x22` and the `[02EBF140]` row by `def+0x24`. Gil is at `+0x30` and experience at `+0x34`, the
   same shape as the stat main value at `+0x20` (block 342).
3. **A level-up is an external consequence inside the loop.**
   - DR-1 says external consequences "have not been excluded". One is now named: the advance `0030C650` posts event 4
     through `0046AB10` for a level change, while the recipient loop is still running.
4. **Gil is the exception in shipped data.**
   - Static census of the shipped `in` area files: **1,004 of 1,146** definitions have both gil terms zero.
   - For them the event-`0x26` post happens only through DR-5's conversion.

Routed to FABLE (§3's `+0x1C2` reading; DR-1's named consequence).

## Not covered

- the loot branch (`003180F0` / `00319CA0`): `00319490` returned 0 for these foes and cursor state, so no drop was placed;
- the EXP-suppression flag (`00236780` nonzero);
- designated (non-shared) EXP mode and an EXP-doubled recipient (DR-2's other figures);
- everything after the poster on the boundary runs;
- a live game.
