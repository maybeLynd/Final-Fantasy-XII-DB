# EC-7 declarations under the FABLE family ruling, 2026-09-29 (SWE2-EC7)

Executes [`fable-family-ruling-0929`](../fable-family-ruling-0929/README.md) (commit `4e32dd8df`) on the plan in
[`ec7-frontier-plan-0929`](../ec7-frontier-plan-0929/README.md). Each ruling item is its own declaration and its own
commit, and each goes to SWE2-AUDIT-SEM with the `reviews` field. Task `SWE2-EC7-FAMILY-RULING-EXEC-0929`.

Inputs for every run below: shipping EXE sha256 `73461D08...21F8`; census `Database/Tools/work/graph/functions.tsv`
(sha256 `c0e1de8f650f2e8d...`) plus the UC-1 bands (`uc1_band.py`); RTTI `Database/Tools/work/rtti/methods.tsv`
(sha256 `336340b0a22dc812...`). Working tree on HEAD `9ca3df0ac`. **Every membership below was also re-derived on a
clean extract of HEAD `9ca3df0ac` (`git archive`, peer-dirty pages absent), with the same result**, so no member depends
on a peer's uncommitted citation.

## R2 / C1: `PClassDescriptorConcrete<T>` placement default constructors, slot 10 (`+0x50`), B, 123 members

**Declared** on
[`class-descriptor-and-metadata-system.md`](../../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md),
the page whose carried-table slot map states the slot's meaning: `+0x50` is "the class's placement default
constructor", `if (rdx) T::T(rdx); return 1`. Members file
`members/pclassdescriptorconcrete-placement-default-ctors.tsv`, generator `members/select_descriptor_placement_ctors.py`.

**Predicate, both halves read from the image.**
1. RTTI: every appearance of the body in `rtti/methods.tsv` is slot 10 of a `Phyre::PClassDescriptorConcrete<...>`
   vtable.
2. Shape, strict form: one `ret`, as the last instruction; `test rdx, rdx` immediately followed by `je`; `al = 1` at that
   `ret` on the null path and the constructed path alike. Two compiled spellings occur. In the *join* spelling the `je`
   lands on `mov al, 1` and only epilogue follows it. In the *hoisted* spelling `mov al, 1` comes before the `test`, and
   nothing after it writes `rax` or calls. The plan's shape half was only a necessary condition (a `test rdx, rdx` and a
   `mov al, 1` anywhere in the body). This one also fixes the return value on both paths.

Not A, not a member of another family, and not a UC-1 body.

**Controls** (`c1-selector-run.txt`):
- positive, the ruling's test: **all 108** already-explained bodies of the same RTTI population (30 A, 78 declared)
  pass the shape half, now under the strict form as well. The population is 231 bodies, and all 231 pass;
- negative: the `xor al, al ; ret` stub `00657140`, which the page puts at `+0x50` on the abstract classes and on those
  without a default constructor, is refused by the shape. The test can fail;
- discriminator: 15 census bodies of 256 B or less outside the RTTI population also pass the shape (10 frontier, 1 A,
  4 declared), and none of them is admitted. The RTTI slot does the selecting, and the shape only confirms the wrapper.

**`plan_candidates.py` re-run** (`c1-plan-candidates-rerun.txt`, after the row): slot-10 population A 30, declared
201 (= 78 + 123), frontier 0, and no body fails the shape. The members file equals the plan's
`cand-slot10-placement-ctors.tsv` frontier rows exactly (123/123).

**What B covers, in the ruling's words.** It covers the wrapper: the slot's role, the null test and the return value.
**The inlined `T::T` in each member is class `T`'s default constructor. It is explained, or not, with class `T`'s own
type entry, not by this row**, and so are the base or member constructors that 30 of the 123 call from inside it.
Declaring C would be wrong, because for game classes the inlined constructor is game code.

**Not done here.** The seven accepted rows that hold the other 78 bodies of the slot are not re-declared (R2: optional,
its own T2 package). One of them, `CxxObjectLifecycle.ConditionalTeardownReturnTrue`, is renamed under R4 below.

