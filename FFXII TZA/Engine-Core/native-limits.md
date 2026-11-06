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
