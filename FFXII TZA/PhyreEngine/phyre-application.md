---
title: "PhyreEngine application framework: how the game process starts, runs its frames and shuts down"
kind: "system"
category: "PhyreEngine"
addresses: "007A3770, 007980A0, 00792350, 02EA5368, 0079E520, 0079B300, 0079F150, 007A4190, 007A4250, 007A4310, 007A3110, 007A0340, 00793E8C, 0079C140, 0079D920, 00798FF0, 0079B160, 0079B190, 0079EDD0, 007A42D0, 007A42E0, 0017E030, 0017E050, 01CB2508, 01CB2480, 02EA5245, 02EA5220, 02EA5228, 02EA5230, 007A0180, 00799980"
---

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
global `02EA5368` (`00792550`), sets the default size 1280 by 720 (`+D24`<sub>h</sub>, `+D28`<sub>h</sub>) and names the
object `PhyreFrameworkApplication`.

### The start-up function `007980A0`

In order:

1. `SetUnhandledExceptionFilter`, `ImmDisableIME`, `CoInitializeEx`; then the Steam context
   (see [Steam integration](../Steam-And-Achievements/steam-integration.md)):
   - `SteamAPI_Init` runs when the context's utils slot `+18`<sub>h</sub> is empty; the `jne` at `00798121`
     skips it when the slot is filled.
   - When `SteamAPI_Init` succeeds (or the utils interface is already present), the Steam callback
     set-up (`0020CD30`, `008655E0`) runs (`0079811C`-`00798137`).
   - `SteamAPI_RestartAppIfNecessary(91640h)` (`0079813C`) runs either way and calls `exit(1)` when Steam asks
     for a relaunch.
