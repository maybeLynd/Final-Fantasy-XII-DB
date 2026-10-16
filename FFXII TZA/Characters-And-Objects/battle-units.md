---
title: "Battle units: the pool of combat slots, who gets one, the actor class bits, the handle and the flag word"
kind: "system"
category: "Characters and objects"
summary: "The fixed pool of battle units that everything fighting in a field draws from: its size and allocation, the walk that binds a unit to every eligible actor of the primary manager and what happens when the pool is full, the two-way link between unit and actor, the encoded handle that names a unit and the resolver that decodes it, the release that scrubs a slot, the three-bit actor class that decides what an actor may do, and the unit flag word bit by bit with every writer the access table proves."
addresses: "002368D0, 00234480, 00265A20, 00234200, 00236820, 00236850, 002367A0, 002134A0, 00263E30, 0031B760, 003589B0, 003588B0, 0031B7E0, 002659D0, 00265020, 00263C20, 00263D30, 00351610, 00238BF0, 00269FE0, 00269F30, 002659A0, 00267CC0, 0026AD00, 00263AC0, 00234D40, 0035A1C0, 0035A060, 0031C1A0, 0035A0C0, 0031BDC0, 004737A0, 004737D0, 00473690, 00318A90, 003206E0, 0030C3C0, 00237430, 00359EA0, 0031FCF0, 0031FD20, 00273780, 00273750, 00273A00, 00358960, 003BBC80"
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

`002368D0`, run when battle storage is set up:

1. zeroes `02089340` and `02089300`, writes the slot count `0208E6A0` = 32, frees a previous pool
   (`003844F0`) and allocates the pool `0208E688` as `32 * 0xF50` bytes under the name `BtlWork`
   (`00384510`) and zeroes it;
2. allocates the two `0x9400`-byte spawn-keep banks `0208E690` (`btlKeepCharWork1`) and `0208E698`
   (`btlKeepCharWork2`), runs `00383A20`, frees a previous `0208E680` (`00384500`), registers the
   static task `00238850` (`003843F0(0x13, ...)`) and runs `0030CF40` and `002EA5F0`;
3. zeroes the twelve qwords at `02EBF1A0`, sets `0208D455` to `0xFFFF`, `0208936C` to 300,
   `0208935C` to 5.0 and `02F973B8` to infinity, and requests the twelve job boards
   (`00238260(0..11)`).

A unit is `0xF50` (3,920) bytes; `00236850` returns the count and `00236820(i)` returns
`0208E688 + i * 0xF50` for `0 <= i < count` and null otherwise. `002367A0(selector)` scans the pool
for a unit whose stats record `+0x698` has the word `+0x04` equal to the selector, after
`00322C50(2, selector)` admits it; a selector of `0xFF` is compared as `0xFFFF`, so it matches that
word value rather than every unit.

### Allocation

`00234480(0, actor)` walks the pool from slot 0 for the first unit whose flag bit 0 is clear and
returns without doing anything when all are in use. For the free slot it:

1. zeroes the whole `0xF50` bytes and sets flag bit 0;
2. writes the slot index to `+0xEA9`;
3. stores the unit pointer at the actor's `+0x30` (`002134A0`) and the actor at the unit's `+0x10`;
4. stores the actor's encoded handle (`003589B0`) at `+0x08`;
5. clears flag bit 21 and copies the actor's entry-group word `+0xF6` (`00263D30`) into the byte
   `+0x57`.

### Who gets a unit

`00265A20(slot)` is the allocator's only caller. For the primary manager only (slot index 0) it
walks the slot's records (`00358940`, `recordCount` at `+0x20`) and, for each record whose byte
`+0x14` has bit 7 set, either enters the bind branch or, once 32 records have entered it in this
walk, clears the record's `+0x14` bit 4 instead. Every record that enters the branch is counted,
whether or not `00234480` found a slot; the branch gives the record:

- the frame callback `00233F70` at `+0x38` ([field runtime](field-runtime.md));
- `00234A00(unit, 1)` (unit `+0x20` = 1) when the back-pointer `+0x30` is set, which is how the walk
  notices a silent allocation failure;
