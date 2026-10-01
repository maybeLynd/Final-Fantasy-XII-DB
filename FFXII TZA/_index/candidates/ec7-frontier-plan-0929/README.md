# EC-7 frontier plan, 2026-09-29 (SWE2-EC7): a plan, not declarations

**Scope.** This is what the frontier consists of after the refused-family repair
(`_index/candidates/ec7-refused-family-repair-0929/`, check_dispositions frontier 12,570 -> 5,816).
It proposes candidate B/C families **only** where a shared body shape or a named upstream boundary is
demonstrated, each with a membership predicate, a positive control and a count. **Nothing here is
declared.** Family meaning is FABLE's adjudication (T2). Task `SWE2-EC7-FRONTIER-PLAN-0929`.

**Population.** `check_dispositions.evaluate(...)["frontier_set"]` on the working tree: **5,816
bodies** = **795 UC-1 bodies** (frontier by ruling: the 2026-09-28 band admission, never A/B/C by
default) + **5,021 listed bodies**. One row per body with every partition key is in
`frontier-partition-0929.tsv`, produced by `frontier_partition.py`.

## 1. The 795 UC-1 bodies are a ruling question, not EC-7 work

| UC-1 body location | bodies |
|---|---:|
| PPFX span | 733 |
| outside the library spans | 40 |
| libvorbis span | 17 |
| libvpx span | 4 |
| SEAD span | 1 |

**733 of them sit inside the PPFX link span.** The
PPFX family's provenance argument (25 source files, PPFX:: vtables, boundary controls) is a span
argument. Unpatched, its selector admitted them all on 2026-09-29. The ruling keeps them frontier,
and this plan does not touch them. **Question for FABLE:** does the band ruling's "never A/B/C *by
default*" leave room for a library family whose span argument already covers a UC-1 body, or are UC-1
bodies excluded from families outright? The answer moves up to 755
bodies (PPFX, libvorbis, libvpx, SEAD spans).

## 2. The 5,021 listed frontier bodies

| size band (bytes) | bodies |
|---|---:|
| 0-16 | 254 |
| 17-64 | 1829 |
| 65-256 | 2454 |
| 257-1024 | 384 |
| 1025+ | 100 |

**Owner / layer x decoded shape** (owner = `PrimaryOwner`; otherwise the first CodeDomain head, both
through `audit_crossrefs.load_functions`, the neighbour audit's own loader. Shape comes from decoding the
whole body with capstone.)

| owner / layer | caller | one-call adapter | short tail-forwarder | leaf, straight-line | leaf, branchy/large | leaf with loop | const/trivial-return | jmp-only | ret-only | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| owned (PrimaryOwner) | 1177 | 92 | 55 | 216 | 57 | 136 | 31 | 0 | 0 | 1764 |
| no owner; CodeDomain NativeRoutine | 1036 | 47 | 2 | 33 | 18 | 14 | 0 | 0 | 0 | 1150 |
| no owner; CodeDomain NativeInline | 2 | 0 | 0 | 328 | 156 | 157 | 0 | 0 | 0 | 643 |
| no owner; CodeDomain Phyre | 123 | 19 | 9 | 46 | 16 | 13 | 10 | 0 | 0 | 236 |
| no owner; CodeDomain NativeDispatch | 191 | 12 | 8 | 1 | 16 | 0 | 0 | 1 | 0 | 229 |
| no owner; CodeDomain NativeLeaf | 0 | 0 | 0 | 189 | 0 | 2 | 37 | 0 | 0 | 228 |
| no owner; CodeDomain Boundary | 122 | 17 | 9 | 29 | 2 | 2 | 2 | 0 | 0 | 183 |
| no owner, no CodeDomain | 83 | 22 | 6 | 35 | 11 | 15 | 5 | 0 | 0 | 177 |
| no owner; CodeDomain NativeAdapter | 47 | 53 | 45 | 20 | 3 | 0 | 0 | 0 | 0 | 168 |
| no owner; other CodeDomain | 112 | 1 | 8 | 4 | 2 | 3 | 1 | 0 | 0 | 131 |
| no owner; CodeDomain Runtime | 94 | 0 | 3 | 7 | 1 | 7 | 0 | 0 | 0 | 112 |

| citation state | bodies |
|---|---:|
| entry-only, evidence-bearing page | 2278 |
| mentioned nowhere | 2179 |
| cited (other) | 564 |

- Vtable slots (rtti/methods.tsv): 405 at a Phyre vtable slot,
  101 at another class's slot, 4515 at none.
