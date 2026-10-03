---
system: Where MP comes from — the walk-regen ladder, the damage gain and the kill bonus
category: 10-Status-Periodic-Terminal
status: AUDITED
owner_layer: PrimaryOwner:Status_Periodic_Terminal + CombatFormula
evidence_tier: 1
registry_slots:
  - "0x02EBF0B8"
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-07
audit:
  passes: 1
  last_pass: 2026-09-07
  last_pass_state: GN160-xiionline-61-self-attack
  last_pass_kind: attack
  crossref_clean: true
  reopened_count: 0
---

# Where MP comes from

> FFXII has no MP potion economy worth the name. MP comes back from **walking**, from **being hit**,
> from **hitting**, and from **killing** — and every one of those four is a row in the same authored
> table, gated by a licence-board effect, and **tripled in about one zone in seven.**

## 1. What the player sees

**MP refills while you move.** The bar creeps up as you cross a map, a point at a time. It is not a
flat rate: the game consults a small ladder keyed on **how much MP you currently have**, and the
ladder says how much walking one point costs.

**Spending MP resets that progress.** Cast a spell and the part-charged next point is thrown away —
you start the next point from nothing.

**Being hurt gives you MP**, in proportion to the size of the hit, on an authored ladder rather than
a flat rate. **Hitting a foe can give you MP too**, and **felling one gives a bonus that scales with
the foe's level** — roughly a quarter of it.

All three of those are **licence-board effects**: without the effect the character gains nothing, and
the two "gain when you hit" routes are *separate* effects that each also require the **action itself**
to be one that grants MP. A physical attack and a spell do not automatically qualify; the action's
own data says whether it does.

**Four rules apply to all of the gain paths:**

- **Damage only.** Healing gives nothing.
- **Across sides only.** Friendly fire gives nothing; so does an enemy hurting another enemy.
- **A delta, not a set.** An action that *sets* HP to a number rather than subtracting from it grants
  no MP to anybody.
- **KO, Stone and ~~Vanish~~ X-Zone stop passive recovery** *(corrected 2026-10-02, OPUS: the predicate is `0x80000003`, ids 0, 1 and 31; id 31 is X-Zone in the thirty-two statuses §2, and "Vanish" there is id 24, Invisible)* — and certain zones let it run anyway.

**And some zones are simply richer in MP.** In 173 of the game's 1,154 fields, every MP gain from
damage is **tripled** and walking recovery is **three times faster**. It is one two-bit number on the
field record, and **a save flag can override it globally.**

**One asymmetry you can see:** MP gained from being hit is announced to the interface. MP gained from
walking is **silent** — the same engine call, with the feedback deliberately switched off.

## 2. Native mechanism

### Which number MP is

`BattleStats_ModifyPrimaryResource` (`00300CE0`) reads and writes a **`short` at BKBI `+0x4C`** and
clamps it against a **`short` at BKBI `+0x28`**:

```asm
00300D69  movsx ebx, word ptr [rsi + 0x4c]     ; live value
00300D83  movsx ecx, word ptr [rsi + 0x28]     ; capacity
00300E00  mov   word ptr [rsi + 0x4c], di      ; store back
```

**`+0x28` is max MP.** The stat rebuild documented in
[`../08-Combat-Formula/where-a-stat-number-comes-from.md`](../08-Combat-Formula/where-a-stat-number-comes-from.md)
writes its output block at **`record + 0x24`**, and its `.ard` column map names `+0x20` HP (`int`)
and `+0x24` MP (`s16`, clamp 999). The two are offset by four — `.ard` `+0x26` Strength lands at
record `+0x2A`, which is the byte the Bow formula reads — so `.ard` `+0x24` MP lands at record
**`+0x28`**, and it is an `s16` in both places.

> **Careful:** `+0x28` in that document's `.ard` column map is **Vitality**. The MP row is `+0x24`.
> They name different structures four bytes apart, and reading the column map as if it were the
> record map gets the wrong stat.

`BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` confirms the pairing independently, at
`002F94FD`: `movsx ecx, word ptr [rax + 0x4c]` is the value its ladder is keyed on.

### The clamp, and the effect that pins MP to zero

```c
newValue = live + delta;
cap = 0;
if (newValue >= 0) {
    if (bkbi[0x6C] >= 0 && bkbi[0x7C] >= 0) cap = (s16)bkbi[0x28];
    newValue = (cap < newValue) ? (bkbi[0x6C] >= 0 && bkbi[0x7C] >= 0 ? cap : 0)
                                : newValue;
} else newValue = 0;
```

`+0x6C` and `+0x7C` are **byte 4 of the two 128-bit effect layers** at `+0x68` and `+0x78`
(see [`Status-And-Augment-Layers/two-layer-effect-model.md`](Status-And-Augment-Layers/two-layer-effect-model.md)),
and the test is on their **sign bit** — bit 7 of byte 4, so **effect id 39** under that document's
`byteIndex = n >> 3, bit = 1 << (n & 7)` convention.

> **Effect 39, in either layer, makes the capacity zero** — and because any positive result then
> exceeds it, **MP is pinned at 0 and cannot be raised at all.** It is not a reduction; it is a floor
> and a ceiling at the same number.

### The rest of the modifier: flags, feedback and the accumulator reset

| flags bit | effect when **set** |
|---:|---|
| 0 | skip the two eligibility masks **at entry** (`BattleTarget_ComputeGlobalEligibilityMask` / `…UnitEligibilityMask`, low halves, `00300D42`–`00300D63`) — a negative delta re-runs both after the publishers **whatever bit 0 says**, testing their high halves (`00300DDD`–`00300DFE`; corrected 2026-09-11) |
| 4 | suppress the publisher at `003283D0` |
| 5 | when `delta == 0`, supplies the direction argument the publisher would otherwise derive |
| 7 | suppress the publisher at `0028F1F0` |

`delta > 0` also calls `BattleStats_ModifySecondaryResource` (`00300BC0`), and — the fact that names
the accumulator —

```c
if (unit && newValue < live) BattleUnit_ClearPrimaryResourceRecoveryAccumulator(unit);
```

> **Any decrease in MP throws away the walk-regen progress toward the next point.** That is what makes
> the `+0x70` float an MP accumulator rather than a generic combat scalar.

One ordering quirk, real and visible in the body: **on a negative delta the two eligibility masks are
re-evaluated *after* the publishers have already been called**, and a non-zero mask returns without
storing. The interface can therefore be told about a decrease that is then not applied. The late
pass is unconditional — flag bit 0 exempts only the entry pass — and it tests the masks' **high**
halves where the entry pass tested the low (`00300DDD`–`00300DFE` against `00300D46`–`00300D63`);
ASTRA's [EXP-061](../_experiments/EXP-061-mp-writer-controls.md) ran the body in isolation with
flags `1` and a global mask `0x00010000`: both publishers fire, nothing is stored, and a mutant
with the late global test removed is rejected. *(qualified 2026-10-02, OPUS, on FABLE's review of ASTRA `ov42-mode17-query-boundaries`: the global mask in that run was a substituted callee. The shipping `BattleTarget_ComputeGlobalEligibilityMask` zeroes its result and writes only the low WORD, so its high half is always 0. On the shipping code the late veto can come only from the unit mask's high half, which is the console's Invincible setting (`+0xC20`) read twice - see "The two eligibility masks" below.)* After the store the order is: the secondary
modifier when the **original** delta is positive (the full delta, not the amount gained), then
the accumulator clear when a unit exists and the new value is below the old (`00300E00`–`00300E25`).

**The secondary resource, read 2026-09-11 (CS-3 corrected).** `BattleStats_ModifySecondaryResource`
(`00300BC0`) ~~reads `+0x4C` and re-enters `00300CE0`~~ does neither: it moves the **`s16` at
`+0x06`** with the same entry gates (`00300BF0`–`00300BFC`), adds the delta, floors at 0, caps at
**`+0x28 × (+0x37 or 1)`, or 0 when either layer's `+0x6C` / `+0x7C` has bit 7** (effect 39;
`00300C10`–`00300C6A`), stores the low word and calls `0030E060(stats, flags)` — the tier
reconciler on [the auto-status page](../08-Combat-Formula/the-auto-status-rebuild.md): when
`+0x28 > 0`, `+0x4E = (+0x37 > 0) ? +0x06 / +0x28 : 0`, stored even when unchanged, with the
retired hook `0016D6A0` (`ret 0`) on a change unless flags bit 1, and the reaction publisher
`003283D0(unit, newTier − oldTier, newTier > oldTier, 1)` when `(flags & 0x410) == 0x400` and the
tier changed. The call graph is `primary → secondary → reconcile`; nothing re-enters. The absolute
wrapper `00300C90` calls the primary with `requested − +0x4C`, then reads `+0x06` *after* that call
and, if the requested value is still greater, calls the secondary with the difference
(`00300CB2`–`00300CC4`) — so an absolute MP write also tops the secondary word up to the request.
EXP-061 ran the five bodies over 27 fixtures (widths, both effect layers, tier changes, both
wrapper branches); what the multiplier `+0x37` is authored from and what the player sees of the
tier remain (`CS-3`, narrowed) — though the consumer is now read: a kind-5 / 6 action spends `max MP × row +0x0A` from the pool and is refused while `+0x4E` is below that count ([the item page](../12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md) §4). [EXP-062](../_experiments/EXP-062-mp-composition.md) drives these
writers from the applier's dispatch on a copy-out's actual output in one retained state (nine
cases): the contracts compose — the owner lookup and both gates are fixtures there, so nothing
about presentation or the accumulator is added.

