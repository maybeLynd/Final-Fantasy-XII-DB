---
title: "Field runtime: how a frame drives every actor's script through the manager slots and the wait slots"
kind: "system"
category: "Characters and objects"
addresses: "0025D9E0, 00314020, 0025DF00, 0025E4C0, 00358940, 002620E0, 00261F90, 0025E400, 00583920, 003590D0, 003588B0, 0032FC30, 00233AA0, 00269860, 003DBF60, 003DC050, 003DB2A0, 002674B0, 003DB640, 00267420, 00267310, 0020E600, 0020E620, 00269800"
---

## What the player sees

Every actor in a field runs a small script: the townspeople, the doors, the treasure pots, the
cutscene triggers, the party members themselves. Each frame the game visits every actor once and
gives its script a turn, unless the script is waiting for something, such as a line of dialogue to
close, a walk to finish or another actor to reach a point.

When what the script was waiting for has finished, the script carries on in the same visit instead
of losing a frame. The pass also plays the area's music, keeps the party roster up to date, and,
once nothing in the field is pending any more, runs the one-time sequence that fades the field in.

## How it works

### Who runs the pass

`00314020(mode, arg)`, the world tick, is the only caller of the pass `0025D9E0(slot)`.

- In mode 0 it runs up to 16 sub-steps. Sub-step 0 runs every slot 0-4; a later sub-step runs a
  slot only while that slot's byte `+0x201` (`00267310`) is non-zero. Each slot visit is
  `00234590(slot)`, the pass, `00234520(slot)`; after the first sub-step's slot loop the tick runs
  `00253C50` and `00268D10` once, and each sub-step ends with the resource pass `003DB1F0(slot)`
  under the same gate.
- In mode 1 it runs slots 3 and 4 only, each as `00234590`, the pass, `003DB1F0`, `00234520`, and
  then `00253C50` once.
- Other modes run no slot.

A slot is a `0x288`-byte block at `02098E10 + slot * 0x288`; five of them fill `02098E10`-`02099AB7`.
The fields the pass uses:

Struct ActorManagerSlot base=`02098E10` size=`0x288`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `u8*` | payload | the bound definition payload; its i16 +`0x50` is the designated record's ordinal |
| `008` | `u8*` | recordPool | i32 count, then count record pointers (`00358940`) |
| `010` | `u8` | flags | bit 0 bound, bit 2 field initialised, bit 3 and bit 4 the slot-0 request steps, bit 5 the `02ADD968` hold, bit 6 music selected, bit 7 field busy |
| `011` | `u8` | flags2 | bit 0 a copy of flags bit 7, bit 1 one-shot trigger, bit 2 suspended, bit 3 blocks the request path |
| `012` | `u8` | drivePending | a designated record must be driven this pass |
| `013` | `u8` | requestFlag | with flags bit 0, enables the request path |
| `017` | `u8` | flags3 | bit 2 skips the arming call, bit 4 the frozen pass, bit 7 the music hold |
| `020` | `i32` | recordCount | the records the loops visit (`00358940` bounds the ordinal by the pool's own count) |
| `024` | `i32` | passCounter | incremented at every pass end |
| `028` | `i32` | slotIndex | 0 for the primary slot |
| `038` | `i32` | passCounter2 | incremented at every pass end |
| `200` | `u8` | rosterFlags | bit 1: the party roster is still being collected |
| `201` | `u8` | stepRequest | read by the tick's sub-step gate (`00267310`) |

### The refusals

The pass returns 1 without driving anything when:

1. the save-write busy flag `02CA99E8` (`00583920`) is non-zero;
2. after copying flags bit 7 into flags2 bit 0: `+0x13` is non-zero or flags bit 0 is set, flags2
   bit 3 is clear, and the byte `022C6D20[slot]` (`0032F6E0`) is non-zero, in which case it first
   runs `0026A5F0(slot)`, which sets bit `slot` of `02099ABC` (and bits 1-3 for slot 0) and calls
   `002E15D0` and `002E1690`;
3. flags bit 0 is clear;
4. the byte `022CB726` (`003603C0`) is non-zero;
5. flags3 bit 4 is set: it runs the frozen pass `0025E400(slot, 1)` instead, which zeroes the two
   simulation scales (`003DA2F0(0)`, `003DD210(0)`), republishes the focus record `02099D78` (leaving
   `02099D70` as it was) and runs `002E5180` for every record of sequence class 3
   (`+0x03 & 0xE0 == 0x60`) whose `+0xC0` object has a `+0x138`;
6. flags2 bit 2 is set.

### The two globals

Before any record is driven the pass publishes `02099D70` = the slot block and `02099D78` = the party
focus actor's record: `003590D0()` reads the packed handle at `022C7FE0`, `003588B0` resolves it, and
the result is null when there is no focus or the handle does not resolve.

### The pass body

The body takes one of these branches after the refusals:

1. Flags bit 7 clear (the field is not busy): every record 0 to `recordCount - 1` is driven through
   the wait resolver `0025DF00`; on slot 0 `0025B740` runs after each; the return value is the AND
   of every record's `+0x14` bit 6. Then `0025C170`, `0025B250` and `0025B820` run for the slot and
   the pass ends.
2. On slot 0 only: `02ADD0D8` (`00377DB0`) must be non-zero, else return 1. While flags bit 4 is
   clear: with bit 3 clear the pass issues the deferred mode request `0032FC30(1, 0xD4)`, sets bit 3
   and returns 1; with bit 3 set it returns 1 while the request word of slot 1 (`022C6E48 + 8`,
   `0032F6C0(1)`, bit 0 masked off) is non-zero or slot 1's flags bit 0 or `+0x13` is set, and
   otherwise sets bit 4 and continues.
3. `drivePending` set: the designated record `00358940(slot, payload i16 +0x50)` is driven once; if
   its `+0x14` bit 6 is clear and its low nibble is clear the pass ends with 0; while bit 6 is
   clear and the low nibble is not, `003DB280(record)` runs and the record is driven again. Once bit
   6 is set, `drivePending` is cleared, the init core `002620E0` runs and the pass ends with 0.
4. Otherwise the area music select `00261F90(slot)` runs first: on slot index 0 with flags bit 6
   clear it selects and starts the area's track once per field, sets flags bit 5 when flags3 bit 2
   is clear, and sets bit 6 at its end ([music](../Sound-And-Music/music-table.md)).
   Then the two holds below are checked, each marking the pass busy.
5. With flags3 bit 7 clear and flags bit 5 clear the main work runs: the init core, the roster loop,
   the all-records loop, the trigger bit and the field-settled sequence, described below.

The two holds of branch 4:

- With flags3 bit 7 set, the current track is the payload's `+0x1534` when `+0x1063` bit 6 is set
  and `003EAA70(field)` otherwise ([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)).
  The bit is cleared when `00360D60()` is 0, or when the track is negative and both `003135C0()`
  and `00303EC0()` are 0.
- With flags bit 5 set, the bit is cleared once `02ADD968` is 0 (`0037CB40`).

At the end of branches 4 and 5 flags bit 7 is rewritten from the busy mark; every branch then runs
`0025B600` on slot 0 and increments `+0x24` and `+0x38`.

### The init core

`002620E0(slot)` does nothing for a slot whose index is not 0. On slot 0 with flags bit 2 clear it
runs `00259B30`, `003E8980(0)`, `0025ACA0`, instantiates the field's effect rows for channels 0 and
`0x1F` (`0026FAD0`) with the lane from `0017D490()` or the payload's `+0x1060` plus 1, then
`00379860(lane)`, `00379290`, `003DE920(0, 1)` and `00363B40`, and sets bit 2 ([weather](../World-Areas-And-Travel/weather.md)
has the lane). It always ends with `003601C0(0xB)` and `003601C0(0xC)`.

### The roster loop

While `rosterFlags` bit 1 is set, the pass walks the four party members at `0209A1F0` (eight bytes
each):

1. on slot index 0, a member whose `+0x08` bit 6 is clear gets `00269860(member, 1)` unless flags3
   bit 2 is set, and bit 6 is set;
2. an empty roster entry, or a member whose `+0x10` is 0, is marked collected; otherwise the member
   is driven through `0025DF00` and marked collected if `+0x10` is 0 afterwards;
3. when all four are collected (`0xF`), `rosterFlags` bit 1 is cleared and, on slot index 0,
   `00233AA0` runs (`0030D8B0(1)`, `00326500`, `00311E10(0)`, `00311E20`).

The roster loop forces the return value to 0 and the busy mark on; while bit 1 is still set after
it, the rest of the body is skipped.

### The all-records loop and the trigger bit

Every record 0 to `recordCount - 1` is fetched with `00358940`: on slot index 0 a record whose
`+0x08` bit 6 is clear gets the same `00269860` arming and the bit; a record whose `+0x10` is not 0
marks the pass busy, is driven through `0025DF00`, and its `+0x14` bit 6 is folded into the return
value. `002F1A30(1)` (a scan of the 32 entries at `022BDEDE` under the mask `022BE7C0`) sets slot 0's
flags2 bit 1 on slot 0; a set flags2 bit 1 marks the pass busy and is cleared.

The same arming call is made outside the pass by `00269800(slot)`, which runs `00269860(record, 1)`
on every record of the slot's class-3 range (ordinals `+0x1DE` to `+0x1DE + +0x1D6 - 1`); the
`entrystart` verb's begin (`0x013F`, `003574B0`) runs it on slot 0.

### The field-settled sequence

When flags bit 7 is set, nothing marked the pass busy and the slot index is 0, the pass runs once:
`00363A80(1)`; `003B7130(0, 1)` when `003135C0()` is non-zero; when `002EFD20(2)` is non-zero,
`002EFE40(6)`, `002EFE50(0xFF)`, `00183070`, the fade request `002EFA70(2, 8, 1)` and, when
`002677B0()` is non-zero, `00268690(9)` and the mapjump mode `00314DA0(003148D0() & ~0x18)`
([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)); then `002E1C40(1)`, flags bit
7 cleared, `00254A90`, `00259FB0`, `00234150`, `00250960(0, 0)` when `02099DA7` is set (then cleared),
and `00263660`.

### The wait resolver

`0025DF00(slot, record)` is what every drive above calls. For a record whose `+0x18` is not 1 it
first runs `002E4A10(record)`; then, for sequence class 3 only, when the steering request
`[[record + 0xB8] + 0xF0]` has a non-zero mode at `+0x29`, it calls `0026D6F0(record, speed * [01DFE0BC], mode)`
with the request's `+0x7C` as the speed and mode 0 when the speed is positive, 2 otherwise.

Then it resolves the current wait slot `[record + 0xA8] + (i8 record +0x11) * 0x28` in a loop:

1. when `001ED180()` is non-zero and `001EDE80()` is 0 the resolver leaves the loop (the half-rate
   gate);
2. the slot's `parked` byte `+0x16` is cleared; when `001EDDA0()` is 0 and the byte was set, a zero
   `001ED180()` leaves the loop;
3. the slot's `waitKind` `+0x14` selects the arm in the table below; a completed wait sets
   `waitKind` to 1 and loops, a held wait sets `parked` and leaves.

| Kind | Arm | Held while | On completion |
|---|---|---|---|
| 1, 2 | the bytecode interpreter `0025E4C0(slot, record, waitSlot)`, with `02099D80` = the record and `00357760()` before it | the interpreter returns non-zero, or `001ED130()` with slot index 1 or 2 and `001EC5C0()` = 0, or slot index 3 with `001EC5E0()`, or `022C7F84` non-zero; in each case only while `00357770()` = 0 | leaves the loop |
| 3 | `003DBF60(0020E600(targetRef), waitResourceId, -1)` | the entry is found (not `0xFF`) | `waitKind` = 1, `settled` = 1 |
| 4 | `003DC050(record, record +0x11, stamp - record +0x58)` | no entry (`0xFF`) | `003DB2A0(record, entry)` removes it, `waitKind` = 1 |
| 5 | `002674B0(slot, &targetRef)`: walks the list `listRef` names from the cursor `listCursor`, resolving each entry's low word as a record ordinal (`00358940`) and its high word as a resource id, and stops at the first `003DBF60(record, id, -1)` that is not `0xFF` | an entry is found | `waitKind` = 1 |
| 6 | `003DB640(0020E600(targetRef), waitChannel)` | the channel bit is set | `waitKind` = 1, `settled` = 1 |
| 7 | `00267420(slot, &targetRef)`: the same walk, stopping at the first record whose channel bit `waitChannel` is set (`003DB640`) | an entry is found | `waitKind` = 1, `settled` = 1 |
| 0, 8 and above | none | always | `parked` = 1 |

After the loop the resolver finishes the visit:

1. record `+0x108` is cleared;
2. record `+0x0C` bit 0 is set when `+0x1C` bit 11 is on, `+0x14` bit 6 is off, `+0x18` is not 1,
   and the entry `003DB550(record, +0x62)` has the id the record's `+0xDE` names (or, when that is
   -1, the word `+0x18` of the payload row reached through `+0x40`, used only when that row's count
   exceeds 11); otherwise it is cleared;
