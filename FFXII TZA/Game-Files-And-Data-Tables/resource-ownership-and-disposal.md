---
title: "Resource ownership and disposal: who owns a loaded source, copy or borrow, effect tickets and contexts, the script motion slots, borrowed views, and the order things are torn down"
kind: "system"
category: "Game files and data tables"
addresses: "0x0041E580, 0x0041E490, 0x00409FE0, 0x00409A60, 0x00409730, 0x00409D60, 0x00409960, 0x00409C00, 0x00427B00, 0x003B3160, 0x003B38B0, 0x003B37E0, 0x003B39E0, 0x003B3B10, 0x003B3C00, 0x0024B3A0, 0x0024F410, 0x0024F4D0, 0x003A9600, 0x003A9950, 0x003A9730, 0x003A9A70, 0x003EDAD0, 0x003AB880, 0x003AB940, 0x003AB7C0, 0x00369800, 0x02EBCD80, 0x02EBD480, 0x020910A0, 0x02F97340, 0x02B64380, 0x02B581A0, 0x02B58A60, 0x003DDA20, 0x003DD4C0, 0x003DDA70, 0x003DD850, 0x003DD420, 0x003DD380, 0x003DD740, 0x003DD770, 0x003492A0, 0x003499C0, 0x0034A6A0, 0x0032F240, 0x0032F170, 0x0032F290, 0x0032F260, 0x00267310, 0x002E4D20, 0x002E4E50, 0x003DC340, 0x003DC5B0, 0x0032E620, 0x0041FCF0, 0x00409CA0, 0x0040A1E0, 0x003A7D30, 0x004096F0, 0x0051F880, 0x005371C0, 0x00537270"
---

## What the player sees

Character motions, effects and script-loaded animation sets appear when their data has loaded and
vanish cleanly when the scene that loaded them is unloaded. An event script that calls `motionread`
waits in `motionreadsync` until the animation set is in memory, plays it, and frees it with
`motiondispose`. Underneath, every loaded block has exactly one owner that frees it, and every
renderer, effect and view that uses it is detached before that happens.

## How it works

Ownership is held per layer, with no shared reference count. A loader owns the bytes it read; the
render resource bank owns either a copy of them or a reference to them; an effect ticket owns an
effect context; the context owns its lookup tables and, in copy mode, its effect data. Each layer is
released by its own routine, in a fixed order.

### The render resource bank

Every loaded source that renders goes through one door: `0x0041E580(manager, source)` loads the bank at
`manager + 0xD90` and jumps to `0x00409FE0`. The manager is `[[0x022C6F28] + 0x48830]` decoded with
`0x0020E600`. The bank holds `0x50`-byte entries (layout below).

`0x00409FE0` first looks for an entry with the same tag and name. A match returns that entry unchanged:
its source is not replaced and its data is not parsed again. Otherwise it takes a new slot and fills
it with `0x00409A60`, which picks the mode from the source value (`0x003AB860`):

- **Mode 0, owned copy** (an untagged pointer): the entry reserves a buffer of the size in the
  source's header `+8`, copies the bytes into it, and from then on uses only the copy (`+0x10`). The
  caller still owns the original.
- **Mode 1, retained source** (a tagged handle): the entry stores the handle at `+0x30` and the
  resolved pointer at `+0x38` and copies nothing. The bytes stay owned by whoever allocated them.

Both modes pad the root and child section names to 32 bytes inside the input before the split, so
the input is written to either way.

### Effect sections and tickets

When the source is an `@FRP` container with an `@FEF` section (`0x00409A30`), `0x00409FE0` also makes an
effect ticket. It looks up a configuration pointer in the table at `0x02B64380`, indexed by the source
entry name's last five characters: the letter's code × `0x500` plus the four digits as a number. A NULL entry writes to
address 0 and ends the game. It then calls `0x003B38B0(source, offset)` with the section offset from the
footer, and for a name containing `chara\h` it parses `%d.efx` and stores the number in the ticket
(`0x003B3B10`; −1 when it does not parse).

