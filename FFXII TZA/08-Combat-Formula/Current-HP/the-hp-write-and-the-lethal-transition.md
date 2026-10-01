---
system: The HP write and the lethal transition — where every damage and heal ends, and what happens when HP reaches the floor
category: 08-Combat-Formula
status: AUDITED
owner_layer: PrimaryOwner:CombatFormula
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: BattleStats_ModifyHPAndProcessLethalState (880 B) and eleven helpers, siblings and
    callers disassembled from the shipping EXE with every RIP target computed by a tool; caller
    counts checked with check_caller_claims (control memcpy 632)
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-hp-write-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The HP write and the lethal transition

> One function writes current HP for every combatant, and it is where the rules a player takes for
> granted actually live: you cannot be healed above your maximum, a Diseased character cannot be
> healed at all, a KO'd character cannot be damaged, healing a KO'd character revives them, and
> reaching zero is what KOs you, credits your killer and tells the encounter you died.

## 1. What the player sees

A damage number, a heal number, a character dropping, a character standing back up. Behind every one
of those is a single call: `BattleStats_ModifyHPAndProcessLethalState` (`00300530`, 880 B), given a
**delta** and a set of **flag bits** that say which of its side effects the caller wants. Its
sibling `BattleStats_SetCurrentHP` (`00300520`, 8 B) is the same function reached with an absolute
value: it subtracts the current HP and falls through (`00300520 sub edx, [rcx+0x48]` /
`jmp 0x300530`).

The rules it enforces, in the order it enforces them:

1. **A source that is not allowed to affect this target does nothing at all** (section 2.2).
2. **Damage to a KO'd, Stone or Vanished target is refused** unless the field allows it.
3. **HP cannot fall below the unit's floor** — normally `0` — **and cannot rise above the cap**:
   the maximum, doubled by one status bit, or frozen at the current value by another.
   *Qualified 2026-09-27 (FABLE, Claude Opus 5.5, on `ASTRA-RETURN-FABLE-HP-FLOOR-CAP-PRECONDITION`): both hold only while the floor
   does not exceed the cap. The code tests the floor first and, when it applies, skips the cap (`00300651` /
   `00300654`); otherwise it applies the cap without testing the floor again. A floor set above the maximum
   therefore yields the floor on one path and the cap on the other (section 4).*
4. **Healing a target whose HP was zero revives it** (status KO removed); healing a living target
   does nothing more than the number.
5. **Reaching the floor KOs the target**, records who did it, bumps the spawn record's death
   statistics, tells the group ledger, and plays a death reaction — unless the group completed,
   in which case the completion plays its own.

## 2. Native mechanism

### 2.1 The signature and the flag word

```c
void BattleStats_ModifyHPAndProcessLethalState(
        BKBI    *target  /* rcx: the stats record, unit +0x698 */,
        int      delta   /* edx */,
        BKBI    *source  /* r8: the actor's stats record, may be NULL */,
        uint32_t flags   /* r9d */);
```

**Corrected 2026-09-12 (`OPUS-HPWRITE-ABI-AND-ISOLATED`): four parameters, not six.** This page and
the contract both read `[rsp+0xB8]` and `[rsp+0xC0]` as a fifth and sixth argument. They are the
function's **own spills** of `edx` and `r8`, written by the first two instructions into the `rdx` and
`r8` home slots (`00300530`, `00300535`) and read back through a frame of `0xA8` — seven pushes plus
`sub rsp, 0x70`. A real fifth and sixth argument would sit at `[rsp+0xD0]` and `[rsp+0xD8]`, and
neither is ever touched. All three callers (`00306699`, `0030EB5F`, `0030F3DC`) set four registers,
and the last reserves only `0x20` of shadow space. So **"arg5" is the delta and "arg6" is the
source's stats record**, and every line below has been rewritten to say so.

`00300520` is a two-instruction thunk onto this one: `sub edx, [rcx+0x48]` turns an absolute target
value into a delta and falls through.

Both records are mapped back to their battle units first — `BattleStats_FindOwningBattleUnit`
(`0031B860`) at `00300553` for the source (`rbp`) and `0030055E` for the target (`rbx`); either may
be null and every side effect below checks. The flag bits are unpacked at `00300580`–`00300601`:

| bit | effect | site |
|---:|---|---|
| 0 | **skip both eligibility gates** (section 2.2) | `003005A0`, `00300605`, `0030072F` |
| 1 | skip `00469BB0(sourceRecord, targetRecord)` on the lethal path | `00300588`, `0030079C` |
| 2 | **no presentation event** — the "notify" predicate is `unit && !bit2` | `003005D2` |
| 4 | suppress the reaction publisher `003283D0` | `0030058D`, `003006AC` |
| 5 | when `delta == 0`, supplies `isHeal = bit 5` (otherwise `isHeal = delta > 0`) — **and `isHeal` reaches only the reaction publisher; the outcome branch tests the delta** | `003005AB`–`003005C0` |
| 6 | suppress the *alive* event even when notifying (`!unit \|\| bit 6` blocks it) | `003005E5`, `0030086C` |
| 7 | suppress the number publisher `0028F1F0` | `003005F6`, `003006D8` |
| 8 | the death event is `0x200E` instead of `0x2007`/`0x2008` | `00300846` |

**Where callers get their bits.** `BattleFormula_ApplyTargetResult` (`003112F0`) builds them from
the result record's `+0x2C` at `00311608`–`00311651`: record bit 19 → flag bit 8, bit 10 → bit 5,
`!bit 18` → bit 6, `!bit 6` → bit 4 — and record **bit 3 selects the absolute writer** (`00300520`)
over the delta writer (`00311657`–`00311661 cmovne`), the whole apply gated on record bit 8
(`00311610`). `BattleStats_ReconcileCurrentHpToEffectiveMaximum` (`0030F340`) passes **`0x217`**
(`0030F3D0`: bits 0, 1, 2, 4, 9 — a silent, ungated clamp to the cap it recomputes the same way).
The deferred-HP queue committers `003065D0` (`00306699`) and `0030EB10` (`0030EB5F`) pass `0`.

### 2.2 The two eligibility gates, and the status refusal

