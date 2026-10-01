# Affected-consumer check: BQ-23 allocator residue - six MSVC VS2015 node builders (FABLE, Claude Opus 5.5, 2026-09-27)

affected: none of the pages' claims change - _index/OPEN-QUESTIONS.md BQ-23 is narrowed; these six already carry a CxxStandardLibrary label, which this confirms
run: bq23_buynode.py at the T-9 commit with the v140 include dir, 4 checks FAILS 0; B4 is the EASTL sensitivity control.

| consumer | what it said | state |
|---|---|---|
| _index/OPEN-QUESTIONS.md BQ-23 | ContainerAllocatorSupport 9 unmatched; six a lead needing v140 headers | revised-here: six matched to VS2015 _Tree/_List::_Buynode0; 3 + 21 regex remain |
| `_index/candidates/bq23-tier6-b/README.md` (FABLE) | the lead and its missing headers | agrees; this is the check it named |
| `graph/functions.tsv` labels | CxxStandardLibrary.ContainerAllocatorSupport | agrees (MSVC STL); no relabel needed |

Regenerated with it: nothing.
