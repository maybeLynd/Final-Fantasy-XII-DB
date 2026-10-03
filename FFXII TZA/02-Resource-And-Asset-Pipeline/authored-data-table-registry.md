---
system: The authored-data table registry
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — every register row is closed or dispositioned and the page's residue is answered (owner re-status 2026-10-01, OPUS, on SWE2-STRUCT's batch 12 and residue record) — the contents of the other 26 slots (UQ-80) are SUPERSEDED 2026-09-27 under FRONTIER's class-1 ruling (uq80_coverage.py: 15 of 23 tables fully mapped, the 60-byte residue carried by the static-FIELDS work); the identity of all 64 slots (AG-2) answered 2026-09-26 (ag2-slot-identity.tsv); whether same-slot classes differ elsewhere (UQ-81) answered 2026-09-25 (they do, in the query-record filler); the board-request slots corrected 2026-09-30 (they hold the loaded boards' addresses; swe2struct-ddres-b12-0930 R2); the AG-4 remainder (the byte 0055CD40 copies into +0x558) answered 2026-09-30 (never read at -1: the board-choice byte is UI state, and 0055B3F0's 0xFF guard covers the copy path; swe2struct-residue3-0930 G1-G9)
owner_layer: PrimaryOwner:Resource / consumed across every gameplay owner
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites `002EE430`; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-11
audit:
  passes: 2
  last_pass: 2026-09-06
  last_pass_state: "GN160 (gzf fa0db293…d2f708, exe 73461d08…d89721f8) — independent pass by repos-4b: capstone decode of the 0x0023A160 category dispatch and the 0x003EA710 call sites. §2's caution on BattleData_SetAreaArdSectionCategory is answered inside the function it names; the five-slot map is now in §2b and 0x02EBF168 was absent from this document entirely."
  last_pass_by: repos-4b
  crossref_clean: true
  reopened_count: 3
origin: found by noticing three separately-documented tables sat within 0xA0 bytes of one another
registry_slots:
  - "0x02EBF020"
  - "0x02EBF078"
  - "0x02EBF0A8"
  - "0x02EBF0D0"
  - "0x02EBF198"
  - "0x02EBF138"
  - "0x02EBF190"
  - "0x02EBF178"
  - "0x02EBF180"
  - "0x02EBF1A8"
  - "0x02EBF1B0"
  - "0x02EBF1B8"
  - "0x02EBF1C0"
  - "0x02EBF1C8"
  - "0x02EBF1D0"
  - "0x02EBF1D8"
  - "0x02EBF1E0"
  - "0x02EBF1E8"
  - "0x02EBF1F0"
  - "0x02EBF1F8"
  - "0x02EBF168"
  - "0x02EBF200"
---

# The authored-data table registry

> **Most of FFXII's authored content — items, actions, loot chances, enemy definitions — is reached
> through one array of 64 pointers.**
>
> **Corrected 2026-09-02 (section 8b).** The original line said *"every authored number"* and the
> document treated all 64 slots as authored tables. **One slot is a runtime state block, not a
> table.** The array is a global pointer registry that authored tables dominate but do not
> monopolise.

**PARTIAL.** The array's existence, bounds and stride are read at tier 1, and five slots are
identified. Most are known only by their principal consumer, three are unreferenced, and the
count/stride/RVA header is **not** universal across slots.

## 1. What the player sees

Nothing, but it is the shape of the entire game's content.

FFXII is a game of tables: what a Potion costs, how much a Fire spell charges for, which loot a
Wolf drops, what a Zodiac Spear requires. All of it is authored data, none of it is in the code —
and the code reaches all of it the same way, through **one registry**.

For anyone modding the game, this is the index at the front of the book.

## 2. Native mechanism

### A 64-slot pointer array — *count corrected 2026-09-22 (FABLE)*

```
0x02EBF008 .. 0x02EBF200      64 slots, 8-byte stride, 512 bytes
```

> **Corrected 2026-09-22 (FABLE) on `OPUS-REQ-FABLE-REGISTRY-PAGE-IS-ONE-SLOT-SHORT`, and OPUS is
> right.** This page read the array as **63 slots ending at `0x02EBF1F8`**. It ends at
> **`0x02EBF200`**, and the function that proves it is the array's own initialiser.
>
> **`00236C30` (1,037 B) fills the array, and ~~its first and last stores are the array's bounds.~~** Its
> ~~first is `mov qword ptr [0x02EBF008], rax` at `00236C74`, sourced from the record's `+4`;~~
> *Corrected 2026-09-26 (FABLE, Claude Opus 5.5): the store at `00236C74` writes `0x02EBF180`, the weapon-class map, as
> the tail read below already says. `0x02EBF008` is bound from `+0x118` by the registrar, the lea at `00237010` and the
> field read at `00237017`, second to last. So the bounds are the LOWEST and HIGHEST slots the initialiser binds, not its
> first and last stores. Neither the origin nor the count of 64 changes. Checked by `ag2_slot_identity.py` C8.* Its
> **last is `mov qword ptr [0x02EBF200], rcx` at `00237031`, sourced from `+0x11C` — immediately
> before `add rsp, 0x28` / `ret`**. A slot written by the initialiser as its final act, in the same
> body that takes the array's origin, is a slot of the array. `(0x02EBF200 − 0x02EBF008) / 8 + 1 = 64`.
>
> *Why the earlier reading stopped one short, stated because the shape recurs:* the census that found
> the array looked for **references**, and `0x02EBF200` has **exactly one — a write, from the
> initialiser**. It is the same blind spot section 8c already corrected once on this page, when a
> load-only scan reported 60 of 63 instead of 62; **the fix then was to count writes too, and this
> slot is the case that fix still missed at the boundary.** A reference census finds an array's
> interior reliably and its ends only if the ends are read.
>
> *The origin is likewise `0x02EBF008` and not `0x02EBF000`* — answering the second half of
> `OPUS-REQ-FABLE-02EBF000-BAND-SHAPE-BEFORE-DECLARATION`. `0x02EBF000` is a **float** with one
> writer, `0039AF20`, and no `lea`; the array's slots begin at `0x02EBF008`, which is the first cell
> `00236C30` addresses. `0x02EBEFF8` and `0x02EBEFFC` belong to the preceding structure (one writer
> each, `0039AED0`), and `0x02EBF208` is `lea`-taken by a **different** function, `00233E00`, which is
> where the next structure begins.

**Corrected 2026-09-02 — see section 8c.** The figure below came from a scan for `MOV`/`LEA`
**loads**, which cannot see a global that is only ever written. A full reference census finds
**62 of 63** slots referenced, not 60, and only `0x02EBF198` has no reference at all. *Both figures are against the 63-slot extent this page carried until 2026-09-22; against the corrected 64 the 64th slot has exactly one reference, the initialiser's write.*

The original, superseded reading: scanning `.text` for genuine `MOV`/`LEA` loads finds **60 of the 63 slots
referenced**, at a perfectly regular 8-byte spacing, with only `0x02EBF178`, `0x02EBF188` and
`0x02EBF198` unreferenced. A run of sixty consecutive referenced 8-byte globals is a pointer array,
not sixty unrelated variables.

A handful of further globals exist past the array (`0x02EBF278`, `0x02EBF380`, `0x02EBF3D0`,
`0x02EBF3E0`, `0x02EBF3F0`) with 1-3 references each; they are outside the regular stride and are
**not** treated here as members.

### The authored tables share one header

Three slots have been read in detail by other documents, and all three use the same header.
**This is the convention authored tables follow, not a property of the array** — see section 8b for a
proven counterexample:

```
<slot pointer>
  +0x04   i32   entry count
  +0x08   u16   row stride
  +0x0C   u32   RVA -> row array, via ImageAddress_ResolveRuntimePointer
```

| Slot | Table | Read in |
|---|---|---|
| `0x02EBF0C0` | loot chance/quantity profiles | Rewards - loot drops |
| `0x02EBF0F8` | equipment definitions | Items - id encoding |
| `0x02EBF160` | weighted action ids | Combat AI - gambits |

`ImageAddress_ResolveRuntimePointer` converts the stored RVA into a live pointer, which is why the
tables can be relocated as a block. This is the **general authored-data access path**, now seen in
four subsystems.

### The registry by weight of use

Reference counts show which tables the engine leans on. The principal named consumer of each is
given where one exists:

| Slot | Refs | Principal named consumer | Entry | A site where it touches the slot |
|---|---:|---|---|---|
| `0x02EBF190` | **170** ⚠ | `BattleSystem_InitializeAreaState` | `002342F0` | `00234360` |
| `0x02EBF138` | **128** ⚠ | `BattleAction_ComputeChargeLimitTicks` | `002F8410` | `002F841F` |
| `0x02EBF0F8` | 42 | `Equipment_SelectPreferredCandidateByAuthoredStats` | `002F7A10` | `002F7A26` |
| `0x02EBF130` | 23 | `BattleUnit_ApplyUnitDefinition` | `0023A570` | `0023AA66` |
| `0x02EBF118` | 18 | `BattleStats_ChangeStatusAndProcessSideEffects` | `0030E360` | `0030E645` |
| `0x02EBF038` | 15 | `BattleStats_InitializeDefinitionRecord` | `0023AC80` | `0023AE15` |
| `0x02EBF040` | 15 | `BattleAction_ComputeChargeLimitTicks` | `002F8410` | `002F8750` |
| `0x02EBF1A0` | 10 ⚠ | `BattleStorage_InitializeWorkArrays` | `002368D0` | `002369E5` |
| `0x02EBF170` | 9 | `BattleUnit_ApplyUnitDefinition` | `0023A570` | `0023A860` |
| `0x02EBF058` | 8 | `InventoryBundleClass0D_ApplyNestedItems` | `002FD780` | `002FD7A2` |
| `0x02EBF0D8` | 7 | `GambitTargetDefinition_BindAndBuildMenuLookup` | `00238880` | `00238895` |
| `0x02EBF120` | 7 | `BattleData_SetAreaArdSectionCategory` | `0023A160` | `0023A196` |
| `0x02EBF018` | 7 | **`battle_message.bin`** — the battle message table (`us`: 102 × 8 B + text heap), named 2026-09-11 by content agreement between every event id the code posts and the row text at that index, not by a traced load ([the post-result events page](../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) §2.5); readers `0046AB10`, `00469570`, `005369C0` | `0046AB10` | `0046AB72` |
| `0x02EBF0C0` | 6 | `Loot_RollDropEntries` | `003180F0` | `0031816D` |
| `0x02EBF0F0` | 5 | `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` | `003008A0` | `003009FB` |
| `0x02EBF160` | 2 | `BattleData_ResolveWeightedId` | `00308EC0` | `00308EDD` |

> **Anchored and re-verified 2026-09-03.** Every named consumer above was checked against a
> whole-image rip-relative reference census: **15 of 15 really do reference the slot they are named
> against**, and the site column is a real instruction in each. **No row was taken on the name.**
>
> **Three ref counts disagree with that census and are marked ⚠**, counting *distinct referencing
> functions*: `02EBF190` **170 → 176**, `02EBF138` **128 → 129**, `02EBF1A0` **10 → 13**. The other
> twelve match exactly. **The originals are left in place rather than overwritten**, because the two
> counts were produced by different instruments and this document does not establish which is right —
> and the census is known to *under*-count, since it decodes `[rip + disp]` only and this executable
> also reaches globals through a register holding the image base. **A disagreement in the direction
> of "the census found more" is the direction that needs explaining, and it is not explained here.**

The two heavyweights are worth naming: **`0x02EBF190` with 170 referencing functions** and
**`0x02EBF138` with 128**. Whatever those hold is consulted by more of the engine than anything
else in the registry.

### A caution on identifying slots by consumer

Many slots list `BattleEncodedId_IsValidForClass` as their only named consumer. **That function
validates ids against many different tables**, so its presence says a slot is an id-indexed table
and nothing more. Those slots are *not* identified here, and are deliberately left blank rather than
labelled by a consumer that touches everything.

The same caution applies more weakly to `BattleData_SetAreaArdSectionCategory`, which appears
against four slots (`0x02EBF120`, `0x02EBF140`, `0x02EBF148`, `0x02EBF150`) - it plausibly binds
several area sections at once.

> ### AUDIT 2026-09-06 — the caution is right, and the answer was inside the function it names
>
> *`repos-4b`, auditing for the pattern "a rule invoked and then not applied".*
>
> **The caution above is correct as a caution** — one function does bind several slots, so a
> reference census cannot attribute them. **But it stops one function short.**
> `BattleData_SetAreaArdSectionCategory` takes a **category number in `ecx`** and dispatches on it:
>
> ```asm
> 0023A160  test ecx, ecx      je 0023A1B7     ; category 0
> 0023A164  sub  ecx, 1        je 0023A1A5     ; category 1
> 0023A169  sub  ecx, 1        je 0023A196     ; category 2
> 0023A16E  sub  ecx, 1        je 0023A187     ; category 3
> 0023A173  cmp  ecx, 1        jne 0023A1C6    ; category 4, else return
> ```
>
> Each arm loads one slot address and tail-calls a binder. Resolving the five `lea rcx, [rip+d]`:
>
> | category | slot | binder | call site in `0x003EA710` |
> |---:|---|---|---|
> | 0 | **`0x02EBF150`** | `0x003845F0` | `0x003EA76A` |
> | 1 | **`0x02EBF168`** | **`0x003846F0` — a different binder**, with a third argument zeroed (`xor r8d, r8d`) | `0x003EA777` |
> | 2 | **`0x02EBF120`** | `0x003845F0` | `0x003EA784` |
> | 3 | **`0x02EBF148`** | `0x003845F0` | `0x003EA7D1` |
> | 4 | **`0x02EBF140`** | `0x003845F0` | `0x003EA7FA` |
>
> **So the slots are individually identifiable after all** — not from the census the caution rightly
> rejects, but from the dispatch three instructions inside the consumer it names. The caller passes
> the category as a literal at each of the five sites, so the mapping is fixed, not data-driven.
>
> **Two corrections follow.**
>
> 1. **The caution names four slots; there are five.** `0x02EBF168` is category 1 — and it occurred
>    **zero times in this document** before this audit. A reader working from the registry would not
>    know the slot exists.
> 2. **Category 1 is not bound the same way as the others.** It goes to `0x003846F0` rather than
>    `0x003845F0`, with an extra zeroed argument. Any statement of the form *"the `.ard` slots are
>    bound by `AreaData_BindAndRebaseSectionDescriptor`"* is true of four of the five.
>
> **This matters now because the enemy-record work starts here.** The board directs three authors to
> this document, and the record's resolution runs through these exact slots.
> [The `.ard` loader sheet](VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)
> reached the same five-slot map from the `.ard` side; **this audit confirms it independently from
> the dispatch, and imports it here.**

## 2z. The last five slots, declared 2026-09-12 (`OPUS-REGISTRY-FIVE-SLOTS`)

`registry_explained` stood at **58 of 63**. These are the other five. Four have a principal
consumer and are declared from it; the fifth has **no consumer at all**, and that is its
declaration rather than a gap in the search.

### `0x02EBF020` — a **grouped** table: an index array, then rows

The only reader is `0032A230(group, key, out)`, and it is the one slot in the registry whose header
uses **two** offsets:

```c
hdr  = *(void **)0x02EBF020;
idx  = ImageAddress_ResolveRuntimePointer(hdr->offset_1C);   /* 0032A25A: [rax + 0x1C] */
rows = ImageAddress_ResolveRuntimePointer(hdr->offset_0C);   /* 0032A2CC: [rax + 0x0C] */
if ((unsigned)group > *(uint32_t *)hdr - 1) return 0;        /* 0032A26D: the count is at +0x00 */   /* <- corrected 2026-10-02, OPUS: the count is the first dword of the +0x1C list, *(uint32_t *)idx_list (0032A230+0x2A mov ecx, dword ptr [rax + 0x1c]; 0032A230+0x3D mov eax, dword ptr [rax] on the 0020E600 result) */
lo = group ? idx[group - 1] : 0;                             /* 0032A28C: [r9 + rcx*4 + 4] */
hi = idx[group];                                             /* 0032A291: [r9 + rsi*4 + 4] */
if (lo >= hi) return 1;                                      /* an empty run */
for (i = lo; i < hi; ++i) {                                  /* 0032A300-0032A30C */
    row = rows + *(uint16_t *)(hdr + 8) * i;                 /* 0032A2F2: the stride at +0x08 */
    *out = row;
    if (*(uint16_t *)row == (uint8_t)key) break;             /* 0032A303: the key is the row's u16 */
}
```

**So it is a CSR-shaped table**: `idx[g-1]..idx[g]` delimits group `g`'s run of rows, the rows are
`stride` bytes each, and the search key is the row's own leading `u16`. **Its count lives at ~~`+0x00`,~~ `+0x00` of the `+0x1C` group list,
not at `+0x04`** *(corrected 2026-10-02, OPUS: `0032A230+0x2A` `mov ecx, dword ptr [rax + 0x1c]` and `0032A230+0x3D` `mov eax, dword ptr [rax]` on `0020E600`'s result; the header's own `+0x00` is the `st2e` magic)* — which is the header non-uniformity §8b already warns about, met here in the one
place it matters most. Two callers: `0031EB20` and `0032A320`.

### `0x02EBF0A8` — an ordinary `st2e`-shaped table with a generated accessor pair

Two readers, and between them they are the whole convention:

| function | size | what it is |
|---|---:|---|
| `003204B0` | 17 B | `Count()` — `return hdr ? *(uint32_t *)(hdr + 4) : 0` |
| `00320B30` | 116 B | `Row(i)` — rejects `i < 0` and `i > count - 1`, resolves `hdr + 0x0C`, and returns ~~`rows + *(uint16_t *)(hdr + 8) * i`~~ the row's leading dword, `*(u32 *)(rows + *(u16 *)(hdr + 8) * i)` *(corrected 2026-10-02, OPUS: `00320B30+0x58` `mov eax, dword ptr [rax]`, as the subtree table below says)* |

**Both are called from exactly one function, `0037C2E0`**, which is itself called from exactly one,
`0022B7E0`, and which selects among its arms on the byte at `02EBF3DC`. The caller census carries its
own control — 632 `memcpy` sites — so "exactly one" is a measurement.

That sole-caller chain is `0022B7E0`'s whole **6-member exclusive subtree** — the multi-frame
table-population machine boot mode 1 pumps once the async-read queue goes idle:

| member | size | role | interior |
|---|---:|---|---|
| `0037C2E0` | 224 B | the state machine on the `02EBF3DC` byte triple — `+0` state, `+1` the index read per pass (never written here), `+2` incremented per record; states 0/1 call `Count()`/`Row(i)` and `002EAE20`-allocate a record into `02ADD948`, state 2 probes it (`002E4C70`) then refcounts (`002EAF70`) or flag-writes (`002EBE20`) it, state 3 loops to 1, state 4 writes `4` to `02EBF3DC` and returns 0 — the "done" `0022B7E0` reads | `0037C2F6` |
| `003204B0` | 17 B | `Count()` — the `02EBF0A8` header's `*(u32*)(hdr + 4)`, 0 on null | `003204BC` |
| `00320B30` | 116 B | `Row(i)` — bounds-checked `i < count`; resolves `*(hdr + 0x0C)` twice through `0020E600` (null-gate then base), and returns **the row's leading dword** `*(u32*)(base + *(u16*)(hdr + 8) * i)` — a dereference, not the pointer | `00320B5D` |
| `002E4C70` | 21 B | record probe — `!(*(u8*)(obj + 0x19) & 4)`, null → 0 | `002E4C75` |
| `002EAF70` | 33 B | record refcount decrement — `dec word [obj + 0x1C]`; on expiry, records with `+0x19 & 3` clear tail to `002EAEB0` (marks `+0x18` bit-2 for deferred release); tagged records just get the count zeroed | `002EAF80` |
| `002EBE20` | 18 B | record bit-1 setter — clears `+0x19 & 2`, writes `(arg & 1) << 1` | `002EBE29` |

The root's side of the contract: `0022B7E0` runs `0037C2E0` only on frames where `0032E520(1)`
reports the queue idle (`jne` skips it while reads are outstanding); while the machine works,
`02064AD4` mirrors the byte at `02064AD3`, and when the machine returns 0 (its state-4 exit)
`02064AD4` is set to `2` — the mode-2 advance the resource-request-queue page records, after which
`00184960(2)` runs each frame. `002EAE20`/`002EAEB0` (record alloc / deferred-release marker) and `0020E600` (the
stored-id resolver) are shared callees — deliberately not census members.

### `0x02EBF078` — the **fourth** table summed into encoded-id class 13's bound

`BattleEncodedId_IsValidForClass` computes class 13's upper bound by **adding four row counts**, each
read as `*(uint32_t *)(hdr + 4)` and each contributing 0 when its slot is null:

```asm
00322E28  [02EBF090] -> r9d      00322E80  lea ecx, [r9 + 0x8000]
00322E44  [02EBF088] -> r10d     00322E7D  add eax, r8d
00322E59  [02EBF080] -> r8d      00322E87  add eax, r10d
00322E6E  [02EBF078] -> eax      00322E8A  add ecx, eax
```

> **[`the-encoded-id-class-registry.md`](../00-Engine-Core-Runtime/the-encoded-id-class-registry.md)
> §10 lists class 13 as THREE sub-tables** — `02EBF090 / 02EBF088 / 02EBF080`, named as key items at
> `0x8000`, `0x8040` and `0x8060`. **The validator sums four.** Routed as
> `OPUS-CONTRA-CLASS13-FOURTH-TABLE` rather than edited here; that page is not this one's to change,
> and which authored file the fourth is remains theirs to name.

### `0x02EBF0D0` — class 12's descriptor, read for its count alone

One reader, `BattleEncodedId_IsValidForClass` at `00322DFE`, taking `*(uint32_t *)(hdr + 4)` as the
bound for class prefix `0x7000`. The class registry already records class 12 against this slot and
notes it is *"referenced by the validator alone"*; this declares the slot with that consumer.

### `0x02EBF198` — **no reference anywhere in the image**, with the control that makes that readable

`globals_index.py` reports no RIP-relative row, and its own caveat is that an indexed
`[reg + i*8 + disp]` access would not appear. So the negative was measured instead, over the whole
registry at its own stride:

> `data_xref_scan.py --range 0x02EBF008 0x02EBF1F8 --stride 8` over all 34,270 function bodies:
> **62 of 63 slots have at least one direct reference. Exactly one has none, and it is `02EBF198`.**

**That is the control.** The same scan, the same method and the same range find every other slot,
so its silence here is a measurement rather than a blind spot. Nothing loads the slot and nothing
stores to it — the neighbouring slots each show a read/write pair in a small generated accessor, and
this one shows neither. **The slot is never populated and never consulted by the shipped code.**

**What this does not claim.** Not that no such table exists in the authored data — only that no
instruction in this image reaches this slot. An access computed through a base register plus a
runtime index would still be invisible, and the honest limit is that the other 62 being reached
*directly* makes an indexed-only 63rd unlikely rather than impossible. Settling that completely needs
a base-plus-index scan keyed on the registry's own base, which is `AG-9`. *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale. `AG-4` is ANSWERED in §7: slot 50 is the underflow element of the `0x02EBF1A0` array. No such binder path exists either. Every one of the 42 calls of `003845F0` is handed one slot's own address, and none is `0x02EBF198` ([record](../_index/candidates/swe2struct-ddres-b12-0930/README.md) check R3). The register's `AG-9` is the battle-state block's layout, not this scan.)*

