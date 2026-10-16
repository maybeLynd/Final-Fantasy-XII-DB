---
title: "Action definition row: power, targeting, range, element and flag fields of a battle action"
kind: "format"
category: "Battle actions"
addresses: "00237FC0, 00236C30, 00238850, 003845F0, 0020E600, 00385F60, 0031C5D0, 0031EB20, 00390AB0"
---

## What the player sees

Every command that does something in battle is one row of one table: Attack, each magick and
technick, each item use, each summon, Quickening and Concurrence, each Foecraft move, and the traps.
The row decides what the action costs, how long it charges, how far it reaches, what it can target,
how wide its area is, how strong it is, its element, the statuses it inflicts and where it sits in the
command list. The name and help text are in the text banks, and the row holds their ids.

## Where it comes from

The rows are section 14 of `battle_pack.bin`, the section its directory entry at file offset `+0x3C`
points to. The section is an `st2e` table of 543 rows, 60 bytes each, starting `0x20` bytes into the
section. In the `us` file the section is at `0x13210`. Row *n* is action id *n*: Cure is row 0,
Attack row 150, Steal row 169.

Every reader computes the row itself rather than calling a getter (`0038B248`-`0038B28E` is one
example). It loads the registry slot `02EBF138`, resolves the slot's `+0x0C` through `0020E600` to
the first row, and adds the action id times the slot's `u16` stride at `+0x08`. While a recipe runs,
the action id is the formula scratch word `02AEDFD4`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u16` | helpId | help text id; 4000 = none (`0031C5D0` at `0031DBB1`, through `002F9860`) |
| `02` | `u8` | rangeNear | near range band, tenths; used when `+0x0C` bit 26 is clear (`00320D70`) |
| `03` | `u8` | rangeMiddle | middle range band, tenths (`00320D70`) |
| `04` | `u8` | knockback | knockback chance base (`00388B50` at `00388BE6`) |
| `05` | `u8` | reach | reach in tenths; bounds the Reflect retarget (`00309300`, `00384F40`) |
| `06` | `u8` | areaRadius | area radius; 0 = the target alone (`0030D160`, `0031A990`) |
| `07` | `u8` | areaAngle | cone half-angle in degrees, or line half-width (`0030D160`, `0031A990`) |
| `08` | `u8` | recipe | damage recipe; 0 = the weapon's (`00385F60` at `0038617E`) |
| `09` | `u8` | chargeBase | charge time base (`002F8410` at `002F8586`) |
| `0A` | `u8` | cost | MP cost, or Mist charges for kinds 5 and 6 (`002F95D0`, `00308FF0`, `00309110`) |
| `0B` | `u8` | b0B | 1-3 on rows 182-207 only |
| `0C` | `u32` | flags | action flags; table below |
| `10` | `u8` | power | action power (31 formula slots) |
| `11` | `u8` | power2 | second power byte (`00388C10`, `0038A9D0`, `0038EB30`) |
| `12` | `u8` | hit | hit threshold into `02AEDFE0` (`00389040` at `00389089`) |
| `13` | `u8` | element | one bit per element (`0038B220`, `0038B6A0`) |
| `14` | `u8` | statusChance | on-hit status chance, percent (`0038F970` at `0038F9B0`) |
| `15` | `u8` | boostPercent | percent added to the working magnitude `02AEE004` (`0038F8E0` at `0038F93B`) |
| `16` | `u8[2]` | pad16 | 0 on every row |
| `18` | `u32` | statusMask | statuses the action applies or removes, one bit each (`003872D0`, `003851F0`) |
| `1C` | `u8` | category | action category 0-9; picks the presentation event (`0030A370` at `0030A37F`) |
| `1D` | `u8` | enmityDirect | enmity toward the user (`003216E0` at `00321716`) |
| `1E` | `u8` | kind | action kind; picks what `+0x22` holds (`003093D0`, `00469EC0`) |
| `1F` | `u8` | enmitySpread | enmity passed to foes already hostile (`00321733`) |
| `20` | `u8` | enmityOthers | enmity taken from the others, negated (`00321744`) |
| `21` | `u8` | effectClass | 0-8, picks an effect started while the action runs (`00329F80` at `00329FE7`) |
| `22` | `u16` | linkedId | the magick, technick, item or ability id of the row (`003093D0`, `003060E0`) |
| `24` | `u16` | effectId | the action's own effect id; bit 15 a flag (`0030AC50`, `0030A190`, `00310DB0`) |
| `26` | `u8` | esper | the Esper's row in the party table, on the 13 summon rows (`00306760`) |
| `27` | `u8` | pad27 | 0 on every row |
| `28` | `u16` | cinematicId | Quickening and Concurrence cinematic (`0030A190` at `0030A209`) |
| `2A` | `u16` | pad2A | 0 on every row |
| `2C` | `u16` | flags2 | second flag word; table below |
| `2E` | `u16` | descId | description text id (`0031C5D0` at `0031DBBE`) |
| `30` | `u32` | event | presentation event of phases 9-11 (`0030A370` at `0030A457`) |
| `34` | `u16` | nameWord | name: bank = word >> 11, entry = word & `0x7FF` (`00305F10`, `00536410`) |
| `36` | `u16` | targetFlags | third flag word; table below |
| `38` | `u8` | menuPage | command list page (`00237FC0` at `00238033`) |
| `39` | `u8` | menuRow | row on that page (`00237FC0` at `00238043`) |
| `3A` | `u8` | aiReaction | bit number set in the AI operand mask of kind 10 (`00312170` at `003121F5`) |
| `3B` | `u8` | pad3B | 0 on every row |

### The kind byte

Byte `+0x1E` is the action's kind ([Command availability](command-availability.md) has the
ownership rule for each):

| Kind | Rows | Examples |
|---:|---:|---|
| `0` | 1 | Attack |
| `1` | 81 | magicks: Cure, Blindna |
| `2` | 24 | technicks: First Aid, Charge |
| `3` | 51 | items: Potion, Ether |
| `5` | 13 | summons: Belias, Mateus |
| `6` | 18 | Quickenings: Red Spiral, White Whorl |
| `7` | 235 | Foecraft: Fear, Aerora |
| `8` | 16 | traps: explosion, choking gas |
| `9` | 26 | Esper attacks: Painflare, Hellfire |
| `10` | 16 | Concurrences: Inferno, Torrent |
| `13`, `14`, `16`, `17` | 3, 1, 1, 1 | the Reserve rows 155-157, `actstop`, `escape`, `escapestop` |
| `255` | 56 | `NOT USED` and Reserve rows |

### The element byte

Bit *n* of `+0x13` is one element; no shipped row sets more than one:

| Bit | Rows | Examples |
|---:|---:|---|
| `0` | 19 | Fire, Fira, Firaga |
| `1` | 11 | Thunder, Thundara |
| `2` | 10 | Blizzard, Blizzara |
| `3` | 8 | Quakeja, Tremor |
| `4` | 13 | Aqua, Aquara |
| `5` | 13 | Aero, Aeroga |
| `6` | 9 | Holy, Holyja |
| `7` | 13 | Dark, Darkra |

### The flag word at +0x0C

| Bit | Rows | Effect (reader) |
|---:|---:|---|
| `0`, `2`, `3` | 71, 341, 416 | the user, allies and foes can be targeted ([Target selection](target-selection.md); `003230E0`, `0031EB20`) |
| `1` | 13 | the area is the whole party ([Area of effect](area-of-effect.md); `0030D461`) |
| `4` | 32 | sets bit 10 of the command entry (`0031F0A4`-`0031F0AF`) |
| `5`, `6` | 22, 103 | how the target list is built ([Target selection](target-selection.md); `00322BD5`-`00322BED`) |
| `8`, `9` | 186, 378 | copied to the query record's `+0x20` (`0031DB9E`-`0031DBA7`) |
| `11` | 57 | clears bit 5 of the result's byte `+0` (`00386079`); also read by `0031AA30` (`0031AB02`) |
| `12` | 18 | the shape reader reports the whole party or no area, whatever the radius (`0031A990`) |
| `13` | 162 | magick class: a target with effect 56 voids it as result kind 7 (`00390EE5`, `003910C3`); no charge time under effect 54 (`002F8689`) |
| `14` | 207 | physical class: effect 55 voids it as result kind 7 (`00390E9A`, `00391076`) |
| `16` | 78 | Reflect (status 23) bounces it: result kind 8 and a new target from `00384F40` (`00390D7F`, `00390DF1`-`00390E42`) |
| `17` | 28 | runs the special-guard roll (`00388058`) |
| `19` | 97 | Silence blocks it (`002FFE56`, [Command availability](command-availability.md)) |
| `21` | 26 | the area is centred on the user ([Area of effect](area-of-effect.md); `0030D271`) |
| `24`, `25` | 49, 5 | the area is a cone or a line ([Area of effect](area-of-effect.md); `0030D2C0`) |
| `26` | 35 | the weapon's reach and range bands replace the row's ([Action range](action-range.md); `00309377`, `00320D74`, `00390C7F`) |
| `27` | 1 | the charge base comes from the weapon row's `+0x27` (`002F8494`, [Action phases](action-phases.md)) |
| `28` | 36 | changes the command entry (`0031F0EF`, `0031F157`) |
| `29` | 112 | the command entry carries a cost (`0031F000`) |
| `30` | 87 | runs a scene: summon, Quickening, Concurrence ([Quickenings and summons](quickenings-and-summons.md); 17 sites, `00304D3F` among them) |
| `31` | 64 | consumes an item: the command entry carries the item count (`0031F077`) |

Bits 13 and 14 are also copied into the kind-10 AI operand mask as its bits 8 and 9 (`00312213`-`00312232`).
Bits 7, 10, 15, 18 and 20 are set on 324, 292, 24, 1 (Attack) and 81 rows and are read by none of the
154 functions that resolve `02EBF138`: their word-wide reads mask other bits (`0030770D` keeps at most bit 13, masked by a 0-or-1 register, `0030D3AE` tests bit 24, `002F8494` bit 27, `002F8689` bit 13). No shipped row sets bits 22 or 23.

### The flag word at +0x2C

| Bit | Rows | Effect (reader) |
|---:|---:|---|
| `0`-`2` | 70 | a value 0-5; for kind-1 rows, values 0-4 pick which of five magick lists the row joins (`002376F0` at `002377FF`, `00237881`); 5 is only on row 81, `NOT USED` |
| `3` | 21 | the user gains MP from the damage when it has effect 86 (`002F92C1`, `002F9323`) |
| `4` | 40 | the user gains MP from the damage when it has effect 20 (`002F9330`-`002F937B`) |
| `6`, `7` | 10, 2 | the action may target a KO or a Stone unit ([Target selection](target-selection.md); `002FFAF5`, `002FFB30`) |
| `8` | 61 | the effect test of `0030CA80` is skipped (`0030CB71`) |
| `10`, `11` | 195, 65 | the target wakes from Sleep and loses Confuse, or loses Invisible (`00390F20` at `00391112`, `00391192`) |
| `13` | 98 | no License needed ([Command availability](command-availability.md); `00323F52`) |
| `14` | 93 | returned by `0030BB30` for categories 1-8 (`0030BC0C`) |

Bits 9, 12 and 15 (3, 20 and 10 rows) are read through the whole word by the AI order selectors
(`00303434`, `00303492`, `00308CF2`) and by `003851F0` and `003872D0` (`003852AB`, `00387382`).
Bit 5 is set on 227 rows and is read by none of the 154 functions that resolve `02EBF138`: their
word-wide reads take bits 0-2 (`00300B3F`, `00317CFF`, `0031CDC2`, `0031EF87`, `0032A46F`), bits 6 and 7
(`00322B67`, `00322B78`) or bits 12 and 15 (`00303496`, `00308CFB`, `00308D02`).

### The flag word at +0x36

| Bit | Rows | Effect (reader) |
|---:|---:|---|
| `0` | 51 | the action adds statuses: `003875D0` returns the mask `+0x18` only with it set and bit 9 of `+0x2C` clear (`00387629`); the gambit target picker passes over a unit that already has them all ([Gambit conditions](../Enemy-AI-And-Gambits/gambit-conditions.md); `0030856F`) |
| `1` | 26 | the action removes statuses: tested by `003872D0` (`00387331`); the gambit target picker passes over a unit that has none of them (`003084EF`) |
| `2` | 2 | the area takes the side opposite the target (Self-Sacrifice, Self-Destruct; `0030D36C`) |
| `3` | 1 | the area takes everyone (Mass-Destruct; `0030D36C`) |
| `4` | 227 | when clear, one branch of the pre-resolution gates fails the result (`00390D55`-`00390D63`) |
| `5` | 14 | the gambit target picker keeps a candidate whose byte `+0x55` is `0x0D` without testing what the action would change (`0030844B`-`00308457`) |

## Shipped data

| Field | Values in the 543 rows |
|---|---|
| `+0x02`, `+0x03` | 0 on 537 rows; `+0x02` is 1 on five rows and 20 on one, `+0x03` 20 on four and 15 on two |
| `05` | 100 × 212, 0 × 130, 30 × 56, 20 × 50, 255 × 39 |
| `06` | 0 × 296, 10 × 98, 8 × 63, 6 × 46, 100 × 13 |
| `07` | 0 × 490, 180 × 33, 60 × 7, 75 × 3 |
| `09` | 0 × 212, 3 × 149, 23 × 81, 1 × 32, 2 × 24; at most 60 |
| `0A` | 0 × 397, 2 × 23, 3 × 14, 8 × 12; at most 72; Cure 8 |
| `10` | 0 × 242, 100 × 36, 90 × 15; at most 253; Cure 20, Fira 67 |
| `12` | 100 × 312, 0 × 157 |
| `14` | 0 × 494; 100 on Bio, 35 on Firaja, 50 on Darkja |
| `+0x15`, `+0x16`, `+0x17`, `+0x27`, `+0x2A`, `+0x3B` | 0 on every row |
| `18` | 0 × 387; Blindna `0x80`, Poisona `0x100`, Raise `0x1` |
| `22` | `0xFFFF` × 343; 200 distinct ids |
| `26` | 27-39 on the summons Belias to Zodiark, 0 elsewhere |
| `28` | 120-153 on the 26 Quickening and Concurrence rows (Red Spiral 120) |
| `34` | the row's own number, except rows 128-142, which hold 136, 137, 128, 129, 130, 138, 139, 140, 141, 135, 142, 131, 132, 133, 134 |
| `+0x38`, `+0x39` | `0xFF` on 386 rows; Attack 0 / 0, Cure 1 / 0, Cura 1 / 1, Fira 2 / 9 |
| `3A` | 255 × 475; 15 × 49, 16 on Cure to Curaja and the Potions |

Cure's row, as stored:

```
a1 0f 00 00 00 64 00 00 04 17 08 00 4c 2d 19 30 14 00 00 00 00 00 00 00 00 00 00 00 01 0c 01 02
04 01 00 30 b3 00 00 00 00 00 00 00 30 10 10 27 00 00 00 00 00 00 30 00 01 00 10 00
```

## Loader behaviour

The table arrives with the battle data resource:

1. `BattleStorage_InitializeWorkArrays` registers `00238850` as the handler for resource `0x13`,
   named `STATIC` (`002369BB`-`002369CE`).
2. On delivery `00238850` stores the blob pointer in `0208E680` and jumps to `00236C30(1)`
   (`0023885A`-`0023886F`).
3. `00236C30` binds the battle tables from the blob's directory and calls `00237FC0` with entry
   `+0x3C` (`00236D7B`-`00236D85`).
4. `00237FC0` binds `02EBF138` to that section through `003845F0` (`00237FD5`-`00237FDE`), which
   stores the section pointer and rebases the header's offsets at `+0x0C`, `+0x10`, `+0x18` and
   `+0x1C` by the section address (`003845F4`-`00384640`).
5. It then walks every row once and files each row with both `+0x38` and `+0x39` set into the
   command grid at `0208D308` (`00238033`-`00238132`).

## Modding notes

- Power is `+0x10`, hit rate `+0x12`, status chance `+0x14`, statuses `+0x18` and element `+0x13`.
- `+0x08` re-routes the whole damage formula; 0 hands it to the equipped weapon.
- The MP cost is the byte `+0x0A`, before the augment adjustments of `002F95D0`.
- The name is not in the row: `+0x34` points into the text bank, so two rows can share a name.
- `+0x15` is a working percent boost that no shipped row uses.

## Related

- [Action range](action-range.md) - `+0x02`, `+0x03`, `+0x05` and flag bit 26.
- [Area of effect](area-of-effect.md) - `+0x06`, `+0x07` and the area flags.
- [Target selection](target-selection.md) - the target flags of `+0x0C` and `+0x2C`.
- [Command availability](command-availability.md) - kinds, costs, Silence and the License bit.
- [Action phases](action-phases.md) - the charge base and the scene flag.
- [Quickenings and summons](quickenings-and-summons.md) - `+0x26` and the scene rows.
- [Steal](../Damage-And-Battle-Formulas/steal.md) - one recipe from `+0x08` end to end.
