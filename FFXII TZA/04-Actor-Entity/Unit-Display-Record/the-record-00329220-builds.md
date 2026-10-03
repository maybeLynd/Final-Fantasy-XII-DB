---
system: The party member status view — the 0xC0-byte record 00329220 builds for the UI
category: 04-Actor-Entity
status: AUDITED
owner_layer: PrimaryOwner:ActorEntity — consumed by UI, Input and Presentation
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: 00329220 (1,933 B) read to its ret from the shipping EXE with every RIP target computed by
    a tool; its four thin callers and their ten callers named from the graph; the distance threshold
    read from .rdata
last_reviewed: 2026-09-10
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-unit-display-record-pass-1
  last_pass_kind: falsification
  crossref_clean: true
  reopened_count: 0
---

# The party member status view — the record `00329220` builds for the UI

> Three field maps kept meeting the same unnamed function: it copies the spawn counter, the affinity
> bytes, twelve stats-record fields, the experience, the LP and the equipment into a record of its
> own. Read to its ret, it is **the view the menus and the HUD read a party member through**: one
> 0xC0-byte snapshot per call, built from the stats record, the unit that owns it and the party row,
> with a flag word that says what the screen may do with the member.

## 1. What the player sees

The status screen, the party menu and the HUD name strip: a member's name, level, HP and its cap,
MP and its bars, experience and the points to the next level, LP, the six equipment slots, the
status icons with their countdowns, whether the member is the leader, KO'd, engaged, out of range
or mid-action. Every one of those is a field of this record.

## 2. Native mechanism

### 2.1 Signature and the two thin callers

`00329220(stats /*rcx*/, memberSlot /*edx*/, out /*r8, 0xC0 bytes*/, full /*r9d*/)` returns `out`.
Two wrappers resolve the member first — `0031FE70` (79 B) with `full = 0`, `00320040` (82 B) with
`full = 1` — through `BattleSlotMap_ResolveMappedBattleSlot` (`0031B9F0`): the resolver's **returned slot** `≤ 0x27`
(not the member index — corrected 2026-09-13, §9)
becomes `*(02EBF190) + 8 + index × 0x1C8`, the party stats record ([the stats map](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md));
an out-of-range index passes a null record (`0031FE8C`, `0032005C`), and the builder then fills
only the header. Two more callers, `0031FEC0` (167 B) and `0031FF70` (199 B), reach it too. The
ten callers of the wrappers are UI, Input and Presentation code: `InputGameplay_ArbitrateDigitalInputAndModalState`
(`00253C70`), `00254560`, `00272E10`, `00272E70`, `00273270`, `00273880` (UI), `00283270`,
`002BFD20` (UI), `0035BC50` (UI), `003C3340` (Presentation).

### 2.2 In execution order

