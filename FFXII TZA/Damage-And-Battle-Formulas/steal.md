---
title: "Steal: the item chances, the three Thief's Cuffs rolls and the steal messages"
kind: "system"
category: "Damage and battle formulas"
addresses: "0x00390390, 0x00385F60, 0x003847C0, 0x0030FED0, 0x0023A570, 0x00385BA0, 0x003112F0, 0x00469EC0, 0x0046A870, 0x0017D450"
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

Steal is calculator slot 195. The qword at `0x01EFABD8`, slot 195 of the calculator table `0x01EFA5C0`,
holds `0x00390390`. Entry 49 of the recipe table `0x01EF96C0` is the list at `0x01EFA198`, which has an empty
preview segment and the committed segment `[195]`; no other recipe lists slot 195. Steal (action
`0xA9`) is the only action whose recipe byte `+0x08` is 49 in the action rows of `battle_pack.bin`.

The resolver `0x00385F60` builds the evaluation context with `0x003847C0` (`0x003860D5`), passing the result
record as context `+0x10` and the user's stats record for the augment bits. It calls each slot of the
committed segment with `(userStats, targetStats, &context)` at `0x003863D0` and leaves the segment when
`0x02AEDFB8` reads 1 (`0x003863D7`).

### Which items can be stolen

The roll finds the target's battle unit (`0x0031B860`) and, for an enemy-side unit (byte `+5` of the
stats record at unit `+0x698` is 1), reads the enemy's record at unit `+0xE60`
(`0x003903AD`-`0x003903DB`). Its words `+0x32`, `+0x34` and `+0x36` are the common, uncommon and rare item,
`0xFFFF` meaning none. Byte `+0x14` of the spawn record at unit `+0x6A0` holds one bit per item still
available: bit 0, 1 and 2.

The attempt ends as "nothing to steal" in either of these cases:

- all three item words are `0xFFFF` (`0x003903DB`-`0x003903F3`);
- an item word is set and its bit is clear (`0x0039041E`, `0x0039044D`, `0x0039047E`).

That exit sets bit 23 (`0x800000`) of the result's `+0x2C` and `0x02AEDFBC` = 1, and returns
(`0x0039048A`-`0x003904A0`).

### When the availability bits change

`BattleUnit_ApplyUnitDefinition` (`0x0023A570`) sets them when the spawn record is fresh, that is when
its byte `+0` has neither bit 0 nor bit 2 (`0x0023A791`). It writes byte `+0x14` = 0 and then sets bit
k for each of the three item words that is not `0xFFFF` (`0x0023A7AE`-`0x0023A7E4`).

A won item clears its bit twice: the result's first step `0x00385BA0` clears bit 2, 1 and 0 for the won
rare, uncommon and common item (`0x00385C17`, `0x00385C41`, `0x00385C6B`), and the applier clears it again
(`0x0031146F`). Because any set item word with a clear bit blocks the next attempt, an enemy can be
stolen from successfully once.

### The Thief's Cuffs test

The roll branches on bit 1 of context byte `+0x1C` (`0x003904A5`). Context bytes `+0x1A`-`+0x29` merge the
user's two augment layers: bit `id & 7` of byte `+0x1A + id / 8` is set when the user's stats record has
augment `id` in its layer `+0x68` or `+0x78` (`0x00384820`-`0x00384858`). Bit 1 of `+0x1C` is therefore
the augment Thievery (17).

Thief's Cuffs are equipment row 354 of `battle_pack.bin` (named in the equipment-name table), and the
row's augment byte `+0x1A` is 17. The stats rebuild `0x0030FED0` collects the augment byte of each of the
five equipped items whose group (`0x0031E9A0`) is 3, which is equipment classes 19-22 (`0x0031E9F0`), and
Thief's Cuffs are class 21 (`0x00310080`-`0x00310121`). It then moves layer `+0x78` to that set
(`0x00310303`-`0x003103A3`).

