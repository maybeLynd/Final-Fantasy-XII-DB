---
title: "Script name bindings: how a script names a model by one number, the binding table with its lists and lanes, where a treasure chest is placed, and the bind verbs"
kind: "system"
category: "Scripts and script commands"
addresses: "002E97C0, 002E9810, 0215FDA0, 02161DA0, 002EA320, 002E25E0, 002E9360, 002EB540, 002EAE20, 002E99C0, 002E4C20, 002E3E20, 002E3DC0, 002E3E90, 002EAF70, 002EB810, 002EBD60, 002EAEB0, 002E65A0, 002E6D60, 002E6700, 002EAD50, 002E4D20, 002EA6E0, 002E60F0, 002ED6F0, 002ED950, 002E9A60, 002EB7A0, 0032E400, 002E2660, 002EB5E0, 002EB9D0, 002E9920, 002EB690, 002EAFA0, 002EB890, 002E3F00, 002E4000, 002E6880, 002E6EB0, 002E4E50, 002E6900, 002E9470, 002ECAB0, 002ECA30, 002ECBA0, 00354400, 00354A40, 00355210, 002FAED0, 002FAF60, 0026E060, 002650B0, 0026A320, 002E28E0, 002E3110, 002EBC90, 002E3C20, 0037CB90, 0033F330, 00340380, 003409F0, 00342640, 003418B0, 00344F00, 00345A60, 003460F0, 00343B00, 00344550, 00343A30, 00344200, 003463F0, 003EB190, 00340FA0, 003414A0, 00341840, 00340450, 00340EC0, 0034B8D0, 0050D810, 0037B4D0, 00267310, 00314D40, 008F8180, 008F6D54, 01CEBC78, 002ECFD0, 00347DD0, 002E9C30"
---

## What the player sees

A treasure chest stands in a fixed spot facing a fixed way, and some chests are only there some of
the time. A story scene gives a character a different body, hands an actor a weapon or a prop, or
attaches a puppet; the scene pauses for a moment while the model loads. Every one of these is a zone
script naming a model by one number and asking the engine to bind it to an actor.

## How it works

### The bound id: what a script names

A script names a model with a 32-bit bound id: bits 16 to 23 are a letter class and bits 0 to 15 a
number. `002E9A60` turns a script's argument into a bound id. A value above `0xFFFFFF` is an index
into the script image's name table at `[context + 0x100]` (`00263F80`: a count, then one dword per
name; an index at or past the count gives 0, and a missing table gives the low 24 bits unchanged).
Smaller values go through `002EB7A0`, which turns 0 and 1 into `0x630000`, 8 and 9 into
`0x6E0001`, `0xC` and `0xD` into `0x770002`, and passes every other value through.

`002ED6F0` splits a bound id into a resource kind and a file index and returns the number of lanes
the model has (the table under Layouts). `002ED950` returns the model's row in a per-letter table for
the classes `b`, `c`, `g`, `m`, `n`, `s`, `t` and `w` (`[021641A8]` to `[021641E0]`, a count at `+8`
and 16-byte rows); any other class, or a number at or past the count, gives null.

### The handle: one number checked before use

The table is 128 entries of `0x40` bytes at `0215FDA0`, followed by 32 lane records of `0x120` bytes
at `02161DA0`. A handle is `(dword [entry + 0x24] << 16) | word [entry + 0x1A] | 0x8000`
(`002E9810`, which returns 0 for a null entry). `+0x1A` is the entry's own slot and `+0x24` its stamp.

`002E97C0` resolves a handle: 0 fails; the slot is `handle & 0x7FFF` and must be below `0x80`; the
entry at `0215FDA0 + slot × 0x40` is returned only when its recomputed handle equals the argument,
and null otherwise. A handle with bit 15 clear never matches. A stale handle names a live slot whose
stamp has moved on, so it resolves to null rather than to another model.

The stamp is a dword at `+0x24`. The allocator `002E25E0`, the re-lister `002EAEB0` and the release
`002E9360` each increment it and then zero the word at `+0x26`, so it counts in 16 bits and wraps from
`0xFFFF` to 0; the initialiser `002EA320` sets every stamp to 0.

### The four lists

Every entry is on exactly one doubly linked list through `+0x00` (previous) and `+0x08` (next):

