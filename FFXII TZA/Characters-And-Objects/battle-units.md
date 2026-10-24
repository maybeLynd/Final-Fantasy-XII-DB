---
title: "Battle units: the pool of combat slots, who gets one, the actor class bits, the handle and the flag word"
kind: "system"
category: "Characters and objects"
addresses: "0x002368D0, 0x00234480, 0x00265A20, 0x00234200, 0x00236820, 0x00236850, 0x002367A0, 0x002134A0, 0x00263E30, 0x0031B760, 0x003589B0, 0x003588B0, 0x0031B7E0, 0x002659D0, 0x00265020, 0x00263C20, 0x00263D30, 0x00351610, 0x00238BF0, 0x00269FE0, 0x00269F30, 0x002659A0, 0x00267CC0, 0x0026AD00, 0x00263AC0, 0x00234D40, 0x0035A1C0, 0x0035A060, 0x0031C1A0, 0x0035A0C0, 0x0031BDC0, 0x004737A0, 0x004737D0, 0x00473690, 0x00318A90, 0x003206E0, 0x0030C3C0, 0x00237430, 0x00359EA0, 0x0031FCF0, 0x0031FD20, 0x00273780, 0x00273750, 0x00273A00, 0x00358960, 0x003BBC80"
---

## What the player sees

Everything that can take part in a battle, the party, guests and every enemy on the field, occupies
one of thirty-two combat slots. When the slots are all taken, the next thing that would join a
fight simply does not: it stands there without a unit, with no message and no error. Separately, a
small class field on every actor decides what the engine may do with it: a steerable character can
be moved and positioned, a placed object such as a door has a position but ignores movement, and a
trigger line can be given its six coordinates by a script.

## How it works

### The pool

`0x002368D0`, run when battle storage is set up:

1. zeroes `0x02089340` and `0x02089300`, writes the slot count `0x0208E6A0` = 32, frees a previous pool
   (`0x003844F0`) and allocates the pool `0x0208E688` as `32 * 0xF50` bytes under the name `BtlWork`
   (`0x00384510`) and zeroes it;
2. allocates the two `0x9400`-byte spawn-keep banks `0x0208E690` (`btlKeepCharWork1`) and `0x0208E698`
   (`btlKeepCharWork2`), runs `0x00383A20`, frees a previous `0x0208E680` (`0x00384500`), registers the
   static task `0x00238850` (`0x003843F0(0x13, ...)`) and runs `0x0030CF40` and `0x002EA5F0`;
3. zeroes the twelve qwords at `0x02EBF1A0`, sets `0x0208D455` to `0xFFFF`, `0x0208936C` to 300,
   `0x0208935C` to 5.0 and `0x02F973B8` to infinity, and requests the twelve job boards
   (`0x00238260(0..11)`).

A unit is `0xF50` (3,920) bytes; `0x00236850` returns the count and `0x00236820(i)` returns
`0x0208E688 + i * 0xF50` for `0 <= i < count` and null otherwise. `0x002367A0(selector)` scans the pool
for a unit whose stats record `+0x698` has the word `+0x04` equal to the selector, after
`0x00322C50(2, selector)` admits it; a selector of `0xFF` is compared as `0xFFFF`, so it matches that
word value rather than every unit.

### Allocation

`0x00234480(0, actor)` walks the pool from slot 0 for the first unit whose flag bit `0x1` is clear and
returns without doing anything when all are in use. For the free slot it:

1. zeroes the whole `0xF50` bytes and sets flag bit `0x1`;
2. writes the slot index to `+0xEA9`;
3. stores the unit pointer at the actor's `+0x30` (`0x002134A0`) and the actor at the unit's `+0x10`;
4. stores the actor's encoded handle (`0x003589B0`) at `+0x08`;
5. clears flag bit `0x200000` and copies the actor's entry-group word `+0xF6` (`0x00263D30`) into the byte
   `+0x57`.

### Who gets a unit

`0x00265A20(slot)` is the allocator's only caller. For the primary manager only (slot index 0) it
walks the slot's records (`0x00358940`, `recordCount` at `+0x20`) and, for each record whose byte
`+0x14` has bit `0x80` set, either enters the bind branch or, once 32 records have entered it in this
walk, clears the record's `+0x14` bit `0x10` instead. Every record that enters the branch is counted,
whether or not `0x00234480` found a slot; the branch gives the record:

- the frame callback `0x00233F70` at `+0x38` ([field runtime](field-runtime.md));
- `0x00234A00(unit, 1)` (unit `+0x20` = 1) when the back-pointer `+0x30` is set, which is how the walk
  notices a silent allocation failure;
- for a class-3 actor, bits `0x100` and `0x2000` of `+0x1C` cleared; `+0x0E` = `(old & 0xF1) | 1`;
- `0x00238FA0(record, 0x0031C4C0())` when byte `+0x12` is below 4;
- the `0x00359B80` object's `+0x40`-`+0x63` and byte `+0x65` cleared.

The number bound is stored at the slot's `+0x1E8`. Records of the other four managers never get a
unit.

### The handle

`0x003589B0(actor)` encodes an actor as `((actor u16 +0x16 & 0x7FF) << 20) | ((actor u8 +0x15 & 0xF) << 16) | actor u16 +0x00`:
the low word is the record's index in its manager, bits 16-19 the manager slot, bits 20-30 the
record's discriminator. `0x002659D0(actor)` advances the discriminator as `(old + 1) & 0x7FF`, with 0
replaced by 1, so it runs over 1 to 2047 and a handle taken before the advance stops resolving.

`0x003588B0(handle)` decodes it: 0 gives null; a selector of 5 or more gives null; the manager
`0x02098E10 + selector * 0x288` must have a record pool (`+0x08`) and a payload (`+0x00`), the index
must be below the slot's `+0x20` and the pool's own count, the slot's `+0x10` bit `0x1` must be set, the
entry must be non-null and the actor's full word `+0x16` must equal the discriminator. `0x0031B7E0`
then returns that actor's unit `+0x30` (`0x00263E30`) when `0x02089340` bit `0x10` is set; `0x0031B760(actor)`
is the null-guarded form of the same back-pointer read.

One such handle is the target of a committed action: the commit `0x0030F760` stores it at unit `+0x710` (`0x0030F7F2`-`0x0030F82A`,
[Action commit](../Battle-Actions/action-commit.md)).

Small predicates over the same reads serve the menus and the HUD: `0x0031FCF0(actor)` is true for a
non-null actor with a unit; `0x0031FD20(handle)` is true when `0x02089340` bit `0x10` is set and the handle
resolves to an actor with a unit; `0x00273780(handle)` is true for a non-zero handle that resolves;
`0x00273750(handle)` is true when the resolved actor's class nibble (`0x00263C20`) is 1 or 2, and
`0x00273A00(handle)` when it is 5. `0x00358960(slot, ordinal)` returns the class bits `+0x03 >> 5` of a
record of the slot `0x00263FF0` gives, and reads address 3 when the ordinal is out of range.

Three more read the unit behind a handle, through `0x003588B0` and, while `0x02089340` bit `0x10` is set, `0x00263E30`:

- `0x003229A0(handle)` returns bit `0x1` of the unit's `+0xE9C`, which `0x002392D0` copies from bit `0x4000` of its flag argument
  (`0x0023932A`-`0x00239339`).
- `0x00273910(handle)` is true when the actor's class nibble is 3 and `0x003229A0` returns 0 (`0x00273934`); the HUD's
  `0x002BFD20` asks it (`0x002BFE2A`).
- `0x00322950(handle)` is true when `0x00321770(unit, 0)` returns 0: none of the unit's 40 enmity bytes (`+0x1A` of
  `[unit+0x6A0]`, for the ids `0x00322C50(2, i)` accepts) is above 0 ([Enmity](../Enemy-AI-And-Gambits/enmity.md)).
  `0x002C7660` asks it (`0x002C780D`) right after `0x003229A0` (`0x002C77F6`).

### Release

`0x00234200(_, actor)` releases the actor's unit. With no unit it runs `0x00263980` and `0x003589A0` on
the actor and returns. Otherwise:

1. it runs `0x00300140(unit, 1)` and `0x00319140(unit, 2)`; with bit `0x2` of its second argument
   `0x00319140` calls `0x003BBC80(actor)`, which zeroes the first two qwords of every entry of the
   64-entry table at `[0x02B457D0]` (stride `0x50`) whose first qword is the unit's actor;
2. for an enemy (stats kind 1) with flag bit `0x10` set, unless a terminal status is present outside a
   town (`0x00377C20`), it copies the unit's position `+0xE0`-`+0xEF` into the spawn record's `+0x60`
   and the yaw `+0x160` into `+0x74`, and sets the spawn record's flag bit `0x4`
   ([spawn placement](../Enemy-Spawning/enemy-spawning.md));
3. it zeroes the whole slot and clears bit `0x1`; the test before the clear (`unit >= base`, else
   `unit < base + 32 * 0xEA7900`, and `0xEA7900` is `0xF50 * 0xF50`) cannot fail for any pointer.

### The actor class

Bits 5-7 of the actor's byte `+0x03` are its class, and bits 0-3 of byte `+0x0E` are a separate
nibble (`0x00263C20`). The class decides what code accepts the actor:

| Class | Test | Examples |
|---|---|---|
| 1 or 3 | `+0x03 >> 5` is 1 or 3 | `0x00265020` reads the position from the movement context `[actor + 0xB8]` and returns zeros otherwise |
| 3 | `(+0x03 & 0xE0) == 0x60` | the movement code: the field runtime's steering (`0x0025DF00`), the frozen pass (`0x0025E400`), the unit bind's `+0x1C` clear (`0x00265A20`) |
| 2 | `(+0x03 & 0xE0) == 0x40` | the `setline` verb `0x00351610`, which writes its six floats into the movement context at `+0x00`, `+0x04`, `+0x08`, `+0x10`, `+0x14` and `+0x18` |

### The refresh from the unit

`0x00238BF0(unit)` brings the bound actor (`+0x10`) in line with the unit's stats record and is what
sets the class nibble and the byte `+0x0F` of a fighting actor. It does nothing without an actor or
a stats record, or for a stats kind other than 0 and 1.

- A party member (kind 0) gets `+0x0F` = 3 and nibble 8 when its type is 27-39, and `+0x0F` = 2 and
  nibble 1 otherwise (`0x00269F30` writes `+0x0F`).
- An enemy (kind 1) whose spawn record byte `+0` has bit `0x20` clear turns a unit byte `+0x58` of 4 into
  1; with `+0x58` = 1 it runs `0x002659A0` and `0x0025D5E0(actor, 10)`, and raises `+0x58` to 7 when the
  enemy row's byte `+0x03` has bit `0x10`.
- An enemy whose spawn record has bit `0x20` set runs `0x00267CC0` and `0x0026B4A0(actor, 10)` instead.
- The nibble is then written by `0x00269FE0(actor, n)` with the value above, or the unit's `+0x58` for
  an enemy when it is not 0, and `0x0026AD00(actor, on)` sets `+0x13` bit `0x80` for an enemy whose class
  row byte `+0x18 & 0xE` is 4 and clears it otherwise.

The writers:

| Function | Writes |
|---|---|
| `0x00269F30(actor, v)` | `+0x0F` = `v` for a non-null actor |
| `0x00269FE0(actor, n)` | for class 3, `+0x1C` bits `0x100` and `0x2000` set when `n` is 4 (each followed by `0x00268EA0` when `+0x0B` bit `0x8` is set) and cleared otherwise; then nibble = `n & 0xF`. The verb `setfreetargettype` (`0x0265`, `0x003528C0`) calls it on the calling actor with a popped `n` |
| `0x002659A0(actor)` | `+0x1C` bits `0x100` and `0x2000` cleared, nibble 5, `+0xF4` = 0 |
| `0x00267CC0(actor)` | `+0x1C` bit `0x8` cleared, bits `0x100` and `0x2000` set (with `0x00268EA0` as above), nibble 4, `+0xF4` = 2 |
| `0x0026AD00(actor, on)` | `+0x13` bit `0x80` = `on != 0` |

