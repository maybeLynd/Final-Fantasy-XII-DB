---
system: The five parallel slot maps
category: 11-Party
status: AUDITED
owner_layer: PrimaryOwner:Party — the battle-state block's field map owns these offsets and declares Party; this page reads the same structure through 0031B9F0
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN159 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN159 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: pair-frontier-repos-55
  crossref_clean: true
  reopened_count: 0
---

# The five parallel slot maps

**The first candidate the pair frontier produced, and it corrects a published reading.**

`+0x5A7E` was ranked top by *five functions touching one offset, four of them documented, no document
citing two of them.* Reading two of the five settles what the offset is — **and it is not what the
party work took it for.**

## Five tables, not two halves of one

```c
BattleSlotMap_ResolveMappedBattleSlot(id, class):
    if (!IsValidForClass(0x17, id)) return 0xFF;
    class 0 -> byte at base + 0x5A48 + id*2
    class 1 ->              + 0x5A5A + id*2
    class 2 ->              + 0x5A6C + id*2
    class 3 ->              + 0x5A7E + id*2
    class 4 ->              + 0x5A90 + id*2
```

**Five bases, exactly `0x12` apart — eighteen bytes, nine `u16` slots each.** The id is validated by
the registry's **class 23**, the definition-selector table.

**The dispatch is a subtract-and-test chain, not a table**, and the fifth arm shows the shape exactly:

```asm
0031BA1E  test  ebx, ebx                 ; class 0?
0031BA22  sub   ebx, 0x1                 ; class 1?
0031BA27  sub   ebx, 0x1                 ; class 2?
0031BA2C  sub   ebx, 0x1                 ; class 3?
0031BA31  cmp   ebx, 0x1                 ; class 4?
0031BA34  jnz   0x0031BA11               ; anything else -> 0xFF
0031BA36  mov   rax, qword ptr [0x02EBF190]
0031BA3D  movzx eax, byte ptr [rax + rdi*0x2 + 0x5a90]
0031BA11  mov   al, 0xff                 ; the refusal
```

> **A class outside 0–4 returns `0xFF`** — the same one-byte "empty" convention this engine uses for
> handle spaces — **and the refusal is the fallthrough, not a guard at the top.**

**ANCHORING NOTE, 2026-09-03.** This document originally named the resolver **in pseudocode and cited
no address inside it**, while its central claim — five bases — rests entirely on that body. **The pair
census then reported this very offset as still uncompared**, because no document cited two of its
touchers *by address*.

> **A document that names a function without citing it is invisible to every instrument here** — the
> read-but-uncited mode, in the document written to demonstrate the instrument that finds it.

> **`+0x5A7E` is the fourth of five parallel maps. It is not "the reserve".** The reserve is the upper
> indices *inside* one map; **these five are five whole maps.**

## They start as four copies of the first

The initialiser fills **only `+0x5A48`** — nine entries, from a byte table at `01EED260`, each validated
and each either registered or defaulted to `0xFFFF` — and then:

```asm
00329DBB  movzx  ecx, byte ptr [0x01EED260]
00329DC2  mov    dword ptr [rax + 0x5aa4], ecx     ; the source's first byte, kept separately
00329DE3  movups xmm0, xmmword ptr [rcx + 0x5a48]  ; sixteen bytes of map 0
00329DEA  movzx  eax,  word ptr [rcx + 0x5a58]     ; ...and the last two
00329DF6  movups xmmword ptr [rcx + 0x5a5a], xmm0  ; -> map 1
00329DFD  mov    word ptr [rcx + 0x5a6a], ax
```

**and the same 16 + 2 pattern again into `+0x5A6C`, `+0x5A7E` and `+0x5A90`.**

> **All five maps begin identical.** They are not five different assignments — **they are one
> assignment copied four times, and whatever makes them differ happens later, elsewhere.**

**That is why five documents each touch a different one and none of them mentions another:** each
subsystem reads *its own* copy, and nothing in any single function reveals that four siblings exist.

## What the classes are is not established here

