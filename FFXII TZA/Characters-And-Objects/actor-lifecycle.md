[Home](../../README.md) / [Characters and objects](README.md) / Actor lifecycle

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Actor lifecycle: an actor record from its manager's bind to the release, and when its handle stops working | lifecycle | Characters and objects | Field actors | The stages of an actor: the manager slot's bind of its definition payload, the record pool built from the payload's sequences, each record's initialiser, the handle, the battle unit a battle actor gets, the holds a time stop or the world lock put on it, the manager's two-phase release with the per-slot state it resets, and the discriminator that makes old handles stop resolving; each stage linked to the page that explains it. | 0x0026C8C0, 0x002679F0, 0x00266530, 0x003589B0, 0x003588B0, 0x002628B0, 0x0025B070, 0x002659D0 |

## What the player sees

When an area or a scene loads, its characters and objects appear, run their scripts and react; in battle they
fight. When the party leaves the area or the scene ends, they all disappear together.

## Stages

| Step | What happens | Where in the code |
|---|---|---|
| 1 | **Bind.** When a manager slot's definition payload has loaded, `0x0026C8C0` binds it to the slot; slot 0, the zone's, also resets the field state that belongs to it ([actor managers](actor-managers.md#the-bind)). |   |
| 2 | **Pool.** `0x002679F0` builds the slot's record pool from the payload's sequences, one block holding the pointer table and every record ([actor record](actor-record.md#the-pool)). |   |
| 3 | **Initialise.** `0x00266530` fills each record and binds its script entry ([actor record](actor-record.md#the-initialiser)). |   |
| 4 | **Handle.** `0x003589B0` names a record by its index, its manager slot and its discriminator, and `0x003588B0` resolves the handle back ([battle units](battle-units.md#the-handle), [identifier spaces](../Engine-Core/identifier-spaces.md)). |   |
| 5 | **Run.** Each frame the records' scripts run in the frame's update order ([script interpreter](../Scripts-And-Script-Commands/script-interpreter.md), [frame update order](../Engine-Core/frame-update-order.md)). |   |
| 6 | **Battle unit.** A record that fights gets a battle unit from its definition ([battle unit construction](battle-unit-construction.md), [battle units](battle-units.md)). |   |
| 7 | **Hold.** A time stop or the world lock holds the record's script while the request is active ([time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [world lock](../Scripts-And-Script-Commands/world-lock.md)). |   |
| 8 | **Release.** On every bound slot but 4 the manager's teardown `0x002628B0` runs `0x0025B070`, which ends the movement job of each class-1 or class-3 record in the slot's two record ranges, runs the per-record teardown and releases the battle units. On every slot it then frees the record block; every record address is valid only until then ([actor record](actor-record.md#release)). | `0x00262D96`-`0x00262DA4` |
| 9 | **The slot's other state.** The same teardown resets the state other systems keep per slot: skips, voices, the summon group, event sounds and script effect slots ([actor record](actor-record.md#what-else-the-teardown-resets)). |   |
| 10 | **New handle.** `0x002659D0` advances a record's discriminator, so a handle taken before stops resolving. It runs for the verb `changeentryid` and through `0x003220E0` (`0x00322050`, `0x00322080`, the latter for `incentryid`). A rebuilt pool restarts every discriminator at 1 ([battle units](battle-units.md#the-handle)). |   |

## Across transitions

- **An area change** requests managers 0 to 3 for reinitialisation, and the next tick tears them down before any
  actor runs ([changing areas](../World-Areas-And-Travel/changing-areas.md)).
- **A scene** loads into manager 1, 2 or 3 through the same loader and is torn down when it is disposed
  ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- **Party members captured by a scene** are bound to a scene record until the scene releases them
  ([party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md)).

## Related

- [Actor managers](actor-managers.md): the slots and the bind.
- [Actor record](actor-record.md): the record, its pool and its release.
- [Battle units](battle-units.md): the battle side of a record.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 66 calls with 20 other topics</summary>

**Sound and music** (explained on [music](../Sound-And-Music/music.md), [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00360B50`](../Sound-And-Music/music.md) (on music)<br>[`0x00360DD0`](actor-lifecycle.md)<br>[`0x003636A0`](../Sound-And-Music/map-sounds.md) (on map sounds) |

**Battle actions** (explained on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) | is called by | [`0x00319F50`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle actor timeline event (on ko and game over)<br>[`0x00325260`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle action timeline event (on ko and game over) |

**Engine core** (explained on [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00229EE0`](../Graphics/effect-lifecycle.md) (on effect lifecycle) |

**Gameplay** (explained on [bestiary](../Enemy-Spawning/bestiary.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) | is called by | [`0x0031ADB0`](../Movement-And-Pathfinding/animation-driven-movement.md) (on animation driven movement) |

**Controls and input** (explained on [vibration](../Controls-And-Input/vibration.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0035B5D0`](../Controls-And-Input/vibration.md) (on vibration) |

**Movement and pathfinding** (explained on [actor record](actor-record.md), [frame update order](../Engine-Core/frame-update-order.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md), [actor record fields](actor-record-fields.md), [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md), [world lock](../Scripts-And-Script-Commands/world-lock.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0025B070`](actor-lifecycle.md) Actor system: release manager records | calls | [`0x002E3D00`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00263560`](../Scripts-And-Script-Commands/world-lock.md) (on world lock)<br>[`0x0026A1D0`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata)<br>[`0x00379070`](../World-Areas-And-Travel/doors-gates-and-map-changes.md) (on doors gates and map changes)<br>[`0x003791C0`](actor-lifecycle.md)<br>[`0x003792D0`](actor-lifecycle.md)<br>[`0x003DAA20`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x00266530`](actor-record.md) Actor storage: initialize record (on actor record) | calls | [`0x00265FF0`](actor-record-fields.md) (on actor record fields)<br>[`0x00268380`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |
| [`0x0026C8C0`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor manager: bind loaded definition payload (on character se tables chse) | calls | [`0x0026D6F0`](../Scripts-And-Script-Commands/world-lock.md) Movement: set requested speed (on world lock) |
| [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) | is called by | [`0x002E5610`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Movement: integrate position and measure displacement (on heading speed to position delta)<br>[`0x002EBFA0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock) |

**Party** (explained on [player movement](../Movement-And-Pathfinding/player-movement.md), [actor managers](actor-managers.md), [frame update order](../Engine-Core/frame-update-order.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00358B40`](../Movement-And-Pathfinding/player-movement.md) (on player movement)<br>[`0x00359200`](../Party/party-leader.md) (on party leader) |
| [`0x0026C8C0`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor manager: bind loaded definition payload (on character se tables chse) | calls | [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00359200`](../Party/party-leader.md) (on party leader) |
| [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) | is called by | [`0x00269C70`](../Party/party-members.md) (on party members)<br>[`0x00326500`](../Party/party-leader.md) Party focus: select and request default actor (on party leader)<br>[`0x00353530`](../Movement-And-Pathfinding/player-movement.md) (on player movement)<br>[`0x0050C610`](../Party/party-leader.md) (on party leader)<br>[`0x0050D2F0`](actor-lifecycle.md) |

**Graphics** (explained on [frame update order](../Engine-Core/frame-update-order.md), [verb table](../Scripts-And-Script-Commands/verb-table.md), [actor managers](actor-managers.md), [authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md), [effect element runtime](../Graphics/effect-element-runtime.md), [effect element types](../Graphics/effect-element-types.md), [battle numbers](../Menus-And-HUD/battle-numbers.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x002E65A0`](../Scripts-And-Script-Commands/script-binding-lifecycle.md) (on script binding lifecycle)<br>[`0x002E8CC0`](actor-lifecycle.md) Character render system: refresh distance cull enable<br>[`0x003EB500`](../Scripts-And-Script-Commands/verb-table.md) (on verb table)<br>[`0x003EB5F0`](../Scripts-And-Script-Commands/verb-table.md) (on verb table) |
| [`0x0026C8C0`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor manager: bind loaded definition payload (on character se tables chse) | calls | [`0x002E83A0`](../Graphics/character-fades.md) Character render system: set fade width (on character fades)<br>[`0x002EBC30`](../Graphics/character-fades.md) Character render system: set fade start distance (on character fades)<br>[`0x002EDA30`](actor-lifecycle.md)<br>[`0x002EDA40`](actor-lifecycle.md)<br>[`0x002EDA50`](actor-lifecycle.md)<br>[`0x002EDA60`](actor-lifecycle.md)<br>[`0x002EDA70`](actor-lifecycle.md)<br>[`0x002EDA80`](actor-lifecycle.md) |
| [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) | is called by | [`0x003A4290`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x003A56F0`](../Graphics/effect-element-runtime.md) (on effect element runtime)<br>[`0x00465120`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00465690`](../Graphics/lens-flares.md) (on lens flares)<br>[`0x00506700`](../Menus-And-HUD/battle-numbers.md) (on battle numbers) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0032E520`](../Graphics/effect-file-loading.md) (on effect file loading) |

**Saving, loading and settings** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields) |
| [`0x0026C8C0`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor manager: bind loaded definition payload (on character se tables chse) | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields) |

**Scripts and script commands** (explained on [effect anchors and targets](../Graphics/effect-anchors-and-targets.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [actor record](actor-record.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) | is called by | [`0x00342150`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00342D40`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x003438F0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00349C90`](actor-lifecycle.md)<br>[`0x0034B5D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x0034BB80`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00352270`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00352940`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00354F20`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x003555F0`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x00357620`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x0050C7A0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |

**Story, events and hunts** (explained on [actor managers](actor-managers.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0026C8C0`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor manager: bind loaded definition payload (on character se tables chse) | calls | [`0x00377440`](../Story-Events-And-Hunts/event-memory.md) (on event memory) |

**World, areas and travel** (explained on [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md), [ebp navigation icons](../EBP-Script-Files/ebp-navigation-icons.md), [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00378230`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x003DFA50`](../EBP-Script-Files/ebp-navigation-icons.md) (on ebp navigation icons)<br>[`0x003EAA00`](actor-lifecycle.md) |
| [`0x0026C8C0`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor manager: bind loaded definition payload (on character se tables chse) | calls | [`0x0026DB30`](../World-Areas-And-Travel/save-and-teleport-crystals.md) World persistence: reset banks for field transition (on save and teleport crystals) |

</details>

---

[← Actor managers](actor-managers.md) | [Field runtime →](field-runtime.md)