### The gate: which actions grant MP at all

`Battle_ProcessActionTarget` (`00307300`) is the **only** caller of either gain function:

```c
if ((result.dwResultFlags >> 8 & 1) != 0 && (result.dwResultFlags & TARGET_HP_ABSOLUTE) == 0) {
    gain = ComputeTargetPrimaryResourceGainFromHpDamage(caster, target, result.nTargetHpValue);
    ModifyPrimaryResource(target->pBkbi, gain, 0x10);

    killed = 1;
    if (target->pBkbi && !(outOfPlay(target) && FieldData_GetActiveFieldRecordBit15() == 0))
        killed = 0;

    gain = ComputeCasterPrimaryResourceGainFromHpDamage(caster, target, result.nTargetHpValue,
                                                       action_id, killed);
    ModifyPrimaryResource(caster->pBkbi, gain, 0x10);
}
```

`dwResultFlags` **bit 8 must be set and bit 3 (`TARGET_HP_ABSOLUTE`) clear** (`bt eax, 8` /
`test al, 8` at `00307B0D`). **An action that assigns HP rather than adding to it grants no MP to
either side.**

**This is also where "caster" and "target" are settled, without relying on the ledger's names:** both
calls take the same `(caster, target)` pair, and the *target* function's result is credited to
`target->pBkbi` while the *caster* function's result is credited to `caster->pBkbi`.

**And `killed` is proven to be a kill flag** — it is 1 exactly when the target is now out of play
(`(bkbi[+0x64] | bkbi[+0x3C]) & 0x80000003`, the KO / Stone / ~~Vanish~~ X-Zone (id 31) *(corrected 2026-10-02, OPUS)* predicate from
[`../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`](../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md))
**and** the field's bit 15 does not override it.

### Gain from being hit — `002F91A0`

```c
if (hp_delta >= 0) return 0;                                  /* damage only */
casterSide = caster ? caster->bkbi[+0x05] : 0xFF;             /* 0xFF when absent */
targetSide = target ? target->bkbi[+0x05] : 0xFF;
if ((casterSide == 0) == (targetSide == 0)) return 0;         /* opposite sides only */

gain = 0;
if ((target->bkbi[0x6A] & 0x20) || (target->bkbi[0x7A] & 0x20))
    gain = LookupFactorByHpDamage(target, -hp_delta);

return (fieldSelector() == 2 || fieldSelector() == 3) ? gain * 3 : gain;   /* lea ebx,[rbx+rbx*2] */
```

`+0x6A` and `+0x7A` are **byte 2** of the two layers, and `0x20` is bit 5 — **effect id 21**.

### Gain from dealing damage — `002F9240`

Same side rule. Two independent routes, and **each pairs a character effect with a permission on the
action itself**:

| route | character effect | action-definition flag |
|---|---|---|
| A | `+0x72`/`+0x82` bit 6 → **effect id 86** | row `+0x2C` **bit 3** (`0x08`) |
| B | `+0x6A`/`+0x7A` bit 4 → **effect id 20** | row `+0x2C` **bit 4** (`0x10`) |

The action row is reached the ordinary way — `row = actionId * stride[+0x08] + resolve(rva[+0x0C])`
on `g_pActionDefinitionTableHeader`. **Route A is tried first; if its action flag is clear the code
falls through and tries route B**, so an action can qualify for one route and not the other.

Then the kill bonus, and the same field multiplier:

```c
if (((caster->bkbi[0x6A] & 0x80) || (caster->bkbi[0x7A] & 0x80)) && killed == 1)
    gain += max(target->bkbi->bLevel >> 2, 1);

return (fieldSelector() == 2 || fieldSelector() == 3) ? gain * 3 : gain;
```

`0x80` on byte 2 is bit 7 — **effect id 23** — and the bonus is **`max(targetLevel / 4, 1)`**, using
the **target's** level, integer-shifted.

### The damage ladder — registry slot `0x02EBF0B8`, rows 1–19

`BattleAction_LookupPrimaryResourceGainFactorByHpDamage` (`002FB6C0`), disassembled whole:

```c
if (damage <= 0) return 0;
for (i = 1; i < 0x14; i++) {
    row = base + stride * i;
    if (damage < (u16)row[0x00]) {                  /* 002FB742 cmp ebp,eax / jl */
        prev = base + stride * (i - 1);             /* 002FB799 lea ecx,[rdi-1] */
        return banded(unit) ? prev[0x03] : prev[0x02];
    }
}
row19 = base + stride * 0x13;                       /* 002FB85B imul ebx,edx,0x13 */
return banded(unit) ? row19[0x03] : row19[0x02];
```

**A row is `{ u16 threshold @ +0x00, u8 factorA @ +0x02, u8 factorB @ +0x03 }`**, `stride` from the
table header `+0x08`. The lookup is a **threshold ladder**: find the first row the damage does *not*
reach and take the row **below** it; if the damage clears all nineteen, take **row 19**.

The column is chosen by

```c
banded(unit) = bkbi != NULL && bkbi[0x05] == 0 && (u8)(bkbi[0x04] - 0x1B) <= 0x0C
```

— the **13-value band `0x1B..0x27`** of the actor-type partition in
[`../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md`](../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md).
**That band is not the main roster** — the main roster is `0x00..0x06`. The band is the span that
earns no License Points, so **column `+0x03` serves the band and column `+0x02` serves everyone else,
main roster included.**

### Walking recovery — the **same** slot, rows 20–24

`BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` (`002F9400`) reads `DAT_02EBF0B8` again, at
`002F94DC` and `002F9556`, with the row index **`i + 0x14`**:

```c
carryHome = (bkbi[0x05] == 0) ? &partyState[bkbi[0x04]]            /* stride 0x40 */
                              : &battleSlotState[owner[0xEA9]];
delta = TakeAndClearAccumulator(unit);              /* drains BattleUnit+0x70 */

if (carryHome[0x18] != delta) {                     /* nothing added since last tick -> skip */
    for (i = 0; ; i++) {
        row = base + stride * (i + 0x14);
        if ((s16)bkbi[0x4C] <= (s32)row[0x04]) break;    /* keyed on CURRENT MP */
        if ((float)i == 4.0f) break;
    }
    interval = (float)(s32)row[0x00];
    if (fieldSelector() == 2 || fieldSelector() == 3) interval /= 3.0f;
    if (delta > interval) { earnedPoint = 1; delta = 0.0f; }
}
carryHome[0x18] = delta;
AddPrimaryResourceRecoveryAccumulator(unit, delta);
return earnedPoint;
```

**So the recovery region is five rows, 20 to 24, of `{ s32 interval @ +0x00, s32 mpThreshold @ +0x04 }`.**
The row is picked by **current MP**, not maximum. The three float constants are literal in the image:
`01CEBC70 = 4.0`, `009146E4 = 5.0`, `008F311C = 3.0`.

