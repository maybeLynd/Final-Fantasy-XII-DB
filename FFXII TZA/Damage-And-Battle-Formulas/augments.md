---
title: "Augments: how a unit's augments, auto-statuses and status immunities are rebuilt from its character, gear, licenses and an enemy's script"
kind: "system"
category: "Damage and battle formulas"
summary: "How the augment set of a unit is rebuilt after every change: the 64 innate augments of a character row, an enemy's scripted augments, one augment per armor or accessory, up to eight per owned augment license; the difference applied to the augment layer; the statuses and immunities that gear and an enemy's script add; how enemy affinity changes survive the rebuild; and the HP, MP and Mist clamps at the end."
addresses: ["0030FED0", "0030E130", "0030E360", "002390B0", "002394C0", "0030E060", "00323890"]
---

# Augments: how a unit's augments, auto-statuses and status immunities are rebuilt from its character, gear, licenses and an enemy's script

## What the player sees

Augments are the passive abilities from the License Board and from gear, such as "Increases max HP
by 30" from a license or the extra Steal rolls of Thief's Cuffs. Some gear also keeps a status on its wearer or
makes the wearer immune to statuses.

- Equipping an item gives its augment at once, and removing it takes the augment away: the set is worked
  out again from scratch, so nothing is left behind.
- Buying an augment license gives its augments the same way.
- Enemies get their augments and status immunities from their own script.

## How it works

### The rebuild

`0030FED0(stats, flags)` rebuilds a unit's augment set. It forces flag bits `0x202` on (`0030FEFB`) and
starts from an empty 128-bit set (`0030FF02`-`0030FF0A`). Its 25 call sites:

| Caller | Sites |
|---|---|
| the equipment setters `0031A410`, `0031A510`, `0031A630` | `0031A4CA`, `0031A5ED`, `0031A6D4` |
| the License setter `00323910` | `00323B87` |
| the level setter `0030C470` and the level-up `0030C650` | `0030C602`, `0030C7CE` |
| the layer write `0030E130`, the status write `0030E360`, `0030E8F0` and `0030F690` | `0030E329`, `0030E828`, `0030E94D`, `0030F735` |
| the result applier `003112F0` | `00311AC5` |
| the spawn finalisation `0023A410` | `0023A502` |
| `00328BD0` | `00328C66` |
| the direct stat orders `002FDDA0` ([Battle orders](../Battle-Actions/battle-orders.md)) | `002FDEF7`, `002FE163`, `002FE1DB`, `002FE22F`, `002FE283`, `002FE2D7`, `002FE32D`, `002FE383`, `002FE3D9`, `002FE42D`, `002FE481`, `002FE4D5` |

### The four sources

The wanted set is the OR of these sources:

| Source | For | Adds | Sites |
|---|---|---|---|
| character row | party records | bits of words `+0x50` (augments 0-31) and `+0x54` (32-63) of the row of `02EBF130` the type byte `+0x04` selects | `0030FF1F`-`00310018` |
| enemy mask | enemy-side records | the 128 bits at battle unit `+0xE80` | `0031001A`-`0031006F` |
| equipment | everyone | byte `+0x1A` of each equipped item of group 3 (helms, armor, accessories), unless it is `0xFF` | `00310071`-`00310121` |
| licenses | everyone | the eight `u16` at `+0x08`-`+0x16` of each owned node (bit *i* of stats `+0x194`, *i* < 361) whose type byte `+0x05` is 15-18, skipping `0xFFFF` | `00310127`-`003102DF` |

The License node's type is classed by `003241D0` and `00323890`: types 15-17 are group `0x1B` and type 18
group `0x1C`, and both groups are class 2, the only class that adds augments (`00310192`-`0031019E`).

### Applying the difference

The wanted set is compared with the augment layer `+0x78` (`003102E5`-`00310336`):

```
added   = (wanted ^ layer) & wanted      -> 0030E130(stats, id, 0, flags, mode 3)
removed = (wanted ^ layer) & layer       -> 0030E130(stats, id, 0, flags, mode 1)
```

The walk covers ids 0-127 (`00310338`-`003103A3`). Mode 3 sets the bit in `+0x78` and mode 1 clears it,
each with the side effects of `0030E130`. Then the stats rebuild `002FEF30` runs (`003103AD`,
[Stats](stats.md)).

### Auto-statuses and immunities from gear

The stats rebuild ORs two status words into the stats record
([Stats](stats.md)): the character row's words `+0x48` and `+0x4C`, and each equipped item's attribute
words `+0x08` and `+0x0C` (`002FF0A3`-`002FF0D9`, `002FF505`-`002FF51E`):

