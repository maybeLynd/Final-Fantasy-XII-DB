---
title: "Battle buffs: what Battle Cry, Enrage, Magick Barrier, Perfect Defense and the other enemy abilities switch on, and how long they last"
kind: "system"
category: "Status effects and KO"
addresses: "0x0030E130, 0x0030EA40, 0x00387020, 0x00385570, 0x002FDDA0, 0x003112F0, 0x00386AE0, 0x003279B0"
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

`0x0030E130(stats, id, timer, flags, mode)` sets or clears one id (`0x0030E130`-`0x0030E358`):

1. The id must pass the class-29 id check, 0 to 128 (`0x0030E1D7`-`0x0030E1E5`;
   [Item and ability ids](../Engine-Core/item-and-ability-ids.md)).
2. Modes 0 and 2 clear and set `+0x68`; modes 1 and 3 clear and set `+0x78`. A change to a bit already in the
   asked state does nothing (`0x0030E1EB`-`0x0030E24E`).
3. For modes 0 and 2, `0x0030EA40` writes the id's timer, below (`0x0030E251`-`0x0030E264`).
4. Nothing else happens unless the id's presence in either layer changed (`0x0030E269`-`0x0030E280`).
5. A result record is built: for a set, `0x00386AE0`, which does something only for id 52; for a clear, an empty
   one (`0x0030E286`-`0x0030E2DA`).
6. With flags bit 1 clear, `0x0046A790` (set) or `0x0046A720` (clear) posts the message of ids 55-57 (`0x0030E2DF`-`0x0030E301`).
7. Ids 104-113 change the gambit-slot count, below (`0x0030E303`-`0x0030E317`).
8. Unless flags bit 9 is set, the augments are rebuilt (`0x0030E31C`-`0x0030E329`).

### Who switches them

Two paths set `+0x68` in shipped play:

- **Enemy AI orders.** Orders `0x4092`-`0x40D1` set id (order − `0x4092`) and orders `0x40D2`-`0x4111` clear id
  (order − `0x40D2`), in the order handler `0x002FDDA0` (`0x002FDF93`-`0x002FDFAC`, `0x002FDFF5`-`0x002FE00B`).
- **Clearing everything.** Order `0x4091` clears every id 0-127 from `+0x68` through `0x0030E970`, with flags
  `0x200`, then rebuilds once with `0x0030FED0(stats, 0x200)` (`0x002FDEC1`-`0x002FDEEF`).
- **Their tests.** The shipped area order sets pair nearly every such order with a test of the same id on the
  enemy itself, opcode `0x21` "lacks" or `0x20` "has" (`0x00302478`): if it lacks the buff it sets it, if it has
  it it may clear it.
- **Abilities of recipe 79.** Wall, Magick Barrier, Force Barrier, Greater Barrier, Battle Cry, Shift, Saber,
  Mana Spring, Enrage, Chain Magick, Limit Break, Unleash, Perfect Defense and Chain Reaction set the ids in their
  action row's bytes `+0x10` and `+0x11` (`0xFF` for none). Slot 187 copies them into the result, and the result
  applier sets them in mode 2 (`0x0038FF72`, `0x003117CB`).

### What each id does

| Id | Set by | Effect | Sites |
|---:|---|---|---|
| `2` | order `0x4094` | an attacker with it removes the target's evade bands and ignores the strong-wind penalty on bow and crossbow hits (wind class `0x02099DAC` = 2, [Weather](../World-Areas-And-Travel/weather.md)) | `0x00389548`, `0x003895D4`, `0x00389614` |
| `4` | order `0x4096` | the holder's innate evade band gains 25, or 30 on the party side | `0x0038937F`-`0x003893BF` |
| `6` | order `0x4098` | the holder parries at half its Speed | `0x0038849A`-`0x003884CB` |
| `7` | order `0x4099` | with id 6, it parries at twice its Speed instead | `0x003884B3`-`0x003884D8` |
| `11` | order `0x409D` | the holder's attacks deal ×1.5 at full HP (×1.4 off the party side) | `0x0038BC54`-`0x0038BCA3`; constants `0x00901B3C`, `0x00901B38` |
| `16` | order `0x40A2` | weather and terrain do not scale elemental damage to or from the holder | `0x0038B226`-`0x0038B23D` |
| `18` | order `0x40A4` | Saboteur: calculator slot 21 starts the holder's hit chance at 100 instead of row `+0x12` less the target's Vitality plus the holder's Magick Power. Slot 21 is in recipes 3, 8, 9, 10, 12, 14, 15, 68 and 72 ([Formula recipes](../Damage-And-Battle-Formulas/formula-recipes.md)); the weapon recipe 20 does not run it. The later slots still act on the chance: in recipe 3, slot 31 halves it against a target with Shell (`0x00389230`-`0x0038924F`), and slot 40 then misses on a draw of `MT19937 % 100` at or above it (`0x00389674`-`0x003896A0`) | `0x00388F2A`-`0x00388F37`, `0x00388F8C`-`0x00388FA1` |
| `31` | order `0x40B1` | the target's Reflect does not bounce the holder's magick | `0x00390DFA`-`0x00390E39` |
| `48` | Greater Barrier | damage to the holder is cut to 70 %, except from `0xB3` | `0x00390F8B`-`0x00390FC3` |
| `49` | Battle Cry | the holder's damage ×1.2 | `0x0038F89B`-`0x0038F8B8`; constant `0x008FCC90` |
| `50` | Saber | the holder's damage ×2 | `0x0038F8BE`-`0x0038F8D0` |
| `51` | Mana Spring, Unleash | the cost `0x002F95D0` gives the holder is 0 once its two earlier routes are passed: a party record's Quickenings (`0xD0`-`0xE1`) and Esper summons (`0x106`-`0x112`) keep the row cost (`0x002F9640`-`0x002F9667`, `0x002F9806`), and a holder with augment 32 gets the gil cost `10 * trunc(cost * 64 / 50)` (`0x002F9674`-`0x002F9682`, `0x002F97E4`-`0x002F9802`), 120 gil for a cost of 10 ([MP gain and cost](mp.md)) | `0x002F97A3`-`0x002F97E0` |
| `52` | Shift | the holder's weakness moves to a random element, and again on each hit on it | `0x00386B0C`, `0x0038B78D`, `0x0038C1ED` |
| `53` | Enrage, Limit Break | Attack and orders charge instantly | `0x002F85A6`-`0x002F888A` |
| `54` | Chain Magick, Limit Break, Unleash | actions with row `+0x0C` bit 13 charge instantly | `0x002F8627`-`0x002F862D` |
| `55` | Force Barrier, Perfect Defense | Paling: actions with row `+0x0C` bit 14 are nullified | `0x00390E4B`-`0x00390EEE` |
| `56` | Magick Barrier, Perfect Defense | Magick Shield: actions with row `+0x0C` bit 13 are nullified | `0x00390EA3`-`0x00390EEE` |
| `57` | Wall | White Wind: harmful statuses do not land on the holder | `0x00387D25`-`0x00387D72` |
| `59` | Chain Reaction | no effect of its own; the shipped AI tests it to pick its phase | `0x00302478` |

