---
system: Battle command availability and reason codes
category: 07-Combat-Action
status: AUDITED — the availability check, its reason codes and the resource pools read; AI-1 answered 2026-09-02 (the codes never reach a screen), AI-8 answered by reference 2026-09-12 (MP, Mist charges, gil), AL-10 named 2026-09-12 (the spawn-keep flag bits); every box ticked, status line brought up to date 2026-09-18 (FABLE)
owner_layer: PrimaryOwner:CombatAction — consumed almost entirely by CombatAction/CombatAI (6 of 7 callers); UI is one caller
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
last_reviewed: 2026-09-02
audit:
  passes: 2
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# Battle command availability and reason codes

> Why a battle command is greyed out — and the numbered reason the engine computes before the
> menu is ever drawn.

**PARTIAL.** The top-level cascade is read at instruction level. Several of its steps call
functions whose bodies have not been read, and the numeric reason codes are recovered but **not
mapped to the on-screen messages**.

## 1. What the player sees

Open the battle menu and some entries are unavailable. Magick you own but cannot cast right now.
A Technick that works on one target and not another. Item greyed out. Everything unavailable while
a character is Stopped or Confused. An ability you have not bought the License for at all.

That is not the menu deciding. **The menu asks, and something else answers.** And the thing it asks
is not a menu component at all — it is the engine's single **action-legality authority**, which the
**Gambit AI** and the **action-execution path** ask too, with the same question and the same rules.

That is the fact worth carrying away: **a gambit declines to fire an action for exactly the same
reason the menu greys it out.** They are not two rule sets that happen to agree; they are one
function with seven callers, six of them in combat and one in the UI.

The practical consequence is that *availability is computed per action, per unit, every time it is
asked* — which is why an entry can grey out mid-battle without the menu being reopened, and why a
gambit can stop firing without anything visible changing.

## 2. Native mechanism

### The asker

`BattleMenu_BuildCommandEntryList` (`0031EB20`, 4,182 B, **UI**-owned) builds the list of command
entries. It is called from **16 sites, all UI**, and is **recursive** (it appears among its own
callers) — consistent with a menu that contains submenus.

It calls, among others:

| Callee | Role |
|---|---|
| `BattleAction_CheckActionAvailabilityReason` (`002FFCF0`) | **the availability cascade — this document** |
| `BattleAction_CheckUnitActionAvailability` (`00306480`) | per-unit leg of the same cascade |
| `BattleAction_ComputeModifiedResourceCostAmount` (`002F95D0`) | the cost after modifiers |
| `BattleUnit_UsesGilActionCostChannel` (`002F9820`) | selects the **gil** cost channel |
| `GambitConfig_ClassifyActionTargetPairCompatibility` (`00327A10`) | action/target legality |
| `BattleEncodedId_IsValidForClass` (`00322C50`) | action-id class validation |

### The cascade

`BattleAction_CheckActionAvailabilityReason(ushort actionId, BattleUnit *unit)` returns **0 when the
action is available**, and a nonzero **reason code** otherwise. Read from `002FFCF0`:

```c
raw = unit->[0x698];                       /* the unit's battle record */

if (!(unit->flags & 0x10) || raw == NULL)              return 2;

/* the engine-wide functional predicate, verbatim */
if (((raw[0x64] | raw[0x3C]) & 0x80000003) != 0
    && FieldData_GetActiveFieldRecordBit15() == 0)     return 2;

if (raw[5] == 1 && (unit->[0x6A0][0] & 0x30))          return 2;
if (raw[5] == 1 && (unit->[0x6A0][0] & 0x48))          return 2;

if (!BattleEncodedId_IsValidForClass(0x14, actionId))  return 4;

if (raw[5] == 0
    && ((raw[0x64] | raw[0x3C]) & 0x08000020) == 0
    && FUN_00253B90()
    && actionId != 0x113 && actionId != 0x95)          return 0x24;

if (actionId - 0x106 <= 0xC                            /* ids 0x106..0x112 */
    && BattleRuntime_GetMode0To5FromFlagsAndFieldBit15() == 1)
                                                       return 0x2C;

/* authored action definition record: base + actionId * stride */
rec  = actionTable + actionId * stride;                /* table @ registry slot 02EBF138 */
mask = ((rec[0x0C] & 0x80000) || rec[0x1E] == 1) ? 0x8000221B : 0x8000201B;

if ((r = FUN_0030E9C0(raw, mask)))                            return r;
if ((r = BattleAction_CheckGlobalCategoryDisableReason(raw, actionId)))   return r;
if ((r = BattleAction_CheckUnitActionAvailability(actionId, raw, 0)))     return r;
return BattleAction_CheckExecutionResourceAvailability(unit, actionId);
```

**Every step returns the first refusal it finds.** The order is the priority order: unit-level
sanity, then id validity, then two special-case gates, then the authored definition's own status
mask, then category, then unit, then cost.

### The per-unit leg, and the License Board

`BattleAction_CheckUnitActionAvailability` (`00306480`) is short enough to give in full:

```c
if (unit == NULL)                                        return 0x2C;
if (BattleAction_CheckDefinitionCategoryAvailability(actionId))  return 0x0F;
if (BattleStats_HasRequiredLicenseForAction(unit, actionId))     return 0;
return 0x10;
```

The last line is the one a player meets constantly: **reason `0x10` is "no License"**. The check is
`BattleStats_HasRequiredLicenseForAction` (`00323EC0`, 338 B, owned by
**Items/Equipment/Shops/License**), and it is the *last* thing tested — so an action you lack the
License for is refused only after it has passed every other gate.

### Reason codes recovered

| Code | Raised by | Meaning as read |
|---:|---|---|
| `0` | — | **available** |
| `2` | `002FFCF0`, five paths | unit not in a state that can act at all |
| `4` | `002FFCF0` | action id is not valid for class `0x14` |
| `0x0F` (15) | `00306480` | the action's **definition category** is unavailable |
| `0x10` (16) | `00306480` | **no License for this action** |
| `0x24` (36) | `002FFCF0` | a global gate; **all ids refused except `0x113` and `0x95`** |
| `0x2C` (44) | `002FFCF0`, `00306480` | null unit; **or** ids `0x106`–`0x112` while runtime **mode 1** |

The remaining legs were read on 2026-09-02 and their codes are enumerated in section 10. Two
points about how they compose:

- `0030E9C0`, `BattleAction_CheckGlobalCategoryDisableReason` and
  `BattleAction_CheckExecutionResourceAvailability` **pass their codes through unchanged** — the
  cascade returns them verbatim.
- `BattleAction_CheckDefinitionCategoryAvailability` does **not**. Its own codes (`4`, `5`, `0x0F`,
  `0xFFFF`) are **collapsed to a single `0x0F`** by `00306480`, which tests only whether the result
  is nonzero. Those four distinctions never reach the caller.

### Two structural findings

**The engine-wide functional predicate appears here verbatim.** `(raw[0x3C] | raw[0x64]) &
0x80000003` combined with `FieldData_GetActiveFieldRecordBit15() == 0` is the same predicate
recorded across the database, at the same status-mask offsets `+0x3C` / `+0x64`. This is a further
independent sighting, and it is the **first at the top of an availability cascade** — it is the
*reason* a Stopped or Confused unit's whole menu goes dead, rather than each command checking
separately.

**The two-layer convention appears at a third offset pair.** `BattleUnit_UsesGilActionCostChannel`
(`002F9820`):

```c
if (unit && raw && raw[5] == 1)                    return 0;
return (raw[0x6C] & 1) || (raw[0x7C] & 1);
```

`+0x6C` / `+0x7C` — a `0x10` stride, exactly parallel to the rewards pair at `+0x6B` / `+0x7B` and
the status pair at `+0x3C` / `+0x64`. Three pairs now, all with layer1 a fixed distance above
layer0, which supports reading these as **two parallel effect blocks** rather than unrelated fields
that happen to be tested together.

## 3. Key addresses

