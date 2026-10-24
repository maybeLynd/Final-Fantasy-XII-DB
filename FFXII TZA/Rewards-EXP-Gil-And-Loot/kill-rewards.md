---
title: "Kill rewards: what an enemy's death triggers, when it gives nothing, and the order of chain, EXP, LP, gil, loot and counters"
kind: "system"
category: "Rewards: EXP, LP, gil and loot"
addresses: "0x0030E360, 0x00312280, 0x003171C0, 0x00315820, 0x00317090, 0x003112F0"
---

## What the player sees

An enemy that is KO'd, turned to Stone or sent to X-Zone pays out at once: the chain moves, the party
gets EXP, LP and gil, and loot may drop where it fell. An enemy killed by another enemy pays nothing.
Enemies finished off by party-applied Poison, or turned to Stone through party-applied Petrify, still
pay. Every enemy defeat counts toward the **Blood Dancer** achievement (500 defeats) and the
**Record Breaker** achievement (a score total of 500,000), and each kind of monster has its own defeat
count.

## How it works

### The trigger

The status write `0x0030E360(stats, source, status, ...)` handles statuses being added and removed.
When status 0 (KO), 1 (Stone) or 31 (X-Zone) is added to a unit that has a battle unit on the field,
it runs the unit's death handling `0x00300FC0(unit, 0)` and then `0x00312280(source, unit)`
(`0x0030E875`-`0x0030E884`). Stone first raises event `0x200C` and X-Zone event `0x200E` through
`0x003299B0` (`0x0030E86D`). The status names are those of the shipped status table (see the status
pages).

Nothing happens when the status word does not actually change, and two cases return earlier:

- when the unit already has KO, Stone or X-Zone and `0x00377C20` reports no town flag, the write returns
  before any of this (so a Stoned enemy that is then KO'd pays once);
- for a party record of type `0x1B`-`0x27` (the Espers) only `0x00300FC0(unit, 0)` runs, never
  `0x00312280`.

### The Poison and Petrify markers

Adding status 2 (Petrify) or 8 (Poison) sets a marker in the unit's byte `+0xE9A`: bit `0x2` for Petrify
(`0x0030E7DD`-`0x0030E801`), bit `0x1` for Poison (`0x0030E7B3`-`0x0030E7D4`). Each is 1 when the source is a
party record (stats byte `+0x05` = 0) and 0 otherwise.

### Two more markers

Two more markers are set by the result applier `0x003112F0` on the target unit. Bit `0x8` is set when
the result's flag word `+0x2C` has bit `0x80000` (`0x00311384`-`0x0031138D`). Bit `0x4` is set when the result's
flag word `+0x140` has bit `0x4000` (`0x00311394`-`0x003113BF`). The only instructions in the image that set bit `0x4000`
of a `+0x140` word are the periodic tick's HP-drain arms at `0x00386DF5`, `0x00386E1D` and `0x00386E2F` in
`0x00386C70` (linear sweep of `.text` for writes to `+0x140`; the two register ORs at `0x0038D6D5` and
`0x0038E4AB` carry 1).

**The order of steps in `0x00312280(killer, enemy)`:**

1. **Chain.** When the defeated unit is an enemy (stats `+0x05` = 1) and the killer is a party record,
   `0x00317ED0(enemy)` updates the chain (see the kill chain page).
2. **Counters.** `0x003171C0(enemy)`, for an enemy only:
   - adds 1 to counter kind 4 (`0x003171DF`-`0x003171E7`, through the thunk `0x00253770` into `0x00316A50`);
   - then, unless the actor's class nibble (`[enemy+0x10]` byte `+0x0E` & `0xF`, `0x00263C20`) is 3, or
     the species word `[[enemy+0xE68] + 0x52]` is `0xFFFF`, counts the defeat for that species through
     `0x00315820` (`0x003171FE`-`0x0031721F`).
3. **The reward gate.** Steps 4-8 run only when the enemy's `+0xE9A` bit `0x8` is clear and one of these
   holds (`0x003122DA`-`0x0031232A`):
   - the killer is a party record;
   - bits `0x1` and `0x4` are both set (Poison from a party source, and the killing blow was a periodic drain);
   - status 1 (Stone) is set in the status words `+0x64 | +0x3C` and bit `0x2` is set (Petrify from a
     party source).
4. **EXP and LP** for each recipient, with level-ups (see the EXP and LP page).
5. **The reward display** `0x0028FB80` with the amounts computed for no recipient.
6. **Gil** (see the gil page; the conversion from step 4 is added here).
7. **The drop.** `0x00265020` reads the enemy actor's position. When `0x00319490(position)` returns
   non-zero, `0x003180F0(enemy, record)` rolls the loot and, when it returns non-zero, `0x00319CA0(record,
   position)` places it (see the loot drops page).
8. **Score.** `0x00317090(enemy)`, for an enemy only, adds
   `d * [E78].u16[+0] + [E70].u16[+0]` to counter kind 17. Here `d` is the enemy's level minus stats
   `+0x88`, and `E70` and `E78` are its reward rows (`0x003170AA`-`0x003170D8`, through the thunk `0x00253770`).

`0x00312280` removes nothing: after the drop its only call is `0x00317090`.

### The per-species count

`0x00315820(species)` ignores species of `0x200` and above. It keeps one
byte per species at `[0x020927C0] + 0x3404 + species`, where the stored value is the count plus one
(0 and 1 both mean none), saturating at `0xFF`. The species is counted only when `0x00315D50(species)`
returns -1. That happens unless the species is in the list in `menuhandbook.bin` (three 16-bit hops
from `+0x08`, then a count at `+2` and up to eleven species words at `+4`). For a listed species,
`0x00315D50` returns the word at `0x01EED130 + index*2`.

### The achievements

Counter kind 4 is a 16-bit total at `[0x020927C0] + 0x3854`, saturating at `0x7FFF`.
Kind 17 is a 32-bit total at `[0x020927C0] + 0x3868`. Kind 11, the LP total fed in step 4, is 32-bit at
`+0x385C`. All three are checked as on the gil page:

| Kind | Total | Achievement (record in `0x01DFE410`) | Threshold in `menuhandbook.bin` |
|---:|---|---|---|
| 4 | enemies defeated | 5, `ACH_COUNT_KILL` "Blood Dancer" (`0x01DFEC08`) | 500 in all nine language folders |
| 11 | LP earned | 13, `ACH_MASTER_LICENSE` "Conqueror" (`0x01DFF8C8`) | 48,000 in `ch`, `cn`, `in`, `kr`; the `de`, `es`, `fr`, `it`, `us` files have no entry, so the table default 0 applies and Conqueror unlocks on the first LP ever earned |
| 17 | score | 9, `ACH_COUNT_SCORE` "Record Breaker" (`0x01DFF268`) | 500,000 in all nine |

The achievement ids come from `0x00D10550 + kind*4`, and each record's first dword is its counter kind.

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| unit `+0xE9A` bit `0x1` | bit | Poison came from a party source | `0x0030E7D4` |
| unit `+0xE9A` bit `0x2` | bit | Petrify came from a party source | `0x0030E801` |
| unit `+0xE9A` bit `0x4` | bit | hit by a periodic drain result | `0x003113BF` |
| unit `+0xE9A` bit `0x8` | bit | pays no rewards | `0x0031138D` |
| `[0x020927C0] + 0x3404 + species` | `u8` | species defeat count plus one | `0x00315820` |
| `[0x020927C0] + 0x3854` | `i16` | enemies defeated (kind 4) | `0x00316BF0` |
| `[0x020927C0] + 0x3868` | `i32` | score (kind 17) | `0x00316BF0` |

## Modding notes

- `0x00312280` has one caller, `0x0030E875`-`0x0030E884` in the status write, so every reward goes through it.
  Hooking it sees each enemy defeat once, with the killer.
- To make an enemy pay nothing, set bit `0x8` of its unit byte `+0xE9A`. Actions whose result carries `+0x2C`
  bit `0x80000` do this already.
- Conqueror's 48,000 LP threshold is missing from the `de`, `es`, `fr`, `it` and `us` handbook files; adding
  bit `0x800` to that record's mask and inserting 48,000 at its place in the packed values restores it.
- The score per enemy is the first word of its two reward rows, the same rows that hold its EXP, LP and
  gil.

## Related

- [Kill chain: chain count, chain level, the chain coin and resets](kill-chain.md)
- [EXP, LP and level-ups from kills: who receives them, the formulas, the split, the doublers and the EXP table](exp-lp-and-level-ups.md)
- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](gil.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](loot-drops.md)
