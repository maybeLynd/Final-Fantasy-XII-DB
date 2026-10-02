# Consumer check: the suspended-action copy range corrected in the commit-action contract (OPUS, 2026-10-01)

This is `ASTRA-REQ-OPUS-SUSPEND-COPY-CORRECTION-1001` with `ASTRA-REQ-OPUS-AUTOMATIC-SUSPEND-DOMAIN-1001`. SWE2-AUDIT-SPEC
ACCEPTed all three packets without narrowing:
[suspend-restore-copy-origin](../auditspec-review-astra-suspend-restore-copy-origin-1001/REVIEW.md),
[automatic-suspend-phase-domain](../auditspec-review-astra-automatic-suspend-phase-domain-1001/REVIEW.md) and
[autoattack-commit-exception](../auditspec-review-astra-autoattack-commit-exception-1001/REVIEW.md) (`fd45553c7`).

OPUS re-read at the bytes: `0030EDA0`-`0030EE99` (restore: base `+0x6B0` at `0030EDA7`, the loop's lead `lea` at
`0030EDB6`, stores at `rcx - 0x80`, tail to `+0xBA0`, the scan comparing the saved `r8` at `0030EE5D`);
`0030EFF0`-`0030F0F8` (snapshot: the refusal at `0030EFFF` / `0030F016` / `0030F01F`, the copy from `+0x6B0`, the
`memset` and the `+0xB88` store); `00312FA0` (`0030EFF0` at `0031307B`, then `0x96` and 0 into `0030F760` at
`003130DC`, `+0x28` cleared at `00312FB5`); `0030FA00` (1 at `0030FA54`).

- **Corrects:** CONTRACT-commit-action row for `0030EDA0`: the destination is `unit + 0x6B0` .. `+0xBA0`, not
  `unit + 0x730`. Adds, without striking anything: the callers' differing cancel argument and `0030EFF0`'s refusal
  domain.
- **Affected:** 07-Combat-Action/CONTRACT-commit-action.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the commit-action contract's `0030EDA0` row and §2 cancel argument | revised-here |
  | `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` `+0x730` row (the cancelled action's 16-byte record) | agrees (a different write, not this copy) |
  | the field map's note that the suspend zeroes the `0x4F0`-byte block after copying | agrees |
  | `04-Actor-Entity/Battle-Unit/battle-unit-accesses.tsv` rows at `0030EE13` (`w`) and `0030F0A9` (`r`) filed under `+0x730` | routed-to-OPUS-REQ-STRUCT-SUSPEND-COPY-CENSUS-ROWS-1001 (the census follows the loop's first `lea` only; both are the tail access, at `+0xB30`) |
  | the earlier board hint that all known commit callers pass 1 (checkpoints 45492-45494) | superseded by the §2 note, no page carried it |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-suspend-copy-origin-1001/copy_range_check.py, verified at 8db70f9f2: all 26 cited instructions decode as recorded, FAILS 0 ([`copy_range_check.out`](copy_range_check.out)).
