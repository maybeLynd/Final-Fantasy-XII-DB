---
title: "EASTL strings and containers: the string, vector and tree layouts, the logging allocator and the static strings built at start-up"
kind: "system"
category: "Third-party libraries"
addresses: "0x001EDF00, 0x00902720, 0x001EDF10, 0x001EDF80, 0x001EDFE0, 0x0016D690, 0x01F82E48, 0x001FF740, 0x02EBA2E0, 0x001E7D30, 0x0016D6D0, 0x0016D720, 0x0016D780, 0x0016D7E0, 0x0016D840, 0x0016DA60, 0x001A3380, 0x00200E60, 0x0015D610, 0x0015C560, 0x0015D2F0, 0x0015D230, 0x0015FFE0, 0x001A52A0, 0x001FC640"
---

## What the player sees

Nothing directly. EASTL, Electronic Arts' container library, holds much of the game's text and many
of its lists, sets and maps, from JSON files read through JsonBox to sorted lookup tables. Knowing its layouts matters when reading any structure in the
executable: three consecutive pointers followed by an allocator are usually one string or one
vector, not four fields.

## How it works

### Identity

The image names the library in its own RTTI: `eastl::allocator_memory_log` (`0x01F480F8`) and
`eastl::allocator` (`0x01F7E300`). The allocator's constructor `0x001EDF00` writes the
`allocator_memory_log` vtable `0x00902720`. Containers pass one of five name strings to that
constructor: `EASTL basic_string` (`0x008F6600`), `EASTL vector` (`0x008C5F58`), `EASTL set`
(`0x008F3CB0`), `EASTL list` (`0x008F3CC0`) and `EASTL map` (`0x008F4120`). The constructor is called from
583 sites in 230 functions.

### The allocator

`0x001EDF00` stores the vtable and returns; the name argument is never kept. The vtable at `0x00902720`
has six slots, followed by 0 at `0x00902750`:

| Slot offset | Function | What it does |
|---|---|---|
| `+0x00` | `0x0016D680` | returns the object |
| `+0x08` | `0x001EDF10` | `_aligned_malloc(size, alignment)` |
| `+0x10` | `0x001EDF80` | `_aligned_malloc(size, 16)`; the allocation every container uses |
| `+0x18` | `0x001EDFE0` | `_aligned_free(p)` when `p` is not null; callers pass the size, which it ignores |
| `+0x20` | `0x0016D690` | returns the name `EASTL` (`0x01CDAE78`) |
| `+0x28` | `0x0016D6A0` | `ret 0`, an empty function at EASTL's `set_name` position |

Each of the three memory slots first creates a 32-byte record at `0x01F82E48` holding
`0x2000000`, `0x200000`, 0 and 0. Only those three functions refer to the record, and none of them
reads it, so no allocation is logged or attributed.

Each slot tests `0x01F82E48` (`0x001EDF1A`, `0x001EDF86`, `0x001EDFE6`) and, while it is null, takes `malloc(0x20)`
(`0x001EDF2F`, `0x001EDF98`, `0x001EDFF8`). A block it gets receives `0x2000000` at `+0x00`, `0x200000` at `+0x04`, a
zero qword at `+0x10` and a zero dword at `+0x18`; the result is stored at `0x01F82E48` null or not (`0x001EDF56`,
`0x001EDFBF`, `0x001EE01F`), so after a failed `malloc` the next call tries again.

Then each slot leaves by a tail jump. Slot `+0x08` jumps to `_aligned_malloc` (`0x008C2B60`) with the size and the
caller's alignment (`0x001EDF6D`), and slot `+0x10` jumps there with the size and 16 (`0x001EDFD3`). Slot `+0x18`
jumps to `_aligned_free` (`0x008C2B70`) for a non-null pointer (`0x001EE033`) and returns at once for null
(`0x001EE029`).

### Strings

An `eastl::basic_string<char>` is `0x20` bytes: begin, end and capacity end pointers followed by an
allocator object (see Layouts). There is no inline buffer. Building a string from C text (`0x001FF740`
is one site):

