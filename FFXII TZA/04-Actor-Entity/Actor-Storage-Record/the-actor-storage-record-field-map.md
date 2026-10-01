---
system: The actor storage record (ActorStorageRecord, 0x6E0) — a field map from every reached accessor
category: 04-Actor-Entity
status: AUDITED
owner_layer: PrimaryOwner:ActorEntity — a companion to the record page, which owns the semantics
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: a typed field scan over every function in functions.tsv, seeded by the two record-returning
    accessors ActorManager_GetRecordByOrdinal (00358940) and ActorHandle_ResolveRegistryEntryByPackedId
    (003588B0), propagated through call arguments and record-returning callees for three hops,
    control ActorResource_RemoveActiveEntry's byte write of the free-list head at +0x60 (found);
    every access row is published beside this page in actor-storage-record-accesses.tsv
last_reviewed: 2026-09-10
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-actor-storage-record-field-map-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The actor storage record — a field map from every reached accessor

> [The record page](the-record-behind-every-actor.md) reads this record's allocator, its handle, its embedded sub-objects and
> its resource lists, and the store carries 62 rows for it. This page is the other axis:
> every offset any reached function touches — 81 of them, from 272 functions — with
> writers and readers per byte, the store's name where it has one, and the bytes nothing enumerated
> reaches. It does not re-read the semantics; it locates them.

## 1. What the player sees

Nothing directly: this is the world-side object behind every actor. What it drives is on the record
page; what this page adds is *who writes each byte*, which is what a reimplementation checks itself
against.

## 2. Native mechanism

### 2.1 How the accessors were found

Two seeds, both functions that return a record in `rax`: `ActorManager_GetRecordByOrdinal`
(`00358940`) and `ActorHandle_ResolveRegistryEntryByPackedId` (`003588B0`). The scanner tracks the
returned register through `mov` / `lea` / `add`, reports every `[reg + disp]`, queues callees that
receive the pointer in an argument register and seeds callers of functions that return it; three
hops.

| | count |
|---|---|
| access rows | 1042 (312 at a seed, 730 through propagation; the seeds include the constructor `00266BD0` since 2026-09-11) — re-run 2026-09-11 with the generation-3 scanner (FZ-16): 954 → 1042, of which 24 misfiled context reads left and 119 record accesses arrived (the CORRECTED note below) |
| functions reached | 275 |
| offsets touched | 86 — 40 with a store row, 46 without |
| hottest | `+0xC0` (94 r / 2 w), `+0x3` (80 r / 0 w), `+0xB8` (67 r / 2 w), `+0x18` (35 r / 2 w), `+0x9` (10 r / 14 w), `+0x0` (21 r / 0 w), `+0x1C` (16 r / 4 w), `+0xC` (11 r / 9 w), `+0x15` (18 r / 0 w), `+0xB` (13 r / 5 w) |
| control | `ActorResource_RemoveActiveEntry` (`003DB2A0`) writes the free-list head byte at `+0x60` (`003DB3F9`) — found |

