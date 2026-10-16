---
title: "MSVC containers: the std::map tree, std::string and std::regex code linked into the executable"
kind: "system"
category: "Compiler and C runtime"
summary: "The Microsoft standard-library containers that sit in FFXII_TZA.exe beside the engine's EASTL: the std::map / std::set red-black tree with its head node, lookup, insert, erase and clear routines and its three instantiations, the std::string layout and its deallocation rule, the std::regex instantiation behind one event-path check, and the MSVCP140 imports these containers call."
addresses: "00714800, 0070D360, 00712F60, 0071E500, 00714DC0, 00714CE0, 00714B60, 00714980, 006FF5D0, 006FF840, 0071D170, 0071EE70, 00169270, 008B7940, 02EA5550, 001DFA10, 0020A800, 009058C0, 008C2618, 008C2430, 001A1990, 001A5500, 001A5630, 00865EC0, 001A1EA0, 00195940, 00197A50, 0019B580, 0019B990, 001A1920, 00865E30, 001E0360, 0020AFE0"
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

A tree object is 16 bytes: a pointer to its head node and an element count. `00714800` makes the
head: it allocates `0x30` bytes through `00210EC0` (which forwards to `malloc`), points the head's
left, parent and right links at the head itself, and writes `0x0101` at `+0x18`, so the head's colour
is 1 (black) and its nil byte is 1 (`00714848`).

Once the tree has elements, the head's parent link is the root, its left link the smallest node and
its right link the largest. Real nodes have nil byte 0.

### Lookup

`0070D360` is a lookup over the tree at `+0xC8` of its object. It starts at the root (`[head+8]`),
compares the 64-bit key at node `+0x20` without sign (`0070D380`), goes left and remembers the node
when the node's key is not below the search key, and goes right otherwise, until it reaches a node
whose nil byte is set. It returns the qword at `+0x28` of the remembered node when that node's key
equals the search key, and 0 otherwise.

### Insert

`00712F60` links a new `0x30`-byte node and rebalances. It first compares the count at `+8` with
`0x0555555555555554` (`00712F6D`), one less than the largest count of `0x30`-byte nodes. When the
count has reached it, it frees the node through `00210EB0` and calls `_Xlength_error` (slot
`008C2618`) with `map/set<T> too long` (`00D8E138`). The rotations are inline, and the last store
paints the root black (`007131FD`, `mov byte ptr [root+0x18], 1`).

`0071E500` is the same routine for `0x60`-byte nodes (limit `0x02AAAAAAAAAAAAA9`). On the length
failure it first destroys the node's value at `+0x20` (`0071E528`, `call 0071EE70`).

### Erase and clear

- `00714CE0` erases a range. When the range is the whole tree (from the head's left link to the
  head), it calls the clear routine `00714B60`. Otherwise it steps through the range, finding each
  successor inline (down the right child and then left, or up while the node is a right child), and
  erases each node with `00714DC0`.
- `00714DC0` unlinks one node and rebalances with the rotations `00714B00` and `0071F240`.
- `00714B60` clears the tree: from the root it walks the left links, destroys each node's right
  subtree with `00714980` and frees the node through `00210EB0`. It then points the head's three
  links back at the head and sets the count to 0.

The full list of these routines is in `msvc-containers-ordered-container-runtime.tsv`.

### Three instantiations

| Tree | Node | Built by | Holds |
|---|---:|---|---|
| A: three maps at `+0xA8`, `+0xB8` and `+0xC8` of the post-effect state block | `0x30` | `006FF5D0`, which makes the heads with `00714800`, `007147A0` and `00714740` | a 64-bit key at node `+0x20` and a pointer at `+0x28` |
| B: one map | `0x60` | node builder `0071F180` | two strings, at node `+0x20` and `+0x40` |
| C: a static map at `02EA5550` | `0x28` head | `00169270` at start-up | nothing: no code inserts into it |

- A is cleared by `006FF840`, which erases each map's whole range (`00714CE0`, `00715110`,
  `007151F0`) and frees its head. All three use the one insert `00712F60` and the one node erase
  `00714DC0`.
- B is the parsed licence of the post-effect library. `006DFF40` calls the checker `0071CD10`, which
  calls `0071D170`. That routine parses the text into the map (`0071CE10`, inserting through
  `0071EA80` and `0071E500`) and looks fields up by name: `FeatureId` (`00D9B190`), `BeginYear`
  (`00D9B19C`) and the other date fields, `MacAddress` (`00D9B1E4`) and `License`.
