---
system: MSVC's `std::_Tree` — the second red-black runtime, the one the engine does not use
category: 24-Compiler-And-CRT-Runtime
status: DOCUMENTED — every register row is closed: which container each instantiation is (MT-1, answered 2026-09-26), instantiation C's module (MT-2, answered 2026-09-16), the further _Isnil bodies (MT-3, answered 2026-09-15), the fourteen profiled bodies read (SD-80, answered 2026-09-30); MT-4 (inlining) NOT A QUESTION, carried by a board task. Owner re-status 2026-09-30 (OPUS)
readiness: BEHAVIORALLY UNDERSTOOD (2026-09-30, OPUS) - all twenty-three family bodies are read: nine
  whole by this page and the other fourteen by SD-80 (nine proven instruction-identical to a read
  sibling, five read directly), and every role label in section 3 holds on the read. The node's
  allocation and construction are read too (section 10, _types MsvcTreeNodeHeader). Was, 2026-09-15:
  SEMANTICALLY IDENTIFIED, rated non-bearing because fourteen of the twenty-three bodies were profiled
  rather than read; superseded by SD-80.
owner_layer: CodeDomain:CxxStandardLibrary.OrderedContainerRuntime; no PrimaryOwner
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: found by the `_Isnil` signature, a byte at `+0x19` that EASTL's `rbtree_node_base` has no
    member for; nine bodies disassembled whole and the remaining fourteen profiled by store offset,
    callee set and caller count; instantiations grouped by which rotation pair each erase calls;
    falsification pass 1 in section 9 re-derived the signature counts independently, widened the
    EASTL control to every operand at +0x19, and read a ninth body whole
last_reviewed: 2026-09-30
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-15
  last_pass_state: fable-msvc-tree-pass-1
  crossref_clean: false
  reopened_count: 0
function_families:
  - "MSVC ordered-container (std::_Tree) runtime | C | members/msvc-ordered-container-runtime.tsv | 22 | (2026-09-30, OPUS: 00714B00 left the row - it is measured A; the other 22 stay C) not this game's code and not the engine's container runtime either: Microsoft's std::_Tree, emitted into separately compiled modules that link into this image beside the engine's EASTL. IDENTIFIED BY A MEMBER EASTL DOES NOT HAVE: every body tests a byte at +0x19, which is MSVC's _Isnil; EASTL's rbtree_node_base is {mpNodeRight +0, mpNodeLeft +8, mpNodeParent +0x10, mColor +0x18} and ends at +0x19. CONFIRMED BY WHERE THE PARENT IS: across a mirror rotation pair the invariant store offset is the parent, and it is +0x08 here against +0x10 in the EASTL family - _Parent against mpNodeParent. THE BOUNDARY: 23 bodies, 6,630 bytes, EVERY ONE UNNAMED. ~~NOT dispositioned: which container each of the three instantiations is, and the 22 further bodies that carry the _Isnil test without a family shape.~~ Dispositioned since (corrected 2026-09-30, SWE2-DATA) - MT-1 names the three containers and MT-3 classes the 23 further _Isnil bodies as non-members; the fourteen profiled bodies are SD-80."
---

# MSVC's `std::_Tree` — the second red-black runtime

> **This image contains two red-black tree implementations, from two toolchains, and the
> engine uses the other one.**
>
> [`the-ordered-container-runtime.md`](the-ordered-container-runtime.md) documents EASTL's
> `rbtree`: six bodies, 1,741 bytes, 99 callers across audio, text, effects and resource loading.
> This page documents the other twenty-three. They are Microsoft's, they came in with separately
> compiled modules, and **not one of them is named**.

## 1. What the player sees

Nothing, twice over. This is a toolchain's own code, like its EASTL counterpart — and unlike that
one it is not even the toolchain the game was built with for its own containers. It arrived inside
modules that were compiled elsewhere and linked in.

What it does mean for a reader is that **"the red-black tree in this image" is not a thing**. There
are two, they have different node layouts, and a page that cites one while describing the other
would be wrong in a way no call-graph check could catch.

## 2. Native mechanism

**The node, and the member that gives the library away.**

