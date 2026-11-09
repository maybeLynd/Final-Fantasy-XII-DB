---
title: "Native limits: the engine's fixed counts, capacities and ranges, where each is set and what happens past it"
kind: "reference"
category: "Engine core"
addresses: "0x00316CD0, 0x003247F0, 0x002FCAC0, 0x003C1A20, 0x00409210, 0x0051CC30, 0x0018AD00, 0x0021A9F0, 0x00219400, 0x00217FD0, 0x0021BDB0, 0x0021CC10, 0x007B1E10, 0x007E32E0, 0x00392200"
---

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

A unit's slot number is its byte `+0xEA9`, stored once by the allocator `0x00234480` (`0x002344E0`). Raising the limit
past 32 has to widen everything that number indexes.
[`native-limits-battle-unit-index-uses.tsv`](native-limits-battle-unit-index-uses.tsv) follows each of its 69 reads,
in 45 functions, to what the same function does with the value. `0x0031B750` only returns it, and its two callers are
the first row of the table below.

| Column | Meaning |
|---|---|
| `function`, `read_at` | the function and the instruction that reads the byte |
| `used_at`, `instruction` | the later instruction that uses the value |
| `use` | `shift by the slot` or `bit test or set`, a mask of one bit per unit; `array index`, `scaled by shift`, `added to a base` and `field of the indexed element`, a table indexed by unit; `compare`; `stored`; `argument`, the register still holds the number at a call, and only `0x00236820` and `0x00328FF0` read it; `field used directly`, the allocator's store; `no use within reach`, `0x0031B750` |
| `array_base_loaded_at` | where the table's base address was loaded, when the use names one |
| `pages` | the pages that cite the function; `-` for none |

The trace reads forward from each read inside its function, follows direct jumps and takes the first branch path, so
a use after a conditional jump may be missing.

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
The three masks of [the result record](../Status-Effects-And-KO/status-timers.md) are among them (`0x00385A7F`,
`0x00385AC0`, `0x00387B97`).
This table covers the slot number only. Saved structures are not in it, and neither are the lists of up to 32 units
held by position: the target list at unit `+0x780`, its bounce slots at `+0x988` and the noticed list at `+0xBC0`.

`Database/Tools/catalogues/battle_unit_index.py` writes the table.

## Related

- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): the allocators behind the pools
- [Area of effect](../Battle-Actions/area-of-effect.md): the 32-entry target list
- [Audio manager](../Sound-And-Music/audio-manager.md): the five bank pools
- [Menu lists](../Menus-And-HUD/menu-lists.md): the 16-bit scroll

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x003247F0` calls `0x00236820`, `0x00236850`, `0x00263E30`, `0x003588B0`; `0x003247F0` is called by `0x00233F70`;
  those functions are documented on [frame update order](frame-update-order.md).
- Audio: `0x00217FD0` calls `0x00212710`, `0x00217E10`; `0x00217FD0` is called by `0x002105E0`; `0x00219400` calls `0x00212710`,
  `0x00219300`; `0x00219400` is called by `0x002105E0`; `0x0021A9F0` calls `0x00212710`, `0x0021A820`; `0x0021A9F0` is called by
  `0x002105E0`; `0x0021BDB0` calls `0x00212710`, `0x0021BCB0`; `0x0021BDB0` is called by `0x002105E0`; `0x0021CC10` calls
  `0x00212710`, `0x0021CB10`; `0x0021CC10` is called by `0x002105E0`.
- Audio: `0x007B1E10` calls `0x007A5570`, `0x007AF380`, `0x007B2880`, `0x007DF750`, `0x007DF8D0`, `0x007E2C50`; `0x007B1E10` is called
  by `0x007A4B30`; `0x007E32E0` calls `0x007A5570`, `0x007AD460`, `0x007D09B0`, `0x007E2BC0`.
- Audio: those functions are documented on [audio manager](../Sound-And-Music/audio-manager.md),
  [debug logging](debug-logging.md), [sound driver objects](../Sound-And-Music/sound-driver-objects.md),
  [sound streaming](../Sound-And-Music/sound-streaming.md).
- Combat AI: `0x00316CD0` is called by `0x0030F130`; `0x003247F0` calls `0x00324F20`, `0x0032A4D0`; those functions are
  documented on [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md),
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md).
- Combat action: `0x00316CD0` is called by `0x0030D160`, `0x0030F760`, `0x00313120`; `0x003247F0` calls `0x002FFEF0`, `0x0030BCB0`.
- Combat action: those functions are documented on
  [action definition row](../Battle-Actions/action-definition-row.md), [identifier spaces](identifier-spaces.md),
  [bestiary](../Enemy-Spawning/bestiary.md), [area of effect](../Battle-Actions/area-of-effect.md),
  [action range](../Battle-Actions/action-range.md).
- Movement: `0x003247F0` calls `0x003919B0`, `0x00391D10`; `0x00392200` calls `0x004690B0`; `0x00392200` is called by `0x00392170`,
  `0x00392740`.
- Movement: those functions are documented on
  [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md),
  [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md),
  [party control modes](party-control-modes.md), [frame update order](frame-update-order.md).
- Platform: `0x00219400` calls `0x005CD0A0`; `0x0021A9F0` calls `0x005CD0A0`; those functions are documented on
  [game application](game-application.md).
- Presentation: `0x00409210` is called by `0x0041D220`, `0x00424D80`; `0x0051CC30` is called by `0x003E6770`; those functions
  are documented on [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md),
  [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md),
  [bone trails](../Graphics/bone-trails.md).
- Resource: `0x00409210` is called by `0x00409780`; those functions are documented on
  [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md).
- UI: `0x003C1A20` is called by `0x003BE3A0`; those functions are documented on
  [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md).
- World area: `0x003247F0` calls `0x00313F60`; those functions are documented on
  [frame update order](frame-update-order.md).
- Combat formula: `0x00236820` is called by `0x0031B860`, `0x0031E800`; those functions are documented on
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- Gameplay: `0x00236820` is called by `0x0030C210`; those functions are documented on
  [enmity](../Enemy-AI-And-Gambits/enmity.md).
- Items equipment shops license: `0x00236820` is called by `0x0031A300`; those functions are documented on
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Spawn encounter lifecycle: `0x00236820` is called by `0x00308D90`; those functions are documented on
  [battle units](../Characters-And-Objects/battle-units.md).
