---
system: The subsystem registry — fifteen Phyre modules that register themselves before main
category: 22-Middleware-PhyreEngine
status: AUDITED
owner_layer: CodeDomain:Phyre.SubsystemRegistration; no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 34 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  project: work/headless_gn160/GFZ_GN160, CHECKPOINT VERIFIED 2026-09-07
last_reviewed: 2026-09-08
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-subsystem-registry-pass-1
  last_pass_kind: falsification
  crossref_clean: false
  reopened_count: 0
function_families:
  - "Phyre PAnimation module | C | ../members/phyre-panimation.tsv | 238 | PhyreEngine's PAnimation module (Sony middleware), not FFXII code: frontier census entries in the module's link span 005A0000-005D0000 that are vtable slot targets of own-namespace Phyre::PAnimation classes (67), plus bodies whose every inbound reference - call/jmp/lea, or a slot of a PAnimation-bound class in a COL-validated vtable - comes from members or bound template referrers, iterated to a fixpoint (136). The selector re-derives all 2,286 COL-validated vtables from the image (the index page's own count) rather than trusting methods.tsv; the registration chain is real: 005AD8F0 leas PAnimatableComponent's member names 'm_animationClips' / 'm_animationWeightedBlenderController' and calls the reflection helpers 006388C0 / 00632FB0. Excluded: 33 A-measured (interior cites keep landing on members - A beats a declaration), 11 ICF-foreign bodies shared with other modules' instantiations (005C51F0 sits at PMethodCallerConcrete<PAnimatableComponent,...> AND <PPhysicsRigidBody,...>), 205 bound-template referrer bodies (machinery, not members), foreign-class vtable slots (PRendering descriptors, PType/PCaller thunks and PInternal visitors the linker placed in-span), entries already declared by other families, 17 with no inbound references at all, 113 not exclusively reached. Controls: outbound calls reach only Phyre core reflection helpers (0063xxxx), other Phyre zones, CRT and imports (74 distinct); inbound non-member referrers are 2 edges; edge neighbours 0059FFC0 (PSerialization side) and 005D0000 (a PRendering descriptor) are not PAnimation's. Boundary: the module's own code; the reflection template machinery, its teardowns and the PUtility object are NOT covered. Selector: ../members/select_phyre_panimation.py 1 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 005B0BB0. 2026-09-30 (SWE2-EC7, DD re-status A-drift, record _index/candidates/ec7-dd-adrift-pairing-0930): 8 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the animation channel binding page (46c98f222) DOCUMENTED, and 75 more left as the exclusive-closure cascade of those departures (their inbound references now include the A bodies, which are not members); re-running ../members/select_phyre_panimation.py drops exactly these 83 and admits nothing. Control: with only the 8 departed bodies held non-A the selector reproduces the pre-re-status 202-member file exactly, so every departure is the A promotion or its cascade; 2 of the 75 are now declared by NativeAdapter.ExplainedCalleeForwarder, 73 are frontier; addresses and causing pages in the record. 2026-09-30 (SWE2-EC7, closure-source ruling - uniform, record _index/candidates/ec7-phyre-uniform-0930): 119 member(s) joined the family under FABLE's closure-source ruling (SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, uniform per SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930): the selector's predicate now ignores accounting state, so an A-measured body or another family's body that passes the module predicate is a closure source (it stays A or stays with its declaring family and is never written here); this restores the 2026-09-30 re-status cascade and the bodies the same exclusion kept out since declaration. Falsified by reading a seeded random sample against this row's description (no misfit) and by check_family_forms (0 MISMATCH); per-family member diff, A-source list and the predicate members owned by other families are in the record."
  - "Phyre PhyreCore module | C | ../members/phyre-phyrecore.tsv | 426 | PhyreEngine's core module (Sony middleware: Phyre::PWorld, PCluster, PObject, the array/map container templates and their private helpers), not FFXII code: frontier census entries that are vtable slot targets of own-namespace Phyre classes carrying NO module namespace segment (93), plus bodies whose every inbound reference - call/jmp/lea, or a slot of a core-bound class in a COL-validated vtable - comes from members or core-bound template referrers, iterated to a fixpoint (384). Unlike PAnimation the linker gave the core NO contiguous span - members sit in 36 of the 64KB zones from 0015xxxx to 0087xxxx wherever the linker interleaved them - so membership is pure namespace + exclusivity, no geography. 'Core-bound' means every '@X@Phyre@' mention is a non-module name (PWorld, PInternal, the VP*/PE* machinery): a class like '.?AVPWorld@Phyre@@' or '.?AVPWorldBullet@PWorld@Phyre@@' qualifies, '.?AVFoo@@' outside the Phyre namespace does not. The module set is the fifteen registered namespaces PLUS the four that own an RTTI namespace without a PUtility registrar - PFramework, PGameplay, PVision, PProfiling; an earlier draft that treated only the fifteen as modules wrongly absorbed 109 foreign bodies and was corrected before declaration. Excluded: A-measured and already-declared entries, 2,178 bound-template referrer bodies (the reflection/container machinery - referrers, never members), bodies with no inbound references, and anything not exclusively reached. Controls: outbound calls reach 288 distinct non-member targets across the Phyre zones, game code, CRT and imports (the core is the library everything calls); inbound non-member referrers are 14 edges in 9 zones (the public API surface); 176 member-referenced .data cells are also touched outside - descriptor objects and shared allocator/registry state, same expected-sharing pattern as PAnimation. Boundary: own code only; the template machinery, the PUtility objects and module teardowns are NOT covered. Selector: ../members/select_phyre_module.py PhyreCore. 2026-09-18: 490→486 - four members (0017D900, 0018D3F0, 0018FE00, 00191130) have since been measured as A and drop out of the fixpoint (A beats a declaration). 4 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 00188AC0, 00193DA0, 0062DFB0, 00635CC0; 3 member(s) left the family 2026-09-20, now declared by other families: 00224C30 -> NativeAdapter.VtableInstallTail; 002251A0 -> NativeAdapter.VtableInstallTail; 007A3CE0 -> NativeAdapter.ZeroFirstArgTailCall 20 member(s) left on the 2026-09-20 selector re-run, no longer derived by the selector (returned to the frontier undeclared): 0061C2B0 and 19 more 20 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. 10 more left as the exclusive-closure cascade of those departures: re-running ../members/select_phyre_module.py PhyreCore drops them, and with the departing entries held non-A the selector reproduces the previous file exactly (control). The re-run would also admit 4 entries, independently of these departures - not added: new membership awaits adjudication (selector-drift.tsv in the same record). 2026-09-29, FABLE family ruling R3 (SWE2-EC7): the 4 would-admit entries are applied - the re-run adds exactly them and removes none; the members file is the selector's output, byte-identical on a clean extract of HEAD; record _index/candidates/ec7-family-ruling-exec-0929. 2026-09-30 (SWE2-EC7): 2 member(s) left the family, since measured as A (A beats a declaration) after OPUS ddbf03b11 re-statused what-the-console-tunes.md DOCUMENTED, and 1 more left as the exclusive-closure cascade of those departures; re-running ../members/select_phyre_module.py PhyreCore drops exactly these three and admits nothing. 2026-09-30 (SWE2-EC7, DD re-status A-drift, record _index/candidates/ec7-dd-adrift-pairing-0930): 3 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the animation channel binding page (46c98f222, 2) and how-a-path-is-resolved-to-bytes (30f461a92, 1) DOCUMENTED; re-running ../members/select_phyre_module.py PhyreCore drops exactly these three and admits nothing; addresses and causing pages in the record. 2026-09-30 (SWE2-EC7, DD re-status A-drift round 2, record _index/candidates/ec7-dd-adrift-pairing-0930): 1 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused how-the-engine-chooses-3d-or-flat-movement.md (d1fe4bef1) DOCUMENTED; re-running ../members/select_phyre_module.py PhyreCore drops exactly it and admits nothing; addresses and causing pages in the record (pairing-round2.tsv). 2026-09-30 (SWE2-EC7, closure-source ruling - uniform, record _index/candidates/ec7-phyre-uniform-0930): The uniform rule is NOT applied to this row: a sample read of the +988 bodies it would admit found game code (FFXII movement, battle-menu and multi-kilobyte presentation bodies), because this predicate has no namespace segment or geography and the A/declared exclusions were acting as its firewall. Per the ruling a misfit stops the admission; the selector keeps the old exclusion for this module until its predicate is repaired."
  - "Phyre PPhysics module | C | ../members/phyre-pphysics.tsv | 134 | PhyreEngine's PPhysics module (Sony middleware: Phyre::PPhysicsRigidBody, the PPhysics* shape classes and their private helpers), not FFXII code: frontier census entries that are vtable slot targets of own-namespace Phyre::PPhysics classes (39), plus bodies whose every inbound reference - call/jmp/lea, or a slot of a PPhysics-bound class in a COL-validated vtable - comes from members or bound template referrers, iterated to a fixpoint (56). No contiguous span: members concentrate in 0067xxxx-006Axxxx (89 of 95) with private helpers the linker placed at 005E/0066/006B/008B. Excluded: 44 ICF-foreign bodies (the same PMethodCallerConcrete<...> sharing the PAnimation pilot found - 005C51F0 folds PAnimatableComponent and PPhysicsRigidBody instantiations into one body), 471 bound-template referrers, A-measured and already-declared entries. Controls: ZERO inbound non-member referrers - the module's frontier surface is reached only through its own evidence chain; 51 distinct outbound targets (Phyre core, CRT, imports); 12 member-referenced .data cells shared outside are the module registry objects and the universal allocator; 13 foreign-class vtable bodies inside the densest member bucket (0069xxxx) stay frontier - the linker interleaved other modules' slots there. Selector: ../members/select_phyre_module.py PPhysics. 2026-09-30 (SWE2-EC7, closure-source ruling - uniform, record _index/candidates/ec7-phyre-uniform-0930): 39 member(s) joined the family under FABLE's closure-source ruling (SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, uniform per SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930): the selector's predicate now ignores accounting state, so an A-measured body or another family's body that passes the module predicate is a closure source (it stays A or stays with its declaring family and is never written here); this restores the 2026-09-30 re-status cascade and the bodies the same exclusion kept out since declaration. Falsified by reading a seeded random sample against this row's description (no misfit) and by check_family_forms (0 MISMATCH); per-family member diff, A-source list and the predicate members owned by other families are in the record."
  - "Phyre PRendering module | C | ../members/phyre-prendering.tsv | 310 | PhyreEngine's PRendering module (Sony middleware: Phyre::PRendering* descriptors, render-pass and surface classes plus their private helpers), not FFXII code: frontier census entries that are vtable slot targets of own-namespace Phyre::PRendering classes (37), plus bodies whose every inbound reference - call/jmp/lea, or a slot of a PRendering-bound class in a COL-validated vtable - comes from members or bound template referrers, iterated to a fixpoint (269). No contiguous span: members concentrate 005Dxxxx-0062xxxx and 006Bxxxx-006Cxxxx where the linker interleaved them. Excluded: 59 ICF-foreign bodies, 1,327 bound-template referrers, A-measured (9 members moved to A after the first declaration - A beats it) and already-declared entries. Controls: ZERO inbound non-member referrers; 130 distinct outbound targets; member-referenced .data cells shared outside are descriptor objects the reflection machinery must touch; 20 foreign-class vtable bodies inside the densest bucket (005Exxxx) stay frontier. Selector: ../members/select_phyre_module.py PRendering 2 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 005E9C20, 005EA0E0 6 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. 12 more left as the exclusive-closure cascade of those departures: re-running ../members/select_phyre_module.py PRendering drops them, and with the departing entries held non-A the selector reproduces the previous file exactly (control). 2026-09-30 (SWE2-EC7, closure-source ruling - uniform, record _index/candidates/ec7-phyre-uniform-0930): 24 member(s) joined the family under FABLE's closure-source ruling (SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, uniform per SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930): the selector's predicate now ignores accounting state, so an A-measured body or another family's body that passes the module predicate is a closure source (it stays A or stays with its declaring family and is never written here); this restores the 2026-09-30 re-status cascade and the bodies the same exclusion kept out since declaration. Falsified by reading a seeded random sample against this row's description (no misfit) and by check_family_forms (0 MISMATCH); per-family member diff, A-source list and the predicate members owned by other families are in the record."
  - "Phyre PPostProcessing module | C | ../members/phyre-ppostprocessing.tsv | 161 | PhyreEngine's PPostProcessing module (Sony middleware), not FFXII code: frontier census entries that are vtable slot targets of own-namespace Phyre::PPostProcessing classes (64), plus bodies whose every inbound reference - call/jmp/lea, or a slot of a bound class - comes from members or bound template referrers, iterated to a fixpoint (100). Concentrated 0064xxxx-0065xxxx (157 of 164). Excluded: 32 ICF-foreign bodies, 383 bound-template referrers, A-measured and already-declared entries. Controls: ZERO inbound non-member referrers; 121 distinct outbound targets; 161 shared .data cells are descriptor objects the reflection machinery registers; 110 foreign-class vtable bodies inside the densest bucket (0065xxxx, shared with PGeometry's neighbourhood) stay frontier. Selector: ../members/select_phyre_module.py PPostProcessing 3 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. 1 more left as the exclusive-closure cascade of those departures: re-running ../members/select_phyre_module.py PPostProcessing drops them, and with the departing entries held non-A the selector reproduces the previous file exactly (control). 2026-09-30 (SWE2-EC7, DD re-status A-drift, record _index/candidates/ec7-dd-adrift-pairing-0930): 4 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the reflected render parameters page (d46835689) DOCUMENTED, and 18 more left as the exclusive-closure cascade of those departures; re-running ../members/select_phyre_module.py PPostProcessing drops exactly these 22 and admits nothing. Control: with only the 4 departed bodies held non-A the selector reproduces the pre-re-status 156-member file exactly; addresses and causing pages in the record. 2026-09-30 (SWE2-EC7, closure-source ruling - uniform, record _index/candidates/ec7-phyre-uniform-0930): 27 member(s) joined the family under FABLE's closure-source ruling (SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, uniform per SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930): the selector's predicate now ignores accounting state, so an A-measured body or another family's body that passes the module predicate is a closure source (it stays A or stays with its declaring family and is never written here); this restores the 2026-09-30 re-status cascade and the bodies the same exclusion kept out since declaration. Falsified by reading a seeded random sample against this row's description (no misfit) and by check_family_forms (0 MISMATCH); per-family member diff, A-source list and the predicate members owned by other families are in the record."
  - "Phyre PSerialization module | C | ../members/phyre-pserialization.tsv | 19 | PhyreEngine's PSerialization module (Sony middleware), not FFXII code: frontier census entries that are vtable slot targets of own-namespace Phyre::PSerialization classes (15 - the whole frontier seed set), plus 7 bodies joined by exclusive closure. Concentrated 0059xxxx as FABLE's runmap estimated. Excluded: 14 ICF-foreign bodies, 40 bound-template referrers. Controls: inbound non-member referrers are 28 edges in 8 zones - game save/serialise code calling the module's public API, the expected pattern for the module every subsystem serialises through; 23 distinct outbound targets; 19 shared .data cells are descriptor objects. Selector: ../members/select_phyre_module.py PSerialization. 1 member left the family 2026-09-17, since measured as A (A beats a declaration): 00598DF0, dropped by re-running the selector. 2026-09-30 (SWE2-EC7, DD re-status A-drift, record _index/candidates/ec7-dd-adrift-pairing-0930): 2 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused how-a-path-is-resolved-to-bytes (30f461a92) DOCUMENTED; re-running ../members/select_phyre_module.py PSerialization drops exactly these two and admits nothing; addresses and causing pages in the record."
  - "Phyre PInputs module | C | ../members/phyre-pinputs.tsv | 103 | PhyreEngine's PInputs module (Sony middleware), not FFXII code: frontier census entries that are vtable slot targets of own-namespace Phyre::PInputs classes (64 - the whole frontier seed set), plus 39 bodies joined by exclusive closure. Concentrated 0086xxxx-0087xxxx entirely, matching FABLE's runmap bucket. Excluded: 36 ICF-foreign bodies, 337 bound-template referrers. Controls: ZERO inbound non-member referrers; 54 distinct outbound targets; 85 shared .data cells are descriptor objects; 105 foreign-class vtable bodies inside the densest bucket (0087xxxx, shared with PHierarchy/PVision code) stay frontier. Selector: ../members/select_phyre_module.py PInputs"
  - "Phyre PFramework module | C | ../members/phyre-pframework.tsv | 47 | PhyreEngine's PFramework module (Sony middleware: PApplicationScript, PApplicationViewport, PInputDevice*, PImGuiInternal - the module the task handled LAST and strictest because FFXII's application classes derive from it), not FFXII code: frontier census entries that are vtable slot targets of own-namespace Phyre::PFramework classes (37), plus 12 bodies joined by exclusive closure in 2 rounds. PFramework registers no PUtility object - it is not one of the fifteen - but owns its own RTTI namespace; an earlier draft that treated only the fifteen registered namespaces as modules mis-attributed these seeds to PhyreCore and was corrected before declaration. Game-derived classes CANNOT contaminate the seed set by construction: a body sitting at a slot of any class whose '@X@Phyre@' mention is not PFramework or PInternal fails the all-bound test. Controls: inbound non-member referrers are 6 edges (0079xxxx/0017xxxx - the game application classes that derive from PFramework, exactly the inbound surface the task predicted); 31 distinct outbound targets; 22 foreign-class vtable bodies inside the densest bucket (0079xxxx) stay frontier. Selector: ../members/select_phyre_module.py PFramework 1 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 007A1640 1 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. Re-running ../members/select_phyre_module.py PFramework drops exactly these."
  - "Phyre PGeometry module | C | ../members/phyre-pgeometry.tsv | 72 | PhyreEngine's PGeometry module (Sony middleware), not FFXII code: 1 frontier own-namespace Phyre::PGeometry vtable slot target plus 71 bodies joined by exclusive call/jmp/lea/bound-slot closure over 6 rounds. Zero inbound non-member referrers; the densest member bucket is shared with PPostProcessing's neighbourhood. Selector: ../members/select_phyre_module.py PGeometry"
  - "Phyre PDynamicGeometry module | C | ../members/phyre-pdynamicgeometry.tsv | 42 | PhyreEngine's PDynamicGeometry module (Sony middleware), not FFXII code: 5 frontier own-namespace Phyre::PDynamicGeometry vtable slot targets plus 34 bodies joined by exclusive closure over 3 rounds. Zero inbound non-member referrers. Selector: ../members/select_phyre_module.py PDynamicGeometry. 2026-09-30 (SWE2-EC7, closure-source ruling - uniform, record _index/candidates/ec7-phyre-uniform-0930): 3 member(s) joined the family under FABLE's closure-source ruling (SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, uniform per SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930): the selector's predicate now ignores accounting state, so an A-measured body or another family's body that passes the module predicate is a closure source (it stays A or stays with its declaring family and is never written here); this restores the 2026-09-30 re-status cascade and the bodies the same exclusion kept out since declaration. Falsified by reading a seeded random sample against this row's description (no misfit) and by check_family_forms (0 MISMATCH); per-family member diff, A-source list and the predicate members owned by other families are in the record."
  - "Phyre PScripting module | C | ../members/phyre-pscripting.tsv | 23 | PhyreEngine's PScripting module (Sony middleware), not FFXII code: 7 frontier own-namespace Phyre::PScripting vtable slot targets plus 25 bodies joined by exclusive closure over 4 rounds. One inbound non-member referrer edge at 0068xxxx. The already-declared PhyreScripting accessor/adapter families stay excluded by construction. Selector: ../members/select_phyre_module.py PScripting 1 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 00685AC0; 12 member(s) left on the 2026-09-20 selector re-run, no longer derived by the selector (returned to the frontier undeclared): 00681C50 and 11 more 1 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. Re-running ../members/select_phyre_module.py PScripting drops exactly these. 2026-09-30 (SWE2-EC7, closure-source ruling - uniform, record _index/candidates/ec7-phyre-uniform-0930): 6 member(s) joined the family under FABLE's closure-source ruling (SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, uniform per SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930): the selector's predicate now ignores accounting state, so an A-measured body or another family's body that passes the module predicate is a closure source (it stays A or stays with its declaring family and is never written here); this restores the 2026-09-30 re-status cascade and the bodies the same exclusion kept out since declaration. Falsified by reading a seeded random sample against this row's description (no misfit) and by check_family_forms (0 MISMATCH); per-family member diff, A-source list and the predicate members owned by other families are in the record."
  - "Phyre PLOD module | C | ../members/phyre-plod.tsv | 30 | PhyreEngine's PLOD module (Sony middleware), not FFXII code: 3 frontier own-namespace Phyre::PLOD vtable slot targets plus 25 bodies joined by exclusive closure over 5 rounds. Zero inbound non-member referrers. Selector: ../members/select_phyre_module.py PLOD. 2026-09-30 (SWE2-EC7, closure-source ruling - uniform, record _index/candidates/ec7-phyre-uniform-0930): 2 member(s) joined the family under FABLE's closure-source ruling (SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, uniform per SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930): the selector's predicate now ignores accounting state, so an A-measured body or another family's body that passes the module predicate is a closure source (it stays A or stays with its declaring family and is never written here); this restores the 2026-09-30 re-status cascade and the bodies the same exclusion kept out since declaration. Falsified by reading a seeded random sample against this row's description (no misfit) and by check_family_forms (0 MISMATCH); per-family member diff, A-source list and the predicate members owned by other families are in the record."
  - "Phyre PGameplay module | C | ../members/phyre-pgameplay.tsv | 19 | PhyreEngine's PGameplay module (Sony middleware - a Phyre namespace with no PUtility registrar), not FFXII code: no frontier own-namespace seed slots; 19 bodies joined purely by exclusive closure from PGameplay-bound template referrers over 4 rounds. Zero inbound non-member referrers. Selector: ../members/select_phyre_module.py PGameplay"
  - "Phyre PHierarchy module | C | ../members/phyre-phierarchy.tsv | 16 | PhyreEngine's PHierarchy module (Sony middleware), not FFXII code: 2 frontier own-namespace Phyre::PHierarchy vtable slot targets plus 15 bodies joined by exclusive closure over 3 rounds. Zero inbound non-member referrers. Selector: ../members/select_phyre_module.py PHierarchy 1 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 00878630"
  - "Phyre PText module | C | ../members/phyre-ptext.tsv | 9 | PhyreEngine's PText module (Sony middleware), not FFXII code: 1 frontier own-namespace Phyre::PText vtable slot target plus 8 bodies joined by exclusive closure over 2 rounds. Zero inbound non-member referrers. Selector: ../members/select_phyre_module.py PText"
  - "Phyre PScene module | C | ../members/phyre-pscene.tsv | 9 | PhyreEngine's PScene module (Sony middleware), not FFXII code: no frontier own-namespace seed slots; 2 bodies joined purely by exclusive closure from PScene-bound template referrers. Zero inbound non-member referrers. Selector: ../members/select_phyre_module.py PScene. 2026-09-30 (SWE2-EC7, closure-source ruling - uniform, record _index/candidates/ec7-phyre-uniform-0930): 7 member(s) joined the family under FABLE's closure-source ruling (SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, uniform per SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930): the selector's predicate now ignores accounting state, so an A-measured body or another family's body that passes the module predicate is a closure source (it stays A or stays with its declaring family and is never written here); this restores the 2026-09-30 re-status cascade and the bodies the same exclusion kept out since declaration. Falsified by reading a seeded random sample against this row's description (no misfit) and by check_family_forms (0 MISMATCH); per-family member diff, A-source list and the predicate members owned by other families are in the record."
  - "Phyre PProfiling module | C | ../members/phyre-pprofiling.tsv | 1 | PhyreEngine's PProfiling module (Sony middleware - a Phyre namespace with no PUtility registrar), not FFXII code: the single frontier own-namespace Phyre::PProfiling vtable slot target. Zero inbound non-member referrers. Selector: ../members/select_phyre_module.py PProfiling"
  - "Phyre module-utility registrars | C | members/phyre-module-utility-registrars.tsv | 13 | toolchain-generated .CRT$XI dynamic initialisers whose registered objects are Phyre's: they register the thirteen frontier-resident P<Module>::PUtility<Module> objects into the bounded module list headed at 02CACC90 documented on this page. PROVED BY FORM + PROVENANCE - 13 members, all 86 bytes, ONE skeleton, no calls, tail-jump the atexit wrapper 00808B90, and every member references the shared list head; each installs the RTTI-verified module vtable named in the table below (PSerialization, PScene, PAnimation, PRendering, PPostProcessing, PGeometry, PPhysics, PDynamicGeometry, PLOD, PInputs, PGame, PHierarchy, PDeveloperExtensions). The other two of the fifteen are already counted elsewhere: 00166210 (PUtilityScripting) and 00167B90 (PUtilityText via 006CCC10) are A-measured - A beats a declaration. NOT dispositioned: the per-module objects and their teardowns. Selector: members/select_xc_array_clusters.py under 24-Compiler-And-CRT-Runtime/Static-Initialization-And-Teardown"