| step | site | what |
|---|---|---|
| clear | `0032923A`–`00329261` | `memset(out, 0, 0xC0)`; `+0x88 = 0`; `+0x00 = 0`; `+0x60 = 0xFFFF`; `+0x10 = 0`; a null record returns here (`00329265`) |
| the owning unit | `0032927B`–`003292A7` | scan the unit pool (`BattleUnit_GetSlotCount` `00236850`, `BattleUnit_GetBySlotIndex` `00236820`) for the unit whose `+0x698` is this record → `rsi` (may be null) |
| the focus unit | `003292AF`–`003292DE` | if `02089340` bit 4: `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) → `ActorHandle_ResolveRegistryEntryByPackedId` (`003588B0`) → `ActorWork_GetBattleUnitRaw` (`00263E30`, the unchecked variant of `ActorWork_GetBattleUnit` `0031B760`); kept only if that unit's flag bit 3 is set → `r13` |
| flag bits 10, 11 | `003292E1`–`0032931D` | bit 10 (`0x400`) when the battle-state block's `+0x5B04` bit 0 is set (`003135E0`, `003135E7`–`003135ED`) and `00320890(block.b_5AD5) == memberSlot` (`00313800`, `00313807`–`0031380E`); bit 11 (`0x800`) when block `+0x5B04` bit 1 is set (`00303EE0`) and the position of `block.b_5AA4` in the nine-byte list at block `+0x5A48` equals `memberSlot` (`00327200`, `00327207`–`0032723B`, via the thunk `00304650`) — **two "this member is the currently designated one" tests keyed by two bytes of the battle-state block** (the block is a save-image region: [the save-payload field map](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) §2.2); what the two designations mean is `FJ-1`'s residue |
| flag bit 4 | `00329323`–`00329334` | `0031FDA0(unit)` (106 B): **"unavailable"** — 1 when the unit is null, its flag bit 4 is clear or bit 43 set (`0031FDA8`–`0031FDBA`), a party-type `0x1A` (`0031FDD0`), a spawn-backed unit whose spawn record has flag bit 3 or 6 (`0031FDEB`–`0031FDF5`); otherwise status bit 24 (`0031FDF7`–`0031FE03`) |
| flag bit 14 | `00329337`–`0032937B` | set for a unit with flag bit 4 whose stats kind is not 0 and whose spawn record has flag bit 6, or whose status words carry bit 24 |
| flag bits 16, 17 | `0032937B`–`003293AF` | bit 16: `003879C0(stats)` (140 B) — for an owner whose stats record `[+0x698]` has kind byte `+5 == 1` and whose `+0xE68` is non-null, **bit 7 of byte `+0x12` of the unit's `.ard` slot-0 class row `[+0xE68]`** (`003879EB`–`003879F9`, `00387A1B`–`00387A2C`; ~~a `+0xE68` page~~ corrected 2026-09-13 — `+0xE68` is the class row, not a stats page), storing the owner in `02EBF188` on the way (`003879D3`); bit 17: `0030C2C0(unit)` (54 B) — **unit flag bit 52** (`0030C2E7`–`0030C2ED`, the high dword's bit 20), after `002FEAD0(unit)` when `003278C0()` is 0 |
| **HP block** | `003293AF`–`00329400` | `+0x20 = HP (+0x48)`; `+0x24 = effective max` — status bit 16 (frozen) → `max(HP, 1)`, else `+0x24`; `+0x28 = cap` — frozen → `max(HP, 1)`, else `+0x24` doubled on status bit 28 ([the HP write](../../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)) |
| **MP block** | `00329403`–`00329438` | `+0x2C = MP (s16 +0x4C)`; `+0x30 = capacity (+0x28)`; `+0x34 = layers clear ? +0x28 : 0`; `+0x38 = the secondary resource (+0x06)` ([where MP comes from](../../10-Status-Periodic-Terminal/where-mp-comes-from.md)) |
| charges, bars | `00329441`–`00329451` | `+0x86 = +0x4E`; `+0x87 = +0x37` |
| **status words** | `00329457`–`00329469` | `+0x44 = presence (+0x64 \| +0x3C)`; `+0x48 = +0x3C` |
| type, kind | `0032946C`–`0032947A` | `+0x60 = +4` (u16), `+0x62 = +5` (u16) |
| **the merged layer** | `00329480`–`003294B3` | `+0x4C`–`+0x5B` = byte-wise OR of the mutable layer `+0x68` and the derived layer `+0x78` ([the two-layer model](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) |
| affinity | `003294B5`–`003294ED` | `+0x89`–`+0x8D = +0x40`–`+0x44` ([the five bytes](../../08-Combat-Formula/elemental-affinity-and-the-five-bytes.md)) |
| **per-status countdown bytes** | `00329500`–`00329539` | for `s < 32`: `+0x66 + s = (present(s) && s ∈ {2, 6}) ? (+0xBC[s] − 1) : 0xFE` — the per-status parameter word of statuses 2 and 6 becomes a display countdown; every other status shows `0xFE` |
| **party only: the name** | `0032953B`–`003295EE` | kind 0: the party row (`02EBF130` by `+0x60`), its word `+0x30` split 5 : 11 through the text banks at `02EBF170`, `002B58B0(block, 0)` → `+0x10` — the same resolution the installer uses for unit `+0x18` ([the unit-definition page](../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.7) |
| party only: three words | `003295F2`–`0032965C` | `0030A310(row, i)` for `i = 0..2` → `+0xB4`, `+0xB6`, `+0xB8` — **the party row's bytes `+4`, `+5`, `+6`** (`0030A31A`–`0030A322`; `0xFFFF` for a null row or `i > 2`), widened to words |
| party only: bits 1, 2 | `00329660`–`00329691` | bit 1 when type `∈ 7..0x19`, bit 2 when type `∈ 0x1B..0x27` (the party-type band [the kind-byte page](../Battle-Record-Kind/battle-record-kind-byte.md) measures) |
| bit 7 | `00329694`–`003296A1` | `= stats +0x00 bit 2` |
| **`full` only** | `003296A3`–`00329740` | `+0xBA = level (+0x1C2)`; `+0x90 = experience (+0x18C)`; `+0x94 = 002F8F20(level) − experience` — **the points to the next level**, from the curve ([the unit-definition page](../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §4); `+0xB0 = LP (+0x190)`; `+0xBB = BattleStats_CountLicenseBits00To17(stats)` (`00324020`); `+0x98`–`+0xAC` = **the five equipment words `+0x50`..`+0x58` and, at `+0xAC`, the stats record's `+0x5A`**, each `<< 16`. `+0x5A` is **not a sixth slot**: it is `saved[0]` of the five-word takeaway backup — see [the equipment-slots page](../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md) §11 (corrected 2026-09-20) |
| actor handle | `00329746`–`00329760` | `+0x04 = ActorHandle_EncodeRegistryEntry(PartyRoster_GetActorBySlot(memberSlot))` (`00263750`, `003589B0`), 0 if none |
| **unit only** | `00329763`–`0032998A` | `r14 = unit +0x708` (action context), `bp = +0x714` (action id), `r15 = +0x710` (target focus); bit 0 = "no terminal status" (cleared when the words carry KO / Stone / Vanished and `00313F60` agrees); bit 6 = unit flag bit 1; bit 8 = unit flag bit 24, or the action id `> 0x21E`, or phase `+0x6B4 ≥ 9`; bit 9 = unit flag bit 23; bit 12 = id `≤ 0x21E` and phase `≥ 9`; bit 13 = id `≤ 0x21E` and phase `≥ 3`; bit 15 = **idle** (no context, id `0xFFFF`, or phase 0); bit 3 = the squared XZ distance to the focus unit (`Vector3_ComputeSquaredXZDistance` `003A1960` on the two `+0xE0` positions) is `≥ 400.0` (`00915A08`) — **"out of range"**; `+0x10 = the empty string at 01CEB638` (overwriting the party name when a unit owns the record); `+0x88 = spawn record +0x12` (the spawn counter); `+0x04 = unit +8` (actor handle); `+0x1C = unit +0x68`; `+0x18 = unit +0x64`; ~~`+0x64 = page +0x52 of unit +0xE68`~~ `+0x64 = class row +0x52 of unit +0xE68` *(answered: `+0xE68` is the class row, corrected 2026-09-13 above; 2026-10-02, OPUS)* for a kind-1 unit whose actor class is not 3 (`ActorRuntime_GetClassNibble` `00263C20`), else `0xFFFF`; while an action is in progress: `+0x3C = unit +0x768`, `+0x40 = +0x76C`, `+0x5C = the action id` (or `BattleRuntime_GetEffectiveActionId(stats)` `00387090` when phase `≥ 9`), `+0x08 = the focus handle`; otherwise `+0x3C = 0`, `+0x5C = 0xFFFF`, `+0x08 = 0`; `+0x5E = unit +0xBA0` when unit flag bit 14 |

### 2.3 The record

```
StatusView (0xC0), built per call
  +0x00 u32  flags   b0 alive  b1 party-type 7..0x19  b2 party-type 0x1B..0x27  b3 out of range (>= 400.0 XZ from the focus unit)
                     b4 0031FDA0(unit)  b6 unit flag 1  b7 stats+0 bit 2  b8 unit flag 24 | id>0x21E | phase>=9  b9 unit flag 23
                     b10 selected by 00313800  b11 selected by 00327200  b12 id<=0x21E & phase>=9  b13 id<=0x21E & phase>=3
                     b14 spawn flag 6 | status 24 (kind 1)  b15 idle  b16 003879C0(stats)  b17 0030C2C0(unit)
  +0x04 u32  actor handle           +0x08 u32 target focus handle        +0x10 ptr name (party row text; "" when a unit owns it)
  +0x18 u32  unit+0x64              +0x1C u32 unit+0x68                  +0x20 HP  +0x24 effective max  +0x28 cap
  +0x2C MP   +0x30 capacity  +0x34 capacity or 0  +0x38 secondary resource   +0x3C/+0x40 unit+0x768/+0x76C while acting
  +0x44 presence  +0x48 status word 2   +0x4C u8[16] merged layers   +0x5C u16 action id   +0x5E u16 unit+0xBA0
  +0x60 u16 type  +0x62 u16 kind  +0x64 u16 page+0x52 (kind 1)   +0x66 u8[32] per-status countdown (0xFE = n/a)   <- corrected 2026-10-02, OPUS - +0xE68 is the .ard class row, not a page (corrected 2026-09-13 above; 003298EA-0032990D)
  +0x86 charges  +0x87 bars  +0x88 spawn counter  +0x89 u8[5] affinity
  +0x90 experience  +0x94 to next level  +0x98..+0xA8 five equipment words << 16
  +0xAC stats +0x5A << 16 = saved[0] of the takeaway backup, NOT a sixth slot   +0xB0 LP
  +0xB4/+0xB6/+0xB8 three party-row words  +0xBA level  +0xBB licence bits 0..17 count
```

## 3. Key addresses

| address | size | what |
|---|---:|---|
| `00329220` | 1,933 B | the builder |
| `0031FE70`, `00320040` | 79 / 82 B | the wrappers (`full` = 0 / 1) through `BattleSlotMap_ResolveMappedBattleSlot` (`0031B9F0`) |
| `0031FEC0`, `0031FF70` | 167 / 199 B | two more callers, ~~unread~~ actor-to-slot wrappers *(answered: see the 2026-09-12 half answer below; 2026-10-02, OPUS)* |
| `002F8F20` | 122 B | the experience curve — `+0x94` is `curve(level) − experience` |
| `003A1960` | 31 B | `Vector3_ComputeSquaredXZDistance`; threshold `400.0` at `00915A08` |
| `00387090` | 149 B | `BattleRuntime_GetEffectiveActionId` — the displayed action id once phase `≥ 9` |
| `003135E0`, `00313800`, `00303EE0`, `00327200` | 17 / 19 / 19 / 60 B | the two designation tests behind bits 10 / 11 — battle-state block `+0x5B04` bits 0 / 1, bytes `+0x5AD5` (through `00320890`) and `+0x5AA4` (position in the nine-byte list at `+0x5A48`) |
| `0031FDA0` | 106 B | the "unavailable" predicate behind bit 4 |
| `003879C0`, `0030C2C0` | 140 / 54 B | bit 16 (class row `[+0xE68]` `+0x12` bit 7, spawn-backed owners only; stores the owner in `02EBF188`) and bit 17 (unit flag bit 52) |
| `0030A310` | 25 B | party row byte `+4 + i`, `i < 3` |

## 4. Data structures and formulas

- `+0x94 = Σ_{k=2}^{level+1} trunc(float32(k³) × 0.4f + float32(12k²)) − experience` — the curve
  called with `level` sums to the threshold of `level + 1`. *Corrected 2026-09-29 (FABLE, Claude Opus 5.5): the linear term was
  written ~~`k(12k − 2)`~~; the executed curve is `12k²` (level 2 = 51, not 47), [`exp-curve-fable`](../../_index/candidates/exp-curve-fable/README.md) `curve.py`.*
- `+0x66 + s`: `0xFE` unless status `s` is present and `s ∈ {2, 6}`, in which case `+0xBC[s] − 1`.
- bit 3: `dist²_xz(unit +0xE0, focus +0xE0) ≥ 400.0` — twenty units from the focused character.

## 5. Call chain

```
UI / Input / Presentation (00253C70, 00254560, 00272E10, 00272E70, 00273270, 00273880, 00283270, 002BFD20, 0035BC50, 003C3340)
  -> 0031FE70 (full 0) / 00320040 (full 1) -> BattleSlotMap_ResolveMappedBattleSlot 0031B9F0 -> stats = *(02EBF190)+8+i*0x1C8
       -> 00329220(stats, member, out, full)
            -> unit pool scan (+0x698 == stats) ; party focus (003590D0 -> 003588B0 -> 00263E30)
            -> stats fields ; party row name (02EBF130 +0x30 -> 02EBF170 -> 002B58B0) ; curve 002F8F20
            -> unit +0x708/+0x710/+0x714/+0x6B4/+0x768/+0x76C/+0xBA0 ; spawn record +0x12 ; page +0x52   <- corrected 2026-10-02, OPUS - class row +0x52 of [unit+0xE68], not a page