| Stats word | From row | From item | What it does |
|---|---|---|---|
| `+0x3C` | `+0x48` | `+0x08` | statuses the unit has as long as the source stays (status word 2) |
| `+0x38` | `+0x4C` | `+0x0C` | statuses the unit cannot get: adding one to `+0x64` is refused (`0030E531`) |

The status write `0030E360` picks its word by mode (jump table `0030E88C`): modes 0, 1 and 2 clear a bit in
`+0x64`, `+0x3C` and `+0x38`; modes 3, 4 and 5 set it, mode 3 refusing a status already in `+0x64` or in
`+0x38` (`0030E4E7`-`0030E564`).

### An enemy's scripted augments and immunities

Two script commands set an enemy's two masks:

- **`btlAtelSetAbility(a, b)`**: the handler `00510440` pops two numbers and jumps to `002390B0`, which
  clears `+0xE80` and sets the augments of the two words in reverse bit order: bit *j* of the second
  argument sets augment 31 - *j*, bit *j* of the first sets augment 63 - *j* (`002390D8`-`00239161`). Only
  augments 0-63 can be set this way.
- **`btlAtelSetStatus(table)`**: the handler `005103B0` resolves its argument to 8 bytes of script data and
  jumps to `002394C0`, which reads 32 two-bit codes, one per status (`00239504`-`00239527`):

| Code | Effect |
|---:|---|
| 3 | the status goes into the immunity mask `+0xE90` (`00239538`) |
| 2 | the status is added once, while the spawn record is fresh (`00239551`-`00239577`) |
| 1 | the same, when bit 0 of a shared gameplay LCG draw is set (`00239547`-`0023954F`) |
| 0 | nothing |

"Fresh" means bits 0 and 2 of the spawn record's first dword are clear (`002394DF`-`002394F9`). After the
stats rebuild, `0030FED0` turns every bit of `+0xE90` into an immunity with `0030E360(..., mode 5)`,
which sets it in `+0x38` (`003103B2`-`00310413`). The stats rebuild clears `+0x38` first, so the loop puts
the immunities back on every rebuild.

### Enemy affinity changes

For an enemy with a battle unit, the rebuild then reconciles the five affinity bytes with the spawn
record (`00310415`-`003104BC`, [Elements](elements.md)):

- spawn record byte `+0` bit 7 set: the spawn record's `+0x78`-`+0x7C` are copied over stats
  `+0x40`-`+0x44`;
- clear: the stats bytes are copied into the spawn record.

The result applier sets that bit when it changes an enemy's affinities
([Action results](../Battle-Actions/action-results.md)), so the change survives the rebuild.

### The clamps

Last, the rebuild limits three values without going through the HP write (`003104BF`-`00310594`):

| Value | Limit |
|---|---|
| current HP `+0x48` | max HP `+0x24`, doubled under Bubble (status 28); under Disease (status 16), the current HP itself, at least 1 |
| current MP `+0x4C` | max MP `+0x28`, or 0 when effect 39 is in either layer (byte `+0x6C` or `+0x7C`, bit 7) |
| Mist pool `+0x06` | max MP times the MP bars `+0x37` (0 counting as 1), or 0 under effect 39 |

The values only go down. Then `0030E060` sets the charge count `+0x4E` to `+0x06 / +0x28` when `+0x37` is
not 0, and to 0 otherwise (`0030E0AF`-`0030E0C3`, `0031059C`).

## Shipped data

| Source | Count in the `us` data |
|---|---|
| License nodes of types 15-18 (`battle_pack.bin` section 12) | 87 of 361 (11, 21, 44 and 11 by type) |
| Augments those nodes grant | 87 different ids, each from one node |
| Scripts calling `btlAtelSetAbility` / `btlAtelSetStatus` | 502 each, 6,746 calls each |

Each augment's text is entry *id* of the augment text bank (text word `0x5000` + id in the augment table
`02EBF040`), for example 74 "Increases max HP by 30" and 20 "Gain MP after dealing magick damage".

## Modding notes

- An armor piece or accessory gives one augment: byte `+0x1A` of its equipment row. Weapons and shields
  are ignored here.
- A License node of type 15-18 can give up to eight augments, the words `+0x08`-`+0x16` of its row.
- An enemy's immunities are code 3 in its `btlAtelSetStatus` table; its augments are the two words of
  `btlAtelSetAbility`, read in reverse bit order.

## Related

- [Stats](stats.md) - the stats rebuild this one calls, and the attribute record.
- [Elements](elements.md) - the affinity bytes and Weatherproof.
- [Steal](steal.md) - Thief's Cuffs, augment 17.
- [Action results](../Battle-Actions/action-results.md) - the applier that changes enemy affinities.
- [HP and KO](hp-and-ko.md) - the HP write the HP clamp bypasses.