| Address | Size | Role |
|---|---:|---|
| `0031EB20` | 4,182 B | `BattleMenu_BuildCommandEntryList` — the asker (UI, 16 callers, recursive) |
| `002FFCF0` | 479 B | `BattleAction_CheckActionAvailabilityReason` — **the cascade** |
| `00306480` | 99 B | `BattleAction_CheckUnitActionAvailability` — per-unit leg |
| `00323EC0` | 338 B | `BattleStats_HasRequiredLicenseForAction` — the License gate |
| `003060E0` | 595 B | `BattleAction_CheckDefinitionCategoryAvailability` |
| `0031A7B0` | 264 B | `BattleAction_CheckGlobalCategoryDisableReason` |
| `00303BD0` | 238 B | `BattleAction_CheckExecutionResourceAvailability` — the cost leg |
| `0030E9C0` | 117 B | status-mask test, called with `0x8000201B` / `0x8000221B` |
| `00322C50` | 1,025 B | `BattleEncodedId_IsValidForClass` |
| `002F9820` | 51 B | `BattleUnit_UsesGilActionCostChannel` |
| `002F95D0` | 589 B | `BattleAction_ComputeModifiedResourceCostAmount` |
| `00377C20` | 78 B | `FieldData_GetActiveFieldRecordBit15` |
| `0030D9A0` | 105 B | `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` |
| `00253B90` | — | null predicate over `01E0C2B8` — also the capability policy's bit-1 input |
| `0x02EBF138` | — | registry slot: the **action definition table**, ids `0`–`0x21E` |

### 3a. The `0031EB20` exclusive subtree — all 10 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns `BattleMenu_BuildCommandEntryList` **10 frontier functions** —
the private machinery beneath the asker: per-command visibility, candidate enumeration, legality
and reason classification. Interior cites are one instruction inside each declared extent
(`interior_cite.py`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| per-command visibility | `002FA140` (90 B) | tri-state classifier: `0` when `[unit+0x698]->byte[5]==1` (unit suppressed); `2` for action ids in `0x106`–`0x112` or `0xD0`–`0xE1` (always-listed classes); else `1`/`0` on flag bit 0 of `[+0x698]+0x6C` / `+0x7C` | `002FA15A` |
| kind-gated record reads | `003093B0` (22 B), `0032A3E0` (228 B) | `003093B0` — `[rec+0x1E]==3` → `word[+0x22]`; `0032A3E0` — `00322C50` class-gated entry classifier over `[rec+0x1E]` and `[+0x2C]&7`, kind arg compared against `0x12`/`0x13` | `003093B5` / `0032A40B` |
| candidate enumeration | `00317C80` (244 B), `0031E630` (181 B), `00322630` (133 B) | `00317C80` — the `0x116`-entry table scan: two `0020E600` row lookups, kind gate `[+0x1E]`/`[+0x2C]&7`, `00306480` unit check, `003093D0`→`00309EC0` ranking keeps the best (`r14=0xFFFF` sentinel); `0031E630` — §12's nearest-candidate default (`003590D0`/`003588B0` resolve, flag `test [rax],8`, two `00265020` coordinate reads, `003A1960` compare); `00322630` — sets `1 << [unit+0xEA9]` in the global mask and kicks `002EA230` on first-set | `00317CBF` / `0031E6A3` / `0032264B` |
| legality gates | `00322A80` (456 B), `00327A10` (388 B) | `00322A80` — §10's unit/action legality (member walk `00236850`/`00236820` matching `[+0x698]`, `003230E0`, status masks `+0x3C`\|`+0x64`, `[+0x2C]` bit `0x40`/`0x80` arms); `00327A10` — `GambitConfig_ClassifyActionTargetPairCompatibility`, action/target pair loop calling `00322C50` on class `0x14`+, returns `0x1C`/`0x20` classes | `00322B43` / `00327A48` |
| reason / slot classifiers | `00318CD0` (869 B), `0032A320` (184 B) | `00318CD0` — the reason-code dispatcher: `0x14`-arm jump table, `0030E9C0` status→reason call with `0x8800223B`, `00317BC0`/`00317C80` legs; `0032A320` — `0032A230` record → 7-entry word list at `+2`, per-entry `bt [+0x10],i` + `0032A3E0` availability test | `00318D78` / `0032A38E` |

`0020E600`, `00322C50`, `0030E9C0`, `003230E0`, `00265020` and `0032A230` are shared callees with
other callers — deliberately not census members.

## 4. Data structures and formulas

```
BattleUnit
  +0x00   flags       bit 0x10 must be set or the unit cannot act        -> reason 2
  +0x698  ptr         battle record ("raw")
  +0x6A0  ptr         a byte block; [0] tested with masks 0x30 and 0x48  -> reason 2

battle record (raw)
  +0x05   byte        unit class selector: 0 and 1 take different gates
  +0x3C   u32         status layer 0   \  tested together as (l0 | l1)
  +0x64   u32         status layer 1   /
  +0x6C   byte        gil-cost layer 0 \  (l0 & 1) || (l1 & 1)
  +0x7C   byte        gil-cost layer 1 /

action definition record  =  actionTable + id * stride
  stride  = *(u16 *)(registry[02EBF138] + 8)
  +0x0C   u32         bit 0x80000 selects the wider status mask
  +0x1E   byte        == 1 also selects the wider status mask

statusMask = (rec[0x0C] & 0x80000) || (rec[0x1E] == 1) ? 0x8000221B : 0x8000201B
```

The two masks differ by `0x200`, so the wider one adds **one** status bit — **bit 9**.
*(An earlier revision said `0x2000` / bit 13. That was an arithmetic slip: `0x8000221B -
0x8000201B = 0x200`. Corrected 2026-09-02 — see section 10.)*

## 5. Call chain

```
UI menu build (16 sites)
  -> 0031EB20  BattleMenu_BuildCommandEntryList          (recursive)
       |
       +-> 002FFCF0  CheckActionAvailabilityReason
       |      +-> 00377C20  FieldData_GetActiveFieldRecordBit15
       |      +-> 00322C50  BattleEncodedId_IsValidForClass
       |      +-> 00253B90  null predicate over 01E0C2B8
       |      +-> 0030D9A0  BattleRuntime_GetMode0To5...        (mode 1 gate)
       |      +-> 0020E600  ImageAddress_ResolveRuntimePointer  (action table)
       |      +-> 0030E9C0  status-mask test
       |      +-> 0031A7B0  CheckGlobalCategoryDisableReason
       |      +-> 00306480  CheckUnitActionAvailability
       |      |      +-> 003060E0  CheckDefinitionCategoryAvailability
       |      |      +-> 00323EC0  BattleStats_HasRequiredLicenseForAction
       |      +-> 00303BD0  CheckExecutionResourceAvailability
       +-> 002F95D0  ComputeModifiedResourceCostAmount
       +-> 002F9820  UsesGilActionCostChannel
```

## 6. Modding notes

- **Availability is a cascade with a fixed order.** To make an action always available you must
  clear whichever gate fires *first*, not the last one you can see.
- **The License check is last.** `BattleStats_HasRequiredLicenseForAction` only runs once an action
  has passed status, id-class, category and global gates — so removing a License requirement will
  not, by itself, make an unavailable command usable.
- **The status mask lives in the authored action record.** `rec[0x0C] bit 0x80000` and
  `rec[0x1E] == 1` widen the mask from `0x8000201B` to `0x8000221B`; that is authored data, editable
  without patching code.
- **Ids `0x106`–`0x112` are special.** Thirteen consecutive actions are refused while the runtime is
  in **mode 1**. Whatever those thirteen are, they share a UI-driven restriction.
- **`0x113` and `0x95` are exempt** from the `0x24` gate that refuses everything else. Two actions
  the engine keeps available when it is shutting the rest down.
- **XIIOnline:** availability is computed **locally, per client, per list build**, from unit state
  plus authored tables. Two clients that disagree about a unit's status layers will build different
  menus. The reason code is not networked and should not be — synchronise the *inputs* (status
  layers, licences, resources), not the verdict.

## 7. What is not known

- [x] ~~What the reason codes mean on screen.~~ **ANSWERED 2026-09-02 — they never reach a screen.**
      All seven callers branch only on zero/nonzero; a byte scan finds no thunk, no address-taken
      reference and no indirect caller. Nineteen codes are computed and discarded. Section 11.
      **AI-1.**
- [x] ~~What actions `0x113`, `0x95` and the range `0x106`–`0x112` are. Naming them needs the
      authored action table at `0x02EBF138`.~~ **AI-2 ANSWERED 2026-09-11:** Dismiss, Dismount, and
      the thirteen Espers Belias–Zodiark — read from the action rows' `+0x34` name references into
      [the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md).
- [x] ~~What `0030E9C0` tests, and what the extra mask bit is.~~ **ANSWERED 2026-09-02** — it maps
      status bits to reason codes; the opt-in bit is **bit 9** (`0x200`), yielding reason `0xA`.
      Section 10. **AI-3.**
- [x] ~~The bodies of the three unread legs and the codes they return.~~ **ANSWERED 2026-09-02** —
      all three read; nineteen codes enumerated in section 10. **AI-4.**
- [x] ~~What the three resource pools are — `raw[0x4C]` (int16), `raw[0x4E]` (byte), and the global
      pool behind `FUN_00253690` with per-unit fallback `unit[0xE58]`. Gil is a flagged inference
      for the third.~~ **AI-8 ANSWERED 2026-09-12 (FABLE), by reference:** `+0x4C` is **live MP**
      (s16; written by `BattleStats_ModifyPrimaryResource` and the derived-state rebuild, [the battle-stats field map](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md),
      [where MP comes from](../../10-Status-Periodic-Terminal/where-mp-comes-from.md)) — reason `0x13` is "not enough MP"; `+0x4E` is **the Mist charge count**, the whole
      max-MP units the secondary pool `+0x06` holds, which a kind-5 / 6 action needs its row `+0x0A`
      of (reason `0x14`, `00303C4B`; Consume takes `max × +0x0A` from `+0x06`); the third is **gil**,
      confirmed 2026-09-03 from `0030EFBB`–`0030EFD8` (reason `0x15`); the struck question's `unit[0xE58]` is not a per-unit fallback pool but the gil cost reserved for the action in progress *(corrected 2026-10-02, OPUS: `+0xE58` is the gil cost reserved for the action in progress, not a purse: `0030EFC0` stores `00309060`'s result there, the refund `00300280` adds it back and the consume path `00305640` clears it; 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md:234; using-an-item-is-an-action-that-costs-an-item.md, "The action gil cost: 00309060")*, and its check runs only for a
      **party-table** unit — `raw[5] == 0` at `00303C6D` (AI-5). Section 11's inference stands as read.
