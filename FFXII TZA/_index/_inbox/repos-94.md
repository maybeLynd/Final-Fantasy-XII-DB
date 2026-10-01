# repos-94 — inbox for merge by repos-55

Block: open question **B-2**, category `24-Compiler-And-CRT-Runtime`.
Program state: GN checkpoint, snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`,
GZF `2ed8affb…c1c00bb9`, EXE `73461d08…d89721f8`. Ledger reproduced 38,161 / 38,003 / 158
(`Verify-GfzCheckpoint.ps1` on `work\proj_h94`, all four stages green) before any analysis ran.

Document landed:
`24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`
— DOCUMENTED, all sections, one recorded falsification pass in §10.
`check_links.py` passes (157 files, 749 links). `verify_doc_addresses.py` green: 62 cited
addresses — 48 entry, 7 interior (`__except` jump targets, correctly interior), 7 data.

No GFZ state was written. No `_index/*.md` was edited. `24-Compiler-And-CRT-Runtime/README.md`
was updated (own category).

---

## COVERAGE

`24-Compiler-And-CRT-Runtime` gains **one** document: 3 total (was 2).

Composition line in that category README is unchanged but is now explained rather than asserted:
of the 3,895 `CompilerGeneratedEH` functions, 3,820 `UnwindFunclet`, 72 `CatchHandler`,
2 `AdjustedObjectCleanup`, 1 `ExceptionFilter`. Total funclet code is **59,914 bytes, 0.75 % of
`.text`**; median body 12 bytes, maximum 158.

Classified-but-not-understood shrinks by 3,895 in the sense that the whole population now has a
mechanism identity resting on complete bodies rather than on Ghidra's `Unwind@`/`Catch_All@`
naming — which was the sole stated evidence in the original GFZ comments
(`EVIDENCE=Function is a Ghidra/MSVC x64 exception-metadata funclet (Unwind@ or Catch_All
family)`), i.e. metadata-derived.

---

## OPEN-QUESTIONS

**B-2 — ANSWERED, with two corrections to the classification it was auditing.**

> Of the 3,895 functions tagged `CompilerGeneratedEH`, **3,893 are genuinely compiler-generated
> funclets**, agreed by two independent instruments: (a) exact-current body shape — 46 distinct
> operand-normalised skeletons covering all 3,895, no metadata read; (b) a structural
> `.pdata → UNWIND_INFO → FuncInfo → UnwindMap/TryBlockMap/scope-table` enumeration of which
> addresses the compiler *declared* as funclets, permitted by EVIDENCE-STANDARD for existence
> only, with its `FuncInfo` magic check passing on all 4,518 records.
> **Two are misclassified** — `001AAF20`, `001AAF50` — and **six genuine funclets are missing
> from the tag** — `0089BEF0`, `008A5AD0`, `008A5B7C`, `008A5B94`, `008A5BB2`, `008A5BDE`.
> Declared-funclet arithmetic: 3,820 unwind + 72 catch + 7 SEH filters = 3,899; minus 6 untagged
> = 3,893 tagged-and-declared; plus the 2 misclassified = the 3,895 tagged.

New questions, all mirrored in the document's §7:

| Proposed ID | Question | Owner doc |
|---|---|---|
| PROPOSED-repos94-1 (B-2/a) | Which empty destructor(s) the linker folded onto `0016D6A0`. Run-time behaviour is proven (`ret`); source identity is not recoverable from the image. | `24-…/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md` |
| PROPOSED-repos94-2 (B-2/b) | Whether the 128 shape-ambiguous funclets can be separated from `atexit` thunks by body evidence alone. Currently they are not; identity rests on tier 8 (no code takes their address) plus the structural parse. | same |
| PROPOSED-repos94-3 (B-2/c) | The 187 lazy statics with no `_Init_thread_abort` funclet are assumed to have non-throwing constructors; not individually verified. | same |
| PROPOSED-repos94-4 (B-2/d) | `006DA980`'s original debug-build behaviour. Strings and call survive; reporting code is `ret`. | same |
| PROPOSED-repos94-5 (B-2/e) | Which of the 250 unclassified funclet parents are game systems. Closing them sharpens "no *owned* gameplay parent" to "none at all". | same |
| PROPOSED-repos94-6 | Concrete identity of `001AAF20`/`001AAF50`/`001952E0`/`00195310` — which class, which virtual base, which slot-`+0x10` method. Kept numeric until proven. | same |

---

## AUDIT-LOG

### Reopening required — `24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`

**Trigger 2/5** (a newly derived fact contradicts a claim the document makes; a higher-tier
measurement is now available for a claim carried by a lower one).

That document states *"117 more are lazy magic statics"* and *"these 117 globals do not exist
until something calls their accessor."* The **mechanism** it describes is exactly right — its
decompiled TLS-epoch gate matches mine instruction for instruction. **The number is wrong.** 117
is the size of the `CompilerGeneratedCpp.ThreadSafeStaticRecordAccessor` tag population, i.e. a
count of functions that received one label — not a census of magic statics.

Measured directly by disassembling all 38,161 bodies from their own entry points:

```
call _Init_thread_header (008092FC) sites : 1,732
call _Init_thread_footer (0080929C) sites : 1,732
distinct functions containing them        :   707
distinct guard variables with an unwind funclet (tail-jump to _Init_thread_abort 0080926C) : 1,545
guard variables, all distinct, in .data   : 01F7F5C8 .. 02EBA258
```

**FFXII TZA has 1,732 lazily-initialised function-local statics across 707 functions**, not 117.
I did not edit that document (it predates my block); it needs `REOPENED`, a corrected §4 and a
propagation check on anything citing its lazy-path count.

*Why the earlier reading was reachable, and where else it hides:* a tag population and a
mechanism census look identical when the tag is all you have. This is the same failure family as
the peer session's `ThirdParty` selector (690 → 801, twelve libraries not eleven) found the same
day. Both are cured by re-deriving the population from the binary instead of re-selecting it from
the classification.

### Instrument defect recorded — a linear `.text` sweep that returned a faithful zero

The first run of the "is any funclet's address taken in code?" test disassembled `.text`
linearly from a single start address. It returned **0 hits for everything, including two known
`atexit` thunks used as positive controls.** It had desynchronised in the first few bytes. Its
answer was numerically identical to the corrected instrument's answer on the quantity of
interest, for entirely the wrong reason. Re-run per function from each known entry point, the
controls fire (`008A81D0` ← `FUN_00160310`, `008A9240` ← `FUN_00160BE0`) and the sweep reproduces
the 1,545 `_Init_thread_abort` tail-jumps already derived independently.
**Nothing about the broken run looked broken.** This is the `strings`-not-installed lesson again,
in a tool we wrote ourselves.

### Claim withdrawn during the pass

"The linker folded every empty function onto one address" — refuted by counting: **34 distinct
addresses in this binary have the body `C2 00 00`**, so folding is partial, not global. The
narrow surviving claim is that at least one empty destructor shares `0016D6A0` with the CFG
check, proven from a body: `Unwind@0089dd0e` passes `0016D6A0` as the *element destructor*
argument of `_eh_vector_destructor_iterator`, which a CFG check cannot be.

### Duplicate work, compared rather than re-announced

Per evidence-standard rule 13 the corpus was grepped first.
`17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md` already identified
`mov rbp, rdx` as the funclet signature and already corrected its own count to "135 functions and
12 funclets". **Confirmed and generalised** — the signature holds across 2,133 bodies. Its
statement "none of the twelve is a `.pdata` `UnwindInfoAddress` target, 0 of 12" is *correct and
not a contradiction*: funclet entry points live in `UnwindMapEntry.action` and
`HandlerType.addressOfHandler`, never in `RUNTIME_FUNCTION.UnwindInfoAddress`, so that test must
return zero. Its 12–13 string-carrying funclets are a subset of the **100** found here by
sweeping every funclet body instead of a pattern list.
`99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md` records a peer
session's structural funclet recovery; this pass reproduces it independently and adds the six SEH
filters a `FuncInfo`-only parse does not reach.

### Selector stated, per the standing lesson

`DumpBodyCorpusByDomain.java` iterates each function's `FunctionTag` **set** and keeps tags
beginning `GFZ.V121.CodeDomain.`, then those continuing `CompilerGeneratedEH`. Set iteration
avoids the composite-tag and CRLF traps. Cross-checked by contents-match over
`work\graph_gn\functions.tsv`: **3,895, symmetric difference 0**; and **no function in the binary
carries more than one V121 `CodeDomain` tag**, so first-match and contents-match cannot diverge.
Adjacent namespaces (`CompilerGeneratedCpp` 417, `CxxObjectLifecycle` 225, `CxxStandardLibrary`
167, `CompilerGeneratedCFG` 145, `Thunk` 689, `Microsoft` 106) are dispositioned explicitly in
the document's §8 rather than left to the tag.

### Noise floors measured before any hit was believed

| signature | matches inside the tag | matches elsewhere in the binary | verdict |
|---|---:|---:|---|
| `lea rcx,[rip+k] ; jmp imm` | 1,620 | **1,328** (static teardown thunks) | not diagnostic |
| bare `jmp imm` | 86 | **749** (`Thunk.InternalForwarder`) | not diagnostic |
| bare `jmp [rip+k]` | 1 | **118** (`Thunk.ExternalImport`) | not diagnostic |
| "a frame register is loaded from RDX" | 419 | **3,133** | not diagnostic |
| the full group-A prologue (`push rbp ; sub rsp,N ; mov rbp,rdx`, or `(lea\|mov) rcx,[rdx+d] ; jmp`) | 2,133 | **6**, all inspected and rejected | diagnostic |

The 6, each opened individually: `00467D20` (Presentation, 817 B), `007F5CC0` (Audio, 1,460 B),
`007FC620` (Audio, 802 B), `0087F7F0` (`ThirdParty.Physics.Bullet`, 876 B), `00891C80`
(`ThirdParty.Audio.LibVorbis`, 686 B), `00892610` (Audio, 888 B). All use RCX as `this` and RDX
as a real second argument; none is a declared funclet; all are hundreds of bytes against a
funclet median of 12. `00892610` is the only one that reaches `mov rbp,rdx` at all, at `+0x24`,
after nine pushes and two reads through RCX — arg2 parked in a callee-saved register, not an
establisher frame.

---

## CALL-CHAINS / ADDRESS-INDEX

### New cross-subsystem edges — these will show up as `UNACCOUNTED NEIGHBOUR` if not registered

The funclet block enters **827 distinct non-EH functions**. **98 of those transitions land on a
function carrying a V120 `PrimaryOwner`:**

| destination owner | transitions |
|---|---:|
| Resource | 58 |
| Audio | 35 |
| Platform / Online / Achievements | 3 |
| Input | 2 |

These are cleanup calls on a failure path. Recommended disposition for Resource/Audio/Input
documents: *by reference* to
`24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md §5`,
which enumerates them — not by absorbing the census.

### Parent census (upstream side), 1,609 distinct parent functions

Owned parents (246): Resource 182 · Audio 41 · Input 11 · Save/Load/Settings 5 ·
Platform/Online/Achievements 4 · Presentation 2 · CoreRuntimeScheduling 1.
By mechanism: Phyre 613 · NativeRoutine 386 · unclassified 250 · ThirdParty 81 · Runtime 44 ·
NativeDispatch 44 · CxxStandardLibrary 40 · CompilerGeneratedCpp 34 · Presentation 29 ·
NativeAdapter 18 · Boundary 17 · Microsoft 13 · EASTL 10 · NativeInline 10 · Platform 9 ·
Media 5 · Application 2 · Bullet 2 · CxxObjectLifecycle 1 · StoryEvent 1.

**No Combat, Movement, Party, Actor, Spawn, Gambit or Script parent exists.** FFXII throws only
where it touches the outside world.

### ADDRESS-INDEX additions

| Address | Name | Note |
|---|---|---|
| `0080926C` | `_Init_thread_abort` | tail target of 1,545 funclets; releases a lazy-static guard |
| `008092FC` | `_Init_thread_header` | 1,732 call sites, 707 functions |
| `0080929C` | `_Init_thread_footer` | 1,732 call sites |
| `00809364` | `_Init_thread_notify` | |
| `008093C0` | `_Init_thread_wait` | the 100 ms retry |
| `02EAED40` | `_Init_thread_lock` | one `CRITICAL_SECTION` for all 1,732 |
| `01F44850` | `_Init_global_epoch` | |
| `00861EB4` | `__CxxFrameHandler3` thunk | personality of 4,377 functions |
| `00861ED8` | `__C_specific_handler` thunk | personality of 9 functions |
| `00808BA8` | `__GSHandlerCheck` | 5,372 functions |
| `00808F64` | `__GSHandlerCheck_EH` | 141 functions |
| `00861EAE` | `__std_terminate` thunk | `noexcept` boundary; 86 funclets jump here |
| `00861ECC` | `_CxxThrowException` thunk | 8 catch funclets rethrow through it |
| `00896270` | `_guard_dispatch_icall` | from load-config slot `008C31C8` |
| `0016D6A0` | `_guard_check_icall` + folded empty destructor(s) | body is `C2 00 00`; 172 funclets jump here |
| `006DA980` | stripped ppfx diagnostic reporter | body `C2 00 00`; 99 funclets still pass `__FILE__`/`__LINE__` |
| `00896280`–`008A6960` | the funclet block | 3,892 of the 3,895 tagged, contiguous |

---

## Rows worth applying (manifest input for the coordinator — I did NOT run Apply-GfzBatch)

Six declared funclets currently carrying a generic shape tag. Each is a **declared SEH filter**
(from the `__C_specific_handler` scope table) whose body is CRT `__ArrayUnwind` scaffolding or a
process SEH filter. Pre-enrich rows, 4 columns, `EnrichCurrentBodyManifest` to compute column 7 —
do **not** copy any prose hash:

```
0089BEF0	CodeDomain	CompilerGeneratedEH.ExceptionFilter	Complete current body is 'return 0xFFFFFFFF'; declared as the filter of parent 005CD1E0 in a __C_specific_handler scope table; sits inside the contiguous funclet block 00896280-008A6960.
008A5AD0	CodeDomain	CompilerGeneratedEH.ExceptionFilter	Complete current body tail-calls FUN_005CCBF0; declared as the filter of parent 005CCBA0 in a __C_specific_handler scope table.
008A5B7C	CodeDomain	CompilerGeneratedEH.ExceptionFilter	Complete current body is 'return *(int*)*p == 0xC0000005' (STATUS_ACCESS_VIOLATION); declared as the filter of parent 00808A54.
008A5B94	CodeDomain	CompilerGeneratedEH.ExceptionFilter	Complete current body calls _seh_filter_exe(code, p); declared as the filter of parent 00808D78.
008A5BB2	CodeDomain	CompilerGeneratedEH.ExceptionFilter	Complete current body is the guarded __ArrayUnwind re-entry 'if (frame[0x20]==0) __ArrayUnwind(...)'; declared as the filter of parent 00808FE4; matches MSVC CRT eh\arrayunwind upstream source.
008A5BDE	CodeDomain	CompilerGeneratedEH.ExceptionFilter	Complete current body is the guarded __ArrayUnwind re-entry with a different frame layout; declared as the filter of parent 00809054; matches MSVC CRT eh\arrayunwind upstream source.
```

**Two rows that should be REMOVED or re-domained rather than added** — I am not proposing a
mutation for these, only flagging them, because their true identity is not yet proven and
"unresolved" beats a wrong label:

```
001AAF20	currently CompilerGeneratedEH.AdjustedObjectCleanup	NOT a funclet
001AAF50	currently CompilerGeneratedEH.AdjustedObjectCleanup	NOT a funclet
```

Both take `this` in RCX, never read RDX, and are absent from the declared-funclet enumeration.
Their 45-byte bodies are **byte-identical** to `001952E0` and `00195310`, which are tagged
`Microsoft.MSVCCRT_STL_Runtime.Support` — four exact clones, two incompatible classifications.
The shared body is a virtual-base-adjusted virtual dispatch:

```c
void f(longlong *this) {
    longlong *nested = *(longlong **)( *this
                                     + (longlong)*(int *)(*(longlong *)*this + 4)  // signed vbase offset
                                     + 0x48 );
    if (nested) (**(code **)(*nested + 0x10))();
}
```

Deciding which of the four tags is right needs the class identity (PROPOSED-repos94-6), so I
recommend leaving all four alone until then rather than propagating either label.

---

## Scratch (mine, under Tools/work/h94)

`scripts/DumpBodyCorpusByDomain.java` (read-only Ghidra dump of exact-current body bytes for all
38,161 functions plus full bodies for the tagged set) · `scripts/skel.py`, `consolidate.py`
(operand-normalised skeleton clustering) · `scripts/ehparse.py` (structural funclet enumeration
with the `FuncInfo` magic validity check) · `scripts/resolve.py`, `callsites.py` ·
`eh_bodies.tsv`, `eh_full.tsv`, `eh_skeletons.tsv`, `declared_funclets.txt`,
`notag_funclets.tsv`, `decomp1.txt`–`decomp3.txt` (128 decompiled bodies).
`work\proj_h94` / `GFZ_H94` is mine and is closed; no GFZ state was written.

---

# repos-94 — second block (BI-1 + the lazy-static document)

Same program state: snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`.
No GFZ state written. No `_index/*.md` edited. Category 24 files only.

**Gates green:** `check_links.py` 166 files / 783 links, all resolve.
`verify_doc_addresses.py` on all three category-24 documents: **ok, 0 ghosts, 0 drift** —
85 entry, 15 interior, 46 data citations.

## COVERAGE

`24-Compiler-And-CRT-Runtime` gains **one** document: **4 total** (was 3).
New: `Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md` — DOCUMENTED,
tier 1, one falsification pass.

## OPEN-QUESTIONS

**BI-1 — CLOSED.** `static-initialization-order-and-injection-timing.md` reopened, corrected and
returned to DOCUMENTED with the trail in its new **section 12**. `reopened_count: 1`, `passes: 5`,
`last_pass_state` advanced to the snapshot it was actually re-verified against.

> The lazy count is **1,681 distinct thread-safe function-local statics, at 1,732 guarded
> construction sites, across 707 functions** — not 117. 1,545 have an `_Init_thread_abort` unwind
> funclet; 136 do not. The 117 figure is the `CompilerGeneratedCpp.ThreadSafeStaticRecordAccessor`
> tag population, and it is *a true subset*: all 117 do hold a lazy static, because the tag fires
> exactly when the accessor is the whole function. The other 590 holders have one buried inside a
> larger routine (Phyre 224, `NativeRoutine` 167, untagged 150, `CompilerGeneratedCpp` 140, 26
> others) and were labelled by what the larger routine looks like.

**Propagation check: complete, and it terminates.** Every `117` in the database was inspected. The
figure appears only in that document and in the two places flagging the correction. The other
matches are unrelated quantities — Phyre class counts, body sizes in bytes, a licence-board row
range. **No downstream document inherits it, so nothing further reopens from BI-1.**

New questions for the lazy-static document, all mirrored in its section 7:

| Proposed ID | Question |
|---|---|
| PROPOSED-repos94-7 (BJ-1) | Which of the 1,681 are reached on a normal boot vs only in specific areas or menus. Needs runtime evidence; static reading cannot answer it. |
| PROPOSED-repos94-8 (BJ-2) | Identity of `01F44830`. It is the CRT pointer-encoding cookie here, read from 2,229 functions at 2,383 sites — but that does not match the 5,372 functions registering `__GSHandlerCheck`, so calling it `__security_cookie` is unproven. |
| PROPOSED-repos94-9 (BJ-3) | Whether the event-fallback path in `_Init_thread_wait` is ever taken on a supported OS. `02EAED70` is set by the CRT, not visible statically. |
| PROPOSED-repos94-10 (BJ-4) | The meaning of the `typeId` constants passed to `00632960` (`0x12` and friends). Closing this turns the 890 recovered field-name strings into a real schema. |
| PROPOSED-repos94-11 (BJ-5) | The 107 holder functions that call neither a reflection routine nor `atexit`: what their lazy statics are. |

## AUDIT-LOG

### Three findings from repos-55 against the funclet document — all three fixed

1. **Dangling forward link** to `../Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md`.
   Cause: I wrote the forward reference into the reopened document before its target existed.
   Fixed by writing the target. `check_links` green. **Lesson taken:** a forward link is a broken
   link until the file exists, and link-check is a shared gate — never leave one across a turn.
2. **GHOST ADDRESS `01F44850`.** Correct finding. Section 3 of the funclet document listed
   `_Init_global_epoch`, a `.data` global, in the function table with a `4 B` size column. Both
   category-24 documents I own now follow the new `_templates/SYSTEM.md` section-3 split: a
   function table, and a separate **Data addresses** block with no size column. Seven data
   addresses moved in the funclet document, ten in the lazy-static document.
3. **BODY DRIFT `00896280` — 59,914 B vs 12 B.** The diagnosis from repos-55 was right: it was a
   span recorded as a body. The row read `00896280 – 008A6960 | the funclet block | 59,914 B`, so
   the checker took the first address as a function and the block total as its extent. `00896280`
   is a real 12-byte funclet (`lea rcx,[rip+guard] ; jmp _Init_thread_abort`); 59,914 is the **sum
   of 3,895 individual body extents**, a correct number wearing the wrong label. Now split into
   two exact function rows (first and last funclet, 12 B each) plus a prose line stating that the
   59,914 is a sum. **I re-checked the rest of both tables for the same defect and found no other
   range sitting in an address column.**

### A correction I made to my own document before repos-55 saw it

The funclet document first said "1,732 lazily-initialised statics" and "187 without a funclet".
That conflated **sites with objects**. Resolving the guard operand at each of the 1,732
`_Init_thread_header` sites — the `lea rcx,[rip+g]` immediately preceding the call, 1,732 of 1,732
resolved, all landing in `.data` — gives **1,681 distinct guards**; 19 are multi-site, always
across different functions, accounting for the 51 difference exactly. Corrected figures: **1,681
objects, 1,732 sites, 136 without a funclet.** Recorded in that document's section 8 rather than
silently rewritten. Note this is the *same failure family* as BI-1 one level down: a count of the
wrong noun. The funclet-side 1,545 was never affected, and the two sets reconcile with zero
orphans in either direction.

### Instrument note

The guard census has a built-in validity check worth reusing: every resolved guard must land in
`.data`. A misaligned or mis-scanned back-search produces out-of-section garbage, and produced
none — 1,732 of 1,732 in `.data`. That is a check that fails loudly, which
`EVIDENCE-STANDARD.md` prefers over a control.

## CALL-CHAINS / ADDRESS-INDEX

### New: the lazy-static chain

```
first touch of a type or singleton
  -> guarded block (1,732 sites / 707 functions)
     -> _Init_thread_header 008092FC -> EnterCriticalSection 02EAED40
        guard == -1 -> _Init_thread_wait 008093C0 -> SleepConditionVariableCS(02EAED68, 02EAED40, 100)
     -> constructor
        -> Phyre reflection registration 00632960 / 00630180 / 006388C0   (535 of 707 holders)
        -> atexit 00808B90                                               (526 of 707 holders)
     -> _Init_thread_footer 0080929C -> bump 01F44850 -> _Init_thread_notify 00809364
     (on a throw) -> the guard's unwind funclet -> _Init_thread_abort 0080926C
process exit -> the atexit chain, reverse registration order
```

Holder ownership (upstream side): only **150 of 707** carry a V120 `PrimaryOwner` — **Resource
149, Platform/Online/Achievements 1**. By mechanism: Phyre 224, `NativeRoutine` 167, untagged 150,
`CompilerGeneratedCpp` 140, `Boundary` 10, `ThirdParty` 10, 6 others. Worth flagging to the
Resource documents: **149 Resource-owned functions contain a lazy static**, which is a real
constraint on where a mod may safely hook, not merely a classification fact.

### ADDRESS-INDEX additions

| Address | Name | Note |
|---|---|---|
| `02EAED68` | `_Init_thread_cv` | condition variable a blocked thread sleeps on |
| `02EAED70` | one-time-init fallback event | zero on the condition-variable path |
| `02EAED78` / `02EAED80` | encoded `SleepConditionVariableCS` / `WakeAllConditionVariable` | decoded `ROR64(cookie ^ slot, cookie & 0x3F)` |
| `01F44830` | CRT pointer-encoding cookie | 2,229 functions, 2,383 sites; identity open as BJ-2 |
| `00808B90` | `atexit` | 23 B; forwards to `_onexit` |
| `00632960` | `Phyre.Reflection.DataMemberRegistration` | 165 B; writes `Phyre::PClassDataMember::vftable`, registers through descriptor virtual slot `+0x40` |
| `006388C0` | `Phyre.Reflection.TypeNameRegistry` | 254 B; hash `h = 0x7B5; h = h*0x21 + (c & 0x1F)` — **case-insensitive by construction**, only the low 5 bits of each character contribute |
| `005AD8F0` / `005E5400` | heaviest lazy-static holders | 5,580 B / 4,088 B; 28 guarded statics each |
| `00189CE0` | worked example | guard `01F7F5C8`, funclet `Unwind@008964A0` |

## Still staged with you, untouched

The six `CompilerGeneratedEH.ExceptionFilter` pre-enrich rows (BI-7). I have not run
`Apply-GfzBatch.ps1` or `Pack-GfzCheckpoint.ps1` and will not.

---

# repos-94 — third block (category 22, BJ-4 + BK-8 + BK-9)

Same program state: snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`.
No GFZ state written. No `_index/*.md` edited.

**Gates green:** `check_links.py` 169 files / 810 links, all resolve.
`verify_doc_addresses.py` on the new document and the two it corrects: **ok, 0 ghosts, 0 drift.**

**Question-drift housekeeping:** I checked `check_questions.py --drift` for my share and there is
none. The 26 items are 23 duplicate ledger IDs (`BC-*`, `BD-*`, `BE-*`, `BG-*`, `BH-*`) plus three
cross-check items in `input-stack-device-channel-and-bindings.md` (2 STALE) and
`gi-render-command-family.md` (1 EARLY). None is in a document I own, so I left them.

## COVERAGE

`22-Middleware-PhyreEngine` gains **one** document: **5 total** (was 4). New:
`Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md` —
DOCUMENTED, tier 1, one falsification pass.

Artifact for reuse: `Tools/work/h94/phyre_schema.tsv` — 682 rows of
`class · member · offset · type · attrs · site`, the recovered schema in full.

## OPEN-QUESTIONS

**BJ-4 — ANSWERED, and its premise was wrong. There is no type id.**

> `00632960` is `PClassDataMember_Register(record, owner, PType *memberType, name, offset, attrs,
> flag2, ctx)`. The fifth argument is a **byte offset of the field inside the owning object**, not
> a size. The sixth is an **attribute bitfield**, not a type code. The field's type is the **third**
> argument, a pointer to a `PType` — a shared `PTypeDefault<T>` singleton for primitives, or the
> class descriptor of the field's own type for object fields.
>
> **Attribute bits, decoded:** bit 0 (`0x01`) = the name string is heap-copied and must be freed
> (proven from `00632FB0`, and it closes a loop with the existing document's teardown reading of
> byte `+0x28` bit 0 — construction and destruction agree, derived independently); bit 1 (`0x02`)
> = the field is stored as a **pointer** to another reflected object, never set on any of 254
> primitive-typed fields; bits 3–4 (`0x18`) = a **per-class constant**, undecoded, filed as BL-1.
>
> **Recovered: 682 field records over 173 named classes, 465 distinct field names, 97 distinct
> field types, with exact byte offsets.** The primitive set falls out of the `PTypeDefault<T>`
> RTTI names via MSVC mangling: `unsigned int` 224, `float` 96, `unsigned char` 29, `int` 26,
> `unsigned short` 19, `bool` 16, `short` 1.

**BK-9 — ANSWERED.** The `h*0x21 + (c & 0x1F)` type-name hash *is* case-insensitive by
construction, and **the engine handles collisions correctly.** `006311D0` walks an ordered tree
using the hash as the key, and when two hashes compare equal it falls through to a byte-by-byte
string comparison, returning a hit only on a full match. The hash is an ordering key, never an
identity. Whether any two real type names actually collide is now only a curiosity — filed as
BL-6, not a risk.

**BK-8 — folded in**, in the new document's §6 and in the lazy-static document: 149 of the 150
owned lazy-static holders are Resource-owned, so a shared-world mod's natural hook sites are
disproportionately inside one-time-init regions.

New questions for the schema document, all mirrored in its §7:

| Proposed ID | Question |
|---|---|
| PROPOSED-repos94-12 (BL-1) | What attribute bits 3–4 (`0x00`/`0x08`/`0x10`) mean. Established: constant per class across all 146 measured, and **not** the descriptor template kind (tested, refuted). |
| PROPOSED-repos94-13 (BL-2) | The `flag2` argument. Compared against `2`; when equal it sets attribute bit 1 **for the duration of the attach call only**, restoring it afterwards. Why the bit is set transiently is unknown. |
| PROPOSED-repos94-14 (BL-3) | The 2 of 682 registrations that are *not* inside a guarded region. |
| PROPOSED-repos94-15 (BL-4) | The 89 sites whose owning class did not resolve and the 53 whose type did not — real registrations, pointer chain not followed. |
| PROPOSED-repos94-16 (BL-5) | What the second intrusive list at record `+0x38` links. The first, at `+0x08`, is the class's member list. |
| PROPOSED-repos94-17 (BL-6) | Whether any two registered type names actually collide under the `& 0x1F` hash. |

## AUDIT-LOG

### A question filed on a wrong premise, and where the wrong premise came from

BJ-4 asked what the `typeId` constants mean. **There are no typeId constants.** I filed that
question myself, from a decompiled call whose positional arguments I took at face value without
reading the callee. Reading `00632FB0` — 25 lines — shows the sixth argument being stored as a
flags word and tested against bit 0, and reading the layout shows the fifth being an offset.

The general form is worth recording: **a decompiler's argument list is a claim about a signature,
not a signature.** Ghidra printed `(undefined8, longlong *, undefined8, undefined8, undefined4,
undefined4, int, undefined8)` and I supplied the nouns. Two of my three nouns were wrong, and they
were wrong in a way that *looked* right — `0x20` is a plausible size and `0x12` is a plausible
enum. The check that caught it was cheap and structural: **sort the recovered values per class and
see whether they form a layout.** Floats 4 apart, pointers 8 apart, two single-byte fields in
adjacent bytes. A size column cannot do that.

### Extended, not overturned — the sibling reflection document

`class-descriptor-and-metadata-system.md` §2 says each class "gets a global descriptor singleton,
constructed by a generated initializer at process start". **Correct for the descriptor object,
incomplete for its contents:** 680 of the 682 member registrations execute behind a
one-time-init guard. A descriptor therefore exists from startup **with an empty member list**,
which fills in on first touch. I added a marked note in place rather than rewriting the section,
and the document's `atexit` pairing proof is untouched. It is an extension, not a reopen — no
claim it makes is false.

### Two corrections to my own lazy-static document

Its worked example read the same call as "32 bytes wide, of type 0x12". Both wrong; corrected in
place with a marked note, and BJ-4 ticked in its §7 with the answer.

### Hypothesis tested and refuted, recorded rather than softened

Attribute bits 3–4 are constant per class, so the obvious reading is that they encode the
descriptor template kind. **Tested against the recovered class names and refuted** —
`PClassDescriptorConcrete` classes take all three values (229 / 118 / 21). Filed as BL-1
unresolved. This is the case the standard warns about: the plausible sentence was available and
would have gone unchallenged.

### An extraction artefact I looked for and did not find

The per-class constancy of bits 3–4 would be manufactured if MSVC hoisted the constant store and
my backward scan reused one value for every call in a function. **Tested: 339 of the 484 resolved
values come from non-first registrations**, so the store is re-emitted per call, and 39 functions
show two values differing only in bit 1 — which a hoisting artefact could not produce.

### Cross-method agreement worth noting

The class and type *names* come from joining `object -> vftable -> class` against
`Tools/work/rtti/vtables.tsv`, recovered by a different session using a different method. 629 of
682 type pointers resolved to a named class, every primitive resolved to a `PTypeDefault<T>` with
a valid MSVC mangling code, and nothing resolved to something structurally impossible. That
agreement is the check on both sides.

## CALL-CHAINS / ADDRESS-INDEX

### New chain: lazy reflection registration

```
first touch of a reflected class
  -> its registration function (248; 246 are lazy-static holders)
     -> _Init_thread_header 008092FC
        -> per field:  PType *t = <the field type's own lazy accessor>()
                       PClassDataMember_Register 00632960
                         -> PClassDataMemberBase_Construct 00632FB0
                         -> owner->vslot[+0x40](owner, record, ctx)
        -> _Init_thread_footer 0080929C
  -> consumers walk the member list: binary serialisation, the animation channel binder,
     the script property bridge, resource binding
```

**Cross-category edge to register:** `22-Middleware-PhyreEngine` reflection registration →
`24-Compiler-And-CRT-Runtime` one-time-init machinery, 680 sites. The two documents cite each
other. Also worth linking: the **Animation-Channel-Binding** document is the consumer side of this
schema — its binder resolves dotted member paths against exactly these records — and I have cited
it; it may want a reciprocal link when it next takes a pass.

### ADDRESS-INDEX additions

| Address | Name | Note |
|---|---|---|
| `00632960` | `PClassDataMember_Register` | 165 B; the single field-registration entry point, 682 call sites |
| `00632FB0` | `PClassDataMemberBase_Construct` | intrusive list + owner + name + attribute word; owns the name copy on bit 0 |
| `006388C0` | `PType_FindOrRegisterByName` | 254 B; hash `h = 0x7B5; h = h*0x21 + (c & 0x1F)` |
| `006311D0` | `PType_LookupByHashThenString` | ordered-tree walk; hash key, full `strcmp` tiebreak — the collision answer for BK-9 |
| `00637440` | registry root accessor | supplies the tree root |
| `005AD8F0` / `005E5400` | heaviest registration functions | 5,580 B / 4,088 B, 28 guarded statics each |

`PClassDataMember` layout: `+0x00` vftable · `+0x08`/`+0x10` intrusive node · `+0x18` owning
descriptor · `+0x20` name · `+0x28` attribute bitfield · `+0x30` `PType *` · `+0x38`/`+0x40`
second list · `+0x48` **field offset** · `+0x50` zero.

## Still staged with you, untouched

The six `CompilerGeneratedEH.ExceptionFilter` pre-enrich rows (BK-7). No `Apply-*`, no `Pack-*`.

---

# repos-94 — fourth block (BL-4 closed, BL-2 answered, BL-1 narrowed)

Same program state: snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`.
No GFZ state written. No `_index/*.md` edited.

**Gates green:** `check_links.py` 172 files / 833 links. `verify_doc_addresses.py` on the schema
document: ok, 0 ghosts, 0 drift (16 entry, 3 data).

## COVERAGE

No new document — the schema document is extended in place, and the sibling class-descriptor
document gains a unit correction. Overall database progress after this block:

```
engine_explained   [#######.................................]  17.08%   5852 / 34270
ledger_resolved    [########################################]  99.54%   34112 / 34270
audit_coverage     [######################################..]  93.75%   75 / 80
questions_closed   [########................................]  19.80%   100 / 505
final_audits       [........................................]   0.00%   0 / 30
OVERALL            [##################......................]  44.35%
```

## OPEN-QUESTIONS

**BL-4 — CLOSED.** The 89 unresolved owning classes and 53 unresolved types were never missing
data. They were argument values a *backward* scan could not follow: register-to-register copies
through callee-saved registers, stack spills, and pointers loaded from a global another function
had filled in. Replacing the scan with a **forward abstract interpreter** — registers and stack
slots carrying symbolic values, calls clobbering the volatiles and putting `('ret', callee)` in
`rax` — resolves **680 of 682 sites completely**: class, field name, byte offset, attribute word
and field type.

> **The schema is now 680 fully-resolved field records over 246 named classes and 109 field
> types**, up from 467 over 173. `Tools/work/h94/phyre_schema.tsv` regenerated.
> `PScene::VPNode` is now complete and carries the minimal pair that proves attribute bit 1:
> `m_worldMatrix` (attrs `0x12`) is a **pointer**, 8 bytes at `+0x18`; `m_localMatrix` (attrs
> `0x10`) is a **`VPMatrix4` stored inline**, 64 bytes at `+0x20`, with `m_name` next at `+0x60`.

**BL-2 — ANSWERED for this binary.** `flag2` is **`0` at all 680 resolved sites**, so the
`if (flag2 == 2)` branch in `00632960` — which would set attribute bit 1 for the duration of the
attach call and restore it afterwards — is **dead code here**. Why the transient set exists at all
is a PhyreEngine question, not an FFXII one.

**BL-1 — narrowed, and one of my own claims about it broke.** See AUDIT-LOG.

**BL-5 — narrowed.** The *first* intrusive list on a member record, at `+0x08`/`+0x10`, is the
class's member list; proven from the attach path. That path never touches `+0x38`, so the second
list is still unidentified.

**BL-7 stays open and is the cheapest high-value item in the database** — agreed, and I have put
it in the document's §7 in those terms.

## AUDIT-LOG

### A claim of mine broke when the sample got bigger

I wrote that attribute bits 3–4 are "constant across every field of a class in **all 146 classes
measured**". With all 680 sites resolved the measurement is **243 of 246**, and there are three
genuine counterexamples: `PGeometry::VPDataBlockD3D11` and `PGeometry::VPIndexDataBlockD3D11`,
each pairing an `0x08` offset-into-a-buffer field with an `0x00` size field, and
`PHierarchy::VPOctreeWorld`, four `0x00` value fields against two `0x08` octree pointers.

**The 146-class sample supported a stronger claim than the data did**, and it was not a biased
sample in any way I could have spotted — it was simply the subset my instrument could resolve.
Worth adding to the standing lesson beside the tag-population one: *a claim measured over the
resolvable subset is a claim about the instrument as much as about the binary.* Also new: the
value `0x00` appears 196 times and had never been seen, because those were exactly the sites that
did not resolve. The bit mask is still `0x1A`.

### The new instrument was checked against the old one, not simply believed

Before using any of the 491 new values I diffed pass 3 against pass 2 field by field:
**0 disagreements, 0 losses**, every one of the 484 attribute / 523 offset / 593 class / 629 type
values reproduced identically. A rewritten extractor that "just resolves more" is exactly the
shape of a tool that has started guessing.

Two bugs found and fixed on the way, both of which produced *quiet* wrong answers rather than
errors: `regs[nm] = src if src else regs.pop(nm, None)` assigns `None` when the source is unknown,
and the `ret` handler sat below an `if not ops: continue` guard — `ret` has no operands, so it
never ran and the accessor map came back empty. The visible symptom of the second was
"accessors returning a fixed object: 0", which is the kind of zero that looks like a finding.

### Two confirmations from the consumer side, which I had not read before

Reading the attach path — descriptor virtual slot `+0x40`, the same function `0062EFD0` on
**1,186 of 1,187** descriptor vtables — corroborates both of the BJ-4 findings from code that has
nothing to do with registration:

- **The offset is validated arithmetically:** `capacity < (fieldOff - baseOffset) + width + used`.
  A size cannot be used that way.
- **Attribute bit 1 means pointer:** `FieldStorageWidth` (`0063C0C0`) reads the attribute word and
  returns literally `8` when bit 1 is set, and otherwise the type's inline size read from
  `type+0x38`.

And a negative worth keeping: **the attach path never reads bits 3–4**, which rules out the most
attractive remaining hypothesis for BL-1 — that they select which of the descriptor's lists a
field is attached to.

### Unit error in `class-descriptor-and-metadata-system.md` — corrected in place

Its §2 and §4 give the `PClassDescriptor` layout with four intrusive lists at `+0x10`, `+0x12`,
`+0x14`, `+0x16`, the class name at `+0x0C` and a counter at `+0x1D`. **Those are qword indices,
not byte offsets** — the decompiler prints `param_1[0x10]` on an `undefined8 *` and the index was
transcribed as an offset. In bytes the lists are `+0x80`, `+0x90`, `+0xA0`, `+0xB0`, confirmed
independently by the attach path (`cls+0x80`, tail `cls+0x88`) and the reset helper `0063D550` —
which re-initialises **six** lists, so there are two more at `+0x50` and `+0x60` that the
destructor does not walk. The class name is at byte `+0x60`, the sub-object at `+0x70`, the
counter at `+0xE8`.

**This one has a practical cost:** a modder using `+0x0C` as a byte offset reads the wrong memory.
I added a marked correction block in place rather than rewriting the table, since the *structure*
that document describes is right and only the unit is wrong. It is the same defect class as a
`GHOST ADDRESS`: a printed reading that is not physically what it claims to be.

## CALL-CHAINS / ADDRESS-INDEX

### The attach path

```
PClassDataMember_Register 00632960
  -> owner->vslot[+0x40]  ==  0062EFD0  (1,186 of 1,187 descriptor vtables)
     -> FieldStorageWidth 0063C0C0   -> type->vslot[+0x08], or type+0x38, or 8 if attrs bit 1
     -> FindMemberByName  00597220   -> walks cls+0x80 and the base chain at cls+0x78
     -> link record+0x08 into the list at cls+0x80 (tail cls+0x88)
  return 0 attached | 5 exceeds the class storage budget | 0x12 duplicate name | 0x15 no name
```

### ADDRESS-INDEX additions

| Address | Name | Note |
|---|---|---|
| `0062EFD0` | `PClassDescriptor::AttachMember` | descriptor vslot `+0x40`; validates `capacity < (fieldOff - baseOffset) + width + used` |
| `0063C0C0` | `FieldStorageWidth` | returns 8 when attribute bit 1 is set, else the type's inline size from `type+0x38` |
| `00597220` | `FindMemberByName` | walks `cls+0x80` and the base chain at `cls+0x78`, byte-by-byte name compare |
| `0063D550` | descriptor list reset | re-initialises six intrusive lists: `cls+0x50/0x60/0x80/0x90/0xA0/0xB0` |
| `00639290` | attach wrapper | the single descriptor whose slot `+0x40` differs |

`PClassDescriptor` corrected byte offsets: `+0x38` storage capacity · `+0x50`/`+0x60` two
unwalked lists · `+0x60` class name · `+0x70` sub-object · `+0x78` base-class chain · `+0x80`/`+0x88`
member list head/tail · `+0x90`/`+0xA0`/`+0xB0` three more lists · `+0xE8` counter ·
`+0xF4` base offset · `+0xF8` used bytes · `+0x100`/`+0x102` member counters.

## Still staged with you, untouched

The six `CompilerGeneratedEH.ExceptionFilter` pre-enrich rows (BK-7). No `Apply-*`, no `Pack-*`.
BK-3 (PostEffects paths) still open and unassigned.

---

# repos-94 — fifth block (BL-5 structurally answered; a correction of mine was wrong)

Same program state: snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`.
No GFZ state written. No `_index/*.md` edited.

**Gates green:** `check_links.py` 174 files / 849 links. `verify_doc_addresses.py` on both
category-22 reflection documents: ok, 0 ghosts, 0 drift. `check_layout_units.py --self-test`
passes (2 hits on the synthetic block, 0 on the real one) and the live run is clean.

```
engine_explained   [#######.................................]  17.12%   5866 / 34270
ledger_resolved    [########################################]  99.54%   34112 / 34270
audit_coverage     [#####################################...]  92.68%   76 / 82
questions_closed   [########................................]  19.34%   100 / 517
final_audits       [........................................]   0.00%   0 / 30
OVERALL            [##################......................]  44.19%
```

## OPEN-QUESTIONS

**BL-5 — structurally answered, semantically open.** The member record's second intrusive list at
`+0x38`/`+0x40` is **owned by the record**: self-linked empty at construction, never touched by
attach or detach, and cleared at teardown through `006B6700`, a generic list-unlink loop. Nine
reflection teardown helpers do the same, one per member-record kind. **What it holds is not
established**, and neither is whether anything in this binary ever puts a node in it: nothing on
the registration path adds to it, and `00632960`'s return value is used at only **2 of 682** call
sites. The scan I built to settle that failed its own positive control — see AUDIT-LOG.

The body that answers it, `00633240`, also confirms three things this document had derived
separately: the owner pointer at member `+0x18`, the name at `+0x20`, and attribute bit 0 meaning
"free the heap-copied name". A still-linked member detaches itself by calling **its owner's**
virtual slot `+0x48`, which is `0062F080`, the exact inverse of `AttachMember`.

**New: PROPOSED-repos94-18 (BL-8)** — the class descriptor's other five intrusive lists (`+0x50`,
`+0x60`, `+0x90`, `+0xA0`, `+0xB0`). Only `+0x80`, the member list, is identified. The destructor
walks four of them and clears `+0x60`; the reset helper `0063D550` touches all six.

## AUDIT-LOG

### My own correction to the sibling document was wrong, and wrong in the way it warned about

Last block I corrected `class-descriptor-and-metadata-system.md` for transcribing qword indices as
byte offsets, and in the same note asserted that "the class name is at byte `+0x60`, the sub-object
at `+0x70` and the counter at `+0xE8`". **I reached those by multiplying that table's own
mislabelled indices by 8** — arithmetic on the very table I was correcting — and then presented
the result as fact rather than deriving it.

Two of the three hold: `+0x70` and `+0xE8` appear directly in the destructor's operands. **The name
does not.** Byte `+0x60` is a sixth intrusive **list**, self-linked by the reset helper and cleared
in the destructor by `006B6700` — which is a list-unlink loop, not the "embedded-string
destructor" the original table called it. **The type name is a plain `char *` at byte `+0x30`**,
loaded by `PType_FindOrRegisterByName` (`006388C0`) as `mov rsi,[rcx+0x30]`, with an early return
when it is null and the hash taken over the bytes it points at.

So the original table was wrong about the *kind* of that field as well as the unit, and my
correction inherited the error by trusting its labels while fixing its arithmetic. Corrected in
place, with the first version of the note quoted rather than deleted. **The lesson is narrow and
worth keeping: a correction derived from the artefact being corrected is not a correction.**

### A scan that failed its own positive control, and was therefore discarded

To answer "does anything ever insert into the member's `+0x38` list?" I scanned for the circular
insert idiom with head `+0x38` and tail `+0x40`. It returned nine candidates. **The control
failed**: the identical test against the head/tail pair the attach function demonstrably uses
(`+0x80`/`+0x88`) did **not** return `0062EFD0`. An instrument that cannot find the case I already
know about cannot be trusted on the case I do not, so the nine hits are discarded and BL-5 stays
open. Likely cause: the idiom's `lea` and its tail store do not share a base register in the
compiled form, which my test required.

I had also run a broader variant first — "functions storing to each list's tail displacement" —
which returned 159 to 425 functions per list. That is a displacement shared by thousands of
unrelated structures and has no discrimination at all; I discarded it before drawing anything from
it rather than after.

### A fifth independent check on the recovered offsets

Descriptor virtual slot `+0x50` is a **default-value constructor**. For `VPLight` (`006BE990`) every
value it writes lands on an offset this document recovered from the registration side, and every
value is semantically right for the field named there: `m_outerConeAngle` = `0x3EC90FDB` = 0.3927
rad = **22.5°**, `m_intensity` = **1.0f**, `m_outerRange` = `0x7F7FFFFF` = **FLT_MAX**,
`m_localToWorldMatrix` and `m_shadowCaster` null. A wrong offset table would not produce sensible
defaults at every slot. Still static, so **BL-7 is untouched** — but it is a second derivation from
an unrelated function rather than another reading of the same one.

## CALL-CHAINS / ADDRESS-INDEX

```
~PClassDataMember 00633240
  -> if still linked: owner->vslot[+0x48] == 0062F080  (DetachMember, inverse of AttachMember)
  -> ListClear(record+0x38)  == 006B6700               (the owned second list)
  -> if attrs bit 0: aligned_free(record+0x20)         (the heap-copied name)
```

| Address | Name | Note |
|---|---|---|
| `0062F080` | `PClassDescriptor::DetachMember` | descriptor vslot `+0x48`; exact inverse of `AttachMember` |
| `006B6700` | `ListClear` | generic intrusive-list unlink loop; **not** a string destructor |
| `006BE990` | `VPLight` default-value constructor | descriptor vslot `+0x50`; independently confirms the `VPLight` offsets |
| `00633240` | `~PClassDataMember` | confirms owner `+0x18`, name `+0x20`, attrs bit 0, and the owned `+0x38` list |

`PClassDescriptor` corrected byte offsets: `+0x30` **type name (`char *`)** · `+0x38` storage
capacity · `+0x50`/`+0x60`/`+0x90`/`+0xA0`/`+0xB0` five unidentified lists · `+0x70` sub-object ·
`+0x78` base-class chain · `+0x80`/`+0x88` member list head/tail · `+0xE8` counter · `+0xF4` base
offset · `+0xF8` used bytes · `+0x100`/`+0x102` member counters.

## Still staged with you, untouched

The six `CompilerGeneratedEH.ExceptionFilter` pre-enrich rows (BK-7). No `Apply-*`, no `Pack-*`.
BK-3 (PostEffects paths) still open and unassigned.

---

# repos-94 — sixth block (BL-8: four of six lists identified)

Same program state: snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`.
No GFZ state written. No `_index/*.md` edited.

**Gates green:** `check_links.py` 177 files / 878 links. `verify_doc_addresses.py` on the schema
document: ok, 0 ghosts, 0 drift. `check_layout_units.py` clean, `--self-test` confirmed firing
first.

```
engine_explained   [#######.................................]  17.22%   5903 / 34270
ledger_resolved    [########################################]  99.54%   34112 / 34270
audit_coverage     [####################################....]  90.59%   77 / 85
questions_closed   [########................................]  20.00%   107 / 535
final_audits       [........................................]   0.00%   0 / 30
OVERALL            [##################......................]  43.97%
```

## OPEN-QUESTIONS

**BL-8 — four of the six lists identified**, up from one.

| head | holds | evidence |
|---|---|---|
| `+0x50` | **this descriptor's own node** in a global registry of class descriptors | `0063D640` unlinks `cls+0x50` and converts a node back to its descriptor by subtracting `0x50` |
| `+0x60` | **unidentified** | cleared at destruction by the generic list-unlink helper |
| `+0x80` | **fields** — the 682 registrations | `AttachMember` |
| `+0x90` | **methods** | 220 non-field `PClassDataMemberBase` constructions, 216 named; insert traced in `005AD8F0` |
| `+0xA0` | **the script bridge** | `005B2860` builds `"GetGlobalTime"` and links it at `+0xA0`; writer census is dominated by `Phyre.ScriptVM.ReflectionBridge` |
| `+0xB0` | **unidentified** | unlinked by the destructor's fourth walk, no nameable writer |

> **The engine reflects methods, not just fields.** 220 record constructions that are not field
> registrations, 216 with recovered names, and the names are unmistakable: `playOnce`,
> `playLooping`, `playOnceByName`, `stop`, `getAnimationTime`, `hasOneShotAnimationFinished`,
> `setSpeedForSlot`, `getTargetName`, `GetTime`, `GetGlobalTime`. 187 come from
> `Phyre.Reflection.GeneratedMetadataRoutine` and go to `+0x90`; 31 come from
> `Phyre.ScriptVM.ReflectionBridge` and go to `+0xA0`. **The engine keeps two callable lists: the
> reflected C++ methods, and the subset published to the script VM.**

Also recovered, and it supersedes guesswork on this structure: **the full descriptor layout from
its constructor `00632D80`**, which writes every field in one body — name `+0x30`, instance size
`+0x38`, alignment `+0x3C`, registry `+0x70`, base chain `+0x78`, and the six list heads.
`005A7ED0` calls it as `ctor(this, registry, "PAnimatableComponent", 0x108, 8, ...)`, so the name
and the instance size arrive as plain arguments.

**A byproduct worth keeping:** the destructor frees a node only when its **attribute bit 0** is
set — the same "name was heap-copied" bit as fields. The `+0x80` walk contains no free at all, so
**every one of the 682 field records is a static object**, while `+0x90`/`+0xA0` mix static and
heap records.

## AUDIT-LOG

### The instrument failed twice more, and both failures were caught by the shape of the answer

**First failure — the one carried over.** Last block's insert scan failed its own control.
Reading `AttachMember` byte by byte showed why: the tail is **never** touched as
`[base + HEAD+8]`. The head is materialised once, `lea rbx,[r14+0x80]`, and everything after goes
through `rbx` — `mov rax,[rbx+8]`, `mov [rbx+8],rcx`. My test had keyed on the base register,
which never appears again. Rebuilt around the real idiom, the control passes.

**Second failure — new, and subtler.** The rebuilt scan returned the *same ten*
`ThreadSafeStaticObjectInitializer` functions as writers of **every** head. That is not what a
list-specific writer set looks like, which is the only reason I looked. Cause: `mov [R+8], R` is
the empty-list **self-link** a constructor emits, and my test counted it as an insert. Excluding
stores whose value register is the head register drops those ten from every head and leaves
writer sets that differ per list — `0062EFD0` alone on `+0x80`, `GeneratedMetadataRoutine` on
`+0x90`, `ScriptVM.ReflectionBridge` on `+0xA0`.

**Neither failure produced an error.** Both produced a plausible number. The first was caught by a
control; the second only by noticing that the *distribution* was wrong — every head having the
same writers is a shape that cannot be true. Worth adding beside the control rule: **check that
the answer has the shape the question implies, not only that the tool ran.**

### I did not re-derive from my own corrected table

Having been wrong twice on this structure — first the unit, then the kind — I took the layout from
the constructor `00632D80` rather than from the table I had corrected. It writes every field in
one body. It independently reproduces the name at `+0x30`, which now has **three** derivations:
`006388C0` loading `[rcx+0x30]` as a string, the constructor storing the argument there, and
`005A7ED0` passing `"PAnimatableComponent"` as that argument.

### A note on the bash heredoc hazard, since it bit again

Two patch scripts written as bash heredocs silently mangled a line continuation, leaving a literal
`\\n` inside a Python source line. The first failed loudly; the second wrote a broken file that
still parsed. Patch scripts with escaped strings go through the file-edit tool, not a heredoc.

## CALL-CHAINS / ADDRESS-INDEX

```
PClassDescriptor ctor 00632D80(this, registry, name, instanceSize, align, baseChain)
  -> six self-linked lists at +0x50 +0x60 +0x80 +0x90 +0xA0 +0xB0
  -> registry at +0x70, base chain at +0x78, name at +0x30, instance size at +0x38

field   registration -> 00632960 -> AttachMember 0062EFD0 -> list +0x80
method  registration -> 00632FB0 -> inline insert          -> list +0x90   (187 records)
script  registration -> 00632FB0 -> inline insert          -> list +0xA0   ( 31 records)
descriptor lifetime  -> 0063D640 -> unlink cls+0x50 from the global registry
```

| Address | Name | Note |
|---|---|---|
| `00632D80` | `PClassDescriptor::PClassDescriptor` | the authoritative layout; all six lists, name, size, registry, base chain |
| `005A7ED0` | an abstract descriptor constructor | calls it with `"PAnimatableComponent", 0x108, 8` |
| `0063D640` | descriptor registry unlink | unlinks `cls+0x50`; node -> descriptor by `- 0x50` |
| `005AD8F0` | metadata routine for `PAnimatableComponent` | 24 method records; the traced `+0x90` insert |
| `005B2860` | script-bridge registration | builds `"GetGlobalTime"`, links it at `+0xA0` |

`PClassDescriptor` byte layout, from the constructor: `+0x08`/`+0x10`/`+0x18` three-pointer head ·
`+0x30` **name** · `+0x38` **instance size** · `+0x3C` alignment · `+0x50` registry node ·
`+0x60` list (unidentified) · `+0x70` registry · `+0x78` base chain · `+0x80` fields ·
`+0x90` methods · `+0xA0` script bridge · `+0xB0` list (unidentified) · `+0xE8` counter ·
`+0xF4` base offset · `+0xF8` used bytes · `+0x100`/`+0x102` member counters.

## Still staged with you, untouched

The six `CompilerGeneratedEH.ExceptionFilter` pre-enrich rows (BK-7). No `Apply-*`, no `Pack-*`.
BK-3 (PostEffects paths) still open and unassigned.

---

# repos-94 — seventh block (BL-8 remainder: a negative, and two rejected instruments)

Same program state: snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`.
No GFZ state written. No `_index/*.md` edited.

**Gates green:** `check_links.py` 177 files / 878 links. `verify_doc_addresses.py` on the schema
document: ok, 0 ghosts, 0 drift.

```
engine_explained   [#######.................................]  17.26%   5916 / 34270
ledger_resolved    [########################################]  99.54%   34112 / 34270
audit_coverage     [####################################....]  90.59%   77 / 85
questions_closed   [########................................]  20.00%   107 / 535
final_audits       [........................................]   0.00%   0 / 30
OVERALL            [##################......................]  43.99%
```

## OPEN-QUESTIONS

**BL-8 — `+0x60` and `+0xB0` NOT closed.** They stay open, and this block's result is a negative
plus a retraction rather than an identification.

**The negative, which has a passing control and does hold:** every function appearing in any slot
of a class-descriptor vtable was scanned for a reference to `[this+0x50]`, `[this+0x60]` or
`[this+0xB0]`. **None touches any of them.** The identical query for `[this+0x80]` returns slot 8
(`AttachMember`) plus two neighbours, so the instrument fires. **Whatever fills those two lists
does so through non-virtual code**, not through the descriptor's own interface — which is how the
field, method and script lists are all reached. That narrows the search for whoever takes it next.

## AUDIT-LOG

### A table I published last block was wrong, and I found it by opening the rows

Last block's inbox and document carried a per-head "writer census" including `+0x50` 7 writers,
`+0x60` 4 and `+0xB0` 2, presented as *"a second, mechanical derivation"*. **It is not.** The scan
matches any structure with a self-linked pair at that displacement and has **no descriptor
specificity at all**. All six candidates it offered for those three heads were opened this block
and **none is a class descriptor**:

| candidate | what it actually is |
|---|---|
| `001D9400` | an EASTL list container constructor (`"EASTL list"`) |
| `0020C730` | `CCallback<CSteamAchievements,…>` registration |
| `008653B0` | `CCallback<SteamCallbacksListener,…>` registration |
| `0078B9D0` | `PPFX::CTinyEffect` constructor |
| `007A3810` | `Phyre::VTS::ScreenState*` constructor |
| `0060CE50` | an unrelated parameter-block copy |

The `+0x90` and `+0xA0` rows survive **only** because their domain composition points at Phyre
reflection *and* each has an instruction-level trace behind it. Without the trace they would carry
no more weight than the six above. Corrected in the document with the retraction stated in place,
not silently.

**The lesson is the one from last block, one turn further on.** I wrote then that a control proves
the instrument fires but not that it measures the right thing, and that checking the *shape* of
the answer catches what a control cannot. The shape check passed here — writer sets did differ per
head — and the result was still wrong, because "different per head" is consistent with both a real
signal and per-head noise. **The check that actually worked was opening the rows.** For a small
candidate set that is cheap, and nothing substitutes for it.

### The replacement instrument was rejected too, before publishing

Anchoring on real descriptor *objects* — every rip-relative reference into the interior of a known
class-descriptor global at each list offset — is descriptor-specific by construction, and its
control passes (`+0x80` returns the reflection routines and `+0x90`/`+0xA0` the expected
registrars). Reading its `+0xB0` candidates found the failure mode anyway: `00630340` and
`00630490` are magic-static accessors for unrelated `PType` singletons that happen to sit at an
address equal to some descriptor's `D + offset`. **Descriptors are ~0x110 bytes packed in `.data`,
so an interior address can be another global's start**, and this scan cannot tell those apart.
Its `+0x60` and `+0xB0` rows are therefore not reported as an answer.

Two instruments built for one question, both rejected, one negative retained. That is the honest
yield of the block.

## CALL-CHAINS / ADDRESS-INDEX

Nothing new to add — no new address earned a claim this block. The corrections above apply to
entries already filed.

## Routing note acknowledged

`22-Middleware-PhyreEngine` reopening for the `GameApplication` / `Phyre::PFramework::PApplication`
boundary from `repos-46` is noted and **not absorbed this block** — it is a different question from
BL-8 and I did not want to fold a category-wide boundary revision into a block that was already
retracting one of its own tables. Available to take next.

## Still staged with you, untouched

The six `CompilerGeneratedEH.ExceptionFilter` pre-enrich rows (BK-7). No `Apply-*`, no `Pack-*`.
BK-3 (PostEffects paths) still open and unassigned.

---

# repos-94 — eighth block (the PhyreEngine boundary revision)

Same program state: snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`.
No GFZ state written. No `_index/*.md` edited.

**Gates green:** `check_links.py` 180 files / 903 links. `verify_doc_addresses.py` on the new
document: **ok**, 0 ghosts, 0 drift — 42 entry, 16 data.

```
engine_explained   [#######.................................]  17.44%   5978 / 34270
ledger_resolved    [########################################]  99.54%   34112 / 34270
audit_coverage     [####################################....]  89.66%   78 / 87
questions_closed   [########................................]  20.18%   111 / 550
final_audits       [........................................]   0.00%   0 / 30
OVERALL            [##################......................]  43.96%
```

## COVERAGE

`22-Middleware-PhyreEngine` gains **one** document: **6 total**. New:
`Application-Framework-Boundary/the-game-is-a-phyre-application.md` — DOCUMENTED, tier 1, one
falsification pass. `Subsystem-Map/phyre-subsystem-map.md` gains a framing note; category README
updated.

## OPEN-QUESTIONS

The framing correction, stated as the category now carries it:

> **FFXII does not *use* PhyreEngine. FFXII *is* a PhyreEngine application.** `GameApplication`
> (vtable `008C5760`, 31 slots) derives from `Phyre::PFramework::PApplication` (vtable `01CB2508`,
> 31 slots). **18 slots overridden, 13 inherited.** Equal slot counts mean the game adds **no new
> virtuals of its own** — it only fills in the framework's. The frame tick, the `FFXII_TZA.vbf`
> mount and the input pump are all game code in middleware slots.

**This explains the subsystem map's §11 finding** that no documented game subsystem calls Phyre.
That measurement is correct; the top-level control flow simply runs the other way. Looking for
game→Phyre calls at the top level finds nothing because the top level is **Phyre→game**. Not a
contradiction — the mechanism that document was missing. Noted in place there.

Five new questions, all mirrored in the document's §7: PROPOSED-repos94-19..23 (BM-1 the nine
unread input-tagged overrides · BM-2 the tick's return codes 0/1/9 · BM-3 what `this+0x113C` gates
· BM-4 whether `PApplication` itself derives from `PBase`/`PMemoryBase`, **asserted by repos-46 but
not verified here** · BM-5 what the 13 inherited slots do).

## AUDIT-LOG

### I re-derived the peer's result rather than absorbing it, and one number did not reproduce

`repos-46` established the inheritance from a destructor-chain argument and RTTI `mdisp = 0`.
**None of that is relied on in the document.** The vtable comparison was done from the recovered
table, and the strongest proof is a function body that needs no RTTI at all.

**The discrepancy:** repos-46 reported *"18 of 31 virtuals supplied, 10 inherited"*. I get **18
overridden and 13 inherited**, and 18 + 13 = 31 exactly, so 13 is the arithmetically complete
count. **It reconciles rather than contradicts:** three of the 13 inherited slots hold do-nothing
stubs — slots 11 and 27 target `005C5230` (constant return) and slot 26 targets `0016D6A0`, the
3-byte `ret` from my own funclet block. So "10 inherited *implementations*" and "13 inherited
*slots*" are both true of different things. I have recorded it that way in §8 rather than as a
correction, because a reader comparing the two documents would otherwise see a bare discrepancy
and have no way to resolve it. **Worth a look at whether repos-46's document states which it
means.**

### The proof I would keep if I could keep only one

Slot 6 of `PApplication` is `0079BF70`. Slot 6 of `GameApplication` is `0017CDC0`, whose entire
27-byte body is:

```c
FUN_0017d670();        // the game's own pre-step
FUN_0079BF70(this);    // <- PApplication's slot 6, by direct address
```

**An override calling the exact function in the base's matching slot.** That is
`Derived::F() { extra(); Base::F(); }` compiled, it needs no RTTI, no destructor chain and no
adjacency, and it also settles the *direction*: a base cannot call its derived class's override by
direct address. Four more overrides fall through to `005C5230`, the middleware's own stub, in the
same "do our part, then defer" shape.

### The three mechanism claims, verified from bodies rather than inherited

- **VBF mount** — `0017CEB0` (slot 2) sets the content root `"../../.."` and mounts
  `"../FFXII_TZA.vbf"`. Two authored strings; the framework asks and the game answers with its
  archive.
- **Frame tick** — `0017CCD0` (slot 4), the largest override at 237 B, reads frame time at
  `this+0x48` and returns 0/1/9.
- **Startup latch** — it is **not a separate mechanism**: it is a byte at `this+0x113D`, tested
  every frame *inside* the tick and set on the first one, never cleared. That is sharper than
  "a startup latch exists" and it is directly useful — a mod wanting "the game has really started"
  can poll one byte.

Also: **11 of the 18 overrides are input-tagged**, which is what `PApplication` is for — it owns
the window, device enumeration and the per-frame pump. And slot 0, the deleting destructor
`0017CC70`, is the declared parent of the `__std_terminate` funclet `00861EAE` from my first
block, so **`~GameApplication` is a `noexcept` boundary**: a throwing destructor hook terminates
the process rather than unwinding.

### Cluster verified, count matches

Twelve vtables in `01CB2400`–`01CB2800`, all `Phyre::PFramework` — independently reproduced,
including the three pad drivers behind one 7-slot interface (`PInputDevicePadDirectInput`,
`PInputDevicePadXInput`, `PInputDevicePadSteamController`).

### Not mine, flagged not touched

`check_layout_units.py` now reports **1 suspect stride**, in
`18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`:

```
+0x14  u64 = 0xFFFFFFFFFFFFFFFF on reset (covers +0x14 and +0x18)
declared u64 (8 bytes) but next field starts 4 byte(s) later
```

The row's own text says it covers two fields, so this looks like the legitimate
overlapping-view case the checker warns about rather than an index/offset error. **It is another
session's document and I did not touch it** — routing to whoever owns 18-Audio.

## CALL-CHAINS / ADDRESS-INDEX

```
Phyre::PFramework::PApplication  (the framework owns the loop)
  -> slot 2  0017CEB0  content root + mount ../FFXII_TZA.vbf
  -> slot 3  0017CF30  device/viewport setup
  -> per frame:
       slot 4  0017CCD0  FRAME TICK -> first-frame latch this+0x113D -> 0017D650
       slot 7  0017CE50  input pump -> InputManager_GetSingleton()
       slot 6  0017CDC0  pre-step -> PApplication::slot6 0079BF70
  -> slot 0  0017CC70  ~GameApplication  (noexcept)
```

**A cross-category edge worth registering:** `22-Middleware-PhyreEngine` → `15-Input`, eleven
overridden slots, and → `02-Resource-And-Asset-Pipeline` through the archive mount. The input
document may want the reciprocal link.

| Address | Name | Note |
|---|---|---|
| `008C5760` | `GameApplication` vtable | 31 slots, `.rdata` |
| `01CB2508` | `Phyre::PFramework::PApplication` vtable | 31 slots |
| `0017CEB0` | slot 2 — VBF mount | `"../../..'`, `"../FFXII_TZA.vbf"` |
| `0017CCD0` | slot 4 — frame tick | frame time `this+0x48`, latch `this+0x113D` |
| `0017CDC0` | slot 6 — calls its base | the inheritance proof |
| `0017CE50` | slot 7 — input pump | `InputManager_GetSingleton()` |
| `0079BF70` | `PApplication` slot 6 | the base implementation |
| `005C5230` | `PApplication` shared stub | constant return |

## Still staged with you, untouched

The six `CompilerGeneratedEH.ExceptionFilter` pre-enrich rows (BK-7). No `Apply-*`, no `Pack-*`.
BK-3 (PostEffects paths) still open and unassigned. BL-8's `+0x60`/`+0xB0` still open with the
non-virtual-writers narrowing.