1. measure the text; with `n` = length + 1,
2. when `n` is below 2, point end and capacity end at the shared byte `0x02EBA2E0` and `0x02EBA2E1`
   without allocating;
3. otherwise allocate `n` bytes through slot `+0x10` and set capacity end to the block plus `n`;
4. copy the text with `memmove`, set end to the last character and write the terminator.

Every empty string in the process points at the same byte. Freeing is guarded by
`capacity end - begin > 1` and a non-null begin, so the shared byte is never freed.

### Vectors

`0x001E7D30` inserts `n` copies of a 16-byte element. When the free capacity is too small it allocates
`max(size + n, size == 0 ? 1 : 2 × size)` elements through the vector's own allocator at `+0x18`,
copies the elements before the insertion point, writes the new ones, copies the rest and frees the
old block. A vector grown one element at a time therefore holds 1, 2, 4, 8 … elements.

`0x001E7D30(vector, position, n, value)` returns at once when `n` is 0 (`0x001E7D63`), and grows only when `n` is
above the free count `(capEnd - end) / 16` (`0x001E7D50`, `0x001E7D5A`). It loads the value before it moves any
element (`0x001E7D69`).

When it grows, a new capacity of 0 allocates nothing (`0x001E7EA4`). The old block is freed through slot `+0x18`
only when `begin` is not null (`0x001E7F44`, `0x001E7F5F`). Then `begin` takes the new block (`0x001E7F72`), `end`
the end of the copies (`0x001E7F7E`) and `capEnd` the address `block + newCapacity * 16` (`0x001E7F6B`, `0x001E7F7A`).

In place, with `k = (end - position) / 16` elements behind the position (`0x001E7D73`):

- when `n < k` (`0x001E7D7A`), it copies the last `n` elements past the end, moves `end` on by `n * 16` bytes
  (`0x001E7DAE`), shifts the other tail elements back from the last one (`0x001E7DC0` to `0x001E7DD2`) and writes
  `n` copies at the position (`0x001E7DE1`);
- otherwise it writes `n - k` copies past the end (`0x001E7E09`), copies the `k` tail elements behind them
  (`0x001E7E38`), moves `end` on in two steps (`0x001E7E1E`, `0x001E7E4F`) and writes the value over the `k` old
  places (`0x001E7E60`).

### Sets and maps: the red-black tree

Every EASTL set and map in the game shares one balanced-tree runtime of six functions. A node starts
with right, left and parent pointers and a colour byte (red 0, black 1); the key and value follow at
`+0x20`.

- `0x0016D6D0` steps to the next node: down the right child and then left as far as possible, or up
  while the node is its parent's right child. It writes nothing. With a right child it returns the leftmost
  node below it (`0x0016D6E4` to `0x0016D6F0`). After the climb it returns the parent it reached, except that a node
  whose right link is that parent is returned itself (`0x0016D70C`, `0x0016D70F`).
- `0x0016D720` steps to the previous node, the mirror image, after first returning the anchor's right
  link when the node is the red anchor itself (its parent's parent is itself).
- `0x0016D780` and `0x0016D7E0` rotate left and right; only the erase calls them.
- `0x0016D780(node, root)` lifts the node's right child: the child's left subtree becomes the node's right
  (`0x0016D787`, `0x0016D793`), the child takes the node's parent (`0x0016D79B`) and the node becomes the child's
  left child (`0x0016D7A7`, `0x0016D7AE`).
- When the node is `root`, `0x0016D780` leaves its parent's links as they are and returns the child as the new
  root (`0x0016D79F`, `0x0016D7A4`). Otherwise the parent's matching link moves to the child (`0x0016D7BD`,
  `0x0016D7CD`) and `root` is returned.
- `0x0016D7E0(node, root)` is the mirror image: it lifts the left child (`0x0016D7E0`, `0x0016D807`), with the same
  root test (`0x0016D7FF`) and return value.
