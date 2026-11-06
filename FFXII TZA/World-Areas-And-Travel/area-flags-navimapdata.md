---
title: "Area flags: the navimapdata.bin record for every area, the town flag, the KO, Stone and X-Zone override and the other bits"
kind: "system"
category: "World, areas and travel"
addresses: "0x00377C20, 0x00377480, 0x00377A40, 0x00377BA0, 0x003779F0, 0x00377700, 0x00377C70, 0x00378540"
---

## What the player sees

Three things take a character out of a fight until they are cured: being KO'd, being turned to Stone,
and being sent to X-Zone. A character in one of those states is treated as absent: no commands, no
actions, no EXP or LP, no attention from monsters.

Inside a town that rule is switched off. In Rabanastre's streets and shops, the Clan Hall, the Sandsea,
every Aerodrome, the Strahl's Sky Saloon, Jahara, Eruyt Village, Mt Bur-Omisace, Balfonheim and the
other safe areas, a fallen party member still walks, talks and shops with the party instead of being
frozen out. The same character in the same condition behaves differently one zone over.

The town flag does more than that. It ends the kill chain when you enter, it changes who the game
controls when a scene hands the party back, and the Map screen uses the same per-area record to know
which page an area belongs to and whether to print its name. A few areas also change how MP comes
back: in the Pharos, the Great Crystal, the Necrohol of Nabudis and similar places MP recovers three
times as fast while walking and three times as much from damage.

None of this is decided by the battle system. It is one three-byte record per area in a shipped data
file, and this page is that record.

## How it works

### The table and how it is loaded

