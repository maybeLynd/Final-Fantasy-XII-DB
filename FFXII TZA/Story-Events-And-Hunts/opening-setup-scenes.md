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
  pass `0x0025D9E0`, which requests it on manager 1 through `0x0032FC30`¹, and `0x0032F430` preloads it
  once ([EBP script container](../EBP-Script-Files/ebp-script-container.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0025DAE8`, `0x0025DAED` |

</details>

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
([Opening setup scripts](opening-setup-scripts.md)): its actors, camera shots, motions, effects, music and loads.

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

**Characters and objects** (explained on [script requests](../Scripts-And-Script-Commands/script-requests.md), [field runtime](../Characters-And-Objects/field-runtime.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [frame update order](../Engine-Core/frame-update-order.md), [actor record](../Characters-And-Objects/actor-record.md), [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0025D9E0`](opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) | calls | [`0x0025B250`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0025B600`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0025B820`](../Characters-And-Objects/field-runtime.md) (on field runtime)<br>[`0x0025C170`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x00263660`](../Characters-And-Objects/actor-managers.md) (on actor managers)<br>[`0x00269860`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record)<br>[`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes)<br>[`0x003DB280`](../Characters-And-Objects/actor-record.md) (on actor record) |
| [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) | calls | [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) |
| [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) | is called by | [`0x0025D9E0`](opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) |
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032ED80`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |

**Sound and music** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0025D9E0`](opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) | calls | [`0x00261F90`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships) |

**Battle actions** (explained on [battle units](../Characters-And-Objects/battle-units.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) | is called by | [`0x00306BD0`](summons-scenes.md) Battle action: initialize global special sequence mode (on summons scenes) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00229EA0`](../Graphics/effect-drawing.md) (on effect drawing) |

**Gameplay** (explained on [field runtime](../Characters-And-Objects/field-runtime.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0025D9E0`](opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) | calls | [`0x00234150`](../Party/party-slots.md) (on party slots) |

**Movement and pathfinding** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0025D9E0`](opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) | calls | [`0x0025DF00`](../Characters-And-Objects/field-runtime.md) World actor: update runtime and script execution state (on field runtime) |

**Party** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0025D9E0`](opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) | calls | [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |

**Game files and data tables** (explained on [startup constants](../Engine-Core/startup-constants.md), [debug menu](../Engine-Core/debug-menu.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032F430`](opening-setup-scenes.md) | calls | [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E520`](../Graphics/effect-file-loading.md) (on effect file loading)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002DF980`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |

**Saving, loading and settings** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0025D9E0`](opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields)<br>[`0x00583920`](../Saving-Loading-And-Settings/saving-and-loading-transaction.md) (on saving and loading transaction) |

**Scripts and script commands** (explained on [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md), [ebp script container](../EBP-Script-Files/ebp-script-container.md), [debug menu](../Engine-Core/debug-menu.md), [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264D60`](../Menus-And-HUD/aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | is called by | [`0x00348DF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x00352A50`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00352EC0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003534F0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003545B0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00354F20`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x003555F0`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x00356B70`](../Characters-And-Objects/npc-names.md) (on npc names)<br>[`0x0050EAB0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections) |
| [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) | is called by | [`0x003522C0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x00353080`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x00353590`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x0050D0C0`](../Engine-Core/debug-menu.md) (on debug menu) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | is called by | [`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |

**World, areas and travel** (explained on [actor record fields](../Characters-And-Objects/actor-record-fields.md), [force fight mode](../Engine-Core/force-fight-mode.md), [field runtime](../Characters-And-Objects/field-runtime.md), [script variables](../Scripts-And-Script-Commands/script-variables.md), [party control modes](../Engine-Core/party-control-modes.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [debug menu](../Engine-Core/debug-menu.md), [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [debug logging](../Engine-Core/debug-logging.md), [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0025D9E0`](opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) | calls | [`0x0025E400`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x0032F430`](opening-setup-scenes.md) | is called by | [`0x00266D10`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x0025D9E0`](opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) | calls | [`0x002677B0`](../Characters-And-Objects/field-runtime.md) (on field runtime)<br>[`0x003148D0`](../World-Areas-And-Travel/save-and-teleport-crystals.md) World transition: get options (on save and teleport crystals)<br>[`0x003148F0`](../World-Areas-And-Travel/treasure-chests.md) World transition: get active or pending field id (on treasure chests)<br>[`0x00314DA0`](../Saving-Loading-And-Settings/save-data-fields.md) World transition: set options (on save data fields)<br>[`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes)<br>[`0x00377DB0`](opening-setup-scripts.md) (on opening setup scripts)<br>[`0x003EAA70`](../Sound-And-Music/sound-banks.md) (on sound banks) |
| [`0x0025D9E0`](opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) | is called by | [`0x00314020`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |
| [`0x0032F430`](opening-setup-scenes.md) | calls | [`0x003EA6B0`](../Game-Files-And-Data-Tables/ard-area-battle-data.md) (on ard area battle data) |
| [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) | calls | [`0x0025D4D0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x003319D0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x003EA6E0`](opening-setup-scripts.md) (on opening setup scripts) |
| [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) | is called by | [`0x00314020`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | is called by | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |
| [`0x003522C0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |
| [`0x00353080`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |

</details>