**What the enumeration cannot see:** index-register forms; pointers stored into other objects and
loaded back (the battle unit's `+0x10` is the record, and the movement code's own handles); the
sub-objects the record embeds (`+0x120`, `+0x350`, `+0x4D8`, `+0x5A0` per the store) when a callee
receives an interior pointer through a register the scan does not follow; anything below the third
hop. `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) is **not** in this table: its writes
go to the ActorManager record ([the manager map](../Actor-Manager-Record/the-actor-manager-record-field-map.md)).

> **CORRECTED 2026-09-11 (FZ-16, FABLE-PUB140) — 24 rows were context reads, not record reads.**
> `WorldActorScriptVM_InterpretBytecode` fetches a record into `r13` through `00358940` in eleven
> handlers and reloads its *context* (the first argument, home slot `[rsp+0xB0]`) into `r13` after
> each (`0025E61B` … `002611A0`). The generation-2 scanner exempted every frame reload as an epilogue
> restore, so `r13` stayed "the record" for the rest of the function and bled through `mov rcx, r13`
> into `00267FC0` → `00262440`. Filed as record reads and now withdrawn: the interpreter's `+0x28`
> (`0026174A`), `+0x68` / `+0x70` / `+0x80` (`00261855`, `0026187D`, `002617C9` +3), the whole of
> `00262440`'s thirteen rows (`+0x48`, `+0x58`, `+0x60`, `+0x78`, `+0x98`, …) and `00268850`'s two at
> `+0x28`. The `+0x028` and `+0x098` rows are gone; `+0x048`, `+0x058` and `+0x060` keep their other
> readers. What the generation-3 census adds in their place is the interpreter's own record (`r15`,
> its second argument): four dwords `+0x64` / `+0x68` / `+0x6C` / `+0x70` and four `movss` floats
> `+0x74` / `+0x78` / `+0x7C` / `+0x80`, each with a writing handler and a reading twin — the store's
> 8-byte `+0x78` row was the context read and needs OPUS's correction (FZ-21 asks what the eight are).
>
> **What a census like this cannot see (2026-09-11, OPUS-NOTICE-CENSUSWRITES).** Seeds: the two record-returning accessors, and — since 2026-09-11 — the per-sequence initialiser `00266BD0` as a constructor seed (eight rows, five of them its `+0x1C` stores). `ActorStorage_InitializeRecord` `00266530` and `ActorStorage_AllocateAndInitializeRecords` `002679F0` derive the record from an index, not an argument, and stay outside: their stores (e.g. `+0x03` at `00267B04` / `00267B13`, `+0x1C` at `002666F1` / `00266A3A` / `00266A4E`) are not in the TSV.
> A scan seeded on *accessors* reaches *consumers*: a constructor that builds the record before
> any accessor can return it is reached only if it is seeded on its own. So the **reads** below are
> the well-covered side and the **writes** are under-covered wherever a constructor or an
> index-derived writer sits outside the seeds — do not rest an absence-of-writer claim on this
> TSV alone; pair it with a displacement scan of the candidate writers.

### 2.2 The field map

Width is the most common operand size at that offset; "w / r" counts distinct functions. The type
column is the store's `ctype` where the offset has a row.

| offset | width | type | store name | w / r | writers | readers |
|---|---|---|---|---|---|---|
| `+0x000` | 2 | uint16 | `selfIndex` | 0 / 21 |  | `0025AAD0` (`0025AAEF`); `0025AE00` (`0025AE9F`); +19 more |
| `+0x002` | 1 | uint8 | `actorIndexClass` ⚠ | 0 / 1 | **census shows none — see below** | `ScriptVM_SubmitActorRuntimeRequest` `00268850` (`002689F0`) |
| `+0x003` | 1 | uint8 | `packedKindAndSequence` | 0 / 80 |  | `ActorSystem_ReleaseManagerRecords` `0025B070` (`0025B0B7` +3); `0025B4C0` (`0025B4D8`); +78 more |
| `+0x004` | 1 | uint16 | *not in the store* | 1 / 3 | `ActorSystem_ReleaseManagerRecords` `0025B070` (`0025B1E5`) | `ActorSystem_ReleaseManagerRecords` `0025B070` (`0025B1B6`); `002EA6A0` (`002EA6A5`); +1 more |
| `+0x005` | 1 |  | inside the store's `+0x4` row | 0 / 1 |  | `003DE5F0` (`003DE5F4`) |
| `+0x006` | 2 | uint16 | `channelActiveMask` | 2 / 5 | `ActorResource_RemoveActiveEntry` `003DB2A0` (`003DB3C5`); `ActorResource_InsertEntryFromDescriptor` `003DB7A0` (`003DBAA2`) | `ActorResource_IsChannelBitActive` `003DB640` (`003DB640`); `ActorResource_FindActiveEntryByIdOrClass` `003DBF60` (`003DBF9D`); +3 more |
| `+0x008` | 1 | uint8 | `flags08` | 4 / 14 | `ActorManager_RunFieldRuntimePass` `0025D9E0` (`0025DD3C`); `0035A990` (`0035A9F6` +3); `0026A430` (`0026A436` +1); +1 more | `0025B250` (`0025B2A0`); `0025B600` (`0025B65C`); +12 more |
| `+0x009` | 1 | uint8 | `flags09` | 14 / 10 | `0035A7A0` (`0035A843` +1); `003B6CC0` (`003B6D21`); `003B6D60` (`003B6DA0`); +11 more | `00226640` (`00226847` +1); `0025B600` (`0025B652`); +8 more |
| `+0x00A` | 1 | uint8 | *not in the store* | 3 / 1 | `0046B690` (`0046B740` +3); `0046B870` (`0046B920` +3); `0046BAC0` (`0046BBB0` +5) | `002647E0` (`002647EE`) |
| `+0x00B` | 1 | uint8 | *not in the store* | 5 / 13 | `00268D10` (`00268DEA`); `00268EA0` (`00268F7D` +2); `0025BAD0` (`0025BE08`); +2 more | `0025AE00` (`0025AF0E`); `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`00261602` +2); +11 more |
| `+0x00C` | 1 | uint8 | `flags0C` | 9 / 11 | `0025C170` (`0025C1BC`); `0025BAD0` (`0025BAF2` +1); `0025BE50` (`0025BF01`); +6 more | `0025B4C0` (`0025B4E9`); `00268D10` (`00268E0A`); +9 more |
| `+0x00D` | 1 | uint8 | `flags0D` | 6 / 4 | `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025E1AD` +1); `002E5180` (`002E52B9`); `Movement_SetSteeringMode` `0026AE90` (`0026AEDB`); +3 more | `002E70E0` (`002E7104`); `0025C830` (`0025C8BD`); +2 more |
| `+0x00E` | 1 | uint8 | `flags0E` | 2 / 10 | `ActorSystem_BindBattleUnitsForEligibleRecords` `00265A20` (`00265ACA` +1); `0026AF30` (`0026AF30` +1) | `0026DC70` (`0026DCD7`); `0026DD50` (`0026DDB4`); +8 more |
| `+0x010` | 1 | uint8 | *not in the store* | 2 / 6 | `00268B10` (`00268C08` +1); `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`0026126F` +1) | `ActorManager_RunFieldRuntimePass` `0025D9E0` (`0025DD40`); `00268B10` (`00268C0F` +1); +4 more |
| `+0x011` | 1 | int8 | `currentWaitSlot` | 1 / 5 | `ActorResource_SelectPendingEntryForExecution` `003DB6E0` (`003DB754`) | `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025DFB6` +1); `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`00261250` +7); +3 more |
| `+0x012` | 1 | uint8 | *not in the store* | 0 / 10 |  | `ActorSystem_BindBattleUnitsForEligibleRecords` `00265A20` (`00265AD2`); `002677F0` (`00267817`); +8 more |
| `+0x013` | 1 | uint8 | `flags13` | 0 / 4 |  | `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025E1E7` +2); `00264DF0` (`00264DF0`); +2 more |
| `+0x014` | 1 | uint8 | `flags14` — **bit 4 drive the bound battle unit** (init sets `0x30`, cleared when the unit pool is full), bit 5 set at init (meaning open), **bit 6 idle / settled**, **bit 7 battle-unit eligible** (sequences 5 / 7 at bind); **bits 0–3 are never written** — the drive loop's inner repeat is dead; support (restated 2026-09-17): the image-wide writer census sees the constructor the route census cannot — every record-based `+0x14` write preserves the nibble (`& 0x7F` and `& 0xB0 | 0x30` in `00266530`, `| 0x80`, `& 0xEF`, `& 0xCF | 0x40`, the bit-6 ops), and every other `+0x14` store in a proven function lands on the wait slot, a `0x28`-stride resource entry, the secondary context or a global table, never the record ([the runtime pass](../the-field-runtime-pass.md) §4; `actor-storage-record-flag-bit-writes.tsv`) | 5 / 12 | `ActorSystem_BindBattleUnitsForEligibleRecords` `00265A20` (`00265B13`); `00266BD0` (`00266C1F` +1); `0026B8E0` (`0026B929`); +2 more | `ActorSystem_ReleaseManagerRecords` `0025B070` (`0025B212`); `0025B250` (`0025B29A`); +10 more |
| `+0x015` | 1 | uint8 | `handleTag4` | 0 / 18 |  | `0025AAD0` (`0025AAE8`); `00268B10` (`00268BEA` +1); +16 more |
| `+0x016` | 2 | uint16 | `handleTag11` | 0 / 6 |  | `0046B690` (`0046B806`); `0046B870` (`0046B9E6`); +4 more |
| `+0x018` | 1 | uint32 | *not in the store* | 2 / 35 | `002693D0` (`00269500`); `00262F90` (`00262FDB` +1) | `0025B820` (`0025B8EC`); `00268B10` (`00268BBE` +1); +33 more |
| `+0x019` | 1 |  | inside the store's `+0x18` row | 1 / 4 | `00262F90` (`00262FE6` +1) | `0025B820` (`0025B8FF`); `002693D0` (`002693F5`); +2 more |
| `+0x01A` | 2 |  | inside the store's `+0x18` row | 1 / 4 | `00262F90` (`00262FEC` +1) | `0025B820` (`0025B8F9`); `002693D0` (`00269415`); +2 more |
| `+0x01C` | 4 | uint32 | `flags1C` — **initial value by sequence** from `00266BD0` (`rec[3] & 0x1F`, jump table `00266C30`): 0 → `0`, 1–2 → `0x38`, 3–4 → `0x40`, 5–6 → `0x30004`, 7 → `0x34C85` (`00266BF6`–`00266C28`) | 4 / 16 | `00266BD0` (`00266BF6` +4); `0025AE00` (`0025AF07` +2); `ActorSystem_BindBattleUnitsForEligibleRecords` `00265A20` (`00265AC3`); `ActorSystem_InitializeManagerRuntime` `0026CE60` (`0026D23A` +2) | `0025B250` (`0025B2A6`); `0025B820` (`0025B943` +2); +14 more |
| `+0x01E` | 2 |  | inside `flags1C` (`+0x1C`) | 0 / 1 |  | `0025C230` (`0025C534`) |
| `+0x020` | 1 | uint8 | *not in the store* | 1 / 1 | `002E3AF0` (`002E3BE0`) | `002E3AF0` (`002E3BD0`) |
| `+0x024` | 2 | uint16 | *not in the store* | 2 / 1 | `00268B10` (`00268C04` +1); `ActorResource_RemoveActiveEntry` `003DB2A0` (`003DB3C9`) | `0025B580` (`0025B584`) |
| `+0x026` | 2 | uint16 | *not in the store* | 2 / 1 | `00268B10` (`00268C15` +1); `ActorResource_RemoveActiveEntry` `003DB2A0` (`003DB3CD`) | `0025B580` (`0025B58D`) |
| `+0x030` | 8 | void* | `battleUnit` | 1 / 12 | `002134A0` (`002134A0`) | `ActorSystem_ReleaseManagerRecords` `0025B070` (`0025B218`); `ActorSystem_BindBattleUnitsForEligibleRecords` `00265A20` (`00265AA4`); +10 more |
| `+0x038` | 8 | void* | *not in the store* | 1 / 1 | `ActorSystem_BindBattleUnitsForEligibleRecords` `00265A20` (`00265AA8`) | `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025E20E`) |
| `+0x040` | 8 | void* | **the actor's authored entry** in the image's `tableOff18` table (`0x30` bytes; planted at `00266734`) — [the binding page](../../01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md) §2.1; store row unnamed | 0 / 16 |  | `0025AE00` (`0025AEE1`); `0025B820` (`0025B959` +2); +14 more |
| `+0x048` | 8 | void* | **the script's function table** `{u32 count; {u32 nameOffInPool, u32 offsetWithinScript}[]}` (`image + resolve(entry.+0x10)`, planted at `002667A2`; indexed by `ActorScriptResource_GetBytecodeOffsetById`; BW-5 2026-09-12) — [the binding page](../../01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md); store row unnamed | 0 / 2 |  | `ActorResource_AllocateAndSubmitEntry` `003DBCF0` (`003DBCFA` +1); `ActorScriptResource_GetBytecodeOffsetById` `00358A00` (`00358A00`) |
| `+0x050` | 8 | void* | `payloadSectionA` — **the script's jump table** `{u32 count; u32 offsetWithinScript[]}` (`image + resolve(entry.+0x14)`, planted at `002667B9`; `FUN_003589E0` indexes it with the `JMP` family's immediate; BW-5 2026-09-12) — [the binding page](../../01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md) | 0 / 1 |  | `003589E0` (`003589E0`) |
| `+0x058` | 8 | void* | `payloadSectionB` — **the actor's bytecode base** (`image + entry.+0x08`, planted at `002667CA`); the pc is this plus the function table's offset — [the binding page](../../01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md) §2.2 | 0 / 5 |  | `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025E097`); `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`002618B3` +2); +3 more |
| `+0x060` | 1 | uint8 | `entryFreeListHead` | 3 / 3 | `ActorResource_RemoveActiveEntry` `003DB2A0` (`003DB3F9`); `ActorResource_AllocateAndSubmitEntry` `003DBCF0` (`003DBD7E`); `ActorResource_UnlinkEntryAndMarkFree` `003DC130` (`003DC160`) | `ActorResource_RemoveActiveEntry` `003DB2A0` (`003DB3E6`); `ActorResource_AllocateAndSubmitEntry` `003DBCF0` (`003DBD26` +1); +1 more |
| `+0x061` | 1 | uint8 | `detachedEntryListHead` | 2 / 4 | `ActorResource_RemoveActiveEntry` `003DB2A0` (`003DB35E`); `ActorResource_InsertEntryFromDescriptor` `003DB7A0` (`003DB980`) | `ActorResource_FindActiveEntryByIdOrClass` `003DBF60` (`003DBFBC`); `ActorResource_FindScriptRequestEntry` `003DC050` (`003DC05A`); +2 more |
| `+0x062` | 1 | uint8 | `selectedEntryIndex` | 1 / 2 | `ActorResource_SelectPendingEntryForExecution` `003DB6E0` (`003DB764`) | `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025E142`); `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`00261239` +3) |
| `+0x063` | 1 | uint8 | `entryListFlags` | 5 / 3 | `003DB1F0` (`003DB25A`); `003DB280` (`003DB28E`); `ActorResource_RemoveActiveEntry` `003DB2A0` (`003DB3F5`); +2 more | `003DB1F0` (`003DB222`); `ActorResource_SelectPendingEntryForExecution` `003DB6E0` (`003DB6E6`); +1 more |
| `+0x064` | 4 |  | **VM register I0** — `POPI0` (`0x36`) stores it, `PUSHI0` (`0x3E`) reads it; an actor-scoped int32 that survives between the actor's script functions ([the interpreter page](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md) §13; store row `UNRESOLVED` pending OPUS) | 1 / 1 | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`00261624`) | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`002616AF`) |
| `+0x068` | 4 |  | **VM register I1** — `POPI1` (`0x37`) stores it, `PUSHI1` (`0x3F`) reads it; an actor-scoped int32 that survives between the actor's script functions ([the interpreter page](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md) §13; store row `UNRESOLVED` pending OPUS) | 1 / 1 | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`00261635`) | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`002616C0`) |
| `+0x06C` | 4 |  | **VM register I2** — `POPI2` (`0x38`) stores it, `PUSHI2` (`0x40`) reads it; an actor-scoped int32 that survives between the actor's script functions ([the interpreter page](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md) §13; store row `UNRESOLVED` pending OPUS) | 1 / 1 | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`00261646`) | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`002616D1`) |
| `+0x070` | 4 |  | **VM register I3** — `POPI3` (`0x39`) stores it, `PUSHI3` (`0x41`) reads it; an actor-scoped int32 that survives between the actor's script functions ([the interpreter page](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md) §13; store row `UNRESOLVED` pending OPUS) | 1 / 1 | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`00261657`) | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`002616E2`) |
| `+0x074` | 4 | f32 | **VM register F0** — `POPF0` (`0x3A`) stores it, `PUSHF0` (`0x42`) reads it; an actor-scoped float32 ([the interpreter page](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md) §13; store row `UNRESOLVED` pending OPUS) | 1 / 1 | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`00261668`) | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`002616F3`) |
| `+0x078` | 4 | f32 | **VM register F1** — `POPF1` (`0x3B`) stores it, `PUSHF1` (`0x43`) reads it; an actor-scoped float32 ([the interpreter page](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md) §13; store row `UNRESOLVED` pending OPUS) | 1 / 1 | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`0026167B`) | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`00261706`) |
| `+0x07C` | 4 | f32 | **VM register F2** — `POPF2` (`0x3C`) stores it, `PUSHF2` (`0x44`) reads it; an actor-scoped float32 ([the interpreter page](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md) §13; store row `UNRESOLVED` pending OPUS) | 1 / 1 | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`0026168E`) | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`00261719`) |
| `+0x080` | 4 | f32 | **VM register F3** — `POPF3` (`0x3D`) stores it, `PUSHF3` (`0x45`) reads it; an actor-scoped float32 ([the interpreter page](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md) §13; store row `UNRESOLVED` pending OPUS) | 1 / 1 | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`002616A1`) | `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`0026172C`) |
| `+0x088` | 1 | uint8 | `slotCountA8` | 0 / 5 |  | `00266C50` (`00266CBB`); `ActorResource_FindActiveEntryByIdOrClass` `003DBF60` (`003DBF63`); +3 more |
| `+0x089` | 1 | uint8 | `slotCountA0` | 0 / 7 |  | `003DB1F0` (`003DB22F`); `ActorResource_FindActiveEntryByIdOrClass` `003DBF60` (`003DBF82`); +5 more |
| `+0x08C` | 1 | uint8[8] | `channelTail` | 1 / 1 | `ActorResource_RemoveActiveEntry` `003DB2A0` (`003DB3E0`) | `ActorResource_RemoveActiveEntry` `003DB2A0` (`003DB3D1`) |
| `+0x094` | 1 | uint8[8] | `channelHead` | 1 / 3 | `ActorResource_RemoveActiveEntry` `003DB2A0` (`003DB3AB`) | `ActorResource_SelectPendingEntryForExecution` `003DB6E0` (`003DB710`); `ActorResource_RemoveActiveEntry` `003DB2A0` (`003DB39D`); +1 more |
| `+0x0A0` | 8 | void* | `slotsA0` | 1 / 12 | `00266AD0` (`00266B79`) | `003DB1F0` (`003DB228`); `ActorResource_FindActiveEntryByIdOrClass` `003DBF60` (`003DBFCB`); +10 more |
| `+0x0A8` | 8 | void* | `slotsA8` | 1 / 4 | `00266AD0` (`00266B9B`) | `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025DFBF`); `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (`00261259` +5); +2 more |
| `+0x0B8` | 8 | void* | `contextPtr` | 2 / 67 | `00266AD0` (`00266AFE` +3); `00262F90` (`0026301F`) | `ActorSystem_ReleaseManagerRecords` `0025B070` (`0025B0C8` +5); `0025B250` (`0025B2AC`); +65 more |
| `+0x0C0` | 8 | void* | *not in the store* | 2 / 94 | `00266AD0` (`00266B05` +3); `00262F90` (`00263011`) | `00225CD0` (`00225D86` +5); `00225EB0` (`00225F66` +5); +92 more |
| `+0x0C8` | 2 |  | *not in the store* | 0 / 3 |  | `00269860` (`00269951`); `002652D0` (`0026530B`); +1 more |
| `+0x0CC` | 2 |  | *not in the store* | 0 / 2 |  | `0025B820` (`0025B99D` +1); `002675C0` (`00267657`) |
| `+0x0CE` | 2 |  | *not in the store* | 0 / 2 |  | `0025C830` (`0025CFA5`); `0025C230` (`0025C490`) |
| `+0x0D0` | 2 |  | *not in the store* | 0 / 2 |  | `0025C830` (`0025D32D`); `0025C230` (`0025C791`) |
| `+0x0D2` | 2 |  | *not in the store* | 0 / 2 |  | `0025C830` (`0025D27E`); `0025C230` (`0025C72C`) |
| `+0x0D4` | 2 |  | *not in the store* | 0 / 1 |  | `0025B2E0` (`0025B36C`) |
| `+0x0D6` | 2 |  | inside the store's `+0xD4` row | 0 / 1 |  | `00269860` (`002698C4`) |
| `+0x0D8` | 2 |  | *not in the store* | 0 / 2 |  | `0025C830` (`0025D122`); `0025C230` (`0025C60D`) |
| `+0x0DC` | 2 |  | *not in the store* | 0 / 4 |  | `0025AE00` (`0025AED5`); `0025B820` (`0025B94C`); +2 more |
| `+0x0DE` | 2 |  | *not in the store* | 0 / 2 |  | `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025E159`); `Actor_RequestConfiguredPrimaryResources` `00269640` (`00269719`) |
| `+0x0E2` | 2 |  | *not in the store* | 0 / 2 |  | `0025C830` (`0025D055`); `0025C230` (`0025C55D`) |
| `+0x0E8` | 2 | uint16 | *not in the store* | 0 / 2 |  | `00268EA0` (`00268F3F`); `0025BAD0` (`0025BCEA`) |
| `+0x0EA` | 2 |  | *not in the store* | 0 / 2 |  | `00268EA0` (`00268EF8`); `00263050` (`002631BB`) |
| `+0x0EC` | 4 | uint64 | *not in the store* | 2 / 0 | `002EB430` (`002EB443`); `002E6BD0` (`002E6C33`) |  |
| `+0x0F0` | 8 |  | inside the store's `+0xEC` row | 1 / 1 | `002EB430` (`002EB44D`) | `002EC3F0` (`002EC486` +2) |
| `+0x0F4` | 1 |  | *not in the store* | 0 / 3 |  | `00268D10` (`00268E5A`); `0025C830` (`0025D0CE`); +1 more |
| `+0x0F5` | 1 | uint8 | *not in the store* | 1 / 0 | `002EB430` (`002EB43C`) |  |
| `+0x0F6` | 2 | uint16 | *not in the store* | 2 / 1 | `0025AE00` (`0025AE5A`); `ActorSystem_InitializeManagerRuntime` `0026CE60` (`0026CF63` +4) | `00263D30` (`00263D30`) |
| `+0x0F8` | 8 | void* | *not in the store* | 0 / 1 |  | `00263990` (`002639A0`) |
| `+0x100` | 2 | uint16 | *not in the store* | 0 / 1 |  | `00263A10` (`00263A1A`) |
| `+0x102` | 2 | uint16 | *not in the store* | 0 / 2 |  | `00263990` (`00263994`); `00263A10` (`00263A10`) |
| `+0x107` | 1 |  | inside the store's `+0x106` row | 0 / 1 |  | `00263B80` (`00263B80`) |
| `+0x108` | 4 |  | *not in the store* | 1 / 0 | `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025E134`) |  |
| `+0x10C` | 4 | uint64 | *not in the store* — **stop set 2 (script execution) live bitset**; `+0x110`/`+0x114` are its pending set/clear words ([the stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) §5/§5a) | 1 / 3 | `00226640` (`0022673B` +1) | `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025E230`); `00264DF0` (`00264DF7`); +1 more |
| `+0x110` | 4 |  | inside the store's `+0x10C` row | 4 / 1 | `00225CD0` (`00225D80`); `00225EB0` (`00225F60`); `00226640` (`00226741`); +1 more | `00226640` (`00226731`) |
| `+0x114` | 4 | uint32 | *not in the store* | 4 / 1 | `00225CD0` (`00225D7A`); `00225EB0` (`00225F5A`); `00226640` (`00226754`); +1 more | `00226640` (`00226748`) |
| `+0x118` | 2 | uint32 | *not in the store* | 2 / 1 | `00268EA0` (`00268F81` +1); `0025BAD0` (`0025BCA2` +1) | `0025BAD0` (`0025BCAB`) |
| `+0x11A` | 2 |  | inside the store's `+0x118` row | 0 / 1 |  | `00268EA0` (`00268F76`) |
| `+0x120` | 0 | uint8[560] | `movementContext` | 0 / 1 |  | `00266AD0` (`00266B0C` +3) |
| `+0x140` | 0 |  | inside `movementContext` (`+0x120`) | 0 / 1 |  | `00266AD0` (`00266B47`) |
| `+0x1A0` | 0 |  | inside `movementContext` (`+0x120`) | 0 / 1 |  | `00266AD0` (`00266B26`) |
| `+0x4D8` | 0 | uint8[200] | `resourceEntryPool` | 0 / 1 |  | `00266AD0` (`00266B6F`) |

