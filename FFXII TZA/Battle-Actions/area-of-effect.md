---
title: "Area of effect: radius, cone and line targeting, which side an area hits, and the target list"
kind: "system"
category: "Battle actions"
addresses: "0x0030D160, 0x0030AB40, 0x002FFF50, 0x0031A990, 0x00316CF0, 0x00316CD0, 0x00316D70"
---

## What the player sees

The player, a gambit or an enemy's AI picks one target. Everyone else the action hits is gathered
later, when the action's state machine reaches its target step, from where everybody stands at that
moment.

- **Radius.** An action with a radius of 0 hits only its target. Otherwise it hits units within that
  distance on the ground (height is ignored). Fire, Cure and Protect have no radius; Fira has 8,
  Cura and Protectga 10, and the -ja spells 100, which covers any battle area.
- **Centre.** The circle is centred on the target, except for actions centred on the user, such as
  the cries and songs (Screech, Wail, Angelsong, the Soundwaves), with a radius from 6 to 100. Every
  one is in the table under [Shipped data](#shipped-data).
- **Cones** (for example the breaths, the gazes, Flash and Tremor; every one is under
  [Shipped data](#shipped-data)) hit units in the radius that are also within an
  angle either side of the line from the user to the target. On most of them that angle is 180
  degrees, which makes the cone test pass for everyone in the radius, so the area is the plain
  circle around the target. Two cones have an angle of 0, which in practice leaves the target alone.
- **Lines** (Gust, Gale, Judgment, Innocence, Mach Wave) hit units in the radius whose sideways
  distance from the line between the user and the target is small enough.
- **Side.** An area spreads to the units on the same side as the chosen target, whichever side the
  user is on: Fira on an enemy spreads to its allies, Cura on a party member spreads to the party.
  Confuse on the target does not turn this around. Self-Destruct spreads to the other side from its
  target, and Mass Destruct hits everyone in range.
- **Who is skipped.** Units that are KO, Stone or X-Zone (except in towns, whose town flag waives this;
  [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md))
  and units failing the other targeting checks below are not added. An Invisible enemy is not
  skipped by this test.
- An action hits at most 32 units.

## How it works

### The gatherer

`0x0030D160` (1,004 bytes) is called once, by the standard-action state machine at
`0x00304EE2`, as `(unit, effectiveActionId, focusHandle, buffer)`: the action id comes from
`0x00387090` (`0x00304ECC`), the focus handle from the action context `+0x60`, and the buffer is the
context's target list at `+0xC8` (context = unit `+0x6B0`, so the list is at unit `+0x778`)
(`0x00304ED1`-`0x00304EE2`). It returns the list's count (`0x0030D51C`).

1. The chosen target is resolved from the focus handle (`0x0031B7E0`); if it does not resolve the
   function returns 0 and leaves the list alone (`0x0030D18A`-`0x0030D195`).
2. The action row is `table + stride * id`, with the table at `0x02EBF138` (base through `0x0020E600`,
   stride the `u16` at table `+8`) (`0x0030D19B`-`0x0030D1E9`).
3. The list is cleared, keeping bit 0 of its flag byte (`0x00316CF0`), and the chosen target is
   appended first (`0x0030D1F3`-`0x0030D200`).
4. **Stats-record path.** When the user's stats-record list (below) is not empty, nothing below runs;
   with a radius the list is rewritten from the mapped battle slots (`0x0030D205`-`0x0030D250`).
5. **Radius.** With the row's byte `+0x06` at 0, the area pass is skipped (`0x0030D255`-`0x0030D26B`).
   Otherwise the radius is squared and compared with squared XZ distances (`0x0030D2BD`,
   `0x0030D3A3`-`0x0030D3AC`). The centre is the user's position (unit `+0xE0`) when bit 21
   (`0x200000`) of the flag word `+0x0C` is set, otherwise the chosen target's (`0x0030D271`-`0x0030D29B`).
6. **Heading.** When bit 24 or 25 is set (`0x3000000`, `0x0030D2C0`), the heading from the user to the
   chosen target is computed (`0x0031AC90`; the user's facing `+0x160` when the two positions coincide
   in X and Z) (`0x0030D2D2`-`0x0030D2E7`). The row's byte `+0x07` is kept as a width and, times
   2 pi / 360 (`0x01CEBC78`, `0x00902438`), as an angle (`0x0030D2EC`-`0x0030D308`).
### Candidates

Every slot from 0 to `0x00236850()` whose unit has bit 4 of its first byte set (`0x00321170`) is a
candidate; the chosen target itself is skipped (`0x0030D313`-`0x0030D34D`). A candidate is appended with
`0x00316CD0` (`0x0030D422`) when it passes these tests, in order:

| Test | Passes when |
|---|---|
| eligibility | `0x002FFEF0(candidate, user, 1)` returns non-zero (`0x0030D35F`); see below |
| side | bit 3 of the row's word `+0x36` is set, or the side predicate called as `(chosenTarget, candidate, 1)` returns 0 (`0x0030D36C`-`0x0030D391`) |
| distance | the candidate is inside the radius (`0x0030D3A8`) |
| cone (bit 24) | the absolute angle between the heading and the user-to-candidate heading, normalised to plus or minus pi by `0x0031A930`, is not above the angle (`0x0030D3B1`-`0x0030D3E1`) |
| line (bit 25, bit 24 clear) | the candidate's offset from the user, rotated into the heading by `0x00325EA0`, has an absolute sideways component not above the width (`0x0030D3E3`-`0x0030D419`) |

The side predicate is `0x0030BB10` when bit 2 of `+0x36` is clear (it returns 1 for relationship class
0 or 2) and `0x0030BCB0` when bit 2 is set (1 for class 0 or 1). The two are loaded with `lea` and
called through `rax`.

### Whole party

When bit 1 of the flag word is set - whatever the radius - the units at the four party positions
(`0x0031B810(i)`, the slot byte at `[0x02EBF190] + 0x5A5A + i*2`) are appended, unless already in the
list (`0x00316D70`). Only units that have a stats record and either none of status bits 0, 1 and 31
(`0x80000003`) or a non-zero `0x00377C20()` count; they are staged in `0x022C1788` first
(`0x0030D461`-`0x0030D50A`).

### The stats-record list

Besides the unit list, the user can carry a list of stats-record indices (actor type ids): count
`+0x6B6`, bytes from `+0x6B9`.

- The commit `0x0030F760` puts one entry there (from `0x022C1DB8 + 12 * [unit+0xEA9]`) when bit 1 of the
  action-context word `unit+0x6B0` is set (`0x0030F865`-`0x0030F894`).
- The action reset `0x003105D0` clears it (`0x0031060A`).
- The effect applier `0x00307300` resolves each byte through `0x00320A40` and applies the result to it
  (`0x003073D7`-`0x0030744B`).
- With a radius, the gatherer rewrites the list from index 0: each mapped battle slot 4 to 8 whose
  stats record exists (`0x00320AB0(slot, 3)`) contributes its byte `+0x04`, and the new count goes to
  `+0x6B6`. Without a radius the committed entry stands.

### The relationship class

`0x0030AB40(a, b, flags)` returns 0 when either unit is null, either
actor's class nibble (`0x00263C20`) is 5, or either unit lacks bit 4 of its first byte
(`0x0030AB64`-`0x0030ABB2`). A unit is on the party side when its stats byte `+0x05` is 0 or its class
nibble is 3. The result is 1 when both are on the same side and 2 when not; when bit 0 of `flags` is
clear and `a` has status bit 5 (Confuse) in `+0x64 | +0x3C`, the answer is swapped
(`0x0030ABB8`-`0x0030AC25`). The gatherer passes 1 to the side predicates, so Confuse never changes
an area's side.

### Eligibility

`0x002FFEF0(candidate, user, mode)` asks `0x0030AB40(candidate, user, 0)` - here
Confuse on the candidate does count - and passes 1 as the hostile flag when the class is above 1,
else 0. It returns 1 when `0x002FFF50(candidate, hostile, mode)` returns an empty mask
(`0x002FFF07`-`0x002FFF35`). `0x002FFF50` sets:

| Bit | When |
|---|---|
| `0x01` | the unit is null or lacks bit 4 of its first byte |
| `0x02` | no stats record, or status bits 0, 1 or 31 (KO, Stone, X-Zone) set while `0x00377C20()` returns 0 |
| `0x04` | `0x003125E0(unit)` returns non-zero: for an active unit, when its flag word has bit 9, 10 or 11, the word at `+0x04` has bit 2, bit 1 is set while the unit has no stats record or is KO, Stone or X-Zone (without the map waiver), or, for an enemy-side unit, bit 3 or 4 of the dword at `[unit+0x6A0]` is set |
| `0x08` | `0x0030B950(unit, hostile)` returns non-zero: bits 9-11 of `0x02089340` (`0x0030B770`), or `0x0030B7F0` - unit flag bit 8, unit flag bit 30 when `hostile`, a party-side unit of type id `0x1A`, or `0x0017D470()` in state 1 or 2 |
| `0x10` | enemy side (stats `+0x05` = 1), `mode` is not 1, and status bit 24 (Invisible) set |
| `0x20` | enemy side, `mode` is not 3, and bit 5 of the byte at `[unit+0x6A0]` |
| `0x40` | enemy side and bit 6 of the byte at `[unit+0x6A0]` |

The gatherer uses mode 1, so bit `0x10` is never set for its candidates. `0x00377C20` returns bit 15
of the current field's map-info word.

### Entry flags

The effect applier `0x00307300` writes each entry's `+0x08`: the low byte is the
outcome code from `0x0030DAE0` (`0x003075BF`), and bits 8, 9, 10 and 11 are set from result flags 3, 2, 1
and 0 (bit 10 only when bit 21 of the user's word `+0x04` is clear, `0x003075C3`-`0x003075EC`). Readers:
the HP write `0x00300530` (bit 8, `0x0030071A`), `0x0031ADB0` (bits 8 and 11, low byte 10), `0x00322760` (low
byte 8), `0x003176E0` (low byte), and the combo continuation `0x00308610`/`0x0030C010` (bit 10); bit 10 is
cleared at `0x002FFA14`, `0x0030019B`, `0x00300EAD`, `0x003011E0` and `0x0030AFF8`.

Before it resolves a target, the applier turns the entry's low byte back into an outcome with
`0x002FEE20`, the inverse of `0x0030DAE0`, and passes it in the result's byte `+0x04` to `0x00385F60`
(`0x00307552`-`0x00307577`):

| Entry code | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Outcome (`0x002FEE20`) | `0` | `5` | `1` | `3` | `2` | `4` | `6` | `7` | `8` | `10` | `11` | `9` |

### The shape reader

`0x0031A990(row, out)` (154 bytes) describes the same fields as a shape: it
writes 0 to `out+4`; with no radius or with bit 12 of the flag word set, the shape is 5 (with
`out+4` = 1) when bit 1 is set and 0 otherwise; otherwise 3 for bit 24 (radius at `+8`, the angle in
radians at `+0xC`), 4 for bit 25, and 1 or 2 for bit 21 clear or set (radius at `+8`)
(`0x0031A990`-`0x0031AA29`). Its one caller is `0x0031AA30` (`0x0031AB58`), which is called from `0x00321060`
and `0x00328530` and jumped to from `0x0031AB80`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | flags | bit 0 kept by the clear (`0x00316D05`-`0x00316D16`); the rest cleared |
| `+0x01` | `u16` | keys | cleared to 0 by `0x00316D1D` |
| `+0x03` | `u8` | pad3 | cleared by the memset of `0x00316D0B` |
| `+0x04` | `i32` | count | entries in use; signed (movsxd at `0x00316CD0` and `0x00316D70`); append refuses at 32 (`0x00316CD4`) |
| `+0x08` | `u8[512]` | entries | 32 ActionTargetEntry records of 16 bytes |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | actorWork | the unit's `+0x10` object; stored by `0x00316CDC`, compared by `0x00316D83` |
| `+0x08` | `u32` | entryFlags | low byte the outcome code (`0x0030DAE0`), bits 8-11 result flags; written by the effect applier `0x00307300` |
| `+0x0C` | `u32` | tail | no unit-relative reader of `+0x78C` in the image (entry-pointer reads not excluded) |

## Shipped data

The shipped action table (`battle_pack.bin`, read through `0x02EBF138`) marks 26 actions as centred on the user (bit 21
of the flag word `+0x0C`). The radius is the row's byte `+0x06`. The same rows carry the flag name "area centred on
the user" in [Action list](action-list.md).

| Radius | Actions centred on the user (id) |
|---|---|
| `6` | Piercing Graviga (`443`) |
| `8` | Angelsong (`349`), Magick Ballad (`350`), Warsong (`351`), Vespersong (`352`), Mystery Waltz (`353`), Hero's March (`354`), Time Requiem (`355`), Soul Etude (`356`), Fly, Enkidu! (`463`), Now, Enkidu! (`464`), Eviscerator (`475`), Force of Will (`486`), Azure Vortice (`488`), Crimson Vortice (`489`) |
| `10` | Screech (`342`), Scream (`343`), Wail (`344`), Eerie Soundwave (`345`), Joyous Soundwave (`346`), Rage (`418`), Shockstorm (`457`), Pollen Dance (`478`) |
| `20` | Monarch Sword (`468`) |
| `100` | Inviolable Will (`491`), Ascension (`495`) |

Cones (bit 24) and lines (bit 25) take the angle or half-width from byte `+0x07`; in [Action list](action-list.md)
they carry the flag names "cone area" and "line area". Monarch Sword and Eviscerator are both centred on the user
and cones.

| Shape | Radius | Angle or width | Actions (id) |
|---|---|---|---|
| cone | `3` | `40` | Cloying Breath (`376`) |
| cone | `3` | `60` | Bad Breath (`377`) |
| cone | `3` | `80` | Putrid Breath (`378`) |
| cone | `3` | `120` | High Jump (`476`) |
| cone | `4` | `45` | Tail Swipe (`404`) |
| cone | `4` | `75` | Stone Gaze (`335`), Phantasmal Gaze (`336`), Flash (`337`) |
| cone | `4` | `180` | Spiral Cut (`394`), Snake Lash (`398`), Flatten (`403`) |
| cone | `6` | `60` | Aqua Bubbles (`357`), Mythril Bubbles (`358`), Breath (`362`), White Breath (`363`), Stone Breath (`364`), Poison Breath (`365`) |
| cone | `6` | `180` | Darkness (`327`), Ice Break (`328`), Water Spout (`329`), Shining Ray (`330`), Tremor (`331`), Tempest (`332`), Sandstorm (`333`), Pyromania (`334`), Blast Wave (`372`), Shock Wave (`373`), Pulsar Wave (`374`), Dark Shock (`375`), Spinkick (`390`), Sonic Turn (`399`), Chain Reaction (`409`), Discharge (`422`), Pollen (`424`), Power Stun (`438`), Power Spin (`442`), Bushfire (`458`), Sporefall (`459`), Sword Dance (`461`), Circle of Judgment (`471`) |
| cone | `8` | `0` | Eviscerator (`475`) |
| cone | `8` | `180` | Screwtail (`406`) |
| cone | `10` | `45` | Gatling Gun (`481`) |
| cone | `10` | `180` | Ultimate Illusion (`466`) |
| cone | `15` | `180` | Ground Shaker (`456`) |
| cone | `18` | `180` | Choco-Comet (`426`) |
| cone | `20` | `0` | Monarch Sword (`468`) |
| cone | `20` | `180` | Tree of Sephira (`492`) |
| cone | `100` | `180` | Gigaflare Sword (`496`) |
| line | `3` | `2` | Gust (`359`) |
| line | `4` | `3` | Innocence (`474`) |
| line | `5` | `2` | Mach Wave (`487`) |
| line | `5` | `3` | Gale (`360`) |
| line | `20` | `10` | Judgment (`411`) |

## Modding notes

- The area fields are bytes of the action row: `+0x06` radius, `+0x07` cone angle in degrees or line
  half-width; flag word `+0x0C` bits 1 (whole party), 21 (centre on user), 24 (cone), 25 (line);
  word `+0x36` bits 2 (other side from the target) and 3 (everyone).
- Shipped `battle_pack.bin`: 247 of 543 action rows have a radius (3, 4, 5, 6, 8, 10, 15, 18, 20 or
  100); 26 rows are centred on the user, 49 are cones (32 of them 180 degrees, two at 0), 5 are lines;
  no row has both cone and line bits, and no row without a radius has bits 21, 24 or 25.
- Of the 247 area rows, 245 follow the target's side, Self-Destruct has bit 2 and Mass Destruct bit
  3. Bit 1 is set only on 13 rows named Reserve.
- Remora Strike has an angle byte (180) but neither cone nor line bit, so its angle has no effect.
- 18 rows with radius 10 have bit 12: the 18 Quickenings, ids 208 to 225 (Red Spiral to
  Resplendence): the gatherer spreads them over the radius, while `0x0031A990` reports them
  as shape 0.
- Raising the radius to 100 makes a spell cover the whole battle area, as the -ja spells do.

## Related

- [The action definition row](action-definition-row.md) - the row these
  bytes and bits belong to.
- [Action range](action-range.md) - how close the user stands before the action runs.
- [Gambits and enmity](../Enemy-AI-And-Gambits/gambits.md) - other uses of
  the relationship class.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - status bits
  0, 1, 5, 24 and 31.
- [The field record table](../World-Areas-And-Travel/area-flags-navimapdata.md)
  - the map-info word whose bit 15 `0x00377C20` returns.
