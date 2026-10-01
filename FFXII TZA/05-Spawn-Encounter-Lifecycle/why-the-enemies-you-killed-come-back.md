---
system: Why the enemies you killed come back
category: 05-Spawn-Encounter-Lifecycle
status: AUDITED
owner_layer: PrimaryOwner:Spawn_Encounter_Lifecycle
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 11 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-13
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: true
  reopened_count: 0
---

# Why the enemies you killed come back

`SpawnKeep_RotatePersistenceBanksForArea` at **`00233780`**, 672 bytes. Three documents cited it as a
name.

## What the player sees

**The game remembers what you killed in exactly two areas: the one you are in, and the one before it.**

Two banks of **37,888 bytes** each — **64 keep entries of `0x250`**, copied in `0x128` chunks of `0x80`
bytes (corrected 2026-09-13, see the note below). On every area change:

- **If the area you are entering is the one you were in two moves ago** — you left it, went somewhere
  else, and came straight back — **the two banks are rotated through a stack temporary and your kills
  are still there.**
- **Otherwise the outgoing area's bank is pushed to the "previous" slot and the incoming bank is wiped
  with `memset(bank, 0, 0x9400)`** — and everything respawns.

> **Go one area away and come back: the enemies stay dead. Go two areas away: they return.** That is
> not a heuristic — it is a two-slot buffer, and the second slot is the entire memory.

## And there is a timer on top of it

```asm
002337D6  cmp   esi, ecx                        ; entering the area from two moves ago?
002337DE  movss xmm0, dword ptr [0x01DFE0B8]    ; the frame-rate base: 1 at 30 fps, 2 at 60
002337E8  mulss xmm0, dword ptr [0x008F8D80]    ; x 30.0  -> ticks per second
002337F0  sub   ecx, dword ptr [0x02089374]     ; elapsed since the last transition
002337FA  imul  edx, dword ptr [0x0208936C]     ; x an authored count
00233801  cmp   ecx, edx
00233803  ja    <wipe>                          ; too long ago -> wipe anyway (unsigned, low 32 bits)
```

**`01DFE0B8 × 30.0` is ticks per second** — 30 at 30 fps, 60 at 60 fps — established independently in
the frame-limit work, **so `0208936C` is a number of seconds.** The window is authored, and the
conversion is why it holds at either frame rate.

> **Coming back is not enough; you have to come back soon.** Both conditions must hold, and **either
> failure takes the same wipe path.**

## The wipe path does three more things

1. **The outgoing bank is copied to "previous" with a different instruction schedule** — the same 128-byte
   chunks, but the last 32 bytes moved as four dwords rather than two qwords. **Two copies of
   one structure, compiled differently; a reader comparing them would see two layouts and there is
   one.**
2. **A parity bit at `0208D454` is flipped** — on *both* paths, so it tracks transitions, not wipes.
3. **A 64-entry `u16` array at `0208D354 + parity × 0x80` is filled with `1`** (`rep stosw`, count `0x40`,
   `002339BC`–`002339E2`) — the same count as the bank's entries, a correspondence this page has not
   traced — reset only on the wiping path.

**Then, unconditionally**, the field history shifts: `[two moves ago] = [last]`, `[last] = current`,
and the timestamp is stamped. **The history is two entries deep, which is why the memory is.**

## What a load does to the two banks and the window — 2026-09-13

*FABLE, static; answers the bank-and-timer part of `L-13` for ASTRA's review.* **None of the window's state is part of
the save image**, so a load changes it only where code copies it:

| state | storage | on a load that passes the stamp guard | on the guard's null / mismatch path |
|---|---|---|---|
| bank 1, current area (`btlKeepCharWork1`) | heap, `[0208E690]` (`BattleStorage_InitializeWorkArrays` `0023695E`) | **not restored** — keeps the session's contents | not touched by `00237DF0` either |
| bank 2, previous area (`btlKeepCharWork2`) | heap, `[0208E698]` (`00236989`) | restored from the image **only when slot 0, the autosave, is loaded** (`SpawnKeep_RestorePersistenceBank` from `005843E0`); otherwise kept | not touched |
| field history `02089370` (last) / `02089372` (two ago) | globals | restored with bank 2 on a slot-0 load (`002335BC`, `002335C7`); otherwise kept | both `−1` (`00237E5D`, `00237E64`) |
| transition stamp `02089374` | global | **never restored** | `0` (`00237E53`) |
| raw tick counter `0208D45C` | global, advanced by `0032A100` | **never restored** | `0` (`0032A160` from `00237E37`) |
| parity `0208D454` | global | never restored | `0` (`00237E6B`) |

