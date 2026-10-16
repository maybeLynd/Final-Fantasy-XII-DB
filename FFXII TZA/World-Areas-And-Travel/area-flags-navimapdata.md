---
title: "Area flags: the navimapdata.bin record for every area, the town flag, the KO, Stone and X-Zone override and the other bits"
kind: "system"
category: "World, areas and travel"
addresses: "00377C20, 00377480, 00377A40, 00377BA0, 003779F0, 00377700, 00377C70, 00378540"
---

## What the player sees

Three things take a character out of a fight for good: being KO'd, being turned to Stone, and being
sent to X-Zone. A character in one of those states is treated as absent: no commands, no actions, no
EXP or LP, no attention from monsters.

Inside a town that rule is switched off. In Rabanastre's streets and shops, the Clan Hall, the Sandsea,
every Aerodrome, the Strahl's Sky Saloon, Jahara, Eruyt Village, Mt Bur-Omisace, Balfonheim and the
other safe areas, a fallen party member still walks, talks and shops with the party instead of being
frozen out. The same character in the same condition behaves differently one zone over.

The town flag does more than that. It ends the kill chain when you enter, it changes who the game
controls when a scene hands the party back, and the Map screen uses the same per-area record to know
which page an area belongs to and whether to print its name. A few areas also change how MP comes
back: in the Pharos, the Great Crystal, the Necrohol of Nabudis and similar places MP recovers a third
as fast while walking and three times as much from damage.

None of this is decided by the battle system. It is one three-byte record per area in a shipped data
file, and this page is that record.

## How it works

### The table and how it is loaded

The area table is the shipped file `navimapdata.bin`: a 4-byte tag `NAV` `02`<sub>h</sub>, a 32-bit record count,
and one 3-byte record per area id. The shipped file has 1,154 records and is 3,470 bytes, exactly
8 + 3 × 1,154. Three byte-identical copies ship, in the `ch`, `cn` and `in` image folders.

The World/Area/Field start-up routine `00378540` requests it as resource (9, 8) under the key
`"MapInfo"` (string at `00D11148`) through the resource loader `0032E620`, with `00378B80` as the
delivery callback. That callback is ten bytes: it zero-extends the delivered 32-bit address and stores
it at `02ADD100` (`00378B82`). `00378540` clears `02ADD100` first, so the cell is null until the file
arrives. No other function writes `02ADD100` (its references are the eight reads in the accessors
below, the two writes in `00378540` and `00378B80`, and two data references in `00379D60`).

### The record and its seven readers

Every record is a little-endian 16-bit word at `+0` and `+1` plus a third byte at `+2`. Seven short
functions read it, and each takes one part:

| Reader | Part | Area id from | Returns |
|---|---|---|---|
| `00377C20` (thunk `00313F60`) | word bit 15, the town flag | the current area (`003148F0`) | 0 or 1 |
| `00377480` | word bit 15 | its argument | 0 or 1 |
| `00377A40` | word bit 14, the area-name flag | its argument | 0 or 1 |
| `00377BA0` (thunk `00320160`) | word bits 12-13, the MP regime | the current area, or the save override | 0 to 3 |
| `003779F0` | word bits 0-11, the Map entry | its argument | 0 to 4,094, or -1 for none |
| `00377700` | third byte bit 0, the hold flag | the current area, with a save veto | 0 or 1 |
| `00377C70` | third byte bits 4-6, the default leader | the current area | 0 to 7 |

All seven share one prologue: load the table pointer, return the default when it is null, compare the
area id unsigned against the count at `+4` and return the default when it is not below it, then read
bytes `+8` and `+9` (or `+10`) of `table + 3 × id`. `00377C20` is the model: `00377C29` loads the
pointer, `00377C33` tests it, `00377C35`-`00377C39` bounds the id, `00377C42`-`00377C53` assembles
the word from two byte loads, `00377C55` shifts by 15.

### The current area id

