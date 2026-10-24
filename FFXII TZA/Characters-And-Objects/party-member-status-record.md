---
title: "Party member status record: the snapshot the menus and HUD read a party member through, field by field"
kind: "system"
category: "Characters and objects"
addresses: "0x00329220, 0x0031FE70, 0x00320040, 0x0031FEC0, 0x0031FF70, 0x0031B9F0, 0x0031FDA0, 0x003879C0, 0x0030C2C0, 0x003135E0, 0x00313800, 0x00303EE0, 0x00327200, 0x0030A310, 0x002F8F20, 0x00387090, 0x003A1960, 0x00324020, 0x00263C20, 0x00313F60"
---

## What the player sees

The status screen, the party menu and the HUD name strip show a member's name, level, HP and its
cap, MP and its bars, experience and the points to the next level, LP, the equipment, the status
icons with their countdowns, and whether the member is the leader, KO'd, engaged, out of range or
in the middle of an action. None of those screens reads the party's stats directly: each asks for a
fresh 192-byte snapshot of the member and reads that.

## How it works

### The builder and its callers

`0x00329220(stats, memberSlot, out, full)` fills the `0xC0`-byte record at `out` from the party stats
record `stats`, the battle unit that owns it and the party row, and returns `out`. `full` adds the
level, experience, LP, licence count and equipment. Four wrappers resolve the member first:

| Wrapper | Member argument | `full` | How the stats record is found |
|---|---|---|---|
| `0x0031FE70(table, index, out)` | an index 0-8 into one of the five slot tables (`0x0031B9F0`: table 0 is the nine words at block `+0x5A48`, 1 `+0x5A5A`, 2 `+0x5A6C`, 3 `+0x5A7E`, 4 `+0x5A90`; `0x00322C50(0x17, index)` admits the index) | 0 | the chosen word is the slot; a slot above `0x27`, or a rejected index, gives a null record and the builder fills only the header |
| `0x00320040(table, index, out)` | the same | 1 | the same; the record is `[0x02EBF190] + 8 + slot * 0x1C8` |
| `0x0031FEC0` | an actor | 1 | the actor's unit (`0x00263E30`), its stats `+0x698`; the member slot is the position of stats byte `+4` among the four party slot words at block `+0x5A5A`, or -1 |
| `0x0031FF70` | a packed actor handle | 1 | the same through `0x003588B0`, gated on `0x02089340` bit `0x10` |

`memberSlot` is therefore the position in the chosen table for the first two wrappers and the
position in the four-word party table for the other two, while flag bits `0x400` and `0x800` compare it with
positions in the nine-word table at `+0x5A48`.

The callers of the wrappers:

- `0x0031FE70` from `0x00273880`;
- `0x00320040` from the input arbiter `0x00253C70` and `0x00254560` (counting members whose type `+0x60`
  is not negative and flag bit 1 is clear), `0x00272E70`, `0x00283270` (table 3; keeps nine copies at
  `[0x0209AC30] + 0x408 + i * 0xC0`) and `0x0035BC50`;
- `0x0031FEC0` from `0x002BFD20` (copies it into its widget at `+0xC0`);
- `0x0031FF70` from `0x00272E10`, `0x00273270` and `0x003C3340`.

### In execution order

1. The record is zeroed, `+0x60` is set to `0xFFFF`; a null stats record returns here
   (`0x0032923A`-`0x00329265`). Flag bit `0x8` stays 0 unless a focus unit exists.
2. The owning unit is found by scanning the unit pool (`0x00236850`, `0x00236820`) for the unit whose
   `+0x698` is this record; the focus unit is the current party focus (`0x003590D0`, `0x003588B0`,
   `0x00263E30`) when `0x02089340` bit `0x10` is set and that unit's flag bit `0x8` is set.
3. The flag bits that do not need the unit are computed: 10, 11, 4, 14, 16 and 17 (the table under
   Layouts).
