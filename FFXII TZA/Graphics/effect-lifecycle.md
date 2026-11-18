[Home](../../README.md) / [Graphics](README.md) / Effect lifecycle

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Effect lifecycle: from the request that names an effect to its release, and what an area change ends | lifecycle | Graphics | Visual effects / Effect Files | The stages an effect passes through: the request that names it, the file load, the instance, its start, the per-step update and per-frame draw, the hold a time stop puts on it, the restart of a looping instance, its end, and the release of its elements, its file and its handle, with what an area change and a return to the title end; each stage linked to the page that explains it. | 0x003B02A0, 0x0024B270, 0x0024B9B0, 0x003A74F0, 0x003A7050, 0x003A7300, 0x0024C550, 0x0024E910, 0x002628B0, 0x003601D0 |

## What the player sees

A spell or ability effect appears when it is asked for, plays out over its frames, can loop, freezes while time is
stopped, and disappears when it ends or when the party leaves the area.

## Stages

1. **Request.** An ability or event names a numbered effect for an owner and its targets (`0x003B02A0`), or an event
   script reads one into a script effect slot ([effects on actors and scripts](effects-on-actors-and-scripts.md)).
2. **Loading.** A battle effect is read into one of the 48 battle effect slots, and other effects into the queue of
   loaded files, where a file can be shared ([effect file loading](effect-file-loading.md)).
