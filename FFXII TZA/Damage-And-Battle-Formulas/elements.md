---
title: "Elements: weakness, absorb, half damage, immunity, elemental potency, Oil, and weather and terrain scaling"
kind: "system"
category: "Damage and battle formulas"
addresses: "0038B6A0, 0038BE30, 0038D280, 0038B220, 002FEF30, 0038B010, 0038C940, 0038B950, 0026D910, 00263DD0"
---

## What the player sees

There are eight elements: fire, lightning, ice, earth, water, wind, holy and dark. A magick carries
the element of its row; a weapon attack carries the weapon's element, or for bows, crossbows, guns
and other ammunition weapons the element of the ammunition.

- **Weak** doubles the damage, **half** halves it, **immune** makes the hit do nothing, and **absorb**
  turns the damage into healing.
- **Potency** (for example the Flame Staff for fire) multiplies the wielder's damage of that element
  by 1.5.
- **Oil** triples fire damage. **Float** makes earth magicks miss.
- **The area's conditions and the ground** make some magick elements 20 % stronger or 50 % weaker. A
  character wearing the Agate Ring, or a target with the same augment, is not affected.

Weakness and resistance are separate: a target weak to an element and halving it takes the normal
amount, because both multipliers apply.

## How it works

### The element bits

An element is one bit of a byte, in the order of the element icons in `help_action.bin` (icon `0x8A` +
bit, for example "fire damage" with icon `0x8A` and "dark damage" with `0x91`):

| Bit | Element | Spells | Weapons and ammunition |
|---:|---|---|---|
| `0` | fire | Fire, Fira | Flametongue, Fiery Arrows |
| `1` | lightning | Thunder, Thundara | Storm Spear, Lightning Arrows |
| `2` | ice | Blizzard, Blizzara | Icebrand, Trident |
| `3` | earth | Quakeja, Tremor | Koga Blade, Mud Shot |
| `4` | water | Aqua, Aquara | Murasame, Aqua Shot |
| `5` | wind | Aero, Aeroga | Zephyr Pole, Windslicer Shot |
| `6` | holy | Holy, Holyja | Excalibur, Holy Lance |
| `7` | dark | Dark, Darkra | Yagyu Darkblade, Dark Shot |

A magick's element is byte `+0x13` of its action row
([Action definition row](../Battle-Actions/action-definition-row.md)). A weapon's is byte `+0x1E` of
its equipment row.

### Where a unit's affinities come from

Five bytes of a unit's stats record hold its affinities, each a mask over the eight elements:

| Byte | Meaning | Equipment attribute byte | Enemy area row byte |
|---|---|---|---|
| `40` | weak | `+0x13` | `+0x2C` |
| `41` | absorb | `+0x10` | `+0x29` |
| `42` | half | `+0x12` | `+0x2A` |
| `43` | immune | `+0x11` | `+0x2B` |
| `44` | potency | `+0x14` | `+0x2D` |

The stats rebuild `002FEF30` clears them (`002FEFB9`-`002FEFC8`). For an enemy-side unit it then copies
the five bytes of the unit's area row: the row of table `02EBF150` named by word `+0` of the unit's
`02EBF120` row (`002FF0E1`-`002FF322`). For every unit it then ORs in the attribute record of each of the
five equipped items, the record that equipment row `+0x28` points to (`002FF3F0`-`002FF57B`). A party
member starts from zero.

The applier can change an enemy's affinities during a fight. Those changes live in the unit's spawn
record at `+0x78`-`+0x7C`, and the auto-status rebuild `0030FED0` copies them back over the stats bytes
when the spawn record's byte `+0` has bit 7 (`00310433`-`003104BC`)
([Action results](../Battle-Actions/action-results.md)).

### The magick affinity stage

Slot 95, `0038B6A0`, compares the action's element with the target's bytes and the user's potency, in
this order (`0038B709`-`0038B932`):

1. **Immune** (`+0x43`): sets `02AEDFCC` = 1 and skips every later test (`0038B70D`-`0038B71D`).
2. **Weak** (`+0x40`): multiplies the scale `02AEE054` by 2.0 and sets bit 1 of the result's `+0x140`
   (`0038B769`-`0038B791`). When the target also has effect 52 in either layer (byte `+0x6E` or `+0x7E`,
   bit 4), it calls `00384B10(element, context)` and sets bit 10 (`0038B78D`-`0038B7F2`).