- `0071EE70` destroys a B element: two strings, the mapped one at `+0x20` of the pair first, then the
  key at `+0x00`.
- C is built by the dynamic initialiser `00169270` (head from `00799B20`, `0x28` bytes) and its
  destructor `008B7940` is registered with `atexit` (`00808B90`). Only those two routines refer to
  `02EA5550` and `02EA5558`.

### Strings

`std::string` is 32 bytes. The first 16 bytes hold the characters while the capacity is below 16;
from capacity 16 on, they hold a pointer to a heap buffer of capacity + 1 bytes. `0071EE70` and the
catch funclet `00896993` show the release sequence:

1. When the capacity at `+0x18` is 16 or more, free the buffer with `001DFA10`.
2. Store capacity 15 and size 0.
3. Store a terminating zero in the first character.

`001DFA10` handles large buffers before calling `free`: when the byte count is `0x1000` or more, the
pointer must be 32-byte aligned and the real block start is the qword just before it, between 8 and
`0x27` bytes lower. When any of these checks fails it calls `_invalid_parameter_noinfo_noreturn`
(slot `008C2DA8`).

### std::regex

The `char` instantiation of `std::regex` is linked in with its twelve node classes, whose one-slot
vtables run from `009058C0` (`std::_Node_base`) to `00905A28` (`std::_Node_class<char, regex_traits<char>>`).
Its parser reports errors through `_Xregex_error` (slot `008C2430`, 31 call sites).

The game code that uses it is `0020A800`, called from `0020AC30`. It compiles the pattern
`(.*)(\\plan_master\\([a-zA-Z]+)\\event\\)(.*)` (`00905958`) and matches its string argument
against it (`00203790`), so it tests whether a path has the form `…\plan_master\<name>\event\…`. The
regex routines that only this use reaches are listed in `msvc-containers-stl-regex-char.tsv`.

The rest of the instantiation, 92 bodies between `002031A0` and `0020B000`, is listed in
`msvc-containers-stl-regex-char-members.tsv` with one function that refers to each. All but four
are called only from `0020A800` and the routines of the first list. The node destructors `002043A0`
(`_Node_class`) and `00204660` (`_Node_if`) are called by the deleting destructors in the vtables at
`00905A28` and `00905930`; `00206CD0` and `00204590` are reached from the catch funclet `008996A0`
of `00206AD0` and the unwind funclet `008999D0` of `0020A800`.

Two examples. `00209530` is the parser's lexer step: it looks the next character up in the
metacharacters `()$^.*+?[]|\-{},:=!` plus newline, carriage return and backspace (`009059B8`,
through `strchr`) and turns it into a token according to the syntax flags. `00205890` parses one
alternative. It raises `_Xregex_error` with 5 on a `)` outside any group (`00205B02`), and with 6,
4 and 10 at `00205B0E`, `00205B1A` and `00205B26`.

### std::sort

`006B9CF0`, slot 1 of `Phyre::PRendering::PContextSwitchLights`, uses two instantiations of the
Microsoft `std::sort`: `006B82A0` over 8-byte elements with a comparator function, and `006B8180`
over 32-bit values compared with `<`. It passes the element count as the starting depth budget.
Both follow the library's introsort:

1. A range of 32 elements or fewer goes to an insertion sort: `006B6FE0` for the 8-byte elements,
   `006B6F30` for the 32-bit values.
2. A longer range is partitioned around a median guess (`006B7800`, `006B7660`): of three elements
   below 41, of nine from 41 on. The 8-byte partition `006B7800` takes the guess from `006B6D70`
   (`cmp rax, 0x28` at `006B6D8D`), which orders each group of three with the comparator through
   `006B7560`; the 32-bit partition takes it from `006B6C20`. The smaller side is sorted by
   recursion and the larger by the loop.
3. Each partition cuts the budget to `budget/2 + budget/4`. When it reaches 0 the range is
   heap-sorted: `006B7290` and `006B71A0` build the heap, `006B8060` and `006B7FC0` pop it, sifting
   through `006B7CF0` and `006B7C20`.

### Library members compiled into the image

Beside the tree, 49 more bodies of the Microsoft library are compiled from its headers rather than
imported. `msvc-containers-library-members.tsv` names each with the import, vtable or failure string
that identifies it:

- `std::string` and `std::wstring` growth, append, assign, erase, find, compare, `operator+` and move. `00195670` grows a
  string: it rounds the capacity up with `or 0xF`, grows it by half, and fails through `_Xbad_alloc`.
- The file streams: the `basic_ifstream<wchar_t>`, `basic_ofstream<wchar_t>` and
  `basic_ofstream<char>` destructor bodies (`00195440`, `001954B0`, `0019B480`) and the
  `basic_filebuf` open (`00197A50`, `0019B990`), `_Endwrite` (`00195940`, `0019B580`) and close (`001969D0`,
  `0019B8C0`, through `fclose`). The key-binding writer
  `001993B0` calls `001969D0`.
- The string streams: the `basic_stringbuf` constructor `001DDFD0`, its `str()` `001E0100` (the stream's `001E0360`) and the
  destructors of `basic_istringstream`, `basic_ostringstream` and `basic_stringstream`.
- The inserters `00194CD0` (wide string) and `001DDE10` (narrow), `std::endl` `00194EB0`, the
  `std::exception` and `std::bad_cast` copy constructors, and two vector members (`001A4D20`,
  `0020E420`), and `001A1EA0`, the header's `sprintf_s` into a 32-byte buffer.

### The library calls behind the containers

The containers and the streams call `MSVCP140.dll`, which supplies 115 of the image's import slots.
The failure helpers are the ones the container code reaches most:

| Import | Slot | Call and jump sites |
|---|---|---:|
| `std::_Xlength_error` | `008C2618` | 59 |
| `std::_Xregex_error` | `008C2430` | 31 |
| `std::_Xbad_alloc` | `008C2608` | 23 |
| `std::_Xout_of_range` | `008C2620` | 14 |
| `std::_Xinvalid_argument` | `008C2610` | 2 |

Most of the rest are character and wide-character stream, stream-buffer and locale members. The stream
inserters and extractors that use them are on [exception-handling.md](exception-handling.md), where
their sentry destructors appear.

## Layouts

`MsvcTree` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u64` | head | pointer to the head node |
| `08` | `u64` | count | number of elements |

`MsvcTreeNode` (offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u64` | left | smaller child; in the head, the smallest node |
| `08` | `u64` | parent | parent; in the head, the root |
| `10` | `u64` | right | larger child; in the head, the largest node |
| `18` | `u8` | color | 0 red, 1 black |
| `19` | `u8` | isNil | 1 in the head node only |
| `20` | `...` | the element, key first: 0x10 bytes in tree A, 0x40 in tree B, 8 in tree C |  |

`MsvcString` (`0x20` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8[16]` | chars | the characters while capacity is below 16; otherwise a heap pointer in the first 8 bytes |
| `10` | `u64` | size | characters in use |
| `18` | `u64` | capacity | 15 for the inline buffer |

## Shipped data

| Fact | Value |
|---|---|
| tree node sizes in use | `0x30` (tree A), `0x60` (tree B), `0x28` head of tree C |
| insert length limits | `0x0555555555555554` (`00712F60`), `0x02AAAAAAAAAAAAA9` (`0071E500`) |
| `std::regex` node classes | 12, vtables `009058C0` to `00905A28` |
| `MSVCP140.dll` import slots | 115 |
| `_Xlength_error` call sites | 59 |
| further `std::regex` bodies (`msvc-containers-stl-regex-char-members.tsv`) | 92 |
| other library bodies compiled in (`msvc-containers-library-members.tsv`) | 49 |
| `std::sort` insertion-sort limit | 32 elements (`cmp rax, 0x20` at `006B81AA`) |

## Modding notes

- Check `+0x19` before treating a node pointer as a tree node of either library: a Microsoft node has
  a nil byte there, and its parent link is at `+0x08`, where EASTL keeps the left child.
- Walking a Microsoft tree ends at the node whose nil byte is 1, which is the head; the head is never
  an element.
- A buffer of `0x1000` bytes or more that is handed to `001DFA10` must come from the matching
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
  runs `00169270` and the `atexit` registration of `008B7940`.
- [Memory and allocation](memory-and-allocation.md): `malloc` and `free` behind `00210EC0` and
  `00210EB0`.
- [Thunks and import stubs](thunks-and-import-stubs.md): how the `MSVCP140` imports are reached.
