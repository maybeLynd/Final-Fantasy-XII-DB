---
title: "Pause screen: the overlay shown while the game window is in the background, the inactive-window hold that brings it up, and what is paused while it is open"
kind: "system"
category: "Menus and HUD"
addresses: "0x00228380, 0x00228490, 0x002284F0, 0x002282F0, 0x00229590, 0x0017E720, 0x00183200, 0x00182FF0, 0x00181E10, 0x00180120, 0x001EC5A0, 0x0017E500"
---

## What the player sees

- When the game window goes to the background a pause picture fades in over the screen, the sound pauses and the
  field ignores the buttons.
- Pressing the cancel button closes the pause screen and the game goes on.
- The pause screen does not appear before the title screen has been shown.

## How it works

### The opener

The field's input arbiter calls `0x00228380` before it reads a button and reads nothing while it answers non-zero
([Controls](../Controls-And-Input/controls.md), `0x00253CC3`). Each call (`0x00228380`-`0x0022843A`):

1. When the window is not in front (`0x0017E4C0` answers 0) and no inactive-window task exists, it starts one
   (`0x00228490`).
2. It answers 0 while `0x003603C0` or `0x001D6B70` answers non-zero, or while `0x01FD4950` is 0. `0x01FD4950` is set once,
   by `0x00229AD0`, which the title asset's factory `0x00394460` runs ([Widgets](widgets.md)).
3. With action policy bit `0x200000` set (`0x002E0FA0`) it goes on only when `0x002E1020(1)` also has bit `0x200000`, and then passes argument 0
   to the overlay of step 5 ([Action availability](../Controls-And-Input/action-availability.md)).
4. With an overlay open it answers 1. With the count `0x01FD46FC` above 0 it counts it down and answers 1.
5. Otherwise, while the inactive-window task exists, it builds the overlay through `0x002282F0(argument)`; with no task
   it answers 0.

`0x002282F0` builds the `0xD0`-byte overlay `0x00229590` into `0x01FD4940` when that is empty (`0x00228303`-`0x00228352`).
`0x01FD46FC` is set to 5 when an overlay is destroyed, so a new one cannot open for five calls.

### The inactive-window task

`0x00228490` builds the `0xD0`-byte task `0x002284F0` into `0x01FD4948` ([Action availability](../Controls-And-Input/action-availability.md)).
`0x00228480` answers whether it exists.

| Message | What the task does |
|---|---|
| `1`, built | runs `0x00196710` on the input manager (`0x001E0980`), runs the drain over the root `0x0208EA40` (`0x00248030`), takes the focus unless `[0x0209AC30] + 0x308` is set, attaches under `0x0208EA48`, and while a movie plays clears the active bit of message window 3 (`0x002E2570(3, 0)`) |
| `10`, its input turn | sets `0x022CBE34` to 5 (`0x00368810`); when channel 0's newest word from `0x0035EF10(0, 0)` equals the cancel mask `0x01E0C2A4`, writes 0 to `0x022CA5F0` (`0x0035ED40`), moves to state 1 and, while a movie plays, sets message window 3 active again |
| `2`, each tick | in state 1: posts window message `0x8002` with 0 (`0x0017E500`), closes the overlay (`0x00244DD0`) and releases itself, state 3; then clears the mouse wheel (`0x001E0F20`), and while `[0x0209AC30] + 0x308` is set treats the cancel word the same way, clearing the input words `0x02F97360`-`0x02F9739B` |
| `18`, destroyed | clears `0x01FD4948` and the wheel; gives the focus to `+0xC8` when set |

`0x001EC5A0` answers whether a movie plays: the movie player's status `+4` is 3 (`0x001B7F20`, `0x001B7D20`,
[Movies](../Graphics/movies.md)). `0x0017E500(on)` sends the message `0x8002` with 1 or 0 to the game
window `0x02EA5248`, the handle the window procedure `0x00798FF0` stores (`0x007990FF`).

### Building the overlay

On message 1 the overlay (`0x00229961`-`0x00229A98`):

1. prints `PauseMenu Create` (`0x0017DB70`) and clears bytes 0, 1 and 2 of the running object (`0x00183200(0)`,
   `0x00182FF0(0)`), below;