- **free**, head `0215FD60`. `002EA320` links slots 0 to 127 in order with slot 0 at the head. The
  allocator pops the head; the release pushes on it.
- **requested**, head `0215FD78`. Find-or-create pushes a new entry here.
- **live**, head `0215FD58`. The request pump moves each requested entry here once its load is filed.
- **retired**, head `0215FD88`. The re-lister moves an entry here when its last holder lets go.

`002EA320` (called from `00266D10`) also clears the other heads, fills the lane records, and
registers the binding callbacks with `0041D6C0` (kinds 5, 4, 6, `0xC`, `0x26`) and installs the retire
step `002E6D60` as the allocation-pressure callback of memory arenas 6 and 10 (`0036C5A0`, arena
record `+0xA0`).

### Find-or-create, holders and the reference count

`002EB540(id, selector)` searches the live list, then the requested list, for an entry whose `+0x14`
equals the id. On a miss it allocates one, pushes it on the requested list and sets pin bit 3
(`+0x19 |= 8`). Either way it sets bit `selector` of the holder word `+0x20`. `002EAE20(id)` does the
same search and creation without pin bit 3 and sets holder bit 0. Neither guards its final writes
against a null allocation: with all 128 entries in use both write through a null pointer.

`002E25E0(id)` pops the free head, increments the stamp, keeps only bits `0xC8` of `+0x19`, zeroes
`+0x10`, `+0x18`, `+0x1C`, `+0x20`, `+0x26` and `+0x28..+0x2F`, stores the id at `+0x14`, sets
`+0x1E` to `0xFFFF` and `+0x30..+0x3B` to `0xFFFFFFFF`, and unlinks the entry.

The bind `002E28E0` and the attach `002E3110` add one to the reference count `+0x1C` and clear
`+0x18` bit 2. `002EB810(id)` and `002EAF70(entry)` take one away. An entry with pin bit 0 or 1 set
(`+0x19 & 3`; `002EBD60(id, on)` sets bit 0) has its count clamped to 0 instead of being released.

Four routines release an unreferenced entry through the re-lister `002EAEB0`:

- `002E3E20(selector, direction)` walks the live list only. A positive direction clears the
  selector's holder bit, a negative one clears the whole holder word. On an entry whose count is 0 or
  less it then clears the selector's bit (for any direction), and re-lists it when the holder word is
  empty and pin bits 0-1 are clear.
- `002E3DC0(id)` re-lists the entry for the id when its count is 0 or less and it is not pinned.
- `002E3E90(id)` does the same, except that it leaves an entry with `+0x19` bit 4 set.
- `002EAF70(entry)` drops one reference and re-lists at 0 or less, unless pinned.

`002EAEB0(entry)`: while the entry is not ready (`+0x18` bit 1 clear) and `+0x19` bit 2 is clear, it
only sets `+0x18` bit 2 and returns, deferring the release until the load completes. Otherwise it
increments the stamp, clears the ready bit, copies the new stamp into the entry's lane record, and
moves the entry from the live or requested list to the head of the retired list. Every handle given
out for the entry stops resolving at that moment.

### The per-frame binding update

`002E65A0` runs the whole cycle. Its callers are `002628B0` and `0022A770`, `0022AF50`, `0022B000`,
`0022B6E0`, `0022B7E0`, `0022B8C0` and `0022BC20`.

In order it calls `003DC4A0`; runs the whole lane
unload queue (`002E6900(1)`); releases the retired entries; runs the unload queue again; compacts
memory arenas 6 and 10 (`00369C60`) when the retired list was not empty; clears `0215FD46`; runs the lane pump `002E6880` and the request
pump `002E6700`; calls `003DD4C0`, compacts arenas 6 and 10 again, calls `0037B2F0`; and finally calls,
once, the callback that `002EACC0` stored at `0215FD98` with the value at `021641F0`.

Retired entries are released from the tail of the list (the oldest) towards the head. An entry whose
load handle `+0x10` is non-zero is first unloaded from the render system (`0041E490` through
`0020E600([022C6F28 + 0x48830])`) unless `+0x18` bit 3 or `+0x19` bit 2 is set, then released by
`002E9360`.

An entry whose `+0x10` is 0 is not passed to `002E9360`: when the walk reaches the head it nulls
`0215FD88`, so the entry ends up on no list and its slot is lost until `002EA320` runs again.

