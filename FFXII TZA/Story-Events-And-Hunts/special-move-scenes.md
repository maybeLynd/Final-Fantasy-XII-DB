---
title: "Special move scenes: the scene script, its actors and what it shows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x0032FCA0"
---

## What it lists

The table [special-move-scenes.tsv](special-move-scenes.tsv) has one row for the scene script `spc_z0000` under
`plan_master/us/event`, and the script list [special-move-script-list.tsv](special-move-script-list.tsv) one row
with its size. It is the only script whose name begins `spc_`.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `spc_z0000` | `210` | no zone script names event 210 | 0 | - |

| Script | Kind | Scene | Actors | Functions | Rows in a scripts table |
|---|---|---|---:|---:|---:|
| `spc_z0000` | scene | event `210` | 5 | 17 | 0 |

### The scene

- Event 210 names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene managers
  1 to 3 ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- No zone script loads event 210 by a literal id, so the table has no loading function.
- The scene's five actors are `監督`, `技読み込み`, `メッセージ監督`, `target00` and `PC00`, whose functions
  include `技読み込み` and `必殺技設定`.
- Its section 2 has no entries, and no function shows a line, gives an item, writes a flag or the story counter, or
  jumps, so the scene has no row in a scripts table.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script with the same file-name prefix whose load call names the event; `-` here |
| `lines` | the number of entries in the scene's section 2 |
| `synopsis` | the `us` text of every non-empty entry; `-` here |
| `items` | items the scene's own functions give or take, by name |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows when the loading script has the same file-name prefix; `-` here |

The script list's columns are `script`, `kind` and `place` (the script, `scene`, and its event id), `actors` and
`functions` (the script's actors and functions), `rows` (its rows in a scripts table) and `shared_actors` (the shared
helper actors it carries).

## Related

- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
- [Action phases](../Battle-Actions/action-phases.md) - the battle action phases, with the script verb `spattackread`.