`0x00263AC0(actor)` reads `+0x0F` back: 0 for a null actor, 1 instead of 2 when the actor is the party
focus (`0x003590D0`, `0x003588B0`, resolved with slot 0 as the current slot), else the byte itself.

`0x00263AA0(actor)` and `0x00263AB0(actor)` return the signed bytes `+0x21` and `+0x22` while `+0x0F` bit `0x40` is set, and 0
otherwise. The minimap's list build `0x003C5130` adds them to the actor's x and z (`0x003C51F5`, `0x003C520F`), so they
move the actor's marker off its position ([Map screens](../Menus-And-HUD/map-screens.md)).

### The script queries

Script verbs read and change a fighting actor's state through its unit and stats record. The
`isdead`, status-read, `getequipitemid` and `getmpratio_1f7` verbs first pass their actor through
`0x00263F10`, which follows a record whose `+0x18` is 2 to the record its `+0x19` (manager) and
`+0x1A` (ordinal) name; the others use the calling actor as it is. A member argument goes through
`0x00264010` (a record of the current slot, or the party focus for a negative value), or through
the roster (`0x00263750`) for `getequipitemid_468`.

| Verb | Id | Helper | Result |
|---|---|---|---|
| `isdead`, `isdead_15f(ordinal)` | `0x015E`, `0x015F` | `0x003597B0` | 1 when `0x00234D40` gives 2, else 0 |
| `isdead2`, `isdead2_49f(ordinal)` | `0x049E`, `0x049F` | `0x003597D0` | `0x00234D40` itself |
| `playerstatus(bit)`, `getcharbattlestatus(bit)` | `0x00A9`, `0x0499` | `0x0035A1C0` | 1 when status bit `bit` is set in `+0x3C` or `+0x64` (`0x00320CA0`) |
| `getcharbattlestatus_49a(member, bit)` | `0x049A` | `0x0035A1C0` | the same for a member |
| `getbtlwork(i)` | `0x0110` | `0x0035A060` | unit byte `+0xEC0 + i`, sign-extended (`movsx`), for `i` below 16 (`0x0031C1A0`), else 0 |
| `getequipitemid(slot)` | `0x0351` | `0x0035A0C0` | the equipment word for `slot` (below), -1 for `0xFFFF` |
| `getequipitemid_468(member, slot)` | `0x0468` | `0x0035A0C0` | the same for roster member `member` |
| `getmpratio_1f7(member, percent)` | `0x01F7` | `0x004737A0` | MP for a percent of 0 or less, else `percent` of the capacity (`0x003206E0`) |
| `setcharbattlestatus(status, v)` | `0x01F0`, `0x01FC` with a member | `0x004737D0` | adds status `status` (`0x00318A90` mode 1, `0x0030EAE0`) |
| `clearcharbattlestatus(status, v)` | `0x01F1`, `0x01FD` with a member | `0x00473690` | removes it (`0x00318A90` mode 0, `0x0030E990`) |
| `isfusion_spattack(v)` | `0x02A1` | `0x0030C3C0` | 1 for `v` from 18 to 33, else 0 |
| `btlAtelIsMimicName` | `0x3062` | `0x00237430` | bit `0x20` of the spawn record's byte `+0` (unit `+0x6A0`), 0 without one |

`0x00234D40(actor)` returns 0 when the actor has no unit or unit flag bit `0x10` is clear, 2 when the stats
record is missing or its status words `+0x3C | +0x64` carry bit `0x1`, `0x2` or `0x80000000` while the town flag
`0x00313F60` is clear, and 1 otherwise.

The handle-based helpers `0x00320CA0`, `0x003206E0` and `0x00318A90` take the actor's handle
(`0x003589B0`), need `0x02089340` bit `0x10`, a unit and a stats record, and fail with -1 (0 for
`0x00320CA0`). `0x00318A90` refuses statuses 0, 1 and 31 with -2 and otherwise calls the add or remove
routine as `(stats, 0, status, -1, -1, 0x13)`. `0x003206E0(handle, which, percent)` reads HP `+0x48`
and capacity `+0x24` for `which` = 0 and MP `i16 +0x4C` and capacity `i16 +0x28` for 1; a percent of
100 returns the capacity and any other positive percent `percent * capacity / 100`, truncated.

