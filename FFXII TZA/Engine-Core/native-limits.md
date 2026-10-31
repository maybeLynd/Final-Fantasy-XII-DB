---
title: "Native limits: the engine's fixed counts, capacities and ranges, where each is set and what happens past it"
kind: "reference"
category: "Engine core"
addresses: "0x00316CD0, 0x003247F0, 0x002FCAC0, 0x003C1A20, 0x00409210, 0x0051CC30, 0x0018AD00, 0x0021A9F0, 0x00219400, 0x00217FD0, 0x0021BDB0, 0x0021CC10, 0x007B1E10, 0x007E32E0, 0x00392200"
---

## What it lists

`native-limits.tsv` holds 210 limits the executable fixes: list and pool sizes, counts of loaded objects, value caps,
index and id ranges, name lengths, file-header bounds and one address bound. Each row names the code or table that
sets the limit and what the engine does with one more, and it links to the page that explains the mechanism.

Values are exact. A count and its highest index are separate rows where both matter (`action-targets` 32 and
`action-target-highest` 31; `item-pictures` 512 and `item-picture-highest` 511). A range row gives both ends.

| Area | Rows | Limits a modder meets first |
|---|---:|---|
| Combat | 12 | 32 battle units, 64 spawn records and 64 spawn counters per bank, 32 targets per action, 32 noticed units per enemy, 11 combo hits, action ids up to `0x21E` and orders `0x4000`-`0x4166`, the 60,000 deposit bank, the 10,000 gil-toss sum |
| Items, licences, party | 6 | 99 of an item, 99,999,999 gil, 3 MP bars, 12 gambit slots, licence members 0-39, 64 grants per scenario preset |
| Menus and input | 14 | 112 pooled widgets, a 32-entry focus stack, 8 message slots, 4 prompt-bar entries, 17 rows per gambit page, row 682 of a 48-pixel list, 11 statuses per party row, `0x4000` text index words, 127-character keymap lines |
| Scripts, maps and actors | 12 | 128 models bound per map, `s16` variables clamped to -32,767 to 32,768, a 65,536-instruction budget per script call, after which the call ends at the first instruction boundary with an empty stack, 32 binding lanes, 512 manager points, scene slots 1-3 |
| Resources, files and saves | 18 | 15 memory arenas, 200 save slots, 1,024 outstanding load requests, 32 effect tickets, 512 item pictures, 18 sloc pictures, 31-character section names, a 1 MiB save image, the 2 GB quest buffer bound |
| Movement | 5 | 128 route steps, 128 cells per collision sub-step, 4 placed party units, the wrapping cell occupancy byte |
| Rendering | 8 | 6 directional lights per character, 32 light groups, 16 event lights, 64-entry effect actor tables, presentation command ids `0x00`-`0x48`, 5,000 render commands |
| Audio | 10 | 96 sound-effect blocks, 256 single banks, 2 music tracks, 92 driver sounds, 8 driver music objects, 32 sound registrations, 2-16 streams |
| Engine libraries | 3 | `0x800` thread-pool jobs, 512 records per draw command buffer, 10,000 to 1,000,000 memory cache entries |

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
| `kind` | `count`, `highest index`, `range`, `value` (a cap on a stored value), `sum`, `bytes`, `characters`, `texels` or `address` |
| `set_by` | the instruction, function, table or field that fixes the limit |
| `past_it` | what the engine does with one more, or with a value past the end |
| `page` | the page that explains the mechanism, by its path in the database |

## Related

- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): the allocators behind the pools
- [Area of effect](../Battle-Actions/area-of-effect.md): the 32-entry target list
- [Audio manager](../Sound-And-Music/audio-manager.md): the five bank pools
- [Menu lists](../Menus-And-HUD/menu-lists.md): the 16-bit scroll
