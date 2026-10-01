---
system: The field runtime pass — how one frame drives every actor's script
category: 04-Actor-Entity
status: DOCUMENTED — the SECTION-12 wait-completion polarity correction that reopened the page is accepted non-author (SWE2-AUDIT-SEM OV-ACCEPTANCE-0929; FABLE's semantic review, A12-6) and survived a non-author falsification pass (2026-10-01, SWE2-CONTRACT for OPUS; one adjacent sentence corrected, the steering mode); the wait slot's `+0x27` is never read as a settled flag (GR-1) (owner re-status 2026-10-01, OPUS).
owner_layer: CodeDomain — ActorEntity
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `0024B9B0` (interior read 2026-09-17, SWE2-FRONTIER: 1,500 B — `00181DD0` first at [`0024BA57`](../_index/ADDRESS-INDEX.md), `0024C060` ×4 + `003A7EE0` ×3 + `003A74F0`/`003A7300` ×2), which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-03
audit:
  passes: 2
  last_pass: 2026-10-01
  last_pass_kind: falsification
  last_pass_state: swe2contract-wait-polarity-falsification-pass-2
  crossref_clean: true
  reopened_count: 1
---

# The field runtime pass — how one frame drives every actor's script

`ActorManager_RunFieldRuntimePass` (`0025D9E0`, 1,297 B) was on the *leaned on and never opened* cut:
**four documents cited it, all at its entry.** Every one of them cites it from a call chain or an
ownership table — *"runs the transaction, does not own weather"*, *"a per-frame field pass: it drives
audio and asks who the party focus is"*. **Its role was known from the call graph and its body had
never been read.** This document reads it.

**Extent checked first**: 364 instructions, ends `ret` at `0025DEF0`, **no `jmp` leaves the extent**.

## 1. What the player sees

Every actor in the field — the townspeople, the doors, the cutscene triggers — runs a small script,
and this is the function that runs them, once per frame. ~~**The detail that matters is that an actor's
script is not advanced one step per frame: it is driven repeatedly within the same frame until it
either finishes or blocks.** That is why a scripted event can start, run through several statements
and reach a wait all in the frame you triggered it.~~ **Each actor is visited once by each pass over the
actors that includes it** — usually once a frame, more often when the game asks for extra simulation
steps in a frame. When a visit finds that what an actor's script was waiting for has finished, the
script carries on in that same visit instead of waiting for the next frame.

*Corrected 2026-09-30 (FABLE): the struck sentences restated the drive loop as §4 first read it. §4's
2026-09-12 correction shows the inner repeat never runs, and §11 (SECTION-12) shows that the same-visit
continuation comes from the wait resolver.*

## 2. The per-slot state block

```asm
0025D9EF  lea   rdi, [rip + 0x1e3b41a]     ; -> 02098E10
0025D9F6  imul  rbx, r14, 0x288            ; slot * 648
0025D9FD  add   rbx, rdi
```

**The argument is a slot index, and each slot owns a `0x288` = 648-byte block based at
`02098E10`.** Everything below is relative to that block.

**The first thing the function does is refuse to run during a save:**

```asm
0025DA00  call  SaveWrite_GetBusyFlag
0025DA05  test  eax, eax
0025DA07  jne   <return 1>
```

**A non-zero busy flag stops the entire field pass**, and the function still returns `1` — success —
so a caller cannot distinguish "ran" from "declined" by the return value alone.

> **`SaveWrite_GetBusyFlag` (`00583920`) is seven bytes and reads one global**:
> `00583920 mov eax, dword ptr [rip + 0x27260c2]` → **`02CA99E8`**, then `ret`. That is the whole
> function. **So what is read here is "a global is non-zero", not "a save is in progress"** — the
> save meaning comes from the ledger name and from whoever writes `02CA99E8`, which this document
> has not read. (Pointer 2026-10-01 (SWE2-CONTRACT for OPUS): read since 2026-09-11; the next paragraph reads the writers.) The pass's behaviour is established; the trigger's identity is borrowed.
>
> **Read 2026-09-11:** three writers, all in the save-write operation. `SaveWrite_PrepareAndSubmitFullImage`
> (`0057E310`) sets it to 1 after handing the image to the write submission (`0057E495`);
> `SaveWrite_OperationStateCallback` (`0057E4D0`) sets it to 1 before driving `FUN_00583fd0`
> (`0057E559`) and to 0 on the completion branch (`0057E58B`). So the name holds: the global is
> non-zero from the start of a save write until its completion event ([the save-image page](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md) §5).

Immediately after, a bit is copied between two flag bytes:

```asm
0025DA09  and   byte ptr [rbx + 0x11], 0xfe
0025DA0D  movzx ecx, byte ptr [rbx + 0x10]
0025DA14  shr   al, 7
0025DA17  or    byte ptr [rbx + 0x11], al     ; +0x11 bit 0  <-  +0x10 bit 7
```

**Bit 7 of `+0x10` is republished as bit 0 of `+0x11` every frame**, so the two bytes are not
independent and a reader who samples only one of them sees a stale copy of the other.

## 3. Two globals the rest of the frame reads

```asm
0025DAB3  mov   qword ptr [rip + …], rbx     ; -> 02099D70   the slot block
0025DABA  mov   qword ptr [rip + …], rax     ; -> 02099D78   the focus actor's registry entry
```

`rax` here is `ActorHandle_ResolveRegistryEntryByPackedId` (`003588B0`) applied to
`PartyFocus_GetCurrentPackedActorHandle` (`003590D0`), or **null when there is no focus** — the null
case is taken from `rdi`, which was zeroed. **So `02099D78` is legitimately null on frames with no
party focus**, and anything reading it must handle that rather than assume a pass implies a focus.

**Null arrives two ways, not one.** Besides the caller's zeroed `rdi`, the resolver has **two null
returns of its own** — `003588B8 xor eax, eax; ret` and `00358933 xor eax, eax; ret` — so a packed
handle that does not resolve produces the same published null as no focus at all. **A reader of
`02099D78` cannot tell the two apart.**

The handle source is seven bytes and reads one global: `003590D0 mov eax, dword ptr [rip + 0x1f6ef0a]`
→ **`022C7FE0`**, then `ret`.

## 4. The actor drive loop — the finding

```asm
0025DB35  call  ActorManager_GetRecordByOrdinal(slot, word [slot.payload + 0x50])
0025DB43  call  WorldActor_UpdateRuntimeAndScriptExecutionState(slot, record)
0025DB48  movzx ecx, byte ptr [rdi + 0x14]
0025DB4C  test  cl, 0x40
0025DB4F  jne   done                     ; settled -> stop
0025DB51  test  cl, 0xf
0025DB54  je    done                     ; nothing pending -> stop
0025DB5D  call  0x3db280
0025DB68  call  WorldActor_UpdateRuntimeAndScriptExecutionState   ; again, same frame
0025DB6D  movzx ecx, byte ptr [rdi + 0x14]
0025DB71  test  cl, 0x40
0025DB74  je    0x25db51                  ; loop
```

*Corrected 2026-09-30 (FABLE): the first line read `ActorManager_GetRecordByOrdinal(actor, word [actor + 0x50])`.
Both arguments come from the slot. `rcx` is the slot block (`0025DB22`), and the ordinal is the word at `+0x50` of the
slot's bound definition payload `[slot + 0x00]` (`0025DB2B`–`0025DB31`). This first drive runs only when the slot's
`+0x12` byte is non-zero (`0025DB25`). It drives that one designated record, clears `+0x12` (`0025DB79`), runs
`002620E0` and jumps to the pass's tail (`0025DB82`). The other call sites of `0025DF00` are listed in §6.*

> **One actor is driven repeatedly inside one frame until it settles.** The loop exits on bit `0x40`
> of the record's `+0x14` — *settled* — or on the low nibble being clear — *nothing pending*.
> **There is no iteration cap.** A script that keeps work pending and never sets `0x40` has nothing in
> this function to stop it.

`byte +0x14` of an actor record is therefore a **status byte with two independent halves**: bit `0x40`
is the settled flag, and bits `0x0F` are a pending-work count or mask. Both are tested here in the
same instruction stream.

> **Corrected 2026-09-12 (FABLE): nothing ever sets the low nibble, so the inner loop is dead code.**
> Every write to a byte at displacement `+0x14` in the image was listed (80 sites); the ones whose
> base is the actor record are `ActorStorage_InitializeRecord` (`002665D7`: `flags & 0xB0 | 0x30`,
> on memory the allocator zeroed), the sequence binder `00266BD0` (`|= 0x80`, sequences 5 and 7),
> `ActorSystem_BindBattleUnitsForEligibleRecords` (`00265B13`: `& 0xEF`), `0026B8E0` (`& 0xCF | 0x40`
> over every record of a slot), `ActorResource_SelectPendingEntryForExecution` and the interpreter
> (bit 6 only). No word or dword store covers the byte. The `= 1`, `= 3`, `= 4`, `= 5` and
> `= 0x0106` stores the same sweep finds are the **wait slot's** `+0x14` (§11's trap), and the
> `= 0` / `= 1` at `0026C410` / `0026C606` are the manager record's. So bits 0–3 are zero for the
> life of every record, `test cl, 0xF` at `0025DB51` never passes, and `0025DB5A`–`0025DB74` never
> runs in the shipped build: **each actor is driven once per loop that names it.** The control is
> the sweep itself, which lists every writer the census knew.
>
> **Cross-checked 2026-09-17 against the image-wide byte-range writer census**
> (`Actor-Storage-Record/actor-storage-record-flag-bit-writes.tsv`): the sweep above could miss a
> store whose width reaches `+0x14` from a lower displacement, and the route-proven access census
> never reaches the constructor at all. The census closes both — `00266530`'s only `+0x14` writes
> are `& 0x7F` (`00266573`) and `(old & 0xB0) | 0x30` (`002665D7`), and every other
> `+0x14`-covering store in a proven function attributes to a non-record base: the wait slot
> (`0025DF00` / `0025E4C0` on `rsi`), the `0x28`-stride resource entries off `+0xA8`
> (`0025B45B`, `003DBE0C`, `002667FD`), the secondary context (`002E4A29` via `[rcx+0xB8]`), the
> `0x70`-stride array at `02B58C50` (`003DE626`), a global `0x2A0`-stride table (`00225E30`).
> What the byte carries instead:
> | bit | set | cleared | meaning |
> |---|---|---|---|
> | 4 (`0x10`) | at init (`0x30`) | when the battle-unit pool is full (`00265B11`, count ≥ 32); by `0026B8E0` | **drive the bound battle unit**: `0025DF00` calls the pointer at record `+0x38` — `BattleUnit_UpdateLifecycleAndCombatFrame` (`00233F70`), planted at `00265AA8` — once per pass while the bit is set and the record is idle-eligible (`0025E1FC`–`0025E222`) |
> | 5 (`0x20`) | at init (`0x30`) | by `0026B8E0` | tested by seven readers (`0025B29A`, `0025B919`, `0025BA2D`, `0025C1C0`, `0025C1FB`, `0026760E`, `003DF709`); ~~meaning not read~~ **the actor entry's script enable flag** — `FRP-1`, ANSWERED 2026-09-18 (FABLE): its only writer is an unlisted 24-byte setter behind script verbs `001E enable` / `001F disable` ([the contract](CONTRACT-field-runtime-pass.md), open item 1; cited here 2026-09-30, FABLE) |
> | 6 (`0x40`) | the interpreter (`0025E5EA`), the entry selector (`003DB77E`), `0026B8E0` | the entry selector (`003DB774`) | **idle / settled** — what this loop and the two AND-folds test |
> | 7 (`0x80`) | the sequence binder (`00266C1F` / `00266C24`) | init (`00266573`, before the binder) | **battle-unit eligible**: `00265A89` binds a unit only when the byte is `≥ 0x80` |

