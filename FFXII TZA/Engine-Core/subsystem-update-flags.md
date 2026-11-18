[Home](../../README.md) / [Engine core](README.md) / Subsystem update flags

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Subsystem update flags: the enable word that switches the sixteen interface update groups on or off each frame | system | Engine core | Main loop and game states | One dword at 0x01E0C464, all ones in the shipped image and written by nothing, that the interface pump tests sixteen times a frame to decide which update groups of the UI manager object run: the sixteen groups in their frame order with their masks, the extra gates each carries, the sub-object of the manager each handler receives, where the pump sits inside the field frame, and the second word that enables the one group gated twice. | 0x0028E290, 0x002507C0, 0x00289970, 0x001EDE80, 0x003F8B40, 0x002917E0, 0x0028C4C0, 0x0028D1C0, 0x003F6BB0, 0x003F7050, 0x003F9F40, 0x00291B90, 0x003F6100, 0x003F24D0, 0x003F24A0, 0x0030C300, 0x003F80D0, 0x00296860, 0x00290CF0, 0x00290EB0, 0x003F8EC0, 0x003F31B0, 0x003FA790, 0x002C6180, 0x0028C870, 0x002547C0, 0x00253970, 0x00184960, 0x00184950, 0x00226280, 0x0036D840 |

## What the player sees

Nothing changes on screen because of this word: it ships with every bit set and nothing in the
game clears one. What it describes is the order in which the interface advances each frame: the
widgets, the menus, the battle display and the message boxes are sixteen update groups run one
after another by one pump, and every group first asks this word whether it may run. A build that
cleared a bit would freeze that part of the interface while the rest kept moving.

## How it works

### The word and its reader

`0x01E0C464` is a dword that holds `0xFFFFFFFF` in the image. Its sixteen read sites are all inside
`0x0028E290`, the interface pump, and no instruction in the image writes it. The pump tests
the bits under mask `0xEF` as byte tests and the bits under mask `0xFF00` as dword tests; bit `0x10` (`0x0010`) is tested
nowhere. Bit `0x2` is tested twice, so sixteen tests gate sixteen groups over fifteen distinct bits.

The dword before it, `0x01E0C460`, is the `UISize.json` cell `mHelpMessageFontCount`. `0x001AF470` stores its address
in a layout slot (`0x001AF5C0`), and the loader writes the cell through that slot as a dword (`0x001CA985`-`0x001CA993`,
[screen layouts](../Menus-And-HUD/screen-layouts.md)), so the store ends at `0x01E0C463` and never reaches this word.

### Where the pump runs

`0x002507C0(first)` is the pump's only caller. The field frame calls it with 1 once per pass when
the `0x002878A0` predicate holds, `0x003583A0()` holds and the time accumulator is 0, and with the
first-step flag once per simulation step when `0x003583A0()` holds; the title and loading state
calls it with 0 ([frame update order](frame-update-order.md)). It runs:

1. `0x02092748` = 1 around `0x00184960(1 + (0x001D6B70() < 1))` ([startup constants](startup-constants.md)),
   then `0x02092748` = 0; everything below only unless `0x002287A0()` holds;
2. `0x0208F570 += 0x00184950()`, and, when `first`, `0x00254CC0`, called with that value in `ecx` but not
   reading it: it adds the dword `0x022CA624` that `0x0035E790` answers (`0x00254CE9`-`0x00254CF8`);
3. `0x0035BC40`, `0x003C6000`, `0x002481A0`, `0x00248030` on the four objects `0x0208EA28`, `0x0208EA40`,
   `0x0208EA48` and `0x0208EA50`, `0x00248190`, `0x002481C0` when `first`, `0x00244980` on the same four;
4. `0x003BBA60` when the 60 fps predicate `0x001EDE80` holds;
5. the pump `0x0028E290([0x01E0C2B0])`;
6. `0x00367200` of `0x00184950()` when `first`, and `0x00228930`.

### The sixteen groups, in frame order

Every group works on the UI manager object at `[0x0209BE80]` ([UI request
router](../Menus-And-HUD/menus.md)); the table gives the handler, the extra
condition the pump adds, and the sub-object or field the handler receives.

