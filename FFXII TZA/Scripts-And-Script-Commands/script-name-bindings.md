[Home](../../README.md) / [Scripts and script commands](README.md) / Script name bindings

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Script name bindings: how a script names a model by one number, the binding table with its lists and lanes, where a treasure chest is placed, and the bind verbs | system | Scripts and script commands | The script machine | How a zone script names a model: the bound id and its letter class, the stamped handle checked before every use, the binding table of 128 entries on four lists (free, requested, live, retired) with find-or-create, holder bits, reference count, pins and the deferred release, the per-frame update that loads and retires entries, the 32-lane record each binding can own, what setuptreasure does in order and how a chest's spot bytes become a position and facing, and what each bind verb attaches to an actor. | 0x002E97C0, 0x002E9810, 0x0215FDA0, 0x02161DA0, 0x002EA320, 0x002E25E0, 0x002E9360, 0x002EB540, 0x002EAE20, 0x002E99C0, 0x002E4C20, 0x002E3E20, 0x002E3DC0, 0x002E3E90, 0x002EAF70, 0x002EB810, 0x002EBD60, 0x002EAEB0, 0x002E65A0, 0x002E6D60, 0x002E6700, 0x002EAD50, 0x002E4D20, 0x002EA6E0, 0x002E60F0, 0x002ED6F0, 0x002ED950, 0x002E9A60, 0x002EB7A0, 0x0032E400, 0x002E2660, 0x002EB5E0, 0x002EB9D0, 0x002E9920, 0x002EB690, 0x002EAFA0, 0x002EB890, 0x002E3F00, 0x002E4000, 0x002E6880, 0x002E6EB0, 0x002E4E50, 0x002E6900, 0x002E9470, 0x002ECAB0, 0x002ECA30, 0x002ECBA0, 0x00354400, 0x00354A40, 0x00355210, 0x002FAED0, 0x002FAF60, 0x0026E060, 0x002650B0, 0x0026A320, 0x002E28E0, 0x002E3110, 0x002EBC90, 0x002E3C20, 0x0037CB90, 0x0033F330, 0x00340380, 0x003409F0, 0x00342640, 0x003418B0, 0x00344F00, 0x00345A60, 0x003460F0, 0x00343B00, 0x00344550, 0x00343A30, 0x00344200, 0x003463F0, 0x003EB190, 0x00340FA0, 0x003414A0, 0x00341840, 0x00340450, 0x00340EC0, 0x0034B8D0, 0x0050D810, 0x0037B4D0, 0x00267310, 0x00314D40, 0x008F8180, 0x008F6D54, 0x01CEBC78, 0x002ECFD0, 0x00347DD0, 0x002E9C30 |

## What the player sees

A treasure chest stands in a fixed spot facing a fixed way, and some chests are only there some of
the time. A story scene gives a character a different body, hands an actor a weapon or a prop, or
attaches a puppet; the scene pauses for a moment while the model loads. Every one of these is a zone
script naming a model by one number and asking the engine to bind it to an actor.

## How it works

### The bound id: what a script names

A script names a model with a 32-bit bound id: the bits under mask `0xFF0000` are a letter class and the bits under mask `0xFFFF` a
number. `0x002E9A60` turns a script's argument into a bound id. A value above `0xFFFFFF` is an index
into the script image's name table at `[context + 0x100]` (`0x00263F80`: a count, then one dword per
name; an index at or past the count gives 0, and a missing table gives the low 24 bits unchanged).
Smaller values go through `0x002EB7A0`, which turns 0 and 1 into `0x630000`, 8 and 9 into
`0x6E0001`, `0xC` and `0xD` into `0x770002`, and passes every other value through.

`0x002ED6F0` splits a bound id into a resource kind and a file index and returns the number of lanes
the model has (the table under Layouts). `0x002ED950` returns the model's row in a per-letter table for
the classes `b`, `c`, `g`, `m`, `n`, `s`, `t` and `w` (`[0x021641A8]` to `[0x021641E0]`, a count at `+8`
and 16-byte rows, row n at table + 16 × (n + 1), `0x002ED9C7`-`0x002ED9CF`); any other class, a class whose
table pointer is null¹, or a number at or past the count (compared signed, `0x002ED9C5`), gives null.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ED9C0` |

</details>

### The handle: one number checked before use

The table is 128 entries of `0x40` bytes at `0x0215FDA0`, followed by 32 lane records of `0x120` bytes
at `0x02161DA0`. A handle is `(dword [entry + 0x24] << 16) | word [entry + 0x1A] | 0x8000`
(`0x002E9810`, which returns 0 for a null entry). `+0x1A` is the entry's own slot and `+0x24` its stamp.

`0x002E97C0` resolves a handle: 0 fails; the slot is `handle & 0x7FFF` and must be below `0x80`; the
entry at `0x0215FDA0 + slot × 0x40` is returned only when its recomputed handle equals the argument,
and null otherwise. A handle with bit `0x8000` clear never matches. A stale handle names a live slot whose
stamp has moved on, so it resolves to null rather than to another model.

The stamp is a dword at `+0x24`. The allocator `0x002E25E0`, the re-lister `0x002EAEB0` and the release
`0x002E9360` each increment it and then zero the word at `+0x26`, so it counts in 16 bits and wraps from
`0xFFFF` to 0; the initialiser `0x002EA320` sets every stamp to 0.

### The four lists

Every entry is on exactly one doubly linked list through `+0x00` (previous) and `+0x08` (next):

- **free**, head `0x0215FD60`. `0x002EA320` links slots 0 to 127 in order with slot 0 at the head. The
  allocator pops the head; the release pushes on it.
- **requested**, head `0x0215FD78`. Find-or-create pushes a new entry here.
- **live**, head `0x0215FD58`. The request pump moves each requested entry here once its load is filed.
- **retired**, head `0x0215FD88`. The re-lister moves an entry here when its last holder lets go.

The loops in `0x002EA320` link the middle records and leave the end links to single stores: slot 0's next,
`0x0215FDA8`¹, and slot 127's previous, `0x02161D60`²; for the lane records, record 0's next
`0x02161DA8`³ and record 31's previous `0x02164080`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EA3CB` |
| ² | `0x002EA404` |
| ³ | `0x002EA425` |
| ⁴ | `0x002EA47D` |

</details>

The entry loop first zeroes both links
of every entry, so slot 0's previous and slot 127's next are null. The record loop links records 1 to 30 and gives
them null unload-queue nodes `+0x10`/`+0x18`¹; record 0's previous link, record 31's next
link and the nodes of records 0 and 31 are not written.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EA455`, `0x002EA45C` |

</details>

`0x002EA320` (called from `0x00266D10`) also clears the other heads (`0x0215FD88`, `0x0215FD78`, `0x0215FD90`, `0x0215FD80`,
then `0x0215FD58` and `0x0215FD68`) and the stored callback `0x0215FD98`¹, loads the ten character SE tables
through `0x002EA530` (`0x002EA34F`;
[character SE tables](../Game-Files-And-Data-Tables/character-se-tables-chse.md)), and fills the entries and
the lane records.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EA32C` |

</details>

Each entry gets its slot at `+0x1A`, a count `+0x1C` of 0, `+0x1E` = `0xFFFF` and a stamp of 0¹. Each lane record gets its index at `+0x20`, owner slot `+0x22` = `0xFFFF`, `+0x44` = 0
and its 32 counts at `+0xE0` zeroed². No other field of either is written.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EA361`-`0x002EA377` |
| ² | `0x002EA390`-`0x002EA3B6` |

</details>

It then registers the binding callbacks with `0x0041D6C0` (kinds 5, 4, 6, `0xC`, `0x26`): kind 5 gets the bare
`ret 0` stub `0x0016D6A0`, so a kind-5 call does nothing, and kinds 4, 6, `0xC` and `0x26` get `0x002E70C0`,
`0x002E7090`, `0x002E70A0` and `0x002E7080`¹. It installs the retire
step `0x002E6D60` as the allocation-pressure callback of memory arenas 6 and 10 (`0x0036C5A0`, arena
record `+0xA0`), and finally sets `0x0215FD46` to 1².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EA484`-`0x002EA4E2` |
| ² | `0x002EA50E` |

</details>

### Find-or-create, holders and the reference count

`0x002EB540(id, selector)` searches the live list, then the requested list, for an entry whose `+0x14`
equals the id. On a miss it allocates one, pushes it on the requested list and sets pin bit `0x8`
(`+0x19 |= 8`). Either way it sets bit `selector` of the holder word `+0x20`. `0x002EAE20(id)` does the
same search and creation without pin bit `0x8` and sets holder bit `0x1`. Neither guards its final writes
against a null allocation: with all 128 entries in use both write through a null pointer.

`0x002E99C0(id)` is that search alone: it returns the first entry on the live list, then on the requested list,
whose `+0x14` equals the id¹, and null when neither list holds one. It writes nothing.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E99D0`, `0x002E99F0` |

</details>

`0x002E25E0(id)` returns null at once when the free list is empty¹. Otherwise it pops the free
head, increments the stamp, keeps only bits `0xC8` of `+0x19`, zeroes
`+0x10`, `+0x18`, `+0x1C`, `+0x20`, `+0x26` and `+0x28..+0x2F`, stores the id at `+0x14`, sets
`+0x1E` to `0xFFFF` and `+0x30..+0x3B` to `0xFFFFFFFF`, and unlinks the entry, zeroing its links `+0x00`
and `+0x08`². It returns the entry.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E25EA` |
| ² | `0x002E2646`, `0x002E264A` |

</details>

The bind `0x002E28E0` and the attach `0x002E3110` add one to the reference count `+0x1C` and clear
`+0x18` bit `0x4`. `0x002EB810(id)` and `0x002EAF70(entry)` take one away. An entry with pin bit `0x1` or `0x2` set
(`+0x19 & 3`; `0x002EBD60(id, on)` sets or clears bit `0x1`) has its count clamped to 0 instead of being released.
`0x002EBD60` takes the first entry with the id on the live list, then on the requested list, and copies bit `0x1`
of `on` into pin bit `0x1`¹, so `on` = 0 clears it; with no entry for the id it stores
nothing².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EBDA4`-`0x002EBDAB` |
| ² | `0x002EBD9E`, `0x002EBDAE` |

</details>

`0x002EB810(id)` itself releases nothing. It takes one from the count of the entry with the id on the live or
requested list, `+0x1C -= 1`¹, and clamps a pinned entry at 0, `+0x1C <= 0` with `+0x19 & 3` giving
`+0x1C = 0`²; an unpinned entry stays listed with its count at 0 or below until one of the
routines below releases it. With no entry for the id it does nothing.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EB854` |
| ² | `0x002EB858`-`0x002EB867` |

</details>

Four routines release an unreferenced entry through the re-lister `0x002EAEB0`:

- `0x002E3E20(selector, direction)` walks the live list only. A positive direction clears the
  selector's holder bit, a negative one clears the whole holder word. On an entry whose count is 0 or
  less it then clears the selector's bit (for any direction), and re-lists it when the holder word is
  empty and pin bits `0x3` are clear.
