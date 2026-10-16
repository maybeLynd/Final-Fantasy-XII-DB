---
title: "Driver DLL search: how the game finds and loads nvapi64.dll through the registry, the driver store and the system folder"
kind: "system"
category: "Steam and achievements"
addresses: "0015BB30, 0015B820, 0015A240, 0015A330, 0015B5F0, 0015A650, 0015A9B0, 0015A780, 0015AC50, 0015AE60, 0015B110, 0015B440, 0015B550, 0015B070, 00159CA0, 00159B10, 00159AA0, 00159420, 00159580, 001595F0, 00159F90, 0015A0E0, 01CC6BE8, 02EAECE0"
---

## What the player sees

Nothing directly. On an NVIDIA machine this loader decides which copy of `nvapi64.dll` the game uses,
and through it whether the Config screen shows NVIDIA's GPU name and the developer line shows the GPU
temperature ([Graphics adapters and vendor libraries](graphics-adapters-and-vendor-libraries.md)).
When no copy is found or a found copy sits outside a trusted folder, the game runs without NVAPI.

## How it works

### The entry: `0015BB30(name, flags)`

`00158EC0` calls it with `nvapi64.dll` and flags 0. It clears the last error, then:

1. A name containing `\` or `/` is refused with error `A0`<sub>h</sub>.
2. On Windows build 14308 (`37E4`<sub>h</sub>) or later, a name starting with `nv` (case-insensitive, `01CC70EC`)
   goes to the driver search `0015B820`. A path it returns is loaded with `0015B550`. When it finds
   nothing and the error is anything but `7E`<sub>h</sub>, `0015BB30` returns 0.
3. Every other case, and a search that ends with `7E`<sub>h</sub>, loads the name from the system folder with
   `00159AA0`.

### The Windows build

`0015A240(n)` returns whether the build is at least `n`. On first use it reads the `REG_SZ` value
`CurrentBuildNumber` under `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion` (`0015A0E0`) and parses
its digits into `02EAECE0`; a value with a non-digit leaves 0, which is read again on the next call.

### Finding the NVIDIA adapter

`0015A330(class, &set, &device)` lists the present devices of the device-interface class `class`
(`SetupDiGetClassDevsW`, flags `12`<sub>h</sub>), reads each interface's path, upper-cases it and stops at the
first that contains `VEN_10DE`. It returns that device and its device-information set, or false. Every
caller passes the class at `01CC6BE8`, `{1CA05180-A699-450A-9A0C-DE4FBE3DDD89}`, the display adapters.

`0015B5F0(class)` reads that device's registry property 9 and prefixes it with
`SYSTEM\CurrentControlSet\Control\Class\` (`0015B440`), giving the adapter's driver key.

### The search: `0015B820(name)`

It refuses a name with a slash (`A0`<sub>h</sub>), builds the driver key with `0015B5F0`, and adds `.dll` to a
name without an extension (`0015A650`; a name ending in a bare `.` loses the dot). Each later step runs
only while the last error is 0, and the first path found ends the search:

1. A file name not ending in `.dll`: the adapter's services, `0015A9B0`.
2. A name not ending in `.sys`: the driver key's values `UserModeDriverName`, `OpenGLDriverName` and
   `UserModeDListDriverName` (`0015AC50`), then the value names under `SOFTWARE\Khronos\Vulkan\Drivers`
   and `SOFTWARE\Khronos\OpenCL\Vendors` (`0015AE60`).
3. The driver key's `DriverSupportModules` value (`0015AC50`).
4. A folder plus the file name (`0015B440`): the driver-store folder from `0015B110` on build 14308 or
   later, else the system folder (`00159580`). The path is kept only when `GetFileAttributesW` succeeds
   and neither bit `10`<sub>h</sub> nor `40`<sub>h</sub> is set; a missing file resets error 2 to 0.

It returns the path with the error cleared, or 0 with error `7E`<sub>h</sub> when nothing set another error. The
names with a `Wow` suffix are placed on the stack and never passed. `nvapi64.dll` ends in `.dll`, so it
skips step 1.

### Matching a file name

`001595F0(path, name)` compares the part of `path` after its last `\` with `name`, ignoring case. When
they differ, it still matches when the two base names are equal and each extension is either empty or
`.dll`.

### The adapter's services

`0015A9B0(name, class)` reads the NVIDIA device's registry properties 4, `11`<sub>h</sub> and `12`<sub>h</sub> in turn. A
`REG_SZ` value is one service name; for a `REG_MULTI_SZ` value it passes the first string on every turn
of its loop, so only the first entry is ever tried (`0015ABB0`). `0015A780(name, service)` opens the
service read-only, and returns a copy of its binary path when the service type is 1 and the path's file
name matches.

### Registry values

- `0015AC50(name, root, key, valueNames)` opens `key` with query access and reads each listed value
  (`00159F90`). A `REG_SZ` value matches as a whole; a `REG_MULTI_SZ` value is searched string by string;
  any other type sets error `D`<sub>h</sub>. It returns a copy of the matching string.
- `0015AE60(name, root, keys)` opens each key for reading and walks its value names with `RegEnumValueW`
  until error `103`<sub>h</sub>, returning the first value name that matches.
- `00159F90(key, value, &type, &data)` asks for the size, allocates it with `LocalAlloc` and reads
  the value; `0015A0E0` wraps it with `RegOpenKeyExW` and `RegCloseKey`.

### The driver store

`0015B110(class)` needs build 6000 or later (else error `78`<sub>h</sub>). It reads the NVIDIA device's property
`{A8B865DD-2E3D-4094-AD97-E593A70C75D6}` 5 (`01CC6BD0`), the device's INF name, asks
`SetupGetInfDriverStoreLocationW` where that INF sits in the driver store, and returns the folder part
of the answer.

### Loading a found path

`0015B550(path, flags)` sends an absolute path (a leading `\` or `/`, or a drive letter, colon and
slash) to `0015B070`; a bare file name to `00159AA0`; any other relative path fails with `7E`<sub>h</sub>.

`0015B070` loads the path with `LoadLibraryExW(path, 0, flags & FFFFE0F7h)` only when the trusted-folder
test `00159CA0` passes; otherwise it fails with `A1`<sub>h</sub>.

`00159CA0(path)` first runs `VerifyVersionInfoW` once for Windows 6.1 or later (major 6, minor 1,
service pack 0, all greater-or-equal, kept at `02EAEBC0`). On an older Windows every path passes. Otherwise
it expands the path with `GetFullPathNameW` and passes it only when it starts with one of the folders
`24`<sub>h</sub>, `26`<sub>h</sub> or `2A`<sub>h</sub> (the Windows folder, Program Files, Program Files (x86)), each built by
`00159B10` with `SHGetFolderPathW` and a trailing `\`.

### System-folder loads

`00159AA0(name, flags)` loads `00159420(name)`, the system folder plus `\` plus the name, with the same
flag mask. `00159580` returns the system folder alone. The helper libraries are loaded this way once
and kept: `Setupapi.dll` at `02EAEAA0`, `Shell32.dll` at `02EAEAE0` and `Advapi32.dll` at `02EAEB38`,
with each function resolved on first use.

### String helpers

`00159520` tests a name for `\` or `/`. `00159760`, `001597E0`, `00159870`, `00159900` and `001599D0`
are bounded copies and appends that return `80070057`<sub>h</sub> for a bad size and `8007007A`<sub>h</sub> when the text
is cut; `00159E60` and `00159EF0` duplicate a string, the second at most `n` characters.

## Operations

| Function | Role |
|---|---|
| `0015BB30(name, flags)` | load a driver DLL by file name |
| `0015B820(name)` | find a driver file for the NVIDIA adapter |
| `0015A240(build)` | Windows build at least `build` |
| `0015A330(class, &set, &device)` | the first NVIDIA device of a class |
| `0015B550(path, flags)` | load a found path |
| `00159CA0(path)` | the trusted-folder test |
| `00159AA0(name, flags)` | load from the system folder |

## State

| Address | What |
|---|---|
| `02EAECE0` | the Windows build, 0 until read |
| `02EAEBC0` | the version record of the 6.1 test; `01F41FA8` holds its result, 1 on an older Windows |
| `02EAEAA0`, `02EAEAE0`, `02EAEB38` | `Setupapi.dll`, `Shell32.dll`, `Advapi32.dll` |

## Modding notes

- A replacement `nvapi64.dll` beside the executable is not loaded: every path the loader tries comes
  from the registry, the driver store or the system folder.
- On Windows 6.1 or later, a found path outside the Windows and Program Files folders is refused with
  `A1`<sub>h</sub>, and the game then runs without NVAPI.

## Related

- [Graphics adapters and vendor libraries](graphics-adapters-and-vendor-libraries.md): what the game asks NVAPI for.
- [Steam integration](steam-integration.md): the game's other platform library.