| # | Mask | Width | Extra gate | Handler and argument |
|---|---|---|---|---|
| 1 | `0x0001` | byte | | `0x00289970(manager + 0x5380)` |
| 2 | `0x0002` | byte | `0x001EDE80()` non-zero | `0x003F8B40(manager + 0x80)` |
| 3 | `0x0004` | byte | | `0x002917E0(manager, [+0x10F6C], [+0x10F70], [+0x10F72])` only with `+0x10F68` bit `0x8`; then, under the enable bit alone, with `[+0x10F00]` set `0x0028C4C0([+0x10F00])` (`0x0028E328`) and `+0x10F00 = 0x0028D1C0([+0x10F00])` (through the jump `0x0028C4B0`, `0x0028E334`), which frees every ring whose state `+0xD54` is 5 (`0x0028D1E0`, unlinked from the `+0xD70` next and `+0xD68` previous chain and released through `0x0028FA50` at `0x0028D23A`) and returns the first remaining ring, or 0 when every ring went (`0x0028D251`), else `+0x10EF0` = 0 |
| 4 | `0x0008` | byte | `[+0x10F30]` set | `0x003F6BB0([+0x10F30])` (`0x0028E369`), then `+0x10F30 = 0x003F7050([+0x10F30])` (`0x0028E375`), which frees every mark whose state `+0x2F0` is 4 (`0x003F7070`, unlinked from the `+0x300` next and `+0x308` previous chain and released through `0x0028FA50` at `0x003F70CA`) and returns the first remaining mark, or 0 when every mark went (`0x003F70E1`) |
| 5 | `0x0020` | byte | `[+0x10F78]` set | `0x003F9F40(manager + 0x57E0)` |
| 6 | `0x0002` | byte | the pump argument's bit `0x1` | `0x00291B90(manager)`, which frees every line of the `+0x10F10` list whose state `+0x850` is 5 (`0x00291BC0`, released through `0x00273B40` with the pool `[+0x10FC0]` at `0x00291C3F`) and moves `+0x10F10` past a freed head (`0x00291BE1`), `0x003F6100([+0x10F10])`, and with `[+0x10F20]` set `0x003F24D0([+0x10F20])` (`0x0028E3D8`-`0x0028E3E4`) rebuilds `+0x10F20`: it frees every mark whose state `+0x9C0` is 5 or 0 (`0x003F24FE`-`0x003F2507`, released through `0x0028FA50` at `0x003F2557`) and returns the first remaining mark, or 0 when every mark went (`0x003F256E`), and `0x003F24A0` runs on the new object |
| 7 | `0x1000` | dword | | `+0x10F68` bit `0x2` = bit `0x1` of `0x0030C300()` (through the jump `0x00273900`, `0x0028E410`-`0x0028E427`); `0x0030C300` stores the members of the nine party slots (`0x00320AB0(i, 1)`) whose status words `+0x64` or `+0x3C` carry no bit of `0x80000003`, or that are in a town (`0x00377C20`), into the roster array `0x022C1740` in slot order (`0x0030C34A`-`0x0030C360`), then returns 1 when one of them carries bit `0x40000000`, Libra (`0x0030C38A`, `0x0030C3B3`), else 0 (`0x0030C398`) |
| 8 | `0x0040` | byte | | `0x003F80D0(manager + 0xA0D0)` |
| 9 | `0x0080` | byte | | `0x00296860(manager + 0x7FB0, 6)` |
| 10 | `0x2000` | dword | | `0x00290CF0(manager)` |
| 11 | `0x4000` | dword | | `0x00290EB0(manager)` |
| 12 | `0x0100` | dword | `+0x10F68` bit `0x100` | `0x003F8EC0(manager + 0xA0)` |
| 13 | `0x0200` | dword | `[+0x10F40]` set | `+0x10F40 = 0x003F31B0([+0x10F40], 0x00290DF0)`, which steps every mark (`0x003F30D0`, `0x003F31E7`), unlinks each mark whose `+0x50` has bit `0x2` from the `+0x70` next and `+0x78` previous chain and hands it to the callback `0x00290DF0`, which frees it (`0x003F31EC`-`0x003F322D`), and returns the first remaining mark, or 0 when every mark went (`0x003F3246`) |
| 14 | `0x0400` | dword | | `0x003FA790(manager + 0x57E0)` |
| 15 | `0x8000` | dword | `[+0x10F80]` set | `0x002C6180([+0x10F80])` (`0x0028E536`-`0x0028E542`), the part that draws marks over units ([HUD](../Menus-And-HUD/hud.md)) |
| 16 | `0x0800` | dword | | `0x0028C870(manager + 0x7EA0)`, the pump's last act |

The order is not the bit order: bit `0x1000` runs seventh, bits `0x2000` and `0x4000` before bit `0x100`, and bit `0x800` last.
Bit `0x2` gates two groups at two points of the frame, the second only when the pump's argument has
bit `0x1`.

