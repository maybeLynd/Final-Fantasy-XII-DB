---
title: "Resource arenas and relocation: the fifteen memory arenas, block headers, handles, the movable-block tree, compaction, and how moved effect data is repaired"
kind: "system"
category: "Game files and data tables"
addresses: "022D7FD0, 00369D30, 0022A0B0, 0036C1D0, 0036C140, 022D89BC, 022D89C0, 022D89B8, 0036A490, 00369860, 0036C660, 0036A100, 0036A190, 0036BC60, 0036BFE0, 0020E600, 0020E620, 01F83530, 0036B130, 003AB7F0, 0036A000, 0036D170, 003AB880, 003AB940, 00369800, 0036A9C0, 0036B410, 0036B4E0, 0036C790, 00369C60, 0036AAD0, 0036ABE0, 0036A2A0, 004746F0, 00369CF0, 003697C0, 002E65A0, 003B3480, 0024D970, 0024D940, 003AA3D0, 003A9BA0, 003A9860, 003A8FF0, 005004C0, 0036C5A0, 002E6D60, 002EA320, 0036B160, 0036C4B0, 0036C6C0, 0036CAD0, 0036D050, 0036A240, 0037B450, 0037B330, 0024AC30, 0024AB30, 0024AB60, 0036A570, 0036A850, 00369760, 0036C1F0, 0036B670, 0036B730, 0036B7F0, 0036B8B0, 0036C9D0"
---

## What the player sees

Nothing while it works. Loaded models, effects and tables live in a handful of large memory arenas
that the game compacts as it goes, moving blocks to close gaps; a block whose header has been
overwritten makes the game write a memory dump and quit.

## How it works

### The arenas

There are fifteen arena records of `A8`<sub>h</sub> bytes at `022D7FD0`, indexed 0 to 14. `00369D30(arena, buffer,
size, slots)` builds one inside a caller's buffer: a `40`<sub>h</sub>-byte name header at the start, a page map
(one qword per 64 KB page, the page count rounded to 32) and a bitmap of `pages / 32` dwords, the
handle-slot table when `slots` is non-zero, and the block heap after them, rounded to 64 bytes. It sets
the arena's bit in the enabled mask `022D89B8` and writes the heap's first free block header.

Boot (`0022A0B0`) and four later calls build these:

| Arena | Size | Slots | Built at |
|---:|---|---:|---|
| 2 | `1DC0000`<sub>h</sub> | 16 | `0022A2AE` |
| 3 | `D20000`<sub>h</sub> | 256 | `0022A2CB` |
| 4 | `100000`<sub>h</sub> | 16 | `0022A2E7` |
| 5 | `1C0000`<sub>h</sub> | 256 | `0022A304` |
| 6 | `6C00000`<sub>h</sub> | 1,024 | `0022A321` |
| 7 | `3000000`<sub>h</sub> | 256 | `0022A33E` |
| 8 | `2000000`<sub>h</sub> | 256 | `0022A35B` |
| 9 | `1200000`<sub>h</sub> | 16 | `0022A377` |
| 11 | `400000`<sub>h</sub> | 256 | `0022A394`, rebuilt by `0037B3D0` |
| 12 | the caller's | 0 | `003E9AEF` |
| 13 | `100000`<sub>h</sub> | 0 | `0025AA21` |
| 14 | `19000`<sub>h</sub> | 0 | `0025AAC1` |

Arenas 0, 1 and 10 are built by none of them.

### Arena 11's modes

Arena 11 is rebuilt whenever its mode changes. `0037B450(mode)` stores the mode at `02ADD930`, runs
`0037B3D0` and then stores it at `02ADD931`. `0037B3D0` sets `02ADD932` to 4 and, when the two bytes
differ, calls `00369760(11)` and `0036D160(11)`, frees its block `01FD4A18` (`0036D250`), takes a
new one (`0036D240`) of `3C0000`<sub>h</sub> bytes for mode 3 or `400000`<sub>h</sub> otherwise, and builds the arena in it
with 256 slots (`00369D30`).

| Mode | Set by |
|---|---|
| `0` | boot (`0037B390`, from `0022A0B0`), `0035B8D0`, `0024AB60` |
| `1` | `0035B840`, which also takes kind 28 path `2n + 1` (`002DF980`) |
| `2` | `003DD6C0`, when a party slot has bit `1`<sub>h</sub> of `+10`<sub>h</sub> and bit `40`<sub>h</sub> of `+17`<sub>h</sub> and `0037B330()` is 0 or 2; with no such slot it stores 0 as the waiting mode (`0037B490(0)`) |
| `3` | `0024AC30`, the menu overlay load |

- A mode can also wait in `02ADD932`: `0037B490` stores it, `0037B380` reads it, and `0037B2F0` (from
  `002E65A0`) applies it as `0037B450` does unless it is 4.
