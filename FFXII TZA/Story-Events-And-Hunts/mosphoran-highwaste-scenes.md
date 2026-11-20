[Home](../../README.md) / [Story, events and hunts](README.md) / Mosphoran Highwaste scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Mosphoran Highwaste scenes: each story scene with its dialogue, rewards and what follows | reference | Story, events and hunts | Scenes and scripts by area / Nalbina and the Mosphoran Highwaste | The two scene scripts of Mosphoran Highwaste that zone scripts load: the zone function that loads each one, every line it holds in the game's own words, the Esper it gives, and the scene that follows. | 0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00 |

## What it lists

The table has one row per scene script of Mosphoran Highwaste under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `mnt_c0100` | `130` | Empyrean Seat | 0 | scene `mnt_c0101` |
| `mnt_c0101` | `131` | Empyrean Seat | 1 | scene `mnt_c0100` or scene `pos_z0000` |

### What the scenes give

- `mnt_c0100` and `mnt_c0101` are the two scenes of the Esper fight on Empyrean Seat; `監督.main` loads them in turn and
  then `pos_z0000`. `mnt_c0100` has no section 2 entries, and the one entry of `mnt_c0101` is an empty string.
- `mnt_c0101` gives the Esper of the map it plays on: its `監督.main` picks the Esper by the current map, and on
  Empyrean Seat (field `223`) adds Exodus when the party does not hold it yet. The `items` cell lists every Esper id
  of that choice, `0xC012` to `0xC01E` and the Second Board id `0xC01F` ([Quickening and Esper
  list](../Battle-Actions/quickening-and-esper-list.md)).

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes`¹, which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00348DF0` |

</details>

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Mosphoran Highwaste scripts](mosphoran-highwaste-scripts.md)): its actors, camera shots, motions, effects, music and loads.

### What follows a scene

The loading function is read on from the scene's load call. Story counter writes and flag sets up to the next scene
load or `mapjump`¹ count as written with the scene, and that next load or jump is what follows it. A jump
made by the scene script itself comes first.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00354D00` |

</details>

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

- [Mosphoran Highwaste scripts](mosphoran-highwaste-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 29 calls with 6 other topics</summary>

**Characters and objects** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032ED80`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00229EA0`](../Graphics/effect-drawing.md) (on effect drawing) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002DF980`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |

**Scripts and script commands** (explained on [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264D60`](../Menus-And-HUD/aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | is called by | [`0x00348DF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x00352A50`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00352EC0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003534F0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003545B0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00354F20`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x003555F0`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x00356B70`](../Characters-And-Objects/npc-names.md) (on npc names)<br>[`0x0050EAB0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | is called by | [`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |

**World, areas and travel** (explained on [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | is called by | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |
| [`0x003522C0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |
| [`0x00353080`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |

</details>