| offset | width | MSVC name | EASTL's `rbtree_node_base` |
|---|---|---|---|
| `+0x00` | 8 | `_Left` | `mpNodeRight` |
| `+0x08` | 8 | `_Parent` | `mpNodeLeft` |
| `+0x10` | 8 | `_Right` | `mpNodeParent` |
| `+0x18` | 1 | `_Color` | `mColor` |
| `+0x19` | 1 | **`_Isnil`** | **no such member** |
| `+0x20` | — | `_Myval` | `rbtree_node<Value>::mValue` |

**And for the `0x30` instantiation the payload is resolved further:** `0070D360`, a `lower_bound`
descent, compares a key at `node+0x20` and returns `[node + 0x28]`. Key `+0x20`, mapped value
`+0x28`, header `0x20` — `0x30`, which is what `00712F60`'s `max_size` guard says independently.
See `MT-3`.

**`+0x19` is the identification.** Every body in this family tests it, as
`cmp byte ptr [reg + 0x19], 0`. **The six EASTL bodies do not touch `+0x19` at all** — not that
one instruction shape, but **any memory operand at that displacement, any mnemonic, any width:
zero, across all six bodies and 521 instructions** (§9 widened the control from the test to the
offset, because a control about one instruction shape is narrower than the claim it supports).
Same operation, same node size, opposite result.

**And the parent pointer confirms it from the other direction, without reference to any header.**
A rotation exchanges two children and reparents three nodes, so **across a mirror pair the
invariant store offset is the parent**. In this family it is `+0x08` — `00714B00` writes
`+0x00`×2, `+0x08`×6, `+0x10`×4 and `0071F240` writes `+0x00`×4, `+0x08`×6, `+0x10`×2. In the
EASTL family it is `+0x10`. `_Parent` against `mpNodeParent`, measured rather than looked up.

**The payload begins at `+0x20` here too, and a destructor says so.** `0071F3A0`, clearing its
tree, does `lea rcx, [rsi + 0x20]` / `call 0071EE70` on each node **before** freeing it — it
destroys the value at `+0x20`. That is the same payload position the EASTL family's callers use,
which is unsurprising for a `0x19`-byte header rounded to 8, and it is measured on both sides
independently.

**The node size is inside the runtime here, and that is the real difference from EASTL.** The
EASTL family never computes a size — `OC-2` was answered by reading its *callers*. MSVC's insert
carries it as a constant, because `max_size()` is `(size_t)-1 / sizeof(_Node)`:

| insert | the `movabs` guard | `(size_t)-1 / node` | node |
|---|---|---|---|
| `00712F60` | `0x0555555555555554` | `0x0555555555555555` at `0x30` | **`0x30`** |
| `0071E500` | `0x02AAAAAAAAAAAAA9` | `0x02AAAAAAAAAAAAAA` at `0x60` | **`0x60`** |

