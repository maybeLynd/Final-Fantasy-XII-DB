# Reconstruction readiness — `FFXII TZA/01-Script-VM-Native-Bridge/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-01-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`86b70c69`); no executable, Ghidra or live game was used. Several pages in this folder are being edited by other lanes; every quotation is the snapshot's text. |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. |

**Counts:** 23 pages read in full (22 system pages + `README.md`), 20 member `.tsv` files checked for layout and counts only · **38 entry-point rows** mapped (5 frame/driver/interpreter, 10 request scheduling, 4 lifecycle and dispatch, 6 value-stack and result, 5 variable, 8 verb groups) · **31** self-stated open gaps + **18** structural gaps · **128 contradictions**: **60 value-changing** (45 itemised + 15 count rows; **17** with a favoured side settled by a dated correction, two of them only in part: C-V9, C-V20; **43** with no favoured side; all "page-text only - needs local check") and **68 stale / banner** · **Rating: NOT YET** overall (lifecycle, value stack, variables and request scheduling MOSTLY; interpreter opcode set and verb bodies NOT YET).

## How to read the citations

Every citation is `ALIAS:line` (or `ALIAS:a-b`). Each alias is exactly one page; the path is relative to
`FFXII TZA/01-Script-VM-Native-Bridge/`. "Not stated" means none of the 23 pages says it. Where another
category's page is the only place a point is made, it is given as a path from `FFXII TZA/` and was **not** audited
for this report.

| alias | page | lines |
|---|---|---:|
| `README` | `README.md` | 50 |
| `DT` | `scriptvm-native-dispatch-table.md` | 1,178 |
| `WAIT` | `verbs-that-only-wait-and-verbs-that-do-nothing.md` | 385 |
| `NAMES` | `how-a-script-names-a-thing-in-the-world.md` | 611 |
| `C-INT` | `CONTRACT-interpreter-core.md` | 314 |
| `C-NCL` | `CONTRACT-native-command-lifecycle.md` | 282 |
| `C-BR` | `CONTRACT-script-to-native-bridge.md` | 472 |
| `INT` | `Interpreter-Core/worldactor-scriptvm-interpreter.md` | 1,148 |
| `RES` | `Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md` | 192 |
| `REQ` | `Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md` | 193 |
| `BIND` | `Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md` | 535 |
| `VARS` | `Interpreter-Core/script-variables-and-their-storage-classes.md` | 601 |
| `ATEL` | `ATEL-Control-Modules/the-ctrl-module-debug-companions.md` | 934 |
| `NCL` | `Native-Command-Lifecycle/native-command-lifecycle.md` | 795 |
| `VD` | `Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md` | 1,425 |
| `C-VD` | `Verb-Dispatch/CONTRACT-verb-dispatch-abi.md` | 687 |
| `POP` | `Verb-Dispatch/the-shape-of-the-verb-population.md` | 499 |
| `REACH` | `Verb-Dispatch/what-each-script-verb-touches.md` | 383 |
| `CC` | `Spawn-Verbs/the-script-to-native-calling-convention.md` | 812 |
| `BP` | `Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md` | 164 |
| `READIN` | `Party-Presentation-Verbs/the-party-read-in-state-machine.md` | 407 |
| `STDM` | `Party-Presentation-Verbs/the-party-standard-motion-verbs.md` | 542 |
| `LOOKS` | `Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md` | 638 |

## Pages read

All 23 pages were read in full, every line. The status columns are as the page states them.

| alias | front-matter status / readiness | `last_reviewed` · `audit.last_pass` | body banner, if any |
|---|---|---|---|
| `README` | category index; "Functions \| 1,900" (`README:8`) | — | calls `INT`, `VD`, `NCL` "**DOCUMENTED, tier 1.**" and `DT` "**DOCUMENTED, tier 2.**" (`README:15`, `:19`, `:28`, `:32`) |
| `DT` | `status: AUDITED` (`DT:4`) | 2026-09-07 · 2026-09-07 (`DT:18`, `:21`) | "**DOCUMENTED.**" (`DT:40`); "**Why this is PARTIAL rather than DOCUMENTED.**" (`DT:420`) |
| `WAIT` | `status: AUDITED` (`WAIT:4`) | 2026-09-13 · 2026-09-13 (`WAIT:18`, `:21`) | — |
| `NAMES` | `status: AUDITED — the last open box … (UQ-58), answered 2026-09-17 …` (`NAMES:4`); `readiness: SEMANTICALLY IDENTIFIED` (`:8`) | 2026-09-13 · 2026-09-13 (`NAMES:17`, `:21`) | — |
| `C-INT` | `readiness: CONTRACT READY`, `confidence: PROVEN` (`C-INT:6-7`) | 2026-09-30 · 2026-09-30 (`C-INT:19`, `:22`) | "SECTION-11 locally validated; formal independent acceptance pending" (`C-INT:28`) |
| `C-NCL` | `readiness: CONTRACT READY`, `confidence: PROVEN` (`C-NCL:6-7`) | 2026-09-29 · 2026-09-29 (`C-NCL:19`, `:22`) | "formal independent acceptance pending" (`C-NCL:28`) |
| `C-BR` | `readiness: CONTRACT READY`, `confidence: PROVEN` (`C-BR:6-7`) | 2026-09-11 · 2026-09-12 (`C-BR:17`, `:20`) | "**Readiness is `CONTRACT READY`, not `RECONSTRUCTION READY`**" (`C-BR:38`) |
| `INT` | `status: "DOCUMENTED — the SECTION-11 reopening is resolved …"` (`INT:4`) | 2026-09-02 · 2026-10-01 (`INT:18`, `:21`) | "This page is REOPENED, preserving its older audit receipts." (`INT:35`) |
| `RES` | `status: PARTIAL` (`RES:4`) | 2026-09-30 · 2026-09-30 (`RES:10`, `:14`) | — |
| `REQ` | `status: PARTIAL` (`REQ:4`) | 2026-09-29 · 2026-09-29 (`REQ:10`, `:13`) | — |
| `BIND` | `status: "REOPENED — SECTION-12 trigger resolved …"` (`BIND:4`) | 2026-09-11 · 2026-09-13 (`BIND:13`, `:16`) | "**The review is done:**" (`BIND:527`) |
| `VARS` | `status: AUDITED` (`VARS:4`) | 2026-09-11 · 2026-09-13 (`VARS:14`, `:17`) | — |
| `ATEL` | `status: AUDITED` (`ATEL:4`) | 2026-09-12 · 2026-09-13 (`ATEL:20`, `:27`) | "## 6. Falsification pass / Not yet run." (`ATEL:795-797`) |
| `NCL` | `status: "DOCUMENTED — every register row the page names is answered …"` (`NCL:4`) | 2026-09-07 · 2026-09-07 (`NCL:18`, `:21`) | "**Historical DOCUMENTED assessment; current corrections require review.**" (`NCL:43`) |
| `VD` | `status: AUDITED` (`VD:4`) | 2026-09-02 · 2026-09-08 (`VD:18`, `:21`) | "`DOCUMENTED`, three falsification passes survived" (`VD:1249`) |
| `C-VD` | `readiness: CONTRACT READY`, `confidence: PROVEN` (`C-VD:6-7`) | 2026-09-12 · 2026-09-12 (`C-VD:17`, `:20`) | "Mutation campaign … Status `FAIL`" (`C-VD:361-362`) |
| `POP` | `status: AUDITED`, `readiness: CLASSIFIED` (`POP:4`, `:8`) | 2026-09-08 · 2026-09-13 (`POP:17`, `:21`) | — |
| `REACH` | `status: DOCUMENTED — every register row is closed …` (`REACH:4`) | 2026-09-30 · 2026-09-13 (`REACH:21`, `:24`) | "`status: PARTIAL` is the honest state." (`REACH:57-58`) |
| `CC` | `status: AUDITED`, `readiness: BEHAVIORALLY UNDERSTOOD` (`CC:4`, `:8`) | 2026-09-08 · 2026-09-13 (`CC:15`, `:18`) | — |
| `BP` | `status: DOCUMENTED` (`BP:4`) | 2026-09-29 · 2026-09-29 (`BP:14`, `:17`) | audit note "pending first review" (`BP:22-23`) |
| `READIN` | `status: AUDITED — the part slots are …` (`READIN:4`) | 2026-09-14 · 2026-09-14 (`READIN:12`, `:15`) | — |
| `STDM` | `status: DOCUMENTED — every register row is closed …`; `readiness: BEHAVIORALLY UNDERSTOOD` (`STDM:4`, `:8`) | 2026-09-30 · 2026-09-13 (`STDM:17`, `:21`) | — |
| `LOOKS` | `status: DOCUMENTED — every register row is closed …`; `readiness: BEHAVIORALLY UNDERSTOOD` (`LOOKS:4`, `:8`) | 2026-09-30 · 2026-09-13 (`LOOKS:17`, `:21`) | — |

**Member `.tsv` files** (used only to confirm layouts and counts; no item below rests on a TSV alone):

| file | rows | checked against | result |
|---|---:|---|---|
| `Interpreter-Core/register-opcodes-by-script.tsv` | 1,114 | `INT:894-900` | totals agree exactly (108,328 functions, 4,430 using registers, 57,568 register opcodes, 788 scripts, all 16 per-opcode sums); the `read_before_write` column is filled for **96** scripts against the page's "84 scripts" (`INT:908`) |
| `Interpreter-Core/script-variables-by-script.tsv` | 1,114 | `VARS:135-140`, `:344` | agrees exactly (43,466 descriptors; class 3 = 0) |
| `Interpreter-Core/script-global-variables-by-script.tsv` | 587 | `VARS:124`, `:135`, `:155` | agrees (587 offsets, 9,448 declarations, max 575 scripts, 110 single-script) |
| `Interpreter-Core/script-global-variables-by-offset.tsv` | 620 | `VARS:148-149` ("lists every payload offset a shipped script declares") | 587 rows with declarations + 33 zero-declaration rows the page does not mention; last row `0xCF4 … u16` |
| `Interpreter-Core/script-global-arrays-by-offset.tsv` | 34 | `VARS:140` (881 array elements) | agrees |
| `native-command-family-tables-accesses.tsv` | 1 | `DT:532`, `:627-628` | one row: `003DC2D0` `rep stosq` into `0x02B57EF0`; cited by no page |
| `vm-value-stack-accesses.tsv` | 40 | — | all rows route from `STATIC 0x02099AC0`; cited by no page |
| `Verb-Dispatch/scriptvm-verb-table.tsv` | 1,960 | `VD:34`, `:138-142`, `:583-590` | rows and family counts agree; **arity filled on 1,960/1,960** (`VD:36` says 1,870); `cat_args == arity` on 1,269 of 1,270 (`VD:37-38` says 1,209 of 1,210); `guard = fsmenu` on 42 rows (`VD:592` says 33) |
| `Verb-Dispatch/scriptvm-dispatch.tsv` | 1,493 | `DT:198` ("1,224 rows"), `C-BR:205` | header says 1,493 rows, extended 2026-09-19/26; begin/poll columns re-framed 2026-09-19 |
| `Verb-Dispatch/scriptvm-verb-reach.tsv` | 1,960 | `REACH:42-45` | agrees (616 labelled, 1,344 blank) |
| `Verb-Dispatch/scriptvm-verb-shapes.tsv` | 1,224 | `POP:63-69`, `:110-117` | family and target counts agree; four rows already carry the corrected family (`POP:466-468` says "unchanged") |
| `Verb-Dispatch/members/scriptvm-verb-adapter-callbacks.tsv` | 1,030 | `POP:26` (1030), `POP:159`, `:170-172` (1,053 = 964/71/18) | agrees with front matter; disagrees with body (944/68/18) |
| `Verb-Dispatch/members/scriptvm-verb-adapter-leftovers.tsv` | 503 | `POP:175-179` (629 = 590/38/1) | disagrees (475/28/0) |
| `Verb-Dispatch/members/scriptvm-verb-marshal-argmap.tsv` | 836 | `POP:188-203` | agrees exactly |
| `Verb-Dispatch/members/async-verbs-by-accessor.tsv` | 304 | `DT:206`, `:218-221` | agrees (304; 146 pair rows) |
| `Spawn-Verbs/members/spawn-verb-call-census.tsv` | 7 | `CC:280-285` | agrees (649,710 sites; getters CALL, setters CALLPOPA) |
| `Spawn-Verbs/members/sysreq-channel-census.tsv` | 675 | `CC:712-714` | agrees (675 sites; 621 immediates; 54 variable) |
| `Party-Presentation-Verbs/members/party-read-states.tsv` | 24 | `READIN:94`, `:99-120`, `:250` | 24 states agree; three transition sites differ (`0037B946`/`0037BA3B`/`0037BB43` on the page, `0037B94C`/`0037BA47`/`0037BB4F` in the TSV) |
| `Party-Presentation-Verbs/party-read-machine-record-accesses.tsv` | 27 | `READIN:219-225` | 7 accesses to the mask at `+0x10` agree with UQ-53; cited by no page |
| `Party-Presentation-Verbs/party-read-machine-record-second-instance-accesses.tsv` | 47 | `READIN:73-75`, `:254` | installer start slots and steps agree; `0037B4D0` reads the verb-mode byte `+0x0C` six times, which no page states; cited by no page |

---

## 1. Interface

The category is one pipeline with five parts. A per-frame field pass hands each actor to a **driver**, which picks
the actor's current **wait slot** and either resumes the **interpreter** or tests a wait condition. The interpreter
is a 100-opcode stack machine. Its call opcodes reach the **native command lifecycle**, which splits a 16-bit call
id into family and command, looks up begin / poll / result callbacks in five **dispatch tables**, and runs a
three-phase machine over the wait slot. The **verbs** on the far side pop their arguments off a shared value stack
and write a typed result back into the wait slot. Requests between actors (`REQ*` opcodes) go through a per-actor
**entry list** that the driver walks by channel.

### 1.1 Entry points (functions, with their callers)

#### Frame entry, driver and interpreter

