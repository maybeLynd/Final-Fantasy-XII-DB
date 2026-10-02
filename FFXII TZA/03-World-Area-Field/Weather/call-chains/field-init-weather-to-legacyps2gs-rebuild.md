---
system: "Call chain: field initialization -> Weather -> Legacy PS2 GS rebuild"
category: 03-World-Area-Field
status: DOCUMENTED
owner_layer: crosses five owners - ActorEntity, WorldAreaField, Movement, ScriptVM, Presentation
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  previous_parent: none - this document carried no provenance stamp at all
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: reverification-against-current-parent
  crossref_clean: true
  reopened_count: 1
---

# Call chain: field initialization -> Weather -> Legacy PS2 GS rebuild

The longest fully-proven cross-subsystem chain in the database. It crosses **five** owner
boundaries without any of them inheriting ownership from another.

## The chain

```
[ActorEntity]        0025D9E0  ActorManager_RunFieldRuntimePass
                       |
                       v
[ActorEntity]        002620E0  field-runtime init core
                       |         gate: managerRecord+0x28 == 0  (primary manager)
                       |         gate: managerRecord+0x10 & 0x04 clear (one-shot)
                       v
[WorldAreaField]     0025ACA0  RollAndApplyWeatherSlotTransition
                       |-> 002658B0  authored EBP weatherProbability (script header +0x64)
                       |-> MT19937   gameplay RNG
                       |-> 0025ABA0  alternate eligible slot
                       v  (tail jump)
[WorldAreaField]     0026D910  ApplyWeatherSlotAndDerivedEnvironmentState
                       |-> payload+0x1060 commit (or preserve, per +0x1061)
                       |-> MWeather preset -> 02099DAC        [reaches CombatFormula]
                       |-> global environment class -> 02099DA8
                       |-> 002E3D40 -> 0040AAD0               [reaches Presentation]
                       v
[ActorEntity]        002620E0  continues
                       |-> 00265920  re-read committed slot
                       |-> publish to notification channel 0   <- corrected 2026-10-02, OPUS: EFB binding channel 0 - 0026FAD0 -> 0026F470 builds the rows whose channel byte +4 is 0 (0026F534)
                       |-> publish to notification channel 0x1F   <- corrected 2026-10-02, OPUS: EFB binding channel 0x1F, as above
                       |-> 00379860(weatherSlot)
                       v
[WorldAreaField]     00379290  field-resource bridge
                       |         if area runtime exists: 02ADD0E9 = 1, tail 0026E8D0(slot)
                       |         else:                   02ADD0E9 = 0, tail 00379630
                       v
[Movement]           0026E8D0  resource-bank reconfiguration     [AUTHORITY 03 -> 06]
                       |-> sets dirty state
                       v
[Movement]           0026E290  observes dirty
                       v
[Presentation]       002F7380  LegacyPS2GS texture-mip budget + slot-table rebuild
                       |-> 00466190 -> 003A1E50   GS page geometry
                       |-> 00467AA0               4 MiB arena, 8 KiB pages
                       |-> allocate count*40 slot table
```

## Owner boundaries crossed

| Step | Owner | Note |
|---|---|---|
| `0025D9E0`, `002620E0` | ActorEntity | runs the transaction, does not own weather |
| `0025ACA0`, `0026D910`, `00379290` | WorldAreaField | owns the weather decision and apply |
| `0026E8D0`, `0026E290` | Movement | owns the resource/dirty transaction |
| `002F7380` | Presentation *(proposed)* | owns the GS dataset mechanism |

**Nothing inherits ownership from its caller.** This chain is the reason the PrimaryOwner /
CodeDomain split exists.

## The split that matters

There are **two** weather paths, and they are not the same transaction:

**Field initialization** (above) - fans the committed slot out into resource/environment
channels, reaches Movement, and rebuilds the LegacyPS2GS table.

**Runtime scripted `setweatherslot`**:
```
0x021A setweatherslot(int)
  -> 003565C0  ScriptVM handler
     -> 0026D910(slot)     apply + MapRef/environment + Presentation refresh
     -> 0026D8F0()         arm bInitializationRestoreState
     -> return
```
There is **no** direct call from here to `00379290`, `00379630`, `0026E8D0`, `0026E290` or
`002F7380`. A runtime weather change does **not** rebuild the Movement/GS resource banks.

## Consequences

- **Modding:** do not force the field-init resource rebuild after a runtime weather change.
  The base game does not, and doing so is less native-coherent than vanilla.