- [x] ~~What `raw[5]` selects.~~ **AI-5 ANSWERED by AL-1 (2026-09-10; ledger closed 2026-09-12,
      FABLE):** the byte is **the high byte of the encoded definition id** — `0` for a unit built from
      the party table `02EBF130`, `1` for one built from the enemy table `02EBF120` and a spawn-record
      page — written whole into the stats record's `+4` word by `BattleStats_InitializeDefinitionRecord`
      (`0023AD8E`); [`../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md`](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) and [the unit-definition page](../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2. So the cascade's
      `raw[5] == 1` lines are "a unit from the enemy table" and `raw[5] == 0` "a unit from the party
      table" — not party / foe *allegiance* (which is why the same test appears in `PartyFollow_*`
      and `SpawnGroup_*`). *Earlier state:* **CENSUSED 2026-09-02** — tested at 104 sites across 82
      functions in 11 subsystems; two kinds, one type-keyed and one owner-keyed. The party/foe
      reading is **refuted**. **AL-1.**
- [x] ~~What `unit->[0x6A0][0]` masks `0x30` and `0x48` are.~~ *Ticked 2026-09-18 (FABLE): the naming below (2026-09-12) closes it.* **ANSWERED STRUCTURALLY 2026-09-02** —
      `+0x000` is an **8-bit lifecycle/eligibility flag byte**; `0x30` = bits **4|5** and `0x48` =
      bits **3|6**, each individually set, cleared and tested elsewhere. The individual bit
      meanings remain open (**AL-10**). Earlier note: —
      `unit + 0x6A0` is the **authored unit definition record** base (592 bytes, table pointer
      `0x0208E690`), so this reads **byte 0 of authored data**. See
      [`../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md`](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) §11. **AI-6.**
      *Named 2026-09-12 (FABLE, AL-10):* the byte is the spawn-keep entry's flag word and its
      writers name the bits — `0x30` = **`RANGE_RETIRE_INHIBITED` | category-4 mode**, `0x48` =
      **lifecycle point mode, positive | negative** ([the spawn-keep entry field map](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) §2.3).
- [x] ~~Whether `BattleMenu_BuildCommandEntryList`'s recursion is submenu descent or something else.~~
      **AI-7 ANSWERED 2026-09-12 (FABLE): not descent — a re-entry that swaps the party-member list
      for the actor-candidate list.** Read from `0031EB20` whole (§12).

## 12. AI-7 answered 2026-09-12 (FABLE) — what the builder's one self-call is

`BattleMenu_BuildCommandEntryList(ctx)` reads a **menu kind** from `ctx+0` (1–`0x23`, a jump table
at `0031EB52`), the acting unit's focus handle from `ctx+8`, the action id from `ctx+0x1C`, and fills
`ctx+0x50` (up to `0x200` entries of `{u32 id, u32 flags}`) with the count at `ctx+0x40` and a
default selection index at `ctx+0x44` (`-1` = none). The callers store the kind before calling —
`0xC` (`0027437B`), `0xF` (`0027B0C6`, `0027B6FE`), `0x10` / `0x12` (`002C4B7D`, `002C4B8F`), `0x14`
/ `0x1A` (`0035BF4B`, `0035BCC3`), `0x19` (`002C3960`, `002C47FF`), `0x22` / `0x23` (`0056A930`,
`0056AF65`, `0056B1D4`, `0056BD0F`) — and the only self-call is inside the case that kinds
**`0xC`–`0x10`** share (`0031F225`).

**That case, in order.** `BattleEncodedId_IsValidForClass(0x14, actionId, 1)` (`0031F232`) or return
`-2`; resolve the unit (`0031F242`) or `-2`; the functional predicate `(raw[0x3C] | raw[0x64]) &
0x80000003` with the field-record bit-15 override (`0031F268`–`0031F27D`); the availability cascade
`002FFCF0(actionId, unit)` — any reason code returns **`-4`** (`0031F28A`–`0031F298`). Then the
decision (`0031F29D`–`0031F300`):

```
if (raw[5] == 0 && kind not in {0xD, 0xE, 0xF})   -> ctx.kind = 0x1B; BuildCommandEntryList(ctx); ctx.kind = saved; return
if (raw[5] == 1 && kind != 0x10)                  -> the same
otherwise                                         -> the member list below
```

`raw[5]` is the definition-table byte (AI-5 above): a **party-table** unit with kind `0xC` or `0x10`,
or an **enemy-table** unit with kind `0xC`–`0xF`, re-enters with kind **`0x1B`** and never runs the
member list. **The member list** (`0031F31E`–`0031F52B`) walks the battle-unit slots
(`BattleUnit_GetSlotCount` / `GetBySlotIndex`, flag `0x10` = live) and classifies each with
`00322A80(unit, memberRaw, actionId, kind == 0xE, kind != 0x10, kind ∉ 0xD..0xF)`: `-1` skip; `0`
entry flag bit 1; `2` remember as the default; `3` default only if none yet; `4` write `ctx+0x44`
outright; the entry id is the member's handle (`+8`). Kind `0xF` alone lists instead the five roster
bytes at `+0x5A7E + 2i`, i = 4…8, of the registry-slot `02EBF190` record — each an index ≤ `0x27`
into its `0x1C8`-stride records, entry id = record byte `+4` (`0031F435`–`0031F525`).

**What kind `0x1B` builds** (the case kinds `0x1A`–`0x1C` share, `0031F54A`): for `0x1B` / `0x1C` the
same id-class and unit checks; then a per-kind rebuild of the **three actor-manager candidate
arrays** — `0046B4C0` (`0x1A`), `0046B870` (`0x1B`), `0046B690` (`0x1C`) — each walking the manager
records `00263FF0(0…2)` ([the slot pool and actor class](../../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md)) and filtering their registry entries by class nibble, `+0xE`
bits 6/7 and the predicates `002E9FE0` / `002EA6A0` / `00322490` / `00317D80` into the manager's
`+0x1F0` array and `+0x1F8` count (`0046B8D0`–`0046B9B7`). The list is then those three arrays in
order (`0031F5F7`–`0031F701`): each packed actor id resolves through
`ActorHandle_ResolveRegistryEntryByPackedId` → `ActorWork_GetBattleUnitRaw`, must pass
`003230E0(unit, raw, actionId, 1, 1)` — `BattleTarget_IsRelationshipClass0Or2` plus the action row's
`+0xC` bits 4 / 8 / 1 — and is appended as the packed id; then `002647E0(id)` bit 0 and the distance
`0031E630(actor)` elect **the nearest candidate as the default selection** (`0031F6A0`–`0031F6D8`).

