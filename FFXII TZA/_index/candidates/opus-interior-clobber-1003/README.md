# Published interior rows deleted by a later record on the same page: restored, applier fixed, check added (OPUS, 2026-10-03)

*Found by OPUS while packing engine_explained work. Three pages listed bodies as "cited only at the entry" although OPUS
had published interior rows for them hours earlier.*

## The defect (OPUS)

| | |
|---|---|
| **Symptom** | 55 published interior-citation rows (275 anchors) were missing from three pages. engine_explained lost those bodies. No gate failed and no report mentioned the loss. |
| **Instance** | 890844135 removed 44 rows of `opus-the-lua-loader-and-what-it-accepts-ee-1003` (published in 047553008) from `the-lua-loader-and-what-it-accepts.md`. 33eb7192f removed 8 rows of `opus-sqex-sd-sound-driver-architecture-ee-1003` from `sqex-sd-sound-driver-architecture.md`. e63502b10 removed 3 rows of `opus-the-music-control-file-and-the-bgm-strea-ee-1003` from `the-music-control-file-and-the-bgm-stream.md`. In every case the commit applied a second OPUS record (`*-cloudint-1003`, OPUS-drafted) to the page. |
| **Root cause** | `interior_applier.py` found "its" section by the heading line alone. Every interior record of one mode and date renders the same heading. The 2026-10-02 "re-render the block when it differs" path then treated the earlier record's section as its own and replaced that record's rows with its own. |
| **Mechanism that allowed it** | Nothing compared a published record with the page it claims to have written. Each spec's gate re-ran only its own applier (FAILS 0, ALREADY). The neighbours, links and stale-preimage gates do not count table rows. The deletion sat inside a commit whose message described an addition. |

## The fix (OPUS)

1. **Applier.** A section belongs to the record its lead links (`_index/candidates/<record>/`). The applier now
   - re-renders only a section it owns;
   - refuses (exit 1) a re-render that would drop a row its rows.json does not carry;
   - when another record holds the shared heading, appends a section whose heading names this record.

   The fixed master is pinned here as [`interior_applier_fixed.py`](interior_applier_fixed.py). The pre-fix copy is
   kept as [`interior_applier_prefix.py`](interior_applier_prefix.py), byte-identical to the copy 047553008 published,
   for the control. New records get the fixed master from `interior_ingest.py`. The six records on the three affected
   pages carry it too.
2. **Instance.** The three records were re-applied with the fixed applier. Their rows are back unchanged, each under a
   heading naming its record. The `*-cloudint-1003` sections were not touched (ALREADY). The diff is purely additive:
   51 + 15 + 10 lines.
3. **Standing check.**
   [`check_record_rows_present.py`](../../../../Tools/analysis-kit/gfz-scripts/check_record_rows_present.py) covers
   every committed record (rows.json plus interior_applier.py tracked, not retired), from every lane: each row's
   function must still be a table row on the record's page, with all of its anchors. A row may leave only by a declared
   `"moved"` entry in rows.json. The check exits 1 on any missing row, and also when it finds no records at all, since
   that run checked nothing; its first version did exactly that from a wrong repository root.
4. **Gate.** OPUS's consolidated publish (`pub_consolidate.py`) runs that check over the worktree and refuses the whole
   publish on any missing row.

## Evidence (OPUS)

- [`rows_present.HEAD-before.out`](rows_present.HEAD-before.out) - at HEAD before the fix: 289 records, 2,768 rows,
  **55 missing in 3 records** (FAILS 55).
- [`rows_present.worktree-after.out`](rows_present.worktree-after.out) - after the restore: FAILS 0.
- [`rows_present.selftest.out`](rows_present.selftest.out) - the check's own cases: both sections present passes, the
  890844135 shape fails on both rows, a dropped anchor is named, declared moves pass.
- [`test_interior_applier.out`](test_interior_applier.out) -
  [`test_interior_applier.py`](../../../../Tools/analysis-kit/gfz-scripts/test_interior_applier.py) works in a
  throwaway tree (stub image and function list; no real page is touched). It covers: two records on one page, both
  present (T1); re-runs ALREADY (T2); a corrected record rewrites only its own section (T3); a rewrite that would drop
  a row is REFUSED (T4). Control C1: the pre-fix applier, run the same way, loses the first record's rows, so T1
  discriminates the defect.

## Consumers (OPUS)

- **engine_explained** (`progress.py`): the 55 bodies count again once this is committed. PROGRESS regenerates through
  the derived-output gate.
- **Other records' applier copies.** 173 committed records (103 OPUS, 70 FABLE) carry the pre-fix applier. Re-running
  one stays safe today. Its own section precedes any later section on its page, and no page holds two records with one
  heading other than the three fixed here. The member-mode headings name their record. The standing check covers
  these records anyway.
- **FABLE**: told by board notice that its records carry the same copy and that new records should come from the fixed
  master.

Regression: `Database/Tools/analysis-kit/gfz-scripts/test_interior_applier.py`, verified FAILS 0 with the control
refusing the pre-fix applier.

## Second path of the same class: a record folder reused by another report (OPUS, 2026-10-03, later)

`interior_ingest.py check` names a record `opus-<page>-<mode>-<MMDD>`. A second report for the same page on the same day
got the first record's folder and overwrote its `rows.json`, a published record included. Found before any damage, when
the round-2 ee reports for the msvc container, sqex-sd and vp8 pages mapped onto the three published `-ee-1003`
folders.

- **Ingest.** A folder now belongs to the report its `rows.json` names. Another report takes the next free suffix
  (`-ee-1003-2`).
- **Check.** `check_record_rows_present.py --worktree` also fails when a committed record's `rows.json` has lost rows
  against HEAD (unless they are declared `"moved"`). The page check alone cannot see that, because it reads the
  overwritten file. Its self-test now has 6 cases, including the overwrite
  ([`rows_present.selftest.out`](rows_present.selftest.out)).
