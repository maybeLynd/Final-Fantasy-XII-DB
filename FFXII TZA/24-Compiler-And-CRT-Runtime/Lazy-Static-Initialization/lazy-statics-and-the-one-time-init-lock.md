---
system: Lazy statics and the one-time-init lock
category: 24-Compiler-And-CRT-Runtime
status: AUDITED
owner_layer: CodeDomain:CompilerGeneratedCpp + Microsoft.MSVCCRT_STL_Runtime
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
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
  - "magic-static descriptor-pair accessors | C | members/descriptor-pair-accessors.tsv | 61 | not this game's code: compiler-generated MSVC thread-safe local-static accessors returning &static where the static is a 16-byte pair {record|1, 0}. PROVED BY OPERAND-LEVEL FORM, NOT BY SIZE - every member is exactly the fixed 22-instruction 115-byte sequence (TLS index load gs:[0x58] -> _tls_index slot 02EAED3C, epoch compare, guard fast-path lea rax,[static]; ret, _Init_thread_header 008092FC, guard==-1 check, lea rax,[record]; mov [static+8],0; or rax,1; mov [static],rax, _Init_thread_footer 0080929C, jmp fast) and the only varying operands are the guard cell, the static pair and the record, with guard = static+0x10. NO atexit - the pair is POD. The 61 accessors share 27 distinct .data records, several already identified as Phyre PClassDescriptorConcrete<> singletons. SELF-BOUNDING: a census-wide scan for the exact 115-byte form finds exactly 61 bodies, all frontier - 0 A-measured, 0 declared elsewhere. THE BOUNDARY: the accessor idiom is the toolchain's; a reconstruction that declares the same magic statics gets these from its own compiler. NOT dispositioned: the 27 payload records, the 61 static pairs and guard cells, and the machinery helpers themselves. Selector: members/select_descriptor_pair_accessors.py"
  - "thread-safe magic-static singleton guards | C | members/magic-static-singleton-guards.tsv | 17 | not this game's code: compiler-generated MSVC thread-safe local-static initialisation stubs. PROVED BY CALL-SET SIGNATURE, NOT BY SIZE - every member's ENTIRE call set is exactly {_Init_thread_header 008092FC, _Init_thread_footer 0080929C, atexit wrapper 00808B90}; the init payload is inlined stores only (TLS index load gs:[0x58] -> _tls_index slot, epoch compare on the per-static guard cell, init stores, footer, atexit registration). Sizes vary 98..474 B because the payload is inlined. SELF-BOUNDING: a census-wide scan of every function for this exact call set finds 39 bodies - the 18 frontier members, 13 already declared by Phyre.Reflection.StaticDescriptorSingleton, 5 by the Phyre module families, 3 A-measured. THE BOUNDARY: the guard idiom is the toolchain's; a reconstruction that declares the same magic statics gets these from its own compiler. NOT dispositioned: the guard cells and objects each member initialises, and the machinery helpers themselves. Selector: members/select_magic_static_guards.py 1 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 00632780"
  - "magic-static descriptor-pair initialisers | C | members/magic-static-pair-initialisers.tsv | 57 | not this game's code: compiler-generated MSVC thread-safe local-static accessors - the init-CALLING siblings of the 61-member 115-byte descriptor-pair accessors above. PROVED BY FORM - three instruction-form skeletons, each collapsing to ONE operand-aware byte image: 133 bytes x16 (payload is inlined stores only; call set exactly {_Init_thread_header, _Init_thread_footer}), 134 bytes x25 and 138 bytes x16 (payload adds ONE member-specific init call). Every member: TLS-index load gs:[0x58] -> _tls_index slot, epoch compare on the per-static guard cell, _Init_thread_header/footer bracket around the payload, install a descriptor PAIR (one statically-known pointer tagged |1, plus either a second tagged constant or the init call's result - tagged in the 138-byte spelling, untagged in the 134-byte), zero the adjacent slot, return &static. CONTROL: external direct targets per member are exactly {008092FC, 0080929C} plus at most one init callee; the nine init callees are 00630180 x18, 0062FF50 x7, 006301F0 x4, 006B19A0 x3, 00630490 x3, 006B09E0 x2, 006B1600 x2, 006B33F0, 006B0EC0. THE BOUNDARY: the descriptor addresses, the guard cells and the init callee vary per member; the idiom is the toolchain's. NOT dispositioned: the nine init callees and what each pair describes. Selector: members/select_magic_static_pair_initialisers.py"
---

# Lazy statics and the one-time-init lock

> 1,681 pieces of the engine are built the first time somebody asks for them, behind a single
> lock — and a mod that interrupts one of those first builds hangs the game forever, silently,
> with no crash and normal CPU usage.

## 1. What the player sees

**The hang.** The game stops on a loading screen. Not a freeze in the usual sense — no black
screen, no "not responding" title bar, no crash dialog, no error log. The music may keep playing.
Task Manager shows the process alive and using a normal amount of CPU. Nothing ever finishes
loading, and the only way out is to kill it.

This is not a bug in the retail game. It is what happens when something *else* — an injected DLL,
a trainer, a debugger that swallowed an exception, a hook that returned early — interrupted the
engine halfway through building one of its internal objects for the first time.

Here is why it looks like that. Large parts of FFXII do not exist when you launch it. The engine
builds them the first time anything needs them: the first time a zone loads, the first time a
particular kind of object appears, the first time a save file is written. Each of these
first-builds is protected so that two threads cannot both do it at once — the first thread to
arrive puts up a sign saying *"building this, wait"*, and everybody else waits, re-checking ten
times a second. When the first thread finishes it takes the sign down and wakes the others.

**If the first thread never finishes, the sign never comes down.** Everyone else waits forever,
politely, ten times a second, which is why the process looks healthy. And because all 1,681 of
these first-builds share *one* lock, ~~a single stuck one can pile unrelated work up behind it~~ but a stuck one blocks only the threads that need that same static *(corrected 2026-10-02, OPUS: the header releases the lock before the construction runs, `008092FC+0x60` tail-jumps `LeaveCriticalSection`, and the 100 ms wait sleeps with the lock released, `008093C0+0x4B` calls `SleepConditionVariableCS` on `02EAED40`)*.

Loading screens are where this shows up because that is where most first-builds happen: a new
area introduces object types the game has not touched yet.

**What the mechanism buys you the other 99.9 % of the time** is start-up speed and honesty about
what the game actually uses. FFXII ships with descriptions of every kind of object it knows how
to build, save and load — over a thousand of them — and building all of that at launch would
cost seconds you would sit through every single time. Instead it builds each description the
first time that kind of object is touched. A playthrough that never enters a particular kind of
area never pays for it.

No addresses in this section. Everything below has them.

