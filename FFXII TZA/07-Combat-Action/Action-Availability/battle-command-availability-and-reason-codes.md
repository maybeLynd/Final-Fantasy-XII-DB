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

~~**PARTIAL.**~~ **AUDITED.** *(corrected 2026-10-02, OPUS: the front matter says `status: AUDITED`, every box ticked; the codes never reach a screen, AI-1 answered 2026-09-02 in §7 and §11, so the unmapped-message clause below is stale)* The top-level cascade is read at instruction level. Several of its steps call
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
if (raw == NULL)  /* RDX = 002FFCF0's RDI, q[unit+0x698] */  return 0x2C;
if (BattleAction_CheckDefinitionCategoryAvailability(actionId))  return 0x0F;
if (BattleStats_HasRequiredLicenseForAction(raw, actionId))      return 0;
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
reading. ~~The enumerated table is therefore **not** the complete reason-code set — it is the set~~
~~raised by the two functions that were read.~~ *(answered: the table was completed the same day - nineteen codes from every leg, section 10, AI-4; 2026-10-02, OPUS)*

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
and a **global** amount ~~with a per-unit fallback~~ checked together with the gil cost already reserved for the action in progress at `unit[0xE58]` *(corrected 2026-10-02, OPUS: `+0xE58` is not a purse - `0030EFC0 mov dword ptr [rbx + 0xe58], eax` stores `00309060`'s result there, the refund `00300280` adds it back and `00305640` clears it; row `0x15` of the reason-code table)*. The third is gated on `raw[5] == 0`, the same class
selector the cascade uses.

**An inference, flagged as one:** a party-wide pool checked before ~~a per-unit one~~ the cost already reserved at `unit[0xE58]` *(corrected 2026-10-02, OPUS: `+0xE58` is a reserved cost, not a per-unit pool, `0030EFC0`; row `0x15`)*, in a system whose
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
bit identified); ~~**AI-1 remains fully open** — nothing here maps a code to on-screen text.~~ *(answered: AI-1, 2026-09-02 - the codes never reach a screen, §7 and §11; 2026-10-02, OPUS)*

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

## SWE2-EC7-19 update (~~2026-05-15~~ 2026-09-18 *(corrected 2026-10-02, OPUS: committed in `add029c9c`)*) — `00322490` angle-wrap + vector submit fragment

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
    raw record's type byte minus `0x1B` with no bound check (`003092D6`..`003092DB`) *(qualified 2026-10-02, OPUS, from ASTRA's SPEC-accepted [`presentation-index-domain`](../../_experiments/evidence/presentation-index-domain/README.md), method A: 'row `0x113`' is a full 64-bit compare of the entry RDX with the zero-extended 32-bit `low32(second resolver return) + u16(context+8) × 0x113`, or 0 when the context or the first return is null, the two resolver returns and context reads not assumed identical; the `+0x24` arm returns the word zero-extended (0..65535) without the type; the table read is in bounds only for type 27..39, and out-of-band addresses are source predictions, not observed faults or values; the returned EAX reaches `0032FC30` as EDX with no index check between, a source transfer not shown to occur in play; natural type and context admission stays OPEN)*.
  - Group 3's index is `4w+1`. The owner path narrows it to a WORD ([the indexed-source
    page](../../02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md), FABLE
    2026-09-30 subsection).
- **The rows.** The nine shipped tables are one table of 543 rows of 60 bytes.
  - No word other than FFFF gives a negative narrowed WORD. This is the WORD sign only. The ten bit-15 words
    32775..32907 (rows 111-123, 246-261, 427-435 and 440) narrow to positive WORDs, and none of their rows has bit 30.
  - FFFF narrows to the WORD -3. FFFF with bit 30 occurs on row `0x113` and on rows **511..534**. All of rows 511..534
    have `+0x1E` 7.
