---
system: How a script binds to an actor, and how an actor's requests are scheduled — the record's four image pointers and the channel walk
category: 01-Script-VM-Native-Bridge
status: "REOPENED — SECTION-12 trigger resolved (SECTION-12 accepted by a non-author review 2026-09-29) and the page returns through the owner read; the wait kinds answered (OV-14); the footer slots answered on ORACLE's record with a premise correction, FABLE adjudication pending (RC-12); the run-state promoters answered (RC-14); RC-13 answered for the question as asked (the shipped scripts' dominant use of each channel; an author's intent is a stated limit); whether shipped play exhausts the notification pool stays on OV-10 (status line current 2026-09-30, SWE2-CONTRACT)"
owner_layer: PrimaryOwner:ActorEntity — the record initialiser and the entry lists; execution by Script_VM_Native_Bridge
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: ActorStorage_InitializeRecord read at the four plants (00266700-002667D7), ActorResource_SelectPendingEntryForExecution
    (168 B) and ActorResource_StartEntryScriptExecution (0x3DBDC0-0x3DBE0C) read in full, ActorResource_InsertEntryFromDescriptor
    read for the channel clamp and the id match; one image's actor-entry table decoded and the version word checked in 1,114
corpus_validated: "1114 / 1114 EBP2 script images carry version word 0x000B, so every shipped actor entry is 0x30 bytes"
last_reviewed: 2026-09-11
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-script-binding-and-scheduling-pass-1
  crossref_clean: true
  last_pass_kind: authored
---

# How a script binds to an actor, and how an actor's requests are scheduled

> **An actor is bound to its script when its record is initialised: the initialiser looks the actor
> up in the image's actor-entry table and plants four pointers into the record — the entry, the
> function-offset table, a second per-actor table and the bytecode base.** From then on a request
> to run a function is an entry on one of the actor's channels; each drive pass picks the
> highest-numbered channel with a runnable entry, and the first run of an entry sets the program
> counter to `bytecode base + functionTable[id]`. BF-4 asked both halves; this is the answer.

## 1. What the player sees

Every scripted thing an actor does — a door opening on approach, an NPC's `talk()`, a monster's
`init()` — is a *request* filed on that actor and run by this machinery. Which of several pending
requests runs first is the channel walk below; a script author's `REQ`, `REQSW`, `REQEW` family
chooses the channel.

## 2. Native mechanism

### 2.1 The binding: four pointers planted by the record initialiser

`ActorStorage_InitializeRecord` (`00266530`) takes the manager slot in `rcx`, the record table in
`rdx` and the actor index in `r8d`, and reads the slot's bound image (`rsi = [rcx]`,
[the manager slot](../../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md)
`+0`). At `002666FC`–`002667CA`:

```
sum      = image + hdr.sumTableOff (+0x14);   record.+0x02 = 1 + (index < sum.entries[0])   ; 002666FC-0026670D
entries  = image + hdr.tableOff18   (+0x18);   stride = hdr.word0 >= 8 ? 0x30 : 0x20         ; 00266710-0026672D
entry    = entries + 4 + index * stride                                                       ; 00266731
record.+0x40 = entry                                                                          ; 00266734
record.+0x48 = image + ImageAddress_ResolveRuntimePointer(entry.+0x10)                        ; 00266795-002667A2
record.+0x50 = image + ImageAddress_ResolveRuntimePointer(entry.+0x14)                        ; 002667A6-002667B9
record.+0x58 = image + entry.+0x08                                                            ; 002667C0-002667CA
record.+0x16 = 1;  then 003DB580 builds the entry lists                                       ; 002667CE-002667D7
```

The header word at `+0` is `0x000B` in every shipped image ([the section_000 sheet](../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md)
reads the dword as the marker `0x8000000B`; its low word is what this branch tests), so every
shipped entry is **0x30 bytes**; the `0x20` form is a legacy branch nothing ships for. `tableOff18`,
"not read by this loader" on the sheet, is **the actor-entry table**: a `u32` count, then one
`0x30`-byte entry per actor in the order the decompiler lists them.

**The actor entry** (`record + 0x40`, FZ-23), from the initialiser and the `local` variable
resolver, with `dst_a0180` as the worked example (six actors, count `6`):

