---
title: "Giza Plains scenes: each story scene with its dialogue, rewards, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table has one row per scene script of Giza Plains under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `sav_b0100` | `170` | Nomad Village | 11 | - |
| `sav_b0180` | `719` | Nomad Village | 3 | story counter 160 |
| `sav_b0181` | `737` | Nomad Village | 7 | - |
| `sav_c0280` | `717` | Crystal Glade | 7 | - |
| `sav_c0281` | `718` | Crystal Glade | 5 | Nomad Village (Giza Plains) |

### What the scenes give

- `sav_b0181` gives Penelo's three Potions and two Phoenix Downs, and `sav_b0180` Masyua's 50 gil, two Potions and two
  Teleport Stones ([scene rewards](scene-rewards.md)).
- `sav_b0180` is followed by story counter 160, Sunstone obtained
  ([story counter values](story-counter-values.md)).
- After `sav_c0281` the loading function jumps to Nomad Village, field `243`.
- Penelo joins in the Nomad Village function that loads `sav_b0181`, not in the scene itself; the
  [Giza Plains scripts](giza-plains-scripts.md) table has that row.
- The first entry of `sav_b0180`, `sav_c0280` and `sav_c0281` is the choice list "View scene again?" (Yes, No), and
  `sav_b0181` begins with "Start event from:" (`sav_a01 (North)`, `sav_a03 (East)`, `sav_a04 (West)`, Other) and
  "View scene again?"; the synopsis keeps them, as it keeps every non-empty entry.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### What follows a scene

The loading function is read on from the scene's load call. Story counter writes and flag sets up to the next scene
load or `mapjump` (`0x00354D00`) count as written with the scene, and that next load or jump is what follows it. A jump
made by the scene script itself comes first.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / ` |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |

## Related

- [Giza Plains scripts](giza-plains-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