- **What does not exclude 511..534.**
  - Class `0x14` accepts 0..542. The count is the runtime value `[02EBF138]+4` (`00322F84`, `0032302C`..`0032303B`).
    543 is the shipped table's row count, and that is a premise: `02EBF138` lies in `.data`'s virtual tail, so it is
    0 at load, and a NULL descriptor refuses every id (FABLE 2026-10-02, review below).
  - The D0..F1 refusal (`0030CEC2`..`0030CEFE`) applies only while the special-sequence state `022C2160` is 5 or 6.
    Rows 511..534 lie above `0xF1` in any case.
  - The queue remap. The queue cell `022C2178` holds `word - 0xD0` (`0030DBDA`, `0030DC7B`, `003068CA`) or -1
    *(qualified 2026-10-02, FABLE: at `003068CA` = `00306760` + 0x16A the word is the low 16 bits of a row
    quotient that the routine computes, not a stored word; the special-sequence queue-writer subsection below)*, and
    its reader `00309C00` consumes the value. The script adapter `0030EEA0` adds `0xD0` back as a 16-bit add
    (`0030EEB2`) before ~~`0030CFB0` stores the word into the slot's `+0x1C` (`0030D14F`)~~ the acquire wrapper
    `0030CFB0` passes the word to the slot allocator `0030D070`, whose last store writes it into the slot's `+0x1C`
    (`0030D070` + 0xDF) *(corrected 2026-10-02, FABLE: the store is the allocator's, not the wrapper's; ASTRA's
    `ov42-slot-id-producer`, FABLE review [record](../../_index/candidates/fable-review-astra-ov42-slot-id-producer-1002/REVIEW.md), slot-allocator subsection below)*.
    Rows 511..534 queue as 303..326 and decode unchanged. Only `0xCF` and FFFF read as unavailable, so the remap has
    no universal inverse.
- **What does exclude them, on two legs only.**
  - (a) `0030DB70`'s record arm. The raw record is the pointer `002FFCF0` loads from the incoming RDX `+0x698` at
    `002FFD05` and keeps in RDI; it passes that pointer as RDX to `00306480` (`002FFCF0` + 0x1A7), which forwards it
    unchanged to `003060E0`, where `003060E0` + 0x49 reads `+5`. The later reloads of `+0x698` do not replace it, so
    the `+5` test concerns that parsed record, not a byte of the outer unit (FABLE 2026-10-02). If the unit's raw
    record has byte `+5` = 0, `003060E0` returns 5 for
    `+0x1E` 7 (`00306300`). `00306480` turns that into `0x0F`, `002FFCF0` refuses, and `0030DB70` returns at
    `0030DBC5`, before its stores. A nonzero `+5` bypasses the test (`0030612F`).
  - (b) Its null-record arm, when the override `01EEBAF0` is negative. The matcher above then returns a byte 0..255
    (`002F8E36`) or -1 (`002F8E28`). Those queue as -208..47 or as -1, never as 303..326.
- **The request needs two gates open.** `00306BD0` returns 0 before `00306C4D` unless both of these hold:
  - `022C2160` is 0, or it is 1 with the same owner in `022C2168`;
  - `0032F6E0(3)` is 0.

  These are the "idle or same owner" and "allows it" conditions of [the mode ladder,
  §2d](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md). Separately,
  `00306760`'s six-way dispatch (`003067AA`) switches on the kind `022C215C`, not on `+0x1E`. Only its kind-4 arm
  writes the queue (FABLE 2026-10-02, the special-sequence queue-writer subsection below). When both gates are
  open, `00306BD0` publishes that kind from its own full 32-bit row quotient (FABLE 2026-10-02, the kind-band
  subsection below).

**What a zero availability reason proves about the id** *(FABLE 2026-10-02, from ASTRA's
[`ov42-actor-predicate-domain`](../../_experiments/evidence/ov42-actor-predicate-domain/README.md) (`2b341ca3a`),
FABLE independent review ACCEPT-WITH-NARROWING,
[`fable-review-astra-ov42-actor-predicate-domain-1002`](../../_index/candidates/fable-review-astra-ov42-actor-predicate-domain-1002/REVIEW.md)).*