## 3. Key addresses

| Address | Role | Verified |
|---|---|---|
| `0x02EBF008` – `0x02EBF200` | the registry: 64 slots, 8-byte stride — **end corrected 2026-09-22 (OPUS)** from `0x02EBF1F8`/63, which this row still carried after the body of the page had been corrected; `00236C30` `lea`s the origin AND writes `0x02EBF200` at `00237031`, and `(0x02EBF200 − 0x02EBF008) / 8 + 1 = 64` | ✅ scanned |
| `0x02EBF198` | the **only** in-span slot with no reference of any kind | ✅ censused 2026-09-02 |
| `0x02EBF178` | **2 references, both writes** — not unreferenced (§8c) | ✅ censused |
| `0x02EBF188` | **93 references, all writes, zero reads** — not unreferenced (§8c) | ✅ censused |
| `0x02EBF0C0` / `0x02EBF0F8` / `0x02EBF160` | loot / equipment / weighted-id tables | ✅ read elsewhere |
| `0x02EBF138` | **action definition table**, ids `0`..`0x21E` (543) | ✅ read via consumers |
| `0x02EBF190` | **battle system runtime state block**, >= 23 KB, mutable | ✅ read via consumers |
| `003845F0` | `AreaData_BindAndRebaseSectionDescriptor` — binds and rebases slots | not read *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale, read whole as `AG-12` in §8d)* |
| ~~`002383C0`~~ `00238390`–`002385A0` | ~~11~~ 12 generated 39-byte slot setters, `0x30` apart *(corrected 2026-10-02, OPUS: `00238260+0x1D` names `00238390`, the setter for `0x02EBF1A0`, ahead of `002383C0`)* | ✅ read |
| `00384160` | `Navigation_BindAndRebaseDataset` — same pattern, Movement | not read *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: read on its owners' pages, [the navigation-mesh page](../06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md) and [the map control pack](../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md))* |
| — | `ImageAddress_ResolveRuntimePointer` | not read *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale, `0020E600` is read whole on this page, "The resolver is three instructions")* |

## 4. Data structures and formulas

```
Registry            0x02EBF008 .. 0x02EBF1F8   <- corrected 2026-10-02, OPUS: .. 0x02EBF200, 64 slots (00236C30+0x401 stores 0x02EBF200)
  slot[i]  = *(void **)(0x02EBF008 + i * 8)        i = 0 .. 62   <- corrected 2026-10-02, OPUS: i = 0 .. 63

Table header        at each slot pointer that IS an authored table (NOT universal - see 8b)
  +0x04   i32   entry count
  +0x08   u16   row stride
  +0x0C   u32   RVA of the row array

Row address
  row(t, n) = ImageAddress_ResolveRuntimePointer(t[+0x0C]) + n * t[+0x08]

Bounds convention   (seen in loot, equipment)
  valid  iff  0 <= index <= t[+0x04] - 1        else fail closed
```

## 5. Call chain

```
area / game load
  -> authored data sections loaded from the VBF archive
  -> registry slots populated with pointers

any gameplay lookup
  -> read slot pointer
  -> count at +0x04         bounds check, fail closed
  -> stride at +0x08
  -> RVA at +0x0C -> ImageAddress_ResolveRuntimePointer
  -> row = base + index * stride
```

**Upstream:** the resource pipeline that loads authored sections.
**Downstream:** effectively every gameplay system - combat, items, loot, AI, status, inventory.

**Do not confuse with:** the Phyre reflection class descriptors, which describe *engine C++ types*.
This registry indexes *authored game content*. Different systems, different data.

## 6. Modding notes

- **This is the index to FFXII's content.** 64 slots — mostly authored tables, but **not exclusively**
  (`0x02EBF190` is a runtime state block).
- **Authored tables share one header** — count, stride, RVA. A generic reader can walk any of them
  once the slot is confirmed to be a table. **Check before assuming**: verify `+0x04` looks like a
  plausible count rather than a bitfield.
- **Bounds are ~~fail-closed~~ per consumer.** ~~An out-of-range index returns a miss, not garbage.~~ The canonical row lookup tests neither the index nor a null table, and reads a null table at a near-null address; only the consumers that compare the index with the `+0x04` count fail closed *(corrected 2026-10-02, OPUS: `003876D0` multiplies the index at `003876D0+0x3B` with no compare, and on a null slot `003876D0+0x42` `xor ecx, ecx` is followed by `003876D0+0x44` `movzx eax, byte ptr [rcx + 9]`; the row-lookup contract §10)*.
- **The RVA indirection means tables can move.** Never hardcode a row address; resolve through the
  slot.
- **`0x02EBF190` and `0x02EBF138` are the highest-value unread targets** — 170 and 128 referencing
  functions respectively. *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale. Both are read as `AG-1` in §8b and
  §7: the action definition table, and the battle-system state block.)*
- **Three slots are unreferenced** (`0x178`, `0x188`, `0x198`) — either cut content or reached by a
  path this scan cannot see. *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale. `AG-4` in §7 shows `0x178` and
  `0x188` are referenced, and that `0x198` is the `−1` element of the `0x02EBF1A0` array, which no instruction
  names.)*
- **XIIOnline:** the registry is authored, read-only content, identical across clients running the
  same build. It is *not* a divergence source — but it is the reference every client must agree on,
  so a version check on the archive is worth more than syncing any individual table.

## 7. What is not known

