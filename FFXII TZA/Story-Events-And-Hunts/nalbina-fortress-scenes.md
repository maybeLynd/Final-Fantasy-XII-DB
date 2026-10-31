---
title: "Nalbina Fortress scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table has one row per scene script of Nalbina Fortress under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `naf_a0100` | `240` | Aerial Gardens | 31 | scene `naf_a0101` |
| `naf_a0101` | `241` | Aerial Gardens | 0 | story counter 13 |
| `naf_a0201` | `247` | Inner Ward | 6 | story counter 16 |
| `naf_b0100` | `242` | Lower Apartments | 12 | story counter 19 |
| `naf_b0400` | `243` | The Highhall | 4 | story counter 22 |
| `naf_b0401` | `244` | The Highhall | 21 | story counter 25, then Overflow Cloaca (Garamsythe Waterway) |

### What the scenes give

- No scene gives an item or changes the party.
- The loading functions write the story counter after five of the scenes: 13 (after Reks wakes), 16 (after
  tutorial 1), 19 (after Reks's unease), 22 (after Reks goes on alone) and 25 (after Reks's death)
  ([story counter values](story-counter-values.md)).
- `naf_a0201` is loaded between a release and a set of flag `0x00FC` ([story flag ids](story-flag-ids.md)).
- After `naf_b0401` the game jumps to Overflow Cloaca in the Garamsythe Waterway, field `1145`.
- `naf_a0101` holds one actor with two functions and no text.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Nalbina Fortress scripts](nalbina-fortress-scripts.md)): its actors, camera shots, motions, effects, music and loads.

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

- [Nalbina Fortress scripts](nalbina-fortress-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
