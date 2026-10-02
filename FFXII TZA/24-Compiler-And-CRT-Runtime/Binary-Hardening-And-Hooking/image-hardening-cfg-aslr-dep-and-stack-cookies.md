---
system: Image hardening — CFG, ASLR, DEP and stack cookies
category: 24-Compiler-And-CRT-Runtime
status: AUDITED
owner_layer: CodeDomain:CompilerGeneratedCFG + PE image configuration
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 39 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-07
audit:
  passes: 2
  last_pass: 2026-09-07
  last_pass_state: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  crossref_clean: true
  reopened_count: 1
function_families:
  - "Phyre serialization scalar-conversion initialisers | C | members/scalar-conversion-registrars.tsv | 142 | the 383-byte thread-safe local-static initialisers 005850F0..00592770 - each lazily builds one node of the 12x12 (source,destination) scalar-conversion tree Phyre PSerialization registers under sentinel 01F2CDA0 and inserts through 0067F700, then atexit-registers its teardown. PROVED BY DERIVED FORM, NOT HAND-MASKED: 296 of 383 byte positions identical across all 144 (the 87 varying positions are the per-static block, guard, descriptor accessors and stored routine), and a census-wide search for that skeleton finds exactly these 144 and none outside the run - the run IS the family here, checked rather than assumed. Universal callees x144: 008092FC _Init_thread_header, 0080929C _Init_thread_footer, 00808B90 atexit, 0067F700 tree insert. Selector members/select_scalar_conversion_registrars.py re-derives membership from the EXE and refuses to write if the census-wide match, the universal-target set, or the A/declared exclusions move. The semantic join - which (source,destination) pair each node serves - comes from guard-adapter-registrars.tsv and is carried as columns, never as membership. NOT dispositioned: the 68 conversion routines themselves, the descriptor accessors 0062FF50..00630490, lookup 0059A030, and the shared sentinel tree state. 1 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. 2026-09-30 (SWE2-EC7, GI re-status): 1 member left the family, since measured as A (A beats a declaration) after SWE2-FRONTIER c97af7156 re-statused the 13 GI pages PARTIAL -> DOCUMENTED; exact A removal - the named selector's write asserts refuse any re-run once the family is declared, so it is not re-run."
---

# Image hardening — CFG, ASLR, DEP and stack cookies

> **The single most useful page in this database for anyone hooking FFXII.** The executable
> loads at a fixed address, does not validate indirect calls, and never moves between runs.
> Every one of those is a deliberate shipping configuration, and each is proven here from the
> PE headers and the instruction bytes.

## 1. What the player sees

Nothing — until they install a mod, and then everything.

Every FFXII trainer, cheat table, texture pack and multiplayer hook that works by naming a
memory address works *because of what is on this page*. The game always loads at the same place
in memory, so an address written down last year is still correct today, on any machine. And the
game never checks whether a function pointer it is about to call is a real function, so a mod
can redirect one and the game will follow.

If FFXII had shipped with the protections its own compiler flags asked for, most of the modding
scene around it would not exist in the form it does.

## 2. Native mechanism

### The image configuration, read from the PE headers

```
ImageBase           = 0x00120000
DllCharacteristics  = 0x8120
    + HIGH_ENTROPY_VA        (0x0020)
    + NX_COMPAT              (0x0100)   DEP enforced
    + TERMINAL_SERVER_AWARE  (0x8000)
```

**What is present matters less than what is absent.** Two flags are *not* set:

| Flag | Value | State |
|---|---|---|
| `DYNAMIC_BASE` | `0x0040` | ❌ **not set — no ASLR** |
| `GUARD_CF` | `0x4000` | ❌ **not set — CFG not enforced** |

`HIGH_ENTROPY_VA` is set but is meaningless on its own: it only widens the randomisation range
*when `DYNAMIC_BASE` is also set*. It is not. The image loads at its preferred base.

### Control Flow Guard: compiled in, shipped off

From `IMAGE_LOAD_CONFIG_DIRECTORY64`:

```
SecurityCookie                 = 0x01F44830
GuardCFCheckFunctionPointer    = 0x008C31C0
GuardCFDispatchFunctionPointer = 0x008C31C8
GuardCFFunctionTable           = 0x00000000     <- empty
GuardCFFunctionCount           = 0              <- empty
GuardFlags                     = 0x00000100     = CF_INSTRUMENTED
```

`CF_INSTRUMENTED` means ~~the code **was compiled**~~ some linked objects were compiled with `/guard:cf` — here only the statically linked CRT *(corrected 2026-10-02, OPUS: the check thunk `00809958` has 11 call sites, all in CRT start-up bodies `008087C4`–`00809CD4`, and the dispatch slot `008C31C8` is never referenced; the 2026-09-19 section)*. But the valid-target table
is empty and `GUARD_CF` is absent from `DllCharacteristics`, so the loader never activates it.

There is even a `.gfids` section — ~~512 bytes, room for 128 RVAs~~ **48 bytes of declared content,
which is exactly the twelve dwords and no more (corrected 2026-09-22, FABLE)** — which the load
config does not point at. The build produced the machinery and then did not wire it up.

> ### `T-9`: what the section actually declares, and why the twelve cannot be resolved here (FABLE, 2026-09-22)
>
> **The `0x200` above is the section's RAW size; its VIRTUAL size is `0x30`.** Twelve dwords at
> `+0x000`–`+0x02C` are the whole of the section's declared content — the remaining 464 raw bytes
> are file padding past `VirtualSize`, not room for 116 more RVAs. *In order they read* **49, 48,
> 19, 10, 13, 16, 69, 113, 10, 98, 55, 11.**
>
> **No guard table could point at them, and not merely because the one this page checks is zero.**
> `IMAGE_LOAD_CONFIG_DIRECTORY` here is **148 bytes** — it ends at `+0x94`. So
> `GuardAddressTakenIatEntryTable` (`+0x98`), `GuardLongJumpTargetTable` (`+0xA8`) and both their
> counts **do not exist in this image's structure at all**. The only guard table the build emitted
> is `GuardCFFunctionTable`, and it is `0`. *That closes the reading in which the twelve belong to
> one of the other guard tables: there is no field that could name them.*
>
> **And `GuardFlags` at `+0x90` reads `0x00000100`** — `IMAGE_GUARD_CF_INSTRUMENTED`, the single
> bit, straight from the load config. This page infers `CF_INSTRUMENTED` from the compiled code;
> the directory states it, which is `S-2`'s subject seen from the header rather than the bytes.
>
> **Why `T-9` stays open, now for a proven reason rather than an assumed one.** Its narrowing says
> deciding between readings *“needs the objects or a map”*. The image confirms it cannot supply
> either: **`NumberOfSymbols` is `0` and `PointerToSymbolTable` is `0`** — no COFF symbol table
> ships. If the twelve are unconverted `.gfids$y` symbol indices, **there is nothing in this file
> to resolve them against**, and no reading inside the image can distinguish them from any other
> small integers. *Controls: the pass reproduces this page's own `GuardCFCheckFunctionPointer`
> `0x008C31C0` and `SecurityCookie` `0x01F44830` before reporting anything.* **Static, headers
> read.**
>
> *Narrowed 2026-09-26 (FABLE, Claude Opus 5.5): the image names the twelve dwords' origin itself.* Its POGO debug record lists
> the whole `.gfids` content as one input contribution, **`.gfids$y`, `0x30` bytes at the section's first byte**. So
> they are the objects' own `.gfids$y` data, passed through unconverted, and not a table the linker built. Which
> functions they index still needs the objects' symbol tables, which do not ship. See "The debug directory" below.
>
> ***Answered 2026-09-27 (FABLE, Claude Opus 5.5): they are the statically linked C/C++ runtime's own `.gfids$y` data.** The objects do ship - in the public VS2015 Update 3 static runtime, installed for this test. Matching each position against whole `.gfids$y` runs of the x64 `libcmt` / `libcpmt` / `libvcruntime` objects names eight: 19 `std_type_info_static` (`??_Etype_info`), 10 `winapisupp` (`initialize_pointers`), 13 `jbcxrval` (`_guard_check_icall_nop`), **69, 113 `exe_winmain` (`_matherr`, `_RTC_Terminate`, a two-value run in place)**, 10, 98 `thread_safe_statics`, 55 `utility_desktop` (`__scrt_unhandled_exception_filter`), 11 `guard_support`. Chance control: none of 2,000 random twelves matches as many positions. 49, 48 fit the UCRT's `initialization` object and 16 `tlsdyn` (`__dyn_tls_init`); those three are inferred, because the installed runtime is build 24237 while the image's prebuilt objects are 24123 / 24210 / 23026, and the VS2015-era UCRT is not installable here. [Record](../../_index/candidates/t9-crt-gfids/README.md).*