`002E6D60`, which arenas 6 and 10 call when an allocation in them fails, unloads
the oldest queued lane record (`002E6900(0)`; with a non-zero argument `002E6900` runs the whole
queue), then releases the single oldest retired entry the same way, and runs the queue once more
when there was none. While the oldest retired entry has `+0x10` = 0 and is not alone on the list,
`002E6D60` picks it on every call and makes no progress.

`002E9360(entry)` queues all 32 lanes of the entry's lane record for unload (`002EAFA0`, unloaded
later by `002E6900`) when that record's stamp `+0x5C` matches, releases the three sub-resources at `+0x30`, `+0x34`, `+0x38` through `003A0F80`,
frees `+0x10` through `00369800` when non-zero, calls `0017F040` with the id, unlinks the entry from
whichever list holds it (moving the free or retired head past it), pushes it on the free list,
increments the stamp, zeroes `+0x26`, `+0x18` and the id `+0x14`. It does not reset `+0x1E`; the
next allocation does.

### Loading an entry

The request pump `002E6700` takes every entry on the requested list. It splits the id with
`002ED6F0` (adding `0x33` to the index for kind 1), asks `0032E400(kind, index)` for the file's
size: `002DF960`'s size rounded up to a multiple of 64 (the per-kind override table at
`022C51F0` it consults first is only ever zeroed, by `0032EA90`, among the static references to
it). It then sets `+0x19` bit 2 and zeroes `+0x10`.

A positive size gets a buffer from `0036B160`, whose handle goes to `+0x10`; when
that succeeds it clears bit 2, files the load with `002EAD50`, and for an entry with pin bit 3
calls `0036C5D0(handle, 1)`. The entry then moves to the live list and pin bit 3 is cleared.

`002EAD50` files `0032E620(kind, index, buffer, size, record)` with the completion callback
`002E4D20` and the entry as its argument. On completion `002E4D20` registers the model with the
render system (`0041E580`) unless a release is already pending (`+0x18` bit 2), in which case it
sets `+0x18` bit 3. It then asks `002EA6E0` whether sub-resources follow: when none do, it sets the
ready bit `+0x18` bit 1 and, if a release was deferred, re-lists the entry at once.

`002EA6E0` files a task with step function `002E60F0` when the model has a row in `002ED950` and
no release is pending. `002E60F0` reads the row's three signed words at `+0`, `+2`, `+4`. A negative
word stores `0xFFFFFFFF` in its slot. Otherwise the word w becomes a class-`0x20` file index (0 → 0,
1 → 1, 2 → 3, below 500 → w − `0xC0`, otherwise w − `0x188`), whose size comes from `0032E400` and
whose load goes into slot `+0x30`, `+0x34` or `+0x38`. When all three are done it sets the ready bit
and re-lists the entry if a release was deferred.

`002E4C20(entry)` is the ready test every wait uses: `+0x18 & 2`, and 0 for a null entry.

### Lanes: the 32 extra files of a binding

A model can own up to 32 extra files (lanes); the lane count comes from `002ED6F0`. With i the index
`002ED6F0` gives, lane n is file `i + 1 + n` of the same kind, or `i + 0x43 + n` for kind 1
(`002E9920`). For class `m` (`0x6D`) lane 0 is file `i + 1`, lanes 1 to 15 are all file `i + 2`,
and lane 16 and above are file `i + 1 + n − 14`.

The lane records are 32 × `0x120` bytes at `02161DA0` on their own lists: free `0215FD70`, idle
`0215FD68`, pending `0215FD80`, and the unload queue `0215FD90` (linked through the second node at
`+0x10`/`+0x18`). `002E2660(entry)` pops a free record, zeroes its masks, handles and counts, and
cross-links it: record `+0x22` = the entry's slot, entry `+0x1E` = the record's index `+0x20`,
record `+0x5C` = the entry's stamp. Every lane access checks `+0x5C` against the entry's stamp first.

`002E9C30(entry)` returns the entry's lane record when the entry has one and its stamp matches,
null otherwise; the model loader `002EE430` uses it.

`002EB5E0(entry, lane, delta, group)` picks the lane with `002EB9D0`, creates the lane record if the
entry has none, and requests lane 0 and the chosen lane through `002EB690`. `002EB9D0(entry, n)`
sets lane n in the entry's `+0x28`; when the lane's file has a positive size (`002E9920`) it also
sets `+0x2C` and returns n, otherwise −1. A lane already in `+0x28` gives n only when it is in
`+0x2C`. A negative n tries lanes from 1 upwards below the lane count (at most 32) the same way.

