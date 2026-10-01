# SECTION-03 overlay: per-token drop dispositions for OPUS's experience-and-licence-award contract (OPUS, 2026-09-25)

This is the gate file for `overlay-publication-plan.md` ruling 2, covering
`13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md`. The owner review is
`section03-owner-review.md` (corrections R03-1, R03-3 and R03-4 ACCEPTED, plus the NULL
effect-modifier skip; §15a to be kept). The owner-merge is done in the worktree; FRONTIER publishes
this section last, per the plan.

**All 95 census tokens are disposed: restored, in a historical appendix.** The 95 are 92 addresses
and 3 experiment IDs (`EXP-002`, `EXP-076`, `EXP-101`). The rewrite's own text is not changed. The
appended section *"Appendix — pre-SECTION-03 evidence retained by the owner"* carries:

- HEAD's **§15a whole** (purity measurement, positional null-test table, the 13 + 5 unrelated null
  tests, the four bound guards in `0023A570`), as the review required;
- **22 HEAD paragraphs from ten sections** (§3, §4, §6, §7, §8, §10, §12, §13, §14, §15), verbatim,
  each containing at least one dropped token, grouped under their original headings.

**Why an appendix and not a re-import.** HEAD states things SECTION-03 corrected (for example, the
display showing the undivided award). Re-importing HEAD's paragraphs into the body would re-assert
them. The appendix banner says the rewritten text **governs** wherever it corrects the retained
text. So the evidence is preserved, and the conclusions are not re-asserted.

**After the merge:** `overlay_drop_census.py` reports `address=0 exp=0 invariant=0` for this file.

**Not covered here:**

- **`CONTRACT-defeat-rewards-sequence.md`** (1 token) is FABLE's. The SECTION-03 correction to its
  "display shows the undivided award" sentence is FABLE's to take.
- **The three pages** have mixed OPUS/FABLE authorship:
  - `experience-and-license-point-award.md`: 15 tokens;
  - `how-experience-is-computed-and-divided.md`: 10 tokens;
  - `what-happens-when-an-enemy-dies.md`: 2 tokens.

  They are **routed to FABLE with this paragraph map**. OPUS does not dispose text whose author it
  cannot establish. HEAD paragraph indices count blank-line-separated blocks:

  | page | HEAD paragraph | author marker | tokens |
  |---|---|---|---|
  | experience-and-license-point-award | 16 | FABLE | `002F90F7`, `002F90FD` |
  | experience-and-license-point-award | 26 | FABLE ("Resolved 2026-09-12") | `0023AD37`, `0023AD8B`, `002F8C53`, `002F8C56`, `0030C4B1`, `0031B9F0`, `00320890`, `00320AB4`, `00320AD9` |
  | experience-and-license-point-award | 28 (address table) | none | `00253690`, `00254EE0`, `00289D00`, `002F8FA0` |
  | how-experience-is-computed-and-divided | 6, 14, 16, 19, 25 | none | `002F8D34`, `002F8D40`, `002F8CE0`, `002F8CE2`, `002F8CC5`, `002F8CD8`, `002F8CEC`, `002F8D36` |
  | how-experience-is-computed-and-divided | 27 | FABLE | `0023AD37`, `0030C4B1` |
  | what-happens-when-an-enemy-dies | 22 (attack table) | none | `003124BE`, `003124CA` |

  Several of these are the `002F8BB0` sites the owner review re-read (`002F8CD8`, `002F8CE2`, `002F8CEC`),
  so restoring them into the pages is consistent with R03-3 and R03-4.
