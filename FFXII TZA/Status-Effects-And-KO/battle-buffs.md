---
title: "Battle buffs: what Battle Cry, Enrage, Magick Barrier, Perfect Defense and the other enemy abilities switch on, and how long they last"
kind: "system"
category: "Status effects and KO"
addresses: "0030E130, 0030EA40, 00387020, 00385570, 002FDDA0, 003112F0, 00386AE0, 003279B0"
---

## What the player sees

Many enemies change how they fight partway through a battle: they put up a Paling against physical attacks, a
Magick Shield against magick or a White Wind against harmful statuses, use Battle Cry or Enrage to hit harder,
or Shift to move their weakness. Paling, Magick Shield and White Wind come with a message when they rise and
when they fall, and last two minutes. The others last until the enemy drops them.

## How it works

### The two augment layers

A stats record holds two 128-bit sets of augment ids: `+0x78`, which gear and licenses rebuild
([Augments](../Damage-And-Battle-Formulas/augments.md)), and `+0x68`, which battle abilities switch on and off. Id *n* is
bit `n & 7` of byte `n >> 3`. The two layers share the augment ids and their text bank, and every reader below
tests both, so an id behaves the same whichever layer holds it. The damage formula merges both into one set of
128 bits ([Damage formula](../Damage-And-Battle-Formulas/damage-formula.md)).

### The layer write

`0030E130(stats, id, timer, flags, mode)` sets or clears one id (`0030E130`-`0030E358`):

1. The id must pass the class-29 id check, 0 to 128 (`0030E1D7`-`0030E1E5`;
   [Item and ability ids](../Engine-Core/item-and-ability-ids.md)).
2. Modes 0 and 2 clear and set `+0x68`; modes 1 and 3 clear and set `+0x78`. A change to a bit already in the
   asked state does nothing (`0030E1EB`-`0030E24E`).
3. For modes 0 and 2, `0030EA40` writes the id's timer, below (`0030E251`-`0030E264`).
4. Nothing else happens unless the id's presence in either layer changed (`0030E269`-`0030E280`).
5. A result record is built: for a set, `00386AE0`, which does something only for id 52; for a clear, an empty
   one (`0030E286`-`0030E2DA`).
6. With flags bit 1 clear, `0046A790` (set) or `0046A720` (clear) posts the message of ids 55-57 (`0030E2DF`-`0030E301`).
7. Ids 104-113 change the gambit-slot count, below (`0030E303`-`0030E317`).
8. Unless flags bit 9 is set, the augments are rebuilt (`0030E31C`-`0030E329`).

### Who switches them

Two paths set `+0x68` in shipped play:

- **Enemy AI orders.** Orders `0x4092`-`0x40D1` set id (order − `0x4092`) and orders `0x40D2`-`0x4111` clear id
  (order − `0x40D2`), in the order handler `002FDDA0` (`002FDF93`-`002FDFAC`, `002FDFF5`-`002FE00B`).
- **Clearing everything.** Order `0x4091` clears every id 0-127 from `+0x68` through `0030E970`, with flags
  `0x200`, then rebuilds once with `0030FED0(stats, 0x200)` (`002FDEC1`-`002FDEEF`).
- **Their tests.** The shipped area order sets pair nearly every such order with a test of the same id on the
  enemy itself, opcode `0x21` "lacks" or `0x20` "has" (`00302478`): if it lacks the buff it sets it, if it has
  it it may clear it.
- **Abilities of recipe 79.** Wall, Magick Barrier, Force Barrier, Greater Barrier, Battle Cry, Shift, Saber,
  Mana Spring, Enrage, Chain Magick, Limit Break, Unleash, Perfect Defense and Chain Reaction set the ids in their
  action row's bytes `+0x10` and `+0x11` (`0xFF` for none). Slot 187 copies them into the result, and the result
  applier sets them in mode 2 (`0038FF72`, `003117CB`).

### What each id does