---

# The subsystem registry — fifteen modules, before `main`

> **Before FFXII shows anything, fifteen engine subsystems put themselves on one list.** Rendering,
> animation, physics, input, text, scripting — each is a statically allocated object that links
> itself into one chain, which the engine walks once to start them all and once to stop them.
>
> **For anyone injecting code into this game, that list is the map of what already exists and what
> does not.**

## 1. What the player sees

Nothing, and that is the point: this all happens before the first frame, before the logos, before
anything is on screen.

But it explains a thing every FFXII modder eventually hits. **The engine is not one program that does
everything; it is fifteen subsystems that were each written to be optional**, and each announces
itself at startup by adding its name to a list the engine then walks. Rendering does not know about
physics. Scripting does not know about text. They only know the list.

**That is why a mod that hooks too early sees an engine that is half-built**, and why the order the
list is in matters more than the order the code appears in.

## 2. Native mechanism

### The list

A single global head at **`0x02CACC90`**, an **intrusive singly-linked list** whose nodes are the
module objects themselves — `next` at node `+0x08`, and an ordering key at node `+0x18`.

**33 functions touch that head, 64 references in all**, and they resolve into three groups.

### Registration — one shape, read from `00166210` in full

```asm
00166210  cmp  qword [02CACC90], 0        ; empty list?
00166218  lea  rax, [02CACC90]            ; rax = &head
0016621F  je   0x166238
00166221  mov  rcx, [rax]                 ; walk...
00166224  cmp  dword [rcx+0x18], 0xFF     ; ...while this node's key is < 0xFF
0016622B  jae  0x166238
0016622D  cmp  qword [rcx+8], 0           ; ...and there is a next
00166232  lea  rax, [rcx+8]
00166236  jne  0x166221
00166238  mov  rcx, [rax]                 ; splice: our next = what was here
0016623B  mov  [01F2EAD0], rcx
00166242  lea  rcx, [01F2EAC8]
00166249  mov  [rax], rcx                 ; ...and the slot now points at us
0016624C  lea  rax, [00D6FD98]            ; our vtable
0016625A  mov  [01F2EAC8], rax            ; written into a STATIC object
00166261  jmp  atexit                     ; 00808B90
```