- for a class-3 actor, bits 8 and 13 of `+0x1C` cleared; `+0x0E` = `(old & 0xF1) | 1`;
- `00238FA0(record, 0031C4C0())` when byte `+0x12` is below 4;
- the `00359B80` object's `+0x40`-`+0x63` and byte `+0x65` cleared.

The number bound is stored at the slot's `+0x1E8`. Records of the other four managers never get a
unit.

### The handle

`003589B0(actor)` encodes an actor as `((actor u16 +0x16 & 0x7FF) << 20) | ((actor u8 +0x15 & 0xF) << 16) | actor u16 +0x00`:
the low word is the record's index in its manager, bits 16-19 the manager slot, bits 20-30 the
record's discriminator. `002659D0(actor)` advances the discriminator as `(old + 1) & 0x7FF`, with 0
replaced by 1, so it runs over 1 to 2047 and a handle taken before the advance stops resolving.

`003588B0(handle)` decodes it: 0 gives null; a selector of 5 or more gives null; the manager
`02098E10 + selector * 0x288` must have a record pool (`+0x08`) and a payload (`+0x00`), the index
must be below the slot's `+0x20` and the pool's own count, the slot's `+0x10` bit 0 must be set, the
entry must be non-null and the actor's full word `+0x16` must equal the discriminator. `0031B7E0`
then returns that actor's unit `+0x30` (`00263E30`) when `02089340` bit 4 is set; `0031B760(actor)`
is the null-guarded form of the same back-pointer read.

Small predicates over the same reads serve the menus and the HUD: `0031FCF0(actor)` is true for a
non-null actor with a unit; `0031FD20(handle)` is true when `02089340` bit 4 is set and the handle
resolves to an actor with a unit; `00273780(handle)` is true for a non-zero handle that resolves;
`00273750(handle)` is true when the resolved actor's class nibble (`00263C20`) is 1 or 2, and
`00273A00(handle)` when it is 5. `00358960(slot, ordinal)` returns the class bits `+0x03 >> 5` of a
record of the slot `00263FF0` gives, and reads address 3 when the ordinal is out of range.

### Release

`00234200(_, actor)` releases the actor's unit. With no unit it runs `00263980` and `003589A0` on
the actor and returns. Otherwise:

1. it runs `00300140(unit, 1)` and `00319140(unit, 2)`; with bit 1 of its second argument
   `00319140` calls `003BBC80(actor)`, which zeroes the first two qwords of every entry of the
   64-entry table at `[02B457D0]` (stride `0x50`) whose first qword is the unit's actor;
2. for an enemy (stats kind 1) with flag bit 4 set, unless a terminal status is present outside a
   town (`00377C20`), it copies the unit's position `+0xE0`-`+0xEF` into the spawn record's `+0x60`
   and the yaw `+0x160` into `+0x74`, and sets the spawn record's flag bit 2
   ([spawn placement](../Enemy-Spawning/enemy-spawning.md));
3. it zeroes the whole slot and clears bit 0; the test before the clear (`unit >= base`, else
   `unit < base + 32 * 0xEA7900`, and `0xEA7900` is `0xF50 * 0xF50`) cannot fail for any pointer.

### The actor class

Bits 5-7 of the actor's byte `+0x03` are its class, and bits 0-3 of byte `+0x0E` are a separate
nibble (`00263C20`). The class decides what code accepts the actor:

| Class | Test | Examples |
|---|---|---|
| 1 or 3 | `+0x03 >> 5` is 1 or 3 | `00265020` reads the position from the movement context `[actor + 0xB8]` and returns zeros otherwise |
| 3 | `(+0x03 & 0xE0) == 0x60` | the movement code: the field runtime's steering (`0025DF00`), the frozen pass (`0025E400`), the unit bind's `+0x1C` clear (`00265A20`) |
| 2 | `(+0x03 & 0xE0) == 0x40` | the `setline` verb `00351610`, which writes its six floats into the movement context at `+0x00`, `+0x04`, `+0x08`, `+0x10`, `+0x14` and `+0x18` |