The area table is the shipped file `navimapdata.bin`: a 4-byte tag `NAV` 0x02, a 32-bit record count,
and one 3-byte record per [field id](zone-changes-and-mapjump.md#what-names-a-map), the number that names a map. The shipped file has 1,154 records and is 3,470 bytes, exactly
8 + 3 × 1,154. Three byte-identical copies ship, in the `ch`, `cn` and `in` image folders.

The World/Area/Field start-up routine `0x00378540` requests it as resource (9, 8) under the key
`"MapInfo"` (string at `0x00D11148`) through the resource loader `0x0032E620`, with `0x00378B80` as the
delivery callback. That callback is ten bytes: it zero-extends the delivered 32-bit address and stores
it at `0x02ADD100` (`0x00378B82`). `0x00378540` clears `0x02ADD100` first, so the cell is null until the file
arrives. No other function writes `0x02ADD100` (its references are the seven reads in the accessors
below, one in each, and the two writes in `0x00378540` and `0x00378B80`).

`0x00378540` sizes the file with `0x0032E400` (`0x003785FA`) and allocates that many bytes in arena 3
(`0x0036C1D0(3, 5)` at `0x0037860D`, `0x0036A190` at `0x00378614`; [resource
arena](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md)), which boot builds once
(`0x0022A2CB`). Its one caller is the loader reset `0x00377CC0` (`0x00377D8C`), which the start-up
initialiser `0x00266D10` runs once (`0x00267146`). No instruction passes the value of `0x02ADD100` to a free,
so the table stays loaded for the run.

### The record and its seven readers

Every record is a little-endian 16-bit word at `+0` and `+1` plus a third byte at `+2`. Seven short
functions read it, and each takes one part:

| Reader | Part | Field id from | Returns |
|---|---|---|---|
| `0x00377C20` (thunk `0x00313F60`) | word bit `0x8000`, the town flag | the current area (`0x003148F0`) | 0 or 1 |
| `0x00377480` | word bit `0x8000` | its argument | 0 or 1 |
| `0x00377A40` | word bit `0x4000`, the area-name flag | its argument | 0 or 1 |
| `0x00377BA0` (thunk `0x00320160`) | word bits `0x3000`, the MP regime | the current area, or the save override | 0 to 3 |
| `0x003779F0` | word bits `0xFFF`, the Map entry | its argument | 0 to 4,094, or -1 for no entry |
| `0x00377700` | third byte bit `0x1`, the hold flag | the current area, with a save veto | 0 or 1 |
| `0x00377C70` | third byte bits `0x70`, the default leader | the current area | 0 to 7 |

All seven share one prologue: load the table pointer, return the default when it is null, compare the
field id unsigned against the count at `+4` and return the default when it is not below it, then read
bytes `+8` and `+9` (or `+10`) of `table + 3 × id`. `0x00377C20` is the model: `0x00377C29` loads the
pointer, `0x00377C33` tests it, `0x00377C35`-`0x00377C39` bounds the id, `0x00377C42`-`0x00377C53` assembles
the word from two byte loads, `0x00377C55` shifts by 15.

These seven are the only code that reads the table. Its address is held only in `0x02ADD100`: no instruction or data
word holds it as an absolute or image-relative value, the key `"MapInfo"` has its one reference in `0x00378540`, and
each reader returns only its own bits. So no code reads third-byte bits under mask `0xE` or bit `0x80` as a field.

### The current field id

The implicit readers take the field id from `0x003148F0`, which returns the save-data field
`+0x1044` of the persistent payload (`0x002EF2B0` returns the payload base, the save image's `+0x200`).
A negative value is clamped to 0 (`0x00314903 cmovs`), so a negative saved id reads record 0 rather
than nothing. During a zone change this field already holds the area being entered, so every implicit
reader answers for the destination as soon as the transition is staged.

### The town flag and the out-of-play rule

Bit `0x8000` is the town flag. The combat layer treats a unit as out of play when either of its two status
words `+0x3C` or `+0x64` has a bit in the mask `0x80000003`, which is status 0 KO, status 1 Stone and
status 31 X-Zone, the three statuses that leave play until they are removed. The waiver is always the same shape:

```c
if (((stats[+0x3C] | stats[+0x64]) & 0x80000003) != 0 && townFlag() == 0)
    refuse;   /* the unit is out of play unless the area is a town */
```

The pairing is the mechanism. A sweep of the code section finds 173 instructions carrying the
immediate `0x80000003`; 117 of them sit within 96 bytes of a call to `0x00377C20` or its thunk
`0x00313F60`. The flag is read by 65 functions directly and by 47 more through the thunk, two of them
both ways (`0x00253C70`, `0x003266C0`), so 110 functions across the combat, AI, status, movement, actor,
script, menu and reward systems consult one authored bit.

Readers worth naming:

- The defeat-reward routine `0x00312280` keeps a recipient who is out of play only when the flag is set
  (`0x00312382`), and the EXP divisor and recipient tests in `0x002F8BB0` use the same mask.
- The kill chain is reset on entering an area with the flag set (`0x003183D0`, see the kill chain page).
- The party-control level `0x0030D9A0` returns level 3 when the flag is set (`0x0030D9CF`-`0x0030D9D8`),
  before the combat and menu levels; see the battle runtime mode page.
- The status write `0x0030E360` lets a unit that already carries a terminal status take another one
  only when the flag is set (`0x0030E4B6`).
- Explicit-id reads go through `0x00377480`; its one caller is the actor definition binder `0x0026C8C0`
  (`0x0026CA30`).

### The MP regime and its save override

Bits `0x3000` select the area's MP regime. `0x00377BA0` first asks `0x00314AA0`, which returns bit `0x80` of
payload byte `+0x1062` (`0x00314AB0 shr eax, 7`); when it is set the function tail-jumps to `0x00314AC0`
(`0x00377BB1`), which returns the bits under mask `0x30` of payload byte `+0x1063` shifted down, `(byte >> 4) & 3`
(`0x00314AD0`-`0x00314AD3`), and the table is never read.

Otherwise it takes the current area from `0x003148F0`
(`0x00377BB6`), reads that record's word and returns `(word >> 12) & 3` (`0x00377BE7`-`0x00377BEA`), or 0 when the
table is missing or the id is not below the count (`0x00377BF4`-`0x00377BFC`). The override replaces the authored
value, it does not merge with it.

Four consumers read the regime, all through the thunk `0x00320160`:

| Consumer | Value 2 or 3 | Where |
|---|---|---|
| `0x002F9400`, MP recovered per step while moving | the distance per point divided by 3.0, so recovery is three times as fast | `0x002F956A`-`0x002F957E` (`divss` by `0x008F311C`) |
| `0x002F91A0`, MP the target gains from HP damage | tripled | `0x002F9220`-`0x002F9234` (`lea ebx, [rbx+rbx*2]`) |
| `0x002F9240`, MP the caster gains from HP damage | tripled | `0x002F93CC`-`0x002F93D6` |
| `0x00301AD0`, gambit target selector | compared with the condition's operand | `0x00303043`-`0x0030304D` (`setge`), `0x00303052` |

So values 0 and 1 are one regime and values 2 and 3 are the other for combat; only the gambit
selector can tell 1 from 0 or 3 from 2.

### The Map entry

Bits `0xFFF` are the area's entry in the in-game Map. `0x003779F0` masks the word with `0xFFF` and returns
-1 when the result is `0xFFF` (`0x00377A23`-`0x00377A32`), so a missing table and an authored `0xFFF` are
the same answer. Nine functions call it: the Map screen builders `0x003C5E50`, `0x003C17E0`, `0x003C60F0`,
`0x003C8670` and `0x00576A50`, the per-map record helpers `0x002550E0`, `0x002551B0` and `0x00255200`, and the
handbook check `0x003160C0`, which walks the handbook's map list at `[0x022C2550] + 8` and treats the
current area's entry as already seen (`0x003160FA`).

### The area-name flag

Bit `0x4000` is read by `0x00377A40` for an explicit id. Its five callers are menu and HUD functions
(`0x003F92B0`, `0x003F9720`, `0x003C2320`, `0x003BF9A0`, `0x003C1180`). `0x003F92B0` shows the use: when the
current area's bit is set (`0x003F92DA`) it prints, after the location text, the region name that `0x00377870`
returns for the word at `+0x04` of its record (`0x003F9310`-`0x003F9314`); otherwise it prints text `0x3EC`.

The same name table (`MapName`, `planmapname.bin`, at `0x02ADD0F8`) also names the regions. Each entry of the offset
table `+0x10` is a `u16` offset from the start of the file. Three readers return a name:

| Reader | Entry | Bound | Callers |
|---|---|---|---|
| `0x00377B60(id)` | `id` | the area count `+0x04` (`0x00377B6C`-`0x00377B6F`) | `0x0029C65A`, `0x002B81D5`, `0x002B9D25`, `0x002BA5FB`, `0x002BB63B`, `0x002BBC80`, `0x003C23DF`, `0x0057FC33`, `0x0057FD93` |
| `0x00377870(region)` | `[+0x04] + region` | the region count `+0x08` (`0x0037787C`-`0x0037787F`) | `0x003BF769`, `0x003F9314`, `0x003F9352`, `0x003F99E7` |
| `0x003778B0(field)` | `[+0x04] + 0x00264F90(field)`, the field's persistence group | the region count `+0x08` (`0x003778C7`-`0x003778CA`) | `0x0029C61A`, `0x0029C62F`, `0x0057FC8A`, `0x0057FD14` |

Each bound is an unsigned compare (`jae`), so a negative id is refused as well. A missing table, a refused id or an
entry of 0 gives the empty string `0x01CEB638` (`0x00377B85`, `0x00377899`, `0x003778E8`), and no reader returns null, so
none of the 17 call sites tests the result: a bad id shows an empty name.

### The hold flag and its save veto

Bit `0x1` of the third byte is read inverted by `0x00377700`: it returns 1 only when the bit is clear and
`0x00314A60` reports bit `0x1` of payload byte `+0x1062` clear (`0x0037772D not`, `0x0037772F test al, 1`,
`0x00377733 call`, `0x0037773C mov eax, 1`). A missing table yields a zero byte (`0x00377728`), so the
missing-table answer is 1, the permissive value. The save bit can only force the answer to 0.

Six actor-system functions call it (`0x00263230`, `0x00268D10`, `0x0026A1D0`, `0x0026B980`, `0x0026C3E0`,
`0x0026C5D0`). Two of them store the inverse into the party-hold byte `0x02099DE7`: `0x0026A1D0` at
`0x0026A20B` and `0x00268D10` at `0x00268E29` (`setz bpl` on the call's result). That byte is the parameter
of the party hold request the time-stop registry receives; see the time stop page.

### The default leader

Bits `0x70` of the third byte are read by `0x00377C70` (`0x00377C99 shr eax, 4`, `0x00377C9C and eax, 7`). Its
callers are `0x00326500`, `0x003266C0` and `0x0031C000`. `0x00326500` picks the party member the game follows
when control returns: the saved leader at `[0x02EBF190] + 0x5AA4` at control levels 0 and 1, id `0x1A`
at level 2, and this field at level 3, the town level (`0x0030D9A0`).

Every shipped record has these bits at 0 (counts below), and 0 is party row 0, Vaan, so in every town the game hands
control to
Vaan; only when he has no battle unit does the function fall back to the first of the four active
slots with a unit, then to `0x00263750(0)`.

### What a missing table returns

Every reader runs its normal shift and mask on a default record of `0x0FFF` for the word and 0 for the
third byte. The defaults do not agree on what they mean:

| Reader | Default | Meaning |
|---|---|---|
| `0x00377C20`, `0x00377480` | 0 | not a town |
| `0x00377A40` | 0 | no area name |
| `0x00377BA0` | 0 | normal MP regime |
| `0x003779F0` | -1 | no Map entry |
| `0x00377700` | 1 unless the save veto is set | hold permitted |
| `0x00377C70` | 0 | leader id 0 |

## Layouts

`AreaTable` (`0x8` bytes, offsets from the start of the table):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | tag | 'NAV' `0x02` (`0x0256414E`); the seven readers never test it |
| `+0x04` | `u32` | count | record count, 1,154 shipped; every reader bounds the id against it unsigned (`0x00377C35`) |

`AreaRecord` (`0x3` bytes, offsets from the start of the table+8+3*id):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | flags | bits `0xFFF` Map entry (`0x003779F0`), bits `0x3000` MP regime (`0x00377BA0`), bit `0x4000` area name (`0x00377A40`), bit `0x8000` town (`0x00377C20`, `0x00377480`) |
| `+0x02` | `u8` | options | bit `0x1` hold flag (`0x00377700`, read inverted), mask `0xE` authored and read by no code, bits `0x70` default leader (`0x00377C70`), bit `0x80` never set and never read |

## Shipped data

Every record, decoded field by field, is in [area-flags-navimapdata.tsv](area-flags-navimapdata.tsv): one row per area
id with the `us` name `0x00377B60` returns (empty for an id with no name entry), the flag word, the Map entry
(`-` for `0xFFF`), the MP regime, the area-name and town bits, the third byte, the hold bit, mask `0xE` and the
default leader.

Counts over the 1,154 records in `navimapdata.bin`:

| Field | Shipped values |
|---|---|
| town flag (bit `0x8000`) | set on 193 areas |
| area name (bit `0x4000`) | set on 155 areas, 154 of them towns |
| MP regime (mask `0x3000`) | 0 on 945, 1 on 36, 2 on 69, 3 on 104 |
| Map entry (mask `0xFFF`) | `0xFFF` (no entry) on 556; one on the other 598: 0 on 200; 369 distinct values, every value from 0 to 368 |
| hold flag (byte 2 bit `0x1`) | set on 170 areas, every one of them a town; the 23 towns without it are ids 0-22 |
| byte 2 bits under mask `0xE` | 0x02, 0x04 and 0x08 in eight combinations across 638 areas |
| byte 2 bits under mask `0xF0` | 0 on every record |

The towns, with the names the `us` `planmapname.bin` gives through the name indexer `0x00377B60`
(offset table at `+0x10`, 1,312 entries; ids with no name entry are omitted):

| Field ids | Towns |
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
variants of those areas.

Areas with MP regime 2 or 3 include:

- Terminus No. 7 in Barheim Passage;
- the Nabreus Deadlands: Vale of Lingering Sorrow, Echoes of the Past, The Slumbermead;
- the Great Crystal: A Vikaari Bhrum, Sthaana Pisces, Crystal Core;
- the Necrohol of Nabudis: Hall of Effulgent Light, Cloister of Solace, The Crucible;
- the Pharos: They Who Thirst Not, Womb of the Sun-cryst, Heaven's Challenge;
- the Lhusu Mines: Site 7;
- the Stilshrine of Miriam: Hall of Worth, Throne of Veiled Gods;
- Giruvegan: Gate of Earth, Gate of Water, Gate of Fire, Gate of Wind.

The name table's header, measured in all nine language copies of `planmapname.bin`:

| Fact | Value |
|---|---|
| magic `+0x00` | `PLMN` |
| area entries `+0x04` | 1,312 (`0x520`) |
| region entries `+0x08` | 59 (`0x3B`) |
| all entries `+0x0C` | 1,371 (`0x55B`) |
| `us` regions | region 0 has no entry; 41 and 44 share the entry `NOT USED`; 3 is Barheim Passage, 37 Nalbina Town |

## Operations

| Function | Signature | Reads | Returns |
|---|---|---|---|
| `0x00378540` | `()` | resource (9, 8) `"MapInfo"` | installs the table pointer through `0x00378B80` into `0x02ADD100` |
| `0x00377C20` | `()` | word bit `0x8000` of the current area | 0/1; 65 callers plus 47 through `0x00313F60` |
| `0x00377480` | `(fieldId)` | word bit `0x8000` | 0/1; caller `0x0026C8C0` |
| `0x00377A40` | `(fieldId)` | word bit `0x4000` | 0/1; five menu callers |
| `0x00377BA0` | `()` | payload `+0x1062` bit `0x80`, then `+0x1063` bits under mask `0x30` or word bits `0x3000` | 0-3; four callers through `0x00320160` |
| `0x003779F0` | `(fieldId)` | word bits `0xFFF` | 0-4,094 or -1; nine callers |
| `0x00377700` | `()` | third byte bit `0x1`, payload `+0x1062` bit `0x1` | 1 when both are clear, else 0; six callers |
| `0x00377C70` | `()` | third byte bits `0x70` | 0-7; callers `0x00326500`, `0x003266C0`, `0x0031C000` |
| `0x003148F0` | `()` | payload `+0x1044` | the current or pending field id, negatives clamped to 0, `id < 0 ? 0 : id` |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `0x02ADD100` | `void*` | the loaded table | `0x00378540` (null), `0x00378B80` (delivery) |
| payload `+0x1044` | `i32` | current or pending field id | the zone change (see the zone changes page) |
| payload `+0x1062` bit `0x1` | bit | vetoes the hold flag | the zone change record's flag byte |
| payload `+0x1062` bit `0x80` | bit | enables the MP regime override | the zone change record's flag byte; the script verb `setmist(v)` (`0x00314BE0`: set for a positive `v`, cleared otherwise) |
| payload `+0x1063` bits under mask `0x30` | 2 bits | the overriding MP regime, the level the scripts call the mist level | the zone change record; `setmist(v)` stores `v & 3` (`0x00314C1B`-`0x00314C28`) and clears it for `v` at most 0 |
| `0x02099DE7` | `u8` | the party hold parameter, `0x00377700() == 0` | `0x0026A20B`, `0x00268E29` |

## Modding notes

- Setting bit `0x8000` on an area makes it a town for every system at once: fallen party members stay in
  play, the chain resets on entry, control level 3 applies and the saved leader is ignored. Clearing it
  on a shop interior re-arms the out-of-play rule there.
- The bits under mask `0x3000` are the only per-area MP control: 2 or 3 cuts the walk per MP point to a third, so
  walking recovery runs three times as fast, and triples the MP gained from damage. The save override at payload `+0x1062` bit `0x80` / `+0x1063` bits under mask `0x30` can
  impose a regime on any area without touching the file.
- The bits under mask `0x70` of the third byte are a working but unused feature: a non-zero value names the party member
  the game follows when control returns inside that town.
- The bits under mask `0xE` of the third byte are authored on 638 areas and read by no function: the table pointer `0x02ADD100` is
  loaded by the seven readers above and stored by the two loaders `0x00378540` and `0x00378B80`, and of the seven only
  `0x00377700` (bit `0x1`, `0x00377721`) and `0x00377C70` (bits `0x70`, `0x00377C91`) read the third byte. Changing them does nothing.
- Area names and the Map pages live in `planmapname.bin`, not here; the record only carries the Map
  entry id and the name flag.
- A name is reached through a `u16` offset from the start of `planmapname.bin`, so every string must start within the
  first 65,535 bytes; the shipped files are 11,008 to 15,264 bytes. An id past the area or region count, or an entry
  of 0, shows an empty name rather than failing.

## Related

- [Kill rewards: what an enemy's death triggers, when it gives nothing, and the order of chain, EXP, LP, gil, loot and counters](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)
- [Kill chain: chain count, chain level, the chain coin and resets](../Rewards-EXP-Gil-And-Loot/kill-chain.md)
- [Battle runtime mode ladder](../Engine-Core/party-control-modes.md)
- [The time-stop registry](../Engine-Core/time-stop-and-freeze.md)
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md)
- [The save payload field map](../Saving-Loading-And-Settings/save-data-fields.md)
