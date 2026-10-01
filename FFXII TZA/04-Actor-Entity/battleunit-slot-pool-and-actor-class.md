---
system: BattleUnit slot pool and actor class
category: 04-Actor-Entity
status: AUDITED
owner_layer: PrimaryOwner:ActorEntity
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
registry_slots:
  - "0x02EBF1A0"
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 1
---

# BattleUnit slot pool and actor class

> **Thirty-two.** That is the fixed number of things that can be in a battle at once — party,
> guests and every enemy share one pool of 32 slots — and a three-bit class field decides what each
> actor is even allowed to do.

## 1. What the player sees

Two hard limits sit behind a lot of FFXII's behaviour.

**Combat participation is a pool.** Anything that fights occupies one slot in a fixed-size
array. When the array is full, the next thing that tries to join simply does not — no error,
no message, it just is not there.

**Not every actor is the same kind of thing.** A small class field decides whether something
can be moved, whether its position can even be read, and what systems will touch it. A
treasure chest, a party member and a monster are not interchangeable to the engine, and the
difference is three bits.

## 2. Native mechanism

### Actor class — three bits, two different readings

The class lives in the top three bits of `bActor_class_flags`, and different subsystems
require different values:

```c
class = actor->bActor_class_flags >> 5;          // top three bits

Actor_GetWorldPosition:   requires class == 1 || class == 3
Movement functions:       require (flags & 0xE0) == 0x60,  i.e. class == 3
```

So **class 3 can both move and be positioned; class 1 can be positioned but not moved.** That
is a real capability split, and it is why some world objects have a readable position yet
never respond to movement calls.

A separate accessor reads the **low** nibble of a different byte:

```c
ActorRuntime_GetClassNibble(actor):  return actor[0x0E] & 0x0F;   // 0 if actor is NULL
```

Low nibble at `+0x0E` and the top three bits of `bActor_class_flags` are **two distinct
fields**. ~~Whether they occupy the same byte is not established — do not assume it.~~ They do not
(M-2, §7): the class bits are byte `+0x03`, the nibble byte `+0x0E`.

**The enumeration (M-1, 2026-09-12, FABLE).** The class is the **layout class** the actor-record
carver stamps from its descriptor table at `01E0C328` — eight sequences, four classes
([the record page](Actor-Storage-Record/the-record-behind-every-actor.md) EH-2, [the pool contract](CONTRACT-actor-record-pool-and-region-map.md)): class **0** (sequence 0, 808 B), class **1** (sequences 1–2,
936 / 816 B), class **2** (sequences 3–4, 840 / 720 B) and class **3** (sequences 5–7, 1,760 / 1,760 /
1,640 B — the `ActorStorageRecord` every steerable actor is). **Classes 4–7 are never carved**; how
many records of each class exist is authored per area (the bound definition payload's count table).
An image-wide census of the tests that follow an `and …, 0xE0` on the byte: **142 sites in 126
functions require class 3**, the position accessor admits 1 or 3 (§2), and exactly **one** site
requires class **2** — the `setline` verb (`0x001C`, six float arguments, `00351610` at `00351682`–
`00351684`, [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)), so a class-2 record is the one a script can give a line to. No test
names class 0 or 1 alone; what those records hold is the residue, reachable through the per-area
counts. *Resolved 2026-09-12 (BV-4):* the decompiled scripts declare each actor with its sequence,
so class 0 is the script-only controller (`__MJ_CTRL`, `Map_Director`, `setup`, …), class 1 the placed
never-moving object (doors, switches, warps), class 2 the trigger line (`setline`, consumed by the
line pass `0025B250`) and class 3 the steerable actor — see
[the movement-mode page](../06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md).

### The BattleUnit slot pool

```c
void BattleUnit_AllocateSlotAndBindActor(int reserved_zero, WorldActor *actor_work)
{
    slot = g_pBtlWorkArray;  i = 0;
    while (slot->qwUnitFlags & 1) {              // bit 0 = slot in use
        i++; slot++;
        if (i >= g_nBattleUnitSlotCount)
            return;                              // POOL FULL - silent failure
    }
    memset(slot, 0, 0xF50);                      // BattleUnit is 3920 bytes
    slot->qwUnitFlags |= 1;                      // claim it
    slot->bBattle_slot_index = (byte)i;
    f_002134A0(actor_work, slot);                // bind
    slot->pActorWork = actor_work;
    slot->dwFieldId  = ActorHandle_EncodeRegistryEntry(actor_work);
    ...
}
```

Four things worth stating plainly:

**Allocation is a linear first-free scan** over `g_pBtlWorkArray`, using bit 0 of
`qwUnitFlags` as the in-use marker.

**A full pool fails silently.** The function returns having done nothing. No flag, no return
value, no diagnostic — the caller cannot tell allocation failed from this function alone.

**What the caller does about it (M-6, read 2026-09-12, FABLE).** The allocator has exactly **one**
caller, `ActorSystem_BindBattleUnitsForEligibleRecords` (`00265A20`), the walk over the actor
manager's records (`[manager + 0x20]` of them, `ActorManager_GetRecordByOrdinal`) that binds a unit
to every record whose `+0x14` is `≥ 0x80` (bit 7, *battle-unit eligible*; [the actor storage record map](Actor-Storage-Record/the-actor-storage-record-field-map.md)). It guards
the pool **before** the call: it counts the records it has bound in this walk and, once the count
reaches **32** (`cmp edi, 0x20 / jge`, `00265A8F`), it does not call the allocator at all — it clears
the record's `+0x14` bit 4 instead (`00265B11`–`00265B13`, the "cleared when the unit pool is full"
the record map records) and does not count the record. And it **does detect** a silent failure
after the call: the allocator plants the unit back-pointer at the actor's `+0x30` (`002134A0`, on
the success path only, `002344E7`), so the caller's `test [rbx + 0x30]` (`00265AA4`–`00265AAF`)
sees null when no slot was free and **skips only the post-bind step** `00234A00(actor, 1)`. What
it does not do is correct or report it: `r14d = 1` was set before the call (`00265A99`), so the
record's free-target nibble is still stamped (`00265ACA`–`00265ACE`), the record is still counted
into the bound total the walk stores at `[manager + 0x1E8]` (`00265B18`–`00265B3B`), and the rest of
the per-record work runs as if a unit existed. So a genuine failure — which needs a slot held by a
unit this walk did not allocate, since the walk's own count stops at the pool size — leaves an
eligible actor with no unit and nothing that says so. The back-pointer test is only as good as the
release path's clearing of `+0x30` (`ActorSystem_ReleaseManagerRecords`, `0025B218`).

**A BattleUnit is `0xF50` = 3,920 bytes**, zeroed in full on allocation, so no state survives
a slot's reuse.

**Identity is captured at bind time.** `dwFieldId` receives
`ActorHandle_EncodeRegistryEntry(actor_work)` — an encoded registry handle, not a raw pointer.

### Slot access

```c
int BattleUnit_GetSlotCount(void) { return g_nBattleUnitSlotCount; }

BattleUnit *BattleUnit_GetBySlotIndex(int i)
{
    if (i >= 0 && i <= g_nBattleUnitSlotCount - 1)
        return g_pBtlWorkArray + i;
    return NULL;                                  // fails closed
}
```

Bounds-checked both ends, returning `NULL` out of range.

## 3. Key addresses

