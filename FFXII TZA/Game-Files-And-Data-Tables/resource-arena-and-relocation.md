---
title: "Resource arenas and relocation: the fifteen memory arenas, block headers, handles, the movable-block tree, compaction, and how moved effect data is repaired"
kind: "system"
category: "Game files and data tables"
addresses: "0x022D7FD0, 0x00369D30, 0x0022A0B0, 0x0036C1D0, 0x0036C140, 0x022D89BC, 0x022D89C0, 0x022D89B8, 0x0036A490, 0x00369860, 0x0036C660, 0x0036A100, 0x0036A190, 0x0036BC60, 0x0036BFE0, 0x0020E600, 0x0020E620, 0x01F83530, 0x0036B130, 0x003AB7F0, 0x0036A000, 0x0036D170, 0x003AB880, 0x003AB940, 0x00369800, 0x0036A9C0, 0x0036B410, 0x0036B4E0, 0x0036C790, 0x00369C60, 0x0036AAD0, 0x0036ABE0, 0x0036A2A0, 0x004746F0, 0x00369CF0, 0x003697C0, 0x002E65A0, 0x003B3480, 0x0024D970, 0x0024D940, 0x003AA3D0, 0x003A9BA0, 0x003A9860, 0x003A8FF0, 0x005004C0, 0x0036C5A0, 0x002E6D60, 0x002EA320, 0x0036B160, 0x0036C4B0, 0x0036C6C0, 0x0036CAD0, 0x0036D050, 0x0036A240, 0x0037B450, 0x0037B330, 0x0024AC30, 0x0024AB30, 0x0024AB60, 0x0036A570, 0x0036A850, 0x00369760, 0x0036C1F0, 0x0036B670, 0x0036B730, 0x0036B7F0, 0x0036B8B0, 0x0036C9D0"
---

## What the player sees

Nothing while it works. Loaded models, effects and tables live in a handful of large memory arenas
that the game compacts as it goes, moving blocks to close gaps; a block whose header has been
overwritten makes the game write a memory dump and quit.

## How it works

### The arenas

There are fifteen arena records of `0xA8` bytes at `0x022D7FD0`, indexed 0 to 14. `0x00369D30(arena, buffer,
size, slots)` builds one inside a caller's buffer, with
`pages = ((size + 0xFFFF) / 0x10000 + 31) & ~31`: one page per 64 KB, rounded up to a multiple of 32
(`0x00369DDF`-`0x00369E0D`, record `+0x58`).

The buffer starts with a `0x40`-byte name header. A bitmap of `pages / 32` dwords follows at record
`+0x20` = `(buffer + 0x7F) & ~0x3F`, the page map of one qword per page at `+0x28` =
`(bitmap + (pages / 32) × 8 + 0x3F) & ~0x3F`, and then `h = (map + pages × 8 + 0x3F) & ~0x3F`
(`0x00369E73`-`0x00369EA4`).

When `slots` is non-zero the handle-slot table of 16-byte slots starts at `h` and the block heap at
`(h + slots × 16 + 0x3F) & ~0x3F` (`0x00369EAC`-`0x00369EC6`); otherwise the heap starts at `h`. It sets
the arena's bit in the enabled mask `0x022D89B8` and writes the heap's first free block header.

Boot (`0x0022A0B0`) and four later calls build these:

| Arena | Size | Slots | Built at |
|---:|---|---:|---|
| 2 | `0x1DC0000` | 16 | `0x0022A2AE` |
| 3 | `0xD20000` | 256 | `0x0022A2CB` |
| 4 | `0x100000` | 16 | `0x0022A2E7` |
| 5 | `0x1C0000` | 256 | `0x0022A304` |
| 6 | `0x6C00000` | 1,024 | `0x0022A321` |
| 7 | `0x3000000` | 256 | `0x0022A33E` |
| 8 | `0x2000000` | 256 | `0x0022A35B` |
| 9 | `0x1200000` | 16 | `0x0022A377` |
| 11 | `0x400000` | 256 | `0x0022A394`, rebuilt by `0x0037B3D0` |
| 12 | the caller's | 0 | `0x003E9AEF` |
| 13 | `0x100000` | 0 | `0x0025AA21` |
| 14 | `0x19000` | 0 | `0x0025AAC1` |