```

## 6. Modding notes

- **The screen never reads the stats record directly**; it reads this snapshot. A mod that changes a
  displayed value without changing the record's source field is undone on the next build.
- **"Out of range" on the HUD is a 20-unit XZ circle around the focused character** (`400.0` squared).
- **The countdown bytes show only statuses 2 and 6**; every other status displays as `0xFE`.

## 7. What is not known

- [x] ~~**What the flag predicates test** — `003135E0` / `00313800` (bit 10), `00303EE0` / `00327200`
  (bit 11), `0031FDA0` (bit 4), `003879C0` (bit 16), `0030C2C0` (bit 17).~~ **FJ-1** — ANSWERED
  2026-09-10 at the byte level (§2.2): bits 10 / 11 are two designations keyed by the battle-state
  block's `+0x5B04` bits 0 / 1 and its bytes `+0x5AD5` / `+0x5AA4`; bit 4 is "unavailable"; bit 16
  is the `.ard` slot-0 class row's `+0x12` bit 7 (~~the stats page's~~, corrected 2026-09-13); bit 17 is unit flag bit 52. What the two designations and the
  two bits *mean* stays open with them.
- [x] **FJ-2.** **What `+0x64` (page `+0x52`) and `+0x5E` (unit `+0xBA0`) are**, ~~and what the battle-state
  block's `+0x5B04` bits 0 / 1, `+0x5AD5`, `+0x5AA4` and the nine-byte list at `+0x5A48` designate~~
  (the block's bytes are named 2026-09-11: `+0x5A48` the nine party selectors, `+0x5AA4` the party
  leader, `+0x5AD5` the special-presentation sequence's actor, `+0x5B04` bits 0 / 1 the UI and
  combat / audio modes — bit 10 = the sequence's actor in the UI mode, bit 11 = the leader in the
  combat / audio mode; [the block page](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)
  §2.4; the three party-row bytes `+4`–`+6` behind `+0xB4`–`+0xB8` are located but not named). **FJ-2.**
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5).** Control: `_index/candidates/fj2-display-fields/fj2_fields.py` (3 checks).
  - **`+0x64` is the enemy's Clan Primer entry id.** For a kind-1 record whose class nibble is not 3, the builder
    stores word `+0x52` of the unit's `.ard` class row `[unit + 0xE68]` (`003298EA`–`0032990D`). The unit-definition
    page names that word the Clan Primer entry id.
  - **`+0x5E` is the unit's issued command action id.** While unit flag bit 14 is set, the builder copies
    `issuedCommandActionId` (`+0xBA0`, the battle-unit field map) at `00329983`.
  - Both fields default to `0xFFFF` (`00329850`).
  - *An observation from the authored `chr_data`, beyond the row's residue.* The six main characters' party-row
    bytes `+4`–`+6` hold three consecutive action ids in `0xD0`–`0xE1`, the eighteen Quickenings: row 0 has Red
    Spiral, White Whorl and Pyroclasm. The names come from the recipe table's action-name join. The thirteen Esper
    rows hold a pair in `0xA0`–`0xB9` plus their own index 1–13 in `+6`. What that pair indexes is not identified: as
    action ids they would name Technicks, which does not fit.
- [x] ~~**Why the name pointer is overwritten with the empty string when a unit owns the record**
  (`003298A6`–`003298AD`), and where the consumers get a unit's display name from instead.~~ **FJ-3**
  — answered 2026-09-11 for the second half: a unit's display name never comes from this record.
  The actor side resolves it with `00263990(actor)` (the `+0x102` script name id through
  `0032A930` / `003EAC10`, else the `+0xF8` definition text), and the stats side with `00536310`
  (party row `+0x30`, actor `+0x102`, or enemy row `+8`, then `00536280` through the text banks at
  `02EBF170`) — the battle log's route ([the post-result events page](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md)
  §2.5). Why this builder blanks its own pointer stays unread; it is consistent with the
  consumers not needing it.
  **NO ADMISSIBLE SOURCE, reviewed and signed 2026-09-27 (OPUS, reviewer; FABLE, author)** for the first half. The
  builder's write set to `+0x10` is complete (three stores and the entry `memset`), and `+0x10` has no reader in the
  shipped executable for any record (OPUS's census, C1–C5 with a positive control). What remains is the programmer's
  reason, which no shipped artefact records. [Package 4](../../_index/candidates/nas-package-4-2026-09-27/README.md),
  [OPUS's review](../../_index/candidates/nas-package-4-2026-09-27/opus-review.md).
- [x] **FJ-4 ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5)** (UQ-98 is its duplicate).
  Which code reads which field of the nine menu copies is a census:
  - the party panel reads HP, MP, status, charges, bars, level and LP;
  - the save/load screen reads charges, bars and level;
  - the license board reads bars, the licence count, experience and LP;
  - the shop row emitter reads the equipment words.
  [Record](../../_index/candidates/fj4-display-record-readers/README.md). *Earlier state, kept:*
- ~~**What the two unread callers `0031FEC0` / `0031FF70` add**~~, and which of the ten UI callers
  draws which field. **FJ-4.** *Half answered 2026-09-12 (FABLE):* both are **actor-to-slot
  wrappers** for the builder. `0031FEC0(?, actor, out)` takes the actor's battle unit
  (`ActorWork_GetBattleUnitRaw`), its stats byte `+4`, finds that id among the party block's four
  slot words `[02EBF190] + 0x5A5A` (stride 2, `0031FF10`–`0031FF22`; `−1` when absent or the id is
  `0xFF`) and tail-calls `00329220(stats, slot, out, 1)`; `0031FF70(?, packedHandle, out)` does the
  same from a packed actor handle (`ActorHandle_ResolveRegistryEntryByPackedId`), both lookups
  gated on `02089340` bit 4. So the member index the ten wrappers pass is, here, the **party slot
  0–3 of a live actor**, and `full` is always 1. Which UI caller draws which field is still open.
  *Narrowed further 2026-09-14 (FABLE):* the ten callers of the wrappers were read around their calls. **Most
  of them do not draw at all.**

  | caller | via | what it reads from the record |
  |---|---|---|
  | `00253C70`, `00254560` | `00320040` over slots 0–8 | type `+0x60 ≥ 0` and flag bit 1 clear, counting to 2 (`0025408C`–`002540A1`, `0025468C`–`002546A2`): **"at least two such members"** |
  | `00272E10` | `0031FF70` | the actor handle `+0x04`, compared with its argument (`00272E55`) |
  | `00272E70` | `00320040` over slots 8…0 | the type `+0x60`, matched against its argument (`00272EA4`) |
  | `00273270` | `0031FF70` | `+0xAC` returned `>> 16` — **the stashed slot-0 item** (stats `+0x5A`), not a sixth equipment slot (`002732B5`–`002732BC`); its five callers are battle-menu bodies, and `0027C3D0` compares it with the selected entry's id |
  | `00273880` | `0031FE70` over slots 0–3 | the actor handle `+0x04`: **"is this actor in party slots 0–3"** (`002738C7`) |
  | `00283270` | `00320040` over slots 0–8 | **keeps nine copies** at `[0209AC30] + 0x408 + i × 0xC0` (to `+0xAC8`, `0028342C`–`00283436`) and reads the type `+0x60` (`00283370`) |
  | `0035BC50` | `00320040` | keeps copies in a stack table; reads type `+0x60`, handle `+0x04` and flag bits 1, 2 and 6, and writes the flags back (`0035BDB0`–`0035BFD0`) |
  | `002BFD20` | `0031FEC0` | **copies it into its widget at `+0xC0`** and reads layer byte `+0x51` bit 1, the presence word `+0x44`, affinity `+0x89` and level `+0xBA` through the widget (`002BFF80`–`002C0293`) |
  | `003C3340` | `0031FF70` | builds it at `[rsp+0x30]` and reads none of it in its own body |

  So the drawn fields are read from the **copies**: the nine-record table in the `0209AC30` object, the stack
  table of `0035BC50`, and `002BFD20`'s widget. Which drawer reads which offset of the `0209AC30` table is what
  remains.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| Every field copied, with source and condition | `0032923A`–`0032998A`, read to the ret | 1 | PROVEN |
| The wrappers' member resolution | `0031FE7F`–`0031FEBA`, `0032004F`–`0032008D` | 1 | PROVEN |
| The 400.0 threshold | `00915A08`, read from `.rdata` | 1 | PROVEN |
| The callers are UI / Input / Presentation | the graph's edges and owners | 1 | PROVEN |
| What the predicates and the three party-row words are | ~~**not established**~~ *(answered: FJ-1 and the 2026-09-26 answer above; 2026-10-02, OPUS)* | — | UNKNOWN |

## 9. Related

- [`../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md`](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) — the source record.
- [`../Battle-Unit/the-battle-unit-field-map.md`](../Battle-Unit/the-battle-unit-field-map.md) — the unit fields read.
- [`../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md`](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) — the spawn counter copied to `+0x88`.
- [`../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md`](../Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) — the name resolution and the experience curve.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py --addr 00329220 --addr 0031B9F0` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment: `0031B9F0` is
already held by [the five parallel slot maps](../../11-Party/the-five-parallel-slot-maps.md), which
this pass does not repeat.)*