3. `+0x0D` bit 6 is cleared; for a record with `+0x10` = 0 that is settled or matched, with `+0x13`
   bit 1 and `+0x09` bit 7 clear, no `00359B80` value at `+0x40`, `+0x14` bit 4 set, `+0x18` = 0,
   `+0x09` bit 5 clear and a callback at `+0x38`, the bit is set and `[record + 0x38](slot index,
   record)` runs: the battle unit frame `00233F70` for a record bound to a battle unit;
4. the steering update runs: `002E97B0`, `002681E0`, `002E5030` and `002E5750` when `+0x13` bit 0 is
   clear and `+0x10C` is 0, or `+0x0B` bit 5 is set; otherwise `002E6310`.

### The wait slots

A record's wait slots are the `0x28`-byte entries at `[record + 0xA8]`, one per resource channel,
indexed by the record's `+0x11`:

Struct ActorWaitSlot size=`0x28`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `i32` | stamp | kind 4 compares it with the record's +`0x58` |
| `14` | `u8` | waitKind | 0 parked, 1 or 2 runnable, 3-7 the waits above |
| `15` | `u8` | commandPhase | 0 begin pending, 1 polling, 2 int result pending, 3 float result pending (`002621D0`) |
| `16` | `u8` | parked | set when a visit ends held |
| `18` | `i32` | targetRef | kinds 3 and 6: a base-relative reference (`0020E620` encodes, `0020E600` decodes against [`01F83530`]) |
| `1C` | `i32` | listRef | kinds 5 and 7: a base-relative reference to a list (i32 count, then i32 entries: record ordinal low, resource id high) |
| `20` | `u16` | waitResourceId | kind 3 |
| `22` | `u16` | listCursor | kinds 5 and 7: the entry the walk resumes from |
| `24` | `u16` | targetOrdinal | the record ordinal the interpreter armed the wait on |
| `26` | `u8` | waitChannel | kind 6 |
| `27` | `u8` | settled | cleared when a wait is armed, set by kinds 3, 6 and 7 |

