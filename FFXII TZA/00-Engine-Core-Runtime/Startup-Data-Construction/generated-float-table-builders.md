---
system: The 0x480000 builder region — 522 KB of generated float code that runs once at startup
category: 00-Engine-Core-Runtime
status: DOCUMENTED — every question the page asks is answered: the objects are pre-built VIF1 packets (BH-1), each builder's object is decoded on the VIF1/VU1 page (BH-2), the hub split (BH-3), the region's other functions (BH-4), the 48 object sizes (UQ-46) and the 15 helper-less builders (UQ-47); the payload's meaning is UQ-213 (ANSWERED); sections 4, 5 and 8 filled 2026-09-30 (SWE2-CONTRACT); owner read 2026-09-30 (OPUS, `_index/candidates/dd-owner-read-b1-0930/`)
evidence_tier: 1
owner_layer: CodeDomain — Boundary.Presentation.RegisteredFunctionAddress and neighbours
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 2
  last_pass: 2026-09-02
  last_pass_state: GN158 checkpoint 2ed8affb… / snapshot 46f02e26…, project GFZ_HD2
  falsification_passes: 1
  last_falsification: 2026-09-02
  last_falsification_by: repos-d2
  falsification_result: 6 claims overturned, 11 survived — see section 10
---

# The `0x480000` builder region

> **Identity found 2026-09-13 (FABLE): this region is the PS2 VIF1 / VU1 layer.** The 66 startup objects are **pre-built
> VIF1 command packets**. 48 of the 74 hub targets store both STCYCL and MSCALF command words, 56 store BASE and OFFSET,
> and a 300-function random control stores neither. That is why the builders are 83 % `mov` of immediates.
> The large float bodies §2 profiled are **recompiled VU1 microprograms**, installed by MPG commands whose payload is
> a function pointer and called by MSCAL. They run over an emulated 1,024-cell VU memory at `02064E30`.
> The interpreter is `0022C970`. See [the VIF1 / VU1 layer](../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md).
> This answers BH-1's identity and most of BH-4. The boxes below stay unticked until the question ledger is free to mirror
> them (FABLE-LEDGER-AP7-EU1). *(Stale since: every box in §7 is ticked and its register row closed — BH-1 to BH-4,
> UQ-46, UQ-47; noted 2026-09-30, SWE2-CONTRACT.)*
>
> **And six of these objects have a named consumer, 2026-09-20 (FABLE, Claude Opus 5).** `02AEB610`, `02AEB810`,
> `02AEB0F0`, `02AEB290`, `02AEA270`, `02AE9BC0` and `02AE9130` are **prototypes copied at run time** by the effect
> element type builders: the copy keeps the object's MPG descriptor verbatim and re-points its data descriptor at a
> freshly built block in the frame packet arena. So the microprogram a row installs is the one an element type of
> that character code runs — the map is in
> [the VIF1 / VU1 layer](../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md) §2.4b. The per-packet contents are still undecoded (BH-2).
> *Decoded since: BH-2 was ANSWERED 2026-09-26 (FABLE) — every builder's object is decoded on that page's §2.4a–§2.4d,
> and what the payload values mean to the microprograms is UQ-213, ANSWERED 2026-09-27 (pointer added 2026-09-30,
> SWE2-CONTRACT).*

**Seven per cent of the game's code, and it runs once.** 197 functions, **522,045 bytes**, mean
function size 2,649 — twelve times the binary's average — reached through a single call at startup and
never again.

**Status is `PARTIAL` deliberately.** *(answered: see the front matter, status DOCUMENTED after the owner read of 2026-09-30; 2026-10-02, OPUS)* The chain, the trigger, the targets and the code's character are
established. **What the 75 objects it builds actually are is not.** *(Superseded: there are 66 objects (§10), and they
are pre-built VIF1 packets, each decoded on the VIF1/VU1 page — BH-1 and BH-2 in §7. The status word stays until the
owner read; 2026-09-30, SWE2-CONTRACT.)*

## 1. What the player sees

**A pause before the title screen.**

This is the largest single block of work the game does at startup that is not loading a file. Between
the executable starting and `GameApplication` declaring itself ready, **65 generated routines write
66 objects into memory that has no file image.**

> **OVERTURNED in section 10.** This sentence said *"65 generated routines run 522 KB of
> floating-point code to construct 75 objects from nothing "*— *"the data has no file image at all,
> so every value in it is computed rather than read."* **Three errors.** There are **66** objects,
> not 75. The 65 builders total **32,848 bytes**, not 522 KB — that figure is the whole 197-function
> region, only 6.3 % of which is reachable from this chain. And the values are **not computed**: the
> builders are 83 % `mov` and 1 % `xmm`, storing **immediate constants** — so the data *is* in the
> file, as operands inside `.text`, rather than in a data section.

## 2. Native mechanism

### The chain, end to end

```
GameApplication setup
   0017D000
      +31   call 0017D4C0  ------> 0022A0B0 (978 B)
                                      -> 0037DF90 (344 B) : 26 calls into the region
                                      -> 0037E0F0 (596 B) : 40 calls into the region
                                             66 (data pointer, builder) pairs total
      +41   call 00210EC0            allocate
      +59   call 0018A840
      +111  call 00189000
      +116  mov byte ptr [rbx + 0x113c], 1     <- the startup latch closes
```

**The region is built first; the latch closes last.** `0017D000` is the same function documented as
the sole writer of `GameApplication`'s ready flag
([the application root](../Application-Root/game-application.md)) — and this is the work it does
before setting it. **Two documents reached that function from opposite directions and agree on its
role.**

### The builder calls

Both hubs are flat sequences of the same two instructions:

```asm
lea  rcx, [rip + <data address>]
call <builder in 0x480000-0x500000>
```

**66 pairs** — 26 from the first hub and 40 from the second, each a distinct data pointer handed
to a builder; 66 distinct pointers and **65** distinct builder functions, the two hubs' builder sets
being disjoint. No loop, no table — the call list is unrolled in the instruction stream.
**(Corrected from "75 pairs" in section 10; 26 + 40 = 66.)**

### The targets have no file image

```
data targets   : 02ADEF40 .. 02AED330   (.data)
.data          : virtual 01DF0000 + 011A7530, raw only 002893F0
first target maps to file offset : None
```