`002EB690(record, lane, delta, group)` adds delta to the lane's count `+0xE0 + lane × 2`, clears the
lane's bit in `+0x2C`, sets it in group word `+0x48 + group × 4`, and, when the lane is in none of
`+0x24`, `+0x28`, `+0x34`, sets it in `+0x28` and moves the record to the pending list. The lane pump
`002E6880` runs `002E6EB0` on every pending record and moves it to the idle list.

`002E6EB0` loads each lane in `+0x28` whose handle `+0x60 + lane × 4` is still 0: a buffer from
`0036B160`, `0036C5D0(handle, 1)` when the lane is in `+0x44`, and `0032E620` with completion
callback `002E4E50` and tag `record index << 16 | lane`. It clears the lane from `+0x28` and, when the
load was filed, from `+0x44` and into `+0x34`. `002E4E50` moves the lane from `+0x34` to `+0x24`,
registers it with `0041E580`, and drops one count (`002EB890`) when the lane was queued for unload
meanwhile; for an owner that no longer resolves it queues the lane for unload instead.

A lane is held while its count is positive, while it is in any of the five group words
`+0x48..+0x5B`, or while it is in the hold mask `+0x38` (the readers `002E3F00`, `002E4000` and
`002EB890` also test `+0x3C`, which has no writer among the xrefs to it).

`002ECAB0(id, lane, on)`
sets or clears the lane in `+0x38`, and `002ECA30(entry, lane, on)` does the same in `+0x40`, a mask
only `002E9C60` reads and `002E6570` clears in all 32 records. Both act only on a lane already in
`+0x24`, `+0x28` or `+0x34`, so a hold set before the lane is requested is dropped; with lane 0
present, lane 0 follows the other bits (set while any other bit is set, otherwise the whole mask is
cleared). `002ECBA0` sets the lane and lane 0 in `+0x44` when its third argument is 1.

`002EAFA0(record, lane)` queues a lane for unload: when the lane is not already in `+0x2C` and is in
`+0x24`, `+0x28` or `+0x34`, it sets `+0x2C`, and a loaded lane (`+0x24`) puts the record on the
unload queue. `002E6900` unloads each queued lane that is loaded (`0041E490`, then `00369800`),
clears it from `+0x24` and `+0x2C`, takes the record off the queue, and returns it to the free list
(`002E9470`) once neither `+0x28` nor `+0x24` has a lane left.

After that pass, every record still
queued whose owner slot `+0x22` is negative goes to `002E6A80` (`002E6A4E`), even for `002E6900(0)`:
it unloads each queued, loaded lane (`002E6E30`), takes the record off the queue and frees it under
the same test. `002E9470` resets the owner's `+0x1E` to `0xFFFF` when the
stamps still match.

`002E3F00(id, lane)` queues the lane, and then lane 0, when its count is 0 or less and it is not in
`+0x38`/`+0x3C`; a held lane has its count clamped to 0. `002E4000(group, direction)` walks the idle
records, clears the group bit (positive direction) or the whole group word (negative), and queues
every lane whose count is 0 or less and that no group word and no hold mask keeps. It does not bound
the group: a group of 5 or more indexes past `+0x58`.

### setuptreasure: placing a chest

`setuptreasure` (verb `0x2BE`) has begin `00354400`, poll `00354A40` and result `00355210`.

The begin hides the actor (`0026A320(actor, 0)` clears `+0x0C` bit 7), pops the spot reference into
`args[2]`, and takes the chest model from the current map header: `0026E060` reads the word at
`+0x88` of the header `[02098E10]` when `02098E20` bit 0 is set, the header's first word exceeds 10
and the signed word is not negative, with `[02099D70]` switched to `02098E10` for the call. Because
`word | 0x3000000` is above `0xFFFFFF`, `002E9A60` takes the chest model from the calling script's
name table at that index (`00263F80`). Otherwise the model is −1.

