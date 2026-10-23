---
title: "Event scenes: the scene managers, loading, starting, waiting on and disposing a scene, movies and skips"
kind: "system"
category: "Scripts and script commands"
addresses: "0x02098E10, 0x02099DE2, 0x00264170, 0x0026A5A0, 0x001C3370, 0x00351880, 0x00351C90, 0x003522C0, 0x00353080, 0x003541B0, 0x00354B20, 0x00355970, 0x00356D40, 0x00332130, 0x00332190, 0x0032ED70, 0x0032F1B0, 0x00267210, 0x022C6E48, 0x022C6D20, 0x0034C9A0, 0x0026B750, 0x00863240, 0x003567F0, 0x00356050, 0x0035B840, 0x0035B7D0, 0x0035B8D0, 0x0035B740, 0x00357300, 0x00184860, 0x00360980, 0x00360710, 0x003604A0, 0x0034DB30, 0x022CB730, 0x02099011, 0x003B08F0, 0x00360670, 0x00360650"
---

## What the player sees

A story scene: the screen fades, the party vanishes and the scene's own actors take the stage, the camera takes
over, characters talk and move on their own, and at the end control comes back. Some scenes are pre-rendered movies.
Many can be skipped from the pause menu.

## How it works

### Scene managers and the two gates

A scene runs in its own actor manager, 1, 2 or 3, beside the zone's manager 0 (`0x02098E10 +
m × 0x288`). Every scene verb takes a slot argument and uses manager `clamp(slot + 1, 1, 3)`; the
plain-named forms (`eventread`, `eventplay`, `eventsync`) fix the slot at 0, manager 1.

Two gates sit in almost every scene verb. `0x00264170` returns the event switch byte `0x02099DE2`,
which area initialisation sets to 1 and `system_seteventexecstatus` (`0x141`) writes through
`0x0026A5A0`; while it is 0 the load, play and sync verbs do nothing. `0x001C3370` returns byte
`+0x10D4` of the application object `0x00796E20` returns, written only to 0 by the constructor
`0x00792350` and read otherwise by the auto-test walker `0x001C2F50`: an auto-test switch that is
never set in retail, so scene verbs always proceed past it.

### Loading, the start hold, playing and disposing

| Verb | Id | Callbacks | What it does |
|---|---|---|---|
| `eventread_e8(slot, id)` | `0x00E8` | begin `0x00351880`, poll `0x00351C90`, result `0x003522C0` | the begin stores both and prefetches `0x001D6A70(id, slot)`; the poll waits while manager `m` is active (`+0x10` bit 0) and busy (`+0x13`); the result queues the load `0x0032FC30(m, id)` and sets the hold `0x0032ED70(m)` |
| `eventread(id)` | `0x00E7` | result `0x00353080` | slot 0, the same load after `0x00314D40(1)` |
| `eventreadsync_ea(slot)` | `0x00EA` | begin `0x00353A10`, poll `0x003541B0` | waits while `0x0032F6C0(m)` reports loads pending, calling `0x00314D40(1)` each poll |
| `eventplay_ec(slot)` | `0x00EC` | result `0x00354B20` | releases the hold `0x00332130(m)`, then `0x001EC680(m)`, `0x0020AF10(m, −1)` and `0x001EC600()` |
| `eventsync_ee(slot)` | `0x00EE` | begin `0x00353A10`, poll `0x00355970` | waits while `0x00267210(m)` is non-zero: manager active or busy |
| `eventstartsync(slot)` | `0x0165` | begin `0x0034F3C0`, poll `0x0034F6F0` | the begin pushes a 0 flag first; waits while manager `+0x10` has bit 1 |
| `eventstartsync_166(slot, flag)` | `0x0166` | begin `0x0034E460`, poll `0x0034EAB0` | waits while `+0x10` has bit 1, or bit 0 while the flag is set and bit 7 is set |
| `eventstartsync_167()` | `0x0167` | begin `0x0034FC50`, poll `0x0034F6F0` | the begin pushes two zeros: manager 1, flag 0 |
| `eventdispose_f2(slot)` | `0x00F2` | begin `0x00356D40`, poll `0x0033F150` | `0x00332190(m)`: marks `0x022C6D20[m]` and, when the manager is active, requests its teardown through `0x0026A5F0`; a negative slot means the issuer's own manager, and the poll halts the issuer (`+0x14` bit 6) when it disposed itself |

The load request `0x0032FC30` queues the scene's files, and `0x0032ED70` sets bit 0 of the manager's
pending-load mask at `0x022C6E48 + m × 8`. That bit is the start hold: the files are loaded when
every other bit is clear, but the scene does not start until `eventplay` calls `0x00332130`, which
clears bit 0 and manager `+0x11` bit 3 and, when the mask is now empty, runs the finaliser
`0x0032F1B0(m)`.

The finaliser binds the payload's lighting sections (`0x0037AA90`), activates the
manager (`0x0026CE60`, which posts the start entry's request list through `0x00266C50`) and the first
field pass then warms the start entry up ([script requests](script-requests.md)).

`startscene(n)` (`0x011B`, `0x0034C9A0`) reports the pair (scene id, n) to the achievement hook
`0x00863240` and calls `0x0026B750(n)`: it resets the frame counter `0x022C252C`, stores `n` at
`0x022C2538`, pushes the scene id into the event-slot panel through `0x0020AF10` and runs the debug
cutscene JSON hook `0x001EC600`, which returns at once in retail.

### Movies

| Verb | Id | Callbacks | Effect |
|---|---|---|---|
| `moviestandby(id)` | `0x0368` | `0x003567F0` / `0x00356050` / `0x00356460` (→ `0x0035B840(id, manager)`) | waits until `0x0035B7A0` says no fade or load is active, then denies user control, sets the arena mode to 1 (`0x0037B450(1)`, `0x0035B877`, [resource arena](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md)), raises busy bit 16, frees `0x022C8058`, opens the movie (`0x001848A0`) and dismisses the loading page `[0x01F82CD8]` through its tail jump to `0x00183070` (`0x0035B8C4`, [game application](../Engine-Core/game-application.md)) |
| `movieplay(v)` | `0x036A` | `0x00356D20` (pops a value it ignores, then `0x0035B7D0`) | switches off the field systems (`0x00358750` and its siblings, `0x002E1CD0(0, 0)`, `0x002E1C40(0, 4)`) and starts playback `0x001848C0` |
| `getmoviestatus` | `0x036F` | `0x00340870` (→ `0x0035B740`) | returns the player's state `0x00184860` when it is 1, 2 or 3, else 0, and pumps the opening player (`0x00184880`) while it is 1 |
| `moviecancel` | `0x036E` | `0x0033FEC0` (→ `0x0035B720`) / `0x00357300` / `0x0033FA20` | asks the player to stop, waits while the status is 1 to 3, then ends |
| `movieend` | `0x036D` | `0x0033FA20` → `0x0035B8D0` | stops the player, frees the buffer, clears busy bit 16 and switches the field systems back on |

The player object at `0x01F81218` keeps its state at `+4`: 0 idle, 1 opening, 2 ready, 3 playing,
4 the last 233 ms, 5 ending, 6 the skip fade. A script therefore reads "finished" from the last
frames onward.

### Skips

Skip slots are 16-byte entries at `0x022CB730`, indexed `index + manager × 8`: `+0` bit, `+1` mask
index, `+2` state, `+4` record id, `+8` executed, `+0xC` armed. `skipstart(i)` (`0x051A`,
`0x0034D3A0` → `0x00360980`) clears user-control denials 13 and 19, sets state 1 and armed, sets the
bit in `0x022CB9C0` and clears it in `0x022CB9D8`. `skipcheck(i)` (`0x051C`) returns the executed word
through `0x003604A0`.

`skipexec(i)` (`0x0539`, `0x0034ECF0` → `0x00360710`) runs only when the manager's skip mask is
clear and the entry is armed: state 2, executed 1, busy bit 15, the teardown of the manager's
sound, effects and presentation, and finally the mask bit `0x0026A5B0(manager, 1, i)` that ends
the waits ([native commands](native-commands.md)).

Part of that teardown, `0x003B08F0`, also run when a skip ends, walks the 36-entry table of 24-byte
effect records at `0x02EBEC00` and stops at the first entry whose first dword is 0. It frees every
entry that is not marked to keep (`+0x13` bit 0) and whose type byte `+0x10` is not `0x63`,
through `0x003B0770` and `0x0024EE60`. `0x003B0770` moves the later entries down one place, so after a
free the walk examines the same slot again.

`0x00360670` reports whether any skip of mask index 1 to 3 has executed (`0x022CB9DC` to
`0x022CB9E4`); while it does, or while byte `0x022CB726` is set (`0x003603C0`), the character sound
player `0x002E9D90` behind the `charseplay` verbs plays nothing.

`skipend(i)` (`0x051B`, begin `0x0034D820`, poll `0x0034DB30`) marks an entry whose state is not 2
(`0x00360650`) in its scratch and releases it at once (`0x00360A20`); otherwise it waits through four
stages (`0x0025C070`; `0x003608D0`, which starts the track `skipexec` recorded, or only sets its volume
when it already plays
([music](../Sound-And-Music/music.md)); `0x00360D60`; the resource queue idle through `0x002F1A30` and
`0x0032E520`), releases, and waits one more stage on `0x00229EB0`.

## Layouts

Globals:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x2098E10` | `SceneManager[5]` | managers | manager `m` at `+ m × 0x288`, five slots ([actor managers](../Characters-And-Objects/actor-managers.md)); 0 is the zone, 1 to 3 the scenes |
| `+0x22C6E48` | `u64[4]` | pendingLoad | per manager; bit 0 is the start hold |
| `+0x22C6D20` | `u8[4]` | unloadRequest | per manager |
| `+0x22CB730` | `SkipEntry[32]` | skips | entry `i + m × 8`, stride 16 |
| `+0x22CB9C0` | `u32[6]` | skipArmed | per mask index |
| `+0x22CB9D8` | `u32[6]` | skipExecuted | per mask index |
| `+0x1F81218` | `MoviePlayer` | movie | the movie player |
| `+0x2099DE2` | `u8` | eventSwitch | 0 stops the scene verbs |