## 5. Four loops, three shapes

| loop | bound | what it accumulates |
|---|---|---|
| the drive loop above | **none** | — |
| `0025DC61`–`0025DCCF` | `cmp r15d, 4` with `rol ebp, 1` | a **four-iteration pass with a rotating single-bit mask** |
| `0025DD10`–`0025DD67` | `cmp edi, dword ptr [rbx + 0x20]` | `r12d &= record[+0x14]` |
| `0025DE80`–`0025DEB1` | `cmp edi, dword ptr [rbx + 0x20]` | `r12d &= record[+0x14] >> 6` |

**`[rbx + 0x20]` is the slot's actor count**, and **two separate passes fold every actor's `+0x14`
into a running AND** — the second shifting right by 6 first, so it is asking **"is bit `0x40` set on
*every* actor"**. That is a whole-field settled test, computed by conjunction rather than by a counter.

**The four-iteration rotating-mask loop is the same idiom as the gambit config's enable mask** — a bit
per slot walked with `rol` — but over a different structure; **no connection between the two is
claimed.** *Identified 2026-09-12:* the structure is the **party roster** — the four
`ActorStorageRecord*` at `0209A1F0` (`lea r13, [0209A1F0]` at `0025DC4D`, `+8` per iteration;
[the party-slot contract](../11-Party/CONTRACT-party-slot-assignment.md)). For each occupied slot the loop drives the member (`0025DC98`–`0025DCA7`), folds its
settled bit into `r12d`, and collects into `r14d` the members whose `+0x10` status byte is zero
(`0025DC92`–`0025DCBF`); on manager slot 0 it also arms a member whose `+8` bit 6 is clear
(`00269860(record, 1)`, `0025DC70`–`0025DC8E`, unless slot `+0x17` bit 2). When all four bits are
collected (`cmp r14d, 0xF`) the slot's `+0x200` bit 1 is cleared and, on slot 0, `00233AA0` runs
(`0025DCDB`–`0025DCED`).

## 6. Call chain

```
World_UpdateSimulationTick 00314020          the only caller (§12): slots 0-4 in mode 0, slots 3-4 in mode 1
 -> ActorManager_RunFieldRuntimePass 0025D9E0 (slot)
  SaveWrite_GetBusyFlag 00583920             -> busy: return 1, do nothing
  PartyFocus_GetCurrentPackedActorHandle 003590D0
    -> ActorHandle_ResolveRegistryEntryByPackedId 003588B0  -> published to 02099D78 (may be null)
  ActorManager_GetRecordByOrdinal 00358940
  WorldActor_UpdateRuntimeAndScriptExecutionState 0025DF00   x5 call sites: 0025DB43 the designated record (§4),
                                                             0025DB68 the dead repeat (§4), 0025DCA7 the roster loop,
                                                             0025DD51 and 0025DE93 the two all-actor loops (§5)
       -> ActorResource_FindActiveEntryByIdOrClass 003DBF60
       -> ActorResource_IsChannelBitActive 003DB640
       -> ScriptVM_WaitList_HasAnyActorChannelActive 00267420
       -> ActorResource_FindScriptRequestEntry 003DC050
       -> ActorResource_RemoveActiveEntry 003DB2A0     (blocked path only)
  002620E0  field-runtime init core
  00261F90  (Audio, 335 B)
  WorldTransition_GetActiveOrPendingFieldId 003148F0 / SaveImage_GetPersistentPayloadBase 002EF2B0
  WorldSimulation_ProcessDeferredModeRequest 0032FC30 (mode 0xD4)
```

**49 distinct callees over 59 call sites.** *Recounted 2026-09-30 (FABLE) with capstone over the whole 1,297-byte
body (364 instructions, `ret` at `0025DEF0`): 59 direct `call` sites, 49 distinct targets, no indirect call and no
jump leaving the extent. `0025DF00` is called 5 times, `00358940` 3 times, and `002620E0` and `002EF2B0` twice each,
as are two callees this page does not name.*

**Upstream (who causes this):** `World_UpdateSimulationTick` (`00314020`) is the only caller. It runs the pass once
per slot per sub-step: slots 0–4 on the mode-0 path and slots 3 and 4 on the mode-1 path (§12).

**Downstream (what this causes):** each visited record goes through the wait resolver `0025DF00`. That resolver
may run the bytecode interpreter `0025E4C0` (§11) and, for an eligible record with bit 4 set, the bound battle unit's
frame `00233F70` (§4). Slot 0 may also issue the deferred resource-set request `0032FC30` (§8). The pass also runs the
area-music select `00261F90` and the init core `002620E0`.

**Do not confuse with:** the wait slot's `+0x14`, which is an eight-case wait-kind enum on a different object
reached through the same record (§11, the falsification pass).

## 6a. Key addresses (FABLE, 2026-09-30)

Addresses are Ghidra image base `0x00120000`. Body sizes are the function extents from `functions.tsv`, read
2026-09-30 (FABLE).

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0025D9E0` | `ActorManager_RunFieldRuntimePass` | 1,297 B | this page: one manager slot's field pass |
| `00314020` | `World_UpdateSimulationTick` | 845 B | the only caller; runs the pass per slot (§12) |
| `00583920` | `SaveWrite_GetBusyFlag` | 7 B | the save-write busy flag; non-zero stops the pass (§2) |
| `003590D0` | `PartyFocus_GetCurrentPackedActorHandle` | 7 B | the party focus handle the pass resolves (§3) |
| `003588B0` | `ActorHandle_ResolveRegistryEntryByPackedId` | 143 B | handle to registry entry, published to `02099D78` (§3) |
| `00358940` | `ActorManager_GetRecordByOrdinal` | 30 B | the slot's record pool lookup (§12) |
| `0025DF00` | `WorldActor_UpdateRuntimeAndScriptExecutionState` | 1,228 B | the wait resolver each visit runs (§11) |
| `0025E4C0` | `WorldActorScriptVM_InterpretBytecode` | 14,646 B | the bytecode interpreter the resolver's kind-1/2 arm runs (§11) |
| `00233F70` | `BattleUnit_UpdateLifecycleAndCombatFrame` | 467 B | the `+0x38` callback that record bit 4 gates (§4) |
| `002620E0` | field-runtime init core | 231 B | called after the designated-record drive and before the roster loop (§4, §6) |
| `00261F90` | area-music select | 335 B | picks and starts the area's music (Audio crossing) |
| `0032FC30` | `WorldSimulation_ProcessDeferredModeRequest` | 110 B | the slot-0 `0xD4` resource-set request (§8) |
| `00377DB0` | WorldAreaField word getter | 7 B | reads `02ADD0D8`; gates the slot-0 request (§8) |
| `00233AA0` | default-focus request | 41 B | run on slot 0 once all four roster bits are collected (§5) |
| `00264640` | `table256` reader | 40 B | slot 0 `+0x48`, index `< 0x100` (§12) |
| `0026ABA0` | `table256` writer | 38 B | slot 0 `+0x48`, index `< 0x100` (§12 Limits) |
| `0026B730` | `table256` entry-0 writer | 25 B | slot 0 `+0x48`, entry 0 only (§12 Limits) |
| `00264D20` | `table64` reader | 37 B | slot 0 `+0x58`, index `< 0x40` (§12) |
| `0026ADC0` | `table64` writer | 35 B | slot 0 `+0x58`, index `< 0x40` (§12) |
| `00264800` | `table32` reader | 37 B | slot 0 `+0x60`, index `< 0x20` (§12 Limits) |
| `0026AD10` | `table32` writer | 35 B | slot 0 `+0x60`, index `< 0x20` (§12) |
| `00266530` | `ActorStorage_InitializeRecord` | 1,439 B | sets record `+0x14` to `(old & 0xB0) \| 0x30` at init (§4) |
| `0026B8E0` | record flag reset | 96 B | `& 0xCF \| 0x40` on every record of a slot (§4) |
| `003DBF60` | `ActorResource_FindActiveEntryByIdOrClass` | 226 B | wait kind 3's predicate (§11) |
| `003DC050` | `ActorResource_FindScriptRequestEntry` | 121 B | wait kind 4's reader (§11) |
| `003DB2A0` | `ActorResource_RemoveActiveEntry` | 378 B | kind 4's removal of the matched notification (§11) |
| `002674B0` | `ScriptVM_WaitList_HasAnyActorResourceEntryActive` | 166 B | wait kind 5's ordered list (§11) |
| `003DB640` | `ActorResource_IsChannelBitActive` | 13 B | wait kind 6's predicate (§11) |
| `00267420` | `ScriptVM_WaitList_HasAnyActorChannelActive` | 132 B | wait kind 7's ordered list (§11) |
| `001EDE80` | half-rate step count | 61 B | the resolver's loop-head gate (§11, the `001EDE80` update) |

### Data addresses cited by this document (FABLE, 2026-09-30)

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02098E10` | manager slot array | `.data`, 5 × `0x288` | the five `ActorManagerSlot` blocks (§2, §12) |
| `02098E20` | slot 0 `+0x10` | byte | slot 0's status bits; bit 0 gates the four table accessors (§12) |
| `02099D70` | current slot | qword | the slot block this pass publishes (§3) |
| `02099D78` | focus registry entry | qword | the party focus actor's registry entry, may be null (§3) |
| `02CA99E8` | save-write busy flag | dword | read by `SaveWrite_GetBusyFlag` (§2) |
| `022C7FE0` | focus handle | dword | read by `PartyFocus_GetCurrentPackedActorHandle` (§3) |
| `0209A1F0` | party roster | 4 × qword | the four `ActorStorageRecord*` the roster loop walks (§5) |
| `02ADD0D8` | WorldAreaField word | dword | the slot-0 request gate (§8) |
| `022C7F88` | per-step flag | dword | cleared before an interpreter step, read after (§11, the `0025DF00` subtree) |

## 7. Modding notes

- **Hook `WorldActor_UpdateRuntimeAndScriptExecutionState` and you will be called several times per
  actor per frame**, not once — once from each loop that names the actor (§5), never from the
  drive loop's inner repeat, which is dead (§4). A hook that assumes one call per frame will
  over- or under-count.
- **Nothing runs while a save is in flight**, and the pass reports success anyway.
- **`02099D78` can be null.** It is the focus actor's registry entry, resolved fresh each pass.
- **`+0x10` bit 7 and `+0x11` bit 0 are the same flag**, republished every frame.

## 8. What is not known

- [x] ~~**How many slots exist.**~~ **ANSWERED 2026-09-10 — five, and the caller is traced.**
      See §12.
- [x] ~~What the `+0x14` low nibble counts. It gates the drive loop and is folded by two later passes;
      its unit is not established.~~ **ANSWERED 2026-09-12 (FABLE):** nothing — no instruction in the
      image sets bits 0–3 of the record's `+0x14`, so the nibble is zero for the record's life and the
      inner repeat is dead code; the byte's live bits are 4–7 (§4, corrected).
