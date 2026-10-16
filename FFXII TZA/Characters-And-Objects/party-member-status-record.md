---
title: "Party member status record: the snapshot the menus and HUD read a party member through, field by field"
kind: "system"
category: "Characters and objects"
addresses: "00329220, 0031FE70, 00320040, 0031FEC0, 0031FF70, 0031B9F0, 0031FDA0, 003879C0, 0030C2C0, 003135E0, 00313800, 00303EE0, 00327200, 0030A310, 002F8F20, 00387090, 003A1960, 00324020, 00263C20, 00313F60"
---

## What the player sees

The status screen, the party menu and the HUD name strip show a member's name, level, HP and its
cap, MP and its bars, experience and the points to the next level, LP, the equipment, the status
icons with their countdowns, and whether the member is the leader, KO'd, engaged, out of range or
in the middle of an action. None of those screens reads the party's stats directly: each asks for a
fresh 192-byte snapshot of the member and reads that.

## How it works

### The builder and its callers

`00329220(stats, memberSlot, out, full)` fills the `C0`<sub>h</sub>-byte record at `out` from the party stats
record `stats`, the battle unit that owns it and the party row, and returns `out`. `full` adds the
level, experience, LP, licence count and equipment. Four wrappers resolve the member first:

| Wrapper | Member argument | `full` | How the stats record is found |
|---|---|---|---|
| `0031FE70(table, index, out)` | an index 0-8 into one of the five slot tables (`0031B9F0`: table 0 is the nine words at block `+5A48`<sub>h</sub>, 1 `+5A5A`<sub>h</sub>, 2 `+5A6C`<sub>h</sub>, 3 `+5A7E`<sub>h</sub>, 4 `+5A90`<sub>h</sub>; `00322C50(17h, index)` admits the index) | 0 | the chosen word is the slot; a slot above `27`<sub>h</sub>, or a rejected index, gives a null record and the builder fills only the header |
| `00320040(table, index, out)` | the same | 1 | the same; the record is `[02EBF190] + 8 + slot * 1C8h` |
| `0031FEC0` | an actor | 1 | the actor's unit (`00263E30`), its stats `+698`<sub>h</sub>; the member slot is the position of stats byte `+4` among the four party slot words at block `+5A5A`<sub>h</sub>, or -1 |
| `0031FF70` | a packed actor handle | 1 | the same through `003588B0`, gated on `02089340` bit 4 |

`memberSlot` is therefore the position in the chosen table for the first two wrappers and the
position in the four-word party table for the other two, while flag bits 10 and 11 compare it with
positions in the nine-word table at `+5A48`<sub>h</sub>.

The callers of the wrappers:

- `0031FE70` from `00273880`;
- `00320040` from the input arbiter `00253C70` and `00254560` (counting members whose type `+60`<sub>h</sub>
  is not negative and flag bit 1 is clear), `00272E70`, `00283270` (table 3; keeps nine copies at
  `[0209AC30] + 408h + i * C0h`) and `0035BC50`;
- `0031FEC0` from `002BFD20` (copies it into its widget at `+C0`<sub>h</sub>);
- `0031FF70` from `00272E10`, `00273270` and `003C3340`.

### In execution order

1. The record is zeroed, `+60`<sub>h</sub> is set to `FFFF`<sub>h</sub>; a null stats record returns here
   (`0032923A`-`00329265`). Flag bit 3 stays 0 unless a focus unit exists.
2. The owning unit is found by scanning the unit pool (`00236850`, `00236820`) for the unit whose
   `+698`<sub>h</sub> is this record; the focus unit is the current party focus (`003590D0`, `003588B0`,
   `00263E30`) when `02089340` bit 4 is set and that unit's flag bit 3 is set.
3. The flag bits that do not need the unit are computed: 10, 11, 4, 14, 16 and 17 (the table under
   Layouts).
4. The stats fields are copied: HP and MP, charges and bars, the two status words, type and kind,
   the merged status layers, the five affinity bytes and the 32 countdown bytes taken from the
   `u32[32]` status durations at `+BC`<sub>h</sub>.
5. For a kind-0 record (a party member) the name is resolved from the party row and the three row
   bytes are copied; flag bits 1 and 2 classify the type.
6. Flag bit 7 is copied from stats `+00`<sub>h</sub> bit 2; with `full`, level, experience, points to the
   next level, LP, licence count and the six equipment words follow.
