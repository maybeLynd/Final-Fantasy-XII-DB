---
system: Party roster and control suppression
category: 11-Party
status: AUDITED
owner_layer: PrimaryOwner:Party
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
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# Party roster and control suppression

> The four active party slots, how a character is assigned to one, and why your controls stop
> responding when your leader goes down.

## 1. What the player sees

Your active party is **four slots**. Everything the game does with "the party" — spawn distance
checks, reward sharing, targeting — walks those four.

And when the character you are controlling is disabled, **you lose control of the party**. Not
reduced control: input suppression. The game does not explain it; it simply stops responding
until the leader recovers or the area waives the rule.

That last clause matters — **some areas waive it**, which is why the same condition in a
different zone behaves differently.

## 2. Native mechanism

### The roster is four pointers

```c
bool PartyRoster_IsFourSlotIndex(uint i)      { return i < 4; }

void *PartyRoster_GetActorBySlot(uint i)
{
    return (i < 4) ? (&DAT_0209a1f0)[i] : NULL;
}
```

`DAT_0209a1f0` is a flat four-entry array of actor pointers. That is the whole active roster.

### Negative index means "whoever you are controlling"

```c
void *PartyRoster_GetActorBySlotOrCurrentFocus(int i)
{
    if (i < 0) {                                       // sentinel
        h = PartyFocus_GetCurrentPackedActorHandle();
        return ActorHandle_ResolveRegistryEntryByPackedId(h);
    }
    return (i < 4) ? (&DAT_0209a1f0)[i] : NULL;
}
```

A **negative slot index is a convention meaning "current focus"** — the character under player
control — resolved through the PartyFocus handle rather than the roster array. Callers use one
function for both "slot N" and "whoever is active".

### Assignment, and the actor's own slot field

```c
void PartyRoster_AssignActorToSlot(void *actor, uint slot)
{
    if (slot < 4 && roster[slot] != NULL) {
        occupant = *(longlong *)(roster[slot] + 0xC0);
        if (occupant) { *(u8 *)(occupant + 0x152) = 1;  f_002681E0(); }   // evict
    }
    if (actor) {
        old = actor[0x12];                    // the actor's own stored slot
        if (old < 4) {
            prev = roster[old];
            roster[old] = 0;
            if (prev) prev[0x12] = 0xFF;      // 0xFF = unassigned
        }
        ...
    }
}
```

**The tail, read 2026-09-12 (FABLE; O-6, and the same reading as [the contract](CONTRACT-party-slot-assignment.md) §7):** the displaced
record also gets `+0x0F = 3` (`00269CD9`); then, when the requested slot is non-negative,
`roster[slot] = actor` (`00269CE1`), the actor's own `+0x12 = slot` and `+0x0F = 2` for slots 0–3
or `3` above (`00269CE5`–`00269CF3` — the same `2 / 3` rule `ActorStorage_InitializeRecord` applies,
below); then for a slot ≤ 3 the **new** occupant's secondary context gets `+0x152 = 0` and the
same notice `002681E0` the evicted one received with `1` (`00269D04`–`00269D17`); and finally, if
no focus handle is set (`PartyFocus_GetCurrentPackedActorHandle() == 0`, `00269D21`), the actor is
**requested as the focus** — `PartyFocus_RequestPackedActorHandle(ActorHandle_EncodeRegistryEntry(actor))`
(`00269D2D`–`00269D34`) — and the notice runs once more (`00269D41`). Nothing else: no event, no
list rebuild.

**What the notice does — `002681E0`, and what `+0x152` marks (O-1).** For a **kind-3** actor only
(`+3 & 0xE0 == 0x60`, `002681F9`–`00268201`) with a secondary context (`+0xC0`), it reads the
context's byte `+0x152` — the **roster-role byte** — and derives a small number it stores as a
**word at `+0x80` of the context's `+0x138` record** and mirrors at the context's `+0x153`
(`00268294`–`002682B5`). That `+0x138` record is the actor's **movement body** (released through
`003DAD00` by `002E3D00`, `002E3D21`–`002E3D2D`; [the context censuses](../04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md)), and its byte `+0x80` is the body's
**cell class**: the placement resolver `00380D30` tests the field cell's blocked mask at bit
`class` (`00380D89`–`00380D8D`, `bt ecx, eax`) and refuses the cell with `+0x82 = −2` when it is set
([the movement body page](../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md)). So **the roster role decides which navigation cells the actor may stand on**:

| `+0x152` (role) | written by | class the notice stores |
|---|---|---|
| `1` | eviction from the roster (`00269CA6`); (re)initialisation (`00265E30`, from `ActorStorage_InitializeRecord`, with `+0x153 = 0xFE`); the refresh's flag-clear arm when the byte was `2` (`0026A850`) | **2** |
| `2` | the refresh's flag-set arm when the byte was `1` (`0026A839`, `BattleUnit_RefreshActorRuntimeFromDefinition` → `0026A7F0(actor, 0 / 1)`, `00238EE4` / `00238F38`) | **3** |
| `3` | nothing in the image (the arm at `00268228` is dead) | 5 |
| `0` | installation into the roster (`00269D10`); the record initialiser's zero | **0 for the focus actor** — when `PartyFocus_GetCurrentPackedActorHandle()` equals the actor's own encoded handle (`00268252`) — unless the actor's `+0x0C` bit 4 and `00265680()` hold, or `002672B0()` fails, in which case **1**; **1 for every other roster member** (`0026828A`); and **5 whenever mode 2 holds** (`0037C860` = `00303EC0`, the chocobo ride, [the mode ladder](../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2c) |

The two predicates walk the `0x288`-stride manager records (`002656C0`–`002656DF`, `002672C3`–
`002672E6`) for live entries whose byte `+0` has bits 0–1 both set; their names are the residue.
The displacement census of `+0x152` finds no other writer of the *context* byte (the `003AF460`
and `0018EEE0` sites are byte channels on other records — interior reads 2026-09-17,
SWE2-FRONTIER: `003AF460` is a per-frame countdown driver over `0x380`-stride records at
`02B3F58C`; each record carries (countdown, rate, accumulator) channels — nonzero count →
`dec` + `addss` accumulate, [`003AF481`](../_index/ADDRESS-INDEX.md) — and the loop advances
`rax += 0x380` at `003AFB1F`. `0018EEE0` is the glyph-record builder (see the glyph-quads page):
its `+0x152` sites are a per-glyph-record byte flag — read at `0018F0FF`/`0018F149`, set at
`0018F11D`, cleared at `0018F20D`/`0018F2B5`).

