---
title: "Enemy AI: the order sets an enemy tries, the phase a command switches to, what an enemy notices and when an order is replaced"
kind: "system"
category: "Enemy AI and gambits"
addresses: "00305AB0, 00305CC0, 002FDDA0, 0023A570, 003247F0, 00324F20, 00325060, 0030F130, 00308610, 003105D0"
---

## What the player sees

An enemy acts from an authored list of orders, tried top to bottom like a gambit list. The list is split
into phases, and the enemy's own orders switch it from one phase to another. An enemy can only pick a
target it has noticed:

- a unit it can see;
- a unit inside either of its two detection radii, the second only for a target below 40 % HP;
- a unit that hit it a short time ago;
- with Lure on a foe it notices, only the Lure foes, besides its own side.

When nothing in its list fits, the enemy waits.

## How it works

### The order sets

Every unit carries four order-set pointers, tried by `00305AB0` in a fixed order ([Gambits](gambits.md)
has the whole cascade):

| Set offset | Holds | Installed by |
|---|---|---|
| `+0x6E8` | the re-plan set: `01EEC3C0` for a party record, `01EEC410` otherwise | `00313458`, `003134DA`, `002FED9E`, `002FEE05`, `0030126B`, `0030F331` |
| `+0x6F8` | the issued command's set `01EEC2D0`, target in `+0x748` | `00311DD4`-`00311DE1` |
| `+0x6E0` | the unit's own list, walked with its subgroup `+0x6B5` | the unit definition, orders `0x4112`-`0x4115` |
| `+0x6F0` | the default set `01E09350` | `0023ABA6`-`0023ABB5`, on the party-table path (`0023AB7E`) |

An enemy-table unit never walks `+0x6F8`, because that step is for party records (`00305BE7`-`00305C03`), and
its `+0x6F0` stays empty from the reset (`00236BB6`). Its cascade is the re-plan set, then its own list, then
the wait `0x4021` from `01EEC298` (`00305C7E`-`00305C9B`).

### The built-in sets

The image holds six one-subgroup sets and one bare order record (`.data`, read at the addresses below). The
wait record `01EEC298` has no count header; `00305AB0` commits it directly with the action commit `0030F760`
([Action commit](../Battle-Actions/action-commit.md)) instead of walking it (`00305C7E`-`00305C9B`):

| Set | Order | Flags | Used for |
|---|---|---|---|
| `01EEC320` | `0x0096` Attack, then `0x4125` | - | a Confused unit, or an enemy with Berserk (`00305B89`) |
| `01EEC370` | `0x0096` Attack | - | a party record with Berserk (`00305BDE`) |
| `01EEC3C0` | `0x4022`, follow the party | `0x2000` | party re-plan set |
| `01EEC410` | `0x414D`, flip the combat stance | - | enemy re-plan set |
| `01EEC2D0` | `0x0096` Attack, relation mode 10 | - | an issued command: attack the unit in `+0x748` |
| `01E09350` | `0x4124`, follow the leader | `0x2000` | the default set |
| `01EEC298` | `0x4021`, wait | `0x2000` | the last resort, committed as a single order |

The attacks in the Confuse and Berserk sets carry relation mode 1 in their test, so they pick a foe;
under Confuse the two sides are swapped ([Gambits](gambits.md)). The orders are on
[Battle orders](../Battle-Actions/battle-orders.md).

### Where an enemy's list comes from

An enemy's own list is a set from the order-set directory `[02EBF168]`, which the area file provides
([Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)):
a `u16` count, then one 32-bit offset per set, each resolved against `01F83530` by `0020E600`.

- The unit definition installs the set named by the definition row's word `+0x50` (`0023A94D`-`0023A95E`).
- Orders `0x4112`-`0x4115` install the set named by word `+0x50`, `+0x52`, `+0x54` or `+0x56` of the row
  (`+0xE60`), bounded by the directory's count, and set the subgroup to 0 (`002FE025`-`002FE0B2`). Only an
  enemy-table unit takes them (`002FE03E`).
- Orders `0x4116`-`0x4121` set the subgroup `+0x6B5` to the id's low byte minus `0x16`, so subgroups 0 to 11
  (`002FE0B3`-`002FE0D2`).

So an enemy has up to four lists and twelve phases in each. The walk `00305CC0` starts a subgroup after the
orders of all earlier subgroups ([Gambits](gambits.md)). Every shipped set and order is on
[Enemy order sets](enemy-order-sets.md).

### The perception list

Each unit keeps a list of up to 32 units it has noticed at `+0xBC0`, in the 0x208-byte target-list layout of
[Area of effect](../Battle-Actions/area-of-effect.md): count `+0xBC4`, entries from `+0xBC8`. An order id
takes this list as its candidates (`00301599`). An action takes it through `0030F130`: the whole list, or,
when the unit's `+0x6D0` radius is set, the units within that radius plus their own size of `+0x6C0`
(`0030F1CE`-`0030F25A`). It also adds
each of party slots 0-3 that the action may target while it has KO, Stone or X-Zone (`0030F261`-`0030F2B2`).

### Rebuilding the list

`003247F0(unit)` rebuilds the list (`00324857`-`00324ED2`):

1. It clears it. A unit that is inactive, has KO, Stone or X-Zone without the field's bit 15, or is an
   enemy-table unit whose spawn record's first byte has a bit of `0x30` keeps it empty (`00324881`-`003248D0`).
