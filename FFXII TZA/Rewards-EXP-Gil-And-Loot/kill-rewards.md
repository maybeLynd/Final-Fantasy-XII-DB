[Home](../../README.md) / [Rewards: EXP, LP, gil and loot](README.md) / Kill rewards

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Kill rewards: what an enemy's death triggers, when it gives nothing, and the order of chain, EXP, LP, gil, loot and counters | system | Rewards: EXP, LP, gil and loot | EXP, loot and progression | The statuses whose arrival on an enemy starts the defeat sequence, the reward gate (party kills, party-applied Poison and Petrify, the no-reward flag), and every step in order: chain, kill and species counters, EXP and LP, the reward display, gil, the drop and the score counter, with the achievements they feed. | 0x0030E360, 0x00312280, 0x003171C0, 0x00315820, 0x00317090, 0x003112F0 |

## What the player sees

An enemy that is KO'd, turned to Stone or sent to X-Zone pays out at once: the chain moves, the party
gets EXP, LP and gil, and loot may drop where it fell. An enemy killed by another enemy pays nothing.
Enemies finished off by party-applied Poison, or turned to Stone through party-applied Petrify, still
pay. Every enemy defeat, paying or not, counts toward the **Blood Dancer** achievement (500 defeats),
and each kind of monster has its own defeat count.

The **Record Breaker** achievement (a score total of
500,000) grows only for the defeats that pay out, and by the score scripts add with `addclanpoint`
([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)).

## How it works

### The trigger

