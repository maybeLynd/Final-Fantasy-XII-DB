---
title: "Save crystals and gate crystals: the heal, the save menu, teleporting and the two bits that switch them off"
kind: "system"
category: "World, areas and travel"
addresses: "00350240, 00351940, 00350600, 00351CE0, 00314D00, 00314C70, 00314B60, 00314B00, 003149E0, 00314A00, 0026DB30, 00352C80, 00264CA0, 00264E40, 002649B0, 00264AE0, 00264CE0, 00342490, 00343010, 0034AC10, 00314D80, 003462D0, 002E1A60, 002E0DA0, 002E1690, 002E0650, 00352E00, 00346DA0, 00254710, 002E09A0, 00254B50, 002E1BA0, 0022B8C0, 00356500, 00359C60, 0030F4B0, 0030F3F0, 0030F4D0, 0030F690, 0030F340, 0030F5A0, 00237CA0, 0034AAB0, 002FEAC0, 003567F0, 003529B0, 0036E6B0, 0024DE70, 003B0AD0, 0024E210, 00344170, 00269060, 00268690, 0036E700, 00314DA0, 00183070, 001D8770, 0034F870, 0034FDC0, 00350AE0, 00346E10, 00343CC0, 00349420, 00350FD0, 00351380, 00352080, 00314B80, 00314CD0, 00314CA0, 00314BB0, 00314BE0, 00314C40, 00314A60, 00314B40, 00314B20, 00314A80, 00314AA0, 00314AC0, 00314AE0, 00377700, 00377780, 00377BA0, 00377750, 00314530, 003145E0, 002695A0, 002628B0"
---

## What the player sees

Walking up to a crystal heals the whole party and revives anyone who is down. Pressing confirm
opens a short menu: save, teleport, or both, depending on which the story currently allows. Saving
fades to black, opens the save screen and fades back in. A gate crystal also asks where to go:
choosing a place costs one Teleport Stone, plays a flash around the party, and the party appears
beside the destination crystal. The first time the party touches a gate crystal, that place joins
the list of destinations.

## How it works

### The crystal's script and its number