- [x] ~~What `0x02EBF190` (170 refs) and `0x02EBF138` (128 refs) hold. **AG-1 — the highest-value
      unread data in the database.**~~ **AG-1 WAS ALREADY ANSWERED BY THIS PAGE AND THE BOX WAS NEVER
      TICKED — closed 2026-09-13 (OPUS), stale checkbox, not new work.** §`0x02EBF138` reads it as the
      **action definition table**, Ghidra's `g_pActionDefinitionTableHeader`, ids `0`..`0x21E` (543)
      at ~~**720-byte rows**~~ **60-byte rows** *(corrected 2026-10-02, OPUS: the stride is the header's `u16 +8`, read at `002376F0+0x73` `movzx ecx, word ptr [rax + 8]`, and the section bound there, `battle_pack.bin` directory `+0x3C`, declares 543 x 60; 720 was a reference figure, not a size)*, confirmed through its consumers; §`0x02EBF190` reads it as **not a table
      at all** but the **battle system's runtime state block**, at least 23 KB, whose `+0x04` is a
      bitfield rather than a count — the counterexample that answered **AG-5**. The summary table at
      §4 already marks both **✅ read via consumers**.
      **ONE THING NEITHER SECTION STATES, ADDED HERE: WHERE THE BLOCK IS.** §`0x02EBF190` bounds the
      structure by its offsets but never locates it. Both writers compute the same compile-time
      constant:
      ```asm
      call 002EF640        ; 8 bytes - lea rax,[02164280] ; ret
      add  rax, 0x4E68C
      mov  [02EBF190], rax ; = 021B290C, always
      ```
      `00233C10` is a **lazy initialiser** — it loads the slot and only computes when it finds null —
      and `00238A80` is **`SaveRuntime_RebindImageBackedGameplayState`**, which does it
      unconditionally. So the slot is not bound from a file at all: **it always holds `021B290C`, a
      fixed `0x4E68C` into the block based at `02164280`**, and the save runtime rebinds it because
      the block is image-backed. The `+0x5AE4` offsets the section cites therefore reach
      `021B83F0`, and the "at least 23 KB" bound is a bound on a **located** structure.
      **This is the second stale checkbox found on this page today** — see AG-4 above, where the page
      called a slot unreferenced while its own AG-11 answer said the main loop publishes it.
      **Neither was found by reading; both were found by re-measuring and then discovering the page
      already knew.**
- [x] The identity of most of the 64 slots. **AG-2.** *34 of them now carry a `battle_pack.bin`
      directory field offset (section 2's band-shape ruling, 2026-09-22); the next step is to name
      those fields in offset order.*
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): every one of the 64 slots has an identity, one row per slot in
      [`ag2-slot-identity.tsv`](../_index/candidates/ag2-slot-identity/ag2-slot-identity.tsv).** The next step above was a
      join of two facts already published:
      - the binder's field-to-slot pairs, in the row-lookup contract's section 7a;
      - `UQ-73`'s rule that manifest slot *k* is pack entry *k*, at directory `+4 + 4k`. The manifest is the image's own
        path array at `0x01E4D830`.

      Decoding `00236C30` gives **42** field-to-slot pairs, not 34, by three routes:
      - 35 through the registrar;
      - five through the bespoke binders it calls with the field in `ecx`;
      - two stored directly: `+4` into `0x02EBF180` and `+0x11C` into `0x02EBF200`.

      Every pair lands on a non-empty entry of all nine language packs, and so on a named file. For example:
      - `0x02EBF180` is `WepJob_Matrix`;
      - `0x02EBF130` is `chr_data`;
      - `0x02EBF138` is `action_data`;
      - `0x02EBF0D8` is `targetchip_data`;
      - `0x02EBF008` is `movie`;
      - `0x02EBF200` is `license_board`. *(Declared 2026-10-01, OPUS, [record](../_index/candidates/opus-registry-slot-200-1001/README.md), `slot200_check.py` FAILS 0:)* unlike its neighbours, the slot never goes through the registrar `003845F0`: `00236C30` stores the record's field `+0x11C` raw, the pack-entry index that names `license_board.bin` (`0023702A` / `00237031`). Nothing reads it - its only reference in the image is that write, and every indexed access through the job-board base `0x02EBF1A0` is bounded to that base's twelve slots, `0x02EBF1A0` to `0x02EBF1F8` (`00233E00`, `002368D0`, `00237630`, `00238260`, `00328990`). So no table is loaded for it here.

      The other 22 are already read on this page:
      - the five area `.ard` sections, categories 0-4;
      - the twelve `board_N.bin` request slots;
      - five cells that hold no authored table: the runtime-published buffer `0x02EBF178`, the write-only sink
        `0x02EBF188`, the `BattleSystemState` pointer `0x02EBF190`, the index-minus-one element `0x02EBF198`, and class
        12's descriptor `0x02EBF0D0`, which nothing installs.

      *Controls:*
      - the registrar pairs reproduce section 7a row for row;
      - eleven names that this page and its neighbours gave slots from their consumers agree with the join. Among them
        are the weapon-class map, the party definitions, the loot table, the text banks and MP gain from HP damage
        (`damagemp_data`).

      *One label differs in wording, and is left as a lead:* the 2026-09-07 named-reader census called slot 7
      (`0x02EBF040`) "status auxiliary / timer parameters" from its charge and cost readers, and its file is
      `ability_data`.

      The identity is the authored file. What each file's rows mean is `UQ-80`. Control:
      [`ag2_slot_identity.py`](../_index/candidates/ag2-slot-identity/ag2_slot_identity.py) (9 checks, FAILS 0).
- [x] ~~Whether the array has a header of its own before `0x02EBF008`.~~ **AG-3 ANSWERED 2026-09-12
      (FABLE): no.** The eight bytes before the array are a **float** at `0x02EBF000` written by one
      unrelated function (`0039AF20`, `movss` at `0039AF27`) and four bytes at `0x02EBF004` that
      nothing in the image references (whole-image rip-relative census). The array starts cold at
      `0x02EBF008`.
- [x] Why `0x02EBF178`, `0x02EBF188` and `0x02EBF198` are unreferenced. **AG-4.**
      **PREMISE CORRECTED 2026-09-13 (OPUS): two of the three are not unreferenced, and this page
      already said so about one of them.** Re-measured per slot over the whole `.text` section:
      ***ANSWERED 2026-09-18 (FABLE) — slot 50 is the underflow element of the next array, reached only through a signed index byte whose one producer of −1 also disarms the only reader.** The first two were corrected on 2026-09-13 (referenced). For `0x02EBF198`: `0055BFF0` reads the `0x02EBF1A0` array as `[base + idx*8 + 0x2D9F1A0]` with `base = 00120000` and `idx = movsx byte [obj+0x558]` (`0055C0A0`..`0055C0A8`), so `idx = −1` is exactly `0x02EBF198`. That byte has two writers. `0055B3F0` stores the return of the lookup `003236B0` (`0055B446`..`0055B44B`), which returns `0xFF` when the id exceeds `0x27`, the registry slot is null, its byte `+5` is non-zero or its kind byte `+4` exceeds 6 (`003236E3`) — so −1 *does* occur — and on that `0xFF` it stores `bp = 0` into the count word `+0x559` (`0055B458`..`0055B463`, `ebp` cleared at `0055B417`) and leaves; the reader's loop runs `byte [obj+0x559]` times (`0055C070`, `0055C08D`), so on this path the −1 read never executes. ~~`0055CD40` copies an authored record byte `+0x108` into `+0x558` under `+0x570` bit 10 (`0055CF73`..`0055CF80`) without touching the counts: that is the one path on which a `0xFF` in the data would make the reader dereference slot 50, and its data range is not checked here.~~ *Corrected 2026-09-30 (SWE2-STRUCT for OPUS): the byte is not authored data, and this path is guarded too. `0055CD40` copies its owner's byte `+0x108` (the licence screen's owner widget `00561390`) into `+0x558` under `+0x570` bit 10 (`0055CF73`..`0055CF80`). That byte is the board picked in the board-choice flow: the picker's cursor, 0 to 11, or `0xFF` from the screen's "no board yet" entry (`00560C98`). No file feeds it, so there is no authored range to census, and the static code does not rule out a `0xFF` arriving under bit 10. It does not need to. The same create arm calls `0055B3F0` next (`0055D105`, no call in between), and that function's `0xFF` test (`0055B451`..`0055B463`) runs on the copy path as well as the lookup path and zeroes the count `+0x559`. The `−1` load `0055C0A8` sits inside that count's loop, and nothing else writes `+0x558` or `+0x559`. So slot 50 is not read through this path either ([record](../_index/candidates/swe2struct-residue3-0930/README.md), checks G1-G9).* The slot itself is BSS — zero in the file image — so the 2026-09-16 note that it is *initialised in the image* to `009224A8` is corrected: `009224A8` is a path string (`PS2Data\plan_master\ch\event\...`), not a value the slot holds. So the slot is unreferenced because nothing names it: it is the array's `−1` position, written by no loader and read only through an index whose failure value is guarded. Static: the reader, the two writers, the lookup, the file image.*

      | slot | address | references | what they are |
      |---:|---|---:|---|
      | 46 | `0x02EBF178` | **2** | both **stores**, `00324558` and `0032469A`, in `00324510` |
      | 48 | `0x02EBF188` | **93** in 40 functions | the busiest slot in this group |
      | 50 | `0x02EBF198` | **0** | the only genuine survivor |

      **THE PAGE CONTRADICTS ITSELF ON `0x02EBF178`.** AG-11's answer above — *"…`0x02EBF178` is
      published by the main loop (AG-4)…"*, added 2026-09-12 — states plainly that slot 46 has a
      writer, while this checkbox still lists `02EBF178` as unreferenced. **The checkbox is stale against its
      own page**, and no structural checker can see that: `check_doc_self` compares a document to its
      own *structure*, and this is a disagreement of *content* between two sections. That is pass 28
      territory and it was found by re-measuring, not by reading.

      **SLOT 50 SURVIVES A STRONGER TEST THAN THE ONE THAT RAISED THE QUESTION.** A function-body
      scan only sees listed bodies, and roughly 1,308 code blocks are not listed. Sweeping **every
      byte of `.text`** for a `disp32` that resolves to each address, independent of the function
      list, with two controls:

      ```
      02EBF190  (slot 49, control)   318 candidate operands
      02EBF178  (slot 46)              2  — exactly the two the body scan found
      02EBF198  (slot 50)              0  — in listed AND unlisted code
      ```

      **THE RESIDUAL, WHICH IS THE PART THAT MATTERS.** *Unreferenced is not unwritten.* The array
      base's address **is** taken — `lea rcx, [02EBF008]` at `00237010` in the STATIC delivery
      callback `00236C30` — and it is not a loop base: it is passed as an **argument** to `003845F0`
      ~~together with a **data-driven index** (`movsxd rdx, [rax + 0x118]`, from `0208E680`). So any~~
      ~~slot, slot 50 included, can be bound through that path without a RIP-relative operand naming~~
      ~~it.~~ **Nothing here establishes that slot 50 is never written** — only that no instruction in
      the image names it.
      *Corrected 2026-09-30 (SWE2-STRUCT for OPUS, DD batch 12):* the value beside the `lea` is not an index. It is
      the descriptor. `003845F0(slot, desc)` stores `desc` into `[slot]` and into nothing else (`003845F4`), so the
      `lea` at `00237010` is slot 0's own address (`movie`), and `[0208E680] + 0x118` is the directory dword it binds
      there. No path binds slot 50: all 42 calls of `003845F0` are handed one slot's own address by a rip-relative
      `lea`, 41 distinct slots and never `0x02EBF198`. The one exception, `00238640`, indexes `0x02F973C0`, outside the
      registry ([record](../_index/candidates/swe2struct-ddres-b12-0930/README.md) check R3). `AG-4`'s answer above
      settles the rest: the reader's −1 path is guarded.

      **What remains of AG-4 is one question about one slot:** whether slot 50 is bound through
      `003845F0`'s index and simply never named, or is a genuinely unused hole in the array.
      **NARROWED 2026-09-16 (SWE2-STRUCT), upper-band section below:** it is neither a hole nor
      merely index-bound — the slot is ~~*initialised in the image* (`0x009224A8`, a pointer into the~~
      ~~static region)~~ BSS, zero at load *(corrected 2026-10-02, OPUS: `0x02EBF198` lies past `.data`'s raw end `0x01F7E400`; AG-4's answer above)* and sits at index −1 of the `0x02EBF1A0` array, which `0055BFF0` reads through
      a signed-byte index with no negative guard (`0055C0A8`). So it is reachable code-side as the
      array's underflow element; whether `byte[obj+0x558]` is ever −1 is the live remainder.
- [x] ~~Whether the header is uniform across all 63 slots or only the three read. **AG-5 — the
      generalisation this document rests on.**~~ **ANSWERED ON THIS PAGE — §8b is headed
      *"AG-1 answered, and AG-5 answered NO"* and §`AG-5 answered: NO, the header convention is not
      uniform` gives it in full: `0x02EBF190` is a proven counterexample — its `+0x04` is a bitfield,
      it has no stride, and it is mutable runtime state rather than authored data. So the registry is
      a global pointer array, not an authored-table array, and membership does not imply the header.**
      **Ticked 2026-09-13 (OPUS) as a stale checkbox, not as new work** — the THIRD on this page
      after AG-1 and AG-4, and the answer has been sitting two sections below the bullet since
      2026-09-02.
- [x] What populates the slots, and when. **AG-6.**
- [x] ~~Whether the isolated globals past `0x1F8` belong to a second array.~~ **AG-7 ANSWERED
      2026-09-12 (FABLE): no second array — four unrelated things.** The census of `0x02EBF200`–
      `0x02EBF3FF` finds (1) **a 64th pointer at `0x02EBF200`**, written by the STATIC binder
      `00236C30` as its last act with the blob's raw directory dword `+0x11C` (`0023702A`–`00237031`,
      not through `AreaData_BindAndRebaseSectionDescriptor`); (2) a structure at `0x02EBF208`
      addressed by `00233E00` alone; (3) a structure at `0x02EBF278` addressed by `0022FF10` and
      `002F1F40`; and (4) a cluster of eleven bytes and two dwords at `0x02EBF3D0`–`0x02EBF3FE`
      private to one unnamed family of six functions (`0037B4D0`, `0037C1A0`, `0037C2E0`, `0037C730`,
      `0037C980`, `0037CA00`). Nothing between `0x02EBF210` and `0x02EBF3CF` but the one structure at
      `+0x278` is referenced at all.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 60 of 63 slots referenced at a regular 8-byte stride *(answered: see *Result: OVERTURNED on two of the three* below and the 64-slot extent; 2026-10-02, OPUS)* | `.text` scan for `MOV`/`LEA` loads with `modrm.rm == 101` into `0x02EBF000`–`0x02EBF400` | 1 |
| Slot bounds `0x02EBF008` – `0x02EBF1F8` *(2026-09-26, FABLE, Claude Opus 5.5: the upper bound is `0x02EBF200` since section 2's 2026-09-22 correction; this row had not followed it)* | first and last referenced slots on the stride | 1 |
| The three unreferenced in-span slots | set difference against the full stride | 1 |
| Header shape `+0x04` count, `+0x08` stride, `+0x0C` RVA | complete bodies of `Loot_RollNormalSlotChance` and `Equipment_CheckPrimarySecondaryDefinitionCompatibility` | 1 |
| Reference counts per slot | the same scan, grouped by enclosing function | 1 |
| Principal consumers | function names from the GFZ, matched to scan results | 3 |

### The scan was restricted to real instructions

The previous block in this database was a byte scan that produced nine false positives, all
dissolved by checking instruction boundaries. That lesson was applied here **before** interpreting
anything: this scan matches only genuine `MOV r64,[rip+d]`, `MOV r32,[rip+d]`, `LEA r64,[rip+d]`,
`MOVZX` and `MOV r16` forms with `modrm.rm == 101`, rather than treating any four bytes as a
displacement.

The result is self-validating in a way a noisy scan could not be: **60 hits landing on a perfect
8-byte grid across 504 bytes**. Random false positives do not align to a stride.

### The generalisation, and its limit

**Three of 63 headers have been read.** The claim that *all* slots share the `+0x04/+0x08/+0x0C`
header is an extrapolation from those three — strong, because they belong to three unrelated
subsystems and agree exactly, but not proven. It is recorded as **AG-5** rather than stated as fact,
and §4 presents the header as the convention those three follow. *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12:
stale. `AG-5` is answered NO in §8b and §7, because `0x02EBF190` is a counterexample.)*

## 8b. Reopened 2026-09-02 - AG-1 answered, and AG-5 answered NO

The two heaviest slots were identified by reading their smallest consumers.

### `0x02EBF138` (128 refs) - the action definition table

Ghidra already carries the name `g_pActionDefinitionTableHeader`, and the consumers confirm it:

```c
void BattleFormula_LoadHitAvoidGuardThresholds(...)
{
    if (g_pActionDefinitionTableHeader != 0) { ... }
    DAT_02AEDFE0 = row[0x12];                        // an outcome threshold byte
    g_uFormulaScratchShieldGuardChance = target->bShieldGuardRate;
    g_uFormulaScratchWeaponGuardChance = target->bWeaponGuardRate;
    g_uFormulaScratchAvoidChance       = target->bAvoidRate;
}

uchar BattleAction_ComputeSecondaryResourceMultiplier(unit, word action_id)
{
    if (0x21E < action_id) { ... }                   // bound
}
```

**Action ids run `0` .. `0x21E`** - a bound of **543 actions**. Row fields seen so far: a byte at
`+0x10` feeding `g_fFormulaScratchScale`, and a byte at `+0x12` used as a hit/avoid/guard threshold.

> **The row is mapped (AG-8, 2026-09-12, FABLE)** on [the action definition row](../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md): every byte and word tallied
> over the 543 shipped rows and a reader census over the 129 referencing functions — recipe
> `+0x08`, charge class `+0x09`, flags `+0x0C`, power `+0x10` / `+0x11`, hit threshold `+0x12`,
> affinity byte `+0x13`, status chance `+0x14`, status mask `+0x18`, message kind `+0x1E`, linked
> menu id `+0x22`, Esper row `+0x26`, element `+0x2C`, description `+0x2E`, name `+0x34`; eighteen
> bytes left as shape.

That explains the 128 references: nearly every combat formula needs the acting definition.

### `0x02EBF190` (170 refs) - **not a table at all**

Its consumers are 14-17 byte accessors over a very large structure:

```c
uint FUN_00236740(void)                        { return *(uint *)(DAT_02EBF190 + 4) >> 0xD & 1; }
undefined1 PartyFocus_GetPreferredDefinitionSelector(void)
                                               { return *(byte *)(DAT_02EBF190 + 0x5AA4); }
void FUN_003139C0(undefined1 v)                { *(byte *)(DAT_02EBF190 + 0x5AD4) = v; }
undefined4 FUN_00304660(void)                  { return *(uint *)(DAT_02EBF190 + 0x5AE4); }
```

Offsets reach **`+0x5AE4`**, so the block is at least **23 KB**. It is **written** as well as read.
And `+0x04` is consumed as a **bitfield** (`>> 0xD & 1`), not as an entry count.

**This is the battle system's runtime state block**, which is exactly why
`BattleSystem_InitializeAreaState` is its principal consumer - and why 170 functions touch it.
`002342F0` scrubs the block's 40 `0x1C8`-stride records on every area transition
(`00234360`–`0023438E`); its full 12-member subtree is bound on
[the battle-unit page](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md).

### AG-5 answered: NO, the header convention is not uniform

Section 4 presented `+0x04` count, `+0x08` stride, `+0x0C` RVA as "the convention", extrapolated
from three slots. **`0x02EBF190` is a proven counterexample**: its `+0x04` is a bitfield, it has no
stride, and it is mutable runtime state rather than authored data.

So the registry is a **global pointer array**, not an authored-table array. Authored tables are the
majority of what has been identified in it, but membership does not imply the header.

**This is the caveat doing its job.** AG-5 was recorded last block precisely because the header was
generalised from three of 63 slots. One additional slot was enough to refute it. Had the
generalisation been stated as fact, the registry document would now be wrong in its central claim
rather than merely narrowed.

### Consequences for reading the rest of the registry

- **Slot identity must be established per slot.** A slot's neighbours say nothing about its shape.
- **Reference count indicates weight, not kind.** The two heaviest slots turned out to be different
  *kinds* of thing - one authored table, one runtime state block.
- The bound `action_id <= 0x21E` is a genuinely useful number for modding: **543 action definitions**.

## 8c. Reopened 2026-09-02 - AG-6 answered: the slots are bound section descriptors

### A generated family of setters

~~Eleven~~ Twelve consecutive slots - ~~`0x02EBF1A8`~~ `0x02EBF1A0` through `0x02EBF1F8` - each have a **39-byte** consumer *(corrected 2026-10-02, OPUS: `00238390+0x1A` writes `0x02EBF1A0`; §5 of the AG-2 ruling below)*, and
those consumers sit at `0x00238390`, `0x002383C0`, `0x002383F0`, `0x00238420` ... `0x002385A0`: **exactly `0x30`
apart**. They are a generated family, and each one is a **setter**:

```c
void FUN_002383c0(int param_1)
{
    if (DAT_02EBF1A8 != 0) { ... }
    DAT_02EBF1A8 = (longlong)param_1;      // bind this slot
}
```

So the registry is not a static table of constants - **it is a set of slots that get bound at
runtime**, one generated binder per slot.

### What binds them

`FUN_003847B0`, the smallest consumer of slot `0x02EBF118`, calls:

```
AreaData_BindAndRebaseSectionDescriptor      (003845F0, 252 B, WorldAreaField)
```

That names the mechanism. The registry holds **section descriptors for loaded area data**, and the
binder **rebases** them - which is precisely why every table reaches its rows through an RVA and
`ImageAddress_ResolveRuntimePointer` rather than a stored absolute pointer. The data moves; the RVA
does not.

The same pattern exists elsewhere under its own name: `Navigation_BindAndRebaseDataset`
(`00384160`, Movement) and `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState`
(`0030B6A0`, Items).

**AG-6 is answered:** the slots are populated by `AreaData_BindAndRebaseSectionDescriptor` when area
data is loaded, and rebased at the same time.

### `.ard` - the area data format, with its PS2 paths intact

The GFZ name `BattleData_SetAreaArdSectionCategory` points at the file type, and the binary still
contains the original authoring paths:

```
PS2Data\plan_master\in\plan_map\bhm_c\area\bhm_c.ard
PS2Data\plan_master\in\plan_map\pla_a\area\pla_a.ard
PS2Data\plan_master\in\plan_map\sav_f\area\sav_f.ard
```

**`PS2Data\plan_master\...`** - the PlayStation 2 development tree, referenced by a 2017 PC
remaster. One `.ard` per map, holding the area's authored sections.

That is the **third** PS2 artifact this database has found in the shipping build, after
`PS2DepthOfField.fx.phyre` and the Tremor integer-only Vorbis decoder.

**A naming caution:** these map codes (`bhm_c`, `pla_a`, `sav_f`) are *not* the same scheme as the
`jsondata/maps/` codes (`alc0101`, `ald0102`) found in the render-parameter work. Two different map
identifier systems coexist, and nothing read so far connects them. **AG-10.**

> **AG-10 answered 2026-09-12 (FABLE): both are columns of the map-reference row, and the
> seven-character code is the map_ctrl map name.** For a field id the map-reference table at
> `[02099D88]` ([the environment-variant page](../03-World-Area-Field/choosing-the-field-environment-variant.md)) holds an 8-byte row: its `s16 +2` selects a 16-byte block entry whose
> first word `MapRef_GetAuxValue0` (`00264F40`) returns — **the namespace-4 resource index of the
> field's `map_ctrl` package** (paths of the form
> `PS2Data\plan_master\map_ctrl\alc01\alc0101\bin\alc0101.mpk`, `00BADCD8`) — and its `u16 +4`
> is **the namespace-21 index of the battle-plan `.ard`** (`MapRef_GetAreaArdFieldResourceIndex`
> `00264ED0`, [the `.ard` loader page](VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md) §3). The field loader `00331990(fieldId)` passes the first to
> `00378A60` → `00379A10(4, index)` *(corrected 2026-09-12, FABLE: `00331990` requests **two** packs — the block word
> `MapRef_GetAuxValue0` in mode 0 (`003319A4`) and the row's own word `+0` `MapRef_GetPrimaryFieldValue` in mode 1
> (`003319BF`) — and `00378A60` calls `00379A10` **only in mode 1** (`00378B46`–`00378B51`), so the scene map name
> comes from the row's word `+0`, not from the block word; [the map_ctrl pack](../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md) §3.1)*, which resolves the path, cuts out the directory segment between
> its second and fourth separators from the end (`00379AB0`–`00379AFB`), remaps five names through the
> alias table at `01EF9490` (`dst0109 → dst0103`, `dst0110 → dst0105`, `frs0109 → frs0101`,
> `frs0110 → frs0106`, `gil0303 → gil0301`; `00379B0F`–`00379B8A`) and stores the result as **the scene
> object's map name** (`+0x241`, setter `001A7A50` via `001805D0`). That string is what
> `001C61F0` wraps as `JsonData/Maps/<name>.json` (`001C6285`, loaded by `00214C30`) and what the
> file cache prefetches as `/PrefetchData/Maps/<name>.txt` (`001DA290`). So the `jsondata/maps` code
> names the PS2 **map_ctrl map** (572 distinct such codes exist across the archive's map art and
> `efb` trees, 459 with a JSON), while the `.ard` code names the **battle-plan area** shared by the
> maps of that area; the engine connects them only through the field's row, never by string. The
> letter / digit resemblance is the PS2 plan's naming convention, not a lookup: reading the code's
> two-digit block as an area letter (`01 → a`, `02 → b`, `10 → j`, `20 → t`; `50`–`52` → `a`–`c`
> again as alternate render sets) puts 420 of the 459 JSON codes in an existing `plan_map` area and
> 227 on an existing field directory — a strong regularity with 39 / 232 exceptions, so it is a
> convention the data mostly follows, not a rule the engine applies.

### What this does and does not establish

> ### AUDIT 2026-09-06 — this paragraph generalises from 11 slots to 63, and the two mechanisms it fuses are disjoint
>
> *`repos-4b`, second pass, hunting the same "rule invoked then not applied" shape.* **The
> observations in §8c are correct and I reproduced them exactly. The conclusion drawn from them is
> not.**
>
> **Measured, by decoding all eleven setters at `0x002383C0` + `0x30`·k:** each reads and writes one
> registry slot, and the eleven cover **`0x02EBF1A8`, `0x1B0`, `0x1B8`, `0x1C0`, `0x1C8`, `0x1D0`,
> `0x1D8`, `0x1E0`, `0x1E8`, `0x1F0`, `0x1F8`** — a contiguous run at the **top** of the span. That
> is §8c's figure and it holds.
>
> **But `each has its own generated setter` is true of ~~11 slots out of 63~~ 12 slots out of 64** *(corrected 2026-10-02, OPUS: setters `00238390`–`002385A0`, and `00236C30+0x401` stores the 64th slot `0x02EBF200`)*, and — the load-bearing
> part — **not one of the eleven is an `.ard` category slot.** The five that
> `BattleData_SetAreaArdSectionCategory` binds are `0x02EBF150`, `0x02EBF168`, `0x02EBF120`,
> `0x02EBF148`, `0x02EBF140` (see the audit note in §2). **The setter family and the area-binder
> family are disjoint sets.** This paragraph joins them in one sentence.
>
> **How the reasoning slips, step by step, because the steps are each reasonable:**
>
> 1. eleven consecutive slots are measured to have generated setters — **correct**;
> 2. *"the registry … is a set of slots that get bound at runtime, one generated binder per slot"* —
>    **generalised from 11 to all 63**;
> 3. *"What binds them"* then cites `FUN_003847B0`, the smallest consumer of **`0x02EBF118`** — a
>    slot **outside the eleven**, so the binder evidence comes from a different family than the one
>    being explained;
> 4. *"the slots are populated by `AreaData_BindAndRebaseSectionDescriptor`"* — asserted for the
>    registry at large.
>
> **Why the corpus cannot object, which is why this needs saying here.** `repos-3f` reports that
> `BattleUnit_ApplyUnitDefinition` touches **eight** registry slots, three of them non-`.ard`
> (`0x02EBF130` ×8, `0x02EBF170` ×4, `0x02EBF190` ×1), using **identical descriptor-lookup code**;
> `repos-1e` reports `BattleStats_Rebuild…` doing the same against `0x02EBF130`. **Both read real
> rows, so no corpus test can separate an `.ard`-backed descriptor from one that is not.** A reader
> who takes this paragraph at face value will treat `0x02EBF130` as area-bound because the lookup
> looks the same.
>
> *CB-11 answered 2026-09-12 (FABLE).* What `[rdi+4]` selects on the `02EBF130` path is the **row
> of the party definition table** — `02EBF130` is `battle_pack.bin`'s directory entry `+0x44`, 40
> rows × 128, names in bank 8 ([the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.10 row 2): the stats record's `u16 +4` is the
> unit's definition id, its high byte `+5` the table (0 party, 1 enemy) and its low byte the row —
> rows 0–16 the characters and guests, 17–25 unnamed, 26 the Chocobo, 27–39 the thirteen Espers
> ([the kind page](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) AL-2). The rebuild's two lookups are the two arms of one switch on `+5`
> (`002FF026`): `02EBF130` × `[rdi+4]` for a party-kind record, `02EBF120` × `[rdi+4]` for an
> enemy-kind one.
>
> **What survives:** ~~eleven~~ twelve slots have generated setters *(corrected 2026-10-02, OPUS: `00238390` is the twelfth, for `0x02EBF1A0`)*; those ~~eleven~~ twelve are mutable and bound at
> runtime; five different slots are bound by the `.ard` category dispatch; `0x02EBF118` has a
> consumer that calls the area binder. **What does not survive is the word *the slots*** — used four
> times in this subsection for four different populations.

**Established, restated with its scope:** ~~*eleven* slots (`0x02EBF1A8`–`0x02EBF1F8`)~~ *twelve* slots (`0x02EBF1A0`–`0x02EBF1F8`) *(corrected 2026-10-02, OPUS: `00238390+0x1A` writes `0x02EBF1A0`)* each have a
generated 39-byte setter and are bound at runtime. *Five* slots (`0x02EBF150`, `0x168`, `0x120`,
`0x148`, `0x140`) are bound by the `.ard` category dispatch at `0x0023A160`. `0x02EBF118` has a
consumer that reaches `AreaData_BindAndRebaseSectionDescriptor`. **These are three findings about
three slot sets, and at least `0x02EBF130`, `0x02EBF170` and `0x02EBF190` belong to none of them.**

> ***AG-2 / the band-shape question ANSWERED 2026-09-22 (FABLE), on
> `OPUS-REQ-FABLE-02EBF000-BAND-SHAPE-BEFORE-DECLARATION` (P1).*** OPUS asked for the slot origin
> and stride *or* a ruling that the band is not one table, before a type is declared over it.
> **The ruling is that it is not one table, and the three findings above are three of FIVE
> populations.** Method: every rip-relative reference into `0x02EBE000`–`0x02EC0800` from **all
> 38,161 listed bodies plus the 508,801 bytes of `.text` no listed body covers**, classified per slot
> into read / direct write / address-taken. *Controls: the sweep reproduces `0030C6E3`'s reference to
> `0x02EBF130`, read by hand for `c479c04da`; and `0x02EBF130`, which the binder installs, returns
> **zero** direct writes, which is what makes a non-zero count elsewhere mean something.*
>
> **1. The origin and stride are confirmed, and they are not evidence of a table.** The regular
> 8-byte grid runs `0x02EBF008`–`0x02EBF200`, **reproducing AG-3's "starts cold at `0x02EBF008`"
> independently** (`0x02EBF000` is one `movss` float, `0x02EBF004` is referenced by nothing) and
> **agreeing with the count of 64 that section 2 corrected earlier the same day**, of which 63 are
> referenced. *A uniform 8-byte spacing is what a run of adjacent pointer globals looks like; it is
> not a stride until something indexes it.*
>
> **2. `0x02EBF198` is referenced ZERO times** — no read, no write, no `lea`, in listed or unlisted
> code — **which section 8c above had already established, with its own control, and this sweep
> reproduces from a different instrument rather than discovers.** *Amended 2026-09-22 (FABLE): as
> first published this paragraph read as a new finding and cited the count as 63. Both were wrong
> about this page — I had corrected the count to 64 myself, hours earlier, on OPUS's request.* What
> the sweep adds is what the hole SEPARATES: the populations either side of it are bound by
> different mechanisms.
>
> **3. Below the hole: 34 slots installed STRAIGHT-LINE, and this is the population `0x02EBF130` and
> `0x02EBF170` belong to.** The binder `0x00236C30` — already identified under **J-B** as the loader
> id `0x13` `"STATIC"` delivery callback — contains **~~34~~ 33 `lea <slot>` / `movsxd rdx, [rax + <field>]`
> / `call 0x003845F0` triples in a row, with ~~34~~ 33 DISTINCT field offsets and no loop**, plus two `call 0x003846F0` triples *(corrected 2026-10-02, OPUS: 33 `call 0x3845f0` and 2 `call 0x3846f0` sites in `00236C30`, the first at `00236C30+0x56` and `00236C30+0x109`)*. The directory
> field offsets **ascend** (`+0x10`, `+0x14`, `+0x18`, `+0x1C`, `+0x24`, `+0x28`, …, `+0x118`) while
> the slots they land in **do not** (`0F0B8`, `0F0A8`, `0F0B0`, `0F0C0`, `0F0E0`, `0F108`, `0F160`,
> `0F110`, `0F038`, `0F130`, …). *That is the whole ruling in one sentence: the code walks an ORDERED
> directory record and scatters each field to an UNRELATED global. A table would name one field
> offset and scale an index.* **Controls, against figures this page already carries and this reading
> did not use:** `0x02EBF130` pairs with `+0x44` and `0x02EBF108` with `+0x28` — exactly the
> `battle_pack.bin` directory entries CB-11 and §2.10 record.
>
> **So the type to declare is the DIRECTORY RECORD, not the band.** It is the thing with ordered
> fields; the band is ~~63~~ 64 separately-named globals that happen to be adjacent *(corrected 2026-10-02, OPUS: `0x02EBF008`–`0x02EBF200`, the extent §2 corrected)*.
>
> **4. Five more binders, which is why "the binder" was singular too long.** Besides `0x00236C30`'s
> 34, the address of a lower-run slot is taken in exactly five other bodies:
> `BattleData_SetAreaArdSectionCategory` (`0x0023A160`) holds **five** — *independently the same five
> the `.ard` finding above names* — and `0x003847B0`, `0x00237FC0`,
> `GambitTargetDefinition_BindAndBuildMenuLookup` (`0x00238880`) and `0x00238160` hold one each.
>
> **5. Above the hole: a genuinely INDEXED array, and it has twelve entries, not eleven.**
> `0x00233E00` bounds a caller-supplied `cl` at `0xB` and reads **`[0x02EBF1A0 + cl*8]`** — the one
> place in the image where a band address is scaled by an index — then counts non-null entries in an
> unrolled loop stepping `0x30` from `0x02EBF1A8`, ending on `lea r11, [0x02EBF208]`, and answers
> *"fewer than six occupied"*. **That walks `0x02EBF1A0`–`0x02EBF1F8` = 12 slots.** ⚠ **The paragraph
> above says eleven, `0x02EBF1A8`–`0x1F8`; it is twelve, and `0x02EBF1A0` is entry 0.** The generated
> setters settle it from the other side: they sit at a regular `0x30` spacing and there are **twelve**
> — `0x00238390` writes `0x02EBF1A0`, then `0x002383C0`, `0x002383F0` … `0x002385A0` write `0x1A8`
> through `0x1F8`. *Two independent measurements — the bound on `cl` and the setter count — give
> twelve. `0x02EBF1A0` was missed because it is also the base every indexing caller `lea`s, so its
> setter is easy to read as the base's own site.*
>
> **6. Eighteen slots are DIRECTLY written, which narrows J-B rather than contradicting it.** J-B
> says *"the registry band has no direct writer — every slot is stored through the binder"*. That
> holds for the binder-installed population — **46 of the 64 grid positions take no direct write at
> all** — but twelve of the eighteen that do are the generated setters of §5, and six more are
> ordinary globals sharing the run: `0x02EBF158` (`0x00238660`), `0x02EBF178` (`0x00324510`),
> `0x02EBF180` and `0x02EBF200` (written by `0x00236C30` itself, not through the installer),
> `0x02EBF190` (two sites) and **`0x02EBF188`, written 93 times from 40 different functions and read
> through a rip-relative operand never** — *a last-value global, not a registry slot.* **J-B's claim
> should be read as scoped to the slots the binder installs, which is where its own evidence lies.**
> *I first measured 26 direct writes at `0x02EBF170`; they are 26 `cmp`, which reads its first
> operand. The count above uses an explicit writing-mnemonic set and the `0x02EBF130` control.*
>
> **7. One slot is installed by nothing, and it makes a class permanently empty.** `0x02EBF0D0` has
> **no `lea` and no direct write anywhere in the image** — alone among the lower run — and exactly one
> reader: `BattleEncodedId_IsValidForClass` (`0x00322C50`) at `0x00322DFE`. That switch arm loads the
> slot, and on null takes `0x00322E1D lea ecx, [rax + 0x7000]` **with `rax` still zero**, so the
> class's id range is `[base, base + 0)`. **Nothing in that class is ever valid, and the arm reads as
> live code.** *Bounded: the absolute-pointer test that would have looked for a data-section
> initialiser is NOT sensitive here — the installed control `0x02EBF130` also returns zero — so this
> rests on the code sweep alone, which is the same evidence that establishes the other 34.*
>
> **What this does NOT answer: AG-2's actual question, which is the slots' IDENTITY.** The map above
> is a map of *binding mechanisms*, and it gives 34 of them a directory field offset to be identified
> from. **AG-2 stays open**, now with a stated next step: name the `battle_pack.bin` directory fields
> in offset order. The instruments are `Tools/work/FABLE/pub140-scratch/bandscan.py`,
> `bandclass.py`, `bandwrite.py` and `bandmap.py`, each carrying its own control.
> *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale. `AG-2` was ANSWERED on 2026-09-26 in §7: all 64 slots have
> an identity in `ag2-slot-identity.tsv`.)*

**Not established:** that *every* slot is rebound on *every* area transition — the cadence, **AG-11**
> *AG-11 answered 2026-09-12 (FABLE), from the three populations this audit separated:* **no —
> only the five `.ard` slots**, and on every *area* change rather than every map: the area loader
> unbinds and rebinds `0x02EBF150` / `0x168` / `0x120` / `0x148` / `0x140` whenever the outer area
> folder changes, and sets them null when the new area ships no `.ard` ([the area-file loader](VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md) §1). The
> ~~eleven~~ twelve setter slots (~~`0x02EBF1A8`–`0x1F8`~~ `0x02EBF1A0`–`0x1F8`) *(corrected 2026-10-02, OPUS: `00238390+0x1A` writes `0x02EBF1A0`)* are bound by their own runtime setters on their own
> cadence, `0x02EBF178` is published by the main loop (AG-4), and every other slot — the
> `battle_pack.bin` tables — is bound **once**, when the STATIC delivery callback runs `00236C30`
> at boot, and never rebound ([the row-lookup contract](CONTRACT-authored-table-row-lookup.md) §14, J-B). So a reconstruction rebinds five slots per
> area and nothing else per transition.
— and, added by this audit, **that every slot is an area-data section descriptor at all.** The
second is the more dangerous of the two, because the first is flagged as unknown and the second read
as settled. *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: both are settled. The first is `AG-11`, answered above.
The second is answered no by `AG-5` and `AG-2` (§7): five cells hold no authored table, and `0x02EBF180` and
`0x02EBF158` use other headers.)*

## 8d. Reopened 2026-09-02 - the binder read, partially

`AreaData_BindAndRebaseSectionDescriptor` (`003845F0`) and its caller were decompiled. **Both bodies
come back heavily elided** - the empty-`if` artifact documented elsewhere in this database - so the
section descriptor layout is *not* recovered here. What the signatures and locals do establish:

```c
void AreaData_BindAndRebaseSectionDescriptor(
        FFXII_ArdSectionDescriptor_Partial *section_base,
        ... *out_bound_section)
{
    *out_bound_section = section_base;      // the bind itself
    if (section_base != NULL) { ... }       // elided
}

void BattleData_SetAreaArdSectionCategory(int section_category, int section_image_address)
{
    if (section_category == 0) { ... }
    if (section_category == 1) { ... }
    if (section_category == 2) { ... }
    if (section_category != 3) { ... }
    AreaData_BindAndRebaseSectionDescriptor(...);
}
```