The tickets are 32 records of `0x38` bytes at `0x02EBCD80` (`0x003B3160` builds them at start-up), with a
free list (`0x02EBDB88`) and an in-use list (`0x02EBDB80` head, `0x02EBDB90` tail). A ticket id is the slot
in bits 0–5, a 22-bit counter (`0x02EBDBB0`) in bits 6–27 and 3 in bits 28–31, so a recycled slot gets a
new id.

The record is found by the id's low six bits; an id with slot bits 32–63 would land in the
instance-handle records at `0x02EBD480`, which follow the tickets, but no ticket id has them.
`0x003B38B0` returns 0 with no context when the free list is empty, and `0x00409FE0` stores that 0 in the
entry's `+0x44` (`0x0040A17C`). Otherwise it:

1. resolves the source (`0x003AB7F0`) and adds the offset;
2. fills a stack template: type 3, flags `+2` `|= 0x0C`, the resolved base at `+0x858`, the source
   at `+0x860` and the offset at `+0x864`;
3. builds the context with `0x0024B3A0` and stores it in the ticket `+0x18`;
4. parses the effect data with `0x003EDAD0(base, dword [base + 0x0C])`.

### Effect contexts

`0x0024B3A0(template)` allocates `0x890` bytes, copies the template, links the copy at the head of the
list `0x020910A0[type]`, clears `+0x870`..`+0x888`, makes it current (`0x02F97340`) and builds its lookup
tables, among them the 320-slot `+0x848` table and the 768-slot `+0x850` table. Its other callers are
`0x0026FB90` (type 2, also flags `|= 0x0C`), `0x002FC4A0` (type 1), `0x003B0660`, `0x003B2220` (type 7) and
`0x003B29B0`.

Flag bit `0x4` decides whether the context borrows or copies its two large runs of effect records.
At `0x003EE018` and `0x003EE117` `0x003EDAD0` tests it:

- **Clear (copy):** allocate the run in arena 8 and copy it, the length truncated toward zero to a
  multiple of 16; the copy goes to `+0x878` or `+0x870`.
- **Set (borrow):** store the input pointer itself at `+0x878` or `+0x870`.

A borrowed run is written in place. Each record starts with a `u16` id and a subtype byte, followed by
its payload. `0x003A9730` copies them into the payload at `+0x280` and `+0x282` and stores the payload's
address in the `+0x848` table at the id; `0x003A9A70` does the same at `+0x42` and `+0x44` with the
`+0x850` table. Both then relocate the payload's stored offsets. For a mode 0 entry this rewrites the bank's copy; for a
mode 1 entry it rewrites the original source.

### The four loaders that register sources

`0x0041E580` has four callers, each a read completion:

| Loader | Completion | Size test before the read |
|---|---|---|
| script name-binding entries | `0x002E4D20` | positive size only |
| script name-binding lanes | `0x002E4E50` | positive size only |
| script motion slots | `0x003DD850` | length of at least 1 |
| motion cache | `0x003DC340` | none: `0x003DC5B0` files whatever size `0x003DC8D0` returns, −1 included |

Each reads into a block it owns and registers that block, so a registration always sees freshly read
bytes. A −1 size completes as delivered (see the read queue page), so only the motion cache can reach
registration without a read: when `0x003DC8D0` (sixteen cached sizes at `0x02B580B0`) gets a negative
index or size it returns −1 and sets a failure flag that `0x003DC5B0` ignores, and the completion then
registers a block nothing was read into.

### Script motion slots

`motionread` (`0x00A2`, `0x003492A0`), `motionreadsync` (`0x00A3`, poll `0x003499C0`) and `motiondispose`
(`0x00A4`, `0x0034A6A0`) work on 80 records of `0x1C` bytes at `0x02B581A0`, five area slots of sixteen.
The area slot is the running script's (`[[0x02099D70] + 0x28]`), the motion number is the verb argument.
A record moves through these states (`+0x04`):