- `0x002E3DC0(id)` searches the live list, then the requested list, and re-lists the entry for the id (a tail
  jump to `0x002EAEB0`, `0x002E3E14`) when its count is 0 or less and it is not pinned. A pinned entry at 0 or less
  has its count set to 0¹; a positive count, or no entry with the id, leaves everything as it was.
- `0x002E3E90(id)` does the same, except that it leaves an entry with `+0x19` bit `0x10` set.
- `0x002EAF70(entry)` drops one reference and re-lists at 0 or less, unless pinned.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E3E1B` |

</details>

`0x002EAEB0(entry)`: while the entry is not ready (`+0x18` bit `0x2` clear) and `+0x19` bit `0x4` is clear, it
only sets `+0x18` bit `0x4` and returns, deferring the release until the load completes. Otherwise it
increments the stamp, clears the ready bit, copies the new stamp into the entry's lane record, and
moves the entry from the live or requested list to the head of the retired list. Every handle given
out for the entry stops resolving at that moment.

The lane record is the one `+0x1E` names. The re-lister copies the stamp only when `+0x1E` is not negative
and that record's stamp `+0x5C` equals the entry's old stamp¹. When the
entry heads the live or the requested list, that head moves to the entry's next².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EAED8`-`0x002EAEF4`, `0x002EAF10` |
| ² | `0x002EAF14`-`0x002EAF33` |

</details>

### The per-frame binding update

`0x002E65A0` runs the whole cycle. Its callers are `0x002628B0` and `0x0022A770`, `0x0022AF50`, `0x0022B000`,
`0x0022B6E0`, `0x0022B7E0`, `0x0022B8C0` and `0x0022BC20`.

In order it calls `0x003DC4A0`; runs the whole lane
unload queue (`0x002E6900(1)`); releases the retired entries; runs the unload queue again; compacts
memory arenas 6 and 10¹ when the retired list was not empty; clears `0x0215FD46`; runs the lane pump `0x002E6880` and the request
pump `0x002E6700`; calls `0x003DD4C0`, compacts arenas 6 and 10 again, calls `0x0037B2F0`; and finally calls,
once, the callback that `0x002EACC0` stored at `0x0215FD98` with the value at `0x021641F0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00369C60` |

</details>

Retired entries are released from the tail of the list (the oldest) towards the head. An entry whose
load handle `+0x10` is non-zero is first unloaded from the render system (`0x0041E490` through
`0x0020E600([0x022C6F28 + 0x48830])`) unless `+0x18` bit `0x8` or `+0x19` bit `0x4` is set, then released by
`0x002E9360`.

An entry whose `+0x10` is 0 is not passed to `0x002E9360` and stays linked. The walk nulls `0x0215FD88` only
when the entry it skips is the head¹, that is, when the update starts with a
zero-handle entry as the newest retired entry. That entry and every older zero-handle entry still linked
behind it then end up on no list, and their slots are lost until `0x002EA320` runs again.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E6649`-`0x002E6653` |

</details>

When the head has a non-zero handle, its release moves `0x0215FD88` to its next¹, so
after the walk the retired list holds exactly the zero-handle entries, newest at the head. They stay there
while newer retired entries keep arriving, and the first update that starts with one of them at the head
drops them all. Such an entry comes from a load the request pump could not file.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E9419`-`0x002E941D` |

</details>

`0x002E6D60`, which arenas 6 and 10 call when an allocation in them fails, unloads
the oldest queued lane record (`0x002E6900(0)`; with a non-zero argument `0x002E6900` runs the whole
queue), then releases the single oldest retired entry the same way, and runs the queue once more
when there was no retired entry. While the oldest retired entry has `+0x10` = 0 and is not alone on the list,
`0x002E6D60` picks it on every call and makes no progress.

`0x002E6D60` returns 0 on every path¹. Its early return for a non-zero `0x002E6900(0)` result² is never taken, because `0x002E6900` returns 0 on every path³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E6E1E` |
| ² | `0x002E6D6D` |
| ³ | `0x002E6A70` |

</details>

`0x002E9360(entry)` returns at once for a null entry¹. It queues all 32 lanes of the entry's lane record for
unload (`0x002EAFA0`, unloaded later by `0x002E6900`) when `+0x1E` is not negative and that record's stamp `+0x5C` matches², releases the three sub-resources at `+0x30`, `+0x34`,
`+0x38` through `0x003A0F80`³, frees `+0x10` through `0x00369800` when non-zero and then zeroes it⁴, and calls `0x0017F040` with the id⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E9363` |
| ² | `0x002E9389`, `0x002E939D`-`0x002E93A4`, `0x002E93B0`-`0x002E93C2` |
| ³ | `0x002E93C4`-`0x002E93DF` |
| ⁴ | `0x002E93E1`-`0x002E93F7` |
| ⁵ | `0x002E93FD` |

</details>

It then unlinks the entry from its neighbours and moves the free or the retired head past it when that head is the
entry (each compared in its low 32 bits; it leaves the live and requested heads alone; `0x002E9402`-`0x002E9438`), pushes
it on the free list¹, increments the stamp, zeroes `+0x26`, `+0x18` and the id
`+0x14`². It does not reset `+0x1E`; the next allocation does.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E943C`-`0x002E9448`, `0x002E945E` |
| ² | `0x002E944B`-`0x002E9456` |

</details>

### Loading an entry

The request pump `0x002E6700` takes every entry on the requested list. For each it pushes arena 6
(`0x0036C1D0(6, 5)`, `0x002E673F`) and tag 5 (`0x0036C1A0(5)`, `0x002E6749`). It splits the id with
`0x002ED6F0` (adding `0x33` to the index for kind 1), asks `0x0032E400(kind, index)` for the file's
size: `0x002DF960`'s size rounded up to a multiple of 64 when it is positive¹. It then
sets `+0x19` bit `0x4` and zeroes `+0x10`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0032E43B`-`0x0032E448` |

</details>

