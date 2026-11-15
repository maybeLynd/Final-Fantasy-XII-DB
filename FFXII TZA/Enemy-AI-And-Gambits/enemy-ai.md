---
title: "Enemy AI: the order sets an enemy tries, the phase a command switches to, what an enemy notices and when an order is replaced"
kind: "system"
category: "Enemy AI and gambits"
addresses: "0x00305AB0, 0x00305CC0, 0x002FDDA0, 0x0023A570, 0x003247F0, 0x00324F20, 0x00325060, 0x0030F130, 0x00308610, 0x003105D0"
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

The lists come from the area file, which holds a directory of order lists. An enemy starts with the list its
definition row names, the row can name up to four lists, and the enemy's own orders switch it to another of those
lists or to one of twelve phases inside a list.

## How it works

### The order sets

Every unit carries four order-set pointers, tried by `0x00305AB0` in a fixed order ([Gambits](gambits.md)
has the whole cascade):

| Set offset | Holds | Installed by |
|---|---|---|
| `+0x6E8` | the re-plan set: `0x01EEC3C0` for a party record, `0x01EEC410` otherwise | `0x00313458`, `0x003134DA`, `0x002FED9E`, `0x002FEE05`, `0x0030126B`, `0x0030F331` |
| `+0x6F8` | the issued command's set `0x01EEC2D0`, target in `+0x748` | `0x00311DD4`-`0x00311DE1` |
| `+0x6E0` | the unit's own list, walked with its subgroup `+0x6B5` | the unit definition, orders `0x4112`-`0x4115`, the script verb `btlAtelSetDefaultLogic` (`0x00239081`), which keeps the subgroup |
| `+0x6F0` | the default set `0x01E09350` | `0x0023ABA6`-`0x0023ABB5`, on the party-table path (`0x0023AB7E`) |

An enemy-table unit never walks `+0x6F8`, because that step is for party records (`0x00305BE7`-`0x00305C03`), and
its `+0x6F0` stays empty from the reset (`0x00236BB6`); the walk returns 0 at once for that null set
(`0x00305CF2`-`0x00305CF7`). Its cascade is the re-plan set, then its own list, then
the wait `0x4021` from `0x01EEC298` (`0x00305C7E`-`0x00305C9B`).

Three cases change that cascade. An issued command (unit flag `0x4000`) is tried before it
(`0x00305ADF`-`0x00305B36`). Outside a town, Confuse (status `0x20`) or Berserk (status `0x08000000`) walks
`0x01EEC320` in place of the re-plan set and its own list (`0x00305B5D`-`0x00305B90`). In resume mode the wait is
not committed (`0x00305C7A`).

### The built-in sets

The image holds six one-subgroup sets and one bare order record (`.data`, read at the addresses below). The
wait record `0x01EEC298` has no count header; `0x00305AB0` commits it directly with the action commit `0x0030F760`
([Action commit](../Battle-Actions/action-commit.md)) instead of walking it (`0x00305C7E`-`0x00305C9B`):

| Set | Order | Flags | Used for |
|---|---|---|---|
| `0x01EEC320` | `0x0096` Attack, then `0x4125` | - | a Confused unit, or an enemy with Berserk (`0x00305B89`) |
| `0x01EEC370` | `0x0096` Attack | - | a party record with Berserk (`0x00305BDE`) |
| `0x01EEC3C0` | `0x4022`, follow the party | `0x2000` | party re-plan set |
| `0x01EEC410` | `0x414D`, flip the combat stance | - | enemy re-plan set |
| `0x01EEC2D0` | `0x0096` Attack, relation mode 10 | - | an issued command: attack the unit in `+0x748` |
| `0x01E09350` | `0x4124`, follow the leader | `0x2000` | the default set |
| `0x01EEC298` | `0x4021`, wait | `0x2000` | the last resort, committed as a single order |

The attacks in the Confuse and Berserk sets carry relation mode 1 in their test, so they pick a foe;
under Confuse the two sides are swapped ([Gambits](gambits.md)). The orders are on
[Battle orders](../Battle-Actions/battle-orders.md).

### Where an enemy's list comes from

An enemy's own list is a set from the order-set directory `[0x02EBF168]`, which the area file provides
([Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)):
a `u16` count, then one 32-bit offset per set, each resolved against `0x01F83530` by `0x0020E600`.