### 2.3 What nobody reaches

11 ranges totalling 37 bytes have no access on any enumerated route once the
store's declared spans (the four embedded sub-objects among them) are counted as covered
(re-counted 2026-09-11 from the generation-3 census: `+0x23`, `+0x2C`–`+0x2F`, `+0x84`–`+0x87`,
`+0x8A`–`+0x8B`, `+0x9C`–`+0x9F`, `+0xB0`–`+0xB7`, `+0xCA`–`+0xCB`, `+0xDA`–`+0xDB`, `+0xE0`–`+0xE1`,
`+0xE4`–`+0xE7`, `+0x11C`–`+0x11F`; `+0x2C`–`+0x2F` and `+0x9C`–`+0x9F` are new, uncovered since the
context reads at `+0x28` and `+0x98` were withdrawn). None of 32 bytes or more.

### 2.4 What the map says that no single page did

- **`+0xC0` is read by 94 functions** and `+0xB8` (`contextPtr`) by 66 —
  the two pointers at the end of the header are the record's most-followed links, and their one
  enumerated writer is `00266AD0` (211 B): it switches on the record's kind (`+0x03 & 0x1F`, 0–7,
  jump table at `00266AE7`) and points `+0xB8` / `+0xC0` **into the record's own embedded area at
  `+0x120`** (`+0x120`, `+0x120 + 0x80`, `+0x120 + 0x20`, `+0x120 + 0x230` by kind; `00266AFB`–`00266B68`),
  then derives `+0xA0` and `+0xA8` from the same base (`00266B79`–`00266B9B`) — the sub-object
  layout the record page's §12 derives, per kind.