- Library spans: only 3 listed frontier bodies lie inside the six library spans measured
  here (PPFX, SEAD, Tremor/vorbisfile, libvorbis, libvpx, CRI HCA, with bounds as their selectors state
  them): PPFX span 1, SEAD span 1, libvorbis span 1. Over the listed population those six
  families leave almost nothing, and what remains in their spans is UC-1 (section 1). Bullet, Lua, zlib,
  JsonBox, ImGui and mkvparser spans were **not** measured.
- Contiguity: 367 in runs of >= 8 frontier bodies, 2573 in runs of 2-7, 2081 isolated.
  The longest run is 48 (`check_frontier_shape.py`, `frontier-shape.txt`).
- Ghidra call-graph in-degree 0: 1793 (504 of them at a vtable slot). `edges.tsv` has no jcc or
  jump-table edges, so this is a lower bound on reach, not a dead-code claim.

## 3. Findings, each with the control that makes the negative mean something

**F1. No stale generated-family membership by tag.** Generated families are named after CodeDomain tags
(`NativeAdapter.CallResultTailCall`, ...). **0** listed frontier bodies carry a tag equal to, or
prefixed by, a declared family's name. *Positive control:* 1,151 of the 3,883 members of the 179
tag-named families carry their family's tag, so the test can fire. The frontier's tags are the
generic control-flow classes (`NativeRoutine.AcyclicDirectCall.Bounded.Conditional` 343,
`NativeInline.NoCall.BitfieldStateAlgorithm` 246, ...), which name no family.

**F2. The listed frontier is clone-poor, so form families are exhausted.** Grouping the 5,021 bodies by
exact bytes gives **0** groups of >= 4. Masking rel32 call/jmp targets and rip displacements gives
**1** group of 6 (`frontier-clone-groups-0929.tsv`). *Positive control:* the same masked grouping
recovers accepted generated families whole: `CompilerGeneratedCpp.StaticContainerTeardown.IndirectAllocator`
60/60, `NativeAdapter.ForwardSecondArgumentCallReturnTrue` 47/47, `NativeAdapter.CallResultTailCall` 62/62.
**Consequence:** another "PROVED BY FORM" family pass over this frontier would yield almost nothing. What
remains is individually distinct code.