2. keeps its argument at `+0xC8`, sets state `+0xC0` to 0, and takes the 1920 x 1080 frame from `0x01E0C1D8` and
   `0x01E0C1DC` as its size;
3. sets bits `0x2`, `0x1`, `0x100000` and `0x200` of action policy row 15 (`0x002E1C20`): bits `0x1`, `0x2` and `0x200` keep the main menu, the battle
   menu and Escape Mode shut, and no reader tests bit `0x100000`;
4. builds button legend scenes `0x12` and `0x0C` (`0x0029DA70`) and formats text `0x467C`, which holds only size and baseline codes,
   with it into `0x01FD4960` (`0x002B4090`);
5. attaches under `0x0208EA48` with priority -9.

With a non-zero argument it then opens screen layer 3, `0x002CCD40({3, descriptor, 100, 0})`, and moves to state 1.
The descriptor is `0x00908B40` when `0x00180120` answers 0, `0x022C7F84` is 0 and world lock 15 is not held
(`0x00226BD0(15)`), and `0x00908B50` otherwise.

`0x002CCCA0(descriptor, value)` and `0x002CCCF0(descriptor, value)` make the same call for layers 1 and 0. The
first serves `0x00241D40`, `0x003939B0`, `0x003F3E40`, `0x005704E0`, `0x00572890`, `0x00573980`, the shop `0x0057A620`,
`0x0057CD40` and the Save and Load screen `0x0057F7D0`; the second serves `0x002C19E0`.

`0x00180120` answers 1 while the event classification byte `0x01F832E9` is set (`0x001EC5C0`, a `spc_` event,
[Debug menu](../Engine-Core/debug-menu.md)) and `0x001EC560` holds: an event slot has queued events and
`0x00265680` answers 0.

### The stages

Each tick (message 2) moves the overlay through its states:

| State | Waits for | Then |
|---:|---|---|
| `0` | `0x01FD4954`, which `0x00229AE0` sets for the movie player (`0x001B7690`, `0x001B7F30`, `0x001B82A0`, `0x001B8400`) and `0x002CEB40` | clears it, opens layer 3 with `0x00908B50`, sets `+0xC8` to 1, state 1 |
| `1` | layer 3's widget reports `+0xE8` (`0x002CCC70(3)`) | pauses, below; state 2 |
| `2` | message 15, the close | state 3 |
| `3` | nothing | resumes, below; closes layer 3 (`0x002CCBC0(3)`), state 4 |
| `4` | layer 3's widget at `[0x0209AC30] + 0x2A8` to be gone | clears the four policy bits (`0x002E1CA0`), turns the framework pause byte off (`0x0017E720(0)`) and releases itself |

On message 4 it draws, once paused with `+0xC8` set, a sprite of the battle atlas (`0x0035D460`) centred on the frame
(`0x002D8CB0`), and in every state the text at `0x01FD4960` (`0x002D8910`).

### What pausing does

At state 1 the overlay prints `PauseMenu Open` and (`0x0022986B`-`0x002298F2`):

- saves the behind-camera switch `0x02098354` at `+0xC4` and clears it (`0x0025A850`, `0x0025A880(0)`); the script verbs
  `tutorial_get_behindcameraenable` (`0x3A0`) and `tutorial_set_behindcameraenable` (`0x3A1`) read and write it;
- pauses the audio kinds `0x3F` (`0x002DF370(0x3F, 1, 1)`, [Audio manager](../Sound-And-Music/audio-manager.md)) unless world
  lock 15 is held or `0x01E027FC` is 0, then sets `0x01E027FC` to 1;
- turns on the framework pause byte at `[0x01F810F0]` (`0x0017E720(1)`, `0x001997E0`;
  [Game application](../Engine-Core/game-application.md));
- unless the frame mode `0x00229EA0` is 5, sets byte 0 (`0x00183200(1)`, `0x0018A820`) and byte 2 (`0x00182FF0(1)`,
  `0x0018A830`) of the three-byte running object `[0x01F7F5D8]` (`0x0018A7D0`), whose byte 0 the frame tick reads to
  choose the pump's mode;