Each actor carries **its own slot number at `+0x12`**, with **`0xFF` meaning unassigned**. So
membership is stored twice — in the roster array and on the actor — and assignment ~~keeps both~~
~~consistent,~~ keeps them consistent for the actor it moves, clearing the actor's previous slot before taking the new one; the occupant it displaces keeps its `+0x12` and `+0x0F` while `roster[slot]` names the newcomer *(corrected 2026-10-02, OPUS: `00269C91`–`00269CAD` only notify that occupant; the reset at `00269CD5`/`00269CD9` hits the record in the actor's old slot — CONTRACT-party-slot-assignment.md §4)*.

### A third writer, from the actor side — added 2026-09-11 (OPUS-REQ-FABLE-ROSTER)

`ActorStorage_InitializeRecord` (`00266530`) enforces the same discipline when a record is
(re)initialised with a slot byte `al` ~~other than `0xFF`~~ in `0x80`–`0xFE` *(corrected 2026-10-02, OPUS: `0026673E jns` skips the block for a byte without bit 7, before the `0xFF` test at `00266740`)* (`00266740`–`00266792`): it reads the
record's **own** stored slot `+0x12` (`00266744`); if that is `0..3` (the compare is unsigned, so
negatives fall out) it clears `0209A1F0[old]` and, if that entry held a record, marks it
`+0x12 = 0xFF`, `+0x0F = 3` (`00266758`–`00266771`); then, if the new index (`al` with bit 7
cleared) is non-negative, installs this record at `0209A1F0[new]` (`0026677C`), stores the index at
`+0x12` and sets `+0x0F` to `2` for slots `0..3` and `3` above (`00266784`–`00266792`). So the
census below is image-wide for the roster's writers: the party verb path, this initialiser, ~~and~~ the clears `002695A0` and `0025BFB0` (bit-0 arm) *(corrected 2026-10-02, OPUS: five writers, CONTRACT-party-slot-assignment.md §15 — `002695AF`/`002695B7` and `0025C017`/`0025C01F` are the other two 32-byte clears)*, and
`WorldPersistence_ResetBanksForFieldTransition` (`0026DB30`), which zeroes exactly the 32 bytes
`0209A1F0`–`0209A20F` with two `movdqu` stores at `0026DB52` / `0026DB5A` — a second, independent
instrument for `void*[4]`. Whether `+0x0F = 2 / 3` is the "in party / not" kind the page's
suppression gate reads is not established here.

### Control suppression — the same functional gate as acting and earning

```c
void PartyControl_RecomputeSuppressionFromLeaderBattleState(void)
{
    suppress = -(uint)((DAT_02089340 & 0x40) != 0);

    if (f_00303EC0() == 0
        && FieldData_GetActiveFieldRecordBit15() == 0
        && (leader = BattleUnit_GetPartyLeader()) != NULL)
    {
        if (leader->pBkbi == NULL   // <- corrected 2026-10-02, OPUS - not an all-suppressed arm: 0023B152 reloads +0x698 and 0023B15E reads [rax + 0x64] with no null test, so this path faults before publishing (the correction block below)
            || ( ((leader->pBkbi->dwStatusMaskMode0_3 | leader->pBkbi->dwStatusMaskMode1_4)
                  & 0x80000003) != 0
                 && FieldData_GetActiveFieldRecordBit15() == 0 ))
        {
            suppress = 0xFFFFFFFF;            // control suppressed
        }
    }
    ...
}
```

> **Corrected 2026-09-12 (ASTRA's falsification, [the capability policy](../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md) §11; FABLE agrees after
> re-reading `0023B0C7`, `0023B152`–`0023B15E` and `0023B17C`–`0023B1B8`).** This sketch stops after the first gate and
> overstates it:
> - **A null `pBkbi` is not an all-suppressed result.** The early branch sets the mask at `0023B0C7`, but `0023B152`
>   reloads the same pointer and `0023B15E` reads its `+0x64` with no second null check — an isolated run faults there
>   before anything is published. Whether initialized gameplay can reach that state is not established.
> - **The mask is three bits built from several contributions**, published separately: bit 2 to `022C8005` bit 1, bit 0
>   to `022C8000` bit 1 (movement), and **NOT bit 1** into `0209A2C5`. Besides the terminal statuses it takes the
>   party-down bits `0x600`, a combo in progress, unit flag 46, the leader's knockback / evade / parry events, an action
>   in phase ≥ 9, unit flag 24, and the wider control-status masks — see the policy page §10.
> - **Immobilize** adds only bits 0 and 2; it does not clear bit 1 that the seed or an event already set.
> - **A later mode-1 gate** (`003135C0`) can replace the whole mask from a second selected unit (`003137F0` →
>   `0031B770`), after the leader's contributions.

This is the **third** independently-found site of one engine-wide rule:

| Subsystem | Consequence when the condition holds |
|---|---|
| Combat action eligibility | the unit cannot act |
| EXP / LP award | the unit earns **nothing** |
| **Party control** | **the player loses control** |

All three test `(statusLayerA | statusLayerB) & 0x80000003` and all three are waived by
`FieldData_GetActiveFieldRecordBit15()`. This one calls that function **directly**, which is
the strongest link yet: the field-record override is not a combat detail, it is a general
"this area suspends the functional rule" switch.

So the rule reads as one sentence: **a unit in status bits 0, 1 or 31 is non-functional —
cannot act, cannot earn, cannot be controlled — unless the current field waives it.**

## 3. Key addresses

