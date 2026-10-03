---
system: Why the unowned code has no owner
category: 99-Unresolved-Residual
status: AUDITED
owner_layer: none - this document measures what has no owner
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: functions.tsv + edges.tsv census; 8-byte-aligned pointer scan of all
    non-.text/.pdata/.reloc sections; capstone reads of the eight highest fan-in bodies
last_reviewed: 2026-09-02
audit:
  passes: 11
  last_pass: 2026-09-02
  last_pass_state: remainder recounted after the four ScriptVM tables were enumerated (GN158, project GFZ_HD2)
  crossref_clean: true
  reopened_count: 0
  falsification_passes: 1
  last_falsification: 2026-09-02
  last_falsification_by: repos-9e
  last_falsification_state: GN158 checkpoint, residual sha c5d4b7f7..., project GFZ_H9E
  falsification_result: 5 overturned, 6 survived - the central 65.8% finding holds; see section 15
  followup: section 16 reads the .data population, certifies the counts against .reloc, and withdraws one section 15 characterisation
---

# Why the unowned code has no owner

> **24,116 functions - 70.4 % of the executable - are classified but unexplained.** This document
> asks why, and the answer is not the one the previous pass gave. **Two thirds of the unexplained
> code has no caller because it is never called by name: it is reached through a pointer stored in
> a table.** The call graph cannot see it, and no amount of caller-side analysis will ever explain
> it.

**For a player, almost nothing here is visible** - this is the plumbing under every system the rest
of the database describes. One measured thing is visible, and it is a ceiling: the engine keeps a
**fixed table of 112 records** for one kind of object and falls back to the heap only when that
table is full (section 6). What those records hold is *not* established here, and this document
does not guess.

---

## 1. RETRACTION: pass 51's headline was wrong

[Pass 51](../../22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md) measured 2,904 call
edges reaching Phyre from unowned functions, found that **no documented game subsystem calls Phyre
at all**, and concluded:

> *"the game/middleware seam runs entirely through code that is classified but not understood... so
> 'understand the seam' and 'understand the generic shape classes' are the same task."*

**The first clause stands. The conclusion does not.** It was drawn from edges counted in one
direction only. Measured in the other direction, the generic shape classes are not a Phyre-facing
adapter layer:

| unowned functions in the 11 generic groups | ~~15,498~~ ~~15,896~~ **15,975** (corrected S15; re-derived GN161 2026-09-14) |
|---|---:|
| of those, **>= 80 % of their callers are Phyre** | **335 (2.1 %)** *(317 when written; a literal re-run over the current set gives 335 — none of the 128 GN161-classified functions qualify, so the drift is the earlier set growing, not the advance)* |
| bytes in that set | 77,111 |

**Two percent.** The shape classes are overwhelmingly *not* Phyre-adjacent. The 2,904 edges are
real, but they are edges, not functions - a small number of heavily-called helpers produces most of
them, and those helpers turn out to be Phyre's own internals rather than a seam between the game and
Phyre (section 5).

So **"understand the seam" and "understand the shape classes" are two different tasks**, and the
seam is by far the smaller of them. The claim is withdrawn from the Phyre document.

### How the error was made

Pass 51 grouped the *callers* of Phyre functions and found them unowned. That is a true fact about
2,904 edges. It silently became a claim about ~11,848 *functions* *(the Native* shape classes at GN161)*. **A census of edges is not a
census of functions** - one function called 864 times contributes 864 edges and one function.

This is the fifth recorded [instrument-shaped blind spot](../../_index/EVIDENCE-STANDARD.md), and
the first where the instrument was correct and the *unit of measurement* was the error.

---

## 2. The census: what "unowned" actually contains

Grouped by `CodeDomain`, unowned functions split cleanly by mean body size:

| | functions | bytes | mean |
|---|---:|---:|---:|
| **Glue-shaped** (`Thunk`, `NativeLeaf`, `NativeAdapter`, `CxxObjectLifecycle`, `CompilerGeneratedCpp/CFG` — see note) | 5,282 | 178,492 | **34 B** |
| **Substantial** (`NativeRoutine`, `Runtime`, `Boundary`, `NativeInline`, `Presentation`, `NativeDispatch`) | 10,693 | 2,664,024 | **249 B** |

> *Re-derived at GN161 2026-09-14: the written `CompilerGenerated*` glob now also matches the
> 3,895 `CompilerGeneratedEH` funclets, which the EH doc owns separately — the glue figure keeps
> this table's original set (Cpp + CFG). Including EH, glue is 9,177 functions / 238,406 B / 26 B.*

A 34-byte mean across 5,282 functions is a category that explains itself: thunks average **5 bytes**
and `NativeLeaf` **17**. A 249-byte mean across 10,693 does not. Two groups stand out for having a
shape label over real behaviour - `Boundary` at a **780-byte** mean and `Presentation` at **1,093**.

**Stated as measured.** Mean body size groups these; it does not identify them. Any role read into a
group from its size alone is a lead, not a finding.

> **Population, added 2026-09-02 by falsification pass 1 (S15) — it was missing.** Every count in
> this section and in section 3 **excludes the 3,891 `CompilerGeneratedEH` exception funclets**.
> The exclusion is defensible and was never stated, and without it none of these figures
> reproduces: the glue row derives as 9,174 functions / 231,893 bytes and lands on 5,283 / 172,156
> only after the funclets come out. The `substantial` row is unaffected and reproduces exactly.

---

## 3. The finding: most of it is never called by name

Of all unowned functions, **10,924 have zero direct callers** in the edge list. That is not a
mystery to be solved one function at a time - it is a property of the instrument. Scanning every
8-byte-aligned qword in the image's data sections for values equal to a function entry address:

```
pointer slots found in data:   29,000 in .rdata,  3,015 in .data,  8 in _RDATA   <- answered 2026-10-02, OPUS: _RDATA has no base relocation, so 0 slots ("The _RDATA 8 were never real")
distinct functions addressed:  10,472        <-- CORRECTED 2026-09-02, was 7,331
```

> **Slot counts corrected 2026-09-02 by falsification pass 1 (S15).** They read
> `27,392 / 204 / 8` until that pass. **The correction noted below had been applied to the
> distinct-function count and not to the slot counts beside it** - those were still the
> restricted scan's output, reproduced exactly by re-running with the restricted candidate set.
> `.data` was understated about 15-fold.
>
> > **The reason offered for why that matters is backwards - corrected 2026-09-02.** It read
> > *"which matters because `.data` slots are runtime-built dispatch tables rather than static
> > vtables."* The opposite is true, and the fact that settles it was already in this database when
> > that sentence was written.
> >
> > `.data` runs `01DF0000`..`02F97530` but its raw size is `0x18E400`, so it is **file-backed only
> > up to `01F7E400`** - **91.2 % of `.data` has no file image** and is zero at load. **All 3,015
> > counted slots lie below that boundary**, so every one of them is *statically initialised in the
> > file*. A slot that is genuinely built at runtime is zero in the file and is **invisible to this
> > scan by construction** - the audio registry singleton `01FD36A0`, the audio request gate
> > `02091098` and the transform workbench at `022D8F00` are all above the boundary and contribute
> > **nothing** to the 3,015.
> >
> > So the 3,015 are **writable tables with a static initialiser** - patchable, but not
> > runtime-built - and the population of runtime-built slots is **not measured by this scan at
> > all**. The `01F7E400` boundary was already derived, from the same PE section fields, in
> > [the shared transform workbench](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md)
> > §8. **The contradicting fact was in the database before the claim was written.**

> **Correction.** The first scan silently restricted its candidate set to functions carrying a
> `CodeDomain` tag, undercounting by 3,141. The **65.8 %** ratio below is unaffected - both sides of
> that intersection came from the same restricted population - but the standalone count was wrong.
> Of the 10,472, **6,883 sit in an RTTI-named vtable**; see
> [the RTTI vtable object model](../../00-Engine-Core-Runtime/Object-Model/rtti-vtable-object-model.md).

Applied to the 10,924:

| | functions | share |
|---|---:|---:|
| zero direct callers, **address-taken in data** | **7,185** | **65.8 %** |
| zero direct callers, **not address-taken** | 3,739 | 34.2 % |

**Two thirds of the uncalled code is reached through a pointer in a table** - vtables, dispatch
tables, callback slots. `.rdata` holds 29,000 such slots and `.data` a further 3,015 (corrected, S15). A `call` never names these functions, so
an `E8`-based edge list reports them as unreachable, and every caller-census technique this database
has used is blind to them by construction.

Their groups: `Phyre` 2,953, `NativeAdapter` 882, `Runtime` 739, `NativeRoutine` 617,
`NativeDispatch` 501, `CompilerGeneratedCpp` 304, `NativeLeaf` 291, `Thunk` 260.

### What remains genuinely dark

**3,739 functions have no caller and no address in any table.** These are the real unknown:

| `Phyre` | 1,743 |
| `NativeRoutine` | 514 |
| `Runtime` | 361 |
| `NativeAdapter` | 243 |
| `Boundary` | 173 |
| `CompilerGeneratedCFG` | 145 |
| `NativeLeaf` | 91 |
| `NativeInline` | 89 |

`CompilerGeneratedCFG` (145, mean 12 bytes) is explainable as a category - control-flow fragments.
The rest are not, and **`Phyre` at 1,743 is nearly half of the dark set**.

### Limits of this measurement - read before using the 65.8 %

- The scan matches any qword in the VA band `0x00120000`-`0x01000000` that **exactly equals a
  function entry**. A coincidental integer can match. Exact-entry matching makes that unlikely, but
  the number is an **upper bound on address-taking**, not a certified count.
- It reads only **8-byte-aligned** qwords. Vtables are aligned, so this is correct for vtables and
  would miss a packed unaligned table.
- **Address-taken is not "called".** A pointer in a table proves the function is *reachable*, not
  that the game ever reaches it. Some of the 7,185 are dead vtable slots.
- It says nothing about *which* table. Identifying the owning vtable is the next step, not this one.

---

## 4. What this changes about the remaining work

The database's coverage debt was being counted as one number. It is three, and they need different
instruments:

| | functions | how it gets explained |
|---|---:|---|
| Glue-shaped, self-explaining as a category | ~5,283 | already explained - record the category, not the bodies |
| **Reachable only through data tables** | **7,185** | **vtable and dispatch-table reconstruction** - caller analysis cannot touch it |
| Called, substantial, unexplained | ~10,613 | ordinary reading, ranked by fan-in |
| Dark: no caller, no address | 3,739 | unknown; `Phyre` is 47 % of it |

**The 7,185 is the discovery.** It was previously inside "accounted for only" with everything else,
and it is the one part of the debt that the tools in use could never have reduced.

---

## 5. Specimens: the eight most-called unowned functions, read

Read at tier 1 rather than inferred - 5,635 call sites between them.

| address | callers | bytes | what it does |
|---|---:|---:|---|
| `00584730` | **2,309** | 10 | `if (p) _aligned_free(p);` |
| `00811130` | 864 | 72 | resize a 16-byte-slot array, zero-filling growth |
| `00812960` | 803 | 83 | four-call fixed sequence with phase arguments 1 then 2 |
| `0080F420` | 537 | 158 | slot-count bounds check against a **1,000,000** limit |
| `008119F0` | 461 | 122 | read a slot's type tag: `*(dword*)(slot+8) & 0xF` |
| `001EDF00` | 230 | 14 | store one vtable pointer, return `this` |
| `0017D260` | 228 | 12 | set two arguments, tail-jump |
| `00244F50` | 203 | 175 | fixed-table allocator with heap fallback (section 6) |

