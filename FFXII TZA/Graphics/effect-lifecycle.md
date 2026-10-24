---
title: "Effect lifecycle: from the request that names an effect to its release, and what an area change ends"
kind: "lifecycle"
category: "Graphics"
addresses: "0x003B02A0, 0x0024B270, 0x0024B9B0, 0x003A74F0, 0x003A7050, 0x003A7300, 0x0024C550, 0x0024E910, 0x002628B0, 0x003601D0"
---

## What the player sees

A spell or ability effect appears when it is asked for, plays out over its frames, can loop, freezes while time is
stopped, and disappears when it ends or when the party leaves the area.

## Stages

1. **Request.** An ability or event names a numbered effect for an owner and its targets (`0x003B02A0`), or an event
   script reads one into a script effect slot ([effects on actors and scripts](effects-on-actors-and-scripts.md)).
2. **Loading.** A battle effect is read into one of the 48 battle effect slots, and other effects into the queue of
   loaded files, where a file can be shared ([effect file loading](effect-file-loading.md)).
3. **Instance.** `0x0024B270` makes the `0x3B0`-byte effect instance in its kind's list, with its emitters and their
   elements ([effect element runtime](effect-element-runtime.md#instances-emitters-and-elements)).
4. **Start.** In state 2 or 8 the step starts the instance (`0x003A74F0`) and moves it to state 1
   ([effect element runtime](effect-element-runtime.md#starting-and-ending-an-instance)).
5. **Update.** Each simulation step updates the instance: the emitter step, births, the base update, the cull, and
   child emitters ([effect element runtime](effect-element-runtime.md#the-update-pass)).
6. **Draw.** Each frame draws the instance in its display layer's pass
   ([effect drawing](effect-drawing.md#the-six-display-layers)).
7. **Hold.** While a time stop holds the instance's owner, bit `0x2` of `+0x368` limits each step to two calls, and
   the instance stands still ([effect element runtime](effect-element-runtime.md#the-effect-teardown),
   [time stop and freeze](../Engine-Core/time-stop-and-freeze.md)).
8. **Restart.** An instance in state 6 moves to 4 when its update ends and starts again
   ([effect element runtime](effect-element-runtime.md#starting-and-ending-an-instance)).
9. **End.** In state 1, an update that returns 0 ends the instance (`0x003A7300`)
   ([effect element runtime](effect-element-runtime.md#starting-and-ending-an-instance)).
10. **Release.** A released element goes back on its emitter's free list `+0x120`
    ([effect element runtime](effect-element-runtime.md#the-cull-the-release-and-the-spawn-slots)). An instance its
    owner lets go is queued on the instance free list `0x02092170` and freed on a later frame
    ([effect element runtime](effect-element-runtime.md#the-free-list)).
11. **Group and file release.** `0x0024C550` frees a group's contexts and instances, and a loaded file is released
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
- **A loaded file kept by its flag** (`+0x20` bit `0x1`) survives the teardown
  ([effect file loading](effect-file-loading.md#filing-sharing-and-releasing-a-loaded-file)).
- **A time stop's end** releases every held instance, so all of them move again at once
  ([effect element runtime](effect-element-runtime.md#the-effect-teardown)).

## Related

- [Effect element runtime](effect-element-runtime.md): the instance, its emitters and elements.
- [Effect element types](effect-element-types.md): what each element type does in its methods.
- [Effect files](effect-files-efx-efb.md): the files an effect is read from.
