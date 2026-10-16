---
title: "PhyreEngine application framework: how the game process starts, runs its frames and shuts down"
kind: "system"
category: "PhyreEngine"
summary: "The PhyreEngine framework layer the game runs inside: the start-up function that brings up Steam, the settings, the single-instance mutex, the engine modules and the window, the run setup that calls the game's initApplication and initScene slots and starts the update thread, the per-frame update that calls the input, animate, resize and render slots, the window procedure's deferred requests, and the close, shutdown and restart paths."
addresses: ["007A3770", "007980A0", "00792350", "02EA5368", "0079E520", "0079B300", "0079F150", "007A4190", "007A4250", "007A4310", "007A3110", "007A0340", "00793E8C", "0079C140", "0079D920", "00798FF0", "0079B160", "0079B190", "0079EDD0", "007A42D0", "007A42E0", "0017E030", "0017E050", "01CB2508", "01CB2480", "02EA5245", "02EA5220", "02EA5228", "02EA5230"]
---

# PhyreEngine application framework: how the game process starts, runs its frames and shuts down

## What the player sees

Everything around the game itself: the one-instance check that refuses a second copy, the window and
its switches between windowed, borderless and full screen, alt-tab and minimise, the confirmation box
when the window is closed, and the restart after a display change that needs one. These come from
PhyreEngine's application framework (`Phyre::PFramework`), which owns the process, the window and the
frame loop and calls the game through the virtual slots of its application object.

## How it works

The game's application object is `GameApplication`, a static object whose class derives from
`Phyre::PFramework::PApplication`; its own slots (the archive mount, the frame tick, the init job) are
on [the game application page](../Engine-Core/game-application.md). This page covers the
framework side: what calls those slots, in what order and on which thread.

### Process start

The program's main function `007A3770` calls the framework start-up `007980A0` on both arms of its
`IsDebuggerPresent` test. The application object exists before that: `GameApplication`'s static
initialiser runs the `PApplication` constructor `00792350`, which stores the object's address in the
global `02EA5368` (`00792550`), sets the default size 1280 by 720 (`+0xD24`, `+0xD28`) and names the
object `PhyreFrameworkApplication`.

### The start-up function `007980A0`

In order:

1. `SetUnhandledExceptionFilter`, `ImmDisableIME`, `CoInitializeEx`; then the Steam context
   (see [Steam integration](../Steam-And-Achievements/steam-integration.md)):
   - `SteamAPI_Init` runs when the context's utils slot `+0x18` is empty; the `jne` at `00798121`
     skips it when the slot is filled.
   - When `SteamAPI_Init` succeeds (or the utils interface is already present), the Steam callback
     set-up (`0020CD30`, `008655E0`) runs (`0079811C`-`00798137`).
   - `SteamAPI_RestartAppIfNecessary(0x91640)` (`0079813C`) runs either way and calls `exit(1)` when Steam asks
     for a relaunch.