| Address | Name | Verified |
|---|---|---|
| `002647C0` | `PartyRoster_IsFourSlotIndex` | ✅ read |
| `00263750` | `PartyRoster_GetActorBySlot` | ✅ read |
| `00263770` | `PartyRoster_GetActorBySlotOrCurrentFocus` | ✅ read |
| `00269C70` | `PartyRoster_AssignActorToSlot` | ✅ read ~~(partial body)~~ whole *(answered: O-6, the tail read 2026-09-12 — §2's tail paragraph; 2026-10-02, OPUS)* |
| `0023B040` | `PartyControl_RecomputeSuppressionFromLeaderBattleState` | ✅ read (gate) |
| `002681C0` | `PartyRoster_ReapplyActorStoredSlot` | not read |
| `002681E0` | the roster-role notice: `+0x152` → the movement body's cell class (`+0x80`, mirror `+0x153`) | ✅ read 2026-09-12 |
| `0209A1F0` | the four-slot roster array | — |
| `02089340` | the battle-state word; bit `0x40` (bit 6) seeds suppression — **"a treasure is being opened"**: set by the begin of the durative verb `btlAtelOpenTreasureStart` (`0032A217`), cleared by its end (`0032A1E3`), read only here and by `00313A40` ([the world-tick page](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.5) | ✅ named 2026-09-12 |
| — | `BattleUnit_GetPartyLeader` (`003272A0`) | ~~not read~~ read *(answered: see active-party-reserve-and-the-moment-the-leader-changes.md §4; 2026-10-02, OPUS)* |
| — | `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) | ~~not read~~ read *(answered: `mov eax, [022C7FE0]` / `ret` — active-party-reserve-and-the-moment-the-leader-changes.md, falsification pass 1; 2026-10-02, OPUS)* |
| `00303EC0` | **`BattleRuntime_GetMode0To5FromFlagsAndFieldBit15() == 2`** — shared mode predicate, 6 callers; **mode 2 is the chocobo ride** (state-block `+0x5B04` bit 1, `ridechocobo` / `getoffchocobo` / `setchocobomode`, [the mode ladder](../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2c) | ✅ read; named 2026-09-12 |
| `0030D9A0` | `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` | ~~not read~~ read *(answered: "The ladder is now fully read", §9 — the battle runtime mode ladder page; 2026-10-02, OPUS)* |
| `002E8100` / `002681E0` | *(suppression/eviction helpers)* | ~~not read~~ `002681E0` read, `002E8100` not read *(answered for `002681E0`: see its own row above, read 2026-09-12; 2026-10-02, OPUS)* |
| `00266530` | `ActorStorage_InitializeRecord` — the actor-side roster writer (`00266740`–`00266792`) | ✅ read (that range) |
| `0026DB30` | `WorldPersistence_ResetBanksForFieldTransition` — zeroes the four slots (`0026DB52`, `0026DB5A`) | ✅ read (that site) |

## 4. Data structures and formulas

```
DAT_0209A1F0        void*[4]   the active party roster
Actor
  +0x12      u8    own party slot; 0xFF = unassigned
  +0xC0      ptr   -> record whose +0x152 is set on eviction
DAT_02089340 u32    the battle-state word; bit 0x40 = a treasure is being opened (seeds the suppression value)
```

**Slot access:**

```
slot(i)  = (i < 4) ? roster[i] : NULL                       unsigned compare
slotOrFocus(i) = (i < 0) ? resolve(PartyFocus handle)
               : (i < 4) ? roster[i]
               :           NULL
```

**Control suppression:**

```
suppress = (DAT_02089340 & 0x40) ? -1 : 0

if  f_00303EC0() == 0
&&  FieldData_GetActiveFieldRecordBit15() == 0
&&  leader != NULL:
        if  leader.pBkbi == NULL
        ||  ( (leader.statusLayer0 | leader.statusLayer1) & 0x80000003 ) != 0
            && FieldData_GetActiveFieldRecordBit15() == 0
        then suppress = 0xFFFFFFFF
        # 2026-09-12: the pBkbi == NULL arm faults later at 0023B15E before publication, and this is
        # only the first of several contributions — see the correction block above.
```

**The unified functional predicate**, shared across three subsystems:

```
nonFunctional(unit) =  ((unit.statusLayer0 | unit.statusLayer1) & 0x80000003) != 0
                    && FieldData_GetActiveFieldRecordBit15() == 0
```

## 5. Call chain

```
leader battle state changes
  -> PartyControl_RecomputeSuppressionFromLeaderBattleState
     -> BattleUnit_GetPartyLeader
     -> status mask 0x80000003 on the leader's two layers
     -> FieldData_GetActiveFieldRecordBit15    <- per-area waiver
     -> suppression value published

party composition changes
  -> PartyRoster_AssignActorToSlot
     -> evict current occupant (mark +0x152, f_002681E0)
     -> clear the incoming actor's previous slot, set old occupant +0x12 = 0xFF   <- corrected 2026-10-02, OPUS - the record reset (+0x12 = 0xFF, +0x0F = 3 at 00269CD5/00269CD9) is the one in the incoming actor's OLD slot; the occupant displaced from the new slot keeps both bytes
     -> install into roster[slot]
```

**Upstream:** combat state changes, and party-management UI.
**Downstream:** input handling (suppression), and every system that walks the four slots.

**Do not confuse with:** PartyFocus, which tracks *which* member is controlled. The roster is
*who is in the party*; focus is *who you are*.

## 6. Modding notes

- **Four slots, hard.** `DAT_0209A1F0` is a flat four-entry array and every accessor bounds-checks
  against 4. A larger active party is not a data change.
- **Negative slot index means "current focus."** Passing `-1` is the idiom, not an error.
- **Membership is stored twice** — roster array and actor `+0x12`. Writing one without the other
  desynchronises the pair; `0xFF` is the unassigned sentinel.
- **Control suppression is per-area waivable.** If a mod changes field-record bit 15, it changes
  when players lose control, not just combat eligibility.
- **XIIOnline:** the roster is a local four-slot array and slot indices are local positions.
  Suppression is computed from the *local* leader, so clients disagreeing about leader status
  will disagree about who has control — this needs an authoritative answer, not per-client
  recomputation.

## 7. What is not known

- [x] ~~What `+0x152` on the evicted occupant's `+0xC0` record marks.~~ **O-1 ANSWERED 2026-09-12
      (FABLE):** the secondary context's **roster-role byte** (`1` evicted, `0` installed, `2` the
      refresh's variant of `1`), consumed only by the notice `002681E0`, which turns it into the
      movement body's **cell class** (`+0x80`, mirrored at `+0x153`: `1 → 2`, `2 → 3`, `0 → 0` for the
      focus actor or `1` for a follower, `5` under the chocobo ride) — the class the placement
      resolver tests against the field cell's blocked mask (the paragraph above).
- [x] ~~What `f_00303EC0` tests — it gates the whole suppression recompute.~~ **O-2 ANSWERED 2026-09-02 (§9): it is `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15() == 2`, a shared mode predicate with six callers.**
- [x] ~~What `DAT_02089340` bit `0x40` represents.~~ **O-3 ANSWERED 2026-09-12 (FABLE) by
      cross-reference to [the world-tick page](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.5:** bit 6 of the battle-state word is **"a treasure is
      being opened"** — the durative verb `btlAtelOpenTreasureStart` (verb `3051`, thunk `0050FBE0`,
      [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)) sets it at its begin (`0032A200`, `0032A217`) and clears it at its end
      (`0032A170`, `0032A1E3`); the store census of the word finds no other writer of the bit, and its
      only readers are this recompute (`0023B050`) and `00313A00` (`00313A40`). So the seed is: control
      is suppressed while a treasure is being opened, before the leader's battle state is consulted.
      The gate in front of the recompute (O-2) is now also named: mode 2 is **the chocobo ride**, so the
      leader's out-of-play state is not consulted while mounted ([the mode ladder](../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2c).
- [x] ~~The remainder of `PartyRoster_AssignActorToSlot` past the eviction/clear phase.~~ **O-6
      ANSWERED 2026-09-12 (FABLE):** install, `+0x12` / `+0x0F = 2 / 3`, the new occupant's notice
      with `+0x152 = 0`, and a focus request when no focus handle is set (the tail paragraph above).
- [x] ~~Whether reserve/inactive party members live in a separate structure.~~ **O-5 ANSWERED on
      [the active-party page](active-party-reserve-and-the-moment-the-leader-changes.md) (ledger reconciled 2026-09-12):** they do not — the battle-state block's nine
      selectors are one array, indices 0–3 the roster and 4–8 the reserve.
- [x] ~~Player-facing identity of status bits 0, 1 and 31 — still open as **C-9**.~~ **ANSWERED 2026-09-11** — KO, Stone and X-Zone, from `status_data.bin` and `listhelp_status.bin` ([the statuses sheet](../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)). **C-9.**

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Roster is exactly four pointers at `0209A1F0` | complete bodies of `002647C0`, `00263750` | 1 |
| Negative index resolves current focus | explicit `if (i < 0)` branch in `00263770` | 1 |
| Actor stores its own slot at `+0x12`, `0xFF` unassigned | assignment clears `prev[0x12] = 0xFF` | 1 |
| Control suppression tests the same `0x80000003` mask | complete gate in `0023B040` | 1 |
| It calls the field-record override **directly** | `FieldData_GetActiveFieldRecordBit15()` appears twice in that gate | 1 |
| Three subsystems share one functional predicate | action eligibility, EXP/LP award and party control, each read independently in separate blocks | 1 |
| The actor initialiser writes the roster with the same eviction discipline | `00266744`–`00266792` in `00266530`: unsigned `cmp edx, 3`, occupant cleared and marked `0xFF` / `3`, this record installed, `+0x12` / `+0x0F` set | 1 |
| The roster is 32 bytes | `movdqu` pair at `0026DB52` / `0026DB5A` in `0026DB30` clears `0209A1F0`–`0209A20F` and nothing beyond | 1 |

**How the third site was found.** Not by searching for the pattern — by reading the party
suppression body for its own sake and recognising a mask documented fifteen blocks earlier.
Recording exact constants rather than paraphrasing them is what made that recognisable.

## 9. Related

- [`../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`](../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md) — the per-area waiver, called directly here
- [`../13-Rewards-Progression-Economy/experience-and-license-point-award.md`](../13-Rewards-Progression-Economy/experience-and-license-point-award.md) — the same predicate gating rewards
- [`../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md`](../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md) — BattleUnit identity behind roster actors
- [`../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) — spawn distance walks these same four slots

## 9. Falsification pass 2026-09-02

**Attack chosen.** Two things here are directly checkable: the claim that **the roster is four
pointers** — which is worth doubting, because FFXII's *active* party is three — and §7's own open
question **O-2**, what the gate in front of the whole suppression recompute actually tests.

### SURVIVED: the roster really is four

Both accessors bound identically, and both index one base:

```c
bool PartyRoster_IsFourSlotIndex(uint i)      { return i < 4; }

undefined8 PartyRoster_GetActorBySlot(uint i) { if (i < 4) return (&DAT_0209A1F0)[i]; return 0; }

void *PartyRoster_GetActorBySlotOrCurrentFocus(int i)
{
    if (i < 0)  return currentFocus;          // negative index = whoever you control
    if (i < 4)  return (void *)(&DAT_0209A1F0)[i];
    return NULL;
}
```

`< 4` appears in all three, the array base is `0209A1F0`, and the negative-index behaviour is
exactly as documented. **Four is not a mistake for three** — ~~the active party is three, and the~~
~~fourth slot is what a guest occupies.~~ the active party is four, and a guest takes the first free of indices 3, 2 and 1 *(corrected 2026-10-02, OPUS: `003170E0` walks map 3 from index 3 down while the index is above 0, `0031711A`–`00317157`; §1 of this page says four slots)*.

### O-2 ANSWERED: the gate is a shared "mode == 2" predicate

`FUN_00303EC0` is four lines:

```c
bool FUN_00303ec0(void)
{
    return BattleRuntime_GetMode0To5FromFlagsAndFieldBit15() == 2;
}
```

It is a thin predicate over `0030D9A0`, whose GFZ name says it yields a **mode in `0..5` derived
from flags and field-record bit 15**. So the whole suppression recompute is gated on the battle
runtime being in **mode 2 specifically**.

**It is not a party-local helper.** `00303EC0` has **six callers**, spanning four subsystems:

| Caller | |
|---|---|
| `PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`) | this document's subject |
| `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`) | the canonical input arbitrator |
| `BattleUnit_ApplyUnitDefinition` (`0023A570`) | Actor/Combat |
| `00235EA0`, `00320230`, `0035BC50` | unnamed |