Every stated extent is exact — `00329220` **1,933 B**, `0031FE70` **79 B**, `00320040` **82 B** —
and `0031B9F0` is **200 B**. The record arithmetic reproduces instruction for instruction:

```asm
0031FE93  imul rcx, rax, 0x1c8
0031FE9A  mov  rax, qword ptr [02EBF190]
0031FEA1  add  rax, 8
0031FEA5  add  rcx, rax          ; *(02EBF190) + 8 + slot * 0x1C8
0031FE8C  xor  ecx, ecx          ; out of range -> a null record, as stated
0031FEA8  xor  r9d, r9d          ; full = 0 for this wrapper, as stated
```

### ⚠ The `0x27` bound is on the resolver's **output**, not on the member index

§2.1 reads *"a member index `≤ 0x27` becomes `*(02EBF190) + 8 + index × 0x1C8`."* The test is two
instructions **after** the call, and it is on `al` — what the resolver **returned**:

```asm
0031FE83  call 0x31b9f0     ; returns a MAPPED SLOT in al
0031FE88  cmp  al, 0x27     ; the bound is on the RESULT
0031FE8A  jbe  0x31fe90
```

**The member index is bounded separately, and far more tightly.** `0031B9F0` opens by validating it:

```asm
0031BA04  lea  ecx, [r8 + 0x17]   ; class 23
0031BA08  call 0x322c50           ; BattleEncodedId_IsValidForClass(23, index)
0031BA0F  jne  0x31ba1e           ; valid -> pick a map
0031BA11  mov  al, 0xff           ; invalid -> 0xFF
```

and **class 23's arm is the literal bound of 9**
([the class registry](../../00-Engine-Core-Runtime/the-encoded-id-class-registry.md) §4), so the
accepted member indices are **`0`–`8`** — nine, the party configuration's own count — not `0`–`0x27`.

> **The two bounds chain through a sentinel.** An index of 9 or more returns **`0xFF`**, and
> `0xFF > 0x27`, so the second test rejects it and the null record results anyway. That is *why* the
> outer test appears to bound the index: it catches the inner failure as a side effect. **But they
> are different numbers on different quantities**, and a reconstruction that admitted indices up to
> `0x27` would index a nine-entry map with forty values.

`0x27` = **39** is the ceiling on the *slot* a map may name, which is the party-stats array's bound,
not the caller's.

**Not claimed:** `00329220`'s 1,933 bytes were **not** re-read — the field map, the flag word, the
twelve stats fields and the distance threshold are untouched. The five maps themselves belong to
[the five parallel slot maps](../../11-Party/the-five-parallel-slot-maps.md). Nothing was executed or
observed live.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `002C7660` | 1190 | ~~display-record channel evaluation~~ the per-unit overhead-display evaluation, which neither builds nor reads this page's 0xC0 record (SD-128, 2026-09-30, FABLE, [record](../../_index/candidates/sd125-sd128-fable-0930/README.md)) (caller `002C62B0`): `[rcx+0x1D78]` context, `0035D4F0` getter, `00272DE0` (`003588B0`+`002E7E90`), `00263C20` x2, `002ED0B0`, `0037C8F0`, `0035BAD0` x2, `00273460`, then workbench `00202C90` x4/`00203080` — calls `002C7B10`. Interior verified 2026-09-17 (SWE2-FRONTIER): `00272DE0` first at [`002C76C4`](../../_index/ADDRESS-INDEX.md). Its callee `002C7B10` reads the same day: 1,146 B — `0035D470` ×3 + workbench `00202C90` ×3 + `00271AB0` ×2, first call [`002C7B6C`](../../_index/ADDRESS-INDEX.md) |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE.** A cited function calls a 7-byte core getter.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT (16 edges through 11 of this page's functions).** The Gameplay layer reaches this page at `00263E30`, `0031B760`, `00313F60`, `00203080` and 7 more. `WorldActor_QueryCombatStanceState` is the worked example, read in full - it is a 96-byte query that takes the actor from `0031B760`, needs bit 4 of `byte[actor]`, and tests the `+0x698` block's `+0x3C` OR `+0x64` pair; **5 of the 12 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — CLIENT.** `FUN_00316930`, owned by that layer, calls `00283270` on this page. That caller is a 287-byte walk of the same `[022C2550]` table against the data at `01EED130`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `002F8F20` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Story_Event_Quest_Hunt — SERVICE.** `00263990` on this page calls `PersistentFlag_QueryBank2048`, owned by that layer. What it reaches is the 2,048-bit bank query, and it states its own range: an id at or above **`0x800`** or below zero answers false without touching the bank; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — MECHANICAL (SWE2-CONTRACT 2026-09-15, 71 edges).** All 71 edges are Movement bodies calling the shared
accessors this page cites: `00326D60`, `PartyFollow_SolveFormation`, `0033C310`,
`BattleLocomotion_BuildSolverContext`, `BattleLocomotion_ResolveTargetSpacingAndAvoidance`,
`BattleLocomotion_QueryDynamicActorObstruction` and ~45 more `0032/0033xxxx` locomotion bodies all
reach `00203080`, `00236820`, `00236850`, `00263C20`, `00263E30`, `00313F60` or `003590D0`. The
display record shares the actor/context getters the whole movement layer uses — pure fan-in.

**CombatAI — MECHANICAL (SWE2-CONTRACT 2026-09-15, 21 edges).** Same shape: `BattleUnit_RebuildPerceptionCandidateCache`,
`AiOrder_EvaluateTargetSelector`, `BattlePerception_RefreshCandidateCacheGeneration`,
`BattleEnmity_*` and the `AiOrder_*` selectors share `00236820`/`00236850`/`00263E30`/`00313F60`/
`0031B760`; `00283270` calls `GambitConfig_CopyBasePairSetForStatsIndex`. Shared-accessor fan-in.



**Presentation — CLIENT and SERVICE (SWE2-EC7-156, 185 edges).** `00181350` calls `001B06D0` and is called by `0022FFE0`/`00274CB0`/`003C7xxx` of that layer — a two-way render-helper exchange, not a second owner.
**Resource — SERVICE (SWE2-EC7-156, 2 edges).** `002915C0`/`002917E0` call `0024A5A0` of that layer — the record's helpers consume a resource-side helper, not a shared responsibility.
**UI — CLIENT (SWE2-EC7-156, 242 edges).** `002A0440` calls `00181560`, `002915C0`/`002917E0`/`002C7660` call `00202C90`; batch-121's `00272F80` helpers `00273410`/`00275E40`/`003178C0` join the same fan-in — the interface layer consults this page's functions, not a shared responsibility.

**Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-175, 15 edges).** `003588B0` and `00263B80`, helpers this page's `002C8820` calls, are reached by `00341CB0`/`00345800`/`00346FA0`/`0034C3D0`/`0034C950`/`0034F800`/`0034FF00`/`00350DD0`/`003516E0`/`00352580`/`003530F0`/`00355830`/`00356570`/`0050E060` and `0034FCC0` of that layer — script-VM bodies share the same object-resolve and field helpers; pure fan-in, not a shared responsibility.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

*This page's subjects are the view builder `00329220`, its wrappers and callers, and the accessors it reads. Most edges below are other layers calling those same accessors. The view is read-only over its sources: it copies them into a 0xC0-byte record and writes nothing back to any layer.*

**Audio — CLIENT and SERVICE (4 edges).** `00362850` (1,036 B, Audio, not read here) reads the focus getter `PartyFocus_GetCurrentPackedActorHandle` `003590D0` and calls the four-float subtract helper `00203080`, which writes `a − b` component-wise. `00229AF0` reads the capability aggregate `002E0FA0`, as the input contract's §11 records. The channel body `002C0400` calls `00225580`, a 4-byte store to `+0x18` that is filed to Audio. Audio shares the focus getter, a vector helper and the capability aggregate with this page's callers. The only audio-filed callee is a single field store, and no audio state enters the view.

**Combat — CLIENT (1 edge).** `003206E0`, the `(handle, 0, 100)` HP clamp, reads `ActorWork_GetBattleUnitRaw` `00263E30`, the unchecked unit getter that the builder uses for the focus unit. It is a consumer of the same getter and has nothing to do with the view.

**CombatFormula — CLIENT and SERVICE (13 edges).** `BattleStats_FindOwningBattleUnit` `0031B860` and `BattleStats_GetOwningActorHandle` `0031E800` walk the unit pool through `BattleUnit_GetSlotCount` `00236850` and `BattleUnit_GetBySlotIndex` `00236820`. That is the same owner scan the builder inlines at `0032927B`. `00384F40` also calls `00236850` and `00313F60`, `BattleStats_ResolveByActorHandle` `00320A70` reads `00263E30`, and `BattleStats_GetByMappedBattleSlot` `00320AB0` resolves through `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` exactly as the two wrappers do. In the service direction, the builder calls `BattleRuntime_GetEffectiveActionId` `00387090`. `00387090`, the bit-16 helper `003879C0` and `00536310` all resolve owners through `0031B860`, and `BattleStats_ModifyHPAndProcessLethalState` `00300530` calls the predicate `00377C20`. The formula layer owns the stats-side resolvers and the effective action id that the view copies, and its own owner scans use the same pool accessors.

**Input and InputGameplay — CLIENT and SERVICE (17 edges).** `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70`, one of the ten callers of the view wrappers, calls the full-view wrapper `00320040` and the page's accessors `002E0FA0`, `003135E0`, `00313F60` and `00377C20`. It also calls seven input bodies: `0017DE10`, `001E0D80`, `001E0F20`, `InputGameplay_TestFilteredMask92Bit0WithTemporalGate` `00250130`, `InputGameplay_TestAggregatedMask62Bit1WithTemporalGate` `002501A0`, `InputGameplay_TestCombinedMaskBit1WithTemporalGate` `00250200` and `00862CF0`. `00226BE0` reads `PartyRoster_GetActorBySlot` `00263750` and `003590D0`. `00313A00` (InputGameplay) sets and clears capability bits through `002E1C20` and `002E1CA0`, which OR or clear bit `edx` in row `ecx` of the 16-row table that `002E0FA0` folds, and it reads `00377C20`. The input arbiter builds a member view through `00320040` next to its capability reads, and the capability-row writers are the ones the arbiter's aggregate reads. The view contributes the member's flags to input, never the reverse.

**Items_Equipment_Shops_License — CLIENT and SERVICE (9 edges).** The builder's `full` arm calls `BattleStats_CountLicenseBits00To17` `00324020` for `+0xBB`. That popcount is shared with `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910`, `BattleStats_CheckLicenseNodeAcquireReason` `00323D10`, `BattleStats_HasRequiredLicenseForAction` `00323EC0` and `BattleStats_ComputeLicenseDerivedRank` `00324100`, and `00323910` also reads `0030A310`, the party-row byte getter behind `+0xB4`..`+0xB8`. `BattleStats_ClearAllEquipmentSlotsByMappedId` `0031A300` walks `00236820`. `Inventory_QueryOwnedCountIncludingReservedActionItems` `00309FB0` and `Equipment_UnequipEncodedItemFromActiveRoster` `0030FD10` read `00377C20`. The view shows the licence count and party-row words through the same helpers that the licence board mutators use, and the equipment bodies are further users of the pool accessor and field predicate.

**Party — CLIENT and SERVICE (40 edges).** The view's handle and focus fields read the party layer. `+0x04` comes from `PartyRoster_GetActorBySlot` `00263750`, and the focus unit comes from `003590D0`. The builder calls both, and the UI evaluators `002C62B0`, `002C6F70` and `002C7660` read `003590D0` too. `0035BC50` reads `PartyFocus_GetPreferredDefinitionSelector` `003271D0` and the focus thunk `003272E0`. Six party bodies read `003590D0`, among them `PartyRoster_GetActorBySlotOrCurrentFocus` `00263770`, `PartyRoster_AssignActorToSlot` `00269C70` and `PartyFocus_IsCurrentPackedActorHandle` `003273B0`. Six read `00263750`, among them `PartyConfiguration_ReconcileRosterFromCurrentSelectors` `003261D0` and `VMPartyCommand_DemoteOtherRuntimeRosterSelectors` `00350CD0`. Five compose handles through `003589B0`, and four read `00263E30`. `00303CC0` and `00304180` call `00327200`, the bit-11 "designated member" test. `0030C0E0` and `BattleUnit_ReleaseTargetRelationAndActionState` `00310780` call `BattleUnit_ResolveByFocusHandle` `0031B7E0`, and `00328BD0` calls `00283270`. The view reports which member is the leader, the focus and the designated slot by reading the party layer's roster and focus state, and those party bodies are the main other users of the same getters.

**Save_Load_Settings — CLIENT and SERVICE (14 edges).** Five save controllers call `00247870`, the widget flag setter that the display record's field pass uses twelve times: `SaveWrite_OperationStateCallback` `0057E4D0`, `SaveLoad_FullImageStorageCompletionCallback` `00580840`, `SaveSlotScan_ControllerCallback` `005819F0`, `SaveStorageQueue_ControllerStateHandler` `005823B0` and `SaveLoad_ControllerLifecycleHandler` `00582860`. `005823B0` and `00582860` also set and clear capability rows through `002E1C20` and `002E1CA0`. `00582860` and `SaveTransition_PrepareRuntimeImageForCapture` `005844A0` call `00283270`, one of the view's ten callers, whose purpose on the save path is not read here. `SaveSlotMetadata_BuildSubmissionDescriptor` `005832B0` calls `00254A10`, which returns 1 when a mode getter answers 0, 7, 8, 10 or 11, and `005817D0` calls `0029F4B0`, a 4-byte store to `+0x1C`. In the service direction, `PersistentFlag_QueryBank2048` `0032A930`, which the name path reads, calls `SaveImage_GetPersistentPayloadBase` `002EF2B0`. The save screens reuse the same widget helpers and capability-row writers that this page's UI callers use. The story flag that picks a member's display name lives in the save payload.

**Spawn_Encounter_Lifecycle — CLIENT (28 edges).** Twenty-four spawn bodies resolve units through `ActorWork_GetBattleUnit` `0031B760`, the checked sibling of the builder's `00263E30`. Among them are `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0`, `SpawnEntry_GetDeathCount` `00235F50`, `SpawnEntry_GetRespawnCooldownTicks` `002366E0` and `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410`. `Spawn_CountActiveCapTrackedActors` `00308D90` walks the pool accessors, and `Spawn_ValidateCandidateDistanceToPlayers` `00234DA0` and `002350C0` read the predicate thunk `00313F60`. The spawn layer is a heavy reader of the unit accessors this page cites. It reads spawn entries, not the party view, and nothing crosses between it and the record.

