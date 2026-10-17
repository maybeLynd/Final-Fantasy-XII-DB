---
title: "Pause screen: the overlay shown while the game window is in the background, the inactive-window hold that brings it up, and what is paused while it is open"
kind: "system"
category: "Menus and HUD"
addresses: "00228380, 00228490, 002284F0, 002282F0, 00229590, 0017E720, 00183200, 00182FF0, 00181E10, 00180120, 001EC5A0, 0017E500"
---

## What the player sees

- When the game window goes to the background a pause picture fades in over the screen, the sound pauses and the
  field ignores the buttons.
- Pressing the cancel button closes the pause screen and the game goes on.
- The pause screen does not appear before the title screen has been shown.

## How it works

### The opener

The field's input arbiter calls `00228380` before it reads a button and reads nothing while it answers non-zero
([Controls](../Controls-And-Input/controls.md), `00253CC3`). Each call (`00228380`-`0022843A`):

1. When the window is not in front (`0017E4C0` answers 0) and no inactive-window task exists, it starts one
   (`00228490`).
2. It answers 0 while `003603C0` or `001D6B70` answers non-zero, or while `01FD4950` is 0. `01FD4950` is set once,
   by `00229AD0`, which the title asset's factory `00394460` runs ([Widgets](widgets.md)).
3. With action policy bit 21 set (`002E0FA0`) it goes on only when `002E1020(1)` also has bit 21, and then passes argument 0
   to the overlay of step 5 ([Action availability](../Controls-And-Input/action-availability.md)).
4. With an overlay open it answers 1. With the count `01FD46FC` above 0 it counts it down and answers 1.
5. Otherwise, while the inactive-window task exists, it builds the overlay through `002282F0(argument)`; with no task
   it answers 0.

`002282F0` builds the `D0`<sub>h</sub>-byte overlay `00229590` into `01FD4940` when that is empty (`00228303`-`00228352`).
`01FD46FC` is set to 5 when an overlay is destroyed, so a new one cannot open for five calls.

### The inactive-window task

`00228490` builds the `D0`<sub>h</sub>-byte task `002284F0` into `01FD4948` ([Action availability](../Controls-And-Input/action-availability.md)).
`00228480` answers whether it exists.

| Message | What the task does |
|---|---|
| `1`, built | runs `00196710` on the input manager (`001E0980`), runs the drain over the root `0208EA40` (`00248030`), takes the focus unless `[0209AC30] + 308h` is set, attaches under `0208EA48`, and while a movie plays clears the active bit of message window 3 (`002E2570(3, 0)`) |
| `10`, its input turn | sets `022CBE34` to 5 (`00368810`); when channel 0's newest word from `0035EF10(0, 0)` equals the cancel mask `01E0C2A4`, writes 0 to `022CA5F0` (`0035ED40`), moves to state 1 and, while a movie plays, sets message window 3 active again |
| `2`, each tick | in state 1: posts window message `8002`<sub>h</sub> with 0 (`0017E500`), closes the overlay (`00244DD0`) and releases itself, state 3; then clears the mouse wheel (`001E0F20`), and while `[0209AC30] + 308h` is set treats the cancel word the same way, clearing the input words `02F97360`-`02F9739B` |
| `18`, destroyed | clears `01FD4948` and the wheel; gives the focus to `+C8`<sub>h</sub> when set |

`001EC5A0` answers whether a movie plays: the movie player's status `+4` is 3 (`001B7F20`, `001B7D20`,
[Movies](../Graphics/movies.md)). `0017E500(on)` sends the message `8002`<sub>h</sub> with 1 or 0 to the game
window `02EA5248`, the handle the window procedure `00798FF0` stores (`007990FF`).

### Building the overlay

On message 1 the overlay (`00229961`-`00229A98`):

1. prints `PauseMenu Create` (`0017DB70`) and clears bytes 0, 1 and 2 of the running object (`00183200(0)`,
   `00182FF0(0)`), below;
2. keeps its argument at `+C8`<sub>h</sub>, sets state `+C0`<sub>h</sub> to 0, and takes the 1920 x 1080 frame from `01E0C1D8` and
   `01E0C1DC` as its size;
3. sets bits 1, 0, 20 and 9 of action policy row 15 (`002E1C20`): bits 0, 1 and 9 keep the main menu, the battle
   menu and Escape Mode shut, and no reader tests bit 20;
4. builds button legend scenes `12`<sub>h</sub> and `0C`<sub>h</sub> (`0029DA70`) and formats text `467C`<sub>h</sub>, which holds only size and baseline codes,
   with it into `01FD4960` (`002B4090`);
5. attaches under `0208EA48` with priority -9.