Arenas 0, 1 and 10 are built by none of them.

### Arena 11's modes

Arena 11 is rebuilt whenever its mode changes. `0x0037B450(mode)` stores the mode at `0x02ADD930`, runs
`0x0037B3D0` and then stores it at `0x02ADD931`. `0x0037B3D0` sets `0x02ADD932` to 4 and, when the two bytes
differ, calls `0x00369760(11)` and `0x0036D160(11)`, frees its block `0x01FD4A18` (`0x0036D250`), takes a
new one (`0x0036D240`) of `0x3C0000` bytes for mode 3 or `0x400000` otherwise, and builds the arena in it
with 256 slots (`0x00369D30`).

| Mode | Set by |
|---|---|
| `0` | boot (`0x0037B390`, from `0x0022A0B0`), `0x0035B8D0`, `0x0024AB60` |
| `1` | `0x0035B840`, which also takes kind 28 path `2n + 1` (`0x002DF980`) |
| `2` | `0x003DD6C0`, when a party slot has bit `0x1` of `+0x10` and bit `0x40` of `+0x17` and `0x0037B330()` is 0 or 2; with no such slot it stores 0 as the waiting mode (`0x0037B490(0)`) |
| `3` | `0x0024AC30`, the menu overlay load |

- A mode can also wait in `0x02ADD932`: `0x0037B490` stores it, `0x0037B380` reads it, and `0x0037B2F0` (from
  `0x002E65A0`) applies it as `0x0037B450` does unless it is 4.
- `0x0037B330` returns `0x02ADD930` while `0x02ADD931` is 0 and 4 otherwise. Both bytes always receive the same
  mode, so it answers 0 or 4, and `0x003DD4C0`'s test for 2 never passes.
- `0x0024AC30(n, wait)` acts only when `0x0037B330()` is 0: it sets mode 3 and requests kind 35, index `n + 7`,
  straight into the block `0x01FD4A18` with the completion `0x0024ACF0`, which sets `0x02091094`; with `wait` it
  drains the queue (`0x0032E520(0)`). Otherwise it only calls the do-nothing body `0x0016D6A0`.
- `0x0024AC10(n)`, called by the menu request host `0x0027FB70`, stores 1 in `0x02091094` and returns 0 for n = 1, and
  runs `0x0024AC30(n, 0)` for any other n.
- `0x0024AB60` sets mode 0 and clears `0x02091094` when it is set. `0x0024AB30`, called from the menu handler
  `0x00280140`, does nothing whatever it finds: it returns at once when `0x02091094` is 0 or `0x0037B330` answers
  4, and otherwise jumps to the empty body `0x0016D6A0` with `ecx` = `0x80000`.

### The current arena

Allocation goes to the current arena `0x022D89BC`. `0x0036C1D0(arena, …)` pushes the current arena state
(arena, a tag byte, flags) onto a 16-byte stack and selects a new one; `0x0036C140` pops it. Popping an
empty stack spins forever, and `0x0036BC60` spins forever when asked to allocate with nothing pushed
(`0x022D89C0` = 0).

`0x0036C1D0` is an entry stub: it passes stack 0 and the qword at its stack pointer + 4, minus 5
(`0x0036C1D7`), and jumps to the body `0x0036C1F0(arena, category, stack, value)`. The body:

1. reads the stack's depth from `0x022D89C0 + stack × 4` and spins forever at a depth of 31 or more;
2. saves the current arena `0x022D89BC`, the category byte `0x022D8E18`, the byte `0x022D8E28` and the
   qword `0x022D8E20` in entry `depth` at `0x022D89D0 + (stack × 32 + depth) × 0x10`, and adds 1 to the depth;