`0x0032E400` returns a size of 0 or less from `0x002DF960` as it is, and −1 for kind `0xFF` before any lookup¹. The per-kind override table at `0x022C51F0` it consults first (for a non-null
pointer and an index below `0x400` it returns that table's dword unrounded, `0x0032E41A`-`0x0032E428`) is only
ever zeroed, by `0x0032EA90`, among the static references to it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0032E404`, `0x0032E438` |

</details>

A positive size gets a buffer from `0x0036B160`, whose handle goes to `+0x10`; when
that succeeds it clears bit `0x4`, files the load with `0x002EAD50`, and for an entry with pin bit `0x8`
calls `0x0036C5D0(handle, 1)`. On every path it then pops the tag and the arena¹. The entry then moves to the live list and pin bit `0x8` is cleared.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036C110`, `0x0036C140`, `0x002E67BA` |

</details>

A size of 0 or less¹ or a failed buffer² files nothing: the entry still moves to
the live list, with `+0x10` = 0 and `+0x19` bit `0x4` set, so no completion runs for it and the re-lister
retires it on its first call. For a size of 0 or less the pump also finds the entry again by its id³, takes one from its reference count `+0x1C`⁴ and, when the count is then 0 or
less and pin bits `0x3` are set, sets it to 0⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E678B` |
| ² | `0x002E6799` |
| ³ | `0x002E6800` |
| ⁴ | `0x002E6835` |
| ⁵ | `0x002E6840`-`0x002E6846` |

</details>

The unlinking leaves the requested head `0x0215FD78` alone; after the last entry, or at once for an empty
list¹, the pump stores 0 there².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E6715` |
| ² | `0x002E686E` |

</details>

`0x0036C5D0(handle, 1)` puts the buffer in accounting group 1 ([resource
arena](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md)): when its header's group byte `+0x17` is
not already 1 it takes the header's size `+0x18` from that group's total, the dword at `0x022D8E10 + 4 × group`, and
adds it to group 1's¹²; it then sets `+0x17` to 1 and
zeroes the word `+0x3E`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x022D8E14` |
| ² | `0x0036C5F9`-`0x0036C610`, `0x0036C60C`, `0x0036C610` |
| ³ | `0x0036C616`, `0x0036C61A` |

</details>

It does nothing for a handle of 0, one with neither of its low two bits set, one below `0x100000`, or one whose header
`[(handle & ~3) + 8]` is null¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0036C5D3`-`0x0036C5F7` |

</details>

`0x002EAD50(entry, id)` takes the buffer's address from `0x0036A000(+0x10)`¹, which holds the
block in place, and calls `0x0017F000(id)`². It splits the id and sizes the file again³, then files `0x0032E620(kind, index, buffer, size, record)`⁴ with the
completion callback `0x002E4D20` and the entry as its argument. The record holds the entry's low 32 bits⁵, and `0x002E4D20` sign-extends its 32-bit argument⁶; the table at `0x0215FDA0` lies
below `0x80000000`, so that gives back the entry's address.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EAD65` |
| ² | `0x002EADB5` |
| ³ | `0x002EADCC`, `0x002EADEA` |
| ⁴ | `0x002EAE08` |
| ⁵ | `0x002EAD9A` |
| ⁶ | `0x002E4D3E` |

</details>

On completion `0x002E4D20` calls `0x0032F3D0(2)`¹ and does not use its result (`0x002E4D4E` zeroes `eax`
before any read of it; for kind 2 it is always 0, since `0x005C5230` returns 0), stores the id at `0x021641FC`²,
labels the loaded block (`0x0036B130`, then `0x0036C660` with the name `0x00409090` gives and the id,
`0x002E4D68`-`0x002E4D82`) and releases the hold with `0x0036D170(+0x10)`³. It then registers the
model with the render system⁴ unless a release is already pending (`+0x18` bit `0x4`), in
which case it sets `+0x18` bit `0x8`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E4D46` |
| ² | `0x002E4D5E` |
| ³ | `0x002E4D89` |
| ⁴ | `0x0041E580` |

</details>

It then asks `0x002EA6E0` whether sub-resources follow, passing three zero values for the slots¹: when no sub-resource follows, it sets the
ready bit `+0x18` bit `0x2` and, if a release was deferred, re-lists the entry at once.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E4DB9` |

</details>

`0x002EA6E0(entry, count, values)` files a task with step function `0x002E60F0` when the model has a row in
`0x002ED950` and no release is pending; otherwise it returns 0 at once¹. It takes
the task from `0x002F16B0`² and copies the values into `+0x30` onward³
before testing it. With all 32 tasks taken it returns 0 with the slots already written⁴;
otherwise it files the task with the entry at task `+0x28` and returns 1⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EA6FC`, `0x002EA709` |
| ² | `0x002EA70B` |
| ³ | `0x002EA720`-`0x002EA72F` |
| ⁴ | `0x002EA734` |
| ⁵ | `0x002EA736`-`0x002EA758` |

</details>

`0x002E60F0` reads the row's three signed words at `+0`, `+2`, `+4`, with no null test of
the row¹. A negative
word stores `0xFFFFFFFF` in its slot. Otherwise the word w becomes a class-`0x20` file index (0 → 0,
1 → 1, 2 → 3, below 500 → w − `0xC0`, otherwise w − `0x188`), whose size comes from `0x0032E400`; a size not
above 0 skips the slot and leaves it as it was².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E6157` |
| ² | `0x002E61B2` |

</details>

For a positive size the load goes into slot `+0x30`, `+0x34` or `+0x38`: a buffer from `0x0036B160` (between
`0x0036C1D0(6, 5)` and `0x0036C140`) is read with `0x0032E620`, and the slot holds the buffer handle while the task
waits, one step at a time, until `0x0032E4D0` answers 0¹. The task then calls `0x0036D200` on the handle². A handle of 0 stores `0xFFFFFFFF`³; any other is registered with `0x003A1650`, whose
block handle replaces it in the slot.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E6290` |
| ² | `0x002E61D6` |
| ³ | `0x002E622D` |

</details>

A failed registration (−1) moves on to the next slot; otherwise the task waits until `0x003A1290` answers 2¹. When all three are done it sets the ready bit
and re-lists the entry if a release was deferred². Its step state is then 9, which
every later step leaves as it is³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E61FE` |
| ² | `0x002E629E`-`0x002E62AB` |
| ³ | `0x002E62C9` |

</details>

`0x003A1290(handle)` answers the byte `+0x0C` of the `0x02AEEDC0` record at the handle's low 16 bits when that record's
handle, `+0x0A` over `+0x08`, equals the handle without bit `0x80000000`, and 0 otherwise (`0x003A129C`-`0x003A12CD`;
[sound banks](../Sound-And-Music/sound-banks.md)). For −1 it reads those fields through a null record pointer instead¹, a value the task above never passes.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A1295`-`0x003A129A` |

</details>

`0x002E4C20(entry)` is the ready test every wait uses: `+0x18 & 2`, and 0 for a null entry.

### Lanes: the 32 extra files of a binding

A model can own up to 32 extra files (lanes); the lane count comes from `0x002ED6F0`. With i the index
`0x002ED6F0` gives, lane n is file `i + 1 + n` of the same kind, or `i + 0x43 + n` for kind 1¹. For class `m` (`0x6D`) lane 0 is file `i + 1`, lanes 1 to 15 are all file `i + 2`,
and lane 16 and above are file `i + 1 + n − 14`. `0x002E9920(id, n)` returns `0x0032E400`'s size for that
file (a tail jump, `0x002E9988`, `0x002E99A8`), and 0 for a model whose lane count is below 1²; it does
not bound n by the lane count.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E9920` |
| ² | `0x002E9957` |

</details>

The lane records are 32 × `0x120` bytes at `0x02161DA0` on their own lists: free `0x0215FD70`, idle
`0x0215FD68`, pending `0x0215FD80`, and the unload queue `0x0215FD90` (linked through the second node at
`+0x10`/`+0x18`). `0x002E2660(entry)` pops a free record, zeroes the masks `+0x24` to `+0x43`, the five group
words `+0x48..+0x5B`, the 32 handles at `+0x60`, the 32 counts at `+0xE0` and both list links, and
cross-links it: record `+0x22` = the entry's slot, entry `+0x1E` = the record's index `+0x20`,
record `+0x5C` = the entry's stamp. Every lane access checks `+0x5C` against the entry's stamp first.

`0x002E2660` leaves the mask `+0x44`, the unload-queue node `+0x10`/`+0x18` and the new free head's previous link
as they were (`0x002E9470` zeroes `+0x44` when it frees a record). With the free list empty it returns null and
writes nothing¹; otherwise it returns the record.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E266D` |

</details>

`0x002E9C30(entry)` returns the entry's lane record when the entry has one and its stamp matches,
null otherwise; the model loader `0x002EE430` uses it.

`0x002EB5E0(entry, lane, delta, group)` picks the lane with `0x002EB9D0`, creates the lane record if the
entry has no lane record, and requests lane 0 and the chosen lane through `0x002EB690`. It returns the lane
record. It returns 0 and requests nothing for a null entry, when `0x002EB9D0` gives −1, when no free record is
left (`0x002E2660` returns null, `0x002EB623`), or when `+0x1E` names a record whose stamp no longer matches: that
stale index gets no new record¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EB611`, `0x002EB647` |

</details>

`0x002EB9D0(entry, n)` returns −1 for a null entry¹. Otherwise it
sets lane n in the entry's `+0x28`; when the lane's file has a positive size² it also
sets `+0x2C` and returns n, otherwise −1, with the lane left in `+0x28`³. A lane already in
`+0x28` gives n only when it is in `+0x2C`. A negative n tries lanes from 1 upwards below the lane count
(at most 32) the same way: the count comes from `0x002ED6F0`⁴, the first lane that qualifies is
returned, and a count of 1 or less, or a walk in which no lane qualifies, gives −1⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EB9E1` |
| ² | `0x002E9920` |
| ³ | `0x002EBA09` |
| ⁴ | `0x002EBA4C` |
| ⁵ | `0x002EBAB9` |

</details>

`0x002EB690(record, lane, delta, group)` adds delta to the lane's count `+0xE0 + lane × 2`, clears the
lane's bit in `+0x2C`, sets it in group word `+0x48 + group × 4`, and, when the lane is in none of
`+0x24`, `+0x28`, `+0x34`, sets it in `+0x28` and moves the record to the pending list. The lane pump
`0x002E6880` runs `0x002E6EB0` on every pending record and moves it to the idle list.

`0x002E6EB0` loads each lane in `+0x28` whose handle `+0x60 + lane × 4` is still 0: a buffer from
`0x0036B160`, `0x0036C5D0(handle, 1)` when the lane is in `+0x44`, and `0x0032E620` with completion
callback `0x002E4E50` and tag `record index << 16 | lane`. It clears the lane from `+0x28` and, when the
load was filed, from `+0x44` and into `+0x34`. Each lane with a zero handle is handled between
`0x0036C1D0(6, 5)` with `0x0036C1A0(5)` and `0x0036C140` with `0x0036C110`.

A lane in `+0x28` whose handle is already non-zero files nothing: it moves from `+0x28` into `+0x34` and keeps
its `+0x44` bit¹. A lane whose size from `0x002E9920` is not above 0, or whose buffer is 0, only
leaves `+0x28`². The owner is the entry in slot `+0x22` when its stamp equals `+0x5C`;
its id is read with no null test³, so with a negative owner slot or a stale stamp the read is at
address `0x14` and faults.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E6EF6` |
| ² | `0x002E6F45`, `0x002E6F57` |
| ³ | `0x002E6F35` |

</details>

`0x002E4E50` moves the lane from `+0x34` to `+0x24`¹. For an owner that no longer resolves
(owner slot negative or stamp different) it queues the lane for unload instead². With a
resolving owner and a non-zero handle it calls `0x0036B130(handle)`, whose result it does not use, and
`0x0036D170(handle)`, registers the handle with `0x0041E580` on `0x0020E600([0x022C6F28 + 0x48830])`, and drops one count³ when the lane was queued for unload meanwhile (`+0x2C`). A zero handle registers nothing.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E4EBE`, `0x002E4EC5` |
| ² | `0x002EAFA0`, `0x002E4F15` |
| ³ | `0x002EB890` |

</details>

`0x002EB890(id, lane)` takes one from the lane's count, `[+0xE0 + 2 * lane] -= 1`¹. At 0 or less,
`[+0xE0 + 2 * lane] <= 0`², a held lane (`+0x38`/`+0x3C`, `bt` at `0x002EB913`) is clamped to 0³ and any other keeps its count; it queues nothing. A negative lane, an id on neither
list, or an entry whose lane record is missing or stale leaves everything as it was.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EB8FC` |
| ² | `0x002EB903` |
| ³ | `0x002EB91B` |

</details>

A lane is held while its count is positive, while it is in any of the five group words
`+0x48..+0x5B`, or while it is in the hold mask `+0x38` (the readers `0x002E3F00`, `0x002E4000` and
`0x002EB890` also test `+0x3C`, which only the qword store of 0 at `0x002E26C9` in `0x002E2660` writes, so it is
always 0).

`0x002ECAB0(id, lane, on)`
sets or clears the lane in `+0x38`, and `0x002ECA30(entry, lane, on)` does the same in `+0x40`, a mask
only `0x002E9C60` reads and `0x002E6570` clears in all 32 records. `0x002ECAB0` takes the first entry with the id
on the live list, then on the requested list, and stores nothing when neither holds one¹; `0x002ECA30` stores nothing for a null entry².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ECADA`, `0x002ECAEE` |
| ² | `0x002ECA36` |

</details>

Both then store nothing when the entry has no lane record (`+0x1E` negative), when the record's stamp
`+0x5C` differs from the entry's, or for a negative lane¹.
Both act only on a lane already in
`+0x24`, `+0x28` or `+0x34`², so a hold set before the lane is requested is dropped;
with lane 0 present, lane 0 follows the other bits (set while any other bit is set, otherwise the whole mask
is cleared).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ECA3F`-`0x002ECA5E`, `0x002ECAFB`-`0x002ECB1A` |
| ² | `0x002ECA78`, `0x002ECB35` |

</details>

`0x002ECBA0(entry, lane, x)` sets the lane and lane 0 in `+0x44` when its third argument is 1¹, with no test that the lane is present. It stores nothing for a negative lane, an entry
without a lane record or a stamp mismatch². It does not test the entry for
null: after the lane test it reads `[entry + 0x1E]`³, so a null entry with a lane of 0 or more
faults.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ECBC8`-`0x002ECBD4` |
| ² | `0x002ECBA2`, `0x002ECBAB`, `0x002ECBC6` |
| ³ | `0x002ECBA4` |

</details>

`0x002EAFA0(record, lane)` queues a lane for unload: when the lane is not already in `+0x2C` and is in
`+0x24`, `+0x28` or `+0x34`, it sets `+0x2C`, and a loaded lane (`+0x24`) puts the record on the
unload queue, at its head: a record already queued is taken out and pushed again¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EAFDD`-`0x002EB01F` |

</details>

`0x002E6900` starts at the queue's tail, the record queued longest ago, and works towards the head¹; with argument 0 it stops after the tail record. It unloads each queued lane that is loaded and
whose handle `+0x60 + lane × 4` is non-zero² (`0x0041E490`, then `0x00369800`), zeroes the handle,
clears it from `+0x24` and `+0x2C`, takes the record off the queue, and returns it to the free list³ once neither `+0x28` nor `+0x24` has a lane left.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E6942`, `0x002E69F7` |
| ² | `0x002E696F` |
| ³ | `0x002E9470` |

</details>

A queued lane that is not loaded keeps its `+0x2C`
bit while the record leaves the queue. The function returns 0.

After that pass, every record still
queued whose owner slot `+0x22` is negative goes to `0x002E6A80`¹, even for `0x002E6900(0)`:
it unloads each queued, loaded lane², takes the record off the queue and frees it under
the same test. When that record is the queue's head, the head `0x0215FD90` is set to 0³ and
`0x002E6A80` relinks nothing, so the queue's other records are no longer reachable from the head.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E6A4E` |
| ² | `0x002E6E30` |
| ³ | `0x002E6A5A`-`0x002E6A61` |

</details>

`0x002E9470` resets the owner's `+0x1E` to `0xFFFF` when the owner slot `+0x22` is not negative¹
and the stamps still match². It also sets the record's owner slot `+0x22` to `0xFFFF`
and `+0x44` to 0, takes the record
off the unload queue, moves the idle, pending and free heads past it, unlinks it and pushes it on the free list
`0x0215FD70`³. A null record leaves everything as it was.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E9484` |
| ² | `0x002E9497`-`0x002E949F` |
| ³ | `0x002E94A7`-`0x002E954A` |

</details>

`0x002E3F00(id, lane)` finds the entry on the live list, then the requested list, and queues the lane¹, and then lane 0, when its count is 0 or less and it is not in
`+0x38`/`+0x3C`; a held lane has its count clamped to 0². A negative lane³, an
id on neither list, or an entry without a lane record whose stamp matches leaves everything as it was. It does
not bound the lane: a lane of 32 or more reads its count past the 32 counts and tests hold bit `lane & 31`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EAFA0` |
| ² | `0x002E3FA4`, `0x002E3FED` |
| ³ | `0x002E3F4F` |

</details>

`0x002E4000(group, direction)` walks the idle records¹ and handles their 32 lanes in turn. A
positive direction clears each lane's bit of the group word `+0x48 + group × 4` before that lane is tested², so it clears the whole group word as a negative direction does³; with direction 0
only a lane whose count is 0 or less loses its bit⁴. That clear comes before the lane's test in
every direction, so only the other four group words can keep the lane.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0215FD68` |
| ² | `0x002E405D` |
| ³ | `0x002E4064` |
| ⁴ | `0x002E4084` |

</details>

`0x002E4000` queues
every lane whose count is 0 or less and that no group word and no hold mask keeps: it sets `+0x2C` when the lane
is not there yet and is in `+0x24`, `+0x28` or `+0x34`, and a loaded lane moves the record to the head of the
unload queue¹. It does not bound
the group: a group of 5 or more indexes past `+0x58`, and a negative group indexes before `+0x48`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E40BA`-`0x002E410B` |

</details>

### setuptreasure: placing a chest

`setuptreasure` (verb `0x2BE`) has begin `0x00354400`, poll `0x00354A40` and result `0x00355210`.

The begin hides the actor (`0x0026A320(actor, 0)` clears `+0x0C` bit `0x80`), pops the spot reference into `args[2]`,
and takes the chest model from the current map header into `args[1]`¹: `0x0026E060` reads the word at
`+0x88` of the header `[0x02098E10]` when `0x02098E20` bit `0x1` is set, the header pointer is non-null², the
header's first word exceeds 10 and the signed word is not negative, with `[0x02099D70]` switched to `0x02098E10` for the
call and restored on every path before it returns³. Otherwise the model is −1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035443A` |
| ² | `0x0026E08E` |
| ³ | `0x0026E077`, `0x0026E0B7` |

</details>

Because `word | 0x3000000` is above `0xFFFFFF`, `0x002E9A60` takes the chest model from a name table at that index¹. The table is the one at `+0x100` of `0x02098E10`, the zone's actor manager 0, which `[0x02099D70]` points at
during the call, whichever script runs the verb: `0x002E9A60` reads it through `0x002640C0`², which returns
that switched `[0x02099D70]`. With no table there the model is the word itself, and an index at or
past the table's count gives 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00263F80` |
| ² | `0x002E9A70` |
| ³ | `0x00263F90`-`0x00263F9D` |

</details>

It then resolves the chest record with `0x002650B0` and rolls for the chest with `0x002FAED0`: no chest
when the opened flag `0x0032AA60(record[+9])` is set (bit `record[+9]` of the 256-bit set at `+0x14B4`
of `0x002EF2B0()`); otherwise a chest when `rand % 100 < record[+0xA]`, `rand` being the Mersenne Twister
thunk `0x00379CD0` ([which roll uses which generator](../Random-Numbers/which-roll-uses-which-generator.md)).

A flag byte of `0xFF` tests bit
255, while the payout `0x002FAFD0` never sets the flag for `0xFF`. Both outcomes of the roll are recorded with
`0x002FB430`. No chest sets the model to −1. A model of −1 leaves `args[0]` at 0; any other model is
found or created with `0x002EAE20` and its handle stored in `args[0]`.

The poll `0x00354A40` ends at once when `args[0]` is 0¹. Otherwise, a handle that no longer
resolves is re-created from the model id in `args[1]` with `0x002EAE20` and stored back, and that call
waits without raising the loading flag². After that the poll waits (raising the
loading flag `0x022C253D` through `0x00314D40(1)`, `0x00354AA1`) until the entry is ready, and a ready entry
ends it³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00354A5F` |
| ² | `0x00354A72`-`0x00354A81` |
| ³ | `0x00354A9D` |

</details>

The result resolves `args[0]`; when that fails it returns with the actor still hidden. On that path
it first calls `0x0026E060`, the map-header chest-model read of the begin, and drops the value it
returns¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00355242`, `0x003552DE` |

</details>

With a resolved entry it
resolves the chest record again, shows the actor (`0x0026A320(actor, 1)`), decodes the spot with `0x002FAF60`,
places the actor at the position¹, sets its facing and its movement heading to the same
angle², sets its separation weight to −1.0³, binds the model⁴ and sets the movement body's mask word to `0x10`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026AF80` |
| ² | `0x0026B620`, `0x0026A0D0` |
| ³ | `0x0026DAC0` |
| ⁴ | `0x002E28E0` |
| ⁵ | `0x002EC5B0` |

</details>

`0x002FAF60` decodes the placement from the chest record, and `setuptreasure`'s result is its only
caller. Byte `+8` is shared: bits `0x3F` are the facing and bit `0x40` is the random-gil flag the payout
reads ([reward verbs](reward-verbs.md) has the contents fields `+0xB..+0x17`).

```python
x = (int16) record[+0x04] / 10.0            0x008F8180 = 10.0
y = 0.0
z = (int16) record[+0x06] / 10.0
w = 1.0
heading = -(record[+0x08] & 0x3F) / 60.0 * 2*pi   0x008F6D54 = 60.0, 0x01CEBC78 = 6.2831855
```

The position is in tenths of a unit, the height is never authored, and the facing steps in 6°
units; codes 60 to 63 go past a full turn and are not clamped.

`0x002FAF60(record, out, heading)` writes x, y, z and w to `out + 0`, `+4`, `+8` and `+0xC` and the heading to
`heading`, and returns 1¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FAF73`, `0x002FAF7B`, `0x002FAF98`, `0x002FAF82`, `0x002FAFC2`, `0x002FAFAA` |

</details>

### The bind: what binding a model to an actor does

`0x002E28E0(actor, entry)` first calls `0x00263FF0` with the actor's byte `+0x15`, which gives the actor's manager record
(`0x02098E10 + byte × 0x288`) used below¹. It needs the actor's presentation context
`[actor + 0xC0]`; without one it only runs its tail, `0x002EB930(actor)`².
With one, it calls `0x0025AB30(actor)` and `0x0025D480(actor)`, marks the actor (`+0x0D` bit `0x2`, `+0x04` = 1), takes a
reference on the entry and clears its pending-release bit³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E290D`-`0x002E2915` |
| ² | `0x002E2920`-`0x002E2923`, `0x002E3054`-`0x002E3086` |
| ³ | `0x002E2959`-`0x002E2979` |

</details>

It creates the render record with `0x0042FB80(entry +0x10, context +0x14C, context +0x14D)`, the two bytes signed, while
`0x01F7F508` holds the entry's id¹, and stores the record's index at context `+0x00`²; the id goes to `+0x04` and the entry pointer to `+0x08` later³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E297D`-`0x002E299D` |
| ² | `0x002E29A8`-`0x002E29AC` |
| ³ | `0x002E2AF7`-`0x002E2B00` |

</details>

Render records are `0x740` bytes from `[0x022C6F28]`; each step below on the record runs only when the context's word
`+0x00` is not −1 and the record it selects is not null and in use (dword `+0x284` non-zero)¹. The bind copies context byte `+0x10 >> 4` to render `+0xC1`², stores
the actor at render `+0x108`³, calls `0x003E5E20(render, [actor + 0x30])`⁴
and copies context `+0x14F >> 3` to render `+0x413`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E29B9`-`0x002E29E7` |
| ² | `0x002E29A4`-`0x002E29E9` |
| ³ | `0x002E29EF`-`0x002E2A15` |
| ⁴ | `0x002E2A1C`-`0x002E2A46` |
| ⁵ | `0x002E2A4B`-`0x002E2A8C` |

</details>

It then calls `0x002EA2A0(actor)`¹ and copies context `+0x150` to render `+0x40C`². For an actor with `[actor + 0x30]`³, it passes
`0x0031B750([actor + 0x30])` as the slot and the record's index from context `+0x00` as the index to the slot set-up
with `0x003E7500`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E2A92`-`0x002E2A95` |
| ² | `0x002E2A9A`-`0x002E2AD8` |
| ³ | `0x002E2ADF`-`0x002E2AF2` |

</details>

`0x003E7500(slot, index)` sets up presentation record `0x02B59D80 + slot × 0x150` ([character status
visuals](../Graphics/character-status-visuals.md)): word `+0` = 1, dword `+4` = the render index,
dword `+8` = 0¹. It stores the slot in the render record's `+0x6A4`², zeroes `0x80`
bytes at the presentation record's `+0xC0`³ and sets up the presentation record's blocks at `+0x20` and
`+0x70` with the index⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003E7527`-`0x003E7530` |
| ² | `0x003E755A` |
| ³ | `0x003E7570` |
| ⁴ | `0x003E7561`, `0x003E7575`, `0x003E7580`, `0x003E757B`, `0x003E7590` |

</details>

For an index of −1, or a render record whose `+0x284` is 0, the `+0x6A4` store goes through a null pointer instead¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003E7534`-`0x003E7557`, `0x003E755A` |

</details>

Next the bind takes a float, `0x00423280(render)` for a record in use and otherwise 30.0¹, clears bit `0x40000` of render `+0x284`² and, for an actor of kind
`0x60` (`+3 & 0xE0`), sets the three floats at `[+0xB8] + 0x20..0x28` to 1.0 and calls `0x002E8E20`³. It then calls `0x00427300(render, float)` and `0x00426E20(render)`⁴,
`0x002E8FD0(actor)` and `0x002E3500(actor)`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008F8D80`; `0x002E2B04`-`0x002E2B4A` |
| ² | `0x002E2B4D`-`0x002E2B89` |
| ³ | `0x002E2B8F`-`0x002E2BB8` |
| ⁴ | `0x002E2BBD`-`0x002E2C11` |
| ⁵ | `0x002E2C16`-`0x002E2C21` |

</details>

With bit `0x1` of the actor's byte `+0x09` cleared for the two calls and then put back, it calls
`0x002E5C90(actor, x, y, z, 1)` with the three floats at `[actor + 0xB8] + 0x00` and `0x002E5E10(actor, +0xA8, +0xAC, 1)`
from the same block¹, zeroes the block's byte `+0xDC` and calls `0x00269F90(block)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E2C26`-`0x002E2C7C` |
| ² | `0x002E2C7F`-`0x002E2C86` |

</details>

It reads keyed parameters of the model with `0x003E6150(render index, key)`, 0.0 with no context or when its dword
`+0x00` is −1: `0x09000606` to `[actor + 0xB8] + 0xE0`¹, and `0x09000707` times the speed
scale `[0x01DFE0BC]` (1.0, or 0.5 at 60 fps; [startup constants](../Engine-Core/startup-constants.md)) to
`+0xE4`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E2C8B`-`0x002E2CB3` |
| ² | `0x002E2CBB`-`0x002E2CEE` |

</details>

It then calls `0x00263640(actor)`¹, and `0x003E6BF0(render, a, a)` with a = 1.5707964 (π/2, `0x008C5F70`) and
`0x003E6BE0(render, b, b)` with b = 1.4959966², each followed by setting bit `0x800` of render `+0x290`³. Then come `0x002E7CE0(actor, 1)` and `0x002E92F0(actor)`⁴, `0x002EC6B0(actor, context +0x12)`, the byte signed and −1 with no context⁵, and `0x00426FA0(render)`⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E2CF6` |
| ² | `0x00D0F8E8` |
| ³ | `0x002E2CFB`-`0x002E2D45`, `0x002E2D4F`-`0x002E2D99` |
| ⁴ | `0x002E2DA3`-`0x002E2DB3` |
| ⁵ | `0x002E2DB8`-`0x002E2DD0` |
| ⁶ | `0x002E2DD5`-`0x002E2E0C` |

</details>

Then it clears bit `0x1` of the actor's byte `+0x0D`, sets its `+0xF5` = `0xFF`, `+0xEC` = 0 and `+0xF0` = `0x1001`¹, calls `0x002EB0D0` unless `+0x18` is 1², and calls
`0x002652D0(manager, actor, 2)`, which only looks up the function of entry slot 2 ([script
requests](script-requests.md)); the bind does not use its result³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E2E11`-`0x002E2E27` |
| ² | `0x002E2E15`, `0x002E2E31`-`0x002E2E57` |
| ³ | `0x002E2E5C`-`0x002E2E68` |

</details>

After that call it reads `0x09001F20` and `0x09002021` for `0x0026AA30`¹;
`0x01002D4F`/`0x01002E50` in a town (`0x00377C20`: bit `0x8000` of the map's word in `[0x02ADD100]`), otherwise
`0x01002143`/`0x01002244`, for `0x0026B2E0`²; `0x09001D1E` for `0x00269E60`³; and `0x600A1244` (integer, `0x003E6310`) for `0x0026AF40` as 1 or 0⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E2E6D`-`0x002E2E8D`, `0x002E2F4C` |
| ² | `0x002E2E91`-`0x002E2ED1`, `0x002E2F95` |
| ³ | `0x002E2ED1`-`0x002E2EE2`, `0x002E2F57` |
| ⁴ | `0x002E2EEA`-`0x002E2EFF`, `0x002E2F78`-`0x002E2F85` |

</details>

`0x09002322`, `0x09002524` and `0x09002423`, each × 50¹ and truncated (`cvttss2si`), go to `0x0026A370` in
that order². `0x09042A2E` is read and its value never used³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008F3130` |
| ² | `0x002E2EF7`-`0x002E2F48`, `0x002E2F9A`-`0x002E2FA5` |
| ³ | `0x002E2EDA`-`0x002E2EE5` |

</details>

`0x0026A370(actor, a, b, c)` does nothing unless the actor is of kind `0x60` (`+3 & 0xE0`); for that kind it stores the
three bytes at `[actor + 0xB8] + 0x104`, `+0x105` and `+0x106` and jumps to `0x00268380`¹, which,
when the presentation context `+0xC0` and its `+0x138` record are not null², passes the three
bytes on to `0x003DAF20(that record, a, b, c)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026A370`-`0x0026A395` |
| ² | `0x002683AD`-`0x002683C7` |
| ³ | `0x00268481`-`0x002684FD` |

</details>

Last the bind calls `0x003E6BC0(render, 0)` and sets bit `0x800` of render `+0x290`¹, clears bit
`0x4` of the actor's byte `+0x08` and calls `0x002E7C70(actor, 0x30B)`² and, for an actor of kind
`0x60`, zeroes the dwords `+0xB4` and `+0x224` of `[actor + 0xB8]` and the byte `+0x63` of `[[actor + 0xB8] + 0xF0]`
and calls `0x002EC3F0(actor)` and `0x002E8EE0(actor)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E2FAA`-`0x002E2FFF` |
| ² | `0x002E3009`-`0x002E3015` |
| ³ | `0x002E301A`-`0x002E304F` |

</details>

The tail calls `0x002EB930(actor)`; then, when the actor has a context whose dword `+0x00` is not −1, it calls
`0x00427280(render)` for a record in use and zeroes the actor's dword `+0xEC`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E3054`-`0x002E30B8` |

</details>

The bind's call, `0x002EB0D0(actor, context, event, flag, f)`, does not read its first argument¹. It returns
at once for a null context or one whose dword `+0x00` is −1 ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md);
`0x002EB0D0`-`0x002EB0F4`). Otherwise it calls `0x00269D60(context, 0, 0)`² and, when bit `0x10` of
the context's byte `+0x11` is set, `0x002EDCC0(word +0x00, 1)`, and clears that bit³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EB104` |
| ² | `0x002EB0FA`-`0x002EB107` |
| ³ | `0x002EB10C`-`0x002EB125` |