Both guards are exactly one below the quotient, which is the `cmp size, K / jb ok` form of
`if (size >= max_size) throw`. **Two inserts, two node sizes, each dividing exactly** — so this
runtime states the size the other one leaves to its callers. ~~*Not corroborated by an allocation
site: the callers' allocation shape is not the vtable-dispatched one the EASTL callers use, and I
did not find their size arguments.*~~ *(Corrected 2026-09-30, SWE2-DATA: corroborated at the allocation. The node builders `00714860` and `00714920` call the CRT allocator with `ecx` = `0x30` (`00714872`, `00714932`), and `0071F180` with `0x60` (`0071F192`). Each is reached from a find-or-create path that then calls the matching insert wrapper: the `+0xC8` and `+0xA8` caches for the `0x30` insert `00712F60`, and pair B's owner for the `0x60` insert `0071E500`. Each `max_size` constant is (2^64 − 1) / size − 1 for that size. Control `_index/candidates/dd-data-2-0930/crt_rbtree_checks.py` M1, M2.)*

**What the insert does on overflow is the other MSVC tell.** `00712F60` opens by loading the
size from `[rcx+8]`, comparing it against that constant, and on failure calling `free`, loading a
string address and calling through an import, then `int3` — the `_Xlength_error` path. A body that
ends in `int3` after a throw helper is not EASTL's.

**Everything else is the standard shape**, and the last two instructions of the insert are the same
sentence the EASTL insert ends on: `mov rcx, [rax+8]` / `mov byte ptr [rcx+0x18], 1` — **paint the
root black**.

## 3. Key addresses

All addresses are VAs with image base `0x00120000` already included. **Every one is `FUN_xxxxxxxx`
in the function list; this family has no names to inherit.**

| address | bytes | callers | role | read |
|---|---:|---:|---|---|
| `00714B00` | 89 | 2 | rotation, pair A | **whole** |
| `0071F240` | 85 | 2 | rotation, pair A — the mirror | profile |
| `00799BD0` | 85 | 1 | rotation, pair C | **whole** |
| `00799C30` | 89 | 1 | rotation, pair C — the mirror | **whole** |
| `00712F60` | 679 | 3 | insert + rebalance, node `0x30`; rotations inlined | **whole** |
| `0071E500` | 680 | 2 | insert + rebalance, node `0x60`; destroys the payload **only on the throw path** | **whole** |
| `00714DC0` | 840 | 5 | erase node + rebalance, pair A | **whole** |
| `0071F590` | 978 | 1 | erase node + rebalance, pair A | profile |
| `0079BA10` | 978 | 1 | erase node + rebalance, pair C | profile |
| `00714B60` · `00714BE0` · `00714C60` | 126 each | 2 each | `_Tidy` — walk, free every node, reset the head's three links, size `= 0` | **`00714B60` whole** |
| `0071F3A0` | 136 | 1 | `_Tidy`, and the one that destroys the payload at `+0x20` first | **whole** |
| `0079B0D0` | 126 | 1 | `_Tidy` | profile |
| `00714980` · `0071F1E0` · `00799B80` | 80 · 89 · 80 | 4 · 1 · 1 | destroy-subtree recursion, called by the tidies | profile |
| `0071EE70` | 148 | 8 | the payload destructor pair B and its tidy call | profile |
| `00714CE0` · `00715110` · `007151F0` · `0071F4B0` · `0079B930` | 218 each | 2 · 2 · 2 · 2 · 1 | erase-range: whole-range goes to the tidy, otherwise loop the node erase | **`0079B930` whole** |

**23 bodies, 6,630 bytes.** Nine read whole, fourteen profiled by store offset, callee set and
caller count. *(2026-09-30, OPUS: the fourteen are read since, by SD-80
([record](../../_index/candidates/sd80-82-ordered-containers-0930/README.md)): nine are instruction-identical to a
read sibling of their own instantiation and five were read directly, and every role above holds. The read also
names the pair A / B rotations' directions: `0071F240` is the left rotation and `00714B00` the right one.)*

## 4. Data structures and formulas

The node header is the table in §2. The only arithmetic in the family is the two `max_size`
constants, and they are the node sizes. No member reads an immediate that encodes a game value.

## 5. Call chain

**Three instantiations, grouped by which rotation pair each erase calls — not by address, and not
by guess.**

| | rotations | erase node | tidy | destroy subtree | erase range |
|---|---|---|---|---|---|
| **A** | `00714B00` / `0071F240` | `00714DC0` | `00714B60`, `00714BE0`, `00714C60` | `00714980` | `00714CE0`, `00715110`, `007151F0` |
| **B** | `00714B00` / `0071F240` *(shared with A)* | `0071F590` | `0071F3A0` | `0071F1E0` | `0071F4B0` |
| **C** | `00799BD0` / `00799C30` | `0079BA10` | `0079B0D0` | `00799B80` | `0079B930` |

**The internal wiring is exact and it is what makes the grouping a measurement.** Each erase-range
body calls **one** tidy and **one** erase-node, each tidy calls **one** destroy-subtree, and each
erase-node calls **one** rotation pair. Nothing crosses a column except A and B sharing the
rotation pair, which is the compiler emitting one rotation for two instantiations of the same
node layout — exactly the relationship the EASTL page describes in the other direction, where one
insert inlined its rotations and the erase did not.

**A has three tidies against one erase.** A `_Tidy` is emitted per value type because it destroys
values; an erase-node is emitted per *node layout*. Three tidies on one erase is therefore three
containers with the same node shape and different payloads — which is a reading, not a
measurement, and is offered as one.

**Where they live.** All of A and B, and every one of the ~~22~~ 23 *(corrected 2026-09-30, SWE2-DATA: MT-3)* further `_Isnil`-carrying bodies
outside this family, fall inside the **YEBIS/PPFX span** `006DA880`–`007911E0` declared by
[`yebis-ppfx-source-map.md`](../../23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md).
**C does not** — `0079B930` and `0079BA10` sit past the span's end, inside the **PhyreEngine
`PFramework`** platform layer: the tree they erase is the static `std::_Tree` at `02EA5550`,
constructed and atexit-registered by `00169270`/`008B7940`, beside `PClassDescriptorForType<
PFramework::*>` statics and the `PhyreFrameworkClass` window creation (see §7, MT-2).

## 6. Modding notes

**Do not confuse the two families when hooking.** A detour written against `mpNodeParent +0x10`
will corrupt a tree of this family on its first rotation, because `+0x10` is a child here. The
`+0x19` byte is the cheapest way to tell at a glance which tree a pointer belongs to: EASTL's
nodes have nothing there.

**XIIOnline:** nothing here carries gameplay state. It is below the layer where the game exists,
and further below it than the EASTL family, because the engine does not use it at all.

## 7. What is not known

- [x] **Which container each of the three instantiations is.** The grouping is structural — who
      calls whose rotations — and no value type is identified. **MT-1.**
      ***NARROWED 2026-09-17 (FABLE): A is three maps owned by one YEBIS object and B is a map that lives on one routine's stack; the value types are still unnamed.** *A.* Each of the three erase-range bodies has two callers: its own 41-byte clear wrapper (`007136D0`, `00713700`, `00713730`) and `006FF840` (172 B), which clears the three maps in turn at the object's `+0xC8`, `+0xB8` and `+0xA8` and frees each header through `00210EB0` (`006FF85F`..`006FF8E7`); the three tidies are also run from the 23,568-byte `006FF900`, ~~the object's teardown~~ *(corrected 2026-09-26 (FABLE, Claude Opus 5.5): it is the block's
      initialiser, `CPostEffect::Initialize` by its own diagnostic strings, as the post-processing catalogue
      already names it. The allocating routine calls it on the freshly constructed block and sign-tests its status,
      and it creates the GPU device the maps use; see the answer below)*. `006FF840` is reached from `006DAFB0`, `006DE780` and `006DEB40`, and `006FF900` from `006DAA70` and `006DE950`, all inside the YEBIS span. The `lower_bound` `0070D360` compares an unsigned 64-bit key at `node+0x20` (`0070D380`, `0070D39E`, both `jae`) and returns the qword at `+0x28`, so the three are maps from a 64-bit key (a pointer or a hash) to a pointer-sized value; the erase-node `00714DC0` is also reached from `0070E520` and `0070E600`, two erase-by-key bodies with no listed caller. *B.* Its one erase-range `0071F4B0` is called from `0071D170` (2,140 B, called from `0071CD10`) on a header at `[rsp+0x20]`, right before the routine sets its `0x8000FFFF` failure code (`0071D974`..`0071D98B`), and from `0071EE40`, which is called only from the unwind entry `008A2FEC`: a function-local map destroyed on both the normal and the exceptional exit. What the keys index and what the values are is not read; that needs the inserters, which this page does not list. Static.*
      *Narrowed 2026-09-18 (FABLE): the owner is named, and the `+0xC8` map is read as a render-texture cache.* **The “one YEBIS object” is not a class instance but YEBIS's global state block**: `0xD40` bytes with **no vtable**, allocated through `006DA880` with the source tag `..\src\ppfx.cpp` (line `0x1C2B` at `006DE9C8`–`006DE9E1` in `006DE950`, line `0x332` at `006DAB84`–`006DAB9D` in `006DAA70`), constructed by `006FF5D0` (608 B: a flag byte at `+0`, pointers zeroed to `+0x90`, then the three map headers made at `+0xA8` by `00714800` (`006FF62D`–`006FF648`), `+0xB8` by `007147A0` (`006FF64B`–`006FF661`) and `+0xC8` by `00714740` (`006FF669`–`006FF67F`)), and stored at `02EA0B70` (`006DE9FB`, `006DABB9`); `006DE780` is the shutdown, which clears the three maps through `006FF840` on the block it finds there and zeroes `02EA0B70`, `02EA0B78` and `02EA0B80` (`006DE805`, `006DE81F`, `006DE8D4`). The RTTI `IPfxBaseContext` vtable `00D8F8E8` that `006DE780` references belongs to a different object; the block itself has none. Some sixty YEBIS entry points (`006DB4C0` .. `006DF440`) load `[02EA0B70]` as their first act, so the block is the current PPFX context every API call implicitly takes. **The `+0xC8` map is a find-or-create cache of `PPFX::CRenderTexture` keyed by a pointer.** `0070D360` walks the `+0xC8` tree for the 64-bit key in `rdx` (`0070D366`–`0070D3A7`); a hit yields the node's `+0x28` value, a miss or a null value calls `006F1F60(block, key, …, &out)` (`0070D3BC`–`0070D3D6`), whose callee `00720FB0` installs the `PPFX::CRenderTexture` vtable, and either way the value is latched at the block's `+0x60` with a caller dword at `+0x68` (`0070D3E4`–`0070D3ED`) — the “current” render texture. The only static route to that lookup is `006CBEA0` (485 B, `Phyre.Middleware`) → `006DD5F0` (`006CBF2E`), which takes the key from the first element's `+0x10` of a Phyre pointer array at the source object's `+0x38` (count at `+0x30`, `006CBEDD`–`006CBF04`) and passes that object's dwords `+0x90`, `+0x94` and `+0xA0` — the shape of a width, height and format — so the key is the Phyre-side texture handle and the cache maps it to YEBIS's wrapper. The `+0xA8` and `+0xB8` maps' inserters and value types are not read; the sibling `006DD660` wrapper has no listed caller. Static: the allocation sites, the constructor, the lookup and its caller.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): A is three resource-wrapper caches, B is the parsed licence, and C is a
      container the shipped code never uses.** Control: [`mt1_container_values.py`](../../_index/candidates/mt1-container-values/mt1_container_values.py) (11 checks, FAILS 0). First read by a delegated
      read-only pass; every cited instruction re-checked.
      - **A: three `map<u64, wrapper*>` find-or-create caches over the PPFX GPU device.** Each lookup's miss path
        calls one of the device's "Ref" creators, then inserts the result. The device sits at the block's `+0x20`
        (the block is the `CPostEffect` object, per `_types`) and is a `PPFX::IGPUDevice` by the RTTI of the vtable its constructor installs. The three creators
        are the slots whose log tags read `Ref2D`, `Ref3D` and `RefRT`:
        - `+0xA8` holds `IGPUSurface*` from slot 66, `RefRT`. It caches a referenced render target, and a hit
          becomes the current target at `+0xD8`.
        - `+0xB8` holds `IGPUVolumeTexture*` from slot 62, `Ref3D`. The current one is kept at `+0xF0`.
        - `+0xC8` is the slot-60 `Ref2D` cache read above, whose `IGPUTexture` becomes the `CRenderTexture`.
        - The class of each value comes from the RTTI of the vtable its constructor chain installs.
        - The `+0xB8` map's API wrapper has no static reference of any kind: no call, no jump, no VA and no RVA.
          So nothing in this build fills that cache from outside.
      - **B: `map<std::string, std::string>`, the parsed YEBIS licence.** Its one owner looks up `FeatureId`,
        `BeginYear`, `BeginMonth`, `BeginDay`, `EndYear`, `EndMonth`, `EndDay`, `MacAddress` and `License` by
        name, and tests each result as an MSVC string. The payload destructor `0071EE70` frees two strings, at
        `+0x20` and `+0x00`. `0x20` header + `0x20` key + `0x20` value is the `0x60` node.
      - **C: an 8-byte element, and no use to read its type from.** The static constructor allocates the head
        with `0x28` bytes, the `0x20` header plus 8. The tidy frees nodes without destroying anything.
        Image-wide, only the static constructor and its atexit destructor address the tree, and the family's
        rotations and erase are reached only from that destructor. Control: the same sweep finds hundreds of sites
        for the YEBIS state block's global. So the shipped game builds C, never fills or searches it, and frees it
        at exit. Its element type is not recoverable from use, because there is none.
