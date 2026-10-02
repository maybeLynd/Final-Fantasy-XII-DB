---
system: The License check — what the board actually tests
category: 12-Items-Equipment-Shops-License
status: AUDITED
owner_layer: PrimaryOwner:Items_Equipment_Shops_License
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-03
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-license-check-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The License check — what the board actually tests

> When the menu greys out an ability with reason code `0x10`, it has asked one question:
> **does this character own any board square that grants this action?** Not the right square —
> **any** square. The board is a bitmask, one bit per node, and the test is an overlap.

## 1. What the player sees

An ability in the menu you cannot pick, because you have not bought its License. In FFXII an
ability can appear on the board in **more than one place** — and a player who buys any one of those
squares gets the ability. That is not a UI convenience; it is what the check does.

The same check is what makes **Quickenings** behave differently from everything else (§5), and what
makes abilities unrestricted for units that are not licensed party members at all (§3).

**Equipment is asked the identical question** — a sword you cannot equip fails the same test with one
argument changed (§5b), which is why one board governs both halves of the game.

## 2. Where this sits

[`battle-command-availability-and-reason-codes.md`](../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md)
established that reason **`0x10` = "no License"** is the *last* gate an action passes, and named
`BattleStats_HasRequiredLicenseForAction` (`00323EC0`) as the thing that answers it. **That document
located the check; this one reads it.**

## 3. The three ways an action is licensed without a board at all

`BattleStats_HasRequiredLicenseForAction(unit, actionId)` returns **non-zero for licensed**. Before
any board data is touched:

```c
if (BattleEncodedId_IsValidForClass(0x14, actionId) == 0)  return 0;   // see §9: the ACTION ID is
                                                             // passed too - this is a bounds check
if (unit == NULL)          return 1;
if (unit[5] != 0)          return 1;                          // record kind byte
if (unit[4] > 6)           return 1;                          // party slot index   <- corrected 2026-10-02, OPUS: the party-table type id (0-5 the party, 6 Reks, 7-16 the other guests), 00323EFF
```

`unit[5]` is the **battle-record kind byte** documented in
[`battle-record-kind-byte.md`](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md),
and `unit[4]` is the party slot. So **the License system applies only to record kind 0 with a slot
index of 6 or less.** Everything else — and every unit whose slot index is out of range — is
**licensed for everything**, returned before a single node is read.

> **The board is not a property of the ability. It is a property of being a licensed party member.**
> ~~Guests and non-party units do not fail this check; they never reach it.~~ The test is on the type id at `+4`, not a party slot: type ids 0–6 reach the board — the six party members and row 6, the guest Reks — while guests 7–16 and non-party units never do *(corrected 2026-10-02, OPUS: checked at `00323EFF` `cmp byte [rsi+4], 6` / `ja` → licensed; CONTRACT-license-check.md §10, "slot 6 included")*.

There is then a per-action escape hatch:

```c
row  = table(02EBF138)[actionId];
if (row->flags16_at_0x2C & 0x2000)  return 1;   // this action needs no License
```

**Bit `0x2000` at `+0x2C` of the action row means "no License required"** — the mechanism behind
abilities every character can use unbought. The test is **16-bit** (`00323F4D mov eax, 0x2000` /
`00323F52 test word ptr [rcx + 0x2c], ax`), so the bit is **bit 5 of the byte at `+0x2D`**, and
**98 of the 543 shipped rows set it** (§9).

## 4. The general test: a 368-bit mask overlap

For every action outside the Quickening range, the check tail-calls
`BattleStats_HasLicensePrerequisiteForRequirement` (`00323BB0`), which is short enough to give whole:

```c
uint8 req[0x2E] = {0};                                   // 46 bytes, zeroed
LicenseData_BuildPrerequisiteNodeMaskForRequirement(kind /*1*/, (uint16)actionId, req);
for (i = 0; i < 0x2E; i++)
    if (unit[0x194 + i] & req[i])  return 1;             // ANY overlapping bit   <- corrected 2026-10-02, OPUS: the stats record, not the unit (00323ECD mov rsi, rcx; one argument, no +0x698 hop)
return 0;
```

**The unit's owned-License bitmask is 46 bytes at `statsRecord + 0x194` — 368 bits, one per board node** (the `BattleStatsRecord` behind unit `+0x698`: `00323EC0` tests the record's kind byte `+5` and job `+4` on the same base — corrected 2026-09-11 from "unit", whose own `+0x194` is a movement snapshot).
The action's requirement is a mask of the same shape, and the test is a byte-wise AND that
**returns on the first non-zero byte**.

