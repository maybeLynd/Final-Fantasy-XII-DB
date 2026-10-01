# Affected-consumer check: HP clamp needs ordered bounds (OPUS, 2026-09-27, consuming ASTRA-RETURN-OPUS-HP-FLOOR-CAP-PRECONDITION)

**State: PENDING REVIEW.** The owner applies the qualification. Independent acceptance is routed to SWE2-AUDIT-SPEC.

**The ruling.** `00300530`'s clamp has one side per branch.
- Below the floor: `00300651` takes the floor and `00300654` jumps past the cap.
- Otherwise: it clamps to the effective cap, with no floor recheck.

The floor slot comes from `unit+0x48`, which `00239820` writes unchecked. So `floor <= hp <= cap` holds only when
`floor <= effectiveCap`. Not claimed: that any caller or script creates an inverted pair. Primary bytes re-read by
OPUS: `0030063B`–`003006A7`, `00300749`, `00239820`–`0023983A`.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md` §4 | invariant qualified; the second-store survival sentence struck and qualified | revised-here |
| `08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md` rule 3 and its "only bottom value" line (FABLE's mechanism page) | needs the same precondition | routed-to-FABLE |

Corrects: 08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md

Run receipt: `_experiments/evidence/hp-floor-cap-precondition/check.py` executed at 8f2094b54 (ASTRA's package, re-run by OPUS before publish).