| Address | Name | Verified |
|---|---|---|
| `00234480` | `BattleUnit_AllocateSlotAndBindActor` | ✅ read |
| `00236820` | `BattleUnit_GetBySlotIndex` | ✅ read |
| `00236850` | `BattleUnit_GetSlotCount` | ✅ read |
| `00263C20` | `ActorRuntime_GetClassNibble` | ✅ read |
| `00265020` | `Actor_GetWorldPosition` | ✅ read |
| `00234200` | `ActorSystem_ReleaseBattleUnitSlotForActor` | not read |
| `00236A60` | `BattleUnit_ResetStateForReuse` | not read here; read on [the unit-definition page](Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) (among much else it nulls `+0x698`, `+0x6A0`, `+0xE60` and `+0xE68`; pointer added 2026-09-29, FABLE) |
| `002368D0` | `BattleStorage_InitializeWorkArrays` | ✅ read 2026-09-15 (§12) |
| `002134A0` | *(actor↔BattleUnit bind)* — plants the unit pointer at actor `+0x30` (§11) | ✅ read |
| `00265A20` | `ActorSystem_BindBattleUnitsForEligibleRecords` — the allocator's only caller (§2) | ✅ read 2026-09-12 |
| `00263D30` | the actor's entry-group word `+0xF6` (`setentrygroup` / `setentrygroupall`), copied to unit `+0x57` at bind | ✅ read 2026-09-12 |
| `003589B0` | `ActorHandle_EncodeRegistryEntry` | ✅ read 2026-09-10 |
| `0031B760` | *(actor → BattleUnit, with a NULL guard)* | ✅ read 2026-09-10 |
| `00263E30` | *(actor → BattleUnit, the raw load)* | ✅ read 2026-09-10 |

## 4. Data structures and formulas

```
WorldActor
  bActor_class_flags     u8    top 3 bits = actor class
  +0x0E                  u8    low nibble = a separate class nibble
  pMovement_state_ptr    ptr   -> movement state; position is its first 3 floats

BattleUnit                     0xF50 bytes (3,920), zeroed on allocation
  qwUnitFlags            u64   bit 0 = slot in use
  bBattle_slot_index     u8    its own index in the pool
  pActorWork             ptr   -> bound WorldActor
  dwFieldId              u32   encoded actor registry handle

Globals
  g_pBtlWorkArray        ptr   base of the BattleUnit pool
  g_nBattleUnitSlotCount i32   pool capacity
```

**Actor class:**

```
class = bActor_class_flags >> 5

position readable  iff  class == 1 || class == 3
movement permitted iff  class == 3          (i.e. (flags & 0xE0) == 0x60)
```

**Position read:**

```
(x, y, z) = movementState[0], movementState[1], movementState[2]
```

**Slot allocation:**

```
i = first index in [0, g_nBattleUnitSlotCount) with (slot[i].qwUnitFlags & 1) == 0
if none:  return silently
else:     memset(slot, 0, 0xF50); slot.qwUnitFlags |= 1; slot.bBattle_slot_index = i
          slot.pActorWork = actor;  slot.dwFieldId = EncodeRegistryEntry(actor)
```

**Slot lookup:**

```
slot(i) = (0 <= i < g_nBattleUnitSlotCount) ? g_pBtlWorkArray + i : NULL
```

## 5. Call chain

```
something needs to enter combat
  -> BattleUnit_AllocateSlotAndBindActor(0, actorWork)
     -> linear scan for a free slot
        -> pool full : return, nothing happens
     -> zero 0xF50 bytes, claim bit 0
     -> 002134A0 bind, store pActorWork
     -> ActorHandle_EncodeRegistryEntry -> dwFieldId

leaving combat
  -> ActorSystem_ReleaseBattleUnitSlotForActor
  -> BattleUnit_ResetStateForReuse
```

**Upstream:** spawn/encounter lifecycle and party setup.
**Downstream:** everything combat — the slot is the unit's combat existence.

**Do not confuse with:** the class *nibble* at `+0x0E` and the class *bits* in
`bActor_class_flags`. Different fields, different readers.

## 6. Modding notes

- **The BattleUnit pool is fixed and fails silently when full.** If a mod raises spawn counts
  and things stop entering combat with no error, this scan is the first place to look.
- **A BattleUnit is 3,920 bytes and fully zeroed on allocation** — nothing carries over from a
  previous occupant, so per-unit state cannot be stashed across reuse.
- **Class 3 moves, class 1 only has a position.** Before wondering why an actor ignores
  movement calls, check `bActor_class_flags >> 5`.
- **`dwFieldId` is an encoded registry handle, not a pointer** — the right thing to carry when
  you need to refer to a unit later.
- **XIIOnline:** the slot index is a *local pool position* and must never be a wire identity;
  two clients will allocate different indices for the same logical unit. `dwFieldId` is closer
  to identity but is still locally encoded. Pool exhaustion is also a divergence risk — a
  client whose pool fills will silently miss units another client has.

## 7. What is not known

- [x] ~~What actor classes other than 1 and 3 mean, and the full class enumeration.~~ **M-1
      ANSWERED 2026-09-12 (FABLE):** the four carved layout classes 0–3 of the descriptor table
      `01E0C328` (4–7 never carved); 142 sites require 3, one — `setline` — requires 2, the position
      accessor admits 1 or 3; what classes 0 and 1 hold is the residue (§2).