| State | Meaning | Entered by |
|---|---|---|
| 0 | idle | reset, a failed sweep, a completed dispose |
| 2 | armed | `0x003DDA20`, from state 0 only, also sets bit `i` of `0x02B58A60[g]` |
| 1 | allocated but held; never read | the sweep, when the area slot's hold byte `0x02099011 + g × 0x288` is set |
| 3 | read in flight | `0x003DDA70` |
| 4 | registered | the completion `0x003DD850` |
| 5 | dispose requested while in flight | `0x003DD420` on state 3 |

The sweep `0x003DD4C0` runs over every record with its pending bit and state 2:

1. The area slot's file comes from `0x0032F240` (enable byte `0x022C6D18 + g`, selector `0x022C6D28 + 4g`)
   and `0x0032F170`: kind 5, index `3s` for slot 0; kind 8, index `4s` for slots 1–3; kind 1, index
   `s + 0x6B` for slot 4. The motion is read from index + 1, the area's `.mot`.
2. The offset and length come from the first `0x88` bytes of that `.mot`, which the area loader keeps
   at `0x022C6E70[g]`: byte 0 is an active flag, then sixteen `{u32 offset, u32 length}` pairs from `+8`
   (`0x0032F260`, `0x0032F290`). Area slot 4 and an inactive header give −1, so slot 4 never loads.
3. It allocates the length in arena 6, or first in arena 11 when `0x0037B330()` is 2 and the area slot's
   byte `+0x17` has bit `0x40` (route byte `+0x0D` = 1; `0x0037B330` answers only 0 or 4, so this
   route is never taken), pins the block and stores the handle, length,
   offset, kind and index + 1.
4. A held area slot goes to state 1; otherwise `0x003DDA70` files the read (`0x0032E620`) with the record's
   address as the callback argument and sets state 3 without checking the result.

Any failure sets state 0 and leaves the pending bit, and the next sweep skips the record until it is
armed again. `motionreadsync` waits while the state is 2 or 3 (`0x003DD770`).

A read that fails calls no completion, because the queue's failure callback needs a −1 byte count and
these reads never file one. The record then stays in state 3: `motionreadsync` waits for good,
`motionread` cannot re-arm it, a dispose only sets state 5, and the pinned block is never freed.

The completion `0x003DD850` unpins the block first. In state 5 it releases the bank entries for it
(`0x0041E490`), frees the block (`0x00369800`) and sets state 0, leaving the old handle in the record.
Otherwise it registers the block (`0x0041E580`) and sets state 4, whatever the registration returned.
`0x003DD740` returns the handle only in state 4.

`motiondispose` (`0x003DD420`) and the area unload `0x002628B0` through `0x003DD380` (all sixteen of one area
slot) act by state:

- state 1: free the block and clear its handle, state and route;
- state 3: set state 5 and let the completion finish it;
- state 4: release the bank entries (`0x0041E490`), free the block and clear its handle, state and
  route;
- states 0, 2 and 5: nothing.

An armed record (state 2) survives the unload with its pending bit, and the next sweep takes the file
from whatever area the slot then holds, so the motion is read from the next area's `.mot`.

### Borrowed views

`0x00409960(entry, tag, name)` returns a pointer into an entry's data: the section offset from
`0x00409780` (0 when the section is absent) added to the entry's base. A mode 0 entry resolves its copy
(`0x0051EE30`, `0x006B5C70`); a mode 1 entry pins its source with `0x003AB880`, which takes the block out of
the movable tree so compaction cannot move it. The sum is `low32(base) + offset` sign-extended.

`0x00409C00(entry)` ends the view: `0x0051EF80` for mode 0, `0x003AB940` for mode 1. The pin is a flag, not
a count: one release ends every pin on the block. The only user is `0x0041FCF0`, which opens a view at
`0x0041FFA0` and ends it at `0x0041FFF8`.

`0x005371C0(array, fn, first)` uses the same view on a strided array (stride `+0x20`, count `+0x24`): it
opens it (`0x0051EE30`, `0x006B5C70`), calls `fn` on `count - first` elements counted from element 0,
not from `first`, and ends it (`0x0051EF80`). Its one caller `0x00537270(array, stride, count, fn)` sizes
the array (`0x0051F020`), stores the stride and count, and runs it with `first` 0 when `fn` is set.

