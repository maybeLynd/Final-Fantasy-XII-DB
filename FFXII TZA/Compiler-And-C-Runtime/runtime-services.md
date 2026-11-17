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

Two writers make these dumps. The one wrapped around the game's main code and its PhyreEngine threads saves
`<executable path>.<date>_<time>.dmp` beside the game; a last-resort handler, for a crash nothing else takes, saves
`Dump_<date and time>.dmp` in the working folder and then shows the box.

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

The narrow file calls, by site (`fopen` `0x008C2EF8`, `freopen` `0x008C2E48`, `CreateFileA` `0x008C2178`, `remove`
`0x008C2B18`, `rename` `0x008C2B00`):

| Site | Call | In | What it opens |
|---|---|---|---|
| `0x00187597` | `fopen`, `wb` | `0x00187550` | `/capture.tga`, the screenshot ([game application](../Engine-Core/game-application.md)) |
| `0x00187771` | `fopen`, `wb` | `0x001876E0` | the numbered `/Capture 4K/` screenshot ([game application](../Engine-Core/game-application.md)) |
| `0x001F43A9` | `fopen`, `rb` | `0x001F4340` | the archive, to read and check its index, at the path it copies to the record's `+0x78` ([bigfile archive](../Game-Files-And-Data-Tables/bigfile-archive.md)) |
| `0x002152AD` | `fopen`, `rb` | `0x00215290` | the archive, once in each reader ([bigfile archive](../Game-Files-And-Data-Tables/bigfile-archive.md)) |
| `0x002E0421` | `fopen`, `rb` | `0x002DF9A0` | the locale's file size table, read whole into `0x02EC3EE0` ([file size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md)) |
| `0x005CCAE8`, `0x0079B298` | `CreateFileA`, `GENERIC_WRITE` | `0x005CCAB0`, `0x0079B1E0` | the crash dumps (below) |
| `0x007162F0` | `fopen`, `r` | `0x007162D0` | the file its second argument's string names, its text appended to the first's (`fgets` through `0x007155E0`, `0x00716345`); a failed open empties the first |
| `0x007163CB` | `fopen`, `w` | `0x007163B0` | the file its second argument's string names, written from the first with `fputs` (`0x007163E0`); nothing calls `0x007163B0` or stores its address |
| `0x0078DA33` | `fopen`, `rb` | `0x0078D920` | a `.tfxo` effect file, in the function its messages call `CTinyEffect::CreateFromFile`; another name is read as text through `0x007162D0` (`0x0078DB29`) ([YEBIS and PPFX](../Third-Party-Libraries/yebis-ppfx-post-effects.md)) |
| `0x0081307A`, `0x0081310F` | `fopen`, `r`; `freopen`, `rb` | `0x00812FA0` | `luaL_loadfilex`'s file ([Lua runtime](../Third-Party-Libraries/lua-runtime.md)) |
| `0x0082571C`, `0x00826729` | `fopen` | `0x00825660`, `0x008266D0` | `io.open` and `opencheckfile`, on the name a chunk passes |
| `0x00826ACF`, `0x00826B31` | `remove`, `rename` | `0x00826AB0`, `0x00826B00` | `os.remove` and `os.rename`, on the names a chunk passes |
| `0x00829553` | `fopen`, `r` | `0x00829460` | `searchpath`'s readability test |

The last four rows are the embedded Lua library's; `io.open`, `opencheckfile`, `os.remove`, `os.rename` and
`searchpath` belong to its `io`, `os` and `package` libraries, which no code opens ([Lua
runtime](../Third-Party-Libraries/lua-runtime.md)).

`0x00828B80`, which `package.loadlib` (`0x008285B4`) and `loadfunc` (`0x00828CE8`, `0x00828D11`) call, loads the library its
caller names (for `package.loadlib`, the chunk's two arguments; for `loadfunc`, the file and `luaopen_` followed by
the name it loads) with `LoadLibraryExA` (`0x00828BE4`) unless `_CLIBS` already holds a handle for that path, and,
unless the symbol starts with `*`, looks it up with `GetProcAddress` (`0x00828C2C`); a failed load returns 1 and a
failed lookup 2 (`0x00828BDA`-`0x00828C44`).

