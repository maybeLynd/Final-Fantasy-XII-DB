---
title: "Golmore Jungle scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table [golmore-jungle-scenes.tsv](golmore-jungle-scenes.tsv) has one row per scene script of Golmore Jungle under
`plan_master/us/event`. The zone scripts load them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`,
`0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index
`4n` of the event file table ([event scenes](../Scripts-And-Script-Commands/event-scenes.md), [zone
changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `gol_a0200` | `262` | The Needlebrake | 20 | - |
| `gol_c0100` | `260` | Dell of the Dreamer | 1 | `gol_c0101` (event `261`) |
| `gol_c0101` | `261` | Dell of the Dreamer | 1 | `pos_z0000` (event `427`) |

### What the scenes give

- `gol_a0200`, loaded in The Needlebrake below story counter 1700, holds the party's talk at the jungle's barrier ("We
  go to seek aid of the viera who dwell ahead." / "I am unwelcome. An unsought guest in their wood."); touching
  `VieraEventTrigger` plays it and writes 1700 ([Golmore Jungle scripts](golmore-jungle-scripts.md)).
- `gol_c0100` and `gol_c0101` are loaded together when the Elder Wyrm fight in Dell of the Dreamer begins; the victory
  pose scene `pos_z0000` follows the fight. Each holds only the Japanese choice list `もう一度？` (`もう一度` / `やめる`).
- No scene gives an item or changes the party.

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
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)`; an entry the `us` tree ships in Japanese: an English sentence, then `Authored text (<its English>): ` and the entry |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Golmore Jungle scripts](golmore-jungle-scripts.md) - every observable function of the same scripts.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
