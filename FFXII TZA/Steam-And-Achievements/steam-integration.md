[Home](../../README.md) / [Steam and achievements](README.md) / Steam integration

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Steam integration: how the game starts and pumps Steam, the interfaces and callbacks it uses, and what it does without Steam | system | Steam and achievements | Steam and achievements | The start-up order (interface context, SteamAPI_Init, the achievement manager, the overlay listener, the relaunch check with app id 595520), the interface context and the five interface slots the game calls, the eight callbacks and their handlers, the per-window-pump SteamAPI_RunCallbacks, the stats receipt, the Steam language and user id the game reads, the teardown, and every path that changes when Steam is absent. | 0x007980A0, 0x01DFE0D0, 0x001F3E10, 0x001F3AE0, 0x0020CD30, 0x0020C730, 0x01F83450, 0x0020CCC0, 0x008655E0, 0x008655A0, 0x007A0810, 0x008653B0, 0x00865510, 0x007A3110, 0x0020C940, 0x0020C8C0, 0x0020CB20, 0x0020CE60, 0x0020CE10, 0x0020CD80, 0x00865660, 0x007A0C60, 0x001F3ED0, 0x0017D990, 0x00798FF0 |

## What the player sees

When Steam's relaunch check asks for it, the game exits at start-up. Under Steam, the overlay works, achievements
unlock, the game's language follows the language set for it in Steam, and saves go to a folder named after
the Steam account. Without Steam the game still runs. The thirty achievements the Sky Pirate's Den shows keep
their award bits and counters in the save; the other eleven (the eight story scenes, the two Trial Mode stages
and Champion of Ivalice) have no saved flag and are not recorded. The language and save folder fall back to
their own settings.

## How it works

### Start-up order

The main routine `0x007980A0` does this before it loads any setting:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `SteamInternal_ContextInit(0x01DFE0D0)` returns the interface context. When its `+0x18` (the utilities interface) is already filled, step 2 is skipped. | `0x00798116` |
| 2 | `SteamAPI_Init`. On failure the game jumps to step 5: no achievement manager and no overlay listener are made. | `0x00798123` |
| 3 | `0x0020CD30` builds the achievement manager. | `0x0079812D` |
| 4 | `0x008655E0` registers the overlay callback. When `0x02EB3860` is 0 it allocates a `0x20`-byte callback object, registers it for 331 with the handler `0x008655A0` and stores it at `0x02EB3860`; a failed allocation stores 0 there. With `0x02EB3860` already set it returns at once. | `0x00798132`<br>`0x008655E4`<br>`0x00865636`<br>`0x0086563C`<br>`0x0086564F` |
| 5 | `SteamAPI_RestartAppIfNecessary(0x91640)`, app id 595520. On true the process calls `exit(1)`. | `0x0079813C`<br>`0x0079814B` |
| 6 | `0x007A0810` builds the connection listener. | `0x00798152` |

Later in the same routine it calls `0x001F3ED0`, which prints the Steam user id¹, reads the
settings² and then applies the Steam language³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007981EA` |
| ² | `0x001DED50`, `0x0079826B` |
| ³ | `0x007A0C60`, `0x00798272` |

</details>

### The interface context

`0x01DFE0D0` holds the context's init callback `0x001F3E10`. That callback zeroes the slots `+0x00`-`+0x98`¹, leaving the last slot `+0xA0` as it was, and, when `SteamAPI_GetHSteamPipe`
returns a pipe², calls `0x001F3AE0` as a tail jump³, returning its result; without a
pipe it returns 0. `0x001F3AE0` creates `SteamClient017` through
`SteamInternal_CreateInterface` and asks that object for each interface by its version string, stopping at
the first that fails; the slot order is in Layouts.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001F3E1B`-`0x001F3E6F` |
| ² | `0x001F3E76` |
| ³ | `0x001F3E88` |

</details>

All 25 calls through `SteamInternal_ContextInit` read one of five slots from the context they get back:

| Slot offset | Interface | Sites | What the game calls |
|---|---|---:|---|
| `+0x08` | `SteamUser019` | 4 | slot `+0x10` for the user id (`0x001F3ED0`); slot `+0x08`, a logged-on test (`0x0020CCC0`) |
| `+0x18` | `SteamUtils009` | 2 | the start-up test (`0x00798116`); slot `+0x48`, the app id (`0x0020C7FD`) |
| `+0x28` | `STEAMUSERSTATS_INTERFACE_VERSION011` | 17 | the achievement calls below |
| `+0x30` | `STEAMAPPS_INTERFACE_VERSION008` | 1 | slot `+0x20`, the game language (`0x007A0C94`) |
| `+0x68` | `SteamController005` | 1 | stored at `0x02EA9508` and initialised (`0x0079791D`) |