`GetProcAddress` (`0x008C2130`) is called at 51 sites, each with a fixed name in `rdx` except two: `0x00862CC0` passes
ordinal 100, and `0x00828C2C` passes the symbol its caller gives, a path only the unopened `package` library reaches.
None of the fixed names is a function that opens, creates, copies, moves or deletes a file:

| Function | Sites | Looks up | Page |
|---|---|---|---|
| `0x00158DE0` | `0x00158DF3`, `0x00158E8B` | `nvapi_QueryInterface`, `nvapi_pepQueryInterface` | [graphics adapters](../Steam-And-Achievements/graphics-adapters-and-vendor-libraries.md) |
| `0x00159B10` | `0x00159BCA` | `SHGetFolderPathW` | [driver DLL search](../Steam-And-Achievements/driver-dll-search.md) |
| `0x00159F90` | `0x0015A02F` | `RegQueryValueExW` | [driver DLL search](../Steam-And-Achievements/driver-dll-search.md) |
| `0x0015A0E0`, `0x0015AC50` | `0x0015A184`, `0x0015A1B5`; `0x0015ACED`, `0x0015AD19` | `RegOpenKeyExW`, `RegCloseKey` | [driver DLL search](../Steam-And-Achievements/driver-dll-search.md) |
| `0x0015AE60` | `0x0015AEEF`, `0x0015AF1B`, `0x0015AF47` | `RegOpenKeyExW`, `RegEnumValueW`, `RegCloseKey` | [driver DLL search](../Steam-And-Achievements/driver-dll-search.md) |
| `0x0015A330` | `0x0015A3FD`, `0x0015A42D`, `0x0015A459`, `0x0015A485` | `SetupDiGetClassDevsW`, `SetupDiEnumDeviceInterfaces`, `SetupDiGetDeviceInterfaceDetailW`, `SetupDiDestroyDeviceInfoList` | [driver DLL search](../Steam-And-Achievements/driver-dll-search.md) |
| `0x0015A780` | `0x0015A81B`, `0x0015A84B`, `0x0015A877`, `0x0015A8A3` | `OpenSCManagerW`, `OpenServiceW`, `QueryServiceConfigW`, `CloseServiceHandle` | [driver DLL search](../Steam-And-Achievements/driver-dll-search.md) |
| `0x0015A9B0`, `0x0015B5F0` | `0x0015AA65`, `0x0015AA91`; `0x0015B6E0`, `0x0015B70C` | `SetupDiGetDeviceRegistryPropertyW`, `SetupDiDestroyDeviceInfoList` | [driver DLL search](../Steam-And-Achievements/driver-dll-search.md) |
| `0x0015B110` | `0x0015B227`, `0x0015B253`, `0x0015B27F` | `SetupDiGetDevicePropertyW`, `SetupGetInfDriverStoreLocationW`, `SetupDiDestroyDeviceInfoList` | [driver DLL search](../Steam-And-Achievements/driver-dll-search.md) |
| `0x0020D2F0` | 17, `0x0020D3E2`-`0x0020D574` | `ADL2_Main_Control_Create` and `_Destroy`, `ADL2_Adapter_NumberOfAdapters_Get`, `ADL2_Adapter_AdapterInfo_Get`, `ADL2_Adapter_Active_Get`, `ADL2_Overdrive_Caps` and eleven `ADL2_OverdriveN_` functions | [graphics adapters](../Steam-And-Achievements/graphics-adapters-and-vendor-libraries.md) |
| `0x0079E700` | `0x0079E82B`, `0x0079E846`, `0x0079E861` | `OpenDesktopA`, `CloseDesktop`, `SwitchDesktop` | [lazy statics](lazy-statics-and-one-time-init.md) |
| `0x00809124` | `0x0080916A`, `0x0080917D`, `0x00809190` | `InitializeConditionVariable`, `SleepConditionVariableCS`, `WakeAllConditionVariable` | [lazy statics](lazy-statics-and-one-time-init.md) |
| `0x00828B80` | `0x00828C2C` | the symbol its caller passes (`rdx` = `rsi`, `0x00828C26`) | [Lua runtime](../Third-Party-Libraries/lua-runtime.md) |
| `0x00862C70` | `0x00862CC0` | ordinal 100 of `xinput1_3.dll` (`edx` = `0x64`, `0x00862CBB`) | [controllers](../Controls-And-Input/controllers.md) |

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
3. in that thread, opens the name at `+0x10` of the thread's argument block with
   `CreateFileA(name, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0x80, NULL)` (`0x005CCAE8`); a failed create
   ends the thread with 0, with no dump and no log line (`0x005CCAF7`);