- **`+0x03` (`packedKindAndSequence`) has 78 readers and no enumerated writer** —
  written by the allocator the record page reads, outside these routes.
- **`+0x09` (`flags09`) has 14 writers** — the most-written flag byte; `+0x0C`
  (`flags0C`) 9.
- **41 touched offsets have no store row**, each with cited sites to start from.
  *Re-measured 2026-09-27 (FABLE, Claude Opus 5.5, FI-1): the table now flags 34, and every one has a store row; the
  twelve in `+0xC8`–`+0xEA` are one `u16[18]` override array. Each is named in [the FI-1 record](../../_index/candidates/fi1-offset-names/README.md).*
- **The image-wide flag writer census** (SWE2-STRUCT EH-4, 2026-09-17; domain repaired
  2026-09-25 under `OPUS-REQ-STRUCT-FLAG-CENSUS-ADMITS-NINE-MNEMONICS`): every write in all
  38,161 listed bodies whose byte range covers `+0x08`, `+0x09`, `+0x0C`, `+0x0D`, `+0x0E`,
  `+0x13`, `+0x14` or `+0x1C`, where *write* is decided per operand by `reg_tracking.op_kind` —
  the earlier build's capstone access-flag gate silently dropped every SSE store, string op,
  atomic and bit op (movups stores alone: +15,276 rows). `actor-storage-record-flag-bit-writes.tsv`
  is now **121,759 rows** (`in_access_census` marks the functions already proven to touch the
  record), beside `actor-storage-record-flag-bits.tsv` (per bit:
  which writer classes can carry it, init coverage, census reader counts),
  `actor-storage-record-flags1c-initial-values.tsv` (the `00266BD0` jump-table cases, one row
  per sequence), queried with `select_flag_bits.py`. Headline, restated for the widened domain:
  `+0x13`'s byte-granular writes inside census functions are `0026D2E3`
  (`ActorSystem_InitializeManagerRuntime`) **and** `002666B0` (`and byte [rbx+0x13], 0x3C` —
  a mask clear, in `00266530`), plus SSE-width stores that cover it (`0025A1EB` movups
  `[r8+0x10]`, `003D9ED8` movups `[rdx+0x10]`, the `0026B05B`/`0026B12F` movss dword stores);
  the `flags1C` bits 8 / 13 the routes never saw written have image-wide writers at `00267CC0` /
  `00269FE0` (`or 0x100` / `or 0x2000` setters; `and 0xFFFFDEFF` clears both at once, the same
  mask the censused `00265AC3` uses).

