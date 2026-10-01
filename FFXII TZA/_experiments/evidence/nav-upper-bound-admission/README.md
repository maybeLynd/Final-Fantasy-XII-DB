# Original navigation query admits exact upper edges

**B — isolated original instructions, synthetic fixture; live=false.**
Exact shipping image SHA
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Full bodies: GGRID `00383F10` 542 B, BASE `0020E600` 10 B,
TTEST `00382D10` 391 B. Raw bodies, disassembly, tool/helper identity,
original import descriptor and planted state are in `source.json`.

## Question and result

Competing explanations: the query rejects/clamps a point exactly at a grid's
upper limit, or admits equality and calculates an out-of-row/table index.
The original upper checks at `00383FAF` / `00383FCD` are **JA**, not JAE.
Equality reaches the signed division and unguarded cell-word load at `0038402C`.

Reused EXP-131's disclosed synthetic grid: origin (0,0), 2x2 cell dimensions,
four columns, two rows, eight declared cells, rectangle 8x4. No application
body is stubbed. The sole imported `_fdclass` predicate is the existing host
stub, bound to the shipping IAT `008C2C10`; native CRT effects are untested.

| Controlled input/state | Actual observation |
|---|---|
| (0,0), (1,1) | Cell 0 read; region 0 returned |
| X one f32 ULP below 8, Z=0 | Cell 3 read; region 2 returned |
| X=8, Z=0 | **Cell 4, the next row's first cell**, read; no region (255) |
| Same point, only cell 4's list offset changed 9 to17 | Cell 4 read; **region 3** returned through the real triangle test |
| X one ULP above8 | Rejected255 before any cell read |
| Table ends at an unmapped guard, (7,3) | Last cell7 still readable; region3 returned |
| Same placement, X=8,Z=3 or X=1,Z=4 | Index8 read attempted at `40100000`, fault at `0038402C` |
| Same placement, X=8,Z=4 | Index12 read attempted at `40100008`, same fault site |
| Z one ULP below4 / above4 | Below: cell4 read, region1; above: rejected255 without cell read |
| Each disposable upper JA->JAE mutation | Corresponding equality rejected255 before cell read/guard fault |

For positive cell dimensions/counts, source arithmetic explains the result:
X equality yields col==cols; a non-last row aliases the following row's first
cell. Z equality yields row==rows, beyond the declared cell table. There is no
clamp or subsequent index/count check before the word load. This is an original
query precondition/edge consequence, not an observed original-game failure.

## Controls and raw evidence

`raw.json` retains all14 cases, points/header/table bytes, actual PCs, cell reads,
stub calls, return/fault positions, registers, instruction counts and ABI state.
Correct x64 entry RSP modulo16=8, MXCSR1F80, and nonvolatile sentinels; completed
calls restore sentinels and return stack. All runs stop within2,000 instructions.
Guard faults are deliberate fixture observations, **not returns**: residual RAX
8/12 is the current index, never a semantic return or a live crash. The positive
last-cell control proves access/detection up to the exact guard boundary.

`check.py` rejects zero/incomplete cases, wrong source/import bytes, unexpected
PCs, read sites/addresses, mutated gate identities, register/return mismatch and
failed positive controls. 12 unmodified cases plus2 disposable mutations pass.
No full historic campaign was replayed; shared EXP-131 evidence is unchanged.

Initial capture used `executed-driver.py`. That exact initial driver was recovered
by reversing the later metadata-only source/import enrichment patch and hashed
after capture, **not** by a pre-run immutable hash receipt. The source enrichment
ran with `--identity-only`, preserving the raw observations without recapture.
The final `probe.py` can reproduce them in a disposable copy and records its own
hash before fresh cases. Consumers/reviewers should assess this identity limit.

## Interpretation, limits, consumers

FABLE's navigation page §2 should state inclusive upper admission and its table
edge consequence, rather than implying all admitted rectangle points have a
valid cell index. OPUS query/contract preconditions must ensure the **computed
cell indices** are within the declared counts. Strict world-coordinate upper
bounds alone do **not** suffice: the negative-origin supplement below falsifies
that proposed rule. Adjacent floats and next-row candidate dependence are shown.
This does not establish whether ordinary callers produce those exact points.

No authored-area prevalence, native allocation/placement, live initialization,
normal reachability, scheduling, import effects, fault manifestation in the real
process, malformed zero cell sizes, exceptional-float campaign or all-engine
coordinate convention is claimed. FABLE/OPUS incorporation and independent
SPEC acceptance remain pending. No source reconstruction phase was started.

Cleanup: Python isolated run exited; no native game launch/attach/input/control,
reference writes, save/config changes or instrumentation. PC OFF; no new live
cleanup receipt. Whole accepted L1+L2 and prerequisite-gated final audit NOT_MET.

## Correction before publication: strict world bounds are insufficient

The initial README proposed strictly lower world-coordinate upper bounds as a
safe-table precondition. That was an unsupported generalization from the first
fixture; `historical-incomplete-precondition/` preserves the rejected wording,
checker/validation/manifest and correction receipt. Initial14 raw observations
remain valid and unchanged. No canonical consumer had accepted this package.

Three **new**, finite, narrowly targeted original-code cases (not a rerun of the
first14) use a positive header: originX=-32768, cellW=255, cols=255, cellH=2,
rows=2. UpperX is exactly32257. The510-word table contains FFFF empty cells and
ends at an unmapped guard; Z=3 selects the last row.

| X input | Actual SUBSS distance before CVTT | Actual table access |
|---|---|---|
| 0 | 32768 | Index383, readable empty cell, returns255 |
| 32256.99609375 (two ULPs below upper) | 65024.99609375 | Last index509, readable empty cell, returns255 |
| 32256.998046875 (one ULP below upper) | **65025.0** | Index510, guard fault at38402C |

All three X values are strictly below the upper world bound. At MXCSR1F80 the
last subtraction rounds its exact midpoint distance up to the whole span65025.
CVTT then gives65025 and IDIV255 gives col255, despite X<upperX. Actual XMM1
bits before/after SUBSS (`0038401C` / `00384020`), table reads/fault site and
positive controls are retained in `supplement-source.json` / `supplement-raw.json`.
The supplemental driver hash is recorded **before** cases. This fixture does
not claim authored-header occurrence or the live game's MXCSR/allocator state.

The sufficient local table-index precondition is positive nonzero cell sizes,
valid declared table storage, and the original computed col/row each in their
declared range. Source world-coordinate bounds do not enforce it. This is a
caller/data-domain obligation unless a reconstruction deliberately changes
behavior. Independent review must include the correction, not merely accept
the older14-case verdict. Owner/SPEC requests remain the existing three routes.

## Packaging failure and producer repair

The private freezer initially excluded every file named `manifest.json`, omitting
the nested historical manifest after the correction history was added. Explicit
publication-pin preparation rejected that incomplete set before publication.
`historical-manifest-omission/` retains the exact bad freezer, rejected manifest,
actual preimage file list and missing member. The producer now excludes only the
root manifest; `check_manifest.py` requires exact nonempty file/member coverage,
all bytes/hashes and the observed omission regression. No prior committed package
or original-code observation was altered; acceptance requires both checkers.
