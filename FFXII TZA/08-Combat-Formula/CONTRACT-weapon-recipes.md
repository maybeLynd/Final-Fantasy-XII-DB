---
contract: Resolve an action's recipe id into two sentinel-separated calculator lists, and run the second
category: 08-Combat-Formula
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md
entries: ["00385F60"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's figures **read from the
    tables' own bytes rather than carried** — the recipe pointer table walked to the first
    non-pointer, two recipes' blobs decoded as `i32` runs, and the sentinel positions taken from the
    decoded values. **This records checks performed on that date, not the method of the original
    derivation**, which is on the recipe page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-weapon-recipes-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — weapon recipes

> **Authored 2026-09-22 by FABLE.** S-22's binding gap is *"calculator slots 60-79 only, of 4
> pages"*. **This takes the fourth, so all four of S-22's pages now carry a contract.**
>
> Written against FRONTIER's adequacy test. **`RW-2` is why this is not an operation-scoped
> contract**: one authored blob serves two different consumers, and which list a consumer reads is
> the whole of what separates a preview number from a committed one.

## 1. Purpose

Decide which calculators an action runs, and which of them only ever produce a preview.

## 2. Interface

`BattleFormula_ResolveTargetResult` (`00385F60`), **2,302 B**. The recipe id is
`ActionDefinition + 0x08`, in `0..108`, resolved through the pointer table at `0x01EF96C0`.
**Id 0 is not a recipe of its own. It means "use the weapon's recipe"** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 316, which executed it; `0038617E`–`003863E6` re-read.)*. For `byte [row + 8] == 0`
(`0038618B`) the body reads the attacker's equipped item word `[stats + 0x50]` (`003861A7`). If the item word is below `0x1000` plus
the equipment table's count, it takes the recipe from byte `+0x19` of that item's row (`003861E2`–`003861FD`). No
lower bound is tested. The body returns:

| case | return |
|---|---|
| the action row's id is `>= 109` | `-1` (`00386182`/`00386212`) |
| the equipped item is at or above `0x1000` + the count | `-2` (`003861B4`/`00386242`) |
| the weapon row names recipe 0 | `-2` (`00386201`–`00386207`) |
| the weapon row names a recipe `>= 109` | `-1` (`0038620D`–`00386210`) |

**So the ranged-weapon recipes 25 and 26 are normally reached through the weapon, not named by the action.**

## 3. Types

```
0x01EF96C0   void*[109]     the recipe pointer table, ids 0..108
recipe blob  i32[...]       two lists, each terminated by -1:
                              [ preview slots ]  -1  [ committed slots ]  -1
slot numbers index the step table at 0x01EFA5C0 -- see CONTRACT-formula-step-table.md
```

## 4. Preconditions · postconditions · invariants

### The five cross-operation invariants

**RW-1 — 109 recipes, and the extent is OVER-DETERMINED rather than asserted.** Every pointer for
ids `0..108` lands in `.data`; the next qword is `000000B4FFFFFFFF`, **not an address**. *So the
table's end is visible in its own bytes, exactly as the step table's 202 is — the two catalogues
this category rests on are both bounded by their data rather than by a claim.*

**RW-2 — One blob, TWO lists, and the committed resolver SKIPS the first.** Each recipe is a run of
signed `i32` slot numbers terminated by `-1`, then a second run terminated by `-1`. Recipe 25
decodes as `5 6 22 33 34 35 42 | -1 | 29 66 96 97 98 99 125 165 171 176 182 | -1`. ~~**The first list~~
~~is preview-side and the second is the committed result**~~ **The first list is the outcome decision, run when the action executes and memoised into the result, and the second is the committed result** *(corrected 2026-10-02, OPUS: §14's correction; ranged-weapon-recipes.md §2)*, and the committed path runs only the
second.

> ***The sentinel is the semantics.*** *A reimplementation that reads one list, or that concatenates
> them, produces a preview that matches the committed result — which is precisely the thing the two
> lists exist to make differ.*

**The committed list can be cut short, or skipped entirely** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 316, which executed it; `0038617E`–`003863E6` re-read.)*. The stop flag is `02AEDFB8`.
- **Cut short.** After each committed step the loop tests the flag (`003863D7 cmp dword [02AEDFB8], 1` / `je`) and
  ends the recipe when that step set it. The rip-relative census of the flag finds 53 stores in 44 functions and
  24 reads (`tools/ripscan.py`, rip-relative forms only). Most of the stores are step functions writing `1`,
  among them the avoid / guard / parry roll. OPUS's run stopped recipe 6 `[3, 4, 61, 90, 91, 112, 180]` after slot 4,
  and recipe 2 `[20, 30, 32, 40, 181]` after slot 40.