*(answered elsewhere: classes 0 to 3 are named by their callers — active-party-reserve-and-the-moment-the-leader-changes.md §2b — and SM-6 of CONTRACT-the-five-parallel-slot-maps.md makes map 0 the live configuration and maps 1–4 derived from it; 2026-10-02, OPUS)*

**The resolver takes the class as a parameter and does nothing with it but choose a base.** Nothing in
either function names the five, and **no caller was read.** The document that cites each toucher may
know what its own class means; **this document establishes only that there are five and that they are
born equal.**

**A dword at `+0x5AA4` takes the source table's first byte** and is not part of any map *(answered: it is the preferred definition selector, the party leader — the battle-state block field map's `+0x5AA4` row; 2026-10-02, OPUS)*.

## Do the four copies ever diverge? A measured answer with a hole in it

**A displacement census over the five 18-byte ranges** (`+0x5A48 … +0x5AA2`) gives **66 sites: 60
reads, 6 writes.**

| range | writers |
|---|---|
| **map 0** (`+0x5A48`) | the initialiser, **and one other function — `00329080`** |
| maps 1–4 | ~~**the initialiser only**, and only at each copy's trailing two bytes~~ **the initialiser and `BattleGroup_RefreshFourActorDefinitions` `003266C0`**, which addresses them through `rdi = block + 0x5A48` (`003266D4`) and so is invisible to this census — see the correction below |

> **~~Within this instrument's reach, nothing writes maps 1–4 after the copy.~~** *(corrected 2026-10-02, OPUS: the refresher `003266C0` writes all four through `rdi = block + 0x5A48` — `00326717`, `00326720`, `0032673E`, `00326747` and its mode arms; the 2026-09-14 correction below)* Only map 0 has a second
> writer, which fits map 0 being the one the initialiser fills before duplicating.

~~**So "four views allowed to drift" is not supported by this measurement** — as far as a
displacement-addressed census can see, **they are four copies that nothing has been found to change.**~~

> **CORRECTED 2026-09-14 (FABLE, `OPUS-NOTICE-FABLE-SLOTMAP-CLASS0`): the maps do diverge, and the hole named
> below is where the writer was.** `BattleGroup_RefreshFourActorDefinitions` `003266C0` loads the block pointer
> and adds `0x5A48` to it (`003266C8`–`003266D4`), then works through that register. It copies map 0 into maps 1
> and 3 (`00326714`–`00326724`) and sets map 1's selectors `[4..8]` to `0xFFFF` (`00326728`–`00326730`). It
> copies map 1 into maps 2 and 4 (`00326735`–`0032674B`), then rewrites selectors `[0..3]` of maps 1, 2 and 4
> per battle runtime mode (`003268BD`–`003268DC`). One branch restores map 4 from a copy taken on entry
> (`003266F4`–`00326709`, restored `003268F8`–`00326901`). **The five are also not peers.** Map 0 is the live party configuration of
> [the battle state block field map](Battle-State-Block/the-battle-state-block-field-map.md) (`[0..3]` active,
> `[4..8]` available; the block reset and ten `PartyConfiguration_*` functions address it — `003172E0`, `00326110`, `003261D0`, `003273D0`, `003286E0`, `003287A0`, `003288F0`, `00328B20`, `00328DB0`, `00329080`), and maps 1–4 are
> battle mappings derived from it. Class 0 of `0031B9F0` therefore returns the low byte of a live party selector.

**The two selector-removal bodies, re-read 2026-09-15** (research import — `XIIONLINE_NATIVE_CALL_ROADMAP_PLAN.md`
calls them `RemovePartyMember` / `RemoveGuestBattleMember`; the bodies carry GFZ names
`PartyConfiguration_RemoveSelector00To06` `00328B20` / `...07To25` `003288F0`). Both take a member
id in `cl`, range-check it (`cl ≤ 6` vs `7 ≤ cl ≤ 0x19` — the party/guest split the roadmap names),
scan map 0's nine entries for a matching low byte, clear that slot's u16 selector to `0xFFFF` and
copy the 18-byte map to the fixed pair `022C2580` (16 B `movups`, `00328B74`) + `022C2590`
(2 B `mov word`, `00328B83`) — one destination, and the *same* `022C2580` the `lea` at
`00328B65` indexes for the `0xFFFF` clear — then resolve the id's `0x1C8`-stride
block at `+0x0008` (bounded `≤ 0x27` — the same `+0x0008` array §"a link to BattleUnit" maps) and
call `00323540` + `003261D0` (the latter itself a named `PartyConfiguration_*` body). The roadmap's
"roster array `02EBF190`+`0x5A48`, 9 × u16 member-id" is confirmed with one correction: `02EBF190`
is the *pointer* global, not the block — the bodies read `[02EBF190]` then index `+0x5A48` on the
result.