- **XIIOnline late join:** authoritative area identity -> authoritative Weather Slot ->
  native WorldAreaField reconciliation -> field-resource init -> Movement binds the slot ->
  Presentation/LegacyPS2GS rebuild locally -> *only then* is weather-dependent spawn
  eligibility valid.
- **Already-loaded client receiving a weather change:** apply the runtime path only. Let
  native consequences follow. Do not manufacture a field-resource rebuild.

## Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Full field-init sequence | complete body of `002620E0` (231 B, `7605a770...182f`) | 1 |
| `00379290` has exactly one caller | complete direct-call census: `002620E0 -> 00379290` only | 1 |
| Both bridge branches feed `0026E8D0(slot)` | complete bodies of `00379290` (53 B, `3ffc8192...eba6`) and `00379630` | 1 |
| Runtime path does not reach the rebuild | complete body of `003565C0` (99 B, `5819ab38...aa9a`); no direct call to any rebuild function | 1 |
| Movement owns the trigger, not the callee | sealed V120 Movement exit-gate evidence | 1 |

## Re-verification 2026-09-02 (AH-5)

This document carried **no provenance stamp at all** - no parent GZF, no EXE hash - which
`check_provenance.py` flagged on its first run. All **20** cited addresses were checked against the
current parent:

**20 of 20 resolve as function entries.** No ghost addresses.

The owner spread confirms the document's headline claim of five owner boundaries:

| Owner | Functions cited |
|---|---|
| ActorEntity | `0025D9E0` |
| WorldAreaField | `0025ABA0`, `0025ACA0`, `002658B0`, `0026D910`, `00379290` |
| Movement | `0026E290`, `0026E8D0` |
| Script VM / Native Bridge | `003565C0` |
| Presentation | `0040AAD0`, `00467AA0` |

Nine further cited functions are unowned in the current parent, which is consistent with the
database's residual: unowned does not mean unresolved.

**Stamp added because the addresses were checked**, not to satisfy the checker. `previous_parent`
records that there was none.

One note for the record: this document already contained `payload+0x1060 commit (or preserve, per
+0x1061)`. A same-day claim in the sibling weather-roll document that the payload link was found
independently by two documents that did not know of each other was **wrong**, and has been corrected
there - this document had it first.

## Cross-subsystem neighbours — disposition (audit pass, repos-2d, 2026-09-03)

The neighbours `audit_crossrefs.py` reports for this document are the Weather system's shared
field-frame neighbourhood, seen from this document's angle. **The census is stated once**, in
[../weather-apply-and-environment-materialization.md](../weather-apply-and-environment-materialization.md)
§ *Cross-subsystem neighbours*, rather than repeated in each of the six Weather documents:

- **Core runtime scheduling** — `ImageAddress_ResolveRuntimePointer` (815 callers, 18 owners), the
  convention every authored table in this engine is addressed through. Runtime infrastructure.
- **Audio** and **Party** — callees of the field-frame routines `ActorManager_RunFieldRuntimePass`
  and two small field routines, cited here for their Weather role. A frame pass that drives audio
  and asks who the party focus is, is doing its own job.
- **RNG/random selection** — `RNG_MT19937_NextU32_Thunk`. Not unaccounted: it is the Weather
  transition roll, documented under the engine's own algorithm name, **MT19937**.
- **Gameplay - SERVICE (1 edge).** `0025D9E0` reaches bodies filed to Gameplay: `00234150` (CombatAction) - shared machinery across the layer boundary, no shared ownership.
- **Movement - SERVICE (14 edges).** `0025D9E0`, `0026E8D0` reach bodies filed to movement: `0025DF00`, `003ECFD0`, `003ED020` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (41 edges).** `001A9930` is also called by bodies filed to presentation: `00180650` (Rendering), `001ACF80` (Rendering), `001BF8B0` (Rendering) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (7 edges).** `00265920`, `0026D8F0`, `0026D910` are also called by bodies filed to script VM / native bridge: `00356250`, `0050D360`, `003565C0` - shared machinery across the layer boundary, no shared ownership.

## `002F7380` opened — 2026-09-03, session `repos-78`

This document cited `002F7380` **at its entry only**, as did nine others; it was the top entry on the
*located, never opened* cut by citation count. It is opened here. **Nothing above is retracted** — this
adds a body to a function the chain already named.

**Extent verified before reading**, because this executable's decompiled output can render a tail
call as part of the caller's body. Disassembled from the image: 177 instructions, **ends `ret` at
`002F7652`, no `jmp` leaves the extent.** The hazard does not apply here.

### What it is: a count → select → allocate pass over field records