---

## 2. Native mechanism

### The shape, and how many

Every C++11 function-local `static` with a non-trivial constructor compiles to the same guarded
block. Counting them by disassembling all 38,161 function bodies:

| measurement | value |
|---|---:|
| guarded construction sites (`call _Init_thread_header`) | **1,732** |
| matching `call _Init_thread_footer` | **1,732** |
| distinct guard variables behind them, all in `.data` | **1,681** |
| functions containing at least one | **707** |
| of those, functions that also call `atexit` | **526** |
| of those, functions that call a `Phyre.Reflection.*` routine | **535 (75.7 %)** |

Sites exceed objects because 19 guards appear at more than one site, always in *different*
functions — the compiler inlined one accessor into several callers, accounting for the 51
difference exactly. The distribution is long-tailed: 451 functions hold exactly one lazy static,
99 hold four, and two functions (`005AD8F0`, `005E5400`) hold **28 each**.

### What is actually being built

Three quarters of it is **PhyreEngine's description of its own object types** — the metadata that
lets the engine serialise an object to a save file, bind a resource to a field, or answer a
property lookup by name. Across the 707 holder functions:

| callee | calls | what it does |
|---|---:|---|
| `00632960` `Phyre.Reflection.DataMemberRegistration` | 680 | builds one `Phyre::PClassDataMember` and hands it to the class descriptor |
| `00630180` / `006301F0` / `006373D0` `StaticDescriptorSingleton` | 602 | the per-type descriptor singletons themselves |
| `006388C0` `Phyre.Reflection.TypeNameRegistry` | 301 | registers/looks a type up by a hash of its name |
| `00632FB0` `Phyre.Reflection.SharedRuntime` | 216 | shared descriptor construction |
| `0067F700` `Runtime.ContainerStringSupport` | 146 | the strings those records hold |

and the field names come through as authored ASCII in the holder bodies — `m_count` (71
functions), `m_els` (60), `m_size`, `m_name`, `m_type`, `m_elements`, `m_localToWorldMatrix`,
`m_texture`, `getLocalToWorldMatrix`, `setX`, `setY`. 347 of the 707 reference at least one such
string, 890 distinct strings in all. A concrete example, from `005AD8F0`:

```c
FUN_00632960(&DAT_02cb0a40, &DAT_02cad140, &DAT_02cae660, "m_animationSet", 0x20, 0x12, 0, 0, ...);
//           ^ the record   ^ the class     ^ the type     ^ field name    ^off  ^attrs
```

That is the engine writing down "class X has a field called `m_animationSet` at byte offset
0x20, of the type described by that object" — on first use, not at startup. **This is why the
lazy path matters to a modder at all:** it is not obscure CRT plumbing, it is where the engine's
schema comes from, and the schema is recovered field by field in
[`../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md).

> **Corrected 2026-09-02.** This example first read the fifth and sixth arguments as "32 bytes
> wide, of type 0x12". Both were wrong: the fifth is a **byte offset**, the sixth an **attribute
> bitfield**, and the type is the third argument, a pointer. The mis-reading came from taking a
> decompiler's positional arguments at face value without reading the callee `00632FB0`, and it
> is what caused BJ-4 to be filed with a false premise. See section 8 of the schema document.

The remaining quarter is ordinary singletons. ~~`008AADA0` builds~~ `005CDA30` builds `Phyre::PTTYCallback` *(corrected 2026-10-02, OPUS: `005CDA30+0x56` stores vtable `00D360A0` (RTTI `Phyre::PTTYCallback`) at `02CB6140`, `005CDA30+0x4F` loads `008AADA0` and `005CDA30+0x5D` registers it with `atexit` `00808B90`; `008AADA0` caches the singleton pointer at `02CB6150`)* (the debug
console callback); `005C3B10` is a ~~three-line accessor that zeroes two words~~ guarded accessor that stores `02CAD140` with bit 0 set and `0` into its two words *(corrected 2026-10-02, OPUS: `005C3B10+0x48` loads `02CAD140`, `005C3B10+0x5A` sets bit 0 and `005C3B10+0x65` stores it at `02CB5D48`; `005C3B10+0x4F` zeroes `02CB5D50`)* and returns their
address — the worked example of the **magic-static descriptor-pair accessors** family (61 members,
all the identical 115-byte form; see `function_families` and
[`members/descriptor-pair-accessors.tsv`](members/descriptor-pair-accessors.tsv)).

### The protocol

Three CRT routines and one lock do all of it.

**`_Init_thread_header(&guard)`** claims the guard. It takes the process-wide critical section,
then loops: if the guard is `0` it writes `-1` (*"mine, under construction"*) and returns; if the
guard is anything other than `-1` the object already exists, so it just refreshes this thread's
epoch and returns; and if it is `-1` somebody else is building it, so it calls
`_Init_thread_wait(100)` and goes round again.

**`_Init_thread_footer(&guard)`** publishes it: bump the global epoch, stamp it into the guard and
into this thread's TLS slot, release the lock, wake the waiters.

**`_Init_thread_abort(&guard)`** puts the guard back to `0` and wakes the waiters. This is the
one the compiler wires into an **exception unwind funclet** — 1,545 of the 1,681 guards have one,
so that a throwing constructor releases the claim instead of stranding it. The 136 without are
the constructions that cannot throw. Those funclets are documented in
[`../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`](../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md).

**The fast path costs one TLS read and one compare.** Once the object exists, its guard holds a
positive epoch number; a thread whose own epoch is already at least that high skips the entire
block without touching the lock. That is what makes 1,681 lazy singletons affordable.

### Waiting and waking

`_Init_thread_wait(ms)` has two implementations chosen at run time by whether a fallback event
handle at `02EAED70` is non-zero:

- **Condition variable (the normal path).** It calls a function pointer kept *encoded* in
  `.data` — the CRT decodes it as `ror64(cookie ^ slot, cookie & 0x3F)` — passing the condition
  variable at `02EAED68`, the critical section at `02EAED40`, and the timeout. This is
  `SleepConditionVariableCS`, and `_Init_thread_notify` decodes the matching slot at `02EAED80`
  to wake all waiters.
- **Event fallback.** If `02EAED70` holds a handle: leave the critical section, `WaitForSingleObjectEx`
  on it for the timeout, retake the critical section. `_Init_thread_notify` then does
  `SetEvent` followed immediately by `ResetEvent`.

Either way the timeout at every call site in this binary is **100** — ten wake-ups a second,
forever, which is exactly why a stuck guard burns a small, steady, entirely innocent-looking
amount of CPU.

### Teardown

526 of the 707 holders call `atexit` inside the guarded region, so the object registers its own
destructor at the moment it is built. Destruction then happens in reverse registration order at
process exit, on the same chain the eagerly-constructed globals use — see
[`../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md).
A consequence worth noticing: **the shutdown order of the lazy statics depends on what the player
did**, because it depends on the order in which they were first touched.