With bit 0 clear, **`BattleTarget_HasLow16EligibilitySuppression(targetUnit, sourceUnit)`**
(`0030B9B0`) non-zero returns before anything is touched (`0030060F`–`00300616`). Then, for a
**negative** delta only (`0030061C jns`), a target whose `(+0x64 | +0x3C) & 0x80000003` is non-zero
— statuses **0, 1, 31 = KO, Stone, Vanished** by
[the field-record page](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
§2d — is refused unless `FieldData_GetActiveFieldRecordBit15()` (`00377C20`) says otherwise
(`00300621`–`00300635`). The same `0x80000003` / Bit-15 pair gates the retire, spawn and frame code
this database has read elsewhere; here it means **a downed combatant takes no further damage**.

The second gate is later and narrower: with bit 0 clear and **not healing**,
`BattleTarget_HasHigh16EligibilitySuppression(targetUnit, sourceUnit)` (`0030B8E0`) non-zero
**skips the store** (`0030073A`–`00300747` → `0030074D`) but not the rest of the function. Both
gates are the two halves of one packed mask, read in
[the periodic tick](../../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md)
§"two suppression gates".

### 2.3 The clamp — the floor and the cap

```c
old   = target->hp_48;                              /* 003005EF */
new   = delta + old;                                /* 0030063B-0030063E */
floor = targetUnit ? targetUnit->d_48 : 0;          /* 0030056D-00300579 */
if (new < floor) new = floor;                       /* 0030064C-00300654 */
else {
    st = target->d_64 | target->d_3C;               /* 00300656-0030065F */
    if (st & 0x10000)          cap = max(old, 1);   /* status bit 16: 0030066E-00300677 */
    else { cap = target->max_24;                    /* 00300679 */
           if (st & (1 << 28)) cap *= 2; }          /* status bit 28: 0030067C-00300682 */
    if (new > cap) new = cap;                       /* 00300684-003006A4, recomputed the same way */
}
```

**Status bit 16 freezes HP at its current value (never below 1)** — the external status enum this
database cites at tier 6 names bit 16 **Disease**, and this is exactly Disease's rule. **Status bit
28 doubles the cap** — it is **Bubble** (bank 5 name; help text *brims with life, doubling max HP*,
[the statuses sheet](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md); `EY-1`).
**The floor is a battle-unit field, `+0x48`, not a constant**: a unit with a non-zero floor cannot be
taken below it by any delta — **but the clamp is numeric and is not protection.** The lethal test at
`0030078B` compares the stored HP against *this same floor* (`cmp [rsi+0x48], eax` / `jg`, with `eax`
reloaded from the floor slot at `00300784`), so `hp == floor` — the only bottom value the clamp can
produce while the floor does not exceed the cap (section 4, qualified 2026-09-27) — **falls through to the death sequence**. A non-zero floor *moves* the death threshold up
rather than removing it, which is why the verb below is named a **low limit**. See
[the contract](../CONTRACT-hp-write-and-lethal-transition.md) §6, corrected 2026-09-13. Its writers
are
the definition installer, which zeroes it on every apply (`0023ABDB`), and the script verb
`btlAtelSetHpLowLimit` (`3061` → `005105E0` → `00239832`) — called by 505 shipped scripts, almost
always with 0, ~~and above zero by two: `dst_a01.ebp` (67) and `naf_a02.ebp` (1000)~~ and **23 calls in 14 scripts set a non-zero floor, not two** (corrected 2026-09-13, FABLE, on `OPUS-REQ-FABLE-HPFLOOR-MEANING`, from the 1,114 decompiled `us` scripts): the byte walk counted only integer immediates, and 21 of the 33 "non-immediate" pushes are **float literals**, which the verb truncates (`005105EC` `VMValueStack_PopInt32CoerceFloat32`). Every one sits in a boss's or a mark's own spawn-entry preamble, and **every one of those units registers with event-flag mode 1** — the completion arm that sets the ledger flag and posts `0x2005` ([the group page](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md) §5): Gabranth (`bhm_b01` 35,359; `dgl_g01` 32,024 and 12,809), Vayne and his next form (`bhm_c01` 35,877 and 67,105), Cid (`dor_b01` 18,247; `dgl_g01` 41,046), the Onmyoji (`dgl_n01` 222,462), Judge Ghis (`rsn_a01` 824), Ba'Gamnan (`lus_g01`–`g04`, 796 each), Remora (`naf_a02`, 1000), the Rogue Tomato mark (`dst_a01`, 67) and Gilgamesh as four consecutive actors whose floors are **exactly 4 : 3 : 2 : 1** (`lus_c01` 98,482 / 73,861 / 49,241 / 24,620; `lus_e01` 378,596 / 283,947 / 189,298 / 94,649 — the fractional literals are what an authored fraction of a maximum HP would leave). **So a non-zero floor is how an encounter ends — or changes phase — at an authored HP instead of at zero:** reaching it runs the lethal sequence, which completes the unit's mode-1 group, and the map script resumes. Read in one case: `lus_g01` binds `scratch1_var_2` with `sysDVAR(1, …)`, waits on it with `waitv` during the fight, then suspends battle, plays a blur sequence, calls `bosskillall()` / `zakokillall()` and advances the scenario flag — the Ba'Gamnan fight ends by script at 796 HP. The other thirteen scripts share the floor-plus-mode-1 shape but were not read to their event code
([the field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) §10; `EY-2`). `BattleStats_ReconcileCurrentHpToEffectiveMaximum` computes the identical
cap (`0030F3AC`–`0030F3CB`) and writes `cap − old` through the same function, which is how a
changed maximum or a newly applied bit 16 is reflected in current HP.

### 2.4 The two publishers

Both run only with a target unit (`003006A7`), **before** the store, on the clamped value:

- `003283D0(targetUnit, delta, isHeal, 0)` at `003006C5`, unless flag bit 4 — it gates on
  ~~`002FA3B0(unit->p_10, isHeal*2)`~~ `002FA3B0(unit->p_10)` (`003283EF`), picks a byte from the table at `01EED300` by
  direction and the unit's class (`0032844E`–`0032845E`; class from `ActorRuntime_GetClassNibble`
  `00263C20` when the record's kind byte is not ~~`1`~~ `0`), and hands it to
  `BattlePresentation_EnqueueReactionWithRandomizedVariant` (`003BBD00`) — **the hit / heal
  reaction**. **Corrected and closed 2026-09-12 (`EY-5`):** `002FA3B0(actor)` takes **one** argument and answers "is this actor within **24.0** units, horizontally, of the party leader?": it refreshes a static copy of the leader's position at `01EEBB00`–`01EEBB08` when `BattleUnit_GetPartyLeader` (`003272A0`) returns one, zeroes the copy's Y, zeroes the actor's own Y, and returns `24.0 > |actor − leader|` (`003A1920`, the constant at `008F3128`; `002FA3E2`–`002FA451`); a null actor returns 0, and with no leader the last copy stands — the argument in
  `edx` is the delta, never read, and `isHeal × 2` is `edi`, the table index. The entry enqueued is
  `{actor, |delta|, type 0, kind}`; the byte is `01EED300[ (direction × 2 | lane) + foe ]`, eight `u32` read as bytes — `{2, 4, 1, 3, 6, 8, 5, 7}` — where `direction` is 1 for a gain, `lane` 0 for HP and 1 for the MP / charge lane, and `foe` is 4 unless the unit's stats record is a party record (kind byte `+5 == 0`) or its actor class nibble is 3 (`00328419`–`00328455`). So the kinds are **party: HP gain 1, HP loss 2, MP gain 3, MP loss 4; foe: 5, 6, 7, 8**. The MP writer calls the same publisher with lane 1
  (`00300DAB`–`00300DBA`), and the charge-tier rederive `0030E060` does too, with the tier change as the
  amount, when `flags & 0x410 == 0x400` (`0030E0DA`–`0030E102`).
- `0028F1F0(targetUnit->d_08, old, new, 0)` at `003006E7`, unless flag bit 7 — posts the pair to the
  object `00296280()` returns, or to `002962C0()`'s when that object's `+0xB0` equals the unit's
  handle (`0028F20E`–`0028F246`, into `003F8980`) — **the number**.

Neither publisher runs for a record with no unit, which is why the spawn-time writers (section 5)
are silent.

### 2.5 The store, the source's target-list bit, and the two outcomes

Between the publishers and the store, one bit is fetched from the **source's** side: the entry for
this target in the source unit's target buffer (`BattleTargetBuffer_FindActorWorkIndex` `00316D70`
over `source + 0x778`, entries of 16 bytes) gives `r13 = bit 8 of source[0x788 + idx*16]`
(`00300700`–`00300726`), `0` when either unit is missing. It selects the *variant* of every event
this function dispatches: `0x2005`/`0x2006` alive, `0x2007`/`0x2008` dead.

The store is `00300749 mov [target+0x48], new` ~~— the only write of current HP on this path.~~ — the only store in
`00300530`'s own instructions. *(Qualified 2026-09-28, FABLE, Claude Opus 5.5, following OPUS's 2026-09-25 contract
correction, [contract](../CONTRACT-hp-write-and-lethal-transition.md) §4.)* When the status transition this function calls
(`0030077A` / `003007CF`) runs the unit's stat recompute, HP is stored again, clamped to a cap recomputed from the
current status. The contract §4 and the candidate note name the recompute and its store site. EXP-148 executed that
store, and EXP-093 reached it ([`s23-runtime-per-invariant-exposure`](../../_index/candidates/s23-runtime-per-invariant-exposure.md);
`pkg-gp-hp-lethal` S).