| entry | callers | what it does | cite |
|---|---|---|---|
| `World_UpdateSimulationTick` `00314020` → `ActorManager_RunFieldRuntimePass` `0025D9E0` | `MainLoop_UpdateAndRenderFrame` `0022B8C0` | per-manager pass; `rbx = 02098E10 + index × 0x288` | `C-VD:609-616`; `INT:978-979`, `:1084` |
| `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (1,228 B) | `0025D9E0` | the driver: selects wait slot `*(actor+0xA8) + sx(actor+0x11)*0x28`, switches on wait kind (`cmp eax, 7`, 8-entry table), interpreter arm `0025E0BE`, blocked exit `0025E127` | `BIND:369-378`; `REQ:102`; `CC:586`; `NCL:742` |
| `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (14,646 B, 3,229 instructions) | `0025DF00` only — "exactly **one** direct call site image-wide" | runs bytecode; `(rcx ActorManagerSlot, rdx actor record, r8 wait slot)` | `INT:43`, `:128`, `:1138-1141`; `C-INT:58`; `BIND:100-101` |
| `WorldActorScriptVM_ServiceRequestWaitState` `0025B400` (108 B) | interpreter (4 calls) | "the yield point"; reads `+0x14 cmp 4` | `INT:107`, `:117`; `VARS:537`; `CC:622` |
| typed 3-way comparator `0025D740` (413 B) | opcodes `0x0A`–`0x0F` | comparison engine | `INT:94`, `:534-547`; `VARS:538` |

#### Requests and scheduling (the `REQ*` opcodes and the entry list)

| entry | callers | what it does | cite |
|---|---|---|---|
| `ScriptVM_SubmitActorRuntimeRequest` `00268850` | nine `REQ*` opcode tails | `(manager, issuer, valueStack, issuerRequest, pc, kind, mode)`; pops target/function/channel, builds a descriptor, gates on the issuer, submits | `BIND:132-188`, `:311`; `REQ:36` |
| `ActorResource_AllocateAndSubmitEntry` `003DBCF0` | `00268850` and 6 other functions (7 sites) | returns 2 when the free list is exhausted (`003DBD32`), 3 for an id out of range | `BIND:159`, `:186`; `REQ:53`; `CC:673-674` |
| `ActorResource_InsertEntryFromDescriptor` `003DB7A0` | `003DBCF0` only | channel clamp (upper only), dedupe walk, kind-dependent admission | `BIND:125-128`, `:151-155`; `CC:662-663` |
| `003DB790` (11 B) / `003DBAE0` | submit modes 1 / 2 | state-1 forward; state-2 insert with promotion | `BIND:182-185`, `:443` |
| `ActorResource_SelectPendingEntryForExecution` `003DB6E0` (168 B) | "the interpreter and seven other callers" | channel walk, highest channel first; sole producer of `actor+0x11` | `BIND:105-123`, `:261`; `CC:116` |
| `ActorResource_StartEntryScriptExecution` `003DBDC0` | channel walk | sets PC = image + function offset, wait kind 1 | `BIND:88-95`, `:239` |
| `ActorResource_RemoveActiveEntry` `003DB2A0` / `ActorResource_RecycleEntryRange` `003DB420` (304 B) | `RET`/`RETT` / `RETN`/`RETTN`/`REQCANCEL` | removal; detached notification at `+0x10 == 4` | `BIND:202-205`; `VARS:574` |
| `ActorResource_FindScriptRequestEntry` `003DC050`; notification producer `003DC0D0` | wait kinds 3/4; removal | notification match, bound `byte[actor+0x89] + 2` | `REQ:72`, `:85`, `:184` |
| `ActorStorage_InitializeRecord` `00266530` | binder | plants the record fields, party roster registration | `BIND:42-56`, `:237` |
| `ScriptExecutionState_ResetCore` `0025D460` (20 B) | start, record init | zeroes wait slot `+0x00..+0x16` only | `BIND:93`, `:430`; `REQ:63-64` |

#### Native command lifecycle and dispatch

| entry | callers | what it does | cite |
|---|---|---|---|
| `VMNativeCommand_ExecuteLifecycle` `002621D0` (461 B) | interpreter, 3 sites `002619B6` / `00261A19` / `00261AD4` | splits the id (`sar r12d,0xc` at `00262205`, `and r15d,0xfff` at `0026220C`), runs the phase machine, pushes one result | `C-VD:474-482`; `VD:280`, `:543-548`; `DT:651-657`; `C-NCL:53` |
| `VMNativeCommandDispatch_InitializeFamilyTables` `003DC2D0` (89 B) | area initialiser `00266D10` (World); "built at startup" (`C-VD:180`) | fills the 16-entry family array; see C-V8 for a disagreement on what it installs | `C-NCL:54`, `:282`; `VD:278`, `:1392`; `DT:532`, `:627-629` |
| `GetBeginCallback` `003DC270` · `GetPollCallback` `003DC240` · `GetResultCallback` `003DC2A0` | `002621D0` only (`002622BA`, `00262220`, `0026225D`) | `(family, command)` → callback or NULL | `C-NCL:55-57`; `C-VD:479-480`; `VD:279` |
| `ActorManager_GetRecordByOrdinal` `00358940` (30 B) | `002621D0` at `0026223B` | rebinds the command's owner actor | `C-VD:413-416`; `C-NCL:280` |

#### Value stack and result helpers

| entry | callers | what it does | cite |
|---|---|---|---|
| `VMValueStack_PopInt32CoerceFloat32` `00267E10` (78 B) | handlers (238 single-call verbs end here) | pop as s32; float → `cvttss2si`; silent on empty, reports a bad tag | `C-BR:66`, `:391-396`; `VD:397-408`; `POP:110` |
| `VMValueStack_PopNumericDiscard` `00267DB0` (84 B; it is a float pop) | handlers, 436 direct call sites | pop as f32; int → `cvtdq2ps`; reports empty, silent on a bad tag | `C-BR:67`, `:73-92`; `VD:410-421` |
| `VMValueStack_PushInt32` `00267F90` (39 B) · `VMValueStack_PushFloat32Bits` `00267F60` (41 B) | interpreter, handlers | push; guard `cmp eax, 0x3F` drops the 64th push silently | `C-BR:68-69`, `:127-128`; `CC:498-501` |
| `VMResult_WriteInt32` `0026B4E0` (28 B) · `VMResult_WriteFloat32` `0026B4C0` (28 B) | returning verbs (tail jump) | write tag 2 / 3 at wait slot `+0x15` and the value at `+0x0C` | `CC:94-109`, `:238`; `C-BR:70-71`; `VD:286-287` |
| `002651A0` (26 B) | `00342A80` only | stamps tag 2, then returns `slot+0x0C` | `CC:439`, `:638`; `C-BR:361` |
| `FUN_008620C0` (14 B) | 52 sites in the interpreter; the pops | fatal-error reporter; retail tail-jumps to the `ret 0` stub `0016D6A0` | `INT:93`, `:493-504`; `CC:792-796` |

#### Variable opcodes and the resolver

| entry | callers | what it does | cite |
|---|---|---|---|
| `ScriptVariable_Resolve` `00262440` (591 B) | `PUSHV` `00267FC0` (0x48), `POPV` `00267E60` (0x49), `PUSHDBG` `0026178F` (0x4A), `PUSHP` `00268100` (0x4B) | descriptor → (kind, address); 0x30-byte out-record | `VARS:45-58`, `:201`, `:242-243`, `:454-463` |
| `DVAR` `00261742` (0x46) | interpreter | calls the folded no-op `0016D6A0` | `VARS:57`, `:473-476` |
| reference resolver `002650B0` (206 B) | handlers (e.g. `003538F0`, `00510620`) | packed reference → address | `VD:291`, `:471-493`; `CC:250-256`; `NAMES:384-418` |
| store `0026D530` | `POPV` | saturating store by width | `VARS:91-98`; `VD:1421` |
| persistence: `WorldPersistence_ResetBanksForFieldTransition` `0026DB30`, `…ResetBanksAndMarkInitializationState` `00268320`, export `0025D8E0`, import `00269A20` | field transition, load | clear / save / restore the scratch banks | `VARS:160-170`, `:207-210` |

#### Verbs documented in this category

| group | entries | cite |
|---|---|---|
| Spawn wrappers (family 3) | `005101F0` (304A), `00510230` (304B), `00510260` (305F), `00510370` (3015), `00510160` (3001), `005103F0` (305C), `00510620` (3016); arities 1/0/0/1/1/2/1 | `CC:159-165`, `:318-326` |
| Battle-party verbs (0x353–0x35C) | eight verbs; begins `0034C030` (shared add/remove), `0034D4E0`, `00350160`, `00350CD0`, `00351A40`, `00352190`, `00352AF0`; polls `0034C370`, `0034CDF0`, `003506A0` (shared by six) | `BP:38-47`, `:62-107` |
| Party read-in machine | `0037B4D0` (24 states, thunk `0037B4C0`); installers `0037C980` / `0037CA00` / `0037CA80` from `partyallread` 0x3EB / `partyallread2` 0x46F / `summonread` 0x203; world-tick entry `0037C1A0`; task callback `0037C730`; end test `0037CB50` | `READIN:71-90`, `:133-140` |
| Party standard motion (0x53E–0x541) | `0034F060`, `0034F890`, `00350050`, `003507B0`; status read `003580C0` (240 B) | `STDM:43-48`, `:143-153` |
| Party appearance (0x40D–0x413) | seven handlers; collector `0031B5A0`; setters `0026A430`, `002EC680`, `002ECD80`, `002E8730` | `LOOKS:54-74`, `:325-341` |
| Entity names | resolver `002E97C0` (68 B, 11 users, 20 sites); `setuptreasure` 0x2BE result `00355210`; placement decoder `002FAF60`; bind `002E28E0` (2,026 B) | `NAMES:44-48`, `:86`, `:136-152` |
| Waits and stubs | 26 poll-only waits, 3 empty records, 9 stubbed verbs; stub bodies `0016D6A0` (`ret 0`) and `005C5230` (`xor eax,eax; ret`) | `WAIT:30-32`, `:59-63`, `:109-126` |
| Request verbs | `sysreq` 0x00AA `0034E5C0`, `sysreqf` 0x0228 `0034EC80`, `sysreqall` 0x00AB `0034F380` | `CC:704-708` |

The category does **not** describe the other ~1,880 handler bodies: "**1,886 distinct functions** serve as callbacks"
(`VD:552`); see G-1.

### 1.2 Inputs and outputs (data read and written, with record layouts)

#### Bytecode and the opcode table

- An instruction is one opcode byte; opcodes `0x48`–`0x63` carry a little-endian `u16` operand. The operand is
  pre-decoded for every opcode `>= 0x47` (`0025E5A9`), so `0x47` reads two bytes past its 1-byte length
  (`INT:180-196`; `C-VD:126-138`; `RES:120-122`).
- Dispatch: `byte [r14]` at `0025E59D`, bound `cmp eax, 0x63` at `0025E5D1` (`ja` → `0025E60A`), table `0x00261DF8` =
  100 × 32-bit RVA against image base `0x00120000`, `jmp rcx` at `0025E5E8` (`INT:72-88`, `:124-135`).
- Shared targets: `0025E60A` ← opcodes `01 02 19 1A 31 47`; `0026121A` ← `2A 2B 2C`; `002618A8` ← `51 60`; 92 distinct
  targets (`INT:147`, `:163-164`, `:1034`).
- Instruction lengths come from a second table, `0x01EFEA60`, stride 24, 100 records: `+0` `s16` length of opcode N
  (0 for `0x00`–`0x02`, 1 for `0x03`–`0x47`, 3 for `0x48`–`0x63`), `+8` the mnemonic of opcode **N+1** (rotated),
  `+2`, `+16`, `+20` unread (`INT:363-383`, `:443-444`).
- The four call opcodes: `0x58 CALL` (current actor), `0x59 CALLACT` (pops the actor, first call only), `0x5D
  CALLPOPA`, `0x5E CALLACTPOPA` (result popped into the A register `cmdState+0x10`); each is 3 bytes with a `u16`
  call id (`VD:79-103`; `C-VD:50-63`; `WAIT:151-152`).
- Per-opcode semantics are on the page only for: `0x00`–`0x03`, `0x0A`–`0x0F`, `0x15`/`0x16`, `0x1B`/`0x1C`, the `REQ*`
  family `0x21`–`0x29`, `RET` group `0x2D`…, `0x32`, register opcodes `0x36`–`0x45`, `0x48`–`0x4F`, `0x51`/`0x60`,
  `0x57`–`0x5F`, `0x61`, `0x63` (`INT:198-213`, `:538-557`, `:644-657`, `:851-858`, `:996-999`; `BIND:132-148`,
  `:202-205`; `REQ:123-126`; `RES:116-117`; `C-INT:173`). The full set is delegated to
  `_index/candidates/bf1-opcode-semantics/README.md` (`INT:260-263`). See G-2.

#### Shared value stack (`VmValueStack`, static at `0x02099AC0`, size `0x284`)

| offset | type | meaning | cite |
|---|---|---|---|
| `+0x000` | `s32` | depth; reset to 0 on every interpreter entry (`0025E4D2`/`0025E4D8`) | `C-BR:108-110`; `INT:1036` |
| `+0x004 + i` | `u8` | tag: 1 = int32, 2 = float32 | `VD:378`; `C-BR:113-115` |
| `+0x044 + i` | `u8` | "source type" 0..5 / 6 = literal (`VD:379-380`) — or "source-kind … the complete enum is unresolved" (`C-BR:116-118`); see C-V12 | |
| `+0x084 + i*4` | `u32` | written 0, never read (`VD:381`; `C-BR:119`) | |
| `+0x184 + i*4` | `u32` | the value (int32, float32 bits, or a packed reference) | `VD:382`; `C-BR:120` |

Capacity 63 usable entries (arrays sized 64); pushes refuse at depth 63 (`C-BR:124-128`; `VD:389`). Arguments are
popped top first, so the first value popped is the catalog's `paramType[0]` and the last-pushed argument
(`VD:434-454`; `CC:79-90`).

#### Wait slot (`ActorWaitSlot`, 0x28 bytes; `cmdState` of the lifecycle)

`slot = *(actor+0xA8) + sx(byte actor+0x11) * 0x28` (`BIND:91`; `RES:179`; `CC:104-116`).

| offset | meaning | cite |
|---|---|---|
| `+0x00` | QWORD PC (also the wait key) | `C-INT:77-80`; `C-BR:142` |
| `+0x08` | bound actor id / saved native-command target ordinal (width disputed, C-V15) | `VD:358`; `C-VD:176`; `C-BR:143` |
| `+0x0C` | result value (int or float) | `VD:359`; `CC:96-109` |
| `+0x10` | A register (`PUSHA`/`POPA`, `CALL*POPA`) | `C-BR:145`; `INT:649`, `:657` |
| `+0x14` | wait kind 0..7 | `REQ:92-100`; `C-BR:362` |
| `+0x15` | phase / result tag (values and meaning disputed, C-V20, C-V21) | `VD:360-361`; `CC:217`; `C-BR:147` |
| `+0x16` | serviced / visit marker | `C-BR:148`, `:363` |
| `+0x18` | 16 bytes of command scratch (wait countdown; encoded target for kinds 3/6) | `VD:362`; `C-BR:149`; `REQ:92-107` |
| `+0x1C`, `+0x20`, `+0x22`, `+0x26`, `+0x27` | list-wait encoding, entry id, cursor, channel, completion flag | `REQ:92-107` |