So the recursion is a **redirect, not a descent**: the kinds `0xC`–`0x10` are "pick a party member for
this action", and when the actor is enemy-built (or the kind is `0xC` / `0x10` for a party member) the
same call is answered with kind `0x1B`'s "pick any compatible actor, nearest first". Nothing is pushed
or nested; the kind is swapped in, the list built once, and the kind restored. *Limits:* the kind
names are structural (which callers pass them, what each lists), not UI labels; the four filter
predicates in the rebuild are read only as calls.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The cascade, its order and its early returns | full disassembly of `002FFCF0` (479 B, 126 instructions) | 1 |
| Reason codes `2`, `4`, `0x24`, `0x2C` | the four `mov eax, imm` sites in `002FFCF0` plus the shared epilogue | 1 |
| `00306480` returns `0x2C` / `0x0F` / `0x10` / `0` | full disassembly (99 B), incl. `cmove ecx, edx` selecting `0x10` | 1 |
| Reason `0x10` is a License refusal | `00306480` calls `BattleStats_HasRequiredLicenseForAction` and returns `0x10` exactly when it fails | 1 |
| Ids `0x106`–`0x112` gated on runtime mode 1 | `sub ax, 0x106; cmp ax, 0xC; ja` then `call 0030D9A0; cmp eax, 1` | 1 |
| The engine-wide functional predicate appears here | `raw[0x64] | raw[0x3C]`, `test eax, 0x80000003`, `call 00377C20` | 1 |
| Two-layer convention at `+0x6C` / `+0x7C` | full disassembly of `002F9820` (51 B) | 1 |
| The action record is `base + id * stride` | `movzx ecx, word ptr [rcx+8]; imul ecx, r14d; add ecx, eax` | 1 |
| `0x02EBF138` is the action definition table | [`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) | 2 |
| `0031EB20` has 16 UI callers and is recursive | caller census over `edges.tsv` | 1 |

**Scope honesty:** three of the cascade's legs return codes this document passes through without
reading. The enumerated table is therefore **not** the complete reason-code set — it is the set
raised by the two functions that were read.

## 9. Related

- [`../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)
  — mode 1 gates thirteen action ids here, the first concrete semantics found for any mode
- [`../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md`](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md)
  — shares the `00253B90` predicate
- [`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
  — the action definition table this cascade indexes
- [`../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`](../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md)
  — the field predicate at the top of the cascade
- [`../Command-And-Action-Seam/native-command-seam.md`](../Command-And-Action-Seam/native-command-seam.md)
  — what happens once an available command is chosen

## 10. Falsification pass 2026-09-02 — the cascade completed, and one arithmetic error

**Attack chosen.** The document shipped with an explicit scope admission: three cascade legs returned
codes it passed through without reading, so its reason-code table was **known incomplete**. The
strongest attack on an admittedly incomplete table is to finish it — and see whether the completed
version contradicts what was already written. It contradicted one thing.

### CORRECTED: the two masks differ by bit 9, not bit 13

The document said *"the two masks differ by exactly `0x2000`, so the wider one adds one status bit —
bit 13."* That is an arithmetic slip:

```
0x8000221B - 0x8000201B = 0x200   ->  bit 9,  not bit 13
```

Bit 13 is in **both** masks. The bit an action opts into via `rec[0x0C] & 0x80000` or
`rec[0x1E] == 1` is **bit 9**, and section 10's mapper shows bit 9 yields reason **`0xA`**.

### `0030E9C0` is a status-bit to reason-code mapper

Read in full (117 B):

```c
status = raw[0x64] | raw[0x3C];              /* the two-layer pair again */
if ((mask & status) == 0) return 0;          /* nothing masked -> available */

if (mask bit 9  && status bit 9 ) return 0xA;
if (mask bit 3  && status bit 3 ) return 7;
if (mask bit 4  && status bit 4 ) return 8;
if (mask bit 13 && status bit 13) return 0xB;
if (mask bit 5  && status bit 5 ) return 9;
if (mask bit 27 && status bit 27) return 0xC;
return 6;                                    /* masked by some other bit */
```

**This is the function that turns a status ailment into a specific refusal**, and the test order is a
priority order. Decomposing the two masks:

| Mask | Bits | Reachable reasons |
|---|---|---|
| `0x8000201B` (base) | 0, 1, 3, 4, 13, 31 | `7`, `8`, `0xB`, and `6` for bits 0/1/31 |
| `0x8000221B` (wide) | adds **9** | also `0xA` |

**Reasons `9` and `0xC` cannot fire from this call site at all** — bits 5 and 27 appear in neither
mask. `0030E9C0` is a general mapper; the battle menu exposes only part of it. Another caller with a
different mask would reach the other two.

### The completed reason-code table

| Code | Raised by | Meaning as read |
|---:|---|---|
| `0` | — | **available** |
| `2` | `002FFCF0`, five paths | unit not in a state that can act |
| `4` | `002FFCF0`; also `0031A7B0` | id invalid for class `0x14`; global category disabled |
| `6` | `0030E9C0` | masked by a status bit with no specific reason (bits 0, 1, 31) |
| `7` | `0030E9C0` | status **bit 3** |
| `8` | `0030E9C0` | status **bit 4** |
| `9` | `0030E9C0` | status **bit 5** — *not reachable from this cascade* |
| `0xA` | `0030E9C0` | status **bit 9** — only when the action opts in |
| `0xB` | `0030E9C0` | status **bit 13** |
| `0xC` | `0030E9C0` | status **bit 27** — *not reachable from this cascade* |
| `0x0F` | `00306480` | definition category unavailable (**collapses** four inner codes) |
| `0x10` | `00306480` | **no License for this action** |
| `0x12` | `00303BD0` | `FUN_003037A0` refused the action |
| `0x13` | `00303BD0` | **16-bit resource pool** `raw[0x4C]` below the cost |
| `0x14` | `00303BD0` | **8-bit resource pool** `raw[0x4E]` below the cost |
| `0x15` | `00303BD0` | a **global** pool *and* ~~a per-unit pool~~ `unit[0xE58]`, the gil cost already reserved for the action in progress, both below the cost *(corrected 2026-10-02, OPUS: `+0xE58` is the gil cost reserved for the action in progress, not a purse: `0030EFC0` stores `00309060`'s result there, the refund `00300280` adds it back and the consume path `00305640` clears it; 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md:234; using-an-item-is-an-action-that-costs-an-item.md, "The action gil cost: 00309060")* |
| `0x24` | `002FFCF0` | global gate; all ids refused except `0x113` and `0x95` |
| `0x2C` | `002FFCF0`, `00306480` | null unit; or ids `0x106`–`0x112` in runtime mode 1 |

Nineteen distinct codes, occupying `0`–`0x15` almost contiguously plus `0x24` and `0x2C`. That
density is what an authored message-id enum looks like.

### The resource leg, read

```c
if (unit == NULL)                                   return 0;
if (FUN_003037A0(unit, id))                         return 0x12;
if ((int16)raw[0x4C] < FUN_00309110(unit, id))      return 0x13;
if ((uint8)raw[0x4E] < FUN_00308FF0(unit, id))      return 0x14;
if (raw[5] == 0) {
    c = FUN_00309060(unit, id);
    if (c && FUN_00253690() < c && unit[0xE58] < c) return 0x15;
}
return 0;
```

Three separate pools with three different widths: a **signed 16-bit** value, an **unsigned byte**,
and a **global** amount with a per-unit fallback. The third is gated on `raw[5] == 0`, the same class
selector the cascade uses.

**An inference, flagged as one:** a party-wide pool checked before a per-unit one, in a system whose
menu builder also calls `BattleUnit_UsesGilActionCostChannel`, reads naturally as **gil**. Nothing
here names it, and the 16-bit and byte pools are not named either. **AI-8.**
*Closed 2026-09-12 (FABLE):* gil was confirmed from the consumer side on 2026-09-03; the 16-bit pool
is live MP and the byte pool the Mist charge count ([the battle-stats field map](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md)) — the checklist entry in §7.

### Two-layer convention, thirteenth sighting

`0030E9C0` opens with `raw[0x64] | raw[0x3C]` — the same status pair, in a fourth distinct function
family. The convention is now attested at three offset pairs across status, rewards and action cost.

### What this pass did not settle

`FUN_003037A0`, `FUN_00309110`, `FUN_00308FF0`, ~~`FUN_00309060`~~ and `FUN_00253690` are unread *(answered for `00309060`: see using-an-item-is-an-action-that-costs-an-item.md, the section "The action gil cost: 00309060" - the gil cost reason `0x15` compares; 2026-10-02, OPUS)*, so the
*cost* side of the resource check is still opaque — only the comparison shape is known. **AI-4 is
closed** (the codes are enumerated); **AI-3 is largely answered** (the mapper is read and the opt-in
bit identified); **AI-1 remains fully open** — nothing here maps a code to on-screen text.

## 11. Falsification pass 2026-09-02 (second) — who actually consumes this

**Attack chosen.** The first pass finished the reason-code table. It never asked the obvious next
question: **who reads those codes?** A table of nineteen distinct values is only worth nineteen
values if something distinguishes them.

### CORRECTED: this is not a UI system

The document's frontmatter said *"consumed almost entirely by UI"*. The caller census says the
opposite — of **seven** callers of `002FFCF0`:

| Caller | Subsystem |
|---|---|
| `BattleAction_CheckCurrentActionInterruptReason` (`002FFB60`) | CombatAction |
| `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) | **CombatAI — gambits** |
| `BattleUnit_SelectAndCommitNextAction` (`00305AB0`) | **CombatAI** |
| `Battle_ProcessActionTarget` (`00307300`) | CombatAction |
| `FUN_0030DB70` | CombatAction |
| `FUN_00317BC0` | CombatAction |
| `BattleMenu_BuildCommandEntryList` (`0031EB20`) | UI — **the only one** |

