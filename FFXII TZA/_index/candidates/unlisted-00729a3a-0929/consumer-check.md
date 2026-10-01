# Consumer-check record — 00729A3A resolved; IMUL290 count annotated (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md`
affected: `_index/candidates/uq218-cm-entry-residues/notes.md`

## Changes

1. The unlisted-code page's classification of the fourteen exception-directory orphans listed one record, `00729A3A`,
   as unclassified. OPUS showed (`624e3534e`, the fragment-size sweep) that it is the third chained fragment of the
   listed `00729920`. The row and the "did not resolve it" sentence are struck, and the resolution is added beside them.
2. FABLE's UQ-218 @FTR record said "71 functions stride 0x290". OPUS's CON-181 (`ee21b57cb`) measured 55 that multiply
   an index by 0x290 and 16 that carry it as a frame size, a size argument or an offset. The count is annotated in
   place (notes.md and its companion ftr.tsv row). The bone-record naming rests on the Skeleton_* bodies, not on the count, so no conclusion changes.

## Consumers

- `_index/candidates/fragment-size-sweep-0929/README.md` (OPUS) already states the resolution. It agrees and is unchanged.
- `_index/progress/crosswalk.md` lists the notice as a request; it is generated and refreshes from the board.
- The ftr-node-table falsification record (OPUS) states 55 already. It agrees.
- No other page states that `00729A3A` is unclassified (grep of the address over the database).

## Regression

pdata_chain_check.py (this folder, output pdata_chain_check.out): P1 checks that both later records chain to
`00729920`'s primary record, with the primary record's unchained flags as the control; P2 checks the jump-table dispatch
and that the default arm lands inside the fragment. The count annotation's regression is OPUS's
falsify_ftr_node_table.py N10.

run: pdata_chain_check.py at 6facc53bc (HEAD when it ran), P1 and P2 pass, FAILS 0
