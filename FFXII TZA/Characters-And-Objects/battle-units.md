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

1. stores infinity at `0x02F973B8` and zeroes `0x02089300` (`0x002368F0`, `0x002368F8`), writes the slot count `0x0208E6A0`
   = 32, frees a previous pool (`0x003844F0`) and allocates the pool `0x0208E688` as `32 * 0xF50` bytes under the name
   `BtlWork` (`0x00384510`) and zeroes it;
2. allocates the two `0x9400`-byte spawn-keep banks `0x0208E690` (`btlKeepCharWork1`) and `0x0208E698`
   (`btlKeepCharWork2`) and zeroes both, runs `0x00383A20`, frees a previous `0x0208E680` (`0x00384500`) and nulls it
   (`0x002369B4`), registers the static task `0x00238850` (`0x003843F0(0x13, ...)`) and runs `0x0030CF40` and `0x002EA5F0`;
3. sets `0x0208935C` to 5.0, zeroes `0x02089340` (`0x002369FB`) and the twelve qwords at `0x02EBF1A0`, sets `0x0208D455` to
   `0xFFFF` and `0x0208936C` to 300, and requests the twelve job boards
   (`0x00238260(0..11)`).

`0x02089300` is the battle system's up flag. Boot runs `0x002368D0` once (`0x0022A41A`), and `0x00236A40`
sets the flag to 1 (`0x00236A44`) when the start-up state `0x0022B6E0` moves to state 1 (`0x0022B77C`).
While it is 0 the definition installer `0x0023A570` returns 0 (`0x0023A5B5`), the fresh stats record
`0x0023AC80` returns 0 (`0x0023ACE4`) and `0x002342F0` does nothing (`0x002342F4`) ([battle unit
construction](battle-unit-construction.md), [kill
chain](../Rewards-EXP-Gil-And-Loot/kill-chain.md)).

A unit is `0xF50` (3,920) bytes; `0x00236850` returns the count and `0x00236820(i)` returns
`[0x0208E688] + i * 0xF50` for `0 <= i < count` and null otherwise. `0x002367A0(selector)` scans the pool
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
- `0x00238FA0(record, 0x0031C4C0(row))`, with the row byte `+0x12` (`0x00265AD2`-`0x00265AE5`), when byte `+0x12` is
  below 4;
- the `0x00359B80` object's `+0x40`-`+0x63` and byte `+0x65` cleared.

The number bound is stored at the slot's `+0x1E8` (`0x00265B3B`). Records of the other four managers never get a
unit: the walk tests the slot's `+0x28` for every record (`0x00265A70`) and stores 0 at `+0x1E8` for them, as it
does for a slot with no records (`0x00265B4D`).

### The handle

`0x003589B0(actor)` encodes an actor as `((actor u16 +0x16 & 0x7FF) << 20) | ((actor u8 +0x15 & 0xF) << 16) | actor u16 +0x00`:
the low word is the record's index in its manager, mask `0xF0000` the manager slot, mask `0x7FF00000` the
record's discriminator. `0x002659D0(actor)` advances the discriminator as `(old + 1) & 0x7FF`, with 0
replaced by 1, so it runs over 1 to 2047 and a handle taken before the advance stops resolving.

`0x003588B0(handle)` decodes it: 0 gives null; a manager slot of 5 or more gives null; the manager
`0x02098E10 + slot * 0x288` must have a record pool (`+0x08`) and a payload (`+0x00`), the index
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

`0x00358960` takes the record from the list at `+0x08` of what `0x00263FF0` returns, entry `ordinal` after the count
dword (`0x0035896E`-`0x00358981`). A null list, a negative ordinal and an ordinal at or past the count all leave the
record 0, so the read at `0x00358986` is of address 3.

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
   with a null `[0x02B457D0]` it does nothing, and it returns 1 when it cleared an entry and 0 otherwise
   (`0x003BBC90`, `0x003BBCAF`, `0x003BBCC3`);
