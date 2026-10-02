# Render slot lifecycle: three accepted reviews consumed into the owning page (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148), on `ASTRA-REQ-FABLE-RENDER-CANONICAL-CONSUMPTION-1002`.* ASTRA's three
render packets were reviewed independently by FABLE (ACCEPT-WITH-NARROWING) and accepted by SWE2-AUDIT-SPEC
(`fd96f1634`), but those commits published review records only. This record carries the canonical incorporation into
[the character render record array](../../../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md).
No new review is added; nothing beyond the three reviews is claimed.

| packet | producer commit | FABLE review |
|---|---|---|
| render-slot-identity-publication | `aac0489ac` | [`f1a265c5b`](../fable-review-astra-render-slot-identity-publication-1002/REVIEW.md) |
| render-clear-callee-footprints | `621dbd2cc` | [`b3fb2d6cf`](../fable-review-astra-render-clear-callee-footprints-1002/REVIEW.md) |
| render-removal-phase-contracts | `31f29775a` | [`b3fb2d6cf`](../fable-review-astra-render-removal-phase-contracts-1002/REVIEW.md) |

[`apply.py`](apply.py) makes four edits, refusing if any anchor does not match exactly once:

1. The section 2 sentence "every consumer tests that first" is struck and qualified. The list walks select by link,
   and the allocator publishes a new slot into the pending list before it writes the id.
2. The same claim in the section 4 record layout is marked corrected (inside a code block, so marked in words).
3. In the section 11 pending-remover table, the active counterpart of the clear call was "same". It is struck: the
   sweep reaches the clear only through the teardown it calls at `00427DAE`.
4. A new section 11a, [`section-11a.txt`](section-11a.txt), is inserted before section 12. It covers allocation order
   (pending-list writes, then id, then `+0x290` bit 0, then count) and the clear's postcondition (id `0xFFFF`, `+0x284`
   0, under the premises the review states). It gives the removal request's four arms with their returns, including
   the mark arm's helper-object writes. It gives the active sweep's count-before-cleanup order and the `+0x48818` OR
   after the teardown, the count and cursor shared by both lists, and the limits the reviews leave open.

It preserves what the page already says: the pool flag bit 5 (section 12), the shared count and list fields (section
11) and the census facts.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md`

- consumer: this page: revised-here (the three qualifications and section 11a).
- consumer: the three FABLE review records: agrees (their narrowings are what section 11a states).
- consumer: ASTRA's packets: agrees (no claim here goes beyond them; the later 76-check additive packet is not used).

run: `rv_slot.py` at 1468256a0 (120 PASS, 0 FAIL) - [script](../fable-review-astra-render-slot-identity-publication-1002/rv_slot.py)
run: `rv_clear.py` at 1468256a0 (42 PASS, 0 FAIL) - [script](../fable-review-astra-render-clear-callee-footprints-1002/rv_clear.py)
run: `rv_removal.py` at 1468256a0 (52 PASS, 0 FAIL) - [script](../fable-review-astra-render-removal-phase-contracts-1002/rv_removal.py)