2. The Steam callback object (`007A0810`), the `My Games\FINAL FANTASY XII THE ZODIAC AGE\<SteamID>\`
   folder (`0079FA00` and the path built after it), and the game settings object, `65C`<sub>h</sub> bytes
   (`001DE050`), stored at `01F82D20`, read from its file or created with defaults (`001DED50`).
3. The mutex `A8825348-F5CE-4E67-8735-D4AF7E7E58F1`. When it already exists (`ERROR_ALREADY_EXISTS`)
   or the settings file can be neither read nor written, a message box whose text comes from the string resources (`0019A510`)
   is shown and the function returns.
4. The command line, converted to narrow strings; then application slot 1 (`00798542`), which
   registers the application's script methods.
5. Window mode, size and options copied from the settings into the application (`+D20`<sub>h</sub> full screen
   when the settings' mode is 1, `+D24`<sub>h</sub>/`+D28`<sub>h</sub> the size), and a `PWindow` object on the stack
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
the settings, points the application's `+D10`<sub>h</sub> at it, and calls the run setup `0079F150`. It then
lowers the main thread's priority by one step (`SetThreadPriority(-1)`); on a failed run setup it runs
the application shutdown `0079EDD0`.

The run setup `0079F150` resets the timing fields, initialises the Phyre render interface, the render
thread and DirectInput (`00797910`), then calls application slot 2 (`0079F591`, logged on failure as
`initApplication`).

It then allocates a 96 MiB arena (`+DE8`<sub>h</sub>) split 64 MiB and 32 MiB for the render
context at `+E8`<sub>h</sub> (`00607E20`) and a 2 MiB block (`+DF0`<sub>h</sub>), starts the worker threads when more than
one processor is available (`0060E9C0`), calls slot 3 (`0079F69A`, `initScene`), and finally creates
the update thread `PhyreFrameworkApplicationUpdateThread` (`007A4250`, `0079F709`). Any stage's
non-zero result is returned and ends the start-up.

Three options of the run setup never run in the shipped game: a script file (`02EA5220`), a log file
(`02EA5228`) and an input-replay file (`02EA5230`) are all zero and have no writer. So the console
object at `+58`<sub>h</sub> stays null, the per-frame function `+D18`<sub>h</sub> keeps `00793E8C`, and the input
recorder (slot 30) and replay (slot 29) are never called.

### The script commands

The script-file and input-replay options would each create a `PApplicationScriptProxy` as that
console object, and both call `007A0180` on it: `00792760` for a script file, and the run setup itself
(`0079F3F9`) for a replay. It registers sixteen commands through `007A0090`, which appends a `50`<sub>h</sub>-byte record,
the handler at `+00`<sub>h</sub> and a name of up to 64 characters at `+08`<sub>h</sub>, to the proxy's array (`+28`<sub>h</sub>,
count `+30`<sub>h</sub>, capacity `+34`<sub>h</sub>, grown to twice the capacity or 16).

| Command | Handler | Command | Handler |
|---|---|---|---|
| `Frames` | `00796490` | `ButtonDown` | `00795800` |
| `Timestep` | `00799980` | `ButtonUp` | `00795A00` |
| `Framerate` | `007963C0` | `Buttonpress` | `00795C00` |
| `MinFramerate` | `005C5230` (returns 0) | `Mousepress` | `00798000` |
| `RenderFrame` | `00798A80` | `InputSource` | `00797A20` |
| `Keypress` | `00797F60` | `Expect` | `005C5230` (returns 0) |
| `KeyDown` | `00797EE0` | `Echo` | `00796210` |
| `KeyUp` | `00797F20` | `Quit` | `00798A30` |

`Timestep` (`00799980`) reads one float with `%f` (`0071F970`, `vsscanf`) into the fixed step `+6C`<sub>h</sub>.
A value of 0 or less returns to real time: it sets the offset `+50`<sub>h</sub> to the time since engine start
(`02CB60E8`) less the total `+40`<sub>h</sub>, so the total carries on from where the fixed steps left it.
Because neither option is ever set, none of these commands runs.

### The update thread

The game runs on the update thread, not on the thread that pumps window messages. The thread object
is the static `02EACF10` (`007A4190`); its body `007A4310` spins with `Sleep(0)` until the window is
handed to it, then loops while its run word `+50`<sub>h</sub> is non-zero, calling the window's two slots:

- slot 0, `007A3110`: returns 9 when the quit byte `+69`<sub>h</sub> is set; otherwise `SteamAPI_RunCallbacks`
  and the input poll `007A2440` on the application's input object `+DF8`<sub>h</sub>;
- slot 1, `007A0340`: applies a pending drawing-area size change queued by the window procedure, returns 9
  on the quit byte, and otherwise jumps through the application's `+D18`<sub>h</sub> (`007A03C4`). `00793E8C`
  there tail-jumps to slot 28, the per-frame update `0079C140`.

A non-zero result sets the thread's byte `+29`<sub>h</sub> and the loop goes on. When the run word is cleared
the thread posts `WM_CLOSE` with `wParam` 3 to the window (`007A436D`) and runs the game's
`0035E700`, which signals the two objects at `022CA610` and `022CA618` and waits for `022CA630` to
reach zero.

### The per-frame update `0079C140`

Inherited unchanged by `GameApplication` (slot 28 holds the same address in both vtables). Each call:

1. When a screen-mode change is pending (`+20`<sub>h</sub>), copies the size and frame rate from the settings.
2. Time (`0079D920`): with a fixed step at `+6C`<sub>h</sub> the delta `+48`<sub>h</sub> is the step and the total `+40`<sub>h</sub>
   grows by it; otherwise the total is the performance-counter time since engine start (`02CB60E8`)
   less `+50`<sub>h</sub>, and the delta is the change in the total.
3. Returns 9 when the quit byte `+69`<sub>h</sub> is set. On the first frame (`+64`<sub>h</sub> = 0) clears the delta and
   calls slot 9, resize (`0079C1F1`). Counts the frame at `+64`<sub>h</sub>.
4. Calls slot 30 when a log stream is open, polls the input devices (`0079D010`, `0079C260`) unless a
   mode, focus or size request is pending, and calls slot 7, input (`0079C26B`).
5. Measures frames per second over two seconds into `+60`<sub>h</sub>, then calls slot 4, animate (`0079C2D6`).
6. Handles the deferred window requests (below), calling slot 9 again after a size change
   (`0079C526`).
7. Calls each viewport's slot 3 (`0079C5FE`) with the render context, then slot 8, render
   (`0079C655`). When `01FD4A68` is clear and render returned 0, it also runs `00600C20` on the render
   context and the context's slot 2.

One branch of the deferred window requests (`0079C4B1`) clears `+20`<sub>h</sub>, sets the bytes `+1E`<sub>h</sub> and `+23`<sub>h</sub> and
calls `00183260`, which sets byte `+02`<sub>h</sub> of the game's render manager (`00189120`) when one exists.

A non-zero result from animate, resize, a viewport or render is logged (`App failed during animate`,
`resize`, `viewport render`, `render`) and returned. The game's own slots behind these calls are on
[the game application page](../Engine-Core/game-application.md).

### Deferred window requests

The window procedure `00798FF0` runs on the main thread and does not touch the renderer. The
inherited request slots only set a flag and store their arguments, and the per-frame update does the
work on the update thread:

| Slot | Body | Flag set | Work done by `0079C140` |
|---|---|---|---|
| 12 | `007A0B10` | `+20`<sub>h</sub>, `+1E`<sub>h</sub>; mode `+D20`<sub>h</sub> | full screen or window at `+D24`<sub>h</sub> by `+D28`<sub>h</sub>; a failed full-screen switch logs and falls back to window mode |
| 13 | `0079F140` | `+21`<sub>h</sub>; argument `+26`<sub>h</sub> | `0079F0F0`: `ShowWindow` restore (9) or minimise (6) |
| 18 | `007A1180` | `+29`<sub>h</sub>; size `+2C`<sub>h</sub>, `+30`<sub>h</sub> | resize through the device (`0062AAB0`) |
| 19 | `007A0AF0` | `+22`<sub>h</sub>, or clears `+23`<sub>h</sub> | re-checks the monitor's mode |
| 20 | `007A0FB0` | `+24`<sub>h</sub> | `0079EBA0`: saves the window position into the settings |

The window procedure calls slot 14 when the new window is the foreground window (`WM_CREATE`), slot 20
on `WM_MOVE`, and slot 17 with 1 or 0 around a mouse press on the title bar or border, installing a `WH_MOUSE` hook
(`00798F80`) for its duration. Activation changes go to the update thread through `007A3BD0` on the
window's `+48`<sub>h</sub> queue, and a new drawing-area size is parked in the window's `+1C`<sub>h</sub> (`007A07C0`) for the
window's slot 1 to apply.

### Window helpers

- `007A0FC0` (`00798277`) sets the thread's interface language from the language setting `[01F82D20]` `+00`<sub>h</sub>
  (`SetThreadUILanguage`): 1 `409`<sub>h</sub>, 2 `40C`<sub>h</sub>, 3 `407`<sub>h</sub>, 4 `410`<sub>h</sub>, 5 `40A`<sub>h</sub>, 6 `412`<sub>h</sub>, 7 `7C04`<sub>h</sub>,
  8 `804`<sub>h</sub>, any other `411`<sub>h</sub>.
- `0079F750` is the size callback (`0079C558`). By ScreenMode (`+08`<sub>h</sub> of the settings) it gives the window the style
  `CF0000`<sub>h</sub> and the WindowSize at the saved position `+6C`<sub>h</sub>/`+70`<sub>h</sub> (0, windowed), only logs (1, full screen), or
  gives it `WS_POPUP` over the monitor rectangle `0017E220` or the screen (2), each time logging
  `[Screen Mode]onSizeCallBack ...` ([Screen mode and aspect](../Graphics/screen-mode-and-aspect.md)).
- `007A04F0` (`001DC78C`) queues request 1 with the WindowSize or the Resolution, by ScreenMode, on the window
  object's queue `+48`<sub>h</sub> (`007A3BD0`).
- `00796310(full)` maximises the window (`ShowWindow` 3), or for 0 maximises and restores it (9)
  (`007A3CE2`, `007A3D41`, `007A4069`, `007A408F`).
- `0079B0B0` stores in `02EA5213` whether the game window `02EA5248` is the foreground window (`007A3E27`,
  `007A3EFF`, `007A40EC`); `0079EC80` brings it forward (`AttachThreadInput`, topmost and back, `SetForegroundWindow`,
  `SwitchToThisWindow`; `00799123`, `007A3F19`); `0079ED60(free)` clips the cursor to the drawing area, or frees it
  (`007A0A89`).
- `00798EB0` is a hook procedure the window procedure installs (`00799264`): on code 5 it centres any other window
  that activates on the screen `01F3DA1C` by `01F3DA20`, then passes the call on (`CallNextHookEx`, `02EA5258`).
- `0079F740` and `0079F9D0` set the window object's bytes `+1E`<sub>h</sub> and `+1F`<sub>h</sub>, and `007A0FA0(v)` stores `02EA5247`,
  from the window-event code `007A3A60`-`007A40B0`; `007A3D70(obj, i)` makes one of the three objects at `+00`<sub>h</sub>,
  `+08`<sub>h</sub>, `+10`<sub>h</sub> current at `+30`<sub>h</sub> and calls its slots `+10`<sub>h</sub> and `+18`<sub>h</sub> (`0079E614`).
- `007A1320` (`0079F0AA`, at shutdown) unlinks the input object's devices, the one at `+150`<sub>h</sub> and the 18 at `+88`<sub>h</sub>,
  from their listener lists.
- `007A37B0` is a `swscanf` (`__stdio_common_vswscanf`) for the XInput test `00797AD0` (`00797D4F`, `00797D8C`;
  [Controllers](../Controls-And-Input/controllers.md)); `0079DA10` (`0079E31B`) builds the input layer's sources, objects
  with the type tags `01F44D90` to `01F44FD0`, two thresholds taken with `sqrtf` and `cosf`.

### Script and replay helpers

These serve the script-file and input-replay options, so they never run in the shipped game:

- `0079BDF0` runs the next command line (`007A08D6`): a pending `Frames` count steps down and runs `Frames` again;
  otherwise it parses `name(arguments)` (`0079BFD0`) and calls the handler, or logs `Unrecognised command %s(%s)`.
- `0079BFD0` splits a line at its parentheses (`Badly formed command %s`); `007A1230` skips spaces and `#` comment
  lines (`0079C0D0` finds the line end), `0079C0F0` finds the next space, and `0079D9A0(text, end, quote)` returns the
  text between two quote characters.
