---
title: "Kill rewards: what an enemy's death triggers, when it gives nothing, and the order of chain, EXP, LP, gil, loot and counters"
kind: "system"
category: "Rewards: EXP, LP, gil and loot"
addresses: "0030E360, 00312280, 003171C0, 00315820, 00317090, 003112F0"
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

The status write `0030E360(stats, source, status, ...)` handles statuses being added and removed.
When status 0 (KO), 1 (Stone) or 31 (X-Zone) is added to a unit that has a battle unit on the field,
it runs the unit's death handling `00300FC0(unit, 0)` and then `00312280(source, unit)`
(`0030E875`-`0030E884`). Stone first raises event `200C`<sub>h</sub> and X-Zone event `200E`<sub>h</sub> through
`003299B0` (`0030E86D`). The status names are those of the shipped status table (see the status
pages).

Nothing happens when the status word does not actually change, and two cases return earlier:

- when the unit already has KO, Stone or X-Zone and `00377C20` reports no town flag, the write returns
  before any of this (so a Stoned enemy that is then KO'd pays once);
- for a party record of type `1B`<sub>h</sub>-`27`<sub>h</sub> (the Espers) only `00300FC0(unit, 0)` runs, never
  `00312280`.

### The Poison and Petrify markers

Adding status 2 (Petrify) or 8 (Poison) sets a marker in the unit's byte `+E9A`<sub>h</sub>: bit 1 for Petrify
(`0030E7DD`-`0030E801`), bit 0 for Poison (`0030E7B3`-`0030E7D4`). Each is 1 when the source is a
party record (stats byte `+05`<sub>h</sub> = 0) and 0 otherwise.

### Two more markers

Two more markers are set by the result applier `003112F0` on the target unit. Bit 3 is set when
the result's flag word `+2C`<sub>h</sub> has bit 19 (`00311384`-`0031138D`). Bit 2 is set when the result's
flag word `+140`<sub>h</sub> has bit 14 (`00311394`-`003113BF`). The only instructions in the image that set bit 14
of a `+140`<sub>h</sub> word are the periodic tick's HP-drain arms at `00386DF5`, `00386E1D` and `00386E2F` in
`00386C70` (linear sweep of `.text` for writes to `+140`<sub>h</sub>; the two register ORs at `0038D6D5` and
`0038E4AB` carry 1).

**The order of steps in `00312280(killer, enemy)`:**

1. **Chain.** When the defeated unit is an enemy (stats `+05`<sub>h</sub> = 1) and the killer is a party record,
   `00317ED0(enemy)` updates the chain (see the kill chain page).
2. **Counters.** `003171C0(enemy)`, for an enemy only:
   - adds 1 to counter kind 4 (`003171DF`-`003171E7`, through the thunk `00253770` into `00316A50`);
   - then, unless the actor's class nibble (`[enemy+10h]` byte `+0E`<sub>h</sub> & `F`<sub>h</sub>, `00263C20`) is 3, or
     the species word `[[enemy+E68h] + 52h]` is `FFFF`<sub>h</sub>, counts the defeat for that species through
     `00315820` (`003171FE`-`0031721F`).
3. **The reward gate.** Steps 4-8 run only when the enemy's `+E9A`<sub>h</sub> bit 3 is clear and one of these
   holds (`003122DA`-`0031232A`):
   - the killer is a party record;
   - bits 0 and 2 are both set (Poison from a party source, and the killing blow was a periodic drain);
   - status 1 (Stone) is set in the status words `+64h | +3Ch` and bit 1 is set (Petrify from a
     party source).
4. **EXP and LP** for each recipient, with level-ups (see the EXP and LP page).
5. **The reward display** `0028FB80` with the amounts computed for no recipient.
6. **Gil** (see the gil page; the conversion from step 4 is added here).
7. **The drop.** `00265020` reads the enemy actor's position. When `00319490(position)` returns
   non-zero, `003180F0(enemy, record)` rolls the loot and, when it returns non-zero, `00319CA0(record,
   position)` places it (see the loot drops page).
8. **Score.** `00317090(enemy)`, for an enemy only, adds
   `d * [E78].u16[+0] + [E70].u16[+0]` to counter kind 17. Here `d` is the enemy's level minus stats
   `+88`<sub>h</sub>, and `E70` and `E78` are its reward rows (`003170AA`-`003170D8`, through the thunk `00253770`).

`00312280` removes nothing: after the drop its only call is `00317090`.

### The per-species count

`00315820(species)` ignores species of `200`<sub>h</sub> and above. It keeps one
byte per species at `[020927C0] + 3404h + species`, where the stored value is the count plus one
(0 and 1 both mean none), saturating at `FF`<sub>h</sub>. The species is counted only when `00315D50(species)`
returns -1. That happens unless the species is in the list in `menuhandbook.bin` (three 16-bit hops
from `+08`<sub>h</sub>, then a count at `+2` and up to eleven species words at `+4`). For a listed species,
`00315D50` returns the word at `01EED130 + index*2`.

### The achievements

Counter kind 4 is a 16-bit total at `[020927C0] + 3854h`, saturating at `7FFF`<sub>h</sub>.
Kind 17 is a 32-bit total at `[020927C0] + 3868h`. Kind 11, the LP total fed in step 4, is 32-bit at
`+385C`<sub>h</sub>. All three are checked as on the gil page:

| Kind | Total | Achievement (record in `01DFE410`) | Threshold in `menuhandbook.bin` |
|---:|---|---|---|
| 4 | enemies defeated | 5, `ACH_COUNT_KILL` "Blood Dancer" (`01DFEC08`) | 500 in all nine language folders |
| 11 | LP earned | 13, `ACH_MASTER_LICENSE` "Conqueror" (`01DFF8C8`) | 48,000 in `ch`, `cn`, `in`, `kr`; the `de`, `es`, `fr`, `it`, `us` files have no entry, so the table default 0 applies and Conqueror unlocks on the first LP ever earned |
| 17 | score | 9, `ACH_COUNT_SCORE` "Record Breaker" (`01DFF268`) | 500,000 in all nine |

The achievement ids come from `00D10550 + kind*4`, and each record's first dword is its counter kind.

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| unit `+E9A`<sub>h</sub> bit 0 | bit | Poison came from a party source | `0030E7D4` |
| unit `+E9A`<sub>h</sub> bit 1 | bit | Petrify came from a party source | `0030E801` |
| unit `+E9A`<sub>h</sub> bit 2 | bit | hit by a periodic drain result | `003113BF` |
| unit `+E9A`<sub>h</sub> bit 3 | bit | pays no rewards | `0031138D` |
| `[020927C0] + 3404h + species` | `u8` | species defeat count plus one | `00315820` |
| `[020927C0] + 3854h` | `i16` | enemies defeated (kind 4) | `00316BF0` |
| `[020927C0] + 3868h` | `i32` | score (kind 17) | `00316BF0` |

## Modding notes

- `00312280` has one caller, `0030E875`-`0030E884` in the status write, so every reward goes through it.
  Hooking it sees each enemy defeat once, with the killer.
- To make an enemy pay nothing, set bit 3 of its unit byte `+E9A`<sub>h</sub>. Actions whose result carries `+2C`<sub>h</sub>
  bit 19 do this already.
- Conqueror's 48,000 LP threshold is missing from the `de`, `es`, `fr`, `it` and `us` handbook files; adding
  bit 11 to that record's mask and inserting 48,000 at its place in the packed values restores it.
- The score per enemy is the first word of its two reward rows, the same rows that hold its EXP, LP and
  gil.

## Related

- [Kill chain: chain count, chain level, the chain coin and resets](kill-chain.md)
- [EXP, LP and level-ups from kills: who receives them, the formulas, the split, the doublers and the EXP table](exp-lp-and-level-ups.md)
- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](gil.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](loot-drops.md)