A **seventh** site tests the same thing without the wrapper: `FUN_00313DB0`, the presentation-ready
ring consumer read on 2026-09-02 during the AH-6 pass on
[`../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`](../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md),
calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15()` directly and branches on `== 2`.

**The ladder is now fully read** and documented as its own system:
[`../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`](../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md).
The key result for *this* document: **mode 3 is the field-bit-15 case and is tested before mode 2**,
so setting an area's bit forces mode 3 and every `== 2` test stops matching. The per-area waiver is
**priority pre-emption inside the ladder**, not a parallel exemption check.

**Mode 2 is therefore a distinguished engine state**, tested by party control, input arbitration,
unit definition and presentation alike. ~~What mode 2 *is*, and the full `0..5` enumeration, is **not~~
~~established** — registered as **O-4**.~~ *(answered: mode 2 is the chocobo ride and the ladder is read in full — O-4, the mode ladder page §2c and this page's `00303EC0` row in §3; 2026-10-02, OPUS)* Naming it "in battle" is the obvious reading and is
deliberately not asserted.

### The connection to field-record bit 15

The mode function's own name derives it from **field-record bit 15** — the same field this database
has repeatedly found at the centre of engine-wide gating. Its accessor
`FieldData_GetActiveFieldRecordBit15` was shown in
[`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md)
§9 to have **the widest subsystem reach of any gameplay function in the executable** (13
subsystems).