3. stores `category` in `0x022D8E18` and `value` in `0x022D8E20`, and makes the arena the byte at
   `0x022D89A8 + arena` the new current arena.

`0x0036C140` reads the same four fields back from stack 0's top entry.

### Blocks

Every block, used or free, starts with a `0x40`-byte header written by `0x0036A490`: magic `0xFF12` at
`+0x00`, the arena at `+0x03`, the size at `+0x18`, a tag word at `+0x1C`, and encoded links at `+0x04`,
`+0x08`, `+0x0C`, `+0x10` and `+0x20`..`+0x30`. The payload follows at `+0x40`.

`0x0036BC60(arena, size, block, fromTop)` rounds the size up to a multiple of 64 and, with no block
given, walks the free list from `+0x90` (bottom up, through `+0x08`) or `+0x98` (top down, through
`+0x04`) for the first block at least that large.

It carves the allocation from the bottom or the top
of that block, writes a new header for any remainder of at least 0 bytes, sets the allocation's
`+0x14` bit 0 (allocated), `+0x15` bit 0 for a top allocation and `+0x16` = the current tag, and
returns the payload. `0x0036A100(size)` allocates bottom-up in the current arena and `0x0036A190` (through
`0x0036A1A0`) top-down; when that fails both fall to `0x0036BFE0`.

`0x0036C660(payload, name, tag)` labels a block: when the header carries the magic and is allocated, it
copies seven characters of the name to `+0x34`, terminates it, stores the tag at `+0x1E` and zeroes
`+0x3E`.

`0x00369860(payload, caller)` frees a block. A payload whose header lacks the magic, or whose `+0x3E` is
non-zero, makes it format a dump of `0xB0` header bytes and `0xD0` caller bytes, record the arena in
`0x022D89BC`, call `0x0036A570(arena, 0xB)` and `exit(1)`.

`0x0036A570(arena, flags, category)` walks an enabled arena and prints nothing. Per flag bit it follows
the blocks from the heap start `+0x10` (bit 0, building a state label from each header's flags and
copying the name of a block of `category`, or of any block for a negative one), the free list from
`+0x90` (bit 1), the used and free slot chains from `+0x48` and `+0x40` (bits 3 and 4) and, for bit 5,
the tree from `+0x50` through `0x0036A850`, which recurses on each node's `+0x24` link and follows
`+0x28`. The labels stay in a local buffer that no output call receives.

`0x00369760(arena)` returns 1 for a disabled arena or one whose `+0x10`, `+0x90` and `+0x98` are equal;
otherwise it runs the walk with all flags (`0x3F`) and returns 0. `0x0036C0F0` runs it with flag 1.

### Block chains

Every header is on the address chain, previous block at `+0x0C` and next at `+0x10`, which the walk
follows from the heap start (`0x0036A570`). A free block is also on the free chain, previous at
`+0x04` and next at `+0x08`, whose ends are record `+0x90` and `+0x98`. All four links are encoded
offsets. Four helpers link a header `b` beside a header `a`:

| Helper | Chain | Puts `b` |
|---|---|---|
| `0x0036B670(a, b)` | free | after `a` |
| `0x0036B730(a, b)` | free | before `a` |
| `0x0036B7F0(a, b)` | address | after `a` |
| `0x0036B8B0(a, b)` | address | before `a` |

- Each first checks `b`'s `+0x3E`: when it is non-zero it walks the current arena with flags `0xB`
  (`0x0036A570`) and calls `exit(1)`. It then zeroes `+0x3E` on every header whose links it rewrites.
- With a null `a`, `b` gets null links on that chain.
- `0x0036C9D0(header, both)` takes a header off the free chain and, when `both` is set, off the address
  chain too, writing `0xFF99` over its magic so the header no longer counts as a block; it zeroes `+0x3E`.

