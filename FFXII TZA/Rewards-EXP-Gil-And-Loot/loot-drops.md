---
title: "Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus"
kind: "system"
category: "Rewards: EXP, LP, gil and loot"
addresses: "003180F0, 003185D0, 003186F0, 00318820, 00318960, 00318510, 00319530, 00310DB0"
---

## What the player sees

A defeated enemy has five normal drop slots and two extra drops. Each slot is a plain percentage
roll; when it succeeds the slot drops one to four of its item. There is no pity timer and no
accumulating luck.

The **chain level** (0 to 3, see [the chain](kill-chain.md)) sets the drop
*chances*: the four rarer slots go from 40 / 25 / 3 / 1 % at level 0 to 55 / 40 / 12 / 5 % at level 3,
and the fifth slot always drops. A **run of the same model** of enemy (palette swaps such as Wolf and
Alpha Wolf count as one model) sets the *quantities*: more than 8, 16 and 24 kills of the same model in
a row move the quantity table up a step each time. Right after a chain break, the chances come from a
weighted roll instead of the chain level, and the more breaks in a row, the better that roll.

The two extra drops are the **Monograph** drops: they roll only while the party holds the key item the
enemy names (one of the six Monographs or the Canopic Jar), usually for Arcana, High Arcana, a Pebble
or the enemy's own loot.

Picking up a loot bag can also give a **chain bonus**: at chain level 1 and up, a 10 % HP or MP
restore, and from level 2, Protect or Shell.

All of these rolls come from one deterministic generator that restarts from a counter on every area
load, so the same actions after the same area loads produce the same drops.

## How it works

### The generator

Every roll here is `draw % 100` compared with a percentage, and every draw comes from the shared
gameplay LCG at `022C256C`:

```python
a = state = state * 0x41C64E6D + 0x3039;
b = state = state * 0x41C64E6D + 0x3039; state = state * 0x41C64E6D + 0x3039;
draw = ((a >> 16 & 0x7FF) << 10 ^ (b >> 16 & 0x3FF)) << 10 ^ (state >> 16 & 0x3FF);   // 11 + 10 + 10 bits
```

The loot and chain functions do not call the generator `00328370`; each carries its own inlined copy
of the same three steps (for example `00318540`-`0031858B`). The state is seeded by its setter
`00328D80`, whose only caller is the area initialisation `002342F0` (`00234320`), which passes a
counter that increases by one on every area initialisation.

### The drop roll

`Loot_RollDropEntries` (`003180F0`, 641 bytes) fills seven output entries
`{u16 item (FFFFh none), u32 quantity}`, all set to empty first (`0031811D`-`00318158`). The enemy's
drop data is the record at `[unit+E60h]`.

1. **Chance profile** = chain level `022C3158` (`00318116`); when breaks in a row `022C3164` is above
   zero it is replaced by `Loot_SelectChanceProfileByWeight` (`00318820`, `0031815C`-`0031816A`).
2. **Quantity profile** = the first row of the drop table whose signed byte `+05`<sub>h</sub> is negative or at
   least the same-model run `022C3160`; row 0 if none qualifies (`003181C7`-`003181EF`).
3. **Five slots** (`003181F8`-`00318238`): slot *i* holds the item word at `record+28h+2i`. The slot
   is kept when its word is not `FFFF`<sub>h</sub> and `Loot_RollNormalSlotChance(profile, i)` succeeds, **or**
   when the developer-console override equals *i*. A kept slot gets quantity
   `Loot_RollNormalSlotQuantityBucket(quantity profile, i) + 1` (`00318225`).
   - The override is read by `0017D340` from `+E64`<sub>h</sub> of the console settings object at `01F81428`
     (console entry "Enable 100% successful drop", values -1 to 3).
4. **Two extra drops** (`0031823A`-`00318283`): `Loot_RollAdditionalItemChance(item, condition,
   chance)` with item `record+4Ah`, condition `record+48h`, chance byte `record+42h`, and again with
   `+4E`<sub>h</sub>, `+4C`<sub>h</sub>, `+43`<sub>h</sub>. Each extra is quantity 1.
5. **Merge** (`003182A0`-`003182D5`): walking from the last entry back to the first, an entry whose item
   matches an earlier entry adds its quantity to the nearest earlier match and is emptied, so every
   duplicate ends in the earliest entry with that item. Empty entries get quantity 0
   (`003182D7`-`0031834F`); the function returns 1 if any entry holds an item.

### The individual rolls

Each roll is its own function:

- `Loot_RollNormalSlotChance(profile, slot)` (`003185D0`): returns 0 for a profile outside the table
  or `slot > 4`; otherwise succeeds when `r < row[slot]`, a signed byte, so a chance of 0 or below never
  drops.
