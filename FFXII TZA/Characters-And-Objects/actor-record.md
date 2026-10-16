---
title: "Actor record: the record every field actor is driven through, its pool, its classes, its sub-objects and its lifetime"
kind: "system"
category: "Characters and objects"
summary: "The record behind every actor a manager owns: how the pool is sized and carved from the loaded script payload's per-sequence counts and the eight-entry descriptor table, the class and sequence byte, what the initialiser writes into a fresh record, the interior sub-objects (movement context, secondary context, resource entry pool, wait slots) and where each class puts them, the resource entry lists and the channel masks, the handle fields, and the two-phase release that frees the pool."
addresses: ["002679F0", "00266530", "00266AD0", "00266BD0", "003DB580", "003DB550", "003DBF60", "003DB2A0", "003DB640", "00358940", "0025B070", "002628B0", "003697F0", "00265020", "00263C20", "003589B0", "002659D0"]
---

# Actor record: the record every field actor is driven through, its pool, its classes, its sub-objects and its lifetime

## What the player sees

Every townsperson, door, trigger line, party member and monster in a field is one record owned by
one of the five actor managers. When a field or a scene loads, the manager's script payload says
how many actors of each kind it brings, the records are carved out of one block, and each is set up
with its script entry, its position and steering state and its slots for resource requests and
waits. The record stays alive until the manager unloads, when the block is freed; the handle code
carries makes a stale reference fail instead of pointing at the wrong actor.

## How it works

### The pool

`002679F0(slot)` builds a manager's record pool from its bound payload (`[slot + 0x00]`) and the
record count at `+0x20` ([actor managers](actor-managers.md)):

1. the payload's table at payload `+[0x14]` holds a `u16` count of sequences followed by a `u16`
   per sequence; the pool's payload size is the sum over sequences of the descriptor's size,
   rounded up to 16, times that count;
2. the header is `(count * 8 + 0x17) & ~0xF` bytes and is allocated twice over: the block is
   `2 * header + payload` bytes from the allocator at `[slot + 0x88]`, zeroed, with the count at
   `+0x00`; `[slot + 0x1F0]` keeps `block + header`;
3. records are carved from `block + 2 * header` in sequence order; the pointer table at `block + 8`
   receives each, and each record's byte `+0x03` becomes `(class << 5) | sequence`; the slot's
   per-class counts at `+0x1D0` (four `u16`) are added up and their running offsets written to
   `+0x1D8`;
4. `00266530(slot, block, i)` initialises every record.

`00358940(slot, ordinal)` returns `[block + 8 + ordinal * 8]` for an ordinal below the count. The
descriptor table at `01E0C328` has eight entries of `{u8 class, u8 sub, u16 size}`:

| Sequence | Class | Sub | Size | Movement context | Secondary context | Resource entries | Wait slots |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | `0x328` | none | none | `+0x120`, 10 | `+0x1E8`, 8 |
| 1 | 1 | 0 | `0x3A8` | `+0x120` | none | `+0x1A0`, 10 | `+0x268`, 8 |
| 2 | 1 | 1 | `0x330` | `+0x120` | none | `+0x1A0`, 8 | `+0x240`, 6 |
| 3 | 2 | 0 | `0x348` | `+0x120` | none | `+0x140`, 10 | `+0x208`, 8 |
| 4 | 2 | 1 | `0x2D0` | `+0x120` | none | `+0x140`, 8 | `+0x1E0`, 6 |
| 5 | 3 | 0 | `0x6E0` | `+0x120` | `+0x350` | `+0x4D8`, 10 | `+0x5A0`, 8 |
| 6 | 3 | 0 | `0x6E0` | `+0x120` | `+0x350` | `+0x4D8`, 10 | `+0x5A0`, 8 |
| 7 | 3 | 1 | `0x668` | `+0x120` | `+0x350` | `+0x4D8`, 8 | `+0x578`, 6 |

`00266AD0(record)` plants the pointers from the sequence in `+0x03 & 0x1F`: `+0xB8` = the movement
context, `+0xC0` = the secondary context, `+0xA0` = the resource entry pool, `+0xA8` = `+0xA0` plus
`0xC8`, or `0xA0` when the descriptor's `sub` is 1. The resource entries are 20 bytes each and the
wait slots 40, so the wait slots end exactly at the record's size on every row.

### The class byte

