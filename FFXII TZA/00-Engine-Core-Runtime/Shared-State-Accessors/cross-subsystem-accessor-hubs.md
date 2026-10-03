---
system: Cross-subsystem accessor hubs
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: multiple — this document exists to describe the seams between owners
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `003BED70`, `00402F00`, `004044D0`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 2
  last_pass: 2026-09-02
  last_pass_state: falsification-superlative-overturned-tables-exact
  crossref_clean: true
  reopened_count: 0
origin: cross-reference audit pass 3 — these hubs were found by dispositioning UNACCOUNTED NEIGHBOUR findings, not by reading a category
---

# Cross-subsystem accessor hubs

> Three functions totalling **125 bytes** are consulted by **168 callers across 14 subsystems**.
> They are the seams where FFXII's otherwise well-separated systems actually touch each other,
> and none of them was found by reading a category — they were found by auditing.

## 1. What the player sees

Nothing names these. But they are why the game feels like one world instead of several.

The music knows where your characters are standing. The spawn system knows you changed zones and
keeps the monsters you just walked away from. Your party's licence points know whether the fight
you just won counted. A treasure chest knows not to open while you are in a cutscene.

All of that coordination runs through a handful of tiny shared accessors. When a mod changes one
of them, it does not change one system — it changes every system that asks.

## 2. Native mechanism

### Hub 1 — `Actor_GetWorldPosition` (61 bytes, 79 callers)

> **Corrected 2026-09-02 (§9).** This read *"the most-consulted function found in the database so
> far"*. **That is false.** Among addresses this database cites, `ResourceTable_ResolveEntryByIndex`
> (`002ED570`, owner **Resource**) has **87** callers, and documented middleware goes far higher —
> `checkPhyreObject` 750, `lua_type` 461. The true superlative is about *reach*, not volume, and
> even there this function ranks **6th of 478**. See §9.

Documented in detail under Actor/Entity; what matters here is its reach across subsystems, which is
the property this document is actually about.

| Caller subsystem | Callers |
|---|---:|
| Script VM / Native Bridge | 23 |
| Movement | 16 |
| *(no owner tag)* | 16 |
| Actor/Entity | 5 |
| Presentation | 5 |
| Spawn/Encounter/Lifecycle | 3 |
| Combat Action | 3 |
| Party | 3 |
| Rewards/Progression | 2 |
| Audio | 1 |
| Combat Formula | 1 |
| UI | 1 |
| **Total** | **79** |

**Audio calls it.** `FUN_00362850` (1,036 bytes, Audio-tagged) reads actor world position — which
is 3D positional audio doing exactly what you would expect, and is a real edge between two
subsystems that no document previously connected.

Recall the gate from Actor/Entity: position is readable only for actor class 1 or 3. **Every one
of these 79 callers is subject to that class check** — a caller holding a class-0 actor gets
nothing back.

### Hub 2 — `WorldTransition_GetActiveOrPendingFieldId` (27 bytes, 49 callers)

```c
int WorldTransition_GetActiveOrPendingFieldId(void)
{
    base = SaveImage_GetPersistentPayloadBase();
    id   = *(int *)(base + 0x1044);
    if (id < 0) id = 0;              // negative clamps to zero
    return id;
}
```

**The current area ID lives inside the save image's persistent payload, at offset `0x1044`.**

That is the structurally interesting part. "Which area am I in" is not a separate runtime global —
it is a field of the same data that gets written to a save file. This is why loading a save puts
you back in the right place without a separate area-restore step: the area *is* save state.

The name says "active or pending", and the clamp is consistent with that: a negative value
(meaning "no pending transition", most likely) reads as area 0 rather than as an error.

| Caller subsystem | Callers |
|---|---:|
| *(no owner tag)* | 21 |
| World/Area/Field | 10 |
| UI | 5 |
| Movement | 3 |
| Actor/Entity | 2 |
| Combat Action | 2 |
| Script VM / Native Bridge | 2 |
| Spawn/Encounter/Lifecycle | 1 |
| Audio | 1 |
| Platform/Online/Achievements | 1 |
| Save/Load/Settings | 1 |
| **Total** | **49** |

Notable individual edges, each verified in the call graph:

- `SpawnKeep_RotatePersistenceBanksForAreaTransition` (`00233780`) — the spawn persistence banks
  rotate against this value. It is the concrete link between "you changed zone" and "your
  monsters were kept".
- `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (`002F8060`) — combat consults the current
  area before triggering authored field actions.
- Platform/Achievements (`003160C0`) — achievement logic is area-aware.

### Hub 3 — `BattleUnit_GetBySlotIndex` (37 bytes, 40 callers)

| Caller subsystem | Callers |
|---|---:|
| **Movement** | **10** |
| *(no owner tag)* | 12 |
| Combat AI | 5 |
| Combat Action | 4 |
| Actor/Entity | 2 |
| Combat Formula | 2 |
| Party | 2 |
| Spawn/Encounter/Lifecycle | 1 |
| Items/Equipment/License | 1 |
| UI | 1 |
| **Total** | **40** |

**Movement is the single largest consumer of the combat slot pool — more than Combat AI.**

That was not expected, and it is the kind of relationship this database exists to surface: the
BattleUnit pool is not a combat-only structure. Movement code walks it routinely, which means
locomotion and combat share a unit registry rather than each keeping their own.

Ten Movement callers against five Combat AI callers is a strong enough asymmetry to state, but it
counts *call sites*, not execution frequency — see §7.

### Hub 4 — the identity resolvers: every way the engine reaches a battle unit (2026-09-13, FABLE)

Hub 3 is one door into the unit pool. **There are nine**, each taking a different kind of identity, and
between them they are some of the most-called code in combat: `BattleStats_FindOwningBattleUnit` alone has
62 direct callers. Read side by side from their bodies, they describe how the battle model is wired —
and three of their names describe something narrower than what they do.

| resolver | input | how it gets there | returns NULL when |
|---|---|---|---|
| `BattleUnit_GetBySlotIndex` `00236820` (40 callers) | pool slot | bounds `0 ≤ slot ≤ [0208E6A0] − 1` (`00236822`–`0023682E`), then `[0208E688] + slot × 0xF50` (`00236833`–`0023683A`) — O(1) | slot out of range; **it never checks that the slot is occupied** |
| `BattleUnit_GetSlotCount` `00236850` | — | `[0208E6A0]` (`00236850`) | — |
| `ActorManager_GetRecordByOrdinal` `00358940` (75 callers) | a manager and an ordinal | `manager+8` array: `count = [arr]`, entry `[arr + 8 + i × 8]` (`00358940`–`00358955`) — O(1) | no array, negative or `≥ count` — **no generation check** |
| `ActorHandle_EncodeRegistryEntry` `003589B0` (63 callers) | a registry entry | `((entry+0x16 & 0x7FF) << 20) \| ((entry+0x15 & 0xF) << 16) \| entry+0` (`003589B5`–`003589D0`) | NULL entry → handle 0 |
| `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0` | a packed handle | class = bits 16–19 (must be `< 5`, `003588DF`), manager `02098E10 + class × 0x288` (`00263FF0`), manager checks (`+0` and `+8` non-null, ordinal `< +0x20`, `+0x10` bit 0, ordinal `< [arr]`, `003588EB`–`00358907`), entry `[arr + 8 + ordinal × 8]`, then **generation `entry+0x16` must equal bits 20–30** (`00358913`–`00358925`) | handle 0, bad class, inactive manager, empty entry, **stale generation** |
| `BattleUnit_ResolveByFocusHandle` `0031B7E0` (35 callers) | a packed handle | only while **bit 4 of `02089340`** is set (`0031B7E4`), resolve as above, then `entry+0x30` — the unit pointer (`00263E30`, tail-jumped at `0031B7FE`) | battle system not initialised, or the handle fails |
| `BattleStats_GetByBattleSlotIndex` `00320A40` (18) | **party member index** 0–39 | `*(02EBF190) + 8 + i × 0x1C8` (`00320A40`–`00320A5D`) — a stats record, not a unit | `i > 0x27` |
| `BattleStats_GetByMappedBattleSlot` `00320AB0` (25) | a slot-map key | `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` (a class-`0x17` id, then one of five ~~byte arrays of the block at `+0x5A58`…`+0x5A90`~~ 18-byte arrays of the block at `+0x5A48`, `+0x5A5A`, `+0x5A6C`, `+0x5A7E` and `+0x5A90`, read as bytes at a two-byte stride *(corrected 2026-10-02, OPUS: `0031B9F0+0x4D` to `+0xBA`)*), then the same party element (`00320AB9`–`00320AD9`) | invalid id or mode, index `> 0x27` |
| `BattleUnit_FindByCombatantId` `0031B770` (10) | **party member index** 0–39 | builds the party element (`0031B77B`–`0031B790`) and **scans every pool slot for a unit whose `+0x698` equals it** (`0031B79C`–`0031B7C3`) — O(slots) | `i > 0x27`; no unit bound to that party record |
| `BattleStats_FindOwningBattleUnit` `0031B860` (62) | a stats record | the same scan, for any record (`0031B87D`–`0031B8A4`) | NULL record; no unit bound to it |
| `BattleUnit_FindByDefinitionSelector` `002367A0` (10) | a class-2 encoded id | `BattleEncodedId_IsValidForClass(2, id)` (`002367BC`), then a pool walk comparing **each unit's stats record `+4` (u16)** with the id (`002367D3`–`002367F3`), **except that 0xFF is compared as 0xFFFF** (`002367E3`–`002367EE`) | invalid id; no unit whose stats carry it |

**What the table says about the design.**

1. **Nothing points from a stats record back to its unit.** Both reverse lookups — `FindOwningBattleUnit`
   and `FindByCombatantId` — walk the pool comparing `+0x698`. The relationship is one pointer, owned by
   the unit ([the installer](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)),
   and the answer is unique only if no two units are bound to one record: the installer binds each unit to
   its own party element or keep entry, and nothing on the lookup side checks it.
2. **Two names say "battle slot" or "combatant" and mean *party member*.** `BattleStats_GetByBattleSlotIndex`
   and `BattleUnit_FindByCombatantId` index the forty-element party array of the battle-state block; a
   spawned enemy's stats live in its SpawnKeep entry (`+0x80`), so **`FindByCombatantId` cannot return an
   enemy**: whatever its ten callers pass, the answer is a party member's unit or NULL.
3. **Only the handle path guards against reuse.** A packed handle carries the entry's 11-bit generation
   and `003588B0` refuses a stale one; `ActorManager_GetRecordByOrdinal` and `BattleUnit_GetBySlotIndex`
   return whatever occupies the index now. Code that stores a slot or ordinal across frames is trusting the
   occupant not to have changed; code that stores a handle is not.
4. **The focus handle is dead outside an initialised battle system.** `ResolveByFocusHandle` checks bit 4
   of `02089340`, which `BattleSystem_InitializeAreaState` `002342F0` sets (`00234339`) and the reset
   `002341C0` clears (`002341E4`); until then every focus resolution is NULL regardless of the handle.
   The initializer's full 12-member exclusive subtree — LCG seed, state resets, nav-grid rebuild — is
   bound on [the battle-unit page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md).
5. **`FindByDefinitionSelector` is how orders name a party member.** The battle locomotion decoder's
   opcodes `0x4026`–`0x4035` call it with `opcode − 0x4026` (`00312970`–`00312976`) and send the unit it
   returns down the same go-to-unit path as the focus-handle opcode `0x414A` (`0031297B` → `00312918`,
   `00312A46`); so those sixteen opcodes are "go to the unit whose stats id is 0–15", and `002367A0` is
   their target resolver, not their handler.

**Not established here:** which ids pass `BattleEncodedId_IsValidForClass(2, …)` and therefore whether the
0xFF → 0xFFFF substitution is reachable; whether any caller stores a slot index across a pool reset.

## 3. Key addresses

| Address | Name | Size | Callers | Verified |
|---|---|---:|---:|---|
| `00265020` | `Actor_GetWorldPosition` | 61 B | 79 | ✅ read |
| `003148F0` | `WorldTransition_GetActiveOrPendingFieldId` | 27 B | 49 | ✅ read |
| `00236820` | `BattleUnit_GetBySlotIndex` | 37 B | 40 | ✅ read |
| `00362850` | *(Audio)* — calls `Actor_GetWorldPosition` | 1,036 B | — | not read *(answered: see the world-tick page's EX-3, the audio listener update; 2026-10-02, OPUS)* |
| `00233780` | `SpawnKeep_RotatePersistenceBanksForAreaTransition` | 672 B | — | not read *(answered: see the shared-neighbours page, read in full 2026-09-14; 2026-10-02, OPUS)* |
| `002F8060` | `BattleUnit_TryTriggerNearbyAuthoredFieldAction` | 648 B | — | not read |
| — | `SaveImage_GetPersistentPayloadBase` | — | — | not read *(answered: see U-5, ANSWERED 2026-09-12 (FABLE); 2026-10-02, OPUS)* |

## 4. Data structures and formulas

```
Save image persistent payload      base from SaveImage_GetPersistentPayloadBase()
  +0x1044   i32   active or pending field (area) id; negative means none
