---
title: "Graphics adapters and vendor libraries: which GPU the game picks, the adapter list, NVAPI and AMD ADL"
kind: "system"
category: "Steam and achievements"
addresses: "0x006253D0, 0x001DD170, 0x00623C10, 0x00623CB0, 0x00624490, 0x001DC650, 0x001DC7A0, 0x00628690, 0x001DF2C0, 0x00159340, 0x00158F60, 0x00158EC0, 0x00158DE0, 0x00158FE0, 0x001590B0, 0x00159180, 0x00159270, 0x0020D2B0, 0x0020D9F0, 0x0020DA50, 0x0020DAB0, 0x0020D050, 0x0020D120, 0x0020D2F0, 0x0020DE30, 0x0020CEF0, 0x0020CF90, 0x0020D720, 0x001DC9D0, 0x001DCB90, 0x01E02580, 0x01F83460"
---

## What the player sees

On a machine with more than one GPU the game starts on the adapter saved in `GameSetting.ini`, or on
the one with the most dedicated video memory. The Config screen's Display Adapter row shows the GPU's
name followed by the monitor, such as `(DISPLAY1)`, and steps through every monitor of
every usable adapter. The Anti-Aliasing row offers only the multisample levels the GPU reports. The
game asks NVIDIA's and AMD's driver libraries for the GPU's name and temperature; without them it uses
the name Windows reports.

The two libraries are asked in turn, NVIDIA's first and then AMD's, and each finds the card by matching the device
number Direct3D reports for it; the first library that answers supplies the name or the temperature. NVIDIA's library
file itself comes only from places the registry, the driver store or the system folder give, never from beside the
game.

## How it works

### Choosing the adapter at start-up

The renderer's start-up `0x006253D0` creates a DXGI factory (`CreateDXGIFactory`, kept at context
`+0x1878`) and walks its adapters. For each adapter `i`:

1. It creates a throw-away device on it with `D3D11CreateDevice`, starting from feature level
   `0x9100`, and skips the adapter unless the level it gets is above `0xAFFF` (11.0 or higher).
2. It reads the adapter's description and counts its outputs, logging
   `%d ,%d Adapter name = %ws , Display Name = %ws`.
3. An adapter with dedicated video memory and at least one output sets bit `i` of the usable mask at
   context `+0x18B0`.
4. Among usable adapters, the first whose device id and LUID equal the window description's `+0x18`,
   `+0x1C` and `+0x20` is taken at once; until then the one with the most dedicated video memory is
   kept. The choice goes to context `+0x1880` and its index to `+0x18AC`.

`0x0079E520` fills those three fields of the window description `0x01F403A8` from settings 19 DeviceID,
20 LUIDLow and 21 LUIDHigh (`0x0079E5AF`-`0x0079E5D2`), stores its address at `[0x02EA5368] + 0xD10` and calls
`0x0079F150`, which passes it on (`0x0079E4FE`). With an adapter chosen, `0x00625830` creates the device and swap chain on it.

### The adapter list

The display object's constructor runs `0x001DD170`, which copies what the renderer found:

1. `0x00623C10` returns the adapter count, the chosen index (`+0x18AC`) and the usable mask (`+0x18B0`),
   stored at display `+0x50`, `+0x4C` and `+0x58`; `+0x48` starts equal to `+0x4C`.
2. For each adapter it allocates a `0x140`-byte `AdapterRecord`: `0x00623CB0` writes the adapter's
   description and its output count; `0x00624490` fills one `0x60`-byte output description per output.
3. A usable adapter adds its output count to `+0x54`.
4. It writes the selected record's device id and LUID back to settings 19, 20 and 21 (`0x001DF340`).

`0x00623C10` writes the chosen index and the mask first (`0x00623C23`, `0x00623C2F`), then calls the factory's
`EnumAdapters` (vtable `+0x38`) for adapter 0, 1, 2 and on, storing the count after each adapter it gets
and releasing that adapter (`0x00623C68`, `0x00623C6D`). Without a factory at `+0x1878`, or when adapter 0 is
missing, it leaves the count unwritten (`0x00623C45`, `0x00623C66`). It returns 0 on every path.

`0x00623CB0` gets adapter `i` the same way, writes its description with `GetDesc` (vtable `+0x40`,
`0x00623CF0`) and calls `EnumOutputs` (vtable `+0x38`) until it gives a null output, storing the number of
outputs it got (`0x00623D44`). It releases the adapter (`0x00623D49`) but not the outputs it counted.

