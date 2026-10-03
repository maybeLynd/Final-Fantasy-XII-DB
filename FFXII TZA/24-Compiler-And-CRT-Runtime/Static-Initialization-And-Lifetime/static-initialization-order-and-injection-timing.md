---
system: Static initialization order and injection timing
category: 24-Compiler-And-CRT-Runtime
status: AUDITED
owner_layer: CodeDomain:CompilerGeneratedCpp + Runtime.StaticLifetimeInfrastructure
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
  passes: 5
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 1
---

# Static initialization order and injection timing

> **1,172 pieces of global state are built before `main` runs, and 1,681 more are built lazily the
> first time anything touches them.** If you inject into FFXII, this page tells you what exists
> when.

## 1. What the player sees

Nothing — this all happens in the seconds between double-clicking the game and the logo
appearing.

But it is the reason a mod can behave differently depending on *when* it loads. Inject too early
and the engine's global tables are not built yet; the mod reads zeroes and either does nothing or
crashes. Inject after the game is running and everything is in place. Mods that "only work if you
attach after the title screen" are usually running into exactly this.

## 2. Native mechanism

### The eager path: 1,172 initializers before `main`

The CRT walks a table of function pointers at startup. In this binary it is a contiguous run of
`.text` addresses in `.rdata`:

```
CRT initializer table
   start   VA 0x008C31D8
   end     VA 0x008C5678
   entries 1,172
   first   0x808D5C, 0x16A290, 0x16A29C, 0x15BC40, 0x15BCD0, 0x15BCF0, ...
   last    ..., 0x16D5A0, 0x16D5B0, 0x16D610
```

It sits immediately after the two CFG guard pointers at `0x8C31C0` / `0x8C31C8`.

Each entry is a generated function with one of a few shapes.

**Construct-and-register** — by far the most common, and the shape the Phyre class descriptors
use:

```c
void FUN_0015bcd0(void)
{
    FUN_005cc8a0(&DAT_01f7f510);     // construct the global in place
    atexit(FUN_008a6990);            // register its destructor
    return;
}

void FUN_0015c540(void)
{
    FUN_001fe8b0(&DAT_01f813c8);
    atexit(FUN_008a69e0);
    return;
}
```

**Prototype copy** — `Runtime.StaticLifetimeInfrastructure`. Instead of running a constructor,
the initializer bulk-copies a compile-time prototype from one part of `.data` into the live
global:

```c
void FUN_0015bd30(void)
{
    _DAT_01f80130       = _DAT_01df09c0;      // copy from an authored prototype
    uRam...01f80138     = uRam...01df09c8;
    _DAT_01f80140       = _DAT_01df09d0;
    ...                                        // continues for hundreds of bytes
}
```

Source `0x01DF09C0` sits ~~at the very start of `.data`~~ `0x9C0` bytes into `.data`, which starts at `0x01DF0000` *(corrected 2026-10-02, OPUS: section table; `01DF0900`–`01DF09B0` are read by other code, among them the sibling prototype copies `0015BF20` and `0015C0D0`)*; the destination `0x01F80130` is the live
object. **The initial value of these globals is authored data compiled into the image**, not
something computed at runtime — which means it can be found and edited statically.

### The lazy path: 1,681 thread-safe function-local statics

> **Corrected 2026-09-02 (section 12).** This section said **117**. That is the size of the
> `CompilerGeneratedCpp.ThreadSafeStaticRecordAccessor` tag population, not a count of magic
> statics. Counting the mechanism gives **1,681 distinct statics at 1,732 guarded construction
> sites across 707 functions.** The shape below is unchanged and correct.

MSVC's C++11 "magic static". The 117 functions carrying the
`CompilerGeneratedCpp.ThreadSafeStaticRecordAccessor` tag are exactly those whose *entire body*
is one accessor, and all 117 do contain a guarded construction — the tag is a true subset, not a
wrong label. The other 590 holder functions carry a different tag because the magic static sits
inside a larger function: Phyre 224, `NativeRoutine` 167, no `CodeDomain` tag at all 150,
`CompilerGeneratedCpp` 140, and 26 others. All 707 share one shape:

```c
undefined * FUN_005c3b10(void)
{
    if (*(int *)(*(longlong *)((longlong)ThreadLocalStoragePointer
                               + (ulonglong)_tls_index * 8) + 4) < <epoch>) {
        ...                                    // guarded one-time construction
    }
    return &DAT_02cb5d48;                      // the static's address
}
```

The read is `_Init_thread_epoch`, a **TLS variable at offset `+4`** in this module's TLS block,
compared against ~~a global initialization epoch~~ the static's own guard dword, which holds the epoch at which that static completed *(corrected 2026-10-02, OPUS: at the gate in `00189CE0`, `00189CE0+0x5D` is `cmp dword ptr [01F7F5C8], eax` with `eax` this thread's `[tls+4]`, and `00189CE0+0x63` `jle` skips `_Init_thread_header`; the global `01F44850` is read only inside the header and the footer; the T-5 answer of 2026-09-14)*. If this thread has not yet observed the
initialization, the guarded construction runs (through `_Init_thread_header` /
`_Init_thread_footer`); otherwise the accessor returns the address immediately.

**These 1,681 globals do not exist until something calls their accessor.** They are built on
first use, not at startup. What they mostly *are* — Phyre's own reflection metadata — and the
full hazard they create for an injected DLL are documented separately in
[`../Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md`](../Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md).

### TLS: storage yes, callbacks no

The TLS directory is present and live, but carries **no callbacks**:

```
TLS directory @ rva 0x01BCBED8, size 40
    RawDataStart       = 0x03004000
    RawDataEnd         = 0x03004008        (8 bytes of TLS data)
    AddressOfIndex     = 0x02EAED3C
    AddressOfCallBacks = 0x008C56B0        -> array is null-terminated immediately
    ZeroFill           = 0
    Characteristics    = 0x00300000
    callbacks: 0
```

This distinction is easy to get wrong and matters: the binary **uses TLS storage** (`_tls_index`,
`_Init_thread_epoch` — the magic statics above depend on it) while registering **zero TLS
callbacks**. Nothing in this image runs before `main` by that route.

### Teardown

Destruction is the mirror image, through `atexit`, in reverse registration order:

| Family | Count | Role |
|---|---|---|
| `CompilerGeneratedCpp.StaticObjectInitializer` | 90 | construct + `atexit` |
| `CompilerGeneratedCpp.ThreadSafeStaticObjectInitializer` | 23 | guarded lazy construct |
| `CompilerGeneratedCpp.ThreadSafeStaticRecordAccessor` | 117 | magic-static accessor — **tag population only**; 707 functions actually hold one |
| `CompilerGeneratedCpp.StaticZeroInitObjectInitializer` | 11 | zero-init |
| `Runtime.StaticLifetimeInfrastructure` | 145 | prototype copy |
| `Runtime.StaticIntrusiveListTeardown` | 224 | list teardown at exit |
| `CompilerGeneratedCpp.StaticContainerTeardown` | 60 | container teardown |
| `CompilerGeneratedCpp.GuardedStaticObjectTeardown` | 28 | guarded teardown |

Plus the 372 `ClassDescriptorStaticTeardown` and 830 `DataMemberMetadataStaticTeardown` entries
belonging to Phyre reflection, all reached the same way.