7. `+04`<sub>h</sub> becomes the actor handle of the roster's member `memberSlot` (`00263750`, `003589B0`).
8. When a unit owns the record, the unit-side fields and flag bits 0, 6, 8, 9, 12, 13, 15 and 3 are
   written, the name pointer is replaced by the empty string and `+04`<sub>h</sub> by the unit's own handle.

### The flag word

| Bit | Set when |
|---|---|
| 0 | the member counts as KO'd: no stats record, or status bits 0, 1 or 31 (KO, Stone, bit 31) in `+3C`<sub>h</sub> or `+64`<sub>h</sub> while the current area's town flag (`00313F60`, area word bit 15) is clear (`0032978D`-`003297A8`) |
| 1 | type `+60`<sub>h</sub> is 7 to 25 |
| 2 | type is 27 to 39 |
| 3 | the squared XZ distance between the unit's and the focus unit's positions (`+E0`<sub>h</sub>, `003A1960`) is above `400.0` (`00915A08`): the member is out of range |
| 4 | `0031FDA0(unit)`: 1 when the unit is null, its flag bit 4 is clear or bit 43 is set; for a kind-0 stats record, 1 when the type is `1A`<sub>h</sub> and 0 otherwise; else 1 when the spawn record has flag bit 3 or 6, otherwise status bit 24 |
| 6 | unit flag bit 1 |
| 7 | stats `+00`<sub>h</sub> bit 2 |
| 8 | unit flag bit 24, or an action id at most `21E`<sub>h</sub> with phase `+6B4`<sub>h</sub> at least 9 |
| 9 | unit flag bit 23 |
| 10 | block `+5B04`<sub>h</sub> bit 0 is set (`003135E0`) and `00320890(block +5AD5h)` equals `memberSlot` (`00313800`) |
| 11 | block `+5B04`<sub>h</sub> bit 1 is set (`00303EE0`) and the position of block byte `+5AA4`<sub>h</sub> in the nine bytes at `+5A48`<sub>h</sub> (stride 2, `00327200`) equals `memberSlot` |
| 12 | action id at most `21E`<sub>h</sub> and phase at least 9 |
| 13 | action id at most `21E`<sub>h</sub> and phase at least 3 |
| 14 | the unit has flag bit 4, its stats record is null or of a kind other than 0, and the spawn record has flag bit 6 or the status words carry bit 24 (`00329337`-`0032937B`) |
| 15 | idle: no action context `+708`<sub>h</sub>, action id `FFFF`<sub>h</sub>, or phase 0 |
| 16 | `003879C0(stats)`: for a kind-1 owner, bit 7 of byte `+12`<sub>h</sub> of the class row `[unit + E68h]` |
| 17 | `0030C2C0(unit)`: unit flag bit 52 (dword `+4` bit 20), after `002FEAD0` when `003278C0()` is 0 |

Block offsets are offsets into the battle-state block `[02EBF190]`
([its field map](../Party/party-data.md)); `+5AA4`<sub>h</sub> is
the party leader byte and `+5AD5`<sub>h</sub> the special-presentation actor there.

### HP, MP and the countdowns

- `+20`<sub>h</sub> is HP (`+48`<sub>h</sub>). `+24`<sub>h</sub> is the effective maximum: `max(HP, 1)` while status bit 16 is set
  in either status word, else `+24`<sub>h</sub>. `+28`<sub>h</sub> is the cap: the same under status bit 16, else
  `+24`<sub>h</sub> doubled when status bit 28 is set.
- `+2C`<sub>h</sub> is MP (`i16 +4Ch`), `+30`<sub>h</sub> the capacity (`+28`<sub>h</sub>), `+34`<sub>h</sub> the capacity when bit 7 of
  both layer bytes `+6C`<sub>h</sub> and `+7C`<sub>h</sub> is clear and 0 otherwise, `+38`<sub>h</sub> the `i16` at `+06`<sub>h</sub>.
- `+66h + s` for `s` from 0 to 31 is the low byte of the duration dword `+BCh + 4 * s` minus 1
  when status `s` is present and `s` is 2 or 6, and `FE`<sub>h</sub> otherwise (`00329500`-`00329539`).

### The name and the party row

For a kind-0 record the party row is `[02EBF130]`'s section `+0C`<sub>h</sub> at stride `+8` times the type;
its word `+30`<sub>h</sub> is split into a bank index (high 5 bits) and an entry (low 11 bits) through the text
banks at `[02EBF170]`, and `002B58B0(block, 0)` gives the pointer stored at `+10`<sub>h</sub>. `0030A310(row, i)`
returns row byte `+4 + i` for `i` below 3, which fill the words `+B4`<sub>h</sub>, `+B6`<sub>h</sub> and `+B8`<sub>h</sub>. When a
unit owns the record the name pointer is replaced by the empty string at `01CEB638`.

