---
system: The thunk layer, and why call counts disagree
category: 24-Compiler-And-CRT-Runtime
status: AUDITED — BU-1 closed 2026-09-18 as NO ADMISSIBLE SOURCE, kind (d): the flag is Ghidra project state the image does not record (proposed FABLE, reviewed and signed OPUS after an independent separating-property sweep over all 835 forwarders)
owner_layer: CodeDomain:Thunk.*
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 35 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-13
audit:
  passes: 3
  last_pass: 2026-09-03
  last_pass_state: opus-thunk-layer-pass-3 - the import stubs resolved to their upstreams and declared as EC-7 family C. The PE import directory holds 538 slots across 30 DLLs; 117 frontier thunks of shape FF 25 (or 48 FF 25) resolve through the IAT to a named DLL and exported symbol, so THE UPSTREAM IS NAMED PER MEMBER rather than per family - 18 DLLs led by api-ms-win-crt-math 34, MSVCP140 20, api-ms-win-crt-runtime 14, VCRUNTIME140 12. TWO UNRELATED INSTRUMENTS DREW THE SAME LINE: this 117 comes from the PE import tables and section 2's Thunk.ExternalImport 117 comes from the checkpoint tag, and they agree exactly - the opposite of what happened to the InternalForwarder count in section 11. THE ONE EXCLUSION IS PRECISE: 00809958 has the identical shape but targets 008C31C0, ONE SLOT PAST the end of the IAT, which the load config names GuardCFCheckFunctionPointer - it is the Control Flow Guard check dispatcher, not an import. And GuardCFFunctionTable/Count are both 0, so the image declares CFG and ships NO valid-target table: a reconstruction needs the indirection to exist and to do nothing
  falsification_passes: 1
  last_falsification: 2026-09-03
  last_falsification_by: repos-d2
  falsification_result: 1 overturned, 5 survived exactly — see section 10
  crossref_clean: true
  reopened_count: 0
function_families:
  - "internal tail-call forwarders | B | members/internal-tail-call-forwarders.tsv | 749 | a forwarder has no behaviour of its own - its complete body is one jmp, so control transfers with every argument register, the stack frame and the return address untouched, and its observable semantics ARE its target's. Could ignorance of this family prevent reproducing FFXII? No, given this page: a reconstruction calls the target directly and the forwarder need not exist - for the 33 members whose target is another member of THIS family it may need up to two extra hops to land (716/30/3 members at chain depth 1/2/3, no cycle, so the collapse always terminates). THE TARGETS ARE NOT DISPOSITIONED BY THIS ROW - as of 2026-09-18, 354 of the 749 distinct targets remain in the frontier (77 A-measured, 318 declared by families - 33 of those being this family's own chained members) and must be explained on their own; the figure is a snapshot and shrinks as peers declare targets."
  - "forward-second-argument tail calls | C | members/forward-second-argument-tail-calls.tsv | 72 | not this game's code: compiler- or template-generated. PROVED BY FORM - 82 members, all 8 bytes, ONE byte image; the entire body is mov rcx, rdx then jmp. CONTROL: 82 members, 82 DISTINCT targets - one each. THE BOUNDARY: each member is a fixed shape around a varying constant or target, and a reconstruction that writes the same declarations gets it from its own toolchain. NOT dispositioned: all 82 targets. This row disposes of 82 argument shuffles and NOTHING they call. 1 member(s) left the family 2026-09-17, since measured as A (A beats a declaration): 0062F4E0."
  - "call-result-then-tail-call adapters | C | members/call-result-then-tail-call-adapters.tsv | 29 | not this game's code: compiler- or template-generated. PROVED BY FORM - 85 members, all 33 bytes, ONE byte image; call one function, pass its result to a second, tail-call. CONTROL: 153 distinct targets over 85 members - each member pairs its own two. THE BOUNDARY: each member is a fixed shape around a varying constant or target, and a reconstruction that writes the same declarations gets it from its own toolchain. NOT dispositioned: all 153 targets. Again: the calling, not the called. 7 member(s) left the family 2026-09-17, since measured as A (A beats a declaration): 00606FD0 00607070 006070D0 006247F0 006BB3C0 006C2630 006C4D90."
  - "external import stubs | C | members/external-import-stubs.tsv | 117 | not this game's code. THE UPSTREAM IS NAMED PER MEMBER, not per family: every one of the 117 is resolved to its DLL and exported symbol through the PE import directory, and the pairs are listed in external-import-stubs-map.tsv beside the members file - 18 DLLs, led by api-ms-win-crt-math (34), MSVCP140 (20), api-ms-win-crt-runtime (14) and VCRUNTIME140 (12). THE BOUNDARY: this game's code ends at the jmp. The stub's own body is one indirect jump through an IAT slot the Windows loader fills at load time; everything past it is the named export's behaviour, documented by its vendor, and a reconstruction links against the same export rather than reproducing it. What is NOT dispositioned by this row is any CALLER's use of an export - passing the wrong argument to _aligned_free is this game's bug, not the CRT's."
---

# The thunk layer, and why call counts disagree

> 689 functions whose entire body is a jump. They are trivial individually and they have caused three
> separate measurement disputes in this database, because **a thunk is a sink in the call graph**.

## 1. What the player sees

Nothing. This document is here for a different reason: **it is the single most common way a
measurement of this binary comes out wrong.**

The engine is full of one-instruction functions that do nothing but jump somewhere else — the seams
where the compiler and linker joined pieces together. They cost a modder nothing to understand and
everything to ignore, because every tool that counts "who calls what" has to decide whether a call
*through* one of these counts as a call to the thunk or a call to the thing behind it. Different
tools answer differently, and this database has three recorded cases of two correct instruments
producing different numbers for that reason alone.

## 2. Native mechanism

### The population

**689 functions carry a `Thunk.*` classification**, and their size distribution is almost degenerate:

| Body size | Count | Form |
|---:|---:|---|
| 5 bytes | 568 | `JMP rel32` — a direct near jump |
| 6 bytes | 108 | `JMP qword ptr [rip+disp32]` — an indirect jump through a table slot |
| 7 bytes | 12 | the same indirect jump, longer encoding |
| 19 bytes | 1 | **not a forwarder at all** — see below |

Three families account for them:

- **`Thunk.InternalForwarder`** (**560**, corrected in §10 — the approximations below do
  not sum to 689) — `JMP rel32` to another function in the image.
- **`Thunk.ExternalImport`** (**117**) — `JMP qword ptr [IAT slot]`. `0019A650` is the canonical shape:
  a single `JMP qword ptr [0x008C20C8]`, and nothing else. These are the import stubs; the slot is
  filled by the loader.
- **`Thunk.DirectTailForwarder`** (12) — `JMP rel32`, **byte-identical in form to the
  InternalForwarders**, and the reason this document exists.

### The one that is not a thunk

> **OVERTURNED in section 10 — there are five, and this section found one because it counted
> the tagged population rather than the binary.** Five 19-byte functions have the identical
> receiver-binding shape; `0028FB40` is the only one carrying a `Thunk.*` tag. One of the other
> four is flagged by neither instrument this document contrasts.

`0028FB40` is the only 19-byte member, and its body is not a forward:

```asm
MOV RCX, qword ptr [0x0209BE80]   ; load a global singleton
ADD RCX, 0xA0                     ; offset to a sub-object
JMP  0x003F8D20                   ; tail-call with that as `this`
```

It **binds a receiver** — it computes `this = g_singleton + 0xA0` and tail-calls. That is a bound
method call, not a forwarder, and classifying it `Thunk.InternalForwarder` records its *shape* rather
than its behaviour. Anyone hooking it expecting a pure jump will be surprised by `RCX`.

### Why the call counts disagree

This is the part that matters beyond this category.

**A thunk is a sink in the call graph.** Measured over the current graph:

```
the 12 DirectTailForwarders:   43 incoming edges,  0 outgoing edges
```

Forty-three calls arrive and nothing is recorded leaving. The `JMP` is not modelled as a call, so a
census that walks the graph **loses the path at the thunk**.

Ghidra compensates for most of them by *modelling* thunk forwarding: it marks
**677 of the 689** with a thunk flag and attributes their callers through to the real target. **It
does not do this for 12** — and those 12 are exactly the `DirectTailForwarder` family, whose
instruction form is indistinguishable from the 528 it does flag.

So two correct instruments give two different answers:

- **A graph census** sees the target's caller list already including the thunk's callers, for the 677.
- **An instruction census** sees the thunk itself as one caller of the target, and separately sees the
  thunk's own callers.

For a function reached both directly and through a thunk, those differ by exactly the thunk's caller
count. That is the mechanism behind the `00313F60` dispute recorded in `AUDIT-LOG.md`: 47 callers of
the 5-byte thunk, 65 of the 78-byte predicate behind it, 110 distinct functions reaching it by either
route — **three correct numbers, three different questions.**

**Neither convention is wrong. Stating which one you used is mandatory.**

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0028FB40` | `Thunk_BindSingletonSubObjectAndTailCall` | 19 B | the only non-forwarding member: loads a global, offsets `0xA0`, tail-calls |
| `0019A650` | import stub (sample) | 7 B | `JMP qword ptr [0x008C20C8]` — canonical `ExternalImport` |
| `00291D40` | direct tail forwarder (sample) | 5 B | `JMP 0x0028E8B0`; **not** flagged as a thunk by Ghidra |
| `002E2560` | direct tail forwarder (sample) | 5 B | `JMP 0x002A7EC0` |
| `004734F0` | direct tail forwarder (sample) | 5 B | `JMP 0x004676C0` |
| `0017CDE0` | internal forwarder (sample) | 5 B | identical form, **is** flagged |

Addresses are Ghidra image base `0x00120000`. Every row above is a function.

### The 12 unflagged `DirectTailForwarder` functions, in full

`00291D40` · `002E2560` · `002EA880` · `002EAA50` · `002ECE40` · `0037D110` · `0037D120` ·
`003844F0` · `003DD220` · `004734F0` · `004735D0` · `00473B20`

All 5 bytes, all `JMP rel32`, all `thunk=false` in the current program.

## 4. Data structures and formulas

There is no structure here — that is the point. The complete content of a thunk is one instruction.

```
InternalForwarder / DirectTailForwarder      5 bytes
  E9 <rel32>                                 JMP target

ExternalImport                               6 or 7 bytes
  FF 25 <disp32>                             JMP qword ptr [rip+disp32]   -> IAT slot
```

### The census identity

For a target `T` reached both directly and through a thunk `K`:

```
graph_callers(T)        = direct_callers(T) + callers(K)     (Ghidra, K flagged)
instruction_callers(T)  = direct_callers(T) + 1              (K counted once, as itself)
distinct_reachers(T)    = |direct_callers(T) U callers(K)|   (either route, deduplicated)
```

Worked example from the audit log — `00377C20` behind thunk `00313F60`:

```
47   distinct callers of the thunk
65   distinct callers of the predicate, excluding the thunk route
110  distinct functions reaching it either way  (not 112 -- two use both routes)
146  call sites in total
```

### Graph edge behaviour, measured

```
12 unflagged DirectTailForwarders : 43 incoming edges, 0 outgoing
5 sampled flagged InternalForwarders : 2 outgoing edges between them
689 Thunk.* total, 677 flagged thunk=true, 12 flagged false
```

## 5. Call chain

```
caller
  -> thunk  (5 or 6 bytes, one JMP)      <- the call graph records the edge INTO here
     -> real target                       <- and records NOTHING leaving
