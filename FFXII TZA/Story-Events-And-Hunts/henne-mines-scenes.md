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

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Henne Mines scripts](henne-mines-scripts.md)): its actors, camera shots, motions, effects, music and loads.

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
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Henne Mines scripts](henne-mines-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0032FCA0` calls `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md).
- Core runtime: `0x00354D00` calls `0x00229EA0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Resource: `0x0032FCA0` calls `0x002DF980`, `0x0032E400`, `0x0032E620`; `0x00351880` calls `0x001D6A70`; `0x003529E0` calls
  `0x001D6A70`; those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [startup constants](../Engine-Core/startup-constants.md),
  [event scenes](../Scripts-And-Script-Commands/event-scenes.md).
- Script VM: `0x00264D60` is called by `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`,
  `0x00354F20`, `0x003555F0`, `0x00356B70`, `0x0050EAB0`; `0x00348DF0` calls `0x00267E10`; `0x00348DF0` is called by `0x00349800`;
  `0x00351880` calls `0x00267E10`; `0x003529E0` calls `0x00267E10`, `0x00267F90`; `0x00354D00` calls `0x00267E10`.
- Script VM: those functions are documented on [archades scenes](archades-scenes.md),
  [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md),
  [npc names](../Characters-And-Objects/npc-names.md),
  [force fight mode](../Engine-Core/force-fight-mode.md); and on
  [native commands](../Scripts-And-Script-Commands/native-commands.md).
- World area: `0x0032FCA0` is called by `0x0032FC30`; `0x003522C0` calls `0x0032FC30`; `0x00353080` calls `0x0032FC30`; those
  functions are documented on [debug menu](../Engine-Core/debug-menu.md).
