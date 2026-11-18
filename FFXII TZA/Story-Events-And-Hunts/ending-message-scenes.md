[Home](../../README.md) / [Story, events and hunts](README.md) / Ending message scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Ending message scenes: the scene with its text and the script that loads it | reference | Story, events and hunts | Scenes and scripts by area / Opening, ending and Trial Mode | The ending message scene script msg_z0001: every line it holds in the game's own words, what it gives and writes, and the Sky Fortress Bahamut zone function that loads it. | 0x003529E0, 0x00353080, 0x0032FCA0, 0x00348DF0, 0x00264D60 |

## What it lists

The table [ending-message-scenes.tsv](ending-message-scenes.tsv) has one row for the scene script `msg_z0001` under
`plan_master/us/event`. No zone script shares its file-name prefix, so its `next` column is `-`; the
zone script that loads it belongs to Sky Fortress Bahamut, and `loaded_by` names it.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `msg_z0001` | `399` | Cannon Superstructure (Sky Fortress Bahamut), `bhm_d01` `ボス監督.main` | 32 | - |

### The scene

- `ボス監督.main` of the Cannon Superstructure loads event 399 with `eventread` (`0x0E7`, `0x003529E0`); the end handler
  `0x00353080` queues the load, which `0x0032FCA0` reads from index `4n` of the event file table
  ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- The text opens "It's hard to believe a year has passed so quickly." and tells of Ashe's coronation next month,
  Larsa and Basch ("Lose Larsa and we lose the Empire."), and the Strahl, whose owner has taken her back.
- It closes "I'll be going too, of course. / Every good sky pirate needs a partner, right?", followed by the `Skip`
  prompt.
- The scene gives no items or party members and writes no story flag or counter value.

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)). Entries 0 and 22 are
empty, so the synopsis holds 30 of the 32 entries.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / ` |
| `items` | items the scene's own functions give or take, by name |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows when the loading script has the same file-name prefix; `-` here |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Ending message scripts](ending-message-scripts.md) - the function that shows each line.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
- [Story counter values](story-counter-values.md) - what each counter value marks.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 24 calls with 5 other topics</summary>

**Characters and objects** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

| Function | | Functions |
|---|---|---|
| `0x0032FCA0` | calls | `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0` |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

| Function | | Functions |
|---|---|---|
| `0x0032FCA0` | calls | `0x002DF980`, `0x0032E400`, `0x0032E620` |
| `0x003529E0` | calls | `0x001D6A70` |

**Scripts and script commands**

| Function | | Functions |
|---|---|---|
| `0x00264D60` | is called by | `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`, `0x00354F20`, `0x003555F0`, `0x00356B70`, `0x0050EAB0` |
| `0x00348DF0` | calls | `0x00267E10` |
| `0x00348DF0` | is called by | `0x00349800` |
| `0x003529E0` | calls | `0x00267E10`, `0x00267F90` |

**Scripts and script commands** (explained on [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md))

**World, areas and travel** (explained on [debug menu](../Engine-Core/debug-menu.md))

| Function | | Functions |
|---|---|---|
| `0x0032FCA0` | is called by | `0x0032FC30` |
| `0x00353080` | calls | `0x0032FC30` |

</details>