- [x] ~~What the four-iteration rotating-mask loop indexes.~~ **ANSWERED 2026-09-12:** the four-entry
      party roster at `0209A1F0` (§5).
- [x] ~~What `0032FC30`'s mode `0xD4` requests.~~ **ANSWERED 2026-09-12 (FABLE), at the mechanism
      level:** `WorldSimulation_ProcessDeferredModeRequest(slot, index)` is a **manager resource-set
      load** — for slot 0 it first refreshes the area ARD for the map-reference field
      (`AreaArd_RefreshForMapRefField`, `0032FC42`) and, unless the loader is in state 1 / 3, runs the
      per-map driver `003319D0(index)`; then `ActorResource_BeginManagerResourceSetLoad(slot, index)`
      requests the manager's `.ebp` / `.mot` / `.fpk` triple through `ResourcePath_Get` — namespace 5,
      row `index × 3` for slot 0 ([the EBP container page](../25-EBP-Script-Container/Container/ebp2-container.md) §"which resource namespace") — and `0025D4D0`
      clears the manager slot's `+0x10` bit 1. The runtime pass issues it **once for slot 0 with
      index `0xD4` = 212** (`0025DACC`–`0025DAF2`): when `00377DB0()` — the WorldAreaField word
      `02ADD0D8`, written by `003775D0` (= 1), `00377CC0` and `00378230` — is non-zero and slot 0's
      `+0x10` bit 4 is clear, it requests map 212's set and latches bit 3 so it is not repeated.
      ~~Which map row 636 of namespace 5 names is not in the image: the path tables at `0215F000` are
      built at boot ([the area nmb index](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md) §"ResourcePath_Get"), so the stem stays unread here.~~
      **`FRP-2` ANSWERED 2026-09-22 (FABLE): row 636 names NOTHING — and the tables are readable
      after all.** They are built at boot, but from **`lea` constants in `002DF9A0`**, so every array
      is a link-time address and its contents are static. `002DF9A0` installs **ten** arrays at
      namespace 5 (`0215F028`), one per language — `us`, `fr`, `de`, `it`, `es`, `uk`, `kr`, `cn`,
      `ch`, `in`. **In all ten, rows 636, 637 and 638 are three NULL pointers**, so map 212's
      `.ebp`/`.mot`/`.fpk` triple is unauthored. *It is not an out-of-bounds read:* the same arrays
      carry non-NULL entries far above it — at least **2,127** non-NULL rows with the highest
      populated map index **1,311** — so 636 sits inside the populated region and the NULL is an
      authored absence. **The `× 3` triple is proved rather than assumed**: rows 0/1/2 read
      `tst_a01.ebp`, `tst_a01.mot`, `tst_a01.fpk` — one stem, three extensions. With `AB-2` (the
      resolver validates nothing and null-tests nothing), the once-per-run slot-0 request returns a
      **NULL path for all three**.
- [x] ~~Whether the drive loop can be made to spin.~~ **ANSWERED 2026-09-12:** it cannot — the repeat
      needs the low nibble, which nothing sets (§4); and one call of `0025DF00` dispatches at most
      twice (a settled wait re-enters the dispatch with `waitKind = 1`; the interpreter arm exits,
      `0025E11E`–`0025E12B`). Whatever bound the bytecode step itself has is [the interpreter page](../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)'s matter.
