# Status and augment namespaces (formula side)

The namespace model itself is documented once, on the **state** side:

→ [`../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md`](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)

This folder exists because the *formula* consequences are owned by CombatFormula and are
referenced from several documents here.

## Why it matters to a formula reader

`003847C0` `BattleFormula_BuildEvaluationContext` ORs the caster's mutable status layer
(BKBI `+0x68`) and derived augment layer (BKBI `+0x78`) into one merged bitmap at
`FormulaEvaluationContext+0x1A`.

**After that merge no calculator can tell which layer a bit came from.**

| Merged bit | Mutable status | Derived augment | Formula effect |
|---:|---|---|---|
| 2 | Petrify | **AccuracyBoost** (Cameo Belt) | ranged severe-weather accuracy bypass — [`../Recipe-System/ranged-weapon-recipes.md`](../Recipe-System/ranged-weapon-recipes.md) |
| 16 | Disease | **Weatherproof** (Agate Ring) | weather/terrain element-scaling bypass — [`../Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`](../Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md) |
| 17 | Lure | Thievery | ~~no formula role established~~ the steal's three-roll branch: the merge carries the status layer, so a Lured source steals like one wearing Thief's Cuffs *(corrected 2026-10-02, OPUS: checked at `00384827`, the merge tests `[stats + 0x68 + (id>>3)]`, and `003904A5` `test byte ptr [rsi + 0x1c], 2`; the-evaluation-context-field-map.md §2.3)* |

Target-side tests in `0038B220` read the two BKBI layers **directly** rather than the merged
context — so a target's status and augment bits are still distinguishable there, while the
caster's are not.

## Rules for documents in this category

- Never write "status bit N" for a merged-context test. Write "merged effect bit N", then
  state the intended augment identity and note the status alias.
- Never rename one namespace's entry after the other's.
- The aliasing is an observed engine property. Whether it is deliberate is ~~**open question
  E-1** — do not assert either way~~ **not a fact the image carries — E-1 closed 2026-09-12 (FABLE)
  as an intent residue, with the consequences stated instead.** What the binary does decide is
  whether each alias can *fire* from the status side, and two of the three can: **Petrify** (status
  2) is the count-down, not Stone — a petrifying unit keeps acting, because the out-of-play mask
  `0x80000003` is statuses 0, 1 and 31 ([the status write](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) §2) — so a petrifying caster's merged bit 2
  reads as **AccuracyBoost** and bypasses the ranged severe-weather accuracy gate; **Disease**
  (16) does not stop acting either, so a diseased caster's merged bit 16 reads as **Weatherproof**
  and turns the weather / terrain element-scaling stage off at its caster test (`0038B220`,
  `TEST byte ptr [R8+1C], 01`), while the same stage's *target* tests read both layers directly and
  so alias the target's Disease with its Weatherproof as well. ~~**Lure** (17) has no formula reader~~
  ~~and its alias is inert.~~ **Lure** (17) is read by the steal's three-roll branch (`003904A5`), so a Lured source steals with three independent rolls *(corrected 2026-10-02, OPUS: checked at `00384827` and `003904A5`)*. Live discriminating checks, queued: a petrifying bow user in severe
  weather should keep full accuracy; a diseased caster's elemental damage should ignore weather
  and terrain. Whether the designers meant that is not recoverable from the shipped data.
