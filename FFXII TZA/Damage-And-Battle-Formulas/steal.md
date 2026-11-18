[Home](../../README.md) / [Damage and battle formulas](README.md) / Steal

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Steal: the item chances, the three Thief's Cuffs rolls and the steal messages | system | Damage and battle formulas | Damage and formulas | How a Steal attempt picks from an enemy's common, uncommon and rare steal items: when an enemy has nothing left to steal, the single first-hit roll at 3, 10 and 55 percent, the three independent rolls at 6, 30 and 80 percent with Thief's Cuffs, the debug value that can force an item, how a won item reaches the inventory, and which battle message each outcome posts. | 0x00390390, 0x00385F60, 0x003847C0, 0x0030FED0, 0x0023A570, 0x00385BA0, 0x003112F0, 0x00469EC0, 0x0046A870, 0x0017D450 |

## What the player sees

An enemy can carry up to three items to steal: a common, an uncommon and a rare one.

- **Without Thief's Cuffs** one attempt gives at most one item. The rare item is tried first, then
  the uncommon one, then the common one.
- **With Thief's Cuffs** each of the three items is rolled on its own, so one attempt can take two or
  all three.
- **Once something has been stolen** from an enemy, every later attempt on it fails with "has nothing
  to steal".
- **A roll that lands on an item the enemy does not carry** fails with "couldn't steal from".

The three items are words of the enemy's own record, and which of them are still there is set when the enemy is first
set up from its spawn record. Thief's Cuffs work through their equipment row, whose augment byte gives the wearer
augment 17, Thievery, the bit the roll tests.

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

The resolver `0x00385F60` builds the evaluation context with `0x003847C0`¹, passing the result
record as context `+0x10` and the user's stats record for the augment bits. It calls each slot of the
committed segment with `(userStats, targetStats, &context)` at `0x003863D0` and leaves the segment when
`0x02AEDFB8` reads 1².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003860D5` |
| ² | `0x003863D7` |

</details>

### Which items can be stolen

The roll finds the target's battle unit¹ and, for an enemy-side unit (byte `+5` of the
stats record at unit `+0x698` is 1), reads the enemy's record at unit `+0xE60`². Its words `+0x32`, `+0x34` and `+0x36` are the common, uncommon and rare item,
`0xFFFF` meaning no item. Byte `+0x14` of the spawn record at unit `+0x6A0` holds one bit per item still
available: bit `0x1`, `0x2` and `0x4`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031B860` |
| ² | `0x003903AD`-`0x003903DB` |

</details>

The roll does not read its first argument. When `0x0031B860` answers null for the target, or the unit
has no stats record, or that record's byte `+0x05` is not 1, the record pointer is 0 and the word at
address `0x32` is read¹. The unit is asked for again before each bit test; a
null unit or a null spawn record there also ends the attempt as nothing to steal². Each answer of `0x0031B860` is
stored in `0x02EBF188`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003903B9`-`0x003903DB` |
| ² | `0x003903FE`-`0x0039041C`, `0x0039042D`-`0x0039044B`, `0x0039045E`-`0x0039047C` |

</details>

The attempt ends as "nothing to steal" in either of these cases:

- all three item words are `0xFFFF`¹;
- an item word is set and its bit is clear².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003903DB`-`0x003903F3` |
| ² | `0x0039041E`, `0x0039044D`, `0x0039047E` |

</details>

That exit sets bit `0x800000` of the result's `+0x2C` and `0x02AEDFBC` = 1, and returns¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0039048A`-`0x003904A0` |

</details>

### When the availability bits change

`BattleUnit_ApplyUnitDefinition`¹ sets them when the spawn record is fresh, that is when
its byte `+0` has neither bit `0x1` nor bit `0x4`². It writes byte `+0x14` = 0 and then sets bit
`0x1`, `0x2` or `0x4` for each of the common, uncommon and rare item words that is not `0xFFFF`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023A570` |
| ² | `0x0023A791` |
| ³ | `0x0023A7AE`-`0x0023A7E4` |

</details>

A won item clears its bit twice: the result's first step `0x00385BA0` clears bit `0x4`, `0x2` and `0x1` for the won
rare, uncommon and common item¹, and the applier clears it again². Because any set item word with a clear bit blocks the next attempt, an enemy can be
stolen from successfully once.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00385C17`, `0x00385C41`, `0x00385C6B` |
| ² | `0x0031146F` |

</details>

### The Thief's Cuffs test