**Heal** — a **strictly positive delta**, not `isHeal` (`0030074D`–`00300784`): `r12` is reloaded
with the spilled delta at `003006B7`/`003006D0`/`003006EE`, one on every path, so `0030074D` tests
the delta. **A zero delta with bit 5 is therefore damage, and cannot revive.** If the old HP was
above zero, done (`00300756`). If it was zero, **revive**:
`BattleStats_ChangeStatusAndProcessSideEffects(target, sourceRecord, status 0, 0,
0, flags, mode 0)` (`0030075C`–`0030077A`) — *clear* KO in mask `+0x64`, by the mode table the
field-record page decoded — and return. **Healing from zero is the only status side effect a heal
has here.**

> **The two thresholds are different fields.** Death is tested against the **floor**
> (`0030078B`, against the floor slot `[rsp+0xB0]`); revive is tested against **literal zero**
> (`00300752`, against `edi`, zeroed at `00300563`, on the pre-clamp HP captured at `003005EF`).
> They coincide only when the floor is 0 — which it is for all but ~~two shipped callers of
> `btlAtelSetHpLowLimit`~~ **23 calls in 14 shipped scripts** of `btlAtelSetHpLowLimit` (§2.3, corrected there
> 2026-09-13; this sentence was left behind until 2026-09-28, FABLE). For those, ~~For the other two,~~ the unit dies at its
> floor and this function's revive arm can never fire for it.

**Damage or zero** (`00300784`): if the stored HP is still above the floor (`0030078E`), the
**alive event** `0x2005 + r13` is dispatched with `r8d = sourceUnit->d_08` (or `0`) — only when
notifying and flag bit 6 is clear (`00300861`–`00300887`). Otherwise the **lethal transition**:

| # | site | what |
|---|---|---|
| 1 | `0030079C`–`003007A8` | `00469BB0(sourceRecord, targetRecord)` unless flag bit 1 — gated inside on `002FA390()` (`002F8E90() & 7`), then `0046AB10(sourceRecord, 0x10, &zeros)` — **the battle event poster**, which posts event `0x10`, "… has fallen." ([the post-result events](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) §2.3, §2.7; superseded note corrected 2026-09-12, OPUS) |
| 2 | `003007AD`–`003007CF` | `BattleStats_ChangeStatusAndProcessSideEffects(target, sourceRecord, status 0, -1, -1, flags, mode 3)` — **set KO** in `+0x64`, refused if already set there or in `+0x38` (the page above, mode 3) |
| 3 | `003007DD`–`003007E5` | `targetUnit->d_30 = sourceUnit->d_08` when there is a source — **the killer's handle**, kept on the unit |
| 4 | `003007E8`–`00300829` | spawn-backed targets (`+0x698`'s byte `+5 == 1`): spawn record `+0x08++` and `+0x0C = seconds` — the death statistics [the group page](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md) §3 reads back |
| 5 | `0030082F` | `SpawnGroup_RecordMemberDeathAndHandleCompletion(targetUnit)` — the ledger; **a completion returns 1 and the function ends without its own event** (`00300836`) |
| 6 | `00300838`–`00300887` | otherwise, when notifying: the **death event** — `0x200E` with flag bit 8, else `0x2007`/`0x2008` by `r13` — with `r8d = sourceUnit->d_08` |

All of steps 3–6 need a target unit (`003007D4`); a record without one is KO'd (step 2) and nothing
else happens.

## 3. Key addresses

| address | size | what |
|---|---:|---|
| `00300530` | 880 B | `BattleStats_ModifyHPAndProcessLethalState(target, delta, source, flags)` |
| `00300520` | 8 B | `BattleStats_SetCurrentHP` — absolute value, falls into the above |
| `00300CE0` / `00300C90` | 351 / 73 B | `BattleStats_ModifyPrimaryResource` / `…SetPrimaryResourceAbsolute` — the MP pair with the same flag bits 0, 4, 5, 7 (`00300D0A`–`00300D3E`; there bit 0 skips only the entry gates — a negative delta re-runs both after the publishers, `00300DDD`–`00300DFE`), [where MP comes from](../../10-Status-Periodic-Terminal/where-mp-comes-from.md) |
| `0030F340` | 172 B | `BattleStats_ReconcileCurrentHpToEffectiveMaximum` — the same cap, written as a delta with flags `0x217` |
| `0030B9B0` / `0030B8E0` | 116 / 109 B | the low / high halves of the eligibility mask — gate 1 / gate 2 |
| `0030E360` | 1,323 B | `BattleStats_ChangeStatusAndProcessSideEffects` — KO set (mode 3) and cleared (mode 0) here |
| `003283D0` | 167 B | reaction publisher → `003BBD00` |
| `0028F1F0` | 112 B | number publisher → `003F8980` |
| `00316D70` | 47 B | `BattleTargetBuffer_FindActorWorkIndex` — the source's entry for this target |
| `00469BB0` | 77 B | lethal step 1, gated by `002FA390`; posts event `0x10` — "… has fallen." — through `0046AB10`, **the battle event poster** ([the post-result events](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) §2.3, §2.7). *Superseded note corrected 2026-09-12 (OPUS); `0046AB10` was read 2026-09-11.* |
| `0031B860` | 83 B | `BattleStats_FindOwningBattleUnit` |
| `00377C20` | 78 B | `FieldData_GetActiveFieldRecordBit15` (via the thunk `00313F60`) |
| `00306F00` | 303 B | `SpawnGroup_RecordMemberDeathAndHandleCompletion` |
| `003299B0` | 83 B | `BattleUnit_DispatchActorPresentationEvent(unit, event, r8d)` |
| `003112F0` | 2,040 B | `BattleFormula_ApplyTargetResult` — the applier, builds the flags from `+0x2C` |
| `003065D0` / `0030EB10` | 361 / 226 B | commit the deferred-HP queue at `022C1F50` (entries: `+8` unit, `+0x10` delta), the first as field-frame step 11 |
| `002352E0` / `0023A410` / `00319F50` / `00329BD0` | | the other callers of `00300520` |

### Fields

| offset | on | meaning |
|---|---|---|
| `+0x48` | BKBI stats record | **current HP** — read `003005EF`, written `00300749` |
| `+0x24` | BKBI stats record | **maximum HP** — the cap base, `00300679` |
| `+0x64`, `+0x3C` | BKBI stats record | the two status masks OR-ed for every test here (`0x80000003`, bit 16, bit 28) |
| `+0x48` | battle unit | **the HP floor** — `0030056D`; `0` when there is no unit |
| `+0x08` | battle unit | the unit's handle — the killer id written to the victim's `+0x30`, and `r8d` of every event |
| `+0x30` | battle unit | **killed by** — `003007E5` |
| `+0x698`, `+0x6A0` | battle unit | the stats record and the spawn record (kind byte `+5`). `BattleUnit_ApplyUnitDefinition` installs `+0x698` as the spawn record `+0x80` and `+0x6A0` as the spawn record for definition ids with high byte 1, and as a `BattleSystemState` element (`*(02EBF190) + 8 + index*0x1C8`) with a null `+0x6A0` for high byte 0 (`0023AA49`–`0023AC01`, resolved 2026-09-10) — which is why the lethal path's spawn-record statistics are behind the `+5 == 1` test |
| `+0x778`, `+0x788` | battle unit (source) | the target buffer: count at `+0x77C`, 16-byte entries from `+0x780`; bit 8 of each entry's second qword selects the event variant |
| `+0x2C` | result record | the applier's flag source: bits 3, 6, 8, 10, 18, 19 for the target's HP call; bits 1, 5, 7, 9, 17 for the source's own HP call (`0031170A`–`00311739`; corrected 2026-09-11) |

## 4. Data structures and formulas

**The clamp**, in one line: ~~`new = min(max(old + delta, floor), cap)`~~ `new = (old + delta < floor) ? floor : min(old + delta, cap)` with
`cap = (st & 0x10000) ? max(old, 1) : (st & 0x10000000) ? 2 * max : max` and `floor = unit ? unit->d_48 : 0`.
*Corrected 2026-09-27 (FABLE, Claude Opus 5.5, on `ASTRA-RETURN-FABLE-HP-FLOOR-CAP-PRECONDITION`): the struck form is the section 2.3 code only
when `floor <= cap`. With a floor above the cap it returns the cap where the code returns the floor: a candidate
below the floor takes the floor and jumps past every cap test (`00300651` / `00300654` to `003006A7`), and a
candidate at or above the floor is limited to the cap with no second floor test before the store at `00300749`. Example,
statuses clear: old 50, max 50, floor 80 - delta 0 stores 80, delta 100 stores 50.*

**The transitions**, which are *not* the clamp and do *not* share a threshold
(added 2026-09-13, `OPUS-HPFLOOR-NOT-INVULNERABILITY`):

```
lethal:  delta <= 0  &&  storedHp <= floor   ->  the six-step death sequence
revive:  delta >  0  &&  oldHp    <= 0       ->  clear KO, and nothing else
```

`storedHp` is `+0x48` read back at `0030078B` *after* the store, which gate 3 may have suppressed;
`floor` is the same `[rsp+0xB0]` slot the clamp used, reloaded at `00300784`; `oldHp` is the
**pre-clamp** value captured at `003005EF` into `[rsp+0x54]` and tested at `00300752` against a
register zeroed at `00300563`. **The clamp guarantees `storedHp >= floor`, so the lethal predicate
is reached at equality** *(while the floor does not exceed the cap; qualified 2026-09-27, see the clamp above)* — a non-zero floor moves the death threshold up rather than removing it,
and because revive still tests zero, a unit with a non-zero floor cannot be un-KO'd by this
function. Implementing `lethal: storedHp <= 0` is the natural mistake and is wrong for every unit
whose floor is not 0.

**The refusal**: `delta < 0 && (st & 0x80000003) && !FieldBit15() → return`.

**The gates**: `!bit0 && Low16(target, source) → return` before everything;
`!bit0 && delta <= 0 && High16(target, source) → no store` — the second test is on the **delta**, so a heal is never gate-3 suppressed.

**The events**: alive `0x2005 + r13` (needs `unit && !bit2 && !bit6`); dead `bit8 ? 0x200E :
0x2008 − r13` (needs `unit && !bit2`, and the group not completing); revive none.

**The status change** — two calls, one function, the mode in the seventh argument:

```
lethal:  0030E360(target, sourceRecord, 0, -1, [0x20] = -1, [0x28] = flags, [0x30] = 3)  set KO
revive:  0030E360(target, sourceRecord, 0,  0, [0x20] =  0, [0x28] = flags, [0x30] = 0)  clear KO
```

## 5. Call chain

```
BattleFormula_ApplyTargetResult 003112F0            record +0x2C bit 8 -> apply HP
  -> bit 3 ? BattleStats_SetCurrentHP : BattleStats_ModifyHPAndProcessLethalState   (call rax, 00311668)
       flags from +0x2C: b19->8, b10->5, !b18->6, !b6->4

field frame step 11: 003065D0  /  BattleSpecialSequence_CommitAccumulatedTargetHp 0030EB10
  -> for each entry of the queue at 022C1F50: ModifyHP(entry.unit->+0x698, entry.delta, [022C1F50], 0)

BattleStats_ReconcileCurrentHpToEffectiveMaximum 0030F340
  -> ModifyHP(rec, cap - cur, NULL, 0x217)                      silent clamp; callers 0030C470, 0030F3F0, 0030F4D0

BattleStats_SetCurrentHP 00300520  <-  Spawn_SetAllSpawnBackedUnitsCurrentHPZero 002352E0
                                       SpawnUnit_FinalizeSpawnEntryActivation 0023A410
                                       BattleUnit_HandleActorTimelineEvent 00319F50
                                       00329BD0

ModifyHP
  -> gate 1: BattleTarget_HasLow16EligibilitySuppression
  -> refusal: 0x80000003 unless FieldData_GetActiveFieldRecordBit15
  -> clamp (unit +0x48 floor; +0x24 cap; status bits 16, 28)
  -> 003283D0 reaction, 0028F1F0 number
  -> gate 2: BattleTarget_HasHigh16EligibilitySuppression (skips the store only)
  -> store +0x48
  -> heal from 0: ChangeStatus(KO, mode 0)
  -> at the floor: 00469BB0 ; ChangeStatus(KO, mode 3) ; unit +0x30 = killer ; spawn record +0x08/+0x0C ;
                   SpawnGroup_RecordMemberDeathAndHandleCompletion ; death event unless completed
```

The script verbs `sethp` / `sethpmode` (`00341B20`, `00340640`) and their family do **not** come
here directly: they tail-jump `004738D0` (`00341B76`, `00340686`). ~~unread — a different HP.~~
**Read 2026-09-12 (FABLE): the same HP, three calls deeper.** `004738D0` (absolute, `sethp` /
`sethp_1f8` / `sethpmode` / `sethpmode_391`) clamps the amount to `003206E0(handle, 0, 100)` —
100 % of max HP `+0x24` — and `00473980` (`sethpratio` / `sethpratiomode`) passes a percentage;
both build a flag word from the verb's option bits (bit 0 → `0x10000000`, bit 1 → `0x20000000`,
bit 2 → `0x40000000`; the absolute forms add bit 31, `0047393A`) and call `00329B70(handle, 0,
amount, flags)`, which resolves the stats record through `ActorHandle_ResolveRegistryEntryByPackedId`
and `ActorWork_GetBattleUnitRaw` only while the battle-state word `02089340` has bit 4
(`00329B7F`–`00329BAE`, else a null record and `00329BD0` returns −1). `00329BD0` then converts a
percentage against max HP (`00329C7F`–`00329CA2`, the `1/100` fixed point) and calls
**`BattleStats_SetCurrentHP` (`00300520`) with flags 0** (`00329CA5`–`00329CAE`) — this page's
writer, both publishers enabled. Mode 1 of the same function is the MP side (`setmp` family, [the MP page](../../10-Status-Periodic-Terminal/where-mp-comes-from.md) CS-4).

## 6. Modding notes

- **To change HP natively, call `00300530` with the flags that describe what you want seen.**
  `0x90` (bits 4 and 7) is a silent write with events; `0x94` adds "no event"; `0x01` bypasses both
  eligibility gates; `0x217` is what the engine itself uses for a bookkeeping clamp. Passing a null
  source skips the killer credit, the target-list variant and the event's `r8d`.
- **Do not write `+0x48` directly if the value can reach the floor or zero.** The revive and lethal
  transitions — KO status, killer id, death statistics, group ledger — happen only through this
  function, and a raw store leaves a unit at its floor that is not KO'd, or at full HP still KO'd.
  *(Was "if the value can cross zero"; corrected 2026-09-13 — the lethal threshold is the floor,
  and only the revive threshold is zero.)*