4. otherwise passes the argument block itself as the exception information (`0x005CCB32`), closes the file,
   logs the line through `0x005CDAA0` with level 2 whether or not the dump succeeded (`0x005CCB59`), and ends
   the thread with 1 when `MiniDumpWriteDump` succeeded, else 0 (`0x005CCB6F`);
5. returns 1.

`0x005CCBF0` returns the result of `0x005CCD00` unchanged: after the call (`0x005CCCD3`) only the cookie check
`0x00808C40` runs, which leaves `rax` alone. It reads the path with `GetModuleFileNameA(NULL, path, 260)`
(`0x005CCC51`) and `0x0019C5D0` formats the name into a second 260-byte buffer with
`%s.%04u%02u%02u_%02u%02u%02u.dmp` (`0x005CCCC3`); `0x00861EC0` zeroes both buffers first (`0x005CCC3F`,
`0x005CCC67`).

So the filter returns 1 (`EXCEPTION_EXECUTE_HANDLER`) and the `__try` in `WinMain` takes the
exception. Threads started through the trampoline `0x005CCBA0` get the same arrangement: the
trampoline calls `fn(arg)` from its context `+8` and `+0x10` directly under a debugger, and
otherwise inside a `__try` (`0x005CCBC3`-`0x005CCBCC`) with the same filter `0x008A5AD0`.

The trampoline returns the result of `fn(arg)` as the thread's exit code on both arms (`0x005CCBBF`,
`0x005CCBC6`, `0x005CCBE2`). When the filter takes a fault, the `__except` block at `0x005CCBCE` calls `0x00861ECC`
(`_CxxThrowException`) with two null arguments (`0x005CCBD2`).

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

The record `0x0079AD50` fills is `{thread id, exception pointers, 1}` (`0x0079AD66`-`0x0079AD72`), with the
thread id from `GetCurrentThreadId` (`0x0079AD59`). A zero `0x01F40128` returns 1 with no dump and no box
(`0x0079AD77`). The pid it passes is `GetProcessId(GetCurrentProcess())` (`0x0079AD98`).

`0x0079B1E0` builds the name with `0x0017D2E0` from the format `%s_%d_%d_%d_%d_%d_%d.dmp` and the string `Dump`
(`0x0079B270`), and opens it with `CreateFileA(name, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL)`
(`0x0079B298`). On failure it calls `ShowCursor(1)` before the box (`0x0079B2AA`) and returns the invalid handle
-1 (`0x0079B2C9`). `0x0079AD50` does not test the handle: it still calls `MiniDumpWriteDump` and `CloseHandle`
with it (`0x0079ADCA`, `0x0079ADD2`) and goes on to the message box.

Before the message `0x0079AD50` calls `SysFreeString(NULL)` (`0x0079ADDA`). It builds the `BSTR` with
`SysAllocStringLen` from the characters after the first word of the string `0x0019A510` returns, with that
word as the length; a null string leaves the box text null (`0x0079ADF4`-`0x0079AE06`). The `BSTR` is freed
with `SysFreeString` after the box (`0x0079AE2F`).

Both dump types include `MiniDumpWithFullMemory` (`0x2`): `0x1826` adds handle data, unloaded
modules, full memory information and thread information; `0x1B27` adds data segments, process
thread data and private read-write memory to those.

### Threads

`0x005CD1E0(thread, params)` is the PhyreEngine thread creator:

1. copies the start function and argument into the thread record and calls `CreateThread` with
   the trampoline `0x005CCBA0` and the requested stack size; on failure it formats the error with
   `FormatMessageA`, frees it and returns 9;
   - the record goes to the thread as its parameter, the creation flags are 0 and the handle lands in the
     record's `+0x00` (`0x005CD201`-`0x005CD22E`);
   - a null handle is the failure: `FormatMessageA` gets the flags `0x1300` and the `GetLastError` code
     (`0x005CD236`-`0x005CD262`), `LocalFree` runs only when it made a text (`0x005CD268`, `0x005CD274`), and 9 is
     returned (`0x005CD27A`);
2. calls `SetThreadAffinityMask` with the requested mask;
3. names the thread for a debugger by raising exception `0x406D1388` with the requested name, or
   `PhyreEngineThread` when no name is given, inside a `__try` (`0x005CD2C8`-`0x005CD2E0`) whose filter
   `0x0089BEF0` continues execution; the exception carries the new thread's id, and no exception is
   raised when `CreateThread` reported the id 0 (`0x005CD2A8`-`0x005CD2B1`);
4. sets the priority: mode 0 gives 1, mode 2 gives -1, mode 3 the requested value; any other
   mode leaves it. It then returns 0 (`0x005CD319`).

`0x00863430` creates the thread of a `crossThreadImpl` object: `CreateThread` with the start
`0x00863500` (suspended unless its fourth argument is 1), `SetThreadPriority(handle, (0x20 - p) / 2)`,
and the same naming exception under a `__try` whose filter is the constant 1. `0x00863500` calls
the object's slot 1 and passes its result to `ExitThread`.

`0x00863430` returns at once when the handle at object `+0x08` is non-null and the byte at `+0x14` is 0
(`0x0086344B`-`0x00863456`). Otherwise it clears `+0x14` (`0x0086345C`) and calls
`CreateThread(NULL, stackSize, 0x00863500, object, flags, object + 0x10)`, with the stack size from its second
argument and flags 4 or 0 (`0x0086348B`). It stores the handle at `+0x08` (`0x00863494`) and uses it without a
test.

The priority `(0x20 - p) / 2` rounds toward zero (`0x0086349F`-`0x008634A2`). The naming record is
`{0x1000, name, [object + 0x10], 0}`, with the name from its sixth argument (`0x008634B4`), raised with
`RaiseException(0x406D1388, 0, 3, record)` (`0x008634AC`-`0x008634DC`).

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
- `0x00368F70` creates, when `0x003692C0` reports bit `0x4`, a thread with the start `0x00368AE0` and stores the stub
  call `0x005C5230(0x00368AD0, ...)` at `0x022CFF18`; `0x00368AD0` releases the semaphore it is given (`0x00863800`).
  `0x00368AE0` waits on its semaphore and calls `0x00368B00`, whose calls all reach `0x005C5230`, which returns 0, so its
  last polling loop never ends.
- `0x003691B0(n)` releases the semaphore `[0x022CFEEC + 4 x n]` (`0x00863800`) for `0x0035E760`, `0x0035EA40` and
  `0x0035EB70`.

