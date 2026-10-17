---
title: "Graphics adapters and vendor libraries: which GPU the game picks, the adapter list, NVAPI and AMD ADL"
kind: "system"
category: "Steam and achievements"
addresses: "006253D0, 001DD170, 00623C10, 00623CB0, 00624490, 001DC650, 001DC7A0, 00628690, 001DF2C0, 00159340, 00158F60, 00158EC0, 00158DE0, 00158FE0, 001590B0, 00159180, 00159270, 0020D2B0, 0020D9F0, 0020DA50, 0020DAB0, 0020D050, 0020D120, 0020D2F0, 0020DE30, 0020CEF0, 0020CF90, 0020D720, 001DC9D0, 001DCB90, 01E02580, 01F83460"
---

## What the player sees

On a machine with more than one GPU the game starts on the adapter saved in `GameSetting.ini`, or on
the one with the most dedicated video memory. The Config screen's Display Adapter row shows the GPU's
name followed by the monitor, such as `(DISPLAY1)`, and steps through every monitor of
every usable adapter. The Anti-Aliasing row offers only the multisample levels the GPU reports. The
game asks NVIDIA's and AMD's driver libraries for the GPU's name and temperature; without them it uses
the name Windows reports.

## How it works

### Choosing the adapter at start-up

The renderer's start-up `006253D0` creates a DXGI factory (`CreateDXGIFactory`, kept at context
`+1878`<sub>h</sub>) and walks its adapters. For each adapter `i`:

1. It creates a throw-away device on it with `D3D11CreateDevice`, starting from feature level
   `9100`<sub>h</sub>, and skips the adapter unless the level it gets is above `AFFF`<sub>h</sub> (11.0 or higher).
2. It reads the adapter's description and counts its outputs, logging
   `%d ,%d Adapter name = %ws , Display Name = %ws`.
3. An adapter with dedicated video memory and at least one output sets bit `i` of the usable mask at
   context `+18B0`<sub>h</sub>.
4. Among usable adapters, the first whose device id and LUID equal the window description's `+18`<sub>h</sub>,
   `+1C`<sub>h</sub> and `+20`<sub>h</sub> is taken at once; until then the one with the most dedicated video memory is
   kept. The choice goes to context `+1880`<sub>h</sub> and its index to `+18AC`<sub>h</sub>.

`0079E520` fills those three fields of the window description `01F403A8` from settings 19 DeviceID,
20 LUIDLow and 21 LUIDHigh (`0079E5AF`-`0079E5D2`), stores its address at `[02EA5368] + D10h` and calls
`0079F150`, which passes it on (`0079E4FE`). With an adapter chosen, `00625830` creates the device and swap chain on it.

### The adapter list

The display object's constructor runs `001DD170`, which copies what the renderer found:

1. `00623C10` returns the adapter count, the chosen index (`+18AC`<sub>h</sub>) and the usable mask (`+18B0`<sub>h</sub>),
   stored at display `+50`<sub>h</sub>, `+4C`<sub>h</sub> and `+58`<sub>h</sub>; `+48`<sub>h</sub> starts equal to `+4C`<sub>h</sub>.
2. For each adapter it allocates a `140`<sub>h</sub>-byte `AdapterRecord`: `00623CB0` writes the adapter's
   description and its output count; `00624490` fills one `60`<sub>h</sub>-byte output description per output.
3. A usable adapter adds its output count to `+54`<sub>h</sub>.
4. It writes the selected record's device id and LUID back to settings 19, 20 and 21 (`001DF340`).

### The Display Adapter row

Console id `10A`<sub>h</sub> steps the monitor, display `+60`<sub>h</sub>, through the selected adapter's outputs. Past the
last one it moves to the next usable adapter with `001DC650` and starts again at monitor 1; going back
from monitor 1 it moves to the previous usable adapter at its last monitor. `001DC650` skips adapters whose bit in `+58`<sub>h</sub> is clear,
stores the index at `+48`<sub>h</sub> and writes the record's device id and LUID to settings 19-21.