- [x] ~~Whether the `+0x0E` nibble and `bActor_class_flags` are the same byte.~~ **M-2 ANSWERED
  2026-09-12 (FABLE): no.** `bActor_class_flags` is the record's byte `+0x03` — `(kind << 5) |
  sequence`, written by the carve loop ([the actor storage record map](Actor-Storage-Record/the-actor-storage-record-field-map.md)) — and the nibble is the low half of byte
  `+0x0E`, the actor's **free-target type** (`setfreetargettype`, `btlAtelSetUnitType`; [the kind-byte page](Battle-Record-Kind/battle-record-kind-byte.md) AL-3).
- [x] ~~The value of `g_nBattleUnitSlotCount` — the actual combat capacity.~~ **M-3 ANSWERED 2026-09-02 (§9): 32.**
- [x] ~~What `002134A0` does at bind~~ **ANSWERED 2026-09-10, §11** — it is two instructions,
      `mov [rcx+0x30], rdx; ret`: it plants the **back-pointer** in the actor. ~~`00263D30`'s
      class-derived value is still unread. **M-4, half open.**~~ **M-4 closed 2026-09-12 (FABLE):**
      `00263D30` is two instructions — `movzx eax, word ptr [rcx + 0xF6]; ret` — and the word is the
      actor's **entry group**: `setentrygroup` (`0x00AC`, `0034FA70` → `0025AD10`, `0025AD34`) writes
      one actor's, `setentrygroupall` (`0x00BE`, `00340970` → `0025AE00`, `0025AE5A`) every record's,
      and the manager initialiser seeds it with the record ordinal (`0026CF63`). The allocator copies
      its low byte to unit `+0x57` (`00234509`) — **the lane byte** the spawn-entry queries read as a
      signed index into the keep's lane map ([the battle-unit field map](Battle-Unit/the-battle-unit-field-map.md); [the keep-entry page](../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)). Not class-derived.
- [x] ~~How `ActorHandle_EncodeRegistryEntry` encodes~~ **ANSWERED 2026-09-10, §11.**
      Whether it is stable across a slot's lifetime is still open, and now sharper: the
      encoding's high field comes from actor `+0x16`, which the actor initialiser sets to
      **1** — ~~and **no incrementer has been found**~~ **M-5 ANSWERED 2026-09-11 (§11):** `002659D0`
      advances it over `1 … 2047` on the installer's re-key path (`003220E0`); the decoder (`003588B0`)
      compares the full word, so a handle is stable until the next re-install of the same actor and
      can collide again after 2,047 advances. ASTRA's EXP-048 executed the advance, the encoder and the
      resolver in isolation over the full period; no live lifetime is claimed.
- [x] ~~Whether any caller checks for allocation failure by other means.~~ **M-6 ANSWERED
      2026-09-12 (FABLE):** the sole caller pre-empts exhaustion by counting to 32 (clearing `+0x14`
      bit 4 instead of calling) and detects a silent failure by the actor's `+0x30` back-pointer
      staying null — but only skips the post-bind step; the record is still stamped and counted (§2).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Class is `bActor_class_flags >> 5` | `Actor_GetWorldPosition` computes exactly that and tests `== 1 \|\| == 3` | 1 |
| Movement requires class 3 | Movement gate `(flags & 0xE0) == 0x60`; `0x60 >> 5 == 3` | 1 |
| Class nibble is a separate field | `ActorRuntime_GetClassNibble` reads `actor[0x0E] & 0x0F` | 1 |
| Linear first-free allocation | complete body of `00234480` | 1 |
| Pool-full failure is silent | the scan's `return` on exhaustion writes nothing and returns void | 1 |
| BattleUnit is `0xF50` bytes | `memset(slot, 0, 0xf50)` on allocation | 1 |
| `dwFieldId` is an encoded handle | `ActorHandle_EncodeRegistryEntry(actor_work)` assigned to it | 1 |
| Slot lookup fails closed | bounds test in `00236820` returns `NULL` | 1 |
| The handle decodes through seven guards and one word compare | `003588B0` read whole (§11); EXP-034's seventeen isolated-execution cases agree | 1 |

All five functions above were read this session from a batch decompile; the GFZ names they
carried match their bodies.

## 8b. Reopened 2026-09-02 — measured reach

Cross-reference audit pass 3 counted the callers of both accessors documented here. Neither count
changes a claim above; both change how important the claims are.

**`Actor_GetWorldPosition` has 79 callers across 12 subsystems** — the most-consulted function
found in the database so far. Script VM (23), Movement (16), Presentation (5), Spawn (3), Combat
(4), Party (3), Rewards (2), **Audio (1)**, UI (1), Actor/Entity (5), plus 16 with no owner tag.

The Audio caller (`FUN_00362850`) is 3D positional audio reading actor positions — a real edge
between two subsystems that no document previously connected.

**Consequence for the class gate:** the `class == 1 || class == 3` test is not a local detail of
this function. All 79 callers inherit it, and a caller holding a class-0 actor silently gets
nothing.

**`BattleUnit_GetBySlotIndex` has 40 callers, and Movement is the largest consumer at 10 — more
than Combat AI's 5.** The BattleUnit pool is therefore **not a combat-only structure**; locomotion
and combat share one unit registry. That was not anticipated when this document was written.

Both counts are static call sites, not execution frequency. See U-4.

## 9. Related

- [`../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../06-Movement-And-Navigation/heading-speed-to-position-delta.md) — the same class field gates movement
- [`../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) — what fills this pool
- [`../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`](../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md) — what a bound BattleUnit then does
- [`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md) — the measured reach of both accessors documented here

## 9. Falsification pass 2026-09-02 — M-3 answered: the pool holds 32

**Attack chosen.** The headline asserts *"a fixed number of things that can be in a battle at
once"* while §7 admits the number itself is unknown (**M-3**). A capacity claim with no capacity is
the weakest thing here, so the pass went after the value rather than after a stated figure.

### The value: `0x20` = 32 slots

`g_nBattleUnitSlotCount` lives at **`0x0208E6A0`**, recovered by decoding the RIP-relative operand
of `BattleUnit_GetSlotCount` (`8B 05 4A 7E E5 01` -> `0208E6A0`). A reference census over that
address finds **24 references and exactly one writer**:

```
WRITE  002368FE  BattleStorage_InitializeWorkArrays   MOV dword ptr [0x0208E6A0], EAX
```

and the body gives the value outright:

```c
g_nBattleUnitSlotCount = 0x20;                                              // 32
g_pBtlWorkArray = alloc(g_nBattleUnitSlotCount * 0xf50, "BtlWork", 0);
memset(g_pBtlWorkArray, 0, (longlong)g_nBattleUnitSlotCount * 0xf50);
```

**One writer, a literal, at initialisation.** The capacity is not configurable, not data-driven and
not resized later — it is `32` from the moment battle storage is set up until the process exits.

```
slots            0x20   = 32
BattleUnit       0xF50  = 3,920 bytes
pool allocation  32 x 3,920 = 125,440 bytes (0x1EA00), tagged "BtlWork"
```

### What that means in play

**Thirty-two is the hard ceiling on everything that can be in a battle simultaneously.** The party,
any guests, and every active enemy all draw from the same 32 slots — `BattleUnit_AllocateSlotAndBindActor`
walks this one array and fails when it is full. A modder raising enemy counts is spending against
that budget, and there is no separate enemy pool to raise instead.

For **XIIOnline** this is the combatant cap: 32 `BattleUnit` slots per client, each 3,920 bytes,
with `bBattle_slot_index` as the natural per-unit key.

### The allocation names are authored

The three allocations in this initialiser carry **developer-written names**, passed as string
literals to the allocator:

| Global | Size | Authored name |
|---|---:|---|
| `g_pBtlWorkArray` | `32 * 0xF50` = 125,440 | **`"BtlWork"`** |
| `g_pBtlKeepCharWork1` | `0x9400` = 37,888 | **`"btlKeepCharWork1"`** |
| `g_pBtlKeepCharWork2` | `0x9400` = 37,888 | **`"btlKeepCharWork2"`** |

`"BtlWork"` confirms the working name this document already used for the pool. The two
`btlKeepCharWork` banks are **new here** — a *pair* of equally-sized buffers, which is the shape of
the spawn-persistence rotation described in
[`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md)
(`SpawnKeep_RotatePersistenceBanksForAreaTransition`). The same initialiser also sets
`g_nSpawnKeepReturnWindow = 300`.

### Independent confirmation of the 3,920-byte size

§2 evidences `0xF50` from the `memset` in `BattleUnit_AllocateSlotAndBindActor`. A **second,
unrelated** encoding of the same constant appears in the raw bytes of `BattleUnit_GetBySlotIndex`:

```
48 69 C0 50 0F 00 00      IMUL RAX, RAX, 0xF50
```

The accessor multiplies the slot index by `0xF50` to reach the element. Two functions, one written
as a clear and one as an index scale, agreeing on the stride — the size claim no longer rests on a
single site.

### Also visible in the initialiser

- `&DAT_02EBF1A0` is cleared as **12 quadwords (96 bytes)** — that is a slot of the authored-data
  registry documented in
  [`../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md),
  and it confirms that slot is **runtime state rather than an authored table**, consistent with that
  document's §8c finding that the upper part of the registry span is a different class of global.
- A 12-iteration loop calls `FUN_00238260(i)` for `i` in `0..11`, and the `02EBF1A0` clear is also
  12 wide. **M-7 answered 2026-09-11:** the twelve are loaded-resource pointers — `00238260(k)` requests
  loader id `0x47 + k` and a generated setter marks its completion
  ([the registry page](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md), *the tail read*);
  they mark the requests for the twelve job boards `board_1.bin` … `board_12.bin` — kind-2 path
  positions 71–82; the bytes live in the loader's resource block, not in the slot
  (FZ-7 answered 2026-09-11; [the file-size table sheet](../02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md)).

## 11. The bind, read from the binary — offsets, the back-pointer, and the handle (2026-09-10)