- `002FFCF0` has two returns: the early constant 2, and the shared reason return.
- The only EAX definition that can make the shared return 0 is the final cost call `00303BD0`, reachable only
  through the class-success edge after the class query at `002FFCF0` + 0x9B.
- The class query receives EDX = the zero-extended low 16 bits of the incoming id (`002FFCF0` + 0x1C), ECX = `0x14`
  (decimal 20) and R8D = 1. The class-`0x14` arm and the shared tail never read R8.
- So a normal zero reason requires class `0x14` to accept the id. Under the count-543 premise the id is then
  0..542, which still includes 511..534.
- This is a necessary condition only. A zero reason also requires `0030E9C0`, `0031A7B0`, `00306480` and
  `00303BD0` each to return 0; nothing here shows that any of 511..534 passes those gates.
- The record's byte `+5` staying unchanged from its load to the `00306480` leg is a premise. Two callees on that
  path, `0030E9C0` and `0031A7B0`, receive the record pointer itself.

**Limits kept.** These limits are ASTRA's and SPEC's.

- The row-`0x113` type bound, the row/codec identity and the descriptor count staying unmodified are premises. So is
  stable raw-record state. So is the interpreter's value transfer: the reader stores the action DWORD through its
  RDX destination (`00309C13`), and a later script read takes it from there; that read is not part of the bridge,
  and its reader is unread. The bridge pops both out-references through `00267E10` *before* the reader runs, so
  the transfer is unchanged only if the two destinations are valid, byte-disjoint and not overwritten before the
  read (next subsection; FABLE 2026-10-02).
- A nonzero raw `+5` bypasses the category test.
- The nonnegative override word is bounded only by the 2026-09-30 subsection above, under its premises.
- ~~`003068D4`,~~ ~~the `00387090` effective-id leg~~ and the other callers of these functions are not covered.
  *(narrowed 2026-10-02, FABLE: the effective-id leg is now read where the standard-action route hands its
  word to the acquire wrapper - the effective-id subsection below)* *(narrowed 2026-10-02, FABLE: the queue
  store `00306760` + 0x174 is now read - the special-sequence queue-writer subsection below)*
- The queue's five direct-reference instructions are a census, not an alias closure.
- No natural slot allocation, command, AI or script selection, successful load, owner submission or rejection is
  observed or proved. The slot allocator's own admission is now read: it stores any word into a free slot (the
  slot-allocator subsection below). Natural rejection and whole OV-42 stay OPEN.

### FABLE 2026-10-02: what the queue reader writes, in what order, and what its script bridge then reads (OV-42)

*From ASTRA's packet [`ov42-queue-output-alias`](../../_experiments/evidence/ov42-queue-output-alias/README.md)
(`4fe271b46`), reviewed by FABLE ACCEPT-WITH-NARROWING
([record](../../_index/candidates/fable-review-astra-ov42-queue-output-alias-1002/REVIEW.md), 49 checks, 0 FAIL, 11 controls).*

- **The reader `00309C00` (50 B, no `.pdata`, a leaf).** It reads the queue DWORD `022C2178`.
  - If the DWORD is FFFFFFFF, the reader returns DWORD 0. It writes nothing and does not reset the queue.
  - Otherwise it stores the DWORD through RDX when RDX is non-null. Then, when RCX is non-null, it loads the unit
    DWORD `022C218C` and stores it through RCX. Finally it resets the queue to FFFFFFFF and returns DWORD 1. Each
    store is 4 bytes.
  - With both pointers NULL, a pending value is still consumed: the queue is reset and the reader returns 1.
- **The two stores are ordered.** The unit load and store come after the action store. If the two destinations
  overlap, the unit store overwrites the overlapping bytes: action byte j becomes unit byte j - d when
  0 <= j - d < 4, where d = RCX - RDX. A shared destination ends holding the unit DWORD in both views. Only
  byte-disjoint destinations keep both values whatever they are, and a sample in which the two values happen to
  agree cannot show that the destinations do not overlap.
