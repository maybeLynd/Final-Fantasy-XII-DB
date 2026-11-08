---
title: "Loading a save: the steps from choosing a slot to the party standing where it saved"
kind: "operation"
category: "Saving, loading and settings"
addresses: "0x00580EB0, 0x00582860, 0x00394400, 0x00394130, 0x00512130, 0x00255260, 0x002EF640, 0x002EF650, 0x00233C10, 0x002CFD10, 0x00268320, 0x00267C90, 0x00314530, 0x002DE050, 0x00584210"
---

## What the player sees

The player picks Load and a slot. "Loading..." shows, then "Load complete."; the screen fades, and the party appears
where the save was made.

The slot's file is read whole into the game's live save image. The party data is then pointed at that image, and the
area is started again from the zone-change record stored in it; the options in force before the load are written back
over the loaded ones.

## Steps

1. **The widget is created.** The End handler `0x00512130` of script verb `0x705D` creates the post-load widget
   `0x00394130` ([verb table](../Scripts-And-Script-Commands/verb-table.md)). On its first message it:
   - sets its state `+0xC0` and its counter `+0xC2` to 0 and keeps itself in `0x02AEE4D0`
     (`0x003942A4`-`0x003942B2`), which `0x00394640` tests so that it creates only one widget;
   - zeroes the active image's play clock (`+0x10` and the dword at `+0x18`, `0x003942B9`-`0x003942BD`);
   - keeps the in-game options, the `0x28`-byte record at `0x002536A0() + 8`, at its `+0xC8`
     (`0x003942C0`-`0x003942E5`) ([game settings](game-settings.md));
   - stores 1 at `0x020927C8` (`0x00254CB0`, `0x003942ED`);
   - resets the active image with `0x002EF650` (`0x003942F2`);
   - sets the pending preset byte `0x0208D455` to 0 (`0x0023A110`, `0x003942F9`);
   - stores `0x112` as the transition record's destination field (`0x00314DC0`, `0x003942FE`-`0x00394303`);
   - starts fade slot 2 over 15 frames (`0x002EFA70`, `0x00394315`) and sets a 30-frame counter
     (`0x0039431A`-`0x00394322`);
   - attaches itself to the parent `[0x0208EA28]` with `0x00244960` (`0x00394329`-`0x00394330`), and returns 0.