## 3. Key addresses

| Address | Role | Verified |
|---|---|---|
| `0x008C31D8` – `0x008C5678` | CRT initializer table, 1,172 entries | ✅ parsed from `.rdata` |
| `0x0015BCD0` / `0x0015C540` | construct-and-`atexit` initializers | ✅ read |
| `0x0015BD30` / `0x0015BF20` | prototype-copy initializers | ✅ read |
| `0x005C3B10` / `0x005C3B90` / `0x005A6670` / `0x005CDA30` | magic-static accessors | ✅ read |
| `0x008B0E20` / `0x008B0E40` | guarded static teardown | ✅ read |
| `0x01CEBED8` | TLS directory (**corrected 2026-09-02** — `0x01BCBED8` is its RVA, not its VA) | ✅ parsed |
| `0x008C56B0` | TLS callback array — empty | ✅ parsed |
| `0x02EAED3C` | `_tls_index` | — |
| `0x03004000` | TLS raw data (8 bytes) | — |
| `0x01DF09C0` | a static prototype in `.data` | — |

## 4. Data structures and formulas

```
CRT initializer table          contiguous QWORD VAs in .rdata
  base   = 0x008C31D8
  count  = 1172
  stride = 8
  entry[i] -> void (*)(void)

IMAGE_TLS_DIRECTORY64  @ rva 0x01BCBED8
  +0x00   u64   RawDataStart        = 0x03004000
  +0x08   u64   RawDataEnd          = 0x03004008
  +0x10   u64   AddressOfIndex      = 0x02EAED3C
  +0x18   u64   AddressOfCallBacks  = 0x008C56B0   (empty array)
  +0x20   u32   SizeOfZeroFill      = 0
  +0x24   u32   Characteristics     = 0x00300000

TLS block (per thread)
  +0x04   i32   _Init_thread_epoch
```

**Magic-static guard** (the exact test, compiled at all **1,732** guarded construction sites):

```
tlsBlock = ThreadLocalStoragePointer[_tls_index]
if (tlsBlock[+4] < epoch):            // _Init_thread_epoch   <- corrected 2026-10-02, OPUS - the comparand is the static's own guard dword, not a global epoch: 00189CE0+0x5D cmp [guard], eax (thread epoch); 00189CE0+0x63 jle skips the header
    guarded one-time construction     // _Init_thread_header / _Init_thread_footer
return &theStatic
```

**Startup order:**

```
for i in 0 .. 1171:                   // eager, in table order
    initTable[i]()
main()
                                      // lazy, on first access
accessor() -> guard -> construct once
                                      // exit, reverse registration order
atexit chain
```

## 5. Call chain

```
process start
  -> Windows loader (no TLS callbacks to run)
  -> CRT startup
     -> walk 1,172 initializers at 0x008C31D8
        -> construct global + atexit(destructor)      (90 + Phyre's 227)
        -> copy authored prototype from .data          (145)
        -> zero-init                                    (11)
  -> main
     -> engine runs
        -> first touch of a function-local static
           -> magic-static accessor        (1,732 sites, 1,681 objects, 707 functions)
              -> _Init_thread_epoch check
              -> guarded construction, once

process exit
  -> atexit chain, reverse order
     -> StaticIntrusiveListTeardown (224), container teardown (60),
        guarded teardown (28), Phyre descriptor teardown (372 + 830)
```

**Upstream:** the Windows loader and the CRT.
**Downstream:** every global the engine owns — including all Phyre class descriptors.

**Do not confuse with:** TLS *callbacks* and TLS *storage*. This image has the second and not the
first.

## 6. Modding notes

- **Inject after `main`, not before.** 1,172 initializers must run before any engine global is
  valid. A DLL loaded by an import-table or TLS-callback trick sees uninitialized memory.
- **There are no TLS callbacks to piggyback on** — but there is also nothing occupying that slot,
  so adding one is available as an injection point *if* you accept running before all engine
  state exists.
- **1,681 globals do not exist until first use.** Reading one of those addresses directly,
  without going through its accessor, can read a zeroed object even long after startup. Call the
  accessor.
- **Initial values of many globals are authored bytes in `.data`.** The prototype-copy
  initializers mean a static's starting state can be found and patched in the file, before any
  code runs.
- **Teardown is `atexit`, reverse order.** A mod that unloads late can find engine globals already
  destroyed.
- **XIIOnline:** this is the concrete answer to "when is it safe to touch engine state?" — after
  the CRT initializer table has run. Anything the injected DLL caches at load time about engine
  globals is suspect unless it can prove startup finished. The 1,681 lazy statics are the
  sharper trap: they can be valid on one run and not another depending on what the player did
  first — and a detour that abandons one mid-construction hangs the process outright, which is
  the subject of
  [`../Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md`](../Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md).

## 7. What is not known

- [x] ~~Where the C / C++ boundary falls inside the 1,172-entry run.~~ **ANSWERED — the question's
      premise was wrong.** There is no boundary inside the run: the C table (`__xi`, 3 entries,
      `008C5680`–`008C56A0`, `_initterm_e`) and the C++ table (`__xc`, 1,172 entries,
      `008C31D0`–`008C5678`, `_initterm`) are separate. **The whole run is C++.** Section 10. **T-1.**
- [x] ~~Which of the 1,172 entries belong to Phyre vs the game vs third-party libraries.~~
      **ANSWERED** — `Input` **325 (27.7 %)**, `Phyre` 317, `Runtime` 279, `CompilerGeneratedCpp`
      101, `NativeRoutine` 62, `EASTL` 58, `Platform` 19, others 10. Section 10. **T-2.**
- [x] Whether the initializer *counts* above track startup *cost*. One initializer that builds a
      large table outweighs fifty pointer assignments. **T-6.** *(status restated in the register 2026-09-26, FABLE, Claude Opus 5.5: see the row; box ticked in a follow-up)*
- [x] ~~What the 145 prototype-copy initializers are copying — which globals get authored starting
      state.~~ **ANSWERED** — **320 bytes** of prototype stamped into **6,692 bytes** across 5
      `.data` clusters, **all owned by `Input` or `Audio`**; no documented gameplay global receives
      any. The count is also wrong: **149** functions carry the tag, **96** of them are CRT entries.
      Section 11. **T-3.**
- [x] ~~Whether `00195DF0` copies from the 1,108-byte cluster at `01DF15DC` into the live binding
      table.~~ **ANSWERED — it is a staging buffer.** Profiles are assembled at `01DF1738 + i*0x15C`
      from authored records at `0x01F80F90`, then copied into the live table at `0x01F80130`.
      **T-7.**
