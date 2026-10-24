---
title: "Feywood scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table [feywood-scenes.tsv](feywood-scenes.tsv) has one row per scene script of The Feywood under
`plan_master/us/event`. The zone scripts load them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`,
`0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index
`4n` of the event file table ([event scenes](../Scripts-And-Script-Commands/event-scenes.md), [zone
changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `mfr_a0400` | `353` | Antiquity's End | 0 | - |
| `mfr_b0100` | `350` | Redolent Glade | 0 | `mfr_b0101` (event `351`) |
| `mfr_b0101` | `351` | Redolent Glade | 0 | `pos_z0000` (event `427`) |
| `mfr_c0300` | `352` | The Edge of Reason | 0 | - |

### What the scenes give

- The four scenes hold no text of their own (`lines` 0), give no items and do not change the party.
- `mfr_a0400` plays when the party touches the Mist at Antiquity's End below story counter 4160; the zone script
  writes 4160 after it.
- `mfr_b0100` and `mfr_b0101` are loaded together when the Rafflesia fight in Redolent Glade begins; after the fight
  come the victory pose scene `pos_z0000` and story counter 4200. `mfr_b0101`'s own functions remove every foe in
  group 0.
- `mfr_c0300` plays when the Gigas gate opens at The Edge of Reason below 4250; the zone script then writes 4230 and
  jumps to Gate of Earth (Giruvegan), field 686.

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
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)` |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |

## Related

- [Feywood scripts](feywood-scripts.md) - every observable function of the same scripts.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
