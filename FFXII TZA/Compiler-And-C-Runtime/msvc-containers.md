---
title: "MSVC containers: the std::map tree, std::string and std::regex code linked into the executable"
kind: "system"
category: "Compiler and C runtime"
addresses: "0x00714800, 0x0070D360, 0x00712F60, 0x0071E500, 0x00714DC0, 0x00714CE0, 0x00714B60, 0x00714980, 0x006FF5D0, 0x006FF840, 0x0071D170, 0x0071EE70, 0x00169270, 0x008B7940, 0x02EA5550, 0x001DFA10, 0x0020A800, 0x009058C0, 0x008C2618, 0x008C2430, 0x001A1990, 0x001A5500, 0x001A5630, 0x00865EC0, 0x001A1EA0, 0x00195940, 0x00197A50, 0x0019B580, 0x0019B990, 0x001A1920, 0x00865E30, 0x001E0360, 0x0020AFE0"
---

## What the player sees

Nothing directly. The game's own code keeps its strings, vectors, sets and maps in EASTL (see
[EASTL strings and containers](../Third-Party-Libraries/eastl-strings-and-containers.md)). The
Microsoft containers on this page belong to code built against the standard library instead: the
post-effect library keeps three lookup maps and parses its licence into a fourth, one start-up
initialiser builds a static map, and one event-path check uses `std::regex`.

## How it works

### Two red-black trees in one image

The image holds two balanced-tree runtimes with different node layouts. EASTL's node keeps right,
left and parent links at `+0x00`, `+0x08` and `+0x10`. The Microsoft node keeps left, parent and
right there, and adds a byte at `+0x19` that is 1 only in the head node. Every walk in this family
stops on that byte (`cmp byte ptr [node+0x19], 0`); the EASTL runtime has no member there.

### The container and its head node

A tree object is 16 bytes: a pointer to its head node and an element count. `0x00714800` makes the
head: it allocates `0x30` bytes through `0x00210EC0` (which forwards to `malloc`), points the head's
left, parent and right links at the head itself, and writes `0x0101` at `+0x18`, so the head's colour
is 1 (black) and its nil byte is 1 (`0x00714848`).

Once the tree has elements, the head's parent link is the root, its left link the smallest node and
its right link the largest. Real nodes have nil byte 0.

### Lookup

`0x0070D360` is a lookup over the tree at `+0xC8` of its object. It starts at the root (`[head+8]`),
compares the 64-bit key at node `+0x20` without sign (`0x0070D380`), goes left and remembers the node
when the node's key is not below the search key, and goes right otherwise, until it reaches a node
whose nil byte is set. It returns the qword at `+0x28` of the remembered node when that node's key
equals the search key, and 0 otherwise.

### Insert

`0x00712F60` links a new `0x30`-byte node and rebalances. It first compares the count at `+8` with
`0x0555555555555554` (`0x00712F6D`), one less than the largest count of `0x30`-byte nodes. When the
count has reached it, it frees the node through `0x00210EB0` and calls `_Xlength_error` (slot
`0x008C2618`) with `map/set<T> too long` (`0x00D8E138`). The rotations are inline, and the last store
paints the root black (`0x007131FD`, `mov byte ptr [root+0x18], 1`).

`0x0071E500` is the same routine for `0x60`-byte nodes (limit `0x02AAAAAAAAAAAAA9`). On the length
failure it first destroys the node's value at `+0x20` (`0x0071E528`, `call 0x0071EE70`).

### Erase and clear

- `0x00714CE0` erases a range. When the range is the whole tree (from the head's left link to the
  head), it calls the clear routine `0x00714B60`. Otherwise it steps through the range, finding each
  successor inline (down the right child and then left, or up while the node is a right child), and
  erases each node with `0x00714DC0`.
- `0x00714DC0` unlinks one node and rebalances with the rotations `0x00714B00` and `0x0071F240`.
- `0x00714B60` clears the tree: from the root it walks the left links, destroys each node's right
  subtree with `0x00714980` and frees the node through `0x00210EB0`. It then points the head's three
  links back at the head and sets the count to 0.

