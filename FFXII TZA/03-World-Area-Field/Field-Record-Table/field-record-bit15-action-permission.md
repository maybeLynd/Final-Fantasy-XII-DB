---
system: Field record table — bit 15 action-permission override
category: 03-World-Area-Field
status: AUDITED
owner_layer: PrimaryOwner:WorldAreaField (the reader) — consumed engine-wide
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
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 1
---

# Field record table — bit 15 action-permission override

> A per-area flag that decides whether a character carrying certain disabling statuses is
> still allowed to act. Most of the combat layer checks it.

## 1. What the player sees

Normally, a character in certain disabling states simply cannot take actions — the game
refuses the command. **In some areas that rule is waived.**

Whether you are in such an area is not decided by the battle system. It is baked into the
*map's own data*: every field carries a flag saying "in here, those states do not stop you
acting." Walk into a different zone and the same character in the same condition may behave
differently.

This is why it matters to anyone changing zones or battle rules: **an area can silently
change what your party is capable of**, and nothing in the battle code makes that visible.

## 2. Native mechanism

`00377C20` is a zero-argument predicate, 78 bytes:

```c
uint FieldData_GetActiveFieldRecordBit15(void)
{
  uint fieldId = WorldTransition_GetActiveOrPendingFieldId();
  if ((DAT_02add100 != 0) && (fieldId < *(uint *)(DAT_02add100 + 4))) {
    return (uint)*(byte *)(fieldId * 3 + 9 + DAT_02add100) * 0x100 +
           (uint)*(byte *)(fieldId * 3 + 8 + DAT_02add100) >> 0xf;
  }
  return 0;
}
```

1. get the **active-or-pending** field id — pending matters: during a transition it already
   answers for the field being entered (`call 003148F0` at `00377C24`);
2. fail closed if the table is absent or the id is out of range → **return 0** (table load
   `00377C29` → `02ADD100`, bounds check `00377C35`, the `0xFFF >> 15` = 0 fallthrough at
   `00377C5F`–`00377C67`);
3. index a 3-byte record, read the little-endian `u16` at `rec+8` — `byte[rec+9] << 8` at
   `00377C42`/`00377C50` plus `byte[rec+8]` at `00377C4B`/`00377C53`, where
   `rec = table + fieldId*3` (`lea` at `00377C3E`);
4. return bit 15 (`>> 15` at `00377C55`).

### How the combat layer uses it

The dominant pattern across CombatAction, CombatAI and Status callers:

```c
if (((bkbi->statusLayer0 | bkbi->statusLayer1) & 0x80000003) != 0 &&
     FieldData_GetActiveFieldRecordBit15() == 0)
        -> refuse: unit cannot act
```

~~Both effect layers are OR'd~~ Two of the three 32-bit status masks, `+0x3C` and `+0x64`, are OR'd *(answered: see the correction to §2 and §4 below; 2026-10-02, OPUS)* (see the
[two-layer effect model](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)),
masked with `0x80000003` — **bits 0, 1 and 31** — and the restriction applies **only when
bit 15 is clear**. A set bit 15 waives it.

Observed at action-eligibility, action-selection and command-validation sites, sometimes
folded into much larger conditions alongside unit flags `0x10`, lifecycle flags `0x30`/`0x48`
and definition-selector checks.

One structurally different consumer exists around `DAT_01e0c2b4` / `DAT_020927e0`, paired
with a `DAT_02f97360 & 0x200` test — a separate subsystem, not the combat gate.

**Identified 2026-09-02 (C-12).** It is `InputGameplay_ArbitrateDigitalInputAndModalState`
(`00253C70`, Input, 1,599 B), which reaches this predicate **twice — directly at `00254067` and
through the thunk at `00254232`** — and is one of only two functions in the image to use both
routes. The three globals are private to that one function, and the predicate forces a per-press
input toggle off. A second Input-side consumer, `00313A00` (`InputGameplay`, 289 B), calls the
predicate at `00313A34`; the §9 caller census counted it under *unowned*, which is why neither
appeared as an Input relationship. Both are worked through in
[field-record-table-navimapdata.md](field-record-table-navimapdata.md) §11. The function's full
22-member callee family is opened on
[battle-runtime-mode-ladder.md](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)
("The `00253C70` exclusive subtree").

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00377C20` | `FieldData_GetActiveFieldRecordBit15` | 78 B | the predicate — **65 direct callers**, **110 including the thunk** (§9) |
| `00313F60` | **thunk** — `JMP rel32 -> 00377C20` | 5 B | same name in the GFZ; **47 further callers** reach the predicate through it |
| — | `WorldTransition_GetActiveOrPendingFieldId` | — | supplies the field id |
| `DAT_02add100` | field-record table base | — | header + 3-byte records |

### Caller distribution

| Callers | Subsystem |
|---:|---|
| 17 | **CombatAction** |
| 4 | Script/VM Native Bridge · Presentation · Movement (each) |
| 3 | CombatAI · Status/Periodic/Terminal (each) |
| 2 | ActorEntity · Items/Equipment/Shops/License (each) |
| 1 | CombatFormula · Input · Party · Rewards/Progression · WorldAreaField (each) |
| 21 | unowned |

## 4. Data structures

```
Field record table   base = DAT_02add100
  +0x00  u32   (unread by this function)
  +0x04  u32   entryCount          bounds check
  +0x08  ...   records, stride 3 bytes

