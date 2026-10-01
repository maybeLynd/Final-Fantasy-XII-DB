---
system: Exception funclets and lazy-static guards
category: 24-Compiler-And-CRT-Runtime
status: AUDITED
owner_layer: CodeDomain:CompilerGeneratedEH
evidence_tier: 1 (one group of 128 relies on tier 8 for its *identity*, see §8)
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites `005DD890`; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 0
function_families:
  - "stream sentry destructor clones (BK-6) | C | members/bk6-sentry-base-destructor-clones.tsv | 4 | MSVC STL, not FFXII code: std::basic_istream<char> / basic_ostream<char> _Sentry_base::~_Sentry_base (vbtable to basic_ios, _Mystrbuf at +0x48, streambuf _Unlock). Members = every census function whose body is byte-identical to 001952E0 (../Generated-Adapters/members/select_generated_adapters.py, exact 45-byte comparison) - 4; the unwind maps register the adjusted-object stubs 008982F0 / 008982FC and their siblings for the stream extractor 001DDC40 and inserters 00194B00 / 001DDE10 / 00194CD0 (BK-6, sec.8). Boundary: the four bodies; the 12-byte stubs, the inserters and extractor are NOT covered"
---

# Exception funclets and lazy-static guards

> The invisible clean-up crew: 3,899 tiny compiler-written routines that run only when
> something has already gone wrong, plus the one-time-initialisation locks that guard
> FFXII's 1,681 lazily-created singletons.

This document exists to answer open question **B-2** — *"~3,895 functions are classified
`CompilerGeneratedEH`. Confirm each is genuinely compiler-generated and none is a real
mechanism hiding behind the classification."* The answer is in §8. It is not a clean yes.

---

## 1. What the player sees

Almost nothing. That is the point.

*Final Fantasy XII: The Zodiac Age* is a game that essentially never shows you an error. A
texture that fails to load, an audio bank that will not open, a controller-config file the
game cannot write — none of these puts a message box on screen. The game notices, tidies up
whatever it had half-built, and carries on. The Battle Menu still opens, the Gambits still
fire, and you never learn that anything happened.

That tidying-up is real code, and there is a lot of it: **3,899 separate little routines that
exist only to be run when something has already failed.** They are not part of any game
system. They are the compiler's own answer to a question the programmer asked once — "if this
throws, what has to be put back?" — repeated a few thousand times.

The one place you can *see* one of them do its job is the key-mapping file. If you rebind your
controls and the game cannot write `keymap.ini` back to disk — read-only folder, full drive,
a mod tool holding the file open — one of these routines catches the failure, writes
`Catch exception when writing keymap.ini` to the process's standard output, and lets the game
continue with your bindings live in memory but unsaved. No dialog, no crash, and your remapped
controls quietly do not survive a restart.

The second thing in this document is more likely to matter to you. FFXII builds **1,681 of its
internal singletons lazily** — they do not exist when the game starts, and are created the
first time anything asks for them. Each one is protected by a small lock so that two threads
asking at the same moment cannot both build it. If a mod interrupts one of those first-time
constructions and never lets it finish, **every other thread that later asks for the same
object waits for it forever, checking back ten times a second.** The game does not crash. It
simply stops — usually on a loading screen, because that is where most of these objects are
first touched. That specific hang is the single most useful thing in this document for anyone
injecting code into FFXII, and §6 says how to avoid it.

No addresses in this section. Everything below has them.

---

## 2. Native mechanism

### What a funclet is, in this binary

When a C++ function has objects on its stack and an exception passes through it, something has
to destroy those objects on the way out. MSVC does not put that code inside the function. It
compiles each cleanup into a **separate, tiny function** — a *funclet* — and records its
address in the exception tables. The unwinder calls the funclet with the failing function's
stack frame as an argument. The funclet reaches into that frame, destroys what it must, and
returns.

That gives funclets a calling convention nothing else in the binary uses:

```
funclet(RCX = ignored, RDX = the parent function's frame pointer)
```

**RDX is the tell.** A funclet gets the *other* function's frame in its second argument and
indexes locals off it. It is visible in the bytes without reading a single exception table, and
2,133 of the 3,895 tagged functions show it outright — either as `mov rbp, rdx` before touching
anything, or by forming a pointer straight out of `[rdx+disp]`.

Be careful with the loose form of that statement, because it is not true. "A frame register is
loaded from RDX" on its own matches **3,552 functions across the whole binary**, most of them
ordinary code doing `mov rbx, rdx` to keep argument 2 alive across a call. What discriminates is
the *complete* prologue — `push rbp ; sub rsp,N ; mov rbp,rdx` with no other work in between, or
the two-instruction `(lea|mov) rcx,[rdx+disp] ; jmp` form — and that measurement is in §8.

Cleanup funclets do not return normally; they **tail-jump** into the destructor. Catch funclets
do return, and what they return is an **address inside the parent function** — the instruction
the unwinder should resume at. `Catch_All@008a5c4b` is three instructions long and its entire
body is `return 0x008098E9`, an address 0x15 bytes into its own parent `008098D4`. That is the
catch-funclet ABI, proved from the body with no table involved.

### The whole population, by what the body does

All 3,895 tagged bodies were disassembled and reduced to an operand-normalised skeleton. They
collapse into **46 distinct shapes**, and the top four cover 84 % of them:

| n | shape | what it is |
|---:|---|---|
| 1,620 | `lea rcx,[rip+k] ; jmp X` | destroy a *named global* object |
| 899 | `lea rcx,[rdx+d] ; jmp X` | destroy a local held **by value** in the parent frame |
| 487 | `mov rcx,[rdx+d] ; jmp X` | destroy a local held **by pointer** in the parent frame |
| 288 | `mov rcx,[rdx+d] ; add rcx,imm ; jmp X` | destroy a sub-object at a fixed offset inside one |

The rest are the same idea with a frame register established first (`push rbp; sub rsp,N;
mov rbp,rdx; …; ret`), or with a conditional gate, or a loop. Nothing in the 46 is a
general-purpose routine. The largest body in the entire set is **158 bytes**; the median is
**12**; the whole 3,895 occupies **59,914 bytes — 0.75 % of `.text`.**

### The biggest single family is not a destructor at all

**1,545 of the 1,620 "destroy a global" funclets tail-jump to one address, `0080926C`**, and
that address is `_Init_thread_abort` — a Ghidra FunctionID single match against the Visual
Studio 2015 CRT, whose body is four lines long:

```c
void _Init_thread_abort(int *guard) {
    EnterCriticalSection(&_Init_thread_lock);   // 02EAED40
    *guard = 0;
    LeaveCriticalSection(&_Init_thread_lock);
    _Init_thread_notify();
}
```

`_Init_thread_abort` has exactly one purpose in the MSVC runtime: a **thread-safe function-local
static** — C++11's "magic static" — was being constructed, the constructor threw, and the
one-time-initialisation lock has to be released so the next thread to ask does not wait
forever. It is only ever reachable on an unwind path. So these 1,545 are provably unwind
funclets *from their own bodies*, without touching an exception table.

They are also a **census**. Each one passes a different guard variable, and all 1,545 guard
addresses are distinct — no repeats. So this binary holds at least 1,545 lazily-initialised
function-local statics with a constructor that can throw.

Counting the construction side directly gives the full number:

| measurement | value |
|---|---:|
| `call _Init_thread_header` sites | **1,732** |
| `call _Init_thread_footer` sites | **1,732** |
| distinct guard variables behind those sites | **1,681** |
| distinct functions containing them | **707** |
| guards with an `_Init_thread_abort` funclet | **1,545** |
| guards without one | **136** |

**FFXII TZA has 1,681 lazily-created function-local statics, reached from 1,732 guarded
construction sites spread over 707 functions.** Sites exceed objects because 19 guards appear at
more than one site — always in *different* functions, the compiler having inlined one accessor
into several callers, which accounts for the difference exactly (1,732 - 1,681 = 51). The 136
without a funclet are the ones whose construction cannot throw. Every one of the 1,545 funclet
guards is also a header-site guard, with none left over in either direction. §4 gives the exact
gate.

### Where the exception machinery actually lives in the game

Every funclet belongs to a parent function, and the parents are not spread evenly. Of the
**1,609 distinct parent functions**:

| parent's subsystem (V120 PrimaryOwner) | parents |
|---|---:|
| Resource | 182 |
| Audio | 41 |
| Input | 11 |
| Save / Load / Settings | 5 |
| Platform / Online / Achievements | 4 |
| Presentation | 2 |
| Core runtime scheduling | 1 |
| **owned parents, total** | **246** |

and by mechanism class, 613 parents are PhyreEngine, 386 are unclassified native routines, 81
are third-party libraries, 40 are the C++ standard library.

> **Bounded 2026-09-14 (aggregate-claims sweep, GN161).** The 3,895-funclet set and the 1,609
> parent population are `.pdata`-structural counts — the GN158→GN161 advance changed only
> `CodeDomain` tags and comments, so neither structural figure can move. The mechanism-class
> split *is* annotation-derived: at most **4** of the 1,609 parents acquired a `CodeDomain` tag
> in R109 (the upper bound across all broad FuncInfo re-parses; the only measured EH-adjacent
> newly-tagged edge is `0089FC9B`→`005DD890`), so "386 unclassified native routines" may now
> overstate by ≤4. The original parent list is not preserved under `Tools/work/`, so an exact
> per-class recount awaits method recovery; the totals stand.

**There is not one Combat, Movement, Party, Actor, Spawn, Gambit or Script parent in the set.**
FFXII throws exceptions where it touches the outside world — files, audio devices, the input
configuration, the middleware's resource loader — and nowhere else. Battle and field logic is
exception-free code. That is why no gameplay mechanism can be hiding in this population: the
population does not reach into gameplay in the first place.

The funclets do call *outward* into 827 distinct non-EH functions, and 98 of those transitions
land on a function with a game-subsystem owner (Resource 58, Audio 35, Platform 3, Input 2).
Those are cleanup calls — freeing a texture handle, releasing a sound buffer — not ownership.
They are registered in §5 because no other document mentions them.

### Two ways the compiler leaves work that does nothing

**172 funclets tail-jump to `0016D6A0`, whose entire body is `C2 00 00` — `ret`.** That address
is also what the PE load configuration names as the Control Flow Guard check function (the
`GuardCFCheckFunctionPointer` slot at `008C31C0` holds `0016D6A0`), which is why Ghidra labels
it `_guard_check_icall` and why the decompiler prints these funclets as "call the CFG check".
They do not. `Unwind@0089dd0e` settles it by passing that same address as the *element
destructor* argument of `_eh_vector_destructor_iterator`:

```c
_eh_vector_destructor_iterator_(frame[0x68], 0x18, 8, _guard_check_icall);
```

A CFG check cannot be an array-element destructor. What happened is that the linker's
identical-COMDAT folding merged one or more **empty destructors** onto the same address as the
`ret`-only CFG check, because the bodies are byte-identical. The source said `~T()`; the
binary says `ret`. Either way, at run time these 172 funclets destroy nothing.

**99 more funclets call `006DA980`, also `C2 00 00` — also `ret`** — but they call it with five
arguments, and two of them are authored strings:

```c
FUN_006da980(frame[0x50], PTR_PTR_01f3ba68, "..\\src\\GPU\\GPUPostEffect.cpp", 0x71ee, frame[0x88]);
FUN_006da980(frame[0x50], PTR_PTR_01f3ba68, "..\\src\\ppfx.cpp",             0x2be, "IPfxContext::Instantiate()");
```

This was a diagnostic in the middleware's debug build — a "released a resource during unwind at
file X line N" report. The release build reduced the reporting function to `ret` but could not
delete the arguments, so **the original source file names and line numbers are still in the
binary**, sitting inside exception funclets. 100 funclet bodies carry a string; 18 distinct
source paths are recoverable this way, including the build-machine path
`d:\bamboo\build\yeblic-ppfxlic-bl2015\src\gpu\GPUClassUtil.h`. See §8 for how this relates to
the PostEffects document, which found the same strings from the other direction.

### The terminate boundary

**86 funclets are five bytes: `jmp 00861EAE`**, and `00861EAE` is itself six bytes,
`jmp qword [008C2A78]`, an import jump to `VCRUNTIME140.dll!__std_terminate`. This is what
`noexcept` compiles to on the failure path: if an exception tries to leave a function that
promised not to throw, unwinding runs this funclet and the process ends. The classification
tags `00861EAE` as a funclet, and the compiler's own tables agree — it is the declared unwind
action of parent `0017CC70` — but its *body* is an ordinary import thunk, byte-identical to 118
others in the binary tagged `Thunk.ExternalImport`. It is both things at once. §8 records that
as a shape collision rather than an error.

### The exception configuration of the whole executable

Parsing every `.pdata` record's handler pointer — a structural parse used here only to say
*which* handler each function registered, never to say what any function does — gives the
binary's complete EH configuration:

| handler | functions | meaning |
|---|---:|---|
| `__GSHandlerCheck` (`00808BA8`) | 5,372 | `/GS` stack cookie only, no C++ EH |
| `__CxxFrameHandler3` (`00861EB4` → VCRUNTIME140) | 4,377 | C++ exception handling |
| `__GSHandlerCheck_EH` (`00808F64`) | 141 | both |
| `__C_specific_handler` (`00861ED8` → VCRUNTIME140) | 9 | structured (`__try`/`__except`) |

`__CxxFrameHandler3`, not `4`, so the classic uncompressed `FuncInfo` layout is in use and the
tables are directly readable. 4,377 + 141 = **4,518 `FuncInfo` records**, every one with a valid
`0x19930520`-family magic — the parse's own built-in validity check, and it never failed.

Only **nine functions in the whole game** use SEH `__try`/`__except`, and their seven filters
are the small group in §3 that the classification currently misses.

---

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0080926C` | `_Init_thread_abort` | 48 B | releases a magic-static guard when the constructor threw; tail target of **1,545** funclets |
| `008092FC` | `_Init_thread_header` | 103 B | claims a magic-static guard; **1,732** call sites |
| `0080929C` | `_Init_thread_footer` | 96 B | publishes a completed magic static; **1,732** call sites |
| `00809364` | `_Init_thread_notify` | 91 B | wakes threads waiting on a guard |
| `008093C0` | `_Init_thread_wait` | 151 B | the 100 ms wait a blocked thread performs |
| `0016D6A0` | `_guard_check_icall` — **and** at least one folded empty destructor | 3 B (`ret 0`) | CFG check per the load config; tail target of **172** funclets — **and 2,422 ordinary call sites in 2,308 functions**, which the funclet figure alone does not suggest. Named `_guard_check_icall` across the database because the load config is the only source that gives these three bytes an identity; the folding is real but nameless. |
| `00896270` | `_guard_dispatch_icall` | 2 B | CFG dispatch, per the load-config slot; sits immediately below the funclet block |
| `006DA980` | stripped ppfx diagnostic reporter | 3 B (`ret`) | called by **99** funclets, still passed `__FILE__`/`__LINE__` |
| `00861EAE` | `__std_terminate` thunk | 6 B | `noexcept` boundary; tail target of **86** funclets |
| `00861ECC` | `_CxxThrowException` thunk | 6 B | rethrow, reached from **64** catch funclets — 64 sites in 64 distinct `Catch_All@` bodies, one site each — plus **5** ordinary call sites in 5 functions. *(Was written as "8 catch funclets"; re-derived from the PE 2026-09-08, and 8 is not the count under either unit.)* |
| `00861EB4` | `__CxxFrameHandler3` thunk | 6 B | the C++ EH personality routine, 4,377 functions |
| `00861ED8` | `__C_specific_handler` thunk | 6 B | the SEH personality routine, 9 functions |
| `00808BA8` | `__GSHandlerCheck` | 29 B | stack-cookie personality, 5,372 functions |
| `00808F64` | `__GSHandlerCheck_EH` | 127 B | cookie + C++ EH, 141 functions |
| `00896280` | first funclet in the block | 12 B | `lea rcx,[rip+0x16E80C9]` -> `01F7E350` ; `jmp 00793250`. **Not** an `_Init_thread_abort` funclet — it has the guard-family *shape* but tail-jumps to `FUN_00793250` (353 B, Phyre framework). |
| `008A6960` | last funclet in the block | 12 B | `mov rcx,[rdx+0x58] ; jmp 00199D30` — a different family: it loads an object field, not a static guard. |
| `008964A0` | **first** `_Init_thread_abort` funclet | 12 B | `lea rcx,[rip+0x16E9121]` -> `01F7F5C8` ; `jmp 0080926C`. The lowest of the **1,545**, and the worked example in §4. |
| `008A6950` | **last** `_Init_thread_abort` funclet | 12 B | the highest of the 1,545. All 1,545 lie inside the block range below. |

> **Correction, 2026-09-08.** The first two rows above previously read *"`lea rcx,[rip+guard] ;
> jmp _Init_thread_abort`"* and *"same family"*. **Both were wrong**, and disassembly says so:
> `00896280` jumps to `FUN_00793250`, and `008A6960` is `mov rcx,[rdx+0x58] ; jmp 00199D30`.
> The *block boundary* is right — all 1,545 guard funclets lie inside it — but the guard body was
> attributed to the block's endpoints, which do not have it. The true endpoints of that family are
> `008964A0` and `008A6950`, now listed above. Found by the `EC-1` re-sweep.

**The funclet block is the address range `00896280`–`008A6960`.** It holds 3,898 functions, of
which 3,892 are tagged `CompilerGeneratedEH`, and **59,914 bytes of funclet code in total** — that
figure is the sum of 3,895 individual body extents across the whole tagged set, not the extent of
any one function. Median body 12 B, maximum 158 B.

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02EAED40` | `_Init_thread_lock` | `CRITICAL_SECTION` | the single lock shared by every lazy static |
| `01F44850` | `_Init_global_epoch` | `int` global | the counter stamped into a completed guard |
| `01F7F5C8`–`02EBA258` | magic-static guards | `int` array region in `.data` | the 1,545 guards that carry an unwind funclet |
| `008C2A78` | `__imp___std_terminate` | IAT slot | resolved through `VCRUNTIME140.dll` |
| `008C31C0` | `GuardCFCheckFunctionPointer` slot | load-config pointer | holds `0016D6A0` |
| `008C31C8` | `GuardCFDispatchFunctionPointer` slot | load-config pointer | holds `00896270` |