- `0037B330` returns `02ADD930` while `02ADD931` is 0 and 4 otherwise. Both bytes always receive the same
  mode, so it answers 0 or 4, and `003DD4C0`'s test for 2 never passes.
- `0024AC30(n, wait)` acts only when `0037B330()` is 0: it sets mode 3 and requests kind 35, index `n + 7`,
  straight into the block `01FD4A18` with the completion `0024ACF0`, which sets `02091094`; with `wait` it
  drains the queue (`0032E520(0)`). Otherwise it only calls the do-nothing body `0016D6A0`.
- `0024AC10(n)`, called by the menu request host `0027FB70`, stores 1 in `02091094` and returns 0 for n = 1, and
  runs `0024AC30(n, 0)` for any other n.
- `0024AB60` sets mode 0 and clears `02091094` when it is set. `0024AB30`, called from the menu handler
  `00280140`, does nothing whatever it finds: it returns at once when `02091094` is 0 or `0037B330` answers
  4, and otherwise jumps to the empty body `0016D6A0` with `ecx` = `80000`<sub>h</sub>.

### The current arena

Allocation goes to the current arena `022D89BC`. `0036C1D0(arena, …)` pushes the current arena state
(arena, a tag byte, flags) onto a 16-byte stack and selects a new one; `0036C140` pops it. Popping an
empty stack spins forever, and `0036BC60` spins forever when asked to allocate with nothing pushed
(`022D89C0` = 0).

`0036C1D0` is an entry stub: it passes stack 0 and the qword at its stack pointer + 4, minus 5
(`0036C1D7`), and jumps to the body `0036C1F0(arena, category, stack, value)`. The body:

1. reads the stack's depth from `022D89C0 + stack × 4` and spins forever at a depth of 31 or more;
2. saves the current arena `022D89BC`, the category byte `022D8E18`, the byte `022D8E28` and the
   qword `022D8E20` in entry `depth` at `022D89D0 + (stack × 32 + depth) × 10h`, and adds 1 to the depth;
3. stores `category` in `022D8E18` and `value` in `022D8E20`, and makes the arena the byte at
   `022D89A8 + arena` the new current arena.

`0036C140` reads the same four fields back from stack 0's top entry.

### Blocks

Every block, used or free, starts with a `40`<sub>h</sub>-byte header written by `0036A490`: magic `FF12`<sub>h</sub> at
`+00`<sub>h</sub>, the arena at `+03`<sub>h</sub>, the size at `+18`<sub>h</sub>, a tag word at `+1C`<sub>h</sub>, and encoded links at `+04`<sub>h</sub>,
`+08`<sub>h</sub>, `+0C`<sub>h</sub>, `+10`<sub>h</sub> and `+20`<sub>h</sub>..`+30`<sub>h</sub>. The payload follows at `+40`<sub>h</sub>.

`0036BC60(arena, size, block, fromTop)` rounds the size up to a multiple of 64 and, with no block
given, walks the free list from `+90`<sub>h</sub> (bottom up, through `+08`<sub>h</sub>) or `+98`<sub>h</sub> (top down, through
`+04`<sub>h</sub>) for the first block at least that large.

It carves the allocation from the bottom or the top
of that block, writes a new header for any remainder of at least 0 bytes, sets the allocation's
`+14`<sub>h</sub> bit 0 (allocated), `+15`<sub>h</sub> bit 0 for a top allocation and `+16`<sub>h</sub> = the current tag, and
returns the payload. `0036A100(size)` allocates bottom-up in the current arena and `0036A190` (through
`0036A1A0`) top-down; when that fails both fall to `0036BFE0`.

`0036C660(payload, name, tag)` labels a block: when the header carries the magic and is allocated, it
copies seven characters of the name to `+34`<sub>h</sub>, terminates it, stores the tag at `+1E`<sub>h</sub> and zeroes
`+3E`<sub>h</sub>.

`00369860(payload, caller)` frees a block. A payload whose header lacks the magic, or whose `+3E`<sub>h</sub> is
non-zero, makes it format a dump of `B0`<sub>h</sub> header bytes and `D0`<sub>h</sub> caller bytes, record the arena in
`022D89BC`, call `0036A570(arena, Bh)` and `exit(1)`.

`0036A570(arena, flags, category)` walks an enabled arena and prints nothing. Per flag bit it follows
the blocks from the heap start `+10`<sub>h</sub> (bit 0, building a state label from each header's flags and
copying the name of a block of `category`, or of any block for a negative one), the free list from
`+90`<sub>h</sub> (bit 1), the used and free slot chains from `+48`<sub>h</sub> and `+40`<sub>h</sub> (bits 3 and 4) and, for bit 5,
the tree from `+50`<sub>h</sub> through `0036A850`, which recurses on each node's `+24`<sub>h</sub> link and follows
`+28`<sub>h</sub>. The labels stay in a local buffer that no output call receives.

