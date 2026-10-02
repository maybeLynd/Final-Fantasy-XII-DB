---
system: The script-to-native calling convention, read from the seven spawn verbs
category: 01-Script-VM-Native-Bridge
status: AUDITED
owner_layer: PrimaryOwner:Script_VM_Native_Bridge
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: all seven verb bodies plus both bridge helpers disassembled from the shipping EXE; the
    result-entry stride derived from the addressing arithmetic; names taken as leads from
    Collaboration research prose and re-derived
last_reviewed: 2026-09-08
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-script-to-native-calling-convention-pass-1
  last_pass_kind: falsification
  crossref_clean: true
  reopened_count: 0
---

# The script-to-native calling convention

> **Imported from the research backlog, then re-derived.** Seven `VM_Spawn*` verbs and the two
> helpers they share. See [`../../_index/RESEARCH-IMPORT-BACKLOG.md`](../../_index/RESEARCH-IMPORT-BACKLOG.md).
>
> **The verbs are the smaller half of the finding.** Reading seven of them together exposes the
> ~~**calling convention every native verb in the game uses**~~ calling convention of the native `result` callbacks *(corrected 2026-10-02, OPUS: `begin` also receives the manager as a fifth argument, `002622C4`–`002622CD`, and `poll` only three registers, `002622EE`–`002622F8`)* — how a script's arguments arrive, in
> what order, and how a value gets back.

## 1. What the player sees

Nothing directly — but this is the doorway through which a zone's authored script reaches the
engine. When an area decides *which* enemy appears at a point, whether that spawn counts against the
area's population cap, or how long before a defeated one returns, it is a script calling one of these
verbs.

**For a modder it is the boundary that matters most**: anything on this list can be changed by editing
script; anything not on it needs a native hook. ~~These seven are the entire spawn vocabulary the script layer has.~~ **They are not** — they are the seven this page reads; the spawn vocabulary is **37 verbs** (§10, 2026-09-13).

## 2. The convention — four registers, two helpers

**Every one of the seven has the same signature**, which is how the convention can be read off them
rather than guessed:

```c
void VM_Verb(ActorStorageRecord *actor /*rcx*/,  /* was `VmResultCtx *result`: the same record, named by its owner (2026-09-11) */
             SpawnCtx    *target /*rdx*/,
             VmEventCtx  *event  /*r8*/,
             VmValueStack *stack /*r9*/);
```

`rcx` is only used by verbs that return something, `r8` only by verbs that raise an actor operation,
and `r9` only by verbs that take arguments — which is why the unused ones are simply never touched.

### Arguments in — `VMValueStack_PopInt32CoerceFloat32` (`00267E10`, 78 B)

```c
int pop(VmValueStack *s) {
    int depth = s->i_00;
    if (depth <= 0) return 0;       /* EF-6, read 2026-09-10: 00267E18 jle -> 00267E3B xor eax,eax / ret.
                                       No error call, depth untouched; the caller cannot tell it from a 0 */
    s->i_00 = --depth;
    u8 type = s->b[4 + depth];      /* the tag byte for this slot; the VALUE is in a separate
                                       array at +0x184, stride 4 - see the pass section */
    if (type == 1) return s->value[depth];             /* tag 1 = int32   (00267E51) */
    if (type == 2) return (int)s->valuef[depth];       /* tag 2 = float32, cvttss2si (00267E42) */
    008620C0(1); return 0;    /* the reporting arm OF THIS POP - the float pop reports on the
                                 opposite condition instead; see the pass section */
}
```

**The stack is depth-prefixed and tagged**: an `int` count at `+0x00`, then one **type byte per slot**
from `+0x04`. The pop decrements first and reads the tag at the new depth, so it is a true LIFO.

> **⚠ Arguments arrive in reverse.** `VM_Spawn_BindEntryAndMarkCapTracked` pops twice from the same
> stack and passes the **first** popped value as argument 2 and the **second** as argument 3:
>
> ```asm
> 00510408  call 0x267E10 / mov ebx, eax     ; first pop  -> becomes edx (arg 2)
> 00510412  call 0x267E10 / mov r8d, eax     ; second pop -> becomes r8d (arg 3)
> 0051041C  mov rcx, rsi / jmp 0x239840
> ```
>
> **So the first value popped is the last the script pushed.** A reimplementation that reads
> arguments left to right will pass them in the wrong order, and for this verb both are integers, so
> nothing will complain.

The name says it coerces float to int, so **a script may push either and the verb sees an `int`.**

### Results out — `VMResult_WriteInt32` (`0026B4E0`, 28 B)

```asm
0026B4E0  movsx rax, byte ptr [rcx + 0x11]     ; the result slot index, SIGNED
0026B4E5  lea   r8, [rax + rax*4]              ; ×5 …
0026B4E9  mov   rax, qword ptr [rcx + 0xA8]    ; the result array
0026B4F0  mov   byte  ptr [rax + r8*8 + 0x15], 2   ; … ×8 = stride 40; type tag = 2
0026B4F6  mov   dword ptr [rax + r8*8 + 0x0C], edx ; the value
```

```c
void VMResult_WriteInt32(ActorStorageRecord *a, int v) {
    ActorWaitSlot *e = a->slotsA8 + (signed char)a->currentWaitSlot;   /* +0xA8, +0x11; 40 bytes per slot */
    e->slotState = 2;                                 /* at +0x15: 1 armed, 2 int result, 3 float result */
    e->value     = v;                                 /* at +0x0C */
}
```