Record (3 bytes, at base + 8 + fieldId*3)
  +0x00  u16   little-endian flags   bit 15 = action-permission override
  +0x02  u8    (not read here)
```

The odd 3-byte stride is worth noting: only two of the three bytes are touched here, so the
third byte carries something this function does not use.

```
Status mask tested by callers: 0x80000003  -> bits 0, 1, 31
  over (BKBI statusLayer0 | statusLayer1)
```

## 5. Call chain

```
area load / transition   <- corrected 2026-10-02, OPUS: boot, once - the binder 00377CC0 has one caller, 00266D10 (00267146), run once by the boot routine
  -> field record table bound (DAT_02add100)

action eligibility / selection / command validation
  -> BKBI status layers OR'd, masked 0x80000003
     -> if any set:
        -> 00377C20  FieldData_GetActiveFieldRecordBit15
           -> WorldTransition_GetActiveOrPendingFieldId
           -> table lookup, bit 15
              -> 0 : refuse the action
              -> 1 : allow it despite the status
```

**Upstream:** the active-or-pending field id, and the field record table bound ~~at area load~~ once at boot *(corrected 2026-10-02, OPUS: `00377CC0` ← `00266D10` at `00267146` ← the boot routine, one caller each)*.
**Downstream:** action eligibility across CombatAction, CombatAI and Status.

**Do not confuse with:** the gameplay capability/inhibition policy
([capability-inhibition-policy](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md)).
That policy consumes this predicate for its row-2 bit 10, but the two are different
mechanisms — this one is per-field map data, that one is a runtime bitmask.

## 6. Modding notes

- **This is map data, not code.** Changing which areas waive the restriction means editing
  the field record table, not the battle system.
- **It fails closed.** Missing table or an out-of-range field id returns 0 — the restrictive
  answer. Preserve that.
- **"Active-or-pending" is deliberate.** During a transition it already reports for the field
  being entered, so eligibility flips at the right moment. Do not substitute a plain
  "current field" getter.
- **The third record byte is untouched here** — something else reads it. Do not assume the
  record is a bare `u16`.
- **XIIOnline:** this is authoritative shared world state derived from area identity. Every
  client must agree on the active field before action eligibility can be trusted; a client
  that is mid-transition will legitimately answer for a different field. Do not network the
  bit — network the area identity and let each client read its own table.

## 7. What is not known

- [x] ~~Player-facing identity of status bits **0, 1 and 31** in mask `0x80000003`.~~
      **C-9 answered 2026-09-02:** status ids **0 = KO**, **1 = Stone**, **31 = ~~Vanished~~ X-Zone** *(corrected 2026-10-02, OPUS: status 31's name in bank 5 — field-record-table-navimapdata.md, 2026-09-26)*
      (*"has vanished without a trace… cannot be reversed"*). The three states from which a unit
      never returns; all three run defeat cleanup and rewards and share one recovery gate. See
      [field-record-table-navimapdata.md](field-record-table-navimapdata.md) §2d.
- [x] ~~Which fields actually set bit 15 — requires reading the shipped table.~~
      **C-10 answered 2026-09-02:** the table is the shipped `navimapdata.bin`
      (magic `NAV`, 1,154 records); **193 fields set bit 15**, and they are the towns, villages,
      shop interiors, aerodromes, airship interiors and story rooms. Full list in
      [field-record-table-navimapdata.md](field-record-table-navimapdata.md) §4.
- [x] ~~Meaning of the other 15 bits of the record `u16`, and of the third record byte.~~
      **C-11 answered 2026-09-02:** bits 0-11 navigation-map id, 12-13 a save-overridable 2-bit
      selector, 14 area-name display; third byte bit 0 the same safe-area flag for a different
      consumer, bits 4-6 a per-field default focus combatant id. See
      [field-record-table-navimapdata.md](field-record-table-navimapdata.md) §4.
- [x] The `DAT_01e0c2b4` / `DAT_020927e0` consumer at a different call site. *(Marker normalised 2026-09-30 (FABLE, [record](../../_index/candidates/qid-marker-truth-fable-0930/README.md)): C-12 is ANSWERED; the toggle's meaning is answered on the R2 force-fight toggle page.)* **C-12 substantially
      closed 2026-09-02** — it is one input-arbitration function's private modal state, and the
      predicate forces its toggle off; ~~what the toggle *is* remains open and belongs to 15-Input~~ *(answered: the R2 force-fight toggle, as this bullet's 2026-09-30 marker says; 2026-10-02, OPUS)*.
      See [field-record-table-navimapdata.md](field-record-table-navimapdata.md) §11.
- [x] ~~**UQ-82.** Designer name for this flag.~~ **NO ADMISSIBLE SOURCE** (2026-09-14, FABLE; EVIDENCE-STANDARD
  addendum 2026-09-15bk): the behaviour is established above, and the designer's name was never shipped.
  *Signed 2026-09-17 by OPUS (reviewer; FABLE, author), recorded 2026-09-27 (FABLE, Claude Opus 5.5), and relabelled OUT OF EVIDENCE BOUNDARY under FRONTIER's carrier test (27f): the bit is tested in code, so its name is an identifier the unshipped source / `FF12X64.pdb` would carry. The negative covers a named population: the three shipped `navimapdata.bin` copies (no printable run at all), the bit-15 predicate's 112-body direct-caller closure (no string operand), an image-wide vocabulary scan and SWE2-DATA's label tables. The unknown name itself is not searchable by construction. [Record](../../_index/candidates/uq82-uq85-signature/README.md).*

**Correction to §2 and §4, 2026-09-02.** This document describes the masked fields as
*"both effect layers"*. There are in fact **three** 32-bit status masks per combatant —
`+0x38`, `+0x3C` and `+0x64` — selected by a six-way operation mode in
`BattleStats_ChangeStatusAndProcessSideEffects`. The gate ORs `+0x3C` and `+0x64` and **ignores
`+0x38`**, so every expression in this document is still correct as written; the description of
what those two fields are was incomplete. They are also a different structure from the 128-bit
effect layers at `+0x68`/`+0x78`.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Complete mechanism | full decompiled body of `00377C20` (78 B, body SHA `838eebb2…e27ea`, 23 instructions) | 1 |
| Table layout: count at +4, 3-byte records from +8 | index arithmetic `fieldId*3 + 8/+9 + base`, bound `*(base+4)` | 1 |
| Returns bit 15 | `>> 0xf` on the assembled little-endian `u16` | 1 |
| Fails closed | both guard branches return 0 | 1 |
| 65 distinct callers across 13 subsystems | full call-graph join, 90,525 edges | 1 |
| Combat gate semantics | decompiled call sites — the `& 0x80000003` + `== 0` conjunction recurs across CombatAction/CombatAI/Status | 1 |

**How this system was found:** not by reading. `audit_crossrefs.py` flagged it on 2026-09-02
as an `UNACCOUNTED NEIGHBOUR` of the capability-policy document, which had described it in a
single line as "a WorldAreaField field-record policy bit source." The call-graph join showed
17 CombatAction callers and forced a reopen. See `_index/AUDIT-LOG.md`.

**Naming discipline:** `bit15` is kept numeric in the name because no authored/designer name
has been recovered. The *behaviour* is proven; the label is not invented.

## 9. Related

- [`field-record-table-navimapdata.md`](field-record-table-navimapdata.md) — the shipped table
  itself: the file it comes from, all three bytes, the 193 fields that set bit 15, and the
  identity of the three statuses this bit overrides (closes C-9, C-10, C-11)
- [`../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md`](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md) — consumes this for policy bit 10
- [`../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md`](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md) — the two layers OR'd before masking
- [`../../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`](../../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md) — where eligibility is enforced

## 9. Falsification pass 2026-09-02

**Attack chosen, and why this document.** Three other documents now rest on this one — the
[battle runtime mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)
(where bit 15 produces mode 3 and pre-empts mode 2),
[party control suppression](../../11-Party/party-roster-and-control-suppression.md), and the
[accessor-hub census](../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md).
A foundation carrying that much weight is worth attacking before anything built on it.

The specific opening: the pass-9 caller census listed **two different functions both named
`FieldData_GetActiveFieldRecordBit15`** — `00377C20` with 65 callers and `00313F60` with 47. This
document mentions only the first. Either there are two implementations of the engine's most
widely-consulted gameplay predicate, or something was miscounted.

### Resolved: there is one implementation and a thunk

`00313F60` is **five bytes**:

```
00313F60:  E9 BB 3C 06 00        JMP rel32 -> 00377C20
```

It is a **jump thunk to the same function**, which is why the GFZ gives both the same name. There is
one implementation, `00377C20`, 78 bytes, exactly as documented. **No defect** — but the document
did not know the thunk existed, and that matters for the numbers below.

### The predicate's real reach is 110 callers, not 65

| | Distinct callers | Owner subsystems |
|---|---:|---:|
| direct, `00377C20` | 65 | 13 |
| via thunk, `00313F60` | 47 | 11 |
| **called both ways** | **2** | |
| **union** | **110** | **15** |

The two routes are almost disjoint — only **2** functions call both — so the direct-caller list
understates the predicate's reach by nearly half. Two subsystems reach it **only through the
thunk**: **Spawn/Encounter/Lifecycle** and **UI**.

Combined caller distribution by owner:

| Owner | Callers |
|---|---:|
| *(no owner tag)* | 37 |
| Combat Action | 20 |
| Actor/Entity | 10 |
| Combat AI | 8 |
| Movement | 8 |
| Status/Periodic/Terminal | 5 |
| Script VM / Native Bridge | 4 |
| Presentation | 4 |
| Party | 3 |
| Combat Formula, Items/Equipment | 2 each |
| Spawn/Encounter/Lifecycle, World/Area/Field | 2 each |
| Input, UI, Rewards/Progression | 1 each |

**Fifteen subsystems consult one authored per-area bit.** That is the quantitative case for §1's
claim that *"most of the combat layer checks it"* — and it reaches well beyond combat.

### The mode ladder calls the real function, not the thunk

`BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) has exactly one callee, and it is
`00377C20` directly. The mode-3 pre-emption documented in the ladder therefore depends on this exact
function, not on the thunk.