Wait kinds: 0 or ≥8 no dispatch; 1/2 interpreter; 3 target entry absent; 4 detached notification present; 5 actor/id
list cursor end; 6 channel bit clear; 7 actor/channel list cursor end (`REQ:92-100`).

#### Call id and dispatch tables

- `family = id >> 12` (arithmetic), `command = id & 0xFFF` (`VD:107-114`; `NCL:66-69`). Family array `0x02B57EF0`,
  16 × 8 bytes (`VD:121`, `:272`; `C-VD:173`).

| family | table | count | cite |
|---|---|---:|---|
| 0 | `0x01EED700` | 1,496 | `VD:138`; `C-VD:79`; `NCL:81` |
| 3 | `0x01F281B0` | 147 | `VD:139`; `C-VD:80` |
| 5 | `0x01F29418` | 1 | `VD:140`; `C-VD:81` |
| 7 | `0x01F29440` | 104 | `VD:141`; `C-VD:82` |
| 1, 2, 4, 6, 8–15 | `0x01F26720` (shared) | 212 | `VD:142`, `:180`; `C-VD:83` |

Total "**1,960 command slots in five physical tables**" (`VD:144`). A table is `s32 count` at `+0`, pad at `+4`, then
32-byte records at `table + 8 + 32*N`: `+0x00` begin, `+0x08` poll, `+0x10` unused (NULL in all 1,960), `+0x18`
result (`VD:160-174`; `C-VD:103-111`). `C-NCL:100-112` draws the same addresses as "`result(N)` lives in row N+1".
Bounds: a null table or signed `command >= count` returns NULL (`VD:170-172`; `C-VD:113-124`).

#### Lifecycle and callback signatures

- Executor `(rcx manager, rdx issuer, r8 valueStack, r9d id, [rsp+0x28] cmdState)` (`C-VD:266-270`).
- `begin(issuer, owner, cmdState+0x18, valueStack, [rsp+0x20] manager)` — five arguments; `poll(issuer, owner,
  cmdState+0x18)`; `result(issuer, owner, cmdState+0x18, valueStack)` (`C-VD:150-165`, `:287`, `:293`; `NCL:469-477`).
- owner = issuer when `cmdState+8 == *(u16*)issuer`, else `ActorManager_GetRecordByOrdinal(vm, cmdState+8)`
  (`C-VD:278-280`).
- Only `test al, 1` on poll's return matters; begin's return is discarded (`C-VD:440`).
- After result: phase 2 pushes int `+0x0C`; phase ≥3 pushes float; phase 0/1 pushes int 0; a null result pushes
  tag 1 / kind 6 / value 0 through `00262360` (`VD:215-221`; `C-VD:295-300`; `NCL:481-482`, `:683-692`).

#### Variable descriptors and storage homes

- Descriptor at `[slot+0x78 + 4 + index*8]`: bits 0–23 offset; 24–26 class (0 global, 1 file, 2 local, 3 unused, 4
  scratch1, 5 scratch2, 7 array); bit 27 float; bits 28–31 width (0 u8, 1 s8, 2 u16, 3 s16, 4 s32, 5 f32)
  (`VARS:62-72`, `:215-216`).
- Homes: 0 `[slot+0x48]` (save payload `+0x200`); 1 `[slot+0x40]`; 2 `([slot+0x98])(slot, record)` =
  `[slot+0x50] + [[record+0x40]+0x1C]`; 3 `img + [img+0x40]`; 4 `[slot+0x58]` = `02099DF0`; 5 `[slot+0x60]` =
  `02099FF0` (`VARS:122-129`).
- Class-7 array header: element descriptor `+0`, `u16` dimension count `+4`, dimensions from `+8`; each index clamped
  `min(max(index,0), dim-1)` with signed `dim`; row-major flatten that wraps mod 2³² (`VARS:76-89`, `:220-228`).
- `PUSHP` reference: `((desc & 0xFFFFFF) + scaledIndex) | (desc & 0x07000000) | 0x70000000`, tag 1 (`VARS:56`;
  `VD:461-468`). Resolver scope `(packed>>24)&7` → the six homes above, offset `packed & 0xFFFFFF` (`VD:474-493`).
- Store saturation (`0026D530`): u8 [0,255], s8 [−128,127], u16 [0,65535], s16 "[−32767,+32768]", s32/f32 raw,
  widths 6–7 store nothing (`VARS:91-98`; `VD:1421`).
- Actor handle (`PUSHACT`): `(hi16 << 16) | index | (1<<14)`, `hi = u16 actorTable[16*index + 0x0E]`; sentinel
  `0x8000` (`VD:501-515`).

#### Actor entry, request descriptor and entry list

- Actor entry (image `+0x18` table, `u32` count then 0x30-byte entries; 0x20 when the header word < 8): `+0x00`
  name-pool offset, `+0x04` type 0–7, `+0x06` party code (width disputed, C-V6), `+0x08` bytecode base, `+0x0C`
  instruction count, `+0x10` function-offset table, `+0x14` jump list, `+0x18` special-function footer `{u16 count =
  0x12; u16 special[18]}`, `+0x1C` local-area offset, `+0x20` duplicate id, `+0x22` pos (`BIND:48-81`).
- Request descriptor → entry (`BIND:153-163`): kind, mode → `+0x10`, channel → `+0x02`, requester wait slot → `+0x03`,
  function id → `+0x04`, requester self index → `+0x06`, flag → `+0x12` bit 0, manager index → `+0x08`, pc offset →
  `+0x0C`. Target ref `(manager << 16) | ordinal` when bit 14 is set; bit 15 aborts (`BIND:145`, `:165-167`).
- `ActorResourceEntry`, 0x14 bytes: `+0x00` next (0xFF end), `+0x02` channel, `+0x10` request mode 1–4, `+0x11` run
  state (0 free, 1 filed, 2 runnable, 3 started) (`BIND:111-116`, `:192-200`).
- Actor record fields used here: `+0x11` current wait slot (signed), `+0x14` flags (bit 6 idle), `+0x26` channel
  bitset, `+0x60` free-list head, `+0x61` detached head, `+0x88` slot count, `+0x89` detached-walk bound,
  `+0x94[ch]` channel heads, `+0xA0` entries, `+0xA8` wait slots (`BIND:48-55`, `:108-117`; `REQ:49`, `:184`).

#### Native-command bodies documented here

- Spawn wrappers share `void VM_Verb(ActorStorageRecord *rcx, SpawnCtx *rdx, VmEventCtx *r8, VmValueStack *r9)`
  (`CC:49-54`; `C-BR:54-59`); returning verbs end `jmp VMResult_Write*` (`CC:148-153`).
- Entity handle: `id == (u16[rec+0x24] << 16) | (u16[rec+0x1A] | 0x8000)`, `slot = id & 0x7FFF` < 128, table 128 ×
  64 B at `0x0215FDA0` (`NAMES:52-78`); `NameBindingEntry` fields `NAMES:177-208`, `:286`; sub-record (0x120) at
  `0x02161DA0` × 32 (`NAMES:212-237`).
- Treasure placement: `x = (s16)spot[+4] / 10.0`, `z = (s16)spot[+6] / 10.0`, `heading = -(spot[+8] & 0x3F) / 60.0 *
  2π` (`NAMES:90-114`).
- Party read-in machine: 24 states (`READIN:99-120`); record layout `READIN:58-67` vs `:141` (C-V31); voice-pack
  pools `022D9AB0` (2 slots) and `022D9AE0` (4 slots), stride 0x18 (`READIN:181-185`).
- Party appearance: slot map 1 `[02EBF190] + 0x5A5A + 2*slot`, four slots, class `0x17` check, 7..25 range split
  (`LOOKS:172-207`); projection-shadow bits on the 0x740-byte render record (`LOOKS:278-292`).
- Standard motion: per actor pushes motion (int), blend (float, default `-1.0f` from `01CEBC9C`), flag; `003580C0`
  pops flag, blend, motion; negative blend = hard cut, positive = cross-fade (`STDM:90-92`, `:143-153`, `:191`).

#### Debug companion files (not loaded by the shipped game)

`.sbn` (`ATEL:68-98`), `.dbg` (`ATEL:102-260`), `.msb` (`ATEL:421-432`, `:607-617`), `.bin` section-000 header
(`ATEL:722-724`) and `EBP2` directory (`ATEL:735`). `003306E0` "returns without registering anything in this build"
(`ATEL:881-887`), so a port of the shipped game needs none of them.

### 1.3 State (globals and objects, with lifetime)

| state | lifetime as stated | cite |
|---|---|---|
| `ActorManagerSlot` table `02098E10 + slot × 0x288` | the VM context (`r13`); section pointers set only by the binder `0026CB3C`–`0026CB6B` | `INT:265-266`, `:976-977`, `:1005-1006` |
| Value stack `0x02099AC0` | depth zeroed on every interpreter entry; arrays retained | `C-INT:88-89`; `INT:1036`; `RES:39` |
| Instruction budget | `0x10000` per invocation (`0025E4FA`), one per instruction | `INT:1037`; `RES:173` |
| Register file I0–I3 `+0x64..+0x70`, F0–F3 `+0x74..+0x80` | zeroed once at pool allocation; persists for the life of the pool; not saved | `INT:839-841`, `:887-891`, `:931`, `:967-972` |
| Wait slot `+0x00..+0x16` | reset by `0025D460`; `+0x18..+0x27` survives | `REQ:63-64`; `BIND:520-521` |
| Family array `0x02B57EF0` | written by `003DC2D0` — "filled once" (`NCL:174`) or "(re)built" at area init (`C-NCL:282`); see C-V42 | |
| Command tables | static `.data`, no writer | `C-VD:463-465` |
| Skip mask, manager slot `+0x201` | set by `skipexec` / `00360710`, cleared by `00360A50`, written 0 by the bind | `NCL:634-638`; `RES:91-94` |
| `global` variables (save payload `+0x200`–`+0xCF4`) | saved and loaded verbatim | `VARS:124`, `:152`, `:248-250` |
| `file` / `local` variables | per script image / per actor inside the image | `VARS:125-126` |
| `scratch1` `02099DF0` (0x200 B) | cleared on every field transition and at init; not exported | `VARS:128` |
| `scratch2` `02099FF0` (0x200 B) | exported/imported with the save; cleared on a persistence-group change or option bit 3 | `VARS:129`, `:166-169`, `:208-210` |
| Name-binding pool (128 entries) | init `002EA320`; allocation pops `[0215FD60]` and bumps the stamp; release pushes and bumps it | `NAMES:290-311` |
| Party read-in records `02EBF3D0`, `02EBF3F0`, `022C8018` | world-tick record's mask set to `0xF` only when 0, cleared per slot, whole-cleared from boot `00266E29` | `READIN:76`, `:141`, `:210-225` |
| Live party roster `0209A1F0` (four pointers) | zeroed by the field-transition reset `0026DB30` | `STDM:108`, `:205` |

### 1.4 Order (what runs when in a frame, and what triggers it)

1. Frame → `00314020` → `0025D9E0` → `0025DF00` per actor → wait-kind switch (`C-VD:609-616`; `BIND:369-378`).
2. Kinds 1/2 enter the interpreter. A satisfied wait sets kind 1 and the following bytecode runs in the same driver
   invocation (`REQ:102-104`; `C-INT:175`).
3. The interpreter loop: fetch, pre-decode, dispatch, advance by the descriptor length (`add r14`, 4 sites) or rewind
   to suspend (`sub r14`, 21 sites) (`INT:462-472`). It stops on a stop request with an empty stack, on a yield, or at
   the 65,536-instruction budget (`C-INT:100-106`; `RES:110-112`).
4. A call opcode enters `002621D0`: poll fetched up front; phase 0 clears `+0x0C` and runs begin; poll; if `&1`, phase
   1 and return 1 (the interpreter rewinds its PC and yields); otherwise result, push by phase, phase 0, return 0
   (`VD:195-223`; `C-VD:274-302`).
5. A busy call resumes on a later driver invocation at the same PC with phase 1, and polls without begin
   (`RES:24-28`; `C-INT:92-94`). Whether that is "every frame" is disputed (C-V41).
6. `REQ*`: the submit builds a descriptor; same-actor immediate submission skips reselection (`BIND:503-504`). The
   channel walk takes the highest channel first, FIFO within a channel, skips state 1, starts state 2
   (`BIND:107-123`). `REQSW` notifies at start, `REQEW` at removal (`REQ:68-76`).
7. Initialisation: `00266D10` (World) → `003DC2D0`, "built at startup" (`VD:1392`; `C-VD:180`) or at area initialisation (`C-NCL:282`); binder plants sections and the record
   (`BIND:42-56`, `:237`); field transition runs `0026DB30` (`VARS:160-170`).

### 1.5 Dependencies (on other systems)

| system | what this category takes from it | pointer |
|---|---|---|
| 04 Actor / Entity | actor manager record, actor storage record, the field runtime pass | `BIND:44`, `:330-331`; `C-VD:239`; `CC:118`, `:730` |
| 25 EBP Script Container | the bytecode container, section-000, request-channel census | `BIND:58`; `REQ:135`; `VARS:63`; `CC:136-137` |
| 19 Save / Load | save payload map (global variables, scratch2) | `VARS:129`, `:334`; `WAIT:246` |
| 03 World / Area / Field | field environment, field-record table, weather | `VARS:173`, `:181`; `VD:839-840` |
| 05 Spawn | the native targets of the spawn wrappers | `CC:306-308` |
| 11 Party | roster `0209A1F0`, the five slot maps, battle-state block | `BIND:70`; `STDM:108`, `:195`; `LOOKS:205` |
| 06 Movement | movement body pool, separation weight | `NAMES:372-376`, `:423-424` |
| 00 Engine Core | system-stop registry, encoded-id class registry, world tick | `INT:1049`; `LOOKS:398`; `NCL:754` |
| 16 UI | fullscreen menu (`0x0209AC30 + 0xC0`), request router, text control codes | `VD:1136-1142`, `:841-842`; `ATEL:436` |
| 08 Combat Formula | step table `0x01EFA5C0` adjoining family 0 | `DT:97-98`; `VD:188` |
| 21 RNG | which roll is on which generator | `NCL:721` |