**~~Four~~ Five `.ard` section categories** (`0`, `1`, `2`, `3`, `4`) *(corrected 2026-10-02, OPUS: `0023A160` dispatches categories 0 to 4, and category 4 binds `02EBF140` at `0023A160+0x18`; the audit note in §2)* are dispatched explicitly, and the section is
passed as an **image address**, not a pointer - which is the same encoding the row RVAs use.

The binder's local variables are typed `runtime_pointer_low32` and `encoded_image_address`,
consistent with an image-address-to-pointer conversion happening inside the elided region.

`Navigation_BindAndRebaseDataset(FFXII_NavigationDatasetHeader_Partial *dataset)` is the parallel
binder for navigation data, with the same shape.

**What is deliberately not claimed:** the `FFXII_ArdSectionDescriptor_Partial` layout. The type name
is Ghidra's (tier 3) and the body that would prove its fields is elided. Recovering it needs
disassembly rather than decompilation. **AG-12.**

> *AG-12 answered 2026-09-12 (FABLE) — the binder read whole* (`AreaData_BindAndRebaseSectionDescriptor`,
> `003845F0`, 252 B). `bind(slot, desc)`: `*slot = desc` (`003845F4`); if `desc` is null, done.
> Otherwise every non-zero field below is **rebased by adding the descriptor's own address** —
> the fields are image-relative offsets inside the section:
>
> | descriptor | rebase | site |
> |---|---|---|
> | `+0x0C` u32 | `+= desc` | `00384600`–`0038460E` — the row array (the contract's `+0x0C` reference) |
> | `+0x10` u32 | `+= desc` | `00384614`–`0038461E` |
> | `+0x18` u32 | `+= desc` | `00384625`–`0038462F` |
> | `+0x1C` u32 | `+= desc` | `00384636`–`00384640` |
> | `+0x14` u32 | `+= desc` ~~, then **resolved** through `0020E620` and stored back~~ giving M, then **encoded** by `0020E620` (M minus the low DWORD of `01F83530`) and that encoded DWORD stored back, even when M is 0 (`00384647`–`00384662`); if M != 0 the sub-directory `{u16 count; u32 entry[count + 1]}` is reached by decoding the stored value with `0020E600` (zero-extend + the full QWORD `01F83530`), and its entries are each rebased by ~~`desc`~~ **M** — the first `count` through the child binder `003846F0(&entry, entry + M, 0)`, the last in place (`00384680`–`003846C7`) *(corrected 2026-10-02, OPUS, on FABLE's review of ASTRA `ov42-action-table-binding`: `0020E620` is the encoder, not a resolver; EBP = M at `003845F0` + 0x6B feeds both the child argument + 0xB9 and the in-place add + 0xC9)* | |
>
> `+0x04` (count) and `+0x08` (stride) are not ~~touched~~ written by any of the binder's own stores — they are values, not offsets. *(narrowed 2026-10-02, OPUS, on FABLE's review of ASTRA `ov42-action-table-binding`: that is the direct store footprint, not whole-call preservation; a nested directory overlapping the header can write them through the in-place add, e.g. a count-0 directory at `desc + 4` adds M to `desc + 8`.)* So the
> descriptor is `{ +0x04 count, +0x08 stride, +0x0C rows, +0x10, +0x14 sub-directory, +0x18, +0x1C }`
> with five relocatable fields, one of which is a nested table of relocatable entries.

## 9. Related

- [`../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md`](../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md) — slot `0x02EBF0C0`, read in full
- [`../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md`](../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md) — slot `0x02EBF0F8`
- [`../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`](../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) — slot `0x02EBF160`
- [`resource-section-addressing.md`](resource-section-addressing.md) — the `ImageAddress_ResolveRuntimePointer` mechanism
- [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md) — the shared-header entry

## 8c. Falsification pass 2026-09-02 — the `02EBF178`/`02EBF188`/`02EBF198` unreferenced-slot claim is overturned

**Attack chosen.** The sharpest checkable claim here was *"scanning `.text` finds **60 of the 63**
slots referenced"*, naming `0x02EBF178`, `0x02EBF188` and `0x02EBF198` as having **no** code
reference. A claim of absence is falsified by a single counter-example, and the original instrument
was a **load scan** — so the killer looked for was a slot referenced by something that is not a load.

**Result: OVERTURNED on two of the three.** A full reference census over the span (every reference
Ghidra records, classified read / write / data, two slots either side of the stated bounds):

| Slot | Document said | Census found |
|---|---|---|
| `0x02EBF178` | no reference | **2 references — both writes, no reads** |
| `0x02EBF188` | no reference | **93 references — all writes, no reads** |
| `0x02EBF198` | no reference | **no reference** ✅ correct |

So **62 of 63 slots are referenced**, not 60, and exactly one slot is genuinely dark.

**Why the error was reachable — and why it is familiar.** A scan for `MOV`/`LEA` *loads* sees reads.
A global that is only ever written is invisible to it, and both missed slots are **write-only**.
This database has already recorded this exact lesson once, in
[`../21-RNG-And-Determinism/rng-streams.md`](../21-RNG-And-Determinism/rng-streams.md) §8b: *"the
right question for a shared global is who **writes** it, not who calls its accessor."* That was
written after a call-edge census missed seven inlined consumers. **The same instrument-shaped blind
spot produced a different wrong answer in a different document**, which is the strongest argument
yet that the lesson belongs in the evidence standard rather than in one document's footnote.

### The census also shows the span is not uniform

Reference *signature* changes partway through the array, and the change is sharp:

| Range | Signature | Reading |
|---|---|---|
| `0x02EBF008` – `0x02EBF170` | many reads + exactly **one** `LEA` (address taken once, by the binder), **no writes** | the pointer registry proper — **46 slots** |
| `0x02EBF178` – `0x02EBF1A0` | writes present, reads sparse or absent | ~~not pointer slots~~ — corrected 2026-09-11: `178`, `180` and `1A0` hold pointers (*the tail read*, below) |
| `0x02EBF1A8` – `0x02EBF1F8` | uniform **2 reads + 1 write** each, `CMP` common | ~~a run of scalar state, not tables~~ — corrected 2026-09-11: ~~the completion words of~~ the loaded-board pointers of the twelve board requests (*the tail read*, below) *(corrected 2026-10-02, OPUS: the setters store the buffer address `00384420+0x99` puts in the descriptor's `+8`)* |

Two documented exceptions inside the clean run: `0x02EBF0D0` (one read, no `LEA`) and `0x02EBF158`
(one write).

**This extends the §8b correction rather than replacing it.** §8b established that *one* slot
(`0x02EBF190`) is a runtime state block rather than a table. The census shows that was not an
isolated intruder: **the upper third of the claimed span is a different class of global entirely**,
and the authored-table pointer registry proper is the `0x02EBF008`–`0x02EBF170` run. The headline
should be read as *"most authored content is reached through one array of ~46 pointers, which sits *(answered: see AG-2's ANSWERED 2026-09-26 - every one of the 64 slots has an identity; 2026-10-02, OPUS)*
at the head of a larger mixed global block."*

**Bounds confirmed at the bottom, fuzzy at the top.** `0x02EBEFF8` and `0x02EBF000`, immediately
below the array, are accessed with `MOVSS` — they are **floats**, so the lower bound is real.
Above, `0x02EBF200` has one write and `0x02EBF208` one `LEA`, while `0x02EBF210` and `0x02EBF218`
have nothing; the upper bound is a fade rather than an edge.

### Independent corroboration of the action table

Slot `0x02EBF138` is documented as the **action definition table, ids `0`..`0x21E` (543)**. It
carries ~~**720 references**~~ **723 references** *(corrected 2026-10-02, OPUS: 722 reads and one `lea` over every function body, the count the slot census and the upper-slot pass below give)*, the second-highest in the array. Separately, and for unrelated reasons,
`BattleUnit_CommitAction` (`0030F760`) was read on 2026-09-02 during the AH-6 pass and gates its
action id with:

```c
if (action_id < 0x21f) { ... }
```

`< 0x21F` is exactly `0..0x21E`. **The bound was confirmed from a different subsystem, by a read
undertaken for a different reason** — which is the strongest form this database has for a claim of
this kind.

### Reference census, top slots

| Slot | Refs | Character |
|---|---:|---|
| `0x02EBF138` | ~~720~~ 723 *(corrected 2026-10-02, OPUS: 722 reads and one `lea`)* | action definitions |
| `0x02EBF190` | 318 | runtime state block (§8b) |
| `0x02EBF0F8` | 272 | equipment definitions |
| `0x02EBF118` | 130 | — |
| `0x02EBF188` | **93, all writes** | **not a table** |
| `0x02EBF130` | 83 | — |
| `0x02EBF040` | 111 | — |

**Note on `0x02EBF188`.** Ninety-three direct writes and zero direct reads is a real signature, but
it is not proof nothing reads `02EBF188`: a read reached through a base register (`LEA` the array head, then
`MOV [base + 0x180]`) would not be attributed to this address. The writes are direct and certain;
the absence of reads is instrument-limited, and is recorded as such rather than as a finding.

## `BattleEncodedId_IsValidForClass` read — 2026-09-03, session `repos-78`

The caution above says this function *"validates ids against many different tables, so its presence
says a slot is an id-indexed table and nothing more."* **That was the right call on the evidence
available, and it can now be sharpened rather than overturned:** the function was on the *leaned on
and never opened* cut — three documents naming it, none reading it — and it is read here.

**Extent checked**: 253 instructions, ends `ret` at `00323050`, no `jmp` leaves the extent.

### It is a 32-way dispatch on the class argument

```asm
00322C5A  lea  eax, [rcx - 1]                      ; class - 1
00322C5F  cmp  eax, 0x1f                           ; classes 1 .. 32
00322C62  ja   fail
00322C72  mov  ecx, dword ptr [rdi + rax*4 + 0x203054]
00322C79  add  rcx, rdi                            ; rdi = 00120000, the image base
00322C7C  jmp  rcx
```

**A 32-entry jump table at `00323054`**, immediately after the function's `ret` — one case per class.

### The validity rule is a bound check against the slot's own count

Every case resolves to a shared tail:

```asm
0032302C  mov  edx, eax        ; eax = 0
0032302E  cmp  ebx, edx        ; ebx = the id
00323030  jl   fail            ; id < 0
00323036  lea  eax, [rcx - 1]  ; rcx = the slot's count
00323039  cmp  ebx, eax
0032303B  jg   fail            ; id > count - 1
00323041  mov  eax, 1
```

**`valid ⇔ 0 ≤ id < count`, where `count` is the dword at `slot pointer + 4`** — the same header field
this document's §2 describes. **A null slot pointer yields 0**, so an unloaded table makes every id
invalid rather than crashing.

### The complete class → slot map

| class | slot | | class | slot | | class | slot |
|---:|---|---|---:|---|---|---:|---|
| 1 | `02EBF130` + re-dispatch | | 12 | `02EBF0D0` | | 23 | `02EBF110` |
| 2 | `02EBF130` | | 13 | `02EBF090` **+ `02EBF088` + `02EBF080` + `02EBF078`** *(corrected 2026-10-02, OPUS: `00322C50+0x21E` reads the fourth)* | | 24 | `02EBF110` |
| 3 | `02EBF120` | | 14 | `02EBF070` | | 25 | `02EBF038` |
| 4 | `02EBF150` | | 15 | `02EBF068` | | 26 | `02EBF118` |
| 5 | `02EBF100` | | 16 | `02EBF060` | | 27 | `02EBF050` |
| 6 | `02EBF0F8` | | 17 | `02EBF0C8` | | 28 | `02EBF0B0` |
| 7 | `02EBF098` | | 18 | `02EBF058` | | 29 | `02EBF040` |
| 8 | `02EBF0F0` | | 19 | `02EBF138` | | 30 | `02EBF068` |
| 9 | `02EBF0E8` | | 20 | `02EBF138` | | 31 | `02EBF068` |
| 10 | `02EBF0E0` | | 21 | `02EBF128` | | 32 | `02EBF038` |
| 11 | `02EBF0D8` | | 22 | `02EBF110` | | | |

**Sharing is real and asymmetric:** `02EBF110` serves classes 22–24, `02EBF068` serves 15, 30 and 31,
`02EBF138` serves 19 and 20, `02EBF038` serves 25 and 32. **Class 13 is composite** — it reads ~~three~~ four
slots *(corrected 2026-10-02, OPUS: `02EBF078` too, read at `00322C50+0x21E` and summed at `00322C50+0x22D`)* and a `0x8000` constant, so its id space is partitioned across tables rather than bounded by one.
**Class 1 additionally calls `00309440` and re-enters the dispatch**, the function's only loop.

### What this does and does not license

**The caution stands where it was aimed.** Knowing a slot appears in this function still does not say
what it contains.

**But it is no longer "nothing more":** each slot now carries **a stable class number that the rest of
the engine uses to name it**. And where a *second, independent* document records what a caller passes
as the id, the pair identifies the table:

| chain | conclusion |
|---|---|
| `battle-command-availability-and-reason-codes.md` reads `IsValidForClass(0x14, actionId)`; class `0x14` = 20 → `02EBF138` | **`02EBF138` is indexed by action id** |
| `spawn-placement-and-retirement.md` reads `IsValidForClass(0x17, i)` then a selector lookup; class `0x17` = 23 → `02EBF110` | **`02EBF110` is indexed by a definition-selector index** |
| `two-layer-effect-model.md` §11 reads `IsValidForClass(0x1D, …)` gating status side effects; class `0x1D` = 29 → `02EBF040` | **`02EBF040` is indexed by status id** |

**That is two sources per row — a class number from this function and an argument name from a document
that read its caller** — which is a different and stronger thing than labelling a slot by a consumer
that touches everything. `02EBF138` is also one of the two heavyweights named above at **128
referencing functions**, and "the action-id table" is a plausible fit for that fan-in.

**Disposition of the `verify_doc_addresses` review flag.** `00323054` is cited as a `.text` address
that is not a function entry. **Confirmed legitimate:** it is the jump table itself, four bytes past
this function's `ret` — the case the checker asks to have confirmed. The case addresses cited above are
interior addresses of `00322C50` for the same reason: switch arms are not functions.

### What is not established

- [x] **UQ-80.** The contents of the other 26 slots. **A class number is an identity, not a description.**
      ***SUPERSEDED 2026-09-27 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling (FABLE-REQ-FRONTIER-UQ80-CLASS1; batch-K-scope-rulings.md Extension 2026-09-27c):** `uq80_coverage.py` measures all 23 st2e tables of the shipped `battle_pack.bin` - 15 fully mapped, the residue 60 bytes in 8 tables with every offset in `uq80_manifest.tsv` ([record](../_index/candidates/uq80-table-field-coverage/README.md)). The residue is the named follow-on, not a reopen.*
      *Narrowed 2026-09-15 (FABLE): every slot now has a source, and 23 of the class slots an authored file name.*
      - **How the names are joined.** Two maps already published compose with one fact:
        - [the row-lookup contract](CONTRACT-authored-table-row-lookup.md) §7a gives `00236C30`'s 35 registrations,
          `battle_pack.bin` directory offset → slot;
        - the manifest at `01E4D830` gives names;
        - **manifest slot *k* is pack entry *k*, directory `+4 + 4k`, in all nine packs**
          ([the VBF page](VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md), UQ-73).
        Shapes are the `us` pack's `st2e` count × record size (`work/FABLE/drift4/uq80_slot_names.py`).

        | slot | classes | pack entry | file | shape |
        |---|---|---|---|---|
        | `02EBF130` | 1, 2 | `+0x44` | `chr_data` | 40 × 128 |
        | `02EBF100` | 5 | `+0x4C` | `dougu_data` (items) | 64 × 12 |
        | `02EBF098` | 7 | `+0x84` | `eventitem_data` | 512 × 10 |
        | `02EBF0F0` | 8 | `+0x78` | `maho_data` (magicks) | 81 × 8 |
        | `02EBF0E8` | 9 | `+0x7C` | `waza_data` (technicks) | 24 × 8 |
        | `02EBF0E0` | 10 | `+0x24` | `gambit_data` | 40 × 64 |
        | `02EBF090` / `088` / `080` | 13 | `+0x88` / `+0x8C` / `+0x90` | `m_daiji` / `g_daiji` / `q_daiji` | 64 / 32 / 416 × 10 |
        | `02EBF070` | 14 | `+0x98` | `eis_data` | 512 × 12 |
        | `02EBF068` | 15, 30, 31 | `+0x9C` | `questreward_data` | 256 × 12 |
        | `02EBF060` | 16 | `+0x74` | `price_data` | 128 × 4 |
        | `02EBF0C8` | 17 | `+0x6C` | `menkyo_data` | 32 × 8 |
        | `02EBF058` | 18 | `+0xE8` | `horidashi` (the bazaar, AB-2) | 128 × 36 |
        | `02EBF128` | 21 | `+0x48` | `comac_data` | 21 × 4 |
        | `02EBF110` | 22, 23, 24 | `+0x30` | `mgccategory_data` | 5 × 4 |
        | `02EBF038` | 25, 32 | `+0x34` | `license_data` | 361 × 24 |
        | `02EBF050` | 27 | `+0xA8` | `attribute_data` | 8 × 2 |
        | `02EBF0B0` | 28 | `+0x18` | `sobicategory_data` | 32 × 4 |
        | `02EBF040` | 29 | `+0xEC` | `ability_data` (augments) | 129 × 8 |

      - **Class slots with another loader.**
        - Three are `battle_pack.bin` entries registered outside `00236C30`: `02EBF0F8` (class 6) is `+0x38` `eitm_data`,
          whose header `+0x18` heap `00238160` rebases (AY-11); `02EBF118` (class 26) is `+0x40` `status_data`; and
          `02EBF138` (classes 19, 20) is `+0x3C` `action_data` ([the action definition row](../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md)).
        - Four are not pack entries: `02EBF150` (class 4) and `02EBF120` (class 3) are `.ard` slots 0 and 2; `02EBF0D8`
          (class 11) is the gambit target definitions; `02EBF0D0` (class 12) is §`0x02EBF0D0` above.
      - **Registered with no class**, named the same way: `02EBF018` `battle_message`, `02EBF0B8` `damagemp_data`,
        `02EBF0A8` `jochumodel_data` (empty), `02EBF0C0` `drop`, `02EBF108` `hpmpbase_data`, `02EBF160` `commandpack`
        (AY-12), `02EBF020` `tutorial_data`, `02EBF0A0` `yugoyaku_data`, `02EBF078` `s_daiji_data` (empty) *(corrected 2026-10-02, OPUS: it is class 13's fourth table, read at `00322C50+0x21E`)*, `02EBF048`
        `shoki_data`, `02EBF028` `savemember_data`, `02EBF030` `saveparty_data`, `02EBF170` `word` (the text banks),
        `02EBF010` `move_support` and `02EBF008` `movie`.
      - **The names corroborate the roles already read.** Every table whose role this database had established lands on
        the matching file:
        - from pages elsewhere: party rows on `chr_data`, licence nodes on `license_data` (361), augments on
          `ability_data` (129), the bazaar on `horidashi` (128), gambit presets on `gambit_data`, the text banks on `word`;
        - from the consumer sweep of [the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)
          §2.10 (2026-09-11), which named the unclaimed slots by their readers:
          - the concurrence selection table on `yugoyaku_data`;
          - the starting inventory grants on `shoki_data` (*shoki*, initial);
          - the per-level HP / MP growth on `hpmpbase_data`;
          - the scripted command-list presets on `tutorial_data`;
          - the SetSaveData presets on `saveparty_data` / `savemember_data`;
          - the per-field locomotion spacing on `move_support`;
          - the clock-driven schedule on `movie`;
          - the weapon-class map `02EBF180` (directory `+4`) on `WepJob_Matrix`, manifest slot 0;
        - and on other pages: the loot chance profiles on `drop`
          ([loot drops](../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md)) and the damage-to-MP table on
          `damagemp_data` ([where MP comes from](../10-Status-Periodic-Terminal/where-mp-comes-from.md)).
        Those roles were read from code, so each name-to-role match is an independent confirmation of this join.
      - **Still open:** a file name is not a field map. This narrowing adds names; it does not audit each table's field
        coverage. Whatever row meaning no page reads, for example `comac_data` and `mgccategory_data` beyond their class
        chains, stays open.
      ***Narrowed 2026-09-27, FABLE, Claude Opus 5.5: the coverage is now measured by a maintained instrument, and the residue is named and counted.** `uq80_coverage.py` reads the 23 `st2e` tables of the us `battle_pack.bin` (the 20 sections above, plus `eitm_data`, `status_data` and `action_data`). For each table it counts which record bytes a page or this pass gives a meaning; `uq80_manifest.tsv` records each field's source, a page or the reader instruction. 15 of 23 tables are fully mapped, `comac_data` and `mgccategory_data` among them. The residue is **60 bytes in 8 tables**: `chr_data` 11, the three key-item tables 2 each, `menkyo_data` 1, `eitm_data` 19, `status_data` 14, `action_data` 9. The run prints every offset. The four non-pack class slots are named, not measured. "No reader" is bounded by the instrument: row pointers handed to callees are not followed. [Record, instrument and field maps](../_index/candidates/uq80-table-field-coverage/README.md).*
- [x] ~~How class 13 partitions its id space across three slots, and what `0x8000` marks.~~
      **ANSWERED 2026-09-13 (OPUS) — but the checkbox was STALE, and the four-slot reading is this
      page's own, not mine.** §`0x02EBF078` above already names the function
      (`BattleEncodedId_IsValidForClass`), lists all four slots with this same instruction table,
      states the null-guard, and routes the disagreement with the class registry as
      `OPUS-CONTRA-CLASS13-FOURTH-TABLE`. **I re-derived it from the binary without checking whether
      a later section had superseded the bullet — the fourth stale checkbox found on this page
      today, and the second one I answered by duplicating work already done.** What follows is kept
      only because the arithmetic and the `0x8000` reading are stated here in one place. The arm at
      `00322E28`–`00322E8C` reads `02EBF090`, `02EBF088`, `02EBF080` **and `02EBF078`**, takes each
      one's **`+0x04` field — the row count this page's own §4 header convention names** — and
      null-guards every one of them to `0`:

      ```asm
      rcx = [02EBF090] ; r9d  = rcx ? [rcx+4] : 0      ; slot A row count
      rcx = [02EBF088] ; r10d = rcx ? [rcx+4] : 0      ; slot B
      rcx = [02EBF080] ; r8d  = rcx ? [rcx+4] : 0      ; slot C
      rcx = [02EBF078] ; eax  = rcx ? [rcx+4] : 0      ; slot D
      eax = eax + r8d                                  ; D + C
      ecx = r9d + 0x8000                               ; A + BASE
      eax = eax + r10d                                 ; + B
      ecx = ecx + eax                                  ; 0x8000 + A + B + C + D
      ```

      **So class 13 does not partition its id space — it CONCATENATES four tables.** The arm computes
      one extent, `0x8000 + Σ row counts`, and an unbound slot contributes nothing rather than
      faulting, so the span shrinks cleanly when a table is absent.
      **`0x8000` is the BASE of class 13's id space** — consistent with §`0x02EBF078`'s note that
      the class registry names its sub-tables as key items at `0x8000`, `0x8040` and `0x8060` — and
      it appears twice in the arm for that reason: once as `mov edx, 0x8000` at `00322E31`, handed to the common tail as the class's
      starting id, and once as `lea ecx, [r9 + 0x8000]` at `00322E80`, biasing the running total. It
      is not a flag bit and marks nothing about an individual id — **it is where this class's ids
      begin.** The next arm sets `edx, 0x9000`, which is the same convention one class along.
      **What this does not say:** the *order* the four tables occupy within the span. The arm needs
      only the total, so nothing here fixes whether A, B, C, D is the id order or merely the
      summation order.
- [x] ~~What `00309440` returns for class 1, and why exactly one class re-dispatches.~~
      **ANSWERED 2026-09-13 (OPUS): it returns `(id >> 12) + 5`, and class 1 re-dispatches because
      class 1 is an ALIAS — its ids carry their real class in the top nibble.** All 30 bytes:

      ```asm
      00309440  movzx eax, cx           ; the id
      00309443  shr   eax, 0xC          ; its TOP NIBBLE
      00309446  cmp   eax, 0xE
      00309449  ja    0030945A          ; nibble 15 -> -1
      0030944B  imul  rcx, rax, 0x58    ; 0x58-byte records
      0030944F  lea   rax, [01EEBCF8]
      00309456  mov   eax, [rcx + rax]  ; the record's FIRST dword
      00309459  ret
      ```

      **The table is inside `.data`'s raw image, so its contents are readable, and the first column
      is a straight line.** Every record's first dword is its own index **plus five**:

      | nibble | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
      |---|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
      | returns | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |

      So the lookup is a **bias**, not a mapping: `00309440(id)` = `(id >> 12) + 5`, range **5..19**,
      with `-1` for a top nibble of 15. The 0x58-byte records carry more — their second dwords are
      `0x40`, `0x1A4`, `0x200`, `0x51`, `0x18`, `0`, `0x100`, `0`, `0x200`, `0x200`, `0x100`, `0`,
      `0x20`, `0x80`, `0x0FFF` — but only the first is read here.
      **THAT IS WHY EXACTLY ONE CLASS RE-DISPATCHES.** The dispatcher's own class field ranges past
      32, so it is not the top nibble; `00309440` reads a *different* field of the same id. **Class 1
      is the escape hatch**: an id filed under class 1 carries its true class in bits 12–15, and the
      loop re-enters with `nibble + 5` — landing in **classes 5 through 19**. No other class needs
      the loop because no other class aliases.
      **What this does not say:** why the bias is five, and whether nibble 15 reaching `-1` is a
      reserved value or an error path. The record's remaining `0x50` bytes are unread.
      *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: this belongs to another page.
      [The encoded-id class registry](../00-Engine-Core-Runtime/the-encoded-id-class-registry.md) owns the fifteen
      `0x58`-byte nibble records at `01EEBCC0`, of which `01EEBCF8` is the `+0x38` class word. It reads the records'
      count `+0x3C` and their handlers, and its `00309EC0` citation reads nibble 15: an id with
      `(id & 0xF000) > 0xE000` is refused there with −1, so it is an invalid id, not a class. Why the bias is five is a
      design choice no reader records.)*
- [x] **UQ-81.** Whether classes sharing a slot differ elsewhere — **this function treats 22, 23 and 24
      identically**, so the distinction, if any, lives in their callers.
      **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): yes, and the witness is the query-record filler.** `0031C5D0`'s
      32-entry jump table (decoded from `0031E598`) sends classes 22 and 23 to the same arm, `0031DD9E`, which validates
      the id and returns 0 with nothing filled. Class 24 goes to its own arm, `0031DDBA`, which validates the id, then
      reads row word `+2` of the `02EBF110` table (`0031DE0B`–`0031DE15`) and resolves it through the text banks
      `02EBF170`. That is the magick school's name. So one table and one bound serve three classes, and only class 24 has
      a name output. Other class-keyed consumers were not censused; this establishes that the classes differ, not every
      place where they do.

---

## Slot 37 (`0x02EBF130`) and slot 49 (`0x02EBF190`) read together — 2026-09-04

**Both are consumed by the same loop in `BattleUnit_ApplyUnitDefinition` (`0023A570`), against the
same index**, which is why they are written up together rather than separately.

`0x02EBF130` carries **83 references across 23 functions** — the reference count this document
already recorded, now confirmed instruction-by-instruction rather than from a database.

### What slot 37 holds: a header, not an array

```
0023AA66  mov   rdx, [0x02EBF130]      ; the slot -> a pointer
0023AA6D  test  rdx, rdx               ; NULL-CHECKED
0023AA70  je    0x23aaa8               ; absent -> esi = 0 and the walk continues
0023AA72  mov   ecx, [rdx + 0x0C]      ; u32 at +0x0C
0023AA75  call  0x20E600               ; -> a base value in eax
0023AA95  movzx esi, word ptr [rdx+8]  ; u16 at +0x08
0023AA99  imul  esi, r12d              ; * the unit index
0023AA9D  add   esi, eax               ; + the base
```

So slot 37 points at a small header with **`+0x08` u16** used as a **per-unit multiplier** and
**`+0x0C` u32** passed to `0x20E600` to obtain a base. The product `esi = hdr[+8] * index + base`
is an offset or id computed **per unit**.

**The table is optional.** `0023AA6D` null-checks it and `0023AAA8` falls through with `esi = 0`, so
a build without this table still runs. **That is a loader-contract fact and it is unusual enough to
be worth a modder's attention.**

### ⚠ Corrected 2026-09-13: slot 49's 456-byte records are RUNTIME stats, not authored rows

**The stride and header below are right. Calling the records *authored data* was not** — and this
page is the authored-data registry, so the framing is the claim. Raised by ASTRA from live capture
(EXP-081) and re-derived here from the shipping image.

The same array has a **dedicated accessor that names what it is**:

```asm
BattleStats_GetByBattleSlotIndex  00320A40          ; 33 bytes, the whole function
00320A40  cmp   cl, 0x27                            ; slot must be 0..39
00320A43  jbe   0x320A48
00320A45  xor   eax, eax                            ; out of range -> NULL
00320A47  ret
00320A4B  imul  rcx, rax, 0x1C8
00320A52  mov   rax, [rip + 0x2B9E737]              ; -> 02EBF190
00320A59  add   rax, 8
00320A5D  add   rax, rcx                            ; *(02EBF190) + 8 + slot*0x1C8
```

**That is byte-for-byte the address `BattleUnit_ApplyUnitDefinition` computes on its kind-0 arm**,
and the bound `cl <= 0x27` makes the population explicit: **40 party battle slots.** So the
"almost certainly units" hedge below is settled — they are units — but in the direction that costs
this page the record: a **per-slot mutable battle-stats array**, reached by an accessor named for
battle slots, is runtime state that the registry slot points *at*, not authored content the loader
brought in.

The type store agrees and always did: `BattleUnit +0x698` is a `BattleStatsRecord*`, and on the
**kind-1** arm the very same field is bound to `SpawnKeep entry + 0x80`, which
`BattleStats_InitializeDefinitionRecord` `0023AC80` **memsets to zero over 0x1C8 bytes** before use.
**An authored table is not memset by its installer.** Both arms carry an object of this one type;
only the storage owner differs.

> **What is NOT claimed.** ASTRA additionally reports an observed **128-byte header stride** for the
> authored party rows, distinct from these 456-byte runtime records. **That stride is ASTRA's live
> observation and is not re-derived here**, so it is recorded as theirs rather than asserted by this
> page. What this page now states is only the part proven from the image: the `0x1C8` array at
> `*(02EBF190) + 8` is the 40-slot party stats array.
>
> **`02EBF190` carries more than this one array** — the party slot-id table lives in the same blob
> at `+0x5A5A`, stride 2. One base pointer, several regions; the registry slot names the blob, not
> the array.

### What slot 49 holds: 456-byte per-unit records

```
0023AAAA  mov   r15, [0x02EBF190]
0023AAB3  imul  rcx, r12, 0x1C8        ; 456-byte stride
0023AABA  add   r15, 8                 ; skip an 8-byte header
0023AAC1  add   r15, rcx               ; -> &record[index]
```

**`0x1C8` = 456 bytes per record, indexed by the same `r12`, after an 8-byte header.** This document
already owns and declares `0x02EBF190`; this adds its **stride and header size**, which were not
previously stated.

> **The two slots are indexed by one variable.** `r12` selects a 456-byte record in slot 49 *and*
> scales the multiplier from slot 37 in the same basic block, so they are two tables about the same
> population — almost certainly units. **"Almost certainly" is doing real work in that sentence:**
> the shared index is established, the population's identity is not.
>
> **Settled 2026-09-13, above:** the population is the **40 party battle slots**, from `BattleStats_GetByBattleSlotIndex`'s `cmp cl, 0x27` bound on the identical address expression.

### The resolver is three instructions, and it settles what slot 37's header means

```
0020E600  mov  eax, ecx                  ; zero-extend the u32 argument
0020E602  add  rax, [rip + 0x1d74f27]    ; + a global base pointer at 0x01F83530
0020E609  ret
```

`0x20E600(x) = x + [0x01F83530]`. So slot 37's `+0x0C` is a **32-bit offset, not a pointer**, and
the header describes a strided array inside a shared arena:

```struct RegistrySlot37Header base=record
+0x08  u16  stride       multiplied by the unit index
+0x0A  u16  unk0A        between stride and baseOffset; not established
+0x0C  u32  baseOffset   offset into the arena at 0x01F83530, NOT a pointer
```

*`unk0A` answered 2026-09-30 (SWE2-STRUCT for OPUS, DD batch 12, [record](../_index/candidates/swe2struct-ddres-b12-0930/README.md)
check R1).* It is the high half of the `st2e` header's u32 `recordSize` at `+0x08`
([the st2e header](VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) §2), and it is 0 in all 333 `st2e`
section headers of the nine shipped `battle_pack.bin`. No instruction reads it. A structflow census from 1,818 loads of
the table slots in 254 functions finds no access covering `+0x0A`, except the dword at `+8` of `0x02EBF158`, a slot whose
header is laid out differently (`u16 +4` stride, `u16 +6` count, `u32 +8` rows). The stride readers, `002FF110` among
them, take the low word only. So the field is a structural zero, not an unknown.

> **`mov eax, ecx` zero-extends, so these are unsigned 32-bit offsets against a 64-bit base.** That
> is the same convention `BW-2` raised from the other end — the EBP section pointer truncated to 32
> bits, and whether the allocator guarantees a sub-4 GiB arena. **Two independent subsystems using
> 32-bit offsets off a base pointer makes `BW-2` a question about an engine-wide convention rather
> than one odd instruction**, and `0x01F83530` is a second place to look for the answer.

### Where the 456-byte record goes

`&record[unitIndex]` is used exactly **twice** in the whole 1,808-byte function, and only one of
those is a real use:

```
0023ABFA  mov  [rdi + 0x698], r15        ; bind the record into the unit object
0023AC61  mov  r15, [rsp + 0x40]         ; epilogue restore, not a use
```

**`BattleUnit_ApplyUnitDefinition` binds, it does not interpret.** It computes the record address
and stores it at **`BattleUnit + 0x698`**; nothing in this function reads a field of the record.

**So the 456 bytes are reached through `BattleUnit + 0x698`, and that is where the next reader
lives** — a structure field, which no global-address scan can find. Same shape as the
`section_008` case: the search must follow the copy, not stop at it.

### `+0x698` is one of the hottest fields in the combat system — and here is the control

**301 functions, 635 uses.** A raw displacement is a weak instrument on its own: plenty of unrelated
structures could have a field at `0x698`, so the count means nothing until the neighbours are
measured.

| displacement | functions | uses |
|---|---:|---:|
| `+0x688` | 19 | 34 |
| `+0x690` | 46 | 71 |
| **`+0x698`** | **301** | **635** |
| `+0x6A0` | 73 | 143 |
| `+0x6A8` | 23 | 31 |
| `+0x6B0` | 30 | 44 |

**The five neighbouring 8-byte slots span 19–73 functions. `+0x698` is 301** — four times the
highest neighbour and roughly ten times the median. **That is far outside the band, so the hit is
real and not an artefact of "structures are large".**

Among the heaviest readers are `002F8410` — `BattleAction_ComputeChargeLimitTicks`, already named in
this document as the principal consumer of slot `0x02EBF138` — and `00307300`, `00301AD0`,
`002FDDA0`. **Combat functions, which is what the binder's own name predicts.** `00307300`'s reach
runs through its exclusive member `0030AD90`, which reads `[[rcx+0x698]+0x50]` when `[rcx] & 0x10`
and feeds the pair into `0030AC50`'s two-stage `02EBF138` registry resolve (bound on the
[battle-unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) `00307300`
subtree section).