The full list of these routines is in [`msvc-containers-ordered-container-runtime.tsv`](msvc-containers-ordered-container-runtime.tsv).

### Three instantiations

| Tree | Node | Built by | Holds |
|---|---:|---|---|
| A: three maps at `+0xA8`, `+0xB8` and `+0xC8` of the post-effect state block | `0x30` | `0x006FF5D0`, which makes the heads with `0x00714800`, `0x007147A0` and `0x00714740` | a 64-bit key at node `+0x20` and a pointer at `+0x28` |
| B: one map | `0x60` | node builder `0x0071F180` | two strings, at node `+0x20` and `+0x40` |
| C: a static map at `0x02EA5550` | `0x28` head | `0x00169270` at start-up | nothing: no code inserts into it |

- A is cleared by `0x006FF840`, which erases each map's whole range (`0x00714CE0`, `0x00715110`,
  `0x007151F0`) and frees its head. All three use the one insert `0x00712F60` and the one node erase
  `0x00714DC0`.
- B is the parsed licence of the post-effect library. `0x006DFF40` calls the checker `0x0071CD10`, which
  calls `0x0071D170`. That routine parses the text into the map (`0x0071CE10`, inserting through
  `0x0071EA80` and `0x0071E500`) and looks fields up by name: `FeatureId` (`0x00D9B190`), `BeginYear`
  (`0x00D9B19C`) and the other date fields, `MacAddress` (`0x00D9B1E4`) and `License`.
- `0x0071EE70` destroys a B element: two strings, the mapped one at `+0x20` of the pair first, then the
  key at `+0x00`.
- C is built by the dynamic initialiser `0x00169270` (head from `0x00799B20`, `0x28` bytes) and its
  destructor `0x008B7940` is registered with `atexit` (`0x00808B90`). Only those two routines refer to
  `0x02EA5550` and `0x02EA5558`.

### Strings

`std::string` is 32 bytes. The first 16 bytes hold the characters while the capacity is below 16;
from capacity 16 on, they hold a pointer to a heap buffer of capacity + 1 bytes. `0x0071EE70` and the
catch funclet `0x00896993` show the release sequence:

1. When the capacity at `+0x18` is 16 or more, free the buffer with `0x001DFA10`.
2. Store capacity 15 and size 0.
3. Store a terminating zero in the first character.

`0x001DFA10` handles large buffers before calling `free`: when the byte count is `0x1000` or more, the
pointer must be 32-byte aligned and the real block start is the qword just before it, between 8 and
`0x27` bytes lower. When any of these checks fails it calls `_invalid_parameter_noinfo_noreturn`
(slot `0x008C2DA8`).

### std::regex

The `char` instantiation of `std::regex` is linked in with its twelve node classes, whose one-slot
vtables run from `0x009058C0` (`std::_Node_base`) to `0x00905A28` (`std::_Node_class<char, regex_traits<char>>`).
Its parser reports errors through `_Xregex_error` (slot `0x008C2430`, 31 call sites).

The game code that uses it is `0x0020A800`, called from `0x0020AC30`. It compiles the pattern
`(.*)(\\plan_master\\([a-zA-Z]+)\\event\\)(.*)` (`0x00905958`) and matches its string argument
against it (`0x00203790`), so it tests whether a path has the form `…\plan_master\<name>\event\…`. The
regex routines that only this use reaches are listed in [`msvc-containers-stl-regex-char.tsv`](msvc-containers-stl-regex-char.tsv).

The rest of the instantiation, 92 bodies between `0x002031A0` and `0x0020B000`, is listed in
[`msvc-containers-stl-regex-char-members.tsv`](msvc-containers-stl-regex-char-members.tsv) with one function that refers to each. All but four
are called only from `0x0020A800` and the routines of the first list. The node destructors `0x002043A0`
(`_Node_class`) and `0x00204660` (`_Node_if`) are called by the deleting destructors in the vtables at
`0x00905A28` and `0x00905930`; `0x00206CD0` and `0x00204590` are reached from the catch funclet `0x008996A0`
of `0x00206AD0` and the unwind funclet `0x008999D0` of `0x0020A800`.

