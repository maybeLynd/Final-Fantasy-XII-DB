# EC-7 refused-family repair, 2026-09-29 (SWE2-EC7)

**What this is.** `check_dispositions.py` refused 31 `function_families` rows on 10 host pages, so every
member of those rows counted as nothing: **6,777 frontier functions** sat inside refused rows. This
package repairs the rows by **removal only**. No membership predicate changed and no member was added.
Tasks: `SWE2-EC7-REFUSED-FAMILY-REPAIR-0929` (pages, members files, selectors) and
`SWE2-EC7-REFUSED-FAMILY-RECORD-0929` (this record).

## Causes found

1. **A-drift (30 rows).** Members were cited well enough since their declaration to be measured A
   (interior cite on an evidence-bearing page). A beats a declaration, so the row is refused. The
   132 such members are removed. They stay explained, as A.
2. **SEAD count/file mismatch.** The row declared 1144 while the file held 1,170 lines. A 2026-09-20
   edit subtracted 26 A departures from the count and appended the drift note, but never regenerated
   the members file. The file now holds 1,136 and the count is 1,136: the 33 current A departures plus
   one entry the UC-1 series break adjudicated a **false entry** and removed from the population. Every
   remaining member lies in the stated span or is one of the nine named past-span SEAD entries,
   checked. 28 of the 33 A departures already had interior cites in the tree at that 2026-09-20 commit
   (a `git grep` count that ignores page status), which is consistent with the 26.
3. **Stale selectors after the UC-1 series break (2026-09-28).** `load_functions()` now adds 795 UC-1
   frontier bodies, which are frontier by ruling and refused in any members file. Unpatched,
   `select_ppfx.py` admitted 733 of them and `select_audio_libraries.py` failed its libvorbis closure
   assertion. All three affected library selectors (`select_ppfx.py`, `select_audio_libraries.py`,
   `select_libvpx.py`) now drop UC-1 frontier bodies from their population. Patched, each reproduces
   the repaired members file exactly, and the audio selector's five other lists are byte-identical to
   the tracked files.
4. **Phyre exclusive-closure cascade (23 members).** A Phyre module member is a body *every* inbound
   reference of which comes from members. When the A departures leave, 23 bodies reached only through
   them no longer qualify. The selector re-run drops them. **Control:** re-run with the departing A
   entries held non-A, the selector reproduces the previous PRendering and PPostProcessing files
   exactly, and PhyreCore's plus the same 4 additions. So the cascade is caused by the departures
   alone. These 23 return to the frontier.

## Rows