`0x0031BDC0(words, slot)` reads the stats record's equipment words `+0x50` (`0x0031BD80`): slots 0-4
give the word itself and slots above 8 give `0xFFFF`. Slots 5, 7 and 8 give word 0 when
`0x00322560` reports that word 0's row in the equipment table `[0x02EBF0F8]` has byte `+0x26` equal
to `0x11`, and word 1 otherwise; slot 6 gives the other one. `0x0035A0C0` passes slots 1-5 through
and turns any other value into 0.

`0x00359EA0(index, focusFirst, includeHidden)` picks a party actor: it lists the members of
`0x0031B670` (up to four) followed by those of `0x0031B680`, drops members whose model is hidden
(`0x002E9600`: class 3 and context `+0x10` bit `0x8`) unless `includeHidden` is set, moves the party
focus record (`0x00264050(0)`) to the front when `focusFirst` is set and it is among the first four,
and returns entry `index`, or null past the end.

The verb `0x308C` (`0x0050F5B0`) calls it through
`0x00510870` with `focusFirst` = 1 and `includeHidden` = 0, and sets its result to 1 when a member
was picked and `0x00262F50` accepted it, 0 otherwise.

## Layouts

Struct BattleUnit size=`0xF50` count=32 base=[`0x0208E688`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u64` | flags | bit `0x1` slot in use; the table below |
| `+0x008` | `u32` | handle | `0x003589B0`(actor) at bind |
| `+0x010` | `u8*` | actor | the bound actor record |
| `+0x020` | `i32` | bound | 1 after the bind walk (`0x00234A00`) |
| `+0x057` | `u8` | entryGroup | actor `+0xF6` at bind |
| `+0x698` | `u8*` | stats | the combat stats record (unit-stats-fields page) |
| `+0x6A0` | `u8*` | spawnRecord |  |
| `+0xE68` | `u8*` | classRow |  |
| `+0xEA9` | `u8` | slotIndex |  |

Globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x0208E688` | `u8*` | the pool | `0x002368D0` |
| `0x0208E6A0` | `i32` | the slot count, 32 | `0x002368D0` |
| `0x0208E690` | `u8*` | btlKeepCharWork1 | `0x002368D0` |
| `0x0208E698` | `u8*` | btlKeepCharWork2 | `0x002368D0` |
| `0x02089340` | `u32` | zeroed by 0x002368D0; bit 0x10 gates 0x0031B7E0 |  |

### The flag word

Every immediate-mask write and test on `+0x00` and `+0x04` in the access table [`battle-unit-fields.tsv`](battle-unit-fields.tsv)
by bit, plus the unit reset `0x00236A60`'s register mask
`0xFFFF7FFDFFE7FFFD` (`0x00236A9C`-`0x00236AB1`), which clears bits `0x2`, `0x80000`, `0x100000`, `0x200000000` and `0x800000000000`:

| Bit | Set by | Cleared by | Tested by |
|---|---|---|---|
| 0 | `0x00234480` | `0x00234200` | `0x00234480` |
| 1 | `0x0023A570`, `0x00300E40` | `0x00236A60` | `0x00233F70`, `0x003125E0`, `0x00319F50`, `0x003243F0`, `0x00324470` and one more |
| 2 | `0x0023A570` | `0x00236A60` | `0x00233AD0`, `0x0023A570`, `0x0031A300`, `0x0031C000`, `0x00324380` and three more |
| 3 | `0x00233AD0` | `0x00236A60` | `0x00233AD0`, `0x00317E60`, `0x00319090`, `0x00319490`, `0x0031ACC0` and three more |
| 4 | `0x00233F70` | `0x00236A60` | 27 functions, among them `0x00233EA0`, `0x00234200`, `0x002350C0`, `0x00237D80` |
| 5 | `0x00308610` | `0x0030EFF0`, `0x00310780` | |
| 6 | `0x00324470`, `0x003266C0` | `0x00324450` | `0x00324450` |
| 8 | `0x00313500` | `0x00233EA0`, `0x00236A60`, `0x00301140`, `0x00306760`, `0x00313F70` | |
| 9 | `0x00319F50` | `0x00233EA0`, `0x00236A60`, `0x00301140`, `0x00306760`, `0x003082F0` | |
| 10 | `0x00319F50` | `0x00236A60`, `0x00301140` | |
| 11 | | `0x00236A60` | |
| 12 | `0x00304850` | | |
| 13 | | `0x00304850` | |
| 14 | | `0x00236A60` | |
| 15 | `0x00239170` | `0x00239170` | |
| 18 | `0x00236300` | `0x00236300`, `0x00325BB0` | |
| 19 | `0x00325260` | `0x00236A60` | |
| 20 | `0x003057D0` | `0x00236A60` | |
| 21 | `0x00239840` | `0x00234480`, `0x00300E40` | `0x00308D90` |
| 22 | `0x00312FA0` | | |
| 23 | | `0x00301140`, `0x0030F2D0` | `0x003081E0`, `0x00312FA0`, `0x00313F20`, `0x003176E0` |
| 24 | `0x00301140`, `0x00313500` | `0x003083A0`, `0x003250F0` | |
| 25 | `0x00313500` | `0x003083A0` | |
| 26 | `0x002354F0`, `0x002355A0`, `0x00235720`, `0x00238FA0`, `0x00239410`, `0x00300310` | `0x00233AD0`, `0x002393E0`, `0x0023A570`, `0x00300E40`, `0x0030F690`, `0x003266C0` | |
| 28 | | `0x0030EFF0`, `0x00310780` | |
| 29 | `0x0030CE10` (`0x0030CF16`, when `0x00306BD0` returns non-zero) | `0x0030CE10` (`0x0030CF00`) | `0x0030CE10` (`0x0030CF1D`) |
| 30 | `0x00301140` | `0x00310DB0` | |
| 33 | | `0x00236A60` | |
| 34 | `0x00319F50` | `0x00236A60`, `0x00300E40`, `0x00300FC0`, `0x00301140` | `0x00233F70`, `0x003125E0` |
| 37 | | `0x00238B40` | `0x0030B7F0`, `0x0046AB10` |
| 38 | `0x00313500` | `0x00233EA0`, `0x00236A60`, `0x003082F0` | `0x00319F50` |
| 39 | `0x00304850` | `0x00304850`, `0x003105D0` | |
| 41 | `0x00311F50` | `0x00301140`, `0x00307D10`, `0x0030F2D0` | `0x00307D10` |
| 42 | `0x00311F50` | `0x00301140`, `0x00307D10`, `0x0030F2D0` | `0x00307D10` |
| 47 | | `0x00236A60` | |
| 48 | | `0x00301140`, `0x00307D10`, `0x0030F2D0` | |
| 52 | | `0x00236A60` | |
| 53 | `0x002FEF30`, `0x00300140`, `0x00300E40`, `0x00301140`, `0x0030AF30` | `0x00304850`, `0x003105D0` | `0x00307300` |

Other writers that apply a mask held in a register are not in the table: among them the
`hideenemy` and `showenemy` verbs on bit `0x800` and the command issuer on bit `0x4000`.

## Operations

- A unit is zero at both ends of its life: the allocator clears the slot before the bind and the
  release clears it after copying the position out, so nothing survives into the next occupant.
- The walk's own count stops at 32, so an allocation failure needs a slot held by a unit the walk
  did not allocate; the record then keeps `+0x14` bit `0x10` and is counted as bound, but has no unit.

## Modding notes

- The thirty-two is a literal in `0x002368D0`; raising spawn counts spends against that budget, and
  there is no separate enemy pool.
- Carry the handle at `+0x08`, not the unit pointer or the slot index: a handle stops resolving
  once the actor's discriminator advances or the manager is unbound.
- An actor that ignores movement calls is one whose class is not 3; check `+0x03 >> 5`.

## Related

- [Field runtime](field-runtime.md): the frame callback a bound unit gets.
- [Actor managers](actor-managers.md): the manager slots the handle's selector names.
- [The actor record](actor-record.md): the actor side of the link.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md): the record at `+0x698`.
- [Spawn placement and retirement](../Enemy-Spawning/enemy-spawning.md): the spawn record the release writes.
