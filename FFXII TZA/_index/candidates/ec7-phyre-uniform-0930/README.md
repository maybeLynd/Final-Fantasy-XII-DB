# Phyre module selectors under the uniform closure-source rule (SWE2-EC7, 2026-09-30)

*FABLE's ruling on `SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930`, point 1: UNIFORM, with point 3 for closure. The rule
is implemented in `select_phyre_panimation.py` and `select_phyre_module.py` ([`patch_phyre.py`](patch_phyre.py), whose
docstring text is in both selectors). Figures are from a clean export of HEAD `4b748e8af`, which already contains the
points 2-4 round `1f52825ce`.*

## 1. The rule as applied (SWE2-EC7)

Each module's seed and closure predicate now ignores accounting state.
- A body that passes the predicate counts as a closure source, whether it is A-measured or declared by another family.
- An A-measured source stays A. A source another family declares stays with that family (point 3: ownership never
  moves, collisions are reported).
- Neither kind is ever written as a member of this module.
- Derived families are never read; the predicate reads no family's membership.
- `PHYRE_FAIL` / `PHYRE_FAIL_FILE` force named bodies to fail the predicate. This is the ruling's mutation control.

## 2. Falsification (SWE2-EC7)

**check_family_forms:** MISMATCH 0. This check is vacuous for the Phyre rows: they claim no member size, so it can
pass without testing them, and it is stated here as a check that carries no weight. The sample reads carry it.

**Sample read against each row's description** ("PhyreEngine's <module> module (Sony middleware), not FFXII code ...
exclusively reached"). A seeded random sample was drawn, at least 5 per family and 25 for PhyreCore, in two independent
draws: [`sample-read-1.txt`](sample-read-1.txt) on the first build and [`sample-read-2.txt`](sample-read-2.txt) on this
one. Each sampled body is listed with its census tag, RTTI slots, callers (and whether each is a member), callees,
and the strings it leas.

- **PhyreCore: misfit, admission stopped.** The rule would admit +988. The 25-body sample contains game code. One body
  is tagged `FFXII.MovementNavigationSteering` (`003DB150`), one is called from battle-menu code (`0027BD80`). There are
  7.6, 8.0 and 28.4 KB Presentation bodies (`0047C360`, `0048D4B0`, `004C8320`), and several FFXII PrimaryOwner
  Presentation leaves. Over the whole +988, 148 bodies carry a census tag naming an FFXII domain (among them Audio;FFXII 27),
  Presentation and Input.
  Cause: this predicate has no module namespace segment and no geography. The A-measured and declared exclusions were
  acting as its firewall, so without them the closure runs from core into game code through game bodies that are A
  or declared. **PhyreCore keeps the old exclusion** (`FIREWALL`, stated in the selector). Its file and row are
  unchanged at 426, and the row says why. A PhyreCore predicate repair is needed before the rule can apply to it.
- **Every other family: no misfit in either draw.** Every sampled body is in the module's address range. Each is
  Phyre-tagged, a Phyre class-descriptor or reflection body (strings such as `m_times`, `m_valueKeys`, `GetGlobalTime`,
  `ANIThreadPoolJobs`), or a generic routine whose callers are module members or Phyre class descriptors. Two are
  module-private std heap-algorithm instances (`006B7E00`, `006B8100`, PRendering). Over the whole admitted sets, the
  census-tag domains contain no FFXII/game tag, only Phyre, NativeRoutine, NativeInline, NativeDispatch, NativeAdapter,
  CxxStandardLibrary and Runtime.

**Controls, from the A-only implementation earlier the same day** (record `ec7-accounting-predicate-audit-0930`
section 3):
- Restricted to the 17 bodies the day's re-statuses promoted, the files equal the pre-re-status files minus exactly
  those bodies (194/152/427/19).
- Forcing every A body to fail reproduces the pre-rule files.
- Failing `005C5C80` alone drops 69 closure-only callees; failing `00658470` drops 16.

## 3. What changes (SWE2-EC7)

| family | before | after | admitted |
|---|---:|---:|---:|
| Phyre PAnimation | 119 | 238 | 119 |
| Phyre PPhysics | 95 | 134 | 39 |
| Phyre PPostProcessing | 134 | 161 | 27 |
| Phyre PRendering | 286 | 310 | 24 |
| Phyre PScene | 2 | 9 | 7 |
| Phyre PScripting | 17 | 23 | 6 |
| Phyre PDynamicGeometry | 39 | 42 | 3 |
| Phyre PLOD | 28 | 30 | 2 |
| Phyre PhyreCore | 426 | 426 | 0 (stopped, section 2) |
| **total** | | | **227** |

This includes the 91 PAnimation/PPostProcessing cascade bodies of the day's re-statuses. Removals: none.

- **Per-family member diff:** [`member-diff.tsv`](member-diff.tsv).
- **A-sources and collisions:** [`a-sources-and-collisions.tsv`](a-sources-and-collisions.tsv). Per module it lists the
  A-measured bodies that act as closure sources, and the predicate members other families own. The second kind is
  reported, not moved: PRendering 509, PPhysics 286, PPostProcessing 134, PDynamicGeometry 131, PGeometry 123 and so
  on. Most belong to the reflection and descriptor families.
- **After the change, three other selectors were re-run:**
  - `select_descriptor_siblings_2.py` reproduces its file; its +2 held in `ec7-f-shape-pass-0930` no longer appears,
    because the bodies are PAnimation/PRendering members now.
  - `select_guarded_class_registrars.py` (DERIVED) passes its guard again: `005B2860` is now a PAnimation member.
    It writes the same 99.
  - The DERIVED NativeAdapter.ExplainedCalleeForwarder admits 1 (`005D0DA0`), 488 -> 489. This is derived movement,
    reported separately.

**F:** on the clean export of `4b748e8af`, **4,791 -> 4,563**, with rows refused 0 and family forms MISMATCH 0.

run: select_phyre_panimation.py and select_phyre_module.py (all 16 modules) on a clean export of 4b748e8af.