- `Loot_RollNormalSlotQuantityBucket(profile, slot)` (`003186F0`): sums the four signed weights at
  `row + 6 + slot*4` and returns the index (0-3) of the first one whose running sum exceeds `r`, or 4
  when none does (`003187E3`-`003187FB`); 0 for bad arguments. So the code allows 1 to 5 items; in the
  shipped table every slot's weights sum to 100, so it is 1 to 4.
- `Loot_SelectChanceProfileByWeight()` (`00318820`): `00318960` picks the first row whose signed byte
  `+21`<sub>h</sub> is negative or at least `022C3164`, or row 0 (`003189D6`). The walk sums signed bytes from
  `row + 22h`, as many as the table has rows (`dword[table+4]` = 4), and returns the first index whose
  running sum exceeds `r`, or 0 (`0031893B`-`00318948`).
- The same walk reads one byte past the row: with the shipped row size of `25`<sub>h</sub>, a row holds three
  weights and the fourth byte read is the next row's `+00`<sub>h</sub> (four zero bytes after the last row in the
  file). In shipped data the three weights always sum to 100, so the fourth never decides.
- `Loot_RollAdditionalItemChance(item, condition, chance)` (`00318510`): returns 0 without drawing when
  the item or condition is `FFFF`<sub>h</sub> or when `BattleEncodedId_QueryMode0Positive(condition)` (`0030B0E0`)
  says the party holds no free copy of the condition item (`0031851E`-`0031853A`); otherwise succeeds
  when `r < chance`.

### How many draws a kill costs

The drop roll draws once for the profile (only while `022C3164 > 0`),
once per slot whose word is not `FFFF`<sub>h</sub>, once per kept slot, and once per extra that passes its guard:
between 0 and 13 draws, depending on the data and on earlier outcomes. The chain update draws a level
roll and a coin roll on a continuing kill (see [the chain](kill-chain.md)).

### The chain bonus from pickups

`BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`), the periodic unit tick, collects a world
loot pickup the unit overlaps (`002FB150` finds it, `00319A00` collects it, `00311105`-`00311141`).
Every pickup adds 1 to the chain's pickup count `022C3174`, which slows the next chain level rise
unless the coin is up. For a party unit (`[unit+698h]+5 == 0`, `00311130`) the tick then rolls the
bonus:

1. `00319530` (`00311146`) rolls `r` and walks the seven unsigned weights at `01EED3B8 + level*7`;
   it returns the first index whose running sum exceeds `r`, or 0 when no index does or when the
   level is above 3 (`003195B8`, `003195EC`).
2. For outcomes 1-6 the tick gathers the party members (`00311173`-`003111B7`; outcomes 3 and 5
   only the picker, `003111DD`-`003111F1`).
3. It applies action `F5`<sub>h</sub>, "Chain Bonus", through `BattleFormula_ResolveTargetResult` /
   `BattleFormula_ApplyTargetResult` (`0031124D`, `0031126C`) with the variant
   `00D102C0[outcome]` = `{-1, 0, 1, 2, 2, 3, 3}`.

The action's effect slot `003908A0` does, by variant:

| Variant | Effect | Where |
|---|---|---|
| 0 | HP amount `02AEE008` = 10 % of the target's HP figure, dword `+24`<sub>h</sub>; doubled when bit 28 of `+64h \| +3Ch` is set; dword `+48`<sub>h</sub> (at least 1) when bit 16 is set | `00390A4E`-`00390A94` |
| 1 | MP amount `02AEE010` = 10 % of the `i16` at `+28`<sub>h</sub>, or 0 when byte `+6C`<sub>h</sub> or `+7C`<sub>h</sub> is negative | `00390A17`-`00390A46` |
| 2 | adds Protect (status 18) through `00387BB0` | `003908DF`-`003909E3` |
| 3 | adds Shell (status 19) through `00387BB0` | `003908DF`-`003909E3` |

A status is refused (`02AEDFBC` = 1) in any of these cases (`003908DF`-`003909E3`):

- the target already has it (`+3C`<sub>h</sub>);
- the action's mask at `+8` holds the status while the status row's byte `+6` bit `20`<sub>h</sub> is clear
  (row in the status table `[02EBF118]`);
- the target is not a party member (byte `+5` non-zero) and the row word `+6` bit `100`<sub>h</sub> is set;
- the action's mask at `+8` overlaps the row's dword `+20`<sub>h</sub>.

| Chain level | nothing | HP 10 % | MP 10 % | Protect (picker) | Protect (party) | Shell (picker) | Shell (party) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 100 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 80 | 10 | 10 | 0 | 0 | 0 | 0 |
| 2 | 50 | 20 | 20 | 5 | 0 | 5 | 0 |
| 3 | 40 | 25 | 25 | 0 | 5 | 0 | 5 |

