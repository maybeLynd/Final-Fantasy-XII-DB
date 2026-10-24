---
title: "Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map"
kind: "system"
category: "World, areas and travel"
addresses: "0x00354D00, 0x00355350, 0x00314440, 0x003145E0, 0x00314020, 0x0032FC30, 0x0032FCA0, 0x003321E0, 0x002620E0, 0x0034AD70"
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
mode)`. Its handlers are read from the family-0 verb table at `0x01EED700`, one 32-byte record per verb from `+8`
([verb dispatch](../Scripts-And-Script-Commands/verb-dispatch.md)): record `0x8D` holds the Start handler
`0x00354D00` at `+0` and the Poll handler `0x00355350` at `+8`, and its result slot `+0x18` is 0, so the verb has no
End handler.

The Start handler `0x00354D00` pops the three arguments in reverse into the verb's context words (`ctx[3]`
= mode, `ctx[2]` = entrance, `ctx[1]` = map). When byte `0x02064AD3` (`0x00229EA0`) is 2 it calls
`0x001831A0`. It then calls `0x005C5230`, which is `xor eax, eax; ret`, so `ctx[0]` is always 0 and the
handler always returns 0.

The Poll handler `0x00355350` runs every frame. In state 0 it does the following, in order:

1. Takes the current field context `c = 0x002640C0()` (`[0x02099D70]`).
2. When `c+0x28` is 0 and byte `c+0x16` is 0 it waits (returns 1) while `0x02099DB8` (`0x00264180`) is
   non-zero or while `0x00264830` finds a manager with `+0x10` bit 0 and `+0x200` bit 2 set (the jump
   lock).
3. Calls `0x001D6AE0(map)`, a guarded indirect call on the file-cache object.
4. Calls `0x00314440(map, entrance, mode, 1)`. A non-zero result means the resource queue is busy; the
   poll returns 1 and tries again next frame.
5. Sets `ctx[0]` = 1.

In state 1 the poll returns 1 while `c+0x28` is 0 and 0 (done) once it is non-zero. `+0x28` is the index
of the actor manager the script runs in: 0 for the zone's own scripts, 1 to 3 for a scene. So a jump
asked for by a scene completes and the scene continues, while a jump asked for by the zone's own
script waits until the jump tears that script down. State 2 calls `0x002EF890` and returns done; nothing
in the Start handler produces it.

### The request

`0x00314440(map, entrance, mode, nonblocking)` is the one funnel every jump passes through:

```c
if (0x00408B00() == 0 && map == 0) map = 0xC;          // byte 0x02B62DB9: input channel mode
if (0x01EED064 < 0) {                                   // no jump pending
    r = 0x003145E0(map, entrance, mode, nonblocking);   // staging
    if (nonblocking && r != 0) return r;              // resource queue busy: caller retries
    0x0026A5F0(0);                                      // request managers 0..3 for reinitialisation
    if ((mode & 1) == 0 && 0x002EFD20(2) == 0) {        // fade slot 2 idle
        0x002EFE40(6); 0x002EFE50(0xFF);
        0x002EFA70(2, ~(mode * 2) & 8, 0, (mode >> 1) & 1);
    }
    0x002E1C40(0, 2); 0x00254AC0(); 0x00183240(0);
    0x001D6C40(0x01EED064);                               // file cache: "[FileCache] OnMapJumpBefore (%d)"
    0x00182D80();
}
return 0;
```

`mode` bit 0 set means no fade-out from this request; bits 1 and 2 shape the fade call. A request made
while `0x01EED064` is non-negative is dropped without error. `0x0026A5F0(0)` ORs bits 0 to 3 into the
manager request mask `0x02099ABC` (requesting manager 0 also requests 1, 2 and 3).

Callers of `0x00314440`: the mapjump poll (`0x003553CF`), `0x00280140` (`0x0028027C`), `0x00394130`
(`0x003941FC`), `0x0050C8A0` (`0x0050C8B6`), the load-completion callbacks `0x00331920` (`0x0033194E`,
`0x0033197F`) and `0x003318C0` (`0x003318E5`, `0x00331914`), and `0x00319F50` (`0x0031A0F1`).

### Staging and the transition record

`0x003145E0(map, entrance, mode, nonblocking)` runs in this order:

1. `0x0032E520(0)` drains the resource queue; with `nonblocking` it calls `0x0032E520(1)` and returns 1
   when the queue is busy.
2. `0x0026E0D0(0, 0)`, busy bit 12 set (`0x003601B0(0xC)` at `0x0031463E`), `0x0026A5F0(1)`, `(2)`, `(3)`.
3. The transition record in the persistent payload (`0x002EF2B0`): `+0x104C` = old `+0x1044`; `+0x1044`
   = map, also copied to `0x01EED064`; `+0x1050` = old `+0x1048`; `+0x1048` = entrance; `+0x1054` = mode;
   `+0x1058` = `0x00264F90(map)`, the persistence group; `+0x105C` = map; `+0x1062` bit 5 cleared.
4. `0x005C5230()`, which returns 0 (`0x003146E5`); `0x022C2540` = 0; `0x002EFA70(3, 0, 1, 0)` (fade slot 3, `0x00314700`).
5. Steps 5 and 6 run only when `0x01EED064` is non-negative (`0x00314705`-`0x0031470C`): `s = 0x00236760()` (bit 12 of
   `[0x02EBF190]+4`). For destination `0xC`: `0x00287D00(0)` and `0x01E0C3EC` = 1. For any other destination the
   map id is written to the runtime buffer at `0x002EF640() + 0x4E664` only when `s` is 0 (`0x00314731`), and
   `0x003C8670()` runs whatever `s` is (`0x00314744`).
6. Autosave: when `0x0020E500(map, 0x00265270(), entrance)` returns non-zero (`0x00314774`-`0x0031477B`), staging
   zeroes three stack buffers of `0x80`, `0x80` and `0x400` bytes, then `0x00229B40(s)`, `0x005844A0(buffers, 1, s)`,
   `0x00584580()` and `0x00583260()` (`0x003147BB`-`0x003147E9`) capture the runtime state and create the autosave
   widget `0x0057E4D0`. Staging then returns 0, and the funnel goes on to `0x0026A5F0(0)` and the slot-2 fade.

Field `0xC` is the title map (`ttl_a01`, see the file table below): a request for map 0 becomes `0xC`
when the input channel mode is 0, and staging `0xC` skips the runtime-buffer write.

`0x00314530` is the restore path: it requests managers 1, 2, 3 and 0, sets `+0x1062` bit 5, copies
`+0x1044` to `0x01EED064` and `+0x105C`, clears `0x022C2540`, starts fade slot 2 with `0x002EFA70(2, 0, 0, 0)`,
sets `0x022C2528` = 1 and notifies the file cache. `0x003145E0` is also called by the area initialisation
`0x00266D10` (`0x00267127`). `0x00314D00(v)` writes bit 2 of `+0x1062`.

### The tick tears the old zone down and starts the load

`0x00314020`, the simulation tick, runs this before any actor:

1. `0x0025BFB0` drains the request mask `0x02099ABC`: when bit 0 is set, `0x0026CE60(m)` reinitialises every
   requested manager from 4 down to 0 and the party roster `0x0209A1F0` to `0x0209A208` is cleared; then
   every requested manager is unloaded with `0x002628B0(m)` and its bit cleared.
2. `0x01EED060` is reset to -1 when non-negative.
3. When `0x01EED064` is non-negative: two console lines (`0x00D103E0`, `0x00D10420`), `0x0032FC30(0, map)`,
   then `0x01EED064` = -1.

`0x0032FC30(0, map)` calls `0x003EA6E0(map, byte 0x022C6D1D)`, then `0x0032FCA0(0, map)`, `0x0025D4D0(0)`, and sets
bit 0 of `0x022C6E48`, the start hold. A branch guarded by `0x005C5230(5)` is dead in this build.

That dead branch calls `0x003319D0(map)`. It takes the zone's `.ebp` path (namespace 5, index
`map * 3`) and makes four sibling paths with `0x00331F50`, which replaces every occurrence of one
substring with another: the folder `global` becomes `entry`, `entry`, `treasure` or `icon` and the
extension `eps`, `ard`, `eps` or `icn`. Each file that exists (`0x0032E400(0xFF, path)`) is read into
a block labelled `POSENT`, `MAPARD`, `TREENT` or `NV_ICON` with the source name `atelload.c`
(`0x0036C750` cuts a path to its file name), with the completions `0x003320E0`, `0x003320D0`,
`0x00332110` and `0x00332100`.

### Where the files come from

`0x0032FCA0(m, ctx)` unloads the manager (`0x002628B0`), resets it (`0x0032ED80`), stores `ctx` at
`0x022C6D28[m]` and `0x022C6D40[m]`, and chooses the archive namespace and base index:

| Manager | Namespace | Base index | Used for |
|---:|---:|---|---|
| 0 | 5 | `ctx * 3` | the zone |
| 1 to 3 | 8 | `ctx * 4` | event scenes |
| 4 | 1 | `ctx + 0x6B` | the fifth manager |

It then queues the asynchronous loads, each setting a bit of the manager's pending mask
`0x022C6E48 + m*8` that its completion callback clears:

| Load | Pending bit | Condition |
|---|---:|---|
| `base + 2` (callback `0x00331760`, buffer `0x022C6E98[m]`) | `0x1000` | managers 1 to 4 |
| `base + 1` (callback `0x003302B0`, buffer `0x022C6E70[m]`) | `0x2000` | managers 0 to 3 |
| `base + 3` from namespace 8 (callback `0x00331820`) | `0x8000` | managers 1 to 3 |
| `base + 3` from namespace `0x25` (callback `0x003317C0`) | `0x4000` | managers 1 to 3 |
| the primary payload, `0x00330310(m, ctx, ns, base)` (callback `0x003304A0`) | `0x20000` | all |

Pending bit 0 is a start hold, not a load. `0x0032ED70(m)` sets it, `0x0032F6C0(m)` reads the mask without
it, and `0x00332130(m)` clears it; when the mask thereby becomes 0, `0x00332130` clears manager `+0x11` bit 3
and calls `0x0032F1B0(m)` to finalise the manager. For the zone, `0x00378120` (called by `0x003775D0` at
`0x003776DD`) binds the new area's navigation data and then calls `0x00332130(0)`, so the zone's actors and
scripts cannot start before its navigation exists.

### The busy mask

`0x022CB720` is a 32-bit mask of reasons the game is busy: `0x003601B0(n)` sets bit `n`, `0x003601C0(n)`
clears it, `0x00360360(n)` tests it, `0x00360100` and `0x00360370` zero it. A sweep of every call site, with
the bit loaded into `ecx` before the call:

| Bit | Set by | Cleared by |
|---:|---|---|
| 3 | `0x00228130` (`0x0022826D`) | `0x00228130` (`0x00228187`) |
| 6 | `0x003615F1` | `0x00361469` |
| 7 | `0x003321E0` (`0x00332244`): a manager has a pending load | `0x003321E0` |
| 10 | `0x0037C4D0` | `0x0037C6C8` |
| 11 | `0x002628B0` (`0x00262BA8`), the manager unload | `0x002620E0` (`0x002621AD`) |
| 12 | `0x003145E0` (`0x0031463E`), `0x002678C0` (`0x002678F5`) | `0x002620E0` (`0x002621BC`), `0x0025D580` (`0x0025D5B3`) |
| 13 | `0x00344CAE`, `0x0034571B` | `0x00345169`, `0x003464F2` |
| 15 | `0x00360710` (`0x003607E1`, bit computed at run time) | `0x003603F0` (`0x00360424`, `0x00360440`), `0x00360A20` (`0x00360A36`) |
| 16 | `0x0035B840` (`0x0035B881`) | `0x0035B8FC` |
| 18 | `0x00342C90` (`0x00342C99`) | `0x00343325` |
| 19 | nine party-command verb bodies (`0x0034C3B1`, `0x0034CCD9`, `0x0034CE3B`, `0x0034D542`, `0x00350184`, `0x00350D17`, `0x00351A66`, `0x003521C8`, `0x00352B05`) | `0x0034C398`, `0x0034CE18`, `0x003506B4` (bit `0x13` plus a selector), `0x0034D465` |

`0x003321E0` sets bit 7 when any of the five pending masks has a bit other than bit 0 set and clears it
otherwise. `0x00360120`, called from the main loop, runs `0x003321E0` and, when the whole mask is 0 and byte
`0x022CB72A` or `0x022CB72B` is set, runs the resume routine `0x003601D0`. `0x002628B0` zeroes the mask through
`0x00360100` (`0x00262B9E`); the boot routine `0x0022A0B0` calls `0x00360370` (`0x0022A39E`).

### The zone is ready

`0x0025D9E0`, the per-manager field pass, calls `0x002620E0(manager)` at `0x0025DB7D` and `0x0025DC27`. Only
manager 0 gets past its first test (`+0x28` == 0). On the first pass for a load (`+0x10` bit 2 clear) it
runs the start work once: `0x00259B30`, `0x003E8980(0)`, `0x0025ACA0`, `0x0026FAD0(0, n, 0)` and `0x0026FAD0(0x1F,
n, 0)` with `n` = `0x0017D490()` when positive, else payload byte `+0x1060` plus 1, then `0x00379860(n)`,
`0x00379290`, `0x003DE920(0, 1)`, `0x00363B40`, and sets `+0x10` bit 2. On every pass it clears busy bits 11 and
12. This is the moment the new zone counts as started; with bit 7 also clear the mask carries no
transition reason.

### Scenes use the same loader

The End handlers of verbs `0xE7` and `0xE8` (the `eventread` pair; table records `0xE8` and `0xE9`,
first slots `0x00353080` and `0x003522C0`) call `0x0032FC30(m, id)` and `0x0032ED70(m)` with `m` = the scene slot
plus 1, clamped to 1 to 3, when `0x00264170()` is non-zero and `0x001C3370()` is not 1. `0x00353080` first
calls `0x00314D40(1)`. A scene is therefore loaded into manager 1, 2 or 3 from namespace 8 at index
`id * 4` when the verb finishes, through the same pending-mask pipeline as a zone.

### The menu scene in manager 3

Two menu tasks load a scene into manager 3 while they are open. A small state machine keeps the state at
`0x02B47748`, the scene id at `0x02B4774C` and an in-use flag at `0x02B47750`:

| Function | What it does |
|---|---|
| `0x003CA140(n)` | when not in use: sets in use, state 1, and the id `0x1B5` for n = 0, `0x1B6` for 1, `0x1B7` for 2, `0x1B8` otherwise |
| `0x003C9FD0(3)` | the step, run each UI frame by `0x00250540` (`0x0025060A`), only while in use and `0x022C6D20[3]` (`0x0032F6E0`) is clear: state 1 runs `0x0032FC30(3, id)` and `0x0032ED70(3)` and becomes 2; state 3, once `0x0032F6C0(3)` reports nothing pending, runs `0x00332130(3)` and becomes 0; state 4, once nothing is pending, runs `0x00332190(3)` and becomes 5 with the flag cleared and the id -1 |
| `0x003CA0C0()` | true in state 2 with nothing pending: the scene is loaded and held |
| `0x003CA1B0(s)` | stores state `s`; the menus call it with 3 to start the held scene |
| `0x003CA0A0()` | while in use, sets state 4 to dispose the scene |
| `0x003CA0F0()` | true when idle: state 0 not in use, or state 5 once `0x022C6D20[3]` is clear |

The menu task `0x002D70F0` starts it with n = 0 for its mode `0x40` and 1 for `0x41` (`0x002D73F3`); `0x0027F5D0` with
n = 2 for its entry `0x42` (`0x0027FA00`). Each waits in its state 8 for `0x003CA0C0` and then calls `0x003CA1B0(3)` in its
state `0xC`. Their close path `0x002D6F90` ends by calling `0x003CA0A0` (`0x002D6FF0`).

### The jump lock

Verbs `0x599` (`lockmapjump`, handler `0x0034AD70`) and `0x59A` (`unlockmapjump`, `0x0034B1C0`) set and
clear bit 2 of byte `+0x200` of the current field context `0x002640C0()`. `0x00264830` reports a lock when
any of managers 0 to 2 (`0x02098E20`, stride `0x288`) has `+0x10` bit 0 and `+0x200` bit 2 set; the mapjump
poll waits on it. A script that locks and never unlocks holds every pending jump.

### The jump-index verbs

Immediate verbs keep their handler in the first slot of the following table record. The verbs that read
or write the transition record:

| Verb | Handler | What it does |
|---|---|---|
| `0x8F` `setmapjumppos(i, dx, dy, dz, ...)` | `0x00356E10` | entrance `i` (negative: the current entrance `0x003148B0`) through `0x00377AB0`; writes its position and angle to four script variables, places the actor (`0x0026AF80` or `0x0026B0C0`) and sets steering mode 0 |
| `0x90` `nowmap()` | `0x0033F310` | payload `+0x1044` (`0x003148F0`), negatives clamped to 0 |
| `0x91` `nowjumpindex()` | `0x0033F7F0` | the entrance `+0x1048` resolved by `0x00264CE0` against manager 0's header: -1 gives `short +0x52`, -2 `+0x78`, -3 `+0x7A`, other negatives `+0x52`, then clamped to 0 or above |
| `0x92` `lastmap()` | `0x0033FC40` | payload `+0x104C` (`0x00314870`) |
| `0x93` `lastjumpindex()` | `0x0033FFF0` | payload `+0x1050` (`0x00314850`) |
| `0xD5` `mapjumpstatus(v)` | `0x0034A250` | bit 0 of byte `+0x17` of the current field context |
| `0x211` `getmapjumpposbyindex(i, ...)` | `0x003538F0` | x, y, z and angle of entrance `i` into four script variables |
| `0x2C5` `effectkeepmapjump(v)` | `0x0033FC20` | `0x0036E9B0(v, 1)` |
| `0x323` `getmapjumpanglebyindex(i)` | `0x00353490` | the angle of entrance `i` |
| `0x365` `getmapdestposbyindex(i, ...)` | `0x00353ED0` | x, y, z and angle of destination `i` into four script variables, through `0x00377900` |
| `0x331` `getmapjumpmode()` | `0x00343930` | payload `+0x1054` (`0x003148D0`) |
| `0x332` `setmapjumpmode(v)` | `0x00343D90` | payload `+0x1054` (`0x00314DA0`) |
| `0x3D1` `setnowjumpindex(i)` | `0x0034AC10` | payload `+0x1048` (`0x00314D80`) |
| `0x40B` `clearmapjumpstatus()` | `0x0033F940` to `0x0025D580` | `0x00238B00(0)`; leaves the `0x02099DA7` hold (`0x00250960`); `0x002E1CD0(1)`; clears busy bit 12; `0x00225CD0(0x13)`; `0x00226280()` |
| `0x56D` `setposparty_mapjump(x, y, z, angle)` | `0x0033F070` | pops four floats and calls `0x0037D000({x, y, z, 1.0}, angle, 0)`: formation placement of party slots 0 to 3 around the point (`0x0031BD60`, `0x0031BAC0`, `0x0026B0C0`), each member turned to the angle |
| `0x576` `fadeout_check_nextmap(map)` | `0x00343710` | when `0x0026DEF0(map)` is negative, `0x00361200(-1, 1, 1)` fades the four music slots at `0x022CB9F0` |
| `0x4EA` `set_ignore_mapjump_func(v)` | `0x00510720` | pops its argument and tail-jumps to `0x0016D6A0`, a `ret 0` stub: a no-op |

`0x00377AB0(i, out)` looks entrance `i` up in the field data through `0x00264B50`; when there is no such
entrance it takes `[[0x0209A678]] + 0x28` and `+0x2C` when `0x02ADD0D8` is set, else zero, and passes the
angle through `0x003A1C50`.

`0x00264B90(table, manager, i, …)` is the reader under both: table 0 is
the list whose offset is at `+0x54` of the manager's header (`0x00264B50`), table 1 the list at `+0x84`
(`0x00264110`). Each list starts with a count, and entry `i` has x, y, z and the angle at
`+0x04 + i × 0x20` to `+0x10 + i × 0x20`; an index at or above the count gives zeros and the result 0.
The aliases -1, -2 and -3 resolve as in `0x00264CE0`. `0x00377900(i, out)` reads table 1 of
manager 0, writes zeros when there is no such record and passes the angle through `0x003A1C50`.

`0x0026DEF0(map)` reads the per-area music number table `0x003EAA70` (blocks of 128
area ids under `[0x02B5E0D0]`, entries selected by the story variable `0x00265270()`); when the number is
negative or its byte in `[0x022CBA50]` lacks bit 0 (`0x00361010`) it returns `0x5B` while the summon mode
`0x003135C0` is on and `0x5A` while `0x00303EC0` reports non-zero.

### What names a map

A map is named by one integer, the field id: the first argument of `mapjump`, payload `+0x1044`, and the
index into three tables.

The archive file table is the first:

- `0x0032FCA0` loads a zone from namespace 5 at index `id * 3`, and `0x002DF980(ns, i)` returns
  `[[0x0215F000 + ns*8] + i*8]`, a path pointer.
- `0x002DF9A0` fills `0x0215F000`. Its ten arms store ten language copies of the namespace-5 table
  (`0x0215F028` is written at `0x002DFC03`, `0x002DFC71`, `0x002DFCD1`, `0x002DFD31`, `0x002DFD91`, `0x002DFDE3`,
  `0x002DFE35`, `0x002DFEBF`, `0x002DFF18` and `0x002DFF71`); the `us` copy is `0x01EE23A0` (`0x002DFBFC`).
- Each id has three path pointers, `.ebp`, `.mot` and `.fpk`, of the form
  `PS2Data\plan_master\us\plan_map\<area>\<area><nn>\global\<area><nn>.<ext>`, and `<area><nn>`
  is the zone's internal name:

| Field id | File |
|---:|---|
| 0 | `tst_a01` (under `plan_work`) |
| `0xC` | `ttl_a01`, the title map |
| `0x132` | `rbn_a18` |
| `0x320` | `nac_b01` |

The `MapRef` resource (namespace 9, loaded by `0x00268750`) has 8 bytes per field id; `0x00264F90(id)` reads
its `+6` word, the persistence group written to the transition record. The music table `0x003EAA70` is the
third.

## Layouts

`ZoneTransitionRecord` (`0x20` bytes, offsets from the start of the payload+0x1044):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | destinationField | payload `+0x1044`: the map being jumped to; also `0x01EED064` while pending (`0x003145E0`) |
| `+0x04` | `i32` | destinationEntrance | payload `+0x1048`: the entrance index (`0x003145E0`, `0x00314D80`) |
| `+0x08` | `i32` | previousField | payload `+0x104C`: the old destinationField (`0x003145E0`) |
| `+0x0C` | `i32` | previousEntrance | payload `+0x1050`: the old destinationEntrance (`0x003145E0`) |
| `+0x10` | `u32` | mode | payload `+0x1054`: the mode argument (`0x003145E0`, `0x00314DA0`) |
| `+0x14` | `i32` | persistenceGroup | payload `+0x1058`: `0x00264F90`(destinationField) (`0x003145E0`) |
| `+0x18` | `i32` | loadedField | payload `+0x105C`: destinationField (`0x003145E0`, `0x00314530`) |
| `+0x1C` | `u8` | startSelector | payload `+0x1060`: 0 to 2, written by `0x0026D910` while `+0x1D` is 0 and passed to `0x00180620`; read by `0x002620E0` when `0x0017D490`() is not positive |
| `+0x1D` | `u8` | initPending | payload `+0x1061`: set to 1 by `0x00268320` and `0x0026D8F0`, cleared by `0x0026D910` after it has written `+0x1C` |
| `+0x1E` | `u8` | flags | payload `+0x1062`: bit 5 cleared by `0x003145E0` and set by `0x00314530`; bit 2 written by `0x00314D00`; bits 0 and 7 read by the area-flag accessors |
| `+0x1F` | `u8` | flags2 | payload `+0x1063`: bits 4-5 the MP-regime override (area flags page); bit 6 selects payload `+0x1534` as the music number (`0x0026DE20`) |

## Operations

| Function | Role |
|---|---|
| `0x00354D00` | mapjump Start: pops map, entrance, mode |
| `0x00355350` | mapjump Poll: waits for quiet, requests, waits for the context to change |
| `0x00314440` | the request: staging, manager reinitialisation, fade, file-cache notice |
| `0x003145E0` | staging: transition record, busy bit 12, autosave decision |
| `0x00314530` | the restore path's re-request of the current field |
| `0x00314020` | the tick: drains `0x02099ABC`, consumes `0x01EED064` |
| `0x0025BFB0` | reinitialises and unloads the requested managers |
| `0x0026A5F0(m)` | ORs manager `m` into `0x02099ABC`; 0 also requests 1 to 3 |
| `0x0032FC30(m, ctx)` | area refresh, begins the load, sets pending bit 0 |
| `0x0032FCA0(m, ctx)` | chooses namespace and index, queues the loads |
| `0x00330310` | the primary payload load, pending bit `0x20000` |
| `0x0032ED70` / `0x0032F6C0` / `0x00332130` | set the start hold, read the mask without it, release the hold |
| `0x003321E0` | busy bit 7 from the pending masks |
| `0x00360120` | main-loop busy check and resume |
| `0x003601B0` / `0x003601C0` / `0x00360360` | busy set, clear, test |
| `0x002620E0` | the ready point: start work once, busy bits 11 and 12 off |
| `0x00264830` | the jump-lock test over managers 0 to 2 |
| `0x00264CE0` | entrance aliases -1, -2, -3 |
| `0x00377AB0` | entrance position and angle |
| `0x001DA090` | file cache notice, records the new and previous map id |
| `0x002DF980` | archive path lookup |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `0x01EED064` | `i32` | pending map id, -1 when none | `0x003145E0`, `0x00314530`, `0x00314020` |
| `0x02099ABC` | `u32` | manager request mask | `0x0026A5F0`, `0x0025BFB0` |
| `0x022C6E48` | `u64[5]` | pending-load mask per manager; bit 0 the start hold | `0x0032FC30`, `0x0032FCA0`, `0x00330310`, `0x0032ED70`, `0x00332130`, the load callbacks |
| `0x022CB720` | `u32` | the busy mask | the table above |
| `0x02099D70` | `void*` | current field context | the actor manager runtime |
| `0x02098E20` | 5 × `0x288` | the actor managers | the actor manager runtime |
| `0x02099DB8` | `u32` | sum of the active managers' `+0x1D4` over managers 0 to 2 | `0x00266D10` (`0x002670C7`), `0x002628B0` (`0x00262F04`), `0x0025B500` (`0x0025B558`), `0x0025C830` (`0x0025D400`) |
| `0x022C6D28`, `0x022C6D40` | `i32[5]` each | the request context per manager | `0x0032FCA0` |

## Modding notes

- The request `0x00314440` is the single funnel every scripted jump passes through; the poll
  `0x00355350` is already a wait loop and can be held in state 0 without touching staging.
- A ready signal that needs no hook: busy bits 7, 11 and 12 of `0x022CB720` clear and `0x01EED064` equal
  to -1.
- The pending mask and the busy mask regenerate themselves every load; writing them breaks the load.
- A second request while one is pending is dropped (`0x00314440` tests `0x01EED064 < 0`).
- The field id is stable across languages: all ten tables under `0x0215F000` name the same zone for the
  same id, so the `<area><nn>` code from the active language's table is a readable name for any map.
- `set_ignore_mapjump_func` does nothing in this build.

## Related

- [Area flags: the navimapdata.bin record for every area, the town flag, the KO, Stone and X-Zone override and the other bits](area-flags-navimapdata.md)
- [The world tick and the field frame](../Engine-Core/frame-update-order.md)
- [The time-stop registry](../Engine-Core/time-stop-and-freeze.md)
- [Spawn placement and retirement](../Enemy-Spawning/enemy-spawning.md)
- [How a cutscene runs](../Scripts-And-Script-Commands/event-scenes.md)
- [The save payload field map](../Saving-Loading-And-Settings/save-data-fields.md)
