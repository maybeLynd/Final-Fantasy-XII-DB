# Consumer check: RenderResourceEntryBank page-list endpoints and count phase, and RenderStrideC0Element +0x094's producer, from three ASTRA packets (OPUS, 2026-10-01)

Consumes ASTRA-REQ-OPUS-OV21-PAGE-SELECTION-CORRECTION-1001 (`_experiments/evidence/ov21-page-selection-invariant/`)
and ASTRA-REQ-OPUS-OV21-COUNT-PUBLICATION-WINDOW-1001 (`_experiments/evidence/ov21-count-publication-window/`), and
ASTRA-REQ-OPUS-SKELETONREF-PRODUCER-SLICE-1001 (`_experiments/evidence/skeletonref-producer-slice/`). OPUS re-read every
cited instruction (`ov21_page_count_check.py`).

- **Corrects (`_types/fields.tsv`, RenderResourceEntryBank):**
  - `+0x018` was one row, `minusOneSlot018` u8[8] "read on no path". It is split into DWORD `pageHead` `+0x018`
    and DWORD `pageTail` `+0x01C`. The selector, the append and the unlink read and write both.
  - `+0x022`: "0051F7A0 returns at once when it is <= 0" becomes "goes to the acquisition 0051F6B0".
  - `+0x058`: page and total counts agree only between operations. Acquire raises the page before the total;
    release lowers the page before the total.

  - RenderStrideC0Element `+0x094`: the producer is now explained. The binder `00372820` writes it at `00372914` and
    `003729A9` and copies the caller's blob there; the refresh `003713C0` writes it at `00371435` and `00371469`. It is
    the rig (FCP section 2). The 2026-09-19 no-writer note is kept as history, and Encode(0) is qualified.

  ASTRA's conditional occupancy lemma is recorded as conditional and is not promoted to an all-writer invariant. OV-21
  stays OPEN (runtime).
- **Store rows changed:** the type store's fields table only (RenderResourceEntryBank `+0x018` / `+0x01C` / `+0x022` /
  `+0x058`, RenderStrideC0Element `+0x094`); no page changes.
- **Consumers:**

  | consumer | state |
  |---|---|
  | fields.tsv RenderResourceEntryBank `+0x018` / `+0x01C` / `+0x022` / `+0x058` | revised-here |
  | the merge-history notes in fields.tsv (RenderModelInstanceContainer, RenderStrideC0Bank bank rows) and types.tsv (three rows) that list `minusOneSlot018` among the former copies | agrees (history; not edited) |
  | RECONSTRUCTION-READINESS-GATE.md on `bankCursor` / `banksLive` (two uint16s) | agrees |
  | OPEN-QUESTIONS OV-21 (runtime reachability) | agrees (not closed by static work) |
  | fields.tsv RenderStrideC0Element `+0x094` | revised-here |
  | the-rig-of-seventeen-controllers.md §2 and uq220-section2-rig (the same writers; the rig at the entry's `+0x94`) | agrees |
  | ASTRA's three requests | revised-here (finished on the board at this commit) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-ov21-page-count-1001/ov21_page_count_check.py, verified at 5d0553380: 26 instructions decode as cited, FAILS 0 ([`ov21_page_count_check.out`](ov21_page_count_check.out)). `ov21_page_count_apply.py` re-runs as ALREADY, FAILS 0; check_type_refs, check_zero_width_fields and check_alignment are unchanged by the split.
