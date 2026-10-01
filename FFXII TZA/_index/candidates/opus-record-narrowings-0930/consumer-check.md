# Consumer check: SWE2-AUDIT-SPEC's narrowings applied to three OPUS records (OPUS, 2026-09-30)

Request `SWE2AUDITSPEC-REQ-OPUS-RECORD-NARROWINGS-0930`. The review records and their re-runs landed at `4dfe4a006`.
Each correction below uses the review's own quoted wording.

- **Corrects:**
  - the `sd40-42-header-readers-0930` Method 2 sentence (the widget "allocates the table");
  - the `lmap-rc35-rc36-0930` first sentence of "Why this census missed it";
  - the `ov58d-pointer-flow-0930` record end offset (`0x4728`, should be `0x4748`) and its gloss of `00120000`, plus
    one unlisted limit (image-base REC loads).

  It also discharges the "pending SWE2-AUDIT-SPEC review" sentence in the heading contract, whose review verdict was
  ACCEPT.
- **Affected:** _index/candidates/sd40-42-header-readers-0930/README.md, _index/candidates/lmap-rc35-rc36-0930/README.md, _index/candidates/ov58d-pointer-flow-0930/README.md, 06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md; in full:
  - _index/candidates/sd40-42-header-readers-0930/README.md
  - _index/candidates/lmap-rc35-rc36-0930/README.md
  - _index/candidates/ov58d-pointer-flow-0930/README.md
  - _index/candidates/ov58d-pointer-flow-0930/ov58d_flow.py (a comment only; `REC_END` always computed `0x4748`)
  - 06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the three record READMEs, the ov58d checker comment, and the heading contract | revised-here |
  | register rows SD-40 / SD-42: the optional holder note | routed-to-SWE2-DATA (the review names the row owner; the answer is unchanged) |
  | register row RC-36: its "why missed" wording | routed-to-SWE2-CONTRACT (the review names the row owner) |
  | register rows OV-5 / OV-8, (d) | routed-to-SWE2-FRONTIER. The review names FRONTIER and FABLE; the conclusion is unchanged, being stated rather than closed |
  | sd7-slot15-callers-0930 | agrees (ACCEPT) |

- **Regression:** Database/FFXII TZA/_index/candidates/ov58d-pointer-flow-0930/ov58d_mirror.py and the three records'
  own checkers. SWE2-AUDIT-SPEC re-ran them and they reproduced (run verified at 4dfe4a006). None of these edits changes
  a computed value.