**The runtime state is provable from the instruction bytes.** Both guard pointers resolve to
stubs that do nothing:

```
__guard_check_icall_fptr    @ 0x8C31C0 [.rdata]  ->  0x0016D6A0
    0x0016d6a0   c2 00 00        ret 0            <- the no-op check
    0x0016d6a3   cc cc cc ...    int3

__guard_dispatch_icall_fptr @ 0x8C31C8 [.rdata]  ->  0x00896270
    0x00896270   ff e0           jmp rax          <- unvalidated indirect jump
    0x00896272   cc cc cc ...    int3
```

`ret 0` is `_guard_check_icall_nop`. `jmp rax` is a bare indirect branch with no target check.

### ~~The 145 guard adapters are dead code~~ The 145 empty-destructor teardowns (corrected 2026-10-02, OPUS: each is registered with `atexit`, so not dead; the S-3 correction below)

145 functions carry `CompilerGeneratedCFG.StaticGuardAdapter`. Every one is 12 bytes:

```asm
0x008a83e0   48 8d 0d 01 2c 40 02    lea rcx, [rip + 0x2402c01]   ; -> 0x02CAAFE8 (.data)
0x008a83e7   e9 b4 52 8c ff          jmp 0x16d6a0                 ; -> ret 0

0x008a83f0   48 8d 0d 29 2c 40 02    lea rcx, [rip + 0x2402c29]
0x008a83f7   e9 a4 52 8c ff          jmp 0x16d6a0
```

Load a `.data` pointer into `rcx`, tail-call the guard check. The guard check returns
immediately. **All 145 of them — 1,740 bytes — are no-ops at runtime.** This is what the
`_guard_check_icall` branch in the Phyre descriptor destructors actually does: nothing.

> **Corrected 2026-09-14 (FABLE, S-3): these are not guard adapters, and they are not dead.** They are
> **static teardowns**: `lea rcx, [object] ; jmp destructor`, where the destructor is empty and the linker folded it
> onto the one-instruction `ret` at `0016D6A0`. That body also serves as `_guard_check_icall`, which is the only
> reason the family carries a CFG name. Every one of the 145 is referenced exactly once in `.text`, as the argument
> to `atexit` (`00808B90`), so each ~~**runs once at process exit**~~ **runs at most once, on a CRT `exit` path, and not at all on a normal quit**, and does nothing *(corrected 2026-10-02, OPUS: a site in the game's exit routine calls `ExitProcess` (address in FABLE's record readiness-apply-fable-1002c) through `008C2260`; the teardown page's UQ-331 answer)*. Member-by-member join:
> [`members/guard-adapter-registrars.tsv`](members/guard-adapter-registrars.tsv), by
> [`members/guard_adapter_registrars.py`](members/guard_adapter_registrars.py).
>
> - **144 are the nodes of one ordered tree**, a 12 × 12 matrix of scalar conversion routines. Each is registered
>   by its own 383-byte thread-safe local-static initialiser in `005850F0`–`00592770` (`_Init_thread_header`
>   `008092FC`). **Declared 2026-09-16 (SWE2-EC7) as EC-7 family C** *Phyre serialization scalar-conversion
>   initialisers* — members file `members/scalar-conversion-registrars.tsv`, selector
>   `members/select_scalar_conversion_registrars.py`, both in this directory. The initialiser fetches two type descriptors from the lazy-static accessors `0062FF50`–`00630490`,
>   stores them at node `+0x18` / `+0x20` with a code pointer at `+0x28`, and inserts the node under the sentinel
>   `01F2CDA0` (rebalance `0067F700`).
>   - The 12 descriptors, named by the string each initialiser stores at record `+0x30`: `bool`, `PChar`,
>     `PUInt8`, `PInt16`, `PUInt16`, `PInt32`, `PUInt32`, `PInt64`, `PUInt64`, `PUInt128`, `float` and `double`.
>     Every one of the 144 ordered pairs occurs once, the 12 identity pairs included. There are 68 distinct routines.
>   - **Direction, from two bodies:** the (`float`, `double`) routine `00594EB0` reads a `double` and writes a
>     `float` (`cvtpd2ps`), and the (`double`, `float`) routine `00594350` does the reverse (`cvtps2pd`). So `+0x18`
>     is the source type and `+0x20` the destination.
>   - The lookup is `0059A030`. On first use it calls all 144 initialisers (flag `02CA9D91`), then walks the tree
>     for (source, destination) and returns `+0x28` or 0. Its caller `0059D2D0` swaps the pair on a flag byte, and
>     **when no routine exists it stores `0016D6A0` itself as a do-nothing converter** (`0059D3BD`).
>   - `0059FE20`, slot 2 of `PSerialization::PUtilitySerialization`
>     ([vtable method index](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md)), empties the tree
>     through `0067F580` and clears the flag. The tree is therefore Phyre serialization's scalar-type conversion
>     table.
> - **1 is ordinary:** `008B1B00` tears down the 0x28-byte record `02D3E880`. The 32-byte dynamic initialiser
>   `00165F80` zeroes that record through `005CC8A0` and registers the teardown. What the record is was not read.
>   Its other rip-relative users are seven functions in `00675460`–`00677BA0`.

### What *is* enforced

Two protections are real and must be respected:

**DEP (`NX_COMPAT`)** — data pages are not executable. Injected code needs `VirtualProtect` or
`VirtualAlloc` with an execute flag.

**Stack cookies (`/GS`)** — genuinely live, genuinely randomised per process, and the whole
mechanism was read end to end in the B-2/f pass below. Overwriting a stack buffer past a protected
frame trips `__report_gsfailure`, which fast-fails the process. Cookie checks are per-function and
unaffected by the CFG situation.

> **This claim used to rest on the wrong kind of evidence.** Until 2026-09-07 the support for
> "cookies are live" was *`SecurityCookie = 0x01F44830` appears in the load config* — which is the
> presence of a **field**, not proof that anything uses it. That is the identical evidential shape
> that made CFG look enforced right up until someone read the check body and found `ret 0`. The
> bodies are now read; see section 10.

### Section layout

