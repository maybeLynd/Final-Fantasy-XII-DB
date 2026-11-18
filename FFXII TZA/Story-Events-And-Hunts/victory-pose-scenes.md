[Home](../../README.md) / [Story, events and hunts](README.md) / Victory pose scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Victory pose scenes: the scene, what it gives and the zone scripts that load it | reference | Story, events and hunts | Scenes and scripts by area / Scenes that recur through the story | The victory pose scene script pos_z0000: the Esper ids its own functions give, and the Trial Mode stages and story maps whose zone scripts load it. | 0x003529E0, 0x00351880, 0x0032FCA0, 0x00345080 |

## What it lists

The table [victory-pose-scenes.tsv](victory-pose-scenes.tsv) has one row for the scene script `pos_z0000` under
`plan_master/us/event`. No zone script shares its file-name prefix, so its `next` column is `-`; the
zone scripts that load it belong to other areas, and `loaded_by` names each.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `pos_z0000` | `427` | 139 zone scripts: the 100 Trial Mode stages and 39 maps of 23 regions | 0 | - |

### The scene

- Zone scripts load event 427 with `eventread` (`0x0E7`, `0x003529E0`) or `eventread_e8` (`0x0E8`, `0x00351880`);
  `0x0032FCA0` reads the scene from index `4n` of the event file table
  ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- In Trial Mode, every stage script's `トライアル監督.main` loads it. On the story maps the loading functions
  include `監督.main` (11 maps), `常駐監督.main`, `EventDirector.main` and `ボス登場.touch` (5 each).
- The scene has no text: its section 2 has no entries.
- Its `EFFECT.EFFECT_READ` holds `additem` (`0x2E5`, `0x00345080`) calls for the thirteen Esper ids `0xC012` to
  `0xC01E`, named on [Victory pose scripts](victory-pose-scripts.md).

### The story maps that load it

| Region | Maps |
|---|---:|
| Giruvegan; Necrohol of Nabudis; Pharos - First Ascent; Sochen Cave Palace; Stilshrine of Miriam; The Tomb of Raithwall | 3 each |
| Garamsythe Waterway; Henne Mines; Lhusu Mines; The Great Crystal | 2 each |
| Barheim Passage; Dalmasca Westersand; Dreadnought Leviathan; Golmore Jungle; Mosphoran Highwaste; Nam-Yensa Sandsea; Pharos - Second Ascent; Pharos - Subterra; Pharos - Third Ascent; Ridorana Cataract; The Feywood; The Salikawood; Zertinan Caverns | 1 each |

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event |
| `lines` | the number of entries in the scene's section 2 |
| `synopsis` | the `us` text of every non-empty entry; a scene with no non-empty entry: one sentence of what its script does |
| `items` | items the scene's own functions give or take, as `receives` and the item's name |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows when the loading script has the same file-name prefix; `-` here |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Victory pose scripts](victory-pose-scripts.md) - the function that gives the Espers, with their names.
- [Quickening and Esper list](../Battle-Actions/quickening-and-esper-list.md) - the Esper ids.
- [Scene rewards](scene-rewards.md) - every item a script gives.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0032FCA0` calls `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md).
- Resource: `0x0032FCA0` calls `0x002DF980`, `0x0032E400`, `0x0032E620`; `0x00351880` calls `0x001D6A70`; `0x003529E0` calls
  `0x001D6A70`; those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [startup constants](../Engine-Core/startup-constants.md),
  [event scenes](../Scripts-And-Script-Commands/event-scenes.md).
- Script VM: `0x00345080` calls `0x00267E10`, `0x00267F90`, `0x0026B4E0`; `0x00351880` calls `0x00267E10`; `0x003529E0` calls
  `0x00267E10`, `0x00267F90`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [native commands](../Scripts-And-Script-Commands/native-commands.md).
- World area: `0x0032FCA0` is called by `0x0032FC30`; those functions are documented on
  [debug menu](../Engine-Core/debug-menu.md).
