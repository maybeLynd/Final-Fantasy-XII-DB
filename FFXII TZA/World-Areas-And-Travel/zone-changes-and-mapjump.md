---
title: "Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map"
kind: "system"
category: "World, areas and travel"
addresses: "00354D00, 00355350, 00314440, 003145E0, 00314020, 0032FC30, 0032FCA0, 003321E0, 002620E0, 0034AD70"
---

## What the player sees

You walk into the glowing edge of an area, or a scene ends and the story moves the party somewhere
else. The screen fades to black, the next area loads, the party appears at that area's entrance and the
screen fades back in. While the screen is dark nothing moves and the menu cannot be opened.

The same thing happens when a scene moves the party, when a gate crystal sends you to another region
and when a save is loaded. A second jump asked for while one is already under way is ignored, and a
scene can hold a jump back until it is ready to let the party go.

## How it works

### The script asks with the mapjump verb

A zone change starts as the script verb `0x8D`, which the script sources call `mapjump(map, entrance,
mode)`. Its handlers are read from the family-0 verb table at `01EED700`, 32 bytes per verb: record
`0x8D` holds the Start handler `00354D00` at `+8` and the Poll handler `00355350` at `+0x10`; record
`0x8E` has a zero first slot, so the verb has no End handler.

The Start handler `00354D00` pops the three arguments in reverse into the verb's context words (`ctx[3]`
= mode, `ctx[2]` = entrance, `ctx[1]` = map). When byte `02064AD3` (`00229EA0`) is 2 it calls
`001831A0`. It then calls `005C5230`, which is `xor eax, eax; ret`, so `ctx[0]` is always 0 and the
handler always returns 0.

The Poll handler `00355350` runs every frame. In state 0 it does the following, in order:

1. Takes the current field context `c = 002640C0()` (`[02099D70]`).
2. When `c+0x28` is 0 and byte `c+0x16` is 0 it waits (returns 1) while `02099DB8` (`00264180`) is
   non-zero or while `00264830` finds a manager with `+0x10` bit 0 and `+0x200` bit 2 set (the jump
   lock).
3. Calls `001D6AE0(map)`, a guarded indirect call on the file-cache object.
4. Calls `00314440(map, entrance, mode, 1)`. A non-zero result means the resource queue is busy; the
   poll returns 1 and tries again next frame.
5. Sets `ctx[0]` = 1.

In state 1 the poll returns 1 while `c+0x28` is 0 and 0 (done) once it is non-zero. `+0x28` is the index
of the actor manager the script runs in: 0 for the zone's own scripts, 1 to 3 for a scene. So a jump
asked for by a scene completes and the scene continues, while a jump asked for by the zone's own
script waits until the jump tears that script down. State 2 calls `002EF890` and returns done; nothing
in the Start handler produces it.

### The request

`00314440(map, entrance, mode, nonblocking)` is the one funnel every jump passes through:

```c
if (00408B00() == 0 && map == 0) map = 0xC;          // byte 02B62DB9: input channel mode
if (01EED064 < 0) {                                   // no jump pending
    r = 003145E0(map, entrance, mode, nonblocking);   // staging
    if (nonblocking && r != 0) return r;              // resource queue busy: caller retries
    0026A5F0(0);                                      // request managers 0..3 for reinitialisation
    if ((mode & 1) == 0 && 002EFD20(2) == 0) {        // fade slot 2 idle
        002EFE40(6); 002EFE50(0xFF);
        002EFA70(2, ~(mode * 2) & 8, 0, (mode >> 1) & 1);
    }
    002E1C40(0, 2); 00254AC0(); 00183240(0);
    001D6C40(01EED064);                               // file cache: "[FileCache] OnMapJumpBefore (%d)"
    00182D80();
}
return 0;
```

`mode` bit 0 set means no fade-out from this request; bits 1 and 2 shape the fade call. A request made
while `01EED064` is non-negative is dropped without error. `0026A5F0(0)` ORs bits 0 to 3 into the
manager request mask `02099ABC` (requesting manager 0 also requests 1, 2 and 3).