- `0x0016D840` inserts a node: it initialises the node's links and colour, hangs it on the chosen side
  of its parent, updates the anchor's leftmost, rightmost and root links, recolours, rotates inline
  (for example `0x0016D8C7` to `0x0016D912`, including the root update at the anchor's `+0x10`, and the
  mirror case), and paints the root black (`0x0016DA4F`). It has 90 call sites in 56 functions.
- Its arguments are `(node, parent, anchor, side)`. The node gets null child links, `parent` as its parent and
  the colour red (`0x0016D842` to `0x0016D84D`). Side 0 hangs it as the parent's left child (`0x0016D855`); when the
  parent is the anchor the node also becomes the root, the leftmost (through that same left link) and the
  rightmost (`0x0016D85E`, `0x0016D878`), and when the
  parent was the leftmost the node takes its place (`0x0016D86A`).
- Any other side hangs the node as the parent's right child (`0x0016D870`), and it replaces a parent that was the
  rightmost (`0x0016D878`). The fix-up loop runs while the node is not the root and its parent is red
  (`0x0016D87B`, `0x0016D894`, `0x0016DA41`). The function returns the root (`0x0016DA4B`).
- `0x0016DA60` erases a node: it splices in the replacement, swaps the two nodes' colour bytes
  (`0x0016DBA9` to `0x0016DBB7`) and rebalances with the two rotations.

The comparison that decides left or right is the caller's. `0x001A3380` is a typical map insert: it
walks from the root comparing an `int` key at node `+0x20`, allocates a `0x38`-byte node through the
container's allocator at `+0x30`, copies a 20-byte value to node `+0x20`, calls `0x0016D840` with the
anchor at container `+0x08`, and increments the count at `+0x28`.

`0x001A3380(map, result, value)` compares signed: a smaller key goes left, any other right (`0x001A33C0` to
`0x001A33D6`). After a left turn at the leftmost node it inserts at once (`0x001A33EA`). Otherwise it takes the last
node of the walk, or after a left turn that node's predecessor from `0x0016D720` (`0x001A33F3`). When that node's key
is not below the new key (`0x001A33FE`), the key is present: it writes that node and 0 to the result and inserts
nothing (`0x001A34BD`, `0x001A34C0`).

On insert the side is 0 (left) when the parent is the anchor or the key is below the parent's key, else 1
(`0x001A3407` to `0x001A3412`, `0x001A3419` to `0x001A342D`). The value copy is skipped only when the block address
`block + 0x20` is 0 (`0x001A3448`, `0x001A3490`). It writes the new node and 1 to the result (`0x001A346C`,
`0x001A346F`, `0x001A34B4`, `0x001A34B7`) and returns the result (`0x001A34C9`).

### Static strings and containers built at start-up

64 entries of the start-up initialiser table build EASTL objects. Each constructs the named allocator,
fills the object and registers its destructor with `atexit` (`0x00808B90`). `0x0015D610` is typical: it
allocates 5 bytes for `null`, copies 4, terminates, and registers `0x008A70F0`. An initialiser for an
empty literal (`0x0015C560`, text `0x01CEB638`) takes the shared byte instead and copies 0 bytes. Two
more (`0x0015D2F0`, `0x0015DBB0`) build an empty string with no copy at all, and four build empty
containers (`0x0015D230` a vector, `0x001601C0` a list, `0x0015D260` and `0x0016A2C0` maps).

`0x0015C560` builds the current cut name `0x01F81358`. It constructs the allocator twice, a stack temporary named
`EASTL basic_string` and then the member `0x01F81370` (`0x0015C576`, `0x0015C59B`). The length is computed as
`esi - esi + 1`, always 1 (`0x0015C5A7` to `0x0015C5AB`), so the shared-byte branch is always taken (`0x0015C5B0`,
`0x0015C600` to `0x0015C60E`). `memmove` copies 0 bytes (`0x0015C61E`), `end` is set to the shared byte (`0x0015C624`),
the terminator 0 is written into the shared byte `0x02EBA2E0` itself (`0x0015C632`), and the routine tail-jumps to
`atexit` with `0x008A69F0` (`0x0015C63F`).