**Every target lies beyond the section's raw data**, in the zero-filled tail. The objects do not exist
in the file; they are constructed entirely at run time. Gaps between consecutive targets — **336, 400,
304, 16, 3520 bytes** — say the objects vary in size.

### The code is scalar float math and says nothing

> **OVERTURNED in section 10, twice.** **None of the six functions profiled below is a builder** — not one is called by either hub, and all six are among the 131 region functions the startup
> chain never reaches. And the actual builders are **not float code**: across all 65, 83 % of
> instructions are `mov`, **1 %** touch `xmm`/`ymm`, and there are **39 scalar and 25 packed float
> operations in total**. The table below is a true census of six large functions in the same address
> range and says nothing about the builders. Section 10 gives the builders' own census.

| function | size | instructions | calls | xmm/ymm | dominant opcodes |
|---|---:|---:|---:|---:|---|
| `004B1190` | 32,136 | 6,492 | 276 | **42 %** | `movss` 923, `lea` 755, `mulss` 367 |
| `004C8320` | 28,422 | 5,382 | 49 | **63 %** | `movss` 869, `mulss` 640, `movups` 617 |
| `004F7070` | 24,541 | 4,907 | 50 | **61 %** | `movss` 1007, `mulss` 527, `movaps` 466 |
| `004EF940` | 22,073 | 4,342 | 47 | **65 %** | `movss` 938, `mulss` 500, `movaps` 443 |
| `004E31E0` | 18,098 | 3,372 | 38 | **73 %** | `movss` 838, `mulss` 319, `movups` 302 |
| `004E7D90` | 15,212 | 2,903 | 30 | **69 %** | `movss` 689, `movups` 284, `mulss` 227 |

**`movss` / `mulss` / `addss` are *scalar* single-precision** — one float at a time in a vector
register. This is ordinary compiler output for float-heavy straight-line code, **not hand-written
SIMD**: nothing here processes four lanes at once.

**The 25 largest functions reference zero strings between them.** No diagnostics, no names, no format
strings — which is why nothing in this region was ever picked up by the string cross-reference passes
that named thousands of functions elsewhere.

## 3. Key addresses

| | |
|---|---|
| region | **`0x00480000` – `0x00500000`** |
| functions | **197**, 522,045 bytes, mean 2,649 |
| trigger | `0x0017D000` (+31) → `0x0017D4C0` → `0x0022A0B0` |
| hubs | `0x0037DF90` (26 calls), `0x0037E0F0` (40 calls) |
| data targets | `0x02ADEF40` – `0x02AED330`, uninitialised `.data` |
| largest functions in the range (**not builders** — section 10) | `004B1190`, `004C8320`, `004F7070`, `004EF940`, `004E31E0`, `004E7D90` |
| the 65 actual builders | 44 — 2,250 B each, **32,848 B total**; largest `004B8F20` |

**Reach from outside:** 142 direct call sites, 45 distinct callers — but `0037E0F0` and `0037DF90`
alone account for **66 of them**. One named caller exists: `RenderCommand_InitializeDoubleBuffers`
(`0x003A1D50`).

## 4. Data structures and formulas

~~**Not established.** The gaps give object sizes and the instruction mix gives the arithmetic's shape,
but **no builder has been read line by line and no constructed object has been decoded.** The honest
statement is structural: *75 variable-size objects, built by float arithmetic, in memory with no file
image.*~~ *Superseded (2026-09-30, SWE2-CONTRACT, citing answered rows): §7 and §11 answer it.*

**The objects (filled 2026-09-30, SWE2-CONTRACT, from existing answers).** Sixty-six objects at `02ADEF40`–`02AED330`
in uninitialised `.data`, one per hub call, each a **pre-built VIF1 packet template** (BH-1). Their sizes are all
determined (UQ-46): for 66 of the 74 objects with a next pointer the builder's last store ends exactly at the next
object, and the rest are read from each packet's own DMA `cnt` tag (`qwc`) or its `UNPACK V4_32` count
([the UQ-46 record](../../_index/candidates/uq46-packet-ends/README.md)). A builder computes nothing data-dependent: it
optionally clears a range and fills the packet with immediate stores (BH-2, UQ-47), and the per-template layout — the
command stream, MPG record, GIF tag and GS register writes — is the generated template table on
[the VIF1 / VU1 layer](../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md) §2.4a–§2.4d (77 rows).

The common header the builders write, whether through a helper or inlined (UQ-47):

```
packet template, the words UQ-47 lists (not a full layout; the full per-template tables are on the VIF1 / VU1 page)
+0x08  u32  word08   0x03000000 or 0x0300001E
+0x0C  u32  word0C   0x02000000 or 0x020001F1
+0x18  u32  word18   0x01000404 in all sixteen helper-less builders
+0x1C  u32  word1C   0x6CNN0000, NN in {11, 12, 14, 17, 18, 19, 1A, 1C}
```

The helper-using builders also stamp `+0x00`..`+0x07` and register the packet: `008631E0(packet, program, addr)`
appends the 16-byte record `(0x4A000000 | addr, program)` to `02EAF930` at the counter `02EB37B0` (1,000 records, no
bound check) and stores at the packet's `+4` the 32-bit handle of that record (`0020E620`), which consumers resolve
with `0020E600` (§11). `0x4A` is the VIF **MPG** command code, and on this port its payload is an 8-byte x64
function pointer (the VIF1 / VU1 layer, command table).

## 5. Call chain

See section 2 — the chain is the finding.

**Filled out (2026-09-30, SWE2-CONTRACT):**

```
GameApplication startup: 0017D000 (before it sets the readiness latch +0x113C)
  -> 0017D4C0 -> 0022A0B0 (the boot fixer)
       -> 0037DF90 : 26 builder calls, objects 02ADEF40..02AE6BF0      <- THIS SYSTEM
       -> 0037E0F0 : 40 builder calls, objects 02AE8620..02AED330      <- THIS SYSTEM
            each: lea rcx, [object] ; call builder
                 builder -> memset (18 of them) | 004DC8B0 (0x11000000) | 008631D0 (command word)
                         | 008631E0 (MPG record -> 02EAF930, handle -> packet +4)
later: the packets are sent through the VIF1 interpreter 0022C970, which runs MPG-installed
       microprograms over the emulated VU memory at 02064E30; some packets are copied as prototypes
       by the effect element builders (the banner above; the VIF1 / VU1 layer §2.4b)
```

