---
system: The EASTL red-black tree - the six bodies every keyed lookup in the game shares
category: 24-Compiler-And-CRT-Runtime
status: DOCUMENTED — every register row is closed: the library, payload offset, node sizes and child sides (OC-1..OC-3, answered 2026-09-15); the 99 callers enumerated (OC-4) and read for purpose (SD-81, answered 2026-09-30: 24 unique-key map/set instantiations, 56 insert wrappers, 30 inline erases, 12 walks); inlined rotations (SD-82, answered 2026-09-30). Owner re-status 2026-09-30 (OPUS)
owner_layer: CodeDomain:CxxStandardLibrary.OrderedContainerRuntime; no PrimaryOwner
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: all six bodies disassembled whole from the shipping EXE and each extent checked to its
    last instruction; structure offsets counted per body by read/write/test; call edges and caller
    subsystems from work/graph/edges.tsv and functions.tsv
last_reviewed: 2026-09-30
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-15
  last_pass_state: fable-ordered-container-falsification-1
  crossref_clean: false
  reopened_count: 0
function_families_withdrawn: "2026-09-30 (OPUS): the ordered-container row (members/ordered-container-runtime.tsv, 6) is withdrawn - all six members are measured A on this DOCUMENTED page, and A beats a declaration; the members file stays as the enumeration"
---

# The ordered-container runtime

> Six compiler-emitted bodies, 1,741 bytes, that hold every sorted keyed lookup in the game -
> and that three documents have described as memory management because none of them had a page
> to point at.
>
> **They are EASTL's `rbtree`, and the node layout is what says so.**

## 1. What the player sees

Nothing directly, and that is the point: this is the toolchain's own code, not the game's.

What a player *does* see is the effect of it being fast and shared. When a gambit list is
re-sorted, when a kerning pair is looked up to place one character next to another, when a sound
bank finds an entry by name, when a texture-animation list finds its slot - each of those is a
lookup in a sorted collection, and every one of them runs through these same six routines. The
game does not contain six of these for six subsystems; it contains one set, used by all of them.

If it broke, nothing would break *specifically*. Text, audio, effects, gambits and resource
loading would all fail together, which is the signature of a shared runtime rather than a
feature.

## 2. Native mechanism

A red-black tree is a sorted collection that stays balanced as things are added and removed. Each
entry is a node; each node points at up to two children, at its parent, and carries a single byte
of bookkeeping. These six routines are the whole of the balancing machinery. The *container* - the
thing that knows what a key is, how to compare two of them, and where the memory came from - sits
above them and is not part of this family.

**The node header, read out of the bodies rather than assumed.** Every one of the six touches
exactly four offsets:

| offset | width | EASTL name | what the bodies do with it |
|---|---|---|---|
| `+0x00` | 8 | `mpNodeRight` | descended by the increment on its way to a successor, relinked by both rotations |
| `+0x08` | 8 | `mpNodeLeft` | descended by the decrement, relinked by both rotations |
| `+0x10` | 8 | `mpNodeParent` | every body reads it; the rotations and both rebalances write it. **This offset is the identification** |
| `+0x18` | 1 | `mColor` | red is `0`, black is `1`. Tested by the decrement's sentinel check, written 9 times by the insert and 18 times by the erase; **never touched by either rotation** |

The colour row is the layout falling out of behaviour rather than being asserted: a red-black
rotation relinks pointers and does not recolour, and neither rotation body writes `+0x18`. The
red/black values are fixed the same way - the insert's last two instructions read the root out of
the head and write `1` into its `mColor` (`0016DA4B` / `0016DA4F`), and a red-black insert ends by
making the root **black**.

**Which library, and how the bytes decide it.** EASTL's `rbtree_node_base` declares
`mpNodeRight`, `mpNodeLeft`, `mpNodeParent`, `mColor` in that order - parent at `+0x10`. MSVC's
`std::_Tree_node` declares `_Left`, `_Parent`, `_Right` - parent at `+0x08`. **All six bodies
climb parents through `+0x10`**, in loops that cannot mean anything else, so the layout is
EASTL's and not MSVC's. Corroboration from a different direction: the consumer cluster that calls
these six constructs an `eastl::allocator_memory_log`, a class the image names in its own RTTI
type descriptor.

**That second line is NOT this page's, and the first draft failed to say so.** [eastl-strings-containers-and-the-logging-allocator.md](../../23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md)
carries that constructor in its own key-address table as `eastl_allocator_memory_log_ctor` — **named
there and deliberately not by address here**, because it has 230 callers and citing it would drag two
more subsystems onto this page that have nothing to do with the tree — states *“The
library is EASTL and the allocator class is `eastl::allocator_memory_log`”* on exactly the same
14-byte body, and had done so before this page existed. I re-derived it and cited nothing.
**What is new here is the first line, not the second:** that page establishes the library for
`basic_string`, `vector` and the allocator, and **names none of these six bodies** — it does not
claim the tree is EASTL's. The node layout is what carries the tree, and that argument is this
page's own.

**A key sits at `+0x20`, and this family never looks at it.** No body in the family reads any
offset at or beyond `+0x20`. The comparison that decides left from right happens in the caller,
before it ever gets here.