The 52 non-empty strings are four copies of the 13 strings a JSON writer and reader need: the escapes
`\"`, `\\`, `\/`, `\b`, `\f`, `\n`, `\r`, `\t`, `\u`, the words `true`, `false`, `null` and the hex
digits `0123456789ABCDEFabcdef`. They belong to JsonBox, which the image names in its RTTI
(`JsonBox::Indenter`, `JsonBox::IndentCanceller`, `JsonBox::SolidusEscaper`).
The four copies of `\t` are built by `0x0015D9D0`, `0x0015E780`, `0x0015F3B0` and `0x0015FFE0`; the last
allocates 3 bytes, copies the two characters from `0x009047BC` into the static string at `0x01FD3FB8`
and registers `0x008A8050`.

### Code instantiated per element type

The compiler emits the string, vector and tree operations once for each element type, so the same
operation appears many times with different element sizes. 55 such bodies are listed in
[`eastl-strings-and-containers-template-instances.tsv`](eastl-strings-and-containers-template-instances.tsv) with the operation and the element or node
size of each; the other 76 are on
[object construction and destruction](../Compiler-And-C-Runtime/object-construction-and-destruction.md).

- `0x001A52A0` appends a character range to a string. When the result does not fit, the new capacity
  is 8 while the old capacity is below 9, otherwise twice the old one, and never less than the
  length needed; it then copies both parts into the new block and frees the old one.
- `0x001A52A0(string, first, last)` returns the string at once for an empty range (`0x001A52B5`). The capacity is
  `capEnd - begin - 1` and the result fits when `size + n <= capacity`, in 32 bits (`0x001A52BB` to `0x001A52D5`).
  In place it copies all but the first character to `end + 1` (`0x001A53B1`), writes the terminator at `end + n`
  (`0x001A53BD`), then the first character at the old end (`0x001A53CE`), and moves `end` on by `n` (`0x001A53D3`).
- When it grows, it allocates `newCapacity + 1` bytes (`0x001A5304`, `0x001A530F`), writes the terminator
  (`0x001A5346`) and frees the old block through slot `+0x18` only when `capEnd - begin > 1` and `begin` is not
  null (`0x001A5353`, `0x001A535C`, `0x001A536D`). `capEnd` becomes `block + newCapacity + 1` (`0x001A537F`); both paths
  return the string (`0x001A5383`, `0x001A53D0`).
- `0x001FC640` is a map's `operator[]` with a `u32` key at node `+0x20`: it walks from the root
  `+0x18`, and when the key is missing it inserts a default value, an empty vector whose allocator
  is named `EASTL vector`, through `0x001FD310`.
- `0x001FC640` keeps the first node whose key is not below the key, comparing unsigned (`0x001FC674` to
  `0x001FC689`); a key equal to that node's key skips the insert (`0x001FC695`). For a missing key it builds the
  pair through `0x001FBFC0` (`0x001FC6CF`), and after `0x001FD310` (`0x001FC701`) frees each temporary vector's block
  through slot `+0x18` when its `begin` is not null (`0x001FC713`, `0x001FC72E`, `0x001FC737`, `0x001FC752`).
- On both paths `0x001FC640` returns the address of the node's value, node `+0x28` (`0x001FC756`).

The string bodies follow the rules under Strings: `0x001B38B0` and `0x001A4BF0` take the shared byte
`0x02EBA2E0` when the length plus one is below 2.

### Columns of eastl-strings-and-containers-template-instances.tsv

| Column | Holds |
|---|---|
| `evidence` | the instructions that show the body is the operation in `operation`: calls through the container allocator's vtable (slot `+0x10` allocates, slot `+0x18` frees), construction of the named allocator through `0x001EDF00`, the shared empty byte `0x02EBA2E0`, the growth rule of a string or vector, or the other container bodies it calls, with their addresses |