Callers of `00314440`: the mapjump poll (`003553CF`), `00280140` (`0028027C`), `00394130`
(`003941FC`), `0050C8A0` (`0050C8B6`), the load-completion callbacks `00331920` (`0033194E`,
`0033197F`) and `003318C0` (`003318E5`, `00331914`), and `00319F50` (`0031A0F1`).

### Staging and the transition record

`003145E0(map, entrance, mode, nonblocking)` runs in this order:

1. `0032E520(0)` drains the resource queue; with `nonblocking` it calls `0032E520(1)` and returns 1
   when the queue is busy.
2. `0026E0D0(0, 0)`, busy bit 12 set (`003601B0(0xC)` at `0031463E`), `0026A5F0(1)`, `(2)`, `(3)`.
3. The transition record in the persistent payload (`002EF2B0`): `+0x104C` = old `+0x1044`; `+0x1044`
   = map, also copied to `01EED064`; `+0x1050` = old `+0x1048`; `+0x1048` = entrance; `+0x1054` = mode;
   `+0x1058` = `00264F90(map)`, the persistence group; `+0x105C` = map; `+0x1062` bit 5 cleared.
4. `022C2540` = 0; `002EFA70(3, 0, 1)` (fade slot 3).
5. When `01EED064` is non-negative: `s = 00236760()` (bit 12 of `[02EBF190]+4`). For a destination
   other than `0xC`, when `s` is 0 the map id is written to the runtime buffer at `002EF640() + 0x4E664`
   and `003C8670()` runs. For destination `0xC`: `00287D00(0)` and `01E0C3EC` = 1.
6. Autosave: when `0020E500(map, 00265270(), entrance)` returns non-zero, `00229B40`, `005844A0`,
   `00584580` and `00583260` capture the runtime state and open the save writer.

Field `0xC` is the title map (`ttl_a01`, see the file table below): a request for map 0 becomes `0xC`
when the input channel mode is 0, and staging `0xC` skips the runtime-buffer write.

`00314530` is the restore path: it requests managers 1, 2, 3 and 0, sets `+0x1062` bit 5, copies
`+0x1044` to `01EED064` and `+0x105C`, clears `022C2540`, starts fade slot 2 with `002EFA70(2, 0, 0, 0)`,
sets `022C2528` = 1 and notifies the file cache. `003145E0` is also called by the area initialisation
`00266D10` (`00267127`). `00314D00(v)` writes bit 2 of `+0x1062`.

### The tick tears the old zone down and starts the load

`00314020`, the simulation tick, runs this before any actor:

1. `0025BFB0` drains the request mask `02099ABC`: when bit 0 is set, `0026CE60(m)` reinitialises every
   requested manager from 4 down to 0 and the party roster `0209A1F0` to `0209A208` is cleared; then
   every requested manager is unloaded with `002628B0(m)` and its bit cleared.
2. `01EED060` is reset to -1 when non-negative.
3. When `01EED064` is non-negative: two console lines (`00D103E0`, `00D10420`), `0032FC30(0, map)`,
   then `01EED064` = -1.

`0032FC30(0, map)` calls `003EA6E0(map, byte 022C6D1D)`, then `0032FCA0(0, map)`, `0025D4D0(0)`, and sets
bit 0 of `022C6E48`, the start hold. A branch guarded by `005C5230(5)` is dead in this build.

That dead branch calls `003319D0(map)`. It takes the zone's `.ebp` path (namespace 5, index
`map * 3`) and makes four sibling paths with `00331F50`, which replaces every occurrence of one
substring with another: the folder `global` becomes `entry`, `entry`, `treasure` or `icon` and the
extension `eps`, `ard`, `eps` or `icn`. Each file that exists (`0032E400(0xFF, path)`) is read into
a block labelled `POSENT`, `MAPARD`, `TREENT` or `NV_ICON` with the source name `atelload.c`
(`0036C750` cuts a path to its file name), with the completions `003320E0`, `003320D0`,
`00332110` and `00332100`.

### Where the files come from

`0032FCA0(m, ctx)` unloads the manager (`002628B0`), resets it (`0032ED80`), stores `ctx` at
`022C6D28[m]` and `022C6D40[m]`, and chooses the archive namespace and base index:

| Manager | Namespace | Base index | Used for |
|---:|---:|---|---|
| 0 | 5 | `ctx * 3` | the zone |
| 1 to 3 | 8 | `ctx * 4` | event scenes |
| 4 | 1 | `ctx + 0x6B` | the fifth manager |

It then queues the asynchronous loads, each setting a bit of the manager's pending mask
`022C6E48 + m*8` that its completion callback clears:

| Load | Pending bit | Condition |
|---|---:|---|
| `base + 2` (callback `00331760`, buffer `022C6E98[m]`) | `0x1000` | managers 1 to 4 |
| `base + 1` (callback `003302B0`, buffer `022C6E70[m]`) | `0x2000` | managers 0 to 3 |
| `base + 3` from namespace 8 (callback `00331820`) | `0x8000` | managers 1 to 3 |
| `base + 3` from namespace `0x25` (callback `003317C0`) | `0x4000` | managers 1 to 3 |
| the primary payload, `00330310(m, ctx, ns, base)` (callback `003304A0`) | `0x20000` | all |

Pending bit 0 is a start hold, not a load. `0032ED70(m)` sets it, `0032F6C0(m)` reads the mask without
it, and `00332130(m)` clears it; when the mask thereby becomes 0, `00332130` clears manager `+0x11` bit 3
and calls `0032F1B0(m)` to finalise the manager. For the zone, `00378120` (called by `003775D0` at
`003776DD`) binds the new area's navigation data and then calls `00332130(0)`, so the zone's actors and
scripts cannot start before its navigation exists.

### The busy mask

`022CB720` is a 32-bit mask of reasons the game is busy: `003601B0(n)` sets bit `n`, `003601C0(n)`
clears it, `00360360(n)` tests it, `00360100` and `00360370` zero it. A sweep of every call site, with
the bit loaded into `ecx` before the call:

| Bit | Set by | Cleared by |
|---:|---|---|
| 3 | `00228130` (`0022826D`) | `00228130` (`00228187`) |
| 6 | `003615F1` | `00361469` |
| 7 | `003321E0` (`00332244`): a manager has a pending load | `003321E0` |
| 10 | `0037C4D0` | `0037C6C8` |
| 11 | `002628B0` (`00262BA8`), the manager unload | `002620E0` (`002621AD`) |
| 12 | `003145E0` (`0031463E`), `002678C0` (`002678F5`) | `002620E0` (`002621BC`), `0025D580` (`0025D5B3`) |
| 13 | `00344CAE`, `0034571B` | `00345169`, `003464F2` |
| 15 | `00360710` (`003607E1`, bit computed at run time) | `003603F0` (`00360424`, `00360440`), `00360A20` (`00360A36`) |
| 16 | `0035B840` (`0035B881`) | `0035B8FC` |
| 18 | `00342C90` (`00342C99`) | `00343325` |
| 19 | nine party-command verb bodies (`0034C3B1`, `0034CCD9`, `0034CE3B`, `0034D542`, `00350184`, `00350D17`, `00351A66`, `003521C8`, `00352B05`) | `0034C398`, `0034CE18`, `003506B4` (bit `0x13` plus a selector), `0034D465` |

`003321E0` sets bit 7 when any of the five pending masks has a bit other than bit 0 set and clears it
otherwise. `00360120`, called from the main loop, runs `003321E0` and, when the whole mask is 0 and byte
`022CB72A` or `022CB72B` is set, runs the resume routine `003601D0`. `002628B0` zeroes the mask through
`00360100` (`00262B9E`); the boot routine `0022A0B0` calls `00360370` (`0022A39E`).

### The zone is ready

`0025D9E0`, the per-manager field pass, calls `002620E0(manager)` at `0025DB7D` and `0025DC27`. Only
manager 0 gets past its first test (`+0x28` == 0). On the first pass for a load (`+0x10` bit 2 clear) it
runs the start work once: `00259B30`, `003E8980(0)`, `0025ACA0`, `0026FAD0(0, n, 0)` and `0026FAD0(0x1F,
n, 0)` with `n` = `0017D490()` when positive, else payload byte `+0x1060` plus 1, then `00379860(n)`,
`00379290`, `003DE920(0, 1)`, `00363B40`, and sets `+0x10` bit 2. On every pass it clears busy bits 11 and
12. This is the moment the new zone counts as started; with bit 7 also clear the mask carries no
transition reason.