| entry offset | meaning | evidence |
|---|---|---|
| `+0x00` | `u32` name-pool offset of the actor's name (`0xA1` → `監督`) | the six entries' first dwords are the six names' pool offsets in order |
| `+0x06` | `u8` party code: `0xFF` none; bit 7 set with `code & 0x7F ≤ 3` registers the record in the four-entry roster at `0209A1F0`, evicting the previous holder (`0026673C`–`00266792`; the roster is the one [the party pages](../../11-Party/README.md) own) | read at `00266738` |
| `+0x08` | `u32` **bytecode base** offset → `record + 0x58` | `002667C0` |
| `+0x10` | `u32` **function-offset table** → `record + 0x48` (through `0020E600`) | `00266795` |
| `+0x14` | `u32` the table `FUN_003589E0` indexes at 4-byte stride → `record + 0x50` | `002667A6` |
| `+0x1C` | `s32` the actor's **`local`-variable area** offset inside the image's `+0x48` region (`0`, `8`, `8`, `8`, `8`, `0x10` for the six — cumulative sizes) | `00264E30`, [the storage-class page](script-variables-and-their-storage-classes.md) |
| `+0x04` | `u16` **the actor's type**, 0–7 (ff12-script `tScriptNames.scriptType`; the count table at header `+0x14` holds one `u16` per type after its `8`, and the entries are sorted by type — see the class note in §2.4) | tier 9 + the corpus (2026-09-12) |
| `+0x06`… | the `u16` ff12-script writes as `pcId` (`0xFF` none, `0x80`–`0x83` a PC slot) — the party code above | tier 9 |
| `+0x0C` | `u32` instruction count of the actor's bytecode (`numOfInstructions`, written by the compiler, read by no loader site) | tier 9 |
| `+0x14` | the jump-position list `{u32 count; u32 offset[]}` (`listOff`) — what `FUN_003589E0` indexes | tier 9 |
| `+0x18` | **the special-function footer** `{u16 count = 0x12; u16 special[18]}` (`sepaOff`): `special[t]` = the index of the actor's function declared with special type `t`, `0xFFFF` none — the table §2.6 reads (~~the wait resolver's "word `+0x18` when the count exceeds 11" is `special[12]`, the `mapjump(12)` function~~ *Corrected 2026-09-30 (OPUS, on SWE2-AUDIT-SPEC's batch-14 narrowing 2): word `+0x18` is `special[11]`, the actor's `parameter` function - the footer is 0-based, `{u16 count; u16 special[18]}` with word k at `+2+2k` ([`rc12-footer-channels-runstate-0930`](../../_index/candidates/rc12-footer-channels-runstate-0930/README.md), controls A and B of `rc12_slots.py`)*) | tier 9 + `0025E16A`–`0025E19C` |
| `+0x20` / `+0x22` | `u16 duplicateId`, `u16 pos` (the actor's index) | tier 9 |
| `+0x24`–`+0x2F` | three dwords the compiler writes as 0 (`unk6`–`unk8`) | tier 9 |

The party code is the one authored byte that reaches outside the script system: it is how an
image says "this actor *is* party slot N".

### 2.2 Starting a function: `pc = bytecode base + functionTable[id]`

`ActorResource_StartEntryScriptExecution` (`003DBDC0`) takes the record and a request entry:

```
slot   = record.+0x11 (currentWaitSlot, SIGNED);  wait = *(record.+0xA8) + slot * 0x28   ; 003DBDD4-003DBDEE
offset = ActorScriptResource_GetBytecodeOffsetById(record, entry.+0x04)           ; 003DBDF2 -> [record+0x48][id]
ScriptExecutionState_ResetCore(wait)                                              ; 003DBDFD
wait.+0x00 = record.+0x58 + offset;  wait.+0x14 = 1 (waitKind RUNNABLE)           ; 003DBE02-003DBE0C
```

The function id is the request entry's `+4` word; the lookup is bounds-checked against the table's
count and returns `0` when out of range (the sheet's "starts at the image base rather than
refusing" — now known to mean *this actor's* bytecode base). The program counter lives in the
**wait slot** (`ActorWaitSlot +0`), which is why the interpreter's third argument is that slot and
`r14 = [r8]` is the pc.

### 2.3 Choosing what runs: the channel walk

`ActorResource_SelectPendingEntryForExecution` (`003DB6E0`, 168 B, read whole):

```
if record.+0x63 == 0: return                                   ; entryListFlags: nothing to do
for channel = record.+0x88 - 1 down to 0:                      ; slotCountA8 - 1 .. 0  (HIGHEST FIRST)
    e = record.+0x94[channel]                                  ; channelHead
    while e != 0xFF:
        entry = *(record.+0xA0) + e * 0x14                     ; ActorResourceEntry
        if entry.+0x11 == 1:  e = entry.+0x00; continue        ; state 1: skip, follow the chain
        record.+0x11 = entry.+0x02                             ; currentWaitSlot := the entry's wait slot
        if entry.+0x11 == 2: StartEntryScriptExecution(record) ; state 2: first run, set the pc
        record.+0x62 = e; record.+0x14 &= ~0x40; return        ; selectedEntryIndex; "not idle"
record.+0x14 |= 0x40; return                                   ; nothing runnable: idle bit
```

So: **higher channel numbers win**, each channel is a FIFO chain from its head, an entry in state 1
is passed over, state 2 means "not started yet" and triggers the pc setup, any other state resumes
where the wait slot left off. The idle bit (`flags14` bit 6) is what the drive loop reads to stop
driving the actor.

Entries are filed by `ActorResource_InsertEntryFromDescriptor` (`003DB7A0`): the descriptor's
channel (`+2`) is **clamped to `slotCountA8 − 1`** (`003DB7C1`–`003DB7C5`), and a kind-4 request
whose resource id (`+4`) already sits on that channel is found by a bounded walk (`003DB83F`–
`003DB867`) rather than filed twice. The entry's `+0x11` state is the caller's fourth argument.

### 2.4 Filing a request: the `REQ` family, the descriptor and the two insert paths (2026-09-12, FABLE-FZ25-26)

Nine request opcodes share one submit tail in the interpreter (`0025F7B6`–`0025F7D0` and its twin at
`002602C3`–`002602E1`) and differ only in two immediates they pass to
`ScriptVM_SubmitActorRuntimeRequest` (`00268850`):

| opcode | mnemonic | kind (`[rsp+0x28]`) | mode (`[rsp+0x30]`) | after a successful submit |
|---|---|---|---|---|
| `0x21` / `0x24` / `0x27` | `REQ` / `REQSW` / `REQEW` | 0 (`r11d`, zero at every loop head) | 1 (`ebp`) / 2 / 3 | `SW` and `EW` set the requester's wait slot to `waitKind` 4 (`002602EE`) |
| `0x22` / `0x25` / `0x28` | `FREQ` / `FREQSW` / `FREQEW` | 2 (`0025FBBC`, `002606B6`, `002610A8`) | 1 / 2 / 3 | same |
| `0x23` / `0x26` / `0x29` | `TREQ` / `TREQSW` / `TREQEW` | 4 (`0025FF93`, `00260A79`) | 1 / 2 / 3 | same |

So the prefix letter is the descriptor **kind** (`R` 0, `F` 2, `T` 4) and the suffix the **mode**
(none 1, `SW` 2, `EW` 3). Each handler pops three values first (`00268870`–`0026893F`, int or
float coerced): the target actor reference `edi`, the function id `r14d` and the channel `esi`;
bit 15 set in either of the first two aborts with 0 (`00268944`). The mode selects one of three
static words added to the pc (`00268955`–`00268982`) — the instruction's own length — and the
advanced pc is written back into the requester's wait slot (`00268993`), so a resumed requester
continues after the `REQ`.

**The descriptor** built on `00268850`'s stack (`002689A4`–`002689C0`) and copied into the entry by
`ActorResource_InsertEntryFromDescriptor` (`003DB8BB`–`003DB906`):

| descriptor | entry | what |
|---|---|---|
| `+0` kind | — (not stored: it selects the insert behaviour at `003DB7DC`–`003DB7F0`; 4 dedupes by id) | 0 / 2 / 4 from the opcode |
| `+1` mode | `+0x10` (the store's `state` row: 4 = detached list, 3 = the remover's special case — values native submitters pass; the interpreter passes 1 / 2 / 3) | 1 / 2 / 3 from the opcode |
| `+2` channel | `+2` (clamped to `slotCountA8 − 1` **from above only** — a signed compare; a low byte ≥ `0x80` enters negative, see EF-2 on [the calling convention](../Spawn-Verbs/the-script-to-native-calling-convention.md)) | the popped channel's **low byte** (`002689B1`) |
| `+3` | `+3` | the requester's `currentWaitSlot` (`record + 0x11`) |
| `+4` function id | `+4` | the popped id; bounds-checked against the target's function table at `003DBD0C` (out of range → return 3) |
| `+6` | `+6` | the requester's `selfIndex` (`record + 0`) |
| `+8` flag | `+0x12` bit 0 | always 1 here (`002689C0`) |
| `+0xC` | `+8` | the requester's **own manager index** — `dword[r13+0x28]`, r13 = the requester's `ActorManagerSlot`, written unconditionally at `002689D9`/`002689DF` whether the target ref encoded a manager or defaulted to the requester's own. *Corrected 2026-09-17 (SWE2-STRUCT): this row previously read "the requester's pc offset — the return point"; the pc offset is descriptor `+0x10` → entry `+0x0C`, see the next row* |
| `+0x10` | `+0xC` | the requester's pc as an offset from its bytecode base (`0026898F` `sub ecx, [r15+0x58]` → `002689BC` `mov dword [rsp+0x30], ecx`) — the return point, carried into the release request's own `+0x10` |

**Target resolution.** The actor reference is either `(manager << 16) | ordinal` when bit 14 is set
(`002689C5`–`002689D3`) or an ordinal in the requester's own manager (`[slot + 0x28]`), resolved by
`003587C0`; no target returns 3 (`00268A3B`).

**Two insert paths, two initial states.** *The class (FZ-25, 2026-09-12):* `record + 0x02` is
`1 + (index < firstTypeCount)` (§2.2), and the header's `+0x14` table is `{u16 8; u16 count[8]}` —
one count per actor type 0–7, the entries sorted by type: in all **1,114** shipped images the first
word is 8 and the eight counts sum to the actor count; in all 1,081 decompiled images with
declarations the types are non-decreasing. So **class 2 = a type-0 actor, class 1 = any other
type**. Type 0 is the control layer — `__MJ_CTRL#` (1,525 declarations), `Map_Director` (626),
`setup` (621), `btl_trap_ctrl`, `EventLightActor`, `EventDirector`, `ReposDirector`, `SE`,
cameras, message and sound actors; the embodied types are 1 (`magic_switch`, `warp`, `gil_*`
interaction actors), 5 (`PC#`, the named party members, `summon`), 6 (`treasure_#`, `WARP_PC#`,
`NPC#`, `hitactor#`) and 7 (`monster_#`, `unique_monster_#`, `trial_#`, `PC#`); ff12-script names
the eight `mapActor`, `interactionActor`, three unknowns, `battleActor`, `sceneActor`, `battleInit`.
**Correction SECTION-12 (2026-09-24): the gate reads the ISSUER, not the target.**
If the issuer's `+0x02` class is 1 and its `+0x10` is 0,
`003DB790` files the entry in **state 1** (`mov r8d, 1; jmp AllocateAndSubmitEntry`); otherwise
`003DBAE0` files it in **state 2**, then — only when target and issuer differ — if the target's `entryListFlags` is non-zero, walks the
target's whole entry array promoting every state-1 entry to 2 (`003DBB30`–`003DBB40`), runs the
channel walk on the target (`003DBB45`) and halves `entryListFlags` (`003DBB4A`).
`AllocateAndSubmitEntry` returns 2 when the free list is exhausted (`003DBD32`) and 3 when the id is
out of range; on 1 the submitter sets bit *channel* of the target's `+0x26` word (`00268A2B`) and
calls `0025B580(target)`; on any other result it decrements the target's `+0x10` (`00268A48`).

### 2.5 The entry's life, from every writer of its run-state byte

The byte the channel walk tests is the entry's **`+0x11` runState**. It is now declared separately from **`+0x10` request mode**; the older no-store-row statement is superseded. SECTION-12 executes both sources independently. Every `.text` write of an `ActorResourceEntry`'s `+0x11` (displacement sweep over the resource and
actor code, the entry base proved at each):

| state | written by | meaning |
|---|---|---|
| 1 | `InsertEntryFromDescriptor` from `003DB790` | filed, not yet selectable — the channel walk passes it over |
| 2 | `InsertEntryFromDescriptor` from `003DBAE0`; the promotion loop at `003DBB35` | runnable, not started — the walk selects it and sets the pc |
| 3 | `ActorResource_StartEntryScriptExecution` `003DBE68` | started; the walk resumes it where the wait slot left off |
| 0 | `ActorResource_UnlinkEntryAndMarkFree` `003DC1A4`, `003DC1B0` (`003DC233`) | free |

`RET` (`0x2D`) and `RETT` remove the running entry through `ActorResource_RemoveActiveEntry`
(`003DB2A0`, which treats an entry whose `+0x10` is 4 as being on the detached list, `003DB2F8`, and
calls `003DC0D0` when `+0x10` is 3 and `+6` is not `0x8000`) and immediately re-run the channel walk; `RETN` / `RETTN` /
`REQCANCEL` go through `ActorResource_RecycleEntryRange` (`003DB420`) first. Who else promotes a
state-1 entry to 2 was not found in the functions read (the wait resolver `0025DF00` is the
candidate) — a limit, not an absence. *Registered as RC-14 (2026-09-30, SWE2-CONTRACT); the SECTION-12 specification
adds that immediate insertion reselects and promotes only when the target is not the issuer
([the actor request](the-actor-request-from-arming-through-start-and-return.md) §1).*

### 2.6 The actor entry's `+0x18`: a per-actor word table (FZ-25, narrowed)

Eighteen sites in the actor pass functions (`0025AE00`, `0025B820` ×3, `0025BAD0`, `0025C230` ×5,
`0025C830` ×5, `0025DF00`, `00263050`, `00263D40`) read the entry's `+0x18` and resolve it with
`ImageAddress_ResolveRuntimePointer` into the image. The wait resolver's use is the one read here
(`0025E16A`–`0025E19C`): the resolved table's word `+0` is a count; when it exceeds 11 the word at
`+0x18` is compared with the current function id, and a match sets bit 0 of the record's `+0x0C`.
~~What the table lists is not established; `+0x0C`, `+0x20`–`+0x2F` of the entry are still unread.~~
**Identified 2026-09-12 (FABLE) from the authoring tool:** the table is the actor's
**special-function footer** — ff12-script writes, after each actor's function list, `{u16 count =
0x12; u16 special[18]}` with `special[function.specialType] = function index`
(`CScriptCompileAsmWrite.cpp`, `_writeFunctionMetadata`), the special type being the number on a
function declaration (`function mapjump(12)`). So the wait resolver's test — count above 11, word
`+0x18` equal to the current function id — asks ~~**"is the running function this actor's
`mapjump` special function"**~~ *Corrected 2026-09-30 (OPUS, on SWE2-AUDIT-SPEC's batch-14 narrowing 2): **"is the running
function this actor's `parameter` special function"** - word `+0x18` is `special[11]` (0-based footer, word k at `+2+2k`;
[`rc12-footer-channels-runstate-0930`](../../_index/candidates/rc12-footer-channels-runstate-0930/README.md))*, and sets record `+0x0C` bit 0 when it is. The other seventeen
sites read other slots of the same footer; which special type each site asks for is not read here *(answered on ORACLE's record: RC-12, 2026-09-30, section 7 — FABLE's adjudication of the numbering is still pending; 2026-10-02, OPUS)*
*(registered as RC-12, 2026-09-30, SWE2-CONTRACT)*.
`+0x0C`, `+0x20`–`+0x2F` are the compiler's instruction count, duplicate id, index and three zero
dwords (§2.2 table); no loader site reads them.

## 3. Key addresses

| address | role |
|---|---|
| `00266530` | `ActorStorage_InitializeRecord` — the four plants at `00266734`, `002667A2`, `002667B9`, `002667CA`; the roster registration `0026673C`–`00266792` |
| `003DB6E0` | `ActorResource_SelectPendingEntryForExecution` — the channel walk |
| `003DBDC0` | `ActorResource_StartEntryScriptExecution` — the pc |
| `00358A00` | `ActorScriptResource_GetBytecodeOffsetById` — `[record+0x48]`, 8-byte stride, dword at `+8` |
| `003DB7A0` | `ActorResource_InsertEntryFromDescriptor` — filing a request |
| `002697A0` | `Actor_RequestResourceReentry` (research import, `X55_NATIVE_REPLAY_CONTRACT.md` — "actor/resource re-entry, **not** lifecycle re-entry"; body re-read 2026-09-15): `ActorResource_RecycleEntryRange` (`003DB420`) twice — channel 1 then channel 0, mode 3 both times — then a tail call to `Actor_RequestConfiguredPrimaryResources` (`00269640`) |
| `00356150` | `Actor_RequestResourceReentry_Thunk` — 8 B: `mov rcx, rdx; jmp 002697A0` (the patched site `X55_NATIVE_REPLAY_CONTRACT.md` §5 describes) |
| `0209A1F0` | the four-entry party roster the party code registers into |

## 4. Data structures and formulas

The record's script pointers, all into the slot's bound image:

| record | store name | from |
|---|---|---|
| `+0x40` | (unnamed) | the actor entry, `tableOff18 + 4 + index × 0x30` |
| `+0x48` | (unnamed) | `image + resolve(entry.+0x10)` — function-offset table |
| `+0x50` | `payloadSectionA` (record) | `image + resolve(entry.+0x14)` |
| `+0x58` | `payloadSectionB` | `image + entry.+0x08` — bytecode base |

## 5. Call chain

`ActorStorage_AllocateAndInitializeRecords` → `ActorStorage_InitializeRecord` (binding) ·
`ActorManager_RunFieldRuntimePass` → `WorldActor_UpdateRuntimeAndScriptExecutionState` →
(`SelectPendingEntryForExecution` from the interpreter and seven other callers) →
`StartEntryScriptExecution` → `WorldActorScriptVM_InterpretBytecode`.

## 6. Modding notes

- An actor's whole script identity is four offsets in its `0x30`-byte entry; a mod that adds an
  actor adds an entry, and the `local` area offset at `+0x1C` must be cumulative or two actors
  share locals.
- Channel numbers are priorities, highest first; a request on channel `slotCountA8` or above is
  silently clamped to the top channel.
- An out-of-range function id runs from this actor's bytecode base, not from nothing.

## 7. What is not known

- [x] ~~The rest of the actor entry — `+0x18` is a resolvable word table (§2.6), `+0x0C` and
      `+0x20`–`+0x2F` are unread — and what `record + 0x02` classifies beyond selecting the insert
      path (§2.4).~~ **FZ-25 ANSWERED 2026-09-12 (FABLE):** the entry is ff12-script's
      `tScriptNames` (§2.2 rows), `+0x18` its special-function footer (§2.6), and the class is the
      actor's type — 2 for the type-0 control actors, 1 for embodied ones (§2.4), checked over all
      1,114 images. Residue: which special slot each of the other seventeen footer readers asks for.
- [x] ~~The entry states beyond 1 and 2 and the descriptor kinds 0 / 2 / 4 — what each request opcode
      files.~~ **ANSWERED 2026-09-12:** §2.4–2.5. **FZ-26.**
- [x] ~~The other seven `waitKind` values (the falsification pass below names only kind 1).~~ *Answered (pointer
      2026-09-30, SWE2-CONTRACT):* the wait kinds 0–7 and their resume conditions are enumerated on
      [the actor request page](the-actor-request-from-arming-through-start-and-return.md) §5, with every list-wait
      producer and a store census in §7 (OV-14, ANSWERED 2026-09-29; record `_index/candidates/ov14-wait-kinds-fable/`),
      and the native wait services are a closed set (OV-11). Tier 1.
- [x] **RC-12.** Which special-function slot each of the other seventeen readers of the actor entry's `+0x18`
      footer asks for (`0025AE00`, `0025B820` ×3, `0025BAD0`, `0025C230` ×5, `0025C830` ×5, `00263050`, `00263D40`; the
      wait resolver's `mapjump` test is §2.6). Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-12:* **ANSWERED 2026-09-30 on ORACLE's record `_index/candidates/rc12-footer-channels-runstate-0930/` (commit `1e4537034`), with a premise correction: the footer is 0-based.** The raw footers name each word directly — word 0 (`+0x02`) is never set in a footer, word 1 is `main`, 2 `talk`, 3 `touch`, 4 `touchon`, 5 `touchoff`, 6 `across` and so on — so FABLE's slot table (`rc121314-fable-0930`, `82cb3490a`) and §2.6's `mapjump` reading are each off by one. **FABLE adjudication pending** (`OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930`); §2.6 is FABLE's text and is not edited here.
- [x] **RC-13.** What each request channel means to a script author beyond its priority (§2.3: highest first). The
      ff12-script documentation and grammar name no channels (searched 2026-09-30); a census of the channel operand
      the shipped `REQ` family passes per function kind is the static next step. Registered 2026-09-30
      (SWE2-CONTRACT).
  *Applied 2026-09-30 (records) RC-13:* **NARROWED 2026-09-30 (ORACLE's record `rc12-footer-channels-runstate-0930`, commit `1e4537034`; FABLE's `rc121314-fable-0930`, `82cb3490a`):** the engine files each special function it triggers on a fixed channel (0–7, read at every native submit), and FABLE's `sysReqchg` rows are not channels. **Residue:** what an author *intended* by putting its own logic on a given channel is an authoring convention — no further static fact decides it, and no run-time observation would add an intent. **Proposed disposition, for a non-author reviewer: OUT OF EVIDENCE BOUNDARY** (not self-closed).
  *Round 3 (records) RC-13:* **ANSWERED 2026-09-30 for the question as asked (SWE2-CONTRACT, disposition (a) of SWE2-AUDIT-SEM's `_index/candidates/auditsem-review-rc121314-0930/REVIEW.md` §4; FABLE's census `_index/candidates/rc121314-fable-0930/rc13_channels.py`, `82cb3490a`, re-run by the reviewer):** the engine gives a channel no meaning beyond its priority, highest first; each engine-triggered special function sits on a fixed channel 0 to 7 (ORACLE `1e4537034`). The shipped scripts use channels by convention, as dominant-use shares: 1 the default and largest channel, an actor's own behaviour — movement, turns, doors, event lights (26,879 calls in 841 scripts; no single function above 8% of its calls); 2 conversation and placement; 3 and 4 the paired show and hide presentation channels, lip flap included; 5 placement and repositioning; 7 mostly reset, cancel and cleanup (about half of its parsed calls), also some repositioning and item hand-overs (`入手`); 0 and 6 almost unused. FABLE's rows 16 and 17 are `sysReqchg` override slots (`talkhold`, `talkterm`), not channels *(restated 2026-10-01 on FABLE's record at `a8aed6ca9`)*. The 12% of calls through `reqArr` arrays or computed targets are counted by channel only. **Limit, not a status:** what an author intended by a channel is a fact about people that no shipped artefact carries; not claimed. *The OUT OF EVIDENCE BOUNDARY proposal is withdrawn: the reviewer did not sign it (that status covers facts about the build carried only by an unadmitted artefact).*
- [x] **RC-14.** Whether any code outside the resource and actor functions the §2.5 displacement sweep covered moves an
      entry's `+0x11` run state from 1 to 2 (the promotion loop at `003DBB35` and the `003DBAE0` insert are the known
      writers of 2). Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-14:* **ANSWERED 2026-09-30 (static; ORACLE's record `rc12-footer-channels-runstate-0930`, commit `1e4537034`, confirming FABLE's `rc121314-fable-0930`, `82cb3490a`):** image-wide, exactly three stores reach an entry's `+0x11` — the same loop over `*(record + 0xA0) + 0x11`, stride `0x14`, gated by record `+0x63` and followed by the channel walk — plus the insert; none elsewhere.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The four plants and their sources | `00266530` at the cited sites; `dst_a0180`'s entry table decoded | 1 | PROVEN |
| Every shipped entry is 0x30 bytes | the header word is `0x000B` in 1,114 / 1,114 images | 1 | PROVEN |
| The channel walk | `003DB6E0` read whole | 1 | PROVEN |
| The pc formula | `003DBDC0` at `003DBDF2`–`003DBE0C`; `00358A00` | 1 | PROVEN |
| The kinds and modes per opcode | the nine handlers' tails (`0025F7B6`, `0025FBB8`, `0025FF8F`, `002602C3`, `002606AE`, `00260A71`, `00260CDF`, `00260DB1`, `002610A0`) | 1 | PROVEN |
| The descriptor and the two insert paths | `00268850` read whole; `003DB790`, `003DBAE0`, `003DBCF0`, `003DB7A0` | 1 | PROVEN |
| The state byte's writers | displacement sweep of `+0x11` writes, each base checked | 1 | PROVEN (for the functions read) |
| What each channel *means* to an author | **dominant use in the shipped scripts** (RC-13, FABLE's `rc13_channels.py`): 1 an actor's own behaviour (a long tail: no function above 8% of its calls), 2 conversation and placement, 3 and 4 show and hide presentation, 5 placement and repositioning, 7 mostly reset, cancel and cleanup (about half its parsed calls; also repositioning and item hand-overs); the engine gives a channel no meaning beyond its priority (§2.3); an author's intent is not claimed; FABLE `82cb3490a`, re-run by SWE2-AUDIT-SEM | authored data | MEASURED (dominant-use shares; intent not claimed) |
| The class is the actor's type; the `+0x14` table is eight per-type counts | `00266700` reads word `+2`; all 1,114 images: first word 8, counts sum to the actor count; 1,081 decompiled images: types non-decreasing (`Tools/work/repos-d2`) | 1 + 9 + data | PROVEN |
| The entry's authored layout and the footer | ff12-script `CScriptContainer.h` `tScriptNames`, `tFuncFooter`; `CScriptCompileAsmWrite.cpp` `_writeFunctionMetadata` | 9 | PROVEN (tool) |

### Claims added 2026-09-30 (SWE2-CONTRACT)

| claim | evidence | tier |
|---|---|---|
| SECTION-12's mechanism is accepted non-author | AUDIT-SEM's OV-acceptance review (re-executed, 139 / 8 / 85) | 1 + isolated original-code execution |
| The wait kinds 0–7 are enumerated | OV-14's record; the actor request page §5, §7 | 1 |
| The authoring tool names no channels | `Collaboration/Tools/ffxii/ff12-script-master` docs and grammar, searched for channel / priority | 9 (tool) |

## 9. Related

- [The interpreter](worldactor-scriptvm-interpreter.md) §14 — the context is the manager slot
- [Script variables](script-variables-and-their-storage-classes.md) — the `local` class uses the entry's `+0x1C`
- [The actor storage record field map](../../04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md)
- [The field runtime pass](../../04-Actor-Entity/the-field-runtime-pass.md) §11 — the wait resolver between the drive loop and the interpreter

## Falsification pass 1 — 2026-09-13 (OPUS)

| claim | measured |
|---|---|
| `003DB6E0` is **168 B** and read whole | **168**, and every step of §2.3's walk is in it |
| the channel walk runs **highest first** | `movzx eax, byte [rcx+0x88]` / `sub eax, 1` / `js`, then `sub r8, 1` / **`jns`** — it counts **down** |
| the `+0x63` gate, the `0xFF` chain end, state 1 skipping, state 2 calling the starter, `+0x62` selected, bit 6 | all present: `cmp byte [rcx+0x63], 0`; `cmp ebx, 0xff`; `cmp ecx, 1` / `jne`; `cmp ecx, 2` / `call 003DBDC0`; `mov byte [rdi+0x62], bl`; `and byte [rdi+0x14], 0xbf` and `or byte [rdi+0x14], 0x40` |
| the entry stride is `0x14` | `lea rcx, [rax + rax*4]` then `lea rdx, [rax + rcx*4]` — **× 5 × 4 = × 20** |
| `003DBDC0` sets the pc from `record.+0x58` and marks the slot runnable | `add rax, qword [rbp+0x58]` / `mov [rdi], rax` / `mov byte [rdi+0x14], 1` |

### `+0xA0` and `+0xA8` are pointers, and the pseudo-code dropped the dereference

Both lines read as arithmetic on the record. Both fields are **loaded**:

```asm
003DBDE7  mov rax, qword ptr [rcx + 0xa8]   ; the wait-slot array — a POINTER
003DB728  mov rax, qword ptr [rdi + 0xa0]   ; the entry array — a POINTER
```

So the wait slot is `*(record + 0xA8) + slot × 0x28` and the entry is `*(record + 0xA0) + e × 0x14`.
Written as `record.+0xA8 + …` the arrays would live **inside** the record at those offsets; they do
not — they are separate allocations the record points at. Corrected in §2.2 and §2.3.

*(`+0x11` is read with `movsx` in both sites, so `currentWaitSlot` is **signed** — noted in §2.2.)*

### The same five instructions appear in a second function, and they settle a cross-page question

`003DBDC0` computes the wait slot with:

```asm
003DBDD4  movsx rax, byte ptr [rcx + 0x11]
003DBDE3  lea   r8,  [rax + rax*4]
003DBDE7  mov   rax, qword ptr [rcx + 0xa8]
003DBDEE  lea   rdi, [rax + r8*8]
```

`0025DF00` — the field runtime pass's wait resolver — computes it with the **same five instructions
in the same order**, different registers (`0025DFB6`–`0025DFC6`). The
[field runtime pass](../../04-Actor-Entity/the-field-runtime-pass.md) pass derived
`*(record + 0xA8) + (int8)(record + 0x11) × 0x28` from that function alone; **this page's
`003DBDC0` confirms it independently**, and supplies the name the other derivation lacked:
`+0x11` is **`currentWaitSlot`**.

And it names one state of an enum that was unnamed. §2.2 writes `wait.+0x14 = 1 (waitKind
RUNNABLE)`. That byte is the one `0025DF00` switches on with `cmp eax, 7` and an eight-entry jump
table — so **the wait slot's `+0x14` is a `waitKind` enum `0…7`, and kind `1` is RUNNABLE**. Two
pages, two halves: one had the range, the other has a name for a value in it.

**Not claimed:** the other seven kinds remain unnamed — this pass adds one value to the enum, not a
table for it. §2.1's binding arithmetic, §2.4's `REQ` family, §2.5 and §2.6 were not re-derived, and
nothing here was executed or observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Movement — SERVICE and CLIENT.**
  - `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`) drives movement in the same per-actor update that
    runs the script: `Movement_UpdateActorFrame`, `Movement_SetRequestedSpeed` and three movement helpers of 20–935 bytes.
  - `00263050` and `ActorStorage_InitializeRecord` call movement bodies of 145–1,339 bytes.
  - `003587C0` is read by `Movement_UpdateSteeringTowardTarget` and two helpers.
  - `ActorResource_RemoveActiveEntry` (`003DB2A0`) is called from the same per-actor update.
- **Presentation — SERVICE and CLIENT.** `0025DF00` calls three small Presentation helpers (42–84 B), and `003587C0` is
  read by the 714-byte render-cluster body.
- **Input — SERVICE.** `00263230` — the mode-1 arm of `ActorResource_StartEntryScriptExecution` — calls
  `00226BE0`, an Input-layer helper that builds a per-channel bitmask (`movsxd rax, ecx`; `r13d = 1 << cl`
  at `00226BFA`–`00226C03`): the entry-start path consults the input channel state. (edge: `edges.tsv`)
- **CombatAI — MECHANICAL (SWE2-EC7-96, 3 edges).** `00377C20` — the re-check this page's `0030A6E0`
  section cites — is reached through 3 edges on the CombatAI layer (`003014C0`, `00301AD0`, `00305AB0`).
  Shared-helper fan-in; no CombatAI relationship to script binding.
- **CombatAction — MECHANICAL (SWE2-EC7-96, 21 edges).** `00320A40` — the resolver the same body
  consults — is reached through 21 edges on the CombatAction layer (`00303830`, `003064F0`, `00306760`,
  `00307300`, +17 more). Shared-resolver fan-in; no CombatAction relationship to script binding.
- **CombatFormula — MECHANICAL (SWE2-EC7-96, 5 edges).** `0030A6E0` calls `00320A40`, `0031B9F0` is
  called by `00320AB0`, and `00320A40` is reached through `00385680`, `00469EC0` and one more on that
  layer. Shared-helper fan-in.
- **Gameplay — MECHANICAL (SWE2-EC7-96, 6 edges).** `0030A6E0` calls `0031B9F0`, `0031B9F0` calls
  `00322C50`, and `00377C20` is reached through `00307D10`, `0030A8A0` and two more on that layer.
  Shared-helper fan-in.
- **Items_Equipment_Shops_License — MECHANICAL (SWE2-EC7-96, 2 edges).** `00377C20` is reached through
  `00309FB0` and `0030FD10` on that layer. Shared-helper fan-in.
- **Rewards_Progression_Economy — MECHANICAL (SWE2-EC7-96, 1 edge).** `00377C20` is reached through
  `00312280` on that layer. Shared-helper fan-in.
- **Status_Periodic_Terminal — MECHANICAL (SWE2-EC7-96, 3 edges).** `00377C20` is reached through
  `0030E360`, `0030F690` and `00310DB0` on that layer. Shared-helper fan-in.
- **Party — CLIENT and SERVICE (4 edges).** 1 inbound (Party bodies `00304180` call page-cited `FieldData_GetActiveFieldRecordBit15` (00377C20)); 3 outbound (page-cited `0025C830`, `00263050`, `00263230` call Party bodies `PartyFocus_GetCurrentPackedActorHandle` (003590D0), `PartyFocus_CommitPendingPackedActorHandle_Thunk` (00358BB0)). Substantive edges include `0025C830` calls `PartyFocus_CommitPendingPackedActorHandle_Thunk` (00358BB0); the remaining edges run through shared helpers the page cites.
- **WorldAreaField — MECHANICAL (5 edges).** 1 WorldAreaField-side calls into shared helper(s) the page cites (`FieldData_GetActiveFieldRecordBit15` (00377C20)); 4 calls from page-cited bodies into shared WorldAreaField plumbing (`FieldData_GetActiveFieldRecordBit15` (00377C20), `WorldTransition_GetActiveOrPendingFieldId` (003148F0)) - the helpers' general call surface, not a WorldAreaField relationship of this page's subjects.
## The `003DBDC0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`003DBDC0` `ActorResource_StartEntryScriptExecution` (41 B) — the
entry-script dispatcher whose mode-1 arm is `00263230` (bound on the
time-stop page): `rax = movsx byte[rcx+0x11]` entry index
(`003DBDD4`), `edx = word[rdx+4]` script id (`003DBDDC`), `r8 =
rax*5` entry stride (`003DBDE3`).

| member | role | interior |
| --- | --- | --- |
| `0025D460` (20 B) | entry-record init — `qword[rcx]`/`[+8]`/`dword[+0x10]`/`word[+0x14]`/`byte[+0x16]` all zeroed (`0025D462`–`0025D470`) | [`0025D46C`](../../_index/ADDRESS-INDEX.md) |
| `00358A00` (21 B) | indexed record fetch — `r8 = [rcx+0x48]` list, `edx` vs `dword[r8]` bound (`00358A04`), `eax = dword[r8+rax*8+8]` (`00358A0F`), then `dword[022C7FE0]` + `003588B0` (`00358A24`/`00358A37`) | [`00358A0F`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003588B0`. The `022C7FE0` cell is
the shared resource count.

## The `00268850` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00268850` (`ScriptVM_SubmitActorRuntimeRequest`, ~250 B) — the submit
body under a full register save.

| member | role | interior |
| --- | --- | --- |
| `003DB790` (11 B) | mode-1 forward — `r8d = 1`, tail `003DBCF0` (`003DB790`/`003DB796`) | [`003DB790`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003DBCF0`.

## The `003DB2A0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`003DB2A0` (`ActorResource_RemoveActiveEntry`, ~93 B) — `movsxd rsi, edx`
(`003DB2AA`).

| member | role | interior |
| --- | --- | --- |
| `003DC0D0` | `word[rdx+6]` + `dword[rbx+8]` entry-field read (`003DC0D9`/`003DC0DD`) | [`003DC0D9`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.


## SWE2-EC7-65 update (2026-09-19) - `00263D40`

`00263D40` (135 B) is a `+0x18`-resolve body - `0020E600` single call. Interior anchor `00263D72` (a `0020E600` call).


## SWE2-EC7-87 update (2026-09-20) - `003DB650` pair-table cross-link measured

`003DB650` (133 B) is the 20-stride byte-table splice the
binding callers run: `r8d` and `edx` index rows at
`[rcx+0xA0] + index*20` (`0xFF` or a null rcx yields no row);
when the `edx` row's `byte[+1]` is itself a valid index its row
is walked, `byte[r8+1]` takes that row's `byte[+1]`, the
intermediate rows take `r11b`, and `byte[r8]` takes `dl` - a
three-row link rewrite.
Interior anchor `003DB6BA` (the cross-link byte writes).

## SWE2-EC7-96 update (2026-09-20) - `0030A6E0` measured

`0030A6E0` (162 B) is the four-slot class-mask scan `0025C230`
and `0025C830` run: `edi` 0-3 feeds `0031B9F0(edi, 1)`, the
returned byte goes through `00320A40` and the resolved record's
`+0x64 | +0x3C` is gated against `0x80000003` with the `00377C20`
re-check; the class byte then picks the flag bit - 7..0x18 tests
`bpl` bit 1, 0x1B..0x26 bit 2, exactly 0x1A bit 3, anything else
bit 0 - and a passing slot sets bit `edi` in the returned mask.
Interior anchor `0030A707` (the `0031B9F0` call).

## SWE2-EC7-97 update (2026-09-20) - `002EC380` measured

`002EC380` (60 B) is the mode-0x60 field write `00263230` and
`002690D0` call: `byte[rcx+3] & 0xE0 == 0x60` admits, `dl << 3`
is XOR-folded into `byte[[rcx+0xB8]->+0xF0 +0x62]` masked `0x38`,
and `xmm2 / [01DFE0BC]` truncates into `word[+0x60]` - the
three-bit rotate field plus the scaled word the binding's mode
arm publishes.
Interior anchor `002EC3A1` (the `0x38`-masked XOR store).


## SECTION-12 — arming is not execution, and notification is not guaranteed (2026-09-24)

[Original-code production and controls](../../_experiments/evidence/continuation-section12-actor-request-waits/REVIEW.md)
connect `00268850` -> allocation/insertion -> selection/start -> interpreter RET -> detached
notification -> `0025DF00` resumption. See [the connected specification](the-actor-request-from-arming-through-start-and-return.md).

- The issuer gate at `002689F0/002689F7` uses R15 (issuer). RBX is the resolved target. Swapping
  their class/counter values discriminates this; same-actor immediate submission skips reselection.
- Request mode1 posts no start/end notification. Mode2 posts at selection/start, BEFORE the callee
  bytecode runs; mode3 posts when the original remover handles the callee's return. The descriptor
  for either notification has mode4 and is filed on the requester's detached list.
- `REQSW` (24) resumes after start; `REQEW` (27) waits for return. The selected original interpreter
  and driver run on both actors. A kind4 notification matches current channel and low32
  continuation PC minus actor bytecode base; finding and removing it resumes in the SAME driver
  invocation under the tested scheduling gates. No extra-frame guarantee exists.
- Notification allocation can fail when the requester has no free entry. Both producers ignore
  that return; target start/return can complete while the caller remains waiting in this fixture.
  Actual shipped capacity, higher recovery, callback reachability and scheduling remain open.
- Admission kind0 refuses an occupied channel, kind2 allows another entry, and kind4 rejects an
  already-present ID on the selected channel. Refused candidates return to the free list.
- The insert clamps high channels to `count-1`; the submitter's separate actor+26 bookkeeping
  uses the original channel. The tested out-of-domain channel7 produces entry channel2/bit2
  but sets bookkeeping bit7. Valid authored channel bounds are still a precondition.
- Core request reset clears only +00..+16. Scratch +18..+27 survives until its owning operation
  writes it; starting one channel leaves the other request slots intact.

The 139 named assertions and eight targeted variants are bounded isolated original-code evidence,
not a live game, full opcode census or independent acceptance. Earlier audit receipts are history;
this correction reopens the mechanism pending review rather than silently retaining AUDITED.

*Reconciled 2026-09-30 (SWE2-CONTRACT, cited).* **The review is done:** SWE2-AUDIT-SEM re-executed
`continuation-section12-actor-request-waits/run_review.py` non-author (139 assertions, an identical repeat, 8 mutants
rejected, 85 original bodies and 8 data spans verified) and byte-verified `003DB6E0`, returning `verdict:ACCEPT`
(`FRONTIER-REVIEW-AUDITSEM-OV-ACCEPTANCE-0929`, record `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-ov-acceptance.md`,
OV-12, whose acceptance item the carrier `FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929` closed). **The four open
bullets have homes:** notification capacity and recovery are OV-10 — the authored bounds and the recovery policy are
answered there (both producers ignore the allocation return), and whether shipped play ever exhausts a pool stays on
OV-10; scheduling, reentrancy and the native wait services are OV-11 (answered; in-frame order on the field-pass page);
callback reachability is the same question as OV-10's pool exhaustion.