That makes the chain in §2 more coherent than it looked. Control suppression does not merely happen
to test the same `0x80000003` mask as acting and earning — **it is gated by a mode derived from the
same field bit those checks also consult.** One authored per-area bit reaches input suppression
through two independent routes: directly in the functional predicate, and indirectly through this
mode. That is why §6's note that suppression is *"per-area waivable"* holds.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Audio — SERVICE, not read.** A 360-byte function this page cites calls a 13-byte Audio-filed stub.
- **Actor - SERVICE (1 edge).** `00266530` reaches bodies filed to Actor: `00265B60` (PresentationState) - shared machinery across the layer boundary, no shared ownership.
- **ActorEntity - CLIENT and SERVICE (91 edges).** `002367A0`, `0023A570` are also called by bodies filed to ActorEntity: `0031B810`, `00300E40`; `0023A570` reaches bodies filed to ActorEntity: `00236A60`, `00322050` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (9 edges).** `0030D9A0`, `00313F60` are also called by bodies filed to combat action: `002FFCF0`, `00313DB0`, `00319F50` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (5 edges).** `0032E520` is also called by bodies filed to core runtime: `0022B6E0`; `0018EEE0`, `00253C70`, `002628B0` reach bodies filed to core runtime: `001A1470`, `001EDE70`, `00229EE0` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (16 edges).** `002367A0` is also called by bodies filed to Gameplay: `00312B40` (CombatAction); `002367A0`, `0023A570`, `00303EC0` reach bodies filed to Gameplay: `00322C50` (Combat), `0030D9A0` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT (1 edge).** `0031B810` is also called by bodies filed to items/equipment: `00309FB0` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (76 edges).** `002367A0`, `0023B040` are also called by bodies filed to movement: `00312730`, `00326BB0`, `00234520`; `002628B0` reaches bodies filed to movement: `00263560` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (4 edges).** `0032E520` is also called by bodies filed to resource: `0024AC30`; `002628B0`, `0032E520` reach bodies filed to resource: `0032E520`, `0032E070`, `0046DFE0` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (2 edges).** `003135C0`, `0031B810` are also called by bodies filed to rewards/progression: `002F8BB0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (42 edges).** `00263750` is also called by bodies filed to script VM / native bridge: `003415D0`, `00341CB0`, `00342250` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT and SERVICE (9 edges).** `0023A570`, `00307140`, `00313F60` are also called by bodies filed to spawn/encounter lifecycle: `0023A3B0`, `00306F00`, `00234DA0`; `0023A570` reaches bodies filed to spawn/encounter lifecycle: `00236100` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (5 edges).** `00265680`, `002E8100`, `00313F60` are also called by bodies filed to status/periodic terminal: `00310DB0`, `00320450`, `00329A20` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - SERVICE (1 edge).** `00253C70` reaches bodies filed to story/event: `0032A8A0` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `0031B770` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — SERVICE.** `0023A570` on this page calls `BattleStats_InitializeDefinitionRecord`, owned by that layer. What it reaches is the `0x1C8`-byte record initialiser, and it states the sentinels: `qword[+0x50]` becomes `-1`, `word[+0x58]` and `word[+0x1C3]` become `0xFFFF` and `byte[+0x1C5]` becomes `0xFF`, after which the definition id's **high byte** selects which authored table its low byte indexes; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Save_Load_Settings — SERVICE.** `0026DB30` on this page calls `SaveImage_GetPersistentPayloadBase`, owned by that layer. What it reaches is a 20-byte accessor returning `002EF640() + 0x200` - **the base the persistent flag banks are indexed off**, so those banks live inside the save payload; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — MECHANICAL (SWE2-EC7-175, 18 edges).** `0060F6B0` and `0016D6A0`, helpers this page's `001889C0` runs, are called by `0079C140`/`007A02F0`/`007A05D0` and the `0086Cxxx`/`0035Exxx`/`0046DD50` set of that layer — input bodies share the same field-set and guard helpers; pure fan-in, not a shared responsibility.

**Presentation — MECHANICAL (SWE2-EC7-175, 14 edges).** `005DC190`/`0060D4F0`/`0060F6B0`/`0016D6A0`, all run by this page's `001889C0`, are also called by `00187950` and the wider `0018/0019/002B/0042xxxx` render set — presentation bodies share the string-build and field helpers; pure fan-in, not a shared responsibility.

**UI — CLIENT (SWE2-EC7-175, 22 edges).** `0018EEE0`, which this page documents as the glyph-record builder, calls this page's `001889C0`; `002778C0`/`00292B70`/`002BE0xx`/`0028E240`/`0035D380` of that layer also reach the shared `0016D6A0` helper — the interface layer consults this page's functions, not a shared responsibility.

## The `0023B040` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`0023B040` (447 B) is this page's subject — the leader-battle-state
suppression recompute. The seed is `esi = [02089340] & 0x40 ? -1 : 0`
(`0023B050`–`0023B063`); `00303EC0`/`00313F60` bail out of battle
(`0023B06C`/`0023B079`); `003272A0` resolves the leader record, `[rax+8]` →
`002E8100` → `ebp`, `[rdi+0x698]` stats `+0x64 | +0x3C` vs `0x80000003` →
`00313F60` else `esi = -1` (`0023B0A2`–`0023B0C7`); `[02089340] & 0x600` and
the `0x400000000000` bit feed the result; `00322600` ×2 and `00322920` ×2
classify ids (`0023B0ED`–`0023B118`); `003135C0`/`003137F0`/`0031B770`/
`00313F60`/`003592C0`/`00359200`~~/`0036FFE0` ×2, `[0208E6B8]` store~~
~~(`0023B22F`–`0023B238`),~~ then tail `0026BD40` publishes ~~`ebx & 1`~~ the inverse of bit 1 of `ebx` *(corrected 2026-10-02, OPUS: `0023B1E1 shr ebx, 1` / `0023B1E3 not ebx` / `0023B1E5 and ebx, 1` before the tail; the `0036FFE0` pair and the `[0208E6B8]` store at `0023B22F`–`0023B238` belong to the next function, `0023B200`, past this one's last instruction at `0023B1FA` — §2's correction block already says NOT bit 1)* into
`0209A2C5` (`0023B1FA`).

| member | role | interior |
| --- | --- | --- |
| `0026BD40` (10 B) | the publisher — `setne [0209A2C5]` (ecx ≠ 0 → 1) | [`0026BD42`](../_index/ADDRESS-INDEX.md) |
| `00322600` (36 B) | id-set membership — `ecx - 0x2006 ≤ 0x36` then `bt 0x7A000000000001, rcx` (`00322600`–`00322619`) | [`0032260B`](../_index/ADDRESS-INDEX.md) |
| `00322920` (36 B) | the inverted twin — `ecx - 0x2001 ≤ 0x30` then `bt 0x1000000000101, rcx`, returns 1 when *not* set (`00322920`–`00322939`) | [`0032292B`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00303EC0`, `00313F60`, `003272A0`,
`002E8100`, `003135C0`, `003137F0`, `0031B770`, `003592C0`, `00359200`~~,~~
~~`0036FFE0`~~ *(corrected 2026-10-02, OPUS: `0036FFE0` is called by `0023B200` at `0023B204` and `0023B221`, not by `0023B040`)*.