Bits 5-7 of `+0x03` are the class and bits 0-4 the sequence. The movement code accepts class 3
(`+0x03 & 0xE0 == 0x60`); the position read `00265020` accepts classes 1 and 3; the `setline` verb
writes class 2 ([battle units](battle-units.md)). `00266BD0` seeds the flag dword `+0x1C` by
sequence: 0 for sequence 0, `0x38` for 1 and 2, `0x40` for 3 and 4, `0x30004` for 5 and 6, `0x34C85`
for 7, and sets `+0x14` bit 7 (battle-unit eligible) for sequences 5 and 7. A separate nibble, bits
0-3 of `+0x0E`, is what `00263C20` returns as the actor class nibble.

### The initialiser

`00266530(slot, block, i)` fills record `i` on a zeroed block:

1. it clears `+0x14` bit 7, zeroes `+0xEC` and sets `+0xF5` to `0xFF`, picks the counts (8 wait
   slots and 10 resource entries, or 6 and 8 for a `sub` of 1), plants the pointers (`00266AD0`) and
   seeds `+0x1C` and `+0x14` bit 7 (`00266BD0`);
2. it writes `+0x00` = `i`, `+0x10` = 0, `+0x12` = `0xFF`, `+0x15` = the slot index, `+0x16` = 1,
   `+0x118` = `0x3C0000`, `+0x102` = `0xFFFF`, `+0x04` = `0xFF00`, `+0x20` = `0xFF`, and `+0xF8` =
   the empty string at `02F8F2A0`, whose own byte it writes 0;
3. it writes `+0x100` = 0, `+0x18` = `0xFFFF0000`, `+0x104` = `0xFFFF`, `+0x106` = 0, `+0x0F` = 0,
   `+0x21` = 0, `+0x0A` = 0, the entry-group word `+0xF6` = 0, and zeroes `+0x28`, `+0x30`, `+0x38`,
   `+0x10C` and `+0x114`;
4. it sets the flag bytes: `+0x14` = `(old & 0xB0) | 0x30`, `+0x0D` = `(old & 0xA2) | 0x82` and
   `+0x08` = `(old & 0x9F) | 0x11` on manager 0 (`(old & 0x22) | 2` and `(old & 0x8F) | 1` elsewhere),
   then `+0x0D` bit 5 and `+0x08` bit 7 cleared, `+0x0B` &= `0xC0`, `+0x0C` = `(old & 0x71) | 8` then
   bits 4-6 cleared, `+0x09` bits 5 and 7 cleared, `+0x13` &= `0x3C`, `+0x0E` |= `0xF0` then `&= 0xF0`,
   and for class 3 `+0x1C` bits 8 and 13 cleared;
5. it binds the script entry: `+0x02` = 1, or 2 while `i` is below the payload's count word at
   `+[0x14] + 2`; `+0x40` = the entry at payload `+[0x18] + 4 + i * 0x20` (`0x30` when the payload's
   word `+0` is 8 or more); `+0x48` and `+0x50` = payload + the resolved dwords at entry `+0x10` and
   `+0x14`, `+0x58` = payload + entry `+0x08`;
6. a tagged entry (byte `+0x06` negative and not `0xFF`) registers the record in the pointer
   table at `0209A1F0` by its low 7 bits (`[0x120000 + rax * 8 + 0x1F7A1F0]`, `00266758`-`0026677C`):
   tags 0-3 are the party roster entries the field runtime walks ([field runtime](field-runtime.md)),
   and tags 4 and above the sixteen pointers from `0209A210` that `0026CE60` clears on slot 0;
7. the record that held a tag below 4 is evicted (`+0x12` = `0xFF`, `+0x0F` = 3), and the new
   record gets `+0x12` = the tag and `+0x0F` = 2 for tags 0-3, 3 above;
8. it builds the resource entry free list (`003DB580`) and clears bytes `+0x00`-`+0x16` of the
   first `+0x88` (channel count) wait slots, which covers every slot only because the two counts
   are both 8 or both 6;
9. it runs the movement defaults `00265FF0(record, [+0xB8])` and `00265B60`. `00265FF0` resets the
   context for the record's class and writes the class nibble: `+0x0E` = `(old & 0xB4) | 4` for
   class 1, `(old & 0xF5) | 5` and `+0x0F` = 3 for class 3, ending with `0026D6F0(record, 0.0, 2)`;
10. it resets the secondary context (`+0x138` = 0, `+0x148` = 1.0, `+0x14E` = 1, `+0x140` and
   `+0x144` = 0 with `00268380`), fills the eighteen words `+0xC8`-`+0xEB` with `0xFFFF`, and for a
   tagged entry with a secondary context sets its `+0x152` = 0 and runs `002681E0`;
