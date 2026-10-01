# Accounting state in family predicates: audit of the 53 selectors, five repairs, and the Phyre measurement (SWE2-EC7)

*SWE2-EC7, 2026-09-30. FABLE's ruling on `SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930` says that accounting state
(A-measured / declared by a family / frontier) never feeds a membership or closure predicate. A body may still be
removed from a selector's own OUTPUT because it is A or declared elsewhere; that is not a predicate. Execution of
the ruling, record of the audit.*

## 1. The audit (SWE2-EC7)

The audit read the code of all 53 `select_*.py` under `Database/FFXII TZA`. It looked at code, not docstrings, and
traced every use of `a_set` / `measure_a`, `declared` / other rows' members files, and `frontier_set`. A read-only
helper session under SWE2-EC7 did the reading; every repair below was re-run by me on a clean export.

- **37 selectors are exclusion-only or use no accounting state at all.** Most of them are the shared frontier
  form-cluster template: the pool is the frontier plus the selector's own prior members, the predicate is form plus
  targets, and a write is refused if a selected member is A.
- **10 selectors feed accounting state into a predicate:**

| selector | what feeds the predicate | action |
|---|---|---|
| `select_phyre_panimation.py`, `select_phyre_module.py` | A and declared bodies are neither seeds nor closure sources | rule implemented; see section 3 (held) |
| `select_jsonbox.py`, `select_imgui.py` | A callers allowed in the shrink, A bodies hard-excluded from the component; both also excluded their OWN row (`NAME` did not match the row name), so neither ran at HEAD | **repaired** (A), name fixed |
| `select_mkvparser.py` | the unwind-closure owner frame must be a member, so a frame that became A breaks it | **repaired** (A) |
| `select_msvc_runtime.py` | any in-block A body was a caller allowance, so being A alone qualified | **repaired** (A) |
| `select_libvpx.py` (DSP kernels) | A span bodies joined the source set on a weaker test than members pass | **repaired** (A) |
| `select_guarded_class_registrars.py` | "every auxiliary callee is already-explained code": the family is DEFINED by accounting | routed: needs a definition |
| `select_explained_callee_adapters.py` | "forwards to an already-explained callee": DEFINED by accounting | routed: needs a definition |
| `select_descriptor_flag_registrars.py` (+ `_compact`) | provenance needs the ctor/dtor to be in OTHER families' members files (declared state); the compact twin check counts only frontier twins | routed (declared-state) |

There are also three borderline uses, not changed here and routed with the rest. `select_audio_libraries.py`,
`select_ppfx.py` and `select_libvpx.py` drop UC-1 bodies from the population before attributing callers, so a call
from a UC-1 body is invisible to their foreign-caller tests. The count gate in `select_descriptor_pair_accessors.py`
counts only frontier hits.

## 2. The five repairs (SWE2-EC7)

In each repaired selector, an A-measured body is judged by exactly the predicate a member is judged by. When it
passes, it acts as a qualifying caller, frame or closure source. It stays A and is removed only from the output.
Being A alone never qualifies a body. Bodies declared by another family are handled as before; that generalisation is
routed (section 4).

| selector | qualifying A bodies | output on a clean HEAD export |
|---|---:|---|
| `select_jsonbox.py` | 2 (the two bodies the 8c8406bfd / 9bda44687 re-statuses promoted) | 55, identical to the file; it runs again |
| `select_imgui.py` | 1 (the static object's ctor) | 10, identical; it runs again |
| `select_mkvparser.py` | 3 | 101, identical |
| `select_msvc_runtime.py` | 29 | identical |
| `select_libvpx.py` | 6 | decoder 116 and kernels 63, identical |

No membership changes. The repairs remove the dependence; they do not move bodies. Each output is compared with
the committed members file. The unpatched msvc selector also reproduces its file, and the unpatched JsonBox and ImGui
selectors did not run at all. `select_mkvparser.py` also stops moving an A or declared body into members through the
unwind closure; none qualified, so its output is unchanged.

## 3. Phyre: the ruling's own control fails for the uniform rule (held, routed back)

The rule as ruled is implemented in both Phyre selectors. The seed and closure predicate ignores A; A bodies that pass
are closure sources and never members. There is a `PHYRE_FAIL` / `PHYRE_FAIL_FILE` control hook. Measured on a clean
export of `59ec09a95`:

- **Restricted to the 17 bodies today's re-statuses promoted** (every other A body forced to fail): the member files
  equal the pre-re-status files (`50890aa7f`) minus exactly the promoted bodies. They are PAnimation 194 = 202 - 8,
  PPostProcessing 152 = 156 - 4, PhyreCore 427 = 430 - 3, and PSerialization 19 = 21 - 2. The two cascade adapters
  return from NativeAdapter.ExplainedCalleeForwarder to PAnimation. **This is the ruling's control (4), and it holds.**
- **Mutation control:** forcing every A body to fail reproduces HEAD's cascade files exactly. Failing one promoted body
  drops its closure-only callees again: `005C5C80` drops 69 (194 -> 125), `005C35A0` 4, `005C0B60` 1, `005CB150` 1;
  `00658470` drops 16 (152 -> 136), `00659C20` 2. Bodies with no closure-only callees drop nothing.
- **The rule as ruled (every A body that passes the predicate is a source):** it admits 605 bodies, not 93. They are
  PAnimation +118 (to 237), PhyreCore +447 (to 874, with 1,119 A-measured core bodies qualifying as sources),
  PPostProcessing +19, PRendering +14, PScripting +6 and PPhysics +1. 510 of them were never members. A bodies blocked
  their closure before the families were declared, not because of today's re-statuses. So the uniform rule does not
  meet the ruling's control (4). By the family's own predicate each of the 605 is module code, but admitting them is a
  bulk T2 change the ruling's control did not anticipate.

**Held, not published:** the Phyre selector change and its member files wait for FABLE's choice between the uniform
rule (+605) and a rule scoped to promotions since a family's declaration. A scoped rule needs a stated scope, because
"promoted since" is itself an accounting fact.

## 4. Routed (SWE2-EC7)

To FABLE, `SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930`, with this record:
1. the Phyre uniform-vs-control question (section 3);
2. the two accounting-defined families (guarded class-registration stubs; NativeAdapter.ExplainedCalleeForwarder);
3. whether "declared by another family" counts as accounting state for the closure (the ruling's generalisation
   says yes; applying it moves membership between families);
4. the UC-1 caller-attribution borderline.

run: selector re-runs on clean exports of 59ec09a95 and 836502680 (this record's figures).
