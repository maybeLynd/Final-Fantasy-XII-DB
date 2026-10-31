---
title: "Eruyt Village scenes: each story scene with its dialogue, rewards, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table has one row per scene script of Eruyt Village under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `vic_a0100` | `253` | Fane of the Path | 26 | - |
| `vic_a0280` | `733` | The Spiritwood | 0 | story counter 1745 |
| `vic_a0300` | `255` | Fane of the Path | 41 | story counter 1950, then Road of Verdant Praise (Eruyt Village) |
| `vic_a0301` | `256` | Road of Verdant Praise | 18 | story counter 1790 |
| `vic_a0380` | `734` | Road of Verdant Praise | 4 | story counter 1740 |

### What the scenes give

- `vic_a0380`, loaded in Road of Verdant Praise, is followed by story counter 1740, after Go and fetch Mjrn ([story
  counter values](story-counter-values.md)): "In the village ahead you will find her: Mjrn. Bring her to me." Its
  first entry is the choice list "View scene again?" (Yes, No).
- `vic_a0280`, loaded in The Spiritwood, has no section 2 entries and is followed by story counter 1745, after signs
  of an intruder.
- `vic_a0100`, loaded in Fane of the Path by `SAKIYOMI_vic_a0100`: the party ask for Mjrn, Jote tells them to leave,
  and says "Our sister has left the Wood and gone west. She wanders warrens among men who hide themselves in clothes
  of cold iron."
- `vic_a0301`, loaded in Road of Verdant Praise, is followed by story counter 1790, Rescue Mjrn: the party take the
  warrens to be the Henne Magicite Mines, in Bancour south of the Ozmone Plain.
- `vic_a0300`, loaded in Fane of the Path, gives Lente's Tear and is followed by story counter 1950, after the
  sisters, and by the jump to Road of Verdant Praise, field `768`: "Lente's Tear is a permission. Pass through the
  Wood and leave." A sister asks to live freely and leave the Wood, and the scene ends with "Good-bye, sister." Its
  first entry is the choice list "View scene from:" (Beginning, Cut 11, Cut 20, Cancel).

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Eruyt Village scripts](eruyt-village-scripts.md)): its actors, camera shots, motions, effects, music and loads.

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

- [Eruyt Village scripts](eruyt-village-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
- [Henne Mines scenes](henne-mines-scenes.md) - the Henne Mines scenes, between `vic_a0301` and `vic_a0300`.