It then resolves the chest record with `002650B0` and rolls for the chest with `002FAED0`: no chest
when the opened flag `0032AA60(record[+9])` is set (bit `record[+9]` of the 256-bit set at `+0x14B4`
of `002EF2B0()`); otherwise a chest when `rand % 100 < record[+0xA]`. A flag byte of `0xFF` tests bit
255, while the payout `002FAFD0` never sets the flag for `0xFF`. Both outcomes of the roll are recorded with
`002FB430`. No chest sets the model to −1. A model of −1 leaves `args[0]` at 0; any other model is
found or created with `002EAE20` and its handle stored in `args[0]`.

The poll ends at once when `args[0]` is 0. Otherwise, a handle that no longer resolves is re-created
from the model id in `args[1]` and stored back, and the poll waits (raising the loading flag
`022C253D` through `00314D40(1)`) until the entry is ready.

The result resolves `args[0]`; when that fails it returns with the actor still hidden. Otherwise it
resolves the chest record again, shows the actor (`0026A320(actor, 1)`), decodes the spot with `002FAF60`,
places the actor at the position (`0026AF80`), sets its facing and its movement heading to the same
angle (`0026B620`, `0026A0D0`), sets its separation weight to −1.0 (`0026DAC0`), binds the model
(`002E28E0`) and sets the movement body's mask word to `0x10` (`002EC5B0`).

`002FAF60` decodes the placement from the chest record, and `setuptreasure`'s result is its only
caller. Byte `+8` is shared: bits 0-5 are the facing and bit 6 is the random-gil flag the payout
reads ([reward verbs](reward-verbs.md) has the contents fields `+0xB..+0x17`).

```python
x = (int16) record[+0x04] / 10.0            008F8180 = 10.0
y = 0.0
z = (int16) record[+0x06] / 10.0
w = 1.0
heading = -(record[+0x08] & 0x3F) / 60.0 * 2*pi   008F6D54 = 60.0, 01CEBC78 = 6.2831855
```

The position is in tenths of a unit, the height is never authored, and the facing steps in 6°
units; codes 60 to 63 go past a full turn and are not clamped.

### The bind: what binding a model to an actor does

`002E28E0(actor, entry)` needs the actor's presentation context `[actor + 0xC0]`; without one it
only runs its tail (`002EB930`). With one, it marks the actor (`+0x0D` bit 1, `+0x04` = 1), takes a
reference on the entry and clears its pending-release bit, and creates the render record with
`0042FB80(entry +0x10, context +0x14C, context +0x14D)` while `01F7F508` holds the entry's id. The
record's index goes to context `+0x00`, the id to `+0x04` and the entry pointer to `+0x08`.

Render records are `0x740` bytes from `[022C6F28]`; one is used only when its `+0x284` is non-zero.
The bind copies context `+0x10 >> 4` to render `+0xC1`, stores the actor at render `+0x108`,
calls `003E5E20(render, [actor + 0x30])`, copies context `+0x14F >> 3` to render `+0x413` and
context `+0x150` to render `+0x40C`, and, for an actor with `[actor + 0x30]`, initialises its slot
with `003E7500`.

It then reads keyed parameters of the model with `003E6150(render index, key)`: `0x09000606` to
`[actor + 0xB8] + 0xE0`; `0x09000707` × 1.0 (`01DFE0BC`) to `+0xE4`; `0x09001F20` and `0x09002021` to
`0026AA30`; `0x01002D4F`/`0x01002E50` in a town (`00377C20`: bit 15 of the map's word in `[02ADD100]`), otherwise
`0x01002143`/`0x01002244`, to `0026B2E0`; `0x09001D1E` to `00269E60`;
`0x600A1244` (integer, `003E6310`) to `0026AF40`; and `0x09002322`, `0x09002524`, `0x09002423`, each
× 50, to `0026A370`. `0x09042A2E` is read and its value never used.

For an actor of kind `0x60` (`+3 & 0xE0`) it also sets the three floats at `[+0xB8] + 0x20..0x28`
to 1.0 and calls `002E8E20`. It sets `+0xF0` = `0x1001`, `+0xF5` = `0xFF`, `+0xEC` = 0, calls
`002EB0D0` unless `+0x18` is 1, and files `002652D0(script, actor, 2)`.

### The attach slots

The presentation context carries the main binding at `+0x00` and attach slots of `0x30` bytes:
`+0x30`, `+0x60`, `+0x90` and two at `+0xC0` and `+0xF0`. Each slot holds a render index, the bound
id, the entry pointer and a flags byte at `+0x10`. `002EBC90(actor, which, on)` sets the high
nibble of a slot's flags byte (`which` 0 the context itself, 1 `+0x60`, 2 `+0x30`, 3 `+0x90`, 4 and
5 the two last slots).