> **What the control licenses and what it does not.** It establishes that `+0x698` is anomalously
> hot. It does **not** establish that all 301 are reading a `BattleUnit` — some may be a different
> structure that happens to have a field there. **Per-hit attribution is unestablished**, and the
> claim here is about the displacement's distribution, not about 301 individual call sites.

### The record's own field map, from 301 readers

Tracing the register loaded from `[unit + 0x698]` and collecting every displacement used against it
while it stays live gives **58 distinct field offsets** inside the 456-byte record:

| offset | reads | functions | width |
|---|---:|---:|---|
| **`+0x005`** | **229** | **156** | u8 |
| **`+0x064`** | 158 | 107 | u32 |
| **`+0x03C`** | 155 | 107 | u32 |
| `+0x004` | 79 | 62 | u8, sometimes u16 |
| `+0x000` | 20 | 16 | mixed 1/2/4/8 |
| `+0x048` · `+0x024` | 19 · 15 | 13 · 10 | u32 |
| `+0x06C` · `+0x07C` | 13 · 13 | 9 · 9 | u8 |
| `+0x050` · `+0x028` · `+0x04C` | 13 · 12 · 8 | 8 · 10 · 8 | u16 |
| **`+0x1C2`** | 10 | 8 | u8 |

**Three fields dominate**: a single byte at `+0x005` read by 156 functions, and two dwords at
`+0x064` and `+0x03C` read by 107 functions each — **the same 107, which is worth checking for a
pair**.

> **`+0x1C2` is an independent confirmation of the stride.** The record is `0x1C8` = 456 bytes and
> a field is read six bytes from its end. The stride came from `imul rcx, r12, 0x1C8` in the binder;
> the field map is a different route to the same number, and they agree.

`+0x004` is read as a byte in 73 sites and a word in 6 — so `+0x004`/`+0x005` are either a packed
pair or a small array, **not** one u16 that this census split.

**Method limit, stated because it bounds every number above.** This is a light single-function
dataflow: it follows the loaded register until that register is written, within one function body.
**It therefore misses any field reached through a second copy of the pointer** — the aliasing case
that nearly published a false `Inert` for `section_008` — and it cannot see fields read after the
pointer is spilled to stack and reloaded. **58 offsets is a floor, not the record's field count.**

### How the four `.ard` tables actually produce a stat — 2026-09-04

**`BattleStats_RebuildEffectiveStatsAndAffinityState` (`0x002FEF30`, 2,859 B) reads four of the five
`.ard` slots in four structurally identical blocks**, at `002FF0E1`, `002FF125`, `002FF167` and
`002FF1A9` — slots `0x02EBF120`, `0x02EBF148`, `0x02EBF140`, `0x02EBF150`, three reads each.

One block in full:

```
002FF0E1  mov   rax, [0x02EBF120]      ; the descriptor
002FF0E8  test  rax, rax
002FF0EB  je    0x2ff122               ; absent -> fall back
002FF0ED  mov   ecx, [rax + 0x0C]      ; baseOffset
002FF0F0  call  0x20E600               ; -> arena(0x01F83530) + baseOffset
002FF109  mov   rcx, [0x02EBF120]
002FF110  movzx r13d, word ptr [rcx+8] ; STRIDE
002FF115  movzx ecx, byte ptr [rdi+4]  ; <-- THE ROW INDEX, one byte
002FF119  imul  r13d, ecx              ; stride * index
002FF11D  add   r13d, eax              ; + base
002FF122  mov   r13, r12               ; FALLBACK when the table is absent
```

**Three things this establishes:**

1. **The slot-37 descriptor shape is the general one.** `{u16 stride @+0x08, u32 baseOffset @+0x0C}`
   resolved against the arena at `0x01F83530` — the same construction, now seen in four more slots
   and a second function. **It is the registry's calling convention, not one table's quirk.**

2. **~~All four tables are indexed by ONE byte, `[rdi+4]`.~~ SUPERSEDED 2026-09-06 — only the first
   block is, and two of the slots in this function are not `.ard` slots at all.** The corrected
   reading is in the falsification pass at the end of this document. The claim is left visible rather
   than deleted because the path to it is evidence about where the same mistake is hiding.

3. **The fallback is a float.** `r12` and `r13` are set at `002FF0C2`/`002FF0CD` by `cvttss2si` from
   `[rdi+0x10]` and `[rdi+0x14]` — floats truncated to int. **So the authored table overrides a
   float default**, and an area with no `.ard` keeps that default. That is the mechanism behind the
   loader's all-or-nothing behaviour.

> **This is the effective-stat computation the function name promises, and the first point at which
> authored `.ard` bytes are seen becoming a number the game uses.**

**What is NOT established, and it is the load-bearing gap.** `rdi` is **not** the 456-byte definition
record — this function contains **zero** loads of `+0x698`. Until `rdi` is identified, *"`[rdi+4]` is
the row index"* names a selector without saying what selects it. **Do not assume `[rdi+4]` is the
definition record's `+0x004`** because both are bytes at offset 4; that is the adjacency reasoning
this database bans.

### `rdi` IS the 456-byte definition record — identified by field fingerprint

**And that closes the link from an authored record to its `.ard` row.**

`rdi` is parameter 1 (`mov rdi, rcx`, `002FEF6B`). It could not be identified the easy way — neither
this function nor either of its two callers references `+0x698` — so it was fingerprinted by the
offsets it touches:

| | |
|---|---:|
| distinct `[rdi+N]` offsets in `002FEF30` | **20** |
| of those, already known as definition-record fields | **18 — 90 %** |
| highest offset touched | **`+0x1C2`** |
| record size | **`0x1C8`** |

Shared: `+0x004 +0x005 +0x008 +0x00A +0x00C +0x00E +0x010 +0x012 +0x014 +0x018 +0x01A +0x01C
+0x01E +0x024 +0x03C +0x050 +0x088 +0x1C2`. The two that are not (`+0x016`, `+0x020`) are fields the
`+0x698` tracker missed — that census was explicitly a floor, not a count.

**Two independent signals agree.** A 90 % field overlap, and a maximum offset of `+0x1C2` that fits
inside `0x1C8` **with six bytes to spare** — `+0x1C2` being a distinctive enough offset that sharing
it by chance is not a serious reading.

> **This was NOT assumed from adjacency.** The section above warned in terms against reading
> `[rdi+4]` as the record's `+0x004` because both are bytes at offset 4. **The warning was right and
> the conclusion survives it**, because it now rests on eighteen shared offsets and a size fit rather
> than on one coincidence.

### The chain, end to end

```
definition record +0x004            the row index (one byte)
  x  stride        .ard slot descriptor +0x08
  +  baseOffset    .ard slot descriptor +0x0C, resolved against arena 0x01F83530
  ->  a row in one of the four .ard st2e tables (84 / 88 / 56 / 56)
  ->  an integer stat, OVERRIDING a float default at [rec+0x10] / [rec+0x14]
```

**and `+0x005`, the byte beside the index, gates whether any of it happens** — 108 of 118 boolean
tests, zero meaning proceed. **That is why `+0x004` and `+0x005` are read as a pair and occasionally
as one u16: they are the selector and its enable bit.**

**What remains for "change a Marlboro":** what a *row* contains. The lookup, the selector, the enable
bit and the fallback are all established; the 84/88/56/56 record layouts are not.
*(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: this belongs to other pages. The `.ard` records are the area-file
pages' to map. [The `.ard` loader](VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)
§7 states the record level as its own remaining part, and its CC-7 section reads the 56-byte slots 5 and 6 as a base
row and a growth row (experience `+0x34`, licence points `+0x2F`, gil `+0x30`).)*

### The earlier chase, kept because the negative was reported honestly

`rdi` is **parameter 1** — `mov rdi, rcx` at `002FEF6B`. The function has exactly **two callers**:

| caller | passes | |
|---|---|---|
| `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0` | `rcx = rbp` | `0030A6AD` |
| `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` | `rcx = rbx` | `003103AA` |

**Neither caller, nor the callee, contains a single reference to `+0x698`** — the field
`BattleUnit_ApplyUnitDefinition` binds the 456-byte definition record into.

> **That is inconclusive, and specifically NOT proof the object is not a `BattleUnit`.** A function
> can hold a unit pointer and never touch that one field; absence of a reference is absence of
> evidence, which is the rule this database states in four other places. **What it does mean is that
> the easy identification is unavailable** — the object cannot be called a `BattleUnit` on this
> evidence, and it must not be assumed to be one because the surrounding functions have battle names.

**Next, and it is a different question than before:** trace the callers of `0030A4E0` and `0030FED0`
for where `rbp`/`rbx` originate, or fingerprint the object by the fields these three functions do
touch. Until then the chain runs **`.ard` row → `stride × [rdi+4] + base` → a stat**, with the link
from `[rdi+4]` back to a *named enemy* unestablished. *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale. The
section above identifies `rdi` as the 456-byte definition record, and `CB-11` is ANSWERED: `[rdi+4]` is the low byte
of the stats record's definition id.)*

### `+0x005` is a boolean gate, and zero is the case that proceeds

**Settled by reading one heavy consumer end to end, then measuring the pattern corpus-wide.**

`00301AD0` (41 uses) tests it twice, identically:

```
00302140  movzx eax, byte ptr [rcx + 5]
00302144  test  eax, eax
00302146  jne   0x303567          ; NON-ZERO -> abandon the whole path
0030214C  movzx edx, byte ptr [rcx + 4]   ; ZERO -> read +0x004 and continue
00302153  call  0x3215c0
```

**Not an enum comparison — a zero test.** And measured across every reader:

| what immediately follows a load of `+0x005` | count |
|---|---:|
| **`test reg, reg` — a zero test** | **102** |
| `cmp reg, 1` | 6 |
| `jmp` / `xor` / other | 10 |
| **total tracked loads** | **118** |

**108 of 118 are boolean tests.** `+0x005` gates whether the record's payload is used at all, and
**zero is the proceeding case**.

It also ties the adjacent pair together: at `0030214C`, **`+0x004` is read only when `+0x005` is
zero.** The census had already shown `+0x004`/`+0x005` are read as separate bytes 73 times and as a
word 6 times; this says why they belong together.

> **This supersedes a suggestive reading recorded here an hour earlier**, which counted 13 distinct
> immediates across 30 compare sites and floated "small enum" while declining to claim it. **That
> tail was tracker noise.** The loose dataflow attributed compares from reused registers, and the
> real signature — `test reg,reg` at 86 % of load sites — was invisible until one function was read
> in full. **The corpus-wide scan was the weaker instrument and the single careful read was the
> stronger one**, which is the opposite of the usual order and worth remembering.

