---
contract: Scale an action's element by environment, weather and terrain — unless either side is weatherproof
category: 08-Combat-Formula
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md
entries: ["0038B220", "00263E10", "00263E20", "00263DD0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the stage's three early-out tests read at their instructions **with the two
    effect-layer displacements as the control**, and both class getters disassembled and their
    globals resolved. **This records checks performed on that date, not the method of the original
    derivation**, which is on the scaling page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-element-scaling-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — environmental element scaling

> **Authored 2026-09-22 by FABLE.** S-22's binding gap is *"calculator slots 60-79 only, of 4
> pages"*. This takes **weather, terrain and element scaling**; the step table and the ranged-weapon
> recipes remain uncontracted and this document does not claim them.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants — and **three of them are about state this subsystem does not own**, published by
> two other systems this session has contracted.

## 1. Purpose

Multiply an action's elemental effect by where the fight is happening and what the weather is doing —
or skip the whole thing.

## 2. Interface

| | body | size |
|---|---|---:|
| **the stage** | `0038B220` | 1,138 B |
| global environment class | `WorldField_GetGlobalEnvironmentClass` (`00263E10`) | **7 B** |
| MWeather gameplay class | `WorldField_GetMWeatherGameplayClass` (`00263E20`) | **7 B** |
| target-local terrain class | `WorldField_ResolveTargetLocalTerrainClass` (`00263DD0`) | 53 B |

## 3. Types

```
ActionDefinition
  +0x13  u8  element mask — 0x01 Fire, 0x02 Lightning, 0x04 Ice, 0x08 Earth, 0x10 Water, 0x20 Wind

globals consumed, both published by S-11's environment variant
  02099DA8  global environment class
  02099DAC  MWeather gameplay class — ALREADY BANDED by its publisher (WE-3)

scratch
  02AEE054  the canonical formula scratch scale
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**WE-1 — This is the PRE-AFFINITY stage, and it shares its input with the one that follows.** It runs
before `BattleFormula_ApplyActionElementAffinity` (`0038B6A0`), the separate
resistance/weakness/absorb stage, and **both read the same element mask at `ActionDefinition + 0x13`**
(`0038B295` here). *Two stages reading one authored byte for different purposes, in a fixed order —
an implementation that merges them changes which multiplications compose.*

**WE-2 — Three ~~independent~~ inputs, ~~multiplied in sequence~~ tested in sequence** *(corrected 2026-10-02, OPUS: an environment rule and a terrain rule for the same element share one multiply, `0038B3E1`–`0038B424`; the rule table below)*. Global environment class, MWeather
gameplay class and target-local terrain class. *The first two are global; only the third is per
target, so two targets of one action scale differently only through terrain.*

**WE-3 — The MWeather value it consumes was ALREADY BANDED somewhere else, and the boundaries are not
this subsystem's.** `00263E20` is **seven bytes** — it reads `02099DAC` and returns. That global is
published by
[the field environment variant](../03-World-Area-Field/CONTRACT-field-environment-variant.md), whose
EV-5 compresses the 3-bit MWeather preset to `0` / `1` / `2` at the boundary *"greater than 3"*.
**So preset 0 → class 0, presets 1–3 → class 1, presets 4–7 → class 2, and this stage cannot tell
which preset it was.** *A subsystem consuming a band it did not compute cannot widen it; changing the
weather's granularity here is impossible without changing the publisher.*

**WE-4 — The early-out reads the SAME BIT two different ways, depending on the combatant.**

```asm
0038B226  test byte ptr [rdx + 0x6a], 1   ; TARGET — raw mutable layer   (+0x68 + 2)
0038B233  test byte ptr [rdx + 0x7a], 1   ; TARGET — raw derived layer   (+0x78 + 2)
0038B23D  test byte ptr [r8  + 0x1c], 1   ; CASTER — the MERGED bitmap   (+0x1A + 2)
```

**The target is tested on its two raw effect layers; the caster on the merged formula-context
bitmap.** That merge is
[the effect-layer contract's](../10-Status-Periodic-Terminal/CONTRACT-effect-layers.md) L-3, and it is
lossy by construction — so **the caster's test inherits the merge's conflation and the target's does
not.** *Any bit the merge folds together is folded for one side of this test and kept apart for the
other, and nothing in this body could tell.*

**WE-5 — And the bit is bit 16, which is where Weatherproof and Disease collide.** In the derived
namespace bit 16 is **Weatherproof**; in the mutable one it is **Disease**. Because WE-4 tests both
raw layers on the target and the merged bitmap on the caster, **a diseased combatant gets the
weatherproof early-out**. *This stage is where the effect-layer contract's L-4 alias becomes
observable* — L-4 states that the namespaces collide, and this is the code that acts on it.

**WE-6 — It operates on the shared formula scratch scale.** `02AEE054`, the canonical scratch, not a
private accumulator — so the stage's product is visible to whatever else reads that scale in the same
evaluation.

*Added 2026-09-25 (FABLE, Claude Opus 5.5), on OPUS block 311, which executed all 288 combinations; the structure
below was re-read in `0038B220`.* **The rule table.** Each rule does four things:
1. tests one element bit of the action row's `+0x13` (`0038B295`, `0038B301`, `0038B37C`, …);
2. compares one class through a one-instruction thunk: the environment class `00321490`, the MWeather class
   `003214A0`, or the target's terrain class `003210E0`. Static call graphs miss the thunks, which is why this
   stage looked callee-free;
3. on a match, multiplies `02AEE054` by ×0.5 (`01CEBB70`) or ×1.2 (`008FCC90`);
4. **before each terrain test, stores the target's unit, resolved by `BattleStats_FindOwningBattleUnit`, to
   `02EBF188`** (`0038B30F` and four more sites). So the stage has a second product beside the scale.

| element | ×0.5 when | ×1.2 when |
|---|---|---|
| Fire | environment 0 | MWeather 2 |
| Lightning | — | environment 0 **or** terrain 0 |
| Ice | — | environment 2 **or** terrain 2 |
| Earth | terrain 0 | environment 1 **or** terrain 1 |
| Water | MWeather 2 | environment 3 **or** terrain 0 |
| Wind | — | MWeather 2 |

The multipliers compose: an element that meets both a ×0.5 and a ×1.2 rule ends at ×0.6. Class value 4, the
shipped default (`GB-2`), matches no rule. The table is data-shaped code, and the players' names for
environment classes 0–3 and terrain classes 0–2 remain FABLE's to give on the weather pages; this table
does not supply them.

## 5. State

**Owned:** nothing persistent. **Read, never written:** `02099DA8` and `02099DAC` (both other
systems'), the target's two effect layers, the caster's merged bitmap, the action's element mask and
the target's field record. **Written:** the shared scratch scale.

## 6. Relationships

| | |
|---|---|
| **Consumes** | [the field environment variant](../03-World-Area-Field/CONTRACT-field-environment-variant.md) — both globals, WE-3 |
| **Consumes** | [the two effect layers](../10-Status-Periodic-Terminal/CONTRACT-effect-layers.md) — WE-4, WE-5 |
| **Precedes** | `0038B6A0`, the affinity stage, sharing the element mask (WE-1) |
| **Sibling** | [`CONTRACT-preparation-step-family.md`](CONTRACT-preparation-step-family.md) — S-22's contracted quarter |

## 7. State transitions

*early-out test (WE-4) → resolve three classes (WE-2, WE-3) → multiply into the scratch scale
(WE-6).* No state transitions belong to this stage; it is a pure scaling pass over borrowed inputs.

## 8. Script · resource · event interactions

The element mask and the field environment tables are authored. The MWeather preset is authored and
reaches this stage only in banded form (WE-3).

## 9. Determinism

Deterministic. No generator is drawn.

## 10. Failure paths and edge conditions

- Bit 16 on **either** combatant skips the entire stage — not a neutral multiplier, **no stage at
  all** (WE-4).
- A target whose field record cannot be resolved falls back through `00263DD0`'s own path; this
  contract does not read it.

## 11. Observable behaviour

Fighting in the rain changes what a fire spell does — unless someone is wearing an Agate Ring, or is
diseased, which the engine cannot tell apart (WE-5).

## 12. Reproduction formula

Set bit 16 in the target's **derived** layer only and assert the stage is skipped; set it in the
**mutable** layer only and assert it is skipped too (WE-4). Set it on the caster's merged bitmap and
assert the same. Drive the MWeather preset across 0, 3 and 4 and assert the class steps 0, 1, 2 —
**at the publisher, not here** (WE-3).

## 13. Runtime validation

**None.** No experiment executes these four bodies. S-22's runtime cell is not addressed by this
contract. *Stated rather than left blank so a CONTRACT READY header is not read as evidence of
execution.*

## 14. Unresolved

- Whether the asymmetry in WE-4 — raw layers for the target, merged for the caster — is deliberate or
  an artefact of which structure each side had to hand.
- The step table and the ranged-weapon recipes, S-22's other two uncontracted pages.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| WE-4 — the three tests and their two shapes | `0038B226`, `0038B233`, `0038B23D` read at their addresses, **with the presence of both layer displacements as the control** | 1 |
| WE-3 — the getters are seven bytes and read exactly those globals | both bodies disassembled in full; `00263E10 → 02099DA8`, `00263E20 → 02099DAC` | 1 |
| WE-1 — the shared element mask | `0038B295` here, against the affinity stage's own read | 1 |
| WE-5's namespace collision | [the effect-layer contract's](../10-Status-Periodic-Terminal/CONTRACT-effect-layers.md) L-4 and the two-layer page's namespace map | 1 |
| WE-2, WE-6 and the terrain resolution | [the scaling page](Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md) | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on WE-1 through WE-6. **WE-4 is the one to copy
exactly**: testing the caster on raw layers, or the target on a merged bitmap, is the tidier design
and changes who is weatherproof.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **CombatFormula — internal.** The stage is this category's own.
- **WorldAreaField — SERVICE.** The three class getters belong to that layer, and WE-3 is the
  statement about what they return.
- **Status_Periodic_Terminal — SERVICE.** The effect layers WE-4 tests are that category's; the
  alias WE-5 names is its contract's L-4.
- **Every other layer reached is MECHANICAL**, through the stage's own callees. *Their addresses are
  deliberately not cited: each is a hub, and naming one imports its whole edge set.*

## 17. Related

- [Weather, terrain and element scaling](Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md) — the mechanism
- [Contract — the field environment variant](../03-World-Area-Field/CONTRACT-field-environment-variant.md) — WE-3's publisher
- [Contract — the two effect layers](../10-Status-Periodic-Terminal/CONTRACT-effect-layers.md) — WE-4 and WE-5's supplier
- [Contract — the preparation step family](CONTRACT-preparation-step-family.md) — S-22's contracted quarter

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives; one thunk is two instructions

**Attack.** WE-1, WE-3, WE-4 and the rule table's structure became checks at their instructions. Script:
`Tools/analysis-kit/gfz-scripts/falsify_element_scaling.py`, output `falsify_element_scaling.out`, image `73461d08…`,
0 BROKEN. The 288-combination behaviour is OPUS block 311's execution, and is not re-run.

| # | Clause attacked | Result |
|---|---|---|
| X0 | §2 sizes | **survives**: 1,138 / 7 / 7 / 53 B |
| X1 | WE-3 | **survives**: `00263E10` reads `02099DA8` and `00263E20` reads `02099DAC`, then each returns |
| X2 | WE-1 | **survives**: `test byte ptr [rcx + 0x13], 1` at `0038B295` |
| X3 | WE-4 | **survives**: target `+0x6A` and `+0x7A`, caster `+0x1C`, each `test ..., 1` |
| X4 | the rule table | **survives, made exact**: the constants are loaded into `xmm6` once each (0.5 from `01CEBB70`, 1.2 from `008FCC90`), and nine sites load, multiply and store `02AEE054`. There are five stores to `02EBF188`. The environment and MWeather thunks are single jumps, but **the terrain thunk `003210E0` is two instructions**: `mov rcx, [rcx + 0x10]` (the unit's actor), then `jmp 00263DD0` |

No correction.