### Experience, LP and equipment

With `full` set: `+BA`<sub>h</sub> is the level (`+1C2`<sub>h</sub>), `+90`<sub>h</sub> the experience (`+18C`<sub>h</sub>), `+B0`<sub>h</sub> the LP
(`+190`<sub>h</sub>), `+BB`<sub>h</sub> the number of licence bits set among bits 0-17 of the licence bytes at `+194`<sub>h</sub>
(`00324020`), and `+98`<sub>h</sub>-`+AC`<sub>h</sub> the six words `+50`<sub>h</sub>-`+5A`<sub>h</sub> each shifted left by 16. `+94`<sub>h</sub> is
the points to the next level:

```python
curve(level) = sum for k = 2 .. level + 1 of trunc(float(k * k * k) * 0.4 + float(12 * k * k))   (002F8F20; 0 for level 0, -1 for level 99 and above)
+0x94 = curve(level) - experience
```

### The unit-side fields

While a unit owns the record:

- `+88`<sub>h</sub> is the spawn record's `+12`<sub>h</sub> (`[unit + 6A0h]`), `+04`<sub>h</sub> the unit's handle (`+08`<sub>h</sub>),
  `+18`<sub>h</sub> and `+1C`<sub>h</sub> the unit's `+64`<sub>h</sub> and `+68`<sub>h</sub>;
- `+64`<sub>h</sub> is the word `+52`<sub>h</sub> of the class row `[unit + E68h]` for a kind-1 record whose actor class
  nibble (`00263C20`, byte `+0E`<sub>h</sub> of the actor) is not 3, else `FFFF`<sub>h</sub>;
- while the unit is acting (context `+708`<sub>h</sub> set, id at most `21E`<sub>h</sub>, phase not 0): `+3C`<sub>h</sub> and
  `+40`<sub>h</sub> are the unit's `+768`<sub>h</sub> and `+76C`<sub>h</sub>, `+08`<sub>h</sub> the focus `+710`<sub>h</sub>, and `+5C`<sub>h</sub> the action
  id, or `00387090(stats)` once the phase is 9 or more; otherwise they are 0, 0, 0 and `FFFF`<sub>h</sub>;
- `+5E`<sub>h</sub> is the unit's `+BA0`<sub>h</sub> while unit flag bit 14 is set, else `FFFF`<sub>h</sub>.

## Layouts

