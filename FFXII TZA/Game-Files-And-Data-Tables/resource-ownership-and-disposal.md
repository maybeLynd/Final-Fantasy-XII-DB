[Home](../../README.md) / [Game files and data tables](README.md) / Resource ownership and disposal

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Resource ownership and disposal: who owns a loaded source, copy or borrow, effect tickets and contexts, the script motion slots, borrowed views, and the order things are torn down | system | Game files and data tables | Loaded resources | How the game keeps track of who owns loaded data: the render resource bank and its two entry modes (an owned copy or a retained external source), the effect tickets and 0x890-byte effect contexts that borrow or copy effect data, the four loaders that register sources, the 80 script motion slots behind motionread, motionreadsync and motiondispose and their states, borrowed section views, and the fixed order in which consumers, tickets, entries and backing memory are released. | 0x0041E580, 0x0041E490, 0x00409FE0, 0x00409A60, 0x00409730, 0x00409D60, 0x00409960, 0x00409C00, 0x00427B00, 0x003B3160, 0x003B38B0, 0x003B37E0, 0x003B39E0, 0x003B3B10, 0x003B3C00, 0x0024B3A0, 0x0024F410, 0x0024F4D0, 0x003A9600, 0x003A9950, 0x003A9730, 0x003A9A70, 0x003EDAD0, 0x003AB880, 0x003AB940, 0x003AB7C0, 0x00369800, 0x02EBCD80, 0x02EBD480, 0x020910A0, 0x02F97340, 0x02B64380, 0x02B581A0, 0x02B58A60, 0x003DDA20, 0x003DD4C0, 0x003DDA70, 0x003DD850, 0x003DD420, 0x003DD380, 0x003DD740, 0x003DD770, 0x003492A0, 0x003499C0, 0x0034A6A0, 0x0032F240, 0x0032F170, 0x0032F290, 0x0032F260, 0x00267310, 0x002E4D20, 0x002E4E50, 0x003DC340, 0x003DC5B0, 0x0032E620, 0x0041FCF0, 0x00409CA0, 0x0040A1E0, 0x003A7D30, 0x004096F0, 0x0051F880, 0x005371C0, 0x00537270 |

## What the player sees