3. **Half** (`+0x42`): multiplies by 0.5 and sets bit 2 (`0038B84A`-`0038B871`).
4. **Absorb** (`+0x41`): sets `02AEDFD0` = 1 and leaves the scale alone (`0038B8BC`-`0038B8D1`).
5. **Potency** (the user's `+0x44`): multiplies by 1.5 and sets bit 3 (`0038B911`-`0038B932`).

Every test that matches applies, so the factors multiply:

| Value | Formula | Code |
|---|---|---|
| weak and half             2.0 * 0.5 | `1.0` |  |
| weak, with potency        2.0 * 1.5 | `3.0` |  |
| weak, half, with potency  2.0 * 0.5 * 1.5 | `1.5` |  |

### The weapon affinity stage

Slot 99, `0038BE30`, runs the same five tests in the same order for weapon attacks, with the same
factors (2.0 at `0038C1DE`, 0.5 at `0038C588`, 1.5 at `0038C8E1`). The element is byte `+0x1E` of the
main-hand row (stats `+0x50`), or of the off-hand row (`+0x52`) when the main hand's byte `+0x11` is
23-26, the ammunition weapons (`0038BEDE`-`0038C001`). As in slot 95, an immune match sets
`02AEDFCC` and returns at once (`0038C011`-`0038C01C`); the other tests run only when the immune byte
misses.

### Immunity and absorb in the final number

The finishing slot `0038D280` (slots 113 and 125) turns the scale and the two flags into the HP change
(`0038D280`-`0038D333`):

1. Attack minus defence below 0 gives a loss of 0.
2. Immune: it sets `02AEDFC0` = 1, the HP loss `02AEE004` = -1 (none), and bit 0 of result `+0x140`. The
   resolver turns `02AEDFC0` into result kind 10 (`003866CE`-`003866D7`).
3. Otherwise the value is `(attack - defence) * scale`. Without absorb it is an HP loss (`02AEE004`).
   With absorb it is an HP gain (`02AEE008`).
4. A target with Reverse (status 12, context `+8` bit 12) swaps the two: a loss becomes a gain and an
   absorbed hit becomes a loss (`0038D2E1`, `0038D302`).

### Oil and Float

Three slots apply the element against the target's statuses:

| Slot | Function | Runs for | Oil (status 11) and fire | Float (status 26) and earth |
|---:|---|---|---|---|
| `92` | `0038B010` | magick recipes 7, 11, 63, 83, 105 | x3 (`0038B076`-`0038B0DB`) | miss: `02AEDFBC` and `02AEDFB8` = 1 (`0038B0E3`-`0038B131`) |
| `102` | `0038C940` | recipes 65, 66 | x3 (`0038CA23`-`0038CA88`) | miss (`0038CA90`-`0038CADE`) |
| `96` | `0038B950` | the weapon recipes 20-29, 64, 103, 104 | x3 with the weapon or ammunition element (`0038BA44`-`0038BBE6`) | not tested |

The same three slots also multiply the scale for other statuses, for example Shell (status 19) by
0.75 at `0038B057`-`0038B065`.

### Weather and terrain scaling

Slot 94, `0038B220`, scales a magick's element by the area's conditions. It runs in recipes 7, 14, 37,
63, 83, 105 and 106, before slot 95; the weapon recipes do not run it. It is skipped when effect 16 is in
the target's layer `+0x68` or `+0x78` (bytes `+0x6A`, `+0x7A`, bit 0) or in the user's merged context
bits (context `+0x1C` bit 0) (`0038B226`-`0038B242`).

Effect 16 is the augment the Agate Ring carries: equipment row 345 has byte `+0x1A` = 16 and class 21,
and the stats rebuild `0030FED0` adds the `+0x1A` augment of each equipped item of classes 19-22 to the
layer `+0x78` (`00310080`-`00310121`, [Steal](steal.md) has the details).

Otherwise it tests nine rules in order, each multiplying `02AEE054` once (0.5 from `01CEBB70`, 1.2 from
`008FCC90`):

| Element | x0.5 when | x1.2 when | Sites |
|---|---|---|---|
| fire | environment class 0 | weather class 2 | `0038B295`-`0038B2B8`, `0038B5FE`-`0038B61A` |
| lightning | - | environment 0 or terrain 0 | `0038B3E1`-`0038B424` |
| ice | - | environment 2 or terrain 2 | `0038B46D`-`0038B4AA` |
| earth | terrain 0 | environment 1 or terrain 1 | `0038B301`-`0038B333`, `0038B4F3`-`0038B530` |
| water | weather class 2 | environment 3 or terrain 0 | `0038B37C`-`0038B398`, `0038B579`-`0038B5B5` |
| wind | - | weather class 2 | `0038B65E`-`0038B67F` |

An "or" rule multiplies once even when both of its tests hold. A ×0.5 and a ×1.2 rule for the same
element both apply, giving 0.6. A terrain test needs the target's battle unit (`0031B860`); without one
it fails.

### The three classes

The environment and weather classes belong to the area, and the terrain class to the target:

- **Environment class** `02099DA8` (read through `00321490`): `0026D910` looks up the active weather
  lane's index byte in the 16-entry table at `map_ref.bin` header `+0x10` (`0026DA10`-`0026DA26`).
- **Weather class** `02099DAC` (read through `003214A0`): `0026D910` takes the lane's weather preset from
  `00377850`, giving 0 for preset 0, 1 for presets 1-3 and 2 for presets 4 and above
  (`0026DA31`-`0026DA4E`).
- **Terrain class** (`003210E0`, then `00263DD0`): the target actor's ground index, the `i16` at `+0x8A`
  of the record its `+0xC0` and `+0x138` pointers reach (index 0 when either is missing), looked up in the
  32-entry table at `map_ref.bin` header `+0x14` (`00263DD7`-`00263E00`; bound by `002678A0`).

## Layouts

The element and affinity fields of an equipment row and its attribute record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `1E` | `u8` | element | weapon or ammunition element, one bit (`0038BE30`, `0038B950`) |
| `28` | `u32` | attributes | offset of the attribute record past header `+0x18`; made a pointer at load (`00238225`-`0023823E`) |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `10` | `u8` | absorb | elements absorbed (`002FF538`) |
| `11` | `u8` | immune | elements nullified (`002FF556`) |
| `12` | `u8` | half | elements halved (`002FF547`) |
| `13` | `u8` | weak | elements doubled (`002FF529`) |
| `14` | `u8` | potency | elements boosted x1.5 when the wearer attacks (`002FF56D`) |

## Shipped data

Equipment with an element affinity, from `battle_pack.bin` section 13 (the 13 Reserve rows 179-191
also carry affinities):

| Item | Weak | Absorb | Half | Immune | Potency |
|---|---|---|---|---|---|
| Six-fluted Pole, Fumarole | | | | | water |
| Burning Bow, Flame Staff | | | | | fire |
| Holy Rod, White Robes | | | | | holy |
| Cherry Staff | | | | | wind |
| Storm Staff | | | | | lightning |
| Glacial Staff | | | | | ice |
| Cloud Staff | | | | | lightning, water, wind |
| Staff of the Magi | | | | | ice, wind, holy |
| Zeus Mace, Black Robes | | | | | dark |
| Gendarme | | all eight | | | |
| Ice Shield, Lamia's Tiara, Tourmaline Ring | | | ice | | |
| Flame Shield, Sash | | | fire | | |
| Dragon Shield | | | | earth | |
| Demon Shield, Black Mask | | dark | | | |
| Venetian Shield | lightning | | | | |
| Zodiac Escutcheon, Rubber Suit, Diamond Armlet | | | | lightning | |
| Adamant Hat, Adamant Vest | ice | | fire | | |
| White Mask, Sage's Ring | | holy | | | |
| Steel Mask, Bone Mail | holy | | dark | | |
| Windbreaker, Agate Ring | | | wind | | |
| Viking Coat | | | | water | |
| Argyle Armlet | | | dark | | |
| Manufacted Nethicite | | | all eight | | |
| Cat-ear Hood | | | ice, wind | | |

The environment class over the 279 weather lanes of `map_ref.bin` (93 blocks of three):

| Class | Lanes |
|---:|---:|
| `0` | 12 |
| `1` | 1 |
| `2` | 4 |
| `3` | 16 |
| 4 (no rule) | 246 |

The terrain table at header `+0x14` holds `4, 3, 4, 4, 1, 2, 4, 4, 3, 3, 4, 0, 0, 4, 4, 0, 4, 2` for
ground indices 0-17 and 0 for indices 18-31. Classes 3 and 4 match no rule.

## Modding notes

- The magick and weapon multipliers are constants in `.rdata`: 2.0 at `01CEBC08`, 0.5 at `01CEBB70`, 1.5
  at `00901B3C`, and the weather factor 1.2 at `008FCC90`. Other code loads the same addresses.
- An item's affinities are the five bytes of its attribute record; several items can point to one record.
- Giving a weapon an element is one byte, `+0x1E`. For bows, crossbows, guns and the other ammunition
  weapons the ammunition's byte counts instead.
- Weather and terrain scaling applies only to the recipes that list slot 94.

## Related

- [Action definition row](../Battle-Actions/action-definition-row.md) - the element byte of an action.
- [Action results](../Battle-Actions/action-results.md) - result `+0x140` and an enemy's affinity changes.
- [Steal](steal.md) - how an equipped item's augment byte reaches the effect layers.
- [Evaluation context](damage-formula.md) - the merged effect bits.
- [Choosing the field environment variant](../World-Areas-And-Travel/weather.md)
  - where the environment and weather classes are published.