| Section | RVA | ~~Virtual size~~ Raw size, except `.data` and `.gfids` *(corrected 2026-10-02, OPUS: the column holds `SizeOfRawData`; the virtual sizes are in the corrected table below)* | Note |
|---|---|---|---|
| `.text` | `0x00001000` | `0x7A0800` | executable code |
| `.rdata` | `0x007A2000` | `0x152D800` | includes IAT and the guard pointers |
| `.data` | `0x01CD0000` | `0x11A7530` | |
| `.pdata` | `0x02E78000` | `0x68C00` | 35,713 `RUNTIME_FUNCTION` entries |
| `.rodata` | `0x02EE1000` | `0x1200` | |
| `.gfids` | `0x02EE3000` | `0x200` raw, **`0x30` virtual** | **present but unreferenced** — the declared content is twelve dwords; see `T-9` above |
| `.tls` | `0x02EE4000` | `0x200` | |
| `_RDATA` | `0x02EE5000` | `0xA400` | |
| `.rsrc` | `0x02EF0000` | `0x4BA00` | |
| `.reloc` | `0x02F3C000` | `0x39400` | relocations present but unused without ASLR |

`.reloc` is worth a note: relocation data is 234 KB and is shipped, but with `DYNAMIC_BASE` off
the loader has no reason to apply it. The image is relocatable in principle and fixed in
practice.

## 3. Key addresses

| Address | Role | Verified |
|---|---|---|
| `0x00120000` | `ImageBase` — the fixed load address | ✅ PE header |
| `0x008C31C0` | `__guard_check_icall_fptr` (in `.rdata`) | ✅ read |
| `0x008C31C8` | `__guard_dispatch_icall_fptr` (in `.rdata`) | ✅ read |
| `0x0016D6A0` | `_guard_check_icall_nop` — `ret 0` | ✅ disassembled |
| `0x00896270` | guard dispatch target — `jmp rax` | ✅ disassembled |
| `0x01F44830` | `SecurityCookie` | ✅ load config |
| `0x008A83E0` / `0x008A83F0` / `0x008A8400` | `StaticGuardAdapter` samples | ✅ disassembled |
| `0x03003000` | `.gfids` section — allocated, unreferenced (**corrected 2026-09-02**, was listed as the RVA `0x02EE3000`) | ✅ section table |

## 4. Data structures and formulas

```
IMAGE_OPTIONAL_HEADER64
  +0x18   u64   ImageBase            = 0x00120000
  +0x46   u16   DllCharacteristics   = 0x8120

IMAGE_LOAD_CONFIG_DIRECTORY64        size = 148 (0x94)
  +0x58   u64   SecurityCookie                  = 0x01F44830
  +0x70   u64   GuardCFCheckFunctionPointer     = 0x008C31C0
  +0x78   u64   GuardCFDispatchFunctionPointer  = 0x008C31C8
  +0x80   u64   GuardCFFunctionTable            = 0
  +0x88   u64   GuardCFFunctionCount            = 0
  +0x90   u32   GuardFlags                      = 0x00000100  (CF_INSTRUMENTED)
```

**Ghidra VA equals runtime VA.** Because `ImageBase` is `0x00120000` and ASLR is off:

```
runtimeVA = ghidraVA = ImageBase + RVA = 0x00120000 + RVA
```

Addresses in this database are directly usable against the live process. No rebasing step.

**CFG is enforced only when all three hold** (none of them do here beyond the first):

```
enforced  iff  (GuardFlags & CF_INSTRUMENTED)         <- true
          &&   (DllCharacteristics & GUARD_CF)        <- FALSE
          &&   GuardCFFunctionTable != 0              <- FALSE
```

**Guard adapter shape** (all 145 identical but for the displacement):

```
lea rcx, [rip + disp32]        ; a .data pointer
jmp 0x0016D6A0                 ; -> ret 0
```

## 5. Call chain

```
process load
  -> Windows loader reads DllCharacteristics
     -> DYNAMIC_BASE absent  -> map at ImageBase 0x00120000, ignore .reloc
     -> GUARD_CF absent      -> do not install CFG, leave the nop stubs in place
     -> NX_COMPAT present    -> enforce DEP

any indirect call compiled with /guard:cf
  -> __guard_check_icall_fptr
     -> 0x0016D6A0  ret 0                <- returns, no validation

function entry with a protected frame
  -> load SecurityCookie 0x01F44830
  -> on return, compare
     -> mismatch -> __report_gsfailure   <- this one is real
```

**Upstream:** the Windows loader, once, at process start.
**Downstream:** ~~every indirect call~~ the CRT's eleven guarded indirect calls (section 9a, 2026-09-19 - the game's own
indirect calls are not instrumented) and every stack frame in the binary.

**Do not confuse with:** the `.pdata` / `.xdata` exception unwind data. That is a separate
compiler facility in the same binary, and this database's evidence standard **bans it as proof**
of ownership or behaviour. Nothing on this page rests on it; the 35,713 entry count is reported
as a size fact only.

## 6. Modding notes

- **Addresses are stable. Use them.** Fixed `ImageBase 0x00120000` with ASLR off means a Ghidra
  address is the runtime address on every machine, every launch. This is why cheat tables and
  hardcoded offsets work at all for this game.
- **Indirect calls are not validated.** Vtable slots, callback tables and global function
  pointers can be redirected freely. The `_guard_check_icall` you will see in decompiled bodies
  is a `ret`.
- **You still need `VirtualProtect`.** DEP is genuinely on. Writing shellcode into a data page
  and jumping to it will fault.
- **Do not smash stacks.** `/GS` cookies are live; a buffer overwrite past a protected frame
  still calls `__report_gsfailure` and kills the process.
- **Do not "fix" the `.gfids` section.** It is present, empty of purpose, and unreferenced.
  Wiring it up would enable CFG and break every hook that depends on it being off.
- **XIIOnline:** the whole injected-DLL-and-detour approach is licensed by this configuration.
  Two consequences worth stating: the project may rely on fixed addresses without a rebasing
  layer, and it must not rely on CFG to catch a bad function pointer — nothing will. A corrupt
  pointer becomes an immediate `jmp rax` to wherever it points.

## 7. What is not known

- [x] ~~Whether `.gfids` contains real RVAs or is zero-filled padding. **S-1 — would show whether
      CFG was disabled deliberately at link time or never completed.**~~
      **S-1 ANSWERED 2026-09-13 (OPUS): NEITHER, and the question's two options are both wrong.**
      The section's **virtual size is 48 bytes** — the 512 on disk is file padding and every byte
      from 48 to 512 is zero. Those 48 bytes hold **twelve `u32` values**: `0x31 0x30 0x13 0x0A
      0x0D 0x10 0x45 0x71 0x0A 0x62 0x37 0x0B`. They are not zero, and **not one of them is a
      plausible RVA** — the image's `.text` spans RVA `0x1000`–`0x7A1635` and the largest value
      here is `0x71` = 113. So the section is neither a populated guard table nor blank padding:
      it carries twelve small integers whose meaning is **not established here**.
      **And the load config settles the CFG half of the question outright.** At RVA `01BCBE40`
      (`.rdata`, size 148): `GuardCFFunctionTable` = **0**, `GuardCFFunctionCount` = **0**, while
      `GuardCFCheckFunctionPointer` = `008C31C0` and `GuardCFDispatchFunctionPointer` = `008C31C8`
      are both **set**. `GuardFlags` = `0x00000100` — `CF_INSTRUMENTED` **without**
      `CF_FUNCTION_TABLE_PRESENT` (`0x400`). The check and dispatch machinery is linked and the
      target list is absent **by declaration, not by omission**: a link that had merely failed to
      finish would not clear the table-present flag while keeping the instrumentation flag.
      This confirms §'s reading from the load config itself rather than from the section size.