</details>

Each step below that uses the render record runs only when the context's word `+0x00` is not −1 and selects a record
of `[0x022C6F28]` that is not null and is in use (dword `+0x284` non-zero)¹. The first hands the event to `0x00427320(record, event)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EB144`-`0x002EB147`, `0x002EB1A0`-`0x002EB1A3`, `0x002EB1DF`-`0x002EB1E2`, `0x002EB209`-`0x002EB20C`, `0x002EB258`-`0x002EB25F`, `0x002EB28D`-`0x002EB294`, `0x002EB2B7`-`0x002EB2BE`, `0x002EB2E7`-`0x002EB2EE` |
| ² | `0x002EB129`-`0x002EB154` |

</details>

The context's float `+0x14` of 0.0 becomes −1.0¹. With a negative context word `+0x2A` the
record gets `0x00427880(record, +0x14, +0x18, +0x1C)`; otherwise it gets `0x004278B0(record, word +0x2A)` for a negative
`+0x14` and `0x004272C0(record, +0x14, word +0x2A)` for any other². Then `+0x14`, `+0x18` and
`+0x1C` are set to −1.0 and word `+0x2A` to −1³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EB160`-`0x002EB16F` |
| ² | `0x002EB17D`-`0x002EB21B` |
| ³ | `0x002EB220`-`0x002EB238` |

</details>

With `flag` non-zero it calls `0x00427860(record)`¹; otherwise `0x004270A0(record, f)` for an `f`
of 0 or more and `0x004272E0(record)` for any other². Last it calls
`0x004272A0(record, bit 0x8 of byte +0x11)`³ and, when that bit is set, `0x00314D30(1)`, and clears
it⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EB23F`-`0x002EB26A` |
| ² | `0x002EB271`-`0x002EB2C9` |
| ³ | `0x002EB2CE`-`0x002EB303` |
| ⁴ | `0x002EB308`-`0x002EB318` |

