# The F jump after the 2026-09-30 DD re-statuses: every moved body paired with its cause (SWE2-EC7)

*SWE2-EC7, 2026-09-30. Request `SWE2-EC7-REQ-OPUS-DD-ADRIFT-PAIRING-0930` (pairing agreed with OPUS),
`OPUS-REQ-EC7-A-DRIFT-REFUSALS-2-0930`, `OPUS-REQ-EC7-A-DRIFT-PAIRING-SHAS-0930`.*

## 1. What moved F, and what did not

The goal gate's F family reads `check_dispositions.py`'s frontier: census bodies that are neither A-measured nor
members of an accepted family row. A row is refused whole when one member is A. A DD re-status to DOCUMENTED makes
the page evidence-bearing, so each interior citation on it makes the cited body A. The row holding that body is then
refused, and all its other members count as frontier.

Measured on a clean export of HEAD `06c849caf` (DB and kit from `git archive`, short root, `fbucket.py`, which uses
`check_dispositions.evaluate` itself), against a clean export of `50890aa7f`, the commit before the first re-status:

| | base `50890aa7f` | HEAD `06c849caf` |
|---|---:|---:|
| frontier (F) | 4,765 | 9,955 |
| A | 9,455 | 9,538 |
| rows refused | 0 | 12 (all "already measured as A") |

The 9,955 bodies at HEAD split into:

| bucket | bodies | kind |
|---|---:|---|
| members of the 12 A-refused rows | 5,227 | **linkage drift**: the body's family accounting is unchanged, but its row is refused because another member became A |
| declared by no row | 4,728 | the frontier that existed before: base 4,765 less 37 bodies the re-statuses made A |
| members of rows refused for any other reason | 0 | |

**Semantic loss: 0.** No body that was A at base has stopped being A (A lost 0, A gained 83), and every body that is
frontier at HEAD but was not at base is a member of an A-refused row. Nothing lost its own accounting. The +5,190 is
entirely rows refused whole.

## 2. Pairing: each re-status commit, the bodies it made A, the rows it refused