- ~~**To make a unit unkillable, raise its floor** (`unit + 0x48`) rather than intercepting damage:
  every delta is clamped to it before anything else runs, and healing still works above it.~~
  **WITHDRAWN 2026-09-13 (`OPUS-HPFLOOR-NOT-INVULNERABILITY`) — this advice does the opposite of
  what it says.** The lethal test at `0030078B` compares the stored HP against **that same floor**
  (`cmp [rsi+0x48], eax`, `eax` reloaded from the floor slot at `00300784`; `jg`, so strictly
  greater survives). The clamp guarantees `hp >= floor` *(for a floor not above the cap; qualified 2026-09-27, section 4)*, so the only bottom value it can produce is
  `hp == floor`, and that **falls through into the death sequence** — there is no floor-is-zero
  test anywhere on it. **Raising the floor to 1000 makes a unit die at 1000 HP, not immortal**;
  it moves the death threshold up. The engine's own verb name agrees: `btlAtelSetHpLowLimit` sets
  a *low limit*. Worse, because the **revive** arm still tests zero (`00300752` against `edi`, with
  the pre-clamp HP captured at `003005EF`), such a unit's `oldHp == floor > 0` takes `jg` and the
  KO is **not** cleared by a heal through this function. There is no known floor value that makes a
  unit unkillable through this path; gate 1 (`0030B9B0`) and gate 3 (`0030B8E0`) are where a
  refusal actually lives. See [the contract](../CONTRACT-hp-write-and-lethal-transition.md) §6, §9.
- **Bit 16 (Disease) freezes HP; bit 28 doubles the cap.** Both are read as OR of `+0x64` and
  `+0x3C`, so either mask suffices.
- **Damage to a KO'd, Stone or Vanished unit is refused by the writer itself** — a mod that wants
  overkill on a downed target has to set field bit 15's condition or pass a positive delta.
- **The deferred queue at `022C1F50` is committed once per field frame** (step 11 of
  [the field frame](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md))
  with flags `0`, so anything queued there shows every reaction and number.

## 7. What is not known

- [x] ~~**The name of status bit 28.** Its mechanic (double the cap) is read; the id-28 help text in
  `listhelp_status.bin` is not decoded here, so the bit stays numeric.~~ **ANSWERED 2026-09-11** —
  Bubble: `status_data.bin` row 28's name reference resolves to bank 5 `Bubble`, and string 120,028
  of `listhelp_status.bin` reads *doubling max HP* ([the statuses sheet](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)). `EY-1`.
- [x] ~~**Who writes the unit's HP floor at `+0x48`**, and whether any shipped script or definition
  sets it above zero.~~ **ANSWERED 2026-09-11** — the installer zeroes it; the verb `3061` sets it;
  two shipped scripts set it above zero (§2.3). `EY-2`.
- [x] ~~**What `00469BB0` / `0046AB10(sourceRecord, 0x10, …)` do on the lethal path.**~~ **`EY-3` ANSWERED 2026-09-13
  (FABLE):** `00469BB0(source, target)` (77 B) builds a zeroed context with `+0x08 = target` (`00469BB6`–`00469BD7`) and posts event **`0x10`** — the row "… has fallen." — through the battle event poster `0046AB10(source, 0x10, &ctx)` (`00469BF2`), **only when `002FA390(target)` is non-zero**, i.e. when the unit classifier `002F8E90(target)` returns 1, 2 or 4 (`test al, 7`, `002FA399`): a party-table unit, an Esper (party-table type ids `0x1B`–`0x27`), or an enemy-table unit whose free-target type is 3 ([the battle record kind byte](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)). Enemy-table units of free-target types 1, 2 and 7 (class 8) and anything else (class `0x10`) fall without the line. `BattleStats_ModifyHPAndProcessLethalState` reaches it at `003007A8` only when its flag bit 1 is clear. The poster's own work — the ten-entry ring, the `0x1C2`-frame window, the row filter and the realiser — is on [the post-result events page](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md). Which of the context's records the realised line names follows the row's slot kinds and is not re-derived here.
  **Half of this is answered (2026-09-12):** the pointer is not something a caller hands through —
  it is **the source's stats record**, this function's own third argument, spilled to `[rsp+0xC0]`
  and reloaded there (see §2.1). What the two callees do with it is still open.
- [x] ~~**What bit 8 of the source's target-buffer entry means**~~ — **`EY-4` ANSWERED 2026-09-11:
  knockback rolled.** `Battle_ProcessActionTarget` copies the result's flag word B bit 3 into it
  (`003075CB`), and that bit is `[02AEDFC8]`, `BattleFormula_RollKnockback`'s outcome, copied by the
  outcome roller (`00389741` / `00389805`) — so `0x2006` / `0x2007` are the knockback variants of
  the hit and death events ([the scratch block](../Scratch-Block/the-formula-scratch-block.md) §2.4).
- [x] ~~**The table at `01EED300`** the reaction publisher indexes by direction and class, and the
  `002FA3B0` gate in front of it.~~ **`EY-5` ANSWERED 2026-09-12 (FABLE):** the eight reaction kinds
  (HP / MP lane × gain / loss × party / foe) and a one-argument "within 24 units of the party leader"
  gate — §2.4, where the gate's second argument and the kind-byte test are corrected.
- [x] ~~**What `004738D0` is**, the HP the `sethp` script verbs write instead of this one.~~ **EY-6 ANSWERED 2026-09-12 (FABLE):** the `sethp` family's entry into `00329BD0`, which reaches **this page's writer** `BattleStats_SetCurrentHP` with flags 0 after a clamp / percentage conversion (§5, the corrected paragraph). Not a different HP.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The flag bits and their sites | `00300580`–`00300601` and each use site in section 2.1 | 1 | PROVEN |
| The applier's mapping from `+0x2C` | `00311608`–`00311668` | 1 | PROVEN |
| `0x217` from the reconcile writer; `0` from the queue committers | `0030F3D0`; `0030668F`, `0030EB51` | 1 | PROVEN |
| Gate 1 returns before anything; gate 2 skips only the store | `0030060F`–`00300616`; `0030073A`–`0030074D` | 1 | PROVEN |
| Damage refused on `0x80000003` unless Bit 15 | `0030061C`–`00300635` | 1 | PROVEN |
| Floor = unit `+0x48`, cap = max / ×2 on bit 28 / frozen on bit 16 | `0030056D`–`00300579`, `00300656`–`003006A4` | 1 | PROVEN |
| The same cap in the reconcile writer | `0030F3AC`–`0030F3CB` | 1 | PROVEN |
| Statuses 0/1/31 are KO/Stone/Vanished; bit 16 is Disease | the field-record page §2d (tier 1) and its cited external enum (tier 6) | 1 / 6 | PROVEN / PROBABLE |
| The two publishers and their suppression bits | `003006AC`–`003006EC`; bodies of `003283D0`, `0028F1F0` | 1 | PROVEN |
| The source target-list bit selects the event variant | `00300700`–`00300726`; `0030087A`, `00300854`–`0030085F` | 1 | PROVEN |
| Heal from zero clears KO; the floor sets KO | the two `0030E360` calls, `0030075C`–`0030077A` and `003007AD`–`003007CF`, against the mode table | 1 | PROVEN |
| Killer id, death statistics, ledger, death event | `003007DD`–`00300887` | 1 | PROVEN |
| A completion suppresses the death event | `00300834`–`00300836` | 1 | PROVEN |
| The delta writer's callers: three direct calls, the `00300520` tail jump, and the applier's register call; the absolute writer's: four direct calls and the applier | `check_caller_claims --addr` (3 `E8` + 1 `E9`; 4 `E8`, control `memcpy` 632); the `call rax` at `00311668` after the two `lea`s at `003114AD`/`003114B4` | 1 | PROVEN |
| The `sethp` verbs go elsewhere ~~— a different HP~~ | `00341B76`, `00340686` tail jumps to `004738D0`; **corrected 2026-09-12:** `004738D0` → `00329B70` → `00329BD0` → `00300520` with flags 0 (`00329CA5`–`00329CAE`) | 1 | PROVEN (route), corrected (destination) |
| What `00469BB0` is: it posts event `0x10`, the "… has fallen." row, through the battle event poster `0046AB10`, only when `002FA390(target)` is non-zero (`EY-3` ANSWERED 2026-09-13; row updated 2026-09-28, FABLE, Claude Opus 5.5) | ~~**not established**~~ `00469BB6`–`00469BF2`, read whole | ~~—~~ 1 | ~~UNKNOWN~~ PROVEN |
| `01EED300` is the eight-entry reaction-kind table; `002FA3B0` is the 24-unit leader-proximity gate | `003283D0` and `002FA3B0` read whole; table bytes read from the image; the three callers' `r8d` / `r9d` (`003006B1`–`003006B4`, `00300DAB`–`00300DB1`, `0030E0F0`–`0030E0FF`) | 1 | PROVEN |
| What `004738D0` is | the script HP setter's entry (EY-6, read 2026-09-12) | 1 | PROVEN |