### And the hole is the same one that has bitten this project seven times

**The census records only `read` and `write` kinds — there are no `addr` rows in the entire file
(15,285 reads, 8,815 writes, zero `lea`).**

> **A `lea` into a map followed by a store through the resulting pointer would not appear.** The
> negative is *"no displacement-addressed write"*, **not "no write"** — and *an operand that is
> computed rather than encoded* is precisely the family that has produced seven instrument failures in
> this database already.

**Stated at the strength the instrument supports and no higher.**

**CLOSED 2026-09-03, three ways — and the hole was larger than the one identified here.**

| instrument | question asked | result |
|---|---|---|
| displacement census | what writes offset N? | maps 1–4: **initialiser only** |
| base-keyed scan **including `lea`** | does a pointer into a range escape? | **0** |
| register-held-offset scan | is a base loaded as an **immediate** and indexed? | **~~8 reads, 0 writes~~** 9 reads, 6 of map 1 and 3 of map 3, and no write through a map 1–4 base; the writes it could not see go through the map-0 base `003266D4 add rdi, 0x5a48` *(corrected 2026-10-02, OPUS: immediate scan of `0x5A5A`, `0x5A6C`, `0x5A7E` and `0x5A90`; the 2026-09-14 correction above)* |

**The second gap was not `lea` at all.** The five bases are also used **as bare immediates** —
`mov esi, 0x5A5A` then `movzx eax, byte [rsi + ptr]` — **a form neither a displacement census nor a
`lea` scan can see.** ~~Seven~~ Six *(corrected 2026-10-02, OPUS: `0031AC11`, `0031B5CD`, `00326573`, `00326B2F`, `00326BEE`, `00328E0D`)* such sites exist for map 1 alone, in `Party`, `Movement` and `ActorEntity`
code, **and every one was read before being counted: all reads.**

> **Three instruments, three different questions, one answer.** **A negative is only as strong as the
> variety of questions that failed to overturn it**, and this is the first in the run to survive three.

**~~So the claim is not "no displacement-addressed write" but "no write, by any of three encodings"~~** *(corrected 2026-10-02, OPUS: there is a write — `003266C0` holds `block + 0x5A48` in `rdi` (`003266D4 add rdi, 0x5a48`) and stores into maps 1–4 at `00326717`–`0032674B` and in its mode arms; none of the three instruments keyed on a map-0 base held in a register)* —
and *"four views allowed to drift"* is withdrawn on both sides, **because it asserted a freedom nothing
supports.**