**Status_Periodic_Terminal — CLIENT (6 edges).** `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860` reads `00263E30`. `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450` and `BattleUnit_AddPrimaryResourceRecoveryAccumulator` `00329A20` read `00313F60`. `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690` and `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` read `00377C20`. These status bodies write the status words and resources that the view later copies (`+0x44`, `+0x48`, the countdown bytes and the MP block). They reach this page only through the shared unit getter and field predicate.

### Interior citation — frontier hub `00271AB0` (2026-09-18, SWE2-EC7)

`00271AB0` — 506 B, 13 callers, `FrameInterpolation.SineOrLinearFourChannel`:
the interpolator `002C7B10` runs twice. It scans the 0xC-stride keyframe records
for the pair bracketing `r9d` (`word[+4]`/`[+0x10]` compare at
[`00271AE0`](../../_index/ADDRESS-INDEX.md)), then interpolates — mode `+8==1`
is linear `((r9-a) << 8) / (c-a)` divided at
[`00271B3D`](../../_index/ADDRESS-INDEX.md); other modes run the `sinf`-eased
arm (`00861F0E`, scale `0x65440C`-family constants). Per-channel, four
channels.


## SWE2-EC7-39 update (2026-09-19) - `003C3340`

`003C3340` (414 B) is the Presentation builder the page names - `01CEBBA8`/`01F44830`/`02B45A04`, `00202B70`/`0031FF70`/`003C6B70`/`00808C40`; builds the record at `[rsp+0x30]` and reads none of it in its own body. Interior anchor `003C3401` (a `00202B70` call).

## SWE2-EC7-43 update (2026-09-19) - `002C62B0`

`002C62B0` (276 B) is a unit-display-record body - `002C7660`/`002C7F90`/`002E0FA0`/`003588B0`/`003590D0`/`003F14D0`. Interior anchor `002C62D8` (a `002C7660` call).

## SWE2-EC7-48 update (2026-09-19) - `0031FF70`

`0031FF70` (199 B) is a body - `00263E30`/`003588B0`. Interior anchor `0031FF96` (a `00263E30` call).

## SWE2-EC7-52 update (2026-09-19) - `003C6B70`

`003C6B70` (1908 B) is the Presentation builder's worker - 0x540 frame, `ucomiss` against `1.0f`, `00248EB0`/`00181560`/`00861F0E`/`00861F08`/`00400420`/`003C86B0` calls, `02EBA498`. Interior anchor `003C6C75` (a `00248EB0` call).

## SWE2-EC7-55 update (2026-09-19) - `003C86B0`

`003C86B0` (241 B) is a call-free tagged-record emitter - `eax-0x13` kind arms building 16-byte records (`+8` tag `6`/`0x16`, packed `0x8000000f` fields) into `[r10+0x10]`'s queue. Interior anchor `003C8704` (the `+8` tag write).

## SWE2-EC7-56 update (2026-09-19) - `00400420`

`00400420` (231 B) is a record-00329220 body - `0035D460` single call plus `00D120E0`. Interior anchor `00400443` (a `0035D460` call).



## SWE2-EC7-66 update (2026-09-19) - `00536280`

`00536280` (131 B) is the text-bank name resolver - `0020E600` single call plus `01CEB638`/`02EBF170`. Interior anchor `005362B0` (a `0020E600` call).


## SWE2-EC7-70 update (2026-09-19) - `003F14D0` tail-append measured

`003F14D0` (78 B) is the tail-append the unit-display builder runs on the
`+0x40` list: zeroes the new node's `+0xF8`/`+0x100` link pair, walks
`+0xF8` links from `[rcx+0x40]` to the tail, and links `rdx` in -
`tail[+0xF8] = rdx`, `rdx[+0x100] = tail`. Empty list stores `rdx` as the
head directly.
Interior anchor `003F1500` (the `+0xF8` walk loop).

## SWE2-EC7-83 update (2026-09-20) - `0042FB20` indexed scale fetch measured

`0042FB20` (85 B) is the record-indexed float the display callers
sample: `cx == -1` returns the `01CB8BA0` constant; else `cx*0x740`
into `022C6F28`, the `+0x284` gate falls back to the same constant,
and a live record runs `003E48E0(rec, 0xB)` whose result converts
`cvtdq2ps` and scales by `01C08010`.
Interior anchor `0042FB59` (the `003E48E0` call).

## SWE2-EC7-95 update (2026-09-20) - `0031FD70` + `0031FCF0` measured

`0031FD70` (39 B) and `0031FCF0` (48 B) are the
`00263E30`-resolve pair `002BFD20` and `002C6F70` call: both
null-gate the argument, then `00263E30` runs - the first hands
`rcx = rax` to the shared `0031FDA0` continuation, the second
returns `rax != 0` as a boolean.
Interior anchors `0031FD86` and `0031FD0D` (the two `00263E30`
calls).

## SWE2-EC7-96 update (2026-09-20) - `002FEAD0` measured

`002FEAD0` (172 B) is the tag-bit writer `0030C2C0` and
`00310780` call: the `[rcx+0x698]` record passes the `+0x64 |
+0x3C` vs `0x80000003` gate with the `00377C20` re-check, then
`0030C0E0` decides the fast path - nonzero sets bit 20 of
`[rbx+4]` directly; zero walks the `+0xEA4` mask for the bit
whose index matches `byte[+0xEA9]` while `cl != byte[+0x6B6]`,
and only that match sets bit 20 (all misses clear it).
Interior anchor `002FEB03` (the `0030C0E0` call).

## SWE2-EC7-103 update (2026-09-20) - `00273A00` measured

`00273A00` (32 B) is the kind-5 predicate
`002BFD20` and `002C0870` call: `003588B0()`
supplies the record, `00263C20` answers a code,
and the return is `code == 5` - the class check
the record builds share.
Interior anchor `00273A13` (the `cmp eax, 5`).

## SWE2-EC7-106 update (2026-09-20) - `002547D0` measured

`002547D0` (105 B) is the seven-slot
invoke `00254940`, `0035BC50` and
`0035C770` run: `ecx != 0` picks
`002E1C20`, else `002E1CA0`, then the
chosen thunk is called six times with
`(edx, ecx)` pairs `(1,8)`, `(2,8)`,
`(4,8)`, `(5,8)`, `(6,8)`, `(7,8)`
and tail-jumped once more with
`(9,8)` - the fixed sequence the
display-record builders fire per
slot.
Interior anchor `002547F2` (the first
`call rbx`).

`003C7750` (988 B) is the record body `003C6B70` runs: `00203170`, `00202B70` x3, `00202CA0` x2 and `00181350` fill the display record's fields under the cookie check - the unit-display record's emit helper.

Interior anchor `003C7928` (function `003C7750`).

`002C0400` (850 B) is the channel body `002BFD20` calls: `00296280` and `002962C0` prepare, `00247870` x12 iterates the record's fields with `0029F6E0` x3 and `0029F4B0` - the display record's `00247870`-dense field pass.

Interior anchor `002C042B` (function `002C0400`).

`00295D90` (588 B) is the build arm `002BFD20` calls: cookie frame, `002AC2E0` + `002F9860` set up the record, `r15d` gates the `edi = 1` path, then `0016D6A0`/`0017D2E0`/`00254A10`/`00264150`/`002AC290`/`002B4090`/`00808C40` run the fill - the unit record's conditional emit.

Interior anchor `00295DFC` (function `00295D90`).

`00272F80` (468 B) is the row iterator `00272F60`/`002BFD20` call: `word[rbx+0xA]` sizes each pass (0 -> `r10d = 2`), `edi - 6*i + 6` clamped to `>= 0xC` bounds the step, and `00273410`/`00275E40`/`003178C0` run per row with `ebp` carrying the worst result - the record's stepped-table walk.

Interior anchor `0027304C` (function `00272F80`).

`003178C0` (112 B) is the bit tester `00272F80`/`00275E40` call: `02089340 & 0x10` gates, `003588B0` resolves the manager, `00263E30` resolves the record, `byte[rax] & 0x10` and `[rax+0x698]`'s `byte[+5] == 1` gate, then `(1 << dl) & 0x80000003` answers the slot bit - the record's per-slot flag query.