- when the monster viewer's settings byte `+0x118` is set (`0x00181DD0`, `0x001EBA40`), sets its `+0x26E` and the flag
  `0x800000` of the render record of its id `+0x134` (`0x00181E10(1)`, `0x001EBC70`, `0x002EF250`).

State 3 undoes each in turn (`0x002297F9`-`0x00229833`): audio on again unless lock 15 is held, the two bytes cleared
(`0x0018A820` with 0 also clears bytes 1 and 2), the behind-camera switch restored, and the viewer flag cleared unless
its `+0x26D` is set.

## Layouts

### The pause overlay

The overlay is the `0xD0`-byte widget at `0x01FD4940` with procedure `0x00229590` (Building the overlay above).

`PauseOverlay` (`0xD0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x00229590` |
| `+0xC0` | `u32` | state | the overlay's stage, 0-4 (The stages above): the construct message sets 0 (`0x00229985`), or 1 when its argument is non-zero and it opens screen layer 3 at once (`0x00229A9D`); the tick dispatches on it (`0x0022974E`) and moves it to 1 (`0x00229941`), 2 (`0x002298F7`) and 4 (`0x00229843`); message 15, the close, sets 3 (`0x00229605`); state 4 sets 0 as it releases the overlay (`0x002297BF`) |
| `+0xC4` | `u32` | savedBehindCamera | the behind-camera switch `0x02098354` saved when the game pauses (`0x0025A850`, `0x00229881`) and restored when it resumes (`0x0022981D`); 1 at construction (`0x0022998B`) |
| `+0xC8` | `u32` | layerOpen | the construct message's argument (`0x00229979`): non-zero opens screen layer 3 at construction (`0x00229A47`); state 0 sets it to 1 when it opens the layer (`0x0022994B`). The draw message draws the battle-atlas sprite only while it and `+0xCC` are set (`0x00229632`) |
| `+0xCC` | `u32` | paused | 1 while the game is paused: state 1 sets it as it pauses ("PauseMenu Open", `0x00229870`); state 3 undoes the pause only when it is set and clears it (`0x002297E5`, `0x002297F0`); 0 at construction (`0x0022997F`). The draw message draws the sprite only while it is set (`0x00229614`) |

### The inactive-window task

The task is the `0xD0`-byte widget at `0x01FD4948` with procedure `0x002284F0` (The inactive-window task above).

`InactiveWindowTask` (`0xD0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x002284F0` |
| `+0xC0` | `u32` | state | the task's state: 0 at construction (`0x0022864A`); the input turn sets 1 when the cancel word arrives (`0x00228570`); the tick, in state 1, closes the overlay, releases the task and sets 3 (`0x00228599`, `0x002285C2`) |
| `+0xC4` | `u8[4]` | pad0C4 | read and written by no function; nothing fixes its width |
| `+0xC8` | `void*` | pendingFocus | the widget that asked for the focus while the task held it: the focus call `0x002470D0` hands such a request to `0x002286B0` (`0x002470FF`), which sends the widget its message 10 and keeps it here (`0x002286E3`); when the task is destroyed (message 18) it gives the focus to this widget (`0x00228532`); the release `0x002482E0` clears it through `0x00228450` when the widget being released is the one kept (`0x0022845C`, `0x00228465`); 0 at construction (`0x00228643`) |

## Modding notes

- The pause screen is a focus-loss pause only. The overlay is built only while the inactive-window task exists
  (`0x00228435`), and one call in the executable starts the task, `0x002283AE`, taken when the window is not in
  front.
- What stops play is the audio mask, the policy bits and the task holding the input; the framework pause byte
  is set and cleared alongside them.
- `0x01FD46FC` makes the opener answer 1 for five calls after a pause screen closes, which keeps the field input off
  for those frames.

## Related

- [Action availability](../Controls-And-Input/action-availability.md) - row 15 and policy bit `0x200000`.
- [Controls](../Controls-And-Input/controls.md) - the input arbiter that calls the opener.
- [Widgets](widgets.md) - the focus, the roots and the release.
- [Audio manager](../Sound-And-Music/audio-manager.md) - the paused kinds.
- [Game application](../Engine-Core/game-application.md) - the framework pause byte and the running object.