- The unit definition installs the set named by the definition row's word `+0x50` (`0x0023A94D`-`0x0023A95E`).
- Orders `0x4112`-`0x4115` install the set named by word `+0x50`, `+0x52`, `+0x54` or `+0x56` of the row
  (`+0xE60`), bounded by the directory's count, and set the subgroup to 0 (`0x002FE025`-`0x002FE0B2`). Only an
  enemy-table unit takes them (`0x002FE03E`).
- Orders `0x4116`-`0x4121` set the subgroup `+0x6B5` to the id's low byte minus `0x16`, so subgroups 0 to 11
  (`0x002FE0B3`-`0x002FE0D2`).

So an enemy has up to four lists and twelve phases in each. The walk `0x00305CC0` starts a subgroup after the
orders of all earlier subgroups ([Gambits](gambits.md)). Every shipped set and order is on
[Enemy order sets](enemy-order-sets.md).

### The perception list

Each unit keeps a list of up to 32 units it has noticed at `+0xBC0`, in the 0x208-byte target-list layout of
[Area of effect](../Battle-Actions/area-of-effect.md): count `+0xBC4`, entries from `+0xBC8`. An order id
takes this list as its candidates (`0x00301599`). An action takes it through `0x0030F130`: the whole list, or,
when the unit's `+0x6D0` radius is set, the units within that radius plus their own size of `+0x6C0`
(`0x0030F1CE`-`0x0030F25A`). It also adds
each of party slots 0-3 that the action may target while it has KO, Stone or X-Zone (`0x0030F261`-`0x0030F2B2`).

### Rebuilding the list

`0x003247F0(unit)` rebuilds the list (`0x00324857`-`0x00324ED2`):

1. It clears it. A unit that is inactive, has KO, Stone or X-Zone without the field's bit `0x8000`, or is an
   enemy-table unit whose spawn record's first byte has a bit of `0x30` keeps it empty (`0x00324881`-`0x003248D0`).
2. It marks every active unit that passes the eligibility test `0x002FFEF0` (`0x00324920`-`0x0032496E`). An
   enemy-table unit whose class row byte `+0x18 & 0x0E` is 4 notices all of them, and steps 3-6 are skipped
   (`0x003248E3`-`0x00324909`, `0x00324976`).
3. **Sight.** The query `0x003919B0` around the unit's position `+0xE0` uses its floats `+0x64`, `+0x68` and
   `+0x160`. A result is kept when it is not an Invisible unit of another side (`0x0030BCB0`), its height differs by at most `+0x68`, and the
   test `0x0032A4D0` passes (`0x0032497E`-`0x00324ABA`).
4. **The two radii,** enemy-table units only. Units within the class row's byte `+0x25` that lack augment 33 (Veil)
   and pass `0x0032A4D0` are kept (`0x00324AC0`-`0x00324BF5`). Units within byte `+0x26` below 40 % HP that lack
   augment 34 (Life Cloak) are kept (`0x00324BFB`-`0x00324D2E`). Each radius also bounds the height difference.
5. **Being hit,** enemy-table units only. A unit whose entry in `+0xDD4 + 4 * slot` is still ahead of the tick
   counter `0x0208D45C` is kept (`0x00324D34`-`0x00324DCF`). An action's first pass over a target sets the
   attacker's entry to the counter plus `10 * (int)(0x01DFE0B8 * 30.0)`, 300 as shipped (`0x00319206`-`0x0031923F`),
   and so does the special-sequence target loop `0x0030EC00` through `0x00317670` (`0x0030ED0C`, `0x003176AE`).
6. With bit `0x10` of the battle flags `0x02089340`, the unit's current target `+0x710` is kept
   (`0x00324DD1`-`0x00324E09`).
7. **Lure.** When a kept unit of another side has Lure, only Lure units and units of its own side or of no
   side go into the list (`0x00324E30`-`0x00324ECB`).

Bit `0x1` of the list's first byte is cleared at the end (`0x00324ED2`).

### When the list is rebuilt

`0x003247F0` runs from the unit's frame update `0x00233F70` (`0x00234009`). While the `.data` switch `0x01EED154` is
non-zero (1 in the image; no instruction writes it), it first calls `0x00324F20` (`0x0032481E`-`0x00324839`):