**~~Map 0's only two writes are `0xFFFF` fill loops in two initialisers~~** Map 0 is written by the reset's `0xFFFF` loop (`00237107`), the initialiser `00329CC0` and `00329080` (`00329122`, `00329176`) *(corrected 2026-10-02, OPUS: displacement scan of `+0x5A48`–`+0x5A59` and the immediate `0x5A48`; this page's own map-0 row names `00329080`)*, read to confirm rather than
counted.

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Are the five bases really parallel tables, or one table read five ways? | **Five distinct base constants, `0x12` apart, in five arms of one `if` chain**, each indexed identically by `id*2`. |
| Is `0x12` nine entries or eighteen? | The initialiser writes **nine** entries stepping by 2 (`iVar7 <= 8`), and the copy moves **16 + 2 = 18 bytes**. **Both agree on nine `u16`.** |
| Could the copies be to unrelated neighbours? | The copy destinations are **exactly the resolver's other four bases**, in order. |
| Does the resolver read a `u16` or a byte? | **A byte**, at an index scaled by 2 — so it reads the low half of each `u16` slot. **Stated as read; why is not established.** |
| Does the write census prove the copies never diverge? | **No.** It proves **no displacement-addressed write** touches maps 1–4. The census has **no `addr`/`lea` rows at all**, so a pointer taken into a map and stored through would be invisible to it. |
| Was the earlier "reserve" reading wrong, or is this a second structure? | **Same base pointer, same offsets**, and the initialiser writes `+0x5A48` and copies to `+0x5A7E`. **One structure; the earlier reading took two of five maps for two halves of one.** *(2026-09-14: one structure of five tables in one format, but map 0 is the source and maps 1–4 are rebuilt from it; see the correction above.)* |

**What this document does not claim:** what the five classes are, what a slot value means, what
`01EED260` holds, or what `00316DF0` and `00323540` do to a registered entry.

## Why this document exists

**The pair frontier's first candidate.** Five functions touched `+0x5A7E`; four had documents; **no
document cited two of them.** Reading two of the five was enough to correct a published reading —
which is the outcome that ranking was built to produce.

> **Nothing was wrong with the earlier reading of one site. It was a correct reading of one of five
> identical maps, in a corpus where nothing pointed at the other four.**

## What the five maps are *inside*, and where that block actually lives (2026-09-10)

This document, and four others, read fields out of `*(0x02EBF190)` without any of them recording
what that block **is**. It had no row in `_types/` at all, while being the most referenced structure
yet measured: **318 references across 176 functions**. It is now `BattleSystemState`.

### It is not a heap allocation. It is part of the save image.

Both writers of the `02EBF190` slot are three instructions and they agree:

```asm
00233C25  call  002EF640              ; SaveImage_GetActiveBuffer
00233C2A  add   rax, 0x4e68c
00233C33  mov   qword ptr [rip + …], rax     ; -> 02EBF190
```

and `002EF640` is **three bytes**: `lea rax, [0x02164280]; ret`. So the battle system runtime state
is at a **fixed offset inside a static buffer**, not allocated and never freed — which is why no
allocation site was ever found for it.

**The buffer is `0x56690` bytes**, from the `memset` at `002EF663`, and four regions inside it are
named by the constant their accessor adds:

| offset | accessor | what is already known about it |
|---:|---|---|
| `+0x00200` | `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) | contains `PersistentFlagPayload`, `0x1538` |
| `+0x02200` | `WorldTransitionSnapshot_CaptureRuntimeState` (`00229B40`) | — |
| `+0x08200` | `FUN_00253970` | — |
| `+0x4E68C` | `00233C10` / `00238A80` | **`BattleSystemState`** |

**~~Size: bounded, not measured.~~** **Size: `0x7410`, measured** *(corrected 2026-10-02, OPUS: the reset `002370C0` clears `mov r8d, 0x7410` bytes at `002370CD`, and the last field is the selection array `+0x7370`–`+0x740F` — the battle-state block field map §2.1)*. `0x4E68C + 0x8004 = 0x56690`, the buffer's end, so `0x8004` is the
**maximum extent**. ~~The highest field anyone has read is `+0x5B04`, giving a floor of `0x5B08`.~~ The
type row carries the maximum and says so; the 9,468-byte tail is reported as a gap rather than
claimed.

**And it explains something this page could not.** `SaveTransitionMetadata_CaptureToRecord`
(`002EF3C0`) and `RestoreFromRecord` (`002EF410`) read and write `+0x5AD0` and `+0x5B04` of this
block. A structure that is captured into and restored from the save transition record *because it
already sits inside the save image* is coherent; a heap block would have needed an explanation.

### The five maps, re-derived rather than transcribed

Every base in §1 was re-checked against the image by an immediate scan over all 34,270 function
bodies, positive control `0x1C8` returning 366 occurrences:

| base | occurrences | resolver arm |
|---|---:|---|
| `+0x5A48` | 31 | ~~`0031B9F0`~~ `0031BAAA` *(corrected 2026-10-02, OPUS: the class-0 arm's load `movzx eax, byte ptr [rax + rdi*2 + 0x5a48]`; `0031B9F0` is the entry)* |
| `+0x5A5A` | 16 | `0031BA8B` |
| `+0x5A6C` | 2 | `0031BA71` |
| `+0x5A7E` | 8 | `0031BA57` |
| `+0x5A90` | 8 | `0031BA3D` |

One thing the type row records that the prose did not: **every reader takes the low byte of a
2-byte stride entry** — `movzx eax, byte ptr [base + idx*2 + N]` at all five arms — so the upper
byte of each of the nine entries is, so far, never read.

### A link to `BattleUnit`, and a claim it puts in question

`+0x0008` begins an array of **40 blocks of `0x1C8` bytes**. Its accessor `0031B770` bounds the
index at `0x27`, computes `state + 8 + index*0x1C8`, and then scans **every `BattleUnit` slot** for
one whose `+0x698` **equals that address**:

```asm
0031B789  imul  rcx, rax, 0x1c8
0031B7B1  cmp   qword ptr [rax + 0x698], rdi
```

So `BattleUnit.spawnRecordKindPage` at `+0x698` is, at least on this path, **a pointer to an element
of this array** — not to a spawn record. The handover that produced that row described it as *"the
spawn record `+0x80`"*, and `00234251`–`0023425D` does test `byte [unit->[0x698] + 5] == 1` for an
authored kind byte, so both readings have real evidence behind them. **Recorded as a contradiction
(`OPUS-CONTRA-BU698`), not resolved**, and the type row for `+0x698` now names both.

### Limits

- **`0x8004` is an upper bound**~~, and the 9,468 bytes above `+0x5B08` are undeclared, as are 3,520~~
  ~~between the `0x1C8` array and the slot maps.~~ *(corrected 2026-10-02, OPUS: the block is `0x7410` bytes, `002370CD`, and the battle-state block field map places every byte above the records, FO-5)*.
- The `0x1C8` element's own layout is **not** recovered; only its stride, count and one consumer.
- `+0x5AD0` is declared as sixteen bytes because that is what the `movups` pair moves. Only two bits
  of its first word have known consumers; calling the rest flags would be a guess.
- The other three save-image regions are named by their accessors only. Their extents in the table
  above are **the distance to the next region**, which is an upper bound on each, not a measurement.
- This is what the block *is* and where it lives. ~~**What the five classes mean is still not~~
  ~~established** — §"What the classes are is not established here" stands unchanged.~~ *(answered: see active-party-reserve-and-the-moment-the-leader-changes.md §2b; 2026-10-02, OPUS)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **Items_Equipment_Shops_License — SERVICE.**
  - The guard `00233C10` and the save rebind `SaveRuntime_RebindImageBackedGameplayState` (`00238A80`) both rebase
    inventory class descriptors (`InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState`).
  - `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects` (`00316DF0`) grants items and increments equipment
    counts (`Inventory_GrantEncodedLootItem`, `EquipmentInventory_IncrementSecondaryCountChannel`).
  - `DefinitionRuntime_DeactivateAndRemoveConfiguredItems` (`00323540`) decrements equipment counts and calls the same
    grant.

  **Activating a definition changes inventory.**
- **Rewards_Progression_Economy — SERVICE.** `00316DF0` also adds gil (`GameState_AddGilClampedAndNotify`) and calls the
  432-byte level-rank function and a 488-byte rewards body.
- **Audio — CLIENT, not read.** The 335-byte Audio-filed body reads `SaveImage_GetPersistentPayloadBase` (`002EF2B0`).
- **CoreRuntimeScheduling — SERVICE and MECHANICAL.** `00233C10` reads a 7-byte core getter. `00316DF0`'s resolver
  reads are MECHANICAL.
- **ActorEntity - CLIENT (25 edges).** `002EF2B0`, `00316DF0` are also called by bodies filed to ActorEntity: `0025D9E0`, `002628B0`, `0026C8C0` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (4 edges).** `0031B770`, `00322C50` are also called by bodies filed to movement: `00326D60`, `0031BAC0`, `00326BB0`; `003266C0` reaches bodies filed to movement: `00311E20` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (1 edge).** `003172E0` is also called by bodies filed to script VM / native bridge: `0034C370` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - SERVICE (1 edge).** `00229B40` reaches bodies filed to spawn/encounter lifecycle: `00233440` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (34 edges).** `00229B40`, `002EF2B0` are also called by bodies filed to WorldAreaField (world area): `003145E0`, `0025ACA0`, `00268320`; `00229B40` reaches bodies filed to WorldAreaField (world area): `0025D8E0` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** `BattleUnit_RunPeriodicCombatMaintenance` calls a function this page cites.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Citation spellings (R5), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Input — SERVICE.** The save-buffer binder this page cites calls two small Input-filed helpers (24 and 26 bytes).
- **Resource — SERVICE.** The save-buffer binder calls two small Resource helpers (20 and 65 bytes).
- **UI — SERVICE.** The save-buffer binder calls a 68-byte UI helper.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `0031B770` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_GetByMappedBattleSlot`, owned by that layer, calls `0031B9F0` on this page. That caller is a 49-byte accessor over the battle stats table: the mapped slot byte is rejected above `0x27`, and the rest index `[02EBF190] + 8` at a stride of `0x1C8` - the same **40 records of `0x1C8` bytes** the battle runtime reset walks; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Story_Event_Quest_Hunt — CLIENT (12 edges, one fan-in).** All 12 edges are Story_Event_Quest_Hunt bodies reaching `002EF2B0` on this page. `PersistentFlag_QueryPrimaryOrAuthoredTable` is the worked example - it is the flag query whose id is masked to `0x3FFF` while **bit 14 selects between the primary and the authored table**. The crossing is **one shared subject with 12 callers on that layer**, not 12 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).