## 9. Related

- [`../../07-Combat-Action/applying-a-result-to-a-target.md`](../../07-Combat-Action/applying-a-result-to-a-target.md)
  — the applier that builds the flags; it said this function was undecoded, and this page is the decode.
- [`../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
  — KO / Stone / Vanished, the status masks and the six modes of `0030E360`.
- [`../../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md`](../../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md)
  — the two eligibility gates and the periodic credit that also reads bit 16.
- [`../../10-Status-Periodic-Terminal/where-mp-comes-from.md`](../../10-Status-Periodic-Terminal/where-mp-comes-from.md)
  — the MP sibling and the same publishers.
- [`../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md)
  — what the lethal path's ledger call does.
- [`../../13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md`](../../13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md)
  — the reward path the status change's terminal switch enters.
- [`../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
  — step 11, the deferred-HP commit.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

| claim | measured |
|---|---|
| the nineteen stated body sizes in §3 | **19 of 19 exact** |
| the reaction table at `01EED300`: eight `u32` read as bytes, `{2, 4, 1, 3, 6, 8, 5, 7}` | **exact** — `02 00 00 00 04 00 00 00 01 …`, and it is **initialised in `.data`**, not zeroed BSS |
| the clamp's cited addresses `003005EF`, `0030063B`–`003006A4` | every one lands on the instruction § names |
| presence is `+0x64` OR `+0x3C` | `00300656 mov ecx,[rsi+0x64]` / `0030065F or ecx,[rsi+0x3c]` |
| **status bit 16** freezes HP at `max(old, 1)` | `and r8d, 0x10000` / `cmp edx, 1` / `cmovl eax, r9d` |
| **status bit 28** doubles the cap | `bt ecx, 0x1c` / `add eax, eax` |
| "the cap is recomputed the same way" in the over-cap branch | **literally the same three instructions again** at `0030068E`–`003006A4` — the compiler duplicated the whole cap computation rather than reuse `eax` |

### `002FA3B0` is exactly what `EY-5` says, down to the strictness

The `EY-5` correction — one argument, 24.0 units, *horizontally* — holds in every part, and the body
shows how each part is achieved:

```asm
002FA3C8  test  rcx, rcx / jne          ; one argument; NULL -> 0
002FA3E2  call  BattleUnit_GetPartyLeader
002FA405  call  Actor_GetWorldPosition  ; the leader, into 01EEBB00/04/08
002FA40A  mov   dword [01EEBB04], 0     ; the leader's Y, zeroed
002FA426  call  Actor_GetWorldPosition  ; the subject, into [rsp+0x20/24/28]
002FA432  mov   dword [rsp+0x24], 0     ; the subject's Y, zeroed
002FA43F  call  003A1920                ; the distance
002FA444  movss xmm1, [008F3128]        ; 24.0f
002FA44E  comiss xmm1, xmm0 / seta al   ; 24.0 > distance
```

**"Horizontally" is two explicit zero stores**, one per Y component — not an XZ-only distance
routine. And `comiss` + `seta` makes the test **strictly** less than 24.0: a subject at exactly 24.0
answers *no*.

One implementation detail worth recording, because it constrains anything that hooks here: **the
leader's position goes into fixed globals `01EEBB00`/`04`/`08`, not a stack local.** The subject's
goes on the stack. So this predicate writes to shared memory while it runs.

**Not claimed:** nothing here was executed or observed live. The corpus claim in §2.3 — that
`btlAtelSetHpLowLimit` is called by **505** shipped scripts, above zero only in `dst_a01.ebp` (67)
and `naf_a02.ebp` (1000) — was **not** re-run; it needs the script decompiler, not a byte census, and
is left standing as `EY-2` records it. The publishers' downstream (`003BBD00`, `003F8980`) and the
lethal path beyond `00469BB0` were not re-read.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **Input and InputGameplay — CLIENT.** `InputGameplay_ArbitrateDigitalInputAndModalS…` reads the action-permission bit
  both directly and through its thunk, and a 289-byte Input-filed helper reads it too. **Input arbitration consults the
  same field permission the lethal path does.**
- **Items_Equipment_Shops_License — SERVICE and CLIENT.**
  - The 432-byte level-rank function asks `BattleStats_ComputeLicenseDerivedRank`.
  - `BattleFormula_ApplyTargetResult` grants stolen items through `Inventory_ModifyEncodedItemAndUpdateDiscoveryState`.
  - The owner lookup is driven by the equipment and licence setters.
  - The permission bit is read by the unequip path and the owned-count query.
- **Movement — CLIENT.** The small accessors this page cites are read throughout locomotion:
  - the class nibble `00263C20`, by `PartyFollow_SolveFormation` and a 66-byte helper;
  - `BattleUnit_GetPartyLeader`, by `BattleLocomotion_BuildSolverContext`, `PartyFollow_LookupDestination`,
    `PartyFollow_SolveFormation`, `BattleLocomotion_DecodeOrderGoal` and five unnamed bodies;
  - the 3-D distance `003A1920`, by `Movement_UpdateSteeringTowardTarget`, `Navigation_TestSegmentAgainstAuxObstaclesXZ`
    and four more;
  - the permission bit and its thunk, by nine movement bodies;
  - the owner lookup, by two locomotion bodies;
  - the presentation dispatcher, by the stance-bit setter;
  - the event poster `0046AB10`, by a 160-byte client that locomotion reaches.

  Spawn activation `0023A410` publishes the locomotion position.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT.** `BattleUnit_UpdateEngagementStateFlag`, owned by that layer, calls `00377C20` on this page. That caller is the engagement test, which reads the actor's `+0x698` block and tests `+0x3C` OR `+0x64` against its own mask; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — SERVICE.** `00319F50` on this page calls `FUN_001d6ae0`, owned by that layer. What it reaches is a 28-byte forwarder: it resolves an object and tail-jumps with the caller's argument unchanged; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (14 edges through 6 of this page's functions).** The UI layer reaches this page at `00263C20`, `00296280`, `00313F60`, `0028F1F0` and 2 more. `FUN_00296280` is the worked example, read in full - it is a 51-byte linear search over **`0xC0`-byte records** from `0209BF66` to `0209C2BE`, matching `dword[+0x32]` and skipping any record whose own or previous `byte` lacks bit 1 - and it returns the record base, `0x7E` behind the member it matched; **6 of the 12 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — MECHANICAL (SWE2-CONTRACT 2026-09-15, 11 edges).** `AiOrder_EvaluateTargetSelector` shares `0030B9B0`/
`003272A0`/`00377C20` (3 edges); the enmity/perception bodies `BattleEnmity_WriteForCombatantId`,
`BattleEnmity_WriteAllCombatantIds`, `BattleEnmity_AdjustOtherRelevantCombatants`,
`BattleUnit_RebuildPerceptionCandidateCache`, `BattlePerception_RefreshCandidateCacheGeneration`
share `00313F60`; `BattleUnit_UpdateCombatFrame` shares `003299B0`; `AiOrder_EvaluateAndResolveActionTarget`
and `BattleUnit_SelectAndCommitNextAction` share `00377C20`. The lethal transition is read by the AI
through shared unit-state accessors — fan-in, not an AI relationship the write owns.

**Save_Load_Settings — CLIENT.** `00581930`, owned by that layer, calls `002DD7E0` — the
`002DD7E0`/`002DD7B0` pair this page names among its own-context helpers; the save/load layer
consults it for its own write path. Fan-in, not shared ownership. Read from `edges.tsv` 2026-09-17
(SWE2-FRONTIER).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Audio — SERVICE (2 edges).** `BattleFormula_ApplyTargetResult` `003112F0` calls `003A1180` and `002DF220`, the resolve-then-play sound pair. The applier that builds the HP write's flags also plays its bit-14 sound; the sound is not part of the HP write.

**CoreRuntimeScheduling — MECHANICAL (2 edges).** `BattleStats_ModifyHPAndProcessLethalState` `00300530` and the battle event poster `0046AB10` call `GameClock_GetRawTickCounter` `0032A150`. On a lethal change the HP write stores a death timestamp (the tick count divided by 30 times the frame multiplier, `00300805`–`00300829`), and the poster (which posts "… has fallen." for the lethal step) reads the same clock; both only read it.

**Party — CLIENT and SERVICE (16 edges).** `ActorWork_GetBattleUnitRaw` `00263E30` is called by `BattleUnit_ResolveByFocusHandle` `0031B7E0`, `PartyConfiguration_ReconcileRosterFromCurrentSelectors` `003261D0`, `BattleUnit_GetPartyLeader` `003272A0` and `PartyConfiguration_SetSelectorsAndReconcileRoster` `003273D0`; the leader-distance test `002FA3B0` calls `003272A0`, which calls `PartyFocus_GetCurrentPackedActorHandle` `003590D0` and is called by `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040`; `0023B040`, `0031AC00` and `00304180` call `FieldData_GetActiveFieldRecordBit15` (directly or through `00313F60`); `ActorHandle_EncodeRegistryEntry` `003589B0` is called by `PartyRoster_AssignActorToSlot` `00269C70`, `PartyFocus_SelectAndRequestDefaultActor` `00326500`, `VMPartyCommand_SetSecondaryFocusActorFromActorIndex` `00353530`, `PartyRoster_AssignActorAndCommitFocusWhenEligible` `0050C610` and `PartyFocus_EncodeActorAndSetTemporaryControlledActorOverride` `0050D2F0`; and the distance helper `003A1920` is called by `PartyFocus_ProcessActorControlPresentationState` `00358F90`. The heal-reaction test "within 24.0 of the party leader" (`EY-5`) reads the leader through the party layer, and the remaining edges are party bodies sharing the page's actor accessors and the field predicate.

**Rewards_Progression_Economy — SERVICE and CLIENT (11 edges).** The level setter `0030C470` calls `002F8F20`, `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` and `BattleStats_ReconcileCurrentHpToEffectiveMaximum` `0030F340`, and is called by `00317480`; `003112F0` calls `GameState_GetGil` `00253690`, `GameState_SetGil` `00254EE0` and `0030C650`; `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` calls `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` and `00377C20`; `BattleStats_FindOwningBattleUnit` `0031B860` is called by `Reward_ComputeExperienceForRecipient` `002F8BB0` and `0030C650`. A level change ends in the silent HP clamp (`0x217`, one of the three clamp callers in §4), and the defeat-reward path runs the same status change and field check as the lethal transition.

**Script_VM_Native_Bridge — CLIENT and SERVICE (30 edges).** `sethp` `00341B20` and `sethpmode` `00340640` pop their arguments through `VMValueStack_PopInt32CoerceFloat32` `00267E10` (and `00341B20` pushes through `VMValueStack_PushInt32` `00267F90`), and they, `00348C50` and `0034A110` call the absolute setter `004738D0`, while `00340CB0`, `003421D0` and `00349220` call the ratio setter `00473980`; `btlAtelSetHpLowLimit` `005105E0` pops through `00267E10`; twelve verbs, among them `00342150`, `00342D40`, `003438F0` and `00349C90`, call `003589B0`; `00344740`, `00352FA0`, `003537D0` and `00355680` call `00377C20`; and `00343D10`, `00344F80` and `00345C20` call `003A1920`. Authored script sets HP through its own setters, which reach the same HP three calls deeper (§5), and sets the low-HP limit the clamp floor honours; the other verb edges share the page's handle encoder, field predicate and distance helper.

**Status_Periodic_Terminal — SERVICE and CLIENT (46 edges).** The lethal transition sets KO (mode 3) through `0030E360`, which `00300530` calls and which calls `BattleUnit_ResetActionControlForStatusTransition` `00300140`, `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140`, `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`, `BattleStatus_ComputeDefaultShortTimer` `003876D0`, `BattleStatus_ComputeDefaultDwordParameter` `00387730` and itself, and is called by `BattleStats_RemoveStatusMode0` `0030E990`, `BattleStats_AddStatusMode3` `0030EAE0`, `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690`, `0030FED0`, `003112F0` and `BattleSpecialSequence_CommitAccumulatedTargetHp` `0030EB10`; `0030E360` also calls the two eligibility gates `BattleTarget_HasHigh16EligibilitySuppression` `0030B8E0` and `BattleTarget_HasLow16EligibilitySuppression` `0030B9B0`, and `BattleUnit_DispatchActorPresentationEvent` `003299B0` (as `00301140` does); `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls `BattleStats_ModifyPrimaryResource` `00300CE0`, `BattleTarget_ComputeGlobalEligibilityMask` `0030B770`, `BattleTarget_ComputeUnitEligibilityMask` `0030B7F0`, `003112F0` and `00377C20`; the level setter `0030C470` calls `0030F690` and `0030FED0`, and the other two clamp callers `0030F3F0` and `0030F4D0` call `0030F690`; `0030FED0` calls the charge-tier rederive `0030E060`; `003112F0` calls `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130` and `0030FED0`, and `0030E130` calls `003112F0`; `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `0030FED0`; `BattleUnit_ClearPrimaryResourceRecoveryAccumulator` `002FA540` is called by `00300CE0`; `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860` calls `00263E30` and the unit classifier `002F8E90`; `BattleFormula_ApplyGlobalPeriodicDrainModes` `00385CA0` calls `002FA390`; `00313F60` is called by `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450` and `BattleUnit_AddPrimaryResourceRecoveryAccumulator` `00329A20`; and `0031B860` by `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400`, `0030E360`, `0030F690`, `0030FED0` and `00386860`. KO is a status: the lethal transition hands off to the status layer's change routine, which in turn uses this page's eligibility gates and HP clamp, and the periodic HP credit and drains write HP through this page's routine.

## The `003BBD00` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`BattlePresentation_EnqueueReactionWithRandomizedVariant` (`003BBD00`, 649 B)
claims one of the 64 `0x50`-byte reaction slots at `[02B457D0]`, chosen by the
round-robin byte `02B443C0` (`003BBD27`); a null entry returns `0xFF`
(`003BBD4E`). For kind-2 requests (`[rsi+0xC] == 2`) it first requires the
`0035D330(0x1A, [rsi+8])` record's `+0x24 != 0xFF` (`003BBD74`). It then scans
all 64 slots for entries bound to the same actor (`[entry] == [rsi]`,
`003BBDB9`) whose counter word is still under its limit (`+4 == 2` → `< 0x100`,
else `< 0x1E`, `003BBDC4`), bucketing hits by `byte[entry+6]` into four
occupancy flags on the stack. The variant `r14` comes from occupancy: two
buckets → `2`/`4`, single buckets → `1`/`3`, mixed → `rand() & 1` then
`*2 + 1` (`003BBE2E`–`003BBE4A`). `0028FBE0` posts the floating-text event,
and for kind 2 a backwards ring walk bumps `word[+0x3A] += 3` on matching
kind-2 slots and accumulates `max([+0x44] + 3)` into `edi` (`003BBE90`–
`003BBEDF`) before `00506700` populates the slot and `[rbp+0x44]` takes the
stacked counter (`003BBEF2`). The duration is `((rand() & 0x1F) * 0.0444 *
6.0) + 1.0` scaled by the per-variant pair at `00D11600[r14]` into
`+0x14`/`+0x18`, `byte[+0x3E]` records the variant, `02B443C0` advances mod 64,
and the return is `slotIndex | 0x20` (`003BBF61`).

| member | role | interior |
| --- | --- | --- |
| `0028FBE0` (170 B) | the floating-text poster — when `[rsi+0xC] == 0` and `+8 != 0`, resolves the actor id (`003589B0`), looks it up via `00296280`, and on `[[0209BE80]+0x10F78]` dispatches `byte[rsi+0xD]−1` (≤ 6) to tail calls: `00296E90`, or `00297040` with `r8d` 0/1 (`0028FC59`/`0028FC6D`/`0028FC7A`) | [`0028FC2B`](../../_index/ADDRESS-INDEX.md) |
| `00296E90` (58 B) | sets `word[record+0x318] \|= 0x10` and zeroes `+0x350` on the `0x160`-stride presentation record indexed by `00273320(actorId)` (`00296EAA`) | [`00296EB3`](../../_index/ADDRESS-INDEX.md) |
| `00297040` (115 B) | the two other flags — `r8d == 0` → `+0x318 \|= 0x20`, `+0x354 = 0`; `r8d != 0` and `byte[+0x31E] != 3` → `+0x318 \|= 0x40`, `+0x356 = 0` (`00297077`/`00297097`) | [`0029706D`](../../_index/ADDRESS-INDEX.md) |
| `00506700` (433 B) | the slot populator — memsets `0x50`, writes actor ptr/id and kind `+0x3C` = `[rsi+0xC]`, then per kind: kind 0 formats text via `003EFD00` into `+0x40`, `+0x3F` = length, colour from `0xD227A8[[rsi+0xD]]` through `002DD7E0`/`002DD7B0`; kind 1 takes its colour pair from `0xD22780`/`0xD22781[[+0x3F]]`; kind 2 sets `+0x3A = 3`, resolves `002B58B0` for `+0x30`, defaults `+0xC` to `0x80808080` then overrides from `[rbx+0x25]` bit-select (`1`/`0x12`/`0xB6`/`0xF3` → `002DD7E0`), `002B3050` fills `+0x40`/`+0x42` (`00506760`–`005067E5`) | [`00506750`](../../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: `0035D330`, `003589B0`,
`00296280`, `00273320`, `003EFD00`, `002B58B0`, `002B3050`, `0024A5A0`,
`002DD7E0`/`002DD7B0`, `00861EC0`, `00808C40`, and CRT `rand` at `008C3098`.

## Interior citation — frontier hub `0035D330` (2026-09-17, SWE2-EC7)

`0035D330` — 72 B, 67 frontier callers at census; this page already calls it as
`0035D330(0x1A, [rsi+8])`. Interior verified: [`0035D336`](../../_index/ADDRESS-INDEX.md) is
`mov dword ptr [rip+...], ecx` — the first of two global stores (arg1 → a `.data` dword, arg2 →
the next). The body then invokes `0031C5D0` (the 8 KB encoded-id definition resolver — a 32-way
kind switch whose cases validate `[rbx]` kind, resolve the per-kind record through the
`0020E600` handle chain, and fill a result struct) on a static `0x98`-byte out-struct; on a
negative return it reports through `0016D6A0` (`0x800`) and zeroes the struct via `00861EC0`
(`memset`, 0x98 B). Returns `&struct` unconditionally — **the encoded-id definition query
wrapper**: kind + id in, resolved definition record out.

NOT claimed: what kind `0x1A` means at this call site (the resolver's switch handles kinds 1..32)
or the result struct's layout — only the store-resolve-failzero shape is verified.


## Interior citation — frontier hub `0030B9B0` (2026-09-18, SWE2-EC7)

`0030B9B0` — 116 B, 6 A-measured callers;
`BattleTarget_HasLow16EligibilitySubstate`-shaped — the eligibility probe the lethal
transition consults. Interior verified: null-guards on both args (`0030B9C2`–`0030B9CA`),
`0030AB40` counts the relationship candidates and `> 1` arms `edi`
([`0030B9CF`–`0030B9D9`](../../_index/ADDRESS-INDEX.md)), then `0030B770()` +
`0030B7F0(rcx, edi)` produce two word results (`0030B9E2`–`0030B9EE`) and the answer is
`ax || bx` (`0030B9F3`–`0030B9FB`). Either substate suffices.

## SWE2-EC7-21 update (2026-09-18) — `003EFD00` lerp/normalize kernel fragment

`003EFD00` (236 B) is a decimal integer formatter: it counts `edx`'s digits
with a `/5` recurrence (`imul 0x66666667` + `sar 2`, `003EFD30`..`003EFD4D`),
defaults an empty count to 1 (`003EFD5E`), and picks `ecx = r8d ?: digits` as
the field width with `ebp = width − digits` as the pad count
(`003EFD51`..`003EFD75`). `00861EC0` then pre-fills `rdi` with `0x20` (space)
when `r9d==0`, `0x30` (zero-pad) otherwise (`003EFD78`..`003EFD82`), and the
emit loop walks the `00D11CE0` power-of-ten table backwards — `esi /= [r9]`,
`al + 0x30` stored at `r8-1` (`003EFD8C`..`003EFDC9`). Terminates with
`[rdi + rax] = 0` at the computed end (`003EFDE2`). The number-to-text the
damage/value displays share. Callers `00289BD0`/`002AE610`/`002B3770`/`00506700`
— including this page's `00506700` transition-side caller.

## SWE2-EC7-29 update (2026-09-18) — `00296280` `0xC0`-stride keyed scan

`00296280` (51 B) — the `0209BFBE..0209C2BE` `0xC0`-stride scan the UI
crossing above names — compares `dword[rax+0x32]` against `ecx` on any
record whose own flag byte `rax[0]` OR its previous record's
`rax[-0x58]` has bit 1 set (both clear skips the compare); a match
returns `rax - 0x7E` — the record base — else the walk ends at
`0209C2BE` and returns 0. Interior anchor `0029629B` (the `+0x32`
compare). The scan reads the same record band `002962D0` sweeps for the
`+0x32`->`003F8A30` dispatch.

## SWE2-EC7-39 update (2026-09-19) - `002B3770`

`002B3770` (435 B) is an HP-write body - `01F44830`, `0039C4A0`/`0020E600`/`003EFD00` pairs plus `00808C40`. Interior anchor `002B379B` (a `0039C4A0` call).


## SWE2-EC7-63 update (2026-09-19) - `003206E0`

`003206E0` (176 B) is the `003206E0(handle, 0, 100)` HP clamp the lethal-transition page names - `00263E30`/`003588B0` plus `02089340`. Interior anchor `003206FC` (a `003588B0` call).



## SWE2-EC7-66 update (2026-09-19) - `002962D0`

`002962D0` (130 B) is the record-band sweep - `002732E0`/`0028F590`/`003F8A30` plus `0209BFBE`/`0209C2BE`. Interior anchor `00296302` (a `002732E0` call).