- **The formula assumes neither destination aliases `022C2178` or `022C218C`.** An action store into `022C218C`
  would change the unit value loaded after it, and any output in `022C2178` is overwritten by the reset.
- **The script bridge (165 B; FABLE confirmed the extent against `.pdata`).** It pops two out-references through
  the interpreter's pop, decodes each to a destination, and passes them as RDX (action) and RCX (unit). After any
  normal return it reads both destinations on a straight line with no test of the result, so it also reads them
  when the reader returned 0, and copies the two values to a pair of globals after shifting their old values. The
  reader's null guards therefore do not make a bridge call with invalid destinations safe; on a 0 return the
  copies are whatever the destinations already held. (The bridge's address is on the script-native pages; it is
  named by role here.)
- **The reader has one other direct caller,** which passes two stack locals `0x20` apart. That raw `E8`/`E9`
  census does not cover indirect callers.

**Limits kept.** These limits are ASTRA's and FABLE's.

- No authored out-reference binding, backing capacity, alias, lifetime, null or invalid destination, fault or
  natural command-to-action path is observed or proved.
- Whether the bridge's decode can yield an invalid destination is not read.
- The role of the bridge's copy globals is not established; no reader census was taken.
- The 8 branch partitions are logical, not native calls. The overlap rows are arithmetic.
- Whole OV-42 stays OPEN.

### FABLE 2026-10-02: what the presentation-slot allocator admits (OV-42)

*From ASTRA's packet [`ov42-slot-id-producer`](../../_experiments/evidence/ov42-slot-id-producer/README.md)
(`0ada51452`), reviewed by FABLE ACCEPT-WITH-NARROWING
([record](../../_index/candidates/fable-review-astra-ov42-slot-id-producer-1002/REVIEW.md), 53 checks, 0 FAIL,
13 controls). Static, plus an emulation of the original bytes on synthetic slots and rows.*

- **The allocator `0030D070` (229 B, one `.pdata` record, no calls).** It scans the 32 slots at `022C17B0` + 48*i
  from slot 0 upward and stops at 32. A slot is free when its WORD `+0x1C` is FFFF, and the first free slot wins.
  - It writes that slot's list links (`+0`, `+8` and the list's head or tail cells), DWORD 1 at `+0x10`, `+0x14`
    and `+0x18`, and the incoming ECX at `+0x20`. Its last store is the incoming DX, zero-extended, at `+0x1C`
    (`0030D070` + 0xDF). It returns EAX = the slot index, 0..31.
  - That store is the action word's only use. No compare in the body reads the word, so there is no action-range,
    category or identity test. Each of 511..534 is stored unchanged when a slot is free.
  - With all 32 slots occupied, it returns AL = FF and writes nothing outside its frame. That is a capacity
    failure, not a refusal of the id. Only AL is defined on that arm.
  - A supplied FFFF is also copied, so the slot is linked and initialised but still reads free. No natural FFFF
    submission is claimed.
- **The acquire wrapper `0030CFB0` (185 B).** It takes the action word in R8W and the identity in EDX. It passes
  them to `0030D070` as EDX (the word, zero-extended) and ECX, then stores the returned AL in unit+4. The wrapper
  itself never writes `+0x1C`; the word store is the allocator's.
  - A unit+4 that is not FF skips the whole acquisition.
  - A row whose `+0x0C` bit 30 is clear allocates directly.
  - With bit 30 set, a word in D0..F1 allocates while `022C2160` is 5 or 6.
  - Every other bit-30 row meets a one-shot flag, bit 1 of `022C2158`. If the bit is set, the row is skipped. If it
    is clear, the wrapper sets it and allocates. The words 511..534 are 303..326 above D0, so they meet this flag.
  - The flag is set *before* the allocator runs, and the wrapper never clears it. That includes the case where the
    array is full and unit+4 stays FF. Whatever clears it is not read.
  - The row comes from `[02EBF138]` through `0020E600` as a zero-extended 32-bit pointer. A null descriptor or a
    null resolve sets that pointer to 0, and the wrapper still reads `+0x0C` (address 0xC). There is no null guard.