### Disposal order

`0x0041E490(manager, source)` pins and unpins the source once, then calls `0x00409D60(manager + 0xD90,
source)`. `0x00409D60` loops while the bank finds an entry for the source (`0x0051FE30` with the test `0x004095B0`,
below), and for each:

1. clears every render record of `[0x022C6F28]` (`0x740` bytes each, chained by the word `+4`) whose
   decoded `+0x68`, `+0xE0`, `+0xF8`, `+0x42C`, `+0x430` or `+0x390` is the source;
2. cancels the entry's ticket when `+0x44` is not −1 (`0x003B37E0`; a 0 there matches no ticket);
3. resets the entry (`0x00409730`);
4. removes the slot (`0x0051FCF0`); when that empties the slot's page, `0x0051F880` unlinks the page from the
   bank's page list and resets it.

`0x00409CA0(bank, tag, name)` runs the same steps 2 to 4 for every entry that holds a section with that tag
and name (`0x0051FE30` with the test `0x0040A1E0`, which asks `0x00409A30`); `0x00504C40` uses it to drop the
`@FDM` entries of an object. `0x00409FE0`'s lookup for an existing entry uses the same test.

The source test `0x004095B0(entry, source)`, passed through its thunk `0x0040A200`, compares by the entry's mode
`+0x04`: a mode-0 entry holds the source when its decoded handle (`0x0051EE00(entry + 0x10)`) is the source, a
mode-1 entry when its raw handle `+0x30` is, and any other mode never. `0x00409FD0(bank, source)` runs one search
with it and returns the entry's slot or −1; the motion start `0x00424D80` asks it for the manager's bank
`+0xD90` (`0x004250CC`).

`0x003B37E0(id)` acts only when the slot's whole id matches, so a stale id does nothing. It sets the
ticket `+0x30` to −1, then:

- detaches the context's effect instances (`0x0024F4D0`): each instance in the type's list that points
  to the context (`+0x340`) is unlinked, its three substructures are released, its deferred block
  `+0x380` is queued (256 entries at `0x02091950`; when full it goes to `0x00182CA0`), and the instance is
  freed;
- frees the context (`0x0024F410`): unlinks it, releases its five tables, among them `0x003A9600` (`+0x848`)
  and `0x003A9950` (`+0x850`), runs `0x0024F4D0` again and frees the `0x890` bytes; `0x02F97340` may be
  left pointing at it;
- recycles the instance handles that carry the ticket (`0x003B39E0`, the 32 records at `0x02EBD480`);
- puts the ticket back on the free list with its slot bits and top nibble only.

`0x003A9600` and `0x003A9950` depend on the context's byte `+3` bit `0x1`. When it is set they free the
run origin (`+0x870` or `+0x878`) only if the context copied the run. When it is clear they free every
non-null table entry from index 1, whatever the borrow flag. Either way they then free the table.
`0x003A7D30` releases the `+0x840` table the same way, except that with the bit clear it frees all 128
entries from index 0, and with it set it frees the block at `+0x880`.

`0x004096F0(entry)` returns an entry's source: the copy's data for mode 0 (`0x006B5C70`), the handle
`+0x30` for mode 1, and 0 for any other mode.

`0x00409730(entry)` calls `0x00427B00` with the entry's `+0x30`, which clears the render records'
`+0x68` (and `+0x69C`), `+0xD8`/`+0xE0` and `+0xF0`/`+0xF8` that decode to it, then releases the
inline buffer (`0x0051EE80`, which frees a mode 0 copy through `0x003AB7C0`) and resets `+0x00` to
`0xFFFF`, `+0x04`, `+0x30`, `+0x40` and `+0x44` (to −1). The cached pointer `+0x38` is not cleared. A
mode 1 source is not freed here; its loader frees it afterwards.

### After a source moves