```asm
002F738E  mov  ecx, dword ptr [0209A6E8]
002F7394  add  ecx, 0x17
002F7397  shl  eax, cl                        ; mask = 1 << (global + 23)
```

**One global picks a bit position, and the resulting single-bit mask is tested against a flags dword
on each entry** (`test dword ptr [r9 - 0x11], esi`). Entries whose bit is clear take no part in what
follows. That is a variant/permission selector driven from a single global.

The body is three passes over two arrays:

| array | base | count | stride |
|---|---|---|---|
| records | `[[rdi+0x150] + 8]` | `[rdi+0x224]` | **0x60** |
| entries | `[rdi+0x178]` | `[rdi+0x174]` | **0x30** |

**Pass 1 — measure.** For each record: `00466190(rec, i)` yields a value tracked as a **maximum**;
`00466220(rec)` is a predicate selecting an increment of either ~~`i+1`~~ `1` *(corrected 2026-10-02, OPUS: `002F73D0 xor ecx, ecx`, `002F7416 lea ebp, [rcx+1]`, `002F744A mov edx, 4` / `002F744F cmovne edx, ebp`)* or `4`, accumulated into a
**sum**. *(Corrected 2026-09-14 (FABLE): the increment is **1**, not `i+1`. `ebp` is `lea [rcx + 1]` at `002F7416` with `rcx` zeroed at `002F73D0` and not changed before it; the loop counter is `r12d`. So the sum is 1 per 4-bit-indexed record plus 4 per other record, as UQ-90 below uses.)* Each record's `word +0x0E` is zeroed. The max and the sum are then handed to
`00467B10(max)`, `00467B00(sum)` and `00467AA0()`, the last returning a **budget**.

**Pass 2 — count references.** For each entry that passes the mask and a `0x3FFF` bound, the record
index is read, and that record's `word +0x0E` is incremented. The walk then continues **forward
through following records while their `word +0x0C` is non-zero**, incrementing each — so `+0x0C`
marks a continuation and a reference counts against a whole run, not one record.

**Pass 3 — select and number.** For each record with `word +0x0E > 1`, `00466190` is consulted again
and a running total compared against the budget; if it fits, the record is given the **next sequential
slot number** and `word +0x0E` is overwritten with it. Records that do not qualify get `-1`.

**Then the allocation:**

```asm
002F75CD  mov  dword ptr [rdi + 0x228], r15d   ; how many were selected
002F75C9  lea  edx, [r15 + r15*4] ; shl edx, 3 ; = r15 * 40 bytes
002F75DC  call 0x3ec8d0                        ; allocate
002F75E1  mov  qword ptr [rdi + 0x218], rax
002F7600  ...per entry: four qwords (+0x00/+0x08/+0x10/+0x18) and one byte (+0x20)
          = 33 of the 40; +0x21..+0x27 are NEVER written...
```

**`[rdi+0x218]` is an array of 40-byte entries, one per selected record, and `[rdi+0x228]` is its
count.**

> **Correction, 2026-09-15 (OPUS), `OPUS-ABI-SLOTRECORD-NOT-ZERO-INITIALISED`.** This sentence said
> *“zeroed on creation”* and the block comment above said *“zero all r15 entries”*. **Neither is
> true of the whole entry.** The loop at `002F7600`–`002F7628` writes exactly five stores per
> element — `002F760B`, `002F7610`, `002F7615`, `002F761A` as qwords and `002F761F` as a byte,
> with `r9` zeroed at `002F75F0`. Because `002F7607 lea rcx, [rcx+0x28]` advances from zero those
> land at `+0x00`, `+0x08`, `+0x10`, `+0x18` and `+0x20`: **33 of each entry's 40 bytes.**
> `+0x21`..`+0x27` are uninitialised allocator memory for the life of the table, and the table is
> reallocated on every rebuild. The allocation tag is `ecx = 6` (`002F75D7`).
> *(This page's `word +0x0E` was always right; it was
> [texture-mip-local-memory-budget.md](../../../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md)
> that called the field `s32`, and that page is the one corrected.)*

### What this fixes, and what it does not

Three things are now exact and were not before:

- **`word +0x0E` on a record is used for two different things in one function** — a reference counter
  in pass 2, then overwritten with a slot index in pass 3. **A reader arriving at pass 3 and calling
  it "the count" would be wrong**, and the two meanings are separated only by which pass is running.
- **`word +0x0C` marks a continuation**, so counting is per-run.
- **The selection rule is "referenced more than once, while the budget lasts."** Both halves are in
  the code: `cmp word ..., 1 / jle` and `cmp ecx, r12d / jge`.