- **Skipped.** Before the loop, `00386249`–`00386278` re-stores the flag. For the seven recipe ids in the bitmask
  `0x4000140000004E` (ids 1, 2, 3, 6, 34, 36, 54) it keeps the value it already holds. For any other recipe it
  sets the flag to `1` when the prepared context carries any of bits `0x80000003` (`0038626C`–`00386274`). When
  the third argument's record has `+0x05 == 0`, kind `+0x04` in `0x1B`–`0x27` and `+0x48 == 0`, the body sets the flag
  and `02AEDFBC` and jumps past the loop (`0038627E`–`003862A9`). Otherwise `003862AE` skips the whole loop when the flag is non-zero.

*So "the committed path runs the second list" names which list, not how much of it. A reimplementation that
always runs every slot changes the outcome of every action that a step stops.* **And the preview list is not a subset of the committed one**: recipe
> 25's preview names slots 5, 6, 22, 33, 34 that the committed list never names, so the two are
> different programs over the same catalogue, not a short form and a long form.

**RW-3 — A recipe is a PROGRAM over the step table, so its meaning is that table's.** The numbers
index `0x01EFA5C0`. *A recipe naming a no-op slot is well-formed and does nothing, and an id is not
an identity — both are the step-table contract's `ST-3` and `ST-2`, and they apply to every recipe
without being visible in one.*

**RW-4 — Recipes 25 and 26 differ in exactly THREE slots and are otherwise identical; the executable
itself pairs the two families.** Bow against crossbow:

| | preview | committed |
|---|---|---|
| **25** bow | `5 6 22 33 34` **`35`** **`42`** | `29` **`66`** `96 97 98 99 125 165 171 176 182` |
| **26** crossbow | `5 6 22 33 34` **`36`** **`43`** | `29` **`65`** `96 97 98 99 125 165 171 176 182` |

*The three differences are the severe-weather scale, the outcome resolver and the preparation step —
one per concern, in the same positions.* **So a weapon family is not a separate formula; it is the
same program with three substitutions.**

**RW-5 — The severe-weather accuracy gate is a DIFFERENT gate from the element bypass, and confusing
them is the available mistake.** The `35`/`36` scales apply only when merged context **bit 2** is
clear — `AccuracyBoost` — *and* the weather gameplay class is `2`. The element bypass uses **bit
16**, `Weatherproof`. *So the Agate Ring does not help a bow in a storm, and the two bits are not
interchangeable even though both read as "weather protection".*

## 5. State