---

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `008092FC` | `_Init_thread_header` | 103 B | claims a guard, or waits; **1,732** call sites in 707 functions |
| `0080929C` | `_Init_thread_footer` | 96 B | publishes a completed object; **1,732** call sites |
| `0080926C` | `_Init_thread_abort` | 48 B | releases a claim after a throwing constructor; reached only from unwind funclets |
| `008093C0` | `_Init_thread_wait` | 151 B | the 100 ms wait, condition variable or event |
| `00809364` | `_Init_thread_notify` | 91 B | wakes waiters |
| `00808B90` | `atexit` | 23 B | 526 of the 707 holders call it inside the guard |
| `00632960` | `Phyre.Reflection.DataMemberRegistration` | 165 B | 680 calls; builds a `Phyre::PClassDataMember` |
| `006388C0` | `Phyre.Reflection.TypeNameRegistry` | 254 B | 301 calls; the name hash in §4 |
| `00630180` | `StaticDescriptorSingleton` | — | a lazy static whose whole guarded body is one `atexit` |
| `005C3B10` | minimal accessor | 115 B | the clearest worked example |
| `008AADA0` | `Phyre::PTTYCallback` singleton | 197 B | one of the 19 multi-site guards |
| `005AD8F0` | heaviest holder | 5,580 B | 28 lazy statics in one function |
| `005E5400` | heaviest holder | 4,088 B | 28 lazy statics in one function |
| `00189CE0` | worked example in §4 | — | guard `01F7F5C8`, funclet `Unwind@008964A0` |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02EAED40` | `_Init_thread_lock` | `CRITICAL_SECTION` | the **single** lock shared by all 1,681 |
| `02EAED68` | `_Init_thread_cv` | `CONDITION_VARIABLE` | what a blocked thread sleeps on |
| `02EAED70` | fallback event handle | `HANDLE` | zero on the condition-variable path |
| `02EAED78` | encoded `SleepConditionVariableCS` | encoded function pointer | decoded per §4 |
| `02EAED80` | encoded `WakeAllConditionVariable` | encoded function pointer | decoded per §4 |
| `01F44850` | `_Init_global_epoch` | `int` global | the counter stamped into completed guards |
| `01F44830` | `__security_cookie` (also the CRT pointer-encoding key) | `u64` global | referenced by 2,216 functions; identity **BJ-2**, answered 2026-09-14 |
| `02EAED3C` | `_tls_index` | `u32` global | selects this module's TLS block |
| TLS block `+0x04` | `_Init_thread_epoch` | per-thread `int` | this thread's observed epoch |
| `01F7F5C8` | the worked example's guard | `int` in `.data` | the guard used throughout §4 |
| `01F7F5C8`–`02EBA258` | magic-static guards | `int`s scattered in `.data` | the 1,545 that carry an unwind funclet |

---

## 4. Data structures and formulas

### The gate compiled at all 1,732 sites

Verbatim from `FUN_00189CE0`, guard `01F7F5C8`:

```c
#define thread_epoch  (*(int *)(*(char **)((char *)ThreadLocalStoragePointer \
                                           + (unsigned long long)_tls_index * 8) + 4))

if (thread_epoch < guard) {          // fast path: already built for this thread -> skip entirely <- corrected 2026-10-02, OPUS - backwards: thread_epoch < guard is the SLOW path that calls the header; already built is thread_epoch >= guard, where 00189CE0+0x63 jle skips the header
    _Init_thread_header(&guard);
    if (guard == -1) {               // -1 means THIS thread owns the construction
        /* ...construct... */        //  <- a throw here runs the guard's unwind funclet
        _Init_thread_footer(&guard);
    }
}
/* ...use the object... */
```

### The guard state machine

```
*guard ==  0   never initialised            -> claim it
*guard == -1   under construction right now -> wait 100 ms, re-check, repeat
*guard  >  0   built; value is the epoch at which it completed   <- corrected 2026-10-02, OPUS - not > 0: the epoch ships 0x80000000 (01F44850) and the footer stores ++epoch (0080929C+0x29 inc, 0080929C+0x31 store), so a built guard is negative as a signed int
```

The only transitions out of `-1` are `_Init_thread_footer` (to a positive epoch) and
`_Init_thread_abort` (back to `0`). **Nothing else clears it.**

### The three CRT routines, exact

```c
void _Init_thread_header(int *g) {
    EnterCriticalSection(&_Init_thread_lock);            // 02EAED40
    for (;;) {
        if (*g ==  0) { *g = -1; break; }                // claim
        if (*g != -1) { thread_epoch = _Init_global_epoch; break; }   // already built
        _Init_thread_wait(100);                          // someone else owns it
    }
    LeaveCriticalSection(&_Init_thread_lock);
}

void _Init_thread_footer(int *g) {
    EnterCriticalSection(&_Init_thread_lock);
    _Init_global_epoch = _Init_global_epoch + 1;         // 01F44850
    *g           = _Init_global_epoch;
    thread_epoch = _Init_global_epoch;
    LeaveCriticalSection(&_Init_thread_lock);
    _Init_thread_notify();
}

void _Init_thread_abort(int *g) {
    EnterCriticalSection(&_Init_thread_lock);
    *g = 0;
    LeaveCriticalSection(&_Init_thread_lock);
    _Init_thread_notify();
}
```

### Wait and notify, with the pointer decode

```c
bool _Init_thread_wait(unsigned ms) {
    if (*(HANDLE *)0x02EAED70 == 0) {
        fn = ROR64(cookie ^ *(u64 *)0x02EAED78, cookie & 0x3F);   // cookie = *(u64*)0x01F44830
        _guard_check_icall(fn);
        return fn(/*cv*/ 0x02EAED68, /*cs*/ 0x02EAED40, ms) != 0; // SleepConditionVariableCS
    }
    LeaveCriticalSection((void *)0x02EAED40);
    r = WaitForSingleObjectEx(*(HANDLE *)0x02EAED70, ms, FALSE);
    EnterCriticalSection((void *)0x02EAED40);
    return r == 0;
}

void _Init_thread_notify(void) {
    if (*(HANDLE *)0x02EAED70 == 0) {
        fn = ROR64(cookie ^ *(u64 *)0x02EAED80, cookie & 0x3F);   // WakeAllConditionVariable
        _guard_check_icall(fn);
        fn(/*cv*/ 0x02EAED68);
        return;
    }
    SetEvent(*(HANDLE *)0x02EAED70);
    ResetEvent(*(HANDLE *)0x02EAED70);
}
```

`ROR64(v, n)` is `(v >> n) | (v << (64 - n))`. The timeout is the literal `100` at every call
site, so a blocked thread wakes **ten times a second, indefinitely**.

### The Phyre type-name hash, from `006388C0`

```c
unsigned h = 0x7B5;                       // 1973
for (const unsigned char *p = name; *p; ++p)
    h = h * 0x21 + (*p & 0x1F);           // 0x21 = 33