Every crystal is the `system_crystal_actor` of its zone's field script. The `us` script corpus
holds the same actor in 81 zone scripts, `alc_c01` among them, and the code below quotes that one.
Its `init` first makes sure the party owns key item `8040`<sub>h</sub> (Rabanastre's crystal) and that the
item is in the destination array `g_menu_telepo_dest` (31 entries), then asks the engine which
crystal it is with `getcrystalid(3, 0)`.

`getcrystalid` is verb `30E`<sub>h</sub>, handler `00352C80`. It pops the entry index and then the kind and
calls `00264CA0(kind, index)`; the result is the `u16` at the entry's `+14`<sub>h</sub>, or -1 when there is
no entry. The lookup:

1. kinds 6 and 9 go to the global table reader `003DFAC0`; every other kind is mapped by
   `00264E40` to a list number: kinds 0, 1 and 2 to list 0, kind 3 to list 2, kind 4 to list 1,
   kind 5 to list 3, kind 8 to list 4, any other kind to none;
2. `002649B0(list, index)` reads the list from the primary manager's payload: `00264AE0(list)`
   returns section `list` of the table at payload `+[70h]` when slot 0's flag bit 0 is set;
3. the section holds a count at `+00`<sub>h</sub> and entries of `20`<sub>h</sub> bytes from `+10`<sub>h</sub>; an index at or
   above the count gives none, and for lists 0 and 1 the entry's byte `+1C`<sub>h</sub> must have bit
   `[02ADD0E8]` (`00377860`) set.

The script keeps the number as the crystal's kind: 0 is a save crystal, 255 is the save crystal
with its own bind message, and every other value is a gate crystal whose destination key item is
`803Fh + n` (the explicit `switch` in `talk`). Number 4 counts as a gate crystal only while
`ismapjumpgroupflag(402Ah)` is set. The name tag is set with `setnpcname` from the number
([NPC names](../Characters-And-Objects/npc-names.md)), and the crystal is an interactable object
(`setfreetargettype(4)`).

### The two save-image bits

Saving and teleporting are each switched off by one bit of the flag byte at payload `+1062`<sub>h</sub>, the
flag byte of the zone transition record ([save data fields](../Saving-Loading-And-Settings/save-data-fields.md),
[zone changes](zone-changes-and-mapjump.md)). Four script verbs read and write them:

| Verb | Id | Handler | Effect |
|---|---|---|---|
| `setsaveramtelepostatus(v)` | `305`<sub>h</sub> | `00350240` | `00314D00(v == 0)`: bit 2 becomes 1 when `v` is 0, 0 otherwise |
| `getsaveramtelepostatus()` | `30A`<sub>h</sub> | `00351940` | returns 1 while bit 2 is 0 (`00314B60`) |
| `setsaveramsavestatus(v)` | `306`<sub>h</sub> | `00350600` | `00314C70(v == 0)`: bit 3 becomes 1 when `v` is 0 |
| `getsaveramsavestatus()` | `30B`<sub>h</sub> | `00351CE0` | returns 1 while bit 3 is 0 (`00314B00`) |

So bit 2 means teleporting is off and bit 3 means saving is off; a script passes 1 to allow and 0
to forbid. The crystal reads both getters when it builds its menu: both allowed gives the
save-or-teleport question, saving alone gives a save prompt, teleporting alone a teleport prompt.

### Every bit of the flag byte

The same byte and the one after it carry six more script-controlled switches. Every writer of
`+1062`<sub>h</sub> and `+1063`<sub>h</sub> in the executable is a verb handler or one of the four engine functions in
the last rows:

| Bit | Set by | Reader | Meaning |
|---|---|---|---|
| `+1062`<sub>h</sub> bit 0 | `setsaverambattlestatus(v)` `303`<sub>h</sub> `0034F870` → `00314B80(v == 0)` | `getsaverambattlestatus` `308`<sub>h</sub> `00350FD0`; `00377700` returns 1 only while the bit is 0 and byte 2 of the area's record has bit 0 clear | battle off |
| bit 1 | `setsaveramsummonstatus(v)` `304`<sub>h</sub> `0034FDC0` → `00314CD0(v == 0)` | `getsaveramsummonstatus` `309`<sub>h</sub> `00351380` only | summoning off |
| bit 2 | `setsaveramtelepostatus` (above) | `getsaveramtelepostatus`; `0026DB30` | teleporting off |
| bit 3 | `setsaveramsavestatus` (above) | `getsaveramsavestatus` | saving off |
| bit 4 | `setsaveramshutoralstatus(v)` `307`<sub>h</sub> `00350AE0` → `00314CA0(v == 0)` | `getsaveramshutoralstatus` `30C`<sub>h</sub> `00352080` only | script-defined switch |
| bit 5 | `00314530` sets it on the restore path, `003145E0` clears it when a jump is staged | `0026DB30` | a load is being restored |
| bit 6 | `setnavimapjamming(v)` `37D`<sub>h</sub> `00346E10` → `00314BB0(v != 0)` | `00377780`, from the map screens `003C4070`, `004001D0`, `004006A0`, `00400E80`, `004017D0`, `00401D40` | the area map is jammed |
| bit 7 | `setmist(v)` `46A`<sub>h</sub> `00343CC0` → `00314BE0(v)`: `v` at most 0 clears it and `+1063`<sub>h</sub> bits 4-5; a positive `v` sets it and stores `v & 3` in those bits | `00377BA0` (thunk `00320160`): the stored level when the bit is set, else bits 12-13 of the area's record | mist level override |
| `+1063`<sub>h</sub> bits 0-1 | `setsaveramnavimapstatus(v)` `3C7`<sub>h</sub> `00349420` → `00314C40(v & 3)` | `00377750`, from `003C5E00`, `003C6000`, `003C5FB0`: 1 gives 1, 2 gives 0, 0 and 3 give 1 | area map availability |
| `+1063`<sub>h</sub> bits 4-5 | `setmist` (above) | `00377BA0` | the mist level |
| `+1063`<sub>h</sub> bit 6 | `0026A720` | `0026DE20`, `0025D9E0`, `00261F90` | the music override at `+1534`<sub>h</sub> is in force |

`00314A00`, reached from `002695A0` in the manager unload `002628B0` (`00262CEF`), clears bits 0,
1, 6 and 7 of `+1062`<sub>h</sub> and bits 0-5 of `+1063`<sub>h</sub> when a zone is left. Bits 2, 3, 4 and 5 are not
touched there, so the save and teleport switches survive a zone change, as the save image does.

### When teleporting is switched back on

`0026DB30` is called from the manager bind `0026C8C0` (`0026CD60`) and from `00266D10`
(`00267131`). Its teleport step:

1. it reads the persistence group of the field being entered (`003148F0`, payload `+1044`<sub>h</sub>) and
   of the field being left (`00314870`, payload `+104C`<sub>h</sub>); the group is word `+06`<sub>h</sub> of the field's
   row in the field table at `[02099D88]`;
2. when the two differ and bit 5 is clear (`0026DBF4` tests `20`<sub>h</sub>), it calls `003149E0`
   (`0026DBFD`), which clears bit 2;
3. it clears the group persistent bank `02099FF0` (`200`<sub>h</sub> bytes) on a group change, and again
   whenever the transition mode `+1054`<sub>h</sub> (`003148D0`) has bit 3 set, the bit a teleport arrival
   carries.

The story also drives the bit directly. In the `us` corpus `setsaveramtelepostatus` is called only
by the opening event script `pre_z0000`, in one `switch` on the story counter that writes 0 or 1 by
range (17 arms, listed under Shipped data); `setsaveramsavestatus` is called by no shipped script.

### The heal

The crystal's `talk` function suspends battle, waits seven frames, calls `healall(0)` and
`btladjustsystem(1)`, and plays revive effect 11 on each party member who is down.

`healall(n)` is verb `3AF`<sub>h</sub>, handler `00356500`: it maps `n` through `00359C60` and calls
`0030F4B0(-1, mask)`, which is `0030F3F0(mask)` for the nine party records (slot table 3 through
`00320AB0`) and `0030F4D0(mask)` for the thirteen guest records `1B`<sub>h</sub> to `27`<sub>h</sub> whose id
`C012h + i` passes `0030B0E0`. The mask bits:

| Mask bit | What is restored | Function |
|---|---|---|
| 1 | HP to its maximum (`+24`<sub>h</sub>, doubled under status bit 28; `max(HP, 1)` under status bit 16); a guest-type record at or below 0 HP also gets `003243F0(unit)` | `0030F340` via `00300530(record, delta, 0, 217h)` |
| 2 | MP to its capacity (`+28`<sub>h</sub>, 0 while layer bytes `+6C`<sub>h</sub> or `+7C`<sub>h</sub> carry bit 7) and the secondary word `+06`<sub>h</sub> to capacity times `+37`<sub>h</sub> | `0030F5A0` via `00300CE0` and `00300BC0` |
| 4 | the statuses in set A, `[0208D320]` | `0030F690` → `0030E360(record, 0, status, 0, 0, 217h, 0)` per bit, then `0030FED0(record, 217h)` |
| 8 | the statuses in set B, `[0208D324]` | the same |
| 16 | statuses 2, 6, 8 and 10 (`544`<sub>h</sub>) in addition | the same |

`00359C60` maps the argument: 1 and anything outside 1-5 give 7 (HP, MP, set A), 2 gives `F`<sub>h</sub>,
3 gives 4, 4 gives `C`<sub>h</sub>, 5 gives `10`<sub>h</sub>. The crystal passes 0, so it heals HP and MP and clears
set A. The two sets are built by `00237CA0` from the status table at `[02EBF118]`: a status whose
row word `+06`<sub>h</sub> has bit 13 goes to set A, the others to set B. When status 0 (KO) is cleared,
`0030F690` also clears bit 26 of the unit flag word unless the record has a terminal status and
the area is a town (`00377C20`).

`btladjustsystem(n)` (`517`<sub>h</sub>, `0034AAB0`) calls `002FEAC0(n)`: for an odd `n` it clears bit 0 of
`022C3178`, zeroes `022C3158`, `022C3160` and `022C3170` and sets `022C3168` to -1.

### The save menu

The save choice in `talk` runs, in order (`alc_c01`):

```
saved = nowjumpindex();
if (nowmap() == 0x193 && global_flag[0] < 0x541) healall(0); else setnowjumpindex(-2);
fadelayer(5); fadeout(10); wait(10);
openfullscreenmenu_48d(0x8005, 0);
fadein(10); wait(10);
setnowjumpindex(saved);
```

`setnowjumpindex` (`3D1`<sub>h</sub>, `0034AC10` → `00314D80`) writes payload `+1048`<sub>h</sub>, the entrance of the
transition record. While the save screen is open the record therefore names entrance -2, which the
entrance resolver `00264CE0` turns into the zone header's `+78`<sub>h</sub>, the save entrance; -1 becomes
`+52`<sub>h</sub>, the teleport-arrival entrance, -3 becomes `+7A`<sub>h</sub>, any other negative value `+52`<sub>h</sub>, and
the result is never negative. `gettelepoindex` (`32D`<sub>h</sub>, `00342490`) and `getsaveindex` (`32E`<sub>h</sub>,
`00343010`) return those two header words of the primary manager's payload (`00263FF0(0)`).

`openfullscreenmenu_48d` (`48D`<sub>h</sub>) is durative:

1. Start `003462D0` stores the byte `02064AD0` (`00229EB0`) at `ctx + 4` and 0 at `ctx + 8`, pops
   the parameter and then the id, and calls `002E1A60(id, param)`, `002E1690` (latch `0215F1A1` = 1)
   and `002E0650` (done byte `0215F1AE` = 0).
2. `002E1A60` maps the id through `002E0DA0`: with bit 15 preserved, `id & 7FFFh` 0 gives `11`<sub>h</sub>,
   1 gives `12`<sub>h</sub>, 2 gives `A`<sub>h</sub>, 3 gives `F`<sub>h</sub>, 4 gives `13`<sub>h</sub>, 5 gives 6, 6 gives `16`<sub>h</sub>, anything
   else 2; for id 6 the parameter is remapped (0, 1, 2 to `40`<sub>h</sub>, `41`<sub>h</sub>, `42`<sub>h</sub>, else 0).
   The crystal's `8005`<sub>h</sub> becomes category `8006`<sub>h</sub>.
3. Unless the latch is already set, or the category is 2 while `002E0FA0()` has bit 0, it writes
   `0215F1A0` = 1, `0215F1A4` = category and `0215F1A8` = parameter.
4. Poll `00352E00` returns 1 (keep waiting) while `0215F1AE` is 0 (`002E0F80`).
5. End `00346DA0` pushes `00254710()`: the word at `[0209BE80] + 10FACh` when the menu state
   `020927D8` is `11`<sub>h</sub> or `12`<sub>h</sub>, else 0. The crystal script ignores it.

The request is consumed by the per-frame menu router `002E09A0`, run from the world tick
`00314020` ([UI request router](../Menus-And-HUD/menus.md)):

1. the request is admitted when `0215F1A0` is set and either the category is below `14`<sub>h</sub> with its
   bit in `E9000`<sub>h</sub>, or `00226BA0()` returns 0, or `0053DD10()` returns non-zero;
2. the router calls `003591F0(0)` and `00254B50(category, param, 0)`, then clears `0215F1A0`;
3. `00254B50` refuses while `02092734` is 1 or the category's bit is in the block mask it builds
   from `01E0C2C0` under `002E0FA0()`; for `category & 7FFFh` = 6 it takes the default arm,
   `0028F970()` then `00280A00(category, param, 0)`, the full-screen menu opener;
4. the done byte is written by `002E1BA0` (`0215F1AE` = `0215F1AF` = 1), whose only caller is the
   menu driver `0022B8C0` in its close-full-menu arm (`0022BB8D`, when `002E05C0()` is non-zero),
   so the Poll releases the crystal when the save screen has closed.

### The teleport

The teleport choice lists the registered destinations from `g_menu_telepo_dest`, rejects a choice
at or above 25 and the current zone (`nowmap()` equal to the destination's field), and asks for
confirmation when a summon is out or the party rides a chocobo. Then `telepoeffectctrl::telepoeffect`
runs (`alc_c01`):

```
subitem(0x2000, 1);                                  // one Teleport Stone
sebsoundplay(0, 95);
effectteleposyncbyid(partycommoneffectplay(12));     // the flash, waited for
whiteout_d1(2, 0);
if (getsummonmodebit() || getchocobomodebit()) sumcho_byebye();
switch (destination key item) { case 0x8040: mapjump(0x132, 4, 10); ... default: mapjump(142, 3, 10); }
```

The warp is the ordinary `mapjump` verb with mode 10 (bits 1 and 3), so it goes through the
`mapjump` poll and `00314440` exactly as [zone changes](zone-changes-and-mapjump.md) describes; the
destination field and entrance are authored per key item (the table under Shipped data).

`effectteleposyncbyid` (`43D`<sub>h</sub>) is durative. Start `003567F0` stores the popped effect handle in
`ctx + 0`; Poll `003529B0` keeps waiting while the handle is non-zero and `0036E6B0(handle)` is
true. The test:

1. `0024DE70(handle)` switches on the handle's top nibble: 1 to `002FCA00`, 5, 6 and 9 to
   `003B0AD0`, 7 to `003B2510`, 8 to `00375AE0`, anything else gives 0;
2. a result of 2 or 3 means the effect is still playing, provided `0024E210(handle, 3)`, bit 7 of
   the effect record's `+36A`<sub>h</sub>, is still 0;
3. for the effect pool, `003B0AD0` returns 2 for an effect whose byte `+370`<sub>h</sub> is 0 and 3 for 1
   or 2, once its word `+378`<sub>h</sub> has bit 8.

### The arrival

The destination zone's `system_terepo_ctrl` tests `(getmapjumpmode() & 8) && nowjumpindex() ==
gettelepoindex()`. When true, `init` sets mode bit 4 (`setmapjumpmode(mode | 16)`), cancels the
fade and holds the screen white, and `main` plays sound 96, calls `calltelepoeffect()`, waits and
fades in. `calltelepoeffect` (`333`<sub>h</sub>, `00344170`) is `00269060()` then `00183070()`:

- `00269060` runs `00268690(9)`: for each of the four party entries `0209A1F0[0..3]` that passes
  `002EA6A0`, the encoded handle (`003589B0`) is collected and `0036E700(0, n, handles, 9)` plays
  `003B02A0(0, handles, n, [01EF9400 + 9 * 4], 5)`, the dword being `8C`<sub>h</sub>, then `0024F920(handle, 1)`;
  then `00314DA0(003148D0() & ~18h)` clears mode bits 3 and 4 in payload `+1054`<sub>h</sub>.
- `00183070` runs `001D8770` on the loading page `[01F82CD8]` (`001D8A60`; built by `001D89D0` with
  the `LoadingPage` vtable): `+08`<sub>h</sub> = 0; when the fading-out byte `+24`<sub>h</sub> is 0 it becomes 1 and the
  fade timer `+20`<sub>h</sub> is zeroed; the armed byte `+1D`<sub>h</sub> = 0. The loading page starts fading out.

The field pass runs the same two calls once the field has settled after any arrival whose mode has
bit 3 ([field runtime](../Characters-And-Objects/field-runtime.md)).

## Layouts

Struct ZoneTransitionFlags base=payload+`1062`<sub>h</sub> size=2:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | flags1 | bit 0 battle off, bit 1 summoning off, bit 2 teleporting off, bit 3 saving off, bit 4 script switch, bit 5 restore pending, bit 6 map jammed, bit 7 mist override |
| `01`<sub>h</sub> | `u8` | flags2 | bits 0-1 map availability, bits 4-5 mist level, bit 6 music override in force |

Struct MenuRequest base=`0215F1A0` size=`10`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | pending | 1 while a full-screen menu is requested (`002E1A60` sets, `002E09A0` clears) |
| `01`<sub>h</sub> | `u8` | latch | 1 from `002E1690` until the router clears it |
| `04`<sub>h</sub> | `u32` | category | `002E0DA0`(id); `8006`<sub>h</sub> for the crystal's save screen |
| `08`<sub>h</sub> | `u32` | parameter | the popped parameter, remapped for id 6 |
| `0E`<sub>h</sub> | `i8` | done | 0 from `002E0650`; 1 from `002E1BA0` when the menu closes |
| `0F`<sub>h</sub> | `i8` | done2 | 1 from `002E1BA0` |

```python
heal(mask):
  bit 1   HP   = max HP  # 0030F340
  bit 2   MP   = capacity  # 0030F5A0
  bit 4   clear statuses in [0208D320]
  bit 8   clear statuses in [0208D324]
  bit 16  clear statuses 0x544 as well
healall(0) = heal(7)
teleport_allowed = (payload[0x1062] & 0x04) == 0
save_allowed     = (payload[0x1062] & 0x08) == 0
```

## Shipped data

### Verb use in the field and event scripts

Counts over the 1,114 `us` scripts of the decompiled corpus:

| Verb | Scripts | Calls |
|---|---|---|
| `getcrystalid` | 81 | 81 |
| `getsaveramsavestatus` | 81 | 243 |
| `getsaveramtelepostatus` | 81 | 162 |
| `btladjustsystem` | 81 | 81 |
| `healall` | 197 | 2,151 |
| `effectteleposyncbyid` | 84 | 87 |
| `calltelepoeffect` | 84 | 87 |
| `setnowjumpindex` | 183 | 2,292 |
| `setsaveramtelepostatus` | 1 | 17 |
| `setsaveramsavestatus` | 0 | 0 |
| `setsaverambattlestatus`, `setsaveramsummonstatus`, `setsaveramshutoralstatus` and their getters | 0 | 0 |
| `setmist` | 55 | 122 |
| `setnavimapjamming` | 55 | 149 |
| `setsaveramnavimapstatus` | 111 | 168 |
| `recoverentry` (`6C`<sub>h</sub>, durative `00345A30`/`00346020`) | 4 | 5 |

`recoverentry` is not part of the crystal: its five calls are in return-to-field functions after a
scene in `nal_c01`, `ozm_c01`, `rsn_b01` and `hne_b0102`.

### The story counter and the teleport switch

`pre_z0000` writes `setsaveramtelepostatus` from the story counter; each arm applies while the
counter is below its bound:

| Counter below | Value | Counter below | Value |
|---|---|---|---|
| `105` | 0 | `2200` | 1 |
| `190` | 1 | `3350` | 1 |
| `343` | 0 | `4000` | 0 |
| `520` | 1 | `5400` | 1 |
| `670` | 0 | `6100` | 0 |
| `760` | 1 | `6150` | 1 |
| `1090` | 0 | `11000` | 0 |
| `1390` | 1 | otherwise | 1 |
| `1580` | 0 |  |  |

### The destinations

The `telepoeffect` switch, key item to `mapjump(field, entrance, 10)`:

| Key item | Field | Entrance | Key item | Field | Entrance |
|---|---|---|---|---|---|
| `8040`<sub>h</sub> | `306` | `4` | `8052`<sub>h</sub> | `823` | `0` |
| `8042`<sub>h</sub> | `630` | `0` | `8053`<sub>h</sub> | `1101` | `0` |
| `8043`<sub>h</sub> | `66` | `0` | `8054`<sub>h</sub> | `751` | `0` |
| `8044`<sub>h</sub> | `157` | `4` | `8055`<sub>h</sub> | `768` | `4` |
| `8045`<sub>h</sub> | `176` | `0` | `8056`<sub>h</sub> | `742` | `3` |
| `8047`<sub>h</sub> | `756` | `3` | `8057`<sub>h</sub> | `129` | `0` |
| `8048`<sub>h</sub> | `188` | `3` | `8058`<sub>h</sub> | `350` | `0` |
| `8049`<sub>h</sub> | `718` | `0` | `8059`<sub>h</sub> | `1151` | `7` |
| `804A`<sub>h</sub> | `791` | `0` | `805A`<sub>h</sub> | `386` | `1` |
| `804B`<sub>h</sub> | `360` | `0` | `805B`<sub>h</sub> | `488` | `0` |
| `804C`<sub>h</sub> | `403` | `3` | any other | `142` | `3` |
| `804E`<sub>h</sub> | `450` | `4` |  |  |  |
| `8050`<sub>h</sub> | `686` | `1` |  |  |  |
| `8051`<sub>h</sub> | `594` | `3` |  |  |  |

The common effect table `01EF9400` holds `72`<sub>h</sub>, `73`<sub>h</sub>, `74`<sub>h</sub>, `75`<sub>h</sub>, `76`<sub>h</sub>, `88`<sub>h</sub>, `87`<sub>h</sub>, `89`<sub>h</sub>, `8A`<sub>h</sub>,
`8C`<sub>h</sub>, `8D`<sub>h</sub>, `95`<sub>h</sub>, `8B`<sub>h</sub>, `96`<sub>h</sub>; entry 9 is `8C`<sub>h</sub>, the arrival flash.

## Operations

- A crystal touch is a script action on the machine whose party touched it: `healall`,
  `btladjustsystem`, the key-item grant and the destination array write are all local verbs.
- The save screen is a UI request of category `8006`<sub>h</sub> raised by the script; the script sits in
  the `openfullscreenmenu_48d` Poll until `0022B8C0` writes the done byte, so the crystal is held
  for as long as the save screen is open.
- A teleport is `mapjump(field, entrance, 10)`: it has no transition path of its own, and the
  destination zone recognises it by mode bit 3 and the arrival entrance `+52`<sub>h</sub>.
- The save and teleport switches travel in the transition record of the save image: a loaded save
  brings its own values, and the restore path's bit 5 keeps `0026DB30` from re-enabling teleport
  during the load.

## State

| Address | Kind | Role |
|---|---|---|
| payload `+1062`<sub>h</sub>, `+1063`<sub>h</sub> | u8, u8 | the flag bytes above (`002EF2B0` base) |
| payload `+1048`<sub>h</sub> | i32 | the staged entrance `setnowjumpindex` writes |
| payload `+1054`<sub>h</sub> | u32 | the transition mode; bit 3 teleport arrival, bit 4 arrival presentation running |
| `0215F1A0`-`0215F1AF` | struct | the menu request |
| `020927D8` | i32 | the menu state `00254710` tests for `11`<sub>h</sub> and `12`<sub>h</sub> |
| `0208D320`, `0208D324` | u32 | status sets A and B (`00237CA0`) |
| `022C3158`-`022C3178` | mixed | the fields `btladjustsystem(1)` resets |
| `02099FF0` | u8[`200`<sub>h</sub>] | the group persistent bank `0026DB30` clears on a teleport arrival |
| `0209A1F0` | ptr[4] | the party entries the arrival flash plays on |
| `01F82CD8` | ptr | the loading page `00183070` fades out |
| `g_menu_telepo_dest` | u16[31] at script global `0BF2`<sub>h</sub> | the registered destinations |

## Modding notes

- To open or close a gate crystal, set or clear bit 2 of payload `+1062`<sub>h</sub> (or call
  `setsaveramtelepostatus`); the next crystal touch rebuilds its menu from the two getters.
- A new destination needs a key item `803Fh + n`, an entry in the `telepoeffect` switch of every
  crystal script and a crystal script answering `getcrystalid(3, 0)` with `n`; the engine side
  needs no change.
- The Teleport Stone cost, the list and the key items are inventory and script-global writes;
  `mapjump` mode 10 and the `+52`<sub>h</sub> entrance are what the destination needs to run its arrival.
- The heal is `heal(7)`: changing the crystal to cure set-B statuses means `healall(2)` in the
  script, or moving a status into set A by setting bit 13 of its status-table word `+06`<sub>h</sub>.

## Related

- [Zone changes and mapjump](zone-changes-and-mapjump.md): the `mapjump` verb, the transition record and the restore bit.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): where the flag bytes sit in the save image.
- [Saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md): what the save screen does once open.
- [Area flags](area-flags-navimapdata.md): the town flag and the record bits the readers fall back to.
- [UI request router](../Menus-And-HUD/menus.md): the consumer of the menu request.
- [Field runtime](../Characters-And-Objects/field-runtime.md): the field-settled sequence that repeats the arrival calls.
- [NPC names](../Characters-And-Objects/npc-names.md): the crystal's name tag.
- [Chocobos and airships](chocobos-and-airships.md): the dismount the teleport performs.
- [Game over](game-over.md): what a party wipe does instead.