- [x] **Whether anything reads the wait slot's `+0x27` settled byte.** Wait kinds 3, 6 and 7 set it and the
      interpreter clears it when it arms a wait, but no reader was found (§11). Registered as `GR-1`
      (2026-09-30, FABLE). *(Answered 2026-09-30 (OPUS `72657b7ca`); register row GR-1, record [`gr1-wait-slot-settled-0930`](../_index/candidates/gr1-wait-slot-settled-0930/README.md): nothing reads `+0x27` as the settled flag. The interpreter clears it when it arms the next wait, and otherwise the next native command that uses the byte overwrites it before any read: the slot's `+0x18`-`+0x27` doubles as the native-command scratch window, `r8` = slot + 0x18.)*

## 9. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Slot block base and stride | `lea rdi, [→02098E10]`, `imul rbx, r14, 0x288` at `0025D9EF` | 1 |
| The save-busy early exit returns 1 | `0025DA00`–`0025DA4C` | 1 |
| `+0x11` bit 0 is republished from `+0x10` bit 7 | `0025DA09`–`0025DA17` | 1 |
| Two globals published per pass, one nullable | `0025DAB3`, `0025DABA`, with the null path at `0025DAA7` | 1 |
| The drive loop and its two exit conditions | `0025DB43`–`0025DB74`, complete | 1 |
| `[rbx+0x20]` is the actor count, folded by AND twice | `0025DD64` and `0025DEAE`, both `cmp edi, [rbx+0x20]` | 1 |
| No iteration cap on the drive loop | complete decode of the loop body; no counter is incremented or compared | 1 |
| Bits 0–3 of the record's `+0x14` are never written | every byte write at displacement `+0x14` in `.text` listed (80 sites, `dispscan`), every word / dword write at `+0x12`–`+0x14` listed, each attributed to its base structure; the control is that the sweep names all five census writers; extended 2026-09-17 by the byte-range writer census (`Actor-Storage-Record/actor-storage-record-flag-bit-writes.tsv`), which additionally covers wide stores from lower displacements and the route-invisible constructor `00266530` — see §4 | 1 |
| Bit 4 gates the `+0x38` callback, which is `BattleUnit_UpdateLifecycleAndCombatFrame` | `0025E1FC`–`0025E222`; `lea r13, [00233F70]` at `00265A4F` and the store at `00265AA8`; `00265B11` | 1 |
| The four-iteration loop walks the party roster | `lea r13, [0209A1F0]` at `0025DC4D`, `add r13, 8` at `0025DCC7` | 1 |
| One `0025DF00` call dispatches at most twice | the jump table `0025E3CC` (8 arms), the five settle arms' back-edges to `0025DFA0`, the interpreter arm's exit | 1 |
| The pass makes 59 direct calls to 49 distinct targets, with no indirect call | capstone over the whole 1,297-byte body of `0025D9E0` (364 instructions, `ret` at `0025DEF0`), 2026-09-30 (FABLE) | 1 |
| The five `0025DF00` call sites, and the first drives one designated record only while slot `+0x12` is set | `0025DB43`, `0025DB68`, `0025DCA7`, `0025DD51`, `0025DE93`; `0025DB22`–`0025DB82` | 1 |
| The tick runs slots 0–4 on the mode-0 path and slots 3–4 on the mode-1 path, with no extra slot-3 call | `00314103`–`0031413C` (`mov ebx, ebp` with `ebp = 3`, `inc ebx`, `cmp ebx, 5`) and `003141C0`–`00314222` | 1 |
| Wait kinds 3, 6 and 7 set the wait slot's `+0x27` | `0025E04F`; `0025E07A`, reached by kind 6 and by kind 7 through `jmp 0x25e06e` at `0025E08F`; the eight-entry table at `0025E3CC` decoded 2026-09-30 (FABLE) | 1 |
| `table256` has two writers and `table32` a reader | `0026ABA0` (`0026ABC0 mov word [r8+rax*2], dx`), `0026B730` (`0026B745 mov word [rax], cx`), `00264800` (`0026481D movzx eax, word [rdx+rax*2]`); a RIP-relative sweep of the whole slot array for `+0x08`, `+0x48` and `+0x60` finds six functions, all on slot 0, and none for `+0x08` | 1 |
| Who fills `recordPool` and the three table pointers | in `ActorSystem_InitializeManagerRuntime`, `mov qword ptr [rbx + 8], rax` directly after `call ActorStorage_AllocateAndInitializeRecords` (`rbx` = the slot); in `ActorManager_BindLoadedDefinitionPayload`, `mov qword ptr [rdi + 0x48], rax` directly after `call SaveImage_GetPersistentPayloadBase` (`rdi` = the slot); `+0x58` / `+0x60` from [the field map](Actor-Manager-Record/the-actor-manager-record-field-map.md) §2.2 and FH-2 | 1 |
| `001EDE80`'s open path adds two seven-byte reads | `0022A080` reads `02064AD8`, `0022A030` reads `02064AA8`, and nothing else | 1 |

**Controls.** The absence claim is *"no iteration cap"*. The same reading positively identifies the
caps on the other three loops — `cmp r15d, 4` and two `cmp edi, [rbx+0x20]` — so the drive loop's
absence of one is a measurement rather than a missed comparison.

## 10. Related

- [`../03-World-Area-Field/Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md`](../03-World-Area-Field/Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md)
  — where this function is cited as the transaction runner
- [`../03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md`](../03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md)
  — the cross-owner call table that names its Audio and Party callees

## 11. `0025DF00` opened — the wait resolver between the drive loop and the interpreter

~~Section 4 established that this function is driven repeatedly inside one frame.~~ Section 4 first read this
function as driven repeatedly inside one frame. Its 2026-09-12 correction shows that each loop of the pass drives
it once. *(Corrected 2026-09-30, FABLE.)* **Citing it put it on
the *leaned on and never opened* cut**, where it sat with three other documents citing it — the
ScriptVM interpreter document, which records it as *"the interpreter's **exactly one** ledger caller"*,
a movement call chain, and a cutscene document that read it only far enough to see it *"gates the
script stop marker"*. **Four narrow purposes, no reading of the body.** It is read here.

**Extent checked**: 329 instructions, ends `ret` at `0025E3CB`, **no `jmp` leaves the extent**.

### The chain, end to end

```
ActorManager_RunFieldRuntimePass 0025D9E0     drives each actor once per loop that names it (§4, corrected)
  -> WorldActor_UpdateRuntimeAndScriptExecutionState 0025DF00    decides whether it MAY run
       -> WorldActorScriptVM_InterpretBytecode 0025E4C0          runs it
```

**This is the middle piece, and it is a wait resolver.** Arguments are `rcx` = the slot block and
`rdx` = the actor record (`rdi` throughout the body).

### Wait completion polarity — corrected by original execution, SECTION-12 (2026-09-24)

The older paragraph mislabeled `0025E127` as a proceed path. **It is the blocked/no-interpreter
exit**, setting request+16. `0025E0BE` is the interpreter arm. Setting waitKind=1 and jumping back
to `0025DFA0` can enter the interpreter in the SAME invocation; it is not an extra-frame delay.

| Wait kind | Actual predicate | Holds the wait when | Completes when | request+27 |
|---|---|---|---|---|
| 0 or >=8 | no interpreter arm | selected by dispatch | no completion inferred | unchanged |
| 1 or 2 | original interpreter | interpreter-dependent | interpreter-dependent | interpreter-dependent |
| 3 | `003DBF60` entry lookup | matching entry exists, including queued state1 | absent (`0xFF`) | set1 |
| 4 | `003DC050` detached notification lookup | channel/continuation key absent | matching notification is removed by `003DB2A0` | unchanged |
| 5 | `002674B0` ordered actor/entry list | current cursor finds a matching entry | cursor reaches end / resolved list absent | unchanged |
| 6 | `003DB640` channel bit | selected bit remains set | selected bit clear | set1 |
| 7 | `00267420` ordered actor/channel list | current cursor finds selected channel active | cursor reaches end / resolved list absent | set1 |

For kinds3/5/6/7 an active dependency BLOCKS. For kind4 an existing matching completion notification
RELEASES the wait. `003DC050` is a reader; the caller removes the notification before retrying
with kind1. The earlier purported polarity correction had mistaken the destination of the branch.

Kinds5/7 keep a WORD cursor at request+22. They skip satisfied entries and stop at the first active
one; later polls begin at that cursor, not index0. A previously passed actor can become active
without being rechecked. This is an ordered progress list, not a simultaneous all-actors barrier.

Original `REQSW` -> selection/start -> notification and `REQEW` -> original RET/removal ->
notification are exercised with two actors. Receipt capacity failure does not roll back the
callee: the producer ignores the insertion result. This is a tested missing-notification boundary,
not proof of a deadlock in ordinary gameplay.

[SECTION-12 evidence](../_experiments/evidence/continuation-section12-actor-request-waits/REVIEW.md)
and [the connected mechanism](../01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md)
include the exact unchanged original bodies, synthetic inputs, 139 assertions, repeat and eight
falsifiers. The full `0025DF00` entry runs; `0025D9E0` and nonempty outer services do not.

### A same-displacement trap, and it is not the one section 4 describes

**`[rsi + 0x14]` in this function is not the actor record's `+0x14`.**

```asm
0025DFC6  lea   rsi, [rax + rcx*8]     ; an element of an array — NOT the record
```

`rsi` is a **wait-slot entry**; `rdi` is the actor record. Both are read at `+0x14` in the same
function:

| base | `+0x14` used as |
|---|---|
| `rsi` — a wait slot | written `= 1` at **four** sites, at completing transitions, not as a generic blocked marker |
| `rdi` — the actor record | tested `& 0x40` twice and `& 0x10` once |

**This is the `+0x24`-on-two-bases species again, in a function I reached by following my own
citation** — and the near-miss was mine: the four `= 1` writes are the obvious candidate for "what
sets the pending bit section 4 tests", and they are a different structure.

### A refinement to section 4

Section 4 reads the record's `+0x14` as **bit `0x40` settled** and **bits `0x0F` pending**, which is
what the *caller* tests. This function tests the same byte with **`0x40` and `0x10`** — and `0x10` is
**bit 4, outside the low nibble**. So the byte carries at least three separately-tested regions:

```
bits 0-3   tested as a group by the drive loop
bit  4     tested here, distinct from both
bit  6     the settled flag, tested in both functions
```

**Section 4's reading stands; it was simply not the whole byte.** *(Noted 2026-09-30, FABLE: §4's own 2026-09-12
correction later removed the "pending" half of that reading. Bits 0–3 are tested but never set, and the live bits
are 4–7, as §4's table shows.)*

### What is not established

- [x] ~~What the wait-slot array's element stride is.~~ **ANSWERED** ([the actor record page](Actor-Storage-Record/the-record-behind-every-actor.md) §14, 2026-09-10):
      `0x28` — `rcx = index × 5` at `0025DFBB`, then `× 8`.
- [x] ~~What `[rsi + 0x27]` is, set alongside `+0x14` by two of the four wait kinds but not the others.~~
      **ANSWERED by cross-reference 2026-09-12:** the wait slot's `settled` byte, ~~set only by kinds 3
      and 6 (the same page's kinds table)~~; ~~no reader of it is cited yet.~~
      *Corrected 2026-09-30 (FABLE):* **set to 1 by kinds 3, 6 and 7.** Kind 3 stores it at `0025E04F`. Kind 6 stores it
      at `0025E07A`, and kind 7's arm (`0025E083`) jumps into kind 6's test at `0025E08F` and shares that store. This
      matches the SECTION-12 table above. The interpreter clears it to 0 when it arms a wait (ten sites, `0025F5CC`
      the first). **No reader found:** a byte-width sweep of displacement `0x27` finds no read in `0025DF00`, the
      interpreter or the command lifecycle, and the remaining byte reads at that displacement are on bases not typed
      as wait slots. Registered as `GR-1`. *(Answered 2026-09-30, OPUS `72657b7ca`: never read as a flag; see the section 8 box.)*
- [x] ~~What bit `0x10` of the record's `+0x14` means.~~ **ANSWERED 2026-09-12:** drive the bound
      battle unit — it gates the call through record `+0x38` to `BattleUnit_UpdateLifecycleAndCombatFrame`
      (§4's table).
- [x] ~~What `[r15 + 0x28]` is, compared against `1` and `3` after the interpreter returns.~~
      **ANSWERED 2026-09-12:** `r15` is the manager slot and `+0x28` its index ([the actor-manager record map](Actor-Manager-Record/the-actor-manager-record-field-map.md)). The
      block after a bytecode step that returns 0 (`0025E0DC`–`0025E11E`) parks the wait slot unless
      the step raised `022C7F88` (zeroed by `00357760` before the step, read by `00357770` after) or a
      cutscene-asset exception holds: `001ED130` (the two-case field-id test on `FieldData_GetVariable0`,
      [the cutscene name-slot page](../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)) and then slots 1–2 with flag B (`0020AA30` → `01F832E9`), slot 3 with flag A
      (`0020AA40` → `01F832E8`), or `022C7F84` non-zero. The loop head's `001ED180` / `001EDE80` /
      `001EDDA0` gates are the same page's transition-field and half-rate vetoes.
- [x] ~~The early movement path — a class check `([rdi+3] & 0xE0) == 0x60` guarding a
      `Movement_SetRequestedSpeed` (`0026D6F0`) branch — was not followed.~~ **Read 2026-09-12
      (FABLE):** for a record whose `+0x18` is not 1 and whose byte `+3` carries sequence class 3
      (`0025DF21`–`0025DF47`), `002E4A10` first copies the movement context's position triple
      (`+0`–`+8`) into its `+0x10`–`+0x18` slots; then, when the context's `+0xF0` steering request
      ([the heading-speed page](../06-Movement-And-Navigation/heading-speed-to-position-delta.md) §"the steering request") has a non-zero steering mode at `+0x29`, the pass calls
      `Movement_SetRequestedSpeed(actor, request.+0x7C × [01DFE0BC], mode)` with ~~mode 2 when that
      speed is positive and 0 otherwise~~ mode 0 when that speed is positive and mode 2 when it is zero, negative
      or unordered (`0025DF6F mov r8d, 2`, `comiss xmm2, xmm0` against 0.0, `cmova r8d, ebp` with `ebp` = 0;
      *Corrected 2026-10-01 (SWE2-CONTRACT for OPUS): check W13 of the falsification pass below runs these bytes*) (`0025DF49`–`0025DF83`)
      — the scaled-speed variant inline,
      the scale being the `1.0` at `01DFE0BC`. What the request's `+0x7C` speed is set from is that
      page's matter. (Pointer 2026-10-01 (SWE2-CONTRACT for OPUS): it is the move verb's speed operand, `0026A640`, per [the steering-slots page](../06-Movement-And-Navigation/Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md) field `+0x7C`.)

## 12. The slot count, traced to its caller — and the accessor family that gates on slot 0 (2026-09-10)

§8 left the slot count open because *"the count is the caller's, and no caller was traced"*. There
is exactly one caller, and it answers the question outright.

### Five slots

`World_UpdateSimulationTick` (`00314020`) is the only function that calls
`ActorManager_RunFieldRuntimePass`, from two sites:

```asm
003140FF  lea   ebp, [r13 + 3]          ; r13d = 0 from 003140D9, so ebp = 3
0031411D  call  0025D9E0                ; slots 3 and 4 (ebx = ebp = 3, inc, cmp 5), on the r14d == 1 path only

003141C0  mov   ebx, r13d               ; 0
003141D9  mov   ecx, ebx
003141DB  call  0025D9E0                ; slot ebx
003141E7  inc   ebx
003141E9  cmp   ebx, 5
003141EC  jl    0x3141c3
```

~~**Slots 0–4 every tick, and slot 3 additionally on one conditional path.**~~ **Slots 0–4 on the mode-0 path
(`r14d == 0`, up to sixteen sub-steps), slots 3 and 4 on the mode-1 path (`r14d == 1`) instead of it, and no slot
in any other mode** ([the world tick page](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
§2.2). *Corrected 2026-09-30 (FABLE): the call at `0031411D` sits in a loop, `00314112 mov ebx, ebp` then
`00314130 inc ebx` / `00314132 cmp ebx, 5`, so the mode-1 path runs slots 3 and 4, not one extra slot-3 call. The
annotation on the second line of the block above read "slot 3" before this correction.* So there are **five**
`ActorManagerSlot`s, `0x288` bytes each, a static array at `02098E10`.

**The extent corroborates it independently.** `5 × 0x288 = 0xCA8`, so the array ends at `02099AB8` —
and the next recovered structure, the 64-entry script wait list the bytecode interpreter registers
into, begins at `02099AC0`. A sixth slot would run straight through it.

### Four accessors, one shape, all fail-closed

The three table pointers `FABLE-REQ-OPUS-UNITGROUP` asked about are manager-slot fields, and their
four accessors are the same eleven-instruction template:

| accessor | field | bound | direction |
|---|---|---:|---|
| `00264640` | `+0x48` `table256` | `0x100` | read |
| `00264D20` | `+0x58` `table64` | `0x40` | read |
| `0026ADC0` | `+0x58` `table64` | `0x40` | write |
| `0026AD10` | `+0x60` `table32` | `0x20` | write |

Each one **bounds the index, tests the gate, null-checks the pointer, and only then touches the
table**; every failure returns `0` or does nothing. There is no error signal — a rejected write and
a successful write are indistinguishable to the caller, which is worth knowing before a mod assumes
one landed.

### A correction to the offsets as they were handed over

The request described these as slot 0 `+0x38` / `+0x48` / `+0x50`, *"all gated by slot-0 bit 0"*.
Measured against the base `0025D9EF` actually uses:

| global | as handed over | actual, from `02098E10` |
|---|---|---|
| `02098E58` | `+0x38` | **`+0x48`** |
| `02098E68` | `+0x48` | **`+0x58`** |
| `02098E70` | `+0x50` | **`+0x60`** |
| gate `02098E20` | *"slot-0 bit 0"* | **bit 0 of slot 0 `+0x10`** |

Every one is shifted by `0x10`, which is the tell: the offsets were taken from `02098E20` — the
gate byte — rather than from the slot base. The gate is not the first byte of the slot; it is
`slotFlags` at `+0x10`, the same byte whose bit 7 this pass republishes into `+0x11` (§9).

### And `+0x08` is the record pool

`ActorManager_GetRecordByOrdinal` (`00358940`) is nine instructions and it names the field:

```c
BattleRecord *ActorManager_GetRecordByOrdinal(ActorManagerSlot *m, int ordinal)
{
    char *pool = m->recordPool;                 /* +0x08 */
    if (!pool)                       return NULL;
    if (ordinal < 0)                 return NULL;
    if (ordinal >= *(int*)pool)      return NULL;   /* count is the pool's first dword */
    return ((void**)pool)[1 + ordinal];             /* table starts at pool + 8 */
}
```

That is **exactly** the block `ActorStorage_AllocateAndInitializeRecords` carves (§11 of the
[record page](Actor-Storage-Record/the-record-behind-every-actor.md)): `*(int*)pool = count` and
`((void**)pool)[1 + slot] = p`. The two were recovered independently, from the producer and from
the consumer, and they agree.

### Limits

- **`0x288` is the stride, not a read layout.** Six fields are declared; `0x000`–`0x007`,
  `0x012`–`0x047`, `0x050`–`0x057` and `0x068`–`0x287` are undeclared, which is 614 of 648 bytes.
  *(2026-09-30, FABLE: the slot's layout belongs to
  [the actor-manager record field map](Actor-Manager-Record/the-actor-manager-record-field-map.md), which names far
  more of the block. This page declares only the fields the pass uses.)*
- ~~**No writer was found for `table256` and no reader for `table32`.** Both are single-direction so
  far, which is a statement about what has been read, not about the engine.~~ **Answered 2026-09-30 (FABLE): both
  directions exist, in the same eleven-instruction template.** `table256` is written by `0026ABA0` (38 B, index
  `< 0x100`) and, at entry 0 only, by `0026B730` (25 B), the counterpart of `FieldData_GetVariable0`, which reads
  entry 0. `table32` is read by `00264800` (37 B, index `< 0x20`). A RIP-relative sweep of the whole five-slot array
  for `+0x08`, `+0x48` and `+0x60` finds six functions, all on slot 0: `00264640`, `00264800`, `0026ABA0`,
  `0026AD10`, `0026B730` and `FieldData_GetVariable0`.
- ~~Slot 3's special first call site is recorded, **not explained** — what distinguishes slot 3 was
  not pursued.~~ **Answered 2026-09-30 (FABLE):** there is no special slot-3 call. The mode-1 path runs slots 3
  and 4, and the mode-0 path runs slots 0–4 (corrected above).
- ~~The slot array's static nature means there is no constructor to read; whatever fills `recordPool`
  and the three tables was not traced.~~ **Answered 2026-09-30 (FABLE):** the array is static, but two per-slot
  initialisers fill it. `ActorSystem_InitializeManagerRuntime` stores the return of
  `ActorStorage_AllocateAndInitializeRecords` into `recordPool` (`+0x08`), with the store directly after the call
  (`mov qword ptr [rbx + 8], rax`, `rbx` = the slot). The bind `ActorManager_BindLoadedDefinitionPayload` stores
  `SaveImage_GetPersistentPayloadBase()` into `table256` (`+0x48`, `mov qword ptr [rdi + 0x48], rax` directly after
  the call) and the static banks into `table64` / `table32` (`+0x58`, `+0x60`;
  [the field map](Actor-Manager-Record/the-actor-manager-record-field-map.md) §2.2 and FH-2). Both initialisers are
  named, not cited by address, because their far ends are other pages' matter.

## Falsification pass 1 — 2026-09-13 (OPUS)

**passes: 1 · last_pass: 2026-09-13**

Everything here rests on one negative — §4's correction that the inner drive loop is dead because
*"nothing ever sets the low nibble"* — and that negative rests on §11's trap: the four
`mov byte [rsi + 0x14], 1` stores belong to a **wait slot**, not the actor record. §11 proves this
far and stops:

```asm
0025DFC6  lea   rsi, [rax + rcx*8]     ; an element of an array — NOT the record
```

**`rax` and `rcx` are resolvable, and resolving them makes the trap much harder to fall into.**

### The wait slot is a 40-byte record the actor record points at

```asm
0025DFB6  movsx rax, byte ptr [rdi + 0x11]   ; a SIGNED byte index, in the record
0025DFBB  lea   rcx, [rax + rax*4]           ; × 5
0025DFBF  mov   rax, qword ptr [rdi + 0xa8]  ; the array base — a POINTER FIELD of the record
0025DFC6  lea   rsi, [rax + rcx*8]           ; base + index × 40
```

So `rsi = *(record + 0xA8) + (int8)(record + 0x11) × 0x28`. The wait slot is **`0x28` = 40 bytes
wide**, and **the actor record owns both halves of the address** — the array pointer at `+0xA8` and
the index at `+0x11`. That is why the two `+0x14`s look alike and why a displacement census cannot
separate them: they are reached from the *same* record, one directly and one through a pointer it
holds.

### And the wait slot's `+0x14` is not a flag byte at all — it is an eight-case enum

```asm
0025DFF0  movzx ecx/eax, byte ptr [rsi + 0x14]
0025DFF4  cmp   eax, 7
0025DFF7  ja    <default>
0025DFFD  mov   ecx, dword ptr [r14 + rax*4 + 0x13e3cc]   ; an RVA table of 8
0025E005  add   rcx, r14
0025E008  jmp   rcx
```

**A bounded jump table on `0..7`.** So the values §4's correction lists — `= 1`, `= 3`, `= 4`, `= 5` —
are **wait-kind states, not bits**, which is exactly why they read as low-nibble writes to a census
keyed on displacement. The trap is not a coincidence of offsets; it is an enum whose range happens to
be the nibble.

**This strengthens §4's conclusion rather than changing it.** The record's `+0x14` is tested
`& 0x40` and `& 0x10`; the slot's `+0x14` is switched on `0..7`. Different object, different width of
meaning, same displacement.

| claim | measured |
|---|---|
| slot block `0x288` = 648 B based at `02098E10` | `0025D9EF lea rdi, [rip] → 02098E10` / `0025D9F6 imul rbx, r14, 0x288` |
| the loop's own test | `movzx ecx, byte [rdi+0x14]` / `test cl, 0x40` / `jne` / `test cl, 0xf` / `je` — verbatim |
| the eight writer sites §4 names | **all eight found** in an independent sweep |
| `0025DF00` is 1,228 B | exact |

### Where my own sweep could not help, and said so

§4's control is *"every write to a byte at displacement `+0x14` in the image was listed (80 sites)"*,
plus *"no word or dword store covers the byte"*. My sweep finds **86** byte stores at `+0x14` — the
six-site gap is a definition difference, since I counted `add`, `xchg` and `setne` as writes too, and
none of the extra six has an actor record as its base.

The second half is the one worth being honest about. **A displacement-keyed sweep finds 9,002 wider
stores whose span covers `+0x14`** — 8,223 of them qword stores at `+0x10` alone. That number
falsifies nothing: it is uncontrolled, because it is not restricted to actor records, and a sweep
keyed on displacement has no way to restrict it. **"No wider store covers the byte" is a claim about
one structure, and no displacement census can settle it** — it rests on knowing which base registers
are actor records, which is a type judgement. §4's wording is honest about this: *"the control is the
sweep itself, which lists every writer the census knew."*

**Not claimed:** nothing here was executed or observed live. The eight jump-table arms at
`0013E3CC + r14` were not each followed; §12's five slots and the four accessors were not re-derived.
Whether a wider store reaches an actor record's `+0x14` is **not** settled by this pass either — it
needs the bases typed, not the displacements counted.

*Reconciled 2026-09-30 (FABLE):* both items this pass left open are now closed on the page.
- **The eight arms.** Decoding the table at `0025E3CC` gives kind 0 → `0025E127`, kinds 1 and 2 → `0025E0BE`,
  3 → `0025E027`, 4 → `0025E091`, 5 → `0025E00A`, 6 → `0025E058` and 7 → `0025E083`. Each arm is described in
  §11's SECTION-12 table.
- **The wider-store question.** §4's 2026-09-17 cross-check settles it against the byte-range writer census, which
  covers stores reaching `+0x14` from lower displacements and attributes each one to its base.

## Falsification pass 2026-10-01 (SWE2-CONTRACT for OPUS)

*A non-author pass: SWE2-CONTRACT wrote neither §11's SECTION-12 table nor the bound it attacks. Static, on the
certified image `73461d08…`; the only execution is check W13, which runs five of the image's own instructions under
Unicorn. Record: [`swe2contract-reopened2-0930`](../_index/candidates/swe2contract-reopened2-0930/README.md).*

**The claim attacked, and why it carries the page.** §11's SECTION-12 wait-completion polarity table, the correction
that reopened the page: which predicate each wait kind runs, which result holds the wait and which completes it, which
kinds set the wait slot's `+0x27`, and that `0025E127` is the blocked exit and `0025E0BE` the interpreter arm. Also
attacked: the bound §8 and §9 draw from that table, that one `0025DF00` call dispatches at most twice. This is what
decides when a waiting script resumes, and the interpreter page, the request-chain page and GR-1's answer all read it.

**Method.** `falsify_wait_polarity.py` decodes `0025DF00` linearly from its `functions.tsv` extent and resolves `r14`
from its `lea`. It decodes the eight-entry table at `0025E3CC` from the image and reads each arm's call, compare,
branch polarity and stores. It runs a store census over the body for `+0x14` and `+0x27` on the wait-slot base, and a
back-edge analysis of the loop head `0025DFA0`. Positive controls: a table copy with kind 3 repointed, a planted
`+0x27` store and a dword store at `+0x24`, each of which the matching check must see.

**Result: SURVIVED for the attacked claim. One adjacent sentence is CORRECTED.**

| check | clause attacked | result |
|---|---|---|
| W1 | 1,228 B, 329 instructions, `ret` at `0025E3CB`, no jump leaving the extent | survives exactly |
| W2–W3 | dispatch on wait `+0x14`, `cmp 7` / `ja 0025E127`; kinds 0→`0025E127`, 1 and 2→`0025E0BE`, 3→`0025E027`, 4→`0025E091`, 5→`0025E00A`, 6→`0025E058`, 7→`0025E083` | survives exactly |
| W4 | kind 3 holds while `003DBF60` finds an entry; `0xFF` completes and sets `+0x27` | survives |
| W5 | kind 4 holds while `003DC050` finds none; a found notification is removed by `003DB2A0`; no `+0x27` store | survives |
| W6–W8 | kind 5 (`002674B0`) and kind 6 (`003DB640`) hold while active; kind 7 calls `00267420` and jumps into kind 6's tail at `0025E06E`, sharing its `+0x27` store | survives |
| W9–W10 | `0025E127` sets wait `+0x16` = 1 and falls to `0025E12B` with no interpreter call; `0025E0BE` calls `0025E4C0(slot, record, wait slot)` | survives |
| W11 | stores covering wait `+0x27` are exactly `0025E04F` and `0025E07A`; the four `= 1` stores to wait `+0x14` are `0025E01E`, `0025E04B`, `0025E076`, `0025E0B5` | survives exactly |
| W12 | at most two dispatches: the four back-edges to `0025DFA0` each follow a `+0x14 = 1` store, and nothing at or after the interpreter arm branches back into the dispatch | survives, within the limit below |
| W13 | §11's early movement path, the mode passed to `Movement_SetRequestedSpeed` | **corrected**: mode 0 for a positive speed and 2 otherwise, measured by running the bytes; the page had the two inverted |
| C1–C3 | the positive controls | each is caught |

**Limit of W12.** The re-dispatch re-reads the wait-slot index from record `+0x11` (`0025DFB6`). In the direct closure
of the ten functions the loop head and the arms call (168 functions), the byte stores covering `+0x11` are all on
`0x14`-stride resource-entry bases (`003DB7A0`, `003DC130`, `003DC1B0`). Four wider stores covering it
(`00226280`, `00226BE0`, `002EBFA0`, `002EC2C0`) are not typed here, and indirect calls are not followed.

Output `falsify_wait_polarity.out`, `FAILS 0`. GR-1's answer is already on the page (the §8 box and §11's `+0x27` item),
and W11 reproduces the store half of it.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT.** `FUN_0031adb0`, owned by that layer, calls `003590D0` on this page. That caller is a 1,790-byte routine with a stack cookie and a `0x80`-byte frame; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — CLIENT.** `FUN_003160c0`, owned by that layer, calls `003148F0` on this page. That caller is a 212-byte walk of the table at `[022C2550]` from `+8`, the same table the equipment-slot eligibility test walks; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Spawn_Encounter_Lifecycle — CLIENT.** `FUN_00307030`, owned by that layer, calls `0026ADC0` on this page. That caller is the clearing half of that same sixty-four-record sweep, which runs only when the gate above it agrees; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (9 edges through 4 of this page's functions).** The UI layer reaches this page at `003148F0`, `003590D0`, `001EDDA0`, `001EDE80`. `FUN_0024b9b0` is the worked example, read in full - it is a 1,500-byte routine whose second argument being **8** short-circuits it to a single arm before any of the rest runs; **6 of the 9 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — MECHANICAL (SWE2-CONTRACT 2026-09-15, 58 edges).** All 58 edges are Presentation bodies sharing the
page's cited helpers: ~40 route through `001EDDA0` (`004500C0`, the cadence-gated dispatch
`002F4020`, `003A8DD0`, `003337B0`, `003A8390`, `00526D80`, `003D92C0` (interior read 2026-09-17, SWE2-FRONTIER: 1,301 B — `01F44830` base at [`003D92DF`](../_index/ADDRESS-INDEX.md), `00430B90` ×4 + `004309C0` ×2 + `003A8950`/`00808C40`), `002F2530`, …); four pairs
of `00358940`/`003590D0` calls come from `00465690`/`003A56F0`/`003A4290`/`00465120`; `001ED180`
calls `Presentation.Cutscene.RuntimeSupport` `001EC560`. `003A4290`/`003A56F0` are the twin
`+0x48`-kind dispatch fronts of
[the effect-element type dispatch](../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md) —
selector bound at [`003A4308`](../_index/ADDRESS-INDEX.md) / `003A578C`, 14-kind outer tables
`003A5540`/`003A68E4`, reached through the `00537xxx` record-store family's tail jumps. The field pass and the render pass share
the same frame and actor accessors — mechanical fan-in, not a render responsibility the pass owns.

**CombatFormula — CLIENT.** `00384F40`, owned by that layer, calls `00313F60` — the 5-B thunk to
`00377C20` (`FieldData_GetActiveFieldRecordBit15`) this page names; the formula layer consults the
shared action-permission accessor through the thunk. Fan-in, not shared ownership. Read from
`edges.tsv` 2026-09-17 (SWE2-FRONTIER).

**Combat — CLIENT (SWE2-EC7 2026-09-19, 1 edge).** `00263E30`, a callee this page's `003229E0`
section cites, is also called by the Combat-filed `003206E0`. The combat caller is a mechanical
user of the same shared helper.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Audio — SERVICE, CLIENT (39 edges).** The pass `0025D9E0` calls `00261F90`, the area-music select: it reads the field id `003148F0` and the save image `002EF2B0` (a save-image bit and byte can override the field's track), substitutes tracks `0x5A`/`0x5B` on two battle-state tests, and starts the result through `002DEC00`, `002DEE50`, `00360D30` and `00361170` with a fade of `0x78`. The init core `002620E0` calls `00363B40`; the tick `00314020` calls `002DEBA0` and `00362850`; the per-record step `00332750` calls `00332C40`, which runs 14 audio helpers such as `002DEF40`, `002DF0F0` and `003A1070` and calls the mode-byte getter `00181DD0` (as do `003B99D0`, `003D7CE0`, `003D7DC0` and `003D7E90`); the slot teardown `00332FA0` calls `002DEE80` and `003B3EA0`; `003775D0` and `003784A0` call `003635E0` and `00363750`; `003B99D0` calls the veto predicate `001EDDA0`; `00362850` calls the focus-handle getter `003590D0`; and `00361DE0`, `003623C0` and `00363FD0` call `0036DD80`, which stores one 16-byte constant into a global. The field pass starts the area's music and the tick machinery runs marker and slot work that ends in audio calls, while audio bodies read the same small getters; the pass owns no audio state and the music choice is the audio pages' matter.

**CombatAI — SERVICE, CLIENT (16 edges).** The battle-unit frame `BattleUnit_UpdateLifecycleAndCombatFrame` (`00233F70`) calls `BattleUnit_UpdateCombatFrame` (`00308610`) and `BattleUnit_RebuildPerceptionCandidateCache` (`003247F0`); the AI's target code calls this page's accessors - `ActorWork_GetBattleUnit` (`0031B760`) from `AiOrder_EvaluateTargetSelector` (`00301AD0`), `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`), `AiOrder_SelectFinalTargetFromCandidates` (`003087E0`) and two more, `ActorWork_GetBattleUnitRaw` (`00263E30`) from the perception cache builders, the field-bit thunk `00313F60` from the three `BattleEnmity_*` writers and the perception bodies, and the slot-table readers `00264640`, `00264D20` and `00264800` from `AiTargetSelector_ResolveOperandValue` (`00321190`). The `+0x38` callback this pass drives hands each bound unit to the AI's per-frame work, and the AI looks units and slot tables up through the same accessors the pass uses; the AI's decisions are not described here.

**CombatAction — SERVICE, CLIENT (20 edges).** `00233F70` calls `0030CA50`; `003229E0` calls `BattleAction_IsTargetEligibleForCurrentAction` (`002FFA60`) and `00306BB0`, a 20-byte test that a battle-state word minus 5 is 0 or 1 (which `BattleUnit_HandleActorTimelineEvent`, `00319F50`, also calls); action bodies reach this page's accessors - `00263E30` from `Battle_ProcessActionTargetEntry` (`003191B0`), `BattleUnit_HandleActionTimelineEvent` (`00325260`) and three more, `0031B760` from `BattleAction_EvaluateTargetPreviews` (`00303830`), `00306010` and `BattleAction_ResolveSpecialSequenceTargets` (`0030EC00`), `00313F60` from `BattleAction_ApplyKnockbackImpulse` (`00323350`) and the two timeline handlers, `003148F0` from `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (`002F8060`) and `002FA740`, `003590D0` from `00317E60` and `00319090`; and `BattleAction_InitializeGlobalSpecialSequenceMode` (`00306BD0`) calls the deferred-mode request `0032FC30`. The action layer resolves units, the focus handle, the field id and the field bit through the page's getters, and its special-sequence start uses the same deferred request the pass issues for slot 0; the pass performs no action logic.

**CoreRuntimeScheduling — SERVICE, CLIENT, MECHANICAL (23 edges).** `001EDDA0` (27 B: returns 1 when one global is non-zero or another is zero) is called by `0025DF00`, `0024B9B0`, `00332750`, `003337B0`, `003A8390`, `003A8950`, `003A8AE0`, `003D92C0`, `004500C0`, `0046E990` and `00526D80`, and `00265860` and `00265880` call it too; `0025DF00` also calls the readiness sum `001EDE80`, which adds the two seven-byte global reads `0022A030` and `0022A080`; the main loop `0022B8C0` calls the mode-byte getter `00181DD0`; the three frame bodies `0022A770`, `0022B8C0` and `0022BC20` call the tick `00314020`; and `0022A0B0` calls the path-table installer `002DF9A0`. *(Added 2026-09-30, FABLE:)* the frame body `0022A770` also calls `0026B730`, which writes entry 0 of slot 0's `table256` (§12 Limits). These are the scheduling layer's two predicates, its frame bodies and a boot installer - the pass and its tick bodies ask the same cadence/veto question every frame, and the frame calls the tick that runs the pass; no scheduling state is owned here.

**Developer — CLIENT, MECHANICAL (5 edges).** The developer monster-record property fill `001C6320` calls `001EBA40` (the lazily resolved shared object), `00200B50`, `00200B80` and `00200BE0`, and `001C2F50` also calls `00200B80`. `00200B50` and `00200B80` read a tagged value as float or int (tag 1 int, tag 2 double) and `00200BE0` tests the tag for 6, so the developer tooling uses the same variant readers and shared object as the pass; they carry no field-runtime meaning.

**Input — SERVICE, CLIENT (12 edges).** The arbiter `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`) calls the slot-table reader `00264640`, the all-slots-ready predicate `00265680` and the field-bit thunk `00313F60`; `002E09A0` also calls `00265680`, and the tick `00314020` calls `002E09A0` and `0036FD90`; `00226BE0` calls `ActorManager_GetRecordByOrdinal` (`00358940`) and the focus-handle getter `003590D0`; and the slot-object tick `0046E990` and release `0046EE70` call the input-owned lookups `0035B1A0`, `0035B240` and `0035B550`. Input arbitration asks this page's readiness and slot questions (`00265680` requires every active manager slot's `+0x17` low bits to be 3), and the tick machinery borrows input's lookup family; neither side owns the other's state.