2. The Steam callback object (`007A0810`), the `My Games\FINAL FANTASY XII THE ZODIAC AGE\<SteamID>\`
   folder (`0079FA00` and the path built after it), and the game settings object, `0x65C` bytes
   (`001DE050`), stored at `01F82D20`, read from its file or created with defaults (`001DED50`).
3. The mutex `A8825348-F5CE-4E67-8735-D4AF7E7E58F1`. When it already exists (`ERROR_ALREADY_EXISTS`)
   or the settings file can be neither read nor written, a message box whose text comes from the string resources (`0019A510`)
   is shown and the function returns.
4. The command line, converted to narrow strings; then application slot 1 (`00798542`), which
   registers the application's script methods.
5. Window mode, size and options copied from the settings into the application (`+0xD20` full screen
   when the settings' mode is 1, `+0xD24`/`+0xD28` the size), and a `PWindow` object on the stack
   (vtable `01CB2480`).
6. `007979B0` (worker count from the process affinity mask), the engine module start-up `005A08E0`
   (`00798603`; [Phyre modules](phyre-modules.md)), and `0079E520`, which creates the window and runs
   the run setup. A non-zero result from any of the three runs the module shutdown and returns 1.
7. Two device callbacks, `00798910` and `007989B0`; the update thread is told its window
   (`007A4240`, `00798653`), which releases it; then the `GetMessageW` loop until `WM_QUIT`, bracketed
   by `SetThreadExecutionState`.

### Window and run setup

`0079E520` creates the window through `0079B300`, which registers the class `PhyreFrameworkClass` and
calls `CreateWindowExW`, fills the render-interface parameter block at `01F403A8` from the window and
the settings, points the application's `+0xD10` at it, and calls the run setup `0079F150`. It then
lowers the main thread's priority by one step (`SetThreadPriority(-1)`); on a failed run setup it runs
the application shutdown `0079EDD0`.

The run setup `0079F150` resets the timing fields, initialises the Phyre render interface, the render
thread and DirectInput (`00797910`), then calls application slot 2 (`0079F591`, logged on failure as
`initApplication`).

It then allocates a 96 MiB arena (`+0xDE8`) split 64 MiB and 32 MiB for the render
context at `+0xE8` (`00607E20`) and a 2 MiB block (`+0xDF0`), starts the worker threads when more than
one processor is available (`0060E9C0`), calls slot 3 (`0079F69A`, `initScene`), and finally creates
the update thread `PhyreFrameworkApplicationUpdateThread` (`007A4250`, `0079F709`). Any stage's
non-zero result is returned and ends the start-up.

Three options of the run setup never run in the shipped game: a script file (`02EA5220`), a log file
(`02EA5228`) and an input-replay file (`02EA5230`) are all zero and have no writer. So the console
object at `+0x58` stays null, the per-frame function `+0xD18` keeps `00793E8C`, and the input
recorder (slot 30) and replay (slot 29) are never called.

### The update thread

The game runs on the update thread, not on the thread that pumps window messages. The thread object
is the static `02EACF10` (`007A4190`); its body `007A4310` spins with `Sleep(0)` until the window is
handed to it, then loops while its run word `+0x50` is non-zero, calling the window's two slots:

- slot 0, `007A3110`: returns 9 when the quit byte `+0x69` is set; otherwise `SteamAPI_RunCallbacks`
  and the input poll `007A2440` on the application's input object `+0xDF8`;
- slot 1, `007A0340`: applies a pending drawing-area size change queued by the window procedure, returns 9
  on the quit byte, and otherwise jumps through the application's `+0xD18` (`007A03C4`). `00793E8C`
  there tail-jumps to slot 28, the per-frame update `0079C140`.

A non-zero result sets the thread's byte `+0x29` and the loop goes on. When the run word is cleared
the thread posts `WM_CLOSE` with `wParam` 3 to the window (`007A436D`) and runs the game's
`0035E700`, which signals the two objects at `022CA610` and `022CA618` and waits for `022CA630` to
reach zero.

### The per-frame update `0079C140`

Inherited unchanged by `GameApplication` (slot 28 holds the same address in both vtables). Each call:

1. When a screen-mode change is pending (`+0x20`), copies the size and frame rate from the settings.
2. Time (`0079D920`): with a fixed step at `+0x6C` the delta `+0x48` is the step and the total `+0x40`
   grows by it; otherwise the total is the performance-counter time since engine start (`02CB60E8`)
   less `+0x50`, and the delta is the change in the total.
3. Returns 9 when the quit byte `+0x69` is set. On the first frame (`+0x64` = 0) clears the delta and
   calls slot 9, resize (`0079C1F1`). Counts the frame at `+0x64`.
4. Calls slot 30 when a log stream is open, polls the input devices (`0079D010`, `0079C260`) unless a
   mode, focus or size request is pending, and calls slot 7, input (`0079C26B`).
5. Measures frames per second over two seconds into `+0x60`, then calls slot 4, animate (`0079C2D6`).
6. Handles the deferred window requests (below), calling slot 9 again after a size change
   (`0079C526`).
7. Calls each viewport's slot 3 (`0079C5FE`) with the render context, then slot 8, render
   (`0079C655`). When `01FD4A68` is clear and render returned 0, it also runs `00600C20` on the render
   context and the context's slot 2.

A non-zero result from animate, resize, a viewport or render is logged (`App failed during animate`,
`resize`, `viewport render`, `render`) and returned. The game's own slots behind these calls are on
[the game application page](../Engine-Core/game-application.md).

### Deferred window requests

The window procedure `00798FF0` runs on the main thread and does not touch the renderer. The
inherited request slots only set a flag and store their arguments, and the per-frame update does the
work on the update thread:

| Slot | Body | Flag set | Work done by `0079C140` |
|---|---|---|---|
| 12 | `007A0B10` | `+0x20`, `+0x1E`; mode `+0xD20` | full screen or window at `+0xD24` by `+0xD28`; a failed full-screen switch logs and falls back to window mode |
| 13 | `0079F140` | `+0x21`; argument `+0x26` | `0079F0F0`: `ShowWindow` restore (9) or minimise (6) |
| 18 | `007A1180` | `+0x29`; size `+0x2C`, `+0x30` | resize through the device (`0062AAB0`) |
| 19 | `007A0AF0` | `+0x22`, or clears `+0x23` | re-checks the monitor's mode |
| 20 | `007A0FB0` | `+0x24` | `0079EBA0`: saves the window position into the settings |

The window procedure calls slot 14 when the new window is the foreground window (`WM_CREATE`), slot 20
on `WM_MOVE`, and slot 17 with 1 or 0 around a mouse press on the title bar or border, installing a `WH_MOUSE` hook
(`00798F80`) for its duration. Activation changes go to the update thread through `007A3BD0` on the
window's `+0x48` queue, and a new drawing-area size is parked in the window's `+0x1C` (`007A07C0`) for the
window's slot 1 to apply.

### Close, shutdown and restart

`WM_CLOSE` carries the reason in `wParam`:

- 1 or 2: sets the quit byte `+0x69` and clears the update thread's run word (`007A42D0`). The game
  posts 1 through `0017E030` (called from `002280B0`).
- 4: the same through `0079B160`, and sets `02EA5245`, the restart request. The game posts 4 through
  `0017E050` after a display change that needs a restart ([config screen](../Menus-And-HUD/config-screen.md)).
- 3: posted by the update thread as it exits; `0079B190` runs the application shutdown `0079EDD0`,
  releases the device context and destroys the window, whose `WM_DESTROY` posts `WM_QUIT`.
- any other value, including 0 from the window's own close: ignored while the bytes `02B40E00` and `02CA99B0` are both set;
  otherwise quits at once in full-screen mode, and in the other modes shows an OK/Cancel box from the
  string resources and quits on OK. A Steam state check on the callback object (`00865510`) can take
  the first close without quitting.

The application shutdown `0079EDD0` stops the update thread (`007A42E0`), releases the viewports,
calls slot 5 (`0079EF47`, `exitScene`) and slot 6 (`0079EF75`, `exitApplication`), then tears down
the settings block, the renderer, the arenas and the input layer (`00799860`, `PInput::Terminate`).

When the message loop ends, `007980A0` unregisters the Steam callbacks, calls `CoUninitialize`, runs
the module shutdown `005A0840` (`007986D5`), closes the mutex and frees the argument strings. With
`02EA5245` set it then brings the window forward, takes its own path from `GetModuleFileNameA` and
starts it again with `CreateProcessA` and the arguments `"-scmd" "appid" "100" -nologo`. Both paths
end in `ExitProcess(0)` (`0079887F`).

## Layouts

The `PApplication` part of the application object, as the framework functions above use it. The
`GameApplication` fields from `+0x1130` on are on the game application page.

```
PApplication  (base of GameApplication; address in 02EA5368)
+0x000  ptr   vtable 01CB2508 (GameApplication: 008C5760)
+0x010  ptr   PProcessorProfileTimelineCpu sub-object (its vtable)
+0x01E  u8    resize pending (slot 12, run setup)
+0x01F  u8    window-style refresh pending
+0x020  u8    screen-mode change pending (slot 12)
+0x021  u8    focus request pending (slot 13)     +0x026 u8  restore (1) or minimise (0)
+0x022  u8    monitor re-check pending (slot 19)  +0x023 u8  skip the next re-check
+0x024  u8    window moved (slot 20)
+0x028  u8    title-bar or border mouse press (slot 17)
+0x029  u8    resize pending (slot 18)            +0x02C i32 width  +0x030 i32 height
+0x03C  i32   frame rate used for a full-screen switch
+0x040  f64   total elapsed time
+0x048  f64   frame delta
+0x050  f64   time offset taken at run setup
+0x058  ptr   console object (script or replay mode only)
+0x060  f32   frames per second, measured over two seconds
+0x064  u32   frame counter
+0x069  u8    quit
+0x06C  f32   fixed time step, 0 = real time
+0x0E8  ...   render context
+0xD10  ptr   render-interface parameter block (01F403A8)
+0xD18  ptr   per-frame function: 00793E8C (slot 28) or 00793E98 (slot 29)
+0xD20  u8    full screen
+0xD24  i32   width (default 1280)                +0xD28 i32 height (default 720)
+0xD98  ptr   input-recording stream
+0xDB8  u32   viewport count                      +0xDC0 ptr viewport array
+0xDE8  ptr   96 MiB arena                        +0xDF0 ptr 2 MiB block
+0xDF8  ptr   input object
```

The application vtable slots the framework calls, named by the framework's own log strings where it
has them:

| Slot | Offset | Called from | Role |
|---|---|---|---|
| 1 | `+0x08` | `00798542` | script method registration |
| 2 | `+0x10` | `0079F591` | `initApplication` |
| 3 | `+0x18` | `0079F69A` | `initScene` |
| 4 | `+0x20` | `0079C2D6` | animate |
| 5 | `+0x28` | `0079EF47` | `exitScene` |
| 6 | `+0x30` | `0079EF75` | `exitApplication` |
| 7 | `+0x38` | `0079C26B` | input |
| 8 | `+0x40` | `0079C655` | render |
| 9 | `+0x48` | `0079C1F1`, `0079C526` | resize |
| 14, 17, 20 | `+0x70`, `+0x88`, `+0xA0` | the window procedure | foreground, title-bar press, move |
| 28 | `+0xE0` | `00793E8C` | per-frame update |
| 29, 30 | `+0xE8`, `+0xF0` | `00793E98`, `0079C23A` | input replay and recording |

`GameApplication` overrides slots 10, 15 and 16, but its overrides are referenced only by its vtable,
and no virtual call in the framework's code or in any function that loads `02EA5368` or calls its
getter `00796E20` goes through those slots.

The framework's other classes sit beside `PApplication` in `.rdata`:

| Vtable | Class | Slots |
|---|---|---:|
| `01CB2430` | `PInputDeviceKeyboard` | 6 |
| `01CB2468` | `PWindowWin32Base` | 2 |
| `01CB2480` | `PWindow` | 2 |
| `01CB2498` | `PApplicationScriptBuffer` | 1 |
| `01CB24A8` | `PApplicationScript` | 1 |
| `01CB24B8` | `PApplicationScriptProxy` | 1 |
| `01CB24C8` | `PInputDevicePad` | 7 |
| `01CB2508` | `PApplication` | 31 |
| `01CB2608` | `PApplicationViewport` | 5 |
| `01CB2638` | `PInputDevicePadDirectInput` | 7 |
| `01CB2678` | `PInputDevicePadXInput` | 7 |
| `01CB26B8` | `PInputDevicePadSteamController` | 7 |

[phyre-application-p-application-accesses.tsv](phyre-application-p-application-accesses.tsv) lists
1,076 instructions in 62 functions that read or write fields of the application object.

## Shipped data

| Fact | Value |
|---|---|
| window class | `PhyreFrameworkClass` |
| single-instance mutex | `A8825348-F5CE-4E67-8735-D4AF7E7E58F1` |
| Steam app id passed to `SteamAPI_RestartAppIfNecessary` | `0x91640` (595,520) |
| restart arguments | `"-scmd" "appid" "100" -nologo` |
| update thread name | `PhyreFrameworkApplicationUpdateThread` |
| default size | 1280 by 720 |
| arenas | 96 MiB (64 MiB and 32 MiB halves), 2 MiB |
| frame-rate window | 2.0 seconds |

## Modding notes

- Game logic runs on the update thread. Code hooked into the window procedure runs on the main
  thread and must hand work over, as the framework does with its request flags.
- Setting `+0x69` on the object at `02EA5368` makes every later frame return 9 at once; quitting
  cleanly needs the update thread's run word cleared as well, which `0079B160` does.
- Posting `WM_CLOSE` with `wParam` 4 quits and starts the executable again.
- A fixed time step can be forced by writing `+0x6C`; the delta then no longer follows real time.

## Related

- [Game application](../Engine-Core/game-application.md): the `GameApplication` object and
  the slots it overrides.
- [Frame update order](../Engine-Core/frame-update-order.md): what the game's frame does
  inside the animate slot.
- [Phyre modules](phyre-modules.md): the engine modules `005A08E0` starts and `005A0840` stops.
- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI the class names come from.
- [Debug logging](../Engine-Core/debug-logging.md): the log call behind the failure messages.
- [Config screen](../Menus-And-HUD/config-screen.md): the display changes that end in a restart.
- [Keymap file](../Controls-And-Input/keymap-file.md): the `My Games` folder the start-up builds.