- [x] Which build flag combination produces `CF_INSTRUMENTED` with an empty table — `/guard:cf`
      compile without `/guard:cf` link is the likely cause but is not proven here. **S-2.**
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5), by reconstruction plus the static headers: a link WITHOUT `/guard:cf`, with
      `/DYNAMICBASE:NO`.** See "`S-2` by reconstruction" below. That combination reproduces all three
      header fields exactly: DllCharacteristics `0x8120`, GuardFlags `0x100`, and an empty table. The game code's
      own compile flags do not matter, because the CRT's guard-aware objects set `CF_INSTRUMENTED`. A `/guard:cf`
      link builds the table even with ASLR off.
      *Narrowed 2026-09-22 (FABLE), and the stated cause is refuted:* ~~the link **did** have
      `/guard:cf` — the `.gfids` section and both guard pointers are linker products that a
      non-`/guard:cf` link never emits.~~ *Corrected 2026-09-26 (FABLE, Claude Opus 5.5): the image's own POGO record
      lists the `.gfids` content as the INPUT contribution `.gfids$y` and the two guard pointers as the CRT's `.00cfg`
      input, so neither shows how the link was run; the refutation rests on `GuardFlags` alone, and the
      compile-without-link reading is not excluded (see "The debug directory" below).* What is absent is **`DYNAMIC_BASE`**: `DllCharacteristics`
      is `0x8120`, carrying `HIGH_ENTROPY_VA` but **not** `DYNAMIC_BASE` and **not** `GUARD_CF`,
      while `.reloc` is fully present. See the section above.
- [x] What the 145 guard adapters would have guarded — the `.data` pointers they load are not
      yet identified. **S-3.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (S-3):* **nothing; they are not guard
      adapters.** Each is an `atexit` teardown (one reference each, the argument to `00808B90`). It hands its static to
      an empty destructor, which the linker folded onto the `ret` that also serves as `_guard_check_icall`.
      - 144 statics are the nodes of Phyre serialization's 12 × 12 scalar-type conversion tree. The sentinel is
        `01F2CDA0` and the lookup is `0059A030`. The types run from `bool` through `double`, and there are 68 routines.
      - One static is the 0x28-byte record `02D3E880`.
      
      See *The 145 guard adapters are dead code* (corrected) and `members/guard-adapter-registrars.tsv`.
- [x] ~~Whether the TLS directory (40 bytes, `.tls` 512 bytes) carries callbacks that run before
      `main`. **S-4 — relevant to injection timing.**~~ **Answered (the register's `S-4` verdict, re-derived 2026-09-14,
      FABLE): no callbacks.** The data directory entry 9 gives the TLS directory at RVA `0x1BCBED8`, 40 bytes. It points to
      raw data `03004000`–`03004008` (the 8 bytes `00 00 00 00 00 00 00 80`), the index at `02EAED3C`, and
      `AddressOfCallBacks` = `008C56B0`. The first qword there is **0**, so the callback list is empty. The array lies in
      `.rdata` (characteristics `0x40000040`, not writable). The `.tls` section is 9 bytes virtual, at RVA `0x2EE4000`, which is `03004000`. TLS
      *storage* is used; no code runs from the TLS directory before the entry point.
- [x] Whether `__report_gsfailure` is reachable in a way a mod could trip accidentally. **S-5.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (S-5):* **yes, but only through a
      cookie mismatch, and three ways lead there.** The sole caller is `__security_check_cookie`'s mismatch tail
      `00808C5C`, and nothing takes the reporter's address. (1) A buffer overrun in any of the 2,209 protected functions
      (2,390 check sites). (2) A detour that returns into a protected frame with a different `rsp` or a clobbered cookie
      slot, because the check compares `cookie ^ rsp`. (3) **Any write to `01F44830` after boot.** Its one writer is
      `__security_init_cookie`, so a mod that scribbles that `.data` quadword kills the process at the next return from
      every protected frame then live. Either way no game minidump is written: the fallback clears the process filter
      first. The sibling `__report_rangecheckfailure` fast-fails with code 8 from 237 sites. Of six game-side guards read,
      three are dead, two fire only on engine-issued values whose producers are unread, and one is untraced. See
      *The stack cookie, read end to end*.

## `S-2` narrowed — the link DID have `/guard:cf`; what is absent is ASLR (FABLE, 2026-09-22)

> *Corrected 2026-09-26 (FABLE, Claude Opus 5.5): this heading's first clause is withdrawn as a proof, and kept as history.* Two of
> the three "linker products" below are input contributions in the image's own POGO record, so they do not show
> how the link was run. See "The debug directory" after this section. The ASLR half stands.

**Every load-config figure above reproduces**, re-read from the image as a control before anything
new was added: `GuardCFCheckFunctionPointer` `008C31C0`, `GuardCFDispatchFunctionPointer`
`008C31C8`, `GuardCFFunctionTable` **0**, `GuardCFFunctionCount` **0**, `GuardFlags`
**`0x00000100`** — `CF_INSTRUMENTED` alone. The `.gfids` section's twelve integers reproduce too:
`49 48 19 10 13 16 69 113 10 98 55 11`, the largest being the `113` this page names.

### The stated hypothesis is refuted by three linker products (FABLE, 2026-09-22)

`S-2` proposes *“`/guard:cf` compile without `/guard:cf` link”*. **That cannot be what happened,
because all three of the things only a `/guard:cf` LINK emits are present:**

| artefact | present? | who emits it |
|---|---|---|
| a **`.gfids`** section (48 B virtual, 512 raw) | **yes** | ~~the linker, and only under `/guard:cf`~~ *an input contribution, `.gfids$y` (POGO, 2026-09-26)* |
| `GuardCFCheckFunctionPointer` / `DispatchFunctionPointer` | **yes**, both set | ~~the linker~~ *the CRT's `.00cfg` input contribution (POGO, 2026-09-26)* |
| `CF_INSTRUMENTED` in `GuardFlags` | **yes** | the linker |

~~*A link that never saw `/guard:cf` produces none of the three.* **So the compile/link mismatch is
the wrong axis.**~~
*Corrected 2026-09-26 (FABLE, Claude Opus 5.5).* The first two rows are input sections that any link containing those objects
carries (`debug_directory.py` D3). Only `GuardFlags` is the linker's own word, and what sets
`CF_INSTRUMENTED` without a function table is toolchain behaviour this image cannot show. So the compile-versus-link
axis is open again, beside the `/DYNAMICBASE` axis below, not replaced by it.

### What IS missing, and it is not CFG (FABLE, 2026-09-22)

**`DllCharacteristics` is `0x8120`** — `HIGH_ENTROPY_VA` + `NX_COMPAT` + `TERMINAL_SERVER_AWARE`.
Two bits that ought to be there are not:

- **`IMAGE_DLLCHARACTERISTICS_GUARD_CF` (`0x4000`) is clear.** That is the bit the *loader* reads to
  turn CFG on; without it the instrumentation in the code is inert whatever the load config says.
- **`IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE` (`0x40`) is clear — the image is not ASLR-enabled** —
  **while `.reloc` is fully present** (234,336 bytes, the base-relocation directory populated, and
  `RELOCS_STRIPPED` **not** set in `Characteristics`). *Relocations were kept and ASLR was still
  turned off.*

> **`HIGH_ENTROPY_VA` without `DYNAMIC_BASE` is inert, and that is the tell.** High-entropy ASLR
> only means anything when ASLR is on. A build that never asked for ASLR would not carry the
> high-entropy bit either. **The shape is a default-hardened link with `/DYNAMICBASE` explicitly
> switched off**, not a build that forgot to harden.