### Interior citation — frontier hub `00359200` (2026-09-18, SWE2-EC7)

`00359200` — 76 B, 5 callers, `PartyControl_SetMovementSuppressionBit`: the
mask setter itself — `ecx` nonzero sets bit `edx` of ~~`dword[022C6FFC]`~~ `dword[022C8000]` *(corrected 2026-10-02, OPUS: `00359204` resolves to `022C8000`, as the correction at this section's end says)* via
`or eax, edx` at [`00359217`](../_index/ADDRESS-INDEX.md), zero clears it;
when the mask is nonzero it resolves ~~`003588B0(dword[022C6FF0])`~~ `003588B0(dword[022C7FE0])` *(corrected 2026-10-02, OPUS: `0035922B` loads `022C7FE0`)* and tails
`0026D6D0` on the record.
### Interior citation — frontier hub 0026D6D0 (2026-09-18, SWE2-EC7)

**0026D6D0** (`Actor_StopRequestedMovement`, 26 B, 4 A-measured callers) — the suppression path's zeroing half. Clears the unit's requested velocity on `[rcx+0x44]`: `mulss xmm0, [rip+0x2b796]` at `0026D6DB` loads **0.0f** (`0051AE78`), stores `0.0` to `[+0x44]/[+0x48]/[+0x4C]`, then tails `0026D6F0` — the `Actor_RequestMovementStop` base that flags the stop. `00359200` (the suppression setter read here 2026-09-16) calls this as its end; the control-suppression bit now has both halves: the gate that sets it (`00359200`) and the zero that executes it. In-scope: `0.0` store pair [`0026D6DB`](../_index/ADDRESS-INDEX.md); tail `jmp 0026D6F0` [`0026D6E4`](../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## CONTRACT — when a party member has a follow destination (2026-09-19, OPUS)

*Two functions state this between them, and every clause below cites a field the type store already
declares. The slot array they share is now declared as `PartyFormationSlot`,
`ARRAY 0x022C7E00 stride=0x60 count=4`.*

### Producer — `PartyFollow_SolveFormation` (`00338490`)

It walks slots `0..3` (`cmp esi, 4` at `00338686`) and **skips** a member on any of three gates:

| gate | test | field |
|---|---|---|
| no unit for the index | `BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`) returns null — `003385CD` | — |
| status bits set | `(statusWord1 \| statusWord2) & 0x80000003` — `003385DA`–`003385E6` | `BattleStatsRecord +0x64`, `+0x3C` |
| the member IS the leader | `cmp rbx, rax` against `BattleUnit_GetPartyLeader` (`003272A0`) — `003385F1` | — |

A member that passes all three gets a slot: its `slotIndex` as the key, a homogeneous position, its
angle around the leader wrapped to `[0, 2*pi)`, and a `BattleUnit*`.

**The status test reads TWO words and ORs them**, which is exactly what `BattleStatsRecord +0x3C`'s
own row states — *"presence is `+0x3C` or `+0x64`"*. The mask is `0x80000003`: bits 0, 1 and 31.

### Consumer — `PartyFollow_LookupDestination` (`00339A60`)

It returns **no destination** on any of three gates, then searches:

| gate | test | field |
|---|---|---|
| no party leader | `BattleUnit_GetPartyLeader` returns null — `00339A78` | — |
| the querying unit IS the leader | `cmp rax, rbx` — `00339A81` | — |
| the leader is not a party unit | `cmp byte [leaderStats + 5], 1` — `00339A97` | `BattleStatsRecord +0x05 kindByte`, *"0 party, 1 spawn-backed"* |

then walks `022C7E00` to `022C7F80` in `0x60` steps comparing each slot's `+0x00` against the unit's
`BattleUnit +0xEA9`.

### Invariants and an asymmetry worth recording

* **The leader never occupies a slot.** Both sides exclude it, independently.
* **The array is keyed, not positional.** The consumer searches by slot index rather than indexing
  by party position, and the producer writes `0xFF` to all four `+0x00` bytes before each solve, so
  a stale slot cannot be matched.
* **The producer ASSUMES `BattleUnit +0x698` is non-null; the consumer CHECKS it.**
  `003385D3` dereferences the stats record with no test, while `00339A8E` tests it and skips the
  kind check when it is null. Same field, two different assumptions about it in one subsystem —
  recorded as an edge rather than resolved.

  **NARROWED, not closed (same pass).** `0031B810` does not itself return a unit: it maps a party
  index to a **selector byte** read from `BattleSystemState +0x5A5A` -- `movzx eax, byte [rax +
  rbx*2 + 0x5a5a]` at `0031B841`, against the declared `slotMapClass1 uint16[9]`, *"nine 2-byte
  entries"*, read with exactly that `*2` stride -- and then tail-jumps to `0x2367A0`, which performs
  the lookup. On the failure path it substitutes `0xFF`. So the producer's null test guards the
  **`0xFF` selector**, not a missing stats record, and the question of whether a returned unit can
  lack one belongs to `0x2367A0`. The asymmetry stands; its cause is now one function further on.

  **RESOLVED as an INVARIANT (same pass).** `0x2367A0` is
  `BattleUnit_FindByDefinitionSelector`. It scans the unit pool -- `mov rbx,[rip->0208E688]`, which
  is exactly `BattleUnit`'s declared route base `PARRAY 0x0208E688`, with the count at `0208E6A0` --
  and at `002367D3` it loads each unit's `+0x698` and **skips the unit when that pointer is null**
  (`test rax, rax` / `je` at `002367DD`) *before* any comparison.

  So units with a null stats record DO exist -- otherwise that test is dead code -- and **this
  lookup can never return one**. The producer's unguarded `mov rcx,[rax+0x698]` at `003385D3` is
  therefore safe by construction, and the consumer's null test at `00339A8E` is also correct,
  because it guards the **party leader**, which arrives from `BattleUnit_GetPartyLeader` and carries
  no such filter.

  **Both functions are right, and the asymmetry is explained by provenance rather than by one of
  them being wrong:**

  > **INVARIANT.** Any `BattleUnit` obtained through `BattleUnit_FindByDefinitionSelector`
  > (`002367A0`), and hence through `BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`),
  > has a non-null `+0x698`. A unit obtained any other way does not carry that guarantee.

  **The whole function was read before claiming that.** `002367A0` has exactly one success path,
  `00236810` (`mov rax, rbx` / `ret`), reachable only after the `test rax, rax` / `je` skip at
  `002367DD`; the only other exit is `00236803` (`xor eax, eax`), which returns null. There is no
  second path that returns a unit, so the guarantee is structural.

  **And the engine does not rely on it.** Sweeping all 36 direct call sites of the two lookups: 28
  go on to load `+0x698` from the returned unit, and **24 of those 28 null-test the loaded stats
  pointer anyway**. Only 4 use it unguarded. So both styles coexist, and the dominant one is
  defensive.

  *That matters for reconstruction more than the invariant does.* A reimplementation may drop those
  24 checks and still be correct by the invariant -- and it would no longer match the engine's
  control flow at 24 sites. **The guarantee is real; depending on it is a choice the original code
  mostly declined to make.**

  *(Method note: the first pass of this sweep reported "29 of 29 guarded" because it counted the
  `test rax, rax` on the RETURNED UNIT -- which every caller needs, since the lookup can return
  null -- as a test of the stats pointer. Two different tests, one register apart. Re-run against
  the loaded value, the split is 24 / 4.)*

  **And the four are not scattered -- they cluster on the party-index entry.**

  | site | reached via | what it does with the stats record next |
  |---|---|---|
  | `003385D3` `PartyFollow_SolveFormation` | `0031B810` | `mov edx,[rcx+0x64]` / `or edx,[rcx+0x3c]` |
  | `00388DFC` `FUN_00388D50` | `0031B810` | `mov eax,[rcx+0x64]` / `or eax,[rcx+0x3c]` |
  | `0030F275` `AiOrder_BuildCandidateTargetBufferFromStorage` | `0031B810` | loads a second `+0x698` |
  | `00326C77` `FUN_00326BB0` | `002367A0` | `movzx edx, byte [rcx+4]`, the definition row index |

  **Three of the four come through `0031B810`**, the narrow party-index entry, rather than the raw
  selector lookup -- so it is that path's callers who treat the result as trusted. And the first two
  run a **byte-identical status gate**: the same `(statusWord1 | statusWord2)` read this contract
  documents for the formation solver, in a function that is not the formation solver.

  *`FUN_00388D50` is therefore a second consumer of the same party status gate, and a candidate for
  the same treatment this page gave `PartyFollow_SolveFormation`. Named here rather than followed,
  because it is a different subsystem's page to write.*

  *Two things fall out of that. `slotMapClass1`'s `0xFF` is the same "no entry" sentinel this
  subsystem uses for `PartyFormationSlot +0x00`, and its census already records the check --
  `cmp byte ptr [rax + rdi*2 + 0x5a5a], 0xff` at `0031BC43`. And the declared field was confirmed
  by a consumer reached from an unrelated direction, at the declared stride.*