The ability ids 48-57 also have set orders, `0x40C2`-`0x40CB`, as every id 0-63 does. The shipped order sets contain
set orders for every id in the table but 52, and clear orders for all but 11, 31, 52 and 59.

### Timers and messages

`0x0030EA40(stats, id, timer)` stores the timer in one of eight slots at `+0x17C`, chosen by the augment row's
byte `+6`; a byte above 7 means no timer (`0x0030EA9D`-`0x0030EAB9`). A negative timer takes the default `0x00387020`,
row `+4` × 30 × frame base. Only ids 55, 56 and 57 have a slot, 3, 4 and 5, with `+4` = 120: 3,600 steps, two
minutes at one step per frame.

Each periodic step `0x00385570` walks the ids held in either layer whose row byte `+6` is not `0xFF`
(`0x003855CD`-`0x00385623`, [Status timers](status-timers.md)) and reads the slot's timer as a signed 16-bit value:

- A timer of 0 or below is left alone (`0x0038562E`-`0x00385631`).
- A positive one loses 1 into the result's timer words `+0x42`, which the result applier copies back to `+0x17C`
  (`0x00385636`-`0x00385645`, `0x00311824`).
- The step that takes it from 1 to 0 also puts the id in the result's clear list `+0x3E` (`0x0038563C`); a timer
  already at 0 queues nothing.

The applier clears each listed id with `0x0030E130` in mode 0 and timer 0 (`0x003117E4`-`0x00311807`), and mode 0
clears `+0x68` only (`0x0030E23E`-`0x0030E24E`):

- held in `+0x68` only: the id goes, and the fall message below posts;
- held in both layers: the `+0x68` bit goes, the id stays in effect through `+0x78`, and the function returns
  before the message (`0x0030E269`-`0x0030E280`);
- held in `+0x78` only: mode 0 finds no `+0x68` bit and returns at once (`0x0030E23E`-`0x0030E244`); the id stays in
  effect with its timer at 0.

The messages are:

| Id | Rises | Falls |
|---:|---|---|
| `55` | `0x3E` "A Paling rises around ..." | `0x3F` "The Paling surrounding ... falls." |
| `56` | `0x40` "A Magick Shield forms around ..." | `0x41` "The Magick Shield surrounding ... fades." |
| `57` | `0x42` "A White Wind surrounds ..." | `0x43` "The White Wind surrounding ... dies." |

The other ids last until a clear order (one id, or all with `0x4091`) removes them or the record is set up again ([Battle message
list](../Battle-Actions/battle-message-list.md)).

### Shift's weakness

Setting id 52 builds a result with `0x00386AE0`, which draws one element at random through `0x00384B10` and makes it
the holder's only weakness through the result applier (`0x00386B0C`-`0x00386BD9`, `0x0030E2DA`). The element slots 95
and 99 draw again, leaving out the element that hit, when a holder of id 52 is hit on its weakness
([Elements](../Damage-And-Battle-Formulas/elements.md)).

### Gambit slots

A change of ids 104-113 in either layer adds or removes one gambit line on each of a party member's three
gambit sets, held between 0 and 12 (`0x003279B0`, `0x003279BB`-`0x00327A0B`;
[Gambits](../Enemy-AI-And-Gambits/gambits.md)). Their augment text is "Adds an additional gambit slot.", and
only the gear and license rebuild sets them, in `+0x78`.

That rebuild is `0x0030FED0`, which the equipment-slot
setters `0x0031A410`, `0x0031A510` and `0x0031A630` ([Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md)), the
licence write `0x00323910` ([Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md)) and the level growers
`0x0030C470` and `0x0030C650` ([Stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md)) run.

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
