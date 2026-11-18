[Home](../../README.md) / [World, areas and travel](README.md) / Save crystals and gate crystals

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Save crystals and gate crystals: the heal, the save menu, teleporting and the two bits that switch them off | system | World, areas and travel | Changing areas and travel | What happens when the player confirms at a crystal: the full heal and what it restores, the save menu request and how the save screen is opened and waited for, the teleport menu, the Teleport Stone, the flash and the ordinary map jump that carries the party, the arrival presentation in the destination zone, the crystal number that tells a save crystal from a gate crystal, and the two bits in the save image that switch saving and teleporting off, with every other bit of that flag byte and the script verbs that set them. | 0x00350240, 0x00351940, 0x00350600, 0x00351CE0, 0x00314D00, 0x00314C70, 0x00314B60, 0x00314B00, 0x003149E0, 0x00314A00, 0x0026DB30, 0x00352C80, 0x00264CA0, 0x00264E40, 0x002649B0, 0x00264AE0, 0x00264CE0, 0x00342490, 0x00343010, 0x0034AC10, 0x00314D80, 0x003462D0, 0x002E1A60, 0x002E0DA0, 0x002E1690, 0x002E0650, 0x00352E00, 0x00346DA0, 0x00254710, 0x002E09A0, 0x00254B50, 0x002E1BA0, 0x0022B8C0, 0x00356500, 0x00359C60, 0x0030F4B0, 0x0030F3F0, 0x0030F4D0, 0x0030F690, 0x0030F340, 0x0030F5A0, 0x00237CA0, 0x0034AAB0, 0x002FEAC0, 0x003567F0, 0x003529B0, 0x0036E6B0, 0x0024DE70, 0x003B0AD0, 0x0024E210, 0x00344170, 0x00269060, 0x00268690, 0x0036E700, 0x00314DA0, 0x00183070, 0x001D8770, 0x0034F870, 0x0034FDC0, 0x00350AE0, 0x00346E10, 0x00343CC0, 0x00349420, 0x00350FD0, 0x00351380, 0x00352080, 0x00314B80, 0x00314CD0, 0x00314CA0, 0x00314BB0, 0x00314BE0, 0x00314C40, 0x00314A60, 0x00314B40, 0x00314B20, 0x00314A80, 0x00314AA0, 0x00314AC0, 0x00314AE0, 0x00377700, 0x00377780, 0x00377BA0, 0x00377750, 0x00314530, 0x003145E0, 0x002695A0, 0x002628B0 |

## What the player sees

Walking up to a crystal only plays its touch effect.

Pressing confirm heals the whole party and revives
anyone who is down, then opens a short menu: save, teleport, or both, depending on which the story
currently allows. Saving
fades to black, opens the save screen and fades back in. A gate crystal also asks where to go:
choosing a place costs one Teleport Stone, plays a flash around the party, and the party appears
beside the destination crystal. The first time the party uses a gate crystal, that place joins
the list of destinations; Rabanastre's crystal joins it as soon as any zone with a crystal loads.

## How it works

### The crystal's script and its number

