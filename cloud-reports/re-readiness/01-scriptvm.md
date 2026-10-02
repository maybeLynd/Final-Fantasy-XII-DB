# Reconstruction readiness — `FFXII TZA/01-Script-VM-Native-Bridge/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-01-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`86b70c69`); no executable, Ghidra or live game was used. Several pages in this folder are being edited by other lanes; every quotation is the snapshot's text. |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. |

**Counts:** *(filled in when the report is complete — see the final commit)*

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
| `VMNativeCommandDispatch_InitializeFamilyTables` `003DC2D0` (89 B) | area initialiser `00266D10` (World); "built at startup" (`C-VD:180`) | fills the 16-entry family array; see C-V16 for a disagreement on what it installs | `C-NCL:54`, `:282`; `VD:278`, `:1392`; `DT:532`, `:627-629` |
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
| `+0x08` | bound actor id / saved native-command target ordinal (width disputed, C-V30) | `VD:358`; `C-VD:176`; `C-BR:143` |
| `+0x0C` | result value (int or float) | `VD:359`; `CC:96-109` |
| `+0x10` | A register (`PUSHA`/`POPA`, `CALL*POPA`) | `C-BR:145`; `INT:649`, `:657` |
| `+0x14` | wait kind 0..7 | `REQ:92-100`; `C-BR:362` |
| `+0x15` | phase / result tag (values and meaning disputed, C-V38, C-V39) | `VD:360-361`; `CC:217`; `C-BR:147` |
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
  name-pool offset, `+0x04` type 0–7, `+0x06` party code (width disputed, C-V9), `+0x08` bytecode base, `+0x0C`
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
- Party read-in machine: 24 states (`READIN:99-120`); record layout `READIN:58-67` vs `:141` (C-V44); voice-pack
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
| Family array `0x02B57EF0` | written by `003DC2D0` — "filled once" (`NCL:174`) or "(re)built" at area init (`C-NCL:282`); see C-V58 | |
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
   (`RES:24-28`; `C-INT:92-94`). Whether that is "every frame" is disputed (C-V59).
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