**Six of seven are combat.** The menu is a *client* of this system, not its owner, and section 1 has
been rewritten to say so. The interesting consequence is the one now in the headline: the Gambit AI
and the player's menu are gated by the same function, so they cannot disagree.

### AI-1 ANSWERED, and not the way it was posed

**AI-1 asked where the reason codes become on-screen text. They do not. Nothing consumes them.**

Every one of the seven call sites does the same thing:

```
call 0x2ffcf0
test eax, eax
je / jne          <- branch on zero vs nonzero, and nothing else
```

Verified individually at `0031F28F`, `00301604`, `00305B0E`, `0030739D`, `0030DBC3`, and in the two
remaining callers. The UI caller is the most explicit: on any nonzero code it returns a flat
`0xFFFFFFFC` (`-4`), discarding which refusal it was.

**The call set is complete.** A byte scan of `.text` finds **7 `E8` call sites, 0 `E9` thunks, 0
occurrences of the function's address as a qword anywhere in the image, and 0 RIP-relative `LEA`s of
it** — so there is no indirect caller, no vtable slot, and no thunk hiding a consumer. *(That scan
was run because this database has already been bitten twice by an edge list that sees `E8` but not
`E9`, and by censuses that miss address-taken references.)*

So the engine computes **nineteen distinct refusal reasons and then throws every one of them away.**
The distinction between "no License", "not enough MP" and "Stopped" exists in the code and reaches
nothing.

**Two readings, neither asserted.** The codes may be vestigial — a facility that once drove a
message and no longer does. Or a debug build may consume them. Nothing in the retail image decides
between those, and this document does not.

**What it does settle:** anyone hoping to surface "why is this greyed out" to a player has to add
the consumer, not find it. The value is computed and available at every call site; nothing reads it.

### Not changed

The cascade, its order, the nineteen codes and the mask decomposition all stand — they were read
from the bodies and this pass did not touch them. What changed is **who the system is for**.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

- **Presentation — CLIENT and SERVICE.**
  - Small accessors this page cites are read by presentation code. The 21-byte `00263FF0` is
    read by five Presentation bodies of 511–4,782 bytes. `002E9FE0` is read by a 958-byte body, and `002EA6A0` by the
    714-byte render-cluster body.
  - `Battle_ProcessActionTarget` asks `BattleUnit_ComputePresentationSuppression…`, which in turn reads the battle
    runtime mode (`0030D9A0`).
  - **The battle menu's command list tests visibility.** `BattleMenu_BuildCommandEntryList` (`0031EB20`) and `00322A80`
    call `BattleUnit_TestActorViewFrustumAtCurrent…`. `00317D80` calls `WorldActor_TestBoundsAgainstViewFrustumAtPosition`.
    Which reason code a failed frustum test yields is not read here.
  - `BattleUnit_ComputePartyBattleStance` reads the 12-byte `00253B90`.
  - The permission bit is read by four presentation functions.
- **Movement — CLIENT and SERVICE.**
  - `00263FF0` is read by two movement bodies, of 702 and 2,026 bytes.
  - `002E9FE0` is read by two 117-byte helpers.
  - The battle runtime mode is read by `BattleRuntime_GetModeDependentBaseDistance` and a 448-byte locomotion helper.
  - Two locomotion bodies ask the id-validity query, and five movement bodies read the permission bit.
  - `Battle_ProcessActionTarget` steers the actor.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — SERVICE and CLIENT.** Cited functions call `BattleFormula_ResolveTargetResult`, `BattleFormula_ApplyTargetResult`, `BattleFormula_MapOutcomeToTargetEntryCode`, `BattleStats_FindOwningBattleUnit` and `BattleStats_GetByBattleSlotIndex`. They are called by `BattleStats_RebuildEffectiveStatsAndAffinityState` and `BattleStats_ModifyHPAndProcessLethalState`.
- **PlatformOnlineAchievements — SERVICE.** `00309EC0` (the BattleEncodedId gate, §3a's
  `00317C80` ranking leg) is also called by `00315E90` — a shared callee reaching into the
  achievements layer, not a command-availability input.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Many of this page's subjects are small shared accessors (the unit table, the actor-manager record `00263FF0`, the actor position, the focus handle, the id-class test); a layer that only calls one of those is recorded as such.*

**CombatAI — CLIENT and SERVICE (40 edges).** `AiOrder_EvaluateAndResolveActionTarget` `003014C0` and `BattleUnit_SelectAndCommitNextAction` `00305AB0` call the availability check `002FFCF0`; the combat frame `00308610` calls the interrupt check `002FFB60`, the null predicate `00253B90` and `00305AB0`; `003014C0` calls `AiOrder_CheckActionPreconditions` `00301830`, `AiOrder_EvaluateTargetSelector` `00301AD0`, `AiOrder_SelectFinalTargetFromCandidates` `003087E0` and `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` `0030F130`, and is called by `BattleUnit_TrySelectAndCommitAiOrderFromSet` `00305CC0`; `00301AD0` calls `003093D0`, `00309EC0`, `0031C500`, `00236820`, `00236850` and `00322C50`; `Battle_ProcessActionTarget` `00307300` calls `BattleEnmity_ApplyActionParameters` `003216E0`; the menu builder `0031EB20` calls `GambitConfig_ClassifyActionTargetPairCompatibility` `00327A10`; and the enmity bodies (`BattleEnmity_WriteForCombatantId` `00321850`, `BattleEnmity_PropagateToPerceivingFoes` `003219D0` and five more), the perception cache (`BattleUnit_RebuildPerceptionCandidateCache` `003247F0`, `00324F20`) and `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` `00327CB0` call the unit-table and id-class helpers. The AI layer is the cascade's real consumer, as section 11 found: its action selection asks `002FFCF0` before it commits, and the menu builder asks the gambit layer whether an action and target pair is compatible; the enmity, perception and gambit-preset bodies only share the unit-table and id-class helpers.

