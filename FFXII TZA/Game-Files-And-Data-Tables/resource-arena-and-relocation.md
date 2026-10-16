---
title: "Resource arenas and relocation: the fifteen memory arenas, block headers, handles, the movable-block tree, compaction, and how moved effect data is repaired"
kind: "system"
category: "Game files and data tables"
summary: "How the game's resource memory is laid out and moved: the arena records and their boot sizes, the current-arena stack, the 0x40-byte block header and its corruption check, suballocation from the free lists, the 32-bit address encoding, tagged handles and their slot table, acquiring and releasing a handle and the tree of blocks that may move, compaction and the allocation-pressure retry, the mover's order of operations, and how an effect file's stored pointers are repaired after its source moves, with the 32-bit limits each step carries."
addresses: "022D7FD0, 00369D30, 0022A0B0, 0036C1D0, 0036C140, 022D89BC, 022D89C0, 022D89B8, 0036A490, 00369860, 0036C660, 0036A100, 0036A190, 0036BC60, 0036BFE0, 0020E600, 0020E620, 01F83530, 0036B130, 003AB7F0, 0036A000, 0036D170, 003AB880, 003AB940, 00369800, 0036A9C0, 0036B410, 0036B4E0, 0036C790, 00369C60, 0036AAD0, 0036ABE0, 0036A2A0, 004746F0, 00369CF0, 003697C0, 002E65A0, 003B3480, 0024D970, 0024D940, 003AA3D0, 003A9BA0, 003A9860, 003A8FF0, 005004C0, 0036C5A0, 002E6D60, 002EA320, 0036B160, 0036C4B0, 0036C6C0, 0036CAD0, 0036D050, 0036A240, 0037B450, 0037B330, 0024AC30, 0024AB30, 0024AB60"
---

## What the player sees

Nothing while it works. Loaded models, effects and tables live in a handful of large memory arenas
that the game compacts as it goes, moving blocks to close gaps; a block whose header has been
overwritten makes the game write a memory dump and quit.

## How it works

### The arenas

There are fifteen arena records of `0xA8` bytes at `022D7FD0`, indexed 0 to 14. `00369D30(arena, buffer,
size, slots)` builds one inside a caller's buffer: a `0x40`-byte name header at the start, a page map
(one qword per 64 KB page, the page count rounded to 32) and a bitmap of `pages / 32` dwords, the
handle-slot table when `slots` is non-zero, and the block heap after them, rounded to 64 bytes. It sets
the arena's bit in the enabled mask `022D89B8` and writes the heap's first free block header.

Boot (`0022A0B0`) and four later calls build these:

| Arena | Size | Slots | Built at |
|---:|---|---:|---|
| 2 | `0x1DC0000` | 16 | `0022A2AE` |
| 3 | `0xD20000` | 256 | `0022A2CB` |
| 4 | `0x100000` | 16 | `0022A2E7` |
| 5 | `0x1C0000` | 256 | `0022A304` |
| 6 | `0x6C00000` | 1,024 | `0022A321` |
| 7 | `0x3000000` | 256 | `0022A33E` |
| 8 | `0x2000000` | 256 | `0022A35B` |
| 9 | `0x1200000` | 16 | `0022A377` |
| 11 | `0x400000` | 256 | `0022A394`, rebuilt by `0037B3D0` |
| 12 | the caller's | 0 | `003E9AEF` |
| 13 | `0x100000` | 0 | `0025AA21` |
| 14 | `0x19000` | 0 | `0025AAC1` |

Arenas 0, 1 and 10 are built by none of them.

### Arena 11's modes

Arena 11 is rebuilt whenever its mode changes. `0037B450(mode)` stores the mode at `02ADD930`, runs
`0037B3D0` and then stores it at `02ADD931`. `0037B3D0` sets `02ADD932` to 4 and, when the two bytes
differ, calls `00369760(11)` and `0036D160(11)`, frees its block `01FD4A18` (`0036D250`), takes a
new one (`0036D240`) of `0x3C0000` bytes for mode 3 or `0x400000` otherwise, and builds the arena in it
with 256 slots (`00369D30`).