**The two functions that are not funclets** (§8, finding 1):

| Address | Body | Tagged | Actually |
|---|---:|---|---|
| `001AAF20` | 45 B | `CompilerGeneratedEH.AdjustedObjectCleanup` | ordinary `__fastcall(this)` virtual-base dispatch helper |
| `001AAF50` | 45 B | `CompilerGeneratedEH.AdjustedObjectCleanup` | byte-identical to `001AAF20` |
| `001952E0` | 45 B | `Microsoft.MSVCCRT_STL_Runtime.Support` | byte-identical to both |
| `00195310` | 45 B | `Microsoft.MSVCCRT_STL_Runtime.Support` | byte-identical to both |

**The seven SEH filters** (six of which carry no `CompilerGeneratedEH` tag):

| Address | Parent | Tagged? | Body |
|---|---|---|---|
| `0089BEF0` | `005CD1E0` | no | `return 0xFFFFFFFF` |
| `008A5AD0` | `005CCBA0` | no | `FUN_005ccbf0()` |
| `008A5B7C` | `00808A54` | no | `return *(int*)*p == 0xC0000005` |
| `008A5B94` | `00808D78` | no | `_seh_filter_exe(code, p)` |
| `008A5BB2` | `00808FE4` | no | guarded `__ArrayUnwind` |
| `008A5BDE` | `00809054` | no | guarded `__ArrayUnwind` |
| `008A5C0A` | `008090C0` | **yes** (`ExceptionFilter`) | `__ArrayUnwind`'s own filter |

---

## 4. Data structures and formulas

### The funclet ABI

```c
// cleanup / unwind funclet
void  __fastcall Unwind_XXXXXXXX(void *ignored_rcx, char *establisher_frame_rdx);

// catch funclet — the return value is where the parent resumes
void *__fastcall Catch_All_XXXXXXXX(void *ignored_rcx, char *establisher_frame_rdx);

// SEH filter — return value is an EXCEPTION_* disposition
LONG  __fastcall filt_N(void *exception_pointers_rcx, char *establisher_frame_rdx);
```

Every local the funclet touches is `establisher_frame_rdx + fixed_offset`, with the offset
baked in at compile time. The frame offsets seen in this binary run from `+0x20` to `+0xF0`.

### The magic-static gate — the exact expression

This is what the compiler emits at every one of the 1,732 guarded construction sites. Taken
verbatim from `FUN_00189CE0`, whose guard is `01F7F5C8` and whose unwind funclet is
`Unwind@008964A0`:

```c
// thread_epoch lives in this module's TLS block at offset +4
#define thread_epoch  (*(int *)(*(char **)((char *)ThreadLocalStoragePointer \
                                           + (unsigned long long)_tls_index * 8) + 4))

if (thread_epoch < guard) {                 // guard = DAT_01f7f5c8, an int in .data
    _Init_thread_header(&guard);
    if (guard == -1) {                      // -1 means "this thread claimed it"
        /* ...construct the object... */    //  <- if this throws, Unwind@008964a0 runs
        _Init_thread_footer(&guard);
    }
}
/* ...use the object... */
```

with the three CRT helpers, exact:

```c
void _Init_thread_header(int *g) {
    EnterCriticalSection(&_Init_thread_lock);          // 02EAED40
    for (;;) {
        if (*g == 0)  { *g = -1; break; }              // unclaimed -> claim it
        if (*g != -1) { thread_epoch = _Init_global_epoch; break; }   // already built
        _Init_thread_wait(100);                        // someone else is building it
    }
    LeaveCriticalSection(&_Init_thread_lock);
}

void _Init_thread_footer(int *g) {
    EnterCriticalSection(&_Init_thread_lock);
    _Init_global_epoch = _Init_global_epoch + 1;       // 01F44850
    *g           = _Init_global_epoch;
    thread_epoch = _Init_global_epoch;
    LeaveCriticalSection(&_Init_thread_lock);
    _Init_thread_notify();
}

void _Init_thread_abort(int *g) {                      // the funclet's tail target
    EnterCriticalSection(&_Init_thread_lock);
    *g = 0;                                            // back to unclaimed
    LeaveCriticalSection(&_Init_thread_lock);
    _Init_thread_notify();
}
```

**The guard's three states are the whole protocol:**

```
*guard ==  0   never initialised
*guard == -1   a thread is constructing it right now; everyone else waits 100 ms and retries
*guard  >  0   built; its value is the epoch at which it completed
```

and the fast path is one TLS read and one compare:

```
thread_epoch >= *guard   ->  skip the whole block, the object is ready
```

`_Init_thread_abort` is the *only* thing that puts a `-1` guard back to `0`. If control leaves
a constructing thread without running either the footer or the abort funclet, that guard stays
`-1` permanently and every later caller loops on `_Init_thread_wait(100)` forever. See §6.

The 1,681 guard variables all live in `.data`; the 1,545 that carry a funclet occupy the range
`01F7F5C8`–`02EBA258`.

### The conditional-destructor gate

Objects that are only *sometimes* constructed get a bitmask in the parent's frame, and the
funclet tests it before destroying:

```c
// Unwind@008971c0, Unwind@008997e6, Unwind@00896ad0 and 42 others
if ((frame[0x20] & MASK) != 0) {          // MASK is 1, 2, 4, ... one bit per object
    frame[0x20] &= ~MASK;                 // clear it first, so a nested throw cannot repeat
    Destructor(frame[OFFSET]);
}
```

### The array-destruction helpers

```c
// Unwind@00896320 — destroy an array in place, backwards
_eh_vector_destructor_iterator(frame[0x50] + 0x20,  /* first element   */
                               0x338,               /* element size    */
                               2,                   /* element count   */
                               FUN_001850b0);       /* element dtor    */

// FUN_008a5bb2 / FUN_008a5bde — the CRT's own guard around __ArrayUnwind
if (frame[0x20] == 0)
    __ArrayUnwind(frame[0x50], frame[0x58], frame[0x28], frame[0x70]);
```

### The filter constants

```c
// 008A5C0A — filt$0 inside __ArrayUnwind: a throw during array unwinding is fatal
if (*(int *)exception_record == 0xE06D7363)   /* 'msc' — the MSVC C++ exception code */
        return terminate();
else    return 0;                             /* EXCEPTION_CONTINUE_SEARCH */

// 008A5B7C
return *(int *)exception_record == 0xC0000005; /* STATUS_ACCESS_VIOLATION */
```

### The `.pdata` / `FuncInfo` record layout (cross-check instrument only)