4. The stats fields are copied: HP and MP, charges and bars, the two status words, type and kind,
   the merged status layers, the five affinity bytes and the 32 countdown bytes taken from the
   `u32[32]` status durations at `+0xBC`.
5. For a kind-0 record (a party member) the name is resolved from the party row and the three row
   bytes are copied; flag bits `0x2` and `0x4` classify the type.
6. Flag bit `0x80` is copied from stats `+0x00` bit `0x4`; with `full`, level, experience, points to the
   next level, LP, licence count and the six equipment words follow.
7. `+0x04` becomes the actor handle of the roster's member `memberSlot` (`0x00263750`, `0x003589B0`).
8. When a unit owns the record, the unit-side fields and flag bits `0x1`, `0x40`, `0x100`, `0x200`, `0x1000`, `0x2000`, `0x8000` and `0x8` are
   written, the name pointer is replaced by the empty string and `+0x04` by the unit's own handle.

### The flag word

| Bit | Set when |
|---|---|
| 0 | the member counts as KO'd: no stats record, or status bits `0x1`, `0x2` or `0x80000000` (KO, Stone, bit `0x80000000`) in `+0x3C` or `+0x64` while the current area's town flag (`0x00313F60`, area word bit `0x8000`) is clear (`0x0032978D`-`0x003297A8`) |
| 1 | type `+0x60` is 7 to 25 |
| 2 | type is 27 to 39 |
| 3 | the squared XZ distance between the unit's and the focus unit's positions (`+0xE0`, `0x003A1960`) is above `400.0` (`0x00915A08`): the member is out of range |
| 4 | `0x0031FDA0(unit)`: 1 when the unit is null, its flag bit `0x10` is clear or bit `0x80000000000` is set; for a kind-0 stats record, 1 when the type is `0x1A` and 0 otherwise; else 1 when the spawn record has flag bit `0x8` or `0x40`, otherwise status bit `0x1000000` |
| 6 | unit flag bit `0x2` |
| 7 | stats `+0x00` bit `0x4` |
| 8 | unit flag bit `0x1000000`, or an action id at most `0x21E` with phase `+0x6B4` at least 9 |
| 9 | unit flag bit `0x800000` |
| 10 | block `+0x5B04` bit `0x1` is set (`0x003135E0`) and `0x00320890(block +0x5AD5)` equals `memberSlot` (`0x00313800`) |
| 11 | block `+0x5B04` bit `0x2` is set (`0x00303EE0`) and the position of block byte `+0x5AA4` in the nine bytes at `+0x5A48` (stride 2, `0x00327200`) equals `memberSlot` |
| 12 | action id at most `0x21E` and phase at least 9 |
| 13 | action id at most `0x21E` and phase at least 3 |
| 14 | the unit has flag bit `0x10`, its stats record is null or of a kind other than 0, and the spawn record has flag bit `0x40` or the status words carry bit `0x1000000` (`0x00329337`-`0x0032937B`) |
| 15 | idle: no action context `+0x708`, action id `0xFFFF`, or phase 0 |
| 16 | `0x003879C0(stats)`: for a kind-1 owner, bit `0x80` of byte `+0x12` of the class row `[unit + 0xE68]` |
| 17 | `0x0030C2C0(unit)`: unit flag bit `0x10000000000000` (dword `+4` bit `0x100000`), after `0x002FEAD0` when `0x003278C0()` is 0 |

Block offsets are offsets into the battle-state block `[0x02EBF190]`
([its field map](../Party/party-data.md)); `+0x5AA4` is
the party leader byte and `+0x5AD5` the special-presentation actor there.

### HP, MP and the countdowns

- `+0x20` is HP (`+0x48`). `+0x24` is the effective maximum: `max(HP, 1)` while status bit `0x10000` is set
  in either status word, else `+0x24`. `+0x28` is the cap: the same under status bit `0x10000`, else
  `+0x24` doubled when status bit `0x10000000` is set.