| family | page | declared -> new (old file) | A removed | cascade | false entry | frontier members before | selector re-run vs new file |
|---|---|---|---|---|---|---|---|
| PPFX post-effect library | `yebis-ppfx-source-map.md` | 1619 -> 1610 (file 1619) | 9 | 0 | 0 | 1610 | select_ppfx.py (patched) - equal |
| SQEX SEAD sound library span | `sead-function-identification.md` | 1144 -> 1136 (file 1170) | 33 | 0 | 1 | 1136 | select_audio_libraries.py (patched) - equal |
| ScriptVM.VerbAdapter | `the-shape-of-the-verb-population.md` | 1047 -> 1037 (file 1047) | 10 | 0 | 0 | 1037 | select_verb_adapters.py - equal except 2 would-admit (withheld) |
| Trivial global accessors | `generated-function-families.md` | 483 -> 482 (file 483) | 1 | 0 | 0 | 482 | equal except 1 would-admit (withheld) |
| NativeAdapter.ExplainedCalleeForwarder | `generated-function-families.md` | 459 -> 448 (file 459) | 11 | 0 | 0 | 448 | drifted (selector-drift.tsv); A-only applied |
| Phyre PhyreCore module | `the-fifteen-modules-registered-before-main.md` | 459 -> 429 (file 459) | 20 | 10 | 0 | 439 | select_phyre_module.py - equal except 4 would-admit (withheld) |
| Phyre PRendering module | `the-fifteen-modules-registered-before-main.md` | 304 -> 286 (file 304) | 6 | 12 | 0 | 298 | select_phyre_module.py - equal |
| NativeLeaf.DocumentedGlobalAccessor | `generated-function-families.md` | 218 -> 211 (file 218) | 7 | 0 | 0 | 211 | drifted (selector-drift.tsv); A-only applied |
| AbstractClassDescriptor constructors | `class-descriptor-and-metadata-system.md` | 182 -> 178 (file 182) | 4 | 0 | 0 | 178 | no selector named - exact A removal |
| Phyre PPostProcessing module | `the-fifteen-modules-registered-before-main.md` | 160 -> 156 (file 160) | 3 | 1 | 0 | 157 | select_phyre_module.py - equal |
| Phyre serialization scalar-conversion initialisers | `image-hardening-cfg-aslr-dep-and-stack-cookies.md` | 144 -> 143 (file 144) | 1 | 0 | 0 | 143 | selector asserts; A-only applied |
| AbstractClassDescriptor base-aware constructors | `class-descriptor-and-metadata-system.md` | 133 -> 132 (file 133) | 1 | 0 | 0 | 132 | no selector named - exact A removal |
| libvpx VP8 decoder object | `third-party-middleware-inventory.md` | 118 -> 116 (file 118) | 2 | 0 | 0 | 116 | select_libvpx.py (patched) - equal |
| guarded class-registration stubs | `class-descriptor-and-metadata-system.md` | 74 -> 72 (file 74) | 2 | 0 | 0 | 72 | drifted (selector-drift.tsv); A-only applied |
| NativeAdapter.CallResultTailCall | `generated-function-families.md` | 65 -> 62 (file 65) | 3 | 0 | 0 | 62 | no selector named - exact A removal |
| Phyre PFramework module | `the-fifteen-modules-registered-before-main.md` | 48 -> 47 (file 48) | 1 | 0 | 0 | 47 | select_phyre_module.py - equal |
| MSVC dynamic-initialiser stubs (assorted statics) | `static-initialisers-and-teardowns.md` | 44 -> 43 (file 44) | 1 | 0 | 0 | 43 | selector asserts; A-only applied |
| NativeAdapter.CallResultWithSavedIntTailCall | `generated-function-families.md` | 32 -> 31 (file 32) | 1 | 0 | 0 | 31 | no selector named - exact A removal |
| scalar deleting destructors, inlined-dtor spelling | `static-initialisers-and-teardowns.md` | 27 -> 24 (file 27) | 3 | 0 | 0 | 24 | equal on this list except 72 would-admit (withheld) |
| NativeAdapter.StaticPointerTailCall | `generated-function-families.md` | 21 -> 20 (file 21) | 1 | 0 | 0 | 20 | no selector named - exact A removal |
| Phyre PScripting module | `the-fifteen-modules-registered-before-main.md` | 18 -> 17 (file 18) | 1 | 0 | 0 | 17 | select_phyre_module.py - equal |
| NativeAdapter.DualLookupIndirectCallback | `generated-function-families.md` | 13 -> 12 (file 13) | 1 | 0 | 0 | 12 | no selector named - exact A removal |
| Phyre.Reflection.StaticDescriptorSingleton | `generated-function-families.md` | 13 -> 12 (file 13) | 1 | 0 | 0 | 12 | no selector named - exact A removal |
| NativeAdapter.FirstMemberPointerTailCall | `generated-function-families.md` | 13 -> 12 (file 13) | 1 | 0 | 0 | 12 | no selector named - exact A removal |
| NativeLeaf.StaticPointerNestedFieldGetter | `generated-function-families.md` | 11 -> 10 (file 11) | 1 | 0 | 0 | 10 | no selector named - exact A removal |
| NativeLeaf.SlideTableRecordCopyInvoke | `generated-function-families.md` | 10 -> 9 (file 10) | 1 | 0 | 0 | 9 | no selector named - exact A removal |
| NativeLeaf.GlobalHandleStateRead | `generated-function-families.md` | 6 -> 5 (file 6) | 1 | 0 | 0 | 5 | no selector named - exact A removal |
| NativeAdapter.MallocRecordArgEmplaceTailCall | `generated-function-families.md` | 6 -> 5 (file 6) | 1 | 0 | 0 | 5 | no selector named - exact A removal |
| NativeAdapter.FixedPipelineCallResult | `generated-function-families.md` | 5 -> 4 (file 5) | 1 | 0 | 0 | 4 | no selector named - exact A removal |
| NativeAdapter.GlobalOffsetTailCall | `generated-function-families.md` | 4 -> 3 (file 4) | 1 | 0 | 0 | 3 | no selector named - exact A removal |
| bump-allocator pop leaf, 17-byte form | `object-construction-destruction-and-static-lifetime.md` | 4 -> 2 (file 4) | 2 | 0 | 0 | 2 | select_teardown_form_clusters_4.py - equal |