The argument is the 16-bit word `0x01E0C2B0`. `0x00253970`, the interface start-up, stores
`0xF` there (`0x002539E5`) and the same `0xF` in the HUD draw word `0x01E0C2AC` (`0x002539D9`). `0x00226280`, the
world-lock apply that runs at the end of every field frame, stores through
`0x002547C0` the value `0xF` when the AND of the lock table's first words has bit `0x1000000000`, else `0xE`,
with bits `0x4` and `0x8` cleared when that AND lacks bit `0x2000000000`. So a lock record that clears bit `0x1000000000` skips group 6 for
every frame it is held, while the other fifteen groups keep running.

`0x0036D840(on)` sets or clears bits `0x4` and `0x8` of two remembered words, `0x02EC0B24` and `0x02EC0B28`, and stores the
first through the same setter and the second as the HUD draw word `0x01E0C2AC` (`0x00254840`, `0x0036D873`;
[HUD](../Menus-And-HUD/hud.md)).

Script verbs call `0x0036D840`: `setmenuhptargetshowstatus` (`0x2A7`, `0x0034D700`); `0x003B7080`, the body of
`duplicatepartyinfo_spattack` (`0x2A3`, `0x0034CF80`), with 0; and `0x003B7BB0`, `0x003B7C60` and `0x003B7E20`, the
bodies of `resumeposbattletarget` (`0x195`), `resumepartyinfo_spattack` (`0x2A4`) and `setpossummonspace`
(`0x191`, `0x003482E0`); `0x003B7C60` is also the begin step of `changetosummonparty` (`0x205`, `0x0034EA30`)
([party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md)).

## Layouts

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01E0C464` | `u32` |  | the enable word; `0xFFFFFFFF` in the image; readers: the sixteen tests in `0x0028E290`; never written. |
| `0x01E0C2B0` | `u16` |  | the pump argument; bit `0x1` enables group 6; writers `0x00226280` and `0x0036D840` through `0x002547C0`, and `0x00253970` |
| `0x0209BE80` | `void*` |  | the UI manager object |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00080` | `...` |  | group 2 sub-object |
| `+0x05380` | `...` |  | group 1 sub-object |
| `+0x057E0` | `...` |  | groups 5 and 14 sub-object |
| `+0x07EA0` | `...` |  | group 16 sub-object |
| `+0x07FB0` | `...` |  | group 9 sub-object |
| `+0x000A0` | `...` |  | group 12 sub-object |
| `+0x0A0D0` | `...` |  | group 8 sub-object |
| `+0x10EF0` | `...` |  | group 3's list |
| `+0x10F00` | `...` |  | group 3's rebuilt head |
| `+0x10F10` | `...` |  | group 6's two objects; with `+0x10F20` |
| `+0x10F20` | `...` |  | group 6's two objects; with `+0x10F10` |
| `+0x10F30` | `...` |  | group 4's object |
| `+0x10F40` | `...` |  | group 13's object |
| `+0x10F68` | `u32` |  | flags: bit `0x2` written by group 7, bit `0x8` gates group 3's `0x002917E0` call, bit `0x100` gates group 12 |
| `+0x10F6C` | `u32` |  | group 3's arguments |
| `+0x10F70` | `u16` |  | group 3's arguments |
| `+0x10F72` | `u16` |  | group 3's arguments |
| `+0x10F78` | `...` |  | group 5's gate |
| `+0x10F80` | `...` |  | group 15's gate |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02092748` | `u32` |  | set to 1 around the `0x00184960` call in `0x002507C0` |
| `0x0208F570` | `u32` |  | accumulates `0x00184950`() per `0x002507C0` call |

## Shipped data

| Fact | Value |
|---|---|
| the enable word | `0xFFFFFFFF` in the image, no writer |
| groups, distinct bits | 16, 15 (bit `0x10` unused) |
| test widths | 8 byte tests (mask `0xFF`), 8 dword tests (mask `0xFF00`) |
| `0x00296860`'s second argument | 6 |

## Operations

Per field-frame pass or simulation step in which `0x003583A0()` holds: `0x002507C0`, then the pump,
which runs each of the sixteen groups whose bit is set and whose extra gate holds, in the table's
order, ending in the tail jump to `0x0028C870`.

## State

The enable word; the pump argument word; the UI manager object's flag word `+0x10F68` and the
object pointers the gates test.

## Modding notes

- The word is an authored switch board left fully on; clearing a bit at run time is the only way
  to use it, since nothing in the game writes it.
