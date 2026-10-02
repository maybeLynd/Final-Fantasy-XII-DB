# Reconstruction readiness — `FFXII TZA/24-Compiler-And-CRT-Runtime/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-24-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`34861cfd`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. Several pages in this folder are being edited by other lanes; every quotation is of the snapshot text. |

**Counts:** COUNTS-PLACEHOLDER

Citation form: `ABBREV:line`, where the abbreviation stands for a page path relative to
`FFXII TZA/24-Compiler-And-CRT-Runtime/`. Line numbers are those of the snapshot file.

| abbrev. | page | lines |
|---|---|---:|
| `README` | `README.md` | 64 |
| `SI` | `Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md` | 950 |
| `LZ` | `Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md` | 808 |
| `ST` | `Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md` | 298 |
| `EH` | `Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md` | 1,063 |
| `OBJ` | `Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md` | 1,126 |
| `OC` | `Cxx-Runtime-Families/the-ordered-container-runtime.md` | 594 |
| `MS` | `Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md` | 393 |
| `GEN` | `Generated-Families/generated-function-families.md` | 315 |
| `RV` | `Generated-Adapters/the-return-value-adapter-family.md` | 498 |
| `MEM` | `Memory-And-Allocation/where-the-games-memory-comes-from.md` | 1,982 |
| `TH` | `Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md` | 824 |
| `RS` | `Runtime-Service-Surface/what-the-game-asks-windows-for.md` | 577 |
| `HARD` | `Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md` | 888 |
| `MATH` | `Maths-Library/the-maths-the-game-runs-on.md` | 897 |

"Not stated" means none of the 15 pages says it. Where a point is made only on a page outside this category
(for example the register `_index/OPEN-QUESTIONS.md`), it is given as a path from `FFXII TZA/` and marked as
outside the audited set.

## Pages read

All 15 `.md` files were read in full (11,277 lines). Member `.tsv` files (and the one `.txt`) were opened only
to confirm layouts and row counts. No item below rests on a `.tsv` alone. Where a `.tsv` disagrees with its
page, that is reported as a contradiction and not resolved.

The category `README` indexes only 5 of the 14 system pages (`README:13-47`): `HARD`, `SI`, `LZ`, `OBJ`, `EH`.
`ST`, `OC`, `MS`, `GEN`, `RV`, `MEM`, `TH`, `RS` and `MATH` are not linked from it.