**Movement — SERVICE, CLIENT (132 edges).** The script driver `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`) calls the locomotion step - `Movement_UpdateActorFrame` (`002E5030`), `002E5750`, `Movement_SetRequestedSpeed` (`0026D6F0`), `002E4A10` (copies a three-dword triple inside a class-3 record's sub-block) and `002E6310` - and those bodies call on (`002E5030` into `Movement_ComputeDeltaFromHeadingSpeed`, `Movement_UpdateSteeringTowardTarget` and five more; `002E5750` into 21 callees such as `00263CC0`); `0025DF00` is itself filed to Movement in the census, so its calls into this page's helpers (`001ED130`, `001ED180`, `001EDDA0`, `001EDE80`, `002681E0`, `00357760`, `00357770`, the `ActorResource_*` entries and the interpreter) count here too, as does the pass's own call of it; `00233F70` calls `BattleUnit_ApplyMovementIntentToWorldActor` (`0023A070`), `Actor_SetMovementSpeed` (`0026A330`) and `Navigation_HasDataset` (`00383C80`); `BattleUnit_SnapshotWorldActorRuntimeState` (`00236300`) calls `Navigation_FindRegionForPositionXZ` (`00384130`), `Navigation_HasDataset` and five more; in the other direction movement bodies call this page's getters - `003590D0` from eleven (such as `Movement_SetRequestedSpeed`, `Movement_UpdateSteeringTowardTarget` and `BattleUnit_CanAdvanceCombatNavigation`, `00325D90`), `00263E30` from ten (such as `PartyFollow_SolveFormation`, `00338490`, and `BattleLocomotion_QueryDynamicActorObstruction`, `003357B0`), plus `00313F60`, `003148F0`, `0031B760`, `00358940`, the angle wrap `0026AC70`, `00366690`, `00380800` (vector normalise) and `00377DB0`; and the tick `00314020` calls `00234520`, `003DAA20`, `003DAA40`, `003DAC70` and `0046AFA0`. Each pass drives an actor's script and then its locomotion, and movement code in turn looks up the focus actor, units and the field state through the pass's accessors; the pass decides when locomotion runs, not how it moves.

**Party — SERVICE, CLIENT (24 edges).** The pass `0025D9E0`, `002681E0` and `Movement_SetRequestedSpeed` call `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`); `00233AA0` calls `PartyFocus_SelectAndRequestDefaultActor` (`00326500`); `00236300` calls `PartyFocus_IsCurrentPackedActorHandle` (`003273B0`); the tick `00314020` calls `PartyControl_UpdateControlledActorLocomotion` (`00358C60`) and `PartyFocus_UpdatePrimarySecondaryActorProcessing` (`00358EE0`); party bodies call the page's accessors - `003590D0` from `PartyRoster_GetActorBySlotOrCurrentFocus` (`00263770`), `PartyRoster_AssignActorToSlot` (`00269C70`), `BattleUnit_GetPartyLeader` (`003272A0`) and three more, `00263E30` from `BattleUnit_ResolveByFocusHandle` (`0031B7E0`), `BattleUnit_GetPartyLeader` and the two `PartyConfiguration_*` roster reconcilers, `00265680` from `PartyControl_ApplyAnalogLocomotionToActor` (`00358CB0`) and `PartyFocus_ProcessActorControlPresentationState` (`00358F90`), `00313F60` from `PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`) and `0031AC00`, `002681E0` from `PartyRoster_AssignActorToSlot`, `0031B760` from `0030BEB0` and `00380800` from `004742A0`. The pass publishes the focus actor it reads from the party focus handle (§3) and, on slot 0, once the roster loop of §5 has collected all four members, runs `00233AA0`, which requests the default focus actor; the party layer owns the handle and the roster, and reads units and readiness back through this page's accessors.