Used in §8 solely to enumerate which addresses the compiler *declared* as funclets. Never used
here to attribute behaviour to any function.

```
RUNTIME_FUNCTION            12 B   { u32 BeginRVA; u32 EndRVA; u32 UnwindInfoRVA; }
UNWIND_INFO                        byte0 = Version:3 | Flags:5      (EHANDLER 1, UHANDLER 2, CHAININFO 4)
                                   byte2 = CountOfCodes, slots padded to an even count
                                   then u32 ExceptionHandlerRVA, then language-specific data
FuncInfo (x64)              40 B   { u32 magic; i32 maxState; u32 pUnwindMap; u32 nTryBlocks;
                                     u32 pTryBlockMap; u32 nIPMap; u32 pIPToStateMap;
                                     u32 dispUnwindHelp; u32 pESTypeList; u32 EHFlags; }
                                   magic must be 0x19930520 / 21 / 22   <- the validity check
UnwindMapEntry               8 B   { i32 toState; u32 action; }        action = cleanup funclet RVA
TryBlockMapEntry            20 B   { i32 tryLow, tryHigh, catchHigh; i32 nCatches; u32 pHandlerArray; }
HandlerType                 20 B   { u32 adjectives; u32 pType; i32 dispCatchObj;
                                     u32 addressOfHandler; u32 dispFrame; }  addressOfHandler = catch funclet RVA
__C_specific_handler scope         { u32 count; count x { u32 Begin, End, Handler, JumpTarget } }
                                   Handler = filter funclet RVA;  JumpTarget = an address *inside the parent*
```

---

## 5. Call chain

```
some engine operation that can fail
   (file open, texture upload, sound-bank read, keymap write, first use of a lazy singleton)
  -> a C++ `throw` inside it
     -> VCRUNTIME140!_CxxThrowException            (thunk 00861ECC)
        -> RtlUnwindEx walks .pdata to the parent frame
           -> VCRUNTIME140!__CxxFrameHandler3      (thunk 00861EB4, personality of 4,377 functions)
              -> THIS SYSTEM: the parent's cleanup funclets, innermost state first
                 -> a destructor / free / _Init_thread_abort / __std_terminate / nothing at all
              -> a catch funclet, which returns a resume address inside the parent
        -> execution continues at that address; the player sees nothing
```

**Upstream (who causes this).** Never a caller in the ordinary sense — a funclet has no callers
at all. The unwinder reaches it from the exception tables. The *parents* are 1,609 functions:
613 PhyreEngine, 386 unclassified native routines, 246 with a game-subsystem owner (Resource
182, Audio 41, Input 11, Save/Load/Settings 5, Platform 4, Presentation 2, scheduling 1), 81
third-party, 40 C++ standard library, the rest runtime and container code.

**Downstream (what this causes).** 827 distinct non-EH functions are entered from a funclet.
By mechanism class: 1,631 transitions into Microsoft CRT/STL code, 588 into unclassified native
adapters, 482 into PhyreEngine, 214 into thunks, 198 into runtime containers, 172 into the
folded `ret` at `0016D6A0`, 101 native routines, 100 leaf stubs, 48 C++ object lifecycle, 42
dispatchers, 26 standard library, 26 subsystem boundaries, 2 Presentation, 1 Media.

**Owner-crossing edges this system introduces — registered here because no other document
mentions them.** 98 funclet transitions land on a function that carries a V120 `PrimaryOwner`:

| destination owner | transitions |
|---|---:|
| Resource | 58 |
| Audio | 35 |
| Platform / Online / Achievements | 3 |
| Input | 2 |

These are **cleanup calls on a failure path**, not ownership and not gameplay control flow. A
Resource or Audio document that enumerates its callers will see these edges and should
disposition them by reference to this document rather than absorb them.

**Do not confuse with:**

- **Static-destructor `atexit` thunks.** 2,579 functions above `008A6960` — tagged
  `Phyre.Reflection.DataMemberMetadataStaticTeardown` (853),
  `Phyre.Reflection.ClassDescriptorStaticTeardown` (404),
  `Runtime.StaticIntrusiveListTeardown` (224) and friends — have the *identical* two-instruction
  shape `lea rcx,[rip+global]; jmp ~T()`. They run at normal shutdown, not on an exception.
  1,328 of them match an EH skeleton byte for byte. The distinction is settled in §8 by the fact
  that every one of them has its address taken by an `atexit` call and **not one of the 3,895
  funclets does**. See [`../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md).
- **Ordinary `Thunk.InternalForwarder` / `Thunk.ExternalImport` stubs.** 749 non-EH functions are
  a bare `jmp imm` and 118 are a bare `jmp [rip+k]`, exactly like the 86-plus-1 terminate
  funclets. Shape alone cannot separate them.
- **The Control Flow Guard adapters.** `0016D6A0` appears in this document only because empty
  destructors were folded onto its address. The CFG mechanism itself is documented in
  [`../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md).
- **`__except` bodies.** The seven addresses `005CCBCE`, `005CD2E0`, `007A3798`, `00808AE6`,
  `00808EB8`, `0080910C`, `008634E4` are declared in scope tables but are *not* funclets — they
  are jump targets inside their parent functions, which is how `__C_specific_handler` works.

---

## 6. Modding notes

- **Best intervention point.** There is none inside this system, and that is the finding. A
  funclet has no callers, runs only during unwinding, and does nothing a mod would want to
  change. If you want to influence what happens when a resource load fails, hook the parent —
  one of the 1,609 in §5 — not its cleanup.

- **The one real hazard: never leave a magic-static constructor without finishing it.** If your
  detour sits inside one of the 707 functions that contain a lazy static, and it returns early,
  longjmps, or throws through a frame that has claimed a guard, then `_Init_thread_footer` and
  `_Init_thread_abort` both fail to run, the guard stays at `-1`, and every other thread that
  later reaches the same static spins in `_Init_thread_wait(100)` forever. **The symptom is a
  silent hang with no crash, usually on a loading screen, with normal CPU usage.** All 1,681
  statics share the single critical section at `02EAED40`, so one stuck guard can also serialise
  unrelated first-time initialisations behind it. If a detour must bail out, bail out *before*
  the `_Init_thread_header` call site, not after.

- **Reading the guards is safe and useful.** A guard int in `.data` between `01F7F5C8` and
  `02EBA258` reading `> 0` means that singleton exists; `0` means it has never been touched;
  `-1` means a construction is in flight *right now* (or is stuck). Watching one is a clean way
  to learn when a subsystem first comes alive, with no code patching at all.

- **Regenerates itself — do not write these.** Guard values are produced by the CRT and ordered
  by `_Init_global_epoch` at `01F44850`. Writing a guard to a positive value to "skip"
  initialisation makes the accessor return an object that was never constructed.

- **Breaks if:** you relocate or pad `.text`. Funclet entry points are recorded as RVAs in the
  exception tables; a funclet that moves without its table entry moving is unreachable, and the
  unwinder will fail *only* on the error path — which means it will pass every test you run and
  fail the first time something actually goes wrong.

- **Recovering source structure.** The 100 funclets carrying strings map regions of the binary
  to real SQEX/middleware source files — `..\src\GPU\GPUPostEffect.cpp`, `..\src\ppfx.cpp`,
  `..\src\GPU\TinyEffect\TinyEffect.cpp` and 15 more. When you need to know which translation
  unit a stretch of PostEffects code came from, its funclets will often tell you and its own
  body will not.

- **Multiplayer / XIIOnline.** Nothing here is world state and nothing here is authoritative.
  The relevant consequence is a stability one: an injected DLL that constructs its own C++
  objects inside a detour placed in one of the 707 lazy-static functions inherits that
  function's unwind contract. Keep detours free of C++ objects with destructors, which the
  project's existing "capture bounded POD facts and return" rule already requires.

- **Mod compatibility.** No authored data. Two mods can both hook parents of the same funclet
  without interacting, because the funclet is stateless and reads only the parent's frame.

---

## 7. What is not known