`002E3110(actor, kind, n, entry, link)` attaches an entry: kind 0 → `+0x30`, 1 → `+0x60`, 2 and 4 →
`+0x90`, 3 → `+0xC0 + n × 0x30` (n unbounded here). It returns without doing anything when the actor
has no presentation context, when the context has no main entry (`+0x08` = 0) or for a kind above 4,
so `bindh` and `bindc` on an actor that was never bound do nothing.

A slot already in use is detached first and its entry loses one reference (`002EB810`). The attach
takes a reference, creates the render record with
`0042FB80(entry +0x10, 1)`, links it to the main record with `002EDAA0(main, link, slot)` (kinds 2
and 4 force link `0x7FFF`) and calls `002EE050(slot, 1.0, 1.0, 1.0)`. Kind 2 clears render `+0x304` bit 6 and kind
4 sets it (when `01FD49EC` is set).

`002E3C20(actor, kind, n)` detaches a slot (`002E3A60`) and refreshes the actor's visibility.

### The bind verbs

| verb | id | callbacks | what it does |
|---|---|---|---|
| `bindp` | `0x00C` | `00340380`, `003409F0`, `00342640` | pushes 1 and 0, then runs `bindp2_d4` |
| `bindp2_d4` | `0x0D4` | `0033F330`, `00342330` → `003409F0`, `00343760` → `00342640` | binds a model and its body replacement |
| `unkCall_5cb` | `0x5CB` | `00340380`, `003418B0`, `00343760` → `00342640` | `bindp` without the body replacement |
| `bindh` | `0x0D7` | `00344F00`, `00342330` → `003409F0`, `00345A60` | attaches a model at `+0x90` (kind 2) |
| `bindhoff` | `0x0D8` | result `003460F0` | detaches `+0x90`, then reattaches the body replacement |
| `bindc` | `0x200` | `00343B00`, `00342330` → `003409F0`, `00344550` | attaches at `+0xC0` or `+0xF0` (kind 3) |
| `puppetbind` | `0x41B` | `00343A30`, `00344200`, `003463F0` | creates a puppet from a model |
| `puppetbind_41c` | `0x41C` | `00344D80`, `00345FB0` → `00344200`, `003463F0` | pushes 0, then `puppetbind`'s begin |
| `puppetbind_41d` | `0x41D` | `00345AE0`, `00345FB0` → `00344200`, `003463F0` | pushes 1 and 0, then `puppetbind`'s begin |
| `modelread` | `0x0BF` | begin `00340FA0` | requests a model; raises the loading flag while it is not ready |
| `modelreadsync` | `0x0C0` | `003414A0`, `00341840` | waits for a model requested earlier |
| `stdmotionreadsync` | `0x119` | poll `0034B8D0` | waits for the actor's motion lane |
| `charcachedispose` | `0x146` | `00340450`, `00340800` | releases this script's holds |
| `charcachedisposeall` | `0x3C8` | `00340EC0`, `00340800` | releases every hold |
| `debug_bindp` | `0x2000` | `0050D660`, `0050D710`, `0050D810` | binds a model with a free lane, sets `+0xF0` = `0x1001` |

Every begin that creates a binding does nothing when the script manager's byte at
`02099011 + manager × 0x288` is set (`00267310`, manager = actor `+0x15`); the begins of
`bindp2_d4`, `bindh`, `bindc` and `puppetbind` then clear the active byte in their arguments so the
poll and result skip. `bindp2_d4` also skips an actor whose `+0x18` is non-zero.

`bindp2_d4(model, b, c)` (`0033F330`) pops c, b and the model, stores b and c in context `+0x14C`
and `+0x14D` (`0026D610`, actors of kind `0x60` only), and finds or creates the model's entry with
holder bit = manager; with actor `+0x18` non-zero it still raises the loading flag. Its poll
`003409F0` runs a state word at `args + 0xA`: state 0 waits for the
entry; when it is ready it looks up a body replacement with `0037CB90(model, b, c)`.

