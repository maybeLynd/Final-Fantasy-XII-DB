---
title: "Runtime services: what the game asks Windows and the C runtime for, its crash dumps, threads and debug output"
kind: "system"
category: "Compiler and C runtime"
addresses: "0x00808D78, 0x007A3770, 0x007980A0, 0x0079AD50, 0x0079B1E0, 0x008A5AD0, 0x005CCBF0, 0x005CCD00, 0x005CCAB0, 0x005CCBA0, 0x005CD1E0, 0x00863430, 0x006DF480, 0x006DF3A0, 0x005CC980, 0x005CC930, 0x00781EC0, 0x0071D9E0, 0x01F40128, 0x02EA0B88, 0x008C2120"
---

## What the player sees

When the game crashes it writes a memory dump next to itself or into its working folder and shows
a box titled `error` that reads "Fatal error encountered." (the text exists in all nine of the
executable's resource languages). Nothing else here is visible: the sound and post-effect
libraries still write diagnostic text to the Windows debug channel, which only a debug viewer
shows.

## How it works

### The import table

The executable imports 538 symbols from 30 DLLs (per-DLL counts under Shipped data). Every slot
is referenced by code. The slots are reached as follows:

| How code reaches the slot | Slots |
|---|---|
| `call [slot]`, at 3,543 call sites | 417 |
| only through `jmp [slot]`: import stubs that other code calls or stores, and tail jumps at the end of a body | 113 |
| only as a loaded value (data imports such as the `std::locale` facet ids, and `SymGetModuleBase64` / `SymFunctionTableAccess64` passed as callbacks) | 8 |

A slot with no `call` is not unused. `memset`, `memcpy` and `sqrtf` have no `call [slot]` site at
all; their stubs have 865, 637 and 570 direct `call` or `jmp` sites. `MiniDumpWriteDump` is reached
only through the stub `0x0080F2BC`, and `GetAdaptersInfo` only through `0x0078A968`.

The functions in `0x00158DE0`-`0x0015B5F0` load DLLs and resolve functions themselves, through
`LoadLibraryExW` (`0x008C2368`, 11 callers there) and `GetProcAddress` (`0x008C2130`), with buffers
from `LocalAlloc` (`0x008C2348`) and `LocalFree` (`0x008C21F8`); `GetLastError` is `0x008C20A8` and
`SHGetFolderPathW` `0x008C27E8`.

### Start-up

The C runtime entry `0x00808D78` calls `0x007A3770` (`0x00808E8A`), the game's `WinMain`. `0x007A3770`
asks `IsDebuggerPresent` (IAT `0x008C2180`) and calls the main body `0x007980A0` either way:

- with a debugger attached, directly (`0x007A377E`);
- without one, inside a `__try` whose scope covers `0x007A378D`-`0x007A3798` and whose filter is
  `0x008A5AD0` (from the function's scope table).

`0x007980A0` installs `0x0079AD50` as the unhandled-exception filter (`0x007980F0` loads it,
`0x007980F7` calls `SetUnhandledExceptionFilter`), then calls `CoInitializeEx(0, 0)` (`0x00798109`).
Its two `WideCharToMultiByte` calls are the only ones in the image.

### The frame filter's dump

`0x008A5AD0` calls `0x005CCBF0` and returns its result. `0x005CCBF0` builds the name
`<module path>.YYYYMMDD_HHMMSS.dmp` from `GetModuleFileNameA` and `GetLocalTime` and calls
`0x005CCD00(exception, name)`, which:

1. sets `SymSetOptions(0x16)` and `SymInitialize`, walks the faulting stack with `StackWalk64`,
   and prints each frame with `SymFromAddr` and `SymGetLineFromAddr64` through the log call
   `0x005CDAA0`;
2. starts a thread at `0x005CCAB0` and waits for it: that thread creates the file and calls
   `MiniDumpWriteDump` with type `0x1B27` and the exception information, then logs
   `Minidump file saved to %s`;
3. returns 1.

So the filter returns 1 (`EXCEPTION_EXECUTE_HANDLER`) and the `__try` in `WinMain` takes the
exception. Threads started through the trampoline `0x005CCBA0` get the same arrangement: the
trampoline calls `fn(arg)` from its context `+8` and `+0x10` directly under a debugger, and
otherwise inside a `__try` (`0x005CCBC3`-`0x005CCBCC`) with the same filter `0x008A5AD0`.

### The unhandled-exception filter

`0x0079AD50` runs only for what no frame handler takes. It records the thread id and the exception
pointers and, when the dword `0x01F40128` is non-zero, which it is in the image and which no
instruction writes:

1. opens the file from `0x0079B1E0`: `Dump_%d_%d_%d_%d_%d_%d.dmp` filled from `GetSystemTime`
   with year, month, day, hour + 8, minute and second, created in the working folder; when the
   create fails it shows `MessageBoxA` "Create dump file filed,Please check your remain size of
   hard disk" titled `CRASH`;
2. calls `MiniDumpWriteDump(process, pid, file, 0x1826, &info, 0, 0)` and closes the file;
3. loads string `0x7837` through `0x0019A510`, copies it into a `BSTR`, calls `ShowCursor(1)` and
   `MessageBoxW(NULL, text, L"error", MB_ICONERROR)`;
4. returns 1.

Both dump types include `MiniDumpWithFullMemory` (`0x2`): `0x1826` adds handle data, unloaded
modules, full memory information and thread information; `0x1B27` adds data segments, process
thread data and private read-write memory to those.

### Threads

`0x005CD1E0(thread, params)` is the PhyreEngine thread creator:

1. copies the start function and argument into the thread record and calls `CreateThread` with
   the trampoline `0x005CCBA0` and the requested stack size; on failure it formats the error with
   `FormatMessageA`, frees it and returns 9;
2. calls `SetThreadAffinityMask` with the requested mask;
3. names the thread for a debugger by raising exception `0x406D1388` with the requested name, or
   `PhyreEngineThread` when none is given, inside a `__try` (`0x005CD2C8`-`0x005CD2E0`) whose filter
   `0x0089BEF0` continues execution;
4. sets the priority: mode 0 gives 1, mode 2 gives -1, mode 3 the requested value; any other
   mode leaves it.

`0x00863430` creates the thread of a `crossThreadImpl` object: `CreateThread` with the start
`0x00863500` (suspended unless its fourth argument is 1), `SetThreadPriority(handle, (0x20 - p) / 2)`,
and the same naming exception under a `__try` whose filter is the constant 1. `0x00863500` calls
the object's slot 1 and passes its result to `ExitThread`.

`SetThreadAffinityMask` is called from six functions: `0x005CD1E0` and five more (`0x007A4D50`,
`0x007A5B50`, `0x007B6F70`, `0x007DE120`, `0x007DE8D0`), four of which log `[sead]` messages; `0x007DE120`
and `0x007DE8D0` create the sound library's `MockDeviceThread` and `AudioSampleThread`.

The game's own threads are made by the start-up step `0x00368ED0`, which keeps `GetCurrentThread()` at
`0x022D7FB0` with priority `0x20` (`0x00863520`), runs `0x00368F70`, `0x00368DD0` and `0x00368C80`, makes the semaphore
`0x022D7F90` (`0x00863540`) and calls `0x0035E820`:

- `0x00368C80` creates a worker thread with the start `0x00368C10` and a `0x4000`-byte stack at `0x022D3F20`.
  `0x00368C10` waits on the semaphore `[0x022D7F68 + 8 x n]` (`0x00863650`), runs the job at `0x022D7F70 + 8 x n` when
  one is set, clears it and lowers its priority to `0x24`, without end. `0x00368F30(n)`, for `0x0046DD50`, answers
  whether job n, or any job for a negative n, is pending.
- `0x00368F70` creates, when `0x003692C0` reports bit 2, a thread with the start `0x00368AE0` and stores the stub
  call `0x005C5230(0x00368AD0, ...)` at `0x022CFF18`; `0x00368AD0` releases the semaphore it is given (`0x00863800`). `0x00368AE0` waits on its semaphore and calls `0x00368B00`, whose
  calls all reach `0x005C5230`, which returns 0, so its last polling loop never ends.
- `0x003691B0(n)` releases the semaphore `[0x022CFEEC + 4 x n]` (`0x00863800`) for `0x0035E760`, `0x0035EA40` and
  `0x0035EB70`.

### The PhyreEngine lock

The PhyreEngine layer builds its lock from a Win32 event and two counters, in a `0x28`-byte record
(layout below):

- `0x005CC8A0` constructs the record by zeroing `+0x00`, `+0x08`, `+0x10`, `+0x18`, `+0x20` and `+0x24`.
  The lock at `0x01F7F510` is built this way by the C++ initialiser `0x0015BCD0`, which then registers
  `0x008A6990` with `atexit`; that teardown only jumps to the `ret 0` body `0x0016D6A0`.
- `0x005CD0A0` creates the event once: `0x005CD0E0` calls `CreateEventA` with auto-reset and an initial
  state of not signalled, stores the handle at `+0x08` and sets the byte at `+0x10`; the byte at
  `+0x00` is set when the handle is valid. `0x005CD6D0` closes the handle and clears both bytes.
- `0x005CD4F0` locks through `0x005CD450`: it counts itself at `+0x18` as a waiter, swaps the state at
  `+0x20` from 0 to 1, and waits on the event (`WaitForSingleObject`, no time-out) while the swap
  fails. It then adds 1 to `+0x24`. 61 sites take it.
- `0x005CD370` locks through `0x005CD380`, the re-entrant form: the state holds the owner's thread id
  (`GetCurrentThreadId`), and a thread that already owns the lock only adds 1 to `+0x24`. Its one
  caller, `0x0017ED20`, first creates the lock at `0x01F7F510` with `0x005CD0A0` while its byte `+0x00`
  is 0.
- `0x005CD820` releases the plain lock: it subtracts 1 from `+0x24`, swaps the state from 1 to 0, and
  signals the event through `0x005CD570` (`SetEvent`) when the waiter count is above 0.
- `0x005CD7D0` releases the re-entrant lock. Only when the state equals the caller's thread id does it
  subtract 1 from `+0x24`, and only when that reaches 0 does it swap the state from the thread id
  to 0. It signals the event through `0x005CD570` whenever the waiter count is above 0. It has 20 call
  and jump sites; `0x0017F760` tail-jumps to it for `0x01F7F510`.

A wait that returns `WAIT_ABANDONED` (`0x80`) formats the error with `FormatMessageA`, frees the
text and leaves the lock untaken.

### The debug channel

`OutputDebugStringA` (IAT `0x008C2120`) has 150 call sites in 93 functions:

- 90 functions in `0x007A4D50`-`0x007F3950` with 147 sites, each of which loads `[sead]` strings;
- two Steam callbacks: `0x0020C940` ("Received stats and achievements from Steam") and
  `0x008655A0` ("Steam overlay now active" / "inactive");
- the log routine `0x006DF480`.

`0x006DF480(format, …)` formats into the 2,048-byte static buffer `0x02EA0BA0` with
`__stdio_common_vsprintf` (options from `0x0016D670`, OR 1), then calls the function pointer at
`0x02EA0B88` with the buffer when it is non-null, else `OutputDebugStringA` (`0x006DF4FA`). It tests
no level or flag. The only write to `0x02EA0B88` is the 8-byte setter `0x006DF3A0`, which no
instruction calls and no data pointer names, so the shipped game always reaches
`OutputDebugStringA`.

`0x006DF480` has 801 direct sites (800 calls and one tail jump) in 160 functions between
`0x006DA8F0` and `0x00790160`. 791 of the sites load a literal string in the eight instructions
before the call, and 761 of those strings carry the post-effect library's tags, such as
`..\src\GPU\GPUPostEffect.cpp(%d) : Feb 18 2016 PPFX ERROR:` or `..\src\ppfx.cpp(%d) : PPFX:`.

### Timers

`0x005CC980` sets up the timer: `timeBeginPeriod(5)`, `Sleep(0)`, a `timeGetTime` sample,
`QueryPerformanceFrequency` into `0x02CB6120` with its reciprocal in `0x02CB6128`, and a
`QueryPerformanceCounter` start sample. It returns `0x17` only when both `timeBeginPeriod` and
`QueryPerformanceFrequency` fail. `0x005CC930` returns the current counter divided by the
frequency, in seconds.

### Text conversion

`MultiByteToWideChar` is not imported. `WideCharToMultiByte` (`0x008C22D8`) is called twice, both
in `0x007980A0`. The C runtime locale imports are `setlocale`, `localeconv` and
`_configthreadlocale`; the C++ library's locale and `codecvt` facets come from `MSVCP140`.

### The network-adapter query

`GetAdaptersInfo` has one user, `0x00781EC0`, which lists the adapters and formats each address as
`%02x-%02x-%02x-%02x-%02x-%02x`. Its only caller is `0x00781DD0`, called from `0x0071D9E0` at `0x0071DDAA` and
`0x0071DE8E`. Before those calls, `0x0071D9E0` compares a MAC string with `00-00-00-00-00-00`
(`0x00D9B260`) using `strncmp` for 17 characters (`0x0071DD64`-`0x0071DD6B`) and, on a match, jumps past
the adapter query (`0x0071DD73`).

This is the post-effect library's licence code: the `MacAddress` field name `0x00D9B1E4` sits among
the `..\src\UT\ppfxLicense.cpp` strings and is read by `0x0071D170`, and the licence string the
image carries (`0x00D86C00`, loaded by `0x006CBD20`) reads `FeatureId = YEBIS_D3D11, ..., MacAddress =
00-00-00-00-00-00, License = ...`.

### The C runtime routines in the image

The 56 functions in [`runtime-services-msvc-runtime-tail.tsv`](runtime-services-msvc-runtime-tail.tsv) are C and C++ runtime code linked
into the executable:

- 13 formatted-output wrappers that fetch the options word through `0x0016D670` and call one
  `__stdio_common_v*printf*` import (`0x0017D2E0` `sprintf`, `0x0019C5D0`, `0x0017D280` and others),
  plus `0x0016D670` itself;
- 3 ATL module functions: the `CAtlBaseModule` constructor `0x0080C440` and destructor `0x0080C4E8`,
  and `GetHInstanceAt` `0x0080C51C`;
- 5 call-free SSE routines: `0x00809D20`, `0x00809D80`, `0x0080A720`, `0x0080AFE0`, and `0x008098C0`, which
  jumps to `0x00809D70` or `0x00809D20` by a CPU-level global;
- 30 start-up, security-check and exception-support routines, among them `atexit` `0x00808B90`,
  `_alloca_probe` `0x00808F10`, the `/GS` handler checks `0x00808BA8`, `0x00808BC8` and `0x00808F64`,
  `__scrt_fastfail` `0x0080996C`, `capture_current_context` `0x008097D8` and `_Init_thread_abort`
  `0x0080926C`;
- 4 start-up helpers that `0x00808D78` calls: `__scrt_release_startup_lock` `0x00808AF0` (clears the
  start-up lock `0x02EAED00`), `__scrt_uninitialize_crt` `0x00808B14` (calls `0x0061ECF0` twice),
  `__scrt_get_show_window_mode` `0x00809AB4` (`GetStartupInfoW`, 10 when no show mode is given) and
  `__scrt_is_managed_app` `0x00809AF0` (tests the CLR directory in the image's own PE header).

## Layouts

The parameter block `0x005CD1E0` reads (its second argument):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | start | thread function |
| `+0x08` | `u32` | stackSize | passed to CreateThread |
| `+0x10` | `void*` | arg | argument for the thread function |
| `+0x18` | `i32` | priorityMode 0: priority 1, 2: priority -1, 3: priority from +0x2C |  |
| `+0x20` | `void*` | name | thread name for the debugger; null gives "PhyreEngineThread" |
| `+0x2C` | `i32` | priority | used with mode 3 |
| `+0x30` | `u64` | affinity | SetThreadAffinityMask argument |

The thread record it fills (its first argument), which `0x005CCBA0` receives:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | handle | from CreateThread |
| `+0x08` | `void*` | start | copied from the parameters |
| `+0x10` | `void*` | arg | copied from the parameters |

The PhyreEngine lock, `0x28` bytes (constructor `0x005CC8A0`; plain lock `0x005CD450` and release
`0x005CD820`; re-entrant lock `0x005CD380` and release `0x005CD7D0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | created | set by `0x005CD0A0` when `CreateEventA` succeeds, cleared by `0x005CD6D0` |
| `+0x08` | `void*` | event | the auto-reset event the waiters block on |
| `+0x10` | `u8` | flag | set by `0x005CD0A0`, cleared by `0x005CD6D0` |
| `+0x18` | `i32` | waiters | changed with lock-prefixed adds around each attempt |
| `+0x20` | `u32` | state | `0` free; `1` taken (plain form); the owner's thread id (re-entrant form) |
| `+0x24` | `i32` | depth | times the owner has taken it |

## Shipped data

| Fact | Value |
|---|---|
| imports | 538 symbols from 30 DLLs; data in [`runtime-services-iat-any-reference.tsv`](runtime-services-iat-any-reference.tsv) |
| `MSVCP140` / `KERNEL32` / `USER32` | 115 / 110 / 59 |
| `api-ms-win-crt-stdio` / `-math` / `-string` / `-runtime` | 45 / 45 / 31 / 24 |
| `VCRUNTIME140` / `ADVAPI32` / `steam_api64` / `dbghelp` | 21 / 10 / 9 / 9 |
| `api-ms-win-crt-heap` / `-time` / `-filesystem` / `-convert` | 8 / 7 / 7 / 4 |
| `ole32` / `WINMM` / `OLEAUT32` / `IMM32` | 6 / 4 / 3 / 3 |
| `api-ms-win-crt-utility` / `-locale` / `-environment` | 3 / 3 / 1 |
| `SHELL32` / `d3d11` / `XINPUT9_1_0` | 2 / 2 / 2 |
| `IPHLPAPI` / `D3DCOMPILER_47` / `DINPUT8` / `dwmapi` / `dxgi` | 1 each |
| busiest `call [slot]` imports (sites / functions) | `_invalid_parameter_noinfo_noreturn` 434 / 80, `LeaveCriticalSection` 310 / 126, `EnterCriticalSection` 286 / 134, `memmove` 244 / 169, `OutputDebugStringA` 150 / 93, `strstr` 61 / 20, `std::_Xlength_error` 59 / 46, `_stricmp` 56 / 15, `GetProcAddress` 51 / 16, `rand` 48 / 30 |
| fatal-error string `0x7837` | languages `0x0407`, `0x0409`, `0x040A`, `0x040C`, `0x0410`, `0x0411`, `0x0412`, `0x0804`, `0x7C04`; English "Fatal error encountered." |
| dump file names | `<module path>.YYYYMMDD_HHMMSS.dmp` (local time) and `Dump_Y_M_D_H_M_S.dmp` (UTC hour + 8, with no wrap or date carry, so the hour runs from 8 to 31) |

## Operations

- Every boot: the C runtime entry, `WinMain`, the main body; the unhandled-exception filter is
  installed before the main body's other work.
- A fault on the main thread, or on a thread started through `0x005CCBA0`, with no debugger: the
  stack is logged and a `0x1B27` dump is written by a helper thread, and the `__try` takes the
  exception.
- A fault nothing else handles: a `0x1826` dump and the fatal-error box.
- Every `0x006DF480` call: format into the static buffer and hand it to the hook or to
  `OutputDebugStringA`.

## State

| Address | What |
|---|---|
| `0x01F40128` | dword, 1 in the image: the unhandled filter's dump gate |
| `0x02EA0B88` | the debug-output hook pointer, null unless `0x006DF3A0` is called |
| `0x02EA0BA0` | the 2,048-byte format buffer of `0x006DF480` |
| `0x02CB6120`, `0x02CB6128` | the performance-counter frequency and its reciprocal |

The descriptor `0x00368ED0` hands to `0x00863540` for the semaphore `0x022D7F90` (`lea` of `0x022D7F98` at `0x00368F08`):

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022D7F9C` | `u32` | 0 (zero-filled tail of `.data`) | `+0x04`, the semaphore's maximum count, `0x10000`; one 8-byte store also sets the initial count `+0x08` (`0x022D7FA0`) to 0 | `0x00368ED0` (`0x00368EFD`) | `0x00863540` (`0x0086355E`, `+0x04`, and `0x00863565`, `+0x08`), which pass them to `0x008632E0` as the maximum and initial counts of `CreateSemaphoreW` (`0x0086331D`) |
| `0x022D7FAC` | `u32` | 0 (zero-filled tail of `.data`) | `+0x14` of the descriptor, stored 0 | `0x00368ED0` (`0x00368F0F`) | `0x00863540` reads `+0x04` and `+0x08` of the descriptor (`0x0086355E`, `0x00863565`), not `+0x14` |

### The thread-name map

`0x02EB37B8` is a static `eastl::map` from thread id to thread name. Its initialiser `0x0016A2C0` builds it empty and
registers the teardown `0x008B9110`. The thread creator `0x008636E0` (called from `0x0035E820`, `0x00368C80`, `0x00368DD0`
and `0x00368F70`) takes the new thread's id from its object's `+0x10`, finds or adds its entry with `0x001AE550`
(`0x008637BA`) and assigns the name with `0x001A5760` (`0x008637D6`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EB37C0` | `void*` | 0 (zero-filled tail of `.data`) | `+0x08`, the anchor's right link: the rightmost node, the map's last entry (nodes link right at `+0x00`, left at `+0x08`, parent at `+0x10`); the initialiser points it at the anchor `0x02EB37C0` itself | `0x0016A2C0` (`0x0016A2DA`, `0x0016A321`); `0x0016D840` (`0x0016D870`, `0x0016D878`) | `0x0016D720` (`0x0016D733`); `0x0016D840` (`0x0016D873`); `0x001AEC30` (`0x001AEC46`) |
| `0x02EB37C8` | `void*` | 0 (zero-filled tail of `.data`) | `+0x10`, the anchor's left link: the leftmost node, the map's first entry (`begin()`); the initialiser points it at the anchor | `0x0016A2C0` (`0x0016A2E1`, `0x0016A328`); `0x0016D840` (`0x0016D855`, `0x0016D86A`) | `0x0016D720` (`0x0016D737`); `0x0016D840` (`0x0016D864`); `0x001AEB00` (`0x001AEB6A`) |
| `0x02EB37D0` | `void*` | 0 (zero-filled tail of `.data`) | `+0x18`, the root node; 0 while empty | `0x0016A2C0` (`0x0016A2E8`, `0x0016A30F`); `0x0016D840` (`0x0016D85E`, `0x0016D912`, `0x0016D9E5`, `0x0016DA3D`) | `0x0016D720` (`0x0016D720`); `0x0016D840` (`0x0016D87B`, `0x0016D8CD`, `0x0016D926`, `0x0016D9A3`, `0x0016D9F8`, `0x0016DA41`, `0x0016DA4B`); `0x001AE550` (`0x001AE574`); `0x001AEB00` (`0x001AEB19`); the teardown `0x008B9110` (`0x008B9124`) |
| `0x02EB37D8` | `u8` | 0 (zero-filled tail of `.data`) | `+0x20`, the anchor's colour byte, 0 | `0x0016A2C0` (`0x0016A2EF`, `0x0016A32F`) | `0x0016D720` (`0x0016D72D`) |
| `0x02EB37E0` | `u32` | 0 (zero-filled tail of `.data`) | `+0x28`, the number of entries | `0x0016A2C0` (`0x0016A2F6`, `0x0016A336`); `0x001AEB00` (`0x001AEBC9`, `0x001AEBF8`); `0x001AEC30` (`0x001AECAD`, `0x001AED09`); `0x001AEF70` (`0x001AEFD2`) | `0x001AE550` (`0x001AE5A3`); `0x001AEB00` (`0x001AEB7D`, `0x001AEB8B`, `0x001AEB9C`, `0x001AEBC9`, `0x001AEBF8`); `0x001AEC30` (`0x001AECAD`, `0x001AECC7`, `0x001AED09`); `0x001AEF70` (`0x001AEFD2`) |

No other instruction reaches these words: no other RIP-relative, image-base-relative or disp32 reference names them,
and the map's address is taken only at `0x008637B3` and `0x008B9133`, the anchor's only at `0x0016A308`.

## Modding notes

- A debug viewer shows the sound library's and the post-effect library's messages with no change
  to the game. To capture the post-effect messages in-process, call `0x006DF3A0` with a function
  that takes the formatted string; the wrapper then calls it instead of `OutputDebugStringA`.
- A fault in a hook running on the main thread or a PhyreEngine thread produces a full-memory
  dump through `0x008A5AD0` unless a debugger is attached, so expect large dump files.
- Setting `0x01F40128` to 0 makes the unhandled filter return 1 at once, with no dump and no box.
- Do not treat an import as unused because no `call [slot]` names it: 113 slots are reached only
  by `jmp` and 8 only as loaded values.

## Related

- [Debug logging](../Engine-Core/debug-logging.md): the log call `0x005CDAA0` the stack
  walker prints through, `0x0019C5D0`, `0x0017D280` and the options word `0x0016D670`.
- [Steam integration](../Steam-And-Achievements/steam-integration.md): the Steam
  callbacks that write to the debug channel.
- [Random number generators](../Random-Numbers/random-number-generators.md): the
  process-wide `rand` stream.
- [Generated function families](generated-function-families.md): the small bodies that end in
  these imports.
- [Thunks and import stubs](thunks-and-import-stubs.md): the `jmp [slot]` stubs.
- [Exception handling](exception-handling.md): scope tables and funclets.
- [Image hardening](image-hardening.md): the security cookie the `/GS` checks compare.