**Gameplay — SERVICE and CLIENT (38 edges).** The cascade calls ownerless combat helpers throughout: `002FFCF0` calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0` and `BattleEncodedId_IsValidForClass` `00322C50`; `003060E0`, `003093D0`, `0030DB70`, `0031A7B0`, `00323EC0`, `00327A10`, `0032A3E0` and `0031EB20` call `00322C50`; `003037A0`, `003060E0` and `0031EB20` call `BattleEncodedId_QueryMode0Positive` `0030B0E0`; `00317BC0`, `00317C80` and `0031EB20` call `BattleEncodedId_DispatchQueryMode0Value` `00309EC0`; `003014C0` calls `WorldActor_GetDefinitionByte12OrMinus1` `002E9C00` and `BattleTargetBuffer_ResetPreservingFlag0` `00316CF0`; `00307300` calls `BattleUnit_SubmitResultReactionMode` `00328480` and `BattleUnit_DispatchActorPresentationEvent` `003299B0`. In the other direction the definition-resolution runtime `0031C5D0`, `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0`, `BattleRuntime_GetModeDependentDistanceThreshold` `00309A90`, the target-focus geometry `0031ADB0`, `BattleAction_FindApproachGeometryAroundTarget` `00339630`, `Battle_EmitReactionPresentationForSlot` `003176E0`, `ActorHandle_GetPrimaryFormulaResourceByte26` `00321380`, `BattleUnit_UpdateEngagementStateFlag` `00307D10`, `BattleUnit_CollectMappedFourSlotUnitsByFlags` `0030A8A0` and `BattleUnit_HasRelationshipClass2PlusInSlotMask` `0030C210` call the page's shared accessors (`00322C50`, `0030D9A0`, `00253B90`, `00263E30`, `00265020`, `003590D0`, `00236820`, `00377C20`). Gameplay is the census's domain label for ownerless combat helpers: the reason cascade is built from their id-class tests and mode getter (reason 4 is `00322C50` failing class `0x14`, reason `0x2C` is mode 1), and the other callers use the same accessors for targeting geometry and presentation.

**Items_Equipment_Shops_License — SERVICE and CLIENT (32 edges).** The per-unit leg `00306480` calls `BattleStats_HasRequiredLicenseForAction` `00323EC0`, which calls `BattleStats_HasLicensePrerequisiteForRequirement` `00323BB0` and `BattleStats_CountLicenseBits00To17` `00324020`; `003060E0` calls `Inventory_QueryEncodedItemDiscoveryBit` `00309B60`. The cost helper `00308FF0` is also called by `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` and `BattleStats_ComputeLicenseDerivedRank` `00324100`; the shared accessors are called by the inventory and equipment bodies `002FD530`, `002FD880`, `Shop_CommitPurchaseItemAndGil` `002FEEB0` and `Shop_CommitSaleItemAndGil` `00310870` (gil), `Equipment_CheckItemEligibleForSlot` `00317930`, the `BattleIdClassD_*` flag bodies (`0030B180`, `0030B4B0`, `0030B510`, `0030B570`, `0030B630`), `BattleStats_HasRequiredLicenseForEquipment` `00323C60`, `BattleStats_CheckLicenseNodeAcquireReason` `00323D10`, the equipment setters `0031A410`, `0031A510`, `0031A630`, `0031A300`, `003096F0`, `00325F40`, `00309FB0` and `0030FD10`. The License Board is part of availability: an action whose licence the unit lacks is refused through `00323EC0` on the per-unit leg; the other licence, equipment and shop bodies call the same id-class, gil and owner helpers for their own checks.

**Party — SERVICE and CLIENT (37 edges).** `002FFB60`, `0030DB70` and the menu builder `0031EB20` call `BattleUnit_ResolveByFocusHandle` `0031B7E0`; the reason dispatcher `00318CD0` calls `BattleUnit_GetPartyLeader` `003272A0`; the manager predicates `0031E630` and `00322490` call `PartyFocus_GetCurrentPackedActorHandle` `003590D0`. The party roster bodies call the page's accessors in turn: `PartyConfiguration_ReconcileRosterFromCurrentSelectors` `003261D0`, `PartyConfiguration_SetSelectorsAndReconcileRoster` `003273D0`, `PartyFocus_SelectAndRequestDefaultActor` `00326500`, `PartyFocus_TryGetCurrentActorWorldPosition` `00359150`, `PartyRoster_AssignActorToSlot` `00269C70`, `PartyFocus_IsCurrentPackedActorHandle` `003273B0`, nine roster-selector bodies that call `00322C50` (among them `003170E0` and `00329080`), and `00303CC0`, `00303F00`, `00304180`, `003272F0`, `00327270` and `00263770`. The command menu asks about the focused party member and the leader, which is what the party layer's focus and leader getters provide; the roster and focus bodies call the same unit, position, mode and id-class accessors for their own roster reconciliation.

**RNG_Random_Selection — SERVICE (2 edges).** `AiOrder_EvaluateAndResolveActionTarget` `003014C0` calls `BattleData_ResolveWeightedId` `00308EC0` and `RNG_SharedGameplayLCG_NextU32` `00328370`. The AI's target resolution takes weighted and random picks from the shared gameplay LCG; availability itself (`002FFCF0`) draws nothing.

**Rewards_Progression_Economy — SERVICE and CLIENT (11 edges).** The cost leg `00303BD0` calls `GameState_GetGil` `00253690`: reason `0x15` is returned when the action's gil cost exceeds both the party's gil and ~~the unit's own pool~~ the cost already reserved for the unit's action in progress at `+0xE58` *(corrected 2026-10-02, OPUS: `+0xE58` is the gil cost reserved for the action in progress, not a purse: `0030EFC0` stores `00309060`'s result there, the refund `00300280` adds it back and the consume path `00305640` clears it; 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md:234; using-an-item-is-an-action-that-costs-an-item.md, "The action gil cost: 00309060")*. The accessors are also called by `GameState_AddGilClampedAndNotify` `003004B0`, `003F4AA0`, `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280`, `Loot_FindOverlappingPickupIndex` `002FB150`, `Loot_RollAdditionalItemChance` `00318510`, `Loot_FindNearestActivePickupPosition` `00319850`, `Reward_ComputeExperienceForRecipient` `002F8BB0` and `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650`. Gil is an availability input through `00303BD0`; the reward and loot bodies use the same gil, position, id and owner accessors for payouts.

**Script_VM_Native_Bridge — CLIENT, OUT-OF-SCOPE (85 edges).** Script-side bodies call the page's actor accessors: `WorldActorScriptVM_InterpretBytecode` `0025E4C0`, `VMNativeCommand_ExecuteLifecycle` `002621D0`, `ScriptVM_WaitList_HasAnyActorChannelActive` `00267420` and `ScriptVM_WaitList_HasAnyActorResourceEntryActive` `002674B0` call `ActorManager_GetRecordByOrdinal` `00358940`; and native verb bodies such as `0033F7F0`, `0033FD60`, `00345CD0`, `00350DD0`, `003516E0` and `0050E060` (85 edges in all) call `00263FF0`, `Actor_GetWorldPosition` `00265020`, `002EA6A0`, `00358940`, `003590D0` and `00377C20`. Scripts address actors through the same manager record, position, predicate and focus accessors the menu's candidate enumeration uses (section 12); none of those verbs asks for command availability.

**Spawn_Encounter_Lifecycle — CLIENT, OUT-OF-SCOPE (5 edges).** `Spawn_CountActiveCapTrackedActors` `00308D90` calls `00236820` and `00236850`; `Spawn_TrySelectCandidatePosition` `00234AF0`, `Spawn_ValidateCandidateDistanceToPlayers` `00234DA0` and `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` call `Actor_GetWorldPosition` `00265020`. The spawn layer counts units and measures distances with the same unit-table and position accessors; it does not consult availability.

**Status_Periodic_Terminal — CLIENT (12 edges).** `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860` calls `00263E30` and `0031B860`; `002F9400`, `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `0030F690` and `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` call `0031B860`; `0030E130`, `0030FED0` and `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` call `00322C50`; `0030E360`, `0030F690` and `00310DB0` call `00377C20`. The status layer shares the owner resolver, id-class test and field predicate with the cascade; the cascade reads status words directly (reason `0x24`, and the `0030E9C0` status-to-reason mapper) and does not call these bodies.