**The two iterator steps - `0016D6D0` is `RBTreeIncrement`, `0016D720` is `RBTreeDecrement`.**
These answer *"what is the next entry in sorted order?"* Neither writes a single byte of memory;
they are pure navigation. `0016D6D0`: if `mpNodeRight` is non-null, go to it and descend
`mpNodeLeft` to the minimum of that subtree; otherwise climb parents for as long as this node is
its parent's **right** child. That is a successor, instruction for instruction. `0016D720` is the
mirror - descend `mpNodeRight` to the maximum of the left subtree, else climb while a **left**
child - with the one extra step a decrement needs and an increment does not: it first tests
`mpNodeParent->mpNodeParent == this` together with `mColor == 0`, which is EASTL's sentinel case,
and returns `mpNodeRight` when both hold. Walking off the end of the collection has to be
detected rather than followed, and only one direction can hit it.

**The two rotations - `0016D780` is `RBTreeRotateLeft`, `0016D7E0` is `RBTreeRotateRight`.** A
rotation is the local repair that keeps the tree shallow: one node takes its child's place and the
child takes the node's. `0016D780` takes `mpNodeRight` and hangs its `mpNodeLeft` back on the
node - a left rotation - then reparents each moved node through `+0x10` and fixes whichever of the
head's three links pointed at the old top. `0016D7E0` is the same body with `mpNodeRight` and
`mpNodeLeft` exchanged. They are mirror images at the instruction level and differ in nothing
else.

**The insert - `0016D840`, EASTL's `RBTreeInsert`.** It receives a node, its intended parent, the
container head and a side selector in `r9d`. Its first four stores *build* the node - `[node+0x10] = parent`,
`[node+0x00] = 0`, `[node+0x08] = 0`, `[node+0x18] = 0` - which is the fact that most cleanly
refutes calling it a release. It then links the node on the selected side, updates whichever of
the head's `mpNodeLeft` / `mpNodeRight` / `mpNodeParent` the new node becomes, and runs the
recolouring loop, ending by reading the root out of the head at `+0x10` and painting it black
(`0016DA4B mov rax, [r8+0x10]` / `0016DA4F mov byte [rax+0x18], 1`). **That last pair also settles
the head's own layout:** the head is node-shaped, and its `+0x00`, `+0x08`, `+0x10` are the
collection's rightmost, leftmost and root - which is what the insert's three conditional head
updates are choosing between.

**The erase - `0016DA60`, EASTL's `RBTreeErase`.** The largest of the six and the only one that
calls anything. It finds
the node that will take the removed node's place (the same descent the iterator steps do), splices
it in, **swaps the two nodes' bookkeeping bytes** (`0016DBA9`-`0016DBB7`: read both `+0x18`, write
each into the other), then runs the fix-up loop, which is where the rotations are called. It makes
37 pointer stores in all.

## 3. Key addresses

All addresses are VAs with image base `0x00120000` already included.

| address | bytes | callers | callees | role |
|---|---:|---:|---:|---|
| `0016D6D0` | 68 | 58 | 0 | `RBTreeIncrement` - successor. **Zero stores** |
| `0016D720` | 94 | 24 | 0 | `RBTreeDecrement` - predecessor, with the sentinel case. **Zero stores** |
| `0016D780` | 92 | 1 | 0 | `RBTreeRotateLeft` |
| `0016D7E0` | 88 | 1 | 0 | `RBTreeRotateRight` |
| `0016D840` | 532 | 56 | 0 | `RBTreeInsert` - builds the node, links it, recolours, blackens the root |
| `0016DA60` | 867 | 30 | 2 | `RBTreeErase` - splices, swaps colours, rotates |

The two rotations have exactly one caller each and it is `0016DA60`. The insert has none, because
the toolchain inlined its rotations into it - one implementation, two inlining outcomes. *(Anchored 2026-09-30, SWE2-DATA: `0016D840` makes no call and holds the `RBTreeRotateLeft` body instruction for instruction at `0016D8D5`..`0016D912`, with the root written back to the header at `+0x10`. Its store signature holds two left-shaped and one right-shaped copies. Control `_index/candidates/dd-data-2-0930/crt_rbtree_checks.py` E1, C1.)*

## 4. Data structures and formulas

The node header is the table in §2. There is no formula: the balancing rules are the standard
red-black invariants, and the bodies implement them without any game-specific constant. No member
reads an immediate that encodes a game value; the only constants in the family are `0` and `1` for
the bookkeeping byte and the structure offsets themselves.

**Size is still not established by this family, and that stays true** - these six bodies never
compute a node size or step an array, so nothing *here* says a node is `0x20` bytes rather than
`0x20` plus a payload.

**It is established one level up, and measured rather than inferred.** Every caller that allocates
a node does it in the same four instructions, immediately before the insert: it fetches the
allocator sub-object's vtable, puts the size in `edx`, calls `allocate` through `[vtable+0x10]`, and
then applies an offset to what comes back before writing the value into it. Over **90 call sites to
`0016D840`, 80 of which allocate**, that offset is `+0x20` at **80 of 80** - no exception anywhere in
the image - and the size is one of **nine** distinct values:

| `edx` at the allocate | header + payload | call sites |
|---|---|---:|
| `0x28` | `0x20` + `0x08` | 16 |
| `0x30` | `0x20` + `0x10` | 15 |
| `0x38` | `0x20` + `0x18` | 10 |
| `0x40` | `0x20` + `0x20` | 5 |
| `0x48` | `0x20` + `0x28` | 10 |
| `0x50` | `0x20` + `0x30` | 4 |
| `0x58` | `0x20` + `0x38` | 5 |
| `0x60` | `0x20` + `0x40` | 10 |
| `0x88` | `0x20` + `0x68` | 5 |

**Nine sizes, every one of them `0x20` plus a multiple of eight, and not one of them `0x20` or
less.** The `80 of 80` is register-tracked rather than windowed: the `+0x20` is required to land
on the register holding the allocate's return, or a plain copy of it, **and** that register must
be what reaches `rcx` at the insert. Eighty sites pass both conditions and none fails either. So the header is `0x20`, the payload starts at `+0x20`, and **the node has no single size** -
it is `0x20 + sizeof(Value)`, and this image holds nine different values. That last part is not a gap
in the measurement; it is what a *shared* runtime means, and it is why the family cannot compute the
size it never needs.

The clearest single site is `001A3380`: `lea edx, [r8+0x38]` with `r8` zeroed, `call [rax+0x10]`,
`add rax, 0x20`, then `movups [rax], xmm0` and `mov [rax+0x10], ecx` - twenty bytes of value written
at `node+0x20`, in a `0x38`-byte node. `001A3220` is the same shape with a single dword
(`mov [rax], ecx` after `add rax, 0x20`, `0x28` bytes), and `001A3BE0` allocates `0x88` and runs a
constructor at `node+0x28` after copying a pointer to `node+0x20`.