Every crystal is the `system_crystal_actor` of its zone's field script. The `us` script corpus
holds the same actor in 81 zone scripts, `alc_c01` among them, and the code below quotes that one.
Its `init` first makes sure the party owns key item `0x8040` (Rabanastre's crystal) and that the
item is in the destination array `g_menu_telepo_dest` (31 entries), then asks the engine which
crystal it is with `getcrystalid(3, 0)`.

`getcrystalid` is verb `0x30E`, handler `0x00352C80`. It pops the entry index and then the kind and
calls `0x00264CA0(kind, index)`; the result is the `u16` at the entry's `+0x14`, or -1 when there is
no entry. The lookup:

1. kinds 6 and 9 go to the global table reader `0x003DFAC0`; every other kind is mapped by
   `0x00264E40` to a list number: kinds 0, 1 and 2 to list 0, kind 3 to list 2, kind 4 to list 1,
   kind 5 to list 3, kind 8 to list 4, any other kind to no list;
2. `0x002649B0(list, index)` reads the list from the primary manager's payload: `0x00264AE0(list)`
   returns section `list` of the table at payload `+[0x70]` when slot 0's flag bit `0x1` is set
   (`0x00264AE6`);
3. a null payload (`0x00264AFE`), a zero table pointer from `0x0020E600` (`0x00264B0E`) or a list number
   at or above the table's count (`0x00264B1E`) gives no section; otherwise the section is the payload
   plus the list's signed offset at table `+4 + 4 × list` (`0x00264B22`-`0x00264B27`);
4. the section holds a count at `+0x00` and entries of `0x20` bytes from `+0x10`; an index at or
   above the count gives no entry (`0x002649D1`), and for lists 0 and 1 (`0x002649D5`) the entry's byte
   `+0x1C` must have the bit of value `1 << [0x02ADD0E8]` set (`0x00377860` reads that signed byte,
   `0x002649E1`-`0x002649FB`); `0x002649B0` returns the entry's address (`0x00264A02`-`0x00264A0D`), else 0.

The script keeps the number as the crystal's kind: 0 is a save crystal, 255 is the save crystal
with its own bind message, and every other value is a gate crystal. Number 4 counts as a gate
crystal only while `ismapjumpgroupflag(0x402A)` is set. The name tag is set with `setnpcname` from
the number ([NPC names](../Characters-And-Objects/npc-names.md)), and the crystal is an interactable object
(`setfreetargettype(4)`).

The explicit `switch` in `talk` names a gate crystal's destination key item: `0x803F + n` for the
21 numbers 1, 3-6, 8-13, 15 and 17-25, and `0x8059`, `0x805A`, `0x805B` and `0x805C` for 28, 29, 32
and 33; its `default` arm gives no key item.

### The two save-image bits

Saving and teleporting are each switched off by one bit of the flag byte at payload `+0x1062`, the
flag byte of the zone transition record ([save data fields](../Saving-Loading-And-Settings/save-data-fields.md),
[zone changes](zone-changes-and-mapjump.md)). Four script verbs read and write them:

| Verb | Id | Handler | Effect |
|---|---|---|---|
| `setsaveramtelepostatus(v)` | `0x305` | `0x00350240` | `0x00314D00(v == 0)`: bit `0x4` becomes 1 when `v` is 0, 0 otherwise |
| `getsaveramtelepostatus()` | `0x30A` | `0x00351940` | returns 1 while bit `0x4` is 0 (`0x00314B60`) |
| `setsaveramsavestatus(v)` | `0x306` | `0x00350600` | `0x00314C70(v == 0)`: bit `0x8` becomes 1 when `v` is 0 |
| `getsaveramsavestatus()` | `0x30B` | `0x00351CE0` | returns 1 while bit `0x8` is 0 (`0x00314B00`) |

So bit `0x4` means teleporting is off and bit `0x8` means saving is off; a script passes 1 to allow and 0
to forbid. The crystal reads both getters when it builds its menu: both allowed gives the
save-or-teleport question, saving alone gives a save prompt, teleporting alone a teleport prompt.

### Every bit of the flag byte

The same byte and the one after it carry six more script-controlled switches. Every instruction that
writes single bits of `+0x1062` and `+0x1063` belongs to a verb handler, to an engine function named in
the rows below, or to `0x00314A00` (after the table). The whole bytes are also written by the payload
clears and copies named in the last row:

| Bit | Set by | Reader | Meaning |
|---|---|---|---|
| `+0x1062` bit `0x1` | `setsaverambattlestatus(v)` `0x303` `0x0034F870` → `0x00314B80(v == 0)` | `getsaverambattlestatus` `0x308` `0x00350FD0`; `0x00377700` returns 1 only while the bit is 0 and byte 2 of the area's record has bit `0x1` clear | battle off |
| bit `0x2` | `setsaveramsummonstatus(v)` `0x304` `0x0034FDC0` → `0x00314CD0(v == 0)` | `getsaveramsummonstatus` `0x309` `0x00351380` only | summoning off |
| bit `0x4` | `setsaveramtelepostatus` (above) | `getsaveramtelepostatus`; `0x0026DB30` | teleporting off |
| bit `0x8` | `setsaveramsavestatus` (above) | `getsaveramsavestatus` | saving off |
| bit `0x10` | `setsaveramshutoralstatus(v)` `0x307` `0x00350AE0` → `0x00314CA0(v == 0)` | `getsaveramshutoralstatus` `0x30C` `0x00352080` only | script-defined switch |
| bit `0x20` | `0x00314530` sets it on the restore path, `0x003145E0` clears it when a jump is staged | `0x0026DB30` | a load is being restored |
| bit `0x40` | `setnavimapjamming(v)` `0x37D` `0x00346E10` → `0x00314BB0(v != 0)` | `0x00377780`, from the map screens `0x003C4070`, `0x004001D0`, `0x004006A0`, `0x00400E80`, `0x004017D0`, `0x00401D40` | the area map is jammed |
| bit `0x80` | `setmist(v)` `0x46A` `0x00343CC0` → `0x00314BE0(v)`: `v` at most 0 clears it and `+0x1063` bits `0x30`; a positive `v` sets it and stores `v & 3` in those bits | `0x00377BA0` (thunk `0x00320160`): the stored level when the bit is set, else bits under mask `0x3000` of the area's record | mist level override |
| `+0x1063` bits `0x3` | `setsaveramnavimapstatus(v)` `0x3C7` `0x00349420` → `0x00314C40(v & 3)` | `0x00377750`, from `0x003C5E00`, `0x003C6000`, `0x003C5FB0`: 1 gives 1, 2 gives 0, 0 and 3 give 1 | area map availability |
| `+0x1063` bits under mask `0x30` | `setmist` (above) | `0x00377BA0` | the mist level: while bit `0x80` of `+0x1062` is set, `0x00377BA0` gives it as the area's MP regime in place of the area's own bits under mask `0x3000` ([area flags](area-flags-navimapdata.md)) |
| `+0x1063` bit `0x40` | `0x0026A720`: a negative argument clears it and stores 0 at `+0x1534` (`0x0026A731`, `0x0026A73D`), any other sets it (`0x0026A74F`); the manager unload `0x002628B0` also clears it and stores 0 at `+0x1534` (`0x00262A6A`, `0x00262A76`, `ebp` zeroed at `0x0026292A`) | `0x0026DE20`, `0x0025D9E0`, `0x00261F90` | the music override at `+0x1534` is in force |
| `+0x1063` bits under mask `0xC` | no instruction sets them; the only write that names them is the clear `and 0xF3` in `0x00314A00` (`0x00314A51`) | no instruction tests them: `0x00314AC0` and `0x00314AE0` read only the bits under masks `0x30` and `0x3` (`0x00314AC9`, `0x00314AE9`) | carried only by the whole-byte writes: the payload clears (`0x002EF2E8`, `0x002EF603`, `0x002EF663`), the save read `0x002EF300` (`0x002EF317`) and the copy `0x00583C00`; `0x00583CB0` and `0x002EF570` copy the byte out |

`0x00314A00`, reached from `0x002695A0` in the manager unload `0x002628B0` (`0x00262CEF`), clears bits `0x1`,
`0x2`, `0x40` and `0x80` of `+0x1062` (`0x00314A09`-`0x00314A2D`) and the bits under mask `0x3F` of
`+0x1063` (`0x30`, `0x3` and `0xC`, `0x00314A39`-`0x00314A51`) when a zone is left. Bits `0x4`, `0x8`,
`0x10` and `0x20` are not touched there, so the save and teleport switches survive a zone change, as
the save image does.

Before it, `0x002695A0` calls `0x003590E0`, zeroes the four party entries at `0x0209A1F0` (`0x002695AF`,
`0x002695B7`), calls `0x0035A240` and clears the `0x200` bytes at `0x02099DF0` (`0x002695D3`). After it, it
calls `0x002341C0`, `0x00314010`, `0x00314DF0(-1)` and `0x00229F10(2 / [0x01DFE0B4])` (`0x002695DD`-`0x002695FE`),
then zeroes the 16 pointers at `0x0209A210` (`0x00269603`-`0x0026962F`).

### When teleporting is switched back on

`0x0026DB30` is called from the manager bind `0x0026C8C0` (`0x0026CD60`) and from `0x00266D10`
(`0x00267131`). Its teleport step:

1. it reads the persistence group of the field being entered (`0x003148F0`, payload `+0x1044`) and
   of the field being left (`0x00314870`, payload `+0x104C`); the group is word `+0x06` of the field's
   row in the field table at `[0x02099D88]`, and both read as 0 while `[0x02099D88]` or `[0x02099D90]` is null
   (`0x0026DB91`-`0x0026DB9D`, `0x0026DBC6`-`0x0026DBD2`), so no group change is seen then;
2. when the two differ and bit `0x20` is clear (`0x0026DBF4` tests `0x20`), it calls `0x003149E0`
   (`0x0026DBFD`), which clears bit `0x4`;
3. it clears the group persistent bank `0x02099FF0` (`0x200` bytes) on a group change, and again
   whenever the transition mode `+0x1054` (`0x003148D0`) has bit `0x8` set, the bit a teleport arrival
   carries.

The story also drives the bit directly. In the `us` corpus `setsaveramtelepostatus` is called only
by the opening event script `pre_z0000`, in one `switch` on the story counter that writes 0 or 1 by
range (17 arms, listed under Shipped data); `setsaveramsavestatus` is called by no shipped script.

### The heal

The crystal's `talk` function suspends battle, waits seven frames, calls `healall(0)` and
`btladjustsystem(1)`, and plays revive effect 11 on each party member who is down.

`healall(n)` is verb `0x3AF`, handler `0x00356500`: it maps `n` through `0x00359C60` and calls
`0x0030F4B0(-1, mask)`, which is `0x0030F3F0(mask)` for the nine party records (slot table 3 through
`0x00320AB0`) and `0x0030F4D0(mask)` for the thirteen Esper records `0x1B` to `0x27` (`0x00320A40`) whose
id `0xC012 + i` passes `0x0030B0E0`.

Both loops treat each record in a fixed order: first the statuses, through `0x0030F690` only when the
chosen sets together are not empty (`0x0030F464`, `0x0030F549`), then HP (`0x0030F340`), then MP
(`0x0030F5A0`) (`0x0030F468`-`0x0030F483`, `0x0030F54D`-`0x0030F56C`). Each of the three returns at once for a
null record. The mask bits:

| Mask bit | What is restored | Function |
|---|---|---|
| 1 | HP to its maximum (`+0x24`, doubled under status bit `0x10000000`; `max(HP, 1)` under status bit `0x10000`); an Esper record at or below 0 HP also gets `0x003243F0(unit)` | `0x0030F340` via `0x00300530(record, delta, 0, 0x217)` |
| 2 | MP to its capacity (`+0x28`, 0 while layer bytes `+0x6C` or `+0x7C` carry bit `0x80`): when the current MP `+0x4C` differs, `0x00300CE0(record, capacity - MP, 0x217)` (`0x0030F5FD`), then, while the capacity is above `+0x06`, `0x00300BC0(record, capacity - [+0x06], 0x217)` (`0x0030F617`); then the secondary word `+0x06` to capacity times `+0x37`, or to the capacity alone when `+0x37` is 0 (`0x0030F637`), through `0x00300BC0` with the difference when `+0x06` differs (`0x0030F64D`-`0x0030F679`) | `0x0030F5A0` via `0x00300CE0` and `0x00300BC0` |
| 4 | the statuses in set A, `[0x0208D320]` | `0x0030F690` → `0x0030E360(record, 0, status, 0, 0, 0x217, 0)` per bit, then `0x0030FED0(record, 0x217)` |
| 8 | the statuses in set B, `[0x0208D324]` | the same |
| 16 | statuses 2, 6, 8 and 10 (`0x544`) in addition | the same |

`0x00359C60` maps the argument: 1 and anything outside 1-5 give 7 (HP, MP, set A), 2 gives `0xF`,
3 gives 4, 4 gives `0xC`, 5 gives `0x10`. The crystal passes 0, so it heals HP and MP and clears
set A. The two sets are built by `0x00237CA0` from the status table at `[0x02EBF118]`: a status whose
row word `+0x06` has bit `0x2000` goes to set A, the others to set B.

`0x00237CA0` zeroes both sets first (`0x00237CCA`) and walks statuses 0 to 31 (`0x00237D3A`); the row of status `i` is
the decoded `+0x0C` of the table plus `i` times its word `+0x08`, added in 32 bits (`0x00237D09`-`0x00237D22`).

When status 0 (KO) is cleared, `0x0030F690` first finds the record's battle unit, the unit whose
`+0x698` is the record (`0x0031B860`, `0x0030F6CC`). It clears bit `0x4000000` of that unit's flag word
`+0x00` (`0x0030F6FC`) only when the record's status words `+0x3C | +0x64` hold one of the statuses
`0x80000003` (KO, Stone, X-Zone) and the area is not a town (`0x00377C20()` is 0,
`0x0030F6E5`-`0x0030F6FA`). A record clear of those statuses, a town, or a record with no battle unit
keeps the bit. The null test of `+0x698` (`0x0030F6E3`) never leads to the clear, since the unit's
`+0x698` is the record itself.

`btladjustsystem(n)` (`0x517`, `0x0034AAB0`) calls `0x002FEAC0(n)`: for an odd `n` it clears bit `0x1` of `0x022C3178`,
zeroes `0x022C3158`-`0x022C3167` and `0x022C3170`-`0x022C3177` and sets `0x022C3168` and `0x022C316C` to -1, with qword stores
(`0x003183A0`-`0x003183BE`).

That reset, `0x003183A0`, is reached directly from `0x002FEAC0`'s jump for an odd argument (`0x002FEAC3`), from the area
initialisation `0x002342F0`, with the battle system's up flag `0x02089300` non-zero, when `0x00377C20` answers non-zero
(`0x002342F4`, `0x00234446`-`0x0023444F`), from the scenario presets' function `0x00239960` for a valid pending preset
(`0x00239A85`) and from the battle-state reset `0x00237DF0` (`0x00237E3C`) ([kill
chain](../Rewards-EXP-Gil-And-Loot/kill-chain.md)).

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

`setnowjumpindex` (`0x3D1`, `0x0034AC10` → `0x00314D80`) writes payload `+0x1048`, the entrance of the
transition record. While the save screen is open the record therefore names entrance -2 (with one exception,
below), which the
entrance resolver `0x00264CE0` turns into the zone header's `+0x78`, the save entrance; -1 becomes
`+0x52`, the teleport-arrival entrance, -3 becomes `+0x7A`, any other negative value `+0x52`, and
the result is never negative.

The exception is field 403, Valley of the Dead: while the story counter is below 1,345 (`0x541`), the script heals
the party again (`healall(0)`) instead of setting -2, so the record keeps the entrance it had.

The resolver runs these tests one after another on the current value (`0x00264CED`-`0x00264D0C`), so a
negative header word is resolved again by the later tests, and a negative result becomes 0
(`0x00264D10`-`0x00264D14`). With no header (the pointer or the header pointer it holds null,
`0x00264CE0`-`0x00264CEB`) it returns the entrance as it came, or 0 when that is negative.

`gettelepoindex` (`0x32D`, `0x00342490`) and `getsaveindex` (`0x32E`, `0x00343010`) return those two
header words, sign-extended, of the primary manager's payload (`0x00263FF0(0)`, `0x003424A1`,
`0x00343021`), written through `0x0026B4E0` as the verb result; with no image loaded (the record's
`+0x00` null) they return 0 (`0x003424A9`, `0x00343029`).

