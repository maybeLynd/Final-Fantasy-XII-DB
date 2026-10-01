# Consumer check: falsification pass 1 on CONTRACT-license-check (OPUS, 2026-09-29)

corrects: 12-Items-Equipment-Shops-License/CONTRACT-license-check.md (§2 "the only caller fixes at 1"; I4 "the early exit is semantically load-bearing"; I1 "three exits"; the 32-bit row sum; four pre-EXP-140 currency lines)
corrects: 12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md (§4 "the loop's early exit is semantically load-bearing")

## What was corrected

- **The kind argument has two sources.** `00323BB0` is entered by two tail jumps:
  - `00323EC0`, at `00323FFD`, with `edx = 1`;
  - `BattleStats_HasRequiredLicenseForEquipment` (`00323C60`), at `00323CF7`, with `edx = 0` and the item id in `r8d`.

  The builder `002F8FA0` has one caller, `00323BB0`. It compares the kind with `00323890`'s class of each licence row's
  byte `+5`, so the kind is 0 for equipment and 1 for actions. `CON-159`.
- **The early exit is an optimisation.** After the builder returns, `00323BB0` writes no memory and calls only
  `__security_check_cookie`. It returns the constant 1 or 0. The result is the OR of all `0x2E` byte-ANDs either way.
  `CON-160`.
- **Precision.**
  - I1 has four exits: one unlicensed and three licensed.
  - The action-row and party-row addresses are summed in 32 bits (`00323F43`, `00323FAF`), so the decoded base loses its
    upper half.
- **Currency.** Four lines saying "nothing is executed" predate EXP-140. They are struck or rewritten.
- **What survives.** §2's signatures, the validator's range and table, and I1's exits and their order. Also I3's bit, I5's
  range, search and signed gate, the three-by-six counter, §7's purity and §9's determinism.

## Current consumers

- consumer: [license-check-what-the-board-actually-tests.md](../../../12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md): revised-here.
  Its §4 sentence is struck, with the reason.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-159`, `CON-160`).
- consumer: [EXP-140](../../../_experiments/EXP-140-license-check-exec.md) agrees. Its "46-byte scan is load-bearing" is
  about the scan's extent: a byte-45-only overlap must license. That is what L6 finds, and it is not a claim about stopping
  early.
- consumer: [CONTRACT-equipment-compatibility.md](../../../12-Items-Equipment-Shops-License/CONTRACT-equipment-compatibility.md) agrees.
  It describes the equipment gate's own exits and makes no claim about `00323BB0`'s callers or kind.
- consumer: [s29-opus-replay-equipment-eligibility](../s29-opus-replay-equipment-eligibility/README.md) agrees. It already
  records that the equipment path asks `00323BB0` for licence class 0.
- consumer: [EXP-194](../../../_experiments/EXP-194-state-predicate-leaves-exec.md) agrees. It executes `00323C60`'s early
  return before `323BB0`, which is the kind-0 entrant this pass names.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_license_check.py`, checks L0-L8.
- L5 fails if `00323BB0` loses either entrant or either kind, which rejects "the only caller fixes at 1".
- L6 fails if anything after the builder writes, calls or computes a non-constant return. That rejects "the early exit is
  load-bearing".

run: verified at df93a1eb7 (BROKEN 0), against the certified image `73461d08…`.