### The three rolls with Thief's Cuffs

With the bit set, the roll draws three numbers `r = MT19937 % 100` (`0x00379CD0`) and tests each item on
its own:

| Item | Wins when | Test | Sets |
|---|---|---|---|
| Rare | `r < 6` and the rare word is set | `0x003904CD`-`0x003904EB` | `0x02AEE04E` |
| Uncommon | `r < 30` and the uncommon word is set | `0x0039050A`-`0x00390527` | `0x02AEE04D` |
| Common | `r < 80` and the common word is set | `0x00390546`-`0x0039055B` | `0x02AEE04C` |

When none of the three is set, it sets `0x02AEDFBC` = 1 and `0x02AEDFB8` = 1 (`0x00390563`-`0x00390584`).

### The single roll without Thief's Cuffs

Without the bit, the roll draws a new number only after the previous test missed:

1. `r < 3` wins the rare item: `0x02AEE04E` = 1 when the rare word is set (`0x003905B8`, `0x0039066A`),
   otherwise the attempt fails (`0x0039057E`).
2. Otherwise `r < 10` wins the uncommon item: `0x02AEE04D` = 1 when its word is set (`0x003905E9`,
   `0x00390650`), otherwise the attempt fails.
3. Otherwise `r < 55` wins the common item: `0x02AEE04C` = 1 when its word is set (`0x00390612`,
   `0x00390635`), otherwise the attempt fails (`0x00390495`).
4. Otherwise the attempt fails (`0x00390621`-`0x00390626`).

A failure here sets `0x02AEDFBC` = 1 and leaves bit 23 clear. For an enemy with all three items:

```python
rare = 0.03
uncommon = 0.97 * 0.10        = 0.097
common = 0.97 * 0.90 * 0.55 = 0.480
nothing = 0.97 * 0.90 * 0.45 = 0.393
with Thief's Cuffs, nothing = 0.94 * 0.70 * 0.20 = 0.132
```

### The debug value that forces an item

Each test also wins when `0x0017D450` returns that item's number: 0 for the common item, 1 for the
uncommon and 2 for the rare (the `test` and `cmp` after each draw). `0x0017D450` returns
`[0x001D50D0() + 0xE5C]`, a field of the settings object that its builder `0x001CCB20` sets to -1
(`0x001CCE1F`), which forces nothing.

### Where the result goes

`BattleFormula_ResetScratchState` (`0x003849B0`) zeroes `0x02AEDFB8`, `0x02AEDFBC` and `0x02AEE04C`-`0x02AEE04E`
(`0x003849BC`-`0x003849C2`, `0x00384A1C`-`0x00384A23`), and the resolver calls it before any slot runs
(`0x00386001`). After the slots, the resolver:

1. sets the result kind `+0x04` to 6 when `0x02AEDFBC` is set (`0x003866C1`-`0x003866CA`), and for kind 6
   clears bits 0, 2 and 3 of `+0x18` (`0x003866EB`);
2. copies `0x02AEE04C`, `0x02AEE04D` and `0x02AEE04E` into the result's `+0x32`, `+0x33` and `+0x34`
   (`0x003867F1`-`0x0038680C`).

For an enemy-side target, the applier `0x003112F0` adds one of each won item (its item word, when not
`0xFFFF`) with `0x003008A0` and clears its availability bit (`0x00311430`-`0x0031148B`)
([Action results](../Battle-Actions/action-results.md)).

### The battle messages

The post-result dispatcher `0x00469EC0` posts the steal lines
([Battle message list](../Battle-Actions/battle-message-list.md) has their texts):