| Case | Result |
|---|---|
| bit `0x1` of `+0xBC0` set | full rebuild |
| the unit's slot `+0xEA9 & 7` equals the generation `0x022C2578` | full rebuild |
| otherwise | the old list is kept, minus inactive units and units with KO, Stone or X-Zone (`0x00324F45`-`0x0032504C`): an entry stays when its handle resolves (`0x00263E30`) to a unit with bit `0x10` of its first dword and a stats record, without KO, Stone or X-Zone unless the town flag `0x00313F60()` is set (`0x00324F7F`-`0x00324FB1`). The 0x208-byte list is then cleared and refilled from the 32 battle units of `0x00236820(0)`, stride `0xF50`: unit `i` goes in, as its `+0x10`, when a kept unit's slot `+0xEA9` is `i` (`0x00324FD7`-`0x0032504C`). `0x00324F20` returns 1 here and 0 in the two cases above |

The generation steps by one, modulo 8, each time the field frame `0x00234590` runs (`0x00325060`, `0x002346FE`),
so with both running every frame a unit rebuilds its list in full one frame in eight. Bit `0x1` is set through
`0x00316D30` when the unit is reset for reuse (`0x00236B03`) and when its action is cancelled (`0x003087D2`).

### An order in flight

`0x00308610`, the unit's combat frame, handles the order it is carrying out (`0x0030868B`-`0x003087D2`). Before that,
when bit `0x20` of `0x02089340` is clear, the unit's status words hold bit `0x10` (Sleep) and `0x003E7DE0()` is 0, it
calls `0x003299B0(unit, 0x2001, 0)` (`0x00308616`-`0x00308648`); it then returns early when `0x0030DA30(unit)` holds,
setting bit `0x2` of `0x02089340` when unit bit `0x1000000` is set, or when `0x00307DF0(unit)` is non-zero after
`0x0033A240(unit + 0x80)`, setting the same bit (`0x0030864D`-`0x00308689`):

1. With no order and unit flag bit `0x20` clear, the unit is cancelled with `0x003105D0`, bit `0x20` is set and its id
   goes into the 64-entry ring `0x022BE984` (`0x00308695`-`0x003086E5`), after `0x00308270(unit)` when unit bit `0x400000`
   is set (`0x003086A0`-`0x003086AA`). With no order and bit `0x20` set the frame returns (`0x0030869A`).
2. With an order, bit `0x2` of `0x02089340` is set when `0x00237670(unit id)` is 0 (`0x003086E6`-`0x003086F2`). When
   `0x002FFB60` reports an interrupt reason, the order is cancelled and the perception list re-armed
   (`0x003086FC`-`0x00308703`, `0x003087BE`-`0x003087D2`).
3. Otherwise, while the order is an order id or an action before phase 9, its flags lack `0x8000` and the
   unit is not changing stance, the selection runs again in resume mode (`0x0030870C`-`0x0030874C`): unit bits
   `0x1000000` and `0x400000` clear, `+0x714` above `0x21E` or `+0x6B4` below 9, and the word `+4` of
   `[+0x708]` not negative. The resumed walk stops at the order in flight, so only an order above it in the
   list can replace it.
4. When the action finishes and no combo continues, the order is cancelled and the list re-armed
   (`0x00308751`-`0x003087D2`). The action is finished when the state step `0x00307BE0` returns non-zero, and a
   result of 1 also sets bit `0x1` of `+0x718` (`0x00308762`); while it returns 0 the frame returns
   (`0x0030875B`). With unit bit `0x400000` set the frame ends in a jump to `0x00308270(unit)` instead of the
   cancel (`0x003087A8`-`0x003087B9`).

`0x003105D0` clears the in-flight order: `+0x714` becomes `0xFFFF`, `+0x708` and `+0x710` 0, the target list is
reset and the previous command is kept in `+0x730`
([Action commit](../Battle-Actions/action-commit.md)). It returns at once for a null unit or one without a
stats record `+0x698` (`0x003105D3`, `0x003105E9`). Otherwise, in order (`0x00310605`-`0x00310758`):

1. `0x00310780(unit)` runs the release ([Action commit](../Battle-Actions/action-commit.md)); `+0x6B6` = 0; the
   slots `+0x695` and `+0x696` are freed with `0x0030C970` and set to `0xFF`; `0x00300280(unit)` gives back a
   reserved item and gil ([Item use](../Items-Equipment-Shops-And-Licenses/item-use.md)).