2. for an enemy (stats kind 1) with flag bit `0x10` set, unless a terminal status is present outside a
   town (`0x00377C20`), and with a spawn record at `+0x6A0` (`0x00234288`), it copies the unit's position
   `+0xE0`-`+0xEF` into the spawn record's `+0x60`
   and the yaw `+0x160` into `+0x74`, and sets the spawn record's flag bit `0x4`
   ([spawn placement](../Enemy-Spawning/enemy-spawning.md));
3. it zeroes the whole slot and clears bit `0x1`; the test before the clear (`unit >= base`, else
   `unit < base + 32 * 0xEA7900`, and `0xEA7900` is `0xF50 * 0xF50`) cannot fail for any pointer.

The town test of step 2 is `0x00313F60`, a jump to `0x00377C20` (`0x00234275`), and a null stats record skips the step
(`0x0023425B`).

### The actor class

The bits under mask `0xE0` of the actor's byte `+0x03` are its class, and the bits under mask `0xF` of byte `+0x0E` are a separate
nibble (`0x00263C20`). The class decides what code accepts the actor:

| Class | Test | Examples |
|---|---|---|
| 1 or 3 | `+0x03 >> 5` is 1 or 3 | `0x00265020` reads the position from the movement context `[actor + 0xB8]` and returns zeros otherwise |
| 3 | `(+0x03 & 0xE0) == 0x60` | the movement code: the field runtime's steering (`0x0025DF00`), the frozen pass (`0x0025E400`), the unit bind's `+0x1C` clear (`0x00265A20`) |
| 2 | `(+0x03 & 0xE0) == 0x40` | the `setline` verb `0x00351610`, which writes its six floats into the movement context at `+0x00`, `+0x04`, `+0x08`, `+0x10`, `+0x14` and `+0x18`; it pops all six for every class, the first popped to `+0x18` and the last to `+0x00`, and stores them only for class 2 (`0x0035163F`-`0x003516AA`), through `[actor + 0xB8]` (`0x00351688`) |

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
| `0x00269FE0(actor, n)` | nothing for a null actor (`0x00269FE3`); for class 3, `+0x1C` bits `0x100` and `0x2000` set when `n` is 4 (each followed by `0x00268EA0` when `+0x0B` bit `0x8` is set) and cleared otherwise; then nibble = `n & 0xF`. The verb `setfreetargettype` (`0x0265`, `0x003528C0`) calls it on the calling actor with a popped `n` |
| `0x002659A0(actor)` | `+0x1C` bits `0x100` and `0x2000` cleared, nibble 5, `+0xF4` = 0 |
| `0x00267CC0(actor)` | `+0x1C` bit `0x8` cleared, bits `0x100` and `0x2000` set (with `0x00268EA0` as above), and for class 3 set a second time with their `0x00268EA0` calls (`0x00267CF4`-`0x00267D23`), nibble 4 (`and 0xF4` then `or 4`, `0x00267D28`-`0x00267D2C`), `+0xF4` = 2 |
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
| `playerstatus(bit)`, `getcharbattlestatus(bit)` | `0x00A9`, `0x0499` | `0x0035A1C0` | 1 when status bit `bit` is set in `+0x3C` or `+0x64` (`0x00320CA0`); 0 when `0x00320CA0` fails (`0x0035A1DB`); `bt` takes `bit` modulo 32, so the bit value tested is `1 << (bit & 31)` (`0x0035A1E1`) |
| `getcharbattlestatus_49a(member, bit)` | `0x049A` | `0x0035A1C0` | the same for a member |
| `getbtlwork(i)` | `0x0110` | `0x0035A060` | unit byte `+0xEC0 + i`, sign-extended (`movsx`), for `i` below 16 (`0x0031C1A0`), else 0; the test is unsigned, so a negative `i` gives 0 (`0x0031C1C2`), and so do a null actor and an actor without a unit (`0x0031C1B3`, `0x0031C1BD`, `0x0035A077`) |
| `getequipitemid(slot)` | `0x0351` | `0x0035A0C0` | the equipment word for `slot` (below), -1 for `0xFFFF` |
| `getequipitemid_468(member, slot)` | `0x0468` | `0x0035A0C0` | the same for roster member `member` |
| `getmpratio_1f7(member, percent)` | `0x01F7` | `0x004737A0` | MP for a percent of 0 or less, else `percent` of the capacity (`0x003206E0`) |
| `setcharbattlestatus(status, v)` | `0x01F0`, `0x01FC` with a member | `0x004737D0` | adds status `status` (`0x00318A90` mode 1, `0x0030EAE0`); -1 for a null actor (`0x004737E2`); `v`, popped first (`0x00346E78`), reaches `0x00318A90` as its fourth argument, which it never reads (`0x00318B18` sets `r9` to -1), so `v` has no effect |
| `clearcharbattlestatus(status, v)` | `0x01F1`, `0x01FD` with a member | `0x00473690` | removes it (`0x00318A90` mode 0, `0x0030E990`); -1 for a null actor (`0x004736A2`); `v` has no effect in the same way (`0x003472B8`) |
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