> ~~**So the best-supported model is `/guard:cf` together with ASLR disabled**, and CFG cannot operate
> on a non-relocating image — which is consistent with the function table being declared absent
> while the instrumentation stays.~~ *Corrected 2026-09-26 (FABLE, Claude Opus 5.5): reconstruction refutes this. A
> `/guard:cf` link with `/DYNAMICBASE:NO` builds a function table and sets `GUARD_CF` (`cfg_link_matrix.py` X3).
> The image's signature is instead what a link without `/guard:cf` produces (X1, X2).* *Stated as the model the image supports.* **Naming the exact
> switch spelling is toolchain knowledge this image cannot settle alone**, so `S-2` stays open; what
> is settled is that its stated hypothesis is not the answer and the `/DYNAMICBASE` axis is.

## The debug directory — what the image records about its own build (FABLE, Claude Opus 5.5, 2026-09-26)

The PE debug directory (data directory 6) has four entries, and this page had read none of them. Control:
[`members/debug_directory.py`](members/debug_directory.py) (5 checks, FAILS 0). It reproduces the load-config
figures above before reporting anything.

| entry | what it says |
|---|---|
| CodeView (type 2), `RSDS` | the build's PDB was `E:\Jenkins\workspace\C11019P16003\Code\source\FF12_PS2_IN\FF12\x64_Retail\FF12X64.pdb`. It is a build-machine path, and the PDB does not ship. |
| VC_FEATURE (type 12) | **1,296** C/C++ objects: **1,265** built with `/GS`, **89** with `/sdl`, **49** guard-aware (`guardN`), none older than VC++ 11 |
| POGO (type 13, `GCTL`) | the linker's list of section contributions, for example `.text$mn`, `.CRT$XCU`, `.rdata$r`, `.xdata`, `.00cfg`, `.gfids$y` |
| type 14 | empty (size 0) |

**What it settles.**
- **Only 49 of 1,296 objects were compiled guard-aware.** That agrees, from an independent record, with section
  9a's measurement that only the statically linked CRT consults the guard slot. The game's own code was not
  compiled with `/guard:cf`.
- **`.gfids` is an input contribution.** POGO lists it as `.gfids$y`, `0x30` bytes at RVA `0x02EE3000`, the
  section's first byte. So `T-9`'s twelve dwords are the guard-aware objects' `.gfids$y` data, not converted into
  RVAs.
- **The two guard pointers are an input contribution too.** POGO lists `.00cfg`, `0x10` bytes at RVA
  `0x007A31C0`, which is `0x008C31C0` less the image base: the check slot, with the dispatch slot as its second
  qword.
- So two of the three legs of the 2026-09-22 refutation of `S-2` are withdrawn (corrected in place above).

**What it does not settle.** Two questions are toolchain behaviour, and the image records neither:
- whether a link without `/guard:cf` still writes `CF_INSTRUMENTED` when guard-aware objects are present.
  *It does. This is settled by reconstruction in the next section, including when the only guard-aware objects
  are the CRT's.*
- whether a `/guard:cf` link with `/DYNAMICBASE:NO` leaves the `.gfids$y` input unconverted.

The build's command line would answer both. The RSDS record shows it lived on a Jenkins build machine. `S-2` ~~and~~
~~`T-9` stay~~ stays open *(answered: see `T-9` above, answered 2026-09-27; 2026-10-02, OPUS)*. **Static, headers read.**

## `S-2` by reconstruction — the signature is a link without `/guard:cf` (FABLE, Claude Opus 5.5, 2026-09-26)

**Evidence class: reconstruction with the local MSVC toolchain, kept separate from the static reading above.**
[`members/cfg_link_matrix.py`](members/cfg_link_matrix.py) compiles one C file, which holds a table of
address-taken functions, twice: with `/guard:cf` and without. It links the results seven ways and reads each
image's headers (4 checks, FAILS 0 on linker 14.51.36256).

| object | link flags | DllCharacteristics | GuardFlags | function table |
|---|---|---|---|---|
| `/guard:cf` | `/DYNAMICBASE:NO` | **`0x8120`** | **`0x100`** | **empty** |
| plain | `/DYNAMICBASE:NO` (static CRT, and DLL CRT) | **`0x8120`** | **`0x100`** | **empty** |
| `/guard:cf` or plain | `/guard:cf /DYNAMICBASE:NO` | `0xC120` (`GUARD_CF` set) | `0x10017500` | 52 entries |
| `/guard:cf` | (default) | `0x8160` (`DYNAMIC_BASE` set) | `0x100` | empty |
| `/guard:cf` | `/guard:cf` | `0xC160` | `0x10017500` | 52 entries |

**The first two rows are this image's signature, field for field. No other row is.**
- So `S-2`'s combination is a link without `/guard:cf`, with `/DYNAMICBASE:NO`. The second row shows the game
  code's own compile flags are irrelevant: `CF_INSTRUMENTED` comes from the CRT's guard-aware objects.
- That matches VC_FEATURE's **49** guard-aware objects out of 1,296, and section 9a's measurement that only the
  static CRT consults the guard slot.
- The third row refutes the 2026-09-22 model. Switching ASLR off does not empty the table.

**The limit, stated.** The game was linked by linker 14.0, build 24215 (VS2015 Update 3, from the Rich header),
which is not installed here. The one visible version difference is the `.gfids` section:
- the game's linker merged the objects' `.gfids$y` input into the image unconverted (the POGO record above);
- the local linker drops that input in a link without `/guard:cf`.

Both are what a link that did not process CFG does. So the difference is consistent with this answer and does not
compete with it. `T-9`'s twelve dwords are that pass-through.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `ImageBase = 0x00120000` | `IMAGE_OPTIONAL_HEADER64 +0x18`, parsed from the authorized EXE | 1 |
| ASLR is off | `DllCharacteristics = 0x8120`; `DYNAMIC_BASE (0x0040)` clear | 1 |
| CFG is not enforced | `GUARD_CF (0x4000)` clear; `GuardCFFunctionTable = 0`; `GuardCFFunctionCount = 0` | 1 |
| ~~CFG *was* compiled in~~ CFG was compiled into the statically linked CRT only *(corrected 2026-10-02, OPUS: the check thunk `00809958` has 11 call sites, all in CRT start-up bodies `008087C4`–`00809CD4`, and the dispatch slot `008C31C8` is never referenced)* | `GuardFlags = 0x100` = `CF_INSTRUMENTED`; `.gfids` section allocated | 1 |
| The check is a no-op | `0x0016D6A0` disassembles to `ret 0` | 1 |
| The dispatch is unvalidated | `0x00896270` disassembles to `jmp rax` | 1 |
| The 145 guard adapters do nothing | all 12 bytes: `lea rcx,[rip+d]` + `jmp 0x16D6A0`; three read, family size from the GFZ tag census | 1 / 3 |
| DEP is enforced | `NX_COMPAT (0x0100)` set | 1 |
| Stack cookies are live and per-process random | complete bodies of `__security_init_cookie` (`00809B8C`), `__security_check_cookie` (`00808C40`) and `__report_gsfailure` (`00809654`); init reached from `entry` (`00808EE4`), the PE `AddressOfEntryPoint` | 1 |
| No section is writable **and** executable | all ten section `Characteristics` dwords re-read from the section table | 1 |
| Relocations are shipped, not stripped | file `Characteristics = 0x0022`, `RELOCS_STRIPPED (0x0001)` clear; `.reloc` virtual size `0x39360` | 1 |
| Section layout | PE section table | 1 |
| EXE provenance | SHA-256 of the parsed file matches the authority SHA | 1 |