**Upstream (who causes this):** application startup, once, from the same function that then declares the game ready.

**Downstream (what this causes):** the VIF1 packets every VU1-path draw starts from.

**Do not confuse with:** the region's other functions — VU microprograms and a 24-function tail of ordinary game code —
which the startup chain does not call (BH-4).

## 6. Modding notes

- **`0x0017D4C0` is the single switch for the builders.** Nothing except the two hubs calls any of
  the 65 builders — verified, zero other callers. **But "everything in this region is downstream of
  one call" is false** (section 10): the chain reaches **66 of 197** functions, and the other 131 are
  entered by 142 call sites from 45 callers outside the region.
- **The objects cannot be patched in the file.** They are in uninitialised `.data` and are written
  only at run time, so a static edit has nothing to edit.
- **XIIOnline:** this runs before the ready latch closes, so it completes before any gameplay path is
  live. It is not a per-frame cost and not a synchronisation concern.

## 7. What is not known

- [x] ~~**What the 66 objects are.**~~ *Identity answered 2026-09-13 (FABLE): pre-built VIF1 packets; contents are BH-2.* This is the whole question. **Now statically answerable** —
      section 10 shows each builder `memset`s its object to a size given as an immediate (`0xDC0` =
      3,520 for `00485390`) and then fills it with `mov [obj+off], imm` stores, so **the object
      contents can be decoded from the instruction stream** without running the game. **BH-1.**
- [x] What any individual builder computes. One (`00485390`) has now been read far enough to
      establish the *form* (section 10); ~~none has been decoded to its object's contents~~. **BH-2.**
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5) by reference: every builder's object is decoded, on [the VIF1 / VU1 layer](../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md) §2.4a–§2.4d.**
      - A builder computes nothing data-dependent. It fills a pre-built VIF1 packet with immediate stores, and the
        page's generated template table decodes each one (77 rows): the command stream, MPG record, GIF tag and
        GS register writes.
      - Every in-region builder the hubs reach has a row, and no row has an unattributed store. Control: [`bh4_region_callers.py`](../../_index/candidates/bh4-region-callers/bh4_region_callers.py).
      - What the payload values mean to the microprograms is `UQ-213`.
- [x] Why the split into two hubs of 26 and 40, and whether the order matters. **BH-3.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BH-3): the order does not matter to any
      packet's contents, and the split follows two disjoint object blocks.*
      Instrument: [`members/bh3_hubs.py`](members/bh3_hubs.py), capstone over both hubs and every target.
      - **Counted over all direct calls,** not only calls into the `0x480000` band: `0037DF90` makes 28 and `0037E0F0`
        makes 49 (48 distinct; `004E3110` twice). Each call is preceded by its own `lea rcx, [object]`. The 26 / 40 above
        count calls into the band; the rest land at `0047E140`, `00476C80`, `004791E0`, `004795D0`, `00479450`,
        `0047A800`, `0047BAF0`, `002EFF50` and `002F0110`.
      - **The two hubs build two disjoint, contiguous object blocks.** Sorted by address, all of `0037DF90`'s objects
        (`02ADEF40`–`02AE6BF0`) come before all of `0037E0F0`'s (`02AE8620`–`02AED330`), with no interleaving. That is
        the layout two separately compiled groups of zero-initialised data get from the linker, so **the best-supported
        reason for two hubs is two source groups, one init function each.** The builders' code does not show the same
        clean split: `0037DF90`'s targets are one run, and `0037E0F0`'s sit on both sides of it (8 below, 41 above).
      - **Why the order cannot change a packet.** No target has a rip-relative operand on another hub object or on any
        `.data` address. Their only calls are `memset`, the constant `004DC8B0` (returns `0x11000000`), the command-word
        stub `008631D0` and the MPG record emitter `008631E0`.
        - `008631E0` is the one shared state. It appends `(0x4A000000 | addr, program)` to `02EAF930` at the counter
          `02EB37B0` and stores in the packet an encoded reference to *that record* (`00863206`–`0086322B`).
        - The table and counter have no other reference in the image (`tools/ripscan.py`: three sites, all in
          `008631E0`). Hub order therefore decides only a record's position, which nothing reads by index.
      - **Capacity, noted in passing.** `02EAF930 + 1000 × 16 = 02EB37B0`, so the table holds exactly 1,000 records and
        ends at its own counter. `008631E0` does not check the bound.
- [x] Whether the 45 external callers use the region's *other* 132 functions for something beyond
      startup construction — the 142 call sites are counted, not classified. **BH-4.**
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): yes. No call site outside the two startup hubs reaches a builder.** Control: [`bh4_region_callers.py`](../../_index/candidates/bh4-region-callers/bh4_region_callers.py)
      (4 checks, FAILS 0). First measured by a delegated read-only pass; re-derived here.
      - **The tail.** Apart from the two microprograms below, every non-hub call or tail jump into the region lands
        on a 24-function tail at the region's top end. That tail is ordinary game code, not VU code: the region
        classification (`99-Unresolved-Residual/vu-region-classification.tsv`) finds neither VU signal in all 20 of
        the tail's functions it covers.
      - **The VU-internal calls.** Three VU helpers are called only by two microprograms that sit just below
        `0x480000`.
      - **The builder count.** The census reproduces 142 call sites from 45 callers. Counting the hubs' two tail
        jumps, the hubs reach 67 in-region builders.

## 8. Evidence

**Tier 1** for everything claimed; the claims are deliberately structural.

**How this was found, and why it had been missed.** A census of every address cited anywhere in the
database against the ledger showed **86.5 % of the executable's code bytes sit in functions no
document mentions**. Bucketing the uncited mass by address put this region at the top: 522 KB in
64 KB of address space, mean function size twelve times the binary's average. **It was invisible to
every technique used so far** — no RTTI vtable (not a class), no authored strings (it emits none), no
`PrimaryOwner`.

**The chain was traced by direct call scan**, not by adjacency: every `E8` call site in `.text` was
decoded and attributed to its containing function, which is how the two hubs and their single caller
were found. Address adjacency is a banned evidence class here and is not used — the region's
*boundaries* are stated as an address range because that is what they are, but nothing about its
membership rests on that.