| Id | Set by | Effect | Sites |
|---:|---|---|---|
| `2` | order `0x4094` | an attacker with it removes the target's evade bands and ignores the strong-wind penalty on bow and crossbow hits (wind class `02099DAC` = 2, [Weather](../World-Areas-And-Travel/weather.md)) | `00389548`, `003895D4`, `00389614` |
| `4` | order `0x4096` | the holder's innate evade band gains 25, or 30 on the party side | `0038937F`-`003893BF` |
| `6` | order `0x4098` | the holder parries at half its Speed | `0038849A`-`003884CB` |
| `7` | order `0x4099` | with id 6, it parries at twice its Speed instead | `003884B3`-`003884D8` |
| `11` | order `0x409D` | the holder's attacks deal ×1.5 at full HP (×1.4 off the party side) | `0038BC54`-`0038BCA3`; constants `00901B3C`, `00901B38` |
| `16` | order `0x40A2` | weather and terrain do not scale elemental damage to or from the holder | `0038B226`-`0038B23D` |
| `18` | order `0x40A4` | the holder's attacks always hit | `00388F2A`-`00388F37` |
| `31` | order `0x40B1` | the target's Reflect does not bounce the holder's magick | `00390DFA`-`00390E39` |
| `48` | Greater Barrier | damage to the holder is cut to 70 %, except from `0xB3` | `00390F8B`-`00390FC3` |
| `49` | Battle Cry | the holder's damage ×1.2 | `0038F89B`-`0038F8B8`; constant `008FCC90` |
| `50` | Saber | the holder's damage ×2 | `0038F8BE`-`0038F8D0` |
| `51` | Mana Spring, Unleash | the holder's actions cost nothing | `002F97A3`-`002F97E0` |
| `52` | Shift | the holder's weakness moves to a random element, and again on each hit on it | `00386B0C`, `0038B78D`, `0038C1ED` |
| `53` | Enrage, Limit Break | Attack and orders charge instantly | `002F85A6`-`002F888A` |
| `54` | Chain Magick, Limit Break, Unleash | actions with row `+0x0C` bit 13 charge instantly | `002F8627`-`002F862D` |
| `55` | Force Barrier, Perfect Defense | Paling: actions with row `+0x0C` bit 14 are nullified | `00390E4B`-`00390EEE` |
| `56` | Magick Barrier, Perfect Defense | Magick Shield: actions with row `+0x0C` bit 13 are nullified | `00390EA3`-`00390EEE` |
| `57` | Wall | White Wind: harmful statuses do not land on the holder | `00387D25`-`00387D72` |
| `59` | Chain Reaction | no effect of its own; the shipped AI tests it to pick its phase | `00302478` |

Ids 48-51 and 53-57 also have orders, `0x40C2`-`0x40CB`. The shipped order sets contain set orders for every id
in the table but 52, and clear orders for most of them.

### Timers and messages

`0030EA40(stats, id, timer)` stores the timer in one of eight slots at `+0x17C`, chosen by the augment row's
byte `+6`; a byte above 7 means no timer (`0030EA9D`-`0030EAB9`). A negative timer takes the default `00387020`,
row `+4` × 30 × frame base. Only ids 55, 56 and 57 have a slot, 3, 4 and 5, with `+4` = 120: 3,600 steps, two
minutes at one step per frame.

Each periodic step `00385570` counts every timed id held in either layer down by one; at 0 it puts the id in the
result's clear list, and the result applier clears it (`003855CD`-`00385645`,
[Status timers](status-timers.md)). The messages are:

| Id | Rises | Falls |
|---:|---|---|
| `55` | `0x3E` "A Paling rises around ..." | `0x3F` "The Paling surrounding ... falls." |
| `56` | `0x40` "A Magick Shield forms around ..." | `0x41` "The Magick Shield surrounding ... fades." |
| `57` | `0x42` "A White Wind surrounds ..." | `0x43` "The White Wind surrounding ... dies." |

The other ids last until a clear order (one id, or all with `0x4091`) removes them or the record is set up again ([Battle message
list](../Battle-Actions/battle-message-list.md)).

### Shift's weakness

Setting id 52 builds a result with `00386AE0`, which draws one element at random through `00384B10` and makes it
the holder's only weakness through the result applier (`00386B0C`-`00386BD9`, `0030E2DA`). The element slots 95
and 99 draw again, leaving out the element that hit, when a holder of id 52 is hit on its weakness
([Elements](../Damage-And-Battle-Formulas/elements.md)).

### Gambit slots

A change of ids 104-113 in either layer adds or removes one gambit line on each of a party member's three
gambit sets, held between 0 and 12 (`003279B0`, `003279BB`-`00327A0B`;
[Gambits](../Enemy-AI-And-Gambits/gambits.md)). Their augment text is "Adds an additional gambit slot.", and
only the gear and license rebuild sets them, in `+0x78`.

That rebuild is `0030FED0`, which the equipment-slot
setters `0031A410`, `0031A510` and `0031A630` ([Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md)), the
licence write `00323910` ([Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md)) and the level growers
`0030C470` and `0030C650` ([Stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md)) run.

## Modding notes

- The buff an ability grants is its action row's `+0x10` and `+0x11`; the buff an order grants is the order id
  minus `0x4092`.
- A buff's duration is data: give an augment row a slot in byte `+6` (0-7) and a value in `+4`.

## Related

- [Augments](../Damage-And-Battle-Formulas/augments.md) - the `+0x78` layer and the rebuild.
- [Status timers](status-timers.md) - the periodic step that counts the timers down.
- [Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md) - the tests an order makes.
- [Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md) - the order sets.
- [Damage formula](../Damage-And-Battle-Formulas/damage-formula.md) - the merged augment bits the slots read.