### JsonBox values

JsonBox stores parsed JSON in EASTL containers. Its reader `0x00200E60` constructs allocators named
`EASTL map`, `EASTL vector` and `EASTL basic_string` for objects, arrays and strings, and its string
reader `0x00201C40` carries JsonBox's message `Expected '"', got '` (`0x00905008`). `0x00200BF0` reads a
whole file into a stream and hands it to `0x00200E60`; the screen-layout files are read this way.

## Layouts

Eastl::basic_string&lt;char&gt;   `0x20` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | begin | first character |
| `+0x08` | `void*` | end | the terminator; length = end - begin |
| `+0x10` | `void*` | capacityEnd | one past the block; `0x02EBA2E1` for an empty string |
| `+0x18` | `void*` | allocator | the allocator object itself (its vtable pointer) |

Eastl::vector&lt;T&gt;:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | begin |  |
| `+0x08` | `void*` | end | size = (end - begin) / sizeof(T) |
| `+0x10` | `void*` | capacityEnd |  |
| `+0x18` | `void*` | allocator | the allocator object itself |

Tree node (set and map elements):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | right |  |
| `+0x08` | `void*` | left |  |
| `+0x10` | `void*` | parent |  |
| `+0x18` | `u8` | colour | 0 red, 1 black |
| `+0x20` | `...` | value | key first; node size is `0x20` plus the value |

Map container, as `0x001A3380` uses it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `node` | anchor | its `+0x00` rightmost, `+0x08` leftmost, `+0x10` root |
| `+0x28` | `u32` | count |  |
| `+0x30` | `void*` | allocator | the allocator object itself |

## Shipped data

| Fact | Value |
|---|---|
| start-up initialisers in the executable's C++ table | 1,172 |
| initialisers that build EASTL objects | 64 |
| strings copied from a literal | 58: 52 non-empty, 6 empty |
| strings built empty without a copy | 2 |
| containers built empty | 4: 2 maps, 1 vector, 1 list |
| distinct non-empty literals | 13, each copied 4 times |

## State

### The escapes of the JSON string writer