- **Direct callers (raw `E8`/`E9` census).** `0030D070` has one direct caller, the wrapper (`0030CFB0` + 0xA1). The
  wrapper has two: the script adapter `0030EEA0` (+ 0x60), and a call in a battle-action routine that this page does
  not otherwise cite (its word source is the next subsection). Indirect callers are not covered.

So the slot allocator does not exclude 511..534. Its only refusals are capacity, a slot the unit already holds and,
for bit-30 rows, the special-sequence state and the one-shot flag.

**Limits kept.** These limits are ASTRA's and FABLE's.

- No command, AI or authored-VM producer is read that supplies 511..534 or FFFF. *(narrowed 2026-10-02, FABLE:
  on the standard-action route the word is the effective-id getter's return, which passes the owner's `+0x714`
  word unchanged unless it is `0x9F`; that route's frontier is now whatever writes `+0x714` and what it admits,
  next subsection)*
- Current row and descriptor identity, readable stable rows, and the pool's initialization, ownership and reuse
  are premises. The slot array lies in `.data`'s virtual tail, so its FFFF markers come from the pool reset, which
  is not read here.
- What a FFFF allocation leads to (a linked slot that still reads free) is not claimed.
- No natural slot allocation, command execution or rejection is observed.
- Whole OV-42 stays OPEN.

### FABLE 2026-10-02: where the standard-action route's slot word comes from (OV-42)

*From ASTRA's packet [`ov42-effective-id-source`](../../_experiments/evidence/ov42-effective-id-source/README.md)
(`2cce275ad`), reviewed by FABLE ACCEPT-WITH-NARROWING
([record](../../_index/candidates/fable-review-astra-ov42-effective-id-source-1002/REVIEW.md), 62 checks, 0 FAIL,
16 controls). Static, plus an emulation of the original bytes on synthetic query records, units, tables and a
scripted unit registry.*

- **The transfer.** The acquire wrapper's other direct caller (previous subsection) sits in case 6 of a
  battle-action routine's 13-way phase switch. There the routine passes its unit's QWORD `+0x698` as RCX to the
  effective-id getter `00387090`, and its next call is `0030CFB0`. Between the two calls, the returned AX is
  zero-extended into R8D, and nothing else writes R8 or calls anything. So the word that the wrapper hands to the
  slot allocator is the getter's return. EDX is the unit's DWORD `+8`. R9D is the unit's BYTE `+0xEA9`, loaded
  before the getter call and kept in RBX, which the getter restores. The routine is named by role here; its
  addresses are in the record.
- **The getter `00387090` (149 B; one root and two chained `.pdata` records).** It calls the owner resolver
  `0031B860` once or twice and returns a zero-extended WORD.
  - *Which record.* A non-null query whose BYTE `+5` is 0 selects record BYTE `+4` of the 64-byte bank at
    `0208D480`, without a first resolver call. Otherwise the first resolver return, O1, is stored to `02EBF188`
    (0 when null). A non-null O1 selects record BYTE `+0xEA9` of the bank at `0208DE80`. A null O1 selects none,
    and the record pointer is 0. A selected pointer is never 0, and the getter bounds neither byte index.
  - *Which word.* The second resolver return, O2, is the owner whose WORD `+0x714` is read. If that word is `0x9F`
    and a record was selected, the getter returns the record's WORD `+0x10` instead (`00387090` + 0x7E).
    Otherwise it returns the `+0x714` word itself (`00387090` + 0x88). A stored `0x9F` therefore comes back
    unchanged only when the first resolver returned null.
  - *No bound.* The getter makes six tests: the query, BYTE `+5`, O1, O2, the record pointer, and the one
    compare with `0x9F`. In the emulation, each of 511..534 is returned unchanged on both legs, and through the
    caller's line it reaches the wrapper as R8 unchanged.
  - *Two owners.* O1 and O2 come from separate resolver calls. The record follows O1 and the word follows O2.
    When the registry changes between the calls, the substitute comes from O1's record (emulated). No stable or
    shared owner is assumed. The `0x9F` compare and the returned word are also two separate reads of `+0x714`.
  - *No safe NULL.* The resolver returns 0 for a NULL query before any registry call. Otherwise it returns the
    first registry unit whose QWORD `+0x698` equals the query, or 0. A null O2 goes straight to the `+0x714`
    read, at address 0x714, and there is no sentinel return. That is a source prediction, not an observed
    fault, and no caller is shown to pass NULL.