Struct PartyMemberStatusRecord size=`C0`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | flags | the flag word above |
| `04`<sub>h</sub> | `u32` | actorHandle | the roster member's handle, or the owning unit's +`08`<sub>h</sub> |
| `08`<sub>h</sub> | `u32` | focusHandle | the unit's +`710`<sub>h</sub> while acting |
| `10`<sub>h</sub> | `u8*` | name | the party row's name text; the empty string when a unit owns the record |
| `18`<sub>h</sub> | `u32` | unitField64 | unit +`64`<sub>h</sub> |
| `1C`<sub>h</sub> | `u32` | unitField68 | unit +`68`<sub>h</sub> |
| `20`<sub>h</sub> | `i32` | hp | stats +`48`<sub>h</sub> |
| `24`<sub>h</sub> | `i32` | hpMaxEffective | stats +`24`<sub>h</sub>, or max(hp, 1) under status bit 16 |
| `28`<sub>h</sub> | `i32` | hpCap | hpMaxEffective doubled under status bit 28 |
| `2C`<sub>h</sub> | `i32` | mp | stats +`4C`<sub>h</sub> |
| `30`<sub>h</sub> | `i32` | mpCapacity | stats +`28`<sub>h</sub> |
| `34`<sub>h</sub> | `i32` | mpCapacityShown mpCapacity, or 0 when layer bytes `+6C`<sub>h</sub> or `+7C`<sub>h</sub> carry bit 7 |  |
| `38`<sub>h</sub> | `i32` | secondary | stats +`06`<sub>h</sub> |
| `3C`<sub>h</sub> | `u32` | actionField768 | unit +`768`<sub>h</sub> while acting |
| `40`<sub>h</sub> | `u32` | actionField76C | unit +`76C`<sub>h</sub> while acting |
| `44`<sub>h</sub> | `u32` | statusPresence | stats +`64`<sub>h</sub> \| +`3C`<sub>h</sub> |
| `48`<sub>h</sub> | `u32` | statusWord | stats +`3C`<sub>h</sub> |
| `4C`<sub>h</sub> | `u8[16]` | mergedLayers | stats +`68`<sub>h</sub> OR +`78`<sub>h</sub>, byte-wise |
| `5C`<sub>h</sub> | `u16` | actionId | the unit's +`714`<sub>h</sub>, or `00387090`(stats) from phase 9 |
| `5E`<sub>h</sub> | `u16` | issuedCommand | unit +`BA0`<sub>h</sub> while unit flag bit 14 |
| `60`<sub>h</sub> | `u16` | type | stats +`04`<sub>h</sub> |
| `62`<sub>h</sub> | `u16` | kind | stats +`05`<sub>h</sub> |
| `64`<sub>h</sub> | `u16` | classRowWord52 | [unit + `E68`<sub>h</sub>] +`52`<sub>h</sub> for a kind-1 record |
| `66`<sub>h</sub> | `u8[32]` | countdown | low byte of duration dword +`BC`<sub>h</sub> + 4s, minus 1, for present statuses 2 and 6, else `FE`<sub>h</sub> |
| `86`<sub>h</sub> | `u8` | charges | stats +`4E`<sub>h</sub> |
| `87`<sub>h</sub> | `u8` | bars | stats +`37`<sub>h</sub> |
| `88`<sub>h</sub> | `u8` | spawnCounter | spawn record +`12`<sub>h</sub> |
| `89`<sub>h</sub> | `u8[5]` | affinity | stats +`40`<sub>h</sub> .. +`44`<sub>h</sub> |
| `90`<sub>h</sub> | `i32` | experience | stats +`18C`<sub>h</sub> (full) |
| `94`<sub>h</sub> | `i32` | toNextLevel | curve(level) - experience (full) |
| `98`<sub>h</sub> | `u32[6]` | equipment | stats +`50`<sub>h</sub> .. +`5A`<sub>h</sub>, each << 16 (full) |
| `B0`<sub>h</sub> | `i32` | lp | stats +`190`<sub>h</sub> (full) |
| `B4`<sub>h</sub> | `u16[3]` | partyRowBytes | party row +4 .. +6 |
| `BA`<sub>h</sub> | `u8` | level | stats +`1C2`<sub>h</sub> (full) |
| `BB`<sub>h</sub> | `u8` | licenceCount | set bits among licence bits 0-17 (full) |

The sixth equipment word at `+AC`<sub>h</sub> is the stats record's `+5A`<sub>h</sub>, not a sixth slot: see the
[equipment slots page](../Items-Equipment-Shops-And-Licenses/equipment.md).

## Operations

Which screen reads which field of its copy:

| Reader | Fields |
|---|---|
| the input arbiter `00253C70`, `00254560` | type `+60`<sub>h</sub> and flag bit 1, counting members |
| `00272E10`, `00273880` | the actor handle `+04`<sub>h</sub> |
| `00272E70` | the type `+60`<sub>h</sub> |
| `00283270` | the type `+60`<sub>h</sub> (compared with 6) and flag bit 1 |
| `00273270` | `+AC`<sub>h</sub> shifted right by 16, the stashed slot-0 item id, compared by `0027C3D0` with the selected entry |
| `0035BC50` | type, handle and flag bits 1, 2 and 6, written back into its own table |
| `002BFD20` | layer byte `+51`<sub>h</sub> bit 1, `+44`<sub>h</sub>, affinity `+89`<sub>h</sub>, level `+BA`<sub>h</sub> and flag bit 16 through its widget, which it also hands to `002C0400` |

## Modding notes

- The screens never read the stats record directly; a displayed value changed without changing its
  source field is undone on the next build.
- "Out of range" on the HUD is a circle of 20 units (`400.0` squared) around the focused character.
- The countdown bytes show only statuses 2 and 6; every other status displays as `FE`<sub>h</sub>.
- A KO'd member is not reported as KO'd in a town: the town flag of the current area masks the
  terminal statuses in flag bit 0.

## Related

- [The battle stats record field map](../Damage-And-Battle-Formulas/unit-stats-fields.md): the source record.
- [The battle unit field map](battle-unit-fields.md): the unit fields read.
- [The battle-state block field map](../Party/party-data.md): the slot words and the leader byte.
- [Area flags and navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md): the town flag.
- [EXP, LP and level ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md): the experience curve.
