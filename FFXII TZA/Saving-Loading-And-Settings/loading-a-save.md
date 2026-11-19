[Home](../../README.md) / [Saving, loading and settings](README.md) / Loading a save

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Loading a save: the steps from choosing a slot to the party standing where it saved | operation | Saving, loading and settings | Saving and loading | The order in which a load runs: the save and load screen opened from the title or a save crystal, the slot read into the active image, the load-complete call that binds the party block, the screen's post-load calls, the area controller's restore steps the game logs by name and the options the loaded save brings with it; and how New Game differs: its own widget keeps the title's options across the image reset. | 0x00580EB0, 0x00582860, 0x00280A00, 0x00280140, 0x00285E60, 0x00394400, 0x00394130, 0x00512130, 0x00255260, 0x002EF640, 0x002EF650, 0x00233C10, 0x002CFD10, 0x00268320, 0x00267C90, 0x00314530, 0x00360D50, 0x002DE050, 0x00584210 |

## What the player sees

The player picks Load and a slot. "Loading..." shows, then "Load complete."; the screen fades, and the party appears
where the save was made.

The slot's file is read whole into the game's live save image, the in-game options record included. The party
data is then pointed at that image, the area is started again from the zone-change record stored in it, and the
options stored in the save take effect: the Config screen's options are the ones the player had when saving.

## Steps

