---
title: "EASTL strings and containers: the string, vector and tree layouts, the logging allocator and the static strings built at start-up"
kind: "system"
category: "Third-party libraries"
addresses: "001EDF00, 00902720, 001EDF10, 001EDF80, 001EDFE0, 0016D690, 01F82E48, 001FF740, 02EBA2E0, 001E7D30, 0016D6D0, 0016D720, 0016D780, 0016D7E0, 0016D840, 0016DA60, 001A3380, 00200E60, 0015D610, 0015C560, 0015D2F0, 0015D230, 0015FFE0, 001A52A0, 001FC640"
---

## What the player sees

Nothing directly. EASTL, Electronic Arts' container library, holds much of the game's text and many
of its lists, sets and maps, from JSON files read through JsonBox to sorted lookup tables. Knowing its layouts matters when reading any structure in the
executable: three consecutive pointers followed by an allocator are usually one string or one
vector, not four fields.

## How it works

### Identity

The image names the library in its own RTTI: `eastl::allocator_memory_log` (`01F480F8`) and
`eastl::allocator` (`01F7E300`). The allocator's constructor `001EDF00` writes the
`allocator_memory_log` vtable `00902720`. Containers pass one of five name strings to that
constructor: `EASTL basic_string` (`008F6600`), `EASTL vector` (`008C5F58`), `EASTL set`
(`008F3CB0`), `EASTL list` (`008F3CC0`) and `EASTL map` (`008F4120`). The constructor is called from
583 sites in 230 functions.

### The allocator

`001EDF00` stores the vtable and returns; the name argument is never kept. The vtable at `00902720`
has six slots, followed by 0 at `00902750`:

| Slot offset | Function | What it does |
|---|---|---|
| `00`<sub>h</sub> | `0016D680` | returns the object |
| `08`<sub>h</sub> | `001EDF10` | `_aligned_malloc(size, alignment)` |
| `10`<sub>h</sub> | `001EDF80` | `_aligned_malloc(size, 16)`; the allocation every container uses |
| `18`<sub>h</sub> | `001EDFE0` | `_aligned_free(p)` when `p` is not null; callers pass the size, which it ignores |
| `20`<sub>h</sub> | `0016D690` | returns the name `EASTL` (`01CDAE78`) |
| `28`<sub>h</sub> | `0016D6A0` | `ret 0`, an empty function at EASTL's `set_name` position |

Each of the three memory slots first creates, once, a 32-byte record at `01F82E48` holding
`2000000`<sub>h</sub>, `200000`<sub>h</sub>, 0 and 0. Only those three functions refer to the record, and none of them
reads it, so no allocation is logged or attributed.

### Strings

An `eastl::basic_string<char>` is `20`<sub>h</sub> bytes: begin, end and capacity end pointers followed by an
allocator object (see Layouts). There is no inline buffer. Building a string from C text (`001FF740`
is one site):

1. measure the text; with `n` = length + 1,
2. when `n` is below 2, point end and capacity end at the shared byte `02EBA2E0` and `02EBA2E1`
   without allocating;
3. otherwise allocate `n` bytes through slot `+10`<sub>h</sub> and set capacity end to the block plus `n`;
4. copy the text with `memmove`, set end to the last character and write the terminator.

Every empty string in the process points at the same byte. Freeing is guarded by
`capacity end - begin > 1` and a non-null begin, so the shared byte is never freed.

### Vectors

`001E7D30` inserts `n` copies of a 16-byte element. When the free capacity is too small it allocates
`max(size + n, size == 0 ? 1 : 2 × size)` elements through the vector's own allocator at `+18`<sub>h</sub>,
copies the elements before the insertion point, writes the new ones, copies the rest and frees the
old block. A vector grown one element at a time therefore holds 1, 2, 4, 8 … elements.

### Sets and maps: the red-black tree

Every EASTL set and map in the game shares one balanced-tree runtime of six functions. A node starts
with right, left and parent pointers and a colour byte (red 0, black 1); the key and value follow at
`+20`<sub>h</sub>.

- `0016D6D0` steps to the next node: down the right child and then left as far as possible, or up
  while the node is its parent's right child. It writes nothing.