**Every claim on this page was derived from the shipping binary in this session** — the PE
headers, the load config directory, and disassembled instruction bytes. None of it relies on a
GFZ annotation, and none of it relies on `.pdata` or unwind data, which the evidence standard
bans as proof.

**One reading correction worth recording.** The first pass flagged `0x0016D6A0` as "not a bare
ret" because the test looked for opcode `0xC3`. The bytes are `C2 00 00` — `ret 0`, the
`imm16` form. Same behaviour, different encoding; the automated check was too narrow and the
disassembly settled it. A byte-pattern test that hard-codes one encoding of an instruction will
produce confident false negatives.

### What this binary is actually made of

Worth stating once, because it reframes the remaining work:

| Component | Functions | Share of 38,161 |
|---|---|---|
| Compiler-generated EH unwind funclets | 3,813 | 10.0 % |
| Phyre reflection | 4,557 | 11.9 % |
| Phyre ScriptVM bindings | 1,219 | 3.2 % |
| Other Phyre | 993 | 2.6 % |
| **Combined** | **10,582** | **27.7 %** |

More than a quarter of the executable is generated glue and compiler artifacts rather than game
logic. A coverage percentage that counts these equally with a combat formula is measuring the
wrong thing.

## 9a. Which code is instrumented - measured 2026-09-19 (FABLE)

**Only the statically linked CRT.** A guard check is a call *through* the pointer slot the load config names,
`008C31C0`. A rip-relative sweep of the image finds **one** instruction that references that slot: the thunk
`jmp [008C31C0]` at `00809958`. That thunk has **eleven** call sites, and every one is in a CRT body between `008087C4`
and `00809CD4` - the scalar deleting destructor (twice), the two EH vector iterators, `__ArrayUnwind`,
`_Init_thread_notify`, `_Init_thread_wait` and four unnamed neighbours. *The last of them, `00809CD4` (74 B, read whole),
shows what a real check looks like: a table walker that, for each non-null pointer, **calls the thunk with the target in
`rcx` and then calls the target** - an indirect call guarded by an indirect check, the opposite of the direct calls
described next.*

**The direct callers of `0016D6A0` are something else.** 2,528 `call` and 340 `jmp` sites reach `0016D6A0` directly, and 22
more through the forwarder `0017E7D0`. A direct call never consults the slot, so none of them is a guard check - and
their arguments say what they are: a boolean made by `setne cl` in the `GiPrim` draw, a render record in one of the
render-record dirty-state handlers, the constant 1 in the `GiPrim` constructor (sites named in the commit that added
this section, not cited here, because this page does not explain those bodies). They are **calls to empty functions** - asserts, debug hooks, routines compiled out of
this build - which the linker folded onto the same three bytes (`C2 00 00`) that serve as the guard's default body.
That is also why a direct call to `0016D6A0` is sometimes followed by an indirect call and sometimes not: the two are
unrelated.

**So the game's own indirect calls are not instrumented at all**, not even nominally; "instrumented and inert"
describes the CRT. For a reader of any other page: **a body that "dispatches through `0016D6A0`" by a direct call or
jump dispatches to nothing.**

## 10. B-2/f — is anything else nominal? (2026-09-07)

CFG is instrumented and inert. The obvious follow-up, opened as **B-2/f**, is whether the rest of
the hardening posture is nominal too — a build that ships a disabled CFG might plausibly be
careless elsewhere. **It is not. CFG is the only nominal protection in this image.** Every other
mechanism was re-derived from the shipping EXE and each one is real.

The prior that motivated the question pointed the wrong way, and that is worth saying: the maths
document established that this build is `/fp:precise` with no fast-math relaxation and ships no
app-local CRT, which reads as an untuned build. Untuned is not the same as unhardened. The posture
here is **coherent and deliberate**, not sloppy.

### The verdict, mechanism by mechanism

| mechanism | status | what settles it |
|---|---|---|
| **CFG** | **nominal — instrumented, never activated** | check body is `ret 0`; `GuardCFFunctionTable = 0`, `GuardCFFunctionCount = 0`, `GuardFlags = 0x00000100` (`CF_INSTRUMENTED` only); `GUARD_CF` absent from `DllCharacteristics` |
| **ASLR** | **off — deliberately, not by omission** | `DYNAMIC_BASE` clear **and** relocations shipped: `RELOCS_STRIPPED` is **not** set and `.reloc` carries `0x39360` bytes. A build that had simply forgotten ASLR would usually have stripped them |
| **DEP** | **genuinely enforced** | `NX_COMPAT` set, and **no section in the image is both writable and executable** — the whole section table was re-read for this |
| **Stack cookies** | **genuinely live and per-process random** | the init, check and failure bodies were all read; see below |

`DllCharacteristics = 0x8120` = `HIGH_ENTROPY_VA | NX_COMPAT | TERMINAL_SERVER_AWARE`. The absence
of `GUARD_CF` alongside compiler-emitted `_guard_check_icall` calls is the signature of `/guard:cf`
reaching the **compiler** but not the **linker** — the instrumentation is paid for and never
switched on.

### The section permission sweep

Re-read from the section headers, because "DEP is on" is worth nothing if a writable page is also
executable:

```
.text    R-X    .rdata   R--    .data    RW-    .pdata   R--    .rodata  R--
.gfids   R--    .tls     RW-    _RDATA   R--    .rsrc    R--    .reloc   R--
```

**No `W+X` section.** DEP has nothing to work around inside the image, so a mod that wants to
execute its own bytes genuinely needs `VirtualProtect` or an execute-flagged `VirtualAlloc`.

### The stack cookie, read end to end

Three bodies, and all three are complete MSVC implementations rather than stubs.

**`__security_init_cookie` (`00809B8C`, 172 B)** — called from exactly one place, `entry`
(`00808EE4`), which is the PE `AddressOfEntryPoint` (RVA `006E8EE4`). It runs before anything else
in the process:

```c
if (*(u64*)0x01F44830 == 0x00002B992DDFA232) {     // still the compile-time default?
    FILETIME ft; GetSystemTimeAsFileTime(&ft);
    u64 v  = *(u64*)&ft;
    v     ^= (u64)GetCurrentThreadId();
    v     ^= (u64)GetCurrentProcessId();
    LARGE_INTEGER pc; QueryPerformanceCounter(&pc);
    u64 r  = ((u64)pc.HighPart << 32) ^ (u64)pc.QuadPart ^ v ^ (u64)&v;   // &v = a stack address
    r     &= 0x0000FFFFFFFFFFFF;                    // 48 bits
    if (r == 0x00002B992DDFA232) r = 0x00002B992DDFA233;   // never ship the default
    *(u64*)0x01F44830 = r;
}
*(u64*)0x01F44838 = ~r;                             // the complement
```

**48 bits of entropy**, mixed from the wall clock, the thread id, the process id, the performance
counter and the address of a stack local. The on-disk value at `01F44830` is the MSVC default
`0x00002B992DDFA232` — as it should be; it is overwritten before `main`.

**`__security_check_cookie` (`00808C40`, 33 B)** — 2,209 direct callers, and it is a real check:

```asm
00808C40  cmp  rcx, qword ptr [01F44830]   ; the frame's cookie vs the process cookie
00808C47  bnd jne  00808C5C                ; mismatch -> fail
00808C4A  rol  rcx, 0x10                   ; also reject a cookie whose top 16 bits
00808C4E  test cx, 0xffff                  ;   are non-zero (the 48-bit invariant)
00808C53  bnd jne  00808C58
00808C56  bnd ret                          ; OK
00808C5C  jmp  __report_gsfailure          ; 00809654
```

