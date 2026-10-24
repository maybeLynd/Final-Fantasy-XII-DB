---
title: "Henne Mines scenes: each story scene with its dialogue, rewards, story counter values and what follows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00"
---

## What it lists

The table has one row per scene script of Henne Mines under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `hne_a0700` | `344` | Staging Shaft | 9 | story counter 1820 |
| `hne_b0100` | `340` | Ore Separation | 0 | scene `hne_b0101` |
| `hne_b0101` | `341` | Ore Separation | 0 | scene `hne_b0100` or scene `pos_z0000` |
| `hne_b0102` | `345` | Ore Separation | 22 | story counter 1900, then Fane of the Path (Eruyt Village) |
| `hne_e0100` | `342` | Special Charter Dig | 0 | scene `hne_e0101` |
| `hne_e0101` | `343` | Special Charter Dig | 1 | scene `hne_e0100` or scene `pos_z0000` |

### What the scenes give

- `hne_a0700`, loaded in the Staging Shaft, is followed by story counter 1820, after Mjrn ([story counter
  values](story-counter-values.md)): the party find the Draklor search for magicite ore and meet Mjrn in the Mist
  ("The stench of humes. The stench of power.").
- `hne_b0100` and `hne_b0101` open the boss fight in Ore Separation and have no section 2 entries; `常駐監督.main` loads
  them in turn and then `pos_z0000`.
- `hne_b0102`, loaded after that fight, is followed by story counter 1900, after Rescue Mjrn, and by the jump to Fane
  of the Path (Eruyt Village), field `766`: Mjrn tells why she left the Wood, the stone set beside her is named as
  manufacted nethicite, and Penelo still carries the stone she was given. `常駐監督.main` takes the Manufacted Nethicite
  after the scene.
- `hne_e0100` and `hne_e0101` are the two scenes of the Esper fight in Special Charter Dig. `hne_e0101` gives the
  Esper of the map it plays on: in Special Charter Dig (field `733`) it adds Zodiark when the party does not hold it
  yet. The `items` cell lists every Esper id of that choice, `0xC012` to `0xC01E` and the Second Board id `0xC01F`
  ([Quickening and Esper list](../Battle-Actions/quickening-and-esper-list.md)).

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

- [Henne Mines scripts](henne-mines-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.