**Resource — SERVICE (1 edge).** The per-map driver `003319D0`, which `0032FC30` runs for slot 0, calls `0032E400`. That is one call into the resource layer on the manager resource-set load path §8 describes; the pass only issues the request.

**Save_Load_Settings and SaveLoad — SERVICE, CLIENT (37 edges).** The pass `0025D9E0` calls `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) and `SaveWrite_GetBusyFlag` (`00583920`), as do `00261F90`, `002620E0` and `003148F0` for the base; `002EF2B0` calls `SaveImage_GetActiveRuntimeBuffer` (`002EF640`), which 18 save bodies call (such as `SaveRuntime_RebindImageBackedGameplayState`, `00238A80`, and `SaveRuntime_InitializeHeaderAndImageBackedState`, `00253A80`) and which, with `002EF2B0`, the SaveLoad-domain `00280140` also calls; `SaveWrite_PrepareAndSubmitFullImage` (`0057E310`) calls `SaveImage_GetCaptureStagingBuffer` (`002EF620`), `002EF630`, `002EF640`, `CRC32_Compute` (`003BB220`), `SavePath_FormatSlotAssetName` (`00584610`) and one more, and is called by `SaveWrite_OperationStateCallback` (`0057E4D0`), which also calls `00583FD0`; and `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) calls `003148F0`. The pass refuses to run while the save-write busy flag is set and reads persistent data through the save image's getters, and the save writer (whose three busy-flag writes §2 lists) reads the field id when it finalises the header; the save layer owns the image and the writes.