The interpreter `0025E4C0` arms a wait only when the thing waited on is already active (for kind 6,
`003DB640` at `0025F593`, then the stores `0025F5A3`-`0025F5D4`, with `waitKind` and
`commandPhase` written as one word `0x0106`). `0020E620` subtracts the 32-bit base `[01F83530]` and
`0020E600` adds it back as 64 bits, so a reference is faithful only for objects within 4 GB above
the base.

## Layouts

```
return value = AND over the driven records of (record +0x14 bit 6)   (forced to 0 by branches 3 and the roster loop)
record +0x14: bit 4 drive the bound battle unit through +0x38 (0025DF00), bit 6 settled (both functions), bits 0-3 the repeat gate of branch 3
```

## Operations

- A pass that refuses still returns 1, so a caller cannot tell a refused pass from a settled one.
- `0025DF00` is called from five sites of the pass: the not-busy loop, the designated drive, the
  dead repeat, the roster loop and the all-records loop. A record is driven once per loop that
  names it, so a party member is driven by both the roster loop and the all-records loop.
- The init core runs on slot 0 in branch 3 after a designated drive and in branch 5 before the
  roster loop; its field initialisation runs once per field (flags bit 2).

## Modding notes

- A hook on `0025DF00` is called several times per actor per frame, once from each loop that names
  the actor; a hook on `0025D9E0` runs up to 16 times a frame per slot in mode 0.
- A script that must not lose a frame between a wait and its next statement needs no care: the
  resolver loops back into the interpreter in the same visit once the wait completes.
- The save-write busy flag stops every slot's pass, including the music select and the roster
  bookkeeping, until the write completes.

## Related

- [The actor record](actor-record.md): the record the pass drives and its `+0xA8` wait slots.
- [Actor managers](actor-managers.md): the slot block.
- [Zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md): the fade request and the mapjump mode.
- [Weather](../World-Areas-And-Travel/weather.md): the lane the init core passes on.
- [Saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md): the busy flag's writers.