```

**Current area:**

```
areaId = max(0, savePayload[0x1044])
```

**Position read** (from Actor/Entity, repeated because all 79 callers inherit it):

```
class = bActor_class_flags >> 5
position readable iff class == 1 || class == 3
(x, y, z) = movementState[0], movementState[1], movementState[2]
```

**Slot lookup** (from Actor/Entity, inherited by all 40 callers):

```
slot(i) = (0 <= i < g_nBattleUnitSlotCount) ? g_pBtlWorkArray + i : NULL
```

## 5. Call chain

```
                       +-- Script VM (23)
                       +-- Movement (16)
Actor_GetWorldPosition +-- Presentation (5)
     (00265020)        +-- Spawn (3), Combat (4), Party (3), Rewards (2)
                       +-- Audio (1)  <- 3D positional audio
                       (class 1 or 3 only, else nothing)

                                            +-- World/Area/Field (10)
SaveImage_GetPersistentPayloadBase           +-- UI (5)
  -> +0x1044 -> WorldTransition_Get...FieldId+-- Movement (3)
        (003148F0)                           +-- Spawn: bank rotation (1)
                                            +-- Combat: field actions (2)
                                            +-- Achievements (1), Save (1)

                          +-- Movement (10)   <- largest consumer
BattleUnit_GetBySlotIndex +-- Combat AI (5), Combat Action (4), Formula (2)
     (00236820)           +-- Party (2), Actor (2), Spawn (1), Items (1), UI (1)