| Mode | Set by |
|---|---|
| `0` | boot (`0037B390`, from `0022A0B0`), `0035B8D0`, `0024AB60` |
| `1` | `0035B840`, which also takes kind 28 path `2n + 1` (`002DF980`) |
| `2` | `003DD6C0`, when a party slot has bit `0x1` of `+0x10` and bit `0x40` of `+0x17` and `0037B330()` is 0 or 2 |
| `3` | `0024AC30`, the menu overlay load |

- A mode can also wait in `02ADD932`: `0037B490` stores it, `0037B380` reads it, and `0037B2F0` (from
  `002E65A0`) applies it as `0037B450` does unless it is 4.
- `0037B330` returns `02ADD930` while `02ADD931` is 0 and 4 otherwise. Both bytes always receive the same
  mode, so it answers 0 or 4, and `003DD4C0`'s test for 2 never passes.
- `0024AC30(n, wait)` acts only when `0037B330()` is 0: it sets mode 3 and requests kind 35, index `n + 7`,
  straight into the block `01FD4A18` with the completion `0024ACF0`, which sets `02091094`; with `wait` it
  drains the queue (`0032E520(0)`). Otherwise it only calls the do-nothing body `0016D6A0`.
- `0024AB60` sets mode 0 and clears `02091094` when it is set. `0024AB30`, called from the menu handler
  `00280140`, does nothing whatever it finds: it returns at once when `02091094` is 0 or `0037B330` answers
  4, and otherwise jumps to the empty body `0016D6A0` with `ecx` = `0x80000`.

### The current arena

Allocation goes to the current arena `022D89BC`. `0036C1D0(arena, …)` pushes the current arena state
(arena, a tag byte, flags) onto a 16-byte stack and selects a new one; `0036C140` pops it. Popping an
empty stack spins forever, and `0036BC60` spins forever when asked to allocate with nothing pushed
(`022D89C0` = 0).

### Blocks

Every block, used or free, starts with a `0x40`-byte header written by `0036A490`: magic `0xFF12` at
`+0x00`, the arena at `+0x03`, the size at `+0x18`, a tag word at `+0x1C`, and encoded links at `+0x04`,
`+0x08`, `+0x0C`, `+0x10` and `+0x20`..`+0x30`. The payload follows at `+0x40`.

`0036BC60(arena, size, block, fromTop)` rounds the size up to a multiple of 64 and, with no block
given, walks the free list from `+0x90` (bottom up, through `+0x08`) or `+0x98` (top down, through
`+0x04`) for the first block at least that large.

It carves the allocation from the bottom or the top
of that block, writes a new header for any remainder of at least 0 bytes, sets the allocation's
`+0x14` bit 0 (allocated), `+0x15` bit 0 for a top allocation and `+0x16` = the current tag, and
returns the payload. `0036A100(size)` allocates bottom-up in the current arena and `0036A190` (through
`0036A1A0`) top-down; when that fails both fall to `0036BFE0`.

`0036C660(payload, name, tag)` labels a block: when the header carries the magic and is allocated, it
copies seven characters of the name to `+0x34`, terminates it, stores the tag at `+0x1E` and zeroes
`+0x3E`.

`00369860(payload, caller)` frees a block. A payload whose header lacks the magic, or whose `+0x3E` is
non-zero, makes it format a dump of `0xB0` header bytes and `0xD0` caller bytes, record the arena in
`022D89BC`, call `0036A570(arena, 0xB)` and `exit(1)`.

### The 32-bit address encoding

Links inside headers and many other stored references are 32-bit values. `0020E600(v)` decodes them as
`base + (u64)v` and `0020E620(p)` encodes them as `low32(p) − low32(base)`, with the base at
`01F83530`. That cell lies in the zero-filled tail of `.data`, so the base is 0 at load and every
encoded block must sit below 4 GB.

### Handles

A handle is the address of a 16-byte slot in an arena's slot table with tag bits in its low two bits:
`{+0x00 u16 next, +0x02 u16 previous, +0x04 u8 arena, +0x05 u8 in use, +0x06 u16 check word, +0x08
header pointer}`. The table at record `+0x30` starts as one free chain headed at `+0x40`; slots in use
hang off `+0x48`.

- `0036A000(handle)` (and `003AB880`, which passes a value with clear tag bits through unchanged)
  checks that the handle is tagged, at least `0x100000`, and that the slot's `+0x06` equals the
  header's `+0x1C`; it then takes the block out of the movable tree (when `+0x15` bit 1 says it is in
  it) and returns the payload.
