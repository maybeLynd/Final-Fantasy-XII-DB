# Consumer check: falsification pass 1 on CONTRACT-heading-speed-to-position-delta (OPUS, 2026-09-29)

corrects: 06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md (§5 "Written: only the caller's output vector"; §7 the order of operations)

## What was corrected

- **§5.** The body also writes the movement block's `+0xF8`:
  - `sqrtf(|v|²)` on the pass-through (`002E43E6`);
  - the speed, when `+0xF8` is negative, on the decomposition path (`002E445C`).

  `CON-167`.
- **§7.** The `00424080` modifier runs between the wrap and the decomposition when `[actor+0xC0]` is live. It may change the
  wrapped yaw and the speed.
- **What survives.** LD-1 (five gate sites), LD-2, LD-3, LD-5, LD-4's flat branch, LD-6, and §9's determinism.

## Current consumers

- consumer: [heading-speed-to-position-delta.md](../../../06-Movement-And-Navigation/heading-speed-to-position-delta.md) agrees.
  It documents both `+0xF8` writes and the `00424080` modifier.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-167`).
- consumer: [CONTRACT-facing-and-steering.md](../../../06-Movement-And-Navigation/CONTRACT-facing-and-steering.md) agrees. It is
  the sibling named in §6 and makes no claim about this body's writes.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_heading_delta.py`, checks H0-H7.
- H3 fails unless both `+0xF8` stores exist, which rejects "writes only the output".
- H4 fails if the modifier call leaves its place between the wrap and the speed-0 test.

run: verified at 9161b92ea (BROKEN 0), against the certified image `73461d08…`.