### Scenes use the same loader

The End handlers of verbs `0xE7` and `0xE8` (the `eventread` pair; table records `0xE8` and `0xE9`,
first slots `00353080` and `003522C0`) call `0032FC30(m, id)` and `0032ED70(m)` with `m` = the scene slot
plus 1, clamped to 1 to 3, when `00264170()` is non-zero and `001C3370()` is not 1. `00353080` first
calls `00314D40(1)`. A scene is therefore loaded into manager 1, 2 or 3 from namespace 8 at index
`id * 4` when the verb finishes, through the same pending-mask pipeline as a zone.

### The jump lock

Verbs `0x599` (`lockmapjump`, handler `0034AD70`) and `0x59A` (`unlockmapjump`, `0034B1C0`) set and
clear bit 2 of byte `+0x200` of the current field context `002640C0()`. `00264830` reports a lock when
any of managers 0 to 2 (`02098E20`, stride `0x288`) has `+0x10` bit 0 and `+0x200` bit 2 set; the mapjump
poll waits on it. A script that locks and never unlocks holds every pending jump.

### The jump-index verbs

Immediate verbs keep their handler in the first slot of the following table record. The verbs that read
or write the transition record:

| Verb | Handler | What it does |
|---|---|---|
| `0x8F` `setmapjumppos(i, dx, dy, dz, ...)` | `00356E10` | entrance `i` (negative: the current entrance `003148B0`) through `00377AB0`; writes its position and angle to four script variables, places the actor (`0026AF80` or `0026B0C0`) and sets steering mode 0 |
| `0x90` `nowmap()` | `0033F310` | payload `+0x1044` (`003148F0`), negatives clamped to 0 |
| `0x91` `nowjumpindex()` | `0033F7F0` | the entrance `+0x1048` resolved by `00264CE0` against manager 0's header: -1 gives `short +0x52`, -2 `+0x78`, -3 `+0x7A`, other negatives `+0x52`, then clamped to 0 or above |
| `0x92` `lastmap()` | `0033FC40` | payload `+0x104C` (`00314870`) |
| `0x93` `lastjumpindex()` | `0033FFF0` | payload `+0x1050` (`00314850`) |
| `0xD5` `mapjumpstatus(v)` | `0034A250` | bit 0 of byte `+0x17` of the current field context |
| `0x211` `getmapjumpposbyindex(i, ...)` | `003538F0` | x, y, z and angle of entrance `i` into four script variables |
| `0x2C5` `effectkeepmapjump(v)` | `0033FC20` | `0036E9B0(v, 1)` |
| `0x323` `getmapjumpanglebyindex(i)` | `00353490` | the angle of entrance `i` |
| `0x365` `getmapdestposbyindex(i, ...)` | `00353ED0` | x, y, z and angle of destination `i` into four script variables, through `00377900` |
| `0x331` `getmapjumpmode()` | `00343930` | payload `+0x1054` (`003148D0`) |
| `0x332` `setmapjumpmode(v)` | `00343D90` | payload `+0x1054` (`00314DA0`) |
| `0x3D1` `setnowjumpindex(i)` | `0034AC10` | payload `+0x1048` (`00314D80`) |
| `0x40B` `clearmapjumpstatus()` | `0033F940` to `0025D580` | `00238B00(0)`; leaves the `02099DA7` hold (`00250960`); `002E1CD0(1)`; clears busy bit 12; `00225CD0(0x13)`; `00226280()` |
| `0x56D` `setposparty_mapjump(x, y, z, angle)` | `0033F070` | pops four floats and calls `0037D000({x, y, z, 1.0}, angle, 0)`: formation placement of party slots 0 to 3 around the point (`0031BD60`, `0031BAC0`, `0026B0C0`), each member turned to the angle |
| `0x576` `fadeout_check_nextmap(map)` | `00343710` | when `0026DEF0(map)` is negative, `00361200(-1, 1, 1)` fades the four music slots at `022CB9F0` |
| `0x4EA` `set_ignore_mapjump_func(v)` | `00510720` | pops its argument and tail-jumps to `0016D6A0`, a `ret 0` stub: a no-op |