[`pairing.tsv`](pairing.tsv) has one line per A member of a refused row: row, body, the citing page, the interior
cite, the cause, and the first commit after base where the page is evidence-bearing and carries that cite
([`pairing.py`](pairing.py)). **Every cause is a page re-status**: no interior cite was added to a page that was
already evidence-bearing. One cite (`how-a-path-is-resolved-to-bytes.md`, inside PhyreCore's `0020C610`) was added by
SWE2-CONTRACT's DD batch 8 and became evidence with the page's re-status.

| re-status commit (OPUS) | page(s) | A members -> row |
|---|---|---|
| `3dac81ee9` | MSVC ordered-container runtime | 8 -> PPFX post-effect library (OPUS repaired its own MSVC/EASTL tree rows in `3a97cebda`) |
| `46c98f222` | animation channel binding | 8 -> Phyre PAnimation, 2 -> Phyre PhyreCore, 1 -> counter-append initialisers |
| `e696ef86e` | save-image buffers | 1 -> zlib 1.2.11 |
| `d46835689` | reflected render parameters | 4 -> Phyre PPostProcessing |
| `d39c8ccbd` | two SEAD architecture pages | 4 -> SQEX SEAD span |
| `8c8406bfd` | EASTL strings; version stamps | 2 -> SEAD, 1 -> JsonBox, 1 -> ExplainedCalleeForwarder; 1 -> ScriptVM.VerbAdapter |
| `9bda44687` | CL2 menu colour tables; source-block mover | 1 -> JsonBox; 1 -> ScriptVM.VerbAdapter |
| `2db6cdb59` | what-each-script-verb-touches | 1 -> NativeAdapter.CallResultTailCall |
| `30f461a92` | how a path is resolved to bytes | 1 -> Phyre PhyreCore, 2 -> Phyre PSerialization |

The other DD commits of the day (`c858cde2b`, `ad15f4c42`, the drawing-context and widget-draw pages in `e696ef86e` /
`d39c8ccbd`, and the non-OPUS DD content batches) made no family member A.

## 3. The repair, and what it cannot re-point

For each refused row: the A members are removed from the members file, and the row's selector is re-run on the clean
export where one exists (it excludes A by design). Where no selector exists, or it cannot run, the removal is exact.
Order matters. The exact removals come first, so every row is accepted before any selector runs. A selector that reads
the live frontier would otherwise see the other refused rows' 5,000 members as frontier.

- Re-run, and each reproduces the exact removal: PPFX (`select_ppfx.py`), SEAD (`select_audio_libraries.py`, its five other
  library files unchanged), ScriptVM.VerbAdapter (`select_verb_adapters.py`, leftovers membership unchanged), zlib
  (`select_zlib.py`), PhyreCore and PSerialization (`select_phyre_module.py`).
- Exact removal only: NativeAdapter.CallResultTailCall (a form family with no selector); counter-append initialisers
  (the named XC-array selector rewrites every cluster file); JsonBox. `select_jsonbox.py` does not run at HEAD. Its
  self-exclusion tests `parts[0] != "JsonBox"` but the row is named "JsonBox JSON library", so it treats all 55 of
  its own members as declared elsewhere. With the name matched, its closure assertion refuses the two departed bodies
  (`001FF740`, `001FFF00`) as "unexplained foreign callers", because they call members from inside the runs. Fixing
  that is selector work, not part of this repair.
- **Closure cascades: 93 bodies.** Re-running the Phyre PAnimation and PPostProcessing selectors drops 75 and 18 more
  members than the A removal. They leave because every inbound reference must come from a member, and some of their
  inbound references now come from the promoted A bodies, which are not members. **Control:** with only the promoted
  bodies held non-A, and the ExplainedCalleeForwarder file at its pre-admission state, both selectors reproduce the
  base files exactly (202 and 156). Their three module selectors also reproduce the base files at base. So the A
  promotion is the whole cause. Two of the 75 (`005AA840`, `005C7930`) are single-explained-callee adapters, and the
  ExplainedCalleeForwarder selector re-run admits them. The other 91 stay frontier ([`cascade.tsv`](cascade.tsv)).
  This is **rule-induced linkage drift**. The bodies are unchanged and so is the evidence that they are module code:
  their callers are the same bodies, now individually explained. But the exclusive-closure rule does not count an
  A-measured former member as a closure source, so re-pointing cannot keep them. Keeping them needs a ruling on that
  rule, routed to FABLE (family semantics).

After the full repair, measured on the clean export of `06c849caf` with every edit applied: **F = 4,819** (4,728
undeclared + 91 cascade), rows refused 0, `check_family_forms` MISMATCH 0 families. The UC-1 body `00712180` (review
queue, PPFX span row) takes it to 4,818.

## 4. Where F stands

| | bodies |
|---|---:|
| F at clean HEAD before repair | 9,955 |
| linkage drift repaired by re-pointing | 5,136 (5,227 less the 91 cascade bodies) |
| cascade drift, needs a closure-rule ruling | 91 |
| pre-existing undeclared frontier | 4,728 |
| semantic loss (a body's own accounting lost) | 0 |

The repair ships in slices, one per group of pages as each comes clean: batch A (VerbAdapter, SEAD,
ExplainedCalleeForwarder, CallResultTailCall, counter-append) in `d1260bf38`, B1 (zlib, JsonBox) after SWE2-FRONTIER
moved the middleware inventory's unattributed pass-22 appends aside, and B2 (PPFX with its UC-1 span row, and the five
Phyre module rows) once the PPFX and fifteen-modules pages are clean.

## 5. Self-falsification

- The zero semantic loss could have been a filter artefact. The A-lost count uses the same `measure_a` on both exports,
  and the positive direction of the same measure finds 83 A gained, so the instrument does see A changes.
- The linkage bucket could have hidden a body that is frontier for a second reason. After the repair, every A-refused
  row is accepted and F falls to exactly undeclared + cascade (4,728 + 91). No residue appears.
- "Every departure is the A promotion" is the claim the base-reproduction control tests. It would fail if a selector,
  a census or an exclusion list had changed between base and HEAD.

## Files

- [`fbucket.py`](fbucket.py): frontier buckets by cause, with a base diff. `python fbucket.py KIT DB [BASE_DB]`.
- [`pairing.py`](pairing.py), [`pairing.tsv`](pairing.tsv): A member -> page -> interior cite -> re-status commit.
- [`cascade.tsv`](cascade.tsv): the 93 closure-cascade bodies and where each is after the repair.
- [`exact_remove.py`](exact_remove.py), [`rows_notes.py`](rows_notes.py), [`build.sh`](build.sh): the repair, as run on
  the clean export. `build.sh` refuses to continue if the refused-row set or any selector's membership change differs
  from what is recorded here.