- [x] ~~**Which module instantiation C belongs to.**~~ **ANSWERED 2026-09-16 (SWE2-EC7) —
      PhyreEngine's `PFramework` layer, a linked middleware module, not engine code.** **MT-2.**
      The teardown `008B7940` erases a **static `std::_Tree` at `.data 02EA5550`** and is the
      atexit-registered destructor half of a constructor pair: static-initializer `00169270`
      constructs the container, stores it at `02EA5550`, and registers `008B7940` through the
      `00808B90` atexit wrapper. The attribution does not rest on the
      teardown's own bytes — it rests on the object's neighbours. The teardown stubs immediately
      following `008B7940` install vtables into `02EA5380`, `02EA5560`, `02EA5660` and `02EA9400`
      whose RTTI complete-object locators decode as
      **`Phyre::PClassDescriptorForType<Phyre::PFramework::{VPApplication, VPApplicationViewport,
      VPDebugUtils, VPInputMapper}>`** — Phyre's reflection descriptors for the framework classes,
      in the same `.data` block, tail-calling `00633390` (the shared `PClassDescriptorForType`
      base destructor already recorded in
      [`class-descriptor-and-metadata-system.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)).
      The code region agrees: `0079B300` registers and creates the **`PhyreFrameworkClass`**
      Win32 window (class name at `01CB3390`; `GetSystemMetrics` virtual-screen metrics,
      `AdjustWindowRectEx`, `CreateWindowExW`, `WM_SETICON`), and `0079C140` is already
      identified as `PApplication` slot 28, the framework's per-frame update
      ([`the-game-is-a-phyre-application.md`](../../22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md)).
      So instantiation C is a `PFramework` static container — a sorted registry owned by the
      framework layer — and its MSVC-STL compilation is exactly what the fingerprint predicts of
      separately compiled middleware: Phyre's object files were built against MSVC's STL, not
      EASTL. *What is still not named is the tree's key/value types — that is MT-1's question,
      not this one's.* *(MT-1, 2026-09-26 (FABLE, Claude Opus 5.5): one 8-byte, trivially destroyed element per node, and the
      shipped code never fills or searches the tree, so no use names the type; see the box above.)*
      *Correction history kept: the two retracted readings (input-backend adjacency, the
      `0016D6A0` fold-stub as "three EASTL objects") were wrong in the way recorded above —
      adjacency and a callee list are not evidence; the RTTI names, the window class string and
      the static-init pairing are.*
- [x] ~~**The 22 further bodies that carry the `_Isnil` test** — 45 in the image, 23 accounted for
      here.~~ **ANSWERED 2026-09-15 (FABLE) — there are **23** of them, not 22, and they are
      container-level operations, not further runtime members.** **MT-3.**
      *The split was wrong by one in both directions: **`0071EE70`, the payload destructor, carries
      no `_Isnil` test at all**, so 45 carriers is **22 members + 23 non-members**, not 23 + 22.
      Classified by shape and two read whole. **Insert wrappers:** `00713210`, `00713370` and
      `007134D0` — 351 bytes each, nine tests each, each calling the `0x30` insert `00712F60`
      **twice**; and `0071EA80` / `0071E7B0` for the `0x60` insert. `00713210` read whole: it takes
      the head at `[rcx]`, the root at `[r11+8]`, descends on `cmp byte [rax+0x19], 0`, and orders
      with `cmp [rax+0x20], rdx` / `setae` against a direction flag — a `lower_bound` with a hint,
      which is the MSVC analogue of the EASTL family's twenty-four `dec`+`ins` callers.
      **`lower_bound` / `find` descents:** the `0070Dxxx` cluster, ten bodies of 144–309 bytes with
      two tests each and no call into the family. **Consumers:** `00705520` (4,375 B),
      `0071D170` (2,140 B), `0070E600`, `0070E520`. None of them is a runtime member — they **use**
      the node layout rather than implement it.*
      *And they close the node size from a third direction. `0070D360` read whole is the canonical
      descent — `cmp [r11+0x20], rdx` / `jae` → left at `[r11]`, else remember and go right at
      `[r11+0x10]`, terminating on `_Isnil` — and it ends `mov rcx, [rax + 0x28]`, **reading the
      mapped value at `node+0x28`**. Key at `+0x20`, value at `+0x28`, header `0x20`: `0x30`, which
      is exactly what `00712F60`'s `max_size` constant says. **Three independent lines, one node.***
- [x] **How much MSVC tree code is inlined**, which no census on this page can see: every one of
      them counts call edges, and an inlined rotation has none. The same limit applies to the EASTL
      page and is recorded there. **MT-4.**
      *NOT A QUESTION 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-2 ruling: the work is carried by the board task `FABLE-CARRIER-TOOLING-AND-CHECKER-PROPOSALS-0926`.*
- [x] **What the fourteen profiled bodies do, read end to end.** `0071F240`, `0071F590`, `0079BA10`, `00714BE0`, `00714C60`, `0079B0D0`, `00714980`, `0071F1E0`, `00799B80`, `0071EE70`, `00714CE0`, `00715110`, `007151F0` and `0071F4B0` are carried on store offsets, callee sets and caller counts (§3), not on a read; each has a read sibling of the same role. **SD-80** (SWE2-DATA, 2026-09-30). *(SD-80 answered 2026-09-30 by OPUS `6836e8067`, [record](../../_index/candidates/sd80-82-ordered-containers-0930/README.md).)*

## 8. Evidence

Read from the shipping EXE, authority hash
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base `0x00120000`.

**The signature, and its control.** `cmp byte ptr [reg + 0x19], 0` on a non-stack base fires in
**45 bodies** image-wide, **221 tests**, distributed by 1 MB band as `{0x06: 1, 0x07: 44}` — one
band. The control that makes that meaningful is the EASTL family: `0016D6D0`–`0016DA60`, the same
operation on the same node size, scores **zero** across 521 instructions.

**The parent-offset contrast.** Measured on the rotation bodies of both families rather than taken
from headers: `+0x08` invariant across this family's mirror pairs, `+0x10` across EASTL's.

**The span cross-reference.** 22 of the 24 densest `_Isnil` carriers fall inside the declared
YEBIS/PPFX span, which is a corroboration of that span rather than a correction to it. The two that
do not are `0079B930` and `0079BA10`.

**The internal wiring** in §5 is a complete accounting: every erase-range's two callees, every
tidy's one, every erase-node's rotation pair. No member calls outside the family except to `free`
and to `0071EE70`.

**What is deliberately not cited by address:** the image's `free`. It has **242 callers**, and a
page inherits the caller set of every address it cites — the same reason
[`the-ordered-container-runtime.md`](the-ordered-container-runtime.md) does not cite the guard
stub.

## 9. Falsification pass 1 — 2026-09-15 (FABLE, the producer's)

Run against the shipping image before the page's first commit was a day old. **Three attacks
failed to dent it and one landed — on a key-address note, not on a conclusion.**

### The attack that landed

**`0071E500` destroys a payload only on the THROW path, and the key-address table implied
otherwise.** It was the one insert carried on a profile rather than a read, and the profile showed a
call to the payload destructor `0071EE70`, which I recorded as *"also destroys a payload"* — a
sentence a reader would take as normal-path behaviour. Read whole, the call is inside the
length-error branch:

```asm
0071E506  mov    rax, [rcx + 8]              ; size
0071E50D  movabs rcx, 0x2AAAAAAAAAAAAA9      ; max_size for a 0x60 node
0071E51A  cmp    rax, rcx
0071E51D  jb     0071E543                    ; ... the normal path
0071E51F  mov    rbx, [rsp + 0x58]           ; otherwise: the node just built
0071E524  lea    rcx, [rbx + 0x20]
0071E528  call   0071EE70                    ; destroy its payload
0071E52D  mov    rcx, rbx
0071E530  call   <free>                      ; free the node
0071E535  lea    rcx, <string>
0071E53C  call   qword ptr [rip + 0x1A40D6]  ; throw
0071E542  int3
```

That is the strong-exception-guarantee cleanup, not a container operation. **Corrected in the table,
and the body is now one of nine read whole rather than fourteen profiled.**

**It also strengthens the payload claim rather than weakening it.** §2 gets `+0x20` from `0071F3A0`,
a `_Tidy`. Here is a second, independent site — an *insert*, cleaning up after itself — doing
`lea rcx, [rbx + 0x20]` on a node it built moments earlier. Two members, two different operations,
same payload offset.

### The three that failed

| attack | result |
|---|---|
| **Does the EASTL family touch `+0x19` in *any* form?** §2's control is about one instruction shape (`cmp byte ptr [reg+0x19], 0`), which is narrower than the claim it supports. Widened to **every memory operand at `+0x19`, any mnemonic, any width** | **Zero. Across all six bodies.** The discriminator survives the wider test, so the page may say the member is absent rather than that one test is |
| **Is there a rotation pair I missed?** The three instantiations rest on finding *all* the rotations; a fourth pair would mean a fourth instantiation | Re-ran the rotation shape — no calls, ≥ 8 qword stores, writes confined to `+0x00`/`+0x08`/`+0x10` — **restricted to `_Isnil` carriers**. **Exactly four bodies, and they are the two pairs §5 names.** No fourth pair |
| **Do the census numbers reproduce?** `45` bodies, `221` tests, `{0x06: 1, 0x07: 44}` were measured once and quoted three times | Re-counted from scratch: **45 / 221 / `{0x06: 1, 0x07: 44}`**, exact |

### What this pass did not attack

The **node-size inference**, which is still one instrument: `max_size()` divides exactly at `0x30`
and `0x60`, and no allocation site corroborates it — §2 already says so and the pass did not improve
it. *(Corroborated since, 2026-09-30: the node allocators ask for `0x30` and `0x60`; see §2's correction and
§10.)* The **instantiation grouping's meaning**: the wiring is measured, but *which container* each of
A, B and C is remains `MT-1`, and the three-tidies-on-one-erase reading remains a reading. And
**`MT-4`, inlining**, which no census on this page can reach, for the reason the EASTL page's own
pass records.

## 10. Related

- [`the-ordered-container-runtime.md`](the-ordered-container-runtime.md) — EASTL's `rbtree`, the
  one the engine actually uses. The two pages are the two halves of one fact: **this image links
  two standard libraries' ordered containers**, and which one a body belongs to is readable in a
  single byte.
- [`yebis-ppfx-source-map.md`](../../23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md)
  — the span that contains instantiations A and B.
- [`third-party-middleware-inventory.md`](../../23-Third-Party-Libraries/third-party-middleware-inventory.md)
  — the inventory this family's existence bears on; instantiation C is outside every span it
  declares.
- [`_types/types.tsv`](../../_types/README.md) — **the node header in §2 is now a declared type,
  `MsvcTreeNodeHeader`** (2026-09-20, OPUS), beside EASTL's `EastlRbTreeNodeBase`. The store rows
  add one line §2 does not have: the parent at `+0x08` is carried by **three** independent
  measurements rather than the mirror-pair invariant alone — that invariant on *both* pairs
  (`+0x08` written 6 times each way in `00714B00`/`0071F240` and again in `00799BD0`/`00799C30`),
  the insert's own parent store `00712FA3 mov [r11+8], r9` on the node it received as its fifth
  argument, and the descent `0070D360`, which climbs no parent at all and so cannot contradict it.
  ~~The `allocation_site` cell is `UNRESOLVED` and names the same gap this page records: the release
  is read (`0071F3A0` → `0071EE70` on `+0x20`, then the image's `free` on the node — **named there
  and, like §8, deliberately not cited by address here**), the acquisition is not, and the
  `max_size` constant is a size rather than a site.~~ *(Resolved 2026-09-30, OPUS, on SWE2-DATA's M1/M2:
  the node comes from MSVC's `_Buynode0`, one per node size (`00714860` and `00714920` ask for `0x30`,
  `0071F180` for `0x60`, through the image's `malloc` wrapper, and point all three links at the head). Its
  callers, the `_Buynode` bodies `00712E60`, `00712F20` and `0071E340`, zero the colour and `_Isnil` bytes in one
  word store at `+0x18` and build the value at `+0x20` before the insert links the node. Control
  [`dd_crt_check.py`](../../_index/candidates/opus-dd-crt-0930/dd_crt_check.py) A1-A3.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Input and Platform — MECHANICAL, four edges.** The container users cited here are input-system bodies:
- `0079C140` calls `0079D010` / `0079D920`;
- `0079B300` is called from `0079E520` and calls the platform's `FindResourceW` loop `0019A510`.

The container code is this page's; the input device registry is `input-stack-device-channel-and-bindings`'.

*Tier 2: ledger names, sizes and `edges.tsv`; no new body read (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