- `007A08F0` maps the `Buttonpress` names to pad bytes of `[+DF8h] + 88h`: `Square` `30`<sub>h</sub>, `Cross` `31`<sub>h</sub>,
  `Circle` `32`<sub>h</sub>, `Triangle` `33`<sub>h</sub>, `Select` `38`<sub>h</sub>, `Start` `39`<sub>h</sub>, `Up` `3C`<sub>h</sub>, `Right` `3D`<sub>h</sub>, `Down` `3E`<sub>h</sub>,
  `Left` `3F`<sub>h</sub>; any other name logs and returns 5.
- `00798AC0` is `RenderFrame`'s screenshot: it logs `PApplication::screenshot: %s`, reads the frame back under the
  render lock (`00615BC0`, `00624960`, `0061EE30`, `00616700`), swaps red and blue and writes a 24-bit BMP.
- `0079A120` replays one record, logged as `INPUT:...`: kind 1 sets a pad byte, kind 2 an action found by name
  (`00873C50`, `00873C40`), kind 3 runs a command; `0079A550` and `00799C90` append a `40`<sub>h</sub>-byte record, and
  `0079D430(file)` reads the replay file's `%d:` lines and returns the last number.

The engine's smaller helpers (threads, locks, arrays, pools and the D3D11 resource accessors) are listed with their
callers in [phyre-engine-helpers.tsv](phyre-engine-helpers.tsv).

