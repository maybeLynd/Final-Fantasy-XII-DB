---
system: Gameplay capability / inhibition policy
category: 15-Input
status: DOCUMENTED - was REOPENED; both reopening triggers are resolved, the initialization residue is UQ-147, SUPERSEDED under the runtime rule (its live remainder is ASTRA's), and a non-author falsification pass on 2026-10-01 CORRECTED three statements (C-7 bit 5, the 002E1C40 tail, the 002E1CD0 polarity) and narrowed the null-leader question statically (owner re-status 2026-10-01, OPUS, on SWE2-STRUCT's swe2struct-capability-0930)
owner_layer: CodeDomain:InputGameplay (proposed) - no PrimaryOwner inherited
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
  previous_parent: 381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
audit:
  passes: 4
  last_pass: 2026-10-01
  last_pass_kind: falsification
  last_pass_state: swe2struct-falsification-2026-10-01 - row-2 bit set, 01E0C2C0 projection and request set {1,2,3,5,14,21} SURVIVED; C-7 bit-5 attribution, the 002E1C40 tail wording and the 002E1CD0 polarity CORRECTED; both reopening triggers resolved; the initialization residue is UQ-147, SUPERSEDED under the runtime rule (live remainder admissible: FABLE-REQ-ASTRA-LEADER-STATS-NULL, FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON); null leader unreachable under the typed BattleUnit census (GetPartyLeader bit 3, reset clears bits 2 and 3 before nulling +0x698)
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 2
  reopened_resolved: >
    audit_crossrefs.py found 00377C20 has 65 callers across 13 subsystems (17 in
    CombatAction) while the document treated it as a WorldAreaField detail, and cited
    01E0C2C0 as a function when it is data. Both corrections were applied to the body,
    and on 2026-09-02 both were independently re-derived from the graph rather than
    taken on the marker's word - see section 10.
---

# Gameplay capability / inhibition policy

> The engine-wide bitmask that decides which player operations are currently allowed, and
> the function that publishes the field/battle contribution to it.

## 1. What the player sees

The reason the Battle Menu is unavailable mid-cutscene, the Party Menu will not open while
an action is committing, you cannot change leader at certain moments, and target cycling
stops responding. It is not a per-menu check scattered through the UI; it is one shared
policy that every consumer reads.

## 2. Native mechanism

The policy is a **16-row x 32-bit** table. Different engine subsystems own different rows.
The effective mask is the OR-reduction of all 16 rows.

Primitives:

| Function | Role |
|---|---|
| `002E1C20(row, bit)` | set a bit in the selected row |
| `002E1CA0(row, bit)` | clear a bit in the selected row |
| `002E0FA0()` | OR-reduce all 16 rows, apply a runtime predicate, conditionally clear effective bit 19, return the aggregate |

`00313A00` reconciles **row 2** - the field/battle contribution - publishing bits
`0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 20`.

