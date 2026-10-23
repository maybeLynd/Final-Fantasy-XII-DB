---
title: "Changing areas: the steps from a jump request to the new zone running"
kind: "operation"
category: "World, areas and travel"
addresses: "0x00314440, 0x003145E0, 0x00314020, 0x0032FC30, 0x0032FCA0, 0x002620E0, 0x00314530"
---

## What the player sees

The screen fades to black, the next area loads, the party appears at its entrance and the screen fades back in.
Nothing moves while the screen is dark, and a second jump asked for in that time is ignored.

## Steps

1. **The request.** A script's `mapjump(map, entrance, mode)`, a door or gate script, the crystal warp (mode 10), the
   game-over and KO paths, the debug menu and the load-completion callbacks all reach the one funnel `0x00314440`; a
   request while a jump is pending is dropped ([zone changes](zone-changes-and-mapjump.md#the-request),
   [save and teleport crystals](save-and-teleport-crystals.md), [game over](game-over.md)).
2. **Staging.** `0x003145E0` drains the resource queue, requests actor managers 1 to 3 for reinitialisation, writes
   the transition record in the save payload (the old and new map and entrance, the mode and the persistence group)
   and calls `0x002EFA70(3, 0, 1, 0)` on fade slot 3 (`0x00314700`)
   ([zone changes](zone-changes-and-mapjump.md#staging-and-the-transition-record),
   [save data fields](../Saving-Loading-And-Settings/save-data-fields.md)).
3. **The autosave test.** Still inside staging, when `0x0020E500(map, 0x00265270(), entrance)` returns non-zero
   (`0x00314774`-`0x0031477B`), the runtime state is captured (`0x003147BB`, `0x003147DF`, `0x003147E4`) and the autosave
   widget `0x0057E4D0` is created (`0x00583260` at `0x003147E9`)
   ([saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md)):
   - the widget queues the write to slot 0;
   - it completes when the result `0x003BB420()` is 0 and opens the insufficient-disk-space popup when it is not
     (`0x0057E53C`-`0x0057E599`).
4. **The fade-out.** After staging returns, the funnel requests manager 0 with `0x0026A5F0(0)` (`0x003144A1`); then,
   unless the mode's bit 0 is set (`0x003144A6`), fade slot 2 starts when `0x002EFD20(2)` reports it idle
   (`0x003144B1`-`0x003144E5`) ([screen fades](../Graphics/screen-fades.md)).
5. **The teardown.** On the next simulation tick `0x00314020` reinitialises and unloads every requested manager before
   any actor runs, releasing what each manager held
   ([actor managers](../Characters-And-Objects/actor-managers.md),
   [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)).
6. **The area data.** `0x0032FC30(0, map)` first reads the area data (`0x003EA6E0`)
   ([area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)).
7. **The loads.** It then queues the zone's files from namespace 5 at index `map × 3`, each load setting a pending
   bit, and sets the start hold ([zone changes](zone-changes-and-mapjump.md#where-the-files-come-from),
   [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md),
   [zone asset list](zone-asset-list.md)).
8. **The script container.** As each read completes, its callback clears its pending bit; when the primary
   payload completes, its directory is walked and each section is handed to its handler
   ([EBP script container](../EBP-Script-Files/ebp-script-container.md)).
9. **The map pack and the navigation bind.** When the map pack completes, its sections are kept or freed and the
   navigation data is bound; only then is the start hold released, so the zone's actors and scripts cannot start before its navigation
   exists ([map pack](mpk-map-pack.md),
   [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)).
10. **The zone starts.** With every pending bit clear the manager is finalised, and the first field pass for manager
   0 runs the start work once and clears the busy bits of the transition
   ([zone changes](zone-changes-and-mapjump.md#the-zone-is-ready)).
11. **The start work.** The follow camera is set up, the weather slot is rolled and applied, the field's effect
    rows are instantiated and the map sounds start ([scripted camera](../Graphics/scripted-camera.md),
    [weather](weather.md), [effect files](../Graphics/effect-files-efx-efb.md),
    [map sounds](../Sound-And-Music/map-sounds.md)).

A loaded save enters at step 2 through the restore path `0x00314530`, which requests managers 1 to 3 and 0, takes the
destination from the transition record already in the payload and starts fade slot 2 itself ([zone changes](zone-changes-and-mapjump.md#staging-and-the-transition-record)).

## Outcomes

- The save payload's transition record holds the previous map and entrance beside the new ones.
- Actor managers 0 to 3 have been reinitialised; the new zone's scripts run in manager 0.
- A scene's jump completes in the scene and the scene continues; the zone's own jump ends with the zone's script.

## Related

- [Zone changes](zone-changes-and-mapjump.md): the mechanism in full.
- [Doors, gates and map changes](doors-gates-and-map-changes.md): the regions that start a jump.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md): scenes use the same loader.