```

**Upstream:** anything. Thunks are distributed across the whole image.
**Downstream:** ordinary functions. The three `DirectTailForwarder` targets sampled here are
`0028E8B0` (19 B), `002A7EC0` (10 B, `NativeAdapter.ConstantFirstArgumentTailCall`) and `004676C0`
(50 B, `NativeInline.NoCall.BitfieldStateAlgorithm`).

**Do not confuse with:**

- **`Phyre.Reflection.PClassDescriptorForType.DestructorThunk`** — 384 further functions that are
  thunks by name but carry a **Phyre** classification, not `Thunk.*`. They are outside this
  document's population, and any census of "thunks in the image" that uses the `Thunk.*` tag will
  miss them.
- **`NativeAdapter.ConstantFirstArgumentTailCall`** — also a tail call, also small, but it *supplies
  an argument*. A thunk changes nothing but the program counter.

## 6. Modding notes

- **Best intervention point:** the thunk, not the target — a 5-byte `JMP rel32` is the easiest hook
  site in the image, and patching it redirects exactly the callers that go through it while leaving
  direct callers untouched. That selectivity is usually what you want.
- **Regenerates itself:** nothing. Import slots are filled once by the loader.
- **Breaks if:**
  - You hook `0028FB40` expecting a pure forward. It sets `RCX` first.
  - You patch an `ExternalImport` stub's *target* rather than its IAT slot. The stub is in `.text`;
    the pointer it reads is not.
  - You assume "no outgoing edges" means "calls nothing". Every thunk in this population is a graph
    sink by construction.
- **Multiplayer / XIIOnline:** thunks are pure code structure with no state; nothing here is
  replicated or replicable. Their only relevance is that a hook placed on a thunk catches a *subset*
  of calls to the target, which is a correctness trap when the two clients disagree about which route
  a call took.
- **Mod compatibility:** two mods hooking the same target — one at the thunk, one at the function —
  will both appear to work and will see different call populations.

## 7. What is not known

- [x] **BU-1 — CLOSED 2026-09-18, `NO ADMISSIBLE SOURCE`** (proposed by FABLE, reviewed and signed by OPUS; see the signature below). **Why Ghidra flags 819 five-byte forwarders and not the 16 byte-identical ones.** *The heading below read "677 and not the other 12" until this closure; those were the tag-census figures, superseded on 2026-09-14 by the 819/16 cross-tabulation in the same bullet and never corrected at the top.* The 16 are byte-identical in form to flagged
      members. **A thunk-to-thunk chain hypothesis was tested and refuted**: of three sampled targets,
      only one is itself a thunk; the others are ordinary functions (`NativeAdapter`, `NativeInline`).
      The cause is unestablished, and this document deliberately records the measured behaviour rather
      than a guess at the heuristic.
      *Narrowed 2026-09-14 (FABLE), not answered: there are 16 unflagged forwarders, not 12, and all of them jump to a leaf
      without unwind data. That condition is necessary but not sufficient.*
      - **Population.** Every listed function whose whole body is a 5-byte `E9 rel32` was cross-tabulated against the thunk
        flag in the parent annotation snapshot: **819 flagged, 16 unflagged**.
        - The 16 are the twelve `DirectTailForwarder`s plus `0035D060`, `0046D100` (`Matrix4x4f_Copy`), `00537170` and
          `007A90A0`. Those four carry older owner tags rather than a `Thunk.*` tag, which is why the tag census saw 12.
      - **The one feature all 16 share: the jump target has no `.pdata` entry.** Every target is a leaf, 3 to 52 bytes
        (`0028E8B0` 19, `002A7EC0` 10, `003D8D60` 7, `003697F0` 13, `001243B0` 3, …).
        - It does not separate the sets: **260 flagged forwarders also jump to leaves without `.pdata`** (109 whose target
          has no other reference, 151 whose target does).
        - Whether the target has other callers does not separate them either. Eight of the 16 targets are reached only
          through the forwarder (*corrected from nine after `AUDITSEM-CONTRA-FABLE-BU1-NINE`*), and 315 flagged targets are too.
      - **So the flag is not a function of the bytes, the unwind data or the reference graph** measured here. It is analysis
        state: most likely the order in which Ghidra created the target and the forwarder, which the image does not
        record. The residue needs the analysis log, not the EXE.
      ***NARROWED 2026-09-17 (FABLE), and a closure proposed for review:** every five-byte `E9 rel32` function in the list, 835 of them, jumps to an address that is itself a function-list entry; none jumps into the interior of a function or outside the list (a pass over `functions.tsv` resolving each displacement). With the earlier findings, that the 16 are byte-identical in form to the 819 flagged ones and that their one shared feature (a leaf target without unwind data) also holds for 260 flagged forwarders, no property of the bytes, of the targets or of the references separates the two sets. What separates them is the state of the Ghidra project when each forwarder was first analysed (a function created before its target existed is not re-thunked, and four of the 16 carry the older owner tags of an early manual pass), which the executable cannot answer. Under the evidence standard's addendum 2026-09-15bk this is a NO ADMISSIBLE SOURCE closure, ~~kind (c)~~ kind (d) *(answered: see the reviewer's signature of 2026-09-18 below; 2026-10-02, OPUS)*; it is filed for review (`FABLE-NOTICE-OPUS-BU1-THUNK-FLAG-IS-PROJECT-STATE`) and the row stays PARTIAL until signed.*
- [x] ~~Why 108 import stubs encode in 6 bytes and 12 in 7. Both are the same instruction.~~ **BU-2 ANSWERED 2026-09-13 (FABLE): they are two different things that happen to share an instruction.** A byte census of every census entry whose whole body is `jmp qword ptr [rip+disp32]` (`ec7/stub_encodings.py`) finds **109 `FF 25`** and **10 `48 FF 25`** bodies (9 through IAT slots, plus the CFG dispatcher `00809958`). The two sets are laid out differently. **The 6-byte stubs are the import libraries' thunks**: 102 of 109 sit exactly 6 bytes after the previous entry, packed end to end with no padding; 82 are in the linker's thunk block `00861E00` up to `00862100`; and their start addresses fall evenly across all eight even residues mod 16. **The 7-byte bodies are compiled functions whose entire code is a tail jump to an import**: 9 of 10 start on a 16-byte boundary and all 10 are followed by `CC` padding, among ordinary compiled code. Examples: `free` `0019C590` and `0078A960` (two copies in two objects), `_aligned_free` `0019C570`, and Bullet's `malloc` `0085E730`. Next to `0019C570`, `0019C580` is the same idiom with an argument zero-extension in front (`mov edx, edx`). The `REX.W` prefix is the form MSVC's compiler emits for a tail jump through memory, and the x64 unwinder recognises that form as an epilog; the import-library thunk needs no unwind recognition. No `.pdata` entry starts at any of the 119, so unwind data does not separate the two sets — layout does. **Not reconciled:** the tag's 108 / 12 partition is by size class, so two of its 7-byte members are bodies of another encoding (§11 already records that).
- [x] What `0028FB40`'s singleton at `0209BE80` is, and what lives at its `+0xA0`.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BU-3): `0209BE80` is the UI / HUD singleton,
      and `+0xA0` is a HUD element that loads the `partytop_8_c` atlas and follows the party's focus actor.*
      - **The singleton** is the one [the UI request router](../../16-UI/Request-Router/ui-request-router.md) records:
        `+0x7EA0` is ticked by the per-frame gate's `0x0800` group, `+0x10F60` / `+0x10F68` hold the open-menu request, and
        `+0x57E0` is the world-object manager. Its pointer is stored by `0028F2F0` (`0028F554`) and `0028F8B0`
        (`0028F8D4`), and 296 rip-relative reads use it.
      - **Every use of `+0xA0`** found by following each load of `[0209BE80]`, matched exactly — *corrected the same day after
        `AUDITSEM-CONTRA-FABLE-BU3-A0-USERS`: the first list matched `0xa0` as a substring and took in two `+0xA0D0` sites*:

        | caller | site | callee |
        |---|---|---|
        | `0028E290` (the gate) | `0028E4BF` | `003F8EC0` |
        | `0028EAB0` | `0028EBD4` | `003F8C70` |
        | `0028FA70` | `0028FA80` | `003F8EA0` |
        | `0028FAF0` | `0028FB11` | `003F8EC0` |
        | `0028FB40` | `0028FB47` | `003F8D20` |

        `0028E43D` (→ `003F80D0`) and `0029045E` (→ `003F80E0`) address **`+0xA0D0`**, a different member.
      - **What the element does.**
        - `0028FB40` → `003F8D20` runs from `00253780` for a message whose `+8` is `0xF` (`0025381A`–`00253825`). Unless flag `+0x52C6`
          bit 0 is set, it loads the resource named by `[01E0C208]`, the string **`partytop_8_c`** (`003F8D45`–`003F8D51`,
          handle at `+0x52B8`), and registers its image (`00181250`).
        - Its per-frame update `003F8EC0` runs from the gate when enable-word bit `0x100` and singleton `+0x10F68` bit 8
          are both set (`0028E4A7`–`0028E4C6`). It resolves the focus handle `022C806C` (`0035BAD0`)
          to a position (`002713E0`, `003F8ED8`–`003F8EE4`). The first time it copies that position into `+0x10` and sets
          `+0x52C6` bit 1; afterwards it eases `+0x10` halfway toward it each frame (`0.5`, `003F8F2D`–`003F8F3D`). With no
          focus actor it clears bit 1.
        - `003F8EA0` clears `+0x52A0` and zeroes `0x1280` bytes at `+0x4020`. `003F8C70` (from `0028EAB0`), when
          `+0x52C6` bit 0 is set, walks `+0x52C0` records of `0x100` bytes from `+0x20` through `003F1290`
          (`003F8C7F`–`003F8CCE`).
      - **So the element tracks the controlled character on screen with a `partytop` texture:** the leader marker is the
        natural reading. What it draws was not observed, and `003F1290` was not read.
- [x] ~~Whether the 384 `Phyre.Reflection.*.DestructorThunk` functions behave identically, and whether
      they too are graph sinks.~~ **BU-4 ANSWERED 2026-09-13 (FABLE): identical, and not sinks.** They share one byte image and one
      target, `00633390`. `graph/edges.tsv` gives each of the 384 exactly one outgoing edge (to `00633390`) and one incoming edge,
      from its exception-unwind funclet. They are the non-deleting destructor that the unwinder calls — not tail forwarders in
      this page's sense — [class descriptors §15](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md).
- [x] Whether any thunk in the image is ever the target of a *data* reference — i.e. address-taken
      rather than called. ~~Not measured here.~~ *(answered: see BU-5 just below - 296 of the 689; 2026-10-02, OPUS)*
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BU-5):* **yes — 296 of the 689 are
      address-taken.** [`members/thunk_address_taken.py`](members/thunk_address_taken.py) searches the whole file for each
      thunk's entry as an 8-byte VA and as a rip-relative `lea` / `mov` operand in `.text`. The control is slot 0 of five
      RTTI-named vtables, and each is found as a qword in `.rdata`. The member list is
      [`members/thunk-address-taken.tsv`](members/thunk-address-taken.tsv).

      | | thunks |
      |---|---:|
      | a qword VA only | 268 |
      | a rip-relative load only (all 37 sites are `lea`) | 25 |
      | both | 3 |
      | **address-taken** | **296** (`InternalForwarder` 269, `ExternalImport` 27) |
      | a 4-byte RVA match only, outside `.pdata` (chance-prone, not counted) | 16 |

      - **Where the qwords are.** 1,393 in `.rdata` and 22 in `.data`: vtable slots, the Lua `luaL_Reg` tables (each
        binding thunk `005A0DC0`… has two), the C++ stream vtables of the MSVC runtime imports (`basic_streambuf`
        `xsgetn` / `xsputn` …), the CFG pointer slots (`_guard_check_icall` ×8), and callbacks such as `free`
        (`0019C590`).
      - **Consequence for this page's argument.** A thunk reached through a vtable or a registration table has callers that
        no direct-call census (Ghidra's attribution or `graph/edges.tsv`) can see. Its zero or low caller count says
        nothing about use.
      - **The twelve `DirectTailForwarder`s have no qword or `lea` reference.** Two have a `.data` dword RVA match, which
        is not counted.


#### The reviewer's signature, and what was actually checked — 2026-09-18 (OPUS)

**Signed.** `BU-1` takes `NO ADMISSIBLE SOURCE` under
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) addendum 2026-09-15bk, **kind (d)** — a
fact about the analysis tool's project state. Bar 4 of that addendum is why this paragraph exists at
all: the status closes a row against a terminal precondition, so it takes a reviewer who is not the
author, and a signature that only says "agreed" would be worth nothing.

**What I ran, independently of the proposal.** The population was rebuilt from the bytes rather than
from the size column — every listed function whose five-byte body decodes as exactly one `E9 rel32`
— and cross-tabulated against the thunk flag: **835 forwarders, 819 flagged, 16 unflagged**, which
reproduces the proposal's figures exactly. Then eleven categorical and three numeric properties were
tested for one that all 16 share and no flagged forwarder does: target is a list entry, target is
itself a five-byte forwarder, target owner, target size, own owner, own name shape, target name
shape, own caller count, target caller count, own section, target section, jump direction, the
`final_no_owner` flag, and whether the entry carries tags. **None separates them.**

**Two of the proposal's own numbers reproduce to the unit, which is why the rest of it is credible.**
819 flagged forwarders have 559 targets carrying a `.pdata` record, leaving exactly the **260**
flagged forwarders whose targets are leaves without one — the figure the bullet above states. And
**0 of the 16** have a target with such a record, so the shared feature is real and, as the page
already says, not sufficient.

> **One property came close and is recorded because it did not make it: all 16 unflagged forwarders
> are 16-byte aligned, against 743 of 819 flagged.** 90.7 % of the flagged set shares it, so it
> separates nothing — but a reviewer who stopped at "I found nothing" would have left it unstated,
> and the next person would run the same test.

**One sentence of the proposal is refused.** It explains the flag as *"a function created before its
target existed is not re-thunked"*. **That explanation makes a prediction and the image reverses
it.** If analysis creates functions as it moves forward, the forwarder whose target did not yet
exist is the one jumping FORWARD — so the unflagged set should skew forward. Measured: **3 of 16
unflagged jump forward (18.8 %), against 458 of 819 flagged (55.9 %).** The unflagged set skews
**backward**, three to one against the prediction.

**That does not disturb the closure, and the difference matters.** `NO ADMISSIBLE SOURCE` says the
remaining question is not answerable from any artefact this project admits; it does not say *why*
the tool decided as it did, and it must not smuggle in a mechanism as if it had been established.
**The row keeps the finding — the flag is project state the image does not record — and drops the
account of which project state**, which is exactly the part no admissible source can supply.

*Method note, since this signature is itself a precedent: bar 3 of the addendum asks for the negative
that was actually checked. For a kind-(d) row that means a separating-property sweep by someone other
than the author, stated in full, including the properties that came close. Asserting "nothing
separates them" without one would be the shrug the status exists to prevent.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 689 `Thunk.*` functions; 568/108/12/1 by body size | census over a freshly regenerated `DumpFullCoverageGraph.java` at the GN checkpoint | 1 |
| `ExternalImport` is a single `JMP qword ptr [IAT]` | complete disassembly of `0019A650` — one instruction | 1 |
| `DirectTailForwarder` is a single `JMP rel32`, identical in form to `InternalForwarder` | complete disassembly of `00291D40`, `002E2560`, `004734F0` | 1 |
| `0028FB40` binds a receiver and is not a forwarder | complete 3-instruction disassembly | 1 |
| 677 of 689 carry Ghidra's thunk flag; the 12 that do not are exactly the `DirectTailForwarder` family | census over the graph's `thunk` column, cross-tabulated against the tag | 1 |
| The 12 have 43 incoming and **0 outgoing** graph edges | edge census over the current graph | 1 |
| The `00313F60` numbers (47 / 65 / 110 / 146) | recorded in `AUDIT-LOG.md` from a two-instrument reconciliation by a peer session | 11 |

**A hypothesis tested and refuted, recorded because it was attractive.** The obvious explanation for
the 12 was that they are **thunk-to-thunk chains**, which Ghidra might decline to model. The first
sample supported it — `00291D40` jumps to `0028E8B0`, itself a flagged thunk. The next two refuted
it: `002E2560` → `002A7EC0` (`NativeAdapter`, not a thunk) and `004734F0` → `004676C0`
(`NativeInline`, 50 bytes of real code). **One confirming sample is not a pattern.**

**Superseded readings:** ~~none — this is the document's first version.~~ *(answered: see §10 - the 2026-09-03 pass overturned readings of this document; 2026-10-02, OPUS)*

## 10. Falsification pass 1 — 2026-09-03, session `repos-d2`

**Previously unattacked** (`passes: 0`), and attacked by a session that had made **both** of the
failure modes this document describes in the same night — a registration census that missed a tail
`jmp`, and an edge scan that counted local branches as edges. Program state: parent `2ed8affb…`,
snapshot `46f02e26…`, EXE `73461d08…`, project `proj_hd2` / `GFZ_HD2`, `CHECKPOINT VERIFIED`.

### Overturned — the receiver-binder is not unique, and the reason is this document's own thesis

§2 says *"`0028FB40` is the only 19-byte member, and its body is not a forward."* True of the
689 `Thunk.*`-tagged functions. **False of the binary.** Scanning every ledger body for the exact
three-instruction shape `mov rcx,[rip+disp]; add rcx,imm; jmp rel32`:

| address | body | Ghidra thunk flag | `Thunk.*` tag |
|---|---:|---|---|
| `0028E220` | 19 B | **yes** | no |
| `0028E860` | 19 B | **yes** | no |
| `0028E8B0` | 19 B | **yes** | no |
| `0028FB40` | 19 B | yes | **yes** — the one this document found |
| `0028FB60` | 19 B | **no** | **no** |

**Five, not one.** `0028E8B0` loads the same global `0209BE80` as `0028FB40` and binds a different
sub-object (`+0x8FA0` against `+0xA0`), so these are a family of bound-method entry points over one
singleton, not an oddity.

**The failure is the one this document exists to warn about, one level up.** §2 measured the
*tagged population* and stated a property of the *binary*. A census restricted to `Thunk.*` cannot
see a receiver-binder that was never tagged — and **`0028FB60` is flagged by neither instrument this
document contrasts**, so it is invisible to the graph census *and* to the tag census, while being
byte-identical in shape to the one that is documented.

**And there is a two-hop chain the section does not anticipate.** `00291D40` — one of the twelve
unflagged `DirectTailForwarder`s — jumps to `0028E8B0`, which is a flagged receiver-binder, which
jumps to `002BE020`:

```
00291D40  (unflagged forwarder)  -> 0028E8B0  (flagged receiver-binder)  -> 002BE020
          graph loses the path here          graph forwards here
