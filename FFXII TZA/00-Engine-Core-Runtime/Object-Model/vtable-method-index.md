---
system: Vtable method index — address → owning class → slot, for 4,275 methods
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: cross-category — Phyre, SQEX audio, PPFX, Bullet, game classes
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 1 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708, on SNAPSHOT-IDENTITY - replaced rather than re-targeted because that basis is FALSE for this document, which cites a record that changed
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
ee_index_only:
  - "Appendix — the 4,275 unambiguously-owned vtable methods"
last_reviewed: 2026-09-02
audit:
  passes: 6
  last_pass: 2026-09-02
  last_pass_state: four-attacks-survived-discharged-GN158
---

# Vtable method index

**The category README calls this "the highest-leverage task in the whole database".** It was recovered
on 2026-09-02 and its open question, **B-3**, then sat at *RECOVERED — NOT YET APPLIED*. This document
applies it: **4,275 function addresses, each tied to exactly one C++ class and vtable slot.**

## 1. What the player sees

Nothing directly — this is the map, not the territory. But it is the difference between *"some
function did something"* and *"the mesh instance's draw path did it"*.

FFXII TZA is roughly 34,000 functions, the overwhelming majority of them anonymous. **Every question
about why the game behaves as it does eventually becomes "what is this code part of?"** — why a
character renders wrong, why audio drops on a zone change, why a physics probe misses. An address with
a class name attached can be reasoned about; an address without one can only be stared at.

**4,275 of those functions now say which engine object they belong to.**

## 2. Native mechanism

MSVC emits, for every polymorphic class, a **Complete Object Locator** immediately *before* the vtable
— at `vtable[-1]`. The COL points to a `TypeDescriptor` carrying the mangled class name, and it
carries a **self-reference (`pSelf`)** that validates the whole structure: a candidate is a real COL
only if that field points back at the COL itself.

```
[ COL* ] [ slot 0 ] [ slot 1 ] [ slot 2 ] ...
   |                    ^
   |                    +--- the vtable proper; each slot a function pointer
   +--> COL { signature, offset, cdOffset, pTypeDescriptor, pClassDescriptor, pSelf }
                                       |
                                       +--> ".?AVPMeshInstance@PRendering@Phyre@@"
```

Walking every COL in `.rdata`, validating by `pSelf`, and reading the vtable that follows yields
**2,286 vtables across 2,248 classes, holding 6,886 distinct method addresses**.

The recovery, the demangling, and the two independent implementations that agree on those counts are
documented in
[`rtti-vtable-object-model.md`](rtti-vtable-object-model.md).

## 3. Key addresses

This document *is* the address table — see the appendix. The recovery constants themselves:

| | |
|---|---|
| COL location | `vtable[-1]` |
| COL validation | `pSelf` self-reference |
| type name form | `.?AV<name>@<ns>@@` (classes), `.?AU...` (structs) |
| vtables recovered | **2,286** |
| classes | **2,248** |
| distinct method addresses | **6,886** |
| **unambiguously owned (this index)** | **4,275** |
| folded, ownership not recoverable | **2,611** |

## 4. Data structures and formulas

### The split that decides what can be listed

A function reachable from **more than one class's** vtable cannot be assigned an owner, because
`/OPT:ICF` folds identical bodies across unrelated types. The two populations are cleanly different
in size, which is what confirms the reading:

| | count | median body | still `FUN_*` |
|---|---:|---:|---:|
| **exactly one class** — listed here | **4,275** | **92 B** | 98.6 % |
| **folded across classes** — excluded | **2,611** | **36 B** | 91.6 % |

**A 92-byte body doing real work in one vtable is a method. A 36-byte body appearing in hundreds of
unrelated vtables is a shared stub.** The extremes make it plain:

```
0016D680          4 B   in 1,349 classes
005C5230          3 B   in 1,302 classes
0016D6A0          3 B   in 1,291 classes   <- _guard_check_icall, a `ret` placeholder
00660570          4 B   in 1,187 classes
0062F080         27 B   in 1,186 classes
```

**4,265 of the 4,275 sit at exactly one slot; 10 occupy two slots of the same class** — multiple
inheritance, where a class has more than one vtable.

### Composition

| namespace | methods | | namespace | methods |
|---|---:|---|---|---:|
| `Phyre` | **3,067** | | `CharacterRenderObject` | 30 |
| `SQEX` | **353** | | `GameApplication` | 18 |
| `PPFX` | **240** | | `btBoxShape` | 14 |
| `std` | 47 | | `btCompoundShape` | 11 |
| `PrimitiveRendererD3D11` | 39 | | `btHashedOverlappingPairCache` | 11 |
| `btDiscreteDynamicsWorld` | 31 | | 164 further namespaces | 384 |

**Middleware dominates**, which is the expected shape and matches what the object-model document
already established: **FFXII's own gameplay code is procedural, not object-oriented**, so the classes
recoverable this way are overwhelmingly Phyre's, Square Enix's audio driver's, Yebis/PPFX's and
Bullet's — not the battle system's.

## 5. Call chain

Not applicable — this is an index, not a mechanism. Each listed address's call behaviour belongs to
its own subsystem's document.

## 6. Modding notes

- **A vtable slot is a stable patch point** in a way an address is not: slot *n* of a class survives
  a rebuild that moves every function. Anything hooking Phyre behaviour should key on
  `(class, slot)` from this index rather than on a raw address.
- **Do not hook a folded address.** The 2,611 excluded here are shared by up to 1,349 classes; a
  detour on one hits every class that folded onto it. That is the single most likely way to break
  something unrelated, and it is exactly why they are excluded rather than guessed at.
- **XIIOnline:** this index makes Phyre call graphs readable, which is its whole value here. It does
  not expose gameplay state — see the composition table for why.

## 7. What is not known

- [x] **The 2,611 folded addresses' owners.** Recoverable in principle only by distinguishing which
      class *originally* defined each folded body, which the binary does not record. **BA-1.**
      *(OUT OF EVIDENCE BOUNDARY for the true owner of the 2,179 FOLDED addresses, 2026-09-28, applied by FABLE
      (Claude Opus 5.5) on SWE2-AUDIT-SEM's bounded non-author signature of OPUS's package.
      [Record](../../_index/candidates/ba1-oeb-applied/README.md).)*
      - Per-function provenance survives only in the unshipped `FF12X64.pdb`.
      - The other classes are answered: INHERITANCE 320, ONE-TEMPLATE-FAMILY 73, STUB 39.
      - The 5 + 15 address-layout leans are leads, not answers.
      - Closed for the gate, unanswered in fact.
- [x] What each listed method *does*. This index gives identity — class and slot — not behaviour.
      **Nothing here has had its body read.** **BA-2.**
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 00-Engine-Core-Runtime/Object-Model/vtable-method-index.md. See the register row.*
- [x] Whether the 10 two-slot methods are all multiple inheritance, or whether some are a recovery
      artifact. **BA-3.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BA-3): neither — all ten are two virtual
      slots of the same single vtable holding one folded body.* The ten, from `rtti/methods.tsv`, restricted to methods
      owned by one class:

      | method | class | slots |
      |---|---|---|
      | `0016D6B0` | `eastl::allocator` | 1, 2 |
      | `0063B9E0` | `Phyre::PClassDataMemberArrayFixedSize` | 6, 7 |
      | `0063BB00` | `Phyre::PClassLayoutInterface` | 4, 5 |
      | `006A3B40` | `btBoxShape` | 18, 24 |
      | `00833B30` | `btConvexHullShape` | 20, 21 |
      | `00836A20` | `btTriangleIndexVertexArray` | 2, 3 |
      | `0084A320` | `btDbvtBroadphase` | 8, 9 |
      | `00855500`, `00857930`, `008581A0` | `btDiscreteDynamicsWorld` | 28/30, 24/25, 29/31 |

      **Every one of these eight classes has exactly one vtable** (`rtti/classes.tsv`, `vtables` = 1). `rtti/vtables.tsv`
      shows both slots of each pair in that one table, for example `01CCF5E0` slots 28 and 30 both `00855500`. That rules out
      multiple inheritance, which would put the two slots in different vtables. It is not a recovery artifact either,
      because the table really stores the address twice. **It is `/OPT:ICF` inside one class:** two distinct virtual
      methods compiled to identical bytes, the shape of const/non-const overload pairs (not verified by name). The
      sentence *"multiple inheritance, where a class has more than one vtable"* above is corrected by this.

## 8. Evidence

**Tier 1 — structural, and verified by two independent implementations.** `vtable_map.py` (address-
keyed) and `rtti_recover.py` (type-keyed) were written separately and, after the defects recorded in
[`rtti-vtable-object-model.md`](rtti-vtable-object-model.md) sections 13–14 were fixed, **agree on
every headline count**: 2,248 classes, 2,286 vtables, and method tables differing by 1 row out of
25,798, that row understood.

**The ownership test is exact, not heuristic.** An address is listed only if the set of classes whose
vtables contain it has size 1. No adjacency, no inheritance-by-caller, no naming-similarity — all
banned by [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) — is used anywhere
in the derivation.

**The 2,611/4,275 split was measured, not assumed.** The challenge recorded against B-3 predicted
"2,612 addresses folded across unrelated classes, median body 36 B". Re-measured independently here:
**2,611 folded, median 36 B**. The one-row difference is not chased; the two measurements are of the
same thing and the agreement is the point.

**Base rate, stated.** 98.6 % of the listed methods are still named `FUN_*`. That is not a finding —
the `Phyre` namespace is 95.4 % `FUN_*` and the binary 84.2 %, and this set is 72 % Phyre. **The
evidence is the COL/`pSelf` structure, not the naming rate.**

**What this does not claim.** That these are all the methods (only the polymorphic classes appear),
that a class named here is *used* at runtime, or that a slot number means the same thing across
classes. Each is a separate question and none is assumed.

### Cross-check against everything the database already named

Of the 4,275 listed addresses, **20 were already cited somewhere in the database**, and exactly **two
collide with a stated name**. Both turn out to be complementary rather than contradictory, which is
the useful result: **this index contradicts no existing identification.**

| address | already in the database as | this index adds | reading |
|---|---|---|---|
| `007A1CD0` | `SteamController_PollState` (GFZ-named) | `PFramework::PInputDevicePadSteamController` **slot 5** | **Both true.** Phyre's Steam pad device class is what drives Steam controller polling — the two facts join into one. |
| `00686280` | listed under `lua_pcall` in the third-party inventory | `PScripting::PClassCallableMethodScript::PCallerScript` **slot 2** | **Not a name collision.** That table says "`lua_pcall` **call sites**" and marks the row *not read*; the matched token is the **callee's** name, not this address's. |

**A caution carried forward on the second row.** Checking it directly, **0 of this function's 59
direct calls reach any Lua-tagged function**, so the "call site" claim it was listed under remains
unverified — as its own `not read` marker already said. **This index names the class; it does not
rescue the call-site claim**, and nothing here should be read as confirming it.

## 9. Related

- [`rtti-vtable-object-model.md`](rtti-vtable-object-model.md) — the recovery itself, the two tools'
  reconciliation, and the five pipeline defects found while proving it.
- [`../../22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`](../../22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md)
  — 747 further functions named the complementary way, by the strings they emit rather than the
  vtables they sit in.
- [`../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
  — the runtime class descriptors, a separate metadata system from the compiler's RTTI.

## Appendix — the 4,275 unambiguously-owned vtable methods

Address, owning class, and vtable slot. Every entry here appears in **exactly one**
class, so the ownership is unambiguous; the 2,611 folded addresses are deliberately
**not** listed (section 7). A `/` in the slot column means the method occupies two
slots of the same class — multiple inheritance, 10 cases.

Grouped by owning namespace for readability; within a group, address order.

### Phyre — 3067 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `00185800` | `PCameraPerspective` | 0 | `00655A10` | `PPostProcessing::PCelShading` | 1 |
| `00185850` | `PCameraProjection` | 0 | `00655AC0` | `PPostProcessing::PDeferredLighting` | 1 |
| `00189C20` | `PCameraPerspective` | 1 | `00655B80` | `PPostProcessing::PDepthOfField` | 1 |
| `0018D100` | `PRendering::PMaterialSelectorBase` | 1 | `00655C10` | `PPostProcessing::PFXAA` | 1 |
| `0018D130` | `PRendering::PMaterialSelectorMaterialSet` | 1 | `00655CA0` | `PPostProcessing::PGlow` | 1 |
| `001EF4B0` | `PCameraOrthographic` | 0 | `00655D30` | `PPostProcessing::PMotionBlur` | 1 |
| `001F0A00` | `PCameraOrthographic` | 1 | `00655E30` | `PPostProcessing::PScreenSpaceReflection` | 1 |
| `00444F4C` | `PLOD::PUtilityLOD` | 3 | `006571A0` | `PPostProcessing::PScreenSpaceReflection` | 5 |
| `005847E0` | `PClassDescriptorForType<class Phyre::PSerialization::PBinary::PClusterHeaderBase>` | 7 | `006571E0` | `PPostProcessing::PAtmospherics` | 2 |
| `00584870` | `PClassDescriptorAbstract<class Phyre::PSerialization::PBinary::PClusterHeaderBase>` | 7 | `00657250` | `PPostProcessing::PCelShading` | 2 |
| `005848D0` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PClusterHeaderBase>` | 10 | `006572C0` | `PPostProcessing::PDeferredLighting` | 2 |
| `00584910` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PClusterHeaderBase>` | 3 | `00657330` | `PPostProcessing::PDepthOfField` | 2 |
| `00584950` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PClusterHeaderBase>` | 7 | `00657430` | `PPostProcessing::PFXAA` | 2 |
| `00584A40` | `PClassDescriptorForType<class Phyre::PSerialization::PBinary::PClusterHeaderD3D11>` | 7 | `006574A0` | `PPostProcessing::PGlow` | 2 |
| `00584AD0` | `PClassDescriptorAbstract<class Phyre::PSerialization::PBinary::PClusterHeaderD3D11>` | 7 | `00657510` | `PPostProcessing::PMaterialPostEffect` | 2 |
| `00584B30` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PClusterHeaderD3D11>` | 10 | `00657570` | `PPostProcessing::PMotionBlur` | 2 |
| `00584B70` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PClusterHeaderD3D11>` | 3 | `00657610` | `PPostProcessing::PScreenSpaceReflection` | 2 |
| `00584BC0` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PClusterHeaderD3D11>` | 7 | `00657690` | `PPostProcessing::PDeferredLighting` | 3 |
| `00584CB0` | `PClassDescriptorForType<class Phyre::PSerialization::PBinary::PClusterHeader>` | 7 | `006576D0` | `PPostProcessing::PDepthOfField` | 3 |
| `00584D50` | `PClassDescriptorAbstract<class Phyre::PSerialization::PBinary::PClusterHeader>` | 7 | `00657710` | `PPostProcessing::PFXAA` | 3 |
| `00584DB0` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PClusterHeader>` | 10 | `006577B0` | `PPostProcessing::PGlow` | 3 |
| `00584E10` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PClusterHeader>` | 3 | `006577F0` | `PPostProcessing::PMotionBlur` | 3 |
| `00584E60` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PClusterHeader>` | 7 | `00657830` | `PPostProcessing::PScreenSpaceReflection` | 3 |
| `00584F50` | `PClassDescriptorForType<class Phyre::PSerialization::PBinary::PInternal::PInstanceListHeader>` | 7 | `0065B270` | `PPostProcessing::PAtmospherics` | 6 |
| `00584FE0` | `PClassDescriptorAbstract<class Phyre::PSerialization::PBinary::PInternal::PInstanceListHeader>` | 7 | `0065B340` | `PPostProcessing::PCelShading` | 6 |
| `00585040` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PInternal::PInstanceListHeader>` | 10 | `0065B400` | `PPostProcessing::PDeferredLighting` | 6 |
| `00585060` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PInternal::PInstanceListHeader>` | 3 | `0065B4C0` | `PPostProcessing::PDepthOfField` | 6 |
| `00585090` | `PClassDescriptorConcrete<class Phyre::PSerialization::PBinary::PInternal::PInstanceListHeader>` | 7 | `0065B590` | `PPostProcessing::PFXAA` | 6 |
| `00598180` | `PClassLayoutInterface` | 0 | `0065B650` | `PPostProcessing::PGlow` | 6 |
| `005981B0` | `PSerialization::PBinary::PInternal::PFindNestedClassVisitor` | 0 | `0065B750` | `PPostProcessing::PMaterialPostEffect` | 6 |
| `00598210` | `PSerialization::PStream` | 0 | `0065B820` | `PPostProcessing::PMotionBlur` | 6 |
| `00598280` | `PSerialization::PStreamReaderFile` | 0 | `0065B920` | `PPostProcessing::PScreenSpaceReflection` | 6 |
| `005982F0` | `PSerialization::PStreamWriterFile` | 0 | `0065D700` | `PPostProcessing::PUtilityPostProcessing` | 2 |
| `0059D4B0` | `PSerialization::PStreamReaderFile` | 5 | `0065E3A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPostProcessing::PPostEffectManager,class Phyre::PBase * __ptr64,unsigned int>` | 2 |
| `0059D550` | `PSerialization::PUtilitySerialization` | 1 | `0065E430` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPostProcessing::PPostEffectManager,class Phyre::PClassDescriptor const * __ptr64,unsigned int>` | 2 |
| `0059ED70` | `PSerialization::PStreamReaderFile` | 3 | `0065E4B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPostProcessing::PPostEffectManager,class Phyre::PTypedObject,unsigned int>` | 2 |
| `0059EE10` | `PSerialization::PStreamWriterFile` | 3 | `0065E6D0` | `PClassDescriptorForType<class Phyre::PGeometry::PDynamicDataBlock>` | 7 |
| `0059F490` | `PSerialization::PStreamWriterFile` | 5 | `0065E760` | `PClassDescriptorAbstract<class Phyre::PGeometry::PDynamicDataBlock>` | 7 |
| `0059FDA0` | `PSerialization::PStreamReaderFile` | 6 | `0065E7E0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDynamicDataBlock>` | 3 |
| `0059FE20` | `PSerialization::PUtilitySerialization` | 2 | `0065E810` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDynamicDataBlock>` | 7 |
| `005A0120` | `PSerialization::PBinary::PInternal::PFindNestedClassVisitor` | 1 | `0065E940` | `PClassDescriptorForType<class Phyre::PGeometry::PMeshSegmentBase>` | 7 |
| `005A04E0` | `PClassDescriptorForType<class Phyre::PTimer>` | 7 | `0065E9D0` | `PClassDescriptorAbstract<class Phyre::PGeometry::PMeshSegmentBase>` | 7 |
| `005A0540` | `PClassDescriptorWrapper<class Phyre::PTimer>` | 7 | `0065EA30` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMeshSegmentBase>` | 10 |
| `005A05A0` | `PCaller` | 0 | `0065EA70` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMeshSegmentBase>` | 3 |
| `005A0AF0` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<double>` | 1 | `0065EAA0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMeshSegmentBase>` | 7 |
| `005A0B30` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<double>` | 4 | `0065EB90` | `PClassDescriptorForType<class Phyre::PGeometry::PIndexDataBlockBase>` | 7 |
| `005A0B60` | `PClassDescriptorWrapper<class Phyre::PTimer>` | 3 | `0065EC20` | `PClassDescriptorAbstract<class Phyre::PGeometry::PIndexDataBlockBase>` | 7 |
| `005A0BD0` | `PClassDescriptorWrapper<class Phyre::PTimer>` | 4 | `0065EC80` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlockBase>` | 10 |
| `005A0C50` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<double>` | 2 | `0065ECA0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlockBase>` | 3 |
| `005A0D20` | `PScene::PUtilityScene` | 1 | `0065ED10` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlockBase>` | 7 |
| `005A0D30` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSpuTargetBlenderController>` | 3 | `0065EE00` | `PClassDescriptorForType<class Phyre::PGeometry::PMesh>` | 7 |
| `005A0D60` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationChannelTarget>` | 7 | `0065EE90` | `PClassDescriptorAbstract<class Phyre::PGeometry::PMesh>` | 7 |
| `005A0DD0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSpuTargetBlenderController>` | 7 | `0065EEF0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMesh>` | 10 |
| `005A0F00` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationChannelTarget>` | 7 | `0065EF40` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMesh>` | 3 |
| `005A0F60` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannelTarget>` | 10 | `0065EF70` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMesh>` | 7 |
| `005A0FB0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannelTarget>` | 3 | `0065F110` | `PClassDescriptorForType<class Phyre::PGeometry::PMeshSegmentD3D11>` | 7 |
| `005A1020` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationController>` | 7 | `0065F170` | `PClassDescriptorForType<class Phyre::PGeometry::PIndexDataBlockBufferD3D11>` | 7 |
| `005A1090` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannelTarget>` | 7 | `0065F220` | `PClassDescriptorAbstract<class Phyre::PGeometry::PMeshSegmentD3D11>` | 7 |
| `005A11D0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationController>` | 7 | `0065F280` | `PClassDescriptorAbstract<class Phyre::PGeometry::PIndexDataBlockBufferD3D11>` | 7 |
| `005A1230` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationController>` | 10 | `0065F310` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMeshSegmentD3D11>` | 10 |
| `005A1260` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationController>` | 3 | `0065F340` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlockBufferD3D11>` | 10 |
| `005A12F0` | `PClassDescriptorForType<class Phyre::PAnimation::PBlendableAnimationSource>` | 7 | `0065F390` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMeshSegmentD3D11>` | 3 |
| `005A1380` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationController>` | 7 | `0065F3E0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlockBufferD3D11>` | 3 |
| `005A1440` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationTargetBlenderController>` | 7 | `0065F480` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMeshSegmentD3D11>` | 7 |
| `005A14B0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PBlendableAnimationSource>` | 7 | `0065F4E0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlockBufferD3D11>` | 7 |
| `005A1510` | `PClassDescriptorConcrete<class Phyre::PAnimation::PBlendableAnimationSource>` | 10 | `0065F540` | `PClassDescriptorForType<class Phyre::PGeometry::PDataBlockBufferD3D11>` | 7 |
| `005A15A0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PBlendableAnimationSource>` | 3 | `0065F610` | `PClassDescriptorAbstract<class Phyre::PGeometry::PDataBlockBufferD3D11>` | 7 |
| `005A16E0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PBlendableAnimationSource>` | 7 | `0065F690` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlockBufferD3D11>` | 10 |
| `005A1740` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationTargetBlenderController>` | 7 | `0065F700` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlockBufferD3D11>` | 3 |
| `005A17D0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationTargetBlenderController>` | 10 | `0065F760` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlockBufferD3D11>` | 7 |
| `005A1820` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationTargetBlenderController>` | 3 | `0065F7C0` | `PClassDescriptorForType<class Phyre::PGeometry::PVertexStream>` | 7 |
| `005A1870` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationClip>` | 7 | `0065F900` | `PClassDescriptorAbstract<class Phyre::PGeometry::PVertexStream>` | 7 |
| `005A1970` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationTargetBlenderController>` | 7 | `0065F960` | `PClassDescriptorConcrete<class Phyre::PGeometry::PVertexStream>` | 10 |
| `005A1A60` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad>` | 7 | `0065F980` | `PClassDescriptorForType<class Phyre::PGeometry::PMeshSegment>` | 7 |
| `005A1AD0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationClip>` | 7 | `0065F9E0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PVertexStream>` | 3 |
| `005A1B30` | `PClassDescriptorForType<class Phyre::PAnimation::PTimeController>` | 7 | `0065FA40` | `PClassDescriptorConcrete<class Phyre::PGeometry::PVertexStream>` | 7 |
| `005A1BA0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationClip>` | 10 | `0065FAC0` | `PClassDescriptorAbstract<class Phyre::PGeometry::PMeshSegment>` | 7 |
| `005A1BF0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationClip>` | 3 | `0065FB20` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMeshSegment>` | 10 |
| `005A1CD0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad>` | 7 | `0065FB70` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMeshSegment>` | 3 |
| `005A1D70` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationClip>` | 7 | `0065FBC0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMeshSegment>` | 7 |
| `005A1DD0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad>` | 3 | `0065FDC0` | `PClassDescriptorForType<class Phyre::PGeometry::PDynamicMesh>` | 7 |
| `005A1E10` | `PClassDescriptorAbstract<class Phyre::PAnimation::PTimeController>` | 7 | `0065FE20` | `PClassDescriptorForType<class Phyre::PGeometry::PIndexDataBlockD3D11>` | 7 |
| `005A1E70` | `PClassDescriptorConcrete<class Phyre::PAnimation::PTimeController>` | 10 | `0065FE80` | `PClassDescriptorAbstract<class Phyre::PGeometry::PDynamicMesh>` | 12 |
| `005A1E90` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationChannelBase>` | 7 | `0065FEA0` | `PClassDescriptorAbstract<class Phyre::PGeometry::PDynamicMesh>` | 4 |
| `005A1EF0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PTimeController>` | 3 | `0065FF00` | `PClassDescriptorAbstract<class Phyre::PGeometry::PDynamicMesh>` | 7 |
| `005A1F10` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad>` | 7 | `0065FF60` | `PClassDescriptorAbstract<class Phyre::PGeometry::PIndexDataBlockD3D11>` | 7 |
| `005A1F80` | `PClassDescriptorConcrete<class Phyre::PAnimation::PTimeController>` | 7 | `0065FFF0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlockD3D11>` | 10 |
| `005A2000` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationChannelBase>` | 7 | `00660070` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlockD3D11>` | 3 |
| `005A2060` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannelBase>` | 10 | `00660110` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlockD3D11>` | 7 |
| `005A20B0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannelBase>` | 3 | `00660190` | `PClassDescriptorForType<class Phyre::PGeometry::PDataBlockD3D11>` | 7 |
| `005A20E0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannelBase>` | 7 | `00660340` | `PClassDescriptorForType<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc>` | 7 |
| `005A21F0` | `PClassDescriptorForType<class Phyre::PAnimation::PTimeIntervalController>` | 7 | `006603B0` | `PClassDescriptorAbstract<class Phyre::PGeometry::PDataBlockD3D11>` | 7 |
| `005A2330` | `PClassDescriptorAbstract<class Phyre::PAnimation::PTimeIntervalController>` | 7 | `00660410` | `PClassDescriptorForType<class Phyre::PGeometry::PMaterialSet>` | 7 |
| `005A23E0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PTimeIntervalController>` | 10 | `00660470` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlockD3D11>` | 10 |
| `005A2430` | `PClassDescriptorConcrete<class Phyre::PAnimation::PTimeIntervalController>` | 3 | `00660510` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlockD3D11>` | 3 |
| `005A24B0` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationChannel>` | 7 | `00660580` | `PClassDescriptorAbstract<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc>` | 7 |
| `005A2520` | `PClassDescriptorConcrete<class Phyre::PAnimation::PTimeIntervalController>` | 7 | `006605E0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlockD3D11>` | 7 |
| `005A2580` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimatableComponent>` | 7 | `00660660` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc>` | 3 |
| `005A2640` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationChannel>` | 7 | `00660680` | `PClassDescriptorAbstract<class Phyre::PGeometry::PMaterialSet>` | 7 |
| `005A26F0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannel>` | 10 | `006606E0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc>` | 7 |
| `005A2770` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannel>` | 3 | `00660740` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMaterialSet>` | 3 |
| `005A2830` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimatableComponent>` | 7 | `00660770` | `PClassDescriptorConcrete<class Phyre::PGeometry::PMaterialSet>` | 7 |
| `005A28B0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimatableComponent>` | 10 | `006608A0` | `PClassDescriptorForType<class Phyre::PGeometry::PDataBlockBase>` | 7 |
| `005A2920` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimatableComponent>` | 3 | `00660960` | `PClassDescriptorAbstract<class Phyre::PGeometry::PDataBlockBase>` | 7 |
| `005A2950` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannel>` | 7 | `00660A20` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlockBase>` | 10 |
| `005A29B0` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationSlotFilter>` | 7 | `00660A40` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlockBase>` | 3 |
| `005A2A20` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationDataSourceListEntry>` | 7 | `00660A70` | `PClassDescriptorForType<class Phyre::PGeometry::PSkeletonJointBounds>` | 7 |
| `005A2A80` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimatableComponent>` | 7 | `00660AD0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlockBase>` | 7 |
| `005A2BE0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationSlotFilter>` | 7 | `00660C10` | `PClassDescriptorForType<class Phyre::PGeometry::PIndexDataBlock>` | 7 |
| `005A2C40` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSlotFilter>` | 10 | `00660C70` | `PClassDescriptorAbstract<class Phyre::PGeometry::PSkeletonJointBounds>` | 7 |
| `005A2C70` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationDataSourceListEntry>` | 7 | `00660D10` | `PClassDescriptorConcrete<class Phyre::PGeometry::PSkeletonJointBounds>` | 10 |
| `005A2CD0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSlotFilter>` | 3 | `00660D60` | `PClassDescriptorConcrete<class Phyre::PGeometry::PSkeletonJointBounds>` | 3 |
| `005A2D00` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationDataSourceListEntry>` | 10 | `00660E10` | `PClassDescriptorConcrete<class Phyre::PGeometry::PSkeletonJointBounds>` | 7 |
| `005A2D80` | `PClassDescriptorForType<class Phyre::PAnimation::PTimeScaleOffsetController>` | 7 | `00660E90` | `PClassDescriptorAbstract<class Phyre::PGeometry::PIndexDataBlock>` | 7 |
| `005A2DE0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationDataSourceListEntry>` | 3 | `00660EF0` | `PClassDescriptorForType<class Phyre::PGeometry::PShape>` | 7 |
| `005A2EC0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSlotFilter>` | 7 | `00660F80` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlock>` | 10 |
| `005A2F60` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationDataSourceListEntry>` | 7 | `00661020` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlock>` | 3 |
| `005A2FE0` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationConstantChannel>` | 7 | `006610B0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PIndexDataBlock>` | 7 |
| `005A3050` | `PClassDescriptorAbstract<class Phyre::PAnimation::PTimeScaleOffsetController>` | 7 | `00661110` | `PClassDescriptorForType<class Phyre::PGeometry::PDataBlock>` | 7 |
| `005A30B0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PTimeScaleOffsetController>` | 10 | `00661190` | `PClassDescriptorAbstract<class Phyre::PGeometry::PShape>` | 7 |
| `005A30E0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PTimeScaleOffsetController>` | 3 | `006611F0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PShape>` | 10 |
| `005A3140` | `PClassDescriptorConcrete<class Phyre::PAnimation::PTimeScaleOffsetController>` | 7 | `00661220` | `PClassDescriptorConcrete<class Phyre::PGeometry::PShape>` | 3 |
| `005A31A0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationConstantChannel>` | 7 | `00661270` | `PClassDescriptorConcrete<class Phyre::PGeometry::PShape>` | 7 |
| `005A3200` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationConstantChannel>` | 10 | `006612D0` | `PClassDescriptorAbstract<class Phyre::PGeometry::PDataBlock>` | 7 |
| `005A3260` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationConstantChannel>` | 3 | `00661330` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlock>` | 10 |
| `005A3300` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationConstantChannel>` | 7 | `006613B0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlock>` | 3 |
| `005A33A0` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationNetworkInstanceTarget>` | 7 | `00661460` | `PClassDescriptorConcrete<class Phyre::PGeometry::PDataBlock>` | 7 |
| `005A34F0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationNetworkInstanceTarget>` | 7 | `00661500` | `PClassDescriptorForType<class Phyre::PGeometry::PSkinBoneRemap>` | 7 |
| `005A3550` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationNetworkInstanceTarget>` | 10 | `00661590` | `PClassDescriptorAbstract<class Phyre::PGeometry::PSkinBoneRemap>` | 7 |
| `005A3570` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationSet>` | 7 | `006615F0` | `PClassDescriptorConcrete<class Phyre::PGeometry::PSkinBoneRemap>` | 3 |
| `005A35D0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationNetworkInstanceTarget>` | 3 | `00661610` | `PClassDescriptorConcrete<class Phyre::PGeometry::PSkinBoneRemap>` | 7 |
| `005A3610` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationNetworkInstanceTarget>` | 7 | `00663A10` | `PClassDataMemberArrayDynamic<class Phyre::PArray<unsigned char,4> >` | 0 |
| `005A3690` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationSet>` | 7 | `00663A70` | `PClassDataMemberArrayDynamic<class Phyre::PArray<int,4> >` | 0 |
| `005A36F0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSet>` | 10 | `00663AD0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PGeometry::PDataBlockD3D11,8> >` | 0 |
| `005A3710` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSet>` | 3 | `00663B30` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc,4> >` | 0 |
| `005A3740` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSet>` | 7 | `00663B90` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PGeometry::PMeshSegment,8> >` | 0 |
| `005A3880` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationBlenderController>` | 7 | `00663BF0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PGeometry::PSkeletonJointBounds,4> >` | 0 |
| `005A3900` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationBlenderController>` | 12 | `00663C50` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PGeometry::PSkinBoneRemap,2> >` | 0 |
| `005A3950` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationBlenderController>` | 4 | `00663CB0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PGeometry::PVertexStream,8> >` | 0 |
| `005A3970` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationSlotListIndex>` | 7 | `00663D10` | `PClassDataMemberArrayDynamic<class Phyre::PSharray<class Phyre::PRendering::PMaterial * __ptr64> >` | 0 |
| `005A3A30` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationBlenderController>` | 7 | `00663D70` | `PClassDataMemberArrayDynamic<class Phyre::PSharray<class Phyre::PGeometry::PDataBlockBufferD3D11> >` | 0 |
| `005A3B80` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationClipBinding>` | 7 | `00663DD0` | `PClassDataMemberArrayDynamic<class Phyre::PSharray<class Phyre::PGeometry::PIndexDataBlockBufferD3D11> >` | 0 |
| `005A3BF0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationSlotListIndex>` | 7 | `00663E30` | `PClassDataMemberPhyreArray<int>` | 0 |
| `005A3C50` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationEvent>` | 7 | `00663E90` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PDataBlockD3D11>` | 0 |
| `005A3CB0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSlotListIndex>` | 10 | `00663EF0` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc>` | 0 |
| `005A3CE0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSlotListIndex>` | 3 | `00663F50` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PMeshSegment>` | 0 |
| `005A3D30` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSlotListIndex>` | 7 | `00663FB0` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PSkeletonJointBounds>` | 0 |
| `005A3D90` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationClipBinding>` | 7 | `00664010` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PSkinBoneRemap>` | 0 |
| `005A3DF0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationEvent>` | 7 | `00664070` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PVertexStream>` | 0 |
| `005A3E50` | `PClassDescriptorHeader<class Phyre::PAnimation::PAnimationClipBinding>` | 11 | `006640D0` | `PClassDataMemberPhyreSharray<class Phyre::PRendering::PMaterial * __ptr64>` | 0 |
| `005A3EC0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationEvent>` | 3 | `00664130` | `PClassDataMemberPhyreSharray<class Phyre::PGeometry::PDataBlockBufferD3D11>` | 0 |
| `005A3F00` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationEvent>` | 7 | `00664190` | `PClassDataMemberPhyreSharray<class Phyre::PGeometry::PIndexDataBlockBufferD3D11>` | 0 |
| `005A4010` | `PClassDescriptorHeader<class Phyre::PAnimation::PAnimationClipBinding>` | 7 | `006641F0` | `PClassDescriptorAbstract<class Phyre::PArray<unsigned char,4> >` | 7 |
| `005A4070` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationWeightedBlenderController>` | 7 | `00664250` | `PClassDescriptorAbstract<class Phyre::PArray<int,4> >` | 7 |
| `005A4220` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationSlotArray>` | 7 | `006642B0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PGeometry::PDataBlockD3D11,8> >` | 7 |
| `005A42A0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationWeightedBlenderController>` | 7 | `00664310` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc,4> >` | 7 |
| `005A4300` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationWeightedBlenderController>` | 10 | `00664370` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PGeometry::PMeshSegment,8> >` | 7 |
| `005A4330` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingChannelMap>` | 7 | `006643D0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PGeometry::PSkeletonJointBounds,4> >` | 7 |
| `005A4390` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationWeightedBlenderController>` | 3 | `00664430` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PGeometry::PSkinBoneRemap,2> >` | 7 |
| `005A4400` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationWeightedBlenderController>` | 7 | `00664490` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PGeometry::PVertexStream,8> >` | 7 |
| `005A4480` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationSlotArray>` | 7 | `006644F0` | `PClassDescriptorAbstract<class Phyre::PSharray<class Phyre::PRendering::PMaterial * __ptr64> >` | 7 |
| `005A44F0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSlotArray>` | 3 | `00664550` | `PClassDescriptorAbstract<class Phyre::PSharray<class Phyre::PGeometry::PDataBlockBufferD3D11> >` | 7 |
| `005A4510` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingChannelMap>` | 7 | `006645B0` | `PClassDescriptorAbstract<class Phyre::PSharray<class Phyre::PGeometry::PIndexDataBlockBufferD3D11> >` | 7 |
| `005A4580` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingChannelMap>` | 3 | `00664610` | `PClassDescriptorConcrete<class Phyre::PArray<unsigned char,4> >` | 7 |
| `005A45A0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSlotArray>` | 7 | `00664670` | `PClassDescriptorConcrete<class Phyre::PArray<int,4> >` | 7 |
| `005A4670` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingChannelMap>` | 7 | `006646D0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PDataBlockD3D11,8> >` | 7 |
| `005A4710` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationDataSource>` | 7 | `00664730` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc,4> >` | 7 |
| `005A4770` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationDataSource>` | 12 | `00664790` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PMeshSegment,8> >` | 7 |
| `005A4810` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationDataSource>` | 4 | `006647F0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PSkeletonJointBounds,4> >` | 7 |
| `005A48A0` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingDataBlockCache>` | 7 | `00664850` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PSkinBoneRemap,2> >` | 7 |
| `005A4930` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationDataSource>` | 7 | `006648B0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PVertexStream,8> >` | 7 |
| `005A4B30` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationEventList>` | 7 | `00664910` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PRendering::PMaterial * __ptr64> >` | 7 |
| `005A4BE0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingDataBlockCache>` | 7 | `00664970` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PGeometry::PDataBlockBufferD3D11> >` | 7 |
| `005A4C60` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationAdditiveBlenderController>` | 7 | `006649D0` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PGeometry::PIndexDataBlockBufferD3D11> >` | 7 |
| `005A4CC0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingDataBlockCache>` | 3 | `00664A30` | `PClassDescriptorForType<class Phyre::PArray<unsigned char,4> >` | 7 |
| `005A4D20` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationChannelTimes>` | 7 | `00664A90` | `PClassDescriptorForType<class Phyre::PArray<int,4> >` | 7 |
| `005A4D90` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingDataBlockCache>` | 7 | `00664AF0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PGeometry::PDataBlockD3D11,8> >` | 7 |
| `005A4DF0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationEventList>` | 7 | `00664B50` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc,4> >` | 7 |
| `005A4E90` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationEventList>` | 3 | `00664BB0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PGeometry::PMeshSegment,8> >` | 7 |
| `005A4F00` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationAdditiveBlenderController>` | 7 | `00664C10` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PGeometry::PSkeletonJointBounds,4> >` | 7 |
| `005A4F60` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationAdditiveBlenderController>` | 10 | `00664C70` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PGeometry::PSkinBoneRemap,2> >` | 7 |
| `005A4F90` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationChannelTimes>` | 7 | `00664CD0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PGeometry::PVertexStream,8> >` | 7 |
| `005A4FF0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationEventList>` | 7 | `00664D30` | `PClassDescriptorForType<class Phyre::PSharray<class Phyre::PRendering::PMaterial * __ptr64> >` | 7 |
| `005A5050` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationAdditiveBlenderController>` | 3 | `00664D90` | `PClassDescriptorForType<class Phyre::PSharray<class Phyre::PGeometry::PDataBlockBufferD3D11> >` | 7 |
| `005A5090` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannelTimes>` | 10 | `00664DF0` | `PClassDescriptorForType<class Phyre::PSharray<class Phyre::PGeometry::PIndexDataBlockBufferD3D11> >` | 7 |
| `005A50B0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannelTimes>` | 3 | `00664E50` | `PNamedSemanticDescriptorForType<class Phyre::PGeometry::PRenderDataType>` | 7 |
| `005A50E0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationAdditiveBlenderController>` | 7 | `00664EB0` | `PGeometry::PDynamicMesh` | 0 |
| `005A5190` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationChannelTimes>` | 7 | `0066FBF0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PGeometry::PMaterialSet,unsigned int>` | 1 |
| `005A5250` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationEventController>` | 7 | `0066FC50` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGeometry::PMaterialSet,class Phyre::PRendering::PMaterial * __ptr64,unsigned int>` | 1 |
| `005A5390` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationEventController>` | 7 | `0066FD00` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PGeometry::PMaterialSet,enum Phyre::PResult,unsigned int,class Phyre::PRendering::PMaterial * __ptr64>` | 1 |
| `005A53F0` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationEventController>` | 10 | `0066FD90` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGeometry::PMesh,int,char const * __ptr64>` | 1 |
| `005A5420` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationEventController>` | 3 | `006709D0` | `PNamedSemanticDescriptorForType<class Phyre::PGeometry::PRenderDataType>` | 10 |
| `005A5460` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationNetworkInstance>` | 7 | `00670AB0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PGeometry::PMaterialSet,unsigned int>` | 4 |
| `005A5540` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationEventController>` | 7 | `00670B30` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGeometry::PMaterialSet,class Phyre::PRendering::PMaterial * __ptr64,unsigned int>` | 4 |
| `005A56B0` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationHierarchyNode>` | 7 | `00670BC0` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PGeometry::PMaterialSet,enum Phyre::PResult,unsigned int,class Phyre::PRendering::PMaterial * __ptr64>` | 4 |
| `005A5710` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationHierarchyNode>` | 12 | `00670C60` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGeometry::PMesh,int,char const * __ptr64>` | 4 |
| `005A5730` | `PClassDescriptorForType<class Phyre::PAnimation::PAnimationSpuTargetBlenderController>` | 7 | `00670CF0` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PDataBlockD3D11>` | 9 |
| `005A5790` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationNetworkInstance>` | 7 | `00670D00` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc>` | 9 |
| `005A5800` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationNetworkInstance>` | 10 | `00670D10` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PMeshSegment>` | 9 |
| `005A5850` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationNetworkInstance>` | 3 | `00670D20` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PSkeletonJointBounds>` | 9 |
| `005A5880` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationHierarchyNode>` | 4 | `00670D30` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PSkinBoneRemap>` | 9 |
| `005A5920` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationNetworkInstance>` | 7 | `00670D40` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PVertexStream>` | 9 |
| `005A59A0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationHierarchyNode>` | 7 | `00670D50` | `PClassDataMemberPhyreSharray<class Phyre::PRendering::PMaterial * __ptr64>` | 9 |
| `005A5A00` | `PInternal::PDeleteChildrenVisitor` | 1 | `00670D60` | `PClassDataMemberPhyreSharray<class Phyre::PGeometry::PDataBlockBufferD3D11>` | 9 |
| `005A5AC0` | `PClassDescriptorAbstract<class Phyre::PAnimation::PAnimationSpuTargetBlenderController>` | 7 | `00670D70` | `PClassDataMemberPhyreSharray<class Phyre::PGeometry::PIndexDataBlockBufferD3D11>` | 9 |
| `005A5B20` | `PClassDescriptorConcrete<class Phyre::PAnimation::PAnimationSpuTargetBlenderController>` | 10 | `006711E0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGeometry::PMaterialSet,class Phyre::PRendering::PMaterial * __ptr64,unsigned int>` | 3 |
| `005AABB0` | `PAnnotationWithValue<unsigned int>` | 0 | `006711F0` | `PNamedSemanticDescriptorForType<class Phyre::PGeometry::PRenderDataType>` | 9 |
| `005AABF0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<unsigned int,4> >` | 0 | `00671270` | `PClassDescriptorConcrete<class Phyre::PArray<unsigned char,4> >` | 3 |
| `005AAC50` | `PClassDataMemberArrayDynamic<class Phyre::PArray<float,4> >` | 0 | `006712E0` | `PClassDescriptorConcrete<class Phyre::PArray<int,4> >` | 3 |
| `005AACB0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PAnimation::PAnimationChannel * __ptr64,8> >` | 0 | `00671350` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PDataBlockD3D11,8> >` | 3 |
| `005AAD10` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PAnimation::PAnimationDataSource * __ptr64,8> >` | 0 | `00671380` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc,4> >` | 3 |
| `005AAD70` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PAnimation::PAnimationChannelTarget,8> >` | 0 | `006713F0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PMeshSegment,8> >` | 3 |
| `005AADD0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PAnimation::PAnimationConstantChannel,8> >` | 0 | `00671420` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PSkeletonJointBounds,4> >` | 3 |
| `005AAE30` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PAnimation::PAnimationDataSourceListEntry,8> >` | 0 | `00671490` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PSkinBoneRemap,2> >` | 3 |
| `005AAE90` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PAnimation::PAnimationEvent,4> >` | 0 | `00671500` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PGeometry::PVertexStream,8> >` | 3 |
| `005AAEF0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PAnimation::PAnimationNetworkInstanceTarget,8> >` | 0 | `00671570` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PRendering::PMaterial * __ptr64> >` | 3 |
| `005AAF50` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotArray,8> >` | 0 | `006715A0` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PGeometry::PDataBlockBufferD3D11> >` | 3 |
| `005AAFB0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad,8> >` | 0 | `006715D0` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PGeometry::PIndexDataBlockBufferD3D11> >` | 3 |
| `005AB010` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotListIndex,8> >` | 0 | `006716D0` | `PGeometry::PUtilityGeometry` | 1 |
| `005AB070` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PAnimation::PBlendableAnimationSource,8> >` | 0 | `00672D60` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PDataBlockD3D11>` | 5 |
| `005AB0D0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PQWord,16> >` | 0 | `00672DE0` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc>` | 5 |
| `005AB130` | `PClassDataMemberArrayDynamic<class Phyre::PSharray<class Phyre::PAnimation::PAnimationClip * __ptr64> >` | 0 | `00672E00` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PMeshSegment>` | 5 |
| `005AB190` | `PClassDataMemberPhyreArray<unsigned int>` | 0 | `00672E20` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PSkeletonJointBounds>` | 5 |
| `005AB1F0` | `PClassDataMemberPhyreArray<float>` | 0 | `00672E40` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PSkinBoneRemap>` | 5 |
| `005AB250` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationChannel * __ptr64>` | 0 | `00672E60` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PVertexStream>` | 5 |
| `005AB2B0` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationDataSource * __ptr64>` | 0 | `00672E80` | `PClassDataMemberPhyreSharray<class Phyre::PGeometry::PDataBlockBufferD3D11>` | 5 |
| `005AB310` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationChannelTarget>` | 0 | `00672EA0` | `PClassDataMemberPhyreSharray<class Phyre::PGeometry::PIndexDataBlockBufferD3D11>` | 5 |
| `005AB370` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationConstantChannel>` | 0 | `00673340` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PDataBlockD3D11>` | 8 |
| `005AB3D0` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationDataSourceListEntry>` | 0 | `00673380` | `PClassDataMemberPhyreArray<class Phyre::PGeometry::PMeshSegment>` | 8 |
| `005AB430` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationEvent>` | 0 | `006733B0` | `PClassDataMemberPhyreSharray<class Phyre::PGeometry::PDataBlockBufferD3D11>` | 8 |
| `005AB490` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationNetworkInstanceTarget>` | 0 | `006733E0` | `PClassDataMemberPhyreSharray<class Phyre::PGeometry::PIndexDataBlockBufferD3D11>` | 8 |
| `005AB4F0` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationSlotArray>` | 0 | `006739A0` | `PGeometry::PUtilityGeometry` | 2 |
| `005AB550` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad>` | 0 | `00674860` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGeometry::PMaterialSet,class Phyre::PRendering::PMaterial * __ptr64,unsigned int>` | 2 |
| `005AB5B0` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationSlotListIndex>` | 0 | `006748E0` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PGeometry::PMaterialSet,enum Phyre::PResult,unsigned int,class Phyre::PRendering::PMaterial * __ptr64>` | 2 |
| `005AB610` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PBlendableAnimationSource>` | 0 | `00674970` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGeometry::PMesh,int,char const * __ptr64>` | 2 |
| `005AB670` | `PClassDataMemberPhyreArray<class Phyre::PQWord>` | 0 | `00674AE0` | `PClassDescriptorForType<class Phyre::PAssetReference>` | 7 |
| `005AB6D0` | `PClassDataMemberPhyreSharray<class Phyre::PAnimation::PAnimationClip * __ptr64>` | 0 | `00674B80` | `PClassDescriptorAbstract<class Phyre::PAssetReference>` | 7 |
| `005AB730` | `PClassDescriptorAbstract<class Phyre::PArray<unsigned int,4> >` | 7 | `00674BE0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PAssetReference>` | 10 |
| `005AB790` | `PClassDescriptorAbstract<class Phyre::PArray<float,4> >` | 7 | `00674C40` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PAssetReference>` | 7 |
| `005AB7F0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PAnimation::PAnimationChannel * __ptr64,8> >` | 7 | `00674D60` | `PClassDescriptorForType<class Phyre::PAssetReferenceImport>` | 7 |
| `005AB850` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PAnimation::PAnimationDataSource * __ptr64,8> >` | 7 | `00674DF0` | `PClassDescriptorAbstract<class Phyre::PAssetReferenceImport>` | 7 |
| `005AB8B0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PAnimation::PAnimationChannelTarget,8> >` | 7 | `00674E50` | `PClassDescriptorConcrete<class Phyre::PAssetReferenceImport>` | 10 |
| `005AB910` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PAnimation::PAnimationConstantChannel,8> >` | 7 | `00674E90` | `PClassDescriptorConcrete<class Phyre::PAssetReferenceImport>` | 3 |
| `005AB970` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PAnimation::PAnimationDataSourceListEntry,8> >` | 7 | `00674F00` | `PClassDescriptorConcrete<class Phyre::PAssetReferenceImport>` | 7 |
| `005AB9D0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PAnimation::PAnimationEvent,4> >` | 7 | `00675700` | `PClassDataMemberDynamicType<class Phyre::PAssetReference>` | 0 |
| `005ABA30` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PAnimation::PAnimationNetworkInstanceTarget,8> >` | 7 | `006775A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PAssetReference * __ptr64,class Phyre::PBase const & __ptr64>` | 1 |
| `005ABA90` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotArray,8> >` | 7 | `00677610` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PAssetReference const * __ptr64,char const * __ptr64>` | 1 |
| `005ABAF0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad,8> >` | 7 | `00677680` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAssetReference,class Phyre::PClassDescriptor const & __ptr64>` | 1 |
| `005ABB50` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotListIndex,8> >` | 7 | `006776E0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAssetReference,class Phyre::PString const & __ptr64>` | 1 |
| `005ABBB0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PAnimation::PBlendableAnimationSource,8> >` | 7 | `00677740` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAssetReference,class Phyre::PTypedObject>` | 1 |
| `005ABC10` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PQWord,16> >` | 7 | `006777D0` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PAssetReference * __ptr64,class Phyre::PBase const & __ptr64>` | 4 |
| `005ABC70` | `PClassDescriptorAbstract<class Phyre::PSharray<class Phyre::PAnimation::PAnimationClip * __ptr64> >` | 7 | `00677850` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PAssetReference const * __ptr64,char const * __ptr64>` | 4 |
| `005ABCD0` | `PClassDescriptorConcrete<class Phyre::PArray<unsigned int,4> >` | 7 | `006778D0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAssetReference,class Phyre::PClassDescriptor const & __ptr64>` | 4 |
| `005ABD30` | `PClassDescriptorConcrete<class Phyre::PArray<float,4> >` | 7 | `00677950` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAssetReference,class Phyre::PString const & __ptr64>` | 4 |
| `005ABD90` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationChannel * __ptr64,8> >` | 7 | `006779D0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAssetReference,class Phyre::PTypedObject>` | 4 |
| `005ABDF0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationDataSource * __ptr64,8> >` | 7 | `00677A80` | `PClassDataMemberDynamicType<class Phyre::PAssetReference>` | 1 |
| `005ABE50` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationChannelTarget,8> >` | 7 | `00677E50` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAssetReference,class Phyre::PClassDescriptor const & __ptr64>` | 2 |
| `005ABEB0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationConstantChannel,8> >` | 7 | `00677EC0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAssetReference,class Phyre::PString const & __ptr64>` | 2 |
| `005ABF10` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationDataSourceListEntry,8> >` | 7 | `00677F30` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAssetReference,class Phyre::PTypedObject>` | 2 |
| `005ABF70` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationEvent,4> >` | 7 | `00678030` | `PClassDescriptorForType<class Phyre::PCamera>` | 7 |
| `005ABFD0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationNetworkInstanceTarget,8> >` | 7 | `006780C0` | `PClassDescriptorAbstract<class Phyre::PCamera>` | 7 |
| `005AC030` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotArray,8> >` | 7 | `00678120` | `PClassDescriptorConcrete<class Phyre::PCamera>` | 10 |
| `005AC090` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad,8> >` | 7 | `00678140` | `PClassDescriptorConcrete<class Phyre::PCamera>` | 3 |
| `005AC0F0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotListIndex,8> >` | 7 | `00678170` | `PClassDescriptorConcrete<class Phyre::PCamera>` | 7 |
| `005AC150` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PBlendableAnimationSource,8> >` | 7 | `00678280` | `PClassDescriptorForType<class Phyre::PCameraProjection>` | 7 |
| `005AC1B0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PQWord,16> >` | 7 | `006782E0` | `PClassDescriptorAbstract<class Phyre::PCameraProjection>` | 12 |
| `005AC210` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PAnimation::PAnimationClip * __ptr64> >` | 7 | `006782F0` | `PClassDescriptorAbstract<class Phyre::PCameraProjection>` | 4 |
| `005AC270` | `PClassDescriptorForType<class Phyre::PArray<unsigned int,4> >` | 7 | `00678310` | `PClassDescriptorAbstract<class Phyre::PCameraProjection>` | 7 |
| `005AC2D0` | `PClassDescriptorForType<class Phyre::PArray<float,4> >` | 7 | `00678F10` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PCamera,class Phyre::PWorldMatrix * __ptr64>` | 1 |
| `005AC330` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PAnimation::PAnimationChannel * __ptr64,8> >` | 7 | `00678F90` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCameraProjection,void,float>` | 1 |
| `005AC390` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PAnimation::PAnimationDataSource * __ptr64,8> >` | 7 | `00678FF0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PCamera,class Phyre::PWorldMatrix * __ptr64>` | 4 |
| `005AC3F0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PAnimation::PAnimationChannelTarget,8> >` | 7 | `00679070` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCameraProjection,void,float>` | 4 |
| `005AC450` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PAnimation::PAnimationConstantChannel,8> >` | 7 | `0067C600` | `PClassDescriptorAbstract<class Phyre::PText::PBitmapFontCharInfo>` | 7 |
| `005AC4B0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PAnimation::PAnimationDataSourceListEntry,8> >` | 7 | `0067C660` | `PClassDescriptorConcrete<class Phyre::PText::PBitmapFontCharInfo>` | 10 |
| `005AC510` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PAnimation::PAnimationEvent,4> >` | 7 | `0067C690` | `PClassDescriptorConcrete<class Phyre::PText::PBitmapFontCharInfo>` | 3 |
| `005AC570` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PAnimation::PAnimationNetworkInstanceTarget,8> >` | 7 | `0067C6C0` | `PClassDescriptorConcrete<class Phyre::PText::PBitmapFontCharInfo>` | 7 |
| `005AC5D0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotArray,8> >` | 7 | `0067C7D0` | `PClassDescriptorForType<class Phyre::PText::PBitmapFont>` | 7 |
| `005AC630` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad,8> >` | 7 | `0067C860` | `PClassDescriptorAbstract<class Phyre::PText::PBitmapFont>` | 7 |
| `005AC690` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotListIndex,8> >` | 7 | `0067C8C0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PText::PBitmapFont>` | 10 |
| `005AC6F0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PAnimation::PBlendableAnimationSource,8> >` | 7 | `0067C910` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PText::PBitmapFont>` | 7 |
| `005AC750` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PQWord,16> >` | 7 | `0067CA00` | `PClassDescriptorForType<class Phyre::PText::PBitmapFontCharInfo>` | 7 |
| `005AC7B0` | `PClassDescriptorForType<class Phyre::PSharray<class Phyre::PAnimation::PAnimationClip * __ptr64> >` | 7 | `0067CC90` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PText::PBitmapFontCharInfo,4> >` | 0 |
| `005AC810` | `PNamedSemanticDescriptorForType<class Phyre::PAnimation::PAnimationKeyDataType>` | 7 | `0067CCF0` | `PClassDataMemberPhyreArray<class Phyre::PText::PBitmapFontCharInfo>` | 0 |
| `005AC870` | `PTypeDefault<unsigned int>` | 7 | `0067CD50` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PText::PBitmapFontCharInfo,4> >` | 7 |
| `005AC8C0` | `PAnimation::PAnimatableComponent` | 0 | `0067CDB0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PText::PBitmapFontCharInfo,4> >` | 7 |
| `005AC950` | `PAnimation::PAnimationAdditiveBlenderController` | 0 | `0067CE10` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PText::PBitmapFontCharInfo,4> >` | 7 |
| `005AC9B0` | `PAnimation::PAnimationBlenderController` | 0 | `0067E130` | `PClassDataMemberPhyreArray<class Phyre::PText::PBitmapFontCharInfo>` | 9 |
| `005ACA40` | `PAnimation::PAnimationChannelTargetBind` | 0 | `0067E160` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PText::PBitmapFontCharInfo,4> >` | 3 |
| `005ACAD0` | `PAnimation::PAnimationChannelTargetBindShaderParameter` | 0 | `0067E2E0` | `PClassDataMemberPhyreArray<class Phyre::PText::PBitmapFontCharInfo>` | 5 |
| `005ACB00` | `PAnimation::PAnimationController` | 0 | `0067E3E0` | `PClassDescriptorForType<class Phyre::PWorldMatrix>` | 7 |
| `005ACB50` | `PAnimation::PAnimationDataSource` | 0 | `0067E470` | `PClassDescriptorAbstract<class Phyre::PWorldMatrix>` | 7 |
| `005ACBA0` | `PAnimation::PAnimationEventController` | 0 | `0067E4D0` | `PClassDescriptorConcrete<class Phyre::PWorldMatrix>` | 10 |
| `005ACBF0` | `PAnimation::PAnimationHierarchyCountNodes` | 0 | `0067E510` | `PClassDescriptorConcrete<class Phyre::PWorldMatrix>` | 3 |
| `005ACC20` | `PAnimation::PAnimationHierarchyNode` | 0 | `0067E570` | `PClassDescriptorConcrete<class Phyre::PWorldMatrix>` | 7 |
| `005ACC70` | `PAnimation::PAnimationHierarchyPopulateArrays` | 0 | `0067EF00` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PWorldMatrix,class Phyre::PMatrix4x3 & __ptr64>` | 1 |
| `005ACCA0` | `PAnimation::PAnimationHierarchyVisitContext` | 0 | `0067EF50` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PWorldMatrix,void,class Phyre::PWorldMatrix const & __ptr64>` | 1 |
| `005ACCD0` | `PAnimation::PAnimationNetworkInstance` | 0 | `0067EFA0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PWorldMatrix,void,class Phyre::PMatrix4 const & __ptr64>` | 1 |
| `005ACD30` | `PAnimation::PAnimationSlotFilter` | 0 | `0067EFF0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PWorldMatrix,void,class Phyre::PMatrix4x3 const & __ptr64>` | 1 |
| `005ACD90` | `PAnimation::PAnimationSpuTargetBlenderController` | 0 | `0067F040` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PWorldMatrix,class Phyre::PMatrix4x3 & __ptr64>` | 4 |
| `005ACDE0` | `PAnimation::PAnimationTargetBlenderController` | 0 | `0067F0C0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PWorldMatrix,void,class Phyre::PWorldMatrix const & __ptr64>` | 4 |
| `005ACE30` | `PAnimation::PAnimationWeightedBlenderController` | 0 | `0067F140` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PWorldMatrix,void,class Phyre::PMatrix4 const & __ptr64>` | 4 |
| `005ACE90` | `PAnimation::PInternal::PAvoidOutputOverwritingInput` | 1 | `0067F1D0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PWorldMatrix,void,class Phyre::PMatrix4x3 const & __ptr64>` | 4 |
| `005ACEC0` | `PAnimation::PNetworkOptimizeBufferAllocator::PBufferAcceptance` | 1 | `0067F4D0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PWorldMatrix,class Phyre::PMatrix4x3 & __ptr64>` | 2 |
| `005ACEF0` | `PAnimation::PNetworkOptimizeBufferAllocator` | 0 | `006804A0` | `PClassDescriptorForType<class Phyre::PScripting::PClassCallableMethodScript>` | 7 |
| `005ACF50` | `PAnimation::PTimeController` | 0 | `00680590` | `PClassDescriptorAbstract<class Phyre::PScripting::PClassCallableMethodScript>` | 7 |
| `005ACFA0` | `PAnimation::PTimeIntervalController` | 0 | `006805F0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PScripting::PClassCallableMethodScript>` | 7 |
| `005ACFF0` | `PAnimation::PTimeScaleOffsetController` | 0 | `006806B0` | `PClassDescriptorForType<class Phyre::PScripting::PAsyncProcessHeader>` | 7 |
| `005AD040` | `PType` | 7 | `00680790` | `PClassDescriptorAbstract<class Phyre::PScripting::PAsyncProcessHeader>` | 7 |
| `005BED30` | `PAnimation::PTimeController` | 4 | `006807F0` | `PClassDescriptorConcrete<class Phyre::PScripting::PAsyncProcessHeader>` | 10 |
| `005C0820` | `PAnimation::PAnimationChannelTargetBindDataMember` | 1 | `00680810` | `PClassDescriptorConcrete<class Phyre::PScripting::PAsyncProcessHeader>` | 3 |
| `005C0B60` | `PAnimation::PAnimationChannelTargetBindFunction` | 1 | `00680850` | `PClassDescriptorConcrete<class Phyre::PScripting::PAsyncProcessHeader>` | 7 |
| `005C0C90` | `PAnimation::PAnimationChannelTargetBindMethod` | 1 | `006809E0` | `PClassDescriptorForType<class Phyre::PScripting::PScriptCallbackHandler>` | 7 |
| `005C0E00` | `PAnimation::PAnimationChannelTargetBindScene` | 1 | `00680A50` | `PClassDescriptorForType<class Phyre::PScripting::PScheduler>` | 7 |
| `005C1000` | `PAnimation::PAnimationChannelTargetBindSceneToMeshInstance` | 1 | `00680BC0` | `PClassDescriptorAbstract<class Phyre::PScripting::PScriptCallbackHandler>` | 7 |
| `005C1160` | `PAnimation::PAnimationChannelTargetBindShaderParameter` | 1 | `00680C20` | `PClassDescriptorConcrete<class Phyre::PScripting::PScriptCallbackHandler>` | 10 |
| `005C12D0` | `PAnimation::PInternal::PAvoidOutputOverwritingInput` | 0 | `00680C60` | `PClassDescriptorAbstract<class Phyre::PScripting::PScheduler>` | 7 |
| `005C1350` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<float>` | 1 | `00680CC0` | `PClassDescriptorForType<class Phyre::PScripting::PScript>` | 7 |
| `005C1390` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,unsigned int>` | 1 | `00680D20` | `PClassDescriptorConcrete<class Phyre::PScripting::PScriptCallbackHandler>` | 3 |
| `005C13F0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,float>` | 1 | `00680D80` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PScripting::PScheduler>` | 10 |
| `005C1460` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,float,unsigned int>` | 1 | `00680DB0` | `PClassDescriptorConcrete<class Phyre::PScripting::PScriptCallbackHandler>` | 7 |
| `005C1500` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,class Phyre::PAnimation::PAnimationClip * __ptr64,unsigned int>` | 1 | `00680E80` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PScripting::PScheduler>` | 7 |
| `005C15B0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,class Phyre::PAnimation::PAnimationSet * __ptr64>` | 1 | `00680EE0` | `PClassDescriptorAbstract<class Phyre::PScripting::PScript>` | 7 |
| `005C1630` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,unsigned int>` | 1 | `00680F40` | `PClassDescriptorConcrete<class Phyre::PScripting::PScript>` | 10 |
| `005C16C0` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,unsigned int,float>` | 1 | `00680F80` | `PClassDescriptorConcrete<class Phyre::PScripting::PScript>` | 3 |
| `005C1770` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,unsigned int,class Phyre::PAnimation::PAnimationClip * __ptr64>` | 1 | `00680FB0` | `PClassDescriptorConcrete<class Phyre::PScripting::PScript>` | 7 |
| `005C1810` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,unsigned int,char const * __ptr64>` | 1 | `00681B40` | `PScripting::PAsyncProcessBatch` | 0 |
| `005C18B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,class Phyre::PAnimation::PAnimationClip * __ptr64>` | 1 | `00681BB0` | `PScripting::PAsyncProcessBuffer` | 0 |
| `005C1930` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,class Phyre::PAnimation::PAnimationSet * __ptr64>` | 1 | `00681BF0` | `PScripting::PScheduler` | 2 |
| `005C19B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,char const * __ptr64>` | 1 | `00684A80` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PScripting::PScheduler * __ptr64>` | 1 |
| `005C1A30` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,void>` | 1 | `00684AB0` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PScripting::PScript const * __ptr64>` | 1 |
| `005C1A60` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,void,float>` | 1 | `00684AE0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScripting::PAsyncProcessHeader,class Phyre::PTypedObject>` | 1 |
| `005C1AC0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,bool>` | 1 | `00684B70` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PScripting::PScheduler,enum Phyre::PResult,class Phyre::PScripting::PScript const & __ptr64,class Phyre::PBase & __ptr64,char const * __ptr64>` | 1 |
| `005C1B20` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,bool,unsigned int>` | 1 | `00684C10` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PScripting::PScheduler,enum Phyre::PResult,class Phyre::PScripting::PScript const & __ptr64,class Phyre::PTypedObject,char const * __ptr64,unsigned int>` | 1 |
| `005C1BB0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationChannelTarget,class Phyre::PClassDescriptor const & __ptr64>` | 1 | `00684D10` | `PScripting::PClassCallableMethodScript::PCallerScript` | 1 |
| `005C1C10` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationChannelTarget,unsigned int>` | 1 | `00685140` | `PScripting::PScheduler` | 0 |
| `005C1C70` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationChannelTarget,char const * __ptr64>` | 1 | `006853C0` | `PScripting::PScheduler` | 4 |
| `005C1CD0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationChannelTarget,class Phyre::PClassDescriptor const * __ptr64>` | 1 | `00685560` | `PScripting::PScheduler` | 1 |
| `005C1D50` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,class Phyre::PString const & __ptr64>` | 1 | `00685770` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PScripting::PScheduler * __ptr64>` | 4 |
| `005C1DA0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,unsigned int>` | 1 | `00685780` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PScripting::PScript const * __ptr64>` | 4 |
| `005C1E00` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,float>` | 1 | `00685790` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScripting::PAsyncProcessHeader,class Phyre::PTypedObject>` | 4 |
| `005C1E70` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,class Phyre::PAnimation::PAnimationChannel const * __ptr64,unsigned int>` | 1 | `00685810` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PScripting::PScheduler,enum Phyre::PResult,class Phyre::PScripting::PScript const & __ptr64,class Phyre::PBase & __ptr64,char const * __ptr64>` | 4 |
| `005C1F20` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,class Phyre::PAnimation::PAnimationConstantChannel const * __ptr64,unsigned int>` | 1 | `006858C0` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PScripting::PScheduler,enum Phyre::PResult,class Phyre::PScripting::PScript const & __ptr64,class Phyre::PTypedObject,char const * __ptr64,unsigned int>` | 4 |
| `005C1FD0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,enum Phyre::PResult,unsigned int>` | 1 | `006859E0` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PScripting::PScheduler * __ptr64>` | 3 |
| `005C2060` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,void,class Phyre::PCluster * __ptr64>` | 1 | `006859F0` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PScripting::PScript const * __ptr64>` | 3 |
| `005C20B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,void,char const * __ptr64>` | 1 | `00685AC0` | `PScripting::PUtilityScripting` | 1 |
| `005C2100` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationSet,class Phyre::PAnimation::PAnimationClip * __ptr64,unsigned int>` | 1 | `00685B30` | `PScripting::PAsyncProcessBuffer` | 1 |
| `005C21B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationSet,enum Phyre::PResult,class Phyre::PCluster & __ptr64>` | 1 | `00685DB0` | `PScripting::PScheduler` | 3 |
| `005C2230` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationSet,enum Phyre::PResult,class Phyre::PAnimation::PAnimationClip * __ptr64>` | 1 | `00685F60` | `PScripting::PUtilityScripting` | 2 |
| `005C38B0` | `PNamedSemanticDescriptorForType<class Phyre::PAnimation::PAnimationKeyDataType>` | 10 | `00685FB0` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PScripting::PScheduler * __ptr64>` | 2 |
| `005C3B00` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<float>` | 4 | `00686010` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PScripting::PScript const * __ptr64>` | 2 |
| `005C3B10` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,unsigned int>` | 4 | `00686070` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScripting::PAsyncProcessHeader,class Phyre::PTypedObject>` | 2 |
| `005C3B90` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,float>` | 4 | `006860E0` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PScripting::PScheduler,enum Phyre::PResult,class Phyre::PScripting::PScript const & __ptr64,class Phyre::PBase & __ptr64,char const * __ptr64>` | 2 |
| `005C3C10` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,float,unsigned int>` | 4 | `00686180` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PScripting::PScheduler,enum Phyre::PResult,class Phyre::PScripting::PScript const & __ptr64,class Phyre::PTypedObject,char const * __ptr64,unsigned int>` | 2 |
| `005C3CA0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,class Phyre::PAnimation::PAnimationClip * __ptr64,unsigned int>` | 4 | `00686280` | `PScripting::PClassCallableMethodScript::PCallerScript` | 2 |
| `005C3D30` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,class Phyre::PAnimation::PAnimationSet * __ptr64>` | 4 | `00687B70` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsMeshBase>` | 7 |
| `005C3DB0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,unsigned int>` | 4 | `00687BD0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMeshBase>` | 10 |
| `005C3E40` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,unsigned int,float>` | 4 | `00687C50` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMeshBase>` | 3 |
| `005C3EE0` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,unsigned int,class Phyre::PAnimation::PAnimationClip * __ptr64>` | 4 | `00687D00` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsShapeBase>` | 7 |
| `005C3F80` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,unsigned int,char const * __ptr64>` | 4 | `00687D60` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsTaperedCylinder>` | 7 |
| `005C4020` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,class Phyre::PAnimation::PAnimationClip * __ptr64>` | 4 | `00687DC0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsTaperedCylinder>` | 10 |
| `005C40B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,class Phyre::PAnimation::PAnimationSet * __ptr64>` | 4 | `00687E60` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsTaperedCylinder>` | 3 |
| `005C4140` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,char const * __ptr64>` | 4 | `00687FA0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMeshBase>` | 7 |
| `005C41D0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,void>` | 4 | `006880F0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsTaperedCylinder>` | 7 |
| `005C4250` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,void,float>` | 4 | `00688240` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsCharacterControllerBullet>` | 7 |
| `005C42E0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,bool>` | 4 | `006882C0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsWorld>` | 7 |
| `005C4360` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,bool,unsigned int>` | 4 | `00688330` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsRigidBodyBase>` | 7 |
| `005C43F0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationChannelTarget,class Phyre::PClassDescriptor const & __ptr64>` | 4 | `006883D0` | `PPhysics::PPhysicsTaperedCapsule` | 3 |
| `005C4470` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationChannelTarget,unsigned int>` | 4 | `00688510` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsCharacterControllerBullet>` | 7 |
| `005C44F0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationChannelTarget,char const * __ptr64>` | 4 | `00688570` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterControllerBullet>` | 10 |
| `005C4570` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationChannelTarget,class Phyre::PClassDescriptor const * __ptr64>` | 4 | `006885A0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsWorld>` | 7 |
| `005C45F0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,class Phyre::PString const & __ptr64>` | 4 | `00688600` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterControllerBullet>` | 3 |
| `005C4670` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,unsigned int>` | 4 | `006886D0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsWorld>` | 10 |
| `005C46F0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,float>` | 4 | `00688720` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsRigidBodyBase>` | 7 |
| `005C4770` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,class Phyre::PAnimation::PAnimationChannel const * __ptr64,unsigned int>` | 4 | `006887A0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsWorld>` | 3 |
| `005C4800` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,class Phyre::PAnimation::PAnimationConstantChannel const * __ptr64,unsigned int>` | 4 | `00688810` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsShapeBullet>` | 7 |
| `005C4890` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,enum Phyre::PResult,unsigned int>` | 4 | `00688870` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase>` | 10 |
| `005C4920` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,void,class Phyre::PCluster * __ptr64>` | 4 | `00688900` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase>` | 3 |
| `005C49B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,void,char const * __ptr64>` | 4 | `00688930` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterControllerBullet>` | 7 |
| `005C4A40` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationSet,class Phyre::PAnimation::PAnimationClip * __ptr64,unsigned int>` | 4 | `00688990` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsWorld>` | 7 |
| `005C4AD0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationSet,enum Phyre::PResult,class Phyre::PCluster & __ptr64>` | 4 | `006889F0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsMeshBullet>` | 7 |
| `005C4B60` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationSet,enum Phyre::PResult,class Phyre::PAnimation::PAnimationClip * __ptr64>` | 4 | `00688A70` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase>` | 7 |
| `005C4BF0` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationChannel * __ptr64>` | 9 | `00688AD0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsTaperedCapsule>` | 7 |
| `005C4C00` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationDataSource * __ptr64>` | 9 | `00688B60` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsShapeBullet>` | 7 |
| `005C4C10` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationChannelTarget>` | 9 | `00688BE0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsShapeBullet>` | 10 |
| `005C4C20` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationConstantChannel>` | 9 | `00688C80` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsShapeBullet>` | 3 |
| `005C4C30` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationDataSourceListEntry>` | 9 | `00688D20` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsMeshBullet>` | 7 |
| `005C4C40` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationEvent>` | 9 | `00688D80` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsTaperedCapsule>` | 7 |
| `005C4C50` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationNetworkInstanceTarget>` | 9 | `00688DE0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMeshBullet>` | 10 |
| `005C4C60` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationSlotArray>` | 9 | `00688E70` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsShapeBullet>` | 7 |
| `005C4C70` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad>` | 9 | `00688ED0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsTaperedCapsule>` | 10 |
| `005C4C80` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationSlotListIndex>` | 9 | `00688F70` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMeshBullet>` | 3 |
| `005C4C90` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PBlendableAnimationSource>` | 9 | `00688FA0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsTaperedCapsule>` | 3 |
| `005C4CA0` | `PClassDataMemberPhyreArray<class Phyre::PQWord>` | 9 | `00689070` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMeshBullet>` | 7 |
| `005C4CB0` | `PClassDataMemberPhyreSharray<class Phyre::PAnimation::PAnimationClip * __ptr64>` | 9 | `00689120` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsTaperedCapsule>` | 7 |
| `005C4D20` | `PAnnotationWithValue<unsigned int>` | 1 | `006892C0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsCharacterController>` | 7 |
| `005C4D30` | `PAnimation::PAnimationController` | 5 | `00689340` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsInterfaceBase>` | 7 |
| `005C4F30` | `PAnimation::PAnimationController` | 8 | `00689500` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsCharacterController>` | 7 |
| `005C5040` | `PAnimation::PAnimationController` | 6 | `006895C0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterController>` | 10 |
| `005C5120` | `PAnimation::PAnimationSlotFilter` | 6 | `00689660` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterController>` | 3 |
| `005C5140` | `PAnimation::PAnimationSpuTargetBlenderController` | 6 | `006896F0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsShape>` | 7 |
| `005C5180` | `PAnimation::PAnimationAdditiveBlenderController` | 11 | `00689750` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsInterfaceBase>` | 7 |
| `005C5190` | `PAnimation::PAnimationController` | 11 | `006897D0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsMesh>` | 7 |
| `005C51A0` | `PAnimation::PAnimationEventController` | 11 | `00689830` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsInterfaceBase>` | 10 |
| `005C51B0` | `PAnimation::PAnimationSlotFilter` | 11 | `00689850` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterController>` | 7 |
| `005C51C0` | `PAnimation::PAnimationSpuTargetBlenderController` | 11 | `006898D0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsInterfaceBase>` | 3 |
| `005C51D0` | `PAnimation::PAnimationWeightedBlenderController` | 11 | `00689900` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsPlaneBase>` | 7 |
| `005C51E0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,class Phyre::PAnimation::PAnimationSet * __ptr64>` | 3 | `006899B0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsInterfaceBase>` | 7 |
| `005C5210` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,class Phyre::PAnimation::PAnimationChannel const * __ptr64,unsigned int>` | 3 | `00689A30` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsShape>` | 7 |
| `005C5220` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,class Phyre::PAnimation::PAnimationConstantChannel const * __ptr64,unsigned int>` | 3 | `00689A90` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsMesh>` | 7 |
| `005C5250` | `PNamedSemanticDescriptorForType<class Phyre::PAnimation::PAnimationKeyDataType>` | 9 | `00689AF0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsShape>` | 10 |
| `005C52D0` | `PAnimation::PAnimationSlotFilter` | 2 | `00689B70` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMesh>` | 10 |
| `005C5330` | `PAnimation::PTimeIntervalController` | 4 | `00689C20` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsShape>` | 3 |
| `005C53C0` | `PAnimation::PTimeScaleOffsetController` | 4 | `00689CC0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMesh>` | 3 |
| `005C5550` | `PClassDescriptorConcrete<class Phyre::PArray<unsigned int,4> >` | 3 | `00689CF0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsPlaneBase>` | 7 |
| `005C55C0` | `PClassDescriptorConcrete<class Phyre::PArray<float,4> >` | 3 | `00689D50` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsPlaneBase>` | 10 |
| `005C55F0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationChannel * __ptr64,8> >` | 3 | `00689DF0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsPlaneBase>` | 3 |
| `005C5660` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationDataSource * __ptr64,8> >` | 3 | `00689EB0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsShape>` | 7 |
| `005C56D0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationChannelTarget,8> >` | 3 | `00689F10` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMesh>` | 7 |
| `005C5700` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationConstantChannel,8> >` | 3 | `0068A030` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsPlaneBase>` | 7 |
| `005C5730` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationDataSourceListEntry,8> >` | 3 | `0068A160` | `PClassDescriptorForType<class Phyre::PPhysics::PRaycastResult>` | 7 |
| `005C5760` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationEvent,4> >` | 3 | `0068A340` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsRigidBodyBullet>` | 7 |
| `005C57D0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationNetworkInstanceTarget,8> >` | 3 | `0068A400` | `PClassDescriptorAbstract<class Phyre::PPhysics::PRaycastResult>` | 7 |
| `005C5840` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotArray,8> >` | 3 | `0068A4B0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PRaycastResult>` | 10 |
| `005C58B0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad,8> >` | 3 | `0068A540` | `PClassDescriptorConcrete<class Phyre::PPhysics::PRaycastResult>` | 3 |
| `005C58E0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PAnimationSlotListIndex,8> >` | 3 | `0068A680` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsRigidBodyBullet>` | 7 |
| `005C5950` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PAnimation::PBlendableAnimationSource,8> >` | 3 | `0068A770` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBullet>` | 10 |
| `005C5980` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PQWord,16> >` | 3 | `0068A850` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBullet>` | 3 |
| `005C59F0` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PAnimation::PAnimationClip * __ptr64> >` | 3 | `0068A8E0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PRaycastResult>` | 7 |
| `005C5C80` | `PAnimation::PUtilityAnimation` | 1 | `0068A940` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsSphereBase>` | 7 |
| `005C6020` | `PAnimation::PAnimationAdditiveBlenderController` | 9 | `0068A9B0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBullet>` | 7 |
| `005C61A0` | `PAnimation::PAnimationWeightedBlenderController` | 9 | `0068AA10` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsCylinderBase>` | 7 |
| `005C6D90` | `PAnimation::PAnimationController` | 10 | `0068AA70` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsInterfaceBullet>` | 7 |
| `005C6E40` | `PAnimation::PAnimationEventController` | 10 | `0068AAD0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsPlaneBullet>` | 7 |
| `005C6ED0` | `PAnimation::PAnimationSlotFilter` | 10 | `0068AC00` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsSphereBase>` | 7 |
| `005C6F20` | `PAnimation::PAnimationSpuTargetBlenderController` | 10 | `0068AC60` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsSphereBase>` | 10 |
| `005C72A0` | `PAnimation::PAnimationTargetBlenderController` | 12 | `0068ACE0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsCylinderBase>` | 7 |
| `005C80F0` | `PTypeDefault<unsigned int>` | 4 | `0068AD40` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsSphereBase>` | 3 |
| `005C9740` | `PClassDataMemberPhyreArray<float>` | 5 | `0068ADF0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsInterfaceBullet>` | 7 |
| `005C9760` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationChannelTarget>` | 5 | `0068AE50` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsPlaneBullet>` | 7 |
| `005C9780` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationConstantChannel>` | 5 | `0068AEB0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCylinderBase>` | 10 |
| `005C97A0` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationDataSourceListEntry>` | 5 | `0068AF40` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsInterfaceBullet>` | 10 |
| `005C97C0` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationEvent>` | 5 | `0068AF90` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsPlaneBullet>` | 10 |
| `005C97E0` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationNetworkInstanceTarget>` | 5 | `0068B030` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCylinderBase>` | 3 |
| `005C9800` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationSlotArray>` | 5 | `0068B0E0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsInterfaceBullet>` | 3 |
| `005C9820` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad>` | 5 | `0068B110` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsPlaneBullet>` | 3 |
| `005C9840` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationSlotListIndex>` | 5 | `0068B140` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsSphereBase>` | 7 |
| `005C9860` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PBlendableAnimationSource>` | 5 | `0068B1A0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCylinderBase>` | 7 |
| `005C9880` | `PClassDataMemberPhyreArray<class Phyre::PQWord>` | 5 | `0068B200` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsInterfaceBullet>` | 7 |
| `005C9F30` | `PAnimation::PAnimationBlenderController` | 12 | `0068B260` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsPlaneBullet>` | 7 |
| `005CA350` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationChannelTarget>` | 8 | `0068B400` | `PPhysics::PPhysicsPlane` | 3 |
| `005CA380` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationConstantChannel>` | 8 | `0068B490` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsWorldBase>` | 7 |
| `005CA3B0` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PAnimationSlotFilterDeferredLoad>` | 8 | `0068B5F0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsRigidBody>` | 7 |
| `005CA3E0` | `PClassDataMemberPhyreArray<class Phyre::PAnimation::PBlendableAnimationSource>` | 8 | `0068B8C0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsWorldBase>` | 7 |
| `005CB140` | `PTypeDefault<unsigned int>` | 0 | `0068B920` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsSphereBullet>` | 7 |
| `005CB150` | `PAnimation::PUtilityAnimation` | 2 | `0068B980` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsInterface>` | 7 |
| `005CB620` | `PAnimation::PAnimationSlotFilter` | 3 | `0068B9E0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsWorldBase>` | 10 |
| `005CB720` | `PAnimation::PTimeController` | 3 | `0068BA60` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsInterface>` | 12 |
| `005CBCC0` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<float>` | 2 | `0068BA80` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsWorldBase>` | 3 |
| `005CBDA0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,float,unsigned int>` | 2 | `0068BB10` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsCylinderBullet>` | 7 |
| `005CBE30` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,class Phyre::PAnimation::PAnimationClip * __ptr64,unsigned int>` | 2 | `0068BB70` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsPlane>` | 7 |
| `005CBEB0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,class Phyre::PAnimation::PAnimationSet * __ptr64>` | 2 | `0068BBD0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsRigidBody>` | 7 |
| `005CBF20` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,unsigned int>` | 2 | `0068BC70` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsRigidBody>` | 10 |
| `005CBFB0` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,enum Phyre::PResult,unsigned int,float>` | 2 | `0068BCC0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsRigidBody>` | 3 |
| `005CC1F0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,bool>` | 2 | `0068BD30` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsInterface>` | 4 |
| `005CC270` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimatableComponent,bool,unsigned int>` | 2 | `0068BD50` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsWorldBase>` | 7 |
| `005CC300` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,class Phyre::PString const & __ptr64>` | 2 | `0068BDF0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsSphereBullet>` | 7 |
| `005CC3E0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,class Phyre::PAnimation::PAnimationChannel const * __ptr64,unsigned int>` | 2 | `0068BE50` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsRigidBody>` | 7 |
| `005CC460` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationClip,class Phyre::PAnimation::PAnimationConstantChannel const * __ptr64,unsigned int>` | 2 | `0068BEB0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsInterface>` | 7 |
| `005CC570` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PAnimation::PAnimationSet,class Phyre::PAnimation::PAnimationClip * __ptr64,unsigned int>` | 2 | `0068BF10` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsSphereBullet>` | 10 |
| `005CC680` | `PAnimation::PAnimationHierarchyCountNodes` | 1 | `0068BF90` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsCylinderBullet>` | 7 |
| `005CC690` | `PAnimation::PAnimationHierarchyCountNodes` | 2 | `0068BFF0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsSphereBullet>` | 3 |
| `005CC6A0` | `PAnimation::PAnimationHierarchyPopulateArrays` | 1 | `0068C0A0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsPlane>` | 7 |
| `005CD8F0` | `PTTYCallback` | 0 | `0068C100` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCylinderBullet>` | 10 |
| `005CDB90` | `PTTYCallback` | 1 | `0068C1A0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsPlane>` | 10 |
| `005CDC00` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassInfo>` | 10 | `0068C260` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCylinderBullet>` | 3 |
| `005CDC30` | `PClassDescriptorConcrete<class Phyre::PRendering::PIndirectArgsBuffer>` | 7 | `0068C320` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsPlane>` | 3 |
| `005CDC90` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassInfo>` | 3 | `0068C350` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsSphereBullet>` | 7 |
| `005CDCC0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferRWTexture2D>` | 7 | `0068C3B0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCylinderBullet>` | 7 |
| `005CDD30` | `PClassDescriptorForType<class Phyre::PRendering::PMeshInstanceAttachPoint>` | 7 | `0068C410` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsPlane>` | 7 |
| `005CDD90` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassInfo>` | 7 | `0068C6A0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsSphere>` | 7 |
| `005CDEE0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferRWTexture2D>` | 7 | `0068C720` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsCylinder>` | 7 |
| `005CE010` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWTexture2D>` | 10 | `0068C780` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsModel>` | 7 |
| `005CE030` | `PClassDescriptorAbstract<class Phyre::PRendering::PMeshInstanceAttachPoint>` | 7 | `0068C870` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsSphere>` | 7 |
| `005CE0B0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWTexture2D>` | 3 | `0068C8D0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsSphere>` | 10 |
| `005CE120` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PMeshInstanceAttachPoint>` | 10 | `0068C980` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsCylinder>` | 7 |
| `005CE1A0` | `PClassDescriptorForType<class Phyre::PRendering::PConstantBufferBase>` | 7 | `0068C9E0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsModel>` | 7 |
| `005CE240` | `PClassDescriptorForType<class Phyre::PRendering::PModifierNetworkDynamicMeshInstance>` | 7 | `0068CA40` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsSphere>` | 3 |
| `005CE2C0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWTexture2D>` | 7 | `0068CAF0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCylinder>` | 10 |
| `005CE390` | `PClassDescriptorForType<class Phyre::PRendering::PShaderPassParameterLocationTypesBase>` | 7 | `0068CBB0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsModel>` | 3 |
| `005CE420` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PMeshInstanceAttachPoint>` | 7 | `0068CBE0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCylinder>` | 3 |
| `005CE5C0` | `PClassDescriptorForType<class Phyre::PRendering::PSamplerState>` | 7 | `0068CCA0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsSphere>` | 7 |
| `005CE660` | `PClassDescriptorAbstract<class Phyre::PRendering::PConstantBufferBase>` | 7 | `0068CD00` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCylinder>` | 7 |
| `005CE6C0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderSource>` | 7 | `0068CD60` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsModel>` | 7 |
| `005CE720` | `PClassDescriptorAbstract<class Phyre::PRendering::PModifierNetworkDynamicMeshInstance>` | 7 | `0068CF20` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsBoxBase>` | 7 |
| `005CE780` | `PClassDescriptorConcrete<class Phyre::PRendering::PConstantBufferBase>` | 10 | `0068CF80` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsCapsuleBase>` | 7 |
| `005CE790` | `PClassDescriptorForType<class Phyre::PRendering::PContextVariantFoldingTable>` | 7 | `0068D0D0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsBoxBase>` | 7 |
| `005CE840` | `PClassDescriptorConcrete<class Phyre::PRendering::PConstantBufferBase>` | 3 | `0068D130` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsCapsuleBase>` | 7 |
| `005CE850` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PModifierNetworkDynamicMeshInstance>` | 10 | `0068D190` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsBoxBase>` | 10 |
| `005CE8C0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderPassParameterLocationTypesBase>` | 7 | `0068D220` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCapsuleBase>` | 10 |
| `005CE9D0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassParameterLocationTypesBase>` | 3 | `0068D2C0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsBoxBase>` | 3 |
| `005CEA10` | `PClassDescriptorConcrete<class Phyre::PRendering::PConstantBufferBase>` | 7 | `0068D370` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCapsuleBase>` | 3 |
| `005CEAA0` | `PClassDescriptorAbstract<class Phyre::PRendering::PSamplerState>` | 7 | `0068D4A0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsCallbackData>` | 7 |
| `005CEB20` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PModifierNetworkDynamicMeshInstance>` | 7 | `0068D550` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsBoxBase>` | 7 |
| `005CEBF0` | `PClassDescriptorConcrete<class Phyre::PRendering::PSamplerState>` | 10 | `0068D5B0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCapsuleBase>` | 7 |
| `005CECB0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassParameterLocationTypesBase>` | 7 | `0068D630` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsCharacterCamera>` | 7 |
| `005CED10` | `PClassDescriptorConcrete<class Phyre::PRendering::PSamplerState>` | 3 | `0068D6A0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsCallbackData>` | 7 |
| `005CED40` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderSource>` | 7 | `0068D700` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PPhysics::PPhysicsCallbackData>` | 10 |
| `005CEDA0` | `PClassDescriptorForType<class Phyre::PRendering::PTexture2DBase>` | 7 | `0068D770` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsCharacterCamera>` | 7 |
| `005CEE40` | `PClassDescriptorAbstract<class Phyre::PRendering::PContextVariantFoldingTable>` | 7 | `0068D7D0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PPhysics::PPhysicsCallbackData>` | 7 |
| `005CEEB0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderSource>` | 10 | `0068D830` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterCamera>` | 10 |
| `005CEF10` | `PClassDescriptorConcrete<class Phyre::PRendering::PSamplerState>` | 7 | `0068D850` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterCamera>` | 3 |
| `005CEF70` | `PClassDescriptorConcrete<class Phyre::PRendering::PContextVariantFoldingTable>` | 3 | `0068D960` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterCamera>` | 7 |
| `005CEFA0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferRWTexture3D>` | 7 | `0068DA40` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsBoxBullet>` | 7 |
| `005CF030` | `PClassDescriptorForType<class Phyre::PRendering::PMeshInstanceSegmentContext>` | 7 | `0068DAA0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsCapsuleBullet>` | 7 |
| `005CF090` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderSource>` | 7 | `0068DB80` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsBoxBullet>` | 7 |
| `005CF100` | `PClassDescriptorConcrete<class Phyre::PRendering::PContextVariantFoldingTable>` | 7 | `0068DBE0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsCapsuleBullet>` | 7 |
| `005CF1D0` | `PClassDescriptorAbstract<class Phyre::PRendering::PTexture2DBase>` | 7 | `0068DC40` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsBoxBullet>` | 10 |
| `005CF2B0` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture2DBase>` | 10 | `0068DCE0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCapsuleBullet>` | 10 |
| `005CF360` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture2DBase>` | 3 | `0068DD80` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsBoxBullet>` | 3 |
| `005CF3B0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferRWTexture3D>` | 7 | `0068DE40` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCapsuleBullet>` | 3 |
| `005CF410` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWTexture3D>` | 10 | `0068DE70` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsBoxBullet>` | 7 |
| `005CF430` | `PClassDescriptorAbstract<class Phyre::PRendering::PMeshInstanceSegmentContext>` | 7 | `0068DED0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCapsuleBullet>` | 7 |
| `005CF490` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWTexture3D>` | 3 | `0068E070` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsMaterial>` | 7 |
| `005CF4C0` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture2DBase>` | 7 | `0068E0D0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsWorldBullet>` | 7 |
| `005CF520` | `PClassDescriptorConcrete<class Phyre::PRendering::PMeshInstanceSegmentContext>` | 10 | `0068E300` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsMaterial>` | 7 |
| `005CF550` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterDefinition>` | 7 | `0068E360` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsBox>` | 7 |
| `005CF5B0` | `PClassDescriptorForType<class Phyre::PRendering::PEffectVariant>` | 7 | `0068E3C0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsCapsule>` | 7 |
| `005CF610` | `PClassDescriptorConcrete<class Phyre::PRendering::PMeshInstanceSegmentContext>` | 3 | `0068E420` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsWorldBullet>` | 7 |
| `005CF680` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWTexture3D>` | 7 | `0068E4C0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMaterial>` | 10 |
| `005CF6F0` | `PClassDescriptorConcrete<class Phyre::PRendering::PMeshInstanceSegmentContext>` | 7 | `0068E4D0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsWorldBullet>` | 10 |
| `005CF860` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterDefinition>` | 7 | `0068E4F0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMaterial>` | 3 |
| `005CF8F0` | `PClassDescriptorAbstract<class Phyre::PRendering::PEffectVariant>` | 7 | `0068E520` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsWorldBullet>` | 3 |
| `005CF970` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterDefinition>` | 10 | `0068E590` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsMaterial>` | 7 |
| `005CF9A0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PEffectVariant>` | 10 | `0068E5F0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsWorldBullet>` | 7 |
| `005CFA40` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterDefinition>` | 3 | `0068E6B0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsBox>` | 7 |
| `005CFAD0` | `PClassDescriptorForType<class Phyre::PRendering::PTexture3D>` | 7 | `0068E710` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsCapsule>` | 7 |
| `005CFBA0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterDefinition>` | 7 | `0068E790` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsBox>` | 10 |
| `005CFC00` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PEffectVariant>` | 7 | `0068E840` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCapsule>` | 10 |
| `005CFCA0` | `PClassDescriptorForType<class Phyre::PRendering::PStructuredBufferBase>` | 7 | `0068E940` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsBox>` | 3 |
| `005CFDC0` | `PClassDescriptorForType<class Phyre::PRendering::PRenderTargetBase>` | 7 | `0068EA00` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCapsule>` | 3 |
| `005CFE70` | `PClassDescriptorAbstract<class Phyre::PRendering::PRenderTargetBase>` | 12 | `0068EA30` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsBox>` | 7 |
| `005CFE80` | `PClassDescriptorAbstract<class Phyre::PRendering::PTexture3D>` | 7 | `0068EAB0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCapsule>` | 7 |
| `005CFF00` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture3D>` | 10 | `0068EB10` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsCharacterControllerBase>` | 7 |
| `005CFF90` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferSampler>` | 7 | `0068EBC0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsCharacterControllerBase>` | 7 |
| `005CFFF0` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture3D>` | 3 | `0068EC20` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterControllerBase>` | 10 |
| `005D0010` | `PClassDescriptorAbstract<class Phyre::PRendering::PStructuredBufferBase>` | 7 | `0068EC50` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterControllerBase>` | 3 |
| `005D0070` | `PClassDescriptorAbstract<class Phyre::PRendering::PRenderTargetBase>` | 4 | `0068EC80` | `PPhysics::PPhysicsTaperedCylinder` | 3 |
| `005D0090` | `PClassDescriptorConcrete<class Phyre::PRendering::PStructuredBufferBase>` | 10 | `0068ECD0` | `PClassDescriptorConcrete<class Phyre::PPhysics::PPhysicsCharacterControllerBase>` | 7 |
| `005D00B0` | `PClassDescriptorConcrete<class Phyre::PRendering::PStructuredBufferBase>` | 3 | `0068EF40` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsMeshBase>` | 7 |
| `005D0100` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture3D>` | 7 | `0068EFB0` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsShapeBase>` | 7 |
| `005D0160` | `PClassDescriptorForType<class Phyre::PRendering::PParameterBufferBase>` | 7 | `0068F010` | `PClassDescriptorForType<class Phyre::PPhysics::PPhysicsTaperedCylinder>` | 7 |
| `005D0210` | `PClassDescriptorAbstract<class Phyre::PRendering::PParameterBufferBase>` | 12 | `0068F080` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsShapeBase>` | 12 |
| `005D0220` | `PClassDescriptorAbstract<class Phyre::PRendering::PRenderTargetBase>` | 7 | `0068F0D0` | `PClassDescriptorAbstract<class Phyre::PPhysics::PPhysicsShapeBase>` | 4 |
| `005D02E0` | `PClassDescriptorConcrete<class Phyre::PRendering::PStructuredBufferBase>` | 7 | `00692E60` | `PClassDataMemberArrayDynamic<class Phyre::PSharray<class Phyre::PPhysics::PPhysicsShape * __ptr64> >` | 0 |
| `005D0340` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferSampler>` | 7 | `00692EC0` | `PClassDataMemberPhyreSharray<class Phyre::PPhysics::PPhysicsShape * __ptr64>` | 0 |
| `005D03A0` | `PClassDescriptorAbstract<class Phyre::PRendering::PParameterBufferBase>` | 4 | `00692F20` | `PClassDescriptorAbstract<class Phyre::PSharray<class Phyre::PPhysics::PPhysicsShape * __ptr64> >` | 7 |
| `005D03C0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferSampler>` | 10 | `00692F80` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PPhysics::PPhysicsShape * __ptr64> >` | 7 |
| `005D03E0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferSampler>` | 3 | `00692FE0` | `PClassDescriptorForType<class Phyre::PSharray<class Phyre::PPhysics::PPhysicsShape * __ptr64> >` | 7 |
| `005D0410` | `PClassDescriptorForType<class Phyre::PRendering::PShaderPassParameterLocationTypes>` | 7 | `006930D0` | `PPhysics::PPhysicsBox` | 3 |
| `005D0480` | `PClassDescriptorAbstract<class Phyre::PRendering::PParameterBufferBase>` | 7 | `00693160` | `PPhysics::PPhysicsBoxBase` | 3 |
| `005D0510` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferSampler>` | 7 | `006931B0` | `PPhysics::PPhysicsBoxBullet` | 3 |
| `005D0620` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderPassParameterLocationTypes>` | 7 | `00693240` | `PPhysics::PPhysicsCapsule` | 3 |
| `005D0680` | `PClassDescriptorForType<class Phyre::PRendering::PShaderStreamDefinition>` | 7 | `006932A0` | `PPhysics::PPhysicsCapsuleBase` | 3 |
| `005D0710` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassParameterLocationTypes>` | 3 | `00693330` | `PPhysics::PPhysicsCapsuleBullet` | 3 |
| `005D07A0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassParameterLocationTypes>` | 7 | `00693390` | `PPhysics::PPhysicsCharacterCamera` | 0 |
| `005D08F0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderStreamDefinition>` | 7 | `006933E0` | `PPhysics::PPhysicsCylinder` | 3 |
| `005D09D0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderStreamDefinition>` | 10 | `00693470` | `PPhysics::PPhysicsCylinderBase` | 3 |
| `005D09F0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderStreamDefinition>` | 3 | `006934C0` | `PPhysics::PPhysicsCylinderBullet` | 3 |
| `005D0A60` | `PClassDescriptorForType<class Phyre::PRendering::PNodeContext>` | 7 | `00693550` | `PPhysics::PPhysicsMesh` | 3 |
| `005D0AC0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferStructuredBuffer>` | 7 | `006935C0` | `PPhysics::PPhysicsMeshBase` | 3 |
| `005D0B20` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderStreamDefinition>` | 7 | `00693610` | `PPhysics::PPhysicsMeshBullet` | 3 |
| `005D0BE0` | `PClassDescriptorAbstract<class Phyre::PRendering::PNodeContext>` | 7 | `00693680` | `PPhysics::PPhysicsPlaneBase` | 3 |
| `005D0C40` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferStructuredBuffer>` | 7 | `006936D0` | `PPhysics::PPhysicsPlaneBullet` | 3 |
| `005D0CE0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferStructuredBuffer>` | 10 | `00693760` | `PPhysics::PPhysicsShape` | 3 |
| `005D0D30` | `PClassDescriptorConcrete<class Phyre::PRendering::PNodeContext>` | 3 | `006937B0` | `PPhysics::PPhysicsShapeBase` | 3 |
| `005D0DC0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferStructuredBuffer>` | 3 | `00693800` | `PPhysics::PPhysicsShapeBullet` | 3 |
| `005D0FE0` | `PClassDescriptorConcrete<class Phyre::PRendering::PNodeContext>` | 7 | `00693850` | `PPhysics::PPhysicsSphere` | 3 |
| `005D1040` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferStructuredBuffer>` | 7 | `006938D0` | `PPhysics::PPhysicsSphereBase` | 3 |
| `005D10E0` | `PClassDescriptorForType<class Phyre::PRendering::PTextureCubeMapBase>` | 7 | `00693920` | `PPhysics::PPhysicsSphereBullet` | 3 |
| `005D1180` | `PClassDescriptorForType<class Phyre::PRendering::PParameterBuffer>` | 7 | `006A0EE0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsCharacterCamera,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64>` | 1 |
| `005D11E0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderPass>` | 7 | `006A0F30` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsCharacterCamera,enum Phyre::PResult,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,float>` | 1 |
| `005D1260` | `PClassDescriptorForType<class Phyre::PRendering::PShaderProgramParamsAndStreams>` | 7 | `006A0FE0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsCharacterControllerBase,float>` | 1 |
| `005D1440` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferStream>` | 7 | `006A1050` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsCharacterControllerBase,bool>` | 1 |
| `005D1530` | `PClassDescriptorAbstract<class Phyre::PRendering::PTextureCubeMapBase>` | 7 | `006A10B0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBody,class sce::Vectormath::Scalar::Aos::Vector3>` | 1 |
| `005D15E0` | `PClassDescriptorForType<class Phyre::PRendering::PMeshInstanceBounds>` | 7 | `006A1110` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBody,enum Phyre::PResult>` | 1 |
| `005D1640` | `PClassDescriptorAbstract<class Phyre::PRendering::PParameterBuffer>` | 7 | `006A1170` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBody,void,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64>` | 1 |
| `005D16A0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderPass>` | 7 | `006A11C0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,float>` | 1 |
| `005D1700` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCubeMapBase>` | 10 | `006A1230` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,class Phyre::PScene::PNode * __ptr64>` | 1 |
| `005D1730` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderProgramParamsAndStreams>` | 7 | `006A12B0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,class Phyre::PWorldMatrix * __ptr64>` | 1 |
| `005D17E0` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCubeMapBase>` | 3 | `006A1330` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,void>` | 1 |
| `005D17F0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPass>` | 10 | `006A13B0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,bool>` | 1 |
| `005D1870` | `PClassDescriptorHeaderWithoutDefaultConstructor<class Phyre::PRendering::PParameterBuffer>` | 10 | `006A1410` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,int,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 1 |
| `005D18A0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderProgramParamsAndStreams>` | 10 | `006A14C0` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,int,float,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 1 |
| `005D18C0` | `PClassDescriptorHeaderWithoutDefaultConstructor<class Phyre::PRendering::PParameterBuffer>` | 11 | `006A15A0` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64>` | 1 |
| `005D1940` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPass>` | 3 | `006A1670` | `PInternal::PCallerImplementation::PCallerImplementation5::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 1 |
| `005D1990` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderProgramParamsAndStreams>` | 3 | `006A1770` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,unsigned int,class sce::Vectormath::Scalar::Aos::Vector4 & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 & __ptr64>` | 1 |
| `005D1A10` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCubeMapBase>` | 7 | `006A1840` | `PInternal::PCallerImplementation::PCallerImplementation5::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,float,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64>` | 1 |
| `005D1A90` | `PClassDescriptorForType<class Phyre::PRendering::PConstantBuffer>` | 7 | `006A1940` | `PInternal::PCallerImplementation::PCallerImplementation6::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,float,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 1 |
| `005D1AF0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferStream>` | 7 | `006A2AA0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsCharacterCamera,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64>` | 4 |
| `005D1B50` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPass>` | 7 | `006A2B20` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsCharacterCamera,enum Phyre::PResult,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,float>` | 4 |
| `005D1BD0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderProgramParamsAndStreams>` | 7 | `006A2BD0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsCharacterControllerBase,float>` | 4 |
| `005D1C70` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferStream>` | 3 | `006A2C50` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsCharacterControllerBase,bool>` | 4 |
| `005D1CA0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferRWStructuredBuffer>` | 7 | `006A2CD0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBody,class sce::Vectormath::Scalar::Aos::Vector3>` | 4 |
| `005D1D30` | `PClassDescriptorAbstract<class Phyre::PRendering::PMeshInstanceBounds>` | 7 | `006A2D50` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBody,enum Phyre::PResult>` | 4 |
| `005D1DC0` | `PClassDescriptorHeaderWithoutDefaultConstructor<class Phyre::PRendering::PParameterBuffer>` | 7 | `006A2DD0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBody,void,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64>` | 4 |
| `005D1E20` | `PClassDescriptorConcrete<class Phyre::PRendering::PMeshInstanceBounds>` | 10 | `006A2E60` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,float>` | 4 |
| `005D1EA0` | `PClassDescriptorConcrete<class Phyre::PRendering::PMeshInstanceBounds>` | 3 | `006A2EE0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,class Phyre::PScene::PNode * __ptr64>` | 4 |
| `005D1ED0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferStream>` | 7 | `006A2F60` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,class Phyre::PWorldMatrix * __ptr64>` | 4 |
| `005D1F50` | `PClassDescriptorAbstract<class Phyre::PRendering::PConstantBuffer>` | 7 | `006A2FE0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,void>` | 4 |
| `005D1FB0` | `PClassDescriptorConcrete<class Phyre::PRendering::PMeshInstanceBounds>` | 7 | `006A3060` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,void,class sce::Vectormath::Scalar::Aos::Quat const & __ptr64>` | 4 |
| `005D2030` | `PClassDescriptorForType<class Phyre::PRendering::PShaderPassParameterLocationTypesConstantBuffer>` | 7 | `006A30F0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,void,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64>` | 4 |
| `005D2090` | `PClassDescriptorConcrete<class Phyre::PRendering::PConstantBuffer>` | 10 | `006A3180` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,bool>` | 4 |
| `005D2110` | `PClassDescriptorConcrete<class Phyre::PRendering::PConstantBuffer>` | 3 | `006A3200` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,int,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 4 |
| `005D2140` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferRWStructuredBuffer>` | 7 | `006A32B0` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,int,float,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 4 |
| `005D21E0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWStructuredBuffer>` | 10 | `006A3370` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64>` | 4 |
| `005D2200` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWStructuredBuffer>` | 3 | `006A3430` | `PInternal::PCallerImplementation::PCallerImplementation5::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 4 |
| `005D2250` | `PClassDescriptorConcrete<class Phyre::PRendering::PConstantBuffer>` | 7 | `006A3500` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,unsigned int,class sce::Vectormath::Scalar::Aos::Vector4 & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 & __ptr64>` | 4 |
| `005D22E0` | `PClassDescriptorForType<class Phyre::PRendering::PSceneRenderPass>` | 7 | `006A35B0` | `PInternal::PCallerImplementation::PCallerImplementation5::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,float,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64>` | 4 |
| `005D2340` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWStructuredBuffer>` | 7 | `006A3680` | `PInternal::PCallerImplementation::PCallerImplementation6::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,float,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 4 |
| `005D23D0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderPassParameterLocationTypesConstantBuffer>` | 7 | `006A3760` | `PClassDataMemberPhyreSharray<class Phyre::PPhysics::PPhysicsShape * __ptr64>` | 9 |
| `005D24C0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassParameterLocationTypesConstantBuffer>` | 3 | `006A3E00` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBody,class sce::Vectormath::Scalar::Aos::Vector3>` | 3 |
| `005D2630` | `PClassDescriptorForType<class Phyre::PRendering::PShaderProgramBase>` | 7 | `006A4010` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PPhysics::PPhysicsShape * __ptr64> >` | 3 |
| `005D26F0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassParameterLocationTypesConstantBuffer>` | 7 | `006A4100` | `PPhysics::PUtilityPhysics` | 1 |
| `005D2750` | `PClassDescriptorAbstract<class Phyre::PRendering::PSceneRenderPass>` | 7 | `006A6640` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsCharacterCamera,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64>` | 2 |
| `005D27B0` | `PClassDescriptorConcrete<class Phyre::PRendering::PSceneRenderPass>` | 10 | `006A66D0` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsCharacterCamera,enum Phyre::PResult,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,float>` | 2 |
| `005D27F0` | `PClassDescriptorForType<class Phyre::PRendering::PMaterialSwitch>` | 7 | `006A6800` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBody,class sce::Vectormath::Scalar::Aos::Vector3>` | 2 |
| `005D2850` | `PClassDescriptorConcrete<class Phyre::PRendering::PSceneRenderPass>` | 3 | `006A6870` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBody,enum Phyre::PResult>` | 2 |
| `005D28A0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferTextureBase>` | 7 | `006A68F0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsRigidBodyBase,class Phyre::PScene::PNode * __ptr64>` | 2 |
| `005D2950` | `PClassDescriptorConcrete<class Phyre::PRendering::PSceneRenderPass>` | 7 | `006A69F0` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,int,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 2 |
| `005D29B0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderProgramBase>` | 7 | `006A6A80` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,int,float,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 2 |
| `005D2AB0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderProgramBase>` | 3 | `006A6B20` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64>` | 2 |
| `005D2AC0` | `PClassDescriptorAbstract<class Phyre::PRendering::PMaterialSwitch>` | 7 | `006A6BD0` | `PInternal::PCallerImplementation::PCallerImplementation5::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 2 |
| `005D2B20` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferTextureBase>` | 7 | `006A6CA0` | `PInternal::PCallerImplementation::PCallerImplementation3::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,unsigned int,class sce::Vectormath::Scalar::Aos::Vector4 & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 & __ptr64>` | 2 |
| `005D2BA0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderProgramBase>` | 7 | `006A6D40` | `PInternal::PCallerImplementation::PCallerImplementation5::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,float,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64>` | 2 |
| `005D2C00` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferByteAddressBuffer>` | 7 | `006A6E00` | `PInternal::PCallerImplementation::PCallerImplementation6::PMethodCallerConcrete<class Phyre::PPhysics::PPhysicsWorld,class Phyre::PTypedObject,float,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4 * __ptr64,enum Phyre::PPhysics::PPhysicsRigidBodyBase::PCollisionGroup>` | 2 |
| `005D2C60` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderParameterCaptureBufferTextureBase>` | 10 | `006A6FA0` | `PClassDescriptorForType<class Phyre::PString>` | 7 |
| `005D2C80` | `PClassDescriptorConcrete<class Phyre::PRendering::PMaterialSwitch>` | 3 | `006A7030` | `PClassDescriptorAbstract<class Phyre::PString>` | 7 |
| `005D2DA0` | `PClassDescriptorConcrete<class Phyre::PRendering::PMaterialSwitch>` | 7 | `006A7090` | `PClassDescriptorConcrete<class Phyre::PString>` | 10 |
| `005D2E30` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderParameterCaptureBufferTextureBase>` | 7 | `006A70A0` | `PClassDescriptorConcrete<class Phyre::PString>` | 3 |
| `005D2F10` | `PClassDescriptorForType<class Phyre::PRendering::PShaderPassStateBase>` | 7 | `006A7130` | `PClassDescriptorConcrete<class Phyre::PString>` | 7 |
| `005D2FC0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferByteAddressBuffer>` | 7 | `006A7250` | `PClassDataMemberArrayDynamic<class Phyre::PString>` | 0 |
| `005D3090` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferByteAddressBuffer>` | 10 | `006A76E0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PString,char const * __ptr64>` | 1 |
| `005D3100` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferByteAddressBuffer>` | 3 | `006A7740` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PString,char const * __ptr64>` | 4 |
| `005D3150` | `PClassDescriptorForType<class Phyre::PRendering::PShaderVertexProgram>` | 7 | `006A78E0` | `PClassDescriptorConcrete<class Phyre::PGameplay::PTrigger>` | 7 |
| `005D3270` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferByteAddressBuffer>` | 7 | `006A7A20` | `PClassDescriptorForType<class Phyre::PGameplay::PTrigger>` | 7 |
| `005D3320` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderPassStateBase>` | 7 | `006A7AB0` | `PClassDescriptorAbstract<class Phyre::PGameplay::PTrigger>` | 7 |
| `005D3380` | `PClassDescriptorForType<class Phyre::PRendering::PRenderTarget>` | 7 | `006A7B10` | `PClassDescriptorConcrete<class Phyre::PGameplay::PTrigger>` | 10 |
| `005D3400` | `PClassDescriptorForType<class Phyre::PRendering::PTexture2D>` | 7 | `006A7B70` | `PClassDescriptorConcrete<class Phyre::PGameplay::PTrigger>` | 3 |
| `005D34A0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassStateBase>` | 10 | `006A7D00` | `PClassDataMemberArrayDynamic<class Phyre::PSharray<class Phyre::PGameplay::PTriggerReceiverComponent * __ptr64> >` | 0 |
| `005D3510` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassStateBase>` | 3 | `006A7D60` | `PClassDataMemberPhyreSharray<class Phyre::PGameplay::PTriggerReceiverComponent * __ptr64>` | 0 |
| `005D3530` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderVertexProgram>` | 7 | `006A7DC0` | `PClassDescriptorAbstract<class Phyre::PSharray<class Phyre::PGameplay::PTriggerReceiverComponent * __ptr64> >` | 7 |
| `005D35B0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderVertexProgram>` | 10 | `006A7E20` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PGameplay::PTriggerReceiverComponent * __ptr64> >` | 7 |
| `005D3620` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassStateBase>` | 7 | `006A7E80` | `PClassDescriptorForType<class Phyre::PSharray<class Phyre::PGameplay::PTriggerReceiverComponent * __ptr64> >` | 7 |
| `005D3680` | `PClassDescriptorForType<class Phyre::PRendering::PShader>` | 7 | `006A8D10` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PGameplay::PTrigger,class Phyre::PWorldMatrix * __ptr64>` | 1 |
| `005D36F0` | `PClassDescriptorAbstract<class Phyre::PRendering::PRenderTarget>` | 7 | `006A8D90` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGameplay::PTrigger,void,bool>` | 1 |
| `005D3790` | `PClassDescriptorAbstract<class Phyre::PRendering::PTexture2D>` | 7 | `006A8DF0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PGameplay::PTrigger,bool>` | 1 |
| `005D37F0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderVertexProgram>` | 7 | `006A8E50` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGameplay::PTrigger,bool,char const * __ptr64>` | 1 |
| `005D3850` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PRenderTarget>` | 10 | `006A8F20` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PGameplay::PTrigger,class Phyre::PWorldMatrix * __ptr64>` | 4 |
| `005D38D0` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture2D>` | 10 | `006A8FA0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGameplay::PTrigger,void,bool>` | 4 |
| `005D3960` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture2D>` | 3 | `006A9030` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PGameplay::PTrigger,bool>` | 4 |
| `005D3A90` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PRenderTarget>` | 7 | `006A90B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGameplay::PTrigger,bool,char const * __ptr64>` | 4 |
| `005D3B70` | `PClassDescriptorAbstract<class Phyre::PRendering::PShader>` | 7 | `006A9140` | `PClassDataMemberPhyreSharray<class Phyre::PGameplay::PTriggerReceiverComponent * __ptr64>` | 9 |
| `005D3BD0` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture2D>` | 7 | `006A9190` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PGameplay::PTriggerReceiverComponent * __ptr64> >` | 3 |
| `005D3C60` | `PClassDescriptorConcrete<class Phyre::PRendering::PShader>` | 10 | `006A93C0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PGameplay::PTrigger,bool,char const * __ptr64>` | 2 |
| `005D3CB0` | `PClassDescriptorForType<class Phyre::PRendering::PStructuredBuffer>` | 7 | `006A9500` | `PClassDescriptorForType<class Phyre::PGameplay::PQuarryComponent>` | 7 |
| `005D3D10` | `PClassDescriptorConcrete<class Phyre::PRendering::PShader>` | 3 | `006A9590` | `PClassDescriptorAbstract<class Phyre::PGameplay::PQuarryComponent>` | 7 |
| `005D3DD0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferLocation>` | 7 | `006A95F0` | `PClassDescriptorConcrete<class Phyre::PGameplay::PQuarryComponent>` | 10 |
| `005D3E30` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferRWByteAddressBuffer>` | 7 | `006A9620` | `PClassDescriptorConcrete<class Phyre::PGameplay::PQuarryComponent>` | 3 |
| `005D3EB0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShader>` | 7 | `006A96C0` | `PClassDescriptorConcrete<class Phyre::PGameplay::PQuarryComponent>` | 7 |
| `005D3F30` | `PClassDescriptorForType<class Phyre::PRendering::PShadowRenderer>` | 7 | `006A9CA0` | `PClassDescriptorForType<class Phyre::PTypedObject>` | 7 |
| `005D4060` | `PClassDescriptorAbstract<class Phyre::PRendering::PStructuredBuffer>` | 7 | `006A9D50` | `PClassDescriptorAbstract<class Phyre::PTypedObject>` | 7 |
| `005D4100` | `PClassDescriptorConcrete<class Phyre::PRendering::PStructuredBuffer>` | 10 | `006A9DB0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PTypedObject>` | 10 |
| `005D4160` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferLocation>` | 7 | `006A9DF0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PTypedObject>` | 7 |
| `005D41C0` | `PClassDescriptorConcrete<class Phyre::PRendering::PStructuredBuffer>` | 3 | `006AA230` | `PThreadPool` | 1 |
| `005D41D0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferRWByteAddressBuffer>` | 7 | `006AA780` | `PClassDescriptorForType<class Phyre::PComponent>` | 7 |
| `005D4230` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWByteAddressBuffer>` | 10 | `006AA840` | `PClassDescriptorAbstract<class Phyre::PComponent>` | 7 |
| `005D4260` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferLocation>` | 3 | `006AA8A0` | `PClassDescriptorConcrete<class Phyre::PComponent>` | 10 |
| `005D4280` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWByteAddressBuffer>` | 3 | `006AA8E0` | `PClassDescriptorConcrete<class Phyre::PComponent>` | 3 |
| `005D42B0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderFragmentProgram>` | 7 | `006AA910` | `PClassDescriptorConcrete<class Phyre::PComponent>` | 7 |
| `005D4340` | `PClassDescriptorAbstract<class Phyre::PRendering::PShadowRenderer>` | 7 | `006AB030` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PComponent,class Phyre::PClassDescriptor const & __ptr64>` | 1 |
| `005D43C0` | `PClassDescriptorConcrete<class Phyre::PRendering::PStructuredBuffer>` | 7 | `006AB090` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PComponent,class Phyre::PEntity * __ptr64>` | 1 |
| `005D4480` | `PClassDescriptorConcrete<class Phyre::PRendering::PShadowRenderer>` | 3 | `006AB110` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PComponent,class Phyre::PClassDescriptor const & __ptr64>` | 4 |
| `005D44F0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferLocation>` | 7 | `006AB190` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PComponent,class Phyre::PEntity * __ptr64>` | 4 |
| `005D4550` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferRWByteAddressBuffer>` | 7 | `006AB270` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PComponent,class Phyre::PEntity * __ptr64>` | 2 |
| `005D45D0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShadowRenderer>` | 7 | `006AB380` | `PClassDescriptorForType<class Phyre::PEntity>` | 7 |
| `005D4630` | `PClassDescriptorForType<class Phyre::PRendering::PMaterial>` | 7 | `006AB440` | `PClassDescriptorAbstract<class Phyre::PEntity>` | 7 |
| `005D4730` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderFragmentProgram>` | 7 | `006AB4A0` | `PClassDescriptorConcrete<class Phyre::PEntity>` | 10 |
| `005D4850` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderFragmentProgram>` | 10 | `006AB4D0` | `PClassDescriptorConcrete<class Phyre::PEntity>` | 3 |
| `005D4960` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferTexture2D>` | 7 | `006AB4E0` | `PClassDescriptorConcrete<class Phyre::PEntity>` | 7 |
| `005D49D0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderFragmentProgram>` | 7 | `006AC3D0` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PEntity * __ptr64,class Phyre::PWorldMatrix * __ptr64>` | 1 |
| `005D4A30` | `PClassDescriptorAbstract<class Phyre::PRendering::PMaterial>` | 7 | `006AC440` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PEntity * __ptr64,class Phyre::PTypedObject>` | 1 |
| `005D4A90` | `PClassDescriptorForType<class Phyre::PRendering::PMeshInstance>` | 7 | `006AC4F0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PEntity,class Phyre::PWorldMatrix * __ptr64>` | 1 |
| `005D4AF0` | `PClassDescriptorForType<class Phyre::PRendering::PEffect>` | 7 | `006AC570` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PEntity,class Phyre::PTypedObject,class Phyre::PClassDescriptor const & __ptr64>` | 1 |
| `005D4B70` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PMaterial>` | 10 | `006AC620` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PEntity,enum Phyre::PResult,class Phyre::PComponent & __ptr64>` | 1 |
| `005D4D90` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PMaterial>` | 7 | `006AC6A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PEntity,void,class Phyre::PWorldMatrix * __ptr64>` | 1 |
| `005D4DF0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferTexture2D>` | 7 | `006AC6F0` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PEntity * __ptr64,class Phyre::PWorldMatrix * __ptr64>` | 4 |
| `005D4E50` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferTexture2D>` | 10 | `006AC770` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PEntity * __ptr64,class Phyre::PTypedObject>` | 4 |
| `005D4E70` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureConstantBuffer>` | 7 | `006AC7E0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PEntity,class Phyre::PWorldMatrix * __ptr64>` | 4 |
| `005D4F10` | `PClassDescriptorAbstract<class Phyre::PRendering::PMeshInstance>` | 7 | `006AC860` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PEntity,class Phyre::PTypedObject,class Phyre::PClassDescriptor const & __ptr64>` | 4 |
| `005D4F70` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferLocationSize>` | 7 | `006AC8F0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PEntity,enum Phyre::PResult,class Phyre::PComponent & __ptr64>` | 4 |
| `005D5010` | `PClassDescriptorAbstract<class Phyre::PRendering::PEffect>` | 7 | `006AC980` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PEntity,void,class Phyre::PWorldMatrix * __ptr64>` | 4 |
| `005D50B0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferTexture2D>` | 3 | `006ACBB0` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PEntity * __ptr64,class Phyre::PWorldMatrix * __ptr64>` | 2 |
| `005D50E0` | `PClassDescriptorForType<class Phyre::PRendering::PIndirectArgsBufferBase>` | 7 | `006ACC20` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PEntity * __ptr64,class Phyre::PTypedObject>` | 2 |
| `005D51C0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PMeshInstance>` | 10 | `006ACDF0` | `PClassDescriptorForType<class Phyre::PCameraOrthographic>` | 7 |
| `005D5240` | `PClassDescriptorConcrete<class Phyre::PRendering::PEffect>` | 10 | `006ACE80` | `PClassDescriptorAbstract<class Phyre::PCameraOrthographic>` | 7 |
| `005D5300` | `PClassDescriptorConcrete<class Phyre::PRendering::PEffect>` | 3 | `006ACEE0` | `PClassDescriptorConcrete<class Phyre::PCameraOrthographic>` | 10 |
| `005D5410` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferTexture2D>` | 7 | `006ACF30` | `PClassDescriptorConcrete<class Phyre::PCameraOrthographic>` | 3 |
| `005D5570` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PMeshInstance>` | 7 | `006ACF90` | `PClassDescriptorConcrete<class Phyre::PCameraOrthographic>` | 7 |
| `005D55D0` | `PClassDescriptorConcrete<class Phyre::PRendering::PEffect>` | 7 | `006AD4A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCameraOrthographic,void,class sce::Vectormath::Scalar::Aos::Vector4 const * __ptr64>` | 1 |
| `005D56B0` | `PClassDescriptorForType<class Phyre::PRendering::PTexture3DBase>` | 7 | `006AD4F0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCameraOrthographic,void,class sce::Vectormath::Scalar::Aos::Vector4 const * __ptr64>` | 4 |
| `005D5710` | `PClassDescriptorForType<class Phyre::PRendering::PForwardShadowRenderer>` | 7 | `006AD660` | `PClassDescriptorForType<class Phyre::PCameraPerspective>` | 7 |
| `005D5770` | `PClassDescriptorForType<class Phyre::PRendering::PShaderPassBase>` | 7 | `006AD6F0` | `PClassDescriptorAbstract<class Phyre::PCameraPerspective>` | 7 |
| `005D57D0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureConstantBuffer>` | 7 | `006AD750` | `PClassDescriptorConcrete<class Phyre::PCameraPerspective>` | 10 |
| `005D5840` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferLocationSize>` | 7 | `006AD7A0` | `PClassDescriptorConcrete<class Phyre::PCameraPerspective>` | 3 |
| `005D58D0` | `PClassDescriptorAbstract<class Phyre::PRendering::PIndirectArgsBufferBase>` | 7 | `006AD800` | `PClassDescriptorConcrete<class Phyre::PCameraPerspective>` | 7 |
| `005D5930` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureConstantBuffer>` | 10 | `006ADD00` | `PClassDescriptorForType<class Phyre::PInstancesComponent>` | 7 |
| `005D5950` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureConstantBuffer>` | 3 | `006ADDA0` | `PClassDescriptorAbstract<class Phyre::PInstancesComponent>` | 7 |
| `005D5980` | `PClassDescriptorForType<class Phyre::PRendering::PSamplerStateBase>` | 7 | `006ADE00` | `PClassDescriptorConcrete<class Phyre::PInstancesComponent>` | 10 |
| `005D59E0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferLocationSize>` | 3 | `006ADE40` | `PClassDescriptorConcrete<class Phyre::PInstancesComponent>` | 3 |
| `005D5A00` | `PClassDescriptorForType<class Phyre::PRendering::PShaderGeometryProgram>` | 7 | `006ADE70` | `PClassDescriptorConcrete<class Phyre::PInstancesComponent>` | 7 |
| `005D5A60` | `PClassDescriptorConcrete<class Phyre::PRendering::PIndirectArgsBufferBase>` | 3 | `006AE010` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PTypedObject,8> >` | 0 |
| `005D5B00` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureConstantBuffer>` | 7 | `006AE070` | `PClassDataMemberPhyreArray<class Phyre::PTypedObject>` | 0 |
| `005D5B60` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferLocationSize>` | 7 | `006AE0D0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PTypedObject,8> >` | 7 |
| `005D5BC0` | `PClassDescriptorConcrete<class Phyre::PRendering::PIndirectArgsBufferBase>` | 7 | `006AE130` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PTypedObject,8> >` | 7 |
| `005D5C40` | `PClassDescriptorAbstract<class Phyre::PRendering::PTexture3DBase>` | 7 | `006AE190` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PTypedObject,8> >` | 7 |
| `005D5CC0` | `PClassDescriptorAbstract<class Phyre::PRendering::PForwardShadowRenderer>` | 7 | `006AF060` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PInstancesComponent,class Phyre::PArray<class Phyre::PTypedObject,8> const & __ptr64>` | 1 |
| `005D5D20` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderPassBase>` | 7 | `006AF0C0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInstancesComponent,class Phyre::PTypedObject const & __ptr64,unsigned int>` | 1 |
| `005D5D80` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture3DBase>` | 10 | `006AF170` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PInstancesComponent,unsigned int>` | 1 |
| `005D5DF0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassBase>` | 10 | `006AF1D0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInstancesComponent,class Phyre::PTypedObject,class Phyre::PClassDescriptor const * __ptr64>` | 1 |
| `005D5E10` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture3DBase>` | 3 | `006AF2C0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PInstancesComponent,class Phyre::PArray<class Phyre::PTypedObject,8> const & __ptr64>` | 4 |
| `005D5E40` | `PClassDescriptorConcrete<class Phyre::PRendering::PForwardShadowRenderer>` | 3 | `006AF340` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInstancesComponent,class Phyre::PTypedObject const & __ptr64,unsigned int>` | 4 |
| `005D5EB0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassBase>` | 3 | `006AF3D0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PInstancesComponent,unsigned int>` | 4 |
| `005D5EE0` | `PClassDescriptorAbstract<class Phyre::PRendering::PSamplerStateBase>` | 7 | `006AF450` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInstancesComponent,class Phyre::PTypedObject,class Phyre::PClassDescriptor const * __ptr64>` | 4 |
| `005D5F80` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderGeometryProgram>` | 7 | `006AF590` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PInstancesComponent,class Phyre::PArray<class Phyre::PTypedObject,8> const & __ptr64>` | 3 |
| `005D5FE0` | `PClassDescriptorConcrete<class Phyre::PRendering::PSamplerStateBase>` | 10 | `006AF5B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInstancesComponent,class Phyre::PTypedObject const & __ptr64,unsigned int>` | 3 |
| `005D6010` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderGeometryProgram>` | 10 | `006AF5C0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PTypedObject,8> >` | 3 |
| `005D60A0` | `PClassDescriptorConcrete<class Phyre::PRendering::PSamplerStateBase>` | 3 | `006AF740` | `PClassDataMemberPhyreArray<class Phyre::PTypedObject>` | 5 |
| `005D60B0` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture3DBase>` | 7 | `006AF810` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PInstancesComponent,class Phyre::PArray<class Phyre::PTypedObject,8> const & __ptr64>` | 2 |
| `005D6110` | `PClassDescriptorConcrete<class Phyre::PRendering::PForwardShadowRenderer>` | 7 | `006AF890` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInstancesComponent,class Phyre::PTypedObject const & __ptr64,unsigned int>` | 2 |
| `005D6170` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassBase>` | 7 | `006AFA00` | `PClassDescriptorForType<class Phyre::PNameComponent>` | 7 |
| `005D6220` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferTexture3D>` | 7 | `006AFAA0` | `PClassDescriptorAbstract<class Phyre::PNameComponent>` | 7 |
| `005D62D0` | `PClassDescriptorConcrete<class Phyre::PRendering::PSamplerStateBase>` | 7 | `006AFB00` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PNameComponent>` | 10 |
| `005D6330` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderGeometryProgram>` | 7 | `006AFB10` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PNameComponent>` | 7 |
| `005D6450` | `PClassDescriptorForType<class Phyre::PRendering::PTextureCubeMap>` | 7 | `006B00A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PNameComponent * __ptr64,char const * __ptr64>` | 1 |
| `005D6550` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferTexture3D>` | 7 | `006B0110` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PNameComponent * __ptr64,char const * __ptr64>` | 4 |
| `005D6600` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferTexture3D>` | 10 | `006B0190` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PNameComponent * __ptr64,char const * __ptr64>` | 3 |
| `005D6640` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferDataBlock>` | 7 | `006B01A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PFunctionCallerConcrete<class Phyre::PNameComponent * __ptr64,char const * __ptr64>` | 2 |
| `005D66C0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType>` | 7 | `006B02A0` | `PClassDescriptorForType<class Phyre::PRandom::PRandomGenerator>` | 7 |
| `005D6720` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferTexture3D>` | 3 | `006B0330` | `PClassDescriptorAbstract<class Phyre::PRandom::PRandomGenerator>` | 7 |
| `005D67B0` | `PClassDescriptorAbstract<class Phyre::PRendering::PTextureCubeMap>` | 7 | `006B0390` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRandom::PRandomGenerator>` | 7 |
| `005D6810` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferTexture3D>` | 7 | `006B1E00` | `PClassDescriptorForType<class sce::Vectormath::Scalar::Aos::Matrix3>` | 7 |
| `005D6870` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCubeMap>` | 10 | `006B1E60` | `PClassDescriptorForType<class sce::Vectormath::Scalar::Aos::Matrix4>` | 7 |
| `005D6920` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCubeMap>` | 3 | `006B1EC0` | `PClassDescriptorForType<class Phyre::PMatrix4>` | 7 |
| `005D6930` | `PClassDescriptorForType<class Phyre::PRendering::PDynamicMeshInstance>` | 7 | `006B1F20` | `PClassDescriptorForType<class sce::Vectormath::Scalar::Aos::Point3>` | 7 |
| `005D69F0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferDataBlock>` | 7 | `006B1F80` | `PClassDescriptorForType<class sce::Vectormath::Scalar::Aos::Quat>` | 7 |
| `005D6A90` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType>` | 7 | `006B1FE0` | `PClassDescriptorForType<class sce::Vectormath::Scalar::Aos::Vector2>` | 7 |
| `005D6AF0` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCubeMap>` | 7 | `006B2040` | `PClassDescriptorForType<class sce::Vectormath::Scalar::Aos::Vector3>` | 7 |
| `005D6B50` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferDataBlock>` | 10 | `006B20A0` | `PClassDescriptorForType<class sce::Vectormath::Scalar::Aos::Vector4>` | 7 |
| `005D6B70` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType>` | 10 | `006B2100` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Matrix3>` | 7 |
| `005D6BB0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferDataBlock>` | 3 | `006B2160` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Matrix4>` | 7 |
| `005D6BE0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType>` | 3 | `006B21C0` | `PClassDescriptorWrapper<class Phyre::PMatrix4>` | 7 |
| `005D6C10` | `PClassDescriptorForType<class Phyre::PRendering::PShaderComputeProgram>` | 7 | `006B2220` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Point3>` | 7 |
| `005D6CC0` | `PClassDescriptorAbstract<class Phyre::PRendering::PDynamicMeshInstance>` | 7 | `006B2280` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Quat>` | 7 |
| `005D6D20` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferDataBlock>` | 7 | `006B22E0` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Vector2>` | 7 |
| `005D6D80` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType>` | 7 | `006B2340` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Vector3>` | 7 |
| `005D6E00` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PDynamicMeshInstance>` | 10 | `006B23A0` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Vector4>` | 7 |
| `005D6F40` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PDynamicMeshInstance>` | 7 | `006B2400` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Point3,class sce::Vectormath::Scalar::Aos::Point3 & __ptr64,float>` | 1 |
| `005D6FD0` | `PClassDescriptorForType<class Phyre::PRendering::PSceneWideParameterBuffer>` | 7 | `006B2480` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Quat,class sce::Vectormath::Scalar::Aos::Quat & __ptr64,float>` | 1 |
| `005D7090` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderComputeProgram>` | 7 | `006B2500` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Vector2,class sce::Vectormath::Scalar::Aos::Vector2 & __ptr64,float>` | 1 |
| `005D7110` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderComputeProgram>` | 10 | `006B2580` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Vector3,class sce::Vectormath::Scalar::Aos::Vector3 & __ptr64,float>` | 1 |
| `005D71A0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferTextureCubeMap>` | 7 | `006B2600` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4 & __ptr64,float>` | 1 |
| `005D7300` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderComputeProgram>` | 7 | `006B2680` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Point3,class sce::Vectormath::Scalar::Aos::Point3 & __ptr64,float>` | 4 |
| `005D7360` | `PClassDescriptorForType<class Phyre::PRendering::PMeshInstanceSegmentStreamBinding>` | 7 | `006B2710` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Quat,class sce::Vectormath::Scalar::Aos::Quat & __ptr64,float>` | 4 |
| `005D7450` | `PClassDescriptorAbstract<class Phyre::PRendering::PSceneWideParameterBuffer>` | 7 | `006B27A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Vector2,class sce::Vectormath::Scalar::Aos::Vector2 & __ptr64,float>` | 4 |
| `005D7580` | `PClassDescriptorConcrete<class Phyre::PRendering::PSceneWideParameterBuffer>` | 3 | `006B2830` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Vector3,class sce::Vectormath::Scalar::Aos::Vector3 & __ptr64,float>` | 4 |
| `005D75B0` | `PClassDescriptorForType<class Phyre::PRendering::PTextureCommonBase>` | 7 | `006B28C0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4 & __ptr64,float>` | 4 |
| `005D7630` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferTextureCubeMap>` | 7 | `006B2990` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Point3,class sce::Vectormath::Scalar::Aos::Point3 & __ptr64,float>` | 3 |
| `005D76A0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferTextureCubeMap>` | 10 | `006B29B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Quat,class sce::Vectormath::Scalar::Aos::Quat & __ptr64,float>` | 3 |
| `005D76C0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferIndexDataBlock>` | 7 | `006B29D0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Vector2,class sce::Vectormath::Scalar::Aos::Vector2 & __ptr64,float>` | 3 |
| `005D7770` | `PClassDescriptorConcrete<class Phyre::PRendering::PSceneWideParameterBuffer>` | 7 | `006B29F0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4 & __ptr64,float>` | 3 |
| `005D77D0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferTextureCubeMap>` | 3 | `006B2A10` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Matrix3>` | 3 |
| `005D7800` | `PClassDescriptorForType<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer>` | 7 | `006B2AE0` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Vector2>` | 3 |
| `005D78A0` | `PClassDescriptorAbstract<class Phyre::PRendering::PMeshInstanceSegmentStreamBinding>` | 7 | `006B2DF0` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Matrix3>` | 4 |
| `005D7990` | `PClassDescriptorConcrete<class Phyre::PRendering::PMeshInstanceSegmentStreamBinding>` | 3 | `006B2E10` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Point3>` | 4 |
| `005D79F0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferTextureCubeMap>` | 7 | `006B2E20` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Quat>` | 4 |
| `005D7AE0` | `PClassDescriptorAbstract<class Phyre::PRendering::PTextureCommonBase>` | 7 | `006B2E30` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Vector2>` | 4 |
| `005D7B60` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCommonBase>` | 10 | `006B2E40` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Vector3>` | 4 |
| `005D7BD0` | `PClassDescriptorForType<class Phyre::PRendering::PIndirectArgsBuffer>` | 7 | `006B2E50` | `PClassDescriptorWrapper<class sce::Vectormath::Scalar::Aos::Vector4>` | 4 |
| `005D7C30` | `PClassDescriptorConcrete<class Phyre::PRendering::PMeshInstanceSegmentStreamBinding>` | 7 | `006B3120` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Point3,class sce::Vectormath::Scalar::Aos::Point3 & __ptr64,float>` | 2 |
| `005D7C90` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCommonBase>` | 3 | `006B31B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Quat,class sce::Vectormath::Scalar::Aos::Quat & __ptr64,float>` | 2 |
| `005D7CE0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferIndexDataBlock>` | 7 | `006B3240` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Vector2,class sce::Vectormath::Scalar::Aos::Vector2 & __ptr64,float>` | 2 |
| `005D7D60` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer>` | 7 | `006B32D0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Vector3,class sce::Vectormath::Scalar::Aos::Vector3 & __ptr64,float>` | 2 |
| `005D7DC0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferIndexDataBlock>` | 10 | `006B3360` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4 & __ptr64,float>` | 2 |
| `005D7DE0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer>` | 10 | `006B36C0` | `PClassDescriptorForType<class Phyre::PMatrix4x3>` | 7 |
| `005D7E00` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferIndexDataBlock>` | 3 | `006B3720` | `PClassDescriptorWrapper<class Phyre::PMatrix4x3>` | 7 |
| `005D7E30` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer>` | 3 | `006B38C0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PMatrix4x3,class Phyre::PMatrix4x3 & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64>` | 1 |
| `005D7E60` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCommonBase>` | 7 | `006B3930` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PMatrix4x3,class Phyre::PMatrix4x3 & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64>` | 4 |
| `005D7EC0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderPassInfo>` | 7 | `006B39E0` | `PClassDescriptorWrapper<class Phyre::PMatrix4x3>` | 3 |
| `005D7F50` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferIndexDataBlock>` | 7 | `006B3A90` | `PClassDescriptorWrapper<class Phyre::PMatrix4x3>` | 4 |
| `005D7FB0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer>` | 7 | `006B3B10` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PMatrix4x3,class Phyre::PMatrix4x3 & __ptr64,class sce::Vectormath::Scalar::Aos::Vector3 const & __ptr64>` | 2 |
| `005D8010` | `PClassDescriptorAbstract<class Phyre::PRendering::PIndirectArgsBuffer>` | 7 | `006B3C70` | `PClassDescriptorForType<class Phyre::PScene::PNode>` | 7 |
| `005D8090` | `PClassDescriptorConcrete<class Phyre::PRendering::PIndirectArgsBuffer>` | 10 | `006B3D00` | `PClassDescriptorAbstract<class Phyre::PScene::PNode>` | 7 |
| `005D8110` | `PClassDescriptorConcrete<class Phyre::PRendering::PIndirectArgsBuffer>` | 3 | `006B3D60` | `PClassDescriptorConcrete<class Phyre::PScene::PNode>` | 10 |
| `005D81D0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderPassInfo>` | 7 | `006B3DB0` | `PClassDescriptorConcrete<class Phyre::PScene::PNode>` | 3 |
| `005DFF20` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PEffectVariant * __ptr64,8> >` | 0 | `006B3DE0` | `PClassDescriptorConcrete<class Phyre::PScene::PNode>` | 7 |
| `005DFF80` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkInstance * __ptr64,8> >` | 0 | `006B5310` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PMatrix4 const & __ptr64>` | 1 |
| `005DFFE0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PSceneRenderPass * __ptr64,8> >` | 0 | `006B5360` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PString const & __ptr64>` | 1 |
| `005E0040` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PContextSwitch const * __ptr64,8> >` | 0 | `006B53C0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PScene::PNode * __ptr64,char const * __ptr64>` | 1 |
| `005E00A0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PLightType const * __ptr64,8> >` | 0 | `006B5460` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PScene::PNode const * __ptr64>` | 1 |
| `005E0100` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PShadowCasterType const * __ptr64,8> >` | 0 | `006B54E0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PWorldMatrix const * __ptr64>` | 1 |
| `005E0160` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PContextVariantFoldingTable,4> >` | 0 | `006B5560` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,void>` | 1 |
| `005E01C0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PMaterialSwitch,8> >` | 0 | `006B5590` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PScene::PNode,void,class Phyre::PScene::PNode & __ptr64>` | 1 |
| `005E0220` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PMatrix4,4> >` | 0 | `006B55E0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PScene::PNode,void,class Phyre::PMatrix4 const & __ptr64>` | 1 |
| `005E0280` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PMeshInstanceSegmentContext,8> >` | 0 | `006B5630` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PScene::PNode,void,class Phyre::PWorldMatrix * __ptr64>` | 1 |
| `005E02E0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PNodeContext,8> >` | 0 | `006B5680` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PScene::PNode,void,char const * __ptr64>` | 1 |
| `005E0340` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PSceneRenderPass,8> >` | 0 | `006B5710` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PMatrix4 const & __ptr64>` | 4 |
| `005E03A0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PShader,8> >` | 0 | `006B5790` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PString const & __ptr64>` | 4 |
| `005E0400` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocation,2> >` | 0 | `006B5810` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PScene::PNode * __ptr64,char const * __ptr64>` | 4 |
| `005E0460` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType,2> >` | 0 | `006B58A0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PScene::PNode const * __ptr64>` | 4 |
| `005E04C0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer,4> >` | 0 | `006B5920` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PWorldMatrix const * __ptr64>` | 4 |
| `005E0520` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PShaderParameterDefinition,8> >` | 0 | `006B59A0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,void>` | 4 |
| `005E0580` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PShaderPass,8> >` | 0 | `006B5A20` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PScene::PNode,void,class Phyre::PScene::PNode & __ptr64>` | 4 |
| `005E05E0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PShaderPassInfo,8> >` | 0 | `006B5AA0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PScene::PNode,void,class Phyre::PMatrix4 const & __ptr64>` | 4 |
| `005E0640` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PShaderStreamDefinition,8> >` | 0 | `006B5B30` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PScene::PNode,void,class Phyre::PWorldMatrix * __ptr64>` | 4 |
| `005E06A0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PString,8> >` | 0 | `006B5BC0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PScene::PNode,void,char const * __ptr64>` | 4 |
| `005E0700` | `PClassDataMemberArrayDynamic<class Phyre::PSharray<unsigned int> >` | 0 | `006B6170` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PMatrix4 const & __ptr64>` | 2 |
| `005E0760` | `PClassDataMemberArrayDynamic<class Phyre::PSharray<class Phyre::PRendering::PMeshInstanceSegmentStreamBinding const * __ptr64> >` | 0 | `006B6200` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PString const & __ptr64>` | 2 |
| `005E07C0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PContextSwitch * __ptr64>` | 0 | `006B6270` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PScene::PNode * __ptr64,char const * __ptr64>` | 2 |
| `005E0820` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PEffectVariant * __ptr64>` | 0 | `006B62F0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PScene::PNode const * __ptr64>` | 2 |
| `005E0880` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PLightType * __ptr64>` | 0 | `006B6360` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PScene::PNode,class Phyre::PWorldMatrix const * __ptr64>` | 2 |
| `005E08E0` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierNetworkInstance * __ptr64>` | 0 | `006B6780` | `PAnnotation` | 0 |
| `005E0940` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PSceneRenderPass * __ptr64>` | 0 | `006B68D0` | `PNamedSemanticDescriptor` | 7 |
| `005E09A0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShadowCasterType * __ptr64>` | 0 | `006B69D0` | `PClassDescriptorForType<class Phyre::PRendering::PMeshSegmentContext>` | 7 |
| `005E0A00` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PContextVariantFoldingTable>` | 0 | `006B6A50` | `PClassDescriptorAbstract<class Phyre::PRendering::PMeshSegmentContext>` | 7 |
| `005E0A60` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PMaterialSwitch>` | 0 | `006B6AB0` | `PClassDescriptorConcrete<class Phyre::PRendering::PMeshSegmentContext>` | 10 |
| `005E0AC0` | `PClassDataMemberPhyreArray<class Phyre::PMatrix4>` | 0 | `006B6AD0` | `PClassDescriptorConcrete<class Phyre::PRendering::PMeshSegmentContext>` | 3 |
| `005E0B20` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PMeshInstanceSegmentContext>` | 0 | `006B6B00` | `PClassDescriptorConcrete<class Phyre::PRendering::PMeshSegmentContext>` | 7 |
| `005E0B80` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PNodeContext>` | 0 | `006B8670` | `PNamedSemanticDescriptorForDynamicType<class Phyre::PRendering::PContextSwitch>` | 7 |
| `005E0BE0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PSceneRenderPass>` | 0 | `006B86D0` | `PRendering::PContextSwitch` | 0 |
| `005E0C40` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShader>` | 0 | `006B8710` | `PRendering::PContextSwitchInstancing` | 0 |
| `005E0CA0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocation>` | 0 | `006B8750` | `PRendering::PContextSwitchLODBlend` | 0 |
| `005E0D00` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType>` | 0 | `006B8790` | `PRendering::PContextSwitchLights` | 0 |
| `005E0D60` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer>` | 0 | `006B87D0` | `PRendering::PContextSwitchLowResParticles` | 0 |
| `005E0DC0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterDefinition>` | 0 | `006B8810` | `PRendering::PContextSwitchShader16BitIndices` | 0 |
| `005E0E20` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderPass>` | 0 | `006B8850` | `PRendering::PContextSwitchShaderLODLevel` | 0 |
| `005E0E80` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderPassInfo>` | 0 | `006B8890` | `PRendering::PContextSwitchShaderOrthoCamera` | 0 |
| `005E0EE0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderStreamDefinition>` | 0 | `006B88D0` | `PRendering::PContextSwitchShaderSkinned` | 0 |
| `005E0F40` | `PClassDataMemberPhyreArray<class Phyre::PString>` | 0 | `006B8F70` | `PNamedSemanticDescriptorForDynamicType<class Phyre::PRendering::PContextSwitch>` | 10 |
| `005E0FA0` | `PClassDataMemberPhyreSharray<unsigned int>` | 0 | `006B9070` | `PRendering::PContextSwitchInstancing` | 2 |
| `005E1000` | `PClassDataMemberPhyreSharray<class Phyre::PRendering::PMeshInstanceSegmentStreamBinding * __ptr64>` | 0 | `006B90A0` | `PRendering::PContextSwitchLODBlend` | 2 |
| `005E1060` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PEffectVariant * __ptr64,8> >` | 7 | `006B9120` | `PRendering::PContextSwitchLights` | 2 |
| `005E10C0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkInstance * __ptr64,8> >` | 7 | `006B93A0` | `PRendering::PContextSwitchShader16BitIndices` | 2 |
| `005E1120` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PSceneRenderPass * __ptr64,8> >` | 7 | `006B93D0` | `PRendering::PContextSwitchShaderLODLevel` | 2 |
| `005E1180` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PContextSwitch const * __ptr64,8> >` | 7 | `006B9410` | `PRendering::PContextSwitchShaderOrthoCamera` | 2 |
| `005E11E0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PLightType const * __ptr64,8> >` | 7 | `006B9450` | `PRendering::PContextSwitchShaderSkinned` | 2 |
| `005E1240` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PShadowCasterType const * __ptr64,8> >` | 7 | `006B94B0` | `PNamedSemanticDescriptorForDynamicType<class Phyre::PRendering::PContextSwitch>` | 9 |
| `005E12A0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PContextVariantFoldingTable,4> >` | 7 | `006B9630` | `PRendering::PContextSwitchLights` | 3 |
| `005E1300` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PMaterialSwitch,8> >` | 7 | `006B9A20` | `PRendering::PContextSwitchShaderLODLevel` | 3 |
| `005E1360` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PMatrix4,4> >` | 7 | `006B9CF0` | `PRendering::PContextSwitchLights` | 1 |
| `005E13C0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PMeshInstanceSegmentContext,8> >` | 7 | `006BA3A0` | `PRendering::PContextSwitchShaderLODLevel` | 1 |
| `005E1420` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PNodeContext,8> >` | 7 | `006BA9B0` | `PProfiling::PProcessorProfileTimelineCpu` | 0 |
| `005E1480` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PSceneRenderPass,8> >` | 7 | `006BAA40` | `PThreadPoolWorkStealing` | 1 |
| `005E14E0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PShader,8> >` | 7 | `006BAAD0` | `PThreadPoolWorkStealing` | 5 |
| `005E1540` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocation,2> >` | 7 | `006BAB40` | `PThreadPoolWorkStealing` | 2 |
| `005E15A0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType,2> >` | 7 | `006BADF0` | `PThreadPoolWorkStealing` | 6 |
| `005E1600` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer,4> >` | 7 | `006BAED0` | `PThreadPoolWorkStealing` | 3 |
| `005E1660` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PShaderParameterDefinition,8> >` | 7 | `006BB000` | `PThreadPoolWorkStealing` | 4 |
| `005E16C0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PShaderPass,8> >` | 7 | `006BB070` | `PThreadPoolWorkStealing` | 7 |
| `005E1720` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PShaderPassInfo,8> >` | 7 | `006BB110` | `PThreadPoolWorkStealing` | 0 |
| `005E1780` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PShaderStreamDefinition,8> >` | 7 | `006BB2F0` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMesh>` | 7 |
| `005E17E0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PString,8> >` | 7 | `006BB350` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMesh>` | 10 |
| `005E1840` | `PClassDescriptorAbstract<class Phyre::PSharray<unsigned int> >` | 7 | `006BB3C0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMesh>` | 3 |
| `005E18A0` | `PClassDescriptorAbstract<class Phyre::PSharray<class Phyre::PRendering::PMeshInstanceSegmentStreamBinding const * __ptr64> >` | 7 | `006BB3F0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMesh>` | 7 |
| `005E1900` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PEffectVariant * __ptr64,8> >` | 7 | `006BB4E0` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment>` | 7 |
| `005E1960` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkInstance * __ptr64,8> >` | 7 | `006BB570` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment>` | 7 |
| `005E19C0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PSceneRenderPass * __ptr64,8> >` | 7 | `006BB5D0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment>` | 3 |
| `005E1A20` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PContextSwitch const * __ptr64,8> >` | 7 | `006BB600` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment>` | 7 |
| `005E1A80` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PLightType const * __ptr64,8> >` | 7 | `006BB660` | `PDynamicGeometry::PModifierNetworkDynamicMesh` | 1 |
| `005E1AE0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShadowCasterType const * __ptr64,8> >` | 7 | `006BB6D0` | `PDynamicGeometry::PModifierNetworkDynamicMesh` | 6 |
| `005E1B40` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PContextVariantFoldingTable,4> >` | 7 | `006BB7D0` | `PDynamicGeometry::PModifierNetworkDynamicMesh` | 5 |
| `005E1BA0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PMaterialSwitch,8> >` | 7 | `006BB8D0` | `PDynamicGeometry::PModifierNetworkDynamicMesh` | 7 |
| `005E1C00` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PMatrix4,4> >` | 7 | `006BB930` | `PDynamicGeometry::PModifierNetworkDynamicMesh` | 0 |
| `005E1C60` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PMeshInstanceSegmentContext,8> >` | 7 | `006BBA40` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMesh>` | 7 |
| `005E1CC0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PNodeContext,8> >` | 7 | `006BBF20` | `PClassDataMemberArrayDynamic<class Phyre::PArray<unsigned char const * __ptr64,8> >` | 0 |
| `005E1D20` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PSceneRenderPass,8> >` | 7 | `006BBF80` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment,8> >` | 0 |
| `005E1D80` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShader,8> >` | 7 | `006BBFE0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PDynamicGeometry::PRenderStream,8> >` | 0 |
| `005E1DE0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocation,2> >` | 7 | `006BC040` | `PClassDataMemberPhyreArray<unsigned char * __ptr64>` | 0 |
| `005E1E40` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType,2> >` | 7 | `006BC0A0` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment>` | 0 |
| `005E1EA0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer,4> >` | 7 | `006BC100` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PRenderStream>` | 0 |
| `005E1F00` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderParameterDefinition,8> >` | 7 | `006BC160` | `PClassDescriptorAbstract<class Phyre::PArray<unsigned char const * __ptr64,8> >` | 7 |
| `005E1F60` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderPass,8> >` | 7 | `006BC1C0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment,8> >` | 7 |
| `005E1FC0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderPassInfo,8> >` | 7 | `006BC220` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PDynamicGeometry::PRenderStream,8> >` | 7 |
| `005E2020` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderStreamDefinition,8> >` | 7 | `006BC280` | `PClassDescriptorConcrete<class Phyre::PArray<unsigned char const * __ptr64,8> >` | 7 |
| `005E2080` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PString,8> >` | 7 | `006BC2E0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment,8> >` | 7 |
| `005E20E0` | `PClassDescriptorConcrete<class Phyre::PSharray<unsigned int> >` | 7 | `006BC340` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PRenderStream,8> >` | 7 |
| `005E2140` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PRendering::PMeshInstanceSegmentStreamBinding const * __ptr64> >` | 7 | `006BC3A0` | `PClassDescriptorForType<class Phyre::PArray<unsigned char const * __ptr64,8> >` | 7 |
| `005E21A0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PEffectVariant * __ptr64,8> >` | 7 | `006BC400` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment,8> >` | 7 |
| `005E2200` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkInstance * __ptr64,8> >` | 7 | `006BC460` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PDynamicGeometry::PRenderStream,8> >` | 7 |
| `005E2260` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PSceneRenderPass * __ptr64,8> >` | 7 | `006BE220` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment>` | 9 |
| `005E22C0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PContextSwitch const * __ptr64,8> >` | 7 | `006BE230` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PRenderStream>` | 9 |
| `005E2320` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PLightType const * __ptr64,8> >` | 7 | `006BE2C0` | `PClassDescriptorConcrete<class Phyre::PArray<unsigned char const * __ptr64,8> >` | 3 |
| `005E2380` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PShadowCasterType const * __ptr64,8> >` | 7 | `006BE330` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment,8> >` | 3 |
| `005E23E0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PContextVariantFoldingTable,4> >` | 7 | `006BE3A0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PRenderStream,8> >` | 3 |
| `005E2440` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PMaterialSwitch,8> >` | 7 | `006BE6E0` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment>` | 5 |
| `005E24A0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PMatrix4,4> >` | 7 | `006BE700` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PRenderStream>` | 5 |
| `005E2500` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PMeshInstanceSegmentContext,8> >` | 7 | `006BE8A0` | `PClassDescriptorForType<class Phyre::PRendering::PLight>` | 7 |
| `005E2560` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PNodeContext,8> >` | 7 | `006BE930` | `PClassDescriptorAbstract<class Phyre::PRendering::PLight>` | 7 |
| `005E25C0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PSceneRenderPass,8> >` | 7 | `006BE990` | `PClassDescriptorConcrete<class Phyre::PRendering::PLight>` | 10 |
| `005E2620` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PShader,8> >` | 7 | `006BE9F0` | `PClassDescriptorConcrete<class Phyre::PRendering::PLight>` | 3 |
| `005E2680` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocation,2> >` | 7 | `006BEA60` | `PClassDescriptorConcrete<class Phyre::PRendering::PLight>` | 7 |
| `005E26E0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType,2> >` | 7 | `006BECC0` | `PNamedSemanticDescriptorForType<class Phyre::PRendering::PLightType>` | 7 |
| `005E2740` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer,4> >` | 7 | `006BED20` | `PRendering::PLightType` | 0 |
| `005E27A0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PShaderParameterDefinition,8> >` | 7 | `006BFD60` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PLight,class Phyre::PWorldMatrix * __ptr64>` | 1 |
| `005E2800` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PShaderPass,8> >` | 7 | `006BFDE0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,float>` | 1 |
| `005E2860` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PShaderPassInfo,8> >` | 7 | `006BFE40` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,float,float>` | 1 |
| `005E28C0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PShaderStreamDefinition,8> >` | 7 | `006BFED0` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,float,float,float,float>` | 1 |
| `005E2920` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PString,8> >` | 7 | `006BFFC0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,class Phyre::PWorldMatrix * __ptr64>` | 1 |
| `005E2980` | `PClassDescriptorForType<class Phyre::PSharray<unsigned int> >` | 7 | `006C0010` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,class sce::Vectormath::Scalar::Aos::Vector4 const * __ptr64>` | 1 |
| `005E29E0` | `PClassDescriptorForType<class Phyre::PSharray<class Phyre::PRendering::PMeshInstanceSegmentStreamBinding const * __ptr64> >` | 7 | `006C0060` | `PNamedSemanticDescriptorForType<class Phyre::PRendering::PLightType>` | 10 |
| `005E2A40` | `PNamedSemanticDescriptorForDynamicType<class Phyre::PRendering::PSceneRenderPassType>` | 7 | `006C0140` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PLight,class Phyre::PWorldMatrix * __ptr64>` | 4 |
| `005E2AA0` | `PRendering::PDynamicMeshInstance` | 0 | `006C01C0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,float>` | 4 |
| `005E2AF0` | `PRendering::PModifierNetworkDynamicMeshInstance` | 0 | `006C0250` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,float,float>` | 4 |
| `005E2B80` | `PProfiling::PProcessorProfileTimelineBase` | 0 | `006C02F0` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,float,float,float,float>` | 4 |
| `005E2BC0` | `PRendering::PRenderer` | 0 | `006C03A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,class Phyre::PWorldMatrix * __ptr64>` | 4 |
| `005E2C40` | `PRendering::PRendererBase` | 0 | `006C0430` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,class sce::Vectormath::Scalar::Aos::Vector4 const * __ptr64>` | 4 |
| `005E2C90` | `PRendering::PRendererForJobs` | 0 | `006C04C0` | `PNamedSemanticDescriptorForType<class Phyre::PRendering::PLightType>` | 9 |
| `005FF750` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMaterial,void,char const * __ptr64,float>` | 1 | `006C0610` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,float>` | 2 |
| `005FF7D0` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMaterial,void,char const * __ptr64,class sce::Vectormath::Scalar::Aos::Matrix4>` | 1 | `006C0640` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,float,float>` | 2 |
| `005FF8F0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PGeometry::PMaterialSet & __ptr64>` | 1 | `006C0680` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PRendering::PLight,void,float,float,float,float>` | 2 |
| `005FF940` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PGeometry::PMesh & __ptr64>` | 1 | `006C0770` | `PClassDescriptorForType<class Phyre::PRendering::PShadowCaster>` | 7 |
| `005FF990` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PMatrix4 const & __ptr64,unsigned int>` | 1 | `006C0800` | `PClassDescriptorAbstract<class Phyre::PRendering::PShadowCaster>` | 7 |
| `005FFA10` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PRendering::PMeshInstanceBounds * __ptr64>` | 1 | `006C0860` | `PClassDescriptorConcrete<class Phyre::PRendering::PShadowCaster>` | 10 |
| `005FFA90` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PWorldMatrix * __ptr64>` | 1 | `006C0890` | `PClassDescriptorConcrete<class Phyre::PRendering::PShadowCaster>` | 3 |
| `005FFB10` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,void,unsigned int,class Phyre::PMatrix4 const & __ptr64>` | 1 | `006C08A0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShadowCaster>` | 7 |
| `005FFB90` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,void,class Phyre::PRendering::PMeshInstanceBounds * __ptr64>` | 1 | `006C0990` | `PClassDescriptorForType<class Phyre::PRendering::PShadowCaster::PShadowSplit>` | 7 |
| `005FFBE0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,void,class sce::Vectormath::Scalar::Aos::Vector4 const * __ptr64>` | 1 | `006C0A20` | `PClassDescriptorAbstract<class Phyre::PRendering::PShadowCaster::PShadowSplit>` | 7 |
| `005FFC30` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PSamplerStateBase,enum Phyre::PResult,float>` | 1 | `006C0A80` | `PClassDescriptorConcrete<class Phyre::PRendering::PShadowCaster::PShadowSplit>` | 10 |
| `005FFD50` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PSamplerStateBase,enum Phyre::PResult,bool>` | 1 | `006C0AC0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShadowCaster::PShadowSplit>` | 3 |
| `005FFDE0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PTextureCommonBase,char const * __ptr64>` | 1 | `006C0AF0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShadowCaster::PShadowSplit>` | 7 |
| `00600E30` | `PRendering::PRendererForJobs` | 2 | `006C12C0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PShadowCaster::PShadowSplit,8> >` | 0 |
| `00603770` | `PNamedSemanticDescriptorForDynamicType<class Phyre::PRendering::PSceneRenderPassType>` | 10 | `006C1320` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShadowCaster::PShadowSplit>` | 0 |
| `00603850` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMaterial,void,char const * __ptr64,int>` | 4 | `006C1380` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PShadowCaster::PShadowSplit,8> >` | 7 |
| `006038F0` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMaterial,void,char const * __ptr64,unsigned int>` | 4 | `006C13E0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShadowCaster::PShadowSplit,8> >` | 7 |
| `00603990` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMaterial,void,char const * __ptr64,float>` | 4 | `006C1440` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PShadowCaster::PShadowSplit,8> >` | 7 |
| `00603A30` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMaterial,void,char const * __ptr64,class sce::Vectormath::Scalar::Aos::Matrix4>` | 4 | `006C14A0` | `PNamedSemanticDescriptorForType<class Phyre::PRendering::PShadowCasterType>` | 7 |
| `00603AD0` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMaterial,void,char const * __ptr64,class sce::Vectormath::Scalar::Aos::Point3>` | 4 | `006C1500` | `PRendering::PShadowCasterType` | 0 |
| `00603B70` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMaterial,void,char const * __ptr64,class sce::Vectormath::Scalar::Aos::Vector3>` | 4 | `006C24C0` | `PNamedSemanticDescriptorForType<class Phyre::PRendering::PShadowCasterType>` | 10 |
| `00603C10` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMaterial,void,char const * __ptr64,class sce::Vectormath::Scalar::Aos::Vector4>` | 4 | `006C25A0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShadowCaster::PShadowSplit>` | 9 |
| `00603CB0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PGeometry::PMaterialSet & __ptr64>` | 4 | `006C25D0` | `PNamedSemanticDescriptorForType<class Phyre::PRendering::PShadowCasterType>` | 9 |
| `00603D30` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PGeometry::PMesh & __ptr64>` | 4 | `006C2630` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShadowCaster::PShadowSplit,8> >` | 3 |
| `00603DB0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PMatrix4 const & __ptr64,unsigned int>` | 4 | `006C2770` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShadowCaster::PShadowSplit>` | 5 |
| `00603E40` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PRendering::PMeshInstanceBounds * __ptr64>` | 4 | `006C2870` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierNetworkInstanceInput>` | 7 |
| `00603EC0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PWorldMatrix * __ptr64>` | 4 | `006C2900` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierNetworkInstanceInput>` | 7 |
| `00603F40` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,void,unsigned int,class Phyre::PMatrix4 const & __ptr64>` | 4 | `006C2960` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInstanceInput>` | 10 |
| `00603FE0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,void,class Phyre::PRendering::PMeshInstanceBounds * __ptr64>` | 4 | `006C2980` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInstanceInput>` | 3 |
| `00604070` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,void,class sce::Vectormath::Scalar::Aos::Vector4 const * __ptr64>` | 4 | `006C29B0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInstanceInput>` | 7 |
| `00604100` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PSamplerStateBase,enum Phyre::PResult,unsigned int>` | 4 | `006C2AA0` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierNetworkInstancePacketInput>` | 7 |
| `00604190` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PSamplerStateBase,enum Phyre::PResult,float>` | 4 | `006C2B30` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierNetworkInstancePacketInput>` | 7 |
| `00604220` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PSamplerStateBase,enum Phyre::PResult,enum Phyre::PRendering::PSamplerStateBase::PSamplerStateFilterFormatType>` | 4 | `006C2B90` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInstancePacketInput>` | 3 |
| `006042A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PSamplerStateBase,enum Phyre::PResult,enum Phyre::PRendering::PSamplerStateBase::PSamplerStateWrapFormatType>` | 4 | `006C2BB0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInstancePacketInput>` | 7 |
| `00604320` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PSamplerStateBase,enum Phyre::PResult,bool>` | 4 | `006C2CC0` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierNetworkInstance>` | 7 |
| `006043B0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PTextureCommonBase,char const * __ptr64>` | 4 | `006C2D50` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierNetworkInstance>` | 7 |
| `00604430` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PContextSwitch * __ptr64>` | 9 | `006C2DB0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInstance>` | 3 |
| `00604440` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PEffectVariant * __ptr64>` | 9 | `006C2DE0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInstance>` | 7 |
| `00604450` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PLightType * __ptr64>` | 9 | `006C31A0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PBase const * __ptr64,8> >` | 0 |
| `00604460` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierNetworkInstance * __ptr64>` | 9 | `006C3200` | `PClassDataMemberPhyreArray<class Phyre::PBase * __ptr64>` | 0 |
| `00604480` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShadowCasterType * __ptr64>` | 9 | `006C3260` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PBase const * __ptr64,8> >` | 7 |
| `00604490` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PContextVariantFoldingTable>` | 9 | `006C32C0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PBase const * __ptr64,8> >` | 7 |
| `006044A0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PMaterialSwitch>` | 9 | `006C3320` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PBase const * __ptr64,8> >` | 7 |
| `006044B0` | `PClassDataMemberPhyreArray<class Phyre::PMatrix4>` | 9 | `006C4460` | `PClassDataMemberPhyreArray<class Phyre::PBase * __ptr64>` | 9 |
| `006044C0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PMeshInstanceSegmentContext>` | 9 | `006C44B0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PBase const * __ptr64,8> >` | 3 |
| `006044D0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PNodeContext>` | 9 | `006C45F0` | `PDynamicGeometry::PUtilityDynamicGeometry` | 1 |
| `006044E0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShader>` | 9 | `006C4750` | `PDynamicGeometry::PUtilityDynamicGeometry` | 2 |
| `006044F0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocation>` | 9 | `006C4860` | `PLOD::PUtilityLOD` | 1 |
| `00604500` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType>` | 9 | `006C4960` | `PClassDescriptorForType<class Phyre::PLOD::PLODLevel>` | 7 |
| `00604510` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer>` | 9 | `006C4A00` | `PClassDescriptorAbstract<class Phyre::PLOD::PLODLevel>` | 7 |
| `00604520` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterDefinition>` | 9 | `006C4A60` | `PClassDescriptorConcrete<class Phyre::PLOD::PLODLevel>` | 10 |
| `00604530` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderPass>` | 9 | `006C4AC0` | `PClassDescriptorConcrete<class Phyre::PLOD::PLODLevel>` | 3 |
| `00604540` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderPassInfo>` | 9 | `006C4B10` | `PClassDescriptorConcrete<class Phyre::PLOD::PLODLevel>` | 7 |
| `00604550` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderStreamDefinition>` | 9 | `006C4C60` | `PClassDescriptorForType<class Phyre::PLOD::PLODGroup>` | 7 |
| `00604570` | `PClassDataMemberPhyreSharray<class Phyre::PRendering::PMeshInstanceSegmentStreamBinding * __ptr64>` | 9 | `006C4D00` | `PClassDescriptorAbstract<class Phyre::PLOD::PLODGroup>` | 7 |
| `00606980` | `PRendering::PModifierNetworkDynamicMeshInstance` | 1 | `006C4D60` | `PClassDescriptorConcrete<class Phyre::PLOD::PLODGroup>` | 10 |
| `006069C0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PGeometry::PMaterialSet & __ptr64>` | 3 | `006C4D90` | `PClassDescriptorConcrete<class Phyre::PLOD::PLODGroup>` | 3 |
| `006069D0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PGeometry::PMesh & __ptr64>` | 3 | `006C4DC0` | `PClassDescriptorConcrete<class Phyre::PLOD::PLODGroup>` | 7 |
| `006069E0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PRendering::PMeshInstanceBounds * __ptr64>` | 3 | `006C5610` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PLOD::PLODLevel,8> >` | 0 |
| `00606A10` | `PNamedSemanticDescriptorForDynamicType<class Phyre::PRendering::PSceneRenderPassType>` | 9 | `006C5670` | `PClassDataMemberArrayDynamic<class Phyre::PSharray<class Phyre::PRendering::PMeshInstance * __ptr64> >` | 0 |
| `00606CC0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PEffectVariant * __ptr64,8> >` | 3 | `006C56D0` | `PClassDataMemberPhyreArray<class Phyre::PLOD::PLODLevel>` | 0 |
| `00606D30` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkInstance * __ptr64,8> >` | 3 | `006C5730` | `PClassDataMemberPhyreSharray<class Phyre::PRendering::PMeshInstance * __ptr64>` | 0 |
| `00606DA0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PSceneRenderPass * __ptr64,8> >` | 3 | `006C5790` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PLOD::PLODLevel,8> >` | 7 |
| `00606E10` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PContextSwitch const * __ptr64,8> >` | 3 | `006C57F0` | `PClassDescriptorAbstract<class Phyre::PSharray<class Phyre::PRendering::PMeshInstance * __ptr64> >` | 7 |
| `00606E80` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PLightType const * __ptr64,8> >` | 3 | `006C5850` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PLOD::PLODLevel,8> >` | 7 |
| `00606EF0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShadowCasterType const * __ptr64,8> >` | 3 | `006C58B0` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PRendering::PMeshInstance * __ptr64> >` | 7 |
| `00606F60` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PContextVariantFoldingTable,4> >` | 3 | `006C5910` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PLOD::PLODLevel,8> >` | 7 |
| `00606FD0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PMaterialSwitch,8> >` | 3 | `006C5970` | `PClassDescriptorForType<class Phyre::PSharray<class Phyre::PRendering::PMeshInstance * __ptr64> >` | 7 |
| `00607000` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PMatrix4,4> >` | 3 | `006C6543` | `PClassDescriptorForType<class Phyre::PPostProcessing::PDeferredLightingBase>` | 16 |
| `00607070` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PMeshInstanceSegmentContext,8> >` | 3 | `006C7500` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PLOD::PLODGroup,class Phyre::PWorldMatrix * __ptr64>` | 1 |
| `006070A0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PNodeContext,8> >` | 3 | `006C7580` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PLOD::PLODGroup,void,bool>` | 1 |
| `006070D0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PSceneRenderPass,8> >` | 3 | `006C7650` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PLOD::PLODGroup,class Phyre::PWorldMatrix * __ptr64>` | 4 |
| `00607100` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShader,8> >` | 3 | `006C76D0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PLOD::PLODGroup,void,bool>` | 4 |
| `00607130` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocation,2> >` | 3 | `006C7760` | `PClassDataMemberPhyreArray<class Phyre::PLOD::PLODLevel>` | 9 |
| `006071A0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType,2> >` | 3 | `006C7770` | `PClassDataMemberPhyreSharray<class Phyre::PRendering::PMeshInstance * __ptr64>` | 9 |
| `00607210` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer,4> >` | 3 | `006C7860` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PLOD::PLODLevel,8> >` | 3 |
| `00607280` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderParameterDefinition,8> >` | 3 | `006C7890` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PRendering::PMeshInstance * __ptr64> >` | 3 |
| `006072B0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderPass,8> >` | 3 | `006C7AF0` | `PClassDataMemberPhyreArray<class Phyre::PLOD::PLODLevel>` | 5 |
| `006072E0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderPassInfo,8> >` | 3 | `006C7F20` | `PClassDataMemberPhyreArray<class Phyre::PLOD::PLODLevel>` | 8 |
| `00607310` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PShaderStreamDefinition,8> >` | 3 | `006C80C0` | `PClassDescriptorForType<class Phyre::POccluderGeometry::POccluderGeometryInstance>` | 7 |
| `00607340` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PString,8> >` | 3 | `006C8150` | `PClassDescriptorAbstract<class Phyre::POccluderGeometry::POccluderGeometryInstance>` | 7 |
| `00607370` | `PClassDescriptorConcrete<class Phyre::PSharray<unsigned int> >` | 3 | `006C81B0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::POccluderGeometry::POccluderGeometryInstance>` | 10 |
| `006073A0` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PRendering::PMeshInstanceSegmentStreamBinding const * __ptr64> >` | 3 | `006C81F0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::POccluderGeometry::POccluderGeometryInstance>` | 7 |
| `00608A40` | `PRendering::PUtilityRendering` | 1 | `006C8650` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::POccluderGeometry::POccluderGeometryInstance,class Phyre::PWorldMatrix * __ptr64>` | 1 |
| `0060A3D0` | `PRendering::PModifierNetworkDynamicMeshInstance` | 2 | `006C86D0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::POccluderGeometry::POccluderGeometryInstance,class Phyre::PWorldMatrix * __ptr64>` | 4 |
| `0060CD10` | `PRendering::PMaterialSelectorMaterialSet` | 0 | `006CB690` | `PWorldMatrixController` | 1 |
| `0060D790` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PContextVariantFoldingTable>` | 5 | `006CCD60` | `PText::PUtilityText` | 1 |
| `0060D7B0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PMaterialSwitch>` | 5 | `006CCE60` | `PClassDescriptorForType<class Phyre::PGameplay::PScriptableComponent>` | 7 |
| `0060D7D0` | `PClassDataMemberPhyreArray<class Phyre::PMatrix4>` | 5 | `006CCEC0` | `PClassDescriptorAbstract<class Phyre::PGameplay::PScriptableComponent>` | 12 |
| `0060D7F0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PMeshInstanceSegmentContext>` | 5 | `006CCED0` | `PClassDescriptorAbstract<class Phyre::PGameplay::PScriptableComponent>` | 4 |
| `0060D810` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PNodeContext>` | 5 | `006CCEF0` | `PClassDescriptorAbstract<class Phyre::PGameplay::PScriptableComponent>` | 7 |
| `0060D830` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PSceneRenderPass>` | 5 | `006CD330` | `PNamedSemanticDescriptorForDynamicType<class Phyre::PGameplay::PTriggerType>` | 7 |
| `0060D8B0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShader>` | 5 | `006CD5B0` | `PNamedSemanticDescriptorForDynamicType<class Phyre::PGameplay::PTriggerType>` | 10 |
| `0060D930` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocation>` | 5 | `006CD690` | `PNamedSemanticDescriptorForDynamicType<class Phyre::PGameplay::PTriggerType>` | 9 |
| `0060D950` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationType>` | 5 | `006CD740` | `PClassDescriptorForType<class Phyre::PGameplay::PTriggerReceiverTypeCallbackData>` | 7 |
| `0060D970` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer>` | 5 | `006CD7D0` | `PClassDescriptorAbstract<class Phyre::PGameplay::PTriggerReceiverTypeCallbackData>` | 7 |
| `0060D990` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterDefinition>` | 5 | `006CD830` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PGameplay::PTriggerReceiverTypeCallbackData>` | 10 |
| `0060D9B0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderPass>` | 5 | `006CD840` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PGameplay::PTriggerReceiverTypeCallbackData>` | 7 |
| `0060D9D0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderPassInfo>` | 5 | `006CDE10` | `PClassDescriptorForType<class Phyre::PGameplay::PTriggerReceiverComponent>` | 7 |
| `0060D9F0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderStreamDefinition>` | 5 | `006CDEA0` | `PClassDescriptorAbstract<class Phyre::PGameplay::PTriggerReceiverComponent>` | 7 |
| `0060DA10` | `PClassDataMemberPhyreArray<class Phyre::PString>` | 5 | `006CDF00` | `PClassDescriptorConcrete<class Phyre::PGameplay::PTriggerReceiverComponent>` | 10 |
| `0060DA30` | `PClassDataMemberPhyreSharray<unsigned int>` | 5 | `006CDF60` | `PClassDescriptorConcrete<class Phyre::PGameplay::PTriggerReceiverComponent>` | 3 |
| `0060F480` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PMaterialSwitch>` | 8 | `006CDF90` | `PClassDescriptorConcrete<class Phyre::PGameplay::PTriggerReceiverComponent>` | 7 |
| `0060F4B0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PMeshInstanceSegmentContext>` | 8 | `006CE570` | `PThreadPoolImmediate` | 1 |
| `0060F4E0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PNodeContext>` | 8 | `006CE650` | `PThreadPoolImmediate` | 5 |
| `0060F510` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PSceneRenderPass>` | 8 | `006CE670` | `PThreadPoolImmediate` | 2 |
| `0060F550` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShader>` | 8 | `006CE6C0` | `PThreadPoolImmediate` | 3 |
| `0060F590` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderParameterDefinition>` | 8 | `006CE6E0` | `PThreadPoolImmediate` | 4 |
| `0060F5C0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderPass>` | 8 | `006CE710` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetwork>` | 3 |
| `0060F5F0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderPassInfo>` | 8 | `006CE760` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetwork>` | 7 |
| `0060F620` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PShaderStreamDefinition>` | 8 | `006CE7C0` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierInstance>` | 7 |
| `0060F650` | `PClassDataMemberPhyreArray<class Phyre::PString>` | 8 | `006CE840` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierInstance>` | 3 |
| `0060F680` | `PClassDataMemberPhyreSharray<unsigned int>` | 8 | `006CE870` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierInstance>` | 7 |
| `006104E0` | `PRendering::PRenderer` | 1 | `006CE960` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_Buffer>` | 7 |
| `00610630` | `PRendering::PUtilityRendering` | 2 | `006CE9F0` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_Buffer>` | 7 |
| `00610A10` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMaterial,void,char const * __ptr64,float>` | 2 | `006CEA60` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_Buffer>` | 3 |
| `00610A50` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMaterial,void,char const * __ptr64,class sce::Vectormath::Scalar::Aos::Matrix4>` | 2 | `006CEA80` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_Buffer>` | 7 |
| `00610B50` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PGeometry::PMaterialSet & __ptr64>` | 2 | `006CEB70` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PRenderStreamInput>` | 7 |
| `00610BB0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PGeometry::PMesh & __ptr64>` | 2 | `006CEC90` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PRenderStreamInput>` | 7 |
| `00610C10` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PMatrix4 const & __ptr64,unsigned int>` | 2 | `006CECF0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PRenderStreamInput>` | 10 |
| `00610CA0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,class Phyre::PRendering::PMeshInstanceBounds * __ptr64>` | 2 | `006CED00` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PRenderStreamInput>` | 3 |
| `00610D00` | `PInternal::PCallerImplementation::PCallerImplementation2::PMethodCallerConcrete<class Phyre::PRendering::PMeshInstance,void,unsigned int,class Phyre::PMatrix4 const & __ptr64>` | 2 | `006CED20` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket>` | 7 |
| `00610D40` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PSamplerStateBase,enum Phyre::PResult,float>` | 2 | `006CED90` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PRenderStreamInput>` | 7 |
| `00610DD0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PRendering::PSamplerStateBase,enum Phyre::PResult,bool>` | 2 | `006CEDF0` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket>` | 7 |
| `00610E60` | `PClassDescriptorConcrete<class Phyre::PRendering::PSamplerStateD3D11>` | 7 | `006CEE50` | `PClassDescriptorHeader<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket>` | 11 |
| `00611050` | `PClassDescriptorForType<class Phyre::PRendering::PTexture3DD3D11>` | 7 | `006CEF50` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PRenderStream>` | 7 |
| `00611180` | `PClassDescriptorForType<class Phyre::PRendering::PShaderPassStateD3D11>` | 7 | `006CEFC0` | `PClassDescriptorHeader<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket>` | 7 |
| `00611270` | `PClassDescriptorForType<class Phyre::PRendering::PShaderVertexProgramD3D11>` | 7 | `006CF040` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PRenderStream>` | 7 |
| `006112D0` | `PClassDescriptorAbstract<class Phyre::PRendering::PTexture3DD3D11>` | 7 | `006CF0A0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PRenderStream>` | 3 |
| `00611340` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture3DD3D11>` | 10 | `006CF0C0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PRenderStream>` | 7 |
| `006113B0` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture3DD3D11>` | 3 | `006CF1B0` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierNetworkBuffer>` | 7 |
| `006113C0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderPassStateD3D11>` | 7 | `006CF240` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierNetworkBuffer>` | 7 |
| `00611420` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassStateD3D11>` | 10 | `006CF2A0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkBuffer>` | 3 |
| `00611460` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassStateD3D11>` | 3 | `006CF2D0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkBuffer>` | 7 |
| `006114E0` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture3DD3D11>` | 7 | `006CF400` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierAndInputs>` | 7 |
| `00611540` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderVertexProgramD3D11>` | 7 | `006CF490` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierAndInputs>` | 7 |
| `006115A0` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassStateD3D11>` | 7 | `006CF4F0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierAndInputs>` | 10 |
| `00611600` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderVertexProgramD3D11>` | 10 | `006CF510` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierAndInputs>` | 3 |
| `00611610` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderVertexProgramD3D11>` | 7 | `006CF540` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierAndInputs>` | 7 |
| `00611720` | `PClassDescriptorForType<class Phyre::PRendering::PShaderFragmentProgramD3D11>` | 7 | `006CF630` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierCode>` | 7 |
| `00611850` | `PClassDescriptorForType<class Phyre::PRendering::PShaderPassD3D11>` | 7 | `006CF6C0` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierCode>` | 7 |
| `006118B0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderFragmentProgramD3D11>` | 7 | `006CF720` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierCode>` | 3 |
| `00611950` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderFragmentProgramD3D11>` | 7 | `006CF750` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierCode>` | 7 |
| `006119B0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderPassD3D11>` | 7 | `006CF860` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierNetwork>` | 7 |
| `00611A10` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassD3D11>` | 10 | `006CF980` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierInstance>` | 7 |
| `00611A40` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassD3D11>` | 3 | `006CF9F0` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PModifierNetwork>` | 7 |
| `00611A70` | `PClassDescriptorConcrete<class Phyre::PRendering::PShaderPassD3D11>` | 7 | `006CFA50` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PModifierNetwork>` | 10 |
| `00611BD0` | `PClassDescriptorForType<class Phyre::PRendering::PConstantBufferD3D11>` | 7 | `006D0580` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierAndInputs,8> >` | 0 |
| `00611D00` | `PClassDescriptorAbstract<class Phyre::PRendering::PConstantBufferD3D11>` | 7 | `006D05E0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkBuffer,8> >` | 0 |
| `00611D60` | `PClassDescriptorConcrete<class Phyre::PRendering::PConstantBufferD3D11>` | 10 | `006D0640` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PDynamicGeometry::PRenderStreamInput,4> >` | 0 |
| `00611DD0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderGeometryProgramD3D11>` | 7 | `006D06A0` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierAndInputs>` | 0 |
| `00611E30` | `PClassDescriptorConcrete<class Phyre::PRendering::PConstantBufferD3D11>` | 3 | `006D0700` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierNetworkBuffer>` | 0 |
| `00611E40` | `PClassDescriptorConcrete<class Phyre::PRendering::PConstantBufferD3D11>` | 7 | `006D0760` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PRenderStreamInput>` | 0 |
| `00611EC0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderGeometryProgramD3D11>` | 7 | `006D07C0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierAndInputs,8> >` | 7 |
| `00611F20` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderGeometryProgramD3D11>` | 7 | `006D0820` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkBuffer,8> >` | 7 |
| `00612130` | `PClassDescriptorForType<class Phyre::PRendering::PTexture2DD3D11>` | 7 | `006D0880` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PDynamicGeometry::PRenderStreamInput,4> >` | 7 |
| `00612190` | `PClassDescriptorForType<class Phyre::PRendering::PShaderComputeProgramD3D11>` | 7 | `006D08E0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierAndInputs,8> >` | 7 |
| `00612340` | `PClassDescriptorAbstract<class Phyre::PRendering::PTexture2DD3D11>` | 7 | `006D0940` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkBuffer,8> >` | 7 |
| `006123F0` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture2DD3D11>` | 10 | `006D09A0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PRenderStreamInput,4> >` | 7 |
| `00612440` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture2DD3D11>` | 3 | `006D0A00` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierAndInputs,8> >` | 7 |
| `00612490` | `PClassDescriptorForType<class Phyre::PRendering::PRenderTargetD3D11>` | 7 | `006D0A60` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkBuffer,8> >` | 7 |
| `006124F0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderComputeProgramD3D11>` | 7 | `006D0AC0` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PDynamicGeometry::PRenderStreamInput,4> >` | 7 |
| `00612550` | `PClassDescriptorAbstract<class Phyre::PRendering::PRenderTargetD3D11>` | 12 | `006D4E90` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierAndInputs>` | 9 |
| `00612570` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderComputeProgramD3D11>` | 10 | `006D4EA0` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierNetworkBuffer>` | 9 |
| `00612580` | `PClassDescriptorConcrete<class Phyre::PRendering::PTexture2DD3D11>` | 7 | `006D4EB0` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PRenderStreamInput>` | 9 |
| `006125E0` | `PClassDescriptorForType<class Phyre::PRendering::PStructuredBufferD3D11>` | 7 | `006D5010` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierAndInputs,8> >` | 3 |
| `00612660` | `PClassDescriptorAbstract<class Phyre::PRendering::PRenderTargetD3D11>` | 4 | `006D5040` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PModifierNetworkBuffer,8> >` | 3 |
| `00612680` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderComputeProgramD3D11>` | 7 | `006D50B0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PDynamicGeometry::PRenderStreamInput,4> >` | 3 |
| `00612700` | `PClassDescriptorAbstract<class Phyre::PRendering::PRenderTargetD3D11>` | 7 | `006D5610` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierAndInputs>` | 5 |
| `00612760` | `PClassDescriptorAbstract<class Phyre::PRendering::PStructuredBufferD3D11>` | 7 | `006D5630` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierNetworkBuffer>` | 5 |
| `006127C0` | `PClassDescriptorConcrete<class Phyre::PRendering::PStructuredBufferD3D11>` | 10 | `006D5650` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PRenderStreamInput>` | 5 |
| `00612820` | `PClassDescriptorConcrete<class Phyre::PRendering::PStructuredBufferD3D11>` | 3 | `006D56F0` | `PClassDataMemberPhyreArray<class Phyre::PDynamicGeometry::PModifierAndInputs>` | 8 |
| `00612830` | `PClassDescriptorConcrete<class Phyre::PRendering::PStructuredBufferD3D11>` | 7 | `006D59F0` | `PNamedSemanticDescriptorForType<class Phyre::PDynamicGeometry::PModifier>` | 7 |
| `00612950` | `PClassDescriptorForType<class Phyre::PRendering::PStreamInputDescD3D11>` | 7 | `006D6FF0` | `PNamedSemanticDescriptorForType<class Phyre::PDynamicGeometry::PModifier>` | 10 |
| `006129E0` | `PClassDescriptorAbstract<class Phyre::PRendering::PStreamInputDescD3D11>` | 7 | `006D70D0` | `PNamedSemanticDescriptorForType<class Phyre::PDynamicGeometry::PModifier>` | 9 |
| `00612A40` | `PClassDescriptorConcrete<class Phyre::PRendering::PStreamInputDescD3D11>` | 10 | `006D7200` | `PClassDescriptorForType<class Phyre::PDynamicGeometry::PMorphModifierWeightsUserDataObject>` | 7 |
| `00612A60` | `PClassDescriptorConcrete<class Phyre::PRendering::PStreamInputDescD3D11>` | 3 | `006D7290` | `PClassDescriptorAbstract<class Phyre::PDynamicGeometry::PMorphModifierWeightsUserDataObject>` | 7 |
| `00612AC0` | `PClassDescriptorConcrete<class Phyre::PRendering::PStreamInputDescD3D11>` | 7 | `006D72F0` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PMorphModifierWeightsUserDataObject>` | 3 |
| `00612C20` | `PClassDescriptorForType<class Phyre::PRendering::PTextureCubeMapD3D11>` | 7 | `006D7320` | `PClassDescriptorConcrete<class Phyre::PDynamicGeometry::PMorphModifierWeightsUserDataObject>` | 7 |
| `00612CA0` | `PClassDescriptorAbstract<class Phyre::PRendering::PTextureCubeMapD3D11>` | 7 | `006D95A0` | `PNamedSemanticDescriptorForType<class Phyre::PLOD::PLODMetricType>` | 7 |
| `00612D00` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCubeMapD3D11>` | 10 | `006D9600` | `PLOD::PLODMetricType` | 0 |
| `00612D30` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCubeMapD3D11>` | 3 | `006D9780` | `PNamedSemanticDescriptorForType<class Phyre::PLOD::PLODMetricType>` | 10 |
| `00612D40` | `PClassDescriptorConcrete<class Phyre::PRendering::PTextureCubeMapD3D11>` | 7 | `006D9860` | `PNamedSemanticDescriptorForType<class Phyre::PLOD::PLODMetricType>` | 9 |
| `00612E70` | `PClassDescriptorForType<class Phyre::PRendering::PStreamInputLayoutD3D11>` | 7 | `006D9990` | `PNamedSemanticDescriptorForType<class Phyre::PLOD::PLODBlendType>` | 7 |
| `00612F00` | `PClassDescriptorAbstract<class Phyre::PRendering::PStreamInputLayoutD3D11>` | 7 | `006D99F0` | `PLOD::PLODBlendType` | 0 |
| `00613010` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PStreamInputLayoutD3D11>` | 7 | `006D9B70` | `PNamedSemanticDescriptorForType<class Phyre::PLOD::PLODBlendType>` | 10 |
| `00613070` | `PClassDescriptorForType<class Phyre::PRendering::PIndirectArgsBufferD3D11>` | 7 | `006D9C50` | `PNamedSemanticDescriptorForType<class Phyre::PLOD::PLODBlendType>` | 9 |
| `00613110` | `PClassDescriptorAbstract<class Phyre::PRendering::PIndirectArgsBufferD3D11>` | 7 | `006D9D40` | `PClassDescriptorForType<class Phyre::POccluderGeometry::POccluderGeometryObject>` | 7 |
| `00613170` | `PClassDescriptorConcrete<class Phyre::PRendering::PIndirectArgsBufferD3D11>` | 10 | `006D9DD0` | `PClassDescriptorAbstract<class Phyre::POccluderGeometry::POccluderGeometryObject>` | 7 |
| `006131C0` | `PClassDescriptorConcrete<class Phyre::PRendering::PIndirectArgsBufferD3D11>` | 3 | `006D9E30` | `PClassDescriptorHeader<class Phyre::POccluderGeometry::POccluderGeometryObject>` | 11 |
| `006131D0` | `PClassDescriptorConcrete<class Phyre::PRendering::PIndirectArgsBufferD3D11>` | 7 | `006D9E80` | `PClassDescriptorHeader<class Phyre::POccluderGeometry::POccluderGeometryObject>` | 10 |
| `006133C0` | `PClassDescriptorForType<class Phyre::PRendering::PShaderProgramD3D11>` | 7 | `006D9EA0` | `PClassDescriptorHeader<class Phyre::POccluderGeometry::POccluderGeometryObject>` | 7 |
| `00613430` | `PClassDescriptorForType<class Phyre::PRendering::PSamplerStateD3D11>` | 7 | `00755F6D` | `PClassDataMemberArrayDynamic<class Phyre::PSharray<class Phyre::PAnimation::PAnimationClip * __ptr64> >` | 11 |
| `006134B0` | `PClassDescriptorAbstract<class Phyre::PRendering::PShaderProgramD3D11>` | 7 | `007912C0` | `PClassDescriptorForType<class Phyre::PFramework::PDebugUtils>` | 7 |
| `00613530` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderProgramD3D11>` | 10 | `00791350` | `PClassDescriptorAbstract<class Phyre::PFramework::PDebugUtils>` | 7 |
| `00613580` | `PClassDescriptorAbstract<class Phyre::PRendering::PSamplerStateD3D11>` | 7 | `007913B0` | `PClassDescriptorConcrete<class Phyre::PFramework::PDebugUtils>` | 10 |
| `006135E0` | `PClassDescriptorConcrete<class Phyre::PRendering::PSamplerStateD3D11>` | 10 | `007913D0` | `PClassDescriptorConcrete<class Phyre::PFramework::PDebugUtils>` | 3 |
| `00613620` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PRendering::PShaderProgramD3D11>` | 7 | `00791410` | `PClassDescriptorConcrete<class Phyre::PFramework::PDebugUtils>` | 7 |
| `00613680` | `PClassDescriptorConcrete<class Phyre::PRendering::PSamplerStateD3D11>` | 3 | `00791520` | `PClassDescriptorForType<class Phyre::PFramework::PApplication>` | 7 |
| `00616F30` | `PClassDataMemberArrayDynamic<class Phyre::PArray<unsigned char,1> >` | 0 | `00791580` | `PClassDescriptorAbstract<class Phyre::PFramework::PApplication>` | 12 |
| `00616F90` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PRendering::PStreamInputDescD3D11,8> >` | 0 | `00791590` | `PClassDescriptorAbstract<class Phyre::PFramework::PApplication>` | 4 |
| `00616FF0` | `PClassDataMemberPhyreArray<unsigned char>` | 0 | `007915B0` | `PClassDescriptorAbstract<class Phyre::PFramework::PApplication>` | 7 |
| `00617050` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PStreamInputDescD3D11>` | 0 | `007916C0` | `PClassDescriptorForType<class Phyre::PFramework::PApplicationViewport>` | 7 |
| `006170B0` | `PClassDescriptorAbstract<class Phyre::PArray<unsigned char,1> >` | 7 | `00791750` | `PClassDescriptorAbstract<class Phyre::PFramework::PApplicationViewport>` | 7 |
| `00617110` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PRendering::PStreamInputDescD3D11,8> >` | 7 | `007917B0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PFramework::PApplicationViewport>` | 10 |
| `00617170` | `PClassDescriptorConcrete<class Phyre::PArray<unsigned char,1> >` | 7 | `007917C0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PFramework::PApplicationViewport>` | 7 |
| `006171D0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PStreamInputDescD3D11,8> >` | 7 | `007918B0` | `PClassDescriptorForType<class Phyre::PFramework::PInputMapper>` | 7 |
| `00617230` | `PClassDescriptorForType<struct CD3D11_BLEND_DESC>` | 7 | `00791940` | `PClassDescriptorAbstract<class Phyre::PFramework::PInputMapper>` | 7 |
| `00617290` | `PClassDescriptorForType<struct CD3D11_DEPTH_STENCIL_DESC>` | 7 | `007919A0` | `PClassDescriptorConcrete<class Phyre::PFramework::PInputMapper>` | 10 |
| `006172F0` | `PClassDescriptorForType<struct CD3D11_RASTERIZER_DESC>` | 7 | `007919D0` | `PClassDescriptorConcrete<class Phyre::PFramework::PInputMapper>` | 3 |
| `00617350` | `PClassDescriptorForType<struct D3D11_DEPTH_STENCILOP_DESC>` | 7 | `00791A00` | `PClassDescriptorConcrete<class Phyre::PFramework::PInputMapper>` | 7 |
| `006173B0` | `PClassDescriptorForType<struct D3D11_RENDER_TARGET_BLEND_DESC>` | 7 | `00793EB0` | `PFramework::PApplication` | 0 |
| `00617410` | `PClassDescriptorForType<class Phyre::PArray<unsigned char,1> >` | 7 | `00793F10` | `PFramework::PApplicationScript` | 0 |
| `00617470` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PRendering::PStreamInputDescD3D11,8> >` | 7 | `00793F80` | `PFramework::PApplicationScriptBuffer` | 0 |
| `006174D0` | `PClassDescriptorWrapper<struct CD3D11_BLEND_DESC>` | 7 | `00793FC0` | `PFramework::PApplicationScriptProxy` | 0 |
| `00617530` | `PClassDescriptorWrapper<struct CD3D11_DEPTH_STENCIL_DESC>` | 7 | `00794030` | `PFramework::PApplicationViewport` | 0 |
| `00617590` | `PClassDescriptorWrapper<struct CD3D11_RASTERIZER_DESC>` | 7 | `00794080` | `PFramework::PImGuiInternal::PImGuiDynamicMesh` | 0 |
| `006175F0` | `PClassDescriptorWrapper<struct D3D11_DEPTH_STENCILOP_DESC>` | 7 | `007940E0` | `PFramework::PInputDevice` | 0 |
| `00617650` | `PClassDescriptorWrapper<struct D3D11_RENDER_TARGET_BLEND_DESC>` | 7 | `00794110` | `PFramework::PInputDeviceKeyboard` | 0 |
| `00623D60` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PStreamInputDescD3D11>` | 9 | `007941A0` | `PFramework::PInputDeviceMouse` | 0 |
| `00624780` | `PClassDescriptorConcrete<class Phyre::PArray<unsigned char,1> >` | 3 | `00794200` | `PFramework::PInputDevicePad` | 0 |
| `006247F0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PRendering::PStreamInputDescD3D11,8> >` | 3 | `00794280` | `PFramework::PInputDevicePadDirectInput` | 0 |
| `00624820` | `PClassDescriptorWrapper<struct CD3D11_BLEND_DESC>` | 3 | `007942E0` | `PFramework::PInputDevicePadSteamController` | 0 |
| `006248A0` | `PClassDescriptorWrapper<struct CD3D11_DEPTH_STENCIL_DESC>` | 3 | `00794360` | `PFramework::PInputDevicePadXInput` | 0 |
| `006248E0` | `PClassDescriptorWrapper<struct CD3D11_RASTERIZER_DESC>` | 3 | `00799DD0` | `PFramework::PInputDeviceKeyboard` | 2 |
| `00624910` | `PClassDescriptorWrapper<struct D3D11_DEPTH_STENCILOP_DESC>` | 3 | `00799E40` | `PFramework::PInputDeviceMouse` | 2 |
| `00624930` | `PClassDescriptorWrapper<struct D3D11_RENDER_TARGET_BLEND_DESC>` | 3 | `0079A6C0` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PTypedObject>` | 1 |
| `00627050` | `PClassDescriptorWrapper<struct CD3D11_BLEND_DESC>` | 4 | `0079A720` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PInputMapper & __ptr64>` | 1 |
| `00627080` | `PClassDescriptorWrapper<struct CD3D11_DEPTH_STENCIL_DESC>` | 4 | `0079A770` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,int>` | 1 |
| `006270B0` | `PClassDescriptorWrapper<struct CD3D11_RASTERIZER_DESC>` | 4 | `0079A7D0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,unsigned int>` | 1 |
| `006270E0` | `PClassDescriptorWrapper<struct D3D11_DEPTH_STENCILOP_DESC>` | 4 | `0079A830` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PFramework::PApplication,float,char const * __ptr64>` | 1 |
| `00627110` | `PClassDescriptorWrapper<struct D3D11_RENDER_TARGET_BLEND_DESC>` | 4 | `0079A8B0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,double>` | 1 |
| `00628470` | `PClassDataMemberPhyreArray<unsigned char>` | 5 | `0079A920` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PApplicationViewport * __ptr64,unsigned int>` | 1 |
| `00628490` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PStreamInputDescD3D11>` | 5 | `0079A9D0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PDebugUtils * __ptr64>` | 1 |
| `0062A8F0` | `PClassDataMemberPhyreArray<class Phyre::PRendering::PStreamInputDescD3D11>` | 8 | `0079AA50` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PWorld const * __ptr64>` | 1 |
| `0062CFE0` | `PNamedSemanticDescriptorForType<class Phyre::PRendering::PTextureFormatBase>` | 7 | `0079AAD0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PFramework::PApplication,void,class Phyre::PCameraProjection & __ptr64>` | 1 |
| `0062DBD0` | `PNamedSemanticDescriptorForType<class Phyre::PRendering::PTextureFormatBase>` | 10 | `0079AB20` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplicationViewport,unsigned int>` | 1 |
| `0062DCB0` | `PNamedSemanticDescriptorForType<class Phyre::PRendering::PTextureFormatBase>` | 9 | `0079AB80` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplicationViewport,float>` | 1 |
| `0062DD80` | `PWorldMatrixFlyController` | 1 | `0079ABF0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PDebugUtils,void>` | 1 |
| `0062DDE0` | `PWorldMatrixFlyController` | 7 | `0079AC20` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PFramework::PDebugUtils,void,class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4>` | 1 |
| `0062DFB0` | `PWorldMatrixFlyController` | 8 | `0079ACF0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PInputMapper,unsigned int>` | 1 |
| `0062E1C0` | `PWorldMatrixFlyController` | 10 | `0079B2F0` | `PFramework::PImGuiInternal::PImGuiDynamicMesh` | 1 |
| `0062E5A0` | `PWorldMatrixFlyController` | 9 | `0079B850` | `PFramework::PImGuiInternal::PImGuiDynamicMesh` | 3 |
| `0062E980` | `PWorldMatrixFlyController` | 6 | `0079BF70` | `PFramework::PApplication` | 6 |
| `0062EE90` | `PClassDescriptorForType<class Phyre::PClusterDependencyList>` | 7 | `0079BF90` | `PFramework::PImGuiInternal::PImGuiDynamicMesh` | 5 |
| `0062EEF0` | `PClassDescriptorConcrete<class Phyre::PClusterDependencyList>` | 12 | `0079BFA0` | `PFramework::PImGuiInternal::PImGuiDynamicMesh` | 6 |
| `0062EF00` | `PClassDescriptorConcrete<class Phyre::PClusterDependencyList>` | 4 | `0079C730` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PTypedObject>` | 4 |
| `0062EF20` | `PClassDescriptorConcrete<class Phyre::PClusterDependencyList>` | 10 | `0079C740` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PInputMapper & __ptr64>` | 4 |
| `0062EF40` | `PClassDescriptorConcrete<class Phyre::PClusterDependencyList>` | 3 | `0079C7C0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,int>` | 4 |
| `0062EF70` | `PClassDescriptorConcrete<class Phyre::PClusterDependencyList>` | 7 | `0079C840` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,unsigned int>` | 4 |
| `0062F150` | `PClassDescriptorForType<class Phyre::PClassDescriptor>` | 7 | `0079C8C0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PFramework::PApplication,float,char const * __ptr64>` | 4 |
| `0062F1B0` | `PClassDescriptorForClassDescriptor` | 12 | `0079C950` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,double>` | 4 |
| `0062F1C0` | `PClassDescriptorForClassDescriptor` | 4 | `0079C9D0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PApplicationViewport * __ptr64,unsigned int>` | 4 |
| `0062F290` | `PClassDescriptorForClassDescriptor` | 7 | `0079CA60` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PDebugUtils * __ptr64>` | 4 |
| `0062F2F0` | `PClassDescriptorForType<class Phyre::PCluster>` | 7 | `0079CAE0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PWorld const * __ptr64>` | 4 |
| `0062F350` | `PClassDescriptorAbstract<class Phyre::PCluster>` | 12 | `0079CB60` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PFramework::PApplication,void,class Phyre::PCameraProjection & __ptr64>` | 4 |
| `0062F360` | `PClassDescriptorAbstract<class Phyre::PCluster>` | 4 | `0079CBF0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplicationViewport,unsigned int>` | 4 |
| `0062F380` | `PClassDescriptorAbstract<class Phyre::PCluster>` | 7 | `0079CC70` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplicationViewport,float>` | 4 |
| `0062F470` | `PClassDescriptorForType<class Phyre::PClassDataMemberDynamic>` | 7 | `0079CCF0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PDebugUtils,void>` | 4 |
| `0062F4D0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassDataMemberDynamic>` | 12 | `0079CD70` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PFramework::PDebugUtils,void,class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4>` | 4 |
| `0062F4E0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassDataMemberDynamic>` | 14 | `0079CE20` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PInputMapper,unsigned int>` | 4 |
| `0062F4F0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassDataMemberDynamic>` | 4 | `0079D560` | `PFramework::PApplication` | 23 |
| `0062F510` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassDataMemberDynamic>` | 10 | `0079D5B0` | `PFramework::PApplication` | 24 |
| `0062F520` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassDataMemberDynamic>` | 7 | `0079D630` | `PFramework::PInputDeviceKeyboard` | 3 |
| `0062F630` | `PClassDescriptorForType<class Phyre::PNamespace>` | 7 | `0079D650` | `PFramework::PInputDeviceMouse` | 3 |
| `0062F690` | `PClassDescriptorAbstract<class Phyre::PNamespace>` | 12 | `0079D690` | `PFramework::PInputDeviceKeyboard` | 4 |
| `0062F6A0` | `PClassDescriptorAbstract<class Phyre::PNamespace>` | 4 | `0079D6A0` | `PFramework::PInputDeviceMouse` | 4 |
| `0062F6E0` | `PClassDescriptorAbstract<class Phyre::PNamespace>` | 7 | `0079D8B0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PInputMapper & __ptr64>` | 3 |
| `0062F7D0` | `PClassDescriptorForType<class Phyre::PWorld>` | 7 | `0079D8F0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PApplicationViewport * __ptr64,unsigned int>` | 3 |
| `0062F830` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PWorld>` | 12 | `0079D900` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PDebugUtils * __ptr64>` | 3 |
| `0062F840` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PWorld>` | 13 | `0079D910` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PWorld const * __ptr64>` | 3 |
| `0062F860` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PWorld>` | 4 | `007A02F0` | `PFramework::PApplicationViewport` | 3 |
| `0062F880` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PWorld>` | 10 | `007A05D0` | `PFramework::PApplication` | 9 |
| `0062F8A0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PWorld>` | 7 | `007A0B40` | `PFramework::PApplication` | 14 |
| `0062FA50` | `PClassDescriptorForType<class Phyre::PClassDescriptorDynamic>` | 7 | `007A15A0` | `PFramework::PInputDevice` | 5 |
| `0062FAB0` | `PClassDescriptorForType<class Phyre::PClassMember>` | 7 | `007A1640` | `PFramework::PInputDeviceKeyboard` | 5 |
| `0062FB10` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassDescriptorDynamic>` | 12 | `007A1790` | `PFramework::PInputDeviceMouse` | 5 |
| `0062FB20` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassMember>` | 12 | `007A1A50` | `PFramework::PInputDevicePadDirectInput` | 5 |
| `0062FB30` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassDescriptorDynamic>` | 14 | `007A1CD0` | `PFramework::PInputDevicePadSteamController` | 5 |
| `0062FB40` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassDescriptorDynamic>` | 4 | `007A2140` | `PFramework::PInputDevicePadXInput` | 5 |
| `0062FB60` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassMember>` | 4 | `007A3200` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PTypedObject>` | 2 |
| `0062FB80` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassDescriptorDynamic>` | 10 | `007A3260` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PInputMapper & __ptr64>` | 2 |
| `0062FBD0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassDescriptorDynamic>` | 7 | `007A32C0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,int>` | 2 |
| `0062FC30` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PClassMember>` | 7 | `007A3340` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,unsigned int>` | 2 |
| `00633900` | `PClassDataMemberArrayDynamic<class Phyre::PSharray<class Phyre::PString> >` | 0 | `007A33C0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PFramework::PApplication,float,char const * __ptr64>` | 2 |
| `006339A0` | `PClassDataMemberDynamicType<class Phyre::PClassDataMemberDynamic>` | 0 | `007A3450` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,double>` | 2 |
| `006339E0` | `PClassDataMemberPhyreSharray<class Phyre::PString>` | 0 | `007A34D0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PApplicationViewport * __ptr64,unsigned int>` | 2 |
| `00633A80` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PString> >` | 7 | `007A3540` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PFramework::PDebugUtils * __ptr64>` | 2 |
| `00633AE0` | `PClassDescriptorForType<class Phyre::PSharray<class Phyre::PString> >` | 7 | `007A35A0` | `PInternal::PCallerImplementation::PCallerImplementation0::PMethodCallerConcrete<class Phyre::PFramework::PApplication,class Phyre::PWorld const * __ptr64>` | 2 |
| `00633B40` | `PClassDescriptorForType<class Phyre::PBase>` | 7 | `007A3600` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PFramework::PApplication,void,class Phyre::PCameraProjection & __ptr64>` | 2 |
| `00633BA0` | `PTypeDefault<char>` | 7 | `007A36B0` | `PInternal::PCallerImplementation::PCallerImplementation4::PMethodCallerConcrete<class Phyre::PFramework::PDebugUtils,void,class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4,class sce::Vectormath::Scalar::Aos::Vector4>` | 2 |
| `00633BF0` | `PTypeDefault<unsigned char>` | 7 | `007A3A20` | `VTS::ScreenStateOnChangeWindowMode` | 1 |
| `00633C40` | `PTypeDefault<short>` | 7 | `007A3A30` | `VTS::ScreenStateBorderless` | 3 |
| `00633C90` | `PTypeDefault<unsigned short>` | 7 | `007A3A60` | `VTS::ScreenStateFullScreen` | 3 |
| `00633CE0` | `PTypeDefault<int>` | 7 | `007A3A80` | `VTS::ScreenStateFullScreenLoseFocus` | 3 |
| `00633D30` | `PTypeDefault<float>` | 7 | `007A3A90` | `VTS::ScreenStateOnChangeFullScreen` | 3 |
| `00633D80` | `PTypeDefault<double>` | 7 | `007A3AA0` | `VTS::ScreenStateWindow` | 3 |
| `00633DD0` | `PTypeDefault<class Phyre::PQWord>` | 7 | `007A3AF0` | `VTS::ScreenStateBorderless` | 5 |
| `00633E20` | `PTypeDefault<__int64>` | 7 | `007A3B20` | `VTS::ScreenStateFullScreen` | 5 |
| `00633E70` | `PTypeDefault<unsigned __int64>` | 7 | `007A3BA0` | `VTS::ScreenStateFullScreenLoseFocus` | 5 |
| `00633EC0` | `PTypeDefault<bool>` | 7 | `007A3BF0` | `VTS::ScreenStateOnChangeFullScreen` | 5 |
| `00633F10` | `PClassDataMember` | 0 | `007A3C10` | `VTS::ScreenStateWindow` | 5 |
| `00633FB0` | `PClassDataMemberArray` | 0 | `007A3CD0` | `VTS::ScreenStateBase` | 4 |
| `00634050` | `PClassDataMemberArrayFixedSize` | 0 | `007A3CE0` | `VTS::ScreenStateBorderless` | 4 |
| `006340F0` | `PClassDataMemberDynamic` | 0 | `007A3CF0` | `VTS::ScreenStateFullScreen` | 4 |
| `00634150` | `PClassDataMemberEnum` | 0 | `007A3D10` | `VTS::ScreenStateFullScreenLoseFocus` | 4 |
| `006341F0` | `PClassDescriptor` | 7 | `007A3D30` | `VTS::ScreenStateWindow` | 4 |
| `00634250` | `PClassDescriptorBase` | 7 | `007A3DF0` | `VTS::ScreenStateBase` | 6 |
| `006342B0` | `PClassDescriptorDynamic` | 7 | `007A3E00` | `VTS::ScreenStateBorderless` | 6 |
| `00634310` | `PIClassDataMemberDynamicType` | 0 | `007A3EE0` | `VTS::ScreenStateFullScreen` | 6 |
| `00639290` | `PClassDescriptorDynamic` | 8 | `007A3F80` | `VTS::ScreenStateFullScreenLoseFocus` | 6 |
| `00639A40` | `PClassDescriptorDynamic` | 12 | `007A4040` | `VTS::ScreenStateOnChangeFullScreen` | 6 |
| `0063A110` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PNamespace & __ptr64>` | 1 | `007A4050` | `VTS::ScreenStateOnChangeWindowMode` | 6 |
| `0063A150` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PClassDescriptor,bool,class Phyre::PClassDescriptor const & __ptr64>` | 1 | `007A40B0` | `VTS::ScreenStateWindow` | 6 |
| `0063A1D0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCluster,class Phyre::PTypedObject,class Phyre::PClassDescriptor const & __ptr64>` | 1 | `00866DB0` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceVisionTrackerY>` | 7 |
| `0063A280` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCluster,enum Phyre::PResult,class Phyre::PBase * __ptr64>` | 1 | `00866E10` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMotionQuatZ>` | 7 |
| `0063A300` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCluster,void,class Phyre::PCluster & __ptr64>` | 1 | `00866E70` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMouseDeltaY>` | 7 |
| `0063A350` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCluster,void,class Phyre::PClassDescriptor const & __ptr64>` | 1 | `00866F20` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceVisionTrackerY>` | 7 |
| `0063A3A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PNamespace,class Phyre::PClassDescriptor const * __ptr64,char const * __ptr64>` | 1 | `00866FA0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceVisionTrackerY>` | 10 |
| `0063A440` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PWorld,unsigned int,char const * __ptr64>` | 1 | `00866FE0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMotionQuatZ>` | 7 |
| `0063A770` | `PClassDescriptorDynamic` | 10 | `00867040` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceVisionTrackerY>` | 3 |
| `0063AD90` | `PClassDescriptorDynamic` | 11 | `00867080` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatZ>` | 10 |
| `0063AFF0` | `PClassDescriptorDynamic` | 14 | `008670C0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMouseDeltaY>` | 7 |
| `0063B5D0` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PNamespace & __ptr64>` | 4 | `00867120` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatZ>` | 3 |
| `0063B5E0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PClassDescriptor,bool,class Phyre::PClassDescriptor const & __ptr64>` | 4 | `00867160` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMouseDeltaY>` | 10 |
| `0063B660` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCluster,class Phyre::PTypedObject,class Phyre::PClassDescriptor const & __ptr64>` | 4 | `00867190` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceVisionTrackerY>` | 7 |
| `0063B6F0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCluster,enum Phyre::PResult,class Phyre::PBase * __ptr64>` | 4 | `008671F0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMouseDeltaY>` | 3 |
| `0063B780` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCluster,void,class Phyre::PCluster & __ptr64>` | 4 | `00867250` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatZ>` | 7 |
| `0063B800` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCluster,void,class Phyre::PClassDescriptor const & __ptr64>` | 4 | `008672B0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMouseDeltaY>` | 7 |
| `0063B890` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PNamespace,class Phyre::PClassDescriptor const * __ptr64,char const * __ptr64>` | 4 | `00867520` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceVisionTrackerZ>` | 7 |
| `0063B920` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PWorld,unsigned int,char const * __ptr64>` | 4 | `00867580` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMotionQuatW>` | 7 |
| `0063B9E0` | `PClassDataMemberArrayFixedSize` | 6/7 | `008675E0` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceTouchRotate>` | 7 |
| `0063BA00` | `PClassLayoutInterface` | 3 | `008676A0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceVisionTrackerZ>` | 7 |
| `0063BAF0` | `PClassLayoutInterface` | 2 | `00867720` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceVisionTrackerZ>` | 10 |
| `0063BB00` | `PClassLayoutInterface` | 4/5 | `00867760` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMotionQuatW>` | 7 |
| `0063BB60` | `PClassDataMemberDynamicType<class Phyre::PClassDataMemberDynamic>` | 1 | `008677C0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceVisionTrackerZ>` | 3 |
| `0063BC70` | `PClassDataMemberArrayFixedSize` | 4 | `00867800` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatW>` | 10 |
| `0063BF80` | `PClassDescriptorDynamic` | 13 | `00867840` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceTouchRotate>` | 7 |
| `0063C020` | `PClassDescriptorDynamic` | 5 | `008678A0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatW>` | 3 |
| `0063C090` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PNamespace & __ptr64>` | 3 | `008678E0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchRotate>` | 10 |
| `0063C0A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PClassDescriptor,bool,class Phyre::PClassDescriptor const & __ptr64>` | 3 | `00867920` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceVisionTrackerZ>` | 7 |
| `0063C0B0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PWorld,unsigned int,char const * __ptr64>` | 3 | `00867980` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchRotate>` | 3 |
| `0063C1F0` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PString> >` | 3 | `008679C0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatW>` | 7 |
| `0063C310` | `PTypeDefault<float>` | 3 | `00867A20` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchRotate>` | 7 |
| `0063C360` | `PTypeDefault<double>` | 3 | `00867BE0` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMotionAngularVelocityX>` | 7 |
| `0063C3B0` | `PTypeDefault<class Phyre::PQWord>` | 3 | `00867C60` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceTouchPinch>` | 7 |
| `0063C450` | `PTypeDefault<bool>` | 3 | `00867D00` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMotionAngularVelocityX>` | 7 |
| `0063C540` | `PClassDescriptorDynamic` | 3 | `00867D60` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionAngularVelocityX>` | 10 |
| `0063D010` | `PClassDescriptorDynamic` | 6 | `00867DA0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceTouchPinch>` | 7 |
| `0063D090` | `PClassDescriptorConcrete<class Phyre::PSharray<class Phyre::PString> >` | 4 | `00867E00` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionAngularVelocityX>` | 3 |
| `0063D0C0` | `PTypeDefault<char>` | 4 | `00867E40` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchPinch>` | 10 |
| `0063D100` | `PTypeDefault<unsigned char>` | 4 | `00867E80` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchPinch>` | 3 |
| `0063D140` | `PTypeDefault<short>` | 4 | `00867EC0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionAngularVelocityX>` | 7 |
| `0063D180` | `PTypeDefault<unsigned short>` | 4 | `00867F20` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchPinch>` | 7 |
| `0063D1C0` | `PTypeDefault<int>` | 4 | `008680E0` | `PClassDescriptorForType<class Phyre::PInputs::PInputAction>` | 7 |
| `0063D200` | `PTypeDefault<float>` | 4 | `008681C0` | `PClassDescriptorForType<class Phyre::PInputs::PInputSource>` | 7 |
| `0063D240` | `PTypeDefault<double>` | 4 | `008682B0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSource>` | 12 |
| `0063D2C0` | `PTypeDefault<bool>` | 4 | `00868340` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMotionAngularVelocityY>` | 7 |
| `0063D3C0` | `PClassDescriptorDynamic` | 4 | `008683A0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputAction>` | 7 |
| `0063D790` | `PClassDescriptorDynamic` | 9 | `00868400` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSource>` | 4 |
| `0063DC60` | `PClassDataMemberPhyreSharray<class Phyre::PString>` | 5 | `00868420` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputAction>` | 10 |
| `0063DF60` | `PClassDataMemberPhyreSharray<class Phyre::PString>` | 8 | `00868460` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceTouchTwoFingerDragX>` | 7 |
| `0063E010` | `PTypeDefault<short>` | 0 | `008684C0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputAction>` | 3 |
| `0063E040` | `PTypeDefault<unsigned short>` | 0 | `00868510` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSource>` | 7 |
| `0063E050` | `PTypeDefault<int>` | 0 | `00868590` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputAction>` | 7 |
| `0063E090` | `PTypeDefault<float>` | 0 | `00868610` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMotionAngularVelocityY>` | 7 |
| `0063E0D0` | `PTypeDefault<double>` | 0 | `00868670` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionAngularVelocityY>` | 10 |
| `0063E170` | `PTypeDefault<class Phyre::PQWord>` | 0 | `008686B0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceTouchTwoFingerDragX>` | 7 |
| `0063E1A0` | `PTypeDefault<__int64>` | 0 | `00868710` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionAngularVelocityY>` | 3 |
| `0063E230` | `PTypeDefault<unsigned __int64>` | 0 | `00868750` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchTwoFingerDragX>` | 10 |
| `0063E2C0` | `PClassDescriptorDynamic` | 0 | `00868790` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchTwoFingerDragX>` | 3 |
| `0063E490` | `PInternal::PCallerImplementation::PCallerImplementation0::PFunctionCallerConcrete<class Phyre::PNamespace & __ptr64>` | 2 | `008687D0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionAngularVelocityY>` | 7 |
| `0063E4F0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PClassDescriptor,bool,class Phyre::PClassDescriptor const & __ptr64>` | 2 | `00868830` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchTwoFingerDragX>` | 7 |
| `0063E580` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCluster,class Phyre::PTypedObject,class Phyre::PClassDescriptor const & __ptr64>` | 2 | `00868940` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceKey>` | 7 |
| `0063E600` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PCluster,enum Phyre::PResult,class Phyre::PBase * __ptr64>` | 2 | `00868B30` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMotionAngularVelocityZ>` | 7 |
| `0063E6D0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PNamespace,class Phyre::PClassDescriptor const * __ptr64,char const * __ptr64>` | 2 | `00868B90` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceKey>` | 7 |
| `0063E750` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PWorld,unsigned int,char const * __ptr64>` | 2 | `00868C10` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceKey>` | 10 |
| `0063E7E0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PAtmosphericsBase>` | 7 | `00868C40` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceTouchTwoFingerDragY>` | 7 |
| `0063E840` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PFXAA>` | 10 | `00868CA0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceKey>` | 3 |
| `0063E8D0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PFXAA>` | 3 | `00868D40` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceKey>` | 7 |
| `0063E8E0` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PMotionBlurBase>` | 7 | `00868DC0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMotionAngularVelocityZ>` | 7 |
| `0063E960` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PFXAA>` | 7 | `00868E20` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionAngularVelocityZ>` | 10 |
| `0063E9C0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMotionBlurBase>` | 10 | `00868E60` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceTouchTwoFingerDragY>` | 7 |
| `0063E9F0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMotionBlurBase>` | 3 | `00868EC0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionAngularVelocityZ>` | 3 |
| `0063EA00` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PAtmosphericsBase>` | 7 | `00868F00` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchTwoFingerDragY>` | 10 |
| `0063EA60` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PAtmosphericsBase>` | 10 | `00868F40` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchTwoFingerDragY>` | 3 |
| `0063EA90` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMotionBlurBase>` | 7 | `00868F80` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionAngularVelocityZ>` | 7 |
| `0063EAF0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PAtmosphericsBase>` | 3 | `00869000` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchTwoFingerDragY>` | 7 |
| `0063EB00` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PAtmosphericsBase>` | 7 | `008690F0` | `PClassDescriptorForType<class Phyre::PInputs::PInputMap>` | 7 |
| `0063EC10` | `PClassDescriptorForType<class Phyre::PPostProcessing::PDepthOfField>` | 7 | `008692A0` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceJoypadButton>` | 7 |
| `0063EE60` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PDepthOfField>` | 7 | `00869340` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputMap>` | 7 |
| `0063EEC0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PAtmosphericsD3D11>` | 7 | `00869460` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputMap>` | 3 |
| `0063EF60` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDepthOfField>` | 10 | `00869490` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMotionLinearAccelerationX>` | 7 |
| `0063EFF0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDepthOfField>` | 3 | `00869530` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputMap>` | 7 |
| `0063F000` | `PClassDescriptorForType<class Phyre::PPostProcessing::PScreenSpaceReflectionBase>` | 7 | `00869590` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceTouchDragX>` | 7 |
| `0063F140` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDepthOfField>` | 7 | `008695F0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceJoypadButton>` | 7 |
| `0063F1A0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PMotionBlurD3D11>` | 7 | `00869670` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceJoypadButton>` | 10 |
| `0063F240` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PAtmosphericsD3D11>` | 7 | `008696A0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceJoypadButton>` | 3 |
| `0063F2A0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PAtmosphericsD3D11>` | 10 | `00869720` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMotionLinearAccelerationX>` | 7 |
| `0063F2E0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PMLAABase>` | 7 | `00869780` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceJoypadButton>` | 7 |
| `0063F340` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PAtmosphericsD3D11>` | 3 | `008697E0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionLinearAccelerationX>` | 10 |
| `0063F390` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PScreenSpaceReflectionBase>` | 7 | `00869820` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceTouchDragX>` | 7 |
| `0063F3F0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceReflectionBase>` | 10 | `00869880` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionLinearAccelerationX>` | 3 |
| `0063F420` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceReflectionBase>` | 3 | `008698C0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchDragX>` | 10 |
| `0063F480` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PAtmosphericsD3D11>` | 7 | `00869900` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchDragX>` | 3 |
| `0063F4E0` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PMotionBlurD3D11>` | 7 | `00869940` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionLinearAccelerationX>` | 7 |
| `0063F580` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMotionBlurD3D11>` | 10 | `008699A0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchDragX>` | 7 |
| `0063F610` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMotionBlurD3D11>` | 3 | `00869BD0` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceJoypadAxis>` | 7 |
| `0063F620` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceReflectionBase>` | 7 | `00869C80` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMotionLinearAccelerationY>` | 7 |
| `0063F680` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PMLAABase>` | 7 | `00869D20` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceTouchDragY>` | 7 |
| `0063F6E0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMLAABase>` | 10 | `00869DC0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceJoypadAxis>` | 7 |
| `0063F710` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMotionBlurD3D11>` | 7 | `00869E20` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceJoypadAxis>` | 10 |
| `0063F770` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMLAABase>` | 3 | `00869EA0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceJoypadAxis>` | 3 |
| `0063F780` | `PClassDescriptorForType<class Phyre::PPostProcessing::PDeferredLightingBase>` | 7 | `00869EF0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMotionLinearAccelerationY>` | 7 |
| `0063F7F0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMLAABase>` | 7 | `00869F50` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionLinearAccelerationY>` | 10 |
| `0063F940` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PDeferredLightingBase>` | 7 | `00869F90` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceTouchDragY>` | 7 |
| `0063F9A0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDeferredLightingBase>` | 10 | `00869FF0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionLinearAccelerationY>` | 3 |
| `0063F9D0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDeferredLightingBase>` | 3 | `0086A030` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceJoypadAxis>` | 7 |
| `0063FA30` | `PClassDescriptorForType<class Phyre::PPostProcessing::PGlowBase>` | 7 | `0086A090` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchDragY>` | 10 |
| `0063FB00` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDeferredLightingBase>` | 7 | `0086A0D0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchDragY>` | 3 |
| `0063FB80` | `PClassDescriptorForType<class Phyre::PPostProcessing::PScreenSpaceReflectionD3D11>` | 7 | `0086A110` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionLinearAccelerationY>` | 7 |
| `0063FC00` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PGlowBase>` | 7 | `0086A170` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceTouchDragY>` | 7 |
| `0063FC80` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlowBase>` | 10 | `0086A3E0` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMouseButton>` | 7 |
| `0063FD00` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlowBase>` | 3 | `0086A450` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMotionLinearAccelerationZ>` | 7 |
| `0063FE00` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlowBase>` | 7 | `0086A4B0` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMotionQuatX>` | 7 |
| `0063FEA0` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PScreenSpaceReflectionD3D11>` | 7 | `0086A550` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMouseButton>` | 7 |
| `0063FF00` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceReflectionD3D11>` | 10 | `0086A5D0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMouseButton>` | 10 |
| `0063FF40` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceReflectionD3D11>` | 3 | `0086A600` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMotionLinearAccelerationZ>` | 7 |
| `0063FF50` | `PClassDescriptorForType<class Phyre::PPostProcessing::PAtmospherics>` | 7 | `0086A660` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMouseButton>` | 3 |
| `00640040` | `PClassDescriptorForType<class Phyre::PPostProcessing::PMLAAD3D11>` | 7 | `0086A6B0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionLinearAccelerationZ>` | 10 |
| `00640100` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceReflectionD3D11>` | 7 | `0086A6F0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMotionQuatX>` | 7 |
| `006401A0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PMotionBlur>` | 7 | `0086A750` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionLinearAccelerationZ>` | 3 |
| `00640220` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PAtmospherics>` | 7 | `0086A790` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatX>` | 10 |
| `00640280` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PAtmospherics>` | 10 | `0086A7D0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMouseButton>` | 7 |
| `006402D0` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PMLAAD3D11>` | 7 | `0086A830` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatX>` | 3 |
| `00640330` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PAtmospherics>` | 3 | `0086A870` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionLinearAccelerationZ>` | 7 |
| `00640340` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMLAAD3D11>` | 10 | `0086A8D0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatX>` | 7 |
| `006403A0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMLAAD3D11>` | 3 | `0086AB40` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceVisionTrackerX>` | 7 |
| `006403B0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PAtmospherics>` | 7 | `0086ABA0` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMouseDeltaX>` | 7 |
| `00640410` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PMotionBlur>` | 7 | `0086AC00` | `PClassDescriptorForType<class Phyre::PInputs::PInputSourceMotionQuatY>` | 7 |
| `00640470` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMLAAD3D11>` | 7 | `0086ACD0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceVisionTrackerX>` | 7 |
| `006404D0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMotionBlur>` | 10 | `0086AD30` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceVisionTrackerX>` | 10 |
| `00640520` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMotionBlur>` | 3 | `0086AD70` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMouseDeltaX>` | 7 |
| `006405A0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMotionBlur>` | 7 | `0086ADD0` | `PClassDescriptorAbstract<class Phyre::PInputs::PInputSourceMotionQuatY>` | 7 |
| `00640640` | `PClassDescriptorForType<class Phyre::PPostProcessing::PGlowGPUBase>` | 7 | `0086AE30` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceVisionTrackerX>` | 3 |
| `00640840` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PGlowGPUBase>` | 7 | `0086AE70` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMouseDeltaX>` | 10 |
| `006408A0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PScreenSpaceReflection>` | 7 | `0086AEA0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatY>` | 10 |
| `00640900` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlowGPUBase>` | 10 | `0086AEE0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMouseDeltaX>` | 3 |
| `006409E0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlowGPUBase>` | 3 | `0086AF40` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatY>` | 3 |
| `00640A50` | `PClassDescriptorForType<class Phyre::PPostProcessing::PLowResParticles>` | 7 | `0086AF80` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceVisionTrackerX>` | 7 |
| `00640AF0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlowGPUBase>` | 7 | `0086AFE0` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMouseDeltaX>` | 7 |
| `00640BC0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PMLAA>` | 7 | `0086B040` | `PClassDescriptorConcrete<class Phyre::PInputs::PInputSourceMotionQuatY>` | 7 |
| `00640C60` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PScreenSpaceReflection>` | 7 | `0086CA30` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PInputs::PInputAction * __ptr64,8> >` | 0 |
| `00640D00` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceReflection>` | 10 | `0086CA90` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PInputs::PInputSource * __ptr64,8> >` | 0 |
| `00640D50` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceReflection>` | 3 | `0086CAF0` | `PClassDataMemberPhyreArray<class Phyre::PInputs::PInputAction * __ptr64>` | 0 |
| `00640D60` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PLowResParticles>` | 7 | `0086CB50` | `PClassDataMemberPhyreArray<class Phyre::PInputs::PInputSource * __ptr64>` | 0 |
| `00640DE0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionBase>` | 7 | `0086CBB0` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PInputs::PInputAction * __ptr64,8> >` | 7 |
| `00640E40` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PLowResParticles>` | 10 | `0086CC10` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PInputs::PInputSource * __ptr64,8> >` | 7 |
| `00640EB0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceReflection>` | 7 | `0086CC70` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PInputs::PInputAction * __ptr64,8> >` | 7 |
| `00640F10` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PLowResParticles>` | 3 | `0086CCD0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PInputs::PInputSource * __ptr64,8> >` | 7 |
| `00640F20` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PMLAA>` | 7 | `0086CD30` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PInputs::PInputAction * __ptr64,8> >` | 7 |
| `00640FD0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMLAA>` | 10 | `0086CD90` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PInputs::PInputSource * __ptr64,8> >` | 7 |
| `00641060` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PLowResParticles>` | 7 | `0086CDF0` | `PInputs::PInputAction` | 0 |
| `006410C0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMLAA>` | 3 | `0086CE50` | `PInputs::PInputSource` | 0 |
| `00641160` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionBase>` | 7 | `0086CEA0` | `PInputs::PInputSourceJoypadAxis` | 0 |
| `006411E0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMLAA>` | 7 | `0086CEF0` | `PInputs::PInputSourceJoypadButton` | 0 |
| `00641280` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionBase>` | 10 | `0086CF40` | `PInputs::PInputSourceKey` | 0 |
| `006412E0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PDeferredLightingD3D11>` | 7 | `0086CF90` | `PInputs::PInputSourceMotionAngularVelocityX` | 0 |
| `00641340` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionBase>` | 3 | `0086CFE0` | `PInputs::PInputSourceMotionAngularVelocityY` | 0 |
| `00641370` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionBase>` | 7 | `0086D030` | `PInputs::PInputSourceMotionAngularVelocityZ` | 0 |
| `006413D0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PGlowD3D11>` | 7 | `0086D080` | `PInputs::PInputSourceMotionLinearAccelerationX` | 0 |
| `00641470` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PDeferredLightingD3D11>` | 7 | `0086D0D0` | `PInputs::PInputSourceMotionLinearAccelerationY` | 0 |
| `006414F0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDeferredLightingD3D11>` | 10 | `0086D120` | `PInputs::PInputSourceMotionLinearAccelerationZ` | 0 |
| `00641520` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDeferredLightingD3D11>` | 3 | `0086D170` | `PInputs::PInputSourceMotionQuatW` | 0 |
| `00641530` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PGlowD3D11>` | 7 | `0086D1C0` | `PInputs::PInputSourceMotionQuatX` | 0 |
| `00641590` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlowD3D11>` | 10 | `0086D210` | `PInputs::PInputSourceMotionQuatY` | 0 |
| `00641600` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDeferredLightingD3D11>` | 7 | `0086D260` | `PInputs::PInputSourceMotionQuatZ` | 0 |
| `00641660` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlowD3D11>` | 3 | `0086D2B0` | `PInputs::PInputSourceMouseButton` | 0 |
| `00641790` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlowD3D11>` | 7 | `0086D300` | `PInputs::PInputSourceMouseDeltaX` | 0 |
| `00641830` | `PClassDescriptorForType<class Phyre::PPostProcessing::PMaterialPostEffect>` | 7 | `0086D350` | `PInputs::PInputSourceMouseDeltaY` | 0 |
| `006418E0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PCelShadingBase>` | 7 | `0086D3A0` | `PInputs::PInputSourceTouchDragX` | 0 |
| `00641A10` | `PClassDescriptorForType<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionD3D11>` | 7 | `0086D3F0` | `PInputs::PInputSourceTouchDragY` | 0 |
| `00641A90` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PMaterialPostEffect>` | 7 | `0086D440` | `PInputs::PInputSourceTouchPinch` | 0 |
| `00641AF0` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PCelShadingBase>` | 7 | `0086D490` | `PInputs::PInputSourceTouchRotate` | 0 |
| `00641B50` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMaterialPostEffect>` | 10 | `0086D4E0` | `PInputs::PInputSourceTouchTwoFingerDragX` | 0 |
| `00641BB0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PCelShadingBase>` | 10 | `0086D530` | `PInputs::PInputSourceTouchTwoFingerDragY` | 0 |
| `00641BE0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMaterialPostEffect>` | 3 | `0086D580` | `PInputs::PInputSourceVisionTrackerX` | 0 |
| `00641BF0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PCelShadingBase>` | 3 | `0086D5D0` | `PInputs::PInputSourceVisionTrackerY` | 0 |
| `00641C20` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMaterialPostEffect>` | 7 | `0086D620` | `PInputs::PInputSourceVisionTrackerZ` | 0 |
| `00641C80` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PCelShadingBase>` | 7 | `00872F20` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInputs::PInputAction,class Phyre::PBase * __ptr64,unsigned int>` | 1 |
| `00641CE0` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionD3D11>` | 7 | `00872FE0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInputs::PInputAction,class Phyre::PClassDescriptor const * __ptr64,unsigned int>` | 1 |
| `00641D40` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionD3D11>` | 10 | `00873090` | `PInputs::PInputSourceJoypadAxis` | 2 |
| `00641DA0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionD3D11>` | 3 | `00873100` | `PInputs::PInputSourceJoypadButton` | 2 |
| `00641E20` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionD3D11>` | 7 | `00873170` | `PInputs::PInputSourceKey` | 2 |
| `00641EC0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PGlow>` | 7 | `008731E0` | `PInputs::PInputSourceMotionAngularVelocityX` | 2 |
| `006420D0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PDeferredLighting>` | 7 | `00873240` | `PInputs::PInputSourceMotionAngularVelocityY` | 2 |
| `00642150` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PGlow>` | 7 | `008732A0` | `PInputs::PInputSourceMotionAngularVelocityZ` | 2 |
| `006421B0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlow>` | 10 | `00873300` | `PInputs::PInputSourceMotionLinearAccelerationX` | 2 |
| `006421E0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PCelShadingD3D11>` | 7 | `00873360` | `PInputs::PInputSourceMotionLinearAccelerationY` | 2 |
| `00642240` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlow>` | 3 | `008733C0` | `PInputs::PInputSourceMotionLinearAccelerationZ` | 2 |
| `00642300` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PGlow>` | 7 | `00873420` | `PInputs::PInputSourceMotionQuatW` | 2 |
| `006423C0` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PDeferredLighting>` | 7 | `00873480` | `PInputs::PInputSourceMotionQuatX` | 2 |
| `00642420` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDeferredLighting>` | 10 | `008734E0` | `PInputs::PInputSourceMotionQuatY` | 2 |
| `00642470` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDeferredLighting>` | 3 | `00873540` | `PInputs::PInputSourceMotionQuatZ` | 2 |
| `00642480` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PCelShadingD3D11>` | 7 | `008735A0` | `PInputs::PInputSourceMouseButton` | 2 |
| `006424E0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusion>` | 7 | `00873610` | `PInputs::PInputSourceMouseDeltaX` | 2 |
| `00642540` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PCelShadingD3D11>` | 10 | `00873680` | `PInputs::PInputSourceMouseDeltaY` | 2 |
| `006425A0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PCelShadingD3D11>` | 3 | `008736F0` | `PInputs::PInputSourceTouchDragX` | 2 |
| `006425B0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDeferredLighting>` | 7 | `00873750` | `PInputs::PInputSourceTouchDragY` | 2 |
| `00642630` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PCelShadingD3D11>` | 7 | `008737B0` | `PInputs::PInputSourceTouchPinch` | 2 |
| `00642690` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusion>` | 7 | `00873810` | `PInputs::PInputSourceTouchRotate` | 2 |
| `006426F0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusion>` | 10 | `00873870` | `PInputs::PInputSourceTouchTwoFingerDragX` | 2 |
| `00642760` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusion>` | 3 | `008738D0` | `PInputs::PInputSourceTouchTwoFingerDragY` | 2 |
| `00642770` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PScreenSpaceAmbientOcclusion>` | 7 | `00873930` | `PInputs::PInputSourceVisionTrackerX` | 2 |
| `006428D0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PFXAABase>` | 7 | `00873990` | `PInputs::PInputSourceVisionTrackerY` | 2 |
| `00642B30` | `PClassDescriptorForType<class Phyre::PPostProcessing::PDepthOfFieldBase>` | 7 | `008739F0` | `PInputs::PInputSourceVisionTrackerZ` | 2 |
| `00642BA0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PPostEffectManager>` | 7 | `00873AD0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInputs::PInputAction,class Phyre::PBase * __ptr64,unsigned int>` | 4 |
| `00642C00` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PFXAABase>` | 7 | `00873B60` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInputs::PInputAction,class Phyre::PClassDescriptor const * __ptr64,unsigned int>` | 4 |
| `00642C70` | `PClassDescriptorForType<class Phyre::PPostProcessing::PCelShading>` | 7 | `00873BF0` | `PClassDataMemberPhyreArray<class Phyre::PInputs::PInputAction * __ptr64>` | 9 |
| `00642CD0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PFXAABase>` | 10 | `00873C00` | `PClassDataMemberPhyreArray<class Phyre::PInputs::PInputSource * __ptr64>` | 9 |
| `00642D40` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PFXAABase>` | 3 | `00873D30` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PInputs::PInputAction * __ptr64,8> >` | 3 |
| `00642DB0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PFXAABase>` | 7 | `00873DA0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PInputs::PInputSource * __ptr64,8> >` | 3 |
| `00642E10` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PDepthOfFieldBase>` | 7 | `00873FB0` | `PInputs::PInputSourceJoypadAxis` | 1 |
| `00642E70` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDepthOfFieldBase>` | 10 | `00873FE0` | `PInputs::PInputSourceJoypadButton` | 1 |
| `00642EE0` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PPostEffectManager>` | 7 | `00874080` | `PInputs::PInputSourceKey` | 1 |
| `00642F40` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDepthOfFieldBase>` | 3 | `00874120` | `PInputs::PInputSourceMouseButton` | 1 |
| `00642F50` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PPostEffectManager>` | 10 | `00874200` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInputs::PInputAction,class Phyre::PBase * __ptr64,unsigned int>` | 2 |
| `00642F70` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PCelShading>` | 7 | `008742A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PInputs::PInputAction,class Phyre::PClassDescriptor const * __ptr64,unsigned int>` | 2 |
| `00642FD0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PPostEffectManager>` | 3 | `00874660` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionMoveTracker>` | 7 |
| `00643000` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PCelShading>` | 10 | `008746C0` | `PClassDescriptorConcrete<class Phyre::PVision::PVisionMoveTracker>` | 3 |
| `00643050` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PCelShading>` | 3 | `008746E0` | `PClassDescriptorConcrete<class Phyre::PVision::PVisionMoveTracker>` | 7 |
| `00643060` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDepthOfFieldBase>` | 7 | `008747D0` | `PClassDescriptorForType<class Phyre::PVision::PVisionMoveTrackerBase>` | 7 |
| `006430C0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PPostEffectManager>` | 7 | `00874830` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionMoveTrackerBase>` | 12 |
| `00643120` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PCelShading>` | 7 | `00874850` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionMoveTrackerBase>` | 4 |
| `006432E0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PMeshParticleSystemBase>` | 7 | `00874870` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionMoveTrackerBase>` | 7 |
| `00643360` | `PClassDescriptorForType<class Phyre::PPostProcessing::PFXAAD3D11>` | 7 | `00874960` | `PClassDescriptorForType<class Phyre::PVision::PVisionMoveTrackerWin32>` | 7 |
| `006434D0` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PMeshParticleSystemBase>` | 7 | `008749C0` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionMoveTrackerWin32>` | 12 |
| `00643530` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMeshParticleSystemBase>` | 10 | `008749E0` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionMoveTrackerWin32>` | 4 |
| `00643560` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PFXAAD3D11>` | 7 | `00874A00` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionMoveTrackerWin32>` | 7 |
| `006435C0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMeshParticleSystemBase>` | 3 | `00874AF0` | `PClassDescriptorForType<class Phyre::PVision::PVisionMoveTracker>` | 7 |
| `006435D0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PFXAAD3D11>` | 10 | `00875230` | `PClassDescriptorForType<class Phyre::PVision::PVisionTracker>` | 7 |
| `00643620` | `PClassDescriptorForType<class Phyre::PPostProcessing::PPostEffectBase>` | 7 | `008752D0` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionTracker>` | 7 |
| `00643680` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PFXAAD3D11>` | 3 | `00875330` | `PClassDescriptorConcrete<class Phyre::PVision::PVisionTracker>` | 3 |
| `006436A0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PMeshParticleSystemBase>` | 7 | `00875350` | `PClassDescriptorConcrete<class Phyre::PVision::PVisionTracker>` | 7 |
| `00643700` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PFXAAD3D11>` | 7 | `00875440` | `PClassDescriptorForType<class Phyre::PVision::PVisionTrackerBase>` | 7 |
| `00643780` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PPostEffectBase>` | 7 | `008754A0` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionTrackerBase>` | 12 |
| `006437E0` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PPostEffectBase>` | 10 | `008754C0` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionTrackerBase>` | 4 |
| `00643810` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PPostEffectBase>` | 3 | `008754E0` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionTrackerBase>` | 7 |
| `00643840` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PPostEffectBase>` | 7 | `008755D0` | `PClassDescriptorForType<class Phyre::PVision::PVisionTrackerWin32>` | 7 |
| `00643950` | `PClassDescriptorForType<class Phyre::PPostProcessing::PDepthOfFieldD3D11>` | 7 | `00875630` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionTrackerWin32>` | 12 |
| `00643AF0` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PDepthOfFieldD3D11>` | 7 | `00875650` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionTrackerWin32>` | 4 |
| `00643B70` | `PClassDescriptorForType<class Phyre::PPostProcessing::PFXAA>` | 7 | `00875670` | `PClassDescriptorAbstract<class Phyre::PVision::PVisionTrackerWin32>` | 7 |
| `00643C10` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDepthOfFieldD3D11>` | 10 | `00875E10` | `PInputs::PUtilityInputs` | 1 |
| `00643C70` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDepthOfFieldD3D11>` | 3 | `00875FC0` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputTypeSemantic>` | 7 |
| `00643D50` | `PClassDescriptorConcrete<class Phyre::PPostProcessing::PDepthOfFieldD3D11>` | 7 | `00876020` | `PInputs::PInputTypeSemantic` | 0 |
| `00643DB0` | `PClassDescriptorForType<class Phyre::PPostProcessing::PMotionBlurBase>` | 7 | `008761A0` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputTypeSemantic>` | 10 |
| `00643E20` | `PClassDescriptorAbstract<class Phyre::PPostProcessing::PFXAA>` | 7 | `00876280` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputTypeSemantic>` | 9 |
| `00646DB0` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PPostProcessing::PPostEffectBase * __ptr64,8> >` | 0 | `008762E0` | `PGame::PUtilityGame` | 1 |
| `00646E10` | `PClassDataMemberPhyreArray<class Phyre::PPostProcessing::PPostEffectBase * __ptr64>` | 0 | `008763B0` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputAxisSemantic>` | 7 |
| `00646E70` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PPostProcessing::PPostEffectBase * __ptr64,8> >` | 7 | `00876410` | `PInputs::PInputAxisSemantic` | 0 |
| `00646ED0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PPostProcessing::PPostEffectBase * __ptr64,8> >` | 7 | `00876590` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputAxisSemantic>` | 10 |
| `00646F30` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PPostProcessing::PPostEffectBase * __ptr64,8> >` | 7 | `00876670` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputAxisSemantic>` | 9 |
| `00646F90` | `PPostProcessing::PAtmospherics` | 0 | `00876790` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputJoypadButtonSemantic>` | 7 |
| `00646FF0` | `PPostProcessing::PAtmosphericsBase` | 0 | `008767F0` | `PInputs::PInputJoypadButtonSemantic` | 0 |
| `00647050` | `PPostProcessing::PAtmosphericsD3D11` | 0 | `008769A0` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputJoypadButtonSemantic>` | 10 |
| `006470B0` | `PPostProcessing::PCelShading` | 0 | `00876A80` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputJoypadButtonSemantic>` | 9 |
| `00647140` | `PPostProcessing::PCelShadingBase` | 0 | `00876BA0` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputKeySemantic>` | 7 |
| `006471D0` | `PPostProcessing::PCelShadingD3D11` | 0 | `00876C00` | `PInputs::PInputKeySemantic` | 0 |
| `00647260` | `PPostProcessing::PDeferredLighting` | 0 | `00876D80` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputKeySemantic>` | 10 |
| `006472C0` | `PPostProcessing::PDeferredLightingBase` | 0 | `00876E60` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputKeySemantic>` | 9 |
| `00647320` | `PPostProcessing::PDeferredLightingD3D11` | 0 | `00876F80` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputMouseButtonSemantic>` | 7 |
| `00647380` | `PPostProcessing::PDepthOfField` | 0 | `00876FE0` | `PInputs::PInputMouseButtonSemantic` | 0 |
| `006473E0` | `PPostProcessing::PDepthOfFieldBase` | 0 | `00877160` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputMouseButtonSemantic>` | 10 |
| `00647470` | `PPostProcessing::PDepthOfFieldD3D11` | 0 | `00877240` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputMouseButtonSemantic>` | 9 |
| `006474D0` | `PPostProcessing::PDepthOfFieldLayered` | 0 | `008772A0` | `PClassDescriptorAbstract<class Phyre::PHierarchy::POctreeChildren>` | 7 |
| `00647530` | `PPostProcessing::PFXAA` | 0 | `00877300` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PHierarchy::POctreeChildren>` | 10 |
| `00647590` | `PPostProcessing::PFXAABase` | 0 | `00877350` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PHierarchy::POctreeChildren>` | 7 |
| `006475F0` | `PPostProcessing::PFXAAD3D11` | 0 | `00877470` | `PClassDescriptorForType<class Phyre::PHierarchy::POctreeWorld>` | 7 |
| `00647650` | `PPostProcessing::PGlow` | 0 | `00877500` | `PClassDescriptorAbstract<class Phyre::PHierarchy::POctreeWorld>` | 7 |
| `006476F0` | `PPostProcessing::PGlowBase` | 0 | `00877560` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PHierarchy::POctreeWorld>` | 10 |
| `00647780` | `PPostProcessing::PGlowD3D11` | 0 | `00877580` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PHierarchy::POctreeWorld>` | 7 |
| `00647820` | `PPostProcessing::PGlowGPUBase` | 0 | `008776A0` | `PClassDescriptorForType<class Phyre::PHierarchy::POctreeData>` | 7 |
| `006478C0` | `PPostProcessing::PLowResParticles` | 0 | `00877730` | `PClassDescriptorAbstract<class Phyre::PHierarchy::POctreeData>` | 7 |
| `00647950` | `PPostProcessing::PMLAA` | 0 | `00877790` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PHierarchy::POctreeData>` | 10 |
| `006479F0` | `PPostProcessing::PMLAABase` | 0 | `008777E0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PHierarchy::POctreeData>` | 7 |
| `00647A90` | `PPostProcessing::PMLAAD3D11` | 0 | `008778F0` | `PClassDescriptorForType<class Phyre::PHierarchy::POctree>` | 7 |
| `00647B30` | `PPostProcessing::PMaterialPostEffect` | 0 | `00877980` | `PClassDescriptorAbstract<class Phyre::PHierarchy::POctree>` | 7 |
| `00647BC0` | `PPostProcessing::PMeshParticleSystemBase` | 0 | `008779E0` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PHierarchy::POctree>` | 10 |
| `00647C50` | `PPostProcessing::PMotionBlur` | 0 | `00877A30` | `PClassDescriptorWithoutDefaultConstructor<class Phyre::PHierarchy::POctree>` | 7 |
| `00647CB0` | `PPostProcessing::PMotionBlurBase` | 0 | `00877B50` | `PClassDescriptorForType<class Phyre::PHierarchy::POctreeChildren>` | 7 |
| `00647D40` | `PPostProcessing::PMotionBlurD3D11` | 0 | `00879490` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputChannelSemantic>` | 7 |
| `00647DA0` | `PPostProcessing::PPostEffectBase` | 0 | `008794F0` | `PInputs::PInputChannelSemantic` | 0 |
| `00647E30` | `PPostProcessing::PScreenSpaceAmbientOcclusion` | 0 | `00879670` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputChannelSemantic>` | 10 |
| `00647EC0` | `PPostProcessing::PScreenSpaceAmbientOcclusionBase` | 0 | `00879760` | `PNamedSemanticDescriptorForType<class Phyre::PInputs::PInputChannelSemantic>` | 9 |
| `00647F50` | `PPostProcessing::PScreenSpaceAmbientOcclusionD3D11` | 0 | `00879890` | `PClassDescriptorForType<class Phyre::PGame::PGameConfig>` | 7 |
| `00647FE0` | `PPostProcessing::PScreenSpaceReflection` | 0 | `00879920` | `PClassDescriptorAbstract<class Phyre::PGame::PGameConfig>` | 7 |
| `00648040` | `PPostProcessing::PScreenSpaceReflectionBase` | 0 | `008799A0` | `PClassDescriptorConcrete<class Phyre::PGame::PGameConfig>` | 3 |
| `006480A0` | `PPostProcessing::PScreenSpaceReflectionD3D11` | 0 | `008799D0` | `PClassDescriptorConcrete<class Phyre::PGame::PGameConfig>` | 7 |
| `006506A0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPostProcessing::PPostEffectManager,class Phyre::PBase * __ptr64,unsigned int>` | 1 | `00879B80` | `PClassDataMemberArrayDynamic<class Phyre::PArray<class Phyre::PInputs::PInputMap * __ptr64,8> >` | 0 |
| `00650750` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPostProcessing::PPostEffectManager,class Phyre::PClassDescriptor const * __ptr64,unsigned int>` | 1 | `00879BE0` | `PClassDataMemberPhyreArray<class Phyre::PInputs::PInputMap * __ptr64>` | 0 |
| `00650800` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPostProcessing::PPostEffectManager,class Phyre::PTypedObject,unsigned int>` | 1 | `00879C40` | `PClassDescriptorAbstract<class Phyre::PArray<class Phyre::PInputs::PInputMap * __ptr64,8> >` | 7 |
| `00653950` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPostProcessing::PPostEffectManager,class Phyre::PBase * __ptr64,unsigned int>` | 4 | `00879CA0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PInputs::PInputMap * __ptr64,8> >` | 7 |
| `006539E0` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPostProcessing::PPostEffectManager,class Phyre::PClassDescriptor const * __ptr64,unsigned int>` | 4 | `00879D00` | `PClassDescriptorForType<class Phyre::PArray<class Phyre::PInputs::PInputMap * __ptr64,8> >` | 7 |
| `00653A70` | `PInternal::PCallerImplementation::PCallerImplementation1::PMethodCallerConcrete<class Phyre::PPostProcessing::PPostEffectManager,class Phyre::PTypedObject,unsigned int>` | 4 | `0087A6C0` | `PClassDataMemberPhyreArray<class Phyre::PInputs::PInputMap * __ptr64>` | 9 |
| `00653B00` | `PClassDataMemberPhyreArray<class Phyre::PPostProcessing::PPostEffectBase * __ptr64>` | 9 | `0087A6F0` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PInputs::PInputMap * __ptr64,8> >` | 3 |
| `00653C60` | `PClassDescriptorConcrete<class Phyre::PArray<class Phyre::PPostProcessing::PPostEffectBase * __ptr64,8> >` | 3 | `0087AE00` | `PHierarchy::PUtilityHierarchy` | 1 |
| `00654830` | `PPostProcessing::PUtilityPostProcessing` | 1 | `0087AE80` | `PHierarchy::PUtilityHierarchy` | 2 |
| `00655920` | `PPostProcessing::PAtmospherics` | 1 | | | |

### SQEX — 353 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `0021F080` | `Sd::Driver::BankCallback` | 0 | `007DDCD0` | `Sd::Driver::WASAPI::MockDevice` | 5 |
| `006793B0` | `Sd::Driver::ExternalVoiceCallback` | 0 | `007DDCE0` | `Sd::Driver::WASAPI::WASAPIDevice` | 5 |
| `007A9820` | `Sd::DynamicValue<0>` | 0 | `007DDCF0` | `Sd::Driver::WASAPI::MockDevice` | 7 |
| `007A98E0` | `Sd::FixedList<0,class SQEX::Sd::SeadHandle>` | 0 | `007DDD00` | `Sd::Driver::WASAPI::WASAPIDevice` | 7 |
| `007A9980` | `Sd::SeadObject<0,8>` | 0 | `007DDE00` | `Sd::Driver::WASAPI::MockDevice` | 9 |
| `007A99C0` | `Sd::Driver::Category` | 0 | `007DDE10` | `Sd::Driver::WASAPI::WASAPIDevice` | 9 |
| `007AB080` | `Sd::FixedQueue<0,struct SQEX::Sd::Driver::ACTION * __ptr64>` | 0 | `007DDEC0` | `Sd::Driver::WASAPI::WASAPIDevice` | 8 |
| `007AB120` | `Sd::FixedQueue<0,struct SQEX::Sd::Driver::ACTION * __ptr64>::NODE` | 0 | `007DE120` | `Sd::Driver::WASAPI::MockDevice` | 1 |
| `007AC158` | `Sd::Driver::EmptyEffect` | 0 | `007DE2F0` | `Sd::Driver::WASAPI::WASAPIDevice` | 1 |
| `007AC200` | `Sd::SeadObject<2,16>` | 0 | `007DEEF0` | `Sd::Driver::WASAPI::WASAPIDevice` | 6 |
| `007AC240` | `Sd::Driver::Audio` | 0 | `007DEFA0` | `Sd::Driver::WASAPI::AudioRenderer` | 0 |
| `007AC280` | `Sd::Driver::Audio::Bus` | 0 | `007DEFB0` | `Sd::Driver::WASAPI::WASAPIDevice` | 9 |
| `007AC2E0` | `Sd::Driver::EmptyEffect` | 0 | `007DF1F0` | `Sd::Driver::WASAPI::WASAPIDevice` | 8 |
| `007AC330` | `Sd::Driver::Core::ICoreEffect` | 0 | `007DF320` | `Sd::Driver::WASAPI::WASAPIDevice` | 0 |
| `007AE430` | `Sd::NameBuffer::NODE` | 0 | `007DF328` | `Sd::Driver::WASAPI::WASAPIDevice` | 0 |
| `007AE600` | `Sd::FixedList<1,class SQEX::Sd::Driver::Core::CoreSourceVoice * __ptr64>` | 0 | `007DF4EC` | `Sd::Driver::WASAPI::WASAPIDevice` | 2 |
| `007AE6A0` | `Sd::FixedList<1,class SQEX::Sd::Driver::Core::CoreSubmixVoice * __ptr64>` | 0 | `007DF500` | `Sd::Driver::WASAPI::MockDevice` | 6 |
| `007AE740` | `Sd::List<1,class SQEX::Sd::Driver::Core::CoreSourceVoice * __ptr64>` | 0 | `007DF550` | `Sd::Driver::WASAPI::WASAPIDevice` | 6 |
| `007AE8B0` | `Sd::SeadObject<1,8>` | 0 | `007DF5A0` | `Sd::Driver::WASAPI::MockDevice` | 4 |
| `007AE8F0` | `Sd::List<1,class SQEX::Sd::Driver::Core::CoreSourceVoice * __ptr64>::NODE` | 0 | `007DF5B0` | `Sd::Driver::WASAPI::WASAPIDevice` | 4 |
| `007B13E0` | `Sd::HashTable` | 0 | `007DF5C0` | `Sd::Driver::WASAPI::MockDevice` | 2 |
| `007B1420` | `Sd::FixedList<0,class SQEX::Sd::Driver::StreamingBank * __ptr64>` | 0 | `007DF5E0` | `Sd::Driver::WASAPI::WASAPIDevice` | 2 |
| `007B1520` | `Sd::FixedList<0,class SQEX::Sd::Driver::Bank * __ptr64>` | 0 | `007DF5F0` | `Sd::Driver::WASAPI::MockDevice` | 3 |
| `007B2B30` | `Sd::FixedList<0,class SQEX::Sd::Driver::Sound * __ptr64>` | 0 | `007DF610` | `Sd::Driver::WASAPI::WASAPIDevice` | 3 |
| `007B4D60` | `Sd::FixedList<0,class SQEX::Sd::Driver::Sequence * __ptr64>` | 0 | `007DF970` | `Sd::SeadObject<1,16>` | 0 |
| `007B54B0` | `Sd::FixedList<0,class SQEX::Sd::Driver::Track * __ptr64>` | 0 | `007DF9B0` | `Sd::Driver::Core::CoreMasterVoice` | 0 |
| `007B5C50` | `Sd::FixedList<0,class SQEX::Sd::Driver::Voice * __ptr64>` | 0 | `007DFA60` | `Sd::Driver::Core::CoreMasterVoice` | 2 |
| `007B61C0` | `Sd::FixedList<0,class SQEX::Sd::Driver::Event * __ptr64>` | 0 | `007DFA70` | `Sd::Driver::Core::CoreMasterVoice` | 3 |
| `007B6258` | `Sd::Driver::EventData` | 0 | `007DFB00` | `Sd::Driver::Core::CoreMasterVoice` | 5 |
| `007B6270` | `Sd::Driver::EventData` | 0 | `007DFF00` | `Sd::Driver::Core::CoreMasterVoice` | 6 |
| `007B62D0` | `Sd::IHashObject` | 0 | `007DFFF0` | `Sd::Driver::Core::CoreSubmixVoice` | 0 |
| `007B6300` | `Sd::Driver::EventData` | 1 | `007E0050` | `Sd::Driver::Core::CoreSubmixVoice` | 2 |
| `007B7110` | `Sd::FixedList<4,class SQEX::Sd::Magi::Music * __ptr64>` | 0 | `007E0060` | `Sd::Driver::Core::CoreSubmixVoice` | 4 |
| `007B7270` | `Sd::SeadObject<4,8>` | 0 | `007E0070` | `Sd::Driver::Core::CoreSubmixVoice` | 3 |
| `007B7F30` | `Sd::FixedList<4,class SQEX::Sd::Magi::Instrument * __ptr64>` | 0 | `007E0100` | `Sd::Driver::Core::CoreSubmixVoice` | 5 |
| `007B8EFC` | `Sd::Driver::ExternalSourceVoice` | 0 | `007E0620` | `Sd::Driver::Core::CoreSubmixVoice` | 6 |
| `007B8F08` | `Sd::Driver::ExternalSourceVoice` | 0 | `007E07A0` | `Sd::Driver::Core::CoreSourceVoice` | 0 |
| `007B8F20` | `Sd::Driver::ExternalSourceVoice` | 0 | `007E07F0` | `Sd::Driver::Core::CoreSourceVoice` | 5 |
| `007B8F70` | `Sd::Driver::Core::ICoreSourceVoiceCallback` | 0 | `007E0860` | `Sd::Driver::Core::CoreSourceVoice` | 12 |
| `007B8FA0` | `Sd::Driver::IExternalSourceVoice` | 0 | `007E0870` | `Sd::Driver::Core::CoreSourceVoice` | 14 |
| `007B8FD0` | `Sd::Driver::ExternalSourceVoice` | 6 | `007E0880` | `Sd::Driver::Core::CoreSourceVoice` | 11 |
| `007B9010` | `Sd::Driver::ExternalSourceVoice` | 2 | `007E0920` | `Sd::Driver::Core::CoreSourceVoice` | 2 |
| `007B93A0` | `Sd::Driver::ExternalSourceVoice` | 1 | `007E0930` | `Sd::Driver::Core::CoreSourceVoice` | 13 |
| `007B93E0` | `Sd::Driver::ExternalSourceVoice` | 1 | `007E0940` | `Sd::Driver::Core::CoreSourceVoice` | 15 |
| `007B9770` | `Sd::Driver::ExternalSourceVoice` | 5 | `007E0970` | `Sd::Driver::Core::CoreSourceVoice` | 10 |
| `007B9910` | `Sd::Driver::ExternalSourceVoice` | 3 | `007E0A40` | `Sd::Driver::Core::CoreSourceVoice` | 9 |
| `007B9930` | `Sd::Driver::ExternalSourceVoice` | 4 | `007E25A0` | `Sd::Driver::Core::CoreSourceVoice` | 8 |
| `007BA990` | `Sd::FixedQueue<3,struct SQEX::Sd::Lay::ACTION * __ptr64>` | 0 | `007E2640` | `Sd::Driver::Core::CoreSourceVoice` | 7 |
| `007BAA30` | `Sd::FixedQueue<3,struct SQEX::Sd::Lay::ACTION * __ptr64>::NODE` | 0 | `007E26B0` | `Sd::Driver::Core::CoreSourceVoice` | 16 |
| `007BAAF0` | `Sd::SeadObject<3,8>` | 0 | `007E26E0` | `Sd::Driver::Core::CoreSourceVoice` | 6 |
| `007BB8B0` | `Sd::FixedList<3,class SQEX::Sd::SeadHandle>` | 0 | `007E2710` | `Sd::Driver::Core::CoreSourceVoice` | 3 |
| `007BB950` | `Sd::Lay::Page` | 0 | `007E2760` | `Sd::Driver::Core::CoreSourceVoice` | 4 |
| `007BBE50` | `Sd::FixedList<3,class SQEX::Sd::Lay::SoundObject * __ptr64>` | 0 | `007E29F4` | `Sd::Driver::OnMemoryBank` | 0 |
| `007BCEF8` | `Sd::Driver::Sound` | 0 | `007E2A00` | `Sd::Driver::OnMemoryBank` | 0 |
| `007BCF04` | `Sd::Driver::Sound` | 0 | `007E2A70` | `Sd::Driver::OnMemoryBank` | 7 |
| `007BCFA0` | `Sd::CurvedDynamicValue<0>` | 0 | `007E2A90` | `Sd::Driver::OnMemoryBank` | 6 |
| `007BCFF0` | `Sd::Driver::ISound` | 0 | `007E2AB0` | `Sd::Driver::OnMemoryBank` | 5 |
| `007BD020` | `Sd::Driver::Sound` | 0 | `007E2AD0` | `Sd::Driver::OnMemoryBank` | 8 |
| `007C1284` | `Sd::Magi::Music` | 0 | `007E2D74` | `Sd::Driver::StreamingBank` | 0 |
| `007C1290` | `Sd::FixedList<4,struct SQEX::Sd::Magi::TimingCallback>::NODE` | 0 | `007E2D80` | `Sd::Driver::StreamingBank` | 0 |
| `007C14A0` | `Sd::CurvedDynamicValue<4>` | 0 | `007E2D90` | `Sd::Driver::StreamingBank::AudioStream` | 0 |
| `007C14F0` | `Sd::DynamicValue<4>` | 0 | `007E2E00` | `Sd::Driver::IDelegate` | 0 |
| `007C1530` | `Sd::FixedList<4,struct SQEX::Sd::Magi::TimingCallback>` | 0 | `007E2E30` | `Sd::Driver::StreamingBank` | 0 |
| `007C15D0` | `Sd::Magi::Music` | 0 | `007E2E80` | `Sd::Driver::StreamingBank` | 7 |
| `007C5A50` | `Sd::Magi::Music` | 24 | `007E3120` | `Sd::Driver::StreamingBank` | 6 |
| `007C5A60` | `Sd::Magi::Music` | 33 | `007E3230` | `Sd::Driver::StreamingBank` | 5 |
| `007C5E50` | `Sd::Magi::Music` | 22 | `007E32E0` | `Sd::Driver::StreamingBank` | 8 |
| `007C61E0` | `Sd::Magi::Music` | 29 | `007E3CF0` | `Sd::Driver::StreamingBank` | 1 — interior read 2026-09-17 (SWE2-FRONTIER): 1,284 B, `"data type is invalid!!"`/`"stream data is invalid!!"` errors, `0019C5D0` ×3, first call at [`007E3D4A`](../../_index/ADDRESS-INDEX.md) |
| `007C61F0` | `Sd::Magi::Music` | 28 | `007E4200` | `Sd::Driver::StreamingBank` | 4 |
| `007C6360` | `Sd::Magi::Music` | 23 | `007E4260` | `Sd::Driver::StreamingBank` | 2 |
| `007C6370` | `Sd::Magi::Music` | 27 | `007E4300` | `Sd::Driver::StreamingBank` | 3 |
| `007C65A0` | `Sd::Magi::Music` | 35 | `007E5040` | `Sd::Driver::StreamingBank` | 10 |
| `007C65B0` | `Sd::Magi::Music` | 25 | `007E50D8` | `Sd::Driver::RandomSound` | 0 |
| `007C68B0` | `Sd::Magi::Music` | 21 | `007E50E4` | `Sd::Driver::RandomSound` | 0 |
| `007C6C70` | `Sd::Magi::Music` | 26 | `007E50F0` | `Sd::Driver::RandomSound` | 0 |
| `007C6DA0` | `Sd::Magi::Music` | 30 | `007E5160` | `Sd::Driver::RandomSound` | 43 |
| `007C6DB0` | `Sd::Magi::Music` | 34 | `007E5724` | `Sd::Driver::VariationSound` | 0 |
| `007C8890` | `Sd::Magi::Music` | 4 | `007E5730` | `Sd::Driver::VariationSound` | 0 |
| `007C8CD0` | `Sd::Magi::Music` | 15 | `007E5740` | `Sd::Driver::VariationSound` | 0 |
| `007C9150` | `Sd::Magi::Music` | 6 | `007E57C0` | `Sd::Driver::VariationSound` | 36 |
| `007C9170` | `Sd::Magi::Music` | 5 | `007E57D0` | `Sd::Driver::VariationSound` | 40 |
| `007C9190` | `Sd::Magi::Music` | 16 | `007E5848` | `Sd::Driver::OrderSound` | 0 |
| `007C91A0` | `Sd::Magi::Music` | 14 | `007E5854` | `Sd::Driver::OrderSound` | 0 |
| `007C91C0` | `Sd::Magi::Music` | 12 | `007E5860` | `Sd::Driver::OrderSound` | 0 |
| `007C92D0` | `Sd::Magi::Music` | 13 | `007E58D0` | `Sd::Driver::OrderSound` | 43 |
| `007CA350` | `Sd::Magi::Music` | 10 | `007E5D14` | `Sd::Driver::CycleSound` | 0 |
| `007CA370` | `Sd::Magi::Music` | 9 | `007E5D20` | `Sd::Driver::CycleSound` | 0 |
| `007CA420` | `Sd::Magi::Music` | 8 | `007E5D30` | `Sd::Driver::CycleSound` | 0 |
| `007CA650` | `Sd::Magi::Music` | 7 | `007E6360` | `Sd::Driver::CycleSound` | 43 |
| `007CA730` | `Sd::Magi::Music` | 11 | `007E65B0` | `Sd::Driver::CycleSound` | 40 |
| `007CA750` | `Sd::Magi::Music` | 18 | `007E6620` | `Sd::Driver::CycleSound` | 42 |
| `007CA9E0` | `Sd::Magi::Music` | 2 | `007E6738` | `Sd::Driver::SwitchSound` | 0 |
| `007CA9F0` | `Sd::Magi::Music` | 3 | `007E6744` | `Sd::Driver::SwitchSound` | 0 |
| `007CFFF0` | `Sd::MabFile` | 0 | `007E6750` | `Sd::Driver::SwitchSound` | 0 |
| `007D0828` | `Sd::Driver::Bank` | 0 | `007E67C0` | `Sd::Driver::SwitchSound` | 43 |
| `007D0840` | `Sd::Driver::Bank` | 0 | `007E6A50` | `Sd::Driver::Sequence` | 0 |
| `007D09B0` | `Sd::Driver::Bank` | 8 | `007E7DB0` | `Sd::Driver::Track` | 0 |
| `007D0C38` | `Sd::Driver::Filter` | 0 | `007E8890` | `Sd::Driver::Track` | 2 |
| `007D0C50` | `Sd::DynamicValue<2>` | 0 | `007E9270` | `Sd::Driver::MaterialTrack` | 0 |
| `007D0C90` | `Sd::SeadObject<2,8>` | 0 | `007E92D0` | `Sd::Driver::MaterialTrack` | 8 |
| `007D0CD0` | `Sd::Driver::Filter` | 0 | `007E9310` | `Sd::Driver::MaterialTrack` | 4 |
| `007D1430` | `Sd::Driver::Filter` | 3 | `007E9340` | `Sd::Driver::MaterialTrack` | 13 |
| `007D14D0` | `Sd::Driver::Filter` | 3 | `007E9380` | `Sd::Driver::MaterialTrack` | 16 |
| `007D1840` | `Sd::Driver::Filter` | 2 | `007E93C0` | `Sd::Driver::MaterialTrack` | 11 |
| `007D1970` | `Sd::Driver::Filter` | 6 | `007E9410` | `Sd::Driver::MaterialTrack` | 12 |
| `007D1A10` | `Sd::Driver::Filter` | 5 | `007E9460` | `Sd::Driver::MaterialTrack` | 9 |
| `007D1C80` | `Sd::Driver::Filter` | 8 | `007E94B0` | `Sd::Driver::MaterialTrack` | 10 |
| `007D319C` | `Sd::Driver::SurroundReverb` | 0 | `007E9500` | `Sd::Driver::MaterialTrack` | 7 |
| `007D31B0` | `Sd::Driver::SurroundReverb` | 0 | `007E9580` | `Sd::Driver::MaterialTrack` | 6 |
| `007D3560` | `Sd::Driver::SurroundReverb` | 3 — interior read 2026-09-17 (SWE2-FRONTIER): 1,356 B, `007A9E00` first call at [`007D3595`](../../_index/ADDRESS-INDEX.md) | `007E95D0` | `Sd::Driver::MaterialTrack` | 5 |
| `007D3C90` | `Sd::Driver::SurroundReverb` | 3 | `007E9620` | `Sd::Driver::MaterialTrack` | 14 |
| `007D5BD0` | `Sd::Driver::SurroundReverb` | 2 | `007E9660` | `Sd::Driver::MaterialTrack` | 15 |
| `007D5F50` | `Sd::Driver::SurroundReverb` | 6 | `007E96A0` | `Sd::Driver::MaterialTrack` | 2 |
| `007D6270` | `Sd::Driver::SurroundReverb` | 5 | `007E9970` | `Sd::Driver::MaterialTrack` | 3 |
| `007D76E0` | `Sd::Driver::SurroundReverb` | 8 | `007E9A10` | `Sd::Driver::SoundTrack` | 0 |
| `007D816C` | `Sd::Driver::SideChainInput` | 0 | `007E9A70` | `Sd::Driver::SoundTrack` | 8 |
| `007D8180` | `Sd::Driver::SideChainInput` | 0 | `007E9AB0` | `Sd::Driver::SoundTrack` | 4 |
| `007D8220` | `Sd::Driver::SideChainInput` | 3 | `007E9AE0` | `Sd::Driver::SoundTrack` | 13 |
| `007D82B0` | `Sd::Driver::SideChainInput` | 3 | `007E9B30` | `Sd::Driver::SoundTrack` | 16 |
| `007D8500` | `Sd::Driver::SideChainInput` | 2 | `007E9B70` | `Sd::Driver::SoundTrack` | 11 |
| `007D8540` | `Sd::Driver::SideChainInput` | 6 | `007E9BD0` | `Sd::Driver::SoundTrack` | 12 |
| `007D8580` | `Sd::Driver::SideChainInput` | 8 | `007E9C30` | `Sd::Driver::SoundTrack` | 9 |
| `007D8A10` | `Sd::Driver::Compressor` | 0 | `007E9C80` | `Sd::Driver::SoundTrack` | 10 |
| `007D8A20` | `Sd::Driver::Compressor` | 0 | `007E9CD0` | `Sd::Driver::SoundTrack` | 7 |
| `007D8A70` | `Sd::Driver::Compressor` | 3 | `007E9D40` | `Sd::Driver::SoundTrack` | 6 |
| `007D8BB0` | `Sd::Driver::Compressor` | 3 | `007E9D90` | `Sd::Driver::SoundTrack` | 5 |
| `007D8E40` | `Sd::Driver::Compressor` | 2 | `007E9DE0` | `Sd::Driver::SoundTrack` | 14 |
| `007D8F70` | `Sd::Driver::Compressor` | 6 | `007E9E20` | `Sd::Driver::SoundTrack` | 15 |
| `007D9070` | `Sd::Driver::Compressor` | 5 | `007E9E60` | `Sd::Driver::SoundTrack` | 2 |
| `007D9200` | `Sd::Driver::Compressor` | 8 | `007EA37C` | `Sd::Driver::Voice` | 0 |
| `007D9624` | `Sd::Driver::SimpleFilter` | 0 | `007EA388` | `Sd::Driver::Voice` | 0 |
| `007D9630` | `Sd::Driver::SimpleFilter` | 0 | `007EA3A0` | `Sd::SeadObject<0,16>` | 0 |
| `007D9690` | `Sd::Driver::SimpleFilter` | 3 | `007EA3E0` | `Sd::Driver::CRI::IHCAMixerVoiceInputVoice` | 0 |
| `007D9740` | `Sd::Driver::SimpleFilter` | 3 | `007EA410` | `Sd::Driver::Voice` | 0 |
| `007D97F0` | `Sd::Driver::SimpleFilter` | 2 | `007EBA70` | `Sd::Driver::Voice` | 1 |
| `007D98F0` | `Sd::Driver::SimpleFilter` | 8 | `007ED4C0` | `Sd::Driver::Voice` | 1 |
| `007D9AF0` | `Sd::Driver::Flanger` | 0 | `007ED580` | `Sd::Driver::Voice` | 2 |
| `007D9B00` | `Sd::Driver::Flanger` | 0 | `007EDA30` | `Sd::Driver::Voice` | 2 |
| `007D9B70` | `Sd::Driver::Flanger` | 3 | `007EE940` | `Sd::Driver::Event` | 0 |
| `007D9C20` | `Sd::Driver::Flanger` | 1 | `007EF160` | `Sd::SeadObject<3,16>` | 0 |
| `007D9C30` | `Sd::Driver::Flanger` | 3 | `007EF1A0` | `Sd::Lay::Listener` | 0 |
| `007D9DF0` | `Sd::Driver::Flanger` | 2 | `007EFA70` | `Sd::Lay::SoundSourceObject` | 0 |
| `007D9EA0` | `Sd::Driver::Flanger` | 8 | `007F1030` | `Sd::Lay::DynamicSound` | 0 |
| `007DA14C` | `Sd::Driver::GranularPitchShift` | 0 | `007F1090` | `Sd::Lay::DynamicSound` | 16 |
| `007DA160` | `Sd::Driver::GranularPitchShift` | 0 | `007F10F0` | `Sd::Lay::DynamicSound` | 35 |
| `007DA1C0` | `Sd::Driver::GranularPitchShift` | 3 | `007F1200` | `Sd::Lay::DynamicSound` | 33 |
| `007DA2A0` | `Sd::Driver::GranularPitchShift` | 1 | `007F1220` | `Sd::Lay::DynamicSound` | 7 |
| `007DA2B0` | `Sd::Driver::GranularPitchShift` | 3 | `007F1300` | `Sd::Lay::DynamicSound` | 36 |
| `007DA8A0` | `Sd::Driver::GranularPitchShift` | 2 | `007F1310` | `Sd::Lay::DynamicSound` | 15 |
| `007DA970` | `Sd::Driver::GranularPitchShift` | 5 | `007F1340` | `Sd::Lay::DynamicSound` | 34 |
| `007DAA00` | `Sd::Driver::GranularPitchShift` | 8 | `007F1630` | `Sd::Lay::DynamicSound` | 14 |
| `007DABC4` | `Sd::Driver::HilbertFilter` | 0 | `007F1670` | `Sd::Lay::DynamicSound` | 10 |
| `007DABD0` | `Sd::Driver::HilbertFilter` | 0 | `007F17B0` | `Sd::Lay::PointSound` | 0 |
| `007DAC30` | `Sd::Driver::HilbertFilter` | 3 | `007F1810` | `Sd::Lay::PointSound` | 16 |
| `007DACB0` | `Sd::Driver::HilbertFilter` | 1 | `007F1850` | `Sd::Lay::PointSound` | 35 |
| `007DACC0` | `Sd::Driver::HilbertFilter` | 3 | `007F1960` | `Sd::Lay::PointSound` | 7 |
| `007DAED0` | `Sd::Driver::HilbertFilter` | 2 | `007F1A40` | `Sd::Lay::PointSound` | 36 |
| `007DAF70` | `Sd::Driver::HilbertFilter` | 8 | `007F1A50` | `Sd::Lay::PointSound` | 34 |
| `007DB744` | `Sd::Driver::BuildReverb` | 0 | `007F1C80` | `Sd::Lay::AmbientSound` | 0 |
| `007DB750` | `Sd::Driver::BuildReverb` | 0 | `007F1CE0` | `Sd::Lay::AmbientSound` | 35 |
| `007DB7A0` | `Sd::Driver::BuildReverb` | 3 | `007F1D10` | `Sd::Lay::AmbientSound` | 34 |
| `007DB8C0` | `Sd::Driver::BuildReverb` | 1 | `007F1D70` | `Sd::Lay::DirectionSound` | 0 |
| `007DB8D0` | `Sd::Driver::BuildReverb` | 3 | `007F1DD0` | `Sd::Lay::DirectionSound` | 35 |
| `007DC0E0` | `Sd::Driver::BuildReverb` | 4 | `007F1EC0` | `Sd::Lay::DirectionSound` | 7 |
| `007DC1F0` | `Sd::Driver::BuildReverb` | 2 | `007F1F80` | `Sd::Lay::DirectionSound` | 34 |
| `007DC340` | `Sd::Driver::BuildReverb` | 6 | `007F2020` | `Sd::Lay::PolygonSound` | 0 |
| `007DC4A0` | `Sd::Driver::BuildReverb` | 5 | `007F2080` | `Sd::Lay::PolygonSound` | 16 |
| `007DC8A4` | `Sd::Driver::CRI::HCAMixerVoice` | 0 | `007F20E0` | `Sd::Lay::PolygonSound` | 35 |
| `007DC8B0` | `Sd::FixedList<5,struct SQEX::Sd::Driver::CRI::HCAMixerVoice::INPUTVOICELISTITEM>::NODE` | 0 | `007F24F0` | `Sd::Lay::PolygonSound` | 7 |
| `007DC970` | `Sd::FixedList<5,struct SQEX::Sd::Driver::CRI::HCAMixerVoice::INPUTVOICELISTITEM>` | 0 | `007F25D0` | `Sd::Lay::PolygonSound` | 36 |
| `007DCA10` | `Sd::SeadObject<5,8>` | 0 | `007F25E0` | `Sd::Lay::PolygonSound` | 34 |
| `007DCA50` | `Sd::Driver::CRI::HCAMixerVoice` | 0 | `007F7390` | `Sd::Lay::SoundObject` | 0 |
| `007DD040` | `Sd::Driver::CRI::HCAMixerVoice` | 1 | `007F73D0` | `Sd::Lay::SoundObject` | 9 |
| `007DD4C0` | `Sd::Driver::WASAPI::AudioRenderer` | 0 | `007F7400` | `Sd::Lay::SoundObject` | 8 |
| `007DD510` | `Sd::Driver::WASAPI::MockDevice` | 0 | `007F7420` | `Sd::Lay::SoundObject` | 7 |
| `007DD5A0` | `Sd::Driver::WASAPI::WASAPIDevice` | 0 | `008024E0` | `Sd::Driver::WASAPI::MockDevice` | 8 |
| `007DD5F0` | `Sd::Driver::WASAPI::WASAPIDevice` | 1 | | | |

### PPFX — 240 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `006DA8D0` | `CPfxMemoryAllocator` | 1 | `0077E0B0` | `CDepthOfField` | 3 |
| `006DA8E0` | `CPfxMemoryAllocator` | 2 | `0077F5B0` | `CDepthOfField` | 4 |
| `006DFEC0` | `IPfxBaseContext` | 3 | `00780B70` | `CTextureLuminance` | 0 |
| `006DFF00` | `IPfxContext_Dx11` | 3 | `00780BB0` | `CTextureLuminance` | 1 |
| `006E0410` | `IPfxAbstractInterface` | 3 | `00780C40` | `CTextureLuminance` | 2 |
| `006E0440` | `IPfxInterface` | 3 | `00780C70` | `CTextureLuminance` | 3 |
| `006E10B0` | `IPfxBaseRenderToTexture` | 3 | `007819F0` | `CTextureLuminanceManage` | 0 |
| `006E10F0` | `IPfxRenderToTexture_Dx11` | 3 | `00781B00` | `CTextureLuminanceManage` | 1 |
| `0071F0A0` | `VerifyFeatureLicense` | 0 | `00781B30` | `CTextureLuminanceManage` | 2 |
| `0071F0E0` | `membuf` | 0 | `00781B70` | `CTextureLuminanceManage` | 3 |
| `007214A0` | `CRenderTexture` | 0 | `00781C40` | `CTextureLuminance` | 4 |
| `007215C0` | `CRenderTexture` | 5 — interior read 2026-09-17 (SWE2-FRONTIER): 1,349 B, `GPURenderTexture.cpp` diagnostics, `007271C0` first call at [`007215DA`](../../_index/ADDRESS-INDEX.md) | `00781CA0` | `CTextureLuminanceManage` | 4 |
| `00721B10` | `CRenderTexture` | 1 — interior read 2026-09-17 (SWE2-FRONTIER): 1,298 B, `02EA18B1` gate byte at [`00721B4A`](../../_index/ADDRESS-INDEX.md), `1.0f` constant `01CEBBA8` | `00783A10` | `MacAddress` | 0 |
| `00722030` | `CRenderTexture` | 2 | `007851F0` | `IGPUResource` | 2 |
| `00722060` | `CRenderTexture` | 3 | `00785C90` | `IGPUSurface` | 7 |
| `00723380` | `CRenderTexture` | 4 | `00785EE0` | `IGPUSurface` | 8 |
| `00724900` | `IGPUDevice` | 3 | `00785FA0` | `IGPUSurface` | 4 |
| `00724930` | `IGPUDevice` | 4 | `00785FD0` | `IGPUSurface` | 6 |
| `00724940` | `IGPUDevice` | 5 | `00786060` | `IGPUSurface` | 9 |
| `007249E0` | `IGPUDevice` | 6 | `007860B0` | `IGPUSurface` | 10 |
| `007249F0` | `IGPUDevice` | 7 | `00786110` | `IGPUSurface` | 11 |
| `00724A00` | `IGPUDevice` | 8 | `007861A0` | `IGPUSurface` | 12 |
| `00724A60` | `IGPUDevice` | 9 | `00786410` | `IGPUSurface` | 13 |
| `00724AB0` | `IGPUDevice` | 10 | `00786940` | `IGPUSurface` | 2 |
| `00724AF0` | `IGPUDevice` | 11 | `00786A70` | `IGPUBaseInterface` | 2 |
| `00724B20` | `IGPUDevice` | 12 | `00786AA0` | `IGPUInterface` | 2 |
| `00724B60` | `IGPUDevice` | 13 | `00786D00` | `IGPUTexture` | 7 |
| `00724BC0` | `IGPUDevice` | 14 | `00786DD0` | `IGPUTexture` | 8 |
| `00724C10` | `IGPUDevice` | 15 | `00787080` | `IGPUTexture` | 9 |
| `00724CD0` | `IGPUDevice` | 16 | `007871F0` | `IGPUTexture` | 20 |
| `00724DB0` | `IGPUDevice` | 18 | `00787230` | `IGPUTexture` | 21 |
| `00724E40` | `IGPUDevice` | 17 | `00787270` | `IGPUTexture` | 6 |
| `00724EA0` | `IGPUDevice` | 19 | `00787780` | `IGPUVolumeTexture` | 7 |
| `00724EB0` | `IGPUDevice` | 20 | `00787790` | `IGPUVolumeTexture` | 8 |
| `00724EC0` | `IGPUDevice` | 21 | `00787930` | `IGPUVolumeTexture` | 9 |
| `00724F50` | `IGPUDevice` | 22 | `00787BD0` | `IGPUBaseTexture` | 2 |
| `00724FE0` | `IGPUDevice` | 23 | `00787C40` | `IGPUCubeTexture` | 2 |
| `00724FF0` | `IGPUDevice` | 24 | `00787CB0` | `IGPUTexture` | 2 |
| `00725080` | `IGPUDevice` | 25 | `00787CF0` | `IGPUVolumeTexture` | 2 |
| `00725090` | `IGPUDevice` | 26 | `00788ED0` | `IGPUBuffer` | 2 |
| `007250A0` | `IGPUDevice` | 27 | `00788F10` | `IGPUIndexBuffer` | 2 |
| `007250B0` | `IGPUDevice` | 28 | `00788F50` | `IGPUInputAttribute` | 2 |
| `007250C0` | `IGPUDevice` | 29 | `00788FB0` | `IGPUVertexBuffer` | 2 |
| `007250D0` | `IGPUDevice` | 30 | `007890C0` | `IGPUBaseQuery` | 3 |
| `007250E0` | `IGPUDevice` | 31 | `007894E0` | `IGPUQueryOcclusion` | 3 |
| `007250F0` | `IGPUDevice` | 32 | `00789560` | `IGPUQueryOcclusion` | 4 |
| `00725100` | `IGPUDevice` | 33 | `00789570` | `IGPUQueryOcclusion` | 5 |
| `00725110` | `IGPUDevice` | 34 | `007895F0` | `IGPUQueryOcclusion` | 11 |
| `00725120` | `IGPUDevice` | 35 | `00789750` | `IGPUBaseQuery` | 2 |
| `00725130` | `IGPUDevice` | 36 | `00789790` | `IGPUQueryOcclusion` | 2 |
| `00725140` | `IGPUDevice` | 37 | `00789B00` | `IGPUEffect` | 5 |
| `00725280` | `IGPUDevice` | 38 | `00789B30` | `IGPUEffect` | 6 |
| `007252A0` | `IGPUDevice` | 39 | `00789B50` | `IGPUEffect` | 7 |
| `00725340` | `IGPUDevice` | 40 | `00789B70` | `IGPUEffect` | 8 |
| `007254A0` | `IGPUDevice` | 41 | `00789B90` | `IGPUEffect` | 9 |
| `007254C0` | `IGPUDevice` | 42 | `00789BB0` | `IGPUEffect` | 10 |
| `007254D0` | `IGPUDevice` | 43 | `00789BC0` | `IGPUEffect` | 11 |
| `00725500` | `IGPUDevice` | 44 | `00789BE0` | `IGPUEffect` | 12 |
| `00725530` | `IGPUDevice` | 45 | `00789C00` | `IGPUEffect` | 13 |
| `00725560` | `IGPUDevice` | 46 | `00789CB0` | `IGPUEffect` | 14 |
| `00725570` | `IGPUDevice` | 47 | `00789CD0` | `IGPUEffect` | 15 |
| `00725590` | `IGPUDevice` | 48 | `00789CF0` | `IGPUEffect` | 16 |
| `007255B0` | `IGPUDevice` | 49 | `00789D10` | `IGPUEffect` | 17 |
| `007255E0` | `IGPUDevice` | 50 | `00789D30` | `IGPUEffect` | 18 |
| `00725760` | `IGPUDevice` | 52 | `00789D50` | `IGPUEffect` | 19 |
| `00725830` | `IGPUDevice` | 51 | `00789D80` | `IGPUEffect` | 20 |
| `007258C0` | `IGPUDevice` | 53 | `00789DA0` | `IGPUEffect` | 21 |
| `00725970` | `IGPUDevice` | 56 | `00789DC0` | `IGPUEffect` | 22 |
| `00725980` | `IGPUDevice` | 57 | `00789DE0` | `IGPUEffect` | 23 |
| `007259D0` | `IGPUDevice` | 58 | `00789E00` | `IGPUEffect` | 24 |
| `00725AA0` | `IGPUDevice` | 61 | `00789E20` | `IGPUEffect` | 25 |
| `00725C80` | `IGPUDevice` | 63 | `00789E40` | `IGPUEffect` | 26 |
| `00725E40` | `IGPUDevice` | 60 | `00789E60` | `IGPUEffect` | 27 |
| `00725FF0` | `IGPUDevice` | 62 | `00789E80` | `IGPUEffect` | 28 |
| `007261B0` | `IGPUDevice` | 64 | `00789EA0` | `IGPUEffect` | 29 |
| `00726360` | `IGPUDevice` | 65 | `00789EC0` | `IGPUEffect` | 30 |
| `00726550` | `IGPUDevice` | 67 | `00789EE0` | `IGPUEffect` | 31 |
| `00726700` | `IGPUDevice` | 66 | `00789F00` | `IGPUEffect` | 32 |
| `007268C0` | `IGPUDevice` | 68 | `00789F20` | `IGPUEffect` | 33 |
| `00726A70` | `IGPUDevice` | 69 | `00789F40` | `IGPUEffect` | 34 |
| `00726C30` | `IGPUDevice` | 70 | `00789F60` | `IGPUEffect` | 35 |
| `00726D00` | `IGPUDevice` | 71 | `00789F80` | `IGPUEffect` | 36 |
| `00726DB0` | `IGPUDevice` | 72 | `00789FA0` | `IGPUEffect` | 37 |
| `00726DD0` | `IGPUDevice` | 73 | `00789FC0` | `IGPUEffect` | 39 |
| `00726E30` | `IGPUDevice` | 74 | `0078A040` | `IGPUEffect` | 40 |
| `00726F00` | `IGPUDevice` | 75 | `0078A470` | `IGPUEffect` | 2 |
| `00726F60` | `IGPUDevice` | 76 | `0078A4B0` | `IGPUEffect` | 38 |
| `007270E0` | `IGPUDevice` | 2 | `0078A4D0` | `IGPUEffect` | 4 |
| `00727120` | `IGPUDevice` | 59 | `0078ACE0` | `IGPUPixelContainer` | 2 |
| `00727140` | `IGPUDevice` | 54 | `0078F960` | `CTinyEffect` | 1 |
| `00727150` | `IGPUDevice` | 55 | `0078F970` | `CTinyEffect` | 2 |
| `007273E0` | `CGPUResourceManage` | 0 | `0078F9F0` | `CTinyEffect` | 3 |
| `00727410` | `CGPUResourceManage` | 1 | `0078FAC0` | `CTinyEffect` | 4 |
| `00727440` | `CGPUResourceManage` | 2 | `0078FAE0` | `CTinyEffect` | 5 |
| `00727450` | `CGPUResourceManage` | 3 | `0078FAF0` | `CTinyEffect` | 6 |
| `00727900` | `CGPUResourceManage` | 4 | `0078FB30` | `CTinyEffect` | 7 |
| `00727980` | `IGPUBaseResourceManage` | 4 | `0078FB90` | `CTinyEffect` | 8 |
| `007307A0` | `CTextureUtil` | 0 | `0078FC10` | `CTinyEffect` | 9 |
| `00731AD0` | `CTextureUtil` | 1 | `0078FC80` | `CTinyEffect` | 10 |
| `00731D00` | `CTextureUtil` | 2 | `0078FCF0` | `CTinyEffect` | 11 |
| `00731D20` | `CTextureUtil` | 3 | `0078FD70` | `CTinyEffect` | 12 |
| `0075ADF0` | `CTextureUtil` | 4 | `0078FDF0` | `CTinyEffect` | 13 |
| `0075C080` | `CRenderTextureArray` | 0 | `0078FE60` | `CTinyEffect` | 14 |
| `0075CAD0` | `CRenderTextureArray` | 1 | `0078FEE0` | `CTinyEffect` | 15 |
| `0075CC10` | `CRenderTextureArray` | 2 | `0078FF50` | `CTinyEffect` | 16 |
| `0075CC50` | `CRenderTextureArray` | 3 | `0078FFD0` | `CTinyEffect` | 17 |
| `0075DE90` | `CRenderTextureArray` | 4 | `00790010` | `CTinyEffect` | 18 |
| `0075EB00` | `CRenderTexturePool` | 0 | `00790020` | `CTinyEffect` | 19 |
| `0075EB80` | `CRenderTexturePool` | 1 | `00790060` | `CTinyEffect` | 20 |
| `0075EBE0` | `CRenderTexturePool` | 2 | `007900A0` | `CTinyEffect` | 21 |
| `0075EC00` | `CRenderTexturePool` | 3 | `007900F0` | `CTinyEffect` | 22 |
| `0075EDC0` | `CRenderTexturePool` | 4 | `00790110` | `CTinyEffect` | 23 |
| `00769430` | `CRenderGlare` | 0 | `00790150` | `CTinyEffect` | 24 |
| `00769470` | `CRenderGlare` | 1 | `00790160` | `CTinyEffect` | 25 |
| `00769600` | `CRenderGlare` | 2 | `007909F0` | `CInheritanceTypedReferenceManager<class PPFX::__CManualProgramParameterTable>` | 0 |
| `00769640` | `CRenderGlare` | 3 — interior read 2026-09-17 (SWE2-FRONTIER): 1,153 B, `006DA8A0` dispatch thunk ×21, `007142F0` first at [`00769660`](../../_index/ADDRESS-INDEX.md) | `00790A20` | `CInheritanceTypedReferenceManager<class PPFX::__CTinyEffect>` | 0 |
| `0076AB60` | `CRenderGlare` | 4 | `00790A50` | `CManualProgramParameterTable` | 0 |
| `0077DE90` | `CDepthOfField` | 0 | `00790A90` | `CTinyEffect` | 0 |
| `0077DED0` | `CDepthOfField` | 1 | `008088EE` | `membuf` | 3 |
| `0077E020` | `CDepthOfField` | 2 | `008088F4` | `membuf` | 6 |

### std — 47 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `00195518` | `basic_ifstream<wchar_t,struct std::char_traits<wchar_t> >` | 0 | `001DE390` | `basic_ostringstream<char,struct std::char_traits<char>,class std::allocator<char> >` | 0 |
| `00195524` | `basic_ofstream<wchar_t,struct std::char_traits<wchar_t> >` | 0 | `001DE39C` | `basic_stringstream<char,struct std::char_traits<char>,class std::allocator<char> >` | 0 |
| `00195530` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 0 | `001DE450` | `basic_stringbuf<char,struct std::char_traits<char>,class std::allocator<char> >` | 0 |
| `00197930` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 14 | `001DFA80` | `basic_stringbuf<char,struct std::char_traits<char>,class std::allocator<char> >` | 3 |
| `00197B40` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 3 | `001DFCF0` | `basic_stringbuf<char,struct std::char_traits<char>,class std::allocator<char> >` | 4 |
| `00197E10` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 4 | `001DFE20` | `basic_stringbuf<char,struct std::char_traits<char>,class std::allocator<char> >` | 10 |
| `001987A0` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 10 | `001DFFC0` | `basic_stringbuf<char,struct std::char_traits<char>,class std::allocator<char> >` | 11 |
| `00198880` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 11 | `001E0390` | `basic_stringbuf<char,struct std::char_traits<char>,class std::allocator<char> >` | 6 |
| `00198ED0` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 12 | `00204AF0` | `_Node_class<char,class std::regex_traits<char> >` | 0 |
| `00198F60` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 13 | `00204B30` | `_Node_str<char>` | 0 |
| `00198FC0` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 7 | `00204B80` | `collate<char>` | 0 |
| `00199320` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 6 | `00204BD0` | `_Node_assert` | 0 |
| `0019B4E8` | `basic_ofstream<char,struct std::char_traits<char> >` | 0 | `00204C70` | `_Node_if` | 0 |
| `0019B500` | `basic_filebuf<char,struct std::char_traits<char> >` | 0 | `00204CB0` | `_Node_rep` | 0 |
| `0019B940` | `basic_filebuf<char,struct std::char_traits<char> >` | 14 | `00204CE0` | `_Root_node` | 0 |
| `0019BAD0` | `basic_filebuf<char,struct std::char_traits<char> >` | 3 | `00209C40` | `collate<char>` | 3 |
| `0019BD80` | `basic_filebuf<char,struct std::char_traits<char> >` | 4 | `00209C90` | `collate<char>` | 5 |
| `0019BE30` | `basic_filebuf<char,struct std::char_traits<char> >` | 10 | `00209CD0` | `collate<char>` | 4 |
| `0019BF10` | `basic_filebuf<char,struct std::char_traits<char> >` | 11 | `00808888` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 5 |
| `0019BFF0` | `basic_filebuf<char,struct std::char_traits<char> >` | 12 | `0080888E` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 8 |
| `0019C0E0` | `basic_filebuf<char,struct std::char_traits<char> >` | 13 | `00808894` | `basic_filebuf<wchar_t,struct std::char_traits<wchar_t> >` | 9 |
| `0019C130` | `basic_filebuf<char,struct std::char_traits<char> >` | 7 | `008088E2` | `collate<char>` | 2 |
| `0019C490` | `basic_filebuf<char,struct std::char_traits<char> >` | 6 | `008088E8` | `collate<char>` | 1 |
| `001DE384` | `basic_istringstream<char,struct std::char_traits<char>,class std::allocator<char> >` | 0 | | | |

### PrimitiveRendererD3D11 — 39 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `006C88A0` | `PrimitiveRendererD3D11` | 0 | `006CAC10` | `PrimitiveRendererD3D11` | 10 |
| `006C8BF0` | `PrimitiveRendererD3D11` | 5 | `006CAC20` | `PrimitiveRendererD3D11` | 27 |
| `006C8C50` | `PrimitiveRendererD3D11` | 4 | `006CAC30` | `PrimitiveRendererD3D11` | 35 |
| `006C9AF0` | `PrimitiveRendererD3D11` | 39 | `006CAC40` | `PrimitiveRendererD3D11` | 26 |
| `006C9B00` | `PrimitiveRendererD3D11` | 37 | `006CAC90` | `PrimitiveRendererD3D11` | 23 |
| `006C9C30` | `PrimitiveRendererD3D11` | 13 | `006CAD30` | `PrimitiveRendererD3D11` | 7 |
| `006CA650` | `PrimitiveRendererD3D11` | 2 | `006CAD50` | `PrimitiveRendererD3D11` | 32 |
| `006CA680` | `PrimitiveRendererD3D11` | 43 | `006CAD90` | `PrimitiveRendererD3D11` | 11 |
| `006CA6F0` | `PrimitiveRendererD3D11` | 41 | `006CADB0` | `PrimitiveRendererD3D11` | 12 |
| `006CA760` | `PrimitiveRendererD3D11` | 0 | `006CADE0` | `PrimitiveRendererD3D11` | 30 |
| `006CA790` | `PrimitiveRendererD3D11` | 34 | `006CAE70` | `PrimitiveRendererD3D11` | 36 |
| `006CA7A0` | `PrimitiveRendererD3D11` | 33 | `006CAE90` | `PrimitiveRendererD3D11` | 9 |
| `006CA7B0` | `PrimitiveRendererD3D11` | 38 | `006CAEB0` | `PrimitiveRendererD3D11` | 8 |
| `006CAB40` | `PrimitiveRendererD3D11` | 19 | `006CAF40` | `PrimitiveRendererD3D11` | 6 |
| `006CAB50` | `PrimitiveRendererD3D11` | 14 | `006CAFB0` | `PrimitiveRendererD3D11` | 29 |
| `006CAB80` | `PrimitiveRendererD3D11` | 15 | `006CB530` | `PrimitiveRendererD3D11` | 3 |
| `006CABC0` | `PrimitiveRendererD3D11` | 25 | `006CB540` | `PrimitiveRendererD3D11` | 44 |
| `006CABE0` | `PrimitiveRendererD3D11` | 22 | `006CB590` | `PrimitiveRendererD3D11` | 42 |
| `006CABF0` | `PrimitiveRendererD3D11` | 20 | `006CB5E0` | `PrimitiveRendererD3D11` | 1 |
| `006CAC00` | `PrimitiveRendererD3D11` | 21 | | | |

### btDiscreteDynamicsWorld — 31 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `00854EC0` | `btDiscreteDynamicsWorld` | 0 | `00857C10` | `btDiscreteDynamicsWorld` | 36 |
| `008553F0` | `btDiscreteDynamicsWorld` | 14 | `00857E70` | `btDiscreteDynamicsWorld` | 32 |
| `00855500` | `btDiscreteDynamicsWorld` | 28/30 | `00858130` | `btDiscreteDynamicsWorld` | 15 |
| `00855510` | `btDiscreteDynamicsWorld` | 7 | `008581A0` | `btDiscreteDynamicsWorld` | 29/31 |
| `00855520` | `btDiscreteDynamicsWorld` | 12 | `008581B0` | `btDiscreteDynamicsWorld` | 8 |
| `00855660` | `btDiscreteDynamicsWorld` | 19 | `008581E0` | `btDiscreteDynamicsWorld` | 13 |
| `008557F0` | `btDiscreteDynamicsWorld` | 38 | `00858270` | `btDiscreteDynamicsWorld` | 20 |
| `008559F0` | `btDiscreteDynamicsWorld` | 39 | `008582F0` | `btDiscreteDynamicsWorld` | 37 |
| `00855A50` | `btDiscreteDynamicsWorld` | 34 | `00858370` | `btDiscreteDynamicsWorld` | 10 |
| `00855B30` | `btDiscreteDynamicsWorld` | 27 | `00858500` | `btDiscreteDynamicsWorld` | 21 |
| `00857820` | `btDiscreteDynamicsWorld` | 4 | `00858560` | `btDiscreteDynamicsWorld` | 16 |
| `00857930` | `btDiscreteDynamicsWorld` | 24/25 | `008585E0` | `btDiscreteDynamicsWorld` | 35 |
| `00857940` | `btDiscreteDynamicsWorld` | 22 | `008588A0` | `btDiscreteDynamicsWorld` | 11 |
| `00857950` | `btDiscreteDynamicsWorld` | 17 | `00858A00` | `btDiscreteDynamicsWorld` | 18 |
| `00857960` | `btDiscreteDynamicsWorld` | 23 | `00858E70` | `btDiscreteDynamicsWorld` | 41 |
| `00857970` | `btDiscreteDynamicsWorld` | 33 | | | |

### CharacterRenderObject — 30 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `001F52F0` | `CharacterRenderObject` | 0 | `001F9B20` | `CharacterRenderObject` | 8 |
| `001F5C10` | `CharacterRenderObject` | 17 | `001F9FE0` | `CharacterRenderObject` | 22 |
| `001F6D60` | `CharacterRenderObject` | 3 | `001F9FF0` | `CharacterRenderObject` | 6 |
| `001F6E50` | `CharacterRenderObject` | 28 | `001FA0A0` | `CharacterRenderObject` | 14 |
| `001F6E70` | `CharacterRenderObject` | 2 | `001FA0E0` | `CharacterRenderObject` | 20 |
| `001F86D0` | `CharacterRenderObject` | 27 | `001FA1A0` | `CharacterRenderObject` | 24 |
| `001F86E0` | `CharacterRenderObject` | 5 | `001FA3D0` | `CharacterRenderObject` | 16 |
| `001F89B0` | `CharacterRenderObject` | 1 | `001FA810` | `CharacterRenderObject` | 21 |
| `001F8BE0` | `CharacterRenderObject` | 11 | `001FA820` | `CharacterRenderObject` | 30 |
| `001F8C00` | `CharacterRenderObject` | 10 | `001FAA10` | `CharacterRenderObject` | 26 |
| `001F8C70` | `CharacterRenderObject` | 12 | `001FAD40` | `CharacterRenderObject` | 25 |
| `001F8D10` | `CharacterRenderObject` | 19 | `001FAFB0` | `CharacterRenderObject` | 18 |
| `001F9A60` | `CharacterRenderObject` | 15 | `001FB070` | `CharacterRenderObject` | 4 |
| `001F9A70` | `CharacterRenderObject` | 23 | `001FB080` | `CharacterRenderObject` | 7 |
| `001F9A80` | `CharacterRenderObject` | 9 | `001FB120` | `CharacterRenderObject` | 13 |

### GameApplication — 18 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `0017CC70` | `GameApplication` | 0 | `0017CFD0` | `GameApplication` | 21 |
| `0017CCD0` | `GameApplication` | 4 | `0017D090` | `GameApplication` | 8 |
| `0017CDC0` | `GameApplication` | 6 | `0017D0C0` | `GameApplication` | 9 |
| `0017CDE0` | `GameApplication` | 5 | `0017D120` | `GameApplication` | 10 |
| `0017CDF0` | `GameApplication` | 23 | `0017D160` | `GameApplication` | 14 |
| `0017CE20` | `GameApplication` | 24 | `0017D170` | `GameApplication` | 22 |
| `0017CE50` | `GameApplication` | 7 | `0017D1A0` | `GameApplication` | 15 |
| `0017CEB0` | `GameApplication` | 2 | `0017D1E0` | `GameApplication` | 25 |
| `0017CF30` | `GameApplication` | 3 | `0017D210` | `GameApplication` | 16 |

### btBoxShape — 14 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `006939D0` | `btBoxShape` | 0 | `006A3C20` | `btBoxShape` | 27 |
| `006A0BF0` | `btBoxShape` | 16 | `006A3D40` | `btBoxShape` | 19 |
| `006A3980` | `btBoxShape` | 22 | `006A4050` | `btBoxShape` | 23 |
| `006A3B10` | `btBoxShape` | 8 | `006A43E0` | `btBoxShape` | 26 |
| `006A3B30` | `btBoxShape` | 21 | `006A4470` | `btBoxShape` | 14 |
| `006A3B40` | `btBoxShape` | 18/24 | `006A4550` | `btBoxShape` | 15 |
| `006A3B50` | `btBoxShape` | 25 | `00786F42` | `btBoxShape` | 28 |

### btCompoundShape — 11 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `00832530` | `btCompoundShape` | 0 | `00832CD0` | `btCompoundShape` | 15 |
| `00832810` | `btCompoundShape` | 7 | `00832DD0` | `btCompoundShape` | 14 |
| `00832930` | `btCompoundShape` | 1 | `00832E90` | `btCompoundShape` | 12 |
| `00832CA0` | `btCompoundShape` | 6 | `008330A0` | `btCompoundShape` | 5 |
| `00832CB0` | `btCompoundShape` | 10 | `00833290` | `btCompoundShape` | 9 |
| `00832CC0` | `btCompoundShape` | 8 | | | |

### btHashedOverlappingPairCache — 11 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `00848130` | `btHashedOverlappingPairCache` | 0 | `00848960` | `btHashedOverlappingPairCache` | 2 |
| `00848170` | `btHashedOverlappingPairCache` | 1 | `00848BE0` | `btHashedOverlappingPairCache` | 3 |
| `008481F0` | `btHashedOverlappingPairCache` | 7 | `00848C10` | `btHashedOverlappingPairCache` | 14 |
| `00848230` | `btHashedOverlappingPairCache` | 9 | `00848C20` | `btHashedOverlappingPairCache` | 10 |
| `00848270` | `btHashedOverlappingPairCache` | 12 | `00848C30` | `btHashedOverlappingPairCache` | 15 |
| `00848880` | `btHashedOverlappingPairCache` | 11 | | | |

### SebAudioBank — 10 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `0021ABC0` | `SebAudioBank` | 7 | `00223FA0` | `SebAudioBank` | 4 |
| `002238F0` | `SebAudioBank` | 6 | `00224180` | `SebAudioBank` | 3 |
| `00223DA0` | `SebAudioBank` | 8 | `00224360` | `SebAudioBank` | 5 |
| `00223E60` | `SebAudioBank` | 2 | `00224A30` | `SebAudioBank` | 1 |
| `00223F40` | `SebAudioBank` | 9 | `00224B30` | `SebAudioBank` | 10 |

### btTriangleShape — 10 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `00847340` | `btTriangleShape` | 0 | `008478D0` | `btTriangleShape` | 27 |
| `008473A0` | `btTriangleShape` | 16 | `00847900` | `btTriangleShape` | 19 |
| `00847830` | `btTriangleShape` | 22 | `00847960` | `btTriangleShape` | 23 |
| `00847890` | `btTriangleShape` | 8 | `00847980` | `btTriangleShape` | 26 |
| `008478B0` | `btTriangleShape` | 25 | `00847C00` | `btTriangleShape` | 15 |

### btDbvtBroadphase — 10 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `00849CA0` | `btDbvtBroadphase` | 0 | `0084A2C0` | `btDbvtBroadphase` | 10 |
| `00849CE0` | `btDbvtBroadphase` | 6 | `0084A320` | `btDbvtBroadphase` | 8/9 |
| `00849D40` | `btDbvtBroadphase` | 7 | `0084A5D0` | `btDbvtBroadphase` | 5 |
| `0084A0C0` | `btDbvtBroadphase` | 1 | `0084A6B0` | `btDbvtBroadphase` | 11 |
| `0084A220` | `btDbvtBroadphase` | 2 | `0084A740` | `btDbvtBroadphase` | 3 |

### Other classes (164 namespaces with fewer than 10 methods each) — 384 methods

| address | class | slot | address | class | slot |
|---|---|---|---|---|---|
| `00158DA0` | `CSingletonCriticalSection` | 0 | `00670580` | `TAsyncUpdate<class Phyre::PGeometry::PIndexDataBlockD3D11>` | 0 |
| `0016D6B0` | `eastl::allocator` | 1/2 | `00679330` | `ExternalVoice` | 0 |
| `0016D6C0` | `eastl::allocator` | 3 | `006793E0` | `ExternalVoice` | 1 |
| `001955F0` | `InputManager` | 0 | `00693040` | `btCollisionWorld::ClosestConvexResultCallback` | 0 |
| `00199D50` | `AsyncJobManager` | 0 | `00693070` | `btCollisionWorld::ClosestRayResultCallback` | 0 |
| `0019DF00` | `AssetListManager` | 0 | `006930A0` | `btCollisionWorld::ConvexResultCallback` | 0 |
| `0019F9F0` | `AsyncLoadManager` | 0 | `006939A0` | `btCollisionWorld::RayResultCallback` | 0 |
| `001B9AF0` | `ChrModel` | 0 | `00693A30` | `btConvexInternalShape` | 0 |
| `001C0EB0` | `SaveloadManager` | 0 | `00693AC0` | `btSphereShape` | 0 |
| `001C2670` | `MultipleDebugDisplay` | 0 | `00693B20` | `btStridingMeshInterface` | 0 |
| `001D70A0` | `ExtraUI` | 0 | `00693B60` | `btTriangleIndexVertexArray` | 0 |
| `001D8660` | `LoadingPage` | 0 | `0069EEB0` | `btGhostPairCallback` | 1 |
| `001DB3D0` | `GiVmax` | 1 | `0069F490` | `btCollisionWorld::ClosestConvexResultCallback` | 2 |
| `001DB550` | `GiVmax` | 0 | `0069F570` | `btCollisionWorld::ClosestRayResultCallback` | 2 |
| `001E1190` | `OrderedObject` | 0 | `006A3AF0` | `btSphereShape` | 10 |
| `001E11D0` | `MapOrderedObject` | 0 | `006A3B20` | `btSphereShape` | 8 |
| `001E1D90` | `MapRenderObject` | 0 | `006A47F0` | `btGhostPairCallback` | 2 |
| `001E5270` | `MapRenderObject` | 1 | `006CB7D0` | `Yebis::YebisPfxMemoryAllocatorD3D11` | 3 |
| `001EDF10` | `eastl::allocator_memory_log` | 1 | `006CB810` | `Yebis::YebisPfxMemoryAllocatorD3D11` | 1 |
| `001EDF80` | `eastl::allocator_memory_log` | 2 | `006CB940` | `Yebis::YebisPfxMemoryAllocatorD3D11` | 2 |
| `001EDFE0` | `eastl::allocator_memory_log` | 3 | `006CBB90` | `Yebis::PfxShimD3D11` | 0 |
| `001F16A0` | `GiSetRtForRtSampling` | 1 | `006CC490` | `CDataFrameQueue` | 0 |
| `001F1F60` | `AmbientOcclusionObj` | 0 | `006CC9F0` | `mkvparser::IMkvReader` | 2 |
| `001F1FA0` | `ApplyJsonForCutSceneObj` | 0 | `006CCA30` | `VbfMkvReader` | 2 |
| `001F1FE0` | `BegineScene0Obj` | 0 | `006CCAD0` | `VbfMkvReader` | 1 |
| `001F2020` | `BegineSceneObj` | 0 | `006CCB90` | `VbfMkvReader` | 0 |
| `001F2060` | `CopyBufferObj` | 0 | `007A5AA0` | `SoundObjectManagerCallbackHandler` | 1 |
| `001F20A0` | `CopyDepthBufferObj` | 0 | `008005C0` | `mkvparser::AudioTrack` | 0 |
| `001F20E0` | `CopyFrontBufferForChrRefraction` | 0 | `00800600` | `mkvparser::BlockGroup` | 0 |
| `001F2120` | `CopyFrontBufferForVFXObj` | 0 | `00800680` | `mkvparser::SimpleBlock` | 0 |
| `001F2160` | `CopyFrontBufferForWaterRefraction` | 0 | `008006D0` | `mkvparser::Track` | 0 |
| `001F21A0` | `DisableMsaaObj` | 0 | `00800710` | `mkvparser::VideoTrack` | 0 |
| `001F21E0` | `EnableDofObj` | 0 | `00808240` | `mkvparser::VideoTrack` | 2 |
| `001F2220` | `EnableMsaaObj` | 0 | `00808770` | `mkvparser::VideoTrack` | 1 |
| `001F2260` | `EndScene0Obj` | 0 | `00808C64` | `type_info` | 0 |
| `001F22A0` | `EndSceneObj` | 0 | `00830C50` | `btCollisionShape` | 0 |
| `001F22E0` | `FastClearObj` | 0 | `00830C80` | `btConvexShape` | 0 |
| `001F2320` | `GaussianFilterObj` | 0 | `00831DC0` | `btPolyhedralConvexAabbCachingShape` | 0 |
| `001F2360` | `GiResetDefaultRenderTargetObj` | 0 | `00831E20` | `btPolyhedralConvexShape` | 0 |
| `001F23A0` | `GiResetRenderTargetObj` | 0 | `00832370` | `btPolyhedralConvexAabbCachingShape` | 5 |
| `001F23E0` | `MaskBorderObj` | 0 | `008337D0` | `btConvexHullShape` | 0 |
| `001F2420` | `MonsterGallerySoftParticleEnable` | 0 | `00833830` | `btConvexHullShape` | 16 |
| `001F2460` | `PostProcessObj` | 0 | `00833A60` | `btConvexHullShape` | 22 |
| `001F24A0` | `Ps2DofObj` | 0 | `00833B20` | `btConvexHullShape` | 8 |
| `001F24E0` | `RazorMarkerPopObj` | 0 | `00833B30` | `btConvexHullShape` | 20/21 |
| `001F2520` | `RazorMarkerPushObj` | 0 | `00833B40` | `btConvexHullShape` | 23 |
| `001F2570` | `ReadPresetDofForCutSceneObj` | 0 | `00833CD0` | `btConvexHullShape` | 15 |
| `001F25B0` | `RenderAfterWaterObj` | 0 | `00833FB0` | `btConvexHullShape` | 12 |
| `001F25F0` | `RenderMapOpaqueObj` | 0 | `008341C0` | `btConvexHullShape` | 5 |
| `001F2630` | `RenderMonsterGalleryChara` | 0 | `00834910` | `btCapsuleShape` | 0 |
| `001F2670` | `RenderOpaqueObj` | 0 | `00834970` | `btCapsuleShape` | 16 |
| `001F26B0` | `RenderSSSObj` | 0 | `00834C70` | `btCapsuleShape` | 7 |
| `001F26F0` | `SetDofObj` | 0 | `00834D50` | `btCapsuleShape` | 1 |
| `001F2730` | `SetPrimIdEnableObj` | 0 | `00834FF0` | `btCapsuleShape` | 8 |
| `001F2770` | `SetRendererCameraObj` | 0 | `00835000` | `btCapsuleShape` | 15 |
| `001F27B0` | `SetScreenIndexToPostProcessManagerObj` | 0 | `00835290` | `btCapsuleShape` | 12 |
| `001F27F0` | `VideoObj` | 0 | `00835480` | `btCylinderShape` | 0 |
| `001F2830` | `ZBufferObj` | 0 | `008355B0` | `btCylinderShape` | 16 |
| `001F28A0` | `VideoObj` | 2 | `00835C90` | `btCylinderShape` | 8 |
| `001F28B0` | `AmbientOcclusionObj` | 1 | `00835CA0` | `btCylinderShape` | 20 |
| `001F29C0` | `ApplyJsonForCutSceneObj` | 1 | `00835CE0` | `btCylinderShape` | 14 |
| `001F29D0` | `BegineScene0Obj` | 1 | `00835E20` | `btCylinderShape` | 15 |
| `001F29E0` | `BegineSceneObj` | 1 | `00835E40` | `btCylinderShape` | 12 |
| `001F2A20` | `CopyBufferObj` | 1 | `00835FC0` | `btInternalTriangleIndexCallback` | 0 |
| `001F2B70` | `CopyDepthBufferObj` | 1 | `00836A20` | `btTriangleIndexVertexArray` | 2/3 |
| `001F2C50` | `CopyFrontBufferForChrRefraction` | 1 | `00836A80` | `btTriangleIndexVertexArray` | 11 |
| `001F2D40` | `CopyFrontBufferForVFXObj` | 1 | `00836AA0` | `btTriangleIndexVertexArray` | 9 |
| `001F2E40` | `CopyFrontBufferForWaterRefraction` | 1 | `00836AB0` | `btTriangleIndexVertexArray` | 10 |
| `001F2F30` | `DisableMsaaObj` | 1 | `00836B80` | ``public: virtual void __cdecl btBvhTriangleMeshShape::processAllTriangles(class btTriangleCallback * __ptr64,class btVector3 const & __ptr64,class btVector3 const & __ptr64)const __ptr64'::`2'::MyNodeOverlapCallback` | 0 |
| `001F2F50` | `EnableDofObj` | 1 | `00836BB0` | `btBvhTriangleMeshShape` | 0 |
| `001F2F70` | `EnableMsaaObj` | 1 | `00836C30` | `btNodeOverlapCallback` | 0 |
| `001F2F90` | `EndScene0Obj` | 1 | `00836D10` | `btBvhTriangleMeshShape` | 8 |
| `001F2FA0` | `EndSceneObj` | 1 | `00836DE0` | `btBvhTriangleMeshShape` | 14 |
| `001F2FB0` | `FastClearObj` | 1 | `00837120` | ``public: virtual void __cdecl btBvhTriangleMeshShape::processAllTriangles(class btTriangleCallback * __ptr64,class btVector3 const & __ptr64,class btVector3 const & __ptr64)const __ptr64'::`2'::MyNodeOverlapCallback` | 1 |
| `001F3090` | `GaussianFilterObj` | 1 | `008373D0` | `btBvhTriangleMeshShape` | 12 |
| `001F3210` | `GiResetDefaultRenderTargetObj` | 1 | `00837580` | `btBvhTriangleMeshShape` | 17 |
| `001F3260` | `GiResetRenderTargetObj` | 1 | `00837600` | `btBvhTriangleMeshShape` | 18 |
| `001F32B0` | `MaskBorderObj` | 1 | `00837680` | `btBvhTriangleMeshShape` | 5 |
| `001F32E0` | `MonsterGallerySoftParticleEnable` | 1 | `008377E0` | `btStaticPlaneShape` | 0 |
| `001F3300` | `PostProcessObj` | 1 | `00837820` | `btStaticPlaneShape` | 1 |
| `001F3440` | `Ps2DofObj` | 1 | `00837860` | `btStaticPlaneShape` | 6 |
| `001F34E0` | `RazorMarkerPopObj` | 1 | `00837870` | `btStaticPlaneShape` | 8 |
| `001F34F0` | `RazorMarkerPushObj` | 1 | `00837880` | `btStaticPlaneShape` | 14 — interior read 2026-09-17 (SWE2-FRONTIER): 1,165 B, `00861F14` ×3 + `00808C40`, first call [`0083794B`](../../_index/ADDRESS-INDEX.md) |
| `001F3500` | `ReadPresetDofForCutSceneObj` | 1 | `00837D10` | `btStaticPlaneShape` | 12 |
| `001F3510` | `RenderAfterWaterObj` | 1 | `00837D70` | `btStaticPlaneShape` | 5 |
| `001F3570` | `RenderMapOpaqueObj` | 1 | `00837D80` | `btSphereShape` | 16 |
| `001F3650` | `RenderMonsterGalleryChara` | 1 | `00837DB0` | `btSphereShape` | 7 |
| `001F36B0` | `RenderOpaqueObj` | 1 | `00837E20` | `btSphereShape` | 1 |
| `001F3740` | `RenderSSSObj` | 1 | `00837F00` | `btSphereShape` | 14 |
| `001F38B0` | `SetDofObj` | 1 | `00838020` | `btSphereShape` | 15 |
| `001F3910` | `SetPrimIdEnableObj` | 1 | `00838740` | `btAxisSweep3Internal<unsigned short>` | 0 |
| `001F3930` | `SetRendererCameraObj` | 1 | `008387A0` | `btAxisSweep3` | 0 |
| `001F39B0` | `SetScreenIndexToPostProcessManagerObj` | 1 | `00838800` | `btBroadphaseInterface` | 0 |
| `001F39E0` | `VideoObj` | 1 | `00838830` | `btNullPairCache` | 0 |
| `001F3A00` | `ZBufferObj` | 1 | `00839FE0` | `btCollisionObject` | 1 |
| `001F48B0` | `GeometryRenderTargetImmediate` | 0 | `0083A060` | `btCollisionObject` | 3 |
| `001F49A0` | `GeometryInstanceOrderedObject` | 0 | `0083A070` | `btCollisionObject` | 4 |
| `001F49E0` | `GeometryInstanceOrderedObject` | 2 | `0083A330` | `btCollisionObject` | 5 |
| `001F49F0` | `GeometryInstanceOrderedObject` | 1 | `0083A420` | `btDiscreteCollisionDetectorInterface::Result` | 0 |
| `001F4A40` | `CharacterOrderedObject` | 0 | `0083A450` | `btOverlapCallback` | 0 |
| `001FB8A0` | `DynGeoTextureInstance` | 2 | `0083AB88` | `DebugDrawcallback` | 0 |
| `001FB8E0` | `DynGeoTextureInstance` | 1 | `0083AC20` | `btConvexCast::CastResult` | 2 |
| `001FB990` | `DynGeoTextureInstance` | 6 | `0083AC50` | `DebugDrawcallback` | 0 |
| `001FBA50` | `DynGeoTextureInstance` | 5 | `0083AC90` | ``public: static void __cdecl btCollisionWorld::rayTestSingle(class btTransform const & __ptr64,class btTransform const & __ptr64,class btCollisionObject * __ptr64,class btCollisionShape const * __ptr64,class btTransform const & __ptr64,struct btCollisionWorld::RayResultCallback & __ptr64)'::`31'::LocalInfoAdder2` | 0 |
| `001FBB10` | `DynGeoTextureInstance` | 19 | `0083ACC0` | ``public: static void __cdecl btCollisionWorld::objectQuerySingle(class btConvexShape const * __ptr64,class btTransform const & __ptr64,class btTransform const & __ptr64,class btCollisionObject * __ptr64,class btCollisionShape const * __ptr64,class btTransform const & __ptr64,struct btCollisionWorld::ConvexResultCallback & __ptr64,float)'::`31'::LocalInfoAdder` | 0 |
| `001FBB70` | `DynGeo3DInstance` | 2 | `0083ACF0` | `btBroadphaseAabbCallback` | 0 |
| `001FBBB0` | `DynGeo3DInstance` | 6 | `0083AD20` | `btCollisionWorld` | 0 |
| `001FBBE0` | `DynGeo3DInstance` | 5 | `0083AD60` | `btSingleRayCallback` | 0 |
| `001FBD70` | `GiBeginScene` | 1 | `0083AD90` | `btSingleSweepCallback` | 0 |
| `001FBE40` | `GiEndScene` | 1 | `0083ADC0` | `btTriangleCallback` | 0 |
| `001FF870` | `JsonBox::OutputFilter<class JsonBox::IndentCanceller>` | 0 | `0083AFB0` | ``public: static void __cdecl btCollisionWorld::rayTestSingle(class btTransform const & __ptr64,class btTransform const & __ptr64,class btCollisionObject * __ptr64,class btCollisionShape const * __ptr64,class btTransform const & __ptr64,struct btCollisionWorld::RayResultCallback & __ptr64)'::`31'::LocalInfoAdder2` | 2 |
| `001FF8D0` | `JsonBox::OutputFilter<class JsonBox::Indenter>` | 0 | `0083B000` | ``public: static void __cdecl btCollisionWorld::objectQuerySingle(class btConvexShape const * __ptr64,class btTransform const & __ptr64,class btTransform const & __ptr64,class btCollisionObject * __ptr64,class btCollisionShape const * __ptr64,class btTransform const & __ptr64,struct btCollisionWorld::ConvexResultCallback & __ptr64,float)'::`31'::LocalInfoAdder` | 2 |
| `001FF930` | `JsonBox::OutputFilter<class JsonBox::SolidusEscaper>` | 0 | `0083DE00` | `btCollisionWorld` | 4 |
| `00201690` | `JsonBox::OutputFilter<class JsonBox::IndentCanceller>` | 3 | `0083E600` | `DebugDrawcallback` | 1 |
| `002016C0` | `JsonBox::OutputFilter<class JsonBox::Indenter>` | 3 | `0083F730` | `btSingleRayCallback` | 1 |
| `002016F0` | `JsonBox::OutputFilter<class JsonBox::SolidusEscaper>` | 3 | `0083F7B0` | `btSingleSweepCallback` | 1 |
| `0020CEF0` | `AmdAdapterInfo` | 0 | `0083F850` (interior read 2026-09-17, SWE2-FRONTIER: 1,041 B — `00861F14` at [`0083FB5F`](../../_index/ADDRESS-INDEX.md), near-leaf) | `DebugDrawcallback` | 1 |
| `0020CF90` | `AmdAdapterInfo` | 1 | `00840910` | ``public: static void __cdecl btCollisionWorld::objectQuerySingle(class btConvexShape const * __ptr64,class btTransform const & __ptr64,class btTransform const & __ptr64,class btCollisionObject * __ptr64,class btCollisionShape const * __ptr64,class btTransform const & __ptr64,struct btCollisionWorld::ConvexResultCallback & __ptr64,float)'::`22'::BridgeTriangleConvexcastCallback` | 2 |
| `0020D010` | `AmdAdapterInfo` | 2 | `00840990` | ``public: static void __cdecl btCollisionWorld::objectQuerySingle(class btConvexShape const * __ptr64,class btTransform const & __ptr64,class btTransform const & __ptr64,class btCollisionObject * __ptr64,class btCollisionShape const * __ptr64,class btTransform const & __ptr64,struct btCollisionWorld::ConvexResultCallback & __ptr64,float)'::`24'::BridgeTriangleConvexcastCallback` | 2 |
| `0020D050` | `NvidiaAdapterInfo` | 0 | `008418F0` | ``public: virtual void __cdecl btTriangleMeshShape::processAllTriangles(class btTriangleCallback * __ptr64,class btVector3 const & __ptr64,class btVector3 const & __ptr64)const __ptr64'::`2'::FilteredCallback` | 0 |
| `0020D120` | `NvidiaAdapterInfo` | 1 | `00841930` | `SupportVertexCallback` | 0 |
| `0020E6C0` | `GiScreenImage` | 1 | `00841970` | `btTriangleMeshShape` | 0 |
| `00211B60` | `AudioFileLoadManager` | 0 | `00841D20` | `btTriangleMeshShape` | 8 |
| `002127D0` | `AudioController` | 0 | `00841D30` | ``public: virtual void __cdecl btTriangleMeshShape::processAllTriangles(class btTriangleCallback * __ptr64,class btVector3 const & __ptr64,class btVector3 const & __ptr64)const __ptr64'::`2'::FilteredCallback` | 1 |
| `00212C60` | `MapOrderedObject` | 1 | `00841FE0` | `btTriangleMeshShape` | 14 |
| `00212C90` | `RenderObject` | 0 | `00842040` | `SupportVertexCallback` | 1 |
| `00212DA0` | `FontBorderOrderedGaussObject` | 0 | `008421B0` | `btTriangleMeshShape` | 5 |
| `00212E70` | `FontBorderOrderedGaussObject` | 1 | `008423C0` | `btQuantizedBvh` | 0 |
| `00212F70` | `FontBorderOrderedObject` | 1 | `00846630` | ``public: void __cdecl btOptimizedBvh::build(class btStridingMeshInterface * __ptr64,bool,class btVector3 const & __ptr64,class btVector3 const & __ptr64) __ptr64'::`2'::NodeTriangleCallback` | 0 |
| `00213040` | `FontBorderOrderedResetObject` | 1 | `00846670` | ``public: void __cdecl btOptimizedBvh::build(class btStridingMeshInterface * __ptr64,bool,class btVector3 const & __ptr64,class btVector3 const & __ptr64) __ptr64'::`2'::QuantizedNodeTriangleCallback` | 0 |
| `00213110` | `DynGeoFontTextInstance` | 2 | `008466B0` | `btOptimizedBvh` | 0 |
| `00213140` | `DynGeoFontTextInstance` | 1 | `00846C20` | ``public: void __cdecl btOptimizedBvh::build(class btStridingMeshInterface * __ptr64,bool,class btVector3 const & __ptr64,class btVector3 const & __ptr64) __ptr64'::`2'::NodeTriangleCallback` | 1 |
| `00213AA0` | `DynGeoFontTextSpecialFinalInstance` | 2 | `00846F70` | ``public: void __cdecl btOptimizedBvh::build(class btStridingMeshInterface * __ptr64,bool,class btVector3 const & __ptr64,class btVector3 const & __ptr64) __ptr64'::`2'::QuantizedNodeTriangleCallback` | 1 |
| `00213AD0` | `DynGeoFontTextSpecialInstance` | 2 | `00847290` | `btOptimizedBvh` | 6 |
| `00213B40` | `DynGeoFontTextSpecialFinalInstance` | 6 | `008472C0` | `btConcaveShape` | 0 |
| `00214210` | `DynGeoFontTextSpecialFinalInstance` | 10 | `00847300` | `btDiscreteCollisionDetectorInterface` | 0 |
| `002142A0` | `DynGeoFontTextSpecialInstance` | 10 | `00847D00` | `btGjkEpaPenetrationDepthSolver` | 1 |
| `002143E0` | `DynGeoFontTextSpecialShadowFinalInstance` | 10 | `008480D0` | ``public: virtual void __cdecl btHashedOverlappingPairCache::cleanProxyFromPairs(struct btBroadphaseProxy * __ptr64,class btDispatcher * __ptr64) __ptr64'::`2'::CleanPairCallback` | 0 |
| `00214540` | `DynGeoFontTextSpecialShadowInstance` | 10 | `00848100` | ``public: virtual void __cdecl btHashedOverlappingPairCache::removeOverlappingPairsContainingProxy(struct btBroadphaseProxy * __ptr64,class btDispatcher * __ptr64) __ptr64'::`2'::RemovePairCallback` | 0 |
| `00214890` | `DynGeoFontTextSpecialInstance` | 11 | `00848910` | ``public: virtual void __cdecl btHashedOverlappingPairCache::cleanProxyFromPairs(struct btBroadphaseProxy * __ptr64,class btDispatcher * __ptr64) __ptr64'::`2'::CleanPairCallback` | 1 |
| `002148B0` | `DynGeoFontTextSpecialShadowInstance` | 11 | `00848940` | ``public: virtual void __cdecl btHashedOverlappingPairCache::removeOverlappingPairsContainingProxy(struct btBroadphaseProxy * __ptr64,class btDispatcher * __ptr64) __ptr64'::`2'::RemovePairCallback` | 1 |
| `00215320` | `CharacterOrderedObject` | 1 | `0084AAC0` | `btTriangleConvexcastCallback` | 0 |
| `00215390` | `DynGeoUIInstance` | 2 | `0084AB00` | `btTriangleRaycastCallback` | 0 |
| `00215A30` | `DynGeoUIInstance` | 6 | `0084B290` | `btConvexCast` | 0 |
| `00215AA0` | `DynGeoUIInstance` | 5 | `0084B2E0` | `btSubsimplexConvexCast` | 0 |
| `00218260` | `AudioBank` | 7 | `0084B320` | `btSubsimplexConvexCast` | 1 |
| `002182A0` | `MusicAudioBank` | 7 | `0084BE30` | `btContinuousConvexCollision` | 0 |
| `002182E0` | `MusicAudioController` | 0 | `0084BE70` | `btPointCollector` | 0 |
| `00218980` | `MusicAudioController` | 7 | `0084BEA0` | `btPointCollector` | 3 |
| `002195D0` | `SepAudioBank` | 7 | `0084BED0` | `btContinuousConvexCollision` | 1 |
| `00219610` | `SepAudioController` | 0 | `0084CAF0` | `btGjkPairDetector` | 0 |
| `00219970` | `SepAudioController` | 1 | `0084CB20` | `btGjkPairDetector` | 1 |
| `00219B10` | `SepAudioController` | 7 | `00853040` | `btRigidBody` | 1 |
| `00219C40` | `SepAudioController` | 3 | `00853660` | `btRigidBody` | 3 |
| `0021AC00` | `SebAudioController` | 0 | `00853750` | `btRigidBody` | 0 |
| `0021B150` | `SebAudioController` | 7 | `00853C90` | `btRigidBody` | 4 |
| `0021B290` | `SebAudioController` | 3 | `00853F70` | `btRigidBody` | 5 |
| `0021BF20` | `ShoutAudioBank` | 7 | `00854E20` | ``protected: virtual void __cdecl btDiscreteDynamicsWorld::solveConstraints(struct btContactSolverInfo & __ptr64) __ptr64'::`2'::InplaceSolverIslandCallback` | 0 |
| `0021BF60` | `ShoutAudioController` | 0 | `00854E60` | `btSimulationIslandManager::IslandCallback` | 0 |
| `0021C3D0` | `ShoutAudioController` | 6 | `00854E90` | `btClosestNotMeConvexResultCallback` | 0 |
| `0021C440` | `ShoutAudioController` | 7 | `00854F00` | `btDynamicsWorld` | 0 |
| `0021CD80` | `StreamAudioBank` | 7 | `00854F40` | ``protected: virtual void __cdecl btDiscreteDynamicsWorld::solveConstraints(struct btContactSolverInfo & __ptr64) __ptr64'::`2'::InplaceSolverIslandCallback` | 1 |
| `0021CDC0` | `StreamAudioController` | 0 | `00855970` | `btClosestNotMeConvexResultCallback` | 2 |
| `0021D3D0` | `StreamAudioController` | 6 | `00857CD0` | `btClosestNotMeConvexResultCallback` | 1 |
| `0021D4E0` | `StreamAudioController` | 4 | `00859040` | `btConstraintSolver` | 0 |
| `0021EFC0` | `AudioSeadObjectBank` | 0 | `00859070` | `btSequentialImpulseConstraintSolver` | 0 |
| `0021F000` | `AudioSeadObjectManager` | 0 | `00859EA0` | `btSequentialImpulseConstraintSolver` | 4 |
| `0021F040` | `AudioSeadObjectSound` | 0 | `0085C3E0` | `btSequentialImpulseConstraintSolver` | 2 |
| `0021F0B0` | `MemoryStreamingReader` | 0 | `0085C4E0` | `btSequentialImpulseConstraintSolver` | 6 |
| `0021F0F0` | `MusicStreamingReader` | 0 | `0085CDC0` | `btSequentialImpulseConstraintSolver` | 8 |
| `00222BD0` | `MusicAudioBank` | 2 | `0085CED0` | `btSequentialImpulseConstraintSolver` | 7 |
| `00222C00` | `MusicAudioBank` | 0 | `0085DCE0` | `btSequentialImpulseConstraintSolver` | 5 |
| `00222C70` | `MusicAudioBank` | 10 | `00862D40` | `GiTrans` | 1 |
| `00222D30` | `SepAudioBank` | 6 | `00862EC0` | `GiTransNz` | 1 |
| `00222F20` | `SepAudioBank` | 8 | `00863040` | `GiSetTexture` | 1 |
| `00222FE0` | `SepAudioBank` | 2 | `00863350` | `Sys::Thread` | 0 |
| `002230D0` | `SepAudioBank` | 4 | `008633B0` | `crossThreadImpl` | 0 |
| `00223100` | `SepAudioBank` | 3 | `00863410` | `crossThreadImpl` | 1 |
| `00223130` | `SepAudioBank` | 5 | `00863850` | `GiColorRect` | 1 |
| `00223490` | `SepAudioBank` | 1 | `00863D80` | `GiPrim` | 1 |
| `00223540` | `SepAudioBank` | 10 | `008641B0` | `GiPrim` | 0 |
| `00224D40` | `ShoutAudioBank` | 2 | `00864330` | `GiSprite` | 1 |
| `002254F0` | `AudioSeadObjectBank` | 1 | `00864750` | `GiSprite` | 0 |
| `00225630` | `AudioSeadObjectSound` | 2 | `00864860` | `GiPolyGT4T` | 1 |
| `00225690` | `btTriangleIndexVertexArray` | 6 | `00864CA0` | `GiPolyGT4T` | 0 |
| `002259B0` | `MemoryStreamingReader` | 1 | `00864D70` | `GiZNormalOnOff` | 1 |
| `00225A50` | `MusicStreamingReader` | 1 | `00864E90` | `GiBeginEff` | 1 |
| `00225B20` | `MemoryStreamingReader` | 2 | `00864F30` | `GiBeginEff` | 0 |
| `00225BA0` | `MusicStreamingReader` | 2 | `008651A0` | `GiNormal` | 1 |
| `00621FF0` | `TAsyncUpdate<class Phyre::PRendering::PTexture2DD3D11>` | 0 | `0087F3D0` | `btSimulationIslandManager` | 0 |
| `00622000` | `TAsyncUpdate<class Phyre::PRendering::PTextureCubeMapD3D11>` | 0 | `0087FC00` | `btSimulationIslandManager` | 2 |
| `00670570` | `TAsyncUpdate<class Phyre::PGeometry::PDataBlockD3D11>` | 0 | `0087FCF0` | `btSimulationIslandManager` | 1 |

## 10. The object-size census across the game-specific set

**A class with a virtual destructor states its own object size**, because MSVC's deleting destructor
passes it to sized `operator delete`
([`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)). Run across the whole
game-specific slice of this index:

```
AGREE     12      both routes present and identical
DISAGREE   0
A_ONLY    80      sized delete only - no allocation site states a size
B_ONLY     3
NEITHER   30      no deleting destructor at all
          ---
          125 classes, 290 uniquely-owned methods

92 of 125 classes now have a code-stated object size.
```

> **"Zero disagreements" is zero out of TWELVE, not out of 125.** Only 12 classes have both routes,
> so the sized-delete route has never been *caught* contradicting an allocation site — which is not
> the same as having been broadly confirmed. **The 80 `A_ONLY` rows are single-route sizes and are
> recorded as such.**

**Route B's silence is not evidence of absence.** The allocation-site route requires a literal
`mov ecx,<size>` in a function that also calls a vtable-referencing constructor. Pool allocators,
sizes passed in other registers, and inlined constructors all defeat it. Those 80 are **"not found by
this method"**, not "not allocated with a stated size".

**A sanity check worth keeping:** `RazorMarkerPushObj` reports **`0x1`**. That is correct rather than
a parse failure — `sizeof` an empty C++ class is 1. The route is reporting language semantics, not a
guessed byte count.

### `NEITHER` is a family, not a leftover

Of the 30 classes with no deleting destructor, **19 are one coherent group**: 15 `Gi*`, 2
`DynGeoFontTextSpecialShadow*`, 2 `FontBorder*Object`. **Every one has a tiny vtable — slots 0 and/or
1 only.** Reading `GiTrans` slot 1 (`00862D40`): it takes a device pointer in `rdx` and issues
`call [dev+0x88]`, `call [dev+0xA8]`, `call [dev+0xA0]`.

**They are render command objects, and slot 1 is execute-against-device.** That explains the missing
destructor structurally: **commands submitted and discarded, not individually-owned objects.**

**The naming carries the game's PlayStation 2 heritage plainly.** `GiPolyGT4T` is the PS2 Graphics
Synthesizer primitive convention — **G**ouraud, **T**extured, **4** vertices — alongside
`GiBeginScene`, `GiEndScene`, `GiSetTexture`, `GiSprite`, `GiColorRect`, `GiZNormalOnOff`. **`Gi`
reads as *graphics interface***, and this is the PS2-era drawing vocabulary surviving intact into a
2017 remaster.

The remainder of `NEITHER`: `GameApplication` (never deleted — see
[the application root](../Application-Root/game-application.md)), `AsyncLoadManager`,
`CSingletonCriticalSection`, `NvidiaAdapterInfo`, `SoundObjectManagerCallbackHandler`, and 7 filter
edge cases.

### Class-count reconciliation: 125 against 117

The two sessions' game-specific filters differ by 8 classes while the **290 methods match exactly** —
so it is a filter edge, not extra data. The more permissive filter admits:

| n | what | why the exclusion list missed it |
|---:|---|---|
| 4 | `TAsyncUpdate<class Phyre::PGeometry::PDataBlockD3D11>` and siblings | templates **over** Phyre types; a depth-aware top-namespace returns `(global)` because the `::` is inside `<>` |
| 2 | function-local Bullet callbacks | backtick-scoped names inside `btCollisionWorld::objectQuerySingle`; a `bt*` prefix rule does not fire on a leading backtick |
| 1 | `type_info` | CRT, no namespace at all |

**Seven of the eight are accounted for, and all are exclusions both filters would want** — none is a
game class. **The eighth is unreconciled. BA-5.**

## 11. What this index does not cover

Restating, because sections 9 and 10 add reach without adding certainty:

- **The 2,611 folded addresses have no recoverable owner.** BA-1.
- **No method in this index has had its body read** by the index itself. BA-2 tracks the reading, and
  five families have been read so far.
- **Sizes for 80 of 125 game classes rest on a single route.** Above.

## 12. Falsification pass 2026-09-02 — survived, four attacks

**This document's guarantee** — *an address is listed only if the set of classes whose vtables
contain it has size 1* — was attacked directly. It carries 4,275 addresses and five other documents
rest on it.

| attack | result |
|---|---|
| **A.** Re-derive the admitted set from `methods.tsv` and diff against the published appendix | **4,275 admitted, 4,275 published, 0 missing, 0 extra** |
| **B.** Is any published address in fact multi-class? | **0** |
| **C.** Do the published slot numbers match the source? | **0 mismatches** |
| **D.** Do the published class names match the *current* post-`AS-9a` demangling? | **0 mismatches** |

**Nothing was found.** The appendix is exactly the set the stated rule admits, with correct slots and
current names.

### The attack's own first result was a false positive

The first run reported **2,134 admitted addresses missing from the appendix** — a defect that would
have invalidated half the document.

**It was the attack script.** The appendix packs **two** `(address, class, slot)` triples per row, and
a single regex over the line **consumes the `|` separator that the second triple needs**, so it found
only the first of each pair. The tell was arithmetic: **2,141 ≈ 4,275 / 2.**

> **An attack instrument is an instrument.** It has to be checked before its result means anything —
> a falsification pass that reports a defect is exactly as capable of being wrong as the document it
> attacks, and is *less* likely to be re-examined because a found defect feels like success.

## 13. What this index cannot reach — measured

Two substantial subsystems have now been found that no RTTI route could name, because **neither is a
C++ object**: the [`Gi*` render device](../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md)
and the [`003CCF20` machine](../../99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md).
**BI-15 asked how much of the binary sits where such things can hide.** Partitioning all 34,270
functions by how they can be reached statically:

| how reachable | functions | of all | code bytes | of all code |
|---|---:|---:|---:|---:|
| **in a vtable** — what RTTI can name | **6,883** | **20.1 %** | **629,978** | **8.5 %** |
| direct-called, not in a vtable | 16,806 | 49.0 % | 5,003,415 | 67.3 % |
| address-taken only (no vtable, no call) | 7,186 | 21.0 % | 1,048,166 | 14.1 % |
| ~~no vtable, no call, no taken address~~ | ~~3,395~~ | ~~9.9 %~~ | ~~748,388~~ | ~~10.1 %~~ **RETRACTED — §14** |

### The index reaches a fifth of the functions and a twelfth of the code

**Vtable methods are 20.1 % of functions but only 8.5 % of code bytes** — they are small. This index
names 4,275 of them, which is **12.5 % of the 34,270 non-funclet functions and less than 6 % of the executable's code**.

> **That is the ceiling, and it is structural.** However well the RTTI recovery is executed, it cannot
> see a subsystem built as static state plus free functions — and **two large ones have already been
> found by walking in from other directions.**

### The last row is where they hide

**3,395 functions holding 748 KB are reached by none of the three static routes** — no vtable entry, no
direct `call`, no address taken by a `lea` or stored in data. They are not unreachable; they are
reached by a mechanism this scan does not follow, the obvious one being the **32-bit RVA jump table**
(`mov ecx, [table + idx*4] ; add rcx, base ; jmp rcx`), whose targets appear in `.text` as
table-relative offsets rather than as pointers.

**That category contains named gameplay code**, not just helpers:

```
001D1660  13,753 B    0048F8C0  13,425 B    0049D540  10,573 B
004AAFC0  10,366 B    00488340  10,225 B    00485790   9,230 B
002778C0   9,374 B    BattleMenu_UpdateCommandSelectionAndDispatch
```

**A named battle-menu function that nothing in the image statically calls** is the clearest statement
of the gap: reachability by the three easy routes is not the same as reachability.

**Caveat stated:** "no static route found" is a property of the three scans run, not proof of
isolation.

> **The fourth route was already measured, and it is empty.** [The unowned-code census](../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md)
> recovered **506 dispatch sites and 5,540 distinct jump-table targets — of which zero are function
> entries.** In this image, image-relative jump-table targets are **always interior case labels**.
> Following them would move essentially nothing out of the 9.9 %. **BI-16 was opened here and closed
> by work this database had already done** — see the audit log for pass 126.

## 14. RETRACTION — the unreached figure was wrong by 8.5x

§13 published **3,395 functions / 748 KB** as reached by no static route, and framed it as the space
where non-C++ subsystems hide. **A peer session challenged the number before mining it, and was
right.** The scan had **two independent defects**, each hiding a real route.

### Defect 1 — half the LEA encodings

The address-taken route matched **`48 8D` only**. `lea r8, [rip+disp]` and every other destination in
`r8`–`r15` is **`4C 8D`** (REX.WR):

```
00276DD3   4c 8d 05 e6 0a 00 00     lea r8, [rip + 0xAE6]   ->  002778C0
```

**The example the section led with — `BattleMenu_UpdateCommandSelectionAndDispatch`, "a named
battle-menu function that nothing statically calls" — is address-taken by exactly that instruction.**
It is the message proc installed on a widget, and it was in the wrong row.

**`string_xref.py` in this repository documents both encodings.** The correct answer was already in
the toolkit; a narrower scan was written from scratch instead of reusing it.

### Defect 2 — tail calls are calls

The scan had **no `E9` route at all**. `jmp rel32` landing on a function entry is a **tail call**, and
MSVC emits them constantly.

```
functions reached by an E9 tail call            : 4,847
of those, reached by NO other route             : 2,895
```

### The corrected partition

**Population: all 34,270 non-funclet functions** — the 38,161 internal functions less the 3,891
`Unwind@`/`Catch_All@` exception funclets. Stated because the rows below sum to exactly that and to
nothing else: a reader taking "of all" to mean all 38,161 reads every percentage here about 11 %
too high. The code-byte column uses the same population.

| how reachable | functions | of all | code bytes | of all code |
|---|---:|---:|---:|---:|
| in a vtable | 6,883 | 20.1 % | 629,978 | 8.5 % |
| direct- or **tail**-called | 19,767 | 57.7 % | 5,449,459 | 73.3 % |
| address-taken only (both LEA encodings) | 7,269 | 21.2 % | 1,262,551 | 17.0 % |
| **no route found** | **351** | **1.0 %** | **87,959** | **1.2 %** |

```
3,395 fn / 748 KB   as published        (48 8D only, no E9)
3,246 fn / 525 KB   + the 4C 8D encoding
  351 fn /  88 KB   + E9 tail calls     <- corrected
```

**An independent instrument built by the peer session gives 435 functions / 81.8 KB.** Two scans
written separately now agree to within noise, having disagreed by **8x**.

### What survives, and what does not

**The RTTI ceiling stands unchanged** — the index names 4,275 methods, **12.5 % of the 34,270 non-funclet functions and under
6 % of the code**, and cannot see non-C++ subsystems by construction. **Two substantial ones have been
found.**

**What does not survive is the residue.** *"748 KB nobody has looked at"* is **88 KB**. The ceiling is
real but narrow: **the index misses specific subsystems, not a large general mass of unexamined
code** — which is a materially weaker and more accurate claim.

> **The disagreement was the finding.** Most cross-checks in this database have been two readings of
> one dump. Here two genuinely independent instruments answered the same question and differed by 8x,
> and **halting to reconcile them cost one pass and prevented a research programme built on a wrong
> denominator.**

## 14a. Defect 3 — the conditional tail call, and it is the guard-stub idiom

FABLE filed a notice on 2026-09-16 naming a route missing from this section's list: the **conditional
near jump `0F 8x rel32`**. The notice quoted §13's retracted 3,395 figure, so it is re-derived here
against §14's corrected framing, which is the live claim.

**It is the same argument as Defect 2.** Defect 2 admitted `E9 jmp rel32` on the grounds that *a tail
call is a call*. The conditional form is a tail call under a condition, and the same reasoning admits
it. §14 fixed `jmp` and did not fix `jcc`, so the route list is one short.

### Measured twice, independently, to the byte

| | functions | code bytes |
|---|---:|---:|
| reached by a `0F 8x rel32` and by no other static route | **42** | **23,944** |

FABLE measured this on 2026-09-16 and I measured it on 2026-09-17 with a separately written sweep
(`Tools/work/OPUS/p1-scratch/routes.py`). **Both return 42 entries and 23,944 bytes.** Where the two
partitions do differ is stated below rather than smoothed over.

Three witnesses, read as bytes at the jump site, each landing on a genuine MSVC prologue rather than a
mid-body label:

```
002DEC22   0f 89 08 cf ef ff   jns 001DBB30     -> push rbx / sub rsp,0x20
00269ABD   0f 89 dd 00 00 00   jns 00269BA0     -> mov [rsp+8],rbx / mov [rsp+0x10],rbp
002032F8   0f 82 a2 fe ff ff   jb  002031A0     -> mov [rsp+8],rbx / mov [rsp+0x10],rbp
```

### What the route actually is

It is not an exotic encoding. It is a **guard stub**: a very small function that tests a precondition
and either falls through to `ret` or conditionally jumps to the real body.

```
0045AEE0   cmp byte [rcx], 0        0045AEE0 is 10 bytes; 0045AEF0 is 867
0045AEE3   jne 0045AEF0
0045AEE9   ret

002E70A0   test rcx, rcx            three tests, then the body
002E70A3   je 002E70B6
002E70A5   test byte [rcx+0xD], 1
002E70A9   jne 002E70B6
002E70AB   cmp qword [rcx+0x30], 0
002E70B0   jne 003250F0             -> BattleUnit_HandleReactionAnimationEvent
002E70B6   ret
```

Three facts settle what these 42 are:

- **All 42 jump sources are themselves reachable** by an ordinary route. Not one is in the residue.
- **29 of the sources are 32 bytes or smaller** — the guard-stub shape.
- **Each of the 42 targets has exactly one conditional source.** These are pairs, not a mesh.

So every one of the 42 is **live code entered through a reachable guard**, not a body nothing reaches.
Three carry real names already: `SaveloadManager_ParseDisableAutosaveList` (`001C0F20`, 2,028 B),
`BattleUnit_HandleActionTimelineEvent` (`00325260`, 1,215 B) and
`BattleUnit_HandleReactionAnimationEvent` (`003250F0`, 279 B) — the last two being battle event
handlers, which is not where a reader of §14's table would look for them.

### Effect on §14's residue

Against the published **351 functions / 87,959 bytes**, the conditional jump accounts for **42
functions and 23,944 bytes — 12 % of the functions and 27 % of the bytes.** §14's *"88 KB"* is at most
about **64 KB**, and its conclusion — *the index misses specific subsystems, not a large general mass
of unexamined code* — holds, with one more specific subsystem shape named: the guard-stub pair.

**Where the two partitions differ, stated.** My own sweep's residue is **485 functions / 107,931
bytes**, not §14's 351 / 87,959, because my address-taken route counts only 8-byte-aligned absolute
qwords in the data sections (excluding `.pdata` and `.reloc`, since pass 6 bans unwind data as
evidence) plus `rip`-relative `lea`. A less conservative address-taken scan finds more routes and a
smaller residue. **The 42 figure does not depend on that difference** — it was reached from both
partitions independently — but the residue totals do, and no figure here should be quoted as if the
two instruments agreed about them.

### The route list, corrected

A function entry is statically reached in this image by **four** routes, not three:

1. a vtable slot (or any stored address in data),
2. a direct `call` (`E8`),
3. an unconditional tail call `jmp rel32` (`E9`) — added by Defect 2,
4. **a conditional tail call `jcc rel32` (`0F 8x`)** — this section,

with "address taken by a `lea`" spanning 1 and 3's data forms. The `7x rel8` short conditional form
reaches **no** function entry anywhere in the image (0 targets), which is expected: a guard stub and
its body are usually further apart than 127 bytes, and where they are not, the assembler still emits
the near form here.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `005DF890` | 906 | vtable slot registration on `[rbx+0x30]`/`[rdi+0x1C0..0x1D8]`/`[r8+0x80]`: `005DF810`, `005E2FB0` x8, `00584730` x8 (CRT init); callers `005D1940`/`00611A40` |

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This index named these bodies only at their entries. Each interior address was read in the shipping
image; the notes say what the instruction does, not yet the body's full role.

| body | interior cite | what is there |
|---|---|---|
| `001F8D10` | `001F9013` | `call memcpy` after five `001945B0` calls — a structured field marshaler |
| `001F6E70` | `001F70A3` | `call _guard_check_icall` — a CFG-guarded indirect dispatch mid-body |
| `006739A0` | `00673CF0` | head of a repeated singly-linked-list splice loop (`[rdx+8]` walk, `cmove` on sentinel); the same idiom recurs ~20 times down the body |
| `006B9CF0` | `006B9F7B` | `call memset` after two `_alloca_probe` calls — a large-stack-frame body that zeroes a scratch record |
| `005C72A0` | `005C7481` | `call sqrtf` — the midpoint of a float-normalise sequence feeding two `005A7E90` calls and a `memcpy` |
| `00864860` | `00864B02` | `call 0018AA30` between `001EE650` and `0018AA10` — the standard guard-check + helper-call shape |
| `001FA3D0` | `001FA4F0` | `call _alloca_probe` inside `CharacterRenderObject_SubmitMaterialsWithFadeMode` before a `memset` of a scratch block |
| `00864330` | `0086463F` | `call 0018AA30` — same guard-check + helper-call shape as `00864860` |
| `0077E0B0` | `0077E0C7` | `call 007142F0` — `CDepthOfField` slot 3 (3,044 B): the effect's **per-frame context gather** — opens with the `007142F0`/`00714560`/`0075E7C0`/`0075E690` setup family, then makes ~25 dispatches through the 13-B thunk `006DA8A0` (`dec dword[02EA0B3C]; jmp [rax+0x10]` — a counted vtable `+0x10` call) on the PPFX manager object `[01F3BA68]→01F3BA78`, one per sibling-context fetch; arms separated by `jmp 0077E23D`/`0077E34F` short-circuits |
| `007D76E0` | `007D8012` | `call powf` (`00861F6E`) — `Sd::Driver::SurroundReverb` slot 8 is the reverb's **parameter commit**: ten calls to the six-case mode-normalise helper `007A9E50` (jump table at `.rdata 01689F1C` off the image base), the driver-global getter `007AED00` (`dword [02EAD348]`), two `powf` calls (dB→linear / decay scaling), and a tap-table fill loop indexing `word[r9 + rax*2]` over constants `0.000488 (1/2048)`, `0.6`, `0.25`, `10.0`, `-6.0` |
| `0085C4E0` | `0085C564` | `lea rcx,[rax+rax*2]` — `btSequentialImpulseConstraintSolver` slot 6 is the solver's **cache-friendly workspace setup**: three `memset` (`00861EC0`) + four `free` (`0085E710`) calls around a ×3-stride record walk (`lea rcx,[rax+rax*2]` recurs six times — three vectors per constraint row) with group-of-4 packing (`cmp r11,4` / `lea r10,[r11-4]` / `lea rdi,[r10*4]`) |
| `0085CED0` | `0085D029` | `call [rax+8]` — `btSequentialImpulseConstraintSolver` slot 7 is the solver's **constraint accounting + pool setup**: iterates typed-constraint pointer arrays (`[r13 + rbx*8]`) making per-constraint vtable calls at +0x08, +0x18 and +0x20, accumulates a row-count total (`add r12d, [rbx]` per element at `0085D149`), then grows the solver pools through `realloc`-style `0085E680` + `free` (`0085E710`) ×3 + `memset` (`00861EC0`) ×2 |
| `00854F40` | `00854FBC` | `call [r10+0x10]` — `btDiscreteDynamicsWorld::solveConstraints`' `InplaceSolverIslandCallback` slot 1 is the per-island **`processIsland`**: two solver-interface dispatches through `[r10+0x10]`, three realloc (`0085E680`) + free (`0085E710`) pairs resizing the island's local solver pools, tail `call 00857F10` |
| `007DB8D0` | `007DB976` | `subss xmm1, xmm6` in a lerp arm — `Sd::Driver::BuildReverb` slot 3 is the build-reverb's **parameter commit**, same shape as `SurroundReverb` slot 8 (`007D76E0`): nine calls to the six-case mode-normalise helper `007A9E50`, the driver-global getter `007AED00` ×2, `expf` (`00861FAA`) + `powf` (`00861F6E`) coefficient scaling over the `+0x490..+0x4CC` float block (`lerp`: `x8 = x8*(b−a)+a` at `007DB96A`–`007DB97F`) |
| `0084B320` | `0084BCD4` | `call sqrtf` (`00861F14`) — `btSubsimplexConvexCast` slot 1 is the subsimplex cast's **`calcTimeOfImpact`**: full xmm6–xmm15 save set + stack cookie, one `008526D0` setup call at entry (`0084B3AD`), the GJK iteration block at `0084BC09`–`0084BD88` calls the vector/support helpers `008521C0`, `008516E0`, `00851740`, `00852170` around a `sqrtf` λ-distance clamp (`0084BCD4`), CFG guard `00808C40` at the tail (`0084BD88`) |
| `0084BED0` | `0084C0CD` | `call [rax+0x18]` — `btContinuousConvexCollision` slot 1 is **`calcTimeOfImpact`** (conservative advancement): three shape-virtual calls at `+0x18` (support/distance queries), `sqrtf` (`00861F14`) ×3 for closest-point norms, the GJK substep family `0084C6B0`/`0084C9E0`/`0084CA50`/`0084CB20`, and `call [rax+0x50]` ×2 on the result object's vtable `01CCF1C0` (RTTI: `btPointCollector` — a `btDiscreteCollisionDetectorInterface::Result`) |
| `007D6270` | `007D62C6` | `movss xmm2, [rbx+0x1ac]` — `Sd::Driver::SurroundReverb` slot 5 is the effect's **per-frame parameter ramp stepper**, ~40 unrolled iterations of one idiom over the (current, target, flag) triple at 0x30 pitch (`+0x58/+0x5C/+0x68`, `+0x88/+0x8C/+0x98`, … `+0x1A8/+0x1AC/+0x1B8`): if `byte[rbx+flag]` set, `cur += xmm1` (the frame delta), `comiss` vs target — on arrival clamp `cur=target`, clear the flag; `cl=1` return. Zero external calls — the `DynamicValue<2>` banks from the ctor stepped in place |
| `0075C080` | `0075C0AB` | `call 007273E0` — `CRenderTextureArray` slot 0 is **`InitializeDevice`** (the established slot-0 convention on this family): opens by calling `CGPUResourceManage::InitializeDevice` and bailing on its `js` failure (`0075C0B0`–`0075C0B2`), guards `[rbx+0x28]` array base + `[rbx+0x3C]` count, runs alternating `006DF480`/`0071B3C0` release pairs over the old entries (`0075C846`–`0075C8A0`), then recreates the array — `0071A380`, `007157A0`, `00719380`, `00719460`, `00715C70`×3, `006DA880`, `00720FB0` (`0075C9C4`–`0075CA97`) |

*(Entry-only-large identification, 2026-09-15: `007307A0` is **`CTextureUtil::InitializeDevice()`** —
named by its own log strings in `GPUTextureUtil.cpp` (`==== CTextureUtil::InitializeDevice() ====`,
`PPFX ERROR:`). The 4,903 B body is the class's whole device-init sequence: it calls
`007273E0` = `CGPUResourceManage` slot 0 (the failure path's string names it
`CGPUResourceManage::InitializeDevice()` — so slot 0 is `InitializeDevice` on both classes),
runs `m_shaderSet.InitializeDevice()` (through `0072D820`/`0072F7D0`/`0073BB50`) and
`InitializeDeviceSharedTexturePool()`, then `m_pGPUDevice->CreateTexture` once per PPFX texture the
engine keeps on the object — the strings name `m_pGPUTextureFullColorDitherMatrix`,
`m_pGPUTextureFilmGrain`, `m_pGPUTextureSpectrum`, `m_pGPUTextureRadiusGaussianFade`,
`m_pGPUTextureZero`, `m_pGPUTextureGray`, `m_pGPUTextureOne`, `m_pGPUTextureAnalyzer`, plus
`CreateDepthStencilSurface(&m_pGPUDepthMeasurement)`. The indirect calls on `[device vtable + 0x30 /
0x68 / 0x208 / 0x220 / 0x228]` are the `IGPUDevice` COM surface driving the creation calls.
Debug-verbosity gates on `01F3BA80`, `02EA0B40`, `01F3BA90` choose whether the progress banners
print. Interior anchor `007307FE` loads the resource manager from `[this+0x22320]`;
interior anchor `00731840` and interior anchor `00731937` are two of the repeated `call [r1x+0x220]` texture-creation calls.
`CTextureUtil` slots 1–4 (`00731AD0`–`0075ADF0`) remain unnamed.)*

*(Pass 22 adjacency, 2026-09-14: vtable hosts cross into the layers that implement the slots —
`0020D050` calls **platform** `00159270`, `0020D120` calls `001590B0`, `00225690` is called by
platform bodies `006239C0`/`0061F200` (interior read 2026-09-17, SWE2-FRONTIER: 1,101 B — **recursive**, self-call at [`0061F252`](../../_index/ADDRESS-INDEX.md), `005FD050` ×7 + `005FCF20` ×6) and three more (7 edges), and `002778C0` calls
**combat-action** `00311CD0`/`00311B20` (2). The index records where slots point; platform and
combat code are where some of them land.)*

*(Pass 22 live-graph completion, 2026-09-15: `00311B20` calls `ActorEntity` `0031B810` (1
edge) — the combat-action slot body forwards into the actor layer, one more slot landing
outside its table's own folder.)*

*(Pass 22 live-graph sweep 2, 2026-09-15: `0031B810`'s callers are `Movement` `00313670`/
`00310920` (and one more, 3), `Rewards_Progression_Economy` `002F8BB0` (1) and
`Spawn_Encounter_Lifecycle` `00234DA0` (and one more, 2) — the actor body the combat slot
forwards to is itself consumed across the layers that drive actors.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT and SERVICE, 42 edges.** They are spread across 21 cited methods. The largest shares are `003CCF20` (10), a 4-byte stub (6) and a 296-byte method (5). `Renderer_CreateRandomNoiseTextureFromGraphicsMT19937` is among the callers.
- **Input — SERVICE, 33 edges.** The crossing is the appendix's application and device classes: the `GameApplication` slots `0017CDC0`/`0017CDF0`/`0017CE20`/`0017CE50` and the `PFramework::PApplication` methods `0079BF70`/`0079D560`/`0079D5B0`/`001967D0` call into input-layer bodies — the pad-device polling the `PInputDevicePadSteamController` row above already names. The index lists the classes; the calls into input code are those methods' own work.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `0031B810` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `FUN_00388d50`, owned by that layer, calls `0031B810` on this page. That caller is a 298-byte target predicate made on the same two-table resolution as the effective-action-id query - `byte[+5] == 0` indexes the `0x40`-byte rows at `0208D480` by `byte[+4]`, anything else the rows at `0208DE80` by the owning unit's `byte[+0xEA9]` - which it then compares against the handle in the unit's `dword[+0x710]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Items_Equipment_Shops_License — CLIENT.** `Inventory_QueryOwnedCountIncludingReservedActionItems`, owned by that layer, calls `0031B810` on this page. That caller is the owned-count query for an item id, which returns `-1` for the sentinel id `0xFFFF`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**RNG_Random_Selection — SERVICE.** `0085CDC0` on this page calls `FUN_0085dde0`, owned by that layer. What it reaches is a 1,161-byte CRT-side routine gated on bit 0 of `byte[+0x3C]` of its last argument and on the low three bits of its second being clear; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — CLIENT (16 edges through 10 of this page's functions).** The Resource layer reaches this page at `0017CEB0`, `00225BA0`, `0059D4B0`, `006CCB90` and 6 more. `FUN_002eeee0` is the worked example, read in full - it is a 295-byte step through a packed `(kind << 16) | index` id: when the index goes negative it looks the kind up in the **eight-entry `.rdata` table** at `00D0F870`, steps to the neighbouring kind modulo eight, and restarts the index at zero - so the id wraps across kinds rather than running off the end; **1 of the 12 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).
**Audio — SHARED HELPER (SWE2-EC7, batch 168).** The batch-168 `00219530` `vector<0x68>` teardown names the `SepAudioController` row (`00219610`) it serves - the controller family's vectors share this per-element destructor, so Audio's 790-row adjacency is the row bodies consulting the shared `_Tidy`, not an Audio subject of this page.
- **ActorEntity — CLIENT and SERVICE (17 edges).** 1 inbound (ActorEntity bodies `ActorResource_BeginManagerResourceSetLoad` (0032FCA0) call page-cited `002DF980`); 16 outbound (page-cited `BattleUnit_HandleActionTimelineEvent` (00325260), `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0), `00269BA0` call ActorEntity bodies `BattleUnit_FindMappedDefinitionSelectorByIndex` (0031B810), `Actor_GetWorldPosition` (00265020), `ActorHandle_ResolveRegistryEntryByPackedId` (003588B0)). Substantive edges include `00269BA0` calls `ActorResource_SubmitRequestDescriptor` (003DBB60); `BattleUnit_HandleActionTimelineEvent` (00325260) calls `0026A430`; the remaining edges run through shared helpers the page cites.
- **Gameplay — CLIENT and SERVICE (6 edges).** 4 inbound (Gameplay bodies `BattleAction_FindApproachGeometryAroundTarget` (00339630), `BattleUnit_HasNonPartyEngagementEvidence` (00308040), `00234150` call page-cited `BattleUnit_FindMappedDefinitionSelectorByIndex` (0031B810), `00203080`, `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0)); 2 outbound (page-cited `BattleUnit_FindMappedDefinitionSelectorByIndex` (0031B810), `BattleUnit_HandleActionTimelineEvent` (00325260) call Gameplay bodies `BattleEncodedId_IsValidForClass` (00322C50), `003257D0`). Substantive edges include `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0) is called by `BattleUnit_HasNonPartyEngagementEvidence` (00308040); `BattleUnit_HandleActionTimelineEvent` (00325260) calls `003257D0`; the remaining edges run through shared helpers the page cites.
- **Party — SERVICE (5 edges).** 5 outbound (page-cited `00310920`, `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0), `BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout` (00311B20) call Party bodies `BattleUnit_GetPartyLeader` (003272A0), `PartyFocus_IsCurrentPackedActorHandle` (003273B0), `00327270`). Substantive edges include `Spawn_ValidateCandidateDistanceToPlayers` (00234DA0) calls `PartyFocus_IsCurrentPackedActorHandle` (003273B0); `00310920` calls `00327270`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `00510740` call page-cited `00660570`). Substantive edges include `00660570` is called by `00510740`.
- **UI — CLIENT and SERVICE (73 edges).** 42 inbound (UI bodies `0018EEE0`, `BattleMenu_ClassifySelectedEntryAndHandleImmediateCommands` (0027C3D0), `0027BED0` call page-cited `00203080`, `00225580`, `00272EE0`); 31 outbound (page-cited `BattleMenu_UpdateCommandSelectionAndDispatch` (002778C0), `001F3300`, `00272EE0` call UI bodies `0035BB20`, `0018EEE0`, `0027DC10`). Substantive edges include `001F3300` calls `0018EEE0`; `BattleMenu_UpdateCommandSelectionAndDispatch` (002778C0) calls `0035BB20`; `BattleMenu_UpdateCommandSelectionAndDispatch` (002778C0) calls `0027DC10`; `BattleMenu_UpdateCommandSelectionAndDispatch` (002778C0) calls `00296AF0`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — MECHANICAL (7 edges).** 1 other inbound edge(s); 6 calls from page-cited bodies into shared WorldAreaField plumbing (`FieldData_GetActiveFieldRecordBit15` (00313F60), `FieldData_GetActiveFieldRecordBit15` (00377C20)) - the helpers' general call surface, not a WorldAreaField relationship of this page's subjects.
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `00510740` call page-cited `00660570`). Substantive edges include `00660570` is called by `00510740`.
## The `00215320` exclusive subtree — all 5 members bound (SWE2-FRONTIER, followup queue)

`00215320` — the appendix's `CharacterOrderedObject` slot-1 method (`0084AAC0`) — is a 9-byte
this-adjusting thunk: `this = [rcx+8]`, tail `001F5D70`. It owns **5 frontier functions**;
every member was disassembled from the shipping image; interior cites sit inside each
declared extent. The family is the object's render-submission pass: `001F5D70` gates on
`byte[+0x4B4]` (visible) plus `dword[+0x480]` id checks (`byte[+0x16]==0x68` on the
`002DF980` record, `+0x480 != 0x6E006D`), decodes params through `002E98F0`, scales the
`0060E810` submit by `cvtdq2ps([01F82F08])` and `[01F82EF4]`, pushes scale state via
`001FB310`, then — when `[+0x50]` is non-null — builds a `vector<0x318>` element list
(`001EDF00` string init from `008C5F58` + `001F87B0` pushes + `rsi+0x78` source), runs the virtual
`[vtable+0xF0]` submit, walks the list staging each element's transforms with `001FAD50`,
and closes with the `001F68E0` palette pass when `[001BDAB0()+0xF8]` requests it. Tail
clears `dword[+0x4A4]` and `byte[+0x4B5]`.

| member | role | interior |
|---|---|---|
| `001F5D70` (2,924 B) | the submission body described above — prologue `00189120`/`0018B4E0` context bytes, `001AD440` `+0xA8` early-exit, id-gated arm, list build, virtual submit, per-element staging loop, palette tail | [`001F62E7`](../../_index/ADDRESS-INDEX.md) |
| `001F87B0` (161 B) | `vector<0x318>` emplace-back: bump `[rcx+8]` past `[rcx+0x10]` check, then a 6×0x80+0x18 SSE copy of the source element; overflow tails `001F5330` (grow) | [`001F87F2`](../../_index/ADDRESS-INDEX.md) |
| `001FAD50` (593 B) | per-element transform stager — `byte[+0x4B4]`-gated, element = `[+0x58][idx]` (0x318 stride): writes the element's `+0xF0`/`+0xF8` scalar slots, then three 64-B matrices from `+0x584`/`+0x5C4`/`+0x604` (or the `+0x4C4`/`+0x504` alternates when `00189120()+0x1D` is clear) into its `+0x100`/`+0x108`/`+0x110` destination slots at `+rsi` | [`001FADDB`](../../_index/ADDRESS-INDEX.md) |
| `001FB310` (66 B) | scale publish: `001F0850()` object gets `+0x4C` = `[this+0x4B8]` and `+0x50` = `const × [this+0x4BC]`; `[this+0x4C0]` → global `04A7C3A8` | [`001FB32C`](../../_index/ADDRESS-INDEX.md) |
| `001F68E0` (1,149 B) | SSE bone-palette pass: per pointer in the `[+0x30]` 8-byte-element array, alloca `count×0x20` scratch via `00808F10`, then a 4-wide `movups`/`shufps` loop gathering the indexed `0x40`-stride rows through the `[+0x58]` index array | [`001F69C0`](../../_index/ADDRESS-INDEX.md) |

`00189120`, `0018B4E0`, `001AD440`, `002E98F0`, `002DF980`, `0060E810`, `001EDF00`,
`0060B980`, `00185A80`, `001F5330`, `001F0850`, `001BDAB0` and `00808F10` are shared
callees with other callers — deliberately not census members.

## The `001C2670` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`001C2670` (52 B) is `MultipleDebugDisplay`'s scalar deleting destructor:
`001C2120(rdi)` runs the body, then `bl & 1` → `00809950(rdi, 0x4670)` — the
object is `0x4670` bytes (`001C2684`–`001C2691`).

| member | role | interior |
| --- | --- | --- |
| `001C2120` (259 B) | the destructor body — installs vtable `008F9DC8` (RTTI locator `01CED198`), `001EAE10` cleanup ×2 (`001C215A`, `001C21B5`), `001C2070` sub-destructors ×2 (`001C21E3`, `001C21EC`), `00809054` scope with callback `001C2110` (`001C2208`) | [`001C2141`](../../_index/ADDRESS-INDEX.md) |
| `001EAE10` (135 B) | the cleanup loop — `001EA050`, `00584730`, `0067B3A0`, `00584730`, `0019CE20`, `0019CC50` (`001EAE33`–`001EAE7D`) | [`001EAE56`](../../_index/ADDRESS-INDEX.md) |
| `0067B3A0` (199 B) | the vtable-slot invoker — `00673860` then `call [rax+0x10]`, `00584730`, `005DD890` (`0067B3CC`–`0067B407`) | [`0067B3CC`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00809950` (free), `001C2070`,
`00809054`/`001C2110` (scope+callback), `001EA050`, `00584730`, `0019CE20`,
`0019CC50`, `00673860`, `005DD890`, `00808C40`.

## The `005C9760` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`005C9760` is the slot-5 adapter for
`PClassDataMemberPhyreArray<PAnimation::PAnimationChannelTarget>`
(29 B): `rax = [rcx+0x18]`, `r9d = dword[rcx+0x48] - dword[rax+0xF4]`
(the array base minus the descriptor's element offset), then
`rcx = r9d + rdx`, `edx = r8d`, tail into `005C8CA0` (`005C9778`) —
the canonical Phyre member-array element accessor.

| member | role | interior |
| --- | --- | --- |
| `005C8CA0` (136 B) | the element accessor — `r8d = dword[rcx]` bound check vs `edx` (`005C8CAF`/`005C8CBC`), `rbx` = array record | [`005C8CBC`](../../_index/ADDRESS-INDEX.md) |
| `005AD2B0` (126 B) | array-record field copy — `esi=r8d`, `rbp=rdx`, `edi=ecx`, `edx=8` call setup (`005AD2CF`) | [`005AD2CF`](../../_index/ADDRESS-INDEX.md) |
| `005BED40` (118 B) | allocator-side helper — `qword[rsp+0x20] = -2` sentinel (`005BED53`), `006372A0` call (`005BED7E`) | [`005BED53`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `006372A0`. The sibling adapters
`005C9780`/`005C97A0`/`005C97C0`/`005C97E0` repeat the same
`[rcx+0x18]`/`-dword[rax+0xF4]` prologue into `005C8CA0` — same
family, separate census rows.

## The `005C97A0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`005C97A0` is the slot-5 adapter for
`PClassDataMemberPhyreArray<PAnimation::PAnimationDataSourceListEntry>`
(29 B): the same `[rcx+0x48] - dword[[rcx+0x18]+0xF4]` element-index
prologue as `005C9760`, tail into `005C8DC0` (`005C97B8`).

| member | role | interior |
| --- | --- | --- |
| `005C8DC0` (135 B) | the element accessor — `r8d = dword[rcx]` bound check vs `edx` (`005C8DCF`/`005C8DDC`), `rbx` = array record | [`005C8DDC`](../../_index/ADDRESS-INDEX.md) |
| `005AD3B0` (132 B) | array-record field copy — `esi=r8d`, `rbp=rdx`, `edi=ecx`, `edx=8` call setup (`005AD3D2`) | [`005AD3D2`](../../_index/ADDRESS-INDEX.md) |
| `005BEE50` (103 B) | allocator-side helper — `dword[rsp+0x18] = r10d` (`005BEE57`), `qword[rax] = r10` store (`005BEE7C`), `dword[r8-0x84] = r10d` (`005BEE85`) | [`005BEE7C`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none exclusive — the pair
`005C8CA0`/`005C8DC0` are sibling accessors for adjacent member
descriptors, not shared callees of each other.

## The `005C9780` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`005C9780` is the slot-5 adapter for
`PClassDataMemberPhyreArray<PAnimation::PAnimationConstantChannel>`
(29 B, the same `[rcx+0x48] - dword[[rcx+0x18]+0xF4]` index prologue),
tail `005C8D30` (`005C9798`).

| member | role | interior |
| --- | --- | --- |
| `005C8D30` (136 B) | element accessor — bound check `edx` vs `dword[rcx]`/`r8d` (`005C8D4C`/`005C8D50`), member call `005AD330` (`005C8D5D`) | [`005C8D5D`](../../_index/ADDRESS-INDEX.md) |
| `005AD330` (126 B) | field copy — `0017D260` resolve (`005AD359`), null test (`005AD361`) | [`005AD359`](../../_index/ADDRESS-INDEX.md) |

## The `005C97C0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`005C97C0` is the slot-5 adapter for
`PClassDataMemberPhyreArray<PAnimation::PAnimationEvent>` (29 B, same
prologue), tail `005C8E50` (`005C97D8`).

| member | role | interior |
| --- | --- | --- |
| `005C8E50` (135 B) | element accessor — bound check (`005C8E6C`/`005C8E70`), member call `005AD440` (`005C8E7D`) | [`005C8E7D`](../../_index/ADDRESS-INDEX.md) |
| `005AD440` (151 B) | field copy — `0017D260` resolve (`005AD46B`), null test (`005AD473`) | [`005AD46B`](../../_index/ADDRESS-INDEX.md) |

## The `005C97E0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`005C97E0` is the slot-5 adapter for
`PClassDataMemberPhyreArray<PAnimation::PAnimationNetworkInstanceTarget>`
(29 B, same prologue), tail `005C8EE0` (`005C97F8`).

| member | role | interior |
| --- | --- | --- |
| `005C8EE0` (135 B) | element accessor — bound check (`005C8EFC`/`005C8F00`), member call `005AD4E0` (`005C8F0D`) | [`005C8F0D`](../../_index/ADDRESS-INDEX.md) |
| `005AD4E0` (213 B) | field copy — `0017D260` resolve (`005AD511`), null test (`005AD519`) | [`005AD511`](../../_index/ADDRESS-INDEX.md) |

## The `0060D7F0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`0060D7F0` is the slot-5 adapter for
`PClassDataMemberPhyreArray<PRendering::PMeshInstanceSegmentContext>`
(29 B, same prologue), tail `0060C630` (`0060D808`).

| member | role | interior |
| --- | --- | --- |
| `0060C630` (136 B) | element accessor — bound check (`0060C64C`/`0060C650`), member call `005E32F0` (`0060C65D`) | [`0060C65D`](../../_index/ADDRESS-INDEX.md) |
| `005E32F0` (131 B) | field copy — `0017D260` resolve (`005E331D`), null test (`005E3325`) | [`005E331D`](../../_index/ADDRESS-INDEX.md) |
| `005FD170` (86 B) | small helper — `edx`/`rcx` null gates (`005FD17B`/`005FD187`) | [`005FD187`](../../_index/ADDRESS-INDEX.md) |

## The `0060D990` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`0060D990` is the slot-5 adapter for
`PClassDataMemberPhyreArray<PRendering::PShaderParameterDefinition>`
(29 B, same prologue), tail `0060C990` (`0060D9A8`).

| member | role | interior |
| --- | --- | --- |
| `0060C990` (136 B) | element accessor — bound check (`0060C9AC`/`0060C9B0`), member call `005E3820` (`0060C9BD`) | [`0060C9BD`](../../_index/ADDRESS-INDEX.md) |
| `005E3820` (131 B) | field copy — `0017D260` resolve (`005E384D`), null test (`005E3855`) | [`005E384D`](../../_index/ADDRESS-INDEX.md) |
| `005FD240` (85 B) | small helper — `edx`/`rcx` null gates (`005FD240`/`005FD269`) | [`005FD269`](../../_index/ADDRESS-INDEX.md) |

## The `006C2770` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`006C2770` is the slot-5 adapter for
`PClassDataMemberPhyreArray<PRendering::PShadowCaster::PShadowSplit>`
(29 B, same prologue), tail `006C26E0` (`006C2788`).

| member | role | interior |
| --- | --- | --- |
| `006C26E0` (135 B) | element accessor — bound check (`006C26FC`/`006C2700`), member call `006C1540` (`006C270D`) | [`006C270D`](../../_index/ADDRESS-INDEX.md) |
| `006C1540` (132 B) | field copy — `0017D260` resolve (`006C156C`), null test (`006C1574`) | [`006C156C`](../../_index/ADDRESS-INDEX.md) |
| `006C2320` (93 B) | small helper — `edx`/`rax` null gates (`006C232B`/`006C2347`) | [`006C2347`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside these censuses: `0017D260` (the resolve every
field copy shares). The six adapters are one codegen family — identical
prologue, one accessor + one field-copy per member descriptor.

## The `005C9800`-family exclusive subtrees — 17 roots, 34 members bound (SWE2-FRONTIER, followup queue)

Second wave of the array-adapter family documented above. Each root is
the same codegen: 29-B `PClassDataMemberPhyreArray` slot-5 adapter —
sign-extend the caller index (`movsxd rcx, r9d`), tail-jump to the
class-specific element helper — or the 33-B
`PClassDescriptorConcrete<PArray<…,8>>` slot-3 variant that calls
`005F13xx` first, then tail-jumps `005DExxx`. Every root owns exactly
two members: the element worker and the tail target.

| root | class (page row) | members | interior |
| --- | --- | --- | --- |
| `005C9800` | `PClassDataMemberPhyreArray<PAnimation::PAnimationSlotArray>` | `005AD5C0` (119-B element worker, `edx = 8`), `005C8F70` (tail) | [`005C980F`](../../_index/ADDRESS-INDEX.md) |
| `005C9820` | `PClassDataMemberPhyreArray<PAnimation::PAnimationSlotFilterDeferredLoad>` | `005AD640` (153 B), `005C9000` (tail) | [`005C982F`](../../_index/ADDRESS-INDEX.md) |
| `005C9880` | `PClassDataMemberPhyreArray<PQWord>` | `005AD840` (163 B), `005C91E0` (tail) | [`005C988F`](../../_index/ADDRESS-INDEX.md) |
| `00606FD0` | `PClassDescriptorConcrete<PArray<PRendering::PMaterialSwitch,8>>` | `005DE3D0` (tail), `005F13E0` (called) | [`00606FDC`](../../_index/ADDRESS-INDEX.md) |
| `00607070` | `PClassDescriptorConcrete<PArray<PRendering::PMeshInstanceSegmentContext,8>>` | `005DE460` (tail), `005F1600` (called) | [`0060707C`](../../_index/ADDRESS-INDEX.md) |
| `006070D0` | `PClassDescriptorConcrete<PArray<PRendering::PSceneRenderPass,8>>` | `005DE580` (tail), `005F1820` (called) | [`006070DC`](../../_index/ADDRESS-INDEX.md) |
| `0060D790` | `PClassDataMemberPhyreArray<PRendering::PContextVariantFoldingTable>` | `005E30E0` (193 B), `0060C480` (tail) | [`0060D79F`](../../_index/ADDRESS-INDEX.md) |
| `0060D7B0` | `PClassDataMemberPhyreArray<PRendering::PMaterialSwitch>` | `005E31B0` (153 B), `0060C510` (tail) | [`0060D7BF`](../../_index/ADDRESS-INDEX.md) |
| `0060D7D0` | `PClassDataMemberPhyreArray<PMatrix4>` | `005E3250` (147 B, `edx = 4`), `0060C5A0` (tail) | [`0060D7DF`](../../_index/ADDRESS-INDEX.md) |
| `0060D810` | `PClassDataMemberPhyreArray<PRendering::PNodeContext>` | `005E3410`, `0060C750` (tail) | [`0060D81F`](../../_index/ADDRESS-INDEX.md) |
| `0060D930` | `PClassDataMemberPhyreArray<PRendering::PShaderParameterCaptureBufferLocation>` | `005E3600`, `0060C7E0` (tail) | [`0060D93F`](../../_index/ADDRESS-INDEX.md) |
| `0060D950` | `PClassDataMemberPhyreArray<PRendering::PShaderParameterCaptureBufferLocationType>` | `005E36A0`, `0060C870` (tail) | [`0060D95F`](../../_index/ADDRESS-INDEX.md) |
| `0060D970` | `PClassDataMemberPhyreArray<PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer>` | `005E3750`, `0060C900` (tail) | [`0060D97F`](../../_index/ADDRESS-INDEX.md) |
| `0060D9B0` | `PClassDataMemberPhyreArray<PRendering::PShaderPass>` | `005E38B0`, `0060CA20` (tail) | [`0060D9BF`](../../_index/ADDRESS-INDEX.md) |
| `0060D9D0` | `PClassDataMemberPhyreArray<PRendering::PShaderPassInfo>` | `005E3960`, `0060CAB0` (tail) | [`0060D9DF`](../../_index/ADDRESS-INDEX.md) |
| `0060D9F0` | `PClassDataMemberPhyreArray<PRendering::PShaderStreamDefinition>` | `005E3A20`, `0060CB40` (tail) | [`0060D9FF`](../../_index/ADDRESS-INDEX.md) |
| `0060DA10` | `PClassDataMemberPhyreArray<PString>` | `005E3AE0`, `0060CBD0` (tail) | [`0060DA1F`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none beyond the listed members —
the adapters carry no other calls.

## The `0060DA30`–`00672E20` exclusive-subtree cluster — all 8 roots, 16 members bound (SWE2-FRONTIER, followup queue)

Eight more roots of the Phyre class-binding codegen family. Six are the
canonical **this-adjust slot-5 adapter**: `r9d = dword[rcx+0x48] -
dword[[rcx+0x18]+0xF4]`, `rcx = rdx + r9d`, `edx = r8d`, tail-jump to the
real member body. `006247F0` instead calls its member `006191F0(rdx)`
first and forwards `(rbx = r8, rdx = rax)` to `00616D80`; `0062F4E0` is
a plain `rcx = rdx; jmp 006361C0` forward.

| root | class (vtable index) | slot | member bodies |
| --- | --- | --- | --- |
| `0060DA30` | `PClassDataMemberPhyreSharray<unsigned int>` | 5 | `005FEF00` (iterate/serialize helper), `0060CC60` (adapter tail) |
| `006247F0` | `PClassDescriptorConcrete<PArray<PStreamInputDescD3D11,8>>` | 3 | `006191F0` (slot-3 body via `00682980`), `00616D80` (forward tail) |
| `00628490` | `PClassDataMemberPhyreArray<PStreamInputDescD3D11>` | 5 | `00617720` (helper), `00627C60` (adapter tail) |
| `0062F4E0` | `PClassDescriptorWithoutDefaultConstructor<PClassDataMemberDynamic>` | 14 | `006361C0` (`+0x58`/`+0x70` walk), `0063D410` |
| `0063DC60` | `PClassDataMemberPhyreSharray<PString>` | 5 | `006396C0` (helper), `0063D9C0` (adapter tail) |
| `00672DE0` | `PClassDataMemberPhyreArray<PDynamicSegmentDesc>` | 5 | `006652B0` (helper), `00672750` (adapter tail) |
| `00672E00` | `PClassDataMemberPhyreArray<PMeshSegment>` | 5 | `00665360` (helper), `006727E0` (adapter tail) |
| `00672E20` | `PClassDataMemberPhyreArray<PSkeletonJointBounds>` | 5 | `006653F0` (helper), `00672870` (adapter tail) |

Interior evidence: the six identical adapter prologues at
[`0060DA38`](../../_index/ADDRESS-INDEX.md),
[`00628498`](../../_index/ADDRESS-INDEX.md),
[`0063DC68`](../../_index/ADDRESS-INDEX.md),
[`00672DE8`](../../_index/ADDRESS-INDEX.md),
[`00672E08`](../../_index/ADDRESS-INDEX.md),
[`00672E28`](../../_index/ADDRESS-INDEX.md); the call-then-forward at
[`006247FC`](../../_index/ADDRESS-INDEX.md)/[`0062480C`](../../_index/ADDRESS-INDEX.md);
the plain forward at [`0062F4E3`](../../_index/ADDRESS-INDEX.md).

## The `00672E40`–`006D5650` exclusive-subtree cluster — all 12 roots, 24 members bound (SWE2-FRONTIER, followup queue)

Twelve more roots of the Phyre class-binding codegen family — eight
canonical **this-adjust slot-5 adapters** (`r9d = dword[rcx+0x48] -
dword[[rcx+0x18]+0xF4]`; `rcx = rdx + r9d`; `edx = r8d`; tail-jump),
three **slot-3 call-then-forward** bodies (`call member(rdx)`; `rcx = r8`,
`rdx = rax`; tail-jump), and one lazy-singleton slot-1 body.

| root | class (vtable index) | slot | members |
| --- | --- | --- | --- |
| `00672E40` | `PClassDataMemberPhyreArray<PSkinBoneRemap>` | 5 | `006654D0`, `00672900` |
| `0067E2E0` | `PClassDataMemberPhyreArray<PBitmapFontCharInfo>` | 5 | `0067CF00`, `0067E250` |
| `006AF740` | `PClassDataMemberPhyreArray<PTypedObject>` | 5 | `006AE270`, `006AF6B0` |
| `006BE6E0` | `PClassDataMemberPhyreArray<PModifierNetworkDynamicMeshSegment>` | 5 | `006BC5D0`, `006BE5C0` |
| `006BE700` | `PClassDataMemberPhyreArray<PRenderStream>` | 5 | `006BC6A0`, `006BE650` |
| `006D5610` | `PClassDataMemberPhyreArray<PModifierAndInputs>` | 5 | `006D0B20`, `006D5460` |
| `006D5630` | `PClassDataMemberPhyreArray<PModifierNetworkBuffer>` | 5 | `006D0BD0`, `006D54F0` |
| `006D5650` | `PClassDataMemberPhyreArray<PRenderStreamInput>` | 5 | `006D0CA0`, `006D5580` |
| `006BB3C0` | `PClassDescriptorConcrete<PModifierNetworkDynamicMesh>` | 3 | `006BBD30`, `006BBDF0` |
| `006C2630` | `PClassDescriptorConcrete<PArray<PShadowSplit,8>>` | 3 | `006C1060`, `006C1C50` |
| `006C4D90` | `PClassDescriptorConcrete<PLODGroup>` | 3 | `006C5420`, `006C5580` |
| `006A4100` | `PPhysics::PUtilityPhysics` | 1 | `0069E790`, `0069E880` |

`006A4100` is the different shape: `byte[01F2CDF0]` clear →
`call qword[[01F2E9B8]+8]` — a lazy singleton init through the stored
vtable (`006A4104`/`006A411B`). Its two members are the CRT TLS-guard
twins: `gs:[0x58]` indexed by `dword[02EAED3C]` with guard objects at
`02E4BDC8`/`02E4BDF0` (`0069E79F`/`0069E7A5`, `0069E88F`/`0069E895`).

Interior evidence: adapter prologues at
[`00672E48`](../../_index/ADDRESS-INDEX.md),
[`0067E2E8`](../../_index/ADDRESS-INDEX.md),
[`006AF748`](../../_index/ADDRESS-INDEX.md),
[`006BE6E8`](../../_index/ADDRESS-INDEX.md),
[`006BE708`](../../_index/ADDRESS-INDEX.md),
[`006D5618`](../../_index/ADDRESS-INDEX.md),
[`006D5638`](../../_index/ADDRESS-INDEX.md),
[`006D5658`](../../_index/ADDRESS-INDEX.md); call-then-forward at
[`006BB3CC`](../../_index/ADDRESS-INDEX.md),
[`006C263C`](../../_index/ADDRESS-INDEX.md),
[`006C4D9C`](../../_index/ADDRESS-INDEX.md); lazy-init at
[`006A411B`](../../_index/ADDRESS-INDEX.md).

## The `00199D50` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00199D50` is a **scalar deleting destructor** — vtable slot 0 of the
class whose ctor is the member (`00199C30` installs the `008F3C68`
vtable, RTTI locator `01CEC978`, `00199C4C`). The body runs the dtor
then tests `dil` bits 0 and 4 for the free (`00199D6F`/`00199D75`).

| member | role | interior |
| --- | --- | --- |
| `00199C30` | class ctor — installs vtable `008F3C68` under EH guard | [`00199C4C`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none beyond the dtor chain.

## The `001E1D90`–`0020D010` exclusive-subtree cluster — all 7 roots bound (SWE2-FRONTIER, followup queue)

Six **scalar deleting destructors** — `call <dtor body>; test bl, 1` then
the free (`001E1D9F`/`001E1DA4` is canonical) — and one singleton
forwarder:

| root | class (vtable index) | slot | member |
| --- | --- | --- | --- |
| `001E1D90` | `MapRenderObject` | 0 | `001E1C90` (dtor body) |
| `001F52F0` | `CharacterRenderObject` | 0 | `001F51E0` (dtor body) |
| `00204AF0` | `std::regex _Node_class<char>` | 0 | `002043A0` (dtor body) |
| `00204BD0` | `_Node_assert` | 0 | `002045E0` (dtor body) |
| `00204C70` | `_Node_if` | 0 | `00204660` (dtor body) |
| `0020D010` | `AmdAdapterInfo` | 2 | `0020D720` (dtor body) |
| `001F2F30` | `DisableMsaaObj` | 1 | `00186130` (forward target via `00189120`) |

Interior evidence: deleting-dtor flag tests at
[`001E1DA4`](../../_index/ADDRESS-INDEX.md),
[`001F5304`](../../_index/ADDRESS-INDEX.md),
[`00204B04`](../../_index/ADDRESS-INDEX.md),
[`00204BE4`](../../_index/ADDRESS-INDEX.md),
[`00204C84`](../../_index/ADDRESS-INDEX.md),
[`0020D024`](../../_index/ADDRESS-INDEX.md); the `DisableMsaaObj`
forwarder tail at [`001F2F40`](../../_index/ADDRESS-INDEX.md).

Shared callees outside the census: `00189120`.

## The `005A2920`/`005A2CD0`/`005A3710`/`005AC950`/`005ACD30`/`005C55C0`/`005C56D0`/`005C5700`/`005C5730`/`005C58B0` exclusive-subtree cluster — all 10 roots bound (SWE2-FRONTIER, followup queue)

Two codegen patterns. Eight are `mov rcx, rdx; mov rbx, r8; call
005Bxxxx` slot-3 `PClassDescriptorConcrete` adapters; two are slot-0
bodies opening with the `qword[rsp+0x20] = -2` EH-state stamp.

| root | class (slot) | member (body) | interior |
| --- | --- | --- | --- |
| `005A2920` | `PClassDescriptorConcrete<PAnimatableComponent>` (3) | `005AA710` | [`005A292C`](../../_index/ADDRESS-INDEX.md) |
| `005A2CD0` | `PClassDescriptorConcrete<PAnimationSlotFilter>` (3) | `005AAB10` | [`005A2CD6`](../../_index/ADDRESS-INDEX.md) |
| `005A3710` | `PClassDescriptorConcrete<PAnimationSet>` (3) | `005AAA90` | [`005A3716`](../../_index/ADDRESS-INDEX.md) |
| `005AC950` | `PAnimationAdditiveBlenderController` (0) | `005A9CF0` | [`005AC956`](../../_index/ADDRESS-INDEX.md) |
| `005ACD30` | `PAnimationSlotFilter` (0) | `005AA0E0` | [`005ACD36`](../../_index/ADDRESS-INDEX.md) |
| `005C55C0` | `PClassDescriptorConcrete<PArray<float,4>>` (3) | `005B83B0` (`or edx, -1`) | [`005B83BF`](../../_index/ADDRESS-INDEX.md) |
| `005C56D0` | `PClassDescriptorConcrete<PArray<PAnimationChannelTarget,8>>` (3) | `005B86E0` | [`005C56D6`](../../_index/ADDRESS-INDEX.md) |
| `005C5700` | `PClassDescriptorConcrete<PArray<PAnimationConstantChannel,8>>` (3) | `005B87F0` | [`005C5706`](../../_index/ADDRESS-INDEX.md) |
| `005C5730` | `PClassDescriptorConcrete<PArray<PAnimationDataSourceListEntry,8>>` (3) | `005B8900` | [`005C5736`](../../_index/ADDRESS-INDEX.md) |
| `005C58B0` | `PClassDescriptorConcrete<PArray<PAnimationSlotFilterDeferredLoad,8>>` (3) | `005B8D40` | [`005C58B6`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: the `005Bxxxx`/`005AAxxx` bodies.

## The `005C5950`-`006072E0` exclusive-subtree cluster — 14 roots bound (SWE2-FRONTIER, followup queue)

Three codegen patterns again: the `mov rcx, rdx; mov rbx, r8; call
member` slot-3 adapter, the `this+0x18`/`this+0x48`/`-[rax+0xF4]`
offset adapter (slot 5), and the `mov rcx, rdx; jmp member` tail
thunk (slot 10).

| root | class (slot) | member (body) | interior |
| --- | --- | --- | --- |
| `005C5950` | `PClassDescriptorConcrete<PArray<PBlendableAnimationS…>>` (3) | `005B8F60` | [`005C5956`](../../_index/ADDRESS-INDEX.md) |
| `005C59F0` | `PClassDescriptorConcrete<PSharray<PAnimationClip*>>` (3) | `005B9180` | [`005C59F6`](../../_index/ADDRESS-INDEX.md) |
| `005C9740` | `PClassDataMemberPhyreArray<float>` (5) | `005C8BF0` | [`005C9740`](../../_index/ADDRESS-INDEX.md) |
| `005C9840` | `PClassDataMemberPhyreArray<PAnimationSlotListIndex>` (5) | `005C9090` | [`005C9840`](../../_index/ADDRESS-INDEX.md) |
| `005CDC90` | `PClassDescriptorConcrete<PShaderPassInfo>` (3) | `005DFC20` | [`005CDC96`](../../_index/ADDRESS-INDEX.md) |
| `005D1870` | `PClassDescriptorHeaderWithoutDefaultConstructor<PParameterBuffer>` (10) | `005EB560` (tail `jmp`) | [`005D1873`](../../_index/ADDRESS-INDEX.md) |
| `005D2850` | `PClassDescriptorConcrete<PSceneRenderPass>` (3) | `005DEBA0` | [`005D2856`](../../_index/ADDRESS-INDEX.md) |
| `005D4B70` | `PClassDescriptorWithoutDefaultConstructor<PMaterial>` (10) | `005EB4F0` (tail `jmp`) | [`005D4B73`](../../_index/ADDRESS-INDEX.md) |
| `005D5300` | `PClassDescriptorConcrete<PEffect>` (3) | `005DEA00` | [`005D5306`](../../_index/ADDRESS-INDEX.md) |
| `006070A0` | `PClassDescriptorConcrete<PArray<PNodeContext,8>>` (3) | `005F1710` | [`006070A6`](../../_index/ADDRESS-INDEX.md) |
| `00607100` | `PClassDescriptorConcrete<PArray<PShader,8>>` (3) | `005F1930` | [`00607106`](../../_index/ADDRESS-INDEX.md) |
| `00607280` | `PClassDescriptorConcrete<…>` (3) | `005F1D70` | [`00607286`](../../_index/ADDRESS-INDEX.md) |
| `006072B0` | `PClassDescriptorConcrete<…>` (3) | `005F1E80` | [`006072B6`](../../_index/ADDRESS-INDEX.md) |
| `006072E0` | `PClassDescriptorConcrete<…>` (3) | `005F1F90` | [`006072E6`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: the `005Bxxxx`/`005DExxx`/`005EBxxx`/
`005F1xxx` class bodies.

## The `00607310`-`0063C1F0` exclusive-subtree cluster — 12 roots bound (SWE2-FRONTIER, followup queue)

Same three codegen patterns; `006340F0`/`006342B0`/`006421B0` are
slot-0 EH-state bodies (`qword[rsp+0x20] = -2`).

| root | class (slot) | member (body) | interior |
| --- | --- | --- | --- |
| `00607310` | `PClassDescriptorConcrete<PArray<PShaderStreamDefinition,8>>` (3) | `005F20A0` | [`00607316`](../../_index/ADDRESS-INDEX.md) |
| `00607340` | `PClassDescriptorConcrete<PArray<PString,8>>` (3) | `005F21B0` | [`00607346`](../../_index/ADDRESS-INDEX.md) |
| `00607370` | `PClassDescriptorConcrete<PSharray<unsigned int>>` (3) | `005F22C0` | [`00607376`](../../_index/ADDRESS-INDEX.md) |
| `006073A0` | `PClassDescriptorConcrete<PSharray<PMeshInstanceSegmentStr…>>` (3) | `005F23D0` | [`006073A6`](../../_index/ADDRESS-INDEX.md) |
| `00611600` | `PClassDescriptorWithoutDefaultConstructor<PShaderVertexProgramD3D11>` (10) | `006188E0` (tail `jmp`) | [`00611603`](../../_index/ADDRESS-INDEX.md) |
| `00612570` | `PClassDescriptorWithoutDefaultConstructor<PShaderComputeProgramD3D11>` (10) | `006187F0` (tail `jmp`) | [`00612573`](../../_index/ADDRESS-INDEX.md) |
| `0062F510` | `PClassDescriptorWithoutDefaultConstructor<PClassDataMemberDynamic>` (10) | `00635CC0` (tail `jmp`) | [`0062F513`](../../_index/ADDRESS-INDEX.md) |
| `0062FB30` | `PClassDescriptorWithoutDefaultConstructor<PClassDescriptorDynamic>` (10) | `00636280` (tail `jmp`) | [`0062FB33`](../../_index/ADDRESS-INDEX.md) |
| `006340F0` | `PClassDataMemberDynamic` (0) | `00633300` | [`006340F6`](../../_index/ADDRESS-INDEX.md) |
| `006342B0` | `PClassDescriptorDynamic` (0) | `00633590` | [`006342B6`](../../_index/ADDRESS-INDEX.md) |
| `0063C1F0` | `PClassDescriptorConcrete<PSharray<PString>>` (3) | `006364B0` | [`0063C1F6`](../../_index/ADDRESS-INDEX.md) |
| `006421B0` | `PClassDescriptorConcrete<PPostProcessing::PGlow>` (0) | `00645DF0` | [`006421B9`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: the `005F2xxx`/`00618xxx`/`00635xxx`/
`00633xxx`/`00645xxx` class bodies.

## The `00642FD0`-`00680D80` exclusive-subtree cluster — 14 roots bound (SWE2-FRONTIER, followup queue)

Same codegen families: slot-3 `call` adapters, slot-5
`this+0x18`/`+0x48`/`−[rax+0xF4]` offset adapters, slot-0
`qword[rsp+0x20] = -2` EH bodies.

| root | class (slot) | member (body) | interior |
| --- | --- | --- | --- |
| `00642FD0` | `PClassDescriptorConcrete<PPostProcessing::PPostEffectManager>` (3) | `0064D0D0` | [`00642FD6`](../../_index/ADDRESS-INDEX.md) |
| `00643530` | `PClassDescriptorConcrete<PPostProcessing::PMeshParticleSystemBase>` (0) | `00645F30` | [`00643539`](../../_index/ADDRESS-INDEX.md) |
| `00643810` | `PClassDescriptorConcrete<PPostProcessing::PPostEffectBase>` (3) | `0064CFB0` | [`00643816`](../../_index/ADDRESS-INDEX.md) |
| `0065E7E0` | `PClassDescriptorConcrete<PGeometry::PDynamicDataBlock>` (3) | `0066BE00` | [`0065E7E6`](../../_index/ADDRESS-INDEX.md) |
| `0065EF40` | `PClassDescriptorConcrete<PGeometry::PMesh>` (3) | `0066C500` | [`0065EF46`](../../_index/ADDRESS-INDEX.md) |
| `00661220` | `PClassDescriptorConcrete<PGeometry::PShape>` (3) | `0066C900` | [`00661226`](../../_index/ADDRESS-INDEX.md) |
| `00671350` | `PClassDescriptorConcrete<PArray<PDataBlockD3D11,8>>` (3) | `0066B070` | [`00671356`](../../_index/ADDRESS-INDEX.md) |
| `006713F0` | `PClassDescriptorConcrete<PArray<PMeshSegment,8>>` (3) | `0066B290` | [`006713F6`](../../_index/ADDRESS-INDEX.md) |
| `00671570` | `PClassDescriptorConcrete<PSharray<PMaterial*>>` (3) | `0066B6D0` | [`00671576`](../../_index/ADDRESS-INDEX.md) |
| `006715A0` | `PClassDescriptorConcrete<PSharray<PDataBlockBufferD3D11>>` (3) | `0066B7E0` | [`006715A6`](../../_index/ADDRESS-INDEX.md) |
| `006715D0` | `PClassDescriptorConcrete<PSharray<PIndexDataBlockBufferD3D11>>` (3) | `0066B8F0` | [`006715D6`](../../_index/ADDRESS-INDEX.md) |
| `00672E80` | `PClassDataMemberPhyreSharray<PDataBlockBufferD3D11>` (5) | `00672A20` | [`00672E88`](../../_index/ADDRESS-INDEX.md) |
| `00672EA0` | `PClassDataMemberPhyreSharray<PIndexDataBlockBufferD3D11>` (5) | `00672AD0` | [`00672EA8`](../../_index/ADDRESS-INDEX.md) |
| `00680D80` | `PClassDescriptorWithoutDefaultConstructor<PScripting::PScheduler>` (0) | `00681560` | [`00680D89`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: the `0064xxxx`/`0066xxxx`/`00672Axx`
class bodies.

## The `00680F80`-`006BED20` exclusive-subtree cluster — 14 roots bound (SWE2-FRONTIER, followup queue)

Same codegen families; `00684D10` is a full body (`mov rax, rsp` +
four-register save), `006AFB00` a tail thunk, `006BED20` a
`rbx = edx` body.

| root | class (slot) | member (body) | interior |
| --- | --- | --- | --- |
| `00680F80` | `PClassDescriptorConcrete<PScripting::PScript>` (3) | `00681A00` | [`00680F86`](../../_index/ADDRESS-INDEX.md) |
| `00681BF0` | `PScripting::PScheduler` (2) | `00681880` | [`00681BF6`](../../_index/ADDRESS-INDEX.md) |
| `00684D10` | `PClassCallableMethodScript::PCallerScript` (1) | `00682AA0` | [`00684D10`](../../_index/ADDRESS-INDEX.md) |
| `0068B0E0` | `PClassDescriptorConcrete<PPhysicsInterfaceBullet>` (3) | `00692660` | [`0068B0E6`](../../_index/ADDRESS-INDEX.md) |
| `0068D850` | `PClassDescriptorConcrete<PPhysicsCharacterCamera>` (3) | `00692080` | [`0068D856`](../../_index/ADDRESS-INDEX.md) |
| `006A4010` | `PClassDescriptorConcrete<PSharray<PPhysicsShape*>>` (3) | `00698D00` | [`006A4016`](../../_index/ADDRESS-INDEX.md) |
| `006A7B70` | `PClassDescriptorConcrete<PGameplay::PTrigger>` (3) | `006A7C70` | [`006A7B76`](../../_index/ADDRESS-INDEX.md) |
| `006A9190` | `PClassDescriptorConcrete<PSharray<PTriggerReceiverComponent*>>` (3) | `006A8810` | [`006A9196`](../../_index/ADDRESS-INDEX.md) |
| `006A95F0` | `PClassDescriptorConcrete<PQuarryComponent>` (10) | `006A97C0` | [`006A95F9`](../../_index/ADDRESS-INDEX.md) |
| `006ADE40` | `PClassDescriptorConcrete<PInstancesComponent>` (3) | `006ADF90` | [`006ADE46`](../../_index/ADDRESS-INDEX.md) |
| `006AFB00` | `PClassDescriptorWithoutDefaultConstructor<PNameComponent>` (10) | `006AFDC0` (tail `jmp`) | [`006AFB03`](../../_index/ADDRESS-INDEX.md) |
| `006B3DB0` | `PClassDescriptorConcrete<PScene::PNode>` (3) | `006B40C0` | [`006B3DB6`](../../_index/ADDRESS-INDEX.md) |
| `006BB930` | `PDynamicGeometry::PModifierNetworkDynamicMesh` (0) | `006BBC70` | [`006BB936`](../../_index/ADDRESS-INDEX.md) |
| `006BED20` | `PRendering::PLightType` (0) | `006BEC40` | [`006BED2A`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: the `0068xxxx`-`006BExxx` class
bodies.

## The `006C0860`-`007917B0` exclusive-subtree cluster — 15 roots bound (SWE2-FRONTIER, followup queue)

Same codegen families; `006CCEC0`/`006CD830`/`007917B0` are `mov
rcx, rdx; jmp member` tail thunks, `006C0860`/`006C4D60` slot-0/10
EH-state bodies, `006C1500`/`006CB7D0` `rbx = edx` bodies.

| root | class (slot) | member (body) | interior |
| --- | --- | --- | --- |
| `006C0860` | `PClassDescriptorConcrete<PShadowCaster>` (10) | `006C0EB0` | [`006C0869`](../../_index/ADDRESS-INDEX.md) |
| `006C0AC0` | `PClassDescriptorConcrete<PShadowCaster::PShadowSplit>` (3) | `006C10F0` | [`006C0AC6`](../../_index/ADDRESS-INDEX.md) |
| `006C1500` | `PRendering::PShadowCasterType` (0) | `006C0FE0` | [`006C150A`](../../_index/ADDRESS-INDEX.md) |
| `006C2DB0` | `PClassDescriptorConcrete<PModifierNetworkInstance>` (3) | `006C30F0` | [`006C2DB6`](../../_index/ADDRESS-INDEX.md) |
| `006C4D60` | `PClassDescriptorConcrete<PLOD::PLODGroup>` (10) | `006C5180` | [`006C4D69`](../../_index/ADDRESS-INDEX.md) |
| `006C7860` | `PClassDescriptorConcrete<PArray<PLODLevel,8>>` (3) | `006C6A40` | [`006C7866`](../../_index/ADDRESS-INDEX.md) |
| `006C7890` | `PClassDescriptorConcrete<PSharray<PMeshInstance*>>` (3) | `006C6B50` | [`006C7896`](../../_index/ADDRESS-INDEX.md) |
| `006CB7D0` | `Yebis::YebisPfxMemoryAllocatorD3D11` (3) | `006CBB20` | [`006CB7DA`](../../_index/ADDRESS-INDEX.md) |
| `006CCEC0` | `PClassDescriptorAbstract<PScriptableComponent>` (12) | `006CD000` (tail `jmp`) | [`006CCEC0`](../../_index/ADDRESS-INDEX.md) |
| `006CD830` | `PClassDescriptorWithoutDefaultConstructor<PTriggerReceiverTypeCallbackData>` (10) | `006CDB70` (tail `jmp`) | [`006CD833`](../../_index/ADDRESS-INDEX.md) |
| `006CDF60` | `PClassDescriptorConcrete<PTriggerReceiverComponent>` (3) | `006CE0D0` | [`006CDF66`](../../_index/ADDRESS-INDEX.md) |
| `006CE710` | `PClassDescriptorConcrete<PModifierNetwork>` (3) | `006D0450` | [`006CE716`](../../_index/ADDRESS-INDEX.md) |
| `006CF510` | `PClassDescriptorConcrete<PModifierAndInputs>` (3) | `006D03D0` | [`006CF516`](../../_index/ADDRESS-INDEX.md) |
| `006D5010` | `PClassDescriptorConcrete<PArray<PModifierAndInputs,8>>` (3) | `006D3350` | [`006D5016`](../../_index/ADDRESS-INDEX.md) |
| `007917B0` | `PClassDescriptorWithoutDefaultConstructor<PApplicationViewport>` (10) | `00796180` (tail `jmp`) | [`007917B3`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: the `006Cxxxx`/`006D0xxx`
class bodies.

## The `00867160`-`0086AE70` exclusive-subtree cluster — 6 roots bound (SWE2-FRONTIER, followup queue)

The `PInputs` descriptor family: five slot-10 EH-state bodies
(`qword[rsp+0x20] = -2`, `rdx` mirrored to `[rsp+0x50]`) and one
slot-3 `call` adapter.

| root | class (slot) | member (body) | interior |
| --- | --- | --- | --- |
| `00867160` | `PClassDescriptorConcrete<PInputSourceMouseDeltaY>` (10) | `0086C5F0` | [`00867169`](../../_index/ADDRESS-INDEX.md) |
| `008684C0` | `PClassDescriptorConcrete<PInputAction>` (3) | `0086ED10` | [`008684CC`](../../_index/ADDRESS-INDEX.md) |
| `00868C10` | `PClassDescriptorConcrete<PInputSourceKey>` (10) | `0086C4C0` | [`00868C19`](../../_index/ADDRESS-INDEX.md) |
| `00869670` | `PClassDescriptorConcrete<PInputSourceJoypadButton>` (10) | `0086C460` | [`00869679`](../../_index/ADDRESS-INDEX.md) |
| `0086A5D0` | `PClassDescriptorConcrete<PInputSourceMouseButton>` (10) | `0086C520` | [`0086A5D9`](../../_index/ADDRESS-INDEX.md) |
| `0086AE70` | `PClassDescriptorConcrete<PInputSourceMouseDeltaX>` (10) | `0086C590` | [`0086AE79`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none beyond the listed members.

## Interior citation — frontier hub `005FD050` (2026-09-17, SWE2-EC7)

`005FD050` — 129 B, 39 frontier callers at census (all in the `0060xxxx`/`0061xxxx` Phyre
descriptor band). Interior verified: [`005FD065`](../../_index/ADDRESS-INDEX.md) is
`mov rax, gs:[0x58]` — the MSVC magic-static lazy-singleton getter: reads the TLS slot index at
`02EAED3C`, checks the epoch at `02CE2610`, runs `_Init_thread_header`/`_Init_thread_footer`
(`008092FC`/`0080929C`) around a one-time `00615840` construction of the object at `02CC0410`
with an `00808B90` (`atexit`) registration of `008ADDD0` — the teardown body, not a census function — and returns `02CC0410`. The shared
descriptor-table singleton the reflection band resolves through.

NOT claimed: the object's class (its ctor `00615840` is cited on the class-descriptor page, but
the singleton's type name is not established here).


## Interior citation — frontier hub `00646C00` (2026-09-18, SWE2-EC7)

`00646C00` — 170 B, 6 A-measured callers; the tagged-pair move-assign behind several vtable
slots on this page. Interior verified: `btr esi, 0x1F` strips the sign/ownership bit from the
source tag dword (`00646C1F`), selects `[rdx+8]` vs `rdx+8`-literal by the low tag
(`00646C31`–`00646C3B`), calls `006A8C90` to clone the payload
([`00646C3D`](../../_index/ADDRESS-INDEX.md)), then — only when the destination tag says owned
(`shr edx,0x1F` at `00646C6E`) and the old pointer differs from both sentinels — releases it via
`00584730` ([`00646C7D`](../../_index/ADDRESS-INDEX.md)) before installing `{newtag, newptr}`
at `00646C82`/`00646C8C`. The bit-31 convention is the owned/borrowed flag.


## Interior citation — frontier hubs `001D5630`, `001D5620` (2026-09-18, SWE2-EC7)

`001D5630` — 21 B, 14 callers; `001D5620` — 15 B, 14 callers. The gated tail-forward pair
this index's slot readers share. Interior verified: both test `byte [rcx+8] != 0`
(`001D5630`/`001D5620`) — set, `001D5630` forwards `(rdx, r8)` to `00609AC0`
([`001D563F`](../../_index/ADDRESS-INDEX.md)) and `001D5620` forwards `rdx` to `00609A30`
([`001D5629`](../../_index/ADDRESS-INDEX.md)); clear, both return silently. The `+8` flag is
the "armed" check on the vtable record.

## SWE2-EC7-33 update (2026-09-19) - `001C0F20`

`001C0F20` (2,028 B) is the `008F6600`-vtable object body - 10 `001EDF00` string copies, the `"EASTL basic_string"` vtable string, `00861EC0`/`00584730`/`0017D260`/`00189120`/`00210EC0`/`001EA830`. Interior anchor `001C1121` (an `001EDF00` copy).

## SWE2-EC7-34 update (2026-09-19) - `00615840`

`00615840` (887 B) is an object init - `005DC0E0` base ctor, zeroes `[rbp+0x108]`/`[+0x110]`, `00861EC0`/`006160B0`/`00615ED0`/`005DC1C0`/`005DBF30`/`006C8750`. Interior anchor `00615863` (the `005DC0E0` call).

## SWE2-EC7-35 update (2026-09-19) - `00863850`

`00863850` (738 B) is an exception-thunk body - the `008C5F80`-`008C5FD0` rdata run, `001EE650`/`0016D6A0`/`00808C40`. Interior anchor `00863882` (an `00808C40` call).

## SWE2-EC7-35 update (2026-09-19) - `00602A40`

`00602A40` (697 B) is an object-model record body - `02CBBE00`/`02CBC018`/`02CBC368` state, `00861EBA`/`0060E5A0`/`001B81B0`/`00194540`. Interior anchor `00602A9A` (an `00861EBA` call).

## SWE2-EC7-36 update (2026-09-19) - `00213140`

`00213140` (644 B) is an object-model body - `008C5F80`-`008C5FD0` rdata run, `002133D0`/`00189120` pairs plus `001EE7C0`/`001EE650`/`00808C40`. Interior anchor `002131A8` (a `002133D0` call).

## SWE2-EC7-37 update (2026-09-19) - `00682AA0`

`00682AA0` (595 B) is a Phyre object init - `00D6FE30`/`00D6FDE0`/`00D6FE70`, `"PhyreObject"` string, `00811130`/`005CDAA0`/`00811950` pairs plus `0080F420`/`008119F0`/`00810620`/`00811640`. Interior anchor `00682AEB` (an `0080F420` call).

## SWE2-EC7-37 update (2026-09-19) - `006A0BF0`

`006A0BF0` (520 B) is a call-free SIMD absolute-value pass - loads the `0x80000000` sign mask from `01CEBDA0` into `xmm3`, walks a float array `r9d`-wide (4-unrolled `comiss`/`xorps` loop) writing `|value|` into `[rcx+0x34..]`. Interior anchor `006A0BFA` (the sign-mask load).

## SWE2-EC7-37 update (2026-09-19) - `00864F30`

`00864F30` (512 B) is a vtable-family body - `008C5D68`, `0039D1D0`/`00189120`/`00186670`/`00678B50`/`0039D1F0`/`0039D1E0`. Interior anchor `00864F57` (a `0039D1D0` call).

## SWE2-EC7-41 update (2026-09-19) - `001F3740`

`001F3740` (355 B) is the `RenderSSSObj`/`btSphereShape` vtable row body - `"Post Process : sss"` string, `009034C8`/`01DFE0C4`/`01F7F4E0`/`02CB8434`, `00609710`/`00600A60`/`001D5630`/`00189120` triple/`001867A0`/`00186660`. Interior anchor `001F377D` (a `00609710` call).

## SWE2-EC7-41 update (2026-09-19) - `00633590`

`00633590` (331 B) is a vtable row body - `00D58380`, `00638F00` plus `00584730` quadruple. Interior anchor `00633604` (a `00638F00` call).

## SWE2-EC7-42 update (2026-09-19) - `001F2A20`

`001F2A20` (323 B) is the `CopyBufferObj`/`btInternalTriangleIndexCallback` vtable row body - `"CopyBufferObj::render"` string, `00903408`/`01F7F4E0`, `001D5630`/`00609710`/`00189120` quadruple/`001868F0`/`001867B0`/`005FEFD0`. Interior anchor `001F2A49` (a `001D5630` call).

## SWE2-EC7-42 update (2026-09-19) - `00673860`

`00673860` (305 B) is a vtable row body - `001B7170`/`001C2720` plus `00584730` quadruple. Interior anchor `0067388D` (an `001B7170` call).

## SWE2-EC7-42 update (2026-09-19) - `00609AC0`

`00609AC0` (302 B) is a vtable row body - `01CEB638`, `00600B30`/`00861EBA`. Interior anchor `00609B17` (a `00600B30` call).

## SWE2-EC7-42 update (2026-09-19) - `006CB810`

`006CB810` (299 B) is a vtable row body - `008C2B40`, `00680150`/`006CBA20`/`0067F700`/`00680200`. Interior anchor `006CB83F` (a `00680150` call).

## SWE2-EC7-43 update (2026-09-19) - `00209CD0`

`00209CD0` (292 B) is a vtable row body - `008C2470` vtable store. Interior anchor `00209D61` (the store site).

## SWE2-EC7-43 update (2026-09-19) - `006A1940`

`006A1940` (291 B) is a vtable row body - `00683BF0`/`00684080`/`0069E230`/`0080F420`/`00810620`/`00811130`/`00811470`/`00811640`. Interior anchor `006A1972` (a `00683BF0` call).

## SWE2-EC7-43 update (2026-09-19) - `0069F570`

`0069F570` (279 B) is a call-free 3x3 transform + lerp - copies `[rdx+0x20]`/`[rdx]`, `r8b` picks a direct `movaps` copy or a 3x3 `mulss` matrix-vector product into `[rcx+0x40]`, then lerps `[rcx+0x20]`/`[rcx+0x30]` rows by `t` into `[rcx+0x50..0x58]` (`01CEBBA8` = 1.0f). Interior anchor `0069F627` (the lerp tail).

## SWE2-EC7-44 update (2026-09-19) - `001F2D40`

`001F2D40` (252 B) is the `CopyFrontBufferForVFXObj` slot-1 body - `001867B0`/`00186990`/`001869E0`/`00188730`/`00189120`/`001D5620`/`001D5630`. Interior anchor `001F2D5D` (an `001867B0` call).

## SWE2-EC7-44 update (2026-09-19) - `00212E70`

`00212E70` (253 B) is a body - `001867E0`/`00186800`/`00189120`/`00190260`/`00193D50`/`00600A60`. Interior anchor `00212E98` (an `001867E0` call).

## SWE2-EC7-44 update (2026-09-19) - `00684C10`

`00684C10` (253 B) is a vtable row body - `006372A0`/`00682980`/`00683350`/`006836B0`/`00683B50`/`0080F420`/`00810580` plus a `call [rsi+8]` vcall. Interior anchor `00684C39` (a `006372A0` call).

## SWE2-EC7-45 update (2026-09-19) - `006A1670`

`006A1670` (246 B) is a vtable row body - `00683BF0`/`00684080`/`0069E230`/`0080F420`/`00810620`/`00811130`/`00811470` plus a `call [rdi+8]` vcall. Interior anchor `006A169D` (a `00683BF0` call).

## SWE2-EC7-45 update (2026-09-19) - `006A1840`

`006A1840` (246 B) is a vtable row body - `00683BF0`/`00684080`/`0069E230`/`0080F420`/`00810620`/`00811130`/`00811640` plus a `call [rdi+8]` vcall. Interior anchor `006A1866` (a `00683BF0` call).

## SWE2-EC7-45 update (2026-09-19) - `00686180`

`00686180` (242 B) is a body - `005A6670`/`005CDAA0`/`006372A0` plus a `call [r15+8]` vcall. Interior anchor `006861CC` (a `005A6670` call).

## SWE2-EC7-46 update (2026-09-19) - `001F2C50`

`001F2C50` (233 B) is `CopyFrontBufferForChrRefraction` - `001867B0`/`00186A80`/`00188730`/`00189120`/`001BC000`/`001D5620`/`001D5630`. Interior anchor `001F2C59` (an `001867B0` call).

## SWE2-EC7-46 update (2026-09-19) - `001F2E40`

`001F2E40` (226 B) is `CopyFrontBufferForWaterRefraction` - `001867B0`/`00186A80`/`00188730`/`00189120`/`001A7750`/`001A9930`/`001D5620`. Interior anchor `001F2E49` (an `001867B0` call).

## SWE2-EC7-46 update (2026-09-19) - `001B81B0`

`001B81B0` (225 B) is a body - `005C5230`/`00861EBA`. Interior anchor `001B8217` (a `005C5230` call).

## SWE2-EC7-46 update (2026-09-19) - `006BFED0`

`006BFED0` (234 B) is a body - `006BFB10`/`00811130`/`00811640` plus a `call [rdi+8]` vcall. Interior anchor `006BFEFF` (a `006BFB10` call).

## SWE2-EC7-46 update (2026-09-19) - `006A3C20`

`006A3C20` (230 B) is a call-free jump-table unit-vector writer - `cmp r8d,5` case dispatch, `01CEBDA0` sign mask, stores `0x3F800000`/`0xBF800000` components into `rdx`. Interior anchor `006A3C41` (the table index load).

## SWE2-EC7-47 update (2026-09-19) - `001F2B70`

`001F2B70` (220 B) is `CopyDepthBufferObj` - `00186660`/`00188730`/`00189120`/`001D5620`/`001D5630`/`001EE8E0`/`005FEFD0`. Interior anchor `001F2B98` (an `00186660` call).

## SWE2-EC7-47 update (2026-09-19) - `006A3980`

`006A3980` (220 B) is a body - `call [rax+0xB8]` vcalls only. Interior anchor `006A3A35` (the first vcall).

## SWE2-EC7-47 update (2026-09-19) - `006A6E00`

`006A6E00` (220 B) is a body - `call [r14+8]` vcalls only. Interior anchor `006A6E8B` (the first vcall).

## SWE2-EC7-47 update (2026-09-19) - `006A3680`

`006A3680` (218 B) is a body - `006301F0`/`0068F0F0`/`006B1600`/`006B19A0`/`0080929C`/`008092FC`. Interior anchor `006A36BB` (a `006301F0` call).

## SWE2-EC7-47 update (2026-09-19) - `001EA050`

`001EA050` (216 B) is a body - `00584730`/`006167C0`/`0063ABF0`. Interior anchor `001EA0A5` (a `00584730` call).

## SWE2-EC7-47 update (2026-09-19) - `0069F490`

`0069F490` (216 B) is a call-free 3x3 matrix-vector transform + record write - `[rdx+0x30]`->`+8`, `[rdx]`->`+0x50`; `movdqa` `+0x10`/`+0x20`->`+0x30`/`+0x40` when `r8b` set, else the `mulss`/`addss` transform into scratch. Interior anchor `0069F4C2` (the transform head).

## SWE2-EC7-47 update (2026-09-19) - `006A14C0`

`006A14C0` (215 B) is a vtable row body - `00683BF0`/`0069E230`/`0080F420`/`00810580`/`00811130`/`00811470`/`00811640` plus a `call [rbx+8]` vcall. Interior anchor `006A14EE` (a `00683BF0` call).

## SWE2-EC7-47 update (2026-09-19) - `006A4470`

`006A4470` (213 B) is a body - `call [rax+0x50]` vcalls x3. Interior anchor `006A44A6` (the first vcall).

## SWE2-EC7-47 update (2026-09-19) - `006CB940`

`006CB940` (212 B) is a body - `0067FE20`/`00680200` plus a `008C2B48` import call. Interior anchor `006CB9E2` (a `0067FE20` call).

## SWE2-EC7-47 update (2026-09-19) - `001F2FB0`

`001F2FB0` (210 B) is a body - `00185DA0`/`00188730`/`00189120`/`005FEFD0`/`00600A60`/`0060D190`/`0060D270`. Interior anchor `001F2FD9` (an `00185DA0` call).

## SWE2-EC7-48 update (2026-09-19) - `00212F70`

`00212F70` (202 B) is `FontBorderOrderedObject` - `0016D6A0`/`00186800`/`00189120`/`005DC190`/`005FEFD0`/`00600A60`/`00609710`. Interior anchor `00212F8D` (an `0016D6A0` call).

## SWE2-EC7-48 update (2026-09-19) - `00225A50`

`00225A50` (207 B) is a body - `0016D6A0`/`00210EB0`/`00221140`/`00221710`/`007A8CA0` plus `call [rax]`/`call [rax+8]` vcalls. Interior anchor `00225A69` (an `0016D6A0` call).

## SWE2-EC7-48 update (2026-09-19) - `006A1770`

`006A1770` (207 B) is a vtable row body - `00683BF0`/`00684080`/`0069E230`/`0080F420`/`00810620`/`00811130`/`00811470` plus a `call [rdi+8]` vcall. Interior anchor `006A1793` (a `00683BF0` call).

## SWE2-EC7-48 update (2026-09-19) - `006A15A0`

`006A15A0` (203 B) is a vtable row body - `00683BF0`/`00684080`/`0069E230`/`0080F420`/`00810620` plus a `call [rdi+8]` vcall. Interior anchor `006A15C1` (a `00683BF0` call).

## SWE2-EC7-48 update (2026-09-19) - `006A3430`

`006A3430` (202 B) is a body - `0068F0F0`/`006B1600`/`006B19A0`/`0080929C`/`008092FC`. Interior anchor `006A346B` (a `0068F0F0` call).

## SWE2-EC7-48 update (2026-09-19) - `006A35B0`

`006A35B0` (202 B) is a body - `006301F0`/`006B1600`/`006B19A0`/`0080929C`/`008092FC`. Interior anchor `006A35EB` (a `006301F0` call).

## SWE2-EC7-49 update (2026-09-19) - `0020D050`

`0020D050` (197 B) is a body - `00159270`/`0020DAB0`/`00808C40`. Interior anchor `0020D079` (an `00159270` call).

## SWE2-EC7-49 update (2026-09-19) - `006A6BD0`

`006A6BD0` (196 B) is a body - `call [rsi+8]` vcall only. Interior anchor `006A6C4B` (the vcall).

## SWE2-EC7-49 update (2026-09-19) - `0079AC20`

`0079AC20` (194 B) is a body - `00683BF0`/`00796BC0` plus a `call [rdi+8]` vcall. Interior anchor `0079AC4A` (a `00683BF0` call).

## SWE2-EC7-49 update (2026-09-19) - `00687E60`

`00687E60` (193 B) is a body - `0069B110` single call. Interior anchor `00687E6C` (the `0069B110` call).

## SWE2-EC7-49 update (2026-09-19) - `00688FA0`

`00688FA0` (193 B) is a body - `0069AFF0` single call. Interior anchor `00688FAC` (the `0069AFF0` call).

## SWE2-EC7-49 update (2026-09-19) - `006A3B50`

`006A3B50` (193 B) is a body - `call [rax+0xD8]`/`call [rax+0x70]` vcalls. Interior anchor `006A3B73` (the first vcall).

## SWE2-EC7-49 update (2026-09-19) - `006A6D40`

`006A6D40` (192 B) is a body - `call [rbp+8]` vcall only. Interior anchor `006A6DC0` (the vcall).

## SWE2-EC7-49 update (2026-09-19) - `0060E810`

`0060E810` (190 B) is a body - `00600B30` plus a `call [rax+0x10]` vcall. Interior anchor `0060E836` (the `00600B30` call).

## SWE2-EC7-50 update (2026-09-19) - `00223DA0`

`00223DA0` (186 B) is a `SebAudioBank` vtable row-8 body - `0016D6A0`/`00212A70`/`00221D10`/`00225570`/`00225580`/`00225590`/`002255A0`/`007A48C0`. Interior anchor `00223DBA` (an `0016D6A0` call).

## SWE2-EC7-50 update (2026-09-19) - `00222F20`

`00222F20` (183 B) is a `SepAudioBank` vtable row-8 body - `0016D6A0`/`00212A70`/`00221D10`/`00225570`/`00225580`/`00225590`/`002255A0`/`007A48C0`. Interior anchor `00222F3A` (an `0016D6A0` call).

## SWE2-EC7-50 update (2026-09-19) - `0068C1A0`

`0068C1A0` (186 B) is a body - `00861EC0` single call. Interior anchor `0068C1BD` (the `00861EC0` call).

## SWE2-EC7-50 update (2026-09-19) - `0068E840`

`0068E840` (186 B) is a body - `00861EC0` single call. Interior anchor `0068E85D` (the `00861EC0` call).

## SWE2-EC7-50 update (2026-09-19) - `006A3370`

`006A3370` (186 B) is a body - `006B1600`/`006B19A0`/`0080929C`/`008092FC`. Interior anchor `006A33A7` (a `006B1600` call).

## SWE2-EC7-50 update (2026-09-19) - `00650800`

`00650800` (185 B) is a vtable row body - `0064FC40`/`00684080`/`0080F420`/`00810620`/`00811130`/`00811470` plus a `call [rdi+8]` vcall. Interior anchor `0065081E` (a `0064FC40` call).

## SWE2-EC7-50 update (2026-09-19) - `007A36B0`

`007A36B0` (184 B) is a body - `005CDAA0` plus a `call [rdi+8]` vcall. Interior anchor `007A36D5` (the `005CDAA0` call).

## SWE2-EC7-50 update (2026-09-19) - `006858C0`

`006858C0` (182 B) is a body - `0062FF50`/`00630180`/`0080929C`/`008092FC`. Interior anchor `006858F7` (a `0062FF50` call).

## SWE2-EC7-50 update (2026-09-19) - `00689DF0`

`00689DF0` (181 B) is a body - `0069A510` single call. Interior anchor `00689DFC` (the `0069A510` call).

## SWE2-EC7-51 update (2026-09-19) - `0068CAF0`

`0068CAF0` (179 B) is a body - `00861EC0` single call. Interior anchor `0068CB0D` (the `00861EC0` call).

## SWE2-EC7-51 update (2026-09-19) - `006BBC70`

`006BBC70` (179 B) is a body - `00584730` single call. Interior anchor `006BBC9C` (the `00584730` call).

## SWE2-EC7-51 update (2026-09-19) - `00872F20`

`00872F20` (179 B) is a vtable row body - `006372A0`/`00684080`/`0080F420`/`00810620`/`00811130`/`00811470`/`00870DD0` plus a `call [rdi+8]` vcall. Interior anchor `00872F3E` (a `006372A0` call).

## SWE2-EC7-51 update (2026-09-19) - `0020D120`

`0020D120` (178 B) is a body - `001590B0`/`0020DAB0`/`00808C40`. Interior anchor `0020D146` (an `001590B0` call).

## SWE2-EC7-51 update (2026-09-19) - `006A32B0`

`006A32B0` (178 B) is a body - `006301F0`/`0068F0F0`/`006B1600`/`0080929C`/`008092FC`. Interior anchor `006A32E7` (a `006301F0` call).

## SWE2-EC7-51 update (2026-09-19) - `00872FE0`

`00872FE0` (176 B) is a vtable row body - `00684080`/`0080F420`/`00810620`/`00811130`/`00811470`/`00870DD0` plus a `call [rdi+8]` vcall. Interior anchor `00872FFE` (a `00684080` call).

## SWE2-EC7-51 update (2026-09-19) - `005C1500`

`005C1500` (175 B) is a vtable row body - `005BC4D0`/`00684080`/`0080F420`/`00810620`/`00811130`/`00811470` plus a `call [rdi+8]` vcall. Interior anchor `005C151E` (a `005BC4D0` call).

## SWE2-EC7-51 update (2026-09-19) - `006506A0`

`006506A0` (175 B) is a vtable row body - `006372A0`/`0064FC40`/`00684080`/`0080F420`/`00810620`/`00811130`/`00811470` plus a `call [rdi+8]` vcall. Interior anchor `006506BE` (a `006372A0` call).

## SWE2-EC7-51 update (2026-09-19) - `0068B030`

`0068B030` (175 B) is a body - `00699A10` single call. Interior anchor `0068B03C` (the `00699A10` call).

## SWE2-EC7-51 update (2026-09-19) - `0068D2C0`

`0068D2C0` (175 B) is a body - `00698F30` single call. Interior anchor `0068D2CC` (the `00698F30` call).

## SWE2-EC7-51 update (2026-09-19) - `0068E790`

`0068E790` (175 B) is a body - `00861EC0` single call. Interior anchor `0068E7AD` (the `00861EC0` call).

## SWE2-EC7-51 update (2026-09-19) - `006A4050`

`006A4050` (175 B) is a call-free packed-normal decoder - `edx` bits 0/1/2 -> `1 - bit` signed components scaled by the `[rcx+0x30]` row, `shufps` per lane. Interior anchor `006A4054` (the row load).

## SWE2-EC7-51 update (2026-09-19) - `006A6B20`

`006A6B20` (175 B) is a body - `call [rsi+8]` vcall only. Interior anchor `006A6B86` (the vcall).

## SWE2-EC7-51 update (2026-09-19) - `00689B70`

`00689B70` (173 B) is a body - `00861EC0` single call. Interior anchor `00689B8D` (the `00861EC0` call).

## SWE2-EC7-51 update (2026-09-19) - `006A66D0`

`006A66D0` (173 B) is a body - `005A6670` plus a `call [r11+8]` vcall. Interior anchor `006A672A` (the `005A6670` call).

## SWE2-EC7-54 update (2026-09-19) - `001EA830`

`001EA830` (347 B) is a vtable-method body - `00185A50`/`001EAC60`/`005FEFD0`/`00600A60`/`0067C260`/`0067C440`/`0067C4F0`. Interior anchor `001EA86B` (a `005FEFD0` call).


## SWE2-EC7-54 update (2026-09-19) - `00615ED0`

`00615ED0` (294 B) is a call-free record defaults initializer - `+0x04=3`, `+0x1C=1`, `+0x2C`/`+0x30=1`, `+0x34=2`, `+0x3C=0xFFFF`, `00D56060`/`00D56070` pairs into `+0x40`/`+0x50`/`+0x68`. Interior anchor `00615F23` (the `0xFFFF` word write).


## SWE2-EC7-54 update (2026-09-19) - `006C8750`

`006C8750` (283 B) is the `+0x18C0` subobject constructor the gi-render page names - `00615ED0` defaults init plus `006DA450`, `00D86960`/`00D86AD0` rdata. Interior anchor `006C8811` (a `00615ED0` call).

## SWE2-EC7-55 update (2026-09-19) - `0067FE20`

`0067FE20` (281 B) is a vtable-method body - `0067F9D0` (the ordered-tree erase) single call. Interior anchor `0067FEB3` (a `0067F9D0` call).

## SWE2-EC7-56 update (2026-09-19) - `0060E5A0`

`0060E5A0` (196 B) is an object-model record body - `005C5230`/`00861EBA`. Interior anchor `0060E5EA` (a `005C5230` call).

## SWE2-EC7-57 update (2026-09-19) - `00638F00`

`00638F00` (176 B) is a vtable row body - `00808B90`/`0080929C`/`008092FC` plus `01F2E780`-`01F2E798`. Interior anchor `00638F5E` (a `008092FC` call).


## SWE2-EC7-57 update (2026-09-19) - `0067C4F0`

`0067C4F0` (174 B) is a vtable-method body - `0067B530`/`0067BF70`/`00861EBA` plus one vcall, `008C2FF8`. Interior anchor `0067C564` (a `0067BF70` call).


## SWE2-EC7-57 update (2026-09-19) - `00650750`

`00650750` (172 B) is a `PMethodCallerConcrete` body - `0064FC40`/`00684080`/`0080F420`/`00810620`/`00811130`/`00811470` plus one vcall, `02CF8470`. Interior anchor `0065076E` (a `00811470` call).


## SWE2-EC7-57 update (2026-09-19) - `00685810`

`00685810` (172 B) is a `PMethodCallerConcrete` body - `0062FF50`/`006372A0`/`0080929C`/`008092FC` plus `02E41370`/`02E41470`/`02E429B0`/`02E429B8`. Interior anchor `00685847` (a `008092FC` call).


## SWE2-EC7-57 update (2026-09-19) - `0079A920`

`0079A920` (172 B) is a `PMethodCallerConcrete` body - `00684080`/`00796960`/`0080F420`/`00810620`/`00811130`/`00811470` plus one vcall, `02EA5380`. Interior anchor `0079A93E` (a `00811470` call).


## SWE2-EC7-57 update (2026-09-19) - `005FF7D0`

`005FF7D0` (171 B) is a `PMethodCallerConcrete` body - `005F8450`/`00683B10`/`00683B50` plus one vcall. Interior anchor `005FF7FE` (a `00683B10` call).


## SWE2-EC7-57 update (2026-09-19) - `0067C260`

`0067C260` (171 B) is a vtable-method body - `005CDAA0`/`0060B980` plus `008C6C98`/`00D6D130`/`02E3F804`. Interior anchor `0067C2A7` (a `005CDAA0` call).


## SWE2-EC7-57 update (2026-09-19) - `0068BFF0`

`0068BFF0` (171 B) is a `PClassDescriptorConcrete` body - `0069AED0` single call. Interior anchor `0068BFFC` (a `0069AED0` call).


## SWE2-EC7-57 update (2026-09-19) - `0068CA40`

`0068CA40` (171 B) is a `PClassDescriptorConcrete` body - `0069AC90` single call. Interior anchor `0068CA4C` (a `0069AC90` call).


## SWE2-EC7-57 update (2026-09-19) - `006A0F30`

`006A0F30` (171 B) is a `PMethodCallerConcrete` body - `00683BF0`/`0069BFC0`/`0080F420`/`00810580`/`00811130`/`00811640` plus one vcall. Interior anchor `006A0F58` (a `00811640` call).


## SWE2-EC7-57 update (2026-09-19) - `006A1410`

`006A1410` (171 B) is a `PMethodCallerConcrete` body - `00683BF0`/`0069E230`/`0080F420`/`00810580`/`00811130`/`00811470` plus one vcall. Interior anchor `006A1439` (a `00811470` call).

## SWE2-EC7-58 update (2026-09-19) - `0067B530`

`0067B530` (1524 B) is a vtable-method body - `0059A600`/`005CDAA0`/`00674610`/`0067B4C0`/`0067BE10`/`0067CBD0`/`00808C40` plus `00D6D090`/`01F44830`. Interior anchor `0067B5F1` (a `0067BE10` call).


## SWE2-EC7-58 update (2026-09-19) - `0067BF70`

`0067BF70` (752 B) is a vtable-method body - `0017D260`/`00584730`/`00671690`/`00671B10`/`00671B20`/`00674230`/`00674420` plus one vcall, `02D3AB18`/`02D3AB48`. Interior anchor `0067BFCD` (a `0017D260` call).


## SWE2-EC7-58 update (2026-09-19) - `0063A1D0`

`0063A1D0` (170 B) is a `PMethodCallerConcrete` body - `005BE870`/`006366C0`/`00684080`/`0080F420`/`00810620` plus one vcall. Interior anchor `0063A1E8` (a `006366C0` call).


## SWE2-EC7-58 update (2026-09-19) - `006C02F0`

`006C02F0` (170 B) is a `PMethodCallerConcrete` body - `006301F0`/`0080929C`/`008092FC` plus `02E58DB0`/`02E59720`-`02E59730`. Interior anchor `006C0327` (a `008092FC` call).


## SWE2-EC7-58 update (2026-09-19) - `0079CD70`

`0079CD70` (170 B) is a `PMethodCallerConcrete` body - `006B19A0`/`0080929C`/`008092FC` plus `02EA9400`/`02EACE20`-`02EACE30`. Interior anchor `0079CDA7` (a `008092FC` call).


## SWE2-EC7-58 update (2026-09-19) - `0067C440`

`0067C440` (169 B) is a vtable-method body - `0018D240`/`00861EBA` plus `00D6D080`/`01CEBBA8` and the `"textColor"` literal. Interior anchor `0067C486` (a `0018D240` call).


## SWE2-EC7-58 update (2026-09-19) - `006AF0C0`

`006AF0C0` (168 B) is a `PMethodCallerConcrete` body - `00684080`/`006AEE00`/`0080F420`/`00810620`/`00811130`/`00811470` plus one vcall. Interior anchor `006AF0DE` (a `00811470` call).


## SWE2-EC7-58 update (2026-09-19) - `006AC440`

`006AC440` (167 B) is a `PMethodCallerConcrete` body - `006372A0`/`00682980`/`00684080`/`0080F420`/`00810620`/`00811130` plus one vcall, `02E4EAF0`. Interior anchor `006AC45B` (a `00682980` call).


## SWE2-EC7-58 update (2026-09-19) - `006A2B20`

`006A2B20` (166 B) is a `PMethodCallerConcrete` body - `006301F0`/`006B1600`/`0080929C`/`008092FC` plus `02E47CD0`/`02E4D4E8`-`02E4D4F8`. Interior anchor `006A2B57` (a `008092FC` call).


## SWE2-EC7-58 update (2026-09-19) - `006A3200`

`006A3200` (166 B) is a `PMethodCallerConcrete` body - `0068F0F0`/`006B1600`/`0080929C`/`008092FC` plus `02E494D0`/`02E4D308`-`02E4D318`. Interior anchor `006A3237` (a `008092FC` call).


## SWE2-EC7-58 update (2026-09-19) - `006A3500`

`006A3500` (166 B) is a `PMethodCallerConcrete` body - `00630180`/`006B19A0`/`0080929C`/`008092FC` plus `02E494D0`/`02E4D2D8`-`02E4D2E8`. Interior anchor `006A3537` (a `008092FC` call).


## SWE2-EC7-58 update (2026-09-19) - `006AC570`

`006AC570` (166 B) is a `PMethodCallerConcrete` body - `006366C0`/`00684080`/`006AC1D0`/`0080F420`/`00810620` plus one vcall. Interior anchor `006AC588` (a `006366C0` call).


## SWE2-EC7-58 update (2026-09-19) - `006AF1D0`

`006AF1D0` (166 B) is a `PMethodCallerConcrete` body - `00684080`/`006AEE00`/`006AEF30`/`0080F420`/`00810620` plus one vcall. Interior anchor `006AF1E8` (a `006AEF30` call).


## SWE2-EC7-58 update (2026-09-19) - `005C16C0`

`005C16C0` (165 B) is a `PMethodCallerConcrete` body - `005BC4D0`/`0080F420`/`00810580`/`00811130`/`00811470`/`00811640` plus one vcall. Interior anchor `005C16E3` (a `00811640` call).


## SWE2-EC7-58 update (2026-09-19) - `00687C50`

`00687C50` (165 B) is a `PMethodCallerConcrete` body - `0069A0B0` single call. Interior anchor `00687C5C` (a `0069A0B0` call).

## SWE2-EC7-59 update (2026-09-19) - `0059A600`

`0059A600` (232 B) is a call-free lead-byte decoder - `al` range compares (`0xE0`/`0xF0`/`0xF8`/`0xFC`) select a continuation count, `(1<<(6-count))-1` masks the payload. Interior anchor `0059A649` (the `shl` continuation mask).


## SWE2-EC7-59 update (2026-09-19) - `0067BE10`

`0067BE10` (171 B) is a vtable-method body - `005CCB80`/`0066F970`/`00671B10`/`00671B30`. Interior anchor `0067BE20` (a `00671B10` call).


## SWE2-EC7-59 update (2026-09-19) - `00223490`

`00223490` (164 B) is the `SepAudioBank` row body - `0016D6A0`/`00225680`/`007A7010`/`007A84A0` plus `008C5F6C`. Interior anchor `002234CD` (a `00225680` call).


## SWE2-EC7-59 update (2026-09-19) - `0068AD40`

`0068AD40` (163 B) is a `PClassDescriptorConcrete` body - `0069ADB0` single call. Interior anchor `0068AD4C` (a `0069ADB0` call).


## SWE2-EC7-59 update (2026-09-19) - `0068C8D0`

`0068C8D0` (162 B) is a `PClassDescriptorConcrete` body - `00861EC0` single call plus `00D79858`. Interior anchor `0068C8ED` (a `00861EC0` call).


## SWE2-EC7-59 update (2026-09-19) - `0020CEF0`

`0020CEF0` (159 B) is an indirect-only `AmdAdapterInfo` predicate - `0xC`-stride `cmp [rax],r9d` scan counted by `[rcx+0x2C]`, bool return. Interior anchor `0020CF20` (the `cmp [rax],r9d` scan).

## SWE2-EC7-60 update (2026-09-19) - `00687DC0`

`00687DC0` (159 B) is a call-free record defaults + vtable stamp `00D76218` (RTTI `01D27890`), `+0x80`=3.0f, `+0x60`=6. Interior anchor `00687E25` (the `00D76218` vtable `lea`).


## SWE2-EC7-60 update (2026-09-19) - `00688ED0`

`00688ED0` (159 B) is a call-free record defaults sibling - vtable `00D709F8` (RTTI `01D27BB0`), `+0x80`=3.0f, `+0x7C`=2.0f. Interior anchor `00688F35` (the `00D709F8` vtable `lea`).


## SWE2-EC7-60 update (2026-09-19) - `006A6CA0`

`006A6CA0` (159 B) is an indirect-only stream-read - `qword[r10]` cursor +=8 x3 (r8d/r9/rax popped) then `call [rsi+8]`. Interior anchor `006A6CF6` (the `call [rsi+8]` vcall).


## SWE2-EC7-60 update (2026-09-19) - `00225BA0`

`00225BA0` (158 B) is the `MusicStreamingReader` row body - `0059EE90`/`0059FBA0` plus one vcall, `01CEBB70`. Interior anchor `00225BF5` (a `0059EE90` call).


## SWE2-EC7-60 update (2026-09-19) - `0063A3A0`

`0063A3A0` (158 B) is a `PMethodCallerConcrete` body - `00637040`/`00683B50`/`00684080`/`0080F420`/`00810620` plus one vcall, `02CF8470`. Interior anchor `0063A3B8` (a `00683B50` call).


## SWE2-EC7-60 update (2026-09-19) - `006B53C0`

`006B53C0` (158 B) is a `PMethodCallerConcrete` body - `00683B50`/`00684080`/`006B5170`/`0080F420`/`00810620` plus one vcall, `02E518D0`. Interior anchor `006B53D8` (a `00683B50` call).


## SWE2-EC7-60 update (2026-09-19) - `002259B0`

`002259B0` (157 B) is the `MemoryStreamingReader` row body - `0016D6A0`/`00210EB0`/`002211B0`/`00221220`/`00221710`/`007A8CA0`. Interior anchor `002259C9` (a `007A8CA0` call).


## SWE2-EC7-60 update (2026-09-19) - `005CBFB0`

`005CBFB0` (157 B) is a `PMethodCallerConcrete` body - `005A6670` single call plus one vcall. Interior anchor `005CC005` (a `005A6670` call).


## SWE2-EC7-60 update (2026-09-19) - `00688C80`

`00688C80` (157 B) is a `PClassDataMemberPhyreArray` body - `0069AB70` single call. Interior anchor `00688C8C` (a `0069AB70` call).


## SWE2-EC7-60 update (2026-09-19) - `00689C20`

`00689C20` (157 B) is a `PClassDescriptorConcrete` body - `0069AA50` single call. Interior anchor `00689C2C` (a `0069AA50` call).


## SWE2-EC7-60 update (2026-09-19) - `0068AF90`

`0068AF90` (156 B) is a call-free record defaults sibling - `+0x70`/`+0x74`=1.0f, `00D79A88`. Interior anchor `0068AFB1` (the `+0x24` = 1.0f store).


## SWE2-EC7-60 update (2026-09-19) - `0068DCE0`

`0068DCE0` (156 B) is a call-free record defaults sibling - `+0x78`=2.0f, `00D79A10`. Interior anchor `0068DD4C` (the `+0x78` = 2.0f store).


## SWE2-EC7-60 update (2026-09-19) - `006A9620`

`006A9620` (156 B) is a `PClassDescriptorForType` body - `006A99E0` single call. Interior anchor `006A962C` (a `006A99E0` call).

## SWE2-EC7-61 update (2026-09-19) - `00684B70`

`00684B70` (154 B) is a `PMethodCallerConcrete` body - `00683040`/`00683350`/`006836B0`/`00683B50`/`0080F420`/`00810580` plus one vcall. Interior anchor `00684B93` (a `00683B50` call).


## SWE2-EC7-61 update (2026-09-19) - `006A6A80`

`006A6A80` (154 B) is a `PClassDescriptorAbstract` body - `00630110` single call plus one vcall. Interior anchor `006A6ADF` (a `00630110` call).


## SWE2-EC7-61 update (2026-09-19) - `001C2070`

`001C2070` (153 B) is a vtable-method body - `001EA180` single call plus one vcall. Interior anchor `001C20A7` (a `001EA180` call).


## SWE2-EC7-61 update (2026-09-19) - `006ACC20`

`006ACC20` (153 B) is a `PClassDescriptorForType` body - `005CDAA0`/`006372A0` plus one vcall, `00D4E750`/`02E4EAF0`. Interior anchor `006ACC44` (a `005CDAA0` call).


## SWE2-EC7-61 update (2026-09-19) - `00864E90`

`00864E90` (153 B) is the `GiBeginEff` row body - `0016D6A0`/`00210520`/`002105A0` plus four vcalls, `008F311C`. Interior anchor `00864EA8` (a `0016D6A0` call).


## SWE2-EC7-61 update (2026-09-19) - `005C3EE0`

`005C3EE0` (152 B) is a `PMethodCallerConcrete` body - `00630180`/`0080929C`/`008092FC` plus `02CAD140`/`02CAD840`/`02CB5AB8`/`02CB5AC0`. Interior anchor `005C3F17` (a `008092FC` call).


## SWE2-EC7-61 update (2026-09-19) - `00670BC0`

`00670BC0` (152 B) is a `PClassDescriptorForType` body - `00630180`/`0080929C`/`008092FC` plus `02CB6B80`/`02D3A440`/`02D3E0C0`/`02D3E0C8`. Interior anchor `00670BF7` (a `008092FC` call).

## SWE2-EC7-62 update (2026-09-19) - `005C1460`

`005C1460` (150 B) is a `PMethodCallerConcrete` body - `005BC4D0`/`0080F420`/`00810640`/`00811130`/`00811470` plus one vcall. Interior anchor `005C147E` (a `00811470` call).


## SWE2-EC7-62 update (2026-09-19) - `005C3F80`

`005C3F80` (150 B) is a `PMethodCallerConcrete` body - `0062FF50`/`00630180`/`0080929C`/`008092FC` plus `02CAD140`/`02CB5A90`/`02CB5A98`/`02CB5AA0`. Interior anchor `005C3FB7` (a `008092FC` call).


## SWE2-EC7-62 update (2026-09-19) - `00603F40`

`00603F40` (150 B) is a `PMethodCallerConcrete` body - `00630180`/`006B09E0`/`0080929C`/`008092FC` plus `02CB6E80`/`02CED0C0`/`02CED0C8`/`02CED0D0`. Interior anchor `00603F77` (a `008092FC` call).


## SWE2-EC7-62 update (2026-09-19) - `006860E0`

`006860E0` (150 B) is a `PMethodCallerConcrete` body - `005A6670` single call plus one vcall. Interior anchor `0068613B` (a `005A6670` call).


## SWE2-EC7-62 update (2026-09-19) - `00689D50`

`00689D50` (149 B) is a call-free record defaults + vtable stamp `00D79A60` (RTTI `01D2D728`), `+0x80`=3.0f (`00687DC0` sibling). Interior anchor `00689DB5` (the `00D79A60` vtable `lea`).


## SWE2-EC7-62 update (2026-09-19) - `0068C100`

`0068C100` (149 B) is a call-free record defaults + vtable stamp `00D79998` (RTTI `01D2D380`), 1.0f lattice. Interior anchor `0068C10D` (the `00D79998` vtable `lea`).


## SWE2-EC7-62 update (2026-09-19) - `0068D220`

`0068D220` (149 B) is a call-free record defaults + vtable stamp `00D799E8` (RTTI `01D2D4E0`), `+0x78`=2.0f. Interior anchor `0068D2A1` (the `00D799E8` vtable `lea`).


## SWE2-EC7-62 update (2026-09-19) - `00874200`

`00874200` (147 B) is a `PClassDescriptorConcrete` body - `006372A0` single call plus one vcall. Interior anchor `00874246` (a `006372A0` call).


## SWE2-EC7-62 update (2026-09-19) - `005C1770`

`005C1770` (146 B) is a `PMethodCallerConcrete` body - `005BC4D0`/`005BCD20`/`0080F420`/`00810580`/`00811130`/`00811470` plus one vcall. Interior anchor `005C178D` (a `005BCD20` call).



## SWE2-EC7-63 update (2026-09-19) - `005C1810`

`005C1810` (146 B) is a `PMethodCallerConcrete` body - `005BC4D0`/`00683B50`/`0080F420`/`00810580`/`00811130`/`00811470` plus one vcall. Interior anchor `005C182D` (a `00683B50` call).



## SWE2-EC7-63 update (2026-09-19) - `005C3E40`

`005C3E40` (146 B) is a `PMethodCallerConcrete` body - `00630180`/`006301F0`/`0080929C`/`008092FC` plus `02CAD140`/`02CB5B00`-`02CB5B10`. Interior anchor `005C3E77` (a `008092FC` call).



## SWE2-EC7-63 update (2026-09-19) - `00683B50`

`00683B50` (146 B) is a vtable row body - `00682980`/`00811130`/`00811530` plus `02E4D630`. Interior anchor `00683B60` (a `00682980` call).



## SWE2-EC7-63 update (2026-09-19) - `006C0250`

`006C0250` (146 B) is a `PModifierNetworkDynamicMeshInstance` row body - `006301F0`/`0080929C`/`008092FC` plus `02E58DB0`/`02E596D8`-`02E596E8`. Interior anchor `006C0287` (a `008092FC` call).



## SWE2-EC7-63 update (2026-09-19) - `001B7170`

`001B7170` (145 B) is a vtable row callee - `001B6EF0`/`00584730`/`00663170`. Interior anchor `001B71A9` (a `00663170` call).



## SWE2-EC7-63 update (2026-09-19) - `00633900`

`00633900` (145 B) is a `PClassDataMemberArrayDynamic` body - `0016D6A0`/`00584730`/`006B6700` plus `00D580B0` and one vcall. Interior anchor `00633943` (a `006B6700` call).



## SWE2-EC7-63 update (2026-09-19) - `006339E0`

`006339E0` (145 B) is a `PClassDataMemberPhyreSharray` body - `0016D6A0`/`00584730`/`006B6700` plus `00D580B0` and one vcall. Interior anchor `00633A23` (a `006B6700` call).



## SWE2-EC7-63 update (2026-09-19) - `0068DC40`

`0068DC40` (145 B) is a call-free record defaults + `00D798A8` - 1.0f lattice sibling. Interior anchor `0068DC61` (the `+0x24` = 1.0f store).



## SWE2-EC7-63 update (2026-09-19) - `0019DF00`

`0019DF00` (144 B) is the `AssetListManager` row body - `0019DAD0`/`0019DBA0`/`0019DCC0`/`005CD6D0`/`00809950` plus `008F4430`. Interior anchor `0019DF2F` (a `0019DAD0` call).



## SWE2-EC7-63 update (2026-09-19) - `005CBDA0`

`005CBDA0` (144 B) is a `PMethodCallerConcrete` body - `006301F0` single call plus one vcall. Interior anchor `005CBDE6` (a `006301F0` call).



## SWE2-EC7-63 update (2026-09-19) - `0063E4F0`

`0063E4F0` (144 B) is a `PMethodCallerConcrete` body - `006379A0` single call plus one vcall. Interior anchor `0063E537` (a `006379A0` call).



## SWE2-EC7-63 update (2026-09-19) - `006748E0`

`006748E0` (144 B) is a `PClassDataMemberPhyreArray` body - `005A6670` single call plus one vcall. Interior anchor `00674928` (a `005A6670` call).



## SWE2-EC7-63 update (2026-09-19) - `005CC270`

`005CC270` (143 B) is a `PMethodCallerConcrete` body - `00630490` single call plus one vcall. Interior anchor `005CC2B6` (a `00630490` call).



## SWE2-EC7-63 update (2026-09-19) - `00688DE0`

`00688DE0` (143 B) is a call-free record defaults + `00D79920` - 1.0f lattice sibling. Interior anchor `00688E01` (the `+0x24` = 1.0f store).



## SWE2-EC7-63 update (2026-09-19) - `001B9AF0`

`001B9AF0` (142 B) is the `ChrModel` row body - `001B9750`/`001BA910`/`00809950` plus `008F9150`. Interior anchor `001B9B47` (a `001BA910` call).



## SWE2-EC7-64 update (2026-09-19) - `00609A30`

`00609A30` (142 B) is a `rdx`-forward body - `00600B30` single call plus one vcall. Interior anchor `00609A3F` (a `00600B30` call).



## SWE2-EC7-64 update (2026-09-19) - `0066FD00`

`0066FD00` (142 B) is a `PClassDescriptorAbstract` body - `005F8450`/`0066E7D0`/`0080F420`/`00810580`/`00811130`/`00811470` plus one vcall. Interior anchor `0066FD1D` (a `005F8450` call).



## SWE2-EC7-64 update (2026-09-19) - `0068AEB0`

`0068AEB0` (142 B) is a call-free record defaults + `00D79970` - 1.0f lattice (`+0x24`-`+0x58` fields). Interior anchor `0068AECE` (the `+0x24` = 1.0f store).



## SWE2-EC7-64 update (2026-09-19) - `006A69F0`

`006A69F0` (142 B) is a `PClassDescriptorConcrete<PSceneRenderPass>` body - `00630110` single call plus one vcall. Interior anchor `006A6A43` (a `00630110` call).



## SWE2-EC7-64 update (2026-09-19) - `005CBF20`

`005CBF20` (141 B) is a `PMethodCallerConcrete` body - `005A6670` single call plus one vcall. Interior anchor `005CBF65` (a `005A6670` call).



## SWE2-EC7-64 update (2026-09-19) - `0063E230`

`0063E230` (141 B) is a call-free `PTypeDefault<unsigned __int64>` byte-reversal - `movabs 0xFF00000000`/`shr 0x10`/`and`/`or` bit gather (`0063E0D0` sibling). Interior anchor `0063E264` (the `0xFF00000000` mask load).



## SWE2-EC7-64 update (2026-09-19) - `006B3B10`

`006B3B10` (140 B) is a `PClassDescriptorConcrete<PShaderParameterCapture>` body - `006B33F0` single call plus one vcall. Interior anchor `006B3B4F` (a `006B33F0` call).



## SWE2-EC7-64 update (2026-09-19) - `005C1B20`

`005C1B20` (139 B) is a `PMethodCallerConcrete` body - `005BC4D0`/`0080F420`/`00810450`/`00811130`/`00811470` plus one vcall. Interior anchor `005C1B3E` (a `00811470` call).



## SWE2-EC7-64 update (2026-09-19) - `00610C10`

`00610C10` (139 B) is a `PMethodCallerConcrete` body - `006B09E0` single call plus one vcall. Interior anchor `00610C4E` (a `006B09E0` call).



## SWE2-EC7-64 update (2026-09-19) - `0065E3A0`

`0065E3A0` (139 B) is a `PStreamReaderFile` caller body - `006372A0` single call plus one vcall. Interior anchor `0065E3DE` (a `006372A0` call).



## SWE2-EC7-64 update (2026-09-19) - `00681880`

`00681880` (139 B) is the `PScripting::PScheduler` row body - `00584730`/`00681720`/`00682D90`/`00685DB0` plus `00D6FD68`. Interior anchor `006818A1` (a `00685DB0` call).



## SWE2-EC7-64 update (2026-09-19) - `006CADE0`

`006CADE0` (139 B) is an indirect-only `PrimitiveRendererD3D11` invocation stub - 12-slot stack-arg marshal, one vcall. Interior anchor `006CAE17` (the `[rcx]` vtable load).



## SWE2-EC7-64 update (2026-09-19) - `001B6EF0`

`001B6EF0` (138 B) is a vtable row callee - `00584730`/`00662F80`. Interior anchor `001B6F37` (a `00662F80` call).



## SWE2-EC7-65 update (2026-09-19) - `00682D90`

`00682D90` (156 B) is a `PScripting::PScheduler` callee - `00584730` single call. Interior anchor `00682DD9` (a `00584730` call).



## SWE2-EC7-65 update (2026-09-19) - `005C1630`

`005C1630` (138 B) is a `PMethodCallerConcrete` body - `005BC4D0`/`0080F420`/`00810580`/`00811130`/`00811470`. Interior anchor `005C164E` (a `00811470` call).



## SWE2-EC7-65 update (2026-09-19) - `0068BA80`

`0068BA80` (138 B) is a `PFunctionCallerConcrete` body - `0069B330` single call. Interior anchor `0068BA8C` (a `0069B330` call).



## SWE2-EC7-65 update (2026-09-19) - `00610DD0`

`00610DD0` (137 B) is a `PMethodCallerConcrete` body - `005A6670` single call plus one vcall. Interior anchor `00610E11` (a `005A6670` call).



## SWE2-EC7-65 update (2026-09-19) - `005FFD50`

`005FFD50` (136 B) is a `PMethodCallerConcrete` body - `005F94F0`/`0080F420`/`00810580`/`00811130`/`008113D0`. Interior anchor `005FFD6B` (a `008113D0` call).



## SWE2-EC7-65 update (2026-09-19) - `00610D40`

`00610D40` (136 B) is a `PMethodCallerConcrete` body - `005A6670` single call plus one vcall. Interior anchor `00610D80` (a `005A6670` call).



## SWE2-EC7-65 update (2026-09-19) - `00662F80`

`00662F80` (136 B) is a vtable row callee - `00584730`/`00673780`/`00674230`. Interior anchor `00662F97` (a `00673780` call).



## SWE2-EC7-65 update (2026-09-19) - `00677740`

`00677740` (136 B) is a `PClassDescriptorAbstract` body - `00676810`/`00684080`/`0080F420`/`00810620`. Interior anchor `00677753` (a `00676810` call).



## SWE2-EC7-65 update (2026-09-19) - `006A93C0`

`006A93C0` (136 B) is a `PClassDescriptorConcrete<PShader>` body - `00630490` single call plus one vcall. Interior anchor `006A93FF` (a `00630490` call).



## SWE2-EC7-65 update (2026-09-19) - `006B3930`

`006B3930` (136 B) is a `PClassDescriptorConcrete<PTextureCommonBase>` body - `006B1600`/`006B33F0`/`0080929C`/`008092FC` plus `02E51748`-`02E51760`. Interior anchor `006B3967` (a `008092FC` call).



## SWE2-EC7-65 update (2026-09-19) - `005FFC30`

`005FFC30` (135 B) is a `PMethodCallerConcrete` body - `005F94F0`/`0080F420`/`00810580`/`00811130`/`00811640`. Interior anchor `005FFC4E` (a `00811640` call).



## SWE2-EC7-65 update (2026-09-19) - `0063E600`

`0063E600` (135 B) is a `PMethodCallerConcrete` body - `005A6670` single call plus one vcall. Interior anchor `0063E63F` (a `005A6670` call).



## SWE2-EC7-65 update (2026-09-19) - `007A33C0`

`007A33C0` (135 B) is a `PMethodCallerConcrete` body - `006301F0` single call plus one vcall. Interior anchor `007A33FD` (a `006301F0` call).



## SWE2-EC7-66 update (2026-09-19) - `005A9CF0`

`005A9CF0` (134 B) is a `PAnimationAdditiveBlenderController` row body - `00584730` single call plus `00D312F0`/`00D315B0`/`00D31690`. Interior anchor `005A9D26` (a `00584730` call).



## SWE2-EC7-66 update (2026-09-19) - `005C1FD0`

`005C1FD0` (134 B) is a `PMethodCallerConcrete` body - `005BCD20`/`0080F420`/`00810580`/`00811130`/`00811470`. Interior anchor `005C1FEE` (a `00811470` call).



## SWE2-EC7-66 update (2026-09-19) - `00610A50`

`00610A50` (134 B) is a `PMethodCallerConcrete` body - `005CDAA0` single call plus `00D4E750`. Interior anchor `00610A89` (a `005CDAA0` call).



## SWE2-EC7-66 update (2026-09-19) - `00633300`

`00633300` (134 B) is a `PClassDataMemberDynamic` body - `00584730`/`006B6700` plus `00D580B0`/`00D58358`. Interior anchor `0063333A` (a `00584730` call).



## SWE2-EC7-66 update (2026-09-19) - `0063E750`

`0063E750` (134 B) is a `PMethodCallerConcrete` body - `00637650` single call plus one vcall. Interior anchor `0063E78E` (a `00637650` call).



## SWE2-EC7-66 update (2026-09-19) - `00674970`

`00674970` (134 B) is a `PClassDataMemberPhyreArray` body - `00630110` single call plus one vcall. Interior anchor `006749AE` (a `00630110` call).



## SWE2-EC7-66 update (2026-09-19) - `0068D190`

`0068D190` (134 B) is a call-free record defaults + `00D79880` - 1.0f lattice sibling. Interior anchor `0068D1AD` (the `+0x24` = 1.0f store).



## SWE2-EC7-66 update (2026-09-19) - `006BFE40`

`006BFE40` (134 B) is a `PClassDescriptorForType` body - `006BFB10`/`00811130`/`00811640`. Interior anchor `006BFE63` (a `00811640` call).



## SWE2-EC7-66 update (2026-09-19) - `006A70A0`

`006A70A0` (133 B) is a `PClassDescriptorWithoutDefaultConstructor` body - `001EAD40`/`006A74B0`/`008100C0`/`00811130`/`00811530`. Interior anchor `006A70B6` (a `008100C0` call).



## SWE2-EC7-66 update (2026-09-19) - `005A15A0`

`005A15A0` (132 B) is a `PClassDescriptorConcrete<PBlendableAnimationSource>` body - `005BACB0` single call. Interior anchor `005A15AC` (a `005BACB0` call).



## SWE2-EC7-66 update (2026-09-19) - `00684AE0`

`00684AE0` (132 B) is a `PMethodCallerConcrete` body - `00682D20`/`00683450`/`0080F420`/`00810620`. Interior anchor `00684AF3` (a `00683450` call).



## SWE2-EC7-66 update (2026-09-19) - `006A43E0`

`006A43E0` (132 B) is a call-free `btBoxShape` interval test - `comiss` bounds pair, `0x80000000` sign flip, `addss`/`subss` range. Interior anchor `006A4404` (the `0x80000000` sign flip).



## SWE2-EC7-66 update (2026-09-19) - `00219610`

`00219610` (131 B) is the `SepAudioController` row body - `00212760`/`002194A0`/`00219530`/`005CD6D0`/`00809950` plus `00907BA8`. Interior anchor `0021963F` (a `005CD6D0` call).



## SWE2-EC7-66 update (2026-09-19) - `0021AC00`

`0021AC00` (131 B) is the `SebAudioController` row body - `00212760`/`0021AA90`/`0021AB20`/`005CD6D0`/`00809950` plus `00907DE0`. Interior anchor `0021AC2F` (a `005CD6D0` call).



## SWE2-EC7-66 update (2026-09-19) - `0063B890`

`0063B890` (131 B) is a `PMethodCallerConcrete` body - `00637800`/`0080929C`/`008092FC` plus `02CF8980`/`02CF9810`-`02CF9820`. Interior anchor `0063B8CA` (a `008092FC` call).



## SWE2-EC7-66 update (2026-09-19) - `0063B920`

`0063B920` (131 B) is a `PMethodCallerConcrete` body - `00637800`/`0080929C`/`008092FC` plus `02CF8A80`/`02CF97F0`-`02CF9800`. Interior anchor `0063B95A` (a `008092FC` call).


## SWE2-EC7-67 update - `0063E1A0`

`0063E1A0` (129 B) is a call-free bswap64 of `[rdx]` - `0xff000000`/`0xff00`/`0xff0000`/`0xff00000000` masks, `sar 0x28`/`0x38` gather, returns 1 (`0063E0D0`/`0063E230` sibling). Interior anchor `0063E1C0` (the `shl 0x10` byte gather).

## SWE2-EC7-67 update - `0068BF10`

`0068BF10` (128 B) is a call-free record defaults + `00D79830` vtable stamp (RTTI `01D2CBB0`) - 1.0f lattice `+0x24`/`+0x38`/`+0x4C`-`+0x58`/`+0x70`, `+0x60`=4, null-guard returns 1. Interior anchor `0068BF2D` (the `+0x24` = 1.0f store).

## SWE2-EC7-67 update - `006A47F0`

`006A47F0` (128 B) is an indirect-only pair dispatch - for each of `rdx`/`r8`, `[obj+0x104]==4` vcalls `[vtable+0x38]` with the other object. Interior anchor `006A483F` (the `call [rax+0x38]` dispatch).

## SWE2-EC7-67 update - `006A6640`

`006A6640` (129 B) is a vtable-row body - `006B1600` plus one vcall. Interior anchor `006A6674` (an indirect call).

## SWE2-EC7-67 update - `006B6170`

`006B6170` (129 B) is a vtable-row body - `006B09E0` plus one vcall. Interior anchor `006B61A4` (an indirect call).

## SWE2-EC7-67 update - `0079A830`

`0079A830` (128 B) is a vtable-row body - `00683B50`/`00796960`/`0080F420`/`00810640`. Interior anchor `0079A848` (a `00683B50` call).

## SWE2-EC7-67 update - `00864D70`

`00864D70` (130 B) is a vtable-row body - `0016D6A0`/`00210560` x2 plus one vcall pair. Interior anchor `00864D88` (a `0016D6A0` call).

## SWE2-EC7-68 update (2026-09-19) - `001867B0` / `00680200` / `00671B10` shared object helpers

`001867B0` (15 B) is the indexed sub-object fetch the `001F2xxx`
vtable-row family runs (`CopyFrontBufferForVFXObj` slot-1,
`Ps2DofObj::Execute`, and eight more rows): `eax` takes
`dword[rcx+0xC30]` and the return is `qword[rcx + rax*8 + 0xB08]` -
a selector word at `+0xC30` picking one pointer out of the
eight-wide `+0xB08` table. Call-free. Interior anchor `001867B6`
(the `rax*8 + 0xB08` load).

`00680200` (10 B) is the intrusive-list push the Phyre record
builders share (the `0059F7A0` "PMapPair" init calls it inside its
`006803D0`/`00680150`/`00680030`/`0067FFB0` register run):
`[rdx] = [rcx]` links the new node to the current head, then
`[rcx] = rdx` installs it - a two-write head insertion. Call-free.
Interior anchor `00680203` (the `[rdx]` link store).

`00671B10` (7 B) is the `+0x74` bit-0 flag reader the render-block
init `001B72B0` and the `+0x280` run builder `00649C20` call four
times each against the sibling sub-objects - `dword[rcx+0x74] & 1`,
nothing else. Call-free. Interior anchor `00671B13` (the `& 1`).

## SWE2-EC7-72 update (2026-09-19) - `0067FFB0` + `00673780` descriptor helpers measured

`0067FFB0` (46 B) is the aligned-size descriptor init the vtable bodies
share: `+8` = stack arg, `+0x10`/`+0` zeroed, `+0x18` = `(rdx + 7) & ~7`,
`+0x1C` = `r8d`, `+0x20` = `(r9 + 7) & ~7`, returns `rcx` - a call-free
record initializer.
Interior anchor `0067FFC6` (the `+0x18` aligned-size store).

`00673780` (98 B) is the drain loop: for `ebx` over
`[+0x20] & 0x7FFFFFFF` entries, `00670D80(rcx, ebx)` resolves the element
and while `*element > 0` it runs `005CCB80(1)` (the count release) and
re-reads - a bounded per-element drain before the object goes down.
Interior anchor `006737A5` (the `00670D80` element resolve).

## SWE2-EC7-75 update (2026-09-19) - `002D7FA0` `0209E6B0` indexed accessor measured

`002D7FA0` (23 B) is the `0209E6B0` indexed record pointer: sign-extends
`cx`, `x48` stride (`(idx + idx*2) << 4`), returns the element address -
the accessor the vtable stubs share.
Interior anchor `002D7FAB` (the `x3` scale).

## SWE2-EC7-77 update (2026-09-20) - `001EAD40` + `001B8100` storage helpers measured

`001EAD40` (104 B) is the swap-and-release helper: `rsi =
001C26B0(rdx)`; when the caller slot (`rbx`) exists but `rsi` is NULL
it returns `rsi+0xD` (degenerate). Otherwise the old `[rdi]` - if
non-NULL with bit 0 of its first byte CLEAR - is freed via
`00584730`, then `[rdi] = rsi` commits and 0 returns.
Interior anchor `001EAD58` (the `001C26B0` call).

`001B8100` (163 B) is the counted-buffer destroy+replace: with
`[rcx]` bit31 clear and `[rcx+8] != rdx`, the `([rcx] & 0x7FFFFFFF)`
elements at `[rcx+8]` (stride `0x88`) each get `00662F80`, then
`00584730` frees the block; `[rbx+8] = rbp` and `[rbx] = r14d`
commit the replacement. Any other shape just stores the two fields.
Interior anchor `001B8153` (the `00662F80` element call).

## SWE2-EC7-78 update (2026-09-20) - `006CCDA0` + `006CCD80` + `006803D0` storage helpers measured

`006CCDA0` (9 B) is the two-field setter: `[rcx+0x10] = rdx`,
`[rcx+0x18] = r8d`.
Interior anchor `006CCDA4` (the `+0x18` store).

`006CCD80` (20 B) is the small ctor: `[rcx] = rdx`, `+8`/`+0x10`/
`+0x18` zeroed, returns `rcx`.
Interior anchor `006CCD85` (the `+8` zero).

`006803D0` (65 B) is the free-list drain: while `[rbx+0x10]` is
non-NULL it pops the head through `[[rbx+0x10]]` and `00584730`s the
node; `[rbx]` is then zeroed - the pool teardown behind the vtable
callers.
Interior anchor `006803EB` (the `00584730` free call).

## SWE2-EC7-79 update (2026-09-20) - `006737F0` + `00663170` + `0063D8B0` + `00615C90` + `005DC400` measured

`006737F0` (98 B) is the per-element spin-drain: `ebx` walks
`[rdi+0x18] & 0x7FFFFFFF` slots; per slot `00670DC0(rdi, ebx)`
fetches the counter record, and while `dword[rax] > 0` it runs
`005CCB80(1)` and re-fetches - a one-tick yield until the counter
drains.
Interior anchor `00673825` (the `005CCB80` yield call).

`00663170` (92 B) is the matching teardown: `006737F0(rbx)` drains,
`byte[+0x6C] & 1` adds `00674420(rbx)`, then `[rbx+0x18]` bit31
clear with count `> 1` and a live `[rbx+0x20]` frees the buffer via
`00584730`; `+0x20`/`+0x18` are zeroed.
Interior anchor `00663182` (the `006737F0` drain call).

`0063D8B0` (123 B) is the `[rdx+0x50]`-chain refcount decrement:
each `+0x78`-linked record's `[+0xEC]` indexes the `[r10+0x18]`
0x20-stride table (bounded by `[r10+0x10] & 0x7FFFFFFF`); the first
hit splices `[rbx+0x38]` out into a self-loop, then every hit runs
`sub [elem+0x10], [rbx+0x70]` and `dec [elem+0x14]`.
Interior anchor `0063D916` (the `sub [rax+0x10], ecx`).

`00615C90` (55 B) is the wide zero-init: `005DC1C0(rcx)` runs the
base ctor, then `+0x10`..`+0x48` (nine fields) are cleared and
`rcx` returns.
Interior anchor `00615C99` (the `005DC1C0` call).

`005DC400` (38 B) is the fixed-shape ctor: `[rcx] = 0x1010105`,
`+4 = 1`, `+8`/`+0x14` zeroed, `+0xC = 1.0f`, `+0x18 = 0x400`.
Interior anchor `005DC408` (the `+4` byte store).

## SWE2-EC7-80 update (2026-09-20) - `005DC1C0` base ctor + link measured

`005DC1C0` (59 B) is the base ctor `00615C90` wraps: `word[+8] = 0`,
`dword[+0xC] = 1`, `[rcx] = rdx`, `or dword[rdx+0x18], 0x100`; then if
`[rdx+0x20]` is empty - or its head's `[+8]` byte is clear and that
head's `[+0]` owner is not `rdx` itself - `rcx` registers into
`[rdx+0x20]`; `rcx` returns.
Interior anchor `005DC1D0` (the `+0x18` flag or).

## SWE2-EC7-91 update (2026-09-20) - `0039EA70` + `00396560` + `00395050` measured

`0039EA70` (440 B) is the slim member of the `0039F9F0` builder
family: `0020E680` + `008642A0` + `0039CDC0` produce the record,
16 byte->float lanes fill its `+0x10` block, `+0x40` = 4 and
`+0x48` = 0, `0020E670` publishes, tail `0020E630`.
Interior anchor `0039EA8A` (the `0020E680` call).

`00396560` (1,219 B) is the near-twin of `00396A30`: one input
vec4 ([rcx]) seeds the `022D9xxx` workbench, the loop advances
the source 0x10 per iteration, dot-product chains accumulate
into staged outputs, `00861F14` renormalizes with a
zero-fallback, and `movups [rax-0x10]` writes each staged vec4
until the watermark matches.
Interior anchor `003968BD` (the `00861F14` call).

`00395050` (634 B) is the min-clamped member of the staging
family: the loop advances the source 0x10 per iteration,
accumulates the same dot-product chains, keeps a running
`addps` total, and publishes `minss`-clamped lanes before
writing the staged vec4 to `[r9]`.
Interior anchor `003951BA` (the `cvtps2pd` magnitude arm).

## SWE2-EC7-108 update (2026-09-20) - `00225920` + `002258D0` measured

`00225920` (120 B) is the
`009087E0`-class destructor behind
vtable[0] `0021F0F0` (callers
`0021FEF0`, `002215D0`, `0089A210`
release through it): the `+0x210`
pointer gets `call [*ptr + 8]`
then `call [*ptr]` with `edx = 1`
(virtual teardown plus scalar
delete), `+0x210` and `+8` are
nulled, `00210EB0(+8)` runs the
base dtor, and the vtable steps
back to `00908790` - the standard
derived-to-base chain.
Interior anchor `0022594B` (the
`call [rax + 8]` virtual).

`002258D0` (65 B) is the sibling
dtor for the `00908808` class
(`0021F0B0` at vtable[0]; callers
`0021FB20`, `00221510`, `0089A200`):
`00210EB0(+0x18)`, `+0x18` and
`+8` nulled, vtable back to
`00908790` - the two-field variant
of the same chain.
Interior anchor `002258EC` (the
`00210EB0` call).

## SWE2-EC7-109 update (2026-09-20) - `001EA180` measured

`001EA180` (94 B) is the
guarded release `00181E70`,
`00181F20`, `001C2070`,
`001C2110`, `001C2790`,
`001C2980` and `008980D0` run:
`0067AD90(rcx + 0x40)` takes the
lock, a `qword[+0x38]` with bit
0 clear gets `00584730`, a
`dword[+0x28]` with bit 31 clear
gets `btr`-normalized and freed
through `001C2720(qword[+0x30])`,
and `+0x30` / `+0x28` zero on
exit - the tagged-pointer
release the object family
shares.
Interior anchor `001EA196` (the
`0067AD90` lock call).

## SWE2-EC7-110 update (2026-09-20) - `001C2720` measured

`001C2720` (104 B) is the
tagged-pointer array
destructor seventeen callers
run (`001EA180`, `001EA6C0`,
`0062EDA0`, `006467E0` among
them): null `rcx` exits early,
then `edx` elements at
`qword[rbx]` step 8 - each
non-null pointer with bit 0
clear (`not al; test al, 1;
je` skips the call) goes to
`00584730`, and the same
`00584730(rsi)` frees the
array block itself. The bit-0
gate is the intrusive-marker
convention the object family
uses for borrowed vs owned
slots.
Interior anchor `001C2750`
(the element-fetch loop head).

## SWE2-EC7-116 update (2026-09-21) - `006DA450` / `006C18D0` / `006C0FE0` / `006C0BA0` / `006BEC40` / `006BA720` / `006BA4D0` / `006B82A0` / `006B8180` measured

`006DA450` (19 B) is the
init `006C8750` calls:
stores `rdx` at `+0`,
`dword[+8] = 0`,
`word[+0x8010] = 0`,
returns `rcx`.
Interior anchor `006DA458`
(the `+0x8010` write).

`006C18D0` (69 B) is the
vtable-pair predicate
`006B9CF0` runs:
`(rcx, rdx)` answers 1 for
`(01F2EDA8, 01F2EDE8)` or
`01F2ED68` paired with
`01F2EE08`/`01F2EE28`, 0
otherwise - a known-class
identity test over the
`00D82F28`/`00D83B60`
vtable cells.
Interior anchor `006C18E8`
(the `al = 1` return).

`006C0FE0` (125 B) is the
`00D83B60` destructor
(vtable slot `006C1500`):
when `dword[+0x18]` is
live it walks the
`02E59BB8` list for the
node whose `+0x10` is
`this + 0x10`, unlinks it,
and clears
`02E59BC0[dword[+0x1C]]` -
the registry removal.
Interior anchor `006C1046`
(the unlink store).

`006C0BA0` (229 B) is the
0xE8-record array copy
`006C1060`/`006C1540` run:
`r8` iterations of a
`movups` block move each
`0xE8` source record
(base `rdx + 0x60` fields)
into the `0xE8`-strided
destination at `rcx`.
Interior anchor `006C0BCD`
(the first record store).

`006BEC40` (125 B) is the
same removal shape on the
`02E58CA0` list /
`02E58CB0` table, stamped
with vtable `00D82F28`
(slot `006BED20` - its own
caller) - the sibling
destructor to `006C0FE0`.
Interior anchor `006BECA6`
(the unlink store).

`006BA720` (110 B) is a
`<= 0x32` jump table at
`006BA790` mapping a type
index to its record size -
`{8, 0xC, 0x10, 6, 1, 2, 3,
0x30, 0x40, 4}` - the
size lookup `0067BF70` and
five more call before
allocation.
Interior anchor `006BA731`
(the table-indexed load).

`006BA4D0` (190 B) is the
shrink `006B9CF0` calls:
`edx` clamps the
bit-31-ownership count at
`[+0]`, each surplus
`0x10`-stride record's `+8`
frees through `00584730`
under its own bit 31, and
the whole `+8` array frees
when the count reaches 0.
Interior anchor `006BA54B`
(the record free call).

`006B82A0` (274 B) is the
8-byte introsort: range
`[rcx, rdx)` in qwords,
depth `r8`, `006B7800`
partitions, the smaller
side recurses,
`006B6FE0` insertion-sorts
under 32 elements, and
`006B7290`/`006B8060` heap
fallback runs at depth 0.
Interior anchor `006B82EB`
(the partition call).

`006B8180` (274 B) is the
identical introsort on
4-byte elements (`/4`
counting, `006B7660`
partition, `006B6F30`
insertion, `006B71A0`/
`006B7FC0` heap fallback).
Interior anchor `006B81CB`
(the partition call).

## SWE2-EC7-117 update (2026-09-21) - the sort machinery and thirteen neighbours measured

`006B82A0`'s introsort is
now fully resolved: the
qword partition `006B7800`
(508 B) median-pivots
through `006B6D70`, runs
the two-sided scan under
the indirect comparator at
`qword[rbp]`, and returns
the split pair in
`[rsp+0x50]`; the dword
partition `006B7660`
(411 B) mirrors it with an
inline `cmp` order through
`006B6C20`. Interior anchor
`006B784A` (the qword
median call);
interior anchor `006B769E`
(the dword median call).

The heap halves:
`006B7290` (321 B) and
`006B71A0` (238 B) are the
make_heaps - qword
sift-down under the
`qword[r15]` comparator,
dword sift-down with
inline `cmp` and `cmovae`
child pick. `006B8060`
(150 B) and `006B7FC0`
(146 B) are the
sort_heap drains -
pop-to-back then
`006B7CF0`/`006B7C20`
sift-down per iteration.
Interior anchor `006B7324`
(the comparator call);
interior anchor `006B7219`
(the child cmovae);
interior anchor `006B80C9`
and interior anchor
`006B8025` (the sift-down
calls).

`006B6FE0` (218 B) and
`006B6F30` (169 B) are the
insertion sorts the <32
tails run - qword under
`qword[rbp]` with
`008C2A40` memmove for the
front insert, dword with
the inline shift loop.
Interior anchor `006B703C`
(the comparator call);
interior anchor `006B6F7C`
(the shift decision).

`006B64F0` (26 B) calls
`006B6510` and stamps
`dword[+8] = 1` on a
nonzero answer - the
mark-if-found `0060B980`
and `005FECF0` run.
Interior anchor `006B64FE`.

`006A8C90` (122 B) is the
pointer-array clone
`00646C00` calls: `edx > 1`
allocs `edx * 8` via
`0017D260` (align 8) else
uses the caller's `r9`
buffer, then copies `edx`
qwords.
Interior anchor `006A8CC5`
(the alloc call).

`00684450` (110 B) and
`00684130` (182 B) are the
`"Vector"` / `"Matrix"`
registered-type creators:
`00810240` allocs 0x10 /
0x40, `0080FA50` with the
name string and tag
`0xFFF0B9D8` registers the
class, `00810F60` with
`0xFFFFFFFE` finishes, and
the caller's fields copy
in (4 / 16 dwords).
Interior anchor `00684486`
(the Vector `0080FA50`
call); interior anchor
`00684166` (the Matrix
`0080FA50` call).

`00683B10` (62 B) is the
lookup `005FF7D0`,
`006B2950` and five more
call: `006828F0(rcx, -1)`
then `00811130(rbx, -2)`,
returning the result or
the `02E41590` fallback.
Interior anchor `00683B20`
(the `006828F0` call).

## SWE2-EC7-118 update (2026-09-21) - the sort family's last five measured

`006B7CF0` (257 B) and
`006B7C20` (207 B) are the
sift-downs the batch-82
drains call - qword under
the `qword[r15]` comparator
(`call qword ptr [r15]` at
the child pick), dword with
inline `cmp`/`cmovae`; both
end with the `sar`-parent
bubble-up loop before the
final store.
Interior anchor `006B7D51`
(the qword comparator
call); interior anchor
`006B7C6D` (the dword
child pick).

`006B6D70` (214 B) and
`006B6C20` (322 B) are the
median selectors the
partitions call: above 0x28
elements both sample a
ninth-stride grid -
`006B6D70` defers to four
`006B7560` med3 calls,
`006B6C20` runs the whole
med3 lattice inline on
dwords; at or under 0x28
both collapse to a single
med3.
Interior anchor `006B6DD4`
(the first `006B7560`
call); interior anchor
`006B6C68` (the first
sample compare).

`006B6510` (382 B) is the
capacity check `006B64F0`
gates on: `(edx + 0xF &
~0xF) + 0x10` must fit
`dword[+0x38]`; under
`005CD4F0` it probes
`006B6690` and drains
`+0x48`-list nodes whose
`dword[+8]` is 0, spinning
`005CCB80(1)` per try and
logging "Trying " through
`005CDAA0` every 1024
iterations.
Interior anchor `006B65CE`
(the `005CDAA0` call).

## SWE2-EC7-119 update (2026-09-21) - the med3 and the window probe measured

`006B7560` (125 B) is the
med3 `006B6D70` calls four
times for its ninth-stride
grid: the `[r9]` comparator
orders `*rcx`/`*rdx`, then
`*rdx`/`*r8`, then re-checks
`*rcx`/`*rdx` after the
second swap - the classic
three-element insertion.
Interior anchor `006B7586`
(the first comparator call).

`006B6690` (42 B) is the
wrap-aware window probe
`006B6510` and `00684860`
call: `r8 = [+0x40] + edx`;
returns 1 when the
`[+0x40, +0x48)` window is
non-empty and `r8` reaches
`+0x48`, else 1 only when
`r8 >= [+0x30]` and `+0x48`
equals the `+0x28` limit.
Interior anchor `006B66AB`
(the `+0x30` compare).

`00663080` (114 B) is the
`00D68DF0`-vtable destructor
`00664EB0` (vtable[0]) and
four other sites call:
`00584730` frees `+0x28` and
`+0x18` when their bit-31
ownership flags are clear,
then both cells zero.
Interior anchor `006630B6`
(the first `00584730`).

`006618A0` and `00661720`
(117 B each) are twin
0x48-record copy-construct
loops `0066F780`/`0066F8B0`
and `0066F710`/`0066F7F0`
call: `r8` records copy
from `rdx` into `rcx`,
stamping `+0x28` with
vtables `00D68DE0`
(RTTI `01D204D8`) and
`00D68DD0` (RTTI `01D20458`)
respectively.
Interior anchor `006618F1`
(the `00D68DE0` stamp);
interior anchor `00661771`
(the `00D68DD0` stamp).

## SWE2-EC7-120 update (2026-09-21) - `006467E0` measured

`006467E0` (319 B) is the
eight-field destructor
`0065ECF0`, `0067B3A0`,
`0089FC60`, `008B0660` and
`008B7C70` call: `00584730`
frees `+0x78`, `+0x68`
(count > 1), `+0x58`,
`+0x38`, `+0x28` and
`+0x18` whenever the paired
`+0x70`/`+0x60`/`+0x50`/
`+0x30`/`+0x20`/`+0x10`
bit-31 ownership flag is
clear, `001C2720` runs the
counted teardown on `+0x48`,
`001B7170` on `+8`/`+0`,
and every cell zeroes
behind it.
Interior anchor `0064680C`
(the first `00584730`).

## SWE2-EC7-124 update (2026-09-21) - `00616060` and `006167C0` measured

`00616060` (78 B) is the
small-object ctor
`005D4100`/`00650D40`/
`00655F10` call: `005DCBD0`
base, `00627750(+0x18, 1)`
init, `+0x48`/`+0x50`/
`+0x58`/`+0x60` zeroed,
returns `this`.
Interior anchor `0061608B`
(the `00627750` call).

`006167C0` (62 B) is the
release its nine callers
share: `[+0x20]` released
via `vtable[+0x10]` and
nulled, `+0x1C` clears bit
7, then it tails into
`0016D6A0`.
Interior anchor `006167DE`
(the `vtable[+0x10]`
release).

## SWE2-EC7-125 update (2026-09-21) - the keyed tree find and the adopt-or-clone assign measured

`00606C60` (92 B) is the
keyed tree find `006007B0`
and `0060B980` share: from
the root at `[rcx+0x18]` it
descends by comparing each
node's `+0x18` key against
`rdx`, choosing the `+0` or
`+8` child on the sign of
the compare until the key
matches or the walk returns
to the sentinel. A hit
yields `node+0x20`; the tail
then indexes `[payload+8]`
by `(r8 - [rdx+0x10]) >> 6`
into a 4-byte table, or
returns null on a miss.
Interior anchor `00606CB6`
(the indexed-slot load).

`005DE950` (170 B) is the
assign `005D0D30` and
`00607370` call on the same
`{count|flag, ptr}` pair
shape: it clones the
source's elements through
`005FEE80` (count masked by
`btr 0x1f`, inline storage
when count <= 1), frees the
destination's old heap
buffer through `00584730`
when it was owned
(`!bit31`) and not inline
(`!= +8`), then stores the
new count and pointer.
Interior anchor `005DE98D`
(the `005FEE80` clone call).

## SWE2-EC7-126 update (2026-09-21) - the clone helper, three ctors, and the record copy measured

`005FEE80` (120 B) is the
dword-array clone
`005DE950` uses: `count <= 1`
stays inline at `rcx + 8`;
larger counts allocate
`count*4` through `0017D260`
(alignment 4). The copy loop
walks the destination and
writes `[rbx]` dwords into
non-null slots, advancing
the source per element.
Interior anchor `005FEEB5`
(the `0017D260` call).

`005FE9C0`'s callers also
reach this page's helpers;
its decode is on
game-application.md where
`0060AB10` lives.

`005DCBE0` (44 B) is the
`02CF7A30`-vtable ctor:
`+0 = vtable`, `+8` word =
0x300, `+0xC`/`+0x14`/
`+0x20`/`+0x28` zeroed,
`+0x18` = 2. Interior anchor
`005DCBEC` (the `+8` word
store).

`005DCBD0` (16 B) is the
minimal ctor
`006127C0` and
`00616060` embed: zeroes `+0`, `+8`,
and the `+0x10` byte,
returns `rcx`. Interior anchor `005DCBD9` (the
byte store).

`005DBF30` (31 B) is the
sibling ctor: zeroes
`+0`..`+0x18` and installs
the same `02CF7A30` vtable
at `+0x20`. Interior anchor
`005DBF40` (the vtable
install).

`005D87E0` (218 B) is the
record-array copy
`005D8650` and its
siblings run: `r8d`
elements on a 0x18 stride,
each getting its +0 word,
`+2`/`+3` bytes, a strdup of
the flag-adjusted `+8`
string (length scan,
`0017D260` alloc,
`00861EBA` copy), and the
`+0x10`/`+0x14` dwords.
Null destinations skip.
Interior anchor `005D8866`
(the string alloc).

## SWE2-EC7-127 update (2026-09-21) - the PAnimation hierarchy record family measured

`005C9CF0` (211 B) is the
node-array reallocator under
`005CA460`
(`PAnimationHierarchyPopulateArrays`):
the old array's header is
`[rsi] - 8`, its `0x138`-stride
elements are destroyed
through `00809054` with dtor
`005AA2F0`, and the block is
freed via `00584730`; the new
`count*0x138 + 8` block
(header = element count) is
allocated by `00584740` and
constructed element-wise by
`00808FE4` with ctor
`005A9690`, storing
`{ptr, count}` back to the
owner.
Interior anchor `005C9D62` (the `00584740` array alloc).

`005C99A0` (848 B) is the
node initializer and
back-reference wirer:
`edx < [rcx+8]` selects the
`0x138` node, it is cleared
through `008C2F70` with
`[+0xFF]` zeroed, then for
each `{idx, arg}` pair in the
`rbp` list it calls
`005C0090` and appends the
node pointer to that node's
`+0x110`/`+0x118` vector
(realloc `(n+1)*8` via
`0017D260`, copy, free old).
Two further loops append
`{dword, 0, -1}` triples to
the selected node's stride-12
`+0x110` list - one taking
entries from the `r14` dword
list, one filling from a
running counter - returning
0 when the index is out of
range.
Interior anchor `005C9A28` (the `005C0090` fill call).

`005C62C0` (1133 B) is the
`PNetworkOptimizeBufferAllocator` /
`PAvoidOutputOverwritingInput`
dependency pass: it stack-
allocates a `count*8`
worklist, resets every node's
`+0x130` order field to -1
and zeroes its `+0x118`
triples, then repeatedly
selects the first node whose
`+0x108` predecessor list is
entirely ordered and assigns
it the next sequence number.
The `r14b` flag arm runs a
second sweep that calls the
`005C2F40` predicate and the
`005C0180` resolver through a
stack object (vtables
`00D31298`/`00D32B18`,
RTTI `01CF7A50`/`01CF99D8`),
marking each stride-12 triple
state 1 -> 2 and clearing the
matching byte in the
`[rbp+0x18]` map.
Interior anchor `005C6590` (the `005C0180` resolver call).

`005BEDC0` (135 B) is the
0x58-stride record-array
constructor: each of `edx`
records receives a fresh
`006372A0` object at `+0x00`
and zeroed fields through
`+0x50`.
Interior anchor `005BEDFF` (the `006372A0` factory call).

`005B7FD0` (114 B) is the
matching array destructor:
it walks `rcx+0x28` stepping
`0x58`, frees each record's
tagged heap member when its
low bit marks it owned
(`00584730`), then frees the
array block itself.
Interior anchor `005B8028` (the array free).

`005AA0E0` (125 B) is the
`PAnimationSlotFilter` /
`PAnimationHierarchyNode`
destructor: vtable
`00D31548` (RTTI `01CF8148`)
is installed, the `+0x30`/
`+0x38` counted vector is
destroyed via `005B8050`, the
`+0x18`/`+0x20` heap member
is freed via `00584730`, both
are zeroed, and the object
re-bases to vtable
`00D312F0` (RTTI `01CF7B40`)
for the base-class unwind.
Interior anchor `005AA117` (the `005B8050` vector destroy).

`005A7E90` (61 B) is the
argument-forwarding thunk the
`005C72A0` composer
(`PAnimationTargetBlenderController`)
calls twice per blend: it
spills `rdx/r8/r9` into a
stack arg array and invokes
`[rcx+0x28]`'s `vtable[+0x10]`
method with
`(self, 0, 0, &args)`.
Interior anchor `005A7EC5` (the `vtable[+0x10]` call).

`005A5DC0` (137 B) is the
flat 0x98-record copy -
nine `movups` pairs plus a
`movsd` tail per element,
`r8d` iterations.
Interior anchor `005A5E1D` (the `+0x80` movups pair).

`005A5CC0` (254 B) is the
0x58-stride record deep-copy:
the header fields are copied,
the `+0x28` counted
string/blob is deep-cloned
(low-bit flag stripped from
the stored pointer, length
found by a backward NUL scan,
`0017D260` alloc with
alignment 2, `00861EBA`
copy), and the tail fields
through `+0x57` complete each
record.
Interior anchor `005A5D5A` (the string alloc call).

`005C2F40` (154 B) is the `(object,index)` referrer predicate `005C62C0` consults: outer loop walks `[rcx+0x128]`'s `+0x120`-counted (`& 0x7fffffff`) record pointers; per record, an inner loop scans the `[r10+0x108]` pair table (`[r10+0x100]` count, 16-byte elements) for an element whose `+0` equals `rcx` itself (the searched object) and `+8` equals `edx` (the index). Each match ANDs `r8b` with `[r10+0x130] != -1` — so the return is `1` only when every matched referrer record has `+0x130 != -1` (and vacuously `1` when none match).

Interior anchor `005C2F95` (function `005C2F40`).

`005C0180` (404 B) is the three-tier slot allocator `005C62C0` runs after `005C2F40`, over the `+8`-table of `[rbx+0x10]`-counted 8-byte `{flag, key}` elements: tier 1 takes the lowest `+4` key `>= edx` among `+0`-clear elements the `[rbp]->vtable[0]` callback accepts; tier 2 (no `edx` bound) takes the callback-accepted element with the highest `+4`; tier 3 takes the first `{0,0}` empty element; if all fail it calls `005C5A40` (the grow) and tail-recurses on success. A won index gets `+0 = 1` and `+4 = max(+4, edx)` written back; returns the index, `-1` only when the grow fails.

Interior anchor `005C01EB` (function `005C0180`).

`005C0090` (234 B) is the 16-byte-element `push_back` `005C99A0` uses to append `(rdx, r8d)` pairs: reads count `[rbx+0x100]` (`btr 0x1f`), allocates `(count+1)*16` via `0017D260` (align 8), `movups`-copies the old `[rbx+0x108]` array, writes the new element at index `count`, frees the old buffer via `00584730` only when it differs and the stored count's high bit was clear (the same inline-storage flag the teardown siblings honor), then stores `count+1` back. Returns `1` on success, `0` when the allocation fails — no spare-capacity field exists, so every append reallocs.

Interior anchor `005C010C` (function `005C0090`).

`005A5BD0` (227 B) is the `0x38`-stride record deep-copy `005AA450`/`005AD2B0` run over `PAnimationHierarchy` node tables: per record it copies `+0`/`+8`/`+0x10`/`+0x18` qwords and the `+0x20` dword verbatim, then if the `+0x28` pointer's low bit tags a string (`&1` stripped into `rdi`) it forward-scans for the NUL, allocates `len+1` via `0017D260` (align 2), `00861EBA`-copies the bytes, and stores the clone at `+0x28`; the `+0x30` dword is copied last. A null tagged pointer leaves `+0x28` zero.

Interior anchor `005A5C7C` (function `005A5BD0`).

`005C5A40` (216 B) is the `+8`-table grow `005C0180`'s allocator tail-calls when all three tiers miss: new capacity `max(2*count, count+0x10)`, `00584740(cap*8)` allocation (`mul`+`cmovo` overflow guard to `-1`), zero-init of each 8-byte `{0,0}` element, copy of the old `[rdi+8]` table's `[rdi+0x10]` entries, `00584730` free of the old buffer, then `+8`/`+0x10` rewritten — returns 1, or 0 only when the allocation fails (which is what makes `005C0180` return `-1`).

Interior anchor `005C5AB0` (function `005C5A40`).

`0027C3D0` (717 B) is the battle-menu dispatch arm `002778C0` installs: `00241A50`, `00272EE0`, `00309B40`, `00311AF0`, `00311CD0` x3 and `00273270` run the command's selected-entry handling - the menu dispatcher's `00311CD0`-triple arm.

Interior anchor `0027C4D2` (function `0027C3D0`).

`0027BED0` (634 B) is the slot claim the dispatch arm `002778C0` calls (the same table family `0027C3D0` walks): `dword[rcx+0x40]` counts the `rbp+0x50` records at stride 8 with the `+4 & 2` flag skip, the four `r11` keys are searched then a `+0x54` first-free scan runs, and `002E9D10` x2/`00203080`/`002703F0`/`00272250`/`00273850`/`00808C40` fill the claimed slot - the dispatch table's keyed insert.

Interior anchor `0027BFDF` (function `0027BED0`).

`0021AB20` (153 B) is the vector teardown `0021AC00` calls: it runs each `0xA0`-stride object's `[vtable+0x38]` method with `edx = 0` across `[rcx]..[rcx+8]`, then frees the buffer through the allocator at `[rsi+0x18]` - count recomputed as `(end - start) / 0xA0` via the `0x6666666666666667` multiply and the free gets `(rdx = [rsi], r8d = count*0xA0)`.

Interior anchor `0021AB58` (function `0021AB20`).

`00219530` (146 B) is the `vector<0x68>` teardown `00219470`/`00219610` (the `SepAudioController` row) and `00899E60` share: walk `[rcx]`..`[rcx+8]` in `0x68` strides calling vtable `+0x38` on each element, then the classic `_Tidy` tail - the element count comes from `(r8 - r10)` scaled by `0x4EC4EC4EC4EC4EC5` (divide by 104), and the allocator vtable `+0x18` deallocates - the per-element destructor loop the audio controller family's vectors run.

Interior anchor `00219568` (function `00219530`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-vtable-method-index-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `005C3C10` | 134 B | returns the address of the 0x18-byte static at `02CB5D60`, filling it once under the thread-safe static guard dword `02CB5D78` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5D60` = `02CAD140` OR 1, qword `02CB5D68` = the return of `00630180`, qword `02CB5D70` = 0 | `005C3C4C`, `005C3C47`, `005C3C60`, `005C3C85` |
| `005C3DB0` | 134 B | returns the address of the 0x18-byte static at `02CB5AE0`, filling it once under the thread-safe static guard dword `02CB5AF8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5AE0` = `02CAD140` OR 1, qword `02CB5AE8` = the return of `00630180`, qword `02CB5AF0` = 0 | `005C3DEC`, `005C3DE7`, `005C3E00`, `005C3E25` |
| `005C4020` | 133 B | returns the address of the 0x18-byte static at `02CB5B60`, filling it once under the thread-safe static guard dword `02CB5B78` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5B60` = `02CAD140` OR 1, qword `02CB5B68` = `02CAD840` OR 1, qword `02CB5B70` = 0 | `005C405F`, `005C405A`, `005C4085`, `005C409E` |
| `005C40B0` | 133 B | returns the address of the 0x18-byte static at `02CB5B80`, filling it once under the thread-safe static guard dword `02CB5B98` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5B80` = `02CAD140` OR 1, qword `02CB5B88` = `02CAE660` OR 1, qword `02CB5B90` = 0 | `005C40EF`, `005C40EA`, `005C4115`, `005C412E` |
| `005C4250` | 134 B | returns the address of the 0x18-byte static at `02CB5BA0`, filling it once under the thread-safe static guard dword `02CB5BB8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5BA0` = `02CAD140` OR 1, qword `02CB5BA8` = the return of `006301F0`, qword `02CB5BB0` = 0 | `005C428C`, `005C4287`, `005C42A0`, `005C42C5` |
| `005C4360` | 134 B | returns the address of the 0x18-byte static at `02CB5D08`, filling it once under the thread-safe static guard dword `02CB5D20` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5D08` = `02CAD140` OR 1, qword `02CB5D10` = the return of `00630180`, qword `02CB5D18` = 0 | `005C439C`, `005C4397`, `005C43B0`, `005C43D5` |
| `005C4770` | 134 B | returns the address of the 0x18-byte static at `02CB5DE8`, filling it once under the thread-safe static guard dword `02CB5E00` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5DE8` = `02CAD840` OR 1, qword `02CB5DF0` = the return of `00630180`, qword `02CB5DF8` = 0 | `005C47AC`, `005C47A7`, `005C47C0`, `005C47E5` |
| `005C4800` | 134 B | returns the address of the 0x18-byte static at `02CB5DC8`, filling it once under the thread-safe static guard dword `02CB5DE0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5DC8` = `02CAD840` OR 1, qword `02CB5DD0` = the return of `00630180`, qword `02CB5DD8` = 0 | `005C483C`, `005C4837`, `005C4850`, `005C4875` |
| `005C4890` | 134 B | returns the address of the 0x18-byte static at `02CB5A30`, filling it once under the thread-safe static guard dword `02CB5A48` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5A30` = `02CAD840` OR 1, qword `02CB5A38` = the return of `00630180`, qword `02CB5A40` = 0 | `005C48CC`, `005C48C7`, `005C48E0`, `005C4905` |
| `005C4920` | 133 B | returns the address of the 0x18-byte static at `02CB5A50`, filling it once under the thread-safe static guard dword `02CB5A68` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5A50` = `02CAD840` OR 1, qword `02CB5A58` = `02CF8780` OR 1, qword `02CB5A60` = 0 | `005C495F`, `005C495A`, `005C4985`, `005C499E` |
| `005C4A40` | 134 B | returns the address of the 0x18-byte static at `02CB5C40`, filling it once under the thread-safe static guard dword `02CB5C58` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5C40` = `02CAE660` OR 1, qword `02CB5C48` = the return of `00630180`, qword `02CB5C50` = 0 | `005C4A7C`, `005C4A77`, `005C4A90`, `005C4AB5` |
| `005C4AD0` | 133 B | returns the address of the 0x18-byte static at `02CB59F0`, filling it once under the thread-safe static guard dword `02CB5A08` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB59F0` = `02CAE660` OR 1, qword `02CB59F8` = `02CF8780` OR 1, qword `02CB5A00` = 0 | `005C4B0F`, `005C4B0A`, `005C4B35`, `005C4B4E` |
| `005C4B60` | 133 B | returns the address of the 0x18-byte static at `02CB5A10`, filling it once under the thread-safe static guard dword `02CB5A28` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5A10` = `02CAE660` OR 1, qword `02CB5A18` = `02CAD840` OR 1, qword `02CB5A20` = 0 | `005C4B9F`, `005C4B9A`, `005C4BC5`, `005C4BDE` |
| `00603DB0` | 134 B | returns the address of the 0x18-byte static at `02CED310`, filling it once under the thread-safe static guard dword `02CED328` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED310` = `02CB6E80` OR 1, qword `02CED318` = the return of `00630180`, qword `02CED320` = 0 | `00603DEC`, `00603DE7`, `00603E00`, `00603E25` |
| `00603FE0` | 133 B | returns the address of the 0x18-byte static at `02CED0E8`, filling it once under the thread-safe static guard dword `02CED100` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED0E8` = `02CB6E80` OR 1, qword `02CED0F0` = `02CB7080` OR 1, qword `02CED0F8` = 0 | `0060401F`, `0060401A`, `00604045`, `0060405E` |
| `00604100` | 134 B | returns the address of the 0x18-byte static at `02CED040`, filling it once under the thread-safe static guard dword `02CED058` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED040` = `02CB77A0` OR 1, qword `02CED048` = the return of `00630180`, qword `02CED050` = 0 | `0060413C`, `00604137`, `00604150`, `00604175` |
| `00604190` | 134 B | returns the address of the 0x18-byte static at `02CED060`, filling it once under the thread-safe static guard dword `02CED078` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED060` = `02CB77A0` OR 1, qword `02CED068` = the return of `006301F0`, qword `02CED070` = 0 | `006041CC`, `006041C7`, `006041E0`, `00604205` |
| `0063B660` | 133 B | returns the address of the 0x18-byte static at `02CF97C0`, filling it once under the thread-safe static guard dword `02CF97D8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CF97C0` = `02CF8780` OR 1, qword `02CF97C8` = `02CF8470` OR 1, qword `02CF97D0` = 0 | `0063B69F`, `0063B69A`, `0063B6C5`, `0063B6DE` |
| `0063B6F0` | 133 B | returns the address of the 0x18-byte static at `02CF97A0`, filling it once under the thread-safe static guard dword `02CF97B8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CF97A0` = `02CF8780` OR 1, qword `02CF97A8` = `02CF8270` OR 1, qword `02CF97B0` = 0 | `0063B72F`, `0063B72A`, `0063B755`, `0063B76E` |
| `0063B800` | 133 B | returns the address of the 0x18-byte static at `02CF9780`, filling it once under the thread-safe static guard dword `02CF9798` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CF9780` = `02CF8780` OR 1, qword `02CF9788` = `02CF8470` OR 1, qword `02CF9790` = 0 | `0063B83F`, `0063B83A`, `0063B865`, `0063B87E` |
| `006AC860` | 133 B | returns the address of the 0x18-byte static at `02E4EFD0`, filling it once under the thread-safe static guard dword `02E4EFE8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E4EFD0` = `02E4EAF0` OR 1, qword `02E4EFD8` = `02CF8470` OR 1, qword `02E4EFE0` = 0 | `006AC89F`, `006AC89A`, `006AC8C5`, `006AC8DE` |
| `006AC8F0` | 133 B | returns the address of the 0x18-byte static at `02E4EF48`, filling it once under the thread-safe static guard dword `02E4EF60` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E4EF48` = `02E4EAF0` OR 1, qword `02E4EF50` = `02E4E720` OR 1, qword `02E4EF58` = 0 | `006AC92F`, `006AC92A`, `006AC955`, `006AC96E` |
| `006AC980` | 133 B | returns the address of the 0x18-byte static at `02E4EF68`, filling it once under the thread-safe static guard dword `02E4EF80` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E4EF68` = `02E4EAF0` OR 1, qword `02E4EF70` = `02E404B0` OR 1, qword `02E4EF78` = 0 | `006AC9BF`, `006AC9BA`, `006AC9E5`, `006AC9FE` |
| `006AF450` | 133 B | returns the address of the 0x18-byte static at `02E4FE28`, filling it once under the thread-safe static guard dword `02E4FE40` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E4FE28` = `02E4F900` OR 1, qword `02E4FE30` = `02CF8470` OR 1, qword `02E4FE38` = 0 | `006AF48F`, `006AF48A`, `006AF4B5`, `006AF4CE` |
| `006B2680` | 132 B | returns the address of the 0x18-byte static at `02E51510`, filling it once under the thread-safe static guard dword `02E51528` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E51510` = the return of `006B0B20` OR 1, qword `02E51518` = the return of `006301F0`, qword `02E51520` = 0 | `006B26BC`, `006B26B7`, `006B26CE`, `006B26F3` |
| `006B2710` | 132 B | returns the address of the 0x18-byte static at `02E514D0`, filling it once under the thread-safe static guard dword `02E514E8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E514D0` = the return of `006B0EC0` OR 1, qword `02E514D8` = the return of `006301F0`, qword `02E514E0` = 0 | `006B274C`, `006B2747`, `006B275E`, `006B2783` |
| `006B27A0` | 132 B | returns the address of the 0x18-byte static at `02E51550`, filling it once under the thread-safe static guard dword `02E51568` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E51550` = the return of `006B1320` OR 1, qword `02E51558` = the return of `006301F0`, qword `02E51560` = 0 | `006B27DC`, `006B27D7`, `006B27EE`, `006B2813` |
| `006B2830` | 132 B | returns the address of the 0x18-byte static at `02E51530`, filling it once under the thread-safe static guard dword `02E51548` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E51530` = the return of `006B1600` OR 1, qword `02E51538` = the return of `006301F0`, qword `02E51540` = 0 | `006B286C`, `006B2867`, `006B287E`, `006B28A3` |
| `006B28C0` | 132 B | returns the address of the 0x18-byte static at `02E514F0`, filling it once under the thread-safe static guard dword `02E51508` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E514F0` = the return of `006B19A0` OR 1, qword `02E514F8` = the return of `006301F0`, qword `02E51500` = 0 | `006B28FC`, `006B28F7`, `006B290E`, `006B2933` |
| `006B5B30` | 133 B | returns the address of the 0x18-byte static at `02E521C8`, filling it once under the thread-safe static guard dword `02E521E0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E521C8` = `02E518D0` OR 1, qword `02E521D0` = `02E404B0` OR 1, qword `02E521D8` = 0 | `006B5B6F`, `006B5B6A`, `006B5B95`, `006B5BAE` |
| `006C03A0` | 133 B | returns the address of the 0x18-byte static at `02E59698`, filling it once under the thread-safe static guard dword `02E596B0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E59698` = `02E58DB0` OR 1, qword `02E596A0` = `02E404B0` OR 1, qword `02E596A8` = 0 | `006C03DF`, `006C03DA`, `006C0405`, `006C041E` |
| `0077E020` | 128 B | calls `00727440(rcx)` and returns its result when negative; calls `0076BE10(qword [rcx+0x238], rcx+0xCC)` and returns 0x80004005 when that is negative; then walks the signed dword `[rcx+0xDC]` entries of the 0x108-stride array that starts at qword `[rcx+0x4B8]` + 0xA0 and returns 0x80004005 at the first entry whose pointed-to object has dword `+0x44` equal to 0; otherwise returns 0 | `0077E029`, `0077E040`, `0077E073`, `0077E095` |
| `00780BB0` | 129 B | calls vtable slot `+8` of the object at qword `[rcx+0x38]`, zeroes qword `[rcx+0x90]`, then for each of the four qwords `[rcx+0x48]`..`[rcx+0x60]` and for qword `[rcx+0x98]` that is non-null calls that object's vtable slot `+8` and nulls the qword; finally tail-jumps to `00727410(rcx)` | `00780BCE`, `00780BD7`, `00780BEC`, `00780C0B` |
| `00786110` | 128 B | returns 0 at once when qword `[rcx+0xF0]` is null; otherwise calls the object's own vtable slot `+0x50` with `edx` = 0..9 (ten calls), keeping the last negative result, then, when qword `[rcx+0xF0]` is still non-null, calls `006DA8A0(qword [01F3BA68], that pointer - 8)` and zeroes the qword; returns the kept result (0 when no call was negative) | `00786116`, `00786148`, `0078614D`, `00786173` |
| `0079CB60` | 133 B | returns the address of the 0x18-byte static at `02EACD98`, filling it once under the thread-safe static guard dword `02EACDB0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02EACD98` = `02EA5660` OR 1, qword `02EACDA0` = `02D3F310` OR 1, qword `02EACDA8` = 0 | `0079CB9F`, `0079CB9A`, `0079CBC5`, `0079CBDE` |
| `007DA970` | 130 B | adds the float in `xmm1` to two float cells: when byte `[rcx+0x38]` is nonzero it stores float `[rcx+0x28]` + `xmm1` to float `[rcx+0x28]` and, when that sum is not below float `[rcx+0x2C]` (comiss), stores float `[rcx+0x2C]` there and stores 0 to the byte, otherwise stores 1 to the byte, then calls the object's vtable slot `+0x40`; the same for byte `[rcx+0x68]` with floats `[rcx+0x58]` / `[rcx+0x5C]` and a second `+0x40` call; returns 0 | `007DA98F`, `007DA99E`, `007DA9B9`, `007DA9E2` |
| `007DFA70` | 131 B | under the critical section at `rcx+8` (`EnterCriticalSection` / `LeaveCriticalSection` through `008C20B8` / `008C20C0`) sets byte `[rcx+0x70]` to 1 and copies dword i of the array at qword `[rcx+0x68]` to dword i at `rdx` for i below `007AECE0()` (re-read every step); returns 0 | `007DFA95`, `007DFA9B`, `007DFABE`, `007DFAD5` |
| `00848880` | 133 B | walks the dword `[rcx+0xC]` 0x20-byte entries of the array at qword `[rcx+0x18]`; for each it asks the predicate object `rdx` through its vtable slot `+8` (argument: the entry); on true it calls `rcx`'s vtable slot `+0x10` with the entry's qwords `+0` and `+8` and `r8`, decrements dword `02EAF39C` and re-tests the same index without advancing; on false it moves to the next entry | `008488C0`, `008488D7`, `008488DA`, `008488E4` |
| `0084A6B0` | 132 B | when dword `[rcx+0x5C]` plus dword `[rcx+0x1C]` is 0, calls `00841010` on `rcx+8` and on `rcx+0x48`, then resets the object: word `+0xDD` = 0x100, dword `+0xAC` = 0, qwords `+0xC4` / `+0xCC` / `+0xD4` = 0, qwords `+0xBC` and `+0xB0` = 1, dword `+0xB8` = 0xA and qwords `+0x88` / `+0x90` / `+0x98` = 0; otherwise does nothing | `0084A6C5`, `0084A6CE`, `0084A6D5`, `0084A70F` |
| `00858560` | 128 B | copies the 16 bytes at `rdx` to `rcx+0x140`, then for each of the dword `[rcx+0x124]` object pointers in the array at qword `[rcx+0x130]` calls `00854110(object, rdx)` unless the object's dword `+0xF4` is 2 or 5 or bit `0x1` of its byte `+0x230` is set | `0085857A`, `0085859C`, `008585AC`, `008585B8` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-vtable-method-index-ee-1003-2)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-vtable-method-index-ee-1003-2/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `005C4140` | 138 B | returns the address of the 0x18-byte static at `02CB5B40`, filling it once under the thread-safe static guard dword `02CB5B58` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5B40` = `02CAD140` OR 1, qword `02CB5B48` = the return of `0062FF50` OR 1, qword `02CB5B50` = 0 | `005C4177`, `005C417C`, `005C4190`, `005C41B9` |
| `005C49B0` | 138 B | returns the address of the 0x18-byte static at `02CB5A70`, filling it once under the thread-safe static guard dword `02CB5A88` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CB5A70` = `02CAD840` OR 1, qword `02CB5A78` = the return of `0062FF50` OR 1, qword `02CB5A80` = 0 | `005C49E7`, `005C49EC`, `005C4A00`, `005C4A29` |
| `00603850` | 150 B | returns the address of the 0x20-byte static at `02CED1F0`, filling it once under the thread-safe static guard dword `02CED210` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED1F0` = `02CB6B80` OR 1, qword `02CED1F8` = the return of `0062FF50` OR 1, qword `02CED200` = the return of `00630110`, qword `02CED208` = 0 | `00603887`, `0060388C`, `006038A0`, `006038B7`, `006038D5` |
| `006038F0` | 150 B | returns the address of the 0x20-byte static at `02CED1C8`, filling it once under the thread-safe static guard dword `02CED1E8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED1C8` = `02CB6B80` OR 1, qword `02CED1D0` = the return of `0062FF50` OR 1, qword `02CED1D8` = the return of `00630180`, qword `02CED1E0` = 0 | `00603927`, `0060392C`, `00603940`, `00603957`, `00603975` |
| `00603990` | 150 B | returns the address of the 0x20-byte static at `02CED218`, filling it once under the thread-safe static guard dword `02CED238` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED218` = `02CB6B80` OR 1, qword `02CED220` = the return of `0062FF50` OR 1, qword `02CED228` = the return of `006301F0`, qword `02CED230` = 0 | `006039C7`, `006039CC`, `006039E0`, `006039F7`, `00603A15` |
| `00603A30` | 150 B | returns the address of the 0x20-byte static at `02CED128`, filling it once under the thread-safe static guard dword `02CED148` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED128` = `02CB6B80` OR 1, qword `02CED130` = the return of `0062FF50` OR 1, qword `02CED138` = the return of `006B08A0`, qword `02CED140` = 0 | `00603A67`, `00603A6C`, `00603A80`, `00603A97`, `00603AB5` |
| `00603AD0` | 150 B | returns the address of the 0x20-byte static at `02CED1A0`, filling it once under the thread-safe static guard dword `02CED1C0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED1A0` = `02CB6B80` OR 1, qword `02CED1A8` = the return of `0062FF50` OR 1, qword `02CED1B0` = the return of `006B0B20`, qword `02CED1B8` = 0 | `00603B07`, `00603B0C`, `00603B20`, `00603B37`, `00603B55` |
| `00603B70` | 150 B | returns the address of the 0x20-byte static at `02CED178`, filling it once under the thread-safe static guard dword `02CED198` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED178` = `02CB6B80` OR 1, qword `02CED180` = the return of `0062FF50` OR 1, qword `02CED188` = the return of `006B1600`, qword `02CED190` = 0 | `00603BA7`, `00603BAC`, `00603BC0`, `00603BD7`, `00603BF5` |
| `00603C10` | 150 B | returns the address of the 0x20-byte static at `02CED150`, filling it once under the thread-safe static guard dword `02CED170` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED150` = `02CB6B80` OR 1, qword `02CED158` = the return of `0062FF50` OR 1, qword `02CED160` = the return of `006B19A0`, qword `02CED168` = 0 | `00603C47`, `00603C4C`, `00603C60`, `00603C77`, `00603C95` |
| `00604070` | 138 B | returns the address of the 0x18-byte static at `02CED108`, filling it once under the thread-safe static guard dword `02CED120` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED108` = `02CB6E80` OR 1, qword `02CED110` = the return of `006B19A0` OR 1, qword `02CED118` = 0 | `006040A7`, `006040AC`, `006040C0`, `006040E9` |
| `00604320` | 134 B | returns the address of the 0x18-byte static at `02CED020`, filling it once under the thread-safe static guard dword `02CED038` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02CED020` = `02CB77A0` OR 1, qword `02CED028` = the return of `00630490`, qword `02CED030` = 0 | `0060435C`, `00604357`, `00604370`, `00604395` |
| `00653950` | 134 B | returns the address of the 0x18-byte static at `02D384A0`, filling it once under the thread-safe static guard dword `02D384B8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02D384A0` = `02D36CA0` OR 1, qword `02D384A8` = the return of `00630180`, qword `02D384B0` = 0 | `0065398C`, `00653987`, `006539A0`, `006539C5` |
| `006539E0` | 134 B | returns the address of the 0x18-byte static at `02D384C8`, filling it once under the thread-safe static guard dword `02D384E0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02D384C8` = `02D36CA0` OR 1, qword `02D384D0` = the return of `00630180`, qword `02D384D8` = 0 | `00653A1C`, `00653A17`, `00653A30`, `00653A55` |
| `00653A70` | 134 B | returns the address of the 0x18-byte static at `02D384E8`, filling it once under the thread-safe static guard dword `02D38500` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02D384E8` = `02D36CA0` OR 1, qword `02D384F0` = the return of `00630180`, qword `02D384F8` = 0 | `00653AAC`, `00653AA7`, `00653AC0`, `00653AE5` |
| `00670B30` | 134 B | returns the address of the 0x18-byte static at `02D3E178`, filling it once under the thread-safe static guard dword `02D3E190` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02D3E178` = `02D3A440` OR 1, qword `02D3E180` = the return of `00630180`, qword `02D3E188` = 0 | `00670B6C`, `00670B67`, `00670B80`, `00670BA5` |
| `00670C60` | 138 B | returns the address of the 0x18-byte static at `02D3E140`, filling it once under the thread-safe static guard dword `02D3E158` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02D3E140` = `02D3A640` OR 1, qword `02D3E148` = the return of `0062FF50` OR 1, qword `02D3E150` = 0 | `00670C97`, `00670C9C`, `00670CB0`, `00670CD9` |
| `00679070` | 134 B | returns the address of the 0x18-byte static at `02D3F7C8`, filling it once under the thread-safe static guard dword `02D3F7E0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02D3F7C8` = `02D3F310` OR 1, qword `02D3F7D0` = the return of `006301F0`, qword `02D3F7D8` = 0 | `006790AC`, `006790A7`, `006790C0`, `006790E5` |
| `0067F140` | 138 B | returns the address of the 0x18-byte static at `02E407C8`, filling it once under the thread-safe static guard dword `02E407E0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E407C8` = `02E404B0` OR 1, qword `02E407D0` = the return of `006B09E0` OR 1, qword `02E407D8` = 0 | `0067F177`, `0067F17C`, `0067F190`, `0067F1B9` |
| `0067F1D0` | 138 B | returns the address of the 0x18-byte static at `02E407A8`, filling it once under the thread-safe static guard dword `02E407C0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E407A8` = `02E404B0` OR 1, qword `02E407B0` = the return of `006B33F0` OR 1, qword `02E407B8` = 0 | `0067F207`, `0067F20C`, `0067F220`, `0067F249` |
| `006A2DD0` | 138 B | returns the address of the 0x18-byte static at `02E4D458`, filling it once under the thread-safe static guard dword `02E4D470` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E4D458` = `02E48BD0` OR 1, qword `02E4D460` = the return of `006B1600` OR 1, qword `02E4D468` = 0 | `006A2E07`, `006A2E0C`, `006A2E20`, `006A2E49` |
| `006A3060` | 138 B | returns the address of the 0x18-byte static at `02E4D490`, filling it once under the thread-safe static guard dword `02E4D4A8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E4D490` = `02E489D0` OR 1, qword `02E4D498` = the return of `006B0EC0` OR 1, qword `02E4D4A0` = 0 | `006A3097`, `006A309C`, `006A30B0`, `006A30D9` |
| `006A30F0` | 138 B | returns the address of the 0x18-byte static at `02E4D4B0`, filling it once under the thread-safe static guard dword `02E4D4C8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E4D4B0` = `02E489D0` OR 1, qword `02E4D4B8` = the return of `006B1600` OR 1, qword `02E4D4C0` = 0 | `006A3127`, `006A312C`, `006A3140`, `006A3169` |
| `006A8FA0` | 134 B | returns the address of the 0x18-byte static at `02E4DFE0`, filling it once under the thread-safe static guard dword `02E4DFF8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E4DFE0` = `02E4D940` OR 1, qword `02E4DFE8` = the return of `00630490`, qword `02E4DFF0` = 0 | `006A8FDC`, `006A8FD7`, `006A8FF0`, `006A9015` |
| `006A90B0` | 138 B | returns the address of the 0x18-byte static at `02E4E000`, filling it once under the thread-safe static guard dword `02E4E018` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E4E000` = `02E4D940` OR 1, qword `02E4E008` = the return of `0062FF50` OR 1, qword `02E4E010` = 0 | `006A90E7`, `006A90EC`, `006A9100`, `006A9129` |
| `006AD4F0` | 138 B | returns the address of the 0x18-byte static at `02E4F448`, filling it once under the thread-safe static guard dword `02E4F460` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E4F448` = `02E4F290` OR 1, qword `02E4F450` = the return of `006B19A0` OR 1, qword `02E4F458` = 0 | `006AD527`, `006AD52C`, `006AD540`, `006AD569` |
| `006AF340` | 134 B | returns the address of the 0x18-byte static at `02E4FE60`, filling it once under the thread-safe static guard dword `02E4FE78` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E4FE60` = `02E4F900` OR 1, qword `02E4FE68` = the return of `00630180`, qword `02E4FE70` = 0 | `006AF37C`, `006AF377`, `006AF390`, `006AF3B5` |
| `006B3120` | 142 B | with `rcx` a callback table: returns 0 when `rdx` is null; otherwise adds 8 to the qword cursor its fifth argument points at, converts the double at the new cursor - 8 to float and calls the table's slot `+8` with (`rdx`, that float); when `r9` is non-null and `r8` equals `006B0B20()` OR 1 it stores the result to qword `[r9+8]`, zeroes qword `[r9]` and returns 1, else returns 0 | `006B3145`, `006B3155`, `006B3161`, `006B316F` |
| `006B31B0` | 142 B | with `rcx` a callback table: returns 0 when `rdx` is null; otherwise adds 8 to the qword cursor its fifth argument points at, converts the double at the new cursor - 8 to float and calls the table's slot `+8` with (`rdx`, that float); when `r9` is non-null and `r8` equals `006B0EC0()` OR 1 it stores the result to qword `[r9+8]`, zeroes qword `[r9]` and returns 1, else returns 0 | `006B31D5`, `006B31E5`, `006B31F1`, `006B31FF` |
| `006B3240` | 142 B | with `rcx` a callback table: returns 0 when `rdx` is null; otherwise adds 8 to the qword cursor its fifth argument points at, converts the double at the new cursor - 8 to float and calls the table's slot `+8` with (`rdx`, that float); when `r9` is non-null and `r8` equals `006B1320()` OR 1 it stores the result to qword `[r9+8]`, zeroes qword `[r9]` and returns 1, else returns 0 | `006B3265`, `006B3275`, `006B3281`, `006B328F` |
| `006B32D0` | 142 B | with `rcx` a callback table: returns 0 when `rdx` is null; otherwise adds 8 to the qword cursor its fifth argument points at, converts the double at the new cursor - 8 to float and calls the table's slot `+8` with (`rdx`, that float); when `r9` is non-null and `r8` equals `006B1600()` OR 1 it stores the result to qword `[r9+8]`, zeroes qword `[r9]` and returns 1, else returns 0 | `006B32F5`, `006B3305`, `006B3311`, `006B331F` |
| `006B3360` | 142 B | with `rcx` a callback table: returns 0 when `rdx` is null; otherwise adds 8 to the qword cursor its fifth argument points at, converts the double at the new cursor - 8 to float and calls the table's slot `+8` with (`rdx`, that float); when `r9` is non-null and `r8` equals `006B19A0()` OR 1 it stores the result to qword `[r9+8]`, zeroes qword `[r9]` and returns 1, else returns 0 | `006B3385`, `006B3395`, `006B33A1`, `006B33AF` |
| `006B5810` | 138 B | returns the address of the 0x18-byte static at `02E521E8`, filling it once under the thread-safe static guard dword `02E52200` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E521E8` = `02E518D0` OR 1, qword `02E521F0` = the return of `0062FF50` OR 1, qword `02E521F8` = 0 | `006B5847`, `006B584C`, `006B5860`, `006B5889` |
| `006B5AA0` | 138 B | returns the address of the 0x18-byte static at `02E521A8`, filling it once under the thread-safe static guard dword `02E521C0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E521A8` = `02E518D0` OR 1, qword `02E521B0` = the return of `006B09E0` OR 1, qword `02E521B8` = 0 | `006B5AD7`, `006B5ADC`, `006B5AF0`, `006B5B19` |
| `006B5BC0` | 138 B | returns the address of the 0x18-byte static at `02E52188`, filling it once under the thread-safe static guard dword `02E521A0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E52188` = `02E518D0` OR 1, qword `02E52190` = the return of `0062FF50` OR 1, qword `02E52198` = 0 | `006B5BF7`, `006B5BFC`, `006B5C10`, `006B5C39` |
| `006C01C0` | 134 B | returns the address of the 0x18-byte static at `02E59700`, filling it once under the thread-safe static guard dword `02E59718` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E59700` = `02E58DB0` OR 1, qword `02E59708` = the return of `006301F0`, qword `02E59710` = 0 | `006C01FC`, `006C01F7`, `006C0210`, `006C0235` |
| `006C0430` | 138 B | returns the address of the 0x18-byte static at `02E596B8`, filling it once under the thread-safe static guard dword `02E596D0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E596B8` = `02E58DB0` OR 1, qword `02E596C0` = the return of `006B19A0` OR 1, qword `02E596C8` = 0 | `006C0467`, `006C046C`, `006C0480`, `006C04A9` |
| `006C76D0` | 134 B | returns the address of the 0x18-byte static at `02E5BAD0`, filling it once under the thread-safe static guard dword `02E5BAE8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02E5BAD0` = `02E5AE00` OR 1, qword `02E5BAD8` = the return of `00630490`, qword `02E5BAE0` = 0 | `006C770C`, `006C7707`, `006C7720`, `006C7745` |
| `00724940` | 150 B | when `rdx` is non-null copies its first 0x28 bytes to `02EA1960` (two 16-byte moves to `02EA1960` / `02EA1970` and a qword to `02EA1980`); calls `00724830` with the incoming arguments; then, when `rdx` is non-null and its qword `+0x18` is non-null and differs from qword `[rcx+0x30]`, calls vtable slot `+0x10` of the object at qword `[rcx+0x30]` and nulls that qword when it is non-null, stores the qword `+0x18` of `rdx` at `[rcx+0x30]` and calls that object's vtable slot `+8`; finally calls `00723440(rcx)` and returns its result when negative, else 0 | `0072495D`, `0072497C`, `007249A2`, `007249B4`, `007249BA` |
| `00724DB0` | 138 B | when `rdx` is non-null turns the dword rectangle there (x, y, width, height) into (x, y, x + width, y + height) on the stack and calls vtable slot `+0x168` of the object at qword `[rcx+0x30]` with (that object, 1, the rectangle); when `rdx` is null calls its own vtable slots `+0x80` and then `+0x90` with a stack buffer; returns 0 (stack cookie `01F44830` checked by `00808C40`) | `00724DD7`, `00724DFE`, `00724E0E`, `00724E1F` |
| `007252A0` | 145 B | returns 0x80070057 when `edx` is 0x14 or more; for `edx` 0..0x13 sets dword `[rcx+0xA1C+edx*4]` to -1; for a negative `edx` sets all twenty dwords `+0xA1C` to `+0xA68` to -1 (ten qword stores); returns 0 in both cases | `007252A5`, `007252B2`, `007252C0`, `00725325` |
| `00725830` | 135 B | unpacks the packed colour in `r8d` into four floats scaled by the constant `00D11104` (1/255): byte 2, byte 1, byte 0 and byte 3 in that order, on the stack; then calls the object's vtable slot `+0x1A0` with `rcx`, `rdx`, the address of the four floats, `r9` loaded with the vtable pointer, and its own fifth argument | `00725842`, `00725858`, `0072588F`, `007258AB` |
| `0072F7D0` | 150 B | calls vtable slot `+0` of the object at qword `[rcx+0x22248]` with qword `[rcx+0x28]`; when the result is negative and dwords `01F3BA80` and `01F3BA90` are both at least 1 (unsigned), calls `006DF480(00DA5A88, 0x13E5)` (format "GPUTextureUtil.cpp(%d) : ... PPFX ERROR: ") and then `006DF480(00DA5AD0, result, 0071B3C0(result))`; when it is not negative and dwords `01F3BA80` and `02EA0B40` are both at least 1 (unsigned), calls `006DF480(00D9F030, 0x13E9)` and then `006DF480(00D9F060)`; returns the result | `0072F7E4`, `0072F80A`, `0072F811`, `0072F84D` |
| `00783A10` | 134 B | deleting destructor: stores vtable `00DAC8A8`; when qword `[rcx+8]` is non-null calls `007823E0(qword [rcx+8], qword [rcx+0x10], rcx+8, r9b)` with `r9b` read from the caller's `rdx` home slot (entry `rsp+0x10`, never written by this body) and `00783E90(rcx+8, qword [rcx+8], (qword [rcx+0x18] - qword [rcx+8]) >> 5)` (arithmetic shift), then zeroes the three qwords `+8` / `+0x10` / `+0x18`; when bit `0x1` of `edx` is set calls `00809950(rcx, 0x20)`; returns `rcx` | `00783A29`, `00783A45`, `00783A5D`, `00783A7E` |
| `00785FD0` | 138 B | calls its own vtable slot `+0x20` with the incoming arguments (and its fifth-argument byte) and returns the result when negative; otherwise takes `n` = `00784E60(rcx)` and `b` = `0071A4F0(dword [rcx+0xB0])`, and calls vtable slot `+0x180` of the object at qword `[qword [rcx+0x18] + 0x30]` (the null itself when `+0x18` is null) with qword `[rcx+0x38]`, `n`, 0, the incoming `rdx`, `b` times dword `[rcx+0xB8]` and 0; returns 0 | `00785FEC`, `00785FFC`, `00786009`, `00786042` |
| `007895F0` | 148 B | with state dword `[rcx+0x28]`: below 2 returns 0x8000FFFF; at 5 stores dword `[rcx+0x30]` to `[rdx]` when `rdx` is non-null and returns 0; otherwise calls its own vtable slot `+0x50` with the byte `r8b` until it stops returning 1, returns a negative result as is, else calls vtable slot `+0x28` with 0, stores dword `[rcx+0x30]` to `[rdx]` when `rdx` is non-null and returns 0 | `0078960C`, `00789630`, `0078965A`, `0078966E` |
| `0079C8C0` | 138 B | returns the address of the 0x18-byte static at `02EACEA8`, filling it once under the thread-safe static guard dword `02EACEC0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02EACEA8` = `02EA5660` OR 1, qword `02EACEB0` = the return of `0062FF50` OR 1, qword `02EACEB8` = 0 | `0079C8F7`, `0079C8FC`, `0079C910`, `0079C939` |
| `0079C9D0` | 134 B | returns the address of the 0x18-byte static at `02EACDB8`, filling it once under the thread-safe static guard dword `02EACDD0` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02EACDB8` = `02EA5660` OR 1, qword `02EACDC0` = the return of `00630180`, qword `02EACDC8` = 0 | `0079CA0C`, `0079CA07`, `0079CA20`, `0079CA45` |
| `007A98E0` | 151 B | deleting destructor: stores vtable `01CB4480`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB4470`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007A98F4`, `007A9902`, `007A9919`, `007A993A`, `007A994C` |
| `007AB080` | 151 B | deleting destructor: stores vtable `01CB45A0`; when qword `[rcx+8]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+8` to `+0x20` and dword `+0x2C`; stores the base vtable `01CB4470`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007AB094`, `007AB0A2`, `007AB0B9`, `007AB0DA`, `007AB0EC` |
| `007AE600` | 151 B | deleting destructor: stores vtable `01CB49C8`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB49F8`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007AE614`, `007AE622`, `007AE639`, `007AE65A`, `007AE66C` |
| `007AE6A0` | 151 B | deleting destructor: stores vtable `01CB49D8`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB49F8`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007AE6B4`, `007AE6C2`, `007AE6D9`, `007AE6FA`, `007AE70C` |
| `007B1420` | 151 B | deleting destructor: stores vtable `01CB4AF8`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB4470`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007B1434`, `007B1442`, `007B1459`, `007B147A`, `007B148C` |
| `007B2B30` | 151 B | deleting destructor: stores vtable `01CB4C90`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB4470`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007B2B44`, `007B2B52`, `007B2B69`, `007B2B8A`, `007B2B9C` |
| `007B4D60` | 151 B | deleting destructor: stores vtable `01CB4D38`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB4470`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007B4D74`, `007B4D82`, `007B4D99`, `007B4DBA`, `007B4DCC` |
| `007B54B0` | 151 B | deleting destructor: stores vtable `01CB4DE0`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB4470`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007B54C4`, `007B54D2`, `007B54E9`, `007B550A`, `007B551C` |
| `007B5C50` | 151 B | deleting destructor: stores vtable `01CB4E68`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB4470`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007B5C64`, `007B5C72`, `007B5C89`, `007B5CAA`, `007B5CBC` |
| `007B61C0` | 151 B | deleting destructor: stores vtable `01CB4EA8`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB4470`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007B61D4`, `007B61E2`, `007B61F9`, `007B621A`, `007B622C` |
| `007B7110` | 151 B | deleting destructor: stores vtable `01CB4F70`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB4F90`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007B7124`, `007B7132`, `007B7149`, `007B716A`, `007B717C` |
| `007B7F30` | 151 B | deleting destructor: stores vtable `01CB5080`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB4F90`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007B7F44`, `007B7F52`, `007B7F69`, `007B7F8A`, `007B7F9C` |
| `007BA990` | 151 B | deleting destructor: stores vtable `01CB5790`; when qword `[rcx+8]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+8` to `+0x20` and dword `+0x2C`; stores the base vtable `01CB57A0`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007BA9A4`, `007BA9B2`, `007BA9C9`, `007BA9EA`, `007BA9FC` |
| `007BB8B0` | 151 B | deleting destructor: stores vtable `01CB57E8`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB57A0`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007BB8C4`, `007BB8D2`, `007BB8E9`, `007BB90A`, `007BB91C` |
| `007BBE50` | 151 B | deleting destructor: stores vtable `01CB5818`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB57A0`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007BBE64`, `007BBE72`, `007BBE89`, `007BBEAA`, `007BBEBC` |
| `007C1530` | 151 B | deleting destructor: stores vtable `01CB5E28`; when qword `[rcx+0x10]` is non-null, calls that object's vtable slot `+0` with 3 when the qword just before it is non-zero, else calls `00210EB0` with that pointer - 8; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB4F90`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007C1544`, `007C1552`, `007C1569`, `007C158A`, `007C159C` |
| `007C6C70` | 139 B | returns a float product: starts from 0.0 when qword `[rcx+0x18]` is null, from 1.0 when the byte it points at is below 3, else from the float at its `+0x28`; multiplies by `007BDAC0` of each of the three 0x40-stride records at `rcx+0x150`, then by floats `[rcx+0x5B0]`, `[rcx+0x5B4]` and `[rcx+0x5B8]` | `007C6C95`, `007C6C9A`, `007C6CB8`, `007C6CCB` |
| `007D1430` | 143 B | a float getter keyed by `r8d`, writing to `[rdx]` and returning 0: 0x200 gives `007A9E00(rcx+0x38)`, 0x201 gives 1.0 divided by `007A9E00(rcx+0x68)`, 0x202 gives `007A9E00(rcx+0x98)`, 0x203 gives dword `[rcx+0x18]` converted to float; any other key returns -1 | `007D1446`, `007D145D`, `007D1478`, `007D149C` |
| `007D8180` | 135 B | deleting destructor of a two-vtable object: stores vtables `01CB7698` at `+0` and `01CB76E8` at `+8`, calls `007AD450(qword [rcx+0x48])` (no null test), then stores the base vtables `01CB7058` at `+0x18`, `01CB4658` at `+8` and `01CB4680` at `+0`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x60)` when bit `0x4` is also set; returns `rcx` | `007D8194`, `007D81A8`, `007D81B4`, `007D81CA`, `007D81DC` |
| `007D9690` | 145 B | a float getter keyed by `r8d`: for 0x400 writes to `[rdx]` float `[rcx+0x24]` when float `[rcx+0x2C]` compares equal to 0.0 (ucomiss, also taken when unordered), else `[rcx+0x20]` + `007A9E50(float [rcx+0x28] / float [rcx+0x2C], dword [rcx+0x34])` times (`[rcx+0x24]` - `[rcx+0x20]`), and returns 0; for 0x401 writes dword `[rcx+0x48]` converted to float but returns -1; any other key returns -1 | `007D96AF`, `007D96D1`, `007D96F8`, `007D9709` |
| `007DD510` | 143 B | deleting destructor: stores vtable `01CB80F8`; calls `SetEvent` (import `008C2198`) on qword `[rcx+0x18]` unless it is -1; unless qword `[rcx+0x10]` is -1, calls `ResumeThread` (import `008C2330`) on it until it returns 0 and then `WaitForSingleObject` (import `008C20E0`) on it with timeout -1 (INFINITE); stores the base vtable `01CB49F8`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x48)` when bit `0x4` is also set; returns `rcx` | `007DD533`, `007DD544`, `007DD555`, `007DD562` |
| `007DF9B0` | 147 B | deleting destructor: stores vtable `01CB8290`; calls `007AD450` on each of qwords `[rcx+0x60]` and `[rcx+0x68]` that is non-null (without nulling them); calls `DeleteCriticalSection` (import `008C20D0`) on `rcx+8`; stores the base vtable `01CB8280`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x78)` when bit `0x4` is also set; returns `rcx` | `007DF9CD`, `007DF9E8`, `007DF9FB`, `007DFA08` |
| `007E0070` | 134 B | under the critical section at `rcx+8` (`EnterCriticalSection` / `LeaveCriticalSection` through `008C20B8` / `008C20C0`) sets byte `[rcx+0xC8]` to 1 and copies dword i of the array at qword `[rcx+0xC0]` to dword i at `rdx` for i below `007AECE0()` (re-read every step); returns 0 | `007E0095`, `007E009E`, `007E00C1`, `007E00D8` |
| `007E0880` | 149 B | returns -1 when dword `[rcx+0x80]` has no bit set other than `0x4`; otherwise, for each column i below dword `[rcx+0xAC]` and each row j below `007AECE0()` (re-read every step), copies dword `[rcx+0x10C + 4*(j*cols + i)]` to the same index of the dword array at `rdx`, and returns 0 | `007E088B`, `007E08B3`, `007E08D0`, `007E08D7` |
| `007E25A0` | 149 B | returns -1 when dword `[rcx+0x80]` has no bit set other than `0x4`; otherwise, for each column i below dword `[rcx+0xAC]` and each row j below `007AECE0()` (re-read every step), copies dword `[rdx + 4*(j*cols + i)]` into dword `[rcx+0x10C + 4*(j*cols + i)]`, and returns 0 | `007E25AB`, `007E25D3`, `007E25F0`, `007E25F4` |
| `0083F7B0` | 147 B | returns 0 in `al` when float `+8` of the object at qword `[rcx+0xC8]` equals 0.0 (ucomiss, ordered); otherwise, with `o` = qword `[rdx]`, calls vtable slot `+8` of the object at qword `[rcx+0xC8]` with qword `[o+0xC8]` and, when the returned byte is nonzero, calls `0083E7E0(qword [rcx+0xD8], rcx+0x30, rcx+0x70, o, qword [o+0xD0], o+0x10, qword [rcx+0xC8], float [rcx+0xD0])`; returns 1 in `al` | `0083F7C8`, `0083F7E9`, `0083F7FB`, `0083F831` |
| `0084A220` | 150 B | removes node `rdx` from its list: calls `00841530` on `rcx+0x48` when the node's dword `+0x58` is 2, else on `rcx+8`, with the node's qword `+0x40`; unlinks it (prev qword `+0x48`, next qword `+0x50`; a null prev makes next the head at `rcx+0x88+8*dword [node+0x58]`); calls vtable slot `+0x18` of the object at qword `[rcx+0xA0]` with (node, `r8`), then `0085E710(node)`; sets byte `[rcx+0xDE]` to 1 | `0084A24C`, `0084A266`, `0084A26C`, `0084A294`, `0084A2A9` |
| `0084CA50` | 150 B | constructor: vtable `01CCF218`; dword `+0x10` = 0, float `+0x14` = 1.0 with dword `+0x18` = 0, dword `+0x1C` = 0; qword `+0x20` = its fifth argument, `+0x28` = `r9`, `+0x30` = `rdx`, `+0x38` = `r8`; dwords `+0x40` / `+0x44` = dword `+8` of `rdx` / `r8`; floats `+0x48` / `+0x4C` = what vtable slot `+0x50` of `rdx` / `r8` returns; byte `+0x50` = 0, dword `+0x58` = -1, dword `+0x64` = 1; returns `rcx` | `0084CA75`, `0084CA9D`, `0084CAB0`, `0084CABE`, `0084CACA` |
| `00857E70` | 145 B | for each of the dword `[rcx+0x124]` object pointers in the array at qword `[rcx+0x130]` whose byte `+0xE8` has neither bit `0x1` nor `0x2` set, calls `008537B0(object, xmm1)`, `008531F0(object, xmm1)` and `00853AE0(object, xmm1, object+0x50)` with the incoming float in `xmm1` | `00857EAB`, `00857EBA`, `00857EC5`, `00857ED4` |
| `008581E0` | 140 B | searches the dword `[rcx+0x104]` qwords at qword `[rcx+0x110]` for `rdx`; when found swaps it with the last entry and decrements the count; then calls `00853B20(qword [rdx+0x20], rdx)` and tail-jumps to `00853B20(qword [rdx+0x28], rdx)` | `00858204`, `00858236`, `00858248`, `00858256` |
| `00873AD0` | 134 B | returns the address of the 0x18-byte static at `02EB7AB0`, filling it once under the thread-safe static guard dword `02EB7AC8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02EB7AB0` = `02EB6CF0` OR 1, qword `02EB7AB8` = the return of `00630180`, qword `02EB7AC0` = 0 | `00873B0C`, `00873B07`, `00873B20`, `00873B45` |
| `00873B60` | 134 B | returns the address of the 0x18-byte static at `02EB7A90`, filling it once under the thread-safe static guard dword `02EB7AA8` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `02EB7A90` = `02EB6CF0` OR 1, qword `02EB7A98` = the return of `00630180`, qword `02EB7AA0` = 0 | `00873B9C`, `00873B97`, `00873BB0`, `00873BD5` |
| `0087FCF0` | 144 B | for each of the dword `[rdx+0xC]` object pointers in the array at qword `[rdx+0x18]`: numbers the objects whose byte `+0xE8` has neither bit `0x1` nor `0x2` set into dword `+0xEC` (0, 1, 2 ...), and sets dword `+0xF0` = -1 and float `+0x110` = 1.0 on all; then calls `0087FFD0(rcx+8)` and tail-jumps to `0087FB60(rcx, r8, rdx)` | `0087FD28`, `0087FD31`, `0087FD3C`, `0087FD5E` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-vtable-method-index-ee-1003-3)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-vtable-method-index-ee-1003-3/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `005C1E70` | 171 B | with `rcx` a table of callbacks and `rdx` a state: takes `v` = `00811470(rdx, -1, 0)`, calls `00811130(rdx, -2)` and gets `o` = `005BCD20(rdx)`; returns 0 when `o` is null; otherwise calls the table's slot `+8` with (`o`, `v`) and, when that returns non-null, `00684080(rdx, result, 02CAD440)`, else `0080F420(rdx, 1)` and `00810620(rdx)`; returns 1 | `005C1E8E`, `005C1EA6`, `005C1EB5`, `005C1ECA`, `005C1EE9` |
| `005C1F20` | 171 B | with `rcx` a table of callbacks and `rdx` a state: takes `v` = `00811470(rdx, -1, 0)`, calls `00811130(rdx, -2)` and gets `o` = `005BCD20(rdx)`; returns 0 when `o` is null; otherwise calls the table's slot `+8` with (`o`, `v`) and, when that returns non-null, `00684080(rdx, result, 02CADC50)`, else `0080F420(rdx, 1)` and `00810620(rdx)`; returns 1 | `005C1F3E`, `005C1F56`, `005C1F65`, `005C1F7A`, `005C1F99` |
| `005C2100` | 171 B | with `rcx` a table of callbacks and `rdx` a state: takes `v` = `00811470(rdx, -1, 0)`, calls `00811130(rdx, -2)` and gets `o` = `005BDDC0(rdx)`; returns 0 when `o` is null; otherwise calls the table's slot `+8` with (`o`, `v`) and, when that returns non-null, `00684080(rdx, result, 02CAD840)`, else `0080F420(rdx, 1)` and `00810620(rdx)`; returns 1 | `005C211E`, `005C2136`, `005C2145`, `005C215A`, `005C2179` |
| `005C38B0` | 222 B | copies the singly linked list at qword `02CAFCD8` (next pointer at node `+8`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `005C38D5`, `005C38FC`, `005C391E`, `005C3945`, `005C3960` |
| `005DC0E0` | 166 B | constructor: zeroes word `[rcx]` and dword `[rcx+4]`; calls `00808FE4(rcx+8, 0x18, 8, 005DC1B0, 0016D6A0)`; zeroes qwords `+0xC8` / `+0xD0`, dword `+0xD8` and word `+0xE0`; zeroes the bytes `+0xE8` to `+0xFB` (overlapping qword stores), then sets dword `+0xFC` = 0x400000 and dword `+0x100` = 0x100000; returns `rcx` | `005DC0F1`, `005DC122`, `005DC127`, `005DC15F`, `005DC176` |
| `00603770` | 222 B | copies the singly linked list at qword `02CBF998` (next pointer at node `+8`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `00603795`, `006037BC`, `006037DE`, `00603805`, `00603820` |
| `00627750` | 164 B | resizes a counted block whose dword `[rcx]` holds the count with bit `0x80000000` marking borrowed storage, and whose storage is inline at `rcx+8` for a count of 1, else the pointer qword `[rcx+8]` (none for 0): returns 0 when `edx` equals the whole dword; otherwise takes the new storage `n` = `0061CF20(rcx)` and returns 0xD when `n` is null and `edx` is non-zero; calls `00584730(old storage)` when the old storage differs from `n`, is not the inline slot, is non-null and bit `0x80000000` is clear; stores `n` at qword `[rcx+8]` unless `n` is the inline slot, sets dword `[rcx]` = `edx` and returns 0 | `0062776B`, `0062778D`, `0062779E`, `006277C9`, `006277DB` |
| `0062DBD0` | 222 B | copies the singly linked list at qword `02CF7110` (next pointer at node `+8`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `0062DBF5`, `0062DC1C`, `0062DC3E`, `0062DC65`, `0062DC80` |
| `00637650` | 206 B | returns `01F2E5A0`, filling that static once under the thread-safe static guard dword `02CF950C` (compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; the one-time body runs between `008092FC` and `0080929C` when the guard reads -1): qword `+0` = `00D311B0`, qwords `+8` / `+0x10` / `+0x18` = `01F2E5A8` (the address of the static's own `+8` cell), dword `+0x20` = 0, qword `+0x28` = 0, qword `+0x30` = `00D58BF0` ("PUInt32"), dwords `+0x38` / `+0x3C` = 4, qwords `+0x40` / `+0x48` = 0; calls `00808B90(008AFE50)` | `0063768F`, `006376B1`, `006376D4`, `00637708`, `00637714` |
| `0066FC50` | 171 B | with `rcx` a table of callbacks and `rdx` a state: takes `v` = `00811470(rdx, -1, 0)`, calls `00811130(rdx, -2)` and gets `o` = `0066E7D0(rdx)`; returns 0 when `o` is null; otherwise calls the table's slot `+8` with (`o`, `v`) and, when that returns non-null, `00684080(rdx, result, 02CB6B80)`, else `0080F420(rdx, 1)` and `00810620(rdx)`; returns 1 | `0066FC6E`, `0066FC86`, `0066FC95`, `0066FCAA`, `0066FCC9` |
| `006709D0` | 222 B | copies the singly linked list at qword `02D38DB8` (next pointer at node `+8`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `006709F5`, `00670A1C`, `00670A3E`, `00670A65`, `00670A80` |
| `0068C260` | 189 B | copies a record into `r8` from the one `00699B30(rdx)` returns: byte `+8`, dwords `+0xC` and `+0x10`, qword `+0x18`, dwords `+0x20` to `+0x58`, dword `+0x60`, qword `+0x68`, dwords `+0x70` to `+0x78` and qword `+0x80` (bytes `+0` to `+7`, `+9` to `+0xB` and dwords `+0x5C` / `+0x64` are not copied) | `0068C26C`, `0068C274`, `0068C2A1`, `0068C2EF`, `0068C310` |
| `0068CBE0` | 189 B | copies a record into `r8` from the one `006998F0(rdx)` returns: byte `+8`, dwords `+0xC` and `+0x10`, qword `+0x18`, dwords `+0x20` to `+0x58`, dword `+0x60`, qword `+0x68`, dwords `+0x70` to `+0x78` and qword `+0x80` (bytes `+0` to `+7`, `+9` to `+0xB` and dwords `+0x5C` / `+0x64` are not copied) | `0068CBEC`, `0068CBF4`, `0068CC21`, `0068CC6F`, `0068CC90` |
| `0068D370` | 189 B | copies a record into `r8` from the one `00699290(rdx)` returns: byte `+8`, dwords `+0xC` and `+0x10`, qword `+0x18`, dwords `+0x20` to `+0x58`, dword `+0x60`, qword `+0x68`, dwords `+0x70` to `+0x78` and qword `+0x80` (bytes `+0` to `+7`, `+9` to `+0xB` and dwords `+0x5C` / `+0x64` are not copied) | `0068D37C`, `0068D384`, `0068D3B1`, `0068D3FF`, `0068D420` |
| `0068DD80` | 189 B | copies a record into `r8` from the one `00699050(rdx)` returns: byte `+8`, dwords `+0xC` and `+0x10`, qword `+0x18`, dwords `+0x20` to `+0x58`, dword `+0x60`, qword `+0x68`, dwords `+0x70` to `+0x78` and qword `+0x80` (bytes `+0` to `+7`, `+9` to `+0xB` and dwords `+0x5C` / `+0x64` are not copied) | `0068DD8C`, `0068DD94`, `0068DDC1`, `0068DE0F`, `0068DE30` |
| `0068E940` | 189 B | copies a record into `r8` from the one `00698E10(rdx)` returns: byte `+8`, dwords `+0xC` and `+0x10`, qword `+0x18`, dwords `+0x20` to `+0x58`, dword `+0x60`, qword `+0x68`, dwords `+0x70` to `+0x78` and qword `+0x80` (bytes `+0` to `+7`, `+9` to `+0xB` and dwords `+0x5C` / `+0x64` are not copied) | `0068E94C`, `0068E954`, `0068E981`, `0068E9CF`, `0068E9F0` |
| `00722060` | 163 B | for each of the two qwords at `rcx+0xF0` and `rcx+0xF8` that is non-null: when its object's qword `+8` is non-null calls `006DA8A0(qword [01F3BA68], that - 8)` and zeroes it, then calls `006DA8A0(qword [01F3BA68], object)` and zeroes the slot; then calls `00720220(rcx)` and `00727450(rcx)` and returns the latter's result when negative, else 0 | `007220A2`, `007220B2`, `007220C1`, `007220D6`, `007220DE` |
| `00724C10` | 186 B | returns 0x80070057 when `rdx` is null; otherwise converts the four dwords at `rdx` (zero-extended) to floats and appends floats `[rdx+0x10]` and `[rdx+0x14]`, and calls vtable slot `+0x160` of the object at qword `[rcx+0x30]` with (that object, 1, the six floats on the stack); returns 0 (stack cookie `01F44830` checked by `00808C40`) | `00724C55`, `00724C90`, `00724C9F`, `00724CB0` |
| `00724CD0` | 206 B | returns 0x80070057 when `rdx` is null; otherwise calls vtable slot `+0x2F8` of the object at qword `[rcx+0x30]` with (that object, a stack dword 1, a six-float stack buffer), then writes to `rdx` the first four floats rounded by adding `00D99774` (0.49999) and truncating as dwords `+0`..`+0xC`, and the last two floats unchanged to `+0x10` / `+0x14`; returns 0 (stack cookie `01F44830` checked by `00808C40`) | `00724D1E`, `00724D38`, `00724D4B`, `00724D81` |
| `00725760` | 196 B | copies the 16 bytes at `r8` (zero when `r8` is null) to a stack slot; with `d` = qword `[rcx+0x30]` and `t` = qword `[rcx+0x8F0]`: when bit `0x10000000` of `edx` is set calls `d`'s vtable slot `+0x190` with (each non-null qword of the dword `[t+0x128]` entries at `t+0x130`, the address of that stack copy); when `edx` AND 3 is non-zero and qword `[t+0x170]` is non-null calls `d`'s slot `+0x1A8` with (that qword, `edx` AND 3, the float in `xmm3`, its fifth-argument byte); returns 0 | `00725797`, `007257B0`, `007257C8`, `007257E2`, `00725806` |
| `007258C0` | 158 B | calls vtable slot `+0x88` of the object at qword `[rcx+0x30]` with 0, calls `00861EC0(a 0x80-byte stack buffer, 0, 0x80)` and `00861EC0(a 0x100-byte stack buffer, 0, 0x100)`, then calls vtable slot `+0x90` of the object at qword `[rcx+0x30]` (re-read) with (0, 0x20, the 0x100-byte buffer, the 0x80-byte buffer twice); returns 0 (stack cookie `01F44830` checked by `00808C40`) | `007258E7`, `007258FA`, `0072590F`, `0072593D` |
| `007259D0` | 199 B | with `ib` = qword `[rcx+0x9B8]`: when it is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9DC90, 0x1FD6)` and `006DF480(00D9D768 "IGPUDevice::DrawIndices(): Index buffer is not set yet.")`; a null `ib` returns 0x8000FFFF either way; otherwise, on the object `d` at qword `[rcx+0x30]`, calls slot `+0x98` with (qword `[qword [ib+0xB8] + 8*dword [ib+0xC0]]`, dword `[ib+0xE8]`, dword `[rcx+0x9C0]`), slot `+0xC0` with `edx`, and slot `+0x60` with (`r8d`, `r9d`, 0); returns 0 | `00725A1E`, `00725A51`, `00725A58`, `00725A68`, `00725A7D` |
| `00726C30` | 194 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9C638, 0x2345)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9C6D8)`; stores `00788DB0(rcx, rdx, r8d, r9, the fifth-argument dword)` to the qword the sixth argument points at; when that result is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9CA70, 0x234F)` and `006DF480(00D9CAC0)`; a null result returns 0x80004005, else returns 0 | `00726C6E`, `00726C93`, `00726C9D`, `00726CC3`, `00726CD4` |
| `00726D00` | 155 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9C208, 0x22D6)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9C238)`; stores `007896A0(rcx)` to `[rdx]`; when that result is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9C3B0, 0x22E3)` and `006DF480(00D9C430)`; a null result returns 0x80004005, else returns 0 | `00726D2E`, `00726D42`, `00726D47`, `00726D6D` |
| `00726E30` | 187 B | returns 0 unless `edx` is 3 to 6; calls vtable slot `+0xE8` of the object at qword `[rcx+0x40]` with (`r8d`, the address of a stack dword `s`) and returns 0 when that result is negative; otherwise returns flags built from `s`: `s` AND 0x4000 gives 0x1, 0x10000 gives 0x2, 0x20 gives 0x10000000 and 0x20000, 0x80 gives 0x20000000, 0x40 gives 0x40000000, 0x8000 gives 0x80000; `r8d` equal to 0x1D, 0x48, 0x4B, 0x4E, 0x5B, 0x5D or 0x63 adds 0x50000, and a true `0071A600(r8d)` adds 0x40000 | `00726E57`, `00726E73`, `00726EBF`, `00726ED1` |
| `00781B70` | 194 B | for qword `[rcx+0x50]` and then qword `[rcx+0x48]`: when non-null decrements the object's dword `+8` and, when it reaches 0, calls its vtable slot `+0x20` with 0 and `006DA8A0(qword [01F3BA68], object)`; zeroes the slot either way; then zeroes qwords `+0x38` / `+0x40` / `+0x48` / `+0x50`, dwords `+0x58` / `+0x60` and byte `+0x5C`, calls `00727450(rcx)` and returns its result when negative, else 0 | `00781B93`, `00781BA9`, `00781BB2`, `00781C07`, `00781C10` |
| `00785EE0` | 182 B | sets dword `[rcx+0x14]` = 1; calls `00784C50(rcx+0x40)` and `0078A970(rcx+0xB0, rcx+0x40)`; sets dword `+0x28` = 0 and dword `+0x24` = 1 when bit `0x20` of byte `[rcx+0x58]` is set plus 2 when bit `0x40` is; calls `0078AB60(rcx)`, zeroes qwords `+0x110` / `+0x118` / `+0x120`, and calls vtable slot `+0x38` of `rdx` with `rcx+0x38`; returns 0 | `00785EFC`, `00785F06`, `00785F16`, `00785F49`, `00785F7C` |
| `00786D00` | 191 B | takes `n` from its own vtable slot `+0x50` and returns 0x8000FFFF when it is 0; otherwise calls `006DA880(qword [01F3BA68], n*8+8, 00DAD4A0 "GPUInterfaceTexture.cpp" after a path prefix, 0x6E1, 0)`; a non-null result gets `n` in its first qword and the address after it is stored at qword `[rcx+0xF0]` (a null result stores 0 there, and the loop that follows does not test it); then stores `007858A0(qword [rcx+0x18], rcx, i, 0)` into pointer entry i of that array for each i below `n`; returns 0 | `00786D10`, `00786D56`, `00786D64`, `00786D8D`, `00786D9F` |
| `00789C00` | 157 B | calls `007157A0(a stack string, rdx)`, then reads that string's length dword `+0` and data qword `+8`; for k from 1 to length - 1 copies byte `[rdx + length - k]` into data byte k (data byte 0 is not written by this body); calls vtable slot `+0x20` of the object at qword `[rcx+0xE0]` with the data pointer; calls `00715C70(the stack string)` and returns the slot call's result | `00789C1F`, `00789C46`, `00789C5E`, `00789C81`, `00789C8B` |
| `0078F9F0` | 197 B | when byte `[rcx+0x99]` is set returns `0078DE00(rcx, rdx, 1)` + 1; otherwise walks the qword vector `[rcx+0xD0]` to `[rcx+0xD8]` and returns i + 1 for the first entry `e` with `007187E0(e+8, rdx)` or `007187E0(e+0x38, rdx)` non-zero, or 0 when none matches | `0078FA0D`, `0078FA33`, `0078FA62`, `0078FA7D`, `0078FAB0` |
| `007A9820` | 192 B | vector deleting destructor of 0x30-byte elements: when bit `0x2` of `edx` is set, walks the qword count at `rcx-8` back from the end storing the base vtable `01CB4470` into each element, then, when bit `0x1` is set, calls `007AD450(rcx-8)` or, when bit `0x4` is also set, `0016D6A0(rcx-8, count*0x30+8)`, and returns `rcx-8`; otherwise stores the base vtable `01CB4470` at `[rcx]`, when bit `0x1` is set calls `007AD450(rcx)` or, when bit `0x4` is also set, `0016D6A0(rcx, 0x30)`, and returns `rcx` | `007A982E`, `007A9850`, `007A986C`, `007A9894`, `007A98AF` |
| `007AB120` | 189 B | vector deleting destructor of 0x18-byte elements: when bit `0x2` of `edx` is set, walks the qword count at `rcx-8` back from the end storing the base vtable `01CB4470` into each element, then, when bit `0x1` is set, calls `007AD450(rcx-8)` or, when bit `0x4` is also set, `0016D6A0(rcx-8, count*0x18+8)`, and returns `rcx-8`; otherwise stores the base vtable `01CB4470` at `[rcx]`, when bit `0x1` is set calls `007AD450(rcx)` or, when bit `0x4` is also set, `0016D6A0(rcx, 0x18)`, and returns `rcx` | `007AB12E`, `007AB150`, `007AB16C`, `007AB194`, `007AB1AF` |
| `007AE740` | 161 B | deleting destructor: stores vtable `01CB49E8`; walks the list from qword `[rcx+0x10]` (next pointer at node `+0x10`, read before the call) calling each node's vtable slot `+0` with 1; zeroes qwords `+0x10` / `+0x18` and dword `+8`; stores the base vtable `01CB49F8`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x20)` when bit `0x4` is also set; returns `rcx` | `007AE75A`, `007AE778`, `007AE77F`, `007AE79A`, `007AE7AC` |
| `007BAA30` | 189 B | vector deleting destructor of 0x18-byte elements: when bit `0x2` of `edx` is set, walks the qword count at `rcx-8` back from the end storing the base vtable `01CB57A0` into each element, then, when bit `0x1` is set, calls `007AD450(rcx-8)` or, when bit `0x4` is also set, `0016D6A0(rcx-8, count*0x18+8)`, and returns `rcx-8`; otherwise stores the base vtable `01CB57A0` at `[rcx]`, when bit `0x1` is set calls `007AD450(rcx)` or, when bit `0x4` is also set, `0016D6A0(rcx, 0x18)`, and returns `rcx` | `007BAA3E`, `007BAA60`, `007BAA7C`, `007BAAA4`, `007BAABF` |
| `007C1290` | 192 B | vector deleting destructor of 0x30-byte elements: when bit `0x2` of `edx` is set, walks the qword count at `rcx-8` back from the end storing the base vtable `01CB4F90` into each element, then, when bit `0x1` is set, calls `007AD450(rcx-8)` or, when bit `0x4` is also set, `0016D6A0(rcx-8, count*0x30+8)`, and returns `rcx-8`; otherwise stores the base vtable `01CB4F90` at `[rcx]`, when bit `0x1` is set calls `007AD450(rcx)` or, when bit `0x4` is also set, `0016D6A0(rcx, 0x30)`, and returns `rcx` | `007C129E`, `007C12C0`, `007C12DC`, `007C1304`, `007C131F` |
| `007CA370` | 170 B | unless qword `[rcx+0x18]` points at a record whose byte `+0` is 3 or more and whose byte `+0xA` has bit `0x8` set, calls `007CA560` on the records at `rcx+0x520`, `rcx+0x550` and `rcx+0x580` with the floats in `xmm1`, `xmm2` and `xmm3` respectively, each with its fifth-argument float as the second float, `r9` = 0 and a stack byte 0; returns 0 | `007CA39B`, `007CA3C1`, `007CA3E2`, `007CA402` |
| `007D1970` | 159 B | returns -1 when `rdx` is null; otherwise calls its own vtable slot `+0x10` four times with the float in `xmm3`: key 0x203 with dword `[rdx]` converted to float, then 0x200, 0x201 and 0x202 with floats `[rdx+4]`, `[rdx+8]` and `[rdx+0xC]`; then calls its slot `+0x40` and returns 0 | `007D19AC`, `007D19AF`, `007D19C5`, `007D19DB`, `007D19FA` |
| `007D98F0` | 168 B | evaluates the ramp at `rcx+0x20` (float `+0x24` when float `+0x2C` is 0.0 or NaN, else `+0x20` + `007A9E50(+0x28 / +0x2C, dword +0x34)` times (`+0x24` - `+0x20`)), multiplies it by float `01CEBC78` (2 pi) and by the writable float `01F41D20` (2.083333e-05 in the image file; it lives in .data and is stored to elsewhere at run time), and by mode dword `[rcx+0x48]`: 0 stores floats `+0x50` = 0 and `+0x54` = 1.0; 1 stores `e` = `expf` (`00861FAA`) of the negated value and 2 of the value minus `01CEBC50` (pi), as `+0x50` = `e` and `+0x54` = 1.0 - `e`; other modes store nothing | `007D9919`, `007D9931`, `007D995C`, `007D9963`, `007D9974` |
| `007D9B70` | 162 B | a float getter keyed by `r8d`, writing to `[rdx]` and returning 0: keys 0x500 to 0x504 give `007A9E00` of the records at `rcx+0x18`, `+0x48`, `+0x78`, `+0xA8` and `+0xD8`; any other key returns -1 | `007D9B86`, `007D9BAA`, `007D9BC2`, `007D9C01` |
| `007D9DF0` | 163 B | a float setter keyed by `edx`: keys 0x501 to 0x504 pick the records at `rcx+0x48`, `+0x78`, `+0xA8` and `+0xD8` with the value in `xmm2`; key 0x500 picks `rcx+0x18` with the value times `007AED00()` converted to float times `008C5B2C` (0.001); it calls `007CA560(record, value, the float in xmm3, 0, a stack byte 0)` and, when that float is 0.0 or NaN, its own vtable slot `+0x40`; other keys do nothing | `007D9E1E`, `007D9E43`, `007D9E53`, `007D9E6D`, `007D9E80` |
| `007DA1C0` | 221 B | a float getter keyed by `r8d`, writing to `[rdx]` and returning 0: 0x600 evaluates the ramp at `rcx+0x20` (end `+0x24` when duration float `+0x2C` is 0.0 or NaN, else start `+0x20` + `007A9E50(elapsed +0x28 / duration, curve dword +0x34)` times (end - start)) and 0x601 the same ramp at `rcx+0x50` (end `+0x54`, elapsed `+0x58`, duration `+0x5C`, curve `+0x64`); any other key returns -1 | `007DA1DD`, `007DA218`, `007DA21C`, `007DA270`, `007DA293` |
| `007DAA00` | 163 B | stores two evaluated ramps: float `[rcx+0x78]` = the ramp at `rcx+0x20` (end `+0x24` when duration float `+0x2C` is 0.0 or NaN, else start `+0x20` + `007A9E50(elapsed +0x28 / duration, curve dword +0x34)` times (end - start)), and float `[rcx+0x7C]` = the same ramp at `rcx+0x50` (end `+0x54`, elapsed `+0x58`, duration `+0x5C`, curve `+0x64`) divided by `007AED00()` converted to float | `007DAA2E`, `007DAA46`, `007DAA68`, `007DAA83`, `007DAA93` |
| `007DC8B0` | 192 B | vector deleting destructor of 0x30-byte elements: when bit `0x2` of `edx` is set, walks the qword count at `rcx-8` back from the end storing the base vtable `01CB7B00` into each element, then, when bit `0x1` is set, calls `007AD450(rcx-8)` or, when bit `0x4` is also set, `0016D6A0(rcx-8, count*0x30+8)`, and returns `rcx-8`; otherwise stores the base vtable `01CB7B00` at `[rcx]`, when bit `0x1` is set calls `007AD450(rcx)` or, when bit `0x4` is also set, `0016D6A0(rcx, 0x30)`, and returns `rcx` | `007DC8BE`, `007DC8E0`, `007DC8FC`, `007DC924`, `007DC93F` |
| `007DC970` | 151 B | deleting destructor: stores vtable `01CB7B10`; when qword `p` = `[rcx+0x10]` is non-null, calls vtable slot `+0` of `p` with 3 when qword `[p-8]` is non-zero, else calls `00210EB0(p - 8)`; zeroes qwords `+0x10` to `+0x28` and dword `+0xC`; stores the base vtable `01CB7B00`; when bit `0x1` of `edx` is set calls `007AD450(rcx)`, or `0016D6A0(rcx, 0x30)` when bit `0x4` is also set; returns `rcx` | `007DC984`, `007DC992`, `007DC9A9`, `007DC9CA`, `007DC9DC` |
| `007DEEF0` | 167 B | when `edx` and `r8d` are both 0: calls `0019C5D0(a 0x100-byte stack buffer, 0x100, 01CB7F10 "[sead][info]onDefaultDeviceChanged")`, stores a newline at the returned length (2 less when that is 0xFF or more) and a terminator after it (an index of 0x100 or more calls `00809728`), calls `OutputDebugStringA` (`008C2120`) and `007A5570(0, buffer)`, then calls vtable slot `+0` of the object at qword `[rcx-8]` when that is non-null; returns 0 (stack cookie `01F44830` checked by `00808C40`) | `007DEF28`, `007DEF3C`, `007DEF57`, `007DEF64`, `007DEF75` |
| `007E8890` | 200 B | copies qwords `[rdx]`, `[rdx+8]` and `[rdx+0x18]` to `[rcx+8]`, `[rcx+0x10]` and `[rcx+0x20]`; when the last is null calls `0019C5D0(a 0x100-byte stack buffer, 0x100, 01CB9090 "[sead][!!error!!]track data invalid")`, stores a newline at the returned length (2 less when that is 0xFF or more) and a terminator after it (an index of 0x100 or more calls `00809728`), calls `OutputDebugStringA` (`008C2120`) and `007A5570(2, buffer)`, sets dword `[rcx+0x1E8]` = 5 and returns -1; otherwise sets dword `[rcx+0x1E8]` = 1 and returns 0 | `007E88B1`, `007E88DB`, `007E890A`, `007E8922`, `007E892E` |
| `007F1220` | 210 B | calls `007F0210(rcx, a stack copy of qword [rdx], r8, r9, its fifth argument)` and returns a negative result as is; otherwise, with `r8` a descriptor, by dword `[r8+0x18]`: 0 sets dword `[rcx+0xE4]` = 0 and dword `[rcx+0x140]` = 1; 1 copies dwords `+0x1C` / `+0x20` / `+0x24` to `+0xE4` / `+0xE8` / `+0x130`, byte `+0x34` to `+0xE1`, dwords `+0x28` / `+0x2C` / `+0x30` to `+0x110` / `+0x114` / `+0x118`, dwords `+0x38` / `+0x3C` to `+0x134` / `+0x144`, byte `+0x40` to `+0x148`, and sets dword `+0x140` = 2; returns the result | `007F1247`, `007F125D`, `007F1282`, `007F12D5`, `007F12DB` |
| `007F1EC0` | 188 B | calls `007F0210(rcx, a stack copy of qword [rdx], r8, r9, its fifth argument)` and returns a negative result as is; otherwise copies the descriptor's dwords `[r8+0x18]` / `+0x1C` / `+0x20` to `[rcx+0x100]` / `+0x104` / `+0x108` and scales that xyz vector in place by 0.5 r (3 - s r r), where s is its squared length under the lane mask `00D11570` (1, 1, 1, 0) and r = rsqrtps(s), with the constants `00D560A0` (3.0) and `00D22600` (0.5), keeping float `+0x10C`; returns the result | `007F1EE7`, `007F1EF5`, `007F1F2B`, `007F1F4B`, `007F1F69` |
| `007F24F0` | 219 B | calls `007F0210(rcx, a stack copy of qword [rdx], r8, r9, its fifth argument)` and returns a negative result as is; otherwise copies from the descriptor `r8`: dwords `+0x18` / `+0x1C` / `+0x20` to `[rcx+0xE4]` / `+0xE8` / `+0x100`, byte `+0x24` to `+0x104`, the count dword `+0x28` to `+0x108`, byte `+0xEC` to `+0xE1`, dword `+0xF0` to `+0x210`, byte `+0xF4` to `+0x214`; then for each of the count entries copies three dwords from `r8+0x2C+12*i` to `rcx+0x110+16*i` and sets the fourth float to 1.0; returns the result | `007F2517`, `007F252D`, `007F2552`, `007F2597`, `007F25AD` |
| `00832DD0` | 182 B | increments dword `[rcx+0x68]`; walks the dword `[rcx+0x1C]` inline 0x60-byte entries at qword `[rcx+0x28]` from the last to the first and, for each whose qword `+0x40` equals `rdx`: increments `+0x68` again, calls `00841530(qword [rcx+0x60], entry qword +0x50)` when qword `+0x60` is non-null, calls `008332A0(rcx+0x18, i, count - 1)`, then, when qword `+0x60` is non-null, stores `i` to dword `+0x28` of the object at qword `+0x50` of the entry now at `i`, and decrements the count; finally tail-calls its own vtable slot `+0x78` | `00832DE0`, `00832E14`, `00832E2C`, `00832E3E`, `00832E53` |
| `00833A60` | 187 B | with `n` = dword `[rcx+0x84]` and the 16-byte points at qword `[rcx+0x90]`: writes to `[r8]` point `edx` mod `n` and to `[r9]` point (`edx` + 1) mod `n` (mod being the signed idiv remainder), each as (x times float `[rcx+0x20]`, y times float `[rcx+0x24]`, z times float `[rcx+0x28]`, 0) | `00833A7B`, `00833A94`, `00833AB7`, `00833AC4`, `00833B11` |
| `00834C70` | 208 B | with axis `a` = dword `[rcx+0x50]` and `b` = (`a` + 2) mod 3, builds the half-extents (f, f, f) from f = float `[rcx+0x30+4*b]` and adds float `[rcx+0x30+4*a]` to component `a`; squares each component as (2 (c + `008FCC84` 0.04))^2 and writes to `[r8]` (c1 + c2) k, (c0 + c2) k and (c0 + c1) k with k = the float in `xmm1` times `01CCD6F8` (1/12) | `00834C94`, `00834CA7`, `00834CCE`, `00834CE6`, `00834D2A` |
| `00837E20` | 216 B | calls its own vtable slot `+0x50` three times (results a, b, c in call order) and writes two 16-byte vectors: to `[r8]` (float `[rdx+0x30]` - c, `[rdx+0x34]` - b, `[rdx+0x38]` - a, 0) and to `[r9]` the same with the three results added | `00837E4D`, `00837E59`, `00837E65`, `00837EA7`, `00837EE8` |
| `00842040` | 173 B | for each of the three 16-byte points at `rdx`, `rdx+0x10` and `rdx+0x20` takes the dot product of its xyz with floats `[rcx+0x70]` / `+0x74` / `+0x78` and, when that is greater than float `[rcx+0x60]`, stores it there and copies the point to `[rcx+0x10]` | `00842065`, `0084206B`, `0084209E`, `008420D8`, `008420E7` |
| `00847C00` | 169 B | dots the direction xyz at `r8` with the three rows at `rcx+0x50`, `rcx+0x60` and `rcx+0x70` (floats `+0`/`+4`/`+8` of each) and copies the 16-byte row with the largest result (the first on ties) to `[rdx]`; returns `rdx` | `00847C1D`, `00847C72`, `00847C8A`, `00847C99`, `00847CA0` |
| `00848270` | 200 B | increments dword `02EAF398`; orders the two objects so that `rdx` has the smaller dword `+0x18`, hashes (larger id << 16) OR smaller id with a shift/xor/add integer hash, masks it with dword `[rcx+0x10]` - 1, and when the bucket is below dword `[rcx+0x3C]` walks its chain (heads in the dword array at qword `[rcx+0x48]`, next links in the dword array at qword `[rcx+0x68]`, -1 ending it) over the 0x20-byte pair records at qword `[rcx+0x18]`; returns the record whose first object pointer (qword `+0`) has dword `+0x18` equal to the smaller id and whose second (qword `+8`) has the larger, or 0 | `00848275`, `008482A1`, `008482D1`, `008482FE`, `00848312` |
| `0084A5D0` | 216 B | calls `008497D0` twice, first on the structure at `rcx+8` with its root qword `[rcx+8]` and then on `rcx+0x48` with qword `[rcx+0x48]`, each time passing `rdx`, `r8`, `r9+0x10`, `r9+0x20`, float `[r9+0x2C]`, its own fifth and sixth arguments and the address of the saved `r9` | `0084A5EC`, `0084A642`, `0084A645`, `0084A658`, `0084A685` |
| `00855A50` | 212 B | calls vtable slot `+8` of the object at qword `[rcx+0xF8]` with (`rcx`, qword `[rcx+0x28]`); for each of the dword `[rcx+0x104]` pointers in the pointer array at qword `[rcx+0x110]`, takes the record's two objects (qwords `+0x20` / `+0x28`) and, when both are non-null, neither has bit `0x1` or `0x2` of byte `+0xE8` set, and they do not both have dword `+0xF4` equal to 2 or 5, calls `00858B50(qword [rcx+0xF8] + 8, first dword +0xEC, second dword +0xEC)`; then tail-calls that object's slot `+0x10` with `rcx` | `00855A73`, `00855AA8`, `00855ABF`, `00855AF7`, `00855B20` |
| `00857C10` | 187 B | a step of the float `xmm1`: calls the function at qword `[rcx+0x98]` when non-null; its own vtable slot `+0x100` with the step; stores the step at float `+0x30` and 0 at dword `+0x34`; stores slot `+0x18`'s result at qword `+0x48`; calls slots `+0x48` and `+0x110`; stores the step at float `+0xB4` and calls slot `+0x118` with `rcx+0xA8`, slot `+0x108` with the step, `00858C10` and `00858C80` with the step, and the function at qword `[rcx+0x90]` with the step when non-null | `00857C2D`, `00857C38`, `00857C53`, `00857C81`, `00857CBE` |
| `00858A00` | 177 B | when byte `[rcx+0x156]` is non-zero calls `00858AC0(rcx, object)` for each of the dword `[rcx+0xC]` pointers in the pointer array at qword `[rcx+0x18]` whose object's byte `+0x104` has bit `0x2` set; otherwise calls `00858AC0(rcx, object)` for each of the dword `[rcx+0x124]` pointers in the pointer array at qword `[rcx+0x130]` whose object's dword `+0xF4` is neither 2 nor 5 | `00858A14`, `00858A38`, `00858A44`, `00858A7B`, `00858A8E` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-vtable-method-index-ee-1003-4)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-vtable-method-index-ee-1003-4/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `006C0060` | 222 B | copies the singly linked list at qword `02E58CA0` (next pointer at node `+0x10`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `006C0085`, `006C00AC`, `006C00CE`, `006C00F5`, `006C0110` |
| `006C24C0` | 222 B | copies the singly linked list at qword `02E59BB8` (next pointer at node `+0x10`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `006C24E5`, `006C250C`, `006C252E`, `006C2555`, `006C2570` |
| `006CD5B0` | 222 B | copies the singly linked list at qword `02E5C210` (next pointer at node `+8`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `006CD5D5`, `006CD5FC`, `006CD61E`, `006CD645`, `006CD660` |
| `006D6FF0` | 222 B | copies the singly linked list at qword `02E9FD60` (next pointer at node `+8`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `006D7015`, `006D703C`, `006D705E`, `006D7085`, `006D70A0` |
| `006D9780` | 222 B | copies the singly linked list at qword `02EA06D8` (next pointer at node `+0x10`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `006D97A5`, `006D97CC`, `006D97EE`, `006D9815`, `006D9830` |
| `006D9B70` | 222 B | copies the singly linked list at qword `02EA0748` (next pointer at node `+0x10`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `006D9B95`, `006D9BBC`, `006D9BDE`, `006D9C05`, `006D9C20` |
| `00719460` | 235 B | with `r8` a byte string: when `r8` is null or the low 32 bits of its length up to the first 0 byte are 0, calls `00715A00(rdx, rcx)`; otherwise calls `007158B0(a stack temporary, qword [rcx+8], dword [rcx] + length, -1)`, calls `memcpy` (import thunk `00861EBA`) with (the temporary's data qword `+8` plus dword `[rcx]`, `r8`, length), calls `00715A00(rdx, the temporary)`, then calls `006DA8A0(qword [01F3BA68], data - 8)` with the temporary's data qword unless it equals `02EA1720` or is null; returns `rdx` | `007194B3`, `007194DF`, `007194F6`, `00719503`, `0071952C` |
| `007214A0` | 271 B | returns 1 when bit `0x80000000` of dword `[rcx+0x38]` is set; otherwise calls `007273E0(rcx)` and returns a negative result; when `rdx` is non-null and qword `[rcx+0x28]` changed across that call, increments dword `02EA1914`, first (when it was 0) storing `rdx` at `02EA1918` and zeroing the four qwords at `01F3CB18` and the nine at `02EA18C0`; then returns 0 when qword `+0x28` is null, dword `+0x44` is 0, or both qwords `+0xA8` and `+0xB8` are non-null, else the result of `00720320(rcx)` when negative, or 0 | `007214AF`, `007214D7`, `00721500`, `00721564`, `0072158E` |
| `007255E0` | 269 B | sets state `r8d` (0..0xF) on slot `edx` (0..0x13), returning 0x80070057 for either out of range: with byte `01F3CBA9` clear the cached dword `[rcx+0xA1C+4*slot]` is reset to -1, and with it set and `r9b` set an equal cache returns 1 at once; otherwise, when the cache is -1 or differs from the state in bits `0x3` or `0xC`, calls on the object at qword `[rcx+0x30]` slot `+0x50` (slots 0..0xF) or `+0xD0` (slots 0x10..0x13, minus 0x10) with (slot, 1, `rcx+0x460+8*state`); stores the state in the cache when byte `01F3CBA9` is set; returns 0 | `007255FE`, `00725624`, `00725650`, `007256A9`, `007256C0` |
| `0075CAD0` | 312 B | calls vtable slot `+8` of each non-null pointer in the dword `[rcx+0x3C]` pointer array at qword `[rcx+0x48]`, and of every pointer (no null test) in the dword `[rcx+0x40]` pointer array at qword `[rcx+0x50]`; for i = 0 and 1 calls slot `+8` of qwords `[rcx+0x60+8i]` and `[rcx+0x80+8i]` when non-null and nulls them; then for i = 0 and 1, when qword `o` = `[rcx+0x90+8i]` is non-null, decrements dword `[o+8]` and, when that reaches 0, calls `o`'s vtable slot `+0x20` with 0 and `006DA8A0(qword [01F3BA68], o)`, and nulls the qword, and calls slot `+8` of qword `[rcx+0x70+8i]` when non-null and nulls it; zeroes dwords `+0x5C` and `+0xA4`; tail-jumps to `00727410(rcx)` | `0075CB10`, `0075CB3B`, `0075CB6C`, `0075CB9B`, `0075CBB9` |
| `0075CC50` | 299 B | for each i below dword `[rcx+0x3C]`: when entry i `o` of the pointer array at qword `[rcx+0x48]` is non-null, decrements dword `[o+8]` and, when that reaches 0, calls `o`'s vtable slot `+0x20` with 0 and `006DA8A0(qword [01F3BA68], o)`, then nulls the entry; does the same for entry i of the pointer array at qword `[rcx+0x50]` when that array is non-null; then, for each of the two array qwords that is non-null, calls `006DA8A0(qword [01F3BA68], array - 8)` and nulls it; zeroes qwords `+0xA0`, `+0x3C` and `+0x58`; returns the result of `00727450(rcx)` when negative, else 0 | `0075CC8D`, `0075CCA3`, `0075CCCB`, `0075CD30`, `0075CD68` |
| `0075E690` | 298 B | returns 0 when `edx` is 0 or `r8` is null; otherwise walks the circular list whose sentinel is qword `[rcx+0x38]` (next `+0`, prev `+8`, payload qword `+0x10`); for a node with payload `p` and `o` = qword `[p+8]`, each of the `edx` qwords at `r8` that is non-null and equals `o` decrements dword `[o+8]`, and when that reaches 0: calls `o`'s vtable slot `+0x20` with 0 and `006DA8A0(qword [01F3BA68], o)`, nulls qword `[p+8]`, calls `006DA8A0(qword [01F3BA68], p)` when the node's payload qword is non-null and nulls it, unlinks the node, decrements qword `[rcx+0x40]`, calls `00210EB0(node)` and goes on with the next node; returns the number of nodes removed | `0075E6FC`, `0075E701`, `0075E755`, `0075E79D`, `0075E7A1` |
| `0075E7C0` | 260 B | walks the circular list whose sentinel is qword `[rcx+0x38]` (next `+0`, prev `+8`, payload qword `+0x10`); for a node with payload `p` whose qword `[p+8]` equals `rdx` (never when `rdx` is null) decrements dword `[rdx+8]`, and when that reaches 0: calls `rdx`'s vtable slot `+0x20` with 0 and `006DA8A0(qword [01F3BA68], rdx)`, nulls qword `[p+8]`, calls `006DA8A0(qword [01F3BA68], p)` when the node's payload qword is non-null and nulls it, unlinks the node, decrements qword `[rcx+0x40]`, calls `00210EB0(node)` and goes on with the next node; returns the number of nodes removed | `0075E81E`, `0075E823`, `0075E86D`, `0075E8B3`, `0075E8B7` |
| `0075EC00` | 283 B | walks the circular list whose sentinel is qword `[rcx+0x38]` (next `+0`, payload qword `+0x10`); for each node with payload `p` and `o` = qword `[p+8]` (no null test): decrements dword `[o+8]` and, when that reaches 0, calls `o`'s vtable slot `+0x20` with 0 and `006DA8A0(qword [01F3BA68], o)`; otherwise, when byte `[p]` is non-zero, keeps decrementing dword `[o+8]` until it reaches 0 and then makes the same two calls; nulls qword `[p+8]`; when the node's payload qword is non-null calls `006DA8A0(qword [01F3BA68], p)` and nulls it; then points the sentinel's next and prev at itself, zeroes qword `[rcx+0x40]` and calls `00210EB0(node)` for every node that followed the sentinel; returns the result of `00727450(rcx)` when negative, else 0 | `0075EC38`, `0075EC65`, `0075EC74`, `0075ECD7`, `0075ED04` |
| `00780C70` | 279 B | calls `007142F0` (result `d`) and `00714560`; when qword `o` = `[rcx+0x38]` is non-null decrements dword `[o+8]` and, when that reaches 0, calls `o`'s vtable slot `+0x20` with 0 and `006DA8A0(qword [01F3BA68], o)`, then nulls qword `+0x38`; when qword `a` = `[rcx+0x80]` is non-null calls `0075E690(qword [d+0x22248], dword [rcx+0x88], a)`, then, when qword `+0x80` is still non-null, calls `006DA8A0(qword [01F3BA68], that - 8)` and nulls it, and zeroes dword `+0x88`; then zeroes qwords `+0x38` to `+0x60`, `+0x80`, `+0x90`, `+0x98` and dwords `+0x68`, `+0x7C`, `+0x88`, `+0xA4`, sets qword `+0xA8` = 2, and returns the result of `00727450(rcx)` when negative, else 0 | `00780C87`, `00780C9F`, `00780CF0`, `00780D0C`, `00780D49` |
| `007819F0` | 258 B | calls `007273E0(rcx)` and returns a negative result; returns 0 when qword `[rcx+0x28]` is null; otherwise calls slot `+0` of the objects at qwords `[rcx+0x50]` and `[rcx+0x48]` with that qword, returning a negative result; then sets dword `+0x500` = 4, float `+0x504` = 0.25, dword `+0x508` = 2, zeroes qword `+0x64` and the 16 bytes at `+0x6C`, and for 17 entries i sets dword `+0x7C+4i` = 1, floats `+0x3F0+4i` and `+0x434+4i` = 1.0, zeroes dwords `+0x1D0`, `+0x214`, `+0x368`, `+0x3AC`, `+0x478`, `+0x4BC` (+4i) and the 16-byte slots `+0xC0+16i` and `+0x258+16i`; returns 0 | `007819F9`, `00781A1A`, `00781A2F`, `00781A5A`, `00781A90` |
| `00786410` | 225 B | walks the circular list headed at qword `[rcx+0x100]` with a cursor and calls `007854D0(rcx, &cursor)` for each node whose qword `+0x18` equals `rdx` (any node when `rdx` is null) and whose dword `+0x10` equals `r8d` (any when `r8d` is -1), re-reading the cursor after the call; returns the last negative result of those calls, else 0 | `0078646B`, `00786482`, `0078649D`, `007864A9`, `007864B8` |
| `00786DD0` | 307 B | takes `n` from its own vtable slot `+0x50` and returns 0x8000FFFF when it is 0; for each i below `n`, with `e` = entry i of the pointer array at qword `[rcx+0xF0]` (dword `[e+8]` is read with no null test): when dword `[e+8]` is above 1, calls `006DF480(00DAD520, 0x71B)` and `006DF480(00DAD570, i, dword [e+8])` when dwords `01F3BA80` and `01F3BA8C` are both at least 1, then clears byte `[e+0xAC]` and qword `[e+0xD8]`; when `e` is non-null calls its vtable slot `+8` and nulls the entry; finally, when qword `[rcx+0xF0]` is non-null, calls `006DA8A0(qword [01F3BA68], that - 8)` and nulls it; returns 0 | `00786DE0`, `00786E2B`, `00786E4F`, `00786E7C`, `00786EA8` |
| `007B1520` | 317 B | vector deleting destructor of 0x30-byte elements: when bit `0x2` of `edx` is set, walks the qword count at `rcx-8` back from the end and for each element stores vtable `01CB4B08`, then, when its qword `p` = `[element+0x10]` is non-null, calls vtable slot `+0` of `p` with 3 when qword `[p-8]` is non-zero, else `00210EB0(p - 8)`; zeroes qwords `+0x10` to `+0x28` and dword `+0xC` and stores the base vtable `01CB4470`; then, when bit `0x1` is set, calls `007AD450(rcx-8)` or, when bit `0x4` is also set, `0016D6A0(rcx-8, count*0x30+8)`, and returns `rcx-8`; otherwise calls `007B14C0(rcx)`, then, when bit `0x1` is set, `007AD450(rcx)` or, when bit `0x4` is also set, `0016D6A0(rcx, 0x30)`, and returns `rcx` | `007B158B`, `007B1593`, `007B15A9`, `007B15C1`, `007B1626` |
| `007C6370` | 283 B | returns a float product starting from 1.0: multiplies in the ramp at `rcx+0x318` and, when qword `[rcx+0x18]` points at a record whose byte `+0` is at least 1 and whose byte `+0xA` has bit `0x1` set, the ramp at `rcx+0x348` (each: end `+4` when duration `+0xC` is 0.0 or NaN, else start + `007A9E50(elapsed +8 / duration, curve dword +0x14)` times (end - start)); then floats `[rcx+0x5DC]` and `[rcx+0x5E0]`, float `[rcx+0x5E4]` under the same record test, and float `[rcx+0x5E8]` | `007C63B7`, `007C63C8`, `007C63FF`, `007C6432`, `007C646D` |
| `007D1840` | 295 B | a float setter keyed by `edx` with value `xmm2` and time `xmm3`: 0x200 stores the value at float `[rcx+0x20]` when byte `[rcx+0x30]` is non-zero, else calls `007CA560(rcx+0x38, value, time, 5 or 4, a stack byte 0)` (5 when `007A9E00(rcx+0x38)` is above the value, 4 otherwise, NaN included); 0x201 takes 1.0 / value (1.0 when the value is 0.0 or NaN) and stores it at float `+0x24` when byte `+0x30` is non-zero, else calls `007CA560(rcx+0x68, it, time, 0, a stack byte 0)`; 0x202 stores the value at float `+0x28` when byte `+0x30` is non-zero, else calls `007CA560(rcx+0x98, value, time, 0, a stack byte 0)`; 0x203 calls `007D16C0(rcx, truncated value, time)`; for any `edx`, a time of 0.0 or NaN then tail-calls its own vtable slot `+0x40` | `007D1882`, `007D1899`, `007D18D4`, `007D190D`, `007D1932` |
| `007D8A70` | 282 B | a float getter keyed by `r8d` - 0x100 through the jump table at image base + `0x6B8B8C`, writing to `[rdx]` and returning 0: keys 0x100, 0x102 and 0x103 give `logf` (`00861F98`) of `007A9E00` of the records at `rcx+0x18`, `+0x78` and `+0xA8` times `01CB7784` (8.685889); 0x101 gives `007A9E00(rcx+0x48)`; 0x104 and 0x105 give `007A9E00` of `rcx+0xD8` and `rcx+0x108` times `008C5F78` (1000); 0x106 and 0x107 give dwords `[rcx+0x13C]` and `[rcx+0x140]` converted to float; any other key returns -1 | `007D8A9A`, `007D8AB1`, `007D8AB6`, `007D8B04`, `007D8B42` |
| `007D8E40` | 258 B | a float setter keyed by `edx` - 0x100 through the jump table at image base + `0x6B8F44`, with value `xmm2` and time `xmm3`: keys 0x100, 0x102 and 0x103 pass `expf` (`00861FAA`) of (the value times `01CB7780` (0.1151293)) to `007CA560` on the records at `rcx+0x18`, `+0x78` and `+0xA8`; 0x101 passes the value to `rcx+0x48`; 0x104 and 0x105 pass the value times `008C5B2C` (0.001) to `rcx+0xD8` and `rcx+0x108` (each call with the time, 0 and a stack byte 0); 0x106 and 0x107 store the truncated value at dwords `+0x13C` / `+0x140` and call its own vtable slot `+0x40`; other keys do nothing | `007D8E6D`, `007D8E79`, `007D8E81`, `007D8EF3`, `007D8F1C` |
| `007D8F70` | 250 B | returns -1 when `rdx` is null; otherwise calls its own vtable slot `+0x10` eight times with the time in `xmm3`: keys 0x100 to 0x105 with floats `[rdx]` to `[rdx+0x14]`, keys 0x106 and 0x107 with dwords `[rdx+0x18]` and `[rdx+0x1C]` converted to float; then calls slot `+0x40` and returns 0 | `007D8FAC`, `007D8FC2`, `007D901A`, `007D902D`, `007D9055` |
| `007DB7A0` | 251 B | a float getter keyed by `r8d` - 0x1000 through the jump table at image base + `0x6BB89C`: keys 0x1000 to 0x1007 write `007A9E00` of the records at `rcx+0x490`, `+0x4C0`, `+0x4F0`, `+0x520`, `+0x550`, `+0x580`, `+0x5B0` and `+0x5E0` (in key order) to float `[rdx]` and return 0; any other key returns -1 | `007DB7C4`, `007DB7D9`, `007DB851`, `007DB881`, `007DB892` |
| `007DC0E0` | 271 B | calls `007CA560(record, target, xmm1, 0, a stack byte 0)` with the float in `xmm1` as the time on each of eight records: `rcx+0x490` with target 0, `+0x4C0`, `+0x4F0` and `+0x520` with 1.0, `+0x550` with `008F30F8` (0.2), `+0x580` with `0090035C` (0.08), `+0x5B0` with `01CEBC08` (2.0) and `+0x5E0` with `00D10FA8` (2000) | `007DC106`, `007DC125`, `007DC168`, `007DC1A6`, `007DC1DF` |
| `007DC1F0` | 293 B | a float setter keyed by `edx` - 0x1000 through the jump table at image base + `0x6BC318`, with value `xmm2` and time `xmm3`: keys 0x1000 to 0x1004 clamp the value to [0, 1.0] for the records at `rcx+0x490`, `+0x4C0`, `+0x4F0`, `+0x520` and `+0x550`; 0x1005 clamps it to [0, `008C5F6C` (0.1)] for `rcx+0x580`; 0x1006 takes max(value, 0) for `rcx+0x5B0`; 0x1007 clamps it to [`00D10FA8` (2000), `009146F8` (20000)] for `rcx+0x5E0`; a value below the lower bound or NaN gives the lower bound; each of these keys then calls `007CA560(record, clamped value, time, 0, a stack byte 0)`; other keys do nothing | `007DC210`, `007DC2BD`, `007DC2D8`, `007DC2EE`, `007DC30B` |
| `007DF1F0` | 288 B | for `edx` 0, 1 and 2 calls `0019C5D0(a 0x100-byte stack buffer, 0x100, s)` with `s` = `01CB7F38` "[sead][info]onStateChagned Inactive", `01CB7F60` "[sead][info]onStateChagned Active" or `01CB7F88` "[sead][info]onStateChagned Expired", stores a newline at the returned length (2 less when that is 0xFF or more) and a terminator after it (an index of 0x100 or more calls `00809728`), and calls `OutputDebugStringA` (`008C2120`) and `007A5570(0, buffer)`; other values do nothing; returns 0 (stack cookie `01F44830` checked by `00808C40`) | `007DF21E`, `007DF264`, `007DF293`, `007DF2A0`, `007DF2D5` |
| `007E2AD0` | 229 B | by dword `k` = `[rdx+0x18]`: 1 tests the byte result of `007CFF90(qword [rdx+0x20])` and 2 that of `007D07A0(qword [rdx+0x20])`; a zero result returns -1, a non-zero one stores qword `[rdx+0x20]` at `[rcx+0x50]` and returns `007D09B0(rcx, rdx)`; any other `k` calls `0019C5D0(a 0x100-byte stack buffer, 0x100, 01CB8470, k)`, stores a newline at the returned length (2 less when that is 0xFF or more) and a terminator after it (an index of 0x100 or more calls `00809728`), calls `OutputDebugStringA` (`008C2120`) and `007A5570(2, buffer)`, and returns -1 (stack cookie `01F44830` checked by `00808C40`) | `007E2B03`, `007E2B3A`, `007E2B4F`, `007E2B67`, `007E2BA6` |
| `007F10F0` | 265 B | zeroes the dwords at `rdx`, `r8`, `r9` and its fifth argument; with `m` = `007BB610(rcx)`, writes the four dot products of the 16-byte vector at `rcx+0xD0` with the 16-byte rows `[m+0x60]`, `[m+0x70]`, `[m+0x80]` and `[m+0x90]` (in that order) to the 16 bytes its sixth argument points at and to `rcx+0x120`; calls `007F0320` with (`rdx`, `r8`, `r9`, the fifth and sixth arguments, float `[rcx+0xE4]`, float `[rcx+0xE8]`, float `[rcx+0x130]`, byte `[rcx+0xEC]`); returns 0 | `007F112A`, `007F114A`, `007F118F`, `007F11CF`, `007F11D7` |
| `007F1850` | 265 B | zeroes the dwords at `rdx`, `r8`, `r9` and its fifth argument; with `m` = `007BB610(rcx)`, writes the four dot products of the 16-byte vector at `rcx+0xD0` with the 16-byte rows `[m+0x60]`, `[m+0x70]`, `[m+0x80]` and `[m+0x90]` (in that order) to the 16 bytes its sixth argument points at and to `rcx+0x110`; calls `007F0320` with (`rdx`, `r8`, `r9`, the fifth and sixth arguments, float `[rcx+0xE4]`, float `[rcx+0xE8]`, float `[rcx+0x120]`, byte `[rcx+0xEC]`); returns 0 | `007F188A`, `007F18AA`, `007F18EF`, `007F192F`, `007F1937` |
| `007F1DD0` | 232 B | with `m` = `007BB610(rcx)`, writes the four dot products of the 16-byte vector at `rcx+0x100` with the 16-byte rows `[m+0x60]`, `[m+0x70]`, `[m+0x80]` and `[m+0x90]` (in that order) to the 16 bytes its sixth argument points at; calls `007F0320` with (`rdx`, `r8`, `r9`, the fifth and sixth arguments, the float `008F8180` (10.0), 0.0, 0.0, byte `[rcx+0xEC]`); then stores 1.0 to the dwords at `rdx` and `r9`; returns 0 | `007F1DF1`, `007F1E16`, `007F1E5E`, `007F1E8E`, `007F1EAA` |
| `00832810` | 279 B | calls its own vtable slot `+8` with (a stack 4x4 matrix of the rows `008C5F80`, `008C5F90`, `008C5FB0` and zeros, a stack vector `a`, a stack vector `b`); with `d` = (`b` - `a`) times `01CEBB70` (0.5) times `01CEBC08` (2.0) per x/y/z component and `k` = the float in `xmm1` divided by `009146E8` (12.0), writes to `[r8]` the floats (dy^2 + dz^2) k, (dx^2 + dz^2) k and (dx^2 + dy^2) k (stack cookie `01F44830` checked by `00808C40`) | `00832877`, `0083287A`, `00832882`, `008328E5`, `00832901` |
| `00832CD0` | 249 B | sets the 16-byte vectors `rcx+0x40` = `01CCD870` (1e18 three times, then 0) and `rcx+0x50` = `01CCD880` (-1e18 three times, then 0); for each of the dword `[rcx+0x1C]` inline 0x60-byte entries at qword `[rcx+0x28]` calls vtable slot `+8` of the object at the entry's qword `+0x40` with (the entry, a stack vector `lo`, a stack vector `hi`), then for x, y and z lowers float `[rcx+0x40+4j]` to component j of `lo` when that is smaller and raises float `[rcx+0x50+4j]` to component j of `hi` when that is larger (a NaN component changes nothing) | `00832CED`, `00832D34`, `00832D48`, `00832D59`, `00832DA5` |
| `00835CE0` | 310 B | copies to `[rdx]` the 16 bytes at the pointer its own vtable slot `+0x78` returns (called with a stack buffer); with `r` = its slot `+0x50` result, returns `rdx` at once when `r` is 0.0 (a NaN `r` goes on); otherwise takes the x/y/z of the vector at `r8`, replaces them by (-1, -1, -1) when their squared length is below `01CCD4E0` (2^-46), scales them by 1 / `00861F14`(squared length), and adds them times a second slot `+0x50` result to floats `[rdx]`, `[rdx+4]` and `[rdx+8]`; returns `rdx` | `00835D00`, `00835D10`, `00835D63`, `00835DA1`, `00835DC5` |
| `00837F00` | 287 B | copies to `[rdx]` the 16 bytes at the pointer its own vtable slot `+0x78` returns (called with a stack buffer); takes the x/y/z of the vector at `r8`, replaces them by (-1, -1, -1) when their squared length is below `01CCD4E0` (2^-46), scales them by 1 / `00861F14`(squared length), and adds them times its slot `+0x50` result to floats `[rdx]`, `[rdx+4]` and `[rdx+8]`; returns `rdx` | `00837F30`, `00837F47`, `00837F6C`, `00837FAA`, `00837FCE` |
| `008553F0` | 257 B | appends the pointer `rdx` to the growable pointer array with count dword `[rcx+0x15C]`, capacity dword `[rcx+0x160]`, data qword `[rcx+0x168]` and owner byte `[rcx+0x170]`: when the count equals the capacity and the new capacity (twice the count, 1 for 0) exceeds it, takes `n` = `0085E680(new capacity*8, 0x10)`, copies the count entries into `n` (skipping each when `n` is null), calls `0085E710(old data)` when the old data is non-null and the owner byte is set, stores `n`, sets the owner byte to 1 and stores the capacity; then stores `rdx` at data + 8*count unless that address is null, and increments the count | `0085540C`, `00855442`, `00855476`, `00855498`, `008554DD` |
| `00855520` | 309 B | appends the pointer `rdx` to the growable pointer array with count dword `[rcx+0x104]`, capacity dword `[rcx+0x108]`, data qword `[rcx+0x110]` and owner byte `[rcx+0x118]`: when the count equals the capacity and the new capacity (twice the count, 1 for 0) exceeds it, takes `n` = `0085E680(new capacity*8, 0x10)`, copies the count entries into `n` (skipping each when `n` is null), calls `0085E710(old data)` when the old data is non-null and the owner byte is set, stores `n`, sets the owner byte to 1 and stores the capacity; then stores `rdx` at data + 8*count unless that address is null, and increments the count; when `r8b` is non-zero calls `008530A0(qword [rdx+0x20], rdx)` and tail-calls `008530A0(qword [rdx+0x28], rdx)` | `00855548`, `0085557C`, `008555B3`, `008555D5`, `00855639` |
| `00857820` | 262 B | calls `0083DE00(rcx)`; each test below calls its own vtable slot `+0x18` again for `w`: when `w` is non-null and `w`'s slot `+0x58` result has bit `0x800` or `0x1000` set, takes `n` = its own slot `+0xB8` result and, for i from `n` - 1 down to 0, calls `00855B80(rcx, its slot +0xC8 result for i)`; then, when `w` is non-null, `w`'s slot `+0x58` result has bit `0x1` or `0x2` set, and on repeated calls `w` is non-null and that result non-zero, calls vtable slot `+0x10` of each of the dword `[rcx+0x15C]` pointers in the pointer array at qword `[rcx+0x168]` with qword `[rcx+0x80]` | `0085782D`, `0085784F`, `00857878`, `00857885`, `00857905` |
| `0085C3E0` | 251 B | passes its ten arguments unchanged (`rcx`, `rdx`, `r8d`, `r9`, then on the stack a dword, a qword, a dword and three qwords) to its own vtable slots `+0x38`, `+0x40` and `+0x30` in that order; returns the float 0.0 | `0085C44D`, `0085C485`, `0085C4BD`, `0085C4C8` |
| `0085CDC0` | 259 B | for each i below dword `+0x14` of its eighth argument calls `0085DDE0` with (`rcx`, i, `rdx`, `r8d`, `r9`, then its fifth to tenth arguments); then passes its ten arguments unchanged to its own vtable slot `+0x28`; returns the float 0.0 | `0085CE02`, `0085CE52`, `0085CE9F`, `0085CEA7` |
| `0085DCE0` | 248 B | with `a` = its eighth argument: when dword `[a+0x2C]` is non-zero, repeats dword `[a+0x14]` times a pass over the dword `[rcx+0xC]` indices in the dword array at qword `[rcx+0x78]`, each index `k` naming the inline 0xC0-byte record `r` = qword `[rcx+0x18]` + 0xC0 k, and calls `0085AC50(rcx, qword [r+0x80], qword [r+0x88], r)` when bit `0x100` of dword `[a+0x3C]` is set, else `0085A900` with the same arguments | `0085DCF3`, `0085DD05`, `0085DD34`, `0085DD58`, `0085DDA8` |
| `008761A0` | 222 B | copies the singly linked list at qword `02EB8260` (next pointer at node `+0x10`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `008761C5`, `008761EC`, `0087620E`, `00876235`, `00876250` |
| `00876590` | 222 B | copies the singly linked list at qword `02EB82D8` (next pointer at node `+0x10`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `008765B5`, `008765DC`, `008765FE`, `00876625`, `00876640` |
| `008769A0` | 222 B | copies the singly linked list at qword `02EB8348` (next pointer at node `+0x10`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `008769C5`, `008769EC`, `00876A0E`, `00876A35`, `00876A50` |
| `00877160` | 222 B | copies the singly linked list at qword `02EB8428` (next pointer at node `+0x10`) into the counted pointer array at `rdx` (dword count `+0`, pointer `+8`): counts the nodes; when the count differs from dword `[rdx]`: a count of 0 makes the new block null without calling `0017D260`, otherwise the new block is `0017D260(count*8, 8)`, zero-filled, and a null result returns 0xD; then, when the old qword `[rdx+8]` differs from the new block, bit `0x80000000` of dword `[rdx]` is clear and the old qword is non-null, calls `00584730(old qword)`; stores the new block and count; then writes each node pointer in list order into the block; returns 0 | `00877185`, `008771AC`, `008771CE`, `008771F5`, `00877210` |
| `0087FC00` | 226 B | for each of the dword `[rdx+0xC]` pointers in the pointer array at qword `[rdx+0x18]`: an object whose byte `+0xE8` has bit `0x1` or `0x2` set gets dwords `+0xEC` = -1 and `+0xF0` = -2; otherwise, with `n` counting such objects from 0, it finds the root of element `n` in the 8-byte entries at qword `[rcx+0x18]` (dword `+0` the parent index, a root being its own parent; each visited entry's parent is replaced by its grandparent on the way), stores the root at dword `+0xEC`, stores the object's index in the array at dword `+4` of entry `n`, sets dword `+0xF0` = -1 and increments `n` | `0087FC38`, `0087FC49`, `0087FC6F`, `0087FC86`, `0087FCAA` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-vtable-method-index-ee-1003-5)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-vtable-method-index-ee-1003-5/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00684860` | 429 B | with `s` = ((`edx` + 15) AND ~0xF) + 16, head = qword `[rcx+0x40]`, tail = qword `[rcx+0x48]`: returns 0 when `s` >= dword `[rcx+0x38]` (unsigned) or the head is null; calls `005CD4F0(rcx)`; while the byte returned by `006B6690(rcx, s)` is non-zero it walks the tail along next qwords `+0` past blocks whose dword `+8` is 0 or, minus dword `02E41060`, has the sign bit set, stopping at another block or the head, and, if it passed none, calls `005CD820(rcx)` and returns 0; before each walk but a round's first it bumps a pass count (reset after the first), calls `005CDAA0(2, 00D6FF60, tail)` when the count is a multiple of 0x400, then `005CCB80(1)`; once `006B6690` returns 0: when head + `s` > qword `[rcx+0x30]` (unsigned) it moves the head to qword `[rcx+0x28]`, writes at the old head dword `+8` = 0, dword `+0xC` = low dword of `[rcx+0x30]` minus the old head's low dword, qword `+0` = qword `[rcx+0x28]`, and restarts the round; otherwise sets the head to head + `s` (qword `[rcx+0x28]` when equal to qword `[rcx+0x30]`), writes at the old head dword `+8` = 0, dword `+0xC` = `edx`, qword `+0` = the new head, stores the old head at qword `[rcx+0x50]`, calls `005CD820(rcx)` and returns it | `00684884`, `006848A8`, `006848B5`, `0068493A`, `006849EA` |
| `00725340` | 331 B | with `s` = `edx`, or dword `[rcx+0xA08]` when `edx` is -1: returns 0x80070057 when `s` is above 0x3F; with byte `01F3CBA8` zero resets the cached dword `[rcx+0xA04]` to -1; stores `s` at dword `+0xA08`; when byte `01F3CBA8` and `r8b` are both non-zero and the cache equals `s`, returns 1; otherwise, with `c` = the cache: when `c` is -1 or `c` XOR `s` has a bit in `0x7` or in `0x18`, calls vtable slot `+0x118` of the object at qword `[rcx+0x30]` with (qword `[rcx+0x60+16s]`, `rcx+0xA0C`, -1); when `c` is -1 or they differ in bit `0x20`, calls its slot `+0x158` with qword `[rcx+0x68+16s]`; stores `s` in the cache when byte `01F3CBA8` is non-zero; returns 0 | `00725351`, `0072536B`, `0072538C`, `00725440`, `0072545C` |
| `00725C80` | 429 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9DAA8, 0x219E)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9DBA8)`; when dword `02EA0B44` is non-zero takes `n` = `0071A630(the seventh-argument dword)` (`00D9C0D7` when null) and `f` = `0071B070(the sixth-argument dword, 1)` and, when dwords `01F3BA80` and `02EA0B44` are both at least 1, calls `006DF480(00D9DAD8 "PPFX: ")` and `006DF480(00D9E0E0, 00D9DBD8 "Tex3D", f, edx, r8d, r9d, n, seventh-argument dword, sixth-argument dword, ninth-argument dword)`; returns 0x80070057 when the eighth-argument pointer is null or any of `edx`, `r8d`, `r9d` is 0; otherwise stores `00787A80(rcx, edx, r8d, r9d, fifth-argument dword, seventh-argument dword, sixth-argument dword, ninth-argument dword)` to the qword the eighth argument points at; when that is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9E160, 0x21B0)` and `006DF480(00D9E1E0)`; a null result returns 0x80004005, else 0 | `00725CCA`, `00725D03`, `00725D78`, `00725DC3`, `00725E0A` |
| `00725E40` | 422 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9DDA8, 0x21C3)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9DD08)`; when dword `02EA0B44` is non-zero takes `n` = `0071A630(the sixth-argument dword)` (`00D9C10A` when null), `k` = `0071B9E0(0)` and `f` = `0071B070(the fifth-argument dword, 1)` and, when dwords `01F3BA80` and `02EA0B44` are both at least 1, calls `006DF480(00D9DDD8 "PPFX: ")` and `006DF480(00D9E3E0, 00D9DEF4 "Ref2D", f, edx, r8d, n, sixth-argument dword, k, 0, fifth-argument dword, 0)`; returns 0x80070057 when the eighth-argument pointer is null or `edx` or `r8d` is 0; otherwise stores `007876E0(rcx, seventh-argument qword, edx, r8d, r9d, sixth-argument dword, fifth-argument dword)` to the qword the eighth argument points at; when that is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9E4E0, 0x21D6)` and `006DF480(00D9E560)`; a null result returns 0x80004005, else 0 | `00725E7F`, `00725EB6`, `00725F40`, `00725F81`, `00725FC8` |
| `00725FF0` | 431 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9E128, 0x21E9)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9E1A8)`; when dword `02EA0B44` is non-zero takes `n` = `0071A630(the seventh-argument dword)` (`00D9C10B` when null) and `f` = `0071B070(the sixth-argument dword, 1)` and, when dwords `01F3BA80` and `02EA0B44` are both at least 1, calls `006DF480(00D9E158 "PPFX: ")` and `006DF480(00D9E5C0, 00D9E1D8 "Ref3D", f, edx, r8d, r9d, n, seventh-argument dword, sixth-argument dword, 0)`; returns 0x80070057 when the ninth-argument pointer is null or any of `edx`, `r8d`, `r9d` is 0; otherwise stores `00787B80(rcx, eighth-argument qword, edx, r8d, r9d, fifth-argument dword, seventh-argument dword, sixth-argument dword)` to the qword the ninth argument points at; when that is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9E6A0, 0x21FC)` and `006DF480(00D9E6F0)`; a null result returns 0x80004005, else 0 | `00726034`, `0072606D`, `007260E2`, `0072613A`, `00726181` |
| `007261B0` | 424 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9E358, 0x2210)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9E528)`; when dword `02EA0B44` is non-zero takes `n` = `0071A630(r9d)` (`00D9C10F` when null), `k` = `0071B9E0(the fifth-argument dword)` and `f` = `0071B070(1, 1)` and, when dwords `01F3BA80` and `02EA0B44` are both at least 1, calls `006DF480(00D9E308 "PPFX: ")` and `006DF480(00D9E750, 00D9E388 "RT   ", f, edx, r8d, n, r9d, k, sixth-argument dword, 1, eighth-argument dword)`; returns 0x80070057 when the seventh-argument pointer is null or `edx` or `r8d` is 0; otherwise stores `00786500(rcx, edx, r8d, r9d, 1, fifth-argument dword, sixth-argument dword, eighth-argument dword, ninth-argument qword, tenth-argument dword)` to the qword the seventh argument points at and returns 0x80004005 when that is null, else 0 | `007261FA`, `00726232`, `007262C0`, `0072631C`, `00726335` |
| `00726550` | 424 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9E648, 0x226F)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9E678)`; when dword `02EA0B44` is non-zero takes `n` = `0071A630(r9d)` (`00D9C1A1` when null), `k` = `0071B9E0(0)` and `f` = `0071B070(0, 1)` and, when dwords `01F3BA80` and `02EA0B44` are both at least 1, calls `006DF480(00D9E6E4 "PPFX: ")` and `006DF480(00D9E890, 00D9E834 "PSURF", f, edx, r8d, n, r9d, k, 0, 0, sixth-argument dword)`; returns 0x80070057 when the fifth-argument pointer is null or `edx` or `r8d` is 0; otherwise stores `00786500(rcx, edx, r8d, r9d, 0, 0, 0, sixth-argument dword, 0, 0)` to the qword the fifth argument points at; when that is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9E8E0, 0x228C)` and `006DF480(00D9E990)`; a null result returns 0x80004005, else 0 | `00726589`, `007265C2`, `00726647`, `00726698`, `007266DF` |
| `00726700` | 431 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9C070, 0x22B6)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9C0A0)`; when dword `02EA0B44` is non-zero takes `n` = `0071A630(r9d)` (`00D9C09F` when null), `k` = `0071B9E0(the fifth-argument dword)` and `f` = `0071B070(1, 1)` and, when dwords `01F3BA80` and `02EA0B44` are both at least 1, calls `006DF480(00D9C0C8 "PPFX: ")` and `006DF480(00D9C110, 00D9C0D0 "RefRT", f, edx, r8d, n, r9d, k, sixth-argument dword, 1, 0)`; returns 0x80070057 when the eighth-argument pointer is null or `edx` or `r8d` is 0; otherwise stores `00785A10(rcx, seventh-argument qword, edx, r8d, r9d, fifth-argument dword, sixth-argument dword)` to the qword the eighth argument points at; when that is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9C160, 0x22C9)` and `006DF480(00D9C1B0)`; a null result returns 0x80004005, else 0 | `0072673F`, `00726777`, `00726809`, `0072684A`, `00726891` |
| `007268C0` | 414 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9C268, 0x2303)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9C2E8)`; when dword `02EA0B44` is non-zero takes `n` = `0071B180(-1)` (`00D9C0C7` when null) and `f` = `0071B070(r9d, 1)` and, when dwords `01F3BA80` and `02EA0B44` are both at least 1, calls `006DF480(00D9C298 "PPFX: ")` and `006DF480(00D9C5C0, 00D9C10C, f, edx, r8d, edx*r8d, n, -1, r9d, the sixth-argument dword)`; stores `007885A0(rcx, edx, r8d, r9d, the sixth-argument dword, the seventh-argument qword)` to the qword its fifth argument points at; when that result is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9C690, 0x2311)` and `006DF480(00D9C760)`; a null result returns 0x80004005, else 0 | `00726904`, `0072693F`, `0072694B`, `007269BE`, `007269EA` |
| `00726A70` | 438 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9C4C8, 0x2325)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9C608)`; when dword `02EA0B44` is non-zero takes `n` = `0071B180(r9d)` (`00D9C0CF` when null) and `f` = `0071B070(the fifth-argument dword, 1)` and, when dwords `01F3BA80` and `02EA0B44` are both at least 1, calls `006DF480(00D9C314 "PPFX: ")` and `006DF480(00D9C8F0, 00D9C15C, f, edx, r8d, edx*r8d, n, r9d, fifth-argument dword, seventh-argument dword)`; stores `00788800(rcx, edx, r8d, r9d, fifth-argument dword, seventh-argument dword, eighth-argument qword)` to the qword its sixth argument points at (no argument checks); when that is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9C980, 0x2334)` and `006DF480(00D9C9D0)`; a null result returns 0x80004005, else 0 | `00726ABC`, `00726AF8`, `00726B78`, `00726BA4`, `00726C0F` |
| `00769470` | 389 B | calls vtable slot `+8` of the objects at qwords `[rcx+0x210]`, `[rcx+0x238]` and `[rcx+0x280]` (no null tests), then of qwords `+0x288`, `+0x290` and `+0x298` when non-null; of every pointer (no null test) in the pointer array at qword `[rcx+0x230]` (re-read per element) for the signed dword count `[rcx+0xD0]` read once (none when it is 0 or negative); of qwords `+0x248`, `+0x250`, `+0x258` and `+0x260` when non-null; when qword `+0x270` is non-null, of every pointer (no null test) in the array it points at (re-read per element) for the unsigned dword count `[rcx+0xF0]` (re-read per element); of qwords `+0x2A0`, `+0x2B0` and `+0x2A8` when non-null; of qword `+0x268` when non-null, then nulling it; tail-jumps to `00727410(rcx)` | `0076948C`, `007694B8`, `007694FE`, `0076957E`, `007695D3` |
| `0077DED0` | 329 B | calls vtable slot `+8` of the object at qword `[rcx+0x4B0]` (no null test); for i from 0 while i is less than the signed dword `[rcx+0xDC]` (re-read each pass, none when 0 or negative), with `e` = qword `[rcx+0x4B8]` + 0x108*i (inline 0x108-byte entries): when byte `[rcx+0x130]` is zero calls slot `+8` of qword `[e+0xA0]` (no null test), else of qwords `[e+0x80]` and `[e+0x88]` when non-null; calls slot `+8` of each non-null qword `[e+0x48+8j]` for j from 0 while j is less than the signed dword `[rcx+0x18C]` (re-read each pass); when qword `[e+0xA8]` is non-null and differs from qword `[e+0x48]`, calls slot `+8` of the non-null qwords `[e+0x90]` and `[e+0x98]` when byte `[rcx+0x130]` is non-zero, else of qword `[e+0xA8]`; then calls slot `+8` of qwords `[e+0xB0]` and `[e+0xB8]` when non-null; tail-jumps to `00727410(rcx)` | `0077DEE5`, `0077DF1A`, `0077DF6B`, `0077DF88`, `0077DFDC` |
| `00787080` | 359 B | returns 0x80070057 when `rdx` is null or when dword `+4` of the stack record that `rdx`'s vtable slot `+0x40` is called with is neither 4 nor 6 afterwards; otherwise, with `f` = qword `[rcx+0xF8]` (re-read from `[rcx+0xF8]` at each use, including after `0078AB60(rcx)`): when qword `[f]` is non-null calls its vtable slot `+0x10` and nulls it; zeroes dword `[rcx+0x14]`; calls `00784C50(rcx+0x40, rdx, 0, 0)` and `0078A970(rcx+0xB0, rcx+0x40)`; sets dword `+0x24` to 1 when bit `0x20` of dword `+0x58` is set, plus 2 when bit `0x40` is; stores `r9d` at dword `+0x28` (the masking branch on bit `0x800` of that 0..3 value never fires) and copies dword `+0x9C` to `+0xEC`; calls `0078AB60(rcx)`; stores `rdx` at qword `[f]` and calls that object's vtable slot `+8` and its slot `+0x38` with `rcx+0x38`; then calls its own vtable slot `+0x38` and, on a negative result, its slot `+0x40`, else its slot `+0x68` with 0; returns 0 | `007870BF`, `007870EE`, `0078710B`, `00787146`, `007871B9` |
| `00787930` | 323 B | returns 0x80070057 when `rdx` is null or when dword `+4` of the stack record that `rdx`'s vtable slot `+0x40` is called with is not 8 afterwards; otherwise, with `f` = qword `[rcx+0xF8]` (re-read from `[rcx+0xF8]` at each use, including after `0078AB60(rcx)`): when qword `[f]` is non-null calls its vtable slot `+0x10` and nulls it; zeroes dword `[rcx+0x14]`; calls `00784C50(rcx+0x40, rdx, 0, 0)` and `0078A970(rcx+0xB0, rcx+0x40)`; sets dword `+0x24` to 1 when bit `0x20` of dword `+0x58` is set, plus 2 when bit `0x40` is; copies dword `+0x4C` to `+0xF0`, stores `r9d` at dword `+0x28` (the masking branch on bit `0x800` of that 0..3 value never fires) and copies dword `+0x9C` to `+0xEC`; calls `0078AB60(rcx)`; stores `rdx` at qword `[f]` and calls that object's vtable slot `+8` and its slot `+0x38` with `rcx+0x38`; calls its own vtable slot `+0x68` with 0; returns 0 | `0078796D`, `00787995`, `007879B2`, `007879F6`, `00787A5E` |
| `007B93E0` | 424 B | calls `EnterCriticalSection` (`008C20B8`) on `rcx+0x10`, and calls `LeaveCriticalSection` (`008C20C0`) on it before every return; returns -1 when qword `[rcx+0x60]` is null; when the signed count dword `[rcx+0x474]` is 30 or more calls `0019C5D0(a 0x100-byte stack buffer, 0x100, 01CB52E0)`, stores a newline at the returned length (2 less when that is 0xFF or more) and a terminator after it (an index of 0x100 or more calls `00809728`), calls `OutputDebugStringA` (`008C2120`) and `007A5570(2, buffer)` and returns -1; otherwise takes `m` = 2 when slot `+0x68` of the object at qword `[rcx+0x60]` returns 1 and 4 when it returns 2 (any other result returns -1), calls slot `+0x60` of the object at qword `[rcx+0x60]` (re-read) and returns -1 unless the unsigned 64-bit remainder of `r8` divided by the sign-extended 32-bit product of that result and `m` is 0 (a zero product faults in the `div`); then fills the ring entry at slot (dword `[rcx+0x478]` + count) signed-remainder 32 with qwords `[rcx+0x70+32*slot]` = `rdx`, `+0x78` = `r8`, `+0x80` = `r9` and `+0x88` = its fifth argument, increments the count, calls `007B9590(rcx-8)` and returns 0 (stack cookie `01F44830` checked by `00808C40`) | `007B9418`, `007B945F`, `007B94E8`, `007B9512`, `007B956D` |
| `007B9770` | 408 B | when dword `[rcx+0x484]` is positive decrements it and, when it reaches 0: when `r9` is not -1, calls `EnterCriticalSection` (`008C20B8`) on `rcx+0x10` and searches the dword `[rcx+0x474]` entries of a 32-slot ring of 32-byte entries, starting at slot dword `[rcx+0x478]` (slot = (start + i) signed-remainder 32), for qword `[rcx+0x88+32*slot]` equal to `r9`; a hit at i sets the start to that slot, subtracts i from the count and stores `r8d` at dword `+0x470`; a miss calls `0019C5D0(a 0x100-byte stack buffer, 0x100, 01CB5330, r9)`, stores a newline at the returned length (2 less when that is 0xFF or more) and a terminator after it (an index of 0x100 or more calls `00809728`), and calls `OutputDebugStringA` (`008C2120`) and `007A5570(1, buffer)`; either way calls `LeaveCriticalSection` (`008C20C0`) on `rcx+0x10`; then, also when `r9` is -1, calls `007CA560(rcx+0x4B8, 1.0, xmm1, 0, a stack byte 0)` and vtable slot `+0x18` of the object at qword `[rcx+0x60]`; returns 0 (stack cookie `01F44830` checked by `00808C40`) | `007B97B6`, `007B97D0`, `007B9808`, `007B989C`, `007B98EC` |
| `007C61F0` | 336 B | zeroes the dwords at `rdx`, `r8` and `r9`, then adds to them, as floats, the ramps at `rcx+0x528`, `rcx+0x558` and `rcx+0x588` in that order; each ramp (start `+0`, end `+4`, elapsed `+8`, duration `+0xC`, curve dword `+0x14`) gives its end when the duration is 0.0 or NaN, else start + `007A9E50(elapsed / duration, curve)` times (end - start); returns 0 | `007C622F`, `007C6258`, `007C62AF`, `007C630D`, `007C6336` |
| `007D9070` | 400 B | advances six ramps by the float `xmm1`: for k from 0 to 5, when byte `[rcx+0x38+0x30k]` is non-zero adds it to float `[rcx+0x28+0x30k]` and, when that reaches float `[rcx+0x2C+0x30k]`, clamps it there and clears the byte, else (NaN included) keeps the byte at 1; calls its own vtable slot `+0x40` when any of the six bytes was non-zero on entry; returns 0 | `007D9088`, `007D9097`, `007D90EC`, `007D91D1`, `007D91F6` |
| `007DC340` | 345 B | returns -1 when `rdx` is null; otherwise calls its own vtable slot `+0x10` eight times with the key in `edx`, a float in `xmm2` and the incoming `xmm3` passed through unchanged as the fourth argument: key 0x1000 with float `[rdx]`; keys 0x1001 to 0x1006 with floats `[rdx+4]` to `[rdx+0x18]` when `r8b` is non-zero, else with 1.0, 1.0, 1.0, `008F30F8` (0.2), `0090035C` (0.08) and `01CEBC08` (2.0); key 0x1007 with float `[rdx+0x1C]` when `r8b` is above 1, else `00D10FA8` (2000); returns 0 | `007DC37F`, `007DC3A7`, `007DC3F9`, `007DC45C`, `007DC47F` |
| `007E32E0` | 361 B | returns -1 when qword `[rdx+8]` is 0; otherwise sets dword `[rcx+0x80]` = 1 and copies qword `[rdx+0x20]` to `+0x88`, dword `[rdx+0x28]` to `+0x90` and byte `c` = `[rdx+0x2C]` to `+0x94`; when `c` is 0 or above 0x10 calls `0019C5D0(a 0x100-byte stack buffer, 0x100, 01CB8580, c)`, stores a newline at the returned length (2 less when that is 0xFF or more) and a terminator after it (an index of 0x100 or more calls `00809728`), calls `OutputDebugStringA` (`008C2120`) and `007A5570(2, buffer)` and returns -1; otherwise for i from 0 while i is less than byte `[rcx+0x94]` (re-read after each pass, after `007E2BC0` has received `rcx`) takes `p` = `007AD460(8, 0xA0, 0)` and, when it is non-null, calls `00861EC0(p, 0, 0xA0)` and stores `007E2BC0(p, rcx)` at qword `[rcx+0xB0+8i]` (a null `p` stores null); returns `007D09B0(rcx, rdx)` (stack cookie `01F44830` checked by `00808C40`) | `007E330A`, `007E336C`, `007E3384`, `007E338F`, `007E33BE` |
| `00808240` | 399 B | with the cursor qword `[r8]` and the signed value `rdx`: returns the result of `00802310(rcx, r8)` when negative; returns 0 when the cursor's vtable slot `+0x10` returns 0, or when `rdx` is not greater (signed) than `00802820(the cursor's slot +8 result, b)` with `b` = qword `[cursor+8]`; otherwise binary-searches the pointer array at qword `[[rcx+8]+0xA0]`, from signed index dword `[b+0x10]` up to signed dword `[[rcx+8]+0xA8]`, for the first entry `e` whose key is greater (signed) than `rdx`, the key being `00802DA0(e, two stack slots)` sign-extended when negative, else qword `[e+0x28]`, multiplied by qword `[qword [qword [e] + 0x78] + 0x28]` when not negative; then steps back one entry at a time starting with the entry before that position (the first step taken unconditionally), storing `00802100(entry, rcx, rdx)` at `[r8]` after each step until a stored value is non-null with a non-zero slot `+0x10` result; when a step lands on the start index without such a value it stores `rcx+0x90` at `[r8]` instead; that is the only bound, so when the search position is the start index or the range is empty the steps begin below it and continue down until a hit; returns 0 | `00808256`, `0080828E`, `0080830A`, `00808329`, `00808359` |
| `008373D0` | 417 B | calls `00830B40(rcx, rdx, r8)` and vtable slot `+0x68` of the object at qword `[rcx+0x40]` with (`rdx+0x10`, `r8`), and copies dword `[rcx+0x18]` to `[rdx+0x48]`; with `s` = `r8` and `b` = qword `[rcx+0x50]`: when `b` is non-null and bit `0x1` of `s`'s slot `+0x60` result is clear, stores at qword `[rdx+0x30]` `s`'s slot `+0x28` result for `b` when non-null, else `s`'s slot `+0x30` result for `b`, and in that case takes `c` = `s`'s slot `+0x18` with (`b`'s slot `+0x18` result sign-extended, 1) and calls `s`'s slot `+0x20` with (`c`, `b`'s slot `+8` result for (qword `[c+8]`, `s`), 0x48564251, `b`); otherwise stores 0 there; zeroes qword `[rdx+0x38]`; handles `m` = qword `[rcx+0x58]` the same way into qword `[rdx+0x40]` under bit `0x2` of a second `s` slot `+0x60` call, with `m`'s slot `+8` result in place of `b`'s slot `+0x18` result, `m`'s slot `+0x10` in place of `b`'s slot `+8`, the tag 0x50414D54 and no further zeroed qword; returns `01CCDFE8` ("btTriangleMeshShapeData") | `008373ED`, `00837400`, `0083742F`, `008374A3`, `00837547` |
| `00841010` | 151 B | with `o` = qword `[rcx]`, when `o` is non-null: when qword `[o+0x30]` is non-zero calls `008414E0(rcx, qword [o+0x28])` and `008414E0(rcx, qword [o+0x30])`; nulls qword `[rcx]` when it still equals `o`; calls `0085E710(qword [rcx+8])` and stores `o` at qword `+8`; then, in every case, calls `0085E710(qword [rcx+8])`, nulls qword `+8` and sets dword `+0x10` = -1; when qword `+0x30` is non-null calls `0085E710` on it if byte `+0x38` is non-zero; zeroes qwords `+0x30` and `+0x24`, sets byte `+0x38` = 1 and zeroes dword `+0x18` | `0084102C`, `00841036`, `0084104C`, `00841060`, `0084107F` |
| `00841D30` | 348 B | tests the triangle of the three 16-byte points at `rdx`, `rdx+0x10` and `rdx+0x20` against the box with minimum floats `[rcx+0x10]` to `[rcx+0x18]` and maximum floats `[rcx+0x20]` to `[rcx+0x28]`: returns when, on x, z or y (tested in that order), the picked smallest of the three coordinates is above the box maximum or the picked largest is below the box minimum; each pick compares the first two points and then the winner against the third with `comiss`, and an unordered (NaN) compare picks the later point, while an unordered compare against the box does not return; otherwise calls vtable slot `+8` of the object at qword `[rcx+8]` with (`rdx`, `r8d`, `r9d`) | `00841D64`, `00841D78`, `00841DDA`, `00841E3A`, `00841E74` |
| `00847D00` | 346 B | with `p` = its fifth argument and `q` = its sixth, builds the stack vector `d` = (floats `[p+0x30]`, `[p+0x34]`, `[p+0x38]` minus `[q+0x30]`, `[q+0x34]`, `[q+0x38]`, 0); when `0084FB30(r8, p, r9, q, &d, &a stack result, 1)` returns non-zero, copies the result's 16-byte fields `+0x10`, `+0x20` and `+0x30` to the 16 bytes its eighth, ninth and seventh arguments point at and returns 1; otherwise calls `0084D7C0(r8, p, r9, q, &d, &the stack result)` and, when that returns non-zero, makes the same three copies; that path returns 0 either way (stack cookie `01F44830` checked by `00808C40`) | `00847D61`, `00847DBA`, `00847DCF`, `00847E05`, `00847E2C` |
| `0084A0C0` | 343 B | takes `n` = `0085E680(0x60, 0x10)` and, when it is non-null, fills qword `[n]` = its fifth argument, words `[n+8]` / `[n+0xA]` = its sixth / seventh arguments, the 16 bytes at `rdx` and at `r8` into `[n+0x20]` / `[n+0x30]`, and zeroes qwords `[n+0x10]`, `[n+0x48]`, `[n+0x50]` (the stores that follow have no null test); sets dword `[n+0x58]` = dword `[rcx+0xAC]`, increments dword `[rcx+0xD8]` and copies it to dword `[n+0x18]`; stores `008410B0(rcx+8, &a stack copy of the two vectors, n)` at qword `[n+0x40]`; pushes `n` on the front of the list headed at qword `[rcx+0x88+8*dword [rcx+0xAC]]` (next `+0x50`, prev `+0x48`); when byte `[rcx+0xDD]` is zero calls `00849560(rcx+8, qword [rcx+8], &the stack vectors, &a stack pair (rcx, n))` and `00849560(rcx+0x48, qword [rcx+0x48], &the stack vectors, &the stack pair)`; returns `n` | `0084A0E6`, `0084A11F`, `0084A17F`, `0084A1B2`, `0084A1F9` |
| `00855660` | 389 B | with `o` = `rdx`: when byte `[o+0xE8]` has neither bit `0x1` nor `0x2` set and bit `0x1` of byte `[o+0x230]` is clear, calls `00854110(o, rcx+0x140)`; returns when qword `[o+0xD0]` is 0; when bit `0x1` of byte `[o+0xE8]` is set calls `0083A3A0(o, 2)`, otherwise appends `o` to the growable pointer array with count dword `[rcx+0x124]`, capacity dword `[rcx+0x128]`, data qword `[rcx+0x130]` and owner byte `[rcx+0x138]` (when full, `0085E680(new capacity*8, 0x10)` with twice the count (1 for 0) gets the entries, the old data goes to `0085E710` when non-null with the owner byte set, the owner byte becomes 1; the store is skipped when data + 8*count is null); then calls its own vtable slot `+0x38` with (`o`, 1, -1) when dword `[o+0xE8]` AND 3 is 0, else with (`o`, 2, 0xFFFFFFFD) | `0085566A`, `0085568C`, `008556F5`, `0085578D`, `008557D1` |
| `008557F0` | 373 B | with `o` = `rdx`: when byte `[o+0xE8]` has neither bit `0x1` nor `0x2` set and bit `0x1` of byte `[o+0x230]` is clear, calls `00854110(o, rcx+0x140)`; returns when qword `[o+0xD0]` is 0; when bit `0x1` of byte `[o+0xE8]` is set calls `0083A3A0(o, 2)`, otherwise appends `o` to the growable pointer array with count dword `[rcx+0x124]`, capacity dword `[rcx+0x128]`, data qword `[rcx+0x130]` and owner byte `[rcx+0x138]` (when full, `0085E680(new capacity*8, 0x10)` with twice the count (1 for 0) gets the entries, the old data goes to `0085E710` when non-null with the owner byte set, the owner byte becomes 1; the store is skipped when data + 8*count is null); then calls its own vtable slot `+0x38` with (`o`, `r8w` and `r9w` zero-extended) | `008557FE`, `00855828`, `0085588A`, `0085592A`, `00855953` |
| `00857CD0` | 416 B | returns 0 when qword `[rdx]` equals qword `[rcx+0x60]`, when word `[rdx+8]` AND word `[rcx+0xE]` is 0, or when word `[rdx+0xA]` AND word `[rcx+0xC]` is 0; returns 1 when vtable slot `+0x30` of the object at qword `[rcx+0x78]` returns a zero byte; otherwise takes `r` = vtable slot `+0x60` of the object at qword `[rcx+0x70]` with (qword `[qword [rcx+0x60] + 0xC8]`, `rdx`) and returns 1 when `r` or qword `[r+0x10]` is null; else calls slot `+0x18` of the object at qword `[r+0x10]` with the address of an empty stack pointer list (count dword `+4`, capacity dword `+8`, data qword `+0x10`, owner byte `+0x18` = 1), then returns 0 at the first listed pointer (no null test) whose object has signed dword `+0x4A0` greater than 0, else 1 (also when the count is 0 or negative); before returning, a non-null list data with the owner byte set is passed to `0085E710` | `00857CF6`, `00857D22`, `00857D53`, `00857DF5`, `00857E13` |
| `008588A0` | 340 B | with `dt` = `xmm1`, `m` = `r8d` and `h` = `xmm3`: when `m` is non-zero stores `a` = `dt` + float `[rcx+0x150]` at `+0x150` and, when `a` is at least `h`, takes `n` = truncate(`a` / `h`) and stores `a` - float(`n`) times `h` at `+0x150` (`n` = 0 when `a` is below `h` or the compare is unordered); when `m` is 0 stores `dt` at `+0x150`, uses `dt` as `h`, and takes `n` = `m` = 1 unless the absolute `dt` is below `00D841C0` (2^-23), where `n` = `m` = 0 (a NaN `dt` gives 1); when its own vtable slot `+0x18` returns non-null it calls slot `+0x18` again and stores bit `0x10` of the second result's slot `+0x58` result (no null test on the second result) as 0 or 1 in byte `02EAF3C0`; when `n` is non-zero, with `k` = the signed min(`n`, `m`), calls its own slots `+0x128` with float(`k`) times `h` and `+0x138`, then `k` times (none when `k` is 0 or negative) slot `+0x120` with `h` followed by slot `+0x90`; when `n` is 0 calls slot `+0x90` once; then calls slot `+0xD8` and returns `n` | `008588C7`, `008588E3`, `00858912`, `00858957`, `0085897E` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-vtable-method-index-ee-1003-6)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-vtable-method-index-ee-1003-6/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00655F10` | 450 B | with `a` = `00584740(0x50)`, calls `00615550(a)` when `a` is non-null and stores `a` (null on failure) at qword `[rcx+0x4240]`; with `c` = dword `[a+0x18]` AND 0x7FFFFFFF (1 when that is 0; no null test on `a`), when `c` is not 8 and `00628050(a, 8)` returns 0, zeroes dword `[a+4]`; returns `0061F070(qword [rcx+0x4240], 0x2800, 0)` when non-zero; does the same with a second `00584740(0x50)` block at qword `[rcx+0x4248]` and `0061F070(qword [rcx+0x4248], 0xC00, 0)`; returns 0 when dword `+0x168` of the `005FD050()` result is less than 0xB000 (signed); otherwise takes `b` = `00584740(0x68)`, calls `00616060(b)` when non-null, stores `b` (null on failure) at qword `[rcx+0x4318]` and returns `0061F200(b, 0x4000, 0xA0, 0xA, 0)` when non-zero; only after that call returns 0 takes a second `00584740(0x68)` block the same way into qword `[rcx+0x4320]` and returns `0061F200(that block, 4, 4, 8, 0)` when non-zero; then zeroes byte `[rcx+0x4309]` and returns 0 | `00655F36`, `00655F7C`, `00655F97`, `0065600D`, `006560B5` |
| `00692080` | 514 B | copies a record from `rdx` into `rcx` and returns `rcx`: qword `+8`, dwords `+0x10` to `+0x40`, the three dwords at each of `+0x48`, `+0x58` and `+0x68`, the three dwords at each `+0x78 + 0xA0i + 0x10j` for i 0 to 1 and j 0 to 9, and the 0x50 bytes at `+0x1B8` dword by dword; bytes `+0` to `+7`, dwords `+0x44`, `+0x54`, `+0x64`, `+0x74` and the fourth dword of each `+0x78 + 0xA0i + 0x10j` slot are not copied | `00692087`, `006920E5`, `00692124`, `006921BC`, `00692233` |
| `00725AA0` | 460 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9D868, 0x2174)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9D898)`; when dword `02EA0B44` is non-zero takes `n` = `0071A630(the sixth-argument dword)` (`00D9C0D6` when null), `k` = `0071B9E0(the seventh-argument dword)` and `f` = `0071B070(the fifth-argument dword, 1)` and, when dwords `01F3BA80` and `02EA0B44` are both at least 1, calls `006DF480(00D9D944 "PPFX: ")` and `006DF480(00D9DE60, 00D9D994 "Tex2D", f, edx, r8d, n, sixth-argument dword, k, eighth-argument dword, fifth-argument dword, tenth-argument dword)`; returns 0x80070057 when the ninth-argument pointer is null or `edx` or `r8d` is 0; otherwise stores `007872F0(rcx, edx, r8d, r9d, then the sixth, seventh, eighth, fifth and tenth argument dwords)` to the qword the ninth argument points at; when that is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9DEB0, 0x2189)` and `006DF480(00D9DF00)`; a null result returns 0x80004005, else 0 | `00725AE4`, `00725B2B`, `00725BBE`, `00725C05`, `00725C4C` |
| `00726360` | 482 B | when dwords `01F3BA80` and `02EA0B40` are both at least 1 calls `006DF480(00D9E478, 0x2234)` (format "GPUInterfaceDevice.cpp(%d) : PPFX: " after a path prefix) and `006DF480(00D9E4A8)`; when dword `02EA0B44` is non-zero takes `n` = `0071A630(r9d)` (`00D9C15F` when null), `k` = `0071B9E0(the fifth-argument dword)` and `f` = `0071B070(2, 1)` and, when dwords `01F3BA80` and `02EA0B44` are both at least 1, calls `006DF480(00D9E554 "PPFX: ")` and `006DF480(00D9E7A0, 00D9E5B4 "DS   ", f, edx, r8d, n, r9d, k, sixth-argument dword, 2, eighth-argument dword)`; returns 0x80070057 when the seventh-argument pointer is null or `edx` or `r8d` is 0; otherwise stores `00786500(rcx, edx, r8d, r9d, 2, fifth-argument dword, sixth-argument dword, eighth-argument dword, ninth-argument qword, tenth-argument dword)` to the qword the seventh argument points at; when that is null, and dwords `01F3BA80` and `01F3BA90` are both at least 1, calls `006DF480(00D9E7F0, 0x224C)` and `006DF480(00D9E840)`; a null result returns 0x80004005, else 0 | `007263AA`, `007263E2`, `00726470`, `007264D8`, `0072651F` |
| `0073BB50` | 459 B | with `a` = `xmm1` and `b` = `xmm2`: when `a` / `b` is below `009002D0` (1.01) or above `00915258` (4096) replaces `b` by `a` divided by that bound (a NaN ratio is left as it is), then applies the same clamp once more; with `q` = `a` / `b` and `y` = `0075B130(q, 0)`, calls vtable slot `+0x88` of the object at qword `[rcx+0x38]` three times, each with a dword key and the address of four stack floats: key dword `[rcx+0x128]` with (`y`, 1/`y`, (e - 1)/`a`, `a`/(e - 1)) where e = `00861FAA`(`y`) (expf); key dword `[rcx+0x12C]` with (`b`, 1/`b`, `q` - 1, 1/(`q` - 1)); key dword `[rcx+0x130]` with (4/`q`^2 - 2, 1/`b`, 1/`q`^2, `a`^2/(2`b`)) | `0073BB98`, `0073BBFC`, `0073BC15`, `0073BC4D`, `0073BCF0` |
| `007D1C80` | 559 B | with `w` = the ramp at `rcx+0x40` (end `+0x44` when duration float `+0x4C` is 0.0 or NaN, else start `+0x40` + `007A9E50(elapsed +0x48 / duration, curve dword +0x54)` times (end - start)) times `01CEBC78` (2 pi) times float `01F41D18` (image value 2.083333e-05), switches on dword `[rcx+0x18]` through the jump table at image base + `0x6B1EB0`: 0 sets float `[rcx+0xD8]` = 1.0 and zeroes qwords `+0xD0` and `+0xDC`; 1 to 4 tail-call `007D1080`, `007D0EA0`, `007D0DD0` and `007D1280` with (`rcx+0xD0`, `w`, `007A9E00(rcx+0x68)`); 5 to 7 tail-call `007D1140`, `007D0F60` and `007D1330` with (`rcx+0xD0`, `w`, `007A9E00(rcx+0x68)`, `007A9E00(rcx+0x98)`); 8 calls `007D0D30(rcx+0xD0, w, 007A9E00(rcx+0x68))`; above 8 (unsigned) does nothing | `007D1CB3`, `007D1CF2`, `007D1D0A`, `007D1D4D`, `007D1E9A` |
| `007D9EA0` | 498 B | evaluates five ramps (each: end `+4` when duration `+0xC` is 0.0 or NaN, else start `+0` + `007A9E50(elapsed +8 / duration, curve dword +0x14)` times (end - start)): stores at dword `[rcx+0x110]` the truncated ramp at `rcx+0x20`, 0x3FF when that is 0x400 or more unsigned; at float `+0x124` that dword converted to float times the ramp at `rcx+0x50`; at float `+0x120` the ramp at `rcx+0x80` times `01CEBC78` (2 pi) divided by `007AED00()` converted to float; at float `+0x118` the ramp at `rcx+0xE0`; and at float `+0x114` the ramp at `rcx+0xB0` | `007D9EDB`, `007D9F01`, `007D9F4F`, `007D9FAD`, `007DA084` |
| `007DC4A0` | 517 B | advances eight ramps by the float `xmm1`: for k from 0 to 7, when byte `[rcx+0x4B0+0x30k]` is non-zero adds it to float `[rcx+0x4A0+0x30k]` and, when that reaches float `[rcx+0x4A4+0x30k]`, clamps it there and clears the byte, else (NaN included) keeps the byte at 1; returns 0 | `007DC4B4`, `007DC4D1`, `007DC577`, `007DC64F`, `007DC696` |
| `007DD040` | 467 B | taking `EnterCriticalSection` (`008C20B8`) on `rcx+8` before and `LeaveCriticalSection` (`008C20C0`) after each list read, walks the nodes from qword `[rcx+0xC0]`: for node `n`, when vtable slot `+0x10` of the object at qword `[n+0x28]` with 0 returns a non-zero byte, calls `001217E0(qword [n+0x20])`, reads `x` = qword `[n+0x10]` under the lock, calls `007DD220(rcx+0xA0, dword [n+0x18])` and moves to `x` when that is not negative, else repeats `n` with no retry bound; otherwise moves to qword `[n+0x10]` when bit `0x1` of byte `[n+0x1C]` is set, else stops; then calls `00121D40(qword [rcx+0x38], rcx+0x48, dword [rcx+0x9C], 0x80, &a stack count c)`; when `c` is greater than 0 (signed) writes in order to the buffer qword `[rcx+0x88+8*dword [rcx+0x98]]`, for each i < `c` and j < the signed dword `[rcx+0x9C]` (re-read), dword i of the buffer qword `[rcx+0x48+8j]`, calls vtable slot `+0x48` of the object at qword `[rcx+0x40]` with (that buffer, 4 times `c` times dword `[rcx+0x9C]`, 0, 0) and sets dword `+0x98` = (dword `+0x98` - 1) AND 1; otherwise calls that slot with (qword `02EAE098`, dword `02EAE090`, 0, 0) (stack cookie `01F44830` checked by `00808C40`) | `007DD065`, `007DD0A3`, `007DD0CB`, `007DD123`, `007DD1C1` |
| `007DE120` | 449 B | calls `InitializeSRWLock` (`008C22F0`) on `rcx+0x38`; stores `CreateEventExW(0, 0, 0, 0x1F0003)` (`008C2320`) at qword `[rcx+0x18]` and, when null, sets it to -1 and returns 0x80004005; stores `CreateThread(0, 0, 007DEC40, rcx, 4, 0)` (`008C21C8`) at qword `[rcx+0x10]` and, when null, sets it to -1, takes `h` = `GetLastError()` (`008C20A8`), as 0x80070000 OR its low 16 bits when positive, calls `0019C5D0(a 0x100-byte stack buffer, 0x100, 01CB8148 "[sead][!!error!!]create MockDeviceThread failed! %x", h)`, stores a newline at the returned length (2 less when that is 0xFF or more) and a terminator after it (an index of 0x100 or more calls `00809728`), calls `OutputDebugStringA` (`008C2120`) and `007A5570(2, buffer)` and returns `h`; when `SetThreadPriority(thread, dword [rdx+0xC])` (`008C21E0`) returns 0 repeats the steps from `GetLastError()` on with `01CB8180` ("[sead][!!error!!]Set priority AudioSampleThread failed! %x"), without the -1 store; otherwise calls `SetThreadAffinityMask(thread, qword [rdx+0x10])` (`008C2200`) unless that qword is -1, copies dwords `[rdx]`, `[rdx+4]`, `[rdx+8]` to `[rcx+0x28]`, `[rcx+0x2C]`, `[rcx+0x34]` and returns 0 | `007DE149`, `007DE15C`, `007DE19C`, `007DE22F`, `007DE29D` |
| `00832E90` | 515 B | calls `00830B40(rcx, rdx, r8)`; with `s` = `r8`, copies dword `[rcx+0x6C]` to `[rdx+0x1C]` and `n` = dword `[rcx+0x1C]` to `[rdx+0x18]` and zeroes qword `[rdx+0x10]`; when `n` is 0 returns `01CCD858` ("btCompoundShapeData") at once; otherwise takes `c` = `s`'s slot `+0x18` with (0x50, `n`) and stores `s`'s slot `+0x30` result for `p` = qword `[c+8]` at `[rdx+0x10]`; for i from 0 while i is less than the signed dword `[rdx+0x18]` (re-read each pass), with `e` = qword `[rcx+0x28]` + 0x60 i, `d` = `p` + 0x50 i and `h` = qword `[e+0x40]`: copies dword `[e+0x4C]` to `[d+0x4C]`, stores `s`'s slot `+0x30` result for `h` at `[d+0x40]` and, when `s`'s slot `+0x28` result for `h` is null, takes `k` = `s`'s slot `+0x18` with (`h`'s slot `+0x58` result sign-extended, 1) and calls `s`'s slot `+0x20` with (`k`, `h`'s slot `+0x60` result for (qword `[k+8]`, `s`), 0x50414853, `h`); then copies dword `[e+0x48]` to `[d+0x48]` and the 0x40 bytes at `e` to `d`; after the loop calls `s`'s slot `+0x20` with (`c`, `01CCD838` "btCompoundShapeChildData", 0x59415241, qword `[c+8]`) and returns `01CCD858` | `00832EA5`, `00832EDE`, `00832F3A`, `00832FB2`, `00833072` |
| `008330A0` | 491 B | with `s` = the x/y/z floats at `rdx`: for i from 0 while i is less than the signed dword `[rcx+0x1C]` (re-read each pass), with `e` = qword `[rcx+0x28]` + 0x60 i (inline 0x60-byte entries), copies `e`'s first 64 bytes to a stack copy `t`; with `o` = qword `[e+0x40]` and `v` the 16 bytes at the pointer `o`'s vtable slot `+0x30` returns, calls `o`'s slot `+0x28` with the address of a stack vector (`v`.x times `s`.x / float `[rcx+0x70]`, `v`.y times `s`.y / `[rcx+0x74]`, `v`.z times `s`.z / `[rcx+0x78]`, 0); multiplies x/y/z of `t`+0x30 by `s`, sets its fourth float to 0 and writes all 64 bytes of `t` back to `e` (so `e`+0 to +0x2F get their values from before the two slot calls); when qword `[rcx+0x60]` is non-null calls `o`'s slot `+8` with (&`t`, &stack `a`, &stack `b`) and `008416A0(qword [rcx+0x60], qword [e+0x50], &a stack copy of a and b)`; calls its own vtable slot `+0x78` twice per entry; finally copies the 16 bytes at `rdx` to `rcx+0x70` (stack cookie `01F44830` checked by `00808C40`) | `008330F4`, `00833123`, `0083317F`, `00833204`, `0083322A` |
| `00833830` | 555 B | sets dword `+0xC` of each of the `r9d` 16-byte vectors at `r8` to 0xDD5E0B6B (-1e18 as a float), none when `r9d` is 0 or negative; then for i from 0 while i is less than the signed dword `[rcx+0x84]` (re-read each pass), with the 16-byte point at qword `[rcx+0x90]` + 16i and `s` = (x times float `[rcx+0x20]`, y times `[rcx+0x24]`, z times `[rcx+0x28]`, 0), and for j from 0 while j is less than the sign-extended `r9d`: when the x/y/z dot product of `s` with the 16-byte direction at `rdx+16j` is above float `[r8+16j+0xC]` (a NaN product changes nothing), stores `s` at `r8+16j` and that product at its float `+0xC` | `00833860`, `008338AE`, `00833920`, `00833927`, `00833A20` |
| `00833FB0` | 525 B | calls `00830B40(rcx, rdx, r8)`; with `s` = `r8`, copies dwords `[rcx+0x30]` to `[rcx+0x3C]` into `[rdx+0x20]` to `[rdx+0x2C]`, dwords `[rcx+0x20]` to `[rcx+0x2C]` into `[rdx+0x10]` to `[rdx+0x1C]`, dword `[rcx+0x40]` into `[rdx+0x30]` and `n` = dword `[rcx+0x84]` into `[rdx+0x48]`; stores at qword `[rdx+0x38]` `s`'s slot `+0x30` result for qword `[rcx+0x90]` (0 when `n` is 0) and zeroes qword `[rdx+0x40]`; when `n` is non-zero takes `c` = `s`'s slot `+0x18` with (0x10, `n`), copies the `n` 16-byte points (none when `n` is negative) from qword `[rcx+0x90]` (re-read every 16 bytes) to qword `[c+8]`, and calls `s`'s slot `+0x20` with (`c`, `01CCDA18` "btVector3FloatData", 0x59415241, qword `[rcx+0x90]`); returns `01CCDA30` ("btConvexHullShapeData") | `00833FD3`, `0083402B`, `00834051`, `0083408F`, `00834197` |
| `0083DE00` | 573 B | with `w` = its own vtable slot `+0x18` result (called again at each use; only gate calls are null-tested): when `w` is non-null and `w`'s slot `+0x58` result has bit `0x8` set, for each i < the signed slot `+0x40` result (read once) of `q` = qword `[rcx+0x28]`, takes `m` = `q`'s slot `+0x48` result for i and, for each k < the signed dword `[m+0x4A0]` (read once), calls `w`'s slot `+0x38` with (`m+0x30+0x120k`, `m+0x50+0x120k`, float `[m+0x60+0x120k]`, dword `[m+0xA8+0x120k]`, &a once-zeroed stack vector); then, when `w` is non-null with bit `0x1` or `0x2` in that slot `+0x58` result, for each of the signed dword `[rcx+0xC]` (re-read) pointers `o` in the pointer array at qword `[rcx+0x18]` whose byte `+0xE8` lacks bit `0x20`: when `w` has bit `0x1`, calls its own slot `+0x28` with (`o+0x10`, qword `[o+0xD0]`, &a stack copy of the 16-byte constant dword `[o+0xF4]` picks: 1 `00D11570`, 2 `008C5F90`, 3 `01CCE8B0`, 5 `00D63910`, any other `008C5F80`); when `g` = qword `[rcx+0x80]` is non-null with bit `0x2` in its slot `+0x58` result, calls slot `+8` of qword `[o+0xD0]` with (`o+0x10`, &stack `a`, &stack `b`) and `g`'s slot `+0x60` with (&`a`, &`b`, &a stack copy of `008C5F80`) | `0083DE31`, `0083DE79`, `0083DEBC`, `0083DFBF`, `0083E018` |
| `008521C0` | 531 B | returns 1 when the four floats at `rdx` equal floats `[rcx+0x130]` to `[rcx+0x13C]` (ordered compares, so any NaN differs); otherwise returns 1 when, for some i less than the signed dword `[rcx]`, the squared distance from the x/y/z floats at `rdx` to the 16-byte point at `rcx+0x10+16i` is at most float `[rcx+0x140]` (a NaN distance does not count), else 0 | `008521E0`, `00852263`, `00852364`, `0085237C`, `008523C6` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-vtable-method-index-ee-1003-7)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-vtable-method-index-ee-1003-7/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00785C90` | 575 B | with `a` = `rdx`, `b` = `r9`: if both are non-null, calls `a`'s slot `+0x38` with &stack `t`, `t`'s slot `+0x10` if non-null, and drops `b`; calls slot `+0x10` of non-null qwords `+0x110`, `+0x118`, `+0x120`, nulling them; with `b` sets dword `+0x14` = 2 and calls `00784810(rcx+0x40, b)`, else 1 and `00784D70(rcx+0x40, a)`; calls `0078A970(rcx+0xB0, rcx+0x40)`; dword `+0x24` = `f` (1 for bit `0x20` of dword `+0x58`, +2 for `0x40`); calls `0078AB60(rcx)`; stores `a` at `+0x110` (slot `+8` if non-null) and, only when non-null, `b` at `+0x38` (slot `+8`); if dword `+0x14` (re-read) is not 2, zeroes `+0x118`/`+0x120`, calls `a`'s slot `+0x38` with `rcx+0x38` (no null test), and for dword `+0x70` 1 or 2 copies `+0x110` to `+0x118` or `+0x120` and calls its slot `+8`; if `f` has bit `0x1`: `007853F0(rcx)`, `r` = own slot `+0x48`(0, `rcx`); a negative `r` calls `006DF480(00DACF20, 0xFE4)`, `006DF480(00DACF70, r, 0071B3C0(r))` (if `01F3BA80`, `01F3BA90` are 1+), own slot `+8`, `006DF480(00DACFC0, 0xFF6)`, `006DF480(00DACFF0)` (if `01F3BA80`, `02EA0B40` are 1+); stores the sixth-argument dword at `+0x28`, AND ~0x300 if bit `0x800` of dword `+0x24` (re-read) is set; returns `r`, else 0 | `00785CC8`, `00785D44`, `00785D8B`, `00785DD5`, `00785E24` |
| `007861A0` | 603 B | returns 0x80070057 when `r8d` is -1; when `rdx` is not `rcx`: for each of dwords `+0xB8`, `+0xBC`, `+0xC0`, `+0xC4` that differs between them, calls `006DF480(f, line)` and `006DF480(g, the rdx dword, the rcx dword)` when dwords `01F3BA80` and `01F3BA90` are both at least 1 (lines 0x56C, 0x572, 0x578, 0x57E with (f, g) = (`00DACA50`, `00DACAA0`), (`00DACB10`, `00DACB60`), (`00DACBD0`, `00DACC20`), (`00DACCA0`, `00DACCF0`)), and then returns 0x80070057 if any differs; otherwise takes `r` = `00785650(rdx, r8d, rcx)`, inserts a node holding (`r8d`, `rdx`) before the head of the list at qword `[rcx+0x100]` through `00786900(rcx+0x100, head, qword [head+8], &the stack pair)` and increments the count qword `[rcx+0x108]` (only when the count equals 0x07FFFFFFFFFFFFFE, tested after the `00786900` call and before the head links are written, it calls `std::_Xlength_error` (`008C2618`) with `00DA6D68` "list<T> too long"), stores `rcx` at qword `[qword [rdx+0xF0] + 8*r8d]`, then calls `rcx`'s vtable slot `+0` when `rcx` differs from `rdx`, else stores `r8d` at dword `[rcx+0xF8]`; returns `r` | `007861B4`, `007861F8`, `00786353`, `0078637D`, `007863D8` |
| `00790160` | 585 B | with `p` = `rdx` and the pointer array `v` = `r8`: returns 0x80070057 when exactly one of `p` and `v` is null; the range is the sixth-argument dword `s` and seventh-argument dword `n` when `p` is non-null, else 0 and 0x20; returns 0x80004005 when some object `v[i]` in the range has byte `+0xC4` non-zero (no null test), first calling `006DF480(00E1FA40, 0x2745)` and `006DF480(00E1FA90, i)` when dwords `01F3BA80` and `01F3BA90` are both at least 1; calls vtable slot `+0x88` of the object `d` at qword `[rcx+0x78]` with qword `[p+0xB8]` (0 when `p` is null); for each i from `s` while i is below `s` + `n` (unsigned 32-bit) fills index i of three 32-entry stack arrays, with no bound check against 32: qword `[qword [v[i]+0xB8] + 8*dword [v[i]+0xC0]]` (0 when `v` or `v[i]` is null), dword i of the fifth-argument array and dword i of the `r9` array (each 0 when its array is null); calls `d`'s slot `+0x90` with (`s`, `n`, the three arrays) and returns 0 (stack cookie `01F44830` checked by `00808C40`) | `00790196`, `007901F3`, `0079021F`, `007902A3`, `00790392` |
| `007A1A50` | 632 B | with `o` = qword `[rcx+0x28]` (returns when null), calls `00861EC0(B, 0, 0x110)` on stack `B`; when `o`'s slot `+0xC8` result is negative, calls `o`'s slot `+0x38` until it stops returning 0x8007001E and returns; calls slot `+0x28` of qword `[02EA5370]` with `rcx+0x1D4`: a 0 result with byte `[rcx+0xA9]` clear calls `005CDAA0(2, 01CB37D8, 0079CEC0(rcx))` and sets the byte, a non-zero result with it set calls `005CDAA0(2, 01CB3818, 0079CEC0(rcx))` and clears it; returns when `o`'s slot `+0x48` with (0x110, `B`) is negative; copies dwords `B+0`, `+4`, `+8`, `+0x14` to `[rcx+0x414]`, `+0x420`, `+0x418`, `+0x424`; stores bit `0x80` of bytes `B+0x30` to `+0x40` as 0/1 bytes at `+0x43C` to `+0x44C` and that of byte `B+0x3D` at `+0x444`; zeroes dword `+0x448` and sets its bytes by dword `B+0x20`: 0 `+0x448`; 0x1194 `+0x448`, `+0x449`; 0x2328 `+0x449`; 0x34BC `+0x449`, `+0x44A`; 0x4650 `+0x44A`; 0x57E4 `+0x44A`, `+0x44B`; 0x6978 `+0x44B`; 0x7B0C `+0x448`, `+0x44B`; when qwords `[rcx+0x1E4]` / `[rcx+0x1EC]` equal qwords `01F40398` / `01F403A0`, stores those bits of bytes `B+0x30` to `+0x33` at `+0x43F` down to `+0x43C`; calls `007A15A0(rcx)` (stack cookie `01F44830` checked by `00808C40`) | `007A1A8C`, `007A1A97`, `007A1ADB`, `007A1B4B`, `007A1CA2` |
| `007D1A10` | 616 B | for k = 0 to 2, when byte `[rcx+0x58+0x30k]` is non-zero adds the float `xmm1` to float `[rcx+0x48+0x30k]`, clamping at float `[rcx+0x4C+0x30k]` and clearing the byte, else keeping it 1 (NaN included); calls its own vtable slot `+0x40` and returns 0 when byte k=0 or k=1 was set on entry, or k=2 was and dword `[rcx+0x18]` is 5 to 7; else returns 0 when byte `[rcx+0x30]` is zero; otherwise clears it and copies `m` = dword `[rcx+0x1C]` to `+0x18`; `m` = 1 or 2: float `+0x44` = `007AED00()` as float times `01CEBB70` (0.5), or 1.0; zeroes `+0x40`, `+0x48`, `+0x4C`, `+0x54`, `+0x5C`, `+0x70`, `+0x78`, `+0x7C`, `+0x84`, `+0x8C`, bytes `+0x58`, `+0x88`; float `+0x74` = 0x3FB4FDF4; calls `007CA560(rcx+0x38, float [rcx+0x20], float [rcx+0x2C], 5 or 4, 0)` and `007CA560(rcx+0x68, float [rcx+0x24], float [rcx+0x2C], 0, 0)`; `m` = 5 to 7: floats `+0x44` / `+0x74` = `+0x20` / `+0x24`, the same zeroes plus `+0xA0`, `+0xA8`, `+0xAC`, `+0xB4`, `+0xBC`, byte `+0xB8`, float `+0xA4` = 1.0, then `007CA560(rcx+0x98, float [rcx+0x28], float [rcx+0x2C], 0, 0)`; any `m` then zeroes the 0x80 bytes at `+0xF0`, calls own slot `+0x40`, returns 0 | `007D1A28`, `007D1AD1`, `007D1BA6`, `007D1C07`, `007D1C68` |
| `00834D50` | 659 B | with axis `a` = dword `[rcx+0x50]` and `r` = float `[rcx+0x30+4*((a+2) signed-remainder 3)]` (`a` a signed dword, with no range check), builds `e` = (`r`, `r`, `r`) with `r` + float `[rcx+0x30+4a]` on axis `a`, then adds the results of three calls to its own vtable slot `+0x50` to the z, y and x of `e` in call order; with the transform at `rdx` (rows `+0`, `+0x10`, `+0x20`, origin `+0x30`), takes for each row i the extent `x_i` = the absolute values of the row's three floats dotted with `e`, and writes (origin x - `x_0`, origin y - `x_1`, origin z - `x_2`, 0) to `[r8]` and the same with + to `[r9]` | `00834DC2`, `00834DEB`, `00834E3D`, `00834FD3`, `00834FD7` |
| `00835000` | 653 B | zeroes the 16 bytes at `rdx`; with `v` = the x/y/z floats at `r8` normalised by 1 / `00861F14`(their squared length), or (1, 0, 0) when that is below `01CEBB60` (0.0001); with axis `a` = dword `[rcx+0x50]`, `r` = float `[rcx+0x30+4*((a+2) signed-remainder 3)]` (no range check on `a`) and `h` = float `[rcx+0x30+4a]`: for `s` = `h` and then -`h` (`a` and `h`, not `r`, re-read after the first slot `+0x50` call), takes `m` = its own vtable slot `+0x50` result and the point `c` whose component j is `v`.j times float `[rcx+0x20+4j]` times `r`, plus `s` on axis `a`, minus `v`.j times `m` (fourth float 0), and stores `c` at `[rdx]` when `c`.`v` is above the best value so far (starting at `01CCD4E4`, -1e18 as a float; a NaN value changes nothing); returns `rdx` | `00835081`, `0083509A`, `008350FC`, `00835186`, `0083525B` |
| `00847980` | 630 B | with `n` = the x/y/z floats of the stack vector passed to `00847710(rcx, &vector)`, `p` = the x/y/z floats at `rdx` and `t` = the float `xmm2`: returns 0 when `n`.`p` - `n`.(floats `[rcx+0x50]`, `[rcx+0x54]`, `[rcx+0x58]`) is below -`t` or above `t` (NaN returns 0); otherwise for each edge k from 0 to 2 calls its own vtable slot `+0xB0` with (k, &stack `a`, &stack `b`), takes `m` = (`b` - `a`) cross `n` scaled by 1 / `00861F14`(the squared length of `m`), and returns 0 when `m`.`p` - `m`.`a` is below -`t` (a NaN value does not return); returns 1 after the three edges | `008479BB`, `00847A2A`, `00847A92`, `00847B18`, `00847B7B` |
| `00848960` | 636 B | increments dword `02EAF390`; with `a` / `b` the objects at `rdx` / `r8` ordered so that `a` has the smaller signed dword `+0x18` (`rdx` when equal), hashes (`b`'s id << 16) OR `a`'s id with a shift/xor/add integer hash masked by dword `[rcx+0x10]` - 1 and walks that bucket's chain (heads in the dword array at qword `[rcx+0x48]`, next links in the dword array at qword `[rcx+0x68]`, -1 ending it) over the 32-byte pairs at qword `[rcx+0x18]` for the pair whose qword `+0` object has `a`'s id and qword `+8` object `b`'s; returns 0 when there is none; otherwise calls its own vtable slot `+0x38` with (the pair, `r9`), keeps qword `[pair+0x18]`, unlinks the pair's index `p` from its chain (the predecessor search follows next links until it meets `p`, with no -1 stop), calls slot `+0x10` of the object at qword `[rcx+0x78]` with (`a`, `b`, `r9`) when that is non-null, and, when `p` is not the last index (dword `[rcx+0xC]` - 1), unlinks the last pair from its chain the same way, moves its 32 bytes to index `p` and links `p` at the head of that chain; decrements dword `[rcx+0xC]` and returns the kept qword | `00848987`, `008489E7`, `00848A67`, `00848AE6`, `00848B93` |
| `00848C30` | 602 B | copies the dword `[rcx+0xC]` 32-byte entries at qword `[rcx+0x18]` into a growable stack array (count, capacity, data, owner byte 1; when full the capacity doubles (1 for 0) through `0085E680(capacity*32, 0x10)`, the entries move over and the old data goes to `0085E710` when non-null and owned; a store whose slot address is null is skipped); calls its own vtable slot `+0x10` with (entry qword `+0`, entry qword `+8`, `rdx`) for each copied entry; sets each of the dword `[rcx+0x5C]` dwords at qword `[rcx+0x68]` to -1; when there are 2 or more entries calls `00838060(&the stack array header, a stack byte, 0, count - 1)`; then calls its own slot `+8` with (entry qword `+0`, entry qword `+8`) for each entry in the array's order; finally passes the array data to `0085E710` when non-null and owned | `00848C87`, `00848CB7`, `00848DC2`, `00848DF4`, `00848E23` |
| `0084A740` | 659 B | with `p` = `rdx` and `B` = a stack copy of the 16-byte `lo` = `[r8]` and `hi` = `[r9]`: if dword `[p+0x58]` is 2, calls `00841530(rcx+0x48, qword [p+0x40])` and stores `008410B0(rcx+8, &B, p)` at qword `[p+0x40]` (a change); else increments dword `[rcx+0xC4]` and, with `l` = qword `[p+0x40]`: if on x, y or z `hi` is below `l`'s min `+0` or `l`'s max `+0x10` below `lo`, calls `008416A0(rcx+8, l, &B)` (a change); else calls `00841720(rcx+8, l, &B, &v, 0.05 (008F30E8))` with `v` = (`p`'s max `+0x30` - min `+0x20`) times 0.5 times float `[rcx+0xA8]` per x/y/z, negated where `lo` is below `p`'s min, w 0 (a change if it returns non-zero); these two changes increment dword `[rcx+0xC8]`; then unlinks `p` (prev qword `+0x48`, next `+0x50`, head qword `[rcx+0x88+8*dword [p+0x58]]`), copies `lo`/`hi` to `p+0x20`/`p+0x30`, sets dword `[p+0x58]` = dword `[rcx+0xAC]` and pushes `p` onto that list's front; after a change sets byte `[rcx+0xDE]` = 1 and, if byte `[rcx+0xDD]` is zero, calls `00848E90(rcx+0x48, qword [rcx+0x48], qword [p+0x40], &stack rcx)` and `00848E90(rcx+8, qword [rcx+8], qword [p+0x40], &stack rcx)` | `0084A786`, `0084A79A`, `0084A7B2`, `0084A8C8`, `0084A9AF` |
| `00857970` | 659 B | with `dt` = `xmm1`, for each of the dword `[rcx+0x124]` bodies `b` in the pointer array at qword `[rcx+0x130]`: sets float `[b+0x110]` = 1.0; skips `b` when dword `[b+0xF4]` is 2 or 5 or byte `[b+0xE8]` has bit `0x1` or `0x2`; calls `00853AE0(b, dt, &a stack transform T)`; when float `[b+0x118]` squared is non-zero, the squared distance from `b`'s 16 bytes `+0x40` to `T`'s origin is above it, and dword `[qword [b+0xD0] + 8]` is less than 0x14 (signed): increments dword `02EAF3C8`, builds a stack result object (vtable `01CCF768`, fraction 1.0, words from `[qword [b+0xC8] + 8]` and `+0xA`, both origins, `b`, the slot `+0x48` result of the object at qword `[rcx+0x78]`, qword `[rcx+0x28]`) and a stack shape (`00831990`, then vtable `00D7AA18`, dword `+8` = 8, floats `+0x30` / `+0x40` = float `[b+0x114]`), calls `0083B580(rcx, &shape, b+0x10, &T, &result, 0.0)`, and when the fraction is below 1.0 stores it at float `[b+0x110]`, calls `00853AE0(b, dt times it, &T)` and zeroes float `[b+0x110]`; then stores vtable `00D7A770` in the shape and calls `00830C40(&shape)`; calls `00853B10(b, &T)` for every body not skipped (stack cookie `01F44830` checked by `00808C40`) | `008579FB`, `00857A34`, `00857A86`, `00857B68`, `00857BB0` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-vtable-method-index-ee-1003-8)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-vtable-method-index-ee-1003-8/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `006007B0` | 678 B | returns 0x16 if bit `0x1` of byte `[rcx+8]` is set, 0x15 if `k` = qword `[rcx+0x80]` is null; counts are dwords AND 0x7FFFFFFF; `e` = qword `[qword [rdx+0x30] + 8 dword [k+0x18]]` if that index < (unsigned) count `[rdx+0x28]`, else or if null the 0x50-byte entry of the count `[rdx+0x18]` at qword `[rdx+0x20]` whose qword `+0` is `k`; returns 7 if `e` is null or count `[e+8]` is 0; `c` = qword `[e+0x10]`; if qword `02CB6360` and `00606C60([02CB6360], e, c)` are non-null, atomically increments its dword; calls `0060F830(rcx, rdx, c, r8, &A, &L)` (zeroed stack, `A` 4 qwords); for each of the `n` = count `[c+8]` 0x2C0-byte entries at qword `[c+0x10]` with qword `+0x18` non-zero, takes a 0x80-byte ring slot (cursor `[rcx+0x60]`, end `+0x58`, wrap `+0x50`, null if still over; first kept at `+0x88`, slot+0x80 at `+0x90`) and, untested, writes 3, `rdx`, the entry, `A`, `L`, `r9d`, 5th, 6th args at `+0`, `+8`, `+0x10`, `+0x18`, `+0x38`, `+0x40`, `+0x44`, `+0x48`; then from `L+8` writes `A[0]`+4 if `A[0]` is non-null, advances the end to `005F08E0(A[1], A[1]+0x10, end)` if `A[1]` is non-null, sets dword `[L]` to the count and atomically adds `n` to each written pointer's dword; returns 0 | `006007CF`, `0060087D`, `006008C7`, `0060098A`, `00600A29` |
| `00654830` | 706 B | when byte `01F2CDF0` is zero calls vtable slot `+8` of the static object `01F2D680`; calls `00649070`, `006488A0` and `00648C70`; then, for each static X below in order, calls `006388C0(X)` followed by `00639450(X)`: `02D35EA0`, then calls `00648E10`; `02D356A0`, then `00648FB0`; `02D35300`, then `006496A0`, `00648620`, `00648100` and `006491B0`; then `02D35BA0`, `02D34A40`, `02D34D40`, `02D360A0`, `02D35DA0`, `02D358A0`, `02D35040`, `02D35500`, `02D366A0`, `02D363A0`, `02D369A0`, `02D34940`, `02D34C40`, `02D35FA0`, `02D35CA0`, `02D357A0`, `02D34F40`, `02D35400`, `02D365A0`, `02D362A0`, `02D368A0`, `02D36AA0` and `02D36BA0`; returns 0 | `0065484B`, `00654864`, `00654870`, `006548B9`, `00654AE6` |
| `006BAB40` | 675 B | returns 7 when `n` = dword `[rcx+0x10]` or dword `[rcx+0x24]` is 0; takes `p` = `00210EC0(8n + 8)` (the size saturates to -1 on overflow) and, when `p` is non-null, stores `n` in its first qword and calls `00808FE4(p+8, 8, n, 006BA870, 005DDAF0)`, storing `p+8` (null when `p` is null) at qword `[rcx+0x30]`; for each i below `n` (unsigned) calls `0019C5D0(a 0x100-byte stack buffer, 0x100, 00D81240, i)` and returns the first non-zero of `005C5230(e, buffer, 0x2000)` and `005C5230(01F2ED08, e)` with `e` = qword `[rcx+0x30]` + 8i; stores `a` = `0017D260(48n, 8)` at qword `[rcx+0x98]` (returning 0xD when null) and `a` + 24n at `+0xA0`, calls `00861EC0(a, 0, 48n)` and stores `e` at qwords `[a+24i]` and `[a+24n+24i]`; calls `005CD160(rcx+k, 0, n)` and sets byte `[rcx+k+8]` = 1 for k = 0x58, 0x68, 0x38, 0x48 in that order; stores `0017D260(8 times dword [rcx+0x24], 8)` at qword `+0x80` (returning 0xD when null) and zeroes its qwords; sets word `+0x90` = 0x101 and returns `006AA3A0(rcx, dword 01F2EB34, dword 01F2EB38)` (stack cookie `01F44830` checked by `00808C40`) | `006BAB65`, `006BABAE`, `006BABDD`, `006BAC35`, `006BADAD` |
| `007A1790` | 695 B | with `o` = qword `[rcx+0x28]` (returns when null) and a zeroed 20-byte stack record `S`: when slot `+0x48` of qword `[o+8]` with (0x14, &`S`) is negative, calls its slot `+0x38` until that stops returning 0x8007001E and returns; when byte `[rcx+0x1E6]` is 1: with `h` = qword `02EA5248`, skips to the end step unless `GetCursorPos` (`008C28B0`)(&`P`), `GetWindowRect` (`008C28D0`)(`h`, &stack) and `GetClientRect` (`008C29A0`)(`h`, &`R`) all return non-zero; calls `GetWindowInfo` (`008C2828`)(`h`, &stack) and `ScreenToClient` (`008C2898`)(`h`, &`P`); stores each of `P`.x, `P`.y, dword `S+8` times 0xFF (32-bit) at dwords `+0x1E8`, `+0x1EC`, `+0x1F0`; when 0 <= `P`.x < `R`.right - `R`.left and 0 <= `P`.y < `R`.bottom - `R`.top (signed) and byte `[o]` is 1, stores bit `0x80` of bytes `S+0xC`, `S+0xE`, `S+0xD` as 0/1 bytes `+0x1F4`, `+0x1F5`, `+0x1F6`; otherwise updates only those of the three that are non-zero; sets byte `[o]` to 1 inside, 0 outside; when byte `+0x1E6` is not 1 stores each of dwords `S+0`, `S+4`, `S+8` times 0xFF and the three bits directly; end step: zeroes bytes `+0x1F4` to `+0x1F6` when byte `02EA523D` is non-zero and calls `007A15A0(rcx)` | `007A17E2`, `007A182F`, `007A188F`, `007A18E8`, `007A1A21` |
| `007A2140` | 760 B | `GetVersionExA` (`008C2288`) on a 0x94-byte stack record: if dwords `+0x10`, `+4`, `+8` are 2, 6, 1, calls `00799A80()` if byte `02EA5379` is non-zero, returns if byte `01F3DA04` is zero; with `u` = dword `[rcx+0x458]` and a zeroed 16-byte stack `S`, `r` = `XInputGetState` (`00861EA2`)(`u`, &`S`); calls `XInputSetState` (`00861EA8`)(`u`, &words (byte `[rcx+0x98]`/255 times 65535, 65535 if byte `[rcx+0x99]` is non-zero else 0)); if `GetForegroundWindow` (`008C2800`) is not qword `02EA5248` clears byte `02EA5213` and returns, else sets it to 1; if dword `S+0` differs from dword `[rcx+0x45C]`: `r` non-zero, byte `[rcx+0xA9]` set: calls `005CDAA0(2, 01CB3890, 0079CEC0(rcx), u)` and clears it; `r` = 0 with it clear calls that with `01CB3858` and sets it, and `r` = 0 stores signed words `S+8`, `+0xA`, `+0xC`, `+0xE` / 128 (to zero) at `+0x414`, `+0x420` (negated), `+0x418`, `+0x424` (negated), bits `0x4000`, `0x1000`, `0x2000`, `0x8000`, `0x100`, `0x200` of word `S+4` at bytes `+0x43C`..`+0x441`, bytes `S+6`/`S+7` non-zero at `+0x442`/`+0x443`, bits `0x20`, `0x10`, `0x40`, `0x80`, `0x1`, `0x8`, `0x2`, `0x4` at `+0x444`..`+0x44B`; then copies `S` to `rcx+0x45C` and calls `007A15A0(rcx)` | `007A216B`, `007A21C0`, `007A2229`, `007A2280`, `007A2409` |
| `007D5BD0` | 671 B | a float setter keyed by `edx` 0 to 0x34 (unsigned) through the jump table at image base + `0x6B5E70`, with value `xmm2` and time `xmm3`; most keys call `007CA560(record, value, time, 0, a stack byte 0)`: keys 0, 1, 2 on `rcx+0x18`, `+0x48`, `+0x78`; 4 on `+0x168`; 5 on `+0x198` with max(value, 1.0); 6 on `+0x1C8` with `007AED00()` as float times the value times `008C5B2C` (0.001), replaced by `01CB75A8` (23999) when not below `01CB75AC` (24000; NaN is kept); 7 on `+0x1F8`; 8 on `+0xA8` with max(value, `008F8180` 10.0); 9 on `+0xD8` with min(value, `008F3110` 0.99) (for max and min a NaN value gives the bound); 10 and 11 on `+0x108` and `+0x138`; keys 13 to 31 except 16, 20, 24, 28, then 34 to 52 except 37, 41, 45, 49, in that order, on the 30 records `rcx+0x228+0x30j`; key 3 stores the 32-bit truncated value at dword `+0x7C8` and key 32 the low dword of its 64-bit truncation at dword `+0x7CC`; keys 12, 16, 20, 24, 28, 33, 37, 41, 45, 49 and keys above 0x34 do nothing | `007D5BFB`, `007D5C19`, `007D5CBB`, `007D5C32`, `007D5E59` |
| `007E96A0` | 704 B | returns `007E8890(rcx, rdx)` if negative; `a` = `007BD8D0(007E71C0(007E8720(rcx)))`, `f` = qword `[rcx+0x20]`, `w` = word `[f+6]` read now; calls `a`'s slot `+0x28` with &stack `S` and `007CF580(&S)`; if word `+0xA` of qword `[result+8]` differs from `w`, `a` = `007B2200(word [f+6])` (re-read); if `a`'s slot `+8` returns 2, `x` = `007E3040(a, word [f+4])`: a null `x` runs `0019C5D0(0x100-byte stack B,0x100, 01CB9150, word [f+4], byte [a+0x94], dword [a+0x80], dword [a+0x48])`, writes 0xA unchecked at B[k] (k = its result, minus 2 when >= 0xFF, signed), then 0 at B[k+1], or calls `00809728` when k+1 >= 0x100; then `OutputDebugStringA` (`008C2120`)(B), `007A5570(2, B)`, `007E8B40(rcx)`, the same format/newline/output for `01CB91B0` (no arguments), returns -1; else `h` = qword `[007E3150(x, &S) + 8]`; for other results `h` = qword `[007CF860(007CF8B0(a's slot +0x28 result for &stack T, &stack U), &S, word [f+4]) + 8]`, `S`/`U` get vtables `01CB4E78`/`01CB5D28`, `007CF580(&T)` runs; then `S` gets vtable `01CB4E88` and `h` at `+8`, `r` = `007B5D20(rcx+0x3C8, &copy of qword [rcx+8], &copy of qword [a+0x10], &S, float [rdx+0x20], 1)`; a negative `r` calls `007E8B40(rcx)`; returns `r` | `007E96C9`, `007E9725`, `007E976F`, `007E980C`, `007E9910` |
| `00833CD0` | 733 B | zeroes the 16 bytes at `rdx`; for each of the dword `[rcx+0x84]` 16-byte points at qword `[rcx+0x90]`, with `s` = (x times float `[rcx+0x20]`, y times `[rcx+0x24]`, z times `[rcx+0x28]`, 0), stores `s` at `[rdx]` and keeps its product as the best when the x/y/z dot product of `s` with the floats at `r8` is above the best so far (starting at `01CCD4E4`, -1e18 as a float; a NaN product changes nothing); returns `rdx` | `00833D04`, `00833DB8`, `00833DC4`, `00833F6E`, `00833F7A` |
| `00834970` | 758 B | with `r` = float `[rcx+0x30+4q]`, `q` = (a+2) % 3 as a signed 32-bit remainder (division truncating toward zero, negative when a+2 < 0), for axis `a` = dword `[rcx+0x50]` read once at entry: for each j below `r9d` (signed), with `v` = the x/y/z floats of the 16-byte direction at `rdx+16j`, and for `s` = `h` and then -`h` (`h` = float `[rcx+0x30+4a]` with `a` re-read each time), takes `m` = its own vtable slot `+0x50` result and the point `c` whose component k is `v`.k times float `[rcx+0x20+4k]` times `r`, plus `s` on axis `a`, minus `v`.k times `m` (fourth float 0), and stores `c` at `r8+16j` when `c`.`v` is above the best for that j (starting at `01CCD4E4`, -1e18 as a float; a NaN value changes nothing) | `008349BC`, `00834A56`, `00834AFE`, `00834B3C`, `00834BEC` |
| `00837120` | 683 B | with mesh `m` = qword `[rcx+8]`, part `edx` and triangle `r8d`: calls `m`'s vtable slot `+0x18` with (&`vb`, &an unread slot, &`t`, &`st`, &`ib`, &`is`, &an unread slot, &`it`, `edx`) on stack slots; with `m` re-read, at the index record `ib` + `is` times `r8d` (32-bit product) takes three indices, words `+4`, `+2`, `+0` when `it` is 3, else dwords `+8`, `+4`, `+0`, and for each the vertex at `vb` + index times `st` (32-bit product): three floats when `t` is 0, else three doubles converted to float, times floats `[m+0x10]`, `[m+0x14]`, `[m+0x18]`, fourth float 0, stored at `rcx+0x40`, `rcx+0x30` and `rcx+0x20` in that order; then calls slot `+8` of the object at qword `[rcx+0x10]` with (`rcx+0x20`, `edx`, `r8d`) and slot `+0x28` of qword `[rcx+8]` (re-read) with `edx` | `00837181`, `0083719C`, `008371C5`, `00837209`, `008373A8` |
| `0083A070` | 700 B | with `s` = `r8`: copies dwords `[rcx+0x10]` to `[rcx+0xBC]` into `[rdx+0x20]` to `[rdx+0xCC]`, dword `[rcx+0xC0]` into `[rdx+0xEC]` and `[rcx+0xC4]` into `[rdx+0xD0]`; zeroes qwords `[rdx]` and `[rdx+0x10]` and stores `s`'s slot `+0x30` result for qword `[rcx+0xD0]` at `[rdx+8]`; copies dwords `[rcx+0xE8]` to `[rcx+0xF4]` into `[rdx+0xF0]` to `[rdx+0xFC]` (`+0xF4` twice), `[rcx+0xF8]` / `+0xFC` / `+0x100` into `[rdx+0xD4]` / `+0xD8` / `+0xDC` and `[rcx+0x104]` into `[rdx+0x100]`; with `q` = `s`'s slot `+0x48` result for `rcx`, stores `s`'s slot `+0x30` result for `q` at qword `[rdx+0x18]` and, when that is non-null, calls `s`'s slot `+0x58` with `q`; copies dwords `[rcx+0x110]` / `+0x114` / `+0x118` (twice) / `+0x11C` into `[rdx+0xE0]` / `+0xE4` / `+0xE8` / `+0x104`; returns `01CCE3D8` ("btCollisionObjectFloatData") | `0083A08A`, `0083A209`, `0083A22B`, `0083A2AB`, `0083A2D0` |
| `00853C90` | 736 B | calls `0083A070(rcx, rdx, r8)`; then copies dwords `[rcx+0x120]` to `[rcx+0x16C]` into `[rdx+0x108]` to `[rdx+0x154]`, `[rcx+0x170]` into `[rdx+0x1C8]`, `[rcx+0x260]` to `[rcx+0x26C]` into `[rdx+0x158]` to `[rdx+0x164]`, `[rcx+0x180]` to `[rcx+0x1DC]` into `[rdx+0x168]` to `[rdx+0x1C4]`, `[rcx+0x1E0]` / `+0x1E4` into `[rdx+0x1CC]` / `+0x1D0`, byte `[rcx+0x1E8]` zero-extended into dword `[rdx+0x1EC]`, and `[rcx+0x1EC]` to `[rcx+0x200]` into `[rdx+0x1D4]` to `[rdx+0x1E8]`; returns `01CCF378` ("btRigidBodyFloatData") | `00853CA0`, `00853D9B`, `00853DA7`, `00853F10`, `00853F5D` |
| `008585E0` | 697 B | with `n` = dword `[rcx+0x104]`, makes a stack pointer array `C` (count, capacity, data, owner byte 1) holding `n` null entries when `n` is positive (data from `0085E680(8n, 0x10)`; a store at a null address is skipped), its count set to `n` even when negative; for each i below its own vtable slot `+0xB8` result (re-called each step) copies qword i of the array at qword `[rcx+0x110]` into it, with no bound against `n`; when the count is greater than 1 (signed) calls `00854830(&C's header, its unwritten rcx home-slot byte, 0, count - 1)`; builds a stack object `K` (vtable `01CCF750`, `rdx`, qword `[rcx+0xF0]`, `C`'s data or null when slot `+0xB8` now returns 0, the count, qwords `[rcx+0x80]`, `[rcx+0x70]`, `[rcx+0x28]`, three empty owned arrays); calls slot `+8` of the object at qword `[rcx+0xF0]` with (dword `[rcx+0xC]`, the slot `+0x40` result of qword `[rcx+0x28]`), `0087F410(qword [rcx+0xF8], qword [rcx+0x28], rcx, &K)`, `00857F10(&K)` and slot `+0x18` of qword `[rcx+0xF0]` (re-read) with (`rdx`, qword `[rcx+0x80]`, qword `[rcx+0x70]`); then passes each of `K`'s three array datas and `C`'s data to `0085E710` when non-null and owned, storing vtable `01CCF738` in `K` before `C`'s | `0085863D`, `008586FF`, `00858723`, `008587BD`, `008587F8` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-vtable-method-index-ee-1003-9)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-vtable-method-index-ee-1003-9/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `005DF890` | 906 B | calls `005DF810(rcx, rdx)`; copies the 0x190 bytes at `rdx+0x30` to `rcx+0x30` and, for k from 0 to 7, the 16 bytes at `+0x1C0+0x20k`; with `c` = dword `[rdx+0x1D0+0x20k]` AND 0x7FFFFFFF takes `n` = `005E2FB0(c, qword [rdx+0x1D8+0x20k])`, calls `00584730` on the old qword `[rcx+0x1D8+0x20k]` when it differs from `n`, bit `0x80000000` of dword `[rcx+0x1D0+0x20k]` is clear and it is non-null, then stores `c` at that dword and `n` at that qword; returns `rcx` | `005DF8AA`, `005DF8D2`, `005DF943`, `005DF96C`, `005DFBC7` |
| `00608A40` | 906 B | while byte `01F2CDF0` is zero (re-read before each) calls vtable slot `+8` of the statics `01F2E9B8`, `01F2EE60` and `01F2EE80` in turn; then makes 57 further calls that set up no argument registers (their order is not stated here; the first is `005E6E70`, the last `005E67C0`), interleaved with `006388C0(f())` for f = `005D8BE0`, `006B6B60`, `0062CC80`, `006C0C90`, `006BEAC0`, and with `006388C0(X)` then `00639450(X)` for the 17 statics X = `02CB6480`, `02CB7CA0`, `02CB9A00`, `02CBB900`, `02CBBB00`, `02CBBD00`, `02CB78A0`, `02CB9C00`, `02CBAD00`, `02CBAF00`, `02CBB000`, `02CBB100`, `02CBB200`, `02CB76A0`, `02CBB600`, `02CB6880`, `02CB6980` in that order (between the two calls for `02CB7CA0` and for `02CB9C00` it ORs 0x20 into dwords `02CB7D9C` and `02CB9CFC`); returns when `0062D0D0()`, then `005FD2A0(0x40)`, then `005CD0A0(005FCF20())` is non-zero, else tail-jumps to `005FD560` | `00608A5B`, `00608AA8`, `00608AC5`, `00608D96`, `00608DC0` |
| `0062E1C0` | 978 B | with `a`/`b`/`c` = `xmm1`/`xmm2`/`xmm3`, sets the 4x4 at `rcx+0x38` to rows (1,0,0,0), (0,-1,0,0), (0,0,-1,0), (floats `[rcx+0x28]`, `+0x2C`, `+0x30`, 1.0); with the stack vector (0, -1.0, 0) as `x`: calls `00188E60(&R, a, &x)` on a stack matrix `R` and copies the 64 bytes `00185100(rcx+0x38, &R, &a stack copy of R)` returns into `rcx+0x38`; does that again with the stack matrix rows (1,0,0,0), (0,C,S,0), (0,-S,C,0), (0,0,0,1), S = `sinf` (`00861F0E`)(`b`), C = `cosf` (`00861F08`)(`b`), in place of the copy of `R`; then again with `R` from `00188E60(&R, c, &x)`; finally writes the 3x4 at `rcx+8` as rows (M1.xyz, M0.x), (M2.xyz, M0.y), (M3.xyz, M0.z), Mk being row k of the 4x4 | `0062E290`, `0062E2C8`, `0062E333`, `0062E3A7`, `0062E576` |
| `0062E5A0` | 985 B | sets the 4x4 `M` at `rcx+0x38` from the 3x4 at `rcx+8`: rows (`+0x14`, `+0x24`, `+0x34`, 0), (`+8`, `+0xC`, `+0x10`, 0), (`+0x18`, `+0x1C`, `+0x20`, 0), (`+0x28`, `+0x2C`, `+0x30`, 1.0); with `f` = row 2 times 1/`sqrtf` (`00861F14`) of its squared length, `p` = `asinf` (`00861EFC`)(`f`.y) - `xmm2` and `y` = `atan2f` (`00861F02`)(`f`.x, `f`.z) + `xmm1`, each moved into [0, 2 pi] by adding `01CEBC78` (2 pi) while below 0 and `00915624` (-2 pi) while above 2 pi (NaN skips both loops; an infinity, or any value of magnitude above 2^27 where adding 2 pi rounds back to the same float, never leaves them); sets row 0 = (-cos y, 0, sin y, 0), row 2 = (sin y cos p, sin p, cos y cos p, 0) and row 1 = (sin p sin y, -cos y (cos y cos p) - (sin y cos p) sin y, cos y sin p) times 1/`sqrtf` of its squared length, fourth float 0, keeping row 3 with fourth float 1.0 (`sinf`/`cosf` = `00861F0E`/`00861F08`); then writes the 3x4 at `rcx+8` as rows (M1.xyz, M0.x), (M2.xyz, M0.y), (M3.xyz, M0.z) | `0062E62F`, `0062E6B8`, `0062E6D9`, `0062E710`, `0062E828` |
| `007D5F50` | 795 B | returns -1 when `rdx` is null; otherwise calls its own vtable slot `+0x10` 32 times with (k, value, `xmm3` unchanged) for k = 0 to 0x1F, the values being floats `[rdx]`, `+8`, `+0xC`, dword `+0x78` as float, floats `+0x1C`, `+4`, `+0x24`, `+0x20`, `+0x10`, `+0x14`, `+0x18`, `+0x7C`, dword `+0x28` as float, floats `+0x2C`, `+0x30`, `+0x34`, dword `+0x38` as float, floats `+0x3C`, `+0x40`, `+0x44`, dword `+0x48` as float, floats `+0x4C`, `+0x50`, `+0x54`, dword `+0x58` as float, floats `+0x5C`, `+0x60`, `+0x64`, dword `+0x58` as float again for k = 0x1C (`+0x68` is not read), floats `+0x6C`, `+0x70`, `+0x74`; then calls its own slot `+0x40` and `007D6CD0(rcx)` and returns 0 | `007D5F89`, `007D5FC8`, `007D61FD`, `007D624E`, `007D6254` |
| `007D9200` | 813 B | evaluates ramps at `rcx+0x20+0x30k` (each: end `+4` when duration `+0xC` is 0.0 or NaN, else start `+0` + `007A9E50(elapsed +8 / duration, curve dword +0x14)` times (end - start)): stores ramps k = 0 to 3 at floats `[rcx+0x148]`, `+0x14C`, `+0x150`, `+0x154`; when ramp 4 is above 0 (NaN is not) stores `expf` (`00861FAA`) of `008F3148` (-2.0) / (ramp 4, evaluated again, times float `[rcx+0x138]`) at float `+0x158`, else 0; when ramp 5 is above 0 stores `expf` of `01CEBC9C` (-1.0) / (ramp 5, evaluated again, times float `[rcx+0x138]`) at float `+0x15C`, else 0; takes `p` = `007AC3E0(qword [02EAD0A8], dword [rcx+0x13C], dword [rcx+0x140])` and stores `p` at qword `+0x168` when it is non-null and its vtable slot `+8` returns 4, else 0 | `007D9237`, `007D9394`, `007D93FC`, `007D94BC`, `007D94FD` |
| `00832930` | 869 B | with `c` = 0.5 times (floats `[rcx+0x50]`/`+0x54`/`+0x58` plus `[rcx+0x40]`/`+0x44`/`+0x48`) and `e` = 0.5 times their differences (both zero when dword `[rcx+0x1C]` is 0), adds the results of three calls to its own vtable slot `+0x50` to the z, y and x of `e` in call order; with the transform at `rdx` (rows `+0`, `+0x10`, `+0x20`, origin `+0x30`), takes `w` = for each row i the row's three floats dotted with `c` plus origin component i, and `x` = for each row the absolute values of its three floats dotted with `e`; writes (`w` - `x`, 0) to `[r8]` and (`w` + `x`, 0) to `[r9]` | `00832941`, `00832A28`, `00832A79`, `00832B39`, `00832C89` |
| `008355B0` | 945 B | for each j below `r9d` (signed), with `v` = the 16-byte direction at `rdx+16j`, `r` = float `[rcx+0x30]` and `h` = float `[rcx+0x34]` (both re-read each time), takes `s` = `sqrtf` (`00861F14`)(`v`.x^2 + `v`.z^2) and writes to `r8+16j` the 16 bytes (x, y, z, w): y = `h`, negated when `v`.y is below 0 (not for NaN); when `s` equals 0.0 (ordered), x = `r` and z = 0, otherwise x = `v`.x times `r`/`s` and z = `v`.z times `r`/`s`; w is a stack dword the body never writes | `0083566C`, `00835677`, `00835685`, `00835697`, `008356C0` |
| `00846C20` | 840 B | computes over the three 16-byte points at `rdx` the per-float minimum (starting at `01CCD870`: 1e18 three times, then 0) and maximum (starting at `01CCD880`: -1e18 three times, then 0) of all four floats, a NaN changing neither; appends a 64-byte node to the array at qword `[rcx+8]` (count dword `+4`, capacity `+8`, data qword `+0x10`, owner byte `+0x18`; when the count equals the capacity and twice the count (1 for 0) is larger (signed), `0085E680(64 times that, 0x10)` gets the entries, the old data goes to `0085E710` when non-null and owned, the owner byte becomes 1 and the capacity dword becomes that; a store at a null slot is skipped): the minimum at `+0`, the maximum at `+0x10`, dwords `+0x20` = -1, `+0x24` = `r8d`, `+0x28` = `r9d`, and stack bytes the body never writes at `+0x2C` to `+0x3F`; increments the count | `00846C5D`, `00846D33`, `00846E5B`, `00846E98`, `00846F3B` |
| `00846F70` | 789 B | computes over the three 16-byte points at `rdx` the x/y/z minimum (each starting at `01CCE8AC`, 1e18) and maximum (each starting at `01CCD4E4`, -1e18), a NaN coordinate changing neither; on each axis where max - min is below `009002B0` (0.002) adds `009002EC` (-0.001) to the min and `008C5B2C` (0.001) to the max; with `q` = qword `[rcx+0x10]`, builds a 16-byte node: words `+0`, `+2`, `+4` = truncate((min - float `[q+0x10+4j]`) times float `[q+0x30+4j]`) AND 0xFFFE, words `+6`, `+8`, `+0xA` = truncate((max - float `[q+0x10+4j]`) times float `[q+0x30+4j]` + 1.0) OR 1, dword `+0xC` = (`r8d` << 21) OR `r9d`; appends it to the array at qword `[rcx+8]` (count dword `+4`, capacity `+8`, data qword `+0x10`, owner byte `+0x18`; when the count equals the capacity and twice the count (1 for 0) is larger (signed), `0085E680(16 times that, 0x10)` gets the entries, the old data goes to `0085E710` when non-null and owned, the owner byte becomes 1 and the capacity dword becomes that; a store at a null slot is skipped) and increments the count | `00846F95`, `008470A2`, `0084712C`, `008471EB`, `00847278` |
| `008473A0` | 870 B | for each j below `r9d` (signed), with `v` = the x/y/z floats of the 16-byte direction at `rdx+16j`, dots `v` with the rows at `rcx+0x50`, `+0x60` and `+0x70` (floats `+0`/`+4`/`+8` of each) giving `d0`, `d1`, `d2`, picks row 1 when `d1` > `d0` (then row 2 if `d2` > `d1`), else row 2 when `d2` > `d0`, else row 0 (ties and NaN keep the earlier row), and copies that 16-byte row to `r8+16j` | `008473F0`, `00847458`, `00847474`, `0084747A`, `008476DD` |