3. **Instance.** `0x0024B270` makes the `0x3B0`-byte effect instance in its kind's list, with an empty emitter list
   (`0x003A8900`). Its emitters and their elements come later, through `0x003A8AE0`, from the events of its timeline
   tracks and the spawn slots of its elements
   ([effect element runtime](effect-element-runtime.md#instances-emitters-and-elements)).
4. **Start.** In state 2 or 8 the step starts the instance (`0x003A74F0`) and moves it to state 1
   ([effect element runtime](effect-element-runtime.md#starting-and-ending-an-instance)). `0x003A74F0` also runs from
   state 4 (step 8) and from the signal `0x0024FE70` (`0x0024FEC7`).
5. **Update.** Each simulation step updates the instance: the emitter step, births, the base update, the cull, and
   child emitters ([effect element runtime](effect-element-runtime.md#the-update-pass)).
6. **Draw.** Each frame draws the instance in its display layer's pass
   ([effect drawing](effect-drawing.md#the-six-display-layers)).
7. **Hold.** While a time stop holds the instance's owner, bit `0x2` of `+0x368` limits each step to two calls, and
   the instance stands still ([effect element runtime](effect-element-runtime.md#the-effect-teardown),
   [time stop and freeze](../Engine-Core/time-stop-and-freeze.md)).
8. **Restart.** An instance in state 4 starts again (`0x003A74F0`, `0x0024BDB3`) and goes to state 5 (`0x0024BDB8`). One in
   state 6 runs its update (`0x0024BE11`–`0x0024BE28`) and also goes to state 5: when the update returns 0 it is ended
   first (`0x003A7300`, `0x0024BE31`), and the 4 stored at `0x0024BE36` is overwritten by the 5 at `0x0024BE3D` ([effect
   element runtime](effect-element-runtime.md#starting-and-ending-an-instance)).
   - State 5 puts the instance back in state 1 and lowers the count in bits `0xF0` of `+0x378`, 0 wrapping to `0xF`;
     it stays in state 5 while `0x001EDDA0` answers non-zero and the count is 0 (`0x0024BDBD`–`0x0024BE08`).
9. **End.** In state 1, an update that returns 0 ends the instance (`0x003A7300`, `0x0024BC23`): `0x003A7300` frees its
   players (`0x003A7360`) and hands each non-zero handle at `+0x110`–`+0x11C` to `0x002FCB60` through the one-jump
   `0x002FC340`, clearing it (`0x003A730A`–`0x003A733A`)
   ([effect element runtime](effect-element-runtime.md#starting-and-ending-an-instance)).
   - With bit `0x1` of `+0x368` clear the instance then goes to state 8 and starts again on its next step (`0x0024BC32`,
     `0x0024BCBF`–`0x0024BCD6`).
   - With the bit set, a kind-3 instance goes to state 7 and a kind other than 2, 3 and 7 to state 3
     (`0x0024BC41`–`0x0024BC59`). A kind-2 or kind-7 instance goes to state 3 when the high nibble of `+0x16` of its
     `0x600` record `+0x373` is 0 or equals the low nibble of `+0x378`, else to state 7 (`0x0024BC6A`–`0x0024BCB4`).
10. **Release.** A released element goes back on its emitter's free list `+0x120`
    ([effect element runtime](effect-element-runtime.md#the-cull-the-release-and-the-spawn-slots)). An instance its
    owner lets go is queued on the instance free list `0x02092170` and freed on a later frame
    ([effect element runtime](effect-element-runtime.md#the-free-list)).
11. **Group and file release.** `0x0024C550` frees a group's contexts and instances, after clearing the owner table of
    kinds 1 and 5 to 9 (`0x0024C569`–`0x0024C594`), and a loaded file is released
    unless it is kept ([effect element runtime](effect-element-runtime.md#emptying-a-group),
    [effect file loading](effect-file-loading.md#filing-sharing-and-releasing-a-loaded-file)).
12. **Reuse.** A slot that is used again gets a new id, so a handle kept from before names nothing
    ([resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md),
    [identifier spaces](../Engine-Core/identifier-spaces.md)).

## Across transitions

- **An area change or a return to the title.** The area unload `0x002628B0` and the title-return reset `0x003601D0` run
  the effect teardown `0x0024E910`: every battle effect, model effect and numbered request ends, the map effect bank is
  disposed, and every loaded file that is not kept is released
  ([effect element runtime](effect-element-runtime.md#the-effect-teardown),
  [changing areas](../World-Areas-And-Travel/changing-areas.md)).
- **The rest of the teardown.** `0x0024E910` also sets the group mask `0x02092160` to `0x3FF`, releases the time-stop hold
  of the model effects and the numbered requests (`0x003B3B50`, `0x003B1130`), and ends in the motion blur and cut-in
  clears (`0x0024E96B`–`0x0024EA0B`; [effect element runtime](effect-element-runtime.md#the-effect-teardown)).
- **A loaded file kept by its flag** (`+0x20` bit `0x1`) survives the teardown
  ([effect file loading](effect-file-loading.md#filing-sharing-and-releasing-a-loaded-file)).
- **A time stop's end** releases every held instance, so all of them move again at once
  ([effect element runtime](effect-element-runtime.md#the-effect-teardown)).

## Related

- [Effect element runtime](effect-element-runtime.md): the instance, its emitters and elements.
- [Effect element types](effect-element-types.md): what each element type does in its methods.
- [Effect files](effect-files-efx-efb.md): the files an effect is read from.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 56 calls with 18 other topics</summary>

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x0024E910` | is called by | `0x002628B0` |
| `0x002628B0` | calls | `0x0025B070`, `0x00263660`, `0x002695A0`, `0x0037B230`, `0x003B6C20`, `0x003DDC20`, `0x003DE920` |
| `0x002628B0` | is called by | `0x0025BFB0`, `0x0032FCA0` |
| `0x003601D0` | calls | `0x00263FF0` |

**Characters and objects** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md), [frame update order](../Engine-Core/frame-update-order.md), [startup constants](../Engine-Core/startup-constants.md))

**Characters and objects** (explained on [event scenes](../Scripts-And-Script-Commands/event-scenes.md), [actor record](../Characters-And-Objects/actor-record.md), [actor managers](../Characters-And-Objects/actor-managers.md), [debug menu](../Engine-Core/debug-menu.md))

**Sound and music**

| Function | | Functions |
|---|---|---|
| `0x001EDDA0` | is called by | `0x003B99D0` |
| `0x002628B0` | calls | `0x00360B50`, `0x00360DD0`, `0x003636A0` |
| `0x003601D0` | calls | `0x002DF060`, `0x002DF0F0`, `0x002DF370`, `0x00360D70`, `0x00362850`, `0x003633B0`, `0x003636A0`, `0x00363750`, `0x00363E40` |

**Sound and music** (explained on [effect anchors and targets](effect-anchors-and-targets.md), [music](../Sound-And-Music/music.md), [game over](../World-Areas-And-Travel/game-over.md), [force fight mode](../Engine-Core/force-fight-mode.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md))

**Sound and music** (explained on [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [frame update order](../Engine-Core/frame-update-order.md))

**Battle actions** (explained on [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md))

| Function | | Functions |
|---|---|---|
| `0x002FCB60` | calls | `0x002FC3C0` |

**Engine core**

| Function | | Functions |
|---|---|---|
| `0x001EDDA0` | is called by | `0x00265860`, `0x00265880` |
| `0x0024B9B0` | calls | `0x001EDDA0` |
| `0x002628B0` | calls | `0x00229EE0` |
| `0x003601D0` | calls | `0x00229EE0`, `0x00229EF0` |
| `0x003A8AE0` | calls | `0x001EDDA0` |

**Engine core** (explained on [script screen effects](script-screen-effects.md), [native commands](../Scripts-And-Script-Commands/native-commands.md), [global state accessors](../Engine-Core/global-state-accessors.md), [game over](../World-Areas-And-Travel/game-over.md))

**Controls and input** (explained on [vibration](../Controls-And-Input/vibration.md))

| Function | | Functions |
|---|---|---|
| `0x002628B0` | calls | `0x0035B5D0` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x001EDDA0` | is called by | `0x0025DF00` |
| `0x002628B0` | calls | `0x00263560`, `0x0026A1D0`, `0x00379070`, `0x003791C0`, `0x003792D0`, `0x003DAA20` |
| `0x003A7360` | calls | `0x0024C6B0`, `0x0024C870` |

**Movement and pathfinding** (explained on [frame update order](../Engine-Core/frame-update-order.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md), [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md))

**Party** (explained on [player movement](../Movement-And-Pathfinding/player-movement.md), [actor managers](../Characters-And-Objects/actor-managers.md))

| Function | | Functions |
|---|---|---|
| `0x002628B0` | calls | `0x00358B40`, `0x00359200` |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md))

| Function | | Functions |
|---|---|---|
| `0x002628B0` | calls | `0x0032E520` |
| `0x003601D0` | calls | `0x0032E520` |

**Saving, loading and settings** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [game over](../World-Areas-And-Travel/game-over.md))

| Function | | Functions |
|---|---|---|
| `0x002628B0` | calls | `0x002EF2B0` |
| `0x003601D0` | calls | `0x002EF5F0` |

**Menus and HUD** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x001EDDA0` | is called by | `0x0024B9B0` |
| `0x003A7050` | is called by | `0x0024B9B0` |
| `0x003A7300` | is called by | `0x0024B9B0` |
| `0x003A74F0` | is called by | `0x0024B9B0` |

**World, areas and travel**

| Function | | Functions |
|---|---|---|
| `0x002628B0` | calls | `0x00378230`, `0x003DFA50`, `0x003EAA00` |
| `0x003601D0` | calls | `0x00331920` |

**World, areas and travel** (explained on [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md), [ebp navigation icons](../EBP-Script-Files/ebp-navigation-icons.md), [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md), [game over](../World-Areas-And-Travel/game-over.md))

</details>