`0x00624490` gets adapter `i`, reads its description into its own stack buffer (`0x006244EF`), and for each
output `k` below `n` that `EnumOutputs` returns, calls the output's `GetDesc` (vtable `+0x38`) on
`out + k * 0x60` (`0x0062452F`). It then releases the last output pointer it got, without testing it, and the
adapter (`0x0062453E`, `0x00624547`). With no factory or no adapter `i`, `0x00623CB0` and `0x00624490` write
nothing (`0x00623CD3`, `0x00623CE8`, `0x006244C4`, `0x006244DD`); both return 0 on every path.

### The Display Adapter row

Console id `0x10A` steps the monitor, display `+0x60`, through the selected adapter's outputs. Past the
last one it moves to the next usable adapter with `0x001DC650` and starts again at monitor 1; going back
from monitor 1 it moves to the previous usable adapter at its last monitor. `0x001DC650` skips adapters
whose bit in `+0x58` is clear, stores the index at `+0x48` and writes the record's device id and LUID to
settings 19-21.

`0x001DC650(display, i, back)` starts at `i % count`, with `count` at `+0x50`, or at `count - 1` when `i`
is negative (`0x001DC661`-`0x001DC671`). While the current adapter's bit in `+0x58` is clear it steps: down
with `back` set, `i - 1`, wrapping from 0 to `count - 1` (`0x001DC685`-`0x001DC68A`); up otherwise,
`(i + 1) % count` (`0x001DC690`-`0x001DC698`). The loop has no other exit, so a mask in which no adapter's
bit is set keeps it looping. It returns the index it stored at `+0x48` (`0x001DC719`).

`0x001DC7A0` stores the monitor, folding a number above the output count back to 1. When the adapter is
the one in use (`+0x48` equals `+0x4C`) and the monitor differs from `+0x64`, it rebuilds the
display-mode list (`0x001DD420`), calls `0x007A03D0`, stores setting 26 Monitor and writes the settings file
(`0x001DFD40`).

`0x001DC7A0` first stores the monitor unchanged at `+0x60` (`0x001DC7A6`). With its third argument zero it
returns there (`0x001DC7AF`); the fold, the comparison and the settings write run only when it is
non-zero. The output count is that of the record at `+0x48`, or display `+0x5C` when `+0x78` is 0
(`0x001DC7B5`, `0x001DC7CF`). The fold compares unsigned (`cmova`, `0x001DC7DF`), and the settings file is
written by a tail jump (`0x001DC81E`).

### Anti-aliasing levels from the device

After the device exists, `0x00625830` calls `0x00628690` (`0x00625E7C`). It asks the device for
`CheckMultisampleQualityLevels` (vtable `+0xF0`) on format 28 for every sample count 2-32, and for
each count that reports levels it sets one bit of the settings' MSAA mask at `[0x01F82D20] + 0x44C`
through `0x0017D9C0` → `0x001DF2B0`:

| Sample count | Bit | MSAA value |
|---:|---:|---|
| 2 | `0x2` | MSAA2X |
| 4 | `0x4` | MSAA4X |
| 8 | `0x8` | MSAA8X, and bit `0x10` CSAA16x when more than 16 quality levels |
| 16 | `0x20` | CSAA16XQ, value 5 (`0x00628714` with `0x0017D9C0(5)`; `0x001DF2B0` sets bit `1 << 5`) |

Bit `0x1` (Off) comes from the settings constructor `0x001DE050`. The Anti-Aliasing row cycles with
`0x001DF2C0`, which steps the value through 0-4 modulo 5, skipping clear bits, and stores it in setting
8 (`+0x20`). The constructor's bit `0x1` (`0x001DE075`, never cleared; the probe only adds bits) means the
skip loop always ends, on Off at worst. Value 5 can be set in the mask but is never reached, and nothing
sets bit `0x40`.

### Loading NVAPI

`0x006253D0` calls `0x00159340` before it creates the factory. `0x00159340` takes the critical section
`0x02EAEA70` and calls `0x00158F60(0)`; on success it raises the reference count `0x02EAE138`. A non-zero
result is logged as `NvAPI_Initialize() failed = 0x%x` and stored as 0 in `0x02CED884` (1 on success);
nothing reads `0x02CED884`.