§2 gave the bind in C with member *names* and no offsets, and left the encoder unread. Both are
closed here. Nothing below is inferred from the C; it is what `00234480`, `002134A0`, `00263E30`
and `003589B0` execute.

### The three members §2 named

| member | offset | site |
|---|---|---|
| `dwFieldId` | **`+0x008`** | `002344FB` `mov [rbx+8], eax` |
| `pActorWork` | **`+0x010`** | `002344EF` `mov [rbx+0x10], rsi` |
| `bBattle_slot_index` | **`+0xEA9`** | `002344E0` `mov byte [rbx+0xEA9], dil` |

The slot index is **not** near the head — it is 3,753 bytes in, near the object's end. §2's field
list reads as a header and is not one; `qwUnitFlags` is the only member of the four that is.

One member §2 did not mention: `002344FE` calls `00263D30(actor)` and `00234509` stores the byte
result at **`+0x057`**. ~~Its meaning is `M-4`'s remaining half.~~ It is the actor's entry group
(§7, M-4 closed 2026-09-12).

### `002134A0` is the back-pointer, and the link is two-way

```asm
002134A0  mov qword ptr [rcx + 0x30], rdx
002134A4  ret
```

`rcx` is the **actor**, `rdx` the slot. So the bind writes **`ActorStorageRecord +0x30 = BattleUnit*`**,
and `BattleUnit +0x10 = WorldActor*` is written three instructions later. The reverse direction is
read by `00263E30` (`mov rax,[rcx+0x30]; ret`) behind the NULL guard `0031B760`, which is how
`SpawnGroup_ConfigureUnitMembershipAndMode` reaches the unit before writing `+0xE98`.

**Neither pointer owns anything.** The slot belongs to the pool and is reclaimed by index; the actor
belongs to the actor storage pool. `ActorStorageRecord +0x30` was `UNRESOLVED ... zeroed` in
`_types/` and is now `battleUnit`.

### `ActorHandle_EncodeRegistryEntry` = `003589B0`

```c
uint32_t ActorHandle_EncodeRegistryEntry(WorldActor *a)   /* 003589B0 */
{
    if (a == NULL) return 0;
    return ((((*(uint16_t*)(a + 0x16) & 0x7FF) << 4) | (*(uint8_t*)(a + 0x15) & 0xF)) << 16)
           | *(uint16_t*)(a + 0x00);
}
```

| bits | source | what it is |
|---|---|---|
| 0–15 | actor `+0x00` | **`selfIndex`** — PROVEN elsewhere as the array index the record was fetched by |
| 16–19 | actor `+0x15` & `0xF` | a 4-bit discriminator; the field was `UNRESOLVED` |
| 20–30 | actor `+0x16` & `0x7FF` | an 11-bit discriminator; the field was `UNRESOLVED` |

**So `dwFieldId` is a slot index plus 15 bits of something else** — the shape of a
slot-plus-generation handle, which is also why `+0x08` must never be treated as a pointer or as a
bare index. `ActorStorage_InitializeRecord` sets `+0x16` to `1` at `002667D3`, and ~~no incrementer
for it has been found~~ — **the incrementer is `002659D0`** (found 2026-09-11 from ASTRA's EXP-048,
read here whole, 24 bytes): `+0x16 = ((+0x16 + 1) & 0x7FF)`, and `1` when that wraps to `0`
(`002659D0`–`002659E3`) — a counter over `1 … 2047` that never holds `0`. Its one caller is
`003220E0`, the installer's re-key delegate (`00322107`): a definition change on a selected unit
(`00322050`, [the definition page](Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md))
advances the actor's discriminator and re-encodes the unit's `+0x08` handle
(`00322115`–`0032211D`), so every handle taken before the change stops resolving — until the counter
comes round again after 2,047 more advances of the same actor. That is what the field is: a
discriminator advanced on re-install, with a finite period; "generation counter" would still
overstate it, because nothing here advances it on any other lifecycle event.

### Decoding the handle back to a unit — the resolver, read 2026-09-11

`BattleUnit_ResolveByFocusHandle` (`0031B7E0`, 42 bytes) is the encoder's inverse, in four
functions:

```
0031B7E4  test byte [02089340], 0x10    ; bit 4 of the battle-state word clear -> NULL
0031B7ED  call ActorHandle_ResolveRegistryEntryByPackedId   ; 003588B0
0031B7F5  NULL actor -> NULL
0031B7FE  jmp  00263E30                 ; returns actor+0x30, the BattleUnit back-pointer (above) - itself possibly NULL
```

`003588B0` (143 bytes): handle 0 → NULL (`003588B4`); selector = bits 16–19 (`003588D0`,
`003588D9`), **5–15 → NULL** (`003588DF`); discriminator = bits 20–30 (`003588CD`, `003588D3`);
index = bits 0–15 (`003588DC`). `00263FF0` = `02098E10 + selector × 0x288`, the manager. Then, each
failing to NULL in this order: manager `+8` (the vector) non-null (`003588EB`), manager `+0`
(storage) non-null (`003588F4`), index < signed `+0x20` (`003588FA`), manager byte `+0x10` bit 0
(`003588FF`), index < the vector's signed count at `+0` (`00358905`), entry `vector + 8 + index × 8`
non-null (`00358909`), and **the actor's full u16 `+0x16` equal to the discriminator**
(`00358913`–`00358925`, `cmovne` to NULL). The word is compared unmasked, so an actor whose `+0x16`
exceeds `0x7FF` can never resolve, and bit 31 of the handle is never read. No active-unit or class
test anywhere in the chain: the caller qualifies the unit it gets back.

