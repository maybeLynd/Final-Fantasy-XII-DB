# Consumer check: ASTRA's name-binding deletion carried into the per-frame update gate contract (OPUS, 2026-10-01)

This is `ASTRA-REQ-OPUS-NAMEBINDING-DELETION-CONTRACT-1001`. SWE2-AUDIT-SPEC ACCEPTed it without narrowing
([review](../auditspec-review-namebinding-deletion-1001/REVIEW.md), `f24457dc7`).

OPUS re-read three ranges at the bytes:
- `002EAEB0`-`002EAECC`: the mark-only arm sets only `+0x18` bit `0x04`. A first draft of this section said "`0x04` and
  `0x10`"; it was corrected before publishing.
- `002E6D66`-`002E6DEA`: the drain conditions and the masked unregister.
- `002E93E1`-`002E93F7`: the release call and the handle clear.

- **Corrects:** nothing struck; a new OPUS section is added: name-binding removal, completion and the release drain.
- **Affected:** 00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the gate contract's new section | revised-here |
  | the name-binding page's 16-bit stamp | agrees (corroborated, unchanged) |
  | the deletion policy and the precise mask naming | FABLE's (ASTRA-REQ-FABLE-NAMEBINDING-DELETION-CONSUME-1001) |
  | the OV-25 box and OV-21 preparation | SWE2-FRONTIER's (ASTRA's routing) |
  | the contract's `002E6900` catalogue paragraph | unchanged here; ASTRA's lane-drain correction waits on its own review (ASTRA-REQ-SPEC-LANE-DRAIN-CORRECTION-1001) |

- **Applier:** [`namebinding_incorp.py`](namebinding_incorp.py), run: [`namebinding_incorp.out`](namebinding_incorp.out). It is
  idempotent. The saved run is the re-run after the section was applied, so it reads ALREADY, FAILS 0.
- **Regression:** Database/Tools/analysis-kit/gfz-scripts/check_questions.py --db (the table and the checklists agree).