2. **The read.** State 8 of the save and load screen queues the storage requests that read the slot's file into
   the active image, `0x56690` bytes ([saving and loading](saving-and-loading.md#the-save-and-load-screen),
   [save file format](save-file-format.md)).
3. **Load complete.** State 9 reports the load
   ([saving and loading](saving-and-loading.md#the-save-and-load-screen)).
4. **The post-load sequence.** On message `0x12` the load screen's lifecycle `0x00582860` runs its post-load calls:
   - `0x00394400`, when `0x00394520` finds it, sends a close request (`0x00244F00`, `0x0039440A`) to the widget at
     `0x02AEE4C0`, the `0x00394070` widget that `0x00394460` creates (`0x00394495`-`0x003944A4`);
   - `0x00584210` handles the mode-3 stash or its restore, calls `0x00316810` (`0x00584398`) and reseeds the gameplay
     generator from the clock ([saving and loading](saving-and-loading.md#what-a-load-runs),
     [save file format](save-file-format.md)).
5. **The header test.** When its counter has run out, the widget passes the active image's header `+0x68`
   (`0x002EF640`, `0x003941D3`-`0x003941DC`) to `0x00255260`, which accepts a pair of zero dwords or the magic
   `0x0131F3EA` followed by the size `0x4818` (`0x00255265`-`0x00255283`); the payload begins at image `+0x200`.
   When the test fails, the widget:
   - resets the active image with `0x002EF650` (`0x003941E5`), which clears its `0x56690` bytes at `0x02164280`
     (`memset`, `0x002EF663`), calls the empty `0x0016D6A0(0)` (`0x002EF66A`) and runs `0x00253A80`, `0x002EF2D0` and
     `0x00238A80`, the last as a tail jump (`0x002EF656`-`0x002EF67D`);
   - clears the cursor-bank entry and the battle-menu cursor block of step 7 (`0x002CFD10`, `0x003941ED`);
   - asks for map 0 through the jump funnel `0x00314440` (`0x003941FC`)
     ([save file format](save-file-format.md), [changing areas](../World-Areas-And-Travel/changing-areas.md)).
6. **`btlCallBackAfterReadSaveRam()`.** When the test passes, `0x00233C10` binds the party block `0x02EBF190` to the
   loaded image ([save data fields](save-data-fields.md), [party data](../Party/party-data.md)). The empty
   function `0x0016D6A0` runs before it ([jump thunks](../Engine-Core/jump-thunks.md)).
   - It binds only while the pointer is empty, and then runs the battle reset `0x00237DF0` twice (`0x00233C3F`,
     `0x00233C48`).
   - With the pointer set it checks the magic `0x05071901` (`0x00233C4D`): a wrong magic runs `0x00237DF0`
     (`0x00233C59`), and a match keeps the loaded block and runs the steps listed on
     [party data](../Party/party-data.md).
7. **`YsSaveRam_CallBackInit()`.** `0x002CFD10` (whose argument it ignores) clears entry 4 of the menu cursor bank 6 (`0x002527B0(6, 4, 0)`) and
   the battle menu's cursor block, `[0x0209BE80] + 0xAA60`, `0xC4` bytes (`0x0028E880`)
   ([battle menu](../Menus-And-HUD/battle-menu.md)).
8. **The options.** The widget writes the options it kept back over the loaded image's record
   (`0x00394234`-`0x00394252`) ([game settings](game-settings.md)).
9. **`AtelRefreshByLoad()`.** `0x00268320` resets the scripts' scratch variables
   ([script variables](../Scripts-And-Script-Commands/script-variables.md)): it zeroes `scratch1` (`0x02099DF0`)
   always (`0x00268359`); only while the load flag `0x0209AC10` is 0 does it zero `scratch2` (`0x02099FF0`, when
   `0x01E0C3EC` is also non-zero, `0x00268324`-`0x00268345`) and set the zone transition record's `initState`,
   payload `+0x1061`, to 1 (`0x0026835E`-`0x0026836C`).
10. **`AtelMapJumpByLoad()`.** `0x00267C90` jumps to the restore path `0x00314530`, which requests the actor managers and
    starts the zone change from the transition record in the payload; the change runs from its staging on
    ([changing areas](../World-Areas-And-Travel/changing-areas.md),
    [zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md#staging-and-the-transition-record)).
11. **`YsConfig_Load()`.** `0x002DE050` runs the options applier `0x002DDA30(0)` ([game settings](game-settings.md)).

The step names are the game's own: `0x0036FCC0` runs the same calls with a log line before each (`0x00D10FD0`-`0x00D11090`),
and before them `AtelLockSystemAndBattleByMapJump()`, `0x002678C0`, which raises stop request 19
([time stop and freeze](../Engine-Core/time-stop-and-freeze.md)); the widget's path does not run it.

The widget's handler `0x00394130` acts on messages 1, 2 and `0x12`. Message 2, the frame message, does nothing while
`0x001EDEC0(+0xB4)` returns 0, which it does only with the 60 fps gate `0x01F82E38` set, `0x01DFE0C0` at 0 and an odd
`+0xB4` (`0x00394184`-`0x00394191`). Otherwise it counts `+0xC2` down to 0 (`0x00394197`-`0x003941A6`) and runs the state
`+0xC0`.

In state 0 it stores 0 at `0x020927C8` (`0x00254CB0(0)`) and moves to state 1 (`0x00394282`-`0x0039428B`). In state 1,
once the counter is 0, it runs the header test of step 5 with steps 6 to 11, or the failed-test path; both end
with a close request on the widget (`0x00244F00`, `0x00394204`, `0x00394269`) and state 2 (`0x0039420B`, `0x00394270`).
State 1 with the counter still running, state 2 and any other state do nothing (`0x003941BF`, `0x003941CD`).

Message `0x12` sends a close request to the object at `0x02AEE4C0` when there is one (`0x00394155`-`0x00394161`) and
clears `0x02AEE4D0` (`0x00394168`). It and every message other than 1 and 2 then go to the shared return-zero stub
`0x005C5230` (`0x0039417F`).

## Outcomes

- The party block points at the loaded image, and the scripts start the zone from its transition record.
- The in-game options are the ones in force when the widget was created, not the loaded image's.
- The menu and battle-menu cursors start from their defaults.
- The gameplay generator is reseeded from the clock, so a reload does not repeat earlier rolls.

## Related

- [Saving and loading](saving-and-loading.md): the screen, the storage queue and the save transaction.
- [Save file format](save-file-format.md): the container and the payload a load reads.
- [Changing areas](../World-Areas-And-Travel/changing-areas.md): the zone change the restore jump starts.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00237DF0` calls `0x00329CC0`; `0x002678C0` is called by `0x0025B600`; `0x002EFA70` is called by `0x0025D9E0`;
  those functions are documented on [party data](../Party/party-data.md),
  [script requests](../Scripts-And-Script-Commands/script-requests.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Audio: `0x002DDA30` calls `0x002DF530`; `0x002DE050` is called by `0x00360D30`, `0x00361080`; those functions are documented
  on [config screen](../Menus-And-HUD/config-screen.md), [music](../Sound-And-Music/music.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Combat AI: `0x00233C10` calls `0x00327F80`; those functions are documented on
  [unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md).
- Combat action: `0x00314440` is called by `0x00319F50`; those functions are documented on
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md).
- Combat formula: `0x00237DF0` calls `0x0023AC80`; those functions are documented on
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md).
- Core runtime: `0x00233C10` calls `0x00229ED0`; `0x00237DF0` calls `0x00229ED0`, `0x0032A160`; `0x002EF650` is called by
  `0x0022B6E0`; `0x00394130` calls `0x001EDEC0`; `0x00582860` calls `0x001EDEC0`.
- Core runtime: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [enemy respawning](../Enemy-Spawning/enemy-respawning.md),
  [global state accessors](../Engine-Core/global-state-accessors.md).
- Gameplay: `0x00233C10` calls `0x00237DF0`; `0x00238A80` calls `0x00237DF0`; `0x00394460` calls `0x00237DF0`; those functions are
  documented on [frame update order](../Engine-Core/frame-update-order.md).
- Input: `0x002678C0` calls `0x00226BE0`; `0x002DDA30` calls `0x001E0FF0`, `0x001E1020`, `0x0035FF30`; `0x00314440` calls
  `0x00182D80`, `0x00408B00`; `0x00314530` calls `0x00182D80`; `0x00394460` calls `0x002501E0`; `0x00582860` calls `0x00182D40`.
- Input: those functions are documented on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [config screen](../Menus-And-HUD/config-screen.md), [vibration](../Controls-And-Input/vibration.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md).
- Input: and on [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Items equipment shops license: `0x00233C10` calls `0x0030B6A0`; `0x00237DF0` calls `0x0023AF50`; `0x00238A80` calls
  `0x0030B6A0`; those functions are documented on
  [item and ability ids](../Engine-Core/item-and-ability-ids.md), [party data](../Party/party-data.md).
- Platform online achievements: `0x002536A0` is called by `0x00315390`, `0x00315420`, `0x003154B0`, `0x00315820`, `0x00315E90`,
  `0x003162E0`, `0x00316440`, `0x00316670`, `0x003166F0`, `0x00316810`, `0x00316930`, `0x00316A50`; `0x002536A0` is also called by
  `0x00316BF0`, `0x00316C60`; `0x00316810` calls `0x00316760`; `0x00584210` calls `0x00316810`.
- Platform online achievements: those functions are documented on
  [shops](../Items-Equipment-Shops-And-Licenses/shops.md), [jump thunks](../Engine-Core/jump-thunks.md),
  [handbook files](../Game-Files-And-Data-Tables/handbook-files.md),
  [gil](../Rewards-EXP-Gil-And-Loot/gil.md), [achievements](../Steam-And-Achievements/achievements.md).
- Platform online achievements: and on [item use](../Items-Equipment-Shops-And-Licenses/item-use.md),
  [save file format](save-file-format.md), [frame update order](../Engine-Core/frame-update-order.md),
  [debug menu](../Engine-Core/debug-menu.md).
- Presentation: `0x001EDEC0` is called by `0x002B7B80`, `0x002BAF80`, `0x002BC3E0`, `0x002D2DB0`, `0x00366B80`; `0x002527B0` is
  called by `0x00579420`.
- Presentation: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md), [controls](../Controls-And-Input/controls.md),
  [menu lists](../Menus-And-HUD/menu-lists.md), [escape](../Controls-And-Input/escape.md),
  [quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md).
- RNG random selection: `0x00584210` calls `0x00379CF0`; those functions are documented on
  [startup constants](../Engine-Core/startup-constants.md).
- Resource: `0x00314440` calls `0x001D6C40`; `0x00314530` calls `0x001D6C40`; `0x00394070` calls `0x0024A680`; `0x00394460` calls
  `0x001D6C60`; those functions are documented on
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [verb table](../Scripts-And-Script-Commands/verb-table.md),
  [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md).
- Script VM: `0x00254CB0` is called by `0x0050D9A0`, `0x0050ED70`, `0x0050EEA0`, `0x0050EF50`, `0x0050F0A0`; `0x002EFA70` is called
  by `0x003559B0`, `0x00355EB0`, `0x00356270`, `0x00356650`, `0x00356A50`, `0x00356FE0`; `0x00314440` is called by `0x00355350`,
  `0x0050C8A0`; `0x00314DC0` is called by `0x0034A770`; `0x0036FCC0` is called by `0x0050C800`, `0x0050D9A0`; `0x00394460` is called
  by `0x00511EA0`.
- Script VM: those functions are documented on
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md),
  [shared zone script actors](../Story-Events-And-Hunts/shared-zone-script-actors.md),
  [screen fades](../Graphics/screen-fades.md).
- Script VM: and on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [debug menu](../Engine-Core/debug-menu.md), [starting inventory](../Party/starting-inventory.md).
- Story event quest hunt: `0x002EF2D0` calls `0x00379160`; those functions are documented on
  [story flags](../Story-Events-And-Hunts/story-flags.md).
- UI: `0x001EDEC0` is called by `0x00252030`, `0x00276D30`, `0x0027C870`, `0x00299090`, `0x0029A0A0`, `0x002B6DB0`, `0x002BE490`,
  `0x0035D6B0`, `0x003C95C0`, `0x003EEEC0`, `0x003EF2E0`, `0x005528C0`; `0x001EDEC0` is also called by `0x005542D0`; `0x00237DF0`
  calls `0x00313840`.
- UI: `0x00244960` is called by `0x0023ED80`, `0x00252030`, `0x00276D30`, `0x002778C0`, `0x00279E20`, `0x0027AD70`, `0x00298250`,
  `0x002985D0`, `0x0029BB40`, `0x0029C770`, `0x0029C850`, `0x0029C9D0`; `0x00244960` is also called by `0x002B6350`, `0x002B9D30`,
  `0x002BDCE0`, `0x002BFB40`, `0x002C9BF0`, `0x003CA310`, `0x003CA860`, `0x003CAE00`, `0x003CB0C0`, `0x003CB650`, `0x003F8790`,
  `0x00551E00`.
- UI: `0x00244960` is also called by `0x00551F00`, `0x005528C0`, `0x00567200`, `0x0056C170`; `0x002527B0` is called by `0x00280DE0`,
  `0x003FDAD0`, `0x005651E0`, `0x00565E00`, `0x00566680`, `0x0056F810`; `0x002678C0` calls `0x002509A0`; `0x002EFA70` is called by
  `0x0027EFA0`; `0x00314440` calls `0x00254AC0`; `0x00582860` calls `0x002814E0`.
- UI: those functions are documented on [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md),
  [force fight mode](../Engine-Core/force-fight-mode.md), [battle menu](../Menus-And-HUD/battle-menu.md),
  [menu screens](../Menus-And-HUD/menu-screens.md), [widget messages](../Menus-And-HUD/widget-messages.md).
- UI: and on [action availability](../Controls-And-Input/action-availability.md), [hud](../Menus-And-HUD/hud.md),
  [game over](../World-Areas-And-Travel/game-over.md),
  [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [map screens](../Menus-And-HUD/map-screens.md).
- UI: and on [party control modes](../Engine-Core/party-control-modes.md),
  [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [tutorial battle commands](../Battle-Actions/tutorial-battle-commands.md).
- UI: and on [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md),
  [party list](../Menus-And-HUD/party-list.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md),
  [controls](../Controls-And-Input/controls.md), [inventory screen](../Menus-And-HUD/inventory-screen.md),
  [dialogs](../Menus-And-HUD/dialogs.md).
- UI: and on [text handbook unrequested](../Menus-And-HUD/text-handbook-unrequested.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md); and on
  [clan primer](../Menus-And-HUD/clan-primer.md).
- World area: `0x002EF2D0` is called by `0x00266D10`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
- World area: `0x002EF640` is called by `0x00229B40`, `0x003145E0`, `0x005843E0`; `0x002EFA70` is called by `0x00314440`,
  `0x00314530`, `0x003145E0`; `0x00314440` calls `0x003145E0`; `0x00314440` is called by `0x003318C0`, `0x00331920`; `0x0036FCC0`
  calls `0x00267C90`, `0x00268320`; `0x00394130` calls `0x00267C90`, `0x00268320`, `0x00314440`, `0x00314DC0`; `0x00582860` calls
  `0x005843E0`; `0x00584210` calls `0x00269A20`, `0x00314DC0`.
- World area: those functions are documented on [script variables](../Scripts-And-Script-Commands/script-variables.md),
  [changing areas](../World-Areas-And-Travel/changing-areas.md), [debug menu](../Engine-Core/debug-menu.md),
  [game application](../Engine-Core/game-application.md).
- World area: and on [frame update order](../Engine-Core/frame-update-order.md),
  [game over](../World-Areas-And-Travel/game-over.md).