> **Any single overlapping bit licenses the action.** This is an OR across nodes, not an AND — so an
> ability that appears in four board squares is unlocked by whichever square you bought, and there is
> no notion of a "required" square. ~~It also means the loop's early exit is semantically load-bearing,
> not an optimisation.~~ *Withdrawn 2026-09-29 (OPUS, the contract's falsification pass 1, `CON-160`): after the loop
> `00323BB0` writes, calls and computes nothing, and returns the constant 1 or 0. The early exit is an optimisation.*

## 5. Quickenings are the exception, and they are counted rather than matched

Action ids **`0xD0`–`0xE1`** (18 ids) never reach §4. They take a different test entirely:

```c
row = table(02EBF130)[ unit[4] ];              // indexed by PARTY SLOT, not by action
idx = FUN_0030A330(row, actionId);             // position of actionId within row's 3-entry list
n   = BattleStats_CountLicenseBits00To17(unit); // popcount of bits 0..17 of the same mask
return idx < n;
```

`0030A330` searches **three** bytes at `row + 4, +5, +6` for the action id and returns its index
`0, 1, 2` — or **3** when the row is null or the id is not among them.
`BattleStats_CountLicenseBits00To17` (`00324020`) is ~~an unrolled popcount~~ a loop of three passes over six bits *(corrected 2026-10-02, OPUS: `lea edi, [r9+3]` / `sub rdi, 1` / `jne 00324040`; CONTRACT-license-check.md §15)* over the **same
`statsRecord + 0x194` mask**, walking bit indices from 0 upward.

So each party slot has a row naming **three** action ids, and the *k*-th of them is available only
when the unit owns at least *k + 1* of License bits 0–17. **The gate is a count, not a match** —
which is exactly the shape of "you have unlocked two Quickenings, so you may use the first two."

**What is not established here:** ~~whether bits 0–17 are exclusively the Quickening squares,~~ *(answered for the shipped tables: CONTRACT-license-check.md §14 — bits 0–17 do nothing but feed this count; 2026-10-02, OPUS)* and what
happens when the count exceeds 3 (an id not in the character's three yields `idx = 3`, which passes
whenever the count is 4 or more). **The mechanism is read; the meaning of the bit range is not.**

## 5b. Equipment asks the same question with a different `kind`

`BattleStats_HasRequiredLicenseForEquipment` (`00323C60`) is the sibling entry point, and it is the
same shape end to end:

```c
if (BattleEncodedId_IsValidForClass(1, itemId) == 0)  return 0;   // class 1 = "derive it"; for a
                                                      // 0x1nnn id that resolves to class 6 (§9)
if (unit == NULL || unit[5] != 0 || unit[4] > 6)  return 1; // the same three passes as §3
row = table(02EBF0F8)[ itemId - 0x1000 ];                   // equipment rows, id base 0x1000
if (row[7] & 0x10)  return 1;                               // this item needs no License
return BattleStats_HasLicensePrerequisiteForRequirement(unit, /*kind=*/0, itemId);
```

**The two entry points differ in exactly three constants** — the class passed to the validity gate
(`1` vs `0x14`), the table and flag encoding the "needs no License" escape (`02EBF0F8` byte `+7` bit
`0x10`, against `02EBF138` word `+0x2C` bit `0x2000`), and **the requirement `kind`: equipment passes
`0`, actions pass `1`.**

> **REFINED 2026-09-03 — class `1` is not "the equipment class".** The validator dispatches on
> `class − 1` through a 32-entry jump table, and **class 1's arm derives the class from the id
> itself** (`FUN_00309440(id)`, then re-enters the switch). So the equipment path asks *"work out
> what this id is and validate it accordingly"*, while the action path names its class outright —
> **class `0x14` resolves to the action table `02EBF138`, which is the same table this section
> cites.** See
> [`the-encoded-id-class-registry.md`](../00-Engine-Core-Runtime/the-encoded-id-class-registry.md).

> **That `kind` is what makes one board serve both.** §6's node scan filters nodes by category, so the
> same 368-bit mask answers "may I cast this?" and "may I wear this?" without either question seeing
> the other's nodes. **One mask, two vocabularies, selected by a single argument.**

The `itemId - 0x1000` index agrees with the encoding in
[`item-id-encoding-and-equipment-compatibility.md`](item-id-encoding-and-equipment-compatibility.md),
where `0x1000` is the base of the equipment range.

## 6. Where a node's requirement comes from

`LicenseData_BuildPrerequisiteNodeMaskForRequirement` (`002F8FA0`) builds the requirement mask by
**scanning every board node**:

```c
n = nodeCount;                                  // dword at 02EBF038 + 4
memset(out, 0, (n + 7) / 8);                    // one bit per node
for (i = 0; i < n; i++) {
    row = base + stride * i;                    // stride = word at 02EBF038 + 8
    if (FUN_00323890(row[5]) == kind)           // node category byte at +5
        for (c = 0; c < 8; c++)                 // EIGHT uint16 ids at +8
            if (*(uint16*)(row + 8 + 2*c) == id) { out[i >> 3] |= 1 << (i & 7); break; }
}
```

**A board node carries a category byte at `+5` and a list of up to eight 16-bit ids at `+8`.** The
requirement mask therefore has a bit set for **every node that grants this (kind, id)** — and §4 then
asks whether the unit owns any of them.

*Qualified 2026-09-27 (FABLE, Claude Opus 5.5), on `ASTRA-RETURN-FABLE-LICENSE-CLEAR-BOUNDARY`
(`_experiments/evidence/license-builder-clear-boundary/`). The sketch hides an ordering and a width:*
- *The clear length is computed first and in 32 bits: `002F8FD3 lea r8d, [rax+7]`, then `shr r8, 3`, then the
  `memset` call at `002F8FE0`.*
- *The signed loop gate comes after it (`002F8FFC test r14d` / `jle`). So a non-positive count does not mean no clear
  was requested. In ASTRA's bounded run a malformed count of `0xFFFFFFF8` produced a request of 536,870,911 bytes,
  stopped before it ran.*
- *A count of 0 clears nothing. The 46-byte all-zero mask comes from the caller: §4's `00323BB0` stores five qwords, a
  dword and a word of zeros at `rsp+0x20`…`0x4D` (`00323BD4`–`00323BF5`) before it calls the builder (`00323BFC`).*
- *So "an empty mask" is a logical result. Its physical zeroing is the caller's guarantee, and a node count above 368
  is a precondition the builder does not check. None of this is shown to happen with shipped data.*

> **The mask is built by search, not by lookup.** There is no reverse index from ability to node; the
> engine walks all `nodeCount` nodes on every check. That is also why the same ability in several
> squares needs no special handling: it simply sets several bits.

The mask buffer is `0x2E` bytes and the sizing expression is `(nodeCount + 7) / 8`, so **the board
holds at most 368 nodes**; the live count is `[02EBF038 + 4]`, which is loaded at runtime and is not
resident in the image.

## 7. Key addresses

| Address | Name | Role |
|---|---|---|
| `00323EC0` | `BattleStats_HasRequiredLicenseForAction` | entry point for actions; §3 gates, §5 Quickenings |
| `00323C60` | `BattleStats_HasRequiredLicenseForEquipment` | entry point for equipment, `kind = 0` (§5b) |
| `00323BB0` | `BattleStats_HasLicensePrerequisiteForRequirement` | the 46-byte mask overlap (§4) |
| `002F8FA0` | `LicenseData_BuildPrerequisiteNodeMaskForRequirement` | builds the requirement mask (§6) |
| `00324020` | `BattleStats_CountLicenseBits00To17` | popcount of bits 0–17 (§5) |
| `0030A330` | — | 3-entry search on the party-slot row (§5) |
| `00323890` | — | node category byte → requirement kind (§6) |
| `00322C50` | `BattleEncodedId_IsValidForClass` | the class-20 gate (§3) |
| `02EBF038` | — | License **node** table descriptor: count `+4`, stride `+8`, handle `+0xC` |
| `02EBF130` | — | per-party-slot Quickening row table |
| `02EBF138` | — | per-action row table; `+0x2C` bit `0x2000` = no License required |
| `02EBF0F8` | — | per-equipment row table, indexed `itemId − 0x1000`; `+7` bit `0x10` = no License required |

The three table descriptors share one shape — `stride` as a word at `+8` and a handle at `+0xC`
resolved by `ImageAddress_ResolveRuntimePointer` (`0020E600`) — so all three are runtime-loaded
resources, not image data.

## 8. Data structures and formulas

```
unit + 0x004   party slot index      (licensed only when <= 6)   <- corrected 2026-10-02, OPUS: statsRecord + 0x004, the party-table type id (0-5 the party, 6 Reks, 7-16 the other guests); 00323EFF
unit + 0x005   record kind byte      (licensed only when 0)   <- corrected 2026-10-02, OPUS: statsRecord + 0x005 (00323EF3)
unit + 0x194   owned-License bitmask, 46 bytes / 368 bits, one bit per board node   <- corrected 2026-10-02, OPUS: statsRecord + 0x194, the check's one argument (00323ECD), as section 4 says

license node row (table 02EBF038, stride = word at +8)
    +0x05  category byte  -> requirement kind via 00323890
    +0x08  uint16 id[8]   -> the abilities this node grants

action row (table 02EBF138, indexed by action id)
    +0x2C  uint16 flags; bit 0x2000 = needs no License
equipment row (table 02EBF0F8, indexed by itemId - 0x1000)
    +0x07  uint8  flags; bit 0x10   = needs no License

licensed(unit, action) =
      kind != 0 or slot > 6            -> yes, unconditionally
    | action flags & 0x2000            -> yes
    | action in [0xD0, 0xE1]           -> quickenIndex(slot, action) < popcount(mask bits 0..17)
    | otherwise                        -> (mask & requirementMask(1, action)) != 0

licensedEquipment(unit, itemId) =
      kind != 0 or slot > 6            -> yes, unconditionally
    | equip row +7 & 0x10              -> yes
    | otherwise                        -> (mask & requirementMask(0, itemId)) != 0
```

**The only difference between the two is the `kind` argument** — `1` for actions, `0` for equipment.

## 9. Call chain

```
menu / AI asks
  -> BattleAction_CheckUnitActionAvailability (00306480)     reason 0x10 on failure
     -> BattleStats_HasRequiredLicenseForAction (00323EC0)
        -> BattleEncodedId_IsValidForClass (00322C50)         class-20 gate
        -> BattleStats_CountLicenseBits00To17 (00324020)      Quickenings only
        -> BattleStats_HasLicensePrerequisiteForRequirement (00323BB0)
           -> LicenseData_BuildPrerequisiteNodeMaskForRequirement (002F8FA0)
              -> scans all nodeCount rows of table 02EBF038
```

**The requirement mask is rebuilt on every check** — ~~`002F8FA0` zeroes a stack buffer~~ the caller zeroes a 46-byte stack buffer, `002F8FA0` clears its first `(n+7)/8` bytes again (§6, qualified 2026-09-27) and walks the
whole node table each time an action's availability is tested. There is no cache in this path.

## 10. Modding notes

**To grant an ability, set any one of its nodes' bits** in the 46-byte mask at ~~`unit + 0x194`~~ `statsRecord + 0x194` *(corrected 2026-10-02, OPUS: the check's one argument is the stats record, `00323ECD`; §4's correction of 2026-09-11)*. There
is no "correct" bit; §4 is an overlap test.

**To make an ability universally available**, set bit `0x2000` at `+0x2C` of its action row — this is
the engine's own mechanism for unrestricted abilities and short-circuits the board entirely.

**A node grants up to eight ids.** Editing the id list at `+8` of a node changes what that square
unlocks without touching any character's mask.

**Quickenings cannot be granted this way** (§5): they are gated on a *count* of bits 0–17, so setting
an unrelated bit in that range changes how many Quickenings are usable.

## 11. What is not known

- ~~**What License bits 0–17 are**, beyond that their popcount gates Quickenings (§5).~~ *(answered for the shipped tables: see CONTRACT-license-check.md §14 — licence records 0–17 list no id, the action mask builder never sets those bits over all 543 ability ids, and party rows 0–5 name exactly the 18 Quickenings `0xD0`–`0xE1`; whether the board can grant four of them to one record stays open; 2026-10-02, OPUS)*
- ~~**The live node count and stride** — both runtime-loaded; the image holds only the descriptor.~~ ~~*(answered: see license-board-grid-format.md §2.3 — the shipped `license_data.bin` holds 360 records of 24 bytes, `32 + 360 * 24 = 8672`; 2026-10-02, OPUS)*~~ *(answered: the live table `02EBF038` holds 361 records of 24 bytes, the `st2e` section at `battle_pack.bin` directory `+0x34`; the image's descriptor carries the count `+4`, the `u16` stride `+8` and the row handle `+0xC`; see the section "13. Buying a licence square: 00323D10" below; 2026-10-02, OPUS)* *(corrected 2026-10-02, OPUS: the node table the game checks is `02EBF038`, bound only by `00236C30` at `00236D5C`–`00236D67` from the `battle_pack.bin` blob (`0208E680`) directory `+0x34`, an `st2e` table of 361 records of 24 bytes in all nine language copies; `00322C50` reads its count `[02EBF038]+4` (`00322FCB`–`00322FD9`); the `license_data.bin` path strings `00A400B8` and `00C19F18` have no code reference, so the standalone 360-record files are not what the game loads)*
- ~~**What `00322C50(class)` tests.**~~ *(answered: see §9's falsification pass, "Both gates are passed the id" — it is `00322C50(class, id)`, a bounds check of this id: class 20 admits `0 ≤ id < count` of the action table, class 1 derives the id's class; 2026-10-02, OPUS)* It is a 1,025-byte shared validator; the action path passes
  `0x14` and the equipment path `1`, and a zero return refuses every License in that path — which no
  observed play state reaches. ~~**Read as a gate, not understood.**~~ *(answered: §9; 2026-10-02, OPUS)*
- ~~**How the mask is populated** when a player buys a square. The write side is
  `BattleStats_SetLicenseNodeStateAndApplySideEffects` (`00323910`, 665 B) with
  `BattleStats_CheckLicenseNodeAcquireReason` (`00323D10`) deciding whether a purchase is allowed —
  **both located, neither read here.**~~ **The gate is read (2026-09-11, OPUS-NOTICE-NODE360):**
  `00323910(page, node, set, flags)` refuses a non-party record (`0032393D`), then
  `BattleEncodedId_IsValidForClass(0x19, node, 1)` (`00323943`–`00323953`) — class 25 is the node
  table `02EBF038`, and the validator's rule is `0 ≤ node < count` against the table's own count
  dword — and returns `-1` without writing on failure; on success it sets or clears the bit at
  `+0x194 + node / 8` (`003239E7`–`00323A29`), charging the row's LP byte `+4` against `+0x190`
  when `flags` bit 0 is clear (`003239C3`–`003239E1`). Every route into the bitmap passes through
  it: the definition initialiser (`0023AE7C`), the SetSaveData apply (`00239D55`) and the licence
  menu (`0055CD40` → `BattleStats_SetLicenseNodeStateByStatsIndex` `003235C0`). ~~**So node 360 —~~
  ~~present on every job board — cannot be granted with the 360-record table every language of this~~
  ~~build loads** (the grid page §5); the auto-status rebuild's read of row 360 is unreachable from~~
  ~~the game. Two residuals: a save image whose bitmap already carries bit 360 (whether the save-side~~
  ~~copy masks bits beyond the count is unread), and~~ **Node 360, present on every job board, passes this range check**: the table the game loads holds 361 records, so the auto-status rebuild's read of row 360 is in range, and the square, the only category-`0x1E` row, is gated by presence bit `0xC01F`, tested by `00323D10` at `00323E88` (the section "13. Buying a licence square: 00323D10" below) *(corrected 2026-10-02, OPUS: the node table the game checks is `02EBF038`, bound only by `00236C30` at `00236D5C`–`00236D67` from the `battle_pack.bin` blob (`0208E680`) directory `+0x34`, an `st2e` table of 361 records of 24 bytes in all nine language copies; `00322C50` reads its count `[02EBF038]+4` (`00322FCB`–`00322FD9`); the `license_data.bin` path strings `00A400B8` and `00C19F18` have no code reference, so the standalone 360-record files are not what the game loads)*. The one residual is the menu's own row lookup for the square under
  the cursor in `0055CD40` — **read 2026-09-17 (SWE2-FRONTIER): guarded.** At
  [`0055D9B1`](../_index/ADDRESS-INDEX.md) the body loads ~~the record count~~ the cursor square's node id `[rcx+8]` and compares
  it to `0x168`; ~~on the stock count~~ for node 360 it substitutes the sentinel pair `0x1690169` *(corrected 2026-10-02, OPUS: word `+8` is the node the grant receives, `0055DA6A` passes it to `003235C0` at `0055DA6E`, and node 360 still reaches that grant, where `00323D10` gates it on bit `0xC01F`)*
  (`0055D9BC`) and never calls the row accessor, otherwise it reads the cursor
  square `byte [rsi+0x60]` through `00323630` (`0055D9C8`). The grant route is the
  same guard's tail: `003235C0` at `0055DA6E` with `r8d = 1`. **A stock install
  cannot read past the table.** ~~`00323D10` remains unread.~~ *(answered: see the section "13. Buying a licence square: 00323D10" below - it returns a reason code, 0 when the square may be taken, and writes nothing; 2026-10-02, OPUS)*
- **Whether `kind` is ever anything but 1** in `00323BB0`'s call from `00323EC0`; it is a constant at
  the only call site read.

## 12. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Return polarity: non-zero = licensed | the caller's `if (…) return 0; return 0x10;` in `00306480`, read from bytes | 1 |
| The three unconditional passes (§3) | `00323EC0` `00323EEA`–`00323F03`, complete decode | 1 |
| Bit `0x2000` at `+0x2C` short-circuits | `mov eax,0x2000 / test word [rcx+0x2C],ax / mov eax,1 / ret` | 1 |
| The 46-byte overlap and its early exit | `00323BB0` decoded in full; loop bound `cmp rax,0x2E` | 1 |
| The mask lives at `unit + 0x194` | the displacement in both `00323BB0` and `00324020` | 1 |
| Quickening range is `0xD0`–`0xE1` | `lea eax,[rbx-0xD0] / cmp eax,0x11 / ja` | 1 |
| `0030A330` searches exactly 3 entries | `cmp rax,2 / ja` and `cmp rax,3 / jl`, complete decode | 1 |
| Node rows: category `+5`, eight ids at `+8` | `002F8FA0` loop body, `cmp ecx,8 / jb` | 1 |
| Equipment passes `kind = 0`, actions `kind = 1` | `xor edx,edx` in `00323C60` vs `mov edx,1` in `00323EC0`, both at the tail call | 1 |
| Equipment rows indexed `itemId − 0x1000`, flag `+7` bit `0x10` | `lea ecx,[rdi-0x1000]` and `test byte [rcx+7],0x10` | 1 |
| One bit per node; ≤ 368 nodes *(a precondition: the builder does not check it, §6)* | `memset` length `(count+7)/8`, computed in 32 bits before the signed loop gate; buffer is `0x2E` bytes, zeroed by the caller | 1 |

**Controls.** The absence claim is *"no cache in this path"*: the same reading positively identifies
the stack buffer's zeroing on every call and the full re-scan, so the zero is a measurement.
`002F8FA0`'s node loop was read to its `jge` exit rather than to the first `return`, because a loop
whose body sets bits must be read past its first success to know it does not stop there — **it does
not; it accumulates every matching node**, which is what makes §4 an overlap rather than an equality.

**Not re-derived here.** Reason code `0x10` and the availability chain come from
[`battle-command-availability-and-reason-codes.md`](../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md);
the record kind byte from
[`battle-record-kind-byte.md`](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md).
`check_already_answered.py` was run for these addresses and terms before any of this was written.

## 13. Related

- [`battle-command-availability-and-reason-codes.md`](../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md) — where reason `0x10` is raised.
- [`battle-record-kind-byte.md`](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) — the `unit[5]` gate in §3.
- [`item-id-encoding-and-equipment-compatibility.md`](item-id-encoding-and-equipment-compatibility.md) — the other read mechanism in this category.

## 13. Buying a licence square: 00323D10 (OPUS, 2026-10-02)

**What `00323D10` is.** `BattleStats_CheckLicenseNodeAcquireReason(record, node, flags)`, 428 B (`00323D10`–`00323EBB`), read whole from the shipping bytes, with every callee read one level down. It returns a **reason code** (0 means the square may be taken) and **writes nothing**: it has no store to memory, and its only side effects are its callees' reads. Static read only; nothing was executed.

**Arguments.**

- `rcx` is the character's `0x1C8`-byte stats record (`rbp`, `00323D26`). The wrapper `00323600` (43 B) computes it as `[02EBF190] + 8 + slot × 0x1C8` (`0032360F`–`00323627`). It passes `rcx = 0` when `slot > 0x27` (`00323600`–`00323605`).
- `edx` is the node number, zero-extended from a `u16` by the wrapper (`00323607`, `00323624`). It is kept in `ebx` (`00323D22`).
- `r8d` holds the flags. Only bit 0 matters: `esi = ~flags & 1` (`00323D1F`–`00323D29`), so `esi = 1` means "charge LP".

**Callers.**

| caller | site | args | uses the result as |
|---|---|---|---|
| `00323600` (slot wrapper) | `0032360A`, `0032362A` (tail jumps) | `flags` passed through | — |
| ← `0055BFF0` (board sweep) | `0055C163` | `flags = 0` (`0055C111`) | reason → display table `0055C504` (16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md:146-157) |
| ← `0055E2C0` | `0055E363` | `flags = 0` (`0055E35D`) | reasons 3, 4 and 5 are skipped (`0055E368`–`0055E36E`) |
| ← `0055F830` | `0055F96F` | `flags = 0` (`0055F969`) | kept in `ebp`, then story flag `0x4B9` is tested (`0055F974`–`0055F97B`) |
| ← `00282E80` | `00282E87` | `flags = 0` (`00282E84`) | `return reason == 1`, meaning "owns it" (`00282E8E`–`00282E91`) |
| `00323910` (node set/clear) | `0032396D` | `flags = its 4th arg` (`00323965`), and only when `set != 0` (`0032395C`) | any non-zero result returns `-1` with no write (`00323972`–`00323979`) |

Who calls `00323910`, and what it passes:

- The menu grant `003235C0` passes `set = 1` (`0055DA60`) and `flags = 0` (`003235CA`/`003235D5`).
- The definition initialiser `0023AC80` (`0023AE6E`–`0023AE7C`) and the SetSaveData apply `00239960` (`00239D47`–`00239D55`) both pass `set = 1` and `flags = 1`. Those start-owned grants still go through this check.

**The rule, in order** (the first matching line returns):

```
if (record == NULL)                         return 6;   // 00323D2C-00323D43 (lea eax,[rcx+6] with rcx = 0)
if (!BattleEncodedId_IsValidForClass(0x19, node))  return 7;   // 00323D44-00323D6A
        // class 25 = node table 02EBF038; valid iff 0 <= node < [02EBF038]+4 (00322FCB-00322FDC, 0032302C-00323041);
        // the r8d = 1 that 00323D49 passes is not read by the validator (00322C50 never reads incoming r8)
if (record.b[0x194 + node/8] & (1 << node%8)) return 1;  // already owned: 00323D6B-00323DAB
row = res(02EBF038.+0xC) + node * 02EBF038.w[+8];        // 00323DAC-00323DE9 (NULL -> 0 at 00323DED)
switch (row.b[+6]) {                                      // square kind: 00323DF0-00323E09
 case 0:  // ordinary
   if (row.b[+5] == 0x1E)                                 // 00323E88-00323E8C
       return QueryMode0Positive(0xC01F) ? 0 : 8;         // 00323E8E-00323EA3
   return 0;                                              // 00323EA5
 case 1:  return AnyPartyRecordOwnsNode(node) ? 3 : 0;    // 00323E78-00323E86 (neg/sbb/and 3)
 case 2:  return CountLicenseBits00To17(record) >= 3 ? 4 : 0;  // 00323E61-00323E76 (cmovge)
 case 3:  if (AnyPartyRecordOwnsNode(node)) return 3;     // 00323E2C-00323E3C
          if ((unsigned)(node - 0x12) > 0xC) return 5;    // 00323E3E-00323E44, 00323E5A
          return QueryMode0Positive((u16)(node - 0x4000)) ? 0 : 5;   // = 0xC000+node; 00323E46-00323E5F
 default: // kind >= 4
   if (esi && row.b[+4] > record.d[+0x190]) return 2;     // 00323E0B-00323E20 (unsigned jbe)
   return 9;                                              // 00323E25
}
```

**The callees, one level down.**

- `BattleEncodedId_IsValidForClass` `00322C50`. The class-25 arm reads the count dword `+4` of descriptor `02EBF038` (`00322FCB`–`00322FDC`) and admits `[0, count)` (`0032302E`–`00323041`).
- `0020E600` turns the descriptor's 32-bit `+0xC` handle into the row base. It is called twice, the same pattern as in the setter (`00323DBF`–`00323DD6`).
- `AnyPartyRecordOwnsNode` `00324280` (107 B). It loops over records `i = 0..6` (`cmp r8b, 7 / jb` at `003242DC`) of `[02EBF190] + 8 + i × 0x1C8` (`003242A7`–`003242B6`). It skips a record unless `byte[+0]` has bit 3 (`003242BB`). It returns 1 on the first record whose `+0x194` bitmap holds `node` (`003242C0`–`003242D7`, `003242E5`), otherwise 0 (`003242E2`). Notes:
  - The `cmp r8b, 0x27 / ja` at `003242A1` can never fire.
  - The caller's own record is included, but for that record the own-bit test at `00323D92` has already returned 1.
- `BattleStats_CountLicenseBits00To17` `00324020` (218 B). It runs 3 iterations × 6 bit tests over `+0x194` with a rotating mask (`00324040`–`003240E6`). It returns the number of bits 0–17 set in **this record only**.
- `BattleEncodedId_QueryMode0Positive` `0030B0E0` (146 B):
  - Id `0xFFFF` gives 0 (`0030B0E6`–`0030B0FE`), and a nibble above `0xE` gives 0 (`0030B106`–`0030B11A`).
  - Otherwise it takes record `01EEBCC0 + (id >> 12) × 0x58` (`0030B11C`–`0030B133`).
  - It requires `(id & 0xFFF) ≤ [+0x3C] − 1` (`0030B136`–`0030B143`) and a non-null `[+0x50]` handler (`0030B145`–`0030B14C`).
  - It returns `handler(id, 0) > 0` (`0030B14E`–`0030B15B`).
  - For nibble `0xC` (class 17) the image holds count `0x20` and handler `002FD970`, so `0xC000`–`0xC01F` are all in range. Mode 0 of `002FD970` tests bit `index & 0xF` of word `index >> 4` in the region-A bitset at descriptor `+8` (`002FDA2F`–`002FDA57`). [The encoded-id page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.9 places quickenings at `0xC000`–`0xC011` and the Esper range at `0xC012`–`0xC01E`. `0xC01F` is the 32nd and last bit of that class. Its only immediate in the code is `00323E8E` (whole-image `retool grep 0xc01f`, one hit).

**Data read.**

| what | where | read at |
|---|---|---|
| owned bitmap | record `+0x194 + node/8`, bit `node % 8` | `00323D85` |
| LP pool (`u32`, compared unsigned) | record `+0x190` | `00323E13` |
| node table descriptor | `02EBF038`: count `+4`, stride `u16 +8`, row handle `+0xC` | `00322FD9`, `00323DE2`, `00323DBF` |
| node row: LP cost | `u8 +4` | `00323E0F` |
| node row: category | `u8 +5` | `00323E88` |
| node row: square kind | `u8 +6` | `00323DF0` |
| party records | `[02EBF190] + 8 + i × 0x1C8`, `i < 7`; byte `+0` bit 3 and `+0x194` | `003242A7`–`003242C3` |
| class-17 presence bits | `01EEBCC0 + 0xC × 0x58`: count `+0x3C`, handler `+0x50`; region A `+8` | `0030B13C`, `0030B145`, `002FDA2F` |

**What the shipped table makes reachable.** `02EBF038` has exactly one binder: `00236C30` at `00236D55`–`00236D67`. That binder calls `003845F0` on the STATIC blob's directory dword `+0x34`, and a whole-image `refs` shows no other write or `lea`. That section of `battle_pack.bin` is an `st2e` table of **361 × 24 bytes** in each of the `in`, `ch`, `us`, `kr` and `cn` copies. Over its rows:

- **Kind byte `+6`:** `0` on 330 rows (nodes 31–360), `2` on nodes **0–17** (category `0x13`, no granted ids) and `3` on nodes **18–30** (category `0x14`, granting actions `0x106`–`0x112`). No row has kind 1 or a kind of 4 or above.
- **Category `0x1E`:** one row only, **node 360**: `LP 30, kind 0, start mask 0, ids {0x0080}` (row bytes `6819 8442 1e 1e 00 00 8000 ffff…`).

So on shipped data:

- Quickening squares (0–17) are refused with **4** once the character holds three of them. The check counts only the character's own bits. It does not look at other party members.
- Esper squares (18–30) are refused with **3** if any of the seven party records with `byte[+0]` bit 3 owns that node. Otherwise they are refused with **5** until bit `0xC000 + node` (`0xC012`–`0xC01E`) is set.
- Node 360 is refused with **8** until bit `0xC01F` is set.
- Every other unowned ordinary square returns **0**.
- The kind-1 arm (`00323E78`), reason **2** and reason **9** (`00323E0B`–`00323E25`) are unreachable.

**Not tested here.**

- **Adjacency.** There is no neighbour or grid read in the body. Adjacency belongs to the menu's `0055E090`/`0055E3F0` passes.
- **LP sufficiency for any shipped square.** The LP compare lives only in the kind-4+ arm. The menu grant passes `flags = 0`, gets 0 back for any eligible kind-0/2/3 square, and the setter then deducts `row.b[+4]` from `+0x190` floored at 0 and capped at 99,999 (`003239C3`–`003239E1`: `jns`, `mov edx, ebx`, `cmovg` against `0x1869F`). Affordability is the sweep's bit 14 (`0055C492`, per the UI page), which this read did not re-derive.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

Every structural claim reproduces from the bytes:

| claim | measured |
|---|---|
| the three early passes return **licensed** | all three jump to `00324002`, which is `mov eax, 1` / `ret` |
| the kind byte and slot test | `movzx eax, byte ptr [rsi + 5]` / `test` / `jne`, then `cmp byte ptr [rsi + 4], 6` / `ja` |
| Quickenings are ids `0xD0`–`0xE1`, **18** of them | `lea eax, [rbx - 0xd0]` / `cmp eax, 0x11` / `ja` — unsigned `≤ 17`, so `0xD0`…`0xE1` |
| the requirement buffer is **46 bytes** | zeroed as five qwords, a dword and a word — `0x20`…`0x4D` = **`0x2E`** |
| the overlap loop | `movzx ecx, byte ptr [rbx + rdx + 0x194]` / `test byte ptr [rdx], cl` / `jne` — first non-zero returns 1; `cmp rax, 0x2e` / `jl` |
| `0030A330` searches three bytes and returns **3** when absent | `cmp rax, 2` / `ja` guards `[rax + r9 + 4]`, a null row yields `0xFFFF`, the loop is `cmp rax, 3` / `jl`, and the return is the miss count |
| the popcount walks the same mask | `00324020` indexes `[r8 + rbx + 0x194]` |

### ⚠ Both gates are passed the id, and that changes what they are

§3 writes `BattleEncodedId_IsValidForClass(0x14)` and §5b `…(1)`, with no second argument. Both
calls pass one:

```asm
00323ED0  mov ebx, edx            ; the action id, saved
00323ED2  lea ecx, [r8 + 0x14]    ; class 20 - and EDX still holds the id
00323ED6  call 0x322c50
```

The validator's signature is `(class, id)`. So §3's gate is **not** a blanket "class-20 gate" that
"refuses everything"; it is a **bounds check of this action id** — class 20's arm reads descriptor
`02EBF138`, the action table, and admits `0 ≤ id < count`
([the class registry](../00-Engine-Core-Runtime/the-encoded-id-class-registry.md)).

And §5b's is sharper still. **Class 1 is the dynamic arm** — "work out what this id is" — and for an
equipment id `0x1nnn` the top nibble `1` derives **class 6**, whose ids are based at **`0x1000`**.
That is precisely the `itemId - 0x1000` on the next line of §5b. **The subtraction and the class
call are the same fact**, reached here from the id side and in the registry from the validator's
arms; neither page had both halves.

### ⚠ The "no License" bit is a byte another page calls unread

`00323F4D mov eax, 0x2000` / `00323F52 test word ptr [rcx + 0x2c], ax` is a **16-bit** test, so
`0x2000` is **bit 5 of the byte at `+0x2D`** — and
[the action definition row](../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md)
lists `+0x2D` as *"a flags byte; reader not found"*. **This function is its reader**, for bit 5.

Counted over the 543 shipped rows: **98 carry it.** The action row's tally of `32 × 47` counts only
rows whose whole byte is `32`; bit 5 occurs inside **eight** distinct values — `32, 48, 96, 100, 104,
105, 160, 176`. So **98 actions need no License**, not 47.

> Two pages held the halves: one had the byte and no reader, the other had the reader and called the
> field `+0x2C`. They missed each other because the reader tests a **word** at `+0x2C` and the field
> map tabulates **bytes** — the same bit under two names.

**Not claimed:** ~~§4's `LicenseData_BuildPrerequisiteNodeMaskForRequirement` (`002F8FA0`, 287 B) was~~
~~not read, so *what* requirement mask a kind and id produce is untouched.~~ *(answered: see §6 and its 2026-09-27 qualification — `002F8FA0` is read whole, and CONTRACT-license-check.md §13 re-reads it statically; 2026-10-02, OPUS)* ~~§5's open item — whether~~
~~bits 0–17 are exclusively Quickening squares — stands.~~ *(answered for the shipped tables: CONTRACT-license-check.md §14; 2026-10-02, OPUS)* Nothing was executed or observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **Presentation — SERVICE.** The 3,564-byte board body `0055CD40` calls a 460-byte Presentation body.
- **Audio — MECHANICAL.** `0055CD40` plays a UI cue through the gated request wrapper.
- **Gameplay — MECHANICAL.** `BattleEncodedId_IsValidForClass` is the shared id-validity query
  ([the shared neighbours page](../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md)).
  The licence functions this page cites call it: `00323910`, `00323C60`, `00323D10` and `00323EC0`. `00323D10` also
  calls `BattleEncodedId_QueryMode0Positive`. The slot map and the 8,136-byte licence body are further callers.
- **Movement - CLIENT (2 edges).** `00322C50` is also called by bodies filed to movement: `0031BAC0`, `00326BB0` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (9 edges).** `00322C50` is also called by bodies filed to party: `003170E0`, `0031AC00`, `0031B510` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (5 edges).** `00322C50`, `00323890` are also called by bodies filed to status/periodic terminal: `0030E130`, `0030FED0`, `00310DB0` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **ActorEntity — CLIENT.** A cited function is called by `BattleSlotMap_InitializeMappingClasses`, `BattleGroup_RefreshFourActorDefinitions`, `BattleUnit_FindByDefinitionSelector`, `BattleUnit_ApplyUnitDefinition` and `BattleUnit_FindMappedDefinitionSelectorByIndex`.
- **CombatAction — CLIENT and SERVICE, 16 edges.** Cited functions are called by `BattleAction_CheckActionAvailabilityReason` (2), `BattleAction_GetSubtype3Field22OrFFFF`, `BattleAction_GetPrimaryRangeScalar` and two action bodies (183 and 244 bytes). They call `BattleAction_CheckDefinitionCategoryAvailability` and `BattleAction_ComputeSecondaryResourceMultiplier`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleEnmity_AnyAboveThreshold`, owned by that layer, calls `00322C50` on this page. That caller is the threshold scan over the same enmity bytes at `[+0x6A0] + 0x19`, id by id; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_InitializeDefinitionRecord`, owned by that layer, calls `00323910` on this page. That caller is the `0x1C8`-byte record initialiser, and it states the sentinels: `qword[+0x50]` becomes `-1`, `word[+0x58]` and `word[+0x1C3]` become `0xFFFF` and `byte[+0x1C5]` becomes `0xFF`, after which the definition id's **high byte** selects which authored table its low byte indexes; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).



**Rewards_Progression_Economy — CLIENT.** `0030B0E0` on this page is consulted by that layer. The crossing is that the layer calls this page's helper, not a shared responsibility. Read from the shipping bytes 2026-09-19 (SWE2-EC7).

### Interior citation — frontier hub `00323630` (2026-09-18, SWE2-EC7)

`00323630` — 54 B, 12 callers, `BattleStats_GetLicenseBoardSelector`: `cl`
above `0x27` returns `0xFF`; otherwise `imul rcx, rax, 0x1C8` at
[`00323638`](../_index/ADDRESS-INDEX.md) strides the `[02EBF190]+8` row table,
`byte[+5]` must be clear and `byte[+4]` at most 6, and the answer is
`byte[row+0x1C4]`. The license-cell selector byte the board tests read.
## SWE2-EC7-39 update (2026-09-19) - `00323D10`

`00323D10` (428 B) is the `BattleStats_CheckLicenseNodeAcquireReason` body the page names - `02EBF038`, `0020E600`/`00324280`/`0030B0E0` pairs plus `00322C50`/`00324020`. Interior anchor `00323D4D` (a `00322C50` call).

## SWE2-EC7-43 update (2026-09-19) - `002F8FA0`

`002F8FA0` (287 B) is `LicenseData_BuildPrerequisiteNodeMaskForRequirement` - `02EBF038` node table, `0020E600`/`00323890`/`00861EC0`; the page's complete-body read stands. Interior anchor `002F8FE0` (a `0020E600` call).

## SWE2-EC7-51 update (2026-09-19) - `00323C60`

`00323C60` (172 B) is `BattleStats_HasRequiredLicenseForEquipment` - `0020E600`/`00322C50`; `xor edx,edx` passes `kind = 0`. Interior anchor `00323C76` (a `0020E600` call).

## SWE2-EC7-58 update (2026-09-19) - `00323BB0`

`00323BB0` (170 B) is the `BattleStats_HasLicensePrerequisiteForRequirement` body the license page names - `002F8FA0`/`00808C40` plus `01F44830`. Interior anchor `00323BFC` (a `002F8FA0` call).


`00323890` (83 B) is the class-code normalizer: `003241D0()`'s result minus `0x15` bounds-checks `<= 9` and jump-tables to a small enum - `0`, `1`, `2` or `3` by arm, `-1` outside the `0x15..0x1E` window - the license/battle-unit callers' class-to-slot map.

Interior anchor `003238A8` (function `00323890`).