- `+0x2C` is MP (`i16 +0x4C`), `+0x30` the capacity (`+0x28`), `+0x34` the capacity when bit `0x80` of
  both layer bytes `+0x6C` and `+0x7C` is clear and 0 otherwise, `+0x38` the `i16` at `+0x06`.
- `+0x66 + s` for `s` from 0 to 31 is the low byte of the duration dword `+0xBC + 4 * s` minus 1
  when status `s` is present and `s` is 2 or 6, and `0xFE` otherwise (`0x00329500`-`0x00329539`).

### The name and the party row

For a kind-0 record the party row is `[0x02EBF130]`'s section `+0x0C` at stride `+8` times the type;
its word `+0x30` is split into a bank index (high 5 bits) and an entry (low 11 bits) through the text
banks at `[0x02EBF170]`, and `0x002B58B0(block, 0)` gives the pointer stored at `+0x10`. `0x0030A310(row, i)`
returns row byte `+4 + i` for `i` below 3, which fill the words `+0xB4`, `+0xB6` and `+0xB8`. When a
unit owns the record the name pointer is replaced by the empty string at `0x01CEB638`.

### Experience, LP and equipment

With `full` set: `+0xBA` is the level (`+0x1C2`), `+0x90` the experience (`+0x18C`), `+0xB0` the LP
(`+0x190`), `+0xBB` the number of licence bits set among bits 0-17 of the licence bytes at `+0x194`
(`0x00324020`), and `+0x98`-`+0xAC` the six words `+0x50`-`+0x5A` each shifted left by 16. `+0x94` is
the points to the next level:

```python
curve(level) = sum for k = 2 .. level + 1 of trunc(float(k * k * k) * 0.4 + float(12 * k * k))   (0x002F8F20; 0 for level 0, -1 for level 99 and above)
+0x94 = curve(level) - experience
```

### The unit-side fields

While a unit owns the record:

- `+0x88` is the spawn record's `+0x12` (`[unit + 0x6A0]`), `+0x04` the unit's handle (`+0x08`),
  `+0x18` and `+0x1C` the unit's `+0x64` and `+0x68`;
- `+0x64` is the word `+0x52` of the class row `[unit + 0xE68]` for a kind-1 record whose actor class
  nibble (`0x00263C20`, byte `+0x0E` of the actor) is not 3, else `0xFFFF`;
- while the unit is acting (context `+0x708` set, id at most `0x21E`, phase not 0): `+0x3C` and
  `+0x40` are the unit's `+0x768` and `+0x76C`, `+0x08` the focus `+0x710`, and `+0x5C` the action
  id, or `0x00387090(stats)` once the phase is 9 or more; otherwise they are 0, 0, 0 and `0xFFFF`;
- `+0x5E` is the unit's `+0xBA0` while unit flag bit `0x4000` is set, else `0xFFFF`.

## Layouts