```

Only the low five bits of each character contribute, so `'a'` (0x61) and `'A'` (0x41) hash
identically — **the type-name registry is case-insensitive for ASCII letters by construction**,
and any two names differing only in case, or in bit 5 or 6 of any character, collide.

### Reflection record construction, from `00632960`

```c
PClassDataMember *reg(PClassDataMember *rec, ClassDescriptor *cls, void *typeInfo,
                      const char *name, u32 size, u32 typeId, int flag, void *ctx) {
    build_shared(rec + 1, cls, name, typeId, -2);
    rec[6]  = typeInfo;
    rec[7]  = &rec[7];  rec[8] = &rec[7];      // empty intrusive list, self-linked
    rec[0]  = Phyre::PClassDataMember::vftable;
    *(u32 *)&rec[9] = size;
    rec[10] = 0;
    saved = *(u32 *)&rec[5];
    if (flag == 2) *(u32 *)&rec[5] = saved | 2;
    (*(void (**)(...))(*(void **)cls + 0x40))(cls, rec, ctx);   // descriptor virtual slot +0x40
    *(u32 *)&rec[5] = saved;
    return rec;
}
```

---

## 5. Call chain

```
gameplay reaches a type or singleton for the first time
  -> the containing function's guarded block  (1,732 sites in 707 functions)
     -> thread_epoch < guard ?
        no  -> use the object, no lock taken            <- the overwhelmingly common path
        yes -> _Init_thread_header(&guard)      008092FC
               -> EnterCriticalSection 02EAED40
                  guard == 0  -> claim it (-1)
                  guard == -1 -> _Init_thread_wait(100)  008093C0
                                 -> SleepConditionVariableCS(02EAED68, 02EAED40, 100)
                                    ... loop ...
               -> THIS SYSTEM: run the constructor
                  -> Phyre reflection registration       00632960 / 00630180 / 006388C0   (535 of 707)   <- corrected 2026-10-02, OPUS - these three are called by 336 of the 707 callers of 008092FC; 535 counts the whole Phyre.Reflection.* label family (the BJ-5 bounding below); the atexit 526 recounts exactly
                  -> atexit(destructor)                  00808B90                          (526 of 707)
               -> _Init_thread_footer(&guard)   0080929C
                  -> bump 01F44850, stamp the guard, _Init_thread_notify -> wake all
               (if the constructor throws)
               -> the guard's unwind funclet -> _Init_thread_abort(&guard)  0080926C
                  -> guard back to 0, wake all

process exit
  -> the atexit chain, reverse registration order  -- so the teardown order of lazy statics
     depends on the order the player caused them to be built
```

**Upstream (who causes this):** any of the 707 holder functions. Only 150 carry a V120
`PrimaryOwner` — **Resource 149, Platform/Online/Achievements 1** — and by mechanism class they
are Phyre 224, `NativeRoutine` 167, unclassified 150, `CompilerGeneratedCpp` 140, `Boundary` 10,
`ThirdParty` 10, and 6 others.

**Downstream (what this causes):** the Phyre reflection registry, and every consumer that reads a
type description — serialisation, resource binding, property lookup by name.

**Do not confuse with:**

- **The eager CRT initializer table.** 1,172 entries run before `main`, unconditionally, with no
  guard and no lock. Different mechanism, different failure mode, documented in
  [`../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md).
- **`CompilerGeneratedCpp.ThreadSafeStaticRecordAccessor` (117 functions).** That tag fires only
  when the accessor *is* the whole function. It is a true subset of the 707 — every one of the
  117 does hold a lazy static — but it is not the census, and reading it as one is the error
  section 12 of the sibling document records.
- **`std::call_once` / `InitOnceExecuteOnce`.** Not this. The guard is a plain `int` in `.data`
  and the protocol is entirely `_Init_thread_*`.

---

## 6. Modding notes

- **Best intervention point:** the holder function, entered *before* its guarded block, or the
  accessor's return value. Never inside the guarded region.

- **The rule that prevents the hang: never leave a guarded region by any path other than
  `_Init_thread_footer` or `_Init_thread_abort`.** Concretely, in a detour placed anywhere in one
  of the 707 holder functions:
  - do not return early from a point after the `_Init_thread_header` call;
  - do not `longjmp`, and do not let a C++ exception propagate out of your own code through that
    frame unless the compiler generated the guard's unwind funclet for it;
  - do not suspend or kill the thread while it holds a claim;
  - if you must bail out, bail out **before** the `call _Init_thread_header` site.

  Miss this and the guard stays `-1` permanently. Every later thread that touches the same static
  blocks in `_Init_thread_wait(100)` with no timeout escape~~, and because all 1,681 share the one~~
  ~~critical section at `02EAED40`, unrelated first-time initialisations queue up behind it~~. Unrelated first-time initialisations do not queue: the wait sleeps with `02EAED40` released *(corrected 2026-10-02, OPUS: `008093C0+0x4B` sleeps through `SleepConditionVariableCS`; the construction itself runs outside the lock, `008092FC+0x60`)*.

- **Diagnosing a suspected hang, without a debugger.** Read the guard ints in `.data`. Any guard
  sitting at `-1` while the game is stuck is the culprit; a `0` means never touched, ~~a positive~~ any other *(corrected 2026-10-02, OPUS: a built guard holds the epoch it completed at, negative as a signed int: `01F44850` ships `0x80000000` and the footer `0080929C` stores the incremented epoch)*
  value means built. This works from an external process, needs no patching, and is the fastest
  way to tell "stuck lazy static" apart from a deadlock elsewhere. The 1,545 guards that carry an
  unwind funclet are enumerable exactly — they are the rip-relative operands of the funclets
  listed in the sibling document.

- **Reading guards is also free telemetry.** A guard's value tells you whether a subsystem has
  ever come alive this session, and the *ordering* of the positive values (they are stamped from
  a monotonically increasing epoch at `01F44850`) tells you the exact order in which the engine
  first touched each one. That is a startup trace with no instrumentation at all.

- **Regenerates itself — do not write these.** Setting a guard to a positive value to "skip"
  initialisation makes the accessor hand out an object that was never constructed. Setting it to
  `0` while the object exists causes a second construction over the top of the first.

