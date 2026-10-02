# Consumer check: the hit pipeline's odds - knockback, counter, combo, the ranged critical and the post-modifiers (OPUS, 2026-10-02)

Board task OPUS-HIT-PIPELINE-ODDS-1002: the 08-Combat-Formula readiness map's structural gaps 1-2. A read-only reader
read `00388350`, `00388490`, `00388550`, `00389140` and `00390F20` whole, and OPUS byte-checked them
(`hit_odds_check.py`).

- **Corrects:**
  - "Parry chance from Speed" (`02AEDFDC` / `02AEDFC4`, slot 7) is the counter chance from augments 6 and 7.
  - Result `+0x18` bit 0 / slot 29 is the ranged critical roll (weapon `+0x1C`), not a resource reaction.
  - Slot 98's ×2 applies only on recipes 25-27.
  - `00390F20` reads action bits 10 and 11, and `+0x2D`.
  - Merged id 13 is the combo augment, not "Disable".
- **Adds:** a section on the step-table page with every formula, the draw accounting and worked examples.
- **Affected:** 07-Combat-Action/Action-Definition-Row/the-action-definition-row.md, 07-Combat-Action/Result-Record/the-result-record-field-map.md, 08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md, 08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md, 08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md, 08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md, 08-Combat-Formula/Step-Table/combat-formula-step-table.md, 08-Combat-Formula/combos-and-the-guard-parry-flag.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the eight pages listed | revised-here |
  | the-thirty-two-statuses.md (statuses are not in the layers) | agrees |
  | function names such as `ComputeParryChanceFromSpeed` in the name store (a name, kept) | routed-to-OPUS (a later rename) |
  | Tools/dashboard/ff12_content.py note that combo / critical rates are not located (a tool) | routed-to-OPUS (a tool fix) |
  | RE repo docs/readiness/08-formula.md (gaps 1-2) | routed-to-OPUS (noted from this commit) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-hit-pipeline-odds-1002/hit_odds_check.py, verified at 56d353a3a: 16 instructions and the 1.8f / 0.7f constants as cited, FAILS 0 ([`hit_odds_check.out`](hit_odds_check.out)). `apply_hit_odds.py` re-runs as ALREADY, FAILS 0.
