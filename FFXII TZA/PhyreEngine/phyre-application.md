---
title: "PhyreEngine application framework: how the game process starts, runs its frames and shuts down"
kind: "system"
category: "PhyreEngine"
addresses: "0x007A3770, 0x007980A0, 0x00792350, 0x02EA5368, 0x0079E520, 0x0079B300, 0x0079F150, 0x007A4190, 0x007A4250, 0x007A4310, 0x007A3110, 0x007A0340, 0x00793E8C, 0x0079C140, 0x0079D920, 0x00798FF0, 0x0079B160, 0x0079B190, 0x0079EDD0, 0x007A42D0, 0x007A42E0, 0x0017E030, 0x0017E050, 0x01CB2508, 0x01CB2480, 0x02EA5245, 0x02EA5220, 0x02EA5228, 0x02EA5230, 0x007A0180, 0x00799980"
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

The program's main function `0x007A3770` calls the framework start-up `0x007980A0` on both arms of its
`IsDebuggerPresent` test. The application object exists before that: `GameApplication`'s static
initialiser runs the `PApplication` constructor `0x00792350`, which stores the object's address in the
global `0x02EA5368` (`0x00792550`), sets the default size 1280 by 720 (`+0xD24`, `+0xD28`) and names the
object `PhyreFrameworkApplication`.

### The start-up function `0x007980A0`

In order:

1. `SetUnhandledExceptionFilter`, `ImmDisableIME`, `CoInitializeEx`; then the Steam context
   (see [Steam integration](../Steam-And-Achievements/steam-integration.md)):
   - `SteamAPI_Init` runs when the context's utils slot `+0x18` is empty; the `jne` at `0x00798121`
     skips it when the slot is filled.
   - When `SteamAPI_Init` succeeds (or the utils interface is already present), the Steam callback
     set-up (`0x0020CD30`, `0x008655E0`) runs (`0x0079811C`-`0x00798137`).
   - `SteamAPI_RestartAppIfNecessary(0x91640)` (`0x0079813C`) runs either way and calls `exit(1)` when Steam asks
     for a relaunch.