**What it is *for* is only partly established.** All seven callees — `003EC8A0`, `00466190`,
`00466220`, `00467B10`, `00467B00`, `00467AA0`, `003EC8D0` — are still unnamed `FUN_` in the
ledger, but four of the questions that sentence bundled together have since moved and the rest have
not:

- **The max and the sum are placed.** `00467B10` publishes the largest single mip-chain footprint
  and `00467B00` the 1-vs-4 aggregate; both are subtracted by `00467AA0` to give the budget
  (`UQ-90`, answered 2026-09-14). **What the 1-vs-4 factor MEANS is still open** — `D-6`, where
  all four candidate readings are now argued against.
- **Two of the forty bytes are ~~read~~ written, and none is read** *(corrected 2026-10-02, OPUS: UQ-89's answer below — only their initial and per-frame reset values exist, because nothing reads them)*. `+0x00` is cleared and `+0x20` is set to `0xFF`, every frame,
  by `002F4520` (`UQ-89`). **The other thirty-one are not**, and no reader of any of them has been
  identified — which is a bounded observation and not an absence claim, since thirteen other
  qword readers of displacement `+0x218` elsewhere in the image have not been excluded as this
  object.
- **The record layouts are registered** as `LegacyPs2GsSourceTextureRecord` (`0x60`),
  `LegacyPs2GsReferenceDescriptor` (`0x30`) and `LegacyPs2GsDerivedSlotRecord` (`0x28`), with only
  the offsets actually read.

The mechanism above is complete; what the entries are *for* still needs the callees named.

- [x] ~~**UQ-88.** What `0209A6E8` is, and why its value is offset by 23 to make a bit position.~~ **Answered 2026-09-14 (FABLE):** it is **the Weather Slot cached for the resource rebuild**, 1-based. RIP census, ten references:
      - **Two writers.**
        - `0026E8D0`, the Movement resource reconfiguration this chain already names, stores its argument (`0026E8E1`). Both of its callers pass `WorldField_GetCurrentWeatherSlot1To3WithDebugOverride()`: the bridge tail `003792B0` and the alternate rebuild `003796A2`.
        - A reset stores 1 (`0026E653`).
      - **Readers.** `002F7380` (this function), `0026ECE9`, `002F5616`, and five small readers at `003ECD0F`–`003ED14C`. The one of those read, `003ECFD0`, indexes a per-slot table of `0x180`-byte records at `[02EBB7F0]` with `slot − 1` (`003ECFE2`–`003ECFEF`).
      **So the offset is a slot-to-bit mapping:** slots 1, 2 and 3 select bits **24, 25 and 26** of each entry's flags dword. The entries carry one membership bit per weather slot, and the rebuild keeps only those that belong to the slot now in force. What sets those bits in the authored entries is not read here.
- [x] **UQ-89.** What the 40-byte selected-record entries at `[rdi+0x218]` hold.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): only their initial and per-frame reset values, because nothing
      reads them.** The owner is `LegacyPs2GsTextureContext`, one heap object cached at `0209A670`. Every function
      referencing that global (24) and every callee handed the loaded context in `rcx` (2) was decoded, and the only
      code touching `+0x218` is the context's own four functions:
      - the context's initialiser sets the pointer to null;
      - the rebuild `002F7380` releases, allocates and writes `+0x00`/`+0x08`/`+0x10`/`+0x18` as zero qwords and
        `+0x20` as a zero byte;
      - the per-frame callback `002F4520` clears `+0x00` and sets `+0x20` to `0xFF` (`002F4600`, `002F460B`);
      - the release callback frees the table through `003EC8A0`.
      Inside those four, the table pointer is dereferenced only by stores. So `+0x08`, `+0x10` and `+0x18` stay
      zero for the table's life, `+0x00` / `+0x20` are reset every frame, `+0x21`..`+0x27` are never written, and no
      field is consumed. The table is sized, allocated and reset but read by nothing in this build, the same shape
      as the other compiled-out PS2 GS paths. **Blind spot, stated:** a reader reaching the context through a pointer
      copy held anywhere other than `0209A670` would not be seen. Control:
      `_index/candidates/uq89-slot-entries/slot_entry_readers.py` (3 checks; its register bindings die on redefinition
      and across calls).