Character motions, effects and script-loaded animation sets appear when their data has loaded and
vanish cleanly when the scene that loaded them is unloaded. An event script that calls `motionread`
waits in `motionreadsync` while the motion record is armed or its read is in flight, plays the
animation set, and frees it with `motiondispose`. The wait also ends when the read was held back or
could not be set up, so its end alone does not mean the set loaded ([Script motion slots](#script-motion-slots)).

Underneath, every loaded block has exactly one owner that frees it, and every
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

`0x00409FE0` first resolves the source (`0x003AB7F0`) and reads its first dword with no null test
(`0x0040A005`), so a source that resolves to 0 faults. It then looks for an entry with the same tag and
name (`0x0051FE30` with the test `0x0040A1E0`, `0x0040A01B`). A match returns that entry's slot unchanged:
its source is not replaced and its data is not parsed again.

Otherwise it takes a new slot (`0x0051FBB0`; with no free slot it returns that call's −1 and registers
nothing, `0x0040A03D`), resets the entry (`0x00409710`: `+0x00` to `0xFFFF` and `+0x44` to −1, `+0x04`,
`+0x30` and `+0x40` to 0, the inline buffer set up with `0x0051EE10`) and fills it with `0x00409A60`,
which picks the mode from the source value (`0x003AB860`: 0 for a null value or one with its low two
bits clear, 1 otherwise). It then writes the slot number to `+0x00` (`0x0040A0A1`):

- **Mode 0, owned copy** (an untagged pointer): the entry reserves a buffer of the size in the
  source's header `+8`, copies the bytes into it, and from then on uses only the copy (`+0x10`). The
  caller still owns the original. `0x00409A60` wraps the copy in `0x003AB880` and `0x003AB940`, which pass
  an untagged pointer through and pin nothing; when the buffer is not reserved it copies nothing
  (`0x00409BCA`).
- **Mode 1, retained source** (a tagged handle): the entry stores the handle at `+0x30` (`0x00409B9E`)
  and the resolved pointer at `+0x38` (`0x00409FE0` stores it, `0x0040A08F`) and copies nothing. The bytes
  stay owned by whoever allocated them.

`0x00409A60(entry, source, mode)` resolves the source first (`0x003AB7F0`); a source that resolves to 0
returns 0 with the entry's mode left unset (`0x00409A85`). Otherwise it stores the mode at `+0x04`, and in
both modes it stores the header's size `+8` at `+0x40` and returns it (`0x00409BE4`-`0x00409BF1`).

Both modes pad the root and child section names to 32 bytes inside the input before the split, so
the input is written to either way. The root name at `+0x10` is always padded (`0x00409AC5`); child
names only in an `@FRP` container (`0x00409ACA`): `count` `+0x0C` of them, through the table at `+0x30`
for version 0 or at `+0x40` for version 1, which skips zero entries (`0x00409B04`). Each child address
is a 32-bit sum (`0x00409B50`-`0x00409B53`, `0x00409B06`-`0x00409B09`).

### Effect sections and tickets

When the source is an `@FRP` container with an `@FEF` section, or is itself one (no shipped file is),
`0x00409FE0` also makes an effect ticket. The section is looked up with `0x00409A30` by the tag `@FEF` and
the root's own name `+0x10` (`0x0040A0A4`-`0x0040A0AC`); without one it returns the slot (`0x0040A0B4`). It
looks up a configuration pointer in the table at `0x02B64380`, indexed by the source entry name's last
five characters: the letter's code × `0x500` plus the four digits as a number (`0x0040A0C0`-`0x0040A12C`).
A NULL entry writes to address 0 and ends the game.

It then calls `0x003B38B0(source, offset)` with the section offset from the footer, not the offset
`0x00409A30` found: the dword of the resolved source at `size − 4`, with `size` the file size that
`0x002DF960` gives for the binding id at `0x021641FC` (`0x002E9770`, `0x002E98F0`; the binding-entry
completion `0x002E4D20` stores that id before it registers) rounded up to a multiple of 64, `(s + 63) & ~63`
for a file size `s` of 0 or more (`add eax, 0x3f`, `cdq`, `and edx, 0x3f`, `and eax, 0xffffffc0`,
`0x0040A13C`-`0x0040A16F`; a negative sum gets 63 more before the mask).

The offset is then `dword [source + size - 4]` (`0x0040A16F`). The source it passes is the low 32 bits of the
copy's data pointer `+0x18` for a mode 0 entry and of the handle for mode 1 (`0x0040A073`, `0x0040A162`).

For a name containing `chara\h`, the character-effect path that `0x001D6EC0` returns for the table's
path (`0x0040A17F`), it parses `%d.efx` after it and stores the number in the ticket (`0x003B3B10`; −1 when
it does not parse); with no such path or no `chara\h` in it the ticket's number is not written
(`0x0040A187`, `0x0040A19C`). It returns the slot (`0x0040A1C9`).

The tickets are 32 records of `0x38` bytes at `0x02EBCD80`, with a free list (`0x02EBDB88`) and an in-use
list (`0x02EBDB80` head, `0x02EBDB90` tail). `0x003B3160` builds them at start-up under arena 8 together with
the 32 instance handles at `0x02EBD480`: each record zeroed, its id `0x30000000 | slot`, chained through
`+0x20` (next) and `+0x28` (previous) into its table's free list, both in-use lists empty and both
counters 0; it ends with `0x0024C550(3)` (`0x003B3164`-`0x003B32A4`,
[character effects](../Graphics/character-effects.md#two-tables-of-32-records)).

A ticket id is the slot in bits `0x3F`, a 22-bit counter (`0x02EBDBB0`) in the bits under mask
`0xFFFFFC0` and 3 in the bits under mask `0xF0000000`, so a recycled slot gets a new id.

The record is found by the id's low six bits, `0x02EBCD80 + 0x38 × (id & 0x3F)` (`0x003B33D2`, `0x003B37EE`,
`0x003B3B12`). An id whose slot bits hold 32 or more would land in the instance-handle records at `0x02EBD480`, which
follow the tickets, but every ticket id carries a slot below 32.
`0x003B38B0` returns 0 with no context when the free list is empty, and `0x00409FE0` stores that 0 in the
entry's `+0x44` (`0x0040A17C`). Otherwise it:

1. resolves the source (`0x003AB7F0`) and adds the offset;
   - it does this before the free-list test, and the whole call runs under arena 8: `0x0036C1D0(8, 10)` first and
     `0x0036C140` on both paths (`0x003B38D0`-`0x003B38E1`, `0x003B38F2`, `0x003B39B8`);
   - it pops the free head, links the ticket to the in-use tail `0x02EBDB90`, raises the counter `0x02EBDBB0` into
     the id's counter bits, stores the resolved address at the ticket's `+0x08` and zeroes `+0x10`
     (`0x003B38FE`-`0x003B396E`);
2. fills a stack template: type 3, flags `+2` `|= 0x0C`, the resolved base at `+0x858`, the source
   at `+0x860` and the offset at `+0x864`, and the ticket id's low 16 bits at `+0x04` (`0x003B3977`-`0x003B399C`);
3. builds the context with `0x0024B3A0` and stores it in the ticket `+0x18`;
4. parses the effect data with `0x003EDAD0(base, dword [base + 0x0C])`.

### Effect contexts

`0x0024B3A0(template)` returns 0 for a null template (`0x0024B3AC`). Otherwise it allocates `0x890` bytes
(`0x0036A100`), copies the template, links the copy at the head of the list `0x020910A0[type]` (its
`+0x08` takes the old head, the old head's `+0x10` takes the copy, its own `+0x10` is zeroed), clears
`+0x870`..`+0x888`, makes it current (`0x02F97340`) and builds its lookup tables, among them the
320-slot `+0x848` table and the 768-slot `+0x850` table, and returns the context.

The five builders are `0x003A9CC0` (`+0x18`), `0x003A76F0` (`+0x38`), `0x003A7D00` (`+0x840`), `0x003A9560`
(`+0x848`, `0xA00` zero-filled bytes) and `0x003A9920` (`+0x850`, `0x1800` zero-filled bytes); before
each it publishes the field's address in `0x02EBEF70`, `0x02EBEFA8`, `0x02EBEFA0`, `0x02EBEF90` or `0x02EBEF78`
(`0x0024B47E`-`0x0024B4CE`). Its other callers are `0x0026FB90` (type 2, also flags `|= 0x0C`), `0x002FC4A0`
(type 1), `0x003B0660`, `0x003B2220` (type 7) and `0x003B29B0`.

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
| motion cache | `0x003DC340`: sets the entry's state byte `+0x06` to 3, puts the block back in the movable tree (`0x0036D170`) and jumps to `0x0041E580` (`0x003DC34A`-`0x003DC371`) | no test: `0x003DC5B0` files whatever size `0x003DC8D0` returns, −1 included |

Each reads into a block it owns and registers that block, so a registration always sees freshly read
bytes. A −1 size completes with the previous read's status, and the completion runs either way: the delivery
callback calls it, and so does the failure callback for a byte count of −1 (see the read queue page). So only
the motion cache can reach registration without a read: when `0x003DC8D0` (sixteen cached sizes at `0x02B580B0`)
gets a negative index or size it returns −1 and sets a failure flag that `0x003DC5B0` ignores, and the
completion then registers a block nothing was read into.

`0x003DC5B0` acts only on an entry whose state byte `+0x06` is 1 (`0x003DC5B9`) and sets it to 2 once it has filed
(`0x003DC692`). It takes the kind and index from `0x003DCA30` and the size from `0x003DC8D0`, both over the entry's
`+0x0C`, `+0x10` and `+0x12` (`0x003DC5EA`, `0x003DC60D`). Under arena 6 (`0x0036C1D0(6, 5)` and `0x0036C1A0(5)`, then
`0x0036C140` and `0x0036C110`) it allocates a handle block of that size (`0x0036B160`), keeps the handle at `+0x00`
(`0x003DC634`) and takes the handle's payload (`0x0036A000`) as the destination.

The request (`0x0032E620`, `0x003DC683`) carries the size as it came, offset 0, the low 32 bits of the entry's
address as the callback word and `0x003DC340` as its delivery and failure callback, with no cancel callback.
`0x003DC340` does not read the flag it is given, so a failed read reaches registration too.

### Script motion slots

`motionread` (`0x00A2`, `0x003492A0`), `motionreadsync` (`0x00A3`, poll `0x003499C0`) and `motiondispose`
(`0x00A4`, `0x0034A6A0`) work on 80 records of `0x1C` bytes at `0x02B581A0`, five manager slots of sixteen.
The [manager slot](../Characters-And-Objects/actor-managers.md#the-slot-array) is the running script's
(`[[0x02099D70] + 0x28]`), the motion number is the verb argument. `motionread` arms the record with
`0x003DDA20(slot, number, 0)`, drops its result, and raises the loading flag `0x022C253D` through
`0x00314D40(1)` (`0x003492C5`, `0x003492D9`).
A record moves through these states (`+0x04`):

| State | Meaning | Entered by |
|---|---|---|
| 0 | idle | reset, a failed sweep, a completed dispose |
| 2 | armed | `0x003DDA20`, from state 0 only, also sets bit `i` of `0x02B58A60[g]` |
| 1 | allocated but held; never read | the sweep, when the manager slot's hold byte `0x02099011 + g × 0x288` is set |
| 3 | read in flight | `0x003DDA70` |
| 4 | registered | the completion `0x003DD850` |
| 5 | dispose requested while in flight | `0x003DD420` on state 3 |

The sweep `0x003DD4C0` runs over every record with its pending bit and state 2:

1. The manager slot's file comes from `0x0032F240` (enable byte `0x022C6D18 + g`, selector `0x022C6D28 + 4g`)
   and `0x0032F170`: kind 5, index `3s` for slot 0; kind 8, index `4s` for slots 1–3; kind 1, index
   `s + 0x6B` for slot 4. The motion is read from index + 1, the area's `.mot`.
2. The offset and length come from the first `0x88` bytes of that `.mot`, which the area loader keeps
   at `0x022C6E70[g]`: byte 0 is an active flag, then sixteen `{u32 offset, u32 length}` pairs from `+8`
   (`0x0032F260`, `0x0032F290`). Manager slot 4 and an inactive header give −1, so slot 4 never loads.
3. It allocates the length in arena 6, or first in arena 11 when `0x0037B330()` is 2 and the manager slot's
   byte `+0x17` has bit `0x40` (route byte `+0x0D` = 1; `0x0037B330` answers only 0 or 4, so this
   route is never taken; a failed arena 11 allocation falls back to arena 6, `0x003DD5B3`).
4. It pins the block (`0x0036A000`), moves it to accounting group 1 (`0x0036C620`) and stores the handle,
   length, offset, kind and index + 1 (`0x003DD5EA`-`0x003DD62C`).
5. A held manager slot (`0x00267310`) goes to state 1; otherwise `0x003DDA70` files the read (`0x0032E620`)
   with the record's address as the callback argument and sets state 3 without checking the result.
   Either way the sweep clears the pending bit and stores the route byte (`0x003DD665`, `0x003DD672`).

`0x003DDA70` passes `0x0032E620` the kind `+0x10`, the file index `+0x12`, the block's address from
`0x0036B130`, the length `+0x14` and a request that holds the offset `+0x18`, the record's low 32 bits
and the completion `0x003DD850` (`0x003DDA7B`-`0x003DDAB9`).

Any failure sets state 0 and route byte 0 and leaves the pending bit. A record with its pending bit in
any state other than 2 is passed over with only its route byte set to 0 (`0x003DD533`, `0x003DD665`), so
the next sweep skips a failed record until it is armed again.

`motionreadsync` waits while the state is 2 or 3 (`0x003DD770`). Its poll raises the loading flag
`0x022C253D` on every call (`0x003499E0`); in state 2 or 3 it counts the wait in the poll's third dword and
returns 1 (`0x003499ED`), and in any other state it returns 0, which ends the wait (`0x00349A21`; the
`0x0053DD10` test before it always passes).

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
`0x00409780` added to the entry's base. It returns 0 for a null entry (`0x00409975`), and 0 without
opening a view when `0x00409780` gives the offset −1 of an absent section (`0x004099B6`).

A mode 0 entry resolves its copy (`0x0051EE30`, `0x006B5C70`); a mode 1 entry pins its source with
`0x003AB880`, which takes the block out of the movable tree so compaction cannot move it. An entry of
any other mode gets no section: `0x00409780` leaves the offset at −1 for a mode other than 0 or 1
(`0x004097AA`, `0x004097D7`-`0x004097E1`), so it returns 0 at `0x004099B6` and the arm that would add the offset to a
base of 0 (`0x004099C6`, `0x004099F8`) is never reached. The sum is
`low32(base) + offset` sign-extended.

`0x00409C00(entry)` ends the view: `0x0051EF80` for mode 0, `0x003AB940` for mode 1. The pin is a flag, not
a count: one release ends every pin on the block. The only user is `0x0041FCF0`, which opens a view at
`0x0041FFA0` and ends it at `0x0041FFF8`.

`0x005371C0(array, fn, first)` uses the same view on a strided array (stride `+0x20`, count `+0x24`): it
opens it (`0x0051EE30`, `0x006B5C70`), calls `fn` on `count - first` elements counted from element 0,
not from `first`, and ends it (`0x0051EF80`). With `first` at or above the count it calls nothing
(`0x00537217`); each next element is `low32(element + stride)` sign-extended (`0x00537225`-`0x00537228`).
Its one caller `0x00537270(array, stride, count, fn)` sizes the array (`0x0051F020`, `stride × count`
bytes), stores the stride and count, and runs it with `first` 0 when `fn` is set.

### Disposal order

`0x0041E490(manager, source)` pins and unpins the source once (`0x003AB880`, `0x003AB940`), then tail-jumps to
`0x00409D60(bank, source)` with the bank pointer that the manager holds at `+0xD90` (`0x0041E4B0`-`0x0041E4C4`).
`0x00409D60` loops while the bank finds an entry for the source (`0x0051FE30` with the test `0x004095B0`,
below), and for each:

1. clears, in every render record of `[0x022C6F28]` (`0x740` bytes each, chained by the word `+4`), each of
   the decoded `+0x68`, `+0xE0`, `+0xF8`, `+0x42C`, `+0x430` and `+0x390` that is the source;
   - the walk starts at the index in the dword `+0x48800` of `[0x022C6F28]` and is skipped when that
     pointer is null or the index is −1 (`0x00409DA0`-`0x00409DB9`);
   - a matching `+0x68` is zeroed as a qword with `+0x69C` set to the encoding of a null pointer,
     `+0xE0` and `+0xF8` are zeroed with `+0xD8` and `+0xF0`, and `+0x42C`, `+0x430` and `+0x390` each get
     the encoding of a null pointer (`0x00409DCA`-`0x00409E83`);
2. cancels the entry's ticket when `+0x44` is not −1 (`0x003B37E0`; a 0 there matches no ticket);
3. resets the entry (`0x00409730`);
4. removes the slot (`0x0051FCF0`); when that empties the slot's page, `0x0051F880` unlinks the page from the
   bank's page list and resets it.

`0x0051F880(bank, page)` first refreshes the directory from its handle `+0x08` when set (`0x0051F89E`), and
returns −1 with nothing changed when the bank's page count `+0x22` is 0 (`0x0051F8B7`). Otherwise it
unlinks the page's directory record (links `+0x04` previous and `+0x08` next; list head `+0x18`, tail
`+0x1C`), sets its `+0x00`, `+0x04` and `+0x08` to −1, zeroes the qword at `+0x14` and lowers the page
count (`0x0051F8D1`-`0x0051F95D`).

It then sets the current page `+0x20` to the first listed page whose count `+0x14` is below
`1 << shift`, to the list head when no listed page has room, or to 0 when no page is left, and returns
the unlinked page's old next index (`0x0051F961`-`0x0051F9E4`).

`0x00409CA0(bank, tag, name)` runs the same steps 2 to 4 for every entry that holds a section with that tag
and name (`0x0051FE30` with the test `0x0040A1E0`, which asks `0x00409A30`); `0x00504C40` uses it to drop the
`@FDM` entries of an object. `0x00409FE0`'s lookup for an existing entry uses the same test.

The source test `0x004095B0(entry, source)`, passed through its thunk `0x0040A200`, compares by the entry's mode
`+0x04`: a mode-0 entry holds the source when its decoded handle (`0x0051EE00(entry + 0x10)`) is the source, a
mode-1 entry when its raw handle `+0x30` is, and any other mode never. `0x00409FD0(bank, source)` runs one search
with it and returns the entry's slot or −1; the motion start `0x00424D80` asks it for the manager's bank
`+0xD90` (`0x004250CC`).

`0x003B37E0(id)` acts only when the slot's whole id matches, so a stale id does nothing. It sets the
ticket `+0x30` to −1, then runs the first two steps only when the ticket's context `+0x18` is non-null
(`0x003B3812`):

- detaches the context's effect instances (`0x0024F4D0`, which returns at once for a null context,
  `0x0024F4D3`): each instance in the type's list `0x020910F0[type]` that points to the context (`+0x340`)
  is unlinked (`+0x348` next, `+0x350` previous), made current in `0x02F97348`, and its three
  substructures `+0x120`, `+0x130` and `+0x1B8` are released (`0x003A81E0`, `0x003A72E0`, `0x003A8D70`);
- its deferred block `+0x380`, when set, is queued (256 entries at `0x02091950`, count `0x0209216A`; when
  full it goes to `0x00182CA0`), and the instance is freed (`0x003697F0`); `0x02F97348` keeps the last freed
  instance;
- frees the context (`0x0024F410`, which returns at once for a null context, `0x0024F413`): unlinks it
  from `0x020910A0[type]`, makes it current (`0x0024F457`), releases its five tables (`0x003A9EE0` for
  `+0x18`, `0x003A75B0` for `+0x38`, `0x003A7D30` for `+0x840`, `0x003A9600` for `+0x848`, `0x003A9950` for
  `+0x850`), runs `0x0024F4D0` again and frees the `0x890` bytes (`0x003697F0`);
- nothing clears `0x02F97340` after that free, so it is left pointing at the freed context. `0x0024F410` makes
  the context current because `0x003A75B0`, `0x003A7D30`, `0x003A9600` and `0x003A9950` read it there (`0x003A75B6`,
  `0x003A7D36`, `0x003A9606`, `0x003A9956`); no function it calls writes `0x02F97340`, nor does `0x003B37E0` or
  another caller after the call;
- `0x02F97340` moves at the next write, such as `0x0024B3A0` making a new context current (`0x0024B477`). When the
  ticket's `+0x18` is null, `0x003B37E0` skips both calls (`0x003B3815`) and `0x02F97340` stays as it was;
- recycles the instance handles that carry the ticket (`0x003B39E0`, the 32 records at `0x02EBD480`): each
  handle with counter bits set whose `+0x18` is the ticket id leaves the used list (`0x02EBDB98` head,
  `0x02EBDBA8` tail) for the head of the free list `0x02EBDBA0`, keeps its slot and top bits and has
  `+0x10` zeroed (`0x003B3A03`-`0x003B3A7F`);
- puts the ticket back on the free list with its slot bits and top nibble only: it unlinks the ticket
  from the in-use list (`0x02EBDB80` head, `0x02EBDB90` tail; next `+0x20`, previous `+0x28`), pushes it at
  the free head `0x02EBDB88` and zeroes `+0x08`, `+0x10` and `+0x18` (`0x003B382C`-`0x003B3896`).

`0x003A9600` and `0x003A9950` work on the current context `0x02F97340` and depend on its byte `+3` bit
`0x1`. When it is set they free the run origin (`+0x870` or `+0x878`) only if the context copied the
run (flags `+2` bit `0x4` clear), and zero the origin either way (`0x003A9633`, `0x003A9983`). When it is
clear they free every non-null table entry from index 1 (to 319 or 767), zeroing each, whatever the
borrow flag. Either way they then free the table (`0x003A9697`, `0x003A99E7`) and leave the context's
table pointer as it was.

`0x003A7D30` releases the `+0x840` table the same way, except that with the bit clear it frees all 128
entries from index 0, and with it set it frees the block at `+0x880`, when set, and zeroes it
(`0x003A7D4F`-`0x003A7D5D`).

`0x004096F0(entry)` returns an entry's source: the copy's data for mode 0 (`0x006B5C70`), the handle
`+0x30` for mode 1, and 0 for any other mode.

`0x00409730(entry)` calls `0x00427B00` with the entry's `+0x30`, which clears the render records'
`+0x68` (and `+0x69C`), `+0xD8`/`+0xE0` and `+0xF0`/`+0xF8` that decode to it. `0x00427B00` walks the
records from the first index `[[0x022C6F28] + 0x48800]` through each record's word `+4` until −1, and
returns at once for a first index of −1 (`0x00427B1D`). A match on `+0x68` zeroes it and stores the
encoded null `0x0020E620(0)` at `+0x69C`; a match on `+0xD8` or `+0xF0` zeroes that field and `+0xE0` or
`+0xF8` (`0x00427B30`-`0x00427BAB`).

`0x00409730` then releases the inline buffer (`0x0051EE80`, which frees a mode 0 copy through `0x003AB7C0`),
resets `+0x00` to `0xFFFF` and `+0x44` to −1, zeroes `+0x04`, `+0x30` and `+0x40`, and sets the inline
buffer up again with `0x0051EE10` (growth `0x800`, `0x00409772`). The cached pointer `+0x38` is not
cleared. A mode 1 source is not freed here; its loader frees it afterwards.

### After a source moves

Compaction can move a mode 1 source. Nothing that moves it repairs the effect data that borrows it.
`0x003B3C00(handle, n)`, which `0x003B8670` and `0x00427DE0` call to start cue `n` of an instance
(`0x0024FE70`), returns 0 for an `n` below 0 or above 10, a stale handle or a slot without an instance,
and 1 for an `n` of 0 without starting a cue (`0x003B3C0C`-`0x003B3C41`). For an `n` of 1 to 10 it first
runs `0x003B3480`, which repairs a borrowing context against the source's new address, and then runs
`0x0024FE70` under arena 8, returning 1 when that does and 0 otherwise (`0x003B3C4D`-`0x003B3C84`).

The repair walks are on the
[arena page](resource-arena-and-relocation.md#repairing-effect-data-after-its-source-moves). The run
origins `+0x870` and `+0x878` are not in those walks.

## Layouts

Bank entry (`0x50`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | slot | `0xFFFF` free |
| `+0x04` | `u32` | mode | 0 copy, 1 retained |
| `+0x10` | `...` | inline buffer | `0x20`: `+0x08` data, `+0x10` capacity, `+0x14` growth, `+0x18` used |
| `+0x30` | `...` |  | source handle |
| `+0x38` | `...` |  | cached pointer |
| `+0x40` | `u32` | size |  |
| `+0x44` | `i32` | ticket | -1 no ticket, 0 no ticket free |

Effect ticket (`0x38`), `0x02EBCD80` + slot*`0x38`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | id |  |
| `+0x08` | `...` |  | source base |
| `+0x18` | `...` | context |  |
| `+0x20` | `...` | next |  |
| `+0x28` | `...` | previous |  |
| `+0x30` | `i32` | effect number | -1 no effect |

Instance handle (`0x38`), `0x02EBD480` + slot*`0x38`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | id |  |
| `+0x10` | `...` | instance |  |
| `+0x18` | `u32` |  | ticket id |
| `+0x20` | `...` | next | next handle on the used or free list (`0x003B340F`, `0x003B3A23`, `0x003B3A5E`) |
| `+0x28` | `...` | previous | previous handle on that list (`0x003B342C`, `0x003B3A1F`, `0x003B3A6E`) |

Effect context (`0x890`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8` | type |  |
| `+0x002` | `u8` | flags | bit `0x4` borrow |
| `+0x003` | `u8` | lifecycleByte3 | bit `0x1` single-run tables |
| `+0x008` | `...` | next |  |
| `+0x010` | `...` | previous |  |
| `+0x840` | `...` | table | one of the three tables |
| `+0x848` | `...` | table | one of the three tables |
| `+0x850` | `...` | table | one of the three tables |
| `+0x858` | `...` |  | source base |
| `+0x860` | `u32` | source |  |
| `+0x864` | `i32` | offset |  |
| `+0x870` | `...` | run origin | one of the two run origins |
| `+0x878` | `...` | run origin | one of the two run origins |

Effect instance:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x340` | `...` | context |  |
| `+0x348` | `...` | next |  |
| `+0x350` | `...` | previous |  |
| `+0x380` | `...` |  | deferred block |
| `+0x390` | `...` |  | base copy |

Motion slot (`0x1C`), `0x02B581A0` + (g*16 + i)*`0x1C`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` | handle |  |
| `+0x04` | `...` | state |  |
| `+0x08` | `...` | armer argument | 0 |
| `+0x0C` | `u8` |  | manager slot |
| `+0x0D` | `u8` | route | 1 = arena 11 |
| `+0x0E` | `u16` |  | motion number |
| `+0x10` | `i16` | kind |  |
| `+0x12` | `i16` |  | file index |
| `+0x14` | `i32` | length |  |
| `+0x18` | `i32` | offset |  |

.mot header (`0x88`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | active |  |
| `+0x08` | `...` | entries | `+0x08` + i*8: u32 offset, u32 length (i = 0..15) |

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

The pending masks are five `u32` at `0x02B58A60 + 4 × g`, one per manager slot `g`; bit `i` marks motion record `i` of
that slot as armed and not yet swept:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B58A68` | `u32` | 0 (zero-filled tail of `.data`) | the pending mask of manager slot 2; the reset's 8-byte store also clears slot 3's mask `0x02B58A6C` | `0x003DD7E0` (`0x003DD7F4`, 0; called from `0x00266D10` at `0x00267112`); `0x003DD790(g)` (`0x003DD7D0`, 0 after it clears the slot's sixteen records; reached from `0x0026C8C0` at `0x0026CDE3`); `0x003DDA20` (`0x003DDA5F`, sets bit `i`); `0x003DD4C0` (`0x003DD672`, clears bit `i` once the record is handled) | `0x003DD4C0` (`0x003DD4F0`, the whole mask; `0x003DD510`, bit `i`) |
| `0x02B58A70` | `u32` | 0 (zero-filled tail of `.data`) | the pending mask of manager slot 4 | `0x003DD7E0` (`0x003DD7FB`, 0); `0x003DD790`, `0x003DDA20` and `0x003DD4C0` as above | `0x003DD4C0` as above |

The other three masks follow the same accesses; the reset clears slots 0 and 1 with one 8-byte store at `0x02B58A60`
(`0x003DD7ED`). `0x003DD790`, `0x003DDA20` and the sweep reach each mask as `0x02B58A60 + 4 × g` (`0x003DD7C9`, `0x003DDA47`,
`0x003DD4D4` with `0x003DD69B`).

## Modding notes

- Two sources with the same tag and name share one bank entry: the first one registered wins, and
  later ones are never parsed.
- At most 32 effect tickets exist at once; a further `@FEF` registration stores ticket 0 and gets no
  effect context.
- Every `.cm` file with an `@FEF` section needs a non-NULL entry in the `0x02B64380` table for its name,
  or loading it ends the game.
- `motionread` loads only motions 0–15 of manager slots 0–3, from the offsets in the first `0x88` bytes of
  the area's `.mot`; give each a length of at least 1.
- Call `motiondispose` before reusing a motion number: `motionread` does nothing unless the slot is
  idle.

## Related

- [Resource arenas and relocation](resource-arena-and-relocation.md): handles, pins, the movable tree and the repair walks.
- [Resource sections](resource-sections.md): the `@FRP` container and section lookup.
- [File requests and the read queue](file-requests-and-the-read-queue.md): how a −1 size completes.
- [File size tables](file-size-tables-fst.md): the file kinds the motion slots read.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): the binding entries and lanes that register here.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Story event quest hunt: `0x0026C8C0` calls `0x00377440`; those functions are documented on
  [actor managers](../Characters-And-Objects/actor-managers.md).