> **Neither block reads the table's authored row count at `+0x04`.** The bounds are compiled in — 19
> ladder rows and 5 recovery rows. **Adding rows to slot 22 does nothing; the engine will never look
> at them.**

The loop's own escape (`002F9524`) is **dead code** with the shipped constants: the `i == 4.0` test
fires before the `i < 5.0` bound can fail, so a row is always selected.

And the payoff, at `003110C3`:

```asm
003110C3  call 0x2f9400                  ; returns 0 or 1
003110C8  mov  rcx, [rsi + 0x698]        ; the BKBI
003110CF  mov  edx, eax                  ; delta = that 0 or 1
003110D1  mov  r8d, 0x90                 ; flags: bits 4 AND 7 -> both publishers suppressed
003110D7  call 0x300ce0
```

> **A tick is worth exactly one MP**, and `0x90` is why **walking recovery is silent** while the
> damage paths pass `0x10` and still publish through `0028F1F0`.

### The zone multiplier — and an open question this answers

`thunk_FUN_00377ba0` (`00320160`) is the only route to `FieldRecord_GetBits12To13OrSaveOverride`
(`00377BA0`), documented in
[`../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`](../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md):

```c
twoBitField = SaveFlags_GetPayload1062Bit7() ? SaveFlags_GetPayload1063Bits4To5()
                                             : (fieldRecord.flags >> 12) & 3;
```

That document records the field's meaning as **open** (`PROPOSED-repos2d-2`) with the shipped
distribution `0`: 945, `1`: 36, `2`: 69, `3`: 104 over 1,154 fields.

> **The MP half of that question is now answered.** Values **2 and 3** — and only those — triple the
> gain in **both** damage functions and divide the walking interval by **3.0**. Values 0 and 1 do
> nothing to MP. For the MP economy the two-bit field is effectively the one-bit test **`>= 2`**, and
> it is true in **173 of 1,154 fields (15.0 %)**.
>
> The field's *other* consumer, `AiOrder_EvaluateTargetSelector`, is **not** examined here, so the
> question is answered for MP and remains open in general.

**A save flag overrides it for the whole game.** When `SaveFlags_GetPayload1062Bit7` is set, the value
comes from save payload 1063 bits 4–5 instead of the field record — so the MP economy can be switched
globally without touching a single field row.

### ~~Five~~ Nine new entries for the effect namespace *(count corrected 2026-10-02, OPUS: the table has nine rows)*

All proven by function, none named on the licence board here:

| effect id | byte tested | what it does |
|---:|---|---|
| **20** | `+0x6A` / `+0x7A` bit 4 | route B: MP for dealing damage, with action flag `0x10` |
| **21** | `+0x6A` / `+0x7A` bit 5 | MP for taking damage |
| **23** | `+0x6A` / `+0x7A` bit 7 | the kill bonus, `max(level / 4, 1)` |
| **39** | `+0x6C` / `+0x7C` bit 7 | **pins MP to zero** |
| **32** | `+0x6C` / `+0x7C` bit 0 | **the gil action-cost channel**: MP cost reported as 0, `trunc(cost × 64 / 50) × 10` computed as gil (the spend side) |
| **36** | `+0x6C` / `+0x7C` bit 4 | MP cost halved |
| **51** | `+0x6E` / `+0x7E` bit 3 | MP cost zero |
| **91 / 92 / 93** | `+0x73` / `+0x83` bits 3 / 4 / 5 | MP cost reduced by the percentage in slot-29 row `0x5B` / `0x5C` / `0x5D` word `+4` |
| **86** | `+0x72` / `+0x82` bit 6 | route A: MP for dealing damage, with action flag `0x08` |

Every one is tested in **both** layers with an `or`, so a temporary status and a derived augment are
interchangeable here — the alias property that document already establishes.

### The spend side — what an action costs (CS-5, read 2026-09-11)

`BattleAction_ComputePrimaryResourceCost` (`00309110`, 165 B; called by
`BattleAction_CheckExecutionResourceAvailability` `00303BD0` and
`BattleAction_ConsumeExecutionResources` `00305640`) takes `(unit, actionId)` — the **unit**, whose `+0x698` both helpers dereference for the stats (`002F9825`, `002F9634`; corrected 2026-09-11, ASTRA-CONTRA-FABLE-MP-COST-TRANSCRIPTION — the first version said `stats`):

```
if actionId > 0x21E                      -> 0                         (00309125-00309128)
row = actionTable[actionId]              (slot 02EBF138, stride word +8, relocated; 0030912A-00309163)
if row.b_1E in {5, 6}                    -> 0                         (00309169-00309171)
if unit == NULL                          -> row.b_0A                  (00309178: the authored MP cost)
if BattleUnit_UsesGilActionCostChannel(unit) -> 0 MP                  (0030918A-00309191; reads unit+0x698)
else -> BattleAction_ComputeModifiedResourceCostAmount(unit, actionId)   (003091A3, tail call)
```

`BattleUnit_UsesGilActionCostChannel` (`002F9820`, 51 B) is false for a unit whose stats' kind byte
`+5` is 1 and otherwise true when either effect layer's byte 4 has bit 0 — **effect id 32**
(`002F9831`–`002F984D`). `BattleAction_ComputeModifiedResourceCostAmount` (`002F95D0`, 589 B) starts
from the same `row.b_0A` (`002F962B`) and, for a unit that is not kind 1, **returns it unchanged for
ids `0xD0`–`0xE1` and `0x106`–`0x112`** — the Quickening and Esper ranges (named from [the battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) 2026-09-11: Red Spiral–Resplendence, Belias–Zodiark) (`002F9646`–`002F9667`,
`002F9806`). For everything else, in this order (`002F9674`–`002F9808`):

| effect (layer byte / bit → id) | cost becomes | site |
|---|---|---|
| byte 4 bit 0 → **32** (the gil channel) | `trunc(base × 64 / 50) × 10` — a gil amount, not MP | `002F97E4`–`002F9802`, constants `00916318` / `008F3130` |
| byte 11 bits 3 / 4 / 5 → **91 / 92 / 93** | `trunc(base − base / 100 × Σ)` — one truncation of the whole single-precision difference (`cvttss2si` after the `subss`, `002F97BD`–`002F97C1`; base 31 with Σ = 10 → 27, not the 28 that `base − trunc(base / 100 × Σ)` gives; corrected 2026-09-11) — where Σ sums word `+4` of rows `0x5B` / `0x5C` / `0x5D` of the slot-29 parameter table `02EBF040`, each effect once whichever layer sets it | `002F9688`–`002F97C1`, `100.0` at `008F3134` |
| byte 6 bit 3 → **51** | 0 | `002F97A3`, `002F97C7`, `002F97E0` |
| byte 4 bit 4 → **36** | halved (toward zero) | `002F97CD`–`002F97DC` |