- `0016D720` steps to the previous node, the mirror image, after first returning the anchor's right
  link when the node is the red anchor itself (its parent's parent is itself).
- `0016D780` and `0016D7E0` rotate left and right; only the erase calls them.
- `0016D840` inserts a node: it initialises the node's links and colour, hangs it on the chosen side
  of its parent, updates the anchor's leftmost, rightmost and root links, recolours, rotates inline
  (for example `0016D8C7` to `0016D912`, including the root update at the anchor's `+10`<sub>h</sub>, and the
  mirror case), and paints the root black (`0016DA4F`). It has 90 call sites in 56 functions.
- `0016DA60` erases a node: it splices in the replacement, swaps the two nodes' colour bytes
  (`0016DBA9` to `0016DBB7`) and rebalances with the two rotations.

The comparison that decides left or right is the caller's. `001A3380` is a typical map insert: it
walks from the root comparing an `int` key at node `+20`<sub>h</sub>, allocates a `38`<sub>h</sub>-byte node through the
container's allocator at `+30`<sub>h</sub>, copies a 20-byte value to node `+20`<sub>h</sub>, calls `0016D840` with the
anchor at container `+08`<sub>h</sub>, and increments the count at `+28`<sub>h</sub>.

### Static strings and containers built at start-up

64 entries of the start-up initialiser table build EASTL objects. Each constructs the named allocator,
fills the object and registers its destructor with `atexit` (`00808B90`). `0015D610` is typical: it
allocates 5 bytes for `null`, copies 4, terminates, and registers `008A70F0`. An initialiser for an
empty literal (`0015C560`, text `01CEB638`) takes the shared byte instead and copies 0 bytes. Two
more (`0015D2F0`, `0015DBB0`) build an empty string with no copy at all, and four build empty
containers (`0015D230` a vector, `001601C0` a list, `0015D260` and `0016A2C0` maps).

The 52 non-empty strings are four copies of the 13 strings a JSON writer and reader need: the escapes
`\"`, `\\`, `\/`, `\b`, `\f`, `\n`, `\r`, `\t`, `\u`, the words `true`, `false`, `null` and the hex
digits `0123456789ABCDEFabcdef`. They belong to JsonBox, which the image names in its RTTI
(`JsonBox::Indenter`, `JsonBox::IndentCanceller`, `JsonBox::SolidusEscaper`).
The four copies of `\t` are built by `0015D9D0`, `0015E780`, `0015F3B0` and `0015FFE0`; the last
allocates 3 bytes, copies the two characters from `009047BC` into the static string at `01FD3FB8`
and registers `008A8050`.

### Code instantiated per element type

The compiler emits the string, vector and tree operations once for each element type, so the same
operation appears many times with different element sizes. 32 such bodies are listed in
`eastl-strings-and-containers-template-instances.tsv` with the operation and the element or node
size of each; the other 75 are on
[object construction and destruction](../Compiler-And-C-Runtime/object-construction-and-destruction.md).

- `001A52A0` appends a character range to a string. When the result does not fit, the new capacity
  is 8 while the old capacity is below 9, otherwise twice the old one, and never less than the
  length needed; it then copies both parts into the new block and frees the old one.
- `001FC640` is a map's `operator[]` with a `u32` key at node `+20`<sub>h</sub>: it walks from the root
  `+18`<sub>h</sub>, and when the key is missing it inserts a default value, an empty vector whose allocator
  is named `EASTL vector`, through `001FD310`.

The string bodies follow the rules under Strings: `001B38B0` and `001A4BF0` take the shared byte
`02EBA2E0` when the length plus one is below 2.

### JsonBox values

JsonBox stores parsed JSON in EASTL containers. Its reader `00200E60` constructs allocators named
`EASTL map`, `EASTL vector` and `EASTL basic_string` for objects, arrays and strings, and its string
reader `00201C40` carries JsonBox's message `Expected '"', got '` (`00905008`). `00200BF0` reads a
whole file into a stream and hands it to `00200E60`; the screen-layout files are read this way.

## Layouts

Eastl::basic_string&lt;char&gt;   `20`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | begin | first character |
| `08`<sub>h</sub> | `void*` | end | the terminator; length = end - begin |
| `10`<sub>h</sub> | `void*` | capacityEnd | one past the block; `02EBA2E1` for an empty string |
| `18`<sub>h</sub> | `void*` | allocator | the allocator object itself (its vtable pointer) |

Eastl::vector&lt;T&gt;:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | begin |  |
| `08`<sub>h</sub> | `void*` | end | size = (end - begin) / sizeof(T) |
| `10`<sub>h</sub> | `void*` | capacityEnd |  |
| `18`<sub>h</sub> | `void*` | allocator | the allocator object itself |

Tree node (set and map elements):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | right |  |
| `08`<sub>h</sub> | `void*` | left |  |
| `10`<sub>h</sub> | `void*` | parent |  |
| `18`<sub>h</sub> | `u8` | colour | 0 red, 1 black |
| `20`<sub>h</sub> | `...` | value | key first; node size is `20`<sub>h</sub> plus the value |

Map container, as `001A3380` uses it:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `08`<sub>h</sub> | `node` | anchor | its +`00`<sub>h</sub> rightmost, +`08`<sub>h</sub> leftmost, +`10`<sub>h</sub> root |
| `28`<sub>h</sub> | `u32` | count |  |
| `30`<sub>h</sub> | `void*` | allocator | the allocator object itself |

## Shipped data

| Fact | Value |
|---|---|
| start-up initialisers in the executable's C++ table | 1,172 |
| initialisers that build EASTL objects | 64 |
| strings copied from a literal | 58: 52 non-empty, 6 empty |
| strings built empty without a copy | 2 |
| containers built empty | 4: 2 maps, 1 vector, 1 list |
| distinct non-empty literals | 13, each copied 4 times |

## Modding notes

- Never free or write through a string whose capacity end is `02EBA2E1`: that is the shared empty
  byte every empty string points at.
- Every non-empty string owns a heap block; there is no short-string storage to overflow into.
- Replacing the allocator vtable's slots `+10`<sub>h</sub> and `+18`<sub>h</sub> redirects every EASTL allocation. The
  container names are not passed through, so a hook cannot tell containers apart by name.
- A tree node's payload starts at `+20`<sub>h</sub> whatever the container; the key is its first field.
- Changing one of JsonBox's static token strings changes only one of its four copies.

## Related

- [Screen layouts](../Menus-And-HUD/screen-layouts.md): JSON files parsed through `00200BF0` into JsonBox
  values.
- `eastl-strings-and-containers-string-static-initialisers.tsv`,
  `eastl-strings-and-containers-basicstring-variant-initialisers.tsv` and
  `eastl-strings-and-containers-container-static-initialisers.tsv`: the start-up initialisers.
- `eastl-strings-and-containers-ordered-container-runtime.tsv` and
  `eastl-strings-and-containers-ordered-container-runtime-callers.tsv`: the tree runtime and its
  callers.
- `eastl-strings-and-containers-template-instances.tsv`: container code instantiated per element
  type.
- [Object construction and destruction](../Compiler-And-C-Runtime/object-construction-and-destruction.md):
  the other per-type container bodies and the record-pool template they build.
