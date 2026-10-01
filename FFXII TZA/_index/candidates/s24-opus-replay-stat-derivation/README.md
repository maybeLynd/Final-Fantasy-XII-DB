# S-24: the stat derivation executed on both paths, over shipped tables and shipped area files (OPUS, 2026-09-25, block 342)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-24's runtime cell is MIXED.
- **EXP-103** ran `002FEF30` with the reset `003105D0` and the sink `00307D10` entry-stubbed, over synthetic registry
  rows.
- **Block 305** analysed that exposure.

This harness runs `BattleStats_RebuildEffectiveStatsAndAffinityState` (`002FEF30`) against
[`CONTRACT-stat-derivation.md`](../../../08-Combat-Formula/CONTRACT-stat-derivation.md) D-1..D-5, D-7 and §12:
- **the party path** over the shipped `battle_pack` tables (bound by shipped code, `shipped_pack.py`);
- **the foe path** over two shipped area files, bound by the game's own binder `AreaArd_BindLoadedRootAndBattleSections`
  (`003EA710`);
- **the reset and the sink real.**

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 341. **No application stub
and no stop boundary.**

The area files come from the shipped extract (`ps2data/plan_master/in/plan_map/…`):

| file | sha256 | definitions |
|---|---|---:|
| `rsn_b.ard` | `41ac8746…bcd992` | 22 |
| `rwf_d.ard` | `7957c1b9…003e34` | 1 |

The `ch` copies of the extract are byte-identical, checked for rsn_b.

**Binding fixture.** Each file sits 0x1000 into its own zeroed mapping, below 4 GB because the binder keeps the buffer in
`ebp` (`003EA732`). `0036C660`, the binder's first call, tests for a heap-block header at `buf − 0x40` (magic `0xFF12`). Here
that header is zero, so its tag branch is not taken.

**Other fixtures:**
- four idle objects;
- the unit pool with owning units (`+0x698` → record);
- a party record (`+5` = 0) and a foe record (`+5` = 1), each with five equipment words `0xFFFF`.

**7 / 7 pass, and `result.json` is byte-identical over three runs** (md5 `73f2a5dce02b1c0115fb6ac0f797d720`).

| case | contract item | observed |
|---|---|---|
| `D1_two_disjoint_sources` | D-1 | See "What each path reads" below |
| `D2_every_output_inside_its_cap` | D-2, §10, §12 | 189 runs: every definition of both areas at level spans 0 / 50 / 255, plus party types 0..0x27 at growth inputs 0 / 1e6 / `0x7FFFFFFF`. Every main value lies in [1, cap] and every word and byte field inside its cap. **In all 69 foe runs the executed main value equals an independent parse of the file:** `clamp(base[def+0x22]+0x20 + perLevel[def+0x24]+0x20 × span, 1, 1e9)` |
| `D3_one_cmove_picks_the_cap` | D-3, §11 | The party path saturates at exactly **9,999**. The same writeback on the foe path passes **52,662,254** through (rwf_d, span 255) |
| `D4_second_write_of_the_same_slot` | D-4, §12 | See the D-4 table below |
| `growth_input_wraps_to_the_floor` | D-2, §10 | See "What the execution adds", item 3 |
| `D5_either_layer_pays_the_bonus` | D-5, §12 | Each of the twelve ids in the main-value list (`.rdata 00D102B0`: 74–85), set in either layer alone, gives the **same** main value. Every one changes it: 1,470 → 1,500 … 1,970 |
| `D7_tail_behind_three_guards` | D-7 | See the D-7 list below |

**What each path reads.** A read hook on the registry slot cells shows the sources are disjoint:

| path | slots read |
|---|---|
| `rec+5` = 0 (party) | `02EBF130`, plus equipment `02EBF0F8` and status `02EBF040` |
| `rec+5` = 1 (foe) | `02EBF120` / `140` / `148` / `150`, plus the same two; **never** `02EBF130` |

**D-4, at growth input 100,000:**

| party type | stores to `rec+0x24` | final value |
|---|---|---|
| `0x1B`, `0x1E`, `0x27` | 9,999 at `002FF7E2`, then 32,767 at `002FF805` | 32,767 (the second store survives) |
| `0x00`, `0x1A` | 9,999 once | 9,999 |

**D-7: when the tail runs.** It runs with the record's own output block, an owning unit, and bit 5 of `+0x3C` flipped
against the settled word. Then:
- the reset `003105D0` and the sink `00307D10` execute real;
- they write the unit at `00310651` and `00307DD1..DE2`;
- `unit+4` gains `0x200000` at `002FFA38`.

Each negative case returns at `002FFA45` with **no** unit write: no change, an explicit output block, or a foe record.

## What the execution adds

1. **§14's two unresolved conditions, read from the prologue and confirmed by execution:**
   - `edi` at `002FF7BB` is `[rsp+0x3C]` = **`rec+5`** (`002FEFFB`), or `0xFF` for a null record (`002FF018`). So the
     9,999 cap applies exactly when `rec+5 == 0`.
   - `[rsp+0x5C]` at `002FF7E5` is 1 exactly when **`rec+5 == 0` and `rec+4 − 0x1B ≤ 0xC`** (`002FF007`–`002FF011`), the
     band D-4 measures. What those thirteen types are is **not claimed**.
2. **D-7's guards, named:**
   - "`edi == 0`" is the same `rec+5 == 0` test.
   - `[rsp+0x64]` is 1 exactly when the output argument is null **and** `0031B860(rec)` finds an owning unit
     (`002FEF6E`–`002FEF89`), which is also when the pre-call snapshot `[rsp+0x68] = rec+0x3C` is taken.
   - The "two specific flag bits" of §14 are **bits 5 and 27** of that status word (mask `0x8000020` at `002FF989`).
     Their meanings are not claimed.
3. **The main-value floor is 1, and the party growth curve can wrap onto it.**
   - The floor is `r15d = 1` (`002FF5A7`, compared at `002FF7B1`). §14 said this was "taken from the stat page's reading
     rather than re-measured"; it is measured here.
   - For some types a large `rec+8` input makes `002F8E50` return a non-positive value, so the result is the floor 1:
     type `0x06` at `0x7FFFFFFF` returns −1, type `0x0C` at 1e8 and type `0x1B` at 1e7 return negative values.
   - Type `0x00` at `0x7FFFFFFF` and type `0x1B` at 1e6 return values above their caps and are capped.
   - The threshold is type-dependent. What `rec+8` counts, and its shipped range, is not claimed.
4. **The foe path is reproducible from the file alone.** An independent parse of the shipped `st2e` tables predicts every
   executed main value in the sweep.

Routed to FABLE: §14's items answered, and §13 can cite this block.

## Not covered

- D-6 (the `+0x15` bits 0/1 source switch): the sweep ran every definition of the two areas, but no case isolates the bit;
- equipment contributions (every equipment word was `0xFFFF`) and the first two status lists' byte fields beyond the caps;
- a live game.
