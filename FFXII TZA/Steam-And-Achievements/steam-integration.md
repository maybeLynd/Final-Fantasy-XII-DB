---
title: "Steam integration: how the game starts and pumps Steam, the interfaces and callbacks it uses, and what it does without Steam"
kind: "system"
category: "Steam and achievements"
addresses: "007980A0, 01DFE0D0, 001F3E10, 001F3AE0, 0020CD30, 0020C730, 01F83450, 0020CCC0, 008655E0, 008655A0, 007A0810, 008653B0, 00865510, 007A3110, 0020C940, 0020C8C0, 0020CB20, 0020CE60, 0020CE10, 0020CD80, 00865660, 007A0C60, 001F3ED0, 0017D990, 00798FF0"
---

## What the player sees

When Steam's relaunch check asks for it, the game exits at start-up. Under Steam, the overlay works, achievements
unlock, the game's language follows the language set for it in Steam, and saves go to a folder named after
the Steam account. Without Steam the game still runs: achievements are kept only in the save, and the
language and save folder fall back to their own settings.

## How it works

### Start-up order

The main routine `007980A0` does this before it loads any setting:

1. `SteamInternal_ContextInit(01DFE0D0)` (`00798116`) returns the interface context. When its `+0x18`
   (the utilities interface) is already filled, step 2 is skipped.
2. `SteamAPI_Init` (`00798123`). On failure the game jumps to step 5: no achievement manager and no overlay
   listener are made.
3. `0020CD30` builds the achievement manager (`0079812D`).
4. `008655E0` registers the overlay callback (`00798132`).
5. `SteamAPI_RestartAppIfNecessary(0x91640)` (`0079813C`), app id 595520. On true the process calls
   `exit(1)` (`0079814B`).
6. `007A0810` builds the connection listener (`00798152`).

Later in the same routine it calls `001F3ED0`, which prints the Steam user id (`007981EA`), reads the
settings (`001DED50`, `0079826B`) and then applies the Steam language (`007A0C60`, `00798272`).

### The interface context

`01DFE0D0` holds the context's init callback `001F3E10`. That callback zeroes the slots and, when
`SteamAPI_GetHSteamPipe` returns a pipe, calls `001F3AE0`. `001F3AE0` creates `SteamClient017` through
`SteamInternal_CreateInterface` and asks that object for each interface by its version string, stopping at
the first that fails; the slot order is in Layouts.

All 25 calls through `SteamInternal_ContextInit` read one of five slots from the context they get back:

| Slot | Interface | Sites | What the game calls |
|---|---|---:|---|
| `+0x08` | `SteamUser019` | 4 | slot `+0x10` for the user id (`001F3ED0`); slot `+0x08`, a logged-on test (`0020CCC0`) |
| `+0x18` | `SteamUtils009` | 2 | the start-up test (`00798116`); slot `+0x48`, the app id (`0020C7FD`) |
| `+0x28` | `STEAMUSERSTATS_INTERFACE_VERSION011` | 17 | the achievement calls below |
| `+0x30` | `STEAMAPPS_INTERFACE_VERSION008` | 1 | slot `+0x20`, the game language (`007A0C94`) |
| `+0x68` | `SteamController005` | 1 | stored at `02EA9508` and initialised (`0079791D`) |

The other sixteen interfaces are fetched and never called.

### The achievement manager

`0020CD30` allocates `0x80` bytes, calls `0020C730(object, 01DFE410, 41)` and stores the result at
`01F83450`. `0020C730`:

1. registers callbacks 1101, 1102 and 1103 (`SteamAPI_RegisterCallback`, `0020C78C`-`0020C7EC`);
2. stores the utilities interface's slot `+0x48` result, the app id, at `+0x00`; every handler compares it
   with the callback's first field and ignores a mismatch;
3. stores the 41 static achievement records as its entry table and calls `0020CCC0`, which, when the user
   interface's slot `+0x08` returns true, calls the stats interface's slot `+0x00` (the stats request).

### Callbacks

Eight registrations, each with an RTTI-named `CCallback<owner, event>` object and its handler:

| Id | Event | Handler | Effect |
|---:|---|---|---|
| 1101 | `UserStatsReceived_t` | `0020C940` | the stats receipt, below |
| 1102 | `UserStatsStored_t` | `0020CB20` | logs `Stored stats for Steam` or `RequestStatsd - failed, %d` |
| 1103 | `UserAchievementStored_t` | `0020C8C0` | counts one more achieved; at 40, awards entry 0 if Steam has it unachieved (`0020CE10`) |
| 331 | `GameOverlayActivated_t` | `008655A0` | logs the overlay state and stores it in byte `+0x1D` of the application object `[02EA5368]` |
| `0x65` | `SteamServersConnected_t` | `00865560` | listener `+0x84` = 1, `+0x88` = 0 |
| `0x67` | `SteamServersDisconnected_t` | `00865570` | listener `+0x88` += 1, `+0x80` = 1, `+0x84` = 0 |
| `0x66` | `SteamServerConnectFailure_t` | `00865570` | the same body |
| `0x2C0` | `SteamShutdown_t` | `00865590` | listener `+0x80` and `+0x88` = 0 |

The first three belong to the manager, the overlay one to the object at `02EB3860`, and the last four to
the listener at `02EACC90` (`008653B0`).

### The pump

`007A3110` is slot 0 of Phyre's `PWindowWin32Base` and `PWindow` vtables (`01CB2468`, `01CB2480`). It
returns 9 when byte `+0x69` of `[02EA5368]` is set, which the window's close handler `00798FF0` does for
close codes 1 and 2 (`00799306`). Otherwise it calls `SteamAPI_RunCallbacks` (`007A312E`), the only call
of that import, and then `007A2440`. Steam callbacks therefore run once per window pump, on that thread.

### The stats receipt

`0020C940`, on a matching app id:

1. A result other than 1 logs `RequestStats - failed, %d` and changes nothing.
2. It sets manager `+0x18` (stats received) and zeroes the achieved count `+0x14`.
3. For entries 1-40 it asks the stats slot `+0x30` (GetAchievement) to write each entry's `+0x190`, counts
   the achieved ones, and copies the `name` and `desc` display attributes (slot `+0x60`) into `+0x10` and
   `+0x90`.
4. When all forty are achieved it reads entry 0 and, if Steam has it unachieved, calls slot `+0x38` and
   `+0x50` (SetAchievement, StoreStats).

Slot names follow the Steamworks interface order; the arguments match it (`+0x30` takes a name and a flag
address, `+0x60` a name and a key).

### Awards

`0020CE60(manager, entry)` (reached from `008632B0`) and the by-scene award `0020CB50` mark the entry's
`+0x190`, then call SetAchievement and StoreStats only when `+0x18` is set. An award made before the receipt
stays local, and the receipt then overwrites `+0x190` with Steam's value.

### The connection listener and closing the window

`007A0810` builds the listener once and registers `008B7DB0` with `atexit` to unregister it (`00865490`).
`00865510` returns 1 when its `+0x80` is 1, `+0x84` is 0 and `+0x88` is at most 1. The close handler
`00798FF0`, for an ordinary close request: in full-screen mode (setting 2 = 1) it quits at once; otherwise
the first close request while `00865510` returns 1 is ignored (`02EACD28`), and any other asks for
confirmation with a message box (texts `0x7836` and `0x7835`).

`0019A510(id)` loads those texts from the executable's string table (`007991FE`, `00799234`): in each
module of the ATL module list it finds block `id / 16 + 1` of resource type 6, and `0019A5B0` steps over
`id & 0xF` length-prefixed strings in the block, returning 0 for an empty or missing string.

### Language and user id

`007A0C60` returns at once without the apps interface. Otherwise it maps Steam's game language to the
Language setting through `001DF340(settings, 0, value)`: `japanese` 0, `english` 1, `french` 2, `german`
3, `italian` 4, `spanish` 5, `koreana` 6, `tchinese` 7, `schinese` 8; any other string leaves it.

`001F3ED0` formats the Steam id as a decimal string (`%llu`) when the user interface exists and leaves the
string empty otherwise. The save folder appends it ([save file format](../Saving-Loading-And-Settings/save-file-format.md)).

### Teardown

After the message loop ends, `007980A0` calls `0020CD80` (`007986AB`), which unregisters the manager's
three callbacks, frees it and stores 0 at `01F83450`, and `00865660` (`007986B0`) for the overlay object.
The game imports no `SteamAPI_Shutdown`.

The manager's callback objects have their own destructors, `0020C860` (`CCallbackImpl<24>`, 1101,
`+0x20`), `0020C880` (`CCallbackImpl<16>`, 1102, `+0x40`) and `0020C840` (`CCallbackImpl<152>`, 1103,
`+0x60`). Each calls `SteamAPI_UnregisterCallback` when bit 0 of the object's `+0x08` is set. They run
only from the unwind funclets `00899B00`, `00899B10` and `00899B20` of `0020C730`, when its construction
is abandoned.

### `code_steam.txt`

