[Home](../../README.md) / [Scripts and script commands](README.md) / Script binding lifecycle

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Script binding lifecycle: a model binding from the script that names it to its release and the slot's reuse | lifecycle | Scripts and script commands | The script machine | The stages of one of the 128 model-binding entries: find-or-create on the requested list, the request pump's load, the completion and the sub-resources that make it ready, the bind and attach that hold it, the release that retires it, the per-frame update that frees it, the pressure path, and the stamp that makes old handles stop working; each stage linked to the page that explains it. | 0x002EB540, 0x002EAE20, 0x002E25E0, 0x002E6700, 0x002EAD50, 0x002E4D20, 0x002EA6E0, 0x002E28E0, 0x002E3110, 0x002EAEB0, 0x002E65A0, 0x002E9360, 0x002E6D60 |

## What the player sees

When a scene gives a character a different body or hands an actor a prop, the scene can pause a moment while the
model loads. When nothing uses the model any more it is unloaded, and a later scene that names it loads it again.

## Stages

| Step | What happens | Where in the code |
|---|---|---|
| 1 | **Find or create.** A bind verb names a bound id. `0x002EB540` or `0x002EAE20` finds its entry on the live or the requested list, or pops a free one onto the requested list, and sets the caller's holder bit ([script name bindings](script-name-bindings.md#find-or-create-holders-and-the-reference-count)). | `0x002E25E0` |
| 2 | **Load.** The request pump `0x002E6700` sizes the model's file, takes a buffer and files the read; the entry moves to the live list ([script name bindings](script-name-bindings.md#loading-an-entry)). | `0x002EAD50` |
| 3 | **Ready.** The completion `0x002E4D20` registers the model with the render system, and `0x002EA6E0` loads up to three sub-resources; when they are in, the ready bit is set, which every wait tests ([script name bindings](script-name-bindings.md#loading-an-entry)). |   |
| 4 | **Held.** The bind `0x002E28E0` and the attach `0x002E3110` each add a reference ([script name bindings](script-name-bindings.md#the-bind-what-binding-a-model-to-an-actor-does), [script name bindings](script-name-bindings.md#the-attach-slots)). |   |
| 5 | **Let go.** When the holders and references are gone and the entry is not pinned, the re-lister `0x002EAEB0` moves it to the retired list, or, while it is still loading, marks the release to happen when the load completes ([script name bindings](script-name-bindings.md#find-or-create-holders-and-the-reference-count)). |   |
| 6 | **Freed.** The per-frame binding update `0x002E65A0` releases retired entries from the oldest: `0x002E9360` queues the entry's lanes for unload, releases its sub-resources and buffer, and pushes the entry on the free list ([script name bindings](script-name-bindings.md#the-per-frame-binding-update)). |   |
| 7 | **Under memory pressure.** When an allocation in arena 6 or 10 fails, `0x002E6D60` unloads one queued lane and releases the oldest retired entry before the arena compacts and retries ([script name bindings](script-name-bindings.md#the-per-frame-binding-update), [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md)). |   |
| 8 | **Reuse.** The stamp rises when the entry is retired and again when it is freed, so a handle given out before stops resolving ([script name bindings](script-name-bindings.md#the-handle-one-number-checked-before-use), [identifier spaces](../Engine-Core/identifier-spaces.md)). |   |

## Across transitions

- **An area unload** runs the per-frame binding update itself (`0x002628B0` is one of its callers), so retired
  entries are freed as the zone goes ([script name bindings](script-name-bindings.md#the-per-frame-binding-update),
  [changing areas](../World-Areas-And-Travel/changing-areas.md)).
- **A pinned entry** (pin bit `0x1` or `0x2`) is never released: when `--count <= 0` its count is clamped to 0
  instead, `count = 0` while `+0x19 & 3` is non-zero (`0x002EAF75`-`0x002EAF8C`;
  [script name bindings](script-name-bindings.md#find-or-create-holders-and-the-reference-count)).
- **A retired entry whose buffer handle is 0** is not passed to `0x002E9360`. It stays on the retired list while
  newer entries are released ahead of it¹; the first per-frame update that starts with such an
  entry at the head of the list nulls the head², so it ends on no list and its slot stays
  lost until the binding table is set up again
  ([script name bindings](script-name-bindings.md#the-per-frame-binding-update)).
- **The 129th binding** at once has no free entry, and both finders write through the null pointer
  ([native limits](../Engine-Core/native-limits.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E9419` |
| ² | `0x002E6653` |

</details>

## Related

- [Script name bindings](script-name-bindings.md): the binding table in full.
- [Model asset list](../Graphics/model-asset-list.md): what a bound id names.
- [Character render records](../Graphics/character-render-records.md): where the bound model is drawn from.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 75 calls with 17 other topics</summary>

**Characters and objects** (explained on [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md), [frame update order](../Engine-Core/frame-update-order.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](event-scenes.md), [actor record](../Characters-And-Objects/actor-record.md), [actor managers](../Characters-And-Objects/actor-managers.md), [native commands](native-commands.md), [debug menu](../Engine-Core/debug-menu.md), [script name bindings](script-name-bindings.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](event-scenes.md) (on event scenes) | calls | [`0x0025B070`](../Characters-And-Objects/actor-lifecycle.md) Actor system: release manager records (on actor lifecycle)<br>[`0x00263660`](../Characters-And-Objects/actor-managers.md) (on actor managers)<br>[`0x002695A0`](../World-Areas-And-Travel/save-and-teleport-crystals.md) (on save and teleport crystals)<br>[`0x0037B230`](event-scenes.md) (on event scenes)<br>[`0x003B6C20`](../Characters-And-Objects/actor-record.md) (on actor record)<br>[`0x003DDC20`](../Characters-And-Objects/actor-managers.md) (on actor managers)<br>[`0x003DE920`](event-scenes.md) (on event scenes) |
| [`0x002628B0`](event-scenes.md) (on event scenes) | is called by | [`0x0025BFB0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) |
| [`0x002E28E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | calls | [`0x0025AB30`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x00263FF0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |
| [`0x002E28E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | is called by | [`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x002E3110`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild) | is called by | [`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x002E65A0`](script-binding-lifecycle.md) | is called by | [`0x002628B0`](event-scenes.md) (on event scenes) |
| [`0x002EAE20`](script-binding-lifecycle.md) | is called by | [`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x002EB540`](script-name-bindings.md) (on script name bindings) | is called by | [`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |

**Sound and music** (explained on [music](../Sound-And-Music/music.md), [game over](../World-Areas-And-Travel/game-over.md), [script name bindings](script-name-bindings.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](event-scenes.md) (on event scenes) | calls | [`0x00360B50`](../Sound-And-Music/music.md) (on music)<br>[`0x00360DD0`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle)<br>[`0x003636A0`](../Sound-And-Music/map-sounds.md) (on map sounds) |
| [`0x002E9360`](script-binding-lifecycle.md) | calls | [`0x003A0F80`](../Sound-And-Music/sound-banks.md) (on sound banks) |

**Engine core** (explained on [game over](../World-Areas-And-Travel/game-over.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](event-scenes.md) (on event scenes) | calls | [`0x00229EE0`](../Graphics/effect-lifecycle.md) (on effect lifecycle) |
| [`0x002E65A0`](script-binding-lifecycle.md) | is called by | [`0x0022A770`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x0022AF50`](../Graphics/graphics-thread-handshake.md) (on graphics thread handshake)<br>[`0x0022B000`](../Graphics/graphics-thread-handshake.md) (on graphics thread handshake)<br>[`0x0022B6E0`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar)<br>[`0x0022B7E0`](../Graphics/graphics-thread-handshake.md) (on graphics thread handshake)<br>[`0x0022B8C0`](../Graphics/graphics-thread-handshake.md) (on graphics thread handshake)<br>[`0x0022BC20`](../Graphics/graphics-thread-handshake.md) (on graphics thread handshake) |

**Controls and input** (explained on [vibration](../Controls-And-Input/vibration.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](event-scenes.md) (on event scenes) | calls | [`0x0035B5D0`](../Controls-And-Input/vibration.md) (on vibration) |

**Movement and pathfinding** (explained on [frame update order](../Engine-Core/frame-update-order.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md), [script name bindings](script-name-bindings.md), [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md), [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](event-scenes.md) (on event scenes) | calls | [`0x00263560`](world-lock.md) (on world lock)<br>[`0x0026A1D0`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata)<br>[`0x00379070`](../World-Areas-And-Travel/doors-gates-and-map-changes.md) (on doors gates and map changes)<br>[`0x003791C0`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle)<br>[`0x003792D0`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle)<br>[`0x003DAA20`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x002E28E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | calls | [`0x00269E60`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00269F90`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering)<br>[`0x0026A370`](script-name-bindings.md) (on script name bindings)<br>[`0x0026AF40`](../Graphics/model-lifecycle.md) (on model lifecycle)<br>[`0x0026B2E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x002E3500`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x002E5C90`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering)<br>[`0x002E5E10`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering)<br>[`0x002E8E20`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x002EC3F0`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering) |
| [`0x002E3110`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild) | calls | [`0x002EC3F0`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering) |

**Party** (explained on [player movement](../Movement-And-Pathfinding/player-movement.md), [actor managers](../Characters-And-Objects/actor-managers.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](event-scenes.md) (on event scenes) | calls | [`0x00358B40`](../Movement-And-Pathfinding/player-movement.md) (on player movement)<br>[`0x00359200`](../Party/party-leader.md) (on party leader) |

**Graphics** (explained on [frame update order](../Engine-Core/frame-update-order.md), [verb table](verb-table.md), [party during scenes](party-during-scenes.md), [script name bindings](script-name-bindings.md), [battle verbs](battle-verbs.md), [party verbs](party-verbs.md), [game application](../Engine-Core/game-application.md), [add motion tables](../Graphics/add-motion-tables.md), [authored presentation commands](../Graphics/authored-presentation-commands.md), [bone trails](../Graphics/bone-trails.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](event-scenes.md) (on event scenes) | calls | [`0x002E65A0`](script-binding-lifecycle.md)<br>[`0x002E8CC0`](../Characters-And-Objects/actor-lifecycle.md) Character render system: refresh distance cull enable (on actor lifecycle)<br>[`0x003EB500`](verb-table.md) (on verb table)<br>[`0x003EB5F0`](verb-table.md) (on verb table) |
| [`0x002E28E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | calls | [`0x002E8FD0`](party-during-scenes.md) Actor: refresh presentation visibility (on party during scenes)<br>[`0x003E6150`](../Graphics/model-files-cm-ca.md) (on model files cm ca)<br>[`0x00426FA0`](../Graphics/character-render-records.md) (on character render records)<br>[`0x00427280`](party-verbs.md) (on party verbs)<br>[`0x0042FB80`](../Graphics/character-render-records.md) (on character render records) |
| [`0x002E3110`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild) | calls | [`0x002E8FD0`](party-during-scenes.md) Actor: refresh presentation visibility (on party during scenes)<br>[`0x002EDF90`](../Graphics/add-motion-tables.md) Character render: update add motion binding state (on add motion tables)<br>[`0x004288B0`](../Graphics/character-render-records.md) (on character render records)<br>[`0x0042F250`](../Menus-And-HUD/clan-primer.md) (on clan primer)<br>[`0x0042FB80`](../Graphics/character-render-records.md) (on character render records) |
| [`0x002E65A0`](script-binding-lifecycle.md) | calls | [`0x003DD4C0`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal) |
| [`0x002E6700`](script-name-bindings.md) (on script name bindings) | is called by | [`0x002E65A0`](script-binding-lifecycle.md) |
| [`0x002E9360`](script-binding-lifecycle.md) | is called by | [`0x002E65A0`](script-binding-lifecycle.md) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [script name bindings](script-name-bindings.md), [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](event-scenes.md) (on event scenes) | calls | [`0x0032E520`](../Graphics/effect-file-loading.md) (on effect file loading) |
| [`0x002E4D20`](script-name-bindings.md) (on script name bindings) | calls | [`0x00409090`](script-name-bindings.md) (on script name bindings) |
| [`0x002E6700`](script-name-bindings.md) (on script name bindings) | calls | [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x002EAD50`](script-binding-lifecycle.md) | calls | [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |

**Saving, loading and settings** (explained on [script name bindings](script-name-bindings.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](event-scenes.md) (on event scenes) | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields) |

**World, areas and travel** (explained on [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md), [ebp navigation icons](../EBP-Script-Files/ebp-navigation-icons.md), [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](event-scenes.md) (on event scenes) | calls | [`0x00378230`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x003DFA50`](../EBP-Script-Files/ebp-navigation-icons.md) (on ebp navigation icons)<br>[`0x003EAA00`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle) |
| [`0x002E28E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | calls | [`0x00377C20`](party-during-scenes.md) (on party during scenes) |

</details>