`openfullscreenmenu_48d` (`0x48D`) is durative:

1. Start `0x003462D0` stores the byte `0x02064AD0` (`0x00229EB0`) at `ctx + 4` and 0 at `ctx + 8`, pops
   the parameter and then the id, and calls `0x002E1A60(id, param)`, `0x002E1690` (latch `0x0215F1A1` = 1)
   and `0x002E0650` (done byte `0x0215F1AE` = 0).
2. `0x002E1A60` maps the id through `0x002E0DA0`: with bit `0x8000` preserved (`0x002E0DA6`), the id with
   bit `0x8000` cleared (`0x002E0DA2`) 0 gives `0x11`, 1 gives `0x12`, 2 gives `0xA`, 3 gives `0xF`,
   4 gives `0x13`, 5 gives 6, 6 gives `0x16`, anything else 2, an id with a bit above `0x8000`
   included (`0x002E0DAC`);
   - for that cleared id 6 the parameter is remapped (0, 1, 2 to `0x40`, `0x41`, `0x42`, else 0;
     `0x002E1A74`-`0x002E1AA1`).
   The crystal's `0x8005` becomes category `0x8006`.
3. Unless the latch is already set, or the category is 2 while `0x002E0FA0()` has bit `0x1`, it writes
   `0x0215F1A0` = 1, `0x0215F1A4` = category and `0x0215F1A8` = parameter.