> ### ⚠ `+0x002`: the store row was renamed, and this table's writer count is a census gap
>
> **Renamed 2026-09-12** from `prevActiveIndex` to **`actorIndexClass`** under
> `FABLE-REQ-OPUS-ACTOR-IMAGEPTRS`. The old name described it as an index and it is not one:
> `ActorStorage_InitializeRecord` writes `1 + (index < bound)` — `002666FC` reads the entry table's
> offset, `00266700` a bound word at that table's `+2`, `00266705`/`00266708` a **signed** `setl`,
> `0026670B` an `inc`, `0026670D` the store. **The field can hold only 1 or 2.** The sole reader,
> `002689F0`, compares it with the literal `1` and never indexes with it, so writer and consumer
> agree independently. What the two classes *select* is OQ FZ-25.
>
> **And the `0 /` in this row's writer column is wrong — not as a page error but as a census gap.**
> `0026670D mov byte ptr [rbx + 2], al` is a real write to this field and it is **not in
> `actor-storage-record-accesses.tsv`**, so the table above reports no writer for a field that is
> written by the record's own initialiser. The generation-3 `hop_scan` did not attribute `rbx` to
> the record at that point. Raised with FABLE, who own the census; the count is left as the census
> reports it rather than hand-edited, because a field map that silently disagrees with its own
> source is worse than one that shows the gap.

## 3. Key addresses

| address | what |
|---|---|
| `00358940`, `003588B0` | the two record-returning accessors used as seeds |
| `003DB2A0` | `ActorResource_RemoveActiveEntry` — the control (`+0x60` byte free-list head) |
| `00266530` | `ActorStorage_InitializeRecord` — the initialiser the store's rows cite |

