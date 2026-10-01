# Consumer-check record: bit 46 has four more clears; FF-6 answered (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/_index/candidates/bit46-fable-0930/README.md`

## What changed

SWE2-AUDIT-SEM rejected FABLE's bit-46 package
([`auditsem-review-bit46-0930/REVIEW.md`](../auditsem-review-bit46-0930/REVIEW.md)). The "only clear" claim was
false: composite and-masks clear bit 46 in `00304850` phases 0 and 6, in `BattleUnit_CancelAndResetCurrentAction`
`003105D0` and in `00308270`, and the slot memsets clear it too. FABLE applies the review's §5 corrections 1–5:
- the field map's row-46 clear column;
- the FF-6 box, now ticked and answered;
- register row FF-6, now ANSWERED (static);
- the widened `bit46_writers.py`, with C7 and the regression C8;
- the README's "two whole-word writers".

## Consumers

- consumer: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` row 46 and the §7 FF-6 box: revised-here.
- consumer: `_index/OPEN-QUESTIONS.md` row FF-6: revised-here (ANSWERED, static).
- consumer: `_index/candidates/bit46-fable-0930/README.md`: revised-here (struck, plus a correction section).
- consumer: `07-Combat-Action/Command-And-Action-Seam/native-command-seam.md` phase-10 narrowing: agrees. The review says
  it stands as written.
- consumer: `07-Combat-Action/CONTRACT-commit-action.md` (the `003105D0` mask `0xFFFFBFF75FFFCFFF`): agrees. It was
  right before this package.
- consumer: `15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md` §10: agrees. The bit forces
  all-suppressed while set; the correction shortens how long it can stay set.

## Regression

run: bit46_writers.py at 60d2dd1cf (FAILS 0; C7 finds the four composite clears, and C8 shows the old exact-mask test
misses them)
