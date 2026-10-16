---
title: "Steal: the item chances, the three Thief's Cuffs rolls and the steal messages"
kind: "system"
category: "Damage and battle formulas"
addresses: "00390390, 00385F60, 003847C0, 0030FED0, 0023A570, 00385BA0, 003112F0, 00469EC0, 0046A870, 0017D450"
---

## What the player sees

An enemy can carry up to three items to steal: a common, an uncommon and a rare one.

- **Without Thief's Cuffs** one attempt gives at most one item. The rare item is tried first, then
  the uncommon one, then the common one.
- **With Thief's Cuffs** each of the three items is rolled on its own, so one attempt can take two or
  all three.
- **Once something has been stolen** from an enemy, every later attempt on it fails with "has nothing
  to steal".
- **A roll that lands on an item the enemy does not carry** fails with "couldn't steal from".

For an enemy that carries all three items:

| Item | Without Thief's Cuffs | With Thief's Cuffs |
|---|---:|---:|
| Rare | 3 % | 6 % |
| Uncommon | 9.7 % | 30 % |
| Common | 48.0 % | 80 % |
| Nothing at all | 39.3 % | 13.2 % |

## How it works

### Where the roll runs

Steal is calculator slot 195. The qword at `01EFABD8`, slot 195 of the calculator table `01EFA5C0`,
holds `00390390`. Entry 49 of the recipe table `01EF96C0` is the list at `01EFA198`, which has an empty
preview segment and the committed segment `[195]`; no other recipe lists slot 195. Steal (action
`A9`<sub>h</sub>) is the only action whose recipe byte `+08`<sub>h</sub> is 49 in the action rows of `battle_pack.bin`.

The resolver `00385F60` builds the evaluation context with `003847C0` (`003860D5`), passing the result
record as context `+10`<sub>h</sub> and the user's stats record for the effect bits. It calls each slot of the
committed segment with `(userStats, targetStats, &context)` at `003863D0` and leaves the segment when
`02AEDFB8` reads 1 (`003863D7`).

### Which items can be stolen

The roll finds the target's battle unit (`0031B860`) and, for an enemy-side unit (byte `+5` of the
stats record at unit `+698`<sub>h</sub> is 1), reads the enemy's record at unit `+E60`<sub>h</sub>
(`003903AD`-`003903DB`). Its words `+32`<sub>h</sub>, `+34`<sub>h</sub> and `+36`<sub>h</sub> are the common, uncommon and rare item,
`FFFF`<sub>h</sub> meaning none. Byte `+14`<sub>h</sub> of the spawn record at unit `+6A0`<sub>h</sub> holds one bit per item still
available: bit 0, 1 and 2.

The attempt ends as "nothing to steal" in either of these cases:

- all three item words are `FFFF`<sub>h</sub> (`003903DB`-`003903F3`);
- an item word is set and its bit is clear (`0039041E`, `0039044D`, `0039047E`).

That exit sets bit 23 (`800000`<sub>h</sub>) of the result's `+2C`<sub>h</sub> and `02AEDFBC` = 1, and returns
(`0039048A`-`003904A0`).

### When the availability bits change

`BattleUnit_ApplyUnitDefinition` (`0023A570`) sets them when the spawn record is fresh, that is when
its byte `+0` has neither bit 0 nor bit 2 (`0023A791`). It writes byte `+14`<sub>h</sub> = 0 and then sets bit
k for each of the three item words that is not `FFFF`<sub>h</sub> (`0023A7AE`-`0023A7E4`).

A won item clears its bit twice: the result's first step `00385BA0` clears bit 2, 1 and 0 for the won
rare, uncommon and common item (`00385C17`, `00385C41`, `00385C6B`), and the applier clears it again
(`0031146F`). Because any set item word with a clear bit blocks the next attempt, an enemy can be
stolen from successfully once.

### The Thief's Cuffs test

The roll branches on bit 1 of context byte `+1C`<sub>h</sub> (`003904A5`). Context bytes `+1A`<sub>h</sub>-`+29`<sub>h</sub> merge the
user's two effect layers: bit `id & 7` of byte `+1Ah + id / 8` is set when the user's stats record has
effect `id` in its layer `+68`<sub>h</sub> or `+78`<sub>h</sub> (`00384820`-`00384858`). Bit 1 of `+1C`<sub>h</sub> is therefore
effect 17.

Thief's Cuffs are equipment row 354 of `battle_pack.bin` (named in the equipment-name table), and the
row's augment byte `+1A`<sub>h</sub> is 17. The stats rebuild `0030FED0` collects the augment byte of each of the
five equipped items whose group (`0031E9A0`) is 3, which is equipment classes 19-22 (`0031E9F0`), and
Thief's Cuffs are class 21 (`00310080`-`00310121`). It then moves layer `+78`<sub>h</sub> to that set
(`00310303`-`003103A3`).

### The three rolls with Thief's Cuffs

With the bit set, the roll draws three numbers `r = MT19937 % 100` (`00379CD0`) and tests each item on
its own:

| Item | Wins when | Test | Sets |
|---|---|---|---|
| Rare | `r < 6` and the rare word is set | `003904CD`-`003904EB` | `02AEE04E` |
| Uncommon | `r < 30` and the uncommon word is set | `0039050A`-`00390527` | `02AEE04D` |
| Common | `r < 80` and the common word is set | `00390546`-`0039055B` | `02AEE04C` |

When none of the three is set, it sets `02AEDFBC` = 1 and `02AEDFB8` = 1 (`00390563`-`00390584`).

### The single roll without Thief's Cuffs

Without the bit, the roll draws a new number only after the previous test missed:

1. `r < 3` wins the rare item: `02AEE04E` = 1 when the rare word is set (`003905B8`, `0039066A`),
   otherwise the attempt fails (`0039057E`).
2. Otherwise `r < 10` wins the uncommon item: `02AEE04D` = 1 when its word is set (`003905E9`,
   `00390650`), otherwise the attempt fails.
3. Otherwise `r < 55` wins the common item: `02AEE04C` = 1 when its word is set (`00390612`,
   `00390635`), otherwise the attempt fails (`00390495`).
4. Otherwise the attempt fails (`00390621`-`00390626`).

A failure here sets `02AEDFBC` = 1 and leaves bit 23 clear. For an enemy with all three items:

```python
rare = 0.03
uncommon = 0.97 * 0.10        = 0.097
common = 0.97 * 0.90 * 0.55 = 0.480
nothing = 0.97 * 0.90 * 0.45 = 0.393
with Thief's Cuffs, nothing = 0.94 * 0.70 * 0.20 = 0.132
```

### The debug value that forces an item

Each test also wins when `0017D450` returns that item's number: 0 for the common item, 1 for the
uncommon and 2 for the rare (the `test` and `cmp` after each draw). `0017D450` returns
`[001D50D0() + E5Ch]`, a field of the settings object that its builder `001CCB20` sets to -1
(`001CCE1F`), which forces nothing.

### Where the result goes

`BattleFormula_ResetScratchState` (`003849B0`) zeroes `02AEDFB8`, `02AEDFBC` and `02AEE04C`-`02AEE04E`
(`003849BC`-`003849C2`, `00384A1C`-`00384A23`), and the resolver calls it before any slot runs
(`00386001`). After the slots, the resolver:

1. sets the result kind `+04`<sub>h</sub> to 6 when `02AEDFBC` is set (`003866C1`-`003866CA`), and for kind 6
   clears bits 0, 2 and 3 of `+18`<sub>h</sub> (`003866EB`);
2. copies `02AEE04C`, `02AEE04D` and `02AEE04E` into the result's `+32`<sub>h</sub>, `+33`<sub>h</sub> and `+34`<sub>h</sub>
   (`003867F1`-`0038680C`).

For an enemy-side target, the applier `003112F0` adds one of each won item (its item word, when not
`FFFF`<sub>h</sub>) with `003008A0` and clears its availability bit (`00311430`-`0031148B`)
([Action results](../Battle-Actions/action-results.md)).

### The battle messages

The post-result dispatcher `00469EC0` posts the steal lines
([Battle message list](../Battle-Actions/battle-message-list.md) has their texts):

| Outcome | Event | Site |
|---|---|---|
| Failed, bit 23 set | `33`<sub>h</sub> (steal failed, nothing to steal) | `0046A3C4`-`0046A3F0` |
| Failed, bit 23 clear | `34`<sub>h</sub> (couldn't steal from) | `0046A3C4`-`0046A3F0` |
| Won items | the stolen-goods lines of `0046A870` | `0046A504` |

`0046A870` gathers the won items into a three-entry list at `02EBB540` (`0046AC90` adds 1 to the count
of an item already in the list) and posts one line per entry (`0046A940`-`0046A9A2`):

| Entry | Gil (`E000`<sub>h</sub> id) | One item | Several of one item |
|---|---|---|---|
| First | `31`<sub>h</sub> | `2E`<sub>h</sub> | `2D`<sub>h</sub> |
| Later | `32`<sub>h</sub> | `30`<sub>h</sub> | `2F`<sub>h</sub> |

## Layouts

The enemy's record at unit `+E60`<sub>h</sub>, the fields the steal reads:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `32`<sub>h</sub> | `u16` | stealCommon | common steal item; `FFFF`<sub>h</sub> = none (`00390390`, `0023A570`) |
| `34`<sub>h</sub> | `u16` | stealUncommon | uncommon steal item; `FFFF`<sub>h</sub> = none |
| `36`<sub>h</sub> | `u16` | stealRare | rare steal item; `FFFF`<sub>h</sub> = none |

The spawn record at unit `+6A0`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `14`<sub>h</sub> | `u8` | stealLeft | bits `1`<sub>h</sub>, `2`<sub>h</sub>, `4`<sub>h</sub>: the common, uncommon and rare item is still available (`0023A570`, `00390390`, `003112F0`) |

## Modding notes

- The chances are immediates in `00390390`: `6`, `1E`<sub>h</sub>, `50`<sub>h</sub> with Thief's Cuffs and `3`, `A`<sub>h</sub>,
  `37`<sub>h</sub> without (the six `cmp r8d` sites above).
- Another accessory gets the three rolls when its equipment row's augment byte `+1A`<sub>h</sub> is 17, for
  an item of classes 19-22. Three weapon rows (90, 98 and 139) also hold 17 there, and the rebuild
  ignores them because weapons are not in group 3.
- Another action gets the steal roll when its recipe byte `+08`<sub>h</sub> is 49, but the steal messages stay
  keyed to action `A9`<sub>h</sub> (`0046A3C9`).

## Related

- [Action results](../Battle-Actions/action-results.md) - the result record and the applier that adds
  the item.
- [Battle log](../Battle-Actions/battle-log.md) - how the steal lines are posted and filtered.
- [Battle message list](../Battle-Actions/battle-message-list.md) - the texts of events `2D`<sub>h</sub>-`34`<sub>h</sub>.
- [Loot drops](../Rewards-EXP-Gil-And-Loot/loot-drops.md) - the drop fields of the same enemy
  record.
- [Evaluation context](damage-formula.md) - the merged effect bits.
- [Which roll uses which generator](../Random-Numbers/which-roll-uses-which-generator.md) -
  the MT19937 stream the roll draws from.