`0x00368C80`, after it creates the worker, and `0x00369080`, which `0x00369170` calls (`0x00369174`) before it waits on the
semaphore `0x022D7F90`, both take a worker index from `0x022D7FB4` and store 0 there. When the index they took is not 0,
they wait for the job word `0x022D7F70`, give that worker's thread (`0x022CFEF4 + 4 x n`) priority `0x24` and worker 0's
thread priority `0x22` (`0x00863520`). Every store that names `0x022D7FB4` writes 0, so the index they take is 0 and
both skip that step.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022D7F28` | `void*` | 0 (zero-filled tail of `.data`) | the worker's thread descriptor `0x022D7F20` `+0x08`: the start `0x00368C10` | `0x00368C80` (`0x00368CE4`) | `0x008636E0` (`0x0086376B`) |
| `0x022D7F30` | `void*` | 0 (zero-filled tail of `.data`) | descriptor `+0x10`: the stack buffer `0x022D3F20` | `0x00368C80` (`0x00368CFB`) | only the store names it; `0x008636E0` does not read `+0x10` |
| `0x022D7F38` | `u32` | 0 (zero-filled tail of `.data`) | descriptor `+0x18`: the stack size `0x4000` | `0x00368C80` (`0x00368CDA`) | `0x008636E0` (`0x00863789`), passed to `0x00863430` |
| `0x022D7F40` | `void*` | 0 (zero-filled tail of `.data`) | descriptor `+0x20`: `0x02EAF6D0` | `0x00368C80` (`0x00368D1B`) | only the store names it; `0x008636E0` does not read `+0x20` |
| `0x022D7F48` | `u32` | 0 (zero-filled tail of `.data`) | descriptor `+0x28`: `0x24` | `0x00368C80` (`0x00368D0E`) | `0x008636E0` (`0x00863781`), passed to `0x00863430` with the stack size |
| `0x022D7F54` | `u32` | 0 (zero-filled tail of `.data`) | descriptor `+0x34`: 0 | `0x00368C80` (`0x00368CF5`) | only the store names it; `0x008636E0` does not read `+0x34` |
| `0x022D7F7C` | `u32` | 0 (zero-filled tail of `.data`) | the worker semaphore's descriptor `0x022D7F78` `+0x04`: the maximum count `0x10000`, stored as one qword with `+0x08`, the initial count 0 | `0x00368C80` (`0x00368C9B`) | `0x00863540` (`0x0086355E`, `0x00863565`), for `CreateSemaphoreW` (`0x008632E0`) |
| `0x022D7F8C` | `u32` | 0 (zero-filled tail of `.data`) | semaphore descriptor `+0x14`: 0 | `0x00368C80` (`0x00368CBA`) | only the store names it; `0x00863540` reads `+0x04` and `+0x08` only |
| `0x022D7FB9` | `u8` | 0 (zero-filled tail of `.data`) | the worker's thread argument: cleared, and its address passed to `0x008636E0` and `0x00863610` | `0x00368C80` (`0x00368D22`) | its address only (`0x00368D2E`, `0x00368D49`) |
| `0x022D7FB4` | `i32` | 0 (zero-filled tail of `.data`) | the worker whose thread priority the next hand-over resets; 0 throughout | `0x00368C80`, 0 (`0x00368CAD`, `0x00368D65`, `0x00368D7B`); `0x00369080`, 0 (`0x0036908D`, `0x003690A8`) | `0x00368C80` (`0x00368D58`, `0x00368D98`); `0x00369080` (`0x00369084`, `0x003690C5`); each sign-extends it |

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
`OutputDebugStringA`. On both paths it returns the formatter's result, or -1 when that result is
negative (`0x006DF4D2`-`0x006DF4E0`, `0x006DF4F1`, `0x006DF500`).

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

`0x005CC980` keeps whether `timeBeginPeriod` returned 0 in the byte `0x02CB60F0` (`0x005CC991`), the `timeGetTime`
sample in `0x02CB60F4` (`0x005CC9B8`), and whether `QueryPerformanceFrequency` returned 1 in the byte `0x02CB60F1`
(`0x005CC9ED`); the return value tests those two bytes (`0x005CCA06`, `0x005CCA8D`). It sets `0x02CB6120` and
`0x02CB6118` to 1 before the two queries (`0x005CC9AD`, `0x005CC9BE`), so a failed frequency query leaves a
frequency of 1. The reciprocal is `1.0 / frequency` (`0x005CC9F4`), and the counter sample goes to `0x02CB6118`
(`0x005CCA00`).

From that sample it stores the start time in seconds, `counter * reciprocal`, in the double `0x02CB6108`
(`0x005CCA24`), the dword `(int64)(seconds * 1000.0 / 2^32)` in `0x02CB60F8` (`0x005CCA2C`-`0x005CCA44`), and the
double `0x02CB60F8 * 2^32 + sample` in `0x02CB6100`, with the `timeGetTime` sample (`0x005CCA4C`-`0x005CCA68`). It
stores `0.0` in the 8-byte slots `0x02CB6110`, `0x02CB6130` and `0x02CB6138` (`0x005CCA73`-`0x005CCA83`).

`0x005CC930` reads `QueryPerformanceCounter` into a local and returns `counter / frequency` as a double, both
converted as unsigned 64-bit values, with the frequency from `0x02CB6120` (`0x005CC939`-`0x005CC975`).

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

The 58 functions in [`runtime-services-msvc-runtime-tail.tsv`](runtime-services-msvc-runtime-tail.tsv) are C and C++ runtime code linked
into the executable:

- 13 formatted-output wrappers that fetch the options word through `0x0016D670` and call one
  `__stdio_common_v*printf*` import (`0x0017D2E0` `sprintf`, `0x0019C5D0`, `0x0017D280` and others),
  plus `0x0016D670` itself;
- 3 ATL module functions: the `CAtlBaseModule` constructor `0x0080C440` and destructor `0x0080C4E8`, and
  `GetHInstanceAt` `0x0080C51C`, which work on the one module object `0x02EAF320` (`0x60` bytes, in the
  zero-filled tail of `.data`):
  - entry `0x008C31E8` of the C++ initialiser table runs `0x0016A29C`, which constructs it (`0x0016A2A7`)
    and registers `0x008B9088` with `atexit` (`0x0016A2AC`-`0x0016A2B7`), and at exit `0x008B9088` runs the
    destructor on it (`0x008B908F`);
  - the constructor stores the version GUID pointer `0x01CC7308`, and the string lookup `0x0019A510`
    passes the object to `GetHInstanceAt` (`0x0019A528`, `0x0019A576`);
- 7 call-free SSE routines: `0x00809D20`, `0x00809D70`, `0x00809D80`, `0x0080A000`, `0x0080A720`, `0x0080AFE0`, and
  `0x008098C0`, which jumps to `0x00809D70` or `0x00809D20` by a CPU-level global;
- 30 start-up, security-check and exception-support routines, among them `atexit` `0x00808B90`,
  `_alloca_probe` `0x00808F10`, the `/GS` handler checks `0x00808BA8`, `0x00808BC8` and `0x00808F64`,
  `__scrt_fastfail` `0x0080996C`, `capture_current_context` `0x008097D8` and `_Init_thread_abort`
  `0x0080926C`;
- 4 start-up helpers that `0x00808D78` calls: `__scrt_release_startup_lock` `0x00808AF0` (clears the
  start-up lock `0x02EAED00`), `__scrt_uninitialize_crt` `0x00808B14` (calls `0x0061ECF0` twice),
  `__scrt_get_show_window_mode` `0x00809AB4` (`GetStartupInfoW`, 10 when no show mode is given) and
  `__scrt_is_managed_app` `0x00809AF0` (tests the CLR directory in the image's own PE header).

### Columns of runtime-services-msvc-runtime-tail.tsv

One row per function, 58 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the function's entry address, from `0x0016D670` to `0x008629C0`; the list above groups the 58 |

## Layouts

The parameter block `0x005CD1E0` reads (its second argument):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | start | thread function |
| `+0x08` | `u32` | stackSize | passed to CreateThread |
| `+0x10` | `void*` | arg | argument for the thread function |
| `+0x18` | `i32` | priorityMode | 0: priority 1, 2: priority -1, 3: priority from `+0x2C` |
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

### Columns of runtime-services-iat-any-reference.tsv

One row per import slot, 538 rows. The references are every instruction in `.text` with a 4-byte displacement
that lands on the slot.

| Column | Holds |
|---|---|
| `code_refs` | how many instructions in `.text` name the slot through a RIP-relative memory operand, of any kind: 1 to 434 (`_invalid_parameter_noinfo_noreturn`); every slot has at least one |
| `by_mnemonic` | the same instructions counted by mnemonic, as `mnemonic:count` pairs in alphabetical order separated by commas, for example `call:310,jmp:11` for `LeaveCriticalSection`. Four mnemonics occur: `call` on 417 rows, `jmp` on 163, `mov` on 11 and `bnd call` on 2 |

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