The other sixteen interfaces are fetched and never called.

### The achievement manager

When `0x01F83450` is 0¹, `0x0020CD30` allocates `0x80` bytes, calls
`0x0020C730(object, 0x01DFE410, 41)` and stores the result at `0x01F83450`²; a failed allocation stores
0 there³. With `0x01F83450` already set it returns at once. `0x0020C730`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0020CD3D` |
| ² | `0x0020CD71` |
| ³ | `0x0020CD59` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | registers callbacks 1101, 1102 and 1103 (`SteamAPI_RegisterCallback`, `0x0020C78C`-`0x0020C7EC`), after setting `+0x00` to 0 and the received byte `+0x18` to 0; each callback object gets the manager at its `+0x10`, its handler at `+0x18` and 0 in its flag byte `+0x08`; | `0x0020C75D`, `0x0020C75F` |
| 2 | sets the achieved count `+0x14` to 0, then stores the utilities interface's slot `+0x48` result, the app id, at `+0x00`; every handler compares it with the callback's first field and ignores a mismatch; | `0x0020C7F3`<br>`0x0020C80A`-`0x0020C80D` |
| 3 | stores the 41 static achievement records as its entry table and calls `0x0020CCC0`, which, when the user interface's slot `+0x08` returns true, calls the stats interface's slot `+0x00` (the stats request). |   |

   The three callback objects are at the manager's `+0x20`, `+0x40` and `+0x60`, for callbacks 1101,
   1102 and 1103 in that order; their vtables are `0x00906360`, `0x009063A0` and `0x009063E0` and their
   handlers `0x0020C940`, `0x0020CB20` and `0x0020C8C0`. Each also gets 0 in its byte `+0x08` and its dword
   `+0x0C` and the manager in its qword `+0x10`, and is then handed with its callback number to the
   import at `0x008C3180`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0020C763`-`0x0020C7EC` |

