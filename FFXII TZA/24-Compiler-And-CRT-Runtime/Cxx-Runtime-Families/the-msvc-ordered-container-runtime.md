---
system: MSVC's `std::_Tree` — the second red-black runtime, the one the engine does not use
category: 24-Compiler-And-CRT-Runtime
status: AUDITED — every register row is closed: which container each instantiation is (MT-1, answered 2026-09-26), instantiation C's module (MT-2, answered 2026-09-16), the further _Isnil bodies (MT-3, answered 2026-09-15), the fourteen profiled bodies read (SD-80, answered 2026-09-30); MT-4 (inlining) NOT A QUESTION, carried by a board task. Owner re-status 2026-09-30 (OPUS)
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
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record fable-msvc-tree-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
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

**`+0x19` is the identification.** Every body in this family ~~tests it~~ but the payload destructor `0071EE70` tests it *(corrected 2026-10-02, OPUS: `0071EE70` frees two string buffers through `001DFA10` and never reads `+0x19`; MT-3's answer)*, as
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
A, B and C is ~~remains `MT-1`~~ was `MT-1` *(answered: see MT-1, ANSWERED 2026-09-26; 2026-10-02, OPUS)*, and the three-tidies-on-one-erase reading remains a reading. And
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

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-msvc-ordered-container-runtime-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00169270` | 67 B | passes `02EA5550` through a 4-byte identity helper (it returns its argument), zeroes the qwords `02EA5550` and `02EA5558`, calls `00799B20(02EA5550)` and stores its result to qword `02EA5550`, then tail-jumps to `00808B90` with the address `008B7940` | `00169274`, `00169289`, `00169297`, `001692A3`, `001692AE` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-msvc-ordered-container-runtime-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0070E520` | 210 B | when byte `[rcx]` is non-zero it returns `0x80004005`, first calling `006DF480(00D95EA8, 0x72bb)` and `006DF480(00D95EF0)` (with `edx` as the first call left it) when dwords `01F3BA80` and `01F3BA90` are both non-zero; otherwise it searches the tree with head qword `[rcx+0xa8]` for the first node whose qword key `+0x20` is not below `rdx` (descending from the head's `+8` through `+0x10` or `+0`, nodes with byte `+0x19` set ending the walk) and returns `0x80070057` when that is the head or its key is above `rdx`; for a found node it calls the vtable slot `+8` of the non-null object qword `+0x28`, calls `00714DC0(rcx+0xa8, rsp+0x30, node)` and returns 0 | `0070E547`, `0070E583`, `0070E5A0`, `0070E5CE`, `0070E5DC` |
| `00714CE0` | 218 B | erases tree nodes from `r8` up to `r9` for the tree whose head node is qword `[rcx]`: when `r8` equals the head's qword `+0` and `r9` is the head itself it calls `00714B60` with the incoming registers and stores the head's qword `+0` to `[rdx]`; otherwise, until the current node equals `r9`, it records the in-order successor (the leftmost node, through qword `+0` links, of the qword `+0x10` subtree, or else the first ancestor reached through qword `+8` links that the node is not the `+0x10` child of, a node whose byte `+0x19` is non-zero ending each walk and leaving the recorded node unchanged when the current node has that byte set), calls `00714DC0(rcx, rsp+0x30, node)` and continues from the recorded node, finally storing it to `[rdx]`; it returns `rdx` | `00714CFD`, `00714D07`, `00714D30`, `00714D98`, `00714DB1` |
| `00715110` | 218 B | erases tree nodes from `r8` up to `r9` for the tree whose head node is qword `[rcx]`: when `r8` equals the head's qword `+0` and `r9` is the head itself it calls `00714BE0` with the incoming registers and stores the head's qword `+0` to `[rdx]`; otherwise, until the current node equals `r9`, it records the in-order successor (the leftmost node, through qword `+0` links, of the qword `+0x10` subtree, or else the first ancestor reached through qword `+8` links that the node is not the `+0x10` child of, a node whose byte `+0x19` is non-zero ending each walk and leaving the recorded node unchanged when the current node has that byte set), calls `00714DC0(rcx, rsp+0x30, node)` and continues from the recorded node, finally storing it to `[rdx]`; it returns `rdx` | `0071512D`, `00715137`, `00715160`, `007151C8`, `007151E1` |
| `007151F0` | 218 B | erases tree nodes from `r8` up to `r9` for the tree whose head node is qword `[rcx]`: when `r8` equals the head's qword `+0` and `r9` is the head itself it calls `00714C60` with the incoming registers and stores the head's qword `+0` to `[rdx]`; otherwise, until the current node equals `r9`, it records the in-order successor (the leftmost node, through qword `+0` links, of the qword `+0x10` subtree, or else the first ancestor reached through qword `+8` links that the node is not the `+0x10` child of, a node whose byte `+0x19` is non-zero ending each walk and leaving the recorded node unchanged when the current node has that byte set), calls `00714DC0(rcx, rsp+0x30, node)` and continues from the recorded node, finally storing it to `[rdx]`; it returns `rdx` | `0071520D`, `00715217`, `00715240`, `007152A8`, `007152C1` |
| `0071CD10` | 236 B | builds a local block at `rsp+0x30` (16 bytes copied from `00D9B600`, dwords 1 at `rsp+0x40` and `rsp+0x44`, and three empty strings with capacity 0xf, length 0 and a zero first byte at `rsp+0x48`, `rsp+0x68` and `rsp+0x88`), zeroes qwords `[rcx+0x50]` and `[rcx+0x48]`, calls `0071D170(rcx, rsp+0x30)` and, when that returns 0, `0071D9E0(rcx, rsp+0x30)`, and when both return 0 copies the local dwords `rsp+0x3c`, `rsp+0x40` and `rsp+0x44` to dwords `[rcx+0x4c]`, `[rcx+0x50]` and `[rcx+0x54]`; it then calls `0071EF10(rsp+0x30)` and returns the first non-zero result or 0; the stack cookie is checked through `00808C40` | `0071CD3D`, `0071CD9C`, `0071CDAD`, `0071CDBA`, `0071CDD4` |
| `0071E340` | 151 B | calls `0071F180` with the incoming registers, zeroes word `+0x18` of the returned block `p`, and unless `p+0x20` is null initialises a string at `p+0x20` as empty (capacity qword `+0x18` = 0xf, length `+0x10` = 0, zero first byte), calls `001A4C90(p+0x20)` with `rdx` = qword `[r8]` of the incoming `r8`, and initialises a second empty string the same way at `p+0x40`; it returns `p` | `0071E360`, `0071E36D`, `0071E37C`, `0071E3A2`, `0071E3AB` |
| `0071EE70` | 148 B | for the string at `rcx+0x20` and then the string at `rcx`, calls `001DFA10(string, its qword +0, capacity+1)` when its capacity qword `+0x18` is 0x10 or more, then sets the capacity to 0xf, the length qword `+0x10` to 0 and the first byte of the inline buffer to 0 | `0071EE85`, `0071EE94`, `0071EEB3`, `0071EEC9`, `0071EEF6` |
| `0071F3A0` | 136 B | starting at the root qword `+8` of the head node qword `[rcx]`, and while the current node's byte `+0x19` is zero, calls `0071F1E0(rcx, node's qword +0x10)`, takes the next node from qword `+0`, calls `0071EE70(node+0x20)` and `00210EB0(node)`; it then points the head's qwords `+8`, `+0` and `+0x10` back at the head and zeroes qword `[rcx+8]` | `0071F3C6`, `0071F3D7`, `0071F3E4`, `0071F3ED`, `0071F410` |
| `0071F4B0` | 218 B | erases tree nodes from `r8` up to `r9` for the tree whose head node is qword `[rcx]`: when `r8` equals the head's qword `+0` and `r9` is the head itself it calls `0071F3A0` with the incoming registers and stores the head's qword `+0` to `[rdx]`; otherwise, until the current node equals `r9`, it records the in-order successor (the leftmost node, through qword `+0` links, of the qword `+0x10` subtree, or else the first ancestor reached through qword `+8` links that the node is not the `+0x10` child of, a node whose byte `+0x19` is non-zero ending each walk and leaving the recorded node unchanged when the current node has that byte set), calls `0071F590(rcx, rsp+0x30, node)` and continues from the recorded node, finally storing it to `[rdx]`; it returns `rdx` | `0071F4CD`, `0071F4D7`, `0071F500`, `0071F568`, `0071F581` |
| `0079B930` | 218 B | erases tree nodes from `r8` up to `r9` for the tree whose head node is qword `[rcx]`: when `r8` equals the head's qword `+0` and `r9` is the head itself it calls `0079B0D0` with the incoming registers and stores the head's qword `+0` to `[rdx]`; otherwise, until the current node equals `r9`, it records the in-order successor (the leftmost node, through qword `+0` links, of the qword `+0x10` subtree, or else the first ancestor reached through qword `+8` links that the node is not the `+0x10` child of, a node whose byte `+0x19` is non-zero ending each walk and leaving the recorded node unchanged when the current node has that byte set), calls `0079BA10(rcx, rsp+0x30, node)` and continues from the recorded node, finally storing it to `[rdx]`; it returns `rdx` | `0079B94D`, `0079B957`, `0079B980`, `0079B9E8`, `0079BA01` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-the-msvc-ordered-container-runtime-ee-1003-2)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-msvc-ordered-container-runtime-ee-1003-2/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `006DAFB0` | 497 B | does log(`02EA0B44`: `00D8E70C`, `00D8E718`) and log(`02EA0B40`: `00D8E748` with line 0x43D, `00D8E768`) (writing log(`g`: `x`, `y`) for: when dword `01F3BA80` and dword `g` are at least 1 (unsigned), call `006DF480(x)` and then `006DF480(y)`); when `c` = qword `02EA0B70` is non-null it calls vtable slot `+8` of qwords `02EA0B78` and `02EA0B80` (each when non-null) and stores 0 to them, takes `r` = `00705520(c, 0)`, does log(`01F3BA90`: `00D8E888` with 0x468, `00D8EA40` with `r` and `0071B3C0(r)`) for negative `r` and returns `r`, else does log(`02EA0B40`: `00D8E948` with 0x46C, `00D8EAA0`), calls `006FF840(d)` and `006DA8A0(qword 01F3BA68, d)` for `d` = qword `02EA0B70` when non-null and stores 0 there, and stores 0 to the qword at the pointer `006E0370(rcx)` returns; then does log(`02EA0B40`: `00D8E9C8` with 0x47A, `00D8E7C8`) and log(`02EA0B44`: `00D8E85C`, `00D8E8B8`) and returns 0 | `006DAFD2`, `006DB03B`, `006DB067`, `006DB129`, `006DB154` |
| `006DEB40` | 394 B | does log(`02EA0B40`: `00D8EE30` with line 0x1C56, `00D8EE50`) (writing log(`g`: `x`, `y`) for: when dword `01F3BA80` and dword `g` are at least 1 (unsigned), call `006DF480(x)` and then `006DF480(y)`); when `c` = qword `02EA0B70` is null it does log(`01F3BA8C`: `00D8EE70` with 0x1C5A, `00D8EEA8`) and returns `al` = 1; otherwise `r` = `00705520(c, 0)`, then for negative `r` log(`01F3BA90`: `00D8EED8` with 0x1C62, `00D8EF10` with `r` and `0071B3C0(r)`), else log(`02EA0B40`: `00D8EF60` with 0x1C66, `00D8EF80`); when qword `02EA0B70` is non-null it calls `006FF840` on it and `006DA8A0(qword 01F3BA68, it)`; it then stores 0 to qword `02EA0B70` on both paths and returns `al` = 0 for negative `r`, else does log(`02EA0B40`: `00D8EFC8` with 0x1C71, `00D8EFE8`) and returns `al` = 1 | `006DEB64`, `006DEBD2`, `006DEC02`, `006DEC6A`, `006DEC80` |
| `0070E600` | 337 B | when byte `[rcx]` is non-zero it calls `006DF480(00D965F8, 0x72DC)` and `006DF480(00D96640)` when dwords `01F3BA80` and `01F3BA90` are at least 1 (unsigned) and returns 0x80004005; otherwise it returns 0x80070057 when there is no node of the tree whose head is qword `[rcx+0xB8]` (root at the head's qword `+8`, nil flag byte `+0x19`, key qword `+0x20`, left `+0`, right `+0x10`) whose key equals `rdx`; else, with `v` = that node's qword `+0x28`, `m` = the equal-key node of the tree at qword `[rcx+0xC8]` and `w` = `m`'s qword `+0x28` (0 when absent), it calls `00714DC0(rcx+0xB8, &t, node)`, `00714DC0(rcx+0xC8, &t, m)` when `w` is non-null, vtable slot `+8` of `v` when non-null and `006E1130(w)` when non-null, and returns 0 | `0070E62A`, `0070E660`, `0070E701`, `0070E730`, `0070E740` |
| `00713210` | 351 B | with head `h` = qword `[rcx]` (root qword `[h+8]`, nil flag byte `+0x19`, key qword `+0x20`, left `+0`, right `+0x10`) and key `k` = qword `[r9]`, descends from the root going left when (`r8b` non-zero: node key at least `k`; else: `k` below node key) and right otherwise, keeping the last node `p` (`p` = `h`, counted as left, when the root is nil); when it last went left and `p` is the leftmost node (qword `[h]`) it inserts at once; otherwise, with `q` = the in-order predecessor of `p` when it last went left (qword `[h+0x10]` when `p` is the head) and `q` = `p` when it went right, it inserts when `q`'s key is below `k`; inserting calls `00712F60(rcx, &t, direction, p, r9, fifth argument)` and stores the qword at the pointer it returns and byte 1 to `[rdx]` and `[rdx+8]`; otherwise it calls `00210EB0(fifth argument)` and stores `q` and byte 0 there; returns `rdx` | `00713258`, `007132A6`, `00713337`, `0071334B`, `00713350` |
| `00713370` | 351 B | with head `h` = qword `[rcx]` (root qword `[h+8]`, nil flag byte `+0x19`, key qword `+0x20`, left `+0`, right `+0x10`) and key `k` = qword `[r9]`, descends from the root going left when (`r8b` non-zero: node key at least `k`; else: `k` below node key) and right otherwise, keeping the last node `p` (`p` = `h`, counted as left, when the root is nil); when it last went left and `p` is the leftmost node (qword `[h]`) it inserts at once; otherwise, with `q` = the in-order predecessor of `p` when it last went left (qword `[h+0x10]` when `p` is the head) and `q` = `p` when it went right, it inserts when `q`'s key is below `k`; inserting calls `00712F60(rcx, &t, direction, p, r9, fifth argument)` and stores the qword at the pointer it returns and byte 1 to `[rdx]` and `[rdx+8]`; otherwise it calls `00210EB0(fifth argument)` and stores `q` and byte 0 there; returns `rdx` | `007133B8`, `00713406`, `00713497`, `007134AB`, `007134B0` |
| `007134D0` | 351 B | with head `h` = qword `[rcx]` (root qword `[h+8]`, nil flag byte `+0x19`, key qword `+0x20`, left `+0`, right `+0x10`) and key `k` = qword `[r9]`, descends from the root going left when (`r8b` non-zero: node key at least `k`; else: `k` below node key) and right otherwise, keeping the last node `p` (`p` = `h`, counted as left, when the root is nil); when it last went left and `p` is the leftmost node (qword `[h]`) it inserts at once; otherwise, with `q` = the in-order predecessor of `p` when it last went left (qword `[h+0x10]` when `p` is the head) and `q` = `p` when it went right, it inserts when `q`'s key is below `k`; inserting calls `00712F60(rcx, &t, direction, p, r9, fifth argument)` and stores the qword at the pointer it returns and byte 1 to `[rdx]` and `[rdx+8]`; otherwise it calls `00210EB0(fifth argument)` and stores `q` and byte 0 there; returns `rdx` | `00713518`, `00713566`, `007135F7`, `0071360B`, `00713610` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-the-msvc-ordered-container-runtime-ee-1003-3)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-msvc-ordered-container-runtime-ee-1003-3/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00712F60` | 679 B | with head `h` = qword `[rcx]` and new node `z` = argument 6: when the size qword `[rcx+8]` is at least 0x555555555555554 it calls `00210EB0(z)` and `_Xlength_error('map/set<T> too long')` (IAT `008C2618`); otherwise it adds 1 to the size, stores parent `p` = `r9` to qword `[z+8]` and links `z` as root, leftmost and rightmost (qwords `[h+8]`, `[h]`, `[h+0x10]`) when `p` is `h`, else as `p`'s left (qword `[p]`) when `r8b` is non-zero, replacing `h`'s leftmost when it was `p`, or as `p`'s right (qword `[p+0x10]`), replacing `h`'s rightmost when it was `p`; then the red-black rebalancing after insert (links left `+0`, parent `+8`, right `+0x10`, colour byte `+0x18` with 0 red and 1 black, nil byte `+0x19`): while `z`'s parent is red, a red uncle is recoloured with the parent (both 1) and the grandparent (0) and `z` moves to the grandparent, otherwise an inner `z` is first rotated into the parent's place, then the parent becomes 1, the grandparent 0 and the grandparent is rotated, rotations re-point child parents (non-nil only) and `h`'s root link qword `[h+8]` as needed; finally stores 1 to the colour byte of qword `[h+8]`, `z` to qword `[rdx]` and returns `rdx` | `00712F7A`, `00712F84`, `00712FA3`, `0071301E`, `007131FD` |
| `00714DC0` | 840 B | erases node `z` = `r8` from the tree with head `h` = qword `[rcx]` (links left `+0`, parent `+8`, right `+0x10`, colour byte `+0x18` with 1 black, nil byte `+0x19`): takes `s` = `z`'s in-order successor (`z` itself when nil); when `z` has at most one non-nil child, that child or nil `x` takes `z`'s place under its parent (or as root qword `[h+8]`), `x`'s parent re-pointed when `x` is not nil, and `h`'s leftmost qword `[h]` and rightmost qword `[h+0x10]` reset to `x`'s extreme or `z`'s parent when they were `z`; otherwise, with `x` = `s`'s right, `s` is spliced into `z`'s place (taking `z`'s left and, when `s` is not `z`'s right child, `x` taking `s`'s old place and `s` taking `z`'s right) and the colour bytes of `z` and `s` are swapped; when `z`'s colour byte is then 1 it runs the red-black rebalancing after erase on `x` (while `x` is not the root and is black: sibling cases with recolouring and rotations by `0071F240(rcx, n)` (left) and `00714B00(rcx, n)` (right)) and stores 1 to `x`'s colour byte; finally calls `00210EB0(z)`, subtracts 1 from the size qword `[rcx+8]` when non-zero, stores `s` to qword `[rdx]` and returns `rdx` | `00714E0C`, `00714F13`, `00714FCE`, `0071500F`, `007150D1` |
| `0071E500` | 680 B | with head `h` = qword `[rcx]` and new node `z` = argument 6: when the size qword `[rcx+8]` is at least 0x2AAAAAAAAAAAAA9 it calls `0071EE70(z+0x20)` and `00210EB0(z)` and `_Xlength_error('map/set<T> too long')` (IAT `008C2618`); otherwise it adds 1 to the size, stores parent `p` = `r9` to qword `[z+8]` and links `z` as root, leftmost and rightmost (qwords `[h+8]`, `[h]`, `[h+0x10]`) when `p` is `h`, else as `p`'s left (qword `[p]`) when `r8b` is non-zero, replacing `h`'s leftmost when it was `p`, or as `p`'s right (qword `[p+0x10]`), replacing `h`'s rightmost when it was `p`; then the red-black rebalancing after insert (links left `+0`, parent `+8`, right `+0x10`, colour byte `+0x18` with 0 red and 1 black, nil byte `+0x19`): while `z`'s parent is red, a red uncle is recoloured with the parent (both 1) and the grandparent (0) and `z` moves to the grandparent, otherwise an inner `z` is first rotated into the parent's place, then the parent becomes 1, the grandparent 0 and the grandparent is rotated, rotations re-point child parents (non-nil only) and `h`'s root link qword `[h+8]` as needed; finally stores 1 to the colour byte of qword `[h+8]`, `z` to qword `[rdx]` and returns `rdx` | `0071E51A`, `0071E528`, `0071E54F`, `0071E5BF`, `0071E79E` |
| `0071E7B0` | 710 B | hinted insert of node argument 5 with key string `k` = `r9`, hint `w` = `r8` and head `h` = qword `[rcx]`, where `L(a, b)` means `0071F430(a, b)` is negative and `I(d, p)` calls `0071E500(rcx, rdx, d, p, k, argument 5)`: when the size qword `[rcx+8]` is 0 it does `I(1, h)`; when `w` is qword `[h]` it does `I(1, w)` if `L(k, w+0x20)`; when `w` is `h` it does `I(0, r)` for `r` = qword `[h+0x10]` if `L(r+0x20, k)`; otherwise, if `L(k, w+0x20)`, with `q` = `w`'s in-order predecessor it does, if `L(q+0x20, k)`, `I(0, q)` when qword `[q+0x10]` is nil (byte `+0x19`) or else `I(1, w)`, and if `L(w+0x20, k)`, with `s` = `w`'s in-order successor it does, if `s` is `h` or `L(k, s+0x20)`, `I(0, w)` when qword `[w+0x10]` is nil or else `I(1, s)`; every other case (including an equal key) calls `0071EA80(rcx, &t, 0, k, argument 5)` and stores the qword at the address it returns to qword `[rdx]`; returns `rdx` | `0071E7F7`, `0071E813`, `0071E8A0`, `0071E973`, `0071EA52` |
| `0071EA80` | 627 B | with head `h` = qword `[rcx]`, key string `k` = `r9` and `C(a, b)` = `memcmp` (thunk `00861ED2`, 0 for length 0) of the strings' data over the shorter length, else -1 when `a` is shorter and 1 when longer (data inline at `+0` when qword `+0x18` is below 0x10, else at qword `+0`; length qword `+0x10`): from root qword `[h+8]` (nil byte `+0x19`) it goes left (qword `+0`) when `C(node+0x20, k)` is not negative (`r8b` non-zero) or `C(k, node+0x20)` is negative (`r8b` zero), else right (qword `+0x10`), keeping the last node `p` (`p` = `h`, counted as left, when the root is nil); when it last went left and `p` is qword `[h]` it inserts at once; otherwise, with `q` = `p`'s in-order predecessor after a left step (qword `[h+0x10]` when `p` is `h`) or `p` after a right step, it inserts when `0071F430(q+0x20, k)` is negative; inserting calls `0071E500(rcx, &t, direction, p, k, argument 5)` and stores the qword at the address it returns and byte 1 to `[rdx]` and `[rdx+8]`; otherwise it calls `0071EE70(argument 5 + 0x20)` and `00210EB0(argument 5)` and stores `q` and byte 0 there; returns `rdx` | `0071EB1A`, `0071EB73`, `0071EBF2`, `0071EC71`, `0071ECC6` |
| `0071F590` | 978 B | erases node `z` = `r8` from the tree with head `h` = qword `[rcx]` (links left `+0`, parent `+8`, right `+0x10`, colour byte `+0x18` with 1 black, nil byte `+0x19`): takes `s` = `z`'s in-order successor (`z` itself when nil); when `z` has at most one non-nil child, that child or nil `x` takes `z`'s place under its parent (or as root qword `[h+8]`), `x`'s parent re-pointed when `x` is not nil, and `h`'s leftmost qword `[h]` and rightmost qword `[h+0x10]` reset to `x`'s extreme or `z`'s parent when they were `z`; otherwise, with `x` = `s`'s right, `s` is spliced into `z`'s place (taking `z`'s left and, when `s` is not `z`'s right child, `x` taking `s`'s old place and `s` taking `z`'s right) and the colour bytes of `z` and `s` are swapped; when `z`'s colour byte is then 1 it runs the red-black rebalancing after erase on `x` (while `x` is not the root and is black: sibling cases with recolouring and rotations, two inline, the others by `0071F240(rcx, n)` (left) and `00714B00(rcx, n)` (right)) and stores 1 to `x`'s colour byte; finally calls `0071EE70(z+0x20)`, calls `00210EB0(z)`, subtracts 1 from the size qword `[rcx+8]` when non-zero, stores `s` to qword `[rdx]` and returns `rdx` | `0071F5DC`, `0071F6E3`, `0071F79F`, `0071F8F5`, `0071F922` |
| `0079BA10` | 978 B | erases node `z` = `r8` from the tree with head `h` = qword `[rcx]` (links left `+0`, parent `+8`, right `+0x10`, colour byte `+0x18` with 1 black, nil byte `+0x19`): takes `s` = `z`'s in-order successor (`z` itself when nil); when `z` has at most one non-nil child, that child or nil `x` takes `z`'s place under its parent (or as root qword `[h+8]`), `x`'s parent re-pointed when `x` is not nil, and `h`'s leftmost qword `[h]` and rightmost qword `[h+0x10]` reset to `x`'s extreme or `z`'s parent when they were `z`; otherwise, with `x` = `s`'s right, `s` is spliced into `z`'s place (taking `z`'s left and, when `s` is not `z`'s right child, `x` taking `s`'s old place and `s` taking `z`'s right) and the colour bytes of `z` and `s` are swapped; when `z`'s colour byte is then 1 it runs the red-black rebalancing after erase on `x` (while `x` is not the root and is black: sibling cases with recolouring and rotations, two inline, the others by `00799BD0(rcx, n)` (left) and `00799C30(rcx, n)` (right)) and stores 1 to `x`'s colour byte; finally calls `00210EB0(z)`, subtracts 1 from the size qword `[rcx+8]` when non-zero, stores `s` to qword `[rdx]` and returns `rdx` | `0079BA5C`, `0079BB63`, `0079BC28`, `0079BCA9`, `0079BDAA` |