### Interior citation — frontier hubs `0030F9A0`, `0030C410` (2026-09-18, SWE2-EC7)

The inventory second-quantity pair, called from the slot-map walkers
`00316DF0`/`00318B40`/`0031A510`/`0031A630`/`00323540`:

- `0030F9A0` — 85 B, `EquipmentInventory_DecrementSecond…`: `cx == 0xFFFF`
  returns `-1`; `(cx & 0xF000) != 0x1000` or `cx == 0x1000` returns 0; otherwise
  calls `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (`003008A0`) with
  `edx = -1`, `r9d = 2`, stack arg 0
  ([`0030F9EB`](../_index/ADDRESS-INDEX.md)).
- `0030C410` — 86 B, `EquipmentInventory_IncrementSecond…`: identical guards,
  same call with `edx = +1` ([`0030C45C`](../_index/ADDRESS-INDEX.md)).

The `0x1000`-class encoded-id gate means the pair only accepts the second-slot
quantity encoding.
## SWE2-EC7-41 update (2026-09-19) - `003287A0`

`003287A0` (331 B) is a slot-map body - `022C2580`/`022C2590`/`02EBF190`, `00322C50`/`003261D0`. Interior anchor `00328859` (a `00322C50` call).

## SWE2-EC7-50 update (2026-09-19) - `003286E0`

`003286E0` (182 B) is a body - `00321100`/`003261D0`. Interior anchor `00328726` (a `00321100` call).

## SWE2-EC7-59 update (2026-09-19) - `003288F0`

`003288F0` (159 B) is a slot-map body - `00323540`/`003261D0` plus `022C2580`/`022C2590`/`02EBF190`. Interior anchor `0032897C` (a `00323540` call).


## SWE2-EC7-95 update (2026-09-20) - `00321100` measured

`00321100` (101 B) is the slot probe `003172E0` and `003286E0`
run: `ebx` 4..8 calls `00322C50(0x17, ebx, 0)`, and the first
index whose `byte[base + rbx*2 + 0x5A86]` is not `0xFF` returns
in `eax`; a clean run returns -1.
Interior anchor `00321139` (the `0xFF` compare).
