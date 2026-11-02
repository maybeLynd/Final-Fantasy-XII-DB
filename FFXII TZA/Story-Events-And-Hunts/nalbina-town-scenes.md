---
title: "Nalbina Town scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table [nalbina-town-scenes.tsv](nalbina-town-scenes.tsv) has one row per scene script of Nalbina Town under
`plan_master/us/event`. The zone scripts load scenes with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8`
(`0x0E8`, `0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads
from index `4n` of the event file table ([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `nac_a0300` | `125` | West Ward | 6 | story counter 301, then the Stockade (Nalbina Dungeons), field `48` |

### The scene

- West Ward's `監督.main` writes 300, loads `nac_a0300`, writes 301 after it and jumps to the Stockade ([Nalbina Town scripts](nalbina-town-scripts.md),
  [Nalbina Dungeons scenes](nalbina-dungeons-scenes.md)).
- Its five lines are Japanese in the `us` tree, and the sixth is the `Skip` prompt. The scene gives no items and no
  party members.
- The Aerodrome loads two scenes that no area owns: the airship scene `pas_z0000`
  ([Aerodrome airship scene](aerodrome-airship-scenes.md)) and `str_z0000`
  ([Strahl scene](strahl-scenes.md)).

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

An entry that the `us` tree ships in Japanese gets an English sentence
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
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; an entry the `us` tree ships in Japanese: an English sentence, then `Authored text (<its English>): ` and the entry |
| `items` | items the scene's own functions give or take, by name |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Nalbina Town scripts](nalbina-town-scripts.md) - every observable function of the same scripts.
- [Nalbina Dungeons scenes](nalbina-dungeons-scenes.md) - the scenes of the Stockade, where this scene leads.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
