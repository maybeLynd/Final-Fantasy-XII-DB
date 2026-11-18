[Home](../../README.md) / [Steam and achievements](README.md) / Driver DLL search

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Driver DLL search: how the game finds and loads nvapi64.dll through the registry, the driver store and the system folder | system | Steam and achievements | Graphics adapters and driver libraries | The loader the game uses for NVIDIA's NVAPI library: the Windows build test, finding the NVIDIA display adapter through SetupAPI, the order it searches the adapter's service, its driver registry values, the Khronos keys, the driver store and the system folder, the trusted-folder test before an absolute path is loaded, and the helpers it builds paths and registry reads with. | 0x0015BB30, 0x0015B820, 0x0015A240, 0x0015A330, 0x0015B5F0, 0x0015A650, 0x0015A9B0, 0x0015A780, 0x0015AC50, 0x0015AE60, 0x0015B110, 0x0015B440, 0x0015B550, 0x0015B070, 0x00159CA0, 0x00159B10, 0x00159AA0, 0x00159420, 0x00159580, 0x001595F0, 0x00159F90, 0x0015A0E0, 0x01CC6BE8, 0x02EAECE0 |

## What the player sees

Nothing directly. On an NVIDIA machine this loader decides which copy of `nvapi64.dll` the game uses,
and through it whether the Config screen shows NVIDIA's GPU name and the developer line shows the GPU
temperature ([Graphics adapters and vendor libraries](graphics-adapters-and-vendor-libraries.md)).
When no copy is found or a found copy sits outside a trusted folder, the game runs without NVAPI.

## How it works

### The entry: `0x0015BB30(name, flags)`

`0x00158EC0` calls it with `nvapi64.dll` and flags 0. It clears the last error, then:

1. A name containing `\` or `/` is refused with error `0xA0` (`0x0015BBFB`) and `0x0015BB30` returns 0; a null
   or empty name skips this test (`0x0015BB56`, `0x0015BB6E`).
2. On Windows build 14308 (`0x37E4`) or later, a name starting with `nv` (case-insensitive, `0x01CC70EC`)
   goes to the driver search `0x0015B820`. A path it returns is loaded with `0x0015B550`. When it finds
   nothing and the error is anything but `0x7E`, `0x0015BB30` returns 0.
3. A found path is freed with `LocalFree` after the load (`0x0015BBF0`), and the handle from `0x0015B550` is
   returned as it is, 0 included: a found path that fails to load is not retried from the system folder
   (`0x0015BBF6`).
4. Every other case, and a search that ends with `0x7E`, loads the name from the system folder with
   `0x00159AA0`.

### The Windows build

`0x0015A240(n)` returns whether the build is at least `n`, as the unsigned test `build >= n` (`0x0015A31D`).
On first use it reads the `REG_SZ` value
`CurrentBuildNumber` under `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion` (`0x0015A0E0`) and parses
its digits into `0x02EAECE0` as `build = build * 10 + digit` (`0x0015A2DE`-`0x0015A2E9`); a value with a
non-digit leaves 0 (`0x0015A2F6`), which is read again on the next call. A failed read or a value type other
than `REG_SZ` also leaves 0 (`0x0015A299`, `0x0015A2A0`), and the read buffer is freed with `LocalFree`
(`0x0015A309`).

### Finding the NVIDIA adapter

`0x0015A330(class, &set, &device)` lists the present devices of the device-interface class `class`
(`SetupDiGetClassDevsW`, flags `0x12`), reads each interface's path, upper-cases it and stops at the
first that contains `VEN_10DE`. It returns that device and its device-information set, or false. Every
caller passes the class at `0x01CC6BE8`, `{1CA05180-A699-450A-9A0C-DE4FBE3DDD89}`, the display adapters.

`0x0015B5F0(class)` reads that device's registry property 9 and prefixes it with
`SYSTEM\CurrentControlSet\Control\Class\` (`0x0015B440`), giving the adapter's driver key.

It clears the last error first (`0x0015B637`); a null `class` sets error `0xA0` and returns 0 (`0x0015B642`).
It returns 0 when `Setupapi.dll`, `SetupDiGetDeviceRegistryPropertyW` or `SetupDiDestroyDeviceInfoList`
cannot be found or `0x0015A330` finds no NVIDIA device (`0x0015B734`), and when the property is empty or
cannot be read (`0x0015B774`, `0x0015B7B5`). It frees the property buffer (`0x0015B7CC`), destroys the
device-information set (`0x0015B7DA`) and clears the last error again when it returns a key (`0x0015B7E7`).

### The search: `0x0015B820(name)`

It refuses a name with a slash (`0xA0`), builds the driver key with `0x0015B5F0`, and adds `.dll` to a
name without an extension (`0x0015A650`; a name ending in a bare `.` loses the dot). Each later step runs
only while the last error is 0, and the first path found ends the search:

1. A file name not ending in `.dll`: the adapter's services, `0x0015A9B0`.
2. A name not ending in `.sys`: the driver key's values `UserModeDriverName`, `OpenGLDriverName` and
   `UserModeDListDriverName` (`0x0015AC50`), then the value names under `SOFTWARE\Khronos\Vulkan\Drivers`
   and `SOFTWARE\Khronos\OpenCL\Vendors` (`0x0015AE60`).
3. The driver key's `DriverSupportModules` value (`0x0015AC50`).
4. A folder plus the file name (`0x0015B440`): the driver-store folder from `0x0015B110` on build 14308 or
   later, else the system folder (`0x00159580`). The path is kept only when `GetFileAttributesW` succeeds
   and neither bit `0x10` nor `0x40` is set; a missing file resets error 2 to 0.

It returns the path with the error cleared, or 0 with error `0x7E` when nothing set another error. The
names with a `Wow` suffix are placed on the stack and never passed. `nvapi64.dll` ends in `.dll`, so it
skips step 1.

### Matching a file name

`0x001595F0(path, name)` compares the part of `path` after its last `\` with `name`, ignoring case. When
they differ, it still matches when the two base names are equal and each extension is either empty or
`.dll`.

### The adapter's services

`0x0015A9B0(name, class)` reads the NVIDIA device's registry properties 4, `0x11` and `0x12` in turn. A
`REG_SZ` value is one service name; for a `REG_MULTI_SZ` value it passes the first string on every turn
of its loop, so only the first entry is ever tried (`0x0015ABB0`). `0x0015A780(name, service)` opens the
service read-only, and returns a copy of its binary path when the service type is 1 and the path's file
name matches.

### Registry values

- `0x0015AC50(name, root, key, valueNames)` opens `key` with query access and reads each listed value
  (`0x00159F90`). A `REG_SZ` value matches as a whole; a `REG_MULTI_SZ` value is searched string by string;
  any other type sets error `0xD`. It returns a copy of the matching string.
- `0x0015AC50` returns 0 when `Advapi32.dll`, `RegOpenKeyExW` or `RegCloseKey` cannot be found (`0x0015ACD2`,
  `0x0015ACFD`, `0x0015AD29`); each is kept at `0x02EAEB38`, `0x02EAEB40` and `0x02EAEB58` once found (`0x0015ACC8`,
  `0x0015ACF3`, `0x0015AD1F`).
- It then opens the key with access 1 (`0x0015AD37`) and returns 0 when that fails (`0x0015AD51`).
- The
  list `valueNames` ends at a null entry (`0x0015AD64`). Each value is matched with `0x001595F0` (`0x0015ADC7`,
  `0x0015ADFA`). A value that cannot be read, has no match, or has another type (after the `0xD` error,
  `0x0015ADB3`) moves on to the next name; the first match whose copy succeeds ends the walk; a
  match whose copy fails (`0x00159E60` returns 0) moves on to the next name (`0x0015AE1B`-`0x0015AE1E`). The key is
  then closed (`0x0015AE29`).
- `0x0015AE60(name, root, keys)` opens each key for reading and walks its value names with `RegEnumValueW`
  until error `0x103`, returning a copy (`0x00159E60`, `0x0015B015`) of the first value name that matches.
- `0x0015AE60` returns 0 when `Advapi32.dll`, `RegOpenKeyExW`, `RegEnumValueW` or `RegCloseKey` cannot be found
  (`0x0015AEDA`, `0x0015AEFF`, `0x0015AF2B`, `0x0015AF57`); each is kept at `0x02EAEB38`, `0x02EAEB40`, `0x02EAEB48` and `0x02EAEB58`
  once found (`0x0015AED0`, `0x0015AEF5`, `0x0015AF21`, `0x0015AF4D`).
- `0x0015AE60`: the list `keys` ends at a null entry (`0x0015AF67`); each key opens with access `0x20019`
  (`0x0015AF75`), and a key that does not open is skipped (`0x0015AF8E`). An error other than `0x103` moves on
  to the next index (`0x0015B022`); the first match whose copy succeeds ends the walk over keys (`0x0015B045`), and a
  match whose copy fails (`0x00159E60` returns 0) moves on to the next index (`0x0015B01D`-`0x0015B028`).
- `0x0015AE60` frees the buffer (`0x0015B02D`) and closes each key it opened (`0x0015B03B`) after its walk; a key whose
  `0x10000`-byte buffer cannot be allocated is closed without a walk (`0x0015AFA8`).
- `0x0015AE60` reads the names into a `0x10000`-byte buffer (`0x0015AF97`), whose first `0x8000` bytes are
  cleared before each read (`0x0015AFC7`), with a length of `0x7FFF` characters (`0x0015AFBC`), and matches
  each with `0x001595F0` (`0x0015B009`).
- `0x00159F90(key, value, &type, &data)` asks for the size, allocates it with `LocalAlloc` and reads
  the value; `0x0015A0E0` wraps it with `RegOpenKeyExW` and `RegCloseKey`.
- `0x00159F90` returns the registry error code. The buffer is zero-filled (`LocalAlloc` flags `0x40`,
  `0x0015A071`); a size of 0 returns 0 with `data` left as the caller set it (`0x0015A06C`); a failed second
  read frees the buffer and sets `data` to 0 (`0x0015A0B4`, `0x0015A0BA`). When `Advapi32.dll` or
  `RegQueryValueExW` cannot be found, or the allocation fails, it returns `GetLastError` (`0x0015A082`).
- `0x0015A0E0(root, key, value, &type, &data)` opens `key` with access 1 (`0x0015A1D3`), returns the open
  error when that fails, else the result of `0x00159F90`, and closes the key (`0x0015A20E`). When
  `Advapi32.dll`, `RegOpenKeyExW` or `RegCloseKey` cannot be found it returns `GetLastError` (`0x0015A22A`).

### The driver store

`0x0015B110(class)` needs build 6000 or later (else error `0x78`). It reads the NVIDIA device's property
`{A8B865DD-2E3D-4094-AD97-E593A70C75D6}` 5 (`0x01CC6BD0`), the device's INF name, asks
`SetupGetInfDriverStoreLocationW` where that INF sits in the driver store, and returns the folder part
of the answer.

### Loading a found path

`0x0015B550(path, flags)` sends an absolute path (a leading `\` or `/`, or a drive letter, colon and
slash) to `0x0015B070`; a bare file name to `0x00159AA0`; any other relative path fails with `0x7E`.

`0x0015B070` loads the path with `LoadLibraryExW(path, 0, flags & 0xFFFFE0F7)` only when the trusted-folder
test `0x00159CA0` passes; otherwise it fails with `0xA1`. It clears the last error first (`0x0015B081`) and
checks the absolute form again: a null path or one that is not absolute fails with error `0xA0` and
returns 0 (`0x0015B0F0`). The load is a tail jump to `LoadLibraryExW` (`0x0015B0E9`).

`0x00159CA0(path)` first runs `VerifyVersionInfoW` once for Windows 6.1 or later (major 6, minor 1,
service pack 0, all greater-or-equal, kept at `0x02EAEBC0`). On an older Windows every path passes. Otherwise
it expands the path with `GetFullPathNameW` and passes it only when it starts with one of the folders
`0x24`, `0x26` or `0x2A` (the Windows folder, Program Files, Program Files (x86)), each built by
`0x00159B10` with `SHGetFolderPathW` and a trailing `\`.

A null path fails (`0x00159D72`), and so does a path whose `GetFullPathNameW` length is 0 or does not fit
the buffer it allocates (`0x00159D92`, `0x00159DC4`). The prefix test is `_wcsnicmp` over the folder's length,
so case is ignored (`0x00159E01`). A folder that `0x00159B10` cannot build ends the test with a failure
(`0x00159DE6`), so the folders after it are not tried. Each built folder and the expanded path are freed
with `LocalFree` (`0x00159E16`, `0x00159E30`, `0x00159E39`).

`0x00159B10(folder, suffix)` asks `SHGetFolderPathW(0, folder, 0, 0, buffer)` for the folder into a cleared
`0x20A`-byte stack buffer (`0x00159B4D`, `0x00159C01`) and returns a new string of the folder, `\` and
`suffix` (`0x00159C4E`-`0x00159C6E`); `0x00159CA0` gives it the empty string (`0x00159DD4`). It returns 0 for a
null `suffix` (`0x00159B3A`), when `SHGetFolderPathW` cannot be found (`0x00159BE5`) or fails (`0x00159C05`),
and when the allocation fails (`0x00159C41`).

### System-folder loads

`0x00159AA0(name, flags)` loads `0x00159420(name)`, the system folder plus `\` plus the name, with the same
flag mask. `0x00159580` returns the system folder alone. The helper libraries are loaded this way once
and kept: `Setupapi.dll` at `0x02EAEAA0`, `Shell32.dll` at `0x02EAEAE0` and `Advapi32.dll` at `0x02EAEB38`,
with each function resolved on first use.

`0x00159420` returns 0 for a null name (`0x00159445`). Otherwise it asks `GetSystemDirectoryW` for the
folder's size, allocates a zero-filled buffer for the folder, a `\` and the name (`0x00159479`), and adds
the `\` only when the folder does not already end in one (`0x00159496`). `0x00159AA0` frees that string after
the load (`0x00159AE7`); a non-null name whose string cannot be built returns 0 without a load
(`0x00159ACB`), and a null name goes on to `LoadLibraryExW` with a null path (`0x00159AC6`).

`0x00159580` clears the last error (`0x0015958C`), allocates the size `GetSystemDirectoryW` asks for, and
frees it and returns 0 when the second call returns 0 or a length larger than the buffer (`0x001595C1`,
`0x001595C5`). It returns 0 with nothing to free when the allocation fails (`0x001595B4`).

### String helpers

`0x00159520` tests a name for `\` or `/`. `0x00159760`, `0x001597E0`, `0x00159870`, `0x00159900` and `0x001599D0`
are bounded copies and appends that return `0x80070057` for a bad size and `0x8007007A` when the text
is cut; `0x00159E60` and `0x00159EF0` duplicate a string, the second at most `n` characters.

`0x0015B440(a, b)` joins two strings into a new one: a null `a` gives a copy of `b` and a null `b` a copy
of `a` (`0x0015B462`). It puts a `\` between them only when `a` is not empty and does not end in `\`, and
`b` is not empty and does not start with `\` (`0x0015B4A3`-`0x0015B4B4`). A failed copy or append frees the
new string and returns 0 (`0x0015B521`).

## Operations

| Function | Role |
|---|---|
| `0x0015BB30(name, flags)` | load a driver DLL by file name |
| `0x0015B820(name)` | find a driver file for the NVIDIA adapter |
| `0x0015A240(build)` | Windows build at least `build` |
| `0x0015A330(class, &set, &device)` | the first NVIDIA device of a class |
| `0x0015B550(path, flags)` | load a found path |
| `0x00159CA0(path)` | the trusted-folder test |
| `0x00159AA0(name, flags)` | load from the system folder |

## State

| Address | What |
|---|---|
| `0x02EAECE0` | the Windows build, 0 until read |
| `0x02EAEBC0` | the version record of the 6.1 test, `0x11C` bytes (`0x00159D1F`): the major version 6 at `0x02EAEBC4` (`0x00159D29`), the minor version 1 at `0x02EAEBC8` (`0x00159D33`) and the service pack 0 at `0x02EAECD4` (`0x00159D3D`); `0x01F41FA8` holds its result, 1 on an older Windows |
| `0x02EAEAA0`, `0x02EAEAE0`, `0x02EAEB38` | `Setupapi.dll`, `Shell32.dll`, `Advapi32.dll` |
| `0x02EAEAE8` | `SHGetFolderPathW` from `Shell32.dll`, looked up once (`0x00159BD0`) and read back on later calls (`0x00159BD9`) |

## Modding notes

- A replacement `nvapi64.dll` beside the executable is not loaded: every path the loader tries comes
  from the registry, the driver store or the system folder.
- On Windows 6.1 or later, a found path outside the Windows and Program Files folders is refused with
  `0xA1`, and the game then runs without NVAPI.

## Related

- [Graphics adapters and vendor libraries](graphics-adapters-and-vendor-libraries.md): what the game asks NVAPI for.
- [Steam integration](steam-integration.md): the game's other platform library.