**NOT CLAIMED:** what the three `movaps` vectors at slot `+0x30`, `+0x40`, `+0x50` hold, or what the
second float at `+0x24` is. They are declared by width and access only.

*Evidence: static disassembly of `00338490` (4,101 B) and `00339A60` (390 B). The array's base,
count, stride and key are each established twice — by the producer's four `0xFF` sentinel writes and
`cmp esi, 4`, and by the consumer's `lea` of `022C7E00` and `022C7F80` with `add rax, 0x60`;
`022C7E00 + 4 * 0x60 = 022C7F80`.*
## The movement locks: one dword and four bytes, by owner (FABLE, 2026-09-19)

*Answers the open item on [the active-party page](active-party-reserve-and-the-moment-the-leader-changes.md) §9 - "what
`022C8000` and `022C8004[4]` are for" - and places `00359250`, one of FRONTIER's uncited bodies. Static; the four
setters, the three script doors and the consumer's window `00358D9B`..`00358E9E` read whole, plus whole-image RIP sweeps
of `022C8000`..`022C8007`; one script census.*

The leader's stick is filtered by **two separate lock words**, and every source of a lock owns its own bit or its own
byte, so that one source releasing its lock cannot release another's.

**`022C8000`, a dword - "stop".** The setter `00359200(on, bit)` sets or clears one bit. Its one reader is the stick
consumer, at `00358DAA`: while **any** bit is up, the requested speed is forced to zero before anything else looks at
it. The bits, from the five call sites:

| bit | owner | site |
|---|---|---|
| 0 | the script: **`setuclockstatus(on)`**, call `0x03C0`, door `00347E00` (25 B) | `00347E14` |
| 1 | the leader's battle state - this page's §2 recompute, internal mask bit 0 | `0023B1DC` |
| 2 | the event lock `00307140(on)` | `003071C7` |
| 3 | **actor-manager slot 3 is loaded**: set, with the leader's requested speed zeroed first, when slot 3's definition payload is bound (`0026CC81`..`0026CCBA`), and cleared when slot 3 is unloaded (`002628F0`..`002628F9`; [the manager request queue](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)). *Which of the five managers slot 3 is was not established here* | |

**`022C8004`..`022C8007`, four bytes - "which parts of steering".** Each byte belongs to one owner; the consumer ORs
the four (`00358DDF`..`00358DF4`) and tests three bits of the result:

| bit of the OR | while set, the stick consumer does not... | window |
|---|---|---|
| 0 | hand the actor its speed and start the move | `00358DFB`..`00358E1B` |
| 1 | turn the actor to face the stick's heading (a turn otherwise limited to 0.3927 rad - 22.5 degrees - a call) | `00358E3E`..`00358E87` |
| 2 | set the actor's desired movement heading | `00358E8C`..`00358E99` |

| byte | owner | setter |
|---|---|---|
| `022C8004` | the script: **`setucpcmovelockstatus(bit, on)`**, call `0x03E1`, door `0034E580` (50 B) | `00359250` (103 B) |
| `022C8005` | the leader's battle state (internal mask bit 2 -> bit 1, §2), and the debug call `0x2084` `debug_TkRequireUCPCMoveLockStatus`, door `0050D2B0` | `003592C0` |
| `022C8006` | the event lock `00307140`, bit 1 only (`003071CC`..`003071D7`) | `00359330(byte, bit, on)` (97 B) |
| `022C8007` | **nobody** - the generic setter's one caller passes byte index 2, and no other store reaches it in the sweep | - |

All four setters end the same way: if the word they just wrote leaves a lock standing - any bit of the dword, bit 0 of
the OR of the bytes - they resolve the leader's packed handle `022C7FE0` and tail-call the stop routine `0026D6D0`, so
a lock takes effect on the frame it is set, not on the next stick sample. The party-focus reset `003590E0` clears both
words.

**What the scripts do with them** ([census](../_experiments/evidence/uc-lock-script-uses/census.out.txt), 1,114 scripts;
positive control 3,838 `mapsoundplay(`): **one script uses them at all** - `naf_a02`, the opening's tutorial, in an
actor named *key restriction* with three functions: *key restriction with the menu allowed* (`setuclockstatus(1)`),
*key restriction just before targeting* (`setuclockstatus(1)` and `setucpcmovelockstatus(0..2, 1)`), and *key
release* (all four back to 0). Everything else in the game that stops the player goes through `ucoff()` or through the
engine-side owners above. The script's own byte is, in shipped data, a tutorial device - and since the engine-side
owners only ever set bit 1, **bits 0 and 2 of the steering bytes are never set outside that tutorial**.

**The other two unknowns of that list, the same day.** `022C7FEC` is a **debug player-character override**: its one
setter `003593A0` (97 B, read whole - it stops the leader, or the previously overridden actor, before switching) is
reached only from the debug script calls `0x2032 debug_setdebugpc` and `0x2033 debug_cleardebugpc`, neither of which
any of the 1,114 shipped scripts uses; while it is non-zero the stick consumer and the per-frame focus update
(`00358EE0`, 175 B, read whole) drive *that* actor instead of the leader `022C7FE0`. `022C7FE8` is the **intervention
camera's subject**: the script call `0x02B9 setinterventioncamera(actor, on)` (door `00353530`, 38 uses in 19 scripts)
stores an encoded actor handle through `00359410` (154 B, read whole), which also switches a camera slot on or off,
and the focus update then processes that actor on camera channel 1 after the leader on channel 0. What the camera
side does with it was not read.

**Resource - INCIDENTAL (crossing).** The manager unload that clears bit 3, 002628B0, also calls a Resource-layer routine
(0032E520) elsewhere in its 1,689 bytes; only its window `002628E4`..`002628FE` was read, and the edge is recorded
because citing the window imports it.

**Correction of the hub note above (2026-09-18, SWE2-EC7).** `00359200` does not write `dword[022C6FFC]` or resolve
`dword[022C6FF0]`: the displacement at `00359204` is `0x1F6EDF6` from `0035920A`, which is **`022C8000`**, and the
handle it resolves at `0035922B` is **`022C7FE0`** - the addresses this page's §2 already uses. The note's two
figures are low by `0x1004` and `0xFF0`.

`001889C0` (247 B) is the two-string field-set `0018EEE0` runs on its `rbx` record: `dword[rcx+0xC30]` selects `[rcx + rax*8 + 0xB08]` and `[rcx+0xB58]` supplies the second source, both `005DC190`-built into stack strings; then `0060D4F0` on `[rbx+8]` fires three times (slots `1`, `7` and the first string), `0060DB50` applies the second and `0060F6B0` closes, `0016D6A0` unwinding both locals - the glyph-record builder's two-field populate.

Interior anchor `001889E8` (function `001889C0`).

`002E0540` (82 B) is the slot-occupancy probe over the `0215F200` table: eight `0x68`-stride rows are scanned (index clamps into 0..7), and a row counts when its `qword[+0]` is set and `byte[+0x3E]`'s sign-fold or `byte[+0x38]` is nonzero - returns 1 on the first live row, the "any slot active" test the cutscene and roster callers share.

Interior anchor `002E0564` (function `002E0540`).