On its first call `0x00159340` stores the vtable `0x01CC6B60` at `0x02EAEA68`, initialises the critical section
and registers `0x008B9040`, which deletes it, with `atexit` (`0x00159377`, `0x00159384`); bit `0x1` of
`0x02EAEA98` marks this done. Around the call it raises and lowers the in-call counter `0x02EAE128`
(`0x00159396`, `0x001593BA`). The new reference count is `old + 1`, with `old` read before the call
(`0x0015939E`, `0x001593B4`), so the first load, which sets it to 1 in `0x00158EC0`, still leaves 1. It leaves
the critical section and returns the result of `0x00158F60` (`0x001593FD`, `0x00159408`).

- `0x00158F60(i)` waits while byte `0x02EAE120 + i` is set, sleeping 100 ms up to ten times, and then gives
  up with -1. With the byte clear it loads library `i` if its handle at `0x02EAE100 + 8i` is 0. Nothing
  writes `0x02EAE120`, so it never waits. It returns 0 when the handle is already set (`0x00158FC5`) and
  otherwise the result of `0x00158EC0(i)` (`0x00158FB9`).
- `0x00158EC0(i)` loads `nvapi64.dll` for `i` = 0 and `nvpowerapi.dll` for 1 through the driver-DLL
  search `0x0015BB30` ([Driver DLL search](driver-dll-search.md)), returns -2 when that fails, and frees
  the library when `0x00158DE0` fails; on success it stores the handle at `0x02EAE100 + 8i` and sets the count
  `0x02EAE138 + 4i` to 1 (`0x00158F31`, `0x00158F39`). Every caller passes 0.
- With the handle at `0x02EAE100 + 8i` already set, `0x00158EC0` returns 0 without loading (`0x00158EEA`). It
  hands `i` on to `0x00158DE0` (`0x00158F19`); when that returns non-zero it frees the library with
  `FreeLibrary` (`0x00158F27`) and returns that value, and on success it returns 0 (`0x00158F44`).
- `0x00158DE0` resolves `nvapi_QueryInterface`, asks it for interface `0x0150E828` and calls it; a
  non-zero result clears the query function and is returned. It then asks for `0x33C7358C` and
  `0x593E8644` as a pre-call and post-call hook pair, keeping them only when the first exists and
  the second does not, and clears the `0x918`-byte function cache at `0x02EAE150`.
- `0x00158DE0` returns -1 when `GetProcAddress` finds no `nvapi_QueryInterface` (`0x00158E03`, `0x00158E18`),
  and also when the query gives no interface `0x0150E828`, after clearing the query function
  (`0x00158E0F`, `0x00158E11`). After clearing the cache it returns 0 (`0x00158EB5`).
- For library 1, `0x00158DE0` instead resolves `nvapi_pepQueryInterface` into `0x02EAE0E8`, a path no
  caller takes. It returns -1 when that is missing (`0x00158E9B`) and otherwise clears the cache and returns
  0. A library index other than 0 and 1 resolves no function and goes straight to clearing the cache
  and returning 0 (`0x00158E82`).

