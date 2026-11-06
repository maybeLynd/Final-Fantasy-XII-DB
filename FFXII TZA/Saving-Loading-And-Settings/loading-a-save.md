---
title: "Loading a save: the steps from choosing a slot to the party standing where it saved"
kind: "operation"
category: "Saving, loading and settings"
addresses: "0x00580EB0, 0x00582860, 0x00394400, 0x00394130, 0x00512130, 0x00255260, 0x002EF640, 0x002EF650, 0x00233C10, 0x002CFD10, 0x00268320, 0x00267C90, 0x00314530, 0x002DE050, 0x00584210"
---

## What the player sees

The player picks Load and a slot. "Loading..." shows, then "Load complete."; the screen fades, and the party appears
where the save was made.

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
