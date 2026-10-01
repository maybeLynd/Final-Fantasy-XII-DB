---
contract: Dispatch an authored recipe through 202 formula-step slots that communicate only through one shared scratch record
category: 08-Combat-Formula
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 08-Combat-Formula/Step-Table/combat-formula-step-table.md
entries: ["0038D280", "0038AAF0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's figures **re-measured from
    the table's own bytes rather than carried** — the extent walked until the first non-pointer, the
    distinct-target count taken over the 202 slots, the no-op target's body read, and the multi-id
    targets enumerated with their slot ids. **The counts close arithmetically against each other**,
    which is §15's control. **This records checks performed on that date, not the method of the
    original derivation**, which is on the step-table page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-step-table-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the formula step table

> **Authored 2026-09-22 by FABLE.** S-22's binding gap is *"calculator slots 60-79 only, of 4
> pages"*. Two of the four are contracted; **this takes the third.** The recipe page remains
> uncontracted and this document does not claim it.
>
> Written against FRONTIER's adequacy test. **A contract on any single step would be inadequate**,
> because the steps have no arguments in common and no return values between them — they communicate
> *only* through one shared scratch record, so the recipe's **order** is the whole semantics. That is
> `ST-4`, and it is invisible from inside any step.

## 1. Purpose

Turn an authored list of step ids into a damage calculation.

## 2. Interface

```
stepTable = (void(**)()) 0x01EFA5C0     .data, 8-byte stride, 202 slots, ids 0..201
step(id)  = stepTable[id]
```

The interpreter that walks a recipe is **not read here**; this contract is about the table it
indexes and the discipline the steps share.

## 3. Types

```
02AEE054  u32  \
02AEE058  u32   |  the shared scratch record — the ONLY channel between steps (ST-4)
02AEE05C  u32  /
```

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**ST-1 — 202 slots, and the extent is OVER-DETERMINED rather than asserted.** Walking the table from
`0x01EFA5C0` until the first qword that is not a `.text` pointer stops at **exactly 202**; all 202
are valid pointers and **none is null**. *Slot 202 holds `3F80000000060303` — a float `1.0` beside
packed bytes, not an address — so the table's end is visible in the data and does not rest on the
recipe evidence that first established it.*

**ST-2 — AN ID IS NOT AN IDENTITY: 202 slots, 152 distinct targets, and SEVEN targets carry more
than one id.** Re-measured and enumerated:

| target | ids | count |
|---|---|---:|
| `00389670` | 40, 45, 46 | 3 |
| `0038AA90` | 61, 64, 75 | 3 |
| `00388FE0` | 23, 24 | 2 |
| `00389F80` | 60, 63 | 2 |
| `0038AAF0` `PrepareStrengthAttackVsDefense` | 65, 76 | 2 |
| `0038D280` `FinalizeTargetHpMagnitude` | 113, 125 | 2 |
| `0038F5A0` | 115, 160 | 2 |

> ⚠ **The page says "six targets"; there are seven.** *Corrected here, and the count is not a
> judgement call:* 42 no-op slots share **1** target and the other **160** slots carry **151**, so
> the table's 202 slots over 152 targets leave a **nine-slot surplus** — and the seven rows above
> sum to `3+3+2+2+2+2+2 = 16` slots over 7 targets, which is exactly nine. **The arithmetic closes
> only at seven.**

**ST-3 — 42 slots are NO-OPS, all pointing at one shared body.** `0016D6A0` is `c2 00 00` — `ret 0`,
read at the bytes. *A recipe naming one of those ids is well-formed and does nothing, which is a
way authored data can disable a step without restructuring the list.*

**ST-4 — The steps share NO arguments and NO return values; they communicate only through the
scratch record, so the ORDER in the recipe is the semantics.** Preparation steps (the 60–79 band)
write `02AEE054`/`58`/`5C`; the modifier band rewrites the same three slots; the finalize step reads
them and produces the damage. *So the same step id means different things at different positions in
a list, and a reimplementation may not reorder, memoise or parallelise steps — there is no data
dependence for it to inspect.*

**ST-5 — The finalize is reachable by TWO ids, so a recipe can finalize twice.** Ids 113 and 125
both hold `0038D280`. *Nothing in the table prevents a recipe from naming both, and what that means
is a property of the interpreter this contract does not read.*

**ST-6 — Slots 71 and 73 have no shipped user.** Carried from
[the page](Step-Table/combat-formula-step-table.md) §2: the preparation band is fully named, and two
of its slots are reachable but unused by any shipped recipe.

**ST-7 — Step SELECTION is authored and deterministic; step EXECUTION is not.** Steps named `Roll*`
draw the shared generator. *So two runs of the same recipe on the same inputs agree on which steps
run and can disagree on the result — and for a networked reimplementation the consequence is to
synchronise the stream rather than the outcome.*

## 5. State

**Owned:** nothing. **Written and read across operations:** the three scratch words (`ST-4`).
**Read, never written by this contract's subject:** the table itself — though see `§10`.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-preparation-step-family.md`](CONTRACT-preparation-step-family.md) — the 60–79 band, S-22's first |
| **Sibling** | [`CONTRACT-environmental-element-scaling.md`](CONTRACT-environmental-element-scaling.md) — S-22's second |
| **Uncontracted** | the ranged-weapon recipe page — S-22's fourth, not claimed here |
| **Draws** | the shared generator, through the `Roll*` steps (`ST-7`) |

## 7. State transitions

*recipe id → table lookup → call → the step mutates the scratch record → next id.* There is no
other channel and no return path (`ST-4`).

## 8. Script · resource · event interactions

Recipes are authored data. **The table is the primitive catalogue**: changing how an action computes
damage is changing which ids it names, not changing code — provided a slot already does the wanted
thing.

## 9. Determinism

**Not deterministic** — see `ST-7`. The *selection* is; the *execution* is not.

## 10. Failure paths and edge conditions

- A recipe naming a no-op id is well-formed and silently does nothing (`ST-3`).
- **The table is in `.data`, not `.rdata`, so it is writable at runtime.** A step can be repointed in
  memory without patching any call site.
- Ids 71 and 73 resolve to real steps that no shipped recipe reaches (`ST-6`).

## 11. Observable behaviour

Every damage number in the game is the product of one of these lists. The visible consequence of
getting `ST-4` wrong is damage that is right for one weapon family and wrong for another, because
the same modifier ran before the preparation instead of after it.

## 12. Reproduction formula

Walk the table from the base until the first non-pointer and assert **202** (`ST-1`). Count distinct
targets over those 202 and assert **152**; count slots pointing at `0016D6A0` and assert **42**;
enumerate targets with more than one id and assert **seven**, and that `42 + 160 = 202` and
`1 + 151 = 152` close (`ST-2`, `ST-3`). Read `0016D6A0`'s first three bytes and assert `c2 00 00`
(`ST-3`). Assert `stepTable[113] == stepTable[125]` (`ST-5`).

## 13. Runtime validation

**None.** No experiment executes this dispatch. S-22's runtime cell is not addressed by this
contract. *Stated rather than left blank so a CONTRACT READY header is not read as evidence of
execution.*

## 14. Unresolved

- **The interpreter that walks a recipe is not read**, so how a list is terminated, whether ids may
  repeat, and what a second finalize does are all open (`ST-5`).
- What 125 of the 152 targets do. The page records 35 with recovered `BattleFormula_*` names and the
  rest still `FUN_*`.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `ST-1` — 202, over-determined | the table walked from its base until the first non-pointer, and slot 202's bytes read as `3F80000000060303` | 1 |
| `ST-2` — 152 distinct, seven multi-id | both counted over the 202 slots and the seven enumerated with their ids; **the control is the arithmetic: the nine-slot surplus closes only at seven** | 1 |
| `ST-3` — 42 no-ops, one body | the count taken over the table and `0016D6A0`'s first three bytes read as `c2 00 00` | 1 |
| `ST-5` — one finalize, two ids | `stepTable[113]` and `stepTable[125]` compared directly | 1 |
| `ST-4`, `ST-6`, `ST-7` | [the step-table page](Step-Table/combat-formula-step-table.md) §§2, 5–6, falsified twice on 2026-09-02 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `ST-1` through `ST-7`. **`ST-4` is the one that
decides whether the port is even structurally right**: giving steps arguments and return values is
the natural design and it removes the property the recipes rely on. **`ST-2` is the one that bites a
data-driven port** — treating an id as a behaviour makes six ids alias wrongly. **`ST-3` is the one
that looks like corrupt data and is not.**

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **CombatFormula — internal.** The table, the steps and the scratch record are this category's own.
- **RNG_Random_Selection — SERVICE, and `ST-7` is the statement.** The generator the `Roll*` steps
  draw belongs to that layer; **this contract asserts only THAT those steps draw it and what follows
  for reproducibility**, and nothing about the generator.
- **Every other layer reached is MECHANICAL**, through the two cited steps' own callees. *Only two
  step bodies are cited by address — the finalize and one preparation step — because those are the
  two `ST-5` and `ST-2` name; the other 150 targets are counted, not read, and are deliberately not
  cited.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun.

## 17. Related

- [The combat formula step table](Step-Table/combat-formula-step-table.md) — the mechanism
- [Contract — the preparation step family](CONTRACT-preparation-step-family.md) — the 60–79 band
- [Contract — environmental element scaling](CONTRACT-environmental-element-scaling.md) — S-22's second

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** ST-1 to ST-4 and ST-7 became checks that fail if the shipping image says otherwise, with the table decoded from its
own bytes. Script: `Tools/analysis-kit/gfz-scripts/falsify_step_table.py`, output `falsify_step_table.out`, image
`73461d08…`, 0 BROKEN. ST-5 is a consequence of ST-2's row, and ST-6 is carried from the page.

| # | Clause attacked | Result |
|---|---|---|
| F0 | ST-1 | **survives**: 202 `.text` pointers from `01EFA5C0`, none null; slot 202 is `3F80000000060303` |
| F1 | ST-2 / ST-3 | **survives**: 152 distinct targets, 42 slots on `0016D6A0`, and exactly the seven multi-id targets with the listed ids |
| F2 | ST-3 | **survives**: `0016D6A0` is `c2 00 00` |
| F3 | ST-4 | **survives**: all 16 distinct targets in the 60-79 band write `02AEE054`/`58`/`5C`, and the finalize `0038D280` reads all three |
| F4 | ST-7 | **survives**: all eight `Roll*` steps reach a generator entry within two call levels |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names the three edges.*

**RNG_Random_Selection — SERVICE (3 edges).** Three of the multi-id step targets of `ST-2` call `RNG_MT19937_NextU32_Thunk` (`00379CD0`): `00389670` (ids 40, 45 and 46), `00389F80` (ids 60 and 63) and `BattleFormula_PrepareStrengthAttackVsDefense` (`0038AAF0`, ids 65 and 76). Each draws from the gameplay Mersenne Twister, so whichever id reaches one of these targets advances the shared stream the same way; that is `ST-7`'s reproducibility statement, and the generator itself is that layer's.
