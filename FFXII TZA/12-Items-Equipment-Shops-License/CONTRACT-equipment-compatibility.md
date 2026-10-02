---
contract: Decide whether a piece of equipment may go in a slot — the partner byte, the forbidden mask, the licence
category: 12-Items-Equipment-Shops-License
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md
entries: ["002F7EC0", "00317930", "00317B20", "00323C60", "002F9F20", "002FABD0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — the compatibility function and the eligibility chain disassembled in full and
    their record operands traced to the argument each came from, the compatibility function's call
    sites censused image-wide and **each site's argument order read at its own instructions**, the
    licence checker read to both of its returns, and the two 16-byte range constants dumped from the
    image through a section-aware offset. **This records checks performed on that date, not the
    method of the original derivation**, which is on the item-id page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-equipment-compat-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — equipment compatibility

> **Authored 2026-09-22 by FABLE.** S-29's binding gap is *"item counts by class; equipment
> compatibility uncontracted"* — its one contract,
> [`CONTRACT-inventory-class-storage.md`](CONTRACT-inventory-class-storage.md), covers how many of an
> item the party holds. **This takes equipment compatibility and candidate eligibility.**
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is eight
> such invariants — and **EQ-2 and EQ-8 are statements about the relationship between two operations
> that neither can make alone.**
>
> **The whole chain past `0031795E` was unread**: nothing in the database cited `00317A18`,
> `00317A2C`, `00317A7F`, `00317A89`, `00317AD3`, `00317AD6` or `00317ADE` before this document.

## 1. Purpose

Decide whether a given piece of equipment is allowed in a given slot on a given character — and
whether the thing in the other hand permits it.

## 2. Interface

| | body | size |
|---|---|---:|
| the standalone partner test | `Equipment_CheckPrimarySecondaryDefinitionCompatibility` (`002F7EC0`) | 212 B |
| **the eligibility chain** | `Equipment_CheckItemEligibleForSlot` (`00317930`) | **493 B** |
| its by-stats-index wrapper | `Equipment_CheckItemEligibleForSlotByStatsIndex` (`00317B20`) | 70 B |
| the licence gate | `BattleStats_HasRequiredLicenseForEquipment` (`00323C60`) | 172 B |
| the recommender | `Equipment_BuildRecommendedLoadoutForMappedStats` (`002F9F20`) | 435 B |
| id classification | `ItemDefinition_ClassifyEncodedItemCategory` (`002FABD0`) | — |

## 3. Types

```
item id   u16      bits 15..12 category, bits 11..0 index; 0xFFFF = no item

equipment definition record   base = resolve(header[+0x0C]) + (id - 0x1000) * header[+0x08]
  +0x07  u8   PACKED (EQ-3):  bits 7..5 = the slot 0..4
                              bit  4    = licence-exempt
  +0x09  i8   this item's EQUIPMENT CLASS
  +0x11  i8   the class this item REQUIRES OF ITS PARTNER (18 = shield, 23..26 = ammunition, -1 = none)

BattleStatsRecord
  +0x04  u8   this record's own index -- into 02EBF190's array AND into 02EBF130's class table
  +0x05  u8   the kind selector; NON-ZERO bypasses every equipment rule (EQ-6)

character class row   02EBF130, indexed by stats[+4]
  +0x00  u32  a FORBIDDEN-equipment-class bitmask (EQ-5)

authored search bounds        00D0F9C0  lo[4]      00D0F9D0  hi[4]     (EQ-4)
per-slot short-circuit ids    00D107E8  1000 FFFF FFFF FFFF FFFF
```

## 4. Preconditions · postconditions · invariants

### The eight cross-operation invariants

**EQ-1 — The test is ASYMMETRIC, and the function's parameter names are inverted relative to every
call site in the image.** `002F7EC0` computes

```asm
002F7F70  movzx ecx, byte ptr [rcx + 9]     ; arg1's record, +0x09
002F7F76  cmp   byte ptr [rbx + 0x11], cl   ; arg2's record, +0x11
```

— that is `record(arg2)[+0x11] == record(arg1)[+0x09]`. It has **2 call sites in 1 function**, and at
both the argument order is the opposite of the names: `002FA013` passes `ecx` = the slot-**1**
candidate and `edx` = `out[0]`; `002FA069` passes `ecx` = `out[1]` and `edx` = `out[0]`. **So arg1 is
the off-hand and arg2 is the main hand**, and the rule performed is *the main hand's required-partner
class equals the off-hand's own class* — which is the only reading that agrees with the field
meanings. *A reimplementation that honours the signature reverses an asymmetric test, and reversing
it is not a no-op because the two sides read different offsets.*

> **Confirmed independently, and this is why it can be asserted.** The same comparison is inlined in
> the eligibility chain at `00317A7B`/`00317A7F`, where the two records are unambiguous — `rcx` is
> resolved from `word [r15]`, the main hand, and `rdi` is the candidate. Both sites take `+0x11` from
> the main hand and `+0x09` from the candidate. *Two sites, one direction.*

**EQ-2 — There are TWO implementations of that rule and they are NOT the same predicate.** The
inlined copy **exempts shields** — `00317A2C cmp byte ptr [rdi + 9], 0x12` / `je` skips the partner
test entirely — and the standalone `002F7EC0` does not. Both exempt an empty main hand; only the
standalone also returns **1** when the *candidate* is `0xFFFF` (`002F7ED5`). ~~*The consequence is an
ordering: the recommender's inner loop admits any shield for slot 1 whatever the main hand is, and
the slot-0 epilogue then calls the stricter `002F7EC0` and drops it (`002FA077`) when the main hand's
`+0x11` is not `0x12`. **Two guards over one rule, the second cleaning up after the first**, and
neither function can state that on its own.*~~ **The consequence was stated out of order** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 323](../_index/candidates/s29-opus-replay-equipment-eligibility/README.md), which executed it; `002F9F20` re-read whole.)*
- **The slot-1 loop applies the stricter rule to every candidate.** A candidate the inlined chain admits, a shield
  included, is re-tested with `002F7EC0` against `out[0]` (`002FA008`–`002FA01A`) before any compare. So a shield
  the main hand does not accept is refused there, inside the loop.