The guard is `00233C10`; `BattleSystem_ResetRuntimeState` `00237DF0` runs only on its null path (first bind, e.g. at boot)
or when the battle-state block's stamp mismatches. **The decision is then made by the next area initialisation**:
`BattleSystem_InitializeAreaState` (called from `ActorSystem_InitializeManagerRuntime` `0026CEC6` and `00266D10` `00267136`;
that the load's requeue reaches it is expected, not traced here) holds the only rotation call, `00234423`, and `SpawnKeep_RotatePersistenceBanksForAreaTransition` compares the entered field (`003148F0`: payload `+0x1044`, which the load did bring from the file) with
`02089372` and `GameClock_GetRawTickCounter() − 02089374` (unsigned) with the authored window. So after a load:

- **autosave (slot 0):** bank 2 and the history are the transition's; entering the field recorded two moves back
  within the window — measured on the **session's** clock against the **session's** stamp — swaps the restored bank 2 in
  as the current bank, and anything else pushes the session's bank 1 into bank 2 and wipes bank 1;
- **manual slot:** the rotation runs on the session's banks, history, stamp and clock, none of which came from the file;
- the window's elapsed time therefore spans play from before the load (it is not measured from the save's time), and a
  stamp later than the clock wraps the unsigned difference to a large value, which takes the wipe.