4. Poll `0x00352E00` returns 1 (keep waiting) while `0x0215F1AE` is 0 (`0x002E0F80`).
5. End `0x00346DA0` pushes `0x00254710()`: the word at `[0x0209BE80] + 0x10FAC` when the menu state
   `0x020927D8` is `0x11` or `0x12`, else 0. The crystal script ignores it.

The request is consumed by the per-frame menu router `0x002E09A0`, run from the world tick
`0x00314020` ([UI request router](../Menus-And-HUD/menus.md)):

1. the request is admitted when `0x0215F1A0` is set and either the category is below `0x14` with its
   bit in `0xE9000`, or `0x00226BA0()` returns 0, or `0x0053DD10()` returns non-zero;
2. the router calls `0x003591F0(0)` and `0x00254B50(category, param, 0)`, then clears `0x0215F1A0`;
3. `0x00254B50` refuses while `0x02092734` is 1 or the category's bit is in the block mask it builds
   from `0x01E0C2C0` under `0x002E0FA0()`, and then returns 0 (`0x00254B71`-`0x00254BC5`, `0x00254C40`); for
   `category & 0x7FFF` = 6 it takes the default arm,
   `0x0028F970()` then `0x00280A00(category, param, 0)`, the full-screen menu opener;
   - no word of `0x01E0C2C0` holds bit `0x40`, so category 6 is refused only by the latch;
   - before the default arm it calls `0x0017E7D0`, `0x0035DA80` and `0x003C8990` (`0x00254BC7`-`0x00254BD1`);
