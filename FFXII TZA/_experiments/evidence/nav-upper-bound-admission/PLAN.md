# Navigation point-query upper-edge admission

Question: does original `00383F10` reject or clamp points exactly at
`origin + cellSize * count`, or admit equality and read a cell outside the
intended row/table? Consumers: FABLE navigation dataset/search page and OPUS
navigation/corridor input preconditions. Existing EXP-131 ran interior, origin,
NaN and beyond-bound cases; its retained case list has no exact upper-edge case.
Do not replay its full campaign or modify its files.

Hypotheses: H1 equality rejects or clamps to the last cell; H2 original JA
bounds admit equality and unguarded row*cols+col addresses the next row or
beyond the declared table. A proves the branch/index recipe. B is chosen to
test actual read ordering, returned region dependence and fault detection under
controlled placement, rather than treating a Python model as the oracle.

Reuse EXP-131's World/synthetic mesh, retaining that exact helper. Execute full
shipping GGRID, BASE and TTEST bodies; disclose the existing `_fdclass` import
stub, planted root/base/mesh and table placement. Finite coordinate cases only.
Use correct x64 entry stack alignment, MXCSR=1F80, nonvolatile sentinels and a
2,000-instruction budget. Observe actual cell reads at validated `0038402C`;
retain PCs, access addresses, bytes and actual returns/faults.

Controls: known inside/origin points, adjacent f32 values below/above upper
bounds, next-row cell-list intervention with geometry unchanged, and a declared
eight-cell table placed exactly before an unmapped guard. Interior final cell
must remain readable; equality faults must identify the same cell-read site.
Two original-byte-asserted JA->JAE disposable mutations test each upper-bound
discriminator. They are regression controls, not altered reference files.

Accept only nonempty completed controls with exact binary/helper identity,
full body/RET coverage, aligned ABI and observed addresses/returns, or precise
expected guard fault. Invalid/truncated/stub-call ambiguity stops acceptance.
No live crash, normal reachability, asset layout prevalence, allocator placement,
native CRT effect or universal map-boundary claim. Ordinary game ownership,
initialization and scheduling remain unobserved.

Cleanup: isolated process exits, no native game attach/control; saves/config and
reference binary untouched. PC OFF. Whole accepted L1+L2/independent final reviews
remain the goal, not case growth; persistent S19 setup limit unchanged.

Supplement: original equality question settled by the retained14 controls. Do not
repeat them. A distinct precondition weakness is finite SUBSS rounding with a
negative origin: could x<upper still give truncated distance==span? Use three new
B cases, origin-32768/cw255/cols255/lastrow, 510 valid empty cells ending at guard.
Observe XMM1 before/after SUBSS and index/read/fault; interior and two-ULP-below
controls must pass. Falsify the proposed strict-world-bound sufficiency; require
computed indices in range instead. Preserve old prose/check/verdict, correct
producer/checker/README and the existing three owner/reviewer returns. No live
setup or authored-data recurrence claim; actual MXCSR1F80 is controlled, not live.
