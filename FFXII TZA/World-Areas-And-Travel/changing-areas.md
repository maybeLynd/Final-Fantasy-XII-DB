[Home](../../README.md) / [World, areas and travel](README.md) / Changing areas

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Changing areas: the steps from a jump request to the new zone running | operation | World, areas and travel | Changing areas and travel | The order in which the game moves the party to another zone: the request every jump passes through, staging with the transition record and the autosave test, the fade, the tick that tears the old zone down, the zone's file loads, the navigation bind that releases the start hold, and the start work of the new zone, each step linked to the page that explains it. | 0x00314440, 0x003145E0, 0x00314020, 0x0032FC30, 0x0032FCA0, 0x002620E0, 0x00314530 |

## What the player sees

The screen fades to black, the next area loads, the party appears at its entrance and the screen fades back in.
Nothing moves while the screen is dark, and a second jump asked for in that time is ignored.

## Steps

| Step | What happens | Where in the code |
|---|---|---|
| 1 | **The request.** A script's `mapjump(map, entrance, mode)`, a door or gate script, the crystal warp (mode 10), the game-over and KO paths, the debug menu and the load-completion callbacks all reach the one funnel `0x00314440`; a request while a jump is pending is dropped ([zone changes](zone-changes-and-mapjump.md#the-request), [save and teleport crystals](save-and-teleport-crystals.md), [game over](game-over.md)). |   |
| 2 | **Staging.** `0x003145E0` drains the resource queue, requests actor managers 1 to 3 for unloading, writes the transition record in the save payload (the old and new map and entrance, the mode and the persistence group) and calls `0x002EFA70(3, 0, 1, 0)` on fade slot 3 ([zone changes](zone-changes-and-mapjump.md#staging-and-the-transition-record), [save data fields](../Saving-Loading-And-Settings/save-data-fields.md)).<br>• A nonblocking request instead returns 1 at once while the queue is busy, before any write. | `0x00314700`<br>`0x00314609`-`0x0031461C` |
| 3 | **The autosave test.** Still inside staging, when `0x0020E500(map, 0x00265270(), entrance)` returns non-zero, the runtime state is captured and the autosave widget `0x0057E4D0` is created (`0x00583260` at `0x003147E9`) ([saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md)):<br>• the widget queues the write to slot 0;<br>• it completes when the result `0x003BB420()` is 0 and opens the insufficient-disk-space popup when it is not. | `0x00314774`-`0x0031477B`<br>`0x003147BB`, `0x003147DF`, `0x003147E4`<br>`0x0057E53C`-`0x0057E599` |
| 4 | **The fade-out.** After staging returns, the funnel requests manager 0 with `0x0026A5F0(0)`; then, unless the mode's bit `0x1` is set, fade slot 2 starts when `0x002EFD20(2)` reports it idle ([screen fades](../Graphics/screen-fades.md)).<br>• After `0x002E1C40(0, 2)` sets bit `0x4` of the script hide word `0x0215F1AC` and clears it in `0x0215F1B4`, the funnel calls `0x00254AC0()`, which returns at once while the dword `0x02092744` is not 0.<br>• Otherwise, unless bits `0x40` and `0x80` of `0x01E0C320` are both set, `0x00254AC0` runs `0x003C8990()`, `0x0035DAC0()`, `0x0028FF20()`, `0x003C58B0()`, `0x002B6140()`, `0x0035D5A0()`, `0x0035D0E0([0x020927EC])`, `0x003C9900()` and `0x003BBFA0(0)` in that order and clears bit `0x80` of `0x020927EC`.<br>• Either way it then clears bits `0xC` of the HUD draw word `0x01E0C2AC` and ends with a tail jump to `0x0017E7D0()`. These are the nine calls of the hide branch of `0x00255330`, in the same order, with the same ending. `0x00255330` is told on [HUD](../Menus-And-HUD/hud.md#the-hud-switch). | `0x003144A1`<br>`0x003144A6`<br>`0x003144B1`-`0x003144E5`<br>`0x003144EA`-`0x003144F1`<br>`0x003144F6`<br>`0x00254AC4`-`0x00254ACB`<br>`0x00254ACD`-`0x00254ADA`<br>`0x00254ADC`-`0x00254B11`<br>`0x00254B1B`-`0x00254B2B`<br>`0x00255348`-`0x00255397` |
| 5 | **The teardown.** On the next simulation tick `0x00314020` unloads every requested manager before any actor runs, releasing what each manager held ([actor managers](../Characters-And-Objects/actor-managers.md), [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)). | `0x00314078` |

   The `0x0026CE60(m)` pass of `0x0025BFB0` before the unloads returns at once for a manager that is still running. See
   [zone changes](zone-changes-and-mapjump.md#the-tick-tears-the-old-zone-down-and-starts-the-load).
| Step | What happens | Where in the code |
|---|---|---|
| 6 | **The area data.** `0x0032FC30(0, map)` first reads the area data ([area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)). | `0x003EA6E0` |
| 7 | **The loads.** It then queues the zone's files from namespace 5 at index `map × 3`, each load setting a pending bit, and sets the start hold ([zone changes](zone-changes-and-mapjump.md#where-the-files-come-from), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [zone asset list](zone-asset-list.md)). |   |
| 8 | **The script container.** As each read completes, its callback clears its pending bit; when the primary payload completes, its directory is walked and each section is handed to its handler ([EBP script container](../EBP-Script-Files/ebp-script-container.md)). |   |
| 9 | **The map pack and the navigation bind.** When the map pack completes, its sections are kept or freed and the navigation data is bound; only then is the start hold released, so the zone's actors and scripts cannot start before its navigation exists ([map pack](mpk-map-pack.md), [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)). |   |
| 10 | **The zone starts.** With every pending bit clear the manager is finalised, and the first field pass for manager 0 runs the start work once and clears the busy bits of the transition ([zone changes](zone-changes-and-mapjump.md#the-zone-is-ready)). |   |
| 11 | **The start work.** The follow camera is set up, the weather slot is rolled and applied, the field's effect rows are instantiated and the map sounds start ([scripted camera](../Graphics/scripted-camera.md), [weather](weather.md), [effect files](../Graphics/effect-files-efx-efb.md), [map sounds](../Sound-And-Music/map-sounds.md)). |   |

A loaded save enters at step 2 through the restore path `0x00314530`, which requests managers 1 to 3 and 0, takes the
destination from the transition record already in the payload and starts fade slot 2 itself
([zone changes](zone-changes-and-mapjump.md#staging-and-the-transition-record)).

## Outcomes

- The save payload's transition record holds the previous map and entrance beside the new ones.
- Actor managers 0 to 3 have been unloaded and manager 0 loaded again with the new zone; the new zone's scripts run in
  manager 0.
- A scene's jump completes in the scene and the scene continues; the zone's own jump ends with the zone's script.

## Related

- [Zone changes](zone-changes-and-mapjump.md): the mechanism in full.
- [Doors, gates and map changes](doors-gates-and-map-changes.md): the regions that start a jump.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md): scenes use the same loader.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 93 calls with 22 other topics</summary>

**Characters and objects** (explained on [event scenes](../Scripts-And-Script-Commands/event-scenes.md), [frame update order](../Engine-Core/frame-update-order.md), [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002620E0`](zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x003DE920`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x002620E0`](zone-changes-and-mapjump.md) (on zone changes and mapjump) | is called by | [`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) |
| [`0x0026A5F0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | is called by | [`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) |
| [`0x002EFA70`](../Graphics/screen-fades.md) (on screen fades) | is called by | [`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) |
| [`0x002EFD20`](changing-areas.md) | is called by | [`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) |
| [`0x00314020`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | calls | [`0x0025BFB0`](zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts)<br>[`0x00263660`](../Characters-And-Objects/actor-managers.md) (on actor managers)<br>[`0x00268650`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003DB1F0`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x0032FC30`](../Story-Events-And-Hunts/tutorials-scenes.md) (on tutorials scenes) | calls | [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices) |
| [`0x0032FC30`](../Story-Events-And-Hunts/tutorials-scenes.md) (on tutorials scenes) | is called by | [`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) |
| [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices) | calls | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032ED80`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |

**Sound and music** (explained on [mpk map pack](mpk-map-pack.md), [debug menu](../Engine-Core/debug-menu.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002620E0`](zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00363B40`](../Sound-And-Music/map-sounds.md) (on map sounds) |
| [`0x00314020`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | calls | [`0x002DEBA0`](../Engine-Core/debug-menu.md) (on debug menu)<br>[`0x00362850`](../Sound-And-Music/spatial-sound.md) (on spatial sound) |

**Battle actions** (explained on [zone changes and mapjump](zone-changes-and-mapjump.md), [battle units](../Characters-And-Objects/battle-units.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00314440`](changing-areas.md) | is called by | [`0x00319F50`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle actor timeline event (on ko and game over) |
| [`0x0032FC30`](../Story-Events-And-Hunts/tutorials-scenes.md) (on tutorials scenes) | is called by | [`0x00306BD0`](../Story-Events-And-Hunts/summons-scenes.md) Battle action: initialize global special sequence mode (on summons scenes) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x001EC760`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x00314020`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | is called by | [`0x0022A770`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x0022B8C0`](../Graphics/graphics-thread-handshake.md) (on graphics thread handshake)<br>[`0x0022BC20`](../Graphics/graphics-thread-handshake.md) (on graphics thread handshake) |

**Controls and input** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [frame update order](../Engine-Core/frame-update-order.md), [zone changes and mapjump](zone-changes-and-mapjump.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x00253C70`](../Controls-And-Input/controls.md) (on controls) |
| [`0x00314020`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | calls | [`0x002E09A0`](../Menus-And-HUD/menus.md) (on menus)<br>[`0x0036FD90`](../Controls-And-Input/controls.md) (on controls) |
| [`0x00314440`](changing-areas.md) | calls | [`0x00182D80`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save)<br>[`0x00408B00`](../Controls-And-Input/controls.md) (on controls) |
| [`0x00314530`](zone-changes-and-mapjump.md) World transition: requeue current field for restore (on zone changes and mapjump) | calls | [`0x00182D80`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) |

**Movement and pathfinding** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00314020`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | calls | [`0x00234520`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x003DAA20`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x003DAA40`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x003DAC70`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x0046AFA0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |

**Party** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00314020`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | calls | [`0x00358C60`](../Movement-And-Pathfinding/player-movement.md) (on player movement)<br>[`0x00358EE0`](../Movement-And-Pathfinding/player-movement.md) (on player movement) |

**Steam and achievements** (explained on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [achievements](../Steam-And-Achievements/achievements.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x003154B0`](../Menus-And-HUD/clan-primer-entries.md) (on clan primer entries)<br>[`0x003161A0`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Graphics** (explained on [weather](weather.md), [debug menu](../Engine-Core/debug-menu.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002620E0`](zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00259B30`](../Graphics/scripted-camera.md) (on scripted camera) |
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x001CD0E0`](../Engine-Core/graphics-settings.md) (on graphics settings) |
| [`0x00314020`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) | calls | [`0x00259AF0`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x003E7650`](../Graphics/character-status-visuals.md) (on character status visuals) |

**Game files and data tables** (explained on [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md), [zone changes and mapjump](zone-changes-and-mapjump.md), [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x001DA220`](../Game-Files-And-Data-Tables/prefetch-manifests.md) (on prefetch manifests)<br>[`0x001DA970`](../Game-Files-And-Data-Tables/prefetch-manifests.md) (on prefetch manifests) |
| [`0x00314440`](changing-areas.md) | calls | [`0x001D6C40`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) |
| [`0x00314530`](zone-changes-and-mapjump.md) World transition: requeue current field for restore (on zone changes and mapjump) | calls | [`0x001D6C40`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) |
| [`0x003145E0`](zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump) | calls | [`0x0032E520`](../Graphics/effect-file-loading.md) (on effect file loading) |
| [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices) | calls | [`0x002DF980`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |

**Saving, loading and settings** (explained on [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md), [zone changes and mapjump](zone-changes-and-mapjump.md), [saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md), [frame update order](../Engine-Core/frame-update-order.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [global state accessors](../Engine-Core/global-state-accessors.md), [party data](../Party/party-data.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002EFA70`](../Graphics/screen-fades.md) (on screen fades) | is called by | [`0x00280140`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |
| [`0x002EFD20`](changing-areas.md) | is called by | [`0x00280140`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |
| [`0x00314440`](changing-areas.md) | is called by | [`0x00280140`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |
| [`0x003145E0`](zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump) | calls | [`0x0020E500`](changing-areas.md) |
| [`0x0020E500`](changing-areas.md) | calls | [`0x001C1720`](../Saving-Loading-And-Settings/saving-and-loading-autosave.md) (on saving and loading autosave)<br>[`0x001C18E0`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x002620E0`](zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields) |
| [`0x00314530`](zone-changes-and-mapjump.md) World transition: requeue current field for restore (on zone changes and mapjump) | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields) |
| [`0x003145E0`](zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump) | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields)<br>[`0x002EF640`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode)<br>[`0x00583260`](changing-areas.md)<br>[`0x005844A0`](../Saving-Loading-And-Settings/save-data-fields.md) Save transition: prepare runtime image for capture (on save data fields) |
| [`0x003BB420`](changing-areas.md) | is called by | [`0x0057E4D0`](../Saving-Loading-And-Settings/saving-and-loading-autosave.md) (on saving and loading autosave)<br>[`0x00582240`](../Saving-Loading-And-Settings/saving-and-loading-transaction.md) (on saving and loading transaction) |
| [`0x0057E4D0`](../Saving-Loading-And-Settings/saving-and-loading-autosave.md) (on saving and loading autosave) | calls | [`0x0057E310`](../Saving-Loading-And-Settings/saving-and-loading-autosave.md) Save write: prepare and submit full image (on saving and loading autosave) |

**Scripts and script commands** (explained on [debug menu](../Engine-Core/debug-menu.md), [screen fades](../Graphics/screen-fades.md), [zone changes and mapjump](zone-changes-and-mapjump.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md), [ebp script container](../EBP-Script-Files/ebp-script-container.md), [debug logging](../Engine-Core/debug-logging.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0026A5F0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | is called by | [`0x0050D0C0`](../Engine-Core/debug-menu.md) (on debug menu)<br>[`0x0050D240`](changing-areas.md) |
| [`0x002EFA70`](../Graphics/screen-fades.md) (on screen fades) | is called by | [`0x003559B0`](../Graphics/screen-fades.md) (on screen fades)<br>[`0x00355EB0`](../Graphics/screen-fades.md) (on screen fades)<br>[`0x00356270`](../Graphics/screen-fades.md) (on screen fades)<br>[`0x00356650`](../Graphics/screen-fades.md) (on screen fades)<br>[`0x00356A50`](../Graphics/screen-fades.md) (on screen fades)<br>[`0x00356FE0`](../Graphics/screen-fades.md) (on screen fades) |
| [`0x002EFD20`](changing-areas.md) | is called by | [`0x0033FD40`](changing-areas.md) |
| [`0x00314440`](changing-areas.md) | is called by | [`0x00355350`](zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x0050C8A0`](zone-changes-and-mapjump.md) (on zone changes and mapjump) |
| [`0x0032FC30`](../Story-Events-And-Hunts/tutorials-scenes.md) (on tutorials scenes) | is called by | [`0x003522C0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x00353080`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x00353590`](../Story-Events-And-Hunts/tutorials-scenes.md) (on tutorials scenes)<br>[`0x0050D0C0`](../Engine-Core/debug-menu.md) (on debug menu) |
| [`0x003BB420`](changing-areas.md) | is called by | [`0x0050C670`](../Engine-Core/debug-logging.md) (on debug logging)<br>[`0x0050C8D0`](changing-areas.md)<br>[`0x0050C990`](changing-areas.md)<br>[`0x0050EEA0`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save)<br>[`0x0050F0A0`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) |

**Story, events and hunts** (explained on [model effects and motion commands](../Graphics/model-effects-and-motion-commands.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x001ED240`](../Graphics/model-effects-and-motion-commands.md) G0999; (on model effects and motion commands) |
| [`0x00265270`](../Menus-And-HUD/clan-primer-entries.md) Field data: get variable0 (on clan primer entries) | is called by | [`0x00377970`](../Story-Events-And-Hunts/story-flags.md) (on story flags) |

**Menus and HUD** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [zone changes and mapjump](zone-changes-and-mapjump.md), [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002EFA70`](../Graphics/screen-fades.md) (on screen fades) | is called by | [`0x0027EFA0`](../Menus-And-HUD/menu-screens.md) (on menu screens) |
| [`0x002EFD20`](changing-areas.md) | is called by | [`0x0027EFA0`](../Menus-And-HUD/menu-screens.md) (on menu screens) |
| [`0x00314440`](changing-areas.md) | calls | [`0x00254AC0`](changing-areas.md) |
| [`0x003BB420`](changing-areas.md) | is called by | [`0x00252030`](../Menus-And-HUD/widgets.md) (on widgets) |

</details>

---

[Zone changes →](zone-changes-and-mapjump.md)
