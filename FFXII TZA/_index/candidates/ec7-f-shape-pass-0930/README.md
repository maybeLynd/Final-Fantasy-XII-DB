# F-shape selector pass on the repaired frontier (SWE2-EC7, 2026-09-30)

*Answers OPUS-NOTICE-EC7-F-SHAPES-0930 (acknowledged earlier, run now that the DD A-drift repair is closed). The pass
re-runs every committed family selector on a clean export of `89d1a685a`, after the repair. Admissions are applied
only under FABLE family ruling R3: the committed selector, frontier bodies, no removals, count and file moving
together.*

## 1. The frontier by shape (SWE2-EC7)

[`fshape_clean.py`](fshape_clean.py) applies OPUS's `f_shapes.bucket` to `check_dispositions`' own frontier on the
clean export, not to the dashboard facts. Rows are in [`fshape_before.tsv`](fshape_before.tsv).

| bucket | listed | UC-1 |
|---|---:|---:|
| larger (> 64 B) | 2,811 | 17 |
| small (<= 64 B) | 1,633 | 24 |
| tiny-leaf | 147 | 6 |
| forwarder | 117 | 8 |
| getter-leaf | 4 | 0 |
| jmp-thunk | 1 | 4 |
| **frontier F** | **4,772** | (59 of the 4,772) |

OPUS's census counted about 930 shape candidates at 6,250 frontier. 269 non-UC-1 candidates remain (147 + 117 + 4 + 1).
The C2 admissions and the selector re-runs since then absorbed most of the rest.

## 2. What the committed selectors admit now (SWE2-EC7)

52 selectors re-run with `--write`; every Phyre module is included.

| outcome | selector / family | bodies | action |
|---|---|---|---|
| R3 admission | `select_explained_callee_adapters.py`, NativeAdapter.ExplainedCalleeForwarder 482 -> 483 | `0036E310` (forwarder) | **applied** |
| R3 admission | `select_documented_global_leafs.py`, NativeLeaf.DocumentedGlobalAccessor 222 -> 224 | `0024F780` (tiny-leaf), `003F4670` (small) | **applied**; count guard 222 -> 224, only that line edited (the R3 precedent) |
| admission, held | `select_descriptor_siblings_2.py`, Phyre shared-runtime identity dispatch adapters 6 -> 8 | `005CA2D0`, `0060F350` | **held**: `005CA2D0` is one of the 91 PAnimation cascade bodies, which the pending Phyre ruling returns to PAnimation |
| not R3 | `select_frontier_form_clusters_2/3/4.py`, nine NativeAdapter form rows | 15 "admissions" | **not applied**: 11 are already NativeAdapter.ExplainedCalleeForwarder members and 2 NativeLeaf.DocumentedGlobalAccessor members (collisions); the other 2 are UC-1 bodies. Those selectors' pools are not frontier-only, which is EC7 follow-up work |
| orphan file | same selectors, `nativeadapter-callboolnormalizereturnsete.tsv` 5 -> 2 | `002DEBB0`, `002E05C0`, `004735E0` | **not applied**: no page declares this file (it is not a family row), and the three dropped bodies are A-measured |
| report file | `select_xc_array_clusters.py`, `xc-initializer-leftovers.tsv` 83 -> 24 | | an information file, not a family row; not applied |
| guard fails | `select_guarded_class_registrars.py` (twin assert, `005B2860`), `select_scalar_conversion_registrars.py` (a form hit is A-measured), `select_static_init_form.py` (group counts drifted) | | no write taken; the first is the accounting-defined family routed to FABLE |

**Result:** 3 bodies admitted, so F falls 4,772 -> **4,769**. Measured on the clean export of `89d1a685a` with these
files: rows refused 0, family forms MISMATCH 0. Each re-run reproduces its file (fixpoint).

## 3. What the shape census does and does not support (SWE2-EC7)

Of 269 shape candidates, the committed families admit 2 (the tiny-leaf `0024F780` and the forwarder `0036E310`).
The other 267 meet no existing family's bar. Size and shape are not a disposition; each body still needs a family
whose predicate it meets, with its own controls. Admitting them needs **a new family declaration**, not a selector
re-run, so it is new EC-7 work. It comes after FABLE's rulings on the Phyre scope and on the two accounting-defined
families, because both change which bodies are frontier.

run: all selectors on a clean export of 89d1a685a (this record's figures).