**The `.data` finding is a negative that proves itself:** `va2off()` returns `None` for the targets
because they lie past the section's raw size. A wrong section table would have failed for everything,
not just these.

**The ordering inside `0017D000` is read from its disassembly** — the builder call at +31, the latch
write at +116 — so "built first, ready last" is instruction order, not inference.

**A defect this document carried on first write, and it is the second instance today.** The named
caller was written as `RenderCommand_InitializeDouble`; the real name is
`RenderCommand_InitializeDoubleBuffers`. **Both instances have the same cause**: an analysis script
printing names through a fixed-width format (`%-30s`, `%-28s`), and the clipped string being copied
into prose. `check_names.py` caught both. **The durable fix is in the scripts, not the care** - a
census that prints identifiers must not truncate them, and the standing rule against completing a
truncated name is worth nothing if the tool hands you one that looks whole.

**Claims, evidence and tier (added 2026-09-30, SWE2-CONTRACT).**

| Claim | Evidence | Tier |
|---|---|---|
| One startup chain builds 66 objects through two hubs, before the readiness latch | direct `E8` scan; `0017D000` disassembly (+31 call, +116 latch) | 1 |
| The objects have no file image | `va2off()` is `None` past `.data`'s raw size | 1 |
| The objects are pre-built VIF1 packets | BH-1: STCYCL/MSCALF and BASE/OFFSET command words in 48 and 56 of 74 targets, a 300-function random control storing neither | 1 |
| Each object's contents are decoded | BH-2: the VIF1 / VU1 layer §2.4a–§2.4d; `bh4_region_callers.py` | 1 |
| All 48 memset-less sizes are determined | UQ-46: `members/builder-store-extents.tsv`; `uq46_packet_ends.py` | 1 |
| Hub order changes no packet | BH-3: `members/bh3_hubs.py` | 1 |
| No call site outside the hubs reaches a builder | BH-4: `bh4_region_callers.py`, 4 checks | 1 |
| `02EAF930` entries are reached through their own handle | §11: `008631E0`'s last three instructions; the `0020E600`/`0020E620` codec | 1 |
| The `0x4A000000` tag is the MPG command the interpreter dispatches on | the VIF1 / VU1 layer command table (`0022CA3D`–`0022CA60`) | 1 |

**What is deliberately not claimed.** ~~That these are shader tables, geometry, curves, or anything
else.~~ *Narrowed 2026-09-30 (SWE2-CONTRACT, from the owner read): what the objects are is answered — pre-built VIF1
packets (BH-1), each decoded (BH-2). What each payload value means to its microprogram is answered as UQ-213 (the VIF1 /
VU1 layer); nothing beyond those two records is claimed here.* The GFZ's own tag says `Boundary.Presentation.RegisteredFunctionAddress`, which locates the
domain and no more. ~~**BH-1 holds the identity open**, and until a builder is read, any name for this
subsystem would be a guess dressed as a finding.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **BH-1** was answered on 2026-09-13. The objects are pre-built VIF1 packets for the VU1 microprograms (the banner at the top of this page).*

## 10. Falsification pass 1 — 2026-09-02, session `repos-d2`

**This document was previously unattacked**, and its own frontmatter said so rather than implying a
pass had happened. That note is what made this pass cheap to scope.

**Program state.** Parent `2ed8affb…`, snapshot `46f02e26…`, embedded EXE `73461d08…`, ledger
38,161 / 38,003 / 158, project `proj_hd2` / `GFZ_HD2`, `CHECKPOINT VERIFIED` before any reading. All
figures below are from a capstone census over the ledger's 38,161 bodies, reading the authorized EXE
directly.

### Overturned

**1. There are 66 objects, not 75.** Decoding both hubs: `0037DF90` issues **26** calls into the
region, `0037E0F0` issues **40** (of 48 total). Every one is preceded by its own `lea rcx,[rip+...]`.
**26 + 40 = 66 pairs, 66 distinct data pointers, 65 distinct builders** (the hubs' builder sets are
disjoint; one builder appears twice inside hub 2). The document's own per-hub numbers were right and
their sum was not. **75 propagated into §1, §2, §4 and BH-1.**

**2. The builders are not 522 KB.** The 65 builders total **32,848 bytes**. Following direct calls
transitively from them reaches **66 of the region's 197 functions and 32,854 bytes — 6.3 % of
522,045.** The 522 KB figure describes the *address range*, not the startup work; the document
attached it to the routines.

**3. Most of the region is not downstream of the startup chain.** **131 of 197** functions are never
reached from `0017D4C0`. §6's *"everything in this region is downstream of one call"* is false. Its
other half — *"nothing else reaches the builders except the two hubs"* — **is exactly right**:
zero callers of the 65 builders outside the two hubs.

**The hubs themselves cross layers downward** (Pass 22 2026-09-14): `0017D4C0` reaches
**resource** `001DB1E0`/`001A11B0`, **input** `00198750`, and `0022A0B0` reaches **resource**
`0032EAE0`/`002DF9A0`, **input** `0035B270`, **actor** `002368D0` — 10 edges. Startup code that
fills tables from loaded data calls resource and input bodies to fetch what it writes; the
crossing is the construction path, not a second owner.

**4. None of the six profiled "largest builders" is a builder.** `004B1190`, `004C8320`, `004F7070`,
`004EF940`, `004E31E0`, `004E7D90` are the largest *functions in the address range*; **not one is
called by either hub**, and all six are among the 131 the chain never reaches. The actual builders
run **44 to 2,250 bytes**, the largest being `004B8F20`.

**5. The builders are not float code.** Census over all 65:

```
instructions          4,518
xmm/ymm-touching         65   (1 %)
dominant opcodes        mov 3,740 (83 %) | xor 126 | lea 98 | call 91 | ret 64
scalar float ops         39   (movss/mulss/addss/subss/divss, ALL 65 builders combined)
packed float ops         25
```

Against the profiled non-builders' 42-73 % xmm and hundreds of `movss`/`mulss` each, this is a
different kind of code entirely. **The heading *"the code is scalar float math"* is true of the six
functions measured and false of the builders.**

**6. The values are not computed, and they are in the file.** `00485390` (1,023 B, a real builder),
read directly:

```asm
0048539A  xor  edx, edx
0048539C  mov  r8d, 0xdc0             ; the object's SIZE - 3,520 bytes
004853A5  call 0x861ec0               ; memset(obj, 0, 0xDC0)
004853AD  lea  rdx, [rip - 0x2b54]
004853B7  call 0x8631e0
004853C1  mov  dword ptr [rbx + 8],    0x3000000
004853CC  mov  dword ptr [rbx + 0xc],  0x2000000
004853D8  mov  dword ptr [rbx + 0x18], 0x1000404
004853E1  mov  dword ptr [rbx + 0x1c], 0x6c180000
004853E8  mov  qword ptr [rbx + 0x20], 0xa
...       mov  dword ptr [rbx + 0x44], 0x3f800000     ; 1.0f, stored as an INTEGER immediate
```

**Zero-fill to a size given as an immediate, then a long run of `mov [obj+off], imm`.** Float values
appear as raw bit patterns in integer moves — which is precisely why the `xmm` share is 1 %.

§1 said *"the data has no file image at all, so every value in it is computed rather than read."*
**The first clause is right and the inference from it is wrong.** The values are in the file; they
are in `.text`, as immediate operands, instead of in a data section. *"No file image"* was measured
on the **destination** and asserted about the **source**.

**This is the pass's most useful result, because it reopens BH-1 as a static question.** Each
builder's `memset` immediate gives its object's size — `0xDC0` = 3,520 for `00485390`, which is the
largest inter-target gap the document already observed — and the store sequence gives the contents.
**The 66 objects can be decoded from the executable without running it.**

### Survived

| Claim | Result |
|---|---|
| region = **197 functions, 522,045 bytes** in `00480000`-`00500000` | **SURVIVED exactly.** |
| hub call counts **26** and **40** | **SURVIVED exactly.** |
| **65** distinct generated routines | **SURVIVED** — 26 + 39, disjoint. |
| data targets `02ADEF40` - `02AED330` | **SURVIVED exactly.** |
| target gaps 336, 400, 304, 16, 3520 | **SURVIVED** — all five occur (336×8, 400×7, 304×6, 16×5, 3520×1). |
| **142** call sites, **45** distinct callers *from outside* | **SURVIVED exactly**, on the stated population. |
| nothing but the two hubs calls the builders | **SURVIVED** — zero others. |
| `0017D000` +31 / +41 / +59 / +111 call targets and the +116 latch write `mov byte [rbx+0x113c], 1` | **SURVIVED, all five exact.** |
| targets lie beyond `.data`'s raw extent | **SURVIVED** — `va2off` returns `None`; raw-backed VA ends at `01F7E400`, first target `02ADEF40`. |
| the six profiled functions' sizes (32,136 … 15,212) | **SURVIVED, all six exact.** |
| **the 25 largest functions reference zero strings** | **SURVIVED, with the control the claim needed** — 0 hits, and the same query against `BattleStorage_InitializeWorkArrays` returns **4**. |

### Figures that did not reproduce, without affecting a conclusion

`.data` is quoted as *"virtual 01DF0000 + 011A7530, raw only 002893F0"*. The virtual base and size
are exact; the raw figure is not — the section's raw size is **`0x0018E400`** and its file offset
`0x01CCE600`. Neither is `0x002893F0`. **The conclusion is unaffected and was re-verified
independently**: the raw-backed range ends at VA `01F7E400`, every target is above it, and the
offset lookup returns `None`.

### A count disagreement chased rather than reported

My first census returned **487** call sites into the region from **88** callers, against the
document's 142 / 45. The document says *"Reach from **outside**"*; restricting to callers outside
`00480000`-`00500000` gives **142 sites, 45 callers** — exact. The other 345 sites are intra-region.
**Third pass running in which a count disagreement resolved into a population difference with the
document correct.** The same discipline is why finding 1 is reported as a finding: there the
document's own two numbers do not sum to its own total, which is not a population question.

### What was tried and failed to break anything

- **Tried to break the region census** by recomputing 197 / 522,045 from the ledger independently.
  Exact, and the mean follows.
