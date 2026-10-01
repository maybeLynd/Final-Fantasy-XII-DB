# Consumer check: interior citations on the world-tick page (OPUS, 2026-10-01)

A new OPUS section adds 125 interior citations. Two of its rows state what the bytes show where an earlier line of the
page says otherwise (`001EC690` increments, not reads, `01F832C4`; `0051E800` stores 0, not 1, at `+0x128`). The two earlier
lines are corrected in place (struck, with a dated note) by `worldtick_corrections.py`, which re-reads `001EC690`,
`0051E809` and `0051E849` in the image first.

- **Corrects:** the mode-2 skip-conditions row's "`01F832C4` flag read" (`001EC690` increments it) and the `0051E800` / `0051E840`
  row's "set `+0x128` `=1`" (`0051E800` stores 0, `0051E840` stores 1).
- **Affected:** 00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's new OPUS interior-citation section | revised-here |
  | the page's mode-2 skip-conditions row (`001EC690`) and the `0051E800` / `0051E840` row | revised-here (`worldtick_corrections.py`, FAILS 0) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-worldtick-interior-1001/worldtick_interior.py (re-decodes all 435 anchors; FAILS on any mismatch) and worldtick_corrections.py (checks the three instructions).