The carving in `0x0036BC60` uses all of them: it takes the chosen free block off both chains, puts the
allocation and the remainder on the address chain where the old block was, and puts the remainder on
the free chain beside the old block's free neighbours. The free `0x00369860`, the resize helpers
`0x0036C290` and `0x0036C380` (from `0x0036CB00`), `0x0036B2C0` and `0x0036B980` call them too.

### The 32-bit address encoding

Links inside headers and many other stored references are 32-bit values. `0x0020E600(v)` decodes them as
`base + (u64)v` and `0x0020E620(p)` encodes them as `low32(p) − low32(base)`, with the base at
`0x01F83530`. That cell lies in the zero-filled tail of `.data`, so the base is 0 at load and every
encoded block must sit below 4 GB.

### Handles

A handle is the address of a 16-byte slot in an arena's slot table with tag bits in its low two bits:
`{+0x00 u16 next, +0x02 u16 previous, +0x04 u8 arena, +0x05 u8 in use, +0x06 u16 check word, +0x08
header pointer}`. The table at record `+0x30` starts as one free chain headed at `+0x40`; slots in use
hang off `+0x48`.

- `0x0036A000(handle)` (and `0x003AB880`, which passes a value with clear tag bits through unchanged)
  checks that the handle is tagged, at least `0x100000`, and that the slot's `+0x06` equals the
  header's `+0x1C`; it then takes the block out of the movable tree (when `+0x15` bit 1 says it is in
  it) and returns the payload.
- `0x0036D170(handle)` (and `0x003AB940`) makes the same check and, when the block is not in the tree,
  puts it back and sets `+0x15` bit 1.
- `0x0036B130(handle)` returns `[slot + 8] + 0x40` with no check word test, so a stale handle resolves
  to whatever the slot holds now. `0x003AB7F0` wraps it and returns 0 when the low 32 bits of the
  result are `0x40` or less.
- `0x0036A0B0(handle)` checks only `(handle & 3) != 0 && handle >= 0x100000` (`0x0036A0BA`-`0x0036A0C5`), takes
  the header `[(handle & ~3) + 8]`, sets the block's `+0x15` bit 2 when it is clear, zeroing `+0x3E`, and returns the payload `+0x40`, or 0; `0x0036D200(handle)` clears that bit and
  `+0x3E` again. The sound-bank loaders `0x002E60F0`, `0x0036E9F0`, `0x0036EAB0`, `0x0036ED50` and `0x003A1650` use the
  first, `0x002E60F0` and `0x003A0EA0` the second.
- `0x00369800(handle)` frees the slot (`0x0036A9C0`: unlinks it, takes the block out of the tree, zeroes
  the slot) and then the block (`0x00369860`).
- `0x0036B160(size)` allocates a block with a handle in the current arena: bottom-up (`0x0036BC60`, then
  `0x0036BFE0`), then `0x0036C4B0(arena, payload)`, which puts the block in the movable tree (`0x0036B410`),
  sets `+0x15` bit 1 and clears bit 2, and takes a free slot (`0x0036AF20`).
- When no slot is free, `0x0036C4B0` takes the block out of the tree again, frees it and returns 0; a slot
  value without tag bits or below `0x100000` makes it write to address 8, a deliberate crash; otherwise
  the slot's `+0x08` gets the header and the handle is returned.
- `0x0036A240(slot, header)` binds a slot to a header: the slot's `+0x08` and check word `+0x06` (from the
  header's `+0x1C`), and the header's encoded slot `+0x20`; it also zeroes the header's `+0x3E`.
- `0x0036C6C0(handle, name, tag)` labels a handle's block as `0x0036C660` labels a payload's, once the
  handle is tagged and at least `0x100000` and its header carries the magic and is allocated.
- `0x0036CAD0(payload, size)` resizes a block in the current arena through `0x0036D050`: a size of 0 frees
  it, a null payload allocates (`0x0036BFE0`), and any other goes to `0x0036CB00`.