`0037CB90` takes the first row of the replacement table `[02ADD940]` that matches (count
`[02ADD938]`, rows of `0x30` bytes: model, b, c with −1 matching anything, a pair count at `+0xC`,
up to four values at `+0x10` and thresholds at `+0x20`) and returns the last value whose threshold is
at or below the story-progress word (`00265270`), or −1; it returns −1 while `01E02800` is 0 or the
table pointer is null.

No replacement: state 1, and the
result binds the model. A replacement: the poll binds the model itself, finds or creates the
replacement's entry with holder bit 0, and waits in state 2; when it is ready, state 3 and the
result attaches it at `+0x90` (kind 4).

`unkCall_5cb`'s poll `003418B0` stops at state 1 once the entry is ready, so its result always
binds the model alone. `bindh(model)` finds or creates the entry and its result attaches it as kind
2 with `002EBC90(actor, 3, 1)`. `bindc(n, model, link)` clamps n to 0..1, and its result attaches the
entry as kind 3 in slot n with `002EBC90(actor, n + 4, 1)` and the given link. `bindhoff`'s result
detaches kind 2 and, when the actor's model has a replacement that is already ready, attaches it as
kind 4.

`puppetbind(d, model, x, y)` (`00343A30`) finds or creates the model with `002EAE20` and keeps the
manager byte; its poll waits for the entry, re-creating it if the handle went stale; its result
calls `003EB190(d, entry, manager, x, y)`, which replaces puppet slot d (below 32) in the table at
`02B5EA20`. `puppetbind_41c(d, model, x)` passes y = 0 and `puppetbind_41d(d, model)` passes
x = 1, y = 0.

`modelread(model)` finds or creates the entry with holder bit = manager and raises the loading flag
when the entry is not ready. `modelreadsync(model)` stores the handle of the model's entry (0 when
none exists); its poll waits until the entry is ready, counting the waits in `args[2]`, and ends at
once for a handle of 0 or one that no longer resolves.