Compaction can move a mode 1 source. Nothing that moves it repairs the effect data that borrows it.
`0x003B3C00(handle, n)`, which `0x003B8670` and `0x00427DE0` call to advance an instance by `n` steps
(`0x0024FE70`), first runs `0x003B3480`, which repairs a borrowing context against the source's new
address. The repair walks are on the
[arena page](resource-arena-and-relocation.md#repairing-effect-data-after-its-source-moves). The run
origins `+0x870` and `+0x878` are not in those walks.

## Layouts

```
bank entry (0x50)      +0x00 u16 slot (0xFFFF free), +0x04 u32 mode (0 copy, 1 retained),
                       +0x10 inline buffer (0x20: +0x08 data, +0x10 capacity, +0x14 growth, +0x18 used),
                       +0x30 source handle, +0x38 cached pointer, +0x40 u32 size, +0x44 s32 ticket (-1 none, 0 none free)
effect ticket (0x38)   0x02EBCD80 + slot*0x38: +0x00 u32 id, +0x08 source base, +0x18 context,
                       +0x20 next, +0x28 previous, +0x30 s32 effect number (-1 none)
instance handle (0x38) 0x02EBD480 + slot*0x38: +0x00 u32 id, +0x10 instance, +0x18 u32 ticket id, +0x20/+0x28 links
effect context (0x890) +0x00 u8 type, +0x02 u8 flags (bit 0x4 borrow), +0x03 u8 (bit 0x1 single-run tables),
                       +0x08 next, +0x10 previous, +0x840/+0x848/+0x850 tables, +0x858 source base,
                       +0x860 u32 source, +0x864 s32 offset, +0x870/+0x878 run origins
effect instance        +0x340 context, +0x348 next, +0x350 previous, +0x380 deferred block, +0x390 base copy
motion slot (0x1C)     0x02B581A0 + (g*16 + i)*0x1C: +0x00 handle, +0x04 state, +0x08 armer argument (0),
                       +0x0C u8 area slot, +0x0D u8 route (1 = arena 11), +0x0E u16 motion number, +0x10 s16 kind,
                       +0x12 s16 file index, +0x14 s32 length, +0x18 s32 offset
.mot header (0x88)     +0x00 u8 active, +0x08 + i*8: u32 offset, u32 length (i = 0..15)
```

The fields are listed access by access in
[`resource-ownership-entry-buffer-accesses.tsv`](resource-ownership-entry-buffer-accesses.tsv),
[`resource-ownership-motion-slot-accesses.tsv`](resource-ownership-motion-slot-accesses.tsv) and
[`resource-ownership-effect-context-list-accesses.tsv`](resource-ownership-effect-context-list-accesses.tsv).

## Shipped data

144 archive files have an `@FEF` section in an `@FRP` container, all of them `.cm` files under
`ps2data/obj_finish/`; no file has `@FEF` as its root.

## State

The bank at manager `+0xD90`, the 32 effect tickets and 32 instance handles with their lists and
counter, the context lists `0x020910A0`, the current context `0x02F97340`, and the 80 motion slots with
their five pending masks at `0x02B58A60`.

## Modding notes

- Two sources with the same tag and name share one bank entry: the first one registered wins, and
  later ones are never parsed.
- At most 32 effect tickets exist at once; a further `@FEF` registration stores ticket 0 and gets no
  effect context.
- Every `.cm` file with an `@FEF` section needs a non-NULL entry in the `0x02B64380` table for its name,
  or loading it ends the game.
- `motionread` loads only motions 0–15 of area slots 0–3, from the offsets in the first `0x88` bytes of
  the area's `.mot`; give each a length of at least 1.
- Call `motiondispose` before reusing a motion number: `motionread` does nothing unless the slot is
  idle.

## Related

- [Resource arenas and relocation](resource-arena-and-relocation.md): handles, pins, the movable tree and the repair walks.
- [Resource sections](resource-sections.md): the `@FRP` container and section lookup.
- [File requests and the read queue](file-requests-and-the-read-queue.md): how a −1 size completes.
- [File size tables](file-size-tables-fst.md): the file kinds the motion slots read.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): the binding entries and lanes that register here.