- A port that iterates the bits under mask `0xFFFF` in order runs the groups in the wrong order; the frame order
  above is the one the handlers were written against.
- Bit `0x2` is one bit for two groups; a one-bit-per-subsystem design cannot express it.
- Groups are also switched off at run time outside the enable word: group 6 through the pump argument (a world
  lock whose record clears bit `0x1000000000` holds it for the lock's duration), group 12 through `+0x10F68` bit
  `0x100` (cleared at `0x0028FA93`, set at `0x0028FB00`) and group 3's `0x002917E0` call through bit `0x8` (cleared at
  `0x002909B3`, `0x00290A18` and `0x002917FE`).
- Half the tests are byte-wide: a port that stores the word as a byte loses the bits under mask `0xFF00`.

## Related

- [Frame update order](frame-update-order.md): where `0x002507C0` sits in the field frame.
- [UI request router](../Menus-And-HUD/menus.md): the UI manager object the
  groups update.
- [`subsystem-update-flags-manager-singleton-0209be80-accesses.tsv`](subsystem-update-flags-manager-singleton-0209be80-accesses.tsv):
  every access to the UI manager object, the battle HUD's owner object ([HUD](../Menus-And-HUD/hud.md)), reached
  through its pointer `[0x0209BE80]` (1,457 rows).
- [`subsystem-update-flags-manager-sub-0209be80-00a0-accesses.tsv`](subsystem-update-flags-manager-sub-0209be80-00a0-accesses.tsv):
  every access to its group 12 sub-object at `+0xA0` (83 rows).
- [`manager-sub-00a0e-ntry-accesses.tsv`](manager-sub-00a0e-ntry-accesses.tsv): every access to the 64
  `0x100`-byte entries from `+0x20` of that sub-object (51 rows).
- [`manager-sub-0209be80-5380-accesses.tsv`](manager-sub-0209be80-5380-accesses.tsv): accesses to its group 1
  sub-object at `+0x5380`, the part the EXP, LP and combo numbers go to (183 rows). A row in a loop over a pool or on
  a pool's list node gives the offset in entry 0; the accesses of `0x00289D70` through the pool B node it finds
  (`0x00289E19`, `0x00289E1D`, `0x00289E44`, `0x00289E60`, `0x00289E6A`, `0x00289F24`, `0x00289F29`) are not listed.
- [`manager-sub-5380-pool-a-entry-accesses.tsv`](manager-sub-5380-pool-a-entry-accesses.tsv): every access
  to the first of that part's three pools: 12 entries of `0x30` bytes from its `+0x0` (51 rows).
- [`manager-sub-5380-pool-b-entry-accesses.tsv`](manager-sub-5380-pool-b-entry-accesses.tsv): accesses to the second
  pool: 6 entries of `0x28` bytes from `+0x240` (63 rows). Not listed: the accesses of `0x00289D70` through the node it
  finds on the list at `+0x428` or appends (`0x00289E19`, `0x00289E1D`, `0x00289E44`, `0x00289E60`, `0x00289E6A`, `0x00289F24`,
  `0x00289F29`).
- [`manager-sub-5380-pool-c-entry-accesses.tsv`](manager-sub-5380-pool-c-entry-accesses.tsv): every access
  to the third pool: 6 entries of `0x28` bytes from `+0x330` (49 rows).
- [`subsystem-update-flags-manager-sub-0209be80-57e0-accesses.tsv`](subsystem-update-flags-manager-sub-0209be80-57e0-accesses.tsv):
  every access to its sub-object for groups 5 and 14 at `+0x57E0`, the world-object manager (481 rows).
- [`subsystem-update-flags-manager-sub-57e0-array-record-accesses.tsv`](subsystem-update-flags-manager-sub-57e0-array-record-accesses.tsv):
  every access to the first of the 13 `0x2A0`-byte records at that sub-object's `+0x270` through its direct routes;
  the later passes of the loop `0x003FA3A5`-`0x003FA3BA` and the walks over the `+0x278` chain are not listed (39 rows).
- [`subsystem-update-flags-manager-sub-0209be80-7ea0-accesses.tsv`](subsystem-update-flags-manager-sub-0209be80-7ea0-accesses.tsv):
  every access to its group 16 sub-object at `+0x7EA0`, the selection marker (124 rows).
- [`manager-sub-7ea0e-ntry-accesses.tsv`](manager-sub-7ea0e-ntry-accesses.tsv): accesses to the marker's two
  `0x20`-byte slots from its `+0x30` (50 rows). Not listed: the slot `0x0028CA40` picks from bit `0x2` of `+0x74`,
  cleared and filled at `0x0028CB4A`-`0x0028CB62` and passed on at `0x0028CB70`.