`0x002002E0(out, text)`, from `0x001FEE80` (`0x001FEF70`) and `0x001FF210` (`0x001FF30C`), writes a string for JSON output.
For each character it appends the matching escape from one copy of the static strings, read through the string's
`begin` and `end`: `"` (`0x002003C5`), `\` (`0x00200440`), `0x08` (`0x002004BD`), `0x0C` (`0x0020053A`), `0x0A`
(`0x002005B7`), `0x0D` (`0x00200633`) and `0x09` (`0x002006AC`).

Each string is a `basic_string` (Layouts) with its own initialiser and destructor:

1. one 16-byte store zeroes `begin` and `end`;
2. both take the two-byte buffer, from the allocator or the shared byte `0x02EBA2E0`, and `end` moves past the two
   characters;
3. the `atexit` destructor reads `begin` and `capacityEnd` to free the buffer.

All are 0 in the file (the zero-filled tail of `.data`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F83090` | `void*` | 0 | `\n` `begin` (text `0x009047B4`) | `0x0015D520` (`0x0015D553`, `0x0015D597`, `0x0015D5C5`) | `0x002002E0` (`0x002005FC`); `0x008A70A0` (`0x008A70B7`) |
| `0x01F83098` | `void*` | 0 | `\n` `end` | `0x0015D520` (`0x0015D553`, `0x0015D59E`, `0x0015D5CC`, `0x0015D5F0`) | `0x002002E0` (`0x002005F5`) |
| `0x01F830B0` | `void*` | 0 | `\t` `begin` (text `0x009047BC`) | `0x0015D9D0` (`0x0015DA03`, `0x0015DA47`, `0x0015DA75`) | `0x002002E0` (`0x002006F1`); `0x008A7230` (`0x008A7247`) |
| `0x01F830B8` | `void*` | 0 | `\t` `end` | `0x0015D9D0` (`0x0015DA03`, `0x0015DA4E`, `0x0015DA7C`, `0x0015DAA0`) | `0x002002E0` (`0x002006EA`) |
| `0x01F83110` | `void*` | 0 | `\\` `begin` (text `0x009047A4`) | `0x0015D7F0` (`0x0015D823`, `0x0015D867`, `0x0015D895`) | `0x002002E0` (`0x00200485`); `0x008A7190` (`0x008A71A7`) |
| `0x01F83118` | `void*` | 0 | `\\` `end` | `0x0015D7F0` (`0x0015D823`, `0x0015D86E`, `0x0015D89C`, `0x0015D8C0`) | `0x002002E0` (`0x0020047E`) |
| `0x01F831B0` | `void*` | 0 | `\f` `begin` (text `0x009047B0`) | `0x0015D430` (`0x0015D463`, `0x0015D4A7`, `0x0015D4D5`) | `0x002002E0` (`0x0020057F`); `0x008A7050` (`0x008A7067`) |
| `0x01F831B8` | `void*` | 0 | `\f` `end` | `0x0015D430` (`0x0015D463`, `0x0015D4AE`, `0x0015D4DC`, `0x0015D500`) | `0x002002E0` (`0x00200578`) |
| `0x01F831D0` | `void*` | 0 | `\r` `begin` (text `0x009047B8`) | `0x0015D050` (`0x0015D083`, `0x0015D0C7`, `0x0015D0F5`) | `0x002002E0` (`0x00200677`); `0x008A6DF0` (`0x008A6E07`) |
| `0x01F831D8` | `void*` | 0 | `\r` `end` | `0x0015D050` (`0x0015D083`, `0x0015D0CE`, `0x0015D0FC`, `0x0015D120`) | `0x002002E0` (`0x00200670`) |
| `0x01F83210` | `void*` | 0 | `\"` `begin` (text `0x009047A0`) | `0x0015D700` (`0x0015D733`, `0x0015D777`, `0x0015D7A5`) | `0x002002E0` (`0x00200408`); `0x008A7140` (`0x008A7157`) |
| `0x01F83218` | `void*` | 0 | `\"` `end` | `0x0015D700` (`0x0015D733`, `0x0015D77E`, `0x0015D7AC`, `0x0015D7D0`) | `0x002002E0` (`0x00200401`) |
| `0x01F83230` | `void*` | 0 | `\b` `begin` (text `0x009047AC`) | `0x0015CE70` (`0x0015CEA3`, `0x0015CEE7`, `0x0015CF15`) | `0x002002E0` (`0x00200502`); `0x008A6D50` (`0x008A6D67`) |
| `0x01F83238` | `void*` | 0 | `\b` `end` | `0x0015CE70` (`0x0015CEA3`, `0x0015CEEE`, `0x0015CF1C`, `0x0015CF40`) | `0x002002E0` (`0x002004FB`) |

No other instruction reaches these globals: no other RIP-relative, image-base-relative or 32-bit offset reference
names them. The addresses taken near them are the strings' `allocator` fields, which `0x001EDF00` fills with 8 bytes
and the destructors call through, and the objects at `0x01F83070` and `0x01F83080` (`0x001FBD80`, `0x001FBE50`), whose code
reaches only their `+0x00` and `+0x08` (`0x001FB840`, `0x001FB810`).

### How every static string is filled

Every static string is filled in the same steps as the escapes above. `0x0015D610`, which builds `null` from
`0x00904780`, shows each store:

1. `0x0015D62E` sets `capacityEnd` to 0, and `0x0015D643` zeroes `begin` and `end` with one 16-byte store.
2. With a block from the allocator, `0x0015D687`, `0x0015D68E` and `0x0015D69E` set `begin` and `end` to the block and
   `capacityEnd` to the block plus 5. When the length plus one is below 2, `0x0015D6B5`, `0x0015D6BC` and `0x0015D6C3`
   set them to `0x02EBA2E0`, `0x02EBA2E0` and `0x02EBA2E1` instead.
