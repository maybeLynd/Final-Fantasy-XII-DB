# Consumer check: 08-Combat-Formula contradictions from a local reconstruction-readiness pass settled on the pages (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-FORMULA-1002: stream R run locally, with no cloud credit. A read-only reader mapped
`08-Combat-Formula/` (rated NOT YET; the map is filed in the RE repo as `docs/readiness/08-formula.md`). It found 56
contradictions, 20 of them value-changing, and decided every value item from the shipping image; none was left to
page text.

A second read-only pass drafted the strike edits (`apply_08formula.py`, 107 edits on 21 pages; only disfavoured
sides; strikes open and close on one line). OPUS re-checked a sample of the value items at the bytes
(`formula_check.py`):
- the foe HP cap of 1,000,000,000;
- slot 98's ×2.0;
- both variants scaling Strength;
- the reset to -1;
- the 0x30-byte context.

- **Affected:** 08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md, 08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md, 08-Combat-Formula/CONTRACT-environmental-element-scaling.md, 08-Combat-Formula/CONTRACT-formula-step-table.md, 08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md, 08-Combat-Formula/CONTRACT-preparation-step-family.md, 08-Combat-Formula/CONTRACT-stat-derivation.md, 08-Combat-Formula/CONTRACT-weapon-recipes.md, 08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md, 08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md, 08-Combat-Formula/README.md, 08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md, 08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md, 08-Combat-Formula/Status-And-Augment-Namespaces/README.md, 08-Combat-Formula/Steal/the-steal-roll.md, 08-Combat-Formula/Step-Table/combat-formula-step-table.md, 08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md, 08-Combat-Formula/combos-and-the-guard-parry-flag.md, 08-Combat-Formula/elemental-affinity-and-the-five-bytes.md, 08-Combat-Formula/the-auto-status-rebuild.md, 08-Combat-Formula/where-a-stat-number-comes-from.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the 21 08-Combat-Formula pages (each disfavoured side; README labels) | revised-here |
  | 12-Items-Equipment-Shops-License shop page (the favoured side of item 50) | agrees |
  | RE repo `docs/readiness/08-formula.md` | routed-to-OPUS (filed from this commit) |
  | the hit-pipeline odds (structural gaps 1-2) | routed-to-OPUS (OPUS-HIT-PIPELINE-ODDS-1002, the next publish) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-formula-readiness-fixes-1002/formula_check.py, verified at 5144628ac: 9 instructions and the 2.0 constant as cited, FAILS 0 ([`formula_check.out`](formula_check.out)). `apply_08formula.py` re-runs as ALREADY (107), FAILS 0.