- [x] What the two `Audio` prototype-copy clusters at `02EAD018` (2,040 B) and `02EADC20` (656 B)
      hold. 795 references across 202 functions. **T-8.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (T-8):* **SQEX Sead's static pools — the
      audio driver's object lists and action queues.** Every `lea vtable ; mov [global], reg` pair that lands in either
      cluster names its object by MSVC RTTI. Each pair sits in a static-teardown thunk in `008B86A0`–`008B8FD0`, which
      resets the vtable as the object dies. The objects:

      | object | class (`SQEX::Sd::…`) | thunk |
      |---|---|---|
      | `02EAD040` | `FixedQueue<Driver::ACTION*>` | `008B86A0` |
      | `02EAD2A0` | `FixedList<Driver::Core::CoreSourceVoice*>` | `008B8850` |
      | `02EAD2D0` | `FixedList<Driver::Core::CoreSubmixVoice*>` | `008B88D0` |
      | `02EAD300` | `List<Driver::Core::CoreSourceVoice*>` | `008B87B0` |
      | `02EAD490` | `FixedList<Driver::StreamingBank*>` | `008B89A0` |
      | `02EAD540`, `02EAD570` | `FixedList<Driver::Sound*>` (two) | `008B8AB0`, `008B8A10` |
      | `02EAD600` | `FixedList<Driver::Sequence*>` | `008B8B30` |
      | `02EAD690` | `FixedList<Driver::Track*>` | `008B8BB0` |
      | `02EAD720` | `FixedList<Driver::Voice*>` | `008B8C20` |
      | `02EAD7E0` | `FixedList<Driver::Event*>` | `008B8CD0` |
      | `02EADCD0` | `FixedList<Magi::Instrument*>` | `008B8E40` |
      | `02EADD70`, `02EADDA0` | `FixedQueue<Lay::ACTION*>` (two) | `008B8F40`, `008B8EC0` |
      | `02EADE80` | `FixedList<Lay::SoundObject*>` | `008B8FD0` |

      So `02EAD018` is the `Sd::Driver` layer's pools, and `02EADC20` the `Magi` (music) and `Lay` (spatial) layers'.
      The busiest referencing functions sit in Sead's driver code: `007B31A0` has 50 references into the first cluster,
      `007BAEC0` has 19 into the second, and the top eight of each fall in `007AB5C0`–`007BC4F0`. **Not established:** that
      the prototype copies are these containers' header initialisation (only the object identities were read), each
      container's capacity, and the unnamed fields between the objects listed.
- [x] Whether initialization order between translation units is relied upon anywhere. **T-4.** *(closed — the register row is WITHDRAWN.)*
      *Bounded 2026-09-22 (FABLE), not closed:* a direct-only sweep of all **1,172** initializers
      finds **8** globals shared between distinct initializers, and **every one** is either
      intra-translation-unit (nine bodies contiguous in both `.text` and the table) or read by an
      initializer that runs **before** its writer. **No cross-TU reliance found; absence not
      proven**, because the sweep reads no callees. See the section above.
