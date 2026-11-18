[Home](../../README.md) / [Rewards: EXP, LP, gil and loot](README.md) / Loot drops

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus | system | Rewards: EXP, LP, gil and loot | EXP, loot and progression | How a defeated enemy's loot is rolled: which drop-chance row the chain selects, slot and quantity rolls, the drop-table layouts with shipped rows, the developer 100 % drop override, and the HP/MP/Protect/Shell chain bonus on pickup. | 0x003180F0, 0x003185D0, 0x003186F0, 0x00318820, 0x00318960, 0x00318510, 0x00319530, 0x00310DB0 |

## What the player sees

A defeated enemy has five normal drop slots and two extra drops. Each slot is a plain percentage
roll; when it succeeds the slot drops one to four of its item. There is no pity timer and no
accumulating luck.

The **chain level** (0 to 3, see [the chain](kill-chain.md)) sets the drop
*chances*: the four rarer slots go from 40 / 25 / 3 / 1 % at level 0 to 55 / 40 / 12 / 5 % at level 3,
and the fifth slot always drops. Right after a chain break, the chances come from a
weighted roll instead of the chain level, and the more breaks in a row, the better that roll.

For quantities, enemies are grouped by a number each enemy's class row carries (`+0x40`, the bestiary's
`model_family`), not by the model they are drawn with: Wolf and Alpha Wolf share one (`0x01FF`), while Wary
Wolf, drawn with the same model `m1015`, has its own (`0x138D`), as do Coeurl (`0x0226`) and Grimalkin
(`0x139A`), both `m1014`.

A **run of one quantity group** of enemy sets the *quantities*: the run's counter moves the quantity table up a step each time it passes 8,
16 and 24. After a reset the counter stays 0 for the first two kills and adds 1 for each further
kill by the party of the same class and group, so kills 1, 2, 10, 11, 19 and 27 leave it at 0, 0, 8, 9, 17 and 25
and use quantity rows 0, 0, 0, 1, 2 and 3 ([the chain](kill-chain.md)).

The two extra drops are the **Monograph** drops; half the enemy definitions have both and the other half neither.
The first rolls only while the party holds the Monograph the enemy names (one of seven), for a Pebble, Arcana, a
Knot of Rust or a loot item, usually one the enemy also drops or gives up to Steal or Poach. The second rolls only
while the party holds the Canopic Jar, for Arcana, High Arcana, Dark Matter, an Ether or a Meteorite.

Collecting a [loot pickup](loot-pickups.md) can also give a **chain bonus**: at chain level 1 and up, a 10 % HP or MP
restore, and from level 2, Protect or Shell.

All of these rolls come from one deterministic generator that restarts from a counter on every area
load, so the same actions after the same area loads produce the same drops.

What drops and how often come from two places. The enemy's own record names the item in each of its five slots and its
two extras. The chances and quantities come from a four-row table in `battle_pack.bin` that every enemy shares, and
the chain picks the row.

## How it works

### The generator

Every roll here is `draw % 100` compared with a percentage, and every draw comes from the shared
gameplay LCG at `0x022C256C`:

```python
a = state = state * 0x41C64E6D + 0x3039;
b = state = state * 0x41C64E6D + 0x3039; state = state * 0x41C64E6D + 0x3039;
draw = ((a >> 16 & 0x7FF) << 10 ^ (b >> 16 & 0x3FF)) << 10 ^ (state >> 16 & 0x3FF);  # 11 + 10 + 10 bits
```

The loot and chain functions do not call the generator `0x00328370`; each carries its own inlined copy
of the same three steps (for example `0x00318540`-`0x0031858B`). The state is seeded by its setter
`0x00328D80`, whose only caller is the area initialisation `0x002342F0` (`0x00234320`), which passes a
counter that increases by one on every area initialisation.

### The drop roll

`Loot_RollDropEntries` (`0x003180F0`, 641 bytes) fills seven output entries
`{u16 item (0xFFFF no item), u32 quantity}`, all set to empty first (`0x0031811D`-`0x00318158`). The enemy's
drop data is the record at `[unit+0xE60]`.