Two examples. `0x00209530` is the parser's lexer step: it looks the next character up in the
metacharacters `()$^.*+?[]|\-{},:=!` plus newline, carriage return and backspace (`0x009059B8`,
through `strchr`) and turns it into a token according to the syntax flags. `0x00205890` parses one
alternative. It raises `_Xregex_error` with 5 on a `)` outside any group (`0x00205B02`), and with 6,
4 and 10 at `0x00205B0E`, `0x00205B1A` and `0x00205B26`.

### std::sort

`0x006B9CF0`, slot 1 of `Phyre::PRendering::PContextSwitchLights`, uses two instantiations of the
Microsoft `std::sort`: `0x006B82A0` over 8-byte elements with a comparator function, and `0x006B8180`
over 32-bit values compared with `<`. It passes the element count as the starting depth budget.
Both follow the library's introsort:

1. A range of 32 elements or fewer goes to an insertion sort: `0x006B6FE0` for the 8-byte elements,
   `0x006B6F30` for the 32-bit values.
2. A longer range is partitioned around a median guess (`0x006B7800`, `0x006B7660`): of three elements
   below 41, of nine from 41 on. The 8-byte partition `0x006B7800` takes the guess from `0x006B6D70`
   (`cmp rax, 0x28` at `0x006B6D8D`), which orders each group of three with the comparator through
   `0x006B7560`; the 32-bit partition takes it from `0x006B6C20`. The smaller side is sorted by
   recursion and the larger by the loop.
3. Each partition cuts the budget to `budget/2 + budget/4`. When it reaches 0 the range is
   heap-sorted: `0x006B7290` and `0x006B71A0` build the heap, `0x006B8060` and `0x006B7FC0` pop it, sifting
   through `0x006B7CF0` and `0x006B7C20`.

### Library members compiled into the image

Beside the tree, 50 more bodies of the Microsoft library are compiled from its headers rather than
imported. [`msvc-containers-library-members.tsv`](msvc-containers-library-members.tsv) names each with the import, vtable or failure string
that identifies it:

- `std::string` and `std::wstring` growth, append, assign, erase, find, compare, `operator+` and move. `0x00195670` grows a
  string: it rounds the capacity up with `or 0xF`, grows it by half, and fails through `_Xbad_alloc`.
- The file streams: the `basic_ifstream<wchar_t>`, `basic_ofstream<wchar_t>` and
  `basic_ofstream<char>` destructor bodies (`0x00195440`, `0x001954B0`, `0x0019B480`) and the
  `basic_filebuf` open (`0x00197A50`, `0x0019B990`), `_Endwrite` (`0x00195940`, `0x0019B580`) and close (`0x001969D0`,
  `0x0019B8C0`, through `fclose`). The key-binding writer
  `0x001993B0` calls `0x001969D0`.
- The string streams: the `basic_stringbuf` constructor `0x001DDFD0`, its `str()` `0x001E0100` (the stream's `0x001E0360`) and the
  destructors of `basic_istringstream`, `basic_ostringstream` and `basic_stringstream`.
- The six streams' deleting destructors (each vtable's slot 0, reached through an adjustor that subtracts the
  virtual-base offset first). Each steps back to the whole object, runs its destructor and, when bit `0x1` of
  the flag is set, frees the object with the sized `delete` `0x00809950`; the string streams also run the
  `basic_ios` destructor through import slot `0x008C25E8`:

  | Deleting destructor | Stream | Steps back | Frees |
  |---|---|---|---|
  | `0x00195570` | `basic_ifstream<wchar_t>` | `0xB0` | `0x110` |
  | `0x001955B0` | `basic_ofstream<wchar_t>` | `0xA8` | `0x108` |
  | `0x0019B540` | `basic_ofstream<char>` | `0xA8` | `0x108` |
  | `0x001DE3B0` | `basic_istringstream<char>` | `0x90` | `0xF0` |
  | `0x001DE400` | `basic_ostringstream<char>` | `0x88` | `0xE8` |
  | `0x001DE4A0` | `basic_stringstream<char>` | `0x98` | `0xF8` |