- [x] ~~**B-2/a** — Which specific empty destructor(s) the linker folded onto `0016D6A0`.~~
  **CLOSED 2026-09-07 — answered in the negative.** The question presumed one recoverable identity;
  there is none. The population is **everything in the program whose body is `ret 0`**, and
  `/OPT:ICF` destroyed the distinction at link time. **Two members survive, both named by something
  outside `.text` that still points at them:** the **Control Flow Guard check function**, named by
  the PE load config (`GuardCFCheckFunctionPointer = 0x008C31C0`, and the qword there is
  `0x0016D6A0`), and **at least one genuine array-element destructor**, named by this document's own
  `Unwind@0089dd0e` passing `0016D6A0` in a role a CFG check cannot occupy. Byte-level correction:
  the body is `C2 00 00` — **`ret 0`, not a bare `ret` (`C3`)**. Derived independently twice
  (`xiionline-61`, `xiionline-8d`). Name settled on `_guard_check_icall`.
- [x] **B-2/b** — Whether the 128 shape-ambiguous funclets in group D of §8 could be separated
  from `atexit` thunks by body evidence alone. They currently are not; their funclet identity
  rests on tier 8 (nothing takes their address) plus the structural table parse. *Answered 2026-09-26 (OPUS): not by body alone (75 share the shape of 1,144 atexit thunks), but the image's POGO record puts all 128 in `.text$x` and every registered atexit thunk in `.text$yd`; see the register row B-2/b and `_index/candidates/b2b-opus-funclet-section-split/`.*
- [x] **B-2/c** — The 136 magic statics that have no `_Init_thread_abort` funclet are assumed to
  have non-throwing constructors. Not individually verified. *Answered 2026-09-26 (OPUS): all 136 verified, none can reach a C++ throw (103 no call, 33 throw-free closures); see the register row B-2/c and `_index/candidates/b2c-opus-magic-statics-nothrow/`.*
- [x] **B-2/d** — `006DA980`'s original debug-build behaviour. The strings and the call survive;
  the reporting code does not. ~~*(NO ADMISSIBLE SOURCE (lost build), reviewed and signed 2026-09-26 by OPUS; see the register row B-2/d.)*~~ *OUT OF EVIDENCE BOUNDARY, 2026-09-27 (FABLE, Claude Opus 5.5): FRONTIER ruled that NO ADMISSIBLE SOURCE does not extend to a lost build artefact (batch-K Extension 2026-09-27b); OPUS's signature carries, on the same four conditions. See the register row B-2/d.*
- [x] ~~**B-2/e** — Which of the 250 unclassified funclet parents are game systems.~~
  **ANSWERED 2026-09-07 by `xiionline-8d`, and this question's own count was wrong.** Re-derived from
  `__CxxFrameHandler3` `FuncInfo` — **4,518 records, valid magic, 0 bad** — there are **4,314 parents,
  3,930 of them unowned**, not 250. Identity attacked with **strings (tier 2), never adjacency**: the
  identifiable unowned parents are **Phyre's script-binding and reflection layer, an octree, and an
  authored-event path parser** — engine and script infrastructure, **no battle or field logic**. The
  sharpened claim is therefore neither "none at all" nor "gameplay is hiding here". **This document's
  core claim survived the attack:** owned parents are Resource 222, Audio 92, Input 55, Save/Load 6,
  Platform 4, Core scheduling 3, Presentation 2, and **not one gameplay owner**.

  > ⚠ **Before re-deriving any of this, read `CH-1`.** The obvious traversal — `.pdata` →
  > `UNW_FLAG_CHAININFO` → chained `RUNTIME_FUNCTION` → parent — **manufactures 3,828 fake
  > "gameplay parents"** (Movement 127, ActorEntity 54, CombatAction 49 …) and reads exactly like a
  > refutation of this document. It is not: **all 11,339 resolvable CHAININFO entries chain to the
  > function they are already inside**, and **zero** chain to a parent registering
  > `__CxxFrameHandler3`. Every "parent" is its own parent.

---

## 8. Evidence

### The selector, stated — and why the answer does not depend on it

A census can only be as good as the query that produced it, and a selector copied from the
classification under test cannot falsify that classification. So the selector is stated here and
was checked two ways.

**Selector.** `DumpBodyCorpusByDomain.java` iterates each function's `FunctionTag` **set** (not a
joined text field) and takes any tag beginning `GFZ.V121.CodeDomain.`, then keeps the function if
that tag continues `CompilerGeneratedEH`. Set iteration sidesteps two known traps: composite
`;`-joined tag fields, and the CRLF that terminates the last column of a TSV dump.

**Check 1 — a different instrument, matching on tag *contents*.** Re-selecting over the
independently produced `graph_gn/functions.tsv` (38,161 rows, 38,161 distinct entries) by
substring `CompilerGeneratedEH` anywhere in the `;`-joined tag list returns **3,895**, symmetric
difference **0** against the selector above. No function in the binary carries more than one
V121 `CodeDomain` tag, so first-match and contents-match cannot diverge.

**Check 2 — the population was re-derived from the binary, not from the tag.** The
`.pdata → FuncInfo → UnwindMap / TryBlockMap / scope table` enumeration in this section never
consults a tag. It yields 3,899 declared funclets from the image itself, and the diff against the
tagged set is what produced findings 1–3 below. A mechanism mis-filed *out* of the
`CompilerGeneratedEH` namespace therefore cannot hide from this document: it would appear as a
declared funclet without the tag, and six did.

**Adjacent namespaces, dispositioned explicitly rather than by omission.** Over all 38,161 rows:

| namespace | n | in scope for B-2? |
|---|---:|---|
| `CompilerGeneratedCpp` | 417 | **No.** Generated C++ lifecycle (static teardown, container teardown, scalar deleting destructors). Runs at shutdown or on `delete`, not on an unwind. The 2,579 `atexit` thunks in §5 live here. |
| `CxxObjectLifecycle` | 225 | **No.** Same reason. |
| `CxxStandardLibrary` | 167 | **No.** Real STL implementation code; several are *callees* of funclets, none is one. |
| `CompilerGeneratedCFG` | 145 | **No.** The CFG guard adapters. Touches this document only because empty destructors were folded onto `0016D6A0`. |
| `Thunk` | 689 | **Partly, and it is checked.** 118 bare `jmp [rip+k]` thunks share a body shape with the terminate funclet, and 749 bare `jmp imm` thunks share one with the 86. The separation is in §10, not in the tag. |
| `Microsoft` | 106 | **No**, but two of its members (`001952E0`, `00195310`) are exact-body clones of a *tagged* pair and appear in finding 1. |
| everything else | — | **No.** None contains a declared funclet; check 2 proves it. |

**A whole-binary shape sweep was also run outside the selector.** Every one of the 38,161
functions was tested for a group-A four-instruction prologue prefix. **Six** non-EH functions
matched, all on the single weakest prefix `mov [rsp+0x10],rdx ; push rbx ; push rbp ; push rsi`,
where the discriminating `mov rbp,rdx` has not yet arrived at instruction four. Each was opened:

| address | body | owner / domain | verdict |
|---|---:|---|---|
| `00467D20` | 817 B | Presentation | full nine-register prologue, `this` in RCX; rejected |
| `007F5CC0` | 1,460 B | Audio | same; rejected. Interior read 2026-09-17 (SWE2-FRONTIER) agrees: calls the SEAD/CRI `007BA9xx`/`007F5xxx` audio band (`007BA950` ×3), first at [`007F5D05`](../../_index/ADDRESS-INDEX.md) — an audio worker, not an establisher frame |
| `007FC620` | 802 B | Audio | same; rejected |
| `0087F7F0` | 876 B | `ThirdParty.Physics.Bullet` | same; rejected |
| `00891C80` | 686 B | `ThirdParty.Audio.LibVorbis` | same; rejected |
| `00892610` | 888 B | Audio | does reach `mov rbp,rdx` — but only at offset `+0x24`, after nine pushes, a `sub rsp,0x58` and two reads through RCX. It is arg2 kept in a callee-saved register, not an establisher frame; rejected |

None is a declared funclet, all use RCX as `this`, and all are hundreds of bytes against a
funclet median of 12. **Noise floor for the group-A signature: 6 in 38,161, every one inspected
individually, none surviving.**

### The B-2 answer

**3,893 of the 3,895 are genuinely compiler-generated. Two are not, and six genuine ones are
missing from the classification.**

Two fully independent instruments were run and compared:

1. **Body shape.** Every one of the 3,895 exact-current bodies was disassembled and reduced to
   an operand-normalised skeleton (`Tools/work/h94/scripts/skel.py`, `consolidate.py`). No
   metadata of any kind was read. 46 distinct skeletons, all 3,895 accounted for.