**Not established:** what the session values are in practice (a load from the title after a fresh boot has them from
the boot's reset and whatever the title ran), whether some other path rewrites the pair or stamp between the load and
the area initialisation, and the player-visible result — those are live questions.

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the comparison against the *last* area or the one before it? | Against `02089372`, and the tail assigns `02089372 = 02089370` **after** the test — so at test time it holds the field from **two** transitions ago. |
| Is `0x9400` the bank size or a coincidence? | `0x128 × 0x80 = 0x9400`, and the copy loops run **`0x128` iterations of 128 bytes**. **The memset and the loops agree.** *(2026-09-13: the size stands; the 128-byte stride is the copy's chunk, not the record — see the correction below.)* |
| Is the rotate really a swap? | **Three copies through a stack temporary** — previous→temp, current→previous, temp→current — which is a swap written the only way it can be for a 37 KB object. |
| Could the timer be frames rather than seconds? | The multiplier is the **frame-rate base**, which is 1 at 30 fps and 2 at 60; times `30.0` it is **ticks per second at either rate.** A frame count would not need that factor. |
| Does the parity flip only on wipes? | **No — both paths flip it**, three instructions apart in different branches. It counts transitions. |

## Correction — 2026-09-13 (ASTRA's independent falsification, consumed by FABLE)

**The bank is 64 entries of `0x250` bytes, not `0x128` records of `0x80`.** The arithmetic above was
right and its reading was wrong: every bank loop (`00233780`'s rotate and wipe branches, the serializer
`00233440`, the restore `00233550`) is a structure-blind `movups` copy that moves the bank in 128-byte
chunks (`mov edi, 0x128` at `00233815` and `00233946`, `mov r8d, 0x128` at `00233560`), and
`64 × 0x250 = 0x128 × 0x80 = 0x9400`. The entry layout is
[the spawn-keep entry field map](Spawn-Record/the-spawn-keep-entry-field-map.md); the allocation and
the `btlKeepCharWork1`/`2` tags are in
[spawn placement and retirement](spawn-placement-and-retirement.md), whose §11 is the falsification consumed here.

**Two qualifications of the rotation story from the same pass:**

- **The window compare is unsigned.** The elapsed tick difference and the multiplied threshold are
  low-32-bit values and `00233803` is `JA`, so the comparison is unsigned 32-bit arithmetic, not a signed
  duration test.
- **The restore helper is not the serializer's inverse.** `SpawnKeep_SerializePersistenceBanks`
  (`00233440`) copies **both** banks into the save buffer; `SpawnKeep_RestorePersistenceBank`
  (`00233550`, 127 B, called twice from `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot`
  `005843E0`) copies **only** buffer `+0x10` into bank 2 (`[0208E698]`) and then the field-id pair
  `02089372` / `02089370`. It does not touch bank 1, the tick stamp `02089374` or the window. So the
  two-slot memory described above is the in-play area change; what a load restores into bank 1 and the
  timer is the open question `L-13` on the retirement page, and nothing here closes it. *Narrowed 2026-09-13
  (FABLE):* `005843E0` runs only when the loaded slot is **0, the field-transition autosave** — the one save that
  captured the pair — so loading the autosave restores bank 2 and the field-id pair from the transition, while
  loading a manual slot restores neither ([request router §2](../16-UI/Request-Router/ui-request-router.md)).

  > ***Observed, and the static half is confirmed — 2026-09-21 (FABLE, consuming ASTRA's `old-save-start-p` run
  > for `L-13`).*** A modern field session returned to the title and loaded an **older manual-slot save** in one
  > process, eight accepted samples over four stages, banks read as raw spans at `[0208E690]` and `[0208E698]`:
  >
  > | transition | battle bytes changed | bank 1 changed | bank 2 changed |
  > |---|---:|---:|---:|
  > | modern field → returned title | 220 | 328 | 346 |
  > | returned title → old load complete | 1,572 | **0** | **0** |
  > | old load complete → settled old field | 0 | 0 | 346 |
  >
  > **The load that replaced 1,572 bytes of the battle block changed neither bank by a single byte** — so
  > *loading a manual slot restores neither* is not only the static reading of `005843E0`'s slot-0 guard, it is
  > what the banks actually do across such a load. **The title return is what moves them**: bank 1 goes from 328
  > nonzero bytes to zero and bank 2 from zero to 346 — *and the run's own comparator records that the modern
  > bank 1 is **not** byte-identical to the returned-title bank 2*, so this is a clear-and-refill, not a copy or
  > a content rotation. Entering the old field then zeroes bank 2 while the battle block does not change at all.
  >
  > **Two things in that data are traps and are called out rather than used.** The last transition's
  > `old_keep1_equals_new_keep2` reads *true*, and it is **degenerate**: both sides are the all-zero block, the
  > same digest bank 1 carries at every stage after the title, so it is not evidence of a copy. And the two
  > modern-field samples agree on bank 1's **count** of 328 nonzero bytes while their digests differ — the bank
  > is live during field play, so a nonzero count is not a fingerprint of its contents.
  >
  > **What this does not establish.** No writer instruction, no slot-0 autosave comparison (that path was not
  > exercised), nothing about the tick stamp `02089374` or the window, and no enemy death, respawn consequence
  > or callback ordering — the run states that it did not test them. `L-13` keeps bank 1 and the timer.

Other restoration paths into the banks are not excluded by this page.

**What this document does not claim:** what a keep entry holds beyond the field map linked above, what the 64 `u16` entries mean
beyond being reset to `1`, what `0032A150` returns as a clock, or **why the window exists** — a
two-slot buffer needs no timer to be correct, so the timer is a policy and its reason is not in this
function.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

This page cites three of the most widely shared services in the image, so most of its crossings are **CLIENTS** of
them. None of those clients bears on why enemies return.

- **The field id, `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`).** Its clients include:
  - **Movement:** a 4,006-byte body and two `003EDxxx` helpers;
  - **Presentation:** two bodies of about 4.8 KB;
  - **CombatAction:** the trigger-point test and its 477-byte sibling;
  - **Script_VM_Native_Bridge:** two verb bodies;
  - **Audio:** the 335-byte body that also reads the persistent payload base;
  - **PlatformOnlineAchievements:** the 212-byte achievement-side caller.

  See [choosing the field environment variant](../03-World-Area-Field/choosing-the-field-environment-variant.md),
  crossings.
- **The raw tick counter, `GameClock_GetRawTickCounter` (`0032A150`).** Its clients include:
  - **CombatFormula:** the HP write `BattleStats_ModifyHPAndProcessLethal…`;
  - **Party:** `BattleUnit_SeedPartyCombatStanceRecheckTimer`;
  - **Presentation:** `BattleUnit_ComputePartyBattleStance` and `PartyCombat_UpdateStanceState`.

  The persistence-bank rotation `00233780` uses the same counter.
- **The area initialiser `00266D10`.** Boot calls it (a **CoreRuntimeScheduling** edge). It then calls into:
  - **Audio:** a 516-byte body that reaches the sound entries;
  - **Input:** the unread 1,936-byte body;
  - **Movement:** three helpers of 9–230 bytes;
  - **Presentation:** `CameraSystem_InitializeRecords` and a 271-byte body;
  - **Script_VM_Native_Bridge:** `VMNativeCommandDispatch_InitializeFa…`.

**The guard `00233C10` — SERVICE.** The table above calls it the guard, and says
`BattleSystem_ResetRuntimeState` (`00237DF0`) runs only on its null path, at first bind. Its other callees are:

- **CombatAI:** `GambitRuntime_RebuildAllOrderSets`;
- **Items_Equipment_Shops_License:** `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState`;
- **Gameplay:** `00237DF0`.

`00237DF0` in turn initialises inventory from the authored table (`Inventory_InitializePrimaryStateFromAuthoredTable`)
and the definition records (**CombatFormula** `BattleStats_InitializeDefinitionRecord`). Both functions also read small
7–11-byte **CoreRuntimeScheduling** getters. **Which of the guard's callees run on every call, and which only on the null path, is
not read here.** The page's claim about bank 1 is unaffected, because `00237DF0` does not touch it.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** A cited function is called by `BattleUnit_RecoverFromTerminalStatusSetIfClear`, `BattleUnit_RunPeriodicCombatMaintenance` and `BattleFormula_ApplyGlobalPeriodicDrainModes`.
- **UI — CLIENT and SERVICE, not read.** Two cited functions are called by four UI bodies (170 to 1,827 bytes), and one calls a 134-byte UI body. Which screen reads respawn state is not read here.
- **SaveLoad - CLIENT (2 edges).** `00233C10`, `002EF640` are also called by bodies filed to SaveLoad (save/load settings): `00280140` (RuntimeLifecycleSupport) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (29 edges).** `00237DF0` is also called by bodies filed to save/load/settings: `00238A80`; `00233C10`, `00235AF0`, `00266D10` reach bodies filed to save/load/settings: `002EF640`, `002EF2D0` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `00266D10` on this page calls `FUN_003b6ed0`, owned by that layer. What it reaches is a 93-byte reset that sizes its own table: `dword[02B40534]` becomes 1, and **`0x20` dwords from `02EBCBE0`** are zeroed along with five named singles at `02EBCC70`, `02EBCC60`, `02EBCBC0` and `02EBCAA0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## The `00233C10` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

The battle-state guard `00233C10` (214 B) is a transition-metadata capture
battery on the `[02EBF190]` block: `00235AF0` opens (`00233C14`), `002EF640`
snapshots the block (`00233C25`) and stores back `02EBF190` (`00233C33`),
`0030B6A0` (`00233C3A`), then the `00237DF0` reset branches
(`00233C48`/`00233C59` — the null-path first-bind). After the prelude the
battery runs `00327F80`, `003139A0`, `00304770` (`00233CAD`–`00233CBB`),
`002FA230`, `002FA260`, `0016D6A0`, `003266C0`, `00311E10`, `00226BD0` ×2
(`00233D35`/`00233D59`), `0031B760` (`00233D74`), `00313F60`, `00320A00`
(`00233DC4`).

| member | role | interior |
| --- | --- | --- |
| `00327F80` (437 B) | `0xFFFF`-masked copy/fill on the transition block — reads `[02EBF0D8]` (`00327F94`), `lea 02089378`, `r9d = 0xFFFF` (`00327FA4`), byte-source `[rax + rdx + 0xC]` from `[02EBF190]` (`00327FB7`) | [`00327FB7`](../_index/ADDRESS-INDEX.md) |
| `003139A0` (29 B) | bit setter — `word[[02EBF190] + 0x5AD0]` bit 1 ← `cx & 1` via the `cx = 2*cx; cx ^= word; cx &= 2; word ^= cx` XOR-replace (`003139A7`–`003139B5`) | [`003139AA`](../_index/ADDRESS-INDEX.md) |
| `00304770` (23 B) | bit setter — `dword[[02EBF190] + 0x5AE0]` bit 0 ← `ecx & 1` via the same XOR-replace idiom (`00304777`–`00304780`) | [`00304777`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00235AF0`, `002EF640`, `0030B6A0`,
`00237DF0`, `002FA230`, `002FA260`, `0016D6A0`, `003266C0`, `00311E10`,
`00226BD0`, `0031B760`, `00313F60`, `00320A00`. The `[02EBF190]` block is
the same transition-metadata record `002EF410` restores from (ladder page
subtree) — `00233C10` is the capture/guard side.
