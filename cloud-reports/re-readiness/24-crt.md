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