- **The slot-0 epilogue does not clean up after that loop, because it runs first.** It runs after slot 0's walk and
  **before** slot 1's (`002FA056`–`002FA077`, with `esi == 0`). It tests `out[1]` against the new main hand.
  `out[1]` is the off-hand carried in from `stats + 0x52` (`002F9F94`–`002F9F99`), not one the inner loop admitted,
  and it is dropped to `0xFFFF` when the new main hand refuses it.

*So there are still two guards over one rule, but they guard different things: the epilogue validates the
existing off-hand against the recommended weapon, and the slot-1 loop validates each new candidate.*

**EQ-3 — Byte `+0x07` of the definition record carries TWO unrelated things.** The **top three bits
are the slot** — `00317A18 movzx eax, byte ptr [rdi + 7]` / `shr eax, 5` / `cmp eax, esi` / `jne`
reject — and **bit 4 is a licence exemption**: `00323CDF test byte ptr [rcx + 7], 0x10` / `jne`
returns "has licence" without consulting the board. *Slot membership is authored per item, not
derived from its id.*

**EQ-4 — The four authored search ranges OVERLAP, and slot 1's upper bound is not what the page
says.** `00D0F9C0` and `00D0F9D0` are two 16-byte constants, a `lo[4]` and a `hi[4]`, loaded together
at `002F9F37`/`002F9F42` and indexed by `slot*4`:

| slot | lo | hi (exclusive) | ids |
|---:|---|---|---:|
| 0 | `0x1000` | `0x10C8` | 200 |
| **1** | `0x10C8` | **`0x11A4`** | **220** |
| 2 | `0x10DC` | `0x1118` | 60 |
| 3 | `0x1118` | `0x1154` | 60 |

**Slot 1's range contains slots 2 and 3 entirely.** The item-id page's §3 ~~lists~~ listed slot 1 as
`0x10C8`..`0x10DB` — the value that would make the four ranges contiguous — *(answered: corrected there 2026-09-22 to `0x10C8`..`0x11A3`; see item-id-encoding-and-equipment-compatibility.md §3, the `002F9F20` row; 2026-10-02, OPUS)* while **its own text two
clauses later speaks of ids `0x1184`..`0x11A3` being reached during the walk**, which is only
possible under the measured bound. *So the ranges are coarse search bounds and not slot definitions;
the slot filter is EQ-3, and that is why they are allowed to overlap.*

**EQ-5 — The character's equipment-class mask is a FORBIDDEN mask, not an allowed one.**
`00317AD1 mov eax, dword ptr [rbx]` reads the class row at `02EBF130` selected by `stats[+4]`, and
`00317AD3 bt eax, ecx` / `00317AD6 jb` **rejects when the bit for the item's class is SET**. *The
polarity is the whole content of the check and it is the opposite of the natural reading.*