| page | front matter as the page states it | README / in-body banner that differs |
|---|---|---|
| `SI` | `status: AUDITED` (`SI:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-02` (`:18`); `passes: 5`, `reopened_count: 1` (`:20`, `:24`) | `README:19` "**DOCUMENTED, tier 1.**"; heading `## 12. REOPENED and corrected 2026-09-02 (fourth pass)` (`SI:807`); body dated to 2026-09-29 (`SI:926`) |
| `LZ` | `status: AUDITED` (`LZ:4`); `evidence_tier: 1`; `last_reviewed: 2026-09-02` (`:18`); `passes: 1` (`:20`) | `README:25` "**DOCUMENTED, tier 1, one falsification pass.**"; body dated to 2026-09-29 (`LZ:783`) |
| `ST` | `status: DOCUMENTED — … (UQ-329), the +0x20 flag (UQ-330) and the atexit-ordering question (UQ-331 …) answered 2026-09-17; the owners of the 224 list heads (UQ-329) and the +0x20 flag (UQ-330) answered 2026-09-17` (`ST:4`; the UQ-329/330 clause is written twice); `last_reviewed: 2026-09-13` (`:11`); `crossref_clean: false` (`:20`) | family rows edited to 2026-10-01 (`ST:46`) |
| `EH` | `status: AUDITED` (`EH:4`); `evidence_tier: 1 (one group of 128 relies on tier 8 for its *identity*, see §8)` (`:6`); `last_reviewed: 2026-09-02` (`:18`); `passes: 1` (`:20`) | `README:43` "**DOCUMENTED, tier 1, one falsification pass.**"; sections dated to 2026-09-29 (`EH:1045`); one update section dated "2026-05-15" (`EH:1019`) |
| `OBJ` | `status: AUDITED` (`OBJ:4`); `last_reviewed: 2026-09-02` (`:19`); `passes: 2` (`:21`); `origin: … 915 functions` (`:26`) | `README:34` "**DOCUMENTED, tier 1, one falsification pass.**"; in-body "`DOCUMENTED`, one falsification pass." (`OBJ:558`) and "`DOCUMENTED`, two falsification passes." (`OBJ:617`); body dated to 2026-09-29 (`OBJ:1092`) |
| `OC` | `status: AUDITED — every register row is closed …` (`OC:4`); `last_reviewed: 2026-09-30` (`:12`); `promoted: 2026-10-01 DOCUMENTED -> AUDITED` (`:20`) | `OC:21` "measured A on this DOCUMENTED page" (2026-09-30); section banner "*Tier 2:" (`OC:593`) vs `evidence_tier: 1` (`OC:6`) |
| `MS` | `status: AUDITED — every register row is closed …` (`MS:4`); `readiness: BEHAVIORALLY UNDERSTOOD (2026-09-30, OPUS)` (`:5`); `last_reviewed: 2026-09-30` (`:20`); `promoted: 2026-10-01` (`:28`) | `MS:9` "Was, 2026-09-15: SEMANTICALLY IDENTIFIED … superseded by SD-80"; "*Tier 2:" (`MS:393`) |
| `GEN` | `status: DOCUMENTED — the fifty-five families are catalogued and every register row is closed …` (`GEN:4`); `last_reviewed: 2026-09-29` (`:11`); `last_pass: 2026-09-13` (`:14`); `crossref_clean: false` (`:20`) | rows edited 2026-09-30 / 2026-10-01 (e.g. `GEN:24`, `:31`) |
| `RV` | `status: AUDITED` (`RV:4`); `last_reviewed: 2026-09-08` (`:19`); `last_pass: 2026-09-13` (`:22`) | no `promoted:` line, unlike `OC:20`/`MS:28`; body dated to 2026-10-02 (`RV:212`) |
| `MEM` | `status: REOPENED` (`MEM:4`); `last_reviewed: 2026-09-12` (`:18`); `passes: 1`, `reopened_count: 0` (`:20`, `:24`); `crossref_clean: false` (`:23`); `external_production: … date: 2026-09-23 … status: "locally validated; formal independent acceptance pending"` (`:25-29`) | "Historical audit receipts above do not certify this new production." (`MEM:1901`); body dated to 2026-10-02 (`MEM:1509`) |
| `TH` | `status: AUDITED — BU-1 closed 2026-09-18 as NO ADMISSIBLE SOURCE …` (`TH:4`); `last_reviewed: 2026-09-13` (`:19`); `passes: 3`, `last_pass: 2026-09-03` (`:21-22`) | "## 12. Audit pass 3 - 2026-09-13 (OPUS)" (`TH:550`) vs `last_pass: 2026-09-03`; "Superseded readings:** none — this is the document's first version." (`TH:380`) beside "OVERTURNED in section 10" (`TH:79`); body dated to 2026-09-29 (`TH:814`); not indexed in `README` |
| `RS` | `status: AUDITED` (`RS:4`); `last_reviewed: 2026-09-07` (`:19`); `passes: 1`, `last_pass: 2026-09-07`, `last_pass_kind: attack` (`:21-24`) | body sections dated 2026-09-12 to 2026-09-29 (`RS:218`, `:250`, `:387`, `:393`, `:259`, `:573`); not indexed in `README` |
| `HARD` | `status: AUDITED` (`HARD:4`); `last_reviewed: 2026-09-07` (`:19`); `passes: 2`, `reopened_count: 1` (`:21`, `:25`); `last_pass_state: b57264ba…` (`:23`), which is `MATH`'s snapshot hash (`MATH:16`), not `HARD`'s own `46f02e26…` (`HARD:9`) | `README:14` "**DOCUMENTED, tier 1.**"; body dated to 2026-09-29 (`HARD:870`); family row edited 2026-09-30 (`HARD:27`) |
| `MATH` | `status: AUDITED` (`MATH:4`); `last_reviewed: 2026-09-12` (`:18`); `last_pass: 2026-09-07` (`:21`) | "`status` unchanged at **DOCUMENTED**" (`MATH:778`); body dated to 2026-09-29 (`MATH:862`) |
| `README` | "Functions \| ~5,150" (`README:8`) | indexes 5 of 14 pages (`README:13-47`) |

## 1. Interface

This category is not one engine system. It is the toolchain and runtime substrate that every other system runs on:
- CRT start-up and static initialisation;
- lazy statics and their lock;
- C++ exception unwind;
- object deletion;
- the two red-black tree runtimes;
- generated adapter families;
- the engine's own memory arena;
- the thunk layer;
- the Windows service surface;
- image hardening;
- the maths library.

A port has a choice for each sub-system: reproduce its *behaviour* (the arena, the trees, the maths, the start-up
order), or replace it with the port's own runtime and keep only the observable contract. The pages are written for
both readers. The map below therefore records the interface each page gives. §2 lists what a behavioural port still
needs.

Sub-systems mapped (§1.1-§1.11):

| § | sub-system | pages |
|---|---|---|
| 1.1 | process entry, CRT start-up and the eager initialiser table | `SI`, `ST`, `OBJ`, `HARD` |
| 1.2 | lazy ("magic") statics and the one-time-init lock | `LZ`, `SI`, `EH` |
| 1.3 | static teardown and process exit | `ST`, `OBJ`, `EH` |
| 1.4 | C++ exception handling and unwind funclets | `EH` |
| 1.5 | object deletion: the deleting-destructor contract | `OBJ`, `GEN` |
| 1.6 | the engine memory arena and the CRT allocation routes | `MEM` |
| 1.7 | ordered containers: EASTL rbtree and MSVC `std::_Tree` | `OC`, `MS` |
| 1.8 | generated families and the return-value adapter | `GEN`, `RV` |
| 1.9 | the thunk layer and the Windows service surface | `TH`, `RS` |
| 1.10 | image hardening: ASLR, CFG, DEP, `/GS` | `HARD` |
| 1.11 | the maths library | `MATH` |
| 1.12 | dependencies on other categories (summary) | all |

### 1.1 Process entry, CRT start-up and the eager initialiser table

#### Entry points

| function | role as stated | caller | cite |
|---|---|---|---|
| `00808EE4` `entry` (18 B, RVA `006E8EE4`) | `sub rsp,0x28; call 00809B8C; add rsp,0x28; jmp 00808D78` | Windows loader | `SI:489-490`; `HARD:620`, `:847-850` |
| `00809B8C` `__security_init_cookie` (172 B) | "the FIRST call in the process" | `entry` only | `SI:491`; `HARD:619-635` |
| `00808D78` CRT start-up (330 B) | runs both initialiser tables, then WinMain | `jmp` from `entry` | `SI:492`; `EH:998` |
| `0080893C` `__scrt_initialize_crt`; `00808900` / `00808AF0` acquire / release start-up lock | — | `00808D78` | `SI:493-497` |
| `00862022` `_initterm_e` | runs the C table `__xi` (3 entries); may fail with `0xFF` | `00808D78` at `00808DDB` | `SI:495`, `:660`, `:679-681` |
| `0086201C` `_initterm` | runs the C++ table `__xc` (1,172 entries); no failure path | `00808D78` at `00808DFC` | `SI:496`, `:665` |
| `00808C90`, `00808D4C`, `00809124` | the three C initialisers; `00809124` creates the lazy-static lock `02EAED40` | `_initterm_e` | `SI:675`; `LZ:483-490` |
| `00808D5C` | first C++ initialiser; calls `_set_new_mode(0)` through thunk `00862046` | `_initterm` | `MEM:95`, `:500` |
| `0015BCD0`, `0015C540` | construct-and-`atexit` initialisers | `_initterm` | `SI:67-79`, `:177` |
| `0015BD30` (484 B), `0015BF20` | prototype-copy initialisers (`.data` → `.data`) | `_initterm` | `SI:87-96`, `:178`, `:913` |
| `0086203A` `_register_thread_local_exe_atexit_callback`; `00862016` `_get_narrow_winmain_command_line` | — | `00808D78` | `SI:498-499` |
| `007A3770` (45 B) | "WinMain shim"; call site `00808E8A`; EH calls it "the game `main` equivalent" | `00808D78` | `SI:500`, `:538`; `EH:1015` |
| `007980A0` (2,153 B) | "the program's **main body**", 56 direct calls; ends in `ExitProcess(0)` at `0079887F` | `007A3770` | `ST:156`, `:164-167` |

#### Inputs, outputs and record layouts

| item | layout / value | cite |
|---|---|---|
| C++ initialiser table `__xc` | `void(*)(void)` qwords, stride 8; "VA 0x008C31D8" … `0x008C5678`, 1,172 entries; but `__xc_a` = `008C31D0` (see §3, X-1) | `SI:52-54`, `:190-194`, `:663-664`, `:672` |
| C table `__xi` | `008C5680` – `008C56A0`, 3 entries | `SI:658-659`, `:671` |
| link order | not sorted ("51 % ascending steps"); intra-TU ordered, slots 356–365 | `SI:463-468`, `:710-713` |
| TLS directory | RawDataStart `0x03004000`, End `0x03004008`, AddressOfIndex `0x02EAED3C`, AddressOfCallBacks `0x008C56B0` (empty: **zero TLS callbacks**), Characteristics `0x00300000` | `SI:137-152`, `:196-202`; `HARD:371-375` |
| per-thread block | `+0x04 i32 _Init_thread_epoch`; template value `0x80000000` | `SI:204-205`, `:340-341` |
| start-up state `02EAECF8` | 0 untouched, 1 in progress (written `00808DC3`), 2 complete (written `00808E01`) | `SI:682-689` |
| `__security_cookie` `01F44830` | ships `0x00002B992DDFA232`; replaced before `main` (algorithm in §1.10); complement at `01F44838` | `SI:509-510`; `HARD:624-640` |
| prototype copies | 320 B from 20 sources → 6,692 B at 86 destinations; binding profiles assembled at `01DF1738 + i*0x15C` from 3 records (stride 0x70) at `0x01F80F90`, live at `0x01F80130` | `SI:741-752`, `:792-794` |
| ownership of the 1,172 | Input 325 (27.7 %), Phyre 317, Runtime 279, CompilerGeneratedCpp 101, NativeRoutine 62, EASTL 58, Platform 19, others 10 | `SI:695-702` |
| per-entry shapes | StaticObjectInitializer 90, StaticZeroInit 11, other 1,071 | `OBJ:194-199` |

#### State and lifetime

- Eager globals live from `_initterm` until the `atexit` chain (`SI:217-227`). On a normal quit that chain
  never runs: "the normal quit ends in ExitProcess and never runs the chain" (`ST:4`, `:156`). See §1.3.
- The lazy-static lock exists before any C++ initialiser runs. It is created by C initialiser `00809124`
  (`LZ:483`, `SI:675`). This is a join of two pages; neither states it in one place.

#### Order

1. `entry` → `__security_init_cookie` → `00808D78` (`SI:489-492`).
2. C initialisers (`_initterm_e`) → C++ initialisers (`_initterm`) → state := 2 → WinMain (`SI:503-505`,
   `:660-666`). "So the true order is **cookie, then C initializers, then the 1,172 C++ initializers, then**" WinMain (`SI:504`).
3. The project's injected DLL loads at the WinMain call (detour on base+`0x6E8E8A`). The earliest
   engine-neutral hook point is `00808D78` (`SI:524`, `:531-546`).

### 1.2 Lazy ("magic") statics and the one-time-init lock

#### Entry points

| function | size | role | caller | cite |
|---|---:|---|---|---|
| `008092FC` `_Init_thread_header` | 103 B | claims a guard, or waits; 1,732 call sites in 707 functions | the holder functions | `LZ:192`; `EH:283`; `SI:826` |
| `0080929C` `_Init_thread_footer` | 96 B | publishes: bumps the global epoch, stamps it into the guard, notifies; 1,732 sites | holders | `LZ:146`, `:193`; `SI:343` |
| `0080926C` `_Init_thread_abort` | 48 B | puts the guard back to 0 and wakes waiters | only the 1,545 unwind funclets | `LZ:149`, `:194`; `EH:282` |
| `008093C0` `_Init_thread_wait` | 151 B | "the 100 ms wait" | `_Init_thread_header` only (but see §3, X-21) | `LZ:195`, `:668`; `EH:286` |
| `00809364` `_Init_thread_notify` | 91 B | wakes threads waiting on a guard | footer, abort | `LZ:196`, `:275`, `:282`; `EH:285` |
| `00808B90` `atexit` | 23 B | registers the static's destructor; 526 holders call it | holders | `LZ:86`, `:197`, `:587` |
| `00632960`, `00630180`/`006301F0`/`006373D0`, `006388C0`, `00632FB0`, `0067F700` | — | the top callees from holders (680 / 602 / 301 / 216 / 146 calls): Phyre reflection registration | holders | `LZ:102-106`, `:198-200` |

#### Inputs, outputs and record layouts

| item | layout / value | cite |
|---|---|---|
| guard | plain `int` in `.data`. `0` untouched; `-1` under construction; "`> 0` built; value is the epoch at which it completed" (but see §3, X-2) | `LZ:248-250`; `EH:419-421` |
| guard address range | `01F7F5C8`–`02EBA258` (the 1,545 with funclets); "The 1,681 guard variables all live in `.data`" | `LZ:221`; `EH:319`, `:434-435` |
| gate compiled at each site | `if (thread_epoch < guard)` → header → `if (guard == -1)` construct, footer | `LZ:227-240`; `EH:372-383`; `SI:208-213` |
| pseudocode of header / footer / abort | given in full | `LZ:259-285`; `EH:389-413` |
| descriptor pair (61 accessors) | 16-byte `{record\|1, 0}`, guard = static+0x10 | `LZ:26` |
| encoded Win32 pointers | decode `ROR64(cookie ^ slot, cookie & 0x3F)` with cookie `01F44830` | `LZ:165`, `:291`, `:313` |
| reflection records built under guards | `PClassDataMember`: rec[0]=vftable, rec[5]\|=2 for flag 2, rec[6]=typeInfo, rec[7..8] self-linked, rec[9]=size, rec[10]=0; descriptor vslot +0x40 | `LZ:331-344` |
| type-name hash | seed `0x7B5`, `h*0x21 + (c & 0x1F)` | `LZ:319-321` |

#### State

| global | value | cite |
|---|---|---|
| `02EAED40` `_Init_thread_lock` | `CRITICAL_SECTION`, spin count 4000; "the **single** lock shared by all 1,681" | `LZ:211`, `:483-484` |
| `02EAED68` `_Init_thread_cv` | `CONDITION_VARIABLE` | `LZ:212` |
| `02EAED70` | fallback event; 0 on the CV path, else `CreateEventW(NULL,TRUE,FALSE,NULL)` | `LZ:213`, `:487-489` |
| `02EAED78` / `02EAED80` | encoded `SleepConditionVariableCS` / `WakeAllConditionVariable` pointers | `LZ:214-215` |
| `01F44850` `_Init_global_epoch` | ships `0x80000000`; advanced only by the footer (`inc eax` at `008092C5`) | `SI:342-343`; `LZ:216` |
| `02EAED3C` `_tls_index` | — | `SI:183`; `LZ:218` |

Census: 1,681 distinct statics, 1,732 guarded sites, 707 holder functions, 1,545 with an abort funclet, 136
without, 19 multi-site guards accounting for the 51 extra sites (`SI:821-838`; `LZ:82-92`; `EH:157-167`).
Lifetime: from first use until the `atexit` chain, in reverse order of first build (`LZ:179-184`). The wait
literal is 100 ms, with "no timeout escape" (`LZ:173`, `:313-314`, `:413`).

#### Order

Built on first use, "usually on a loading screen" (`EH:63-70`). Which of the 1,681 a normal boot builds is
"live-only by measurement". NATIVE-REPLAY lower bound: 19 constructed; 1,662 residue (`LZ:452-454`). The pages do
not state whether any lazy static is built *before* `main` by an eager initialiser. A direct-closure attempt found
94 holders reachable from the entry and the 1,172 initialisers, then was withdrawn: "not publishing it as a
finding" (`LZ:455`).

### 1.3 Static teardown and process exit

| item | statement | cite |
|---|---|---|
| 224 intrusive-list teardowns | 82 B each, one instruction form. Each unlinks a node from a list head, resets it to empty, tests `byte [head+0x20]` bit 0 and calls `00584730` on `[head+0x18]` | `ST:23`, `:67-88` |
| node layout | prev +0, next +8, owner +0x10, name +0x18, flags dword +0x20; owner's list at +0xA0; bit 0 of +0x20 = "name copied to heap" (copy via `0017D260`) | `ST:150`, `:153`; members `.tsv` header |
| who registers them | "exactly one of 51 class-registration functions", inside the thread-safe static guard, so "function-local statics built on first use" | `ST:150` |
| 145 empty-destructor wrappers | `lea rcx,[static]; jmp 0016D6A0` (12 B); registered with `atexit` | `ST:24`; `HARD:157-161` |
| 60 `IndirectAllocator` container thunks | 72 B; if count > 1 and begin non-null, call `[rax+0x18]` | `OBJ:866`, `:884-891` |
| `atexit` wrapper | `00808B90` over `_onexit` `00808B40` | `ST:156` |
| chain order on `exit` paths | "registrations run last-in first-out" | `ST:155-156` |
| normal quit | `WM_QUIT` test `0079869A` → … → `007986BF`→`0061C540` → `ExitProcess(0)` at `0079887F`; relaunch via `CreateProcessA` `00798817`; "`ExitProcess` terminates the process without the runtime's exit sequence" | `ST:156`, `:187-190` |
| CRT `exit` reach | nine sites: `0079814B` plus "eight error exits in `00369860`, `0036B670`, `0036B730`, `0036B7F0`, `0036B8B0`, `0036CB00` and `008272D0`" | `ST:156` |

### 1.4 C++ exception handling and unwind funclets

#### Entry points and ABI

| item | statement | cite |
|---|---|---|
| funclet ABI | `funclet(RCX = ignored, RDX = the parent function's frame pointer)`; locals at `establisher_frame_rdx + fixed_offset`, +0x20…+0xF0 | `EH:91`, `:362-363` |
| prototypes | `Unwind_XXXXXXXX(void*, char *establisher_frame_rdx)`; `Catch_All_…` returns the resume address; `filt_N(void *exception_pointers_rcx, …)` returns `EXCEPTION_*` | `EH:352-359` |
| reached by | "a funclet has no callers at all. The unwinder reaches it from the exception tables" | `EH:515-516` |
| handlers | `__CxxFrameHandler3` thunk `00861EB4` (4,377 functions); `__GSHandlerCheck` `00808BA8` (5,372); `__GSHandlerCheck_EH` `00808F64` (141); `__C_specific_handler` `00861ED8` (9) | `EH:264-267`, `:292-295` |
| throw / terminate | `_CxxThrowException` thunk `00861ECC`; `__std_terminate` thunk `00861EAE` (86 funclets tail-jump to it) | `EH:247`, `:290-291` |
| seven SEH filters | `0089BEF0`/`005CD1E0`, `008A5AD0`/`005CCBA0`, `008A5B7C`/`00808A54`, `008A5B94`/`00808D78`, `008A5BB2`/`00808FE4`, `008A5BDE`/`00809054`, `008A5C0A`/`008090C0` (filter / parent) | `EH:337-343` |

#### Record layouts

| record | layout | cite |
|---|---|---|
| `RUNTIME_FUNCTION` | 12 B `{BeginRVA, EndRVA, UnwindInfoRVA}` | `EH:482` |
| `UNWIND_INFO` | byte0 `Version:3 \| Flags:5` (EHANDLER 1, UHANDLER 2, CHAININFO 4); byte2 CountOfCodes; then handler RVA and language data | `EH:483-485` |
| `FuncInfo` (x64) | 40 B, 10 fields, magic `0x19930520/21/22` | `EH:486-489` |
| `UnwindMapEntry` | 8 B `{i32 toState; u32 action}` | `EH:490` |
| `TryBlockMapEntry` / `HandlerType` | 20 B each; `addressOfHandler` = catch funclet RVA | `EH:491-493` |
| `C_specific` scope table | `{u32 count; count × {Begin, End, Handler, JumpTarget}}` | `EH:494-495` |
| IP-to-state map | named as the field `pIPToStateMap` only | `EH:487` |
| filter constants | `0xE06D7363` → terminate; `0xC0000005` | `EH:468`, `:473` |

#### Order

`throw` → `_CxxThrowException` → `RtlUnwindEx` → `__CxxFrameHandler3` → cleanup funclets "innermost state first"
→ catch funclet → resume (`EH:502-513`). Census: 3,895 tagged funclets, of which 3,893 are genuine; 2 are not and
6 are missing from the tag. 3,899 are declared (3,820 unwind + 72 catch + 7 filters), in block `00896280`–`008A6960`
(`EH:35-36`, `:308-309`, `:707-708`, `:783`).

### 1.5 Object deletion: the deleting-destructor contract

| item | statement | cite |
|---|---|---|
| contract | `rcx` = this, `edx` = flags; bit 0 = free; returns this; vtable slot 0 | `OBJ:95-97`, `:270-277` |
| spelling A | e.g. `001D70A0`: install vtable `00900370`, free 0x90 via `00809950` | `OBJ:103-112` |
| spelling B | e.g. `00195530`: flag to `ebx`, inner dtor `00195180`, free 0x98 | `OBJ:119-129` |
| two-bit form | e.g. `00185800` (66 B), `0017CC70` (GameApplication, 0x1140): bit 0 gates freeing, bit 2 selects `0016D6A0` (a `ret 0`, so "**these destructors free nothing at all**") over `00584730` → `_aligned_free` | `OBJ:164-183`, `:594-603`, `:778-788` |
| bit-2-clear deallocators | `00584730` 1,494 · `007AD450` (SEAD) 93 · `0085E710` (Bullet) 19, over 1,606 resolvable members | `OBJ:175-176`, `:589-591` |
| deallocators | `00809950` `free` (5-byte thunk → `00210EB0`); `00584730` `if (this) _aligned_free(this)` (10 B); `0019C570` `_aligned_free` import thunk | `OBJ:256`, `:261-262`, `:431` |
| `sizeof` | the `mov edx, imm` before the free is the class size (0x90, 0x98, 0xD8), "per call site and not as a population statistic" | `OBJ:280-281`, `:608-612` |
| third-party allocators | Bullet `btAlignedFreeInternal` `0085E710` (counters `02EAF6C8`/`02EAF6C4`, hooks `01F44CF8`/`01F44CF0`, installed by `006A4100`); SEAD `007AD450`/`007AD460` (block stamp `0x5EAD5EAD` +0, tag +4, size +8, original pointer at result−8; slots `02EAD0B8`/`02EAD0B0`, setter `007AD620` called from `007A4D50`) | `OBJ:417`, `:1098-1101` |
| vtable install | 60 + 25 `VtableInstall*` bodies | `OBJ:236-237` |
| `vector<void*>::insert` `001AB570` | `{begin,cur,end}` at +0/+8/+0x10; allocator at `[rcx+0x18]` slots +0x10/+0x18; new cap = 2*cap (min 1) | `OBJ:837-846` |

### 1.6 The engine memory arena and the CRT allocation routes

#### CRT routes

| route | statement | cite |
|---|---|---|
| imports | 8 heap imports from `api-ms-win-crt-heap-l1-1-0`; IAT `008C2B40`–`008C2B78` (malloc `…B40`, free `…B48`, `_aligned_malloc` `…B60`, `_aligned_free` `…B70`) | `MEM:81-82`, `:558-563` |
| no `operator new`/`delete` imported | "every allocation route read for this document goes to `malloc` or `_aligned_malloc` directly" | `MEM:500-502` |
| `_set_new_mode(0)` | called once by `00808D5C`; "`malloc` returns `NULL` on failure rather than invoking a handler" | `MEM:498-500` |
| wrappers | `0017D260` `allocate(n, align)`; `00584740` `allocate(n)` (align 16); `00584730` free (2,309 callers); `0019C580` aligned-malloc adapter; `00809950` → `00210EB0` → `0019C590` free chain; `00210EC0` malloc forwarder | `MEM:527-534`, `:739`, `:767`, `:1560-1565` |
| EASTL allocator | virtuals `0016D6B0`, `0016D6C0`, `001EDF10`, `001EDF80`, `001EDFE0`; ctor `001EDF00`; vtables `008F6500` (allocator), `00902720` (memory_log); memory log `01F82E48` (0x20 B, lazily created) | `MEM:351-363`, `:433-452`, `:518-526` |

#### The arena (fifteen heaps)

| item | statement | cite |
|---|---|---|
| allocator `0036BC60` (887 B) | `(arena, size, 0, 0)`; 64-byte rounding; 0x40-byte header; first-fit from head / last-fit from tail (arg4); splits | `MEM:107-110`, `:1065-1079`, `:1097`, `:1293` |
| wrappers | `0036A100` / `0036A190` / `0036A1A0`; `0036A100` = `0036BC60`, then retry `0036BFE0` on failure, then three header writes | `MEM:113-114`, `:1141-1151` |
| retry `0036BFE0` | asks the heap's callback slot and the reclaim step before returning null (see §3, X-M6) | `MEM:40-41`, `:67` |
| boot | `0022A0B0` makes 9 blocks via `0036D240` → malloc thunk `0085E730`, then `00369D30(id, block, size, slotCount)` per arena; "About 256 MiB in all" | `MEM:120-134`, `:172-178`, `:308-317` |
| arena sizes (MiB / slots) | 2 = 29.75/16; 3 = 13.125/256; 4 = 1/16; 5 = 1.75/256; 6 = 108/1,024; 7 = 48/256; 8 = 32/256; 9 = 18/16; 11 = 4/256 (re-malloc 3.75 or 4 by `02ADD930`); 13 nested 1 MiB `EVTM` | `MEM:126-137` |
| records | 15 × 0xA8 at `022D7FD0`; +0x08 backing, +0x10 first header, +0x18 descriptor bound, +0x20 dword bitmap, +0x28 qword page table, +0x30/+0x38/+0x40 slot table start/end/free head, +0x48 in-use head, +0x50 tree root, +0x5C free size, +0x60 sequence word, +0x62 latch, +0x68 `uint32[9]` counters, +0x90/+0x98 free-list head/tail, +0xA0 callback | `MEM:107-108`, `:148-153`, `:165`, `:174-176`, `:182`, `:199`, `:225-226`, `:999`, `:1035`, `:1086-1089`, `:1118`, `:1688`, `:1708-1724`, `:1890` |
| block header (0x40) | +0x00 magic `0xFF12` live / `0xFF99` unlinked; +0x02 category stamp; +0x03 arena id; +0x04/+0x08 free-list prev/next (base-encoded); +0x0C/+0x10 physical prev/next; +0x14 bit 0 allocated; +0x15 flags (0x02 in tree, 0x04 movable); +0x16 counter index; +0x17 category counter index; +0x18 payload length; +0x1C id word; +0x20 encoded handle; +0x24/+0x28/+0x2C tree left/right/parent; +0x34 name string; +0x3E guard word (always 0) | `MEM:182`, `:200-203`, `:208`, `:231-250`, `:296-297`, `:1009-1053`, `:1661-1664`, `:1705-1736` |
| slot and handle | 16-byte slot: word +0 next, word +2 previous (`0xFFFF` = none), byte +4 arena id, +8 header pointer. Handle = slot address \| 3; release rejects values with the low 2 bits clear or below 0x100000 | `MEM:176-177`, `:182-188` |
| selection stack | push `0036C1D0`/`0036C1F0`, pop `0036C140`; 2 stacks × 32 × 16 B at `022D89D0`; active arena `022D89BC`; map `022D89A8`; enable mask `022D89B8`; category `022D8E18` (init 0xFF); "an allocation through the wrappers requires at least one pushed selection" | `MEM:280-293`, `:308-327` |
| free `00369860(payload, aux)` | six gates; abort path through `0036A570`, the hook cell `q[008C2D80]` and `int3` | `MEM:217-223`, `:1093-1094`, `:1645-1664` |
| compaction | `0036AAD0`/`0036ABE0` select; `0036A2A0` relocates; `00369C60` explicit front | `MEM:67`, `:1749-1762`, `:1878-1880` |
| consumers | Presentation 123, World 44, ActorEntity 48, Script 12, Audio 32, Input 6, Platform 4, SaveLoad 1, Application 1 | `MEM:1930-1956` |
| frame hook | `00332660` reads the arena-6 latch → `0041E500`, `00426950`, then clears it; called by `MainLoop_UpdateAndRenderFrame` and the field frame | `MEM:1891-1893`, `:1960` |

### 1.7 Ordered containers: EASTL rbtree and MSVC `std::_Tree`

| item | EASTL (`OC`) | MSVC (`MS`) |
|---|---|---|
| bodies | 6 bodies, 1,741 B: increment `0016D6D0` (68 B, 58 callers), decrement `0016D720` (94 B, 24), rotate-left `0016D780`, rotate-right `0016D7E0`, insert `0016D840` (532 B, 56 callers, rotations inlined), erase `0016DA60` (867 B, 30 callers) (`OC:26`, `:136-144`) | 23 bodies, 6,630 B, in three instantiations A/B/C: rotations `00714B00`/`0071F240`/`00799BD0`/`00799C30`, inserts `00712F60` (node 0x30) and `0071E500` (0x60), erase-node `00714DC0`/`0071F590`/`0079BA10`, tidy, destroy-subtree, payload dtor `0071EE70`, erase-range (`MS:121-137`) |
| node | +0x00 right, +0x08 left, +0x10 parent, +0x18 colour (red 0, black 1); payload at +0x20; node = `0x20 + sizeof(Value)`; nine sizes 0x28…0x88 (`OC:57-62`, `:89`, `:160-179`) | +0 `_Left`, +8 `_Parent`, +0x10 `_Right`, +0x18 `_Color`, +0x19 `_Isnil`, +0x20 `_Myval`; 0x30 node = key +0x20, value +0x28 (`MS:57-68`) |
| head | node-shaped: +0x00 rightmost, +0x08 leftmost, +0x10 root; root painted black at end of insert (`OC:118-121`) | head at `[rcx]`, root at `[r11+8]`, size at `[rcx+8]` (`MS:106`, `:259-260`) |
| insert | rcx = node, rdx = parent, r8 = head, r9d = side; the node gets `[+0x10]=parent`, +0 = +8 = +0x18 = 0 (`OC:112-114`, `:273-276`) | parent store `00712FA3 mov [r11+8], r9`, on the node received as fifth argument (`MS:373`) |
| comparator | in the caller; the family never reads the key (`OC:89-91`) | descent `cmp [rax+0x20], rdx` / `setae` (`MS:259-260`) |
| allocation | allocator vtable `+0x10`, size in `edx` (`OC:157-160`) | `_Buynode0` / `_Buynode`; `max_size` `0x0555555555555554` (0x30) / `0x02AAAAAAAAAAAAA9` (0x60); overflow → free, `_Xlength_error`, `int3` (`MS:94-108`, `:379-381`) |
| users | 99 callers: 24 unique-key map/set instantiations, 56 insert wrappers, 30 inline erases, 12 walks (`OC:4`, `:207-208`) | A = three YEBIS resource-wrapper caches in the 0xD40 block at `02EA0B70`; B = parsed licence map; C = static tree at `02EA5550`, "never filled or searched" (`MS:175`, `:197-221`) |

### 1.8 Generated families and the return-value adapter

| item | statement | cite |
|---|---|---|
| catalogue | "55 tag groups of ten or more members each collapse to exactly ONE instruction form, covering 1,236 functions"; "Nothing here is a claim about behaviour." | `GEN:16-19`, `:226` |
| trivial global accessors | 482 bodies: one RIP-relative instruction then `RET` (lea 91; reads 1/2/4/8 = 58/17/102/53; writes 35/3/67/9; write-const 20/18/10) | `GEN:23` |
| sixteen shared implementations | all have a role (UQ-319, 2026-09-26): e.g. `00633240` `PClassDataMember` dtor, `006B6750` `PAnnotation` dtor, `007DF6D0` `InitializeCriticalSection` + zeroing | `GEN:265-284` |
| adapter template | 403 bodies, 26 B each: `push rbx; sub rsp,0x20; mov rcx,rdx; mov rbx,r8; call <accessor>; mov [rbx],rax`; signature *(context, argument, result\*)*, arg 1 dropped; bytes `40 53 48 83 EC 20 48 8B CA 49 8B D8 E8 rel32 48 89 03 48 83 C4 20 5B C3` | `RV:28`, `:71-93` |
| where they sit | descriptor slot 5, "fetch a `T*` from the script value"; 1,185 appearances | `RV:255-256`, `:414-416` |
| DF-1 owned-buffer reset | 46 × 59 B at slot 11: if header dword +0 bit 31 clear and +8 non-null, `00584730(ptr)`, zero +8 and +0, return true | `RV:29`, `:154-161` |

### 1.9 The thunk layer and the Windows service surface

#### Thunks (`TH`)

| item | statement | cite |
|---|---|---|
| population | 689 `Thunk.*` functions, sizes 568 / 108 / 12 / 1 at 5 / 6 / 7 / 19 bytes; tags `InternalForwarder` 560, `ExternalImport` 117, `DirectTailForwarder` 12 | `TH:58-65`, `:448` |
| encodings | forwarders `E9 rel32` (5 B); import stubs `FF 25 disp32` or `48 FF 25 disp32` through the IAT (`008C2000`..`008C31C0`), "filled once by the loader" | `TH:150-157`, `:213`, `:562`, `:588` |
| image-wide forwarders | "**749 functions have a complete body of exactly five bytes, `E9 rel32`**", 749 distinct targets (but see §3, X-T1) | `TH:493-494`, `:510` |
| import stubs | 117, each resolved to DLL and export; 18 DLLs (math 34, MSVCP140 20, runtime 14, VCRUNTIME140 12, heap 9, string 7, kernel32 5, …) | `TH:561-572` |
| receiver binder `0028FB40` (19 B) | `MOV RCX,[0209BE80]; ADD RCX,0xA0; JMP 003F8D20`; "It **binds a receiver**"; four siblings `0028E220`, `0028E860`, `0028E8B0`, `0028FB60` | `TH:86-92`, `:397-404` |
| HUD element behind it | `003F8D20` load (on message `+8 == 0xF` from `00253780`), `003F8EC0` per frame, `003F8EA0` clear, `003F8C70` walk; fields `+0x52C6`, `+0x52B8`, `+0x52A0`, `+0x4020` (0x1280 B), `+0x52C0` count of 0x100-byte records; position eased by 0.5 | `TH:271-281` |
| CFG dispatcher thunk | `00809958` = `jmp [__guard_check_icall_fptr]` (`008C31C0`) | `TH:587-600` |
| address-taken thunks | 296 of 689 (268 qword, 25 `lea`, 3 both) | `TH:291-305` |
| Ghidra flag | "**835 forwarders, 819 flagged, 16 unflagged**"; why 16 are unflagged is "NO ADMISSIBLE SOURCE" (Ghidra project state) | `TH:4`, `:229`, `:326` |

#### Runtime service surface (`RS`)

| item | statement | cite |
|---|---|---|
| import surface | "**30 DLLs, 538 imported symbols.**"; 417 slots called through `FF 15`, 3,543 indirect sites; the other 121 reached through 104 stubs, 9 in-body tail jumps and 8 as loaded values | `RS:60-61`, `:286`, `:299-303` |
| busiest imports | `_invalid_parameter` 434 sites / 80 functions; Leave/EnterCriticalSection 310/126 and 286/134; `memmove` 244; `OutputDebugStringA` 150/93; `rand` 48/30 | `RS:82-93` |
| debug log `006DF480` (137 B) | Yebis printf-style wrapper; 0x800-byte buffer at `02EA0BA0`; `__stdio_common_vsprintf` (options `\| 1`) then `OutputDebugStringA`; 801 call sites from 160 functions; hook slot `02EA0B88` starts at 0 and "stays 0 in the shipped build" | `RS:113-123`, `:219-245` |
| crash filter `0079AD50` | installed by `007980A0` (`SetUnhandledExceptionFilter` at `007980F7`) "on every boot"; gate `01F40128` = 1; `MiniDumpWriteDump(GetCurrentProcess(), GetProcessId(…), file, 0x1826, &exceptionInfo, 0, 0)`; then string `0x7837` "Fatal error encountered.", `MessageBoxW(NULL, text, L"error", MB_ICONERROR)`; returns 1 | `RS:252-275` |
| second dump path | `008A5AD0` → `005CCBF0` → `005CCD00` (symbolised stack walk, 926 B) → `CreateThread(005CCAB0)`, dump type `0x1B27` | `RS:156-158`, `:280-285`, `:441` |
| SEH users | nine `__C_specific_handler` users (WinMain, thread trampoline `005CCBA0`, thread-name guards `005CD1E0` / `00863430` with `0x406D1388`, four CRT bodies) | `RS:389-435` |
| licence check | `GetAdaptersInfo` at `00781F80`/`00781FD7`; `strncmp(licence MacAddress, "00-00-00-00-00-00", 17)`; shipped licence `FeatureId = YEBIS_D3D11 … MacAddress = 00-00-00-00-00-00` | `RS:310-318` |
| service / registry layer | 18 bodies `00159420`…`0015B5F0`: dynamic loads of Setupapi / Advapi32 / Shell32; HKLM `SOFTWARE\Microsoft\Windows NT\CurrentVersion` `CurrentBuildNumber` (cache `02EAECE0`); `SYSTEM\CurrentControlSet\Control\Class\`; HRESULTs `0x80070057` / `0x8007007A` | `RS:495-577` |

### 1.10 Image hardening: ASLR, CFG, DEP, `/GS`

| item | statement | cite |
|---|---|---|
| ImageBase | `0x00120000`; `DllCharacteristics 0x8120` (HIGH_ENTROPY_VA, NX_COMPAT, TERMINAL_SERVER_AWARE); `DYNAMIC_BASE` and `GUARD_CF` not set → "Ghidra VA equals runtime VA" | `HARD:55-67`, `:243-258` |
| load config | 148 B at RVA `01BCBE40`; +0x58 SecurityCookie `0x01F44830`; +0x70 `0x008C31C0`; +0x78 `0x008C31C8`; +0x80 table 0; +0x88 count 0; +0x90 GuardFlags `0x00000100` | `HARD:100`, `:246-252` |
| CFG | check slot `008C31C0` → `0016D6A0` = `ret 0` (`C2 00 00`); dispatch slot `008C31C8` → `00896270` = `jmp rax`; enforced iff CF_INSTRUMENTED && GUARD_CF && table ≠ 0 | `HARD:130-135`, `:266-268` |
| cookie init | if cookie == `0x00002B992DDFA232`: FILETIME ^ tid ^ pid, then `r = (pc.HighPart<<32) ^ pc.QuadPart ^ v ^ &v`, `r &= 0x0000FFFFFFFFFFFF`, avoid the default, store, then `*(u64*)0x01F44838 = ~r` | `HARD:624-635` |
| cookie check `00808C40` (33 B) | `cmp rcx,[01F44830]`; `rol rcx,0x10; test cx,0xffff`; mismatch tail `00808C5C` → `__report_gsfailure` `00809654` → `int 0x29` (ecx = 2), else `UnhandledExceptionFilter` → `TerminateProcess(…, 0xC0000409)`; game crash filter `0079AD50` is never reached | `HARD:642-670` |
| range check | `__report_rangecheckfailure` `00809728`, fast-fail 8; 237 sites | `HARD:680-685` |
| DEP | `.text` R-X, `.data` / `.tls` RW-, all others R-- | `HARD:608-609` |
| corrected section table | `.text` VA `0x00121000` / `0x7A0635` … `.reloc` `0x0305C000` / `0x39360` | `HARD:805-818` |
| toolchain | linker 14.0 build 24215 (VS2015 U3); VC_FEATURE 1,296 objects / 1,265 `/GS` | `HARD:452`, `:499` |

### 1.11 The maths library

| item | statement | cite |
|---|---|---|
| source | 45 imports from `api-ms-win-crt-math-l1-1-0.dll` → `ucrtbase.dll`, "none shipped"; always "`call` into a jump thunk, never inlined" | `MATH:70-72`, `:92` |
| call counts | `sqrtf` 566 sites / 269 functions; `sinf` 174; `powf` 133; `cosf` 109; `logf` 86; `expf` 65; `tanf` 60; `atan2f` 51; … 29 routines tabulated | `MATH:94-113` |
| SIMD | `rsqrtps` + one Newton–Raphson step `y1 = (3.0f - (x * y0) * y0) * (0.5f * y0)`; masked dot product (mask `00D11570` = 1,1,1,0) then `haddps` ×2; cross product `a.yzx*b.zxy - a.zxy*b.yzx` (`shufps 0xC9`/`0xD2`); all SIMD sites are Audio-owned | `MATH:173-212`, `:378-406`, `:663-666` |
| angle wrap `0033CB70` (128 B) | near path `while a>π: a-=2π` (and the mirror); far path for \|a\| > 12.566371f: `a - (float)(int)(a/2π)*2π` via `cvttss2si`; regimes for large inputs given | `MATH:245-275`, `:473-483` |
| turn-rate easing (`0033CEF0`) | if \|Δ\| < π/3: `c = cosf(3·|Δ|)`, `turnRate = (1-c)*0.5*(turnRate-1°)+1°`; turnRate from +0xE4 or +0xE8 | `MATH:427-441` |
| XZ distance `004686D0` / squared `003A1960` | `dx=a[0]-b[0]; dz=a[2]-b[2]; dz*dz+dx*dx` (Y ignored), then `sqrtf` | `MATH:326-327`, `:414-420` |
| combat pow `0038EAF0` | `*(s32*)0x02AEE004 = (s32)pow(2.0,(double)n)`, n = byte `+0x5B0E` of `*0x02EBF190`, n ≤ 17 | `MATH:458-463`, `:564` |
| boot tunable `0016A270` | `*(float*)0x02EADEF0 = 0.9f / sqrtf(16.0f)` = 0.225 | `MATH:372`, `:489-497` |
| constants | π `01CEBC50`, 2π `01CEBC78`, −π `00915620`, −2π `00915624`, ±4π `00D10B0C`/`00D10B20`, 1° `008C5F68`, π/3 `0091572C`, 3.0 `008F311C` | `MATH:354-369` |

### 1.12 Dependencies on other categories (summary)

| from | on | cite |
|---|---|---|
| lazy statics, static init, teardown | PhyreEngine reflection (class descriptors, data-member registration): 535 of 707 holders call `Phyre.Reflection.*` | `LZ:87`, `:96-122`; `SI:570`; `ST:100-104`, `:150` |
| eager initialisers | Input (325 entries), Audio/SEAD static pools, Engine core | `SI:301-328`, `:695-702`, `:799` |
| EH | VCRUNTIME140 handlers; 1,609 funclet parents across Resource, Audio, Input, Save, Platform, Presentation | `EH:174-186`, `:265-267` |
| deletion | Bullet and SEAD allocators | `OBJ:417` |
| arena | EFX, Resource, Phyre `PAssetReference`, Audio, actor pool (`002679F0` via hook `M+0x88`) | `MEM:154-164`, `:536-537`, `:654-658`, `:905`, `:1905-1916` |
| MSVC tree | YEBIS / PPFX post-effects (`006DA880`–`007911E0`), Phyre PFramework | `MS:171-177` |
| adapters | Phyre reflection descriptors, `00682980` PhyreObject registry | `RV:109-111`, `:412` |
| maths | Movement, Presentation, UI, Audio, Party, CombatAction; OS `ucrtbase.dll` "varies by Windows version" | `MATH:61-64`, `:296-308`, `:502` |
| hardening | Phyre serialization (the 144 scalar-conversion initialisers) | `HARD:27`, `:165-184` |

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open, live-only, or out of evidence)

Only gaps the pages still leave open are listed. Rows the pages answer are not listed, even where a stale "open"
sentence remains. Those are in §3.2.

| # | gap as the page states it | cite |
|---|---|---|
| G-1 | Which of the 1,681 lazy statics a normal boot builds: "live-only by measurement"; NATIVE-REPLAY lower bound 19, residue 1,662 | `LZ:452-454` |
| G-2 | "Nothing here has been seen to execute; the hang is derived from the control flow, not witnessed." | `LZ:682-683` |
| G-3 | What each of the 1,172 eager initialisers costs: T-6 is ticked, but "**Not claimed:** that these shares reflect startup *time*." | `SI:290-291`, `:715-716` |
| G-4 | SEAD static pools: "**Not established:** that the prototype copies are these containers' header initialisation …, each container's capacity, and the unnamed fields between the objects listed." | `SI:326-328` |
| G-5 | "**Developer — CLIENT, not read.**" (the 18-byte function with a 1,046-byte Developer caller) | `SI:894` |
| G-6 | The lock-pair dispatch: "**Not claimed:** `005CD570`'s dispatch target list … or the lock object's owner type." | `LZ:710-711` |
| G-7 | EH: "**Not attempted, and therefore not claimed:** runtime confirmation that any funclet ever executes" | `EH:985-987` |
| G-8 | EH: "**Not challenged this pass:** the identity of the 827 downstream callees, the 250 unclassified parents, and whether the 46 skeletons are stable"; "The original parent list is not preserved" | `EH:197-198`, `:896-897` |
| G-9 | 254 Phyre per-type constructors "untouched"; 83 frontier `.CRT$XI` members "each … needs individual reading" | `ST:107-110`, `:117-121` |
| G-10 | Every `ST` family row ends "NOT dispositioned: …" (per-type destructors, record types, callback targets) | `ST:23-44` |
| G-11 | "**The per-class mapping is still not established.**" (26 `PInputSource` deleting destructors to classes) | `OBJ:701` |
| G-12 | BQ-27: whether bit 2 is ever passed (so whether those objects leak) is "checkable at runtime"; 61 live-breakpoint sites | `OBJ:604`, `:815-822`, `:830` |
| G-13 | "Which containers the 60 hosts own is still open." | `OBJ:943` |
| G-14 | `02ADD100`: "**NOT CLAIMED:** what the handle indexes, or whether the resource system releases the buffer" | `OBJ:1012-1013` |
| G-15 | "**What the game does when memory runs out has not been observed.**" | `MEM:66` |
| G-16 | "**Which overrun the guard is positioned to catch is not settled**" | `MEM:248` |
| G-17 | Memory-status readers `0020C610` / `00792F10`: "whether either reader influences any size is not established" | `MEM:271-272` |
| G-18 | The accounting array: "**So the closure holds for the literal call sites, and is open for this one path.**" | `MEM:1526-1528` |
| G-19 | "Six of the new rows say "NOT UNDERSTOOD"" (header fields) | `MEM:1742-1745` |
| G-20 | Asset registry: "**Not read:** whether entries are removed when a cluster unloads." / "**Not claimed:** how often either pool is built" | `MEM:929-933` |
| G-21 | SECTION-07: "The callback bodies and whole game scheduling are not certified by these static call sites"; actual Windows CRT behaviour is "an explicit evidence boundary" | `MEM:1893-1894`, `:1899-1901` |
| G-22 | MSVC tree C: element type "not recoverable from use" | `MS:221` |
| G-23 | Adapters: "Not claimed: what descriptor slot 5 *does* is untouched"; "Nothing was executed or observed live" | `RV:372-375` |
| G-24 | BU-1 residue "needs the analysis log, not the EXE"; `003F1290` "was not read" | `TH:248`, `:283` |
| G-25 | 354 of 749 forwarder targets still in the frontier; "The import **slots** (538) are not dispositioned" | `TH:31`, `:624-625` |
| G-26 | Crash path: "Actual initialisation and live main-module-only behaviour are not established"; "Not observed here: which language copy is chosen at run time, that the box appears, or how the process ends." | `RS:266`, `:278-279` |
| G-27 | Licence check: "the per-adapter comparison after that was not traced"; Steam: "the rest of the Steam surface is not examined here" | `RS:317`, `:322-324` |
| G-28 | "**Not attacked:** the per-DLL import counts, the busiest-import table" | `RS:383-385` |
| G-29 | Hardening: OS behaviour "needs runtime evidence (tier 10) and has not been done"; record `02D3E880` "was not read"; guard `003F9C96` "not traced" | `HARD:186`, `:695`, `:728-729` |
| G-30 | Maths: the scalar CRT algorithms are excluded on purpose and come from the OS's `ucrtbase.dll`, which varies by Windows build | `MATH:61-64`, `:74-82`, `:550-554` |
| G-31 | UQ-323: "The **21 `movaps` and 19 `subss` sites are unresolved**" | `MATH:592` |
| G-32 | UQ-324's answer is "exactly as strong as the inventory is complete" | `MATH:615-618` |
| G-33 | Generated families: "**Nothing here is a claim about behaviour.**"; leftovers "NOT dispositioned" (435 globals' meanings, 559 and 613 leftovers) | `GEN:23-25`, `:226` |

### 2.2 Structural gaps (a port needs these and no page states them)

| # | missing | where the gap shows |
|---|---|---|
| SG-1 | **One coherent lazy-guard numeric model.** The gate, the guard's built value and the epoch's start value disagree (§3, X-2/X-3/X-4). A bit-exact port of the guard protocol cannot be written until they agree. | `LZ:235`, `:250`; `SI:340-343`; `EH:421`, `:427` |
| SG-2 | **IP-to-state map layout and state numbering** (`pIPToStateMap`, `toState`, `dispUnwindHelp`, `EHFlags`): named, not described | `EH:486-490` |
| SG-3 | **Per-funclet tables** (parent, state, destructor target): counts only; "The original parent list is not preserved" | `EH:116-121`, `:197` |
| SG-4 | **What each eager initialiser constructs.** Family counts cover 90 + 227 + 145 + 11 = 473 of 1,172; the remaining entries' targets are not described | `SI:236-238`; `OBJ:199` |
| SG-5 | **`_onexit` table storage and `.CRT$XI` bounds on the teardown page.** `ST` gives neither address; `SI` gives the `__xc` bounds (disputed, X-1) | `ST:115`, `:156` |
| SG-6 | **A consolidated arena-record table.** Fields are scattered over ~20 places; `+0x00`–`+0x07` and `+0x8C`–`+0x8F` are never named | `MEM:107-108`, `:148-153`, `:174-176`, `:1086-1089`, `:1118` |
| SG-7 | **Header fields `+0x1C`, `+0x1E`, `+0x30`, and `+0x15` bits other than 0x02/0x04** | `MEM:1046`, `:1743` |
| SG-8 | **Arena sizes for ids 0, 1 and 10** (12–14 rest on ASTRA's evidence only) | `MEM:126-137` |
| SG-9 | **The link-encoding base value and who sets it** (`01F83530` vs "base `0`" in experiments vs `ptr − arena`) | `MEM:113`, `:147`, `:254`, `:1032` |
| SG-10 | **Arena callees named but not described:** `0036B200` (per-kind choice), `0036B210` (coalescer), `0036B5F0`, `0036C4B0`, `0036D050`, `0036A490`, `0036C660` (tag constant `0x1676`), `0036A190` (difference from `0036A100`) | `MEM:113`, `:115`, `:186`, `:226`, `:303`, `:817-819`, `:1025-1026`, `:1710` |
| SG-11 | **Actor-pool size table contents** (`recordSizeTable` at `DAT_01E0C32A`, `countArray`, `L`) | `MEM:617-618` |
| SG-12 | **EASTL erase / increment / decrement calling conventions and return values**; the empty-anchor state | `OC:95-102`, `:119`, `:123-128` |
| SG-13 | **Offset of the tree head inside its container** (`[rcx+0x10]` read as "first node" vs head +0x10 = root) | `OC:120`, `:264` |
| SG-14 | **Who frees EASTL nodes** (the erase does not) | `OC:507` |
| SG-15 | **SD-82's answer** (inlined rotations): only "answered 2026-09-30" is on the page | `OC:358` |
| SG-16 | **MSVC head initial state** (`_Isnil`, `_Color` red value) and erase / tidy / erase-range interfaces | `MS:111`, `:127-135`, `:381` |
| SG-17 | **Who calls descriptor slot 5, and what adapter argument 1 ("context") is** | `RV:74`, `:92`, `:119-121`, `:414-416` |
| SG-18 | **Bit-exact scalar maths.** No reference `ucrtbase` version; no coefficients | `MATH:74-82`, `:550-554` |
| SG-19 | **Floating-point environment.** MXCSR, FP control word, rounding mode and denormal handling: not stated on any page; `/fp:precise` is inferred | `MATH:628`; `HARD:583-585` |
| SG-20 | **16 of the 45 maths imports are not named** (29 are tabulated) | `MATH:70`, `:94-113` |
| SG-21 | **`VectorPowf4` `0080A270` / core `0080B8A0`**: no algorithm, no coefficients | `MATH:85-87`, `:733-745` |
| SG-22 | **How the turn solver applies `turnRate`, and the speed gate that picks `+0xE4` / `+0xE8`** | `MATH:427-441` |
| SG-23 | **Cookie pseudocode is incomplete**: `r` is used after the `if` when the cookie is not the default; the check's jump target `00808C58` is never shown | `HARD:624-635`, `:645-651` |
| SG-24 | **66 of the 68 scalar-conversion routines** are not described (two are) | `HARD:27`, `:175-177` |
| SG-25 | **Two declared thunk families are not described in the body** (forward-second-argument, call-result) | `TH:32-33` |
| SG-26 | **The full import list.** The page's per-DLL table covers 21 of 30 DLLs; only `iat-any-reference.tsv` has all 538 | `RS:60`, `:63-73` |
| SG-27 | **Service-layer IAT slots used but not named** (`008C2348` "tagged allocator", `008C2368`, `008C2130`, `008C21F8`, `008C20A8`, `008C27E8`, …) and linker-block helpers `00861EC0`, `00861ED2`, `00861EEA`, `00861F20` | `RS:483-535`; `TH:736`, `:794` |
| SG-28 | **Crash dump file name** built by `0079B1E0`: not given | `RS:255`, `:493` |
| SG-29 | **The 27 payload records and nine init callees** of the descriptor-pair families | `LZ:26-28` |
| SG-30 | **Frame-level order.** Apart from the arena-6 latch (`MEM:1891-1893`) and the HUD element (`TH:274-275`), no page says when, within a frame, any runtime service runs. A port of the frame loop gets nothing from this category. | not stated |
| SG-31 | **The 132 sub-threshold generated groups (415 functions)** are deliberately undeclared | `GEN:217-224` |
| SG-32 | **The sized-delete path's leak behaviour** cannot be settled statically, so a port cannot know whether to free | `OBJ:602-604`, `:820-821` |

### 2.3 Fields written by documented functions whose meaning is not given

| # | field | cite |
|---|---|---|
| F-1 | Memory-log record `+0x08`, `+0x0C`, `+0x1C` (never written; purpose not given) | `MEM:572-583` |
| F-2 | `022D8E28` (compared by `0036A490`) and `022D8E20` (the tag, "no reader") | `MEM:303-306` |
| F-3 | Teardown body `mov qword ptr [rsp+0x20], -2 ; EH state` | `ST:73` |
| F-4 | `007DF6D0`'s 0x24 zeroed bytes after the `CRITICAL_SECTION` | `GEN:279-280` |
| F-5 | `003008A0`'s `edx = 0x63` | `GEN:116` |
| F-6 | Locomotion fields `+0xE0`, `+0xBC`, `+0xEC` (untyped) | `MATH:593` |
| F-7 | Record `02D3E880` (0x28 B, zeroed by `00165F80`) | `HARD:185-186` |
| F-8 | HUD singleton `0209BE80` fields `+0x7EA0`, `+0x10F60` / `+0x10F68`, `+0x57E0` | `TH:255-257` |
| F-9 | Container counter `[container+0x28]` (seen, "not adopted") | `OC:289-291` |
| F-10 | YEBIS block (0xD40 B at `02EA0B70`): fields other than the three maps and the current-pointer latches | `MS:197` |
| F-11 | `0036C660`'s header tag constant `0x1676` | `MEM:818-819` |
| F-12 | Region 2's three cells zeroed by `0036D260` | `MEM:1354` |

## 3. Contradictions (statements a re-implementer would have to choose between)

Every quotation below was checked mechanically against the snapshot text at the line cited. A range such as
`SI:336-337` means the quotation wraps across those lines. Each item carries one of two labels:
- "favoured side" is named only where a **dated correction on the pages** settles it;
- "none" means the pages leave the choice open.

Value-changing items (§3.1) disagree on a count, offset, address, constant, formula, function role or ordering.
None can be settled from text alone, so every one is marked **page-text only - needs local check** (the executable
was not available to this session). Stale and banner items (§3.2) do not change a value a port would use. They are
"open" claims that another part of the pages answers, or status lines that disagree.

| group | items | with a favoured side | no favoured side |
|---|---:|---:|---:|
| §3.1 value-changing | 104 | 31 | 73 |
| §3.2 stale "open / not read" | 40 | 27 | 13 |
| §3.2 status banner / front matter | 11 | 1 | 10 |
| **total** | **155** | **59** | **96** |

The value-changing items a port is most likely to trip on are:
- the lazy-guard numeric model (X-2, X-3, X-4);
- the `__xc` table bounds (X-1);
- the identity of `00584730` / `0016D6A0` (X-5, X-6);
- whether `atexit` teardown runs at all (X-10);
- the arena's free-path abort (X-65) and retry behaviour (X-64);
- the arena record's `+0x50` / `+0x62` fields (X-67);
- the accounting-array extent (X-68);
- the link-encoding origin (X-76).

### 3.1 Value-changing — page-text only - needs local check

##### Start-up, static initialisation and lazy statics

#### X-1. Start address of the C++ initialiser table `__xc`

- **Side A:** "start   VA 0x008C31D8" (`SI:52`); "(0x8C5678 - 0x8C31D8) / 8" (`SI:581`); "0x008C31D8" (`OBJ:189`)
- **Side B:** "| **C++** (`__xc`) | `008C31D0` – `008C5678` | **1,172** | `_initterm` |" (`SI:672`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side B's bounds span 1,173 qword slots for "1,172" entries; no page says whether `__xc_a` (`008C31D0`) is a null sentinel. The same shape holds for `__xi`: `008C5680`–`008C56A0` is four slots for "3" entries (`SI:671`).
- **page-text only - needs local check**

#### X-2. Numeric value of a built guard vs the epoch's starting value

- **Side A:** "*guard  >  0   built; value is the epoch at which it completed" (`LZ:250`); "*guard  >  0   built; its value is the epoch at which it completed" (`EH:421`)
- **Side B:** "It ships as `0x80000000` and is" (`SI:342`); "so a thread starts at `INT_MIN`" (`SI:340-341`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Starting at `INT_MIN` and incremented by the footer, epochs stay negative for a long time, so "built" guards would not be `> 0`. The gate test (`thread_epoch < guard`) depends on which reading is right.
- **page-text only - needs local check**

#### X-3. Direction of the lazy-static fast path

- **Side A:** "if (thread_epoch < guard) {          // fast path: already built for this thread -> skip entirely" (`LZ:235`)
- **Side B:** "thread_epoch < guard ?" (`LZ:354`); "no  -> use the object, no lock taken" (`LZ:355`); "thread_epoch >= *guard   ->  skip the whole block, the object is ready" (`EH:427`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: In side A the comment calls the `<` branch the fast path, but the branch body calls `_Init_thread_header`. Side B takes the lock on `<`.
- **page-text only - needs local check**

#### X-4. What the gate compares against

- **Side A:** "compared against a global initialization epoch" (`SI:126`); "if (tlsBlock[+4] < epoch):" (`SI:212`)
- **Side B:** "**there is no single value; the premise is off by one level.**" (`SI:336-337`); "Each accessor compares **its own guard dword** with **this thread's**" (`SI:338`)
- **Favoured side:** B — the T-5 answer dated 2026-09-14 (`SI:335-336`).
- **page-text only - needs local check**

#### X-5. Role of `00584730`: `operator delete` or `_aligned_free` wrapper

- **Side A:** "| `00584730` is `operator delete` |" (`ST:210`); "`00584730` is `operator delete`" (`GEN:266`); "call 00584730     ;   no  -> ordinary operator delete(ptr)" (`OBJ:785`)
- **Side B:** "`00584730` is `if (this) _aligned_free(this)`" (`OBJ:164`); "no `operator new` and no `operator delete`" (`MEM:501`); "00584730  free(p)" (`MEM:739`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: All sides agree on the 10-byte body (`test rcx,rcx / jne 0019C570 / ret`, `ST:210`). What differs is the allocator family a port must pair it with. Separately, `GEN:266` calls it "the one external target of the 224 static teardowns", and `OBJ`'s members files show it shared by other families too.
- **page-text only - needs local check**

#### X-6. Identity of `0016D6A0` (the 3-byte `ret 0`)

- **Side A:** "`_guard_check_icall` — **and** at least one folded empty destructor" (`EH:287`); "`_guard_check_icall_nop`" (`HARD:233`); "`_guard_check_icall` `0016D6A0`" (`GEN:266`)
- **Side B:** "0016D6A0 IS AN ICF-FOLDED ret 0 - a shared empty destructor, not a Control Flow Guard check" (`ST:24`); "**Not specifically `_guard_check_icall`**" (`OBJ:257`)
- **Side C:** "selects the sized-delete stub 0016D6A0 over the _aligned_free wrapper 00584730" (`GEN:82`); "So **bit 2 selects the sized `operator delete` over `_aligned_free`**" (`OBJ:165`)
- **Side D:** "Not that `0016D6A0` is `operator delete(void*, size_t)`" (`OBJ:827`); "`0016D6A0` packs a 0x58-byte record" (`MEM:1870`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: For A–C the behaviour is the same (return at once). Side D's `MEM:1870` gives it a body that writes a record, which contradicts `MEM:679`'s own "`ret 0`".
- **page-text only - needs local check**

#### X-7. Incoming-call counts for `0016D6A0`

- **Side A:** "2,422 ordinary call sites in 2,308 functions" (`EH:287`)
- **Side B:** "**2,471 bodies call `0016D6A0`**" (`OBJ:794`)
- **Side C:** "2,528 `call` and 340 `jmp` sites reach `0016D6" (`HARD:563`)
- **Side D:** "2,479" (`MEM:679`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The pages use different instruments (sites, bodies, call vs jmp, incoming edges). None says how its figure relates to the others.
- **page-text only - needs local check**

#### X-8. Which address is "entry" / "main", and what `007980A0` is

- **Side A:** "`00808D78` (`MSVCCRT.ExecutableStartup`, the entry the config pages reach through `007A3770`)" (`EH:998`); "`007A3770` (the game `main` equivalent)" (`EH:1015`)
- **Side B:** "`007980A0`" (`ST:164`); "is the program's **main body**" (`ST:165`); "`007980A0`, the framework startup" (`RS:252`)
- **Side C:** "`007980A0` — **the crash-dump filter**" (`RS:427`); "`WinMain`'s first guarded instruction is literally `call 007980A0`, the crash-dump filter this table names" (`RS:414-415`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `RS:252-253` itself says the filter is `0079AD50`, installed by `007980A0`. Side C therefore contradicts `RS:252` on the same page.
- **page-text only - needs local check**

#### X-9. When the 224 teardowns' objects are built

- **Side A:** "tail-jumping to `atexit`" (`ST:103`); "before `main`" (`ST:51`)
- **Side B:** "so the objects are function-local statics built on first use" (`ST:150`)
- **Favoured side:** B — UQ-329 ANSWERED 2026-09-17 (`ST:148-150`).
- Note: §3 of `ST` was not revised.
- **page-text only - needs local check**

#### X-10. Whether the `atexit` chain runs at a normal quit

- **Side A:** "It runs at process exit, after the game has stopped" (`ST:139-140`); "They run at normal shutdown, not on an exception." (`EH:547`); "process exit" (`HARD:161`)
- **Side B:** "not executed on a normal quit" (`ST:156`)
- **Favoured side:** B — UQ-331 ANSWERED 2026-09-17 (`ST:156`); the reason given is that the normal quit ends in `ExitProcess(0)` at `0079887F`.
- Note: `SI:225-226` and `LZ:179-184` also describe teardown "at exit" in reverse order without this qualification.
- **page-text only - needs local check**

#### X-11. What the 145 "CFG guard adapters" are

- **Side A:** "### The 145 guard adapters are dead code" (`HARD:141`); "**All 145 of them — 1,740 bytes — are no-ops at runtime.**" (`HARD:153-154`); "The CFG guard adapters." (`EH:682`); "CFG StaticGuardAdapter 145" (`README:51`)
- **Side B:** "**Corrected 2026-09-14 (FABLE, S-3): these are not guard adapters, and they are not dead.**" (`HARD:157`); "the family's earlier name is corrected by this row" (`ST:24`)
- **Favoured side:** B — the dated correction at `HARD:157` (2026-09-14).
- Note: The old reading survives unstruck at `HARD:141`, `:153-155`, `:271`, `:517`, `:760-761`, `EH:682` and `README:51`.
- **page-text only - needs local check**

#### X-12. Whether the game's own code was compiled with `/guard:cf`

- **Side A:** "**CFG compiled in but shipped disabled**" (`README:15`); "`CF_INSTRUMENTED` means the code **was compiled** with `/guard:cf`" (`HARD:85`); "| CFG *was* compiled in |" (`HARD:514`)
- **Side B:** "**So the game's own indirect calls are not instrumented at all**" (`HARD:572`); "The game's own code was not compiled with `/guard:cf`." (`HARD:458-459`)
- **Favoured side:** B — the dated sections of 2026-09-19 (`HARD:552`) and 2026-09-26 (`HARD:443`).
- Note: Side A survives unstruck at `HARD:85`, `:287-289`, `:312-313`, `:514`, `:598`, `:770` and `README:15`.
- **page-text only - needs local check**

#### X-13. Ownership of the eager initialisers attributed to Phyre

- **Side A:** "Phyre's 227" (`SI:236`); "227 of these initializers build Phyre class descriptors" (`SI:570`)
- **Side B:** "317" (`SI:696`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: These may be different selectors (descriptor builders vs owner), but the page does not say so.
- **page-text only - needs local check**

#### X-14. Prototype copy source in `0015BD30`

- **Side A:** "_DAT_01f80130       = _DAT_01df09c0;" (`SI:89`); "Source `0x01DF09C0` sits at the very start of `.data`" (`SI:96`)
- **Side B:** "`01DF09E0` into `01F80140`" (`SI:913`)
- **Side C:** "01DF0980" (`SI:745`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side C puts the prototype cluster before `01DF09C0`, which contradicts "the very start".
- **page-text only - needs local check**

#### X-15. Prototype-copy (`StaticLifetimeInfrastructure`) count

- **Side A:** "| `Runtime.StaticLifetimeInfrastructure` | 145 | prototype copy |" (`SI:164`); "(145)" (`SI:237`); "StaticLifetimeInfrastructure 145" (`README:50`)
- **Side B:** "image-wide it is 149, and only **96** are CRT entries" (`SI:729`)
- **Favoured side:** B — §11, dated 2026-09-02 (`SI:718`); its own words are "Corrected here rather than in place" (`SI:730-731`).
- **page-text only - needs local check**

#### X-16. Roles of `005CC8A0`, the formatter initialiser, and `_Init_thread_header`

- **Side A:** "construct the global in place" (`SI:69`); "`00809C50`" (`SI:898`); "(the lock-init)" (`SI:919`)
- **Side B:** "The memory-status reader `005CC8A0` is called by" (`SI:937`); "The CRT formatter-option initializer `0016D670` is reached from `007A5570`." (`SI:933`); "claims a guard, or waits" (`LZ:192`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `LZ:483` puts the lock's creation in `00809124`, not in `_Init_thread_header`. `SI:785` and `SI:941` also name `00195DF0` differently ("`InputManager_RestoreDefaultBindings`" vs "`InputManager_RestoreDefaultBindingProfiles`").
- **page-text only - needs local check**

#### X-17. Two different things called "the one-time-init lock"

- **Side A:** "the **single** lock shared by all 1,681" (`LZ:211`); "each reference `02EAED40` and nothing else" (`LZ:664`)
- **Side B:** "**The one-time-init lock is a service every layer takes, SERVICE throughout.**" (`LZ:785`); "one-time-init / shared-lock pair this page documents." (`LZ:702`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side B is the `005CD4F0` / `005CD820` `lock cmpxchg` spin-lock pair, which is a different mechanism from the `CRITICAL_SECTION` at `02EAED40`.
- **page-text only - needs local check**

#### X-18. `_Init_thread_wait` callers

- **Side A:** "`_Init_thread_wait` is called from one place, `_Init_thread_header`" (`LZ:668`)
- **Side B:** "Two functions call it in total" (`LZ:669`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-19. What the descriptor-pair accessor `005C3B10` stores

- **Side A:** "`005C3B10` is a three-line accessor that zeroes two words and returns their" (`LZ:131`)
- **Side B:** "lea rax,[record]; mov [static+8],0; or rax,1; mov [static],rax" (`LZ:26`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The members file `descriptor-pair-accessors.tsv` gives `005C3B10` a non-zero record (`02CAD140`), which supports side B.
- **page-text only - needs local check**

#### X-20. Who builds `Phyre::PTTYCallback`

- **Side A:** "`008AADA0` builds `Phyre::PTTYCallback`" (`LZ:130`)
- **Side B:** "Four keep the pointer the `Phyre::PTTYCallback` singleton `005CDA30` returns" (`LZ:517`)
- **Favoured side:** B — BJ-5 ANSWERED 2026-09-26 (`LZ:509`); `bj5-residue.tsv` classes `008AADA0` as `CACHED_PTR`.
- **page-text only - needs local check**

#### X-21. Attribution of the 535 Phyre-reflection holders

- **Side A:** "(535 of 707)" (`LZ:363`)
- **Side B:** "those five give 294" (`LZ:537`); "only the label family gives 535" (`LZ:538`)
- **Favoured side:** B — the BJ-5 bounding dated 2026-09-22 (`LZ:503`).
- Note: Side A attributes 535 to three callees (`00632960` / `00630180` / `006388C0`).
- **page-text only - needs local check**

#### X-22. Does one stuck guard block unrelated statics?

- **Side A:** "a single stuck one can pile unrelated work up behind it" (`LZ:57`); "unrelated first-time initialisations queue up behind it" (`LZ:414`)
- **Side B:** "Two mods hooking different holders cannot" (`LZ:443`); "interfere" (`LZ:444`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `LZ:293` has the wait release the critical section (`SleepConditionVariableCS`), which bears on the choice.
- **page-text only - needs local check**

#### X-23. Role of `00221770`

- **Side A:** "`00221770` (8 B) is the indexed" (`LZ:744`)
- **Side B:** "the one-argument `malloc` thunk" (`LZ:794`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-24. Lock-caller edge counts by subsystem

- **Side A:** "11" (`LZ:704`); "2" (`LZ:707`)
- **Side B:** "22" (`LZ:788`); "4" (`LZ:789`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Audio 11 → 22 and Input 2 → 4. The later figures probably count acquire plus release, but the page does not say so.
- **page-text only - needs local check**

#### X-25. Cookie reference count, and its unit

- **Side A:** "is read from 2,229 functions" (`LZ:457`)
- **Side B:** "2,216 functions reference it." (`LZ:466`); "is read at 2,216 sites" (`HARD:676`)
- **Favoured side:** B — BJ-2 ANSWERED 2026-09-14 (`LZ:459`) favours 2,216 over 2,229.
- Note: No page settles the unit: `LZ` says functions and `HARD` says sites.
- **page-text only - needs local check**

#### X-26. BJ-5 residue counts and the singleton-guard family size

- **Side A:** "12" (`LZ:508`); "finds 39 bodies - the 18 frontier members" (`LZ:27`)
- **Side B:** "**14 descriptor pairs**" (`LZ:513`); "| 17 |" (`LZ:27`)
- **Favoured side:** B — BJ-5 ANSWERED 2026-09-26 (`LZ:509`) and the 2026-09-20 departure in the `LZ:27` row; the `.tsv` files have 14 PAIR rows and 17 rows.
- **page-text only - needs local check**

##### Teardown and exception handling

#### X-27. Census of exception-funclet parents

- **Side A:** "**1,609 distinct parent functions**" (`EH:175`); "386 are unclassified native routines" (`EH:188`); "250 unclassified funclet parents" (`EH:630`)
- **Side B:** "there are **4,314 parents," (`EH:632`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side B is "ANSWERED 2026-09-07" (`EH:631`), but a later note dated 2026-09-14 says "the totals stand" for 1,609 (`EH:191-198`). The two may count different populations (funclet parents vs `FuncInfo` owners); the page does not say.
- **page-text only - needs local check**

#### X-28. Size of the `CompilerGeneratedCpp` and `Thunk` namespaces vs their contents

- **Side A:** "The 2,579 `atexit` thunks in §5 live here." (`EH:679`); "| `Thunk` | 689 |" (`EH:683`)
- **Side B:** "| `CompilerGeneratedCpp` | 417 |" (`EH:679`); "749 non-EH functions are a bare `jmp imm` and 118 are a bare `jmp [rip+k]`" (`EH:551-552`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: 2,579 thunks cannot fit in a 417-function namespace, and 749 + 118 = 867 > 689.
- **page-text only - needs local check**

#### X-29. Group D (128) vs the 75-funclet remainder of the 1,620 "destroy a global" shape

- **Side A:** "**1,545 of the 1,620 "destroy a global" funclets tail-jump to one address, `0080926C`**" (`EH:130`); "75 share the shape of 1,144 atexit thunks" (`EH:625`)
- **Side B:** "| **D** `lea rcx,[rip+.data]; jmp dtor` | **128** |" (`EH:730`); "1,328 of them match an EH skeleton byte for byte" (`EH:548`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Two pairs disagree: 75 vs 128 and 1,144 vs 1,328.
- **page-text only - needs local check**

#### X-30. Self-proving funclets

- **Side A:** "Shape alone is therefore **not** sufficient for 1,762 of the tagged set" (`EH:931-932`)
- **Side B:** "only the 2,133 RDX-frame bodies and the 1,545 `_Init_thread_abort` tails are self-proving" (`EH:932-933`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: 3,895 − 2,133 = 1,762 leaves out the 1,545 that side B calls self-proving.
- **page-text only - needs local check**

#### X-31. `00194CD0`: `ostream` inserter or call-free funclet

- **Side A:** "`00195310` of **`00194CD0`** (`ostream` inserters" (`EH:760`)
- **Side B:** "`00194CD0` (455 B) is a call-free exception funclet" (`EH:1025`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side B (2026-09-19) is later, but it conflicts with "The largest body in the entire set is **158 bytes**" (`EH:125-126`).
- **page-text only - needs local check**

#### X-32. Role of `0061ECF0`

- **Side A:** "`0061ECF0`" (`EH:1006`)
- **Side B:** "the `return 1` stub the lazy-guard callers use as their success sentinel" (`EH:1041-1042`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: In side A it drives `__isa_available_init` and the `02EAED38` shutdown path (`EH:1006`, `:1013`). No lazy-guard caller is named.
- **page-text only - needs local check**

#### X-33. Unwind-funclet count in the README

- **Side A:** "EH unwind funclets 3,813" (`README:49`)
- **Side B:** "3,820" (`EH:783`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-34. `CxxObjectLifecycle` namespace size

- **Side A:** "| `CxxObjectLifecycle` | 225 |" (`EH:680`); "915 functions" (`OBJ:26`)
- **Side B:** "**916 functions** *(GN161; R109 added one `CxxObjectLifecycle` member)*" (`README:36`); "226" (`OBJ:62`)
- **Favoured side:** B — `README:36` / `OBJ:62-63` record the GN161 batch R109 addition.
- Note: Separately, `OBJ`'s own `CxxObjectLifecycle` sub-labels add to 248: 135 deleting-destructor (`OBJ:139-142`), 85 `VtableInstall*` (`:236-237`) and 28 `ConditionalTeardownReturnTrue` (`:404`). That exceeds both 225 and 226, and no page reconciles it.
- **page-text only - needs local check**

#### X-35. Family counts in `ST` rows: count column vs row prose

- **Side A:** "PROVED BY FORM - 61 members" (`ST:26`); "27 members" (`ST:28`); "328 members" (`ST:32`); "PROVED BY CONTROL - 12 members" (`ST:42`); "the remaining **108** are declared **B**" (`ST:133-134`)
- **Side B:** "| 65 |" (`ST:26`); "| 24 |" (`ST:28`); "| 327 |" (`ST:32`); "| 6 |" (`ST:42`); "| 107 |" (`ST:46`)
- **Favoured side:** B — the dated joins and departures inside each row (`ST:26` 2026-09-17, `:28` 2026-09-29, `:32` 2026-09-20, `:42` 2026-09-20, `:46` 2026-10-01); all match their `members/*.tsv` row counts.
- Note: Exception: for `ST:26`, 61 − 5 + 12 = 68 ≠ 65, so that row's own arithmetic still does not close.
- **page-text only - needs local check**

#### X-36. The 530-body 32-byte initialiser form

- **Side A:** "the generic remainder of the 530-body 32-byte form" (`ST:31`)
- **Side B:** "the 319 PInputs" (`ST:31`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The same row lists 319 + 110 + 56 + 44 = 529 (or 528 with the current 43).
- **page-text only - needs local check**

#### X-37. Frontier leftovers in the `.CRT$XI` array

- **Side A:** "83 frontier array members" (`ST:117`)
- **Side B:** "# 87 .CRT$XI entries in the frontier after the 2026-09-19 cluster declarations." (`LO:2`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `LO` is `Static-Initialization-And-Teardown/members/xc-array-frontier-leftovers.txt`. It still lists the four rows `ST:121-124` says became a family. The six grow-helper departures that "returned to the frontier undeclared" (`ST:42`) appear in neither list.
- **page-text only - needs local check**

#### X-38. `00632BE0`: deleting destructor (`??_G`) or constructor

- **Side A:** "`??_G` cluster window" (`ST:218`)
- **Side B:** "`00632BE0` (170 B) is the sibling constructor" (`ST:220`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-39. Roles of `0059A030` and `0067F700`

- **Side A:** "bootstrap lookup 0059A030" (`ST:24`); "0067F700 tree insert" (`HARD:27`); "ordered-insert 0067F700" (`ST:24`)
- **Side B:** "is the static-init driver" (`ST:224`); "is the call-free CRT `_Tree` node relink" (`ST:228`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `HARD:178` calls `0059A030` the conversion-tree lookup. `LZ:106` tags `0067F700` `ContainerStringSupport`, and `OC:541` calls it the Phyre tree.
- **page-text only - needs local check**

##### Object deletion and generated families

#### X-40. `AlignedOrGuardedFree` population

- **Side A:** "| `CxxObjectLifecycle.DeletingDestructor.AlignedOrGuardedFree` | 53 |" (`OBJ:140`)
- **Side B:** "The 63 `AlignedOrGuardedFree` members" (`OBJ:145`)
- **Side C:** "| 46 |" (`GEN:30`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `OBJ:168`, `:257`, `:411`, `:425` and `:595` also use 63. The `GEN:30` row says "PROVED BY FORM - 53 members" with one departure, which gives 52; its members file has 46 rows.
- **page-text only - needs local check**

#### X-41. Meaning of flag bit 2 in a deleting destructor

- **Side A:** "if (flags & 4)  free(base, size);          /* array: free the whole block  */" (`OBJ:287`)
- **Side B:** "**Bit 2 selects the sized `operator delete` over `_aligned_free`.**" (`OBJ:594`); "the bit-2 path **these destructors free nothing at all**" (`OBJ:602`)
- **Favoured side:** B — the dated answer at `OBJ:408`, "**ANSWERED 2026-09-02, and the question's framing was wrong** — it is **not** the vector form.".
- **page-text only - needs local check**

#### X-42. Which branch of the two-bit destructor actually frees

- **Side A:** "-> free 00809950  or the aligned/guarded path via 0016D6A0" (`OBJ:317`)
- **Side B:** "Only the `_aligned_free` side actually releases memory." (`OBJ:183`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-43. Roles of `00210EC0`, `0085E730` and `0019C580`

- **Side A:** "`00210EC0` → the `malloc` import" (`OBJ:417`); "malloc(0x18) via 0085E730" (`OBJ:35`); "`0019C580` (9 B) is the `_aligned_malloc` import thunk itself" (`TH:786`)
- **Side B:** "`00210EC0` is the aligned allocator the object constructors call" (`GEN:266`); "`0085E730`, the free/dealloc entries this corpus has identified" (`OBJ:986`); "The `_aligned_malloc` wrapper `0019C580`" (`RS:566`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `MEM:527` calls `0019C580` an "aligned-malloc adapter". It is not in `external-import-stubs.tsv`.
- **page-text only - needs local check**

#### X-44. Which labels make up "the 88 teardowns"

- **Side A:** "| `CompilerGeneratedCpp.GuardedStaticObjectTeardown` + `StaticContainerTeardown.*` | 88 |" (`OBJ:212`)
- **Side B:** "`CxxObjectLifecycle.ConditionalTeardownReturnTrue` (28)" (`OBJ:404`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `GEN:38` and `GEN:40` list `ConditionalTeardown` (28 × 44 B) and `GuardedStaticObjectTeardown` (28 × 21 B) as different families.
- **page-text only - needs local check**

#### X-45. Internal sums in `OBJ`

- **Side A:** "scored `CxxObjectLifecycle.ScalarDeletingDestructor` at **0 of 135**" (`OBJ:457-458`); "566 of the 70" (`OBJ:503`)
- **Side B:** "63" (`OBJ:139`); "117" (`OBJ:210`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The two sub-label rows for that label are 63 + 9 = 72, not 135. "566 of the 707" outside the families leaves 141 inside, against 117 + 23 = 140 (`OBJ:210-211`). The owner breakdowns at `OBJ:330-331` (sum 166 of 178) and `:168-169` (1,537 of 1,545) also fall short.
- **page-text only - needs local check**

#### X-46. BQ-27 site arithmetic

- **Side A:** "at none of the 262 sites" (`OBJ:803`); "The live target is the remaining **61** sites" (`OBJ:820`)
- **Side B:** "all 263 literal flags here are written as 32-bit `edx`" (`OBJ:816`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: From the page's own figures, 345 − 217 − 19 − 47 = 62, not 61.
- **page-text only - needs local check**

#### X-47. BQ-23 sub-counts

- **Side A:** "`OrderedContainerRuntime.*` 19" (`OBJ:370`)
- **Side B:** "| `OrderedContainerRuntime.*` | **30** |" (`OBJ:384`)
- **Favoured side:** B — the ANSWERED 2026-09-27 line (`OBJ:401`), which uses 18 + 3 + 9 = 30.
- Note: Also within BQ-23, with no favoured side: "the 24 regex-span members" vs "`StdRegex.Runtime` 21" (`OBJ:370` vs `:383`), and 31 + 6 = 37 vs 40 (`OBJ:369` vs `:382`).
- **page-text only - needs local check**

#### X-48. `005CD6D0` caller count

- **Side A:** "4 A-measured callers" (`OBJ:854`)
- **Side B:** "has six audio callers" (`OBJ:1102`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-49. `00194F50`: CRT `filebuf` body or sound request

- **Side A:** "filebuf vtable" (`OBJ:745`)
- **Side B:** "`00194F50` (270 B) is a sound-request body" (`OBJ:1028`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-50. `GEN`: fifty-five families vs the front matter

- **Side A:** "The fifty-five rows are in this page's frontmatter" (`GEN:249`); "ten or more" (`GEN:211-212`)
- **Side B:** "| 2 |" (`GEN:185`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The `GEN` front matter has 178 family rows. 100 of them are below the stated ten-member threshold, and the declared counts sum to 3,351, not 1,236. That figure is my count of the rows; the page does not state it.
- **page-text only - needs local check**

#### X-51. `GEN` row counts that do not close

- **Side A:** "38 are declared here" (`GEN:33`); "11 members" (`GEN:100`)
- **Side B:** "| 8 |" (`GEN:33`); "| 10 |" (`GEN:100`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `GEN:33`: 38 − 27 − 1 = 10, but the row says 8. Same shape at `GEN:64` (18 − 3 = 15 vs 16) and `GEN:78` (9 − 2 = 7 vs 8). `GEN:100`'s members file has 11 rows; it is the only `.tsv` mismatch on `GEN`.
- **page-text only - needs local check**

#### X-52. `VtableInstall*` counts across pages; role of `006B6700`

- **Side A:** "| 60 |" (`OBJ:236`); "register the member fn via 006B6700" (`GEN:98`)
- **Side B:** "| 40 |" (`GEN:37`); "destroys the member at `+0x38` (`006B6700`)" (`GEN:270`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

##### Ordered containers and adapters

#### X-53. Byte sizes of MSVC rotation pair C

- **Side A:** "| `00799BD0` / `00799C30` | 89 / 85 B |" (`OC:477`)
- **Side B:** "| `00799BD0` | 85 | 1 | rotation, pair C |" (`MS:123`); "| `00799C30` | 89 |" (`MS:124`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The `MS` members file agrees with side B.
- **page-text only - needs local check**

#### X-54. EASTL members with zero callees

- **Side A:** "four of the six members" (`OC:380`)
- **Side B:** "both iterator steps, the insert and both rotations" (`OC:380-381`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side B lists five, and so does the key-address table (`OC:136-140`). `OC:430` repeats "four of the six".
- **page-text only - needs local check**

#### X-55. EASTL callers by subsystem

- **Side A:** "| **Audio** | 13 |" (`OC:214`)
- **Side B:** "**Audio, 46:**" (`OC:582`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side A is Audio 13, Presentation 7, Resource 5, Platform 2 (`OC:213-217`). Side B is Audio 46, Presentation 14, Resource 8, Platform 4 (`OC:582-585`).
- **page-text only - needs local check**

#### X-56. "99 call sites" vs 99 callers / 213 sites

- **Side A:** "99 call sites across audio, text, effects and resource loading" (`OC:304`)
- **Side B:** "**99 distinct callers**" (`OC:207-208`); "**213 call sites**" (`OC:249`)
- **Favoured side:** B — the census at `OC:248-250`.
- **page-text only - needs local check**

#### X-57. Return-value adapter `00624580`: slot 5 or slot 3, and family membership

- **Side A:** "`00624580`, each at slot 5 of its descriptor triple" (`RV:443`); "Every one of the 403 has size 26" (`RV:83`)
- **Side B:** "`00624580` (~32 B) — the standard" (`RV:457`); "slot-3 adapter" (`RV:458`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `df4-return-value-adapters.tsv` has 402 rows and no `00624580`. `RV:28` declares 402 against "403 matches" (`RV:251`).
- **page-text only - needs local check**

#### X-58. Adapter count: 401 vs 403; the 351 as family size

- **Side A:** "401 adapters exist" (`RV:182`); "the only field that differs between the 351" (`RV:76`)
- **Side B:** "**403 / 403**" (`RV:254`); "`351` is a *tag* count" (`RV:259`)
- **Favoured side:** B — DF-5 ANSWERED 2026-09-14 (`RV:331`): "403 adapters = 401 + 2" (`RV:361`).
- **page-text only - needs local check**

#### X-59. Class names behind the shared adapters; role of `0061A250`

- **Side A:** "`PPoint3`, `PQuat`, `PVector2`, `PVector3` **and** `PVector4`" (`RV:141-142`); "`PClassDescriptorConcrete` class body" (`RV:463`)
- **Side B:** "`Vectormath::Scalar::Aos::Matrix3`" (`RV:295`); "**`Phyre.ScriptVM.ObjectPointerAccessor`**" (`RV:408-409`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-60. Does every MSVC tree body test `_Isnil`?

- **Side A:** "Every body in this family tests it" (`MS:71`)
- **Side B:** "**`0071EE70`, the payload destructor, carries no `_Isnil` test at all**" (`MS:254-255`)
- **Favoured side:** B — MT-3 ANSWERED 2026-09-15 (`MS:251-253`).
- **page-text only - needs local check**

#### X-61. MSVC member count, and outbound calls

- **Side A:** "**23 bodies, 6,630 bytes.**" (`MS:137`); "No member calls outside the family except to `free` and to `0071EE70`" (`MS:295-296`)
- **Side B:** "| 22 |" (`MS:30`)
- **Favoured side:** B — for the count: `MS:30` "2026-09-30, OPUS: 00714B00 left the row - it is measured A".
- Note: The members file's header still says 23 members but it holds 22 rows. It lists callee `001DFA10` for `0071EE70`, which contradicts `MS:295-296`; that sub-point has no favoured side.
- **page-text only - needs local check**

##### Memory arena

#### X-62. How many heap doors are called

- **Side A:** "through exactly **six** doors" (`MEM:35`); "Six of the eight are actually called:" (`MEM:83-84`)
- **Side B:** "~~**0**~~ **1**, through the import thunk `00862046`" (`MEM:95`)
- **Favoured side:** B — the row correction dated 2026-09-30 (`MEM:95`); the headline counts were not updated.
- **page-text only - needs local check**

#### X-63. "Does not grab one big block at startup" vs the boot arenas

- **Side A:** "it does not grab one big block at startup and live inside it the way a console game does." (`MEM:49-50`)
- **Side B:** "About 256 MiB in all, from the CRT heap." (`MEM:134`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-64. What the retry allocator `0036BFE0` does when allocation keeps failing

- **Side A:** "**With a static kind and a failing allocator it spins forever**" (`MEM:1164-1165`)
- **Side B:** "`0036BFE0` returns null only when" (`MEM:67`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side B (2026-09-28/30) is later than side A (2026-09-19), but it does not say it corrects A.
- **page-text only - needs local check**

#### X-65. How the free path aborts

- **Side A:** "takes a diagnostic path ending in an imported `exit(1)`" (`MEM:219`)
- **Side B:** "routes to `0036A570`, calls through the hook cell `q[008C2D80]`, and executes `int3`." (`MEM:1092-1093`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The EXP-126 fold-in (2026-09-20, `MEM:1643-1647`) corrects the number of gates (three → six) but not the exit mechanism. `ST:156` lists `00369860` among the CRT `exit` callers.
- **page-text only - needs local check**

#### X-66. Free-gate count

- **Side A:** "is gated three ways before it reclaims anything" (`MEM:218`)
- **Side B:** "the gates are **six**, ordered" (`MEM:1646-1647`)
- **Favoured side:** B — the EXP-126 fold-in dated 2026-09-20 (`MEM:1643`).
- **page-text only - needs local check**

#### X-67. Arena record `+0x50` and `+0x62`

- **Side A:** "**binary tree root at `+0x50`**" (`MEM:199`); "`+0x62`" (`MEM:1118`)
- **Side B:** "`+0x50` pool pointer" (`MEM:1118`); "is a movement-since-clear latch" (`MEM:1890`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `MEM:1118` itself calls `+0x02`/`+0x62` "live marks"; `MEM:1890` (2026-09-23) calls `+0x62` a latch.
- **page-text only - needs local check**

#### X-68. Extent of the accounting array at `022D8E10`

- **Side A:** "closed — the array is two elements" (`MEM:1477`); "**`022D8E18` is element 2 and is never reached.**" (`MEM:1497-1498`)
- **Side B:** "establishes it is an **8-element dword array at stride 4, indexed by `[rec+0x17]`" (`MEM:1359`)
- **Side C:** "the index is 0..15" (`MEM:1523`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side C (OPUS, 2026-10-02) reopens the closure for the forwarding path, so the dated chain ends open.
- **page-text only - needs local check**

#### X-69. Role of `022D8E1C`

- **Side A:** "`022D8E1C` is the arena allocator's fallback" (`MEM:302`); "the fallback byte" (`MEM:1412`)
- **Side B:** "failure code" (`MEM:1158`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-70. Which function owns the map write at `0036A290`

- **Side A:** "`0036A290` in `0036A280`" (`MEM:291`)
- **Side B:** "`0036A240` (63 B)" (`MEM:1545`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: A 63-byte body starting at `0036A240` ends at `0036A27E`, before `0036A290`.
- **page-text only - needs local check**

#### X-71. Selection stack: does the push install the active arena, or does the pop stage it?

- **Side A:** "the active arena through the map" (`MEM:291`)
- **Side B:** "the pop stages it into `022D89BC`" (`MEM:1197`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `MEM:1214-1215` adds that the pushed `r9` becomes "the *next* staged qword — a pipeline register".
- **page-text only - needs local check**

#### X-72. Number of push sites

- **Side A:** "(135 call sites)" (`MEM:284`)
- **Side B:** "136 call sites into `0036C1D0` / `0036C1F0`" (`MEM:1439`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-73. `0036A2A0`: record clone or relocation

- **Side A:** "is a **record clone**" (`MEM:1312-1313`)
- **Side B:** "**SECTION-07 correction:**" (`MEM:1316`); "is the actual selected-block relocation producer" (`MEM:1878`)
- **Favoured side:** B — SECTION-07, dated 2026-09-23 (`MEM:1874`).
- Note: The GN162 class name `RecordClone` (`MEM:1285`) and `MEM:1432` still say clone.
- **page-text only - needs local check**

#### X-74. Header bytes `+0x30`..`+0x3D`

- **Side A:** "`+0x30 encodedRef30`" (`MEM:1734`)
- **Side B:** "the undeclared `0x30`–`0x3D` region" (`MEM:246`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `MEM:1736` says nine bytes from `+0x35` "stay unobserved", while `MEM:247`, `:1313-1314` and `:115` read a NUL-terminated 7-character name at `+0x34`.
- **page-text only - needs local check**

#### X-75. "Mark" at `+0x3E` vs `+0x02`

- **Side A:** "**mark word**" (`MEM:1049`)
- **Side B:** "the mark byte" (`MEM:1146`); "guard word" (`MEM:231`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `MEM:1146` writes `[rbx - 0x3e]`, which is header `+0x02`, not `+0x3E`.
- **page-text only - needs local check**

#### X-76. Origin of the block-link encoding

- **Side A:** "`01F83530`" (`MEM:113`)
- **Side B:** "d[link] = ptr − arena" (`MEM:1032`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side A encodes relative to a global base; side B encodes relative to the arena (`MEM:1148`, `:1154`).
- **page-text only - needs local check**

#### X-77. Name lookup in `00676BD0`; key order in the asset registry

- **Side A:** "the hash, then `memcmp`" (`MEM:923`); "**length-first key comparison**" (`MEM:896-897`)
- **Side B:** "`00674F60`" (`MEM:1852`); "It is not a length-first comparison." (`MEM:920-921`)
- **Favoured side:** B — for the key order only: UQ-326 ANSWERED 2026-09-25 (`MEM:902`).
- Note: For the `00676BD0` tie-break, side B (`MEM:1852-1862`, 2026-09-21) describes a three-way dword compare with `strchr('#')` / substring / `memcmp` / `strncmp`; no favoured side.
- **page-text only - needs local check**

#### X-78. Audio buffer size formula

- **Side A:** "channels × 48000 × 4" (`MEM:540`)
- **Side B:** "seconds × 48 kHz × 4 bytes" (`MEM:868-869`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-79. Role of `0036D2F0`

- **Side A:** "**one display-geometry object**" (`MEM:1355`)
- **Side B:** "is the pool-descriptor build" (`MEM:1870`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-80. Caller counts for the allocation wrappers

- **Side A:** "228" (`MEM:529`); "230" (`MEM:523`)
- **Side B:** "88 frontier callers" (`MEM:1559`); "104 frontier callers" (`MEM:1568`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `0017D260` 228 vs 88 and `001EDF00` 230 vs 104. "frontier" may explain it; the page does not say.
- **page-text only - needs local check**

#### X-81. Arena record `+0xA0`: per-kind constructor or callback slot

- **Side A:** "per-kind constructor" (`MEM:1118`)
- **Side B:** "the heap's callback slot" (`MEM:67`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

##### Thunks and the runtime service surface

#### X-82. Size of the five-byte `E9` forwarder population

- **Side A:** "**749 functions have a complete body of exactly five bytes, `E9 rel32`.**" (`TH:493`)
- **Side B:** "**835 forwarders, 819 flagged, 16 unflagged**" (`TH:326`); "all 835 forwarders" (`TH:4`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Both use the same selector; `internal-tail-call-forwarders.tsv` has 749 rows. `TH:31`, dated 2026-09-18, still says 749.
- **page-text only - needs local check**

#### X-83. Ghidra thunk flag: 677/12 vs 819/16

- **Side A:** "**It does not do this for 12**" (`TH:110-111`); "There is none in the tagged population" (`TH:461`)
- **Side B:** "**819 flagged, 16 unflagged**" (`TH:237`)
- **Favoured side:** B — "superseded on 2026-09-14 by the 819/16 cross-tabulation" (`TH:229`); 677/12 still holds for the tagged 689.
- **page-text only - needs local check**

#### X-84. `InternalForwarder` count

- **Side A:** "indistinguishable from the 528 it does flag" (`TH:112`)
- **Side B:** "**`InternalForwarder` 560, `ExternalImport` 117, `DirectTailForwarder` 12**" (`TH:448`)
- **Favoured side:** B — §10, dated 2026-09-03 (`TH:69`, "corrected in §10").
- **page-text only - needs local check**

#### X-85. The 7-byte import bodies: same encoding or compiled functions

- **Side A:** "| 7 bytes | 12 | the same indirect jump, longer encoding |" (`TH:64`); "`0019A650` is the canonical shape" (`TH:71`)
- **Side B:** "**The 7-byte bodies are compiled functions whose entire code is a tail jump to an import**" (`TH:250`)
- **Favoured side:** B — BU-2 ANSWERED 2026-09-13 (`TH:250`) for the encoding.
- Note: Whether `0019A650` is "canonical" (`TH:71-73`, `:132`) is not separately settled.
- **page-text only - needs local check**

#### X-86. IAT-reaching indirect-jump bodies: 118 vs 117

- **Side A:** "**109 `FF 25`** and **10 `48 FF 25`** bodies" (`TH:250`)
- **Side B:** "gives **117 stubs**" (`TH:562`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side A gives 109 + 10 = 119; minus the CFG dispatcher, that leaves 118.
- **page-text only - needs local check**

#### X-87. `TH` family rows: count column vs prose

- **Side A:** "82 members" (`TH:32`); "85 members" (`TH:33`)
- **Side B:** "| 72 |" (`TH:32`); "| 29 |" (`TH:33`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The members files agree with side B (72 and 29 rows, headers "restated" 2026-09-18). The page records departures that do not account for the difference.
- **page-text only - needs local check**

#### X-88. Thunk definition vs members that are not one jump

- **Side A:** "689 functions whose entire body is a jump" (`TH:39`); "The complete content of a thunk is one instruction." (`TH:149`)
- **Side B:** "**not a forwarder at all**" (`TH:65`); "`00249180` (35 B) is the forwarding" (`TH:757`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `TH:685` also calls the predicate `00377C20` a thunk, whereas `TH:122` calls it a "78-byte predicate".
- **page-text only - needs local check**

#### X-89. Argument order of `00249180`; packet size in `00280750`

- **Side A:** "`00249180(rcx, 7, 0xD6, 3, 1, 00246A10)`" (`TH:802`)
- **Side B:** "`00249180(rsi, 7, 3, 0xD7, proc 00280740)`" (`TH:810`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `TH:810` also says "an eleven-pointer packet of `01E0C1xx` thunk cells", but it lists ten `009152A0`…`009153D0` addresses and "the ten `[rcx+0x338..+0x388]` slots", a range of 11.
- **page-text only - needs local check**

#### X-90. Import surface: 30 DLLs / 538 symbols vs the per-DLL table

- **Side A:** "**30 DLLs, 538 imported symbols.**" (`RS:60`)
- **Side B:** "MSVCP140" (`RS:64-65`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The table at `RS:63-73` has 21 DLLs summing to 502. It omits the heap, time, filesystem, convert, utility and environment CRT sets, plus OLEAUT32, SHELL32 and dwmapi. `iat-any-reference.tsv` has 538 rows over 30 DLLs. The page uses `_wmkdir` (filesystem) and `SysAllocStringLen` (OLEAUT32) itself (`RS:262`, `:302`).
- **page-text only - needs local check**

#### X-91. Which debug messages are not PPFX

- **Side A:** "**The game's own code contributes nothing to this channel**" (`RS:231`)
- **Side B:** "| Audio (SEAD), calling the API directly | **90** | 147 |" (`RS:105`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-92. Role of `005CD1E0`

- **Side A:** "The Phyre thread creator `005CD1E0`" (`RS:477`)
- **Side B:** "The SEH-filter parent `005CD1E0`" (`RS:569`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `EH:337` lists it as the parent of filter `0089BEF0`, and `RS:429` has it guarding `RaiseException(0x406D1388)`.
- **page-text only - needs local check**

#### X-93. Debug-wrapper call sites: 800 or 801

- **Side A:** "**801** call sites" (`RS:219`)
- **Side B:** "**was 800**" (`RS:375`)
- **Favoured side:** B — the falsification pass dated 2026-09-07 (`RS:357`, `:375-376`): 800 `call` + 1 `jmp` = 801.
- **page-text only - needs local check**

##### Hardening and maths

#### X-94. Section sizes in `HARD` §2 vs the corrected table

- **Side A:** "| `.tls` | `0x02EE4000` | `0x200` |" (`HARD:217`); "| `.reloc` | `0x02F3C000` | `0x39400` |" (`HARD:220`); "`0x7A0800`" (`HARD:211`)
- **Side B:** "| `.tls` | `0x03004000` | `0x9` |" (`HARD:815`); "`0x39360`" (`HARD:818`); "`0x7A0635`" (`HARD:809`)
- **Favoured side:** B — the "OVERTURNED" correction dated 2026-09-02 (`HARD:781`, `:801-803`, `:825-826`).
- Note: `.rdata`, `.pdata`, `.rodata`, `_RDATA` and `.rsrc` differ in the same way (`HARD:212-219` vs `:810-817`). §2 was never edited.
- **page-text only - needs local check**

#### X-95. Where a debugger at `0x02F3C000` lands

- **Side A:** "lands 1.1 MB short of `.reloc`, inside `.pdata`." (`HARD:798`)
- **Side B:** "`.data`" (`HARD:811`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The corrected table puts `.data` at `0x01DF0000` + `0x11A7530` = `0x02F97530` and `.pdata` at `0x02F98000`, so `0x02F3C000` falls inside `.data`. This is my arithmetic from the page's own table.
- **page-text only - needs local check**

#### X-96. Scalar-conversion initialiser family size

- **Side A:** "**144 are the nodes of one ordered tree**" (`HARD:165`)
- **Side B:** "| 142 |" (`HARD:27`)
- **Favoured side:** B — for family membership: the dated departures (2026-09-29 and 2026-09-30) in the `HARD:27` row.
- Note: 144 remains the tree-node count. The members file's header comment still says 144, over 142 rows.
- **page-text only - needs local check**

#### X-97. Number of SSE square-root instructions

- **Side A:** "only **four** SSE `sqrt` instructions in the whole 7.5 MB of code" (`MATH:30-31`)
- **Side B:** "~~13~~ **14**" (`MATH:125`)
- **Favoured side:** B — "Corrected 2026-09-07" (`MATH:654-655`); the opening line (`MATH:30`) was never qualified to scalar.
- **page-text only - needs local check**

#### X-98. Whether `rsqrtps` is the geometry path

- **Side A:** "The geometry path is the `rsqrtps` + Newton–Raphson normalise" (`MATH:759-760`)
- **Side B:** "**The geometry path has no SIMD in it at all.**" (`MATH:164`)
- **Favoured side:** B — the same-pass correction (`MATH:663-666`): all 14 `sqrtps` and all 10 `rsqrtps` sites are Audio-owned.
- **page-text only - needs local check**

#### X-99. What `02EBF190`+0x5B0E is, and its range

- **Side A:** "settings object pointer" (`MATH:371`); "Whether `n` can reach 31 depends on the settings byte at `+0x5B0E`" (`MATH:465-466`)
- **Side B:** "**Answered 2026-09-14 (FABLE):** it is not a setting." (`MATH:564`)
- **Favoured side:** B — UQ-320 ANSWERED 2026-09-14 (`MATH:564`): "it **never exceeds 17**".
- **page-text only - needs local check**

#### X-100. `sqrtss` sites: attributed or not

- **Side A:** "All four `sqrtss` sites are FFXII's own code" (`MATH:594-595`)
- **Side B:** "The unattributed maths sites `007D0F60`, `007D1140` and `007E9030`" (`MATH:871`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-101. Width of the fabs mask at `01CEBD80`

- **Side A:** "`0x7FFFFFFFFFFFFFFF`" (`MATH:368`)
- **Side B:** "`0x7FFFFFFF` mask at" (`MATH:839`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

#### X-102. Number of SIMD cluster functions

- **Side A:** "all eleven cluster functions disassembled in full" (`MATH:630`)
- **Side B:** "**missed by the original scan**" (`MATH:339`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The §3 table lists 12 (`MATH:331-342`). The 2026-09-29 list (`MATH:868-869`) names 11 and leaves out `007F1670`.
- **page-text only - needs local check**

#### X-103. Owners with "no transcendental maths" vs later client edges

- **Side A:** "contain **no transcendental maths whatsoever**" (`MATH:315`)
- **Side B:** "CombatAI, CombatAction and WorldAreaField — CLIENT, 26 edges" (`MATH:876`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The loot searches reach `sqrtf` through `004686D0` (`MATH:326`, `:888-893`). Side A counts only direct import callers (`MATH:294`).
- **page-text only - needs local check**

#### X-104. Users of the 1°-in-radians constant

- **Side A:** "the only non-third-party user of the 1°-in-radians constant" (`MATH:325`)
- **Side B:** "each is referenced from more than one place" (`MATH:540-541`)
- **Favoured side:** none. No dated correction on the pages settles it.
- **page-text only - needs local check**

### 3.2 Stale "not read / open" claims and banner disagreements

#### Stale claims

#### S-1. "117 lazy statics" repeated after the §12 correction

- **Side A:** "and **117** lazy statics" (`SI:577`); "The **117** lazy function-local statics and the family counts in §2 were not recounted this pass." (`SI:640`)
- **Side B:** "**1,681 distinct thread-safe function-local statics, reached from 1,732 guarded construction" (`SI:821`)
- **Favoured side:** B — `## 12. REOPENED and corrected 2026-09-02 (fourth pass)` (`SI:807`).

#### S-2. The correction claims it appears "only in this document"

- **Side A:** "It appears **only in this document**" (`SI:879`)
- **Side B:** "(117 functions)" (`LZ:389`); "(117/117 and 23/23)" (`README:38`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `LZ:620` also carries it. Those uses are tag-scoped, but the statement undercounts the places the figure appears.

#### S-3. T-1: "may span both C and C++ tables"

- **Side A:** "initializers", which may span both C and C++ tables." (`SI:376`)
- **Side B:** "**The entire 1,172-entry run is C++.**" (`SI:674`)
- **Favoured side:** B — §10, second pass, 2026-09-02 (`SI:643`).

#### S-4. T-8: Audio clusters "unidentified"

- **Side A:** "and are unidentified. **T-8.**" (`SI:803`)
- **Side B:** "**SQEX Sead's static pools" (`SI:303`)
- **Favoured side:** B — "Answered on the page 2026-09-14 (FABLE)" (`SI:303`).

#### S-5. T-4: withdrawn and closed, yet "not closed"

- **Side A:** "**T-4.** *(closed — the register row is WITHDRAWN.)*" (`SI:329`)
- **Side B:** "*Bounded 2026-09-22 (FABLE), not closed:*" (`SI:330`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The withdrawal is undated.

#### S-6. T-6 ticked with no answer on the page

- **Side A:** "box ticked in a follow-up" (`SI:291`)
- **Side B:** "**Not claimed:** that these shares reflect startup *time*." (`SI:715`)
- **Favoured side:** none. No dated correction on the pages settles it.

#### S-7. T-9 (`.gfids` dwords) "deliberately left open" vs answered

- **Side A:** "and it is deliberately left" (`SI:399`); "Why `T-9` stays open" (`HARD:110`); "`S-2` and `T-9` stay open." (`HARD:474-475`)
- **Side B:** "***Answered 2026-09-27 (FABLE, Claude Opus 5.5): they are the statically linked C/C++ runtime's own `.gfids$y` data.**" (`HARD:124`)
- **Favoured side:** B — the answer dated 2026-09-27 (`HARD:124`); three of the twelve values are "inferred".

#### S-8. BJ-1 / BJ-3 "need a live process"

- **Side A:** "BJ-1 and BJ-3 both need a" (`LZ:683`); "not visible statically" (`LZ:480`)
- **Side B:** "*ANSWERED 2026-09-28 (FRONTIER ruling, carried residue): live-only by measurement" (`LZ:452`)
- **Favoured side:** B — BJ-3 answered statically 2026-09-14 (`LZ:481-482`), BJ-1 ANSWERED 2026-09-28 (`LZ:452`).

#### S-9. The 136 funclet-less statics "not attempted"

- **Side A:** "individual verification of the 136 magic statics without a funclet." (`EH:986-987`)
- **Side B:** "*Answered 2026-09-26 (OPUS): all 136 verified" (`EH:627`)
- **Favoured side:** B — the answer dated 2026-09-26 (`EH:627`).

#### S-10. Group D's identity "rests on tier 8"

- **Side A:** "They currently are not" (`EH:624`); "relies on tier 8 for its *identity*" (`EH:6`)
- **Side B:** "*Answered 2026-09-26 (OPUS)" (`EH:625`)
- **Favoured side:** B — B-2/b answered 2026-09-26 (`EH:625`); the front-matter tier note (`EH:6`) was not updated.

#### S-11. `0016D6A0` described as `ret` vs `ret 0`

- **Side A:** "whose entire body is `C2 00 00` — `ret`." (`EH:213`)
- **Side B:** "**`ret 0`, not a bare `ret` (`C3`)**" (`EH:621`)
- **Favoured side:** B — B-2/a CLOSED 2026-09-07 (`EH:613-614`).
- Note: The bytes are the same in both; only the label differs.

#### S-12. Identity of the folded empty destructor, and of `001AAF20`, "not attempted" / "stays numeric"

- **Side A:** "the source-level identity of the folded empty destructor" (`EH:986`); "stays numeric" (`EH:753`)
- **Side B:** "**CLOSED 2026-09-07 — answered in the negative.**" (`EH:614`); "**BK-6 answered 2026-09-12 (FABLE)" (`EH:755`)
- **Favoured side:** B — the dated closures at `EH:614` and `EH:755`.

#### S-13. `00584730` "NOT dispositioned" in the teardown row

- **Side A:** "NOT dispositioned" (`ST:23`)
- **Side B:** "`00584730` × 224" (`ST:90`)
- **Favoured side:** B — the body reading (`ST:90-91`, `:210`) and UQ-329 ANSWERED 2026-09-17 (`ST:150`).

#### S-14. Teardown "list head" comments vs node self-link

- **Side A:** "the list is now empty" (`ST:80`)
- **Side B:** "every head is a node of the Phyre reflection registry" (`ST:150`)
- **Favoured side:** B — UQ-329 / UQ-331 answers dated 2026-09-17 (`ST:150`, `:155`).

#### S-15. BQ-26 "unmeasured"

- **Side A:** "the population is unmeasured (**BQ-26**)" (`OBJ:550-551`)
- **Side B:** "the population became **1,608**" (`OBJ:576`)
- **Favoured side:** B — `OBJ:408` (ANSWERED 2026-09-02).

#### S-16. BQ-27 ticked [x] but stated open

- **Side A:** "- [x] Why the sized `operator delete` path resolves to a `ret 0`." (`OBJ:413`)
- **Side B:** "`BQ-27` stays open on the 345." (`OBJ:830`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Narrowed 2026-09-27 to 61 sites (`OBJ:815`), and still open after that.

#### S-17. BQ-23 "stays open" vs answered

- **Side A:** "this row stays open and tier 6 stays the decider." (`OBJ:391`)
- **Side B:** "***ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5): compared at tier 6, and no member is left unmatched.**" (`OBJ:401`)
- **Favoured side:** B — the answer dated 2026-09-27 (`OBJ:401`).

#### S-18. BQ-22: label "unsupported" vs "WRONG"

- **Side A:** "is called out as unsupported by its own name" (`README:40`); "### FOUND: one label whose name is not supported" (`OBJ:507`)
- **Side B:** "the label is not merely unsupported but WRONG for at least two members." (`OBJ:364`)
- **Favoured side:** B — BQ-22 ANSWERED 2026-09-22 (`OBJ:363`).

#### S-19. The 28 "teardown" thunks construct, they do not destroy

- **Side A:** "**NOT CLAIMED:** which interface the 28 implement" (`OBJ:923`); "ConditionalTeardownReturnTrue" (`OBJ:404`)
- **Side B:** "it constructs, it does not destroy." (`OBJ:913-914`); "This answers two of the NOT CLAIMED items above." (`OBJ:942`)
- **Favoured side:** B — "**Corrected 2026-09-29 (SWE2-EC7, FABLE family ruling R4)**" (`OBJ:913-914`).

#### S-20. `001AB570` / `005CD6D0` "NOT dispositioned"

- **Side A:** "the shared implementation(s) 005CD6D0" (`OBJ:47`)
- **Side B:** "## Interior citation — frontier hub `001AB570` (2026-09-18, SWE2-EC7)" (`OBJ:835`)
- **Favoured side:** B — the interior citations dated 2026-09-18 (`OBJ:835`, `:852`).

#### S-21. Four MSVC-tree addresses "named by no document"

- **Side A:** "`0079BA10`, `00799BD0`, `00799C30` and `006B52A0` are named by no document in the database" (`OC:513-514`)
- **Side B:** "`00799BD0`" (`MS:123`); "PNode::addChild" (`OC:528`)
- **Favoured side:** none. No dated correction on the pages settles it.

#### S-22. EASTL key position "not measured"

- **Side A:** "supplies the `node+0x20` key position this page does not measure" (`OC:566-567`)
- **Side B:** "**80 of 80**" (`OC:161`)
- **Favoured side:** none. No dated correction on the pages settles it.

#### S-23. SD-81 / SD-82 open in the falsification note

- **Side A:** "what the sweep cannot rule out: **SD-82**" (`OC:541`); "not one caller was read for purpose" (`OC:353-354`)
- **Side B:** "*(SD-81 answered 2026-09-30 by OPUS `08f4c0821`" (`OC:357`); "*(SD-82 answered 2026-09-30 by OPUS `6836e8067`" (`OC:358`)
- **Favoured side:** B — the answers dated 2026-09-30 (`OC:357-358`); the SD-82 answer's content is not on the page.

#### S-24. Members-file header: 621 vs 521 instructions

- **Side B:** "over 521 instructions" (`OC:371`)
- **Favoured side:** B — the page correction at `OC:458-461`; side A is the header of `members/ordered-container-runtime.tsv` ("621 instructions"), which was not corrected.

#### S-25. MSVC: "fourteen profiled", MT-1 open, inserters not read

- **Side A:** "nine bodies disassembled whole and the remaining fourteen profiled" (`MS:16`); "*which container* each of A, B and C is remains `MT-1`" (`MS:352-353`); "What the keys index and what the values are is not read" (`MS:196`)
- **Side B:** "all twenty-three family bodies are read" (`MS:5`); "**ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5)" (`MS:198`)
- **Favoured side:** B — the readiness line (2026-09-30, `MS:5-10`) and MT-1 ANSWERED 2026-09-26 (`MS:198`).

#### S-26. MSVC users: input system vs `PhyreFrameworkClass`

- **Side A:** "The container users cited here are input-system bodies" (`MS:387`)
- **Side B:** "retracted readings (input-backend adjacency" (`MS:247`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side A is pass 22 (2026-09-29); side B is the MT-2 answer (2026-09-16), which the later pass does not acknowledge.

#### S-27. Return-value adapter: four evidence rows left behind

- **Side A:** "| Each appears exactly three times in `.rdata` |" (`RV:230`); "**The arithmetic does not close**" (`RV:235`); "**that difference is unexplained.**" (`RV:432-433`); "(120 of 120 appearances)" (`RV:180`)
- **Side B:** "**Corrected 2026-09-13: 367 of the 403 appear three times" (`RV:98`); "ANSWERED 2026-09-14" (`RV:331`); "**DF-4 answered 2026-09-12 (FABLE): "351" was the tag census, not the family." (`RV:435`); "Extended 2026-09-13 to all 403 adapters" (`RV:395`)
- **Favoured side:** B — each by its own dated line (`RV:98`, `:331`, `:435`, `:395`).
- Note: The descriptor variant name (`RV:398` vs `:402-404`) and the "§4's hook advice is wrong" heading (`RV:291` vs `:138-146`) are stale in the same way.

#### S-28. Arena backing "not established"

- **Side A:** "whose backing is not established" (`MEM:39`); "Where the arena's backing is obtained" (`MEM:115-116`)
- **Side B:** "**Where the backing comes from (2026-09-12, ASTRA's supplement re-read by FABLE).**" (`MEM:120`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Here the stale side is the *later* text (the 2026-09-28 correction around `MEM:38-39`). No dated line resolves it.

#### S-29. "Failure is not handled"

- **Side A:** "### Failure is not handled" (`MEM:497`); "which the caller will not check" (`MEM:783-784`)
- **Side B:** "**The arena retries before it fails.**" (`MEM:67`); "*(corrected 2026-09-30, SWE2-DATA" (`MEM:504`)
- **Favoured side:** B — the corrections dated 2026-09-28 and 2026-09-30.

#### S-30. "The allocator is a leaf"

- **Side A:** "it is a leaf." (`MEM:749`); "**The gameplay chain is a different chain and does not join this one:**" (`MEM:751`)
- **Side B:** "So the pool comes from the `0036A100` arena" (`MEM:819`)
- **Favoured side:** B — the answer dated 2026-09-14 (`MEM:819`).

#### S-31. Arena "not read here" items answered elsewhere on the page

- **Side A:** "Whether `0036BC60` can return a block before a category is pushed is **not read here**" (`MEM:1423-1424`); "`0036CB00` is untouched by this and remains unread." (`MEM:1433`); "purposes not read here" (`MEM:179-180`)
- **Side B:** "an allocation through the wrappers requires at least one pushed selection" (`MEM:326-327`); "`0036CB00` (1,353 B) is a free-block realloc path" (`MEM:1533`); "bucket" (`MEM:225-226`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: None of the B lines says it answers the A line.

#### S-32. Header not added to `_types`; second list root "NOT established"

- **Side A:** "**The header is NOT being added to `_types/` yet, and that is deliberate.**" (`MEM:1057`); "**What is NOT established is where that second list is rooted**" (`MEM:1028-1029`)
- **Side B:** "ImageAddressArenaBlockHeader" (`MEM:1732`); "*(Answered by reconciliation 2026-09-30, SWE2-DATA" (`MEM:1091`)
- **Favoured side:** B — the 2026-09-20 `_types` section (`MEM:1732-1736`) and the 2026-09-30 reconciliation (`MEM:1091`).

#### S-33. SD-164 … SD-169 open on the page, answered in the register

- **Side A:** "is `SD-164`" (`MEM:67`); "`SD-166`" (`MEM:160`); "`SD-169`" (`MEM:1407`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Side B is outside the audited set: `_index/OPEN-QUESTIONS.md:3643-3648` marks SD-164…SD-169 ANSWERED (2026-09-30, SD-165 2026-10-01). The pages were not updated. SD-165 (`MEM:70`, `:504`), SD-167 (`MEM:193`) and SD-168 (`MEM:195`) are in the same state.

#### S-34. BU-1: "kind (c)", "PARTIAL until signed", "not re-thunked"

- **Side A:** "this is a NO ADMISSIBLE SOURCE closure, kind (c)" (`TH:249`)
- **Side B:** "**kind (d)**" (`TH:319`); "**BU-1 — CLOSED 2026-09-18" (`TH:229`)
- **Favoured side:** B — the signature dated 2026-09-18 (`TH:318-319`), which also refuses the "not re-thunked" mechanism sentence (`TH:344-355`).

#### S-35. "Superseded readings: none"; BU-5 "Not measured here"; "approximations below"

- **Side A:** "none — this is the document's first version." (`TH:380`); "Not measured here." (`TH:290`); "the approximations below do not sum to 689" (`TH:69-70`)
- **Side B:** "**OVERTURNED in section 10" (`TH:79`); "**yes — 296 of the 689 are address-taken.**" (`TH:291-292`)
- **Favoured side:** B — for the first two: the overturn (2026-09-03) and BU-5 answered 2026-09-14.
- Note: No approximations remain below `TH:69`; §10 still quotes them (`TH:447`).

#### S-36. "No banned evidence" vs `.pdata` used as a separating property

- **Side A:** "**No banned evidence.** No `.pdata`/`.xdata`/unwind/EH." (`TH:463`)
- **Side B:** "**The one feature all 16 share: the jump target has no `.pdata` entry.**" (`TH:240`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `RS:402-405` records the pass-6 principle: unwind data may be used for finding, not for what executes.

#### S-37. CV-3 question unstruck; second-dump trigger "not read"; evidence row "not a body read"

- **Side A:** "is unestablished" (`RS:249`); "Its trigger, and whether it can run before the filter, are not read." (`RS:284-285`); "**an address-range argument plus a string join, not a body read**" (`RS:342`)
- **Side B:** "The framework installs the writer as the unhandled-exception filter on every boot.**" (`RS:250-251`); "The filter `008A5AD0` calls `005CCBF0`, the minidump path above" (`RS:441`); "(137 B, read whole)" (`RS:237-238`)
- **Favoured side:** B — CV-3 answered 2026-09-14 (`RS:250`), BK-5 2026-09-14 / pass-6 2026-09-16 (`RS:387`, `:393`), CV-2 2026-09-12 (`RS:237`).
- Note: Whether the second dump runs before the unhandled-exception filter is still not stated.

#### S-38. S-2: link with or without `/guard:cf`, answered or open

- **Side A:** "a link WITHOUT `/guard:cf`, with `/DYNAMICBASE:NO`." (`HARD:346-347`)
- **Side B:** "so `S-2` stays open" (`HARD:440`); "the compile-versus-link axis is open again" (`HARD:415-416`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Both sides are dated 2026-09-26. `HARD:598-600` (2026-09-07) gives a third reading: `/guard:cf` reached the compiler but not the linker. The section heading `HARD:388` ("the link DID have `/guard:cf`") is kept and withdrawn "as a proof" at `HARD:390`.

#### S-39. UQ-323 "closed — WITHDRAWN" vs "The row stays OPEN"

- **Side A:** "*(closed — the register row is WITHDRAWN.)*" (`MATH:590`)
- **Side B:** "**The row stays OPEN.**" (`MATH:592`)
- **Favoured side:** none. No dated correction on the pages settles it.

#### S-40. `00202F00` "which I did not read"; UQ-322 callers "not traced"

- **Side A:** "which I did not read" (`MATH:593`); "their callers were not traced" (`MATH:583`)
- **Side B:** "## Interior citation — frontier hub `00202F00` (2026-09-17, SWE2-EC7)" (`MATH:827`); "*ANSWERED 2026-09-27" (`MATH:586`)
- **Favoured side:** B — the interior citation dated 2026-09-17 and UQ-322 ANSWERED 2026-09-27.

#### Status banners and front matter

#### B-1. `SI`: AUDITED vs README DOCUMENTED vs §12 REOPENED; pass counts

- **Side A:** "status: AUDITED" (`SI:4`); "passes: 5" (`SI:20`)
- **Side B:** "**DOCUMENTED, tier 1.**" (`README:19`); "## 12. REOPENED and corrected 2026-09-02 (fourth pass)" (`SI:807`); "the four falsification passes in sections 9–11" (`SI:866`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: Sections 9–11 hold three passes, and `## 9.` appears twice (`SI:567`, `:573`). `last_reviewed: 2026-09-02` (`SI:18`) predates body text to 2026-09-29.

#### B-2. `LZ`, `EH`, `OBJ`: AUDITED vs README / in-body DOCUMENTED

- **Side A:** "status: AUDITED" (`LZ:4`); "status: AUDITED" (`EH:4`); "status: AUDITED" (`OBJ:4`)
- **Side B:** "**DOCUMENTED, tier 1, one falsification pass.**" (`README:25`); "**DOCUMENTED, tier 1, one falsification pass.**" (`README:43`); "`DOCUMENTED`, two falsification passes." (`OBJ:617`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: All three carry `last_reviewed: 2026-09-02` with body text dated to 2026-09-29. `EH:1019` is a section dated "2026-05-15", before the page existed.

#### B-3. `ST`: status line repeats a clause; last_reviewed predates it

- **Side A:** "the owners of the 224 list heads (UQ-329) and the +0x20 flag (UQ-330) answered 2026-09-17" (`ST:4`)
- **Side B:** "last_reviewed: 2026-09-13" (`ST:11`)
- **Favoured side:** none. No dated correction on the pages settles it.

#### B-4. `OC` / `MS`: AUDITED (promoted 2026-10-01) vs "DOCUMENTED page"; tier 1 vs tier-2 banners

- **Side A:** "promoted: 2026-10-01 DOCUMENTED -> AUDITED" (`OC:20`); "evidence_tier: 1" (`OC:6`)
- **Side B:** "measured A on this DOCUMENTED page" (`OC:21`); "*Tier 2:" (`OC:593`); "*Tier 2:" (`MS:393`)
- **Favoured side:** A — for status: the promotion (2026-10-01) postdates the withdrawal note (2026-09-30).
- Note: `MS:9` keeps the superseded rating "SEMANTICALLY IDENTIFIED", marked "superseded by SD-80" (`MS:10`).

#### B-5. `GEN`: last_reviewed vs row edits; `RV`: no promotion record; section order

- **Side A:** "last_reviewed: 2026-09-29" (`GEN:11`); "last_reviewed: 2026-09-08" (`RV:19`)
- **Side B:** "*(Corrected 2026-10-02, FABLE" (`RV:212`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `GEN` rows carry 2026-09-30 / 2026-10-01 edits (e.g. `GEN:24`, `:31`). `RV:4` is AUDITED with no `promoted:` line. `RV`'s sections run §6, §9, §7, §8 (`RV:223`, `:237`, `:377`, `:388`).

#### B-6. `MEM`: REOPENED with reopened_count 0; one audit pass vs a later uncertified production

- **Side A:** "status: REOPENED" (`MEM:4`); "reopened_count: 0" (`MEM:24`)
- **Side B:** "Historical audit receipts above do not certify this new production." (`MEM:1901`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `last_reviewed: 2026-09-12` (`MEM:18`) vs body text to 2026-10-02 (`MEM:1509`). The heading "### Two corrections from the same pass" (`MEM:1217`) is followed by three.

#### B-7. `TH`: audit pass dates; duplicate heading; section order

- **Side A:** "last_pass: 2026-09-03" (`TH:22`)
- **Side B:** "## 12. Audit pass 3 - 2026-09-13 (OPUS)" (`TH:550`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: The heading "Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)" appears twice (`TH:627`, `:664`). §10 (`TH:382`) precedes §9 (`TH:466`).

#### B-8. `RS`: last_reviewed / pass vs body; "table above" points below

- **Side A:** "last_reviewed: 2026-09-07" (`RS:19`)
- **Side B:** "2026-09-28" (`RS:259`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `RS:421-422` refers to "the table above", but the table is at `RS:425-435`.

#### B-9. `HARD`: README DOCUMENTED; audit hash is another page's; reopened_count 1 unnamed

- **Side A:** "status: AUDITED" (`HARD:4`); "last_pass_state: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34" (`HARD:23`)
- **Side B:** "**DOCUMENTED, tier 1.**" (`README:14`); "snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2" (`HARD:9`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `b57264ba…` is `MATH`'s `snapshot_sha256` (`MATH:16`). `reopened_count: 1` (`HARD:25`) does not say what was reopened. Sections are numbered §8, §9a, §10, then "## 9." twice (`HARD:507`, `:552`, `:576`, `:731`, `:737`).

#### B-10. `MATH`: AUDITED vs "unchanged at DOCUMENTED"; README omits it

- **Side A:** "status: AUDITED" (`MATH:4`)
- **Side B:** "unchanged at **DOCUMENTED**" (`MATH:778`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `last_reviewed: 2026-09-12` (`MATH:18`) vs body text to 2026-09-29 (`MATH:862`). `MATH:611-612` cites a "§6" statement about `SQEX::Sd::*` that §6 does not contain.

#### B-11. `README` indexes 5 of 14 pages

- **Side A:** "## Systems in this category" (`README:11`)
- **Favoured side:** none. No dated correction on the pages settles it.
- Note: `ST`, `OC`, `MS`, `GEN`, `RV`, `MEM`, `TH`, `RS` and `MATH` exist in the folder but are not listed (`README:13-47`).
