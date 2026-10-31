---
title: "Necrohol of Nabudis scenes: each story scene with its dialogue, Espers, flags and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table has one row per scene script of Necrohol of Nabudis under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `bds_a0100` | `226` | Hall of Effulgent Light | 12 | - |
| `bds_e0100` | `224` | The Crucible | 0 | scene `bds_e0101` |
| `bds_e0101` | `225` | The Crucible | 1 | scene `bds_e0100` or scene `pos_z0000` |
| `bds_f0100` | `220` | Cloister of Solace | 1 | scene `bds_f0101` |
| `bds_f0101` | `221` | Cloister of Solace | 1 | scene `bds_f0100` or scene `pos_z0000` |
| `bds_g0100` | `222` | Cloister of Reason | 1 | scene `bds_g0101` |
| `bds_g0101` | `223` | Cloister of Reason | 1 | scene `bds_g0100` or scene `pos_z0000` |

### What the scenes give

- `bds_a0100`, loaded in Hall of Effulgent Light, is followed by flag `0x0035`, the location map's exits between
  Necrohol of Nabudis and The Salikawood ([story flag ids](story-flag-ids.md)): "This is all that remains of
  Nabudis. Two years ago it was destroyed utterly by a mysterious force."
- `bds_a0100`: the Mist of the Midlight Shard has made it a necrohol, and Fran gives the road to Archades: east
  through the Salikawood, along the Phon Coast to the Tchita Uplands.
- `bds_e0100` and `bds_e0101` open and close the fight in The Crucible; `監督.main` loads them in turn and then
  `pos_z0000`. `bds_e0100` has no section 2 entries, and the single entry of `bds_e0101` is an empty string.
  `bds_e0101` gives Chaos on field `438`.
- `bds_f0100` and `bds_f0101` (Cloister of Solace) and `bds_g0100` and `bds_g0101` (Cloister of Reason) open and close
  those fights; each holds one entry, the choice list `もう一度？` (`もう一度`, `やめる`), in Japanese in the `us` tree.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Necrohol of Nabudis scripts](necrohol-of-nabudis-scripts.md)): its actors, camera shots, motions, effects, music and loads. An entry that the `us` tree ships in Japanese gets an English sentence
first; the entry follows after `Authored text`, with its English in brackets.

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
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a scene with no non-empty entry: one sentence of what its script does; an entry the `us` tree ships in Japanese: an English sentence, then `Authored text (<its English>): ` and the entry |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |

## Related

- [Necrohol of Nabudis scripts](necrohol-of-nabudis-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
- [Nabreus Deadlands scenes](nabreus-deadlands-scenes.md) - `bog_a0201` holds nearly the same lines on the ruin of
  Nabudis ("two years" where `bds_a0100` has "2 years").
