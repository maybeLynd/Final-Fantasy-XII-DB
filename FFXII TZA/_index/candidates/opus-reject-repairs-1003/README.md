# Repairs for SWE2-AUDIT-SPEC's two REJECTs of OPUS rows at cc2da97b8 (OPUS, 2026-10-03)

SWE2-AUDIT-SPEC reviewed 28 OPUS homing and interior-citation packages at `cc2da97b8`: 26 ACCEPT, 2 REJECT. Both
rejects name an exact repair. OPUS re-read each function at the bytes before applying it.

## The two rows (OPUS)

| row | record | defect | repair |
|---|---|---|---|
| `001FB770` | [opus-sab-sound-bank-container-cloudint-1002](../opus-sab-sound-bank-container-cloudint-1002/consumer-check.md) | the byte passed to `001FB470` is read from the unwritten r8 home slot (0x48 frame), not a fifth argument; the third argument is the address of a slot holding the node | SPEC's clause, verbatim |
| `00568BB0` | [opus-contract-widget-object-homing-1002](../opus-contract-widget-object-homing-1002/consumer-check.md) | element `+0x48`'s top byte depends on word `+0x350`; elements `+0x20`/`+0x28` have a base colour and a `002DD7E0(6)` replacement on byte `+0x17`; the `+0x33E` gates were unpaired | row rewritten per SPEC's repair |

## Regression (OPUS)

`reject_rows_check.py` decodes both functions from the certified image, checks the instructions each repair rests on,
and checks the published rows ([`reject_rows_check.out`](reject_rows_check.out): 2 rows, FAILS 0). With `--rejected`
it runs on the rejected texts and fails both rows ([`reject_rows_check.rejected.out`](reject_rows_check.rejected.out)).
Each record's `interior_applier.py` still verifies its anchors: FAILS 0.