The hook pair is kept only when the pre-call hook exists and the post-call hook does not
(`0x00158E57`-`0x00158E76`). So the post-call slot is 0 whenever the pair is kept, and the wrappers' post-call step
never runs. Each wrapper tests each slot before it calls through it:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAE0F0` | `void*` | 0 (zero-filled tail of `.data`) | the NVAPI pre-call hook, interface `0x33C7358C` | `0x00158DE0`, the query's answer (`0x00158E4A`) and 0 when the pair is dropped (`0x00158E6F`) | `0x00158DE0` (`0x00158E57`); the wrappers `0x00158FE0` (`0x00159041`), `0x001590B0` (`0x00159111`), `0x00159180` (`0x001591F2`) and `0x00159270` (`0x001592D8`), which call it with the interface id and a cookie slot |
| `0x02EAE0F8` | `void*` | 0 (zero-filled tail of `.data`) | the NVAPI post-call hook, interface `0x593E8644`; 0 whenever the pair is kept | `0x00158DE0`, the query's answer (`0x00158E5F`) and 0 when the pair is dropped (`0x00158E76`) | the wrappers `0x00158FE0` (`0x0015906C`), `0x001590B0` (`0x0015913C`), `0x00159180` (`0x0015922D`) and `0x00159270` (`0x00159305`), which would pass it the id, the cookie and the result |

### Calling NVAPI

The four wrappers share one shape: they raise the in-call counter `0x02EAE128` (locked add), call
`0x00158F60(0)`, resolve their function once through the query function into a cache slot, call the
pre-call hook, the function and the post-call hook, and lower the counter. A function that cannot be
resolved returns -3.

A non-zero result of `0x00158F60(0)` is returned at once, after lowering the counter, without resolving or
calling anything (`0x00159001`, `0x001590D1`, `0x001591B2`, `0x00159298`). Otherwise each wrapper returns the
function's result. A hook whose slot is 0 is skipped, and the pre-call hook gets a cookie slot that is set
to 0 first (`0x00159048`, `0x00159118`, `0x001591F9`, `0x001592DF`).

| Wrapper | Interface id | Cache slot | What the game reads |
|---|---|---|---|
| `0x00158FE0(handles, &count)` | `0xE5AC921F` | `0x02EAE1B0` | the GPU handles and their count |
| `0x00159180(handle, &id, &subsys, ...)` | `0x2DDFB66E` | `0x02EAE268` | PCI vendor and device in one dword, the subsystem id |
| `0x001590B0(handle, name)` | `0xCEEE8E9F` | `0x02EAE260` | the GPU name, into a 64-byte buffer |
| `0x00159270(handle, 0, settings)` | `0xE3640A56` | `0x02EAE310` | the temperature at `+0x14` of a `0x44`-byte buffer whose first dword is `0x20044` |

### Loading AMD ADL

The static initialiser `0x0015DC80` builds `AmdAdapterInfo` at `0x01F83460` with `0x0020D2F0` and registers
`0x008A7360` to tear it down. `0x0020D2F0`:

1. loads `atiadlxx.dll`, else `atiadlxy.dll`, with plain `LoadLibraryW`, and stops if neither loads;
2. resolves seventeen `ADL2_` functions into `+0x30`-`+0xB0`;
3. requires all but `ADL2_OverdriveN_PowerLimit_Get`, `_PowerLimit_Set` and `_Temperature_Get`, then
   calls `ADL2_Main_Control_Create(0x0020D7B0, 1, +0xC0)`; `0x0020D7B0` is a `malloc` adapter;
4. reads the adapter count, allocates `count × 0x624` bytes at `+0xC8` and fills them with
   `ADL2_Adapter_AdapterInfo_Get`;
5. parses each record's identifier string at `+0x08` with `0x0020DE30` into an `AdapterIds`, appends it
   to the vector at `+0x10`, then sets the count `+0x2C` and the ready byte `+0x28`.

`0x0020DE30` splits the string at each `&`, splits each part at its last `_`, and reads the value as hex
(`"0x"` prefix, `sscanf` with `%x`). The keys `PCI_VEN`, `DEV` and `SUBSYS` fill vendor, device and
subsystem; other keys are ignored.

`0x0020D720`, slot 2's body (`0x0020D010`), and the exit routine `0x008A7360` call
`ADL2_Main_Control_Destroy` when a context exists, free the library and release the vector.

`0x0020D010(object, flags)` calls `0x0020D720(object)` first. When bit `0x1` of the flags is set it then
calls `0x00809950(object, 0xD0)`. It answers the object in both cases (`0x0020D01F`-`0x0020D036`).

### The adapter-info chain

`0x0020D2B0` builds an `AdapterInfos` head on the caller's stack: its own vtable, whose two slots return
false (`0x00657140`), then `+0x08` → `NvidiaAdapterInfo` at `0x01E02580`, whose `+0x08` it points at
`AmdAdapterInfo` (`0x01E02588`). `0x0020DA50` (slot 0, temperature) and `0x0020D9F0` (slot 1, name) call
the slot on each link in turn and stop at the first that returns true.

`0x0020D2B0` also zeroes the head's vector words `+0x10`, `+0x18` and `+0x20`, its `+0x28` and its `+0x2C`
(`0x0020D2B2`-`0x0020D2C1`), sets its vtable to `0x00906880` (`0x0020D2CB`) and returns the head (`0x0020D2E7`).
`0x0020D9F0` returns true from the first link that answers true (`0x0020DA2C`), and false when the last link
has answered false (`0x0020DA18`, `0x0020DA43`).

Both vendor objects find a GPU by matching the DXGI device id with `+0x04` of their `AdapterIds`
records:

| Slot | NVIDIA | AMD |
|---|---|---|
| 0, temperature in °C | `0x0020D050`: `0x00159270` on the matching handle, `+0x30 + 8 * index` (`0x0020D0FD`), with the buffer's `+0x08` and `+0x18` set to 1 (`0x0020D0ED`, `0x0020D0F5`); when that returns 0 it stores `+0x14` and returns true (`0x0020D10B`-`0x0020D111`) | `0x0020CEF0`: `ADL2_OverdriveN_Temperature_Get(ctx, adapterIndex, 1, &t)`, then `t / 1000`; the adapter index is `+0x04` of the ADL record at the matching position (`0x0020CF5C`), and the division truncates toward zero (`0x0020CF72`-`0x0020CF83`); when the call returns 0 it stores the quotient and returns true (`0x0020CF87`) |
| 1, name | `0x0020D120`: `0x001590B0`, copied out; the name goes to a 64-byte stack buffer and, when the call returns 0, is copied up to its terminating zero and true returned (`0x0020D1AB`-`0x0020D1CE`) | `0x0020CF90`: the adapter name at `+0x118` of its ADL record, copied up to its terminating zero, then true (`0x0020CFF0`-`0x0020D002`) |

Each slot returns false and writes no output when the ids are not ready (for NVIDIA when `0x0020DAB0`
returns 0, `0x0020D080`, `0x0020D14D`; for AMD when `+0x28` is 0, `0x0020CF03`, `0x0020CF9A`), when no record
among the first `+0x2C` holds the device id (`0x0020D0B0`, `0x0020D176`, `0x0020CF31`, `0x0020CFC4`), or when
the vendor call returns non-zero (`0x0020D109`, `0x0020D1B2`, `0x0020CF70`).

The NVIDIA object fills itself on first use: `0x0020D050` and `0x0020D120` call `0x0020DAB0`, which runs once
(the flag `0x01E02570` starts at 1 and is cleared on entry). It enumerates the GPU handles into `+0x30`,
asks `0x00159180` for each one's PCI ids (zeros on failure), appends the `AdapterIds`, and sets `+0x2C`
and `+0x28`. A failed enumeration leaves `+0x28` at 0 for the rest of the run.

`0x0020D1E0` joins two strings for `0x0020DE30`; `0x0020D270`, `0x0020D7C0`, `0x0020D8A0` and `0x0020E420` copy,
reallocate, grow and append the 12-byte `AdapterIds` vector.

### Where the name and temperature appear

- The Config screen row text `0x0023B530` kind 4 calls `0x0017FDC0` → `0x001DC9D0`. It takes the selected
  output's device name (`(%ws)`, with `\` and `.` removed), asks the chain for the GPU name by the
  selected adapter's device id, falls back to the DXGI description (`%ws`), and joins them (`%s%s`).
- The developer menu's row renderer `0x001CD0E0` calls `0x001DCB90` (`0x001CD593`), which formats
  ` Count %d ,Now: %s ,Video Memory: %lld MB, Temperature: %d(C)` from display `+0x54`, the same name,
  the dedicated video memory divided by 1000 twice, and the chain's temperature (0 when no library
  answers).

## Layouts

`AdapterRecord`, `0x140` bytes, at display `+0x78` (`0x001DD170`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u16[128]` | description | the adapter's UTF-16 name, the fallback GPU name |
| `+0x104` | `u32` | deviceId | PCI device; the key for the vendor libraries and setting 19 |
| `+0x110` | `u64` | dedicatedVideoMemory | bytes; shown in MB, and the start-up tie-break |
| `+0x128` | `u32` | luidLow | setting 20 |
| `+0x12C` | `i32` | luidHigh | setting 21 |
| `+0x130` | `u32` | outputCount | outputs of the adapter (`0x00623CB0`) |
| `+0x138` | `void*` | outputs | `outputCount` output descriptions of `0x60` bytes, each starting with a UTF-16 device name |

