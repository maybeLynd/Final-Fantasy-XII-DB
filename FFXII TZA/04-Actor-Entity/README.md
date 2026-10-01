# Actor / Entity

**Engine category.** Actor identity, the actor registry, ActorManager records, and runtime entity lists.

| | |
|---|---|
| Classification source | PrimaryOwner: ActorEntity |
| Functions | 235 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`battleunit-slot-pool-and-actor-class.md`](battleunit-slot-pool-and-actor-class.md) —
  **DOCUMENTED, tier 1.** The fixed BattleUnit pool (3,920 bytes per slot, linear first-free
  allocation, **silent failure when full**) and the three-bit actor class that decides whether
  something can be moved (class 3) or merely positioned (class 1).

Known anchor: ActorManager records have stride `0x288`, manager index at `+0x28`, status bits at `+0x10`. Index 0 is the primary manager and is the only one that runs the field-runtime weather/resource initialization core (`002620E0`).

- [`Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md`](Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) —
  **DOCUMENTED, tier 1.** One installer, two authored tables, one `0x1C8` stats record with two
  homes: the definition id's class byte selects the party table and a battle-state element, or the
  enemy table and a spawn record's `+0x80` page. Every field written is cited, including the steal
  bits, the per-area spawn-history counter, and a character's starting equipment, licences, level
  and gambit preset. Resolves `OPUS-CONTRA-BU698`.

- [`Battle-Unit/the-battle-unit-field-map.md`](Battle-Unit/the-battle-unit-field-map.md) —
  **DOCUMENTED, tier 1.** The 3,920-byte battle unit, offset by offset, from a typed field scan
  seeded by the pool and the three unit-returning accessors: 144 offsets across 310 functions with
  writers and readers, the names the store and the pages established, and the 45 ranges nothing
  enumerated reaches. The access table is published beside it.

- [`Actor-Manager-Record/the-actor-manager-record-field-map.md`](Actor-Manager-Record/the-actor-manager-record-field-map.md) —
  **DOCUMENTED, tier 1.** The 648-byte manager record, five slots at `02098E10`, from two
  controlled routes plus the bind: 57 touched offsets with writers and readers, the tick's two
  bytes, the bind's pointer block — and the type `OPUS-CONTRA-REC60` was really about.

- [`Actor-Storage-Record/the-actor-storage-record-field-map.md`](Actor-Storage-Record/the-actor-storage-record-field-map.md) —
  **DOCUMENTED, tier 1.** A companion to the record page: 81 touched offsets from 272 functions
  with writers and readers per byte, the store's names where they exist, and the 31 untouched
  bytes; the access table beside it.

- [`Unit-Display-Record/the-record-00329220-builds.md`](Unit-Display-Record/the-record-00329220-builds.md) —
  **DOCUMENTED, tier 1.** The party member status view: the 0xC0-byte snapshot `00329220` builds
  per call for the UI from a party stats record, its unit and its row — every displayed number with
  its source, the eighteen flag bits, the 20-unit "out of range" circle, the points to the next level.

- [`Actor-Names/the-npc-name-dictionary.md`](Actor-Names/the-npc-name-dictionary.md) — `npcdic.bin`: 1,141 name pairs, the actor's `+0x102` id, and the persistent flag with the same number that swaps in the second name (247 pairs differ).
- [`Actor-Contexts/the-movement-and-secondary-context-censuses.md`](Actor-Contexts/the-movement-and-secondary-context-censuses.md) —
  **PARTIAL, tier 1.** The two regions every actor record reaches only through pointers — the
  movement context (0x230 at `+0x120`) and the secondary context (0x188 at `+0x350`) — censused
  through the pointers: 313 and 302 accesses at 58 and 40 offsets, the position as three floats at
  the front of the first, and a third pointer at `+0xA0` found beside them. The layouts are the
  store's to declare.

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Audio — SERVICE.** `002620E0` on this page calls `FUN_00363b40`, owned by that layer. What it reaches is a 768-byte area-music selector: it collects the non-zero track ids out of the table at `[022CBAF8]`, de-duplicates them into the scratch list at `022CBB58` with the count at `[022CBB70]`, and then either starts the chosen id outright or crossfades to it over `0xF` steps, falling back to the id `0xB4` when the table is absent; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — SERVICE.** `00329220` on this page calls `BattleRuntime_GetEffectiveActionId`, owned by that layer. What it reaches is a 149-byte action-id resolution: a record with `byte[+5] == 0` indexes the `0x40`-byte rows at `0208D480` by `byte[+4]`, anything else resolves its owning unit and indexes the rows at `0208DE80` by `byte[+0xEA9]`, and the row's `word[+0x10]` is substituted only when the unit's current `word[+0x714]` is `0x9F`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — SERVICE.** `002620E0` on this page calls `FUN_00259b30`, owned by that layer. What it reaches is a 699-byte reset of two `0x860`-byte presentation slots based at `02098378`: each slot's `0x630`-byte body and its three `0xB0`-byte sub-blocks are zeroed and re-seeded from one transform, with the `+0x1F8` scale set to 1.0; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — SERVICE.** `00329220` on this page calls `FUN_002f8f20`, owned by that layer. What it reaches is a bounded id mapping: zero returns zero and ids outside `1..0x62` take the out-of-range path; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Save_Load_Settings — SERVICE.** `002620E0` on this page calls `SaveImage_GetPersistentPayloadBase`, owned by that layer. What it reaches is a 20-byte accessor returning `002EF640() + 0x200` - **the base the persistent flag banks are indexed off**, so those banks live inside the save payload; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatAction — SERVICE (1 edge).** The display-record builder `00329220` calls `003879C0`. That 140-byte test answers bit 7 of byte `+0x12` of the unit's `.ard` slot-0 class row, for an owner whose stats kind byte `+5` is 1, and the builder stores the answer as the record's flag bit 16.

**Items_Equipment_Shops_License — SERVICE (1 edge).** `00329220` calls `BattleStats_CountLicenseBits00To17` `00324020`. The builder stores that licence-bit count at the record's `+0xBB` in its `full` arm, as the display-record page shows.

**Party — SERVICE (2 edges).** `00329220` calls `PartyRoster_GetActorBySlot` `00263750` and `PartyFocus_GetCurrentPackedActorHandle` `003590D0`. The builder encodes the member slot's actor handle into `+0x04` and, when the focus bit is set, picks the focus unit; both come from the party layer's roster and focus state.

**WorldAreaField — SERVICE and CLIENT (6 edges).** The field-runtime initialisation core `002620E0` calls the weather roll `0025ACA0` and `00379290`, the weather chain's step into Movement; `00329220` calls the field predicate thunk `FieldData_GetActiveFieldRecordBit15` `00313F60`; and the save-image buffer getter `002EF640` is called by `WorldTransitionSnapshot_CaptureRuntimeState`, `WorldTransition_StageFieldTransition` and `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot`. Manager 0's initialisation runs the area's weather roll and its hand-off, the display record's "no terminal status" bit asks the field predicate, and the field-transition snapshot code reads and restores state through the same save-image buffer whose `+0x200` holds the persistent flag banks.
