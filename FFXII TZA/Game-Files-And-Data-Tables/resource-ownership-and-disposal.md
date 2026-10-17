---
title: "Resource ownership and disposal: who owns a loaded source, copy or borrow, effect tickets and contexts, the script motion slots, borrowed views, and the order things are torn down"
kind: "system"
category: "Game files and data tables"
addresses: "0041E580, 0041E490, 00409FE0, 00409A60, 00409730, 00409D60, 00409960, 00409C00, 00427B00, 003B3160, 003B38B0, 003B37E0, 003B39E0, 003B3B10, 003B3C00, 0024B3A0, 0024F410, 0024F4D0, 003A9600, 003A9950, 003A9730, 003A9A70, 003EDAD0, 003AB880, 003AB940, 003AB7C0, 00369800, 02EBCD80, 02EBD480, 020910A0, 02F97340, 02B64380, 02B581A0, 02B58A60, 003DDA20, 003DD4C0, 003DDA70, 003DD850, 003DD420, 003DD380, 003DD740, 003DD770, 003492A0, 003499C0, 0034A6A0, 0032F240, 0032F170, 0032F290, 0032F260, 00267310, 002E4D20, 002E4E50, 003DC340, 003DC5B0, 0032E620, 0041FCF0, 00409CA0, 0040A1E0, 003A7D30, 004096F0, 0051F880, 005371C0, 00537270"
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

Every loaded source that renders goes through one door: `0041E580(manager, source)` loads the bank at
`manager + D90h` and jumps to `00409FE0`. The manager is `[[022C6F28] + 48830h]` decoded with
`0020E600`. The bank holds `50`<sub>h</sub>-byte entries (layout below).

`00409FE0` first looks for an entry with the same tag and name. A match returns that entry unchanged:
its source is not replaced and its data is not parsed again. Otherwise it takes a new slot and fills
it with `00409A60`, which picks the mode from the source value (`003AB860`):

- **Mode 0, owned copy** (an untagged pointer): the entry reserves a buffer of the size in the
  source's header `+8`, copies the bytes into it, and from then on uses only the copy (`+10`<sub>h</sub>). The
  caller still owns the original.
- **Mode 1, retained source** (a tagged handle): the entry stores the handle at `+30`<sub>h</sub> and the
  resolved pointer at `+38`<sub>h</sub> and copies nothing. The bytes stay owned by whoever allocated them.

Both modes pad the root and child section names to 32 bytes inside the input before the split, so
the input is written to either way.

### Effect sections and tickets

When the source is an `@FRP` container with an `@FEF` section (`00409A30`), `00409FE0` also makes an
effect ticket. It looks up a configuration pointer in the table at `02B64380`, indexed by the source
entry name's last five characters: the letter's code × `500`<sub>h</sub> plus the four digits as a number. A NULL entry writes to
address 0 and ends the game. It then calls `003B38B0(source, offset)` with the section offset from the
footer, and for a name containing `chara\h` it parses `%d.efx` and stores the number in the ticket
(`003B3B10`; −1 when it does not parse).

The tickets are 32 records of `38`<sub>h</sub> bytes at `02EBCD80` (`003B3160` builds them at start-up), with a
free list (`02EBDB88`) and an in-use list (`02EBDB80` head, `02EBDB90` tail). A ticket id is the slot
in bits 0–5, a 22-bit counter (`02EBDBB0`) in bits 6–27 and 3 in bits 28–31, so a recycled slot gets a
new id.

The record is found by the id's low six bits; an id with slot bits 32–63 would land in the
instance-handle records at `02EBD480`, which follow the tickets, but no ticket id has them.
`003B38B0` returns 0 with no context when the free list is empty, and `00409FE0` stores that 0 in the
entry's `+44`<sub>h</sub> (`0040A17C`). Otherwise it:

1. resolves the source (`003AB7F0`) and adds the offset;
2. fills a stack template: type 3, flags `+2` `|= 0Ch`, the resolved base at `+858`<sub>h</sub>, the source
   at `+860`<sub>h</sub> and the offset at `+864`<sub>h</sub>;
3. builds the context with `0024B3A0` and stores it in the ticket `+18`<sub>h</sub>;
4. parses the effect data with `003EDAD0(base, dword [base + 0Ch])`.

### Effect contexts

`0024B3A0(template)` allocates `890`<sub>h</sub> bytes, copies the template, links the copy at the head of the
list `020910A0[type]`, clears `+870`<sub>h</sub>..`+888`<sub>h</sub>, makes it current (`02F97340`) and builds its lookup
tables, among them the 320-slot `+848`<sub>h</sub> table and the 768-slot `+850`<sub>h</sub> table. Its other callers are
`0026FB90` (type 2, also flags `|= 0Ch`), `002FC4A0` (type 1), `003B0660`, `003B2220` (type 7) and
`003B29B0`.

