[Home](../../README.md) / [Game files and data tables](README.md) / Resource arenas and relocation

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Resource arenas and relocation: the fifteen memory arenas, block headers, handles, the movable-block tree, compaction, and how moved effect data is repaired | system | Game files and data tables | Loaded resources | How the game's resource memory is laid out and moved: the arena records and their boot sizes, the current-arena stack, the 0x40-byte block header and its corruption check, suballocation from the free lists, the 32-bit address encoding, tagged handles and their slot table, acquiring and releasing a handle and the tree of blocks that may move, compaction and the allocation-pressure retry, the mover's order of operations, and how an effect file's stored pointers are repaired after its source moves, with the 32-bit limits each step carries. | 0x022D7FD0, 0x00369D30, 0x0022A0B0, 0x0036C1D0, 0x0036C140, 0x022D89BC, 0x022D89C0, 0x022D89B8, 0x0036A490, 0x00369860, 0x0036C660, 0x0036A100, 0x0036A190, 0x0036BC60, 0x0036BFE0, 0x0020E600, 0x0020E620, 0x01F83530, 0x0036B130, 0x003AB7F0, 0x0036A000, 0x0036D170, 0x003AB880, 0x003AB940, 0x00369800, 0x0036A9C0, 0x0036B410, 0x0036B4E0, 0x0036C790, 0x00369C60, 0x0036AAD0, 0x0036ABE0, 0x0036A2A0, 0x004746F0, 0x00369CF0, 0x003697C0, 0x002E65A0, 0x003B3480, 0x0024D970, 0x0024D940, 0x003AA3D0, 0x003A9BA0, 0x003A9860, 0x003A8FF0, 0x005004C0, 0x0036C5A0, 0x002E6D60, 0x002EA320, 0x0036B160, 0x0036C4B0, 0x0036C6C0, 0x0036CAD0, 0x0036D050, 0x0036A240, 0x0037B450, 0x0037B330, 0x0024AC30, 0x0024AB30, 0x0024AB60, 0x0036A570, 0x0036A850, 0x00369760, 0x0036C1F0, 0x0036B670, 0x0036B730, 0x0036B7F0, 0x0036B8B0, 0x0036C9D0, 0x00378BC0 |

## What the player sees

Nothing while it works. Loaded models, effects and tables live in a handful of large memory arenas
that the game compacts as it goes, moving blocks to close gaps; a block whose header has been
overwritten makes the game write a memory dump and quit.

A block keeps its handle when compaction moves it, but an address kept elsewhere still points at the old place.
Effects keep addresses into their source data, so the game compares the source's current address with the one the
effect stored and, when they differ, shifts every kept address by the distance moved.

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
- `0x0024AC30(n, wait)` first sizes kind 35, index `n + 7` (`0x0032E400`, `0x0024AC4C`) and acts only when `0x0037B330()`
  is 0: it sets mode 3 (`0x0037B450(3)`, `0x0024AC7F`) and requests kind 35, index `n + 7`, with that size,
  straight into the block `0x01FD4A18` as it stands after the mode change, with the completion `0x0024ACF0`, which
  sets `0x02091094`; with `wait` it drains the queue (`0x0032E520(0)`).
- The request's descriptor (`0x0024AC5C`-`0x0024AC9F`) has offset 0, callback word 0, `0x0024ACF0` as the delivery
  and failure callback and no cancel callback.
- Otherwise, after the same size lookup, `0x0024AC30` only calls the do-nothing body `0x0016D6A0` (with `0x80000`,
  `0x0024ACC1`). It returns 0 on every path (`0x0024ACAF`, `0x0024ACD0`).
- `0x0024AC10(n)`, called by the menu request host `0x0027FB70`, stores 1 in `0x02091094` and returns 0 for n = 1, and
  runs `0x0024AC30(n, 0)` for any other n.
- `0x0024AB60` sets mode 0 and clears `0x02091094` when it is set. `0x0024AB30`, called from the menu handler
  `0x00280140`, does nothing whatever it finds: it returns at once when `0x02091094` is 0 or `0x0037B330` answers
  4, and otherwise jumps to the empty body `0x0016D6A0` with `ecx` = `0x80000`.

### The current arena

Allocation goes to the current arena `0x022D89BC`. `0x0036C1D0(arena, …)` pushes the current arena state
(arena, a tag byte, flags) onto a 16-byte stack and selects a new one; `0x0036C140` pops it. Popping an
empty stack spins forever, and `0x0036BC60` spins forever when asked to allocate with no block given and nothing
pushed (`0x022D89C0` = 0, `0x0036BC79`-`0x0036BC87`); with a block given it does not read the depth.

`0x0036C1D0` is an entry stub: it passes stack 0 and the qword at its stack pointer + 4, minus 5
(`0x0036C1D7`), and jumps to the body `0x0036C1F0(arena, category, stack, value)`. The body:

1. reads the stack's depth from `0x022D89C0 + stack × 4` and spins forever at a depth of 31 or more;
2. saves the current arena `0x022D89BC`, the category byte `0x022D8E18`, the byte `0x022D8E28` and the
   qword `0x022D8E20` in entry `depth` at `0x022D89D0 + (stack × 32 + depth) × 0x10`, and adds 1 to the depth;
3. stores `category` in `0x022D8E18` and `value` in `0x022D8E20`, and makes the arena the byte at
   `0x022D89A8 + arena` the new current arena.

`0x0036C140` reads the same four fields back from stack 0's top entry.

