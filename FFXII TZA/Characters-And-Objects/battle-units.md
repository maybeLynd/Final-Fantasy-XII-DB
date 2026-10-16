---
title: "Battle units: the pool of combat slots, who gets one, the actor class bits, the handle and the flag word"
kind: "system"
category: "Characters and objects"
summary: "The fixed pool of battle units that everything fighting in a field draws from: its size and allocation, the walk that binds a unit to every eligible actor of the primary manager and what happens when the pool is full, the two-way link between unit and actor, the encoded handle that names a unit and the resolver that decodes it, the release that scrubs a slot, the three-bit actor class that decides what an actor may do, and the unit flag word bit by bit with every writer the access table proves."
addresses: ["002368D0", "00234480", "00265A20", "00234200", "00236820", "00236850", "002367A0", "002134A0", "00263E30", "0031B760", "003589B0", "003588B0", "0031B7E0", "002659D0", "00265020", "00263C20", "00263D30", "00351610"]
---

# Battle units: the pool of combat slots, who gets one, the actor class bits, the handle and the flag word

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

### Release

`00234200(_, actor)` releases the actor's unit. With no unit it runs `00263980` and `003589A0` on
the actor and returns. Otherwise:

1. it runs `00300140(unit, 1)` and `00319140(unit, 2)`;
2. for an enemy (stats kind 1) with flag bit 4 set, unless a terminal status is present outside a
   town (`00377C20`), it copies the unit's position `+0xE0`-`+0xEF` into the spawn record's `+0x60`
   and the yaw `+0x160` into `+0x74`, and sets the spawn record's flag bit 2
   (spawn placement);
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

## Layouts

```
struct BattleUnit size=0xF50 count=32 base=[0208E688]
+0x000  u64   flags          bit 0 slot in use; the table below
+0x008  u32   handle         003589B0(actor) at bind
+0x010  u8*   actor          the bound actor record
+0x020  i32   bound          1 after the bind walk (00234A00)
+0x057  u8    entryGroup     actor +0xF6 at bind
+0x698  u8*   stats          the combat stats record (unit-stats-fields page)
+0x6A0  u8*   spawnRecord
+0xE68  u8*   classRow
+0xEA9  u8    slotIndex
```

```
globals
0208E688  u8*   the pool               002368D0
0208E6A0  i32   the slot count, 32     002368D0
0208E690  u8*   btlKeepCharWork1       002368D0
0208E698  u8*   btlKeepCharWork2       002368D0
02089340  u32   zeroed by 002368D0; bit 4 gates 0031B7E0
```

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
- The actor record: the actor side of the link.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md): the record at `+0x698`.
- Spawn placement and retirement: the spawn record the release writes.
