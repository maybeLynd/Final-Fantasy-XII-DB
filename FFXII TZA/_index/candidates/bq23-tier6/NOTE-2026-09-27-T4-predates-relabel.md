# Note on `bq23_tier6.py` T4 (FABLE, Claude Opus 5.5, 2026-09-27)

`bq23_tier6.py` selects its population by the `CxxStandardLibrary.*` labels in `Database/Tools/work/graph/functions.tsv`.
That file is untracked, generated data. After this control ran, SWE2-EC7 relabelled the 18 EASTL rbtree members to
`EASTL.OrderedContainerRuntime.*` (`FRONTIER-REQ-SWE2-EC7-EASTL-RBTREE-RELABEL`), which is the change this record asked
for.

A re-run now prints T4 as **FAIL** with `OrderedContainerRuntime {unmatched: 9, MSVC: 3}`. That is the relabel, not a
regression.

The receipt stays as run. The current-state control is
[`../bq23-tier6-b/bq23_ordered_residue.py`](../bq23-tier6-b/bq23_ordered_residue.py), whose V1 asserts the relabel
(18 / 12).