Flag bit `4`<sub>h</sub> decides whether the context borrows or copies its two large runs of effect records.
At `003EE018` and `003EE117` `003EDAD0` tests it:

- **Clear (copy):** allocate the run in arena 8 and copy it, the length truncated toward zero to a
  multiple of 16; the copy goes to `+878`<sub>h</sub> or `+870`<sub>h</sub>.
- **Set (borrow):** store the input pointer itself at `+878`<sub>h</sub> or `+870`<sub>h</sub>.

A borrowed run is written in place. Each record starts with a `u16` id and a subtype byte, followed by
its payload. `003A9730` copies them into the payload at `+280`<sub>h</sub> and `+282`<sub>h</sub> and stores the payload's
address in the `+848`<sub>h</sub> table at the id; `003A9A70` does the same at `+42`<sub>h</sub> and `+44`<sub>h</sub> with the
`+850`<sub>h</sub> table. Both then relocate the payload's stored offsets. For a mode 0 entry this rewrites the bank's copy; for a
mode 1 entry it rewrites the original source.

### The four loaders that register sources

`0041E580` has four callers, each a read completion:

| Loader | Completion | Size test before the read |
|---|---|---|
| script name-binding entries | `002E4D20` | positive size only |
| script name-binding lanes | `002E4E50` | positive size only |
| script motion slots | `003DD850` | length of at least 1 |
| motion cache | `003DC340` | none: `003DC5B0` files whatever size `003DC8D0` returns, −1 included |

Each reads into a block it owns and registers that block, so a registration always sees freshly read
bytes. A −1 size completes as delivered (see the read queue page), so only the motion cache can reach
registration without a read: when `003DC8D0` (sixteen cached sizes at `02B580B0`) gets a negative
index or size it returns −1 and sets a failure flag that `003DC5B0` ignores, and the completion then
registers a block nothing was read into.

### Script motion slots

`motionread` (`00A2`<sub>h</sub>, `003492A0`), `motionreadsync` (`00A3`<sub>h</sub>, poll `003499C0`) and `motiondispose`
(`00A4`<sub>h</sub>, `0034A6A0`) work on 80 records of `1C`<sub>h</sub> bytes at `02B581A0`, five area slots of sixteen.
The area slot is the running script's (`[[02099D70] + 28h]`), the motion number is the verb argument.
A record moves through these states (`+04`<sub>h</sub>):

| State | Meaning | Entered by |
|---|---|---|
| 0 | idle | reset, a failed sweep, a completed dispose |
| 2 | armed | `003DDA20`, from state 0 only, also sets bit `i` of `02B58A60[g]` |
| 1 | allocated but held; never read | the sweep, when the area slot's hold byte `02099011 + g × 288h` is set |
| 3 | read in flight | `003DDA70` |
| 4 | registered | the completion `003DD850` |
| 5 | dispose requested while in flight | `003DD420` on state 3 |

The sweep `003DD4C0` runs over every record with its pending bit and state 2:

1. The area slot's file comes from `0032F240` (enable byte `022C6D18 + g`, selector `022C6D28 + 4g`)
   and `0032F170`: kind 5, index `3s` for slot 0; kind 8, index `4s` for slots 1–3; kind 1, index
   `s + 6Bh` for slot 4. The motion is read from index + 1, the area's `.mot`.
2. The offset and length come from the first `88`<sub>h</sub> bytes of that `.mot`, which the area loader keeps
   at `022C6E70[g]`: byte 0 is an active flag, then sixteen `{u32 offset, u32 length}` pairs from `+8`
   (`0032F260`, `0032F290`). Area slot 4 and an inactive header give −1, so slot 4 never loads.
3. It allocates the length in arena 6, or first in arena 11 when `0037B330()` is 2 and the area slot's
   byte `+17`<sub>h</sub> has bit `40`<sub>h</sub> (route byte `+0D`<sub>h</sub> = 1; `0037B330` answers only 0 or 4, so this
   route is never taken), pins the block and stores the handle, length,
   offset, kind and index + 1.
4. A held area slot goes to state 1; otherwise `003DDA70` files the read (`0032E620`) with the record's
   address as the callback argument and sets state 3 without checking the result.

Any failure sets state 0 and leaves the pending bit, and the next sweep skips the record until it is
armed again. `motionreadsync` waits while the state is 2 or 3 (`003DD770`).

A read that fails calls no completion, because the queue's failure callback needs a −1 byte count and
these reads never file one. The record then stays in state 3: `motionreadsync` waits for good,
`motionread` cannot re-arm it, a dispose only sets state 5, and the pinned block is never freed.