| Outcome | Event | Site |
|---|---|---|
| Failed, bit 23 set | `0x33` (steal failed, nothing to steal) | `0x0046A3C4`-`0x0046A3F0` |
| Failed, bit 23 clear | `0x34` (couldn't steal from) | `0x0046A3C4`-`0x0046A3F0` |
| Won items | the stolen-goods lines of `0x0046A870` | `0x0046A504` |

`0x0046A870` gathers the won items into a three-entry list at `0x02EBB540` (`0x0046AC90` adds 1 to the count
of an item already in the list) and posts one line per entry (`0x0046A940`-`0x0046A9A2`):

| Entry | Gil (`0xE000` id) | One item | Several of one item |
|---|---|---|---|
| First | `0x31` | `0x2E` | `0x2D` |
| Later | `0x32` | `0x30` | `0x2F` |

## Layouts

The enemy's record at unit `+0xE60`, the fields the steal reads:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x32` | `u16` | stealCommon | common steal item; `0xFFFF` = none (`0x00390390`, `0x0023A570`) |
| `+0x34` | `u16` | stealUncommon | uncommon steal item; `0xFFFF` = none |
| `+0x36` | `u16` | stealRare | rare steal item; `0xFFFF` = none |

The spawn record at unit `+0x6A0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x14` | `u8` | stealLeft | bits `0x1`, `0x2`, `0x4`: the common, uncommon and rare item is still available (`0x0023A570`, `0x00390390`, `0x003112F0`) |

## State

The won-items list is three 4-byte entries from `0x02EBB540`: the item id (`u16`) at `+0`, the count (`u8`) at `+2`; no
instruction uses byte `+3`. `0x0046A870` empties it first (`0x0046A88D`, `0x0046A897`); `0x0046AC90(item)` adds 1 to the
count of an entry that holds the item, or puts the item with count 1 in the first entry whose count is 0
(`0x0046ACC0`-`0x0046AD0C`); gil (`0xE000` ids) always takes a new entry (`0x0046ACA5`-`0x0046ACB0`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBB548` | `u8[4]` | 0 | the third entry: the third different item or gil won, which is the rare item when all three are won and differ | `0x0046A870`, 0 (`0x0046A897`); `0x0046AC90`: the count (`0x0046ACFE`), the item and count 1 (`0x0046AD07`, `0x0046AD0C`) | `0x0046AC90` (`0x0046ACC0`, `0x0046ACC8`, `0x0046ACE8`); `0x0046A870`, which posts its line (`0x0046A940`, `0x0046A944`) |

No other instruction reaches `0x02EBB548`-`0x02EBB54B`. The search covered the executable's RIP-relative references (the
list's addresses are taken by `0x0046A870` and `0x0046AC90` only), its image-base-relative references, which hold none,
and a scan of `.text` for the 32-bit offsets of `0x02EBB540`, `0x02EBB542` and `0x02EBB548` from the image base, which
finds none.

## Modding notes

- The chances are immediates in `0x00390390`: `6`, `0x1E`, `0x50` with Thief's Cuffs and `3`, `0xA`,
  `0x37` without (the six `cmp r8d` sites above).
- Another accessory gets the three rolls when its equipment row's augment byte `+0x1A` is 17, for
  an item of classes 19-22. Three weapon rows (90, 98 and 139) also hold 17 there, and the rebuild
  ignores them because weapons are not in group 3.
- Another action gets the steal roll when its recipe byte `+0x08` is 49, but the steal messages stay
  keyed to action `0xA9` (`0x0046A3C9`).

## Related

- [Action results](../Battle-Actions/action-results.md) - the result record and the applier that adds
  the item.
- [Battle log](../Battle-Actions/battle-log.md) - how the steal lines are posted and filtered.
- [Battle message list](../Battle-Actions/battle-message-list.md) - the texts of events `0x2D`-`0x34`.
- [Loot drops](../Rewards-EXP-Gil-And-Loot/loot-drops.md) - the drop fields of the same enemy
  record.
- [Evaluation context](damage-formula.md) - the merged augment bits.
- [Which roll uses which generator](../Random-Numbers/which-roll-uses-which-generator.md) -
  the MT19937 stream the roll draws from.