**Result** (`check_dispositions`, same tree): B 3,063 -> 3,186, frontier 6,275 -> 6,152, families accepted 333 -> 334.
The one refused row (`Bullet physics`, 5 A-drift members) predates this package and is untouched.

**Gates:** `check_dispositions --self-test` 13/13; `check_family_forms` 0 MISMATCH; `check_family_spans` rc 0;
`verify_doc_addresses` on the page 0 to confirm; `check_publish_neighbours` ADDS NOTHING (1216 -> 1216).

**Review:** T2 (a family claim), adjudicated for meaning by FABLE's R2. First-line audit: SWE2-AUDIT-SEM re-derives the
members and the positive control.

**Published:** `e23d9914d`.

## R3 / C2: the bodies the existing accepted selectors admit, 59 applied, 2 withheld (SWE2-EC7)

R3 makes this routine (T0) when the selector file is the committed version (with the UC-1 exclusion patch), the run
adds members and removes none or the removals are reported separately, and the declared count and the members file
move together. Every family below was re-run with its own selector. Each members file is now **the selector's output**,
and on a clean extract of HEAD `9ca3df0ac` the same selector writes a byte-identical file. Every change is in
`c2-membership-changes.tsv`, and the runs are in `c2-selector-runs.txt`.

| family | page | selector | count | admitted | dropped | T0 test |
|---|---|---|---|---:|---:|---|
| `NativeAdapter.ExplainedCalleeForwarder` | `generated-function-families.md` | `select_explained_callee_adapters.py` | 448 -> 487 | 40 | 1 | committed selector, unchanged |
| `NativeLeaf.DocumentedGlobalAccessor` | `generated-function-families.md` | `select_documented_global_leafs.py` | 211 -> 222 | 12 | 1 | **selector edited: count guard only** |
| `Trivial global accessors` | `generated-function-families.md` | `select_global_accessors.py` | 482 -> 483 | 1 | 0 | **selector edited: UC-1 exclusion added** |
| `Phyre PhyreCore module` | `the-fifteen-modules-registered-before-main.md` | `select_phyre_module.py PhyreCore` | 429 -> 433 | 4 | 0 | committed selector, unchanged |
| `ScriptVM.VerbAdapter` | `the-shape-of-the-verb-population.md` | `select_verb_adapters.py` | 1037 -> 1039 | 2 | 0 | committed selector, unchanged |
| **total** | | | | **59** | **2** | |

All 59 admissions were frontier bodies, and they are exactly the plan's `cand-selector-admits.tsv` rows for these five
families (40 + 12 + 1 + 4 + 2, address for address). None collides with C1 or with another family.

**Removals, reported separately (R3).** Neither is an A departure. Each lost the explanation it inherited because the
page carrying it is now `REOPENED`, which `progress.evidence_bearing` does not count:
- `0036CAD0` leaves `ExplainedCalleeForwarder`. Its callee `0036D050` was A on `where-the-games-memory-comes-from.md`,
  and that page is `REOPENED`, so `0036D050` is frontier now and so is its adapter.
- `003DE970` leaves `DocumentedGlobalAccessor`. Its target global `02B58C50` is cited only on
  `the-field-runtime-pass.md`, now `REOPENED`.

Both return to the frontier. They were already flagged "would-drop" in the repair record's `selector-drift.tsv`.

**Two departures from the strict T0 test, stated so the audit can check them:**
1. `select_documented_global_leafs.py` writes its file and **then** asserts `len(members) == 196`, its declaration
   count of 2026-09-17. The row has been 218 and then 211 since, through A-drift edits made without a re-run, so the
   committed selector already failed this guard before this package. The guard now reads 222, with a comment saying
   why. **The predicate is unchanged**, and the output written before the assert is byte-identical with and without the
   edit.
2. `select_global_accessors.py` had no UC-1 exclusion. Unpatched, it admits **10 UC-1 bodies** (493), and
   `check_dispositions` would refuse the row. It now carries the patch the three library selectors received in
   `839236205`, word for word in effect: it drops `uc1_band.frontier_starts()` from the census. Patched, it writes 483 =
   482 + the one frontier admission.

