# Consumer check: "bit 21 is set and cleared only by the Save/Load handlers" corrected (OPUS, 2026-09-30)

- **Corrects:** the claim that capability-policy bit 21 is set and cleared only by the Save/Load controller handlers.
- **Affected:** 15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md (§7 SD-3 box, §9 "own row 1 bit 21")
  and _index/candidates/sd3-policy-bit21-0930/README.md (its opening sentence).
- **Correction:** a census of all 77 call sites of the set / clear primitives finds these additional writers:
  - row 1: the movie player (`001B7690`, `001B7F30`, `001B8400`, `001B82A0`), the spawn-verb body `0023FBE0`,
    `002CEB40` and the title-asset consumer `003939B0`;
  - row 0: the title singleton's handler `00394070`;
  - rows 2 and 8: the restore loop `00229510`.
- **Consumers:**

  | consumer | state |
  |---|---|
  | capability-inhibition-policy.md §7 SD-3 box and §9 | revised-here |
  | _index/candidates/sd3-policy-bit21-0930/README.md | revised-here (struck "only", pointer to W1) |
  | 15-Input/CONTRACT-input-subsystem.md §11 | agrees: it names the two consumers of row 1 bit 21 and makes no writer claim |
  | 16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md | agrees: it records the title objects' channel-1 set and channel-0 clear |
  | _index/OPEN-QUESTIONS.md SD-3 row | routed-to-OPUS-REQ-DATA-SD3-ANSWER-ROW-0930, for the register owner to restate |

- **Regression:** Database/FFXII TZA/_index/candidates/sd3-bit21-pause-0930/sd3_pause.py, W1, asserts the full writer
  set and fails on the "only Save/Load" set. Run verified at cdc88cf40 (worktree at HEAD cdc88cf40, FAILS 0).