The implicit readers take the area id from `003148F0`, which returns the save-data field
`+1044`<sub>h</sub> of the persistent payload (`002EF2B0` returns the payload base, the save image's `+200`<sub>h</sub>).
A negative value is clamped to 0 (`00314903 cmovs`), so a negative saved id reads record 0 rather
than nothing. During a zone change this field already holds the area being entered, so every implicit
reader answers for the destination as soon as the transition is staged.

### The town flag and the out-of-play rule

Bit 15 is the town flag. The combat layer treats a unit as out of play when either of its two status
words `+3C`<sub>h</sub> or `+64`<sub>h</sub> has a bit in the mask `80000003`<sub>h</sub>, which is status 0 KO, status 1 Stone and
status 31 X-Zone, the three statuses that permanently leave play. The waiver is always the same shape:

```c
if (((stats[+0x3C] | stats[+0x64]) & 0x80000003) != 0 && townFlag() == 0)
    refuse;   /* the unit is out of play unless the area is a town */
```

The pairing is the mechanism. A sweep of the code section finds 173 instructions carrying the
immediate `80000003`<sub>h</sub>; 117 of them sit within 96 bytes of a call to `00377C20` or its thunk
`00313F60`. The flag is read by 65 functions directly and by 47 more through the thunk, two of them
both ways (`00253C70`, `003266C0`), so 110 functions across the combat, AI, status, movement, actor,
script, menu and reward systems consult one authored bit.

Readers worth naming:

- The defeat-reward routine `00312280` keeps a recipient who is out of play only when the flag is set
  (`00312382`), and the EXP divisor and recipient tests in `002F8BB0` use the same mask.
- The kill chain is reset on entering an area with the flag set (`003183D0`, see the kill chain page).
- The party-control level `0030D9A0` returns level 3 when the flag is set (`0030D9CF`-`0030D9D8`),
  before the combat and menu levels; see the battle runtime mode page.
- The status write `0030E360` lets a unit that already carries a terminal status take another one
  only when the flag is set (`0030E4B6`).
- Explicit-id reads go through `00377480`; its one caller is the actor definition binder `0026C8C0`
  (`0026CA30`).

### The MP regime and its save override

Bits 12-13 select the area's MP regime. `00377BA0` first asks `00314AA0`, which returns bit 7 of
payload byte `+1062`<sub>h</sub>; when it is set the function tail-jumps to `00314AC0` (`00377BB1`), which
returns bits 4-5 of payload byte `+1063`<sub>h</sub>, and the table is never read. Otherwise it reads the word
and returns `(word >> 12) & 3`. The override replaces the authored value, it does not merge with it.

Four consumers read the regime, all through the thunk `00320160`:

| Consumer | Value 2 or 3 | Where |
|---|---|---|
| `002F9400`, MP recovered per step while moving | divided by 3.0 | `002F956A`-`002F957E` (`divss` by `008F311C`) |
| `002F91A0`, MP the target gains from HP damage | tripled | `002F9220`-`002F9234` (`lea ebx, [rbx+rbx*2]`) |
| `002F9240`, MP the caster gains from HP damage | tripled | `002F93CC`-`002F93D6` |
| `00301AD0`, gambit target selector | compared with the condition's operand | `00303043`-`0030304D` (`setge`), `00303052` |

So values 0 and 1 are one regime and values 2 and 3 are the other for combat; only the gambit
selector can tell 1 from 0 or 3 from 2.

### The Map entry

Bits 0-11 are the area's entry in the in-game Map. `003779F0` masks the word with `FFF`<sub>h</sub> and returns
-1 when the result is `FFF`<sub>h</sub> (`00377A23`-`00377A32`), so a missing table and an authored "none" are
the same answer. Nine functions call it: the Map screen builders `003C5E50`, `003C17E0`, `003C60F0`,
`003C8670` and `00576A50`, the per-map record helpers `002550E0`, `002551B0` and `00255200`, and the
handbook check `003160C0`, which walks the handbook's map list at `[022C2550] + 8` and treats the
current area's entry as already seen (`003160FA`).

### The area-name flag

Bit 14 is read by `00377A40` for an explicit id. Its five callers are menu and HUD functions
(`003F92B0`, `003F9720`, `003C2320`, `003BF9A0`, `003C1180`). `003F92B0` shows the use: when the
current area's bit is set (`003F92DA`) it prints the area's name from the name table through
`00377870` after the location text; otherwise it prints text `3EC`<sub>h</sub>.

The same name table (`MapName`, `planmapname.bin`, at `02ADD0F8`) also names the regions.
`00377B60(id)` returns the area name at entry `id` of the offset table `+10`<sub>h</sub> while `id` is below the
area count `+04`<sub>h</sub>. `003778B0(field)` returns the name of the field's region, the persistence group
`00264F90(field)`: entry `[+04h] + group` of the same offset table, while the group is below the
region count `+08`<sub>h</sub>; an empty entry or a missing table gives the empty string `01CEB638`. Its callers
are the menu location line `0029C530` and the save-file entry `0057FB00`.

### The hold flag and its save veto

Bit 0 of the third byte is read inverted by `00377700`: it returns 1 only when the bit is clear and
`00314A60` reports bit 0 of payload byte `+1062`<sub>h</sub> clear (`0037772D not`, `0037772F test al, 1`,
`00377733 call`, `0037773C mov eax, 1`). A missing table yields a zero byte (`00377728`), so the
missing-table answer is 1, the permissive value. The save bit can only force the answer to 0.

Six actor-system functions call it (`00263230`, `00268D10`, `0026A1D0`, `0026B980`, `0026C3E0`,
`0026C5D0`). Two of them store the inverse into the party-hold byte `02099DE7`: `0026A1D0` at
`0026A20B` and `00268D10` at `00268E29` (`setz bpl` on the call's result). That byte is the parameter
of the party hold request the time-stop registry receives; see the time stop page.

### The default leader

Bits 4-6 of the third byte are read by `00377C70` (`00377C99 shr eax, 4`, `00377C9C and eax, 7`). Its
callers are `00326500`, `003266C0` and `0031C000`. `00326500` picks the party member the game follows
when control returns: the saved leader at `[02EBF190] + 5AA4h` at control levels 0 and 1, id `1A`<sub>h</sub>
at level 2, and this field at level 3, the town level (`0030D9A0`). Every shipped record has these
bits at 0 (census below), so in a town the lookup fails and the function falls back to the first of
the four active slots with a unit, then to `00263750(0)`.

### What a missing table returns

Every reader runs its normal shift and mask on a default record of `0FFF`<sub>h</sub> for the word and 0 for the
third byte. The defaults do not agree on what they mean:

| Reader | Default | Meaning |
|---|---|---|
| `00377C20`, `00377480` | 0 | not a town |
| `00377A40` | 0 | no area name |
| `00377BA0` | 0 | normal MP regime |
| `003779F0` | -1 | no Map entry |
| `00377700` | 1 unless the save veto is set | hold permitted |
| `00377C70` | 0 | leader id 0 |

## Layouts

`AreaTable` (`8`<sub>h</sub> bytes, offsets from the start of the table):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | tag | 'NAV' `02`<sub>h</sub> (`0256414E`<sub>h</sub>); the seven readers never test it |
| `04`<sub>h</sub> | `u32` | count | record count, 1,154 shipped; every reader bounds the id against it unsigned (`00377C35`) |

`AreaRecord` (`3`<sub>h</sub> bytes, offsets from the start of the table+8+3*id):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | flags | bits 0-11 Map entry (`003779F0`), bits 12-13 MP regime (`00377BA0`), bit 14 area name (`00377A40`), bit 15 town (`00377C20`, `00377480`) |
| `02`<sub>h</sub> | `u8` | options | bit 0 hold flag (`00377700`, read inverted), bits 1-3 authored and read by nothing (scope: the eight readers of `02ADD100` above), bits 4-6 default leader (`00377C70`), bit 7 never set and never read |

## Shipped data

Census of the 1,154 records in `navimapdata.bin`:

| Field | Shipped values |
|---|---|
| town flag (bit 15) | set on 193 areas |
| area name (bit 14) | set on 155 areas, 154 of them towns |
| MP regime (bits 12-13) | 0 on 945, 1 on 36, 2 on 69, 3 on 104 |
| Map entry (bits 0-11) | `FFF`<sub>h</sub> (none) on 556, 0 on 200, 370 distinct values, highest 368 |
| hold flag (byte 2 bit 0) | set on 170 areas, every one of them a town; the 23 towns without it are ids 0-22 |
| byte 2 bits 1-3 | `02`<sub>h</sub>, `04`<sub>h</sub> and `08`<sub>h</sub> in eight combinations across 638 areas |
| byte 2 bits 4-7 | 0 on every record |

The towns, with the names the `us` `planmapname.bin` gives through the name indexer `00377B60`
(offset table at `+10`<sub>h</sub>, 1,312 entries; ids with no name entry are omitted):

| Area ids | Towns |
|---|---|
| 0-22 | no name entries |
| 48, 50, 51 | Stockade, rbn_z01, Oubliette |
| 124-130 | Observation Parlour, Sky Saloon, Air Deck, South Bank Village, North Bank Village |
| 233, 243 | Outpost, Nomad Village |
| 289-310 | North End, Muthru Bazaar, East End, Southern Plaza, Amal's Weaponry, Panamis's Protectives, Migelo's Sundries, Yugri's Magicks, Batahn's Technicks, Yamoora's Gambits, Samalzalam Manor, The Clan Hall, The Sandsea, Eastgate, Southgate, Westgate |
| 312, 488 | East Waterway Control, Hunters' Camp |
| 567-575 | Cellar Stores, Cellars, Lower Halls, Secret Passage, Treasure Room No. 8, The Garden Stairs |
| 631-643 | Jajim Bazaar, West Ward, Grand Arcade, Highgarden Terrace, Molberry, Trant, Charlotte's Magickery, Bulward's Technicks |
| 666 | Womb of the Sun-cryst |
| 701-708 | North Sprawl, South Sprawl, Dalan's House, Residence |
| 736-770 | Hall of the Light, Temple Grounds, Temple Approach, Sand-strewn Pass, Nilbasse, Rienna, Vint's Armaments, Granch's Requisites, Lebleu's Gambits, Banks of the Sogoht, Lull of the Land, The Elderknoll, Tsenoble, Alley of Muted Sighs, Alley of Low Whispers, Fane of the Path, The Spiritwood, Road of Verdant Praise, vic_a04 |
| 788-837 | Aerodrome (five areas), Travica Way, Cloudborne Row, Miners' End, Lhusu Square, Khus Skygrounds, Kaff Terrace, Targe's Arms, Rithil's Protectives, Mait's Magicks, Clio's Technicks, Bashketi's Gambits, The Staras Residence, The Cloudborne, Sea Breeze Lane, Gallerina Marketplace, Quayside Court, Saccio Lane, Chivany Breakwater, Canal Lane, Beruny's Armaments, Odo's Technicks, Port Villa (two areas), The Whitecap |
| 854-871 | dor_z01, Dalan's Marker, glf_z01, rbn_x01, byu_z01, byu_y01, alc_z01 to alc_z04, Bridge |
| 910-924 | rbn_y01, byu_w01, byu_x01, Siti Bhrusuna, var_z01, bhm_y01, bhm_z01 |
| 1151 | Babbling Vale |

Every named town is a settlement, a shop or house interior, a plaza, an aerodrome, an airship interior
or a story room; the code-shaped names (`alc_z01`, `rbn_x01`, `var_z01` and the like) are the scene
variants of those areas. Areas with MP regime 2 or 3 include Terminus No. 7, the Necrohol of Nabudis
(Vale of Lingering Sorrow, Echoes of the Past, The Slumbermead), the Great Crystal (A Vikaari Bhrum,
Sthaana Pisces, Crystal Core), the Pharos (Hall of Effulgent Light, Cloister of Solace, The Crucible),
the Henne Mines (Site 7) and Giruvegan (Hall of Worth, Throne of Veiled Gods).

The name table's header, measured in all nine language copies of `planmapname.bin`:

| Fact | Value |
|---|---|
| magic `+00`<sub>h</sub> | `PLMN` |
| area entries `+04`<sub>h</sub> | 1,312 (`520`<sub>h</sub>) |
| region entries `+08`<sub>h</sub> | 59 (`3B`<sub>h</sub>) |
| all entries `+0C`<sub>h</sub> | 1,371 (`55B`<sub>h</sub>) |
| `us` regions | region 0 has no entry; 41 and 44 share the entry `NOT USED`; 3 is Barheim Passage, 37 Nalbina Town |

## Operations

| Function | Signature | Reads | Returns |
|---|---|---|---|
| `00378540` | `()` | resource (9, 8) `"MapInfo"` | installs the table pointer through `00378B80` into `02ADD100` |
| `00377C20` | `()` | word bit 15 of the current area | 0/1; 65 callers plus 47 through `00313F60` |
| `00377480` | `(areaId)` | word bit 15 | 0/1; caller `0026C8C0` |
| `00377A40` | `(areaId)` | word bit 14 | 0/1; five menu callers |
| `00377BA0` | `()` | payload `+1062`<sub>h</sub> bit 7, then `+1063`<sub>h</sub> bits 4-5 or word bits 12-13 | 0-3; four callers through `00320160` |
| `003779F0` | `(areaId)` | word bits 0-11 | 0-4,094 or -1; nine callers |
| `00377700` | `()` | third byte bit 0, payload `+1062`<sub>h</sub> bit 0 | 1 when both are clear, else 0; six callers |
| `00377C70` | `()` | third byte bits 4-6 | 0-7; callers `00326500`, `003266C0`, `0031C000` |
| `003148F0` | `()` | payload `+1044`<sub>h</sub> | the current or pending area id, negatives clamped to 0 |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `02ADD100` | `void*` | the loaded table | `00378540` (null), `00378B80` (delivery) |
| payload `+1044`<sub>h</sub> | `i32` | current or pending area id | the zone change (see the zone changes page) |
| payload `+1062`<sub>h</sub> bit 0 | bit | vetoes the hold flag | the zone change record's flag byte |
| payload `+1062`<sub>h</sub> bit 7 | bit | enables the MP regime override | the zone change record's flag byte |
| payload `+1063`<sub>h</sub> bits 4-5 | 2 bits | the overriding MP regime | the zone change record |
| `02099DE7` | `u8` | the party hold parameter, `00377700() == 0` | `0026A20B`, `00268E29` |

## Modding notes

- Setting bit 15 on an area makes it a town for every system at once: fallen party members stay in
  play, the chain resets on entry, control level 3 applies and the saved leader is ignored. Clearing it
  on a shop interior re-arms the out-of-play rule there.
- Bits 12-13 are the only per-area MP control: 2 or 3 slows walking recovery to a third and triples
  the MP gained from damage. The save override at payload `+1062`<sub>h</sub> bit 7 / `+1063`<sub>h</sub> bits 4-5 can
  impose a regime on any area without touching the file.
- Bits 4-6 of the third byte are a working but unused feature: a non-zero value names the party member
  the game follows when control returns inside that town.
- Bits 1-3 of the third byte are authored on 638 areas and read by no function; changing them does
  nothing.
- Area names and the Map pages live in `planmapname.bin`, not here; the record only carries the Map
  entry id and the name flag.

## Related

- [Kill rewards: what an enemy's death triggers, when it gives nothing, and the order of chain, EXP, LP, gil, loot and counters](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)
- [Kill chain: chain count, chain level, the chain coin and resets](../Rewards-EXP-Gil-And-Loot/kill-chain.md)
- [Battle runtime mode ladder](../Engine-Core/party-control-modes.md)
- [The time-stop registry](../Engine-Core/time-stop-and-freeze.md)
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md)
- [The save payload field map](../Saving-Loading-And-Settings/save-data-fields.md)