Compare that with the CFG check at `0016D6A0`, whose entire body is `C2 00 00`. **Same build, same
compiler, one mechanism wired up and one not** — which is the cleanest available demonstration that
the CFG situation is a deliberate configuration choice rather than a broken toolchain.

**`__report_gsfailure` (`00809654`, 209 B)** — also real. It asks
`IsProcessorFeaturePresent(PF_FASTFAIL_AVAILABLE)` and, if available, executes `int 0x29` with
`ecx = 2` (`FAST_FAIL_STACK_COOKIE_CHECK_FAILURE`), which terminates the process immediately with no
exception handling and no chance to intercept. Otherwise it captures the context and takes the
unhandled-exception path.

*Read to the end 2026-09-14 (FABLE).* The fallback is `__raise_securityfailure` (`00809620`, called at
`0080971B`), and its first act is `SetUnhandledExceptionFilter(NULL)` (`00809629` `xor ecx, ecx`, `0080962B`, import
slot `008C2250`). Only then does it call `UnhandledExceptionFilter` (`00809634`, slot `008C23C0`) on a synthesised
`STATUS_STACK_BUFFER_OVERRUN` (`0xC0000409`) record, and finally `TerminateProcess(GetCurrentProcess(), 0xC0000409)`
(`0080963A` / `0080964D`). **Neither path reaches the game's own crash filter `0079AD50`**: the fast-fail path never
raises an exception, and the fallback unregisters every process filter before it reports. A cookie failure therefore
leaves **no game minidump**
([what the game asks Windows for, CV-3](../Runtime-Service-Surface/what-the-game-asks-windows-for.md)).

**Reach.** In the raw call index (unlisted code included, `jmp` tails included) `__report_gsfailure` has exactly one
caller, the mismatch tail `00808C5C` of `__security_check_cookie`; `__security_check_cookie` has **2,390 call sites in
2,209 listed functions** and none in unlisted code. Outside `.pdata` no byte sequence in the file holds either
reporter's address, so nothing takes it indirectly. The cookie `01F44830` is read at 2,216 sites and written at one,
`__security_init_cookie`'s `00809C1C`; its complement `01F44838` is written at `00809C2B` and read only by
`__report_gsfailure` (`00809708`).

**A second fast-fail the question did not name.** `__report_rangecheckfailure` (`00809728`) calls
`__report_securityfailure(8)` (`0080973C`), which has the same two paths with `ecx = 8`
(`FAST_FAIL_RANGE_CHECK_FAILURE`, `int 0x29` at `00809758`) and the same filter-clearing fallback (`008097CD` →
`00809620`). The compiler emits it before a write through a fixed-size local or global array whose index it could not
bound. **237 call sites**: 113 listed functions plus 10 sites in unlisted code, and 209 of the 237 lie in
`007A0000`–`007F8000`, the block holding SEAD's `Voice::Initialize` (`007EBAD0`, 23 sites). Six game-side guards were
read:

| Guard | Bound | Index source | Can it fire? |
|---|---|---|---|
| `0026CA87` / `0026CAA5` (`ActorManager_BindLoadedDefinitionPayload`) | 8 | a loop counter bounded by 8 | no, dead |
| `00578635` (item-screen pane `00578450`) | 12 | a token count clamped to 12 by `cmovg` at `0057861C` | no, dead |
| `002A1C13` (`002A1B00`) | 128 | a string length from `002B2D90`, which masks the length byte with `0x7F` (≤ 127) | no, dead |
| `0032F883` (`ActorResource_OnDefinitionPayloadLoaded`) | 5 | the low nibble of the load callback's tagged argument (0–15), unchecked in the caller `003304A0` | only if the loader issues a tag ≥ 5; its producers are not read |
| `00332343` (`00332250`, script-container path) | `0x104` | the position of a `\` or `/` separator in a path copied **unbounded** (`003322E0` byte loop) from the runtime table `0215F000[kind][id]` into the stack buffer at `rsp+0x20` | only when that separator lies at offset ≥ 260; the copy itself reaches the cookie slot `rsp+0x240` only for a path of 544 bytes or more, and then the check at `00332384` fails too |
| `003F9C96` (`003F9720`) | 16 | not traced | not established |

None of the six is shown to take an index from authored file data.

### What this means for a mod

- **Do not smash stacks, and do not expect to catch it if you do.** The failure path is `int 0x29`,
  which is *not* an exception — a `__try`/`__except` or a vectored handler will not see it and the
  process is gone. That is stricter than an access violation. On a machine without fast-fail the
  fallback first calls `SetUnhandledExceptionFilter(NULL)`, so a filter the DLL installed is removed
  before it could run, and the game's minidump filter `0079AD50` never runs either.
- **Never write the cookie quadword.** `01F44830` has one writer, at boot. A stray write there
  fails every protected frame that is live at that moment, on its return.
- **A detour that grows a protected frame must preserve the cookie slot.** 2,209 functions check
  one, so the odds that a given hook target is `/GS`-protected are high.
- **The cookie is readable at a fixed address.** `01F44830` is at a known VA because ASLR is off, so
  injected code already inside the process can read the live cookie directly and does not need to
  defeat it — which is the practical reason `/GS` is a robustness feature here rather than a barrier
  to modding.
- **The relocations are shipped and correct.** `RELOCS_STRIPPED` is clear, so the image is
  relocatable in principle; nothing applies them because `DYNAMIC_BASE` is absent. A tool that
  wanted to rebase this image could.

### Falsification

*Killer observation named in advance:* find one hardening mechanism whose body is a stub while the
header advertises it — that is, reproduce the CFG result somewhere else. I read the init, the check
and the failure path for `/GS`, and swept every section's permission bits for DEP. **All three
cookie bodies are complete implementations and no section is W+X.** The attempt failed; the claim
stands.

The residual weakness is stated rather than hidden: **DEP and ASLR are enforced by the loader, not
by the image**, so `NX_COMPAT` set and `DYNAMIC_BASE` clear are statements about what this image
*requests*. Confirming what the OS actually does with the request needs runtime evidence (tier 10)
and has not been done. Nothing in the image can settle it.

## 9. Related

- [`../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) — where the `_guard_check_icall` branch appears, and why it does nothing
- [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) — the ban on `.pdata` / unwind data as proof
- [`../../_index/COVERAGE.md`](../../_index/COVERAGE.md) — the composition table above belongs in any reading of those numbers

## 9. Falsification pass 2026-09-02

**Attack chosen.** This document calls itself *"the single most useful page in this database for
anyone hooking FFXII"*, and every claim in it is a **PE header field** — so every claim can be
checked exactly, from the authorized binary, in one pass. A page that a modder will act on directly
deserves that.

### SURVIVED: every hardening claim, exactly

Read straight from the headers of the authorized EXE:

| Claim | Header value | |
|---|---|---|
| `ImageBase = 0x00120000` | `0x00120000` | ✅ |
| **no ASLR** | `DllCharacteristics = 0x8120`, `DYNAMIC_BASE (0x0040)` **absent** | ✅ |
| **DEP enforced** | `NX_COMPAT (0x0100)` **present** | ✅ |
| **CFG not enforced** | `GUARD_CF (0x4000)` **absent** | ✅ |
| `SecurityCookie = 0x01F44830` | load config `+0x58` | ✅ |
| `__guard_check_icall_fptr = 0x008C31C0` | load config `GuardCFCheckFunctionPointer` | ✅ |
| `0016D6A0` is `ret 0` | bytes `C2 00 00` | ✅ |

### STRENGTHENED: the load config proves "compiled in, shipped off" directly

