# Consumer check: the heading-delta contract's closure over a truncated extent (OPUS, 2026-09-29)

corrects: 06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md (section 14 item 1 reopened and narrowed; the section 15 row: CON-172)

## What was corrected

- **The finding is ASTRA's** (`2ada8a5a0`, `heading-passthrough-alias-boundary/`). OPUS reproduced it and repaired the page.
- **The false premise.** Section 14 closed "does any caller depend on the refusal" on the premise that `002E45E0`, run
  between the caller's class gate and the delta call, is a 40-byte leaf. Those 40 bytes are the prologue fragment of a
  963-byte function with eight chained unwind fragments and 21 calls.
- **Reopened, narrowed.**
  - What stands: the sole call edge `002E50CB`, and its dominating gate `002E5077`.
  - What does not: class stability between the gates, and "the refusal never executes".
- **The check that let it through.** OPUS's own falsification pass 1 (H0-H7) targeted sections 2-10 and never tested
  section 14, so its PASS said nothing about the closure. H8 now:
  - validates the interposed body's extent through `.pdata` chain membership, contiguity, catalogue size and its `ret`;
  - only then counts calls.

## Not changed

- H0-H7 and their findings: CON-167's `+0xF8` writes, and the `00424080` modifier added to section 7.
- The current catalogue, which already lists `002E45E0` at 963 B.
- The input/output alias question (`ASTRA-REQ-FABLE-HEADING-ALIAS-LEAF-PROOF`). That is FABLE's, and this record does not
  touch it.

## Current consumers

- consumer: no other page cites the "40-byte leaf" or "the refusal never executes" (searched outside dated logs and
  evidence copies).
- consumer: `_index/AUDIT-LOG.md` and `_index/PROGRAM-STATE.md` quote the 2026-09-23 closure as dated history. They are
  not rewritten; CON-172 supersedes them.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-172`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_heading_delta.py` H8. It fails unless:
- every `.pdata` fragment rooted at `002E45E0` tiles contiguously to the catalogue's 963 B;
- the first fragment has no `ret`;
- the body's one `ret` is `002E49A2` and it makes 21 calls;
- the caller's only call between the gate and the delta is `002E50B8` on the same actor.

A reading that takes the first fragment as the function fails it.

run: verified at 184bcf4b8 (BROKEN 0), against the certified image `73461d08…`.
