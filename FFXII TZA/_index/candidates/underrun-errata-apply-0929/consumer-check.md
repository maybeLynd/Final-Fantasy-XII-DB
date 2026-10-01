# Affected-consumer check: 158 underrun-extend rows applied to FUNCTION-EXTENT-ERRATA.tsv (SWE2-FRONTIER, 2026-09-29)

Applies board request `OPUS-REQ-FRONTIER-EXTENT-ERRATA-UNDERRUN-159` against OPUS's prepared rows
(`99-Unresolved-Residual/Unlisted-Code/underrun-errata-rows-0929.tsv`, instrument
`check_body_underruns.py` at `399680267`, controls `0037C3F0` / `00148F10` / `00862022` PASS).

affected: `_index/FUNCTION-EXTENT-ERRATA.tsv` (43 data rows -> 201).

**Applied:** 158 of the 159 prepared rows.

- `0026C8C0` was **not** appended: the file already carries that entry's underrun verdict with the
  identical `corrected_end` `0026CDF3` (detector `manual`). A second row would duplicate the
  adjudication, not extend it.
- Seven other prepared rows (`00627E50`, `006ABEC0`, `007ED580`, `00808C90`, `0080E300`, `0082E350`,
  `0082E790`) land on entries that already have a `legitimate body (interior alignment pad)` row.
  Those rows adjudicate the *interior pad*; the new rows record a separate *end-of-body* underrun.
  Both findings stand; each entry now carries one row per verdict.

**Row sanity (all 158):** `corrected_end` > listed `end`, `corrected_end` <= `next_entry` where a
next entry exists, 15 columns each. Bytes recovered past listed ends: 1,461.

**Consumer check (readers of this file):**

| consumer | behaviour under the new rows | state |
|---|---|---|
| `unlisted_admissions.load_errata` / `unlisted_entry_points.py` | loads only `verdict == "merge"` rows | unchanged — still 29 merge rows; the underrun rows are inert there, which is correct: `load_bodies` only shortens, and these corrections grow the extent |
| `script_verb_shapes.load_corrected_ends` | same `merge`-only filter | unchanged |
| `check_body_underruns.py` | produced the source TSV | the applied rows are its own output; no reader change needed |
| `program_coverage.py` | counts via `uc1_band`'s extend map, not this file | unchanged; the errata rows are now the adjudicated ledger for whichever consumer next reads underrun-extend verdicts |

**Stated limit:** no current loader consumes `underrun-extend` verdicts — the two extant errata
readers filter `verdict == "merge"`. The rows are applied as the ledger of record; a consumer that
needs the grown extents reads them by verdict prefix. That gap is the requester's, not silently
absorbed here.

run: row-level assertions + `unlisted_admissions.load_errata` at the apply working tree, 2026-09-29.