11. it issues the initial resource requests through `003DBB60(record, channel, id, 2, 0)`, counting
   each request on the last channel in `+0x10`. On channel `channels - 1` it issues the `+0x20` id
   (only when the payload word `+0` is 10 or more; from `+0xE6`, else the entry row's word `+0x20`
   when the row's count is 16 or more), then id 0, then the `+0x14` id (`+0xDA`, else row `+0x14`
   when the count is over 9);
12. on channel 0 it issues the `+0x04` id (`+0xCA`, else row `+0x04` when the count is over 1), not
   counted. An id of -1 or an absent row word issues nothing;
13. for a class-3 actor it sets `+0x1C` bit 2 from the `+0x06` id (`+0xCC`, else row `+0x06` when
   the count is over 2), running `00268EA0` when `+0x0B` bit 3 is set, else clears bit 2; then bit 10
   from the `+0x16` id (`+0xDC`, else row `+0x16` when the count is over 10) with the same call, and
   setting bit 10 clears bit 2 again; else clears bit 10. It ends with `003DB280(record)`.

### The resource entry lists

The pool at `+0xA0` holds the record's 20-byte resource entries, linked by index: `003DB580` chains
them (`+0x00` next, `+0x01` previous, `+0x04` = `0x80000000`, `+0x10` = 0), sets the counts `+0x88`
(channels) and `+0x89` (entries), the free-list head `+0x60` = 0 and the detached head `+0x61` =
`0xFF`, the channel heads `+0x94` and tails `+0x8C` to `0xFF`, and clears the masks `+0x06` and
`+0x24`. `003DB550(record, index)` returns `[+0xA0] + index * 0x14`, null for `0xFF`.

- `003DBF60(record, id, class)` walks every channel whose bit in `+0x06` is set, from its head,
  returning the first entry whose `+0x04` word equals `id` or whose `+0x12 >> 1` equals `class`
  (either filter may be -1), bounded by the entry count; `0xFF` when none.
- `003DB640(record, channel)` tests bit `channel` of `+0x06`.
- `003DB2A0(record, index)` removes an entry. An entry in state 4 (`+0x10`) or with a negative
  channel byte `+0x02` is on the detached list at `+0x61`, otherwise on its channel's list at
  `+0x94[channel]`. The remover:
  1. unlinks it (`003DC1B0`);
  2. on a channel list, notifies the end of a mode-3 request whose `+0x06` is not `0x8000`
     (`003DC0D0`), notifies by class (`00263050`) when `+0x12` is 2 or more, fixes the head and tail,
     and clears bit `channel` of `+0x06`, `+0x24` and `+0x26` when the channel empties;
  3. pushes the entry on the free list (`003DB650`), sets `+0x63` bit 1 and makes it the head.

### The handle

A record is named outside its manager by the handle `003589B0` encodes from `+0x00` (the index),
`+0x15` (the manager) and `+0x16` (the discriminator, seeded 1 by the initialiser and advanced by
`002659D0` through 1-2047 on a definition change); the resolver `003588B0` checks all three against the live record ([battle
units](battle-units.md)).

### Release

A manager's teardown `002628B0` runs in two phases.

1. `0025B070(slot)` is the semantic cleanup, run for every slot but 4. For the class-1 and
   class-3 records (the ranges
   `+0x1DA`/`+0x1D2` and `+0x1DE`/`+0x1D6`) it ends the movement context's `+0x74` or `+0x220` job
   (`0024CFF0`) and zeroes it.
2. For the class-3 range it also runs `002693D0(record, 1)`, the per-`+0x04` teardown (`002E3AF0`,
   `003DE5F0` or `002E3D00` for 1, 2 or 3) and sets the `+0x04` word to `0xFF00`; then for every
   record with `+0x14` bit 7 and a unit at `+0x30` it releases the unit (`00234200`) and runs
   `002EB780`.
3. The owning release: the block at `[slot + 0x08]` is freed with `003697F0`, the pointer nulled,
   the slot's `+0x10` bit 0 and `+0x200` bit 2 cleared and `+0x13` zeroed (`00262D96`-`00262DB3`).
4. The slot's `+0x00`, `+0x30`, `+0xE8`, `+0x1E0` and `+0x1FC` are zeroed and `+0x17` bit 3 is
   cleared; the live-slot totals `02099DB4`/`02099DB8` and the flag `02099DA1` are recomputed over
   slots 0-2; the slot's `+0x108` callback is called once with the slot and then nulled.