### The refresh from the unit

`00238BF0(unit)` brings the bound actor (`+0x10`) in line with the unit's stats record and is what
sets the class nibble and the byte `+0x0F` of a fighting actor. It does nothing without an actor or
a stats record, or for a stats kind other than 0 and 1.

- A party member (kind 0) gets `+0x0F` = 3 and nibble 8 when its type is 27-39, and `+0x0F` = 2 and
  nibble 1 otherwise (`00269F30` writes `+0x0F`).
- An enemy (kind 1) whose spawn record byte `+0` has bit 5 clear turns a unit byte `+0x58` of 4 into
  1; with `+0x58` = 1 it runs `002659A0` and `0025D5E0(actor, 10)`, and raises `+0x58` to 7 when the
  enemy row's byte `+0x03` has bit 4.
- An enemy whose spawn record has bit 5 set runs `00267CC0` and `0026B4A0(actor, 10)` instead.
- The nibble is then written by `00269FE0(actor, n)` with the value above, or the unit's `+0x58` for
  an enemy when it is not 0, and `0026AD00(actor, on)` sets `+0x13` bit 7 for an enemy whose class
  row byte `+0x18 & 0xE` is 4 and clears it otherwise.

The writers:

| Function | Writes |
|---|---|
| `00269F30(actor, v)` | `+0x0F` = `v` for a non-null actor |
| `00269FE0(actor, n)` | for class 3, `+0x1C` bits 8 and 13 set when `n` is 4 (each followed by `00268EA0` when `+0x0B` bit 3 is set) and cleared otherwise; then nibble = `n & 0xF`. The verb `setfreetargettype` (`0x0265`, `003528C0`) calls it on the calling actor with a popped `n` |
| `002659A0(actor)` | `+0x1C` bits 8 and 13 cleared, nibble 5, `+0xF4` = 0 |
| `00267CC0(actor)` | `+0x1C` bit 3 cleared, bits 8 and 13 set (with `00268EA0` as above), nibble 4, `+0xF4` = 2 |
| `0026AD00(actor, on)` | `+0x13` bit 7 = `on != 0` |

`00263AC0(actor)` reads `+0x0F` back: 0 for a null actor, 1 instead of 2 when the actor is the party
focus (`003590D0`, `003588B0`, resolved with slot 0 as the current slot), else the byte itself.

### The script queries

Script verbs read and change a fighting actor's state through its unit and stats record. The
`isdead`, status-read, `getequipitemid` and `getmpratio_1f7` verbs first pass their actor through
`00263F10`, which follows a record whose `+0x18` is 2 to the record its `+0x19` (manager) and
`+0x1A` (ordinal) name; the others use the calling actor as it is. A member argument goes through
`00264010` (a record of the current slot, or the party focus for a negative value), or through
the roster (`00263750`) for `getequipitemid_468`.

| Verb | Id | Helper | Result |
|---|---|---|---|
| `isdead`, `isdead_15f(ordinal)` | `0x015E`, `0x015F` | `003597B0` | 1 when `00234D40` gives 2, else 0 |
| `isdead2`, `isdead2_49f(ordinal)` | `0x049E`, `0x049F` | `003597D0` | `00234D40` itself |
| `playerstatus(bit)`, `getcharbattlestatus(bit)` | `0x00A9`, `0x0499` | `0035A1C0` | 1 when status bit `bit` is set in `+0x3C` or `+0x64` (`00320CA0`) |
| `getcharbattlestatus_49a(member, bit)` | `0x049A` | `0035A1C0` | the same for a member |
| `getbtlwork(i)` | `0x0110` | `0035A060` | unit byte `+0xEC0 + i`, sign-extended (`movsx`), for `i` below 16 (`0031C1A0`), else 0 |
| `getequipitemid(slot)` | `0x0351` | `0035A0C0` | the equipment word for `slot` (below), -1 for `0xFFFF` |
| `getequipitemid_468(member, slot)` | `0x0468` | `0035A0C0` | the same for roster member `member` |
| `getmpratio_1f7(member, percent)` | `0x01F7` | `004737A0` | MP for a percent of 0 or less, else `percent` of the capacity (`003206E0`) |
| `setcharbattlestatus(status, v)` | `0x01F0`, `0x01FC` with a member | `004737D0` | adds status `status` (`00318A90` mode 1, `0030EAE0`) |
| `clearcharbattlestatus(status, v)` | `0x01F1`, `0x01FD` with a member | `00473690` | removes it (`00318A90` mode 0, `0030E990`) |
| `isfusion_spattack(v)` | `0x02A1` | `0030C3C0` | 1 for `v` from 18 to 33, else 0 |
| `btlAtelIsMimicName` | `0x3062` | `00237430` | bit 5 of the spawn record's byte `+0` (unit `+0x6A0`), 0 without one |