### The movable-block tree

Each arena keeps the blocks that may be moved in a binary tree rooted at record `+0x50` (a full
pointer). A block's left, right and parent links are encoded offsets at `+0x24`, `+0x28` and `+0x2C`,
and it is ordered by its size `+0x18` as a signed value; an equal size goes right (`0x0036B4E0`).
`0x0036B410` clears a block's links and `+0x3E` and inserts it, or makes it the root of an empty tree;

`0x0036C790` removes it, relinking children with `0x0036B490` (left, `+0x24`) and `0x0036B5A0` (right,
`+0x28`), which also set the child's parent link `+0x2C`. Acquiring a handle takes its block out;
releasing it puts it back.

### Compaction

`0x00369C60(arena, repeat)` does nothing for a disabled arena or an empty tree. Otherwise it runs the
exact pass once and the adjacent pass once, or repeatedly while `repeat` is set and a pass moves
something, and on any move sets record `+0x02` and the moved latch `+0x62`. It returns the number of
moves.

- **Exact pass** `0x0036AAD0`: for the free block at the head of `+0x90`, it searches the tree for a block
  of the same size at a higher address (low 32 bits compared unsigned) whose `+0x15` bit 2 is clear,
  and moves it into the hole.
- **Adjacent pass** `0x0036ABE0`: for each free block, when the block physically after it is in the tree
  and not inhibited (`+0x15 & 6` = 2) and allocated, it moves that block down; otherwise it searches
  for an equal-size block higher up as above. It moves at most one block per call.

`0x0036BFE0(arena, size)` is the pressure path: it calls the arena's callback at record `+0xA0` when one
is set, compacts once, and retries the allocation, until the allocation succeeds or nothing moved and
the callback returned 0. A disabled arena spins forever. `0x00369CF0` reads and `0x003697C0` clears the
moved latch.

`0x0036C5A0(arena, fn)` is the only setter of the pressure callback. The binding-table init `0x002EA320`
installs `0x002E6D60` for arenas 6 and 10, so under pressure in arena 6 the binding system first unloads
one queued lane and releases its oldest retired model entry, and only then does the arena compact and
retry ([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)).

The binding
system's per-frame update `0x002E65A0` also compacts arenas 6 and 10 with repeat 1 (`0x00369C60(6, 1)`,
`0x00369C60(10, 1)`) every frame, and once more after releasing retired bindings. Arena 10 is built by none
of the sites above, so its compaction does nothing.

### The mover

`0x0036A2A0(arena, hole, source)` saves the source header's fields and name, then:

1. takes the source out of the tree when it is in it;
2. points the source's handle slot at the hole's header, sets the hole's `+0x20` backlink and copies
   the check word;
3. frees the source (`0x00369860`) and copies `source +0x18` payload bytes into the hole with `memcpy`
   (`0x004746F0`);
4. claims the hole (`0x0036BC60(arena, size, hole, 0)`), restores the saved fields and name, puts it back
   in the tree when the source was there, and republishes the slot.

The handle value stays the same across a move and resolves to the new address; a raw pointer a
consumer kept still points at the old one. The old block is released before the copy, and the copy
uses `memcpy`, not a move that tolerates overlap.

### Repairing effect data after its source moves

An effect template keeps a full 64-bit source base at `+0x858`, a tagged source handle at `+0x860` and
a signed offset at `+0x864`. `0x003B3480` resolves the handle (`0x003AB7F0`), adds the sign-extended offset
and, when the result differs from `+0x858`, calls `0x0024D970(template, newBase)`; it repeats the test
against a second object's base at `+0x390` and repairs it with `0x0024D940`.

`0x0024D970` computes the delta as a 32-bit difference of the low halves of the new and old bases, runs
three repair walks with it (`0x003AA3D0`, `0x003A9BA0`, `0x003A9860`), and stores the full new base.