- **Breaks if:** you assume a lazy static exists because you saw it exist last run. It is built on
  first use, so whether it exists depends on what the player did. Any cached pointer taken at
  DLL-load time to one of these objects is reading zeroes.

- **XIIOnline.** This is the mechanism behind the project's standing rule that detours capture
  bounded POD facts and return. A detour that constructs its own C++ objects, takes a lock, or
  can throw, placed inside one of the 707 holders, inherits that function's one-time-init
  contract — and the failure is not a crash you can debug, it is a silent hang on a loading
  screen. 149 of the 150 owned holders are **Resource**-owned, which is exactly where a
  shared-world mod wants to hook.

- **Mod compatibility.** No authored data here. Two mods hooking different holders cannot
  interfere; two mods hooking the *same* holder can, because they serialise on the one lock.

---

## 7. What is not known

- [x] **BJ-1** — Which of the 1,681 statics are reached on a normal boot versus only in specific
  areas or menus. Requires runtime evidence; the static reading cannot answer it.
  *ANSWERED 2026-09-28 (FRONTIER ruling, carried residue): live-only by measurement; OPUS's
  NATIVE-REPLAY lower bound constructed 19, and the 1,662-guard residue is carried by
  `OPUS-REQ-ASTRA-BJ1-GUARD-SNAPSHOT`. See the register row.*
  **TESTED AND THE ROW IS RIGHT - 2026-09-16 (FABLE), now with a number instead of an assertion.** *Static reading cannot answer it* is the kind of claim I am supposed to attack, so I attacked it. It holds, and the measurement is worth more than the verdict. **The attempt.** A lazy static whose holder is not reachable from the process entry cannot be initialised on a normal boot - that *is* a static statement, and it would partition the population for free. Seeds: the PE `AddressOfEntryPoint` **`00808EE4`** plus **all 1,172 listed functions in the CRT static-initializer table `008C31D8`–`008C5678`**. **Why it fails.** Forward direct-call closure over those 1,173 roots reaches **2,397 of the 38,161 listed bodies - 6.3%**. The engine is driven overwhelmingly through **indirect** calls, so *unreachable in the direct graph* is the normal condition for **94% of the image** and carries almost no information. The partition it produces - **94 holders reachable, 613 not** - is therefore **dominated by the blind spot, and I am not publishing it as a finding.** **One thing the attempt does establish.** The population reproduces independently: the callers of `_Init_thread_header` `008092FC` number **exactly 707**, matching the figure filed by `repos-94`, so the holder set is confirmed by a second route. **And it names the instrument that would actually work.** The obstacle is indirect-call resolution - vtable and function-table binding - which is **the same blind spot `AR-5` ran into** (477 `call reg` sites, 11 indexed calls). **One instrument answers both questions.** Until it exists, boot reachability is not statically decidable here, and the row's *requires runtime evidence* stands. **Recorded as a dead route on purpose**, so the next reader does not spend the same day on it.
- [x] **BJ-2** — The identity of `01F44830`. It is the cookie the CRT uses for pointer encoding
  here and is read from ~~2,229~~ 2,216 functions *(corrected 2026-10-02, OPUS: `01F44830` has 2,216 reads in 2,216 functions and one write; BJ-2's answer below)*, but the count does not match the 5,372 functions that
  register `__GSHandlerCheck`, so calling it `__security_cookie` is unproven.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BJ-2):* **it is `__security_cookie`; one
  variable has both roles.** Three independent anchors:
  1. **The PE load configuration's `SecurityCookie` field holds `0x01F44830`.** Parsed with pefile. MSVC's `loadcfg`
     points that field at `__security_cookie` by construction, and the loader treats it as the `/GS` cookie.
  2. **Its only writer is `__security_init_cookie`** (`00809C1C`, which also writes the complement at `01F44838`), and
     `__security_check_cookie` compares against it (`00808C40`). The whole mechanism is read on the
     [image hardening page](../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md).
  3. **The reference census splits cleanly.** 2,216 functions reference it.
     - **2,208 are prologue loads** (`mov rax, [01F44830]`), and every one of those functions calls
       `__security_check_cookie`. That routine has 2,209 caller functions and 2,390 call sites; the one extra caller,
       `00808BC8`, is `__GSHandlerCheckCommon`, which checks a frame's cookie during exception unwinding and so has no
       load of its own.
     - **Five are CRT pointer-encoding sites**, which load the cookie and derive a rotate count from its low six bits:
       `_onexit` `00808B46`, `_Init_thread_notify` `00809376`, `_Init_thread_wait` `008093DC`, `00808988` and
       `00809124`. UCRT keys its pointer encoding with `__security_cookie`.
     - **The last three** are `__security_init_cookie`, `__security_check_cookie` and `__report_gsfailure`.

  **The 5,372 was the wrong comparison.** It counts unwind-data registrations of `__GSHandlerCheck`, a different
  population (this database bans unwind data as evidence of function identity). The cookie-check call census is the
  matching measure, and it matches exactly.