The status write `0x0030E360(stats, source, status, ...)` handles statuses being added and removed.
When status 0 (KO), 1 (Stone) or 31 (X-Zone) is added to a unit that has a battle unit on the field,
it runs the unit's death handling `0x00300FC0(unit, 0)` and then `0x00312280(source, unit)`¹. Stone first raises event `0x200C` and X-Zone event `0x200E` through
`0x003299B0`². The status names are those of the shipped status table (see
[Statuses](../Status-Effects-And-KO/statuses.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030E875`-`0x0030E884` |
| ² | `0x0030E86D` |

</details>

Nothing happens when the status word does not actually change, and two cases return earlier:

- when the unit already has KO, Stone or X-Zone and `0x00377C20` reports no town flag, the write returns
  before any of this (so a Stoned enemy that is then KO'd pays once);
- for a party record of type `0x1B`-`0x27` (the Espers) only `0x00300FC0(unit, 0)` runs, never
  `0x00312280`.

### The Poison and Petrify markers

Adding status 2 (Petrify) or 8 (Poison) sets a marker in the unit's byte `+0xE9A`: bit `0x2` for Petrify¹, bit `0x1` for Poison². Each is 1 when the source is a
party record (stats byte `+0x05` = 0) and 0 otherwise.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030E7DD`-`0x0030E801` |
| ² | `0x0030E7B3`-`0x0030E7D4` |

</details>

### Two more markers

Two more markers are set by the result applier `0x003112F0` on the target unit. Bit `0x8` is set when
the result's flag word `+0x2C` has bit `0x80000`¹. Bit `0x4` is set when the result's
flag word `+0x140` has bit `0x4000`². The only instructions in the image that set bit `0x4000`
of a `+0x140` word are the periodic tick's HP-drain arms at `0x00386DF5`, `0x00386E1D` and `0x00386E2F` in
`0x00386C70` (linear sweep of `.text` for writes to `+0x140`; the two register ORs at `0x0038D6D5` and
`0x0038E4AB` carry 1).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00311384`-`0x0031138D` |
| ² | `0x00311394`-`0x003113BF` |

</details>

**The order of steps in `0x00312280(killer, enemy)`:**

| Step | What happens | Where in the code |
|---|---|---|
| 1 | **Chain.** When the defeated unit is an enemy (stats `+0x05` = 1) and the killer is a party record, `0x00317ED0(enemy)` updates the chain (see [Kill chain](kill-chain.md)). |   |
| 2 | **Counters.** `0x003171C0(enemy)`, for an enemy only:<br>• adds 1 to counter kind 4 (`0x003171DF`-`0x003171E7`, through the thunk `0x00253770` into `0x00316A50`);<br>• then, unless the actor's class nibble (`[enemy+0x10]` byte `+0x0E` & `0xF`, `0x00263C20`) is 3, or the species word `[[enemy+0xE68] + 0x52]` is `0xFFFF`, counts the defeat for that species through `0x00315820`. | `0x003171FE`-`0x0031721F` |
| 3 | **The reward gate.** Steps 4-8 run only when the defeated unit's stats record `+0x698` is not null and has byte `+0x05` = 1, its `+0xE9A` bit `0x8` is clear and one of these holds:<br>• the killer is a party record;<br>• bits `0x1` and `0x4` are both set (Poison from a party source, and the killing blow was a periodic drain);<br>• status 1 (Stone) is set in the status words `+0x64 \| +0x3C` and bit `0x2` is set (Petrify from a party source). | `0x003122DA`-`0x003122EE`<br>`0x003122F4`-`0x0031232A` |
| 4 | **EXP and LP** for each recipient, with level-ups (see [EXP, LP and level-ups](exp-lp-and-level-ups.md)). |   |
| 5 | **The reward display** `0x0028FB80` with the amounts computed for no recipient. |   |
| 6 | **Gil** (see [Gil](gil.md); the conversion from step 4 is added here). |   |
| 7 | **The drop.** `0x00265020` reads the enemy actor's position. When `0x00319490(position)` returns non-zero, `0x003180F0(enemy, record)` rolls the loot and, when it returns non-zero, `0x00319CA0(record, position)` places it (see [Loot drops](loot-drops.md)). |   |
| 8 | **Score.** `0x00317090(enemy)`, for an enemy only, adds `d * [E78].u16[+0] + [E70].u16[+0]` to counter kind 17. Here `d` is the enemy's level minus stats `+0x88`, and `E70` and `E78` are its reward rows (`0x003170AA`-`0x003170D8`, through the thunk `0x00253770`). |   |

`0x00312280` removes nothing: after the drop its only call is `0x00317090`.

### The per-species count

`0x00315820(species)` ignores species of `0x200` and above. It keeps one
byte per species at `[0x020927C0] + 0x3404 + species`, where the stored value is the count plus one
(0 and 1 both mean no defeats counted), saturating at `0xFF`.

The species is counted only when `0x00315D50(species)`
returns -1. That happens unless the species is in the list in `menuhandbook.bin` (three 16-bit hops
from `+0x08`, then a count at `+2` and up to eleven species words at `+4`) at a position whose word in
`0x01EED130` is not -1. For a listed species,
`0x00315D50` returns the word at `0x01EED130 + index*2`, sign-extended¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00315DAD`-`0x00315DB7` |

</details>

Of the eleven words only positions 1 (167) and 10 (170) hold a value other than -1, so a species at any other
position of the list is counted. With no file at `[0x022C2550]`, a zero hop or a species not in the list,
`0x00315D50` returns -1¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00315D5D`-`0x00315DBC` |

</details>

### The achievements

Counter kind 4 is a 16-bit total at `[0x020927C0] + 0x3854`, saturating at `0x7FFF`.
Kind 17 is a 32-bit total at `[0x020927C0] + 0x3868`. Kind 11, the LP total fed in step 4, is 32-bit at
`+0x385C`. All three are checked as on the [gil page](gil.md):

| Kind | Total | Achievement (record in `0x01DFE410`) | Threshold in `menuhandbook.bin` |
|---:|---|---|---|
| 4 | enemies defeated | 5, `ACH_COUNT_KILL` "Blood Dancer" (`0x01DFEC08`) | 500 in all nine language folders |
| 11 | LP earned | 13, `ACH_MASTER_LICENSE` "Conqueror" (`0x01DFF8C8`) | 48,000 in the `in` and `ch` copies, the only ones the game reads: every language's kind 7 array names id 200 as one of them; the `de`, `es`, `fr`, `it` and `us` copies have no entry, but no array names them |
| 17 | score | 9, `ACH_COUNT_SCORE` "Record Breaker" (`0x01DFF268`) | 500,000 in all nine |

The achievement ids come from `0x00D10550 + kind*4`, and each record's first dword is its counter kind.

## State

<details>
<summary>Show the state it keeps</summary>

| Address | Width | Meaning | Written by |
|---|---|---|---|
| unit `+0xE9A` bit `0x1` | bit | Poison came from a party source | `0x0030E7D4` |
| unit `+0xE9A` bit `0x2` | bit | Petrify came from a party source | `0x0030E801` |
| unit `+0xE9A` bit `0x4` | bit | hit by a periodic drain result | `0x003113BF` |
| unit `+0xE9A` bit `0x8` | bit | pays no rewards | `0x0031138D` |
| `[0x020927C0] + 0x3404 + species` | `u8` | species defeat count plus one | `0x00315820` |
| `[0x020927C0] + 0x3854` | `i16` | enemies defeated (kind 4) | `0x00316BF0` |
| `[0x020927C0] + 0x3868` | `i32` | score (kind 17) | `0x00316BF0` |

</details>

## Modding notes

- `0x00312280` has one caller, `0x0030E875`-`0x0030E884` in the status write, so every reward goes through it.
  Hooking it sees each enemy defeat once, with the killer.
- To make an enemy pay nothing, set bit `0x8` of its unit byte `+0xE9A`. Actions whose result carries `+0x2C`
  bit `0x80000` do this already.
- The calculator's slots 190, 196 and 162 ([slot list](../Damage-And-Battle-Formulas/formula-slots.md)) set that bit
 ¹. They end the committed lists of recipe 9 (Warp, Warp Mote and Kill), 58
  (Poach) and 88 (Cannibalize) ([recipes](../Damage-And-Battle-Formulas/formula-recipes.md)).
- Each runs only when no earlier slot of its list stops the list²: the hit roll of slot 40
  (recipe 9, `0x0038968D`-`0x003896A0`) or 47 (Poach, `0x00389BB1`-`0x00389BC0`), slot 14 when a Poach target lacks HP
  Critical³, or slot 0 when a Poach or Cannibalize target has Safety⁴.
- Conqueror's 48,000 LP threshold is absent from the `de`, `es`, `fr`, `it` and `us` handbook copies, which no
  path array names; the `in` and `ch` copies the game reads hold it, so every language needs 48,000 LP.
- The score per enemy is the first word of its two reward rows, the same rows that hold its EXP, LP and
  gil.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0039017E`, `0x003907C8`, `0x0038F6DA` |
| ² | `0x003863D7`-`0x003863DE` |
| ³ | `0x003889C0`-`0x003889D8` |
| ⁴ | `0x00387F40`-`0x00387F56` |

</details>

## Related

- [Kill chain: chain count, chain level, the chain coin and resets](kill-chain.md)
- [EXP, LP and level-ups from kills: who receives them, the formulas, the split, the doublers and the EXP table](exp-lp-and-level-ups.md)
- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](gil.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](loot-drops.md)

---

[EXP, LP and level-ups from kills →](exp-lp-and-level-ups.md)
