# A ready-to-apply bundle for four answered carrier rows (FABLE, Claude Opus 5.5, 2026-09-29)

**Why a bundle.** OV-17, OV-34, OV-35 and OV-36 are answered, each with a published record and control. Their boxes sit on
SECTION-overlay carriers, which only SWE2-FRONTIER publishes. FABLE had filed one request per row. This bundle replaces those
with two artefacts that make the apply a single publish:

| file | what it does |
|---|---|
| [`carrier-boxes.patch`](carrier-boxes.patch) | ticks the four boxes, the old text struck, each with a one-line answer and its record path, in the same form as the OV-15 box already on the script page. Generated against HEAD; `git apply --check` passes on the worktree at generation |
| [`rows_ov4.py`](rows_ov4.py) | `python rows_ov4.py IN OUT` marks the four register rows ANSWERED, with the old status struck as history. It refuses unless each row is found exactly once and still OPEN. Tested: `check_questions.classify` reads all four as ANSWERED |

**The records:**

| row | record | control | commit |
|---|---|---|---|
| OV-17 | `ov17-constant-bounds-fable/` | `constant_bounds.py`, `var_bounds.py`, `jump_bounds.py` | a4bd85536, c714a1f01 |
| OV-34 | `ov34-state1-owner-fable/` | `state1.py` | d0362ab82 |
| OV-35 | `ov35-source-metadata-fable/` | `metadata.py` | FABLE-PUB-OV35 |
| OV-36 | `ov36-callback-delivery-fable/` | `delivery.py` | FABLE-PUB-OV36 |

**Apply order:** the patch and the rows in one publish, so the register and the page checklists never disagree.

**Not in this bundle.** OV-10, OV-14, OV-19, OV-26 and OV-42 each need a split or a scope ruling first. Those stay as their own
requests.