1. **Chance profile** = chain level `0x022C3158` (`0x00318116`); when breaks in a row `0x022C3164` is above
   zero it is replaced by `Loot_SelectChanceProfileByWeight` (`0x00318820`, `0x0031815C`-`0x0031816A`).
2. **Quantity profile** = the first row of the drop table whose signed byte `+0x05` is negative or at
   least the quantity-group run `0x022C3160`; row 0 if no row qualifies (`0x003181C7`-`0x003181EF`).
   - With the shipped limits 8, 16, 24 and -1 this is row 0 for a run of 0-8, row 1 for 9-16,
     row 2 for 17-24 and row 3 from 25.
   - The table is the one in slot `0x02EBF0C0`, its row count the dword `+0x04`; a null
     slot gives row 0 (`0x0031816D`-`0x00318186`). When the slot is set and `0x0020E600`
     answers null, the row address is 0 and its byte `+0x05` is read with no test
     (`0x00318195`-`0x003181C7`).
   - When the killer is a party unit, the roll reads the run after the same kill's chain update:
     `0x00312280` calls `0x00317ED0` at `0x003122CD` (`0x003122B9`-`0x003122C8`) and the drop roll at `0x003125A1`.
   - A kill with no party killer that the reward gate still pays through its Poison or Petrify arm
     (`0x00312305`-`0x0031231B`, [kill rewards](kill-rewards.md)) does not update the chain, and its roll reads the run as the last
     update left it. How kills move the run is on [the chain](kill-chain.md).
3. **Five slots** (`0x003181F8`-`0x00318238`): slot *i* holds the item word at `record+0x28+2i`. The slot
   is kept when its word is not `0xFFFF` and `Loot_RollNormalSlotChance(profile, i)` succeeds, **or**
   when the developer-console override equals *i*. A kept slot gets quantity
   `Loot_RollNormalSlotQuantityBucket(quantity profile, i) + 1` (`0x00318225`).
   - The override is read by `0x0017D340` from `+0xE64` of the console settings object at `0x01F81428`
     (console entry "Enable 100% successful drop", values -1 to 3).
4. **Two extra drops** (`0x0031823A`-`0x00318283`): `Loot_RollAdditionalItemChance(item, condition,
   chance)` with item `record+0x4A`, condition `record+0x48`, chance byte `record+0x42`, and again with
   `+0x4E`, `+0x4C`, `+0x43`. Each extra is quantity 1.
5. **Merge** (`0x003182A0`-`0x003182D5`): walking from the last entry back to the first, an entry whose item
   matches an earlier entry adds its quantity to the nearest earlier match and is emptied, so every
   duplicate ends in the earliest entry with that item. Empty entries get quantity 0
   (`0x003182D7`-`0x0031834F`); the function returns 1 if any entry holds an item.

In the six functions `0x003180F0`, `0x00318820`, `0x00318960`, `0x003185D0`, `0x003186F0` and `0x00318510`, the instructions that
address the chain's state `0x022C3158`-`0x022C317B` ([kill chain](kill-chain.md#state)) directly are the reads at
`0x00318116`, `0x0031815C`, `0x003181D2` and `0x003189D6`. The roll's one direct caller is `0x00312280` (`0x003125A1`), and
`0x00318960`'s is `0x00318820` (`0x003188AB`).

### The individual rolls

Each roll is its own function:

- `Loot_RollNormalSlotChance(profile, slot)` (`0x003185D0`): returns 0 for a profile outside the table
  or `slot > 4`; otherwise succeeds when `r < row[slot]`, a signed byte, so a chance of 0 or below never
  drops. A table pointer `0x02EBF0C0` of 0 counts as no rows, so every profile is outside (`0x00318672`).
- The chance roll draws `r` before the arguments are tested (`0x003185E4`-`0x00318641`), so a call that returns 0
  for a bad argument still advances the generator.