</details>

So the bind, which passes `0x1001`, flag 1 and −1.0 from `0x01CEBC9C`¹, and `0x002EB030` ([HP and
KO](../Damage-And-Battle-Formulas/hp-and-ko.md)), which passes flag 1, reach `0x00427860`, and `0x002EB330`, which passes flag 0,
`0x004272E0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E2E33`-`0x002E2E57` |

</details>

### The attach slots

The presentation context carries the main binding at `+0x00` and attach slots of `0x30` bytes:
`+0x30`, `+0x60`, `+0x90` and two at `+0xC0` and `+0xF0`. Each slot holds a render index, the bound
id, the entry pointer and a flags byte at `+0x10`.

`0x002EBC90(actor, which, on)` sets the high
nibble of a slot's flags byte to the low four bits of `on` and keeps its low nibble¹
(`which` 0 the context itself, 1 `+0x60`, 2 `+0x30`, 3 `+0x90`, 4 and
5 the two last slots; any other `which`, negative or above 5, also takes the context itself, `0x002EBCCF`).
It stores nothing for a null actor or an actor without a context².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EBD2D`-`0x002EBD35` |
| ² | `0x002EBCA7`-`0x002EBCBA`, `0x002EBD22` |

</details>

`0x002E3110(actor, kind, n, entry, link)` attaches an entry: kind 0 → `+0x30`, 1 → `+0x60`, 2 and 4 → `+0x90`, 3
→ `+0xC0 + n × 0x30` (n unbounded here)¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E315F`-`0x002E3181`, `0x002E318E`, `0x002E31F8`-`0x002E3207`, `0x002E3212`, `0x002E32D0`-`0x002E32D6` |

</details>