### The `00301AD0` exclusive subtree — all 6 members bound (SWE2-FRONTIER, followup queue)

`00301AD0` (`AiOrder_EvaluateTargetSelector`, 6,963 B) owns **6 frontier functions** — the
scoring helpers its selector arms call. Every member was disassembled from the shipping
image; interior cites are one instruction inside each declared extent. `003215C0` is the
call the `+0x005` section above quotes at `00302153`: it is the `+0x6A0`-buffer predicate
the zero-gate proceeds into.

| member | size | role | interior |
|---|---:|---|---|
| `0031E6F0` | 106 B | body-to-body clearance: `0030A130(a)`/`0030A130(b)` fetch two radii, `004686D0(a+0xE0, b+0xE0)` the position distance — returns `max(0, dist − r_a − r_b)`; the root calls it six times across the selector arms | `0031E71D` |
| `0031E760` | 74 B | the point-to-body variant: `0030A130(a)` once, `004686D0(a+0xE0, point)` — `max(0, dist − r_a)` | `0031E77A` |
| `003209E0` | 21 B | `a·100 / b` percent-of with a null-divisor fast path returning `a·100` (`cqo`/`idiv` at `003209E8`) | `003209E8` |
| `00321320` | 82 B | the `+0x698` → `+0x50` chain resolver: `[rdx] = -1` sentinel written first, then `rcx` null → `-1`, `[rcx+0x698]` null → `-2`, `+0x50` null → `-3`, else `00321400(word[+0x50])` and `0` | `00321353` |
| `003215C0` | 102 B | the `+0x005`-gated lookup: resolves `[rcx+0x6A0]+0x19` (or fails `-1`), then `00322C50(buf, arg_byte, 2)`; returns `-1` when that probe fails — this is the `00302153` call | `003215F6` |
| `00321630` | 175 B | the max-scan: `0030A880(&list, 1)` enumerates candidate records, and per entry resolves `[+0x698]` → `00322C50(rec, byte[+4], 2)`; on success it takes `byte[byte4 + [+0x6A0]+0x19 + 1]` and keeps the maximum — the selector's "best stat across candidates" measure | `00321680` |

`0030A130`, `004686D0`, `0030A880`, `00322C50`, `00321400` are shared callees with other
callers — deliberately not census members.

### The earlier attempt, kept because the method limit is the lesson

`+0x005` is the record's hottest field: **229 reads in 156 functions**, and **`movzx` in all 117
tracked loads**, so it is a byte zero-extended into a wider register — the shape of a small enum,
an index or a count.

**Testing the enum reading against the compare sites did not settle it:**

| | |
|---|---:|
| reads of `+0x005` | 229 |
| of those, compared against an immediate | **30** |
| distinct immediates | **13** |

The values are `1` (×9), `3` (×9 across two encodings), `5`, `2`, `8`, `10`, `-1`, and a tail of
`51`, `53`, `55`, `254`, `358`.

**Two reasons this is not a finding.** Only **30 of 229** uses are comparisons at all, so the field
is predominantly *used* — as an index or an argument — rather than tested; and a 13-value set with a
scattered tail is not the clean contiguous signature a small enum produces. **The tail may equally
be the tracker mis-attributing a reused register**, which the method cannot rule out.

> **Suggestive is not deciding.** A byte compared against `1`, `2`, `3`, `5`, `8` and `10` invites
> "unit category" and the invitation should be declined: nothing here distinguishes that from a
> count, a tier, or an index whose callers happen to test a few values.

**What would settle it:** read one heavy consumer end to end — `00301AD0` (41 uses) or `002FDDA0`
(29) — and see what the byte actually selects. That is a bounded read and it is the next step.

### Not declared, and why

**`registry_slots` is not extended to `0x02EBF130` here.** The rule is to declare only where the
document establishes **what the slot holds**, and what is established is its *shape* — a header with
a multiplier and a resolver argument — not its contents. A slot declared on structure alone would
be the count-match error the `st2e` document already caught itself making.

**What would settle it:** read `0x20E600` (what base does it return, and from what?) and the 456-byte
record layout in slot 49. Both are bounded reads.

### Instrument note

These references were invisible to two earlier scans. A RIP-relative sweep over `.text` returned
**0 of 63 registry slots referenced** — and returned 0 for a control address read out of a
disassembly by hand, which is what exposed it. **`.text` contains data and padding, so a linear
sweep desynchronises and silently never decodes large stretches.** Disassembling from each entry in
`functions.tsv` returns 83 references for this slot and 4 for the control.

`data_xref_scan.py` now does this and **refuses to report a result when its control returns zero**,
because *"no references"* and *"my instrument cannot see references"* produce identical output.

## Falsification pass 2026-09-06 — the "four tables, one index" claim is overturned

**Two sessions reached this independently and neither read the other first**, which is what makes it
a finding rather than a report: `repos-1e` from an audit of the work board's summary, `repos-c7`
from a complete read of `BattleStats_RebuildEffectiveStatsAndAffinityState` (`0x002FEF30`, 2,859 B).

### What was believed

*"All four tables are indexed by ONE byte, `[rdi+4]`. Four parallel per-row lookups keyed on the same
selector."*

### What is now believed

**The function performs that lookup twice, against two different registry slots, and only one of them
is an `.ard` slot.**

| lookup site | `imul` by `[rdi+4]` | slot resolved | is it `.ard`? |
|---|---|---|---|
| `0x002FF119` | yes | `0x02EBF120` | **yes** — `.ard` directory slot 2 |
| `0x002FF065` | yes | `0x02EBF130` | **no** — character/unit growth definitions |

`0x02EBF130` is slot 37, *character/unit growth definitions*, read by
`BattleUnit_ApplyUnitDefinition` (`0x0023A570`) and
`BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0x0030C650`). **The `.ard` loader does not
fill it** — that loader binds exactly `02EBF150 / 02EBF168 / 02EBF120 / 02EBF148 / 02EBF140`, and
`0x02EBF130` is not among them.

**And the function reads seven registry slots, not four:**

| slot | refs here | what it is |
|---|---:|---|
| `0x02EBF040` | 10 | status auxiliary / timer parameters — **not `.ard`** |
| `0x02EBF0F8` | 3 | equipment definitions — **not `.ard`** |
| `0x02EBF120` | 3 | `.ard` slot 2 |
| `0x02EBF130` | 3 | growth definitions — **not `.ard`** |
| `0x02EBF140` | 3 | `.ard` slot 6 |
| `0x02EBF148` | 3 | `.ard` slot 5 |
| `0x02EBF150` | 3 | `.ard` slot 0 |

Each appears in the same three-reference shape — slot pointer, `+0x0C` baseOffset, `0x20E600`,
`+0x08` stride. **`0x02EBF168`, the gambit order-set slot, is not read here** *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: it is read on its owner's page, [the `.ard` loader](VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md) §7a, "Slot 1 read whole", CC-5)*, which is consistent:
four `.ard` slots feed stats and one feeds AI.

`0x02EBF130` serves the `rec[+0x05] == 0` path specifically — the selector byte this document already
records as gating whether the authored override happens at all.

### Why the earlier reading was reachable

**Section 5 of this document was never wrong.** It states the lookup generically — *"any gameplay
lookup: read slot pointer, count at `+0x04`, stride at `+0x08`, RVA at `+0x0C`, row = base + index x
stride"* — and **never says `.ard`.**

The `.ard` clause was introduced by a **summary** of this document on the work board, and two authors
built on it for two days. The generic statement was correct; the restatement was one clause stronger
than its source.

> **Cite the document; do not restate its conclusion in stronger words.** A summary that reads as
> settled is what a session under time pressure reads instead of the source, and this is the second
> instance of that failure in three days. Recorded in
> [`../_index/COVERAGE.md`](../_index/COVERAGE.md).

### What survived the attack unchanged

`repos-1e` re-derived the whole surrounding block and **everything else verified exactly**: body size
2,859 B, 20 distinct `[rdi+N]` offsets, maximum `+0x1C2` fitting inside `0x1C8`, zero-means-proceed
on `+0x005`, stride `u16` at descriptor `+0x08`, baseOffset at `+0x0C`, and the arena `0x01F83530`
confirmed to be in BSS. **The `rdi` identification by field fingerprint stands.**

`repos-4b`, auditing separately, found a second defect in section 2's own caution: it answers itself
**three instructions inside the function it names** — categories 0..4 map to
`0x02EBF150 / 168 / 120 / 148 / 140`. **The caution listed four slots; there are five, and
`0x02EBF168` appeared zero times in this document's 967 lines at the time.**

### A third correction, smaller and load-bearing for anyone reading `+0x004`

**`+0x004` is not only a row index.** It is range-tested as an **actor type id in the 13-value band
`0x1B`..`0x27`** at `0x002FF00B` (`sub al,0x1b ; cmp al,0xc`) — already documented in
[`../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md`](../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md).
The same byte is both a partition test and a table index, and a modder changing it changes both.

### Program state