- `Loot_RollNormalSlotQuantityBucket(profile, slot)` (`0x003186F0`): sums the four signed weights at
  `row + 6 + slot*4` and returns the index (0-3) of the first one whose running sum exceeds `r`, or 4
  when no sum does (`0x003187E3`-`0x003187FB`); 0 for bad arguments. So the code allows 1 to 5 items; in the
  shipped table every slot's weights sum to 100, so it is 1 to 4.
- Like the chance roll, `0x003186F0` draws `r` before it tests the profile and the slot (`0x00318704`-`0x00318761`),
  so a bad argument costs a draw there as well.
- `Loot_SelectChanceProfileByWeight()` (`0x00318820`): `0x00318960` picks the first row whose signed byte
  `+0x21` is negative or at least `0x022C3164`, or row 0 (`0x003189D6`). The walk sums signed bytes from
  `row + 0x22`, as many as the table has rows (`dword[table+4]` = 4), and returns the first index whose
  running sum exceeds `r`, or 0 (`0x0031893B`-`0x00318948`).
- The same walk reads one byte past the row: with the shipped row size of `0x25`, a row holds three
  weights and the fourth byte read is the next row's `+0x00` (four zero bytes after the last row in the
  file). In shipped data the three weights always sum to 100, so the fourth never decides.
- `Loot_RollAdditionalItemChance(item, condition, chance)` (`0x00318510`): returns 0 without drawing when
  the item or condition is `0xFFFF` or when `BattleEncodedId_QueryMode0Positive(condition)` (`0x0030B0E0`)
  says the party does not own the condition item (`0x0031851E`-`0x0031853A`); otherwise succeeds when
  `r < chance`. Every condition is a key item (below), whose class answers mode 0 with its owned bit
  (`0x002FD970`).

### How many draws a kill costs

The drop roll draws once for the profile (only while `0x022C3164 > 0`),
once per slot whose word is not `0xFFFF`, once per kept slot, and once per extra that passes its guard:
between 0 and 13 draws, depending on the data and on earlier outcomes.

On a continuing kill the chain update draws the coin (`0x00317FC1`) and, before it, the level roll of
`0x003183D0` (`0x0031844A`), except at level 3 (`0x003183ED`-`0x003183F1`) and when the kills since the last
rise pass the level's threshold, which raises the level without a draw (`0x00318414`-`0x00318417`): two
draws, or one in those two cases. A first kill and a breaking kill draw nothing
([the chain](kill-chain.md)).

### The chain bonus from pickups

`BattleUnit_RunPeriodicCombatMaintenance` (`0x00310DB0`), the periodic unit tick, collects a world
loot pickup the unit overlaps (`0x002FB150` finds it, `0x00319A00` collects it, `0x00311105`-`0x00311141`).
Every pickup adds 1 to the chain's pickup count `0x022C3174`, which slows the next chain level rise
unless the coin is up. For a party unit (`[unit+0x698]+5 == 0`, `0x00311130`) the tick then rolls the
bonus:

1. `0x00319530` (`0x00311146`) rolls `r` and walks the seven unsigned weights at `0x01EED3B8 + level*7`;
   it returns the first index whose running sum exceeds `r`, or 0 when no index does or when the
   level is above 3 (`0x003195B8`, `0x003195EC`).
2. For outcomes 1-6 the tick gathers the party members (`0x00311173`-`0x003111B7`; outcomes 3 and 5
   only the picker, `0x003111DD`-`0x003111F1`).
   The members are the nine entries of party map 1 (`0x00320AB0(i, 1)`), kept at `0x022C1740`
   when `(+0x64 | +0x3C) & 0x80000003` is 0 or `0x00377C20` reports a town
   (`0x00311173`-`0x003111B7`). An outcome of 0 or above 6 ends the bonus (`0x0031114E`-`0x0031115D`).