- The inserters `0x00194CD0` (wide string) and `0x001DDE10` (narrow), `std::endl` `0x00194EB0`, the
  `std::exception` and `std::bad_cast` copy constructors, and two vector members (`0x001A4D20`,
  `0x0020E420`), and `0x001A1EA0`, the header's `sprintf_s` into a 32-byte buffer.

### The library calls behind the containers

The containers and the streams call `MSVCP140.dll`, which supplies 115 of the image's import slots.
The failure helpers are the ones the container code reaches most:

| Import | Slot | Call and jump sites |
|---|---|---:|
| `std::_Xlength_error` | `0x008C2618` | 59 |
| `std::_Xregex_error` | `0x008C2430` | 31 |
| `std::_Xbad_alloc` | `0x008C2608` | 23 |
| `std::_Xout_of_range` | `0x008C2620` | 14 |
| `std::_Xinvalid_argument` | `0x008C2610` | 2 |

Most of the rest are character and wide-character stream, stream-buffer and locale members. The stream
inserters and extractors that use them are on [exception-handling.md](exception-handling.md), where
their sentry destructors appear.

## Layouts

`MsvcTree` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | head | pointer to the head node |
| `+0x08` | `u64` | count | number of elements |

`MsvcTreeNode` (offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | left | smaller child; in the head, the smallest node |
| `+0x08` | `u64` | parent | parent; in the head, the root |
| `+0x10` | `u64` | right | larger child; in the head, the largest node |
| `+0x18` | `u8` | color | 0 red, 1 black |
| `+0x19` | `u8` | isNil | 1 in the head node only |
| `+0x20` | `...` | the element, key first: 0x10 bytes in tree A, 0x40 in tree B, 8 in tree C |  |

`MsvcString` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[16]` | chars | the characters while capacity is below 16; otherwise a heap pointer in the first 8 bytes |
| `+0x10` | `u64` | size | characters in use |
| `+0x18` | `u64` | capacity | 15 for the inline buffer |

## Shipped data

| Fact | Value |
|---|---|
| tree node sizes in use | `0x30` (tree A), `0x60` (tree B), `0x28` head of tree C |
| insert length limits | `0x0555555555555554` (`0x00712F60`), `0x02AAAAAAAAAAAAA9` (`0x0071E500`) |
| `std::regex` node classes | 12, vtables `0x009058C0` to `0x00905A28` |
| `MSVCP140.dll` import slots | 115 |
| `_Xlength_error` call sites | 59 |
| further `std::regex` bodies (`msvc-containers-stl-regex-char-members.tsv`) | 92 |
| other library bodies compiled in (`msvc-containers-library-members.tsv`) | 50 |
| `std::sort` insertion-sort limit | 32 elements (`cmp rax, 0x20` at `0x006B81AA`) |

## Modding notes

- Check `+0x19` before treating a node pointer as a tree node of either library: a Microsoft node has
  a nil byte there, and its parent link is at `+0x08`, where EASTL keeps the left child.
- Walking a Microsoft tree ends at the node whose nil byte is 1, which is the head; the head is never
  an element.
- A buffer of `0x1000` bytes or more that is handed to `0x001DFA10` must come from the matching
  allocation, with the real start stored just before it, or the game stops in
  `_invalid_parameter_noinfo_noreturn`.
- Tree C is built and freed but never filled, so changing it has no effect on the game.

## Related

- [EASTL strings and containers](../Third-Party-Libraries/eastl-strings-and-containers.md): the
  game's own tree, string and vector.
- [YEBIS and PPFX](../Third-Party-Libraries/yebis-ppfx-post-effects.md): the post-effect library
  that owns trees A and B, and its licence check.
- [Exception handling](exception-handling.md): the catch funclet that frees a string, and the stream
  routines.
- [Static initialisation and teardown](static-initialisation-and-teardown.md): the start-up table that
  runs `0x00169270` and the `atexit` registration of `0x008B7940`.
- [Memory and allocation](memory-and-allocation.md): `malloc` and `free` behind `0x00210EC0` and
  `0x00210EB0`.
- [Thunks and import stubs](thunks-and-import-stubs.md): how the `MSVCP140` imports are reached.