```

**Each hop defeats a different instrument, and the receiver binding is invisible to both.** A graph
census stops at hop 1; a census that models thunk forwarding walks through hop 2 and never records
that `RCX` was rewritten on the way.

### Survived — every measurement, exactly

| Claim | Result |
|---|---|
| **689** functions carry a `Thunk.*` classification | **SURVIVED, exact** |
| size distribution **568** / **108** / **12** / **1** at 5 / 6 / 7 / 19 bytes | **SURVIVED, exact on all four** |
| Ghidra flags **677 of 689**, and the 12 it does not are the `DirectTailForwarder` family | **SURVIVED, exact** — the twelve unflagged are precisely the twelve listed in §3 |
| the 12: **43 incoming edges, 0 outgoing** in the graph | **SURVIVED, exact** |
| `00313F60`: **47 / 65 / 110** | **SURVIVED, exact** — see below |

**The `00313F60` figures are exact under a call-only convention, and the pass demonstrates the
document's thesis on the document's own example.** Counting `call` *and* `jmp` gives **47 / 66 /
111** — one more on each of the last two, and the extra caller is **the thunk itself**, which
reaches `00377C20` by `jmp`. Remove it and both figures land exactly on 65 and 110.

> **Two instruments, three numbers, one binary, and the difference is entirely whether a `JMP` counts
> as a call.** That is the sentence this document is about, and it reproduces on its own worked
> example without anything being wrong in either measurement.

### Two figures restated with their predicates

- **Family counts.** §2 gives *"~528"*, *"~105"* and 12, which sum to **645**, not 689. The exact
  tag counts are **`InternalForwarder` 560, `ExternalImport` 117, `DirectTailForwarder` 12**, summing
  to 689 with no remainder. The tildes concealed a 44-function gap in a document whose subject is
  measurement discipline.
- **Edges against sites.** The twelve's *43 incoming edges* is a count of distinct caller→callee
  pairs. The instruction census finds **45 incoming `call`/`jmp` sites** across the same twelve, and
  **12 outgoing** where the graph records 0. Both are right; they answer *how many relationships* and
  *how many instructions*.

### What was tried and failed to break anything

- **Tried to break 689, 677/12, and the size histogram** against the ledger directly. All exact.
- **Tried to make the twelve unflagged functions something other than the `DirectTailForwarder`
  family.** They are exactly that set, and exactly the twelve §3 enumerates.
- **Tried to find a thirteenth unflagged thunk.** There is none in the tagged population — the
  extras found above are outside it, which is a different claim and is reported as one.
- **No banned evidence.** No `.pdata`/`.xdata`/unwind/EH. The five receiver-binders are grouped by an
  exact instruction-sequence match, not by lying in `0028Exxx`–`0028Fxxx`.

## 9. Related

- [`../../_index/AUDIT-LOG.md`](../../_index/AUDIT-LOG.md) — the `00313F60` reconciliation and the standing rule on stating your selector
- [`../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`](../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md) — measured the same shape-vs-identity problem in a larger population
- [`../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md) — the other place caller counts need their selector stated