3. After the copy, `0x0015D6E0` moves `end` past the four characters and `0x0015D6EE` writes the terminator.
4. At exit, `0x008A70F0` reads `capacityEnd` (`0x008A70FD`) and `begin` (`0x008A7107`) and frees the block through the
   allocator's slot `+0x18` when it is longer than one byte.

### Who reads the token strings

The 52 token strings are four copies of the same 13: copy 1 from `0x01F83090` to `0x01F83230` (around the empty string `0x01F83130`), copies 2 to 4 at
`0x01FD3C58` to `0x01FD4118`. While the game runs, only copy 1 and one string of copy 4 are read:

- the escapes of copy 1, by `0x002002E0` (above);
- `null`: the value writer `0x001FF210` builds a string value from its `begin` (`0x001FF491`) and `end`
  (`0x001FF48A`), and the value reader `0x00200E60` matches its four letters against the input (`0x00200F1F`,
  `0x00200F42`, `0x00200F75`, `0x00200FA8`);
- `true` and `false`: `0x00200E60` matches them letter by letter (`true` at `0x00200FDE`, `0x00201005`, `0x00201038`,
  `0x0020106B`; `false` at `0x00201084`, `0x002010AB`, `0x002010DE`, `0x00201111`, `0x00201144`);
- for a boolean value, `0x001FF210` passes the address of `true` or `false` (`0x001FF41E`, `0x001FF425`, chosen at
  `0x001FF42F`) to `0x001FE820`, which copies its `begin` (`0x001FE879`) and `end` (`0x001FE875`) into a string value;
- `0123456789ABCDEFabcdef` (`0x01F830F0`): `0x00200E60` starts a number on a character from entry 0 to entry 9
  (`0x00200FCA`), the number reader `0x00201890` tests for a leading `0` (`0x0020197F`), and the string reader
  `0x00201EB0` accepts a `\u` digit in entries 0 to 9, 10 to 15 or 16 to 21 (`0x00202281`);
- `\/` of copy 4 (`0x01FD4058`), by JsonBox's `SolidusEscaper` `0x002165B0`
  ([Third-party libraries](third-party-libraries.md)).

Copy 4's `\r` sits at `0x01FD40D8`, with its end at `0x01FD40E0` and its capacity end at `0x01FD40E8`. `0x001600D0` builds
it, setting the capacity end to 0 (`0x001600EE`) and then to the end of its block (`0x0016015E`) or, for an empty
string, `0x02EBA2E1` (`0x00160183`); its exit routine `0x008A80A0` reads it (`0x008A80AD`) before it frees the block.

`\u` and `\/` of copy 1, and every other string of copies 2 to 4, are read only by their own destructors.

### The empty string value and the empty map

`0x0015D2F0` builds `0x01F83130` without a copy: `begin` and `end` take the shared byte `0x02EBA2E0` (`0x0015D30E`,
`0x0015D31C`) and `capacityEnd` takes `0x02EBA2E1` (`0x0015D32A`). `0x00200BA0` returns its address for every value whose
type tag is not 0, the string tag. Its two callers read it: `0x001C3760` its `begin` (`0x001C38FF`, after the call at
`0x001C38FA`), and `0x001C6E20` its `end` and `begin` (`0x001C6F68`, `0x001C6F6C`, after the call at `0x001C6F47`). The
destructor `0x008A6FB0` reads `capacityEnd` and `begin`.

`0x0015D260` builds an empty map at `0x01F83250` with an allocator named `EASTL map` (`0x008F4120`):

1. the anchor's right and left links point at the anchor `0x01F83258` (`0x0015D2C1`, `0x0015D2C8`);
2. the root is 0 (`0x0015D2AF`), the anchor's colour byte is 0 (`0x0015D2CF`) and the count is 0 (`0x0015D2D6`).