## 4. Data structures and formulas

The store's `ActorStorageRecord` rows plus the writer/reader sites in §2.2; the full access list is
the TSV beside this page, one row per instruction with the route that reached it.

## 5. Call chain

Every function in the table reaches the record through one of the two accessors or receives it as
an argument; the TSV's `route` column records which, per access.

## 6. Modding notes

- **Reach the record through the accessors the engine uses** (`ActorManager_GetRecordByOrdinal`,
  `ActorHandle_ResolveRegistryEntryByPackedId`); the handle is not a pointer and does not survive
  slot reuse ([the record page](the-record-behind-every-actor.md)).
- **The untouched ranges are not free space**: the embedded sub-objects and the unfollowed routes
  live there.

## 7. What is not known

- [x] **UQ-93.** **The names of the 41 touched offsets without a store row**, starting with the
  most-read among them. **FI-1.**
  *ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: all 34 flagged offsets have store rows and a meaning -
  the store's, a reference, or a reading - in [the FI-1 record](../../_index/candidates/fi1-offset-names/README.md) (control `fi1_offsets.py`, 10 checks).*
- [x] ~~**The writers the routes do not reach** — `+0x03` and the other read-only header bytes are
  written by the allocator / initialiser path the scan does not seed.~~ **FI-2 ANSWERED 2026-09-12
  (FABLE) — enumerated on that path.** `ActorStorage_AllocateAndInitializeRecords` (`002679F0`, the
  only caller of the initialiser by a function-list-independent `E8`/`E9` index) writes **`+0x03`**
  per record at `00267B04` / `00267B13`: `(old & 0xE0) | (kind & 0x1F)`, then `| (sequenceByte << 5)`
  — the packed kind (low 5 bits) and sequence (high 3) the 78 readers consume — and `+0x08` (word)
  at `00267B53`. `ActorStorage_InitializeRecord` (`00266530`) writes the rest of the header: `+0x00`
  word (`002665EB`), `+0x02` (`0026670D`), `+0x04` word `0xFF00` (`00266692`), `+0x08` (`002665FD`,
  `0026663E`, `00266677`, masked `0x7F` at `0026667A`), `+0x09` (`002665C8` `& 0xDF`, `002666A8` `& 0x7F`),
  `+0x0A` (`002667C6`), `+0x0B` (`00266643`, `00266660`), `+0x0C` (`0026661B`, `0026667E`, `002666AC`),
  `+0x0D` (`002665F7`, `00266639`, `00266669`, `0026666C`), `+0x0E` (`0026665A` `| 0xF0`, `002666F8`),
  `+0x0F` (`00266682`, `00266771` = 3, `00266792`), `+0x10` word (`002665F2`). **FI-2.**