**Withheld: `guarded class-registration stubs` (2 frontier bodies).** Today the re-run of
`select_guarded_class_registrars.py` also **moves** `00665870` and `00666380` from the orchestrators row to the stubs
row. They are two of the 134 drift admissions outside the frontier, which R3 excludes. It also now admits `005EFE60`, a
body the Phyre PRendering cascade returned to the frontier on 2026-09-29, after the plan was measured. Applying the
selector output would carry those moves, and applying only the frontier rows would leave a file the selector does not
reproduce. So neither is done. The plan's one body here (`00676A70`) and `005EFE60` stay frontier, and the family
decision on the orchestrator/stub split is left open.

**Not covered and not applied** (stays in `selector-drift.tsv`): the two asserting selectors
(`select_scalar_conversion_registrars.py`, `select_static_init_form.py`), and the 72 scalar-deleting-destructor
admissions outside the frontier.

**Cascade check after C1 and C2.** All 17 Phyre module selectors were re-run into scratch on the resulting tree. 16
reproduce their tracked files byte for byte. `PAnimation` differs by 2 bodies outside its span, because its tracked file
comes from the span-limited `select_phyre_panimation.py`, not the general selector. That difference is by design and
predates this package.

**Result** (`check_dispositions`, same tree, after C1): B 3,186 -> 3,239 (+53), C 16,418 -> 16,422 (+4), frontier
6,152 -> 6,095 (-57 = 59 admitted - 2 dropped). Families accepted 334, and the one refused row is still the Bullet
A-drift.

**Published:** `302bf18a6`.

## A-drift repairs found while measuring (SWE2-EC7)

These are not ruling items. During this package two accepted rows went **refused** because peers' commits measured some
of their members A, and while a row is refused `check_dispositions` counts all of its members as frontier. Both are
repaired by removal only, the T0 repair the evidence standard prescribes ("a generated family membership goes stale
every time A grows"):

| row | page | cause | removed | count |
|---|---|---|---|---|
| `Bullet physics library` | `third-party-middleware-inventory.md` | `08afb6b02` re-statused the citing page DOCUMENTED | `00832390`, `008324B0`, `008531F0`, `00854080`, `008542B0` | 472 -> 467 |
| `NativeAdapter.CallThenTailCall` | `generated-function-families.md` | `5e5fee584` cites `00409F84` inside it | `00409F80` | 18 -> 17 |

`members/select_bullet.py` re-run drops exactly these five and admits nothing, and it writes the same file on a clean
extract of HEAD. `CallThenTailCall` names no selector, so its A member is removed exactly. Both causes are committed
pages, so neither removal depends on a peer's uncommitted text. Result: `check_dispositions` refuses **0** rows, C
16,422 -> 16,888, frontier 6,095 -> 5,627.

**Published:** `8c093b7d0`.

## R4: `CxxObjectLifecycle.ConditionalTeardownReturnTrue` renamed (SWE2-EC7)

The row on `generated-function-families.md` is now `Phyre.PClassDescriptorConcrete.PlacementCtorConditionalReturnTrue`.
All 17 members are RTTI-exclusive slot 10 of `PClassDescriptorConcrete<T>`: the class's placement default constructor,
not a teardown. Its acceptance by form, letter, count and members file are unchanged. Its note keeps the old name and
says why it changed. The same wrong reading ("a conditional destroy-and-report-success virtual") stood on the
object-construction page's BQ-25 section. It is struck and corrected there, with the RTTI evidence for all 28 tagged
bodies: 27 are `PClassDescriptorConcrete<T>` slot 10, and one is `PClassDescriptorWithoutDefaultConstructor<PScheduler>`
slot 10.

Consumers, with the agreement state of each: [`consumer-check.md`](consumer-check.md). The register row BQ-25 is routed
to SWE2-CONTRACT, which holds `OPEN-QUESTIONS.md` (`SWE2-EC7-REQ-CONTRACT-BQ25-ROW-0929`), with the exact text.
Regression: [`rename_check.py`](rename_check.py), FAILS 0 here, and FAILS 4 on the pre-rename extract
(`rename-check-run.txt`).
