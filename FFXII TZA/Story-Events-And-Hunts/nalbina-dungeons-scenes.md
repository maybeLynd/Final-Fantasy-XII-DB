---
title: "Nalbina Dungeons scenes: each story scene with its dialogue, rewards, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00, 0x0034C030, 0x0034D4E0, 0x0034A790"
---

## What it lists

The table has one row per scene script of the Nalbina Dungeons under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `nal_a0100` | `30` | Stockade | 12 | the Stockade, story counter 302 and 303 |
| `nal_b0100` | `31` | Arena | 6 | scene `nal_b0101` |
| `nal_b0101` | `33` | Arena | 45 | The Confiscatory |
| `nal_c0101` | `34` | The Black Watch | 3 | scene `nal_c0100` |
| `nal_c0100` | `32` | The Black Watch | 0 | story counter 312 |
| `nal_c0200` | `35` | The Confiscatory | 6 | the Confiscatory |
| `nal_d0100` | `36` | Oubliette | 29 | story counter 316, then The Lightworks (Barheim Passage) |

### What the scenes give

- In `nal_b0100` Balthier joins and the fighting party is set to Vaan and Balthier; in `nal_b0101` Fran joins and the
  fighting party is Vaan, Balthier and Fran (`addpartymember` `0x0034C030`, `setbattlemember` `0x0034D4E0`,
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md)).
- In `nal_c0200` the party's items and equipment come back (`giveback_item_and_equip`, `0x0034A790`), and the key items
  Nalbina Dungeons and Goddess's Magicite are given
  ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [scene rewards](scene-rewards.md)).

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Nalbina Dungeons scripts](nalbina-dungeons-scripts.md)): its actors, camera shots, motions, effects, music and loads.

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
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a scene with no non-empty entry: one sentence of what its script does |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |

## Related

- [Nalbina Dungeons scripts](nalbina-dungeons-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