Both layers (`+0x68` and `+0x78`) are tested for every bit, and the arithmetic is single-precision
with a truncation at each step — `10 × trunc(f32(base × 64.0) / 50.0)` (base 31 → 390, not
`trunc(31 × 12.8) = 396`) and `trunc(f32(base − f32(base / 100.0) × Σ))`, then the halving on the
truncated integer. So the authored MP cost is the action row's byte `+0x0A`; three augments in
the 88–95 byte subtract percentages the parameter table holds; one effect frees it, one halves
it; and one diverts it into gil. **The gil side has its own twin**: `BattleAction_ComputeGilCost`
(`00309060`, 168 B) returns 0 for a kind-1 unit, an id above `0x21E`, kinds 5 / 6, or a unit *not*
on the channel, and otherwise the same `002F95D0` — which with effect 32 set is the gil formula
(`00309070`–`003090F6`). `BattleAction_PrepareExecutionResources` (`0030EF20`, called from
`Battle_ProcessActionTarget` `00307300` and `00304850`) is the payer: it first derives the action id from the row pointer and the action table's stride (`0030EF2F`–`0030EF5E`, before any guard — a missing header or zero stride faults even for a null unit, EXP-064), then for a kind-0 unit it stores
the consumed item (row `+0x22` when `+0x1E == 3`, else `0xFFFF`) at unit `+0xDC8` and removes it,
then stores the gil cost at unit `+0xE58` and, when non-zero, `GameState_SetGil` (`00254EE0`) of
`max(GameState_GetGil` (`00253690`) `() − cost, 0)` (`0030EFB5`–`0030EFD8`). Both fields are **reservations**:
`BattleAction_RefundReservedExecutionResources` (`00300280`) gives the item back (`003002A5`–
`003002D0`) and adds `+0xE58` to the gil before zeroing it (`003002D7`–`003002F5`), the
availability check compares against `+0xE58` (`00303C8F`) and the consume path stores it again
(`003056B3`). A kind-1 unit with effect 32 gets no gil channel and pays
the gil-formula number **as MP** through the MP wrapper (`002F9820` false → `002F95D0` → the effect-32
branch). ASTRA's [EXP-063](../_experiments/EXP-063-mp-cost-controls.md) executed the four bodies
(the wrapper, both helpers and the pointer resolver, no stubs) over 31 fixtures: the id bound,
the kind gate, both exemption ranges' endpoints, each effect alone and stacked, the float order,
and a `ja → jae` mutant on the id bound rejected. **The percentages are 10, 10 and 10** (`FV-4`,
answered 2026-09-11): registry slot 29 is bound by `00236C30` from directory slot 59 of the
"STATIC" blob — `battle_pack.bin`, resource-pool entry 19, loaded by
`BattleStorage_InitializeWorkArrays` through `003843F0(0x13, …, "STATIC")` — via
`AreaData_BindAndRebaseSectionDescriptor` (`00236F88`–`00236F96`, the dword at `+0xEC` of the
blob); that section (file offset `0x267B0` in the `us` file) is an `st2e` table of 129 rows × 8
bytes `{u16 nameId, u16 0x5000 + row, u16 parameter,` ~~`u16 0xFF}`~~ `u16}` whose low byte `+6` is the stage-3 timer-slot index: `0xFF` in 126 rows, `03` / `04` / `05` in rows 55 / 56 / 57 *(corrected 2026-10-02, OPUS: checked against `battle_pack.bin` slot 29; the periodic tick reads it at `00385619`)*, and rows `0x5B`, `0x5C`, `0x5D`
carry `parameter = 10` each — so Channeling 1 / 2 / 3 cut the MP cost by 10 % apiece, 30 % with
all three, and a 31-MP spell costs 27 / 24 / 21.

## 3. Key addresses

| address | name | size |
|---|---|---:|
| `00307300` | `Battle_ProcessActionTarget` — the only caller of both gain paths | — |
| `002F91A0` | `BattleAction_ComputeTargetPrimaryResourceGainFromHpDamage` | 159 B |
| `002F9240` | `BattleAction_ComputeCasterPrimaryResourceGainFromHpDamage` | 438 B |
| `002FB6C0` | `BattleAction_LookupPrimaryResourceGainFactorByHpDamage` | 500 B |
| `002F9400` | `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` | 458 B |
| `00329A20` | `BattleUnit_AddPrimaryResourceRecoveryAccumulator` | 84 B |
| `00320450` | `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` | 87 B |
| `002FA540` | `BattleUnit_ClearPrimaryResourceRecoveryAccumulator` | 30 B |
| `00300CE0` | `BattleStats_ModifyPrimaryResource` | 351 B |
| `00300BC0` | `BattleStats_ModifySecondaryResource` | 207 B |
| `00309110` | `BattleAction_ComputePrimaryResourceCost` | 165 B — the spend side (§2, "the spend side") |
| `002F95D0` | `BattleAction_ComputeModifiedResourceCostAmount` | 589 B — the exemptions, the gil channel, Channeling, effects 51 and 36 |
| `002F9820` | `BattleUnit_UsesGilActionCostChannel` | 51 B — effect 32 on a non-kind-1 unit |
| `00309060` | `BattleAction_ComputeGilCost` | 168 B — the gil twin of the MP wrapper |
| `0030EF20` | `BattleAction_PrepareExecutionResources` | 205 B — stores the gil cost at unit `+0xE58` and deducts it; the item consume beside it |
| `00309110` | `BattleAction_ComputePrimaryResourceCost` | 165 B |
| `00320160` | `thunk_FUN_00377ba0` — the zone multiplier selector | 5 B |
| `003283D0` | publisher suppressed by flags bit 4 | — |
| `0028F1F0` | publisher suppressed by flags bit 7 | — |
| `0x02EBF0B8` | registry slot 22 — both ladders | — |
| `0x01CEBC70` | `4.0` — recovery loop index limit | — |
| `0x009146E4` | `5.0` — recovery row count | — |
| `0x008F311C` | `3.0` — the zone divisor | — |

## 4. Modding notes

- **Slot `0x02EBF0B8` is two tables in one.** Rows **1–19** are the damage ladder,
  `{u16 threshold, u8 otherFactor, u8 bandFactor}`; rows **20–24** are the walk-recovery ladder,
  `{s32 interval, s32 mpThreshold}`. Row 0 exists only as the "row below" for the first ladder hit.
- **Both bounds are compiled in.** Nineteen and five. **Extra rows are unreachable**, and the header's
  count field is never read by either consumer.
- **The lookup takes the row *below* the first threshold the damage fails to reach**, and saturates on
  row 19. An off-by-one when authoring shifts every band.
- **Column `+0x03` is the `0x1B..0x27` band, not the party.** Main-roster characters (`0x00..0x06`)
  read column `+0x02` along with foes.
- **No opposite sides, no MP** — the table is never consulted, so a friendly-fire mod grants nothing
  however the ladder is authored.
- **An HP-absolute action grants no MP to anyone.** If a custom action sets HP instead of adding to
  it, `dwResultFlags` bit 3 kills both gain paths.
- **The dealing-damage routes need the action's own permission**, action-definition row `+0x2C` bits
  3 and 4. Granting a character effect 20 or 86 does nothing until an action opts in.
- **Field flags bits 12–13 are the cheapest global MP lever there is** — set a field's value to 2 or
  3 and every MP gain in that zone triples while walk-recovery runs three times faster. Save payload
  1062 bit 7 plus 1063 bits 4–5 does it for the whole game at once.
- **Effect 39 is a hard MP lock**, not a penalty: capacity becomes zero and no path can raise the
  value.
- **If you null the slot-22 pointer, the ladder dereferences a small constant address** (`002FB7B3`
  reads `[rbx+3]` with `rbx = 0`). Leave the table present.

## 5. What is not known