**Owned:** nothing. **Read:** the recipe pointer table, the blobs, and the step table.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-formula-step-table.md`](CONTRACT-formula-step-table.md) — the catalogue `RW-3` indexes, S-22's third |
| **Sibling** | [`CONTRACT-preparation-step-family.md`](CONTRACT-preparation-step-family.md) — slots 65 and 66, the `RW-4` substitution |
| **Sibling** | [`CONTRACT-environmental-element-scaling.md`](CONTRACT-environmental-element-scaling.md) — the bit-16 gate `RW-5` distinguishes |

## 7. State transitions

~~*action → recipe id → pointer table → blob → scan to the first `-1` for preview, past it for
committed → run that list against the step table.*~~
*action → recipe id (id 0: the equipped weapon row's `+0x19`) → pointer table → blob → scan to the first `-1` for
preview, past it for committed → stop flag set? skip : run that list against the step table, stopping after the
first step that sets the flag.* *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 316, which executed it; `0038617E`–`003863E6` re-read.)*

## 8. Script · resource · event interactions

Recipes and the ids that name them are authored data. **Nothing here is code-selected**: changing
which calculators a weapon family runs is changing three numbers.

## 9. Determinism

**Selection is deterministic; execution is not** — the committed lists name `Roll*` steps, which is
the step-table contract's `ST-7`.

## 10. Failure paths and edge conditions

- A recipe naming a no-op slot is well-formed and does nothing (`RW-3`).
- The preview and committed lists may name entirely different slots (`RW-2`).
- Bit 2 and bit 16 both look like weather protection and gate different things (`RW-5`).

## 11. Observable behaviour

Why a bow misses in a storm and a crossbow misses differently, and why the damage preview and the
damage dealt are not computed the same way.

## 12. Reproduction formula

Walk the pointer table and assert **109** entries in `.data` with the next qword not a pointer
(`RW-1`). Decode recipe 25 and assert **two** `-1`-terminated runs, and that the preview run names
slots the committed run does not (`RW-2`). Diff recipes 25 and 26 and assert **exactly three**
differing slots (`RW-4`). Set merged bit 2 and assert the severe-weather scale does **not** apply;
set bit 16 and assert it still does (`RW-5`).

## 13. Runtime validation

**None.** No experiment executes this resolver. S-22's runtime cell is not addressed by this
contract. *Stated rather than left blank so a CONTRACT READY header is not read as evidence of
execution.*

## 14. Unresolved

- ~~**Who consumes the preview list.**~~ — **resolved 2026-09-23 (SWE2-CONTRACT): the preview-side
  consumer is `0x3858E7`, a second recipe walker~~ — and it is statically orphaned~~.** *(corrected 2026-10-02, OPUS: `0x3858E7` lies inside `00385680`, reached by `jne` / `je` at `00385893` / `003858A0`, and `00385680` has two callers; see below)* The recipe
  pointer table `0x01EF96C0` has **exactly two** code references in the whole image, and both use a
  route form a rip-census cannot see: `lea reg, [rip→0x120000]` materialises the *image base as a
  value*, and the table is indexed as `[reg + id*8 + 0x1DD96C0]` — a disp32 holding the table's
  **RVA**, not a next-insn-relative displacement. The two sites are `0x38635D` inside `00385F60`
  (the committed resolver — it counts list 1, then walks `blob + (len1+1)*4` through `len2`,
  executing only the second list, exactly as `RW-2` says) and `0x3859BD` inside **`0x3858E7` —
  which walks `blob[0..len1)`**: the first list, executed through the *same* step table
  (`call [reg + rax*8 + 0x1DDA5C0]` = `0x01EFA5C0`), writing outcome flags into a different result
  record (`[rbx+4]`/`[rbx+8]` bitmasks, `[rbx+0x12]` flag bits). So the preview number is not a
  cheaper or partial evaluation — it is a complete second program run over the same catalogue.
  **The residual:** `0x3858E7` ~~itself is statically orphaned~~ is an interior label of `BattleFormula_EvaluateTargetPreview` `00385680`, reached by `jne` / `je` at `00385893` / `003858A0`, which is why it has *(corrected 2026-10-02, OPUS: checked at those addresses)* — zero `call`/`jmp` edges, zero
  `lea`/immediate materialisations, zero data qword/dword slots (its only image bytes are its own
  `.pdata` record), while `00385F60` is registered in `.rdata` `{rva32,…}` records
  (`0x01D7CD2C`/`3C`/`54`). ~~Who *invokes* the preview walker is a runtime-registration question,~~
  ~~not answerable from the image.~~ The image answers who invokes it: `00385680` is called by `BattleAction_EvaluateTargetPreviews` `00303830` (`00303910`) and by `00303A00` (`00303AD7`), and `00303830` by `BattleUnit_AdvanceStandardActionState` `00304850` (`00304F1D`) and by `00313120` (`003132A6`) — the first list runs when the action executes, as its hit / evade / knockback / combo decision *(corrected 2026-10-02, OPUS: checked by `retool.py callers`; ranged-weapon-recipes.md §2, corrected 2026-09-30)*. **Route-form note:** this idiom — image-base-in-a-register plus an
  RVA disp32 — is a fifth access form outside rip-target/immediate/data-qword/`lea` censuses; it is
  caught only by a raw disp32 byte scan over all of `.text`.
- What the other 107 recipes name. Two are decoded; the rest are authored data this contract does
  not enumerate.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `RW-1` — 109, over-determined | the pointer table walked: ids `0..108` all in `.data`, and the next qword read as `000000B4FFFFFFFF` | 1 |
| `RW-2` — two `-1`-terminated lists | recipe 25's blob at `0x01EF9E60` decoded as `i32` and the two sentinels located by value | 1 |
| `RW-4` — exactly three differences | recipes 25 and 26 decoded and compared slot by slot | 1 |
| `RW-3`, `RW-5` and the slot identities | [the recipe page](Recipe-System/ranged-weapon-recipes.md) §2, re-verified 2026-09-02 and independently falsified 2026-09-07 | 1 |
| the preview list is consumed by `0x3858E7`, which walks `blob[0..len1)` through the same step table | whole-image census of `0x01EF96C0` across rip-target, immediate, data-qword and raw disp32-RVA route forms: exactly two code sites (`0x3859BD`, `0x38635D`); `0x3858E7` decoded — first-list walk `[r15+rdi*4]`, bound `ecx` counted to the first `-1` at `0x3859D0`, step calls `[r12+rax*8+0x1DDA5C0]`; zero registration slots for `0x3858E7` itself | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `RW-1` through `RW-5`. **`RW-2` is the one a
port collapses**: reading one list, or concatenating them, is the obvious simplification and it
makes the preview agree with the commit. **`RW-5` is the one a port merges** — two weather bits that
sound alike gate different things.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **CombatFormula — internal.** The resolver, the recipe tables and the slot lists are this
  category's own.
- **Weather — SERVICE, and `RW-5` is the statement.** The gameplay weather class the severe-weather
  scale tests belongs to that layer; **this contract asserts only WHICH class value and WHICH merged
  bit the gate reads**, and nothing about how weather is decided.
- **Items_Equipment_Shops_License — MECHANICAL.** The augment namespace that names bit 2
  `AccuracyBoost` and bit 16 `Weatherproof` is that layer's; the bits are cited by **number** here,
  with the names carried from the page, so nothing rests on the namespace being read.
- **CombatAction — CLIENT, and it is the caller side.** Three bodies in that layer call the
  resolver. *They are cited by no address here: this contract asserts what the resolver does with
  a recipe id, not who supplies one, and which caller asks for a preview rather than a commit is
  §14's open question.*
- **Every other layer reached is MECHANICAL**, through the resolver's own callees. *Only the
  resolver is cited by address; the step bodies the recipes name are the step-table contract's and
  are deliberately not re-cited here.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun. *"Weather" would otherwise be cleared by the word alone.*

## 17. Related

- [Ranged weapon recipes](Recipe-System/ranged-weapon-recipes.md) — the mechanism
- [Contract — the formula step table](CONTRACT-formula-step-table.md) — the catalogue the slots index
- [Contract — the preparation step family](CONTRACT-preparation-step-family.md) — slots 65 and 66

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** RW-1, RW-2 and RW-4 became checks against the table and recipes decoded from their own bytes, plus the stop-flag
sites. Script: `Tools/analysis-kit/gfz-scripts/falsify_weapon_recipes.py`, output `falsify_weapon_recipes.out`, image
`73461d08…`, 0 BROKEN. RW-5's bit semantics are carried from the page.

| # | Clause attacked | Result |
|---|---|---|
| W0 | §2 size | **survives**: 2,302 B |
| W1 | RW-1 | **survives**: all 109 pointers land in `.data`; the next qword is `000000B4FFFFFFFF` |
| W2 | RW-2 / RW-4 | **survives**: recipes 25 and 26 decode as quoted and differ in exactly three slots; 25's preview slots 5, 6, 22, 33 and 34 are absent from its committed list; recipes 2 and 6's committed lists are as quoted |
| W3 | RW-2's stop flag and skip mask | **survives**: `cmp [02AEDFB8], 1` at `003863D7`; `movabs rcx, 0x4000140000004e` decodes to ids 1, 2, 3, 6, 34, 36 and 54 |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names the callers it left unaddressed.*

**CombatAction — CLIENT (3 edges).** `Battle_ProcessActionTarget` (`00307300`), `BattleAction_ResolveSpecialSequenceTargets` (`0030EC00`) and `BattleUnit_HandleActorTimelineEvent` (`00319F50`) call `BattleFormula_ResolveTargetResult` (`00385F60`). These are the action layer's three entries that run the committed recipe program for one target: per-target action processing, special-sequence target resolution and the actor timeline's hit event. They supply the recipe id and the target; what the resolver does with the recipe is this contract's.

**Status_Periodic_Terminal — CLIENT (1 edge).** `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) calls `00385F60`. The periodic tick resolves its own results through the same recipe resolver, so a periodic effect runs a recipe program exactly as an attack does.