## 11. Audit pass 2 - 2026-09-13 (OPUS): the tag-based census under-counts by 181

*(Static only - every body in the 34,270-function census classified by its own bytes, with the
`Thunk.*` tag used only as the thing being tested. Nothing executed.)*

### What reproduces exactly

| section 2 claim | measured |
|---|---:|
| functions carrying any `Thunk.*` tag | **689** |
| of those, 5-byte `JMP rel32` | **568** |
| of those, 6-byte `JMP qword ptr [rip+disp32]` | **108** |
| of those, 7-byte | **12** |

**Four figures, four exact matches.** The partition in section 2 is sound *over the population it
partitions*.

### ✖ But that population is not the thunk layer

Counting by **bytes** instead of by tag, over the same 34,270 non-funclet bodies:

> **749 functions have a complete body of exactly five bytes, `E9 rel32`.** The tag knows about
> **568** of them. **181 byte-identical forwarders carry no `Thunk.*` tag at all** - a **32%
> under-count**, and they are invisible to every census that starts from the tag.

Where the untagged 181 live instead: **137** under `CategoryExitV106`, 9 under
`ABI_UNRESOLVED_DEFAULT`, 9 under `CategoryExitV112`, 7 under `GFZ.V120.FinalNoPrimaryOwner`, 6
under `ABI_CURATED_TYPED`, and the rest scattered.

**This document already knew the failure mode and had measured it once.** Section 10's overturn
records that the 19-byte receiver-binder section was wrong *"because it counted the tagged
population rather than the binary"*, and found one function. The same instrument error, measured at
scale, is worth **181**.

### Controls, and one that shaped the family definition

- **Every one of the 749 targets is a real function entry.** Zero dangling, zero self-references.
  A mis-identified body would land somewhere that is not an entry, and none does.
- **749 forwarders, 749 distinct targets** - one-to-one. No two forwarders share a target.
- **None of the 749 is measured as A**, so declaring them takes nothing out of the explained count.