---

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open, live-only, or declared limits)

Only items that no later dated text on the 23 pages answers are listed. Items a later section answers are in §3.2.

| id | gap | cite |
|---|---|---|
| S-1 | **Live scheduling, synchronisation, reentrancy and allocation identity.** OV-16 is unticked; both contracts list frame scheduling and reentrancy as unresolved. | `RES:140`; `C-NCL:222`; `C-INT:238` |
| S-2 | Whether shipped play exhausts the request-notification pool, and what recovery follows (OV-10). | `REQ:163`; `BIND:4`, `:532-534` |
| S-3 | RC-12 (which special slot each of the eighteen footer readers asks for): answered on ORACLE's record with a premise correction, but "**FABLE adjudication pending**". The value is corrected at `BIND:79`; the adjudication is not recorded. | `BIND:291` |
| S-4 | RC-16 residue: "which record a spawn entry's function runs on (static, not traced)". | `INT:931` |
| S-5 | 51 of the 436 direct `00267DB0` call sites are undetermined (31 `jmp`, 19 `call`, 1 `ret`). | `INT:873`; `C-BR:88-92` |
| S-6 | The game's MXCSR state; what the process does after an integer divide fault (`idiv` at `0025F0DA`, `OPMOD` at `0025F1F4`); which scripts compare NaNs. | `INT:549-560`; `VARS:113-114` |
| S-7 | What a `global` variable at a given offset means (FZ-27): the TSVs give names and widths only. | `VARS:266`, `:327` |
| S-8 | Which fields share a persistence group id: "authored in that file and not decoded here". | `VARS:179-180` |
| S-9 | Whether any shipped array has a dimension of 0 or less (the clamp reads one element before the array when `dim == 0`). | `VARS:83-89` |
| S-10 | The value-stack `+0x44` byte: "What the other values of that byte are is still unknown"; the bridge contract lists "the complete enum" and "the purpose of the +84 array" as unresolved. | `VARS:469`; `C-BR:116-118`, `:326-329` |
| S-11 | Whether any of the 1,960 handlers reads `begin`'s fifth (stack) argument: "unmeasured". | `C-VD:161-163` |
| S-12 | **No live observation of the dispatcher or any verb.** "breakpoint `002621D0` and read `id`, `phase` … still queued and still unperformed"; "There is still no live evidence". | `C-VD:312`, `:388-389`; `C-BR:303`, `:365`; `STDM:220`; `LOOKS:428-429` |
| S-13 | Parity dimensions `INTEGRATION`, `TIMING`, `PRESENTATION`, `RNG`, `SERIALIZATION`, `FULL SUBSYSTEM` are "Not constructible offline"; "Links 4 and 5 — the 1,228-byte drive and the interpreter — have never been run". | `C-VD:599-602`, `:635-637` |
| S-14 | "Whether the `rsp+0x50` field is the caller-visible return is not proved here" (`POPV`). | `VD:1423` |
| S-15 | The three empty records (`0x0330`, `0x0356`, `0x03B0`): behaviour unrecoverable (CR-2 / UQ-65 "closed NO ADMISSIBLE SOURCE"); two candidate script matches are "unverified". | `WAIT:138-140`, `:182-190`, `:232` |
| S-16 | `003B6F60` and `003B7D30` (the tails of `disposesummon`'s and `changetonormalparty`'s results) are unread. | `WAIT:247-248`, `:342-343` |
| S-17 | What the other 71 callers of the skip-mask reader `00267310` do with the mask. | `NCL:640-641` |
| S-18 | Dispatch-table residual: "a compensating pair of shifts inside one anchor-free window ≤ 25 records is not excluded". | `DT:362-363`, `:979-981` |
| S-19 | Name-binding sub-record `+0x30` and `+0x58` "stay UNRESOLVED"; the writer of `+0x3C` is not among the 16 referencers. | `NAMES:235-237` |
| S-20 | The 997-byte part-slot function's 15 callees "were not read". | `NAMES:467` |
| S-21 | Bridge §14: the reason for the pop asymmetry; values below a command's arguments; other command wrappers and native services; whether single-threaded use holds ("assumed … not proven"). | `C-BR:211-213`, `:333-338` |
| S-22 | EF-2 residue: "35 register-sourced stores at displacement `0x11` on untyped bases, and it is not re-examined here" (a negative wait-slot index). | `CC:526`, `:735-739` |
| S-23 | `00268D10`'s calls to `00377700` and `00317E60` are not read; WorldAreaField edges from `00394130` are "not dispositioned here". | `CC:747-755` |
| S-24 | The 37-verb spawn vocabulary "is a floor, not a ceiling" (direct calls only). | `CC:403-405` |
| S-25 | `DO-1`: the begin and poll handlers are recorded and not classified. | `POP:271-272`, `:286-288`, `:474` |
| S-26 | The verb-reach census does not read handler bodies (UQ-57, superseded as the census's declared scope); 1,029 of the 1,344 blank verbs need handler reads. | `REACH:4`, `:38`, `:194-197` |
| S-27 | Battle party: the Party-layer roster mutators the begins end in, the lock routine, and the per-actor routine the preamble calls are not read. | `BP:56-58`, `:87`, `:127-129`, `:150-151` |
| S-28 | Party read-in: "Writes through a pointer into `02EBF3D0`–`02EBF3FF` were not excluded." | `READIN:226` |
| S-29 | Party appearance: what the `m[+0x08]` bits 1–2 pair selects (SP-1); the third and fourth states of the `+0x304` two-bit field. | `LOOKS:296-297`, `:391-393` |
| S-30 | Standard motion: which values the shipped scripts pass; whether a shipped script issues the SP-2 divergence. | `STDM:213-219` |
| S-31 | Debug companions (not needed by a port of the shipped game, see §1.2): per-`cmd` escape semantics, unpinned arities (`18`, `0F 37 81`), q3 head word `X` ("What X counts is not claimed"), the `.mld` format. | `ATEL:616-621`, `:715-716`, `:810`, `:891-892` |

### 2.2 Structural gaps found while mapping (a port needs these and no 01 page states them)

| id | what is missing | why a port needs it | where the gap shows |
|---|---|---|---|
| G-1 | **The verb bodies.** "**1,886 distinct functions** serve as callbacks" over 2,277 non-null slots. This category describes about forty of them (spawn wrappers, party verbs, entity names, waits/stubs, a few examples). The verb table gives arity and operand types only. | Every script call ends in one of them; without them a port can run the bytecode but not its effects. | `VD:550-553`, `:577-578`; `C-VD:599`; `REACH:4`, `:38` |
| G-2 | **Opcode semantics for about half the 100 opcodes.** The pages give semantics for the opcodes listed in §1.2 and delegate "all 100 handlers" to a candidate directory. Not described on any page: `0x04 SYSTEM`, `0x05`–`0x09`, `0x10`–`0x14`, `0x17`, `0x18`, `0x1D`–`0x20`, `0x2A`–`0x2C` (`PREQ`/`PREQSW`/`PREQEW`, only their shared target `0026121A`), `0x2E`–`0x31`, `0x33 PREQWAIT`, `0x34 REQCHG`, `0x35`, `0x52`–`0x56`, `0x5A`–`0x5C`, `0x62 INCINITTAG`. | The interpreter cannot be written from the pages alone. | `INT:163`, `:260-263`, `:386-411`; `C-INT:233`, `:237` |
| G-3 | **Arithmetic typing per opcode.** Only "Tested int addition wraps at 32 bits; mixed numeric addition uses float32" and the comparator/divide (`0x0A`–`0x0F`, `0x15`, `0x16`) are stated; "Helper call counts do not establish the arithmetic type of every opcode." | Integer vs float results change script behaviour (see C-V2). | `C-INT:82-84`; `INT:532-557` |
| G-4 | **`WorldActorScriptVM_ServiceRequestWaitState` `0025B400`** (108 B): named "the yield point" and shown to test `+0x14 == 4`; its body is not described. | The interpreter's yield path. | `INT:107`, `:117`, `:251`; `VARS:537`; `CC:622` |
| G-5 | **The driver beyond its kind table.** Wait kinds 3–7 have one-line conditions; kind 2 is listed with kind 1 as "Original interpreter" with no stated difference; the footer test at `0025E16A`–`0025E19C` and the driver's other arms are delegated to the 04 field-runtime-pass page. "clears its active-actor global afterward" gives no address. | The resume rules. | `REQ:92-100`; `BIND:216-217`, `:331`; `C-INT:135-136` |
| G-6 | **Interpreter return values**: "This is not a complete error/success taxonomy." | The driver branches on them. | `C-INT:64` |
| G-7 | **The mode-1 start arm `00263230`** of `StartEntryScriptExecution` and the call `0025B580(target)` on a successful submit are named, not described. | Request start-up. | `BIND:188`, `:397`, `:423` |
| G-8 | **Result-list / source-kind byte values.** The value a push writes at `+0x44` for each source, and whether anything reads it, are not settled (S-10, C-V12). | A port must decide what to store. | `VD:379-380`; `C-BR:116-118`; `VARS:465-469` |
| G-9 | **Per-command scratch shapes** beyond `wait`, `*sync` and the verbs read: "Other commands' scratch shapes, service effects, polling conditions and resource ownership" are unresolved. | Every durative verb keeps state in `+0x18`. | `C-NCL:221`; `NCL:524-610` |
| G-10 | **The partition of the 1,960 commands.** `327 + 1,573 = 1,900`; the page never accounts for the other 60 (the TSV's 33 `empty` + 27 `stub(ret 0)`). CY-4's four rows plus "4 none" sum to 1,931. | A port needs the shape of every slot to know which calls block. | `VD:604`, `:1271-1274`, `:1350` |
| G-11 | **Notification ids** returned by `0032F240` to "the voice verbs" are not described; the tables are populated only at runtime. | The notification side of `POPV`'s sibling paths. | `VARS:298-316` |
| G-12 | **Entity names**: the host object of `002650B0` (`002640C0()`) and its six pools; the meaning of the fourteen bind keys ("deliberately opaque"); the `.rdata` constant multiplied with `0x09000707`; the full list-head map (`0215FD58/60/68/70/78/80/90`) is never given in one place; `0050D810`'s verb id; `0037B4D0`'s role as a bind caller. | `setuptreasure` and the bind verbs. | `NAMES:142`, `:244-245`, `:286`, `:345-348`, `:404-416`, `:442-443`, `:606-608` |
| G-13 | **Party read-in machine**: what the verb-mode byte `02EBF3FC` (0 for `summonread`, 1 otherwise) does inside `0037B4D0` (the access TSV shows six reads); the state-2 apply chain and state-22 place chain are address lists; the `0037C2E0` sub-machine; the `highmodelreplace.bin` lookup ("22 records, (a,b,c) keys"); `00233AA0`'s and `00233CF0`'s constituents; the shared poll `0034E3E0`. | The party read-in is what eight party verbs wait on. | `READIN:75`, `:103`, `:119`, `:141`, `:189`, `:391-394`; `STDM:538-540`; `WAIT:98-100` |
| G-14 | **Battle party**: the reconcile algorithm `setbattlemember` runs; the add routine behind `0034C370`; `00324360` ("a boolean of `0037CB50`") has no body. | Who ends up in the party. | `BP:66`, `:91-92`, `:105-106` |
| G-15 | **Standard motion**: what a motion id selects; the `00427860` commit. | The visible animation. | `STDM:81`, `:147-153` |
| G-16 | **Party appearance**: `002E8FD0`'s visibility-refresh gates (via `00428E10`/`00428DE0`/`00429020`); `BattleUnit_FindByDefinitionSelector` `002367A0` is named only. | The visible effect of the shadow / LOD verbs. | `LOOKS:184`, `:577-583` |
| G-17 | **Spawn native targets** (`002366E0`, `002354F0`, `00235360`, `002391C0`, `0023A3B0`, `00239840`, `0023A2E0`) are named and pointed to the 05 spawn pages. | The spawn verbs' effects. | `CC:159-165`, `:306-308` |
| G-18 | **`setuptreasure` order's callees** `0026A320(actor, 1)`, `002640C0()`, `0026AF80`, `0026E060`, and the bind's tail callees `0026A370`, `0026B2E0`, `00269E60`, `00426C90`, `00263A30` are named, not described. | Treasure placement and binding. | `NAMES:140-148`, `:252-262` |

---

## 3. Contradictions (statements a re-implementer would have to choose between)

Quotes are exact, from the snapshot. `…` marks an elision; emphasis markers (`**`, `*`) inside a quote are kept only
where they appear on the page. "Favoured" is named **only** where a dated correction on the pages settles the point;
otherwise the item says **no favoured side**. Every value-changing item is **page-text only - needs local check**: this
session cannot see the executable.

### 3.1 Value-changing (behaviour, offsets, addresses, constants, formulas)

#### Interpreter, driver and requests

**C-V1. What the default dispatch arm `0025E60A` does: nothing, or a stop request.**
- Side A: `INT:150-152`: "**The VM treats those six exactly as it treats an opcode it does not recognise.** They are
  not rejected loudly — `0025E60A` is `mov [rsp+0xC0], ebp ; mov edi, ebp` and continues into the common path — but
  they carry no behaviour of their own." `INT:154`: "**Six of one hundred opcodes are inert in the shipped
  interpreter**".
- Side B: `RES:110`: "`0025E60A` sets a stop request; `0025E613` advances without newly setting it." `C-INT:100`:
  "**I4 — There are distinct epilogue entries.** `0025E60A` requests a stop".
- Status: **favoured side B.** The SECTION-11 correction dated 2026-09-23 on the interpreter page itself says "There
  are separate stop-request and plain-advance entries; zero-length handlers do not all behave alike." (`INT:30-33`).
  `INT:150-154` is not amended. This decides what opcodes `01 02 19 1A 31 47` and any out-of-range opcode do.
- Page-text only - needs local check.

**C-V2. Is script arithmetic float?**
- Side A: `INT:113-115`: "The dominant operation by a wide margin is *pop an int32, coerce to float32* — so the
  bytecode is integer-encoded and the arithmetic is float".
- Side B: `C-INT:82-84`: "Integer arithmetic is not universally float arithmetic. Tested int addition wraps at 32
  bits; mixed numeric addition uses float32, and float-to-int pops truncate."
- Status: **no favoured side.** `INT:95-96` calls the "pop-an-int32-coerce-to-float32" reading "false as a statement
  about the callees", but no dated line strikes `INT:113-115`. See G-3.
- Page-text only - needs local check.

**C-V3. Where the start path reads the wait-slot index: the actor or the entry.**
- Side A: `REQ:182`: "the slot is `[actor+0xA8] + byte[entry+0x11]·0x28`".
- Side B: `BIND:91`: "slot = record.+0x11 (currentWaitSlot, SIGNED); wait = *(record.+0xA8) + slot * 0x28";
  `RES:179`: "the issuing request is `actor+0xA8 + sx(actor+0x11)·0x28`". On the entry, `+0x11` is the run state
  (`BIND:192-200`).
- Status: **no favoured side.** Both are falsification-pass rows (2026-09-29 and 2026-09-30); neither corrects the other.
- Page-text only - needs local check.

**C-V4. Function sizes on the binding page that do not contain their own cited addresses.**
- `003DBDC0`: `BIND:422`: "`003DBDC0` `ActorResource_StartEntryScriptExecution` (41 B)" — against `BIND:10`:
  "ActorResource_StartEntryScriptExecution (0x3DBDC0-0x3DBE0C) read in full" (76 B) and `BIND:199`:
  "`ActorResource_StartEntryScriptExecution` `003DBE68`" (a store past both extents).
- `00268850`: `BIND:438`: "`00268850` (`ScriptVM_SubmitActorRuntimeRequest`, ~250 B)" — against interior sites up to
  `00268A48` (`BIND:188`), 0x1F8 bytes past the entry.
- `00358A00`: `BIND:431`: "`00358A00` (21 B)" — the same row cites `00358A24`/`00358A37`, past `00358A15`.
- Status: **no favoured side.** A port that copies these extents would cut the functions short.
- Page-text only - needs local check.

**C-V5. Which footer word the driver tests: `special[11]` (`parameter`) or `special[12]` (`mapjump`).**
- Side A (corrected): `BIND:79`: "~~the wait resolver's "word `+0x18` when the count exceeds 11" is `special[12]`, the
  `mapjump(12)` function~~ *Corrected 2026-09-30 (OPUS …): word `+0x18` is `special[11]`, the actor's `parameter`
  function - the footer is 0-based".
- Side B (unstruck): `BIND:290`: "wait resolver's `mapjump` test is §2.6".
- Status: **favoured side A** by the 2026-09-30 correction. The RC-12 adjudication is still "pending" (`BIND:291`,
  S-3).
- Page-text only - needs local check.

**C-V6. Width of actor-entry `+0x06`.**
- Side A: `BIND:70`: "| `+0x06` | `u8` party code".
- Side B: `BIND:76`: "| `+0x06`… | the `u16` ff12-script writes as `pcId`".
- Status: **no favoured side.**
- Page-text only - needs local check.

**C-V7. What `00226BE0` is.**
- Side A: `INT:1049`: "it is `00226BE0`, the system-stop registry's request start, which builds the records, marks
  every actor and raises the dirty flag" (pointer 2026-09-30).
- Side B: `BIND:397-399`: "`00263230` — the mode-1 arm of `ActorResource_StartEntryScriptExecution` — calls
  `00226BE0`, an Input-layer helper that builds a per-channel bitmask … the entry-start path consults the input
  channel state."
- Status: **no favoured side.** The 2026-09-30 line is a pointer on another page, not a correction of `BIND`.
- Page-text only - needs local check.

#### Native command lifecycle and dispatch tables

**C-V8. What the family-table initialiser installs, and at which address.**
- Side A: `DT:532-533`: "`VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2D0`) fills an array of **16 family
  tables** at `0x02B57EF0`: twelve share a default at `0x01F26720`"; `DT:627-629`: "(`003DC2D0`, 89 B) writes the array:
  a `rep stosq` of `0x01F26720` over all 16 slots, then four overrides". `C-NCL:54`, `VD:115-131` and the
  `native-command-family-tables-accesses.tsv` row agree.
- Side B: `DT:763-764`: "`VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2F0`) is nine instructions and
  installs **four** bases."; `DT:774-775`: "**Families 1, 2, 4 and 6 are never installed** — which is why the accessor
  null-checks the table pointer before touching it."; `DT:835`: "whatever writes that slot is the answer, and it is
  not `003DC2F0`."
- Status: **no favoured side** on the pages (both are undated 2026-09-02-era sections of `DT`). Three other pages
  and the TSV state side A. If side B held, calls in families 1, 2, 4, 6 would return NULL instead of reaching the
  shared table.
- Page-text only - needs local check.

**C-V9. Table extents: whether the tables abut, and where family 0 ends.**
- Side A: `DT:643-646`: "**The four tables abut exactly** … **There is no gap, no terminator and no padding between
  them**"; `DT:57`: "the table occupies `01EED700`..`01EF9208`".
- Side B: `DT:860`: "So the tables are adjacent but **not contiguous** — 16, 8 and 8 bytes of slack."; `DT:769`:
  "| **0** | `02B57EF0` | `01EED700` | **1496** | `01EED700`..`01EF9200` |".
- Status: for family 0's end, **favoured `01EF9208`**: `DT:57` carries the 2026-09-19 (FABLE) restoration of the
  `tbl + 8 + 0x20n` frame, under which the last record ends at base + 8 + 0x20 × 1,496. The abut/slack pair uses the
  same two end conventions and is **not settled** by a dated line.
- Page-text only - needs local check.

**C-V10. Sizes of the begin and result accessors.**
- Side A: `DT:752-753`: "`VMNativeCommandDispatch_GetBeginCallback` (`003DC270`) and `…GetResultCallback`
  (`003DC2A0`) are the same 36 bytes at a different field offset."
- Side B: `C-NCL:55-57` give `003DC270` 39 B, `003DC240` 39 B, `003DC2A0` 41 B (re-checked "461 / 89 / 39 / 39 / 41 B",
  `C-NCL:266`); `VD:279` agrees; `DT:736` itself gives the poll accessor "39 bytes".
- Status: **no favoured side.** The result accessor also has no displacement (`inc rax / shl rax,5`, `DT:275`), so
  "the same … at a different field offset" does not describe it.
- Page-text only - needs local check.

**C-V11. Does an out-of-range command fail closed?**
- Side A: `VD:170-172`: "**An out-of-range verb fails closed**; it does not read past the table."; `NCL:232-233`: "an
  out-of-range command id fails closed with a null callback rather than reading past the table."
- Side B: `C-VD:113-118`: "### ⚠ CORRECTED 2026-09-12 by the 40th pilot — the guard is ONE-SIDED … `cmp edx,[rcx] /
  jge` is a **signed** compare and `movsxd rax, edx` sign-extends"; `C-NCL:115-117`: "the signed bounds check is `N <
  count`, which permits `result(count−1)` to read at `tbl + 32*count` — one row past the counted rows."
- Status: **favoured side B** for negative commands, by the 2026-09-12 correction; the contract also says the case is
  unreachable from bytecode (`C-VD:126-138`). The `C-NCL` "one row past" wording is a row-model statement: it is the
  same address as record `count−1`'s `+0x18` in the `VD` frame.
- Page-text only - needs local check.

**C-V12. What the value-stack byte at `+0x44` holds.**
- Side A: `VD:379-380`: "+0x044 + i u8 source type 0..5 = the declared type of the variable it came from (uchar,
  char, ushort, short, int, float); 6 = a literal or computed value, not from a variable".
- Side B: `C-BR:116-118`: "source-kind byte; direct pushes store6. Existing variable-load evidence distinguishes
  descriptor byte0 from its separate high-nibble selector. Do not equate those fields; the complete enum is
  unresolved."; `VARS:469`: "**What the other values of that byte are is still unknown.**"
- Status: **no favoured side.** (`NCL:378` "always 6" describes the lifecycle's own append only.)
- Page-text only - needs local check.

**C-V13. Entering the executor with phase ≥ 2: does poll run?**
- Side A: `VD:201-208`: the pseudo-code has only `if (phase == 0) {…}` and then "/* phase 0 and 1 both fall through
  to poll */ running = poll ? poll(b, owner, cmdState + 0x18) : 0;" — no phase ≥ 2 arm.
- Side B: `C-VD:217`: "phase >=2 --result----------> push, phase 0 (NO begin and NO poll; EXP-085 (2))";
  `C-VD:223-226`: "anything else falls through to `00262255`, which fetches `result` and calls it directly … an entry
  at phase >= 2 pushes whatever `+0xC` already held".
- Status: **favoured side B**, by §13b "EXP-085's findings, adjudicated against the bytes — 2026-09-17 (OPUS)"
  (`C-VD:391-452`). `VD:705-718` (BQ-5, 2026-09-26) adds that no writer leaves phase 2/3 behind.
- Page-text only - needs local check.

**C-V14. How many arguments a callback receives.**
- Side A: `VD:242`: "Every callback receives the same four things, in the Microsoft x64 convention:"; `C-VD:148`:
  "Microsoft x64, and the same four things every time:".
- Side B: `C-VD:158`: "**`begin` takes FIVE arguments, and the fifth is on the stack** — added 2026-09-13".
- Status: **favoured side B** by the 2026-09-13 addition. Whether any handler reads the fifth is S-11.
- Page-text only - needs local check.

**C-V15. Width of `cmdState+0x08` (the bound actor id).**
- Side A: `VD:358`: "+0x08  u32   bound actor id      compared against *(u16 *)b at 00262225".
- Side B: `C-VD:176`: "`+0x08` bound actor id (u16)".
- Also: `C-VD:416`: "`00262225 mov edx, dword [rdi+8]` — **`dword [cmdState+8]`**".
- Status: **no favoured side**; the contract disagrees with itself.
- Page-text only - needs local check.

**C-V16. How many commands have no callback at all: 33 or 4.**
- Side A: `VD:726`: "The **90 rows still without a measured arity**: 33 command slots with no callback at all";
  `VD:1058`: "| slot has no callback at all | 33 |"; `VD:1242`: "33 slots with no callback".
- Side B: `VD:606-608`: "~~**27 command slots point at the 3-byte `ret 0` stub** and 33 have no callback at all.~~
  **34 callback slots over 33 commands point at the 3-byte `ret 0` stub** … and **4 commands have no `begin`, `poll`
  or `result` callback at all**. Measured 2026-09-15".
- Status: **favoured side B** by the 2026-09-15 correction. The 33 are 29 poll-only plus the 4 (the TSV's `empty`
  shape). A port that took side A would make 29 waiting verbs inert.
- Page-text only - needs local check.

**C-V17. What `0x20D3` is.**
- Side A: `VD:677-679`: "`0x20D3` is the **last id of family 2** and its handler is `0016D6A0`, the folded three-byte
  `ret 0` — the terminator the dispatch falls closed onto".
- Side B: `C-VD:503-504`: "**8 poll-driven records** (`begin` stub + `poll` `005C5230`, `result` real or NULL — family 0
  518/521/882/883/884/1198, shared 211, family 3 32)". Shared-table command 211 is `0x20D3`; the verb table carries
  begin `0016D6A0`, poll `005C5230`.
- Status: **no favoured side.** `VD:170-172` also says out-of-range commands return NULL rather than land on a
  terminator.
- Page-text only - needs local check.

**C-V18. Instantaneous commands: 1,573 all result-only, or 1,571 plus two that can block.**
- Side A: `VD:229-230`: "That is why 1,573 of the 1,960 commands are instantaneous"; `VD:604`: "**327 verbs are
  durative, 1,573 are instantaneous.**"
- Side B: `VD:1271`: "| `result` only — *instantaneous* | 1,571 |"; `VD:1319-1321`: "**Two verbs are labelled
  `instantaneous` and carry a `poll`** … **these two can block despite the label.**"
- Status: **favoured side B** by CZ-1 "*Answered 2026-09-14 (FABLE, `CZ-1`)*" (`VD:1324-1337`). The TSV label is not
  corrected.
- Page-text only - needs local check.

#### Bridge, calling convention and result tag

**C-V19. Is the four-register signature universal?**
- Side A: `CC:30-31`: "exposes the **calling convention every native verb in the game uses**"; `C-BR:205-207`: "this
  contract is the calling convention every one of them obeys."
- Side B: `C-BR:50-52`: "It is not a universal signature for begin/poll/result callbacks: Section11 executes begin
  with a fifth manager argument, poll without a newly supplied R9 stack argument, and result with its own surface".
- Status: **favoured side B**: it is the SECTION-11 production correction dated 2026-09-23 (`C-BR:28`), and it
  agrees with C-V14. `C-BR:205-207` contradicts its own `:50-52`.
- Page-text only - needs local check.

**C-V20. Which values wait-slot `+0x15` takes, and where `1` is written.**
- Side A: `C-BR:266-268`: "**No tag above 3 exists** — resolved 2026-09-14: the entry-typed `+0x15` writer population
  is enumerated image-wide and writes only 0 (interpreter clear), 2 and 3 (§14 item 2)."; `C-BR:359`: "`+0x15` writer
  population is exactly {clear 0, int 2, float 3} … | 1 | PROVEN |".
- Side B: `C-BR:330-332`: "**Corrected object identity:** `0026230B` DOES write phase1 in the same selected
  ActorWaitSlot used by the result writers. … The prior whole-image exclusion of this site was wrong."; `C-BR:199`:
  "lifecycle `0026230B` writes1, `00262382` writes0".
- Side C: `CC:444-448`: "Across all six, `+0x15` takes **`0`, `1`, `2`, `3`** and nothing else. **`1` is written
  exactly once in the EXE, and not as a byte:** … `00261B97  mov word ptr [rsi + 0x14], 0x107`".
- Status: that `1` **is** written is **favoured** by the SECTION-11 correction (2026-09-23, `C-BR:28`, §14 item 2).
  Which site writes it (`0026230B`, `00261B97`, or both) is **not settled**.
- Page-text only - needs local check.

**C-V21. What the `+0x15` values mean.**
- Side A: `CC:217`: "| `+0x15` | result entry | type tag; `0` none, `1` armed, **`2` = int32**, `3` = float32 |".
- Side B: `C-BR:147`: "entry +0x15   u8          phase0 begin pending,1 poll pending;2 int/3 float typing during
  completion".
- Status: **no favoured side.**
- Page-text only - needs local check.

**C-V22. Does a pop with an unknown tag consume the slot?**
- Side A: `C-BR:237-239`: "`PopInt32` treats any tag other than 1 or 2 as the error path (`00267E31`, after the
  decrement, so `depth` **is** consumed); `PopFloat32` … also after the decrement." The execution table row `C-BR:311`
  (EXP-013, 2026-09-10): "an unknown tag (0, 3, 255) returns 0 / +0.0 and consumes the slot (depth 1 → 0)".
- Side B: `C-BR:397-398` (falsification pass 1, 2026-09-12, about the empty-stack and unknown-tag paths in the table
  at `:391-396`): "On every one of the four paths the depth word at `[rcx]` is left untouched, so a refusal is not a
  pop."
- Status: **no favoured side** by a correction; the 2026-09-10 execution row supports side A.
- Page-text only - needs local check.

#### Variables

**C-V23. What an out-of-range array index reads.**
- Side A: `VARS:254`: "Array indices are clamped, not checked: an out-of-range read returns the edge element
  silently."
- Side B: `VARS:83-84`: "`min(max(index, 0), dim - 1)` with the dimension read as a signed dword, so the edge element
  is read only when the dimension is 1 or more. A dimension of 0 gives index -1, one element before the array".
- Status: **favoured side B** by the 2026-09-28 qualifications (`VARS:80-89`).
- Page-text only - needs local check.

#### Verbs on this category's pages

**C-V24. ATRAC3 verb shapes.**
- Side A: `WAIT:95` lists `atrac3standbysync` and `atrac3playsync` among the 26 poll-only waits; `WAIT:101-102`: "both
  poll `005C5230` — **the stub**"; `WAIT:125`: "| `atrac3cancel` | `0016D6A0` | `005C5230` | — |".
- Side B: `WAIT:239-241` (2026-09-26): "the dispatch records register all five ATRAC3 verbs the same way, with a result
  callback only, and exactly one of them is the folded `ret 0`. There is no two-shape split to explain."
- Status: **no favoured side.** The dated note is later, but `scriptvm-verb-table.tsv` shows side A (`04AB`/`04AD`
  poll-only `005C5230`; `04AE` begin `0016D6A0` + poll `005C5230`).
- Page-text only - needs local check.

**C-V25. Arity of `unkCall_5c7` (`0x05C7`).**
- Side A: `WAIT:126`: "| `unkCall_5c7` | — | — | `0016D6A0` | — takes **2** arguments |".
- Side B: `WAIT:338-340`: "**`arity 0`** and **`arity_status CONFLICT`**. §2's table states the 2 flatly."
- Status: **no favoured side**; the page flags it and leaves the table unedited.
- Page-text only - needs local check.

**C-V26. What `003B7180` is.**
- Side A: `WAIT:373`: "`003B7180` (129 B) is a wait/do-nothing verb body"; `WAIT:383`: "the four-slot readiness poll
  `003B7180` runs for the wait verbs".
- Side B: `WAIT:248`: "`00350F30` (`changetonormalparty`) calls `003B7D30()` and tail-jumps `003B7180`" — a result
  that does real work (`WAIT:213-216`).
- Status: **no favoured side.**
- Page-text only - needs local check.

**C-V27. Width of the entity stamp.**
- Side A: `NAMES:286` (2026-09-17): "a stamp that is sixteen bits wide"; `NAMES:68`: "`u16[rec + 0x24]`".
- Side B: `NAMES:317-319` (2026-09-14): "The stamp is a full `dword`: the release compares it as one (`002E949A`)";
  `NAMES:553-554`: "a **dword** load, not the `u16` §2's formula writes."
- Status: **no favoured side.** The later answer does not strike the dword compare; a port must choose the
  comparison width.
- Page-text only - needs local check.

**C-V28. Do all fourteen bind keys land?**
- Side A: `NAMES:243-244`: "**the fourteen keyed values land in the actor's `+0xB8` steering record, the `+0xC0` render
  link, and the render record itself**".
- Side B: `NAMES:333`: "So thirteen of the fourteen keys have a destination, and the fourteenth is a dead read."
- Status: **favoured side B** by the UQ-60 answer "ANSWERED 2026-09-14 (FABLE) … with two corrections" (`NAMES:321`).
- Page-text only - needs local check.

**C-V29. Which verbs are the bind family, and which call the bind.**
- Side A: `NAMES:46`: "**`setuptreasure`, `puppetbind`, `bindp`, `bindh`, `bindc`** — the whole *bind* family".
- Side B: `NAMES:455-456`: "**The bind verbs** are `bindp`, `bindh`, `bindc` and `puppetbind`. Their six callbacks are
  `003409F0`, `00342640`, `00345A60`, `00344550`, `00344200` and `003463F0`." The bind's caller table (`NAMES:437-443`)
  lists only `00355210`, `003409F0`, `00342640`, `0050D810`, `0037B4D0`.
- Status: **no favoured side.** Whether `bindh`, `bindc` and `puppetbind` call `002E28E0` at all is not stated.
- Page-text only - needs local check.

**C-V30. Where the name-binding `requestMask` lives.**
- Side A: `NAMES:207`: "`+0x28` requestMask / `+0x2C` readyMask (per-selector bits set by `002EB9D0`)".
- Side B: `NAMES:600`: "`r8d<<cl` into `[r10+rax*4+0x48]` requestMask, `~bit` AND into `+0x2C`".
- Status: **no favoured side.**
- Page-text only - needs local check.

**C-V31. Size and first field of the party read-in record.**
- Side A: `READIN:36`: "The machine's record is 12 bytes: an encoded actor pointer"; `READIN:59-60`: "party read-in
  record 12 bytes … `+0x00` u32 actor encoded image pointer".
- Side B: `READIN:141`: "the two static **`PartyReadMachineRecord`** instances (declared 2026-09-18, size `0x18`) …
  `+0x00` `boundRowRef` (base-relative authored-row offset, `0020E620`/`0020E600`)".
- Status: **no favoured side.** The two may describe the machine operand and the static instance; no line joins them.
  The access TSVs touch `+0x0C`..`+0x10`, which fits `0x18`.
- Page-text only - needs local check.

**C-V32. What `0037CE80` writes to the state byte.**
- Side A: `READIN:208-209`: "`0037CE80` fills `+0x00` resolved id, `+0x08` state 0, `+0x09` param, `+0x0A` counter 0,
  `+0x0B` = `002DEBD0`".
- Side B: `READIN:352-355` (SWE2-EC7-92, 2026-09-20): "bytes `+8`/`+9`/`+0xA`/`+0xB` come from the
  `002DEBD0`/`002DEB90` pair under the `0016D6A0` gate, `[rdi+0x23]` is cleared, and `+8` gains `0x80`."
- Status: **no favoured side.**
- Page-text only - needs local check.

**C-V33. Where states 7, 10 and 13 store their handle.**
- Side A: `READIN:62`: "`+0x04` u32 pending handle … written by states 1 (0037B720) and 19 (0037BEA8)".
- Side B: `READIN:108`: state 7 "requests the new one (`0031BEC0(actor, 0)` → `002EB7A0` → `002EAE20`), stores its
  handle" (and states 10 and 13 do "the same").
- Status: **no favoured side**; the store location for states 7/10/13 is not stated.
- Page-text only - needs local check.

**C-V34. `VM_Spawn_ApplySelectedUnit`: `00510160` or `005101B0`.**
- Side A: `READIN:79`: "| `VM_Spawn_ApplySelectedUnit` `005101B0` |"; `READIN:204`: "`005101B0` is
  `VM_Spawn_ApplySelectedUnit` `0x3001`'s step".
- Side B: `READIN:336`: "`VM_Spawn_ApplySelectedUnit` `00510160`, the middle entry of the verb triple"; `CC:163`:
  "| `VM_Spawn_ApplySelectedUnit` `00510160` | 72 B |".
- Status: **no favoured side.** The triple `{00510440, 00510160, 005101B0}` (`READIN:205`) and the verb table (begin
  `00510160`, poll `005101B0`) suggest the name belongs to the begin, but no page says so.
- Page-text only - needs local check.

**C-V35. The 0x740-byte render-record table base.**
- Side A: `LOOKS:283`: "`char *e = *(char **)0x022C6F28 + (int64_t)idx * 0x740;`" (a pointer read through).
- Side B: `LOOKS:636`: "`sx(cx) * 0x740 + 022C6F28` resolves the record"; `READIN:160`: "the `0x740` record pool at
  `022C6F28`" (a direct base).
- Side C: `LOOKS:580`: "render-record array at `020FB7xx` (`imul rcx, rax, 0x740`".
- Status: **no favoured side.**
- Page-text only - needs local check.

**C-V36. Offset of the movement context written by `002E5C90`.**
- `LOOKS:396`: "the **movement context** `[actor+0xB8]` (*corrected 2026-09-18, FABLE: the 0x230-byte context at actor
  `+0x120` in [the context census]…*". One sentence gives `+0xB8` and `+0x120`; `READIN:103` says "the three floats at
  actor `+0xB8`".
- Status: **no favoured side**; the correction renames the target without saying which offset is right.
- Page-text only - needs local check.

**C-V37. `002E9C00`: a definition byte or a runtime byte.**
- Side A: `STDM:483-487`: "`WorldActor_GetDefinitionByte12OrMinus1` … `movsx eax, byte [rax+0x12]` … the signed
  definition byte the verb predicates on."
- Side B: `READIN:197-199`: "note the doc's `WorldActor_GetDefinitionByte12OrMinus1` is that runtime byte, **not** a
  definition read".
- Status: **favoured side B** by UQ-51 "Answered 2026-09-16 (SWE2-STRUCT)" (`READIN:191-192`).
- Page-text only - needs local check.

**C-V38. Which battle-party verbs run the roster preamble.**
- Side A: `BP:56-57`: "The two `set` verbs first walk roster slots 0-3 and call one routine on every actor present".
- Side B: `BP:84`: "`addguestbattlemember` … the `set` verbs' preamble"; `BP:156`: "the slot-0..3 preamble in the three
  verbs that have it".
- Status: **favoured side B** (three verbs) by falsification pass 1, 2026-09-29 (`BP:146`, row B1 `:156`). Which
  three is not listed.
- Page-text only - needs local check.

**C-V39. Which verbs reach the read-in installers.**
- Side A: `READIN:71-79` lists `partyallread` 0x3EB, `partyallread2` 0x46F and `summonread` 0x203.
- Side B: `STDM:206-208`: "the read-in verbs `partyallread` (`0x03EB`), `partyallread2` (`0x046F`), `summonread`
  (`0x0203`) and `summontopartyread` (`0x0207`) through `0037C980` / `0037CA00` / `0037CA80`".
- Status: **no favoured side.**
- Page-text only - needs local check.

**C-V40. What `0037CA80` resets.**
- Side A: `STDM:493-495`: "three sibling globals get field resets (`+8` = 0, `dword` = 0, `+4` = 4, `+0x1C` = 0) and two
  flag bytes, then it tails `00233CF0`."
- Side B: `READIN:75`: `summonread` installs "start 0, step +1, and `02EBF3FC` = 0" (the second-instance access TSV
  shows three byte writes, `+0xC`, `+0xE`, `+0xD`).
- Status: **no favoured side.**
- Page-text only - needs local check.

#### Lifecycle timing and table lifetime

**C-V41. Is a running command polled every frame?**
- Side A: `NCL:54-55`: "the command is started, polled every frame while it runs"; `NCL:182` (call chain, 2026-09-30):
  "once per frame per actor while the verb runs."
- Side B: `NCL:547`: "Invocation count is not automatically live frame count."; `C-NCL:196`: "No particular
  relationship between invocation count and live elapsed frames is established here."
- Status: **favoured side B**: it belongs to the SECTION-11 production rewrite dated 2026-09-23 (`NCL:29-34`), which
  says "Historical audits do not certify this rewrite". Side A is not amended.
- Page-text only - needs local check.

**C-V42. When the family-table pointers are written.**
- Side A: `NCL:174`: "family table 02B57EF0[family] (filled once by 003DC2D0)".
- Side B: `C-NCL:282`: "Area initialisation is where the sixteen family-table pointers at `02B57EF0` are (re)built".
- Status: **no favoured side.**
- Page-text only - needs local check.

**C-V43. Two accessor descriptions inside the lifecycle page.**
- Side A: `NCL:100`: "GetBeginCallback  (003DC270):  *(void **)(tbl +  8 + 32*command)"; `NCL:105`: "All three
  bounds-check `command` against `*(int *)tbl` — the count".
- Side B (subtree section): `NCL:783-784`: "`003DC270` (`GetBeginCallback`, record `+0`)"; `NCL:777`: "`GetPollCallback`
  — bounds-checks `family` against `dword[02B57EF0]` (`003DC253`)".
- Status: **no favoured side** on `NCL`; `C-NCL:105` and `C-NCL:123-124` agree with side A.
- Page-text only - needs local check.

#### Debug companion files (not loaded by the shipped game; a port of the shipped game does not need them)

**C-V44. Narrowing text that a 2026-09-28 correction supersedes, still unstruck.** `ATEL:809` says "Three claims in
the narrowings above are superseded, §2 carries the corrected text". Each pair below is **favoured side B** by the
dated correction named.
- `.sbn` page trailer — A: `ATEL:805`: "full pages are `{u16 lineOff[32]; u16 chunkEnd; u16 0}`"; B: `ATEL:96`: "the
  trailer is a single **u32**, not `{u16 chunkEnd; u16 0}`" (Corrected 2026-09-28, `ATEL:94`).
- `.dbg` header slots — A: `ATEL:804`: "The header is three `(offset, size)` pairs"; B: `ATEL:103`: "**(section
  offset, table offset)**, not (offset, size) (corrected 2026-09-28".
- Debug-flag index — A: `ATEL:806`: "btlctrl index `N` ↔ `global_debug_flag[N+34]`"; B: `ATEL:209-210`: "**exactly `N
  = 0..0xFFF` ↔ `global_debug_flag[N]`**" (the front-table correction 2026-09-28, `ATEL:124-126`).
- q0 line numbering — A: `ATEL:806`: "**`pos` is the 0-based source line number**"; B: `ATEL:281`: "**`lineNo` is a
  1-based logical line.**" (qualified 2026-09-28, `ATEL:277`).
- Heap landings — A: `ATEL:806`: "T3/T4/T8/q1 land mid-string at irregular depth"; B: `ATEL:391`: "the earlier "may
  land mid-string" claim is retracted" ("Correction 2026-09-22, still standing", `ATEL:242`).
- T1 — A: `ATEL:807`: "***T1 RESOLVED 2026-09-22 (SWE2-DATA): it is the ATEL verb-category directory.**"; B:
  `ATEL:234-235` retracts that reading (and `ATEL:809` item 3).
- Page-text only - needs local check.

**C-V45. Debug-companion figures that disagree with no dated settlement** (all **no favoured side**):
- `003306E0` size — `ATEL:880`: "the function is 3,882 bytes" vs `ATEL:917`: "`003306E0` (~351 B)".
- `evctrl` scope-1 overrun — `ATEL:264`: "runs 143 bytes past its directory span" vs `ATEL:273`: "continues 144 bytes
  past".
- S2 shape — `ATEL:113`: "**S2 = a 64-slot directory**" vs `ATEL:387-388`: "65 entries for ctrl/evctrl/btlctrl, 301
  for mapctrl".
- `btlctrl` heap start — `ATEL:243`: "`0x1CA20` in `btlctrl`" vs `ATEL:393`: "`btlctrl` it runs `0x1CD7D..~0x41F4F`".
- q1 contents — `ATEL:302-304`: "**no variable names at all**" vs `ATEL:400-401`: "each scope's q1 lists exactly its
  `@`-labels and named variables".
- Page-text only - needs local check.

#### Counts that disagree (no engine behaviour attached, but a port's tables would differ)

| id | side A | side B | status |
|---|---|---|---|
| C-V46 | `VD:36-38`: "**1,870 of the 1,960 rows carry a measured arity**; on the 1,210 of those that the authored catalog also names and declares, the two agree **1,209 times**"; `README:22-23` repeats it | `VD:730`: "*ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: all 90 now have an arity"; the TSV has arity on 1,960 rows and `cat_args == arity` on 1,269 of 1,270 | **favoured side B** by BQ-9 (2026-09-27) |
| C-V47 | `VD:592`: "`fsmenu` for the 33 fullscreen-menu verbs" | `VD:1221`: "the **unguarded** half of the family (62 of 104" (so 42 guarded); the TSV's `guard = fsmenu` is on 42 rows | no favoured side |
| C-V48 | `VD:1160`: "on **65 of its 131 callbacks**"; `VD:1162`: "Family 7's records come in exactly four shapes" (20/22/54/5 = 101) | `VD:141`: family 7 has 104 records; the TSV adds 3 poll-only records and 64 guarded callbacks | no favoured side |
| C-V49 | `VD:672`: "**Family 3's seven are `0x3086`–`0x308F`**" (a 10-id range) | the TSV names `0x308A`–`0x308C`; the seven are `3086`–`3089`, `308D`–`308F` | no favoured side |
| C-V50 | `POP:159`: "The declared adapter family — 1,053 of the 1,682 frontier callbacks"; `POP:170-173`: 964 / 71 / 18; `POP:175`: "The **629 frontier callbacks that fail the rule**" | `POP:26` front matter: "members/scriptvm-verb-adapter-callbacks.tsv \| 1030"; the TSVs hold 1,030 (944 / 68 / 18) and 503 leftovers | no favoured side; the front-matter departures log does not sum from 1,053 to 1,030 |
| C-V51 | `DT:390-391`: "The other **259 implement `begin` and `poll`**" | `DT:1023` counts 26 poll-only; the verb table shows 259 = 160 begin+poll + 73 begin-only + 26 poll-only | no favoured side |
| C-V52 | `DT:198`: "(1,224 rows)"; `C-BR:205`: "the 1,224-row dispatch table in `Verb-Dispatch/scriptvm-dispatch.tsv`"; `README:28` "1,224 catalog rows" | the TSV header: "1,493 rows", extended 2026-09-19 and 2026-09-26 | no favoured side on the pages (the TSV's own header is dated) |
| C-V53 | `NCL:117-118`: "1,155 of 1,496 records with a single non-null field" (family 0) | `C-NCL:133-134`: "every one of the 1,155 single-callback commands"; `NCL:493`: "1,573 of the 1,960 commands work at all" | no favoured side |
| C-V54 | `NCL:243-247`: "The authored verb catalogue ([the verb table]…, 1,960 ids) … **2** (212 …)" | `NCL:276`: "The authored catalogue is the ff12-script decompiler's command table (`CScriptContainerInitializers.cpp`, 1,954 entries …) … 211 in family 2" | no favoured side; two different lists share one name |
| C-V55 | `VARS:152`: "`+0x200`–`+0xCF4` of the persistent payload is the script-global variable space**, 0xAF5" bytes | `script-global-variables-by-offset.tsv` ends with a `u16` at `0xCF4` (to `0xCF5`, i.e. 0xAF6 bytes) | no favoured side |
| C-V56 | `INT:908`: "172 functions in 84 scripts read a register before writing it" | `register-opcodes-by-script.tsv` fills `read_before_write_in_some_function` for 96 scripts | no favoured side (the column is not defined on the page) |
| C-V57 | `CC:344-345`: "**`0x10`** for the single-int verbs" | the verb table gives `0x00` for `304A` and nothing for `304B`/`305F` | no favoured side |
| C-V58 | `REACH:337`: "ActorEntity **162** against 142" | `REACH:358` (RC-21, 2026-09-30): "ActorEntity 135–154" across 100 seeds | no favoured side; RC-21's range excludes 162 |
| C-V59 | `READIN:108`, `:111`, `:112`: transition sites `0037B946`, `0037BA3B`, `0037BB43` | `members/party-read-states.tsv`: state writes at `0037B94C`, `0037BA47`, `0037BB4F` | no favoured side (the page may cite the branches) |
| C-V60 | `BP:9-12`: "eleven bodies" | the same sentence lists twelve addresses | no favoured side |

All rows: page-text only - needs local check.

### 3.2 Stale "not read / open" claims, struck-but-repeated text, and banner disagreements

These do not change a value; a re-implementer would only be misled about what is known. "Answered by" names the
dated line that settles it where there is one.

#### Status banners and front matter

| id | stale or banner text | answered or contradicted by |
|---|---|---|
| C-S1 | `README:19`: `VD` "**DOCUMENTED, tier 1.**"; `VD:1249`: "`DOCUMENTED`, three falsification passes survived" | `VD:4`: "status: AUDITED". Also `VD:20` `audit.passes: 4` against "three falsification passes" (`VD:1249`). Not settled. |
| C-S2 | `README:28`: `DT` "**DOCUMENTED, tier 2.**"; `DT:40`: "**DOCUMENTED.**" | `DT:4`: "status: AUDITED"; `DT:420`: "**Why this is PARTIAL rather than DOCUMENTED.**" Not settled. |
| C-S3 | `INT:35`: "This page is REOPENED, preserving its older audit receipts." | `INT:4`: "DOCUMENTED — the SECTION-11 reopening is resolved (accepted non-author 2026-09-29 …) … (owner re-status 2026-10-01, OPUS)"; `README:15` agrees with `INT:4`. |
| C-S4 | `NCL:43`: "**Historical DOCUMENTED assessment; current corrections require review.**" | `NCL:4` (re-status 2026-10-01) and `NCL:46-48`: "*(Reconciled 2026-09-30, SWE2-CONTRACT: the review is done — …)*". |
| C-S5 | `REACH:57-58`: "`status: PARTIAL` is the honest state."; `REACH:245`: "its status `PARTIAL`" | `REACH:4`: "status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS)". |
| C-S6 | `BIND:4`: "REOPENED — …"; `BIND:525`: "this correction reopens the mechanism pending review" | `BIND:527`: "*Reconciled 2026-09-30 (SWE2-CONTRACT, cited).* **The review is done:**" |
| C-S7 | `C-INT:28`, `C-NCL:28`, `C-BR:25`: "formal independent acceptance pending"; `RES:11`: "independent acceptance pending"; `REQ:32`: "It is not … independent acceptance." | `INT:27` and `NCL:26`: "accepted non-author 2026-09-29 (SWE2-AUDIT-SEM, OV-18)"; `RES:142` OV-18 "NOT A QUESTION 2026-09-29"; `BIND:527-531` "returning `verdict:ACCEPT`". |
| C-S8 | `readiness: CONTRACT READY`, `confidence: PROVEN` on all four contracts (`C-INT:6-7`, `C-NCL:6-7`, `C-BR:6-7`, `C-VD:6-7`) | `C-INT:39-40`: "not complete execution or semantic acceptance"; `C-VD:361-362`: "Status `FAIL`, reported as it came back."; `C-BR:38`: "not `RECONSTRUCTION READY`". `C-VD:22`: "crossref_clean: false        # audit_crossrefs.py reports nothing for this document" (the value and its comment disagree). |
| C-S9 | `last_reviewed` older than the page's own dated edits: `INT:18` 2026-09-02; `VD:18` 2026-09-02; `DT:18` 2026-09-07; `NCL:18` 2026-09-07; `CC:15` and `POP:17` 2026-09-08; `BIND:13` and `VARS:14` 2026-09-11; `C-BR:17` 2026-09-11; `ATEL:20` and `C-VD:17` 2026-09-12; `WAIT:18` and `NAMES:17` 2026-09-13; `READIN:12` 2026-09-14 | latest dated edits: `INT:931` (2026-10-01); `VD:730` (09-27), `:1423` (09-30); `DT:1131` (09-26); `NCL:194` (10-01); `CC:657` (09-25); `POP:26` (10-01); `BIND:79` (09-30); `VARS:439` (09-29); `C-BR:24` (09-23); `ATEL:807`, `:810` (09-30, 09-29); `C-VD:456` (09-22); `WAIT:232` (09-30); `NAMES:286` (09-17); `READIN:214` (09-25), `:330` (09-29) |
| C-S10 | `ATEL:795-797`: "## 6. Falsification pass / Not yet run." | `ATEL:816`: "## 9. Falsification pass 1 — 2026-09-13 (OPUS)"; `ATEL:26-27`. |
| C-S11 | `STDM:21-22`: "last_pass: 2026-09-13 … EVERY figure reproduces and there is no correction" | `STDM:328`: "KILLER TESTS RUN — 2026-09-14 (FABLE). Three hold. One is refuted". |
| C-S12 | `BP:20-23` (front matter): "the three add verbs' begins and the flag pair keyed 0x13 are not read … pending first review" | `BP:79-87`: "The add side, read whole 2026-09-19"; `BP:146` falsification pass 1, 2026-09-29; `BP:156`. |
| C-S13 | `LOOKS:426-427`: "This is why the document is `L1` and not `L2`: … the presentation consequence is not." | `002E8CE0` and `002E5C90` "read 2026-09-18" (`LOOKS:4`, `:396`, `:425`). Not settled. |
| C-S14 | Duplicate section numbers: `DT` has two "## 14." (`DT:605`, `:729`) and no §11; `VARS` has two "## 9." (`VARS:329`, `:336`) | structural; links to "§9" on `VARS` mean the falsification section. |

#### Interpreter, scheduling and contracts

| id | stale or banner text | answered or contradicted by |
|---|---|---|
| C-S15 | `INT:257-258`: "**no handler has been read for semantics**"; `INT:312`: "**BF-1 holds the whole semantic layer open.**"; `INT:427`: "**BF-1 stays open:**"; `RES:160-161`: "remaining opcode/service semantics are still separate obligations"; `C-INT:237`: "Remaining opcode semantics" | `INT:260`: "*ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: all 100 handlers are read"; `RES:137`. `INT:312-314` and `:429` carry stale pointers; `RES` and `C-INT` do not. |
| C-S16 | `C-INT` §14 (`C-INT:237-241`): "other wait kinds"; "register reuse"; "Authored operand/index bounds and resource lifetime"; "Meaning/producer scope of the actor-indexed control byte"; `C-INT:133`: "Full resource lifetime not established."; `C-INT:195`: "The existing ASTRA live register-reuse task remains separate." | `REQ:92-100`, `RES:138` (OV-14, 2026-09-29); `INT:931` (register file persists for the life of a pool); `RES:141` (OV-17, 2026-09-29); `RES:94`, `:139` (OV-15: the skip mask, 2026-09-29); `INT:935` ("no live observation is needed"). |
| C-S17 | `INT:1001`: "`+0x201` … a byte fed into every handler in `edx`" | `RES:94` (OV-15, 2026-09-29): "the indexed control is the target manager's skip mask (manager record `+0x201`…)". |
| C-S18 | `INT:238-239` (unstruck): "**`0x00261DF8` is the single point of control over the whole scripting language.**" | `INT:247-249`: "~~**`0x00261DF8` is the single point of control …**~~ **FALSE — there are two coupled tables.**" (§10, 2026-09-02). |
| C-S19 | `INT:981-982`: the interpreter's third argument is "the actor's request entry in `r8`" | `C-INT:58`: "R8 its selected `ActorWaitSlot`"; `BIND:100-101`. "Entry" elsewhere is the 0x14-byte `ActorResourceEntry` (`BIND:112`). |
| C-S20 | `INT:326`: "The interpreter has one entry, `0025DF00`, ticked per frame" | `C-INT:9`: `entries: ["0025E4C0"]`; `INT:1138-1141`: `0025DF00` is the one call site. |
| C-S21 | `BIND:205-207`: "Who else promotes a state-1 entry to 2 was not found in the functions read" | `BIND:301` (RC-14): "**ANSWERED 2026-09-30 …:** image-wide, exactly three stores reach an entry's `+0x11` … plus the insert". |
| C-S22 | `BIND:381`: "**Not claimed:** the other seven kinds remain unnamed" | `BIND:283-287`: "*Answered (pointer 2026-09-30, SWE2-CONTRACT):* the wait kinds 0–7 … are enumerated"; `REQ:92-100`. |
| C-S23 | `BIND:228-229`, `:280`: which special slot each footer reader asks for "is not read here" | `BIND:291` (RC-12, 2026-09-30), pending adjudication (S-3). |
| C-S24 | `BIND:156`: "`+0x10` (the store's `state` row …)" | `BIND:192`: "It is now declared separately from **`+0x10` request mode**; the older no-store-row statement is superseded." |
| C-S25 | `BIND:261-262`: "`StartEntryScriptExecution` → `WorldActorScriptVM_InterpretBytecode`." | `INT:1138-1139`: one direct call site, from `0025DF00`; `BIND:94` shows `003DBDC0` only sets PC and kind. |

#### Native command lifecycle, dispatch tables and verb dispatch

| id | stale or banner text | answered or contradicted by |
|---|---|---|
| C-S26 | `C-NCL:97-98`: "*Whether that is deliberate aliasing or a fallback for unimplemented families is `AO-1` and is not settled here.*"; `C-NCL:220`: "complete catalog reconciliation"; `NCL:87-89` | `NCL:242-243`: "**AO-1 ANSWERED 2026-09-12 (FABLE): the shared table is family 2's, and the other eleven are verb-less fallbacks.**"; `NCL:276` (AO-5, 2026-09-18). |
| C-S27 | `NCL:262-263`, `:322`: "Family **3** is **spawn**"; `NCL:317-318`: "Why a family was spent on it is open" | `NCL:268` (AO-4, 2026-09-27): "Family 3 is the battle-actor set, not only spawn."; `NCL:270-274` (AO-6 closed 2026-09-12). |
| C-S28 | `NCL:346-347`: "**`_guard_check_icall`** as their `result` callback — the bare `ret 0` at `0016D6A0`"; `NCL:351` "the disabled CFG stub" | `VARS:57`: "~~that callee is the CFG stub~~ — it is the **folded no-op** … Corrected 2026-09-13". |
| C-S29 | `NCL:597`: `FUN_00267310(actorState[0x15])` | `NCL:621-626`: the CE-5 correction (SECTION-11, 2026-09-23) — `00267310(idx)` reads `02099011 + sign_extend(idx)*0x288`. |
| C-S30 | `NCL:129`: the executor "branches three ways" | `NCL:133-138` and §12 (`NCL:452-510`): fall-through; the §11 block is labelled "REFINED in section 12" (`NCL:399-402`). |
| C-S31 | `DT:199-200`: "**Rows are a lead, not fact** — the index mapping is known wrong in at least one region."; `DT:345-346`; `DT:418`; `DT:420-424` | `DT:61-64`: "CORRECTED 2026-09-07 … the call ID, exactly". |
| C-S32 | `DT:249-253`: "Record layout (interpretation UNPROVEN beyond field +0)"; `DT:104-106` | `DT:57` (restored 2026-09-19) and `DT:267-301` (superseded 2026-09-16). |
| C-S33 | `DT:784-786`: "header occupies record 0's `+0` field … so record 0's `+0` slot holds the count and its begin/poll fields are live" | `DT:191`: "*Restored 2026-09-19 (FABLE): these 32 bytes are not a header*". |
| C-S34 | `DT:217-223`: "**`scriptvm-dispatch.tsv` has the two callbacks one call id early.** … **259 of the 304 asynchronous verbs have no row in that file at all**" | the TSV header: begin/poll columns "RE-FRAMED 2026-09-19 (OPUS)" and 259 rows added; the page is not updated. |
| C-S35 | `DT:1030-1031`: "**Left open:** the **26 records with a `poll` callback and nothing else**" | `WAIT:87-89`: "**This closes `CE-1`**". |
| C-S36 | `VD:945-946`: "69 writes in the interpreter, 0 reads … Left open rather than explained away." | `VD:638`: "**BQ-1 ANSWERED 2026-09-13 (FABLE):** … **78 stores**". |
| C-S37 | `VD:1062`: "**BQ-7** stays open on those four categories."; `VD:1236`, `:1242-1245` (BQ-9 "Ninety rows") | `VD:721-725` (BQ-7 CLOSED 2026-09-02); `VD:730-740` (BQ-9, 2026-09-27). |
| C-S38 | `VD:56-59`: verbs that take time "hold the script until they are done" | `VD:1266-1267` (CY-4, 2026-09-08): "**for 77 verbs that gloss is wrong.**" |
| C-S39 | `VD:1321-1322`: "Neither handler is read. `CZ-1`." | `VD:1324`: "*Answered 2026-09-14 (FABLE, `CZ-1`)*". |
| C-S40 | `C-VD:557-558`: "`VA-1` — what that slot was for — stays open"; `C-VD:584-585` "§13 and `VA-1` are unchanged" | `C-VD:456-457`: "~~**`VA-1`** — what the unused `+0x10` slot was for.~~ — **resolved 2026-09-22 (SWE2-CONTRACT) as far as the image can resolve it: dead space in the 32-byte stride.**" |
| C-S41 | `C-VD:584`: "**Not claimed:** the lifecycle half is still unexecuted" | `C-VD:315`: "**CORRECTED 2026-09-16 (OPUS).** THE LIFECYCLE HALF WAS EXECUTED THREE DAYS AGO". |
| C-S42 | `C-VD:594-596`: "`STATE-TRANSITION` … Still constructible offline and still not built" | `C-VD:317-319`: EXP-085, "35/35 cases pass". Not reconciled (an experiment, not a parity fixture). |
| C-S43 | `C-VD:493-494`: "The source page counts populated callbacks per family; it does not separate the stub." | `VD:292`, `:606-611` (corrected 2026-09-15) separate it. |

#### Verb population, reach and calling convention

| id | stale or banner text | answered or contradicted by |
|---|---|---|
| C-S44 | `POP:271-272`: "Only the *begin* handler is classified in §3. **The 261 poll and result handlers are recorded and unclassified**"; `POP:333-335`, `:458`, `:461` (old slot labels) | `POP:286-288` ("Slot names corrected 2026-09-22 (FABLE)": "is a census of **result** handlers … is **begin and poll**"); `POP:268-269`. |
| C-S45 | `POP:154-155`: "240 of 583 single-call verb handlers"; `POP:433-438`: "the eight verb handlers above" | `POP:110`, `:119-126` (regenerated 2026-09-13: 238 of 584); `POP:398`: "**Ten handlers, not the eight this section first named.**" |
| C-S46 | `POP:466-468`: "**`scriptvm-verb-shapes.tsv` is unchanged.** The four rows still carry the old family" | `POP:56-57` (regenerated 2026-09-13); the TSV carries the corrected rows. |
| C-S47 | `REACH:25`: "so the map is stale against the older GN160 snapshot"; `REACH:50-51`, `:269`, `:346-347`: five rows "drift at the current snapshot" | `REACH:358` (RC-21, 2026-09-30): "the five rows do not drift with the snapshot." |
| C-S48 | `REACH:259`: "`Save_Load_Settings` appears only at depth ≥ 2" | `REACH:122`: "~~from nothing~~ **from 1 at depth 1**"; `REACH:331`. |
| C-S49 | `CC:230-231`: "five of the seven tail-call their native target" | `CC:413-418`: "**Three, three and one.**" (2026-09-13). |
| C-S50 | `CC:301-302`: "What any other result tag means … UNKNOWN"; "Which script opcode reaches these verbs … UNKNOWN"; `CC:205`: "`002640C0`, `002650B0` … **not read**" | `CC:238` (EF-1, 2026-09-13); `CC:267-285` (UQ-55/EF-5); `CC:247-257` (EF-3, 2026-09-11). |
| C-S51 | `CC:238`, `:444`, `:646`: "all **six**" sites | `CC:430-432`: "~~exactly six~~ **Corrected 2026-09-14 (OPUS) … the census is SEVEN**". |
| C-S52 | `CC:526`: "`EF-2` (a negative slot index) is untouched"; `CC:654-655`: "`EF-2` stays open on the producer side" | `CC:239-246`, `:657-739` (UQ-54 answered 2026-09-25); residue S-22. |
| C-S53 | `CC:526-528`: the meaning of slot `+0x10`, `+0x16`, `+0x18`, `+0x1C`–`+0x27` "is **not** established" | `C-BR:141-151` names them; see C-V21 for `+0x15`. |
| C-S54 | `C-BR:36`, `:264`: EF-1 answered "in part"; `C-BR:404`: "whether tags above 3 exist is still `UNKNOWN`" | `C-BR:266-268` (2026-09-14), itself disputed by C-V20. |

#### Verbs on this category's pages

| id | stale or banner text | answered or contradicted by |
|---|---|---|
| C-S55 | `WAIT:204`: "`0034E3E0` | poll shared by `summonreadsync` and `summontopartyreadsync`" | `WAIT:98-100`, `:313-315`: four verbs (§7, 2026-09-13). |
| C-S56 | `WAIT:342`: "**Not claimed.** `CR-2` and `CR-3` stand."; `WAIT:342-343`: the result bodies' callees "were not" read | `WAIT:239` (CR-3 dissolved 2026-09-26); `WAIT:232` (UQ-65 closed 2026-09-30); `WAIT:363` (`00237D60` read 2026-09-14); `WAIT:373`, `:383`. |
| C-S57 | `WAIT:30-31`: "Nine are PlayStation-era leftovers" | `WAIT:217-218` names five; four rows of the stub table say "—" (`WAIT:118-126`); the attribution is tier 8 (`WAIT:261`). |
| C-S58 | `NAMES:484`: "eleven users, five of them named verbs" | `NAMES:532-549`: seven named verbs, ten callbacks. |
| C-S59 | `NAMES:492-493`: "what a record holds with a map loaded | **not established** | — | UNKNOWN"; "any runtime observation | **none exists**" | `NAMES:286` (UQ-58, 2026-09-17); `NAMES:471-474` (UQ-63 superseded 2026-09-14). |
| C-S60 | `NAMES:564-566`: "`ER-1` and the "does the stamp ever change" question stay open. `002E28E0`, `002EC5B0`, `002650B0`, `0026DAC0` remain unread."; `NAMES:354-357`: "**NOT read: what it does with the fourteen values.**"; `NAMES:193-195`: "that the stamp ever changes is not observed" | `NAMES:286`, `:302` (UQ-59, 2026-09-14), `:320-333` (UQ-60), `:358-383`, `:384-421`, `:422-426`. |
| C-S61 | `NAMES:186`: "`+0x1E` | `0xFFFF` in all 128 | unknown, uniform"; `NAMES:352-353`: "uses the `.rdata` constant `30.0f` at `008F8D80`" | `NAMES:205-206` (subTableIndex, 2026-09-18); `NAMES:249-250` ("corrected 2026-09-14, FABLE": 50.0f). |
| C-S62 | `READIN:39`: "in four part slots"; `READIN:59`: "three statics are known" | `READIN:157`, `:163` (UQ-49, 2026-09-16: six elements, "one enum, not 'four slots'"); `READIN:141`: "the two static … instances". |
| C-S63 | `STDM:166`: "the discarded extra argument of `0540`/`0541`"; `STDM:72`, `:162-163`, `:178`, `:316` ("discard") | `STDM:66`: "**Refuted 2026-09-14 (FABLE): the extra argument is the float.**" |
| C-S64 | `STDM:311-313`: "It **is not a push** — it is `edx`" | `STDM:338-340`: "**OPUS's refinement above … does not stand**" (2026-09-14). |
| C-S65 | `STDM:142`: "What the `-1.0f` means to the pop that consumes it is still open."; `STDM:386`: "`00233F50` and `002ED020` remain unread" | `STDM:143` (answered 2026-09-30); `STDM:142` ("Both read 2026-09-18 (FABLE)"). |
| C-S66 | `STDM:107`: "then three gates and a 7..25 range split" | `LOOKS:325`: "four slots, two gates, one range test"; `LOOKS:352`. Not settled. |
| C-S67 | `LOOKS:410-411`: "The second half … remains open."; `LOOKS:532`: "What the four setters do — **none of their bodies was read here**"; `LOOKS:636`: "the scripted colour/alpha triple" | `LOOKS:421` (RC-18, 2026-09-30); `LOOKS:384`; the superseding note on `LOOKS:636` itself (2026-09-30: "a position, not a colour"). |
| C-S68 | `BP:56`: "the setter itself was not read here"; `BP:128`: "Not read: … the flag setter and clearer keyed `0x13`"; `BP:55`: "Each pops its arguments from the script stack, then **raises flag `0x13`**" | `BP:156`: "`003601B0` / `003601C0` set and clear bit `cl` of `022CB720`"; `BP:162`: "`setbattlemember` runs its preamble and raises the flag (`0034D542`) before its first pop" (2026-09-29). |

---

## 4. Rating

**Overall: NOT YET.** The machinery that runs a script is documented closely. What a script *does* is not: the
verb bodies (G-1) and about half the opcodes' semantics (G-2) are not on the category's pages.

| part | rating | why |
|---|---|---|
| Dispatch tables, call-id split and the begin / poll / result lifecycle | **MOSTLY** | The table layout, the accessors, the executor's arms and the push rules are stated at instruction level, and the lifecycle was executed from shipped bytes (EXP-085, `C-VD:315-334`). Open: which tables the initialiser installs (C-V8), the `cmdState+0x08` width (C-V15), what `0x20D3` is (C-V17), and the per-command scratch shapes (G-9). C-V11, C-V13, C-V14 and C-V16 are each settled by a dated correction, but the stale side is still printed on `VD`. |
| Value stack and the script-to-native calling convention | **MOSTLY** | Layout, capacity, coercion, argument order, references and actor handles are stated. Open: the `+0x44` byte (C-V12, S-10), the unknown-tag pop (C-V22), and the `+0x15` values and writers (C-V20, C-V21). |
| Variables and storage classes | **MOSTLY** | Descriptor format, the six homes, array clamping, saturation and persistence are stated and agree with the TSVs. Open: variable meanings (S-7), group-id sharing (S-8), the stale edge-element rule (C-V23, settled 2026-09-28). |
| Request scheduling (`REQ*`, the entry list, the channel walk, wait kinds) | **MOSTLY** | The submit, admission, channel walk, wait kinds and notification are stated. Open: the wait-slot index source (C-V3), three function extents (C-V4), the driver beyond its kind table and kind 2 (G-5), the mode-1 start arm (G-7), live scheduling and pool exhaustion (S-1, S-2). |
| The interpreter (dispatch loop and opcode set) | **NOT YET** | **Structural gap.** The loop, the dispatch, the length table, the budget and the stop/advance arms are stated (the default arm is settled as a stop request, C-V1). But about half the 100 opcodes have no semantics on any page (G-2), arithmetic typing per opcode is not stated (G-3, C-V2), and the yield path `0025B400` is undescribed (G-4). |
| Verbs (the native handlers) | **NOT YET** | **Structural gap.** 1,886 callback functions; about forty are described here (G-1). The verb table gives arity and operand types only. |
| Party verbs, entity names, waits and stubs (the verbs this category does describe) | **MOSTLY** | The verb layer of each is stated. Open: the party read-in record (C-V31–C-V34), the render-record base (C-V35), the bind family (C-V29), the ATRAC3 shapes (C-V24), and the unread Party-layer mutators (S-27, G-13, G-14). |
| Debug companion files (`.sbn`, `.dbg`, `.msb`) | not needed | The shipped game never loads them (`ATEL:881-887`). Their pages carry eleven value disagreements (C-V44, C-V45). |

**To reach MOSTLY overall**, the database would need:
- the semantics of every opcode on the interpreter page or its contract, not only in the candidate directory (G-2),
  with arithmetic typing per opcode (G-3) and the body of `0025B400` (G-4);
- a local check of C-V2, C-V3, C-V8, C-V12, C-V15, C-V17, C-V20, C-V21 and C-V22 against the image;
- a statement of which category owns each verb body. If the verbs belong to their subsystems' pages, the category's
  README could say so, and G-1 would become a dependency rather than a gap.