- [x] ~~**UQ-90.** What `00467AA0` returns — it is the budget the whole selection is bounded by.~~ **Answered 2026-09-14 (FABLE):** the remaining legacy PS2 GS local-memory budget, in 32-bit words:
      `(0x1007FF − 3·[022D8EAC]·[022D8EB4] − [02CA6008] − [02CA6004]) & ~0x7FF`, that is `ceil((0x100000 − used) / 0x800) · 0x800`.
      - **The arena and the reservation.** The 4 MiB arena, 8 KiB pages and the three 512 × 448 surfaces are derived on [texture-mip-local-memory-budget.md](../../../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md) §4.
      - **The two subtracted totals** are the rebuild's own two totals, published just before the call: `00467B10` stores the **largest single-record mip-chain footprint** (`00466190`, the running maximum in `esi`, `002F7436`–`002F743B`) at `02CA6004`, and `00467B00` stores **the sum of 1 per 4-bit-indexed record and 4 per other record** (`00466220` selects `edx` = 1 or 4, `002F744A`–`002F7455`) at `02CA6008`. So the max and the sum this page left unexplained are what the budget is reduced by.
      - **Consequence.** The budget is 176 pages (1.375 MiB) only while those two totals together stay under `0x800` words. It does not depend on the machine, but it does depend on the area's texture bank.

### The `002F7380` exclusive subtree — all 6 members bound (SWE2-FRONTIER, followup queue)

The exclusive census assigns `002F7380` **6 frontier functions** — five of the seven "unnamed
`FUN_`" callees the opened section above lists (`003EC8A0` and `003EC8D0` are shared
allocator-side callees, not census members). Every member was disassembled from the shipping
image; interior cites are one instruction inside each declared extent. **The members are the
GS texture-memory machinery the section said the meaning needed**: `00466190` is the per-record
mip-chain footprint, `003A1E50` the per-level GS block-layout cost it sums, and `00467AA0` the
UQ-90 budget formula itself, confirmed byte-for-byte.

| member | size | role | interior |
|---|---:|---|---|
| `003A1E50` | 144 B | the per-level footprint formula: `((w−1+gw) & ~(gw−1)) · ((h−1+gh) & ~(gh−1)) / div`, where a jump table on `arg3 − 2` (0–0x2A, RVA entries at `003A1EE0`) picks the format's granularity triple (gw/gh/div — e.g. arms for `0x40/0x40/2`, `0x80/0x80/4`, `0x80/0x80/8`) | `003A1E7C` |
| `00466190` | 134 B | the record's total mip-chain footprint — the pass-1 "maximum": record `i` at `[base+8] + i·0x60`, `byte[+5]` is the mip count (clamped ≤7), and the loop sums `003A1E50(fmt, w≫k, h≫k)` over `word[+6]`/`word[+8]` halving per level | `004661E8` |
| `00466220` | 25 B | the 1-vs-4 increment selector: passes only when `byte[rec] ∈ {0x14, 0x1C, 0x24, 0x2C}` (the `(x−0x14) & 0xE7 == 0` mask — the 4-bit-format family), and returns 1 for `{0x14, 0x24, 0x2C}`, 0 for `0x1C` | `00466228` |
| `00467AA0` | 41 B | the budget itself — `(0x1007FF − 3·[022D8EB4]·[022D8EAC] − [02CA6008] − [02CA6004]) & ~0x7FF`, the UQ-90 formula verified against the bytes | `00467AB0` |
| `00467B00` | 7 B | stores `ecx` → `02CA6008` — the pass-1 sum the budget subtracts | `00467B00` |
| `00467B10` | 7 B | stores `ecx` → `02CA6004` — the pass-1 maximum (largest record footprint) the budget subtracts | `00467B10` |

`003EC8A0` (entry point's early call) and `003EC8D0` (the `+0x218` allocator) are shared
callees with other callers — deliberately not census members. UQ-89 (the `0x28`-byte
selected-record entries' content) ~~stays open~~ *(answered 2026-09-26: see UQ-89 above — nothing reads them; 2026-10-02, OPUS)*: none of the six reads or writes them.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Save_Load_Settings — SERVICE.** `0025D9E0` on this page calls `SaveWrite_GetBusyFlag`, owned by that layer. What it reaches is **seven bytes** returning the flag at `[02CA99E8]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## The `0026D910` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0026D910` (`WorldField_InitializeCurrentFieldRuntimeParameters`, ~44 B)
— opens on `0017D490(ecx)` (`0026D921`).

| member | role | interior |
| --- | --- | --- |
| `00180620` | gated apply — `001A9930(ecx)` non-null gate (`00180628`/`00180630`) | [`00180628`](../../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0017D490`, `001A9930`.
