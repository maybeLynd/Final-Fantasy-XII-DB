[Home](../../README.md) / [Graphics](README.md) / Effect lifecycle

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Effect lifecycle: from the request that names an effect to its release, and what an area change ends | lifecycle | Graphics | Visual effects / Effect Files | The stages an effect passes through: the request that names it, the file load, the instance, its start, the per-step update and per-frame draw, the hold a time stop puts on it, the restart of a looping instance, its end, and the release of its elements, its file and its handle, with what an area change and a return to the title end; each stage linked to the page that explains it. | 0x003B02A0, 0x0024B270, 0x0024B9B0, 0x003A74F0, 0x003A7050, 0x003A7300, 0x0024C550, 0x0024E910, 0x002628B0, 0x003601D0 |

## What the player sees

A spell or ability effect appears when it is asked for, plays out over its frames, can loop, freezes while time is
stopped, and disappears when it ends or when the party leaves the area.

## Stages

| Step | What happens | Where in the code |
|---|---|---|
| 1 | **Request.** An ability or event names a numbered effect for an owner and its targets, or an event script reads one into a script effect slot ([effects on actors and scripts](effects-on-actors-and-scripts.md)). | `0x003B02A0` |
| 2 | **Loading.** A battle effect is read into one of the 48 battle effect slots, and other effects into the queue of loaded files, where a file can be shared ([effect file loading](effect-file-loading.md)). |   |
| 3 | **Instance.** `0x0024B270` makes the `0x3B0`-byte effect instance in its kind's list, with an empty emitter list. Its emitters and their elements come later, through `0x003A8AE0`, from the events of its timeline tracks and the spawn slots of its elements ([effect element runtime](effect-element-runtime.md#instances-emitters-and-elements)). | `0x003A8900` |
| 4 | **Start.** In state 2 or 8 the step starts the instance and moves it to state 1 ([effect element runtime](effect-element-runtime.md#starting-and-ending-an-instance)). `0x003A74F0` also runs from state 4 (step 8) and from the signal `0x0024FE70`. | `0x003A74F0`<br>`0x0024FEC7` |
| 5 | **Update.** Each simulation step updates the instance: the emitter step, births, the base update, the cull, and child emitters ([effect element runtime](effect-element-runtime.md#the-update-pass)). |   |
| 6 | **Draw.** Each frame draws the instance in its display layer's pass ([effect drawing](effect-drawing.md#the-six-display-layers)). |   |
| 7 | **Hold.** While a time stop holds the instance's owner, bit `0x2` of `+0x368` limits each step to two calls, and the instance stands still ([effect element runtime](effect-element-runtime.md#the-effect-teardown), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md)). |   |
| 8 | **Restart.** An instance in state 4 starts again and goes to state 5. One in state 6 runs its update and also goes to state 5: when the update returns 0 it is ended first, and the 4 stored at `0x0024BE36` is overwritten by the 5 at `0x0024BE3D` ([effect element runtime](effect-element-runtime.md#starting-and-ending-an-instance)).<br>• State 5 puts the instance back in state 1 and lowers the count in bits `0xF0` of `+0x378`, 0 wrapping to `0xF`; it stays in state 5 while `0x001EDDA0` answers non-zero and the count is 0. | `0x003A74F0`, `0x0024BDB3`<br>`0x0024BDB8`<br>`0x0024BE11`-`0x0024BE28`<br>`0x003A7300`, `0x0024BE31`<br>`0x0024BDBD`-`0x0024BE08` |
| 9 | **End.** In state 1, an update that returns 0 ends the instance: `0x003A7300` frees its players and hands each non-zero handle at `+0x110`–`+0x11C` to `0x002FCB60` through the one-jump `0x002FC340`, clearing it ([effect element runtime](effect-element-runtime.md#starting-and-ending-an-instance)).<br>• With bit `0x1` of `+0x368` clear the instance then goes to state 8 and starts again on its next step.<br>• With the bit set, a kind-3 instance goes to state 7 and a kind other than 2, 3 and 7 to state 3. A kind-2 or kind-7 instance goes to state 3 when the high nibble of `+0x16` of its `0x600` record `+0x373` is 0 or equals the low nibble of `+0x378`, else to state 7. | `0x003A7300`, `0x0024BC23`<br>`0x003A7360`<br>`0x003A730A`-`0x003A733A`<br>`0x0024BC32`, `0x0024BCBF`-`0x0024BCD6`<br>`0x0024BC41`-`0x0024BC59`<br>`0x0024BC6A`-`0x0024BCB4` |
| 10 | **Release.** A released element goes back on its emitter's free list `+0x120` ([effect element runtime](effect-element-runtime.md#the-cull-the-release-and-the-spawn-slots)). An instance its owner lets go is queued on the instance free list `0x02092170` and freed on a later frame ([effect element runtime](effect-element-runtime.md#the-free-list)). |   |
| 11 | **Group and file release.** `0x0024C550` frees a group's contexts and instances, after clearing the owner table of kinds 1 and 5 to 9, and a loaded file is released unless it is kept ([effect element runtime](effect-element-runtime.md#emptying-a-group), [effect file loading](effect-file-loading.md#filing-sharing-and-releasing-a-loaded-file)). | `0x0024C569`-`0x0024C594` |
| 12 | **Reuse.** A slot that is used again gets a new id, so a handle kept from before names nothing ([resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md), [identifier spaces](../Engine-Core/identifier-spaces.md)). |   |

## Across transitions

- **An area change or a return to the title.** The area unload `0x002628B0` and the title-return reset `0x003601D0` run
  the effect teardown `0x0024E910`: every battle effect, model effect and numbered request ends, the map effect bank is
  disposed, and every loaded file that is not kept is released
  ([effect element runtime](effect-element-runtime.md#the-effect-teardown),
  [changing areas](../World-Areas-And-Travel/changing-areas.md)).
- **The rest of the teardown.** `0x0024E910` also sets the group mask `0x02092160` to `0x3FF`, releases the time-stop hold
  of the model effects and the numbered requests¹, and ends in the motion blur and cut-in
  clears (`0x0024E96B`–`0x0024EA0B`; [effect element runtime](effect-element-runtime.md#the-effect-teardown)).
- **A loaded file kept by its flag** (`+0x20` bit `0x1`) survives the teardown
  ([effect file loading](effect-file-loading.md#filing-sharing-and-releasing-a-loaded-file)).
- **A time stop's end** releases every held instance, so all of them move again at once
  ([effect element runtime](effect-element-runtime.md#the-effect-teardown)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B3B50`, `0x003B1130` |

</details>

## Related

- [Effect element runtime](effect-element-runtime.md): the instance, its emitters and elements.
- [Effect element types](effect-element-types.md): what each element type does in its methods.
- [Effect files](effect-files-efx-efb.md): the files an effect is read from.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 56 calls with 18 other topics</summary>

**Characters and objects** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md), [frame update order](../Engine-Core/frame-update-order.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md), [actor record](../Characters-And-Objects/actor-record.md), [actor managers](../Characters-And-Objects/actor-managers.md), [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0024E910`](effect-lifecycle.md) | is called by | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0025B070`](../Characters-And-Objects/actor-lifecycle.md) Actor system: release manager records (on actor lifecycle)<br>[`0x00263660`](../Characters-And-Objects/actor-managers.md) (on actor managers)<br>[`0x002695A0`](../World-Areas-And-Travel/save-and-teleport-crystals.md) (on save and teleport crystals)<br>[`0x0037B230`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x003B6C20`](../Characters-And-Objects/actor-record.md) (on actor record)<br>[`0x003DDC20`](../Characters-And-Objects/actor-managers.md) (on actor managers)<br>[`0x003DE920`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | is called by | [`0x0025BFB0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices) |
| [`0x003601D0`](../World-Areas-And-Travel/game-over.md) (on game over) | calls | [`0x00263FF0`](effect-anchors-and-targets.md) (on effect anchors and targets) |

**Sound and music** (explained on [effect anchors and targets](effect-anchors-and-targets.md), [music](../Sound-And-Music/music.md), [game over](../World-Areas-And-Travel/game-over.md), [force fight mode](../Engine-Core/force-fight-mode.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001EDDA0`](effect-lifecycle.md) | is called by | [`0x003B99D0`](effect-anchors-and-targets.md) (on effect anchors and targets) |
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00360B50`](../Sound-And-Music/music.md) (on music)<br>[`0x00360DD0`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle)<br>[`0x003636A0`](../Sound-And-Music/map-sounds.md) (on map sounds) |
| [`0x003601D0`](../World-Areas-And-Travel/game-over.md) (on game over) | calls | [`0x002DF060`](effect-file-loading.md) (on effect file loading)<br>[`0x002DF0F0`](../Sound-And-Music/sound-effects.md) (on sound effects)<br>[`0x002DF370`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x00360D70`](../Sound-And-Music/music-table.md) (on music table)<br>[`0x00362850`](../Sound-And-Music/spatial-sound.md) (on spatial sound)<br>[`0x003633B0`](effect-file-loading.md) (on effect file loading)<br>[`0x003636A0`](../Sound-And-Music/map-sounds.md) (on map sounds)<br>[`0x00363750`](../Sound-And-Music/map-sounds.md) (on map sounds)<br>[`0x00363E40`](../Sound-And-Music/map-sounds.md) (on map sounds) |

**Battle actions** (explained on [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002FCB60`](effects-on-actors-and-scripts.md) (on effects on actors and scripts) | calls | [`0x002FC3C0`](effect-element-runtime.md) (on effect element runtime) |

**Engine core** (explained on [script screen effects](script-screen-effects.md), [native commands](../Scripts-And-Script-Commands/native-commands.md), [global state accessors](../Engine-Core/global-state-accessors.md), [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001EDDA0`](effect-lifecycle.md) | is called by | [`0x00265860`](effect-lifecycle.md)<br>[`0x00265880`](../Scripts-And-Script-Commands/native-commands.md) (on native commands) |
| [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) | calls | [`0x001EDDA0`](effect-lifecycle.md) |
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00229EE0`](effect-lifecycle.md) |
| [`0x003601D0`](../World-Areas-And-Travel/game-over.md) (on game over) | calls | [`0x00229EE0`](effect-lifecycle.md)<br>[`0x00229EF0`](effect-file-loading.md) (on effect file loading) |
| [`0x003A8AE0`](effect-lifecycle.md) | calls | [`0x001EDDA0`](effect-lifecycle.md) |

**Controls and input** (explained on [vibration](../Controls-And-Input/vibration.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0035B5D0`](../Controls-And-Input/vibration.md) (on vibration) |

**Movement and pathfinding** (explained on [frame update order](../Engine-Core/frame-update-order.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md), [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001EDDA0`](effect-lifecycle.md) | is called by | [`0x0025DF00`](../Characters-And-Objects/field-runtime.md) World actor: update runtime and script execution state (on field runtime) |
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00263560`](../Scripts-And-Script-Commands/world-lock.md) (on world lock)<br>[`0x0026A1D0`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata)<br>[`0x00379070`](../World-Areas-And-Travel/doors-gates-and-map-changes.md) (on doors gates and map changes)<br>[`0x003791C0`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle)<br>[`0x003792D0`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle)<br>[`0x003DAA20`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x003A7360`](effect-element-runtime.md) (on effect element runtime) | calls | [`0x0024C6B0`](effect-element-runtime.md) (on effect element runtime)<br>[`0x0024C870`](effect-element-runtime.md) (on effect element runtime) |

**Party** (explained on [player movement](../Movement-And-Pathfinding/player-movement.md), [actor managers](../Characters-And-Objects/actor-managers.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00358B40`](../Movement-And-Pathfinding/player-movement.md) (on player movement)<br>[`0x00359200`](../Party/party-leader.md) (on party leader) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x0032E520`](effect-file-loading.md) (on effect file loading) |
| [`0x003601D0`](../World-Areas-And-Travel/game-over.md) (on game over) | calls | [`0x0032E520`](effect-file-loading.md) (on effect file loading) |

**Saving, loading and settings** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields) |
| [`0x003601D0`](../World-Areas-And-Travel/game-over.md) (on game over) | calls | [`0x002EF5F0`](../Rewards-EXP-Gil-And-Loot/gil.md) (on gil) |

**Menus and HUD** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001EDDA0`](effect-lifecycle.md) | is called by | [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) |
| [`0x003A7050`](effect-lifecycle.md) | is called by | [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) |
| [`0x003A7300`](effect-lifecycle.md) | is called by | [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) |
| [`0x003A74F0`](effect-lifecycle.md) | is called by | [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) |

**World, areas and travel** (explained on [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md), [ebp navigation icons](../EBP-Script-Files/ebp-navigation-icons.md), [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md), [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00378230`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x003DFA50`](../EBP-Script-Files/ebp-navigation-icons.md) (on ebp navigation icons)<br>[`0x003EAA00`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle) |
| [`0x003601D0`](../World-Areas-And-Travel/game-over.md) (on game over) | calls | [`0x00331920`](../Saving-Loading-And-Settings/game-settings.md) (on game settings) |

</details>