Static reading is this section's tier. ASTRA's [EXP-034](../_experiments/EXP-034-focus-resolver.md)
executed the four original bodies in isolation over synthetic managers, vectors and actors —
seventeen cases (selectors 2 and 4, the gate off, handle 0, selector 5, null vector and storage, a
disabled manager, capacity and count edges, a null entry, wrong and full-word discriminators, the
bit-31 alias, a null back-pointer) — and every case returned what the reading above predicts. That
is isolated execution of original code, **not** a live binding: nothing here says which unit the
game resolves for a real `+0x710`. The two fields stay discriminators; the reader compares them —
the one incrementer is `002659D0`, above (`M-5`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT.** `BattleStats_GetOwningActorHandle`, owned by that layer, calls `00236820` on this page. That caller is the 91-byte handle form of the owning-unit search: it walks every battle unit for the one whose `[unit + 0x698]` equals the pointer it is given and returns that unit's `dword[+8]` rather than the unit; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Items_Equipment_Shops_License — CLIENT.** `BattleStats_ClearAllEquipmentSlotsByMask`, owned by that layer, calls `00236820` on this page. That caller is the masked equipment-slot clear, in a `0x40`-byte frame with a stack cookie; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT (SWE2-CONTRACT 2026-09-15, 14 edges).** The slot-pool accessors are consulted by the combat
semantic helpers: `Gameplay.CombatAction.TargetFocusGeometryRuntime` `0031ADB0` shares
`00263E30`/`00265020`/`0031B7E0`/`003589B0` (4 edges); `BattleAction_FindApproachGeometryAroundTarget`,
`BattleUnit_HasRelationshipClass2PlusInSlotMask`, `Battle_EmitReactionPresentationForSlot`,
`ActorHandle_GetPrimaryFormulaResourceByte26`, `WorldActor_HasActiveBattleActionOrUnitFlag14`,
`BattleUnit_HasRelationshipClass2PlusInTrackedActorList`, `WorldActor_QueryCombatStanceState`,
`BattleUnit_HasCurrentFocusEngagementEvidence` and the facing-operand evaluator `00312B40` each
reach `00236820`/`00263E30`/`00265020`/`0031B760`/`0031B7E0`. The pool is where those helpers
resolve battle units — the layer consults the pool, not shared ownership.

**CombatFormula — MECHANICAL (SWE2-CONTRACT 2026-09-15, 7 edges).** `BattleStats_GetOwningActorHandle`,
`BattleStats_FindOwningBattleUnit` and `00384F40` share `00236820`/`00236850`/`00265020`;
`BattleStats_ResolveByActorHandle` shares `00263E30`. Shared resolver fan-in.

**Status_Periodic_Terminal — SERVICE and CLIENT (SWE2-CONTRACT 2026-09-15, 3 edges).** The release/reuse
path hands units to the status layer's reset helpers: `ActorSystem_ReleaseBattleUnitSlotForActor`
`00234200` calls `BattleUnit_ResetActionControlForStatusTransition` `00300140`, and
`BattleUnit_ResetStateForReuse` `00236A60` calls
`BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450`. In the other direction
`00263E30` is consulted by `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860`. The
crossing is the reset hand-off, not shared ownership.

**RNG_Random_Selection — SERVICE (SWE2-CONTRACT 2026-09-15, 1 edge).** The facing-operand evaluator
`00312B40` (already cited above for its Gameplay callers) draws from
`RNG_SharedGameplayLCG_NextU32` `00328370`. The page owns the evaluator's operands, not the stream.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Audio — CLIENT (9 edges).** `00362850`, the 3D positional audio body §8b names, calls `Actor_GetWorldPosition` (`00265020`); it is itself called by `00363560` and by the tick (below), and it calls seven audio helpers - `002DF410`, `002DF560`, `00362C60`, `00362D20`, `00362E50`, `003631B0` and `00363F30`. Positional audio reads actor positions through this page's class-gated accessor, so a class-0 or class-2 actor has no position to place a sound at; the audio work around it is the audio pages'.

**CombatAI — CLIENT (33 edges).** The AI resolves units through the pool accessors: `BattleUnit_GetBySlotIndex` (`00236820`) is called by `AiOrder_EvaluateTargetSelector` (`00301AD0`), `AiOrder_ComputeBoundedSelectorScalar` (`00308C20`), `BattleEnmity_PropagateToPerceivingFoes` (`003219D0`), `BattleUnit_RebuildPerceptionCandidateCache` (`003247F0`) and `BattlePerception_RefreshCandidateCacheGeneration` (`00324F20`), `BattleUnit_GetSlotCount` (`00236850`) by three of them, `BattleUnit_FindByDefinitionSelector` (`002367A0`), `BattleUnit_ResolveByFocusHandle` (`0031B7E0`) and `Vector3_ComputeXZHeadingOrFallback` (`0031AC90`) by the selector, `0031B760` by five `AiOrder_*`/`BattleUnit_*` bodies and `00263E30` by the two perception bodies; the shared stream `RNG_SharedGameplayLCG_NextU32` (`00328370`) is drawn by `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`), `AiOrder_CheckActionPreconditions` (`00301830`) and `AiOrder_SelectFinalTargetFromCandidates` (`003087E0`); the selector `00301AD0` calls seven `BattleTarget_*`/`BattleEnmity_*`/`AiTargetSelector_*` helpers such as `BattleTarget_ComputeSurfaceDistanceBetweenUnits` (`0031E6F0`) and is called by `003014C0`; `003247F0` calls `00324F20` and `BattlePerception_TestCachedSpatialVisibilityPair` (`0032A4D0`); and the area-descriptor handler `00236C30` calls `GambitTargetDefinition_BindAndBuildMenuLookup` (`00238880`), which calls the tagged allocator `00384510`. The AI iterates the 32-slot pool and resolves units by slot, handle and definition through these accessors, and the gambit target table is bound while the area's battle data is loaded; target choice is the AI pages' matter.

**Core and CoreRuntimeScheduling — CLIENT (2 edges).** `002341C0` (filed to Core) calls `Navigation_ClearDataset` (`00383A20`), and `0022A0B0` calls `BattleStorage_InitializeWorkArrays` (`002368D0`). The scheduling layer's `0022A0B0` runs the storage rebuild of §12 that allocates the 32 `BtlWork` records, and the navigation clear it performs is called from one more body; both are lifecycle calls, not pool semantics.

**Input — CLIENT (2 edges).** `00226BE0` (the system-stop start) and `002E09A0` call the slot-block getter `00263FF0`. Both input-filed bodies fetch an actor-manager slot block through the same one-line getter; neither touches the battle-unit pool.

**Movement — CLIENT, SERVICE (80 edges).** Locomotion is the pool's largest consumer (§8b): `BattleUnit_GetBySlotIndex` (`00236820`) is called by ten movement bodies such as `BattleLocomotion_BuildSolverContext` (`00336710`), `BattleLocomotion_QueryDynamicActorObstruction` (`003357B0`) and `PartyFollow_SolveFormation` (`00338490`), `BattleUnit_GetSlotCount` by four, `Actor_GetWorldPosition` (`00265020`) by sixteen such as `Movement_UpdateSteeringTowardTarget` (`002E45E0`) and `BattleUnit_PublishLocomotionPosition` (`00300310`), `00263E30` by ten, `BattleUnit_ResolveByFocusHandle` (`0031B7E0`) by four, `ActorRuntime_GetClassNibble` (`00263C20`) by two, `ActorHandle_EncodeRegistryEntry` (`003589B0`) by `Movement_IntegratePositionAndMeasureDisplacement` (`002E5610`) and `002EBFA0`, and `BattleUnit_FindByDefinitionSelector`, `0031B760`, `00263FF0` and the shared stream `00328370` by one or two each; `00336710` is called by five solver bodies such as `BattleLocomotion_SolveAndPublishNextStep` (`00336CE0`) and calls `Navigation_CheckDirectRouteAcrossRegionsXZ` (`0033D3E0`) and three more; `003278D0` (which walks every slot calling `003839C0` and `Navigation_ResetPathPredecessors`, `003839F0`) is called by five `0026E...` bodies; `BattleLocomotion_ResetPathAndSetTargets` (`003291B0`) and `BattleUnit_ResetStateForReuse` (`00236A60`) call the same path resets; `002368D0` calls `Navigation_ClearDataset`; and `003247F0` calls `003919B0` and `00391D10`. Locomotion and combat share one unit registry, the class gate decides which actors have a position to steer, and the pool's reset and rebuild paths clear per-unit path state; movement's algorithms are the movement pages'.

**Party — CLIENT, SERVICE (26 edges).** Party bodies resolve units through the pool - `BattleUnit_FindByDefinitionSelector` (`002367A0`) from `PartyFocus_SelectAndRequestDefaultActor` (`00326500`) and `PartyConfiguration_ReconcileRuntimeRosterFirstThreeFromRequestedSelectors` (`00328DB0`), `BattleUnit_GetBySlotIndex`, `BattleUnit_GetSlotCount` and `00263E30` from the `PartyConfiguration_*` roster reconcilers, `00263E30` also from `BattleUnit_ResolveByFocusHandle` (`0031B7E0`) and `BattleUnit_GetPartyLeader` (`003272A0`), `Actor_GetWorldPosition` from `00303CC0`, `00304180` and `PartyFocus_TryGetCurrentActorWorldPosition` (`00359150`), `ActorHandle_EncodeRegistryEntry` from five roster and focus setters such as `PartyRoster_AssignActorToSlot` (`00269C70`), `0031B760` from `0030BEB0`, and the shared stream from `BattleUnit_SeedPartyCombatStanceRecheckTimer`; in the other direction the selector `00301AD0` and `00336710` call `0031B7E0`, `003272A0` and `PartyFocus_IsCurrentPackedActorHandle` (`003273B0`), the re-key delegate `003220E0` calls `00326500`, and `00362850` calls `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`). The roster and focus are stored as encoded registry handles made by this page's encoder and are turned back into units through its resolvers; the party layer owns which actors those are.