`removed-members.tsv` has every removed address with its reason. `selector-drift.tsv` has what a
selector re-run would change *beyond* these removals (would-admit 134, would-drop 2 non-A, 2 selectors
assert). **None of that drift was applied:** new membership is a family decision (T2) and is left for
adjudication.

## Result (check_dispositions, same tree, before -> after)

Before (percentages of 35,064 = 34,269 listed + 795 UC-1 frontier, the census at the time):
```
  A  individually explained (interior cite, evidence-bearing page)   :   9295
  B  class-explained          (declared)                               :    885
  C  dispositioned            (declared)                               :  12314
  D  declared exception       (declared, NOT counted as explained)     :      0
  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
  explained (A + B + C)                                                :  22494  64.15%
  frontier  (declared by nothing)                                      :  12570
      of which UC-1 1-64 B band (unexplained code admitted 2026-09-28)  :    795

  families accepted: 303   refused: 31
```
After (the same 35,064):
```
  A  individually explained (interior cite, evidence-bearing page)   :   9295
  B  class-explained          (declared)                               :   3063
  C  dispositioned            (declared)                               :  16890
  D  declared exception       (declared, NOT counted as explained)     :      0
  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
  explained (A + B + C)                                                :  29248  83.41%
  frontier  (declared by nothing)                                      :   5816
      of which UC-1 1-64 B band (unexplained code admitted 2026-09-28)  :    795

  families accepted: 334   refused: 0
```
Frontier 12,570 -> 5,816 (-6,754 = 6,777 frontier members of refused rows - 23 cascade returns).
A is unchanged at 9,295.

## Self-falsification: what would have shown this wrong, and was it looked for

- *A removal of a member that is not A.* All 132 A-measured removals are A in the working tree
  **and** at HEAD content: dirty peer pages were replaced by their HEAD text and untracked pages
  dropped, giving an A set of 9,290 with all 132 still in it (`a_at_head.py`). So no removal depends on
  a peer's uncommitted citation.
- *A repaired row colliding with another family.* `check_dispositions` checks collisions before the
  A overlap and would refuse a later row that shares a member. After the repair it refuses 0 rows.
- *A selector re-run doing more than the A removal.* Each named selector was run into scratch against
  the same inputs and diffed. Where it did more (additions, non-A drops, assertions) only the exact A
  removal was applied, and the difference is recorded.
- *Cascade misattributed.* The held-non-A control above.
- Gates on the 10 pages: `check_dispositions --self-test` 13/13; `check_family_forms` 0 MISMATCH;
  `check_family_spans` rc 0; `verify_doc_addresses` ok on all 10; `check_questions` consistent;
  `check_links` red only on pre-existing BROKEN AT HEAD links in other pages; `check_publish_neighbours`
  ADDS NOTHING (1,929 -> 1,928). The first draft of the notes listed the removed addresses and added 6
  unaccounted neighbours; the addresses were moved to this record.

## Limits

- A is a proxy (interior citation), not proof of understanding. This package moves no body into A.
- The restored rows are the rows as they were declared and previously accepted. Their notes and
  controls are the declaring lane's. The only new claims are the removals, their reasons, and the
  SEAD count explanation.
- Some notes still state historical member counts in their inclusion prose (for example "N members,
  all K bytes"). The appended dated sentence records the departure, as earlier drift sweeps did.
- Inputs: HEAD at run `8b269d9fa` plus the working tree; census `Database/Tools/work/graph/functions.tsv`
  (sha256 c0e1de8f650f2e8d...) + UC-1 bands (uc1_band.py; 1-64 9c4ce599..., 65-256 365a6240...);
  shipping EXE sha256 73461D08...21F8; RTTI `Database/Tools/work/rtti/methods.tsv` (336340b0...).

## Review

Tier: the selector-reproduced removals (PPFX, libvpx, the five Phyre modules, the verb A-removals) and
the exact A-only removals are **T0** (determined by selector + input, or by the A set). The **SEAD
membership change is T1**, routed to `SWE2-AUDIT-SEM`. The withheld selector additions are
T2 family decisions and are reported to FABLE, not applied.