2. The Steam callback object (`0x007A0810`), the `My Games\FINAL FANTASY XII THE ZODIAC AGE\<SteamID>\`
   folder (`0x0079FA00` and the path built after it), and the game settings object, `0x65C` bytes
   (`0x001DE050`), stored at `0x01F82D20`, read from its file or created with defaults (`0x001DED50`).
3. The mutex `A8825348-F5CE-4E67-8735-D4AF7E7E58F1`. When it already exists (`ERROR_ALREADY_EXISTS`)
   or the settings file can be neither read nor written, a message box whose text comes from the string resources (`0x0019A510`)
   is shown and the function returns.
4. The command line, converted to narrow strings; then application slot 1 (`0x00798542`), which
   registers the application's script methods.
5. Window mode, size and options copied from the settings into the application (`+0xD20` full screen
   when the settings' mode is 1, `+0xD24`/`+0xD28` the size), and a `PWindow` object on the stack
   (vtable `0x01CB2480`).
6. `0x007979B0` (worker count from the process affinity mask), the engine module start-up `0x005A08E0`
   (`0x00798603`; [Phyre modules](phyre-modules.md)), and `0x0079E520`, which creates the window and runs
   the run setup. A non-zero result from any of the three runs the module shutdown and returns 1.
7. Two device callbacks, `0x00798910` and `0x007989B0`; the update thread is told its window
   (`0x007A4240`, `0x00798653`), which releases it; then the `GetMessageW` loop until `WM_QUIT`, bracketed
   by `SetThreadExecutionState`.

### Window and run setup

`0x0079E520` creates the window through `0x0079B300`, which registers the class `PhyreFrameworkClass` and
calls `CreateWindowExW`; a negative result from `0x0079B300` returns 9 at once (`0x0079E544`-`0x0079E548`).
Otherwise it fills the render-interface parameter block at `0x01F403A8` from the window and
the settings, points the application's `+0xD10` at it, and calls the run setup `0x0079F150`.

It then lowers the main thread's priority by one step (`SetThreadPriority(-1)`, `0x0079E600`) and runs
`0x007A3D70` on the window's `+0x48` with ScreenMode, the settings' `+0x08` (`0x0079E606`-`0x0079E614`); on a
failed run setup it runs the application shutdown `0x0079EDD0` (`0x0079E624`). It returns the run setup's
result (`0x0079E62E`).

The run setup `0x0079F150` resets the timing fields, initialises the Phyre render interface, the render
thread and DirectInput (`0x00797910`), then calls application slot 2 (`0x0079F591`, logged on failure as
`initApplication`).

It then allocates a 96 MiB arena (`+0xDE8`) split 64 MiB and 32 MiB for the render
context at `+0xE8` (`0x00607E20`) and a 2 MiB block (`+0xDF0`), starts the worker threads when more than
one processor is available (`0x0060E9C0`), calls slot 3 (`0x0079F69A`, `initScene`), and finally creates
the update thread `PhyreFrameworkApplicationUpdateThread` (`0x007A4250`, `0x0079F709`). Any stage's
non-zero result is returned and ends the start-up.

Three options of the run setup never run in the shipped game: a script file (`0x02EA5220`), a log file
(`0x02EA5228`) and an input-replay file (`0x02EA5230`) are all zero and have no writer. So the console
object at `+0x58` stays null, the per-frame function `+0xD18` keeps `0x00793E8C`, and the input
recorder (slot 30) and replay (slot 29) are never called.

### The script commands

The script-file and input-replay options would each create a `PApplicationScriptProxy` as that
console object, and both call `0x007A0180` on it: `0x00792760` for a script file, and the run setup itself
(`0x0079F3F9`) for a replay. It registers sixteen commands through `0x007A0090`, which appends a `0x50`-byte record,
the handler at `+0x00` and a name of up to 64 characters at `+0x08`, to the proxy's array (`+0x28`,
count `+0x30`, capacity `+0x34`, grown to twice the capacity or 16).

| Command | Handler | Command | Handler |
|---|---|---|---|
| `Frames` | `0x00796490` | `ButtonDown` | `0x00795800` |
| `Timestep` | `0x00799980` | `ButtonUp` | `0x00795A00` |
| `Framerate` | `0x007963C0` | `Buttonpress` | `0x00795C00` |
| `MinFramerate` | `0x005C5230` (returns 0) | `Mousepress` | `0x00798000` |
| `RenderFrame` | `0x00798A80` | `InputSource` | `0x00797A20` |
| `Keypress` | `0x00797F60` | `Expect` | `0x005C5230` (returns 0) |
| `KeyDown` | `0x00797EE0` | `Echo` | `0x00796210` |
| `KeyUp` | `0x00797F20` | `Quit` | `0x00798A30` |

`Timestep` (`0x00799980`) reads one float with `%f` (`0x0071F970`, `vsscanf`) into the fixed step `+0x6C`,
whatever its value (`0x007999AC`).
A value of 0 or less returns to real time: it sets the offset `+0x50` to the time since engine start
(`0x02CB60E8`) less the total `+0x40`, so the total carries on from where the fixed steps left it
(`clock - [0x02CB60E8] - total`, `0x007999B3`-`0x007999CF`). The handler returns 0 (`0x007999D4`).
Because neither option is ever set, none of these commands runs.

### The update thread

The game runs on the update thread, not on the thread that pumps window messages. The thread object
is the static `0x02EACF10` (`0x007A4190`). `0x007A4250` sets its run word `+0x50` to 1 (`0x007A42A7`) and creates
the thread through `0x005CD1E0` (`0x007A42AE`) with a stack of `0x100000` bytes (`0x007A428C`), the routine
`0x007A4230`, a jump to the body `0x007A4310`, and the object as its argument (`0x007A4299`); it then sets the
object's `+0x48` to 1 and clears `+0x28` (`0x007A42B8`, `0x007A42BC`).

`0x007A4240` hands the window over: it stores it at `+0x20` and sets `+0x28` to 1 (`0x007A4240`, `0x007A4244`).
The body `0x007A4310` spins with `Sleep(0)` until `+0x28` is set, that is until the window is
handed to it, then loops while its run word `+0x50` is non-zero, calling the window's two slots:

- slot 0, `0x007A3110`: returns 9 when the quit byte `+0x69` is set; otherwise `SteamAPI_RunCallbacks`
  and the input poll `0x007A2440` on the application's input object `+0xDF8`, then returns 0 (`0x007A3140`);
- slot 1, `0x007A0340`: moves a drawing-area size parked by the window procedure into the `+0x48` queue as
  request 0 (`0x007A3BD0`, `0x007A0372`, under the lock at `+0x20`), runs the screen-mode state step
  `0x007A3FC0(+0x48, ScreenMode)` (`0x007A0395`), returns 9 on the quit byte, and otherwise jumps through the application's `+0xD18` (`0x007A03C4`). `0x00793E8C`
  there tail-jumps to slot 28, the per-frame update `0x0079C140`.
  - In the state step the current state's slots `+0x30` and `+0x38` run; a result n other than -1 leaves the
    old state, makes entry n current, logs `[Screen Mode]=======Change State %d` and enters it.

Slot 1 runs only when slot 0 returns 0 (`0x007A4340`). A non-zero result from either slot sets the
thread's byte `+0x29` (`0x007A4350`) and the loop goes on. When the run word is cleared
the thread posts `WM_CLOSE` with `wParam` 3 to the window (`0x007A436D`) and runs the game's
`0x0035E700`, which signals the two objects at `0x022CA610` and `0x022CA618` and waits for `0x022CA630` to
reach zero; the body then returns 0 (`0x007A4378`).

### The per-frame update `0x0079C140`

Inherited unchanged by `GameApplication` (slot 28 holds the same address in both vtables). Each call:

1. When a screen-mode change is pending (`+0x20`), copies the size and frame rate from the settings.
2. Time (`0x0079D920`): with a fixed step above 0 at `+0x6C` (`0x0079D92E`) the delta `+0x48` is the step
   and the total `+0x40` grows by it; otherwise the total is the performance-counter time since engine
   start (`0x02CB60E8`) less `+0x50`, and the delta is the change in the total. Both paths also store the
   total as a float at `+0xE0` (`0x0079D952`, `0x0079D988`).
3. Returns 9 when the quit byte `+0x69` is set. On the first frame (`+0x64` = 0) clears the delta and
   calls slot 9, resize (`0x0079C1F1`). Counts the frame at `+0x64`.
4. Calls slot 30 when a log stream is open, polls the input devices (`0x0079D010`, `0x0079C260`) unless a
   mode, focus or size request is pending, and calls slot 7, input (`0x0079C26B`).
5. Measures frames per second over two seconds into `+0x60`, then calls slot 4, animate (`0x0079C2D6`).
6. Handles the deferred window requests (below), calling slot 9 again after a size change
   (`0x0079C526`).
7. Calls each viewport's slot 3 (`0x0079C5FE`) with the render context, then slot 8, render
   (`0x0079C655`). When `0x01FD4A68` is clear and render returned 0, it also runs `0x00600C20` on the render
   context and the context's slot 2.

One branch of the deferred window requests (`0x0079C4B1`) clears `+0x20`, sets the bytes `+0x1E` and `+0x23` and
calls `0x00183260`, which sets byte `+0x02` of the game's render manager (`0x00189120`) when one exists.

A non-zero result from animate, resize, a viewport or render is logged (`App failed during animate`,
`resize`, `viewport render`, `render`) and returned. The game's own slots behind these calls are on
[the game application page](../Engine-Core/game-application.md).

### Deferred window requests

The window procedure `0x00798FF0` runs on the main thread and does not touch the renderer. The
inherited request slots only set a flag and store their arguments, and the per-frame update does the
work on the update thread:

| Slot | Body | Flag set | Work done by `0x0079C140` |
|---|---|---|---|
| 12 | `0x007A0B10` | `+0x20`, `+0x1E`; mode `+0xD20` | full screen or window at `+0xD24` by `+0xD28`; a failed full-screen switch logs and falls back to window mode |
| 13 | `0x0079F140` | `+0x21`; argument `+0x26` | `0x0079F0F0`: `ShowWindow` restore (9) or minimise (6) |
| 18 | `0x007A1180` | `+0x29`; size `+0x2C`, `+0x30` | resize through the device (`0x0062AAB0`) |
| 19 | `0x007A0AF0` | `+0x22`, or clears `+0x23` | re-checks the monitor's mode |
| 20 | `0x007A0FB0` | `+0x24` | `0x0079EBA0`: saves the window position into the settings |

The window procedure calls slot 14 when the new window is the foreground window (`WM_CREATE`), slot 20
on `WM_MOVE`, and slot 17 with 1 or 0 around a mouse press on the title bar or border, installing a `WH_MOUSE` hook
(`0x00798F80`) for its duration. Activation changes go to the update thread through `0x007A3BD0` on the
window's `+0x48` queue, and a new drawing-area size is parked in the window's `+0x1C` (`0x007A07C0`) for the
window's slot 1 to apply.

### Window helpers

- `0x007A0FC0` (`0x00798277`) sets the thread's interface language from the language setting `[0x01F82D20]` `+0x00`
  (`SetThreadUILanguage`): 1 `0x409`, 2 `0x40C`, 3 `0x407`, 4 `0x410`, 5 `0x40A`, 6 `0x412`, 7 `0x7C04`,
  8 `0x804`, any other `0x411`.
- `0x0079F750` is the size callback (`0x0079C558`). By ScreenMode (`+0x08` of the settings) it gives the window the style
  `0xCF0000` and the WindowSize at the saved position `+0x6C`/`+0x70` (0, windowed), only logs (1, full screen), or
  gives it `WS_POPUP` over the monitor rectangle `0x0017E220` or the screen (2), each time logging
  `[Screen Mode]onSizeCallBack ...` ([Screen mode and aspect](../Graphics/screen-mode-and-aspect.md)).
- `0x007A04F0` (`0x001DC78C`) queues request 1 with the WindowSize or the Resolution, by ScreenMode, on the window
  object's queue `+0x48` (`0x007A3BD0`).
- `0x00796310(full)` maximises the window (`ShowWindow` 3), or for 0 maximises and restores it (9)
  (`0x007A3CE2`, `0x007A3D41`, `0x007A4069`, `0x007A408F`).
- `0x0079B0B0` stores in `0x02EA5213` whether the game window `0x02EA5248` is the foreground window (`0x007A3E27`,
  `0x007A3EFF`, `0x007A40EC`); `0x0079EC80` brings it forward (`AttachThreadInput`, topmost and back, `SetForegroundWindow`,
  `SwitchToThisWindow`; `0x00799123`, `0x007A3F19`); `0x0079ED60(free)` clips the cursor to the drawing area, or frees it
  (`0x007A0A89`).
- `0x00798EB0` is a hook procedure the window procedure installs (`0x00799264`): on code 5 it centres any other window
  that activates on the screen `0x01F3DA1C` by `0x01F3DA20`, then passes the call on (`CallNextHookEx`, `0x02EA5258`).
- `0x0079F740` and `0x0079F9D0` set the window object's bytes `+0x1E` and `+0x1F`, and `0x007A0FA0(v)` stores `0x02EA5247`,
  from the window-event code `0x007A3A60`-`0x007A40B0`; `0x007A3D70(obj, i)` makes one of the three objects at `+0x00`,
  `+0x08`, `+0x10` current at `+0x30` and calls its slots `+0x10` and `+0x18` (`0x0079E614`).
- `0x007A1320` (`0x0079F0AA`, at shutdown) unlinks the input object's devices, the one at `+0x150` and the 18 at `+0x88`,
  from their listener lists.
- `0x007A37B0` is a `swscanf` (`__stdio_common_vswscanf`) for the XInput test `0x00797AD0` (`0x00797D4F`, `0x00797D8C`;
  [Controllers](../Controls-And-Input/controllers.md)); `0x0079DA10` (`0x0079E31B`) evaluates one input source against the
  devices: it reads the source's type tag `+0x10` (`0x01F44D90` to `0x01F44FD0`) and device index `+0x18`, with two
  thresholds taken with `sqrtf` and `cosf` ([Phyre input semantics](../Controls-And-Input/phyre-input-semantics.md)).

### Script and replay helpers

These serve the script-file and input-replay options, so they never run in the shipped game:

- `0x0079BDF0` runs the next command line (`0x007A08D6`): a pending `Frames` count steps down and runs `Frames` again;
  otherwise it parses `name(arguments)` (`0x0079BFD0`) and calls the handler, or logs `Unrecognised command %s(%s)`.
- `0x0079BFD0` splits a line at its parentheses (`Badly formed command %s`); `0x007A1230` skips spaces and `#` comment
  lines (`0x0079C0D0` finds the line end), `0x0079C0F0` finds the next space, and `0x0079D9A0(text, end, quote)` returns the
  text between two quote characters.