The current tag `0x022D8E1C`, which `0x0036BC60` stores at a new block's `+0x16` (`0x0036BE8D`), has a stack of its own:
31 bytes at `0x022D8DD0`. `0x0036C1A0(tag)` pushes the current tag and makes `tag` current, doing nothing at a depth of
31 or more; `0x0036C110()` pops it while the depth is not negative. Each has 21 call sites (the map pack's `0x00378030`
among them, around its allocation). A pop at depth 0 still runs: the depth becomes -1 and the tag comes from
`0x022D8DCF`, the byte before the stack.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022D89C8` | `i32` | 0 (zero-filled tail of `.data`) | the depth of the tag stack at `0x022D8DD0` | `0x00369D30`, 0 while no arena is enabled (`0x00369D8A`, an 8-byte store that also zeroes `0x022D89CC`); `0x0036C1A0`, 1 more (`0x0036C1C2`); `0x0036C110`, 1 less (`0x0036C123`) | `0x0036C1A0` (`0x0036C1A0`, sign-extended); `0x0036C110` (`0x0036C110`) |

### Blocks

Every block, used or free, starts with a `0x40`-byte header written by `0x0036A490`: magic `0xFF12` at
`+0x00`, the arena at `+0x03`, the size at `+0x18`, a check word at `+0x1C` (the arena record's handle serial
`+0x60`, Layouts), and encoded links at `+0x04`, `+0x08`, `+0x0C`, `+0x10` and `+0x20`..`+0x30`. The payload
follows at `+0x40`.

`0x0036A490(arena, header, size, word)` writes nothing for a null header (`0x0036A493`). Otherwise every link it
writes is the encoding of a null pointer (`0x0020E620(0)`). It also stores `0xFF` at `+0x02` (`0x0036A4C6`), zeroes
the words `+0x14`, `+0x16` and `+0x1E` (`0x0036A504`, `0x0036A4CD`, `0x0036A4BC`), and then sets `+0x15` to 8 while
`0x022D8E28` is non-zero (`0x0036A4F6`-`0x0036A514`). It clears the label byte `+0x34` and the dword `+0x3C`, which
holds the guard word `+0x3E` (`0x0036A550`, `0x0036A554`).

`0x0036BC60(arena, size, block, fromTop)` rounds the size up to a multiple of 64, sets the arena record's byte
`+0x02` to 1 (`0x0036BCC5`) and, with no block given, returns 0 when the arena's bit in `0x022D89B8` is clear
(`0x0036BCD2`-`0x0036BCE9`) and otherwise walks the free list from `+0x90` (bottom up, through `+0x08`) or `+0x98`
(top down, through `+0x04`) for the first block at least that large.

It carves the allocation from the bottom or the top
of that block. When the block holds at least `0x40` bytes beyond the allocation, room for a header
(`0x0036BDD9`-`0x0036BDE0`), the rest becomes a free block of its own, even with an empty payload; otherwise
the whole block is taken. It sets the allocation's
`+0x14` bit `0x1` (allocated), `+0x15` bit `0x1` for a top allocation and `+0x16` = the current tag, and
returns the payload. `0x0036A100(size)` allocates bottom-up in the current arena and `0x0036A190` (through
`0x0036A1A0`) top-down; when that fails both fall to `0x0036BFE0`.

On success `0x0036A100` stamps the header: the category byte `0x022D8E18` at `+0x02` (`0x0036A15F`), the encoding
of a null pointer (`0x0020E620(0)`) at the dword `+0x30` (`0x0036A167`) and 0 in the guard word `+0x3E`
(`0x0036A16D`). It returns the payload, or null when `0x0036BFE0` also fails (`0x0036A154`).

`0x0036C660(payload, name, tag)` labels a block: when the header carries the magic and is allocated, it
copies seven characters of the name to `+0x34`, terminates it, stores the tag at `+0x1E` and zeroes
`+0x3E`. It writes nothing for a null payload, a header without the magic or one whose `+0x14` bit `0x1` is
clear (`0x0036C673`-`0x0036C684`), and returns the payload on every path (`0x0036C6A4`). The copy is
`strncpy(header + 0x34, name, 7)` and the terminator is the byte `+0x3B` (`0x0036C686`-`0x0036C696`).

`0x00369860(payload, caller)` frees a block. A payload whose header lacks the magic makes it format a dump of `0xB0`
header bytes and `0xD0` caller bytes; a header whose `+0x3E` is non-zero makes it format
`TkFreeMain:MCB Broken:from %p` with the caller. Both then record the arena in `0x022D89BC`, call `0x0036A570(arena, 0xB)`
and `exit(1)` (`0x003698D5`-`0x00369A79`, `0x00369A80`-`0x00369AB7`).

A payload with tag bits and a block whose `+0x14` bit `0x1` is clear get a formatted line from `0x00369860` and are not
freed (`0x00369892`, `0x00369ABE`).

`0x0036A570(arena, flags, category)` walks an enabled arena and prints nothing. Per flag bit it follows
the blocks from the heap start `+0x10` (bit `0x1`, building a state label from each header's flags and
copying the name of a block of `category`, or of any block for a negative one), the free list from
`+0x90` (bit `0x2`), the used and free slot chains from `+0x48` and `+0x40` (bits `0x8` and `0x10`) and, for bit `0x20`,
the tree from `+0x50` through `0x0036A850`, which recurses on each node's `+0x24` link and follows
`+0x28`. The labels stay in a local buffer that no output call receives.

`0x00369760(arena)` returns 1 for a disabled arena, for an arena number above 14 (`0x0036977C`) or one whose
`+0x10`, `+0x90` and `+0x98` are equal; otherwise it runs the walk with all flags (`0x3F`) and category −1,
every block (`0x003697A7`-`0x003697B2`), and returns 0. `0x0036C0F0` runs it with flag 1.

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

- Each returns at once for a null `b` (`0x0036B670`, `0x0036B730`, `0x0036B7F0`, `0x0036B8B0`). Each then checks
  `b`'s `+0x3E`: when it is non-zero it walks the current arena with flags `0xB` and category −1
  (`0x0036A570`) and calls `exit(1)`. It then zeroes `+0x3E` on every header whose links it rewrites.
- With a null `a`, `b` gets null links on that chain.
- `0x0036C9D0(header, both)` takes a header off the free chain and, when `both` is set, off the address
  chain too, writing `0xFF99` over its magic so the header no longer counts as a block; it zeroes `+0x3E`.
- `0x0036C9D0` does nothing for a null header (`0x0036C9D3`). On each chain it joins the header's two
  neighbours to each other, zeroing their `+0x3E`, and gives the header's own two links the encoding of a
  null pointer (`0x0036C9EB`-`0x0036CA4B`, `0x0036CA52`-`0x0036CAAB`). It takes no arena record, so the free chain's
  ends `+0x90` and `+0x98` are left to its callers.

The carving in `0x0036BC60` uses all of them: it takes the chosen free block off both chains, puts the allocation and
the remainder on the address chain where the old block was, and puts the remainder on the free chain beside the old
block's free neighbours. The free `0x00369860`, the resize `0x0036CB00` and its helpers `0x0036C290` and `0x0036C380`,
`0x0036B2C0` and `0x0036B980` call them too.

In the carving, a chain end `+0x90` or `+0x98` that held the old block takes the remainder, or with no remainder the
old block's free-chain neighbour (`0x0036BDE4`-`0x0036BE27`). The page map `+0x28` holds at most one free block per 64 KB
page: when it holds the old block, `0x0036C900` (`0x0036BE34`) hands that entry to the old block's free-chain next if it
lies in the same page and otherwise clears the entry and the page's bit in the bitmap `+0x20` (`0x0036C94C`-`0x0036C9AE`).

The remainder takes its page's entry and sets the bit only when the page has no entry or one at a higher address
(`0x0036B5F0`, `0x0036BEAA`, `0x0036B617`-`0x0036B667`). Last, `0x0036B210` joins the remainder with the free blocks that are
its neighbours on both chains (`0x0036BF6B`), so the remainder can end up inside a larger free block; neither call is
made when the carving leaves no remainder (`0x0036BE96`, `0x0036BEEE`, `0x0036BEFF`).

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
  header's `+0x1C`; it then takes the block out of the movable tree (when `+0x15` bit `0x2` says it is in
  it) and returns the payload.
- `0x0036A000` tests the handle as a 32-bit value and returns 0 for 0, for an untagged or smaller value, for a
  slot whose header pointer `+0x08` is null and for a check word that differs (`0x0036A006`-`0x0036A03C`, `0x0036A099`).
- In `0x0036A000` the tree removal is `0x0036C790(arena record, header, 0x1263)`, with the arena record
  `0x022D7FD0 + 0xA8 ×` the header's byte `+3`, or null for an arena number of 15 or more; it then clears bit `0x2`
  of `+0x15` and zeroes the `u16` `+0x3E` (`0x0036A044`-`0x0036A080`). The payload is the header plus `0x40` on both
  paths (`0x0036A07C`, `0x0036A08F`).
- `0x0036D170(handle)` (and `0x003AB940`) makes the same handle and check-word tests and, when the block is
  not in the tree, puts it back and sets `+0x15` bit `0x2`.
- `0x0036D170` returns at once for a handle whose low 32 bits are 0, carry no tag bits or are below
  `0x100000` (`0x0036D174`-`0x0036D183`). It has no null-header test: it compares the slot's `+0x06` with
  `[header + 0x1C]` straight away (`0x0036D196`-`0x0036D1A2`), so a slot whose `+0x08` is null makes it read
  address `0x1C`. `0x003AB940` jumps to it for any non-zero tagged value (`0x003AB957`).
- The re-entry is `0x0036B410(record, header, 0x12DD)`, with the record of the header's byte `+0x03`, null for
  15 or more (`0x0036D1AA`-`0x0036D1D9`); it then sets bit `0x2` and zeroes `+0x3E` (`0x0036D1DE`-`0x0036D1E2`). Bit
  `0x4` is left as it is.
- `0x0036B130(handle)` returns `[slot + 8] + 0x40` with no check word test, so a stale handle resolves
  to whatever the slot holds now. `0x003AB7F0` wraps it and returns 0 when the low 32 bits of the
  result are `0x40` or less.
- `0x003AB7F0(h)` returns 0 for 0 (`0x003AB7FA`) and a value without tag bits unchanged (`0x003AB846`); only a
  tagged value goes to `0x0036B130`, which receives its low 32 bits (`0x003AB82A`-`0x003AB838`).
- `0x0036A0B0(handle)` checks only `(handle & 3) != 0 && handle >= 0x100000` (unsigned; `0x0036A0BA`-`0x0036A0C5`),
  takes
  the header `[(handle & ~3) + 8]`, sets the block's `+0x15` bit `0x4` when it is clear, zeroing `+0x3E`, and returns the payload `+0x40`, or 0; `0x0036D200(handle)` clears that bit and
  `+0x3E` again. The sound-bank loaders `0x002E60F0`, `0x0036E9F0`, `0x0036EAB0`, `0x0036ED50` and `0x003A1650` use the
  first, `0x002E60F0` and `0x003A0EA0` the second.
- `0x00369800(handle)` frees the slot (`0x0036A9C0`: unlinks it, takes the block out of the tree, zeroes
  the slot) and then the block (`0x00369860`).
- `0x00369800` does nothing for a handle whose low 32 bits are 0, carry no tag bits or are below `0x100000`
  (`0x00369804`-`0x00369813`). The slot is the low 32 bits with the tag bits cleared (`0x00369815`-`0x0036981A`).
  It reads the header pointer `+0x08` before freeing the slot and, when it is non-null, tail-jumps to
  `0x00369860(header + 0x40, 0)` (`0x00369824`-`0x00369846`).
- `0x0036A9C0(slot)` does nothing for a null slot or one whose in-use byte `+0x05` is 0 (`0x0036A9C3`,
  `0x0036A9D5`). It takes the record of the slot's arena byte `+0x04`, null for 15 or more
  (`0x0036A9EB`-`0x0036AA03`); nothing tests that null, and the unlink's first access to the record faults on it
  (`0x0036AA1C`, `0x0036AA32` or `0x0036AA3E`).
- `0x0036A9C0` then unlinks the slot from the used chain (indices `+0x00` next and `+0x02`
  previous, `0xFFFF` at a chain end; head `+0x48`) and pushes it at the head of the free chain `+0x40`
  (`0x0036AA06`-`0x0036AA77`).
- When the slot's header is non-null, `0x0036A9C0` clears its `+0x15` bit `0x4` and zeroes `+0x3E`. When bit
  `0x2` is set it takes the block out of the tree (`0x0036C790(record, header, 0x1087)`), clears bit `0x2` and
  zeroes `+0x3E` again (`0x0036AA7B`-`0x0036AAA4`). Last it zeroes the slot's `+0x05`, `+0x06` and `+0x08`
  (`0x0036AAAD`-`0x0036AAB5`).
- `0x0036B160(size)` allocates a block with a handle in the current arena: bottom-up (`0x0036BC60`, then
  `0x0036BFE0`), then `0x0036C4B0(arena, payload)`, which puts the block in the movable tree (`0x0036B410`),
  sets `+0x15` bit `0x2` and clears bit `0x4`, and takes a free slot (`0x0036AF20`).
- `0x0036B160` reads the current arena `0x022D89BC` once and passes it to all three (`0x0036B16F`-`0x0036B1AE`); it
  calls `0x0036C4B0` even when both allocations failed. It returns 0 when `0x0036C4B0` returns 0 (`0x0036B1B7`).
- Otherwise `0x0036B160` acquires the handle (`0x0036A000`) and stamps the header: the category byte `0x022D8E18`
  at `+0x02`, the encoding of a null pointer at the dword `+0x30` and 0 at `+0x3E` (`0x0036B1C0`-`0x0036B1D9`).
  It then releases the handle (`0x0036D170`) and returns it (`0x0036B1DD`-`0x0036B1E2`).
- `0x0036C4B0` returns 0 at once for a null payload (`0x0036C4BC`). It uses the record of `arena`, null for an
  arena number above 14 (`0x0036C4D3`-`0x0036C4EE`), and asks `0x0036AF20` for a slot of the arena named by the
  header's byte `+0x03` (`0x0036C50D`, `0x0036C51C`).
- When no slot is free, `0x0036C4B0` takes the block out of the tree again, frees it and returns 0; a slot
  value without tag bits or below `0x100000` makes it write to address 8, a deliberate crash; otherwise
  the slot's `+0x08` gets the header and the handle is returned.
- In that last case the slot is the handle's low 32 bits with the tag bits cleared (`0x0036C56A`-`0x0036C572`),
  and `0x0036C4B0` zeroes `+0x3E` on every path that reaches `0x0036AF20` (`0x0036C515`, `0x0036C521`, `0x0036C578`,
  `0x0036C587`).
- `0x0036A240(slot, header)` binds a slot to a header: the slot's `+0x08` and check word `+0x06` (from the
  header's `+0x1C`), and the header's encoded slot `+0x20`; it also zeroes the header's `+0x3E`. A null
  slot or a null header makes it return with nothing written (`0x0036A243`, `0x0036A258`).
- `0x0036C6C0(handle, name, tag)` labels a handle's block as `0x0036C660` labels a payload's, once the
  handle is tagged and at least `0x100000` and its header carries the magic and is allocated.
- `0x0036C6C0` tests the handle's low 32 bits (`0x0036C6CF`-`0x0036C6DF`), takes the slot as those bits with the
  tag bits cleared, and writes nothing when the slot's header pointer `+0x08` is null (`0x0036C6F2`-`0x0036C6F9`).
  It returns the handle on every path (`0x0036C735`).
- `0x0036CAD0(payload, size)` resizes a block through `0x0036D050`: a size of 0 frees it, a null payload allocates in the
  current arena `0x022D89BC` (`0x0036BFE0`), and any other goes to `0x0036CB00` in the arena named by the header's byte
  `+0x03` (`0x0036D0C6`).
- In `0x0036D050` a size of 0 frees a non-null payload with `0x00369860(payload, 0)` and returns 0
  (`0x0036D05A`-`0x0036D06E`). A null payload goes straight to the pressure path `0x0036BFE0` (`0x0036D075`-`0x0036D08F`),
  so the pressure callback, when one is set, and a compaction run before its first try.
- Otherwise `0x0036D050` rounds the size up to a multiple of 64, `r = (s + 63 + (s + 63 < 0 ? 63 : 0)) & ~63`
  (`cdq`, `and edi, 0xffffffc0`, `0x0036D09E`-`0x0036D0CF`), takes the record of the header's byte
  `+0x03`, null for 15 or more, and subtracts the old size from the group total of `+0x17` when that group
  is non-zero (`0x0036D09E`-`0x0036D0FE`). It then calls `0x0036CB00(record, header, payload, rounded size)`
  (`0x0036D117`).
- With `h` = payload - `0x40`: record = `0x022D7FD0 + 0xA8 × h[+0x03]` when `h[+0x03] < 15`
  (`0x0036D0C6`-`0x0036D0E8`), and `[0x022D8E10 + 4 × h[+0x17]] -= h[+0x18]` when `h[+0x17] != 0`
  (`0x0036D0EC`-`0x0036D0FE`).
- When `0x0036CB00` returns a block, `0x0036D050` adds the size change to the `u32` at record
  `+0x68 + 4 ×` the old header's byte `+0x16`, and adds the new block's `+0x18` to the group total of its
  `+0x17` when that group is non-zero (`0x0036D124`-`0x0036D138`). It returns that block, or null with the old
  size already subtracted.

### The movable-block tree

Each arena keeps the blocks that may be moved in a binary tree rooted at record `+0x50` (a full
pointer). A block's left, right and parent links are encoded offsets at `+0x24`, `+0x28` and `+0x2C`,
and it is ordered by its size `+0x18` as a signed value; an equal size goes right (`0x0036B4E0`).
`0x0036B410` clears a block's links and `+0x3E` and inserts it, or makes it the root of an empty tree.

`0x0036B410(record, header)` does nothing for a null header (`0x0036B413`); the links it clears get the
encoding of a null pointer (`0x0036B42E`-`0x0036B449`), and a non-empty tree goes to `0x0036B4E0(root, header)`
(`0x0036B477`). `0x0036B4E0(node, header)` does nothing for a null header or node (`0x0036B4E3`, `0x0036B4FC`). It
descends left while the node's size is greater and right otherwise, to the first empty link
(`0x0036B507`-`0x0036B541`). There it sets the header's parent link `+0x2C` to the node and the node's `+0x24` or
`+0x28` to the header, and zeroes `+0x3E` on both (`0x0036B543`-`0x0036B57D`).

`0x0036C790` removes it, relinking children with `0x0036B4E0`, `0x0036B490` (left, `+0x24`) and `0x0036B5A0`
(right, `+0x28`); the last two also set the child's parent link `+0x2C`. Acquiring a handle takes its
block out; releasing it puts it back.

`0x0036C790(record, header, line)` does nothing for a null header (`0x0036C793`) and leaves the removed
header's own links as they were. It acts by the header's decoded parent, left child and right child
(`0x0036C7AC`-`0x0036C7D2`):

- no parent and a right child: the right child becomes the root `+0x50` with a null parent link and its
  `+0x3E` zeroed, and the left subtree is inserted under it with `0x0036B4E0` (`0x0036C7E4`-`0x0036C804`);
- no parent and only a left child: the left child becomes the root with a null parent link and its `+0x3E`
  zeroed (`0x0036C813`-`0x0036C823`); with no child the root becomes null (`0x0036C82C`);
- a parent and a right child: the left subtree is inserted under the right child (`0x0036B4E0`), the right
  child's parent link becomes the parent, the parent's `+0x24` or `+0x28` that held the header gets the
  right child, and both zero `+0x3E` (`0x0036C83C`-`0x0036C89A`);
- a parent and no right child: `0x0036B490` or `0x0036B5A0` hangs the left child, which may be null, on the
  parent's link that held the header and zeroes `+0x3E` on the parent and on a non-null left child
  (`0x0036C8A0`-`0x0036C8D7`, `0x0036B4B4`, `0x0036B4C5`, `0x0036B5C4`, `0x0036B5D5`).

### Compaction

`0x00369C60(arena, repeat)` does nothing for a disabled arena or an empty tree. Otherwise it runs the
exact pass once and the adjacent pass once, or repeatedly while `repeat` is set and a pass moves
something, and on any move sets record `+0x02` and the moved latch `+0x62`. It returns the number of
moves.

`0x00369C60` hands `repeat` to the exact pass, which repeats itself (`0x00369CAE`), and itself calls the
adjacent pass again while `repeat` is set and the last call moved a block (`0x00369CB5`-`0x00369CC5`). The count
is the exact pass's moves plus 1 per moving adjacent call (`0x00369CB3`, `0x00369CC1`). A disabled arena returns
0 (`0x00369C73`). An enabled arena number above 14 gives a null record, and the tree test then reads address
`0x50` (`0x00369C8A`, `0x00369CA2`, `0x00369CA5`).

- **Exact pass** `0x0036AAD0`: for the free block at the head of `+0x90`, it searches the tree for a block
  of the same size at a higher address (low 32 bits compared unsigned) whose `+0x15` bit `0x4` is clear,
  and moves it into the hole.
- The exact pass `0x0036AAD0(record, repeat)` returns 0 at once for an empty free list (`0x0036AAEF`). Its
  search goes left from a larger node and right otherwise, comparing sizes as signed values
  (`0x0036AB3C`-`0x0036AB46`); a smaller qualifying node is noted and never used (`0x0036AB76`-`0x0036AB97`). When no
  block matches it returns without trying the next free block (`0x0036AB9E`-`0x0036ABA3`).
- After a move (`0x0036A2A0(record, hole, block)`, `0x0036AB60`) the exact pass returns when `repeat` is 0;
  otherwise it starts again from the new head of `+0x90` (`0x0036AB68`-`0x0036AB74`). It returns the number of
  moves (`0x0036ABA8`).
- **Adjacent pass** `0x0036ABE0`: for each free block, when the block physically after it is in the tree
  and not inhibited (`+0x15 & 6` = 2) and allocated, it moves that block down; otherwise it searches
  for an equal-size block higher up as above. It moves at most one block per call.
- The adjacent pass returns 0 at the first free block that has no block after it on the address chain
  (`0x0036AC13`-`0x0036AC1E`), and when the block after it is in the tree and not inhibited but not allocated
  (`0x0036ACBA`-`0x0036ACC1`). It goes on to the next free block through the free chain's `+0x08`
  (`0x0036AC7A`-`0x0036AC88`). It returns 1 after its one move (`0x0036AC95`-`0x0036AC9A`) and 0 when no free block
  led to one.

`0x0036BFE0(arena, size)` is the pressure path: it calls the arena's callback at record `+0xA0` when one
is set, compacts once, and retries the allocation, until the allocation succeeds or nothing moved and
the callback returned 0. A disabled arena spins forever. `0x00369CF0` reads and `0x003697C0` clears the
moved latch.

`0x0036BFE0` uses `arena` only for that enabled test (`0x0036BFF8`). Each round it reads the current arena
`0x022D89BC` again and takes the callback, the compaction and the retry from it (`0x0036C013`, `0x0036C03D`,
`0x0036C08B`). Its four callers, `0x0036A100`, `0x0036A1A0`, `0x0036B160` and `0x0036D050` (`0x0036A149`, `0x0036A1F0`,
`0x0036B1A4`, `0x0036D08F`), pass `0x022D89BC` as `arena`, read at `0x0036A12E`, `0x0036A1D8`, `0x0036B16F` and, for
`0x0036D050`, by its one caller `0x0036CAD0` (`0x0036CAE6`). An arena number above 14 gives a null record, whose
callback cell is read at address `0xA0` (`0x0036C01D`-`0x0036C02D`).

The callback receives the arena and the size (`0x0036C039`-`0x0036C03B`). The compaction is one exact pass with
`repeat` 0 and one adjacent pass, skipped for a disabled arena or an empty tree, and a move sets `+0x02` and
`+0x62` (`0x0036C049`-`0x0036C099`). The retry is always bottom-up, `0x0036BC60(arena, size, 0, 0)`
(`0x0036C0A1`-`0x0036C0A9`), also for the top-down `0x0036A190`, which puts 1 in `r9d` (`0x0036A1DE`) that the body
never reads.

`0x00369CF0(arena)` returns 0 for a disabled arena (`0x00369CFB`) and otherwise the record's byte `+0x62`; an
enabled arena number above 14 reads address `0x62` (`0x00369D1C`-`0x00369D1E`).

So `0x0036A100` and `0x0036A190` return null when an enabled arena stays full after compaction and its callback, if it
has one, gives up (`0x0036C0AE`-`0x0036C0BF`, `0x0036A1F5`-`0x0036A1FB`). Arena 4 has no callback (`0x0036C5A0` is called only
for arenas 6 and 10, `0x002EA4F3` and `0x002EA504`), and the map-pack completion `0x00378BC0`
([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md#the-dispatch)) does not test for null.

For a field's own pack
it takes the size of section 4, the navigation dataset (`0x0036C100`, `0x00378CD5`), pushes arena 4 (`0x0036C1D0(4, 5)` at
`0x00378CE5`), allocates top-down (`0x0036A190`, `0x00378CF6`), labels the block (`0x0036C660`, which itself skips a null
block at `0x0036C670`), copies the section into it with `memcpy` (`0x00861EBA`, `0x00378D27`) and frees the original
(`0x003697F0`, `0x00378D33`). When arena 4 has no room for the copy, the game loading the field writes the navigation
dataset through address 0 and crashes.

`0x0036C5A0(arena, fn)` is the only setter of the pressure callback. The binding-table init `0x002EA320`
installs `0x002E6D60` for arenas 6 and 10, so under pressure in arena 6 the binding system first unloads
one queued lane and releases its oldest retired model entry, and only then does the arena compact and
retry ([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)).

The binding
system's per-frame update `0x002E65A0` also compacts arenas 6 and 10 with repeat 1 (`0x00369C60(6, 1)`,
`0x00369C60(10, 1)`) every frame, and once more after releasing retired bindings. Arena 10 is built by
none of the sites above, so its compaction does nothing.

### The mover

`0x0036A2A0(arena, hole, source)` saves the source header's fields and name, then:

1. takes the source out of the tree when it is in it;
2. points the source's handle slot at the hole's header, sets the hole's `+0x20` backlink and copies
   the check word;
3. frees the source (`0x00369860`) and copies `source +0x18` payload bytes into the hole with `memcpy`
   (`0x004746F0`);
4. claims the hole (`0x0036BC60(arena, size, hole, 0)`), restores the saved fields and name, puts it back
   in the tree when the source was there, and republishes the slot.

In detail:

- The saved fields are the bytes `+0x02`, `+0x03`, `+0x14`, `+0x15`, `+0x16` and `+0x17`, the dword `+0x30`,
  the word `+0x1E`, the size `+0x18` and the name from `+0x34` (`0x0036A2C3`-`0x0036A32C`). `arena` is the arena
  record: the tree calls receive it, and the claim takes the arena number from its byte `+0x01` (`0x0036A3AC`).
- Step 1 is `0x0036C790(arena, source, 0x14B6)` (`0x0036A338`-`0x0036A344`). Step 2 runs only when the source's
  decoded `+0x20` slot and the hole are both non-null; the slot's `+0x06` takes the hole's `+0x1C` and the
  hole's `+0x3E` is zeroed (`0x0036A349`-`0x0036A378`).
- Before the free it adds the source's size to its group total `0x022D8E10[+0x17]` (`0x0036A37D`-`0x0036A391`).
  The free is `0x00369860(source + 0x40, 0)` and the copy `memcpy(hole + 0x40, source + 0x40, size)`
  (`0x0036A393`-`0x0036A3A7`).
- After the claim it writes the saved bytes, the dword `+0x30`, the word `+0x1E` and the name over the
  hole's header, and the hole's `+0x20` gets the encoded slot, the encoding of a null pointer when there is
  no slot (`0x0036A3C0`-`0x0036A428`).
- When the source was in the tree the hole re-enters it: bit `0x2` is cleared,
  `0x0036B410(arena, hole, 0x14E5)` runs and bit `0x2` is set again (`0x0036A42B`-`0x0036A445`).
- The slot is republished only when it exists: its `+0x08` gets the hole, the hole's `+0x20` the slot and
  the slot's `+0x06` the hole's `+0x1C` (`0x0036A449`-`0x0036A461`). Last the hole's `+0x3E` is zeroed
  (`0x0036A465`).

The handle value stays the same across a move and resolves to the new address; a raw pointer a
consumer kept still points at the old one. The old block is released before the copy, and the copy
uses `memcpy`, not a move that tolerates overlap.

### Repairing effect data after its source moves

An effect template keeps a full 64-bit source base at `+0x858`, a tagged source handle at `+0x860` and
a signed offset at `+0x864`. `0x003B3480` resolves the handle (`0x003AB7F0`), adds the sign-extended offset
and, when the result differs from `+0x858`, calls `0x0024D970(template, newBase)`; it repeats the test
against a second object's base at `+0x390` and repairs it with `0x0024D940`.

`0x003B3480(context, instance)` does nothing unless the context's byte `+0x02` has bit `0x4` (`0x003B348A`).
With an instance it makes the instance current (`0x0024ED80`, `0x003B34A7`). Without one it publishes the
context at `0x02F97340` and its tables `+0x18`, `+0x38`, `+0x840`, `+0x848` and `+0x850` at `0x02EBEF70`,
`0x02EBEFA8`, `0x02EBEFA0`, `0x02EBEF90` and `0x02EBEF78` (`0x003B34AE`-`0x003B34EE`).

It reads the handle `+0x860` as a sign-extended 32-bit value (`0x003B34F5`). The second test runs only with
an instance, whose `+0x390` is the second base (`0x003B351F`-`0x003B3533`).

`0x0024D970` computes the delta as a 32-bit difference of the low halves of the new and old bases, runs
three repair walks with it (`0x003AA3D0`, `0x003A9BA0`, `0x003A9860`), and stores the full new base.

The repair is exact only when the real distance moved
lies between −2^31 and 2^31 − 1; beyond that the base is right and every repaired pointer is wrong.
`0x005004C0` is the type switch that the `0xA00` record handlers also run at load; the effect element
types it sets up are on the
[effect element dispatch](../Graphics/effect-element-runtime.md)
page.

The walks take the 32-bit delta in `ecx`; each one that writes a pointer itself sign-extends the delta
and adds it:

- `0x003AA3D0` follows the record chain from `[[0x02EBEF70]]` (the context's `+0x18` record store) through
  each record's encoded `+0x00` and writes nothing itself. It forwards the delta to the element handlers:
  `0x00501420` for a record whose byte `+0x0E` is `0x52` and `0x00503F10` for `0x56` (`0x003AA3DA`-`0x003AA41F`).
- `0x003A9BA0` visits the qwords at offsets 8 to `0x17F8` of the table `[[0x02EBEF78]]` (the context's `+0x850`
  definitions; slot 0 is skipped). For each non-null one it calls `0x005004C0(entry + delta, delta)` and then
  adds the delta to the stored pointer (`0x003A9BAA`-`0x003A9BF7`).
- `0x003A9860` does the same over offsets 8 to `0x9F8` of `[[0x02EBEF90]]` (the context's `+0x848` emitter
  records), calling `0x00442460(entry + delta, delta)` (`0x003A986A`-`0x003A98B7`).
- `0x0024D940(instance, newBase)` runs one walk, `0x003A8FF0(d)` with `d = (int32)newBase - (int32)instance[+0x390]`
  (the 32-bit difference of the low halves of the new base and `+0x390`, `sub ecx, dword ptr [rbx + 0x390]`,
  `0x0024D950`-`0x0024D952`), then stores the full new base, `instance[+0x390] = newBase` (`0x0024D95D`).
- `0x003A8FF0` adds it at list records `+0x100`, `+0x108`, `+0x18` and `+0x20`: it follows the list whose
  head is the qword at `[0x02EBEF88] + 8` through each record's `+0x08`, adding at `+0x100` and `+0x108`.
- In each of those records `0x003A8FF0` also follows the list from `+0x118` through `+0x30`, adding at
  `+0x18` and `+0x20` (`0x003A8FF0`-`0x003A9061`).

## Layouts

Arena record (`0x022D7FD0` + i*`0xA8`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | byte00 |  |
| `+0x01` | `u8` | index |  |
| `+0x02` | `u8` | dirty |  |
| `+0x08` | `...` |  | name header |
| `+0x10` | `...` |  | heap start |
| `+0x18` | `...` |  | heap middle |
| `+0x20` | `...` | bitmap |  |
| `+0x28` | `...` |  | page map |
| `+0x30` | `...` |  | slot table |
| `+0x38` | `...` |  | slot end |
| `+0x40` | `...` |  | free slot |
| `+0x48` | `...` |  | used slot |
| `+0x50` | `...` |  | tree root |
| `+0x58` | `u32` | pages |  |
| `+0x5C` | `u32` |  | heap size |
| `+0x60` | `u16` |  | handle serial: the check word `0x0036A490` stores at a new header's `+0x1C` (`0x0036A517`). `0x00369D30` zeroes it (`0x00369F60`) and gives the arena's first header that 0 (`0x00369FCB`); `0x0036BC60` gives it to the allocation and to the remainder (`0x0036BE46`, `0x0036BE6D`; for a null remainder `0x0036A490` returns at once, `0x0036A493`), `0x0036B980` to every piece of a split (`0x0036BB95`), `0x0036C290` and `0x0036C380` to the free block a shrink leaves behind the block (`0x0036C2A4`, `0x0036C3FA`), and `0x0036CB00` to a block it moves down into the free block before it (`0x0036CD9A`). Each of those five adds 1 once its headers are written (`0x0036BFC5`, `0x0036BC31`, `0x0036C35B`, `0x0036C470`, `0x0036CE3E`), `0x0036B980` once for all its pieces, and `0x0036BC60` also when no free block is large enough (`0x0036BD66`). `0x0036AF20` and `0x0036A240` copy a header's `+0x1C` to its handle slot's check word `+0x06` (`0x0036B005`-`0x0036B00C`, `0x0036A266`-`0x0036A26A`); `0x0036A000` and `0x0036D170` accept a handle only when the two match (`0x0036A034`-`0x0036A038`, `0x0036D19A`-`0x0036D19E`). No other instruction reads or writes the field |
| `+0x62` | `u8` | moved |  |
| `+0x68` | `u32[9]` |  | tag bytes: a byte total per block tag t (a header's `+0x16`) at `+0x68` + 4 × t, zeroed by `0x00369D30` (`0x00369FAD`-`0x00369FC0`). `0x0036BC60` adds the allocation's rounded size under the tag it stores, the current tag `0x022D8E1C` or, for a given block such as the mover's hole, that block's own `+0x16` (`0x0036BD57`, `0x0036BE85`, `0x0036BFAD`); the free `0x00369860` subtracts the size `+0x18` under the block's tag (`0x00369B05`-`0x00369B18`); the resize `0x0036D050`, once `0x0036CB00` succeeds, adds the new rounded size less the old under the old tag (`0x0036D0A8`, `0x0036D124`-`0x0036D126`); the split `0x0036B980` subtracts the block's size, adds its new size and adds each piece's size, all under the block's tag (`0x0036BAC2`, `0x0036BAED`, `0x0036BB09`, `0x0036BC0C`). Only these updates read the counters: the arena-record access tables list no other access at `+0x68` to `+0x88` |
| `+0x90` | `...` |  | free list bottom |
| `+0x98` | `...` |  | free list top |
| `+0xA0` | `...` |  | pressure callback |

Block header (payload `+0x40`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | magic | `0xFF12` |
| `+0x02` | `u8` | category | `0x022D8E18`, stamped at `0x0036A15F`; `0xFF` when free |
| `+0x03` | `u8` | arena |  |
| `+0x04` | `...` | encoded link | one of the four encoded links |
| `+0x08` | `...` | encoded link | one of the four encoded links |
| `+0x0C` | `...` | encoded link | one of the four encoded links |
| `+0x10` | `...` | encoded link | one of the four encoded links |
| `+0x14` | `u8` | allocFlags | bit `0x1` allocated |
| `+0x15` | `u8` | blockFlags | bit `0x1` top, bit `0x2` in tree, bit `0x4` not movable, bit `0x8` set while `0x022D8E28` |
| `+0x16` | `u8` | tag |  |
| `+0x18` | `i32` | size |  |
| `+0x1C` | `u16` |  | check word |
| `+0x1E` | `u16` |  | label tag |
| `+0x20` | `...` |  | encoded slot |
| `+0x24` | `...` | encoded tree link | one of the three encoded tree links |
| `+0x28` | `...` | encoded tree link | one of the three encoded tree links |
| `+0x2C` | `...` | encoded tree link | one of the three encoded tree links |
| `+0x30` | `...` | encoded link | `0x0020E620`(0), the encoding of a null pointer, written by `0x0036A490` (`0x0036A54D`), `0x0036A100` (`0x0036A167`), `0x0036A190` (`0x0036A20E`), `0x0036B160` (`0x0036B1D6`) and the free `0x00369860` (`0x00369B4C`); the mover `0x0036A2A0` saves and restores it (`0x0036A302`, `0x0036A3FC`), as the resize `0x0036CB00` does (`0x0036CD07`, `0x0036CF64`; `0x0036CDEA`, `0x0036CEB3`, `0x0036CFC4`), and the split `0x0036B980` copies the block's dword into each piece (`0x0036BB5B`-`0x0036BB5E`) and, after `0x0036A490`, gives the piece the block's value again (`0x0036BACA`, `0x0036BBC4`-`0x0036BBD9`). No other arena instruction writes it. Apart from those copies only the walk `0x0036A570` reads it, and it decodes the value and drops it (`0x0036A6C0`-`0x0036A6C3`) |
| `+0x34` | `char[8]` | label |  |
| `+0x3E` | `u16` | guardWord | must be 0 on free |
| `+0x40` | `...` | payload |  |

Handle slot:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | next |  |
| `+0x02` | `u16` | previous |  |
| `+0x04` | `u8` | arena |  |
| `+0x05` | `u8` |  | in use |
| `+0x06` | `u16` |  | check word |
| `+0x08` | `...` | header |  |

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

The second table comes from a search that follows the record through each function's branches. It starts at the
19 instructions that form the array's address `0x022D7FD0` relative to `rip`, each a `lea`, which are all the
instructions that refer to the array that way. Where two paths join, the search keeps every record address either
path held, so it errs towards listing an access rather than missing one.

## Operations

Per allocation: one free-list walk and up to two header writes. A compaction `0x00369C60` runs the exact pass and
then the adjacent pass. The exact pass searches the tree once and moves at most one block when `repeat` is 0
(`0x0036AB68`); when it is set it searches again from the new head of the free list after each move, until a
search finds no block (`0x0036AB6D`-`0x0036AB74`).

The adjacent pass takes the free blocks in turn until one block moves, and returns after that move
(`0x0036AC95`-`0x0036AC9A`): for each free block it either moves the block after it, with no search, or searches
the tree once. Each move is a header save and restore plus one payload copy.

## State

The fifteen arena records, the enabled mask `0x022D89B8`, the current arena `0x022D89BC` and its stack, and
the encoding base `0x01F83530`.

The byte totals per accounting group: a `u32` table at `0x022D8E10`, indexed by a block header's byte `+0x17`. The
mover `0x0036A2A0` adds the size `+0x18` of the block it moves to that block's group (`0x0036A37D`-`0x0036A391`); the
free `0x00369860` subtracts it for a non-zero group (`0x00369B1B`-`0x00369B34`), and so does the resize `0x0036D050`
(`0x0036D0EC`-`0x0036D0FE`). The resize then adds the new block's size to its own non-zero group when `0x0036CB00`
returns one (`0x0036D12A`-`0x0036D138`).

`0x0036C5D0(handle,
group)` and `0x0036C620(payload, group)` move the size from the old group to the new one and store the new group
(`0x0036C60C`, `0x0036C610`, `0x0036C616`; `0x0036C642`, `0x0036C649`). The boot step `0x0036D260`, run by the boot fixer at
`0x0022A3B4`, zeroes groups 8 to 12:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022D8E30` | `u32` | 0 (zero-filled tail of `.data`) | bytes in group 8; one 8-byte store also zeroes group 9 (`0x022D8E34`) | `0x0036D260` (`0x0036D262`); the group updates above | the group updates above (each adds to or subtracts from the word it reads) |
| `0x022D8E38` | `u32` | 0 (zero-filled tail of `.data`) | bytes in group 10; one 8-byte store also zeroes group 11 (`0x022D8E3C`) | `0x0036D260` (`0x0036D269`); the group updates above | the group updates above |
| `0x022D8E40` | `u32` | 0 (zero-filled tail of `.data`) | bytes in group 12 | `0x0036D260` (`0x0036D270`); the group updates above | the group updates above |

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
- [Effect element dispatch](../Graphics/effect-element-runtime.md): the effect elements the repair walks reach.
