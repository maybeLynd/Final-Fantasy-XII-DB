# Register rows split by literal pipes (FABLE, Claude Opus 5.5, 2026-09-28)

affected: PS-1, BI-13, UQ-210, UQ-218, UQ-242, UQ-255 (register rows)

**The defect.** A literal `|` inside a row's text splits the row into extra cells, as in `(generation << 8) | index`,
`|b − a|` or `|frpan|`. A reader that takes the row's last cell then gets a fragment of text instead of the status.
UQ-242's last cell read "x pi/2)`: at 1 the sound…", UQ-255's read "0x40`, else verbatim)…", and BI-13's read "index`**
with a 24-bit generation…".

**The repair.** [`escape_rows.py`](escape_rows.py) ([output](escape_rows.out)) escapes each such pipe as `\|`.
- Nothing else in the text changes. Each repaired line equals the original when `\|` is read back as `|`, and the
  script refuses otherwise.
- Each repaired row has its table's 3 cells, with a status cell that starts with a verdict word.
- The cell groups are fixed per row in the script. The script refuses any row it has no rule for, and does not guess.

**The scan.** [`cell_count_scan.py`](cell_count_scan.py) ([output](cell_count_scan.out)) lists rows whose cell count
differs from their table's column count. Its `--self-test` plants one split row and one escaped row, and must flag
exactly the first. Verified at 996166340: 42 rows before this repair, 36 after.

**Not repaired here: 36 rows.**
- 32 have 2 cells: the question and status are not separated by a pipe on the row's own line. Some rows continue
  onto following lines without a leading `|`; in others the separator was written escaped. A mechanical repair would
  have to guess which text is the status, so the script refuses them.
- 4 have 4 cells and no fixed rule: BF-4, BI-3c, UQ-220 and UQ-247.
- They are routed to FRONTIER, which owns the register format, with this scan as the check.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` six rows | pipes escaped; text and verdicts unchanged | revised-here |