## Layouts

The drop table is `battle_pack.bin` directory entry `+1C`<sub>h</sub>, bound to `02EBF0C0` at `00236CD7`; it is
identical in all nine language copies.

`LootTableHeader` (offsets from the start of the section):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | magic | 'st2e' |
| `04`<sub>h</sub> | `i32` | count | rows; 4 in the shipped file |
| `08`<sub>h</sub> | `u16` | stride | row size; `25`<sub>h</sub> in the shipped file |
| `0A`<sub>h</sub> | `u16` | pad0A | not read by the loot code |
| `0C`<sub>h</sub> | `u32` | rowsOff | offset of the rows, resolved through `0020E600` |

`LootTableRow` (`25`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i8[5]` | chance | drop chance per slot, percent (`003185D0`) |
| `05`<sub>h</sub> | `i8` | runLimit | same-model run limit for the quantity row (`003181C7`); -1 ends the list |
| `06`<sub>h</sub> | `i8[20]` | qtyWeights | four cumulative quantity weights per slot (`003186F0`) |
| `1A`<sub>h</sub> | `u8[7]` | bonusCopy | the same values as the chain-bonus row at `01EED3B8`; the code reads the EXE copy |
| `21`<sub>h</sub> | `i8` | breakLimit | breaks-in-a-row limit for the weighted chance profile (`00318960`); -1 ends the list |
| `22`<sub>h</sub> | `i8[3]` | profileWeights weights of chance profiles 0-2 (00318820) |  |

The shipped rows:

| Row | Slot chances % | `+05`<sub>h</sub> | Slot 0 quantity weights | `+21`<sub>h</sub> | `+22h..+24h` |
|---:|---|---:|---|---:|---|
| 0 | 40 / 25 / 3 / 1 / 100 | 8 | 100 / 0 / 0 / 0 | 6 | 100 / 0 / 0 |
| 1 | 45 / 30 / 6 / 2 / 100 | 16 | 65 / 35 / 0 / 0 | 12 | 85 / 10 / 5 |
| 2 | 50 / 35 / 8 / 3 / 100 | 24 | 30 / 50 / 20 / 0 | 20 | 75 / 15 / 10 |
| 3 | 55 / 40 / 12 / 5 / 100 | -1 | 0 / 60 / 30 / 10 | -1 | 65 / 20 / 15 |

The enemy's drop record (`[unit+E60h]`), the fields the drop roll reads:

`EnemyDropFields` (offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `28`<sub>h</sub> | `u16[5]` | slotItems | the five normal drops; `FFFF`<sub>h</sub> = none |
| `32`<sub>h</sub> | `...` | other | fields not read by the drop roll |
| `42`<sub>h</sub> | `u8` | extraChance0 | chance of extra drop 0, percent |
| `43`<sub>h</sub> | `u8` | extraChance1 | chance of extra drop 1, percent |
| `44`<sub>h</sub> | `...` | gap44 | not read by the drop roll |
| `48`<sub>h</sub> | `u16` | extraCond0 | key item that must be held for extra drop 0 |
| `4A`<sub>h</sub> | `u16` | extraItem0 | extra drop 0 |
| `4C`<sub>h</sub> | `u16` | extraCond1 | key item for extra drop 1 |
| `4E`<sub>h</sub> | `u16` | extraItem1 | extra drop 1 |

Over the 1,146 shipped spawn rows the condition is always one of eight key items: `8065`<sub>h</sub>-`806A`<sub>h</sub>
and `806B`<sub>h</sub> (the Monographs) and `806C`<sub>h</sub> (the Canopic Jar); the extra item is Arcana (`204C`<sub>h</sub>,
526 entries), High Arcana (`204D`<sub>h</sub>, 49), a Pebble (`209D`<sub>h</sub>, 277) or the enemy's own loot
(`209E`<sub>h</sub>-`20EF`<sub>h</sub>).

## Modding notes

- Drop chances and quantities are the four rows of the `battle_pack.bin` table above; editing a chance
  changes the drop rate linearly. Keep each slot's four quantity weights summing to 100 or less: below
  100, the remainder becomes a fifth bucket that drops five of the item.
- To change the chain bonus weights, edit `01EED3B8` in the executable: that is the copy `00311146` reads.
- An enemy's drops are its record's five item words and two extras; enemies have no drop profile of
  their own.
- Because all of this shares one generator with spawning and AI, any change in the number of rolls
  before a drop changes the drop.

## Related

- [Kill chain](kill-chain.md) - the chain level, the same-model
  run and breaks in a row.
- [Who gets EXP, LP and gil from a kill](exp-lp-and-level-ups.md) - the
  rest of the defeat rewards.
- [RNG streams](../Random-Numbers/random-number-generators.md) - the shared gameplay generator.