**EQ-6 — `stats[+0x05]` non-zero bypasses the class mask AND the licence, in two functions
independently.** `00317A89`/`00317A8F` returns eligible before either test; `00323C8F`/`00323C93`
returns "has licence" before the board lookup. The licence gate additionally exempts
**`stats[+0x04] > 6`** (`00323C97`). *So equipment restriction is a player-character-only system, and
`stats[+0x05]` is the same selector byte that
[stat derivation](../08-Combat-Formula/CONTRACT-stat-derivation.md),
[enmity](../09-Combat-AI-And-Gambits/CONTRACT-enmity.md) and
[the trigger points](../03-World-Area-Field/CONTRACT-authored-trigger-points.md) branch on.*

**EQ-7 — One item id is validated under TWO different id classes.** The eligibility chain passes
class **6** (`0031799A lea ecx, [r8 + 6]`, `r8` zeroed at `0031798B`); the licence gate passes class
**1** (`00323C72 lea ecx, [r8 + 1]`) — both to the same validator `BattleEncodedId_IsValidForClass`,
for the same id. *(That validator's own address is deliberately not cited: it is a shared service
whose callers are the rest of the engine, and naming it imports all of them for a claim carried
entirely by the two call sites above.)* *Two classes over one id space, and a failure of the class-1 test is
the one path in the licence gate that returns **0**; every other early exit returns 1.*

**EQ-8 — The recommender decides the main hand first, forces it non-empty, and invalidates the
off-hand before searching for one.** The slot-0 epilogue runs while `esi` is still 0
(`002FA056 test esi, esi` / `jne`): an empty `out[0]` becomes `0x1000` (`002FA05F`), then
`002F7EC0(out[1], out[0])` runs and a failure sets `out[1] = 0xFFFF` (`002FA077`). Only then does
`esi` become 1 and slot 1's own walk begin, re-testing every candidate against `out[0]`. *The main
hand is never revisited.* **And the builder copies FIVE equipment words `+0x50`..`+0x58`
(`002F9F8D`–`002F9FB4`) but optimises only FOUR** (`002FA08F cmp esi, 4`) — `out[4]` is passed
through untouched.

## 5. State