- [`subsystem-update-flags-manager-sub-0209be80-7fb0-accesses.tsv`](subsystem-update-flags-manager-sub-0209be80-7fb0-accesses.tsv):
  every access to its group 9 sub-object at `+0x7FB0`, the level-up blink part (90 rows).
- [`manager-sub-7fb0-record-accesses.tsv`](manager-sub-7fb0-record-accesses.tsv): accesses to that part's six
  `0x110`-byte records, one per unit whose level went up (95 rows). Not listed: `0x002966E0`'s accesses to the record
  `0x00299A30` returns (`0x00296715`-`0x0029675D`: the slots at `+0xF8` and the count at `+0x106`).
- [`subsystem-update-flags-manager-sub-0209be80-8fa0-accesses.tsv`](subsystem-update-flags-manager-sub-0209be80-8fa0-accesses.tsv):
  every access to its sub-object at `+0x8FA0`, the help block (187 rows).
- [`subsystem-update-flags-manager-sub-8fa0-slot-record-02b8-accesses.tsv`](subsystem-update-flags-manager-sub-8fa0-slot-record-02b8-accesses.tsv):
  every direct access to the two `0x2B8`-byte records from the help block's `+0xAC0`; the accesses of `0x002BE290`,
  `0x002BE300`, `0x002C0F30` and the record handler `0x002C0870` are not listed (60 rows).
- [`subsystem-update-flags-manager-sub-0209be80-a0d0-accesses.tsv`](subsystem-update-flags-manager-sub-0209be80-a0d0-accesses.tsv):
  every access to its group 8 sub-object at `+0xA0D0` (19 rows).
- [`manager-sub-0d0-record-accesses.tsv`](manager-sub-0d0-record-accesses.tsv): the address of the two `0x110`-byte
  elements at the start of that sub-object, taken at `0x0028E43D` (1 row). `0x003F7E80` picks element `[+0x980]` and
  reaches it through `0x00273A20` (`0x00273A22`) and through `0x00245000`, whose `0x002465F0` clears it (`0x00246626`) and
  writes `+0x0` and `+0x40` (`0x00246641`-`0x0024666D`).
- [`subsystem-update-flags-manager-sub-0209be80-ab30-accesses.tsv`](subsystem-update-flags-manager-sub-0209be80-ab30-accesses.tsv):
  every access to its sub-object at `+0xAB30`, the battle menu ([widgets](../Menus-And-HUD/widgets.md)), outside the element
  handlers `0x00279E20` and `0x002985D0` that its `+0` holds (152 rows).

In the `route` cells of these tables, `ManagerSingleton0209BE80` names the UI manager object and
`ManagerSub0209BE80_` with an offset its sub-object at that offset.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat AI: `0x00377C20` is called by `0x003014C0`, `0x00301AD0`, `0x00305AB0`; those functions are documented on
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [glossary](glossary.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Gameplay: `0x00320AB0` calls `0x0031B9F0`; `0x00377C20` is called by `0x00307D10`, `0x0030A8A0`, `0x0030C210`, `0x0030D9A0`; those
  functions are documented on [identifier spaces](identifier-spaces.md), [force fight mode](force-fight-mode.md),
  [enmity](../Enemy-AI-And-Gambits/enmity.md), [frame update order](frame-update-order.md).
- Input gameplay: `0x00377C20` is called by `0x00313A00`; those functions are documented on
  [force fight mode](force-fight-mode.md).
- Items equipment shops license: `0x00320AB0` is called by `0x002F9F20`, `0x0030A4E0`, `0x0030FAA0`, `0x0030FBE0`, `0x0030FD10`;
  `0x00377C20` is called by `0x00309FB0`, `0x0030FD10`; those functions are documented on
  [equipment](../Items-Equipment-Shops-And-Licenses/equipment.md), [stats](../Damage-And-Battle-Formulas/stats.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Rewards progression economy: `0x00320AB0` is called by `0x002F8BB0`, `0x00312280`; `0x00377C20` is called by `0x00312280`;
  those functions are documented on [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md).
- Status periodic terminal: `0x00320AB0` is called by `0x00310DB0`; `0x00377C20` is called by `0x0030E360`, `0x0030F690`,
  `0x00310DB0`; those functions are documented on [frame update order](frame-update-order.md),
  [force fight mode](force-fight-mode.md),
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- Actor entity: `0x003B7080` calls `0x003B6CC0`.