Struct PartyMemberStatusRecord size=`0xC0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | flags | the flag word above |
| `+0x04` | `u32` | actorHandle | the roster member's handle, or the owning unit's `+0x08` |
| `+0x08` | `u32` | focusHandle | the unit's `+0x710` while acting |
| `+0x10` | `u8*` | name | the party row's name text; the empty string when a unit owns the record |
| `+0x18` | `u32` | unitField64 | unit `+0x64` |
| `+0x1C` | `u32` | unitField68 | unit `+0x68` |
| `+0x20` | `i32` | hp | stats `+0x48` |
| `+0x24` | `i32` | hpMaxEffective | stats `+0x24`, or max(hp, 1) under status bit `0x10000` |
| `+0x28` | `i32` | hpCap | hpMaxEffective doubled under status bit `0x10000000` |
| `+0x2C` | `i32` | mp | stats `+0x4C` |
| `+0x30` | `i32` | mpCapacity | stats `+0x28` |
| `+0x34` | `i32` | mpCapacityShown mpCapacity, or 0 when layer bytes +0x6C or +0x7C carry bit 0x80 |  |
| `+0x38` | `i32` | secondary | stats `+0x06` |
| `+0x3C` | `u32` | actionField768 | unit `+0x768` while acting |
| `+0x40` | `u32` | actionField76C | unit `+0x76C` while acting |
| `+0x44` | `u32` | statusPresence | stats `+0x64` \| `+0x3C` |
| `+0x48` | `u32` | statusWord | stats `+0x3C` |
| `+0x4C` | `u8[16]` | mergedLayers | stats `+0x68` OR `+0x78`, byte-wise |
| `+0x5C` | `u16` | actionId | the unit's `+0x714`, or `0x00387090`(stats) from phase 9 |
| `+0x5E` | `u16` | issuedCommand | unit `+0xBA0` while unit flag bit `0x4000` |
| `+0x60` | `u16` | type | stats `+0x04` |
| `+0x62` | `u16` | kind | stats `+0x05` |
| `+0x64` | `u16` | classRowWord52 | [unit + `0xE68`] `+0x52` for a kind-1 record |
| `+0x66` | `u8[32]` | countdown | low byte of duration dword `+0xBC` + 4s, minus 1, for present statuses 2 and 6, else `0xFE` |
| `+0x86` | `u8` | charges | stats `+0x4E` |
| `+0x87` | `u8` | bars | stats `+0x37` |
| `+0x88` | `u8` | spawnCounter | spawn record `+0x12` |
| `+0x89` | `u8[5]` | affinity | stats `+0x40` .. `+0x44` |
| `+0x90` | `i32` | experience | stats `+0x18C` (full) |
| `+0x94` | `i32` | toNextLevel | curve(level) - experience (full) |
| `+0x98` | `u32[6]` | equipment | stats `+0x50` .. `+0x5A`, each << 16 (full) |
| `+0xB0` | `i32` | lp | stats `+0x190` (full) |
| `+0xB4` | `u16[3]` | partyRowBytes | party row +4 .. +6 |
| `+0xBA` | `u8` | level | stats `+0x1C2` (full) |
| `+0xBB` | `u8` | licenceCount | set bits among licence bits 0-17 (full) |

The sixth equipment word at `+0xAC` is the stats record's `+0x5A`, not a sixth slot: see the
[equipment slots page](../Items-Equipment-Shops-And-Licenses/equipment.md).

## Operations

Which screen reads which field of its copy:

| Reader | Fields |
|---|---|
| the input arbiter `0x00253C70`, `0x00254560` | type `+0x60` and flag bit `0x2`, counting members |
| `0x00272E10`, `0x00273880` | the actor handle `+0x04` |
| `0x00272E70` | the type `+0x60` |
| `0x00283270` | the type `+0x60` (compared with 6) and flag bit `0x2` |
| `0x00273270` | `+0xAC` shifted right by 16, the stashed slot-0 item id, compared by `0x0027C3D0` with the selected entry |
| `0x0035BC50` | type, handle and flag bits `0x2`, `0x4` and `0x40`, written back into its own table |
| `0x002BFD20` | layer byte `+0x51` bit `0x2`, `+0x44`, affinity `+0x89`, level `+0xBA` and flag bit `0x10000` through its widget, which it also hands to `0x002C0400` |

## Modding notes

- The screens never read the stats record directly; a displayed value changed without changing its
  source field is undone on the next build.
- "Out of range" on the HUD is a circle of 20 units (`400.0` squared) around the focused character.
- The countdown bytes show only statuses 2 and 6; every other status displays as `0xFE`.
- A KO'd member is not reported as KO'd in a town: the town flag of the current area masks the
  terminal statuses in flag bit `0x1`.

## Related

- [The battle stats record field map](../Damage-And-Battle-Formulas/unit-stats-fields.md): the source record.
- [The battle unit field map](battle-unit-fields.md): the unit fields read.
- [The battle-state block field map](../Party/party-data.md): the slot words and the leader byte.
- [Area flags and navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md): the town flag.
- [EXP, LP and level ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md): the experience curve.