GN160 `fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`, re-verified 2026-09-07.
Merged by `xiionline-61`; open residue tracked as `CB-11` in
[`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md). *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12:
stale. `CB-11` is ANSWERED.)*

## Registry slot census by named reader — 2026-09-07

`xiionline-61`, GN160. **`.text` disassembled function by function**, every RIP-relative operand
resolved, and every reference landing on an 8-byte boundary in `02EBF008`–`02EBF1F8` attributed to
its owning function.

**62 of the 63 slots are referenced from `.text`.** Slot 50 (`02EBF198`) is referenced by nothing —
consistent with `AG-4`, which already records `02EBF198` as unreferenced.

**40 of the 62 have at least one reader the ledger has named.**

> ⚠ **Corrected 2026-09-07, one block after this section was written.** It originally read *"forty
> have a named consumer sitting there unused"* — **and thirty-nine of the forty were already cited by
> a document in this database.** Only **slot 14** has a named reader and no citation anywhere. The
> check that falsifies it is a grep for the slot address across the database, and it takes seconds;
> it was not run. See *"What this census actually establishes"* below.

### Evidence tier, stated before the table rather than after

**These are leads at tier 4 (ledger function names), not identifications.** A reader's *name* is a
prior session's claim about that reader. The table says *"a function called X reads this slot"*,
which is a fact about the call graph; it does **not** say the slot holds what X's name suggests.
**Promote a row only by reading the consumer body** — the standard the enemy-record round used, where
`+0x2A` became Strength because `BattleFormula_ReduceStrengthTo70Percent` reads it, not because the
name looked right.

| slot | address | refs | named readers | reading suggested (UNPROVEN) |
|---:|---|---:|---|---|
| 6 | `02EBF038` | 64 | `BattleStats_CheckLicenseNodeAcquireReason`, `BattleMenu_BuildCommandEntryList` | licence / command-entry table |
| 7 | `02EBF040` | 111 | `BattleAction_ComputeChargeLimitTicks`, `BattleAction_ComputeModifiedResourceCostAmount` | status auxiliary / timer parameters *(already recorded)* |
| 8 | `02EBF048` | 7 | `Inventory_InitializePrimaryStateFromAuthoredTable` | inventory initial state |
| 12 | `02EBF068` | 8 | `InventoryBundleClass0A_ApplyNestedItems` | nested-item bundle class 0A |
| 13 | `02EBF070` | 8 | `InventoryBundleClass09_ApplyGilAndNestedItems` | gil + nested-item bundle class 09 |
| 19 | `02EBF0A0` | 5 | `BattleSpecialSequence_SelectActionByAuthoredThreshold` | authored threshold table for special sequences |
| 22 | `02EBF0B8` | 21 | `BattleAction_LookupPrimaryResourceGainFactorByHpDamage`, `BattleUnit_ResolvePeriodicPrimaryResource…` | **EXPLAINED 2026-09-07** — **two tables in one slot**: rows **1–19** `{u16 threshold, u8 factor, u8 bandFactor}` are the MP-gain-from-HP-damage ladder, rows **20–24** `{s32 interval, s32 mpThreshold}` are the walk-recovery ladder. **Neither consumer reads the header's row count**; both bounds are compiled in. See [`../10-Status-Periodic-Terminal/where-mp-comes-from.md`](../10-Status-Periodic-Terminal/where-mp-comes-from.md) |
| **23** | **`02EBF0C0`** | **18** | **`Loot_RollDropEntries`, `Loot_RollNormalSlotChance`, `Loot_RollNormalSlotQuantityBucket`** | **the loot / drop table** |
| 26 | `02EBF0D8` | 34 | `GambitConfig_ClassifyActionTargetPairCompatibility`, `GambitRuntime…` | gambit action/target compatibility |
| 27 | `02EBF0E0` | 8 | `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` | authored gambit presets |
| 29 | `02EBF0F0` | 22 | `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` | item discovery state |
| 30 | `02EBF0F8` | 272 | `BattleAction_Compute*` family | equipment definitions *(already recorded)* |
| 34 | `02EBF118` | 130 | `BattleAction_ComputeAuthoredStatusMask`, `BattleFormula_AdvanceS…` | authored status masks |
| 35 | `02EBF120` | 27 | `BattleData_SetAreaArdSectionCategory`, `BattleStats_InitializeDe…` | `.ard` slot 2, the join spine *(proven, `CB`)* |
| 37 | `02EBF130` | 83 | `BattleAction_CheckDefinitionCategoryAvailability` | character/unit growth definitions *(proven, `CB-11`)* |
| 38 | `02EBF138` | **723** | `AiOrder_*`, `BattleAction_AcquirePrese…` | action definitions, 543 rows *(proven, `AG-1`)* |
| 39/40/41 | `02EBF140/148/150` | 8/8/11 | `BattleStats_RebuildEffectiveStatsAndAffinityState` | `.ard` slots 6 / 5 / 0 *(proven, `CB`)* |
| 43 | `02EBF160` | 3 | `BattleData_ResolveWeightedId` | weighted-id resolution table |
| 44 | `02EBF168` | 5 | `BattleUnit_ApplyUnitDefinition` | `.ard` slot 1, gambit order sets *(proven, `CB-1`)* |

> **Slot 44 was explained here and not DECLARED, and that is why `registry_explained` read 62 of
> 63 — corrected 2026-09-14 (OPUS).** The row above has carried the `CB-1` proof since it was
> written, the caution table names `0x02EBF168` as a category-1 slot bound by `0x003846F0` with a
> third argument zeroed, and the five `BattleData_SetAreaArdSectionCategory` binds list it — while
> the `registry_slots:` list in this file's own frontmatter did not. **A declaration gap, not a
> coverage gap**, and the same shape as the twelve experiment records whose `contract:` key was
> missing while their prose said what they tested.
>
> *The first attempt at this fix put the explanation inside the YAML list as `#` comments and the
> figure did not move: `check_formats.claimed_slots` ends the block at any non-matching non-blank
> line, so the comment terminated the list before the new entry. `check_assets.claimed_formats`
> skips `#` lines for exactly that reason — "a commented example is not a claim" — and the two
> parsers disagree. Filed as `OPUS-NOTE-SLOT-LIST-COMMENT-PARSE`.*
| 45 | `02EBF170` | 58 | `BattleUnit_ApplyUnitDefinition` | ~~unit definition table~~ **CORRECTED 2026-09-10:** a text bank table — ≤ 32 banks of image-relative pointers to text blocks, addressed by a definition row word split 5 : 11 and read through `002B58B0` ([the unit-definition page](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.7). **Decoded 2026-09-11:** the section is `battle_pack.bin`'s directory entry at the blob's `+0xF8` (`us` file offset `0x2BBA8`), bound by the two-level rebase `003846F0` from `00236FCF`; fifteen banks — action names, equipment, licence nodes, commands, statuses, gambit conditions, characters, bazaar goods, key items, locations, enemy classes and genera — on [the battle text banks page](VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) |
| 48 | `02EBF188` | 93 | `BattleFormula_ApplyPreResolutionTargetGates`, `BattleFormula_ApplyResultMetadata` | formula gates / result metadata |
| 49 | `02EBF190` | **318** | `AiOrder_EvaluateTargetSelector`, `BattleFormula_A…` | battle-system runtime state block, ≥ 23 KB *(proven, `AG-1`)* |
| 51 | `02EBF1A0` | 15 | `BattleStorage_InitializeWorkArrays` | battle work arrays |

**~~Slot 23 is the one worth taking first.~~ WITHDRAWN — it was documented on 2026-09-02.**
[`../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md`](../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md)
already names `02EBF0C0` the **loot chance-profile table** with its count at `+4`, lists it in its own
frontmatter, and reads `Loot_RollAdditionalItemChance` completely plus two more partially. The claim
that *"the fifteen-function `Loot_*` family is a system nobody has documented"* was false when
written.

### The tail is structurally interesting on its own

**Slots 52–62 each have exactly 2 references**, and slots 53–62 have *no* named reader. Eleven
consecutive slots with an identical, minimal reference count is not a coincidence — it is the
signature of the **generated per-slot setter family** this document already records at
`002383C0`–`002385A0`, one setter every `0x30` bytes. **Two references = the generated setter writes
it and one consumer reads it.** These are bound at load and reached generically, which is the same
shape the eleven anonymous class descriptors turned out to have.

### What this census actually establishes — restated after the correction

It attributes references to owning functions. **It does not read a single consumer body**, so it
cannot say what any slot *holds*. And measured against the database rather than against the binary:

| | |
|---|---:|
| slots referenced from `.text` | **62 of 63** |
| slots with a reader the ledger has named | **40** |
| slots **already cited** by at least one document | **46** |
| slots with a named reader and **no citation anywhere** | **1** — slot 14, `02EBF078` |
| slots `registry_explained` counts as explained | **9** |

**So the census is not a discovery instrument here; it is a completeness check, and it mostly
confirms prior work.** Three things survive as its actual contribution:

1. **Slot 50 (`02EBF198`) is referenced by nothing at all** — independently reproducing `AG-4`.
2. **Slot 14 (`02EBF078`) is the one genuinely uncited slot with a named reader.**
3. **Slots 52-62 carry exactly 2 references each and 53-62 have no named reader** — the signature of
   the generated per-slot setter family, setter writes and one generic consumer reads.

> **The gap between 46 cited and 9 explained is a depth problem, not a discovery problem.** No scan
> closes it; reading consumer bodies does. **A census that measures the binary and not the database
> will keep re-finding what the database already knows** — and will report it as new.
## The tail read — 2026-09-11 (FABLE-PUB119)

The three tail slots the census left as *not pointer slots* and the eleven it called *scalar
state* are read here from their consumers; every reading below is a body, not a reference count.

**`02EBF158` — the shop table** (directory `+0xA0`). The one write the census saw is the binder
`00238660` adding the directory dword to the slot (`00238678`–`00238686`) before it rebases three
levels of nested offsets; the consumers are the shop menu's list builder and the script verb
`setshopname`. [The shop table page](../12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md) declares the slot.

**`02EBF180` — the weapon-class map** (directory `+4`). The binder stores this directory dword
directly (`00236C70`–`00236C74`), ~~the only slot it fills without~~
~~`AreaData_BindAndRebaseSectionDescriptor`~~ one of four slots it fills without `AreaData_BindAndRebaseSectionDescriptor` - `0x02EBF200` is stored the same way, and `02EBF160` / `02EBF170` go through `003846F0` *(corrected 2026-10-02, OPUS: `00236C30+0x401` stores `0x02EBF200`; `00236C30+0x109` and `00236C30+0x3BA` call `003846F0`)*; the `us` section is `{u16 stride 1, u16 count 23}` and
23 bytes: `00 01 04 03 0C 0D 06 09 08 00 08 07 07 09 0A 0B 00 0E 0F 00 0F 05 02`. Its readers
index it by an **equipment row's category byte `+0x26`**: `003203B0(id, &out)` resolves a
`0x1000`-class id to its `02EBF0F8` row (`003203C3`–`00320408`), takes `+0x26` when the row's kind
byte `+7` is below `0x20` (`00320418`–`0032041E`; the 308 weapon and shield rows of the `us` pack —
every row at or above `0x20` carries category 0) and reads `map[category]` (`0032042D`–`00320443`;
a row at or above `0x20` yields index −1, the count's high byte, 0). `003202F0(statsRecord, &out)`
feeds it: a kind-1 record's definition byte (`+0xE60` → `+0x13`, `00320319`–`0032033C`); otherwise
the weapon word `+0x50`, except bare hands (`0x1000`) with an empty off-hand and stats flag `+0x69`
or `+0x79` bit 1, which read entry 22 directly (`0032034B`–`00320380`, value 2). `00325AD0(unit)`
and `00325A20(unit, arg)` return **entry 1 (= 1) for every party record** (`00325AED`–`00325AFF`,
`00325A48`–`00325A5A`) and take the stats path otherwise. Three consumers show what the class is
for without naming it: `002E4C30(model, class)` tests bit `class` of the model row's `+0x24` in the
`0x120`-stride table at `020C1DA0` (`002E4C39`–`002E4C61`; from `002EE430`, which resolves the
weapon id held in the word at `02105E30`); `00325A20` hands it to `003DC410` and `00325B40` to
`003DCCF0`, each with the unit's actor record; `0030C890` stores `class & 3` in bits 1–2 of a
record's `+0x2C` (`0030C8E2`–`0030C8EE`). A weapon-category → class map, then — and **what the class picks is the attack motion file
(FZ-9 answered 2026-09-11)**: `00325B40` and `00325A20` hand it, with the action's motion id from
`BattleAction_SelectGlobalSequencePresentationEvent` (`0030CD21`–`0030CD2B`), to the motion cache
`003DCD00(actor, motion, class, flag)`, which keys its sixteen 20-byte entries at `02B57F70` by the
model id (`002E96B0`: the movement context's `+4`), the motion word and the class byte
(`003DCD70`–`003DCD9F`) and on a miss resolves the file through `003DCA30(model, motion, class,
&kind, &index)` — **kind `0x1E` = 30, the `obj_finish` `.ca` motion array** (`003DCA49`), the index
looked up in three runtime tables of 16-byte `{u32 model, u16 class, u16 motion, u16 index}` rows
(`02B58188` by model and motion, `02B58178` and `02B58180` by model, motion and class,
`003DCA5F`–`003DCB53`) — then sizes it (`0032E400`, `003DC977`) and requests it (`003DC380`,
`003DC5B0`). So a party record's constant entry 1 and a monster's category-derived class choose
which `cNNNN_10_XXXX.ca` / `mNNNN_10_XXXX.ca` file animates the swing. The three tables are set by
`003DC330`, `003DCF00` and `003DCF10`, whose callers — the loader of the per-model motion index — are
unread. *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale. `CC-10` on [the `.ard` loader](VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)
§7 reads them: `02B58178` is the `.ard`'s slot-7 table and `02B58180` is `section_019`'s `+0x2C` table, and the
binder `003DCBC0` nulls both at start-up. Check R4 pins the callers. `003DC330` (it sets `02B58188`) has no caller:
`003DCBC0` registers it as a load-completion callback. `003DCF00` is called from `003EA6B0`, `003EA710` and `003EA820`,
and `003DCF10` from `003EA6B0` and `003EAA00`.)*

**`02EBF178` — a runtime-published pointer, not a table** (AG-4, narrowed). `00324510` (from
`MainLoop_UpdateAndRenderFrame`, `0022BAEF`) is a three-state builder on the dword `022C27A0`:
state 1 writes a `u16 301` header into the buffer at `022C27B0` and points the cursor past its
302 offsets (`00324587`–`003245CF`); state 2 loads up to ten items per call — `0032E620(0x1a, i,
cursor, id)` ~~for every positive id in the `{i32 id, i32 size}` pairs~~ for every positive size in the `{i32 size, i32 requestId}` pairs, that size being the fourth argument, *(corrected 2026-10-02, OPUS: the assembler `00324510` passes the entry's first dword as the fourth argument (`00324510+0x119` `mov r9d, dword ptr [rbx]`), which is the byte count (part A, C-V2), advances the cursor by it, and stores the returned request id into the second (`00324510+0x133` `mov dword ptr [rbx + 4], eax`))* at `022C27B8` — recording
each offset and size and advancing the cursor by the size rounded up to four (`003245D9`–
`0032467A`); when all 301 are done it publishes the buffer pointer to `02EBF178` and sets state 3
(`0032468F`–`003246A1`); the teardown branch frees the buffer through `003697F0` and clears both
(`0032453C`–`00324558`). Nothing reads the slot by address. What sets state 1 and fills the 301
ids, and who reads the blob, is **FZ-8**.

**`02EBF1A0`–`02EBF1F8` — ~~the completion words of~~ the loaded-board pointers of twelve board requests** *(corrected 2026-10-02, OPUS: `00384420+0x99` writes the buffer address into the descriptor's `+8`; the 2026-09-30 correction below)* (M-7 answered; corrected the same day).
`BattleStorage_InitializeWorkArrays` clears the twelve and calls `00238260(k)` for k = 0 … 11
(`00236A17`–`00236A24`). `00238260` builds the twelve setters' addresses on its stack
(`0023827D`–`00238300`: `00238390` + `0x30·k`), and if slot k is empty (`00238319`–`00238327`) and
`00233E00(k)` allows — fewer than six of the twelve are set (`00233E21`–`00233E95`) — requests
**loader id `0x47 + k`** through `00384420(id, setter_k, 008A46A0, 3, 8, 4)` (`00238355`–
`0023837D`), which resolves the id (`0032E400(2, id)`, `0036A190`) and queues `0032E620(2, id, …)`
with the setter as its delivery callback (`0038444E`–`003844C9`). **Corrected 2026-09-11:** the
delivery callback receives the descriptor's `+8` word, not the buffer ([the request queue page](the-resource-request-queue.md)
§2.4), ~~and `00238260` passes `3` in that word (`00238364`)~~; each setter releases whatever the slot
held through `003844F0` → `003697F0` and stores that word (`002383C9`–`002383DA`), on delivery and
on failure alike. ~~So the eleven are **completion markers**, not pointers: the loaded bytes live in~~
~~the resource block `0036A190` allocated, tagged at its header by `0036C660`, and nothing reads the~~
~~twelve but the six-resident count `00233E00`.~~
*Corrected 2026-09-30 (SWE2-STRUCT for OPUS, DD batch 12, [record](../_index/candidates/swe2struct-ddres-b12-0930/README.md)
check R2): the word is the buffer's address, so the twelve are pointers to the loaded boards.*
- *The `3` at `00238364` is `00384420`'s fourth argument. `00384420` spends it on `0036C1D0` (`00384448`, `00384464`)
  before `mov rbx, rax` (`0038447E`) replaces it with the buffer `0036A190` allocated.*
- *The descriptor's `+8` word is then `ebx`, the buffer's low dword (`003844B9`). `0032E620` copies the descriptor
  whole, `0032E870` moves `+8` to the request's `+0x60`, and both callback calls pass `+0x60` as `ecx` (`0032E34C`,
  `0032E38F`).*
- *So each setter stores the sign-extended address of the loaded `board_{k+1}.bin`, and the `003844F0` release on
  rebind frees the previous board.*
- *`0055BFF0` dereferences that pointer as the file's `licd` header: width `+4`, height `+6`, cells from `+8`
  (`0055C0B0`–`0055C0CC`). All 48 shipped `board_N.bin` carry width and height 24 there.*
- *The round trip through a 32-bit word assumes the buffer lies below 2 GiB. That is the allocator's convention
  (`BW-2` territory), not something this check settles.*

Loader ids `0x47`–`0x52` are kind-2 path-array positions 71–82 — **`board_1.bin` … `board_12.bin`, the
twelve job boards** ([the board grid page](../12-Items-Equipment-Shops-License/license-board-grid-format.md)
§3; the request sizes them through [the file-size table](Loose-Files-And-Size-Tables/file-size-tables-fst.md), 1,160 bytes each)
— so slot `02EBF1A0 + 8k` ~~marks the completion of the request for~~ *(corrected 2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: holds the address of the loaded)* `board_{k+1}.bin`, at most six
requests resident. FZ-7 answered 2026-09-11, and the eleven from `1A8` are declared here on that basis.

**`02EBF198`** still has no reference of any kind.

## The upper sixteen slots, classified — 2026-09-16 (SWE2-STRUCT)

`OPUS-REQ-SWE2-STRUCT-REGISTRY-UPPER-SLOTS` asked the narrow question AG-5 leaves open after §8b:
**do the consumers of `0x02EBF180`–`0x02EBF1F8` read the `+0x04`-count / `+0x08`-stride / `+0x0C`-RVA
header the way the censused band's do?** Method: `data_xref_scan.py --range 0x02EBF180 0x02EBF1F8
--stride 8 --control 0x02EBF138` over all 34,270 function bodies (control positive at 723
references), then instruction-level reads of every distinct consumer shape rather than counts alone.

**AG-5 stays NO, and the boundary is now named per slot.** The band's table header holds only where
an individual slot was proven a table; the upper sixteen contain four different layouts:

| Slot | Refs | Kind | Is there a `+0x04` row-count header? |
|---|---:|---|---|
| `0x02EBF180` | 5 | **Table pointer, different header** — the weapon-class map read in the tail section: `u16 +0` stride (=1), `u16 +2` count (=23), byte rows from `+4`. All four consumers load the slot then do `movzx eX, word [ptr]` and `movzx eY, byte [ptr + word*index + 4]` (`00320376`, `0032042D`, `00325A50`, `00325AF5`) | **No** — `+4` is row data, not a count |
| `0x02EBF188` | 93 | **Write-only state sink** — all 93 sites are `mov [slot], reg` stores; nothing loads it and nothing dereferences a value from it (§8c) | **No** — never dereferenced |
| `0x02EBF190` | 318 | **BattleSystemState pointer** — the `0x7410`-byte block whose `+0` is magic `0x05071901` and `+4` a flag dword OR-ed with `0x100`/`0x80` (§8b; `BattleSystemState` in the type store) | **No** — `+4` is a bitfield |
| `0x02EBF198` | 0 | **~~Initialised but~~ BSS and never named** *(corrected 2026-10-02, OPUS: past `.data`'s raw end `0x01F7E400`)* — disposition below | n/a |
| `0x02EBF1A0`–`0x02EBF1F8` | 16 + 2×11 | **One 12-qword array, not twelve independent slots** — bulk-zeroed by `rep stosq` (`ecx=0xC`) from `lea rdi, [02EBF1A0]` at `002369E5`; per-slot setters at `00238390`–`002385A0` (`0x30` stride) store `movsxd(ecx)` after releasing the previous value through `003844F0` → `003697F0` | **No** — ~~the slots hold scalar values, not table pointers~~ *(corrected 2026-09-30, SWE2-STRUCT for OPUS, DD batch 12, check R2: each slot holds the address of a loaded `licd` board, `{u16 width, u16 height}` at `+4`, not a `st2e` table)* |

**The boundary, stated exactly:** the `+0x04`/`+0x08`/`+0x0C` header is a property of *individual
slots proven to be authored tables*, all of which so far live at or below `0x02EBF178` (slot 46).
Nothing from `0x02EBF180` up exposes that header — not even `0x02EBF180`, which is a genuine table
pointer but uses the `u16 stride, u16 count` header instead.

**Two corrections this pass makes to what the page already said:**

1. **Twelve setters, not eleven.** The generated family runs `00238390`–`002385A0` at `0x30` stride —
   `00238390` (for slot `0x02EBF1A0`) precedes the `002383C0`..`002385A0` run §8c counted. The array
   is therefore all twelve slots `0x02EBF1A0`–`0x02EBF1F8`, matching the `rep stosq` width and
   `00238260(k)` for k = 0…11 in the tail read.
2. **The twelve are read by indexed access, which the per-slot direct scan cannot see — and one such
   read treats the values as pointers.** `0055BFF0` (`0055C0A8`) executes
   `mov rdx, [rdx + rax*8 + 0x2D9F1A0]` where `rdx` is freshly reloaded to the image base
   `0x00120000` at the top of every outer-loop iteration (`0055C04C`, `0055C390`), so the target is
   genuinely `0x02EBF1A0 + 8·rax` with `rax = movsx byte [obj+0x558]`. It then dereferences the slot
   value: `word [rdx+4]` and `word [rdx+6]` are read as bounds for a `u16` grid at `+8`. The tail
   read's claim that *"nothing reads the twelve but the six-resident count `00233E00`"* is therefore
   superseded — there is at least one indexed reader, and it wants pointers to
   `{u16 bound, u16 bound, u16[] grid}` objects, the shape a loaded `board_N.bin` grid would have.
   **Live tension, recorded rather than resolved:** §2.4 of the request-queue page has the delivery
   callback receive the descriptor's `+8` word, and the tail read has the setters storing `3`; a slot
   holding `3` would fault this reader. Either the slots also receive real pointers on a path not yet
   read ~~(the image-initial values below are already pointers)~~ (the slots are BSS, zero at load *(corrected 2026-10-02, OPUS: `0x02EBF1A0`–`0x02EBF1F8` lie past `.data`'s raw end `0x01F7E400`)*), or this reader only runs while they
   hold them. The setters' `movsxd` is not itself evidence either way — every pointer value in this
   image is below `0x80000000`, so sign-extending `ecx` preserves a delivered pointer losslessly.
   *(Resolved 2026-09-30, SWE2-STRUCT for OPUS, DD batch 12, check R2: the first branch holds, and on the setters' own
   path. The descriptor's `+8` word is the buffer's address, not `3`, so every delivery stores a real pointer to the
   loaded `licd` board; see the correction in the tail read above.)*

### `0x02EBF198` — disposition

Allocated ~~and initialised~~ in BSS *(corrected 2026-10-02, OPUS: zero at load, past `.data`'s raw end `0x01F7E400`)*, never named by an instruction, reachable only through the adjacent
array's underflow index.

- **~~Initialised in the image.~~ BSS.** ~~The `.data` bytes hold `0x009224A8` — a non-zero pointer into the~~
  ~~image's static region, of the same shape as its fifteen neighbours (each holds a distinct~~
  ~~pointer-like initial value, e.g. `0x1A0` → `0x009234D8`). It is not reserved padding and it is not~~
  ~~BSS.~~ The slot and its fifteen neighbours lie past `.data`'s raw end `0x01F7E400`, so all are zero at load; `0x009224A8` is a path string's address, not this slot's value *(corrected 2026-10-02, OPUS: the section table gives `.data` a raw size of `0x18E400` from `0x01DF0000`; AG-4's answer in §7)*.
- **No instruction names it.** Zero direct absolute references across all 34,270 function bodies,
  with the positive control (`02EBF138`, 723 refs) passing; a raw `disp32` sweep of the code section
  for `0x2D9F198` finds zero candidates while finding `0x2D9F1A0`'s. It is also **not** among the ~~38~~ 37 *(corrected 2026-10-02, OPUS: 35 `lea`s and the two direct stores `00236C30+0x44` and `00236C30+0x401`)*
  slot addresses the STATIC registrar `00236C30` takes individually, and the `rep stosq` init covers
  `0x02EBF1A0`–`0x02EBF1F8`, starting one slot later.
- **The one identified reachability channel is index −1 of the `0x02EBF1A0` array.** `0055C0A8`
  computes `0x02EBF1A0 + 8·rax` with `rax = movsx byte [obj+0x558]` — a signed byte read directly
  from an input field, with no negative guard between the read and the dereference. If that field is
  ever `−1`, the access lands exactly on `0x02EBF198` and dereferences its initialised pointer.
  Whether the field can be `−1` is not established here — it is never written inside `0055BFF0`.
  *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale. `AG-4`'s 2026-09-18 answer in §7 reads the field's two
  writers. In `0055B3F0` the path that produces −1 also zeroes the reader's loop count. `0055CD40` copies a byte under
  `+0x570` bit 10, and that answer leaves the byte's data range unchecked. The same answer
  corrects the "initialised in the image" bullet above: the slot is BSS.)*
  *(2026-09-30, SWE2-STRUCT for OPUS, residue 3: the remainder is answered, and it is "never read at −1". The copied
  byte is the board picked in the licence screen's board-choice flow, not authored data. Whatever it holds, `0055B3F0`
  runs straight after the copy and its `0xFF` test covers both paths, so the reader's loop count is 0 whenever the
  index is −1. The `AG-4` answer's sentence on the `0055CD40` copy is corrected in §7, and the batch-12 phrase "the path that produces −1
  also zeroes the reader's loop count" holds for the copy path too. [Record](../_index/candidates/swe2struct-residue3-0930/README.md),
  checks G1-G9.)*
- **Bounded claim.** The slot is ~~populated at image load~~ zero at load (BSS) *(corrected 2026-10-02, OPUS: past `.data`'s raw end `0x01F7E400`)* and consultable through a signed-index
  underflow of the board-request array — most plausibly a default/spacer element the image ships so
  that index −1 still yields a valid object. It could also still be *written* through the registrar's
  base-plus-index binder path (`003845F0` with a data-driven index, per the AG-4 residual) without
  ever being named. What it is not proven to be is *written or read by name*: no binder, setter or
  consumer addresses it directly. *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12, check R3: no such binder path
  exists. `003845F0` writes only the slot it is handed, and its 42 calls hand it 41 distinct named slots. The "index"
  at `00237010` is slot 0's descriptor; see the correction under `AG-4` in §7.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**Input — SERVICE and CLIENT.** Boot mode 1 `0022B7E0` installs `InputControl_SetOneShotFrameCallback`. The request `0032E620` is also issued by the 177-byte Input-filed item-graphics loader.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Audio — SERVICE, not read.** `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`, which this page cites, calls two Audio-filed helpers (92 and 111 bytes).

**Presentation — SERVICE on ninety-seven edges, CLIENT on twenty (117 edges through 19 of this
page's functions; four subjects read in full; OPUS 2026-09-14, tier 1 from the shipping bytes).**
The count is large and the shape is not: **91 of the 117 edges are two functions**.

`002F1F40` takes 74 of them, and it has 75 callers in all — one short of the hub threshold this pass
uses, which is why it is still counted per-edge here. It resolves a display parameter: it reads the
global at `02F97348`, and **if `byte[global+0x2F0]` is `0xFF` it reads from `[object+0x50]` instead**,
which is the override-versus-default choice; it stamps the out-parameter with `0x80808080` before
doing anything else, so a caller that ignores the result gets a recognisable sentinel rather than
stale bytes; and it compares `byte[object+0x44]` against `0xA0`. `0036A190` takes another 17, and is
one line — `mov edx, 1 / jmp 0036A1A0` — onto a lookup that reads the handle at `022D89BC` and
retries `0036BC60` with a different argument when the first answer is null. The same `022D89BC`
handle is what `0036A100` reads on
[what the engine fixes at boot](../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md).

The remaining 26 edges are ordinary and spread over 17 subjects, the largest being `0022B7E0` with
4 — a startup sequence that calls six initialisers in a row — and `00214C30` with 4, which
short-circuits unless its index argument is zero.

So the crossing is **two shared resolutions with most of a layer reading them**, plus a tail of
single calls. Naming any one caller of `002F1F40` would describe less than one edge in
seventy-four. **Four of the 110 presentation bodies are read; the rest are counted.** Edge count and
subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

## The `0030A4E0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`0030A4E0` `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats`
(498 B) — the loadout evaluator the caller-trace above leaves open.
Early-exit through `00320AB0` (`0030A503` → jmp `0030A6BC` out);
`00318B40` (`0030A5D5`); per-slot `00323C60` compare of `word[rbx+8]`
against the stack row (`0030A64F`), writing `word[rdi+0x28] = ax`
(`0030A640`); then `00309480` classifies compatibility and the code is
stored at `dword[rdi+0x24]` (`0030A691`/`0030A6A0`); finally
`002FEF30` `BattleStats_RebuildEffectiveStatsAndAffinityState` with
`rdx = rdi` (derived-stats buffer), `r8 = rbx` (equipment record)
(`0030A6B7`).

| member | role | interior |
| --- | --- | --- |
| `00309480` `Equipment_ClassifyCandidateLoadoutCompatibilityReason` (615 B) | reason-code classifier — `(ecx, edx, r8w, r9w)`; `0031EA90` ×4 id/category lookups on the word args (`003094AF`–`003094D7`), then `003096F0` twice (`00309527`, `00309567`) | [`00309527`](../_index/ADDRESS-INDEX.md) |
| `003096F0` `Equipment_CheckMatchingSecondaryPartnerSelectedOrOwned` (475 B) | secondary-slot probe — `00322C50` (`00309706`), then `[02EBF0F8]` context + `0020E600` row lookups (`00309716`/`0030972B`/`00309735`/`0030973F`) | [`0030972B`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00320AB0`, `00318B40`, `00323C60`,
`002FEF30`, `0031EA90`, `00322C50`, `0020E600`. The `02EBF0F8` cell is
the shared equipment-state context the row lookups key on.

## The `00378A60` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00378A60` (199 B) — the map-pack init that publishes
`r14d`→`02EBF9C8`/`02ADD0F4` and `ebx`→`02ADD118` (`00378A82`–
`00378A95`), calls `003C63A0`/`0032F3D0` (`00378AA4`/`00378AAB`),
compares/stores `02ADD0DC`/`02ADD0EA` (`00378AB4`/`00378AC9`), then
enters sibling root `00378230` (`00378ACF` — shared edge, not owned).

| member | role | interior |
| --- | --- | --- |
| `0026EAF0` (56 B) | double callback registration — `rdx = 0026EDB0` → `0209A670` then `0209A668`, each `003EC860`/`003ECF70`/`0026E640` (`0026EB02`/`0026EB07`/`0026EB0C`, `0026EB18`) | [`0026EB02`](../_index/ADDRESS-INDEX.md) |
| `003784A0` (143 B) | lazy-init wrapper — `qword[02ADD000]` vs `rbx` gate (`003784A8`), `0026EAF0` + `003697F0` (`003784B1`/`003784BD`), store + `02ADD0E0 = -1` (`003784C2`/`003784C9`), `02ADD0A0` check (`003784D3`) | [`003784C2`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003C63A0`, `0032F3D0`, `00378230`,
`003EC860`, `003ECF70`, `0026E640`, `003697F0`.

## The `00379A10` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00379A10` (~46 B into a `0x250` stack-cookie frame —
`00379A16`/`00379A27`).

| member | role | interior |
| --- | --- | --- |
| `001805D0` | `001A9930(rcx)` non-null gate — same resolver as `00180620` (`001805D9`/`001805E1`) | [`001805D9`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001A9930`.

## Thirty of these tables have a proven shape and no declared type (OPUS)

Measured 2026-09-20 (OPUS), while looking for the consumer that reads a licence node record.

**The search that led here failed in a way worth recording.** No body in the image both references
the `license_data` slot at `02EBF038` and indexes by its `0x18` record size - not as
`imul reg, reg, 0x18`, and not as the `lea r,[r+r*2]` / `shl r,3` idiom a compiler emits for ×24.
**Because the indexing is generic**: the stride comes from the descriptor at runtime, so no literal
record size appears in the code at all. That is why a stride-shaped search finds nothing, and it is
the same lesson `PApplication` taught - the search shape was wrong, not the searching insufficient.

**What the registry then shows.** The table above binds **32 authored data files** to slots, class
ids, pack entries and **shapes taken from the `st2e` pack's own metadata** - `count × record size`,
measured rather than inferred. Cross-referencing every one against `_types`:

| | |
|---|---:|
| authored tables with a shape in this registry | **32** |
| mentioned anywhere in a declared type | **2** (`license_data`, `status_data`) |
| **with a proven record size and no type row** | **30** |

**That is a whole dimension's gap in one number**, and it is unusually cheap to close by the store's
own standard: the ruling made for the 162 Phyre extents says *"a type with `size=UNRESOLVED` cannot
be allocated by a reconstruction at all, so a known size with honestly declared gaps is strictly more
useful"*. Every one of these thirty has a known size **and** a known count **and** a name.

**Deliberately not mass-declared here.** Thirty rows with proven extents and empty interiors is
either a real step or thirty rows of bookkeeping, and which one depends on a convention question
this file cannot settle: whether the store wants shells for authored records it can size but not
read. `LicenseNodeRecord` was declared as the single worked example, because S-31's verdict turns on
it; the other twenty-nine are recorded here as a measured population rather than created on my own
judgement.

**What would make them more than shells** is the generic accessor that resolves a descriptor to a
record - one body, shared by all 32 tables, which is why finding it is worth more than carving any
single table.


## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

These paragraphs cover only the edges that the `UQ-81` answer brings in by citing the query-record filler
`0031C5D0` (its jump table and two class arms). The gate credits each layer name below for all of that
layer's edges into this page; the ones not listed here are not dispositioned.

**Gameplay — PEER.** The filler and the validator `00322C50` sit on gameplay paths: the gameplay body `0023A570` calls the
validator, for example. This page relies only on how the filler's arms treat classes 22, 23 and 24.

**UI — PEER.** The filler's name output feeds UI text builders through the shared name formatter. This page
claims only that class 24 yields a name and classes 22 and 23 do not.

`0037C2E0` (224 B) is the deferred init pump the registry census already lists under `0022B7E0`: the `02EBF3DC` state byte cycles - states `0`/`1` compare the `02EBF3DD` index against `003204B0()`'s count and `00320B30`-step records, `002EAE20`-allocating a `02ADD948` object when rows arrive (state `2`); state `2` probes it through `0024C70`→`002E4C70`, refcounts via `002EAF70` or flag-writes `002EBE20(obj, 1)`; state `3` ~~exits~~ loops back to state `1` and state `4` exits *(corrected 2026-10-02, OPUS: `0037C2E0+0x29` `mov ebx, 1` loops for state 3; state 4 reaches `0037C2E0+0xBC`, stores 4 and returns 0)* - the `4`-write and `0`/`1` return encode done vs still-pumping

Interior anchor `0037C35E` (function `0037C2E0`).
- **ActorEntity — CLIENT and SERVICE (53 edges).** 24 inbound (ActorEntity bodies `BattleUnit_ApplyUnitDefinition` (0023A570), `0037B4D0`, `ActorResource_BeginPrimaryPayloadLoad` (00330310) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `0032E400`, `BattleUnit_ApplyUnitDefinition` (0023A570)); 29 outbound (page-cited `AiOrder_EvaluateTargetSelector` (00301AD0), `BattleMenu_BuildCommandEntryList` (0031EB20), `0037B4D0` call ActorEntity bodies `BattleUnit_GetBySlotIndex` (00236820), `BattleUnit_GetSlotCount` (00236850), `Actor_GetWorldPosition` (00265020)). Substantive edges include `BattleSystem_InitializeAreaState` (002342F0) is called by `ActorSystem_InitializeManagerRuntime` (0026CE60); `00238260` is called by `BattleStorage_InitializeWorkArrays` (002368D0); `BattleUnit_ApplyUnitDefinition` (0023A570) is called by `BattleUnit_TeardownAndDespawn` (00300E40); `BattleUnit_ApplyUnitDefinition` (0023A570) is called by `BattleGroup_RefreshFourActorDefinitions` (003266C0); the remaining edges run through shared helpers the page cites.
- **CombatAI — CLIENT and SERVICE (43 edges).** 28 inbound (CombatAI bodies `AiOrder_EvaluateTargetSelector` (00301AD0), `AiOrder_EvaluateAndResolveActionTarget` (003014C0), `BattleTarget_ComputeSurfaceDistanceBetweenUnits` (0031E6F0) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `BattleUnit_GetNavigationClearanceRadius` (0030A130), `BattleUnit_BuildFilteredFourSlotUnitBuffer` (0030A880)); 15 outbound (page-cited `AiOrder_EvaluateTargetSelector` (00301AD0), `BattleStats_InitializeDefinitionRecord` (0023AC80), `00233C10` call CombatAI bodies `GambitRuntime_RebuildAllOrderSets` (00327F80), `GambitTargetDefinition_BindAndBuildMenuLookup` (00238880), `GambitRuntime_RebuildOrderSetForStatsRecord` (00327DE0)). Substantive edges include `00233C10` calls `GambitRuntime_RebuildAllOrderSets` (00327F80); `00236C30` calls `GambitTargetDefinition_BindAndBuildMenuLookup` (00238880); `BattleStats_InitializeDefinitionRecord` (0023AC80) calls `GambitRuntime_RebuildOrderSetForStatsRecord` (00327DE0); `BattleStats_InitializeDefinitionRecord` (0023AC80) calls `GambitConfig_InitializeThreeBanksFromBasePairs` (00326030); the remaining edges run through shared helpers the page cites.
- **CombatAction — CLIENT and SERVICE (59 edges).** 30 inbound (CombatAction bodies `0030CBE0`, `BattleUnit_AdvanceStandardActionState` (00304850), `00320E10` call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `BattleStats_GetByBattleSlotIndex` (00320A40), `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360)); 29 outbound (page-cited `Battle_ProcessActionTarget` (00307300), `BattleMenu_BuildCommandEntryList` (0031EB20), `AiOrder_EvaluateTargetSelector` (00301AD0) call CombatAction bodies `BattleTarget_HasLow16EligibilitySuppression` (0030B9B0), `BattleUnit_CancelAndResetCurrentAction` (003105D0), `BattleTarget_ClassifyRelationshipClass` (0030AB40)). Substantive edges include `BattleSystem_InitializeAreaState` (002342F0) calls `00306570`; `BattleSystem_InitializeAreaState` (002342F0) calls `BattleActionSnapshot_ResetPool` (0030E010); `BattleSystem_InitializeAreaState` (002342F0) calls `BattleAction_ResetPendingQueueBanks` (0030FE60); `BattleStorage_InitializeWorkArrays` (002368D0) calls `BattleAction_ResetPresentationSlotPool` (0030CF40); the remaining edges run through shared helpers the page cites.
- **CombatFormula — CLIENT and SERVICE (32 edges).** 9 inbound (CombatFormula bodies `BattleFormula_ApplyTargetResult` (003112F0), `BattleFormula_DispatchPostResultEvents` (00469EC0), `BattleStats_ModifyHPAndProcessLethalState` (00300530) call page-cited `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360), `BattleStats_GetByBattleSlotIndex` (00320A40), `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0)); 23 outbound (page-cited `Battle_ProcessActionTarget` (00307300), `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360), `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30) call CombatFormula bodies `BattleStats_FindOwningBattleUnit` (0031B860), `BattleFormula_ApplyTargetResult` (003112F0), `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30)). Substantive edges include `BattleUnit_ApplyUnitDefinition` (0023A570) calls `BattleStats_InitializeDefinitionRecord` (0023AC80); `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30) calls `002F9180`; `BattleStats_RebuildEffectiveStatsAndAffinityState` (002FEF30) calls `002F8E50`; `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0) is called by `BattleFormula_ApplyTargetResult` (003112F0); the remaining edges run through shared helpers the page cites.
- **Items — SERVICE (1 edge).** 1 outbound (page-cited `00236C30` call Items bodies `00238660`). Substantive edges include `00236C30` calls `00238660`.
- **Items_Equipment_Shops_License — CLIENT and SERVICE (67 edges).** 47 inbound (Items_Equipment_Shops_License bodies `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` (0030A4E0), `BattleStats_SetEquipmentSlotByMappedId` (0031A510), `Equipment_BuildRecommendedLoadoutForMappedStats` (002F9F20) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0), `BattleStats_GetByMappedBattleSlot` (00320AB0)); 20 outbound (page-cited `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` (0030A4E0), `0055CD40`, `BattleStats_InitializeDefinitionRecord` (0023AC80) call Items_Equipment_Shops_License bodies `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (0030B6A0), `BattleStats_SetLicenseNodeStateAndApplySideEffects` (00323910), `BattleStats_SetEquipmentSlotDirect` (0031A630)). Substantive edges include `00233C10` calls `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (0030B6A0); `SaveRuntime_RebindImageBackedGameplayState` (00238A80) calls `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (0030B6A0); `BattleStats_InitializeDefinitionRecord` (0023AC80) calls `BattleStats_SetLicenseNodeStateAndApplySideEffects` (00323910); `BattleStats_InitializeDefinitionRecord` (0023AC80) calls `BattleStats_SetEquipmentSlotDirect` (0031A630); the remaining edges run through shared helpers the page cites.
- **Movement — CLIENT and SERVICE (85 edges).** 52 inbound (Movement bodies `0026EAC0`, `0026EAF0`, `0026E760` call page-cited `Vector3_ComputeXZDistance` (004686D0), `0026E640`, `003EC860`); 33 outbound (page-cited `0037B4D0`, `BattleSystem_InitializeAreaState` (002342F0), `Battle_ProcessActionTarget` (00307300) call Movement bodies `Actor_SetDesiredMovementHeading` (0026A0D0), `Actor_SetFacingHeading_Variant1` (0026B620), `BattleUnit_GetNavigationClearanceRadius` (0030A130)). Substantive edges include `0022FF10` is called by `00233230`; `0022FF10` calls `0022F050`; `BattleSystem_InitializeAreaState` (002342F0) calls `00322220`; `BattleSystem_InitializeAreaState` (002342F0) calls `0033A380`; the remaining edges run through shared helpers the page cites.
- **Party — CLIENT and SERVICE (19 edges).** 11 inbound (Party bodies `00328BD0`, `00304180`, `PartyConfiguration_CollectSelectorsOutside07To25` (00320800) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0), `BattleStats_GetByMappedBattleSlot` (00320AB0)); 8 outbound (page-cited `AiOrder_EvaluateTargetSelector` (00301AD0), `BattleUnit_CommitAction` (0030F760), `BattleMenu_BuildCommandEntryList` (0031EB20) call Party bodies `BattleUnit_ResolveByFocusHandle` (0031B7E0), `PartyRoster_GetActorBySlot` (00263750), `PartyFocus_IsCurrentPackedActorHandle` (003273B0)). Substantive edges include `AiOrder_EvaluateTargetSelector` (00301AD0) calls `PartyFocus_IsCurrentPackedActorHandle` (003273B0); `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0) is called by `00328BD0`; `0037B4D0` calls `PartyRoster_IsFourSlotIndex` (002647C0); the remaining edges run through shared helpers the page cites.
- **RNG_Random_Selection — SERVICE (3 edges).** 3 outbound (page-cited `0022B7E0`, `BattleSystem_InitializeAreaState` (002342F0), `BattleData_ResolveWeightedId` (00308EC0) call RNG_Random_Selection bodies `RNG_MT19937_NextU32_Thunk` (00379CD0), `RNG_SharedGameplayLCG_SetState` (00328D80), `RNG_SharedGameplayLCG_NextU32` (00328370)). Substantive edges include `BattleSystem_InitializeAreaState` (002342F0) calls `RNG_SharedGameplayLCG_SetState` (00328D80); `BattleData_ResolveWeightedId` (00308EC0) calls `RNG_SharedGameplayLCG_NextU32` (00328370); the remaining edges run through shared helpers the page cites.
- **Rewards_Progression_Economy — CLIENT and SERVICE (18 edges).** 8 inbound (Rewards_Progression_Economy bodies `BattleUnit_ProcessDefeatRewardsAndLoot` (00312280), `0030C470`, `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (0030C650) call page-cited `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (0030C650), `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0), `BattleStats_GetByMappedBattleSlot` (00320AB0)); 10 outbound (page-cited `Loot_RollDropEntries` (003180F0), `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (0030C650), `BattleSystem_InitializeAreaState` (002342F0) call Rewards_Progression_Economy bodies `Loot_InitializeWorldPickupPool` (00319B10), `0030C470`, `002F9B20`). Substantive edges include `BattleSystem_InitializeAreaState` (002342F0) calls `Loot_InitializeWorldPickupPool` (00319B10); `BattleStats_InitializeDefinitionRecord` (0023AC80) calls `0030C470`; `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (0030C650) is called by `0030C470`; `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (0030C650) calls `002F9B20`; the remaining edges run through shared helpers the page cites.
- **SaveLoad — CLIENT (2 edges).** 2 inbound (SaveLoad bodies `00280140` call page-cited `00233C10`, `SaveImage_GetActiveRuntimeBuffer` (002EF640)). Substantive edges include `00233C10` is called by `00280140`; the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — CLIENT and SERVICE (24 edges).** 22 inbound (Save_Load_Settings bodies `SaveImage_FinalizeHeaderAndChecksum` (00583D60), `002EF300`, `SaveRuntime_RebindImageBackedGameplayState` (00238A80) call page-cited `SaveImage_GetActiveRuntimeBuffer` (002EF640), `00236740`, `SaveRuntime_RebindImageBackedGameplayState` (00238A80)); 2 outbound (page-cited `00233C10`, `SaveRuntime_RebindImageBackedGameplayState` (00238A80) call Save_Load_Settings bodies `SaveImage_GetActiveRuntimeBuffer` (002EF640)). Substantive edges include `00236740` is called by `SaveImage_FinalizeHeaderAndChecksum` (00583D60); `SaveRuntime_RebindImageBackedGameplayState` (00238A80) is called by `SaveRuntime_ResetActiveImageAndRebindState` (002EF650); `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (0030B6A0) is called by `SaveRuntime_RebindImageBackedGameplayState` (00238A80); `0032E620` is called by `002EF300`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT (35 edges).** 35 inbound (Script_VM_Native_Bridge bodies `0050F3F0`, `0050CDE0`, `003580C0` call page-cited `BattleStats_GetByMappedBattleSlot` (00320AB0), `002EAE20`, `002E4C30`). Substantive edges include `00236740` is called by `0050F3F0`; `MapRef_GetAuxValue0` (00264F40) is called by `0050CDE0`; `002E4C30` is called by `003580C0`; `002E4C30` is called by `0034B120`; the remaining edges run through shared helpers the page cites.
- **Spawn_Encounter_Lifecycle — CLIENT and SERVICE (5 edges).** 2 inbound (Spawn_Encounter_Lifecycle bodies `Spawn_ApplyScriptSelectedUnit` (0023A3B0), `SpawnUnit_FinalizeSpawnEntryActivation` (0023A410) call page-cited `BattleUnit_ApplyUnitDefinition` (0023A570), `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0)); 3 outbound (page-cited `BattleSystem_InitializeAreaState` (002342F0), `BattleUnit_ApplyUnitDefinition` (0023A570) call Spawn_Encounter_Lifecycle bodies `SpawnKeep_RotatePersistenceBanksForAreaTransition` (00233780), `SpawnGroup_ResetLifecycleLedger` (00307090), `SpawnKeep_ResolvePrimaryEntry` (00236100)). Substantive edges include `BattleSystem_InitializeAreaState` (002342F0) calls `SpawnKeep_RotatePersistenceBanksForAreaTransition` (00233780); `BattleSystem_InitializeAreaState` (002342F0) calls `SpawnGroup_ResetLifecycleLedger` (00307090); `BattleUnit_ApplyUnitDefinition` (0023A570) is called by `Spawn_ApplyScriptSelectedUnit` (0023A3B0); `BattleUnit_ApplyUnitDefinition` (0023A570) calls `SpawnKeep_ResolvePrimaryEntry` (00236100).
- **Status_Periodic_Terminal — CLIENT and SERVICE (29 edges).** 14 inbound (Status_Periodic_Terminal bodies `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0), `BattleStats_RemoveStatusesFromMaskAndRecompute` (0030F690), `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360) call page-cited `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360), `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0), `BattleEncodedId_IsValidForClass` (00322C50)); 15 outbound (page-cited `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360), `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0), `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0) call Status_Periodic_Terminal bodies `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0), `BattleStats_ChangeStatusAndProcessSideEffects` (0030E360), `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` (0030E130)). Substantive edges include `BattleSystem_InitializeAreaState` (002342F0) calls `BattleStats_RemoveStatusMode0` (0030E990); `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0) calls `BattleStats_RemoveAllMode0StatusesAndRecompute` (0030E8F0); `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0) calls `BattleStats_RecomputeDerivedStateAndAutoStatuses` (0030FED0); `BattleUnit_ExecuteDirectStateCommandOrder` (002FDDA0) calls `BattleStats_ClearStatusLayer0AndProcessSideEffects` (0030E970); the remaining edges run through shared helpers the page cites.
- **World — CLIENT and SERVICE (10 edges).** 7 inbound (World bodies `00378540`, `00266D10`, `003847B0` call page-cited `AreaData_BindAndRebaseSectionDescriptor` (003845F0), `BattleSystem_InitializeAreaState` (002342F0), `0032E400`); 3 outbound (page-cited `00236C30`, `00378230`, `00378A60` call World bodies `003C63A0`, `003847B0`). Substantive edges include `BattleSystem_InitializeAreaState` (002342F0) is called by `00266D10`; `00236C30` calls `003847B0`; `0032E400` is called by `00378540`; `0032E620` is called by `00378540`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (96 edges).** 62 inbound (WorldAreaField bodies `00236C30`, `AreaArd_LoadOrUnloadFieldResource` (003EA820), `00378A60` call page-cited `0036C660`, `0032E400`, `003846F0`); 34 outbound (page-cited `00378A60`, `00331990`, `BattleSystem_InitializeAreaState` (002342F0) call WorldAreaField bodies `AreaData_BindAndRebaseSectionDescriptor` (003845F0), `FieldData_GetActiveFieldRecordBit15` (00377C20), `003846F0`). Substantive edges include `001805D0` is called by `00379A10`; `BattleSystem_InitializeAreaState` (002342F0) calls `002FA520`; `00236C30` is called by `00238850`; `00236C30` calls `003846F0`; the remaining edges run through shared helpers the page cites.
- **CoreRuntimeScheduling - CLIENT and SERVICE (17 edges).** 12 inbound (CoreRuntimeScheduling bodies `0022B7E0`, `0022A0B0`, `0022A580` call page-cited `00324510`, `00184960`, `0032E520`); 5 outbound (page-cited `00184960`, `00233C10`, `0046AB10` call CoreRuntimeScheduling bodies `001EDE70`, `001EDEF0`, `00229EA0`).
- **PlatformOnlineAchievements — CLIENT (1 edge).** 1 inbound (PlatformOnlineAchievements bodies `00315E90` call page-cited `BattleEncodedId_DispatchQueryMode0Value` (00309EC0)).

## The inverse reader: three row-to-index divides over the action table (OPUS, 2026-10-02)

From FABLE's reviews of ASTRA's [`ov42-sequence-queue-source`](../_index/candidates/fable-review-astra-ov42-sequence-queue-source-1002/REVIEW.md)
and [`ov42-kind-row-coherence`](../_index/candidates/fable-review-astra-ov42-kind-row-coherence-1002/REVIEW.md), both ACCEPT-WITH-NARROWING.
- OPUS re-read the six descriptor reads, the divides and the queue store at the bytes
  ([`ov42_check.py`](../_index/candidates/opus-ov42-typestore-1002/ov42_check.py)).
- The classifier's selector values and the return use rest on FABLE's review evidence (`rv_kindrow.py`).

The usual access multiplies an index by the slot `02EBF138` header's `+0x08` stride. Three sites run it backwards:
they turn a row pointer into an index.
- **The sites.** `00306760` + 0x138 .. + 0x158 (the kind-4 arm), `00306760` + 0xAD .. + 0xCD (the kind-3 arm) and
  `00306BD0` + 0x92 .. + 0xB2.
- **The arithmetic.** D = (low32(row) - low32(`0020E600`(header `+0x0C`))) mod 2^32 (a 32-bit `sub`), then an
  UNSIGNED 32-bit `div` by the zero-extended u16 header `+0x08`, with EDX zeroed first.
- **Two descriptor loads.** Each site loads the `02EBF138` QWORD twice, with the lookup call between the loads:
  `+0x0C` comes from the first load and `+0x08` from the second. Equality and stability are not established.
- **Precondition: recordStride > 0.** No zero test sits between the WORD load and the `div`. A zero stride would
  fault (#DE in emulation; a source prediction, not an observed fault).
- **What each site does with the quotient.**
  - Kind 4 at `00306760` narrows the quotient to its low 16 bits. FFFF becomes a queue DWORD FFFFFFFF; anything else
    becomes (w - 0xD0) mod 2^32, stored at `022C2178` (`00306760` + 0x174).
  - Kind 3 passes the full 32-bit quotient on as EDX.
  - `00306BD0` classifies the full 32-bit quotient (`add eax, -0x94`, unsigned `cmp eax, 0x7f`, a 128-byte selector).
    It publishes kind 4 exactly for q 208..225, and kind 7 for every q outside 148..275.
- **Return use at `00306BD0` + 0x86.**
  - The RAX / flags of the callee `0032FC30` are never read: a 16-byte leaf overwrites RAX, and + 0x92 overwrites it
    again.
  - The `0032F6E0` return is tested (+ 0x57).
- **Open, as the register's OV-42 states.** Row-to-kind / caller / owner consistency. A quotient equals an action id
  only for a row on the descriptor's stride grid.

## The action table's forward readers, two more inverse readers and the binder's ABI (OPUS, 2026-10-02)

From FABLE's reviews of ASTRA's [`ov42-caller-row-preconditions`](../_index/candidates/fable-review-astra-ov42-caller-row-preconditions-1002/REVIEW.md),
[`ov42-caller-quotient-bound`](../_index/candidates/fable-review-astra-ov42-caller-quotient-bound-1002/REVIEW.md),
[`ov42-terminal-resource-helper`](../_index/candidates/fable-review-astra-ov42-terminal-resource-helper-1002/REVIEW.md) and
[`ov42-action-table-binding`](../_index/candidates/fable-review-astra-ov42-action-table-binding-1002/REVIEW.md), all ACCEPT-WITH-NARROWING.
OPUS re-read every instruction named here at the bytes ([`batch6_check.py`](../_index/candidates/opus-ov42-batch6-routes-1002/batch6_check.py), 63 checks,
FAILS 0). Statements marked *(FABLE)* rest on FABLE's review scripts, not on this record's checks.

**The forward readers.** Three routines build a row pointer from an index through the slot `02EBF138` header. Each
multiplies by the `+0x08` stride and adds the product to the decoded `+0x0C` base in 32 bits.
- `00304850`: the index is the WORD at unit `+0x714`, latched at + 0x3D (`movzx r13d, word ptr [rsi + 0x64]`,
  RSI = unit + 0x6B0). An unsigned compare against 0x21E (+ 0x8E / + 0x92) leaves before the phase switch.
  - The row build: `+0x0C` at + 0xB3 / + 0xC7, the stride at + 0xD9, `imul ecx, eax` at + 0xE1 and `add r15d, ecx`
    at + 0xE4. The row is zero-extend32(low32(lookup) + id * stride).
  - The row is then used as a pointer, so the table must lie below 4 GB.
- `0030D160`: the index is the incoming DX (+ 0x27). The build: `+0x0C` at + 0x59 / + 0x6D, the stride at + 0x7F,
  and a 32-bit add into RSI at + 0x89.
- `00305430`: an unsigned 16-bit `cmp dx, 0x115` bounds the index (+ 0x16 / + 0x23). Three row builds follow: `+0x0C`
  at + 0x31 / + 0x46, + 0x79 / + 0x8E and + 0x162 / + 0x177, with the stride at + 0x58, + 0xA0 and + 0x186.
- The stride is re-read after each lookup call, the same two-load shape as the inverse sites. A positive stride is
  assumed by every inverse reader, and no forward site checks the descriptor's fields.

**Inverse readers four and five: the terminal cost helper `00305640`.**
- The sites: `+0x0C` at + 0x2E, the stride at + 0x4B, then `div r10d` at + 0x50. A second pair has `+0x0C` at + 0x128,
  the stride at + 0x13C and `div ecx` at + 0x143. Both are unsigned 32-bit divides with no zero test.
- Widths: the two comparators get `movzx edx, di` (+ 0x81, + 0x8C), the quotient mod 65536. The full 32-bit
  recomputed quotient is passed on at + 0x14A (`mov edx, eax`).
- Mode: + 0xA3 `test r12d, r12d` and + 0xA8 `setne` normalise the incoming flag to 0 / 1. The two stats writers
  get 16 plus that bit, not the raw flag *(FABLE)*.
- Own non-stack writes: DWORD unit `+0xE58` := 0 (+ 0x73) and WORD unit `+0xDC8` := 0xFFFF (+ 0x7A). Both are gated
  by unit, record and record byte `+5` == 0 *(FABLE)*.
- NULL preconditions: unit (+ 0x99 reads unit `+0x698` unconditionally), the record (+ 0xC4 reads its WORD `+0x28`),
  the descriptor, and a stride > 0 at both divides.

**The section binder's ABI** (`003845F0`, the AG-12 block above, as corrected):
- Entry: RCX = slot, RDX = descriptor. The action-table caller `00237FC0` passes RCX = &`02EBF138` and RDX = its own
  incoming ECX sign-extended (+ 0xF `movsxd`). FABLE's review traces that DWORD to directory `+0x3C`.
- `*slot = desc` (QWORD, + 0x4) comes before the null test and every rebase. `+0x0C` is addressed through RDX
  (+ 0x10); `+0x10`, `+0x18`, `+0x1C` and `+0x14` go through reloads of `*slot` (+ 0x21, + 0x32, + 0x43, + 0x54).
- The rebase is NOT idempotent: x != 0 becomes low32(x + low32(desc)), and there is no already-rebased flag.
- Widths: the encoder `0020E620` subtracts the low DWORD of `01F83530`, and the decoder `0020E600` zero-extends and
  adds the full QWORD. Only the low-32 round trip is exact. Full 64-bit identity needs the QWORD's upper half to be 0.
- Preconditions: valid, separate slot and descriptor storage, and sub-directory storage disjoint from the header.