- **Other direct callers (raw `E8`/`E9` census).** The getter has three. One is this call. One is in a later case
  of the same routine, where its AX goes to EDX for a different callee. One is in the unit display-record builder.
  Only the first is read for the transfer. Indirect callers are not covered.

So on this route the effective-id getter adds no bound. A non-`0x9F` word at O2's `+0x714` reaches the slot
allocator unchanged. The standard producer frontier therefore narrows to whatever writes `+0x714` and what that
writer admits. [The battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) lists
three writers of the field in its census: the commit, the cancel and the reuse reset. None of them is read here for its domain. [The
formula scratch-block page](../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) describes the
`0x9F` substitute as a drawn id. That writer is not read here either.

**Limits kept.** These limits are ASTRA's and FABLE's.

- Valid, readable and stable query, owner, record and frame accesses, the normal native ABI and preserved
  nonvolatile registers are premises.
- O1 and O2 are not shown to be the same unit, or to be the caller's own unit. O2 is the first registry unit with
  the query's `+0x698`. Owner lifetime, reuse and registry order are not read.
- The banks' initialization, contents and extent are not read. No value domain is claimed for record `+0x10`.
- No natural `+0x714` value, NULL caller, fault, command acceptance or execution is observed.
- The caller's line is placed inside one case of the routine. It is not proved from a natural entry, and the
  routine's unit, records and phase byte are premises.
- Whole OV-42 stays OPEN.

### FABLE 2026-10-02: what the special-sequence queue store writes (OV-42)

*From ASTRA's packet [`ov42-sequence-queue-source`](../../_experiments/evidence/ov42-sequence-queue-source/README.md)
(`0c4215736`), reviewed by FABLE ACCEPT-WITH-NARROWING
([record](../../_index/candidates/fable-review-astra-ov42-sequence-queue-source-1002/REVIEW.md), 58 checks, 0 FAIL,
17 controls). Static, plus an emulation of the original bytes on synthetic rows, descriptors and lookup returns.*

- **The routine `00306760` (five chained `.pdata` records, 936 bytes).** Its 911 code bytes end at its one `ret`
  (`00306760` + 0x38E). A NOP and six DWORD jump entries follow (+ 0x390 .. + 0x3A8). They are data, not code.
- **The dispatch.** It loads the kind DWORD `022C215C` (+ 0x4A), subtracts 1 and compares the result unsigned with
  5. Kinds 1..6 jump through the six entries. Kind 0 and every kind above 6 (unsigned) go straight to the shared tail. Only the
  kind-4 arm (+ 0xE8) reaches the queue store (+ 0x174). In the emulation of the whole routine with the kind cell
  set to 0..7, only the kind-4 run writes `022C2178`.