**Script_VM_Native_Bridge — SERVICE, CLIENT (91 edges).** `0025DF00` calls `WorldActorScriptVM_InterpretBytecode` (`0025E4C0`), `ScriptVM_WaitList_HasAnyActorChannelActive` (`00267420`), `ScriptVM_WaitList_HasAnyActorResourceEntryActive` (`002674B0`) and the per-frame state pair `00357760`/`00357770`; the interpreter calls `WorldActorScriptVM_ServiceRequestWaitState` (`0025B400`), `VMNativeCommand_ExecuteLifecycle` (`002621D0`), `0025D740` and 14 more, and together with those it calls the `ActorResource_*` entries `003DB2A0`, `003DB640`, `003DBF60` and `003DC050` and the record getter `00358940`; and script-VM bodies call the page's getters - `00358940` from 17 (such as `00346FA0`, `0034A640` and `0034B350`), `003590D0` from 14 (such as `00341CB0`, `00350DD0` and `003516E0`), the angle wrap `0026AC70` from nine (such as `003439B0` and `003578B0`), the deferred-mode request `0032FC30` from `003522C0`, `00353080`, `00353590` and `0050D0C0`, and `001ED130`, `001ED180`, `00263CC0`, `00265680`, `0026B8E0`, `003148F0`, `0031B760` and `00377DB0` from one to three each. This pass is the interpreter's driver (§11: `0025DF00` is its only ledger caller), and script verbs read actors, the focus handle, the field state and the mode request through the same accessors; what each verb does is the script-VM pages' matter.

**Status_Periodic_Terminal — SERVICE, CLIENT (5 edges).** `00233F70` calls `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`), which calls the readiness predicate `00265680`; `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` (`00386860`) calls `00263E30`; and `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` (`00320450`) and `BattleUnit_AddPrimaryResourceRecoveryAccumulator` (`00329A20`) call the field-bit thunk `00313F60`. The battle-unit callback this pass drives runs the periodic maintenance, which with the recovery accumulators reads units, readiness and the field bit through the page's accessors; periodic effects are the status pages' matter.

**Story_Event_Quest_Hunt — CLIENT (12 edges).** `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) is called by all twelve `PersistentFlag_*` bodies, among them `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`), `PersistentFlag_QueryBank2048` (`0032A930`), `PersistentFlag_SetPrimary` (`0032AB60`) and `PersistentFlag_SetBank2048` (`0032ABF0`). The story flags live in the save image's persistent payload, so every flag query and set resolves its bank through the getter this page cites for the pass's own reads; the pass reads no story flag.

## 13. The `0025DF00` exclusive subtree — all 9 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns nine functions to `WorldActor_UpdateRuntimeAndScriptExecutionState`
(`0025DF00`, §11). Every member was disassembled from the shipping image for this binding; each interior
citation is an instruction inside the member's declared extent.

| member | role | interior |
| --- | --- | --- |
| `002E6310` | 20 B — kind gate: `[rcx+3] & 0xE0 == 0x60` record-kind test (the `0x60` class mask) | [`002E631B`](../_index/ADDRESS-INDEX.md) |
| `00357760` | 11 B — clears the per-frame state dword `022C7F88` | [`00357760`](../_index/ADDRESS-INDEX.md) |
| `00357770` | 7 B — reads `022C7F88` (the pair to `00357760`) | [`00357770`](../_index/ADDRESS-INDEX.md) |
| `003E68B0` | 42 B — `003E6E60` resolve gate, then tail `003AEF20(rcx+0x550)` | [`003E68C9`](../_index/ADDRESS-INDEX.md) |
| `003E6A70` | 42 B — same gate, then tail `003AEF50(rcx+0x550)` | [`003E6A89`](../_index/ADDRESS-INDEX.md) |
| `003E6EF0` | 84 B — same gate, forwards `(rcx+0x550, rdx, r8, xmm3)` to `003AF220` | [`003E6F1A`](../_index/ADDRESS-INDEX.md) |
| `003AEF50` | 54 B — accumulates a 2-bit flag word over the `[+0x18]` `+0x48`-linked list: bit1 = any node `+2!=0`, bit0 = any node `+1!=0` | [`003AEF60`](../_index/ADDRESS-INDEX.md) |
| `003AEF90` | 655 B — the move-queue fold: zeroes two out-structs, gates on `02B3F540`==0, walks the `+0x48` list, unlinks `word[+0x22]==0x16` nodes, and accumulates `minss`-clamped floats into the out-structs | [`003AEFF4`](../_index/ADDRESS-INDEX.md) |
| `003AF220` | 136 B — `003AEF90` first, then if `[+0x18]` nonzero: `|v|²`→`00861F14` sqrt, `00380800` normalize, `min(step,|v|)*v̂` back into `rdi` — a step-clamped displacement | [`003AF287`](../_index/ADDRESS-INDEX.md) |

In the root's settle block (`0025E241`–`0025E3AA`) the trio run per linked record: each call site is
gated on the `word[rbx]` index ×`0x740` into the render-record array `022C6F28` with a `+0x284` match —
`003E6EF0` step-clamps the displacement into the `rsp+0x30`/`rsp+0x40` out-structs, `003E68B0`'s result
merges under the `[rdi+0xD]` bit-1 gate, `003E6A70`'s flag word sets `ebp`/`esi` — and the results drive
the `002681E0`/`002E5030`/`002E5750` steering dispatch at the block's tail plus a 2-bit field write at
`[rbx+0x10]` bits 2–3. Each wrapper resolves the actor's `+0x550` sub-record through the shared
`003E6E60` gate and forwards to one `003AExxx` body — the move queue (`003AF220`→`003AEF90`), the flag
accumulator (`003AEF50`), and `003AEF20` (shared, other callers — excluded from the census alongside
`003E6E60`, `00380800`, `00861F14`, and the root's own intra-extent `0025DFF0`–`0025E3AF` subregions and
wait-table callees `003DB2A0`–`003DC050`, `00267420`, `0025E4C0`).

## The `00233F70` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`00233F70` (467 B) is `BattleUnit_UpdateLifecycleAndCombatFrame` — the `+0x38`
callback bit 4 drives once per pass. The entry chain: `0031B760(rdx)` resolve
(null → out, `00233F8B`), `002671C0` ready (`00233F91`), `00383C80`
(`00233F9E`), `unitFlags` bits 3/4 gates (`00233FAD`–`00233FC6`), `[+0x698]`
stats flags `+0x64 | +0x3C` vs `0x80000003` → `00313F60` → `00307C70(rbx)`
(`00233FD8`–`00233FF1`); `003228E0` at `002340D0`, `00267240` at `0023411A`.

| member | role | interior |
| --- | --- | --- |
| `002671C0` (46 B) | `ActorSystem_IsPrimaryBattleSimulationReady` — `[02098E20]` bit 0 set AND `([02098E21] & 1 \| [02098E20] >> 7) == 0` AND `byte[02099DA1] == 0` (`002671C7`–`002671EA`) | [`002671CB`](../_index/ADDRESS-INDEX.md) |
| `00267240` (27 B) | flags predicate — `byte[rcx+0x10] == 0` and (`[+0x14] & 0x40` or `[+0xC] & 1`) → 1 (`00267240`–`0026725A`) | [`00267246`](../_index/ADDRESS-INDEX.md) |
| `003228E0` (51 B) | throttle predicate — `ecx+1 ≤ 1` → `0024DE70(ecx) ≥ 3`; else 0 (`003228EB`–`0032290B`) | [`003228F0`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0031B760`, `00383C80`, `00313F60`,
`00307C70`, `0024DE70`, plus the mid-body lifecycle battery this page's
§150/§251 rows already enumerate.

## The `0057E310` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0057E310` (`SaveWrite_PrepareAndSubmitFullImage`, ~8 B into a `0xE0`
stack-cookie frame — `0057E31B`/`0057E322`).