`00369760(arena)` returns 1 for a disabled arena or one whose `+10`<sub>h</sub>, `+90`<sub>h</sub> and `+98`<sub>h</sub> are equal;
otherwise it runs the walk with all flags (`3F`<sub>h</sub>) and returns 0. `0036C0F0` runs it with flag 1.

### Block chains

Every header is on the address chain, previous block at `+0C`<sub>h</sub> and next at `+10`<sub>h</sub>, which the walk
follows from the heap start (`0036A570`). A free block is also on the free chain, previous at
`+04`<sub>h</sub> and next at `+08`<sub>h</sub>, whose ends are record `+90`<sub>h</sub> and `+98`<sub>h</sub>. All four links are encoded
offsets. Four helpers link a header `b` beside a header `a`:

| Helper | Chain | Puts `b` |
|---|---|---|
| `0036B670(a, b)` | free | after `a` |
| `0036B730(a, b)` | free | before `a` |
| `0036B7F0(a, b)` | address | after `a` |
| `0036B8B0(a, b)` | address | before `a` |

- Each first checks `b`'s `+3E`<sub>h</sub>: when it is non-zero it walks the current arena with flags `B`<sub>h</sub>
  (`0036A570`) and calls `exit(1)`. It then zeroes `+3E`<sub>h</sub> on every header whose links it rewrites.
- With a null `a`, `b` gets null links on that chain.
- `0036C9D0(header, both)` takes a header off the free chain and, when `both` is set, off the address
  chain too, writing `FF99`<sub>h</sub> over its magic so the header no longer counts as a block; it zeroes `+3E`<sub>h</sub>.

The carving in `0036BC60` uses all of them: it takes the chosen free block off both chains, puts the
allocation and the remainder on the address chain where the old block was, and puts the remainder on
the free chain beside the old block's free neighbours. The free `00369860`, the resize helpers
`0036C290` and `0036C380` (from `0036CB00`), `0036B2C0` and `0036B980` call them too.

### The 32-bit address encoding

Links inside headers and many other stored references are 32-bit values. `0020E600(v)` decodes them as
`base + (u64)v` and `0020E620(p)` encodes them as `low32(p) − low32(base)`, with the base at
`01F83530`. That cell lies in the zero-filled tail of `.data`, so the base is 0 at load and every
encoded block must sit below 4 GB.

### Handles

A handle is the address of a 16-byte slot in an arena's slot table with tag bits in its low two bits:
`{+00h u16 next, +02h u16 previous, +04h u8 arena, +05h u8 in use, +06h u16 check word, +08h
header pointer}`. The table at record `+30`<sub>h</sub> starts as one free chain headed at `+40`<sub>h</sub>; slots in use
hang off `+48`<sub>h</sub>.

- `0036A000(handle)` (and `003AB880`, which passes a value with clear tag bits through unchanged)
  checks that the handle is tagged, at least `100000`<sub>h</sub>, and that the slot's `+06`<sub>h</sub> equals the
  header's `+1C`<sub>h</sub>; it then takes the block out of the movable tree (when `+15`<sub>h</sub> bit 1 says it is in
  it) and returns the payload.
- `0036D170(handle)` (and `003AB940`) makes the same check and, when the block is not in the tree,
  puts it back and sets `+15`<sub>h</sub> bit 1.
- `0036B130(handle)` returns `[slot + 8] + 40h` with no check word test, so a stale handle resolves
  to whatever the slot holds now. `003AB7F0` wraps it and returns 0 when the low 32 bits of the
  result are `40`<sub>h</sub> or less.
- `0036A0B0(handle)` checks only the tag bits and the `100000`<sub>h</sub> floor, sets the block's `+15`<sub>h</sub> bit 2 when it
  is clear, zeroing `+3E`<sub>h</sub>, and returns the payload `+40`<sub>h</sub>, or 0; `0036D200(handle)` clears that bit and
  `+3E`<sub>h</sub> again. The sound-bank loaders `002E60F0`, `0036E9F0`, `0036EAB0`, `0036ED50` and `003A1650` use the
  first, `002E60F0` and `003A0EA0` the second.
- `00369800(handle)` frees the slot (`0036A9C0`: unlinks it, takes the block out of the tree, zeroes
  the slot) and then the block (`00369860`).
- `0036B160(size)` allocates a block with a handle in the current arena: bottom-up (`0036BC60`, then
  `0036BFE0`), then `0036C4B0(arena, payload)`, which puts the block in the movable tree (`0036B410`),
  sets `+15`<sub>h</sub> bit 1 and clears bit 2, and takes a free slot (`0036AF20`).