- `0x007A08F0` maps the `Buttonpress` names to pad bytes of `[+0xDF8] + 0x88`: `Square` `0x30`, `Cross` `0x31`,
  `Circle` `0x32`, `Triangle` `0x33`, `Select` `0x38`, `Start` `0x39`, `Up` `0x3C`, `Right` `0x3D`, `Down` `0x3E`,
  `Left` `0x3F`; any other name logs and returns 5.
- `0x00798AC0` is `RenderFrame`'s screenshot: it logs `PApplication::screenshot: %s`, reads the frame back under the
  render lock (`0x00615BC0`, `0x00624960`, `0x0061EE30`, `0x00616700`), swaps red and blue and writes a 24-bit BMP.
- `0x0079A120` replays one record, logged as `INPUT:...`: kind 1 sets a pad byte, kind 2 an action found by name
  (`0x00873C50`, `0x00873C40`), kind 3 runs a command; `0x0079A550` and `0x00799C90` append a 0x40-byte record, and
  `0x0079D430(file)` reads the replay file's `%d:` lines and returns the last number.

The engine's smaller helpers (threads, locks, arrays, pools and the D3D11 resource accessors) are listed with their
callers in [phyre-engine-helpers.tsv](phyre-engine-helpers.tsv).

### Close, shutdown and restart

`WM_CLOSE` carries the reason in `wParam`:

- 1 or 2: sets the quit byte `+0x69` and clears the update thread's run word (`0x007A42D0`). The game
  posts 1 through `0x0017E030` (called from `0x002280B0`).
- 4: the same through `0x0079B160`, and sets `0x02EA5245`, the restart request. The game posts 4 through
  `0x0017E050` after a display change that needs a restart ([config screen](../Menus-And-HUD/config-screen.md)).