> **The object is static, not heap.** `01F2EAC8` is a fixed address in the image; the initializer
> writes a vtable into it and links it in. **Nothing is allocated, so this cannot fail** — which is
> presumably why it is safe to run before `main`.
>
> **The insertion walks while `node[+0x18] < 0xFF`** — but **every module object carries `0xFF` in
> the image**, so `jae` is taken on the first node and **each module splices at the head.** The
> ordering mechanism exists and the shipped data does not exercise it: unless something lowers a key
> at runtime, the final chain is simply the reverse of registration order. **`DB-3` is answered, and
> the answer is that the priority field is uniform.**

### The fifteen modules

Each appears **twice** among the 33 registrars: once installing its own vtable, once installing the
base `PUtility` vtable at `00D26BC0`. Fifteen modules, thirty functions, plus three shared helpers.

> **⚠ Which of the two is the constructor is settled by the image, and it is not the obvious
> reading.** The second column below was first labelled *destructor* — the C++ teardown idiom of
> downgrading an object to its base vtable. **The static data says otherwise: every one of the
> fourteen readable module objects already holds `00D26BC0` in the image**, with `next = 0` and the
> ordering key at `0xFF`. That is the *pre-`main`* state, so `00D26BC0` is the value the object
> starts with — consistent with **`PUtility::PUtility()`, the base constructor, doing the list
> insertion**, after which the derived constructor overwrites the vtable with its own.
>
> **What is established: fifteen functions install the derived vtable and fifteen install the base
> vtable into the same objects.** ~~Which is ctor-versus-base-ctor and which is ctor-versus-dtor is~~
> ~~**not** established, and the column is headed accordingly.~~ The base-vtable column is the destructor column *(corrected 2026-10-02, OPUS: the registrar `00167810` passes `008B6A40` to `atexit` (`00167810+0x43`, `00167810+0x51`), and `008B6A40` re-stamps the base vtable `00D26BC0` into `01F2EE60` (`008B6A40+0x8`, `008B6A40+0xF`) before unlinking; the answer block below)*.

