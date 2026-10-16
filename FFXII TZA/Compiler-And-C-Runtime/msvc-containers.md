---
title: "MSVC containers: the std::map tree, std::string and std::regex code linked into the executable"
kind: "system"
category: "Compiler and C runtime"
summary: "The Microsoft standard-library containers that sit in FFXII_TZA.exe beside the engine's EASTL: the std::map / std::set red-black tree with its head node, lookup, insert, erase and clear routines and its three instantiations, the std::string layout and its deallocation rule, the std::regex instantiation behind one event-path check, and the MSVCP140 imports these containers call."
addresses: ["00714800", "0070D360", "00712F60", "0071E500", "00714DC0", "00714CE0", "00714B60", "00714980", "006FF5D0", "006FF840", "0071D170", "0071EE70", "00169270", "008B7940", "02EA5550", "001DFA10", "0020A800", "009058C0", "008C2618", "008C2430"]
---

# MSVC containers: the std::map tree, std::string and std::regex code linked into the executable

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

```struct MsvcTree base=record size=0x10
+0x00  u64  head   pointer to the head node
+0x08  u64  count  number of elements
```

```struct MsvcTreeNode base=record
+0x00  u64  left    smaller child; in the head, the smallest node
+0x08  u64  parent  parent; in the head, the root
+0x10  u64  right   larger child; in the head, the largest node
+0x18  u8   color   0 red, 1 black
+0x19  u8   isNil   1 in the head node only
+0x20  ...  the element, key first: 0x10 bytes in tree A, 0x40 in tree B, 8 in tree C
```

```struct MsvcString base=record size=0x20
+0x00  u8[16]  chars     the characters while capacity is below 16; otherwise a heap pointer in the first 8 bytes
+0x10  u64     size      characters in use
+0x18  u64     capacity  15 for the inline buffer
```

## Shipped data

| Fact | Value |
|---|---|
| tree node sizes in use | `0x30` (tree A), `0x60` (tree B), `0x28` head of tree C |
| insert length limits | `0x0555555555555554` (`00712F60`), `0x02AAAAAAAAAAAAA9` (`0071E500`) |
| `std::regex` node classes | 12, vtables `009058C0` to `00905A28` |
| `MSVCP140.dll` import slots | 115 |
| `_Xlength_error` call sites | 59 |

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