`00234D40(actor)` returns 0 when the actor has no unit or unit flag bit 4 is clear, 2 when the stats
record is missing or its status words `+0x3C | +0x64` carry bit 0, 1 or 31 while the town flag
`00313F60` is clear, and 1 otherwise.

The handle-based helpers `00320CA0`, `003206E0` and `00318A90` take the actor's handle
(`003589B0`), need `02089340` bit 4, a unit and a stats record, and fail with -1 (0 for
`00320CA0`). `00318A90` refuses statuses 0, 1 and 31 with -2 and otherwise calls the add or remove
routine as `(stats, 0, status, -1, -1, 0x13)`. `003206E0(handle, which, percent)` reads HP `+0x48`
and capacity `+0x24` for `which` = 0 and MP `i16 +0x4C` and capacity `i16 +0x28` for 1; a percent of
100 returns the capacity and any other positive percent `percent * capacity / 100`, truncated.

`0031BDC0(words, slot)` reads the stats record's equipment words `+0x50` (`0031BD80`): slots 0-4
give the word itself and slots above 8 give `0xFFFF`. Slots 5, 7 and 8 give word 0 when
`00322560` reports that word 0's row in the equipment table `[02EBF0F8]` has byte `+0x26` equal
to `0x11`, and word 1 otherwise; slot 6 gives the other one. `0035A0C0` passes slots 1-5 through
and turns any other value into 0.

`00359EA0(index, focusFirst, includeHidden)` picks a party actor: it lists the members of
`0031B670` (up to four) followed by those of `0031B680`, drops members whose model is hidden
(`002E9600`: class 3 and context `+0x10` bit 3) unless `includeHidden` is set, moves the party
focus record (`00264050(0)`) to the front when `focusFirst` is set and it is among the first four,
and returns entry `index`, or null past the end.

The verb `0x308C` (`0050F5B0`) calls it through
`00510870` with `focusFirst` = 1 and `includeHidden` = 0, and sets its result to 1 when a member
was picked and `00262F50` accepted it, 0 otherwise.

## Layouts