**The most-called function in the executable is a null-guarded aligned free.** Ten bytes:

```asm
00584730  test rcx, rcx
00584733  jne  _aligned_free        ; 0019C570
00584739  ret
```

Its 2,309 callers are the only place in this census where owned game code appears at all - `Input`
39, `Resource` 23, `Audio` 2. Everything else is unowned.

### A 16-byte tagged-slot stack

Four of the eight operate on one structure: an array of **16-byte slots** with a **type tag in the
dword at `+8`, masked `& 0xF`**, a moving cursor at `[obj+0x10]`, a slot array reached through
`[obj+0x20]`, and a hard cap of `0xF4240` = **1,000,000 slots**. Negative indices address from the
top of the stack, positive from the base, and one fixed address is compared as an invalid-slot
sentinel.

> **AR-1 ANSWERED 2026-09-02 — and this section should never have called it a lead.**
> **It is Lua's value stack**, and this database had already established every piece of it before
> this pass read the four functions from scratch:
>
> | | |
> |---|---|
> | `00811130` | **`lua_settop`** |
> | `008119F0` | **`lua_type`**, with `index2addr` inlined — "7 constants matched" |
> | stride `0x10` | `TValue { Value value_; int tt_; }` — 16 bytes on 64-bit |
> | cap `0xF4240` | **`LUAI_MAXSTACK` = 1,000,000** |
> | `0xFFF0B9D8` | `-0xF4628` = **`LUA_REGISTRYINDEX` = -LUAI_MAXSTACK - 1000** |
>
> Every observation below matches: the `& 0xF` type mask is Lua's basic-type extraction from `tt_`,
> the negative-index-from-top handling is `index2addr`, and the zero written at `+8` while growing is
> `LUA_TNIL`. See
> [embedded Lua and Phyre object bindings](../../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md).
>
> **The Phyre attribution below is wrong, and the reason is worth keeping.** 87 % of the callers
> carry a `CodeDomain.Phyre.*` label because Phyre's script bindings are the heaviest **user** of the
> Lua C API — not because Phyre owns the stack. **A caller census identifies the busiest consumer,
> never the owner.**

**Whose stack it is, is a lead, not a finding.** 87 % of `00811130`'s callers (751 of 864) carry a
`CodeDomain.Phyre.*` label, as do 747 of 803 and 404 of 461 for the others - so these are almost
certainly **Phyre's own runtime**, unlabelled because the leaf helpers carry none of the RTTI or
naming evidence the Phyre classification was built from. Which Phyre sub-group owns it is
unverified. **AR-1.**

That is also why the pass-51 conclusion inverted: these functions sit *below* Phyre, not between
Phyre and the game.

---

## 6. A fixed table of 112 records with a heap fallback

`00244F50`, ~~203 callers~~ 206 calling functions *(corrected 2026-10-02, OPUS: 231 `call` sites and 16 tail-`jmp` sites, 247 in all, rel32 sweep)*, read in full:

```c
if (size == 0) size = 0xC0;
if (size <= 0x120) {
    rec = *(void **)0x0208EA58;                  /* table base -- CORRECTED 2026-09-08 */
    for (i = 0; i < 0x70; i++, rec += 0x120)     /* 112 records, stride 0x120 */
        if (!(rec->flags_40 & 0x4000) && rec->byte_A2 == 0) {
            rec->byte_A2 = 1;                    /* claim the slot */
            init(rec, size, arg2, arg3, /*pooled=*/1);
            return rec;
        }
}
rec = allocate(size);                            /* 002497B0 - table full or oversized */
init(rec, size, arg2, arg3, /*pooled=*/0);
return rec;
```

Measured facts: **112 records**, **stride `0x120` bytes**, table pointer at **`0x0208EA58`**, default
size **`0xC0`** when the caller passes 0, and requests **larger than `0x120` bypass the table
entirely**. A slot is free when bit `0x4000` of `+0x40` is clear *and* the byte at `+0xA2` is zero;
claiming it sets `+0xA2` to 1. The fifth argument to the initialiser distinguishes the two paths.

> ### The table pointer was wrong, and everything around it was right — corrected 2026-09-08
>
> This section read **`0x02093958`**. The address is **`0x0208EA58`**:
>
> ```
> 00244F7F   48 8b 1d d2 9a e4 01     mov rbx, qword ptr [rip + 0x1E49AD2]
>            next instruction 0x00244F86  +  0x1E49AD2  =  0x0208EA58
> ```
>
> **`0x02093958` appears nowhere in the function's 175 bytes.** Every RIP-relative operand in
> the body was re-resolved with a tool and there is exactly one. The difference is `0x4F00`,
> which is not a transposition.
>
> **Nothing else in this section moved.** 112 records, stride `0x120`, default `0xC0`, both
> free-slot conditions, the claim writing `+0xA2`, and the fall-through that sends an oversize
> request and an exhausted table to the same heap arm all reproduce exactly. **One address in
> an otherwise-correct reading**, found by a block that set out to re-derive the whole function
> and discovered the census had already read it. [a 512-byte widget that registers itself once](../../16-UI/Widget-Object-Model/a-512-byte-widget-that-registers-itself-once.md) §5.