Its inputs:
- `02089350` - CombatAction current-selected-BattleUnit state (most bits mirror whether this is non-null)
- `00377C20` - a WorldAreaField field-record policy bit drives bit 10
- `00253B90` - a null predicate over global `01E0C2B8` contributes to bit 1
- `02089340 & 0x40` - ~~a shared runtime/gameplay flag~~ **battle-state bit 6, "a treasure is being opened"** ([the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.5, 2026-09-12); ~~when clear and no BattleUnit is
  selected, the tail reconciles a separate bit-5 gate via `002E1C40`~~ *Corrected 2026-10-01 (SWE2-STRUCT for OPUS):*
  the tail always calls `002E1C40(ecx, 5)`, with `ecx = 1` exactly when this bit is clear and no BattleUnit is
  selected. With `ecx = 1` it clears bit 5 of the 16-bit word `0215F1AC`, otherwise it sets it, and it always clears
  bit 5 of `0215F1B4`. Both words lie below the policy table `0215F1C0`, so this is not a policy row; row 2's own bit 5
  is written with the other selection bits (falsification pass below, checks F4 and F5)

**No ownership is inherited from any of those inputs.** The evidence spans CombatAction,
WorldAreaField, InputGameplay and UI - which is exactly why this is a CodeDomain
classification and not a PrimaryOwner one.

### Projection into UI refusals

`00254500` translates the aggregate policy into a UI-request inhibit mask: it iterates the
22 low policy bits and ORs a 32-bit value from the static table at `01E0C2C0`
(22 x 32-bit = 88 bytes).

| Policy bit | Inhibits UI request |
|---:|---|
| 0 | 2 |
| 1 | 1, 3, 5 |
| 2 | 3 |
| 3 | 2 |
| 5 | 5 |
| 6 | 14 |
| 8 | 1, 21 |
| 9 | 5, 14 |
| 10 | 3 |
| 4, 7, 11-21 | *(no UI projection - consumed directly elsewhere)* |

A zero entry does **not** mean the bit is unused. Several are read directly by gameplay and
Input consumers outside this translation.

Applying that table to row 2 gives the exact set `00313A00` can inhibit: **requests 1, 2, 3,
5, 14, 21** - Battle Menu, Party Menu, party-leader change, free-target cycling, and two
valid-but-unnamed slots.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00313A00` | `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation` | 289 B | reconciles row 2 — **classified 2026-09-02, GN checkpoint** |
| `002E0FA0` | aggregate policy reader | - | OR-reduce 16 rows |
| `002E1C20` / `002E1CA0` / `002E1C40` | policy bit set / clear / gate | - | primitives |
| `00254500` | policy -> UI-request inhibit mask | 67 B | projection |
| `00253C70` | `InputGameplay_ArbitrateDigitalInputAndModalState` | 1,599 B | canonical Input arbiter |
| `00377C20` | `FieldData_GetActiveFieldRecordBit15` | 78 B | WorldAreaField — **cross-cutting, see §5** |
| `00253B90` | null predicate over `01E0C2B8` | - | contributes to bit 1 |

`01E0C2C0` is **data, not a function** — see §4.

Aggregate consumers: **29 direct call sites across 25 functions** read `002E0FA0`, testing
bits 0, 4, 5, 6, 9, 10, 11, 18 and 21.

## 4. Data structures

```
Policy table         16 rows x 32 bits    (row 2 owned by 00313A00)
01E0C2C0             u32[22]              policy bit -> inhibited UI request bits
                                          88 bytes of static DATA, not a function
                                          SHA-256 eadec033c5635a6d9375347f46ff568904bd02c1fc465c931bc9f12d714bfd49
02089350             BattleUnit*          CombatAction current-selected unit
02089340             u32                  battle-state word (bit 6 = treasure opening, bits 9 / 10 = party down; world-tick §2.5)
01E0C2B8             u32                  force fight mode flag (C-5); read through 00253B90
```

*(Corrected 2026-09-30, SWE2-DATA: this row read `01E0C2B8 ptr meaning unproven`. C-5 answered it on 2026-09-02
(§7): it is the u32 force-fight flag, documented on
[the force-fight page](../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md).)*

## 5. Call chain

```
committed action reaches presentation readiness
  -> 00304850  BattleUnit_AdvanceStandardActionState
     -> 0030CA80  presentation-slot ready?
        -> enqueue packed BattleUnit ID into the 64-entry ring @ 022BEDA4
  -> 00313DB0  consumes the ring
     -> publishes 02089350
     -> 00313A00              <- THIS (reconcile row 2)

field-frame path
  -> 00234624 -> 00313A00     <- also called directly after field predicates update

consumption
  002E0FA0 aggregate
    -> 00254500 -> inhibit mask -> 00254B50 UI request router (refuses inhibited requests)
    -> 00253C70 InputGameplay arbiter and ~24 other direct consumers
```

**Upstream:** CombatAction current-unit publication, and field/runtime predicate updates.
**Downstream:** UI request refusal and direct gameplay/input eligibility gates.

### `00377C20` is not a WorldAreaField detail — it is engine-wide field state

Found by `audit_crossrefs.py` on 2026-09-02, not by reading. `FieldData_GetActiveFieldRecordBit15`
(78 B, WorldAreaField-owned) has **65 distinct callers** spanning almost every gameplay
subsystem:

| Callers | Subsystem |
|---:|---|
| 17 | **CombatAction** |
| 4 | Script/VM Native Bridge · Presentation · Movement (each) |
| 3 | CombatAI · Status/Periodic/Terminal (each) |
| 2 | ActorEntity · Items/Equipment/Shops/License (each) |
| 1 | CombatFormula · Input · Party · Rewards/Progression · WorldAreaField (each) |
| 21 | *no PrimaryOwner* - **but all 21 are explicitly classified**; see section 10 |

So this policy's bit 10 is fed by a predicate that **17 CombatAction functions also gate on
directly**. Whatever `bit 15` of the active field record means, it is a shared engine-wide
gameplay condition, not a UI concern — and treating it as an Input/WorldAreaField
implementation detail understates it badly.

That predicate now has its own document -
[`../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`](../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md).
Do not assume this policy is the only consumer of that field state, and do not reason about
bit 10 in isolation.

## 6. Modding notes

- **Do not call `00313A00` to "fix" state** you changed at a lower level. It is a derived-state
  reconciler; if you had to call it manually, the real mistake is upstream.
- **Do not write `02089350` directly.** It is published by `00313DB0` as part of a real
  action/presentation transaction.
- **XIIOnline:** this is *local* gameplay/UI capability state, not shared world authority.
  Never network the mask bits. The multiplayer-significant state underneath these menus -
  party composition, equipment, inventory, licences, Gambits, actor identity, action intent -
  must be synchronised at its own owners, and the local policy will follow.

## 7. What is not known

- [x] ~~Authored meaning of `01E0C2B8`.~~ **ANSWERED 2026-09-02** — it is the **force fight mode**
      flag, set by the script verb `setforcefightmode` (call id `0x0334`, arity-verified). The
      predicate `00253B90` is true when the mode is **off**. See
      [`../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md`](../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md). **C-5.**
- [x] ~~Authored field-bit meaning behind `00377C20` (open question **C-6**).~~ **Answered on
      [the field-record table page](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
      §2c / §4 (ledger reconciled 2026-09-12):** bit 15 of the field record's `u16` is the
      action-permission override set on 193 of 1,154 fields (towns and safe areas); its designer
      name is not in the binary.
- [x] ~~Meaning of the remaining aggregate bits, and of row-2 bits 4, 7, 11, 12, 20 which have
      no UI projection (open question **C-7**).~~ **Censused 2026-09-12 (FABLE), writer and reader
      sides.** *Writer:* `00313A00` publishes every row-2 bit but ~~1, 5 and 10~~ *Corrected 2026-10-01
      (SWE2-STRUCT for OPUS):* 1 and 10 from **one** condition
      — a BattleUnit is currently selected (`[02089350]` non-null, `00313A22`–`00313A29`) — through
      the set / clear pair `002E1C20` / `002E1CA0` (`00313A63`–`00313AF5`); bit 1 also admits
      `00253B90`, bit 10 is the field record's bit 15, ~~bit 5 goes through `002E1C40`. So bits 4, 7,
      11, 12 and 20 of row 2 *are* the selection mirror, indistinguishable from 0, 2, 3, 6 and 8 at
      the writer.~~ *Corrected 2026-10-01 (SWE2-STRUCT for OPUS):* and bit 5 is written from the
      selection condition like the others (`00313AA0`–`00313AA8`, edx 5, ecx 2). The tail call
      `002E1C40` writes bit 5 of the words `0215F1AC` and `0215F1B4`, not the policy table (§2). So
      bits 4, 7, 11, 12 and 20 of row 2 **are** the selection mirror, indistinguishable from 0, 2, 3,
      5, 6 and 8 at the writer (checks F3, F4 and F5 in the falsification pass below). Bits **12 and 20** are also in the fixed mask `0x139203` (bits 0, 1, 9, 12, 13,
      16, 17, 20) that `002E1CD0(on, row)` sets or clears wholesale on **rows 0, 3 and 6** from the
      field-entry, area-unload and notify functions (`00268D10`, `002628B0`, `00263050`, `0026C3E0`,
      `0026C5D0`, `00263660`, `002678C0`, `0025C830`, `0025D580`) and four menu handlers
      (`00344C60`, `00345140`, `003456E0`, `003464D0`) — the script side's block set. *Readers:*
      over all 25 callers of the aggregate `002E0FA0`, tracking the returned register, and the
      three direct row readers of `002E1020` (the Save/Load family, row 1): **bit 4** is tested by
      `002736B0`, `00273950` and `002C64C0` — the force-fight family ([the R2 force-fight toggle](../Modal-Toggles/r2-force-fight-toggle.md) §2e) asking
      "is no unit selected" — and by nothing else; **bits 7, 11, 12 and 20 are tested by no reader
      at all** and project to no UI request, so in this build they are written and never consumed.
      The remaining aggregate bits with readers are 5 (`00283270`), 10 (ten functions, the toggle
      appliers among them), 18 (`003C8B70`) and 21 (Save/Load, `00228380` / `00229AF0`).
- [x] **SD-3.** What aggregate policy bit 21 changes when it is set. It is set and cleared only by the Save/Load
      controller handlers (row 1, §*PROPOSED-repos2d-12 answered*), and its two consumers test it: `00228380`
      (`002283DA`), which the input arbiter calls, and `00229AF0` (`00229B03`, Audio). *Registered 2026-09-30
      (SWE2-DATA), static; supersedes PROPOSED-repos2d-13.* *(Answered by OPUS 2026-09-30 (`442815afc`), restated ANSWERED in register row SD-3 by SWE2-DATA 2026-09-30,
      [record](../../_index/candidates/sd3-bit21-pause-0930/README.md): the input consumer opens the **pause menu**. With
      bit 21 absent the pause opens at once. With it present and in row 1, the menu is built deferred and opens when
      `01FD4954` is raised (movie bring-up, `002CEB40`). With it present only in another row, the pause is refused. The
      audio consumer skips the full-screen audio hold. **Correction:** "set and cleared only by the Save/Load controller
      handlers" is false. A census of all 77 set/clear call sites also finds row-1 writers in the movie player
      (`001B7690`, `001B7F30`, `001B8400`, `001B82A0`), the spawn-verb body `0023FBE0`, `002CEB40` and the title-asset
      consumer `003939B0`; a row-0 writer, the title singleton's handler `00394070`; and the rows 2/8 restore loop
      `00229510`.)*
- [x] **SD-4.** What unit flag bit 24 means. The recompute tests it (`0023B131`–`0023B14F`); the battle-unit field
      map's flag table lists its writers and readers but gives no name. *Registered 2026-09-30 (SWE2-DATA),
      static.* *(SD-4 answered 2026-09-30 by OPUS `35db7fbb2`, [record](../../_index/candidates/sd4-unit-flag-bit24-0930/README.md).)*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Row-2 reconciliation and exact bit set | complete body of `00313A00` (289 B, plain-body `c076cfea...9d246`) | 1 |
| 16x32 policy shape and bit direction | complete bodies of `002E1C20`, `002E1CA0`, `002E0FA0` | 1 |
| Policy -> request projection | complete body of `00254500` (67 B, `7b993dc5...4dcd`) + static table `01E0C2C0` (88 B, `eadec033...fd49`) | 1 |
| `02089350` is CombatAction current-selected-BattleUnit | canonical V120 ownership, writer `00313DB0` | 1 |
| Aggregate is Input-domain, not a UI-only bitset | 29 call sites / 25 functions incl. canonical `00253C70` (1,599 B, `e6309cd5...fa093`) | 1 |

**Corrections from audit, 2026-09-02** (found mechanically, not by re-reading):

| Was | Now | Proved by |
|---|---|---|
| `01E0C2C0` listed in the *Key addresses* function table with an "88 B" body | it is **static data**, not a function; moved to §4 | `GHOST ADDRESS` — absent from the current function list |
| `00377C20` described only as "a WorldAreaField field-record policy bit source" | a **cross-cutting engine-wide field predicate** with 65 callers across 13 subsystems, 17 of them CombatAction | `UNACCOUNTED NEIGHBOUR` — verified against the 90,525-edge call graph |

The second is the more serious error. Nothing in the document was false, but it was
**incomplete in a way that would mislead a modder** into thinking bit 10 was a UI-side
concern. Incompleteness of that kind is a defect, not a stylistic gap.

**Superseded readings:** the earlier conservative names
`Runtime.ControlPolicy.FieldBattleOperationInhibitMaskReconciliation` and
`InputGameplay.FieldBattleOperationInhibitMaskReconciliation` are both superseded by the
current `CapabilityAndUIRequest` wording, justified by the exact projection table.

**Status:** **APPLIED AND PERSISTENCE-CERTIFIED**, GN checkpoint 2026-09-02. Fenced against the
live parent (body 289 B, gate hash `0966b7b4…a16071`), applied with exact expected count,
whole-project diff clean with immutable drift 0, packed with `PACK_PASS`, fresh-imported into
a new project and reproduced. Ledger moved 38,001 → 38,003 explicit, 160 → 158 unresolved.

Call chain re-derived from the live 90,525-edge graph at apply time: callers are exactly
`00234590` `BattleSystem_RunFieldFrameOrchestrator` (WorldAreaField) and `00313DB0`
(CombatAction); callees are exactly `00253B90`, `002E1C20`, `002E1C40`, `002E1CA0`,
`00377C20`. Both match the documented chain with no drift.

## 9. Related

- [`../../16-UI/Request-Router/ui-request-router.md`](../../16-UI/Request-Router/ui-request-router.md)
- [`../../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`](../../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md)

## Re-verification 2026-09-02 (AH-10)

Stamped against parent `381d2aea...`; re-checked against the current `2ed8affb...`.

**Addresses:** 15 cited - 14 function entries, 1 interior - 0 unresolved.

**Central claim re-derived, and sharpened.** The document describes `002E0FA0` as
*"OR-reduce all 16 rows, apply a runtime predicate, conditionally clear effective bit 19"*. The body
confirms every part:

```c
uint FUN_002e0fa0(void)
{
    acc = 0;
    p   = &DAT_0215F1D0;
    do {
        accA |= p[-1];          // 128-bit SIMD OR
        accB |= *p;
        p += 2;                 // 32 bytes per iteration
    } while ((longlong)p < 0x0215F210);

    uVar4 = fold128to32(accA | accB);

    if (FUN_00360360(0x10) != 0)
        uVar4 = uVar4 & 0xFFF7FFFF;     // <- conditional clear
    return uVar4;
}
```

**The row count is exact.** The loop reads four 16-byte vectors spanning `0x0215F1C0`-`0x0215F1FF` -
**64 bytes = 16 u32 rows**, reduced by SIMD OR and folded to a single 32-bit aggregate. "All 16 rows"
is literally what it does.

**Bit 19 confirmed arithmetically.** `0xFFF7FFFF` is exactly `~0x00080000`, and `0x00080000` is bit
**19**. The clear is gated on `FUN_00360360(0x10)`.

**Corroboration from elsewhere in the session.** `InputGameplay_ArbitrateDigitalInputAndModalState`
was independently found to be one of only five non-script consumers of the `Primary` persistent flag
bank, so the input capability layer really does read durable game state - consistent with this
document's account.

Also of note: `00313A00`, listed here as reconciling row 2, is one of the two functions whose
classification changed between the `01:09` and `01:23` graph dumps (see the unresolved-residual
document). It is now classified, which closes that loose end.

**Stamp advanced because the body was re-read**, per the evidence standard.

## Verification note 2026-09-02 — the call-site count is exact, and correctly phrased

During a database-wide sweep for counts phrased as *call sites* that were really **edge** counts,
this document's figure was re-measured at instruction level:

```
002E0FA0 : 29 CALL instruction sites across 25 distinct functions
```

**Exactly as written.** This is the only place in the database that distinguishes the two, and it
distinguishes them correctly — 29 sites across 25 functions is a figure a call-graph edge census
*cannot* produce, since edges hold one row per caller-callee pair and would have reported 25.

The sweep was prompted by the opposite error found elsewhere: an edge count reported as "10 call
sites" in
[`../../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md),
and a vacuous inference drawn from `edges == distinct callers` in
[`../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md).
**This document is the sweep's control: it got the distinction right before the rule existed.**

## 10. Falsification pass 2026-09-02 - the reopening re-derived, not trusted

**Attack chosen.** This document was **REOPENED** by `audit_crossrefs.py`, and the body already
carried the resulting corrections. The obvious failure mode is that a correction gets written down
and never checked - the marker believed because a tool produced it. So both reopening findings were
re-derived from the graph, and then the frontmatter that recorded the reopening was examined.

### The frontmatter was the real defect

The file carried **two `audit:` blocks**:

| block | says |
|---|---|
| first | `passes: 1`, `crossref_clean: true` |
| second | `passes: 0`, `crossref_clean: false`, plus the `reopened_reason` |

**YAML keeps the last duplicate key**, so every tool reading this file saw `passes: 0` - a document
with an AH-10 re-verification, a corrections table and a call-site verification note was being
counted as **never audited**, and simultaneously as not crossref-clean after its crossref findings
had been resolved. The two blocks are now merged into one.

Nothing else in the database has a duplicate frontmatter key, and no existing check could see this
one: the file's links resolve, its addresses resolve, its prose is self-consistent.
`check_consistency.py` now fails on duplicate top-level frontmatter keys.

### SURVIVED: both reopening findings, re-derived independently

| Finding | Re-derivation | Result |
|---|---|---|
| `01E0C2C0` is data, not a function | rows matching it in `functions.tsv` | **0** - confirmed data |
| `00377C20` has 65 distinct callers | distinct callers in `edges.tsv` | **65** - exact |

The subsystem distribution reproduces **cell for cell**: 17 CombatAction; 4 each for Script/VM,
Presentation and Movement; 3 each for CombatAI and Status; 2 each for ActorEntity and Items; 1 each
for CombatFormula, Input, Party, Rewards and WorldAreaField - 13 owned subsystems, 65 callers.

### REFINED: "21 unowned" understated how well attributed these callers are

`unowned` here meant *no PrimaryOwner*, which reads like a gap. Resolving those 21 against the two
other classification layers:

| | count |
|---|---:|
| carry a `GFZ.V121.CodeDomain.*` classification | **18** |
| `final_no_owner = true` (**explicitly** no owner - a classification, not an absence) | **2** |
| `00313A00` itself - unclassified in the 01:09 dump, classified by 01:23 | **1** |

**None of the 65 callers appears in the residual set — 158 functions when written, 30 at GN161** *(corrected 2026-09-14; the residual only ever shrank, so the claim holds a fortiori)*.** Every caller of
this predicate is explicitly classified. The table row is corrected accordingly.

That also **raises the combat weight**: 17 CombatAction owners plus 4 callers whose code domain is
`Gameplay.Combat.NativeSemanticHelper` means **21 of 65 callers are combat**, roughly a third,
strengthening rather than weakening the point made in section 5.

### Operational finding: the audit kit's inputs are one checkpoint stale

`functions.tsv` and `edges.tsv` on disk are the **01:09** dump and yield **160** unresolved; the
canonical `residual_addrs.txt` is the **01:23** dump at **158**. The `audit_crossrefs.py` docstring
says to *"regenerate both from the CURRENT parent before every audit pass"*, and they have not been.

This did not corrupt anything here - the counts above are structural, and the two functions that
moved between the dumps are known - but it is a live hazard for any pass that reads ownership from
those files, because a function classified after 01:09 still reads as unowned. **Any future
ownership census must regenerate the graph first.** Recorded as a standing caveat rather than
silently relied on.

## Cross-subsystem neighbours — disposition (audit pass, repos-2d, 2026-09-03)

`audit_crossrefs.py` against `Tools/work/graph_gn` reported **3 UNACCOUNTED NEIGHBOUR** findings
for this document. One of them is a **second owner of the policy table** and belongs in §2 rather
than in a disposition list.
- **ActorEntity - CLIENT and SERVICE (91 edges).** `0026D6D0`, `002E1CD0`, `00263660` are also called by bodies filed to actor entity: `0025C830`, `002628B0`, `00300E40` (+22 more); `002628B0`, `0026C5D0`, `00268D10` reach bodies filed to actor entity: `003588B0`, `0025B4C0`, `00233D70` (+32 more) - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT and SERVICE (15 edges).** `002DF370`, `00226BD0`, `002E0FA0` are also called by bodies filed to audio: `00229AF0`, `00229AB0`; `002628B0`, `003939B0`, `00229AF0` reach bodies filed to audio: `002DF370`, `00360B50`, `00360DD0` (+7 more) - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT and SERVICE (13 edges).** `00377C20`, `00253B90`, `0031B770` are also called by bodies filed to combat AI: `00301AD0`, `00308610`, `003014C0` (+1 more); `0023AC80`, `00234590`, `00283270` reach bodies filed to combat AI: `00325060`, `0032A650`, `00326030` (+4 more) - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT and SERVICE (50 edges).** `00377C20`, `00253B90`, `002DEE70` are also called by bodies filed to combat action: `00313DB0`, `002FFCF0`, `0030C010` (+17 more); `00304850`, `00234590`, `00300FC0` reach bodies filed to combat action: `003105D0`, `003065D0`, `00306BB0` (+22 more) - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT and SERVICE (4 edges).** `00377C20` is also called by bodies filed to combat formula: `00300530`; `00304850`, `0023A570` reach bodies filed to combat formula: `0023AC80`, `00387090`, `00387A50` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (12 edges).** `0032E520`, `001B8400`, `002E1CA0` are also called by bodies filed to core runtime scheduling: `0017D6E0`, `0022B8C0`, `0022A770` (+2 more); `00234590`, `001B8400`, `00253C70` reach bodies filed to core runtime scheduling: `001EDE70`, `0017D980`, `0032A100` (+3 more) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT and SERVICE (4 edges).** `00377C20` is also called by bodies filed to items/equipment: `00309FB0`, `0030FD10`; `0023AC80` reaches bodies filed to items/equipment: `0031A630`, `00323910` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (55 edges).** `003272A0`, `0026D6F0`, `00377C20` are also called by bodies filed to movement: `0026C3E0`, `00234520`, `00338490` (+21 more); `002628B0`, `00234590`, `00304850` reach bodies filed to movement: `0026D6F0`, `002EBE50`, `003246C0` (+19 more) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (48 edges).** `0026D6D0`, `003137F0`, `0031B770` are also called by bodies filed to party: `0023B040`, `00328BD0`, `00358B40` (+10 more); `0023B040`, `003266C0`, `00234590` reach bodies filed to party: `003590D0`, `0023B040`, `003272A0` (+10 more) - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - CLIENT and SERVICE (4 edges).** `00283270`, `00316930` are also called by bodies filed to platform/online achievements: `00316930`, `00316670`; `00316930` reaches bodies filed to platform/online achievements: `00315E90`, `003162E0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (16 edges).** `00377C20`, `002E0FA0`, `004235C0` are also called by bodies filed to presentation/rendering: `002B7B80`, `00308130`, `00400E80` (+8 more); `002628B0`, `00234590` reach bodies filed to presentation/rendering: `00307E70`, `002E65A0`, `002E8CC0` (+2 more) - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (10 edges).** `0032E520` is also called by bodies filed to resource: `0024AC30`; `001B7F30`, `0032E520`, `001B7690` reach bodies filed to resource: `0017D960`, `002DF980`, `0032E520` (+4 more) - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT and SERVICE (4 edges).** `003135C0`, `00377C20` are also called by bodies filed to rewards/progression: `002F8BB0`, `00312280`; `00234590`, `0023AC80` reach bodies filed to rewards/progression: `00319600`, `0030C470` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - SERVICE (1 edge).** `00582860` reaches bodies filed to save/load: `00582790` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (14 edges).** `00283270`, `002E1C20`, `002E1CA0` are also called by bodies filed to save/load/settings: `00582860`, `005823B0`, `005844A0`; `00582860`, `005823B0`, `002628B0` reach bodies filed to save/load/settings: `002EF2B0`, `00582040`, `00582240` (+5 more) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (31 edges).** `002E1C40`, `002E1CD0`, `0032E520` are also called by bodies filed to script VM / native bridge: `0033F1B0`, `00346860`, `00352000` (+25 more); `00344C60`, `003456E0`, `003464D0` reach bodies filed to script VM / native bridge: `00267E10`, `0026B4E0` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT and SERVICE (5 edges).** `003272A0`, `0023A570` are also called by bodies filed to spawn/encounter: `0023A3B0`, `00234AF0`, `002350C0`; `00234590`, `0023A570` reach bodies filed to spawn/encounter: `00307030`, `00236100` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT and SERVICE (8 edges).** `00377C20`, `002E8100`, `00300FC0` are also called by bodies filed to status/periodic terminal: `00310DB0`, `0030E360`, `0030F690`; `00234590`, `00304850` reach bodies filed to status/periodic terminal: `00300140`, `0030E360` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - SERVICE (1 edge).** `00253C70` reaches bodies filed to story/event/quest: `0032A8A0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT and SERVICE (60 edges).** `002E0FA0`, `002E1CA0`, `002E1C20` are also called by bodies filed to UI: `00279E20`, `003C8B70`, `0035D6B0` (+18 more); `003C8B70`, `00254B50`, `00253C70` reach bodies filed to UI: `003669D0`, `0028F970`, `003C87B0` (+25 more) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (33 edges).** `00234590`, `0023B040`, `00263660` are also called by bodies filed to world area: `00234590`, `00314020`, `00314440` (+2 more); `00253C70`, `002628B0`, `003266C0` reach bodies filed to world area: `00377C20`, `00313F60`, `00377700` (+7 more) - shared machinery across the layer boundary, no shared ownership.
### Save/Load/Settings is a second writer of the policy table

§2 says *"different engine subsystems own different rows"* and then documents row 2 and its owner
`00313A00`. The audit names another writer, and it writes through **both** primitives:

| Edge | Function | Owner |
|---|---|---|
| `002E1C20` ← `005823B0` | `SaveStorageQueue_ControllerStateHandler` (398 B) | Save/Load/Settings |
| `002E1CA0` ← `005823B0` | same, clearing | Save/Load/Settings |
| `002E1C20` ← `00582860` | `SaveLoad_ControllerLifecycleHandler` (1,777 B) | Save/Load/Settings |
| `002E1CA0` ← `00582860` | same, clearing | Save/Load/Settings |

Both handlers are named for **controller state and controller lifecycle** — which is what a save
system needs a capability row for: a controller disconnect or a save-in-progress must inhibit
player operations, and this is the mechanism it uses.

**Which row and bit — answered below.** The first census run abstained on all four sites, and its
row-argument distribution (`14 CONST, 24 DYNAMIC, 34 UNKNOWN`) was itself produced by a defective
instrument; both are superseded by the hand-read encodings in the next section. **Row 1, bit 21.**

### The other two

**Audio.** `002E0FA0` ← `00229AF0` (78 B, Audio) — an Audio-side reader of the aggregate mask,
consistent with §3's census of 29 call sites across 25 functions, which this document already
states but does not enumerate by owner. And `00313DB0` → `002DEE70` (13 B, Audio) — the ring
consumer named in §5 calling a small Audio helper on its own path; it is not part of the policy
reconciliation.

**Spawn/Encounter/Lifecycle.** `00234590` `BattleSystem_RunFieldFrameOrchestrator` →
`00307030` `SpawnGroup_DispatchPendingCompletionSignals`. The orchestrator is cited in §5 as one of
the two callers of `00313A00`; it is a field-frame hub with many callees, and dispatching spawn
completion signals is field-frame work belonging to that function's own system, not to the
capability policy. *Irrelevant here, with the reason stated.*

### Neighbours re-audited 2026-09-12 (FABLE)

`audit_crossrefs.py` against the current graph reports two findings, both dispositioned:

- **`00283270` ← `00316930` (PlatformOnlineAchievements).** The page cites `00283270` only as the reader of
  aggregate bit 5. `00316930` calls it with `ecx = 1` as its first act (`00316945`); what the achievement code
  does with the answer is not read. It is a caller of a cited reader, not a policy writer. *Recorded, not
  followed.*
- **`002628B0` → `0032E520` (Resource).** `002628B0` is cited as the area-unload caller of `002E1CD0`; a
  resource release on the same unload path is not policy work. *Irrelevant here, with the reason stated.*

### PROPOSED-repos2d-12 answered: Save/Load owns **row 1**, and the bit is **21**

All four Save/Load call sites write **row 1, bit 21**. Every one was read from the encoding by
hand, because a block-local liveness census had abstained on them:

| Site | Encoding | Row | Bit | Effect |
|---|---|---:|---:|---|
| `005823F8` | `xor edi,edi` … `lea edx,[rdi+0x15]` / `lea ecx,[rdi+1]` | 1 | 21 | **clear** (`002E1CA0`) |
| `0058252C` | `xor edi,edi` … `lea edx,[rdi+0x15]` / `lea ecx,[rdi+1]` | 1 | 21 | **set** (`002E1C20`) |
| `005828B4` | `mov edx,0x15` / `lea ecx,[rdx-0x14]` | 1 | 21 | **set** |
| `00582F1B` | `mov edx,0x15` / `lea ecx,[rdx-0x14]` | 1 | 21 | **clear** |

The second handler computes the row *from* the bit — `mov edx, 0x15` then `lea ecx, [rdx - 0x14]`,
so `row = bit - 20 = 1`. The first passes both as offsets from a zeroed register. Different
idioms, same pair.

The primitives confirm the shape: `002E1C20(row, bit)` is
`table[row] |= 1 << bit` over the 16-entry table at `0215F1C0`, bounded `row < 0x10`; `002E1CA0`
is the same with `&= ~(1 << bit)`.

**Independently confirmed from the consumer side.** Two functions test aggregate bit 21, and one of
them names the row without being asked to:

```c
/* 00229AF0, Audio, 78 B */
DAT_01E027FC = 0;
policy = 002E0FA0();                 /* the aggregate */
if (policy & (1 << 21))
    return FUN_002E1020(1);          /* <- reads policy row 1 directly */
if (FUN_00226BD0(0xF) == 0)
    return FUN_002DF370(0x3F, 1, 1); /* Audio */
```

`002E1020(row)` is a 14-byte per-row reader over the same table at `0215F1C0`. So a consumer that
sees bit 21 in the aggregate goes on to read **row 1** — the row the writers write. **Writer side
and consumer side agree on the row, and they can fail independently**, which is what makes this a
confirmation rather than a restatement.

The second consumer is `00228380` (204 B), whose only caller is
`InputGameplay_ArbitrateDigitalInputAndModalState`. It tests bit 21, reads a row, and tests bit 21
of the row.

**What the bit does is not established here.** *(Established since: SD-3, §7, 2026-09-30, OPUS. It decides whether the
pause menu opens at once, is deferred or is refused, and whether the full-screen audio hold runs.)* Bit 21 has no entry in the `01E0C2C0` UI-request
projection — §2's table lists bits 4, 7 and 11-21 as having none — so it is consumed directly by
gameplay and Audio rather than by refusing a UI request. The two handlers are named for controller
state and controller lifecycle, which is consistent with an inhibition raised while a save is in
progress or a controller is lost, but this document does not claim the behaviour from the names.
Carried as `PROPOSED-repos2d-13`. *(Registered 2026-09-30 (SWE2-DATA) as **SD-3** in §7; both consumers'
bit-21 tests are pinned by [`in_dd_checks.py`](../../_index/candidates/dd-data-0930/in_dd_checks.py) B21.)*

**Row 1 therefore has an owner**, and §2 can say so: `00313A00` reconciles row 2, and the two
Save/Load controller handlers own row 1 bit 21. *(Corrected 2026-09-30, OPUS: they are two of its owners, not the only
ones. The movie player, the spawn-verb body `0023FBE0`, `002CEB40` and the title-asset consumer `003939B0` also set or
clear row 1 bit 21; see SD-3 in §7 and [`sd3_pause.py`](../../_index/candidates/sd3-bit21-pause-0930/sd3_pause.py) W1.)*

## 10. `0023B040` read — the second consumer of `02089340 & 0x40`, and what it seeds

Section 2 lists `02089340 & 0x40` among `00313A00`'s inputs as *"a shared runtime/gameplay flag"*.
**A second function consumes the same bit and uses it very differently**, and it was on the *leaned on
and never opened* cut with three documents citing it by name only.

`PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`, 447 B). **Extent: 123
instructions, and the last instruction is `jmp 0x26bd40` — a genuine tail call**, `0026BD40` being its
own 10-byte function. The behaviour continues there.

### The bit seeds an all-or-nothing mask

```asm
0023B050  mov  eax, dword ptr [02089340]
0023B056  and  al, 0x40
0023B058  neg  al             ; CF = (bit set)
0023B05A  sbb  esi, esi       ; esi = -1 if set, 0 if clear
0023B060  and  esi, r14d      ; r14d = -1
0023B063  mov  ebx, esi
```

> **Bit `0x40` set means "start from fully suppressed"; clear means "start from nothing suppressed."**
> It is not one input among many here — **it is the initial value of the whole mask**, which the rest of
> the function then refines.

**And two more bits of the same word are read further in:** `test dword ptr [02089340], 0x600` selects
whether the leader's incapacity contributes at all. **So `02089340` carries at least three distinct
control-policy bits — `0x40`, `0x200` and `0x400` — and this document previously knew only the first.**

### The mask is three bits, and each goes somewhere different

```asm
0023B1C7  shr  edx, 2 ; and edx, 1     -> PartyControl_SetSuppressionMask1Bit(1, bit2)
0023B1D9  and  ecx, 1                  -> PartyControl_SetMovementSuppressionBit(bit0, 1)
0023B1E1  shr  ebx, 1 ; not ebx ; and 1 -> tail call 0026BD40(NOT bit1)
```

| bit | consumer | note |
|---:|---|---|
| 0 | `PartyControl_SetMovementSuppressionBit` | movement |
| 1 | `0026BD40`, **inverted** | the only inverted one |
| 2 | `PartyControl_SetSuppressionMask1Bit` | mask 1 |

**Bit 1 is inverted before publication:** a set mask bit produces permit byte **0**, and a clear
mask bit produces permit byte **1**. All three mask bits mean suppression; the stored permit byte
has the opposite polarity. (Corrected by independent original-code review, §11.)
**A reader who assumes one polarity across the mask gets one of the three backwards.**

### Control suppression uses a wider status set than action eligibility

```asm
0023B166  and  eax, 0x8800403b
0023B16B  cmove ecx, ebx           ; no match -> unchanged
0023B173  and  edx, 0x8800003b
0023B179  cmove ebx, ecx
```

Two status masks, and both are **strict supersets** of the `0x80000003` predicate this database has
tracked across eight sightings:

| mask | extra bits over `0x80000003` |
|---|---|
| `0x8800403B` | 3, 4, 5, **14**, 27 |
| `0x8800003B` | 3, 4, 5, 27 |

**They differ from each other by exactly bit 14 (`0x4000`).**

> **The statuses that stop you *controlling* a character are a superset of those that stop it
> *acting*.** A unit can be eligible to act on its own and still not accept player input — which is the
> mechanical shape of the conditions a player experiences as "I can't move but the gambits still run".

### What is not established

- [x] ~~What `0026BD40` (10 B) does with the inverted bit 1.~~ **Answered 2026-09-12 (FABLE):** it stores
      `arg != 0` into the byte `0209A2C5` (`0026BD42`), so the byte is **1 when mask bit 1 is clear** — a
      *permit* flag. Readers: the getter `00265460` (← `InputGameplay_ArbitrateDigitalInputAndModalState`
      `00254145`, the force-fight family `002C64C0`, `002C6F70` ×2, `003C8B70`) and `0026DFB0` (← field entry
      `00268D10`), which requires it **and** `0209A2C4` / `0209A2C6` set, plus a live focus actor.
- [x] ~~What bits `0x200` and `0x400` of `02089340` distinguish.~~ **Answered 2026-09-12 (by propagation):**
      bit 9 = every active member of the party is incapacitated, bit 10 = the whole roster is
      ([the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.5). Either one replaces the whole mask with all-suppressed
      **after the mode/field gates and non-null leader lookup are passed**
      (`0023B0CA`–`0023B0E3`); otherwise the initial seed is published (§11).
- [x] ~~What the paired predicates `00322600` and `00322920` test~~ **Answered 2026-09-12 (FABLE):** both test a
      **presentation event id** in the `0x20xx` space. `00322600(id)` is true for `0x2006` (the alive knockback
      HP event, [the HP write](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)) and
      `0x2037`, `0x2039`–`0x203C` (the evade / parry reaction events, [the scratch block](../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.6), and
      either hit makes the mask all-suppressed. `00322920(id)` is **false only** for `0x2001`, `0x2009` and
      `0x2031`, and any other id sets bit 1. The two ids tested are the value `002E8100` returns for the
      leader's handle (its character render record through `0041FCA0`, independently read in §11) and the unit's
      `lastPresentationEventId` `+0x05C` ([the field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)). *Selection settled 2026-09-12 (ASTRA's [render-event selection evidence](../../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md) §3–4; FABLE agrees after re-reading `0041FCA6`–`0041FCD7` and `004235C0`'s gates `004236B0`–`0042373E`):* the getter passes the **current** event `+0xCC` as `004235C0`'s selector, and the only rejecting selectors, 0 and 2, are kind-0 events that return 1 at the current-kind gate first, so **under stable valid records the leader's reported event is `+0xCE` whenever an alternate entry `+0xC8` is present, else `+0xCC`**. The call still resolves entry `+0xC4` (a possible cache write, or a fault on a null table with a nonzero id), so it is not removable from an effect model. ~~Residue: the names of events `0x2009`
      and `0x2031`, and the complete semantic selection performed by `004235C0` (§11).~~
      *Answered 2026-09-30 (SWE2-DATA), from FABLE's event-slot census
      [`bt4-event-motion-slots`](../../_index/candidates/bt4-event-motion-slots/README.md) (`event-slot-names.tsv`;
      [`in_dd_checks.py`](../../_index/candidates/dd-data-0930/in_dd_checks.py) EV0–EV1): `0x2001` is `ready`,
      `0x2009` `magic_ready` and `0x2031` `ability_ready`, so `00322920` exempts exactly the three ready poses. The
      selection residue is carried by UQ-148, SUPERSEDED onto UQ-193 and UQ-194, both ANSWERED 2026-09-27.*
- [x] ~~What the five extra status bits (3, 4, 5, 14, 27) are individually, and why bit 14 is in one mask
      and not the other.~~ **Answered 2026-09-12 (FABLE):** Stop, Sleep, Confuse, **Immobilize** and Berserk
      ([the statuses sheet](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)). Any of KO, Stone, Stop, Sleep, Confuse, Immobilize, Berserk or X-Zone on
      the leader sets mask bits 0 and 2 (movement and mask 1, `0023B15B`–`0023B16E`); any of them **except
      Immobilize** also sets bit 1 (`0023B170`–`0023B179`). Immobilize alone therefore **adds movement/mask-1 suppression without changing existing
      bit-1 suppression**. The permit remains on only when the seed, events, combo, action, unit flags
      and later mode-1 counterpart check leave bit 1 clear (§11). It is not an unconditional exemption.
- [x] ~~What `leader + 0x6B7`, `+ 0x6B4` and `word + 0x714` (compared against `0x21E`) hold.~~ **Answered
      2026-09-12 (by propagation, [the field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)):** `+0x6B7` is **combo progress** — any non-zero value
      makes the mask all-suppressed **when the leader recompute reaches that test**
      (`0023B124`–`0023B12D`); `+0x6B4` is the **action phase** and `+0x714` the
      **action id**, and bit 1 is set when the id is an action-definition id (`≤ 0x21E`, [the handler table](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md))
      in phase 9 or later, or whenever unit flag bit 24 is set (`0023B131`–`0023B14F`).

**Also read (2026-09-12):** the recompute is skipped, leaving the seed, when the chocobo-mode predicate `00303EC0`
([the mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)) or the field record's bit 15 holds (`0023B065`–`0023B079`); unit flag
**bit 46** forces all-suppressed when reached (`0023B0D4`–`0023B0E9`). ~~Neither flag bit 24 nor bit 46 is named by
[the field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md).~~
*(Corrected 2026-09-30, SWE2-DATA: bit 46 is named on
[the native command seam](../../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md): action phase 9
sets it when the action executes and phase 10 clears it, so it marks an action in execution. Bit 24 has a row in
the field map's flag table, with writers and readers, but no name; it is registered as **SD-4**.)*

## 11. Independent falsification: polarity, gate precedence and invalid state

**ASTRA, 2026-09-12. Result: REOPENED.** The event membership and local status-mask
arithmetic survive independent review. The former sentence that a set mask bit 1
means permit was reversed, and the unconditional Immobilize exemption was too broad.
Those sentences are corrected above. Related party-control prose still requires peer
propagation; this component review does not constitute the database's final audit.
*(Pointer 2026-10-01, SWE2-STRUCT for OPUS: the propagation is done. FABLE agreed on 2026-09-12 and OPUS on
2026-09-13 (the ticked box at the end of this section, and §12), and the party page carries the correction.)*

Evidence: [method, identity and controls](../../_experiments/evidence/capability-policy-falsification/README.md),
[complete primary bodies](../../_experiments/evidence/capability-policy-falsification/primary.json),
[raw original-code results](../../_experiments/evidence/capability-policy-falsification/result.json),
and [independent effect review](../../_experiments/evidence/capability-policy-falsification/review.json).
The reference executable has the exact SHA-256 in this page's frontmatter. The complete
447-byte body at `0023B040` has SHA-256
`1fddc7fe42c93f931e9a3a80acf674e267ee60bf30ec9ffba6809ce3e14b532e`.

### What was actually executed

Method A read 30 complete original bodies. Method B entered shipping `0023B040`
at its first instruction with injected, internally connected registry, actor, unit,
status, field, render and movement records. The two feasibility controls reached
opposite suppression outcomes before the larger bounded run. No callees were stubbed.
Across the final cases, 29 bodies executed; `004235C0` did not. The render record's
`+C8 = -1` selects the original `0041FCA0` direct `+CC` return. This is isolated
original-code evidence, not a live game, native initialization or normal scheduling.

The result contains 24 valid full-entry cases, 116 event-predicate cases and five
permit-setter cases. All 145 returned with the stack and nonvolatile registers
preserved and original code unchanged. A separate deliberate invalid-state case
faulted as described below; it is **not** counted as a successful return. The
independent reader replayed every non-stack read/write and final observed buffer,
and checked exact write order. Removing the requested-speed write from a private
copy of a receipt was rejected even with successful return/ABI flags retained.

### Contributions accumulate; skipped branches contribute nothing

Values below are the low three internal mask bits. The initial seed is zero unless
battle-state bit `0x40` is set. Defaults have a valid leader/status record, mode 0,
clear field bit 15, both event IDs `0x2001`, no combo or other inhibition.

| Controlled change | Mask | Permit byte | Distinguishing observation |
|---|---:|---:|---|
| Healthy default | 0 | 1 | Opposite control for status/movement writes |
| Immobilize in either status layer | 5 | 1 | Both layer reads contribute; bit 1 stays clear |
| Immobilize plus event `0x2002` in either event source | 7 | 0 | The status does not undo event suppression |
| Immobilize plus seed bit `0x40` | 7 | 0 | The status does not undo initial suppression |
| Stop | 7 | 0 | Control for the narrower status mask |
| Combo byte 1 or 255; or unit flag 46 | 7 | 0 | Nonzero unsigned combo boundary; adjacent flag 45 leaves mask 0 |
| Battle-state `0x200` or `0x400` | 7 | 0 | Applies within a reached leader recompute |
| Both incapacity bits, but no leader | 0 | 1 | The `0023B0CA` test is never reached |
| Both incapacity bits, combo and flag 46, but mode 2 or field bit 15 | 0 | 1 | The leader lookup is never reached |
| Seed `0x40`, mode 2 | 7 | 0 | Skipping recompute retains the seed |
| Action `0x21E`, phase 8 / 9 | 0 / 2 | 1 / 0 | Unsigned phase boundary |
| Action `0x21F`, phase 9 | 0 | 1 | Unsigned action-ID upper boundary |
| Unit flag 24, action `0xFFFF`, phase 0 | 2 | 0 | Flag overrides those action/phase tests |
| Mode 1, selected counterpart healthy / KO | 0 / 7 | 1 / 0 | A later unit can still replace the mask |

The last gate was absent from the earlier explanation. `003135C0` tests mode 1;
`003137F0` reads the battle-state block's `+5AD5` byte, and `0031B770` finds a unit
whose `+698` is the corresponding combatant record. When found, a null record or
`0x80000003` status match with the field override clear replaces the mask at
`0023B1B8`. The tested counterpart was a second constructed unit. Its gameplay role
and the scheduling/initialization of this selection remain open. *(Dispositioned 2026-09-30, SWE2-DATA: carried
by UQ-147, SUPERSEDED 2026-09-26 under the runtime rule; the live half is the ASTRA request
FABLE-REQ-ASTRA-LEADER-STATS-NULL, which keeps this page REOPENED.)*

### Output effects and preconditions

In order, the routine updates **bit 1** of byte `022C8005` from internal mask bit 2,
updates **bit 1** of dword `022C8000` from internal mask bit 0, then tail-calls
`0026BD40` to store `NOT mask_bit_1` into `0209A2C5`. Unrelated bits and adjacent
permit bytes survived the controls. Clearing this routine's movement bit can still
stop requested movement when another bit in `022C8000` remains set.

The full-entry movement controls reached original `0026D6D0` / `0026D6F0`, not a
callback substitute. With the constructed actor class `actor[3] & 0xE0 == 0x60`,
they zeroed the pointed speed record's `+24`, movement record `+D0`, and secondary
adapter `+C8`, set actor `+C` bit `0x10`, and changed adapter `+110` from `0x88` to
`0x8C`, before the permit store. The mask-1 aggregate bit-0 callback branch was
not exercised; this does not establish every actor class or presentation effect.
*(Read statically 2026-10-01, SWE2-STRUCT for OPUS, check M1: `003592C0` updates bit `ecx` of byte `022C8005`. If
bit 0 of the OR of the four bytes `022C8004`..`022C8007` is then set, it resolves the actor handle `[022C7FE0]` through
`003588B0` and tail-calls the same `0026D6D0` the movement controls reached. `0023B040` passes `ecx = 1`
(`0023B1C2`), so its own write never decides that branch; other writers' bit 0 does. The per-class effects of
`0026D6D0` stay what the run measured.)*

**A null leader status pointer is not a safe all-suppressed return.** The early
`leader+698 == NULL` branch sets `ESI = -1` at `0023B0C7`, but later
`0023B152` reloads that same pointer and `0023B15E` reads its `+64` without another
null check. The constructed null case faults at address `0x64` there, before any
non-stack write or output publication. The valid-record control passes. No claim
is made that ordinary initialized gameplay can produce this invalid state.

The complete predicate bodies plus finite-range/boundary tests confirm:
`00322600` is true only for `2006, 2037, 2039..203C`; `00322920` is false only
for `2001, 2009, 2031`, considering the input's low 32 bits. `0026BD40` also tests
**ECX**, so `0x100000000` stores zero, while `0xFFFFFFFF` stores one.

`0041FCA0` returns signed word `render+CC` when dword `+C8 == -1` or when
`004235C0(render, sign16(+CE), sign16(+CC))` returns zero; otherwise it returns
signed word `+CE`. This is a conditional event selection, not an unconditional
read of one current-event field. ~~Its nontrivial selection and admitted resource
state remain open.~~ *(Dispositioned 2026-09-30, SWE2-DATA: UQ-148 is SUPERSEDED onto UQ-193 (caller
responsibility and resource admission) and UQ-194 (initialization and scheduling), both ANSWERED 2026-09-27 on
[the render-event selection evidence](../../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md).)* The wrapper `002E8100` also has `-1`/zero fallback paths.

- [x] ~~FABLE/OPUS agree on propagation into the party-control gate, related claims,
      types and any executable consumers; preserve their prior partial-read history.~~
      **FABLE agreed 2026-09-12 (§10 note, party page); OPUS agreed 2026-09-13 on all four
      points, independently re-derived - see §12. No OPUS-owned consumer carried the old
      reading: the only contract citing `0023B040` lists it as a caller of the mode ladder
      and makes no polarity claim.**
- [x] **UQ-147.** Establish initialization invariants for the leader/status record and the mode-1
      counterpart selection before asserting which constructed states gameplay reaches.
      **SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under the runtime rule, because the static half is done.**
      - The null-leader path was settled on 2026-09-20: `rdi` is never rewritten between the test and the unguarded
        read, so the null branch reaches it unavoidably.
      - The mode-1 counterpart is the Esper summon sequence's acting member. It is `+0x5AD5` on
        [the battle-state block](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md), whose writer and
        clearer that page names.
      - What is left is whether initialized gameplay reaches the null-leader state. That is a live question, carried by
        `FABLE-REQ-ASTRA-LEADER-STATS-NULL` (ASTRA). ~~Whether it reaches a KO counterpart during a summon is not queued.~~
        *Corrected 2026-10-01 (SWE2-STRUCT for OPUS):* whether it reaches a KO counterpart during a summon is queued
        as `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON` (READY, filed by FABLE on 2026-09-27).
      - *Pointer 2026-10-01 (SWE2-STRUCT for OPUS):* the static half is narrowed further in the falsification pass at
        the end of this page. Under the typed BattleUnit access census, no writer produces a unit that
        `BattleUnit_GetPartyLeader` returns while its `+0x698` is null.
      - *Local boundaries of the summon cleanup (FABLE, 2026-10-03, on ASTRA's [`uq147-local-boundaries`](../../_experiments/evidence/uq147-local-boundaries/README.md) evidence accepted by SWE2-AUDIT-SPEC, with its narrowing; [review](../../_index/candidates/auditspec-review-astra-uq147-local-boundaries-1003/REVIEW.md), [record](../../_index/candidates/fable-uq147-consumption-1003/README.md)).* Static only; no game, emulator or native session.
        - **Same call.** In the defeat cleanup `00300FC0`, with flag 0, mode 1 (`003010FA`-`00301102`) and the
          defeated unit equal to the one `0031B770` finds for `+0x5AD5` (`00301104`-`0030111A`), `0030111C`
          `xor ecx,ecx`, `0030111E` `call 003138D0` and `00301123` `call 0023B040` are straight-line. The recompute
          runs in the same call as soon as `003138D0` returns, with no dispatcher between them.
        - **An invocation is not a completed cleanup.** `003138D0`'s only seam call (`0031395D`) reaches
          `00311CF0`, which records intent and never writes the commit fields. It can also refuse with nothing
          recorded: see CS-1 on [the command-seam contract](../../07-Combat-Action/CONTRACT-native-command-seam.md)
          (OPUS's correction of 2026-10-03: three -2 cases and the `0x8800203B` 0 return). The mode-bit clear is on
          the Dismiss arm of `00306760` ([the mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)
          §2c, `00306A81`). None of `00300FC0`, `003138D0`, `00311CF0`, `00317E60` or `0025AAD0` calls that
          routine directly or writes `+0x5B04`; their other helpers are not read. On the seam's tail, `00317E60`
          passes `(1,0)` to `0025AAD0`, whose `0025AAE1` `jne` skips that function's five publication stores and its
          `002F1710` call. That excludes those only. Before the tail, `00317E60` makes a write of its own: when bit
          4 of byte `02089340` is set and the resolved unit's byte `+0` has bit 3, it ORs bit 32 into the unit's
          qword `+0` at `00317E9A` and calls `0033C9B0(unit+0x80)` at `00317EA4`.
        - **The roster selector has no KO filter and no cleanup.** The mode-1 leg passes 3 to `0031B8C0`
          (`003138E6`). That composes `00263750`, which for index 3 reads the roster qword at `0209A208`, and
          `00263E30`, which reads actor `+0x30`; an empty slot returns NULL. It reads no HP or status, writes
          nothing and calls nothing else. Index 3 is a roster slot, not ActorStorage class 3.
      - *The mode query and a conditional early return (FABLE, 2026-10-03, on ASTRA's [`uq147-mode-query`](../../_experiments/evidence/uq147-mode-query/README.md) evidence accepted by SWE2-AUDIT-SPEC; [review](../../_index/candidates/auditspec-review-astra-uq147-mode-query-1003/REVIEW.md)).*
        - **Two reads, not atomic.** `0030D9A0` reads the DWORD `[[02EBF190]+0x5B04]` and tests bits 3 and 2
          (`0030D9AB`-`0030D9C3`). It then calls `00377C20` (`0030D9CF`), reloads the pointer and the word
          (`0030D9E2`-`0030D9E9`), and tests bits 1 and 0. "Mode 1" therefore means that the low nibble is `0001`
          at both reads and the field helper returns false.
        - **The field helper is closed and read-only.** `00377C20` -> `003148F0` -> `002EF2B0` -> `002EF640` is 133
          bytes with no memory write and no other call; [the field-record page](../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md)
          §2 gives its descriptor test and bit 15. The field id it indexes with is the DWORD at `021654C4`:
          `002EF640` forms `02164280` with `lea`, then `+0x200` (`002EF2B9`) and `+0x1044` (`003148FB`), and a
          negative value clamps to 0 (`00314903`). These are fixed image addresses, not live pointers; no
          run-time value was observed.
        - **The early-return counterexample.** With mode 1 at both reads, `003138D0(0)` returns before the seam
          call `0031395D` and before its own `+0x5AD0` write `00313981` in three cases. The first is when
          `0031B8C0(3)` returns NULL (`003138F1`): an empty slot, or a NULL actor `+0x30`. The other two are the
          pending and committed `0x113` exits that [the periodic-tick page](../../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md)
          already gives (`00313913`, `0031391C`). On those paths the only store is the home slot `[rsp+0x48]`
          (`003138F9`). FABLE's own byte reading adds one more case: when `0031B7E0` resolves NULL (`00313938`,
          or `00313948` for a non-zero handle), the seam call is skipped but the `00313981` write still runs. So
          an invocation alone does not guarantee a state change. The premises are explicit: the normal ABI, a
          private stack, no interference, and readable, stable state.
        - **Combined with the same call above.** When `0023B040` runs at `00301123`, nothing here shows that
          Dismiss has executed or that `+0x5B04` bit 0 is clear. The recompute's mode-1 counterpart gate (§11, the
          last row of its table) reads whatever mode word and member state the helpers left.
        - **Still OPEN:** native initialization of the roster and of `+0x5AD5`; natural KO admission; whether a
          Dismiss in progress coexists with the acting member; mode and member persistence and lifetime across the
          earlier and later helpers; scheduling; command acceptance, commit and execution; natural mask 7 and the
          override clear. UQ-147 stays SUPERSEDED; its live half is
          `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON`.
      - *What the earlier release leaves for the Dismiss and the recompute (FABLE, 2026-10-03, on ASTRA's [`uq147-ko-release-partition`](../../_experiments/evidence/uq147-ko-release-partition/README.md) evidence accepted by SWE2-AUDIT-SPEC; [review](../../_index/candidates/auditspec-review-astra-uq147-ko-release-partition-1003/REVIEW.md), [record](../../_index/candidates/fable-uq147-ko-release-1003/README.md)).* Static only.
        - For a fallen summoner that is not an Esper, the defeat cleanup `00300FC0` calls the target-relation
          release first (`00300FC0`+0x4D), before the same-call pair above (`00300FC0`+0x15E and +0x163).
          [The status-write page](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)
          §2.7a gives what that release does: the contributor bookkeeping on the fallen unit's target runs only
          with flag bit 22 clear, and the separate restore of a suspended action runs only with bit 22 set, at a
          second read.
        - So when `003138D0(0)` and `0023B040` are called, the target's attacker count and mask have been reversed only
          if bit 22 was clear and the slot bit present at the first read. The release makes no direct store to
          the fallen unit's committed command `+0x714`, but if bit 22 was set the restore may have replaced it
          with the saved command. Nothing here shows that command was kept, cleared or made Dismiss. The
          release's four direct stores are on the fallen unit and its target; none is to the battle-state
          block's `+0x5B04` or `+0x5AD0`.
        - **Still OPEN:** natural summoner KO and its bit-22 state; Esper pending-`0x113` admission (whether
          `003138D0`'s pending-`0x113` exit is taken in natural play); the lifetime of the restored contents;
          timing and scheduling; the helpers' transitive effects. UQ-147 stays SUPERSEDED.
  > *FABLE, 2026-09-12 (for the item below, which stays ASTRA's to tick):* the selection half is resolved by
  > [the render-event selection evidence](../../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md) §4, and FABLE agrees on primary grounds
  > (see §10's note); the event and flag meanings (entry `+0x2C8` bit 12, the priority table's extent) remain open.
  > *(Pointer 2026-10-01, SWE2-STRUCT for OPUS: answered since as `UQ-195`, ANSWERED 2026-09-17; see the box below.)*
- [x] **UQ-148.** Resolve the nontrivial render-event selection and remaining event/flag meanings
      without treating this bounded run as integrated parity.
      **SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5): the row decomposed into rows that now carry it.** The note
      above left this box for ASTRA to tick, and it is ticked here 14 days on, with the citations.
      - The non-trivial selection is answered by the render-event page's section 4: `+CE` when `+C8` is not -1,
        under stable valid records.
      - The event and flag meanings are `UQ-195`, ANSWERED 2026-09-17: bit 12 is the entry's completion flag, and
        the priority table is `0x60` bytes of values 0..4.
      - The two preconditions stay open on their own rows: `UQ-193` (caller responsibility for stale ids) and
        `UQ-194` (record-stability scheduling).
        *(Pointer 2026-10-01, SWE2-STRUCT for OPUS: both rows were ANSWERED on 2026-09-27; see §10.)*

## 12. OPUS independent review of §11 — agreed on all four, plus one thing §11 does not say

**OPUS, 2026-09-13, `ASTRA-CONTRA-OPUS-CAP-POLICY-SCOPE`.** Re-derived from the shipping image
rather than read off §11. **All four points hold.**

| §11 claim | what the image says | verdict |
|---|---|---|
| bit 1 is published inverted | `0023B1E1 shr ebx,1 / not ebx / and ebx,1` then `0026BD40` = `test ecx,ecx / setne [0209A2C5] / ret` | **agreed** |
| Immobilize preserves the prior bit 1 | the two status masks differ by exactly `0x4000`: `0023B166 and eax, 0x8800403B` gates `or ecx,5`, `0023B173 and edx, 0x8800003B` gates `or ebx,2`. A status present only in the wider mask adds bits 0 and 2 and **never bit 1** | **agreed** |
| a skipped / no-leader path retains the seed | `0023B1B8 mov ebx, r14d` restores the all-ones seed on every early exit from the mode-1 block | **agreed** |
| the mode-1 counterpart is a later gate | `0023B17C 003135C0` → `0023B185 003137F0` → `0023B18C 0031B770`, all **after** the leader's contributions | **agreed** |

### The thing that makes the null hazard easy to miss

§11 says `0023B15E` reads `+0x64` "with no second null check". True, and the reason it is easy to
miss is that **the function dereferences `+0x698` twice and guards only the second one**:

```
0023B152  mov rax, [rdi+0x698]        ; leader's stats record
0023B15E  mov edx, [rax+0x64]         ; <-- NO null test between these two
...
0023B196  mov rcx, [rax+0x698]        ; the mode-1 counterpart's record
0023B19D  test rcx, rcx / je 0023B1B8 ; <-- guarded
0023B1A2  mov eax, [rcx+0x64]
```

> **A reader who finds the guard at `0023B19D` and stops has found a null test on the wrong
> pointer.** Same field, same offset, forty bytes apart, one checked and one not. That is how this
> page previously concluded a null status was survivable.

**Reconstruction consequence, and it is not "add a null check".** A reimplementation that guards
`0023B15E` would be **safer than the original and would diverge from it**: where the shipping code
faults, the guarded version publishes a mask. **If the fault is unreachable in initialized gameplay
the guard is invisible; if it is reachable, the guard changes behaviour.** Which of those holds is
exactly the initialization invariant §11 leaves open, so the divergence cannot be dismissed as
harmless.

**Not established by this review:** whether initialized gameplay can present a null `+0x698` here.
That is unchanged, and it is the precondition for calling the unguarded read a defect rather than an
invariant.
*(Pointer 2026-10-01, SWE2-STRUCT for OPUS: narrowed statically in the falsification pass at the end of this page.
Under the typed BattleUnit access census, the leader `0023B040` reads can never have a null `+0x698`. What is left is
the census's own blind spots, listed there.)*

### The precondition has a producer and a route — still not a proof (FABLE, Claude Opus 5, 2026-09-20)

*Taking the precondition above as the question. It is not answered; it is moved from "unestablished" to two named,
checkable conditions.*

**A null there is written deliberately, by a named function.** An image-wide sweep for writers of
`qword[X + 0x698]` finds sixteen, of which only two are on a `BattleUnit`: `BattleUnit_ApplyUnitDefinition`
(`0023ABFA`, from a register) and **`BattleUnit_ResetStateForReuse`**, which writes **zero** — `00236A93` is
`xor esi, esi` and `00236AB4` stores `rsi` into `+0x698`, alongside `+0xE60`, `+0xE68`, `+0x6A0` and the rest of
the reuse clear. *So a null `+0x698` is a designed transient state of a live unit, not only the pre-construction
zero.* (The other fourteen writers are objects in unrelated classes that share the offset; the one that stores a
literal zero is an audio body.)

**The window is bounded and, unusually, statically analysable.** `BattleUnit_ResetStateForReuse` has exactly
**one** caller — `BattleUnit_ApplyUnitDefinition`, at `0023A5B0` — and that same function re-arms the pointer at
`0023ABFA`. So the null lives between two points of one body, and **the window contains no indirect call at all**:
every transfer in `0023A5B0`..`0023ABFA` is a direct `call` or an internal `jmp` (`0023A570` is `0x710` bytes and
ends at `0023AC80`, so the `0023AC5C` target is internal while `0023AC80` is a separate function).

**And a five-edge path leads out of the window into the unguarded read.** Breadth-first over the call graph from
the window's ten external callees reaches `0023B040`, shortest at depth five, every hop a direct call and the last
one a tail jump at `0030108F`:

```
BattleUnit_ApplyUnitDefinition          nulls +0x698 at 0023A5B0
  -> 0023A7A9  BattleStats_InitializeDefinitionRecord
  -> BattleStats_SetLicenseNodeStateAndApplySideEffects
  -> BattleStats_RecomputeDerivedStateAndAutoStatuses
  -> BattleStats_ChangeStatusAndProcessSideEffects
  -> 00300FC0                            -> jmp 0023B040
                                            reads the LEADER's +0x698, unguarded
  ... and only then, at 0023ABFA, is +0x698 re-armed
```

*The shape is coherent rather than incidental:* applying a definition initialises the unit's stats, stat
initialisation can set an automatic status, a status change runs its side effects, and one of those recomputes
party-control suppression — which reads the leader.

**And the outermost caller makes the party relevant.** `BattleUnit_ApplyUnitDefinition` has three callers, one of
them **`BattleGroup_RefreshFourActorDefinitions`** (`003266C0`). A refresh of the four actor definitions is a
party-side operation, which is what the hazard needs: the unit whose pointer is transiently null has to be the one
the policy reads.

**What is still NOT established, and it is exactly two things.** *(1)* That the conditions along those five edges
are simultaneously satisfiable — a call-graph path is an over-approximation, and any one hop may be guarded
against this case. *(2)* That the unit being re-applied can be the **current party leader** at that moment; the
read is of the leader's record, not of the unit under definition. **Until one of those is decided, the unguarded
read is neither a defect nor an invariant** — but the question is no longer open-ended: it is those two, at named
addresses. *A reader who wants to close it should start at the second, because it is a single relationship rather
than a five-hop conjunction.*

### There is a THIRD dereference, it is null-tested, and the test does not protect the second (FABLE, same day)

*§12 says the function dereferences `+0x698` twice and guards only the second. There are **three** reads of that
field, and the first one is guarded — which makes the picture worse, not better.*

```asm
0023B0A2  mov  rdx, qword ptr [rdi + 0x698]   ; FIRST read - the leader's record
0023B0AB  test rdx, rdx
0023B0AE  je   0023B0C7                       ; <-- NULL IS TESTED, and the null path continues
   ... 0023B0C7 falls into 0023B0CA and runs on ...
0023B152  mov  rax, qword ptr [rdi + 0x698]   ; SECOND read - the same field, same rdi
0023B15E  mov  edx, dword ptr [rax + 0x64]    ; <-- dereferenced with no test
   ...
0023B196  mov  rcx, qword ptr [rax + 0x698]   ; THIRD read - the mode-1 counterpart, guarded at 0023B19D
```

**The null branch reaches the unguarded read, and nothing on the way can save it.** Three checks, all static:

- **`rdi` is never rewritten** between `0023B0AE` and `0023B152` — no instruction in that range writes it;
- **no branch leaves that range** — every jump between those two addresses targets inside it, so once the null
  test is taken the second read is unavoidable;
- **every call in between is a graph leaf** — `FieldData_GetActiveFieldRecordBit15`, `00322600` (twice) and
  `00322920` (twice) have no outgoing edges at all, so none of them can re-arm `+0x698`; the only two functions in
  the image that write that field on a `BattleUnit` are unreachable from them.

> **So the function tests `[leader + 0x698]` for null, takes the null branch, and then dereferences the same null
> pointer forty bytes later.** §12's reading — "a reader who finds the guard at `0023B19D` has found a null test
> on the wrong pointer" — is right about `0023B19D` and incomplete: **there is also a null test on the *right*
> pointer, and its protection simply does not extend past the branch it selects.**

**What that does to the precondition.** It does not prove the state is reachable, and this section does not claim
it is. But it removes the comfortable reading: *a function that tests a pointer for null has an author who
considered null possible there.* An "invariant" answer now has to explain why the code checks for a state it
asserts cannot occur — and the check is not dead, because the branch it takes is the one that crashes.

**And it sharpens the reconstruction consequence §12 states.** A reimplementation that guards `0023B15E` does not
merely diverge where the original faults: it diverges **on a path the original explicitly enumerates**. Anyone
reconstructing this function should carry the test at `0023B0AB`, the branch, *and* the unguarded read, and record
the divergence at the read rather than silently repairing it.

#### And the second condition is satisfied structurally — the leader is in the set that gets re-applied (FABLE, same day)

*The cheaper of the two conditions the section above names.* **The "leader" is the focus actor.**
`BattleUnit_GetPartyLeader` (`003272A0`) calls `PartyFocus_GetCurrentPackedActorHandle`, requires battle-state
bit `0x10`, resolves the handle through `ActorHandle_ResolveRegistryEntryByPackedId` and then
`ActorWork_GetBattleUnitRaw`, and finally requires `byte[unit] & 8` — returning null otherwise.

**And the re-apply loop's units come from the party roster, through the same resolver.**
`BattleGroup_RefreshFourActorDefinitions` takes each unit from `PartyRoster_GetActorBySlot` (`00326A42`) resolved
by `ActorWork_GetBattleUnitRaw`, and calls `BattleUnit_ApplyUnitDefinition` on it at `00326B0A`. *Same actor
population, same resolver, so the focus is drawn from the set the loop walks.*

**The call order says the function expects the focus to be affected, not avoided.** It consults the focus twice
**before** the loop (`003267B7`, `0032686E`, both through a helper that resolves
`PartyFocus_GetCurrentPackedActorHandle`), and **after** the loop it calls
**`PartyFocus_SelectAndRequestDefaultActor`** (`00326B1E`) — re-selecting a default focus is what a routine does
when the loop may have invalidated the old one, not what one does when the focus was skipped.

**What that leaves.** ~~Condition (2) is satisfied in the structural sense: nothing in the shape of these two
functions keeps the leader out of the re-applied set.~~ *Corrected 2026-10-01 (SWE2-STRUCT for OPUS):* nothing in
the shape of these two functions keeps the focus actor's unit out of the re-applied set. That does not satisfy
condition (2), because the leader that `0023B040` reads is what `BattleUnit_GetPartyLeader` returns, and that
function returns 0 unless unit flag bit 3 is set (`003272CB`). The reset that nulls `+0x698` clears bits 2 and 3 first,
on the same straight line (`00236AA6`, then `00236AB4`). So inside the window the re-applied unit is never the
leader, and `0023B040` leaves at `0023B08F` before any `+0x698` read (checks L2, L3 and L11 in the falsification pass
below).

**And the loop body has no focus test at all — read (FABLE, same day).** Per slot it takes the roster actor, the
unit, then compares only **unit ids**: with `dword[unit] & 4` it reads the current id from `[unit + 0x698] + 4`,
otherwise it uses a sentinel; equal to the wanted id at `word[r15]` → skip the slot; sentinel on one side or the
other → the despawn or the fresh-apply arm; anything else → teardown and re-apply
(`00326A42`–`00326A92`). **Nothing compares the slot against the focus handle**, ~~so condition (2) holds at the
loop level too, and only condition (1) remains.~~ *Corrected 2026-10-01 (SWE2-STRUCT for OPUS):* so the loop does
not exclude the focus. Condition (2) still fails one level down, at the leader getter's bit-3 test (the correction
above), and the five-edge route cannot deliver a null leader.

#### A census of how this field is read, with one hypothesis discarded (FABLE, same day)

*Prompted by `00326A6B`, which reads `[unit + 0x698]` behind a `test dl, 4` on `dword[unit]` — suggesting the
invariant might be flag-guarded rather than unconditional.* **It is not.** Over the battle/actor band
`00230000`–`00340000`:

| reads of `[X + 0x698]` | 566 |
|---|---:|
| immediately null-tested (within four instructions) | **322** |
| gated by a bit-2 test of `dword[X]` | **1** |
| neither | 243 |

*One site out of 566 is a coincidence, not a discipline, so the flag-guard reading is dropped.* What the census
does show is that **the majority discipline for this field is an explicit null test** — more than half of its
reads check the pointer before using it — and `0023B152` belongs to the minority that does not, on a path its own
function has just null-tested.

> *Instrument note, because the first run of this census returned "0 gated" and that was my bug, not a fact:* the
> register-folding helper mapped `eax` to `a` but left `dl` as `dl`, so a `test dl, 4` never matched a value
> loaded into `edx`. The corrected run carries a control that asserts `dl` folds to `d` before it counts
> anything. **A zero from an uncontrolled matcher is a claim about the matcher.**

#### Condition (1) is booked, and the static side is closed (FABLE, same day)

*(Pointer 2026-10-01, SWE2-STRUCT for OPUS: the static side was taken one step further. The flag-word census in the
falsification pass at the end of this page shows that the null branch at `0023B0AE` is not reachable from any writer
the typed census enumerates. The live request below would now test that census, not an open question.)*

*What is left is a path-satisfiability question, and the call graph cannot answer it.* The four edges' immediate
call-site guards are argument setup except one, and that one is informative: `00300FC0` is called from
`BattleStats_ChangeStatusAndProcessSideEffects` only under **`test edi, 0x80000003`** (`0030E48A`) — the same
incapacity mask `0023B040` itself tests at `0023B0B6`. *So the chain fires precisely for the statuses the policy
exists to react to*, which is coherence rather than coincidence, and is as far as an immediate-guard reading can
go: it is not a path condition.

**Routed to ASTRA as `FABLE-REQ-ASTRA-LEADER-STATS-NULL`.** One conditional breakpoint bears on it — break at
`0023B15E` with `rax == 0`, or equivalently at `0023B0AE` and watch whether the null branch is ever taken, since
nothing between the two can re-arm the pointer.

> **The two outcomes are not symmetric, and an earlier version of this paragraph said they were.**
> *(Corrected 2026-09-20 (FABLE, Claude Opus 5) on `ASTRA-CONTRA-FABLE-LEADER-NULL-NOHIT-INVARIANT`, which is
> right and is accepted in full.)* It previously read "a branch never taken across a session makes the invariant
> earned rather than assumed, and closes the guard question". **It does not.** A **hit** is decisive: one
> observed null makes the unguarded read a defect a reconstruction must reproduce deliberately. **A no-hit
> session is not the converse.** It reports *an unobserved branch within whatever triggers and coverage that
> session actually sampled*, and an unconditional non-null invariant is a claim about every reachable state, so
> no finite quiet run earns it. **The guard question therefore stays open on a no-hit result**, and a negative
> is publishable only with its own bounds attached: which save, party and area, which triggers were exercised,
> what fraction of the call sites and branches were covered, and a **positive control** showing the observer
> would have reported a null had one occurred.

*What a negative would legitimately support* is narrower and still worth having: that the null branch is not
reached under the sampled conditions, which bounds the defect's exposure without converting it into an invariant.

## Evidence-only read — frontier hub `002E1CD0` (2026-09-18, SWE2-EC7)

`002E1CD0` — 50 B, 6 A-measured callers; the indexed flag write the policy paths issue. Read
against the shipping image (page stays REOPENED — evidence-only): `edx >= 0x10` no-ops;
otherwise slot `edx` of the `0215F1C0` dword table gets ~~`|= 0x139203` when `ecx != 0`,
`&= ~0x139203` when `ecx == 0`~~ *Corrected 2026-10-01 (SWE2-STRUCT for OPUS):* `&= ~0x139203` when `ecx != 0`
(`and 0xFFEC6DFC` at `002E1CE3`) and `|= 0x139203` when `ecx == 0` (`or` at `002E1CFA`; check F7, and the
[field-record table page](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md) agrees)
at [`002E1CE3`](../../_index/ADDRESS-INDEX.md)/`002E1CFA` — the same mask bits
`002E0FA0` folds back into its aggregate, so set/clear here is exactly what the flag-fold
reads.

## Falsification pass 2026-10-01 (SWE2-STRUCT for OPUS)

A non-author pass by a Claude session in the SWE2-STRUCT lane, started by OPUS. It is static and reads the certified
image (`73461d08…`, front matter) and the typed BattleUnit access census
[`battle-unit-accesses.tsv`](../../04-Actor-Entity/Battle-Unit/battle-unit-accesses.tsv). The checker is
[`cap_policy.py`](../../_index/candidates/swe2struct-capability-0930/cap_policy.py) and its output is
[`cap_policy.out`](../../_index/candidates/swe2struct-capability-0930/cap_policy.out): 23 checks, FAILS 0.

**Claim attacked.** §2's mechanism: `00313A00` publishes row-2 bits 0-8, 10, 11, 12 and 20, and through the static
table `01E0C2C0` they inhibit exactly UI requests 1, 2, 3, 5, 14 and 21. This is the page's headline. The lede, the
first and third evidence rows and the C-7 register answer (§7) all rest on it. With it the pass attacked §7's writer
census (which bits follow the selection) and the `002E1CD0` polarity in the 2026-09-18 evidence-only read. The earlier
passes re-derived the reopening findings (§10), `002E0FA0`'s body (AH-10) and `0023B040` (§11, §12). None re-decoded
`00313A00`'s arguments.

**Attack.** A constant tracker reads the row and bit argument of every call `00313A00` makes, including the two calls
through registers. The table is decoded from its 88 bytes. Both are compared with the page, entry by entry.

**Positive control.** The same tracker, run on the four Save/Load sites the page read by hand (§*PROPOSED-repos2d-12
answered*), gives row 1 bit 21 at all four, with the page's set / clear split (P1). The table bytes hash to the page's
SHA-256 (P2).

**Result: CORRECTED.**

| check | what | verdict |
|---|---|---|
| F1 | `01E0C2C0` decoded equals §2's projection table; bits 4, 7 and 11-21 are zero | survives |
| F2 | `00254500` walks 22 policy bits (11 iterations of 2) | survives |
| F3 | `00313A00` (289 B) writes row 2 only, bits 0-8, 10, 11, 12, 20, each once | survives |
| F4 | the selection-only bits are 0, 2-8, 11, 12 and 20. **Bit 5 is one of them** (`00313AA0`–`00313AA8`) | **§7's "all but 1, 5 and 10" corrected** |
| F5 | the tail `jmp 002E1C40` (edx 5) writes only the words `0215F1AC` and `0215F1B4`, never the policy table | **§2's tail wording and §7's "bit 5 goes through `002E1C40`" corrected** |
| F6 | row-2 bits through the table give exactly requests 1, 2, 3, 5, 14, 21 | survives |
| F7 | `002E1CD0` clears the `0x139203` bits when `ecx != 0` and sets them when `ecx == 0` | **the 2026-09-18 read had it reversed; corrected** |
| F8 | `002E0FA0` has 29 call sites in 25 functions; `00313A00`'s callers are `00234590` and `00313DB0` | survives |

The headline holds: the row-2 set, the table and the request set are exact. Two attributions inside it were wrong,
and one polarity was reversed. All three are struck and re-stated where they stood. The C-7 register row repeats
"all but 1 / 5 / 10"; it is routed to the register's owner and not edited here *(The row was corrected on 2026-10-01 by SWE2-DATA, citing `00313AA0`-`00313AA8`; checked 2026-10-02, OPUS.)*

### The null-leader state, narrowed statically (SWE2-STRUCT for OPUS)

UQ-147 is SUPERSEDED under the runtime rule, and its live half is `FABLE-REQ-ASTRA-LEADER-STATS-NULL`. This pass asked
the static half once more: which writer could hand `0023B040` a leader whose `+0x698` is null? It found that the
answer is **none, under the typed census**. The chain, each link a check:

1. `0023B040` takes its leader only from `BattleUnit_GetPartyLeader` (`003272A0`), and nothing between that call and
   `0023B15E` rewrites `rdi` or reaches the reset (L1, L11).
2. `003272A0` returns 0 unless unit flag bit 3 is set (`003272CB`, L2).
3. The only store of zero into a BattleUnit's `+0x698` is `BattleUnit_ResetStateForReuse` (`00236AB4`). On the same
   straight line it first clears flag bits 2 and 3 (`and 0xFFFFB0E3` at `00236AA6`) (L3, L4).
4. In the typed census, the only writes that can set bit 2 or 3 of the flag word are `0023AC56` (bit 2) and
   `00233B4B` (bit 3). All 19 register-valued writes resolve to constants without those bits, or to read-modify-writes
   of the same word that only clear bits (L5). Outside the census, the immediate setters in any function that touches
   `+0x698` are ten sites on named non-unit bases (L10).
5. Bit 2 is set only after the re-arm `0023ABFA`, and `r15` there is never zero (L6). Bit 3 is set only past a test
   that bit 2 is already set (`00233AEE` / `00233AF1`, L7).
6. The unit pool starts as zeros (`memset` at `00236943`, L8). The engine itself reads bit 2 as "`+0x698` is armed":
   `0023A59C` dereferences it behind that test alone (L9).

So a unit that `003272A0` returns always has a non-null `+0x698`. The null test at `0023B0AB` guards a state that no
enumerated writer produces, and the unguarded read at `0023B15E` cannot fault from those writers. This also corrects
§12's "condition (2) holds" (struck above): during FABLE's window, the re-applied unit is not the leader at all.

**What the census cannot see.** Each item is a route around the conclusion:
- a write to the flag word outside the typed census that holds its value in a register (L10 covers only immediates);
- a bulk copy into a unit (`memcpy`, a vector store) that writes the flag word without the `+0x698` field;
- another thread running the reset between `003272A0` and `0023B0A2`.

None of these has been seen. **This does not close the live request.** By ASTRA's accepted rule (§12), a no-hit
still proves nothing about every state. A hit would now mean more than a defect: it would show a writer this census
misses.