- When no slot is free, `0036C4B0` takes the block out of the tree again, frees it and returns 0; a slot
  value without tag bits or below `100000`<sub>h</sub> makes it write to address 8, a deliberate crash; otherwise
  the slot's `+08`<sub>h</sub> gets the header and the handle is returned.
- `0036A240(slot, header)` binds a slot to a header: the slot's `+08`<sub>h</sub> and check word `+06`<sub>h</sub> (from the
  header's `+1C`<sub>h</sub>), and the header's encoded slot `+20`<sub>h</sub>; it also zeroes the header's `+3E`<sub>h</sub>.
- `0036C6C0(handle, name, tag)` labels a handle's block as `0036C660` labels a payload's, once the
  handle is tagged and at least `100000`<sub>h</sub> and its header carries the magic and is allocated.
- `0036CAD0(payload, size)` resizes a block in the current arena through `0036D050`: a size of 0 frees
  it, a null payload allocates (`0036BFE0`), and any other goes to `0036CB00`.

### The movable-block tree

Each arena keeps the blocks that may be moved in a binary tree rooted at record `+50`<sub>h</sub> (a full
pointer). A block's left, right and parent links are encoded offsets at `+24`<sub>h</sub>, `+28`<sub>h</sub> and `+2C`<sub>h</sub>,
and it is ordered by its size `+18`<sub>h</sub> as a signed value; an equal size goes right (`0036B4E0`).
`0036B410` clears a block's links and `+3E`<sub>h</sub> and inserts it, or makes it the root of an empty tree;

`0036C790` removes it, relinking children with `0036B490` (left, `+24`<sub>h</sub>) and `0036B5A0` (right,
`+28`<sub>h</sub>), which also set the child's parent link `+2C`<sub>h</sub>. Acquiring a handle takes its block out;
releasing it puts it back.

### Compaction

`00369C60(arena, repeat)` does nothing for a disabled arena or an empty tree. Otherwise it runs the
exact pass once and the adjacent pass once, or repeatedly while `repeat` is set and a pass moves
something, and on any move sets record `+02`<sub>h</sub> and the moved latch `+62`<sub>h</sub>. It returns the number of
moves.

- **Exact pass** `0036AAD0`: for the free block at the head of `+90`<sub>h</sub>, it searches the tree for a block
  of the same size at a higher address (low 32 bits compared unsigned) whose `+15`<sub>h</sub> bit 2 is clear,
  and moves it into the hole.
- **Adjacent pass** `0036ABE0`: for each free block, when the block physically after it is in the tree
  and not inhibited (`+15h & 6` = 2) and allocated, it moves that block down; otherwise it searches
  for an equal-size block higher up as above. It moves at most one block per call.

`0036BFE0(arena, size)` is the pressure path: it calls the arena's callback at record `+A0`<sub>h</sub> when one
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
2. points the source's handle slot at the hole's header, sets the hole's `+20`<sub>h</sub> backlink and copies
   the check word;
3. frees the source (`00369860`) and copies `source +18h` payload bytes into the hole with `memcpy`
   (`004746F0`);
4. claims the hole (`0036BC60(arena, size, hole, 0)`), restores the saved fields and name, puts it back
   in the tree when the source was there, and republishes the slot.

The handle value stays the same across a move and resolves to the new address; a raw pointer a
consumer kept still points at the old one. The old block is released before the copy, and the copy
uses `memcpy`, not a move that tolerates overlap.

### Repairing effect data after its source moves

An effect template keeps a full 64-bit source base at `+858`<sub>h</sub>, a tagged source handle at `+860`<sub>h</sub> and
a signed offset at `+864`<sub>h</sub>. `003B3480` resolves the handle (`003AB7F0`), adds the sign-extended offset
and, when the result differs from `+858`<sub>h</sub>, calls `0024D970(template, newBase)`; it repeats the test
against a second object's base at `+390`<sub>h</sub> and repairs it with `0024D940`.

`0024D970` computes the delta as a 32-bit difference of the low halves of the new and old bases, runs
three repair walks with it (`003AA3D0`, `003A9BA0`, `003A9860`), and stores the full new base.

Each walk
sign-extends the delta and adds it to every stored pointer it covers (`003A8FF0` adds it at list
records `+100`<sub>h</sub>, `+108`<sub>h</sub>, `+18`<sub>h</sub> and `+20`<sub>h</sub>). The repair is exact only when the real distance moved
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

`ArenaStackEntry` (`10`<sub>h</sub> bytes, offsets from the start of the 022D89D0+(stack*32+depth)*`10`<sub>h</sub>):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | arena | the current arena `022D89BC` |
| `02`<sub>h</sub> | `u8` | category | `022D8E18` |
| `03`<sub>h</sub> | `u8` | flag | `022D8E28` |
| `04`<sub>h</sub> | `u32` | pad | not written by `0036C1F0` |
| `08`<sub>h</sub> | `u64` | value | `022D8E20` |

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