Each walk
sign-extends the delta and adds it to every stored pointer it covers (`0x003A8FF0` adds it at list
records `+0x100`, `+0x108`, `+0x18` and `+0x20`). The repair is exact only when the real distance moved
lies between −2^31 and 2^31 − 1; beyond that the base is right and every repaired pointer is wrong.
`0x003AA3D0` forwards the delta to the element handlers `0x00501420` and `0x00503F10`; the effect element
types `0x005004C0` sets up are on the
[effect element dispatch](../17-Presentation-Rendering/effect-element-runtime.md
)
page.

## Layouts

```
arena record   0x022D7FD0 + i*0xA8: +0x00 u8, +0x01 u8 index, +0x02 u8 dirty, +0x08 name header, +0x10 heap start,
               +0x18 heap middle, +0x20 bitmap, +0x28 page map, +0x30 slot table, +0x38 slot end, +0x40 free slot,
               +0x48 used slot, +0x50 tree root, +0x58 u32 pages, +0x5C u32 heap size, +0x60 u16 tag, +0x62 u8 moved,
               +0x90 free list bottom, +0x98 free list top, +0xA0 pressure callback
block header   +0x00 u16 0xFF12, +0x02 u8 category (0x022D8E18, stamped at 0x0036A15F; 0xFF when free), +0x03 u8 arena, +0x04/+0x08/+0x0C/+0x10 encoded links,
               +0x14 u8 bit 0 allocated, +0x15 u8 bit 0 top, bit 1 in tree, bit 2 not movable, bit 3 set while 0x022D8E28,
               +0x16 u8 tag, +0x18 s32 size, +0x1C u16 check word, +0x1E u16 label tag, +0x20 encoded slot,
               +0x24/+0x28/+0x2C encoded tree links, +0x34 char[8] label, +0x3E u16 must be 0 on free; payload +0x40
handle slot    +0x00 u16 next, +0x02 u16 previous, +0x04 u8 arena, +0x05 u8 in use, +0x06 u16 check word, +0x08 header
```

`ArenaStackEntry` (`0x10` bytes, offsets from the start of the 0x022D89D0+(stack*32+depth)*0x10):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | arena | the current arena `0x022D89BC` |
| `+0x02` | `u8` | category | `0x022D8E18` |
| `+0x03` | `u8` | flag | `0x022D8E28` |
| `+0x04` | `u8[4]` | pad | read and written by neither the push `0x0036C1F0` nor the pop `0x0036C140`; nothing fixes its width |
| `+0x08` | `u64` | value | `0x022D8E20` |

The arena record's fields are listed access by access in
[`resource-arena-record-accesses.tsv`](resource-arena-record-accesses.tsv) and
[`resource-arena-record-accesses-flow-sensitive.tsv`](resource-arena-record-accesses-flow-sensitive.tsv).

## Operations

Per allocation: one free-list walk and up to two header writes. Per compaction pass: one tree search and
at most one move, a header save and restore plus one payload copy.

## State

The fifteen arena records, the enabled mask `0x022D89B8`, the current arena `0x022D89BC` and its stack, and
the encoding base `0x01F83530`.

## Modding notes

- Keep a handle, not a payload pointer, across any allocation, and in arena 6 across a frame: any
  allocation can compact an arena, and arena 6 is compacted every frame.
- A block taken with `0x0036A000` stays put until it is released with `0x0036D170`.
- Every arena block must lie below 4 GB for the 32-bit links to work.
- Writing past a block's end into the next header ends the game at that block's free.

## Related

- [Resource sections](resource-sections.md): how data inside a loaded block is found.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): the binding system that compacts arena 6 and supplies its pressure callback.
- [File requests and the read queue](file-requests-and-the-read-queue.md): the loads that fill these blocks.
- [Effect element dispatch](../17-Presentation-Rendering/effect-element-runtime.md
): the effect elements the repair walks reach.
