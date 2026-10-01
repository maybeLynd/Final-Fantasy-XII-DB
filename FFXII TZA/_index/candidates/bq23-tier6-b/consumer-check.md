# Affected-consumer check: BQ-23 ordered-container residue matched (FABLE, Claude Opus 5.5, 2026-09-27)

affected: none edited here - _index/OPEN-QUESTIONS.md BQ-23 is narrowed; two SWE2-EC7 notes that disagree and the label change are routed to SWE2-EC7
run: bq23_ordered_residue.py at de6d5ed1b (worktree = that HEAD plus this package), 4 checks FAILS 0; V4 is the MSVC sensitivity control.

| consumer | what it said | state |
|---|---|---|
| _index/OPEN-QUESTIONS.md BQ-23 | 9 OrderedContainerRuntime members unmatched | revised-here: 7 EASTL subtree routines + 2 Phyre packed-colour tree; still PARTIAL (allocator 9, regex 21) |
| `Database/Tools/work/graph/functions.tsv` (derived labels, SWE2-EC7) | the nine carry `CxxStandardLibrary.OrderedContainerRuntime` | routed: request to SWE2-EC7 to extend the EASTL relabel to the seven and to relabel the two as Phyre |
| `_index/candidates/bq23-tier6/bq23_tier6.py` (FABLE receipt) | T4 partition by the old labels | receipt unchanged; dated note beside it explains its T4 FAIL after the relabel |
| `22-Middleware-PhyreEngine/Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md`, SWE2-EC7-52 update | `0067F9D0` "MSVC `_Tree` shape" | **disagrees**: MSVC `_Tree` keeps `_Color`/`_Isnil` as bytes `+0x18`/`+0x19`; `0067F9D0` packs the colour into bit 0 of the parent word at `+0x10` (V3). Routed to SWE2-EC7 (owner of the note) |
| `16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md`, SWE2-EC7-44 update | `001FC770` "two `call [rax+0x10]` vcalls, no direct calls" | **disagrees in part**: it also calls itself (`call 0x1fc770`), EASTL DoCopySubtree's recursion (V2). Routed to SWE2-EC7 |
| `23-Third-Party-Libraries/EASTL` pages | EASTL map/set in use | agrees; not revised |

Regenerated with it: nothing.
