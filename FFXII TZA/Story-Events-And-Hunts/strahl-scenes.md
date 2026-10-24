---
title: "Strahl scenes: the scene, its text and the zone scripts that load it"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x0032FCA0"
---

## What it lists

The table [strahl-scenes.tsv](strahl-scenes.tsv) has one row for the scene script `str_z0000` under
`plan_master/us/event`, and the script list [strahl-script-list.tsv](strahl-script-list.tsv) one row with its size.
No zone script shares its file-name prefix, so its `loaded_by` and `next` columns are `-`; the zone scripts that load it
belong to other areas.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `str_z0000` | `211` | 18 zone scripts: five aerodromes and thirteen field maps | 2 | - |

| Script | Kind | Scene | Actors | Functions | Rows in a scripts table |
|---|---|---|---:|---:|---:|
| `str_z0000` | scene | event `211` | 8 | 40 | 0 |

### The scene

- The private airship desks of the Aerodromes of Rabanastre, Nalbina Town, Bhujerba, Archades and Balfonheim Port
  load event 211 from a talk function (`シュトラール受付.talk_step01` in Nalbina Town, `NPC01.talk_step01` or
  `NPC01.talk_09a` elsewhere; [Nalbina Town scripts](nalbina-town-scripts.md)).
- Thirteen field maps load it from `ym_shutoraljump.shtjump`: Passage Entrance (Dalmasca Estersand), Yensa Border
  Tunnel (Ogir-Yensa Sandsea), The Sandscale Bank (Nam-Yensa Sandsea), Kaukula Pass (Phon Coast), Babbling Vale
  (Mosphoran Highwaste), Sunlit Path (Ozmone Plain) and Path of the Firstfall (Paramina Rift).
- The other six are The Chosen Path (Tchita Uplands), Footfalls of the Past (Ridorana Cataract), both Crystal Glade
  maps (Giza Plains), Journey's Rest (Cerobi Steppe) and The Western Divide (Dalmasca Westersand).
- The debug control script `evctrl` also loads event 211, as the third choice of a debug menu whose event table
  holds 121, 121, 211 and 214 ([ATEL debug companions](../EBP-Script-Files/atel-debug-companions.md)).
- The load goes through `eventread` (`0x0E7`, `0x003529E0`) or `eventread_e8` (`0x0E8`, `0x00351880`), and `0x0032FCA0`
  reads the scene from index `4n` of the event file table
  ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- The scene's actors are `監督`, `ユニットＡ`, `ユニットＢ`, `ユニットＣ`, `カメラ`, `効果音`, `背景曲` and
  `STURAHL`. Its two lines are choice lists of digits, `(choices: 0 / 1 / 2 / 3)` and `(choices: 0 / 1)`.
- No function of the scene passes a line to the four message verbs, gives an item, writes a flag or the story
  counter, or jumps, so the scene has no row in a scripts table.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script with the same file-name prefix whose load call names the event; `-` here |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)` |
| `items` | items the scene's own functions give or take, by name |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows when the loading script has the same file-name prefix; `-` here |

The script list's columns are `script`, `kind` and `place` (the script, `scene`, and its event id), `actors` and
`functions` (the script's actors and functions), `rows` (its rows in a scripts table) and `shared_actors` (the shared
helper actors it carries).

## Related

- [Nalbina Town scripts](nalbina-town-scripts.md) - the private airship desk that loads this scene.
- [Aerodrome airship scenes](aerodrome-airship-scenes.md) - the scene the same aerodromes load for the public airships.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