- `0036D170(handle)` (and `003AB940`) makes the same check and, when the block is not in the tree,
  puts it back and sets `+0x15` bit 1.
- `0036B130(handle)` returns `[slot + 8] + 0x40` with no check word test, so a stale handle resolves
  to whatever the slot holds now. `003AB7F0` wraps it and returns 0 when the low 32 bits of the
  result are `0x40` or less.
- `00369800(handle)` frees the slot (`0036A9C0`: unlinks it, takes the block out of the tree, zeroes
  the slot) and then the block (`00369860`).
- `0036B160(size)` allocates a block with a handle in the current arena: bottom-up (`0036BC60`, then
  `0036BFE0`), then `0036C4B0(arena, payload)`, which puts the block in the movable tree (`0036B410`),
  sets `+0x15` bit 1 and clears bit 2, and takes a free slot (`0036AF20`).
- When no slot is free, `0036C4B0` takes the block out of the tree again, frees it and returns 0; a slot
  value without tag bits or below `0x100000` makes it write to address 8, a deliberate crash; otherwise
  the slot's `+0x08` gets the header and the handle is returned.
- `0036A240(slot, header)` binds a slot to a header: the slot's `+0x08` and check word `+0x06` (from the
  header's `+0x1C`), and the header's encoded slot `+0x20`; it also zeroes the header's `+0x3E`.
- `0036C6C0(handle, name, tag)` labels a handle's block as `0036C660` labels a payload's, once the
  handle is tagged and at least `0x100000` and its header carries the magic and is allocated.
- `0036CAD0(payload, size)` resizes a block in the current arena through `0036D050`: a size of 0 frees
  it, a null payload allocates (`0036BFE0`), and any other goes to `0036CB00`.

### The movable-block tree

Each arena keeps the blocks that may be moved in a binary tree rooted at record `+0x50` (a full
pointer). A block's left, right and parent links are encoded offsets at `+0x24`, `+0x28` and `+0x2C`,
and it is ordered by its size `+0x18` as a signed value; an equal size goes right (`0036B4E0`).
`0036B410` clears a block's links and `+0x3E` and inserts it, or makes it the root of an empty tree;

`0036C790` removes it, relinking children with `0036B490` (left, `+0x24`) and `0036B5A0` (right,
`+0x28`), which also set the child's parent link `+0x2C`. Acquiring a handle takes its block out;
releasing it puts it back.

### Compaction

`00369C60(arena, repeat)` does nothing for a disabled arena or an empty tree. Otherwise it runs the
exact pass once and the adjacent pass once, or repeatedly while `repeat` is set and a pass moves
something, and on any move sets record `+0x02` and the moved latch `+0x62`. It returns the number of
moves.

- **Exact pass** `0036AAD0`: for the free block at the head of `+0x90`, it searches the tree for a block
  of the same size at a higher address (low 32 bits compared unsigned) whose `+0x15` bit 2 is clear,
  and moves it into the hole.
- **Adjacent pass** `0036ABE0`: for each free block, when the block physically after it is in the tree
  and not inhibited (`+0x15 & 6` = 2) and allocated, it moves that block down; otherwise it searches
  for an equal-size block higher up as above. It moves at most one block per call.

`0036BFE0(arena, size)` is the pressure path: it calls the arena's callback at record `+0xA0` when one
is set, compacts once, and retries the allocation, until the allocation succeeds or nothing moved and
the callback returned 0. A disabled arena spins forever. `00369CF0` reads and `003697C0` clears the
moved latch.

`0036C5A0(arena, fn)` is the only setter of the pressure callback. The binding-table init `002EA320`
installs `002E6D60` for arenas 6 and 10, so under pressure in arena 6 the binding system first unloads
one queued lane and releases its oldest retired model entry, and only then does the arena compact and
retry ([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)).

The binding
system's per-frame update `002E65A0` also compacts arenas 6 and 10 with repeat 1 (`00369C60(6, 1)`,
`00369C60(10, 1)`) every frame, and once more after releasing retired bindings. Arena 10 is built by none
of the sites above, so its compaction does nothing.

### The mover

`0036A2A0(arena, hole, source)` saves the source header's fields and name, then:

1. takes the source out of the tree when it is in it;
2. points the source's handle slot at the hole's header, sets the hole's `+0x20` backlink and copies
   the check word;