| member | role | interior |
| --- | --- | --- |
| `002EF630` | `lea rax, [02211000]`; `ret` — 7-byte base getter; sibling `002EF640` returns `02164280` (`002EF630`) | [`002EF630`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `003A8950` (2026-09-17, SWE2-EC7)

`003A8950` — 394 B, 34 frontier callers at census; the per-element command interpreter this page
reaches through `003D92C0`. Interior verified: an 8-iteration loop (head
[`003A89B0`](../_index/ADDRESS-INDEX.md)) walks byte tags at `[rax+0x298+i]` and dispatches on
{0,1,2,3}: tag 2 first consults `001EDDA0` (the cadence/veto predicate this page documents) then
gates on `arg1 == 2` before the shared `003A8AE0` tail; tag 3 requires `arg1 == 3`; the word at
`[rsi-0x18]` (`rax+0x288+i*2`) feeds `cvtsi2ss` scaling by the caller's `[rdx+0x3C]` float.
Element slots are `{byte tag, word scale}` pairs striding a fixed table.

NOT claimed: what tags 0/1 mean semantically, or which element table owns the 8-slot array.
*Answered by cross-reference 2026-09-30 (FABLE):*
[an effect element frame by frame](../17-Presentation-Rendering/Effect-File-Formats/an-effect-element-frame-by-frame.md)
§3 reads the routine whole as an effect element's child-spawn slots. The array belongs to the element's source record
(`[element + 0x18]`). Tag 0 is an empty slot, and tag 1 fires once, when the element's frame reaches the slot's start
word.


## Interior citation — frontier hub `00181DD0` (2026-09-18, SWE2-EC7)

`00181DD0` — 21 B, 29 callers; the `001EBA40`-object `+0x118` byte getter the `0024B9B0`
interior read above invokes. Interior verified: `001EBA40()` at
[`00181DD4`](../_index/ADDRESS-INDEX.md) supplies the shared object, then
`movzx eax, byte [rax+0x118]` at [`00181DD9`](../_index/ADDRESS-INDEX.md) returns its mode
byte. Nothing else happens — a pure field accessor on a lazily-resolved global.

### Crossing — Developer (batch-9 hub exposure)

Naming `001EBA40` (the shared-object supplier `00181DD0` reads `+0x118` from) exposes one
Developer-domain caller edge: `001C6320` calls `001EBA40`. The tuning/developer tooling
resolves the same lazily-created object the field pass consults — a read-side share, not
field-runtime reaching into the developer layer.

## SWE2-EC7-18 update (2026-05-15) — `001EDE80` gated predicate + `00383C80` readiness arm

`001EDE80` (61 B) is the two-gate readiness sum this page's loop head invokes: `dword[01F82E38]==0` or `dword[01DFE0C0]!=0` short-circuits to `eax=1` (`001EDE84`..`001EDE94`); on the open path it returns `0022A080() + 0022A030()` (`001EDE9B`..`001EDEA7`) ~~— the pair of readiness probes whose combined count tells the pass the group-2 set is still populating.~~ — two seven-byte reads, of the per-frame parity flag `02064AD8` and the main loop's step counter `02064AA8`. So the open path is HALFRATE, and the sum is the number of steps this frame ([the game-settings page](../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md) §17.3). §11 calls this gate a half-rate veto. *Corrected 2026-09-30 (FABLE): the struck reading had no anchor. `0022A080` and `0022A030` each read one of those two dwords and return.*

`00383C80` (13 B) is the readiness-test arm the pass checks after `002671C0` is ready: its whole body is `eax = (qword[02AEDFB0] != 0)` (`00383C80`..`00383C8C`) — a null-test predicate on the `02AEDFB0` run-state pointer, returning 1 while that global is populated.

## SWE2-EC7-22 update (2026-09-18) — `003E6E60` three-slot id resolver

`003E6E60` (139 B) is the deferred id->slot resolver the field pass runs per
record: `00422D50` object fetch, then three `0020E600` lookups on `[rbx+0xE0]`
/ `[rbx+0xF8]` / `[rbx+0xE0]` adding `[rbx+0xE8]` / `[rbx+0x100]` and storing
the results at `+0x558` / `+0x560` — the staged resolves the runtime pass
commits into the record's late slots. Interior anchor `003E6E73` (the first
`+0xE0` id load).

## SWE2-EC7-33 update (2026-09-19) - `001C6320`

`001C6320` (2,261 B) is the monster-record property fill - 58 `001FF740` writes plus `00200BE0`/`00200B50`/`00200B80`/`001EDF00`, with the `"MonsterId%d"`, `"monsterWeaponIndex"`, `"monsterWeaponIndex2"`, `"motionIndex"` and `"Common"` name strings. Interior anchor `001C63A6` (a `001FF740` write).

## SWE2-EC7-34 update (2026-09-19) - `004500C0`

`004500C0` (959 B) is an element walker - `[rcx+0x20]+0x180` record, `[rcx+0x44]` dword, `00430B90`/`004314E0`/`0039AF70`/`00398F90`/`005002E0`/`0042FDB0`. Interior anchor `004500FA` (an `00430B90` call).

## SWE2-EC7-34 update (2026-09-19) - `00526D80`

`00526D80` (844 B) is a field element pass - `[rdi+0x2C2]!=0` gate, `inc [rcx+0x230]`, `001EDDA0`, `01DFE0B4` state, `0044B960`/`0039AF70`/`00398F90`/`005270B4`/`0036DD80`. Interior anchor `00526DB0` (the `001EDDA0` call).

## SWE2-EC7-37 update (2026-09-19) - `003337B0`

`003337B0` (519 B) is a field-runtime pass body - `02F97348`/`02EC0F88`/`01CEBBA8`, `003A3E30`/`0020E600`/`003331A0` triples plus `0046EE70`/`003697F0`/`00314960`/`001EDDA0`. Interior anchor `003337F8` (a `0046EE70` call).

## SWE2-EC7-47 update (2026-09-19) - `0044B960`

`0044B960` (212 B) is a call-free XorShift-style bit-mixer gated on `022D9138` - seed `01EF93E8`, repeated `(x ^ (x >> 0x12) & 0x3FFFFF) | 0x1FC00000` chains producing bounded pseudo-random dwords. Interior anchor `0044B96D` (the seed load).

## SWE2-EC7-53 update (2026-09-19) - `003A3E30`

`003A3E30` (373 B) is a field-runtime pass body - `0024ED80`/`00322760`/`003229E0`/`003B02A0`/`003B0FD0` plus `02096A24`/`02096B24`/`02F97348`. Interior anchor `003A3EB0` (a `003229E0` call).

## SWE2-EC7-62 update (2026-09-19) - `003229E0`

`003229E0` (150 B) is a field-runtime pass body - `00263E30`/`00306BB0`/`003588B0` plus `02089340`. Interior anchor `003229F5` (a `003588B0` call).



## SWE2-EC7-66 update (2026-09-19) - `00267420`

`00267420` (132 B) is `ScriptVM_WaitList_HasAnyActorChannelActive` - `0020E600`/`00358940`/`003DB640`. Interior anchor `00267438` (a `0020E600` call).


## SWE2-EC7-73 update (2026-09-19) - `003B2CA0` registered-pointer lookup measured

`003B2CA0` (60 B) is the `02EBDBC8`..`02EBE5C8` registered-pointer
scan: stride `0x28`, matching entries have `[rax-8] != 0` and
`[rax] == rcx`; a hit returns `02EBDBC0 + index*40`, a miss 0 - the
linear lookup the runtime pass shares.
Interior anchor `003B2CB6` (the `[rax] == rcx` compare).

## SWE2-EC7-74 update (2026-09-19) - `00366690` angle wrap measured

`00366690` (80 B) is the `(-pi, pi]` wrap sibling of `0026AC70`:
`xmm0` is scaled by `0x40490FDB` (pi) and divided by `0x43340000`
(180), then two `comiss` loops add `0x40C90FDB` (+2pi) while under
`-pi` and `0xC0C90FDB` (-2pi) while over `+pi` - the degree-input
angle normalize the runtime pass shares.
Interior anchor `003666C0` (the `+2pi` wrap loop).

## SWE2-EC7-87 update (2026-09-20) - `003E4F50` field-anchored vec4 apply measured

`003E4F50` (278 B) is the sibling out-record the field-pass
callers run: `[rcx+0x400]` with a nonzero `word[+0x12]` resolves
a record whose `+0xD0`/`+0xD4`/`+0xD8` fill `[rbx..+0xB]` with
`+0xC` = 1.0f; `0046D100(&stack, rdi+0x180)` and
`0046D0C0(rbx, &stack, rbx)` commit; the `[rdi+0x670]` vec4 is
then lane-added into `[rbx]` (the dead arm adds zero instead) -
under a stack cookie.
Interior anchor `003E4FC7` (the `0046D100` call).

## SWE2-EC7-98 update (2026-09-20) - `002E0540` measured

`002E0540` (82 B) is the eight-slot scan `001ED180` and
`00265680` call: for each `0x68`-stride entry of the
`0215F200` table, `qword[+0]` non-null and (`byte[+0x3E]`
bit 0 sign-extended or `byte[+0x38]` nonzero) together yield
1; all eight quiet yields 0 - the any-live-entry probe the
runtime pass consults.
Interior anchor `002E0568` (the `qword` liveness test).

## SWE2-EC7-104 update (2026-09-20) - `0026FF50` measured

`0026FF50` (54 B) is the one-shot reset
`00378230` and `003784A0` call: when
`byte[02F8F238]` is set it runs
`0024C550(2)`, clears the flag, zeroes the
qword at `02F8F228`, and sets
`byte[02F8F29D] = 1` - a latched teardown that
runs once and then becomes a no-op until the
flag is armed again.
Interior anchor `0026FF62` (the `0024C550`
call).

## SWE2-EC7-105 update (2026-09-20) - `00263CC0` measured

`00263CC0` (55 B) is the class-dispatched
float read `00236300`, `002E5750` and the
`003B7xxx` arms call: `byte[+3] >> 5` picks
the class - class 2 answers
`float[[rcx + 0xB8] + 0xA4]`, class 1
`+0x38`, anything else (or a null `rcx`)
`0.0f` - the uniform magnitude fetch over
the two record layouts.
Interior anchor `00263CD6` (the class-2
`+0xA4` load).

`003A7050` (581 B) is the countdown arm `0024B9B0` calls: `02F97348`'s `word[+0x368] & 0x1000` gates, `word[+0x35A]` decrements by `cvttss2si(xmm6)`, and on reaching zero the `02EBEFB0` table walks 16 stride-8 slots calling `003334B0` each before the 0x1000 bit clears, else `+0x35A` converts to the `+0x35C` float - with `00332750`/`00333350`/`00333740`/`003697F0`/`003A8390` in the tail - the pass's tick-down.

Interior anchor `003A70C6` (function `003A7050`).

`00332750` (1262 B) is the per-record step `003A7050` calls: `[rcx+0x290]` nonzero plus `00250000`/`001EDDA0` either early-outs with `ebx+1` or publishes `rdi` to `02EC0F88`, accumulates `xmm6` into `+0x8C`, then `00332C40`/`003331A0`/`003697F0`/`003A3E30`/`003A8130`/`003A9070`/`0046E990`/`0046EE70`/`0020E600`/`00861EBA` run the record - the pass's per-record work.

Interior anchor `00332770` (function `00332750`).

`00333350` (91 B) is the 16-slot teardown `003A7050` and `003A7360` call: `00332FA0` runs on the record first, then every non-null of `[rsi+rbx*8]`, rbx = 0..0xF, takes `0046EE70` + `003697F0` and the slot is nulled - the pass's pointer-table clear.

Interior anchor `00333367` (function `00333350`).