Every record address and interior pointer is valid only until that release.

## Layouts

```
struct ActorRecord size=by sequence (0x2D0 to 0x6E0)
+0x000  u16   index            the record's ordinal in its manager
+0x002  u8    entryClass       1 or 2 from the initialiser
+0x003  u8    classAndSequence bits 5-7 class, bits 0-4 sequence
+0x004  u16   definitionState  0xFF00 at init and at release
+0x006  u16   channelActiveMask
+0x008  u8    flags08          bit 6 set by the field runtime's roster and record loops
+0x00A  u8    field0A          0 at init
+0x009  u8    flags09
+0x00B  u8    flags0B
+0x00C  u8    flags0C          bit 0 the wait resolver's id match
+0x00D  u8    flags0D          bit 6 set while the +0x38 callback runs
+0x00E  u8    flags0E          bits 0-3 the class nibble (00263C20): 4 class 1, 5 class 3 (00265FF0)
+0x010  u8    pendingRequests  resource requests the initialiser issued; 0 = idle for the field runtime
+0x011  i8    currentWaitSlot
+0x012  u8    slotTag          0xFF, or the entry's tag
+0x013  u8    flags13
+0x014  u8    flags14          bit 4 drive the battle unit, bit 6 settled, bit 7 battle-unit eligible
+0x015  u8    managerIndex
+0x016  u16   discriminator    1 at init
+0x01C  u32   flags1C          seeded by sequence (00266BD0)
+0x024  u16   channelMask24
+0x026  u16   channelMask26
+0x030  u8*   battleUnit       002134A0
+0x038  void* frameCallback    00233F70 for a unit-bound record
+0x040  u8*   scriptEntry      the payload's entry for this actor
+0x048  u8*   functionTable    payload + entry +0x10
+0x050  u8*   jumpTable        payload + entry +0x14
+0x058  u8*   bytecodeBase     payload + entry +0x08
+0x060  u8    entryFreeListHead
+0x061  u8    detachedEntryListHead
+0x062  u8    selectedEntryIndex
+0x063  u8    entryListFlags
+0x064  i32[4] vmRegI          the script VM's integer registers
+0x074  f32[4] vmRegF          the script VM's float registers
+0x088  u8    channelCount     8 or 6
+0x089  u8    entryCount       10 or 8
+0x08C  u8[8] channelTail
+0x094  u8[8] channelHead
+0x0A0  u8*   resourceEntries  20-byte entries
+0x0A8  u8*   waitSlots        40-byte slots (field runtime page)
+0x0B8  u8*   movementContext  0x230 bytes at +0x120
+0x0C0  u8*   secondaryContext 0x188 bytes at +0x350, class 3 only
+0x0C8  u16[18] overrides      0xFFFF at init
+0x0F6  u16   entryGroup       0 at init; stamped by 0026CE60
+0x0F8  u8*   nameText         the literal name (npc-names page)
+0x100  u16   nameLength
+0x102  i16   nameId
+0x118  u32   field118         0x3C0000 at init
```

```
struct ActorResourceEntry size=0x14
+0x00  u8   next
+0x01  u8   prev
+0x02  i8   channel      negative: on the detached list
+0x04  u16  resourceId
+0x06  u16  field06      0x8000 when unset
+0x10  u8   state        3 a request in flight, 4 detached
+0x12  u8   classAndFlag the class in bits 1-7
```

## Operations

- The pool is one allocation per manager; the record count, the per-class counts and the carve
  order all come from the payload's sequence table, and the class is stamped before any record is
  initialised.
- Interior pointers (`+0xA0`, `+0xA8`, `+0xB8`, `+0xC0`) point into the record itself and are valid
  for the life of the block.

## Modding notes

- A script's actor counts set the pool: adding an actor to a scene means adding it to the payload's
  sequence table, which sizes the block.
- Only class-3 records carry a secondary context and can be steered; a class-1 record has a
  position but no steering, a class-2 record is a trigger line.
- Hold a handle, not a record pointer, across a field change: the block is freed at unload.

## Related

- [Actor record fields](actor-record-fields.md): every reached offset and the two contexts' access tables.
- [Actor managers](actor-managers.md): the slot the pool belongs to.
- [Field runtime](field-runtime.md): the wait slots and the drive loops.
- [Battle units](battle-units.md): the unit bound at `+0x30` and the handle.
- [NPC names](npc-names.md): `+0xF8` and `+0x102`.