3. frees the source (`00369860`) and copies `source +0x18` payload bytes into the hole with `memcpy`
   (`004746F0`);
4. claims the hole (`0036BC60(arena, size, hole, 0)`), restores the saved fields and name, puts it back
   in the tree when the source was there, and republishes the slot.

The handle value stays the same across a move and resolves to the new address; a raw pointer a
consumer kept still points at the old one. The old block is released before the copy, and the copy
uses `memcpy`, not a move that tolerates overlap.

### Repairing effect data after its source moves

An effect template keeps a full 64-bit source base at `+0x858`, a tagged source handle at `+0x860` and
a signed offset at `+0x864`. `003B3480` resolves the handle (`003AB7F0`), adds the sign-extended offset
and, when the result differs from `+0x858`, calls `0024D970(template, newBase)`; it repeats the test
against a second object's base at `+0x390` and repairs it with `0024D940`.

`0024D970` computes the delta as a 32-bit difference of the low halves of the new and old bases, runs
three repair walks with it (`003AA3D0`, `003A9BA0`, `003A9860`), and stores the full new base.

Each walk
sign-extends the delta and adds it to every stored pointer it covers (`003A8FF0` adds it at list
records `+0x100`, `+0x108`, `+0x18` and `+0x20`). The repair is exact only when the real distance moved
lies between −2^31 and 2^31 − 1; beyond that the base is right and every repaired pointer is wrong.
`003AA3D0` forwards the delta to the element handlers `00501420` and `00503F10`; the effect element
types `005004C0` sets up are on the
[effect element dispatch](../17-Presentation-Rendering/effect-element-runtime.md
)
page.

## Layouts

```
arena record   022D7FD0 + i*0xA8: +0x00 u8, +0x01 u8 index, +0x02 u8 dirty, +0x08 name header, +0x10 heap start,
               +0x18 heap middle, +0x20 bitmap, +0x28 page map, +0x30 slot table, +0x38 slot end, +0x40 free slot,
               +0x48 used slot, +0x50 tree root, +0x58 u32 pages, +0x5C u32 heap size, +0x60 u16 tag, +0x62 u8 moved,
               +0x90 free list bottom, +0x98 free list top, +0xA0 pressure callback
block header   +0x00 u16 0xFF12, +0x02 u8 category (022D8E18, stamped at 0036A15F; 0xFF when free), +0x03 u8 arena, +0x04/+0x08/+0x0C/+0x10 encoded links,
               +0x14 u8 bit 0 allocated, +0x15 u8 bit 0 top, bit 1 in tree, bit 2 not movable, bit 3 set while 022D8E28,
               +0x16 u8 tag, +0x18 s32 size, +0x1C u16 check word, +0x1E u16 label tag, +0x20 encoded slot,
               +0x24/+0x28/+0x2C encoded tree links, +0x34 char[8] label, +0x3E u16 must be 0 on free; payload +0x40
handle slot    +0x00 u16 next, +0x02 u16 previous, +0x04 u8 arena, +0x05 u8 in use, +0x06 u16 check word, +0x08 header
```

The arena record's fields are listed access by access in
[`resource-arena-record-accesses.tsv`](resource-arena-record-accesses.tsv) and
[`resource-arena-record-accesses-flow-sensitive.tsv`](resource-arena-record-accesses-flow-sensitive.tsv).

## Operations

Per allocation: one free-list walk and up to two header writes. Per compaction pass: one tree search and
at most one move, a header save and restore plus one payload copy.

## State

The fifteen arena records, the enabled mask `022D89B8`, the current arena `022D89BC` and its stack, and
the encoding base `01F83530`.

## Modding notes

- Keep a handle, not a payload pointer, across any allocation, and in arena 6 across a frame: any
  allocation can compact an arena, and arena 6 is compacted every frame.
- A block taken with `0036A000` stays put until it is released with `0036D170`.
- Every arena block must lie below 4 GB for the 32-bit links to work.
- Writing past a block's end into the next header ends the game at that block's free.

## Related

- [Resource sections](resource-sections.md): how data inside a loaded block is found.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): the binding system that compacts arena 6 and supplies its pressure callback.
- [File requests and the read queue](file-requests-and-the-read-queue.md): the loads that fill these blocks.
- [Effect element dispatch](../17-Presentation-Rendering/effect-element-runtime.md
): the effect elements the repair walks reach.