- **Tried to make the gaps wrong.** The five quoted values looked like the first five in order and
  are not — but all five occur in the gap multiset, so the claim as written ("gaps ... say the
  objects vary in size") holds. **Checked before reporting; would have been a false finding.**
- **Tried to find a builder called from outside the hubs.** Zero.
- **Ran a positive control on the strings absence** before accepting it.
- **No banned evidence.** No `.pdata`, `.xdata`, unwind or EH reasoning. The region is named by an
  address range because that is what it is, and no membership or semantic claim rests on adjacency;
  the builder set is defined by *being called from the hubs*, not by lying in the range.

### Consequences

- **BH-1 moves from "not established" to "extractable".** A decoder over the 65 builders' immediate
  stores yields all 66 objects' sizes and contents statically. That is the single highest-value
  follow-up in this document.
- **BH-2 narrows**: the builders' *form* is now known (zero-fill then immediate stores); what remains
  is what the stored constants mean.
- **BH-4 is answered in part**: the 131 functions the chain never reaches are entered by 142 outside
  call sites from 45 callers, so the region is **not** a startup-only region. Only 6.3 % of its bytes
  belong to startup construction.
- **The document's title should be revisited.** *"Generated float table builders"* names a
  characterisation that this pass overturned; the builders are generated table writers, and the float
  code in the range is something else that the startup chain does not call. *Done since (noted 2026-09-30,
  SWE2-CONTRACT): the heading and the `system:` line now read "The `0x480000` builder region", and the banner at
  the top names the VIF1 identity; the file name is kept so existing links resolve.*
- *(BH-2 and BH-4 in the two bullets above are both ANSWERED since, 2026-09-26; see §7.)*

## 9. Related

- [`../Application-Root/game-application.md`](../Application-Root/game-application.md) — the startup
  latch this construction precedes, and the same function `0017D000` seen from the other side.
- [`../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md)
  — **T-6** asks whether initializer *counts* track startup *cost*, noting that one initializer
  building a large table outweighs fifty pointer assignments. **This region is that case in its
  extreme form** — though note it is **not** a CRT static-initializer chain: it is an explicit call
  from application startup.

## 11. The objects decoded — 2026-09-03

The premise this block was assigned under was that **each builder's `memset` immediate gives its
object's size, so all 66 are decodable statically.** ~~That is true for a quarter of them.~~
**Corrected 2026-09-17 (FABLE): it is true for fifteen of the eighteen, whose `memset` starts at `+0`.** Three
call it on an *interior* sub-buffer — `00492D40` at `+0x1E8` (0x9C0) and `+0xBC0` (0x1F0), `00485390` at `+0`
(0xDC0) and again at `+0xBC0`, `0048CE70` at `+0xBC0` (0x1F0) — so an immediate is a sub-buffer size unless the
call's `rcx` is the object itself. The two rows below that were *not* exact are those two sub-buffers; the objects'
written extents are `0xDC0`, their gaps. The size witness that does not need `memset` at all — the builder's last
store — is in [`members/builder-store-extents.tsv`](members/builder-store-extents.tsv) (`UQ-46`).

### Only 18 of the 65 builders call `memset` at all

Decoding both hubs again (66 pairs, 26 + 40, reproduced exactly) and reading every builder body:

| the builder calls | count |
|---|---:|
| `memset` (`00861EC0`) | **18** |
| the header initialiser `008631D0` | **40** |
| the registration helper `008631E0` | **29** |
| none of the three | 15 |

**Seventeen object sizes are recoverable**, and they verify against the layout: every one is **≤ the
gap to the next data pointer, and nine are exactly equal to it** — which is what consecutive
objects with no padding look like.

| data pointer | builder | `memset` size | gap to next | |
|---|---|---:|---:|---|
| `02ADEF40` | `00492D40` | ~~`0x9C0`~~ | `0xDC0` | **sub-buffer at `+0x1E8`, corrected 2026-09-17 (FABLE); the object's written extent is `0xDC0`, exact** |
| `02ADFE90` | `004956A0` | `0x150` | `0x150` | **exact** |
| `02AE21B0` | `00485390` | `0xDC0` | `0xDC0` | **exact** |
| `02AE31F0` | `004B0000` | `0x140` | `0x140` | **exact** |
| `02AE3330` | `004B0B70` | `0x130` | `0x2F0` | |
| `02AE4160` | `0048CE70` | ~~`0x1F0`~~ | `0xDC0` | **sub-buffer at `+0xBC0`, corrected 2026-09-17 (FABLE); the object's written extent is `0xDC0`, exact** |
| `02AE8620` | `004D3E20` | `0x80` | `0x190` | the ctor installs `004D40E0` as the object's member body (`lea rdx` → `008631E0` at [`004D3E2D`](../../_index/ADDRESS-INDEX.md)); `004D40E0` itself is 14,891 B — read 2026-09-17 (SWE2-FRONTIER): a `0022CC20`/`0022CC40`/`0022CC30` processor battery (×13/×5/×5) over `004DF360`/`005376D0` with `sqrtf` ×4 — first `0022CC20` call at [`004D4238`](../../_index/ADDRESS-INDEX.md), first `sqrtf` at `004D431F`; the same processor-trio profile as the `00478280` frame callback |
| `02AE8900` | `004F4F80` | `0x2E0` | ~~`0x530`~~ `0x2E0` | **exact** against `02AE8BE0`, the next data pointer, which `0037E0F0+0x124` hands to `0047A800` below the band; `0x530` is the gap to the next in-band pointer `02AE8E30` *(corrected 2026-10-02, OPUS: not counted in the nine above)* |
| `02AE8E30` | `004FD060` | `0x300` | `0x300` | **exact** |
| `02AE9140` | `004DA460` | `0x150` | `0x150` | **exact** |
| `02AEA270` | `004DC6B0` | `0x130` | `0x130` | **exact** |
| `02AEA3A0` | `004C2040` | `0xC20` | `0xD50` | |
| `02AEB0F0` | `004DCA00` | `0x90` | `0x1A0` | |
| `02AEB360` | `004C4A50` | `0x150` | `0x150` | **exact** |
| `02AEB610` | `004E2930` | `0x200` | `0x200` | **exact** |
| `02AEB820` | `004E2CD0` | `0xC0` | `0xC0` | **exact** |
| `02AEBE10` | `004C8080` | `0x80` | `0x290` | |

`0xDC0` = 3,520 is both a `memset` size and the largest inter-target gap §2 measured — the two are
the same object, `02AE21B0`.

### What the other 47 do instead — and it is not clearing memory

Neither of the two hot helpers is a `memset` variant. Both write a **common object header**:

```asm
008631D0(obj, dx)                       ; 15 bytes - header only
    word  [obj + 0] = dx
    byte  [obj + 3] = 0x10              ; kind tag
    dword [obj + 4] = 0

008631E0(obj, rdx, r8d)                 ; 84 bytes - header + REGISTRATION
    byte  [obj + 3] = 0x30              ; a different kind tag
    word  [obj + 0] = 1
    n = *(u32 *)02EB37B0                ; a global counter
    *(u32 *)(02EAF930 + 16*n)     = r8d | 0x4A000000
    *(u64 *)(02EAF930 + 16*n + 8) = rdx
    *(u32 *)02EB37B0 = n + 1
    dword [obj + 4] = FUN_0020E620(...) ; the returned id is stored back in the object
```

So the objects share a header — a `u16` at `+0`, a **kind byte at `+3`** (`0x10` or `0x30`), and a
`u32` at `+4` that is zero for the plain kind and a **returned id** for the registered kind — and
**29 of the 66 append a 16-byte entry to a global registry at `02EAF930`**, tagged `0x4A000000`,
counted by `02EB37B0`.

**That is the mechanism the "builder" framing was hiding.** These are not writers of float tables:
they are constructors that stamp a small header and, for the registered kind, publish the object into
a runtime registry and keep the id it is given back. §10 established what they are *not*; this is what
they are.

### What is still unknown

- [x] ~~What `02EAF930` is a registry *of*, and what consumes it. The counter and the entry layout are
      read; **no consumer of `02EAF930` was traced.**~~ **ANSWERED 2026-09-13 (OPUS): consumers never touch the
      base — they reach each entry through the 32-bit handle codec, and the appender hands them that
      handle.** The last three instructions of `008631E0` are the whole answer: after storing the
      entry it does `lea rcx, [r10 + rax*8]` — **the entry's own address** — then
      `call 0020E620` and `mov [rbx + 4], eax`. **So the object's `+4` is not "a returned id": it is
      the handle OF ITS OWN REGISTRY ENTRY.**
      The codec is a 64-bit pointer compressed to 32 bits against a base in `01F83530`:
      `0020E600(h) = (u32)h + [01F83530]` and `0020E620(p) = (u32)p − (u32)[01F83530]`, exact
      inverses. Anything holding a registered object calls `0020E600(obj->+4)` and reads the entry's
      `+0` and `+8` directly.
      **That is why the base-reference scan found nothing, and the scan was not wrong.** `02EAF930`
      has **exactly one RIP-relative reference in the image** — the `lea r10` at `008631ED` inside
      the appender — and `r10` never escapes it: it is used only to form the two store addresses,
      never stored, passed or returned. The counter `02EB37B0` likewise has 2 references, both in
      the same function. **A consumer does not need the base and never takes it.**
      Scale of the codec, for context: `0020E600` has **4,371 call/jmp sites in 815 functions**, of
      which **714 only resolve** and never encode. This handle scheme is image-wide infrastructure,
      not private to this registry — so resolving a handle is not evidence of consuming *these*
      entries, and no individual consumer of a `02EAF930` row is named here.
      *Control on "nothing else can reach it":* scanning `02EAF800`–`02EB0100` for any reference
      finds 10 referenced addresses of 289, all of them **below** `02EAF930` (`02EAF8E0`, `02EAF8E8`,
      `02EAF8F0`) and each accessed directly as its own global — none is used as a base indexed
      forward into the registry.
- [x] ~~The meaning of the `0x4A000000` tag ORed into every entry's first dword.~~
      **NARROWED 2026-09-13 (OPUS): it is stamped and never tested.** Exactly **one instruction in
      the image carries `0x4A000000` as an immediate** — the appender's own
      `or r8d, 0x4a000000` at `00863207`. There is no `cmp`, `and` or `test` against it, and the
      constant is never loaded into a register, pushed, or stored to memory.
      *Two false trails are recorded because both looked like findings.* A raw byte-scan for the
      dword reported **74 hits in 50 functions**; every one was the sequence `00 00 00 4A` spanning
      an instruction boundary — a zero displacement followed by the next instruction's `4A` REX
      prefix — the same class of error as reading `0xE8` inside operand data as a call. A second,
      instruction-shaped pass reported one memory-operand hit at `003DBDE9`, which disassembly shows
      is inside `mov rax, [rcx + 0xA8]`. **Only the appender survives both.**
      **THE REMAINING BOUNDARY, STATED RATHER THAN GLOSSED:** a consumer could *mask the field*
      (`and eax, 0x00FFFFFF`, or a byte compare on the top octet) instead of comparing the whole
      immediate, and that would not appear in this search. So what is established is that
      **no code branches on the literal `0x4A000000`** — not that the top byte is never examined.
      *Answered since (2026-09-30 pointer, SWE2-CONTRACT): the top byte IS examined, as a command code.* `0x4A` is the
      VIF **MPG** command, and the VIF1 interpreter `0022C970` dispatches on the command byte: its `0x4A` arm stores the
      8-byte payload, an x64 function pointer, at `02068E30[addr]` and appends `addr` to the list at `02088E50`
      (`0022CA3D`–`0022CA60`, [the VIF1 / VU1 layer](../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md)
      command table). So the tag is the command word of an MPG record, read by the interpreter as a byte, which is why
      no whole-immediate compare exists. Tier 1.
- [x] **UQ-46.** The 48 objects with no `memset` size. Their sizes are bounded above by the gap to the next
      pointer but not determined; **the gaps are not claimed as sizes**, since 8 of the 17 measured
      objects are strictly smaller than their gap.
      ***NARROWED 2026-09-17 (FABLE): sizes determined for 42 of the 48 by a second witness, and the memset premise corrected.** The witness is the builder's own last store: for every hub call the census records the highest offset written through the object pointer (`store_extent` in `members/builder-store-extents.tsv`). Over all 74 objects with a next pointer the extent **never exceeds the gap** and **equals it for 66** - objects packed without padding, the shape this section argued from memset; for the 47 in-band objects with no memset and a gap, **42 are exact**. The five that stop short (`02AE06B0` 0x1A0 of 0x2F0, `02AE1DA0` 0x150 of 0x2E0, `02AE4F20` 0xC70 of 0x1A30, `02AE9EE0` 0x150 of 0x390, `02AEC660` 0x10 of 0x200) are bracketed [extent, gap]: an unwritten tail is either padding or a region something else fills, and the builder cannot say which; the last object `02AED330` has no next pointer. **And the premise memset size = object size is wrong for three of the eighteen:** `00492D40`, `00485390` and `0048CE70` call `memset` on INTERIOR sub-buffers (`+0x1E8` for 0x9C0, `+0xBC0` for 0x1F0), so the table's `0x9C0` (`02ADEF40`) and `0x1F0` (`02AE4160`) are sub-buffer sizes, and both objects' written extents are `0xDC0` - exactly their gaps, the two rows the table had as not exact. Three `0xDC0` objects with the same tail (`+0xBA8 = 0x1000404`, `+0xBAC = 0x6c2000d2`, `+0xDB0 = 0x15000000`) are one layout. Static; re-run the script to re-check.*
      ***ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5): the last six sizes are read from each packet's own length.*** Every
      one of these objects is a PS2 packet template, and its DMA cnt tag (`qwc`, id `0x10`) or, where the builder writes
      none, its `UNPACK V4_32` count plus the closing qword states where it ends: `02AE06B0` `0x1A0`, `02AE1DA0` `0x150`,
      `02AE4F20` `0xC70`, `02AE9EE0` `0x150`, `02AEC660` `0x200` (its builder tail-jumps to a second one that fills the
      rest, which the extent census did not follow), `02AED330` `0x130`. The first four tails are the next variable,
      referenced by a function that never touches the object. With the 42 above, all 48 sizes are determined.
      [The UQ-46 record](../../_index/candidates/uq46-packet-ends/README.md), control `uq46_packet_ends.py`, 4 checks.
- [x] ~~**UQ-47.** The 15 builders that call none of the three helpers.~~
      **ANSWERED 2026-09-17 (FABLE).** The fifteen (sixteen with `0047E140`, which the page lists outside the band) are the plain kind with everything inlined: **no call of any kind and no store to any global but their own object** - 47 to 111 stores each, all `mov [obj+off], imm` or `reg` through `rcx` or a register copied from it (`members/builder-store-extents.tsv`, every hub call censused). They neither stamp the `+0..+7` object header (the kind byte `+3` stays zero; three write `[+4] = 0`) nor register, and they do not clear first: they write every byte they need, and for 14 of the 16 the last store ends exactly at the next object (`02AE06B0` and `02AE1DA0` stop short, at `0x1A0` of `0x2F0` and `0x150` of `0x2E0`). What they write is the same packet header the helper-using builders write after their helper: `+8 = 0x3000000` or `0x300001e` and `+0xC = 0x2000000` or `0x20001f1` (eight of each), `+0x18 = 0x1000404` in all sixteen, `+0x1C = 0x6cNN0000` with NN in {11, 12, 14, 17, 18, 19, 1A, 1C}, then immediates and float constants - the pre-built VIF1 packet body BH-1 identified. So the three helpers do not sort the builders into kinds; they are two decisions each builder makes - whether the object carries the header and a registry entry, and whether a range is cleared before being written. What the floats MEAN stays `BH-2`. Static.

*(Pass 22 live-graph completion, 2026-09-15: `002368D0` also calls `CombatAction` `0030CF40`
and `Movement` `00383A20` (2 edges) — the construction path's actor leg reaches combat and
locomotion state on the way through.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Save_Load_Settings — SERVICE.** `0017D4C0` on this page calls `FUN_001c1710`, owned by that layer. What it reaches is **ten bytes**: it swaps zero into `byte[+0x10]` - an atomic clear that keeps the old value - and jumps on; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).
- **Presentation — CLIENT and SERVICE (35 edges).** 21 inbound (Presentation bodies `004B0CF0`, `004825F0`, `004753B0` call page-cited `0022CC20`, `0022CC30`, `0022CC40`); 14 outbound (page-cited `0037DF90`, `0022A0B0`, `0037E0F0` call Presentation bodies `0061D9C0`, `AddMotion_LoadSkeletonMapping` (0036FFF0), `AddMotion_LoadHighModelReplace` (0037CCC0)). Substantive edges include `0018A840` calls `0061D9C0`; `0022A0B0` calls `AddMotion_LoadSkeletonMapping` (0036FFF0); `0022A0B0` calls `AddMotion_LoadHighModelReplace` (0037CCC0); `0022CC20` is called by `004B0CF0`.
- **RNG_Random_Selection — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_Seed` (00379CF0)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **World — SERVICE (1 edge).** 1 outbound (page-cited `0022A0B0` call World bodies `00266D10`). Substantive edges include `0022A0B0` calls `00266D10`.
## Interior citation — frontier hub `008631D0` (2026-09-17, SWE2-EC7)

`008631D0` — 15 B, 48 frontier callers at census; the header initialiser §12 already counts at
40 call sites. Interior verified: [`008631D3`](../../_index/ADDRESS-INDEX.md) is
`mov byte ptr [rcx + 3], 0x10` — the whole body stamps `word[rcx]=dx`, `byte[rcx+3]=0x10`,
`dword[rcx+4]=0` and returns. It is exactly the MPG-record sub-header the VIF1 page describes
(tag `0x10` at `+3`, zeroed tail dword), nothing more.

NOT claimed: byte `+1`/`+2` are never written by this helper — any value there is the caller's
or the emitter `008631E0`'s.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-generated-float-table-builders-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `004795D0` | 116 B | registers `rcx` through an 84-byte registrar with a 4,524-byte callback in `rdx` and `r8d = 0`, then stores `0x3000000` and `0x2000000` to dwords `+8` and `+0xC`, initialises `rcx + 0x10` through a 15-byte header setter with `edx = 2`, and stores `0x1000404` to dword `+0x18`, `0x6C020000` to qword `+0x1C`, `0x302E4000` to dword `+0x24`, `0x412` to qword `+0x28`, and the float bits `0x45000000` (2048.0) to dwords `+0x30` and `+0x34`, `0x43800000` (256.0) to `+0x38` and `0x43600000` (224.0) to `+0x3C` | `004795D9`, `004795E3`, `004795FF`, `0047960B`, `00479630` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-generated-float-table-builders-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `004C2040` | 281 B | zeroes `0xc20` bytes at `rcx` with `memset` (`00861EC0`) and stores immediates: dwords `+8` = `0x3000000`, `+0xc` = `0x2000000`, `+0x18` = `0x1000404`, `+0x1c` = `0x6cbc0000`, `+0x20` and `+0x24` = `0x44fa0000`, `+0x28` and `+0x2c` = `0x45000000`, `+0x30` and `+0x34` = `0x457fa000`, `+0x38` = `0x3f800000`, `+0x4c` = `0x8000`, `+0xbb0` = 1, `+0xbb4` = `0x10000000`, `+0xbc8` = 6, `+0xbd0` = `0x8000`, `+0xbd4` = `0x902a4000`, `+0xbd8` = `0x24242412`, `+0xbdc` = 4, `+0xbec` = `0x50000002`, `+0xbf0` = `0x8001`, `+0xbf4` = `0x10000000`, `+0xc10` = `0x15000000` and `+0xc1c` = 0, and qwords `+0xbb8` = `0xe`, `+0xbf8` = `0xe`, `+0xc00` = 0, `+0xc08` = 8 and `+0xc14` = `0x13000000`; returns 0 | `004C2051`, `004C2056`, `004C20AC`, `004C20DF`, `004C2148` |
| `004DF360` | 219 B | loads the 16-byte cell at `02064E30` + word `[02064DD0]`*16 into `02064C60` and, with `c` = the cell at word `[02064DB0]`, stores word `02064DB8` + `0x8000` (zero-extended) to dword `[c]` and the loaded cell's bytes `+4`..`+0xf` to `c+4`; it stores `w` = word `02064B0C` to word `02064DB8` and `w`+`0x352` to word `02064DB4`, replaced by `w`+`0x2bc` unless `w` equals word `02064DB0` minus `0x2bc`; it calls `rcx(c, rdx, 0)`, then stores word `02064B0C` plus word `02064DB4` to word `02064DB0` and that plus 1 to word `02064DB4` | `004DF386`, `004DF3B6`, `004DF3FC`, `004DF410`, `004DF424` |