### Close, shutdown and restart

`WM_CLOSE` carries the reason in `wParam`:

- 1 or 2: sets the quit byte `+69`<sub>h</sub> and clears the update thread's run word (`007A42D0`). The game
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
`GameApplication` fields from `+1130`<sub>h</sub> on are on the game application page.

PApplication  (base of GameApplication; address in `02EA5368`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `void*` | vtable 01CB2508 (GameApplication: 008C5760) |  |
| `010`<sub>h</sub> | `void*` | PProcessorProfileTimelineCpu sub-object (its vtable) |  |
| `01E`<sub>h</sub> | `u8` | resize pending (slot 12, run setup) |  |
| `01F`<sub>h</sub> | `u8` | window-style refresh pending |  |
| `020`<sub>h</sub> | `u8` | screen-mode change pending (slot 12) |  |
| `021`<sub>h</sub> | `u8` | focus request pending (slot 13) | +`026`<sub>h</sub> u8  restore (1) or minimise (0) |
| `022`<sub>h</sub> | `u8` | monitor re-check pending (slot 19) | +`023`<sub>h</sub> u8  skip the next re-check |
| `024`<sub>h</sub> | `u8` | window moved (slot 20) |  |
| `028`<sub>h</sub> | `u8` | title-bar or border mouse press (slot 17) |  |
| `029`<sub>h</sub> | `u8` | resize pending (slot 18) | +`02C`<sub>h</sub> i32 width  +`030`<sub>h</sub> i32 height |
| `03C`<sub>h</sub> | `i32` | frame rate used for a full-screen switch |  |
| `040`<sub>h</sub> | `f64` | total elapsed time |  |
| `048`<sub>h</sub> | `f64` | frame delta |  |
| `050`<sub>h</sub> | `f64` | time offset taken at run setup |  |
| `058`<sub>h</sub> | `void*` | console object (script or replay mode only) |  |
| `060`<sub>h</sub> | `f32` | frames per second, measured over two seconds |  |
| `064`<sub>h</sub> | `u32` | frame counter |  |
| `069`<sub>h</sub> | `u8` | quit |  |
| `06C`<sub>h</sub> | `f32` | fixed time step, 0 = real time |  |
| `0E8`<sub>h</sub> | `...` | render context |  |
| `D10`<sub>h</sub> | `void*` | render-interface parameter block (01F403A8) |  |
| `D18`<sub>h</sub> | `void*` | per-frame function: 00793E8C (slot 28) or 00793E98 (slot 29) |  |
| `D20`<sub>h</sub> | `u8` | full screen |  |
| `D24`<sub>h</sub> | `i32` | width (default 1280) | +`D28`<sub>h</sub> i32 height (default 720) |
| `D98`<sub>h</sub> | `void*` | input-recording stream |  |
| `DB8`<sub>h</sub> | `u32` | viewport count | +`DC0`<sub>h</sub> ptr viewport array |
| `DE8`<sub>h</sub> | `void*` | 96 MiB arena | +`DF0`<sub>h</sub> ptr 2 MiB block |
| `DF8`<sub>h</sub> | `void*` | input object |  |

The application vtable slots the framework calls, named by the framework's own log strings where it
has them:

| Slot | Offset | Called from | Role |
|---|---|---|---|
| 1 | `+08`<sub>h</sub> | `00798542` | script method registration |
| 2 | `+10`<sub>h</sub> | `0079F591` | `initApplication` |
| 3 | `+18`<sub>h</sub> | `0079F69A` | `initScene` |
| 4 | `+20`<sub>h</sub> | `0079C2D6` | animate |
| 5 | `+28`<sub>h</sub> | `0079EF47` | `exitScene` |
| 6 | `+30`<sub>h</sub> | `0079EF75` | `exitApplication` |
| 7 | `+38`<sub>h</sub> | `0079C26B` | input |
| 8 | `+40`<sub>h</sub> | `0079C655` | render |
| 9 | `+48`<sub>h</sub> | `0079C1F1`, `0079C526` | resize |
| 14, 17, 20 | `+70`<sub>h</sub>, `+88`<sub>h</sub>, `+A0`<sub>h</sub> | the window procedure | foreground, title-bar press, move |
| 28 | `+E0`<sub>h</sub> | `00793E8C` | per-frame update |
| 29, 30 | `+E8`<sub>h</sub>, `+F0`<sub>h</sub> | `00793E98`, `0079C23A` | input replay and recording |

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
| Steam app id passed to `SteamAPI_RestartAppIfNecessary` | `91640`<sub>h</sub> (595,520) |
| restart arguments | `"-scmd" "appid" "100" -nologo` |
| update thread name | `PhyreFrameworkApplicationUpdateThread` |
| default size | 1280 by 720 |
| arenas | 96 MiB (64 MiB and 32 MiB halves), 2 MiB |
| frame-rate window | 2.0 seconds |

## Modding notes

- Game logic runs on the update thread. Code hooked into the window procedure runs on the main
  thread and must hand work over, as the framework does with its request flags.
- Setting `+69`<sub>h</sub> on the object at `02EA5368` makes every later frame return 9 at once; quitting
  cleanly needs the update thread's run word cleared as well, which `0079B160` does.
- Posting `WM_CLOSE` with `wParam` 4 quits and starts the executable again.
- A fixed time step can be forced by writing `+6C`<sub>h</sub>; the delta then no longer follows real time.

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