§2 argues CFG was **compiled into** the image but **not enabled** at link time, from the nop stubs
and the dead guard adapters. The load-config **`GuardFlags`** field settles it without needing that
argument:

```
GuardFlags = 0x00000100   =  IMAGE_GUARD_CF_INSTRUMENTED
                             IMAGE_GUARD_CF_FUNCTION_TABLE_PRESENT (0x400) is NOT set
```

**The image declares itself CF-instrumented while carrying no guard function table.** That is
precisely "compiled in, shipped off", stated by the binary's own metadata rather than inferred from
instruction bytes.

### NEW: `HIGH_ENTROPY_VA` is set, and inert

`DllCharacteristics` also carries **`HIGH_ENTROPY_VA` (0x0020)**, which this document did not
record. It is **inert**: that flag only says *"if this image is randomised, use the full 64-bit
address space"*. With `DYNAMIC_BASE` absent nothing is randomised, so the image still loads at
`0x00120000` every time. Worth knowing only so that a reader who spots the flag does not conclude
ASLR is on.

### OVERTURNED: the section table listed RVAs as virtual addresses

Both section addresses in §2 are **relative virtual addresses**, not the VAs the rest of the
database uses:

| Section | Document said | Actual VA | Difference |
|---|---|---|---|
| `.reloc` | `0x02F3C000` | **`0x0305C000`** | `0x120000` |
| `.gfids` | `0x02EE3000` | **`0x03003000`** | `0x120000` |

**Each is short by exactly the image base.** The irony is sharp: §4 of this same document states
*"Ghidra VA equals runtime VA, because `ImageBase` is `0x00120000` and ASLR is off"* — the very
reason the two differ — and the project's `CLAUDE.md` states the convention outright: *"Ghidra/GZF
addresses for this binary are canonical virtual addresses — image base `0x00120000` is already
included. Do not add it again."* The section table added it never.

**Why this one matters more than most.** A modder attaching a debugger and going to `0x02F3C000`
lands 1.1 MB short of `.reloc`, inside ~~`.pdata`~~ `.data` *(corrected 2026-10-02, OPUS: by the corrected table below, `.data` spans `0x01DF0000`–`0x02F97530` and `.pdata` starts at `0x02F98000`)*. On the page that presents itself as the reference
for hooking, an address off by the image base is the worst kind of error to ship.

The size also needed a note: `.reloc` is **`0x39360`** virtual, which the document rounded to
`0x39400` — that is the file-aligned raw size, not the virtual size. Both are true of different
fields; the label was wrong.

### The complete section table, corrected

| Section | Virtual address | Virtual size |
|---|---|---:|
| `.text` | `0x00121000` | `0x7A0635` |
| `.rdata` | `0x008C2000` | `0x152D7FC` |
| `.data` | `0x01DF0000` | `0x11A7530` |
| `.pdata` | `0x02F98000` | `0x68A0C` |
| `.rodata` | `0x03001000` | `0x11C0` |
| `.gfids` | `0x03003000` | `0x30` |
| `.tls` | `0x03004000` | `0x9` |
| `_RDATA` | `0x03005000` | `0xA250` |
| `.rsrc` | `0x03010000` | `0x4B830` |
| `.reloc` | `0x0305C000` | `0x39360` |

`.gfids` being **48 bytes** rather than a populated guard table is a third independent confirmation
that CFG never shipped: the section exists, is allocated, and is far too small to hold a function
table for a 38,161-function image.

**One consequence worth propagating.** The residual document computes ".text is 2.25% of the image"
against a `.text` virtual size of `0x7A0800`. The true virtual size is **`0x7A0635`**; `0x7A0800`
is the aligned figure. The percentage is unaffected at two decimal places, so that document is left
as it stands, with this note as the record.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Audio — MECHANICAL, cited as a hardening example.**
  - `007EBAD0` is SEAD's `Voice::Initialize`, which the page cites for its 23 guard sites. Its 32 callees and its
    300-byte caller are Audio-filed.
  - The 25-byte zeroing helper `005CC8A0` is also called by five Audio-filed bodies of 97–448 bytes.

  None of those edges is a hardening mechanism.
- **Platform — CLIENT and SERVICE.**
  - `005CC8A0` is also called by a 1,101-byte Platform body.
  - The crash filter `0079AD50` calls the resource lookup `0019A510` (`FindResourceW`)
    ([the Phyre application page](../../22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md)
    §7a names the same lookup at start-up).

## The `00808EE4` exclusive subtree — the image `entry` point bound (SWE2-FRONTIER, followup queue)

`00808EE4` (`entry`, ~20 B) — the PE entry point: `sub rsp, 0x28`,
`call 00809B8C` (CRT pre-init), `add rsp, 0x28`, then `jmp 00808D78`
into the main CRT startup tail
(`00808EE8`/`00808EED`/`00808EF1`).

| member | role | interior |
| --- | --- | --- |
| `00809B8C` | CRT pre-init callee | [`00809B8C`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00808D78` (the post-init tail).

## SWE2-EC7-45 update (2026-09-19) - `00594EB0`

`00594EB0` (238 B) is a call-free strided double-to-float converter - `[r8]` count, `[r8+4]`/`[r8+8]` src/dst strides, `byte[r8+0xC]` `cmovne` base select between `[rax+8]`/`[rax+0x48]`; 4-unrolled `movsd`/`cvtpd2ps`/`movss` + scalar tail. Interior anchor `00594F20` (the unrolled loop head).

## SWE2-EC7-47 update (2026-09-19) - `00594350`

`00594350` (219 B) is a call-free strided float-to-double converter - mirror sibling of `00594EB0`: same `[r8]` count, `byte[r8+0xC]` `cmovne` base select, 4-unrolled `movss`/`cvtps2pd`/`movsd` + scalar tail. Interior anchor `005943B2` (the unrolled loop head).

`00578120` (118 B) is the chain harvest `00578450` (item-screen pane) runs: from `rcx` it repeatedly calls `002B39A0(cur, 2)` for the next node, steps `cur++`, probes `002B39A0(cur, 3)` and steps once more when that returns `cur` itself; each visited node is stored into `rdx[i]` and the loop ends when the walker yields null — returns the count `edi`, 0 on a null start. (The `00578450` caller sits on the presentation side — the item-screen pane — a crossing this page cites for the census table, not a hardening relationship it owns.)

Interior anchor `00578160` (function `00578120`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

The stack-cookie census cites the functions whose buffers it tested, so their callers arrive with them. None of
them is a hardening relationship.

- **ActorEntity — CLIENT, 19 edges.**
  - `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (`003304A0`), cited for the unchecked tag nibble, is
    called by `ActorResource_BeginPrimaryPayloadLoad`.
  - It calls `ActorResource_FinalizeManagerRuntimeAfterLoads`, `ActorResource_OnDefinitionPayloadLoaded` and the
    `0032FA10`-`0032FB70` loaders.
  - The script-container path `00332250` is called from `ActorResource_BeginPrimaryPayloadLoad` and `003306E0`.
- **UI, 5, and WorldAreaField, 1 — CLIENT.** `003F9720`, an untraced cookie site, is a widget body. It calls
  `003F8FE0`, `003F9270`, `003F92B0`, `003F9390` and `WorldTransition_GetActiveOrPendingFieldId`, and is called by
  `003F8EC0`.
- **Presentation — MECHANICAL, two edges.** The item-screen pane `00578450` calls both `xmlStrchr` (`002B39A0`) and the
  chain harvest `00578120`.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 slice OPUS-P22-SLICE-24-99).*
