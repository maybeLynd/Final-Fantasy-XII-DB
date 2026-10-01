# FRONTIER-RT-DATA-CENSUS-REDERIVE — row dispositions (SWE2-DATA)

SWE2-DATA, 2026-09-27. Control: `census_rederive.py` beside this file (C1–C5 checks, FAILS 0).
Dumps compared: `Database/Tools/work/graph_gn/functions.tsv` (2026-09-02, the baseline AC-6 names)
vs `Database/Tools/work/graph/functions.tsv` (2026-09-27 fresh dump). Shipping EXE sha256
`73461D08…721F8`; Ghidra image base `0x00120000` already included.

## AC-6 — re-derive every functions.tsv census against a fresher dump: EXECUTED

**Cell-level delta (38,161 rows, identical address sets):**

| column | changed cells | what changed |
|---|---|---|
| `entry`,`name`,`owner`,`final_no_owner`,`thunk`,`noreturn` | 0 | — |
| `body_bytes` | 1 | `0057FE80` 2105 → 2360 (re-analysis grew one body) |
| `comment_len` | 158 | comments imported since 2026-09-02 |
| `tags` | 176 rows | a `GFZ.V121.CodeDomain.*` retag pass; removed tags are all `CodeDomain.CxxStandardLibrary.OrderedContainerRuntime.*` (18 rows, renamed to `CodeDomain.EASTL.OrderedContainerRuntime.*`); added tags are new V121 CodeDomain classifications (155 distinct) |

**Consumer audit (396 in-database scripts reading functions.tsv):**

- No consumer reads `comment_len`. → the 158 comment changes cannot move any census.
- No consumer names `0057FE80`. Only a selector that *includes* the row and sums `body_bytes` could move; the row's tags are `CodeDomain.Boundary.SaveLoad.NativeSupport` + audit tags, and no published census selects that namespace for a size claim.
- Tag-column selectors that intersect the delta (BO-2 sweep below): **`bq23_tier6.py`** loses the 18 `CxxStandardLibrary.OrderedContainerRuntime` rows — re-run under the fresh dump its T4 partition check FAILS (`OrderedContainerRuntime` drops from `{EASTL:18, MSVC:3, unmatched:9}` to `{MSVC:3, unmatched:9}`), which is the re-derivation made concrete: the ledger retag settled what the census was measuring. And **`select_documented_global_leafs.py`** gains two `NativeLeaf` rows (`NativeLeaf.AccessorForwarder`, `NativeLeaf.InlineSIMDStateMutation`) — up to two new frontier rows pending its `a_set`/`declared` exclusions.
- All other 394 consumers re-derive identically; the delta cannot reach their selections.

## BO-2 — re-derive tag-prefix selectors in other categories' censuses: EXECUTED

Sweep of all 396 consumers found **eight genuine tag-prefix/substring predicates** against the
`functions.tsv` tags column (the rest of the `select_*` family selects on RTTI/mangled names,
vtable slot targets, or code spans — not tags):

| script | selector | delta exposure | selector class |
|---|---|---|---|
| `select_imgui.py` | seed `"DearImGui"`, CONV_TAGS convergence, edge asserts | CONV_TAGS +2 rows (`Lifecycle`, `Teardown` substrings hit new `CodeDomain` tags); asserts unaffected | seed+verify: seed feeds a population that is then checked against names/vtables — not circular |
| `select_jsonbox.py` | seed `"JsonBox"`, same CONV_TAGS | same +2 | same |
| `select_libvpx.py` | seed `"LibVPX"`, `RedBlackTree` assert | unaffected — the renamed tag still contains `RedBlackTree` | seed+verify |
| `select_mkvparser.py` | seed `"WebM_MKV"` | unaffected | seed+verify against `mkvparser::` names |
| `select_documented_global_leafs.py` | `"NativeLeaf"` | **+2 rows** | selector is the taxonomy being counted — exposure flagged |
| `select_explained_callee_adapters.py` | `"CodeDomain.NativeAdapter."` | 0 rows | selector is the taxonomy being counted |
| `bj5_residue.py` | `"Phyre.Reflection"` | 0 rows | seed |
| `bq23_tier6.py` | `"CxxStandardLibrary"` population + control exclusion | **−18 rows** | selector is the axis under test — **the pass-3 defect class**: its T4 partition is proven stale by re-run |

On the defect class: the `ThirdParty.*`-style scope defect was a selector copied from the
document under test. Six of the eight selectors are seeds whose results are verified downstream
against independently-derived evidence (RTTI strings, `mkvparser::`/`DearImGui`/`JsonBox`/`LibVPX`
name spaces, vtable slotting) — a tag edit can shift their seed set but not their conclusion.
The two exposures are `bq23_tier6.py` (selector = the measured axis; now provably stale) and
`select_documented_global_leafs.py` (selector = the taxonomy being enumerated; +2 rows).

## UQ-377 — the true unlisted-body count: EXECUTED as recount, bounded

The published splitter was reconstructed and verified against `unlisted-code-blocks.tsv`:
gap → strip `0xCC` edges → split on int3 runs that **end at a 16-aligned address** → drop
segments made of pure alignment padding (`0x00`/multi-byte-NOP encodings; all 81 over-splits in a
naive rule are exactly such segments). The reconstruction reproduces 1,442 of the 1,471 published
blocks with zero false blocks (98.0% boundary agreement; the 29 misses are single-byte blocks and
boundary-edge fragments, i.e. the rule's known recall gap, not new structure).

**Recount under the fresh dump: the residue is unchanged except one block.** `0057FE80`'s grown
body (2105→2360) absorbs the head of block `005806B9`, moving it to `005807B8` and shrinking it
379→124 bytes. Block count is stable (1,442→1,442 in the reconstruction; the published census
moves identically: one block relocated and shrunk, total ~244,364 bytes).

**On "the true count" beyond the floor:** the floor is a property of the measuring instrument
(int3/alignment splitter, recall 0.926), not of the dump — re-deriving against any dump cannot
raise it. UC-5 already removed 163 truncation tails, giving ~1,308 bodies as the corrected
lower estimate; the recall bound implies the true count could exceed 1,471 by ~7% (~1,589) if the
missed boundaries all hide bodies. A point answer needs a new detector (e.g. CFG-reconstruction
or prologue voting over the residue) — that instrument is the carrier task
`FABLE-CARRIER-TOOLING-AND-CHECKER-PROPOSALS-0926`'s scope. The recount portion is executed here;
the new-detector portion is declined for DATA with that reason.