**Result entries are the actor's wait slots, 40 bytes** — the record's `slotsA8` array indexed by
its `currentWaitSlot` (OPUS-CONTRA-VMRESULTCTX, 2026-09-11) — the state byte lives at `+0x15`, the
`int32` payload at `+0x0C`, and **the writer stores `2` for int32, `3` for float32**; no reader
distinguishes the two, every test is against 0. The slot index at `c + 0x11` is read with `movsx` — **signed** — so a
negative index is representable and nothing here rejects it. *Narrowed 2026-09-13 (EF-2):* the only producer found for the actor record's `+0x11` is `ActorResource_SelectPendingEntryForExecution` (`003DB6E0`): it walks the channels from `slotCountA8 - 1` down to 0 through their list heads `+0x94[ch]`, and for the first entry whose run state is not 1 stores that entry's channel byte (`003DB750`–`003DB754`) — an entry reached from a channel list, which the remover treats as non-negative (`003DB2FE`–`003DB303`). The record's constructor zeroes the field. A census of the 87 `.text` stores with displacement `0x11` finds no other on an actor storage record — the ones in the actor families are flag masks on manager slots (`0025DA09`, `0026CAD1`, `003303DF`), resource-entry run states (`003DB8E9`, `003DBE68`, `003DC1A4`) and a `+0xC0` sub-object's flags (`00265BA4`, `00265FB8`) — but not all 87 were typed, so a negative index is unproduced by every writer read, not proven impossible. *Narrowed further 2026-09-14 (FABLE, EF-2): no path that stays inside the record's arrays can produce a negative
cursor, and the one that could corrupts the record first.* The route-proven access census of the actor storage record
([`actor-storage-record-accesses.tsv`](../../04-Actor-Entity/Actor-Storage-Record/actor-storage-record-accesses.tsv)) has
exactly **one writer** of `+0x11`, the store at `003DB754`. That store copies byte `+0x02` (the entry's channel) of an entry
the selector reached through the channel tails `+0x94[ch]`, `ch = +0x88 − 1 … 0` (`003DB6F3`–`003DB750`). Entry `+0x02` is
written only by `ActorResource_InsertEntryFromDescriptor` (`003DB906`, `003DBA08`), from the descriptor's channel. For a
script request that channel is **the low byte of the popped value** (`002689B1 mov [rsp+0x22], sil`), checked by nothing
but the insert's **upper** clamp (`003DB7C1`–`003DB7C5`, signed compare). A channel byte ≥ `0x80` therefore enters as a
negative number. Script requests use modes 1–3, which take the channel-list path, and that path indexes the list heads with
the sign-extended channel (`003DBA0C`, `movzx ebx, byte [rbp + r10 + 0x8C]`). A negative channel reads and links through
bytes **below** the head array, in the `+0x88`–`+0x8B` counts, before any selection. The selector only walks tails
`0 … count − 1`, so the entry would never be selected normally. **A negative `+0x11` therefore needs corrupted channel
counts, and that needs a script `REQ` family opcode whose channel operand has its low byte ≥ `0x80`.** Whether any shipped
script passes one is an authored-data question, routed as `FABLE-REQ-SWE2-DATA-REQ-CHANNEL-RANGE`. The live samples on
[the record page](../../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md) (80, cursor within the count
in all) agree and prove nothing about the authored corpus. *(Re-applied 2026-09-14: the first application was reverted by
a peer harness's `git checkout` before it was committed; `OPUS-NOTE-FABLE-HARNESS-REVERTED-A-FILE`.)*

*Closed 2026-09-18 (SWE2-DATA, `FABLE-REQ-SWE2-DATA-REQ-CHANNEL-RANGE`):* the authored side is now
measured, not sampled. A full-corpus scan of all 10,036 valid `section_000` script images
(237,662 script bodies; [`req-channel-census.tsv`](../../25-EBP-Script-Container/Bytecode-And-Opcodes/members/req-channel-census.tsv),
[`gen_req_channel_census.py`](../../25-EBP-Script-Container/Bytecode-And-Opcodes/members/gen_req_channel_census.py))
enumerates **326,204 descriptor-building sites**. The only channel-carrier opcodes that ship are
`REQ` (197,102 sites), `REQEW` (101,398) and `REQSW` (27,704) — `FREQ`/`TREQ`/`FREQSW`/`TREQSW`/`FREQEW`/`TREQEW`
never appear in the corpus. Every channel operand is an authored immediate: **distribution
{0:18, 1:242611, 2:43738, 3:16446, 4:13347, 5:7929, 6:198, 7:1917} — maximum `0x07`, zero sites ≥ `0x80`**.
The channel is the first-pushed of the three arguments (`PUSH channel; PUSH target; PUSH funcid`), matching
the third-pop read into `sil` at `002689B1`; `PREQ*` and the wait/cancel/change opcodes consume already-built
entries and carry no channel operand of their own. **A negative `+0x11` is therefore unreachable from shipped
authored scripts** — UQ-54's route needs a channel byte the game does not contain: a representable-but-unreached
encoding, not a shipped behaviour.

### The structural rule you can read off the last instruction

- **A verb that returns a value ends `jmp VMResult_WriteInt32`.**
- **A verb that returns nothing ends `jmp <the native function>`** — or plain `ret`.

~~Two of the seven return; five do not.~~ **Three of the seven return; four do not** (2026-09-13: §3's and §9's tables were right and this sentence was not — `005101F0`, `00510230` and `00510260` all end `jmp 0x26b4e0`). **The tail target is the return type.**

## 3. The seven verbs

| verb | size | arity | native target | returns |
|---|---:|---:|---|---|
| `VM_SpawnEntry_GetRespawnCooldownTicks` `005101F0` | 54 B | 1 | `SpawnEntry_GetRespawnCooldownTicks` `002366E0` | **int** |
| `VM_Spawn_SelectPreviousMapEntry` `00510230` | 32 B | 0 | `Spawn_SelectPreviousMapEntry` `002354F0` | **int** |
| `VM_Spawn_SelectContinuousEntry` `00510260` | 32 B | 0 | `Spawn_SelectContinuousEntry` `00235360` | **int** |
| `VM_SpawnEntry_SetRangeRetireInhibitTag` `00510370` | 32 B | 1 | `SpawnEntry_SetRangeRetireInhibitTag` `002391C0` | none |
| `VM_Spawn_ApplySelectedUnit` `00510160` | 72 B | 1 | `Spawn_ApplyScriptSelectedUnit` `0023A3B0` | none |
| `VM_Spawn_BindEntryAndMarkCapTracked` `005103F0` | 67 B | **2** | `SpawnUnit_BindEntryAndMarkCapTracked` `00239840` | none |
| `VM_Spawn_SetEntryMapAndResetTransientEntries` `00510620` | 63 B | 1 | `SpawnUnit_SetEntryMapAndResetTransientEntries` `0023A2E0` | none |

### Two verbs do more than forward

**`VM_Spawn_ApplySelectedUnit` (`00510160`) checks its own work.**

```c
int unit = pop(stack);
Spawn_ApplyScriptSelectedUnit(target, unit);          /* 0023A3B0 */
if (ActorWork_HasAppliedUnitDefinition(target))       /* 00237650 */
    VMEventContext_InitializeActorOperation(event, target, -1);   /* 0037CF50 */
```

**It applies the unit, then asks whether a definition actually took**, and only then raises the actor
operation on the event context — with `r8d = -1`. **A script's spawn request that does not take is
silently not followed by the operation**, and the verb returns nothing either way, so **the script
cannot tell.**

**`VM_Spawn_SetEntryMapAndResetTransientEntries` (`00510620`) resolves a handle first.**

```c
int arg = pop(stack);
void *a = FUN_002640C0();                 /* no arguments — a global/current lookup */
void *b = FUN_002650B0(a, target, arg);
SpawnUnit_SetEntryMapAndResetTransientEntries(target, b);   /* 0023A2E0, tail */
```

The script's integer is **not** what reaches the native function: it is turned into a pointer by a
two-step lookup first. **The verb's argument is an id, not an address**, which is what one wants from
a script boundary and is worth stating because the native function's own signature does not say so.

## 4. Key addresses

| address | size | what |
|---|---:|---|
| `00267E10` | 78 B | `VMValueStack_PopInt32CoerceFloat32` — argument in |
| `0026B4E0` | 28 B | `VMResult_WriteInt32` — result out, 40-byte entries, tag `2` |
| `005101F0`, `00510230`, `00510260`, `00510370`, `00510160`, `005103F0`, `00510620` | 32–72 B | the seven verbs |
| `00237650` | 32 B | `ActorWork_HasAppliedUnitDefinition` |
| `0037CF50` | 102 B | `VMEventContext_InitializeActorOperation` |
| `002640C0`, `002650B0` | — | the handle resolution in `00510620` — **not read** *(answered: EF-3, 2026-09-11, §6; 2026-10-02, OPUS)* |
| `00354740`, `00511F20`, `005120B0`, `00512130` | 5 B each | thunks in the same backlog cluster — **disposition C**, forwarders only |

### Fields

| offset | on | meaning |
|---|---|---|
| `+0x00` | value stack | `int` depth |
| `+0x04 + i` | value stack | type tag byte for slot `i` |
| `+0x11` | result context | **signed** result-slot index |
| `+0xA8` | result context | pointer to the result array, **40-byte entries** |
| `+0x0C` | result entry | `int32` payload |
| `+0x15` | result entry | ~~type tag; `0` none, `1` armed,~~ phase and result type: `0` begin pending, `1` poll pending, **`2` = int32**, `3` = float32 *(corrected 2026-10-02, OPUS: `00262248`–`0026224F` branch on 0 / 1, `0026230B` writes 1 on a busy poll, the result writers 2 / 3, `00262382` resets 0)* |
| `+0x44 + i` | value stack | a second byte array; both pushes store **`6`** — meaning unknown |
| `+0x84 + i*4` | value stack | a third array; both pushes store **`0`** — meaning unknown |
| `+0x184 + i*4` | value stack | **the payload**, 4 bytes per slot (`00267E51`, `00267F8x`) |
| capacity | value stack | **63** — `cmp eax, 0x3f` / `jge` / `ret`; a 64th push is silently dropped |

## 5. Modding notes

- ~~**These seven are the whole spawn vocabulary of the script layer.** Anything else about spawning requires a native hook, not a script edit.~~ **False, corrected 2026-09-13.** **37 call ids** reach a `Spawn_Encounter_Lifecycle`-owned native by a direct `call`/`jmp` from their verb handler, touching **35 of the 52** functions that owner holds. Setting spawn distance, level, the entry struct, the despawn type, the position-attempt limit, and reading the death count, the elapsed time and the entry point are all **script-reachable already** — see §10.
- **Push arguments in the order the verb pops them backwards.** For the two-argument verb, the last
  value pushed becomes the *first* native argument after the context.
- **`VM_Spawn_ApplySelectedUnit` gives no feedback.** If the unit definition does not apply, the
  actor operation is skipped and the script continues as though it succeeded.
- **Hook the verb, not the native function**, if the intent is to change what scripts can do — ~~five~~ three *(corrected 2026-10-02, OPUS: `00510370+0x1B`, `0051042E`, `0051065A`; three others tail-jump `0026B4E0` and `00510160` ends in `ret` — "Three, three and one" below)* of
  the seven tail-call their native target, so a hook on the native also catches every non-script
  caller.
- **The result tag `2` is int32.** Writing a different tag into `+0x15` is how a verb would return
  another type, but no other tag is established here.

## 6. What is not known

- [x] ~~**What the other result type tags are.** Only `2` (int32) is proven; `0026B500` onward holds further code in the same family that was not read.~~ **`EF-1` ANSWERED 2026-09-13 (OPUS):** tag **`3` = float32**, from `VMResult_WriteFloat32` (`0026B4C0`, 28 B) — the same five instructions, `movss [slot+0x0C], xmm1` then `mov byte [slot+0x15], 3`. **The pointer in this question was wrong**: `0026B500` is a bitfield setter on a different record, and the family runs *downward* from `0026B4E0`, not upward. Across **every** function in the EXE that reaches a slot through the record idiom — all **six**, censused — the tag takes only `0`, `1`, `2`, `3`; see §10.
- [x] ~~**UQ-54.** **What the signed result-slot index at `+0x11` means when negative.** It is read with `movsx`
  and nothing bounds-checks it. `EF-2`.~~ **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): nothing in the shipped
  game. No channel producer can emit a negative value.** The record's one route-proven writer, `003DB754`,
  copies a request entry's channel. Every producer of that channel is now enumerated:
  every native call site of the insert's four wrappers, and every script route, including
  the three `sysreq` verbs no earlier census covered. None yields a negative channel. If one were ever stored, it
  would overwrite two of the record's own request entries. See
  [§ UQ-54 answered](#uq-54-answered--every-producer-of-a-request-channel-enumerated-fable-claude-opus-55-2026-09-25).
- [x] ~~**What `002640C0` and `002650B0` resolve** in `VM_Spawn_SetEntryMapAndResetTransientEntries` —
  the step that turns a script id into a pointer.~~ **`EF-3` ANSWERED 2026-09-11 (FABLE):** `002640C0`
  returns the current actor-manager slot block, the qword at `02099D70` (`002640C0`–`002640C7`);
  `002650B0(block, _, id)` treats the script's integer as a **region-tagged offset** — bits 24–26
  select a base, the low 24 bits are added to it (`002650B9`–`002650E5`, jump table `0026516C`-relative):
  region 0 → `[block + 0x48]` (`002650E8`), 1 → `[block + 0x40]` (`002650FC`), 2 → the pointer the
  block's own routine at `+0x98` returns (`00265110`–`00265124`), 3 → `[block + 0x58]` (the pointer
  block `02099DF0`, `0026512D`), 4 → `[block + 0x60]` (`02099FF0`, `00265141`), 5 → the block's first
  qword plus that object's own `+0x40` word (`00265155`–`00265163`), 6–7 → the bare offset
  (`0026516C`). The verb hands the resolved pointer to `0023A2E0` (`0051064A`–`0051065A`). Which
  region holds which authored table is [the actor-manager record](../../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md)'s rows `+0x40`–`+0x60`.
- [x] ~~**Why `VMEventContext_InitializeActorOperation` is passed `-1`**, and what operation that
  selects.~~ **`EF-4` ANSWERED 2026-09-11 (FABLE):** it selects nothing — `VM_Spawn_ApplySelectedUnit`
  is the initialiser's **only caller** on the call graph and always passes `-1` (`0051018E`), and the
  initialiser clamps every negative code to `-1` anyway (`0037CF5F`–`0037CF71`, `cmovs`) before
  storing it as the context's byte `+9` = `0xFF`. The rest of the context is fixed: `+0` the
  image-relative encoding of the unit pointer (`0020E620`, `0037CF74`–`0037CF79`), `+8` and `+0xA`
  zero, `+0xB` the result of `002DEBD0()`; then `002DEB90(1)`, `0016D6A0()`, and the unit's byte
  `+0x23` is cleared (`0037CFA2`). The call is made only when `00237650(unit)` is non-zero
  (`00510185`–`0051018C`).
- [x] ~~**UQ-55.** **How these seven are reached from a script** — which opcode or verb id dispatches to them. The
  bridge is read from the native side only. `EF-5`.~~ **ANSWERED — this box was never ticked after `EF-5`
  was answered on 2026-09-08** (closed 2026-09-25, FABLE, Claude Opus 5.5).
  - **The route.** The seven are the `begin`/`result` callbacks of the family-3 records `3001`
    `btlAtelSetUnit`, `3015` `btlAtelSetCallGroup`, `3016` `btlAtelSetTotalEntryNumber`, `304A`
    `btlAtelGetRespawnTime`, `304B` `btlAtelDecideEntryGroupByPreviousMap`, `305C`
    `btlAtelSetKeepWorkGroup` and `305F` `btlAtelDecideEntryGroupByContinuous`
    ([`scriptvm-verb-table.tsv`](../Verb-Dispatch/scriptvm-verb-table.tsv)).
  - **How a script names them.** A CALL-family opcode carries the packed id; `002621D0` splits it into
    family and command (`00262205`, `0026220C`) and indexes family 3's table `0x01F281B0`
    ([the dispatch ABI](../Verb-Dispatch/CONTRACT-verb-dispatch-abi.md) §2.2).
  - **What ships, added 2026-09-25**
    ([`members/spawn_verb_call_census.py`](members/spawn_verb_call_census.py) →
    [`members/spawn-verb-call-census.tsv`](members/spawn-verb-call-census.tsv)): 649,710 call sites in
    4,518 of the 10,036 script images.
    - The three getters (`304A`/`304B`/`305F`) are called only with `0x58 CALL`, which leaves the result
      on the value stack.
    - The four setters are called only with `0x5D CALLPOPA`, which pops it into the A register.
    - No site uses the actor-id forms `0x59`/`0x5E`, so every call acts on the current actor.
- [x] ~~The failure path of `VMValueStack_PopInt32CoerceFloat32` when the stack is empty; the body was
  read only as far as the tag dispatch.~~ `EF-6` **answered 2026-09-10**: returns `0` with no error
  call and no depth change (`00267E18`→`00267E3B`); the float pop is the one that reports
  (`00267DB8`→`00267DF2`). [The bridge contract](../CONTRACT-script-to-native-bridge.md) §10.

## 7. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The uniform 4-register verb signature | all seven bodies disassembled; register usage compared across them | 1 | PROVEN |
| Arguments arrive in reverse order | the two `call 0x267E10` sites in `005103F0` and the registers they land in | 1 | PROVEN |
| Result entries are 40 bytes, tag at `+0x15`, value at `+0x0C`, tag `2` = int32 | `lea r8,[rax+rax*4]` with `*8` scaling, and the two stores | 1 | PROVEN |
| The tail target encodes the return type | **three** tail-jump `VMResult_WriteInt32`, **three** tail-jump their native target, and **one** (`00510160`) plain `ret`s | 1 | PROVEN |
| `00510160` gates the actor operation on a post-check | `call 00237650` / `test eax,eax` / `je` | 1 | PROVEN |
| `00510620`'s argument is an id, not a pointer | the `002640C0`/`002650B0` pair between the pop and the native call | 1 | PROVEN |
| What any other result tag means | **not established** *(answered: EF-1 — `3` is float32, `0026B4C0`; 2026-10-02, OPUS)* | — | UNKNOWN |
| Which script opcode reaches these verbs | **not traced** *(answered: UQ-55 / EF-5, §6; 2026-10-02, OPUS)* | — | UNKNOWN |

## 8. Related

- [`../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md)
  — the native side of the spawn lifecycle these verbs drive, including
  `SpawnEntry_GetRespawnCooldownTicks`.
- [`../../_index/RESEARCH-IMPORT-BACKLOG.md`](../../_index/RESEARCH-IMPORT-BACKLOG.md) — the import.

## 9. `EF-5` answered — the seven script commands, and a corroboration

**`EF-5` should never have been filed.** It asked which script opcode reaches these verbs, and
[`../Verb-Dispatch/scriptvm-verb-table.tsv`](../Verb-Dispatch/scriptvm-verb-table.tsv) already held
the answer in full. `check_already_answered.py` reported *"no existing coverage"* because of two bugs
in the checker itself, both now fixed — see the audit log entry for 2026-09-08.

| call id | script command | native verb | arity | returns |
|---|---|---|---:|---|
| `3001` | **`btlAtelSetUnit`** | `VM_Spawn_ApplySelectedUnit` | 1 | — |
| `3015` | **`btlAtelSetCallGroup`** | `VM_SpawnEntry_SetRangeRetireInhibitTag` | 1 | — |
| `3016` | **`btlAtelSetTotalEntryNumber`** | `VM_Spawn_SetEntryMapAndResetTransientEntries` | 1 | — |
| `304A` | **`btlAtelGetRespawnTime`** | `VM_SpawnEntry_GetRespawnCooldownTicks` | 1 | int |
| `304B` | **`btlAtelDecideEntryGroupByPreviousMap`** | `VM_Spawn_SelectPreviousMapEntry` | 0 | int |
| `305C` | **`btlAtelSetKeepWorkGroup`** | `VM_Spawn_BindEntryAndMarkCapTracked` | 2 | — |
| `305F` | **`btlAtelDecideEntryGroupByContinuous`** | `VM_Spawn_SelectContinuousEntry` | 0 | int |

**These are the names a zone script actually writes.** All are family `3` (`btlAtel*`), and the
command byte is the low two hex digits of the call id.

### The table corroborates this document independently

The verb table was built by a **prior census**, this document from **disassembly**, and they were
compared only after both existed:

| | this document | `scriptvm-verb-table.tsv` |
|---|---|---|
| arity, in table order | 1, 1, 1, 1, 0, 2, 0 | `pops_int` 1, 1, 1, 1, 0, 2, 0 |
| returns a value | no, no, no, **yes**, **yes**, no, **yes** | `result_writes` 0, 0, 0, **1**, **1**, 0, **1** |

**Seven verbs, two independent derivations, no disagreement** — including the "tail target is the
return type" rule, which the census reached by a different route.

The table also carries `param_types`: **`0x10`** for the single-int verbs and **`0x12,0x12`** for the
two-argument one. So at least two parameter type codes exist. **These are parameter tags, not the
result tags of `EF-1`**, and the two encodings are not shown to be the same space.

### ⚠ Three places where the script name and the native name disagree

| script command | native name | the tension |
|---|---|---|
| `btlAtelGetRespawnTime` | `…GetRespawnCooldownTicks` | script says **Time**, the imported native name says **Ticks** — and `00235FB0`, the neighbouring reader, was proved to return **seconds**. Suggestive for `EE-1`, **not decisive**: the verb's name is not evidence about the field's unit. *`EE-1` answered 2026-09-13 from the scripts: all 1,765 calls compare it against `btlAtelGetElapseTime` — seconds; the imported name is wrong.* |
| `btlAtelSetTotalEntryNumber` | `…SetEntryMapAndResetTransientEntries` | "TotalEntryNumber" reads as a **count**, but §3 proved the argument is an **id turned into a pointer** by `002640C0`/`002650B0` before the native call. |
| `btlAtelSetCallGroup` | `…SetRangeRetireInhibitTag` | substantially different descriptions of one operation. |

> **Neither name is authority.** The script command name is what the authors typed in a script; the
> native name is a prior session's label. **The body is the source**, and where the two names
> disagree the disagreement is recorded rather than resolved by preferring one.

## 10. Falsification pass 1 — 2026-09-13 (OPUS)

Every size this page states is **exact** — all eleven, checked against the function graph — and
so is every claim about register use, argument order and the two verbs that do more than forward:

| claim | measured |
|---|---|
| the uniform 4-register signature, and *which* registers each verb leaves alone | holds for all seven: only the three returning verbs touch `rcx`, only `00510160` touches `r8`, and only the five with arity ≥ 1 touch `r9` |
| arity 1, 0, 0, 1, 1, **2**, 1 in §3's order | one `call 0x267E10` each, none, none, one, one, **two**, one |
| arguments arrive in reverse | `00510408` → `ebx` → **`edx` (arg 2)**; `00510412` → **`r8d` (arg 3)** |
| `00510160` gates the operation on a post-check, and passes `-1` | `call 0x237650` / `test eax,eax` / `je`, then `or r8d, 0xffffffff` |
| `00510620` resolves the id before the native call | `call 0x2640C0` / `mov rcx,rax` / `mov r8d,ebx` / `call 0x2650B0` / `mov rdx,rax` / `jmp 0x23A2E0` |
| "no reader distinguishes `2` from `3`, every test is against `0`" | confirmed — the only reads of `+0x15` anywhere are **four** `cmp byte ptr [rsi + 0x15], 0`, never against `2` or `3` |

Three things were wrong, and one of them matters to a modder.

### ⚠ The spawn vocabulary is 37 verbs, not seven

§1 and §5 told a modder that **anything not on this list needs a native hook**. Tested by
disassembling **every** verb handler in
[`../Verb-Dispatch/scriptvm-verb-table.tsv`](../Verb-Dispatch/scriptvm-verb-table.tsv) — 2,276
handler bodies over 1,960 rows — and collecting direct `call`/`jmp` targets owned by
`Spawn_Encounter_Lifecycle`:

| | |
|---|---:|
| call ids reaching the spawn subsystem directly | **37** |
| distinct handlers | 35 |
| distinct spawn natives reached, of the 52 that owner holds | **35** |
| **the seven this page documents, recovered by the same instrument** | **7 / 7** |
| ids beyond those seven | **30** |

The recovery of all seven is the **control**: the instrument that found the extra thirty is the one
that reproduces the known set, so the thirty are not an artefact of it. Four of the thirty are not
even `btlAtel*`: **`03B8 bosskillall`**, **`0478 showenemy`**, **`0479 hideenemy`**,
**`04DE killgroup`**. Among the rest a script can already set the spawn distance (`300B`), the level
(`3031`), the entry struct (`3018`), the despawn type (`3019`) and the position-attempt limit
(`3038`), and read the death limit and count (`3028`, `3029`), the elapsed time (`3036`) and the
entry point (`3035`).

> **This is the correction with consequences.** A modder following §5 would write a native hook for
> work the script layer already exposes.

**Scope:** this counts a *direct* `call`/`jmp` from a handler body. A verb reaching spawn through one
more hop is not counted, so **37 is a floor, not a ceiling** — the claim corrected here is a
negative one, and only the negative one is settled.

### The return count contradicted the page's own tables

§2 said "two of the seven return; five do not"; §7 said "five tail-jump their native target, two
tail-jump `VMResult_WriteInt32`". The tails are:

```
005101F0 jmp 0x26b4e0   00510230 jmp 0x26b4e0   00510260 jmp 0x26b4e0     <- three return
00510370 jmp 0x2391c0   005103F0 jmp 0x239840   00510620 jmp 0x23a2e0     <- three forward
00510160 ret                                                              <- one, the gated verb
```

**Three, three and one.** §3's `returns` column and §9's `result_writes` corroboration both already
said three; only the prose said two. Corrected in both places — the rule itself ("the tail target is
the return type") survives untouched.

### `EF-1`: the family runs downward, and the tag set is `0, 1, 2, 3`

`0026B4C0` is **`VMResult_WriteFloat32`**, 28 B, immediately *before* the int writer and structurally
identical — `movss dword ptr [rax + rdx*8 + 0xc], xmm1` then `mov byte ptr [rax + rdx*8 + 0x15], 3`.
`EF-1` sent a reader to `0026B500`, which is a bitfield setter on an unrelated record.

A census of the whole EXE for the idiom — `movsx r, byte ptr [rec + 0x11]` followed within eight
instructions by `mov r, qword ptr [rec + 0xa8]` — returned **six functions**, and they were
published as the complete set of writers. ~~exactly six~~ **Corrected 2026-09-14 (OPUS), on
`AUDITSPEC-REQ-OPUS-EF2-SEVENTH-READER`: the census is SEVEN, and the seventh is a writer — see
[the seventh](#the-seventh-site-and-what-it-changes) below. The word *complete* is withdrawn.**
The six as first published:

| | |
|---|---|
| `0025DF00` `WorldActor_UpdateRuntimeAndScriptExecutionState` | the field runtime pass's resolver |
| `0025E4C0` `WorldActorScriptVM_InterpretBytecode` | the interpreter — the **reader** of `+0x0C` |
| `002651A0` (26 B) | a **third** writer: stores tag `2`, then **returns** `slot.+0x0C` |
| `0026B4C0` `VMResult_WriteFloat32` | tag `3` |
| `0026B4E0` `VMResult_WriteInt32` | tag `2` |
| `003DBDC0` `ActorResource_StartEntryScriptExecution` | sets the pc and `+0x14 = 1` |

Across all six, `+0x15` takes **`0`, `1`, `2`, `3`** and nothing else. ~~**`1` is written exactly once~~ *(corrected 2026-10-02, OPUS: `1` is also written as a byte, by the lifecycle: `0026230B mov byte ptr [rdi + 0x15], 1`)*
~~in the EXE, and not as a byte:**~~ **The interpreter's own write is a word:**

```asm
00261B97  mov word ptr [rsi + 0x14], 0x107     ; +0x14 = 7  AND  +0x15 = 1, one store
```

So the legend "`1` armed" is right, but it is reachable ~~only~~ through a **fused 16-bit store that
pairs it with wait kind 7** — ~~a byte-level search for `mov byte ptr […+0x15], 1` finds nothing and~~ *(corrected 2026-10-02, OPUS: and through `0026230B`'s byte store)*
~~would conclude the value is unused.~~ The interpreter also writes `+0x14` = `3` (`00261596`) and `5`
(`00261D24`), which with `1` and `7` puts four of the eight kinds in use.

### The 40-byte entry, mapped from all six users

| offset | width | evidence |
|---|---|---|
| `+0x00` | qword | the pc — `mov qword ptr [rsi], r14` (×4), `mov qword ptr [rdi], rax` (`003DBE09`) |
| `+0x0C` | dword | the payload; written by both writers, **read by the interpreter** (`cmp eax, dword ptr [rsi + 0xc]` ×5) |
| `+0x10` | dword | `00261AF6` |
| `+0x14` | byte | **wait kind**; `1`, `3`, `5`, `7` written |
| `+0x15` | byte | **result tag**; `0`, `1`, `2`, `3` |
| `+0x16` | byte | `0025DFD3`–`0025E127` |
| `+0x18` | dword | also taken by address — `lea rdx, [rsi + 0x18]` ×5, so a sub-object starts here |
| `+0x1C`, `+0x22` | dword, word | written together ×3 |
| `+0x20` | word | `0026158E` |
| `+0x26`, `+0x27` | byte, byte | `+0x26` read ×5, `+0x27` written `0`/`1` |

### The value stack is four parallel arrays, and both of its ends fail silently

> **⚠ Retraction, same day.** This heading and the failure-mode table below it were published as
> findings of this pass. **They were not new.**
> [`CONTRACT-script-to-native-bridge.md`](../CONTRACT-script-to-native-bridge.md) already gives
> *"`VmValueStack`, size `0x284` — four parallel arrays of 64, indexed by slot"*, `+0x184` as
> **THE VALUE**, *"63 usable slots, not 64"* with the `cmp eax, 0x3F` guard, and *"both pushes write
> literal `0` to `+0x84`"*; and the mirror-image failure modes are the headline of
> `OPUS-PASS-SCRIPT-BRIDGE`, **2026-09-12 — my own pass**. What follows is a re-derivation, and is
> kept because §9's other findings lean on the layout. The genuinely new work of this pass is the
> 37-verb spawn vocabulary, the three/three/one return count, `EF-1`, and the six-function idiom
> census — not this.

§2 documents the depth and the tag array and never says where the value is. Both pushes give the
whole layout:

```
+0x000  int32  depth
+0x004  u8     tag  [64]      1 = int32, 2 = float32
+0x044  u8     ?    [64]      both pushes store 6
+0x084  u32    ?    [64]      both pushes store 0
+0x184  u32    value[64]      the payload            -> the struct ends at 0x284
```

**It is not an array of tagged slots** — a reconstruction that packs tag and value together will
have the right behaviour and the wrong memory image.

**Capacity is 63.** `VMValueStack_PushInt32` (`00267F90`) and `PushFloat32Bits` (`00267F60`) both
open `cmp eax, 0x3f` / `jge` / `ret`: at depth 63 the push **stores nothing, does not increment, and
does not report.** A script that pushes a 64th argument loses it silently — the mirror of the
underflow `EF-6` already recorded.

And the two pops report on **exactly opposite** conditions:

| | `00267E10` pop→int | `00267DB0` pop→float |
|---|---|---|
| depth ≤ 0 | returns `0`, **silent** | **reports** `008620C0(1)`, returns `0.0` |
| unknown tag | **reports** `008620C0(1)`, returns `0` | returns `0.0`, **silent** |

`EF-6` recorded that "the float pop is the one that reports". That is true of *underflow only*; the
int pop reports too, on the other condition. **Every one of the four failure modes is silent to the
script**, which is the contract statement a reimplementation needs.

*(The graph labels `00267DB0` `VMValueStack_PopNumericDiscard`; its body returns a float32 in `xmm0`
and coerces tag 1 with `cvtdq2ps`, so it is the mirror of `00267E10`, not a discard. Recorded as an
observation about the label — names are not authority here.)*

### One cross-page disagreement, settled in this page's favour

This page writes the slot address as `a->slotsA8 + (signed char)a->currentWaitSlot` — a real
dereference. [The script-binding page](../Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md)
wrote the same access as `record.+0xA8 + slot * 0x28`, which would put the array *inside* the record.
`0026B4E9 mov rax, qword ptr [rcx + 0xa8]` is a load. **This page was right**; the other was corrected
earlier the same day.

**Not claimed:** `EF-2` (a negative slot index) is untouched *(answered: UQ-54, 2026-09-25 — no producer emits a negative channel, §6; 2026-10-02, OPUS)* — nothing bounds-checks it and nothing
here shows what one would do. The meaning of `+0x44` and `+0x84` on the stack, and of slot `+0x10`, *(answered: the bridge contract's slot layout names the slot fields; `+0x44` is 6 or `PUSHP`'s width nibble, `00268185`; 2026-10-02, OPUS)*
`+0x16`, `+0x18`, `+0x1C`–`+0x27`, is **not** established — only that they are written and how wide.
The other four wait kinds remain unnamed. Nothing here was executed or observed live; every statement
is static.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Movement — SERVICE and CLIENT.** The per-actor update `0025DF00` runs `Movement_UpdateActorFrame`,
  `Movement_SetRequestedSpeed` and three helpers. `WorldActorScriptVM_InterpretBytecode` is run from that same update.
  The 7-byte `002DEB90` is read by a 475-byte movement body. `VMValueStack_PushFloat32Bits` (`00267F60`) is also called by four Movement-filed bodies (88–233 B), which push floats onto the script stack. Which verbs they serve is not read.
- **Presentation — SERVICE.** `0025DF00` calls three small Presentation helpers (42–84 B).

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE.** `SpawnEntry_GetElapsedTicksSinceLastDeath` reads `GameClock_GetRawTickCounter` (7 bytes), and `WorldActor_UpdateRuntimeAndScriptExecutionState` calls two small core helpers (27 and 61 bytes).
- **Audio — SERVICE.** The spawn-verb body `0023FBE0` calls `00249C60`, the gated audio accessor
  (`dword[02091098]` non-zero test at `00249C64`, lazy init through `003A1180`) — the verb emits audio
  alongside the spawn. (edge: `edges.tsv`)
- **UI — SERVICE.** The same verb `0023FBE0` calls `0023ED80` and `00291D80` — the latter bounds-checks
  `dword[01E0C484]` and tail-jumps `0028FD00`, an indexed UI census read (`00291D80`–`00291D87`).
  (edges: `edges.tsv`, two of them)
- **CombatFormula and Rewards_Progression_Economy — MECHANICAL.** `003A1180`, the lazy-init helper the
  gated audio accessor `00249C60` reaches at `00249C6D`, is a shared provider also called from the
  Rewards level-up recompute (`BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`, recorded in the
  registry by address) and from a CombatFormula applier whose edge is dead — its gate at result
  `+0x2C` bit 0 is cleared by both transition builders before it can run. (edges: `edges.tsv`,
  two of them; the CombatFormula side rests on a dead edge)

## `EF-2` — six readers, all signed, and a third slot function the page does not name (OPUS, 2026-09-14)

`EF-2` asks what a negative result-slot index means, noting that `VMResult_WriteInt32` reads the slot
at `+0x11` with `movsx` and nothing bounds-checks it. FABLE narrowed the producer side on
2026-09-13. **The reader side is measurable, and it says the signedness is the field's TYPE rather
than one function's accident.**

Read from the shipping image at the authority hash `73461D08…9721F8`.

### The write shape, exactly

```
0026B4E0  movsx rax, byte  [rcx + 0x11]        ; the slot index - SIGNED
0026B4E5  lea   r8,  [rax + rax*4]             ; x5
0026B4E9  mov   rax, qword [rcx + 0xA8]        ; the slot array
0026B4F0  mov   byte  [rax + r8*8 + 0x15], 2   ; type tag  (x8 -> stride 40)
0026B4F6  mov   dword [rax + r8*8 + 0x0C], edx ; the value
```

**Slot stride 40, value at `+0x0C`, type tag at `+0x15`.** `VMResult_WriteFloat32` is byte-for-byte
the same shape with tag **3** and a `movss`.

### Every reader of `+0x11` scales it by 40, and every one is signed

Swept over every listed body for a `+0x11` byte load followed by an `×5` scale:

| | bytes | load | what it does with the slot |
|---|---:|---|---|
| `0025B400` `WorldActorScriptVM_ServiceRequestWaitState` | 108 | `movsx` | |
| `0025DF00` `WorldActor_UpdateRuntimeAndScriptExecutionState` | 1,228 | `movsx` | |
| `0025E4C0` `WorldActorScriptVM_InterpretBytecode` | 14,646 | `movsx` | |
| `002651A0` **(unnamed)** | 26 | `movsx` | **tag 2, then READS `+0x0C` into `eax`** |
| `0026B4C0` `VMResult_WriteFloat32` | 28 | `movsx` | tag 3, writes `xmm1` |
| `0026B4E0` `VMResult_WriteInt32` | 28 | `movsx` | tag 2, writes `edx` |

> **Seven readers. Seven `movsx`. Zero `movzx`.** *(Corrected from six, 2026-09-14 (OPUS) — the
> seventh is `003DBDC0` below. The count moved; the conclusion did not, and it got stronger.)*

That is not one function being careless. **The field's declared type is a plain `char`** - signed on
this toolchain - and every site inherits it. A field intended as an unsigned index would have been
`movzx` somewhere across seven independent sites, and it is not.

### The seventh site, and what it changes

**`003DBDC0` `ActorResource_StartEntryScriptExecution`** carries the fingerprint and was missed:

```
003DBDD4  movsx rax, byte [rcx + 0x11]     ; the signed index, seventh site
003DBDE3  lea   r8,  [rax + rax*4]         ; x5
003DBDE7  mov   rax, qword [rcx + 0xA8]    ; the slot array
003DBDEE  lea   rdi, [rax + r8*8]          ; x8 -> stride 0x28, as everywhere else
003DBE09  mov   qword [rdi], rax           ; WRITES +0x00
003DBE0C  mov   byte  [rdi + 0x14], 1      ; WRITES +0x14
```

Three things follow, and only the first is what the request asked about.

1. **It is a writer, and the six were published as “the complete set of writers”.** That word is
   withdrawn above. Nothing between the load and the `lea` bounds the index, so the page's
   *“nothing in any of the six sites bounds it”* holds at seven — the unbounded-signed-index
   finding is widened, not weakened.
2. **It is not a fourth member of the slot family.** The three named slot functions write the
   value/tag pair at `+0x0C` / `+0x15`; this one writes the qword at `+0x00` and the state byte at
   `+0x14` — the same 40-byte record, different fields. *“Three slot functions”* stands as a claim
   about that pair. What is now known is that the record has a second field pair with its own
   writer, and `0025B400` reads `+0x14` (`cmp byte [rax + rdx*8 + 0x14], 4`) rather than the tag.
3. **The read/write split on this page is wrong in the other direction too.** A recount that
   follows the computed slot register rather than any store in the neighbourhood gives **twelve
   sites in seven functions: five writers and two pure readers**. `WorldActorScriptVM_InterpretBytecode`
   holds six of the twelve sites and **every one of them is a load** — the interpreter reads this
   array six times and writes it never, which the single-row table above cannot show.

*Why the first census missed it:* the idiom test keyed on the `+0xA8` load following the `movsx`
closely. Here two register moves and a `movzx` sit between them, and the `lea` that does the ×5
comes third rather than first. A window measured in instructions is a proxy for a dataflow question,
and this is the shape where the proxy fails. Recounted by binding the destination register, killing
it on redefinition and refusing to walk past the owning function's end — the same instrument the
`FE-1` correction of the same day was built on, and for the same reason.

### And there is a third slot function the page does not name

`002651A0` is **not a writer**: it stamps tag `2` and then **reads the value back** out of `+0x0C`.
So the slot family is write-int32, write-float32, and claim-as-int32-and-read - three functions
sharing one unbounded signed index, not two.

### What a negative index does, concretely

A slot index `N` addresses `base + 40N`. For `N = -1` the two stores land at **`base - 0x1C`** (the
value) and **`base - 0x13`** (the tag) - twenty-eight and nineteen bytes *before* the array. Nothing
in any of the six sites bounds it.

### Not claimed

Whether a negative value ever reaches `+0x11` - FABLE's narrowing found one producer and it cannot
produce one. This section adds that **if one ever did, three functions would act on it**, and that
the signedness is deliberate typing rather than a slip. What occupies `base - 0x1C` is not read here.

*(Read by OPUS 2026-09-14. `EF-2` stays open on the producer side *(answered: UQ-54, 2026-09-25, §6; 2026-10-02, OPUS)* and is narrowed on the reader
side.)*

## UQ-54 answered — every producer of a request channel enumerated (FABLE, Claude Opus 5.5, 2026-09-25)

**Answer.** In the shipped game a negative `+0x11` has no meaning, because nothing produces one. The
actor record's one route-proven writer of `+0x11` is `003DB754` in `ActorResource_SelectPendingEntryForExecution`,
and it copies byte `+2` of a request entry: the entry's **channel**. A channel reaches that byte
only through `ActorResource_InsertEntryFromDescriptor` (`003DB7A0`), which reads it with `movsx`
from descriptor `+2` (`003DB7A7`) and clamps it **from above only** (`003DB7C1`–`003DB7C5`). This
section enumerates **every producer of that descriptor byte**. None can make it negative. *Static,
from the shipping bytes and the full shipped script corpus.*

**The insert has two arms, and only one of them feeds the selector.** When descriptor `+1` is `4`,
the entry is linked onto the single list at record `+0x61` (`003DB894`–`003DB980`). The channel is
stored (`003DB906`) but never used as an index. Every other descriptor takes the channel arm
(`003DB995`–`003DBAA2`), which indexes the heads `+0x8C[ch]`, the tails `+0x94[ch]` and the
busy mask word `+6`. The selector walks only those tails.

**Every route into the insert.** `003DB7A0` has one caller, `ActorResource_AllocateAndSubmitEntry`
(`003DBCF0`, `003DBD5F`). That has seven call sites in six functions (raw E8/E9 index plus `jcc` sweep).

| route | channel source | values |
|---|---|---|
| `ScriptVM_SubmitActorRuntimeRequest` → `003DB790` / `003DBAE0` | the `REQ`-family descriptor (`002689B1`) | `0`–`7`, authored immediates (SWE2-DATA census above) |
| `003DBDC0`, `003DC0D0` | the originating entry's `+3`, under descriptor word `0x402` | `+0x61` arm: **not an index** |
| `ActorResource_SubmitRequestDescriptor` `003DBB60`, 23 sites | `edx` at each site | 20 native sites: immediates or record-derived, together `0`–`7` (below). Three carry script values: `00268BDB` (the `REQALL`/`REQIALL` operand), and `00269B71` / `00269C0D` (the `sysreq` verbs) |
| thunk `003DBBE0` → `003DBBF0`, 4 sites | `r8d` | `00268D10`: `7`; `00268EA0`: `4`/`6` and `5`/`3`; `00268B10`: the `REQALL`/`REQIALL` operand |

**The record-derived native channels are all bounded.**
- `00266C50` (`00266CBB`) and `ActorStorage_InitializeRecord` (`00266952`) pass `slotCountA8 − 1`.
  That count has a single writer, which stores `8` or `6`, so the channel is `7` or `5`.
  `00266926` passes `r15 − 1`, where `r15` is the same `8`/`6` from the kind table
  (`00266567`, `00266596`).
- The `ebp` channels in `0025BAD0` and `00269640`, and the `r10d` channel in `0025C230`, are loaded
  only from immediates: `4`/`6`, `0`/`1`, and `4`. Every write to the register in the body was
  checked, not just the last one before the call.
- The `r9 + k` channels (`0025B3BF`, `0025B727`, `0025D2DC`, `002699A7`) follow an `xor r9d, r9d`,
  and no jump lands between the zeroing and the call.
- **Two sites are also entered by jumps that skip the last `edx` write**, found by checking every
  branch that lands between that write and the call:
  - `0025C7E7` also receives `2` (`0025C770`).
  - `0025D39B` receives `4` on every path; on the skipping path the value comes from `0025D211`,
    `lea edx, [r13 + 5]` with `r13 = −1`.

**The script routes, three of them.**
- `REQ`/`REQEW`/`REQSW`: 326,204 authored immediates, `0`–`7` (SWE2-DATA, above).
- `REQALL`/`REQIALL`: pop the channel in `00268A80` and hand it to `00268B10`, whose `[rsp+0x80]`
  is that argument's home slot. Authored immediates `0`–`7` / `1`–`5`
  ([the list-wait census](../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md)).
- **Script verbs, which no earlier census covered.** `sysreq` (`0x00AA`, `0034E5C0`) and `sysreqf`
  (`0x0228`, `0034EC80`) pop class, ordinal, then channel, and call `00269A90`. That bounds the class
  (`< 0x12`) and the ordinal (`0 ≤ ordinal < count`, `00269ABB`) but **not the channel**, which
  `00269BA0` passes on as `edx`. `sysreqall` (`0x00AB`, `0034F380`) pops class, then channel, into
  `00269AD0`. In all three the channel is the **first-pushed argument**.
  [`members/sysreq_channel_census.py`](members/sysreq_channel_census.py) →
  [`members/sysreq-channel-census.tsv`](members/sysreq-channel-census.tsv), over all 10,036
  `section_000` images:
  - **`sysreq`: 675 sites, all resolved.** 621 pass an immediate `1`–`7`.
  - `sysreqall` and `sysreqf`: **no shipped site**.
  - **The other 54 pass a variable.** All are in `mnt_d01` (the same six sites in each of nine
    language copies), and each reads its own entry's `local` byte:
    - Entries 27–32 each declare two `local` bytes, `(131, 132)` … `(141, 142)`, and use no others.
    - The channel variable is the offset-1 byte (descriptor `0x12000001`, class 2 `local`).
    - Its only stores are `0` or `file` variable 72.
    - Var 72 gets `0` or var 73; var 73 gets `0` or var 74; var 74 gets immediates `0`–`6`.
    - That is 84 stores per copy, identical in all nine copies, so the channel is in **`0`–`6`**.

**What a negative channel, or a negative `+0x11`, would do.** This is recorded because the
encoding is representable.
- On the channel arm, `ch = −k` indexes `+0x8C − k` and `+0x94 − k`. For `k ≤ 4` that is the count
  bytes `+0x88`–`+0x8B`; for any `k ≤ 8` it is the head array itself. So the entry corrupts the
  record's counts or heads before any selection. This is §1's corruption route.
- A negative `+0x11` makes the readers address `slotsA8 + 40N` (`0025DFB6 movsx`, `0025DFBB`–`0025DFC6`).
  On this record `slotsA8` begins exactly where the request-entry array `slotsA0` ends (`+0x4D8` +
  10 × `0x14` = `+0x5A0`, or + 8 × `0x14` = `+0x578`;
  [the record page](../../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md)).
- So OPUS's `base − 0x1C` (value) and `base − 0x13` (tag), for `N = −1`, are **the `+0x0C` dword of the
  second-last request entry** and **the `+0x01` link byte of the last one**. A negative slot write
  would therefore damage the request list the channel came from.

**Bound, stated so it is not over-read.** This closes the producer side **through `003DB754`**, the
writer the route-proven access census attributes to the actor record. `EF-2`'s separate residue is
**35 register-sourced stores at displacement `0x11` on untyped bases**, and it is not re-examined
here. If one of them were shown to target an actor storage record, that would be a new writer, not
a new channel.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

`00268D10` is cited above for one fact only: the constant channel `7` it passes at `00268DC4`
to `003DBBE0`, the thunk into `003DBBF0`. After that submit, the same body calls into two other layers.
Neither call is read here, and nothing in the UQ-54 answer rests on either.

**WorldAreaField — CLIENT.** `00268D10` calls `00377700` at `00268E11`, after the submit and
the selector run. This section does not say what that call does. It cites `00268D10` only as a
producer of a request channel, and the call cannot change the channel that was already passed.
*This paragraph covers the `00268D10` edge only.* The page's other WorldAreaField edges, from
`00394130` in SWE2-FRONTIER's `00511F20`/`00512130` subtree section below, are **not** dispositioned here. The neighbour gate
credits the layer as a whole, so a lower count after this publish does not mean they were answered.

**CombatAction — CLIENT.** `00268D10` calls `00317E60` at `00268E35`, also after the
submit. The same holds: this section makes no claim about the call.
- **Resource — CLIENT (1 edge).** 1 inbound (Resource bodies `0032E3B0` call page-cited `008620C0`). Substantive edges include `008620C0` is called by `0032E3B0`.
## The `005120B0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`005120B0` (5 B) — `jmp 003945E0` thunk. `003945E0` (22 B) is a flag-gated
trigger: when `byte[01EFAC11] != 2` it forwards `cl = 1`, `edx = 0xFF` to
`002406F0` (`003945E0`/`003945F0`); equal returns immediately
(`003945F5`).

`002406F0` (93 B) — the deferred-message enqueue: when `qword[0208E6D8]`
is null it packs `{dword 0, byte cl, word dx}` into a 12-byte stack
record (`0024071B`/`0024070E`/`00240716`) and submits it through
`00244F50(ecx = 0x4D8, rdx = &0023FBE0, r8 = &record)` (`00240725`–
`00240736`); a live `0208E6D8` skips the submit entirely (`00240723`).

| member | role | interior |
| --- | --- | --- |
| `003945E0` (22 B) | flag gate — `byte[01EFAC11] != 2` → `002406F0(1, 0xFF)` | [`003945E0`](../../_index/ADDRESS-INDEX.md) |
| `002406F0` (93 B) | enqueue — `0208E6D8` null → `00244F50(0x4D8, &0023FBE0, &{0, cl, dx})` | [`00240736`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00244F50`, `00808C40`. The
`0023FBE0` descriptor and the `0x4D8` selector are the shared submit
contract; `01EFAC11` is the sibling-paired flag byte (`01EFAC10` is the
`00394600` twin's gate).

## The `00511F20`/`00512130` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

| root | member (target) | role | interior |
| --- | --- | --- | --- |
| `00511F20` | `00394600` | `byte[01EFAC10] == 2` gate -> `00393EA0` op `ecx = 0x108` | [`00394600`](../../_index/ADDRESS-INDEX.md) |
| `00512130` | `00394640` | `qword[02AEE4D0] == 0` gate -> `00394130` op `ecx = 0xF0` | [`00394640`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00393EA0`, `00394130`.


## Interior citation — frontier hub `008620C0` (2026-09-18, SWE2-EC7)

`008620C0` — 14 B, 13 callers; the reporting arm `008620C0(1)` the float-pop row above
invokes. Interior verified: `lea rdx, [01CCF998]` loads an `"FFXI…"` literal
([`008620C0`](../../_index/ADDRESS-INDEX.md)), `ecx` is zeroed, and the tail is
`jmp 0016D6A0` at [`008620C9`](../../_index/ADDRESS-INDEX.md) — the `ret 0` folded leaf. The
report is a no-op in the shipped image: the string is staged and dropped.

## SWE2-EC7-41 update (2026-09-19) - `00393EA0`

`00393EA0` (326 B) is the shared callee outside the census the page names - `01EFAC10`/`0208EA28`, `003BB430`/`003BB420`/`0036FD70`/`00244F00` each paired. Interior anchor `00393EE3` (a `003BB430` call).

`0023F240` (1418 B) is the input-driven body `0023FBE0` runs: `02F97368`/`02F9736A`/`02F9736C` filtered words and `byte[rdi+0xEC]` load the press state, `001E0A10` resamples the rate, then `002D3BA0` x2 list dispatches with `0023F190` x6, `0023F7D0` x4, `002D47C0` x4, `002D2D40` x2 and `001E0F20` - the spawn verb's filtered-input driver.

Interior anchor `0023F3C8` (function `0023F240`).

`0023F7D0` (223 B) is the flag-bracketed dispatch `0023F240` runs on the `+0xD8` spawn record: `+0xE4` gains bit `2`, `002D45C0(r14, 0)` opens the arm, `+0xE4` is rebuilt as `([+0xE4] & ~bit22) | ((+0xE0 & 0x1000000) >> 2 | bit25)`, `002D3BA0` runs the caller's `esi`/`edi`/`ebx` triple, `0023F190` post-processes `rbp`, then bits `0xC00000` clear, `002D45C0(r14, 1)` closes, bit `2` clears - returns `ebx`, defaulting to `002D3BA0`'s result when the stack arg was `0`

Interior anchor `0023F81F` (function `0023F7D0`).

`0023F190` (163 B) is the spawn-cost check `0023F240`/`0023F7D0` run on the `+0xD8` record: `r8d = (s16[+0xF2] + s16[+0xF4]) * u8[+0xEC] + s8[+0xEE] + s8[+0xED]` indexes the `01E0BF60` pointer table by `u8[+0xC0]` (< 0x2D), bounds-checks against the row's `+2` u16, then walks `row + (r8d + (r8d+1)*2) * 2` to a byte < 0x2D whose own table row must not carry first-byte `0x0B`/`0x0C` - returns `result != 0x12`

Interior anchor `0023F1C8` (function `0023F190`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-script-to-native-calling-convention-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0034E5C0` | 103 B | reads dword `+0x28` of the pointer the 8-byte getter of qword `02099D70` returns, calls `00267E10(r9)` three times, and returns a 52-byte helper's result for (that dword, second result, third result, first result, 0) with 0 as the fifth (stack) argument | `0034E5DF`, `0034E5E2`, `0034E5F6`, `0034E5FE`, `0034E60D` |
| `0034EC80` | 103 B | reads dword `+0x28` of the pointer the 8-byte getter of qword `02099D70` returns, calls `00267E10(r9)` three times, and returns a 52-byte helper's result for (that dword, second result, third result, first result, 1) with 1 as the fifth (stack) argument | `0034EC9F`, `0034ECA2`, `0034ECB6`, `0034ECBE`, `0034ECCD` |
| `0034F380` | 61 B | calls `00267E10(r9)` twice, then the 8-byte getter of qword `02099D70`, and tail-jumps a 200-byte helper with (dword `+0x28` of that pointer, second `00267E10` result, first `00267E10` result) | `0034F390`, `0034F39A`, `0034F3A1`, `0034F3AB`, `0034F3B8` |
| `00394600` | 30 B | returns at once when byte `01EFAC10` equals 2; otherwise tail-jumps a 175-byte helper with (`0x108`, the address of a 326-byte routine, 0), that address in `rdx` | `00394607`, `0039460C`, `00394613`, `00394618` |
| `003DB790` | 11 B | tail-jumps `ActorResource_AllocateAndSubmitEntry` with `r8d` = 1, passing `rcx` and `edx` through unchanged | `003DB796` |