`0x00318A90` tests the bit value `1 << (status & 31)` against `0x80000003` (`0x00318AD2`-`0x00318AD9`), so 32, 33 and
63 are refused as well, and the routine receives the status's low byte (`0x00318B10`). Any mode other than 0 adds
(`0x00318B14`), and a call made returns 0 (`0x00318B23`). `0x003206E0` returns -1 for a `which` other than 0 and 1
(`0x00320726`) and the current value for a percent of 0 or less (`0x0032073C`-`0x00320740`); its product is 64-bit
and the division signed (`0x00320752`-`0x00320774`).

`0x0031BDC0(words, slot)` reads the stats record's equipment words `+0x50` (`0x0031BD80`): slots 0-4
give the word itself and slots above 8 give `0xFFFF`. Slots 5, 7 and 8 give word 0 when
`0x00322560` reports that word 0's row in the equipment table `[0x02EBF0F8]` has byte `+0x26` equal
to `0x11`, and word 1 otherwise; slot 6 gives the other one. `0x0035A0C0` passes slots 1-5 through
and turns any other value into 0.

A negative slot gives `0xFFFF` as well, since `0x0031BDD3` compares unsigned, and `0x0035A0C0` turns it into 0 the
same way (`0x0035A0CC`). `0x0035A0C0` returns -1 for a null actor (`0x0035A0C7`) and for a `0xFFFF` word
(`0x0035A10F`-`0x0035A116`); `0x0031BD80` gives `0xFFFF` for an actor without a unit or a stats record
(`0x0031BD88`-`0x0031BDB3`).

`0x00359EA0(index, focusFirst, includeHidden)` picks a party actor: it lists the members of
`0x0031B670` (up to four) followed by those of `0x0031B680`, drops members whose model is hidden
(`0x002E9600` gives 0: it gives 1 only for class 3 with context `+0x10` bit `0x8` set) unless `includeHidden`
is set, moves the party
focus record (`0x00264050(0)`) to the front when `focusFirst` is set and it is among the first four,
and returns entry `index`, or null past the end.

Without `includeHidden` the walk keeps an entry only when it is non-null and `0x002E9600` gives non-zero
(`0x00359F40`-`0x00359F5B`), and zero-fills the slots it freed (`0x00359F8B`). The focus record is `0x00264050(0, -1)`
(`0x00359F9A`-`0x00359F9F`), sought in the first four slots (`0x00359FB0`-`0x00359FBE`). The index test is signed
(`0x0035A010`), so a negative index is not refused and reads the stack before the list (`0x0035A025`).

`0x00359CA0` takes the same arguments and gives the same pick, except that it filters the two lists apart and looks
for the party focus only among the members of `0x0031B670`, so a focus member from `0x0031B680` keeps its place;
capturebattlemembeructop, ucmovecancel_52d and setbattlethinkstatus_52e use it.

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
| `0x02089340` | `u32` |  | zeroed by `0x002368D0`; bit `0x10` gates `0x0031B7E0` |

### The flag word

