# Consumer check: RC-12's 0-based footer propagated to its consumers (OPUS, 2026-09-30)

Request `SWE2AUDITSPEC-REQ-OPUS-RC12-PROPAGATION-0930` (SWE2-AUDIT-SPEC batch-14 review, `auditspec-review-batch14-0930/REVIEW.md`,
narrowing 2). RC-12 is ANSWERED on SWE2-ORACLE's `rc12-footer-channels-runstate-0930` (`1e4537034`, restated `7dce8563b`): the
special-function footer is 0-based, `{u16 count; u16 special[18]}` with word k at `+2+2k`, so the wait resolver's footer word
`+0x18` is `special[11]`, the actor's `parameter` function, not `special[12]` / `mapjump`. The review's wording is applied.

- **Corrects:** the mapjump reading of footer word +0x18 in 01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md (the section 2 table row and the section 2.6 sentence) and 04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md (the +0x0C row), and the unclaimed slot meaning in _types/fields.tsv ActorStorageRecord 0x0C8.
- **Affected:** 01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md, 04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md (the _types store row is in the table below and in this publish)
- **Consumers:**

  | consumer | state |
  |---|---|
  | the scheduling page's section 2 table (+0x18 row) and section 2.6 sentence | revised-here |
  | the actor-record page's +0x0C row | revised-here |
  | fields.tsv ActorStorageRecord 0x0C8 (overrideSlots) | revised-here |
  | the scheduling page's RC-12 box (line ~289) | agrees (it already carries the 0-based answer) |
  | register row RC-12 | agrees (ANSWERED, 7dce8563b) |

- **Regression:** Database/FFXII TZA/_index/candidates/rc12-footer-channels-runstate-0930/rc12_slots.py (controls A and B fix the
  0-based word order; control C the site census). Run verified at 72657b7ca: controls PASS.