Interior anchor `003178D2` (function `003178C0`).

`002C8310` (449 B) is the field-map op `002C7660` calls: `r8w` gates, `003F0040` resolves the fifth stack arg into `r14`, `0031FC10`/`00320640` bounds come back in `ebx`/`rcx` with `cmovle` taking the smaller, then `002C5F90`/`002C69A0`/`0035D3D0`/`003F1290`/`00202B10` run the range walk - the record's bounded field pass.

Interior anchor `002C833F` (function `002C8310`).

`002C69A0` (417 B) is the packed-nibble decoder `002C8310` (and `002C7F90`/`002C8820`) call: `byte[r8+7] >> 4` and `& 0xF` split the selector byte, the high nibble indexes `byte[[rdi+0x20] + 0x30 + hi]` and the low nibble adds in, then `word[r14+0xE8]`/`qword[r14+0xE0]` take the decoded value and the record pointer - the record build's sub-field unpack.

Interior anchor `002C6A63` (function `002C69A0`).

`002C5F90` (483 B) is the call-free gauge mapper `002C8310` calls: a three-case `ecx` dispatch whose case 2 reads the `01E0CF20` rect globals (`+0x4`/`+0x10`/`+0x14` ends and origins), scales `(rdx+1) / 26.0` through `00916484`, lerps `01E0CF24..01E0CF34` and shifts `<< 8` into the return - the bar-fill width computation inside the record pass.

Interior anchor `002C5FA9` (function `002C5F90`).

`002C0760` (267 B) is the sub-widget reset `002BFD20` runs on `rcx`: six fixed slot indices `{1, 2, 0x11, 7, 6, 0xC}` (with `{0xA, 0xB, 0x12}` staged) each run `00247870` on `[[rcx+0x60] + idx x 8] + 0x18`; a second pass over seven indices clears bit 0 of `dword[[[rcx+0x60] + idx x 8] + 8]`; finally `word[[[rcx+0x60]+0x28] + 0x12] + word[+0xE]` lands in `word[rcx+0x9E]` - the dimension refresh the unit-display record rebuilds after clearing its children.

Interior anchor `002C07EE` (function `002C0760`).

`00273160` (260 B) is the flag lookup `002C6F70` runs: `00320C60` fills `*[rsp+0x48]` with a bitmask, and when nonzero `0035D490`'s table is scanned 32 deep (`[rax + i*8 + 0x1700]`) for a record whose `+0x98` bit lies in the mask; on hit `*[rsi]` takes that bit index and `*[rdi]` a flag byte - base `2` (or `0` when `byte[+0x23] == 0xFF`) OR'd with `+0x25` bits 1..4 mapped to bits 0/2/3/4 - returning `1`; `0` and empty outs otherwise - the overhead status-order read of the cached L1 (`+0x1700`) table, keyed on row `+0x23`, that drives the status icon shown above each unit (corrected 2026-09-27, GA-1: earlier called a generic "privilege decode"; the `+0x1700` walk is hard-wired at `002731B0`/`002731E1` and the call chain is per-actor overhead-icon, `002C71D0` in `002C6F70`).

Interior anchor `00273188` (function `00273160`).

`002C8920` (255 B) is the element init `002C7660` runs when `dx` is nonzero: `003F0040` resolves the index to a `rbx` object, `00202C90` binds `rbp` to it, `dword[+0xC] = -1.0f` arms it, `0035D460` resolves the source, `003F12E0(rbx, src, 0xE00, 1)` pulls the entry whose `[+4] & 0xFFF` and `>> 0xC` fields zero-extend into the staging pair, and `003F1290` commits `+0x5C` and friends - the display-record element populate.

Interior anchor `002C8949` (function `002C8920`).

`002C8820` (241 B) is the scaled-count emit `002C7660` runs when `byte[rcx+0x2C] * dx >> 7` is nonzero: `003F0040` resolves the `[rsp+0x60]` index, `003588B0` on `dword[rsi+0x10]` feeds `00263B80` - a `1` answer short-circuits, else `0035D3D0` runs three times, `002C69A0` binds `r14` and `003F1290` commits - the display-record scaled-element emit.

Interior anchor `002C8855` (function `002C8820`).

`0035D490` (65 B) is the init-once `022C8B08` accessor: when `dword[022C83E8]` lacks bit 0x200 the body runs `00273BA0(&022C8B08)` and sets it, then returns `&022C8B08` - the shared static-object gate the widget and record-build callers share.

Interior anchor `0035D4AC` (function `0035D490`).

`00273BA0` (643 B) is the `022C8B08` status cache build `0035D490` gates once: it stamps each of cells 0..31 with a copy of the category-0x1A template `0035D330(0x1A, i)` (0x98-byte rows plus a trailing qword) - the 32 class-26 status records at `+0x0`..`+0x14FF` - then runs the `002D02C0` bitmask-expand + `002D03B0` enumeration pair four times over the cell field lanes and converts each emitted byte pair into record pointers (`index*0xA8` into `rbx`) stored into the four 32-qword status order tables rooted at `+0x1508`/`+0x1608`/`+0x1708`/`+0x1808` (`+0x1500`..`+0x18FF`) - the ordered-status tables the readers (`00273160`, `00273380`, `00271FB0`, `00273410`, `00272F80`) index by listing key (corrected 2026-09-27, GA-1: earlier called a "link table" and "neighbour table"; the four tables are status order lists, each built with `002D02C0` kind 1-4).

Interior anchor `00273C63` (function `00273BA0`).

`002734F0` (230 B) is the unit-record classifier `002BFD20` runs on `ecx`: `0` returns `0xFF`; a `0035BB60`-bounded `0035BB00` scan that finds `edi` returns `0`; otherwise it resolves the record via `003588B0`, requires `00263C20(record) - 1 <= 2` and a live `0031FD20(edi)` + `0035BAF0()` object, then diffs `0031FBD0(record)` (or `object[+0xBA]` when negative) against `object[+0xBA]` - the delta ladder returns `1` (`<= 0`), `2` (`<= 2`), or `3` (`> 2`), with `0` on any dead link

Interior anchor `00273576` (function `002734F0`).

`0031FD20` (66 B) is the gated liveness resolve `002734F0` and `00273710` share: a clear `02089340` bit `0x10` returns `0` untouched; set, it resolves `ecx` through `003588B0`, and only when the record is non-null does it run `00263E30` and return whether that produced an object - `0` on the disabled gate, a dead record, or a dead resolve

Interior anchor `0031FD3B` (function `0031FD20`).

`00275E40` (200 B) is the set-bit lane counter `00272F80` calls: for each set bit of `ecx` (max 32) it `0035D330`s the lane record keyed `0x1A`, picks a sentinel byte by mode `edx-1` (`+0x23` / `+0x24` / `+0x22` with an optional `003178C0` callback when `r8d != 0`, else `+0x21`) and counts lanes whose byte is not `0xFF`

Interior anchor `00275E8C` (function `00275E40`).

`00320640` (155 B) is the scaled-field read `002C8310` runs: `00263E30(rcx)` resolves the record, `[rax+0x698]` is the sub-table, and `edx` picks the pair (`edx == 0`: dwords `+0x24`/`+0x48`; `edx == 1`: words `+0x28`/`+0x4C`); `r8d <= 0` returns the first, `r8d == 0x64` returns `-1`, otherwise it returns `second + first*r8d/100` through the `0xA3D70A3D70A3D70B` multiply - a percent-scaled stat lane.