Every immediate-mask write and test on `+0x00` and `+0x04` in the access table
[`battle-unit-fields.tsv`](battle-unit-fields.tsv) by bit, plus the unit reset `0x00236A60`'s register mask
`0xFFFF7FFDFFE7FFFD` (`0x00236A9C`-`0x00236AB1`), which clears bits `0x2`, `0x80000`, `0x100000`, `0x200000000` and
`0x800000000000`. The reset also clears `+0x00` with `0xFFFFB0E3` (`0x00236AA6`) and `+0x04` with `0xFFEFFFBB`
(`0x00236A95`). Each bit value is a bit of the qword at `+0x00`, so values from `0x100000000` up are bits of the dword
at `+0x04`.

The Tested by column lists the functions that test the bit on the word in memory. The last column lists the
functions that load the word into a register and, before any branch, test the bit with `bt` or `test` on that
register or a copy of it, each with the address of its first such test. `0x00301140`, for one, tests `0x4000000`
with `bt rax, 0x1a` at `0x00301176`:

| Bit value | Set by | Cleared by | Tested by | Tested in a register by |
|---|---|---|---|---|
| `0x1` | `0x00234480` | `0x00234200` | `0x00234480` | |
| `0x2` | `0x0023A570`, `0x00300E40` | `0x00236A60` | `0x00233F70`, `0x003125E0`, `0x00319F50`, `0x003243F0`, `0x00324470` and one more | |
| `0x4` | `0x0023A570` | `0x00236A60` | `0x00233AD0`, `0x0023A570`, `0x0031A300`, `0x0031C000`, `0x00324380` and three more | `0x003266C0` (`0x00326A66`) |
| `0x8` | `0x00233AD0` | `0x00236A60` | `0x00233AD0`, `0x00317E60`, `0x00319090`, `0x00319490`, `0x0031ACC0` and three more | `0x00233F70` (`0x00233FAD`), `0x0030BE80` (`0x0030BE87`), `0x0030BEB0` (`0x0030BEC3`), `0x003125E0` (`0x003125F5`) |
| `0x10` | `0x00233F70` | `0x00236A60` | 27 functions, among them `0x00233EA0`, `0x00234200`, `0x002350C0`, `0x00237D80` | `0x00233F70` (`0x00233FC3`), `0x0030B7F0` (`0x0030B80D`), `0x0030DA30` (`0x0030DA46`), `0x003125E0` (`0x003125F1`) |
| `0x20` | `0x00308610` | `0x0030EFF0`, `0x00310780` | | `0x00308610` (`0x00308698`), `0x00313CD0` (`0x00313D36`) |
| `0x40` | `0x00324470`, `0x003266C0` | `0x00324450` | `0x00324450` | |
| `0x100` | `0x00313500` | `0x00233EA0`, `0x00236A60`, `0x00301140`, `0x00306760`, `0x00313F70` | | |
| `0x200` | `0x00319F50` | `0x00233EA0`, `0x00236A60`, `0x00301140`, `0x00306760`, `0x003082F0` | | `0x003125E0` (`0x0031269C`) |
| `0x400` | `0x00319F50` | `0x00236A60`, `0x00301140` | | `0x003125E0` (`0x00312693`) |
| `0x800` | | `0x00236A60` | | `0x003125E0` (`0x0031268A`) |
| `0x1000` | `0x00304850` | | | `0x00304850` (`0x00304EA5`), `0x0030CA80` (`0x0030CB58`) |
| `0x2000` | | `0x00304850` | | `0x0030CA80` (`0x0030CB58`), `0x00313DB0` (`0x00313EEE`) |
| `0x4000` | | `0x00236A60` | | `0x0030BA30` (`0x0030BA43`), `0x0030BA80` (`0x0030BA93`) |
| `0x8000` | `0x00239170` | `0x00239170` | | |
| `0x10000` | | | | `0x00233F70` (`0x00233FB8`) |
| `0x40000` | `0x00236300` | `0x00236300`, `0x00325BB0` | | `0x0023A070` (`0x0023A0E4`), `0x00304850` (`0x00304FB7`), `0x00325D90` (`0x00325E45`) |
| `0x80000` | `0x00325260` | `0x00236A60` | | `0x003057D0` (`0x00305806`) |
| `0x100000` | `0x003057D0` | `0x00236A60` | | `0x003057D0` (`0x00305811`) |
| `0x200000` | `0x00239840` | `0x00234480`, `0x00300E40` | `0x00308D90` | |
| `0x400000` | `0x00312FA0` | | | `0x002FFB60` (`0x002FFBD9`), `0x00305AB0` (`0x00305AC1`), `0x00307300` (`0x00307544`), `0x00308270` (`0x0030827B`), `0x00308610` (`0x003086A0`), `0x0030C010` (`0x0030C053`), `0x0030F760` (`0x0030F939`), `0x00310780` (`0x003107BE`), `0x00312FA0` (`0x00312FF3`) |
| `0x800000` | | `0x00301140`, `0x0030F2D0` | `0x003081E0`, `0x00312FA0`, `0x00313F20`, `0x003176E0` | `0x00325BB0` (`0x00325CC2`) |
| `0x1000000` | `0x00301140`, `0x00313500` | `0x003083A0`, `0x003250F0` | | `0x002FEF30` (`0x002FF99C`), `0x002FFB60` (`0x002FFBB3`), `0x00304850` (`0x003048AD`), `0x00308610` (`0x0030865B`), `0x0030DA30` (`0x0030DA3B`), `0x0030E360` (`0x0030E772`), `0x0030EFF0` (`0x0030EFFF`), `0x00313F20` (`0x00313F22`), `0x00320BB0` (`0x00320C30`) |
| `0x2000000` | `0x00313500` | `0x003083A0` | | |
| `0x4000000` | `0x002354F0`, `0x002355A0`, `0x00235720`, `0x00238FA0`, `0x00239410`, `0x00300310` | `0x00233AD0`, `0x002393E0`, `0x0023A570`, `0x00300E40`, `0x0030F690`, `0x003266C0` | | `0x00233AD0` (`0x00233BCF`), `0x0023A570` (`0x0023A643`), `0x00301140` (`0x00301176`) |
| `0x10000000` | | `0x0030EFF0`, `0x00310780` | | |
| `0x20000000` | `0x0030CE10` (`0x0030CF16`, when `0x00306BD0` returns non-zero) | `0x0030CE10` (`0x0030CF00`) | `0x0030CE10` (`0x0030CF1D`) | `0x0030CBE0` (`0x0030CDC0`) |
| `0x40000000` | `0x00301140` | `0x00310DB0` | | |
| `0x200000000` | | `0x00236A60` | | |
| `0x400000000` | `0x00319F50` | `0x00236A60`, `0x00300E40`, `0x00300FC0`, `0x00301140` | `0x00233F70`, `0x003125E0` | |
| `0x2000000000` | | `0x00238B40` | `0x0030B7F0`, `0x0046AB10` | |
| `0x4000000000` | `0x00313500` | `0x00233EA0`, `0x00236A60`, `0x003082F0` | `0x00319F50` | |
| `0x8000000000` | `0x00304850` | `0x00304850`, `0x003105D0` | | |
| `0x20000000000` | `0x00311F50` | `0x00301140`, `0x00307D10`, `0x0030F2D0` | `0x00307D10` | |
| `0x40000000000` | `0x00311F50` | `0x00301140`, `0x00307D10`, `0x0030F2D0` | `0x00307D10` | |
| `0x800000000000` | | `0x00236A60` | | |
| `0x1000000000000` | | `0x00301140`, `0x00307D10`, `0x0030F2D0` | | |
| `0x10000000000000` | | `0x00236A60` | | |
| `0x20000000000000` | `0x002FEF30`, `0x00300140`, `0x00300E40`, `0x00301140`, `0x0030AF30` | `0x00304850`, `0x003105D0` | `0x00307300` | |

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
- [Actor managers](actor-managers.md): the manager slot a handle names.
- [The actor record](actor-record.md): the actor side of the link.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md): the record at `+0x698`.
- [Spawn placement and retirement](../Enemy-Spawning/enemy-spawning.md): the spawn record the release writes.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Save load settings: `0x0022B6E0` calls `0x002EF650`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
