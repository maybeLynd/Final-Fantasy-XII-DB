[Home](../../README.md) / [Story, events and hunts](README.md) / Opening setup scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Opening setup scenes: the event script pre_z0000, how it is requested and what it sets | reference | Story, events and hunts | Scenes and scripts by area / Opening, ending and Trial Mode | The one event script of the pre group, pre_z0000 (event 212): the executable's preload and request of it, its lines, items and story values, and what follows it, in the form of the region scene pages. | 0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00 |

## What it lists

The table has one row per scene script of the `pre` group under `plan_master/us/event` that an event id names. Zone
scripts load scenes with `eventread` (`0x0E7`, `0x003529E0`) and `eventread_e8` (`0x0E8`, `0x00351880`), which `0x0032FCA0`
reads from index `4n` of the event file table ([event scenes](../Scripts-And-Script-Commands/event-scenes.md));
`pre_z0000` is requested by the executable instead.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `pre_z0000` | `212` | the field runtime pass `0x0025D9E0` | 0 | - |

### What the scenes give

- `pre_z0000` holds no text, gives no item, writes no story counter value and makes no story flag call. Its one
  function sets script globals from the story counter and calls `eventdispose` ([Opening setup
  scripts](opening-setup-scripts.md)).
- No `us` script names event 212 in `eventread` or `eventread_e8`, so its `loaded_by` cell names the field runtime
  pass `0x0025D9E0`, which requests it on manager 1 through `0x0032FC30` (`0x0025DAE8`, `0x0025DAED`), and `0x0032F430` preloads it
  once ([EBP script container](../EBP-Script-Files/ebp-script-container.md)).

### How the synopsis is taken

A scene's synopsis is its own text: every non-empty string of its section 2, in entry order, as the `us` tree ships
it. The scene's message verbs pass these entries to `mes` (`0x00348DF0`), which reads them from the scene's section 2
through `0x00264D60` ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

A scene with no non-empty entry has instead one sentence of what its script does, read from its steps
([Opening setup scripts](opening-setup-scripts.md)): its actors, camera shots, motions, effects, music and loads.

### What follows a scene

The loading function is read on from the scene's load call. Story counter writes and flag sets up to the next scene
load or `mapjump` (`0x00354D00`) count as written with the scene, and that next load or jump is what follows it. A jump
made by the scene script itself comes first.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event; for `pre_z0000`, the exe step that requests it |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a scene with no non-empty entry: one sentence of what its script does |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene or by its loading function after the load, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene or by its loading function after the load, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows: a later scene load or a `mapjump` target with its field id; `-` when the loading function does neither |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Opening setup scripts](opening-setup-scripts.md) - every observable function of the same scripts.
- [Story counter values](story-counter-values.md) - what each counter value marks.
- [Scene rewards](scene-rewards.md) - the items scenes give, across the game.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 69 calls with 20 other topics</summary>

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x0025D9E0` | calls | `0x0025B250`, `0x0025B600`, `0x0025B820`, `0x0025C170`, `0x00263660`, `0x00269860`, `0x003588B0`, `0x00358940`, `0x003DB280` |
| `0x0032FC30` | calls | `0x0032FCA0` |
| `0x0032FC30` | is called by | `0x0025D9E0` |
| `0x0032FCA0` | calls | `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0` |

**Characters and objects** (explained on [script requests](../Scripts-And-Script-Commands/script-requests.md), [field runtime](../Characters-And-Objects/field-runtime.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [frame update order](../Engine-Core/frame-update-order.md))

**Characters and objects** (explained on [actor record](../Characters-And-Objects/actor-record.md), [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

**Sound and music** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x0025D9E0` | calls | `0x00261F90` |

**Battle actions** (explained on [battle units](../Characters-And-Objects/battle-units.md))

| Function | | Functions |
|---|---|---|
| `0x0032FC30` | is called by | `0x00306BD0` |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00354D00` | calls | `0x00229EA0` |

**Gameplay** (explained on [field runtime](../Characters-And-Objects/field-runtime.md))

| Function | | Functions |
|---|---|---|
| `0x0025D9E0` | calls | `0x00234150` |

**Movement and pathfinding** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x0025D9E0` | calls | `0x0025DF00` |

**Party** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x0025D9E0` | calls | `0x003590D0` |

**Game files and data tables**

| Function | | Functions |
|---|---|---|
| `0x0032F430` | calls | `0x0032E400`, `0x0032E520`, `0x0032E620` |
| `0x0032FCA0` | calls | `0x002DF980`, `0x0032E400`, `0x0032E620` |
| `0x00351880` | calls | `0x001D6A70` |
| `0x003529E0` | calls | `0x001D6A70` |

**Game files and data tables** (explained on [startup constants](../Engine-Core/startup-constants.md), [debug menu](../Engine-Core/debug-menu.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

**Saving, loading and settings** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x0025D9E0` | calls | `0x002EF2B0`, `0x00583920` |

**Scripts and script commands**

| Function | | Functions |
|---|---|---|
| `0x00264D60` | is called by | `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`, `0x00354F20`, `0x003555F0`, `0x00356B70`, `0x0050EAB0` |
| `0x0032FC30` | is called by | `0x003522C0`, `0x00353080`, `0x00353590`, `0x0050D0C0` |
| `0x00348DF0` | calls | `0x00267E10` |
| `0x00348DF0` | is called by | `0x00349800` |
| `0x00351880` | calls | `0x00267E10` |
| `0x003529E0` | calls | `0x00267E10`, `0x00267F90` |
| `0x00354D00` | calls | `0x00267E10` |

**Scripts and script commands** (explained on [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

**Scripts and script commands** (explained on [ebp script container](../EBP-Script-Files/ebp-script-container.md), [debug menu](../Engine-Core/debug-menu.md), [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md))

**World, areas and travel** (explained on [actor record fields](../Characters-And-Objects/actor-record-fields.md), [force fight mode](../Engine-Core/force-fight-mode.md))

| Function | | Functions |
|---|---|---|
| `0x0025D9E0` | calls | `0x0025E400` |
| `0x0032F430` | is called by | `0x00266D10` |

**World, areas and travel**

| Function | | Functions |
|---|---|---|
| `0x0025D9E0` | calls | `0x002677B0`, `0x003148D0`, `0x003148F0`, `0x00314DA0`, `0x0032FC30`, `0x00377DB0`, `0x003EAA70` |
| `0x0025D9E0` | is called by | `0x00314020` |
| `0x0032F430` | calls | `0x003EA6B0` |
| `0x0032FC30` | calls | `0x0025D4D0`, `0x003319D0`, `0x003EA6E0` |
| `0x0032FC30` | is called by | `0x00314020` |
| `0x0032FCA0` | is called by | `0x0032FC30` |
| `0x003522C0` | calls | `0x0032FC30` |
| `0x00353080` | calls | `0x0032FC30` |

**World, areas and travel** (explained on [field runtime](../Characters-And-Objects/field-runtime.md), [script variables](../Scripts-And-Script-Commands/script-variables.md), [party control modes](../Engine-Core/party-control-modes.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md))

**World, areas and travel** (explained on [debug menu](../Engine-Core/debug-menu.md), [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [debug logging](../Engine-Core/debug-logging.md))

**World, areas and travel** (explained on [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md), [frame update order](../Engine-Core/frame-update-order.md))

</details>
