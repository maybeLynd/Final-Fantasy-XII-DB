---
title: "Old Archades scenes: each story scene with its dialogue, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table [old-archades-scenes.tsv](old-archades-scenes.tsv) has one row per scene script of Old Archades under
`plan_master/us/event`. The zone scripts load them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8`
(`0x0E8`, `0x00351880`); the end handlers `0x00353080` and `0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads
from index `4n` of the event file table ([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `ald_a0179` | `728` | Alley of Muted Sighs | 10 | - |
| `ald_a0180` | `727` | Alley of Muted Sighs | 21 | - |
| `ald_a0200` | `173` | Alley of Low Whispers | 12 | story counter 3210 |

### The scenes

- `ald_a0180` is the meeting with Jules, the streetear, who offers his help for a price ("So, wise man, how does
  [value] gil sound?" with the choices Pay up and Decline).
- In `ald_a0179` Jules praises Vaan for telling his rumour just as he was told, a brawl breaks out ("The moogles are
  riotin'!"), and Jules gives Balthier word of "the prodigal Bunansa son".
- `ald_a0200` is the arrival in Old Archades ("Smells less like a capital... and more like a sewer."); its first
  entry is the replay prompt "View scene again?". After it the loading function writes 3210.
- None of the scenes gives items or party members.

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
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a line that names its speaker begins with the name |
| `items` | items the scene's own functions give or take, by name |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |

## Related

- [Old Archades scripts](old-archades-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