`00377AB0(i, out)` looks entrance `i` up in the field data through `00264B50`; when there is no such
entrance it takes `[[0209A678]] + 0x28` and `+0x2C` when `02ADD0D8` is set, else zero, and passes the
angle through `003A1C50`.

`00264B90(table, manager, i, …)` is the reader under both: table 0 is
the list whose offset is at `+0x54` of the manager's header (`00264B50`), table 1 the list at `+0x84`
(`00264110`). Each list starts with a count, and entry `i` has x, y, z and the angle at
`+0x04 + i × 0x20` to `+0x10 + i × 0x20`; an index at or above the count gives zeros and the result 0.
The aliases -1, -2 and -3 resolve as in `00264CE0`. `00377900(i, out)` reads table 1 of
manager 0, writes zeros when there is no such record and passes the angle through `003A1C50`.

`0026DEF0(map)` reads the per-area music number table `003EAA70` (blocks of 128
area ids under `[02B5E0D0]`, entries selected by the story variable `00265270()`); when the number is
negative or its byte in `[022CBA50]` lacks bit 0 (`00361010`) it returns `0x5B` while the summon mode
`003135C0` is on and `0x5A` while `00303EC0` reports non-zero.

### What names a map

A map is named by one integer, the field id: the first argument of `mapjump`, payload `+0x1044`, and the
index into three tables.

The archive file table is the first:

- `0032FCA0` loads a zone from namespace 5 at index `id * 3`, and `002DF980(ns, i)` returns
  `[[0215F000 + ns*8] + i*8]`, a path pointer.
- `002DF9A0` fills `0215F000`. Its ten arms store ten language copies of the namespace-5 table
  (`0215F028` is written at `002DFC03`, `002DFC71`, `002DFCD1`, `002DFD31`, `002DFD91`, `002DFDE3`,
  `002DFE35`, `002DFEBF`, `002DFF18` and `002DFF71`); the `us` copy is `01EE23A0` (`002DFBFC`).
- Each id has three path pointers, `.ebp`, `.mot` and `.fpk`, of the form
  `PS2Data\plan_master\us\plan_map\<area>\<area><nn>\global\<area><nn>.<ext>`, and `<area><nn>`
  is the zone's internal name:

| Field id | File |
|---:|---|
| 0 | `tst_a01` (under `plan_work`) |
| `0xC` | `ttl_a01`, the title map |
| `0x132` | `rbn_a18` |
| `0x320` | `nac_b01` |

The `MapRef` resource (namespace 9, loaded by `00268750`) has 8 bytes per field id; `00264F90(id)` reads
its `+6` word, the persistence group written to the transition record. The music table `003EAA70` is the
third.

## Layouts

`ZoneTransitionRecord` (`0x20` bytes, offsets from the start of the payload+0x1044):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `i32` | destinationField | payload +`0x1044`: the map being jumped to; also `01EED064` while pending (`003145E0`) |
| `04` | `i32` | destinationEntrance | payload +`0x1048`: the entrance index (`003145E0`, `00314D80`) |
| `08` | `i32` | previousField | payload +`0x104C`: the old destinationField (`003145E0`) |
| `0C` | `i32` | previousEntrance | payload +`0x1050`: the old destinationEntrance (`003145E0`) |
| `10` | `u32` | mode | payload +`0x1054`: the mode argument (`003145E0`, `00314DA0`) |
| `14` | `i32` | persistenceGroup | payload +`0x1058`: `00264F90`(destinationField) (`003145E0`) |
| `18` | `i32` | loadedField | payload +`0x105C`: destinationField (`003145E0`, `00314530`) |
| `1C` | `u8` | startSelector | payload +`0x1060`: 0 to 2, written by `0026D910` while +`0x1D` is 0 and passed to `00180620`; read by `002620E0` when `0017D490`() is not positive |
| `1D` | `u8` | initPending | payload +`0x1061`: set to 1 by `00268320` and `0026D8F0`, cleared by `0026D910` after it has written +`0x1C` |
| `1E` | `u8` | flags | payload +`0x1062`: bit 5 cleared by `003145E0` and set by `00314530`; bit 2 written by `00314D00`; bits 0 and 7 read by the area-flag accessors |
| `1F` | `u8` | flags2 | payload +`0x1063`: bits 4-5 the MP-regime override (area flags page); bit 6 selects payload +`0x1534` as the music number (`0026DE20`) |