**What the records hold is not established.** The GFZ names the initialiser
`GenerationBoundRecordInitializeAndInitialNotify`, which is suggestive and is not evidence. Per the
standard, a name constrains; only the writers decide. **AR-2.** *(Answered since — `AR-2`, 2026-09-12, under *Open questions* below: small UI widget objects of many classes, from the factory's callers.)*

**Why it matters anyway:** 112 is a hard number in a shipped engine, and the fallback path means
exceeding it changes allocation behaviour rather than failing. If these records back anything a
player can multiply on screen, that ceiling is a real limit - which is exactly why identifying them
is worth doing, and exactly why it must not be guessed.

---

## Open questions

- [x] ~~Which Phyre sub-group owns the 16-byte tagged-slot stack.~~ **ANSWERED — it is not Phyre's,
      it is Lua's value stack**, and this database had documented it before this pass re-read it.
      **AR-1.**
- [x] ~~What the 112 `0x120`-byte records hold. Requires reading the writers, not the name.~~
      **AR-2 ANSWERED 2026-09-12 (FABLE), from the factory's callers:** the records hold **small UI
      widget objects of many classes**, not one record type. `00244F50(size, ctor, arg)` has **231
      call sites** image-wide; each passes a byte size in `ecx` and its own constructor in `rdx`
      (`lea rdx, [rip + …]` to a function that itself calls the factory back for its parts). **145 of
      the 231 request `0xC0`–`0x120` bytes** and are served from the 112-slot table when a slot is
      free (`+0x40` bit 14 clear and `+0xA2` zero); the other 86 — `0x128` up to `0x179E0` — and any
      request when the table is full take the heap arm (`00244FB0`, `002497B0`). So the table is
      the **pool behind every small widget** (menus' rows, cursors, labels, icons: the constructors
      at `00227E20`–`00583990` are the UI layer's, [the 512-byte widget page](../../16-UI/Widget-Object-Model/a-512-byte-widget-that-registers-itself-once.md)) and 112 is the ceiling on
      *simultaneously live small widgets*; a 113th falls through to the heap rather than failing.
      The GFZ's "generation-bound record" name describes the slot header, not the payload. *Not done:*
      naming the 145 pooled classes one by one. **AR-2.**
- [x] ~~Reconstruct the `.rdata` vtables so the 7,185 table-reachable functions become attributable.~~
      **DONE 2026-09-02** - 2,286 vtables recovered and named via RTTI; **3,784 previously-unowned
      functions attributed to exactly one class**. Attribution is safe only for the 62 % of functions
      that appear in a single class's vtable; the rest are inherited into several.
      [The RTTI vtable object model](../../00-Engine-Core-Runtime/Object-Model/rtti-vtable-object-model.md).
      **AR-3.**
- [x] ~~Why functions have neither a caller nor a stored address.~~ **ANSWERED 2026-09-02** — their
      address is **materialised in code by `lea reg,[rip+disp]` and never stored**, so no scan of data
      can see them. Covers **3,129 of 3,451 (90.7 %)**; EH funclets, recovered structurally, cover most
      of the rest in a population that includes them. Section 12. **AR-4.**
- [x] ~~What the 431 truly unreferenced functions are.~~ **ANSWERED — retained PPFX library code**,
      established by per-function source-file provenance: **41 of 41** tagged residual functions cite a
      `.cpp` that referenced code in the same cluster also cites. **One translation unit per cluster.**
      Section 13. **AR-4b.**
- [x] ~~The one cluster that is not a mixture: `006F16E0`–`006F1C00`.~~ **ANSWERED — it is not a dead
      object and the "zero referenced" was a metric artifact.** Eight of the twelve are byte-identical
      generated accessors over a field block that live code reads 5–27 times per slot; **435 of 435**
      residual functions have live code on both sides. Section 14. **AR-4c. AR-4 is closed.**
- [x] ~~What the `.rdata` 4-byte RVA tables are that reference 691 of the dark set.~~ **ANSWERED
      NEGATIVELY** — measured against a control, the RVA scan runs at **1.16x chance by position**.
      The 691 is withdrawn and the dark set is **not** reduced by it. Section 11. **AR-4a.**
- [x] Whether any of the 7,185 are dead vtable slots never dispatched at runtime. **AR-5.** *(closed — the register row is WITHDRAWN.)*
      *Narrowed 2026-09-27 (FABLE, Claude Opus 5.5): no slot can be shown dead from the image alone.* Every slot index
      the 2,286 RTTI vtables use (0–76) is named by at least one fixed-slot `call` or tail-dispatch `jmp`. Every
      vtable is referenced, so every class can be constructed. What remains is a per-site type-flow analysis, or a
      runtime observation, and a capture can never show "never". [Record](../../_index/candidates/ar5-vtable-dispatch/README.md).

## 10. AR-4 narrowed: five mechanisms ruled out (2026-09-02)

Pass 52 left **3,739** functions with no caller and no stored address. Re-measured and attacked
mechanism by mechanism, the number is **3,453** and five explanations are eliminated.

| mechanism tested | covers |
|---|---:|
| `E8` direct call edges | 0 — the set is defined by their absence |
| an 8-byte pointer in data, **at any alignment** (not just aligned) | +12 only |
| **`E9`/`EB` jump targets** — tail calls and thunk forwarding | **336 (8.9 %)** |
| **`/OPT:ICF` byte-identical twins** where the twin is reachable | **45 (1.3 %)** |
| **the CFG guard function table** | **0 — the table does not exist** |

**The unaligned scan is worth recording as a near-null result.** Re-running the pointer scan at every
byte offset instead of every 8 found **12 more functions** out of 10,984. Data pointers in this image
are aligned; that hypothesis is closed.

**ICF folding fails as an explanation.** Only 65 of the 3,453 are byte-identical to *any* other
function, and only 45 have a twin that is itself reachable. The folded `ret 0` at `0016D6A0` is real
but it is not a general mechanism.

**The CFG table does not exist**, which this database already knew — see
[image hardening](../../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md):
`GuardFlags = 0x00000100` is `CF_INSTRUMENTED` **without** `CF_FUNCTION_TABLE_PRESENT`,
`GuardCFFunctionTable = 0`, and the check pointer at `0x008C31C0` resolves to the three-byte `ret 0`.
**The code was compiled with `/guard:cf` and shipped with the enforcement removed.**

That document also already explains **145 members of this dark set**: every
`CompilerGeneratedCFG` function is a guard-check stub, *"all 145 of them — 1,740 bytes — are no-ops
at runtime."* Nothing references them because nothing needs to.

### What the remaining 3,308 look like

```
median size      26 bytes
<= 16 bytes      1,509  (44 %)
Phyre            1,739  (50 %)
NativeRoutine      370      Runtime  355      NativeAdapter  192      Boundary  162
```

**Tiny, numerous, half of them Phyre.** A 26-byte median rules out most of the interesting
explanations: these are not dead subsystems, they are individually trivial functions.

**`.pdata` was deliberately not used.** A 4-byte RVA scan finds 24,209 functions in `.pdata` and
1,298 of the dark set — and it means nothing. **`.pdata`/`.xdata`/unwind data is banned as evidence
in this database**: an entry there says a function has a prologue worth unwinding, not that anything
reaches it. Reporting that 1,298 as coverage would have been the banned inference wearing a new hat.

A 4-byte RVA scan of `.rdata` does cover **691** of the dark set, but **what those tables are is not
established**, and presence in an unidentified table is not reachability. **AR-4a.**

### Method note — rule 13, fourth occurrence

This pass parsed the PE Load Config directory, extracted `GuardCFFunctionTable`, `GuardCFFunctionCount`
and `GuardFlags`, and resolved the check pointer — **all of which the hardening document already
recorded, field by field, including the same hex values.** Four tool calls spent re-deriving
published work.

**Rule 13 keeps being learned and not applied.** Reading it is not the same as running it. The
practical form: **before investigating an address, a structure or a term, grep the corpus for it** —
the same reflex `check_names.py` made mechanical for names.

## 11. AR-4a: the RVA scan was noise — measured against a control (2026-09-02)

Section 10 reported that a 4-byte RVA scan of `.rdata` covers **691** of the dark set, while warning
that "presence in an unidentified table is not reachability". **It is worse than that: most of the
scan is chance, and the 691 is withdrawn.**

### The control

Two sets of the same size (34,270), drawn from the same `.text` RVA range with the same 16-byte
alignment. One is the real function entries. The other is **deliberately chosen not to be functions.**
Both are scanned against the same dwords.

| scan | real | control | ratio |
|---|---:|---:|---:|
| **4-byte RVA, `.rdata`** (5,551,614 dwords) | 54,655 positions | **46,966** | **1.16x** |
| **8-byte VA, all data sections** | 32,019 positions | **301** | **106x** |

**A set of addresses that are provably not functions matches 46,966 positions.** The real set's 54,655
is 1.16 times that. **By position count the RVA scan carries essentially no signal**, and any
statement of the form "N of the dark set are referenced by an `.rdata` RVA" is unsupported.

### The distinct count tells a more interesting story

| | real | control |
|---|---:|---:|
| distinct values hit at least once | **8,732** | **906** |

That is **9.6x**, not 1.16x. The two ratios disagree because the control's positions concentrate on
few values — 46,966 positions across only 906 distinct means a handful of unlucky constants matched
thousands of times each.

So **real 4-byte RVA references do exist** — 9.6x above chance on distinct functions — but with a
**false-positive floor near 10 %**, and the scan cannot say *which* individual function is genuinely
referenced. For a set-level claim it is weak evidence; for the reachability of any one function it is
none. **AR-4a is answered negatively: the 691 does not reduce the dark set.**

### What this validates

The same control **vindicates the 8-byte pointer scan at 106x**, which is the instrument behind this
document's central measurement — that 65.8 % of apparently-uncalled unowned code is address-taken in
data — and behind the vtable recovery. **That number was load-bearing and had never been controlled.
It is now.**

### The rule this produces

**Control every scan that matches values against a large set.** The standard already requires
positive controls for *zeros* — "before believing no references, run the instrument against something
known to be present". This is the mirror image and was missing: **before believing a non-zero count,
run the instrument against something known to be absent.**

A scan matching 34,270 values against 5.5 million dwords will hit by chance. Whether 54,655 hits mean
anything is not answerable by looking at 54,655; it is answerable only by looking at what a control
set scores. **Two scans in this pass differed by a factor of ninety in how much they could be
trusted, and nothing about their output said so.**

## 12. AR-4 ANSWERED — the address is materialised in code, never stored (2026-09-02)

Five mechanisms were eliminated in section 10 and a sixth was withdrawn as noise in section 11. **The
answer is a seventh that was never on the list, and it is the simplest one:**

> **`lea reg, [rip + disp]` — the function's address is computed into a register and never written
> anywhere.** It is not a call, not a jump, and not a stored pointer. The value exists only in a
> register until some callee stashes it at runtime, so **every scan of *data* is blind to it by
> construction**, no matter how carefully controlled.

### Measured against this document's own dark set

```
dark set (no E8 caller, no stored 8-byte pointer at any alignment, no E9/EB jump target)   3,451
   of those, address materialised by a `lea` in code                        3,129   (90.7 %)
   remaining                                                                  322
```

**One mechanism explains 90.7 % of a set that six others could not touch.**

The covered subset is the profile this document reported as characteristic of the dark set —
**median 21 bytes, 48 % under 16, 56 % Phyre** — confirming that the dark set *was* the LEA
population all along, not a mixture.

### The residual, and what it looks like

The 322 that remain have **nothing in common with the 3,129**:

| | dark set | residual |
|---|---:|---:|
| median size | 26 B | **93 B** |
| under 16 bytes | 44 % | **1 of 322** |
| Phyre | 50 % | **0** |

**A different population entirely**, and no longer tiny generated glue. Ledger domains:
`NativeRoutine` 132, `NativeAdapter` 102, `NativeDispatch` 25, `ThirdParty` 25.

### Independent corroboration, and an exact reconciliation

This was solved in parallel by a **peer analysis session** working read-only, which reached the same
mechanism from the other direction and additionally recovered **EH funclets structurally** — parsing
`.pdata` → `UNWIND_INFO` → language-specific data to get funclet *entry points*, **not** using the
presence of a `.pdata` entry as evidence, which remains banned. It reported LEA + EHFUNC covering
**94.6 %** of its reconstruction and a residual of **431**.

**The two residuals reconcile exactly.** This document's population **excludes `Unwind@` and
`Catch_All@` entries at load**, so EH funclets were never in its dark set — which is precisely why
LEA alone reaches 90.7 % here while LEA+EHFUNC were both needed there. **322 versus 431, from
populations that differ by exactly the funclets.** The residual profiles agree to the unit: median 93
vs 92, zero Phyre in both, essentially nothing under 16 bytes in either.

### Three further results from that work, adopted here

**The 4-byte RVA scan is noise everywhere, not just in `.rdata`.** Section 11 measured 1.16x against
a control there; the peer's independent control measured **0.9x in `.text`**. **The technique is
withdrawn from this database's evidence set entirely.**

**Jump tables are not a mechanism.** Structural MSVC switch recovery — locating `jmp reg` ← `add
reg,base` ← `mov reg32,[base+idx*4+T]`, with entry counts taken from the preceding `cmp`/`ja` bound
rather than guessed — found **506 dispatch sites and 5,540 distinct targets, of which zero are
function entries**. Jump-table targets in this image are always interior case labels. A clean
negative, and it explains why a raw 4-byte scan of `.text` found anything at all.

**Nothing in this image reads code as data.** Every rip-relative reference to a function entry is a
`lea`; the "other rip-relative" class is empty.

**And this document's own 106x control reproduced at 108x** on an independently constructed control
set. That is the pointer scan behind the 65.8 % measurement, now confirmed twice.

### What is still not established

The 322/431 have **no incoming reference of any kind** — no call, jump, `lea`, stored pointer, funclet
record or throw record. They cluster in the **high end of `.text`** where MSVC places statically
linked library code, **interleaved with referenced functions**: in the densest cluster 136 of 240
functions are residual, the other 104 reached by ordinary calls.

**The natural reading is retained-but-unreferenced library code** — object files pulled in for the
symbols the game does use, carrying their unused siblings along. **That is a lead and is not
established.** The honest statement is that **431 functions are statically unreferenced by every
mechanism either analysis has modelled**, and the mission's bar is met for the other 33,700-odd.
**AR-4b.**

## 13. AR-4b ANSWERED — retained PPFX library code, established by per-function provenance

The 431 truly unreferenced functions are **the unused half of live PPFX translation units.** That was
recorded as a lead in section 12; it is now established, and by evidence far stronger than similarity.

### PPFX tags its own functions

PPFX logs through string literals of the form:

```
..\src\GPU\GPURenderTexture.cpp(%d) : Feb 18 2016 PPFX ERROR:
```

**The executable contains 528 of them, citing 19 distinct source files**, all stamped `Feb 18 2016`:

| file | tags | | file | tags |
|---|---:|---|---|---:|
| `gpuposteffect.cpp` | 202 | | `ppfx.cpp` | 46 |
| `gpuinterfacedevice.cpp` | 56 | | `gpudepthoffield.cpp` | 37 |
| `tinyeffect.cpp` | 53 | | `ppfxrendertotexture.cpp` | 13 |
| `gputextureutil.cpp` | 50 | | `gpurendertexturearray.cpp` | 12 |

**That gives many functions a per-function provenance tag** — which is a categorically better
instrument than any similarity metric, because a mismatch would announce itself.

### The decisive test

**Every cluster resolves to a single dominant source file**, and the residual and referenced halves
cite *the same* file:

```
residual functions carrying a source-file tag                          41
whose file is ALSO cited by a REFERENCED function in the same cluster  41   (100 %)
per cluster: 18/18, 6/6, 12/12, 3/3, 1/1, 1/1
```

**Not one residual function cites a translation unit its live neighbours do not.** The clusters are
not "one library each" — they are **one `.cpp` each**.

Corroborating, and only corroborating: callee-set overlap runs at **6.5x** unrelated clusters and
reaches **71 % of a same-codebase baseline** built by splitting each cluster's *referenced* half in
two at random. And the residual functions **call** the live ones interleaved with them — 66 of 99 in
the `ppfx.cpp` cluster. **They are inside the same call graph; they are simply never called.**

### The mechanism, and a clean illustration

**PPFX was linked per translation unit.** The game uses part of each `.cpp`'s API; the unused
remainder of the same file rides along. The `TFXString.cpp` cluster shows it exactly: its residual
functions reference `GPUMULTISAMPLE_10_SAMPLES` through `..._13_SAMPLES` — **an enum-to-string table
where the game only ever needs some of the values**, with the rest of the stringifier emitted because
the translation unit was.

Sampled bodies are ordinary unused API: `FUN_007067E0` (90 B, `GPUPostEffect.cpp`) validates two
fields, logs at line `0xC33`, and returns `E_FAIL` — a textbook uncalled public method.

### Three caveats, kept

1. **Only 41 of 433 carry a tag.** The 100 % is of the checkable ones. The other 392 rest on cluster
   membership plus callee similarity — **established for the tagged, strongly supported for the rest**.
2. **Three clusters fall well below the same-codebase baseline** (0.35, 0.36, 0.52). Two of them do
   have source-file confirmation, so they are likely the same story with sparser call sharing, **but
   the metric does not carry them alone**.
3. ~~**One cluster is a genuine exception.** `006F16E0`–`006F1C00` holds 12 residual functions and no
   referenced function at all — a solid unreferenced run…~~ **RETRACTED — see section 14.** The
   "no referenced function" count was **produced by the metric's own definition**, not by the data.
   There are no isolated dead regions in the residual. **AR-4c.**

**AR-4b answered.** The residual is retained library code, and the largest structural question this
category ever held is closed apart from a 0x520-byte run.

## 14. AR-4 CLOSES — and the last "dead object" was a metric artifact

### The `006F16E0` run is generated accessors over live data

**Eight of the twelve are one accessor block.** Verified here: all eight are **32 bytes with a single
distinct instruction shape**, differing only in one displacement.

```asm
006F1850   push rbx / sub rsp,0x20
           call FUN_007142F0          ; singleton getter
           mov  rbx, rax
           call FUN_00714560          ; ensure / init
           mov  rax, [rbx + 0x22270]  ; <- THE ONLY THING THAT VARIES
           add  rsp,0x20 / pop rbx / ret
```

```
006F1850 +0x22270   006F18B0 +0x22260   006F1910 +0x22298   006F1970 +0x222B0
006F1880 +0x22278   006F18E0 +0x22268   006F1940 +0x222A8   006F19A0 +0x222B8
```

The ledger's own tag is `NativeAdapter.DoubleCallThenSavedResult` — it already described them.

**Every callee is live**, and **so are the fields**: the twelve slots at `+0x22260`..`+0x222B8` carry
**5 to 27 references each from live code**, and four of them (`+0x22280`, `+0x22288`, `+0x22290`,
`+0x222A0`) have **no accessor at all** yet 3–10 live references. **The engine reads all twelve
inline; someone generated getters for eight of them that nothing calls.** Redundant wrappers around
live data — the PPFX story again, not a different one.

### The correction: "N = 0" could not have come out any other way

Section 13's cluster metric defined each span as `[first residual, last residual]` and counted live
functions **strictly inside** it. **For any run whose residual functions are contiguous, that count is
zero by construction.** `R=12, N=0` was not evidence of isolation — **it was the measurement
reporting its own definition back.**

The run is bracketed by live code immediately on both sides: `006F1650` before, `006F1CD0` after.

Replacing the span metric with the question actually intended — *does each residual function have live
code on both sides in address order?*:

```
residual functions with live code on both sides : 435 / 435   (100 %)
longest unbroken residual runs : 24, 21, 15, 12, 9 x4, 8, 7 x2, 6 x5 …
122 runs are a single residual function between two live ones
```

**Not one residual function sits in an isolated dead region**, and `006F16E0` is not even the longest
run — runs of 24, 21 and 15 were never flagged, because each happened to have a live function inside
its span and so scored `N > 0` under the broken metric. **It was selecting for contiguity and being
read as isolation.**

*(Bookkeeping: 435 under the TEXTJT-excluded definition; the earlier 433 predates dropping TEXTJT as
noise.)*

### AR-4 is closed

Every part of the residual now has one explanation: **unused surface inside live modules.** No wholly
dead object exists in it. The `006F16E0` run was the last candidate and it is not one.

**What was looked for and not found**, so the negative is bounded: no distinct prologue idiom (it is
identical to the surrounding accessors), no source strings (this region of `.text` carries no logging
at all, live or dead), no dead-only callees, no imports, no separate data island. **The only thing
that ever distinguished the run was the metric.**

## 15. Falsification pass 1 — 2026-09-02, session `repos-9e`

**The first deliberate attempt to destroy this document**, by a session that did not write it,
against the GN158 checkpoint (`CHECKPOINT VERIFIED`, residual sha `c5d4b7f7…`, project `GFZ_H9E`).
**Five claims overturned, six survived — and the central finding is one of the survivors.**

This document defends itself better than most: §3 carries an explicit *"Limits of this
measurement"* block, §11 measured a scan against a control, and §1 is itself a retraction. **None
of the five failures below is of a kind those defences were pointed at.** Four are undeclared
populations and one is a correction that was applied to half of its own evidence.

### Overturned

**1. §3's slot table is stale with respect to §3's own correction.** The table reports
`27,392 in .rdata, 204 in .data, 8 in _RDATA`. Re-derived independently from the authorized EXE —
every 8-byte-aligned qword in all non-`.text`/`.pdata`/`.reloc` sections whose value equals a
function entry:

| | `.rdata` | `.data` | `_RDATA` | distinct functions |
|---|---:|---:|---:|---:|
| this document | 27,392 | **204** | 8 | 10,472 |
| re-derived, **all** functions as candidates | **29,000** | **3,015** | 8 | 10,473 |
| re-derived, candidates restricted to `CodeDomain`-tagged | 27,396 | **204** | 8 | **7,332** |

**The third row is the document's own superseded scan.** It reproduces `204` and `8` exactly and
`.rdata` within 4, and its distinct count 7,332 is the **7,331** the correction note says was
wrong. So the correction — *"the first scan silently restricted its candidate set to functions
carrying a `CodeDomain` tag, undercounting by 3,141"* — was applied to the **distinct-function
count** and not to the **slot counts printed beside it**. The two numbers in that block come from
two different scans.

**`.data` is understated by a factor of about 15**, and that is the part that matters: at 204 the
story reads as almost purely vtables; at 3,015 the writable-section side is a substantial second
population.

> ~~while `.data` slots are the runtime-built dispatch tables that the largest-unclassified document
> §2 identifies as a major engine pattern~~ — **withdrawn by the author of this pass, section 16.**
> All 3,015 lie inside `.data`'s **raw** extent (`01DF0000`-`01F7E400`) and carry base relocations,
> so they are **statically initialised in the file**, not built at runtime. The runtime-built regions
> (`022D9000`, `02AEE000`) sit far past the raw extent where a static scan cannot see them at all.
> Two different parts of `.data` were conflated.

**2. §1 and §2 disagree about the same set.** §1: *"unowned functions in the 11 generic groups |
15,498"*. §2's two buckets sum to `5,283 + 10,613 = 15,896`. Same eleven prefixes, same document,
**398 apart**. Re-derived, §2 is exact and §1 is not: the eleven groups hold **19,787** functions,
of which **3,891** are funclets, leaving **15,896**.

**3. The 3,891 exception funclets are excluded from every population in §2 and §3, and the
exclusion is never declared.** It is not an error — it is a defensible choice — but it is invisible,
and it is the difference between reproducing this document and failing to:

| the document's figure | re-derived as stated | re-derived minus funclets |
|---|---:|---:|
| glue-shaped, 5,283 | 9,174 | **5,283** ✓ |
| glue bytes, 172,156 | 231,893 | **172,156** ✓ |
| unowned, zero direct callers, 10,924 | 14,814 | **10,923** (within 1) |
| not address-taken, 3,739 | 7,628 | **3,737** (within 2) |

Every one lands only after subtracting 3,891. A reader re-deriving any of these gets a different
answer and no stated reason. This is the defect the coordinator has just fixed in `progress.py`
for the same reason: **state the population beside every number.**

**4. "70.4 % of the executable" is 70.4 % of a denominator the document never gives.**
`24,116 / 34,270 = 70.4 %`, where 34,270 is the non-funclet function count. Against all 38,161
functions it is **63.2 %**. Against bytes it is neither. "Of the executable" is the one reading
that is not true.

**5. The headline calls named upstream library code "unexplained".** The population reproduces
exactly — `CodeDomain`, no `PrimaryOwner`, minus funclets = **24,116** — but of those, **8,458
(35.1 %) carry a specific mechanism identity rather than a generic shape class**, including:

```
ThirdParty.Video.LibVPX_VP8_1_6_0.Vp8FilterBlock1d16V6Ssse3
ThirdParty.Video.LibVPX_VP8_1_6_0.Vp8MbPostProcDownC
EASTL.BasicString.StaticInitializer
Media.ImageProcessing.SIMD
ThirdParty.Rendering.Yebis
```

A function matched to a named upstream routine is **tier 6 identified** by this database's own
evidence hierarchy. The mission prompt's figure for *"accounted for and not understood"* is
**~11,800**, roughly half the headline. *(Sensitivity: that 8,458 counts `Runtime.*` and
`Boundary.*` as generic, following §2's own treatment of them as shape labels. Excluding `Phyre`'s
6,768 as a genuine grey area still leaves ~1,690 unambiguously identified functions inside a count
of "unexplained".)*

### Survived — attacked and not broken

**The central finding survives, and it is the one worth having.** *Two thirds of the uncalled
unowned code is reached through a pointer in a data table, so an `E8`-based edge list is blind to
it by construction.* Re-derived from the image with the full candidate set: **7,186** of **10,923**
= **65.8 %**, against the document's 7,185 of 10,924 = 65.8 %. Within one function on both sides.
The stale slot table sits beside this claim; **it does not carry it.**

| Claim | How attacked | Result |
|---|---|---|
| 65.8 % address-taken among no-caller unowned | independent scan, full candidate set | **7,186 / 10,923 = 65.8 %** — holds |
| Dark set: `Phyre` 1,743 | independent derivation | **exact** |
| Dark set: `NativeRoutine` 514, `Runtime` 361, `NativeAdapter` 243, `Boundary` 173, `CompilerGeneratedCFG` 145, `NativeLeaf` 91 | same | **all six exact** |
| ~~`_RDATA` holds 8 slots~~ *(answered: see §15, "The `_RDATA` 8 were never real"; `_RDATA` carries no base relocation; 2026-10-02, OPUS)* | independent scan | **exact** |
| 10,472 distinct functions addressed | independent scan | **10,473** — within 1 |
| §2 `substantial`: 10,613 functions, 2,573,049 bytes, mean 242 | independent derivation | **exact, all three** |
| §1's retraction of pass 51 — an edge census is not a function census | re-derivation | **sound**, and the distinction is real |

**The instrument was controlled before its results were believed.** A scan for function pointers
must be able to find a vtable. Self-contained control: any run of ≥8 consecutive 8-byte-aligned
qwords all equal to function entries is a vtable by construction. The scan finds **1,534** such
runs, the largest **1,172 slots** at `008C31D8`, verified against the raw bytes. An implementation
that could not find those would have produced a plausible number and no error.

### What this pass did not test

- **§5 (the eight specimens), §6 (the 112-record table), and §10–§14 (AR-4 and its closure) were
  read but not attacked.** They are now the largest untested surface in this document, and §12–§14
  in particular carry the kind of positive claim this pass did not go after.
- Whether any of the 7,186 address-taken functions is a **dead** vtable slot. §3 flags this itself
  as a limit; it remains untested and it bounds what "reachable" means here.
- The `.data` slot population is now known to be 15× larger than reported and **nothing has been
  read from it**.

### The killer observations, named

- *The slot table would be wrong if a restricted candidate set reproduced it.* One does, exactly.
- *The census figures would be wrong if a stated population failed to reproduce them.* Four failed
  until 3,891 funclets were removed, which no caption mentions.
- *The central 65.8 % would be wrong if an independent scan disagreed.* It does not — within one
  function on both sides of the ratio.

## 16. The `.data` slot population, read — 2026-09-02, session `repos-9e`

§15 corrected the `.data` slot count from 204 to 3,015 and left the population unread. This section
reads it, **certifies it**, and **withdraws one of §15's own characterisations**.

### The predicate, stated in the document and not only in the script

Every number in this section counts slots matching **exactly this test**. It is written out because
a census whose selector lives only in a script cannot be reproduced or contradicted, and because one
clause of it turned out to be load-bearing in a way the author did not anticipate.

```
a .data / .rdata FUNCTION-POINTER SLOT is a virtual address V such that

  1.  V is 8-byte aligned
  2.  V lies inside the section's RAW extent          <- load-bearing, see the withdrawal below
        .data raw = 01DF0000 .. 01F7E400   (of a virtual 01DF0000 .. 02F97530)
  3.  the qword stored at V satisfies 0x00120000 <= q < 0x01000000
  4.  q is exactly the entry address of a function in the certified function list
  5.  V carries a DIR64 base relocation                <- the certification, new here
```

**Clause 2 is why this census can say nothing about runtime-built tables.** A static scan reads only
the file image; `.data` is 18.5 MB virtually and 1.6 MB on disk, so **91 % of `.data` is invisible to
any test of this shape**. Clauses 1–4 are the original scan; clause 5 is what turns its upper bound
into a count.

**Clause 4 is a choice, not a law.** Requiring an *exact* function entry excludes an interior
pointer — a jump into the middle of a function, or a pointer to a function this list does not know
about. Those exist in principle and this census cannot see them, so all figures below are **exact
for the stated predicate and a floor for "address-taking" in general.**

### Controls — two, and neither borrowed from a document

**Control 1, the relocation parse.** The 1,172-slot table at `008C31D8` is **1,172-of-1,172**
relocation-backed. A broken relocation parse fails here first.

**Control 2, the census itself.** A `.data` function-pointer census that cannot find the tables the
database already documents has not earned its numbers. Run blind, this one recovers all three:

| recovered by the census | independently documented as |
|---|---|
| a 202-slot run at `01EFA5C0` | the combat formula step table, 202 × 8 |
| runs of 226 / 62 / 33 / 16 at `01EEC460`–`01EECDA8` | the battle action handler table, 359 slots, *"they are one table; the runs break at null entries"* |
| ~1,740 slots from `01EED700` | ScriptVM native dispatch family 0, 1,496 × `0x20` |

Neither control was constructed from the answer: control 1 is definitional, and control 2 compares
against documents written before this section existed.

### The count is now certified, not an upper bound

§3's limits block says the scan *"matches any qword that exactly equals a function entry. A
coincidental integer can match... the number is an **upper bound** on address-taking, not a
certified count."* That limit can be removed. **Every genuine absolute pointer in a PE must carry a
base relocation**, or ASLR would break it. Intersecting the slots with the `DIR64` entries in
`.reloc` (114,962 of them) separates real pointers from coincidences exactly:

| section | slots matching a function entry | relocation-backed | coincidental |
|---|---:|---:|---:|
| `.rdata` | 29,000 | **27,202** | **1,798** (6.2 %) |
| `.data` | 3,015 | **3,015** | **0** |
| `_RDATA` | 8 | **0** | **8** (100 %) |

**Control:** the 1,172-slot table at `008C31D8` is 1,172-of-1,172 relocation-backed. An
implementation that failed to parse relocations would fail there first.

**The `_RDATA` 8 were never real.** All eight qwords are the constant `0x00800000`, sitting among
`0x000000007F000000` and `0x0000800000000000` neighbours — a block of float bit patterns. `0x00800000`
is simultaneously a valid function entry and the IEEE-754 encoding of the smallest normal float, and
nothing relocates it. **This document and its audit both reported 8, and both were wrong, because
both used the same method.** Agreement between measurements that share a source is not corroboration
— a rule this database already holds, here caught applying to itself.

### Withdrawn: these are not the runtime-built tables

> **§15 said the `.data` slots are *"the runtime-built dispatch tables"*. That is wrong and is
> withdrawn.** `.data` spans `01DF0000`–`02F97530` virtually but its **raw image covers only
> `01DF0000`–`01F7E400`**. Every one of the 3,015 slots lies inside that raw range and carries a
> base relocation, so all 3,015 are **statically initialised in the file**. The runtime-built regions
> the largest-unclassified document describes — `022D9000`, `02AEE000` — are far past the raw
> extent, and **a static scan cannot see them at all**. Two different parts of `.data` were
> conflated. The corrected reading is in fact more useful: a function pointer that is *statically
> initialised into a **writable** section* is one the engine intends to be **replaceable at
> runtime**, which is a different and sharper claim than "built at runtime".

### Three quarters of it was already documented

"Nothing has been read from this population" was also wrong. Measured against the **spans** other
documents state — base, stride and extent, not proximity to a cited address:

| slots | table | documented in |
|---:|---|---|
| 1,740 | ScriptVM native dispatch, family 0 — `01EED700`, 1,496 × `0x20` | [`scriptvm-native-dispatch-table.md`](../../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md) |
| ~~339~~ 340 *(corrected 2026-10-02, OPUS: re-derived as in §17: 340 relocated function-entry slots in `01EEC460`–`01EECD98`)* | Battle action handler table — `01EEC460`, 359 slots | [`battle-action-handler-table.md`](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md) |
| 202 | Combat formula step table — `01EFA5C0`, 202 × 8 | [`combat-formula-step-table.md`](../../08-Combat-Formula/Step-Table/combat-formula-step-table.md) |
| **~~2,281~~ 2,282** *(corrected 2026-10-02, OPUS: 1,740 + 340 + 202)* | **inside an already-documented table (75.7 %)** | |
| ~~734~~ 733 *(corrected 2026-10-02, OPUS: 3,015 − 2,282)* | outside every documented span (24.3 %) | |

Of the 734, **501 point at `Script_VM_Native_Bridge`-owned functions** and cluster around
`01F26xxx` — consistent with the four further ScriptVM tables that document describes (five tables,
1,960 records total, of which family 0 holds 1,496). **The genuinely undocumented remainder is
therefore about 233 slots.**

> **A defect in this section's first instrument, recorded rather than fixed silently.** Coverage was
> first measured as *"is any address within 64 bytes of this run cited anywhere in the database"*,
> which reported **1,959 of 1,977 runs uncited**. That is nonsense: a 1,496-record table cites its
> **base**, not its rows. The battle action document had already performed this section's exact run
> analysis — its §142 states *"226 and 62 slots. They are one table; the runs break at null
> entries"* — and the proximity test could not see it. **A coverage test keyed on citation distance
> measures how documents are written, not what they cover.**

### The remainder, and the one part worth a modder's attention

| run | slots | what it points at |
|---|---:|---|
| `01F41E98` | 26 | Audio-owned, plus vtable members and a computed-call dispatcher |
| `01F003A8` | 13 | **7 of the 13 targets are unresolved functions** |
| `01EECFE0` | 12 | ItemsEquipment support, a Party callback, 5 CFG stubs |
| `01E0C498` | 10 | `Runtime.RealFunctionPointerOrVtableMember` |
| `01F41CF8` | 4 | **`malloc`, `free`, `calloc`, `realloc`** |
| `01F44CE0` | 4 | **`malloc`, `free`**, plus an aligned-free callback |

The two allocator runs are the interesting ones. **The CRT allocator entry points are stored as
function pointers in a writable section**, which is what an engine does when it intends to swap its
allocator — and it is the cleanest interception point in the image for anyone instrumenting
allocation, because replacing them needs no code patching at all. 58 further slots hold
`_guard_check_icall`, the CFG stub used as a null placeholder.

### A residual function has an admissible reference after all — and the scan that says otherwise

**This is the consequential result.** Intersecting the certified slots with the 158 unresolved
functions returns exactly one hit:

```
slot 00916518  [.rdata]  ->  002AAE40      base-relocation certified
```

`002AAE40` is the 2,440-byte function [the-unresolved-158 §11](../the-unresolved-158.md) singles out:

> *"this function [`002AAE40`] has **no admissible reference of any kind** — no caller, no vtable, no dispatch
> table. It is the purest example in the database of why a call-context classifier cannot touch
> these."*

**It has one.** A relocated 8-byte function pointer in `.rdata` is a real data reference — tier 8,
and certified rather than inferred. The certified evidence dump lists three incoming references for
`002AAE40` and all three are the banned EH records that passage describes; **`00916518` does not
appear in it at all.**

The cause is the same family as the string scanner: `DumpUnresolvedIncomingDataRefContexts` reports
references Ghidra holds, and Ghidra holds none from a data slot that was never typed as a pointer.
**This matters more than the single function, because that scan is the source of the residual
category's founding claim** — *"96 % of the incoming references to these 158 functions are exception
metadata"*. That census counts only references the database happens to contain.

> **The locality is not evidence and is not used as any.** The slot sits 8 bytes before the
> power-of-ten table at `00916520` that the numeric-formatting document reads. Adjacency is a banned
> evidence class here, and the last document this session audited flagged an adjacency, declined to
> claim it, and was later proved right to — the adjacency was coincidence. This one is recorded as a
> **reason to look**, nothing more. The independent evidence that `002AAE40` is font drawing is
> tier 2 and unrelated: it closes the scope named `"display : draw Font"`, per
> [glyph-run rendering](../Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md).

### What is still not known

- **The ~233-slot remainder is characterised, not read.** No body behind it was opened.
- **Who writes these slots at runtime.** Every one is statically initialised; whether anything ever
  overwrites them is untested, and that is the whole point of their being in a writable section.
  **PROPOSED-repos9e-12.**
- **How many of the 158 gain an admissible reference once the reference census is redone properly.**
  One was found by intersecting with relocations; ~~the full re-census has not been run.~~ *(answered: see the category README, "The re-census has now been run", and the-unresolved-158.md, 158 of 158; 2026-10-02, OPUS)*
  **PROPOSED-repos9e-13.**
- The `.rdata` side was certified (27,202 of 29,000) but **not read** — it is nine times larger.

## 17. The remainder recounted — 2026-09-02, session `repos-d2`

§16 left **734 slots outside every documented span**, of which *"501 point at
`Script_VM_Native_Bridge`-owned functions and cluster around `01F26xxx`"*, giving a *"genuinely
undocumented remainder of about 233 slots."* Those four ScriptVM tables have since been enumerated
in
[the dispatch table document](../../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md)
§14, so the subtraction that defined the remainder has changed.

> **A remainder is defined by a subtraction, so it goes stale whenever anything else is documented,
> and nothing in the figure announces that.** It is the one quantity here that changes on another
> session's success rather than on new evidence. **Any remainder should be published with what it
> was subtracted from and when** — this one is subtracted from the seven spans in the table below,
> as of 2026-09-02.

### The census reproduces exactly, then the remainder moves

§16's five-condition test was re-implemented independently and applied verbatim: 8-byte aligned,
in `.data`, value equals a certified function entry, and the slot carries a `DIR64` base relocation.

| | §16 | independent re-derivation |
|---|---:|---:|
| `DIR64` base relocations parsed | 114,962 | **114,962** |
| certified `.data` slots | 3,015 | **3,015** |

| documented span | slots |
|---|---:|
| ScriptVM command family 0 — `01EED700`, 1,496 × `0x20` | 1,740 |
| battle action handler table — `01EEC460`, 359 slots | 340 |
| combat formula step table — `01EFA5C0`, 202 × 8 | 202 |
| **ScriptVM command default table** — `01F26720`, 212 × `0x20` | **250** |
| **ScriptVM command family 3** — `01F281B0`, 147 × `0x20` | **153** |
| **ScriptVM command family 5** — `01F29418`, 1 × `0x20` | **2** |
| **ScriptVM command family 7** — `01F29440`, 104 × `0x20` | **130** |
| inside a documented span | **2,817** |
| **REMAINDER** | **198** |

**The remainder is 198, not ~233**, and the difference is not a correction to §16's arithmetic — it
is that **535 slots acquired a home**, which is 34 more than the 501 the estimate anticipated.

**Why the estimate undershot the coverage.** It subtracted by **target ownership** ("slots pointing
at `Script_VM_Native_Bridge`-owned functions") where the remainder's own definition subtracts by
**span membership**. Those four tables hold 35 callbacks pointing at functions owned by other
subsystems or by nobody — a command table is perfectly entitled to call out of its own subsystem.
**An owner-keyed estimate of a span-keyed quantity is systematically low**, and it is low by exactly
the cross-subsystem callbacks, which is the interesting part of any dispatch table.

### The remainder is mostly not loose slots

The 198 fall into 113 contiguous runs, but **contiguity is the wrong shape for most of them**: the
large groups are **strided records whose pointer fields are non-adjacent**, so a run analysis
fragments one table into many two-slot runs.

The clearest case is the eight two-slot runs at `01EEBD08`, `01EEBD60`, `01EEBDB8`, `01EEBE10`,
`01EEBE68`, `01EEBF18`, `01EEBFC8` and `01EEC128`, all `Items_Equipment_Shops_License`. **They are
one table**, and its consumer says so exactly:

```asm
InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState  (0030B6A0, 195 B)
  0030B6A8  lea r8,  [rip -> 01EEBCC0]      ; base
  0030B6B2  lea rbx, [rip -> 01EEC1E8]      ; END
  ...
  0030B6F9  add r8, 0x58                    ; stride 88
  0030B6FD  cmp r8, rbx
  0030B700  jl  loop
```

`0x01EEC1E8 - 0x01EEBCC0 = 0x528`, and `0x528 / 0x58 = 15` exactly. **Fifteen inventory class
descriptors of 88 bytes at `01EEBCC0`**, and the rebaser gives the record layout for free:

```
InventoryClassDescriptor  (0x58 bytes, 15 of them at 01EEBCC0)
  +0x00  u32/ptr  offset -> rebased into +0x08 as (u32)[+0x00] + instanceBase
  +0x18  u32/ptr  offset -> rebased into +0x20
  +0x28  u32/ptr  offset -> rebased into +0x30
  +0x3c  u32      element count, accumulated across descriptors
  +0x40  u32      running cumulative index, written back per descriptor
  +0x48  ptr      MUTATE callback     <- the slots this census counted
  +0x50  ptr      QUERY  callback     <-
```

The callback pairs are `InventoryPackedCountClass_MutateChannels` / `_QueryChannel` and
`InventoryBitsetClass_MutateState` / `_QueryState` — **two storage classes shared across fifteen
descriptors**, which is why the same two addresses repeat down the table.

A second strided family sits at `01F32150`, stride `0x80`, pairs of `006D5xxx`/`006D6xxx` functions,
with five per-record accessors at `008B75A0`-`008B75E0` each taking the address of one record. Its
extent is **not** established here and it is not claimed.

### What survived, and one run §16 did not list

All six runs §16 tabulates reproduce exactly: `01F41E98` (26, Audio), `01F003A8` (13),
`01EECFE0` (12), `01E0C498` (10), `01F41CF8` (4, the CRT allocator entry points) and `01F44CE0` (4).
**A seventh is larger than two of them and is not listed:** `01F41E60`, **6 slots, all Audio-owned**,
sitting 56 bytes before the 26-slot Audio run — very likely the same structure, which is again the
fragmentation effect rather than a new find.

Of the 198 remainder targets: **111 have no owner** in the ledger, 41 Presentation, 22 Audio, 20
Items, 2 ScriptVM, 1 each Platform and Party. **38 of the 198 slots hold `_guard_check_icall`
(`0016D6A0`)** used as a null placeholder — §16 reports 58 such slots across the wider 734.

### What this leaves

**The genuinely uncharacterised part of the remainder is smaller than 198.** Fifteen inventory
descriptors (30 slots at most), the allocator runs (8), the folded-stub placeholders (38) and the
Audio pair of runs (32) are all accounted for by shape. The residue is the 88 single-slot runs, which
is where a slot really is a lone callback rather than a fragmented table.

## The 27,202 certified `.rdata` slots, accounted for — 2026-09-03

§3 counts the pointer slots but says nothing about what they are. Applying the relocation-certified
predicate to `.rdata` and then partitioning by structure:

```
P1  8-byte aligned and inside the section's RAW extent
P2  the qword is non-zero
P3  its value is a known function ENTRY
P4  the slot carries an IMAGE_REL_BASED_DIR64 relocation
```

| | slots | share |
|---|---:|---:|
| certified `.rdata` function-pointer slots | **27,202** | 100 % |
| inside an RTTI-recovered vtable | **25,761** | **94.7 %** |
| the C++ static-initializer table `__xc` (`008C31D0`–`008C5678`) | **1,172** | 4.3 % |
| the C initializer table `__xi` (`008C5680`–`008C56A0`) | **3** | — |
| **accounted for by those three** | **26,936** | **99.02 %** |
| **uncharacterised** | **266** | **0.98 %** |

The vtable figure comes from recovering **~~2,335~~ 2,350 RTTI type descriptors → ~~2,271~~ 2,286 complete-object
locators → ~~2,271~~ 2,286 vtables** *(corrected 2026-10-02, OPUS: RTTI recount: 2,350 `.?AV`/`.?AU` descriptors sharing one `type_info` vftable, 2,286 locators whose self-RVA checks, 2,286 `.rdata` qwords pointing at them — §3's 2,286; the slot totals above were walked from 2,271 and are not re-derived here)* and walking each until a slot fails the predicate. The two initializer
tables are documented in
[static initialization order and injection timing](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md),
whose extents and `_initterm_e` / `_initterm` split this census reproduces independently. Its count
of **3** populated `__xi` entries is confirmed — the span holds four slots and one is the null
sentinel, so the two figures measure different things and do not disagree.

**So `.rdata` is not an unread mass.** Nineteen slots in twenty are a C++ vtable, and almost all of
the rest are the list of static constructors the CRT runs before `main`.

### What is actually left

The 266 uncharacterised slots form **52 groups**, of which **22 are single slots**.

> **Corrected 2026-09-03 — the first version of this line said "192 runs, 166 single slots".** That
> was step-8 contiguity, which is the right rule for the rest of `.rdata` (arrays of pointers, where
> consecutive entries really are 8 bytes apart) and **the wrong rule for this residue**, which is
> largely **16-byte records with one pointer field**. Every such table shatters into singletons under
> contiguity. Regrouped as maximal arithmetic progressions with a stride established by at least
> three members:
>
> | rule | groups | singletons |
> |---|---:|---:|
> | contiguity, step 8 | 192 | **166 (86 %)** |
> | progression, stride `0x8`–`0x100`, ≥3 members | **52** | **22 (42 %)** |
>
> Strides found: `0x10` ×14, `0x8` ×6, `0x18` ×4, `0x30` ×3, `0x20` ×2, `0x60` ×1. **The residue is
> not fragmented — it is mostly record tables.** 86 % singletons against this section's own base rate
> of about 16 % was the tell, and it was flagged by a session measuring grouping behaviour per
> section rather than by anything in this document.

Ranked by members, under the progression rule:

| group | members | stride | owners |
|---|---:|---|---|
| `01CCB168`–`01CCB308` | 27 | `0x10` | unowned |
| `01CCA3F8`–`01CCA548` | 22 | `0x10` | unowned |
| `01CEB070`–`01CEB108` | 20 | `0x8` | Audio 12 — **a true pointer array**, read below |
| `01CCC6C8`–`01CCC7B8` | 16 | `0x10` | unowned |
| `01CCAD58`–`01CCAE28` | 14 | `0x10` | unowned |
| `01CCAFF8`, `01CCE790` | 12 each | `0x10` | unowned |

**The largest structures in the residue are 16-byte-record tables in `01CCAxxx`–`01CCExxx`, not the
Audio pointer arrays** — and they are larger than the Audio tables that were found first, because
contiguity had hidden them. None of them is characterised; their consumers were not traced.

The original contiguity ranking, kept because the Audio runs below were read under it:

| run | slots | owners of the targets |
|---|---:|---|
| `01CEB070`–`01CEB108` | 20 | Audio 12, unowned 8 |
| `01CEB148`–`01CEB188` | 9 | Audio 5, unowned 4 |
| `009164C0`–`009164E8` | 6 | unowned 6 — **already read**: the 12-entry sparse table holding ~~the residual function~~ `002AAE40` (*corrected 2026-09-14: `002AAE40` left the residual list when it went 158 → 139; the certified parent classifies it `Presentation.Text.GlyphRunCharacterWalkAndScreenWidthBatchSplit`. **The "unowned 6" count is about the six table references and is unchanged** — it is the word "residual" that expired*) |
| `01CE3080`–`01CE30A8` | 6 | Audio 5, unowned 1 |
| four runs of 4 | 16 | mostly unowned |

**The residue is small, fragmented, and clustered in `01CEBxxx` around Audio.** That is a bounded
target rather than a survey: 192 runs, and a third of the mass sits in four of them.

### A method note, since this census had to be built twice

The first partition returned **14.4 %** in vtables, not 94.7 %. The cause was the type-descriptor
regex requiring the mangled class name to begin with a letter, which silently dropped every
**template** class — names beginning `?$` — and recovered **640 of 2,335**. It was caught because
640 contradicted a figure already on file (~2,350 RTTI markers ship in this image), **not** because
the partition looked wrong; at 14.4 % it looked like an interesting finding about vtable coverage.

**A census whose own instrument undercounts its denominator produces a plausible number, not an
obvious failure** — the same shape as the printable-byte filter that returned zero diagnostic
strings, and the `0x`-prefix displacement regex that lost one vtable slot in twenty.

## 18. The `01F32xxx` runs closed — a name-keyed registry, not an array

§17 left the second strided family at `01F32150`, stride `0x80`, with its extent *"not established
and not claimed."* It is now established, and **the shape was wrong**: there is no array and no
stride.

### What they are

The five two-slot runs at `01F32150`, `01F321D0`, `01F32250`, `01F322D0` and `01F32350` are the
`+0x40` / `+0x48` fields of five **individually declared descriptor objects** whose bases are
`01F32110 + k*0x80`. Each begins with a `char *` name, and the names decide it:

| base | name | `+0x40` | `+0x48` |
|---|---|---|---|
| `01F32110` | **`Skin`** | `006D5CC0` | `006D5DF0` |
| `01F32190` | **`SkinLocal`** | `006D5B60` | `006D5DF0` |
| `01F32210` | **`SkinLocalTangent`** | `006D5B60` | `006D63D0` |
| `01F32290` | **`SkinVertex`** | `006D5CC0` | `006D6AC0` |
| `01F32310` | **`SkinVertexLocal`** | `006D5B60` | `006D6AC0` |

**Five named skinning variants** — the mesh-deformation paths a character model is processed
through. The two callbacks are **orthogonal discriminators**, which the sharing makes plain without
reading either function: `+0x40` selects the space (`006D5B60` for every `…Local` name, `006D5CC0`
for the two without it) and `+0x48` selects the output kind (`006D5DF0` plain, `006D63D0` tangent,
`006D6AC0` vertex). Five of the six combinations of those two axes exist.

### The extent is established, and not by a loop

There is no walking loop here, so the rule that closed the previous four blocks does not apply. **The
registrar is the schema instead.** `FUN_006D5A60` (132 B, reached through `thunk_006D5A50`) is a
singly-linked-list insert keyed on the name:

```c
name = *(char **)(record + 0x00);          // +0x00  char *name
if (!name) return 0x11;                    // refuse an unnamed record
for (n = g_head /* 02E9FD60 */; n; n = n->next /* +0x08 */)
    if (strcmp(n->name, record->name) == 0) return 0x12;   // refuse a duplicate name
record->next = g_head;                     // +0x08  next
g_head = record;                           // push
return 0;
```

So a record is `{ char *name; Record *next; ... }` and **the registry does not know or care how large
a record is** — which is why records of two different sizes are registered through it, and why
"stride" was the wrong question.

**The population is bounded by enumerating the registration sites**, and there is exactly one
registering function: `FUN_006C45F0` performs **14** registrations, and `FUN_006C4750` performs the
matching 14 unregistrations through `FUN_006D6F90` (the unlink, which walks the list patching the
predecessor's `next`). Nine of the fourteen are a different record type at `02E9FEF0 + k*0xD0`.

### Why only five of the fourteen ever reached this census

`.data`'s raw extent ends at `01F7E400`. The five `Skin*` records lie **below** it — statically
initialised, relocated, file-backed — so their callback pointers satisfy §16's five-condition
test. The nine at `02E9Fxxx`/`02EA0xxx` lie **above** it, in the zero-filled tail: no file image, no
relocations, name pointers null in the file, constructed entirely at run time.

**The certified-slot census can only ever see the statically initialised half of this registry.**
That is not a defect in it — its predicate says so — but it means a run appearing in the remainder
may be a *fragment of a population that is mostly invisible to the test*, which is a different
situation from a run being the whole of something small.

### An instrument defect of my own, recorded

My first registration-site scan counted `call` instructions and reported **13** sites. The
fourteenth is a **tail jump**: `lea rcx,[01F32310]` / `add rsp,0x28` / `jmp 0x6d5a50` at `006C4734`.
`SkinVertexLocal` was missing from the enumeration and the name pattern is what made the gap
visible — four `Skin*` names with an obvious fifth absent.

**This is the third time tonight the tail-call-as-sink effect has cost something**, after Ghidra's
call graph reporting zero callers for `0023A520` and under-reporting `00263E30` through its guard
`0031B760`. Both of those were written up as other tools' blind spots; **this one was mine, built
into a scan I wrote after describing the defect twice.** A census of call sites that does not count
tail jumps is not a census of call sites.

**What the corrected caller graph actually shows for `00263E30`.** Eleven **movement** bodies
call it (`00326D60`, `003357B0`, `00319490`, `00329A80`, `00311F70`, `00311E20`…), six
**gameplay** bodies call it or its guard `0031B760` (`00321380`, `003176E0`, `0031ADB0`,
`0030BFB0`, `0030B050`, `0030BA30`) — 17 edges across the two layers. The function is unowned;
its *consumers* are not. A shared getter read by locomotion and gameplay code is exactly what
"no owner" predicts, and the crossing says nothing about who should write it.

### The residue read: a statically-linked audio library reached only through pointers

The four largest uncharacterised runs are one mechanism. All of their targets lie in
`0088E000`–`00895000`: **42 functions, 29,042 bytes, 32 of them `Audio`-owned — and zero functions
outside that range call into it directly.** It is a self-contained library linked into the image and
reached entirely through function pointers, which is this document's own thesis in its purest form.

**`01CEB618`, four slots — the library's allocator hook table.** Not a dispatch table: **242
`call qword ptr [rip + …]` instructions** from `Audio`-owned functions in the block target two of its
four slots.

| slot | target |
|---|---|
| `01CEB618` | `calloc` |
| `01CEB620` | `realloc` |
| `01CEB628` | `malloc` |
| `01CEB630` | `free` |

That is the standard shape of a portable library's replaceable-allocator table, wired in this build
straight to the CRT. **Every allocation this library makes passes through those four pointers**, so
they are the one place a modder can account for or redirect its memory — subject to `.rdata` being
read-only at runtime, so it is a link-time seam rather than a live hook.

**`01CEB070`, twenty slots — the library's dispatch table.** Every entry points into the same block.
It has **no RIP-relative consumer at all**; it is reached through a single pointer stored at
`01CDCF68`, and the one instruction that takes that address is `00882495` in `FUN_008822F0` —
**inside the block itself**. It is preceded in `.rdata` by float constants, not by a
complete-object locator, so it is a vtable-shaped table for a class compiled without RTTI, which is
exactly why the RTTI partition above could not see it.

Runs `01CEB148` (9), `01CEB118` (4) and `01CE3080` (6) sit in the same region with the same owner
mix and are almost certainly more of the same structure; **their consumers were not traced and they
are not claimed.**

> **A reading error of my own, recorded because it produced a confident wrong answer.** The pointer
> to `01CEB070` was located correctly on the first attempt, but the locator printed its address in
> **decimal** and I converted it to hex wrongly by eye — reading `30265192` as `01CDF3A8` when it is
> `01CDCF68`. I then read that wrong address, found float constants, and had a coherent but entirely
> fictitious account of the structure. The instrument was right the whole time. **A units or radix
> mismatch between a tool's output and the reader survives every check aimed at the tool**, and it
> was caught only because the follow-up read disagreed with the search that produced it.

## 19. The single-slot runs were an artifact of the grouping, not a population

§17 bounded the remainder at 198 slots and said the residue was *"the 88 single-slot runs — where
a slot really is a lone callback rather than a fragmented table."* **That was wrong, and the error was
in the instrument that produced it.**

### Regrouping by stride instead of adjacency

Runs were built by **contiguity**: slots are one group if they are 8 bytes apart. **A table whose
record contributes exactly one pointer can never produce a contiguous run** — consecutive pointers
are one *stride* apart, not 8 — so every such table shatters into as many "single-slot runs" as it
has records.

Regrouping the same 198 slots into **arithmetic progressions of three or more**:

| | contiguity | arithmetic progression |
|---|---:|---:|
| groups | 113 | **34** |
| slots in a group of ×3+ | — | **179** |
| **truly isolated slots** | *"88"* | **19** |

**The residue is 19, not 88.** The largest groups:

| span | stride | slots | targets |
|---|---:|---:|---|
| `01EFFAF0`-`01EFFF70` | `0x10` | **73** | `PresentationAuthoredCommand_Class*`, `_guard_check_icall` fillers |
| `01F41E68`-`01F41F58` | `0x10` | 16 | Audio |
| `01F003A8`-`01F00408` | `0x08` | 13 | mostly untagged |
| `01EECFE0`-`01EED038` | `0x08` | 12 | untagged + one Party |
| `01E0C498`-`01E0C4E0` | `0x08` | 10 | untagged |
| `01F41E60`-`01F41F60` | `0x20` | 9 | Audio |
| `01EEBD08`-`01EEC1D8` | `0x58`/`0xB0` | 13 | the §17 inventory class descriptors |
| `01F32150`-`01F32358` | `0x80` | 10 | the §18 `Skin*` descriptors |
| `01F41CF8`, `01F44CE0` | `0x08` | 4 + 4 | `malloc` / `free` / `calloc` / `realloc` |

The Items and `Skin*` entries are the tables §17 and §18 already identified, **reappearing here as
"singletons" wherever a record's second callback happens to be null.** That is the same fragmentation
seen from the other end.

### The largest group is a 128-entry command table, and its consumer states the bound

`PresentationEmbeddedRecord_ExecuteCommandStreamUntilThreshold` (`0041E000`) hoists the base out of its loop and indexes:

```asm
0041E097  lea r13, [rip -> 01EFFAF0]        ; base, hoisted
...
0041E0C6  and eax, 0x7f                     ; index masked to 0..127  -> 128 RECORDS
0041E0C9  shl rax, 4                        ; x 0x10                  -> STRIDE 16
0041E0CD  cmp byte ptr [rax + r13 + 8], 0   ; +0x08  enable/mode byte
0041E0D3  jne skip
0041E117  call qword ptr [r9 + r13]         ; +0x00  handler
```

**A 128-record authored-command table at `01EFFAF0`**, `0x10` per record, **handler at `+0x00`** and
an **enable byte at `+0x08`**, the index **masked rather than validated** — the same clamp-don't-check
pattern this database records for the descriptor table at `022D94B0`. Span `01EFFAF0`-`01F002F0`.
Its other consumers are `PresentationEmbeddedRecord_UpdateCurrentState` (`0041DA90`) and
`PresentationEmbeddedRecord_ExecuteDeferredCommandSubset` (`0041E1D0`); only **73** of the 128 records hold a
certified pointer, the rest being null or filled with `_guard_check_icall`.

### What this means for the remainder

**The remainder is a floor on structures, not a count of loose pointers.** Of 198 slots, at least
nine distinct tables account for 179; the honest uncharacterised residue is **19 slots**, and even
those are not established as lone callbacks — only as slots this grouping could not place.

> **A grouping rule is a hypothesis about the data's shape, and reporting its output as a population
> asserts that hypothesis.** "88 single-slot runs" reads as a fact about the engine and was a fact
> about `step == 8`. The check is cheap: **regroup under a different rule and see whether the
> population survives.** It did not — 88 became 19.


## The `01F00398` dispatch table's no-caller members — 2026-09-14 (NOCALLER-INSTALLERS)

§16 listed `01F003A8` as a 13-slot run of mostly-untagged functions. Reading the surrounding data
shows the run is one longer table starting at `01F00398`: slot 0 is a data pointer (`01F00090`),
slots 1–14 are the fourteen handler entries. A descriptor array at `01F00090`+0x18 walks the table
as `{1, &slot}` pairs — so the table is *indexed by a side array*, not scanned. No `.text`
rip-relative operand and no data qword names either base; the object is reached by its own
relocations only, which is why the group has no caller.

| slot | address | role | interior |
|---:|---|---|---|
| 1 | `004223F0` | selector-0 adapter: `xor edx,edx ; jmp 004256E0` | |
| 2 | `00422400` | selector-1 adapter: `mov edx,1 ; jmp 004256E0` | `00422405` |
| 3 | `00422410` | selector-2 adapter: `mov edx,2 ; jmp 004256E0` | `00422415` |
| 4 | `00422420` | builds the `0041F2F0` out-struct from `+0x110`/`+0xCC`, then `00808C40` (CFG-guarded tail) | `00422426` |
| 5 | `00422500` | same `0041F2F0` out-struct; two `00422583` self-path calls | `00422506` |
| 6 | `005C5230` | shared empty stub — a null slot | |
| 7 | `00660570` | non-frontier body | |
| 8 | `004225A0` | reads `this+0x2E0`, walks `+0x18`/`+0x10` fields of the sub-object | `004225E4` |
| 9 | `00422630` | `0041F2F0` + `00424370` vector-subtract on globals `00D117E0`/`009166FC` | `00422636` |
| 10 | `004226C0` | `0041F2F0` + `00424370` + `003A6E60`; globals `00D117E0`/`00D12440`/`008F6D54` | `004226C6` |
| 11 | `00422760` | `0041F2F0` + `00424460`; global `00D117E0` | `00422766` |
| 12 | `004227D0` | `0041F2F0` + `00424370`; globals `00D117E0`/`00D12440`/`008F6D54` | `004227D6` |
| 13 | `00422870` | `0041F2F0` + `00424370` + `003A6E60`; globals `00D1243C`/`00D117E0`/`00902EF0` | `00422876` |
| 14 | `00422940` | `this+0x2E0` id lookup — `+0x18` id → `0020E600` record → `002ED570` index → `003E2CD0`, against `022C6F28+0x1B0` | `00422960` |

The nine real bodies are one family: all begin from a `+0x2E0` sub-object or the
`0041F2F0`/`00424370` pair (build a `0x40`-byte out-struct, subtract the `+0x30`…`+0x38` vector)
and read the `00D117E0`/`00D12440`/`009166FC`/`00902EF0` global band — a per-kind transform/query
handler set dispatched by the descriptor array, with slots 1–3 as the shared-tail adapters and
slot 6 empty. What object kind the table serves is **not established** — nothing names the table
base, which is the same "reached only by its own slots" shape §16 recorded.

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This page named these bodies only at their entries (§18's skin-registry table). Each interior
address was read in the shipping image; the notes confirm the §18 role — SIMD matrix-blend kernels.

| body | interior cite | what is there |
|---|---|---|
| `006D63D0` | `006D65ED` | `movups xmmword ptr [r15]` — stores a blended 0xC-stride output vertex at the top of the inner blend loop (`shl rcx,6` bone-matrix stride, `shufps` weight splat) |
| `006D5DF0` | `006D5E90` | `shl rdx, 6` — scales a bone-index byte by 64 = a 4×4 float matrix row in the palette at `r10`; §18's `Skin`/`SkinLocal` entry |
| `006D6AC0` | `006D6B27` | `shl rax, 6` — the same 64-byte palette stride; §18's `SkinVertex`/`SkinVertexLocal` entry, accumulating with `mulps`/`addps` into `xmm5` |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** Cited functions are called by `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` and `BattleUnit_RecoverFromTerminalStatusSetIfClear`.
- **CoreRuntimeScheduling — SERVICE, 5 edges, mechanical.** Every edge is a cited body (`002AAE40`, `002ED570`, `0031ADB0`, `003E2CD0`, `00422940`) calling `0020E600`, `ImageAddress_ResolveRuntimePointer` — the shared image-address resolver the core runtime layer owns. The crossing is the resolver call itself, not a semantic one. *Re-run 2026-09-16 (SWE2-FRONTIER), on `OPUS-REQ-FRONTIER-UNOWNED-CENSUS-CITES-A-RESOLVED-BODY`:* the edge count survives exactly — all five calls are still in `edges.tsv` — but the census premise has moved: `002AAE40` now carries `CodeDomain.Presentation.Text` (owned by 16-UI — the glyph-run width batch split), `002ED570` carries `PrimaryOwner.Resource`, and `0031ADB0` carries `CodeDomain.CombatAction`. Only `003E2CD0` and `00422940` — the previously unnamed fifth — remain `final_no_owner`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (53 edges through 14 of this page's functions).** The ActorEntity layer reaches this page at `0031B760`, `00263E30`, `00326D60`, `0031ADB0` and 10 more. `BattleUnit_GetBySlotIndex` is the worked example, read in full - it is **37 bytes that give the record its width**: the index is bounded against `[0208E6A0] - 1` and indexes `[0208E688]` at a **`0xF50`-byte stride** - 3,920 bytes, the same figure the slot-pool page states from the other end; **7 of the 35 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT.** `BattleUnit_SelectAiOrderSetVariantFromAuthoredTable`, owned by that layer, calls `0031B760` on this page. That caller is the variant choice, bounded at **four** indices: `word[[+0xE60] + 0x50 + index*2]` names a row in the table at `[02EBF168]`, and the resolved pointer is stored at the unit's `+0x6E0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Spawn_Encounter_Lifecycle — CLIENT (24 edges, one fan-in).** All 24 edges are Spawn_Encounter_Lifecycle bodies reaching `0031B760` on this page. `SpawnLifecycle_CheckAndRetireByNativeRange` is the worked example - it is the range retirement: it runs only when the zone query agrees, then takes the unit and measures it. The crossing is **one shared subject with 24 callers on that layer**, not 24 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

## Interior citation — frontier hub `0041F2F0` (2026-09-18, SWE2-EC7)

`0041F2F0` — 65 B, 8 A-measured callers; the out-struct builder the callers above share.
Interior verified: the `r8` record is zeroed for `0x40` bytes (`0041F2F2`–`0041F30D`), then
`[+0x30]` receives `dword[rcx+0x110]` and `[+0x00]` the sign-extended `word[rcx+0xCC]`
([`0041F311`](../../_index/ADDRESS-INDEX.md)–`0041F322`); the tail `jmp 002ED500` at `0041F32C` forwards
`rcx = [rcx+0x108]` with the filled record — a field-snapshot plus bitfield write into the
paged-state table.

## SWE2-EC7-38 update (2026-09-19) - `0041E000`

`0041E000` (461 B) is a ~~call-free~~ unowned body *(corrected 2026-10-02, OPUS: it calls `qword [r9 + r13]` through the `01EFFAF0` table at `0041E000`+0x117)* - `[rcx+0x368]` object, `test byte[rdi+0x96], 0x80` gate, `0x80220010` magic, `01EFFAF0`. Interior anchor `0041E034` (inside the gated arm).

## SWE2-EC7-41 update (2026-09-19) - `0041E1D0`

`0041E1D0` (348 B) is a ~~call-free~~ record walker *(corrected 2026-10-02, OPUS: it calls through the `01EFFAF0` table at `0041E1D0`+0xED)* - `[rcx+0x368]` base plus `[rdx+0x84]`/`[+0x8c]` counts, 6-byte entries tested `byte[+2] & 0x3f` against a `word[+4]` bound, `0x80220040` flag, `01EFFAF0` ~~vtable~~ command table *(corrected 2026-10-02, OPUS: 16-byte `{handler, 0}` records with no complete-object locator before them — §19's 128-record table)*. Interior anchor `0041E246` (the `test byte [rbp+2], 0x3f`).

## SWE2-EC7-41 update (2026-09-19) - `006D5B60`

`006D5B60` (347 B) is an unowned body - `00187460`/`00185100` pair. Interior anchor `006D5BB4` (an `00187460` call).

## SWE2-EC7-43 update (2026-09-19) - `006D5CC0`

`006D5CC0` (295 B) is an unowned-census body - `00185100` single call. Interior anchor `006D5D3B` (the `00185100` call).

## SWE2-EC7-46 update (2026-09-19) - `00424460`

`00424460` (228 B) is a body - `0046D0C0`/`0046D100`/`0046D340`/`005213F0`/`00808C40`/`00861F02`. Interior anchor `004244B7` (a `0046D0C0` call).

## SWE2-EC7-56 update (2026-09-19) - `00187460`

`00187460` (194 B) is an unowned body - `00185AF0` single call. Interior anchor `0018746E` (a `00185AF0` call).


## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

Every citation on this page is a census entry of unresolved or unowned code, so each layer below arrives with those bodies' ordinary call graphs. None of them is a claim this page makes.

**Audio — MECHANICAL, 3 edges.** `008822F0` calls `0017CB40`, `008820E0`, `00882180`.

**Combat — MECHANICAL, 1 edge.** `ActorWork_GetBattleUnitRaw` (`00263E30`) is called by `003206E0`.

**CombatFormula — MECHANICAL, 1 edge.** `ActorWork_GetBattleUnitRaw` (`00263E30`) is called by `BattleStats_ResolveByActorHandle` (`00320A70`).

**Party — MECHANICAL, 12 edges.** `ActorWork_GetBattleUnitRaw` (`00263E30`) is called by `BattleUnit_ResolveByFocusHandle` (`0031B7E0`), `PartyConfiguration_ReconcileRosterFromCurrentSelectors` (`003261D0`), `BattleUnit_GetPartyLeader` (`003272A0`), `PartyConfiguration_SetSelectorsAndReconcileRoster` (`003273D0`); `00311E20` calls `PartyRoster_GetActorBySlot` (`0031ABF0`), `003272F0`; `0031ADB0` calls `BattleUnit_ResolveByFocusHandle` (`0031B7E0`), `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`); `00311E20` is called by `PartyFocus_SelectAndRequestDefaultActor` (`00326500`); `00319490` calls `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`); `ActorWork_GetBattleUnit` (`0031B760`) is called by `0030BEB0`; `00326D60` calls `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`).

**Rewards_Progression_Economy — MECHANICAL, 1 edge.** `00319490` is called by `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`).

**Save_Load_Settings — MECHANICAL, 4 edges.** `00583990` is called by `SaveLoad_ControllerTransitionStateMachine` (`00580EB0`), `SaveLoad_ControllerLifecycleHandler` (`00582860`), `SaveLoad_HandleStorageStatusResultAndAdvanceController` (`00583040`); `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (`0030B6A0`) is called by `SaveRuntime_RebindImageBackedGameplayState` (`00238A80`).

**Script_VM_Native_Bridge — MECHANICAL, 5 edges.** `WorldActor_QueryCombatStanceState` (`0030BFB0`) is called by `00343290`, `00344CC0`; `WorldActor_HasActiveBattleActionOrUnitFlag14` (`0030BA30`) is called by `00341070`; `ActorWork_GetBattleUnit` (`0031B760`) is called by `005102D0`; `00660570` is called by `00510740`.

**WorldAreaField — MECHANICAL, 3 edges.** `Battle_EmitReactionPresentationForSlot` (`003176E0`) calls `FieldData_GetActiveFieldRecordBit15` (`00313F60`); `00326D60` calls `FieldData_GetActiveFieldRecordBit15` (`00313F60`); `00329A80` calls `FieldData_GetActiveFieldRecordBit15` (`00313F60`).

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-why-the-unowned-code-has-no-owner-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `006D5940` | 174 B | `008B75A0` + 0x7 | walks the list whose head qword is `02E9FD60` (each node links on to qword `+8`) for the node equal to `rcx` and, when it finds it, stores that node's qword `+8` into the head or the predecessor's `+8` and zeroes it; then, for dword `+0x20` with qword `+0x28` and for dword `+0x10` with qword `+0x18`, calls (`006D5940` + 0x74, + 0x96 respectively) with the qword when bit 31 of the dword is clear and the qword is non-null, and zeroes the qword and the dword in either case | Interior anchor `006D597B`; Interior anchor `006D5998`; Interior anchor `006D59A2`; Interior anchor `006D59B4`; Interior anchor `006D59D6` |