`001DC7A0` stores the monitor, folding a number above the output count back to 1. When the adapter is
the one in use (`+48`<sub>h</sub> equals `+4C`<sub>h</sub>) and the monitor differs from `+64`<sub>h</sub>, it rebuilds the display-mode list (`001DD420`), calls
`007A03D0`, stores setting 26 Monitor and writes the settings file (`001DFD40`).

### Anti-aliasing levels from the device

After the device exists, `00625830` calls `00628690` (`00625E7C`). It asks the device for
`CheckMultisampleQualityLevels` (vtable `+F0`<sub>h</sub>) on format 28 for every sample count 2-32, and for
each count that reports levels it sets one bit of the settings' MSAA mask at `[01F82D20] + 44Ch`
through `0017D9C0` → `001DF2B0`:

| Sample count | Bit | MSAA value |
|---:|---:|---|
| 2 | 1 | MSAA2X |
| 4 | 2 | MSAA4X |
| 8 | 3 | MSAA8X, and bit 4 CSAA16x when more than 16 quality levels |
| 16 | 5 | CSAA16XQ |

Bit 0 (Off) comes from the settings constructor `001DE050`. The Anti-Aliasing row cycles with
`001DF2C0`, which steps the value through 0-4 modulo 5, skipping clear bits, and stores it in setting
8 (`+20`<sub>h</sub>). The constructor's bit 0 (`001DE075`, never cleared; the probe only adds bits) means the
skip loop always ends, on Off at worst. Value 5 can be set in the mask but is never reached, and nothing
sets bit 6.

### Loading NVAPI

`006253D0` calls `00159340` before it creates the factory. `00159340` takes the critical section
`02EAEA70` and calls `00158F60(0)`; on success it raises the reference count `02EAE138`. A non-zero
result is logged as `NvAPI_Initialize() failed = 0x%x` and stored as 0 in `02CED884` (1 on success);
nothing reads `02CED884`.

- `00158F60(i)` waits while byte `02EAE120 + i` is set, sleeping 100 ms up to ten times, and then gives
  up with -1. With the byte clear it loads library `i` if its handle at `02EAE100 + 8i` is 0. Nothing
  writes `02EAE120`, so it never waits.
- `00158EC0(i)` loads `nvapi64.dll` for `i` = 0 and `nvpowerapi.dll` for 1 through the driver-DLL
  search `0015BB30` ([Driver DLL search](driver-dll-search.md)), returns -2 when that fails, and frees
  the library when `00158DE0` fails; on success it stores the handle at `02EAE100 + 8i` and sets the count
  `02EAE138 + 4i` to 1 (`00158F31`, `00158F39`). Every caller passes 0.
- `00158DE0` resolves `nvapi_QueryInterface`, asks it for interface `0150E828`<sub>h</sub> and calls it; a
  non-zero result clears the query function and is returned. It then asks for `33C7358C`<sub>h</sub> and
  `593E8644`<sub>h</sub> as a pre-call and post-call hook pair, keeping them only when the first exists and
  the second does not, and clears the `918`<sub>h</sub>-byte function cache at `02EAE150`.
- For library 1, `00158DE0` instead resolves `nvapi_pepQueryInterface` into `02EAE0E8`, a path no
  caller takes.

### Calling NVAPI

The four wrappers share one shape: they raise the in-call counter `02EAE128` (locked add), call
`00158F60(0)`, resolve their function once through the query function into a cache slot, call the
pre-call hook, the function and the post-call hook, and lower the counter. A function that cannot be
resolved returns -3.

| Wrapper | Interface id | Cache slot | What the game reads |
|---|---|---|---|
| `00158FE0(handles, &count)` | `E5AC921F`<sub>h</sub> | `02EAE1B0` | the GPU handles and their count |
| `00159180(handle, &id, &subsys, ...)` | `2DDFB66E`<sub>h</sub> | `02EAE268` | PCI vendor and device in one dword, the subsystem id |
| `001590B0(handle, name)` | `CEEE8E9F`<sub>h</sub> | `02EAE260` | the GPU name, into a 64-byte buffer |
| `00159270(handle, 0, settings)` | `E3640A56`<sub>h</sub> | `02EAE310` | the temperature at `+14`<sub>h</sub> of a `44`<sub>h</sub>-byte buffer whose first dword is `20044`<sub>h</sub> |