The completion `003DD850` unpins the block first. In state 5 it releases the bank entries for it
(`0041E490`), frees the block (`00369800`) and sets state 0, leaving the old handle in the record.
Otherwise it registers the block (`0041E580`) and sets state 4, whatever the registration returned.
`003DD740` returns the handle only in state 4.

`motiondispose` (`003DD420`) and the area unload `002628B0` through `003DD380` (all sixteen of one area
slot) act by state:

- state 1: free the block and clear its handle, state and route;
- state 3: set state 5 and let the completion finish it;
- state 4: release the bank entries (`0041E490`), free the block and clear its handle, state and
  route;
- states 0, 2 and 5: nothing.

An armed record (state 2) survives the unload with its pending bit, and the next sweep takes the file
from whatever area the slot then holds, so the motion is read from the next area's `.mot`.

### Borrowed views

`00409960(entry, tag, name)` returns a pointer into an entry's data: the section offset from
`00409780` (0 when the section is absent) added to the entry's base. A mode 0 entry resolves its copy
(`0051EE30`, `006B5C70`); a mode 1 entry pins its source with `003AB880`, which takes the block out of
the movable tree so compaction cannot move it. The sum is `low32(base) + offset` sign-extended.

`00409C00(entry)` ends the view: `0051EF80` for mode 0, `003AB940` for mode 1. The pin is a flag, not
a count: one release ends every pin on the block. The only user is `0041FCF0`, which opens a view at
`0041FFA0` and ends it at `0041FFF8`.

`005371C0(array, fn, first)` uses the same view on a strided array (stride `+20`<sub>h</sub>, count `+24`<sub>h</sub>): it
opens it (`0051EE30`, `006B5C70`), calls `fn` on `count - first` elements counted from element 0,
not from `first`, and ends it (`0051EF80`). Its one caller `00537270(array, stride, count, fn)` sizes
the array (`0051F020`), stores the stride and count, and runs it with `first` 0 when `fn` is set.

### Disposal order

`0041E490(manager, source)` pins and unpins the source once, then calls `00409D60(manager + D90h,
source)`. `00409D60` loops while the bank finds an entry for the source (`0051FE30` with the test `004095B0`,
below), and for each:

1. clears every render record of `[022C6F28]` (`740`<sub>h</sub> bytes each, chained by the word `+4`) whose
   decoded `+68`<sub>h</sub>, `+E0`<sub>h</sub>, `+F8`<sub>h</sub>, `+42C`<sub>h</sub>, `+430`<sub>h</sub> or `+390`<sub>h</sub> is the source;
2. cancels the entry's ticket when `+44`<sub>h</sub> is not −1 (`003B37E0`; a 0 there matches no ticket);
3. resets the entry (`00409730`);
4. removes the slot (`0051FCF0`); when that empties the slot's page, `0051F880` unlinks the page from the
   bank's page list and resets it.

`00409CA0(bank, tag, name)` runs the same steps 2 to 4 for every entry that holds a section with that tag
and name (`0051FE30` with the test `0040A1E0`, which asks `00409A30`); `00504C40` uses it to drop the
`@FDM` entries of an object. `00409FE0`'s lookup for an existing entry uses the same test.

The source test `004095B0(entry, source)`, passed through its thunk `0040A200`, compares by the entry's mode
`+04`<sub>h</sub>: a mode-0 entry holds the source when its decoded handle (`0051EE00(entry + 10h)`) is the source, a
mode-1 entry when its raw handle `+30`<sub>h</sub> is, and any other mode never. `00409FD0(bank, source)` runs one search
with it and returns the entry's slot or −1; the motion start `00424D80` asks it for the manager's bank
`+D90`<sub>h</sub> (`004250CC`).

`003B37E0(id)` acts only when the slot's whole id matches, so a stale id does nothing. It sets the
ticket `+30`<sub>h</sub> to −1, then:

- detaches the context's effect instances (`0024F4D0`): each instance in the type's list that points
  to the context (`+340`<sub>h</sub>) is unlinked, its three substructures are released, its deferred block
  `+380`<sub>h</sub> is queued (256 entries at `02091950`; when full it goes to `00182CA0`), and the instance is
  freed;
- frees the context (`0024F410`): unlinks it, releases its five tables, among them `003A9600` (`+848`<sub>h</sub>)
  and `003A9950` (`+850`<sub>h</sub>), runs `0024F4D0` again and frees the `890`<sub>h</sub> bytes; `02F97340` may be
  left pointing at it;
- recycles the instance handles that carry the ticket (`003B39E0`, the 32 records at `02EBD480`);
- puts the ticket back on the free list with its slot bits and top nibble only.