```

**Upstream:** for hub 2, the save/persistence layer — the area id is save state.
**Downstream:** effectively the whole engine.

**Do not confuse with:** ownership. A subsystem calling one of these hubs does not own it. The
evidence standard explicitly bans "caller ownership implies callee ownership", and nothing here
reassigns an owner — these are read-only accessors consulted across owner boundaries.

## 6. Modding notes

- **These are the highest-blast-radius functions in the game.** Hooking `Actor_GetWorldPosition`
  affects audio, rendering, script, movement, spawning, combat and rewards simultaneously.
- **The current area id is save state at payload `+0x1044`.** Editing it in a save file changes
  where the game thinks you are, and every one of those 49 callers will believe it.
- **Negative area ids read as 0, not as an error.** Do not use `-1` as a "no area" sentinel and
  expect callers to notice.
- **The BattleUnit pool is not combat-only.** Movement walks it more than Combat AI does; a mod
  changing pool semantics changes locomotion too.
- **Position is class-gated.** All 79 callers get nothing for a class-0 actor. If a hooked
  position read returns garbage, check the actor class before suspecting the hook.
- **XIIOnline:** all three hubs read *local* state — local actor positions, the local save
  payload, the local slot pool. Every one is a place where two clients will legitimately disagree.
  The area id being save state is the sharpest: area identity must be reconciled from an
  authority, not read per-client from a local save payload.

## 7. What is not known

- [x] **UQ-30.** What else lives in the save persistent payload around `+0x1044`. **U-1 — would open the *(closed — the register row is WITHDRAWN.)*
      save format.**
- [x] ~~What the "pending" half of the name means — is there a second field for in-flight
      transitions?~~ **U-2 ANSWERED 2026-09-12 (FABLE): not in this getter.** `WorldTransition_GetActiveOrPendingFieldId`
      (`003148F0`, 27 B) reads **one** field — the persistent payload's dword `+0x1044` — and returns it,
      or 0 when it is negative (`003148FB`–`00314903`); the "pending" is the GFZ name's gloss on the
      payload field being written ahead of the transition it names, not a second field. What writes
      `+0x1044` and when is the residue that U-1 covers.
- [x] ~~The 21 + 16 + 12 callers with no owner tag: which subsystems they belong to.~~ **U-3
  ANSWERED 2026-09-12 (FABLE)** — every untagged caller attributed from three independent signals
  (its GFZ code-domain tag, the named functions on either side of it, and its named callees),
  listed with that evidence in [`untagged-hub-callers.tsv`](untagged-hub-callers.tsv) beside this
  page (49 rows: 16 + 21 + 12). By subsystem:
  - **Hub 1 (`Actor_GetWorldPosition`, 16):** Battle — `002FA3B0`, `002FB8C0`, `003091C0`, `00317D80`,
    `0031ACC0`, `0031ADB0`, `0031E630`, `00322490`, `00339630` (all between `BattleAction_*` /
    `BattleUnit_*` / `PartyFocus_*` neighbours and calling them); the battle **action timeline
    interpreter** `003B8670` (BQ-12); Presentation — `0037AD40` (tagged `CodeDomain.Presentation`);
    VFX — `00255CF0`, `00258190` (between `SaveImage_ValidateRuntimeF…` and `VFXSystem_RenderLayerPass`,
    calling `ActorRuntime_GetClass3FloatPair`); the actor runtime pass — `003DE640`; UI/Input —
    `00402F00` (beside `InputControl_GetRegistered…`) and the 4.8 KB input-state dispatcher
    `002B7B80` (calls `InputGameplay_TestCombination…`).
  - **Hub 2 (`WorldTransition_GetActiveOrPendingFieldId`, 21):** the **navigation-map UI family**
    `003BD480`–`003C1070` (ten functions between `BattlePresentation_Enqueue…` and `003C3340`,
    calling `MapRef_GetPersistenceGroupId` and `PersistentFlag_Query…`) and its two neighbours
    `003C5FB0` / `003C60F0` (the revealed-tile copy of FG-1); Loot — `002FAED0`, `002FAFD0` (beside
    `Loot_FindOverlappingPickupIndex`, calling `BattleUnit_GetPartyLeader`); Battle — `002F82F0`; Movement —
    `002E3D40` (beside `Movement_ComputeDeltaFromH…`, calling `MapRef_GetPrimaryFieldVa…`);
    Battle-formula / render bounds — `0046B3F0`; Input — `002B7B80`, `002BAF80` (the two 4.8 KB
    dispatchers), `005369C0` (beside `InputDevice_QueryAvailabil…`); World-area-field — `00576A50`
    (tagged `CodeDomain.WorldAreaField`).
  - **Hub 3 (`BattleUnit_GetBySlotIndex`, 12):** all Battle — `0030C0E0`, `0030C210`, `0031B690`,
    `0031C0F0`, `00320BB0`, `00320CF0`, `00322A80`, `003230E0`, `00324380`, `00327150`, `00329220` (the
    unit display-record builder), `0032A060` — every one sits between `BattleUnit_*` /
    `BattleStats_*` / `BattleSlotMap_*` names and calls `BattleUnit_GetSlotCount` or the hub itself.
  The owner-tag gap was the GFZ's, not the code's: none of the 49 is cross-subsystem in any way the
  named neighbourhood does not already show.
- [x] Whether Movement's 10 `BattleUnit_GetBySlotIndex` call sites are hot or cold paths — call *(closed — the register row is WITHDRAWN.)*
      sites are not call frequency. **U-4.**
      *Bounded 2026-09-22 (FABLE), frequency still ASTRA's:* the ten are 11 sites in 10 functions;
      **exactly one is both loop-resident and reachable from the per-frame world tick** —
      `PartyFollow_SolveFormation` (`00338490`) — and **four are neither**. See the section above
      for the table and for what the direct-call-only walk cannot see.
- [x] ~~`SaveImage_GetPersistentPayloadBase` itself is unread.~~ **U-5 ANSWERED 2026-09-12 (FABLE):** `002EF2B0` is `SaveImage_GetActiveRuntimeBuffer() + 0x200` — the buffer getter (`002EF640`) returns the static at `02164280`, so the persistent payload is the active runtime image from its `+0x200` on ([the storage-class page](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md) §2.3, where the script `global` class is shown to be this same base).
- [x] ~~Whether other hubs of this size exist that the audit has not yet surfaced.~~ **U-6 ANSWERED 2026-09-19 (OPUS):** no — at the three hubs' own band (≥ 40 callers) the census finds 219 hubs with 0 uncited, and in their exact shape (≤ 128 B, ≥ 40 callers, ≥ 2 `CodeDomain`s) all 78 are explained; uncited hubs begin only below the size (2 at ≥ 15, 8 at ≥ 8).

## `U-4` bounded — one of Movement's ten sites is the hot candidate (FABLE, 2026-09-22)

**Hot-or-cold is a frequency question and stays ASTRA's.** What a static reading *can* decide is
the two properties that make a site hot: whether the call sits **inside a loop** in its own body,
and whether its function is **reachable from the per-frame world tick**. Neither proves frequency;
both absent is the strongest cold signal available without running the game.

> **A count reconciliation first, because it is the same distinction twice over.** The hub has
> **46 call sites in 40 distinct functions** — §'s “40 callers” is *functions*. Movement holds
> **11 sites in 10 functions** (`00336710` contains two), which is exactly `U-4`'s ten.

| function | in a loop | reachable from the world tick |
|---|---|---|
| **`00338490` `PartyFollow_SolveFormation`** | **YES** | **YES** |
| `003357B0` `BattleLocomotion_QueryDynamic…` | — | YES |
| `00336710` `BattleLocomotion_BuildSolverCo…` (2 sites) | — | YES |
| `003377C0` | — | YES |
| `00326D60` | YES | — |
| `003278D0` | YES | — |
| `00338140` `BattleLocomotion_ResolveTarget…` | — | — |
| `0033C310` | — | — |
| `0033CEF0` | — | — |
| `0033D200` | — | — |

**Exactly one site is both: `0033905F` inside `PartyFollow_SolveFormation`.** *A per-frame body
looping over party members is the one place in Movement where this hub can be called many times a
frame*, and it is the site to measure first. **Four of the ten are neither**, which is the
cold end of the same bound.

> **What this reading cannot see, stated because it decides how much weight the negatives carry.**
> The reachability walk follows **direct calls only**. It reaches **9,771** functions from the tick,
> so *“reachable” is a weak signal* — almost everything is. **The informative half is the negative**,
> and it is exactly there that the method is weakest: a function entered through a vtable or a
> function pointer is invisible to it, so *“not reachable” means “not reachable by a direct-call
> path”, not “never runs”. Loop detection is likewise a backward jump inside the body itself and
> does not see a loop in a caller.

**Controls:** the sweep reproduces the published **40** distinct callers, and the tick walk
contains `WorldActorScriptVM_InterpretBytecode` (`0025E4C0`), which is known to be per-frame.

**Story/quest-layer adjacency, accounted** (18 edges): the save-payload getter `002EF2B0` (U-5)
is called by twelve `0032Axxx` story/quest bodies (`0032AA60`, `0032A930`, `0032ABF0`,
`0032A8A0`, `0032ACF0`…), and four cited hubs call the persistent-flag accessors `0032A8A0`,
`0032AA60`, `0032AD70` — `002F8060` → `0032AD70`, `002FAED0` → `0032AA60`, `002FAFD0` →
`0032AD70`, `003BD480`/`003C0F70`/`003C18A0` → `0032A8A0`. Quest and story gating reads the same
shared state these hubs expose — that is what "cross-subsystem" means here, so the crossing is the
page's subject rather than an anomaly.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Area id is `savePayload[0x1044]`, negative clamped to 0 | complete body of `003148F0` | 1 |
| Caller counts and subsystem breakdowns | full call-graph reverse-edge census over `edges.tsv` (38,161 functions) | 1 |
| Audio reads actor world position | edge `00265020` ← `00362850`, an Audio-tagged 1,036-byte function | 1 |
| Spawn bank rotation consults the area id | edge `003148F0` ← `00233780` | 1 |
| Movement is the largest `BattleUnit_GetBySlotIndex` caller | 10 Movement callers vs 5 Combat AI, from the same census | 1 |
| Position class gate applies to all callers | complete body of `Actor_GetWorldPosition`, already documented | 1 |

### How this document came to exist

It was not planned. Cross-reference audit pass 3 ran `audit_crossrefs.py` over all 33 existing
documents and reported **128 UNACCOUNTED NEIGHBOUR findings across 43 documents** — cross-subsystem
call edges that the documents citing those addresses never mentioned.

The hard checks came back clean: **zero GHOST ADDRESS, zero BODY DRIFT, zero CLASSIFICATION
findings.** Every address cited anywhere in the database resolves in the current program and its
body extent matches. So the audit found no false claims — it found *missing* ones.

Dispositioning those findings is what surfaced all three hubs. The Audio → position edge, the
spawn-bank → area-id edge, and the Movement → BattleUnit asymmetry were each sitting in the
findings list as a line of noise until the callers were counted.

**This is the audit working as intended.** The instruction was that information must earn its
place by surviving an attempt to disprove it. Here the attempt found nothing false and instead
exposed a whole layer that had been invisible because every individual document was looking only
at its own category.

### What is deliberately not claimed

The caller counts are **call sites in the static call graph**. They are not execution counts, not
weighted by frequency, and not proof that a path is hot. "Movement is the largest consumer" means
it has the most call sites — recorded as **U-4** rather than dressed up as a runtime claim.

The 49 callers of hub 2 include 21 with no owner tag, and hub 1 has 16. Those are not silently
dropped from the totals; they are listed, and identifying them is **U-3** *(answered: see U-3, ANSWERED 2026-09-12 (FABLE); 2026-10-02, OPUS)*.

## 9. Related

- [`../../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md`](../../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md) — hubs 1 and 3 are documented in detail there; this page adds their reach
- [`../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) — the bank rotation that consults hub 2
- [`../../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md) — the largest consumer of hub 3
- [`../../18-Audio/`](../../18-Audio/) — the positional-audio caller of hub 1
- [`../../_index/CALL-CHAINS.md`](../../_index/CALL-CHAINS.md) — cross-subsystem chains register
- [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) — the ban on caller→callee ownership inference

## 9. Falsification pass 2026-09-02

**Attack chosen.** This document is three counted tables with stated totals — exactly the shape that
failed in
[`../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
§9, where a correct total sat over a breakdown that misfiled 256 functions. All three tables were
therefore recounted **row by row** from the call graph, not just checked for sum.

### SURVIVED: all three tables, every row

| Hub | Callers | Rows verified |
|---|---:|---|
| `Actor_GetWorldPosition` (`00265020`) | 79 | **12 / 12 exact** |
| `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) | 49 | **11 / 11 exact** |
| `BattleUnit_GetBySlotIndex` (`00236820`) | 40 | **10 / 10 exact** |

Every subsystem row matches the census exactly.

> **Retracted 2026-09-02, one pass later.** This paragraph originally continued: *"the tables also
> survive a check they did not claim — for all three hubs the number of call-graph edges equals the
> number of distinct callers (79/79, 49/49, 40/40), so no function calls any of these hubs twice."*
> **That check is vacuous.** `edges.tsv` holds exactly one row per caller-callee pair — 90,525 rows
> across 90,525 distinct pairs, zero duplicates — so an edge count *always* equals the distinct
> caller count, for every function in the binary. It can never show that a caller calls a hub only
> once. The row counts above stand; the extra inference drawn from them does not.

### OVERTURNED: "the most-consulted function found in the database so far"

It is not. Ranking every address this database cites by caller count:

| Callers | Function | |
|---:|---|---|
| 2,309 | `00584730` | cited here |
| 750 | `00682980` `checkPhyreObject` | documented in the Lua bindings doc |
| 461 | `008119F0` `lua_type` | documented in the Lua bindings doc |
| **87** | `002ED570` `ResourceTable_ResolveEntryByIndex` | **owner `Resource` — not middleware** |
| 79 | `00265020` `Actor_GetWorldPosition` | |

The middleware entries could be argued away as infrastructure. `ResourceTable_ResolveEntryByIndex`
cannot: it carries a **`PrimaryOwner` of `Resource`**, is 146 bytes of engine code, and is cited in
[`../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md`](../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md).
**87 > 79**, so the superlative fails on its own terms.

### The true superlative is about reach — and this hub is 6th

The document's actual subject is cross-subsystem *reach*, so the right measure is how many distinct
**owner subsystems** appear among a function's callers. Over all 478 functions with ≥ 20 callers:

| Subsystems | Callers | Function | |
|---:|---:|---|---|
| 19 | 2,209 | `__security_check_cookie` | CRT |
| 17 | 815 | `ImageAddress_ResolveRuntimePointer` | runtime infrastructure |
| 17 | 615 | `memset` | CRT |
| 15 | 2,479 | `_guard_check_icall` | CFG stub |
| **15** | **110** | **`FieldData_GetActiveFieldRecordBit15`** (`00377C20` **+ its thunk `00313F60`**) | **gameplay — corrected 2026-09-02** |
| 11 | 79 | `Actor_GetWorldPosition` | **this hub — rank 6 of 478** |
| 10 | 49 | `WorldTransition_GetActiveOrPendingFieldId` | hub 2 |
| 9 | 40 | `BattleUnit_GetBySlotIndex` | hub 3 |

Excluding CRT and runtime plumbing, the widest-reaching **gameplay** function in the executable is
not an actor accessor at all — it is `FieldData_GetActiveFieldRecordBit15`.

> **Corrected 2026-09-02.** This table originally listed **two** rows for that name — `00377C20`
> with 13 subsystems / 65 callers and `00313F60` with 11 / 47 — treating them as different
> functions. **`00313F60` is a five-byte `JMP rel32` thunk to `00377C20`.** They are one
> implementation reached two ways, and the two caller sets are almost disjoint: only **2** functions
> call both. Combined, the predicate has **110 distinct callers across 15 owner subsystems** —
> tying `_guard_check_icall` and beaten only by CRT and runtime plumbing. Splitting it in two
> **understated the very finding this section was making.**

**A defensible claim survives:** `Actor_GetWorldPosition` is the most cross-subsystem *actor-state*
accessor, and hubs 2 and 3 rank 10th and 12th overall. That is a real finding. "Most-consulted in
the database" was not.

### An independent corroboration for another document

`FieldData_GetActiveFieldRecordBit15` topping the gameplay list is not a loose end — it is the
accessor inside the engine-wide predicate

```c
((layer0 | layer1) & 0x80000003) != 0 && FieldData_GetActiveFieldRecordBit15() == 0
```

which [`../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md`](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)
records as the engine-wide convention on the strength of **ten independently-read sightings**. Those
sightings are qualitative evidence gathered one function at a time. This census is **quantitative and
independent**: of every function in the binary, its field accessor has the widest subsystem reach of
any gameplay function. Two unrelated methods, the same conclusion.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `003BED70` | 1720 | large hub body (callers `002B7B80`/`002BAF80`/`00402A40`): `003C0340` x4, `003BF430` x6, `003C18A0`, `003C0F70`, `003BE1E0`, `003C0380`, `003BF5E0` — the `003BExxx`/`003C0xxx` evaluation family; interior verified 2026-09-17 (SWE2-FRONTIER): `003C0340` first at [`003BEDDF`](../../_index/ADDRESS-INDEX.md) |
| `004044D0` | 606 | `[rdi+0x4C]`/`+0x18`/`+0x1A` + `[rsi+0x58..0x90]` field pass: `002B3400`, `002718C0`, `00254A10`, `002F9860`, `002D8670` |

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This index named these bodies only at their entries. Each interior address was read in the shipping
image; the notes say what the instruction does, not yet the body's full role.

| body | interior cite | what is there |
|---|---|---|
| `002B7B80` | `002B8048` | `mov word ptr [rip+…], …` — writes `0209E5B8`, the selector word this hub's sibling writes at `0209E5E8` |
| `002BAF80` | `002BB4AC` | `mov word ptr [rip+…], …` — writes `0209E5E8`; same accessor-hub shape as `002B7B80` with `01E0C1D8`/`01E0C1DC` counter updates |
| `00339630` | `00339670` | `call BattleUnit_ResolveByFocusHandle` — first call inside `BattleAction_FindApproachGeometryAroundTarget`, before two `Actor_GetWorldPosition` reads |

*(Pass 22 adjacency, 2026-09-14, tail row: the accessor hubs also reach the **rng** stream —
`002342F0` calls `00328D80`, and `002F8060`/`002FAED0`/`002FAFD0` call `00379CD0` (4 edges).
Randomness is one more shared service the hubs consume; same argument as the story/quest note.)*

## The `002F8060` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002F8060` (~~`BattleUnit_TryTriggerNearbyAuthoredFieldAction`, ~128 B~~ `BattleUnit_TryTriggerNearbyAuthoredFieldAction`, 648 B *(corrected 2026-10-02, OPUS: its extent is 648 B, as the key table above states)*) —
a seven-register body over the `0x98`-byte frame.

| member | role | interior |
| --- | --- | --- |
| `002FB3B0` | `dword[+0x28]`-counted walk — count <= 0 out, else `r9` strides the record (`002FB3B5`/`002FB3BC`) | [`002FB3B5`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citations — frontier shared-callee hub `002F9860` (2026-09-17, SWE2-EC7)

`002F9860` — the largest frontier shared callee after `0020E620` (129 callers at census).
Interior verified: [`002F9866`](../../_index/ADDRESS-INDEX.md) is `mov eax, 0x10624DD3`, opening the
signed-magic divide that splits the argument: `id / 1000` selects a bucket (bounded `< 0x1C` = 28)
in a qword presence table at `image+0x2DA3D80`, whose sibling pointer table at
`image+0x2E773C0` gives a per-bucket record; `id % 1000` is bounds-checked against the record's
dword count at `+0x04`, then indexes a dword array reached through the encoded pointer at
`+0x14` — every stored pointer resolved through `0020E600`. Returns ~~`01C8B638`~~ `01CEB638` *(corrected 2026-10-02, OPUS: `002F9860+0x1E` `lea rax, [01CEB638]`)* (a static empty
record) on any miss: out-of-range bucket, absent bucket, or index past the slot count.

So the function is the **encoded-id → runtime record resolver** — the bucketed lookup the
encoded-id page's query record feeds. NOT claimed: which subsystem's records the 28 buckets hold,
or whether bucket/1000 granularity is authored or a storage detail.

## Interior citation — frontier hubs `00264010` / `00263F10` (2026-09-17, SWE2-EC7)

Two more accessor leaves over this page's named resolver trio (`00358940` =
`ActorManager_GetRecordByOrdinal`, `003588B0` = `ActorHandle_ResolveRegistryEntryByPackedId`):

- `00264010` (53 B, 32 frontier callers) — the sign router between them. `ecx >= 0` tails straight
  to `00358940` with `rdx=ecx`; `ecx < 0` first calls `003590D0` and, on a non-null answer, passes
  that as the packed handle to `003588B0` (tail at
  [`00264039`](../../_index/ADDRESS-INDEX.md)). So negative ordinals are interpreted as
  handle-registry probes before the packed-id path runs.
- `00263F10` (44 B, 31 frontier callers) — a record-indirection resolver: when the record's
  `byte [rcx+0x18] == 2`, it replaces the record with `003587C0(sbyte [+0x19], word [+0x1A])` if
  that call answers non-null (call at [`00263F27`](../../_index/ADDRESS-INDEX.md), `cmovne` at
  `00263F2F`); otherwise the original record is returned. A type-2 record is a forward reference,
  not a leaf.

NOT claimed: what `003590D0` resolves the negative value against, or which tag system `+0x18`
carries.

## Interior citation — frontier hub `003587C0` (2026-09-17, SWE2-EC7)

`003587C0` — 50 B, 10 A-measured callers at census; the forward target `00263F10`'s type-2
records resolve through. Interior verified: `call 00263FF0(ecx)` maps the class byte to its
manager, then `ebx` bounds-checks against `[[mgr+8]]` and returns `[tbl + ebx*8 + 8]` at
[`003587DF`](../../_index/ADDRESS-INDEX.md) — the same `[arr + 8 + i*8]` entry shape as
`00358940`, reached through the class byte rather than the manager arg. Negative or
out-of-range -> null.

## Interior citation — frontier hub `002B3400` (2026-09-18, SWE2-EC7)

`002B3400` — 125 B, 7 A-measured callers; the persistent-record sibling of `002B3050`'s
stack-context build. Interior verified: same opener — `002AC1E0` context init (`002B3418`),
`0039BAD0(r8)` kind byte stored to `[rdi+0xA6]` — but writes into the caller's record: when
`00254A10()` is 0 and the kind is 7, `[+0x44]` gains bit 11 and `0039C4A0(bit11)` selects the
table pointer stored at `[+0x60]` ([`002B343D`](../../_index/ADDRESS-INDEX.md)–`002B3452`); `[+0x28]` receives the
`rdx` source, `+0x8C` the literal `0x7D00`, `+0xA3` the byte `2`. A query-record populate, not
a dispatch.


## Interior citation — frontier hub `002EF2B0` (2026-09-18, SWE2-EC7)

`002EF2B0` — 20 B, 70 callers; `SaveImage_GetPersistentPayloadBase`, the U-5 answer recorded
above. Interior verified: `002EF640()` at [`002EF2B4`](../../_index/ADDRESS-INDEX.md) returns
the active runtime buffer, then `add rax, 0x200` at [`002EF2B9`](../../_index/ADDRESS-INDEX.md)
skips the image header — the persistent payload begins exactly `0x200` into the active image,
as the script `global` storage-class section derives.


### Interior citation — frontier hub `002D7580` (2026-09-18, SWE2-EC7)

`002D7580` — 107 B, 7 callers (`002B7B80`, `002BAF80`, `005691E0` above): the
`0209AC30` callback arm — `[+0xD8]` falls back to `[+0x100]`, and the live
one's `[rcx]` vfn is invoked with a `{0x120, movsxd edx, movsxd ecx}` block at
[`002D75D7`](../../_index/ADDRESS-INDEX.md), cookie-guarded. Sibling shape of
`002C9EB0`'s `0x11F` arm.
### Interior citation — frontier hub 003AA280 (2026-09-18, SWE2-EC7)

**003AA280** (95 B, 4 A-measured callers) — a three-field matcher over the `02EBF370` chain — the same record family `003B8670` (ownerless-shared-scratch §2) walks. Match on `[+0xC] == ecx`, `[+0xE] == edx`, `[+0xF] == r8b`; on miss `0020E600([rax])` takes the next node. Three independent callers across Presentation and the audio pack — a true cross-subsystem accessor. In-scope: triple compare [`003AA2A1`](../../_index/ADDRESS-INDEX.md); `0020E600` advance [`003AA2C3`](../../_index/ADDRESS-INDEX.md).

## SWE2-EC7-26 update (2026-09-18) — `00317D80` two-stage query compose

`00317D80` (94 B) is cookie-checked (`00808C40`): `00265020(rcx, &o1,
&o2, &o3)` fills three stack outs, `xmm0` is zeroed into `+0x2C`, then
`003223C0(rcx, &o1)` composes and `setne` makes the bool — the
query-then-compose truth test the availability and hub callers share.
Interior anchor `00317DA7` (the `00265020` call).

## SWE2-EC7-35 update (2026-09-19) - `0037AD40`

`0037AD40` (742 B) is an accessor-hub body - `02EBF460`/`02ADD8E0`/`02EBF464`/`02EBF438`/`02ADD8F0` state, four `0037A5B0` plus `00265020`. Interior anchor `0037AE0D` (an `0037A5B0` call).

## SWE2-EC7-36 update (2026-09-19) - `004044D0`

`004044D0` (606 B) is an accessor-hub body - `01CEBB70`, `002F9860`/`002D8670`/`002B3400`/`002718C0`/`00808C40`. Interior anchor `0040450B` (an `00808C40` call).

## SWE2-EC7-37 update (2026-09-19) - `00402F00`

`00402F00` (545 B) is an accessor-hub body - `01CEBDA0`/`01F44830`/`008C5FD0`/`01CEBBA8`, `003C8060` pair plus `00264790`/`0035D320`/`003588B0`/`00265020`/`003C3F90`/`00203170`. Interior anchor `00402F2D` (a `00264790` call).

## SWE2-EC7-50 update (2026-09-19) - `003DE640`

`003DE640` (183 B) is the actor runtime pass - `00264010`/`00265020`/`002E97B0`/`003ABD00`. Interior anchor `003DE677` (a `00264010` call).

## SWE2-EC7-51 update (2026-09-19) - `0031C0F0`

`0031C0F0` (174 B) is a body - `00236820`/`00236850`/`0031C000`/`00322C50`. Interior anchor `0031C115` (a `00236820` call).

## SWE2-EC7-53 update (2026-09-19) - `0037A5B0`

`0037A5B0` (561 B) is an accessor-hub body - `0020E600`/`003CC5F0`/`00466BF0` plus `008C5B34`/`01CEBC9C` rdata. Interior anchor `0037A5F6` (a `0020E600` call).

## SWE2-EC7-56 update (2026-09-19) - `003C3F90`

`003C3F90` (219 B) is an accessor-hub body - `00203170`/`003977B0`/`003985B0`/`00398C50` plus `00915FE4`/`01CEBB70`/`01CEBDA0`. Interior anchor `003C3FA8` (a `00203170` call).

## SWE2-EC7-61 update (2026-09-19) - `0032A060`

`0032A060` (154 B) is a cross-subsystem accessor hub - `00236820`/`00236850`/`002EAA10`/`00313F60`. Interior anchor `0032A06E` (a `00236850` call).


## SWE2-EC7-67 update - `002FAED0`

`002FAED0` (129 B) is an accessor-hub body - `003148F0`/`0032AA60`/`00379CD0`/`002FB430` x2 plus `02EC3E60`. Interior anchor `002FAEDD` (a `003148F0` call).

## SWE2-EC7-76 update (2026-09-19) - `00264790` gated accessor measured

`00264790` (30 B) is the `02098E20`/`02098E10` gated accessor: flag
bit 0 and the singleton both required, returning `movsx
word[rax+0x7C]`; either missing returns -1 - the accessor the shared
hubs call.
Interior anchor `002647A5` (the `+0x7C` read).

## SWE2-EC7-85 update (2026-09-20) - the `002B7B80`/`002BAF80` accessor row measured

`00402730` (151 B) is the chained-element accessor the hub callers
run: `[global]+0x60` -> `[rax+8]` yields the element, `rcx`/`dx`/
`r8w` store at `+0xC0`/`+0xC8`/`+0xCA`, and when `rcx` and `r8w` are
live the `[[rcx+0x20]+0x30]` word tables index by high/low byte to
extend `[r9+0xCC]` into `[r11+0xC]` - else `[r9+0xCC]` alone.
Interior anchor `0040277E` (the `movzx` word-table read).

`004026D0` (90 B) is the rect copy: `word[rdx+0x30..0x36]` writes
twice, to `rcx+8..+0xE` and again to `rcx+0..+6` - call-free.
Interior anchor `004026EE` (the first `+8` store).

`004026B0` (26 B) is the `byte[+1]`-keyed list find: the
`[rcx+0x60]` chain walks until a record's `+1` byte matches `dl`;
the record or 0 returns - call-free.
Interior anchor `004026BA` (the `[rcx+0x60]` step).

`00402610` (111 B) is the `00275320`-backed record build:
`00275320(&stack, rcx, rcx+8, [rcx+0x10])` resolves, both stack
qwords copy to `rsi`, `word[rdi+0x30..0x36]` land at `rsi+8..+0xE`,
and `dword[rsi+0x10]` zeroes.
Interior anchor `00402635` (the `00275320` call).

## SWE2-EC7-86 update (2026-09-20) - `00402200` + `003EC700` measured

`00402200` (27 B) is the sibling ancestor walk for flag bit 5:
from `rcx` it follows `+0x60` links until `byte[+0x28] & 0x20`
holds, returning that node - or NULL when no ancestor is flagged
(`00402230` returns `rcx` in the same case).
Interior anchor `00402205` (the `+0x28` bit-5 test).

`003EC700` (28 B) is the two-hop forward the shared-accessor
callers run: `003EB720(rcx)` resolves the record, then a tail
`002E7410(resolved, edx)` finishes the query.
Interior anchor `003EC717` (the `002E7410` tail).

## SWE2-EC7-88 update (2026-09-20) - `003C4AB0` + `003C0CF0` + `003BF430` measured

`003C4AB0` (21 B) is the delta forward the hub callers run:
`002DD550(02EBA488, 02EBA484 - 02EBA488)` - the adjacent-label
delta (-4) forwarded with the data pointer.
Interior anchor `003C4AC0` (the `002DD550` tail).

`003C0CF0` (64 B) is the two-slot status probe over
`[02B457E0+0x120]`: slots 0-1 (0xA8 stride) whose
`byte[+0x10]` matches `ecx` yield 1 when `qword[+8]` is null
and 2 when it is live; a miss returns 0.
Interior anchor `003C0D23` (the matched-slot arm).

`003BF430` (237 B) is the two-level packed resolver the hub
callers run: `[02B457E0+0xE0]`'s `byte[+9]` bounds the first
index into a `word`-relative block; the second index is bound
against that block's `byte`/`byte[+1]` ranges and picks either
the `r9+4+idx*24` direct arm (`out-mode` 0) or the
sub-byte-index arm (`out-mode` 1), with `out-mode` defaulting
to 3 on the header path - a 24-byte element resolver with a
mode out-param.
Interior anchor `003BF4E8` (the mode-1 arm).

## SWE2-EC7-89 update (2026-09-20) - `003C18A0` mode-0 word fetch measured

`003C18A0` (220 B) is the mode-0 arm `003BF920` dispatches to:
`003BCBA0(rdx)` supplies the flag set, `word[+0xE]` shorts
through `0032A8A0` (clean record) or `00309EC0` (the `+0x10`
`0xFC0` arm), the result assembles a flag byte, and the return is
1 only when `word[+0xC]` matches `0037ED70()` or the
`byte[+0xCA] == 6` arm confirms `0037ED80() == 1` - with a null
`[02B457D8]` forcing 0 on the flag-clear path.
Interior anchor `003C18E2` (the `0032A8A0` call).

## SWE2-EC7-90 update (2026-09-20) - `003BCBA0` flag-word builder measured

`003BCBA0` (255 B) is the flag-word assembly both `003BF920`
arms call: `word[+0xC]` runs `003C0380` -> `003C1070` for bit 0,
`00255200` sets bit 0xA, `003C06E0`'s bit-8 arm resolves via the
`>>4` complement or `00264F90` + `002543F0`, bit 2 joins under a
`002543F0` nonzero, bit 0xF under the `+0xD0` `0x800` bit, and the
`003BE2D0`/`004022F0` arm re-masks the whole word to `0x2800` when
neither the `0x800` flag nor `byte[+0xCA] == 6` applies and `ebx`
is empty - bit 0xC armed on the path out.
Interior anchor `003BCBB8` (the `003C0380` call).

## SWE2-EC7-91 update (2026-09-20) - `002543F0` keyed table probe measured

`002543F0` (71 B) is the probe `003BCBA0`'s flag-word arm runs:
`word[[rip-table] + 0xC]` selects a sub-table, `word[rdx]` bounds
`ecx`, and the `word[rdx + ecx*2 + 2]` key must not be `0xFFFF` -
~~`00309EC0(ecx, 0)` then returns the boolean the caller folds into
bit 2 of the assembled word.~~ `00309EC0(ecx)` then returns the **signed mode-0 value**. For the
packed-count classes that is free = total − reserved, and it can be negative. For the bitset
classes it is the owned bit, and it is −1 for a sentinel id. The caller booleanizes it with
`test eax, eax` / `setne` (`0025442B`–`0025442D`) and folds that into bit 2 of the assembled
word, so a negative balance or a nibble-`F` sentinel counts as set. *Corrected 2026-09-26 (FABLE,
Claude Opus 5.5): the dispatcher returns a value, not a boolean. See
`_index/candidates/query-abi-meaning-check.md`, where the dispatcher's positive-only sibling reads
the same value the other way.*
Interior anchor `00254424` (the `00309EC0` call).

## SWE2-EC7-92 update (2026-09-20) - `0037ED80` get-or-default measured

`0037ED80` (35 B) wraps `0037EC70` for the `003C18A0` accessor
callers: it fills a stack dword through the helper and returns it,
answering 2 instead when the helper reports 0.
Interior anchor `0037ED89` (the `0037EC70` call).

## SWE2-EC7-95 update (2026-09-20) - `00320A30` measured

`00320A30` (16 B) is the `+0x698` link read `002F8060`,
`002F8E70`, `002FA290` and `00469A50` share: null in, null out;
otherwise `[rcx+0x698]` comes straight back - the minimal
two-line accessor the whole fan-in goes through.
Interior anchor `00320A38` (the `+0x698` load).

## SWE2-EC7-96 update (2026-09-20) - `002FB430` measured

`002FB430` (208 B) is the three-slot ring inserter `002FAED0`
and `002FAFD0` call: a `+0x28`-counted scan of the `0xC`-stride
entries finds `edi`; a hit sets bit `1<<r8` in `+8` and merges
`(r9<<r8)` into `+4` after clearing the old bit, while a miss
appends at the `[rbx+0x24]` write slot with `+8 = 1<<r8`,
`+4 |= r9<<r8`, `[entry] = edi`, the count incrementing to a
cap of 3 and the write slot advancing mod 3 (the `0x55555556`
divide).
Interior anchor `002FB4E6` (the hit-arm `or` into `+8`).

## SWE2-EC7-104 update (2026-09-20) - `00264ED0` measured

`00264ED0` (49 B) is the indexed word fetch
`003EA6E0` and `005369C0` call on the
`02099D88` table: entry =
`table + dword[table + 4] + ecx * 8`, and the
answer is `word[entry + 4]` - returning 0 when
the table, its `02099D90` companion pointer,
or the computed entry is null. One of the
small shared lookups the hub pattern predicts.
Interior anchor `00264EE9` (the table-offset
read).

## SWE2-EC7-105 update (2026-09-20) - `00264770` measured

`00264770` (30 B) is the guarded slot read
`002B7B80`, `002BA310` and `004048E0` call:
when `02098E20` bit 0 is armed and the
`02098E10` pointer is live it answers
`movsx word[ptr + 0x7E]`, else `-1` - the
signed-index fetch with a single ready
flag in front of it.
Interior anchor `00264785` (the `+0x7E`
word read).

## SWE2-EC7-106 update (2026-09-20) - `002543A0` measured

`002543A0` (40 B) is the counted-table
relay `002B7B80`, `002BAF80` and
`003BD040` call on the `020927D0`
record: `rdx = rax + word[rax + 0xE]`
locates a counted dword table, `ecx ==
0` or `ecx >= dword[rdx]` answers the
`01CEB638` empty row, otherwise it
reloads `ecx = dword[rdx + ecx*4 + 4]`
and tails `002F9920` - the
bounds-checked index hop in front of
the shared resolver.
Interior anchor `002543BF` (the
`rdx + rax*4 + 4` fetch).

## SWE2-EC7-111 update (2026-09-20) - `0018E470` measured

`0018E470` (34 B) is the
two-call context gate the
whole image shares - the
census shows several hundred
callers across every
subsystem: `0065E5D0(rcx)`
fetches the context object,
`001976E0(result)` runs the
inner predicate, and
`and al, byte[rbx + 0xA0]`
folds the object's own armed
byte into the answer - a
caller's flag byte can veto
the shared gate locally.
Interior anchor `0018E486`
(the `+0xA0` flag fold).

`002718C0` (18 B) is the two-mode flag extract `00554EA0` calls per map marker and `004044D0` shares on the accessor path: `cl` bit 0 clear returns 2, else `dl & 1` is the answer — a flag-byte pair folded to a three-state visibility word.

Interior anchor `002718CB` (function `002718C0`).

`002BA310` (543 B) is the pane constructor `002BAF80` calls: `00264150` and `00402000(r15)` gate, `00244F50(0x3E0, 002BD680, 0)` builds the object with `rsi`/`r15`/`r14` at `+0x3C0`/`+0x3C8`/`+0x3D0`, `003678F0` + `00402000` + `002BA530` size it, `0024ABC0` and the `002D46F0`/`002D4930` pair finish, `00402000`/`002432B0`/`00264770`/`003678F0`/`00808C40` behind - the hub's widget spawn.

Interior anchor `002BA332` (function `002BA310`).

`00402000` (511 B) is the copy-and-resolve `002BA310` calls: `[rdx+0x28] & 0x200` picks a direct buffer or `00403F90` copies it to `[rsp+0x48]` first, `003BE2D0(word[rbx+0x1C])` resolves the id, then `ebp = 3` rounds of `00255150`/`003DFB50`/`003DFBB0`/`003FFF40`/`00808C40` - the hub's record marshal.

Interior anchor `00402054` (function `00402000`).

`00402DB0` (325 B) is the flag-directed chain resolver `002BAF80` calls: `r9b & 0x10` walks `rcx+0x68` to the tail then scans the `+0x60` chain for `byte[+1]==byte[rcx+8]`; `r9b & 0x40` repeats the pattern keyed on `byte[rcx+9]` - two flag-selected sibling/parent resolutions through the accessor hub's chain links.

Interior anchor `00402E58` (function `00402DB0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-EC7)

**Presentation — CLIENT (SWE2-EC7-166, 287 edges).** The accessor-hub
subjects are consulted across the Presentation layer - `0018E470` is
called by `00189CE0`, `00203170` by `00245E60`/`00258350`/`002B7xxx`,
and this page's `00402DB0` chain resolver joins the same pattern through
`002BAF80` (+283 more of the same shape). Consultation of the shared
accessors, not shared ownership.

`00320C60` (63 B) is the two-field flag merge `00273160` and `003C5130` both run: `00263E30` resolves `rcx`, the `[rax+0x698]` sub-object is null-checked, then `dword[+0x64] | dword[+0x3C]` lands in `[rdx]` and `1` returns - `0` on any null leg; the shared-lookup flag reader both callers consult.

Interior anchor `00320C6E` (function `00320C60`).

`0037EC70` (253 B) is the `02AED490`-object status query `0037ED80` runs: `dword[rdi]` takes `2` when the global is absent or its `+0xE0` lacks bit `0x100`; otherwise `00473B70` gives a count and `00473BB0(0, i, count, &pair)` is looped until a `+0x20`-code of `2` or a nonzero `+0x34`, after which `dword[rdi]` is set `2`/`1`/the pending code and `1` returns - the gated result-code producer on the shared object.

Interior anchor `0037ECD1` (function `0037EC70`).

`00202C50` (31 B) is the 16-byte snapshot copier the three unrelated callers share: `00216FC0(&tmp)` fills the stack temp, then `movups` copies both qwords into `[rcx]` - the shared out-param snapshot.

Interior anchor `00202C5E` (function `00202C50`).

`003C2190` (21 B) is the `02B457E0`-bound shim: `rcx` shifts to `rdx`, `rdx` to `r8`, `rcx` loads `qword[02B457E0]` (the encoded-id query record) and the body tail-jumps `003C1F00` - the singleton-bound lane the accessor-hub and widget callers share.

Interior anchor `003C21A0` (function `003C2190`).

**Resource — SERVICE.** `003C1F00` — the body `003C2190` tail-jumps into — calls `00249180`/`00249210` on the resource layer; the shim's real work delegates down, not shared ownership.

**Save/Load — CLIENT.** The save layer reaches helpers cited on this page — `00582790` calls `00249210` and `00280140` calls `002EF2B0`/`002EF640`.

**UI — CLIENT.** `003CB4F0` on the UI layer calls `003C2190`, and the page's cited `00203170` transform helper is reached by the UI layer's callers (`00247AE0`, `002D2600`, `002D28E0`, `00368010` and ~130 more).


`003C1F00` (450 B) is the two-slot accessor `003C2190` forwards to: it scans the `rcx+0x120`/`+0x1C8` pair of `0xA8`-stride slots and refuses when both are live, reads the request's kind byte out of the `02B457E0` `+0xE8` table (the `edi`-indexed `+4` slot byte) and counts how many of the table's `0x32` entries differ to pick the parity arm, then `00249180(rbp, 7, dil+0x142, [r14])` populates the free slot - `rsi+0x10` = kind, `[rsi]` = result, `+0x12` = `[r14+0x10]` - and when the table's `+1` flag byte is set `00249210(rbp, 7, byte+0xE1)` refreshes the `02B457E0+0x118` cache after freeing the old one with `003697F0`, returning 1.

Interior anchor `003C1FD9` (function `003C1F00`).

`002BD590` (227 B) is the node broadcast `002BAF80` runs over `r9`'s `+0x60` next-chain: each node is visited through `002BCB00` with the caller's `ecx`/`edx`/`r8` triple and a marshaled seven-slot out frame - `[rsp+0x20]` pointer, `xmm6` float, the `[rsp+0xD8]` dword, `r13d` or `-1` selected by whether the `[rsp+0xC0]` bound matches the node, then `r12d`/`r15d`/`r14d` - until the chain ends

Interior anchor `002BD5F0` (function `002BD590`).

`004022F0` (214 B) is the group-membership probe `003BCBA0` runs: `rcx == 0` returns 0; for `edi` in 3..8 it `003DFBB0`s each group's count then `003DFB50`s every member - under mode `edx == 0x14` or `edx - 0x17 <= 1` a member `+8` u16 of `0x14`/`0x17`/`0x18` returns 1, otherwise a member `+8` s16 equal to `edx` returns 1

Interior anchor `0040234A` (function `004022F0`).

`00275320` (196 B) is the 8.8 fixed-point vec4 lerp `00402610` calls: for each of four signed words it computes `a + (((b - a) * r9d) >> 8)` between the `[rdx]` and `[r8]` vectors and stores into `[r14]` - the interpolation step shared by the accessor hub's callers

Interior anchor `00275364` (function `00275320`).

`002B9B30` (169 B) is the banked teardown-and-rebuild `002BAF80` runs: under `0209E5F0` it picks the `0xBC10`-stride bank selected by `([+0x179D2] >> 2) & 1`, runs `00244F00`/`0035C080`/`00401FE0` on it, sets `+0x179D2` bit 3, releases `0209E600` and `0209E5F8` when held, calls `0029DF20`, and returns `base + 0x1B0 + bank*0xBC10`

Interior anchor `002B9B5F` (function `002B9B30`).

`00216FC0` (159 B) is the vec3-by-mat4x3 transform `00202C50` calls: `[r8]`'s xyz multiply the `rdx` matrix columns (`+0x00`/`+0x10`/`+0x20` triples), sum with the `+0x30` translation row, and store to `[rcx]`/`+4`/`+8` with `+0xC` zeroed - the shared point-transform primitive

Interior anchor `0021703E` (function `00216FC0`).

`0031BF60` (151 B) is the indexed `02EBF0F8` lookup `0031C000` wraps: `cx == 0xFFFF` or a failed `00322C50(slot 6, cx)` check returns -1; otherwise `[02EBF0F8]`'s `+0xC` id resolves through `0020E600`, the row base is `eax + (cx - 0x1000) * word[02EBF0F8 + 8]`, and the return is `dword[row + 0x30]` - a bounds-checked id-to-dword read off the shared table.

Interior anchor `0031BFE0` (function `0031BF60`).
- **ActorEntity — CLIENT and SERVICE (233 edges).** 125 inbound (ActorEntity bodies `BattleGroup_RefreshFourActorDefinitions` (003266C0), `0046BAC0`, `ActorManager_RunFieldRuntimePass` (0025D9E0) call page-cited `00263FF0`, `ActorManager_GetRecordByOrdinal` (00358940), `PartyFocus_GetCurrentPackedActorHandle` (003590D0)); 108 outbound (page-cited `WorldActorScriptVM_InterpretBytecode` (0025E4C0), `00326D60`, `00329220` call ActorEntity bodies `BattleUnit_GetBySlotIndex` (00236820), `Actor_GetWorldPosition` (00265020), `ActorHandle_ResolveRegistryEntryByPackedId` (003588B0)). Substantive edges include `00203170` is called by `003F1E90`; `002341C0` is called by `002695A0`; `BattleSystem_InitializeAreaState` (002342F0) is called by `ActorSystem_InitializeManagerRuntime` (0026CE60); `WorldActorScriptVM_InterpretBytecode` (0025E4C0) calls `ActorResource_SelectPendingEntryForExecution` (003DB6E0); the remaining edges run through shared helpers the page cites.
- **Audio — CLIENT and SERVICE (15 edges).** 5 inbound (Audio bodies `00362850`, `00261F90`, `00363560` call page-cited `Actor_GetWorldPosition` (00265020), `SaveImage_GetPersistentPayloadBase` (002EF2B0), `WorldTransition_GetActiveOrPendingFieldId` (003148F0)); 10 outbound (page-cited `00362850`, `003B8670` call Audio bodies `00362C60`, `00362E50`, `00363F30`). Substantive edges include `PartyFocus_GetCurrentPackedActorHandle` (003590D0) is called by `00362850`; `00362850` is called by `00363560`; `00362850` calls `00362C60`; `00362850` calls `00362E50`; the remaining edges run through shared helpers the page cites.
- **Combat — MECHANICAL (1 edge).** 1 Combat-side calls into shared helper(s) the page cites (`ActorWork_GetBattleUnitRaw` (00263E30)) - the helpers' general call surface, not a Combat relationship of this page's subjects.
- **CombatAI — CLIENT and SERVICE (33 edges).** 32 inbound (CombatAI bodies `AiOrder_EvaluateTargetSelector` (00301AD0), `BattleUnit_RebuildPerceptionCandidateCache` (003247F0), `BattleEnmity_PropagateToPerceivingFoes` (003219D0) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `BattleUnit_GetBySlotIndex` (00236820), `FieldData_GetActiveFieldRecordBit15` (00313F60)); 1 outbound (page-cited `002341C0` call CombatAI bodies `BattlePerception_ResetCandidateCacheGeneration` (00325080)). Substantive edges include `002341C0` calls `BattlePerception_ResetCandidateCacheGeneration` (00325080); `BattleUnit_GetSlotCount` (00236850) is called by `AiOrder_EvaluateTargetSelector` (00301AD0); `BattleUnit_GetSlotCount` (00236850) is called by `BattleUnit_RebuildPerceptionCandidateCache` (003247F0); `BattleUnit_GetSlotCount` (00236850) is called by `BattleEnmity_PropagateToPerceivingFoes` (003219D0); the remaining edges run through shared helpers the page cites.
- **CombatAction — CLIENT and SERVICE (104 edges).** 92 inbound (CombatAction bodies `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (002F8060), `BattleUnit_CommitAction` (0030F760), `Battle_BuildActionTargetSet` (0030D160) call page-cited `BattleUnit_ResolveByFocusHandle` (0031B7E0), `FieldData_GetActiveFieldRecordBit15` (00377C20), `BattleEncodedId_IsValidForClass` (00322C50)); 12 outbound (page-cited `BattleSystem_InitializeAreaState` (002342F0), `002341C0`, `0031ADB0` call CombatAction bodies `00306570`, `BattleAction_ResetPendingQueueBanks` (0030FE60), `BattleActionSnapshot_ResetPool` (0030E010)). Substantive edges include `002341C0` calls `00306570`; `002341C0` calls `BattleAction_ResetPendingQueueBanks` (0030FE60); `BattleSystem_InitializeAreaState` (002342F0) calls `00306570`; `BattleSystem_InitializeAreaState` (002342F0) calls `BattleActionSnapshot_ResetPool` (0030E010); the remaining edges run through shared helpers the page cites.
- **CombatFormula — CLIENT and SERVICE (105 edges).** 102 inbound (CombatFormula bodies `00384F40`, `BattleStats_GetOwningActorHandle` (0031E800), `BattleStats_FindOwningBattleUnit` (0031B860) call page-cited `RNG_MT19937_NextU32_Thunk` (00379CD0), `BattleStats_FindOwningBattleUnit` (0031B860), `BattleUnit_GetSlotCount` (00236850)); 3 outbound (page-cited `002FA290`, `00329220`, `005369C0` call CombatFormula bodies `BattleStats_FindOwningBattleUnit` (0031B860), `BattleRuntime_GetEffectiveActionId` (00387090)). Substantive edges include `BattleUnit_GetSlotCount` (00236850) is called by `00384F40`; `BattleUnit_GetSlotCount` (00236850) is called by `BattleStats_GetOwningActorHandle` (0031E800); `002F8E70` is called by `00384F40`; `FieldData_GetActiveFieldRecordBit15` (00313F60) is called by `00384F40`; the remaining edges run through shared helpers the page cites.
- **Gameplay — CLIENT and SERVICE (36 edges).** 27 inbound (Gameplay bodies `0031ADB0`, `BattleAction_FindApproachGeometryAroundTarget` (00339630), `00312B40` call page-cited `BattleUnit_ResolveByFocusHandle` (0031B7E0), `FieldData_GetActiveFieldRecordBit15` (00377C20), `ActorWork_GetBattleUnitRaw` (00263E30)); 9 outbound (page-cited `BattleUnit_FindByDefinitionSelector` (002367A0), `002543F0`, `BattleSlotMap_ResolveMappedBattleSlot` (0031B9F0) call Gameplay bodies `BattleEncodedId_DispatchQueryMode0Value` (00309EC0), `BattleEncodedId_IsValidForClass` (00322C50), `BattleSlotMap_ResolveMappedBattleSlot` (0031B9F0)). Substantive edges include `00203170` is called by `BattleAction_FindApproachGeometryAroundTarget` (00339630); `002543F0` calls `BattleEncodedId_DispatchQueryMode0Value` (00309EC0); `002FA3B0` is called by `BattleUnit_SubmitResultReactionMode` (00328480); `BattleEncodedId_DispatchQueryMode0Value` (00309EC0) is called by `0031C5D0`; the remaining edges run through shared helpers the page cites.
- **Input — CLIENT and SERVICE (12 edges).** 9 inbound (Input bodies `00226BE0`, `InputGameplay_ArbitrateDigitalInputAndModalState` (00253C70), `001E0A40` call page-cited `001976E0`, `00263FF0`, `FieldData_GetActiveFieldRecordBit15` (00313F60)); 3 outbound (page-cited `0018E470`, `002B7B80`, `002BAF80` call Input bodies `001976E0`, `InputGameplay_TestCombinedMaskBit1WithTemporalGate` (00250200), `InputGameplay_TestFilteredMask92Bit0WithTemporalGate` (00250130)). Substantive edges include `0018E470` calls `001976E0`; `001976E0` is called by `001E0A40`; `001976E0` is called by `001E0CE0`; `002B7B80` calls `InputGameplay_TestCombinedMaskBit1WithTemporalGate` (00250200); the remaining edges run through shared helpers the page cites.
- **InputGameplay — MECHANICAL (1 edge).** 1 InputGameplay-side call into a shared helper the page cites: `00313A00` calls `FieldData_GetActiveFieldRecordBit15` (00377C20), one of the accessor hubs this page documents (65 callers); the hub's population, not an InputGameplay relationship (re-read 2026-09-30, SWE2-CONTRACT).
- **Items_Equipment_Shops_License — CLIENT and SERVICE (32 edges).** 31 inbound (Items_Equipment_Shops_License bodies `BattleStats_SetEquipmentSlotByMappedId` (0031A510), `Equipment_UnequipEncodedItemFromActiveRoster` (0030FD10), `Equipment_CheckItemEligibleForSlot` (00317930) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `BattleStats_GetByMappedBattleSlot` (00320AB0), `00324380`); 1 outbound (page-cited `00329220` call Items_Equipment_Shops_License bodies `BattleStats_CountLicenseBits00To17` (00324020)). Substantive edges include `BattleEncodedId_DispatchQueryMode0Value` (00309EC0) is called by `Equipment_CheckItemEligibleForSlot` (00317930); `00324380` is called by `Equipment_UnequipEncodedItemFromActiveRoster` (0030FD10); `00324380` is called by `BattleStats_SetEquipmentSlotByMappedId` (0031A510); `00324380` is called by `InventoryEquipment_SnapshotAndClearTemporaryState` (0030FBE0); the remaining edges run through shared helpers the page cites.
- **Movement — CLIENT and SERVICE (226 edges).** 138 inbound (Movement bodies `00326D60`, `00326BB0`, `0033C310` call page-cited `00203170`, `Actor_GetWorldPosition` (00265020), `PartyFocus_GetCurrentPackedActorHandle` (003590D0)); 88 outbound (page-cited `PartyFollow_SolveFormation` (00338490), `0033C310`, `BattleLocomotion_QueryDynamicActorObstruction` (003357B0) call Movement bodies `0031ABE0`, `00313F80`, `002EA7F0`). Read (2026-09-30, SWE2-CONTRACT): most of these edges are the accessor hubs this page documents (`00203170`, `Actor_GetWorldPosition` (00265020), `PartyFocus_GetCurrentPackedActorHandle` (003590D0), `ActorWork_GetBattleUnitRaw` (00263E30)), MECHANICAL. The relationship is the battle-area pair: `BattleSystem_InitializeAreaState` (002342F0) takes the world bounds from `Navigation_GetWorldBoundsXZ` (00383740) at `002343B5`, passes a bounds-derived float to `003924B0` at `0023441E`, then resets Movement state through `0031BD60`, `00327360` and `0033A380`; the teardown `002341C0` clears the navigation dataset (`Navigation_ClearDataset` (00383A20), `002341C9`) and calls `00392710` and `0031BD60`. Substantive edges include `BattleSystem_InitializeAreaState` (002342F0) calls `Navigation_GetWorldBoundsXZ` (00383740); `002342F0` calls `003924B0`; `002341C0` calls `Navigation_ClearDataset` (00383A20); `002341C0` calls `0031BD60`; the remaining edges run through shared helpers the page cites.
- **Party — CLIENT and SERVICE (63 edges).** 42 inbound (Party bodies `PartyFocus_SelectAndRequestDefaultActor` (00326500), `PartyConfiguration_ReconcileRosterFromCurrentSelectors` (003261D0), `PartyConfiguration_SetSelectorsAndReconcileRoster` (003273D0) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `PartyFocus_GetCurrentPackedActorHandle` (003590D0), `ActorHandle_EncodeRegistryEntry` (003589B0)); 21 outbound (page-cited `003091C0`, `0031ADB0`, `00329220` call Party bodies `PartyFocus_GetCurrentPackedActorHandle` (003590D0), `BattleUnit_GetPartyLeader` (003272A0), `BattleUnit_ResolveByFocusHandle` (0031B7E0)). Substantive edges include `BattleUnit_GetSlotCount` (00236850) is called by `PartyConfiguration_SetSelectorsAndReconcileRoster` (003273D0); `003091C0` calls `PartyRoster_GetActorBySlot` (0031ABF0); `003091C0` calls `003272F0`; `FieldData_GetActiveFieldRecordBit15` (00313F60) is called by `PartyControl_RecomputeSuppressionFromLeaderBattleState` (0023B040); the remaining edges run through shared helpers the page cites.
- **Platform — CLIENT (1 edge).** 1 inbound (Platform bodies `006253D0` call page-cited `0065E5D0`). Substantive edges include `0065E5D0` is called by `006253D0`.
- **PlatformOnlineAchievements — CLIENT (4 edges).** 4 inbound (PlatformOnlineAchievements bodies `003160C0`, `00315E90` call page-cited `00264790`, `BattleEncodedId_DispatchQueryMode0Value` (00309EC0), `WorldTransition_GetActiveOrPendingFieldId` (003148F0)). Substantive edges include `00264790` is called by `003160C0`; `BattleEncodedId_DispatchQueryMode0Value` (00309EC0) is called by `00315E90`; `003160C0` is called by `00315E90`; the remaining edges run through shared helpers the page cites.
- **Rewards_Progression_Economy — CLIENT and SERVICE (13 edges).** 10 inbound (Rewards_Progression_Economy bodies `BattleUnit_ProcessDefeatRewardsAndLoot` (00312280), `Reward_ComputeExperienceForRecipient` (002F8BB0), `Reward_ComputeLicensePointsForRecipient` (002F90C0) call page-cited `Actor_GetWorldPosition` (00265020), `BattleStats_FindOwningBattleUnit` (0031B860), `BattleStats_GetByMappedBattleSlot` (00320AB0)); 3 outbound (page-cited `002341C0`, `BattleSystem_InitializeAreaState` (002342F0), `00329220` call Rewards_Progression_Economy bodies `Loot_InitializeWorldPickupPool` (00319B10), `002F8F20`). Substantive edges include `002341C0` calls `Loot_InitializeWorldPickupPool` (00319B10); `BattleSystem_InitializeAreaState` (002342F0) calls `Loot_InitializeWorldPickupPool` (00319B10); `00264150` is called by `Reward_ComputeLicensePointsForRecipient` (002F90C0); `00329220` calls `002F8F20`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT and SERVICE (243 edges).** 226 inbound (Script_VM_Native_Bridge bodies `0034B5D0`, `0034BB80`, `003516E0` call page-cited `00263F10`, `00264010`, `Actor_GetWorldPosition` (00265020)); 17 outbound (page-cited `WorldActorScriptVM_InterpretBytecode` (0025E4C0) call Script_VM_Native_Bridge bodies `VMValueStack_PopInt32CoerceFloat32` (00267E10), `ScriptVM_WaitList_HasAnyActorChannelActive` (00267420), `ScriptVM_WaitList_HasAnyActorResourceEntryActive` (002674B0)). Substantive edges include `00203170` is called by `00356160`; `WorldActorScriptVM_InterpretBytecode` (0025E4C0) calls `ScriptVM_WaitList_HasAnyActorChannelActive` (00267420); `WorldActorScriptVM_InterpretBytecode` (0025E4C0) calls `ScriptVM_WaitList_HasAnyActorResourceEntryActive` (002674B0); `WorldActorScriptVM_InterpretBytecode` (0025E4C0) calls `ScriptVM_SubmitActorRuntimeRequest` (00268850); the remaining edges run through shared helpers the page cites.
- **Spawn_Encounter_Lifecycle — CLIENT and SERVICE (10 edges).** 8 inbound (Spawn_Encounter_Lifecycle bodies `Spawn_CountActiveCapTrackedActors` (00308D90), `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0), `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0) call page-cited `Actor_GetWorldPosition` (00265020), `FieldData_GetActiveFieldRecordBit15` (00313F60), `BattleUnit_GetBySlotIndex` (00236820)); 2 outbound (page-cited `BattleSystem_InitializeAreaState` (002342F0) call Spawn_Encounter_Lifecycle bodies `SpawnKeep_RotatePersistenceBanksForAreaTransition` (00233780), `SpawnGroup_ResetLifecycleLedger` (00307090)). Substantive edges include `BattleSystem_InitializeAreaState` (002342F0) calls `SpawnKeep_RotatePersistenceBanksForAreaTransition` (00233780); `BattleSystem_InitializeAreaState` (002342F0) calls `SpawnGroup_ResetLifecycleLedger` (00307090); `BattleUnit_GetSlotCount` (00236850) is called by `Spawn_CountActiveCapTrackedActors` (00308D90); `FieldData_GetActiveFieldRecordBit15` (00313F60) is called by `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0); the remaining edges run through shared helpers the page cites.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-cross-subsystem-accessor-hubs-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002EAA10` | 30 B | returns 0 when `rcx` is null, when qword `+0xC0` of `rcx` is null, or when the dword at that pointer is negative; otherwise tail-jumps `003B50E0` with that dword in `ecx` (`jns`) | `002EAA15`, `002EAA21`, `002EAA25`, `002EAA2B` |
| `0034B5D0` | 64 B | chains `00267E10(r9)` into `00264010`, its result into `00263F10`, that into `003589B0`, and that into `00320790(result, 0)`, then tail-jumps `0026B4E0` with the incoming `rcx` and the `00320790` result as `edx` | `0034B5DC`, `0034B5E3`, `0034B5F3`, `0034B5FC`, `0034B60B` |
| `00466BF0` | 75 B | returns 0.0 unless the dword `02EBB6E4` is non-negative and less than (signed) dword `02EBB6E0` and qword `+0x8` of the `0x50`-byte entry at qword `02EBB6F0` plus that index times `0x50` is non-zero; then returns 0.01 (`008F30E4`) times the float at the qword `+0xA8` of the entry's qword `+0x28`, or 0.0 when that `+0xA8` pointer is null | `00466BFE`, `00466C0C`, `00466C17`, `00466C2E`, `00466C32` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-cross-subsystem-accessor-hubs-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00240A60` | 100 B | for the object at qword `[[rdx+0x10]]` stores `002F9860(dword at 00914C60 + r9d*8)` (signed index) at qword `+0x18` and `0020E620(0)` at dword `+0x20`; does the same for the object at qword `[[rdx+0x10]+8]` with `002F9860(0x53d)`; returns 1 | Interior anchor `00240A7E`; Interior anchor `00240A81`; Interior anchor `00240A88`; Interior anchor `00240AA1`; Interior anchor `00240AB4` |
| `002637D0` | 54 B | calls `002E97B0` with the incoming registers and returns the incoming `edx` when the result is null, its dword `+0` is -1, or bit 0 of its byte `+0x29` is clear; otherwise returns bit 1 of that byte | Interior anchor `002637D8`; Interior anchor `002637E2`; Interior anchor `002637EE`; Interior anchor `002637F5` |
| `00269F60` | 44 B | calls `002E97B0` with the incoming registers and, when the result is non-null and its dword `+0` is not -1, tail-jumps (at `00269F60`+0x21) with the result's word `+0` as `ecx` and the incoming `edx`; otherwise returns the `002E97B0` result unchanged | Interior anchor `00269F68`; Interior anchor `00269F72`; Interior anchor `00269F77`; Interior anchor `00269F81` |
| `002CA6C0` | 255 B | switches on dword `[rdx]`: 4 returns 0; 2 calls `002CA6C0`+0x3A with `rcx`, then clears bit 0 of dword `+0x50` when dword `+0x168` of qword `+0x108` has bit `0x10000`, else sets it, and returns 0; 1 calls `002432B0(rcx+0x50, qword +0x38 of qword 0209AC30, 6, rcx)`, copies the result's words `+4`, `+6`, `+8`, `+0xa` to `+0x98`, `+0x9a`, `+0x9c`, `+0x9e` when `rcx` is non-null, stores dword `[rdx+8]` at `+0xd4` and qword `[rdx+0x10]` at `+0x108`, clears bit 0 of `+0x50` when that qword's dword `+0x168` has bit `0x10000`, and returns 0; any other value tail-jumps at `002CA6C0`+0x32 with `rcx` | Interior anchor `002CA6D5`; Interior anchor `002CA712`; Interior anchor `002CA723`; Interior anchor `002CA751`; Interior anchor `002CA78C` |
| `002CB150` | 156 B | when dword `[rdx]` is not 1 tail-jumps (at `002CB150`+0x13) with `rcx`; otherwise calls `002432B0(rcx+0x50, qword +0x38 of qword 0209AC30, 8, rcx)`, copies the result's words `+4`, `+6`, `+8`, `+0xa` to `+0x98`, `+0x9a`, `+0x9c`, `+0x9e` when `rcx` is non-null, clears bit 0 of dword `+8` in the objects at qwords `+0` and `+8` of the table at qword `rcx+0x60`, clears bit `0x800` of dword `rcx+0x40` and returns 0 | Interior anchor `002CB156`; Interior anchor `002CB180`; Interior anchor `002CB19E`; Interior anchor `002CB1C8`; Interior anchor `002CB1DD` |
| `002D5E00` | 161 B | when dword `[rdx]` is not 1 tail-jumps (at `002D5E00`+0x13) with `rcx`; otherwise calls `002432B0(rcx+0x50, qword +0x18 of qword 0209AC30, 1, rcx)`, ORs `0x8000000` into dword `+0x20` of the object at qword `[[rcx+0x60]]`, copies the result's words `+4`, `+6`, `+8`, `+0xa` to `+0x98`, `+0x9a`, `+0x9c`, `+0x9e` when `rcx` is non-null, passes the result of the call at `002D5E00`+0x89 (with 5) as `rdx` to the call at `002D5E00`+0x94 with `rcx`, and returns 0 | Interior anchor `002D5E30`; Interior anchor `002D5E48`; Interior anchor `002D5E66`; Interior anchor `002D5E89`; Interior anchor `002D5E94` |
| `00347580` | 67 B | calls `00264010(00267E10(r9))`, passes that to `00265020` with three stack out-slots as `rdx`, `r8`, `r9`, then calls `00347580`+0x38 with the incoming `rcx` and the float written through the `rdx` slot in `xmm1` | Interior anchor `0034758C`; Interior anchor `00347593`; Interior anchor `003475AA`; Interior anchor `003475AF`; Interior anchor `003475B8` |
| `00347600` | 81 B | calls `00267E10(r9)` three times, passes the third value to `00264010`, and tail-jumps (at `00347600`+0x4C) with that result, the second value as `edx` and the first as `r8d` | Interior anchor `00347615`; Interior anchor `0034761F`; Interior anchor `00347629`; Interior anchor `00347630`; Interior anchor `0034764C` |
| `00347AB0` | 67 B | calls `00264010(00267E10(r9))`, passes that to `00265020` with three stack out-slots as `rdx`, `r8`, `r9`, then calls `00347AB0`+0x38 with the incoming `rcx` and the float written through the `r8` slot in `xmm1` | Interior anchor `00347ABC`; Interior anchor `00347AC3`; Interior anchor `00347ADA`; Interior anchor `00347ADF`; Interior anchor `00347AE8` |
| `00347BE0` | 81 B | calls `00267E10(r9)` three times, passes the third value to `00264010`, and tail-jumps (at `00347BE0`+0x4C) with that result, the second value as `edx` and the first as `r8d` | Interior anchor `00347BF5`; Interior anchor `00347BFF`; Interior anchor `00347C09`; Interior anchor `00347C10`; Interior anchor `00347C2C` |
| `00347FF0` | 67 B | calls `00264010(00267E10(r9))`, passes that to `00265020` with three stack out-slots as `rdx`, `r8`, `r9`, then calls `00347FF0`+0x38 with the incoming `rcx` and the float written through the `r9` slot in `xmm1` | Interior anchor `00347FFC`; Interior anchor `00348003`; Interior anchor `0034801A`; Interior anchor `0034801F`; Interior anchor `00348028` |
| `00348800` | 55 B | passes `00263F10(00264010(00267E10(r9)))` to the call at `00348800`+0x23 and tail-jumps to `0026B4E0` with the incoming `rcx` and that call's result as `edx` | Interior anchor `0034880C`; Interior anchor `00348813`; Interior anchor `0034881B`; Interior anchor `00348823`; Interior anchor `00348832` |
| `00349490` | 48 B | passes `00264010(00267E10(r9))` to the call at `00349490`+0x1B and tail-jumps (at `00349490`+0x2B) with the incoming `rcx` and that call's float result moved into `xmm1` | Interior anchor `0034949C`; Interior anchor `003494A3`; Interior anchor `003494AB`; Interior anchor `003494B0`; Interior anchor `003494BB` |
| `0034AAD0` | 74 B | calls `00267E10(r9)` and `00263F10(rdx)`, passes that result and the `00267E10` value as `edx` to the call at `0034AAD0`+0x2C, and tail-jumps to `0026B4E0` with the incoming `rcx` and that call's result as `edx` | Interior anchor `0034AAE8`; Interior anchor `0034AAF2`; Interior anchor `0034AAFC`; Interior anchor `0034AB15` |
| `0034B060` | 55 B | passes `00263F10(00264010(00267E10(r9)))` to the call at `0034B060`+0x23 and tail-jumps to `0026B4E0` with the incoming `rcx` and that call's result as `edx` | Interior anchor `0034B06C`; Interior anchor `0034B073`; Interior anchor `0034B07B`; Interior anchor `0034B083`; Interior anchor `0034B092` |
| `0034C1D0` | 55 B | passes `00263F10(00264010(00267E10(r9)))` to the call at `0034C1D0`+0x23 and tail-jumps to `0026B4E0` with the incoming `rcx` and that call's result as `edx` | Interior anchor `0034C1DC`; Interior anchor `0034C1E3`; Interior anchor `0034C1EB`; Interior anchor `0034C1F3`; Interior anchor `0034C202` |
| `0034C500` | 74 B | calls `00267E10(r9)`, then the call at `0034C500`+0x17, passes its result and the `00267E10` value to `00358940`, passes that through `00263F10` to the call at `0034C500`+0x31, and tail-jumps to `0026B4E0` with the incoming `rcx` and that call's result as `edx` | Interior anchor `0034C510`; Interior anchor `0034C521`; Interior anchor `0034C529`; Interior anchor `0034C531`; Interior anchor `0034C545` |
| `0034C6A0` | 96 B | calls `00267E10(r9)` twice, passes the second value through `00264010` and `00263F10`, calls `0034C6A0`+0x42 with that result and the first value clamped to 0 when negative, and tail-jumps to `0026B4E0` with the incoming `rcx` and that call's result as `edx` | Interior anchor `0034C6C9`; Interior anchor `0034C6D1`; Interior anchor `0034C6DA`; Interior anchor `0034C6E2`; Interior anchor `0034C6FB` |
| `0034CC60` | 74 B | calls `00267E10(r9)`, then the call at `0034CC60`+0x17, passes its result and the `00267E10` value to `00358940`, passes that through `00263F10` to the call at `0034CC60`+0x31, and tail-jumps to `0026B4E0` with the incoming `rcx` and that call's result as `edx` | Interior anchor `0034CC70`; Interior anchor `0034CC81`; Interior anchor `0034CC89`; Interior anchor `0034CC91`; Interior anchor `0034CCA5` |
| `0034DA30` | 75 B | calls `00263F10(rdx)` and `00267E10(r9)`, passes both (the latter as `edx`) to the call at `0034DA30`+0x2D, and tail-jumps to `0026B4E0` with the incoming `rcx` and that call's result as `edx` | Interior anchor `0034DA48`; Interior anchor `0034DA53`; Interior anchor `0034DA5D`; Interior anchor `0034DA76` |
| `0034E190` | 89 B | calls `00267E10(r9)` twice, passes the second value through `00264010` and `00263F10`, calls `0034E190`+0x3B with that result and the first value as `edx`, and tail-jumps to `0026B4E0` with the incoming `rcx` and that call's result as `edx` | Interior anchor `0034E1A8`; Interior anchor `0034E1B9`; Interior anchor `0034E1C1`; Interior anchor `0034E1CB`; Interior anchor `0034E1E4` |
| `00351EE0` | 37 B | stores `00264010(00267E10(r9))` as a qword at `[r8]` and tail-jumps at `00351EE0`+0x20 | Interior anchor `00351EEC`; Interior anchor `00351EF3`; Interior anchor `00351EF8`; Interior anchor `00351F00` |
| `00352270` | 79 B | calls `00267E10(r9)` and `003589B0(00263F10(rdx))`, then tail-jumps with the `00267E10` value as `ecx` and the `003589B0` result as `edx`: at `00352270`+0x3B when byte `rdx+0x15` is 3, else at `00352270`+0x4A | Interior anchor `00352280`; Interior anchor `0035228A`; Interior anchor `00352292`; Interior anchor `00352297`; Interior anchor `0035229F` |
| `00352940` | 58 B | calls `00267E10(r9)` and `003589B0(00263F10(rdx))`, then tail-jumps (at `00352940`+0x35) with the `00267E10` value as `ecx` and the `003589B0` result as `edx` | Interior anchor `00352950`; Interior anchor `0035295A`; Interior anchor `00352962`; Interior anchor `00352975` |
| `003C9840` | 86 B | returns when qword `rcx+0xc8` is 0; otherwise calls `003C5FB0(rcx)`, calls `003C9840`+0x29 with `rcx` and 2 when that returned non-zero, else 1, and, when qword `+0xc8` is still non-null, copies the returned record's word `+0xc` to that object's word `+0x98` and its word `+0xe` to `+0x9a` | Interior anchor `003C9846`; Interior anchor `003C9853`; Interior anchor `003C9862`; Interior anchor `003C9869`; Interior anchor `003C9882` |
| `003FC3F0` | 283 B | switches on dword `[rdx]`: 15 stores word 1 at `+0xc2`; 2 does nothing when word `+0xc2` is non-zero, else, when the sign-extended word `+0xc0` is below dword `01DFE0B4` times `0x3c` (unsigned compare), increments it by one (no loop), and otherwise calls `00244F00(rcx)`; 1 passes the result of `003FC3F0`+0x8C to `002432B0(rcx+0x50, result, 2, rcx)`, calls `003FC3F0`+0xB1 and, when `rcx` is non-null, stores the record's word `+4` at `+0x98`, that call's result plus `0xc` minus word `+0xa` at `+0x9a`, word `+8` at `+0x9c` and word `+0xa` at `+0x9e`, then calls `003FC3F0`+0xF2 with (`rcx`, `00D11FF0`) and `003FC3F0`+0xFF with (`rcx`, `0x58`); these cases return 0, and any other value tail-jumps at `003FC3F0`+0x22 with `rcx` | Interior anchor `003FC41C`; Interior anchor `003FC447`; Interior anchor `003FC45E`; Interior anchor `003FC491`; Interior anchor `003FC4C3` |
| `0050E3A0` | 101 B | calls `002E97B0(rdx)` and `00267E10(r9)`; when the first result is null tail-jumps (at `0050E3A0`+0x60) with `00D22A18` in `rcx`, otherwise sets bit 12 of the `00267E10` value and tail-jumps (at `0050E3A0`+0x45) with the incoming `rdx` as `rcx` and that value as `edx` | Interior anchor `0050E3B8`; Interior anchor `0050E3C3`; Interior anchor `0050E3CB`; Interior anchor `0050E3CD`; Interior anchor `0050E3E5` |
| `0057FA30` | 197 B | calls `0057FA30`+0x12 with (`rcx`, 0); in the qword table at `rcx+0x10` clears bit 0 of dword `+8` in entry `+0xd8`, sets it in entry `+0xb0` and in the 7 entries indexed by the bytes at `00D23EAC` (index times 8), then clears it in entry `+0xd0`; then by dword `[r8]` (3, 4, 5) stores `002F9860(0x874)`, `002F9860(0x873)` or `002F9860(0x872)`, or `01CEB638` for any other value, at qword `+0x18` of entry `+0xb0` and `0020E620(0)` at its dword `+0x20` | Interior anchor `0057FA59`; Interior anchor `0057FA83`; Interior anchor `0057FA87`; Interior anchor `0057FAC9`; Interior anchor `0057FADC` |