**Owned:** nothing. Every body here is a predicate except the recommender, which writes only the
caller's five-word `out`. **Read, never written:** the equipment definition table behind `02EBF0F8`,
the class table behind `02EBF130`, the stats record, and the two authored constants.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-inventory-class-storage.md`](CONTRACT-inventory-class-storage.md) — S-29's contracted half |
| **Calls** | [`CONTRACT-license-check.md`](CONTRACT-license-check.md) — EQ-6's board lookup, reached only when every exemption fails |
| **Shares the selector** | stat derivation, enmity and the trigger points, on `stats[+0x05]` (EQ-6) |
| **Depends on** | [the five-slot count](equipment-slots-and-the-single-stat-rebuild.md) — S-24's page, which established the five slots and the `00D107E8` table; **not re-derived here** |

## 7. State transitions

None; this subsystem holds no state. Per candidate: *slot from `+0x07` → (slot 1: shield, or empty
main hand, or partner-class match) → `stats[+0x05]` bypass → class not forbidden → licence.* The
recommender's transition is EQ-8's slot order.

## 8. Script · resource · event interactions

The definition table, the class table and both 16-byte range constants are authored. The slot and the
licence exemption are authored **per item**, in one byte (EQ-3).

## 9. Determinism

Deterministic. No generator is drawn.

## 10. Failure paths and edge conditions

- A slot above 4 rejects (`0031794D`); the compare is unsigned after a sign-extend, so negatives
  reject too — established on [S-24's page](equipment-slots-and-the-single-stat-rebuild.md).
- An id equal to the slot's short-circuit entry at `00D107E8` is eligible with **no further checks**
  (`0031795A`), which is how `0x1000` stays legal in slot 0 and `0xFFFF` in slots 1–4.
- `0xFFFF` in any other slot rejects (`0031797E`).
- A definition table that fails to resolve leaves the record pointer **zero** and the chain reads
  `[0 + 7]` (`00317A15`/`00317A18`); this contract does not establish that it can happen.

## 11. Observable behaviour

The game will not let you put a shield on when you are holding a two-handed weapon, will not let a
character equip what their licence board has not opened, and its "optimise" command fills the weapon
hand first and then throws away an off-hand that no longer fits.

## 12. Reproduction formula

Call `002F7EC0(a, b)` with `record(b)[+0x11] == record(a)[+0x09]` and assert 1, then swap the
arguments and assert the result **changes** — an implementation that made the test symmetric passes
both (EQ-1). ~~Offer a shield for slot 1 with a main hand whose `+0x11` is not `0x12` and assert the inner loop accepts it and the epilogue drops it to `0xFFFF` (EQ-2).~~ Offer a shield for slot 1 with a main hand whose `+0x11` is not `0x12` and assert the slot-1
loop **refuses** it at its `002F7EC0` re-test (`002FA013`). Then carry such a shield in as the off-hand (`stats + 0x52`) and
assert the slot-0 epilogue drops it to `0xFFFF` (`002FA077`) before slot 1's walk (EQ-2; the §4 correction of 2026-09-25,
propagated here 2026-09-29 by OPUS falsification pass 1). Dump `00D0F9D0` and assert
`hi[1] == 0x11A4` (EQ-4). Set the class row's bit for an item's own class and assert the item is
**rejected** (EQ-5). Set `stats[+0x05]` non-zero and assert both the mask and the licence are skipped
(EQ-6).

## 13. Runtime validation

~~**None.** No experiment executes these bodies. S-29's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*~~ **Superseded
2026-09-25**: [OPUS block 323](../_index/candidates/s29-opus-replay-equipment-eligibility/README.md) executed EQ-1 to EQ-8 and the recommender as shipped code. The evidence class is native
replay, not live.

## 14. Unresolved

- ~~What the ids `0x1184`..`0x11A3` are, which the recommender compares under **mode 0** rather than
  their slot (`002FA021`–`002FA033`; `r14d` is zeroed at `002F9FEE`, immediately before the inner
  loop head, so the mode really is 0 and not `slot*4`).~~ **ANSWERED by execution** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 323](../_index/candidates/s29-opus-replay-equipment-eligibility/README.md), which executed it; `002F9F20` re-read whole.)*. They are the range
  the weapon comparator searches for a weapon's **partner** when the weapon's `+0x11` is 23–26. Scoring such a
  weapon, the comparator walks `0x1184`–`0x11A3` through the slot-1 wrapper and compares the matching partner under
  mode 0. The recommender forces mode 0 for the same range too (`002FA021`–`002FA033`). *That
  23–26 means ammunition is §3's label, not something this run measured.*
- Why slot 1's search range covers slots 2 and 3 when EQ-3 already excludes them.
- What `out[4]` is for, given the recommender never optimises it (EQ-8).
- Whether the class-6 and class-1 validations of EQ-7 can disagree for a real id. **PARTIAL** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 323](../_index/candidates/s29-opus-replay-equipment-eligibility/README.md), which executed it; `002F9F20` re-read whole.)*: for an id
  of the `0x1xxx` family, class 1 re-dispatches through the family-code lookup to class 6, the same range test. So
  the two cannot disagree there. OPUS's run showed class 1 answering as the family's own class for every family
  0–14. *Whether any real id reaches a validator with a mismatched family is not established.*

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| EQ-1 — the expression and the inverted names | `002F7F70`/`002F7F76` read at their instructions, then **both call sites' argument registers traced at `002FA013` and `002FA069`**, with the inlined copy at `00317A7B`/`00317A7F` as the **independent control** — a second site whose operands are unambiguous | 1 |
| EQ-2 — the shield exemption and the epilogue drop | `00317A2C` against `002F7EC0`'s own early-outs; `002FA069`–`002FA077` read in order | 1 |
| EQ-3 — the packed byte | `00317A18`/`00317A1C`/`00317A1F` and `00323CDF` | 1 |
| EQ-4 — the four ranges | both 16-byte constants dumped from the image through a **section-aware** offset, and the load sites `002F9F37`/`002F9F42` and index `002F9FE0`/`002F9FE5` read | 1 |
| EQ-5 — the mask polarity | `00317AD1`/`00317AD3`/`00317AD6`, the `jb` taken to the zero return at `00317AE7` | 1 |
| EQ-6 — the two bypasses | `00317A89`/`00317A8F` and `00323C8F`/`00323C93`/`00323C97`, each traced to a `mov eax, 1` | 1 |
| EQ-7 — the two classes | `0031799A` and `00323C72` read at their instructions, each `lea` resolved against its zeroed base register, and both confirmed to target the same validator entry | 1 |
| EQ-8 — the slot order | `002FA056`–`002FA07F` read as one sequence; the five copies at `002F9F8D`–`002F9FB4` against `002FA08F` | 1 |
| the id encoding and the `id - 0x1000` index | [the item-id page](item-id-encoding-and-equipment-compatibility.md) §2, falsified 2026-09-02 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on EQ-1 through EQ-8. **EQ-1 and EQ-5 are the two
that a port gets wrong while looking correct**: the partner test reads as "do these two match" and is
not symmetric, and the class mask reads as a permission and is a prohibition. Either error produces a
game that equips almost everything correctly and is wrong at exactly the boundary the data was
authored to control.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Items_Equipment_Shops_License — internal.** Every body named here is this category's own.
- **CombatFormula — SERVICE.** The stats record and its `+0x04`/`+0x05` bytes are that layer's, and
  EQ-6 is the statement about them. *The record's own field map is not re-derived here.*
- **CoreRuntimeScheduling — SERVICE.** `ImageAddress_ResolveRuntimePointer` and the encoded-id
  validator are that layer's; EQ-7 is about which class each caller passes, not about the validator.
- **Gameplay — MECHANICAL.** Reached as callees of the eligibility chain: the shared encoded-id
  validator, and the owned-count query the by-stats-index wrapper switches on. **This contract states
  which class each call passes (EQ-7) and that the wrapper always enables the owned test — nothing
  about either callee's behaviour**, and neither address is cited.
- **Every other layer reached is MECHANICAL**, through these bodies' own callees. *Their addresses
  are deliberately not cited: each is a hub, and naming one imports its whole edge set.*

## 17. Related

- [Item id encoding and equipment compatibility](item-id-encoding-and-equipment-compatibility.md) — the mechanism
- [Contract — inventory class storage](CONTRACT-inventory-class-storage.md) — S-29's contracted half
- [Contract — the license check](CONTRACT-license-check.md) — EQ-6's board lookup
- [Equipment slots and the single stat rebuild](equipment-slots-and-the-single-stat-rebuild.md) — the five-slot count, S-24's

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **CombatFormula - SERVICE (1 edge).** `002F9F20` reaches bodies filed to combat formula: `00320AB0` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - SERVICE (3 edges).** `00317930`, `00323C60` reach bodies filed to Gameplay: `00309EC0` (Combat), `00322C50` (Combat) - shared machinery across the layer boundary, no shared ownership.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives; §12 caught up with the §4 correction

**Attack.** EQ-1 to EQ-8, §2's sizes and §10's three early exits became checks at their instructions. The call census of
`002F7EC0` is image-wide, and both range constants and the short-circuit table were read through section-aware offsets.
Script: `Tools/analysis-kit/gfz-scripts/falsify_equipment_compat.py`, output `falsify_equipment_compat.out`, image
`73461d08…`, 0 BROKEN. The behaviour was executed by OPUS block 323 and is not repeated.

| # | Clause attacked | Result |
|---|---|---|
| Q0 | §2 | **survives**: 212 / 493 / 70 / 172 / 435 B |
| Q1 | EQ-1 | **survives**: arg2 in `rbx` (`movzx ebx, dx`) supplies `+0x11`, and arg1 supplies `+0x09`; exactly 2 call sites (`002FA013`, `002FA069`) with the inverted order; the inline copy takes `+0x11` from `word [r15]`'s record |
| Q2 | EQ-2 | **survives, as corrected on 2026-09-25**: the shield skip at `00317A30`; both empty-main-hand exits; the standalone's empty-candidate exit; every slot-1 candidate re-tested at `002FA013`; the off-hand copied from `+0x52` |
| Q3 | EQ-3 | **survives**: `shr eax, 5` slot test; `test byte [rcx+7], 0x10` → return 1 |
| Q4 | EQ-4 | **survives**: lo `{1000, 10C8, 10DC, 1118}`, hi `{10C8, 11A4, 1118, 1154}`; slot 1 contains slots 2 and 3 |
| Q5 | EQ-5 | **survives**: `bt` / `jb` to `xor eax, eax` |
| Q6 | EQ-6 | **survives**: both `+5` bypasses and the `+4 > 6` exemption reach `mov eax, 1` |
| Q7 | EQ-7 | **survives**: classes 6 and 1 to one validator; the failed class-1 test is the one exit that returns 0; every other early exit is `00323CFC`, and the board lookup is the tail |
| Q8 | EQ-8 | **survives**: the epilogue at `esi == 0`, `0x1000` forced, `0xFFFF` dropped; five copies, loop bound 4 |
| Q9 | §10 | **survives**: slot > 4 rejects; the short-circuit table `{1000, FFFF ×4}`; `0xFFFF` rejects |

**Propagated:** §12's EQ-2 formula still asserted the pre-2026-09-25 order ("the inner loop accepts it and the epilogue
drops it"). It now asserts the slot-1 loop's refusal and the epilogue's drop of a carried-in off-hand. There is no new
contradiction: the finding is OPUS block 323's, and §4 already carried it.