- [x] **BJ-3** — Whether the event fallback path in `_Init_thread_wait` is ever taken on a
  supported OS. `02EAED70` is initialised by the CRT~~, not visible statically~~ *(answered: see BJ-3's answer below, static, 2026-09-14; 2026-10-02, OPUS)*.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BJ-3):* **no. The fallback is chosen once at
  start-up, only when `kernel32.dll` lacks a condition-variable export, and every Windows this game can run on has them.**
  - **The decision.** `00809124` (the CRT's thread-safe-statics initialiser) first creates the lock `02EAED40`
    (`__vcrt_InitializeCriticalSectionEx`, spin 4000). It then takes `GetModuleHandleW(L"kernel32.dll")` and three
    `GetProcAddress` lookups: `InitializeConditionVariable`, `SleepConditionVariableCS` and `WakeAllConditionVariable`
    (`0080914E`–`00809190`).
    - **If all three resolve:** it clears `02EAED70` (`008091A8`), initialises the condition variable `02EAED68`, and
      stores the sleep and wake pointers encoded with `__security_cookie` in `02EAED78` / `02EAED80`.
    - **If any is missing:** it stores `CreateEventW(NULL, TRUE, FALSE, NULL)` in `02EAED70` (`00809218`–`0080921E`).
    - **If kernel32 or the event is unavailable:** `__scrt_fastfail(7)`.
  - **The use.** `_Init_thread_wait` takes the condition-variable path when `02EAED70` is 0 (`008093D3`): it decodes and
    calls `SleepConditionVariableCS(&02EAED68, &02EAED40, timeout)`. Only a non-zero handle sends it to the event path,
    which leaves the lock, calls `WaitForSingleObjectEx(event, timeout, FALSE)` and re-enters (`00809414`–`0080943C`).
  - **Why never.** All three exports exist in `kernel32.dll` from Windows Vista on (documented API availability, not
    observation), so on any 64-bit Windows the game supports, `02EAED70` stays 0 and the event path is unreachable.
- [x] ~~**BJ-4** — What type id `0x12` and the other `typeId` constants passed to `00632960` mean.~~
  **ANSWERED, and the premise was wrong: there is no type id.** The fifth argument is a byte
  offset, the sixth an attribute bitfield, and the type is a pointer. 682 field records over 173
  named classes recovered. See
  [`../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md).
- [x] **BJ-5** — The 107 holder functions that call neither a reflection routine nor `atexit`:
  what their lazy statics are.
  *Bounded 2026-09-22 (FABLE), not closed:* **16-byte `{tagged pointer, 0}` descriptor pairs,
  constructed inline** — 84 of the 107 call nothing external beyond the guard pair, all 269
  globals are in `.data`, and 63 of the 67 two-global holders write a pair exactly 8 bytes apart.
  **77 of the 107 are already this page's own families** (the entire 61-member
  `descriptor-pair-accessors`, plus 16 `magic-static-pair-initialisers`). **Residue: 30**, of which
  12 are still pair-shaped. See the section above.
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): the 30 are classified, so every one of the 107 has a kind.** The set was
  rebuilt from the image, and all five published figures came back as controls: 707 holders, 526 reaching `atexit`,
  535 reaching a `Phyre.Reflection.*` routine, a complement of 107, and 30 outside both families. Each of the 30 was
  classified from its own guarded initialiser:
  - **14 descriptor pairs**: two `.data` globals written exactly 8 bytes apart. The section above counted 12 with its
    own sweep; this script's criterion is any written pair.
  - **7 computed constant tables**, which call `cosf` / `sinf` / `powf`, and **1 computed float constant**
    (`00712910`, one `movss` store between the guard calls).
  - **5 cached singleton pointers**. Four keep the pointer the `Phyre::PTTYCallback` singleton `005CDA30` returns
    (vtable `00D360A0`); the fifth, a per-frame body, keeps a pointer 8 bytes into another lazily built object.
  - **2 lazily built named type records**. `006CCD80` builds `{name, 0, 0, 0}` for **`PCollisionGroup`**
    (`0069E790`) and **`PRigidBodyType`** (`0069E880`), and `006CCDA0` then fills each from a 15-entry table.
  - **1 empty guard** (`006FE7F0`): the header, the `-1` test, then the footer, with nothing initialised between.

  The classifier and its per-holder table are `members/bj5_residue.py` and `members/bj5-residue.tsv`. The five
  controls must pass before anything is classified, and none of the 30 is left as OTHER.

---

## `BJ-5` bounded — the 107 are inlined descriptor-pair accessors (FABLE, 2026-09-22)

**The set is reproduced before it is described.** Three figures this page published before the
sweep existed are used as controls, and all three come back exactly: **707** holders (functions
calling `_Init_thread_header` `008092FC`), **526** of them calling `atexit` `00808B90`, and **535**
calling a `Phyre.Reflection.*` routine. The complement is **107** — `BJ-5`'s set, reached
independently.

> *One definition had to be got right first.* “Calls a reflection routine” means **the whole
> `Phyre.Reflection.*` label family**, not the five top callees §4 tabulates: those five give 294
> and 486, and only the label family gives 535 and therefore 107.

### What they are (FABLE, 2026-09-22)

| | |
|---|--:|
| call **nothing external** beyond the guard pair | **84 of 107** |
| distinct globals they initialise | **269 — every one in `.data`, none in `.bss`** |
| write exactly 2 globals | 67, of which **63 are a pair EXACTLY 8 bytes apart** |
| write exactly 3 globals | 24, **all 24** containing an 8-byte-apart pair |
| body size | min 91 B, **median 115 B**, max 3,977 B |

**So the answer to “what their lazy statics are” is: 16-byte `{tagged pointer, 0}` descriptor
pairs, constructed inline.** That is why they call neither reflection nor `atexit` — *there is no
constructor call to make and no destructor to register.* The median 115 bytes is the same
**115-byte form** this page's own `members/descriptor-pair-accessors.tsv` header describes, whose
note ends *“init is inlined”*.

> **77 of the 107 are already families on this page**, which is the strongest form the answer
> takes: the **entire 61-member** `descriptor-pair-accessors` family is inside the 107, and 16 more
> are `magic-static-pair-initialisers`. *`BJ-5` was largely answered by this page's own member
> lists and nobody had intersected them.* The singleton-guard family overlaps **0**.

**Residue, and it is what keeps this bounded rather than closed: 30 holders in neither family.**
12 of those still write an 8-byte-apart pair, leaving roughly eighteen that are genuinely something
else — among them the largest bodies in the set and a handful calling `cosf` / `sinf` / `powf`,
which are computed constant tables rather than descriptor pairs. **Those eighteen are named by
address in the sweep and are the remaining work.**
*Done 2026-09-26 (FABLE, Claude Opus 5.5): all 30 are classified; see `BJ-5` in the box above and
`members/bj5-residue.tsv`.*

> **An instrument correction worth carrying, because it reversed a headline.** The call-set
> collector takes `jmp` as well as `call` — which is **required**, since some holders *tail-jump*
> to `atexit` and the 526 control only passes with it. But a `jmp` to a label **inside the holder's
> own body** is not a callee, and counting those made the set look as though 84 holders each called
> one routine. Excluding intra-body targets gives the opposite and stronger reading: **those 84
> call nothing external at all.**

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 1,732 guarded sites, 1,681 distinct guards, 707 functions | per-function disassembly of all 38,161 exact-current bodies from their own entry points; guard resolved from the `lea rcx,[rip+g]` immediately preceding each `call 008092FC`, 1,732 of 1,732 resolved, every one landing in `.data` | 1 |
| 19 guards are multi-site, always across different functions, accounting for 51 | grouping the 1,732 resolved guards by address | 1 |
| 1,545 guards carry an unwind funclet, 136 do not, zero orphans either way | intersection of the header-site guard set with the guard operands of the 1,545 `_Init_thread_abort` funclets | 1 |
| The guard protocol and the three CRT routines | complete exact-current bodies of `008092FC`, `0080929C`, `0080926C` | 1 |
| The gate expression | complete body of `FUN_00189CE0` and the minimal accessor `005C3B10` | 1 |
| `_Init_thread_wait` waits 100 ms via a condition variable, with an event fallback | complete body of `008093C0`; the decode `ROR64(cookie ^ slot, cookie & 0x3F)` read from the instruction stream | 1 |
| `0080926C` is `_Init_thread_abort` | Ghidra FunctionID single match, "Visual Studio 2015 Release", corroborated by the body matching the documented CRT semantics exactly | 1 + 6 |
| 526 of 707 holders call `atexit`; `00808B90` is `atexit` | call-site sweep of the 707 bodies; `00808B90` decompiles to `_onexit` forwarding | 1 |
| 535 of 707 call a `Phyre.Reflection.*` routine | call-site sweep of the 707 bodies against the current classification | 1 + 11 |
| `00632960` builds a `Phyre::PClassDataMember` | complete body; writes `Phyre::PClassDataMember::vftable` into the record | 1 + 4 |
| Field names are authored strings in the holder bodies | rip-relative operands resolved to NUL-terminated ASCII in `.rdata`; 347 of 707 holders, 890 distinct strings | 2 |
| The type-name hash `h = h*0x21 + (c & 0x1F)`, seed `0x7B5` | complete body of `006388C0` | 1 |
| Holder ownership: 149 Resource, 1 Platform | V120 `PrimaryOwner` tags of the 707 | 11 |

### The killer observation, and what happened when it was sought

**The claim most likely to be false is the census itself** — 1,681 objects at 1,732 sites. The
killer: a guarded construction that the sweep never sees, or a guard the sweep invents.

Sought two ways, both of which could only have refuted it:

1. **Completeness.** If the `lea rcx,[rip+g]` back-scan failed on any site, the guard count would
   be an undercount of unknown size. It resolved **1,732 of 1,732**, every result landing in
   `.data`, with none falling in `.rdata`, `.text` or outside a section — a wrong scan would
   produce out-of-section garbage, and produced none.
2. **Independent closure.** The 1,545 guards recovered from the exception funclets were derived
   from *completely different bodies*, in a different part of the binary, by a different pass.
   Every one of them is in the header-site set, and none is missing. **Zero orphans in either
   direction.** If the sweep had missed sites, funclet guards would have had nowhere to land.

Neither broke it. What *did* break was a coarser earlier statement — see below.

### Superseded readings

**Corrected before publication: 1,732 is the site count, not the object count.** The first
measurement in this line of work reported "1,732 lazily-initialised statics" and, by subtraction,
"187 without a funclet". Resolving the guard operand at each site shows 1,681 distinct objects and
136 without a funclet. The error was reachable because the site count arrived first and one site
was read as one object. Recorded here and in the exception-funclet document's §8.

**Corrected in the sibling document: 117 is a tag population.** See section 12 of
[`../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md).
All 117 functions tagged `ThreadSafeStaticRecordAccessor` do hold a lazy static — the tag fires
only when the accessor is the whole function — so it is a true subset of the 707, not a wrong
label. It is simply not a census.

---

## 9. Related

- [`../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md) —
  the eager path, the `atexit` teardown chain this feeds, and the corrected lazy count.
- [`../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`](../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md) —
  the 1,545 unwind funclets that release a guard when a constructor throws.
- [`../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md) —
  `_guard_check_icall`, which `_Init_thread_wait` calls before its decoded indirect call.
- [`../../22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md`](../../22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md) —
  the middleware whose reflection metadata is three quarters of what these statics build.
- [`../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) —
  the class descriptors these registrations populate.
- [`../README.md`](../README.md) — category index.

---

## 10. Falsification pass — 2026-09-02

Against snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`.

**Attacked: the census.** *Killer:* an unresolved or out-of-section guard, or a funclet guard with
no matching header site. Result: **survived** — 1,732/1,732 resolved, all in `.data`, and the
1,545 funclet guards reconcile with zero orphans in either direction. Recorded in §8.

**Attacked: "1,732 objects."** *Killer:* a guard appearing at two sites. Result: **broke**, and
this is why the document says 1,681. Nineteen guards are multi-site, accounting for exactly the 51
difference. Corrected before publication rather than after.

**Attacked: "these are mostly Phyre reflection."** *Killer:* the reflection callees being a
minority. Result: **survived but is bounded** — 535 of 707 (75.7 %) call a `Phyre.Reflection.*`
routine, and the classification of those callees is itself tier 11. The claim is stated as a
measured fraction with its instrument named, not as "these are reflection objects". The 107
holders that call neither reflection nor `atexit` are filed as BJ-5 rather than glossed.

**Attacked: "all 1,681 share one lock."** *Killer:* a second critical section in any of the three
routines. Result: **survived** — `_Init_thread_header`, `_Init_thread_footer` and
`_Init_thread_abort` each reference `02EAED40` and nothing else, and `_Init_thread_wait` releases
and retakes that same address on its fallback path.

**Attacked: "the timeout is 100 ms."** *Killer:* a call site passing something else. Result:
**survived** — `_Init_thread_wait` is called from one place, `_Init_thread_header`, with the
literal `100`. ~~Two functions call it in total~~ One function calls it, at one site *(corrected 2026-10-02, OPUS: the only edge into `008093C0` is `008092FC+0x25`, and no data reference names it)* (`008093C0` has 1 caller by edge count), consistent
with a single site.

**Attacked: the hang itself.** *Killer:* a timeout, a retry limit, or any other path that clears a
`-1` guard. Result: **survived, and this is the load-bearing claim.** `_Init_thread_header`'s loop
has no iteration bound and no timeout branch; `_Init_thread_wait`'s return value is discarded by
its only caller, so a wait that times out simply loops. The only writers of a `-1` guard in the
entire binary are `_Init_thread_footer` (to a positive epoch) and `_Init_thread_abort` (to zero).

**Re-checked for banned evidence.** No `.pdata`, `.xdata`, unwind record or EH map appears in any
claim here. The link to the unwind funclets cites their *bodies*, and the 1,545/136 split is an
intersection of two body-derived sets.

**Not attempted, and therefore not claimed:** any runtime observation. Nothing here has been seen
to execute; the hang is derived from the control flow, not witnessed. BJ-1 ~~and BJ-3 both need~~ needs a *(answered: see BJ-3 above, answered statically 2026-09-14; 2026-10-02, OPUS)*
live process, and a runtime pass would materially strengthen §1 and §6.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Presentation — CLIENT.** `005AD8F0` names its members with animation strings (`m_animationSet`,
`m_animationClips`, `m_animationWeightedBlenderController`) and holds 28 lazy statics. It is called by a 920-byte
Presentation-filed body, which fits those animation member strings.

## Interior citation — frontier hub `005CD820` (2026-09-17, SWE2-EC7)

`005CD820` — 32 B, 41 frontier callers at census (55 total callers spanning CRT, Audio,
Input, ResourceDataLoading, Presentation and Phyre bands — a shared runtime lock, not a
subsystem leaf). Interior verified: [`005CD82A`](../../_index/ADDRESS-INDEX.md) is
`lock cmpxchg [rcx+0x20], edx` with `eax=1`/`edx=0` — a spin-lock **release**: decrement
`[rcx+0x24]` (hold depth), clear the lock flag atomically, then when `dword[rcx+0x18] > 0`
tail-jumps `005CD570(rcx+8)` to wake the delegated waiters. The unlock half of the
~~one-time-init /~~ shared-lock pair, which is not the one-time-init lock this page documents *(corrected 2026-10-02, OPUS: `005CD820` clears a `lock cmpxchg` flag at `[rcx+0x20]` and wakes through `005CD570` (`SetEvent`); it never touches `_Init_thread_lock` `02EAED40`)*.

**Audio — CLIENT (11 edges).** `005CD820` is called by eleven Audio-tagged bodies
(`00212050`/`002120E0`/`00212300`/`00219C40` and seven more in `0021xxxx`); the crossing is that
the layer uses the shared lock release, not that the lock is an Audio mechanism.
**Input — CLIENT (2 edges).** `0079C140`/`007A0340` call `005CD820` — same relationship class.
Edge counts and caller list from `edges.tsv`; bodies read from the shipping image 2026-09-17.

NOT claimed: `005CD570`'s dispatch target list (a computed call into the wake path, not read
here) or the lock object's owner type.


### Interior citation — frontier hub `002124C0` (2026-09-18, SWE2-EC7)

`002124C0` — 219 B, 17 callers (the `0019xxxx`/`0021xxxx` registration cluster
above). Read from the shipping image: `byte[rcx+0xB8]` selects the locking arm —
when set, `005CD4F0(rcx + 0x90)` acquires the one-time-init lock at
[`002124E5`](../../_index/ADDRESS-INDEX.md) before the body walks the
`[rdi+0x70]`/`[rdi+0x60]` region. The conditional-lock wrapper the registration
stubs call through.
## SWE2-EC7-47 update (2026-09-19) - `00212300`

`00212300` (221 B) is a `0021xxxx` init-lock family body - `002124C0`/`005CD4F0`/`005CD820` plus a `call [rax+0x18]` vcall. Interior anchor `00212333` (a `002124C0` call).

## SWE2-EC7-49 update (2026-09-19) - `008AADA0`

`008AADA0` (197 B) is a body - `005CDA30`/`0080929C`/`008092FC`. Interior anchor `008AADED` (a `005CDA30` call).


## SWE2-EC7-64 update (2026-09-19) - `00212050`

`00212050` (138 B) is a `0021xxxx` lazy-init-family body - `0017D940`/`0017D960`/`00212260`/`002124C0`/`005CD4F0`/`005CD820` plus one vcall. Interior anchor `00212071` (a `0017D940` call).



## SWE2-EC7-65 update (2026-09-19) - `00212260`

`00212260` (150 B) is a `0021xxxx` lazy-init-family sibling - `00221770`/`00597970`/`00598100`/`0059BD40`/`0059F4A0`. Interior anchor `00212289` (a `00597970` call).


## SWE2-EC7-108 update (2026-09-20) - `00221770` measured

`00221770` (8 B) is the indexed
thunk `00212260`, `00224DC0` and
`00225030` reach: `movsxd rcx,
ecx` then `jmp 00210EC0` - the
sign-extended one-argument forward
into the runtime's indexed slot
the lazy-init registrations use.
Interior anchor `00221773` (the
`jmp 00210EC0`).

## SWE2-EC7-114 update (2026-09-21) - `007A3BD0` / `0079F0F0` measured

`007A3BD0` (17 B) is the
`+0x30`-object forwarder
`00798FF0`, `007A0340`,
`007A03D0` and `007A04F0`
call: a live `qword[+0x30]`
tail-jumps its
`vtable[+0x28]`, a null one
returns - the mode object
`007A3D70` selects, invoked.
Interior anchor `007A3BDC`
(the `+0x28` vtable jump).

`0079F0F0` (79 B) is the
paired dispatch `0079C140`
runs: a nonzero `cl` takes
the IAT import `008C2928` on
`02EA5248` with `edx = 9`, a
zero takes `edx = 6`, then
both arms tail-jump
`005CDAA0(2, 01CB3230)` /
`(2, 01CB3248)` - the two
`FocusScale*` labels at
`01CB3230`/`01CB3248` fed
one switch.
Interior anchor `0079F104`
(the `edx = 9` arm call).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**~~The one-time-init lock~~ The `005CD4F0` / `005CD820` shared lock is a service every layer takes, SERVICE throughout.** *(corrected 2026-10-02, OPUS: this pair is a `lock cmpxchg` flag lock with an event wake; the one-time-init lock `02EAED40` is referenced only by `00809124`, `00809244`, `0080926C`, `0080929C`, `008092FC` and `008093C0`)* Its acquire `005CD4F0` and release
`005CD820` are called by:
- **Resource, 42:** the queue and registration bodies `001A0A90`, `001A0BB0`, `001A0C50`, `001A1240` and more;
- **Audio, 22:** `00212050`, `002120E0`, `00212300`, `00219C40` and the rest of the `0021xxxx` cluster;
- **Input, 4:** `0079C140`, `007A0340`;
- **Platform, 2:** `0019CC50`.

**Resource, 105, and Audio, 44: the lazy-init family.**
- The `0021xxxx` bodies `00212050`, `00212260` and `002124C0` (17 callers, among them `001B4D70`, `0020B840`,
  `0020BFA0` and `001B1960`) call the Phyre serialisers `00597970`-`0059F4A0` and the one-argument `malloc` thunk
  `00221770` (via `00224DC0`, `00225030`).
- `0017D940` / `0017D960` are reached from `00212050`.

The lock and the guard are this page's; what each lazily built object is belongs to its owner.

**Input, 7; Platform, 4; PlatformOnlineAchievements, 1; Save_Load_Settings, 1; CoreRuntimeScheduling, 1 —
MECHANICAL.**
- `0079C140` calls `0079D010` / `0079D920` and `0079F0F0`.
- The `+0x30` forwarder `00798FF0` reaches `0019A510`, `0079E700`, `007A0810` and `GameSettingConfig_WriteFile`.
- `007A3BD0` / `007A3D70` are called from `007A0340` / `0079E520`.
- `00189CE0` (the magic-static example) is reached from the frame step `0017D6E0`.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 slice OPUS-P22-SLICE-24-99).*

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-lazy-statics-and-the-one-time-init-lock-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `001D9F70` | 23 B | `0017D940` + 0x17 | returns without a write when `edx` is above 1 (unsigned); otherwise atomically adds 1 (`lock xadd`) to dword `rcx+0x24` + sign-extended `edx` * 4 and returns that dword's previous value | Interior anchor `001D9F73`; Interior anchor `001D9F78`; Interior anchor `001D9F7C` |