With a non-zero argument it then opens screen layer 3, `002CCD40({3, descriptor, 100, 0})`, and moves to state 1.
The descriptor is `00908B40` when `00180120` answers 0, `022C7F84` is 0 and world lock 15 is not held
(`00226BD0(15)`), and `00908B50` otherwise.

`002CCCA0(descriptor, value)` and `002CCCF0(descriptor, value)` make the same call for layers 1 and 0. The
first serves `00241D40`, `003939B0`, `003F3E40`, `005704E0`, `00572890`, `00573980`, the shop `0057A620`,
`0057CD40` and the Save and Load screen `0057F7D0`; the second serves `002C19E0`.

`00180120` answers 1 while the event classification byte `01F832E9` is set (`001EC5C0`, a `spc_` event,
[Debug menu](../Engine-Core/debug-menu.md)) and `001EC560` holds: an event slot has queued events and
`00265680` answers 0.

### The stages

Each tick (message 2) moves the overlay through its states:

| State | Waits for | Then |
|---:|---|---|
| `0` | `01FD4954`, which `00229AE0` sets for the movie player (`001B7690`, `001B7F30`, `001B82A0`, `001B8400`) and `002CEB40` | clears it, opens layer 3 with `00908B50`, sets `+C8`<sub>h</sub> to 1, state 1 |
| `1` | layer 3's widget reports `+E8`<sub>h</sub> (`002CCC70(3)`) | pauses, below; state 2 |
| `2` | message 15, the close | state 3 |
| `3` | nothing | resumes, below; closes layer 3 (`002CCBC0(3)`), state 4 |
| `4` | layer 3's widget at `[0209AC30] + 2A8h` to be gone | clears the four policy bits (`002E1CA0`), turns the framework pause byte off (`0017E720(0)`) and releases itself |

On message 4 it draws, once paused with `+C8`<sub>h</sub> set, a sprite of the battle atlas (`0035D460`) centred on the frame
(`002D8CB0`), and in every state the text at `01FD4960` (`002D8910`).

### What pausing does

At state 1 the overlay prints `PauseMenu Open` and (`0022986B`-`002298F2`):

- saves the behind-camera switch `02098354` at `+C4`<sub>h</sub> and clears it (`0025A850`, `0025A880(0)`); the script verbs
  `tutorial_get_behindcameraenable` (`3A0`<sub>h</sub>) and `tutorial_set_behindcameraenable` (`3A1`<sub>h</sub>) read and write it;
- pauses the audio kinds `3F`<sub>h</sub> (`002DF370(3Fh, 1, 1)`, [Audio manager](../Sound-And-Music/audio-manager.md)) unless world
  lock 15 is held or `01E027FC` is 0, then sets `01E027FC` to 1;
- turns on the framework pause byte at `[01F810F0]` (`0017E720(1)`, `001997E0`;
  [Game application](../Engine-Core/game-application.md));
- unless the frame mode `00229EA0` is 5, sets byte 0 (`00183200(1)`, `0018A820`) and byte 2 (`00182FF0(1)`,
  `0018A830`) of the three-byte running object `[01F7F5D8]` (`0018A7D0`), whose byte 0 the frame tick reads to
  choose the pump's mode;
- when the monster viewer's settings byte `+118`<sub>h</sub> is set (`00181DD0`, `001EBA40`), sets its `+26E`<sub>h</sub> and the flag
  `800000`<sub>h</sub> of the render record of its id `+134`<sub>h</sub> (`00181E10(1)`, `001EBC70`, `002EF250`).

State 3 undoes each in turn (`002297F9`-`00229833`): audio on again unless lock 15 is held, the two bytes cleared
(`0018A820` with 0 also clears bytes 1 and 2), the behind-camera switch restored, and the viewer flag cleared unless
its `+26D`<sub>h</sub> is set.

## Modding notes

- The pause screen is a focus-loss pause only. The overlay is built only while the inactive-window task exists
  (`00228435`), and a raw call scan of the executable finds one call that starts the task, `002283AE`, taken when
  the window is not in front.
- What stops play is the audio mask, the policy bits and the task holding the input; the framework pause byte
  is set and cleared alongside them.
- `01FD46FC` makes the opener answer 1 for five calls after a pause screen closes, which keeps the field input off
  for those frames.

## Related

- [Action availability](../Controls-And-Input/action-availability.md) - row 15 and policy bit 21.
- [Controls](../Controls-And-Input/controls.md) - the input arbiter that calls the opener.
- [Widgets](widgets.md) - the focus, the roots and the release.
- [Audio manager](../Sound-And-Music/audio-manager.md) - the paused kinds.
- [Game application](../Engine-Core/game-application.md) - the framework pause byte and the running object.