Only `0x0015D260` and the destructor `0x008A6F10` refer to the map, so it stays empty. `0x008A6F10` reads the root
(`0x008A6F24`) and returns at `0x008A6F2E` because it is 0. Its loop would free `0x50`-byte nodes (`0x008A6F75`), each
with a string key at `+0x20` and a value at `+0x40` that it passes to `0x002001F0`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| each row of [`eastl-strings-and-containers-state.tsv`](eastl-strings-and-containers-state.tsv): the 138 string fields that no table above lists and the five written fields of the empty map | `void*`; the map's colour `u8` and count `u32` | 0 (zero-filled tail of `.data`) | one field of a static string (its object, literal and copy) or of the empty map | the initialiser, at the sites in `set_by` | the readers above and the destructors (`read_by`); `-` for the 45 fields that no code reads: 41 `end` pointers and the map's two anchor links, colour byte and count |

## Modding notes

- Never free or write through a string whose capacity end is `0x02EBA2E1`: that is the shared empty
  byte every empty string points at.
- Every non-empty string owns a heap block; there is no short-string storage to overflow into.
- Replacing the allocator vtable's slots `+0x10` and `+0x18` redirects every EASTL allocation. The
  container names are not passed through, so a hook cannot tell containers apart by name.
- A tree node's payload starts at `+0x20` whatever the container; the key is its first field.
- Changing one of JsonBox's static token strings changes only one of its four copies.

## Related

- [Screen layouts](../Menus-And-HUD/screen-layouts.md): JSON files parsed through `0x00200BF0` into JsonBox
  values.
- [`eastl-strings-and-containers-string-static-initialisers.tsv`](eastl-strings-and-containers-string-static-initialisers.tsv),
  [`eastl-strings-and-containers-basicstring-variant-initialisers.tsv`](eastl-strings-and-containers-basicstring-variant-initialisers.tsv) and
  [`eastl-strings-and-containers-container-static-initialisers.tsv`](eastl-strings-and-containers-container-static-initialisers.tsv): 62 of the 64
  start-up initialisers.
  - The other two, `0x0015C560`, which builds the cut name, and `0x0015FFE0`, which builds the fourth copy of `\t`,
    are described under "Static strings and containers built at start-up" above.
- [`eastl-strings-and-containers-ordered-container-runtime.tsv`](eastl-strings-and-containers-ordered-container-runtime.tsv) and
  [`eastl-strings-and-containers-ordered-container-runtime-callers.tsv`](eastl-strings-and-containers-ordered-container-runtime-callers.tsv): the tree runtime and its
  callers.
- [`eastl-strings-and-containers-template-instances.tsv`](eastl-strings-and-containers-template-instances.tsv): container code instantiated per element
  type.
- [Object construction and destruction](../Compiler-And-C-Runtime/object-construction-and-destruction.md):
  the other per-type container bodies and the record-pool template they build.

### Columns of eastl-strings-and-containers-ordered-container-runtime.tsv

One row per function, 6 rows in address order.

| Column | Holds |
|---|---|
| `entry` | one of the six tree functions: the next-node step `0x0016D6D0`, the previous-node step `0x0016D720`, the rotations `0x0016D780` and `0x0016D7E0`, the insert `0x0016D840` and the erase `0x0016DA60` |

### Columns of eastl-strings-and-containers-ordered-container-runtime-callers.tsv

| Column | Holds |
|---|---|
| `member_signature` | which of the six tree functions the caller calls directly, joined by `+`: `inc` the next-node step `0x0016D6D0`, `dec` the previous-node step `0x0016D720`, `rotL` and `rotR` the rotations `0x0016D780` and `0x0016D7E0`, `ins` the insert `0x0016D840`, `era` the erase `0x0016DA60`. Six signatures occur across the 99 rows: `inc+era` 30, `dec+ins` 24, `inc+ins` 16, `ins` 16, `inc` 12 and `rotL+rotR` 1, the erase `0x0016DA60` itself; no caller uses more than two of the six |