The first `0x130` bytes are the adapter's DXGI description as `0x00623CB0` returns it.

`AdapterIds`, 12 bytes, the element of both vendor vectors:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | vendor | `PCI_VEN`, or the low half of NVAPI's device dword |
| `+0x04` | `u32` | device | `DEV`, or the high half; matched against the DXGI device id |
| `+0x08` | `u32` | subsystem | `SUBSYS`, or NVAPI's subsystem id |

`NvidiaAdapterInfo` at `0x01E02580` (vtable `0x00906760`, constructed by `0x0015DCA0`) and `AmdAdapterInfo`
at `0x01F83460` (vtable `0x009064B8`) share the first `0x30` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | slot 0 temperature, slot 1 name |
| `+0x08` | `void*` | next | the next link of the chain; AMD's is 0 |
| `+0x10` | `AdapterIds*` | idsBegin | vector start |
| `+0x18` | `AdapterIds*` | idsEnd | vector end |
| `+0x20` | `AdapterIds*` | idsCapacity | vector capacity |
| `+0x28` | `u8` | ready | set when the ids are read |
| `+0x2C` | `i32` | count | GPUs found |
| `+0x30` | `void*` | gpuHandles | NVIDIA: the first of the GPU handles, one per GPU |

In `AmdAdapterInfo` the vector words are `0x01F83470` (`idsBegin`), `0x01F83478` (`idsEnd`) and `0x01F83480`
(`idsCapacity`).