**F3. Existing predicates admit 60 frontier bodies today.** Re-running six families' own selectors
(2026-09-29, recorded in the repair record's `selector-drift.tsv`) would admit these frontier bodies.
The repair withheld them, because adding members is a membership decision:

| family | selector | frontier bodies it would admit |
|---|---|---:|
| NativeAdapter.ExplainedCalleeForwarder | `select_explained_callee_adapters.py` | 40 |
| NativeLeaf.DocumentedGlobalAccessor | `select_documented_global_leafs.py` | 12 |
| Phyre PhyreCore module | `select_phyre_module.py PhyreCore` | 4 |
| ScriptVM.VerbAdapter | `select_verb_adapters.py` | 2 |
| guarded class-registration stubs | `select_guarded_class_registrars.py` | 1 |
| Trivial global accessors | `select_global_accessors.py` | 1 |

**F4. A named-boundary family is demonstrable: the descriptor placement constructors.** See C1.

**F5. 2,278 listed frontier bodies are already cited at their entry by an evidence-bearing page.**
They are the cheapest route to A, but **only by reading them**. An interior citation added without reading is
the citation padding EC-7 refuses. The pages carrying most of them are in section 5.

**F6. A declared family's name conflicts with RTTI (a naming question, not a disposition defect).** All
17 members of `CxxObjectLifecycle.ConditionalTeardownReturnTrue` (generated-function-families.md) are
RTTI-exclusive slot-10 (`+0x50`) bodies of `PClassDescriptorConcrete<T>`. The class-descriptor page names
that slot the class's **placement default constructor**. The row's note claims only a form ("PROVED BY
FORM ... ONE instruction form"), so its acceptance is not affected. Its *name* says teardown, and RTTI
says construction. Routed to FABLE with C1, and not edited here.

## 4. Candidate families (proposals for FABLE; none declared)

### C1: `Phyre PClassDescriptorConcrete<T> +0x50 placement default constructors`, 123 frontier members

- **Upstream boundary (named, RTTI-proven):** every RTTI vtable appearance of the body is slot 10 (`+0x50`)
  of a `Phyre::PClassDescriptorConcrete<T>` instantiation. The class-descriptor page's carried-table
  slot map already names `+0x50` as **"the class's placement default constructor"**: `if (rdx) T::T(rdx);
  return 1`, a per-class value on 296 of 315 classes.
- **Predicate:** RTTI-exclusive (template head, slot) = (`PClassDescriptorConcrete`, 10) **and** the decoded
  body contains `test rdx, rdx` and a `mov al, 1` / `mov eax, 1` return. Both halves come from the image.
- **Positive control:** all 108 already-explained bodies of the same
  population (30 A, 78 declared) pass the shape half, and so do all 123
  frontier bodies. No body fails. The 78 declared ones sit in seven rows: six uniform-size "PROVED BY FORM"
  rows (`NativeAdapter.OutRecordDescriptorInitReturnTrue` 19, `CxxObjectLifecycle.ConditionalTeardownReturnTrue`
  17, `NativeAdapter.NullableOutRecordHeaderInitReturnTrue` 9, `NativeAdapter.OutRecordZeroInitMemberInit` 7,
  `NativeAdapter.OutRecordVtablePairStore` 6, `NativeAdapter.NullableOutRecordVptrCall` 5), and 15 in
  `NativeAdapter.ExplainedCalleeForwarder`. Five of the six form notes describe the wrapper as "if the
  out(-record) pointer is non-null ... return 1", by form and without naming the slot. The
  123 frontier bodies are the form-diverse remainder: 67 distinct sizes, 12-124 B,
  median 44. That diversity is why no form family reached them.
- **Count:** 123. Members: `cand-slot10-placement-ctors.tsv`, status column = frontier. Suggested letter:
  B (class-explained: the slot's meaning is stated once for the class of bodies). The inlined `T::T`
  body of each member is **not** explained by this, exactly as the form rows' notes say of theirs.
- **Also open for FABLE:** whether the seven rows that hold the 78 should be unified under this
  meaning. That is a re-declaration of accepted rows, so it is not proposed here.

### C2: admit F3's 60 bodies into their existing families

Re-run each family's own selector with `--write` and take its admissions only. Predicates, controls and
meanings already exist and are accepted. Count 60. It is a membership change, so T2.

### Considered and not proposed (no demonstrable shared meaning yet)

- `PClassDescriptorConcrete<T>` slot 3 (`+0x18`, 41 frontier / 71 A / 219 declared). The page says
  "per class on the carried table; not named here", so there is no stated meaning to declare.
- `PMethodCallerConcrete` slots 1/2 (35 + 23 + 18 + 10 frontier) and `PTypeDefault` slots 3/4 (8 + 10). These
  are RTTI-exclusive groups, but their slot meanings are not stated anywhere this plan could cite. They
  are the next named-boundary candidates once a page states them.
- Any CodeDomain shape tag (`NativeRoutine.*`, `NativeInline.*`). Those are control-flow classes, not
  shared bodies (F1, F2). A family over one would be the unsupported bulk disposition REVIEW-POLICY refuses.

## 5. What the rest needs

After C1 and C2 the listed frontier is about 4,838 bodies. F2 says it is individually
distinct, so it closes by **reading** (A), routed to the page that already cites the body, or by
specific named-boundary families as their slot or protocol meanings get stated. The pages that cite the
most frontier entries (evidence-bearing pages per `progress.evidence_bearing`, backticked citations per `check_dispositions.CITE`; this plan's own scan) are
`00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` (396),
`00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` (130),
`17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md` (68),
`00-Engine-Core-Runtime/Application-Root/game-application.md` (62),
`16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md` (57), and 286 more pages.

## Reproduction and limits

`frontier_partition.py` -> `frontier-partition-0929.tsv`; `frontier_clones.py` -> `frontier-clone-groups-0929.tsv`;
`plan_candidates.py` -> the two `cand-*.tsv`. The scripts write to `Database/Tools/work/SWE2-EC7/`,
and the committed copies are these. Inputs: working tree at HEAD `8b269d9fa` plus the repair package;
census `Database/Tools/work/graph/functions.tsv` + `uc1_band`; `rtti/methods.tsv`; `graph/edges.tsv`
(Ghidra call graph: no jcc or jump-table edges); shipping EXE sha256 73461D08...21F8.

Limits: the shape classes are a decode-level heuristic for partitioning only and carry no meaning. "Mentioned
nowhere" is `check_dispositions`' backticked citation pattern, not a text search for any spelling. In-degree
is the Ghidra graph. C1's shape half is a necessary-condition check: it shows the wrapper form, not the
inlined constructor.