**Presentation — CLIENT (20 edges).** `001E8580` calls `002134A0`, the 5-byte store the allocator uses to plant the unit pointer at actor `+0x30`; `CharacterRenderSystem_Initialize` (`004269A0`) calls the verb-registration helper `0041D6C0`; the effect-element fronts `003A4290` and `003A56F0`, with `00465120`, `00465690` and `003DD4C0`, call `00263FF0`, and four of them plus `00506700` call `ActorHandle_EncodeRegistryEntry`; `Actor_GetWorldPosition` is called by seven render bodies such as `BattleUnit_TestActorViewFrustumAtCurrentPosition` (`00322360`), `003C29A0` and `003C37B0`; and the selector `00301AD0` calls `00322360`. Rendering and effects read positions, slot blocks and handles through the same accessors, and one render body calls the same `+0x30` store the bind uses; the render work is not this page's.

**Resource — SERVICE (8 edges).** `002368D0` and the area-descriptor handler `00236C30` call `003843F0` (section registration), which calls `00384420`; `00238260` (per-channel init) calls `00384420`, which is also called by `002385D0` and itself calls `0032E400` and `0032E620`. The storage rebuild registers the authored-data section `0x13` and the twelve channels through the resource layer's tagged register family (§12); the pool uses it only to bind its data.