### Confirmed unchanged

- `00377C20` is **78 bytes** — matches.
- **65 direct callers** — matches exactly.
- Bit extraction by `>> 0xF` on an assembled little-endian `u16` — unchanged, tier 1.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Audio — CLIENT, not read.** A 335-byte Audio-filed body reads `WorldTransition_GetActiveOrPendingFieldId`
  (`003148F0`) and the persistent payload base. What it selects is open
  ([field record accessors](../CONTRACT-field-record-accessors.md), crossings).
- **PlatformOnlineAchievements — CLIENT.** The 212-byte achievement-side caller reads the same field id.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE.** A cited function calls a 7-byte core getter.
- **ActorEntity - CLIENT and SERVICE (16 edges).** `0030D9A0`, `00313F60` are also called by bodies filed to ActorEntity: `00300FC0`, `003266C0`, `00233AD0`; `00253C70` reaches bodies filed to ActorEntity: `0025B4C0` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (8 edges).** `00313F60` is also called by bodies filed to combat AI: `00321850`, `00321B00`, `00321D30` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (25 edges).** `0030D9A0`, `00313A00`, `00313F60` are also called by bodies filed to combat action: `002FFCF0`, `00313DB0`, `00319F50` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (2 edges).** `00313F60`, `00377C20` are also called by bodies filed to combat formula: `00384F40`, `00300530` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT (7 edges).** `0030D9A0`, `00313F60`, `00377C20` are also called by bodies filed to Gameplay: `00309A90` (Combat), `003176E0` (Combat), `003257D0` (CombatAction) - shared machinery across the layer boundary, no shared ownership.
- **Input - SERVICE (9 edges).** `00253C70` reaches bodies filed to input: `0017DE10`, `001E0D80`, `001E0F20` - shared machinery across the layer boundary, no shared ownership.
- **InputGameplay - CLIENT (1 edge).** `00377C20` is also called by bodies filed to InputGameplay: `00313A00` (FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT (2 edges).** `00377C20` is also called by bodies filed to items/equipment: `00309FB0`, `0030FD10` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT (14 edges).** `0030D9A0`, `00313F60` are also called by bodies filed to movement: `00309AE0`, `00311F70`, `0031BAC0` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (6 edges).** `0030D9A0`, `00313F60` are also called by bodies filed to party: `00303CC0`, `00303F00`, `00326500` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (7 edges).** `0030D9A0`, `003148F0`, `00377C20` are also called by bodies filed to presentation: `003125E0`, `002B7B80` (UI), `002BAF80` (UI) - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (1 edge).** `00377C20` is also called by bodies filed to rewards/progression: `00312280` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (2 edges).** `003148F0` is also called by bodies filed to save/load/settings: `00583D60`; `003148F0` reaches bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (6 edges).** `003148F0`, `00377C20` are also called by bodies filed to script VM / native bridge: `0033F310`, `00357450`, `00344740` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT (3 edges).** `00313F60`, `003148F0` are also called by bodies filed to spawn/encounter lifecycle: `00234DA0`, `002350C0`, `00233780` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (5 edges).** `00313F60`, `00377C20` are also called by bodies filed to status/periodic terminal: `00320450`, `00329A20`, `0030E360` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - SERVICE (1 edge).** `00253C70` reaches bodies filed to story/event: `0032A8A0` - shared machinery across the layer boundary, no shared ownership.
- **UI - SERVICE (12 edges).** `00253C70` reaches bodies filed to UI: `00254B50`, `0028F970`, `003669D0` - shared machinery across the layer boundary, no shared ownership.