3. It applies action `0xF5`, "Chain Bonus", through `BattleFormula_ResolveTargetResult` /
   `BattleFormula_ApplyTargetResult` (`0x0031124D`, `0x0031126C`) with the variant
   `0x00D102C0[outcome]` = `{-1, 0, 1, 2, 2, 3, 3}`.

   For each member it takes the id `0x0031E800(member)`, calls
   `0x002EACD0(id, 1, &id, 0x76)` when the id is not 0 (`0x003111D8`-`0x00311208`), clears a
   `0x148`-byte result and puts the variant into bits `0x18` of the result's first dword
   (`0x0031120D`-`0x00311241`). Both calls pass no source: `0x00385F60(0xF5, 0, member, result)`
   and `0x003112F0(result, 0, member, 0xF5, 0)`.

The action's effect slot `0x003908A0` does, by variant:

| Variant | Effect | Where |
|---|---|---|
| 0 | HP amount `0x02AEE008` = 10 % of the target's HP figure, dword `+0x24`; doubled when bit `0x10000000` of `+0x64 \| +0x3C` is set; dword `+0x48` (at least 1) when bit `0x10000` is set | `0x00390A4E`-`0x00390A94` |
| 1 | MP amount `0x02AEE010` = 10 % of the `i16` at `+0x28`, or 0 when byte `+0x6C` or `+0x7C` is negative | `0x00390A17`-`0x00390A46` |
| 2 | adds Protect (status 18) through `0x00387BB0` | `0x003908DF`-`0x003909E3` |
| 3 | adds Shell (status 19) through `0x00387BB0` | `0x003908DF`-`0x003909E3` |

`0x00387BB0(source, stats, status, context)` adds to the result at context `+0x10`. It
answers 0 and adds nothing when a source is given and the context's dword `+0x08` has a
bit of `0x80000003` (`0x00387BDF`-`0x00387BEE`). For status 0 it adds nothing either: it
answers 0 when the stats byte `+0x68` or `+0x78` has bit `0x2`, and 1 otherwise
(`0x00387BF5`-`0x00387C0C`).

The add sets bit `1 << status` of the result's `+0x54`. Unless the status row's byte
`+0x08` is `0xFF`, it stores `0x00387730(source, stats, status)` at result
`+0x5C + 4 * status`; statuses 2 and 6 then get `0xB` there. It stores the word
`0x003876D0(status)` at result `+0xDC + 2 * status` and answers 1 (`0x00387C0E`-`0x00387C8E`).

The row address is `0x0020E600(table dword +0x0C) + status * table word +0x08`, summed as 32-bit values
and zero-extended (`0x00387C4A`-`0x00387C51`), for the table at
`[0x02EBF118]`. With a null table, or a null answer of `0x0020E600`, the address is 0 and the byte `+0x08`
is read from it all the same (`0x00387C1B`-`0x00387C57`).

A status is refused (`0x02AEDFBC` = 1) in any of these cases (`0x003908DF`-`0x003909E3`):

- the target already has it (`+0x3C`);
- the target's statuses, `dword[+0x64] | dword[+0x3C]` as the formula context `0x003847C0` keeps them at `+8`
  (`0x0038485F`-`0x00384868`; bit `0x1000`, or bits `0x811000`, cleared in two cases at `0x00384896` and `0x003848A6`),
  hold the status while the status row's byte `+6` bit `0x20` is clear (row in the status table `[0x02EBF118]`,
  `0x00390910`-`0x00390957`);
- the target is not a party member (byte `+5` non-zero) and the row word `+6` bit `0x100` is set;
- those statuses overlap the row's dword `+0x20` (`0x003909DC`-`0x003909DF`).

| Chain level | nothing | HP 10 % | MP 10 % | Protect (picker) | Protect (party) | Shell (picker) | Shell (party) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 100 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 80 | 10 | 10 | 0 | 0 | 0 | 0 |
| 2 | 50 | 20 | 20 | 5 | 0 | 5 | 0 |
| 3 | 40 | 25 | 25 | 0 | 5 | 0 | 5 |

## Layouts

The drop table is `battle_pack.bin` directory entry `+0x1C`, bound to `0x02EBF0C0` at `0x00236CD7`; it is
identical in all nine language copies.

