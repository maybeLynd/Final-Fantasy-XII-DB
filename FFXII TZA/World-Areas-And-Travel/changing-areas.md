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
   unless the mode's bit `0x1` is set (`0x003144A6`), fade slot 2 starts when `0x002EFD20(2)` reports it idle
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
   navigation data is bound; only then is the start hold released, so the zone's actors and scripts cannot start
   before its navigation exists ([map pack](mpk-map-pack.md),
   [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)).
10. **The zone starts.** With every pending bit clear the manager is finalised, and the first field pass for manager
   0 runs the start work once and clears the busy bits of the transition
   ([zone changes](zone-changes-and-mapjump.md#the-zone-is-ready)).
11. **The start work.** The follow camera is set up, the weather slot is rolled and applied, the field's effect
    rows are instantiated and the map sounds start
    ([scripted camera](../Graphics/scripted-camera.md),
    [weather](weather.md), [effect files](../Graphics/effect-files-efx-efb.md),
    [map sounds](../Sound-And-Music/map-sounds.md)).

A loaded save enters at step 2 through the restore path `0x00314530`, which requests managers 1 to 3 and 0, takes the
destination from the transition record already in the payload and starts fade slot 2 itself
([zone changes](zone-changes-and-mapjump.md#staging-and-the-transition-record)).

## Outcomes

- The save payload's transition record holds the previous map and entrance beside the new ones.
- Actor managers 0 to 3 have been reinitialised; the new zone's scripts run in manager 0.
- A scene's jump completes in the scene and the scene continues; the zone's own jump ends with the zone's script.

## Related

- [Zone changes](zone-changes-and-mapjump.md): the mechanism in full.
- [Doors, gates and map changes](doors-gates-and-map-changes.md): the regions that start a jump.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md): scenes use the same loader.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x002620E0` calls `0x003DE920`; `0x002620E0` is called by `0x0025D9E0`; `0x0026A5F0` is called by `0x0025D9E0`;
  `0x002EFA70` is called by `0x0025D9E0`; `0x002EFD20` is called by `0x0025D9E0`; `0x00314020` calls `0x0025BFB0`, `0x0025D9E0`,
  `0x00263660`, `0x00268650`, `0x003DB1F0`; `0x0032FC30` calls `0x0032FCA0`; `0x0032FC30` is called by `0x0025D9E0`; `0x0032FCA0`
  calls `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0`.
- Actor entity: those functions are documented on [event scenes](../Scripts-And-Script-Commands/event-scenes.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [zone changes and mapjump](zone-changes-and-mapjump.md); and on
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md).
- Audio: `0x002620E0` calls `0x00363B40`; `0x00314020` calls `0x002DEBA0`, `0x00362850`; those functions are documented on
  [mpk map pack](mpk-map-pack.md), [debug menu](../Engine-Core/debug-menu.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Combat action: `0x00314440` is called by `0x00319F50`; `0x0032FC30` is called by `0x00306BD0`; those functions are
  documented on [zone changes and mapjump](zone-changes-and-mapjump.md),
  [battle units](../Characters-And-Objects/battle-units.md).
- Core runtime: `0x00265270` is called by `0x001EC760`; `0x00314020` is called by `0x0022A770`, `0x0022B8C0`, `0x0022BC20`; those
  functions are documented on [frame update order](../Engine-Core/frame-update-order.md).
- Input: `0x00265270` is called by `0x00253C70`; `0x00314020` calls `0x002E09A0`, `0x0036FD90`; `0x00314440` calls `0x00182D80`,
  `0x00408B00`; `0x00314530` calls `0x00182D80`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [zone changes and mapjump](zone-changes-and-mapjump.md).
- Movement: `0x00314020` calls `0x00234520`, `0x003DAA20`, `0x003DAA40`, `0x003DAC70`, `0x0046AFA0`; those functions are
  documented on [frame update order](../Engine-Core/frame-update-order.md).
- Party: `0x00314020` calls `0x00358C60`, `0x00358EE0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Platform online achievements: `0x00265270` is called by `0x003154B0`, `0x003161A0`; those functions are documented on
  [handbook files](../Game-Files-And-Data-Tables/handbook-files.md),
  [achievements](../Steam-And-Achievements/achievements.md).
- Presentation: `0x002620E0` calls `0x00259B30`; `0x00265270` is called by `0x001CD0E0`; `0x00314020` calls `0x00259AF0`,
  `0x003E7650`; those functions are documented on [weather](weather.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Resource: `0x00265270` is called by `0x001DA220`, `0x001DA970`; `0x00314440` calls `0x001D6C40`; `0x00314530` calls `0x001D6C40`;
  `0x003145E0` calls `0x0032E520`; `0x0032FCA0` calls `0x002DF980`, `0x0032E400`, `0x0032E620`.
- Resource: those functions are documented on
  [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md),
  [zone changes and mapjump](zone-changes-and-mapjump.md), [debug menu](../Engine-Core/debug-menu.md),
  [startup constants](../Engine-Core/startup-constants.md).
- Save load settings: `0x002EFA70` is called by `0x00280140`; `0x002EFD20` is called by `0x00280140`; `0x00314440` is called by
  `0x00280140`; `0x003145E0` calls `0x0020E500`; those functions are documented on
  [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md),
  [zone changes and mapjump](zone-changes-and-mapjump.md).
- Save load settings: `0x0020E500` calls `0x001C1720`, `0x001C18E0`; `0x002620E0` calls `0x002EF2B0`; `0x00314530` calls
  `0x002EF2B0`; `0x003145E0` calls `0x002EF2B0`, `0x002EF640`, `0x00583260`, `0x005844A0`; `0x003BB420` is called by `0x0057E4D0`,
  `0x00582240`; `0x0057E4D0` calls `0x0057E310`.
- Save load settings: those functions are documented on
  [saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
  [global state accessors](../Engine-Core/global-state-accessors.md).
- Save load settings: and on [zone changes and mapjump](zone-changes-and-mapjump.md),
  [party data](../Party/party-data.md).
- Script VM: `0x0026A5F0` is called by `0x0050D0C0`, `0x0050D240`; `0x002EFA70` is called by `0x003559B0`, `0x00355EB0`,
  `0x00356270`, `0x00356650`, `0x00356A50`, `0x00356FE0`; `0x002EFD20` is called by `0x0033FD40`; `0x00314440` is called by
  `0x00355350`, `0x0050C8A0`; `0x0032FC30` is called by `0x003522C0`, `0x00353080`, `0x00353590`, `0x0050D0C0`; `0x003BB420` is called
  by `0x0050C670`, `0x0050C8D0`, `0x0050C990`, `0x0050EEA0`, `0x0050F0A0`.
- Script VM: those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [screen fades](../Graphics/screen-fades.md),
  [zone changes and mapjump](zone-changes-and-mapjump.md),
  [event scenes](../Scripts-And-Script-Commands/event-scenes.md).
- Script VM: and on [ebp script container](../EBP-Script-Files/ebp-script-container.md),
  [debug logging](../Engine-Core/debug-logging.md).
- Story event quest hunt: `0x00265270` is called by `0x001ED240`; those functions are documented on
  [model effects and motion commands](../Graphics/model-effects-and-motion-commands.md).
- Story event quest hunt: `0x00265270` is called by `0x00377970`; those functions are documented on
  [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md).
- UI: `0x002EFA70` is called by `0x0027EFA0`; `0x002EFD20` is called by `0x0027EFA0`; `0x00314440` calls `0x00254AC0`; `0x003BB420`
  is called by `0x00252030`; those functions are documented on
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [zone changes and mapjump](zone-changes-and-mapjump.md),
  [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md).