4. the done byte is written by `0x002E1BA0` (`0x0215F1AE` = `0x0215F1AF` = 1), whose only caller is the
   menu driver `0x0022B8C0` in its close-full-menu arm (`0x0022BB8D`, when `0x002E05C0()` is 0),
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

The warp is the ordinary `mapjump` verb with mode 10 (bits `0x2` and `0x8`), so it goes through the
`mapjump` poll and `0x00314440` exactly as [zone changes](zone-changes-and-mapjump.md) describes; the
destination field and entrance are authored per key item (the table under Shipped data).

`effectteleposyncbyid` (`0x43D`) is durative. Start `0x003567F0` stores the popped effect handle in
`ctx + 0`; Poll `0x003529B0` keeps waiting while the handle is non-zero and `0x0036E6B0(handle)` is
true. The test:

1. `0x0024DE70(handle)` switches on the handle's top nibble: 1 to `0x002FCA00`, 5, 6 and 9 to
   `0x003B0AD0`, 7 to `0x003B2510`, 8 to `0x00375AE0`, anything else gives 0;
2. a result of 2 or 3 means the effect is still playing, provided `0x0024E210(handle, 3)`, bit `0x80` of
   the effect record's `+0x36A`, is still 0 (`0x0036E6C3`-`0x0036E6D7`); any other result ends the wait;
   - `0x0024E210(handle, s)` looks the record up in the list `[0x020910F0 + 8 × top nibble]`, following
     `+0x348`, as the one whose words `+0x04` and `+0x06` equal the handle's low and high 16 bits
     (`0x0024E225`-`0x0024E24F`). Selector `s` 0 to 5 gives bit `0x20`, `0x40`, `0x100`, `0x80`,
     `0x200` or `0x400` of `+0x36A` as 0 or 1 (`0x0024E269`-`0x0024E2BC`);
   - it gives 0 when no record matches or `s` is above 5 (`0x0024E251`), so an effect whose record has
     left the list still counts as playing while `0x0024DE70` answers 2 or 3;
