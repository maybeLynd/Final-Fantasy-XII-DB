---
title: "Victory pose scenes: the scene, what it gives and the zone scripts that load it"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x0032FCA0, 0x00345080"
---

## What it lists

The table [victory-pose-scenes.tsv](victory-pose-scenes.tsv) has one row for the scene script `pos_z0000` under
`plan_master/us/event`. No zone script shares its file-name prefix, so its `loaded_by` and `next` columns are `-`; the
zone scripts that load it belong to other areas.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `pos_z0000` | `427` | 139 zone scripts: the 100 Trial Mode stages and 39 maps of 23 regions | 0 | - |

### The scene

- Zone scripts load event 427 with `eventread` (`0x0E7`, `0x003529E0`) or `eventread_e8` (`0x0E8`, `0x00351880`);
  `0x0032FCA0` reads the scene from index `4n` of the event file table
  ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- In Trial Mode, every stage script's `トライアル監督.main` loads it. On the story maps the loading functions
  include `監督.main` (11 maps), `常駐監督.main`, `EventDirector.main` and `ボス登場.touch` (5 each).
- The scene has no text: its section 2 has no entries.
- Its `EFFECT.EFFECT_READ` holds `additem` (`0x2E5`, `0x00345080`) calls for the thirteen Esper ids `0xC012` to
  `0xC01E`, named on [Victory pose scripts](victory-pose-scripts.md).

### The story maps that load it

| Region | Maps |
|---|---:|
| Giruvegan; Necrohol of Nabudis; Pharos - First Ascent; Sochen Cave Palace; Stilshrine of Miriam; The Tomb of Raithwall | 3 each |
| Garamsythe Waterway; Henne Mines; Lhusu Mines; The Great Crystal | 2 each |
| Barheim Passage; Dalmasca Westersand; Dreadnought Leviathan; Golmore Jungle; Mosphoran Highwaste; Nam-Yensa Sandsea; Pharos - Second Ascent; Pharos - Subterra; Pharos - Third Ascent; Ridorana Cataract; The Feywood; The Salikawood; Zertinan Caverns | 1 each |

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script with the same file-name prefix whose load call names the event; `-` here |
| `lines` | the number of entries in the scene's section 2 |
| `synopsis` | the `us` text of every non-empty entry; `-` here |
| `items` | items the scene's own functions give or take, as `receives` and the item id |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows when the loading script has the same file-name prefix; `-` here |

## Related

- [Victory pose scripts](victory-pose-scripts.md) - the function that gives the Espers, with their names.
- [Quickening and Esper list](../Battle-Actions/quickening-and-esper-list.md) - the Esper ids.
- [Scene rewards](scene-rewards.md) - every item a script gives.
