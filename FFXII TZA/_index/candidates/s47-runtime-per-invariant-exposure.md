# S-47 runtime: per-contract stub exposure, and a stub that decides which lists get repaired (OPUS, 2026-09-25)

**Row:** S-47 resource entry tree. The runtime cell is MIXED, *"no per-invariant stub-exposure analysis yet"*. The
row's binding gap (*"types PARTIAL … and nothing executed"*) is stale on its runtime half: four records execute
the three contracts' operations. This note scores nothing.

The records and their disclosed substitutions:

| record | subject | substitutions |
|---|---|---|
| **EXP-083** | entry membership tree (`0036B4E0`, `0036B410`, `0036C790`, `0036A000`, `0036D170`, `003AB880`, `003AB940`) | **none** (*"No callee is stubbed"*); the codec base `[01F83530]` is a planted fixture |
| **EXP-084** | EFX source rebase: resolver, both rebasers, the four repair walks, the driver `003B3480`, and a slice of `0024D540` | **`0024ED80` (a `ret` stub) in the two `rdx ≠ 0` driver cases**; the walk roots `02EBEF70`/`78`/`88`/`90`, the codec base and `02F97340` are planted |
| **EXP-125** | allocator pool adoption, including the BST helpers `0036B410`/`0036B4E0`/`0036C790` | `00369860` (payload release) and `004746F0` (payload copy) inside the adopt-one body `0036A2A0` |
| **EXP-077** | arena initializer address width | `0017D2E0` (`sprintf`): a no-write stub |

## `0024ED80` is not "outside the rebase claim"

EXP-084 describes its one stub as a callee that *"only publishes the second object's field addresses to globals and
is outside the rebase claim"*. The bytes say otherwise:
- **Order:** on the driver's `rdx ≠ 0` path, `003B34A7` calls `0024ED80(rdx)` immediately before the resolver
  (`003B34FC`) and the two rebasers (`003B351A`, `003B3533`).
- **What `0024ED80` writes** (a call-free leaf, `0024ED80`–`0024EE0A`): with `ctx = q[obj+0x340]`,

  | cell | value |
  |---|---|
  | `02F97340` | `ctx` |
  | `02F97348` | `obj` |
  | **`02EBEF70`** | `ctx+0x18` |
  | **`02EBEF78`** | `ctx+0x850` |
  | **`02EBEF90`** | `ctx+0x848` |
  | **`02EBEF88`** | `obj+0x1B8` |
  | `02EBEFA0` / `A8` / `98` / `B0` | four further heads |

- **Who reads them:** the four repair walks read exactly those roots, and nothing else in their bodies selects a
  list:

  | walk | reads |
  |---|---|
  | `003AA3D0` | `02EBEF70` |
  | `003A9BA0` | `02EBEF78` |
  | `003A9860` | `02EBEF90` |
  | `003A8FF0` | `02EBEF88` |

  `0024D970` runs the first three, and `0024D940` runs `003A8FF0`.

So on the `rdx ≠ 0` path, **`0024ED80` decides whose lists the rebase repairs**: the container passed in. The
contract already reads this statically. Section 14 calls `0024ED80` *"the make-a-container-current"* and
identifies `+0x1B8` as the `02EBEF88` head. **But no record executes that selection.** EXP-084's `rdx ≠ 0` cases
walked planted roots.

## Per contract

| contract | claims | can a substitution reach them? | owner reading |
|---|---|---|---|
| **efx-source-rebase** (§1 mechanism, §2 resolver guard, §3 repair, §4 offset round-trip) | the resolver arithmetic, the 64-bit guards, the 32-bit deltas, the 1 + 3 walk split, the wrap cases | no for the bodies. All seventeen run as shipped bytes, and every §13 row is an executed case. | **not reachable** |
| efx-source-rebase: the **driver** with `rdx ≠ 0` | "rebase the caller template, then the container, **repairing that container's lists**" | **yes**: the root selection is the stubbed `0024ED80`, and the roots were planted | **exposed; the selection is unexecuted** (statically read, above) |
| **resource-entry-tree** | membership insert / unlink / descend | no: EXP-083 has no stubs. EXP-125's two stubs are payload helpers inside `0036A2A0` (compaction), not the tree operations. | **not reachable** |
| **resource-input-ownership** (RL-1..RL-9) | layer-relative ownership, borrowed mutability, disposal order | **not mapped by this note.** None of the four records above names these entries (`003EDAD0`, `0026FB90`, `0024B3A0`, `003B38B0`, …) as its subject. Its evidence is the SECTION-06/07 reviews, whose substitutions were not re-read here. | **mapped in the addendum below (block 246)**: one exposure, the overlapping-copy import boundary |

`EXP-077`'s `sprintf` stub writes no memory. The address-width claims are the header writer's and the encoder's
own results, which are not substituted.

## For the scorer

- **efx-source-rebase:** one exposure, and it is a **selection**: which container's lists the driver repairs. The
  execution that would close it is small. Rerun EXP-084's two `rdx ≠ 0` driver cases with `0024ED80` real (about
  0x88 bytes, no calls) and the roots **not** planted. Then check that the walks visit the container's
  `ctx+0x18` / `+0x850` / `+0x848` / `obj+0x1B8` lists. This is routed to ORACLE.