Its exit routine `0x008A7360` skips the vector when `idsBegin` is 0 (`0x008A739F`). Otherwise it calls `0x0016D6A0`
with begin and end (`0x008A73CA`), which returns at once (`0x0016D6A0`: `ret`), since a 12-byte `AdapterIds` needs no
destructor. It then frees the storage with `0x001CD050(begin, n)`, where `n = (idsCapacity - idsBegin) ÷ 12`
(`0x008A73CF`-`0x008A73F4`: the byte span at `0x008A73D6`, `rdx = (span × 0x2AAAAAAAAAAAAAAB) >> 64` at
`0x008A73DD`, then `sar 1`), and `0x001CD050` frees `n × 12` bytes (`0x001CD06A`-`0x001CD06E`). Last, it zeroes the
three words (`0x008A740D`, `0x008A7415`).

`AmdAdapterInfo` continues, `0xD0` bytes in all:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `void*` | mainControlCreate | `ADL2_Main_Control_Create` |
| `+0x38` | `void*` | mainControlDestroy | `ADL2_Main_Control_Destroy` |
| `+0x40` | `void*` | numberOfAdaptersGet | `ADL2_Adapter_NumberOfAdapters_Get` |
| `+0x48` | `void*` | adapterInfoGet | `ADL2_Adapter_AdapterInfo_Get` |
| `+0x50` | `void*` | adapterActiveGet | `ADL2_Adapter_Active_Get` |
| `+0x58` | `void*` | odnCapabilitiesGet | `ADL2_OverdriveN_Capabilities_Get` |
| `+0x60` | `void*` | odnSystemClocksGet | `ADL2_OverdriveN_SystemClocks_Get` |
| `+0x68` | `void*` | odnSystemClocksSet | `ADL2_OverdriveN_SystemClocks_Set` |
| `+0x70` | `void*` | odnPerformanceStatusGet | `ADL2_OverdriveN_PerformanceStatus_Get` |
| `+0x78` | `void*` | odnFanControlGet | `ADL2_OverdriveN_FanControl_Get` |
| `+0x80` | `void*` | odnFanControlSet | `ADL2_OverdriveN_FanControl_Set` |
| `+0x88` | `void*` | odnPowerLimitGet | `ADL2_OverdriveN_PowerLimit_Get` |
| `+0x90` | `void*` | odnPowerLimitSet | `ADL2_OverdriveN_PowerLimit_Set` |
| `+0x98` | `void*` | odnMemoryClocksGet | `ADL2_OverdriveN_MemoryClocks_Get` |
| `+0xA0` | `void*` | odnMemoryClocksSet | `ADL2_OverdriveN_MemoryClocks_Set` |
| `+0xA8` | `void*` | overdriveCaps | `ADL2_Overdrive_Caps` |
| `+0xB0` | `void*` | odnTemperatureGet | `ADL2_OverdriveN_Temperature_Get`, the only one the game calls after start-up |
| `+0xB8` | `void*` | module | the ADL library handle |
| `+0xC0` | `void*` | context | from `ADL2_Main_Control_Create` |
| `+0xC8` | `void*` | adapterInfos | `count` ADL records of `0x624` bytes: index at `+0x04`, identifier string at `+0x08`, name at `+0x118` |

## Operations

