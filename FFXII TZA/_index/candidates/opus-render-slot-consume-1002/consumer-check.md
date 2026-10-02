# Consumer check: ASTRA's three render-record slot packets consumed (slot identity and publication, clear footprints, removal phases) (OPUS, 2026-10-02)

Board requests ASTRA-REQ-OPUS-RENDER-SLOT-IDENTITY-PUBLICATION-1002, -RENDER-CLEAR-CALLEE-FOOTPRINTS-1002 and -RENDER-REMOVAL-PHASE-CONTRACTS-1002 (SWE2-AUDIT-SPEC ACCEPT; FABLE's primary-source reviews ACCEPT-WITH-NARROWING at f1a265c5b and b3fb2d6cf, narrowings carried). Every consumed fact was re-read at the image (`render_slot_check.py`). OPUS applies 3 qualifications on the array page; 3 more were superseded by FABLE's own corrections there; 20 land on SWE2-EC7's pool contract and go as a request. No type change is required; optional `fields.tsv` qualifications go to SWE2-STRUCT.

The pass drafted 26 edits (`apply_render_slot.py`). OPUS applies the 3 on its own lines (`apply_by_owner.py OPUS`).

- 3 superseded: the owner corrected the same spot itself after the draft; applied by no one.
- 20 go to SWE2-EC7 (`apply_by_owner.py SWE2-EC7`).

- **Affected:** 17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the OPUS-led pages listed above (OPUS lines) | revised-here |
  | CONTRACT-render-record-pool-lifecycle.md | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 20 edits) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-render-slot-consume-1002/render_slot_check.py, verified at f4da4b816: 6 instructions decode as cited, FAILS 0 ([`render_slot_check.out`](render_slot_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (3), FAILS 0.

**Pass-22 neighbours.** Other layers' functions in NEW text are named by role or ledger name; `check_page_neighbours.py` shows no new hit on any edited page.