### Loading AMD ADL

The static initialiser `0015DC80` builds `AmdAdapterInfo` at `01F83460` with `0020D2F0` and registers
`008A7360` to tear it down. `0020D2F0`:

1. loads `atiadlxx.dll`, else `atiadlxy.dll`, with plain `LoadLibraryW`, and stops if neither loads;
2. resolves seventeen `ADL2_` functions into `+30`<sub>h</sub>-`+B0`<sub>h</sub>;
3. requires all but `ADL2_OverdriveN_PowerLimit_Get`, `_PowerLimit_Set` and `_Temperature_Get`, then
   calls `ADL2_Main_Control_Create(0020D7B0, 1, +C0h)`; `0020D7B0` is a `malloc` adapter;
4. reads the adapter count, allocates `count × 624h` bytes at `+C8`<sub>h</sub> and fills them with
   `ADL2_Adapter_AdapterInfo_Get`;
5. parses each record's identifier string at `+08`<sub>h</sub> with `0020DE30` into an `AdapterIds`, appends it
   to the vector at `+10`<sub>h</sub>, then sets the count `+2C`<sub>h</sub> and the ready byte `+28`<sub>h</sub>.

`0020DE30` splits the string at each `&`, splits each part at its last `_`, and reads the value as hex
(`"0x"` prefix, `sscanf` with `%x`). The keys `PCI_VEN`, `DEV` and `SUBSYS` fill vendor, device and
subsystem; other keys are ignored.

`0020D720`, slot 2's body (`0020D010`), and the exit routine `008A7360` call
`ADL2_Main_Control_Destroy` when a context exists, free the library and release the vector.

### The adapter-info chain

`0020D2B0` builds an `AdapterInfos` head on the caller's stack: its own vtable, whose two slots return
false (`00657140`), then `+08`<sub>h</sub> → `NvidiaAdapterInfo` at `01E02580`, whose `+08`<sub>h</sub> it points at
`AmdAdapterInfo` (`01E02588`). `0020DA50` (slot 0, temperature) and `0020D9F0` (slot 1, name) call
the slot on each link in turn and stop at the first that returns true.

Both vendor objects find a GPU by matching the DXGI device id with `+04`<sub>h</sub> of their `AdapterIds`
records:

| Slot | NVIDIA | AMD |
|---|---|---|
| 0, temperature in °C | `0020D050`: `00159270` on the matching handle | `0020CEF0`: `ADL2_OverdriveN_Temperature_Get(ctx, adapterIndex, 1, &t)`, then `t / 1000` |
| 1, name | `0020D120`: `001590B0`, copied out | `0020CF90`: the adapter name at `+118`<sub>h</sub> of its ADL record |

The NVIDIA object fills itself on first use: `0020D050` and `0020D120` call `0020DAB0`, which runs once
(the flag `01E02570` starts at 1 and is cleared on entry). It enumerates the GPU handles into `+30`<sub>h</sub>,
asks `00159180` for each one's PCI ids (zeros on failure), appends the `AdapterIds`, and sets `+2C`<sub>h</sub>
and `+28`<sub>h</sub>. A failed enumeration leaves `+28`<sub>h</sub> at 0 for the rest of the run.

`0020D1E0` joins two strings for `0020DE30`; `0020D270`, `0020D7C0`, `0020D8A0` and `0020E420` copy,
reallocate, grow and append the 12-byte `AdapterIds` vector.

### Where the name and temperature appear

- The Config screen row text `0023B530` kind 4 calls `0017FDC0` → `001DC9D0`. It takes the selected
  output's device name (`(%ws)`, with `\` and `.` removed), asks the chain for the GPU name by the
  selected adapter's device id, falls back to the DXGI description (`%ws`), and joins them (`%s%s`).