- [x] **UQ-94.** **The sub-objects' interiors** — accesses through interior pointers the scan does not follow.
  **FI-3.** **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5) by reference: each interior is censused on the pointer the planter
  stores, and typed in the store.** This page's scan does not follow those pointers; the pages below do.
  - `+0x120` is the movement context and `+0x350` the secondary context: [the context censuses](../Actor-Contexts/the-movement-and-secondary-context-censuses.md)
    §2.3 and §2.4, typed as `MovementContext` and `SecondaryContext`.
  - `+0x4D8` is the resource-entry pool (`ActorResourceEntry`) and `+0x5A0` the wait-slot array (`ActorWaitSlot`):
    [the record page](the-record-behind-every-actor.md) and the census page's `FS-3`.
  - These are the sequence-5..7 shapes; the planter switches on the record's sequence.
  - Control: [`fi3_subobject_interiors.py`](../../_index/candidates/fi3-subobject-interiors/fi3_subobject_interiors.py) (3 checks, FAILS 0).

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| Every row of the table | `actor-storage-record-accesses.tsv`; `hop_scan.py --retseed 00358940,003588B0 --argseed 00266BD0:0 --size 0x6E0 --depth 3`, control `003DB2A0:0x60` found (generation-3 scanner, 2026-09-11) | 1 | PROVEN |
| The names in the store column | `_types/fields.tsv` (OPUS's rows, each citing its site) | 1 | PROVEN (by reference) |
| The untouched ranges | absence on every enumerated route with a passing control | 1 | PROVEN (for those routes) |
| Flag-bit writer candidates beyond the census seeds | `actor-storage-record-flag-bit-writes.tsv`, `actor-storage-record-flag-bits.tsv`, `actor-storage-record-flags1c-initial-values.tsv` (all 38,161 bodies; controls `00265AC3`, `00267CC0`, `00269FE0` captured) | 1 | PROVEN (as a census of displacements; ownership per row unproven) |

## 9. Related

- [`the-record-behind-every-actor.md`](the-record-behind-every-actor.md) — the record's semantics, allocator, handle and sub-objects.
- [`../Actor-Manager-Record/the-actor-manager-record-field-map.md`](../Actor-Manager-Record/the-actor-manager-record-field-map.md) — the record this one was confused with.
- [`../Battle-Unit/the-battle-unit-field-map.md`](../Battle-Unit/the-battle-unit-field-map.md) — the unit whose `+0x10` is this record.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every cited access site in this map was disassembled and its displacement compared with the offset of
the row citing it, by
[`check_field_citations.py`](../../../Tools/analysis-kit/gfz-scripts/check_field_citations.py):
**218 sites across 86 rows**.

| outcome | sites |
|---|---:|
| displacement **is** the row's offset | **215** (**98.6 %**) |
| resolved through an embedded sub-object base | 3 |
| other — indexed, a cited datum, or control flow | 0 |

**Nothing failed to decode, and no site contradicts its row.** Sub-object bases (2 distinct):
`+0x120` x2, `+0x350` x1.

**98.6 % direct is the highest of the eight maps checked** — against the save payload's 15.7 %. The contrast is structural, not editorial: this record is reached from its own base almost everywhere, while the save payload is reached through embedded sub-blocks. **A field map's direct-citation rate measures how much of its record is addressed as itself.**

**Not claimed:** this checks that each citation touches the offset it is filed under. It says nothing
about fields the census never reached; the document's own coverage limits stand unchanged.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT and SERVICE.** Cited functions are called by `MainLoop_UpdateAndRenderFrame` and the 2,001-byte core frame body. They call four small core helpers (7, 27, 61 and 93 bytes).
- **Status_Periodic_Terminal — CLIENT.** One cited function is called by five status bodies: `BattleStats_RecomputeDerivedStateAndAutoStatuses`, `BattleStats_ChangeStatusAndProcessSideEffects`, `BattleStats_RemoveStatusesFromMaskAndRecompute`, `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` and `BattleFormula_BuildRuntimeCounterPeriodicHpCredit`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Audio — SERVICE.** `0025D9E0` on this page calls `FUN_00261f90`, owned by that layer. What it reaches is a per-object audio state step: it needs `[obj+0x28] == 0` and bit 6 of `byte[obj+0x10]` clear, then sets bit 5 of that same byte and notifies through `0037C910`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `0031B810` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — SERVICE.** `0025D9E0` on this page calls `FUN_00234150`, owned by that layer. What it reaches is a 104-byte registration helper that takes the `.text` address `002FED60` as a callback and gates on `byte[+0] & 0x10` of what `0031B810` returns; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Items_Equipment_Shops_License — CLIENT.** `Inventory_QueryOwnedCountIncludingReservedActionItems`, owned by that layer, calls `0031B810` on this page. That caller is the owned-count query for an item id, which returns `-1` for the sentinel id `0xFFFF`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — CLIENT.** `PartyControl_ApplyAnalogLocomotionToActor`, owned by that layer, calls `00264DF0` on this page. That caller is the analog locomotion apply, gated twice before it touches anything: a party query must answer non-zero and the per-slot availability test must answer zero; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `Reward_ComputeExperienceForRecipient`, owned by that layer, calls `0031B810` on this page. That caller is the experience computation for one recipient: it needs `byte[rec+5] == 0` and takes its context from `0031B860`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Story_Event_Quest_Hunt — SERVICE.** `0026C8C0` on this page calls `EventMemory_QueryDefinitionIdAbsent`, owned by that layer. What it reaches is a 62-byte linear scan of the counted table at `[02ADD0A8]` that answers **1 when the id is NOT present** - the sense is inverted from what the name suggests on a quick read; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (10 edges through 6 of this page's functions).** The UI layer reaches this page at `002647E0`, `002B0280`, `0025B4C0`, `0026CE60` and 2 more. `FUN_00253a30` is the worked example, read in full - it is a 67-byte teardown: eight calls in fixed order, `[020927C8]` and `[020927CC]` zeroed, and a tail-jump to a ninth; **2 of the 7 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 24 edges).** `0026C8C0` applies the
render-fade configuration family — `CharacterRenderSystem_SetFadeWidth`/`SetFadeStartDistance` plus
the six `CharacterRenderConfig_*` getters and setters — and `0025DF00` calls `003E68B0`/`003E6EF0`/
`003E6A70`; `002E5180` reaches `CharacterRenderQuerySupport` `002E8000` and `00420A10`. Caller-side,
`ActorOverlapDrivenTransparencyFadeUpdate` `00256F60` calls `002EA6A0`,
`BattleUnit_BroadcastPartyCombatTargetRelation` and `PartyCombat_UpdateStanceState` call `0031B810`,
`00358940` fans in to four Presentation bodies, `00263990` is reached by ShaderMaterial `002B0280`,
and the glyph-batch flush `001E8580` calls `002134A0`. The storage record is consulted by and
configures the render layer — the fade-parameter writes are the substantive crossing.

**CombatFormula — MECHANICAL (SWE2-CONTRACT 2026-09-15, 36 edges).** Same shape as the manager-record row: all 36
edges are CombatFormula bodies (`BattleFormula_ApplyPreResolutionTargetGates`,
`BattleFormula_ApplyResultMetadata`, `BattleFormula_RollAvoidGuardParryOutcome`,
`BattleFormula_EvaluateTargetPreview`, `BattleFormula_DispatchPostResultEvents`,
`BattleStats_ModifyHPAndProcessLethalState`, …) calling the cited owner resolvers
`0031B860`/`0031B810`. Shared "find owning battle unit" fan-in.

**Input — MECHANICAL (SWE2-CONTRACT 2026-09-15, 8 edges).** `00225CD0`/`00225EB0` call the input helpers
`00182D40`/`00182D60`/`00182DA0` (6 edges); `InputGameplay_ArbitrateDigitalInputAndModalState`
shares `0025B4C0`; `Input.ActorControlMaskPropagationRuntime` `00226BE0` shares `00358940`.

**Script_VM_Native_Bridge — CLIENT (SWE2-EC7-164, 102 edges, one fan-in).** The math helpers this page's `003A1C90` cites (`00202E10` and family, the `0025Axxx`/`0025Bxxx`/`0025Dxxx` leaves) are called across the script VM / native bridge layer (`00340970`, `00268850`, `0025E4C0`…) — one shared helper set with a wide caller fan, not field-map plumbing.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Save_Load_Settings — SERVICE (3 edges).** `ActorManager_RunFieldRuntimePass` (`0025D9E0`) calls `SaveWrite_GetBusyFlag` (`00583920`, a 7-byte read of `02CA99E8`) at its head and branches on it, and calls `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) twice to test bit `0x40` of payload byte `+0x1063` and read the id at `+0x1534`; `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) calls `002EF2B0` and stores the payload base into the manager record at `+0x48`. The field pass defers to a save write in progress and reads one override id from the persistent payload, and the bind caches the payload's address in the manager record; the save layer owns the payload and the flag, and this page only reads them.

**Spawn_Encounter_Lifecycle — CLIENT (7 edges).** `SpawnGroup_UpdateExpectedMemberLaneMask` (`00306E60`) and `SpawnGroup_RecordMemberDeathAndHandleCompletion` (`00306F00`) call `00263D30`, the 8-byte reader of the record's word `+0xF6`; `SpawnUnit_FinalizeSpawnEntryActivation` calls `BattleUnit_SetupEngagedActionState` (`002FED60`); `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`) and `SpawnLifecycle_CheckAndRetireByNativeRange` (`002350C0`) call `FieldData_GetActiveFieldRecordBit15` (`00313F60`, a 5-byte jump to the field predicate); and `Spawn_TrySelectCandidatePosition` (`00234AF0`) and `002350C0` call `BattleUnit_GetPartyLeader` (`003272A0`). The spawn lifecycle reads a group member's `+0xF6` word through this record's accessor and uses the same leader and field-bit accessors this page cites; it consumes the record, it does not lay it out.

## The `0025B2E0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0025B2E0` (~185 B) — storage-record op under a wide save prologue.

| member | role | interior |
| --- | --- | --- |
| `003A17D0` | EH float body — `rbx = r9`, xmm6/xmm7 saved (`003A17E9`) | [`003A17E9`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `0026AE90`/`002E70E0` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

`0026AE90` (`Movement_SetSteeringMode`, ~73 B) — `(byte[+3] & 0xE0) ==
0x60` selects `qword[+0xB8]`, `edx - 2` in {0,1} the mode
(`0026AE9D`/`0026AEAD`).

| member | role | interior |
| --- | --- | --- |
| `002E55C0` | mode clear — `[[rdx+0xF0]+0x29] = 0`; `(byte[+0x28] & 0x7F)` vs 2 (`002E55D0`/`002E55E4`) | [`002E55D0`](../../_index/ADDRESS-INDEX.md) |

`002E70E0` (~60 B) — `003588B0(rdx)` record resolve, null-gated
(`002E70E9`/`002E70F1`).

| member | role | interior |
| --- | --- | --- |
| `003E65E0` | `word[+2] - 0xE` switch arm (`003E65EA`/`003E65F1`) | [`003E65EA`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003588B0`.


## Interior citation — frontier hub `002647B0` (2026-09-18, SWE2-EC7)

`002647B0` — 13 B, 10 callers; the `+0x12` mode bound-check this map's readers share.
Interior verified: `movsx edx, byte [rcx+0x12]` then `cmp edx, 3; setbe` at
[`002647B0`–`002647B9`](../../_index/ADDRESS-INDEX.md) — returns `+0x12 <= 3` as a boolean.
The storage record's mode byte is meaningful in `0..3`; higher is "no mode".

## SWE2-EC7-22 update (2026-09-18) — the `+0x400` sub-record accessor family

Four sibling accessors on the storage record's `[+0x400]` sub-object:

`003E56A0` (24 B): `[rcx+0x400]` -> `[rdx+2]` word, `rdx + word` returned as
`cdqe` — the sub-record base+offset pointer. Interior anchor `003E56AF`.

`003E56C0` (32 B): same shape on `[rdx+0x12]`, with the word's zero test
returning null — the tagged next-pointer variant. Interior anchor `003E56CF`.

`003E58B0` (88 B): the stat modifier — `[rdx+0x12]` nonzero gate, then
`xmm0 = [rcx+0x260] * [rcx+0x160] * [rcx+0x26C]` triple product, the
`[rcx+0x284] & 0x40000` flag selecting `* [rdx+0x30]` vs `* [rdx+0x34]`;
no sub-record -> `[00D117B8]` default. Interior anchor `003E58CF` (the flag
test).

`003E57B0` (25 B): the sibling channel — `xmm0 = [rcx+0x268] * [rcx+0x168] *
[rcx+0x26C]`, no flag select. Interior anchor `003E57B8` (the first `mulss`).

Callers span the getter cluster (`003A4290`/`003A56F0` on this page's manager
side, `003E65E0`/`002E8000`, `0042xxxx` render-zone consumers) — the family
reads the storage record's `+0x284` flags and `+0x400` sub-object the field
map documents.

## SWE2-EC7-75 update (2026-09-19) - `002E6570` + `002E63D0` table sweeps measured

`002E6570` (44 B) is the `02161DA0` SecondaryContext-table `+0x40`
zeroing: 32 iterations, `0x120` stride, `dword[rec+0x40] = 0` each -
the field clear the storage-record family runs.
Interior anchor `002E6592` (the `+0x40` store).

`002E63D0` (67 B) is the `0215FDA0` paired bit-4 clear: 64 iterations,
`0x80` stride, index `r8d` stepping by 2 from 1 - clears `+0x19` bit 4
on record `r8-1` (bound-checked) and record `r8` (when `<= 0x7F`) -
the sweep that resets the NameBindingEntry flag bit across the table.
Interior anchor `002E63EE` (the `and byte [rcx+0x19], 0xEF` clear).

## SWE2-EC7-90 update (2026-09-20) - `003A1BB0` angular threshold measured

`003A1BB0` (154 B) is the angle predicate the storage callers
run: `00861F02` on the two coordinate deltas yields the heading,
`xmm6` is subtracted, the result is wrapped into
[-2pi, +pi] by the `C0C90FDB`/`40490FDB` loops, and the body
returns 1 only when `|angle|` stays under `xmm7`.
Interior anchor `003A1BD8` (the `00861F02` call).

## SWE2-EC7-95 update (2026-09-20) - `0031E7B0` measured

`0031E7B0` (74 B) is the indexed dword read `003B6CC0` and
`003B6D60` call: `00322C50(0x17, ecx, 0)` gates the lookup,
`byte[02EBB1xx + ecx*2 + 0x5A5A]` supplies the key (`0xFF` when
the gate fails), `002367A0` resolves it, and `[rax+8]` is the
dword returned (0 on a null resolve).
Interior anchor `0031E7E1` (the `002367A0` call).

## SWE2-EC7-98 update (2026-09-20) - `00428FE0` measured

`00428FE0` (60 B) is the flag-word update `002E3AF0`,
`002E6420` and `002E92F0` tail into: `[+0x304]` bit 4 is
cleared then re-set iff `edx != 0` (the `neg`/`sbb`/`and 0x10`
idiom), and `[+0x290]` takes `0x4000000` when `edx != 0` and
`byte[+0x294] & 8` is clear, `0x8000000` otherwise - the
paired flag writes the record's state arms apply.
Interior anchor `00429006` (the `0x4000000` or).

## SWE2-EC7-104 update (2026-09-20) - `0026B500` measured

`0026B500` (32 B) is the flag-bit writer
`003B6CC0`, `003B6D60`, `003B7C60` and
`003B7D30` call on a record's `+0x0D` byte:
it clears bit 1 and ORs `(edx != 0) << 1`
back in, then tails `002EA970` - the
predicate-to-bit publish the storage arms
share.
Interior anchor `0026B509` (the bit clear).

## SWE2-EC7-107 update (2026-09-20) - `00237F40` measured

`00237F40` (118 B) is the gated
enumeration `0025C830` and
`0026C3E0` run: `003272A0()`
resolves the record, `02089340`
bits 9 and 10 must both be armed,
and the record path - `byte[rax] &
4`, `[rax + 0x698]` live,
`([+0x64] | [+0x3C]) & 0x80000003`
armed and `00313F60()` nonzero -
vetoes the walk; surviving the gates runs
`0030A880(rbp, 3)` and, when it
counts > 0, `00327810([[rbp]])` -
the two-bit gate in front of the
storage-record pass.
Interior anchor `00237F5A` (the
`bt ecx, 9`).

`002E4A10` (35 B) is the tag-gated vec3 mirror on the storage record: `byte[rcx + 3] & 0xE0 == 0x60` selects the record class, then `qword[rcx + 0xB8]`'s first three dwords copy verbatim to its `+0x10`/`+0x14`/`+0x18` - the class-0x60 position dup the actor-storage and battle-unit callers lean on.

Interior anchor `002E4A1A` (function `002E4A10`).

`003DB650` (133 B) is the link-record splice: `r8 = [rcx+0xA0] + r11*20` addresses the target row (index `0xFF` or a null record yields `r8 = 0`), the `edx`-indexed sibling row in the same 20-byte chain threads `byte[+1]` links both ways - `r8`'s takes the old next (or `0xFF`), the `edx` row's takes `r11`, `r10`'s takes `r11` too - and `byte[r8] = dl` writes the owner - the storage-chain weave the actor-storage callers share.

Interior anchor `003DB6B5` (function `003DB650`).

`003A1C90` (158 B) is the two-delta normal `003A17D0` calls: it builds `rdx - rcx` and `r8 - rcx` as vec3s on the stack, `00202E10`s them into a cross/normal at `[rsp+0x40]`, and returns `[rsp+0x44]` - the middle component of the plane between two position pairs

Interior anchor `003A1D11` (function `003A1C90`).