- 3: posted by the update thread as it exits; `0x0079B190` runs the application shutdown `0x0079EDD0`
  (`0x0079B1A0`) and logs `PWindowWin32Base::onClose: An error occurred closing the window on Win32.`
  when it returns non-zero (`0x0079B1A9`-`0x0079B1B5`). It then releases the device context at its
  argument's `+0x10` (`ReleaseDC`, `0x0079B1C5`) and destroys the window `0x02EA5248` (`DestroyWindow`,
  `0x0079B1D7`), whose `WM_DESTROY` posts `WM_QUIT`.
- any other value, including 0 from the window's own close: ignored while the bytes `0x02B40E00` and `0x02CA99B0` are both set;
  otherwise quits at once in full-screen mode, and in the other modes shows an OK/Cancel box from the
  string resources and quits on OK. A Steam state check on the callback object (`0x00865510`) can take
  the first close without quitting.

The application shutdown `0x0079EDD0` stops the update thread (`0x007A42E0`), releases the viewports,
calls slot 5 (`0x0079EF47`, `exitScene`) and slot 6 (`0x0079EF75`, `exitApplication`), then tears down
the settings block, the renderer, the arenas and the input layer (`0x00799860`, `PInput::Terminate`).
To stop the thread, `0x007A42E0` clears its run word `+0x50` (`0x007A42EA`), waits for it through
`0x005CD330` (`0x007A42F9`), which calls `WaitForSingleObject` with no time limit (`0x005CD346`), calls
`0x005C5230`, which returns 0, on the thread part `+0x30` (`0x007A4301`) and clears `+0x48` (`0x007A4306`).

When the message loop ends, `0x007980A0` unregisters the Steam callbacks, calls `CoUninitialize`, runs
the module shutdown `0x005A0840` (`0x007986D5`), closes the mutex and frees the argument strings. With
`0x02EA5245` set it then brings the window forward, takes its own path from `GetModuleFileNameA` and
starts it again with `CreateProcessA` and the arguments `"-scmd" "appid" "100" -nologo`. Both paths
end in `ExitProcess(0)` (`0x0079887F`).

## Layouts

The `PApplication` part of the application object, as the framework functions above use it. The
`GameApplication` fields from `+0x1130` on are on the game application page.

