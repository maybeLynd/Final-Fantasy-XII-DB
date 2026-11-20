[Home](../../README.md) / [Engine core](README.md) / Native limits

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Native limits: the engine's fixed counts, capacities and ranges, where each is set and what happens past it | reference | Engine core | Glossary, ids and limits | Limits the executable fixes, one row each: what it bounds, its exact value, whether it is a count, a highest index, a range, a width or an address bound, the instruction or table that sets it, what the engine does past it, and the page that explains the mechanism. | 0x00316CD0, 0x003247F0, 0x002FCAC0, 0x003C1A20, 0x00409210, 0x0051CC30, 0x0018AD00, 0x0021A9F0, 0x00219400, 0x00217FD0, 0x0021BDB0, 0x0021CC10, 0x007B1E10, 0x007E32E0, 0x00392200 |

## What it lists

[`native-limits.tsv`](native-limits.tsv) holds 229 limits the executable fixes: list and pool sizes, counts of loaded objects, value caps,
index and id ranges, name lengths, file-header bounds and one address bound. Each row names the code or table that
sets the limit and what the engine does with one more, and it links to the page that explains the mechanism.

Values are exact. A count and its highest index are separate rows where both matter (`action-targets` 32 and
`action-target-highest` 31; `item-pictures` 512 and `item-picture-highest` 511). A range row gives both ends.

| Area | Pages in | Rows | Limits a modder meets first |
|---|---|---:|---|
| Actors and combat | 04, 05, 07, 08, 09, 13 | 30 | 32 battle units, 512 actor manager points, 64 spawn records and 64 spawn counters per bank, 32 targets per action, 32 noticed units per enemy, 11 combo hits, action ids up to `0x21E` and orders `0x4000`-`0x4166`, the 60,000 deposit bank, the 10,000 gil-toss sum |
| Items, licences, party | 11, 12 | 10 | 99 of an item, 99,999,999 gil, 3 MP bars, 12 gambit slots, licence members 0-39, 64 grants per scenario preset |
| Menus and input | 15, 16 | 44 | 112 pooled widgets, a 32-entry focus stack, 8 message slots, 17 rows per gambit page, row 682 of a 48-pixel list, 11 statuses per party row, `0x4000` text index words, 127-character keymap lines |
| Scripts, maps and engine core | 00, 01, 03 | 24 | 128 models bound per map, `s16` variables clamped to -32,767 to 32,768 (`v < -32767 ? -32767 : v > 32768 ? 32768 : v`, then the low word stored, `0x0026D530`), a 65,536-instruction budget per script call, after which the call ends at the first instruction boundary with an empty stack, 32 binding lanes, scene slots 1-3 |
| Resources, files and saves | 02, 19 | 38 | 15 memory arenas, 200 save slots, 1,024 outstanding load requests, 32 effect tickets, 512 item pictures, 18 sloc pictures, 4 prompt-bar entries, 31-character section names, a 1 MiB save image, the 2 GB quest buffer bound |
| Movement | 06 | 10 | 128 route steps, 128 cells per collision sub-step, 4 placed party units, the wrapping cell occupancy byte |
| Rendering | 17 | 43 | 6 directional lights per character, 32 light groups, 16 event lights, 64-entry effect actor tables, presentation command ids `0x00`-`0x48`, 5,000 render commands reserved before the list first doubles (`n ? 2 * n : 1` entries for `n` held, `0x001AB5F0`, `0x001AB5FD`) |
| Audio | 18 | 16 | 96 sound-effect blocks, 256 single banks, 2 music tracks, 92 driver sounds, 8 driver music objects, 32 sound registrations, 2-16 streams |
| Engine libraries | 22, 23, 24 | 14 | `0x800` thread-pool jobs, 512 records per draw command buffer, 10,000 to 1,000,000 memory cache entries |

The engine handles one past the limit in five ways, and the `past_it` column says which:

- it refuses the request and says so (the 93rd driver sound, the text index buffer, the stream count);
- it serves the request from somewhere else (the 113th pooled widget comes from the heap);
- it drops the item without a word (the 33rd target, the 33rd noticed unit, the party row's 12th status);
- it clamps or wraps the value (item counts, gil, MP bars, gambit slots, the `s16` variable, light groups);
- it writes past the end, a fault or a corruption waiting to happen (the 129th bound model, the gambit page's 18th row,
  an async request with no free entry).

## Columns

| Column | Meaning |
|---|---|
| `limit` | the row's name |
| `bounds` | what the limit bounds |
| `value` | the exact value; a range gives both ends |
| `kind` | `count`, `highest index`, `range`, `value` (a cap on a stored value), `sum`, `bytes`, `characters` or `address` |
| `set_by` | the instruction, function, table or field that fixes the limit |
| `past_it` | what the engine does with one more, or with a value past the end |
| `page` | the page that explains the mechanism, by its path in the database |

### The battle-unit limit in the code

[`native-limits-battle-unit-sites.tsv`](native-limits-battle-unit-sites.tsv) has one row for each of the 204 code
sites, in 77 functions, that use the limit directly.

| Column | Meaning |
|---|---|
| `function`, `site` | the function that holds the instruction, and the instruction's address |
| `kind` | what the instruction uses: the slot count `0x0208E6A0`, the pool `0x0208E688`, the per-slot table `0x02B59D80`, a call of an accessor, the stride `0xF50` (`imul`, `add` or `lea`), the size `0xF50` of a clear, the product `0xEA7900`, a compare with 32 or 31, a count of 32 before a `rep stos` or for a loop counted down, or a bit operation whose bit number is in a register |
| `instruction` | the instruction as disassembled |
| `pages` | the pages that cite the function; `-` for none |

The pool is 32 records of `0xF50` bytes. The two keep banks allocated beside it hold 64 spawn records of `0x250`
each, so they follow the spawn limit and are not listed. A function that receives a unit pointer from its caller
is not listed unless it also uses one of these directly, or clears the 32 entries at unit `+0xDD4` as `0x003176C0` does.Compare and bit rows are the operations of that kind in a listed function; a row does not by itself say the
operand is a unit index.

`Database/Tools/catalogues/battle_unit_deps.py` writes the table.

### What uses a unit's slot number

A unit's slot number is its byte `+0xEA9`, stored once by the allocator `0x00234480`¹. Raising the limit
past 32 has to widen everything that number indexes.
[`native-limits-battle-unit-index-uses.tsv`](native-limits-battle-unit-index-uses.tsv) follows each of its 69 reads,
in 45 functions, to what the same function does with the value. `0x0031B750` only returns it, and its two callers are
the first row of the table below.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002344E0` |

</details>

| Column | Meaning |
|---|---|
| `function`, `read_at` | the function and the instruction that reads the byte |
| `used_at`, `instruction` | the later instruction that uses the value |
| `use` | `shift by the slot` or `bit test or set`, a mask of one bit per unit; `array index`, `scaled by shift`, `added to a base` and `field of the indexed element`, a table indexed by unit; `compare`; `stored`; `argument`, the register still holds the number at a call, and only `0x00236820` and `0x00328FF0` read it; `field used directly`, the allocator's store; `no use within reach`, `0x0031B750` |
| `array_base_loaded_at` | where the table's base address was loaded, when the use names one |
| `pages` | the pages that cite the function; `-` for none |

The trace reads forward from each read inside its function and follows direct jumps and both paths of a conditional
jump, up to 48 instructions on a path.

The tables it indexes:

| Storage | Per slot | What it holds |
|---|---|---|
| `0x02B59D80` | `0x150` bytes, 32 records | the presentation records ([Status visuals](../Graphics/character-status-visuals.md)): `0x0031B750`'s callers `0x002E28E0` and `0x002E3AF0` pass the number to `0x003E7500` and `0x003E7D50` |
| unit `+0xDD4` | one `u32`, 32 in all, cleared by `0x003176C0` | one entry per other unit, which the being-hit check reads ([Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md)) |
| `0x0208DE80` | `0x40` bytes | the slot record the damage code picks ([Damage formula](../Damage-And-Battle-Formulas/damage-formula.md)) |
| `0x022C1DB0` | 12 bytes, `0x180` in all, cleared by `0x0030C3F0` | what a battle verb saves and restores ([Battle verbs](../Scripts-And-Script-Commands/battle-verbs.md)) |
| `0x022C1F50` | 16 bytes, indexed at `+8` and `+0x10` | the deferred HP list ([Quickenings and summons](../Battle-Actions/quickenings-and-summons.md)) |
| `0x022C26A0`, `0x022C2720` | one `u32` each, `0x100` in all | the AI's mask of pairs already tested and of pairs found clear ([Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md)) |

A `u32` mask holds one bit per unit, so 32 units fill it. 23 of the rows shift or test such a bit, in 13 functions.
The three masks of [the result record](../Status-Effects-And-KO/status-timers.md) are among them¹.
This table covers the slot number only.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00385A7F`, `0x00385AC0`, `0x00387B97` |

</details>

`Database/Tools/catalogues/battle_unit_index.py` writes the table.

### What depends on the limit

[`native-limits-battle-unit-dependencies.tsv`](native-limits-battle-unit-dependencies.tsv) has one row for each of
the 16 structures tied to the limit: the pool and its count, the slot number, the per-slot tables, the masks and the
lists held by position, with where each is sized, used and cleared and whether it is saved.

The count `0x0208E6A0` is set once, to the constant `0x20`¹. `0x00324F20` does not use it: it walks the pool
with the constant 32, stepping `0xF50` from `0x00236820(0)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002368FE` |
| ² | `0x00325012`, `0x00325042` |

</details>

Three lists hold up to 32 units by position and not by slot: the target list at unit `+0x778`, its bounce slots at
`+0x988` and the noticed list at `+0xBC0`. Their capacity is separate from the pool's.

The spawn keep banks follow the 64-record spawn limit. `0x00233440` writes both to the save, `0x9400` bytes each, and
`0x00233550` restores bank 2. Direct and tail calls from `0x00229B40`, `0x00233440`, `0x00233550`, `0x00584580` and `0x005843E0`
reach no function that loads the unit pool and no unit accessor.

The `saved_state` cells rest on one search. The save image is `0x56690` bytes at `0x02164280`¹. The save
closure is the 145 functions that direct and tail calls reach from the capture functions `0x00229B40`, `0x00584580`,
`0x005844A0`, `0x00233440`, `0x0025D8E0`, `0x002EF540`, `0x002EF510`, `0x002EF3C0`, `0x00583D60`, `0x002EF570`, `0x00234ED0` and the
restore functions `0x005843E0`, `0x00233550`, `0x00269A20`, `0x00584210`, `0x002EF410`, `0x002EF4A0`, `0x002EF7C0`, `0x002EF740`,
`0x00235AF0`. A call or jump through a pointer ends the walk.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EF640` |

</details>

A row's functions are the code references to its address, or the rows of its field in
[`battle-unit-fields.tsv`](../Characters-And-Objects/battle-unit-fields.tsv). A payload write is a `w` or `rw` row of the
accessor tables of [save data fields](../Saving-Loading-And-Settings/save-data-fields.md). Each write's source registers
were followed back through the function's linear code, ten definitions at most, stopping at a call for a volatile
register. A cell that says a write takes no value from the dependency reports that walk.

A field's rows run from its first byte to its last, and each is a direct access. A function that reaches a field
through a copied pointer or a block copy has no row there: `0x0030EDA0` copies into `+0x6B0` to `+0xB9F`, nine passes
of 0x80 bytes¹ and then 0x70 more², and it has no row in `+0x778` to `+0x97F`.
A count covers direct accesses only,
and no cell takes it as proof that a save writer does not exist.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030EDB1` |
| ² | `0x0030EE09`-`0x0030EE44` |

</details>

`0x005844A0` and `0x00583D60` reach battle code only through `0x00283270`, which calls `0x00320040` at `0x00283368`, which
jumps to `0x00329220` at `0x0032008D`. None of the 33 functions that lie only behind `0x00283270` has a payload write. Without
it the closure has 112 functions and none of the battle functions `0x00236820`, `0x00236850`, `0x00263E30`, `0x0031B7E0`,
`0x0031B860`, `0x00387090`, `0x002FEAD0`, `0x0030C0E0`, `0x0031FDA0`, `0x00329220`.

### Which compares and bit tests are about units

[`native-limits-battle-unit-site-classes.tsv`](native-limits-battle-unit-site-classes.tsv) sorts the 46 compare, bit
and loop rows of the site table by what the operand is. 26 are tied to the limit and 20 are status bits or bits
of another field.

### Who reaches a unit through a pointer

[`native-limits-battle-unit-consumers.tsv`](native-limits-battle-unit-consumers.tsv) has the 444 functions of
[`battle-unit-fields.tsv`](../Characters-And-Objects/battle-unit-fields.tsv), with the route each reaches a unit by and how
many fields it uses. 378 of them are not in the site table: they depend on the record's layout and not on the count.
43 read the slot number.

### Columns of native-limits-battle-unit-dependencies.tsv

| Column | Holds |
|---|---|
| `dependency`, `kind` | the structure, and whether it is storage, a count, an index, a mask, a state bit or a list held by position |
| `capacity`, `what_a_slot_or_entry_holds` | its size and what each part holds |
| `set_or_sized_at`, `read_or_used_at`, `reset_at` | the instructions that size or set it, use it and clear it |
| `saved_state` | what the save does with it and at which site, or where its accesses stand against the save closure (described above) |
| `page` | the page that describes it |

### Columns of native-limits-battle-unit-site-classes.tsv

`function`, `site`, `kind` and `instruction` repeat the site table. `class` is `slot number`, `unit loop`, `unit
mask`, `unit storage`, `table loop`, `list capacity`, `status` or `other`. `what_the_operand_is` says why.

### Columns of native-limits-battle-unit-consumers.tsv

| Column | Holds |
|---|---|
| `function`, `name` | the function and its name in the field table |
| `route` | how it reaches a unit: an accessor's address, or `arg0` for a unit passed in |
| `fields`, `reads`, `writes`, `other` | how many offsets it uses, and how many accesses of each kind |
| `uses_the_limit_directly`, `reads_the_slot_number` | `yes` when it is in the site table, or in the slot-number table |

### Spawn records, memory arenas and save slots

[`native-limits-family-dependencies.tsv`](native-limits-family-dependencies.tsv) has one row for each of the 23
structures tied to these three limits, with where each is sized, used and cleared and whether it is saved.

The 64-record spawn limit is shared by the two keep banks, the 2 x 64 counters, the lane maps' slot bytes and the
bank scan `0x00235360`. `0x002395A0` seeds records from a count in its argument and does not test it against 64¹. `0x00233440` writes both banks to the save. Direct and tail calls from `0x00229B40`,
`0x00233440`, `0x00233550`, `0x00584580` and `0x005843E0` do not reach the functions that use the counters or their bank
byte.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023967E`, `0x00239685` |

</details>

The 15 arenas each have a record, a bit in the enabled mask `0x022D89B8` and a byte in the table `0x022D89A8`. A block's
header names its arena in byte `+0x03`. The arena stack stops at depth 31 by jumping to itself¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036C20B` |

</details>

The 200 save slots are carried by five structures: the status table `0x02B407C0`, a bit set at controller `+0x568`,
the row table at `+0xEF`, the header cache and the file listing `0x02B41140`. The file name has three decimal digits.

[`native-limits-family-sites.tsv`](native-limits-family-sites.tsv) sorts each family's code sites by what the
operand is. [`native-limits-family-consumers.tsv`](native-limits-family-consumers.tsv) has the functions that reach
a family's records through a pointer or an accessor.

### Columns of the family tables

All three start with `family`: `spawn-records`, `memory-arenas` or `save-slots`.

`native-limits-family-dependencies.tsv` has the columns of
[`native-limits-battle-unit-dependencies.tsv`](native-limits-battle-unit-dependencies.tsv).

`native-limits-family-sites.tsv` has `function`, `site`, `kind` and `instruction`, then `class` and
`what_the_operand_is`. `class` is `storage`, `accessor`, `stride`, `size`, `limit`, `slot number`, `slot loop`,
`slot bit`, `arena number`, `mask` or `unrelated`.

`native-limits-family-consumers.tsv` has `function`, `name`, `route`, `fields`, `reads`, `writes`, `other` and
`uses_the_limit_directly`. `route` says how the function reaches a record, or which accessor it calls and how often.
`fields`, `reads`, `writes` and `other` are `-` where no field table covers the function.

In `route`, `arena ?` is a call whose arena number the table does not follow back to a constant. 90 of the 112
`memory-arenas` rows have one.

`Database/Tools/catalogues/native_limit_unit_tables.py`, `native_limit_family_sites.py` and
`native_limit_family_tables.py` write these tables.

## Related

- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): the allocators behind the pools
- [Area of effect](../Battle-Actions/area-of-effect.md): the 32-entry target list
- [Audio manager](../Sound-And-Music/audio-manager.md): the five bank pools
- [Menu lists](../Menus-And-HUD/menu-lists.md): the 16-bit scroll

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 69 calls with 24 other topics</summary>