| static object | class | installs derived vtable | installs base vtable |
|---|---|---|---|
| `01F2CD80` | `PSerialization::PUtilitySerialization` | `00160320` | `008A8CE0` |
| `01F2CDF8` | `PScene::PUtilityScene` | `00160380` | `008A8DC0` |
| `01F2CE20` | `PAnimation::PUtilityAnimation` | `001610E0` | `008AAD40` |
| `01F2D680` | `PRendering::PUtilityRendering` | `00162B70` | `008AE6D0` |
| `01F2E800` | `PPostProcessing::PUtilityPostProcessing` | `00165420` | `008B0B40` |
| `01F2E9B8` | `PGeometry::PUtilityGeometry` | `00165EA0` | `008B1A60` |
| `01F2EAC8` | `PScripting::PUtilityScripting` | `00166210` | `008B2670` |
| `01F2EB00` | `PPhysics::PUtilityPhysics` | `00166C30` | `008B3E30` |
| `01F2EE60` | `PDynamicGeometry::PUtilityDynamicGeometry` | `00167810` | `008B6A40` |
| `01F2EE80` | `PLOD::PUtilityLOD` | `00167870` | `008B6AA0` |
| `01F44D70` | `PInputs::PUtilityInputs` | `0016AB40` | `008B9890` |
| `01F44FE8` | `PGame::PUtilityGame` | `0016AEC0` | `008BA260` |
| `01F47550` | `PHierarchy::PUtilityHierarchy` | `0016D5B0` | `008C1580` |
| `01F47570` | `PDeveloperExtensions::PUtilityDeveloperExtensions` | `0016D610` | `008C15E0` |
| `02E5BE88` | `PText::PUtilityText` | `006CCC10` (via `00167B90`) | `008B6F00` |

**Every class name is read from the vtable's RTTI complete-object-locator**, not from adjacency or a
guess.

> *Corrected 2026-09-14 (FABLE, `DB-1` below): both installers use `02E5BE88`. `02E5BE50` is a seven-pointer table the
> constructor fills first.* ~~**`PText` is the one irregularity**: its two installers use `02E5BE50` and `02E5BE88`, **`0x38`
> apart**~~ — where the other fourteen use one address for both. **It is also the only object absent
> from the image's raw data**: `02E5BE50` lies in BSS, so unlike the other fourteen it has no static
> initial vtable, `next` or key to read. Either the text module is a larger object whose base
> sub-object sits at `+0x38`, or the pairing is not what it looks like. **Not resolved here.**
> `DB-1`.

**And `PText` is also the only one whose object lives at `02E5Bxxx`** rather than the `01F2Cxxx`–
`01F47xxx` band the other fourteen share.

### Who walks the list