2. **Structural handler-data parse.** `.pdata → UNWIND_INFO → FuncInfo → UnwindMap /
   TryBlockMap / scope table` was parsed to enumerate *which addresses the compiler declared as
   funclets* (`scripts/ehparse.py`). Per
   [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) this structural parse
   is permitted for funclet **existence** and is used here for nothing else — never to say what
   a function does, never to attribute ownership. Its built-in validity check (`FuncInfo` magic
   `0x19930520`-family) passed on all 4,518 records.

They agree on 3,893 addresses and disagree on nine, and every disagreement is a finding.

| group | n | what the **body alone** proves | corroborated by the parse |
|---|---:|---|---:|
| **A** RDX is used as the parent's establisher frame | **2,133** | funclet ABI, unambiguous — no ordinary function indexes locals off its second argument | 2,133 |
| **B** tail-calls `_Init_thread_abort(&guard)` | **1,545** | releasing a one-time-init lock is meaningful only while unwinding | 1,545 |
| **C** tail-jumps to `__std_terminate` | **87** | the `noexcept` failure path | 87 |
| **D** `lea rcx,[rip+.data]; jmp dtor` | **128** | destroys a named global — **shape-identical to an `atexit` thunk** | 128 |
| **E** takes `this` in RCX, ignores RDX | **2** | **not a funclet** | **0** |

**Finding 1 — two functions are misclassified, and the classification contradicts itself.**
`001AAF20` and `001AAF50` are tagged `CompilerGeneratedEH.AdjustedObjectCleanup`. Their
45-byte bodies take `this` in RCX, never touch RDX, and are not declared as funclets by the
compiler's own tables. They decompile to:

```c
void FUN_001aaf20(longlong *this) {
    longlong *nested = *(longlong **)( *this
                                     + (longlong)*(int *)(*(longlong *)*this + 4)   // signed vbase offset
                                     + 0x48 );
    if (nested) (**(code **)(*nested + 0x10))();      // virtual call, slot +0x10
}
```

That is an ordinary member function performing a virtual-base-adjusted virtual dispatch. It has
**two exact-body clones**, `001952E0` and `00195310`, and those two are tagged
`Microsoft.MSVCCRT_STL_Runtime.Support`. Four byte-identical bodies, two incompatible
classifications — at least one pair is wrong, and the EH pair is the wrong one, since neither
instrument places them in the funclet population. *This is the "real mechanism hiding behind
the classification" that B-2 asked about.* Its concrete identity — which class, which interface,
which slot-`+0x10` method — is not recovered here and stays numeric.

