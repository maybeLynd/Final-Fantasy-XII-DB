[Home](../../README.md) / [Story, events and hunts](README.md) / Jahara scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Jahara scenes: each story scene with its dialogue and the zone that loads it | reference | Story, events and hunts | Scenes and scripts by area / Ozmone Plain and Golmore Jungle | The three scene scripts of Jahara, the garif village: the zone function that loads each one and every line it holds in the game's own words, from Larsa's invitation to Mt Bur-Omisace to the legend of the nethicite. | 0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00 |

## What it lists

The table has one row per scene script of Jahara under `plan_master/us/event`. The zone scripts load
them with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`); the end handlers `0x00353080` and
`0x003522C0` queue the load of event `n`, which `0x0032FCA0` reads from index `4n` of the event file table
([event scenes](../Scripts-And-Script-Commands/event-scenes.md),
[zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `glf_a0200` | `327` | Lull of the Land | 32 | - |
| `glf_a0300` | `325` | The Elderknoll | 28 | - |
| `glf_z0100` | `326` | field `858` (`glf_z01`) | 62 | - |

### What the scenes give

- No scene gives an item, changes the party or writes the story counter; the counter values of the village are
  written by the zone functions on [Jahara scripts](jahara-scripts.md).
- `glf_z0100` is loaded on field `858` (`glf_z01`), which the Elderknoll function `常駐イベント.促し` jumps to after
  writing 1640; the field then jumps back to Lull of the Land.
- `glf_a0200` holds "Holy Mt Bur-Omisace stands at the northern end of the Jagd Ramooda." and ends with "Any
  self-respecting leading man would do the same.", and `glf_a0300` holds the account of the nethicite and the
  Dynast-King.

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
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Jahara scripts](jahara-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Story flag ids](story-flag-ids.md) - what each flag opens.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 29 calls with 6 other topics</summary>

**Characters and objects** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

| Function | | Functions |
|---|---|---|
| `0x0032FCA0` | calls | `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0` |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00354D00` | calls | `0x00229EA0` |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

| Function | | Functions |
|---|---|---|
| `0x0032FCA0` | calls | `0x002DF980`, `0x0032E400`, `0x0032E620` |
| `0x00351880` | calls | `0x001D6A70` |
| `0x003529E0` | calls | `0x001D6A70` |

**Scripts and script commands**

| Function | | Functions |
|---|---|---|
| `0x00264D60` | is called by | `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`, `0x00354F20`, `0x003555F0`, `0x00356B70`, `0x0050EAB0` |
| `0x00348DF0` | calls | `0x00267E10` |
| `0x00348DF0` | is called by | `0x00349800` |
| `0x00351880` | calls | `0x00267E10` |
| `0x003529E0` | calls | `0x00267E10`, `0x00267F90` |
| `0x00354D00` | calls | `0x00267E10` |

**Scripts and script commands** (explained on [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md))

**World, areas and travel** (explained on [debug menu](../Engine-Core/debug-menu.md))

| Function | | Functions |
|---|---|---|
| `0x0032FCA0` | is called by | `0x0032FC30` |
| `0x003522C0` | calls | `0x0032FC30` |
| `0x00353080` | calls | `0x0032FC30` |

</details>