Struct BattleUnit size=`0xF50` count=32 base=[`0208E688`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `u64` | flags | bit 0 slot in use; the table below |
| `008` | `u32` | handle | `003589B0`(actor) at bind |
| `010` | `u8*` | actor | the bound actor record |
| `020` | `i32` | bound | 1 after the bind walk (`00234A00`) |
| `057` | `u8` | entryGroup | actor +`0xF6` at bind |
| `698` | `u8*` | stats | the combat stats record (unit-stats-fields page) |
| `6A0` | `u8*` | spawnRecord |  |
| `E68` | `u8*` | classRow |  |
| `EA9` | `u8` | slotIndex |  |

Globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0208E688` | `u8*` | the pool | `002368D0` |
| `0208E6A0` | `i32` | the slot count, 32 | `002368D0` |
| `0208E690` | `u8*` | btlKeepCharWork1 | `002368D0` |
| `0208E698` | `u8*` | btlKeepCharWork2 | `002368D0` |
| `02089340` | `u32` | zeroed by 002368D0; bit 4 gates 0031B7E0 |  |

### The flag word

Every immediate-mask write and test on `+0x00` and `+0x04` in the access table `battle-unit-fields.tsv`
(each site checked against the executable), by bit, plus the unit reset `00236A60`'s register mask
`0xFFFF7FFDFFE7FFFD` (`00236A9C`-`00236AB1`), which clears bits 1, 19, 20, 33 and 47:

| Bit | Set by | Cleared by | Tested by |
|---|---|---|---|
| 0 | `00234480` | `00234200` | `00234480` |
| 1 | `0023A570`, `00300E40` | `00236A60` | `00233F70`, `003125E0`, `00319F50`, `003243F0`, `00324470` and one more |
| 2 | `0023A570` | `00236A60` | `00233AD0`, `0023A570`, `0031A300`, `0031C000`, `00324380` and three more |
| 3 | `00233AD0` | `00236A60` | `00233AD0`, `00317E60`, `00319090`, `00319490`, `0031ACC0` and three more |
| 4 | `00233F70` | `00236A60` | 27 functions, among them `00233EA0`, `00234200`, `002350C0`, `00237D80` |
| 5 | `00308610` | `0030EFF0`, `00310780` | |
| 6 | `00324470`, `003266C0` | `00324450` | `00324450` |
| 8 | `00313500` | `00233EA0`, `00236A60`, `00301140`, `00306760`, `00313F70` | |
| 9 | `00319F50` | `00233EA0`, `00236A60`, `00301140`, `00306760`, `003082F0` | |
| 10 | `00319F50` | `00236A60`, `00301140` | |
| 11 | | `00236A60` | |
| 12 | `00304850` | | |
| 13 | | `00304850` | |
| 14 | | `00236A60` | |
| 15 | `00239170` | `00239170` | |
| 18 | `00236300` | `00236300`, `00325BB0` | |
| 19 | `00325260` | `00236A60` | |
| 20 | `003057D0` | `00236A60` | |
| 21 | `00239840` | `00234480`, `00300E40` | `00308D90` |
| 22 | `00312FA0` | | |
| 23 | | `00301140`, `0030F2D0` | `003081E0`, `00312FA0`, `00313F20`, `003176E0` |
| 24 | `00301140`, `00313500` | `003083A0`, `003250F0` | |
| 25 | `00313500` | `003083A0` | |
| 26 | `002354F0`, `002355A0`, `00235720`, `00238FA0`, `00239410`, `00300310` | `00233AD0`, `002393E0`, `0023A570`, `00300E40`, `0030F690`, `003266C0` | |
| 28 | | `0030EFF0`, `00310780` | |
| 30 | `00301140` | `00310DB0` | |
| 33 | | `00236A60` | |
| 34 | `00319F50` | `00236A60`, `00300E40`, `00300FC0`, `00301140` | `00233F70`, `003125E0` |
| 37 | | `00238B40` | `0030B7F0`, `0046AB10` |
| 38 | `00313500` | `00233EA0`, `00236A60`, `003082F0` | `00319F50` |
| 39 | `00304850` | `00304850`, `003105D0` | |
| 41 | `00311F50` | `00301140`, `00307D10`, `0030F2D0` | `00307D10` |
| 42 | `00311F50` | `00301140`, `00307D10`, `0030F2D0` | `00307D10` |
| 47 | | `00236A60` | |
| 48 | | `00301140`, `00307D10`, `0030F2D0` | |
| 52 | | `00236A60` | |
| 53 | `002FEF30`, `00300140`, `00300E40`, `00301140`, `0030AF30` | `00304850`, `003105D0` | `00307300` |

Other writers that apply a mask held in a register are not in the table: among them the
`hideenemy` and `showenemy` verbs on bit 11 and the command issuer on bit 14.

## Operations

- A unit is zero at both ends of its life: the allocator clears the slot before the bind and the
  release clears it after copying the position out, so nothing survives into the next occupant.
- The walk's own count stops at 32, so an allocation failure needs a slot held by a unit the walk
  did not allocate; the record then keeps `+0x14` bit 4 and is counted as bound, but has no unit.

## Modding notes

- The thirty-two is a literal in `002368D0`; raising spawn counts spends against that budget, and
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