SceneManager (stride `0x288`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x008` | `void*` | actors | actor table: `u32` count, then actor pointers from its `+8` |
| `+0x010` | `u8` | flags | bit 0 active |
| `+0x011` | `u8` | loadFlags | bit 3 loading |
| `+0x013` | `u8` | busy | non-zero while busy |
| `+0x1D6` | `u16` | windowCount | entries in the ordinal window |
| `+0x1DE` | `u16` | windowFirst | first ordinal of the window |
| `+0x1E0` | `i32` | lockCount | world-lock takes |
| `+0x201` | `u8` | skipMask | one bit per skip index (`0x02099011 + m × 0x288`) |

SkipEntry (16 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | bit | bit index in the masks |
| `+0x01` | `u8` | maskIndex | which mask word |
| `+0x02` | `u8` | state | 1 started, 2 executed |
| `+0x04` | `u32` | recordId | record id |
| `+0x08` | `u32` | executed | read by `skipcheck` |
| `+0x0C` | `u32` | armed | set by `skipstart` |

MoviePlayer:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` | state | 0 idle, 1 opening, 2 ready, 3 playing, 4 last frames, 5 ending, 6 skip fade |

## Shipped data

| Fact | Value |
|---|---|
| scene managers | 3 (1 to 3) beside the zone's manager 0 |
| `startscene` uses | 3,789 |
| `eventread_e8` / `eventplay_ec` / `eventsync_ee` uses | 596 / 567 / 553 |
| skip verbs | `skipstart` 292, `skipend` 291, `skipcheck` 237, `skipexec` 19 |
| movie status values a script sees | 1 opening, 2 ready, 3 playing; 0 otherwise |

## Operations

Per scene: load (one request), wait, release the hold, run, wait for the manager to idle, dispose.

## State

The three scene managers' active, busy and loading bits, the pending-load masks, the skip table and masks, and
the movie player state.

## Modding notes

- A scene cannot start before `eventplay` clears the hold, however early its files finish loading.

## Related

- [The party during scenes](party-during-scenes.md): hiding, capturing and the summon group.
- [The world lock](world-lock.md): what holds everyone else still during a talk or scene.
- [Native commands](native-commands.md): the skip mask that ends waits.
