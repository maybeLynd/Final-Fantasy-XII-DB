---
system: Combos and the guard/parry flag
category: 08-Combat-Formula
note_kind: function
parent: ../07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md
status: DOCUMENTED — its one registered residue, GR-8, is ANSWERED (owner re-status 2026-09-30, OPUS) — the unmapped fields of the per-unit 64-byte record were registered (GR-8, since answered: the second half is never accessed and every field of the first half has a reader); "status bit 23" is the target unit's engaged flag and 02AEDFE4 is the combo chance ComputeComboChance writes (Findings, 2026-09-30); the combo cap reads the attacker, not the target (corrected 2026-09-30); converted to the NOTE template 2026-09-30 (FABLE)
owner_layer: PrimaryOwner:CombatFormula
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 5 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: pair-frontier-repos-55
  crossref_clean: false
  reopened_count: 0
---

# Combos and the guard/parry flag

**The pair frontier's third candidate:** `02AEDFC4`, touched by **five `BattleFormula_*` functions**,
three of them documented, **and no document citing two of them.** Reading two settles what the field is
and produces a mechanic nobody had written down.

## Scope (FABLE, 2026-09-30)

This note carries the function-level evidence for two calculator slots: the combo-count roll
`BattleFormula_RollAndStoreComboCount` (`00388660`, slot 10) and the guard/parry pre-roll
`BattleFormula_RollGuardParryMode` (`003884F0`, slot 8). It also shows how the first overrules the second. Its parent,
[how a combo continues and what it blocks](../07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md), owns the
continuation mechanism (the `+0x6B7` counter, its writers and readers), the call chain, the player view and the modding
notes. The scratch words the two slots use are censused on [the formula scratch block](Scratch-Block/the-formula-scratch-block.md).
*(Converted to the NOTE template 2026-09-30, FABLE. The content below is the page's own, regrouped; additions are dated.)*

## Findings (FABLE, 2026-09-30)

Each finding is anchored in the text and tiered in the Evidence table.

### The lower your health, the longer your combo (FABLE, 2026-09-30)

`BattleFormula_RollAndStoreComboCount` (`00388660`) decides how many extra hits a strike lands.

**First, one roll decides whether there is a combo at all:**

```asm
00388705  mov  eax, 0x51EB851F        ; the compiler's % 100
00388716  cmp  dword ptr [0x02AEDFE4], r8d
0038871D  jbe  <no combo>             ; draw >= threshold -> nothing
```

**Then the per-hit chance is chosen from the attacker's remaining health as a fraction of its
maximum:**

| remaining | chance per extra hit |
|---|---:|
| below **1/16** of maximum | **0x40** |
| below **1/8** | **0x20** |
| below **1/4** | **0x10** |
| otherwise | **0x08** |

**and that chance is rolled eleven more times**, one extra hit per success. *(Anchored 2026-09-30, FABLE:
`003887DA mov r14d, 0xb` / `003887E0 mov ebp, r14d` set the trip count, the loop `003887E3`–`00388807` draws once per
pass, and `00388801 inc ebx` adds a hit when the draw is under the chance.)*

> **A wounded attacker hits more often, and the effect is eightfold between full health and a
> sixteenth.** The bands are computed from the same max-health expression as the derived-state
> rebuild — `+0x24`, **doubled when status bit 28 is set**, or `+0x48` clamped to at least 1 when
> status bit 16 is — so **the two documents agree about how maximum health is obtained.**

**The total is capped twice:** by a byte of the ~~target's~~ **attacker's** `.ard` slot-0 class row (`[+0xE68] + 0x20`, minus one; the unit's class row, not its stats record — [the unit-definition page](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.1)
when the ~~target~~ **attacker** is a foe, and by **11** unconditionally. **So the ceiling is twelve hits, and a foe's
own record can lower it.**

> **Corrected 2026-09-30 (FABLE): the cap reads the attacker, not the target.** The class row comes from
> `BattleStats_FindOwningBattleUnit` called on `rsi` (`00388809`–`0038880C`). `rsi` is the function's first argument
> (`0038866E`), the same stats record whose health picks the band above. Every calculator slot is called with the
> **source's** stats first and the target's second: `003863CA`–`003863D0` pass `r14` and `rsi`, and `003860BF`–`003860D5`
> hand the same two to `BattleFormula_BuildEvaluationContext` as source and target
> ([the evaluation context](Evaluation-Context/the-evaluation-context-field-map.md) §5). The foe test is the owning unit's
> stats byte `+5 == 1` (`00388827`–`00388837`). So a foe's own class row limits the combos **it** lands, and nothing about
> the target limits a combo.

**The result is stored in the high nibble of one byte** of a 64-byte per-unit slot — `0208D480 + kind
× 0x40` on the party side, `0208DE80 + slot × 0x40` otherwise.

**And a stored value can replace the whole computation.** If `+0x6B7` is non-zero, **no roll happens
at all**: the stored nibble is compared against it and the combo is accepted or refused.

> **CORRECTED 2026-09-03 — and the correction inverts what the branch means.** This document first
> called `+0x6B7` *"the source's record byte"* and concluded *"a forced combo count is a field, not a
> special case."* **Both halves are wrong.**
>
> **The byte is on the unit, not on the record.** The two objects are built separately in this
> function — `FindOwningBattleUnit` produces the unit the gate reads (`00388679`–`0038868A`), while the
> record `0208D480 + kind*0x40` (`003886A7`–`003886B6`) is where the **stored nibble** lives.
>
> **And it is a runtime counter with exactly two writers:** `BattleAction_TryContinueComboSequence`
> **increments** it, `BattleUnit_CancelAndResetCurrentAction` **clears** it. **There is no authored
> field and no forced-value path.**

**So the skipped roll is memoisation, not a designer override.** The count was decided on hit 1 and
kept in the nibble; hits 2..N compare progress against it — **`>=` ends the combo, `<` continues.**

**The difference is not cosmetic.** An authored record byte would be **a per-action knob a modder could
set**; a runtime counter cleared by the action reset **is not patchable the same way.**

**And a combo is not an animation with a length.** `0030FA00` **re-commits the same action** — reading
`+0x708`, `+0x714` and `+0x710` and calling the commit function with all three unchanged — and **only a
successful commit advances the counter.**

**Two consequences of that one byte, neither previously written down:**

- **You cannot move while your combo is running.** A non-zero counter is an unconditional `return 0` in
  `BattleUnit_CanAdvanceCombatNavigation` (`00325DDF cmp byte ptr [rdi + 0x6b7], 0` and `00325DE6 ja` to
  `00325DA5`, `xor eax, eax; ret`; *anchored 2026-09-30, FABLE*).
- **A combo in progress overrides the leader's party-control suppression wholesale** (`0023B12D`,
  a `cmova`) — **discarding the flags accumulated above it rather than adding one.**

### The field the two functions share, and it runs both ways (FABLE, 2026-09-30)

`BattleFormula_RollGuardParryMode` (`003884F0`) **writes** `02AEDFC4`:

```c
if (target_flags bit 23) {
    draw = mt19937();
    02AEDFC4 = (draw % 100 < 02AEDFDC);      // a percentage against a global threshold
}
```

**and the combo function clears it:**

```c
if (result_flags & 2) { 02AEDFC4 = 0; 02AEDFC8 = 0; }
```

> **A landed combo cancels the guard/parry outcome.** One function rolls it, the other erases it, and
> **the erasure is conditional on the combo having been accepted** — so the two are not independent
> steps of a pipeline, they are **a later stage overruling an earlier one.**

**Neither function names the other**, and until this pair was compared **no document mentioned both.**

### What the bit-23 test reads, and who sets the two thresholds (2026-09-30, FABLE)

- **"Bit 23" is not a status bit.** `003884F0` hands its **second** argument, the target's stats, to
  `BattleStats_FindOwningBattleUnit` (`003884F4`–`003884F7`). It then tests bit 23 of the returned **unit's** flag word
  (`00388508`–`00388510`, `shr eax, 0x17; and eax, 1`). Unit flag bit 23 is the **engaged** flag: the engaged-state
  setup sets it and its partner clears it
  ([how a battle unit is built](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.9;
  [the battle-unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md), flag bit 23). **So only an
  engaged target can parry.** In the code block above, `target_flags` means the target unit's flag word, not its
  status layers.
- **`02AEDFE4`, the combo gate's threshold, is the combo chance.** `BattleFormula_ComputeComboChance` writes it
  (`00388550`, at `00388648`), and `BattleFormula_ResetScratchState` zeroes it (`003849B0`, at `003849F8`)
  ([the scratch block](Scratch-Block/the-formula-scratch-block.md) §2.2). `02AEDFDC`, the parry threshold, is written by
  `BattleFormula_ComputeParryChanceFromSpeed` (`00388490`; the 2026-09-11 note under Limits).
- **The byte that holds the count is fully mapped.** Record `+0x12` bit 0 is "a preview is stored", bits 1–3 are the
  previewed result's flag word B bits 1–3, and bits 4–7 are this count
  ([the scratch block](Scratch-Block/the-formula-scratch-block.md) §2.5). The rest of the 64-byte record is only partly
  mapped (`GR-8`, Limits).

## Evidence (FABLE, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| One percent gate decides whether there is a combo | `003886FD`–`0038871D`: `draw % 100` by the `0x51EB851F` reciprocal; `jbe` past the combo unless `[02AEDFE4]` is above it | 1 |
| The four health bands and their per-hit chances | `00388723`–`003887D6`: `>> 4`, `>> 3`, `>> 2` of maximum HP against current HP `+0x48`; chances `0x40`, `0x20`, `0x10`, else `0x08` | 1 |
| Maximum HP is `+0x24`, doubled under status bit 28, or `+0x48` (at least 1) under status bit 16 | `0038872B`–`00388757` | 1 |
| Eleven further rolls, one hit each | `003887DA`–`00388807` | 1 |
| The count is capped by the attacker's class row when the attacker is a foe, and by 11 | `00388809`–`0038884D`; `00388850`–`00388853` | 1 |
| Calculator slots take the source's stats first, the target's second | `003863CA`–`003863D0` with `003860BF`–`003860D5` | 1 |
| The count is the high nibble of record `+0x12`; later hits compare progress against it | `0038885D`–`00388865`; `0038886B`–`00388874` | 1 |
| The guard/parry roll needs the target unit's flag bit 23 and compares against `[02AEDFDC]` | `003884F0` read whole (82 B): `003884F4`–`00388537` | 1 |
| An accepted combo clears `02AEDFC4` and `02AEDFC8` | `00388891`–`003888AB` | 1 |
| A non-zero counter stops combat navigation | `00325DDF`–`00325DE6`, target `00325DA5` | 1 |
| A running combo replaces the leader's accumulated suppression flags | `0023B124`–`0023B12D`, `cmova` | 1 |
| `02AEDFE4` is written by `BattleFormula_ComputeComboChance` | `00388648`; reset at `003849F8` | 1 |

### Falsification pass — 2026-09-03 (FABLE, 2026-09-30)

| attack | result |
|---|---|
| Are the four bands really 1/16, 1/8, 1/4? | Three successive `>> 4`, `>> 3`, `>> 2` with the standard negative-rounding correction, each against the same maximum. **Three shifts, three comparisons, one fallthrough.** |
| Is the per-hit chance a percentage? | Every draw is reduced `% 100` by the `0x51EB851F` reciprocal before comparison. **A comparison against a modulo-100 value is a percentage.** |
| Is the combo cap 11 or 12? | The count starts at **1** and eleven further rolls can each add one — **twelve maximum**, then clamped to `0xB` **as a count of additions**. Both readings appear in the arithmetic and the clamp is applied to the accumulator, not to the total. **Stated as: one hit plus up to eleven.** |
| Does the combo really clear the guard flag, or write a different global? | **Same address `02AEDFC4`** written by one and zeroed by the other, with `02AEDFC8` zeroed alongside. |
| Is the forced-value path a debug feature? | **The question was malformed and the open answer is why it was correctable.** This row first read *"a record byte with a stored comparison; nothing here says who writes `+0x6B7`"* — **leaving the writer open is what kept the error from becoming load-bearing.** It is a **unit** field with **two** writers and no authored path. |
| Is `+0x6B7` a byte or part of a wider field? | **`003106EB` clears `+0x6B7` and `+0x6B8` with a single `word` store** — which **bounds the bytes touched, not the field width.** Every other access in the image is byte-wide: **two one-byte fields cleared together.** |

## Limits (FABLE, 2026-09-30)

**What this document does not claim:** what `02AEDFDC` and `02AEDFE4` hold or who sets them, what
status bit 23 on the target means, what the other bits of the 64-byte slot hold, what `02AEDFC8` is, or
what consumes the guard/parry flag downstream.

*(2026-09-11: three of those are now read — `02AEDFC8` is the knockback roll's outcome
(`BattleFormula_RollKnockback` `00388440`), `02AEDFDC` the parry chance from speed
(`BattleFormula_ComputeParryChanceFromSpeed` `00388490`), and the guard/parry flag is consumed by the
outcome roller (`0038970A`, `00389779`: kinds 4 / 2 instead of 3 / 1) and by the preview into the
result's flag word B bit 2 — [the scratch block](Scratch-Block/the-formula-scratch-block.md) §2.2–2.4.)*

*(2026-09-30, FABLE: the rest, dispositioned.)*
- **Who sets `02AEDFE4`:** `BattleFormula_ComputeComboChance`. Answered (Findings, "What the bit-23 test reads").
- **What "status bit 23 on the target" means:** it is not a status bit. It is the target unit's engaged flag, unit flag
  bit 23 (Findings). The question named the wrong word; answered.
- **What the other bits of the 64-byte slot hold:** the count's byte `+0x12` is fully mapped (Findings). The record's
  other fields are mapped only in part: `+0x00`, `+0x04`, `+0x08`, `+0x10` and `+0x12` on the scratch block §2.5, and a
  flag at `+0x1C` that movement code sets, on the battle-unit field map. The rest is registered as **`GR-8`**.
  *(Answered 2026-09-30, OPUS `48de14c6b`; register row GR-8, record [`gr8-unit-record-64-0930`](../_index/candidates/gr8-unit-record-64-0930/README.md): the second half, `+0x20`..`+0x3F`, is never accessed, and every field of the first half has a reader except three padding bytes. `+0x00` is a u32 - the u64 is the preview's clear. The record lists the scratch-block section 2.5 and field-map corrections, routed to their owner.)*
- **Not claimed here:** how `BattleFormula_ComputeComboChance` computes the chance (the scratch block owns that word), and
  anything executed. Every claim in this note is a static read.

## Method (FABLE, 2026-09-30)

Static reads of the shipping image (the `exe_sha256` above), with the FABLE kit in `Database/Tools/work/FABLE/pub140-scratch`:
- `python disr.py 00388660` and `python disr.py 003884F0`: both bodies read whole (602 B and 82 B).
- `disr.py` on `BattleUnit_CanAdvanceCombatNavigation` up to `00325DE8`; on
  `PartyControl_RecomputeSuppressionFromLeaderBattleState` over `0023B110`–`0023B170`; and on
  `BattleFormula_ResolveTargetResult` over `003860B0`–`003863E0` for the argument order.
- Callers from `tools/rawcalls.json`: neither slot has a direct call site. **Positive control:** the step table's qwords
  at `01EFA600` and `01EFA610` read back as `003884F0` and `00388660`, slots 8 and 10. That matches the slot list in
  [attack-vs-defence preparation](Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) (`AJ-7`), so the
  missing direct calls are the table dispatch, not a blind index.
- The scratch words' writers and readers are the scratch block's census; it was not re-run here.
- Nothing was executed live for this note. OPUS executed the combo roll against an independent model
  ([s20-opus-replay-combo-roll](../_index/candidates/s20-opus-replay-combo-roll/README.md)), which
  [the combo contract](../07-Combat-Action/CONTRACT-combo-continuation.md) cites for its roll claim.

## Why this document exists

**Five functions touch `02AEDFC4`. Three are documented. No document cites two of them.** The mechanic
above is what fell out of reading two — **a health-scaled combo chance and a later stage overruling an
earlier one, neither visible from either function alone.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleUnit_UpdateCombatFrame`, owned by that layer, calls `0030FA00` on this page. That caller is the per-unit combat frame step, behind `byte[02089340] & 0x20`: it tests the unit's stats record for bit 4 of the OR-ed `+0x3C`/`+0x64` pair - the **sixth** entry point on that pair - and on the retire path appends `dword[unit+8]` to a **64-entry ring** at `022BE984` whose index at `byte[022BE981]` wraps with `& 0x3F`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**RNG_Random_Selection — SERVICE (3 edges).** `BattleFormula_RollAndStoreComboCount` (`00388660`), `BattleFormula_RollGuardParryMode` (`003884F0`) and `BattleFormula_RollKnockback` (`00388440`) each call `RNG_MT19937_NextU32_Thunk` (`00379CD0`). The combo count, the guard/parry mode written to `02AEDFC4` and the knockback roll are all draws from the gameplay Mersenne Twister, so the health-scaled combo length and the parry flag this page describes depend on that shared stream's position.