| Step | What happens | Where in the code |
|---|---|---|
| 1 | **The screen opens.** On the title, commands 1 and 5 store the load mode with `unkCall_7067` (2 for command 1, 3 for command 5), which `0x00394630` keeps at `0x02AEE4D8`, and open the save and load screen with `openfullscreenmenu_48d(0x8005, 1)` (`ttl_a01` `ゲームスタート処理.ロード画面起動`).<br>• Save crystals open the same screen with `openfullscreenmenu_48d(0x8005, 0)`, 1,146 calls in the us scripts ([save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md)). |   |
| 2 | **The mode screen.** The request reaches `0x00280A00` through the default arm of `0x00254B50`, and `0x00280A00` spawns the mode-screen task `0x0027FB70` and the area controller `0x00280140`, `0xD8` bytes each ([game over](../World-Areas-And-Travel/game-over.md)). | `0x00254C39` |
| 3 | **The read.** State 8 of the save and load screen queues the storage requests that read the slot's file into the active image, `0x56690` bytes ([saving and loading](saving-and-loading-screen.md#the-save-and-load-screen), [save file format](save-file-format.md)). |   |
| 4 | **Load complete.** State 9 reports the load ([saving and loading](saving-and-loading-screen.md#the-save-and-load-screen)). On message 12 with code `0x10` the screen `0x00582860` records the load mode (`0x00238A30(1)` for mode 3, else `0x00238A30(0)`) and calls `0x00285E60(-1)`, which sets bits `0x200` and `0x400` of the area controller's word `[0x0209AC30] + 0x400` and runs steps 5 and 6. | `0x00582CBA`-`0x00582CE6`<br>`0x00285E64`-`0x00285E7C` |
| 5 | **`btlCallBackAfterReadSaveRam()`.** `0x00233C10` binds the party block `0x02EBF190` to the loaded image ([save data fields](save-data-fields.md), [party data](../Party/party-data.md)).<br>• It binds only while the pointer is empty, and then runs the battle reset `0x00237DF0` twice.<br>• With the pointer set it checks the magic `0x05071901`: a wrong magic runs `0x00237DF0`, and a match keeps the block, whose first `0x6000` bytes the prelude `0x00235AF0` has replaced with the image's copy at `+0x2200` when the two differ, and runs the steps listed on [party data](../Party/party-data.md). | `0x00285E86`<br>`0x00233C3F`, `0x00233C48`<br>`0x00233C4D`<br>`0x00233C59`<br>`0x00233C14`, `0x00235B76` |
| 6 | **`YsSaveRam_CallBackInit()`.** `0x002CFD10` (`0x00285E92`, whose argument it ignores) clears entry 4 of the menu cursor bank 6 (`0x002527B0(6, 4, 0)`) and the battle menu's cursor block, `[0x0209BE80] + 0xAA60`, `0xC4` bytes ([battle menu](../Menus-And-HUD/battle-menu.md)). `0x0028E880` does nothing while `[0x0209BE80]` is null. | `0x0028E880`<br>`0x0028E887`-`0x0028E88A` |
| 7 | **The post-load sequence.** On message `0x12`, with bit `0x10` of its `+0xC4` set, the screen runs its post-load calls:<br>• while its byte `+0x598` is clear, `0x001831A0`, the load flag `0x0209AC10` = 1, `0x005843E0` and `0x00182D40`;<br>• `0x00394400`, when `0x00394520` finds it, sends a close request to the title asset at `0x02AEE4C0`, the `0x00394070` widget that `0x00394460` creates;<br>• `0x00584210` handles the mode-3 stash or its restore, calls `0x00316810` and reseeds the gameplay generator from the clock ([saving and loading](saving-and-loading-autosave.md#what-a-load-runs), [save file format](save-file-format.md)). | `0x00582E81`-`0x00582EBA`<br>`0x00244F00`, `0x0039440A`<br>`0x00394495`-`0x003944A4`<br>`0x00584398` |
| 8 | **`AtelRefreshByLoad()`.** When the mode screen closes, the area controller's message `0x12` finds bit `0x200`, clears bits `0x200` and `0x400` and runs `0x00268320`, which resets the scripts' scratch variables ([script variables](../Scripts-And-Script-Commands/script-variables.md)).<br>• It zeroes `scratch1` always.<br>• Only while the load flag `0x0209AC10` is 0 does it zero `scratch2` (`0x02099FF0`, when `0x01E0C3EC` is also non-zero, `0x00268324`-`0x00268345`) and set the zone transition record's `initState`, payload `+0x1061`, to 1; step 7 sets the flag to 1 while the screen's byte `+0x598` is clear.<br>• With `0x0020E5A0()` at 5 the controller then clears payload `+0x1061` and runs `0x0020E4E0`. | `0x002801DA`-`0x002801F8`<br>`0x002801FF`<br>`0x02099DF0`<br>`0x00268359`<br>`0x0026835E`-`0x0026836C`<br>`0x00280204`-`0x0028021A` |
| 9 | **`AtelMapJumpByLoad()`.** `0x00267C90` jumps to the restore path `0x00314530`, which requests the actor managers and starts the zone change from the transition record in the payload; the change runs from its staging on ([changing areas](../World-Areas-And-Travel/changing-areas.md), [zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md#staging-and-the-transition-record)). | `0x0028021F` |
| 10 | **`YsConfig_Load()`.** The controller then calls `0x00360D50`, which sets `0x022CBA60` to 1.<br>• The music code clears it and runs `0x002DE050` once the new area's music is settled: `0x00360D30` or the music task `0x00361080` ([music](../Sound-And-Music/music.md)).<br>• `0x002DE050` runs the options applier `0x002DDA30(0)`, which applies the loaded record and skips the FF12CONFIG overrides ([game settings](game-settings.md)). | `0x00280224`<br>`0x002620C5`-`0x002620D0`<br>`0x0036114F`-`0x0036115E` |
| 11 | **A failed header.** While the controller's state byte `[0x0209AC30] + 0x400` is 1 and `0x0032E4D0` answers 0, its frame message passes the image header `+0x68` to the test `0x00255260` ([save file format](save-file-format.md)).<br>• A pass runs `0x00233C10` and `0x002CFD10`.<br>• A failure resets the image with `0x002EF650` and sets bit `0x100`; on close the controller then asks for map 0 through `0x00314440`, or runs `0x003603E0` in mode `0xC`. | `0x00280369`-`0x00280377`<br>`0x002803B8`-`0x002803C0`<br>`0x0028037B`<br>`0x00280262`-`0x0028027C` |

The step names are the game's own: `0x0036FCC0` runs the same calls with a log line before each¹,
and before them `AtelLockSystemAndBattleByMapJump()`, `0x002678C0`, which raises stop request 19
([time stop and freeze](../Engine-Core/time-stop-and-freeze.md)). Only the debug verbs
`debug_load_mapjump`² and `debug_loadjfdata`³ reach `0x0036FCC0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00D10FD0`-`0x00D11090` |
| ² | `0x0050C800` |
| ³ | `0x0050D9A0` |

</details>

New Game does not run the load steps. `fsttl_newgamestart` (verb `0x705D`, result callback `0x00512130`, a jump to
`0x00394640`) builds the `0xF0`-byte new-game widget `0x00394130` only while `0x02AEE4D0` is 0
([verb table](../Scripts-And-Script-Commands/verb-table.md)). The title calls it after the New Game list, and the
staff-roll and Trial Mode questions after `btlAtelResetNgPlus` or `btlAtelResetNgMinus`
([New Game+ and New Game-](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md)). On its first message it:

- sets its state `+0xC0` and its counter `+0xC2` to 0 and keeps itself in `0x02AEE4D0`¹,
  which `0x00394640` tests so that it creates only one widget ([widgets](../Menus-And-HUD/widgets.md));
- zeroes the active image's play clock (`+0x10` and the dword at `+0x18`, `0x003942B9`-`0x003942BD`)
  ([save file format](save-file-format.md));
- keeps the in-game options, the `0x28`-byte record at `0x002536A0() + 8`, at its `+0xC8`²:
  on the title these are the defaults that `fsttl_initialize` installs (`0x00394460` runs `0x002DDE60` at `0x00394481`)
  ([game settings](game-settings.md));
- stores 1 at `0x020927C8`³ ([controls](../Controls-And-Input/controls.md));
- resets the active image with `0x002EF650`⁴, which clears its `0x56690` bytes at `0x02164280`
  (`memset`, `0x002EF663`), calls the empty `0x0016D6A0(0)`⁵ and runs `0x00253A80`, `0x002EF2D0` and
  `0x00238A80`, the last as a tail jump⁶; `0x00253A80` installs the option defaults again
 ⁷ and writes the header magic⁸
  ([save file format](save-file-format.md));
- sets the pending preset byte `0x0208D455` to 0⁹
  ([scenario presets](../Party/scenario-presets.md));
- stores `0x112` as the transition record's destination field¹⁰
  ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md#staging-and-the-transition-record));
- starts fade slot 2 over 15 frames¹¹ and sets a 30-frame counter¹²
  ([screen fades](../Graphics/screen-fades.md));
- attaches itself to the parent `[0x0208EA28]` with `0x00244960`¹³, and returns 0
  ([widgets](../Menus-And-HUD/widgets.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003942A4`-`0x003942B2` |
| ² | `0x003942C0`-`0x003942E5` |
| ³ | `0x00254CB0`, `0x003942ED` |
| ⁴ | `0x003942F2` |
| ⁵ | `0x002EF66A` |
| ⁶ | `0x002EF656`-`0x002EF67D` |
| ⁷ | `0x002DDE60`, `0x00253B2A` |
| ⁸ | `0x00253AED`-`0x00253AFB` |
| ⁹ | `0x0023A110`, `0x003942F9` |
| ¹⁰ | `0x00314DC0`, `0x003942FE`-`0x00394303` |
| ¹¹ | `0x002EFA70`, `0x00394315` |
| ¹² | `0x0039431A`-`0x00394322` |
| ¹³ | `0x00394329`-`0x00394330` |

</details>

When its counter has run out, the widget passes the image header `+0x68`¹ to
`0x00255260`, which accepts a pair of zero dwords or the magic `0x0131F3EA` followed by the size `0x4818`²; the payload begins at image `+0x200`, and the rebuilt image carries the magic.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EF640`, `0x003941D3`-`0x003941DC` |
| ² | `0x00255265`-`0x00255283` |

</details>

- A failed test resets the image again¹, clears the cursors² and asks
  for map 0 through the jump funnel `0x00314440`³
  ([changing areas](../World-Areas-And-Travel/changing-areas.md)).
- A passed test runs `0x0016D6A0`, `0x00233C10` and `0x002CFD10`⁴, writes the kept options back over
  the new image's record⁵ and runs `0x00268320`, `0x00267C90` and `0x002DE050`
 ⁶ ([saving and loading](saving-and-loading-autosave.md#what-a-load-runs)). The new game starts in
  field `0x112` with the options in force on the title.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EF650`, `0x003941E5` |
| ² | `0x002CFD10`, `0x003941ED` |
| ³ | `0x003941FC` |
| ⁴ | `0x0039421D`-`0x0039422A` |
| ⁵ | `0x00394234`-`0x00394252` |
| ⁶ | `0x00394257`-`0x00394261` |

</details>

The widget's handler `0x00394130` acts on messages 1, 2 and `0x12`. Message 2, the frame message, does nothing while
`0x001EDEC0(+0xB4)` returns 0, which it does only with the 60 fps gate `0x01F82E38` set, `0x01DFE0C0` at 0 and an odd
`+0xB4`¹. Otherwise it counts `+0xC2` down to 0² and runs the state
`+0xC0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00394184`-`0x00394191` |
| ² | `0x00394197`-`0x003941A6` |

</details>

In state 0 it stores 0 at `0x020927C8` (`0x00254CB0(0)`) and moves to state 1¹. In state 1,
once the counter is 0, it runs the header test and the calls above, or the failed-test path; both end
with a close request on the widget² and state 2³.
State 1 with the counter still running, state 2 and any other state do nothing⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00394282`-`0x0039428B` |
| ² | `0x00244F00`, `0x00394204`, `0x00394269` |
| ³ | `0x0039420B`, `0x00394270` |
| ⁴ | `0x003941BF`, `0x003941CD` |

</details>

Message `0x12` sends a close request to the object at `0x02AEE4C0` when there is one¹ and
clears `0x02AEE4D0`². It and every message other than 1 and 2 then go to the shared return-zero stub
`0x005C5230`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00394155`-`0x00394161` |
| ² | `0x00394168` |
| ³ | `0x0039417F` |

</details>

## Outcomes

- The party block points at the loaded image, and the scripts start the zone from its transition record.
- The in-game options are the loaded save's own: `0x002DDA30(0)` applies its record and skips the FF12CONFIG
  overrides. A new game keeps the options in force on the title instead.
- The menu and battle-menu cursors start from their defaults.
- The gameplay generator is reseeded from the clock, so a reload does not repeat earlier rolls.

## Related

- [Saving and loading](saving-and-loading.md): the screen, the storage queue and the save transaction.
- [Save file format](save-file-format.md): the container and the payload a load reads.
- [Changing areas](../World-Areas-And-Travel/changing-areas.md): the zone change the restore jump starts.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 147 calls with 36 other topics</summary>

**Characters and objects** (explained on [party data](../Party/party-data.md), [script requests](../Scripts-And-Script-Commands/script-requests.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x00329CC0`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) Battle slot map: initialize mapping classes (on strong and weak mode) |
| [`0x002678C0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) | is called by | [`0x0025B600`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) |
| [`0x002EFA70`](../Graphics/screen-fades.md) (on screen fades) | is called by | [`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts) |

**Sound and music** (explained on [config screen](../Menus-And-HUD/config-screen.md), [music](../Sound-And-Music/music.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002DDA30`](game-settings.md) (on game settings) | calls | [`0x002DF530`](game-settings.md) (on game settings) |
| [`0x002DE050`](loading-a-save.md) | is called by | [`0x00360D30`](../Sound-And-Music/music.md) (on music)<br>[`0x00361080`](../Sound-And-Music/music.md) (on music) |

**Enemy AI and gambits** (explained on [unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00233C10`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | calls | [`0x00327F80`](../Party/party-data.md) Gambit runtime: rebuild all order sets (on party data) |

**Battle actions** (explained on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00314440`](../World-Areas-And-Travel/changing-areas.md) (on changing areas) | is called by | [`0x00319F50`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle actor timeline event (on ko and game over) |

**Damage and battle formulas** (explained on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x0023AC80`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: initialize definition record (on equipment) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md), [enemy respawning](../Enemy-Spawning/enemy-respawning.md), [global state accessors](../Engine-Core/global-state-accessors.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00233C10`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | calls | [`0x00229ED0`](game-settings.md) (on game settings) |
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x00229ED0`](game-settings.md) (on game settings)<br>[`0x0032A160`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x002EF650`](loading-a-save.md) | is called by | [`0x0022B6E0`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |
| [`0x00394130`](loading-a-save.md) | calls | [`0x001EDEC0`](saving-and-loading-screen.md) (on saving and loading screen) |
| [`0x00582860`](saving-and-loading-screen.md) (on saving and loading screen) | calls | [`0x001EDEC0`](saving-and-loading-screen.md) (on saving and loading screen) |

**Gameplay** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00233C10`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | calls | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x00238A80`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) | calls | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x00394460`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | calls | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |

**Controls and input** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [config screen](../Menus-And-HUD/config-screen.md), [vibration](../Controls-And-Input/vibration.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002678C0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) | calls | [`0x00226BE0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock) |
| [`0x002DDA30`](game-settings.md) (on game settings) | calls | [`0x001E0FF0`](game-settings.md) (on game settings)<br>[`0x001E1020`](game-settings.md) (on game settings)<br>[`0x0035FF30`](game-settings.md) (on game settings) |
| [`0x00314440`](../World-Areas-And-Travel/changing-areas.md) (on changing areas) | calls | [`0x00182D80`](loading-a-save.md)<br>[`0x00408B00`](../Controls-And-Input/controls.md) (on controls) |
| [`0x00314530`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: requeue current field for restore (on zone changes and mapjump) | calls | [`0x00182D80`](loading-a-save.md) |
| [`0x00394460`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | calls | [`0x002501E0`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) |
| [`0x00582860`](saving-and-loading-screen.md) (on saving and loading screen) | calls | [`0x00182D40`](saving-and-loading-autosave.md) (on saving and loading autosave) |

**Items, equipment, shops and licenses** (explained on [item and ability ids](../Engine-Core/item-and-ability-ids.md), [party data](../Party/party-data.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00233C10`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | calls | [`0x0030B6A0`](../Items-Equipment-Shops-And-Licenses/inventory.md) Inventory runtime: rebase class descriptors and clear derived state (on inventory) |
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x0023AF50`](../Party/starting-inventory.md) Inventory: initialize primary state from authored table (on starting inventory) |
| [`0x00238A80`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) | calls | [`0x0030B6A0`](../Items-Equipment-Shops-And-Licenses/inventory.md) Inventory runtime: rebase class descriptors and clear derived state (on inventory) |

**Steam and achievements** (explained on [shops](../Items-Equipment-Shops-And-Licenses/shops.md), [jump thunks](../Engine-Core/jump-thunks.md), [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [gil](../Rewards-EXP-Gil-And-Loot/gil.md), [achievements](../Steam-And-Achievements/achievements.md), [item use](../Items-Equipment-Shops-And-Licenses/item-use.md), [save file format](save-file-format.md), [frame update order](../Engine-Core/frame-update-order.md), [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002536A0`](loading-a-save.md) | is called by | [`0x00315390`](../Items-Equipment-Shops-And-Licenses/shops.md) (on shops)<br>[`0x00315420`](../Menus-And-HUD/clan-primer-entries.md) (on clan primer entries)<br>[`0x003154B0`](../Menus-And-HUD/clan-primer-entries.md) (on clan primer entries)<br>[`0x00315820`](../Enemy-Spawning/bestiary.md) (on bestiary)<br>[`0x00315E90`](../Steam-And-Achievements/achievements.md) (on achievements)<br>[`0x003162E0`](../Steam-And-Achievements/achievements.md) (on achievements)<br>[`0x00316440`](../Steam-And-Achievements/achievements.md) (on achievements)<br>[`0x00316670`](../Steam-And-Achievements/achievements.md) (on achievements)<br>[`0x003166F0`](../Steam-And-Achievements/achievements.md) (on achievements)<br>[`0x00316810`](../Steam-And-Achievements/achievements.md) (on achievements)<br>[`0x00316930`](../Steam-And-Achievements/achievements.md) (on achievements)<br>[`0x00316A50`](../Steam-And-Achievements/achievements.md) (on achievements) |
| [`0x002536A0`](loading-a-save.md) | is also called by | [`0x00316BF0`](../Steam-And-Achievements/achievements.md) (on achievements)<br>[`0x00316C60`](../Menus-And-HUD/menu-screens.md) (on menu screens) |
| [`0x00316810`](../Steam-And-Achievements/achievements.md) (on achievements) | calls | [`0x00316760`](../Steam-And-Achievements/achievements.md) (on achievements) |
| [`0x00584210`](save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) | calls | [`0x00316810`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Graphics** (explained on [frame update order](../Engine-Core/frame-update-order.md), [controls](../Controls-And-Input/controls.md), [menu lists](../Menus-And-HUD/menu-lists.md), [escape](../Controls-And-Input/escape.md), [quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001EDEC0`](saving-and-loading-screen.md) (on saving and loading screen) | is called by | [`0x002B7B80`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002BAF80`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x002BC3E0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x002D2DB0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00366B80`](../Controls-And-Input/escape.md) (on escape) |
| [`0x002527B0`](../Menus-And-HUD/dialogs.md) (on dialogs) | is called by | [`0x00579420`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) |

**Random numbers** (explained on [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00584210`](save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) | calls | [`0x00379CF0`](../Engine-Core/startup-constants.md) (on startup constants) |

**Game files and data tables** (explained on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [verb table](../Scripts-And-Script-Commands/verb-table.md), [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00314440`](../World-Areas-And-Travel/changing-areas.md) (on changing areas) | calls | [`0x001D6C40`](loading-a-save.md) |
| [`0x00314530`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: requeue current field for restore (on zone changes and mapjump) | calls | [`0x001D6C40`](loading-a-save.md) |
| [`0x00394070`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | calls | [`0x0024A680`](../Game-Files-And-Data-Tables/handbook-files.md) (on handbook files) |
| [`0x00394460`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | calls | [`0x001D6C60`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) |

**Scripts and script commands** (explained on [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [shared zone script actors](../Story-Events-And-Hunts/shared-zone-script-actors.md), [screen fades](../Graphics/screen-fades.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [debug menu](../Engine-Core/debug-menu.md), [starting inventory](../Party/starting-inventory.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00254CB0`](loading-a-save.md) | is called by | [`0x0050D9A0`](save-file-format.md) (on save file format)<br>[`0x0050ED70`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors)<br>[`0x0050EEA0`](saving-and-loading-transaction.md) (on saving and loading transaction)<br>[`0x0050EF50`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors)<br>[`0x0050F0A0`](saving-and-loading-transaction.md) (on saving and loading transaction) |
| [`0x002EFA70`](../Graphics/screen-fades.md) (on screen fades) | is called by | [`0x003559B0`](../Graphics/screen-fades.md) (on screen fades)<br>[`0x00355EB0`](../Graphics/screen-fades.md) (on screen fades)<br>[`0x00356270`](../Graphics/screen-fades.md) (on screen fades)<br>[`0x00356650`](../Graphics/screen-fades.md) (on screen fades)<br>[`0x00356A50`](../Graphics/screen-fades.md) (on screen fades)<br>[`0x00356FE0`](../Graphics/screen-fades.md) (on screen fades) |
| [`0x00314440`](../World-Areas-And-Travel/changing-areas.md) (on changing areas) | is called by | [`0x00355350`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x0050C8A0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) |
| [`0x00314DC0`](loading-a-save.md) World transition: set active or pending field id | is called by | [`0x0034A770`](loading-a-save.md) |
| [`0x0036FCC0`](loading-a-save.md) | is called by | [`0x0050C800`](loading-a-save.md)<br>[`0x0050D9A0`](save-file-format.md) (on save file format) |
| [`0x00394460`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | is called by | [`0x00511EA0`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) |

**Story, events and hunts** (explained on [story flags](../Story-Events-And-Hunts/story-flags.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002EF2D0`](../Story-Events-And-Hunts/story-flags.md) (on story flags) | calls | [`0x00379160`](../Story-Events-And-Hunts/story-flags.md) (on story flags) |

**Menus and HUD** (explained on [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md), [force fight mode](../Engine-Core/force-fight-mode.md), [battle menu](../Menus-And-HUD/battle-menu.md), [menu screens](../Menus-And-HUD/menu-screens.md), [widget messages](../Menus-And-HUD/widget-messages.md), [action availability](../Controls-And-Input/action-availability.md), [hud](../Menus-And-HUD/hud.md), [game over](../World-Areas-And-Travel/game-over.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [map screens](../Menus-And-HUD/map-screens.md), [party control modes](../Engine-Core/party-control-modes.md), [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [tutorial battle commands](../Battle-Actions/tutorial-battle-commands.md), [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md), [party list](../Menus-And-HUD/party-list.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [controls](../Controls-And-Input/controls.md), [inventory screen](../Menus-And-HUD/inventory-screen.md), [dialogs](../Menus-And-HUD/dialogs.md), [text handbook unrequested](../Menus-And-HUD/text-handbook-unrequested.md), [frame update order](../Engine-Core/frame-update-order.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [clan primer](../Menus-And-HUD/clan-primer.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001EDEC0`](saving-and-loading-screen.md) (on saving and loading screen) | is called by | [`0x00252030`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00276D30`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x0027C870`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00299090`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x0029A0A0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x002B6DB0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x002BE490`](../Menus-And-HUD/battle-menu.md) (on battle menu)<br>[`0x0035D6B0`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x003C95C0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x003EEEC0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x003EF2E0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x005528C0`](../Menus-And-HUD/map-screens.md) (on map screens) |
| [`0x001EDEC0`](saving-and-loading-screen.md) (on saving and loading screen) | is also called by | [`0x005542D0`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x00313840`](../Engine-Core/party-control-modes.md) (on party control modes) |
| [`0x00244960`](loading-a-save.md) | is called by | [`0x0023ED80`](../Menus-And-HUD/config-screen.md) (on config screen)<br>[`0x00252030`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00276D30`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x002778C0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x00279E20`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x0027AD70`](../Menus-And-HUD/battle-menu.md) (on battle menu)<br>[`0x00298250`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x002985D0`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x0029BB40`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x0029C770`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x0029C850`](saving-and-loading-autosave.md) (on saving and loading autosave)<br>[`0x0029C9D0`](../Menus-And-HUD/party-list.md) (on party list) |
| [`0x00244960`](loading-a-save.md) | is also called by | [`0x002B6350`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002B9D30`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002BDCE0`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x002BFB40`](../Menus-And-HUD/battle-menu.md) (on battle menu)<br>[`0x002C9BF0`](../Menus-And-HUD/shop-screens.md) (on shop screens)<br>[`0x003CA310`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x003CA860`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x003CAE00`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x003CB0C0`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x003CB650`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x003F8790`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x00551E00`](loading-a-save.md) |
| [`0x00244960`](loading-a-save.md) | is also called by | [`0x00551F00`](loading-a-save.md)<br>[`0x005528C0`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x00567200`](../Menus-And-HUD/menu-screens.md) (on menu screens)<br>[`0x0056C170`](../Menus-And-HUD/menu-screens.md) (on menu screens) |
| [`0x002527B0`](../Menus-And-HUD/dialogs.md) (on dialogs) | is called by | [`0x00280DE0`](../Menus-And-HUD/opening-the-main-menu.md) (on opening the main menu)<br>[`0x003FDAD0`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen)<br>[`0x005651E0`](../Menus-And-HUD/inventory-screen.md) (on inventory screen)<br>[`0x00565E00`](../Game-Files-And-Data-Tables/battle-text-tables.md) (on battle text tables)<br>[`0x00566680`](../Menus-And-HUD/dialogs.md) (on dialogs)<br>[`0x0056F810`](../Menus-And-HUD/dialogs.md) (on dialogs) |
| [`0x002678C0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) | calls | [`0x002509A0`](../Menus-And-HUD/hud.md) (on hud) |
| [`0x002EFA70`](../Graphics/screen-fades.md) (on screen fades) | is called by | [`0x0027EFA0`](../Menus-And-HUD/menu-screens.md) (on menu screens) |
| [`0x00314440`](../World-Areas-And-Travel/changing-areas.md) (on changing areas) | calls | [`0x00254AC0`](../World-Areas-And-Travel/changing-areas.md) (on changing areas) |
| [`0x00582860`](saving-and-loading-screen.md) (on saving and loading screen) | calls | [`0x002814E0`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) |

**World, areas and travel** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [script variables](../Scripts-And-Script-Commands/script-variables.md), [changing areas](../World-Areas-And-Travel/changing-areas.md), [debug menu](../Engine-Core/debug-menu.md), [game application](../Engine-Core/game-application.md), [frame update order](../Engine-Core/frame-update-order.md), [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002EF2D0`](../Story-Events-And-Hunts/story-flags.md) (on story flags) | is called by | [`0x00266D10`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x002EF640`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) | is called by | [`0x00229B40`](save-data-fields.md) World transition snapshot: capture runtime state (on save data fields)<br>[`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump)<br>[`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships) |
| [`0x002EFA70`](../Graphics/screen-fades.md) (on screen fades) | is called by | [`0x00314440`](../World-Areas-And-Travel/changing-areas.md) (on changing areas)<br>[`0x00314530`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: requeue current field for restore (on zone changes and mapjump)<br>[`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump) |
| [`0x00314440`](../World-Areas-And-Travel/changing-areas.md) (on changing areas) | calls | [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump) |
| [`0x00314440`](../World-Areas-And-Travel/changing-areas.md) (on changing areas) | is called by | [`0x003318C0`](game-settings.md) (on game settings)<br>[`0x00331920`](game-settings.md) (on game settings) |
| [`0x0036FCC0`](loading-a-save.md) | calls | [`0x00267C90`](loading-a-save.md)<br>[`0x00268320`](../World-Areas-And-Travel/weather.md) World persistence: reset banks and mark initialization state (on weather) |
| [`0x00394130`](loading-a-save.md) | calls | [`0x00267C90`](loading-a-save.md)<br>[`0x00268320`](../World-Areas-And-Travel/weather.md) World persistence: reset banks and mark initialization state (on weather)<br>[`0x00314440`](../World-Areas-And-Travel/changing-areas.md) (on changing areas)<br>[`0x00314DC0`](loading-a-save.md) World transition: set active or pending field id |
| [`0x00582860`](saving-and-loading-screen.md) (on saving and loading screen) | calls | [`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships) |
| [`0x00584210`](save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) | calls | [`0x00269A20`](save-data-fields.md) World persistence: import group persistent bank (on save data fields)<br>[`0x00314DC0`](loading-a-save.md) World transition: set active or pending field id |

**Enemy spawning** (explained on [enemy respawning](../Enemy-Spawning/enemy-respawning.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships) | calls | [`0x00233550`](save-data-fields.md) Spawn keep: restore persistence bank (on save data fields) |

</details>

---

[← Saving and loading](saving-and-loading.md) | [Save file format →](save-file-format.md)