- [x] The global epoch value each magic-static accessor compares against. **T-5.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (T-5):* **there is no single value; the premise
      is off by one level.**
      - **What an accessor compares.** Each accessor compares **its own guard dword** with **this thread's**
        `_Init_thread_epoch`, and takes the slow path when the guard is greater. Example: `00630180`, `cmp [02CF950C], eax ;
        jg`, with `eax` = TLS block `+4`. The TLS template (`.tls` raw data `03004000`) holds `0x80000000` at `+4`, so a thread
        starts at `INT_MIN`.
      - **The global.** The only global involved is `_Init_global_epoch` `01F44850`. It ships as `0x80000000` and is
        advanced only by `_Init_thread_footer` (`0080929C`: `inc eax` at `008092C5`, stored at `008092C7`). The footer
        stamps the new value into the finished guard (`008092CD`) and into the constructing thread's epoch (`008092E8`).
      - **A guard's life.** It is **0** before construction and **−1** while one thread constructs.
        `_Init_thread_header` (`008092FC`) sets −1 under the lock `02EAED40` (`EnterCriticalSection`). A second thread
        seeing −1 waits in `_Init_thread_wait` (`008093C0`, 100 ms) and re-tests. A thread seeing a finished guard copies
        the global into its own epoch (`00809346`–`0080934C`) and skips.
      - **The value itself.** A finished guard holds the global's value at the moment it completed, so the number is
        construction order across the whole process. It is a runtime value, not a constant any accessor carries.
      
      Addresses and the full pseudo-code are in
      [exception funclets and lazy static guards](../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 1,172 CRT initializer entries at `0x008C31D8` | contiguous `.text`-range QWORD scan in `.rdata`, anchored on three known initializer VAs | 1 |
| Construct-and-`atexit` is the dominant shape | complete bodies of `0015BCD0`, `0015C540` | 1 |
| Prototype-copy initializers exist | complete body of `0015BD30` — bulk `.data` → `.data` copy | 1 |
| Magic statics use `_Init_thread_epoch` at TLS `+4` | four accessor bodies, all identical in shape | 1 |
| Zero TLS callbacks | `AddressOfCallBacks = 0x008C56B0`, array null-terminated at index 0 | 1 |
| TLS storage *is* used | `_tls_index` dereferenced in every magic-static accessor | 1 |
| Family counts | GFZ `CodeDomain` tag census | 3 |

**Anchoring, not guessing.** The initializer table was located by searching `.rdata` for the
absolute VAs of three functions already proven to be static initializers by reading their bodies
(`0015BCD0` and the Phyre descriptor initializers `001603E0` / `00160420` / `00160480`). All three
were found, 8 bytes apart, inside one contiguous run. The count follows from walking that run to
its ends. It was not read off a symbol or assumed from a section name.

**The stated limit of that method.** The walk stops where the pointers stop looking like `.text`
addresses, which cannot distinguish `__xi` from `__xc` if the linker placed them adjacently with
no null between. 1,172 is therefore "contiguous initializer entries containing the known
initializers", ~~which may span both C and C++ tables~~ *(answered: see §10 - the entire 1,172-entry run is C++, and `__xi` is the separate table at `008C5680`; 2026-10-02, OPUS)*. Recorded as **T-1** rather than reported as
a clean `__xc` count.

### Two open questions closed this pass

**S-4 — TLS callbacks: ANSWERED. There are none.** The callback array at `0x008C56B0` is
null-terminated at index 0. Nothing in this image runs before `main` via TLS.

**S-1 — `.gfids` contents: ANSWERED, with a caveat.** The section is not zero padding, but it is
also not a guard function table. All 512 bytes were dumped; exactly 12 dwords are nonzero and all
sit in the first `0x30` bytes:

```
+0x000  0x31 (49)   +0x004  0x30 (48)   +0x008  0x13 (19)   +0x00c  0x0a (10)
+0x010  0x0d (13)   +0x014  0x10 (16)   +0x018  0x45 (69)   +0x01c  0x71 (113)
+0x020  0x0a (10)   +0x024  0x62 (98)   +0x028  0x37 (55)   +0x02c  0x0b (11)
```

Every value is between 10 and 113 — **far below `0x1000`, the lowest possible code RVA in this
image**, so none of them can be a function RVA. The section contains no usable guard table, which
independently corroborates `GuardCFFunctionTable = 0` from the load config by a completely
separate route.

What those 12 dwords *are* is a new question, recorded as **T-9**, and it ~~is deliberately left~~ was left *(answered: see T-9 on the hardening page, answered 2026-09-27 - the statically linked runtime's own `.gfids$y` data; 2026-10-02, OPUS)*
open rather than guessed. The claim proven here is the negative one, and it is the one the
hardening document needed.

> **`T-9` narrowed 2026-09-14 (FABLE), not answered: the best-supported model is object-file symbol indices that were
> never converted.**
> - **The format.** A compiler building with `/guard:cf` emits, per object, a `.gfids$y` section: a list of 32-bit
>   indices into **that object's own COFF symbol table**, one per address-taken function. The linker turns them into
>   image RVAs for `GuardCFFunctionTable` only when it runs the guard pass. (LLVM `lld-link` implements the same
>   format, which is where this is documented outside Microsoft.)
> - **Why the 12 dwords fit it.**
>   - Every value is a small integer (10–113), as object-local symbol indices are.
>   - The value 10 occurs twice (`+0x00C`, `+0x020`). One object lists a symbol once, so the section is the
>     concatenation of **at least two** objects' lists. A grouped-section merge would produce exactly that.
>   - The load config says the guard pass did not run: `GuardCFFunctionTable = 0`, `GuardCFFunctionCount = 0`,
>     `GuardAddressTakenIatEntryTable = 0` and `GuardLongJumpTargetTable = 0` (read with pefile, directory size
>     `0x94`). So indices that reached the image would have stayed unconverted.
> - **The neighbouring `.rodata` section is a different source, and is not evidence for this.** The section before
>   `.gfids` is **`.rodata`** (`0x03001000`, `0x11C0` bytes), a name the MSVC compiler does not emit. Every rip-relative
>   reference into it comes from the hand-written SIMD window `00121000`–`00160000` (`tools/ripscan.py`: `00149DC0` and
>   `0014A48A` with 54 each, `00147B00` 30, `0012B980` 27, …; interior reads 2026-09-17
>   (SWE2-FRONTIER) confirm the family — all three open by loading the Q15 transform constants
>   `5A825A825A825A82` = cos(π/4) and `0000200000002000` = the rounding bias, `00147B00` at
>   [`00147B32`](../../_index/ADDRESS-INDEX.md) from `03001A20`/`03001A30`, `0012B980` identically
>   from `03001380`/`03001570`/`03001590` at `0012B9B2`, `00149DC0` from its own constant block
>   (`00149DF3` reads `[rbp+0x30]`, `00149DF7` builds `[rcx+rdx]` row pointers) —
>   these are integer DCT/IDCT-class kernels; `0014A48A` is a different member of
>   the same hand-written window — a byte-domain blend/composite kernel: no calls,
>   `paddsb`/`pand`/`pxor` over the `03001EB0`–`03001EF0` mask block
>   (`0101..`/`7F7F..`/`8080..`) using the xor-`0x80` signed-bias trick, at
>   [`0014ADF7`](../../_index/ADDRESS-INDEX.md)), so it is assembler-named constant data
>   ([the unlisted code](../../99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md)).
>   Assembler objects carry no `/guard:cf` lists, so `.rodata` says nothing about which objects contributed `.gfids`.
> - **What would decide it:** the objects themselves, or a linker map. Neither is in the image. No listed function's
>   symbol index can be recovered from the executable, so the 12 values cannot be joined to functions.

## `T-4` bounded — every initializer dependency found is INTRA-translation-unit (FABLE, 2026-09-22)

**The question is decidable in one direction.** An initializer relies on another's order exactly
when it **reads a global that the other writes**. A sweep of each initializer's *own body* — not its
callees — gives **under-approximated** read/write sets, and that is what makes the result usable:
*it cannot prove absence, but every pair it finds is real.*

**Two controls, both against figures this database published before the sweep existed.** The table
at `008C31D8`–`008C5678` parses to exactly **1,172** slots — §6's figure — and **1,172 of 1,172**
point into `.text`. And exactly **8** initializers write `02E522E0`, the context-switch word budget,
matching the eight static installers that
[the context-switch page](../../22-Middleware-PhyreEngine/Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md)
§3 documents.

| | |
|---|--:|
| initializers with a direct `.data`/`.bss` **write** set | **535** |
| initializers with a direct `.data`/`.bss` **read** set | **1,044** |
| **globals written by one initializer and read by a different one** | **8** |

### The ordered dependencies are one compiland, not two (FABLE, 2026-09-22)

The clearest chain looks at first like exactly what `T-4` asks about. `00164180` **constructs** an
object at `02CF8270` and installs a function pointer into it; `00163E30` then calls
`00631C40(dest = 02CF8470, src = 02CF8270, 0x30)` — **deriving its own object from that one** — and
five more initializers read `02CF8270` the same way. `02CF8470` is in turn read by `00163EA0`, so
it is a **two-level chain**. Every reader runs after its writer.

> **But all nine bodies are a single translation unit, and that changes the answer.** They occupy
> **slots 356–365** of the table *and* a **contiguous run of `.text` — nine bodies from `00163DB0`
> to `00164180` with zero other functions between them.** MSVC emits one compiland's initializers
> contiguously in both places. **Order within a translation unit is guaranteed by declaration
> order**, so this is not the fragile link-order reliance `T-4` is about. *The second ordered pair,
> slots 733 → 735, is adjacent in the same way.*

**And the only DISTANT pairs run in the wrong direction to be dependencies.** `0015BC40` sits at
slot **3** and reads `01F2CDF8` and `01F2CE20`, which are written at slots **106** and **161** —
*the reader runs first*, so it takes the statically initialised value and cannot be depending on
those writers at all.

> **So: no cross-translation-unit order reliance was found, and absence is NOT proven.** The sweep
> reads no callees, so an initializer that reaches a global through a helper is invisible to it.
> **What the result does establish is that the obvious place to look has been looked at** — the
> 8 shared globals are enumerated, and each one is either intra-TU or ordered the wrong way round.

## 13. What runs before the initializer tables (2026-09-07, `xiionline-8d`)

This document has always started at `_initterm`. **Two things run before it**, and for a document
whose subject is injection timing that window is the interesting one — it is the only period in
which the process is alive and the engine does not exist yet.

The chain from the PE entry point, every step read from its own body:

```
AddressOfEntryPoint  RVA 006E8EE4  ->  VA 00808EE4
  entry (00808EE4, 18 B)
    call __security_init_cookie   (00809B8C, 172 B)   <- the FIRST call in the process
    jmp  00808D78                 (330 B, the CRT startup)
         call __scrt_initialize_crt          (0080893C, 73 B)
         call __scrt_acquire_startup_lock    (00808900)
         call _initterm_e                    (00862022) -> the C table,   __xi,     3 entries
         call _initterm                      (0086201C) -> the C++ table, __xc, 1,172 entries
         call __scrt_release_startup_lock    (00808AF0)
         call _register_thread_local_exe_atexit_callback  (0086203A)
         call _get_narrow_winmain_command_line            (00862016)
         call 007A3770                       (45 B)     <- the game's entry, see below
```

`entry` is eighteen bytes and does exactly one thing before handing over: it initialises the stack
cookie. So the true order is **cookie, then C initializers, then the 1,172 C++ initializers, then
the game**.

### Why the cookie step belongs in an injection-timing document

`__security_init_cookie` overwrites the global at `01F44830`, which ships holding the MSVC default
`0x00002B992DDFA232`, with a 48-bit per-process random value. The full mechanism is in
[the image-hardening document](../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md#10-b-2f--is-anything-else-nominal-2026-09-07).
What matters here is the timing:

- **Injected before `entry` runs** — a process created suspended, or a debugger at the entry point —
  the cookie global still reads as the compile-time default. Anything cached from it is stale the
  moment `entry` executes.
- **Injected after** — which is every ordinary DLL injection, because the loader runs `DllMain` for
  a statically-imported DLL *before* `entry`, but an injected one arrives far later — the cookie is
  already the live per-process value.
- **There is no TLS-callback window.** This document's §"TLS: storage yes, callbacks no" establishes
  that the callback array's first entry is null. A TLS callback would ordinarily be the one hook
  that runs *before* `entry`; in this image that door does not exist, so `entry` really is first.

Practically: **the earliest engine-neutral hook point in the process is `00808D78`**, after the
cookie is live and before a single initializer has run. Nothing engine-side exists yet, so nothing
engine-side can be inspected — but it is the only place where all 1,172 constructions can still be
observed from the start.

### Where this repository's DLL lands — `CJ-2` answered 2026-09-26 (FABLE, Claude Opus 5.5)

**`XIIOnlineNet`'s `DllMain` runs after `entry`, after the cookie is live, and after every C and C++ initialiser.** It
is loaded at the CRT's call to `WinMain`. The deployed clients (`D:/FFXII MP Mod/FFXII_TestClient{1,2}/x64`) load it
through the FF12 module loader, a proxy `dinput8.dll` with `hook.ini` and a `modules/` folder. The route has three steps:
- The shipping exe imports `DINPUT8.dll` statically. So the proxy's own `DllMain` does run during static-import
  initialisation, before `entry`, which is the case the bullet above describes for a statically imported DLL.
- That `DllMain` does not load the modules. On `DLL_PROCESS_ATTACH` it installs its module loader as a detour on exe
  base `+ 0x6E8E8A` through the trampoline's `createHook`, and it never calls the loader itself.
- Exe base `+ 0x6E8E8A` is `00808E8A`, the startup routine `00808D78`'s `call 007A3770`: the `WinMain` call. It comes after
  `_initterm_e` (`00808DDB`) and `_initterm` (`00808DFC`), and `entry` has already run `__security_init_cookie`. The
  detour loads every module and then calls the real `WinMain`.

So the DLL reads the live per-process cookie, and every engine singleton built by a static initialiser already exists
when it attaches. The lazy statics above exist only if something has already touched them. The loader's own log shows the same order: *Hijacking
DINPUT8.dll*, then *Initialized module* for each module, `XIIOnlineNet.dll` last. **Scope:** this is the loader build
deployed today (`dinput8.dll` sha256 `1a335f09…71df`, the same in both clients); a different loader must be re-read.
A detour inside the DLL still sits under `CI-2`'s constraint. Control: `_index/candidates/cj2-load-order/load_order.py`
(6 checks, static reads of the exe and the proxy).

### The game's own entry

`007A3770` (45 B) is called immediately after `_get_narrow_winmain_command_line`, in the position
MSVC's CRT startup reserves for `WinMain`. Forty-five bytes is a thunk, not an application, so this
is the `WinMain` shim rather than the game's real main loop. **The identification is positional —
tier 1 for the call sequence, tier 6 for the CRT-source shape that names the slot — and the body it
forwards to has not been traced here.** Recorded so the next session does not re-derive the chain;
~~naming what `007A3770` actually calls is left open.~~ *Answered 2026-09-12 (FABLE, `CJ-1`): it is `WinMain` and
forwards to the game's real `main` on both arms of a debugger check
([what the engine fixes at boot](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)). Noted here
2026-09-26.*

### What this does *not* change

The 1,172-entry count, the two-table split (T-1), the ownership breakdown (T-2) and the copy
analysis (T-3) are untouched — this section adds a prologue to the timeline and corrects nothing in
it. No address or count already in this document was re-derived for it.

## 9. Related

- [`../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md) — S-1 and S-4 originate there; the guard pointers sit immediately before this table
- [`../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) — 227 of these initializers build Phyre class descriptors
- [`../../00-Engine-Core-Runtime/`](../../00-Engine-Core-Runtime/) — what runs once `main` is reached

## 9. Falsification pass 2026-09-02

**Attack chosen.** Everything load-bearing here is a **PE structure or a pointer table**, so all of
it can be read directly from the authorized binary. The headline claims **1,172** eager initializers
and ~~**117** lazy statics~~ **1,681** lazy statics *(answered: see §12, corrected 2026-09-02 - 117 was a tag population; 1,681 distinct guards at 1,732 sites in 707 functions, recounted at the image; 2026-10-02, OPUS)*, and §2 makes four specific TLS assertions.

### SURVIVED, and more strongly than claimed: the CRT initializer table

The table at `0x008C31D8`–`0x008C5678` holds `(0x8C5678 - 0x8C31D8) / 8` = **1,172** qword entries,
exactly as documented. Reading every one of them:

```
entries pointing into .text        1172
null entries                          0
entries anywhere else                 0
of those, known function entries   1172
```

**All 1,172 are valid function entries. Not one null, not one stray.** The document claimed the
count; the table is stronger than that — it is completely dense and completely valid, which is what
a compiler-generated initializer run should look like and is worth recording as such.

### SURVIVED: three of four TLS assertions

Read from the PE TLS directory:

| Field | Value | Document | |
|---|---|---|---|
| `AddressOfIndex` | `0x02EAED3C` | `0x02EAED3C` | ✅ |
| `AddressOfCallBacks` | `0x008C56B0` | `0x008C56B0` | ✅ |
| callback array contents | first entry **null** | "empty" | ✅ |
| raw data | `0x03004000`–`0x03004008` = **8 bytes** | "8 bytes" | ✅ |

*(The `.tls` section's virtual size is `0x9`, one byte more than the raw data span. The section is
padded; the directory is authoritative, and the document's 8 is right.)*

**"Storage yes, callbacks no" is confirmed at the structure level**, which matters for injection: no
TLS callback runs, so there is no pre-`main` hook point of that kind in this binary.

### OVERTURNED: the TLS directory address is an RVA

| | |
|---|---|
| Document | `0x01BCBED8` |
| **Actual VA** | **`0x01CEBED8`** |
| Difference | `0x120000` — exactly the image base |

`0x1BCBED8` is the **RVA** recorded in the PE data directory. This is the **same error class as
§9 of** [`../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md),
where `.reloc` and `.gfids` were also given as RVAs — **three instances, all in this category.**

**The cause is now identifiable and worth stating**, because it predicts where the next one will
be: addresses taken from **PE data directories and the section table are RVAs**, while every address
taken from **Ghidra already includes the base**. Every address in these documents sourced from
Ghidra is correct; every address sourced from a PE structure by hand was short by `0x120000`. Mixing
the two sources in one table is what produces it.

**Why it is hard to catch mechanically.** A guard was written for exactly this and then removed: the
obvious test — *outside the image, but inside once the base is added* — **misses all three cases**,
because this image spans `0x121000`–`0x3095400` and an RVA that large is itself a valid VA.
`0x01BCBED8` resolves cleanly into `.rdata`; it simply is not the TLS directory. The guard's only
hits were quoted float bytes. The reasoning is recorded in `verify_doc_addresses.py` so it is not
attempted again. **This class is caught by checking a citation's *semantics* against the real PE
structure — which is what this pass did by hand.**

### Not re-derived

The ~~**117**~~ lazy function-local statics *(answered: see §12 - 1,681 statics at 1,732 sites; 2026-10-02, OPUS)* and the family counts in §2 were not recounted this pass.
They rest on the GFZ tag census and are unaffected by the TLS correction.

## 10. Falsification pass 2026-09-02 (second) — T-1's premise was wrong; T-1 and T-2 answered

**How this document was reached.** An unrelated census of every contiguous run of function pointers
in the image flagged `008C31D8` as the largest table in the executable — 1,172 slots — and opened it
as an unknown. **It was already documented here**, base, end and count identical. The re-derivation
was independent (a blind `.rdata` scan, versus this document's anchored one) and agrees exactly,
which is worth more than the wasted motion cost.

### T-1: there is no boundary inside the run — there are two tables

The question assumed the C and C++ initializers share the 1,172-entry block and that "the data does
not separate them". **The data separates them completely.** `00808D78` — the CRT startup driver —
makes the two standard calls back to back:

```asm
00808DCD  lea rdx, [rip + 0xBC8CC]   ; -> 008C56A0    __xi_z
00808DD4  lea rcx, [rip + 0xBC8A5]   ; -> 008C5680    __xi_a
00808DDB  call _initterm_e                            ; C initializers, run FIRST
00808DE0  test eax, eax / jne -> return 0xFF          ; a C initializer may FAIL the startup

00808DEE  lea rdx, [rip + 0xBC883]   ; -> 008C5678    __xc_z
00808DF5  lea rcx, [rip + 0xBA3D4]   ; -> 008C31D0    __xc_a
00808DFC  call _initterm                              ; C++ initializers, run SECOND
00808E01  mov dword ptr [rip + 0x26A5EED], 2          ; startup state := 2
```

| table | bounds | entries | runner |
|---|---|---:|---|
| **C** (`__xi`) | `008C5680` – `008C56A0` | **3** | `_initterm_e` |
| **C++** (`__xc`) | `008C31D0` – `008C5678` | **1,172** | `_initterm` |

**The entire 1,172-entry run is C++.** The C table is elsewhere in `.rdata` and has three entries:
`00808C90`, `00808D4C`, `00809124`.

Two details that matter for injection timing, both new:

- **`_initterm_e` is checked for failure and `_initterm` is not.** A C initializer returning non-zero
  aborts startup with `0xFF` before any C++ initializer runs. The 1,172 C++ initializers have no
  failure path.
- **The startup-state global is `02EAECF8`, and it has three states, not two.** ~~`0x026A5EED`~~
  *(corrected 2026-09-21 (FABLE) on `ASTRA-RETURN-FABLE-UQ146-PRINTF-INITIALIZER`: **`026A5EED` is
  the rip displacement of `00808E01`, not an address** — a reader who looked it up found nothing.
  ASTRA caught it; all three instructions were re-resolved here and agree.)* The same dword is read
  at `00808DAA` and compared with `1` to detect re-entry, written `1` at `00808DC3` **before either
  table runs**, and written `2` at `00808E01` after both. So `0` means untouched, `1` means
  initialization in progress, and only `2` is the "initialization complete" flag — the re-entry
  test works precisely because of the `1` the earlier line did not mention.

### T-2: who owns the 1,172

| owner | initializers | share |
|---|---:|---:|
| **`Input`** | **325** | **27.7 %** |
| `Phyre` | 317 | 27.0 % |
| `Runtime` | 279 | 23.8 % |
| `CompilerGeneratedCpp` | 101 | 8.6 % |
| `NativeRoutine` | 62 | 5.3 % |
| `EASTL` | 58 | 4.9 % |
| `Platform` | 19 | 1.6 % |
| `NativeAdapter` 4 · `Presentation` 3 · `Application`, `RNG`, `Resource`, `Audio` 1 each | 10 | 0.9 % |

**`Input` is the single largest contributor to pre-`main` startup — more than Phyre.** That is
surprising for a subsystem the player never thinks about, and it is consistent with the separate
finding that `Input` is one of only two owned subsystems built as classes at all
([the RTTI vtable object model](../../00-Engine-Core-Runtime/Object-Model/rtti-vtable-object-model.md),
125 virtual methods against zero for every combat subsystem).

The table is **not sorted** — 51 % ascending steps, i.e. link order — and the owners appear in
contiguous blocks (EASTL first, then Phyre and Runtime interleaved, then Platform, then 370
consecutive `Input` entries). **Link order groups a translation unit's initializers together**, which
is why the ownership census reads as blocks rather than a mixture.

**Not claimed:** that these shares reflect startup *time*. They are counts of initializers, and one
initializer that builds a large table costs more than fifty that assign a pointer. **T-6.**

## 11. Falsification pass 2026-09-02 (third) — T-3 answered, and the count was wrong

### The count: 145 is not right, and it conflates two populations

| measured | |
|---|---:|
| functions in the image tagged `Runtime.StaticLifetimeInfrastructure` | **149** |
| of those, present in the CRT initializer table | **96** |
| tagged but **not** in the table — reached some other way | **53** |

This document's section 2 table records **145** in a breakdown of the 1,172 CRT entries. Neither
number matches: image-wide it is 149, and only **96** are CRT entries. **A count of functions with a
tag is not a count of table slots carrying that tag**, and the two were merged. Corrected here rather
than in place, because both numbers are now needed.

### T-3: what is copied, and where it lands

Separating true bulk-copy sources (`movaps`/`movups` **loads**) from `lea` targets matters — an
earlier cut of this measurement counted `lea` self-pointers as "sources" and made source and
destination appear to overlap. With `lea` excluded there is **zero overlap**.

| | distinct | total |
|---|---:|---:|
| **prototype sources** (XMM loads) | 20 | **320 bytes** in 2 clusters |
| **destinations** (XMM stores) | 86 | **6,692 bytes** in 5 clusters |

```
PROTOTYPES        01DF0980 .. 01DF0A70   (256 B)
                  01F800F0 .. 01F80120    (64 B)

DESTINATIONS      01DF15DC .. 01DF1A30   (1,108 B)
                  01F80130 .. 01F80C68   (2,872 B)
                  02EA5510 .. 02EA5520      (16 B)
                  02EAD018 .. 02EAD810   (2,040 B)
                  02EADC20 .. 02EADEB0     (656 B)
```

**320 bytes of prototype fill 6,692 bytes of globals.** The authored starting state is not a large
dataset — it is a small record **stamped repeatedly**, which is exactly the loop shape in
`0015BD30`: a `0x40` header copy followed by a `0x80`-per-iteration block loop, three records of
stride `0x15C`.

### Who owns the globals that receive it

Counting every instruction in the image that references each destination cluster, by owner:

| cluster | bytes | referencing functions | owners |
|---|---:|---:|---|
| `01DF15DC` | 1,108 | 7 | **`Input` 31 refs**, `Runtime` 19 |
| `01F80130` | 2,872 | 10 | `Runtime` 44, **`Input` 18** |
| `02EA5510` | 16 | 1 | `Runtime` 1 |
| `02EAD018` | 2,040 | **150** | **`Audio` 611 refs**, `Runtime` 59, `SQEX` 34 |
| `02EADC20` | 656 | 52 | **`Audio` 184 refs**, `Runtime` 22, `SQEX` 18 |

**Every prototype-copy destination belongs to `Input` or `Audio`.** Not one of them is a combat,
movement, party, world or UI global.

### The modding value is real, but it is not where this document expected

Section 7 filed T-3 as "high modding value" on the reading that these carry authored starting state
for engine globals generally. **They do not.** A direct check against every global this database has
documented — force fight mode `01E0C2B8`, the formula step table `01EFA5C0`, the battle action table
`01EEC460`, the battle record array `0208E690`, the native command tables `02B57EF0`, the pooled
record pointer `02093958`, the input channel records `022CAE90` — finds **none** of them in a
prototype-copy destination.

What is there instead is narrower and arguably more useful: **cluster `01DF15DC` is referenced by
`00195DF0`, which the GFZ names `InputManager_RestoreDefaultBindings`.** If that name is right, the
1,108-byte block is **the authored default control scheme** — written once at startup and written
again whenever the player picks "restore defaults" in the config menu, which would make it directly
editable to change what the controller does out of the box.

> **T-7 RESOLVED 2026-09-02 — the lead was half right, and the half it got wrong matters.**
> `00195DF0` does rebuild the binding profiles, but **`01DF15DC` is a staging buffer, not the
> authored defaults.** The function assembles each profile at `0x01DF1738 + i*0x15C` from authored
> records at **`0x01F80F90`** (3 records, stride `0x70`), then copies `0x15C` bytes into the **live
> binding profile table at `0x01F80130`** — the same three addresses the CRT initializer `0015BD30`
> stamps before `main`. A stride and base derived twice, by different code.
>
> So this cluster *is* part of the default control scheme, as the scratch area it is built in — and
> the editable authored bytes are elsewhere. Full read in
> [the input stack](../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md)
> section 11.

The two `Audio` clusters are larger and far more heavily used — 795 references across 202 functions —
and are ~~unidentified~~ SQEX Sead's static pools *(answered: see T-8, answered on the page 2026-09-14; 2026-10-02, OPUS)*. **T-8.**

---

## 12. REOPENED and corrected 2026-09-02 (fourth pass) — the lazy count was a tag population

Reopened under trigger 5 (*a higher evidence tier became available for a claim carried by a lower
one*) and trigger 2 (*a newly derived fact contradicts a claim this document makes*), filed as
**BI-1**. Run against snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`.

### What was believed

> "117 more are built lazily the first time anything touches them." · "All 117 share one shape."
> · "These 117 globals do not exist until something calls their accessor." · "the exact test
> compiled into all 117 accessors."

### What is now believed

**1,681 distinct thread-safe function-local statics, reached from 1,732 guarded construction
sites, spread across 707 functions.**

| measurement | value |
|---|---:|
| `call _Init_thread_header` (`008092FC`) sites | **1,732** |
| `call _Init_thread_footer` (`0080929C`) sites | **1,732** |
| guards resolved from the `lea rcx,[rip+g]` preceding each site | **1,732 of 1,732**, all in `.data` |
| distinct guard variables | **1,681** |
| distinct functions containing at least one | **707** |
| guards carrying an `_Init_thread_abort` unwind funclet | **1,545** |
| guards without one (non-throwing construction) | **136** |

Sites exceed objects because **19 guards appear at more than one site**, always in *different*
functions — the compiler inlined one accessor into several callers. That accounts for the
difference exactly: 1,732 − 1,681 = 51 extra sites.

Distribution across the 707: 451 functions hold exactly one lazy static, 52 hold two, 33 three,
99 four, and the tail runs to **28 in one function** (`005AD8F0` and `005E5400`).

### What proved it

Per-function disassembly of all 38,161 exact-current bodies from their own entry points, counting
real call sites rather than call-graph edges — the edge count is 707 by construction, because
`edges.tsv` stores one row per caller/callee pair regardless of how many times the call appears.
Two independent closures agree with it: every one of the 1,545 guard addresses recovered from the
`_Init_thread_abort` unwind funclets is also a header-site guard, and no header-site guard is
missing from that intersection in either direction.

### Why the earlier reading was reachable — and it is not a careless error

The 117 figure is *correct as what it measures*. All 117 functions tagged
`CompilerGeneratedCpp.ThreadSafeStaticRecordAccessor` do contain a guarded construction; the tag
fires precisely when the accessor **is the whole function**. The other 590 holders have a magic
static buried inside a larger routine and were therefore labelled by what that larger routine
looks like — Phyre 224, `NativeRoutine` 167, unlabelled 150, `CompilerGeneratedCpp` 140.

**A tag population and a mechanism census are indistinguishable when the tag is all you have.**
Both are a number attached to the same words, and nothing in the classification says which one it
is. The same failure appeared twice more in this database on the same day — `ThirdParty` counted
690 functions when contents-matching finds 801 across twelve libraries, and this session's own
funclet document briefly reported 1,732 *objects* when 1,732 was the *site* count. The cure in
all three cases was identical: **re-derive the population from the binary instead of re-selecting
it from the classification, and state the selector alongside the number.**

Note what this means for the four falsification passes in sections 9–11. None of them was
negligent, and none of them could have caught this: each re-checked the claims the document made,
and the document's claim was internally consistent. What breaks a tag-population error is not a
better audit of the document — it is counting the mechanism.

### What did not change

The mechanism in section 2, the TLS-epoch gate in section 4, the `_Init_thread_header` /
`_Init_thread_footer` protocol and the entire eager path are all unaffected and were re-derived
independently this pass, matching instruction for instruction. Only the count was wrong.

### Propagation

Every occurrence of the figure in this database was checked. It appears **only in this document**
and in the two places that flagged the correction (this category's `README.md` and the
exception-funclet document's section 8). The other `117`s found by a corpus-wide search are
unrelated quantities — Phyre class counts, body sizes in bytes, a licence-board row range. **No
downstream document inherits the wrong number, so no further reopening propagates from BI-1.**

### Not re-derived this pass

The 1,172-entry eager table, the TLS directory parse, the teardown family counts and the
`Input` 325 / `Phyre` 317 initializer attribution were left as sections 9–11 established them.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Developer — CLIENT, not read.** An 18-byte function this page cites is called by a 1,046-byte Developer-labelled body.

## The `00808D4C` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00808D4C` (16 B) — a `sub rsp, 0x28` thunk that calls `00809C50` (**identified 2026-09-21 (FABLE):
the CRT formatter-option initializer — it ORs `4` into the printf options qword behind `0016D670`
and `2` into the scanf one behind `0018A320`, and is the only writer of either in the image**),
zeroes `eax`, and returns
(`00808D50`/`00808D55`/`00808D5B`) — a CRT init-terminator /
registration-return shape.

| member | role | interior |
| --- | --- | --- |
| `00809C50` | callee body | [`00809C50`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-38 update (2026-09-19) - `0015BD30`

`0015BD30` (484 B) is the prototype-copy initializer the page names - call-free `movaps` `.data`-to-`.data` (~~`01DF09E0` into `01F80140`+~~ `01DF09C0` into `01F80130`+ *(corrected 2026-10-02, OPUS: `0015BD30` itself reads `01DF09C0` and `0015BD30+0x1C` stores it at `01F80130`; `01DF09D0` goes to `01F80140` at `0015BD30+0x32`, and `01DF09E0`, read at `0015BD30+0x28`, to `01F80150` at `0015BD30+0x40`)*), then a `movups` 0x80-step bulk copy loop. Interior anchor `0015BD87` (inside the copy loop).

## SWE2-EC7-79 update (2026-09-20) - `005FD0E0` TLS-guarded lazy singleton measured

`005FD0E0` (129 B) is the CRT-style lazy accessor: `gs:[0x58]` TLS
slot `02EAED3C` supplies the pointer, `[+4]` is compared against
`02CE70B0`; a higher value runs `008092FC` (~~the lock-init~~ `_Init_thread_header`, which claims the guard *(corrected 2026-10-02, OPUS: the lock `02EAED40` is created by the C initializer `00809124`: `00809124+0x12` loads it and `00809124+0x1E` calls the critical-section initialiser `00861EF0` with spin count `0xFA0`)*), and a
`-1` mark then runs `005DC200(02CE4720)` (the ctor), registers
`008ADDE0` through `00808B90` (atexit), and `0080929C` unlocks.
Either way `02CE4720` is returned - the once-per-process singleton
the callers share.
Interior anchor `005FD0F5` (the `gs:[0x58]` TLS read).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Audio — CLIENT, 88 edges: the prototype pools' referencing functions are SEAD's driver.** This page cites
`007B31A0` (50 references into the first static cluster) and `007BAEC0` (19 into the second), and the band
`007AB5C0`-`007BC4F0`. Those bodies call the rest of SEAD's driver (`007AA3E0`-`007AA550`, `007A46E0`, `007A7A20`,
`007BB610`, `007DF8D0`, `007EFB20` and more) and are called from `007A5400` / `007A5E50` / `007BD120`-`007BED30`.
- The CRI HCA entry `00121000` sits in the same neighbourhood.
- The CRT formatter-option ~~initializer~~ accessor `0016D670` is reached from `007A5570` *(corrected 2026-10-02, OPUS: `0016D670` is `lea rax, [02EBA3D0]; ret`, the printf-options accessor, with 23 call sites; the initializer is `00809C50`, which ORs `4` into what it returns)*.

Which pools the sound engine initialises is the 18 pages' subject.

**Resource, 6; Platform, 1; Audio's `0021xxxx` bodies — SERVICE.** The ~~memory-status reader~~ record zero-initializer `005CC8A0` *(corrected 2026-10-02, OPUS: its 25-byte body zeroes `+0`, `+8`, `+0x10`, `+0x18`, `+0x20` and `+0x24` of `rcx` and returns `rcx`; it reads no memory status)* is called by
`00165F80`, `0019F490`, `0019F620`, `001D9400`, `0061F200` and `002116B0`-`0021A9F0`.

**Input — CLIENT, four edges.**
- `InputManager_RestoreDefaultBindingProfiles` (`00195DF0`), named in T-3 as the copy from the 1,108-byte static
  cluster, is called by `InputManager_Initialize`, `001E0F70` and `001E1050`.
- It asks `InputBinding_ShouldKeepAuthoredPairOrderForPlatformState`.

**Presentation — MECHANICAL, four edges.**
- `001FE8B0` is called by `001C5750`, `001C6E20` and `001CCB20`.
- The 28-lazy-static body `005AD8F0` is called from `005C5C80`.



**CoreRuntimeScheduling — CLIENT, 1 edge: the scheduler runs the cited commit.** (2026-10-02,
 SWE2-CONTRACT, graph-churn residue)
- `0017D6E0` calls `00189CE0` (the `ActiveCameraSnapshotAndDerivedRenderMatrixCommit` body cited
  for its `_Init_thread` epoch gate) — the camera commit's caller surface, not a scheduling
  relationship of this page's subjects.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 slice OPUS-P22-SLICE-24-99).*

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-static-initialization-order-and-injectio-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00163DB0` | 122 B | calls `00631A60(02CF8370, 02CF8680, 8)`, clears bit 1 and sets bit 3 of dword `02CF846C`, stores `02CF8E80`, `02CF8EE0` and `02CF8F40` at qwords `02CF8430`, `02CF8438` and `02CF8440`, stores `00D56AD8` at qword `02CF8370`, and tail-jumps `00808B90` with the address of a 26-byte stub | `00163DC8`, `00163DDA`, `00163DFF`, `00163E13`, `00163E25` |
| `00163E30` | 108 B | calls `00631C40(02CF8470, 02CF8270, 0x30)`, ORs 2 into dword `02CF856C`, stores `02CF7F60`, `02CF8060` and `02CF8160` at qwords `02CF8530`, `02CF8538` and `02CF8540`, stores `00D56768` at qword `02CF8470`, and tail-jumps `00808B90` with the address of a 26-byte stub | `00163E48`, `00163E4D`, `00163E5B`, `00163E8C`, `00163E97` |
| `00163EA0` | 119 B | calls `00631E20(02CF8580, 02CF8470, 0)`, clears bit 1 and sets bit 3 of dword `02CF867C`, stores `02CF7AE0`, `02CF7C20` and `02CF7D60` at qwords `02CF8640`, `02CF8648` and `02CF8650`, stores `00D56ED0` at qword `02CF8580`, and tail-jumps `00808B90` with the address of a 26-byte stub | `00163EB5`, `00163EC7`, `00163EEC`, `00163F00`, `00163F12` |
| `00164180` | 56 B | calls `006318A0(02CF8270)`, stores 0 at dword `02CF82A8` and `00D582D0` at qword `02CF8270`, and tail-jumps `00808B90` with the address of a 26-byte stub | `0016418B`, `00164197`, `001641A8`, `001641B3` |
| `001E0F70` | 49 B | when `InputManager_GetSingleton()` is non-null, calls `InputManager_MaterializeRuntimeBindingProfiles(InputManager_GetSingleton())` and tail-jumps `InputManager_RestoreDefaultBindingProfiles(InputManager_GetSingleton())`; otherwise returns | `001E0F74`, `001E0F7C`, `001E0F86`, `001E0F97` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-static-initialization-order-and-injectio-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00808C90` | 185 B | calls `0086200A` (the `_set_app_type` stub) with 2, `0086202E` (`_set_fmode`) with the result of `00809C38()`, then stores `005C5230()` at the dword `0086204C()` (`__p__commode`) returns; when `00808988(1)` returns 0 in `al` calls `0080996C(7)` (an int3 follows); otherwise calls `00809C88()`, `00808B90(00809CD4)` and `00861FE0` (`_configure_narrow_argv`) with the result of `0053DD10()`; a non-zero result loads 7 into `ecx`, the last listed instruction; otherwise calls `00809C40()` and, when `00809C6C()` returns non-zero, `00862010` (`__setusermatherr`) with `005C5230`; then calls `0016D6A0` twice with no argument set up, `00862040` (`_configthreadlocale`) with `005C5230()`, `00861FE6` (`_initialize_narrow_environment`) when `0061ECF0()` returns non-zero in `al`, and `005C5230()`; returns 0 | `00808C9B`, `00808CC0`, `00808CE1`, `00808CFF`, `00808D23` |

### Crossings into other layers - functions this page's newest interior rows name (OPUS, 2026-10-03)

- **Script_VM_Native_Bridge - SERVICE (17 edges).** `0053DD10` is also called by `00341840`, `00341F90`, `00345250`, `00346AA0` (+8 more), filed to the script VM / native bridge (+5 more edges of the same shape) - shared machinery across the layer boundary, no shared ownership.
- **UI - SERVICE (1 edge).** `0053DD10` is also called by `003C80C0`, filed to ui - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (1 edge).** `0053DD10` is also called by `003789A0`, filed to world area - shared machinery across the layer boundary, no shared ownership.