Interior anchor `00320654` (function `00320640`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-record-00329220-builds-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00273380` | 135 B | returns 0 when `ecx` is zero; otherwise calls `0035D490()`, picks the table offset from `edx` (1 gives `0x1700`, 2 gives `0x1600`, 3 gives `0x1800`, any other value `0x1500`) and walks the 32 qwords at that offset of the returned pointer, returning the first qword whose dword `+0x98` names a bit (`bt`) that is set in the original `ecx`, or 0 when none of the 32 does | `0027338E`, `00273392`, `002733D3`, `002733DA`, `002733E6` |
| `00273410` | 76 B | calls `0035D490()` and returns its pointer plus `0x1700` when `ecx` is 1, plus `0x1600` when 2, plus `0x1800` when 3, and plus `0x1500` for any other value | `00273418`, `00273450`, `00273444`, `00273438`, `0027342C` |
| `002915C0` | 389 B | walks the list headed by qword `+0x10F20` of `rcx` (next link qword `+0x9B0`) and returns the first node whose dword `+0x980` equals `r9d`; otherwise allocates `0x9D0` bytes with `00273A30(0, qword +0x10FC0 of qword 0209BE80, 0x9D0)` (returning 0 when that fails), runs `00275550(node, 0x9D0)` twice, then calls `00202C90(node+0x960, r8)` when `r8` is non-null, else ORs 2 into byte `+0x991`, stores `r9d` at `+0x980` and calls `002713E0(node+0x960, r9d)`; stores `dl` at byte `+0x990`, ORs 4 into `+0x991` when the fifth (stack) argument is non-zero and stores the sixth (stack, float) argument at `+0x9A8`; fills qword `+0x10F50` of `rcx` from `0024A5A0(qword 01E0C1E0)` when it is null and copies it to `+0x988`; calls `00271140` and `003F2600(node, ...)` on a stack buffer, stores word 1 at `+0x9C0`, links the node in with `003F2580(old head, node)` into `+0x10F20` and returns the node | `002915F1`, `00291624`, `0029166E`, `002916B3`, `0029171F` |
| `002ED0B0` | 125 B | calls `003588B0(rcx)`; when the result is null, or its qword `+0xC0` is null, or the dword at that pointer is -1, stores 1 at dword `[rdx]` and 0 at dword `[r8]` and returns; otherwise returns without stores when the word at that pointer is `0xFFFF`, when the word sign-extended times `0x740` plus qword `022C6F28` is zero, or when dword `+0x284` of that record is zero, and else tail-jumps `003E4EA0(record, rdx, r8)` | `002ED0C0`, `002ED0D6`, `002ED0E8`, `002ED111`, `002ED116` |
| `0031FC10` | 85 B | returns -1 when `rcx` is null, `00263E30(rcx)` returns null, or qword `+0x698` of that result is null; otherwise ORs dwords `+0x64` and `+0x3C` of the `+0x698` object and, when bit 16 is set, returns dword `+0x48` raised to at least 1 (signed), else returns dword `+0x24`, doubled when bit 28 is set | `0031FC19`, `0031FC32`, `0031FC45`, `0031FC4D`, `0031FC56` |
| `00345800` | 46 B | returns 1 when `003588B0(003590D0())` is non-null and `00264E10` of that pointer returns non-zero, else 0 | `00345806`, `0034580D`, `0034581C`, `00345823` |
| `00346FA0` | 73 B | takes `00267E10(r9)`; when it is non-negative (signed) resolves the object with `00358940(002640C0(), value)`, otherwise with `003588B0(003590D0())`, and tail-jumps `003B6F80(object)` when the object is non-null, else returns 0 | `00346FA9`, `00346FB2`, `00346FBE`, `00346FCC`, `00346FDE` |
| `0034C3D0` | 75 B | resolves `003588B0(00267E10(r9))` and, when that is non-null and `00262F50(rdx, object)` returns non-zero, calls `0035AE10(object, 1)` | `0034C3E0`, `0034C3E7`, `0034C3FA`, `0034C401`, `0034C40B` |
| `0034C950` | 51 B | resolves `003588B0(00267E10(r9))` and tail-jumps `00262F50(rdx, object)` when it is non-null, else returns 0 | `0034C95C`, `0034C963`, `0034C96B`, `0034C978` |
| `0034F800` | 112 B | resolves `003588B0(003590D0())`; when non-null tail-jumps `0034EBC0(rcx, object, r8, r9)`, otherwise calls `00267DB0(r9)` three times, the third as a tail jump | `0034F818`, `0034F81F`, `0034F844`, `0034F84C`, `0034F86B` |
| `0034FF00` | 156 B | resolves `003588B0(003590D0())` and reads a float with `00267DB0(r9)`, passing it as `0026B620(object, float)` when the object is non-null; then resolves `003588B0(003590D0())` again and calls `0034EBC0(rcx, object, r8, r9)` when non-null, otherwise calls `00267DB0(r9)` three times | `0034FF24`, `0034FF3F`, `0034FF52`, `0034FF68`, `0034FF72` |
| `00350DD0` | 238 B | reads a float radius with `00267DB0(r9)` and an index with `00267E10(r9)`, resolves `00358940(002640C0(), index)` and `003588B0(003590D0())`; when both are non-null, fills three floats with `00265020(first, &a, &b, &c)` and sets the result to 1 when the radius squared is greater (`comiss`, `cmova`) than the squared distance between floats `+0`, `+4`, `+8` at qword `+0xB8` of the second object and `a`, `b`, `c`, else 0; tail-jumps `0026B4E0(rcx, result)` | `00350DF4`, `00350E10`, `00350E47`, `00350E95`, `00350EB9` |
| `003516E0` | 213 B | reads a float radius with `00267DB0(r9)` and an index with `00267E10(r9)`, resolves `00358940(002640C0(), index)` and `003588B0(003590D0())`; when both are non-null, fills three floats with `00265020(first, &a, &b, &c)` and sets the result to 1 when the radius squared is greater (`comiss`, `cmova`) than the squared two-axis distance of floats `+0` and `+8` at qword `+0xB8` of the second object from `a` and `c` (`b` unused), else 0; tail-jumps `0026B4E0(rcx, result)` | `00351704`, `00351720`, `00351757`, `0035178C`, `003517B0` |
| `00352580` | 213 B | reads four floats with `00267DB0(r9)` (radius, then values 2, 3, 4) and resolves `003588B0(003590D0())`; when non-null, sets the result to 1 when the radius squared is greater (`comiss`, `cmova`) than the squared distance of floats `+0`, `+4`, `+8` at qword `+0xB8` of the object from values 4, 3 and 2 respectively, else (also for a null object) 0; tail-jumps `0026B4E0(rcx, result)` | `003525A9`, `003525DB`, `003525FB`, `00352627`, `00352650` |
| `003530F0` | 171 B | reads three floats with `00267DB0(r9)` (radius, then values 2 and 3) and resolves `003588B0(003590D0())`; when non-null, sets the result to 1 when the radius squared is greater (`comiss`, `cmova`) than the squared two-axis distance of floats `+0` and `+8` at qword `+0xB8` of the object from values 3 and 2 respectively, else (also for a null object) 0; tail-jumps `0026B4E0(rcx, result)` | `00353113`, `00353139`, `00353159`, `00353173`, `00353196` |
| `00356570` | 55 B | calls `002640C0()` and `00267E10(r9)` without keeping their results, then stores the qword `003588B0(003590D0())` at `[r8]` | `00356580`, `00356588`, `0035658D`, `00356594`, `0035659E` |
| `0035C770` | 33 B | calls `002547D0(ecx)`, then tail-jumps `00254E70()` when `ecx` was zero and returns otherwise | `0035C778`, `0035C77D`, `0035C786` |

## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; move drafted by OPUS)

*Each body below was homed on another page by FABLE's homing stream (cloud-drafted, FABLE-verified). SWE2-AUDIT-SPEC reviewed its sentence, site and anchors exact, and rejected only the host: that page cites the caller as a foreign or boundary mention (commit `4522aeff6`). The row is moved here because this page cites the caller in its own text. The sentence is unchanged except where `moves.json` records a bits-as-values edit. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`move_rows.py`](../../_index/candidates/opus-fable-home-host-moves-1003/move_rows.py): every site transfers to its function, this page cites the caller outside this section, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors | moved from |
|---|---|---|---|---|---|
| `00322950` | 67 B | `002C7660` + 0x1AD | returns 0 when bit `0x10` of byte `02089340` is clear; otherwise passes the result of the call at `00322950` + 0xD to the call at `00322950` + 0x1A and that result with 0 to the call at `00322950` + 0x29, returning 0 if either of the first two results is null and else 1 when the last call returns 0 and 0 when it returns non-zero | Interior anchor `00322954`; Interior anchor `0032295D`; Interior anchor `0032296A`; Interior anchor `00322979`; Interior anchor `00322982` | [the-status-write-and-its-side-effects](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) |