3. for the effect pool, `0x003B0AD0` returns 2 for an effect whose byte `+0x370` is 0 and 3 for 1
   or 2, once its word `+0x378` has bit `0x100`:
   - it finds the handle among the 36 entries of 24 bytes at `0x02EBEC00` by their first dword, and
     returns 0 when no entry holds it or the entry's pointer `+0x08` is null
     (`0x003B0AD0`-`0x003B0B04`);
   - with bit `0x100` clear, or a byte `+0x370` above 6, it returns 1 (`0x003B0B12`, `0x003B0B1E`);
     byte 3 gives 5 and bytes 4 to 6 give 4 (`0x003B0B3F`, `0x003B0B45`), so only 0, 1 and 2 keep the
     wait going.

### The arrival

The destination zone's `system_terepo_ctrl` tests `(getmapjumpmode() & 8) && nowjumpindex() ==
gettelepoindex()`. When true, `init` sets mode bit `0x10` (`setmapjumpmode(mode | 16)`), cancels the
fade and holds the screen white, and `main` plays sound 96, calls `calltelepoeffect()`, waits and
fades in. `calltelepoeffect` (`0x333`, `0x00344170`) is `0x00269060()` then `0x00183070()`:

- `0x00269060` runs `0x00268690(9)`: for each of the four party entries `0x0209A1F0[0..3]` that is set and
  passes `0x002EA6A0`, the encoded handle (`0x003589B0`) is collected (`0x002686D0`-`0x00268703`).
- With at least one handle, `0x0036E700(0, n, handles, 9)` plays `0x003B02A0(0, handles, n, [0x01EF9400 + 9 * 4], 5)`,
  the dword being `0x8C`, then `0x0024F920(handle, 1)` for a non-zero result only
  (`0x0036E72C`-`0x0036E737`); with no handle nothing plays and `0x00268690` returns 0 (`0x0026871C`).
- `0x00269060` then calls `0x00314DA0(0x003148D0() & ~0x18)`, which clears mode bits `0x8` and `0x10` in
  payload `+0x1054` (`0x0026906E`-`0x0026907C`).
- `0x00183070` runs `0x001D8770` on the loading page `[0x01F82CD8]` (`0x001D8A60`; built by `0x001D89D0` with
  the `LoadingPage` vtable): `+0x08` = 0; when the fading-out byte `+0x24` is 0 it becomes 1 and the
  fade timer `+0x20` is zeroed; the armed byte `+0x1D` = 0. The loading page starts fading out.

The field pass runs the same two calls once the field has settled after any arrival whose mode has
bit `0x8` ([field runtime](../Characters-And-Objects/field-runtime.md)).

## Layouts

Struct ZoneTransitionFlags base=payload+`0x1062` size=2:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | flags1 | bit `0x1` battle off, bit `0x2` summoning off, bit `0x4` teleporting off, bit `0x8` saving off, bit `0x10` script switch, bit `0x20` restore pending, bit `0x40` map jammed, bit `0x80` mist override |
| `+0x01` | `u8` | flags2 | mask `0x3` map availability, mask `0x30` mist level, bit `0x40` music override in force |

Struct MenuRequest base=`0x0215F1A0` size=`0x10`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | pending | 1 while a full-screen menu is requested (`0x002E1A60` sets, `0x002E09A0` clears) |
| `+0x01` | `u8` | latch | 1 from `0x002E1690` until the router clears it |
| `+0x04` | `u32` | category | `0x002E0DA0`(id); `0x8006` for the crystal's save screen |
| `+0x08` | `u32` | parameter | the popped parameter, remapped for id 6 |
| `+0x0E` | `i8` | done | 0 from `0x002E0650`; 1 from `0x002E1BA0` when the menu closes |
| `+0x0F` | `i8` | done2 | 1 from `0x002E1BA0` |

```python
heal(mask):
  bit 0x1   HP   = max HP  # 0x0030F340
  bit 0x2   MP   = capacity  # 0x0030F5A0
  bit 0x4   clear statuses in [0x0208D320]
  bit 0x8   clear statuses in [0x0208D324]
  bit 0x10  clear statuses 0x544 as well
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
| `recoverentry` (`0x6C`, durative `0x00345A30`/`0x00346020`) | 4 | 5 |

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
| `0x8040` | `306` | `4` | `0x8052` | `823` | `0` |
| `0x8042` | `630` | `0` | `0x8053` | `1101` | `0` |
| `0x8043` | `66` | `0` | `0x8054` | `751` | `0` |
| `0x8044` | `157` | `4` | `0x8055` | `768` | `4` |
| `0x8045` | `176` | `0` | `0x8056` | `742` | `3` |
| `0x8047` | `756` | `3` | `0x8057` | `129` | `0` |
| `0x8048` | `188` | `3` | `0x8058` | `350` | `0` |
| `0x8049` | `718` | `0` | `0x8059` | `1151` | `7` |
| `0x804A` | `791` | `0` | `0x805A` | `386` | `1` |
| `0x804B` | `360` | `0` | `0x805B` | `488` | `0` |
| `0x804C` | `403` | `3` | `0x805C` (the `default` arm) | `142` | `3` |
| `0x804E` | `450` | `4` |  |  |  |
| `0x8050` | `686` | `1` |  |  |  |
| `0x8051` | `594` | `3` |  |  |  |