## Operations

| Function | Role |
|---|---|
| `00354D00` | mapjump Start: pops map, entrance, mode |
| `00355350` | mapjump Poll: waits for quiet, requests, waits for the context to change |
| `00314440` | the request: staging, manager reinitialisation, fade, file-cache notice |
| `003145E0` | staging: transition record, busy bit 12, autosave decision |
| `00314530` | the restore path's re-request of the current field |
| `00314020` | the tick: drains `02099ABC`, consumes `01EED064` |
| `0025BFB0` | reinitialises and unloads the requested managers |
| `0026A5F0(m)` | ORs manager `m` into `02099ABC`; 0 also requests 1 to 3 |
| `0032FC30(m, ctx)` | area refresh, begins the load, sets pending bit 0 |
| `0032FCA0(m, ctx)` | chooses namespace and index, queues the loads |
| `00330310` | the primary payload load, pending bit `0x20000` |
| `0032ED70` / `0032F6C0` / `00332130` | set the start hold, read the mask without it, release the hold |
| `003321E0` | busy bit 7 from the pending masks |
| `00360120` | main-loop busy check and resume |
| `003601B0` / `003601C0` / `00360360` | busy set, clear, test |
| `002620E0` | the ready point: start work once, busy bits 11 and 12 off |
| `00264830` | the jump-lock test over managers 0 to 2 |
| `00264CE0` | entrance aliases -1, -2, -3 |
| `00377AB0` | entrance position and angle |
| `001DA090` | file cache notice, records the new and previous map id |
| `002DF980` | archive path lookup |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `01EED064` | `i32` | pending map id, -1 when none | `003145E0`, `00314530`, `00314020` |
| `02099ABC` | `u32` | manager request mask | `0026A5F0`, `0025BFB0` |
| `022C6E48` | `u64[5]` | pending-load mask per manager; bit 0 the start hold | `0032FC30`, `0032FCA0`, `00330310`, `0032ED70`, `00332130`, the load callbacks |
| `022CB720` | `u32` | the busy mask | the table above |
| `02099D70` | `void*` | current field context | the actor manager runtime |
| `02098E20` | 5 × `0x288` | the actor managers | the actor manager runtime |
| `02099DB8` | `u32` | sum of the active managers' `+0x1D4` over managers 0 to 2 | `00266D10` (`002670C7`), `002628B0` (`00262F04`), `0025B500` (`0025B558`), `0025C830` (`0025D400`) |
| `022C6D28`, `022C6D40` | `i32[5]` each | the request context per manager | `0032FCA0` |

## Modding notes

- The request `00314440` is the single funnel every scripted jump passes through; the poll
  `00355350` is already a wait loop and can be held in state 0 without touching staging.
- A ready signal that needs no hook: busy bits 7, 11 and 12 of `022CB720` clear and `01EED064` equal
  to -1.
- The pending mask and the busy mask regenerate themselves every load; writing them breaks the load.
- A second request while one is pending is dropped (`00314440` tests `01EED064 < 0`).
- The field id is stable across languages: all ten tables under `0215F000` name the same zone for the
  same id, so the `<area><nn>` code from the active language's table is a readable name for any map.
- `set_ignore_mapjump_func` does nothing in this build.

## Related

- [Area flags: the navimapdata.bin record for every area, the town flag, the KO, Stone and X-Zone override and the other bits](area-flags-navimapdata.md)
- [The world tick and the field frame](../Engine-Core/frame-update-order.md)
- [The time-stop registry](../Engine-Core/time-stop-and-freeze.md)
- [Spawn placement and retirement](../Enemy-Spawning/enemy-spawning.md)
- [How a cutscene runs](../Scripts-And-Script-Commands/cutscenes-and-the-world-lock.md)
- [The save payload field map](../Saving-Loading-And-Settings/save-data-fields.md)
