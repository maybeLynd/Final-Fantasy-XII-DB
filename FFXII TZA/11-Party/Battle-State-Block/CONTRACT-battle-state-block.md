---
contract: Bind, validate and reset the 0x7410-byte battle state block that lives inside the save payload
category: 11-Party
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 11-Party/Battle-State-Block/the-battle-state-block-field-map.md
entries: ["00233C10", "002370C0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — the binder read in full with **all three of its arms traced to what each one
    invokes**, and the reset read with **its clear size, its magic rewrite and its selector loop's
    bound taken at their instructions**, the bound being the fact §4's last invariant turns on.
    **This records checks performed on that date, not the method of the original derivation**, which
    is on the field-map page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-battle-state-block-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the battle state block

> **Authored 2026-09-22 by FABLE.** S-28's binding gap is *"slot assignment only, of 4 pages"*.
> Three of the four are contracted; **this takes the fourth, so all of S-28's pages now carry one.**
>
> Written against FRONTIER's adequacy test. **`BS-5` is why this could not be a narrower contract:**
> the reset's behaviour is only meaningful against the five slot maps, and what it leaves behind is
> not what [the slot-maps contract](../CONTRACT-the-five-parallel-slot-maps.md) describes after the
> *other* initialisation path.

## 1. Purpose

Find the battle state block, decide whether what is there can be trusted, and clear it when it
cannot.

## 2. Interface

| | body | note |
|---|---|---|
| **the binder** | `00233C10`, 214 B | three arms, and they do not invoke the reset the same number of times (`BS-2`) |
| **the reset** | `002370C0`, 121 B | clears `0x7410`, rewrites the magic, fills **one** map (`BS-3`, `BS-5`) |
| **what the binder invokes** | `BattleSystem_ResetRuntimeState` (`00237DF0`), 173 B | runs `002370C0` first (its first call `0023AF50` makes `002370C0` its own first call), then re-initialises the forty stats records, and at `00237E41` calls the slot-map initialiser `00329CC0` (2026-09-29, OPUS falsification pass 1, `CON-171`) |

## 3. Types

```
[02EBF190] -> the battle state block, 0x7410 bytes
  +0x0000  u32      the magic 0x05071901
  +0x0004  u32      the flag dword
  +0x0008  BattleStatsRecord[40]   stride 0x1C8
  +0x5A48  u16[9]   slot map 0     \  the five parallel maps
  +0x5A5A  u16[9]   slot map 1      |  -- see CONTRACT-the-five-parallel-slot-maps.md
  ...      through map 4 at +0x5A90 /
  +0x5AC8  u32      accumulator, zeroed by the reset
  +0x5ACC  u32
```

## 4. Preconditions · postconditions · invariants

### The five cross-operation invariants

**BS-1 — The block is PART OF THE SAVE PAYLOAD, not a heap allocation.** The binder takes the active
runtime buffer and adds `0x4E68C` (`00233C25`–`00233C2A`). *So its lifetime is the save image's, its
contents are serialised, and anything inside it — the forty stats records, the five slot maps, the
inventory descriptors — is save state rather than session state.*

**BS-2 — The binder has THREE arms and they do not reset the same number of times.** Read at the
instructions:

| arm | test | what it invokes |
|---|---|---|
| unbound | `00233C20 test rax, rax` / `jne` | rebase the inventory descriptors, then **`BattleSystem_ResetRuntimeState` TWICE** — once by `00233C3F call` and again by `00233C48 jmp`, the same target |
| bound, magic wrong | `00233C4D cmp dword ptr [rax], 0x5071901` / ~~`jne`~~ the fall-through past `00233C53 je` (2026-09-29, OPUS falsification pass 1, `CON-171`) | the reset **once**, by tail-jump at `00233C59` |
| bound, magic right | `00233C53 je` | neither — it proceeds into the body at `00233C5E` |

> ***The first-bind path runs the reset twice and that is a reading, not an inference:*** the `call`
> at `00233C3F` and the `jmp` at `00233C48` name the identical address, with only the stack
> adjustment between them. *A reimplementation that resets once is observably different for anything
> the reset is not idempotent over, and `BS-3` is exactly such a thing.*

**BS-3 — The reset REWRITES THE MAGIC, so a reset block is valid rather than blank.** `002370C0`
memsets `0x7410` bytes to zero (`002370CD`/`002370D3`) and then stores `0x05071901` back at offset 0
(`002370DF`). ~~*So the second invocation on the first-bind path takes a block whose magic is already
correct — the two resets are not two identical operations against the same input, and any later
binder call sees a valid block rather than a zeroed one.*~~ *Any later binder call sees a valid block rather than a
zeroed one.* **The block's prior contents cannot make the two resets differ** (2026-09-29, OPUS falsification pass 1, `CON-171`):
- the reset reads nothing before the memset: `00237DF0` and `0023AF50` each call before any memory read, and
  `002370C0` loads only the block pointer;
- the magic already being set is therefore invisible to the second invocation.

Whatever differs between the two invocations lies outside the block.

**BS-4 — Forty stats records at `+8 + i × 0x1C8`.** Carried from
[the field map](the-battle-state-block-field-map.md) §2.2: every offset of the stats record map
applies at `+8 + d` for record 0.

**BS-5 — The reset fills ONLY map 0 with the empty marker, and leaves maps 1–4 ZEROED — which is a
DIFFERENT value.** The selector loop starts at `0x5A48` and its bound is
`0023710F cmp rcx, 0x5a5a`, so it writes `0xFFFF` over exactly `0x12` bytes — **nine `u16`, stopping
at map 1's base**. Maps 1, 2, 3 and 4 keep the zero the `memset` left.

> **Where this state survives** (2026-09-29, OPUS falsification pass 1, `CON-171`). It exists after `002370C0` alone. **The binder never leaves it
> behind.**
> - The binder's reset is `00237DF0`, which runs `002370C0` and then `00329CC0` before returning; `00329CC0` fills
>   map 0 from the authored table and copies it into maps 1–4.
> - So after a binder reset the five are identical: `SM-4`'s state, not this one.
> - The disagreement below survives only where `002370C0` is called directly: `00239960`'s scenario arm at
>   `002399E9` ([the setsavedata presets](../the-setsavedata-presets-test-battle-scenarios.md)). That arm writes map 0
>   through `00329080` and reaches neither `00329CC0` nor the refresher `003266C0` through direct calls to depth 8.
>   Indirect calls were not followed.
>
> **So immediately after ~~a reset~~ `002370C0` the five maps do not agree, and they disagree in the one way that
> matters: `0xFFFF` is the empty marker and `0` is not.** *A class-0 lookup returns `0xFF`; a
> class-1-to-4 lookup returns `0` — a low byte that reads as slot zero rather than as a refusal.*
> **This is the state [the slot-maps contract](../CONTRACT-the-five-parallel-slot-maps.md)'s `SM-7`
> describes from the other side** — the derived maps are stale until the refresher runs — and it
> shows the stale value is not merely old, it is a *different kind* of value. *It is also not the
> state `SM-4` describes: that is the OTHER initialisation path, which fills map 0 from an authored
> table and copies it into all four. The two paths leave the block differently, and only one of them
> leaves the five identical.*

## 5. State

**Owned:** the whole `0x7410`-byte block, through the pointer global. **Not owned:** the save runtime
buffer it sits inside, and the inventory class descriptors the binder rebases into it.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`../CONTRACT-the-five-parallel-slot-maps.md`](../CONTRACT-the-five-parallel-slot-maps.md) — `BS-5` is `SM-7`'s other side |
| **Sibling** | [`../CONTRACT-party-slot-assignment.md`](../CONTRACT-party-slot-assignment.md) and [`../CONTRACT-party-focus-and-control-suppression.md`](../CONTRACT-party-focus-and-control-suppression.md) — S-28's first two |
| **Contains** | the forty stats records, whose field map is [the stats record page's](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) |
| **Corrects** | [the save payload field map](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) — its extent was the scan's reach, and `BS-1` places this block inside it |

## 7. State transitions

*unbound → bind, rebase, reset, reset → bound-and-valid.* *bound with a wrong magic → reset →
bound-and-valid.* *bound and valid → proceed.* **A block never stays zeroed**: every path that
memsets it also rewrites the magic (`BS-3`).

## 8. Script · resource · event interactions

The block is serialised with the save image (`BS-1`). The inventory descriptors inside it are rebased
on every bind.

## 9. Determinism

Deterministic. No generator is drawn.

## 10. Failure paths and edge conditions

- A wrong magic is not an error: it silently resets (`BS-2`).
- After ~~a reset~~ `002370C0` alone (the setsavedata scenario arm), a class-1-to-4 slot lookup returns `0` rather
  than a refusal (`BS-5`). After the binder's reset it returns map 0's low byte, because `00329CC0` has run (`CON-171`).
- The first bind resets twice (`BS-2`).

## 11. Observable behaviour

None directly. This is where the party, its stats and its battle slots live between saves; the
visible consequence of `BS-5` is a slot lookup answering "slot 0" for a party that has not been
built yet: on the setsavedata scenario path, not after an ordinary bind (`CON-171`).

## 12. Reproduction formula

Bind with the global null and assert the reset runs **twice** (`BS-2`). Corrupt the magic, bind, and
assert exactly one reset and a restored magic (`BS-2`, `BS-3`). Run `002370C0` alone and then read `+0x5A48` and
`+0x5A5A`: assert **`0xFFFF` at the first and `0` at the second** (`BS-5`). Bind with the global null and assert
map 1 equals map 0 afterwards, because `00329CC0` ran inside the reset (`CON-171`). Assert the memset length
is `0x7410` and that offset 0 is non-zero afterwards (`BS-3`).

## 13. Runtime validation

**None.** No experiment executes these bodies. S-28's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*

## 14. Unresolved

- What the second reset on the first-bind path is for. `BS-2` establishes that it happens; nothing
  read here says why. ~~and the two invocations differ only in the block's magic being already set.~~ The block's
  prior contents cannot distinguish them, because nothing reads the block before the memset (`CON-171`). Any
  difference lies in state outside the block.
- The writer side of the block generally. [The field map](the-battle-state-block-field-map.md) §2.1
  states its own census is seeded on accessors, so **writes are under-covered wherever a constructor
  or an index-derived writer sits outside the seeds** — this contract inherits that limit and does
  not make absence-of-writer claims.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `BS-1` — inside the save payload | `00233C25`–`00233C2A` read at the instructions | 1 |
| `BS-2` — three arms, two resets on one of them | `00233C20`, `00233C4D`, `00233C53` traced to what each reaches; the `call` at `00233C3F` and the `jmp` at `00233C48` compared and found to name one address | 1 |
| `BS-3` — the magic is rewritten | `002370CD`/`002370D3` for the length, `002370DF` for the store | 1 |
| `BS-5` — only map 0 is filled | the loop's bound read at `0023710F cmp rcx, 0x5a5a`, which is map 1's base, against the start `0x5A48` — a span of `0x12`, nine `u16` | 1 |
| `BS-4` and the field layout | [the field map](the-battle-state-block-field-map.md) §§2.2–2.3, falsified 2026-09-12 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `BS-1` through `BS-5`. **`BS-5` is the one a port
gets wrong by being tidy**: filling all five maps with the empty marker is the obvious reading of
"reset the slot maps", and it changes what every class-1-to-4 lookup returns between ~~the reset and
the first refresh~~ `002370C0` and the next write of maps 1–4. On the binder's path that write is inside the same
reset (`00329CC0`), so only the setsavedata scenario arm exposes the difference (`CON-171`). **`BS-2`'s double reset is the one a port silently drops**, and it only shows
where the reset is not idempotent.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Party — internal.** The block, its binding, its reset and the five maps inside it are this
  category's own.
- **Save_Load_Settings — SERVICE, and `BS-1` is the statement.** `SaveImage_GetActiveRuntimeBuffer`
  is that layer's; this contract asserts **the offset applied to its result and that the block
  therefore lives inside the save payload**, both visible at the call site, and nothing about how the
  buffer is produced or serialised.
- **Items_Equipment_Shops_License — SERVICE.** The inventory descriptor rebase on the bind path is
  that layer's; **`BS-2` asserts only that it happens on the unbound arm and before the resets**, not
  what rebasing does.
- **Gameplay — SERVICE, and it is the body `BS-2` COUNTS.** `BattleSystem_ResetRuntimeState` belongs to that layer,
  and is **named rather than cited by address**, because this contract counts its invocations and
  never reads it. **This contract asserts only HOW MANY TIMES each binder arm
  invokes it — twice on the unbound arm, once on a magic mismatch, never on a match — which is a
  property of the binder's control flow and is read there.** What resetting runtime state does is
  that layer's and is not read here, which is also why §14 records the second invocation's purpose
  as unknown rather than guessing it.
- **CombatAI and CoreRuntimeScheduling — MECHANICAL.** Two further callees of the binder belong to
  those layers. *They are reached only because `BS-2` required reading the binder in full; no arm's
  invocation count depends on them and neither body is read.*
- **Every other layer reached is MECHANICAL**, through these two bodies' own callees — the `memset`
  and the runtime-state reset among them. *Their addresses are deliberately not cited beyond the two
  entries: each is a hub, and naming one imports its whole edge set for a statement §4 already makes
  by name.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun. *"Party" and "save" would otherwise each be cleared by
> the word alone.*

## 17. Related

- [The battle state block field map](the-battle-state-block-field-map.md) — the mechanism
- [Contract — the five parallel slot maps](../CONTRACT-the-five-parallel-slot-maps.md) — `BS-5`'s other side
- [The battle stats record field map](../../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) — the forty records

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **CombatAI - SERVICE (1 edge).** `00233C10` reaches bodies filed to combat AI: `00327F80` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - SERVICE (1 edge).** `00233C10` reaches bodies filed to core runtime: `00229ED0` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - SERVICE (1 edge).** `00233C10` reaches bodies filed to Gameplay: `00237DF0` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT and SERVICE (2 edges).** `002370C0` is also called by bodies filed to items/equipment: `0023AF50`; `00233C10` reaches bodies filed to items/equipment: `0030B6A0` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (1 edge).** `00233C10` is also called by bodies filed to SaveLoad (save/load settings): `00280140` (RuntimeLifecycleSupport) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (1 edge).** `00233C10` reaches bodies filed to save/load/settings: `002EF640` - shared machinery across the layer boundary, no shared ownership.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — SERVICE and CLIENT (5 edges).** `BattleSystem_ResetRuntimeState` `00237DF0` calls `BattleSlotMap_InitializeMappingClasses` `00329CC0`; `BattleGroup_RefreshFourActorDefinitions` `003266C0` calls `BattleUnit_ApplyUnitDefinition` `0023A570`, `ActorWork_GetBattleUnitRaw` `00263E30` and `BattleUnit_TeardownAndDespawn` `00300E40`, and is called by `00233CF0`, a 36-byte step that calls one helper with 0, the refresher, a second helper with 1, and returns 1. The block's slot maps are initialised by the actor layer's mapper (copying map 0 into maps 1–4, `CON-171`), and the four-actor refresh re-binds or tears down units through that layer's own lifecycle bodies.

**CombatAction — SERVICE (1 edge).** `003266C0` calls `BattleUnit_CancelAndResetCurrentAction` `003105D0`. Before tearing a unit down and re-applying its definition, the refresh cancels that unit's current action (`00326AA9`); the action state is that layer's, and the block contract only records that the refresh runs.

**CombatFormula — SERVICE (3 edges).** `00237DF0` calls `BattleStats_InitializeDefinitionRecord` `0023AC80`, and the scenario arm `00239960` calls `0023AC80` and `BattleStats_GetByBattleSlotIndex` `00320A40`. Both resets re-initialise stats records through the formula layer's initialiser (the forty records of §2) and look records up by battle slot; the record layout is that layer's.

**Movement — SERVICE (1 edge).** `003266C0` calls `00311E20`, a 93-byte body that, when the dword `022BE974` is zero, takes the actor in the roster slot a party helper returns, reads its world position and then tail-jumps into a Movement routine. It is the refresh's first call (`003266EF`); what locomotion does with that position is that layer's business.

**Rewards_Progression_Economy — SERVICE (2 edges).** `00239960` calls `GameState_SetGilClampedNonnegative` `00300500` and the level setter `0030C470`. The scenario arm sets gil from a word of its scenario row (`+0xE`) and a unit's level from a row byte (`+2`); the gil and level writers are the rewards layer's, and the BS-5 note is what this contract says about that arm.

**UI — SERVICE (1 edge).** `00237DF0` calls `00313840`, a 134-byte body that clears bit 0 of the block's dword `+0x5B04` (calling a notifier when it was set), zeroes `+0x5AD5`, `+0x5AD8` and `+0x5ADC`, sets `+0x5AD4` to `0x1B` and clears bits 0 and 1 of `+0x5AD0` — all through the block pointer `02EBF190`. The reset hands a UI-filed body part of the block's state to clear; the fields sit inside this contract's block even though the body is filed to UI.

**WorldAreaField — CLIENT and SERVICE (8 edges).** `BattleSystem_InitializeAreaState` `002342F0` calls `00239960`; `SaveImage_GetActiveRuntimeBuffer` `002EF640` is called by `WorldTransitionSnapshot_CaptureRuntimeState` `00229B40`, `WorldTransition_StageFieldTransition` `003145E0` and `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` `005843E0`; `003266C0` calls `FieldData_GetActiveFieldRecordBit15` `00377C20`, its thunk `00313F60` and `00377C70` (which returns bits 4–6 of the current field's navimapdata row byte); `00329CC0` calls `WorldTransition_GetActiveOrPendingFieldId` `003148F0`. The area initialiser runs the scenario arm, the world-transition snapshot and restore read the same runtime save buffer the block lives in (`+0x4E68C` from it), and the refresh and the slot mapper consult the current field's record and id.

## Falsification pass 1 — 2026-09-29 (OPUS): the bytes survive; the binder's reset is a different body, and BS-5 holds only on the scenario path

**Attack.** BS-1 to BS-3 and BS-5 became checks at their instructions, and the body the binder actually invokes was read.
Script: `Tools/analysis-kit/gfz-scripts/falsify_battle_state_block.py`, output `falsify_battle_state_block.out`, image
`73461d08…`, 0 BROKEN. BS-4 is carried from the field map.

| # | Clause attacked | Result |
|---|---|---|
| K1 | §2 / BS-2 / BS-3: the binder's reset is `002370C0` | **refuted** (`CON-171`): the binder reaches only `BattleSystem_ResetRuntimeState` (`00237DF0`). It runs `002370C0` first (via `0023AF50`) and calls `00329CC0` at `00237E41`; its only conditional branch is the record loop |
| K2 | BS-5, §§10, 11, 16: after a reset maps 1–4 are zero | **refuted for the binder** (`CON-171`): its reset returns after `00329CC0` copies map 0 into maps 1–4. The zeroed maps survive only `00239960`'s scenario arm (`002399E9`), which reaches no map-1–4 writer through direct calls to depth 8 (738 functions) |
| K3 | BS-3: the second first-bind reset differs because the magic is set | **refuted** (`CON-171`): nothing reads the block before the memset |
| B1 | BS-1 | **survives**: `call 002EF640`, `add rax, 0x4e68c`, stored to `02EBF190` |
| B2 | BS-2's arms and counts | **survives**: two on the unbound arm, one on a wrong magic, none on a right one. The wrong magic is the fall-through past `00233C53 je`, not a `jne` |
| B3 | BS-3's bytes | **survives**: `mov r8d, 0x7410`, memset, magic store at `002370DF` |
| B4 | BS-5's loop in `002370C0` | **survives**: from `0x5A48`, `0xFFFF` words, bound `cmp rcx, 0x5a5a` |
| B5 | §3, §2 sizes | **survives**: `+0x5ACC` and `+0x5AC8` zeroed; 214 B and 121 B |

Corrected in place: §2, the BS-2 table, BS-3, BS-5, and §§10, 11, 12, 14, 16. Also corrected: one ordering sentence in
`CONTRACT-bazaar-unlock-and-purchase.md` (OPUS's own). The consumer record is
`_index/candidates/battle-state-block-falsification-pass-1-0929/`.