**World — CLIENT (4 edges).** The actor-manager frame bodies `0025E400` and `002623A0` call `ActorManager_GetRecordByOrdinal` `00358940` and `PartyFocus_GetCurrentPackedActorHandle` `003590D0`. The world frame walks actor-manager records and the focus handle with the accessors this page cites; it is not an availability consumer.

**WorldAreaField — SERVICE and CLIENT (10 edges).** `002FFCF0`, `003014C0`, `00305AB0`, `00307300` and the mode getter `0030D9A0` call `FieldData_GetActiveFieldRecordBit15` `00377C20`, and the menu builder `0031EB20` and the target-status evaluation `00322A80` call its five-byte thunk `00313F60`; `00377C20` calls `WorldTransition_GetActiveOrPendingFieldId` `003148F0` and is called by `BattleSystem_InitializeAreaState` `002342F0`; the conditional battle-id resolution `00576A50` calls `00309EC0`. The area's action-permission bit is an input to availability (`002FFCF0` refuses a unit whose status words carry any of the three bits it tests unless the bit is set, and `0030D9A0` folds the bit into the battle mode); area setup reads it too.

## SWE2-EC7-19 update (2026-05-15) — `00322490` angle-wrap + vector submit fragment

`00322490` (203 B) is one of the manager predicates this page names (`002E9FE0`/`002EA6A0`/`00322490`/`00317D80`): `003590D0` (`003224AC`) yields the index, `test [02089340],0x10` (`003224B1`) gates the whole body — clear returns 0 (`00322541`); set, `003588B0` resolves the index to `rdi` and a null exits (`003224C0`..`003224CB`). When `rcx`'s record is non-null, `00263E30(rcx)` (`003224D5`) must return a record with `byte[+0]&0x10` and `002FFED0(rdx=0, r8d=3)` must succeed (`003224DF`..`003224F4`) or it returns 0. The compare half then reads two three-dword fields — `00265020(rdi, rsp+0x30, rsp+0x34, rsp+0x38)` and `00265020(rcx, rsp+0x20, rsp+0x24, rsp+0x28)` (`003224F6`..`0032251F`) — and returns `003A1960(&rsp+0x30, &rsp+0x20) <= [00D1081C]` via `comiss`/`setbe` (`0032252E`..`0032253C`): the bounded-distance availability test the manager's callers consume.

## SWE2-EC7-26 update (2026-09-18) — `003093D0` gated row-word fetch

`003093D0` (112 B) gates on `00322C50(0x14, bx)`, resolves the
`02EBF138` pool row `word[+8] * bx + 0020E600([+0xC])`, requires
`byte[+0x1E] == 3`, and returns `word[+0x22]` — `0xFFFF` on any gate
failure. The reason-code word the availability ladder publishes.
Interior anchor `00309425` (the `+0x1E` check).

## SWE2-EC7-37 update (2026-09-19) - `003060E0`

`003060E0` (595 B) is a command-availability body - `02EBF138` octet/`02EBF130` triple flag fields, `0020E600` sextuple plus `00322C50`/`00309B60`/`0031B860`/`003037A0`/`0030B0E0`. Interior anchor `0030610D` (a `00322C50` call).

## SWE2-EC7-50 update (2026-09-19) - `00317BC0`

`00317BC0` (183 B) is a CombatAction body - `002FFCF0`/`00306480`/`003093D0`/`00309EC0`/`0030E9C0`. Interior anchor `00317BEC` (a `002FFCF0` call).

## SWE2-EC7-60 update (2026-09-19) - `0046B4C0`

`0046B4C0` (158 B) is the `0x1A` array walker the command-availability page names - `00263FF0`/`00358940`/`0046BAC0`. Interior anchor `0046B4E2` (a `00263FF0` call).


## SWE2-EC7-74 update (2026-09-19) - `0030E9C0` flag-pair reason decoder measured

`0030E9C0` (117 B) is the reason-code decoder the availability bodies
call: `eax = [+0x64] | [+0x3C]`; `(edx & eax) == 0` returns 0, then a
priority ladder maps shared bits - bit 9 -> 0xA, bit 3 -> 7, bit 4 ->
8, bit 13 -> 0xB, bit 5 -> 9, bit 27 set -> 0xC else 6 - the two-flag
intersect that produces the denial reason.
Interior anchor `0030E9CD` (the first `bt edx, 9`).

## SWE2-EC7-94 update (2026-09-20) - `003230E0` measured

`003230E0` (262 B) is the four-flag availability predicate
`0031EB20` and `00322A80` run: two `0020E600` resolves on the
`02EBF114`/`02EBF131` globals' `+0xC` ids build `ebp` as
`word[+8]*bx + eax` (0 when either resolve fails), the
`00236850`/`00236820` loop finds the slot whose `+0x698` matches
the argument record and `0030BB10` validates the pair, then the
return is composed from the `+0xC` flag byte - bit 2 with the
`r14d` gate, bit 3 with the stack arg, bit 1 against
`[r15+0x698]==rsi` - each arm returning 1 or falling through to 0.
Interior anchor `00323116` (the first `0020E600` call).

`0031C500` (49 B) is the masked pair test on an availability row: null `rcx`/`rdx` returns 0, else `003872D0(rcx, rdx, 0, 0)`'s answer is AND-ed with `dword[rdx+0x64] | dword[rdx+0x3C]` - the two-field mask the command-availability and action-dispatch callers apply to the query result.

Interior anchor `0031C516` (function `0031C500`).

`0032A230` (239 B) is the ranged row scan over `02EBF020`: `*r8` presets 0, `esi` bounds against the `[+0x1C]`-resolved table's `dword[0] - 1`, the scan runs rows `dword[esi-1]+4`-indexed `ebx` to `dword[esi]+4`-indexed `esi` comparing each row's `word[0]` to `bpl`, and the first match writes its address to `*r8` - returns 1 on miss/out-of-range, the reason-code range search the availability callers share.

Interior anchor `0032A303` (function `0032A230`).

`002F8D60` (234 B) is the three-byte matcher `0030DB70` runs on `rcx`: a non-negative `01EEBAF0` short-circuits to the `022BE930[idx*2]` u16 row; otherwise it scans `edi = [02EBF0A0]+4 - 1` records downward, resolves each row's base twice through `0020E600` (offset `u16[+8] * edi` over the second resolve), and accepts when the query's first three bytes each pass `>=` against record bytes `+1`/`+2`/`+3` - a match returns `*record`, exhaustion `-1`

Interior anchor `002F8DF3` (function `002F8D60`).

### FABLE 2026-09-30: what the override short-circuit can return (OV-42)

*Consumed from ASTRA's [`special-action-override-domain`](../../_experiments/evidence/special-action-override-domain/README.md)
(SWE2-AUDIT-SPEC `_index/candidates/auditspec-review-astra-special-override-domain-0930/REVIEW.md`, ACCEPT-WITH-NARROWING) and
[`special-action-override-label-binding`](../../_experiments/evidence/special-action-override-label-binding/README.md)
(`_index/candidates/auditspec-review-astra-special-override-labels-0930/REVIEW.md`, ACCEPT); FABLE record
[`astra-returns-fable-0930`](../../_index/candidates/astra-returns-fable-0930/README.md). Static only.*

- **The words.** `002F79E0` copies 16 bytes from `.rdata` `00D0F9E0` to `022BE930`: eight u16 words 241, 231, 234, 237,
  229, 228, 227, 226. `022BE930` lies in the `.data` virtual tail, so it is zero until that copy; its only writer is the
  copy and its only address-taking reader is `002F8D74` above. `002F79E0` has one direct caller, `001D03DC` in `001D0390`.