The common effect table `0x01EF9400` holds `0x72, 0x73, 0x74, 0x75, 0x76, 0x88, 0x87, 0x89, 0x8A,
0x8C, 0x8D, 0x95, 0x8B, 0x96`; entry 9 is `0x8C`, the arrival flash.

### Every crystal

[`save-and-teleport-crystals-list.tsv`](save-and-teleport-crystals-list.tsv) lists the 81 field scripts that hold
`system_crystal_actor`, one crystal each: the zone with its map and region name, the number `getcrystalid(3, 0)`
returns for it (entry 0 of list 2 in the script's `+0x70` table, its `u16` at `+0x14`), the kind that number gives, and
for a gate crystal its key item and where teleporting to it arrives.

The same entry gives the spot where the crystal stands. `init` places the actor with `setposbynaviicon(3, 0)`
(`0x030D`, `0x00352430`). That verb reads the entry through `0x003DFBE0`, `0x003DFDD0` and `0x00264CA0`, then passes the floats
at `+0x00`, `+0x04`, `+0x08` and `+0x0C` to `setpos2_20d` (`0x00350C30`). The table's `x`, `y` and `z` columns give the
position, and `facing` gives the heading in radians. All 81 entries carry a spot.

- 56 are save crystals (number 0) and 25 are gate crystals, numbered 1, 3-6, 8-13, 15, 17-25, 28, 29, 32 and 33: each
  number once, the same 25 the `talk` switch names. Number 4, in Barheim Passage's North-South Junction, is a gate
  crystal only while map-jump group flag `0x402A` is set. No crystal has the number 255.
- Every gate crystal's destination is its own zone, so teleporting to an area's key item arrives at that area's
  gate crystal.
- `mic_b07.ebp` holds a save crystal but no resource-kind 5 path names the script, so no zone loads it and the
  player never meets that crystal.

## Operations

- Using a crystal is a script action of its `talk` function: `healall`, `btladjustsystem`, the key-item grant and
  the destination array write are all script verbs.
- The save screen is a UI request of category `0x8006` raised by the script; the script sits in
  the `openfullscreenmenu_48d` Poll until `0x0022B8C0` writes the done byte, so the crystal is held
  for as long as the save screen is open.
- A teleport is `mapjump(field, entrance, 10)`: it has no transition path of its own, and the
  destination zone recognises it by mode bit `0x8` and the arrival entrance `+0x52`.
- The save and teleport switches travel in the transition record of the save image: a loaded save
  brings its own values, and the restore path's bit `0x20` keeps `0x0026DB30` from re-enabling teleport
  during the load.

## State

| Address | Kind | Role |
|---|---|---|
| payload `+0x1062`, `+0x1063` | u8, u8 | the flag bytes above (`0x002EF2B0` base) |
| payload `+0x1048` | i32 | the staged entrance `setnowjumpindex` writes |
| payload `+0x1054` | u32 | the transition mode; bit `0x8` teleport arrival, bit `0x10` arrival presentation running |
| `0x0215F1A0`-`0x0215F1AF` | struct | the menu request |
| `0x020927D8` | i32 | the menu state `0x00254710` tests for `0x11` and `0x12` |
| `0x0208D320`, `0x0208D324` | u32 | status sets A and B (`0x00237CA0`) |
| `0x022C3158`-`0x022C3178` | mixed | the fields `btladjustsystem(1)` resets |
| `0x02099FF0` | u8[0x200] | the group persistent bank `0x0026DB30` clears on a teleport arrival (`0x0026DC2E`) and on a persistence group change (`0x0026DC11`) |
| `0x0209A1F0` | ptr[4] | the party entries the arrival flash plays on |
| `0x01F82CD8` | ptr | the loading page `0x00183070` fades out |
| `g_menu_telepo_dest` | u16[31] at script global `0x0BF2` | the registered destinations |

## Modding notes

- To open or close a gate crystal, set or clear bit `0x4` of payload `+0x1062` (or call
  `setsaveramtelepostatus`); the next use of a crystal rebuilds its menu from the two getters.
- A new destination needs a key item named in the `talk` switch, an entry in the `telepoeffect`
  switch of every crystal script and a crystal script answering `getcrystalid(3, 0)` with `n`; the
  engine side needs no change.
- The Teleport Stone cost, the list and the key items are inventory and script-global writes;
  `mapjump` mode 10 and the `+0x52` entrance are what the destination needs to run its arrival.
- The heal is `heal(7)`: changing the crystal to cure set-B statuses means `healall(2)` in the
  script, or moving a status into set A by setting bit `0x2000` of its status-table word `+0x06`.

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
- [`group-persistent-bank-accesses.tsv`](group-persistent-bank-accesses.tsv): every access to the group
  persistent bank `0x02099FF0` (`0x200` bytes): its copy out to the save (`0x0025D8E0`) and back (`0x00269A20`) (70 rows).

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Random numbers** (explained on [enemy respawning](../Enemy-Spawning/enemy-respawning.md))

| Function | | Functions |
|---|---|---|
| `0x002342F0` | calls | `0x00328D80` |

</details>