- **resource-entry-tree:** no exposure.
- **resource-input-ownership:** see the addendum (block 246).

## Addendum (OPUS, 2026-09-25, block 246): resource-input-ownership RL-1..RL-9 mapped

The ownership contract's evidence is the SECTION-06, 07, 08, 09 and 10 native controls
(`_experiments/evidence/continuation-section0{6..9}-*`, `…section10-nonempty-registration`). Their substitution
tables were re-read. Every one has **one application substitution**: the diagnostic formatter `0017D2E0`, which
writes an empty string and counts calls, and which the normal fixture paths assert is never reached. Apart from
that they have:
- import adapters: memset `008C2A60`, memcpy `008C2A68` for non-overlapping copies only, strncpy `008C2F70`;
- a synthetic GS stack-limit environment;
- planted arenas, tables and container nodes.

Each review states that no allocator, parser, destructor, queue helper, ticket, bank matcher, compactor, source
free or refresh is replaced by a no-op.

| inv. | executed in | can a substitution reach it? | owner reading |
|---|---|---|---|
| **RL-1** (layer-relative ownership: mask4, copy vs borrow) | SECTION-06, SECTION-10 | the parser and context constructor are original | **not reachable** |
| **RL-2** (borrowed input is mutable) | SECTION-06 | the default subtype only, as the contract states | **not reachable**; specialised rebasers are out of scope by the contract's own wording |
| **RL-3** (allocation vs copy length vs bounds) | SECTION-06 | the copy **length** is original arithmetic; the memcpy adapter only moves bytes | **not reachable** |
| **RL-4** (cleanup layout vs ownership bit) | SECTION-06 | the 800/A00 teardowns are original | **not reachable** |
| **RL-5** (selectors and caches are not handles) | SECTION-06, SECTION-07 | SECTION-06 moves sources **by fixture** (*"the original mover is NOT run"*); SECTION-07 runs the original mover and refresh | **not reachable**, given SECTION-07 |
| **RL-6** (disposal order) | SECTION-08 | ticket cancellation, entry reset and bank removal are original | **not reachable** |
| **RL-7** (state3 / state4 source ownership) | SECTION-09, SECTION-10 | the completion is the original helper; there is no OS IO | **not reachable** for the stated states; the contract itself leaves full failure recovery unproved |
| **RL-8** (view pair; refresh after movement) | SECTION-08, SECTION-07 | the pins run at the real import-copy boundary. **A movement whose source and destination overlap stops at the memcpy import** (SECTION-07 M07-7: `0x100` hole plus `0x400` source, overlapping ranges) | **exposed at the overlapping-copy import**: the shipped mover hands overlapping ranges to the CRT `memcpy` import, and what the CRT does with them is not established |
| **RL-9** (reuse does not transfer the allocation) | SECTION-10 | registration is original | **not reachable** (synthetic alias policy, as the contract says) |

**For the scorer (S-47 as a whole):** there are two exposures across the three contracts.
1. **efx-rebase:** the driver's `rdx ≠ 0` selection of which lists get repaired (`0024ED80`, above).
2. **Ownership:** the overlapping-copy import boundary on source movement (RL-8/RL-5 path). This one is not an
   application stub. It is the CRT's behaviour on overlap, and closing it needs the exact imported routine's
   behaviour, not a host substitute. SECTION-07 already frames it that way.

Everything else is executed with no application stub.

## Addendum (OPUS, 2026-09-26): the overlapping-copy exposure executed

The second exposure above (**ownership**: the overlapping-copy import on source movement, RL-8/RL-5) is executed in
[`s47-opus-crt-memcpy-overlap/`](s47-opus-crt-memcpy-overlap/README.md).
- **The routine.** The image imports `memcpy` from `VCRUNTIME140.dll` (IAT `008C2A68`) and ships no app-local copy.
  In the host's System32 copy (14.51.36247.0, SHA `d1f4225d…`), the `memcpy` export is one `jmp` to `memmove`.
- **Executed on the host CPU** through the DLL's own code, with every dispatch path forced: 39,215 overlapping and
  adjacent copies, M07-7's shape included, give **0 failures** against memmove's result. A forward-copier control is
  caught.
- **The census.** All 41 x64 `vcruntime140.dll` versions on the host (14.00–14.51) export `memcpy` as `memmove`: the
  same entry or a single `jmp`.
- **M07-7 carried past the import.** SECTION-07's own harness is run in a patched copy (the original is SHA-verified and
  untouched). Its overlap adapter performs the measured semantics. The real compactor moves `0x30000500` →
  `0x300003C0` with the whole `exact_move` post-state, **23/23**. ORACLE's 123-check baseline is unchanged, and a
  backward-copier control fails exactly the payload assertion.

**RL-8's owner reading becomes "not reachable".** The overlapping case is executed through the bound CRT's semantics.
What remains is a host whose VCRUNTIME140 lies outside the census, and a live game.
