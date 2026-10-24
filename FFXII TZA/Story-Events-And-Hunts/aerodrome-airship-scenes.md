---
title: "Aerodrome airship scenes: the scene, its text and the aerodrome scripts that load it"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x0032FCA0"
---

## What it lists

The table [aerodrome-airship-scenes.tsv](aerodrome-airship-scenes.tsv) has one row for the scene script `pas_z0000`
under `plan_master/us/event`, and the script list
[aerodrome-airship-script-list.tsv](aerodrome-airship-script-list.tsv) one row with its size. No zone script shares
its file-name prefix, so its `loaded_by` and `next` columns are `-`; the zone scripts that load it are the aerodromes.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `pas_z0000` | `214` | the Aerodromes of Rabanastre, Nalbina Town, Bhujerba, Archades and Balfonheim Port | 2 | - |

| Script | Kind | Scene | Actors | Functions | Rows in a scripts table |
|---|---|---|---:|---:|---:|
| `pas_z0000` | scene | event `214` | 26 | 191 | 0 |

### The scene

- Each aerodrome loads event 214 from two functions: its director's `main` (`監督`, `常駐監督` or `EventDirector`)
  and `発着イベント監視.イベント再生とマップジャンプ`, the function the airship counters request, which also holds the
  jumps to the destinations ([Nalbina Town scripts](nalbina-town-scripts.md)).
- The debug control script `evctrl` also loads event 214, as the fourth choice of a debug menu whose event table
  holds 121, 121, 211 and 214 ([ATEL debug companions](../EBP-Script-Files/atel-debug-companions.md)).
- The load goes through `eventread_e8` (`0x0E8`, `0x00351880`) or `eventread` (`0x0E7`, `0x003529E0`), and `0x0032FCA0`
  reads the scene from index `4n` of the event file table
  ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- The scene's actors include `民間飛空艇` (the civilian airship), one set of three for each of the five towns
  (`ラバナスタ用１` to `バーフォン用３`), `客` (passengers) and `カメラマン`.
- Its two lines are Japanese choice lists in the `us` tree: `民間飛空艇発着イベントカメラ` with `何もしない`,
  `離陸カメラ` and `着カメラ`, and a second list with `もう一度` and `やめる`.
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

- [Nalbina Town scripts](nalbina-town-scripts.md) - the Aerodrome functions that load this scene and the jumps that follow.
- [Chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md) - riding chocobos and airships.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