| address | size | role |
|---|---:|---|
| `005A08E0` | 507 B | **engine init** — walks the chain calling each module's slot `+0x08` |
| `005A0840` | 145 B | **engine shutdown** — walks the chain calling each module's slot `+0x10` |
| `005A0CB0` | 100 B | slot `+0x00` of every module vtable — ~~**body unread**~~ *(answered: see the 2026-09-14 answer block - the modules' shared scalar deleting destructor; 2026-10-02, OPUS)* |

> **Crossings into Resource and Platform — FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** The walkers bracket the module
> list with three platform-layer calls.
>
> - **Init, `005A08E0`.** Early in the walker, at `005A092D`, it calls `00677450`. That helper creates the
>   synchronisation object at `02D3E880` through a platform helper that reaches `CreateEventA`, and returns `0x16` if the
>   object already exists. The ledger files `00677450` under **Resource**.
> - **Timer, also in `005A08E0`.** At `005A0A63` it calls a timer and stores the result at `02CB60E8`. The timer is
>   `QueryPerformanceCounter` divided by the frequency held at `02CB6120`, which gives seconds as a double. The ledger
>   files it under **Platform**. The framework's `%f` option parser `00799980` later subtracts that stored start time
>   ([the Yebis source map](../../23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md) note).
> - **Shutdown, `005A0840`.** At `005A088F` it calls `00677520`, which closes the same object through a platform
>   helper that calls `CloseHandle`. It returns `0x15` if the object was never created. The ledger files it under **Resource**.
>
> None of the three is a resource or asset operation.

The two walkers are called from `00798603`, `007986D5` and `00798886`. **`005A0CB0` has no direct
callers because it is a virtual slot** — the function at offset 0 of `PUtilityScripting`'s vtable
`00D6FD98`, and by construction of the base class, of every module's.

### ⚠ The registry is walked exactly twice per run — `DB-2` answered

**It is a lifecycle manifest, not a per-frame dispatch table.**

```asm
; init, 005A0A27
005A0A27  mov  rbx, [02CACC90]        ; the head
005A0A33  mov  rax, [rbx]             ; the module's vtable
005A0A39  call qword ptr [rax + 8]    ; slot +0x08 = per-module INIT
005A0A3C  test eax, eax
005A0A3E  jne  0x5a0ad5               ; NON-ZERO ABORTS THE WHOLE STARTUP
005A0A44  mov  rbx, [rbx + 8]         ; next
005A0A4B  jne  0x5a0a33

; shutdown, 005A0860
005A0860  mov  rax, [rbx]
005A0866  call qword ptr [rax + 0x10] ; slot +0x10 = per-module SHUTDOWN
005A0869  mov  rbx, [rbx + 8]         ; next; return value ignored
005A0870  jne  0x5a0860
```

> **Any one of the fifteen modules can abort engine startup by returning non-zero from its init**, and
> the walk stops where it fails — every module after it in the chain is never initialised. **Shutdown
> ignores return values entirely**, which is the usual asymmetry: failing to start is fatal, failing
> to stop is not.

**Both are guarded by one flag at `0x02CACCA0`**, so both are idempotent: init returns immediately if
the flag is set, shutdown if it is clear. **Init allocates a `0xE0`-byte object at ~~`01F3F5B8`~~ `01F7F5B8`** *(corrected 2026-10-02, OPUS: `005A08FC mov ecx, 0xE0`, `005A0919` stores the result to `01F7F5B8`; nothing references `01F3F5B8`)* and
**registers `005A0840` with `atexit`** (`lea rcx, [rip-0x287]` at `005A0AC0`, then
`call 00808B90`) — ~~so the shutdown walk runs at process exit, not from game code.~~ and the start-up function also calls it directly *(corrected 2026-10-02, OPUS: `007980A0` calls `005A0840` at `007986D5` and `00798886`; the guard byte `02CACCA0`, tested at `005A0844` and cleared at `005A08C5`, makes the first call do the walk and the `atexit` one a no-op - as the-game-is-a-phyre-application.md's shutdown sequence says)*.

**So each module's vtable has a known lifecycle contract:**

| slot | role |
|---|---|
| `+0x00` | shared `005A0CB0` — ~~**unread**~~ the shared scalar deleting destructor *(answered: see the 2026-09-14 answer block; 2026-10-02, OPUS)* |
| `+0x08` | **init**, returns 0 for success; non-zero aborts startup |
| `+0x10` | **shutdown**, return ignored |

*The ledger tags both walkers `Phyre.Runtime.UtilityThreadPoolOrchestration`. **Nothing in either
body read here is thread-pool work** — that tag is the ledger's claim and this document does not
adopt it.*

## 3. Key addresses

| address | what |
|---|---|
| `0x02CACC90` | the registry list head |
| `0x00D26BC0` | the base `PUtility` vtable every destructor installs |
| `00166210` | the registration shape, read in full |
| `00808B90` | `atexit` — every registrar tail-calls it |
| `005A08E0`, `005A0840` | the two list walkers |
| `005A0CB0` | vtable slot 0, shared by all fifteen — ~~body unread~~ *(answered: see the 2026-09-14 answer block; 2026-10-02, OPUS)* |
| `0x008C31D8` | the CRT initializer table these fifteen are reached from |

### The `005A08E0` exclusive subtree — all 11 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the init walker **11 frontier functions** — the machinery the
`slot +0x08` walk is bracketed by: the manager object it allocates, the timer it calibrates, the
reflected-type lists it builds, and the bucket index it finishes with. Interior cites are one
instruction inside each declared extent (`interior_cite.py scan`; no boundary crossings).

| member | size | role | interior |
|---|---:|---|---|
| `0062EA20` | 51 B | ctor for the `0xE0` object the root stores at `01F7F5B8` — eh-vector build of 4 × `0x38` records (element ctor `0062EB20`, dtor `0062EAE0`) through `` `eh_vector_constructor_iterator' `` `00808FE4` | `0062EA26` |
| `00677450` | 27 B | create-once gate for the sync object at `02D3E880`: returns `0x16` when the flag byte is already set, else tail-jumps `005CD0A0` (the `CreateEventA` create of §2) | `00677457` |
| `005CC980` | 295 B | high-resolution timer calibration — `timeBeginPeriod(5)` (IAT `008C2A98`, success flag `02CB60F0`), `Sleep(0)` (`008C21B0`), `timeGetTime` → `02CB60F4` (`008C2A88`), `QueryPerformanceFrequency` → `02CB6120` and period `1.0/freq` → `02CB6128` (`008C2190`), `QueryPerformanceCounter` → `02CB6118`/`02CB6108` (`008C2188`); returns `0x17` when neither timer source came up | `005CC984` |
| `00686C40` | 186 B | second registration battery — 21 no-arg inits (including `00617810`, the `PUtilityDynamicGeometry` registrar of the §2 table) plus 6 factory→`006388C0` register pairs (`00613E80` — interior read 2026-09-17 (SWE2-FRONTIER): 1,319 B, `02EAED3C` count gate at `00613E99`, `008092FC`/`0080929C`/`00808B90` driver thunks ×11 each, first call [`00613ECC`](../../_index/ADDRESS-INDEX.md) — /`006143B0`/`00613A30`/`00614640`/`00613800`/`00612550`; `00613A30` and `00614640` verified the same day: 1,097 B and 1,093 B, the identical `008092FC`/`0080929C`/`00808B90` ×9 registration battery, first calls [`00613A7C`](../../_index/ADDRESS-INDEX.md)/[`0061468C`](../../_index/ADDRESS-INDEX.md)) | `00686C4E` |
| `006AA380` / `006AA360` / `006AA350` | 7 B each | one-field config setters — `ecx` → `01F2EB34` / `01F2EB38` / `01F2EB3C`, called by the root with `0x40000` / `0x8000` / `0x800`; `006AA280` then spends `01F2EB30`–`01F2EB3C` sizing the `02E4E610` object the root virtual-calls | `006AA386` / `006AA366` / `006AA356` |
| `00637F20` | 2,454 B | 13-arm lazy-init battery — each arm gates on a TLS slot (`02EAED3C` index into `gs:[0x58]`) against once-counters `02CF94F0`–`02CF9520`, runs `_Init_thread_header`/`_Init_thread_footer` + `atexit(008AFxxx)`, builds a `0x50`-stride sentinel record at `01F2E370`–`01F2E730` (self-linked list heads, vtables `00D58A08`–`00D58D80`), and registers it into the name map through `006388C0` (the first arm registers `02CF8470` as well) | `00637F2A` |
| `00637A70` | 476 B | two-pass rebuild over the `006373D0` registry's `01F2E340` list — pass 1 (state `01F2E350` = 1) sums each node's `+0xF0` chain into `+0xF4`/`+0xF8`; pass 2 (state 2) calls `vt+0x60`, `00639A60(0)`, `00639C80(0)` on nodes whose `+0xFC` is non-negative with bit 30 set | `00637A7F` |
| `00634350` | 136 B | `count`×`0x18` node-pool allocator via `0017D260`; sentinel-inits each record `{0, 0, −1, −1}` — its only corpus caller is `00638AE0` | `00634362` |
| `00638AE0` | 419 B | per-kind bucket index — allocs `[02CF8260]+1` records via `00634350`, walks `006373D0`'s `+0x10` list bucketing nodes by `+0xE8` kind (`rbx + kind*24`), writes `+0xEC` link cursors, stores the node count at `02CF8264`; `0xd` on alloc failure, freed via `00584730` | `00638B0B` |

`006388C0` — the shared registrar all these arms feed — reads the name string at `[node+0x30]`,
hashes it (`edx = 0x7B5`, `×0x21 + (c & 0x1F)`), and splices `node+0x08` into the `00637440` map
(`0067F700`), ~~returning `0x12` on a duplicate insert.~~ returning a bool *(corrected 2026-10-02, OPUS: `0x12` is only an internal code, `0063898A`; the result is `sete al` at `006389A1`, so a duplicate insert or an already-present name (`0063894A`) returns false and a fresh insert true)*.

So the init walk's exclusive reach is mostly *registration*, not gameplay: reflected-type
lists, a name-keyed map, a sync object, and timer calibration — the modules' own
world-building, kept out of the shared callee pool because only this walker ever calls it.

### The `PAnimation` module declared as one family — the per-module provenance pilot (2026-09-16, SWE2-EC7)

The first module-level C row uses this page's own machinery: the linker placed `Phyre::PAnimation`'s
code in the contiguous span `005A0000`–`005D0000` (1,345 census entries), and the selector
[`select_phyre_panimation.py`](../members/select_phyre_panimation.py) claims the **203 frontier
entries that the image's own RTTI and reachability attribute to the module** (the selector
re-derives on every run — the row was 218 at declaration and shrinks as interior citations move
members to A; 33 are now A-measured, A beats a declaration):

- **Seeds (67)** — vtable slot targets whose slot belongs to an *own-namespace*
  `Phyre::PAnimation` class: the selector re-walks `.rdata`, validates all 2,286
  complete-object locators by self-reference (reproducing the vtable index's documented count
  exactly), demangles each class name, and keeps non-template classes whose first module mention
  is `PAnimation`.
- **Closure (136, seven rounds to fixpoint)** — a span entry joins only when *every* inbound
  reference to it — `call`/`jmp`/`lea`, or a vtable slot — comes from a member or from a
  *PAnimation-bound referrer*: a template body whose every module mention is `PAnimation` or
  `PInternal` (205 such; they are the descriptor/caller machinery, bound but not owned).

What the rule refuses is as important as what it claims. The span is not pure: hundreds of entries
are already declared by the generated reflection families, 43 vtable slots belong to foreign classes
the linker parked here (`PClassDescriptor*<PRendering::*>` below the upper edge,
`PTypeDefault`, `PCaller`, `PInternal` visitors), 11 bodies are **ICF-folded across modules** —
`005C51F0` sits in `PMethodCallerConcrete` instantiations for *both* `PAnimatableComponent` and
`PPhysicsRigidBody`, so no PAnimation-exclusive edge exists through it — and 113 bodies are
reached from outside the module's evidence chain. The A-measured members (including the two
walkers and the shared slot-0 body) stay out by the standing rule.

Controls are printed on every run: 74 distinct outbound call targets (Phyre core reflection
helpers `0063xxxx`, sibling Phyre zones, CRT, imports), exactly 2 inbound non-member referrer
edges (`006Axxxx`, `0017xxxx`), and `.data` cells members share with non-member code — those
cells are the module's descriptor objects at `01F2CExx`, which the in-span bound-template
referrers (`005Cxxxx`) and the reflection-machinery zone (`0016xxxx`) *must* also touch to
register them; sharing the records they exist to file is expected, not a boundary leak. The edge controls hold: `0059FFC0` below has no PAnimation class,
`005D0000` above is a `PRendering` descriptor.

This is the pilot the other fourteen module rows copy: same method — image-derived vtables,
own-namespace seeds, bound-template referrers, exclusive closure — one span at a time.

### The `PhyreCore` module declared as one family — the generalised selector (2026-09-16, SWE2-EC7)

`select_phyre_module.py PhyreCore` generalises the pilot for the modules the linker gave **no
contiguous span**: core code is interleaved through the whole image — the members sit in 36 of the
64KB zones from `0015xxxx` to `0087xxxx` — so membership carries no geographic bound and exclusivity
does the work. **477 members**: 93 own-namespace seed slots plus 384 bodies joined by exclusive
closure in 11 rounds.

Two name rules differ from the pilot, because "the core" is defined negatively:

* **Core-bound class** — every `@X@Phyre@` mention is a **non-module** name: `PWorld`, `PInternal`,
  the `VP*`/`PE*` machinery encodings, the container templates. `.?AVPWorld@Phyre@@` (no module
  segment) and `.?AVPWorldBullet@PWorld@Phyre@@` (a core sub-namespace) both qualify.
* **Module set** — the fifteen registered namespaces **plus four more that own an RTTI namespace
  without a `PUtility` registrar**: `PFramework`, `PGameplay`, `PVision`, `PProfiling`. The first
  draft of this selector equated "module" with the fifteen and wrongly absorbed 109 foreign bodies
  (37 `PFramework` own-namespace seeds among them); the image's own namespace census caught it
  before declaration.
* **Own-namespace seed** — a non-template class under `@Phyre@` with no module mention. The
  `@Phyre@` presence check matters: a plain global class `.?AVFoo@@` is not Phyre at all.

Controls: 2,178 bound-template referrer bodies stay referrers (the reflection/container machinery
is what makes the core's referrer set the largest of any module); outbound calls reach 288 distinct
non-member targets across Phyre zones, game code, CRT and imports — the core is the library
everything calls; inbound non-member referrers are 14 edges in 9 zones, the public API surface the
game and sibling modules legitimately call; 176 member-referenced `.data` cells are shared outside —
descriptor objects and shared allocator/registry state, the same expected-sharing pattern as
PAnimation's.

### The remaining module rows (2026-09-16, SWE2-EC7)

The same selector, one row per module, in the task's largest-frontier-first order. Fifteen more
families landed after `PhyreCore` — the task's six named modules plus every other Phyre namespace
that yields frontier members under the same rule:

| module | members | seeds | joined | inbound non-member refs | densest zone |
|---|---|---|---|---|---|
| `PPhysics` | 95 | 39 | 56 | **0** | `0069xxxx` (53) |
| `PRendering` | 306 | 37 | 269 | **0** | `005Exxxx` (83) |
| `PPostProcessing` | 164 | 64 | 100 | **0** | `0065xxxx` (105) |
| `PSerialization` | 22 | 15 | 7 | 28 — the API every subsystem serialises through | `0059xxxx` (17) |
| `PInputs` | 103 | 64 | 39 | **0** | `0087xxxx` (55) |
| `PFramework` | 49 | 37 | 12 | 6 — game application classes deriving from it, exactly the predicted surface | `0079xxxx` (35) |
| `PGeometry` | 72 | 1 | 71 | **0** | shared with `PPostProcessing`'s neighbourhood |
| `PDynamicGeometry` | 39 | 5 | 34 | **0** | — |
| `PScripting` | 32 | 7 | 25 | 1 | — |
| `PLOD` | 28 | 3 | 25 | **0** | — |
| `PGameplay` | 19 | 0 | 19 | **0** | — |
| `PHierarchy` | 17 | 2 | 15 | **0** | — |
| `PText` | 9 | 1 | 8 | **0** | — |
| `PScene` | 2 | 0 | 2 | **0** | — |
| `PProfiling` | 1 | 1 | 0 | **0** | — |

`PFramework` was handled last and strictest as the task required: it owns an RTTI namespace but no
`PUtility` object, and FFXII's application classes derive from it — a body at a slot of any
non-`PFramework`-bound class fails the all-bound test, so game-derived classes cannot contaminate
the seed set. Every module's exclusion tail — A-measured, already-declared, ICF-foreign bodies,
bound-template referrers, and frontier bodies not exclusively reached — stays frontier.

Zero frontier members under the rule: `PGame`, `PVision`, `PDeveloperExtensions` — their
own-namespace surfaces are already dispositioned or empty, which is itself the selector's verdict
rather than a gap in coverage.

## 4. Modding notes

- **All fifteen exist before `main`.** They are static objects; their addresses are fixed in the
  image and are listed above, so a tool can read a module's vtable pointer to check it is
  constructed.
- **Inject after `main`, not before** — the standing advice in
  [`../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md)
  — and this is the concrete list of what that initializer run builds.
- **The chain order is data, not code order.** Insertion walks while `node[+0x18] < 0xFF`, so
  changing a module's key changes where in the sequence the walkers reach it.
- **The list head is one pointer.** Anything that walks the engine's subsystems starts at
  `0x02CACC90`, and a tool can enumerate the live modules from it without knowing any of the fifteen
  addresses in advance.
- **Slot 0 of every module vtable is the same function**, `005A0CB0`: the scalar deleting destructor, which unlinks
  the module from the head `0x02CACC90` before an optional 32-byte free (UQ-294). It is shared, so a change there
  reaches all fifteen.

## 5. What is not known

- [x] ~~What the walkers do.~~ **`DB-2` answered — init and shutdown, once each per run.** Slot
  `+0x08` initialises and **can abort startup**; slot `+0x10` shuts down. Not a per-frame dispatch
  table.
- [x] ~~**UQ-294.** **What slot `+0x00` (`005A0CB0`, 100 B) is.** The one part of the module lifecycle contract
  still unread. `DB-5`.~~ **Answered 2026-09-14 (FABLE): the modules' shared scalar deleting destructor, which also
  unregisters the module.** `005A0CB0(this, flags)` does three things:
  1. It re-stamps the base vtable `00D26BC0`, whose own slot 0 is this function (`005A0CB6`–`005A0CC0`).
  2. It walks the chain from the head `02CACC90` through each node's `+0x08` until it finds `this`, then splices it
     out: the predecessor's link takes `this->next`, and `this+0x08` is cleared (`005A0CC3`–`005A0CF4`). An empty chain,
     or one that no longer contains `this`, is left alone.
  3. When bit 0 of `flags` is set, it frees the object as a **32-byte** allocation (`free(this, 0x20)`,
     `005A0CFC`–`005A0D06`). It returns `this`.

  So the lifecycle is `+0x08` init, `+0x10` shutdown, and `+0x00` destroy-and-unlink. Replacing slot 0 changes how
  every module leaves the chain.
- [x] ~~What `node[+0x18]` means.~~ **`DB-3` answered — it is `0xFF` in all fourteen readable module
  objects**, so the ordered walk terminates on the first node and every module inserts at the head.
  The ordering mechanism is present and unexercised by the shipped data. **What the key would mean
  if something set it lower is still unknown.**
- [x] ~~**UQ-295.** **Whether anything lowers a module's key at runtime.** If nothing does, the chain order is
  fixed and is the reverse of CRT initializer order. `DB-4`.~~ **Answered 2026-09-14 (FABLE): nothing does, so the
  order is fixed.**
  - **No absolute reference.** No instruction in the image references `+0x18` of any of the fifteen module objects
    `rip`-relatively.
  - **Every function that touches the head is accounted for.** There are 33: the fifteen registrars, the fifteen
    `008Axxxx`–`008Cxxxx` bodies, the shared slot-0 destructor, and the two walkers `005A0840` and `005A08E0`. Among
    them the only store to a module's `+0x18` is `mov dword [rcx+0x18], 0xFF` in the BSS text module's constructor
    `006CCC10` (`006CCC17`). That writes the same value every other module carries in the image.
  - **The walker's `+0x18` is a different thing.** `005A0840` uses `+0x18` only as a vtable slot
    (`call [rdx+0x18]`, `005A0882`), not as the key.
  - **A side result settles the ⚠ above.**
    - The derived-vtable installers are the static constructors. `00166210` links the object into the chain, writes
      its derived vtable, and tail-jumps `atexit` with `008B2670` as the argument (`00166253`–`00166261`).
    - The base-vtable installers are those `atexit` teardowns. `008B2670` re-stamps `00D26BC0` and unlinks the object
      from the head, with no free (`008B2670`–`008B26C4`).
    - So the `008Axxxx`–`008Cxxxx` column is the destructor column, registered for process exit.
- [x] **`PText`'s `0x38` offset** between the object its two installers use. **Its object is also the
  only one not present in the image's raw data at all** — `02E5BE50` lies in BSS, so it has no static
  initial value to read. `DB-1`.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (DB-1): there is no offset. Both installers use
  `02E5BE88`, and `02E5BE50` is a separate seven-slot table the constructor fills.*
  - **The object is `02E5BE88`.** The static initialiser `00167B90` passes `lea rcx, [02E5BE88]` to `006CCC10`
    (`00167B94`–`00167B9B`) and registers `008B6F00` with `atexit` (`00167BA0`–`00167BAB`).
  - **`006CCC10` constructs it like the other fourteen:** base `PUtility` vtable `00D26BC0` first, key `+0x18 = 0xFF`, name
    `+0x10` = `"Text"` (`00D89C80`), ordered insertion into the module chain `02CACC90`, then the derived vtable
    `00D89C68` (`006CCC10`–`006CCC68`). `tools/rtti_bcd.py` names that vtable `PUtilityText@PText` over base `PUtility`.
  - **Then it fills `02E5BE50`–`02E5BE80`** with seven pointers to consecutive `0x20`-byte slots `02E5BEA8`–`02E5BF68`
    (`006CCC6B`–`006CCCC6`). That store is the first one in the function, which is why `02E5BE50` was read as the object.
    It is module-private storage beside the object.
  - **`008B6F00` unlinks `02E5BE88`** and restores the base vtable (`008B6F08`–`008B6F49`), matching the constructor.
  - **Why it is in BSS.** The object and its table live in zero-initialised storage, and the constructor writes every field.
    The other fourteen have initialised images in `.data`. That is a difference in how the object was declared, not in
    the pairing.
- [x] ~~**UQ-296.** Whether the three functions at `00798603` / `007986D5` / `00798886` that call the walkers are
  themselves reachable from game code, or are further middleware plumbing.~~ **Answered 2026-09-14 (FABLE):** they are not three functions. They are three call sites inside **one** 2,153-byte function, the framework start-up, which the console pages also record as the `GameSettingConfig` singleton's allocator. That function is on the process's only start-up path. Raw-call chain, each step with a single caller:
  - **The PE entry point** (the optional header's `AddressOfEntryPoint`, 18 B) runs `__security_init_cookie` and jumps to the CRT common-main body (330 B).
  - **The CRT common main** calls a 45-byte main wrapper once.
  - **The wrapper** asks `KERNEL32!IsDebuggerPresent` and calls the framework start-up on either branch, keeping its return value.
  So the walkers run once, from `main`, before the game loop; they are not detached middleware.
  *(The chain is named by role and size: the entry point belongs to a generated function family, and citing the start-up body's entry would import neighbours that belong to other pages.)*

## 6. Evidence

| claim | evidence | tier |
|---|---|---|
| Single list head at `02CACC90`, 33 registrars, 64 refs | `data_xref_scan.py` with a passing control | 1 |
| The registration shape | complete disassembly of `00166210` | 1 |
| The objects are static, in the image | the `mov [rip+disp], rax` target of each registrar | 1 |
| Ordered insertion on `node[+0x18] < 0xFF` | the walk loop at `00166221`–`00166236` | 1 |
| The fifteen class names | each vtable's RTTI complete-object-locator, type-descriptor name | 1 |
| Fifteen functions install the base `PUtility` vtable | all fifteen install the same `00D26BC0` into the fifteen objects | 1 |
| **Those fifteen are constructors, not destructors** | ~~**not established**~~ **refuted: they are the exit-time destructors** *(corrected 2026-10-02, OPUS: `00167810+0x43`/`00167810+0x51` hand `008B6A40` to `atexit`; `008B6A40+0x8`/`008B6A40+0xF` re-stamp `00D26BC0`)* — the image's initial vtable is already `00D26BC0`, which is consistent with a base constructor but does not prove it | 8 |
| The ordering key is `0xFF` in every readable module object | read from `.data` at object `+0x18`, 14 of 15 (`PUtilityText` is in BSS) | 1 |
| Every registrar tail-calls `atexit` | `jmp 0x808b90`, and `00808B90` is named `atexit` in the ledger | 2 |
| `005A0CB0` is vtable slot 0 | it is the first entry after the RTTI pointer at `00D6FD98` | 1 |
| Init walks calling slot `+0x08`; non-zero aborts startup | `005A0A27`–`005A0A4B`, disassembled | 1 |
| Shutdown walks calling slot `+0x10`, return ignored | `005A0860`–`005A0870`, disassembled | 1 |
| One guard flag at `02CACCA0` makes both idempotent | the `cmp`/`mov` pair at `005A08EF` / `005A0ACC` and `005A0844` / `005A08C5` | 1 |
| Init registers shutdown with `atexit` | `lea rcx,[rip-0x287]` → `005A0840`, then `call 00808B90` | 1 |
| **Slot `+0x00`'s role** | ~~**not established — `005A0CB0` unread**~~ *(answered: see the 2026-09-14 answer block - destroy and unlink; 2026-10-02, OPUS)* | — |

## 7. Related

- [`../Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`](../Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md)
  — `PUtilityScripting`, the module this registry was found through.
- [`../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md)
  — the 1,172-entry table that runs these fifteen registrars.
- [`phyre-subsystem-map.md`](phyre-subsystem-map.md) — the RTTI-derived subsystem identity map; **this
  document is fifteen of those subsystems seen from the runtime side.**

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py --addr 02CACC90 --addr 00166210` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment: it returns this
page, `embedded-lua-and-phyre-object-bindings.md` and the answered `DA-2`. Nothing below is offered
as new.)*

### The reference census reproduces, and its shape explains itself

| claim | measured |
|---|---|
| "**33 functions** touch that head, **64 references** in all" | **64 references in 33 distinct functions** — both figures, both units |

The breakdown is the part worth having, because it accounts for the page's own arithmetic:

| form | count | what it is |
|---|--:|---|
| `lea rax, [02CACC90]` | **31** | take the address of the head |
| `cmp qword ptr [02CACC90], 0` | **31** | is the list empty? |
| `mov rbx, qword ptr [02CACC90]` + `test rbx, rbx` | **2** | read the head and NULL-check it |

**One `cmp` and one `lea` per insert site, so 31 inserters and 2 readers — 33 functions.** §2 says
*"fifteen modules, thirty functions, plus three shared helpers"*; the census says the three helpers
are **one further inserter and the two readers**, which is what 30 + 3 = 33 resolves into.

> The pairing is not incidental. `rax` ends up holding **either `&head` or `&node->next`**
> (`0016621F` falls through to `lea rax, [rcx + 8]`), so the splice `mov [rax], rcx` is the same
> instruction whether the module goes at the head or mid-chain. That is why the head is *addressed*
> exactly as often as it is *tested*, and loaded as a value only twice in the whole image.

`00166210` reproduces instruction for instruction at every address §2 quotes — the emptiness test,
the `lea` of the head, the `cmp dword [rcx+0x18], 0xff` walk guard, the `lea rax, [rcx+8]` advance,
and the two-store splice.

### `DB-3`'s answer holds, and the "fourteen" is exact

§3 says *"every one of the **fourteen** readable module objects already holds `00D26BC0` in the
image, with `next = 0` and the ordering key at `0xFF`."* Read out of the image:

| | |
|---|---:|
| module objects listed | 15 |
| present in the raw image | **14** |
| of those, vtable `00D26BC0` **and** `next == 0` **and** key `== 0xFF` | **14 / 14** |
| any object differing on any of the three | **0** |

And the fifteenth is not a gap in the reading: **`PUtilityText`'s object at `02E5BE88` (*corrected 2026-09-14 from `02E5BE50`, `DB-1`*) lies outside
the raw data** — in the uninitialised tail of `.data` — so there is nothing to read. That is
precisely why the count is fourteen and not fifteen, which §3 states without saying why.

So the ordering field is uniform across every object that exists in the file, the walk's `jae` is
taken on the first node every time, and **`DB-3`'s answer — the priority mechanism exists and the
shipped data does not exercise it — stands on a complete reading rather than a sample.**

### Nothing was found wrong

Every figure, address, field value and structural claim this pass could reach reproduced.

**Not claimed:** the fifteen class names come from RTTI locators that were **not** re-walked here;
the base-vtable column's ctor-versus-dtor question is untouched, and §3 already marks it unresolved.
Nothing was executed or observed live.

## The `005A0840` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`005A0840` (145 B) is the atexit shutdown walker the page already names; the
subtree owns the four helpers it calls on the way down. The body: gate on
`[02CACCA0]` (`005A0844`), walk the `[02CACC90]` module list calling
`vtable+0x10` per node (`005A0860`–`005A0870`), then `005CCB90` →
`006AA280`→`vtable+0x18` (`005A087C`–`005A0882`) → `00638C90` → `0016D6A0` →
`00677520` → drain the `[01F7F5B8]` list through `0062EAF0` → `00809950`, then
`[01F7F5B8] = 0`, `[02CACCA0] = 0` (`005A08BA`–`005A08C5`).

| member | role | interior |
| --- | --- | --- |
| `005CCB90` (12 B) | import thunk — `ecx = 5`, tail-jump through IAT slot `008C2AA0` (qword `01CCE944`) | [`005CCB95`](../../_index/ADDRESS-INDEX.md) |
| `0062EAF0` (40 B) | scoped per-node call — `0x38` frame, `[rsp+0x20] = -2` cookie, `edx = 0x38`, `r8d = 4`, `r9 = 0062EAE0` (the real per-node body), then `00809054` | [`0062EAFD`](../../_index/ADDRESS-INDEX.md) |
| `00638C90` (621 B) | epoch-gated deferred-destruction reaper — `gs:[0x58]` TEB, per-thread slot `rax[[02EAED3C]]`, local counter at `slot+4` vs global epoch `[02CF94EC]` (`00638CD7`); when stale, loops `00638D78`–`00638EF8` unlinking nodes from the `01F2E340` intrusive list (`[rcx+8]=next`, `self-link` reset at `00638D31`–`00638D3F`), destroys each `node-0x50` record via `008092FC`/`00808B90`/`0080929C` | [`00638D31`](../../_index/ADDRESS-INDEX.md) |
| `00677520` (42 B) | close-once guard — `[02D3E880] == 0` → return `0x15` (the 21 modules); else `005CD6D0(&02D3E880)` → 0 (`0067752B`–`00677549`) | [`0067752B`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `006AA280`, `0016D6A0`, `00809950`,
`00809054` (scope helper), `005CD6D0`, `008092FC`/`00808B90`/`0080929C` (the
record teardown trio), `0062EAE0` (the drained node's real body).


### Interior citation — frontier hub `00639C80` (2026-09-18, SWE2-EC7)

`00639C80` — 1,160 B, 12 callers: the dual-buffer region init the module
registration runs. Read from the shipping image: `[rcx+0xC8]` and `[+0xD0]`
must both exist or it early-outs; `dword[rsi+0xFC]` loses bits
`0x18000000` (`and 0xE7FFFFFF`); `00861EC0` then 0xFF-fills `[+0xC8]` for
`[+0x38]` bytes and zero-fills `[+0xD0]` the same length
([`00639CD3`](../../_index/ADDRESS-INDEX.md)); cursor ends are computed at
`base + [+0xF8]`, and the `[rsi+0x78]` chain is walked with `006372B0` /
`0063C1A0` validating each linked record's `+0x38` bound against the
caller's. The layout-validation pass the tags name.
## SWE2-EC7-50 update (2026-09-19) - `006AA280`

`006AA280` (181 B) is a body - `006BA880`/`006CE5B0`/`00808B90`/`0080929C`/`008092FC`. Interior anchor `006AA2A8` (a `006BA880` call).

## SWE2-EC7-57 update (2026-09-19) - `006BA880`

`006BA880` (185 B) is a pre-main module body - `006AA180`/`00808FE4` plus `00D81200`. Interior anchor `006BA8A0` (a `006AA180` call).

## SWE2-EC7-59 update (2026-09-19) - `006CE5B0`

`006CE5B0` (160 B) is a pre-main module body - `006AA180`/`00808B90`/`0080929C`/`008092FC` plus `00D8A730`/`02E5C930`/`02E5C938`/`02E5C968` and the `"0R\\"` literal. Interior anchor `006CE5FE` (a `008092FC` call).


## SWE2-EC7-78 update (2026-09-20) - `006AA180` module-record ctor measured

`006AA180` (38 B) is the module-record constructor the registration
sweep calls: vtable `00D7C860` (RTTI `01D2FAF0`, `[0] = 00861EC6`)
at `[rcx]`, `+0x10 = edx`, `+0x24 = r8d`, `+8`/`+0x18`/`+0x20`/
`+0x28` zeroed, returns `rcx`.
Interior anchor `006AA18A` (the vtable store).

## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)

- **Input - SERVICE (1 edge).** DirectInputKeyboard_PollState (`007A1640`) reaches bodies filed to Input: InputDevice_FinalizeButtonTransitions (`007A15A0`) - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (7 edges).** `005AD8F0`, `005B0BB0`, `005CD0A0`, `006372B0` are called by bodies filed to Presentation: `005C5C80`, `005FD2A0`; `00637A70`, `00639C80`, `0063C1A0` reach bodies filed to Presentation: `00639A60` - shared machinery across the layer boundary, no shared ownership.