**This confirms [`font-data-kerning-and-expansion.md`](../../16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md)
§4.2 from a completely different direction** - that page read a key at `node+0x20` inside one
consumer; this is the allocation arithmetic of eighty sites that never mention a key. And it is what
`rbtree_node<Value>` predicts, `rbtree_node_base` being `0x19` bytes and eight-aligned - but the
prediction is not what carries it here. **NOT CLAIMED:** which value type any particular size
belongs to, and what the `0x88` node holds. *(Both answered 2026-09-30 by SWE2-ORACLE's SD-81 record, `08f4c0821`,
[`sd81-eastl-callers-0930`](../../_index/candidates/sd81-eastl-callers-0930/README.md): its 24-instantiation table
gives each node size its key compare and value layout. The `0x88` node is instantiation I06, a tagged `EASTL map`
keyed by an unsigned qword whose `0x60`-byte value is copied in by `001A2750` at `+0x28`. The set/map word for an
untagged instantiation is that record's INFERENCE, and it says so.)*

## 5. Call chain

Callers reach the family directly; there is no dispatcher and no vtable in front of it. The
family's internal structure is one edge pair: `0016DA60` calls `0016D780` and `0016D7E0`, and
nothing else in the image calls either.

**The caller census, and it is why this page exists.** 170 call edges from **99 distinct
callers**, of which **71 call two or more members** - the signature of a shared runtime rather
than six unrelated leaves. By the subsystem attribution `audit_crossrefs` uses:

| caller subsystem | callers |
|---|---:|
| substrate / shape classes (no subsystem) | 72 |
| **Audio** | 13 |
| **Presentation** | 7 |
| **Resource** | 5 |
| **Platform** | 2 |

### The 99, enumerated and grouped

*Added 2026-09-15 (FABLE). `OC-4` asked for the 72 substrate callers to be enumerated rather than
counted; all **99** are, in
[`members/ordered-container-runtime-callers.tsv`](members/ordered-container-runtime-callers.tsv),
with two structural groupings that need no reading for meaning.*

**Every one of the 99 is `FUN_xxxxxxxx`.** Not one caller of this family carries a name. That is a
fact about where the family sits rather than about the callers: the code that uses the ordered
container is the code nobody has had a reason to name, which is the same reason this page did not
exist until today.

**The first grouping is which members a caller uses, and it is sharper than expected.** Six
signatures occur, and **no caller uses more than two of the six**:

| signature | callers | what two members together means |
|---|---:|---|
| `inc` + `era` | 30 | walk and remove — a clear, or an erase-by-predicate |
| `dec` + `ins` | 24 | **a hinted insert**; see below |
| `inc` + `ins` | 16 | walk and add |
| `ins` | 16 | add only |
| `inc` | 12 | walk only |
| `rotL` + `rotR` | 1 | `0016DA60` itself — the family's only internal edge |

`30 + 24 + 16 + 16 + 12 + 1 = 99`, and `60 + 48 + 32 + 16 + 12 + 2 = 170`, which is the page's edge
count arrived at from the other direction. **No caller pairs `ins` with `era`.** These are not
general container users; each is a single container operation, which is what compiler-emitted
`insert` / `erase` / `clear` bodies look like.

**Two numbers that are both right and are not the same number.** There are **170 distinct
(caller, callee) pairs** — the page's "170 call edges" — across **213 call sites**, because a caller
that inserts in two branches is one pair and two sites. The TSV carries sites; §5's figure is pairs.

**The second grouping is the node size**, from `OC-2`'s allocation reading: **48** of the 99 allocate
before an insert, and the nine sizes cluster by address — `0x38` and `0x88` in `001A3xxx`/`001A4xxx`,
`0x48` and `0x60` in `001FCxxx`/`001FDxxx`, `0x40` in `001BDxxx`, `0x50` in `001FFxxx`/`00200xxx`,
`0x58` in `001B9xxx`/`001BAxxx`. Callers that allocate the same node size and sit together are the
same container instantiated once; that is a candidate partition into container families, and it is
offered as one rather than asserted.

**The `dec` + `ins` twenty-four are hinted inserts, and the body says so.** `00199DB0` and
`001A3220` are the same shape:

```asm
00199E16  test  dl, dl                  ; the caller passed "I have a hint"
00199E1A  cmp   rbx, [rcx + 0x10]       ; is the hint the collection's first node?
00199E20  mov   rcx, rbx
00199E23  call  0016D720                ; --hint
00199E2E  cmp   [rbx + 0x20], rax       ; is the PREDECESSOR's key below the new one?
00199E43  mov   edi, 1                  ; ... then the side is 1
00199E6C  lea   edx, [r8 + 0x28]        ; allocate 0x28
00199E70  call  [rax + 0x10]
00199E76  add   rax, 0x20               ; the payload
00199E7F  mov   [rax], rcx              ; the key
00199E82  mov   r9d, edi                ; side
00199E85  mov   r8,  r12                ; head
00199E88  mov   rdx, rbx                ; parent
00199E8B  mov   rcx, r14                ; node
00199E8E  call  0016D840
```

**That confirms three of this page's claims from the caller's side, where none of them was measured
before.** `0016D720` is the **decrement** — `OC-3` decided that from the library and from the
sentinel test; here it is *used* as `--hint`, which only a decrement can be. The key sits at
**`node+0x20`** — and this is a **third independent line** for `OC-2`, different in kind from both
the others: the font page read a key there, §4 measures the allocation offset there, and this
**compares an existing node's key** there, before any allocation happens. And `r9d` really is the
**side selector** the insert's description calls it: `edi` is set to `1` or `0` by that comparison
and nothing else.

**One level up, and recorded as such.** The same bodies increment a counter at `[container+0x28]`
after a successful insert and return a two-word `{node, true}` through `rsi`. Those are facts about
the *container*, not this family, and this page does not adopt them — but they are where a reader
should start if the wrappers are ever documented.

**These crossings are the subject here, not an accident.** A page that documents a shared runtime
is *expected* to reach Audio, Presentation, Resource and Platform, because that is what "shared"
means: each of those subsystems keeps at least one sorted keyed collection, and the ordered
container it uses is this one. That is the whole of the relationship - none of these subsystems
has anything specific to do with this code, and this code has no knowledge of any of them. It is
the same relationship every one of the 72 substrate callers has.

## 6. Modding notes

**Do not detour any of these six.** A detour on one of them is a detour on every sorted collection
in the game at once - 99 call sites across audio, text, effects and resource loading. `0016D6D0`
alone is reached from 58 places. There is no way to scope a hook here to one subsystem, because
nothing in the family knows which subsystem called it.

If you need to observe one container's contents, hook the container wrapper that calls these, not
these.

**XIIOnline:** nothing here carries gameplay state, and nothing here is worth synchronising. It is
below the layer where anything about the game exists.

## 7. What is not known

- [x] ~~**Which container library this is.**~~ **ANSWERED 2026-09-15 (OPUS) - EASTL, decided by the
      parent pointer.** **OC-1.**
      *EASTL's `rbtree_node_base` is `{mpNodeRight +0, mpNodeLeft +8, mpNodeParent +0x10, mColor +0x18}`;
      MSVC's `std::_Tree_node` is `{_Left +0, _Parent +8, _Right +0x10}`. **All six bodies climb parents
      through `+0x10`**, in loops whose whole purpose is to reach a parent, and under MSVC's layout that
      offset is a child. The question was filed believing the header compatible with either reading; it
      is not, and the discriminator was already measured on this page before the question was written.*
      *Corroborated from a different direction: the consumer cluster that calls these six constructs an
      `eastl::allocator_memory_log`, named in the image's own RTTI type descriptor. Two independent
      lines, neither derived from the other. The `mColor` values follow too - the insert ends by writing
      `1` into the root's colour, and `kRBTreeColorRed` is `0`.*
- [x] ~~**The node's total size, and where the payload begins.**~~
      **ANSWERED 2026-09-15 (FABLE) - measured in the callers, because that is the only place either
      fact is expressed.** **OC-2.**
      *The payload begins at `+0x20`: over 90 call sites to `0016D840`, the 80 that allocate apply
      `+0x20` to the returned pointer before writing the value into it, at **80 of 80**. The node has
      **no single size** - the allocate takes one of **nine** values, `0x28` `0x30` `0x38` `0x40`
      `0x48` `0x50` `0x58` `0x60` `0x88`, every one `0x20` plus a multiple of eight and none of them
      `0x20` or less. So the header is `0x20` and the node is `0x20 + sizeof(Value)`, which is what a
      shared runtime looks like from the allocation side. Confirms the font page's `node+0x20` key
      from a direction that never reads a key. See §4.*
- [x] ~~**Which of `+0x00` and `+0x08` is "left".**~~ **ANSWERED 2026-09-15 (OPUS) alongside OC-1 -
      `+0x00` is `mpNodeRight` and `+0x08` is `mpNodeLeft`.** **OC-3.**
      *It follows from the library, and it is checked against behaviour rather than assumed: `0016D6D0`
      goes to `+0x00` and then descends `+0x08` to that subtree's extreme, which is a **successor** only
      if `+0x00` is the right child. `0016D720` is the one carrying the sentinel test, and a decrement is
      the direction that can walk off the end of an EASTL tree. So `0016D6D0` is `RBTreeIncrement` and
      `0016D720` is `RBTreeDecrement`, and the rotations follow: `0016D780` takes `mpNodeRight` (a left
      rotation), `0016D7E0` takes `mpNodeLeft`.*
- [x] ~~**The 72 substrate callers are not enumerated.** They are counted, not read.~~
      **ANSWERED 2026-09-15 (FABLE) — all 99 enumerated in
      [`members/ordered-container-runtime-callers.tsv`](members/ordered-container-runtime-callers.tsv),
      with two structural groupings.** **OC-4.**
      *Six member signatures and **no caller uses more than two of the six**: `inc`+`era` 30,
      `dec`+`ins` 24, `inc`+`ins` 16, `ins` 16, `inc` 12, `rotL`+`rotR` 1 — summing to 99 callers and
      170 pairs across 213 call sites. **Every one of the 99 is `FUN_xxxxxxxx`.** 48 allocate, in the
      nine `OC-2` node sizes, clustered by address. The `dec`+`ins` 24 are hinted inserts, read whole
      at `00199DB0`. **THE BOUNDARY:** enumerated and grouped **structurally**; not one caller was
      read for purpose, and §5's subsystem attribution is still `audit_crossrefs`', not derived here.
      What "substrate" means for the 72 is unchanged by this. See §5.* *(The boundary is closed by SD-81, below: the
      callers were read for purpose, and 56 of them are the insert wrappers of 24 unique-key map/set instantiations.)*
- [x] **What the 99 callers build with the tree, and which wrappers sit between them and the six bodies.** §5 groups them structurally, and its subsystem split is `audit_crossrefs`'. No caller was read for purpose, the value type behind each measured node size is not tied to a caller, and no container wrapper was examined. **SD-81** (SWE2-DATA, 2026-09-30). *(SD-81 answered 2026-09-30 by OPUS `08f4c0821`, [record](../../_index/candidates/sd81-eastl-callers-0930/README.md).)*
- [x] **Whether any body inlines a single EASTL rotation, or any body over 20,000 bytes inlines one.** The both-direction sweep (§9, 2026-09-30 note) finds no inlined pair outside this family and Phyre's own tree. A copy of one direction alone, or one inside a body the sweep skips, is not ruled out. **SD-82** (SWE2-DATA, 2026-09-30). *(SD-82 answered 2026-09-30 by OPUS `6836e8067`, [record](../../_index/candidates/sd80-82-ordered-containers-0930/README.md).)*

## 8. Evidence

Read whole from the shipping EXE, authority hash
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base `0x00120000`.
Degrees and caller subsystems from `work/graph/edges.tsv` and `work/graph/functions.tsv`.

**Full-body boundaries, checked rather than assumed.** All six extents end in `ret` exactly at the
size the function list records: `0016D713`, `0016D77D`, `0016D7DB`, `0016D837`, `0016DA53`,
`0016DDC2`.

**The layout-closure control.** Counting every memory operand in all six bodies by read, write and
test, over 521 instructions: the only structure offsets that appear are `+0x00`, `+0x08`, `+0x10`
and `+0x18`. A family that reached a key, a payload or an allocator would show it here and none
does.

**The rotation control.** `0016DA60` is the only body in the image that calls `0016D780` or
`0016D7E0`, and each of them has exactly one caller. An erase is the one red-black operation that
needs both directions.

**The negative that refutes the memory reading.** `0016D6D0` and `0016D720` contain **no store
instruction at all**, and four of the six members — both iterator steps, the insert and both
rotations — have **zero callees**. The only calls anywhere in the family are the erase's two, and
they go to the rotations. An allocator must call something; a routine that unlinks must store
something; and nothing here reaches a heap function at any depth.

**Two prior readings agree, independently of this page and of each other.**
[`game-application.md`](../../00-Engine-Core-Runtime/Application-Root/game-application.md) line 624
calls `0016D840`'s users "red-black-insert users", and
[`ta-texture-animation-lists.md`](../../02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md)
line 279 groups `0016D840`/`0016D720` users under "container iterators".

**Three readings did not.** Corrected under `CON-121` and `OPUS-CONTRA-AUDIO-UNLINK-IS-A-READ`:
[`font-data-kerning-and-expansion.md`](../../16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md)
called `0016D6D0` and `0016D720` "alloc" and `0016D840` a "release", and a second page calls
`0016D6D0` an "unlink" three times and `0016DA60` a "pool-free". The absence of this page is the
cause: a shared runtime with 99 callers and no document of its own gets described by whoever
happens to cite it, from the position it occupies in their call sequence.

**The identification, stated as a negative too, and with its prior art.** The allocator half was
published first on [eastl-strings-containers-and-the-logging-allocator.md](../../23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md) and is cited, not claimed, here; the tree half is this page's.
Nothing in the six bodies contains a string, a symbol or an import that names EASTL. The identification rests on a structure offset and on a
class name found in a *neighbouring* consumer, and it would be overturned by any red-black
implementation that puts its parent pointer third. ~~None is known in this image: these six are the
only red-black machinery in it.~~ **Corrected 2026-09-15 by FABLE's falsification pass (section 9):
there are three rotation pairs in this image and four erase-shaped bodies, not one and one — and
the other two pairs are MSVC's `std::_Tree`.** That makes the sentence false and the *identification*
stronger than it was: the discriminator no longer rests on library headers, because **both layouts
are in this binary and can be read against each other**. See section 9.

**The tags are four heads for one family, and one of them is right.** `0016D840` carries
`CxxStandardLibrary.OrderedContainerRuntime.RedBlackTreeInsertRebalance`. `0016D6D0` and
`0016DA60` carry `Runtime.ContainerStringSupport`, and neither touches a string. `0016D720` carries
`NativeInline.NoCall.TableAccessorOrComputation`, and it is not a table accessor. The two rotations
carry `NativeInline.NoCall.ConditionalStateAlgorithm`. The `NoCall` half of those three is exactly
right, and is the same fact the callee-count control turns on.

## 9. Falsification pass 1 — 2026-09-15 (FABLE, independent)

Run by a reader who is not the author, against the shipping image at authority hash
`73461d08…9721f8`. Every number below was re-derived from the bytes before the page's own was
looked at. **Nine claims survived, two did not, and one attack failed in a way worth recording.**

### What survived, re-measured rather than re-read

| claim on this page | independent result |
|---|---|
| six extents, 1,741 bytes, each ending in `ret` at `0016D713` / `0016D77D` / `0016D7DB` / `0016D837` / `0016DA53` / `0016DDC2` | **all six**, exactly |
| layout closure — only `+0x00`, `+0x08`, `+0x10`, `+0x18` are touched, nothing at or beyond `+0x20` | **confirmed**: 76 / 70 / 94 / 45 operands on those four and no other non-stack displacement anywhere in the six |
| 170 call edges, 99 distinct callers, 71 of them calling two or more members | **170 / 99 / 71** — three independent counts, all exact |
| `0016D6D0` and `0016D720` contain no store instruction at all | **confirmed** — see the note below, because my first instrument said otherwise and it was wrong |
| four of the six have zero callees; the erase calls only the two rotations | **confirmed** — the erase's only external targets are `0016D780` and `0016D7E0`, at four call sites |
| the rotations have exactly one caller each and it is `0016DA60` | **confirmed, and strengthened** |
| `+0x18` written 9 times by the insert, 18 times by the erase, **never** by either rotation | **9 / 18 / 0 / 0** — exact |
| the erase makes 37 pointer stores | **37** qword stores — exact |
| the insert's first four stores build the node | **confirmed**: `0016D842 mov [rcx+0x10], rdx` · `0016D846 mov [rcx], rax` · `0016D849 mov [rcx+8], rax` · `0016D84D mov byte [rcx+0x18], al` |

**The rotation claim is stronger than the page states it.** "Exactly one caller" was measured from
direct call edges, and a direct-edge census cannot see a call made through a table or through the
image-base idiom — which is how two other absence claims in this database have failed this month. So
it was checked the other way too: **none of the six addresses appears anywhere in the image as a
little-endian qword, and none of them is ever the target of a `lea`.** They are not in a pointer
table, not in a vtable, and not reachable as `[00120000 + d]`. Direct calls are the whole of the
population, and the page can say so.

> **The qword half of that read nothing at all the first time, and is re-run here with a control.**
> As first published it called `Image.read(0x00120000, 0x00F00000)` — the image **base**, which is
> the PE header and lies in no section, so the reader returned `None` and the search ran over **zero
> bytes** and reported zero hits for everything. **A search that has not read a byte agrees with
> every absence claim ever made.** Re-run 2026-09-16 section by section over all **31.3 MB** of raw
> data, with two controls that must fire and do: six strings that have to be in the image
> (`navimapdata`, `EnableYebis`, `YEBIS_D3D11`, `Bin_Menu`, `.?AVallocator_memory_log@eastl@@`,
> `CRASH`) are all found, and **a function address that genuinely is in a pointer table is found
> where it lives** — `002A9F00`, stored at `009164D0`, the dispatch table this database documents
> under the image-base idiom. On that instrument the six still score **zero**, so the claim stands.
> It stands on evidence that did not exist when it was first written.

### What did not survive

**1. The instruction count is 521, not 621.** `24 + 29 + 29 + 29 + 154 + 256`. The extents are
right — they sum to the page's own 1,741 bytes and each ends in `ret` where the page says — so this
is the count and nothing else. The closure conclusion is unaffected: it holds over the 521 that are
actually there. Corrected in both places.

**2. These six are not the only red-black machinery in the image.** The page's identification rests
on a structure offset, and it guards that with *"it would be overturned by any red-black
implementation that puts its parent pointer third. None is known in this image."* Three more are.

A rotation is the most distinctive body a red-black implementation has, so the census was run on the
rotation shape taken from the two documented ones rather than on anything invented: no calls, at
least eight qword stores, **writes confined to `+0x00`/`+0x08`/`+0x10` and never to the colour byte
at `+0x18`**, reads confined to the node header. Thirteen bodies match; six of those write a single
offset eight times and are not rotations. **The rest are three mirror pairs:**

| rotation pair | sizes | called by | erase body |
|---|---|---|---|
| `0016D780` / `0016D7E0` | 92 / 88 B | 1 caller each | `0016DA60` — **this page's** |
| `00714B00` / `0071F240` | 89 / 85 B | 2 callers each | `00714DC0` (840 B) **and** `0071F590` (978 B) — **MSVC** |
| `00799BD0` / `00799C30` | 89 / 85 B | 1 caller each | `0079BA10` (978 B) — **MSVC** |

The pairing is not asserted from size. Each pair is a mirror in its store profile the same way the
documented pair is — `00714B00` writes `+0x00`×2, `+0x08`×6, `+0x10`×4 and `0071F240` writes
`+0x00`×4, `+0x08`×6, `+0x10`×2, against `0016D780`'s ×2/×4/×5 and `0016D7E0`'s ×4/×2/×5 — and
neither member of any pair touches `+0x18`, which is this page's own discriminator for a rotation.
The three undocumented erases carry the documented erase's profile: **18 writes to `+0x18` and 14
reads of it, writes confined to the same four offsets.** `0016DA60` writes `+0x18` 18 times and
reads it 14. So does each of them.

**And they are not EASTL. They are MSVC's `std::_Tree` — the layout this page's discriminator
excludes — so the falsified sentence turns out to have named the very thing that was there.**

Read a rotation from each family side by side and the answer is four instructions long. In
`0016D780` every reparenting store is `[X + 0x10] = Y`: `0016D793 mov [rax+0x10], rcx`,
`0016D79B mov [r8+0x10], rax`, and `mov [rcx+0x10], r8` at `0016D7AE`, `0016D7C8` and `0016D7D7`.
In `00714B00` every reparenting store is `[X + 8] = Y`: `00714B14 mov [rax+8], rdx`,
`00714B1C mov [r8+8], rax`, `00714B29 mov [rax+8], r8`, and `mov [rdx+8], r8` at `00714B31`,
`00714B48` and `00714B54`. `00799BD0` is the same again. **The invariant offset across a mirror pair
is the parent**, because a rotation exchanges the two children and reparents three nodes — so the
parent write lands at `+0x10` for this family and at `+0x08` for the other two, which is exactly
`mpNodeParent +0x10` against `_Parent +0x08`.

The `+0x19` byte settles it from the second direction. `00714B0E cmp byte [rax+0x19], 0` guards
those reparenting stores, and `0079BA10` opens on `cmp byte [r8+0x19], 0` and descends through
nineteen more. MSVC's node is `{_Left +0, _Parent +8, _Right +0x10, _Color +0x18, _Isnil +0x19}` —
**`_Isnil` is exactly that byte**, and EASTL's `rbtree_node_base` has no such member, which is why
the documented six never read `+0x19` and these never stop reading it. Their erases calling the
image's `free` — deliberately not cited by address here, for the reason section 10 gives about the
guard stub: it has 242 callers and a page inherits the caller set of every address it cites — fits
the same reading, MSVC's `_Tree` owning its nodes where EASTL's `rbtree` erase does not.

**So OC-1's answer survives and its argument improves.** It rested on two library headers and a
class name found in a neighbour. It now rests on a contrast *inside this binary*: one operation,
written twice by two toolchains, with the parent in two different places, and the six on the EASTL
side of it. What falls is the sentence — and that sentence is why nobody went looking, because it
asserted in advance that there would be nothing to find. `0079BA10`, `00799BD0`, `00799C30` and
`006B52A0` are named by no document in the database; the other four appear in `ADDRESS-INDEX.md` as
table-only entries. Filed as `FABLE-CONTRA-OPUS-OC1-THREE-RBTREES-NOT-ONE`; **OC-1's row is OPUS's
and this pass does not edit it.**

> **Corrected in place, an hour after I wrote it.** The first version of this section said the other
> pairs *“put the parent at `+0x10` too, so MSVC is not back in the running”*. That was read off a
> store-offset histogram — `+0x00`/`+0x08`/`+0x10` in every pair, mirroring the same way — without
> reading a single rotation body. **The histograms are identical between the two families; the
> bodies are not**, and which offset is the parent is visible only in the instruction. I had the
> counts and took the conclusion from them, which is the one thing this page's own author did not
> do.

One loose end, recorded because it is unexplained rather than because it is load-bearing:
`006B52A0` (102 B) ~~has the rotation shape~~ — writes `+0x00`×4, `+0x08`×4, `+0x10`×2, no calls — and
**no caller at all**. *(Corrected 2026-09-30, SWE2-DATA: it is not red-black code. It walks a singly linked child list from `[parent+0x10]` through each node's `+0`, unlinks the node, stores the new parent at `[node+8]` and pushes the node on the new parent's list: a reparent over parent / first-child / next-sibling links. No call, jump or pointer reaches it. Its one reference is a `lea` in the `PScene::PNode` reflection registrar, which stores it in a `PMethodCallerConcrete<PNode, void, PNode&>` caller registered under the name `addChild`. It is `PNode::addChild`, called only through reflection. Control `_index/candidates/dd-data-2-0930/crt_rbtree_checks.py` E3, C2.)*

### The attack that failed, and why it is reported anyway

The page says the toolchain inlined the insert's rotations into it. If inlining happened once it can
have happened elsewhere, and **an inlined copy is invisible to every census on this page**, because
all of them count call edges. Two instruments were built to look for inlined tree code and **both
failed to discriminate**: storing to all four node offsets matches **1,264** bodies, which is only to
say that objects have four qwords at the front; a colour-byte comparison at `+0x18` together with a
parent load at `+0x10` still matches 60 non-family bodies, almost all with a count of one. The three
trees above were found by the *rotation* shape, which is a separate, out-of-line body — so the
finding says nothing about how much inlined red-black code the image holds.

~~**That question stays open and no instrument here touches it.**~~ *(Corrected 2026-09-30, SWE2-DATA: an instrument now reaches most of it. The store-displacement signatures of the two rotations (children `+0`/`+8`, parent `+0x10`) find the rotation in its own body and nothing in a non-tree body. Swept over every body up to 20,000 bytes, only four hold both shapes: this family's insert and erase, and Phyre's own red-black tree (`0067F700`, `0067F9D0`, parent-and-colour word at `+0x10`), which the reflection pages already describe. So no other body inlines an EASTL rotation pair. A single inlined direction, and bodies over 20,000 bytes, are what the sweep cannot rule out: **SD-82**. Control `_index/candidates/dd-data-2-0930/crt_rbtree_checks.py` E4.)* The result of an attack that fails
is that the claim is unconfirmed, not that it is safe: what an instrument cannot see is not
discoverable from the things it can.

### Not examined by this pass

The subsystem attribution of the 99 callers (OC-4 counts them and this pass did not read them);
the container wrappers
above the family; and whether `0016D840` genuinely inlines its rotations, per the paragraph above. *(2026-09-30, SWE2-DATA: the inlining is answered (§3 note, E1); the callers' purpose and the container wrappers are **SD-81**.)*

## 10. Related

- [`the-return-value-adapter-family.md`](../Generated-Adapters/the-return-value-adapter-family.md) -
  the other large "this is the toolchain, not the game" family in this category.
- [eastl-strings-containers-and-the-logging-allocator.md](../../23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md) -
  the same library from the string and allocator side, and the page that named
  `eastl::allocator_memory_log` first. It covers no member of this family and this family covers no
  member of it; together they are the two halves of one library's presence in the image.
- [`static-initialisers-and-teardowns.md`](../Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md) -
  documents the Control Flow Guard dispatch stub that sits beside this family in the image and gets
  swept up with it by anyone reading the address range rather than the bodies. **Deliberately not
  cited by address here:** it has 2,479 callers, and a page inherits the caller set of every address
  it cites — naming it would have raised fourteen unaccounted-neighbour findings on this page,
  every one of them through that one stub and none of them through a member of this family.
- [`font-data-kerning-and-expansion.md`](../../16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md) -
  the consumer whose insert cluster is built on these six, and which supplies the `node+0x20` key
  position this page does not measure.
- [`_types/types.tsv`](../../_types/README.md) - **the node this page describes is now a declared
  type, `EastlRbTreeNodeBase`** (2026-09-20, OPUS): `0x20`, the four offsets §2 reads, and the
  extent taken from the other side - `FUN_00199db0` asks its allocator for `0x28` at `00199E70`,
  takes the payload at `add rax, 0x20` and stores an 8-byte key there, so the header ends where the
  payload begins rather than where an alignment rule would put it. Its sibling
  `MsvcTreeNodeHeader` is the other page's node, and **the two are the same size with the same four
  principal offsets and different meanings at three of them** - the case a shared offset set cannot
  decide, which is why both rows carry the measurement that separates them rather than a
  cross-reference to each other.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**The red-black tree runtime is a service; its callers are clients in every layer.** The members are ~~the hinted~~
~~insert `00199DB0`,~~ `RBTreeIncrement` `0016D6D0`, the erase `0016DA60` and `RBTreeDecrement` `0016D720`. *(Corrected 2026-09-30, SWE2-DATA: `00199DB0` is not a member. It is one of the twenty-four hinted-insert callers (OC-4, §5), calling `RBTreeDecrement` and `RBTreeInsert`. Control `_index/candidates/dd-data-2-0930/crt_rbtree_checks.py` E2.)*
- **Audio, 46:** the sound engine's `002116B0`, `002187D0`, `00218990`, `002199C0`, `00219D80`, `0021AF80` and more.
- **Presentation, 14:** `001ACF80`, `001B5B60`, `001BC190`, `001BD4A0`, `001BD040`.
- **Resource, 8:** `0020B840`, `0020BFA0`, `006761F0`, `00676000`, `0019F490`, `0020B150`.
- **Platform, 4:** `0019CC50`, `001B1960`.

Each keeps its own map; this page owns the tree code.

**UI and Presentation — MECHANICAL, four edges.** `002A9F00` appears here only as the proof that the pointer-table
search finds a real table entry (stored at `009164D0`). Its callers are the text interpreter `002AC5F0`, `002AE610`
and `002B0280`, which are the text-control language's.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 slice OPUS-P22-SLICE-24-99).*