2. Unit flag bits `0x3000`, `0x20000000`, `0x80000000` and `0x1000000` are cleared, and `+4` bits `0x8`, `0x80`,
   `0x4000`, `0x40000`, `0x80000` and `0x200000`; `+0x690` = 0. The call `0x0016D6A0(unit)` between the two flag
   clears is a bare `ret 0` and does nothing (`0x0031065E`).
3. The unit's bit `1 << +0xEA9` is cleared in `+0xEA0` of every unit of the `0x00236820` list
   (`0x00310672`-`0x003106AB`).
4. `0x00316CF0(unit + 0x778)` resets the target list; `+0x718`-`+0x72F` are copied to `+0x730`-`+0x747`;
   `+0x700` loses bits `0x3`; the word `+0x6B7`, the byte `+0x6B4` and the dword `+0x75C` are zeroed, and the
   qwords `+0x760`, `+0x768`, `+0x6D0` and `+0x6D8`.
5. `0x003291B0(unit + 0x80, 0, 0)` runs; then the dword `+0x1A0`, the qword `+0x1A4` and the dword `+0x6D4` are
   zeroed, bit `0x20` of `+0x1F0` is cleared, and `0x0033C9B0(unit + 0x80)` resets the locomotion block.

A status change can also end the order. `0x00300140(unit, cancel)` empties the issued command set `+0x6F8` and its
target `+0x748`, and with `cancel` non-zero first cancels the order with `0x003105D0` (`0x00300149`-`0x0030015C`); adding
or removing Confuse or Berserk runs it ([Status changes](../Status-Effects-And-KO/status-changes.md)).

## Layouts

The header of an order set, followed by its 24-byte orders ([Gambits](gambits.md)) from `+0x20`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[12]` | counts | orders in subgroups 0-11, summed by the walk (`0x00305D30`, `0x00305D89`) |
| `+0x0C` | `u8[20]` | pad0C | 0 in the built-in sets |

## State

`0x0032A4D0(unit, other, refresh)`, the line-of-sight test of steps 3 and 4, keeps its answers for the frame in the
`0x100` bytes at `0x022C26A0`: one 32-bit mask per unit index `+0xEA9` of the pairs already tested
(`0x022C26A0 + 4i`), and one of the pairs found clear (`0x022C2720 + 4i`).

A pair already tested gives its kept
answer unless `refresh` is set (`0x0032A510`-`0x0032A52B`); otherwise the test casts a line between the two units'
positions, raised by the height `0x00263940` gives (`0x0032A54C`-`0x0032A5D8`), and keeps the answer for both units.
`0x0032A650`, run by the field frame `0x00234590` (`0x002346EA`), clears the block (`0x0032A663`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C2564` | `i32` | 0 | the lines cast so far this frame: every test that is not answered from the kept masks adds 1 (`0x0032A61C`) | `0x0032A4D0` (`0x0032A61C`); `0x0032A650`, 0 (`0x0032A681`) | `0x0032A650`, which keeps the larger of it and `0x022C2568` in `0x022C2568` before clearing it (`0x0032A668`-`0x0032A67B`); no other function reads `0x022C2568` |

No other instruction reaches `0x022C2564` or `0x022C2568`.

## Modding notes

- A phase change is an order. One of an enemy's own orders `0x4116`-`0x4121` selects phase 0 to 11, and an order
  `0x4112`-`0x4115` that installs a new set also returns it to phase 0 (`0x002FE09F`); a selector at or past
  the directory's count refuses that order instead (`0x002FE073`-`0x002FE077`).
- The default and wait records are `.data`: patching `0x01EEC298`'s word changes what every unit does when its
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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x003E7DE0` is called by `0x00332C40`, `0x003B3D20`, `0x003B99D0`; those functions are documented on
  [animation sounds](../Sound-And-Music/animation-sounds.md),
  [effect drawing](../Graphics/effect-drawing.md),
  [effect anchors and targets](../Graphics/effect-anchors-and-targets.md).
- Input: `0x00313F60` is called by `0x00253C70`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Items equipment shops license: `0x00236820` is called by `0x0031A300`; `0x00300280` calls `0x003008A0`; those functions are
  documented on [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md),
  [identifier spaces](../Engine-Core/identifier-spaces.md).
