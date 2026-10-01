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
if (unit[4] > 6)           return 1;                          // party slot index
```

`unit[5]` is the **battle-record kind byte** documented in
[`battle-record-kind-byte.md`](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md),
and `unit[4]` is the party slot. So **the License system applies only to record kind 0 with a slot
index of 6 or less.** Everything else — and every unit whose slot index is out of range — is
**licensed for everything**, returned before a single node is read.

> **The board is not a property of the ability. It is a property of being a licensed party member.**
> Guests and non-party units do not fail this check; they never reach it.

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
    if (unit[0x194 + i] & req[i])  return 1;             // ANY overlapping bit
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
`BattleStats_CountLicenseBits00To17` (`00324020`) is an unrolled popcount over the **same
`statsRecord + 0x194` mask**, walking bit indices from 0 upward.

So each party slot has a row naming **three** action ids, and the *k*-th of them is available only
when the unit owns at least *k + 1* of License bits 0–17. **The gate is a count, not a match** —
which is exactly the shape of "you have unlocked two Quickenings, so you may use the first two."

**What is not established here:** whether bits 0–17 are exclusively the Quickening squares, and what
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
unit + 0x004   party slot index      (licensed only when <= 6)
unit + 0x005   record kind byte      (licensed only when 0)
unit + 0x194   owned-License bitmask, 46 bytes / 368 bits, one bit per board node

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

**To grant an ability, set any one of its nodes' bits** in the 46-byte mask at `unit + 0x194`. There
is no "correct" bit; §4 is an overlap test.

**To make an ability universally available**, set bit `0x2000` at `+0x2C` of its action row — this is
the engine's own mechanism for unrestricted abilities and short-circuits the board entirely.

**A node grants up to eight ids.** Editing the id list at `+8` of a node changes what that square
unlocks without touching any character's mask.

**Quickenings cannot be granted this way** (§5): they are gated on a *count* of bits 0–17, so setting
an unrelated bit in that range changes how many Quickenings are usable.

## 11. What is not known

- **What License bits 0–17 are**, beyond that their popcount gates Quickenings (§5).
- **The live node count and stride** — both runtime-loaded; the image holds only the descriptor.
- **What `00322C50(class)` tests.** It is a 1,025-byte shared validator; the action path passes
  `0x14` and the equipment path `1`, and a zero return refuses every License in that path — which no
  observed play state reaches. **Read as a gate, not understood.**
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
  menu (`0055CD40` → `BattleStats_SetLicenseNodeStateByStatsIndex` `003235C0`). **So node 360 —
  present on every job board — cannot be granted with the 360-record table every language of this
  build loads** (the grid page §5); the auto-status rebuild's read of row 360 is unreachable from
  the game. Two residuals: a save image whose bitmap already carries bit 360 (whether the save-side
  copy masks bits beyond the count is unread), and the menu's own row lookup for the square under
  the cursor in `0055CD40` — **read 2026-09-17 (SWE2-FRONTIER): guarded.** At
  [`0055D9B1`](../_index/ADDRESS-INDEX.md) the body loads the record count `[rcx+8]` and compares
  it to `0x168`; on the stock count it substitutes the sentinel pair `0x1690169`
  (`0055D9BC`) and never calls the row accessor, otherwise it reads the cursor
  square `byte [rsi+0x60]` through `00323630` (`0055D9C8`). The grant route is the
  same guard's tail: `003235C0` at `0055DA6E` with `r8d = 1`. **A stock install
  cannot read past the table.** `00323D10` remains unread.
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

**Not claimed:** §4's `LicenseData_BuildPrerequisiteNodeMaskForRequirement` (`002F8FA0`, 287 B) was
not read, so *what* requirement mask a kind and id produce is untouched. §5's open item — whether
bits 0–17 are exclusively Quickening squares — stands. Nothing was executed or observed live.

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