**Characters and objects** (explained on [frame update order](frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003247F0`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle unit: rebuild perception candidate cache (on enemy ai) | calls | [`0x00236820`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) (on equipping an item)<br>[`0x00236850`](../Enemy-AI-And-Gambits/enemy-order-sets.md) (on enemy order sets)<br>[`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse)<br>[`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |
| [`0x003247F0`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle unit: rebuild perception candidate cache (on enemy ai) | is called by | [`0x00233F70`](../Enemy-Spawning/enemy-respawning.md) Battle unit: update lifecycle and combat frame (on enemy respawning) |

**Sound and music** (explained on [audio manager](../Sound-And-Music/audio-manager.md), [debug logging](debug-logging.md), [sound driver objects](../Sound-And-Music/sound-driver-objects.md), [sound streaming](../Sound-And-Music/sound-streaming.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00217FD0`](native-limits.md) | calls | [`0x00212710`](native-limits.md)<br>[`0x00217E10`](native-limits.md) |
| [`0x00217FD0`](native-limits.md) | is called by | [`0x002105E0`](../Sound-And-Music/sound-banks.md) (on sound banks) |
| [`0x00219400`](native-limits.md) | calls | [`0x00212710`](native-limits.md)<br>[`0x00219300`](../Sound-And-Music/audio-manager.md) (on audio manager) |
| [`0x00219400`](native-limits.md) | is called by | [`0x002105E0`](../Sound-And-Music/sound-banks.md) (on sound banks) |
| [`0x0021A9F0`](native-limits.md) | calls | [`0x00212710`](native-limits.md)<br>[`0x0021A820`](native-limits.md) |
| [`0x0021A9F0`](native-limits.md) | is called by | [`0x002105E0`](../Sound-And-Music/sound-banks.md) (on sound banks) |
| [`0x0021BDB0`](native-limits.md) | calls | [`0x00212710`](native-limits.md)<br>[`0x0021BCB0`](native-limits.md) |
| [`0x0021BDB0`](native-limits.md) | is called by | [`0x002105E0`](../Sound-And-Music/sound-banks.md) (on sound banks) |
| [`0x0021CC10`](native-limits.md) | calls | [`0x00212710`](native-limits.md)<br>[`0x0021CB10`](native-limits.md) |
| [`0x0021CC10`](native-limits.md) | is called by | [`0x002105E0`](../Sound-And-Music/sound-banks.md) (on sound banks) |
| [`0x007B1E10`](native-limits.md) | calls | [`0x007A5570`](../Sound-And-Music/sound-engine.md) (on sound engine)<br>[`0x007AF380`](../Sound-And-Music/sound-driver-objects.md) (on sound driver objects)<br>[`0x007B2880`](../Sound-And-Music/sound-driver-objects.md) (on sound driver objects)<br>[`0x007DF750`](../Sound-And-Music/sound-driver-objects.md) (on sound driver objects)<br>[`0x007DF8D0`](../Sound-And-Music/sound-driver-objects.md) (on sound driver objects)<br>[`0x007E2C50`](../Sound-And-Music/sound-streaming.md) (on sound streaming) |
| [`0x007B1E10`](native-limits.md) | is called by | [`0x007A4B30`](../Sound-And-Music/sound-streaming.md) (on sound streaming) |
| [`0x007E32E0`](native-limits.md) | calls | [`0x007A5570`](../Sound-And-Music/sound-engine.md) (on sound engine)<br>[`0x007AD460`](../Sound-And-Music/sound-engine-config.md) (on sound engine config)<br>[`0x007D09B0`](native-limits.md)<br>[`0x007E2BC0`](../Sound-And-Music/sound-streaming.md) (on sound streaming) |

**Enemy AI and gambits** (explained on [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md), [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00316CD0`](../Battle-Actions/area-of-effect.md) Battle target buffer: try append actor work (on area of effect) | is called by | [`0x0030F130`](../Party/party-slots.md) Ai order: build candidate target buffer from stored range and status (on party slots) |
| [`0x003247F0`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle unit: rebuild perception candidate cache (on enemy ai) | calls | [`0x00324F20`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle perception: refresh candidate cache generation (on enemy ai)<br>[`0x0032A4D0`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle perception: test cached spatial visibility pair (on enemy ai) |

**Battle actions** (explained on [action definition row](../Battle-Actions/action-definition-row.md), [identifier spaces](identifier-spaces.md), [bestiary](../Enemy-Spawning/bestiary.md), [area of effect](../Battle-Actions/area-of-effect.md), [action range](../Battle-Actions/action-range.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00316CD0`](../Battle-Actions/area-of-effect.md) Battle target buffer: try append actor work (on area of effect) | is called by | [`0x0030D160`](../Battle-Actions/area-of-effect.md) Battle: build action target set (on area of effect)<br>[`0x0030F760`](identifier-spaces.md) Battle unit: commit action (on identifier spaces)<br>[`0x00313120`](../Battle-Actions/concurrence-list.md) (on concurrence list) |
| [`0x003247F0`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle unit: rebuild perception candidate cache (on enemy ai) | calls | [`0x002FFEF0`](../Battle-Actions/area-of-effect.md) (on area of effect)<br>[`0x0030BCB0`](../Battle-Actions/action-range.md) (on action range) |

**Movement and pathfinding** (explained on [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [party control modes](party-control-modes.md), [frame update order](frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003247F0`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle unit: rebuild perception candidate cache (on enemy ai) | calls | [`0x003919B0`](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md) (on navigation mesh and pathfinding)<br>[`0x00391D10`](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md) (on navigation mesh and pathfinding) |
| [`0x00392200`](native-limits.md) | calls | [`0x004690B0`](native-limits.md) |
| [`0x00392200`](native-limits.md) | is called by | [`0x00392170`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning)<br>[`0x00392740`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) |

**Platform** (explained on [game application](game-application.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00219400`](native-limits.md) | calls | [`0x005CD0A0`](../Compiler-And-C-Runtime/runtime-services.md) (on runtime services) |
| [`0x0021A9F0`](native-limits.md) | calls | [`0x005CD0A0`](../Compiler-And-C-Runtime/runtime-services.md) (on runtime services) |

**Graphics** (explained on [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md), [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md), [bone trails](../Graphics/bone-trails.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00409210`](../Graphics/animation-playback.md) (on animation playback) | is called by | [`0x0041D220`](../Graphics/animation-playback.md) (on animation playback)<br>[`0x00424D80`](../Graphics/character-render-records.md) (on character render records) |
| [`0x0051CC30`](../Graphics/bone-trails.md) (on bone trails) | is called by | [`0x003E6770`](../Graphics/bone-trails.md) (on bone trails) |

**Game files and data tables** (explained on [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00409210`](../Graphics/animation-playback.md) (on animation playback) | is called by | [`0x00409780`](../Game-Files-And-Data-Tables/resource-sections.md) Resource entry: find section index and offset (on resource sections) |

**Menus and HUD** (explained on [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003C1A20`](native-limits.md) | is called by | [`0x003BE3A0`](../Game-Files-And-Data-Tables/menu-map-files.md) (on menu map files) |

**World, areas and travel** (explained on [frame update order](frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003247F0`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle unit: rebuild perception candidate cache (on enemy ai) | calls | [`0x00313F60`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) (on equipping an item) |

**Damage and battle formulas** (explained on [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) (on equipping an item) | is called by | [`0x0031B860`](../Battle-Actions/battle-log.md) Battle stats: find owning battle unit (on battle log)<br>[`0x0031E800`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Battle stats: get owning actor handle (on enemy order sets) |

**Gameplay** (explained on [enmity](../Enemy-AI-And-Gambits/enmity.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) (on equipping an item) | is called by | [`0x0030C210`](../Enemy-AI-And-Gambits/enmity.md) Battle unit: has relationship class2 plus in slot mask (on enmity) |

**Items, equipment, shops and licenses** (explained on [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) (on equipping an item) | is called by | [`0x0031A300`](../Menus-And-HUD/status-and-equip-screen.md) Battle stats: clear all equipment slots by mapped id (on status and equip screen) |

**Enemy spawning** (explained on [battle units](../Characters-And-Objects/battle-units.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) (on equipping an item) | is called by | [`0x00308D90`](../Enemy-Spawning/enemy-spawning.md) Spawn: count active cap tracked actors (on enemy spawning) |

**Random numbers** (explained on [force fight mode](force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002395A0`](native-limits.md) Spawn entry: reset from table | calls | [`0x00328370`](../Random-Numbers/random-number-generators.md) (on random number generators) |

**Controls and input** (explained on [force fight mode](force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00320040`](../Characters-And-Objects/party-member-status-record.md) (on party member status record) | is called by | [`0x00253C70`](../Controls-And-Input/controls.md) (on controls) |

**Rewards: EXP, LP, gil and loot** (explained on [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031B860`](../Battle-Actions/battle-log.md) Battle stats: find owning battle unit (on battle log) | is called by | [`0x002F8BB0`](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md) Reward: compute experience for recipient (on stat growth per level)<br>[`0x0030C650`](../Menus-And-HUD/hud.md) Battle stats: advance level to target and recompute growth (on hud) |
| [`0x00329220`](../Party/party-table.md) (on party table) | calls | [`0x002F8F20`](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md) (on exp lp and level ups) |

**Status effects and KO** (explained on [status timers](../Status-Effects-And-KO/status-timers.md), [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md), [force fight mode](force-fight-mode.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse) | is called by | [`0x00386860`](../Status-Effects-And-KO/statuses.md) Battle formula: build runtime counter periodic hp credit (on statuses) |
| [`0x0031B860`](../Battle-Actions/battle-log.md) Battle stats: find owning battle unit (on battle log) | is called by | [`0x002F9400`](../Status-Effects-And-KO/mp.md) Battle unit: resolve periodic primary resource recovery step (on mp)<br>[`0x0030E360`](identifier-spaces.md) Battle stats: change status and process side effects (on identifier spaces)<br>[`0x0030F690`](../Damage-And-Battle-Formulas/augments.md) Battle stats: remove statuses from mask and recompute (on augments)<br>[`0x0030FED0`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Battle stats: recompute derived state and auto statuses (on equipping an item)<br>[`0x00386860`](../Status-Effects-And-KO/statuses.md) Battle formula: build runtime counter periodic hp credit (on statuses) |

**Story, events and hunts** (explained on [identifier spaces](identifier-spaces.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) | calls | [`0x0032A8A0`](../World-Areas-And-Travel/zone-asset-list.md) Persistent flag: query primary or authored threshold gate (on zone asset list) |

</details>