> **The five-byte rule earns its tightness.** A looser *"body ends in a `jmp`"* rule would have
> swept in **16** bodies of `xor ecx, ecx; jmp` and **12** of `xor edx, edx; jmp`. Those are not
> forwarders: they **bind an argument to zero** before tail-calling, so their semantics are *not*
> their target's. They are also **untagged**, which is why a shape census has to define the shape
> and not the family name. This is exactly the trap section 10 found in the 19-byte receiver-binder,
> and it is 28 more instances of it.

### And a miss of my own, in the same class

My filter for the 7-byte thunks matched only `FF 25` and found **10** of the **12** the tag reports.
The page is right and my pattern was incomplete - the tagged 7-byte set is not one encoding.
**Recorded because it is the same error as the page's: a filter that encodes one form of a thing
and then reports a count of the thing.**

### EC-7: the family is declared

The 749 are declared in this page's frontmatter as **`function_families: internal tail-call
forwarders | B | 749`**, with the enumerated population in
[`members/internal-tail-call-forwarders.tsv`](members/internal-tail-call-forwarders.tsv) and the
selector recorded in that file's header. `check_dispositions.py` accepts the row.

**The bar B has to clear, answered here:** a forwarder's complete body is one `jmp`, so control
transfers with every argument register, the stack frame and the return address untouched, and its
observable semantics **are** its target's. Could ignorance of this family prevent reproducing FFXII?
**No, given this page** - a reconstruction calls the target directly and the forwarder need not
exist at all.

> **What this row does NOT disposition: the targets.** 713 of the 749 targets are themselves in the
> frontier and are untouched by this declaration. **Dispositioning a forwarder says nothing about
> the function it forwards to**, and a reading that treats 749 as 749 functions explained is exactly
> the citation-volume error `EC-7` exists to prevent.

**Not claimed.** The 6- and 7-byte import stubs are **not** declared here - an import stub's
behaviour is the loader's and the upstream library's, which is a **C** disposition needing the
upstream named, and that is a separate row somebody should write. The `Thunk.*` tag itself is not
corrected; it is the checkpoint's, and this pass tests it rather than repairing it. Nothing executed.

## 12. Audit pass 3 - 2026-09-13 (OPUS): the import stubs, resolved to their upstreams

*(Static only - the PE import directory, IAT and load-config directory parsed from the shipping EXE,
and every 6/7-byte indirect thunk resolved through them. Nothing executed.)*

Audit pass 2 left the import stubs undeclared, saying *"an import stub's behaviour is the loader's
and the upstream library's, a C disposition needing the upstream named, and that is a separate row
somebody should write."* This is that row.

### The upstream is named per member, not per family

The import directory holds **538 slots across 30 DLLs**. Resolving every frontier thunk whose body
is `FF 25 rel32` (or `48 FF 25 rel32`) through the IAT gives **117 stubs**, each with a DLL and an
exported symbol:

| upstream | stubs | | upstream | stubs |
|---|---:|---|---|---:|
| `api-ms-win-crt-math` | 34 | | `kernel32` | 5 |
| `MSVCP140` | 20 | | `imm32` | 3 |
| `api-ms-win-crt-runtime` | 14 | | `d3d11`, `xinput9_1_0`, `api-ms-win-crt-stdio` | 2 each |
| `VCRUNTIME140` | 12 | | `iphlpapi`, `d3dcompiler_47`, `dinput8`, `dbghelp`, `dxgi`, `api-ms-win-crt-utility`, `api-ms-win-crt-locale` | 1 each |
| `api-ms-win-crt-heap` | 9 | | | |
| `api-ms-win-crt-string` | 7 | | **total** | **117** |

> **Two unrelated instruments drew the same line.** This 117 comes from the **PE import tables**;
> section 2's `Thunk.ExternalImport` count of **117** comes from the **checkpoint's tag**. Neither
> derives from the other, and they agree exactly - which is a stronger result than either count
> alone, and the opposite of what happened to the `InternalForwarder` number in section 11.

**That the largest single upstream is `api-ms-win-crt-math` is worth noticing**, and it is the same
observation section 12 of
[animation channel binding](../../22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md)
arrived at from the other side: scalar maths in this image goes through the CRT by call, which is
why an instruction census of `sqrt*` sees none of it.

### ⚠ The one that is not an import, and it is not an import for a precise reason

**`00809958`** has the identical 7-byte shape and **does not resolve**. Its target is `008C31C0`,
and the IAT runs `008C2000`..`008C31C0` - **one slot past the end**. The load-config directory
settles what it is:

```
GuardCFCheckFunctionPointer      +0x70 = 008C31C0     <-- this slot
GuardCFDispatchFunctionPointer   +0x78 = 008C31C8
GuardCFFunctionTable             +0x80 = 0
GuardCFFunctionCount             +0x88 = 0
```

So `00809958` is **`jmp qword ptr [__guard_check_icall_fptr]`** - the **Control Flow Guard** check
dispatcher, patched by the loader, not an import stub. It is **excluded from the family** and the
members file says so by address.

> **And the CFG table is empty.** `GuardCFFunctionTable` and `GuardCFFunctionCount` are both **0**:
> the image declares the CFG pointers and ships **no valid-target table**, so the loader points the
> check at a no-op. A reconstruction needs the indirection to exist and needs it to do nothing;
> reproducing a CFG check that actually validates would reject indirect calls the shipped game
> makes. The forwarder family's `0017E7D0 -> 0016D6A0 _guard_check_icall` is the image's own local
> body for the same mechanism.

**One off-by-one slot separates an import stub from a security-runtime pointer**, and a filter that
had matched `FF 25` shape alone would have declared it as a library call.

### EC-7: declared

The 117 are declared as **C** in this page's frontmatter, with
[`members/external-import-stubs.tsv`](members/external-import-stubs.tsv) and the per-member upstream
pairs in
[`members/external-import-stubs-map.tsv`](members/external-import-stubs-map.tsv).

**What this row does not disposition:** any **caller's** use of an export. Passing the wrong
argument to `_aligned_free` is this game's bug and stays this game's problem; the row disposes of
the stub, not of the calls through it.

**Not claimed.** The 30 DLLs include 12 whose stubs are all A-measured or otherwise outside the
frontier and are simply not in this population. The import **slots** (538) are not dispositioned -
a slot is data, and this family is about the 117 functions that jump through one. Nothing executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Audio — MECHANICAL.** The 3-byte ICF body `001243B0` has 56 Audio-filed callers, and its thunk `007A90A0` has five
  more. This is the page's own point: a folded body's caller list spans unrelated code.
- **Items_Equipment_Shops_License, Movement, Spawn_Encounter_Lifecycle, ActorEntity, Party and
  CombatAction — CLIENT.**
  The field action-permission bit (`00377C20`) and its 5-byte thunk `00313F60` are read by:
  - the unequip path and the owned-count query;
  - nine movement bodies;
  - `Spawn_ValidateCandidateDistanceToPlayers` and `SpawnLifecycle_CheckAndRetireByNativeRange`;
  - eleven ActorEntity bodies — `BattleUnit_ApplyUnitDefinition`, the category-parse helpers
    (`00233D70`, `00233EA0`, `00237D80`) and the spawn/despawn path — all consulting the same
    bit through the thunk;
  - three Party bodies — `PartyControl_RecomputeSuppressionFromLeaderBattleState`, `0031AC00`
    and `00304180`, the last reaching the body `00377C20` directly;
  - twenty CombatAction bodies (`BattleUnit_HandleActorTimelineEvent`,
    `BattleUnit_HandleActionTimelineEvent`, `BattleAction_ApplyKnockbackImpulse`,
    `BattleUnit_CommitAction`, `BattleUnit_ProcessPendingActionSelectionQueue`,
    `BattleAction_IsTargetEligibleForCurrentAction`, `BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout`,
    `BattleTarget_ComputeEligibilityBlockMask`, `Battle_BuildActionTargetSet`, …) — combat consults
    the same permission bit before and during action resolution (SWE2-CONTRACT 2026-09-15).

  **The thunk and the body are both called directly**, which is the call-count disagreement this page explains.
- **Presentation — CLIENT and MECHANICAL.** The other cited thunks and small bodies are rendering-side:
  - `0019C580` (9 B, `_aligned_malloc`), used by `AddMotion_LoadHighModelReplace`, `AddMotion_LoadSkeletonMapping`,
    `AddMotion_ApplyBonePose`, `Skeleton_UpdateFinalPoseAndCombatLook` and a 9,695-byte body;
  - `Matrix4x4f_Copy` (`0046D100`, 5 B), used by the `CharacterRenderRecord_*` LOD and transform functions and
    `SkeletonModelWork_PropagateParentSecondaryTr…`;
  - `00537170` (5 B), used by `SkeletonModelGroup_UpdateFinalPoses`;
  - `003F1290` (56 B), used by four bodies;
  - `00181250`, used by a 667-byte body;
  - `0028E290`, `0028EAB0` (`"Gaussian Filter"`, `"display UI 2"`), `003F8C70` and `003F8D20`, which call into a dozen
    Presentation bodies;
  - the permission bit, read by four presentation functions.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** Both entries named `FieldData_GetActiveFieldRecordBit15` are called by status bodies. `00313F60`'s callers are the primary-resource recovery accumulator's two sides; `00377C20`'s are `BattleStats_ChangeStatusAndProcessSideEffects`, `BattleStats_RemoveStatusesFromMaskAndRecompute` and `BattleUnit_RunPeriodicCombatMaintenance`. That split is this page's case in point: callers divide across the two entries.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT.** `BattleStats_ModifyHPAndProcessLethalState`, owned by that layer, calls `00377C20` on this page. That caller is the HP-modification entry point: it resolves the owning unit for both the source and the target, reads the target unit's `dword[+0x48]`, and decodes its flags argument bit by bit - bits 0, 1, 2, 4 and 5 each select a separate behaviour; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT.** `BattleUnit_UpdateEngagementStateFlag`, owned by that layer, calls `00377C20` on this page. That caller is the engagement test, which reads the actor's `+0x698` block and tests `+0x3C` OR `+0x64` against its own mask; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**InputGameplay — CLIENT.** `FUN_00313a00`, owned by that layer, calls `00377C20` on this page. That caller is a state query that tests the pointer at `[02089350]` and the global equality predicate `00253B90`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `00377C20` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — MECHANICAL (SWE2-CONTRACT 2026-09-15, 8 edges).** Same permission-bit fan-in as the CombatAction entry:
`00313F60` is shared with `BattleEnmity_WriteForCombatantId`/`BattleEnmity_WriteAllCombatantIds`/
`BattleEnmity_AdjustOtherRelevantCombatants`/`BattleUnit_RebuildPerceptionCandidateCache`/
`BattlePerception_RefreshCandidateCacheGeneration`; `00377C20` is shared with
`BattleUnit_SelectAndCommitNextAction`/`AiOrder_EvaluateAndResolveActionTarget`/
`AiOrder_EvaluateTargetSelector`. The two thunks are consulted across the AI layer — mechanical
count on the same accessors.

**Save_Load_Settings — SERVICE (SWE2-EC7-163, 2 edges).** `00245020` is called
by `0057E4D0` (`SaveWrite_OperationStateCallback`), and `0032E620` — a helper
this page's `002C8EE0` builder runs — is called by `002EF300` on that layer.
Mechanical fan-in on shared accessors.

**Script_VM_Native_Bridge — SERVICE (SWE2-EC7-163, 5 edges).** `0032E620` is
called by `0050DFE0`, and `00377C20` is called by `00344740`/`00352FA0` (+2
more) on that layer — the script bridge reaches the same shared helpers the
thunk page measures. Mechanical.

## The `002EA880`/`002EAA50`/`002ECE40` exclusive-subtree cluster — all 3 roots bound (SWE2-FRONTIER, followup queue)

Three plain `jmp` thunks — each root is 5 B, and its census member is the
target body:

| root | member (target) | interior |
| --- | --- | --- |
| `002EA880` | `003D8D60` | [`002EA880`](../../_index/ADDRESS-INDEX.md) |
| `002EAA50` | `003B5440` | [`002EAA50`](../../_index/ADDRESS-INDEX.md) |
| `002ECE40` | `0037B2C0` | [`002ECE40`](../../_index/ADDRESS-INDEX.md) |

## The `003DD220`/`00473B20` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

| root | member (target) | role | interior |
| --- | --- | --- | --- |
| `003DD220` | `0037DB70` | `dword[02EBF3C0] = ecx` — 7-byte setter | [`0037DB70`](../../_index/ADDRESS-INDEX.md) |
| `00473B20` | `00290C50` | `0209BE80` base, `and dword[+0x10F68], 0xFFFFFFDF` — bit-5 clear | [`00290C57`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.


## SWE2-EC7-64 update (2026-09-19) - `0031AC00`

`0031AC00` (139 B) is a Party suppression body - `00313F60`/`00322C50` plus `02EBF190`. Interior anchor `0031AC29` (a `00322C50` call).


## SWE2-EC7-101 update (2026-09-20) - `00296670` + `00296260` + `00296240` measured

`00296670` (100 B) is the `0x110`-stride clear loop
`0028E8D0` and `0028F2F0` call: `edx` records are walked
through the `00273A20`/`00245020` gate pair, then each
takes `+0xF0`/`+0x100` dwords and the `+0xF8` qword
zeroed - the counted reset the thunk arms run on the
record array.
Interior anchor `002966A4` (the field clears).

`00296260` (20 B) and `00296240` (20 B) are the twin
global-clear trampolines `0028F2F0` and `0028F8B0` call:
`00861EC0` tails zero `0xC0` bytes at `0209C240` and
`0x300` bytes at `0209BF40` respectively - the two
fixed-size state resets the layer exposes.
Interior anchors `00296262` and `00296242` (the
`lea`s).

## SWE2-EC7-103 update (2026-09-20) - `00273B40` measured

`00273B40` (89 B) is the intrusive-list unlink
`0028F2F0`, `0028FA50`, `00290DF0` and `00291B90`
call: the node at `rdx - 0x20` is unlinked - a
null `+0x18` back-link writes the node's `+0x10`
forward into `[rcx]` (and when `r8` is the list
head, `+0x18` or `+0x10` becomes the new
`[rcx + 0x10]`), the `+0x18`/`+0x10` neighbours
are cross-linked, and the node's two links are
zeroed - the detach the thunk walks run.
Interior anchor `00273B6C` (the relink).

## SWE2-EC7-106 update (2026-09-20) - `00249180` measured

`00249180` (35 B) is the forwarding
thunk `002467A0`, `00253780`,
`00280750`, `002808D0`, `0029DC90`,
`002CEAE0`, `003158B0`, `0035C5B0`
and `003C1F00` call: it moves
`[rsp + 0x60]` into the argument
stack and calls `00249210`, then
writes the second incoming stack
argument `[rsp + 0x68]` into
`[rax + 0x10]` and
answers `qword[rax + 8]` - the
call-and-patch shim that explains why
the thunk layer's call counts never
match its entry count.
Interior anchor `00249196` (the
`[+0x10]` write).

`002C8EE0` (348 B) is the builder `00253780` calls: loops filling 7-wide stack records (`edx = rdi + 0x74`, `0024AB90` per entry) into `0209E640`, with `002C9040` taken by address and `00249810`/`0032E620` finishing - the thunk-adjacent record constructor.

Interior anchor `002C8F2F` (function `002C8EE0`).

`0017D260` (12 B) is the `_aligned_malloc` call-site shim: `r9d = -1`, `r8d = 0`, tail `jmp 0019C580` - forwards `(rcx, rdx)` with the two trailing argument slots defaulted.

Interior anchor `0017D267` (function `0017D260`).

`00584740` (16 B) is the `_aligned_malloc` shim variant `001A11B0` (the 1.31 MB singleton) uses: `r9d = -1`, `r8d = 0`, `edx = 0x10`, tail `jmp 0019C580` - the alignment-16 preset sibling of `0017D260`.

Interior anchor `0058474B` (function `00584740`).

`0019C580` (9 B) is the `_aligned_malloc` import thunk itself: `mov edx, edx` zero-extends the argument then `jmp qword[008C2B60]` through the IAT - the compiled-function tail-jump form BU-2 distinguishes from the packed import-library stubs.

Interior anchor `0019C582` (function `0019C580`).

`00210EC0` (11 B) is the `malloc` call-site shim the ensure-singleton stubs route allocations through: `r8d = -1`, `edx = 0`, tail `jmp 0085E730` (the Bullet-compiled `malloc`) - the same default-two-args idiom as `0017D260`.

Interior anchor `00210EC6` (function `00210EC0`).

`001A1990` (112 B) is the three-way string compare: unpacks both SSO forms (`[+0x18] >= 0x10` selects the heap pointer, else `+0x10` inline), `00861ED2` memcmps the shorter length, and a tie breaks on length order - `-1`/`0`/`+1`.

Interior anchor `001A19CB` (function `001A1990`).

`001A5A80` (114 B) is the vector reallocation validator before `00210EB0`: rejects `r8 > 0x1FFFFFFFFFFFFFFF`, and for `r8*8 >= 0x1000` vetoes the `rdx` block through four `008C2DA8` invalid-parameter traps - misalignment (`& 0x1F`), `[rdx-8]` out of range, an offset below 8 or above `0x27` - then tail-enters the sibling free.

Interior anchor `001A5AED` (function `001A5A80`).

`002467A0` (249 B) is the lazy registry init `00253780` calls: under the `0208EA88` null-guard it allocates the five `01E0C218`..`01E0C288`-described objects via `0024A4E0(x, 2)` into `0208EA90`/`0208EA98`/`0208EAA0`/`0208EAA8`/`0208EAB8`, then builds the outer registrar through `00249180(rcx, 7, 0xD6, 3, 1, 00246A10)` and stores it at `0208EA88` - once per process

Interior anchor `00246838` (function `002467A0`).

`002808D0` (161 B) is the lazy request pair `00253780` runs on `0209AC30`: `+0x3D0` gets `00249180(rcx, 7, 0xD3, 3, args)` when empty and `+0x3C8` the same with kind `0xD4`, then tail `00280750` - the thunk layer's two-slot loader registration

Interior anchor `0028090A` (function `002808D0`).

`00280750` (381 B) is the request builder `002808D0`'s lazy pair wraps: a stack-cookie body that lays an eleven-pointer packet of `01E0C1xx` thunk cells (`009152A0`/`009152B0`/`009152C0`/`009152D0`/`009152D8`/`009152E8`/`00915338`/`00915348`/`009153C0`/`009153D0`) on the frame, lazy-fills the ten `[rcx+0x338..+0x388]` slots through `0024A4E0(2)`, then fires ~~`00249180(rsi, 7, 3, 0xD7, proc 00280740)`~~ `00249180(rsi, 7, 0xD7, 3, 1, 00280740)` *(corrected 2026-10-02, OPUS: `00280750+0xEB` sets `edx = 7` and `00280750+0xFC` sets `r8d = 0xD7`, then `r9d = 3` and `[rsp+0x20] = 1`; `00280750+0x111` is the call, in the same order as `002467A0`'s)*

Interior anchor `00280817` (function `00280750`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Application, CoreRuntimeScheduling and Platform — MECHANICAL, four edges.** The thunks and wrappers this page counts
have ordinary callers:
- the 16-byte `_aligned_malloc` wrapper `00584740`, from `001A98B0` (the map-art context) and `00650D40`;
- `001A11B0`, from the bootstrap `0017D4C0`;
- `0028E290`, which calls `001EDE80`.

The page's subject is why call counts disagree, not what these callers do.

*Tier 2: ledger names, sizes and `edges.tsv`; no new body read (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-thunk-layer-and-why-call-counts-disa-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002C9040` | 21 B | stores dword 0 at `0209E638 + ecx * 0x10` (`ecx` sign-extended), that is, at `+0x00` of the `0x10`-byte record `ecx` of the table at `0209E638` | `002C9043`, `002C904A`, `002C904D` |
| `002CEAE0` | 82 B | when bit `0x2` of byte `+0xD3C` of the object at qword `0209AC30` is set, calls `00249180(rcx, 7, byte +0xB2D of that object + 0x10, 2)` with `rcx` passed through unchanged and 1 and 0 as the fifth and sixth (stack) arguments, and stores the returned qword at `+0x3C0` of the object at qword `0209AC30` (re-read); when the bit is clear it returns without the call or the store | `002CEAEB`, `002CEAF2`, `002CEB01`, `002CEB1A`, `002CEB26` |
| `0037B2C0` | 41 B | when `ecx` < 5 (signed compare), stores the floats `xmm1`, `xmm2` and `xmm3` at `+0x40`, `+0x44` and `+0x48` of the `0x50`-byte record `ecx` (sign-extended) of the table at `02EBF420`; when `ecx` >= 5 it returns without a store | `0037B2C3`, `0037B2D6`, `0037B2DC`, `0037B2E2` |
| `003B5440` | 37 B | compares bit 0 of byte `02B40518` with the whole of `ecx`; when they are equal it returns without a store, otherwise it replaces bit 0 of that byte with bit 0 of `cl` (other bits kept), stores the byte back to `02B40518` and tail-jumps to `003B4FD0` | `003B544C`, `003B544E`, `003B5457`, `003B5459`, `003B545F` |