- [x] ~~**The licence-board names of effects 20, 21, 23, 39 and 86.**~~ **CS-1 ANSWERED 2026-09-12
  (FABLE), from the shipped tables.** The augment table (registry `02EBF040`, the blob's `+0xEC`,
  129 × 8) carries a bank-10 text word at `+2` ([the battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)): row 20 *"Gain MP after dealing
  magick damage."*, 21 *"Gain MP after taking damage."*, 23 *"Gain MP after defeating a foe."*, 86
  *"Gain MP after dealing damage."*, and **39 *"NOT USED"***. The licence-board nodes (`02EBF038`, the
  blob's `+0x34`, 361 × 24; category byte `+5`, up to eight ids at `+8`, [the licence-check page](../12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md)) that
  carry those ids in category 15 are, by their bank-3 names: **219 Warmage** (id 20), **220
  Martyr** (21), **221 Inquisitor** (86), **222 Headsman** (23) — 30 LP each. Id 39 sits on no
  category-15 node (its only occurrences are action ids on magick nodes), so the zero-capacity
  effect has no licence and no text: it reaches a unit from a definition row, not the board.
- [x] ~~**The shipped contents of slot 22.**~~ **CS-2 ANSWERED 2026-09-12 (FABLE) — read from the
  `us` `battle_pack.bin`.** The binder stores the blob's directory entry `+0x10` into slot 22
  (`00236C92`–`00236C9D`, `003845F0`); in the shipped file that is an `st2e` table at `0x1B58`
  ([the string-table page](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) §2) with **25 rows of 8 bytes** (header count 25, record size 8, header 32) —
  exactly the compiled-in 20 + 5, so the "adding rows does nothing" note above is also the file's
  own shape. ~~Bytes `+4`–`+7` of every row are zero.~~ Bytes `+4`–`+7` are zero in rows 0–19 only; rows 20–24 hold 25, 50, 100, 200 and 1,000 there, the `mpThreshold` column *(corrected 2026-10-02, OPUS: checked against `battle_pack.bin` at `0x1B58`; §2, walking recovery)*.

  **The damage ladder (rows 0–19):**

  | row | threshold | factor `+2` (everyone) | factor `+3` (the Esper band) |
  |---:|---:|---:|---:|
  | 0 | 1 | 1 | 6 |
  | 1 | 50 | 1 | 6 |
  | 2 | 100 | 1 | 6 |
  | 3 | 300 | 1 | 6 |
  | 4 | 500 | 2 | 12 |
  | 5 | 750 | 2 | 12 |
  | 6 | 1,000 | 2 | 12 |
  | 7 | 1,250 | 2 | 12 |
  | 8 | 1,500 | 3 | 18 |
  | 9 | 2,000 | 3 | 18 |
  | 10 | 2,500 | 3 | 18 |
  | 11 | 3,000 | 4 | 24 |
  | 12 | 3,500 | 4 | 24 |
  | 13 | 4,000 | 4 | 24 |
  | 14 | 5,000 | 5 | 30 |
  | 15 | 6,000 | 6 | 36 |
  | 16 | 7,000 | 8 | 48 |
  | 17 | 8,000 | 10 | 60 |
  | 18 | 9,000 | 15 | 90 |
  | 19 | 9,999 | 30 | 180 |

  With the ladder rule above (first row the damage does not reach, take the row below; 19 if it
  clears all), damage below 50 yields factor 1, 500–749 factor 2, 1,500–1,999 factor 3, 3,000–
  4,999 factor 4, then 5, 6, 8, 10, 15 per thousand, and 9,999 or more factor 30. **The Esper
  band's column is six times the other on every row.**

  **Walking recovery (rows 20–24):**

  | row | interval | current MP up to |
  |---:|---:|---:|
  | 20 | 9 | 25 |
  | 21 | 13 | 50 |
  | 22 | 18 | 100 |
  | 23 | 22 | 200 |
  | 24 | 27 | 1,000 (and the `i == 4` fallback) |

  The row is the first whose `mpThreshold` is not below the current MP, so **low MP recovers
  faster**: a unit at 25 MP or less earns its point every 9 accumulator units of walking, one at
  more than 200 MP every 27 — thirds of those under field selector 2 / 3. `CS-2`.
- [x] **CS-3.** ~~**`BattleStats_ModifySecondaryResource` (`00300BC0`).** Called on every positive MP change. It
  reads `+0x37`, `+0x28`, `+0x6C`, `+0x7C` and `+0x4C` and re-enters `00300CE0` — so it is not a
  separate pool but something that feeds back into MP. Not read.~~ Read 2026-09-11 (§2, "the
  secondary resource"): it moves `+0x06`, never touches `+0x4C` and re-enters nothing. Narrowed
  again 2026-09-11: the pool is **spent by kind-5 / 6 actions at `max MP × row +0x0A`** (Consume,
  `0030570D`) and **gated by `+0x4E` against that count** (availability reason `0x14`) — so the tier
  is "how many whole max-MP charges the pool holds". Left: the authored source of the multiplier
  `+0x37` and the pool's name in the text banks. `CS-3`, narrowed.
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): the pool is the Mist Charges, and `+0x37` is derived from the licence
  board, not authored.** Control: `_index/candidates/cs3-mist-charges/cs3_mist_charges.py` (5 checks, FAILS 0).
  - **`+0x37` is `min(stats +0x20, 3)` for a party record and 0 for any other.** The stats rebuild clamps and
    stores it, and only kind 0 reaches the load.
  - **`+0x20` is the larger of `chr_data +0x46` and a licence-derived rank,** set by the level grower. That rank is
    the larger of two values: the count of owned Quickening licences 0–17, and the highest Mist Charge cost
    (action `+0x0A`) among the owned Esper licences `0x12`–`0x1E`. The instruction addresses are in the control.
  - **The shipped data.** In all nine packs, `chr_data +0x46` is 0 in every row, and the Esper summons
    `0x106`–`0x112` cost 1,1,1,2,2,3,1,2,3,2,2,3,3.
  - **The name.** The us `help_menu.bin` says "Perform an action expending Mist Charges" at `+0xDB4`.
  - *This reading was first made by a delegated read-only pass and was re-checked on the bytes and the data here.*
- [x] ~~**`003283D0` and `0028F1F0`**, the two publishers the flag bits switch.~~ **CS-4 ANSWERED
  2026-09-12 (FABLE).** [the HP write page](../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) names them — `003283D0` the **reaction publisher** (→ `003BBD00`)
  and `0028F1F0` the **number publisher** (→ `003F8980`), the same pair the HP writer switches with
  the same bits. A census of every caller of `BattleStats_ModifyPrimaryResource` shows **bit 4 set
  on every MP path in the image**: `Battle_ProcessActionTarget` `0x10` (`00307B34`, `00307B86`),
  `BattleAction_ConsumeExecutionResources` `r15 | 0x10` (`003056F0`), the periodic maintenance
  `0x90` (`003110D1`), `BattleStats_ReconcileResourcesToEffectiveCapacity` `0x217` (`0030F5F7`).
  The one path that can clear it is the script's: `setmp` / `setmpmode` / `setmpratio` /
  `setmpratiomode` (`00473A00`, `00473A90` → `00329B70` → `00329BD0`, mode 1) build the flags from
  the verb's option word — bit 0 → suppress flag bit 1, **bit 1 → let the reaction publisher run**
  (flag bit 4 clear, `00329C0B`–`00329C15`), bit 2 → suppress flag bit 2 — and hand them to
  `BattleStats_SetPrimaryResourceAbsolute` (`00329C68`). So an MP reaction is script-optional and
  never a combat event.
- [x] ~~**`BattleAction_ComputePrimaryResourceCost` (`00309110`)** — the spend side — is not read.~~
  `CS-5` — ANSWERED 2026-09-11 (§2, "the spend side"): action row `+0x0A`, kinds 5 / 6 free, Quickening
  and Esper ids exempt from modification, effect 32 diverts the cost into gil, 91–93 subtract
  authored percentages, 51 frees, 36 halves.
- [x] ~~**The Channeling percentages** in slot-29 rows `0x5B`–`0x5D` word `+4` — authored data
  neither this page nor EXP-063 has decoded.~~ `FV-4` — ANSWERED 2026-09-11: 10 % each, from
  `battle_pack.bin` directory slot 59 (§2, "the spend side").
- [x] ~~The `0x40`-stride per-combatant state arrays the carry lives in, and why the party path indexes
  by `bkbi[0x04]` (an actor **type id**, not a roster index) rather than a slot.~~ **CS-6 ANSWERED
  2026-09-12 (FABLE): because for a party-table record the type id *is* a table row index.** The
  two arrays are `0208D480` (party path, `002F9439`) and `0208DE80` (slot path, `002F9461`) — the
  same pair [the handler-table page](../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md) reads as the per-combatant persistent-state records that
  `BattleRuntime_ResetPersistentStatePrefix` clears (first 32 bytes) and [the spawn keep entry map](../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) names the
  unit's 64-byte record. Their distance is `0x208DE80 − 0x208D480 = 0xA00 = 40 × 0x40`: the party
  array has exactly one entry per row of the **40-row party definition table** (`02EBF130`,
  [the kind-byte page](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)), and a kind-0 record's byte `+4` is that row — Vaan … Penelo, the guests, the
  Espers. So the party carry is keyed by *who* the unit is and survives its battle slot; the
  non-party array (32 × `0x40`) is keyed by the unit's slot `+0xEA9` and is reused. `CS-6`.
- [x] ~~Whether the `AiOrder_EvaluateTargetSelector` use of field bits 12–13 is consistent with the
  `>= 2` reading proven here for MP.~~ **Consistent (read 2026-09-12, FABLE).** The accessor's thunk
  `00320160` has exactly four callers: the two gain functions and the recovery step (each `== 2 ||
  == 3`, `002F9225`–`002F9232`, `002F93C7`–`002F93D4`, `002F956F`–`002F957C`) and the selector,
  which compares the value against the gambit's own operand — sub-mode 1 `== operand`
  (`00303052`–`00303063`), sub-mode 2 `>= operand` (`00303043`–`0030304D`) — and matches the
  result against the expected truth (`00303066`). The selector therefore treats the two bits as an
  ordered level 0–3, exactly as the MP code does, and is the one reader that can tell 1 from 0.

## 6. Evidence

| claim | evidence | tier |
|---|---|---|
| Live MP `+0x4C`, capacity `+0x28`, both `s16` | `00300CE0` disassembled: `movsx …[rsi+0x4c]`, `movsx …[rsi+0x28]`, `mov word [rsi+0x4c], di` | 1 |
| `+0x28` is MP | the stat rebuild's output block at `record+0x24` and its `.ard` column map (`+0x24` MP `s16`/999), offset four, cross-checked by `+0x26`→`+0x2A` Strength which the Bow formula reads | 1 |
| Effect 39 pins MP to zero | the two sign-bit tests on `+0x6C`/`+0x7C` and the `cap = 0` path, complete body | 1 |
| Decrease clears the accumulator | `if (unit && iVar8 < iVar5) ClearPrimaryResourceRecoveryAccumulator(unit)` | 1 |
| Eligibility re-checked after the publishers on a decrease | the second `0x30B770`/`0x30B7F0` pair at `00300DDD`/`00300DEB`, after `003283D0`/`0028F1F0` | 1 |
| Result-flag gate: bit 8 set, bit 3 clear | `00307B0D bt eax,8 / jae` and `00307B13 test al,8 / jne` | 1 |
| Caster/target labelling | the call site credits the target function's result to `target->pBkbi` and the caster function's to `caster->pBkbi` — **independent of the ledger names** | 1 |
| `killed` is a kill flag | `iVar5 = 1` defaulted, zeroed unless the target is out of play with bit 15 not overriding | 1 |
| Opposite-sides rule, damage-only | complete bodies of `002F91A0` and `002F9240` | 1 |
| Effects 21 / 20+`0x10` / 86+`0x08` / 23 | the byte-and-mask tests, mapped through `byteIndex = n>>3` from the two-layer document, whose convention the weather document independently confirms at `+0x6A` bit 0 = id 16 | 1 |
| Kill bonus `max(level/4, 1)` | `bVar1 = target->bkbi->bLevel >> 2; if (bVar1 == 0) uVar4 = 1;` | 1 |
| Ladder shape, columns, 19-row bound, row-19 saturation | complete disassembly of `002FB6C0`, `cmp edi,0x14`, `lea ecx,[rdi-1]`, `imul ebx,edx,0x13`, reads at `+2`/`+3` | 1 |
| Band selector is the `0x1B..0x27` partition | `002FB766`–`002FB76E`: `movzx eax,[rcx+4]; sub al,0x1b; cmp al,0xc; ja` | 1 |
| Recovery uses the **same slot**, rows 20–24 | `002F94DC lea eax,[rbx+0x14]` and `002F9556`, both on `DAT_02EBF0B8` | 1 |
| Recovery keyed on **current** MP | `002F94FD movsx ecx, word ptr [rax+0x4c]; cmp ecx,[r9+4]` | 1 |
| The three float constants | read from the image at the rip-relative targets: `4.0`, `5.0`, `3.0` | 1 |
| A tick is worth exactly 1 MP, silently | `003110C3`: return value passed as `delta` with `r8d = 0x90`, and the two `flags` tests in `00300CE0` | 1 |
| The late gates run regardless of bit 0; the secondary word's cap and tier; no recursion | `00300CE0`, `00300BC0`, `00300C90`, `0030E060` read whole; EXP-061 (27 isolated cases, late-gate mutant rejected) | 1 + isolated original code |
| The spend side: base, exemptions, gil channel, Channeling, effects 51 / 36; the gil twin and the payer | `00309110`, `002F9820`, `002F95D0`, `00309060`, `0030EF20` read whole; the three float constants read from `.rdata` (64.0, 50.0, 100.0); EXP-063 (31 isolated cases over the four bodies without stubs, id-bound mutant rejected) | 1 + isolated original code |
| Field bits 12–13 values 2/3 triple gain and third the interval | `lea ebx,[rbx+rbx*2]` in both gain functions and `divss xmm6,[008F311C]` in the recovery step, all behind `thunk_FUN_00377ba0` | 1 |
| 173 of 1,154 fields | the shipped distribution recorded in the navimapdata document, **not re-censused here** | 2 |
| Neither block reads the authored row count | absence of any read of table `+0x04` in either complete body | 1 |

## 7. Related

- [`Status-And-Augment-Layers/two-layer-effect-model.md`](Status-And-Augment-Layers/two-layer-effect-model.md)
  — the `+0x68`/`+0x78` layers and the bit-numbering convention; **five new entries for its namespace map.**
- [`../08-Combat-Formula/where-a-stat-number-comes-from.md`](../08-Combat-Formula/where-a-stat-number-comes-from.md)
  — where max MP is computed, and the record/`.ard` offset-by-four this document relies on.
- [`../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`](../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
  — the two-bit field, **whose MP meaning this document establishes.**
- [`../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`](../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md)
  — the out-of-play predicate reused here as a kill test.
- [`../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md`](../04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md)
  — the band that picks the factor column.
- [`../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
  — the registry convention, and where slot 22 was first identified.

## 8. Provenance — how the GN160 stamp above was earned

**This document was drafted against the wrong parent and then re-derived against the right one.** The
headless project it was written in (`work/headless/GFZ_HEADLESS`) turned out to hold **GN158**, two
certified checkpoints behind — its snapshot `46f02e26…`, residual `c5d4b7f7…` and ledger
`explicit=38003 unresolved=158` match the `GN158` lineage entry in `GfzEnv.ps1` byte for byte.

The mechanism above never depended on that project: **every instruction, constant and offset in this
document was disassembled from `work/exe/FFXII_TZA.exe`, independently SHA-verified against the
authorized `73461d08…`.** What the project supplied was *names and sizes*.

So those were re-derived. The certified GN160 parent
(`fa0db293…`, 82,130,611 B) was fresh-imported and **`Verify-GfzCheckpoint` passed on all four
axes** — ledger `explicit=38022 unresolved=139 pct=99.63575`, snapshot `b57264ba…`, embedded EXE
`73461d08…`, residual `b5008f9d…`. All twenty functions this document names were then re-decompiled
against it:

**Every name reproduces. Every size reproduces but one** —
`BattleStats_ModifySecondaryResource` is **`0xCF` = 207 bytes**, and the draft said 288.
**288 was the byte count of the disassembly window chosen to look at it**, carried into the table as
though it were a measurement. *A number that entered as a tool argument and left as a fact.* Corrected
here and in `CS-3`.

The thunk size was checked independently rather than inherited: `00320160` is
`e9 3b 7a 05 00` — **five bytes, `jmp 0x377ba0`** — which also confirms structurally the
navimapdata document's claim that it is the only route to `00377BA0`.

**The 19 functions that GN158 and GN160 disagree about were enumerated and none of them appears in
this document** — they are the Presentation glyph/widget/nine-patch cluster, cited only under
`99-Unresolved-Residual/`.

## Falsification pass — 2026-09-07, `xiionline-61`

**Self-attack, same day as authorship.** The session that wrote this document had a demonstrated
error rate, so its own claims were re-derived rather than re-read.

**The systematic attack:** every "only caller" / "N callers" statement in the day's four documents was
made with a scan that matched `E8 call rel32` only. **The CRT block later established that this
binary reaches things through `E9 jmp rel32` tail calls and import thunks**, so every one of those
claims was re-run against **both** instruction forms, and against `data_xref_scan.py` for
address-taken references (vtables, pointer tables) with a passing control.

### Result for this document — **no claim overturned**

| claim re-tested | both call forms | data refs | verdict |
|---|---|---|---|
| `Battle_ProcessActionTarget` is the **only** caller of both gain functions | 1 call, 0 jmp | — | **stands** |
| `002F91A0` target gain — one caller | 1 call, 0 jmp | — | **stands** |
| `002F9240` caster gain — one caller | 1 call, 0 jmp | — | **stands** |
| `002FB6C0` ladder — reached from both gain paths | 2 calls, 0 jmp | — | **stands** |
| `002F9400` periodic step — one caller | 1 call, 0 jmp | — | **stands** |

**The dead-code claim was re-derived, not re-read.** §2 says the recovery loop's `i < 5.0` escape at
`002F9524` is unreachable. Re-tracing: at `i = 4` the `(float)i == 4.0` test at `002F950E` breaks to
the row block *before* the `inc`/bound check can run, and the escape is reached only when
`5.0 > (i+1)` is false, i.e. `i >= 4`. **Unreachable. Confirmed.**

**Not attacked, and still resting where the document says it rests:** the identification of record
`+0x28` as maximum MP, which depends on the `.ard`-column-plus-four join in
[`../08-Combat-Formula/where-a-stat-number-comes-from.md`](../08-Combat-Formula/where-a-stat-number-comes-from.md);
the "173 of 1,154 fields" figure, borrowed at tier 2 and not re-censused; ~~and the four functions
listed as unread in §5, which remain unread.~~ *(answered: see §5 — every item there is ticked, CS-1 to CS-6 and FV-4 among them; 2026-10-02, OPUS)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

- **CoreRuntimeScheduling — mechanical.** Ten of the functions cited here reach their authored rows through
  `ImageAddress_ResolveRuntimePointer`: `002F9240`, `002F9400`, `002F95D0`, `002FB6C0`, `00304850`, `00305640`,
  `00307300`, `00309060`, `00309110` and `0030EF20`. `AreaData_BindAndRebaseSectionDescriptor` also uses its inverse,
  `RuntimePointer_EncodeImageAddress`. That is the image's ordinary table-access path, not an MP dependency.
- **Gameplay.**
  - `BattleUnit_AdvanceStandardActionState` (`00304850`) asks `BattleAction_FindApproachGeometryAroundTarget`.
  - Both it and `Battle_ProcessActionTarget` (`00307300`) raise presentation events through
    `BattleUnit_DispatchActorPresentationEvent`.
  - `00307300` submits a reaction mode through `BattleUnit_SubmitResultReactionMode`, which is the caller of the
    **Presentation** queue `BattlePresentation_EnqueueReactionWithRandomizedVariant` (`003BBD00`) this page cites.
- **Movement.** The two action-state functions steer the unit.
  - `00304850` calls `BattleLocomotion_ResetPathAndSetTargets`, `BattleLocomotion_SetApproachAndReferenceTargets`,
    `BattleUnit_UpdateCombatNavigationStep` and one small unnamed helper.
  - `00307300` calls `Actor_SetDesiredMovementHeading`, `Actor_SetFacingHeading_Variant1` and four unnamed movement
    helpers.
  - None of those touches the MP fields this page follows.
- **PlatformOnlineAchievements.**
  - `GameState_SetGil` fires achievement counters 6 and 7 ([the achievement catalogue](../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md) AB-7).
  - `BattleAction_ConsumeExecutionResources` (`00305640`), on its `+0x1E == 10` arm (the Esper-attack rows), calls a
    55-byte helper at `0030575C`. That helper tests bit 5 of save byte `+0x3845`, which is awarded bit 13 of the
    bitset at `+0x3844`. When the bit is set, it calls `00863280(0x13)`, and if that returns 0, `008632B0(0x13)`.
    Those two are not read, so what the Steam side does with index `0x13` is open.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**UI — SERVICE.** `0028F1F0` on this page calls `FUN_00296280`, owned by that layer. What it reaches is a 51-byte linear search over **`0xC0`-byte records** from `0209BF66` to `0209C2BE`, matching `dword[+0x32]` and skipping any record whose own or previous `byte` lacks bit 1 - and it returns the record base, `0x7E` behind the member it matched; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatAI — SERVICE and CLIENT (3 edges).** The registry binder `00236C30` (which binds slot 29, the Channeling table, from the `"STATIC"` blob) also calls `GambitTargetDefinition_BindAndBuildMenuLookup` `00238880`, and `00238880` calls `AreaData_BindAndRebaseSectionDescriptor` `003845F0`; `Battle_ProcessActionTarget` `00307300` calls `BattleEnmity_ApplyActionParameters` `003216E0`. The binder installs the gambit-target table in the same pass as the MP-cost table, and the per-target action step that grants MP on a hit is also the step that applies threat; neither is an MP relationship.

**CombatFormula — SERVICE and CLIENT (35 edges).** The MP writers `BattleStats_ModifyPrimaryResource` `00300CE0`, `BattleStats_SetPrimaryResourceAbsolute` `00300C90` and `BattleStats_ModifySecondaryResource` `00300BC0` are called by `BattleStats_ReconcileResourcesToEffectiveCapacity` `0030F5A0`, `BattleFormula_ApplyTargetResult` `003112F0`, `BattleAction_ConsumeExecutionResources` `00305640` and `00329BD0`, and call `BattleStats_FindOwningBattleUnit` `0031B860`, the modifier `0030E060` and `BattleUnit_ClearPrimaryResourceRecoveryAccumulator` `002FA540`; the two publishers `003283D0` and `0028F1F0` are called by `BattleStats_ModifyHPAndProcessLethalState` `00300530` and `00300CE0`; `00307300` calls `BattleFormula_MapTargetEntryCodeToOutcome` `002FEE20`, `BattleFormula_MapOutcomeToTargetEntryCode` `0030DAE0`, `BattleStats_GetByBattleSlotIndex` `00320A40`, `BattleFormula_ResolveTargetResult` `00385F60`, `003112F0` and `00300CE0`; `BattleUnit_AdvanceStandardActionState` `00304850` calls `BattleRuntime_GetEffectiveActionId` `00387090` and `BattleRuntime_ResolveAndCacheEffectiveActionId` `00387A50`; `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400` calls `0031B860`; `003112F0` calls `GameState_GetGil` `00253690` and `GameState_SetGil` `00254EE0`, which this page cites for the gil channel of an action's cost. MP is a field of the stats record that layer owns: every gain and spend on this page ends in its resource writers, and the per-target step resolves the result through its resolver.

**Items and Items_Equipment_Shops_License — SERVICE and CLIENT (11 edges).** `BattleAction_PrepareExecutionResources` `0030EF20` and `BattleAction_RefundReservedExecutionResources` `00300280` call `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` `003008A0`; the gil accessors `00253690` and `00254EE0` are called by `InventoryBundleClass09_ApplyGilAndNestedItems` `002FD530`, `InventoryEncodedGilClass0E_ApplyGilDelta` `002FD880`, `Shop_CommitPurchaseItemAndGil` `002FEEB0` and `Shop_CommitSaleItemAndGil` `00310870`; the binder `00236C30` calls `00238660`, the setter of one registry global. An action's cost can be an item as well as MP or gil (the spend side, CS-5), and shops move the same gil balance an action spends.

**Party — CLIENT and SERVICE (7 edges).** `00304850` calls `BattleUnit_ResolveByFocusHandle` `0031B7E0` and `PartyFocus_IsCurrentPackedActorHandle` `003273B0`; `ActorHandle_EncodeRegistryEntry` `003589B0` is called by the roster and focus bodies `PartyRoster_AssignActorToSlot` `00269C70`, `PartyFocus_SelectAndRequestDefaultActor` `00326500`, `VMPartyCommand_SetSecondaryFocusActorFromActorIndex` `00353530`, `PartyRoster_AssignActorAndCommitFocusWhenEligible` `0050C610` and `PartyFocus_EncodeActorAndSetTemporaryControlledActorOverride` `0050D2F0`. The action-state step resolves the unit's focus and asks whether it is the player's; the handle encoder, which the `setmpratiomode` body `00473A00` also calls, is shared with roster code.

**Resource — SERVICE (2 edges).** `00236C30` calls `003843F0`, which calls `00384420`. The binder reaches the resource-pool loader that brings in `battle_pack.bin` (`"STATIC"`), the file whose slot 29 holds the Channeling percentages.

**Rewards_Progression_Economy — SERVICE and CLIENT (14 edges).** The spend-side bodies `BattleAction_CheckExecutionResourceAvailability` `00303BD0`, `00305640`, `0030EF20` and `00300280` call `GameState_GetGil` `00253690` and (all but the check) `GameState_SetGil` `00254EE0`; those two are also called by `GameState_AddGilClampedAndNotify` `003004B0`, `GameState_SetGilClampedNonnegative` `00300500`, `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` and `003F4AA0`. A gil-costed action checks, reserves, spends and refunds through the economy layer's gil balance, the same balance defeat rewards credit.

**Script_VM_Native_Bridge — CLIENT (20 edges).** The `setmpratiomode` bodies `00473A00` and `00473A90` are called by the verb handlers `00341140`, `00341EE0`, `00349620`, `0034A4C0`, `00341690`, `00342500` and `00349AD0`; `003589B0` is called by twelve verb bodies (`00342150`, `00342D40`, `003438F0` and nine more); `008632B0` is called by one more verb body. Script verbs set the MP-ratio mode this page reads in section 5, and share the handle encoder and the achievement notify gate; only the first is an MP relationship.

**WorldAreaField and World — SERVICE, DEPENDENCY (16 edges).** `00236C30` calls `003845F0` and `003846F0`, is called by `00238850`, and calls `003847B0`; `003845F0` is called by `00236C30`, `BattleData_SetAreaArdSectionCategory` `0023A160`, `00238640` and `003847B0`, and calls `003846F0`; the zone-multiplier getter `00377BA0` calls `WorldTransition_GetActiveOrPendingFieldId` `003148F0`, `00314AA0` and `00314AC0`; `00307300` calls `FieldData_GetActiveFieldRecordBit15` `00377C20`, and `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450` and `BattleUnit_AddPrimaryResourceRecoveryAccumulator` `00329A20` call its jump `00313F60`. The Channeling table is bound through that layer's section descriptor, the walking-recovery zone multiplier is a field byte a save flag can override, and the recovery accumulator consults the field record's bit 15.

## SWE2-EC7-58 update (2026-09-19) - `00309110`

`00309110` (165 B) is the `BattleAction_ComputePrimaryResourceCost` body the MP page names - `0020E600`/`002F9820` plus `02EBF138`. Interior anchor `00309139` (a `0020E600` call).


## SWE2-EC7-67 update - `00473A00`

`00473A00` (130 B) is a where-mp-comes-from body - `003589B0` single call, tail `00329B70`. Interior anchor `00473A37` (a `003589B0` call).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-where-mp-comes-from-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00238640` | 19 B | sign-extends `ecx`, forms the pointer `02F973C0 + ecx*8` in `rcx` and tail-jumps `003845F0` with it, leaving the other argument registers unchanged | `00238643`, `0023864A`, `0023864E` |
| `00300500` | 28 B | clamps `ecx` to zero when it is negative (`cmovns` keeps a non-negative `ecx`), calls `00254EE0(clamped value)` and returns the clamped value | `0030050A`, `0030050F`, `00300514` |
| `00341140` | 75 B | resolves `00263F10(rdx)`, reads two values by calling `00267E10(r9)` twice, and tail-jumps `00473A00(resolved pointer, second value, first value)` | `00341155`, `00341160`, `0034116A`, `00341186` |
| `00341690` | 75 B | resolves `00263F10(rdx)`, reads two values by calling `00267E10(r9)` twice, and tail-jumps `00473A90(resolved pointer, second value, first value)` | `003416A5`, `003416B0`, `003416BA`, `003416D6` |
| `00341EE0` | 91 B | calls `00267F90(r9, 2)`, resolves `00263F10(rdx)`, reads two values by calling `00267E10(r9)` twice, and tail-jumps `00473A00(resolved pointer, second value, first value)` | `00341EFD`, `00341F05`, `00341F10`, `00341F1A`, `00341F36` |
| `00342150` | 90 B | resolves `00263F10(rdx)`; when `003D9FE0()` returns non-zero, compares `003589B0(resolved pointer)` with `003D9FA0()` and takes 1 when they are equal, else 0; when `003D9FE0()` returns zero takes 0; then tail-jumps `0026B4E0(rcx, that 0 or 1)` | `00342174`, `0034217B`, `00342187`, `0034218E`, `003421A5` |
| `00342D40` | 49 B | tail-jumps `0026B4E0(rcx, 00320790(003589B0(00263F10(rdx)), 0))` | `00342D4C`, `00342D54`, `00342D5D`, `00342D6C` |
| `00342500` | 91 B | calls `00267F90(r9, 2)`, resolves `00263F10(rdx)`, reads two values by calling `00267E10(r9)` twice, and tail-jumps `00473A90(resolved pointer, second value, first value)` | `0034251D`, `00342525`, `00342530`, `0034253A`, `00342556` |
| `003438F0` | 52 B | tail-jumps `0026B4E0(rcx, 00320790(003589B0(00263F10(rdx)), 1))` | `003438FC`, `00343904`, `00343910`, `0034391F` |
| `0034A4C0` | 102 B | calls `00267F90(r9, 2)`, reads three values by calling `00267E10(r9)` three times, resolves `00263F10(00264010(third value))` and tail-jumps `00473A00(that pointer, second value, first value)` | `0034A4DA`, `0034A4F6`, `0034A4FD`, `0034A505`, `0034A521` |
| `00353530` | 86 B | reads two values by calling `00267E10(r9)` twice; when the second is non-zero tail-jumps `00359410(003589B0(00264010(first value)))`, otherwise tail-jumps `00359410(0)` | `00353540`, `00353551`, `00353555`, `0035356E`, `00353581` |
| `00473A90` | 123 B | builds a flag word from `r8d`: bit 0 shifted to bit 28, bit 29 set when `r8d` bit 1 is set and bit 30 set when `r8d` bit 2 is set; when `rcx` is null returns -1, otherwise tail-jumps `00329B70(003589B0(rcx), 1, edx, flag word)` | `00473AAC`, `00473ABB`, `00473AE0`, `00473AF3`, `00473AFD` |
| `0050D2F0` | 23 B | tail-jumps `003593A0(003589B0(rdx))` | `0050D2F7`, `0050D302` |

## The two eligibility masks (OPUS, 2026-10-02)

From FABLE's review of ASTRA's [`ov42-mode17-query-boundaries`](../_index/candidates/fable-review-astra-ov42-mode17-query-boundaries-1002/REVIEW.md)
(ACCEPT-WITH-NARROWING). OPUS re-read the global mask's zeroing, the setting getter and the settings root at the bytes
([`batch6_check.py`](../_index/candidates/opus-ov42-batch6-routes-1002/batch6_check.py)). The unit mask's arms rest on FABLE's `rv_mode17q.py`.
- **Global** (`BattleTarget_ComputeGlobalEligibilityMask`, `0030B770`): the DWORD result is zeroed at + 0x15, and only
  its low WORD is written after that. The high WORD is 0 for every input. The low WORD is 0..31: bit `0x1` when `02089340` has any of 0x3080, bit `0x2` from
  bit `0x1` of `022C2158`, and bits `0x4`, `0x8` and `0x10` from its bits `0x400`, `0x200` and `0x800`.
- **Unit** (`0030B7F0(unit, edx)`): 0 unless the unit is non-NULL and bit `0x10` of its first DWORD is set. Its high
  WORD has two bits *(FABLE)*:
  - bit `0x1` when the first setting read is 1, unit `+0x698` is non-NULL and that record's byte `+5` is 0;
  - bit `0x2` when the second read is 2.
  Both reads go through `0017D470`, which returns DWORD `+0xC20` of the settings object. Two calls make two reads, so the
  high WORD is 0..3 in general and 0..2 when both reads see one value. The low bit `0x2` needs EDX != 0. The MP writer
  `00300CE0` passes EDX = 0 at both its call sites.
- **The settings root** (read by the accessor `0017D470` calls first): a non-NULL root at `01F81428` is returned as is, with no call. A NULL root
  allocates 0x10E8 bytes, runs the constructor `001CCB20` on success and stores the result as the root. A failed
  allocation leaves it NULL, and the getter then reads `[0xC20]`.
- **Premises:** an initialized root, no other write to the root or `+0xC20` during the query, and private frames
  under the Win64 ABI.