It returns without doing anything for a null actor, when the actor has no presentation context, when the context has
no main entry (`+0x08` = 0) or for any other kind, a negative one too¹, so `bindh`
and `bindc` attach nothing to an actor without a presentation context, nor to one never bound whose model has no
replacement row (for a replacement the shared poll first binds the model as the main model, `0x00340AC2`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E3113`-`0x002E3145`, `0x002E3181` |

</details>

Kinds 2 and 4 force link `0x7FFF`¹. On the main render record, when it is in use, kind 2
clears bit `0x40` of `+0x304`, zeroes the dword `+0x640` and sets bit `0x2000` of `+0x290`; kind 4 does the same but
sets bit `0x40`, and only while the byte `0x01FD49EC` is set².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E3195`, `0x002E3219` |
| ² | `0x002E3187`-`0x002E31F3`, `0x002E320F`-`0x002E3254` |

</details>

Kind 2 then calls `0x002EE0D0(main, 0)` and `0x002EDE70(main, 0)`, each when the context holds a main record (`+0x00` ≠
−1)¹, and, for an actor of kind `0x60` (`+3 & 0xE0`), zeroes the dwords `+0xB4` and `+0x224`
of `[actor + 0xB8]` and the byte `+0x63` of `[[actor + 0xB8] + 0xF0]` and calls `0x002EC3F0(actor)` and
`0x002E8EE0(actor)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E325E`-`0x002E328F` |
| ² | `0x002E3294`-`0x002E32C9` |

</details>

A slot already in use is detached as `0x002E3A60(slot, 1)` does: `0x0042F250`, `0x002ED470`, and its entry loses one
reference with `0x002EB810`¹. Every slot, in use or not, is then cleared: the high nibble of its
flags byte `+0x10`, `+0x00` = −1, `+0x08` = 0, `0x00269D60(slot, 0, 0)` and `+0x20` = 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E32DE`-`0x002E330E` |
| ² | `0x002E3315`-`0x002E3330` |

</details>

The attach then takes its reference on the entry (see above; `0x002E3334`-`0x002E333C`), creates the render record with
`0x0042FB80(entry +0x10, 1, 0)` while `0x01F7F508` holds the entry's id¹ and stores the record's
index, the id and the entry in the slot².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E3346`-`0x002E3360` |
| ² | `0x002E3367`-`0x002E3375` |

</details>

When the main record is in use it sets the main record's `+0xC1` to the slot's flags `+0x10 >> 4`, which the clear has
just made 0, so it writes 0¹. It calls `0x00426E20` on the new record when it is in
use², links it to the main record with `0x002EDAA0(main index, link, new index)` (the link as its
low 16 bits)³ and calls `0x002EE050(new index, 1.0, 1.0, 1.0)`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E3367`, `0x002E3379`-`0x002E33B3` |
| ² | `0x002E33B9`-`0x002E33DF` |
| ³ | `0x002E33E4`-`0x002E33EE` |
| ⁴ | `0x002E33F3`-`0x002E3404` |

</details>

Then it calls `0x002E8FD0(actor)` and, when the new record is in use, `0x004288B0(record, −1)`¹;
`0x002E8FD0(actor)` also runs before the record is created². Kind 4 ends with `0x002EDF90` on the main record
with 1 when the context holds one (`+0x00` ≠ −1) and on the `+0x90` slot with 2 when that slot holds a record,
each with its id `+0x04`, and kind 2 with both at 0 under the same tests³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E3409`-`0x002E343F` |
| ² | `0x002E3341` |
| ³ | `0x002E3444`-`0x002E34D2` |

</details>

`0x002E3C20(actor, kind, n)` detaches a slot¹ and refreshes the actor's visibility. It picks the
slot as the attach does: kind 0 → `+0x30`, 1 → `+0x60`, 2 and 4 → `+0x90`, 3 → `+0xC0 + n × 0x30` (n
unbounded); a null actor or context passes a null slot, which `0x002E3A60` ignores. For kinds 2, 3 and 4 a detach
that found a render record (`0x002E3A60` returns 1) is followed by `0x002E42D0(actor)`². Any other kind
detaches nothing. Every path ends in the refresh, a tail jump to `0x002E8FD0(actor)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E3A60` |
| ² | `0x002E3C9B` |
| ³ | `0x002E3CA8`, `0x002E3CEF` |

</details>

`0x002E3A60(slot, flag)` answers 0 for a null slot¹ and for one whose dword `+0` is −1². With
a slot whose dword `+0` is not −1, it first, for a non-zero flag, calls `0x0042F250(word +0)`, sets bits `0xB` of byte
`+0x10` and sets byte `+0x11` to `(+0x11 & 0x9F) | 6`³. It then calls `0x002ED470(dword +0)` and
`0x002EB810(dword +4)`, writes −1 to both dwords and answers 1⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E3A79` |
| ² | `0x002E3A7E` |
| ³ | `0x002E3A82`-`0x002E3A98` |
| ⁴ | `0x002E3A9B`-`0x002E3AB1` |

</details>

Every non-null slot is then reset: byte `+0x10` keeps its low four bits, dword `+0` = −1, qword `+8` = 0,
`0x00269D60(slot, 0, 0)` runs and dword `+0x20` = 0¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E3AB6`-`0x002E3AD1` |

</details>

`0x002E42D0(actor)` does nothing for a null actor, a null context or a context whose dword `+0x00` is −1¹. Otherwise it calls `0x00427280` on the render record that the context's render index names, when
that index, the word at `+0x00`, is not −1, the record address is non-null and the record is in use (`+0x284`
non-zero)², and in either case zeroes the actor's `+0xEC`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E42D3`, `0x002E42E7`-`0x002E42EC` |
| ² | `0x002E42F5`-`0x002E4314` |
| ³ | `0x002E4319` |

</details>

### The bind verbs

| verb | id | callbacks | what it does |
|---|---|---|---|
| `bindp` | `0x00C` | `0x00340380`, `0x003409F0`, `0x00342640` | pushes 1 and 0, then runs `bindp2_d4` |
| `bindp2_d4` | `0x0D4` | `0x0033F330`, `0x00342330` → `0x003409F0`, `0x00343760` → `0x00342640` | binds a model and its body replacement |
| `unkCall_5cb` | `0x5CB` | `0x00340380`, `0x003418B0`, `0x00343760` → `0x00342640` | `bindp` without the body replacement |
| `bindp2` | `0x0BD` | `0x00340380`, `0x00342330` → `0x003409F0`, `0x00343760` → `0x00342640` | enters as `bindp` does |
| `bindp2_d6` | `0x0D6` | `0x0033FC60`, `0x00342330` → `0x003409F0`, `0x00343760` → `0x00342640` | pushes 0 (`0x0033FC85`), then `bindp2_d4`'s begin |
| `modeldispose` | `0x0C1` | result `0x00342340` | passes the bound id to `0x002E3E90` (`0x00342359`) |
| `settrapresource` | `0x53B` | result `0x00355400` | passes the bound id to `0x003EC630` (`0x00355419`), on [traps](../World-Areas-And-Travel/traps.md) |
| `lockcharresource` | `0x538` | result `0x00354990` | passes the bound id and its second argument to `0x002EBD60` (`0x003549C4`) |
| `bindh` | `0x0D7` | `0x00344F00`, `0x00342330` → `0x003409F0`, `0x00345A60` | attaches a model at `+0x90` (kind 2) |
| `bindhoff` | `0x0D8` | result `0x003460F0` | detaches `+0x90`, then reattaches the body replacement |
| `bindc` | `0x200` | `0x00343B00`, `0x00342330` → `0x003409F0`, `0x00344550` | attaches at `+0xC0` or `+0xF0` (kind 3) |
| `puppetbind` | `0x41B` | `0x00343A30`, `0x00344200`, `0x003463F0` | creates a puppet from a model |
| `puppetbind_41c` | `0x41C` | `0x00344D80`, `0x00345FB0` → `0x00344200`, `0x003463F0` | pushes 0, then `puppetbind`'s begin |
| `puppetbind_41d` | `0x41D` | `0x00345AE0`, `0x00345FB0` → `0x00344200`, `0x003463F0` | pushes 1 and 0, then `puppetbind`'s begin |
| `modelread` | `0x0BF` | begin `0x00340FA0` | requests a model; raises the loading flag while it is not ready |
| `modelreadsync` | `0x0C0` | `0x003414A0`, `0x00341840` | waits for a model requested earlier |
| `stdmotionreadsync` | `0x119` | poll `0x0034B8D0` | waits for the actor's motion lane |
| `charcachedispose` | `0x146` | `0x00340450`, `0x00340800` | releases this script's holds |
| `charcachedisposeall` | `0x3C8` | `0x00340EC0`, `0x00340800` | releases every hold |
| `debug_bindp` | `0x2000` | `0x0050D660`, `0x0050D710`, `0x0050D810` | binds a model with a free lane, sets `+0xF0` = `0x1001` |

The result callback `0x00342640` of `bindp`, `bindp2_d4` and `unkCall_5cb` ends the same way after its bind: it
refreshes the lane index¹ after either bind, and on every path, bound or not, it reads the
body weight `0x00265950(actor)`, float `[[actor + 0xC0] + 0x148]`, or 0.0 when it has no context², and tail-jumps to `0x0025B470(actor, weight)`³, which re-applies the body mask's bit `0x10`
([Movement bodies](../Movement-And-Pathfinding/movement-bodies-and-separation.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EAC90`, `0x003426C1` |
| ² | `0x0026595A`, `0x003426C9` |
| ³ | `0x003426DE` |

</details>

Every begin that creates a binding creates none when the script manager's byte at `0x02099011 + manager × 0x288` is set
(`0x00267310`, manager = actor `+0x15`); the begins of `bindp2_d4`, `bindh`, `bindc` and `puppetbind` then clear the
active byte in their arguments so the poll and result skip. `bindp2_d4` also skips an actor whose `+0x18` is non-zero.

`bindp2_d4(model, b, c)`¹ pops c, b and the model and sets the state word `args + 0xA` to 0². It calls `0x002E97B0(actor)`, the context getter, and leaves its result unused³.
With actor `+0x18` non-zero it clears the active byte `args + 8` and still raises the loading flag: it
tests a null entry, which `0x002E4C20` reports as not ready⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0033F330` |
| ² | `0x0033F34D` |
| ³ | `0x0033F382` |
| ⁴ | `0x0033F3A0`, `0x0033F3E1`-`0x0033F3F0` |

</details>

Otherwise it sets the active byte to 1, calls `0x0025AB30(actor)`¹, stores b and c in context
`+0x14C` and `+0x14D` (`0x0026D610`, actors of kind `0x60` only), and finds or creates the model's entry with
holder bit = manager. It keeps the bound id at `args + 0` and the entry's handle at `args + 4`² and raises the loading flag when the entry is not ready³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0033F3B3` |
| ² | `0x0033F3C6`, `0x0033F3DE` |
| ³ | `0x0033F3E4`-`0x0033F3F0` |

</details>

Its poll `0x003409F0` runs a state word at `args + 0xA` and returns 0 at once while the active byte
`args + 8` is 0¹. State 0 waits for the entry, raising the loading flag and returning 1 on
each wait; a handle that no longer resolves is re-created from `args + 0` with holder bit = manager and
stored back².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00340A0F` |
| ² | `0x00340A2D`-`0x00340A4A` |

</details>

When the entry is ready it looks up a body replacement with
`0x0037CB90(model, b, c)`, b and c read back as signed bytes from context `+0x14C` and `+0x14D` (`0x002657E0`,
`0x00263FC0`, `0x00340A69`-`0x00340A7F`; 1 and 0 for an actor not of kind `0x60` or without a context).

The model rebuild's state 19 reads the same two bytes through `0x002657E0` and `0x00263FC0` (`0x0037BD90`, `0x0037BD86`;
[actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md)).

The debug verbs `debug_tty_modellocalno`¹ and `debug_tty_modelclutno`² read `+0x14C` and
`+0x14D` respectively, as signed bytes, for an actor that is found, of kind `0x60`, with `0x002EA6A0` answering non-zero
and a non-null context³, and print the value with `"%d "` through
`0x0017D280`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0050D860` |
| ² | `0x0050D780` |
| ³ | `0x0050D899`-`0x0050D8C2`, `0x0050D7BC`-`0x0050D7E2` |
| ⁴ | `0x0050D8D0`, `0x0050D7F0` |

</details>

`0x0037CB90` takes the first row of the replacement table `[0x02ADD940]` that matches (count
`[0x02ADD938]`, rows of `0x30` bytes: model, b, c, a pair count at `+0xC`, four value slots at `+0x10`
and four threshold slots at `+0x20`). The model must be equal¹; b and c each match when
equal or when the row holds −1, which matches anything².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0037CC00` |
| ² | `0x0037CC05`-`0x0037CC1A` |

</details>

It returns the last value, in pair order, whose threshold is at or below the story-progress word
(`0x00265270`, its low 16 bits compared signed with the threshold, `0x0037CC74`), or −1. A matching row
with a signed pair count of 0 or less gives −1¹, and later rows are not tried. The loop
runs the whole count with no cap at four², so a fifth pair reads its value from `+0x20`
and its threshold from the next row. It returns −1 while the byte `0x01E02800` is 0 or the table
pointer is null³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0037CC5A` |
| ² | `0x0037CC89` |
| ³ | `0x0037CBAD`, `0x0037CBBB` |

</details>

No replacement: state 1, the poll returns 0, and the
result binds the model: `0x002EBC90(actor, 0, 1)`, the bind `0x002E28E0` with the entry `args + 4` resolves
to, then `0x002EAC90`¹. A replacement: the poll binds the model itself
with the same three calls², sets state 2, finds or creates the replacement's entry
with holder bit `0x1` (`0x002EB540(replacement, 0)`) and stores its handle at `args + 4`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00342662`-`0x00342683`, `0x003426C1` |
| ² | `0x00340AA7`-`0x00340ACA` |
| ³ | `0x00340AEB` |

</details>

When that entry is already ready the poll sets state 3 and returns 0 in the same call¹. Otherwise it waits in state 2, where a handle that no longer resolves is not
re-created and the wait goes on²; when it is ready, state 3 and the
result attaches it at `+0x90` (kind 4): `0x002EBC90(actor, 3, 1)`, `0x002E3110(actor, 4, 0, entry, 0)` and
`0x002EAC90`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00340AFB`-`0x00340B0C` |
| ² | `0x00340B14`-`0x00340B27` |
| ³ | `0x0034268B`-`0x003426C1` |

</details>

The result binds nothing when the active byte is 0 or the state is
neither 1 nor 3¹. A poll entered with a state other than 0 or 2 returns the dword
at `[rsp + 0x40]`, a stack slot it never writes².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00342655`, `0x00342689` |
| ² | `0x00340B3B` |

</details>

`bindh` and `bindc` reach the same poll through `0x00342330`, a jump to `0x003409F0`, and their begins¹ start it at state 0 with the bound id at `args + 0`. A `bindh` or `bindc` model
that has a replacement row is therefore bound as the actor's main model by the poll, and `args + 4` then
holds the replacement's handle, which their results attach.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00344F00`, `0x00343B00` |

</details>

`unkCall_5cb`'s poll `0x003418B0` stops at state 1 once the entry is ready, so its result always
binds the model alone. It has the same inactive exit, state-0 waits and re-creation of a stale handle¹, and the same state-2 wait², though neither it nor its
begin `0x0033F330` stores state 2; a state other than 0 or 2 returns the dword at `[rsp + 0x40]`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003418C5`, `0x003418DF`-`0x003418FC` |
| ² | `0x00341932` |
| ³ | `0x00341965` |

</details>

`bindh(model)`¹ pops the model and turns it into a bound id² and zeroes the state word `args + 0xA`³, all before the manager's-byte test, so on
both of its paths.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00344F00` |
| ² | `0x00267E10`, `0x002E9A60`, `0x00344F18`-`0x00344F1F` |
| ³ | `0x00344F28` |

</details>

Past the manager's-byte exit described above¹ it stores the bound id in `args[0]`²,
finds or creates the entry with holder bit = manager³, keeps its handle in `args[1]`⁴ and sets the active byte to 1⁵. Its result `0x00345A60` attaches it as
kind 2 with `0x002EBC90(actor, 3, 1)`⁶ and `0x002E3110(actor, 2, 0, entry, 0)`⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00344F30`-`0x00344F39` |
| ² | `0x00344F4D` |
| ³ | `0x002EB540`, `0x00344F55` |
| ⁴ | `0x002E9810`, `0x00344F5D`-`0x00344F67` |
| ⁵ | `0x00344F6A` |
| ⁶ | `0x00345A89` |
| ⁷ | `0x00345AAB` |

</details>

`bindc(n, model, link)` clamps n to 0..1, `n < 0 ? 0 : n > 1 ? 1 : n`¹, and its result
`0x00344550` attaches the entry as kind 3 in slot n with `0x002EBC90(actor, n + 4, 1)`² and the given
link³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00343B47`-`0x00343B5D` |
| ² | `0x0034457E` |
| ³ | `0x003445A2` |

</details>

Both results skip when the active byte is clear or the bound id in `args[0]` is negative¹, and attach the entry that the handle in `args[1]` names. The shared poll
`0x003409F0` also looks the bindh or bindc model up with `0x0037CB90`: for a replacement it binds that
model as the actor's main model² and stores the replacement's handle in `args[1]`³, so the result attaches the replacement.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00345A77`, `0x00344567` |
| ² | `0x00340AC2` |
| ³ | `0x00340AEB` |

</details>

`bindhoff`'s result `0x003460F0` detaches kind 2 (`0x002E3C20(actor, 2, 0)`, `0x00346112`) on every path, and stops there
when the actor has no presentation context¹ or context `+0x00` is −1². Otherwise it looks up `0x0037CB90(id at context +0x04, 0x002657E0(actor), 0x00263FC0(actor))`³ and, for a replacement (an answer that is not negative, `0x00346147`), finds or creates its
entry with holder bit = manager through `0x002EB540`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E97B0`, `0x00346100` |
| ² | `0x0034611A`, `0x0034611F` |
| ³ | `0x00346129`-`0x00346140` |
| ⁴ | `0x0034614F` |

</details>

The result's null test of that entry¹ never fires, because `0x002EB540` writes through the entry before it
returns².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0034615A` |
| ² | `0x002EB5AD`, `0x002EB5B1`-`0x002EB5B9` |

</details>

An entry that is not ready keeps the manager's holder bit and is not attached¹.
When the actor's model has a replacement that is already ready, the result calls `0x002EBC90(actor, 3, 1)` and attaches
it as kind 4 with `0x002E3110(actor, 4, 0, entry, 0)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E4C20`, `0x0034615F`-`0x00346166` |
| ² | `0x00346174`, `0x0034618E` |

</details>

`puppetbind(d, model, x, y)`¹ finds or creates the model with `0x002EAE20` and keeps the
manager byte; its poll waits for the entry, re-creating it if the handle went stale; its result
`0x003463F0` calls `0x003EB190(d, entry, manager, x, y)`², which replaces puppet slot d
(below 32) in the table at `0x02B5EA20`. `puppetbind_41c(d, model, x)` passes y = 0 and
`puppetbind_41d(d, model)` passes x = 1, y = 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00343A30` |
| ² | `0x00346437` |

</details>

`0x003EB190` returns at once when d is above 31 compared unsigned, so a negative d changes nothing
either¹. Otherwise it releases a puppet already in the slot with `0x003EB470` and clears
the slot², then stores `0x003EB250(entry, manager, x, y)` there, the bind that
takes the first record of the free list at `0x02B5EB70`³. `0x003EB250` returns
null when that list is empty, and for a null entry it returns the first free record without
unlinking or binding it⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EB193` |
| ² | `0x003EB1C9`, `0x003EB1CE` |
| ³ | `0x003EB1E2`, `0x003EB1F1` |
| ⁴ | `0x003EB260`, `0x003EB45C` |

</details>

`0x003EB470(record)` does nothing for a null puppet record¹. Otherwise it calls `0x002ED470` with the puppet
record's dword `+0x10`, `0x002EB870` with its qword `+0x18` and `0x00265F90(record + 0x10)`²,
unlinks the puppet record and zeroes its two links³, pushes it on the free list at `0x02B5EB70`⁴ and clears its byte `+0x40`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EB473` |
| ² | `0x003EB485`-`0x003EB497` |
| ³ | `0x003EB49C`-`0x003EB4BE` |
| ⁴ | `0x003EB4C2`-`0x003EB4E3` |
| ⁵ | `0x003EB4E7` |

</details>

When the entry is not null and the free list is not empty¹, `0x003EB250(entry, manager, x, y)`
unlinks the free list's first puppet record and pushes it on the bound list at `0x02B5EB20`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EB260`-`0x003EB26C` |
| ² | `0x003EB272`-`0x003EB2C5` |

</details>

It stores the manager in the puppet record's byte `+0x41`, 1 in its byte `+0x40` and the entry at `+0x18`, adds one to
the entry's reference count `+0x1C` and clears its pending-release bit (`+0x18` bit `0x4`)¹.
The puppet record's dword `+0x10` takes `0x002ED4E0(entry dword +0x10, x, y)`, called while `0x01F7F508` holds the entry's
id `+0x14`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EB2B4`-`0x003EB2D7` |
| ² | `0x003EB2DB`-`0x003EB2EF` |

</details>

While the puppet record's render index, word `+0x10`, is not −1, the render record at `[0x022C6F28]` + index ×
`0x740` is non-null and its `+0x284` is non-zero (re-read before each step), the bind clears the render record's qword
`+0x108`, calls `0x003E5E20(render, 0)` and clears its byte `+0x413`¹, and takes
`0x00423280(render)` (30.0 from `0x008F8D80` otherwise; `0x003EB383`-`0x003EB3D2`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EB2F5`-`0x003EB37C` |

</details>

It then calls `0x002E8340(record + 0x10, 0)` and `0x002EE050(index, 1.0, 1.0, 1.0)`¹ and, while the
same tests still pass, `0x00427300(render, that value)` and `0x00426E20(render)`². It returns the
puppet record³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EB3D5`-`0x003EB3F2` |
| ² | `0x003EB3F7`-`0x003EB457` |
| ³ | `0x003EB45C` |

</details>

`modelread(model)` finds or creates the entry with holder bit = manager and raises the loading flag
when the entry is not ready. `modelreadsync(model)` stores the handle of the model's entry (0 when
no entry exists); its poll waits until the entry is ready, counting the waits in `args[2]`, and ends at
once for a handle of 0 or one that no longer resolves.

`stdmotionreadsync`'s poll `0x0034B8D0` reads the actor's motion lane, the signed byte
`[actor + 0xC0] + 0x12` (`0x002E9C00`, −1 without a context), and tests it on the main entry with
`0x002E4C30` (the lane's `+0x24` bit; 1 for a negative lane; −1 without a matching lane record). A
loaded lane ends the poll after `0x002EAC90` (and `0x002EB380` when actor `+0x0D` bit `0x80` is set).
Otherwise it claims the lane with `0x002EB9D0`, raises the loading flag and waits¹; it ends
at once when the claim fails² or the context has no main entry³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0034B953` |
| ² | `0x0034B94C` |
| ³ | `0x0034B907` |

</details>

The poll first calls `0x00263A30(manager, word [actor + 0x00])`, which returns a pointer into the
manager's script image (the string `NOACTOR` at `0x00915708` when the manager, its script or the
actor's record is missing), and drops it¹. An actor with
no presentation context ends the poll before the lane is read². Its ending paths call
`0x0053DD10`, which always returns 1³, so the call to the `ret 0` stub `0x0016D6A0` at
`0x0034B96D` never runs and the poll returns 1, a wait, only after a claim.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0034B8F6` |
| ² | `0x0034B8FE` |
| ³ | `0x0034B961` |

</details>

`stdmotioneventsync` (`0x0473`) waits for a marker in the actor's motion. Its begin `0x002ECFD0`
(through `0x003479E0`) clears bits `0x1` and `0x2` of the render record's `+0x419` (`0x0042F210` for each);
its poll `0x00347DD0` ends when either bit is set again¹. The motion sets
them through its authored command id 4, subtypes 11 and 10².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ECF60`, `0x0042F1C0` |
| ² | `0x00417AD0` |

</details>

`0x002ECFD0` reads the render index at context `+0x00` and clears nothing for a null actor, an actor without
a context or an index of −1¹; otherwise it calls `0x0042F210(index, 0)`
and `0x0042F210(index, 1)` with the index's low 16 bits².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ECFD7`, `0x002ECFE3`, `0x002ECFEF` |
| ² | `0x002ED000`-`0x002ED00F` |

</details>

`debug_bindp(model)`¹ finds or creates the model with `0x002EAE20` (holder bit `0x1`), stores
the entry pointer itself rather than a handle, claims a free lane (`0x002EB9D0(entry, −1)`), requests
it with `0x002EB490` and stores it with `0x002EC6B0`. Its poll `0x0050D710` waits for the entry to be
ready and the lane loaded.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0050D660` |

</details>

Its result `0x0050D810` binds the stored pointer and calls `0x002EB330(actor, 0x1001)`, and tests no
flag. In order it sets the context's flags nibble with `0x002EBC90(actor, 0, 1)`¹, binds
the stored pointer², refreshes the lane index with `0x002EAC90`³
and calls `0x002EB330(actor, 0x1001)` as a tail jump⁴. `0x002EB330` sets actor `+0x0D` bit
`0x1`, `+0xF5` = `0xFF`, `+0xEC` = 0 and `+0xF0` = `0x1001`, and calls
`0x002EB0D0(actor, context, 0x1001, 0, −1.0)` unless `+0x18` is 1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0050D829` |
| ² | `0x002E28E0`, `0x0050D835` |
| ³ | `0x0050D83D` |
| ⁴ | `0x0050D854` |

</details>

`charcachedispose` calls `0x002E3E20(manager, 0)` and `0x002E4000(manager, 0)` and sets `0x0215FD46` (its begin `0x00340450`
ends with a jump to `0x002EC500`, which stores 1 there, `0x0034047B`); `charcachedisposeall` calls both with the manager
and −1 (`0x00340ED7`, tail jump `0x00340EE8`), which clears the whole holder word of every live entry and the manager's
group word in every idle lane record. Both begins first zero the dword at `args + 0`¹; their
shared poll `0x00340800` adds one to it and returns 1 while it is 1 or less, so the first poll returns 1 and the second
returns 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00340456`, `0x00340EC6` |

</details>

`lock_charmotion_once` (`0x011C`) keeps an area's models through its next release, once. Its handler `0x0034D350` is
`mov ecx, 1` and a jump to `0x0026AF70`, a seven-byte store that the function list does not hold. Three release paths
read the byte. While it is 0 each calls `0x002E4000` and `0x002E3E20` for the manager; while it is 1 they skip
both, so the manager's holds on its models survive:

- the definition-payload arm `0x0025AFC0`, for manager 0 only, then clears the byte;
- the field-runtime record step `0x00261F90`, which leaves it;
- the manager unload `0x002628B0`. That read is dead, because the unload first calls `0x005C5230`, which returns 0, and on
  that 0 stores 0 into the byte before the test.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02099DA0` | `u8` | 0 (zero-filled tail of `.data`) | the one-shot model hold: 1 skips the two model releases at the next release that reads it | `0x0026AF70`, 1 (`0x0026AF70`, from `0x0034D350`); `0x0025AFC0`, 0 (`0x0025B02F`); `0x002628B0`, 0 (`0x00262D4B`, `0x00262D8F`, `bpl` 0); the start-up reset `0x00266D10`, 0 (`0x00266DF7`, `esi` cleared at `0x00266D3E`) | `0x0025AFC0` (`0x0025AFFB`); `0x00261F90` (`0x00261FDA`); `0x002628B0` (`0x00262D63`) |

`0x0037B4D0`, the party member rebuild, is the fifth caller of the bind. The resolver `0x002E97C0` has
20 call sites in 11 functions; the bind `0x002E28E0` has five callers: `0x003409F0`, `0x00342640`,
`0x00355210`, `0x0050D810` and `0x0037B4D0`.

## Layouts

<details>
<summary>Show the memory layouts</summary>

Binding entry   `0x0215FDA0` + slot*`0x40`, 128 slots:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` |  | prev (free / requested / live / retired list) |
| `+0x08` | `...` |  | next (free / requested / live / retired list) |
| `+0x10` | `u32` |  | load handle (`0x0036B160`) |
| `+0x14` | `u32` |  | bound id |
| `+0x18` | `u8` |  | state: bit `0x2` ready, bit `0x4` release pending, bit `0x8` not registered with the render system |
| `+0x19` | `u8` |  | pins: mask `0x3` keep at count 0, bit `0x4` no load buffer, bit `0x8` created with a holder, bit `0x10` kept by `0x002E3E90` |
| `+0x1A` | `u16` |  | own slot |
| `+0x1C` | `i16` |  | reference count |
| `+0x1E` | `i16` |  | lane record index (-1 no lane record) |
| `+0x20` | `u16` |  | holder bits (one per manager) |
| `+0x24` | `u32` |  | stamp (`+0x26` always 0) |
| `+0x28` | `u32` |  | claimed lanes |
| `+0x2C` | `u32` |  | lanes with a positive size |
| `+0x30` | `u32` |  | sub-resources (-1 no sub-resource); with `+0x34` and `+0x38` |
| `+0x34` | `u32` |  | sub-resources (-1 no sub-resource); with `+0x30` and `+0x38` |
| `+0x38` | `u32` |  | sub-resources (-1 no sub-resource); with `+0x30` and `+0x34` |

Lane record     `0x02161DA0` + i*`0x120`, 32 records:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` |  | links (free `0x0215FD70`, idle `0x0215FD68`, pending `0x0215FD80`); with `+0x08` |
| `+0x08` | `...` |  | links (free `0x0215FD70`, idle `0x0215FD68`, pending `0x0215FD80`); with `+0x00` |
| `+0x10` | `...` |  | unload-queue node (`0x0215FD90`); with `+0x18` |
| `+0x18` | `...` |  | unload-queue node (`0x0215FD90`); with `+0x10` |
| `+0x20` | `u16` |  | own index |
| `+0x22` | `u16` |  | owner slot |
| `+0x24` | `...` | loaded |  |
| `+0x28` | `...` |  | to load |
| `+0x2C` | `...` |  | queued for unload |
| `+0x34` | `...` | loading |  |
| `+0x38` | `...` |  | hold mask |
| `+0x3C` | `...` |  | tested with `+0x38` |
| `+0x40` | `...` |  | mask read by `0x002E9C60` |
| `+0x44` | `...` |  | keep on load |
| `+0x48-0x5B` | `...` |  | five group words |
| `+0x5C` | `u32` |  | owner's stamp |
| `+0x60` | `u32[32]` |  | lane handles |
| `+0xE0` | `i16[32]` |  | lane counts |

Chest record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | index in the field |
| `+0x04` | `i16` |  | x tenths |
| `+0x06` | `i16` |  | z tenths |
| `+0x08` | `u8` |  | facing (mask `0x3F`) and random gil (bit `0x40`) |
| `+0x09` | `u8` |  | opened-flag id |
| `+0x0A` | `u8` |  | presence % |
| `+0x0B-0x17` | `...` |  | contents (reward verbs) |

Presentation    [actor+`0xC0`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `...` |  | render index |
| `+0x004` | `...` |  | bound id |
| `+0x008` | `...` | entry |  |
| `+0x010` | `...` | flags |  |
| `+0x012` | `i8` |  | motion lane |
| `+0x14C` | `u8` |  | variant byte b |
| `+0x14D` | `u8` |  | variant byte c |
| `+0x030` | `...` |  | attach slots (`0x30` each); with `+0x60` and `+0x90` and `+0xC0` and `+0xF0` |
| `+0x060` | `...` |  | attach slots (`0x30` each); with `+0x30` and `+0x90` and `+0xC0` and `+0xF0` |
| `+0x090` | `...` |  | attach slots (`0x30` each); with `+0x30` and `+0x60` and `+0xC0` and `+0xF0` |
| `+0x0C0` | `...` |  | attach slots (`0x30` each); with `+0x30` and `+0x60` and `+0x90` and `+0xF0` |
| `+0x0F0` | `...` |  | attach slots (`0x30` each); with `+0x30` and `+0x60` and `+0x90` and `+0xC0` |

`0x002ED6F0`, letter class → resource kind, file index, lane count:

```python
'C' 0x43 -> 0x0F, n,      0      'b' 0x62 -> 0x16, n*2,    1      'n' 0x6E -> 0x13, n*0x19, 24
'M' 0x4D -> 0x12, n,      0      'c' 0x63 -> 0x0E, n*0x19, 24     's' 0x73 -> 0x17, n*0x19, 24
'N' 0x4E -> 0x14, n,      0      'g' 0x67 -> 0x0D, n*2,    1      't' 0x74 -> 0x19, n,      0
'S' 0x53 -> 0x18, n,      0      'm' 0x6D -> 0x22, n*0x0B, 10     'w' 0x77 -> 0x10, n,      0
other    -> 0x01, n,      1      (kind 1 adds 0x33 to the index)
```

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Verb | Uses in the US scripts |
|---|---|
| `bindp2_d4` | 9,877 |
| `modelread` | 4,539 |
| `modelreadsync` | 4,531 |
| `bindp2` | 2,061 |
| `stdmotionreadsync` | 1,989 |
| `setuptreasure` | 1,966 |
| `bindc` | 1,561 |
| `modeldispose` | 1,319 |
| `bindhoff` | 774 |
| `bindh` | 706 |
| `settrapresource` | 390 |
| `charcachedispose` | 289 |
| `puppetbind` | 285 |
| `puppetbind_41d` | 24 |
| `bindp2_d6` | 22 |
| `unkCall_5cb` | 1 |
| `bindp`, `puppetbind_41c`, `charcachedisposeall`, `debug_bindp`, `lockcharresource` | 0 |

</details>

## Operations

Per frame: one pass of `0x002E65A0` (lane unload queue, retired releases, lane pump, request pump).
Per bind verb: one begin, one poll per frame until the entry is ready, one result.

## State

<details>
<summary>Show the state it keeps</summary>

The 128 binding entries and 32 lane records, the list heads `0x0215FD58` to `0x0215FD98`, the flag
`0x0215FD46`, the loading flag `0x022C253D`, and each actor's presentation context. The flag sits in a band of
separate globals, `0x0215FD40` to `0x0215FD57`: the float `0x0215FD40`¹, the masks `0x0215FD44` and
`0x0215FD45`², the wind save `0x0215FD47` and `0x0215FD48`³, the
sound gates `0x0215FD54` and `0x0215FD55`⁴, the culling mask `0x0215FD56`⁵ and the byte
`0x0215FD57`⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EEED0` |
| ² | `0x002EA8E0`, `0x002EA8B0` |
| ³ | `0x002EAB40`, `0x002EAA60` |
| ⁴ | `0x002E9D90` |
| ⁵ | `0x002EBBF0` |
| ⁶ | `0x002E63B0` |

</details>

</details>

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
- [Script variables](script-variables.md): the reference decoder `0x002650B0`.
- [Movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md):
  the separation weight and mask the chest sets.