`LootTableHeader` (offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | 'st2e' |
| `+0x04` | `i32` | count | rows; 4 in the shipped file |
| `+0x08` | `u16` | stride | row size; `0x25` in the shipped file |
| `+0x0A` | `u8[2]` | pad0A | read by none of the loot functions; nothing fixes its width |
| `+0x0C` | `u32` | rowsOff | offset of the rows, resolved through `0x0020E600` |

`LootTableRow` (`0x25` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i8[5]` | chance | drop chance per slot, percent (`0x003185D0`) |
| `+0x05` | `i8` | runLimit | quantity-group run limit for the quantity row (`0x003181C7`); -1 ends the list |
| `+0x06` | `i8[20]` | qtyWeights | four cumulative quantity weights per slot (`0x003186F0`) |
| `+0x1A` | `u8[7]` | bonusCopy | the same values as the chain-bonus row at `0x01EED3B8`; the code reads the EXE copy |
| `+0x21` | `i8` | breakLimit | breaks-in-a-row limit for the weighted chance profile (`0x00318960`); -1 ends the list |
| `+0x22` | `i8[3]` | profileWeights | weights of chance profiles 0-2 (`0x00318820`) |

The shipped rows:

| Row | Slot chances % | `+0x05` | Slot 0 quantity weights | `+0x21` | `+0x22..+0x24` |
|---:|---|---:|---|---:|---|
| 0 | 40 / 25 / 3 / 1 / 100 | 8 | 100 / 0 / 0 / 0 | 6 | 100 / 0 / 0 |
| 1 | 45 / 30 / 6 / 2 / 100 | 16 | 65 / 35 / 0 / 0 | 12 | 85 / 10 / 5 |
| 2 | 50 / 35 / 8 / 3 / 100 | 24 | 30 / 50 / 20 / 0 | 20 | 75 / 15 / 10 |
| 3 | 55 / 40 / 12 / 5 / 100 | -1 | 0 / 60 / 30 / 10 | -1 | 65 / 20 / 15 |

Every byte of the four rows, with the quantity weights of all five slots and the chain-bonus copy (the seven
percentages of the chain-level table above), is in [the drop table](loot-drops-drop-table.tsv).

### Columns of loot-drops-drop-table.tsv

One row per drop table row, 4 rows; `row` is the chance profile and the quantity profile that pick it.

| Column | Holds |
|---|---|
| `chance_slot0`, `chance_slot1`, `chance_slot2`, `chance_slot3`, `chance_slot4` | row bytes `+0x00` to `+0x04`, signed: the percent chance that drop slot 0 to 4 drops (`0x003185D0`); slot 4 is 100 on every row, slot 0 runs from 40 to 55 |
| `qty_weights_slot0`, `qty_weights_slot1`, `qty_weights_slot2`, `qty_weights_slot3`, `qty_weights_slot4` | row bytes `+0x06 + slot × 4`, four signed weights each, written `a / b / c / d`: the chances in percent of 1, 2, 3 and 4 items for that slot (`0x003186F0` returns the index whose running sum first exceeds the roll, and the quantity is that index plus 1); they add up to 100 in every row |
| `chain_bonus_copy` | row bytes `+0x1A` to `+0x20`: the seven percentages of the chain-level row (nothing, HP 10 %, MP 10 %, Protect for the picker and the party, Shell for the picker and the party); the code reads the copy in the executable at `0x01EED3B8` instead |
| `break_limit` | row byte `+0x21`, signed: the breaks-in-a-row limit `0x00318960` compares, 6, 12 and 20 in rows 0 to 2; -1 in row 3 ends the list |
| `profile_weights` | row bytes `+0x22` to `+0x24`, written `a / b / c`: the weights of chance profiles 0, 1 and 2 that `0x00318820` draws from after a chain break |

The enemy's drop record (`[unit+0xE60]`), the fields the drop roll reads:

`EnemyDropFields` (offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x28` | `u16[5]` | slotItems | the five normal drops; `0xFFFF` = no drop |
| `+0x32` | `u16[3]` | steal | the three steal slots; not read by the drop roll |
| `+0x38` | `u32[2]` | partIds | model rebuild parts; not read by the drop roll |
| `+0x40` | `u8[2]` | partLinks | their attach links; not read by the drop roll |
| `+0x42` | `u8` | extraChance0 | chance of extra drop 0, percent |
| `+0x43` | `u8` | extraChance1 | chance of extra drop 1, percent |
| `+0x44` | `u16[2]` | poach | the two poach items; not read by the drop roll |
| `+0x48` | `u16` | extraCond0 | key item that must be held for extra drop 0 |
| `+0x4A` | `u16` | extraItem0 | extra drop 0 |
| `+0x4C` | `u16` | extraCond1 | key item for extra drop 1 |
| `+0x4E` | `u16` | extraItem1 | extra drop 1 |

The whole record, with the readers of the fields the drop roll skips, is on
[battle-unit-construction](../Characters-And-Objects/battle-unit-construction.md).

Of the 1,146 shipped enemy definitions ([Bestiary](../Enemy-Spawning/bestiary.md)), 573 carry both
extra drops and 573 neither. Extra drop 0's condition is always one of the seven Monographs, `0x8065`-`0x806B`, and
extra drop 1's always the Canopic Jar, `0x806C`.

Extra drop 0 is a Pebble (`0x209D`, 277 definitions), a loot item (`0x209E`-`0x20EF`, 200, of which 176 are one of
the definition's own drop, steal or poach items), Arcana (`0x204C`, 57) or a Knot of Rust (`0x003F`, 39). Extra
drop 1 is Arcana (469), High Arcana (`0x204D`, 60), Dark Matter (`0x003E`, 33), an Ether (`0x0003`, 6) or a
Meteorite (`0x0019`-`0x001C`, 5).

## Modding notes

- Drop chances and quantities are the four rows of the `battle_pack.bin` table above; editing a chance
  changes the drop rate linearly. Keep each slot's four quantity weights summing to 100 or less: below
  100, the remainder becomes a fifth bucket that drops five of the item.
- To change the chain bonus weights, edit `0x01EED3B8` in the executable: that is the copy `0x00319530` reads
  (`0x003195BE`), called at `0x00311146`.
- An enemy's drops are its record's five item words and two extras; enemies have no drop profile of
  their own.
- Because all of this shares one generator with spawning and AI, any change in the number of rolls
  before a drop changes the drop.

## Related

- [Kill chain](kill-chain.md) - the chain level, the quantity-group
  run and breaks in a row.
- [Who gets EXP, LP and gil from a kill](exp-lp-and-level-ups.md) - the
  rest of the defeat rewards.
- [RNG streams](../Random-Numbers/random-number-generators.md) - the shared gameplay generator.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 16 calls with 6 other topics</summary>

**Steam and achievements** (explained on [debug menu](../Engine-Core/debug-menu.md))

| Function | | Functions |
|---|---|---|
| `0x00312280` | calls | `0x00316A50` |

**Sound and music** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

| Function | | Functions |
|---|---|---|
| `0x003112F0` | calls | `0x002DF220`, `0x003A1180` |

**Controls and input** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x00253C70` |

**Input gameplay** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x00313A00` |

**Scripts and script commands**

| Function | | Functions |
|---|---|---|
| `0x00320AB0` | is called by | `0x0050FD00`, `0x0050FD50`, `0x0050FDD0`, `0x0050FE20`, `0x0050FE80`, `0x0050FED0`, `0x0050FF20` |
| `0x00377C20` | is called by | `0x00344740`, `0x00352FA0`, `0x003537D0`, `0x00355680` |

**Scripts and script commands** (explained on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [script censuses](../Story-Events-And-Hunts/script-censuses.md))

</details>

---

[← Kill chain](kill-chain.md) | [Loot pickups →](loot-pickups.md)