</details>

   The entry table's address goes to the manager's `+0x08` and the count to
   its dword `+0x10`¹. `0x0020C730` answers the manager².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0020C80F`, `0x0020C813` |
| ² | `0x0020C81F` |

</details>
| Step | What happens | Where in the code |
|---|---|---|
| 4 | `0x0020CCC0` returns 0 when the context's stats slot `+0x28` or user slot `+0x08` is 0 or the logged-on test is false; otherwise it reaches the stats request as a tail jump and returns its result. `0x0020C730` returns the object. | `0x0020CCD1`, `0x0020CCE5`<br>`0x0020CD05`<br>`0x0020CD1F`<br>`0x0020C81F` |

### Callbacks

Eight registrations, each with an RTTI-named `CCallback<owner, event>` object and its handler:

| Id | Event | Handler | Effect |
|---:|---|---|---|
| `1101` | `UserStatsReceived_t` | `0x0020C940` | the stats receipt, below |
| `1102` | `UserStatsStored_t` | `0x0020CB20` | logs `Stored stats for Steam` or `RequestStatsd - failed, %d`: the first for a result of 1, the second for any other result (`0x0020CB31`-`0x0020CB4A`) |
| `1103` | `UserAchievementStored_t` | `0x0020C8C0` | counts one more achieved (`0x0020C8D4`); at 40, awards entry 0 if Steam has it unachieved (`0x0020CE10`): when the count equals `count - 1` (`0x0020C8D9`) it reads entry 0 from Steam through the stats slot `+0x30` (`0x0020C901`) and, when that leaves `+0x190` at 0, calls `0x0020CE10(manager, entry 0's name)` (`0x0020C918`), which calls SetAchievement and StoreStats only when `+0x18` is set (`0x0020CE16`) and otherwise returns 0; on every matching callback it then logs `Stored Achievement for Steam` (`0x0020C91D`-`0x0020C92E`) |
| `331` | `GameOverlayActivated_t` | `0x008655A0` | logs the overlay state and stores it in byte `+0x1D` of the application object `[0x02EA5368]` |
| `101` | `SteamServersConnected_t` | `0x00865560` | listener `+0x84` = 1, `+0x88` = 0 |
| `103` | `SteamServersDisconnected_t` | `0x00865570` | listener `+0x88` += 1, `+0x80` = 1, `+0x84` = 0 |
| `102` | `SteamServerConnectFailure_t` | `0x00865570` | the same body |
| `704` | `SteamShutdown_t` | `0x00865590` | listener `+0x80` and `+0x88` = 0 |

The first three belong to the manager, the overlay one to the object at `0x02EB3860`, and the last four to
the listener at `0x02EACC90`¹. `0x008653B0` registers them in the order 101, 103, 102, 704², then sets `+0x84` to 1 and `+0x80` and `+0x88` to 0³ and
returns the listener.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008653B0` |
| ² | `0x008653E2`-`0x0086546B` |
| ³ | `0x00865474`-`0x0086547F` |

</details>

### The pump

`0x007A3110` is slot 0 of Phyre's `PWindowWin32Base` and `PWindow` vtables¹. It
returns 9 when byte `+0x69` of `[0x02EA5368]` is set, which the window's close handler `0x00798FF0` does for
close codes 1 and 2². Otherwise it calls `SteamAPI_RunCallbacks`³, the only call
of that import, and then `0x007A2440` with the application's `+0xDF8`⁴, and returns 0⁵. Steam callbacks therefore run once per window pump, on that thread.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x01CB2468`, `0x01CB2480` |
| ² | `0x00799306` |
| ³ | `0x007A312E` |
| ⁴ | `0x007A3134`-`0x007A313B` |
| ⁵ | `0x007A3140` |

</details>

### The stats receipt

`0x0020C940`, on a matching app id:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | A result other than 1 logs `RequestStats - failed, %d` and changes nothing. |   |
| 2 | It logs `Received stats and achievements from Steam` with `OutputDebugStringA`, then sets manager `+0x18` (stats received) and zeroes the achieved count `+0x14`. | `0x0020C974`<br>`0x0020C97F`, `0x0020C983` |
| 3 | For entries 1-40 it asks the stats slot `+0x30` (GetAchievement) to write each entry's `+0x190`, counts the achieved ones, and copies the `name` and `desc` display attributes (slot `+0x60`) into `+0x10` and `+0x90`, through `0x001CCAC0(+0x10, 0x80, "%s", name)` and `0x001CCAC0(+0x90, 0x100, "%s", desc)`. | `0x0020CA1A`<br>`0x0020CA57` |
| 4 | When all forty are achieved it reads entry 0 and, if Steam has it unachieved, calls slot `+0x38` and `+0x50` (SetAchievement, StoreStats). |   |

Slot names follow the Steamworks interface order; the arguments match it (`+0x30` takes a name and a flag
address, `+0x60` a name and a key).

### Awards

`0x0020CE60(manager, entry)` (reached from `0x008632B0`) and the by-scene award `0x0020CB50` mark the entry's
`+0x190`, then call SetAchievement and StoreStats only when `+0x18` is set. An award made before the receipt
stays local, and the receipt then overwrites `+0x190` with Steam's value.

Both skip an entry whose `+0x190` is already set¹ and clear `+0x194` when they set it². `0x0020CE60` returns 1 for an entry already achieved³, 0 before the
receipt⁴, and otherwise StoreStats' result through its tail jump⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0020CE79`, `0x0020CBC2` |
| ² | `0x0020CE82`, `0x0020CBCF` |
| ³ | `0x0020CEE2` |
| ⁴ | `0x0020CED6` |
| ⁵ | `0x0020CED2` |

</details>

### The connection listener and closing the window

`0x007A0810` builds the listener once and registers `0x008B7DB0` with `atexit` to unregister it¹.
`0x00865510` returns 1 when its `+0x80` is 1, `+0x84` is 0 and `+0x88` is at most 1. The close handler
`0x00798FF0`, for an ordinary close request: in full-screen mode (setting 2 = 1) it quits at once; otherwise
the first close request while `0x00865510` returns 1 is ignored², and any other asks for
confirmation with a message box (texts `0x7836` and `0x7835`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00865490` |
| ² | `0x02EACD28` |

</details>

`0x0019A510(id)` loads those texts from the executable's string table¹: in each
module of the ATL module list it finds block `id / 16 + 1` of resource type 6, and `0x0019A5B0` steps over
`id & 0xF` length-prefixed strings in the block, returning 0 for an empty or missing string.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007991FE`, `0x00799234` |

</details>

### Language and user id

`0x007A0C60` returns at once without the apps interface. Otherwise it maps Steam's game language to the
Language setting through `0x001DF340(settings, 0, value)`: `japanese` 0, `english` 1, `french` 2, `german`
3, `italian` 4, `spanish` 5, `koreana` 6, `tchinese` 7, `schinese` 8; any other string leaves it.

`0x001F3ED0` formats the Steam id as a decimal string (`%llu`) when the user interface exists and leaves the
string empty otherwise. The save folder appends it ([save file format](../Saving-Loading-And-Settings/save-file-format.md)).

It zeroes `0x1FE` bytes of a `0x200`-byte buffer in its own frame¹ and takes the context from
`SteamInternal_ContextInit(0x01DFE0D0)`². When the context's `+0x08`, the user interface, is non-null
it calls that interface's slot `+0x10` for the id³, formats it through `0x001F3A80` with `%llu`⁴ and prints it with `"%s\n"` through `0x001F3F70`⁵, which writes to `__acrt_iob_func(1)`
with `__stdio_common_vfwprintf`⁶. Without the interface it prints nothing.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001F3EF6` |
| ² | `0x001F3F02` |
| ³ | `0x001F3F28` |
| ⁴ | `0x001F3F3C` |
| ⁵ | `0x001F3F4D` |
| ⁶ | `0x001F3F98`, `0x001F3FB7` |

</details>

It returns the buffer's address¹, which lies in its own released frame; its four callers use the
string right after the return².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001F3F52` |
| ² | `0x00197F7A`, `0x007981EF`, `0x0079FA94`, `0x00862B24` |

</details>

### Teardown

After the message loop ends, `0x007980A0` calls `0x0020CD80`¹, which unregisters the manager's
three callbacks, frees it and stores 0 at `0x01F83450`, and `0x00865660`² for the overlay object.
The game imports no `SteamAPI_Shutdown`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x007986AB` |
| ² | `0x007986B0` |

</details>

`0x0020CD80` returns at once when `0x01F83450` is 0¹. It unregisters the callbacks in the order
1103, 1102, 1101, each only when bit `0x1` of its object's `+0x08` is set², then calls `0x00809950(manager, 0x80)`³. `0x00865660` does the same for `0x02EB3860`:
nothing when it is 0⁴, the unregister only when bit `0x1` of `+0x08` is set⁵,
`0x00809950(object, 0x20)`⁶ and 0 stored at `0x02EB3860`⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0020CD90` |
| ² | `0x0020CD92`, `0x0020CDAC`, `0x0020CDC6` |
| ³ | `0x0020CDE8` |
| ⁴ | `0x00865670` |
| ⁵ | `0x00865672` |
| ⁶ | `0x00865693` |
| ⁷ | `0x00865698` |

</details>

The manager's callback objects have their own destructors, `0x0020C860` (`CCallbackImpl<24>`, 1101,
`+0x20`), `0x0020C880` (`CCallbackImpl<16>`, 1102, `+0x40`) and `0x0020C840` (`CCallbackImpl<152>`, 1103,
`+0x60`). Each calls `SteamAPI_UnregisterCallback` when bit `0x1` of the object's `+0x08` is set. They run
only from the unwind funclets `0x00899B00`, `0x00899B10` and `0x00899B20` of `0x0020C730`, when its construction
is abandoned.

### `code_steam.txt`

At boot `0x0017D990` (from `0x0022A17D`) reads `.\GameData\code_steam.txt` and `.\GameData\data.txt` into
the 16-byte buffers `0x01F7F490` and `0x01F7F4A0`, copying from the eighth character to the first space, or
prints `load failed!`. Neither file is in the shipped archive, and nothing else reads either buffer.

### Without Steam

- `SteamAPI_Init` fails, so `0x01F83450` stays 0: `0x008632B0`, `0x00863240` and `0x00863280` return at once and
  no achievement reaches Steam. Counters, award bits and the Sky Pirate's Den statues still work for the thirty
  tracked achievements; the script and scene awards and Champion of Ivalice leave no record.
- The interface slots stay 0: no language override, no Steam id in the save folder, and no Steam
  controller.
- The overlay and achievement callbacks are never registered; the connection listener is.

## Layouts

<details>
<summary>Show the memory layouts</summary>

The interface context, as `SteamInternal_ContextInit` returns it¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001F3AE0` |

</details>

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` | SteamClient017 |  |
| `+0x08` | `...` | SteamUser019 |  |
| `+0x10` | `...` | SteamFriends015 |  |
| `+0x18` | `...` | SteamUtils009 |  |
| `+0x20` | `...` | SteamMatchMaking009 |  |
| `+0x28` | `...` | STEAMUSERSTATS_INTERFACE_VERSION011 |  |
| `+0x30` | `...` | STEAMAPPS_INTERFACE_VERSION008 |  |
| `+0x38` | `...` | SteamMatchMakingServers002 |  |
| `+0x40` | `...` | SteamNetworking005 |  |
| `+0x48` | `...` | STEAMREMOTESTORAGE_INTERFACE_VERSION014 |  |
| `+0x50` | `...` | STEAMSCREENSHOTS_INTERFACE_VERSION003 |  |
| `+0x58` | `...` | STEAMHTTP_INTERFACE_VERSION002 |  |
| `+0x60` | `...` | STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001 |  |
| `+0x68` | `...` | SteamController005 |  |
| `+0x70` | `...` | STEAMUGC_INTERFACE_VERSION010 |  |
| `+0x78` | `...` | STEAMAPPLIST_INTERFACE_VERSION001 |  |
| `+0x80` | `...` | STEAMMUSIC_INTERFACE_VERSION001 |  |
| `+0x88` | `...` | STEAMMUSICREMOTE_INTERFACE_VERSION001 |  |
| `+0x90` | `...` | STEAMHTMLSURFACE_INTERFACE_VERSION_003 |  |
| `+0x98` | `...` | STEAMINVENTORY_INTERFACE_V002 |  |
| `+0xA0` | `...` | STEAMVIDEO_INTERFACE_V002 |  |

The achievement manager, `0x80` bytes at `[0x01F83450]`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | appId | utilities slot `+0x48`; compared with each callback's first field |
| `+0x08` | `void*` | entries | `0x01DFE410`, `0x198` bytes per entry |
| `+0x10` | `i32` | count | 41 |
| `+0x14` | `i32` | achieved | entries 1-40 achieved |
| `+0x18` | `u8` | received | set by the stats receipt; gates every send |
| `+0x20` | `fn*` |  | 1101 object (handler at `+0x38`) |
| `+0x40` | `fn*` |  | 1102 object |
| `+0x60` | `fn*` |  | 1103 object |

The connection listener at `0x02EACC90`, four `0x20`-byte callback objects, then:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x80` | `i32` | lost | 1 after a disconnect or a failed connect |
| `+0x84` | `i32` | connected | 1 at start and after a connect |
| `+0x88` | `i32` | failures | disconnects and failed connects since the last connect |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Fact | Value |
|---|---|
| `steam_api64.dll` imports | 9: `SteamAPI_Init`, `RestartAppIfNecessary`, `RunCallbacks`, `RegisterCallback`, `UnregisterCallback`, `GetHSteamPipe`, `GetHSteamUser`, `SteamInternal_CreateInterface`, `SteamInternal_ContextInit` |
| call sites | `RegisterCallback` 8, `UnregisterCallback` 11 (3 of them tail jumps), `ContextInit` 25, `GetHSteamPipe` 2, each of the others 1 |
| interface version strings | 21, `0x00903538`-`0x009037A0` |
| app id | 595520 (`0x91640`) |
| log strings | `0x00906400`-`0x00906490` |

</details>

## State

<details>
<summary>Show the state it keeps</summary>

| Address | What |
|---|---|
| `0x01DFE0D0` | the interface context record |
| `0x01F83450` | the achievement manager, 0 without Steam |
| `0x02EB3860` | the overlay callback object |
| `0x02EACC90` | the connection listener |
| `[0x02EA5368] + 0x1D` | overlay active |

</details>

## Modding notes

- A build that must run without Steam needs no patch: the null manager already turns every award off.
- `RestartAppIfNecessary` is called even when `SteamAPI_Init` fails, and a true result always ends the
  process; patching the `jz` at `0x00798144` keeps it running.
- Sending an achievement from code works only after the stats receipt; call `0x008632B0(entry)` after
  `[0x01F83450] + 0x18` is set.

## Related

- [Achievements](achievements.md): what the game awards through Steam.
- [Save file format](../Saving-Loading-And-Settings/save-file-format.md): the save folder built with the Steam id.
- [Languages](../Saving-Loading-And-Settings/languages.md): the Language setting the Steam language overrides.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): the settings object and `0x001DF340`.