PApplication  (base of GameApplication; address in `0x02EA5368`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0000` | `void*` |  | vtable `0x01CB2508` (GameApplication: `0x008C5760`) |
| `+0x0010` | `void*` |  | PProcessorProfileTimelineCpu sub-object (its vtable) |
| `+0x001E` | `u8` |  | resize pending (slot 12, run setup) |
| `+0x001F` | `u8` |  | window-style refresh pending |
| `+0x0020` | `u8` |  | screen-mode change pending (slot 12) |
| `+0x0021` | `u8` |  | focus request pending (slot 13) |
| `+0x0026` | `u8` |  | restore (1) or minimise (0) |
| `+0x0022` | `u8` |  | monitor re-check pending (slot 19) |
| `+0x0023` | `u8` |  | skip the next re-check |
| `+0x0024` | `u8` |  | window moved (slot 20) |
| `+0x0028` | `u8` |  | title-bar or border mouse press (slot 17) |
| `+0x0029` | `u8` |  | resize pending (slot 18) |
| `+0x002C` | `i32` | width |  |
| `+0x0030` | `i32` | height |  |
| `+0x003C` | `i32` |  | frame rate used for a full-screen switch |
| `+0x0040` | `f64` |  | total elapsed time |
| `+0x0048` | `f64` |  | frame delta |
| `+0x0050` | `f64` |  | time offset taken at run setup |
| `+0x0058` | `void*` |  | console object (script or replay mode only) |
| `+0x0060` | `f32` |  | frames per second, measured over two seconds |
| `+0x0064` | `u32` |  | frame counter |
| `+0x0069` | `u8` | quit |  |
| `+0x006C` | `f32` |  | fixed time step, 0 = real time |
| `+0x0090` | `f32[3]` |  | global ambient colour, shader parameter type `0x10` ('globalambientcolor'); opens the scene block `+0x090`..+`0x0E7` |
| `+0x00B0` | `void*` | texture of parameter type 0x12 | `+0x0B8` the second value of its capture record |
| `+0x00C8` | `void*` |  | texture of parameter type `0x14` |
| `+0x00D0` | `void*` | type 0x15 |  |
| `+0x00D8` | `void*` | type 0x16 |  |
| `+0x00E0` | `f32` |  | total elapsed time as a float, parameter type `0x11` ('time') |
| `+0x00E8` | `...` |  | render context |
| `+0x0D10` | `void*` |  | render-interface parameter block (`0x01F403A8`) |
| `+0x0D18` | `void*` |  | per-frame function: `0x00793E8C` (slot 28) or `0x00793E98` (slot 29) |
| `+0x0D20` | `u8` |  | full screen |
| `+0x0D24` | `i32` |  | width (default 1280) |
| `+0x0D28` | `i32` | height (default 720) |  |
| `+0x0D98` | `void*` |  | input-recording stream |
| `+0x0DB8` | `u32` |  | viewport count |
| `+0x0DC0` | `void*` | viewport array |  |
| `+0x0DE8` | `void*` |  | 96 MiB arena |
| `+0x0DF0` | `void*` | 2 MiB block |  |
| `+0x0DF8` | `void*` |  | input object |
| `+0x10D4` | `u8` |  | auto-test switch, 0 in retail: gates the map walker `0x001C2F50` and the scene verbs through `0x001C3370` |
| `+0x10D8` | `...` |  | embedded PDebugUtils (`0x58` bytes); its m_autoClear at `+0x1128` is set to 1 |

The application vtable slots the framework calls, named by the framework's own log strings where it
has them:

| Slot | Offset | Called from | Role |
|---|---|---|---|
| 1 | `+0x08` | `0x00798542` | script method registration |
| 2 | `+0x10` | `0x0079F591` | `initApplication` |
| 3 | `+0x18` | `0x0079F69A` | `initScene` |
| 4 | `+0x20` | `0x0079C2D6` | animate |
| 5 | `+0x28` | `0x0079EF47` | `exitScene` |
| 6 | `+0x30` | `0x0079EF75` | `exitApplication` |
| 7 | `+0x38` | `0x0079C26B` | input |
| 8 | `+0x40` | `0x0079C655` | render |
| 9 | `+0x48` | `0x0079C1F1`, `0x0079C526` | resize |
| 14, 17, 20 | `+0x70`, `+0x88`, `+0xA0` | the window procedure | foreground, title-bar press, move |
| 28 | `+0xE0` | `0x00793E8C` | per-frame update |
| 29, 30 | `+0xE8`, `+0xF0` | `0x00793E98`, `0x0079C23A` | input replay and recording |

`GameApplication` overrides slots 10, 15 and 16, but its overrides are referenced only by its vtable,
and no virtual call in the framework's code or in any function that loads `0x02EA5368` or calls its
getter `0x00796E20` goes through those slots.

The framework's other classes sit beside `PApplication` in `.rdata`:

| Vtable | Class | Slots |
|---|---|---:|
| `0x01CB2430` | `PInputDeviceKeyboard` | 6 |
| `0x01CB2468` | `PWindowWin32Base` | 2 |
| `0x01CB2480` | `PWindow` | 2 |
| `0x01CB2498` | `PApplicationScriptBuffer` | 1 |
| `0x01CB24A8` | `PApplicationScript` | 1 |
| `0x01CB24B8` | `PApplicationScriptProxy` | 1 |
| `0x01CB24C8` | `PInputDevicePad` | 7 |
| `0x01CB2508` | `PApplication` | 31 |
| `0x01CB2608` | `PApplicationViewport` | 5 |
| `0x01CB2638` | `PInputDevicePadDirectInput` | 7 |
| `0x01CB2678` | `PInputDevicePadXInput` | 7 |
| `0x01CB26B8` | `PInputDevicePadSteamController` | 7 |

[phyre-application-p-application-accesses.tsv](phyre-application-p-application-accesses.tsv) lists
1,076 instructions in 62 functions that read or write fields of the application object.

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PApplication` (`0x1130` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0050` | `f64` | timeOffset | time offset taken at run setup: the run setup `0x0079F150` stores the clock reading minus the start value at `0x02CB60E8` (`0x0079F1AF`) and adds the elapsed time `+0x40` after initScene (`0x0079F6CA`-`0x0079F6D4`); the time update `0x0079D920` subtracts it from each clock reading (`0x0079D96D`); 0 from the constructor `0x00792350` (`0x007923BB`); no registered member covers it (`0x00791AC0` registers the `0x1130`-byte class at `0x00791B10`) |
| `+0x0084` | `u8[1]` | bytes84 | the byte at `+0x84`, after the dword the constructor `0x00792350` clears at `+0x80` (`0x007923D4`) and before the qword it clears at `+0x88` (`0x007923DB`); no registered member covers it (`0x00791AC0` registers the `0x1130`-byte class at `0x00791B10`) |
| `+0x009C` | `u8[4]` | bytes9C | the four bytes at `+0x9C`, inside the sub-object at `+0x90` whose address the constructor `0x00792350` passes on (`0x007923E2`); no registered member covers it (`0x00791AC0` registers the `0x1130`-byte class at `0x00791B10`) |
| `+0x0D38` | `u32` | dwordD38 | zeroed by the constructor `0x00792350` together with `+0xD3C` (qword store `0x00792482`); no registered member covers it (`0x00791AC0` registers the `0x1130`-byte class at `0x00791B10`) |
| `+0x0D3C` | `u32` | settingD3C | set at start-up by `0x007980A0` from the settings object [`0x01F82D20`]: `0x001DE570` takes its `+0x20` modulo 5 and returns 1, 2, 4, 8 or 9 from the table `0x00900EE8` (`0x0079856F`); the game's `0x00186CD0` reads it through the getter `0x00796E20` (`0x00186D3C`) and stores it in `0x01DF0900` and `0x02CB8084` (`0x00186D62`, `0x00186D68`); no registered member covers it (`0x00791AC0` registers the `0x1130`-byte class at `0x00791B10`) |
| `+0x0D68` | `u32` | widthAfterInit | the width (`+0xD24`) as it stands after initScene, copied by the run setup `0x0079F150` (`0x0079F6E9`-`0x0079F6EF`); no registered member covers it (`0x00791AC0` registers the `0x1130`-byte class at `0x00791B10`) |
| `+0x0D6C` | `u32` | heightAfterInit | the height (`+0xD28`) as it stands after initScene, copied by the run setup `0x0079F150` (`0x0079F6F5`-`0x0079F6FB`); no registered member covers it (`0x00791AC0` registers the `0x1130`-byte class at `0x00791B10`) |
| `+0x10D0` | `u16` | iconId | the window icon's resource id: `0x0079B300` passes it to LoadIconA with the module handle (`0x0079B758`) and keeps the icon at `0x02EA5250`; the game-application constructor `0x0015BC40` sets it to 40101 (`0x9CA5`) through `0x007A1190`, a 4-byte store (`0x0015BC71`-`0x0015BC7D`); no registered member covers it (`0x00791AC0` registers the `0x1130`-byte class at `0x00791B10`) |
| `+0x10D5` | `u8[3]` | bytes10D5 | the bytes after the byte the constructor `0x00792350` clears at `+0x10D4` (`0x00792521`), before the qword it clears at `+0x10D8` (`0x00792528`); no registered member covers it (`0x00791AC0` registers the `0x1130`-byte class at `0x00791B10`) |

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

## State

### Window and host statics

The window procedure `0x00798FF0` and the window set-up `0x0079B300` keep the window's state in plain statics. On its
first call the procedure registers the message `PHYREMSG_HOSTHWND` (`0x01CB33E0`). A host program that sends that
message with its own window handle in `wParam` makes the game window its child (`SetParent`, `0x0079909F`), and the
procedure answers with the message `PHYREMSG_SENDHWND` (`0x01CB31E0`) and the game window's handle (`SendMessageW`,
`0x007990BC`).

The jump table at `0x007990E4` sends `WM_CREATE`, `WM_DESTROY`, `WM_MOVE`, `WM_SIZE`, `WM_ACTIVATE`,
`WM_CLOSE`, `WM_ERASEBKGND`, `WM_GETMINMAXINFO`, `WM_DISPLAYCHANGE` and the four title-bar button messages to their
own branches; the button-up messages above `0x112` are tested at `0x0079968A`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EACD24` | `u32` | 0 (zero-filled tail of `.data`) | the message number `RegisterWindowMessageW("PHYREMSG_HOSTHWND")` returns, taken by the first call that finds the word 0 | `0x00798FF0` (`0x00799043`) | `0x00798FF0` (`0x0079902C`, the zero test; `0x0079906D`, compared for equality with the message) |
| `0x02EA523E` | `u8` | 0 (zero-filled tail of `.data`) | 1 once the host message has arrived: the window is hosted | `0x00798FF0` (`0x00799081`, 1); `0x0079B300` (`0x0079B420`, 0 when `GetClientRect` on the host window fails) | `0x00798FF0` (`0x007994B4`: while it is set, `WM_ERASEBKGND` returns 1 without the default handling); `0x0079B300` (`0x0079B3F8`, `0x0079B554`: while it is set, the window takes the size of the host's drawing area from `GetClientRect`) |
| `0x02EA5238` | `u32` | 0 (zero-filled tail of `.data`) | the low 32 bits of the host message's `wParam`, the host window's handle | `0x00798FF0` (`0x00799088`) | `0x0079B300` (`0x0079B407`, sign-extended to 64 bits and passed to `GetClientRect`) |
| `0x02EA5240` | `u32` | 0 (zero-filled tail of `.data`) | the low 32 bits of the host message's `lParam` | `0x00798FF0` (`0x0079908E`) | no instruction names it |
| `0x02EA523C` | `u8` | 0 (zero-filled tail of `.data`) | 1 when ScreenMode (settings `+0x08`) is 2, borderless, at start-up | `0x007980A0` (`0x007985D4`, `sete`) | `0x0079B300` (`0x0079B3DB`, which then stores ScreenMode 2 through `0x001DF340(settings, 2, 2)` at `0x0079B3F3`; `0x0079B426` and `0x0079B5CE`, which choose the `WS_POPUP` style `0x80000000`) |
| `0x02EA523F` | `u8` | 0 (zero-filled tail of `.data`) | 1 while the window is minimised: `WM_SIZE` with `SIZE_MINIMIZED` (1) sets it and any other `WM_SIZE` clears it | `0x00798FF0` (`0x007993FD`, 1; `0x00799409`, 0) | no instruction names it |
| `0x02EA523D` | `u8` | 0 (zero-filled tail of `.data`) | 1 from a `WM_ACTIVATE` with `WA_CLICKACTIVE` (2) until the next `WM_LBUTTONUP` or `WM_RBUTTONUP`: the click that activated the window | `0x00798FF0` (`0x00799507`, 1; `0x007996B6`, 0) | `0x007A1790` (`0x007A19EF`): while it is set, the mouse poll zeroes the three button bytes `+0x1F4`-`+0x1F6` it has just filled from bit `0x80` of the device's state bytes, so the activating click does not reach the game |
| `0x01F3DA06` | `u8` | 1 (file-backed `.data`) | 1 when the framework last showed the cursor with `ShowCursor(1)`, 0 when it last hid it with `ShowCursor(0)` | `0x00798FF0` (`0x00799593`, 1: on `WM_ACTIVATE` with `WA_INACTIVE`, when the cursor was hidden); `0x007A0A80` (`0x007A0ABD`, 1, when asked to show a hidden cursor; `0x007A0ADB`, 0, when asked to hide a shown one) | no instruction names it |
| `0x02EACD30` | `u32` | 0 (zero-filled tail of `.data`) | `cbSize` of the `CURSORINFO` record `0x02EACD30`-`0x02EACD47`, set to `0x18` before each `GetCursorInfo` on it; the flags word `0x02EACD34` that call fills decides the stores to `0x01F3DA06` | `0x00798FF0` (`0x0079956A`); `0x007A0A80` (`0x007A0A95`) | `GetCursorInfo`, through the address `0x00798FF0` (`0x00799574`) and `0x007A0A80` (`0x007A0A8E`) pass |
| `0x02EA5244` | `u8` | 0 (zero-filled tail of `.data`) | 1 while a mouse button is held on the title bar or border | `0x00798FF0` (`0x007995C8`, 1, on `WM_NCLBUTTONDOWN` or `WM_NCRBUTTONDOWN`, after slot 17 with 1, and the `WH_MOUSE` hook `0x00798F80` is then installed; `0x00799617`, 0, on `WM_NCLBUTTONUP` or `WM_NCRBUTTONUP`, after slot 17 with 0, and the hook is then removed) | `0x00798FF0` (`0x007995A7`, `0x007995F8`); `0x00798F80` (`0x00798FA4`: while it is set, a `WM_LBUTTONUP` the hook sees posts `WM_NCLBUTTONUP` to the window) |
| `0x02EA5361` | `u8` | 0 (zero-filled tail of `.data`) | when set, the close confirmation stores ScreenMode 1 (`0x001DF340(settings, 2, 1)`, `0x007992CA`) and writes the settings file (`0x007992D6`) after its box closes, calling `0x0017DB40` first when the answer is OK, and then clears the byte | `0x00798FF0` (`0x007992DB`, 0) | `0x00798FF0` (`0x007992A7`) |
| `0x02EA5360` | `u8` | 0 (zero-filled tail of `.data`) | 1 after the borderless branch of the size callback has placed the window; while it is set, the next borderless placement adds `SWP_NOMOVE` (2) to the `SetWindowPos` flags `0x60` (`0x0079F96B`-`0x0079F981`) | `0x0079F750` (`0x0079F99D`, 1; `0x0079F89E`, 0, windowed; `0x0079F8C0`, 0, full screen); `0x00795DC0` (`0x00795EA9`, 0, after its own `SetWindowPos`); `0x007A03D0` (`0x007A03E0`, 0, before it queues request 5) | `0x0079F750` (`0x0079F96B`) |

The only store to `0x02EA5361` is the clear at `0x007992DB`, so the settings write on close runs only if the byte is set
from outside the executable.

### Frame-rate statics

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAC980` | `u32` | 0 (zero-filled tail of `.data`) | frames counted since the last frames-per-second measurement | `0x0079C140` (`0x0079C27E`, plus 1 after the input slot; `0x0079C2CA`, 0) | `0x0079C140` (`0x0079C276`; converted to a float as an unsigned value at `0x0079C2AD`) |
| `0x02EAC984` | `f32` | 0 (zero-filled tail of `.data`) | seconds accumulated over the same frames from the delta `+0x48`; when it exceeds 2.0 (`0x01CEBC08`), `+0x60` becomes the count divided by it, `+0x68` becomes 1 and both statics restart | `0x0079C140` (`0x0079C299`; `0x0079C2C2`, 0.0) | `0x0079C140` (`0x0079C28D`) |
| `0x02EA5378` | `u8` | 0 (zero-filled tail of `.data`) | 1 while the application's `+0xD44` (VSync, settings `+0x14`) is 0, Off; stored every frame | `0x0079C140` (`0x0079C224`, `sete`) | no instruction names it |

The `lea` of `0x02EA5370` at `0x00797942` names the 8-byte slot before it, which `0x00797910` passes to `0x008088FA` as its
output pointer (`0x0079795D`).

### The render-interface parameter block

`0x0079E520` fills the block at `0x01F403A8` from the window and from `+0xD20` of the application (`[PWindow + 0x08]`,
which `0x00792F10` sets from its second argument at `0x00792F4A`), points the application's `+0xD10` at it
(`0x0079E5DF`) and runs the run setup. The run setup passes the block to `0x006253D0` (`0x0079F492`), which reads it
through `r14`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F403A8` | `u64` | 0 (file-backed `.data`) | `+0x00`: the game window handle `0x02EA5248` | `0x0079E520` (`0x0079E567`) | `0x006253D0` (`0x00625473`, passed to `GetClientRect`; `0x006257A8`, passed to `0x00625830`) |
| `0x01F403B0` | `u32` | 1 (file-backed `.data`) | `+0x08`: the application's `+0xD3C`, the MSAA sample count `0x001DE570` returns (1, 2, 4, 8 or 9), or 1 when that is 0 | `0x0079E520` (`0x0079E59C`) | no instruction names it; `0x006253D0` does not read `+0x08` |
| `0x01F403B4` | `u8` | 0 (file-backed `.data`) | `+0x0C`: the application's `+0xD20`, 1 for full screen (ScreenMode 1) | `0x0079E520` (`0x0079E578`) | `0x006253D0` (`0x006257AE`: 0 makes the device request windowed, `sete r9b`) |
| `0x01F403B8` | `u32` | 0 (file-backed `.data`) | `+0x10`: the application's `+0xD44`, VSync (settings `+0x14`); `0x006253D0` turns 0, 1 and 2 into the word `0`, `1` and `0x101` at its `+0x1848` | `0x0079E520` (`0x0079E585`) | `0x006253D0` (`0x006254D9`) |
| `0x01F403BC` | `u32` | 1 (file-backed `.data`) | `+0x14`: the application's `+0xD4C`, the swap-chain buffer count: 2 when BackBufferCount (settings `+0x44`) is 0, otherwise 3 (`0x007985BB`-`0x007985C6`) | `0x0079E520` (`0x0079E5A9`) | `0x006253D0` (`0x006254CF`, `0x006254DD`, both stored at its `+0x184C`) |
| `0x01F403C0` | `u32` | 0 (file-backed `.data`) | `+0x18`: DeviceID (settings `+0x4C`) | `0x0079E520` (`0x0079E5C2`) | `0x006253D0` (`0x006256A9`, compared for equality with each adapter's device id) |
| `0x01F403C4` | `u32` | 0 (file-backed `.data`) | `+0x1C`: LUIDLow (settings `+0x50`) | `0x0079E520` (`0x0079E5D2`) | `0x006253D0` (`0x006256C1`, compared for equality) |
| `0x01F403C8` | `u32` | 0 (file-backed `.data`) | `+0x20`: LUIDHigh (settings `+0x54`) | `0x0079E520` (`0x0079E5B9`) | `0x006253D0` (`0x006256B5`, compared for equality) |

An adapter is chosen by `0x006253D0` only when all three of DeviceID, LUIDLow and LUIDHigh match.

`0x006253D0` also prepares a multimedia timer period: it clears the byte `0x02CF2544` (`0x0062542A`) and
keeps the minimum period `timeGetDevCaps` reports in `0x02CF2540`, or -1 when the call fails
(`0x00625463`).

The render thread's block `0x19` arm `0x006234A0` ([screen
fades](../Graphics/screen-fades.md)) begins it on one path with
`timeBeginPeriod([0x02CF2540])` while `0x02CF2544` is 0, setting the byte to 1 when the call succeeds
(`0x006236B1`-`0x006236D3`), and on the other ends it with `timeEndPeriod`, clearing the byte
(`0x0062380A`-`0x00623831`). `0x0062B5A0` ends a period still begun (`0x0062B781`-`0x0062B790`).

### Message-pump callbacks

`0x007980A0` registers two callbacks after the window is created, each with the `PWindow` on its stack (`[rbp - 0x40]`)
as the argument, and clears both after the message loop (`0x007986BF`, `0x007986C8`). Both callbacks, `0x00798910` and
`0x007989B0`, pump the pending window messages with `PeekMessageW`, `TranslateMessage` and `DispatchMessageW` until
no message is left or `WM_QUIT` is next, so the window keeps answering while the renderer waits.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CB6348` | `void*` | 0 (zero-filled tail of `.data`) | the callback `0x00600C20` calls while it waits: `0x007989B0` | `0x005FE190` (`0x005FE190`), from `0x007980A0` (`0x00798642`, `0x007989B0`; `0x007986C8`, 0) | `0x00600C20` (`0x00600C60`, called when not 0 on every turn of its wait at `0x005CD8B0`) |
| `0x02CB6340` | `void*` | 0 (zero-filled tail of `.data`) | that callback's argument, the `PWindow` | `0x005FE190` (`0x005FE197`), from `0x007980A0` (`0x00798642`; `0x007986C8`, 0) | `0x00600C20` (`0x00600C6C`) |
| `0x02CEDA10` | `void*` | 0 (zero-filled tail of `.data`) | the argument of the callback `0x00615BC0` calls while it waits for `0x02CC03D8` with a 1000 ms limit (`0x005CD720`); the callback, `0x00798910`, is the neighbour `0x02CEDA18` | `0x0061C540` (`0x0061C547`), from `0x007980A0` (`0x00798632`; `0x007986BF`, 0) | `0x00615BC0` (`0x00615C55`) |

### Input-replay statics

The input-replay option keeps its records in one array, which `0x0079FB10` fills from the replay file and `0x00796490`
(the `Frames` handler in the table above) replays. Like the rest of the replay path, none of it runs in the shipped
game.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EA5480` | `u32` | 0 (zero-filled tail of `.data`) | record count; bit `0x80000000` set marks a buffer the array does not own | `0x007A0540` through the address `0x0079FB10` passes (`0x0079FC78`); `0x00796490` (`0x007965CB`, `0x00796604`, 0, once every record is replayed or the quit byte is set); `0x008B7B90` (`0x008B7BC6`, 0), the exit teardown `0x00169510` registers | `0x00796490` (`0x007964A9`, `0x00796591`); `0x008B7B90` (`0x008B7B9D`) |
| `0x02EA5488` | `void*` | 0 (zero-filled tail of `.data`) | the records, `0x98` bytes each; `+0x04` is the frame number a record waits for | `0x007A0540`, as above; `0x00796490` (`0x007965C4`, `0x007965FD`, 0, after freeing it); `0x008B7B90` (`0x008B7BBF`, 0) | `0x00796490` (`0x007964E9`, `0x00796539`, `0x007965A6`, `0x007965E2`); `0x0079FB10` (`0x0079FD1F`, `0x0079FD49`, `0x0079FD9E`, `0x0079FDD0`, `0x0079FE1D`, `0x0079FE2C`, `0x0079FEEF`, `0x0079FF45`, `0x0079FFD6`); `0x008B7B90` (`0x008B7BAC`) |
| `0x02EA5364` | `u32` | 0 (zero-filled tail of `.data`) | index of the next record to replay; compared unsigned with the count and the record's frame with the frame counter `+0x64` (`0x007964CC`, `0x007964F0`) | `0x00796490` (`0x00796513`, `0x00796566`, plus 1 per replayed record; `0x0079659B`, `0x007965D7`, 0) | `0x00796490` (`0x007964C0`, `0x00796507`, `0x00796556`, `0x0079658B`) |
| `0x02EAC278` | `u8` | 0 (zero-filled tail of `.data`) | 1 once `0x0079A120` has logged its one-time warning `0x01CB2978` for a record whose kind is not 1, 2 or 3 | `0x0079A120` (`0x0079A16C`) | `0x0079A120` (`0x0079A158`) |
| `0x02EAC279` | `u8` | 0 (zero-filled tail of `.data`) | 1 once `0x0079FB10` has logged its one-time warning `0x01CB29D8`, that the input stream found no keyboard | `0x0079FB10` (`0x0079FDB8`) | `0x0079FB10` (`0x0079FDAF`) |

### Update-thread object bytes

`0x007A4190` builds the update-thread object `0x02EACF10` on first use: `0x005CC900` zeroes `+0x00`-`+0x17` and
`+0x30`-`+0x47`, and the bytes after each are cleared by hand. A guard word, `0x02EACF68`, makes the
building run once (`0x007A41BA`-`0x007A41D5`, `0x007A4214`); it registers `0x008B8620`, a jump to `0x0016D6A0`,
which returns at once, as the exit teardown (`0x007A4207`), and every call returns `0x02EACF10` (`0x007A4219`,
`0x007A421E`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EACF28` | `u8` | 0 (zero-filled tail of `.data`) | `+0x18` of the object | `0x007A4190` (`0x007A41E6`, 0) | no instruction names it; `0x007A4240`, `0x007A4250`, `0x007A42D0`, `0x007A42E0` and `0x007A4310` do not access `+0x18` of the object |
| `0x02EACF58` | `u8` | 0 (zero-filled tail of `.data`) | `+0x48` of the object, `+0x18` of its thread part `+0x30`: 1 while the update thread exists | `0x007A4190` (`0x007A41F9`, 0); `0x007A4250` (`0x007A42B8`, 1, after `0x005CD1E0` creates the thread); `0x007A42E0` (`0x007A4306`, 0, after `0x005CD330` waits for it) | no instruction names it |

### Two counts cleared at shutdown

The application shutdown `0x0079EDD0` calls `0x0064AD60`, which empties two statics, `0x02D351F0` and `0x02D35278`. For each
it runs `0x00671690(static, 0, 0, 0)`, which stores the two zeros at `+0x00` and `+0x04`, and then compares the
product of `+0x00` and `+0x04` with `+0x78`; when they differ it releases the static through `0x00674230`, if bit `0x1` of
`+0x74` is set, and stores the product.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02D35268` | `u32` | 0 (zero-filled tail of `.data`) | `+0x78` of `0x02D351F0`: the product last stored | `0x0064AD60` (`0x0064ADFB`, 0) | `0x0064AD60` (`0x0064ADD7`, compared for equality) |
| `0x02D352F0` | `u32` | 0 (zero-filled tail of `.data`) | `+0x78` of `0x02D35278`, the same | `0x0064AD60` (`0x0064AE46`, 0) | `0x0064AD60` (`0x0064AE22`, compared for equality) |

## Modding notes

- Game logic runs on the update thread. Code hooked into the window procedure runs on the main
  thread and must hand work over, as the framework does with its request flags.
- Setting `+0x69` on the object at `0x02EA5368` makes every later frame return 9 at once; quitting
  cleanly needs the update thread's run word cleared as well, which `0x0079B160` does.
- Posting `WM_CLOSE` with `wParam` 4 quits and starts the executable again.
- A fixed time step can be forced by writing `+0x6C`; the delta then no longer follows real time.

## Related

- [Game application](../Engine-Core/game-application.md): the `GameApplication` object and
  the slots it overrides.
- [Frame update order](../Engine-Core/frame-update-order.md): what the game's frame does
  inside the animate slot.
- [Phyre modules](phyre-modules.md): the engine modules `0x005A08E0` starts and `0x005A0840` stops.
- [Class hierarchy](../Engine-Core/class-hierarchy.md): the RTTI the class names come from.
- [Debug logging](../Engine-Core/debug-logging.md): the log call behind the failure messages.
- [Config screen](../Menus-And-HUD/config-screen.md): the display changes that end in a restart.
- [Keymap file](../Controls-And-Input/keymap-file.md): the `My Games` folder the start-up builds.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Core runtime: `0x001C2F50` is called by `0x0017D6E0`; those functions are documented on
  [debug menu](../Engine-Core/debug-menu.md).
- Script VM: `0x001C3370` is called by `0x003522C0`, `0x00353080`, `0x003541B0`, `0x00354B20`, `0x00354E80`, `0x00355970`,
  `0x00355F60`; those functions are documented on [event scenes](../Scripts-And-Script-Commands/event-scenes.md),
  [ebp script container](../EBP-Script-Files/ebp-script-container.md),
  [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md).
