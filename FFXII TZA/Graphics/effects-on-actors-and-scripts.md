[Home](../../README.md) / [Graphics](README.md) / Effects on actors and scripts

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Effects on actors and scripts: numbered effects on actors and the script effect slots | system | Graphics | Visual effects / Effects On Characters And Menus | How actors and scripts start effects: numbered effects played on an owner and its targets with their request table, and the 32 script effect slots event scripts load and play effects through. | 0x0024B270 |

## What the player sees

Abilities and events play numbered effects on a character and its targets, and event scripts load
and play effects of their own.

## How it works

### Numbered effects on actors

`0x003B02A0(owner, targets, count, number, kind)` plays effect `number` as an instance of kind 5, 6 or 9
and refuses any other kind. Unless the request kind below is 1, it also refuses when
`0x002FC9B0()` plus `0x003B0B70()` exceeds 23, `0x002FC9B0() + 0x003B0B70() >= 0x18`¹. It makes
the instance² with state 2 and the number in `+0x373`, stores the owner at `+0x08`, and appends each
target whose render record is live and passes `0x002E9FE0` to the target array `+0x10`. Numbers 100 to 103 and
`0x94` are kind-3 requests in the table below.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B0377`-`0x003B0388` |
| ² | `0x0024B270` |

</details>

The requests sit in 36 entries of `0x18` bytes at `0x02EBEC00`, packed from the start:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` |  | handle: kind << 28 \| serial (`0x02EBEF60`) |
| `+0x04` | `u32` |  | set by `0x003B0FD0` |
| `+0x08` | `void*` |  | the instance |
| `+0x10` | `u8` |  | effect number |
| `+0x11` | `u8` | target test |  |
| `+0x12` | `u8` | kind |  |
| `+0x13` | `u8` |  | bits `0x6`: request kind (3 for 100-103 and `0x94`, 1 when the number's `0x01EFE260` byte is 1, else 0) |

- `0x003B0980` returns the first free entry; with all 36 taken it ends the first instance whose
  request kind is 0 or 3¹, closes the gap and returns the last entry.
- An entry is free while its dword `+0x00` is 0², and the request
  kind is bits `0x6` of its byte `+0x13`³. When all 36 are taken
  and every one has request kind 1 or 2, `0x003B0980` ends nothing and answers 0
 ⁴.
- `0x003AFFB0(n)`, from `0x002FCCC0`, ends requests from the front of the table until `n` are left,
  sparing request kinds 1 and 2. `0x003B0B70` returns half the number of entries in use.
- `0x003B0BF0(handle)` returns the entry, `0x003B0940(handle)` its effect number or −1, and
  `0x003B0FD0(handle, v)` stores `v` at `+0x04`. `0x003B0C30(owner, number)` is
  `0x003B02A0(owner, 0, 0, number, 5)`.
- `0x003B0820(v)`, with arena 8 selected, ends the instance⁵ of every entry whose `+0x04`
  equals `v`, closes each gap and clears `0x02EBEF48`. `0x002FCB60(handle)` calls it with its own
  handle first⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024EE60` |
| ² | `0x003B0994`-`0x003B09B5` |
| ³ | `0x003B0A20`-`0x003B0A2D` |
| ⁴ | `0x003B0A2F`-`0x003B0A3A` |
| ⁵ | `0x0024EE60` |
| ⁶ | `0x002FCB79` |

</details>

The last entry, `0x02EBEF48`-`0x02EBEF5F`, is the one a closed gap leaves behind. After moving the later entries up one,
`0x003B0770` and `0x003AFFB0` clear its handle `0x02EBEF48` and its instance `0x02EBEF50`¹, and `0x003B0820`² and `0x003B0220`³ clear its handle. When `0x003B0980` ends an instance to free an
entry, it clears bit `0x1` of the last entry's `+0x13`, `0x02EBEF5B`⁴, and returns that entry⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B07F2`-`0x003B07FC`, `0x003B00D9`-`0x003B00E0` |
| ² | `0x003B089D` |
| ³ | `0x003B028B` |
| ⁴ | `0x003B0A9D` |
| ⁵ | `0x003B0AA4` |

</details>

- `0x003B1260(handle, kind)`, for a kind of 1 to 10, calls `0x0024FE70(instance, kind)` with arena 8
  selected.
- `0x003B1050(targets, n)`, from `0x0024FBF0`, raises bit `0x4` of `+0x368` on every kind-5 instance
  whose request kind is 0, or is 1 or 3 and whose owner `+0x08` equals an id of the list (`+0x11`
  = 0) or the value `0x002E9B80` returns for one (`+0x11` = 1).
- `0x002FD090()`, from the same `0x0024FBF0`¹, raises bit `0x4` of `+0x368` on the instance `+0x10` of
  every handle on the kind-1 active list `0x02EC3D60`, without a test.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024FC58` |

</details>

### Script effect slots

Event scripts reach the loaded-file queue through 32 slots of `0x18` bytes at `0x022D94B0`: the
queue id `+0x00`, a state word `+0x04` (0 free, 1 reading, 2 read, 3 playing, 4 cancelled), the
reading manager `+0x08` and the signal bytes `+0x10` ([native commands](../Scripts-And-Script-Commands/native-commands.md)).
Every slot number is clamped to 0 to 31, `slot < 0 ? 0 : slot > 31 ? 31 : slot`, at the start of each slot
function (`0x0036E32C`-`0x0036E33D` in `0x0036E320`; `0x0036E540`, `0x0036E5A0`, `0x0036E5E0`, `0x0036E8B0`, `0x0036DDC0`,
`0x0036DF80`, `0x0036E460`).

- Read: `effectread(id)` (`0x00DB`), `locationeffectread(id)` (`0x0127`) and `questeffectread(id)`
  (`0x01DA`) push slot 0 and the kind 0, 1 or 2; their two-argument forms (`0x00E0`, `0x0128`,
  `0x01DB`) take the slot first. The shared body `0x003576D0` calls `0x0036E320` unless the issuer's
  manager is skipping¹, and then `0x00314D40(1)`.
- `0x0036E320(manager, slot, id, kind)` acts only on a free slot: it clears the signal bytes, adds
  `0x1000` to the id for kind 1 or `0x2000` for kind 2, files it with `0x003B1A80(id, slot)`, which puts
  the slot in mask `0xFC0` of the queue id, keeps the manager, and sets state 1 when it got an id.
- `effectreadsync` (`0x00DC`, slot 0) and `effectreadsync_e1(slot)` (`0x00E1`) poll `0x0036E540`: a
  reading slot waits until `0x0024DE70(id)` reports 2 or 3, then becomes state 2.
- Play: `effectplay(n)` (`0x00DD`, slot 0) and `effectplay_e2(slot, n)` (`0x00E2`) call
  `0x0036E8B0(slot, n)`. A slot in state 2 or 3 whose file reports 2 or 3 becomes state 3 and is
  played by `0x003B1BA0` with the owner `[0x02EBCC70]`, the target list `0x02EBCBE0` (count
  `[0x02EBCC60]`) and `n`. Then `0x0024F8D0` sets mask `0x7000` of the instance's `+0x36A` to 3 for a
  slot read by manager 3 and to 0 otherwise, which picks the target table above.
- `effectsync` (`0x00DE`, slot 0) and `effectsync_e3(slot)` (`0x00E3`) wait while the state word
 ² is non-zero; a skip cancels the slot instead.
- Cancel: `effectcancel` (`0x00DF`, slot 0) and `effectcancel_e4(slot)` (`0x00E4`) run `0x0036DDC0`,
  which sets state 4 on a slot in any state but 0 and 4 and, unless the queue entry's flag bit `0x1` is
  set³, releases the entry⁴. `effectcancelall` (`0x00E5`,
  handler `0x00350FA0` `jmp 0x0036DE20`) runs `0x003B1710` over the queue and sets every slot to state 4.
- Triggers: `effecttriggersync` (`0x0274`, `0x0275`) waits while `0x0036E5E0(slot, n)` holds: for a
  playing slot, `0x0024FDA0` makes the instance current⁵ and hands `0x003333F0` the first qword
  of its `+0x130` block, a timeline player⁶.
- `0x003333F0` asks whether one of that player's 16 track pointers, at player + 8 x k for k from 0 to 15,
  has byte `+0x11` equal to `n`⁷, or else `0x003A8FC0(n)`⁸. The
  player and its tracks are in [Effect element runtime](effect-element-runtime.md).
- `effecttriggercancel` (`0x01DC`, slot 0) and `effecttriggercancel_1dd(slot, n)` (`0x01DD`) run
  `0x0036DF80`, which passes a non-free slot's id to `0x003B27A0`.
- `effectsignal(slot, v)` (`0x0241`, `0x0036E460`) passes `v` to `0x0024F3C0`, which, for `v` = 1,
  adds 1 to the bits under mask `0xF0` of the instance's word `+0x378`.
- `0x0024F3C0` reads `v` through the pointer in its second argument and finds the instance
  with `0x003B2470`; any other `v`, or no instance, changes nothing, and the four bits
  wrap from 15 to 0 without touching the rest of the word⁹.
- `effecthitsyncbyid` (`0x0440`) waits while `0x0036E640(id)` holds: the file reports 2 or 3 and bit `0x20`
  of the instance's `+0x36A` is clear (`0x0024E210(id, 0)`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00267310` |
| ² | `0x0036E5A0` |
| ³ | `0x003B24C0` |
| ⁴ | `0x003B18E0` |
| ⁵ | `0x0024ED80` |
| ⁶ | `0x0024FDF6`, `0x0024FE25` |
| ⁷ | `0x00333400`-`0x00333415` |
| ⁸ | `0x0033341A` |
| ⁹ | `0x0024F3C4`-`0x0024F3FD` |

</details>

## Related

- [Effect element runtime](effect-element-runtime.md): instances, emitters, the update and timeline tracks.
- [Effect drawing](effect-drawing.md): the display layers and the draw list.
- [Effect anchors and targets](effect-anchors-and-targets.md): anchor queries and target slots.
- [Effect file loading](effect-file-loading.md): battle effect slots and the loaded-file queue.
- [Native commands](../Scripts-And-Script-Commands/native-commands.md): the effect verbs of event scripts.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 159 calls with 28 other topics</summary>

**Characters and objects** (explained on [frame update order](../Engine-Core/frame-update-order.md), [field runtime](../Characters-And-Objects/field-runtime.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md), [actor record](../Characters-And-Objects/actor-record.md), [target selection](../Battle-Actions/target-selection.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002E9B80`](effect-anchors-and-targets.md) (on effect anchors and targets) | calls | [`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens) |
| [`0x002E9FE0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) | is called by | [`0x0025B820`](../Characters-And-Objects/field-runtime.md) (on field runtime)<br>[`0x0025C230`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0025C830`](../Menus-And-HUD/text-npc-names.md) (on text npc names)<br>[`0x003DF6F0`](../Characters-And-Objects/actor-record.md) (on actor record)<br>[`0x0046BAC0`](../Battle-Actions/target-selection.md) (on target selection) |

**Sound and music** (explained on [animation sounds](../Sound-And-Music/animation-sounds.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002E9B80`](effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x00332C40`](../Sound-And-Music/spatial-sound.md) (on spatial sound) |

**Battle actions** (explained on [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002FCB60`](effects-on-actors-and-scripts.md) | calls | [`0x002FC3C0`](effect-element-runtime.md) (on effect element runtime) |

**Engine core** (explained on [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003B1BA0`](effect-file-loading.md) (on effect file loading) | calls | [`0x00229E40`](../Story-Events-And-Hunts/script-language-differences.md) (on script language differences) |

**Controls and input** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00267310`](effect-file-list.md) (on effect file list) | is called by | [`0x002E09A0`](../Menus-And-HUD/menus.md) (on menus) |

**Movement and pathfinding** (explained on [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00267310`](effect-file-list.md) (on effect file list) | is called by | [`0x002E45E0`](../Movement-And-Pathfinding/facing-and-steering.md) Movement: update steering toward target (on facing and steering)<br>[`0x002E5750`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering) |
| [`0x002E9FE0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) | is called by | [`0x002E6330`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x002EA7F0`](../Party/party-leader.md) (on party leader) |

**Party** (explained on [map screens](../Menus-And-HUD/map-screens.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002E9FE0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) | is called by | [`0x00359150`](effect-anchors-and-targets.md) Party focus: try get current actor world position (on effect anchors and targets) |

**Game files and data tables** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [debug menu](../Engine-Core/debug-menu.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003B1710`](effect-file-loading.md) (on effect file loading) | calls | [`0x0032E4D0`](effect-file-loading.md) (on effect file loading)<br>[`0x0032E520`](effect-file-loading.md) (on effect file loading)<br>[`0x0032E590`](effect-file-loading.md) (on effect file loading) |
| [`0x003B18E0`](effect-file-loading.md) (on effect file loading) | calls | [`0x0032E4D0`](effect-file-loading.md) (on effect file loading)<br>[`0x0032E520`](effect-file-loading.md) (on effect file loading)<br>[`0x0032E590`](effect-file-loading.md) (on effect file loading) |

**Scripts and script commands** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [music table](../Sound-And-Music/music-table.md), [actor managers](../Characters-And-Objects/actor-managers.md), [effect files efx efb](effect-files-efx-efb.md), [music](../Sound-And-Music/music.md), [script screen effects](script-screen-effects.md), [scripted camera](scripted-camera.md), [map sounds](../Sound-And-Music/map-sounds.md), [pkfl packages](../Game-Files-And-Data-Tables/pkfl-packages.md), [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md), [small bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md), [vibration](../Controls-And-Input/vibration.md), [character se tables chse](../Game-Files-And-Data-Tables/character-se-tables-chse.md), [native commands](../Scripts-And-Script-Commands/native-commands.md), [voices](../Sound-And-Music/voices.md), [graphics settings](../Engine-Core/graphics-settings.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [sound effects](../Sound-And-Music/sound-effects.md), [effect file list](effect-file-list.md), [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [action phases](../Battle-Actions/action-phases.md), [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party control modes](../Engine-Core/party-control-modes.md), [verb table](../Scripts-And-Script-Commands/verb-table.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md), [ebp script container](../EBP-Script-Files/ebp-script-container.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [debug menu](../Engine-Core/debug-menu.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00267310`](effect-file-list.md) (on effect file list) | is called by | [`0x0033F330`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x00340260`](../Sound-And-Music/music-table.md) (on music table)<br>[`0x00340FA0`](effect-file-list.md) (on effect file list)<br>[`0x00341590`](effect-file-list.md) (on effect file list)<br>[`0x00341710`](effect-file-list.md) (on effect file list)<br>[`0x00341F50`](effect-file-list.md) (on effect file list)<br>[`0x00342770`](../Characters-And-Objects/actor-managers.md) (on actor managers)<br>[`0x003428C0`](effect-file-list.md) (on effect file list)<br>[`0x00342F80`](../Sound-And-Music/music.md) (on music)<br>[`0x003435C0`](effect-file-list.md) (on effect file list)<br>[`0x003436B0`](effect-file-list.md) (on effect file list)<br>[`0x00343A30`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings) |
| [`0x00267310`](effect-file-list.md) (on effect file list) | is also called by | [`0x00343B00`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x00343C60`](../Characters-And-Objects/actor-managers.md) (on actor managers)<br>[`0x00343F10`](effect-file-list.md) (on effect file list)<br>[`0x00344340`](effect-file-list.md) (on effect file list)<br>[`0x003445E0`](effect-file-list.md) (on effect file list)<br>[`0x00344660`](effect-file-list.md) (on effect file list)<br>[`0x00344F00`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x00345010`](../Sound-And-Music/music.md) (on music)<br>[`0x00345930`](effect-file-list.md) (on effect file list)<br>[`0x00345B60`](../Sound-And-Music/music-table.md) (on music table)<br>[`0x00346260`](../Sound-And-Music/map-sounds.md) (on map sounds)<br>[`0x00346C00`](../Sound-And-Music/music-table.md) (on music table) |
| [`0x00267310`](effect-file-list.md) (on effect file list) | is also called by | [`0x00347B00`](../Game-Files-And-Data-Tables/pkfl-packages.md) (on pkfl packages)<br>[`0x003486A0`](effect-file-list.md) (on effect file list)<br>[`0x0034A1D0`](effect-file-list.md) (on effect file list)<br>[`0x0034A530`](effect-file-list.md) (on effect file list)<br>[`0x0034A600`](effect-file-list.md) (on effect file list)<br>[`0x0034AB50`](../Game-Files-And-Data-Tables/pkfl-packages.md) (on pkfl packages)<br>[`0x0034AC30`](../Controls-And-Input/vibration.md) (on vibration)<br>[`0x0034B3C0`](../Controls-And-Input/vibration.md) (on vibration)<br>[`0x0034B7C0`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) (on character se tables chse)<br>[`0x0034BBD0`](effect-file-list.md) (on effect file list)<br>[`0x0034C210`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) (on character se tables chse)<br>[`0x0034C570`](../Scripts-And-Script-Commands/native-commands.md) (on native commands) |
| [`0x00267310`](effect-file-list.md) (on effect file list) | is also called by | [`0x0034CA40`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) (on character se tables chse)<br>[`0x0034DCC0`](../Scripts-And-Script-Commands/native-commands.md) (on native commands)<br>[`0x0034E630`](effect-file-list.md) (on effect file list)<br>[`0x0034E8B0`](effect-file-list.md) (on effect file list)<br>[`0x0034EE40`](effect-file-list.md) (on effect file list)<br>[`0x0034EF60`](effects-on-actors-and-scripts.md)<br>[`0x00350700`](effect-file-list.md) (on effect file list)<br>[`0x00350EC0`](effect-file-list.md) (on effect file list)<br>[`0x00353260`](../Engine-Core/graphics-settings.md) (on graphics settings)<br>[`0x00353D90`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x00354300`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x00354800`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) |
| [`0x00267310`](effect-file-list.md) (on effect file list) | is also called by | [`0x003549D0`](../Sound-And-Music/music.md) (on music)<br>[`0x00355160`](effect-file-list.md) (on effect file list)<br>[`0x00355300`](effect-file-list.md) (on effect file list)<br>[`0x003563D0`](effect-file-list.md) (on effect file list)<br>[`0x00356990`](effect-file-list.md) (on effect file list)<br>[`0x00357040`](../Sound-And-Music/sound-banks.md) (on sound banks)<br>[`0x003576D0`](effect-file-list.md) (on effect file list)<br>[`0x003581B0`](../Sound-And-Music/voices.md) (on voices) |
| [`0x00314D40`](effect-file-list.md) (on effect file list) | is called by | [`0x0033F330`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x003409F0`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x00340FA0`](effect-file-list.md) (on effect file list)<br>[`0x00341710`](effect-file-list.md) (on effect file list)<br>[`0x00341840`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x003418B0`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x00341F90`](../Sound-And-Music/music-table.md) (on music table)<br>[`0x00342770`](../Characters-And-Objects/actor-managers.md) (on actor managers)<br>[`0x00342F50`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x00344200`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x00344660`](effect-file-list.md) (on effect file list)<br>[`0x00345250`](effect-file-list.md) (on effect file list) |
| [`0x00314D40`](effect-file-list.md) (on effect file list) | is also called by | [`0x003453D0`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x00346020`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x003466A0`](effect-file-list.md) (on effect file list)<br>[`0x00346AA0`](effect-file-list.md) (on effect file list)<br>[`0x003473A0`](../Game-Files-And-Data-Tables/ard-area-battle-data.md) (on ard area battle data)<br>[`0x00347660`](effect-file-list.md) (on effect file list)<br>[`0x00347C60`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x00348870`](../Battle-Actions/action-phases.md) (on action phases)<br>[`0x003491B0`](effect-file-list.md) (on effect file list)<br>[`0x003492A0`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal)<br>[`0x003499C0`](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) (on resource ownership and disposal)<br>[`0x00349A30`](effect-file-list.md) (on effect file list) |
| [`0x00314D40`](effect-file-list.md) (on effect file list) | is also called by | [`0x0034A300`](../Scripts-And-Script-Commands/reward-verbs.md) (on reward verbs)<br>[`0x0034B120`](effect-file-list.md) (on effect file list)<br>[`0x0034B8D0`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x0034C320`](effect-file-list.md) (on effect file list)<br>[`0x0034CED0`](effect-file-list.md) (on effect file list)<br>[`0x0034D740`](effects-on-actors-and-scripts.md)<br>[`0x0034D8B0`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x0034E1F0`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x0034E3E0`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x0034E8B0`](effect-file-list.md) (on effect file list)<br>[`0x0034EE40`](effect-file-list.md) (on effect file list)<br>[`0x0034F770`](effect-file-list.md) (on effect file list) |
| [`0x00314D40`](effect-file-list.md) (on effect file list) | is also called by | [`0x0034FB20`](effect-file-list.md) (on effect file list)<br>[`0x0034FE80`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x003523B0`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x00352E40`](effect-file-list.md) (on effect file list)<br>[`0x00353080`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x00353590`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x00353720`](effect-file-list.md) (on effect file list)<br>[`0x003541B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x00354690`](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md) (on file requests and the read queue)<br>[`0x00354920`](effect-file-list.md) (on effect file list)<br>[`0x00354A40`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x003550F0`](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md) (on file requests and the read queue) |
| [`0x00314D40`](effect-file-list.md) (on effect file list) | is also called by | [`0x00356050`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x00357300`](../Controls-And-Input/action-availability.md) (on action availability)<br>[`0x003576D0`](effect-file-list.md) (on effect file list)<br>[`0x0050CB00`](effect-file-list.md) (on effect file list)<br>[`0x0050D0C0`](../Engine-Core/debug-menu.md) (on debug menu)<br>[`0x0050D540`](effect-file-list.md) (on effect file list)<br>[`0x0050D710`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x0050E1E0`](effect-file-list.md) (on effect file list)<br>[`0x0050EA80`](effect-file-list.md) (on effect file list) |
| [`0x003576D0`](effect-file-list.md) (on effect file list) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003576D0`](effect-file-list.md) (on effect file list) | is called by | [`0x0034B880`](effect-file-list.md) (on effect file list)<br>[`0x0034BC90`](effect-file-list.md) (on effect file list)<br>[`0x0034C0F0`](effect-file-list.md) (on effect file list)<br>[`0x0034C430`](effect-file-list.md) (on effect file list)<br>[`0x0034C820`](effect-file-list.md) (on effect file list)<br>[`0x0034CB80`](effect-file-list.md) (on effect file list) |
| [`0x0036DDC0`](effects-on-actors-and-scripts.md) | is called by | [`0x0034EF60`](effects-on-actors-and-scripts.md)<br>[`0x0034FD80`](effects-on-actors-and-scripts.md)<br>[`0x003501D0`](effects-on-actors-and-scripts.md) |
| [`0x0036DF80`](effects-on-actors-and-scripts.md) | is called by | [`0x003504D0`](effects-on-actors-and-scripts.md)<br>[`0x00350990`](effects-on-actors-and-scripts.md) |
| [`0x0036E320`](effect-file-list.md) (on effect file list) | is called by | [`0x003576D0`](effect-file-list.md) (on effect file list) |
| [`0x0036E460`](effects-on-actors-and-scripts.md) | is called by | [`0x0034D690`](effects-on-actors-and-scripts.md) |
| [`0x0036E540`](effects-on-actors-and-scripts.md) | is called by | [`0x0034D740`](effects-on-actors-and-scripts.md) |
| [`0x0036E5A0`](effects-on-actors-and-scripts.md) | is called by | [`0x0034EF60`](effects-on-actors-and-scripts.md) |
| [`0x0036E5E0`](effects-on-actors-and-scripts.md) | is called by | [`0x00355F40`](effects-on-actors-and-scripts.md) |
| [`0x0036E640`](effects-on-actors-and-scripts.md) | is called by | [`0x00351FD0`](effects-on-actors-and-scripts.md) |
| [`0x0036E8B0`](effects-on-actors-and-scripts.md) | is called by | [`0x0034DE50`](effects-on-actors-and-scripts.md)<br>[`0x0034E2A0`](effects-on-actors-and-scripts.md) |

**Menus and HUD** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0024ED80`](effect-drawing.md) (on effect drawing) | is called by | [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) |
| [`0x0024EE60`](character-effects.md) (on character effects) | is called by | [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) |
| [`0x003B0220`](effects-on-actors-and-scripts.md) | is called by | [`0x0024B9B0`](effect-element-runtime.md) (on effect element runtime) |

**World, areas and travel** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [debug logging](../Engine-Core/debug-logging.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00314D40`](effect-file-list.md) (on effect file list) | is called by | [`0x00266D10`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x00267310`](effect-file-list.md) (on effect file list) | is called by | [`0x00314020`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |

</details>
