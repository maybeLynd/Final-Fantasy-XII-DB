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

Each of the three memory slots first creates, once, a 32-byte record at `0x01F82E48` holding
`0x2000000`, `0x200000`, 0 and 0. Only those three functions refer to the record, and none of them
reads it, so no allocation is logged or attributed.

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

### Sets and maps: the red-black tree

Every EASTL set and map in the game shares one balanced-tree runtime of six functions. A node starts
with right, left and parent pointers and a colour byte (red 0, black 1); the key and value follow at
`+0x20`.

- `0x0016D6D0` steps to the next node: down the right child and then left as far as possible, or up
  while the node is its parent's right child. It writes nothing.
- `0x0016D720` steps to the previous node, the mirror image, after first returning the anchor's right
  link when the node is the red anchor itself (its parent's parent is itself).
- `0x0016D780` and `0x0016D7E0` rotate left and right; only the erase calls them.
- `0x0016D840` inserts a node: it initialises the node's links and colour, hangs it on the chosen side
  of its parent, updates the anchor's leftmost, rightmost and root links, recolours, rotates inline
  (for example `0x0016D8C7` to `0x0016D912`, including the root update at the anchor's `+0x10`, and the
  mirror case), and paints the root black (`0x0016DA4F`). It has 90 call sites in 56 functions.
- `0x0016DA60` erases a node: it splices in the replacement, swaps the two nodes' colour bytes
  (`0x0016DBA9` to `0x0016DBB7`) and rebalances with the two rotations.

The comparison that decides left or right is the caller's. `0x001A3380` is a typical map insert: it
walks from the root comparing an `int` key at node `+0x20`, allocates a `0x38`-byte node through the
container's allocator at `+0x30`, copies a 20-byte value to node `+0x20`, calls `0x0016D840` with the
anchor at container `+0x08`, and increments the count at `+0x28`.

### Static strings and containers built at start-up

64 entries of the start-up initialiser table build EASTL objects. Each constructs the named allocator,
fills the object and registers its destructor with `atexit` (`0x00808B90`). `0x0015D610` is typical: it
allocates 5 bytes for `null`, copies 4, terminates, and registers `0x008A70F0`. An initialiser for an
empty literal (`0x0015C560`, text `0x01CEB638`) takes the shared byte instead and copies 0 bytes. Two
more (`0x0015D2F0`, `0x0015DBB0`) build an empty string with no copy at all, and four build empty
containers (`0x0015D230` a vector, `0x001601C0` a list, `0x0015D260` and `0x0016A2C0` maps).

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
- `0x001FC640` is a map's `operator[]` with a `u32` key at node `+0x20`: it walks from the root
  `+0x18`, and when the key is missing it inserts a default value, an empty vector whose allocator
  is named `EASTL vector`, through `0x001FD310`.

The string bodies follow the rules under Strings: `0x001B38B0` and `0x001A4BF0` take the shared byte
`0x02EBA2E0` when the length plus one is below 2.

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
| `+0x08` | `node` | anchor | its +`0x00` rightmost, +`0x08` leftmost, +`0x10` root |
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
  [`eastl-strings-and-containers-container-static-initialisers.tsv`](eastl-strings-and-containers-container-static-initialisers.tsv): the start-up initialisers.
- [`eastl-strings-and-containers-ordered-container-runtime.tsv`](eastl-strings-and-containers-ordered-container-runtime.tsv) and
  [`eastl-strings-and-containers-ordered-container-runtime-callers.tsv`](eastl-strings-and-containers-ordered-container-runtime-callers.tsv): the tree runtime and its
  callers.
- `eastl-strings-and-containers-template-instances.tsv`: container code instantiated per element
  type.
- [Object construction and destruction](../Compiler-And-C-Runtime/object-construction-and-destruction.md):
  the other per-type container bodies and the record-pool template they build.