At boot `0017D990` (from `0022A17D`) reads `.\GameData\code_steam.txt` and `.\GameData\data.txt` into
the 16-byte buffers `01F7F490` and `01F7F4A0`, copying from the eighth character to the first space, or
prints `load failed!`. Neither file is in the shipped archive, and nothing else reads either buffer.

### Without Steam

- `SteamAPI_Init` fails, so `01F83450` stays 0: `008632B0`, `00863240` and `00863280` return at once and
  no achievement reaches Steam. Counters, award bits and the Sky Pirate's Den statues still work.
- The interface slots stay 0: no language override, no Steam id in the save folder, and no Steam
  controller.
- The overlay and achievement callbacks are never registered; the connection listener is.

## Layouts

The interface context, as `SteamInternal_ContextInit` returns it (`001F3AE0`):

```
+0x00  SteamClient017                         +0x58  STEAMHTTP_INTERFACE_VERSION002
+0x08  SteamUser019                           +0x60  STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
+0x10  SteamFriends015                        +0x68  SteamController005
+0x18  SteamUtils009                          +0x70  STEAMUGC_INTERFACE_VERSION010
+0x20  SteamMatchMaking009                    +0x78  STEAMAPPLIST_INTERFACE_VERSION001
+0x28  STEAMUSERSTATS_INTERFACE_VERSION011    +0x80  STEAMMUSIC_INTERFACE_VERSION001
+0x30  STEAMAPPS_INTERFACE_VERSION008         +0x88  STEAMMUSICREMOTE_INTERFACE_VERSION001
+0x38  SteamMatchMakingServers002             +0x90  STEAMHTMLSURFACE_INTERFACE_VERSION_003
+0x40  SteamNetworking005                     +0x98  STEAMINVENTORY_INTERFACE_V002
+0x48  STEAMREMOTESTORAGE_INTERFACE_VERSION014 +0xA0 STEAMVIDEO_INTERFACE_V002
+0x50  STEAMSCREENSHOTS_INTERFACE_VERSION003
```

The achievement manager, `0x80` bytes at `[01F83450]`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `i32` | appId | utilities slot +`0x48`; compared with each callback's first field |
| `08` | `void*` | entries | `01DFE410`, `0x198` bytes per entry |
| `10` | `i32` | count | 41 |
| `14` | `i32` | achieved | entries 1-40 achieved |
| `18` | `u8` | received | set by the stats receipt; gates every send |
| `20` | `fn*` | 1101 object (handler at +0x38) |  |
| `40` | `fn*` | 1102 object |  |
| `60` | `fn*` | 1103 object |  |

The connection listener at `02EACC90`, four `0x20`-byte callback objects, then:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `80` | `i32` | lost | 1 after a disconnect or a failed connect |
| `84` | `i32` | connected | 1 at start and after a connect |
| `88` | `i32` | failures | disconnects and failed connects since the last connect |

## Shipped data

| Fact | Value |
|---|---|
| `steam_api64.dll` imports | 9: `SteamAPI_Init`, `RestartAppIfNecessary`, `RunCallbacks`, `RegisterCallback`, `UnregisterCallback`, `GetHSteamPipe`, `GetHSteamUser`, `SteamInternal_CreateInterface`, `SteamInternal_ContextInit` |
| call sites | `RegisterCallback` 8, `UnregisterCallback` 11 (3 of them tail jumps), `ContextInit` 25, `GetHSteamPipe` 2, each of the others 1 |
| interface version strings | 21, `00903538`-`009037A0` |
| app id | 595520 (`0x91640`) |
| log strings | `00906400`-`00906490` |

## State

| Address | What |
|---|---|
| `01DFE0D0` | the interface context record |
| `01F83450` | the achievement manager, 0 without Steam |
| `02EB3860` | the overlay callback object |
| `02EACC90` | the connection listener |
| `[02EA5368] + 0x1D` | overlay active |

## Modding notes

- A build that must run without Steam needs no patch: the null manager already turns every award off.
- `RestartAppIfNecessary` is called even when `SteamAPI_Init` fails, and a true result always ends the
  process; patching the `jz` at `00798144` keeps it running.
- Sending an achievement from code works only after the stats receipt; call `008632B0(entry)` after
  `[01F83450] + 0x18` is set.

## Related

- [Achievements](achievements.md): what the game awards through Steam.
- [Save file format](../Saving-Loading-And-Settings/save-file-format.md): the save folder built with the Steam id.
- [Languages](../Saving-Loading-And-Settings/languages.md): the Language setting the Steam language overrides.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): the settings object and `001DF340`.