`003A9600` and `003A9950` depend on the context's byte `+3` bit `1`<sub>h</sub>. When it is set they free the
run origin (`+870`<sub>h</sub> or `+878`<sub>h</sub>) only if the context copied the run. When it is clear they free every
non-null table entry from index 1, whatever the borrow flag. Either way they then free the table.
`003A7D30` releases the `+840`<sub>h</sub> table the same way, except that with the bit clear it frees all 128
entries from index 0, and with it set it frees the block at `+880`<sub>h</sub>.

`004096F0(entry)` returns an entry's source: the copy's data for mode 0 (`006B5C70`), the handle
`+30`<sub>h</sub> for mode 1, and 0 for any other mode.

`00409730(entry)` calls `00427B00` with the entry's `+30`<sub>h</sub>, which clears the render records'
`+68`<sub>h</sub> (and `+69C`<sub>h</sub>), `+D8`<sub>h</sub>/`+E0`<sub>h</sub> and `+F0`<sub>h</sub>/`+F8`<sub>h</sub> that decode to it, then releases the
inline buffer (`0051EE80`, which frees a mode 0 copy through `003AB7C0`) and resets `+00`<sub>h</sub> to
`FFFF`<sub>h</sub>, `+04`<sub>h</sub>, `+30`<sub>h</sub>, `+40`<sub>h</sub> and `+44`<sub>h</sub> (to −1). The cached pointer `+38`<sub>h</sub> is not cleared. A
mode 1 source is not freed here; its loader frees it afterwards.

### After a source moves

Compaction can move a mode 1 source. Nothing that moves it repairs the effect data that borrows it.
`003B3C00(handle, n)`, which `003B8670` and `00427DE0` call to advance an instance by `n` steps
(`0024FE70`), first runs `003B3480`, which repairs a borrowing context against the source's new
address. The repair walks are on the
[arena page](resource-arena-and-relocation.md#repairing-effect-data-after-its-source-moves). The run
origins `+870`<sub>h</sub> and `+878`<sub>h</sub> are not in those walks.

## Layouts

```
bank entry (0x50)      +0x00 u16 slot (0xFFFF free), +0x04 u32 mode (0 copy, 1 retained),
                       +0x10 inline buffer (0x20: +0x08 data, +0x10 capacity, +0x14 growth, +0x18 used),
                       +0x30 source handle, +0x38 cached pointer, +0x40 u32 size, +0x44 s32 ticket (-1 none, 0 none free)
effect ticket (0x38)   02EBCD80 + slot*0x38: +0x00 u32 id, +0x08 source base, +0x18 context,
                       +0x20 next, +0x28 previous, +0x30 s32 effect number (-1 none)
instance handle (0x38) 02EBD480 + slot*0x38: +0x00 u32 id, +0x10 instance, +0x18 u32 ticket id, +0x20/+0x28 links
effect context (0x890) +0x00 u8 type, +0x02 u8 flags (bit 0x4 borrow), +0x03 u8 (bit 0x1 single-run tables),
                       +0x08 next, +0x10 previous, +0x840/+0x848/+0x850 tables, +0x858 source base,
                       +0x860 u32 source, +0x864 s32 offset, +0x870/+0x878 run origins
effect instance        +0x340 context, +0x348 next, +0x350 previous, +0x380 deferred block, +0x390 base copy
motion slot (0x1C)     02B581A0 + (g*16 + i)*0x1C: +0x00 handle, +0x04 state, +0x08 armer argument (0),
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

The bank at manager `+D90`<sub>h</sub>, the 32 effect tickets and 32 instance handles with their lists and
counter, the context lists `020910A0`, the current context `02F97340`, and the 80 motion slots with
their five pending masks at `02B58A60`.

## Modding notes

- Two sources with the same tag and name share one bank entry: the first one registered wins, and
  later ones are never parsed.
- At most 32 effect tickets exist at once; a further `@FEF` registration stores ticket 0 and gets no
  effect context.
- Every `.cm` file with an `@FEF` section needs a non-NULL entry in the `02B64380` table for its name,
  or loading it ends the game.
- `motionread` loads only motions 0–15 of area slots 0–3, from the offsets in the first `88`<sub>h</sub> bytes of
  the area's `.mot`; give each a length of at least 1.
- Call `motiondispose` before reusing a motion number: `motionread` does nothing unless the slot is
  idle.

## Related

- [Resource arenas and relocation](resource-arena-and-relocation.md): handles, pins, the movable tree and the repair walks.
- [Resource sections](resource-sections.md): the `@FRP` container and section lookup.
- [File requests and the read queue](file-requests-and-the-read-queue.md): how a −1 size completes.
- [File size tables](file-size-tables-fst.md): the file kinds the motion slots read.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): the binding entries and lanes that register here.