**Rewards_Progression_Economy — CLIENT (2 edges).** `Loot_FindOverlappingPickupIndex` (`002FB150`) and `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) call `Actor_GetWorldPosition` (`00265020`). Loot placement and pickup overlap read an actor's position through the class gate; which actors drop what is the rewards pages'.

**Script_VM_Native_Bridge — CLIENT, SERVICE (62 edges).** Script verbs call the accessors - `Actor_GetWorldPosition` from 23 (such as `0033FD60`, `00344AF0` and `003478A0`), `00263FF0` from 20 (such as `0033F7F0` and `0034AF50`), `ActorHandle_EncodeRegistryEntry` from twelve (such as `00342150` and `00357620`) and `0031B760` from `005102D0`; the `setentrygroup` body `0034FA70` calls `0025AD10` and the `setentrygroupall` body `00340970` calls `0025AE00`, and `003574B0` calls `00340970`; and `00340970`, `0034FA70` and the `setline` verb `00351610` call the VM's value-stack pops `VMValueStack_PopInt32CoerceFloat32` (`00267E10`) and `VMValueStack_PopNumericDiscard` (`00267DB0`). Scripts position actors, set entry groups (copied to unit `+0x57` at bind) and address actors by encoded handle through this page's functions, and the verb bodies read their arguments off the VM stack; what each verb means is the script pages'.

**Spawn_Encounter_Lifecycle — CLIENT (38 edges).** `0031B760` is called by 24 spawn bodies such as `SpawnLifecycle_CheckAndRetireByNativeRange` (`002350C0`), `Spawn_SelectContinuousEntry` (`00235360`) and the `SpawnEntry_Get*` family (`00235EF0`, `00236030`, `002366E0`); the shared stream `00328370` by five such as `Spawn_TrySelectCandidatePosition` (`00234AF0`) and `SpawnPoint_GeneratePositionFromAuthoredRegion` (`00236450`); `Actor_GetWorldPosition` by `00234AF0`, `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`) and `002350C0`; `Spawn_CountActiveCapTrackedActors` (`00308D90`) walks the pool with `00236820` and `00236850`; `SpawnGroup_UpdateExpectedMemberLaneMask` (`00306E60`) and `SpawnGroup_RecordMemberDeathAndHandleCompletion` (`00306F00`) call the entry-group getter `00263D30`, and `00306F00` also calls `00238B70`, one of the six bodies that read the pool base; and `00234AF0` calls `0031AC90`. Spawning counts live units against caps, checks distances from actor positions and records member deaths by entry group, all through this page's accessors; spawn policy is the spawn pages'.

**UI — CLIENT (14 edges).** `BattleMenu_BuildCommandEntryList` (`0031EB20`) and `00322A80` walk the pool with `00236820` and `00236850`, and `0031EB20` also calls `00263E30` and `0031B7E0`; `ActorRuntime_GetClassNibble` (`00263C20`) is called by seven UI bodies such as `BattleMenu_RecordSelectedTargetAndCursorContext` (`0027D330`), `002C7660` and `003C8B70`; and `003C5130` calls `Actor_GetWorldPosition`. The battle menu builds its command and target lists from the pool and tells actors apart by the `+0x0E` class nibble; the menus are the UI pages'.

**World — SERVICE (1 edge).** The area-descriptor handler `00236C30` calls `003847B0` (15 B, filed to the world domain). It is one call among the handler's section binds, made while the area's battle data is loaded.

**WorldAreaField — SERVICE, CLIENT (12 edges).** The area-descriptor handler `00236C30` calls `AreaData_BindAndRebaseSectionDescriptor` (`003845F0`), `003846F0`, `003843F0` and `00384500`, and is called by `00238850` (the handler block §12 re-registers), which also calls `003846F0`; `ActorSystem_ReleaseBattleUnitSlotForActor` (`00234200`) and `003247F0` call the field-bit thunk `FieldData_GetActiveFieldRecordBit15` (`00313F60`); the selector `00301AD0` calls `FieldData_GetFormat0RecordVectorByIndex` (`00320940`) and `FieldData_GetActiveFieldRecordBit15` (`00377C20`); and the tick `World_UpdateSimulationTick` (`00314020`) calls `00362850`. The pool's authored-data section is bound through the field layer's area-data section binder, and the unit release path consults the per-area action-permission bit; the field record and area data are that layer's.

## 12. The `002368D0` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`BattleStorage_InitializeWorkArrays` (`002368D0`, 353 B) is the storage rebuild that
runs before battle work can be handed out — the point where every work array the
pool pages describe is freed, reallocated and zeroed. Read end-to-end from the
shipping image:

- Stores `float[008A4700]` into `02F973B8`, zeroes `02089300`, writes `0x20` to the
  count cell `0208E6A0`, then frees the old `[0208E688]` via `003844F0` and
  reallocs `0x20 × 0xF50 = 0x1EA00` bytes through the tagged allocator
  `00384510` — the `BtlWork` array (32 records × `0xF50`).
- Two further `00384510` allocs of `0x9400` each land at `0208E690` and `0208E698`
  and are zeroed by `00861EC0` — the two keep-work banks the spawn page's §2 sizes
  describe. The tag args passed are `009146B0` / `009146B8` / `009146D0`, and read
  out of the shipping image those three addresses hold `BtlWork`,
  `btlKeepCharWork1` and `btlKeepCharWork2`. The tags are the strings, and this
  code passes them — which is what the allocation table in the pool section above
  already assumed.

  > **CORRECTED 2026-09-18 (OPUS).** This bullet used to say the opposite twice
  > over: that the three pointers land on empty `.rdata`, and that the literal
  > `btlKeepCharWork` strings sit somewhere else, at a pair of addresses it then
  > named. Both halves fail against the bytes, and the arithmetic says how. Each of
  > the two addresses it named is the canonical one less `0x00120000` — the image
  > base that this project's addresses already include — so the pair is a second
  > subtraction of the base. Neither lands in `.rdata`: both are inside `.text`,
  > and the second of them begins a function prologue, `40 53 48 83 EC 20`. The
  > conclusion the bullet drew from the pair, that the tag gloss was a string-xref
  > association rather than the pointer this code passes, falls with it.
- `00383A20()` runs, then `[0208E680]` — the authored-data descriptor cell
  `00236C30` mode-0 frees — is released through `00384500` and nulled, and section
  `0x13` is re-registered through `003843F0` with handler block `00238850`.
- Members `0030CF40` and `002EA5F0` run back-to-back, then the tail clears the
  12-qword channel table at `02EFF1A0` (`rep stosq`, 0xC qwords), stores
  `float[008A46E4]` to `0208935C`, zeroes `02089340`, writes `0xFFFF` to
  `0208D455` and `0x12C` to `0208936C`, and loops `00238260` over channels 0–0xB.

| member | role | interior |
| --- | --- | --- |
| `0030CF40` (99 B) | `BattleAction_ResetPresentationSlotPool` — clears list heads `022BEB88`/`022BE978` and resets the 32-record `0x30`-stride pool at `022C17B0`: mask `+0x2C &= ~0x1F`, links nulled, `+0x28 = 0x80000000`, `+0x24 = -1`, word `+0x1C = 0xFFFF` | [`0030CF6E`](../_index/ADDRESS-INDEX.md) |
| `002EA5F0` (93 B) | script-verb registration battery — five `0041D6C0` calls: id 5 → `0016D6A0`, id 4 → `002E70C0`, id 6 → `002E7090`, id `0xC` → `002E70A0`, id `0x26` → `002E7080` | [`002EA5FB`](../_index/ADDRESS-INDEX.md) |
| `00238260` (296 B) | per-channel init, called for `cl` = 0–0xB — builds a 12-pointer case table on the stack, checks `02EBF1A0[cl]`, probes capacity through `00233E00`, and on success calls `00384420` with `ecx = cl + 0x47`, `r9 = 3`, stack args 4/8 | [`00238329`](../_index/ADDRESS-INDEX.md) |
| `00233E00` (156 B) | channel-capacity probe — `cl > 0xB` → 0; `02EFF1A0[cl]` already set → 1; else counts non-null qwords across the 12 slots and returns `count < 6` — a channel is usable when claimed or fewer than half the slots are in use | [`00233E40`](../_index/ADDRESS-INDEX.md) |

Shared callees — all deliberately outside the census: `003844F0`/`00384500`/
`00384510`/`00384420`/`003843F0` (tagged alloc/free/register family), `00861EC0`
(memset), `0041D6C0` (verb registration), `00383A20`, `00808C40` (stack-cookie
check). The `00238260` stack table's twelve `rip+`-relative targets past the
function end (`00238390`–`002383E9`) are left as a recorded unknown. The tag
arguments are no longer one of them: they are read above, out of the image.

## The 1016-byte gap at `+0x298` is the tail of the acquire-side reset block (2026-09-18, OPUS)

`unobservedSpan0298` is 1016 bytes — **75 % of this type's 1,357 unknown bytes in one span**. Two
measurements bound it without explaining it, and the distinction matters:

**It ends exactly where the reset block ends.** `1016 = 0x3F8`, and `0x298 + 0x3F8 = 0x690`.
`BattleUnit_ResetStateForReuse` sets `rcx = unit+0x80`, `edx = 0`, `r8d = 0x610` at
`00236B12`/`00236B1F`/`00236B28` and fills through `00236BF0`, so it clears `+0x80 .. +0x690` —
and this gap is the last `0x3F8` bytes of exactly that block, stopping on the same byte, eight
short of the stats-record pointer at `+0x698`. The gap is not an arbitrary hole between fields; it
is the unnamed tail of a region the acquire path already treats as one unit. That is **extent, not
meaning**, and the span stays `DISCOVERED` / `UNKNOWN`.

**Nothing that can reach the pool reaches it.** A pool closure over this type — seeded from the
callers of every accessor, tainting the accessor's **return value**, then following each handoff
that passes the unit itself in `rcx` — reports the span untouched, by direct access and by handoff
alike. So do `+0x120` (32 B) and the `+0xEB4` tail (156 B).

Three routes were closed in turn, and the second one is why the first result should not have been
believed on its own:

| route | how it was closed | result |
|---|---|---|
| the two obvious accessors | `00236820` + `00234480`, 41 seed callers, **57** proved bodies | span untouched |
| **a third accessor the first pass missed** | every body that reads the pool base `0208E688` is exactly **six** — `00234200`, `00234480`, `002367A0`, `00236820`, `002368D0`, `00238B70` — and `002367A0 BattleUnit_FindByDefinitionSelector` is an accessor that was not seeded. Adding it: 50 seed callers, **67** proved bodies, one new handoff (`+0x0E0` → `0031AC90`) | span **still** untouched |
| an interior pointer escaping to memory | a store of any tainted `unit+d` value into memory, over all 67 bodies. **The only displacement that ever escapes is `+0x000`** — the unit pointer itself, at `00302D2A`, `00324957`, `00324DB5`, `00336869` | no interior pointer into this object is ever stored anywhere |

Enumerating the pool-base readers is what makes the set closed rather than merely large: a closure
seeded from accessors I happened to know is worth much less than one seeded from all six bodies
that can obtain the array at all.

The closure's control is one this page established independently and by other means: the only
non-zero handoff in the object, apart from `+0x0E0`, is **`+0x200` to both `003839F0`
(`Navigation_ResetPathPredecessors`) and `003839C0`** — the 128-byte predecessor table and the two
`0xFFFF` path endpoints described in the reset section above. A scan that rediscovers that pair
from the instructions alone is working; a silence from it is a measurement rather than an absence
of effort.

The closure's control is one this page established independently and by other means: the only
non-zero handoff it finds anywhere in the object is **`+0x200` to both `003839F0`
(`Navigation_ResetPathPredecessors`) and `003839C0`** — the 128-byte predecessor table and the two
`0xFFFF` path endpoints described in the reset section above. A scan that rediscovers that pair
from the instructions alone is working; a silence from it is a measurement rather than an absence
of effort.

Four bodies that were the obvious candidates were checked individually and touch nothing in the
span either: `003278D0`, `003291B0` (`BattleLocomotion_ResetPathAndSetTargets`), `00236A60` and
`0030EFF0` (`BattleUnit_SnapshotAndSuspendActionState`).

### The four escape sites, followed — and all four are dead ends

The one route left open above was the escaping pointer: the closure follows registers, so a unit
pointer written into some other structure leaves it. All four stores were traced to what receives
the pointer and to who reads it back.

| site | in | destination | who reads it back |
|---|---|---|---|
| `00302D2A` | `AiOrder_EvaluateTargetSelector` (`00301AD0`) | the global `022C17A8` | **exactly one body references that global — the one that wrote it**, and it is already inside the closure as an accessor caller |
| `00324957` | `BattleUnit_RebuildPerceptionCandidateCache` (`003247F0`) | `[rsp+0x70]`, a **stack** array of pointers (`mov [r13],r14; add r13,8`) | nobody — the buffer is **never passed to any call** in that body |
| `00324DB5` | the same function | the same `[rsp+0x70]` array, through a second cursor | as above |
| `00336869` | `BattleLocomotion_BuildSolverContext` (`00336710`) | `ctx+0xF0`, after `BattleUnit_GetBySlotIndex` on the slot byte at `[ctx+0x108]+0x177` | the solver family — **28 bodies**, the five callers of `00336710` plus `BattleLocomotion_SolveAndPublish` and their callees. Tainting the unit back out of `ctx+0xF0`, they reach it at **`+0x698`, `+0x714`, `+0x768`, `+0x76C`, `+0xE68` and nowhere else** — all outside the span, all already documented |

**And there is no dispatch escape hatch.** Every handoff target in the 67-body closure is a
**direct** call; not one passes the unit through an indirect or virtual call, so "the closure
follows direct calls" costs nothing here. That was measured, not assumed — it is the obvious way
this argument could have been quietly incomplete.

### What that adds up to

Six independent routes, each closed by its own measurement:

1. the two obvious accessors — 57 bodies;
2. the third accessor, found by enumerating **all six** readers of the pool base `0208E688` — 67 bodies;
3. escaping interior pointers — the only displacement ever stored is `+0x000`;
4. each of those four stores, followed to its consumer — above;
5. indirect dispatch — none exists;
6. **the accessor bodies themselves**, which the closure had never scanned — they are members now,
   which is why the counts above are 57 and 67 rather than 55 and 64.

Route 6 was a real hole and it was found by reading a warning about a different question.
`check_absence_claims.py` flags `UQ-339`, an **earlier OPUS claim of exactly this shape** —
*"authoring-tool state nothing reads"* — which was contradicted because the name it looked for was
composed at run time (`"PresetDof "` + index) and so had no literal to find. The specific failure
does not apply to an offset claim, but the general one does: **a "nothing reads it" result is
worth only as much as the instrument's ability to see the reading mechanism.** Asking what the
analogous blind spot was here produced one immediately — the closure seeds from an accessor's
*callers*, so the accessor **bodies** were never members, and
`BattleUnit_AllocateSlotAndBindActor` is precisely where a back-pointer into the actor record
would be written. Scanned directly, all six pool-base readers store nothing and touch no offset in
the span; **the binder writes no back-pointer**, which closes the `actorWork` route as well.

`member_reach_scan.py` adds the accessor bodies to the member set now, so the hole cannot recur
silently, and its self-test asserts they are present. The hole was real and closing it
**strengthened** the result rather than changing it — which is the outcome one should hope for
from this kind of check, and not the one to assume.

**`+0x298` is written by the acquire-side clear and read by nothing in the shipped image that
static analysis can reach.** For reconstruction that is a usable, bounded fact: the 1016 bytes
must be *allocated and zeroed*, because the slot stride and the `0x610` fill both depend on them,
and **no observable behaviour reads them back**.

**The limit, stated rather than left implicit.** This is a statement about statically traceable
routes, not about the running game. It does not exclude a reader that computes the address from
data — a script, a table of offsets, or anything that reaches the slot by arithmetic rather than
through the accessors — and no runtime evidence has been taken. The honest reading is *"unread by
every route this project can measure, and the measurement is now exhaustive over those routes"*,
which is a different and much stronger claim than the `no censused access` the store started with,
and still not `dead`. Runtime confirmation is an ASTRA question if anyone wants the stronger one.
## SWE2-EC7-31 update (2026-09-18) — `00263D30` entry-group word getter, verified

`00263D30` (8 B) is exactly the two instructions this page already
quotes: `movzx eax, word ptr [rcx+0xF6]; ret` — the actor's
entry-group word, copied to unit `+0x57` at bind by `002344FE`/
`00234509`. No guards, no sign extension beyond `movzx`. Interior
anchor `00263D37` (the `ret` — the body is exactly the two
instructions).

## The `+0x298` result extends to all thirty-one unknown spans (2026-09-19, OPUS)

The pool closure was built to answer one question about `+0x298`. Run against **every** `UNKNOWN`
span this type declares — 31 of them, 1,357 bytes, 34.6 % of the record — the answer is the same
for all of them: **not one offset falls in any of them.**

The same run says something about the instrument, which is why the negative is worth more than a
silence. Across the 63 proved member bodies the closure finds **19 distinct offsets, and all 19
lie inside already-named fields** — none in an unknown span, none outside every row. It never
contradicts the layout and never adds to it.

**That is a narrow view, and saying so is the point.** Nineteen offsets is a small fraction of a
178-row type, because this closure follows registers from three accessors while the existing rows
came from a **1,777-row access census** built by other means. So the corroboration is a check on
the instrument — two independently built views agreeing wherever they overlap — and the zero is
what the instrument adds: the 1,357 unknown bytes are not merely uncensused, they are unreached by
everything the accessors can hand the object to.

Bounded exactly as the `+0x298` finding is: four static routes, no runtime evidence, and a reader
that computes an address in a form the taint does not model would look identical.

## The slot is scrubbed on RELEASE too, not only on allocation (2026-09-19, OPUS)

*§2 evidences `0xF50` from the `memset` in `BattleUnit_AllocateSlotAndBindActor`. There is a second
full-slot clear on the other side of the lifetime, and no page records it.*

`ActorSystem_ReleaseBattleUnitSlotForActor` (`00234200`) ends by zeroing the entire slot:

```
002342A1  mov     rdx, [rip+0x1E5A3E0]     ; the pool base
002342AD  movsxd  rax, dword [rip+0x1E5A3EC]
002342B4  imul    rcx, rax, 0xEA7900       ; the pool extent
002342BE  cmp     rbx, rcx                 ; bounds-check the slot against the pool
002342C3  xor     edx, edx
002342C5  mov     r8d, 0xf50
002342CB  mov     rcx, rbx
002342CE  call    00861EC0                 ; memset(slot, 0, 0xF50)
```

**The clear is guarded by a pool bounds check** — the slot must lie between the base and
`base + count × 0xEA7900` — so a pointer that is not a pool slot is not scrubbed. That is the
release-side counterpart of the allocation-side `memset` at `002344D2`, and the two together mean a
slot is zero at both ends of its life.

**The ordering matters and this page already documents the other half of it.** The release copies the
unit's world position `+0xE0` and yaw `+0x160` out to the spawn record *before* this point, so the
scrub is the last act: **nothing in a released slot survives into the next occupant.** A
reimplementation that recycled slots without the clear would leak a previous unit's state into a new
one through every field the binder does not explicitly set — and **the unknown spans are exactly
the fields nobody has shown the binder sets**, `unobservedSpan0298`'s 1,016 bytes among them.

**NOT CLAIMED:** that these are the only whole-slot clears. `memset(g_pBtlWorkArray, 0, count × 0xF50)`
in §above clears the array wholesale, which is a third; this note adds the per-slot release path,
not a census of all of them.

*Found by `check_ctor_clears.py`'s size-matching pass — a declared type size equal to a literal
`memset` length — which is a **candidate generator**, not a finding: the destination has to be read.
Here it was, and `rbx` is bounds-checked against the pool two instructions earlier.*

## SWE2-EC7-61 update (2026-09-19) - `0034FA70`

`0034FA70` (151 B) is the `setentrygroup` body the slot-pool page names - `0025AD10`/`002640C0`/`00267E10`. Interior anchor `0034FA85` (a `002640C0` call).


`00263D40` (135 B) is the variable-length chain read: `rbx = [rcx]` must carry `word[+0] > 3`, then `[rdx+0x40]`'s `dword[+0x18]` resolves through `0020E600` into the word-run buffer at `base + rbx`; the body walks `esi + 1` links (each link's `word[0] + 1` is its own stride) and returns `word[rcx + rdi*2 + 2]` when `rdi < word[rcx]`, else -1 - the nested-record element getter the slot-pool and actor-record callers share.

Interior anchor `00263D90` (function `00263D40`).