- The developer menu's row renderer `001CD0E0` calls `001DCB90` (`001CD593`), which formats
  ` Count %d ,Now: %s ,Video Memory: %lld MB, Temperature: %d(C)` from display `+54`<sub>h</sub>, the same name,
  the dedicated video memory divided by 1000 twice, and the chain's temperature (0 when no library
  answers).

## Layouts

`AdapterRecord`, `140`<sub>h</sub> bytes, at display `+78`<sub>h</sub> (`001DD170`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `u16[128]` | description | the adapter's UTF-16 name, the fallback GPU name |
| `104`<sub>h</sub> | `u32` | deviceId | PCI device; the key for the vendor libraries and setting 19 |
| `110`<sub>h</sub> | `u64` | dedicatedVideoMemory | bytes; shown in MB, and the start-up tie-break |
| `128`<sub>h</sub> | `u32` | luidLow | setting 20 |
| `12C`<sub>h</sub> | `i32` | luidHigh | setting 21 |
| `130`<sub>h</sub> | `u32` | outputCount | outputs of the adapter (`00623CB0`) |
| `138`<sub>h</sub> | `void*` | outputs | `outputCount` output descriptions of `60`<sub>h</sub> bytes, each starting with a UTF-16 device name |

The first `130`<sub>h</sub> bytes are the adapter's DXGI description as `00623CB0` returns it.

`AdapterIds`, 12 bytes, the element of both vendor vectors:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | vendor | `PCI_VEN`, or the low half of NVAPI's device dword |
| `04`<sub>h</sub> | `u32` | device | `DEV`, or the high half; matched against the DXGI device id |
| `08`<sub>h</sub> | `u32` | subsystem | `SUBSYS`, or NVAPI's subsystem id |

`NvidiaAdapterInfo` at `01E02580` (vtable `00906760`, constructed by `0015DCA0`) and `AmdAdapterInfo`
at `01F83460` (vtable `009064B8`) share the first `30`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | vtable | slot 0 temperature, slot 1 name |
| `08`<sub>h</sub> | `void*` | next | the next link of the chain; AMD's is 0 |
| `10`<sub>h</sub> | `AdapterIds*` | idsBegin | vector start |
| `18`<sub>h</sub> | `AdapterIds*` | idsEnd | vector end |
| `20`<sub>h</sub> | `AdapterIds*` | idsCapacity | vector capacity |
| `28`<sub>h</sub> | `u8` | ready | set when the ids are read |
| `2C`<sub>h</sub> | `i32` | count | GPUs found |
| `30`<sub>h</sub> | `void*` | gpuHandles | NVIDIA: the first of the GPU handles, one per GPU |

`AmdAdapterInfo` continues, `D0`<sub>h</sub> bytes in all:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `30`<sub>h</sub> | `void*` | mainControlCreate | `ADL2_Main_Control_Create` |
| `38`<sub>h</sub> | `void*` | mainControlDestroy | `ADL2_Main_Control_Destroy` |
| `40`<sub>h</sub> | `void*` | numberOfAdaptersGet | `ADL2_Adapter_NumberOfAdapters_Get` |
| `48`<sub>h</sub> | `void*` | adapterInfoGet | `ADL2_Adapter_AdapterInfo_Get` |
| `50`<sub>h</sub> | `void*` | adapterActiveGet | `ADL2_Adapter_Active_Get` |
| `58`<sub>h</sub> | `void*` | odnCapabilitiesGet | `ADL2_OverdriveN_Capabilities_Get` |
| `60`<sub>h</sub> | `void*` | odnSystemClocksGet | `ADL2_OverdriveN_SystemClocks_Get` |
| `68`<sub>h</sub> | `void*` | odnSystemClocksSet | `ADL2_OverdriveN_SystemClocks_Set` |
| `70`<sub>h</sub> | `void*` | odnPerformanceStatusGet | `ADL2_OverdriveN_PerformanceStatus_Get` |
| `78`<sub>h</sub> | `void*` | odnFanControlGet | `ADL2_OverdriveN_FanControl_Get` |
| `80`<sub>h</sub> | `void*` | odnFanControlSet | `ADL2_OverdriveN_FanControl_Set` |
| `88`<sub>h</sub> | `void*` | odnPowerLimitGet | `ADL2_OverdriveN_PowerLimit_Get` |
| `90`<sub>h</sub> | `void*` | odnPowerLimitSet | `ADL2_OverdriveN_PowerLimit_Set` |
| `98`<sub>h</sub> | `void*` | odnMemoryClocksGet | `ADL2_OverdriveN_MemoryClocks_Get` |
| `A0`<sub>h</sub> | `void*` | odnMemoryClocksSet | `ADL2_OverdriveN_MemoryClocks_Set` |
| `A8`<sub>h</sub> | `void*` | overdriveCaps | `ADL2_Overdrive_Caps` |
| `B0`<sub>h</sub> | `void*` | odnTemperatureGet | `ADL2_OverdriveN_Temperature_Get`, the only one the game calls after start-up |
| `B8`<sub>h</sub> | `void*` | module | the ADL library handle |
| `C0`<sub>h</sub> | `void*` | context | from `ADL2_Main_Control_Create` |
| `C8`<sub>h</sub> | `void*` | adapterInfos | `count` ADL records of `624`<sub>h</sub> bytes: index at `+04`<sub>h</sub>, identifier string at `+08`<sub>h</sub>, name at `+118`<sub>h</sub> |

## Operations

| Function | Role |
|---|---|
| `006253D0(context, window)` | load NVAPI, pick the adapter, create the device |
| `001DD170(display)` | build the adapter list and write settings 19-21 |
| `00623C10(context, &count, &chosen, &mask)` | adapter count, chosen index and usable mask |
| `00623CB0(context, i, desc, &outputs)` | one adapter's description and output count |
| `00624490(context, i, n, out)` | one adapter's output descriptions |
| `001DC650(display, i, back)` | select the next usable adapter from `i` and save it |
| `001DC7A0(display, monitor, apply)` | select a monitor |
| `00628690(context)` | probe the multisample levels |
| `001DF2C0(settings, value, up)` | step the Anti-Aliasing value |
| `00159340()` | initialise NVAPI |
| `0020DA50` / `0020D9F0(chain, deviceId, out)` | temperature / name through the chain |

## State

| Address | What |
|---|---|
| `01E02580` | `NvidiaAdapterInfo` |
| `01E02570` | its run-once flag |
| `01F83460` | `AmdAdapterInfo` |
| `02EAE100` | NVAPI library handles, two |
| `02EAE0E0` | `nvapi_QueryInterface` |
| `02EAE128` | NVAPI in-call counter |
| `02EAE138` | NVAPI reference counts: set to 1 by a load in `00158EC0` (`00158F39`), raised by `00159340` |
| `02CED884` | NVAPI initialised, written only |
| `[01F82D20] + 44Ch` | the MSAA mask |

## Modding notes

- To force an adapter, write its device id and LUID into DeviceID, LUIDLow and LUIDHigh; an adapter
  below feature level 11.0, without dedicated memory or without an output is never chosen.
- `0020CEF0` calls `ADL2_OverdriveN_Temperature_Get` without testing the pointer, and `0020D2F0` does
  not require it, so an ADL library without that export faults when the temperature is asked for.
- Neither vendor library is required: every query falls through to the next link, and the name falls
  back to the DXGI description.

## Related

- [Driver DLL search](driver-dll-search.md): how `nvapi64.dll` is found.
- [Screen mode and aspect](../Graphics/screen-mode-and-aspect.md): the display object and its mode lists.
- [Config screen](../Menus-And-HUD/config-screen.md): the Display Adapter and Anti-Aliasing rows.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): DeviceID, LUIDLow, LUIDHigh, MSAA and Monitor.