`stdmotionreadsync`'s poll `0034B8D0` reads the actor's motion lane, the signed byte
`[actor + 0xC0] + 0x12` (`002E9C00`, −1 without a context), and tests it on the main entry with
`002E4C30` (the lane's `+0x24` bit; 1 for a negative lane; −1 without a matching lane record). A
loaded lane ends the poll after `002EAC90` (and `002EB380` when actor `+0x0D` bit 7 is set).
Otherwise it claims the lane with `002EB9D0`, raises the loading flag and waits; it ends at once
when the claim fails or the context has no main entry.

`stdmotioneventsync` (`0x0473`) waits for a marker in the actor's motion. Its begin `002ECFD0`
(through `003479E0`) clears bits 0 and 1 of the render record's `+0x419` (`0042F210` for each);
its poll `00347DD0` ends when either bit is set again (`002ECF60`, `0042F1C0`). The motion sets
them through its authored command id 4, subtypes 11 and 10 (`00417AD0`).

`debug_bindp(model)` (`0050D660`) finds or creates the model with `002EAE20` (holder bit 0), stores
the entry pointer itself rather than a handle, claims a free lane (`002EB9D0(entry, −1)`), requests
it with `002EB490` and stores it with `002EC6B0`. Its poll `0050D710` waits for the entry to be
ready and the lane loaded; its result `0050D810` binds the stored pointer and calls
`002EB330(actor, 0x1001)`.

`charcachedispose` calls `002E3E20(manager, 0)` and `002E4000(manager, 0)` and sets `0215FD46`;
`charcachedisposeall` calls both with −1, which clears the whole holder word of every live entry and
the manager's group word in every idle lane record.

`0037B4D0`, the party member rebuild, is the fifth caller of the bind. The resolver `002E97C0` has
20 call sites in 11 functions; the bind `002E28E0` has five callers: `003409F0`, `00342640`,
`00355210`, `0050D810` and `0037B4D0`.

## Layouts

```
binding entry   0215FDA0 + slot*0x40, 128 slots
  +0x00 prev, +0x08 next (free / requested / live / retired list)
  +0x10 u32 load handle (0036B160), +0x14 u32 bound id
  +0x18 u8 state: bit1 ready, bit2 release pending, bit3 not registered with the render system
  +0x19 u8 pins: bits0-1 keep at count 0, bit2 no load buffer, bit3 created with a holder, bit4 kept by 002E3E90
  +0x1A u16 own slot, +0x1C s16 reference count, +0x1E s16 lane record index (-1 none)
  +0x20 u16 holder bits (one per manager), +0x24 u32 stamp (+0x26 always 0)
  +0x28 u32 claimed lanes, +0x2C u32 lanes with a positive size
  +0x30, +0x34, +0x38 u32 sub-resources (-1 none)
lane record     02161DA0 + i*0x120, 32 records
  +0x00/+0x08 links (free 0215FD70, idle 0215FD68, pending 0215FD80)
  +0x10/+0x18 unload-queue node (0215FD90)
  +0x20 u16 own index, +0x22 u16 owner slot
  +0x24 loaded, +0x28 to load, +0x2C queued for unload, +0x34 loading
  +0x38 hold mask, +0x3C tested with +0x38, +0x40 mask read by 002E9C60, +0x44 keep on load
  +0x48..+0x5B five group words, +0x5C u32 owner's stamp
  +0x60 u32[32] lane handles, +0xE0 s16[32] lane counts
chest record    +0x00 u8 index in the field, +0x04 s16 x tenths, +0x06 s16 z tenths, +0x08 u8 facing (bits 0-5) and random gil (bit 6),
                +0x09 u8 opened-flag id, +0x0A u8 presence %, +0x0B..+0x17 contents (reward verbs)
presentation    [actor+0xC0]: +0x00 render index, +0x04 bound id, +0x08 entry, +0x10 flags
  +0x12 s8 motion lane, +0x14C, +0x14D variant bytes b and c; attach slots +0x30, +0x60, +0x90, +0xC0, +0xF0 (0x30 each)
```

`002ED6F0`, letter class → resource kind, file index, lane count:

```python
'C' 0x43 -> 0x0F, n,      0      'b' 0x62 -> 0x16, n*2,    1      'n' 0x6E -> 0x13, n*0x19, 24
'M' 0x4D -> 0x12, n,      0      'c' 0x63 -> 0x0E, n*0x19, 24     's' 0x73 -> 0x17, n*0x19, 24
'N' 0x4E -> 0x14, n,      0      'g' 0x67 -> 0x0D, n*2,    1      't' 0x74 -> 0x19, n,      0
'S' 0x53 -> 0x18, n,      0      'm' 0x6D -> 0x22, n*0x0B, 10     'w' 0x77 -> 0x10, n,      0
other    -> 0x01, n,      1      (kind 1 adds 0x33 to the index)
```

## Shipped data

| Verb | Uses in the US scripts |
|---|---|
| `bindp2_d4` | 9,877 |
| `modelread` | 4,539 |
| `modelreadsync` | 4,531 |
| `stdmotionreadsync` | 1,989 |
| `setuptreasure` | 1,966 |
| `bindc` | 1,561 |
| `bindhoff` | 774 |
| `bindh` | 706 |
| `charcachedispose` | 289 |
| `puppetbind` | 285 |
| `puppetbind_41d` | 24 |
| `unkCall_5cb` | 1 |
| `bindp`, `puppetbind_41c`, `charcachedisposeall`, `debug_bindp` | 0 |

## Operations

Per frame: one pass of `002E65A0` (lane unload queue, retired releases, lane pump, request pump).
Per bind verb: one begin, one poll per frame until the entry is ready, one result.

## State

The 128 binding entries and 32 lane records, the list heads `0215FD58` to `0215FD98`, the flag
`0215FD46`, the loading flag `022C253D`, and each actor's presentation context.

## Modding notes

- A chest's placement is five bytes of its record: two signed tenths and a facing byte. Height is
  never authored, so a chest cannot be raised through its record.
- A map can bind at most 128 models at once, and the engine faults rather than refusing a 129th.
- A handle stops working the moment its entry is retired; a script that keeps one must re-resolve
  it, as `setuptreasure`'s and `puppetbind`'s polls do.
- `bindp` and `unkCall_5cb` differ only in the body replacement: a model listed in the replacement
  table gets its replacement body attached by `bindp` once the story-progress threshold is met.

## Related

- [Verb dispatch](verb-dispatch.md): how a verb's arguments arrive and how begin, poll and result run.
- [Verb table](verb-table.md): every verb id with its callbacks.
- [Reward verbs](reward-verbs.md): what opening a chest gives.
- [Script variables](script-variables.md): the reference decoder `002650B0`.
- [Movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md):
  the separation weight and mask the chest sets.