> **BK-6 answered 2026-09-12 (FABLE): the four bodies are `std::basic_ostream<char>` /
> `basic_istream<char>` `_Sentry_base::~_Sentry_base`, and both classifications were half right.**
> The owning functions come from the unwind maps: `001AAF20` is the state-0 and `001AAF50` the
> state-1 cleanup of **`001DDC40`** (an `istream` extractor — it imports `_Ipfx`, `ios_base::getloc`,
> `streambuf::sgetc` / `snextc`), `001952E0` the state-0 cleanup of **`00194B00`** and of `001DDE10`,
> `00195310` of **`00194CD0`** (`ostream` inserters — `sputc` / `sputn`, `_Osfx`, `flush`,
> `uncaught_exception`). The registered actions are the 12-byte stubs `008982F0` / `008982FC` /
> `008968B0` / `00898350` / `00896900` — each `lea rcx, [rdx + 0x28] ; jmp body` — so the
> **funclets** are the stubs (adjusted-object cleanup, exactly the tag's meaning) and the **bodies**
> are the ordinary destructor they tail-call on the local sentry at frame `+0x28`. That destructor
> is MSVC's `_Sentry_base::~_Sentry_base`: `rdx = *this` is the stream reference, `[rax + 4]` the
> `vbtable` displacement of the virtual base `basic_ios`, `[vbase + 0x48]` its `_Mystrbuf`, and slot
> `+0x10` of the streambuf vtable is **`_Unlock`** — `if (_Ostr.rdbuf()) _Ostr.rdbuf()->_Unlock();`.
> Four byte-identical copies are the four instantiations the linker kept (istream / ostream, two
> translation units each); the `Support` tag fits the bodies, the `AdjustedObjectCleanup` tag fits
> the stubs that reach them, and neither is a funclet body in its own right.

**Finding 2 — the classification is six short, not over-broad.** Seven SEH filter funclets
exist; only `008A5C0A` carries a `CompilerGeneratedEH` tag. `0089BEF0`, `008A5AD0`, `008A5B7C`,
`008A5B94`, `008A5BB2` and `008A5BDE` are declared in `__C_specific_handler` scope tables, sit
inside the funclet block, and their bodies are textbook CRT `__ArrayUnwind` scaffolding and
process SEH filters. They currently carry generic shape tags.

**Finding 3 — the "not a function" residue is fully explained.** Seven declared addresses are
not function entries: `005CCBCE`, `005CD2E0`, `007A3798`, `00808AE6`, `00808EB8`, `0080910C`,
`008634E4`. All seven are `JumpTarget` fields in scope tables — `__except` bodies live inside
their parent, not in a funclet. They are not missing functions.

Arithmetic, exactly: 3,820 unwind + 72 catch + 7 filters = **3,899 declared funclets**;
3,899 − 6 untagged = 3,893 tagged-and-declared; 3,893 + 2 misclassified = **3,895 tagged**.

### The killer observation, and what happened when it was sought

**The claim most likely to be false was group D** — 128 funclets whose two-instruction body is
byte-for-byte the same as a static-destructor `atexit` thunk. If even one of them were an
`atexit` thunk, "these are all EH" would be wrong, and the same doubt would spread to the other
1,620-shaped bodies.

The killer observation was named first: *an `atexit` thunk must have its address taken by code
somewhere, because something has to register it.* This database has already established (AR-4)
that in this image every rip-relative reference to a function entry is a `lea`.

So `.text` was swept function by function for a `lea reg,[rip+X]` where X is any of the 3,895
funclet entries, **with a positive control**: two known `atexit` thunks, `008A81D0` and
`008A9240`.

```
positive control  008A81D0   1 hit, from FUN_00160310:  atexit(FUN_008a81d0)
positive control  008A9240   1 hit, from FUN_00160be0:  atexit(FUN_008a9240)
3,895 funclet entries        0 hits
```

**Not one funclet address is materialised anywhere in `.text`.** None is registered with
`atexit`, stored in a vtable, or reachable by any means other than the unwinder. Group D
survives, and the reading was not broken.

The control mattered. An earlier run of the same sweep, disassembling `.text` linearly from a
single start address, returned **zero for everything including the controls** — it desynchronised
in the first few bytes and stayed wrong. Without the control it would have read as "no funclet
is referenced anywhere", the same answer the corrected instrument gives, for entirely the wrong
reason. Re-run per-function from each known entry point, it reproduces the 1,545
`_Init_thread_abort` tail jumps that had already been derived independently — that is the
control that says the instrument works.

### Claim table

| Claim | Evidence | Tier |
|---|---|---|
| The funclet ABI is `(rcx ignored, rdx = establisher frame)` | complete exact-current bodies of 2,133 functions; `mov rbp,rdx` / `lea rbp,[rdx+d]` / `[rdx+disp]` before any other use | 1 |
| A catch funclet returns a resume address inside its parent | complete body of `008A5C4B` returns `&DAT_008098E9`; its declared parent is `008098D4` | 1 |
| 1,545 funclets release a magic-static guard | complete bodies; tail target `0080926C` is a Ghidra FunctionID single match for `_Init_thread_abort` (VS2015 CRT), body read in full | 1 + 6 |
| FFXII has 1,681 lazily-initialised function-local statics, at 1,732 guarded sites in 707 functions | per-function disassembly of all 38,161 bodies: 1,732 `call _Init_thread_header` and 1,732 `call _Init_thread_footer` sites, each guard resolved from the `lea rcx,[rip+g]` immediately preceding it (1,732 of 1,732 resolved, all in `.data`); positive control passed | 1 |
| 1,545 distinct funclet guards, no repeats, `01F7F5C8`–`02EBA258`, every one also a header-site guard | rip-relative operand of each of the 1,545 funclet bodies, intersected with the 1,681 header-site guards: 0 orphans either way | 1 |
| The guard protocol is `0 / -1 / epoch` with a 100 ms retry | complete bodies of `008092FC`, `0080929C`, `0080926C`, and the call site in `FUN_00189CE0` | 1 |
| 172 funclets tail-jump to a body that is `ret` | complete body of `0016D6A0` = `C2 00 00`; per-function sweep counts 172 funclet jumps | 1 |
| That address is *also* the CFG check | PE load config `GuardCFCheckFunctionPointer` slot `008C31C0` holds `0016D6A0` | 7 |
| Empty destructors were folded onto it | complete body of `Unwind@0089dd0e` passes it as the *element destructor* argument of `_eh_vector_destructor_iterator` | 1 |
| 99 funclets carry stripped ppfx diagnostics | complete bodies; `006DA980` body is `C2 00 00`; the two string arguments read directly from `.rdata` | 1 + 2 |
| 18 middleware source paths recoverable from funclet bodies | rip-relative operands resolved to NUL-terminated ASCII in `.rdata` | 2 |
| 86 funclets are the `noexcept` terminate boundary | complete 5-byte bodies; `00861EAE` resolves through IAT slot `008C2A78` to `VCRUNTIME140!__std_terminate` | 1 + 3 |
| EH configuration: 4,377 / 5,372 / 141 / 9 | handler pointer of every `.pdata` record, resolved through the IAT; 4,377 + 141 = 4,518 valid `FuncInfo` magics | 7 |
| 1,609 parent functions, 246 owned, none in gameplay | parent RVAs from the structural parse, mapped to the current function list and its V120 tags | 7 + 11 |
| `001AAF20` / `001AAF50` are not funclets | complete bodies (RCX-based, RDX unused); absent from the declared set; two exact-body clones classified differently | 1 + 5 |
| No funclet is `atexit`-registered | `lea` sweep of all 38,161 bodies with a passing positive control: 0 hits on 3,895, 1 hit each on 2 controls | 8 |

### Comparison with work this database already held

Per rule 13 of the evidence standard, the corpus was searched before investigating.

[`../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md`](../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md)
already identified `mov rbp, rdx` as the funclet signature and corrected its own count from 147
to "135 functions and 12 funclets". **That reading is confirmed and generalised here** — the
same signature holds across 2,133 bodies. That document also reported "none of the twelve is a
`.pdata` `UnwindInfoAddress` target, 0 of 12". That is correct and is not a contradiction:
funclet entry points appear in `UnwindMapEntry.action` and `HandlerType.addressOfHandler`, never
in `RUNTIME_FUNCTION.UnwindInfoAddress`, so a test against unwind-info RVAs must return zero.
The 12–13 funclets it found carrying ppfx strings are a subset of the 100 found here by sweeping
every funclet body rather than a pattern list.

[`../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md`](../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md)
records that a peer session recovered EH funclets structurally from
`.pdata → UNWIND_INFO → language-specific data` and that the two residuals "reconcile exactly,
322 here vs 431 there, differing by precisely the `Unwind@`/`Catch_All@` entries this database
excludes at load". This pass reproduces that recovery independently and adds the six SEH filters
that a `FuncInfo`-only parse does not reach.

### Superseded readings

**Corrected in this pass — the count of lazily-initialised statics.**
[`../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md)
states *"117 more are lazy magic statics"* and *"these 117 globals do not exist until something
calls their accessor"*. The mechanism it describes is exactly right and its decompiled gate
matches this one instruction for instruction. **The number is not.** 117 is the size of the
`CompilerGeneratedCpp.ThreadSafeStaticRecordAccessor` tag population — a count of how many
functions received one label — not a census of magic statics. Counting the mechanism itself
gives **1,681 statics at 1,732 guarded sites across 707 functions**, of which 1,545 carry an
unwind funclet. The
earlier figure was reachable because a tag population and a mechanism census look identical when
you only have the tag; it is the same failure mode the evidence standard already records for
hand-maintained indexes. That document is owed a `REOPENED` status and a corrected §4.

**Withdrawn during this pass — "the linker folded every empty function onto one address".**
Initially the 172 jumps to `0016D6A0` were read as wholesale identical-COMDAT folding. Counting
tiny bodies refutes the strong form: **34 distinct addresses in this binary have the body
`C2 00 00`**, so folding is partial, not global. The surviving claim is the narrow one — at
least one empty destructor shares `0016D6A0`, proven by `Unwind@0089dd0e` passing it as an
array-element destructor — and the run-time consequence (`ret`) is unchanged.

**Corrected in this document, same day, by finishing the measurement.** This document first
reported "1,732 lazily-initialised function-local statics" and "the 187 without a funclet". That
conflated **construction sites with objects**. Resolving the guard operand at each of the 1,732
`_Init_thread_header` sites — the `lea rcx,[rip+g]` immediately preceding the call, 1,732 of
1,732 resolved, all landing in `.data` — gives **1,681 distinct guards**. Nineteen guards appear
at more than one site, always in different functions (the accessor was inlined into several
callers), which accounts for the 51 difference exactly. So the object count is 1,681, the site
count is 1,732, and the number without a funclet is **136, not 187**. The error was reachable
because the site count was measured first and read as if one site meant one object; it is the
same class of mistake as counting a tag population and calling it a census, one level down. The
funclet-side figures (1,545) were never affected, and the two sets reconcile with **zero orphans
in either direction**.

**Not challenged this pass:** the identity of the 827 downstream callees, the 250 unclassified
parents, and whether the 46 skeletons are stable under a future re-analysis of the program.

---

## 9. Related

- [`../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md) —
  the eager side of the same lifetime story, and the document this pass corrects on the lazy count.
- [`../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md) —
  `/GS` cookies (5,372 functions here carry `__GSHandlerCheck`) and the CFG check whose address the
  folded destructors share.
- [`../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md`](../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md) —
  the PostEffects middleware whose stripped diagnostics survive inside 99 of these funclets.
- [`../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md`](../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md) —
  why funclets have no callers, and the independent structural recovery this pass reproduces.
- [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) —
  the banned-evidence list, and the carve-out that permits a structural parse for funclet existence.
- [`../README.md`](../README.md) — category index.

---

## 10. Falsification pass — 2026-09-02

Run against snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`
(GN checkpoint, ledger 38,161 / 38,003 / 158, verified before any analysis began).

**Attacked: "all 3,895 are compiler-generated."** *Killer:* a body that does not fit any
compiler-generated shape. Result: **the claim broke.** Two bodies do not fit — `001AAF20`,
`001AAF50` — and the disagreement was independently confirmed by the structural parse, which
does not declare them. The claim is now stated as 3,893 of 3,895, with the two named.

**Attacked: "the shape families are diagnostic."** *Killer:* non-EH functions with the same
complete body shape. Result: **found, in quantity.** 1,328 non-EH functions share the
`lea rcx,[rip+k]; jmp imm` shape, 749 share the bare `jmp imm` shape, 118 share `jmp [rip+k]`,
and the 45-byte `AdjustedObjectCleanup` body has 2 non-EH exact clones. Shape alone is therefore
**not** sufficient for 1,762 of the tagged set; only the 2,133 RDX-frame bodies and the 1,545
`_Init_thread_abort` tails are self-proving. This is why §8 splits the population into
evidence groups instead of claiming one blanket tier.

**Attacked: "group D are not `atexit` thunks."** *Killer:* any code that takes a funclet's
address. Result: **survived**, with a passing positive control (2/2 known `atexit` thunks found,
0/3,895 funclets found). Documented in §8 including the first, broken run of the instrument.

**Attacked: "the linker folded empty destructors onto `0016D6A0`."** *Killer:* many distinct
`ret`-only addresses, which would mean folding did not happen. Result: **the strong form broke**
— 34 distinct `C2 00 00` bodies exist. The narrow form survives on a direct body observation
(`Unwind@0089dd0e` passes `0016D6A0` as an array-element destructor, which a CFG check cannot
be). Recorded as a withdrawal in §8.

**Attacked: "117 lazy magic statics" (inherited from a sibling document).** *Killer:* a direct
count of the mechanism disagreeing with the tag count. Result: **the inherited claim broke.**
1,732 `_Init_thread_header` call sites, 1,732 `_Init_thread_footer` call sites, 1,681 distinct
guards, 707 containing functions, 1,545 guards with unwind funclets. Reopening filed.

**Attacked: "the 3,895 are the whole population."** *Killer:* a funclet sitting outside the tag
namespace the selector queries — the failure mode that cost `23-Third-Party-Libraries` an entire
library on the same day. Result: **the claim broke, in the direction predicted.** Six declared
funclets carry no `CompilerGeneratedEH` tag (finding 2). They were found because the population
was re-derived from the image rather than re-selected from the classification; a prefix query
over the tag would have reproduced 3,895 and read the agreement as confirmation. The selector
itself was then re-derived over a second, independently produced graph dump by contents-match
and agreed exactly. Both are stated in §8 rather than left implicit.

**Attacked: "RDX-as-establisher-frame identifies a funclet."** *Killer:* ordinary functions with
the same register move. Result: **the loose form broke** — 3,552 functions binary-wide load a
frame register from RDX, because that is also how any function keeps argument 2 alive. The
surviving form is the complete prologue, whose noise floor is 6 in 38,161, each inspected and
rejected. §2 now warns against the loose statement explicitly.

**Attacked: "no gameplay mechanism is in this set."** *Killer:* a funclet parent owned by
Combat, Movement, Party, Actor, Spawn or Script. Result: **survived.** All 1,609 parents were
enumerated; the owned ones are Resource 182, Audio 41, Input 11, Save/Load/Settings 5, Platform
4, Presentation 2, scheduling 1. The instrument demonstrably reports owners, so the absence is
not an empty query. The residual weakness is the 250 parents with no classification at all,
filed as B-2/e.

**Re-checked for banned evidence.** The `.pdata`/`FuncInfo` parse appears in this document only
as an existence enumerator and a handler census, per the standard's explicit carve-out. No claim
about what any function *does* rests on it; every such claim in §8 cites a complete body. The
one place a table result stands alone — the parent census in §5 — is labelled tier 7/11 and is
not used to assign ownership to anything.

**Physically verified.** All 3,895 tagged addresses resolve in the current parent with the body
extents used here (dumped from the live program, not from a stored list); the 3,899 declared
funclet addresses were re-derived from the embedded EXE whose SHA-256 reproduced as
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8` during checkpoint
verification.

**Not attempted, and therefore not claimed:** runtime confirmation that any funclet ever
executes; the source-level identity of the folded empty destructor; individual verification of
the 136 magic statics without a funclet.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Application — CLIENT.** The Phyre framework teardown `00793250`, which funclet `00896280` tail-jumps to, is also
called by a 26-byte Application-filed body, so it has an ordinary caller besides the funclet.

## 11. The `00808D78` exclusive subtree — all 9 members bound (SWE2-FRONTIER, followup queue)

`00808D78` (`MSVCCRT.ExecutableStartup`, the entry the config pages reach through `007A3770`) owns
nine functions — the `__scrt` startup battery around the `main` hand-off. Every member was
disassembled from the shipping image; interior citations are instructions inside each member's
declared extent.

| member | role | interior |
| --- | --- | --- |
| `00808900` `__scrt_acquire_startup_lock` | 57 B — the `02EAED00` startup spin-lock acquire (`00809960` yield/sleep) | [`00808904`](../../_index/ADDRESS-INDEX.md) |
| `0080893C` `__scrt_initialize_crt` | 73 B — the `02EAED38` init-state machine driving `__isa_available_init` + `0061ECF0` | [`00808959`](../../_index/ADDRESS-INDEX.md) |
| `00809458` `__isa_available_init` | 454 B — CPU feature detection: `cpuid` ×3 + `xgetbv`, publishes the ISA-level dwords `01F44858`–`01F44860`/`02EAED88` | [`0080947C`](../../_index/ADDRESS-INDEX.md) |
| `00809AB4` `__scrt_get_show_window_mode` | 60 B — `GetStartupInfoW` (`008C23A8`); returns `wShowWindow` when `STARTF_USESHOWWINDOW` else `0xA` | [`00809AE5`](../../_index/ADDRESS-INDEX.md) |
| `00809AF0` `__scrt_is_managed_app` | 84 B — `GetModuleHandleW(0)` → MZ/PE sig checks → PE32+ magic `0x20B` → CLR directory `[+0xF8]!=0` | [`00809B3C`](../../_index/ADDRESS-INDEX.md) |
| `00809C78` | 8 B — returns `&02F974E8` (CRT argv-family static cell) | [`00809C78`](../../_index/ADDRESS-INDEX.md) |
| `00809C80` | 8 B — returns `&02F974E0` (the adjacent cell — the `00809C78` pair) | [`00809C80`](../../_index/ADDRESS-INDEX.md) |
| `00808AF0` `__scrt_release_startup_lock` | 36 B — the `02EAED00` lock release | [`00808AF6`](../../_index/ADDRESS-INDEX.md) |
| `00808B14` `__scrt_uninitialize_crt` | 43 B — the `02EAED38` shutdown path via `0061ECF0` | [`00808B2B`](../../_index/ADDRESS-INDEX.md) |

The root's other callees — `007A3770` (the game `main` equivalent), the `00809958`/`0080996C`/
`00808ED9`/`00808E15`/`00808A54` intra-startup helpers, the `00861Fxx`/`008620xx` CRT leaves, and the
`008Cxxxx` IAT slots — have other callers and are excluded from the exclusive census.

## SWE2-EC7-19 update (2026-05-15) — `008098D4` conversion-tail fragment

`008098D4` (26 B window) is the parent body this page already discusses for its self-return `0x008098E9`: the window's real content is `mulpd xmm3,xmm1` → `cvttpd2dq xmm3,xmm3` → `pshufd xmm3,xmm3,0xDC` → `por xmm3,[rip+0x27FB7B7]` (`008098D8`..`008098E1`) — the double→packed-int conversion + mask-merge half of the CRT float helper the page's funclet discussion frames.

## SWE2-EC7-38 update (2026-09-19) - `00194CD0`

`00194CD0` (455 B) is a call-free exception funclet - `word[rdx]` length walk (`inc r14` loop), `008C2688`/`008C2710`/`008C2690` rdata, SEH-style frame stores. Interior anchor `00194D10` (the `inc r14` step).

## SWE2-EC7-39 update (2026-09-19) - `00194B00`

`00194B00` (441 B) is the stream inserter the page names - eight `008C26xx` import-thunk calls plus two vcalls; `001952E0` is its state-0 cleanup. Interior anchor `00194B9C` (an `008C26E8` thunk call).

## SWE2-EC7-39 update (2026-09-19) - `001DDC40`

`001DDC40` (430 B) is the istream extractor the page names - `_Ipfx`/`getloc` imports, `001AA6C0`, three vcalls plus `00195CF0`. Interior anchor `001DDC9C` (an `008C2540` thunk call).

## SWE2-EC7-39 update (2026-09-19) - `001DDE10`

`001DDE10` (419 B) is the second stream inserter sibling - `008C2660` triple plus `008C26E8`/`008C26A0`/`008C2600`/`008C26D0` thunks and two vcalls. Interior anchor `001DDE7C` (an `008C26E8` thunk call).

## SWE2-EC7-79 update (2026-09-20) - `0061ECF0` constant-one measured

`0061ECF0` (3 B) is the `return 1` stub the lazy-guard callers use
as their success sentinel - no body beyond `mov al, 1; ret`.
Interior anchor `0061ECF2` (the `ret`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

The funclet census opened candidate frames and rejected most of them, so it cites ordinary bodies from several
layers.

- **Audio — CLIENT, 32 edges.** The rejected candidates `007F5CC0`, `007FC620` and `00892610` are audio workers.
  - `007F5CC0` calls the SEAD/CRI band (`007BA050`-`007BA230`, `007BA950`).
  - `007FC620` calls `007F8460`, `007F9360` and `007FA810`.
  - `00892610` calls `0017CB40`, `00882180` and `00883E90`.
  - The audio caller `00212130` reaches the SEH-filter parent `005CD1E0`.

  None is an establisher frame; the sound pages own what they do.
- **Resource — MECHANICAL, two edges.** `005CD1E0` is also called by `001DAAC0`, and the catch-funclet example's parent
  `008098D4` by `001F4250`.
- **CoreRuntimeScheduling and Presentation — MECHANICAL, one edge each.** The magic-static example `00189CE0` is
  reached from the frame step `0017D6E0`, and the rejected `00467D20` from `002F6AB0`.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 slice OPUS-P22-SLICE-24-99).*