The roll branches on bit `0x2` of context byte `+0x1C`¹. Context bytes `+0x1A`-`+0x29` merge the
user's two augment layers: bit value `1 << (id & 7)` of byte `+0x1A + id / 8` is set when the user's stats
record has augment `id` in its layer `+0x68` or `+0x78`². Bit `0x2` of `+0x1C` is therefore
the augment Thievery (17).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003904A5` |
| ² | `0x00384820`-`0x00384858` |

</details>

Thief's Cuffs are equipment row 354 of `battle_pack.bin` (named in the equipment-name table), and the
row's augment byte `+0x1A` is 17. The stats rebuild `0x0030FED0` collects the augment byte of each of the
five equipped items whose group¹ is 3, which is equipment classes 19-22², and
Thief's Cuffs are class 21³. It then moves layer `+0x78` to that set⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031E9A0` |
| ² | `0x0031E9F0` |
| ³ | `0x00310080`-`0x00310121` |
| ⁴ | `0x00310303`-`0x003103A3` |

</details>

### The three rolls with Thief's Cuffs

With the bit set, the roll draws three numbers `r = MT19937 % 100`¹ and tests each item on
its own:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00379CD0` |

</details>

| Item | Wins when | Test | Sets |
|---|---|---|---|
| Rare | `r < 6` and the rare word is set | `0x003904CD`-`0x003904EB` | `0x02AEE04E` |
| Uncommon | `r < 30` and the uncommon word is set | `0x0039050A`-`0x00390527` | `0x02AEE04D` |
| Common | `r < 80` and the common word is set | `0x00390546`-`0x0039055B` | `0x02AEE04C` |

When none of the three is set, it sets `0x02AEDFBC` = 1 and `0x02AEDFB8` = 1¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00390563`-`0x00390584` |

</details>

### The single roll without Thief's Cuffs

Without the bit, the roll draws a new number only after the previous test missed:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `r < 3` wins the rare item: `0x02AEE04E` = 1 when the rare word is set, otherwise the attempt fails. | `0x003905B8`, `0x0039066A`<br>`0x0039057E` |
| 2 | Otherwise `r < 10` wins the uncommon item: `0x02AEE04D` = 1 when its word is set, otherwise the attempt fails. | `0x003905E9`, `0x00390650` |
| 3 | Otherwise `r < 55` wins the common item: `0x02AEE04C` = 1 when its word is set, otherwise the attempt fails. | `0x00390612`, `0x00390635`<br>`0x00390495` |
| 4 | Otherwise the attempt fails. | `0x00390621`-`0x00390626` |

A failure here sets `0x02AEDFBC` = 1 and leaves bit `0x800000` clear. For an enemy with all three items:

```python
rare = 0.03
uncommon = 0.97 * 0.10        = 0.097
common = 0.97 * 0.90 * 0.55 = 0.480
nothing = 0.97 * 0.90 * 0.45 = 0.393
with Thief's Cuffs, nothing = 0.94 * 0.70 * 0.20 = 0.132
```

Without Thievery a rare or an uncommon win also stores 1 in `0x02AEDFB8`¹; a common win stores `0x02AEE04C` alone². The
failures of steps 1, 2 and 4 store 1 in both `0x02AEDFBC` and `0x02AEDFB8`³, and
the failure of step 3 stores `0x02AEDFBC` alone⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0039066A`-`0x00390670`, `0x00390650`-`0x00390656`, `0x00390584` |
| ² | `0x00390635`-`0x0039063C` |
| ³ | `0x0039057E`-`0x00390584` |
| ⁴ | `0x00390495`-`0x003904A0` |

</details>

With Thievery a common win returns at once¹, and a rare or uncommon win whose
item word is `0xFFFF` leaves its flag byte as it was².
The test at `0x00390563`-`0x0039057C` reads the three flag bytes as they then are, so a byte that was not
0 on entry also keeps the two failure stores from being made.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0039055B`-`0x00390561` |
| ² | `0x003904DD`-`0x003904EB`, `0x00390519`-`0x00390527` |

</details>

### The debug value that forces an item

Each test also wins when `0x0017D450` returns that item's number: 0 for the common item, 1 for the
uncommon and 2 for the rare (the `test` and `cmp` after each draw). `0x0017D450` returns
`[0x001D50D0() + 0xE5C]`, a field of the settings object that its builder `0x001CCB20` sets to -1¹, which forces nothing.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001CCE1F` |

</details>

### Where the result goes

`BattleFormula_ResetScratchState`¹ zeroes `0x02AEDFB8`, `0x02AEDFBC` and `0x02AEE04C`-`0x02AEE04E`², and the resolver calls it before any slot runs³. After the slots, the resolver:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003849B0` |
| ² | `0x003849BC`-`0x003849C2`, `0x00384A1C`-`0x00384A23` |
| ³ | `0x00386001` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | sets the result kind `+0x04` to 6 when `0x02AEDFBC` is set, and for kind 6 clears bits `0x1`, `0x4` and `0x8` of `+0x18`; | `0x003866C1`-`0x003866CA`<br>`0x003866EB` |
| 2 | copies `0x02AEE04C`, `0x02AEE04D` and `0x02AEE04E` into the result's `+0x32`, `+0x33` and `+0x34`. | `0x003867F1`-`0x0038680C` |