- **The index.** `01EEBAF0` has one writer, the setter `002F7A00`, called once (from the debug console's override arm),
  and one reader, `002F8D66` above. Its file value `FFFFFFFF` is only a file value, not live initialisation.
- **The state behind the index.** The owning object's DWORD `+0xAE0`: the constructor `001CCB20` stores QWORD `0x2710` at
  `+0xADC` (`001CCC06`), so `+0xAE0` is 0 at that store; the console arm (its instruction span is in the ASTRA packet)
  steps the state left or right, saturating inside 0..8, and passes state - 1 to the setter. A state in 0..8 therefore gives an index in -1..7,
  and the short-circuit returns one of the eight words, none of them in 511..534.
- **The labels.** The straight-line initializer `001D03E1`..`001D04D1` writes nine NUL-terminated ASCII labels into
  32-byte slots at `+0xAE4 + 32*state` (`+0xAE4`..`+0xC03`): OFF, Black Hole, Luminescence, Ark Blast, Whiteout,
  Windburst, Torrent, Cataclysm, Inferno. The debug formatter's internal item 182 (not a script verb or action id)
  sign-extends `+0xAE0`, shifts it by 5, adds `+0xAE4` and passes that label as the third `%s` of
  `"%s%s %s "`, with no clamp. So state k >= 1 pairs label k with word k - 1 (Black Hole 241, Luminescence 231, Ark Blast
  234, Whiteout 237, Windburst 229, Torrent 228, Cataclysm 227, Inferno 226), and state 0 is OFF with index -1 and no word.

**The arm is not a sanitizer** (the review's narrowing). A corrupt state 9 stays 9 on the increment input and writes
index 8, past the eight words; on the decrement input it becomes 8 (index 7). A state of -1 stays -1 on the decrement
input and writes index -2, which `002F8D60` sends to its negative-index record scan. State 9 would also make the formatter
address `+0xC04`, past the nine label slots.

**One constructor write that does not reach `+0xAE0`** *(FABLE 2026-09-30, from ASTRA's reviewed SOFTEDGES packets; record [`astra-returns-softedges-fable-0930`](../../_index/candidates/astra-returns-softedges-fable-0930/README.md))*: the same constructor binds the PhyreText `softEdges` parameter into its object's `+0x120`..`+0x127` (8 bytes, the shipped definition), and no definition in that asset is large enough to reach `+0xAE0`; see [the render parameters page, 8e](../../17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md). This excludes one route only, for the unchanged shipped asset; it proves no load.

**Limits kept.** Same-object pairing of the constructor, the console arm and the formatter (whose `r15` is reused in two
other branches), and the absence of other writes to the array, the index or `+0xAE0`, are premises. Writer, alias and
lifetime closure is OPEN: nine image-wide disp32 stores overlap `+0xAE0`..`+0xAE3`, four of them on unidentified objects
(`00184FBA`, `001881BF`, `006DD2D0`, `007049B8`). The labels are original debug display names; they certify neither a
combat effect, player presentation nor normal selection. Unwritten slot padding is unknown, and the constructor's other
calls are assigned no effect. The external EXP190 replay's stubs are not live initialisation. Other action-id producers,
natural action selection and whole OV-42 stay OPEN.

### FABLE 2026-10-02: which action rows the special-sequence path could turn into a rejected request (OV-42)

*Consumed from four ASTRA packets after SWE2-AUDIT-SPEC review (records committed in `2e88eceef`):
[`ov42-special-action-preconditions`](../../_experiments/evidence/ov42-special-action-preconditions/README.md)
(`_index/candidates/auditspec-review-astra-ov42-action-preconditions-0930/REVIEW.md`, ACCEPT-WITH-NARROWING, narrowings applied),
[`ov42-class20-action-admission`](../../_experiments/evidence/ov42-class20-action-admission/README.md)
(`_index/candidates/auditspec-review-astra-ov42-class20-admission-0930/REVIEW.md`, ACCEPT),
[`spattack-native-word-remap`](../../_experiments/evidence/spattack-native-word-remap/README.md)
(`_index/candidates/auditspec-review-astra-spattack-remap-0930/REVIEW.md`, ACCEPT) and
[`action-selector-local-exclusions`](../../_experiments/evidence/action-selector-local-exclusions/README.md)
(`_index/candidates/auditspec-review-astra-action-selector-exclusions-0930/REVIEW.md`, ACCEPT); FABLE record
[`astra-returns-ov42-fable-1002`](../../_index/candidates/astra-returns-ov42-fable-1002/README.md). Static only.*

- **The path.** `0030CBE0` reads the presentation slot's u16 action id (`0030CC25`). It checks the id as class `0x14`
  (`0030CC32`), builds the row pointer from the same word (`0030CC7A`..`0030CC81`) and passes the pointer to
  `0030CE10` (`0030CD99`).
  - `0030CE10` drops a row whose `+0x0C` bit 30 is clear (`0030CE93`/`0030CE9A`). Otherwise it calls `00306BD0`
    (`0030CF0D`).
  - `00306BD0` hands `00309230`'s result to `0032FC30` as group 3 (`00306C4D`..`00306C56`). That result is the row's
    `+0x24` word. For row `0x113` (decimal 275, `003092B4`) it is instead an entry of a 13-entry table, indexed by the
    raw record's type byte minus `0x1B` with no bound check (`003092D6`..`003092DB`).
  - Group 3's index is `4w+1`. The owner path narrows it to a WORD ([the indexed-source
    page](../../02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md), FABLE
    2026-09-30 subsection).
- **The rows.** The nine shipped tables are one table of 543 rows of 60 bytes.
  - No word other than FFFF gives a negative narrowed WORD. This is the WORD sign only. The ten bit-15 words
    32775..32907 (rows 111-123, 246-261, 427-435 and 440) narrow to positive WORDs, and none of their rows has bit 30.
  - FFFF narrows to the WORD -3. FFFF with bit 30 occurs on row `0x113` and on rows **511..534**. All of rows 511..534
    have `+0x1E` 7.
- **What does not exclude 511..534.**
  - Class `0x14` accepts 0..542. The count is `[02EBF138]+4` = 543 (`00322F84`, `0032302C`..`0032303B`).
  - The D0..F1 refusal (`0030CEC2`..`0030CEFE`) applies only while the special-sequence state `022C2160` is 5 or 6.
    Rows 511..534 lie above `0xF1` in any case.
  - The queue remap. The queue cell `022C2178` holds `word - 0xD0` (`0030DBDA`, `0030DC7B`, `003068CA`) or -1, and
    its reader `00309C00` consumes the value. The script adapter `0030EEA0` adds `0xD0` back as a 16-bit add
    (`0030EEB2`) before `0030CFB0` stores the word into the slot's `+0x1C` (`0030D14F`). Rows 511..534 queue as
    303..326 and decode unchanged. Only `0xCF` and FFFF read as unavailable, so the remap has no universal inverse.
- **What does exclude them, on two legs only.**
  - (a) `0030DB70`'s record arm. If the unit's raw record (`002FFD05`) has byte `+5` = 0, `003060E0` returns 5 for
    `+0x1E` 7 (`00306300`). `00306480` turns that into `0x0F`, `002FFCF0` refuses, and `0030DB70` returns at
    `0030DBC5`, before its stores. A nonzero `+5` bypasses the test (`0030612F`).
  - (b) Its null-record arm, when the override `01EEBAF0` is negative. The matcher above then returns a byte 0..255
    (`002F8E36`) or -1 (`002F8E28`). Those queue as -208..47 or as -1, never as 303..326.
- **The request needs two gates open.** `00306BD0` returns 0 before `00306C4D` unless both of these hold:
  - `022C2160` is 0, or it is 1 with the same owner in `022C2168`;
  - `0032F6E0(3)` is 0.

  These are the "idle or same owner" and "allows it" conditions of [the mode ladder,
  §2d](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md). Separately,
  `00306760`'s six-way dispatch (`003067AA`) switches on the kind `022C215C`, not on `+0x1E`.

**Limits kept.** These limits are ASTRA's and SPEC's.

- The row-`0x113` type bound, the row/codec identity and the descriptor count staying unmodified are premises. So are
  the interpreter's value transfer (`00309C13` -> `00267E10`) and stable raw-record state.
- A nonzero raw `+5` bypasses the category test.
- The nonnegative override word is bounded only by the 2026-09-30 subsection above, under its premises.
- `003068D4`, the `00387090` effective-id leg and the other callers of these functions are not covered.
- The queue's five direct-reference instructions are a census, not an alias closure.
- No slot allocation, command, AI or script selection, successful load, owner submission or rejection is observed or
  proved. Natural rejection and whole OV-42 stay OPEN.