2. It marks every active unit that passes the eligibility test `002FFEF0` (`00324920`-`0032496E`). An
   enemy-table unit whose class row byte `+0x18 & 0x0E` is 4 notices all of them, and steps 3-6 are skipped
   (`003248E3`-`00324909`, `00324976`).
3. **Sight.** The query `003919B0` around the unit's position `+0xE0` uses its floats `+0x64`, `+0x68` and
   `+0x160`. A result is kept when it is not an Invisible unit of another side (`0030BCB0`), its height differs by at most `+0x68`, and the
   test `0032A4D0` passes (`0032497E`-`00324ABA`).
4. **The two radii,** enemy-table units only. Units within the class row's byte `+0x25` that lack effect 33
   and pass `0032A4D0` are kept (`00324AC0`-`00324BF5`). Units within byte `+0x26` below 40 % HP that lack
   effect 34 are kept (`00324BFB`-`00324D2E`). Each radius also bounds the height difference.
5. **Being hit,** enemy-table units only. A unit whose entry in `+0xDD4 + 4 * slot` is still ahead of the tick
   counter `0208D45C` is kept (`00324D34`-`00324DCF`). An action's first pass over a target sets the
   attacker's entry to the counter plus `10 * (int)(01DFE0B8 * 30.0)`, 300 as shipped (`00319206`-`0031923F`),
   and so does the special-sequence target loop `0030EC00` through `00317670` (`0030ED0C`, `003176AE`).
6. With bit 4 of the battle flags `02089340`, the unit's current target `+0x710` is kept
   (`00324DD1`-`00324E09`).
7. **Lure.** When a kept unit of another side has Lure, only Lure units and units of its own side or of no
   side go into the list (`00324E30`-`00324ECB`).

Bit 0 of the list's first byte is cleared at the end (`00324ED2`).

### When the list is rebuilt

`003247F0` runs from the unit's frame update `00233F70` (`00234009`). While the `.data` switch `01EED154` is
non-zero (1 in the image; no instruction writes it), it first calls `00324F20` (`0032481E`-`00324839`):

| Case | Result |
|---|---|
| bit 0 of `+0xBC0` set | full rebuild |
| the unit's slot `+0xEA9 & 7` equals the generation `022C2578` | full rebuild |
| otherwise | the old list is kept, minus inactive units and units with KO, Stone or X-Zone (`00324F45`-`0032504C`) |

The generation steps by one, modulo 8, each time the field frame `00234590` runs (`00325060`, `002346FE`),
so with both running every frame a unit rebuilds its list in full one frame in eight. Bit 0 is set through
`00316D30` when the unit is reset for reuse (`00236B03`) and when its action is cancelled (`003087D2`).

### An order in flight

`00308610`, the unit's combat frame, handles the order it is carrying out (`0030868B`-`003087D2`):

1. With no order and unit flag bit 5 clear, the unit is cancelled with `003105D0`, bit 5 is set and its id
   goes into the 64-entry ring `022BE984` (`00308695`-`003086E5`).
2. When `002FFB60` reports an interrupt reason, the order is cancelled and the perception list re-armed
   (`003086FC`-`00308703`, `003087BE`-`003087D2`).
3. Otherwise, while the order is an order id or an action before phase 9, its flags lack `0x8000` and the
   unit is not changing stance, the selection runs again in resume mode (`0030870C`-`0030874C`). The resumed
   walk stops at the order in flight, so only an order above it in the list can replace it.
4. When the action finishes and no combo continues, the order is cancelled and the list re-armed
   (`00308751`-`003087D2`).

`003105D0` clears the in-flight order: `+0x714` becomes `0xFFFF`, `+0x708` and `+0x710` 0, the target list is
reset and the previous command is kept in `+0x730`
([Action commit](../Battle-Actions/action-commit.md)).

A status change can also end the order. `00300140(unit, cancel)` empties the issued command set `+0x6F8` and its
target `+0x748`, and with `cancel` non-zero first cancels the order with `003105D0` (`00300149`-`0030015C`); adding
or removing Confuse or Berserk runs it ([Status changes](../Status-Effects-And-KO/status-changes.md)).

## Layouts

The header of an order set, followed by its 24-byte orders ([Gambits](gambits.md)) from `+0x20`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[12]` | counts | orders in subgroups 0-11, summed by the walk (`00305D30`, `00305D89`) |
| `+0x0C` | `u8[20]` | pad0C | 0 in the built-in sets |

## Modding notes

- A phase change is an order: an enemy switches phase only when one of its own orders `0x4116`-`0x4121`
  runs.
- The default and wait records are `.data`: patching `01EEC298`'s word changes what every unit does when its
  lists come up empty.
- An enemy with class row byte `+0x18 & 0x0E` = 4 notices every eligible unit at once, at any distance.

## Related

- [Gambits](gambits.md) - the cascade, the walk and the target tests.
- [Gambit conditions](gambit-conditions.md) - the tests an order can make.
- [Enemy order sets](enemy-order-sets.md) - every shipped order set and order, and the selector's full test list.
- [Enmity](enmity.md) - which noticed unit an enemy attacks.
- [Battle orders](../Battle-Actions/battle-orders.md) - the order ids.
- [Action commit](../Battle-Actions/action-commit.md) - committing and cancelling an order.
- [Area of effect](../Battle-Actions/area-of-effect.md) - the target-list layout.