- **The value.** The routine keeps its incoming RDX, the row pointer, in RDI. The kind-4 arm then works as follows.
  - It loads `02EBF138` and passes its DWORD `+0xC` to `0020E600`. It subtracts the returned EAX from EDI, a 32-bit
    subtraction: D = (low32(row) - low32(base)) mod 2^32.
  - It loads `02EBF138` again and divides D by the WORD `+8`, zero-extended, with an unsigned 32-bit `div`
    (+ 0x158). The quotient is q.
  - It compares q's low 16 bits, w, with FFFF. If w is FFFF it stores FFFFFFFF. Otherwise it stores
    (w - 0xD0) mod 2^32 to `022C2178` (+ 0x16A, + 0x174). The store is a DWORD.
  - For a row formed as base + 60 * id, ids 511..534 queue as 303..326 (emulated). These are arithmetic results,
    not native runs.
  - Quotients alias modulo 65536 before the test. w = `0xCF` also stores FFFFFFFF.
- **Two loads, no guard.** The descriptor is loaded twice, and the lookup call comes between the loads. The key comes
  from the first load and the divisor from the second. In the emulation, repointing the cell during the call changes
  only the divisor. Nothing tests the divisor before the `div`. A zero WORD faults (#DE in the emulation); that is a
  source prediction, not an observed fault.
- **The arm's other writes.** After the store, the arm writes the unit's DWORD `+8` to `022C218C`, the value the
  queue reader returns with the queue (subsection above). Every return of the routine stores 5 to `022C2160`.
- **Kind 3** computes the same full 32-bit quotient. It passes it to another callee, not to the queue.
- **The caller.** The raw `E8`/`E9` census gives the routine one direct caller. That caller is in the same
  battle-action routine as the acquire wrapper's second caller (slot-allocator subsection), and it calls only when
  row bit 30 (`+0x0C`) is set. Indirect callers are not covered.

So the local producer leg has a single bound: the kind. Whatever row the caller passes, kind 4 queues that row's
quotient through the remap. Nothing in this routine tests the row's id or category. Excluding 511..534 on this leg
needs the kind-to-row, caller and owner consistency: the kind in `022C215C` must refer to the same row this call
passes. That consistency is not established.

**Limits kept.** These limits are ASTRA's and FABLE's.

- Kind-to-row, caller and owner consistency stays OPEN. A normal kind-4 call is not shown to carry a row in the
  usual Quickening range. ~~The kind cell's writers and persistence are not read.~~ ASTRA's later packet
  `ov42-kind-row-coherence` (`d83287255`) bears on this ~~and is not yet reviewed~~. *(narrowed 2026-10-02, FABLE:
  the packet is reviewed, and the kind cell's direct writers are now counted; its persistence is still not closed -
  the kind-band subsection below)*
- The two descriptor loads are not shown to read the same, initialized descriptor. A positive WORD `+8` is a
  precondition.
- The arm's five earlier callees (four helpers and a `memset`) are opaque. The Win64 ABI, which preserves RDI and
  RBX, and valid, readable, stable row, unit and descriptor state are premises.
- No natural kind-4 call, queue consumption, command execution or rejection is observed.
- Whole OV-42 stays OPEN.

### FABLE 2026-10-02: which quotients publish kind 4, and what that binds in the queue (OV-42)

*From ASTRA's packet [`ov42-kind-row-coherence`](../../_experiments/evidence/ov42-kind-row-coherence/README.md)
(`d83287255`; method addendum `19e732aa6`), reviewed by FABLE ACCEPT-WITH-NARROWING
([record](../../_index/candidates/fable-review-astra-ov42-kind-row-coherence-1002/REVIEW.md), 75 checks, 0 FAIL, 18 controls).
Static, plus an emulation of the original classifier and of the queue's kind-4 arm on synthetic rows, descriptors
and stubbed callees.*

- **The classifier `00306BD0` (three chained `.pdata` records, 440 bytes).** Its 284 code bytes end at its last
  `ret` (`00306BD0` + 0x11B). Seven DWORD jump entries (+ 0x11C) and 128 selector bytes (+ 0x138) follow. They are
  data, not code.
- **When it publishes.** Only past the two gates above. It then records its RCX as the owner in `022C2168`, sets
  `022C2160` to 2, computes the kind, stores it as a DWORD to `022C215C` and returns 1. The owner compare tests the
  unit, not the row.
- **The quotient is full 32-bit.** The row is the classifier's incoming RDX. It computes
  q = ((low32(row) - low32(base)) mod 2^32) / u16 stride with an unsigned 32-bit `div`. The key comes from the
  first load of `02EBF138` and the stride from a second load after the lookup call; there is no zero test. This is
  the same shape as the queue arm (subsection above). The full EAX then goes through `add eax, -0x94` and an
  unsigned `cmp eax, 0x7f`. Nothing narrows q to a WORD first.
- **The kinds.** For q = 148..275 a selector byte picks one of seven entries: 148 -> 5, 149 -> 6, 150..181 -> 7,
  182..207 -> 3, 208..225 -> 4, 226..261 -> 7, 262..274 -> 1, 275 -> 2. Every other 32-bit q, including 0..147,
  publishes 7. **Kind 4 is published exactly for q = 208..225.** Kind 3 has no arm of its own: it is the 3 that
  the routine loads into EBX at its start, and it survives five calls only by the Win64 ABI.
- **The full-32 / low-16 split.** The queue arm narrows its own quotient to 16 bits before its FFFF test and its
  `- 0xD0`; the classifier does not. So q = 65744 (`0x100D0`) publishes kind 7, while the queue arm would read it
  as 208 and queue 0 (emulated).
- **The `0032FC30` result is unused.** On the publishing path nothing reads that call's RAX or flags. The next
  call is a 16-byte leaf whose first instruction overwrites RAX, and the descriptor load after it writes RAX again.
  This concerns return use only. It does not show the request's native effect or success.
- **The kind cell's direct writers.** In a census of rip-relative and image-base-relative accesses, only the
  classifier writes a nonzero kind. Two end-of-sequence routines zero kind and state together with one 8-byte
  store each, then clear the owner. The two readers are the queue routine's dispatch and the finisher's kind
  dispatch. The queue routine never reads the owner cell. Register-based, aliased and indirect writes are not
  covered.
- **The two rows come from different routines.** The classifier's one direct caller is `0030CE10`, which passes its
  own incoming row unchanged; `0030CE10`'s one direct caller is `0030CBE0` (first subsection). The queue routine's
  one direct caller builds its row separately (queue-writer subsection). Indirect callers are not covered.

**The conditional invariant.** Suppose the queue routine's dispatch still reads the kind 4 that this classifier
published, and the queue arm's quotient equals the classifier's. Then q is 208..225, its low 16 bits are q, and the
queue DWORD is q - 208 = 0..17. Ids 511..534, which queue as 303..326, are then excluded on this leg. Equal row
low32, equal base low32 and equal positive strides are enough. Equal quotients alone are also enough, so pointer
identity is not needed. Neither equality is established for a normal call. Two supplied states mark the limits:
a kind-4 publication at q 208 followed by a queue quotient of 511 queues 303, and q 65744 publishes kind 7 but
queues 0. Both are arithmetic run through the original bytes in emulation, not native runs.

**Limits kept.** These limits are ASTRA's and FABLE's.

- Natural kind-to-row, caller and owner consistency stays OPEN. The two quotients come from rows built in
  different routines, at different times, from separate descriptor reads. No natural-impossibility claim is made
  for 511..534.
- The kind's persistence between the classifier and the queue dispatch is closed only for direct writes. Re-entry
  between the two is not read.
- The descriptor's initialization and its stability between each pair of loads and across calls are premises. So is
  a positive stride: a zero WORD faults after state 2 and the owner are written (a source prediction).
- The native effects of `0032F6E0`, `00309230`, `0032FC30` and `0020E600` are not read. The Win64 ABI, which
  preserves RSI and RBX, and valid, readable, stable row and descriptor state are premises.
- ASTRA's later packet `summon-kind-row-carrier` (`c40b24340`), on the queue routine's row carrier, is not yet
  reviewed.
- Whole OV-42 stays OPEN.