For an enemy-side target, the applier `0x003112F0` adds one of each won item (its item word, when not
`0xFFFF`) with `0x003008A0` and clears its availability bit¹
([Action results](../Battle-Actions/action-results.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00311430`-`0x0031148B` |

</details>

### The battle messages

The post-result dispatcher `0x00469EC0` posts the steal lines
([Battle message list](../Battle-Actions/battle-message-list.md) has their texts):

| Outcome | Event | Site |
|---|---|---|
| Failed, bit `0x800000` set | `0x33` (steal failed, nothing to steal) | `0x0046A3C4`-`0x0046A3F0` |
| Failed, bit `0x800000` clear | `0x34` (couldn't steal from) | `0x0046A3C4`-`0x0046A3F0` |
| Won items | the stolen-goods lines of `0x0046A870` | `0x0046A504` |

`0x0046A870` gathers the won items into a three-entry list at `0x02EBB540` (`0x0046AC90` adds 1 to the count
of an item already in the list) and posts one line per entry¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0046A940`-`0x0046A9A2` |

</details>

| Entry | Gil (`0xE000` id) | One item | Several of one item |
|---|---|---|---|
| First | `0x31` | `0x2E` | `0x2D` |
| Later | `0x32` | `0x30` | `0x2F` |

`0x0046A870` takes the source, the target record and the result in its second to fourth arguments. It does nothing
for a null target record¹. It empties the list and keeps the target's unit in `0x02EBF188`, and stops
there when the record has no unit, the unit has no stats record or a record that is not an enemy's, or the unit's
`+0xE60` is null².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0046A873` |
| ² | `0x0046A88D`-`0x0046A8E1` |

</details>

The won items are those whose result bytes `+0x32`, `+0x33` and `+0x34` are set: the record's `+0x32`, `+0x34` and
`+0x36`, in that order¹. An entry with count 0 that is not gil posts no line². Each line goes through `0x0046AB10(source, event, &block)` with the source at block `+0x00`, the target
record at `+0x08`, the item word at `+0x20` and the count at `+0x24`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0046A8E7`-`0x0046A90F` |
| ² | `0x0046A970`, `0x0046A993` |
| ³ | `0x0046A916`-`0x0046A9A2` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

The enemy's record at unit `+0xE60`, the fields the steal reads:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x32` | `u16` | stealCommon | common steal item; `0xFFFF` = no item (`0x00390390`, `0x0023A570`) |
| `+0x34` | `u16` | stealUncommon | uncommon steal item; `0xFFFF` = no item |
| `+0x36` | `u16` | stealRare | rare steal item; `0xFFFF` = no item |

The spawn record at unit `+0x6A0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x14` | `u8` | stealLeft | bits `0x1`, `0x2`, `0x4`: the common, uncommon and rare item is still available (`0x0023A570`, `0x00390390`, `0x003112F0`) |

</details>

## State

<details>
<summary>Show the state it keeps</summary>

The won-items list is three 4-byte entries from `0x02EBB540`: the item id (`u16`) at `+0`, the count (`u8`) at `+2`; no
instruction uses byte `+3`. `0x0046A870` empties it first¹; `0x0046AC90(item)` adds 1 to the
count of an entry that holds the item, or puts the item with count 1 in the first entry whose count is 0²; gil (`0xE000` ids) always takes a new entry³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0046A88D`, `0x0046A897` |
| ² | `0x0046ACC0`-`0x0046AD0C` |
| ³ | `0x0046ACA5`-`0x0046ACB0` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBB548` | `u8[4]` | 0 | the third entry: the third different item or gil won, which is the rare item when all three are won and differ | `0x0046A870`, 0 (`0x0046A897`); `0x0046AC90`: the count (`0x0046ACFE`), the item and count 1 (`0x0046AD07`, `0x0046AD0C`) | `0x0046AC90` (`0x0046ACC0`, `0x0046ACC8`, `0x0046ACE8`); `0x0046A870`, which posts its line (`0x0046A940`, `0x0046A944`) |

No other instruction reaches `0x02EBB548`-`0x02EBB54B`. The list's addresses are taken by `0x0046A870` and `0x0046AC90` only.

</details>

## Modding notes

- The chances are immediates in `0x00390390`: `6`, `0x1E`, `0x50` with Thief's Cuffs and `3`, `0xA`,
  `0x37` without (the six `cmp r8d` sites above).
- Another accessory gets the three rolls when its equipment row's augment byte `+0x1A` is 17, for
  an item of classes 19-22. Three weapon rows (90, 98 and 139) also hold 17 there, and the rebuild
  ignores them because weapons are not in group 3.
- Another action gets the steal roll when its recipe byte `+0x08` is 49, but the steal messages stay
  keyed to action `0xA9`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0046A3C9` |

</details>

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