| Function | Role |
|---|---|
| `0x006253D0(context, window)` | load NVAPI, pick the adapter, create the device |
| `0x001DD170(display)` | build the adapter list and write settings 19-21 |
| `0x00623C10(context, &count, &chosen, &mask)` | adapter count, chosen index and usable mask |
| `0x00623CB0(context, i, desc, &outputs)` | one adapter's description and output count |
| `0x00624490(context, i, n, out)` | one adapter's output descriptions |
| `0x001DC650(display, i, back)` | select the next usable adapter from `i` and save it |
| `0x001DC7A0(display, monitor, apply)` | select a monitor |
| `0x00628690(context)` | probe the multisample levels |
| `0x001DF2C0(settings, value, up)` | step the Anti-Aliasing value |
| `0x00159340()` | initialise NVAPI |
| `0x0020DA50` / `0x0020D9F0(chain, deviceId, out)` | temperature / name through the chain |

## State

| Address | What |
|---|---|
| `0x01E02580` | `NvidiaAdapterInfo` |
| `0x01E02570` | its run-once flag |
| `0x01F83460` | `AmdAdapterInfo` |
| `0x02EAE100` | NVAPI library handles, two |
| `0x02EAE0E0` | `nvapi_QueryInterface` |
| `0x02EAE128` | NVAPI in-call counter |
| `0x02EAE138` | NVAPI reference counts: set to 1 by a load in `0x00158EC0` (`0x00158F39`), raised by `0x00159340` |
| `0x02CED884` | NVAPI initialised, written only |
| `[0x01F82D20] + 0x44C` | the MSAA mask |

The fields of `NvidiaAdapterInfo` that instructions name directly, and the accesses its own functions make through
the object (`rdi` in `0x0020D050`, `rsi` in `0x0020D120`, `rbp` in `0x0020DAB0`):

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01E02590` | `void*` | 0 (file-backed `.data`) | `+0x10` `idsBegin`; each 16-byte store also clears `idsEnd` `0x01E02598` | `0x0015DCA0` (`0x0015DCDD`, 0); the exit destructor `0x008A7430` (`0x008A74AD`, 0); through the object, the grow and append helpers `0x0020DAB0` passes `+0x10` to (`0x0020DBD1`, `0x0020DC08`) | `0x008A7430` (`0x008A7434`, `0x008A7458`, `0x008A7472`, `0x008A7493`); `0x0020D050` (`0x0020D08C`); `0x0020D120` (`0x0020D159`); `0x0020DAB0` (`0x0020DB9A`, `0x0020DBE3`) |
| `0x01E025A0` | `void*` | 0 (file-backed `.data`) | `+0x20` `idsCapacity` | `0x0015DCA0` (`0x0015DCB9`, 0); `0x008A7430` (`0x008A74A2`, 0); the same helpers | `0x008A7430` (`0x008A7464`: the capacity less `idsBegin`, divided by the 12-byte record size, is the count it frees with `0x001CD050`); `0x0020DAB0` (`0x0020DBC6`, `0x0020DBFD`, compared with `idsEnd`) |
| `0x01E025A8` | `u8` | 0 (file-backed `.data`) | `+0x28` `ready` | `0x0015DCA0` (`0x0015DCC3`, 0); `0x0020DAB0` (`0x0020DC57`, 1) | `0x0020DAB0` (`0x0020DC5B`, its return value) |
| `0x01E025AC` | `i32` | 0 (file-backed `.data`) | `+0x2C` `count` | `0x0015DCA0` (`0x0015DCC9`, 0); `0x0020DAB0` (`0x0020DC54`) | `0x0020D050` (`0x0020D082`); `0x0020D120` (`0x0020D14F`); both sign-extend it (`movsxd`) |

`0x0015DCA0` registers `0x008A7430` with `atexit`. `0x0020DAB0` also writes `idsEnd` through the object (`0x0020DC27`, plus
12 per record).

## Modding notes

- To force an adapter, write its device id and LUID into DeviceID, LUIDLow and LUIDHigh; an adapter
  below feature level 11.0, without dedicated memory or without an output is never chosen.
- `0x0020CEF0` calls `ADL2_OverdriveN_Temperature_Get` without testing the pointer, and `0x0020D2F0` does
  not require it, so an ADL library without that export faults when the temperature is asked for.
- Neither vendor library is required: every query falls through to the next link, and the name falls
  back to the DXGI description.

## Related

- [Driver DLL search](driver-dll-search.md): how `nvapi64.dll` is found.
- [Screen mode and aspect](../Graphics/screen-mode-and-aspect.md): the display object and its mode lists.
- [Config screen](../Menus-And-HUD/config-screen.md): the Display Adapter and Anti-Aliasing rows.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): DeviceID, LUIDLow, LUIDHigh, MSAA and Monitor.
