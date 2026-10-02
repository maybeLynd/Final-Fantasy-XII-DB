---
system: PhyreEngine subsystem map
category: 22-Middleware-PhyreEngine
status: DOCUMENTED — how the 6,769 Phyre functions map onto the classes (AQ-2) is SUPERSEDED 2026-09-26 as a population-coverage statement, its population carried by members/phyre-function-class-map.tsv (4,515 placed by vtable evidence, 2,254 without); whether the ~992 non-glue functions are driven or dead-linked (AQ-5) answered 2026-09-18: 973 of 993 reachable from the program's roots, 20 dead-linked. Re-statused 2026-09-29 (OPUS, owner read under FABLE's status-currency ruling, _index/candidates/dd-owner-read-0929)
owner_layer: CodeDomain:Phyre — no PrimaryOwner (middleware)
evidence_tier: 4
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
last_reviewed: 2026-09-02
audit:
  passes: 3
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# PhyreEngine subsystem map

> The largest single block in the image — **6,769 functions, 20 % of the executable** — has **two**
> recovered names. RTTI has 1,604 class names for it, and the ledger says **85 % of it is generated
> reflection and script-binding glue**: only about **993 functions** are engine behaviour.

> **Framing corrected 2026-09-02 — the game is a Phyre *application*, not a Phyre *user*.**
> `GameApplication` derives from `Phyre::PFramework::PApplication` (31 slots, 18 overridden, 13
> inherited), so the middleware owns the loop and calls the game through vtable slots. That is the
> mechanism behind §11's finding that **no documented game subsystem calls Phyre** — the
> measurement is right, and the top-level call direction is Phyre → game. See
> [`../Application-Framework-Boundary/the-game-is-a-phyre-application.md`](../Application-Framework-Boundary/the-game-is-a-phyre-application.md).

~~**PARTIAL, and tier 4 by construction.**~~ **DOCUMENTED, tier 4 by construction.** *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`)* This document reports *identity from RTTI*, not mechanism.
No Phyre function body is read here *(answered: see the AQ-2 and AQ-5 answers, 2026-09-18, which decode bodies; 2026-10-02, OPUS)*. Its value is that it converts "6,769 unexplained functions"
into a named breakdown that later work can attack a piece at a time.

## 1. What the player sees

FFXII: The Zodiac Age is not built on an engine written for FFXII. It is built on **PhyreEngine**,
Sony's middleware, and a fifth of the executable is that middleware. Rendering, animation, physics,
post-processing and the scene graph all come from it — which is why the game's *look* and its
*rules* feel like they were designed by different people. They were.

For a modder this matters practically: a change to how something is **drawn or animated** is a change
to Phyre and may be documented upstream, while a change to how something is **decided** is FFXII's
own code and is not.

## 2. What RTTI says is in there

`rtti_recover.py` recovered ~~**2,133 classes**~~ **2,248 classes** image-wide, of which ~~**1,604 are `Phyre::`**~~ **1,739 are `Phyre::`** *(corrected 2026-10-02, OPUS: `Tools/work/rtti/classes.tsv` has 2,248 rows today and 1,739 `Phyre::` names; an independent walk of the image's complete-object locators finds the same 1,739 `Phyre::` classes; the 2,133 run failed to demangle most names, class-descriptor-and-metadata-system.md §14; the namespace table below is that older run's)*, carrying
**1,714 vtables**.

### The real namespaces, by size

| Namespace | classes | vtables |
|---|---:|---:|
| **`PRendering`** | **422** | 444 |
| **`PAnimation`** | **190** | 217 |
| **`PPhysics`** | **153** | 169 |
| **`PPostProcessing`** | **151** | 153 |
| **`PInputs`** | **139** | 140 |
| **`PGeometry`** | **106** | 108 |
| **`PDynamicGeometry`** | **78** | 78 |
| `PFramework` | 30 | 40 |
| `PScripting` | 24 | 25 |
| `PGameplay` | 21 | 24 |
| `PSerialization` | 17 | 17 |
| `PLOD` | 17 | 18 |
| `PVision` | 14 | 14 |
| `PHierarchy` | 13 | 13 |
| `PText` | 12 | 12 |
| `POccluderGeometry` | 7 | 7 |
| `PScene` | 5 | 14 |
| `PGame` | 4 | 4 |
| `PRandom` | 3 | 3 |
| `PInternal` | 3 | 3 |
| `PProfiling` | 2 | 2 |
| `PDeveloperExtensions` | 1 | 1 |
| *(directly in `Phyre::`)* | 50 | 50 |

**Seven namespaces hold 1,239 of the 1,604 classes.** Rendering alone is a quarter of Phyre.

### The `VP*` classes are the reflected types, not a namespace

A large second group — `VPString`, `VPCamera`, `VPMatrix4`, `VPEntity`, `VPComponent`, `VPWorld`,
`VPNode`, `VPAssetReference`, `VPTimer` and others — are **reflected engine types**, the subjects of
the class-descriptor system already documented in
[`../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md).
Their vtables are dominated by two template families, `?$PMethodCallerConcrete` and
`?$PClassDescriptorForType`, which are **reflection machinery rather than engine behaviour** — a
`PMethodCallerConcrete` with 53 slots is 53 reflected *calls*, not 53 distinct algorithms.

### Named entry points worth knowing

| Class | slots | note |
|---|---:|---|
| `Phyre::PFramework::PApplication` | 31 | the application root |
| `Phyre::PScene::VPNode` | 33 | scene graph node |
| `Phyre::PRendering::VPMeshInstance` | 30 | a drawn mesh |
| `Phyre::PPhysics::VPPhysicsWorld` | 24 | the physics world |
| `Phyre::PRendering::VPLight` | 20 | a light |
| `Phyre::PRendering::VPMaterial` | 17 | a material |

## 3. The extractor's noise floor — read before using the table

Grouping class names by their leading namespace token produces about **twenty entries that are not
namespaces at all**: `I`, `M`, `H`, `E`, `D`, `F`, `G`, `N`, `_J`, `_K`, `_N`, `PEAVPBase`,
`PEBVPBase`, `PEAVPEntity`, `PEAVPNameComponent`, `AEAVPNamespace` and similar.

These are **MSVC name-mangling fragments** — `PEAV` is "pointer to class", `AEA` "reference to", and
single letters are type codes — that survived demangling and were then split as though they were
namespaces. They account for roughly 25 classes.

**The table above lists only names that are actually namespaces.** The artifacts are named here
rather than silently dropped, because a reader regrouping the raw `classes.tsv` will meet them and
should know they are noise, not undiscovered subsystems.

## 4. What this does and does not establish

**Does:** that Phyre's 6,769 functions divide into a small number of large, conventionally-named
subsystems, and roughly how big each is. That is enough to plan.

**Does not:** anything about mechanism. Not one Phyre function body is read here. A class name is
tier-4 evidence — it says what the author called something, which is a strong hint and not a
description.

**And a counting caution.** `classes.tsv`'s method column counts **vtable slots**, which double-count
across template instantiations. The distinct figure recorded elsewhere in this database is **6,886
distinct virtual methods, 6,609 still named `FUN_*`**. Do not add the per-namespace slot counts and
call the total "methods in Phyre".

## 5. Key artifacts

| Path | Contents |
|---|---|
| `Tools/work/rtti/classes.tsv` | ~~2,133 classes~~ 2,248 classes *(corrected 2026-10-02, OPUS: the table's current row count)*: name, mangled, vtable count, method count |
| `Tools/work/rtti/methods.tsv` | per-method rows: address, class, slot, current name |
| `Tools/analysis-kit/gfz-scripts/rtti_recover.py` | the recovery tool |
| `Tools/analysis-kit/gfz-scripts/rtti_challenge.py` | its adversarial check |

## 6. Modding notes

- **Rendering, animation, physics and post-processing are middleware.** Upstream PhyreEngine
  documentation may describe them; FFXII-specific behaviour will not be there.
- **`PInputs` is Phyre's own input layer** — distinct from the game's
  [input stack](../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md), which is
  FFXII's. Two input systems coexist; do not conflate them.
- **`PScripting` is not the FFXII script VM.** The game's zone scripts run on its own VM
  ([`../../01-Script-VM-Native-Bridge/`](../../01-Script-VM-Native-Bridge/)); `PScripting` is Phyre's.
- **The reflection machinery inflates apparent size.** A class with fifty vtable slots may be one
  reflected type, not fifty behaviours.

## 7. What is not known

- [x] Everything about mechanism. ~~No Phyre function body is read.~~ **AQ-1.** *(SUPERSEDED in the register 2026-09-26, FABLE, Claude Opus 5.5: a duplicate; the open residue is carried by **AQ-2**)*
      **PREMISE RETRACTED 2026-09-16 (FABLE) — Phyre function bodies are read, in quantity, including
      in this folder.** `verify_doc_addresses.py` over
      [`../`](../) gives **711 interior citations across the section's 20 documents**, and an interior
      citation is a quoted instruction inside a body. The heaviest are the cluster-header contract
      (88), **[the fifteen modules registered before `main`](the-fifteen-modules-registered-before-main.md)
      — 78, in this same directory** — what happens between two frames (69), the class-descriptor
      contract (63), animation channel binding (61), the post-process passes (54), the Phyre
      application boundary (50), member registration (45), the class-descriptor system (43) and
      how a class registers its array members (44).
      **What is true is narrower and is already said by the front matter:** *this* page is
      `evidence_tier: 4`, built from the GZF snapshot and RTTI rather than from the executable, so it
      reads no body. Writing that as *"No Phyre function body is read"* turned a scope statement into
      a claim about the corpus, and the claim is false.
      **NOT ANSWERED, and deliberately not ticked.** Retracting a false premise is not answering the
      question. *"Everything about mechanism"* over 6,769 `CodeDomain:Phyre` functions is not a
      question that closes; what it was reaching for is carried by **`AQ-2`** (how the 6,769 map onto
      the 1,604 classes) and **`AQ-5`** (whether the ~992 non-glue functions are driven or
      linked-and-unused). ~~both still open below~~ *(2026-09-29, OPUS: AQ-5 is ANSWERED and AQ-2 SUPERSEDED; see
      their boxes below.)*
      *Found while triaging the forty-six register rows whose own text carries a universal negative,
      after `EH-4` turned out to be one — see `../../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md` §7.*
- [x] How the 6,769 `CodeDomain:Phyre` functions map onto the 1,604 classes — the RTTI naming has
      **not been applied to the GZF** (open question **B-3**). **AQ-2.**
      *Status 2026-09-26 (FABLE, Claude Opus 5.5): **B-3** is now ANSWERED (the class set was applied 2026-09-02 as the vtable method index), so the clause above is history. This box is **AQ-2**, which ~~stays PARTIAL on the 2,254 unplaced functions~~ is SUPERSEDED (the line below; 2026-09-29, OPUS: the counts reconcile, 1,606 + 1,063 + 1,846 = 4,515 placed and 4,515 + 2,254 = 6,769).*
      ***NARROWED 2026-09-18 (FABLE): 4,515 of the 6,769 are placed on a class by vtable evidence, 2,254 are not, and the per-function map is [`members/phyre-function-class-map.tsv`](members/phyre-function-class-map.tsv).*** The census takes every function the ledger tags `CodeDomain.Phyre` (6,769 today) and joins it two ways: to the RTTI methods table (`Tools/work/rtti/methods.tsv`, a body sitting in a class's vtable slot) and to a sweep of the vtables a body *installs* (every body of the population decoded; each rip-relative `lea` of an `.rdata` address whose `[−8]` is a valid RTTI locator, joined on the mangled name in `classes.tsv`, names the class whose constructor, destructor or factory the body is). **1,606** sit at exactly one class's slot (1,374 of them also install that class's vtable), **1,063** sit at the slots of several classes (folded bodies, the index page's `2,611` problem seen from this side), and **1,846** sit at no slot but install one Phyre vtable — the constructors, destructors and descriptor builders the method index cannot list. That leaves **2,254** with no vtable evidence either way, and the ledger's own sub-tags say what they are: 1,032 `Reflection`, 603 `ScriptVM`, 291 `Middleware`, 205 `Rendering`, and the rest under 20 each; 1,172 of the 2,254 are under 64 bytes, the thunk-and-accessor band. On the class side, `classes.tsv` carries **1,739** `Phyre::` names today (the 1,604 above predates the AS-9a recount): **1,466** are reached by a single-class slot, **78** more only through a body that installs their vtable, and **195** by neither route — every one of those 195 has methods in `classes.tsv`, so their slot bodies are either folded across classes or tagged outside the Phyre domain. Still open: which class each of the 1,063 folded bodies serves (the index page's question), what the 2,254 are beyond their sub-tags, and the GZF application itself (B-3). Static: the ledger, the two RTTI tables and the sweep.
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 22-Middleware-PhyreEngine/Subsystem-Map/members/phyre-function-class-map.tsv. See the register row.*
- [x] ~~Which Phyre subsystems FFXII actually drives.~~ **ANSWERED 2026-09-02** — 1,558 functions at
      the seam, split by group in section 11; `Middleware` is most game-facing at 62.8 %, `Physics`
      least at 4.3 %. Reached almost entirely from **unowned adapter code**, not from any documented
      game subsystem. Sections 10–11. **AQ-3.**
- [x] Whether Phyre's physics is used at all, or only driven internally from a frame update the game
      calls. Only 3 of 70 `Phyre.Physics` functions have a non-Phyre caller. **AQ-6.**
- [x] Whether the ~992 non-glue functions are themselves mostly driven or mostly linked-and-unused.
      **AQ-5.**
  ***ANSWERED 2026-09-18 (FABLE) — driven, almost entirely: 973 of the 993 are reachable from the program's roots and 20 are not.** The measure is a static reachability fixpoint over the whole image: roots are the PE entry, the two main-loop entries (`0022B8C0`, `0022B0B0`), the eight IAT-created thread start routines and the pool thread bodies; the closure follows direct calls (`edges.tsv`), every function whose address reachable code takes, and every pointer table whose address reachable code takes — qword tables (vtables, CRT initialiser and factory tables) and the engine's 32-bit image-address tables (the verb dispatch and its kin), tolerating gaps of up to 64 entries. It reaches 30,686 of the 38,161 listed functions. Of the 6,769 Phyre functions it reaches 6,326 (93.5 %); of the **993 non-glue** ones **973 (98.0 %, 344,612 of 351,533 bytes)**: Middleware 345 / 347, Rendering 285 / 288, PostProcessing 71 / 72, Physics 68 / 70, Animation 65 / 69, and every smaller group whole except Framework 15 / 19, GameplayTrigger 0 / 3 and DebugUtils 1 / 2. The **20 unreached** are the static dead-linked floor: `001E2AF0` (4,745 B, Rendering), `005CCD00` (926 B, DebugUtils), `006A8A20` (320 B) and `006A8810` (270 B, Middleware), `006A0B60` (139 B) and `00691DB0` (64 B, Physics), `00646AB0` (81 B, PostProcessing), `007933C0`, `00793570`, `00793750`, `007934E0` (Framework, 11–73 B), `005AA2C0`, `005AA260`, `005A9F00`, `005A9E60` (Animation, 11–43 B), `006A91C0`, `006A9280`, `006A9150` (GameplayTrigger, 4–62 B), `0018D0E0` and `005DD660` (Rendering, 11 B). Reachable bounds *driven* from above (a slot in a table reachable code names can still go uncalled), and the strict variant of the same walk — calls, taken pointers and strictly-shaped vtables only — still reaches 253 of the 993, so the true driven count lies between 253 and 973 with the 20 firmly outside it. So the non-glue remainder is linked *and used*: by count 98 % of it has a path from the game's roots, and what is dead-linked is twenty mostly tiny bodies. Static: `phyre_reach.py` over the shipping image; the glue split is the 2026-09-02 pass's.*
- [x] What the 50 classes directly in `Phyre::` are. **AQ-4.**
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (AQ-4), by a fresh census of the image's own RTTI
  type descriptors:* **the root namespace is the engine's core. 40 plain classes and 22 template families end in
  `@Phyre@@` with no sub-namespace**, which is 62 names. The map's 50 used a different counting rule, not reproduced here.
  The 40 plain classes fall into five groups:

  | group | classes |
  |---|---|
  | **reflection and type system** (22) | `PType`, `PClassData`, `PClassDataMember`, `PClassDataMemberArray`, `PClassDataMemberArrayFixedSize`, `PClassDataMemberDynamic`, `PClassDataMemberEnum`, `PClassDescriptor`, `PClassDescriptorBase`, `PClassDescriptorDynamic`, `PClassDescriptorForClassDescriptor`, `PClassLayoutInterface`, `PClassMember`, `PIChildClassVisitor`, `PIClassDataMemberDynamicType`, `PAnnotatable`, `PAnnotation`, `PNamedSemanticBase`, `PNamedSemanticDescriptor`, `PHashEntryConst`, `PHashEntryConstKey`, `PRedBlackTreeNode` |
  | **object base and lifetime** (5) | `PMemoryBase`, `PBase`, `PInitializable`, `PComponent`, `PUtility` |
  | **threading** (5) | `PThread`, `PThreadWin32`, `PThreadPool`, `PThreadPoolImmediate`, `PThreadPoolWorkStealing` |
  | **cameras and view control** (6) | `PCamera`, `PCameraProjection`, `PCameraPerspective`, `PCameraOrthographic`, `PWorldMatrixController`, `PWorldMatrixFlyController` |
  | **call plumbing** (2) | `PCaller`, `PTTYCallback` |

  The 22 root templates, with instantiation counts:
  - **descriptor forms:** `PClassDescriptorForType` 409, `PClassDescriptorAbstract` 393, `PClassDescriptorConcrete` 331,
    `PClassDescriptorWithoutDefaultConstructor` 38, `PClassDescriptorWrapper` 15, `PClassDescriptorHeaderWithoutDefaultConstructor` 4,
    `PClassDescriptorHeader` 3;
  - **member templates:** `PClassDataMemberArrayDynamic` 71, `PClassDataMemberPhyreArray` 59, `PClassDataMemberPhyreSharray` 10,
    `PClassDataMemberDynamicType` 2;
  - **callers:** `PMethodCallerConcrete` 156, `PFunctionCallerConcrete` 11;
  - **named semantics:** `PNamedSemanticDescriptorForType` 17, `PNamedSemantic` 11, `PNamedSemanticDescriptorForDynamicType` 3,
    `PNamedSemanticDynamic` 1, `PAnnotationWithValue` 1;
  - **containers:** `PSimpleListElement` 12, `PSimpleDoubleListElement` 5, `PRingBuffer` 1;
  - **scalar types:** `PTypeDefault` 12, the twelve scalar types of
    [the lazy-static records](../Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md).

  **What that means.** Nothing game-specific lives in the root namespace. It holds the reflection machinery every other
  subsystem registers through, the base classes, a thread pool, and a camera stack. The fly controller is the only
  debug-flavoured name.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 1,604 `Phyre::` classes, 1,714 vtables | `classes.tsv`, filtered on the `Phyre::` prefix | 4 |
| Per-namespace class and vtable counts | grouping `classes.tsv` by the token after `Phyre::` | 4 |
| Seven namespaces hold 1,239 of 1,604 classes | the same grouping, summed | 4 |
| Phyre is 6,769 functions | `functions.tsv`, `GFZ.V121.CodeDomain.Phyre*` | 1 |
| Only 2 Phyre functions carry a recovered name | `functions.tsv`, non-`FUN_`/`thunk_` names within that domain | 1 |
| ~25 apparent namespaces are mangling fragments | inspection of the grouped output: `PEAV`/`AEA`/single-letter type codes | 2 |
| Slot counts double-count across templates | the distinct-method figure recorded in `COVERAGE.md` (6,886) is far below the slot sum | 2 |

**Scope honesty:** this is a map, not an explanation. It is filed at **tier 4** deliberately — RTTI
names are the author's labels, and every count here is a count of *declarations*, not of behaviour.

## 9. Related

- [`../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) — the `VP*` reflection machinery this map keeps running into
- [`../Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`](../Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md) — the other documented Phyre surface
- [`../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md`](../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md) — PPFX/Yebis, a *separate* middleware from Phyre's `PPostProcessing`
- [`../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md`](../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md) — FFXII's input stack, not `PInputs`

## 10. Falsification pass 2026-09-02 — 85 % of Phyre is generated glue

**Attack chosen.** The document's headline is that Phyre is "the largest unexplained block in the
image — 6,769 functions, 20 % of the executable". **AQ-3** asked which of it the game actually uses.
Both are attackable from the ledger without reading a line of Phyre, and the answer changes what
"unexplained" means here.

### The split

Grouping the 6,769 functions by their `CodeDomain.Phyre.*` label:

| group | functions | bytes | mean size |
|---|---:|---:|---:|
| **`Reflection`** | **4,557** | 421,064 | **92 B** |
| **`ScriptVM`** (object-binding adapters) | **1,219** | 204,419 | **168 B** |
| `Middleware` | 347 | 177,238 | 511 B |
| `Rendering` | 288 | 74,634 | 259 B |
| `PostProcessing` | 72 | 14,054 | 195 B |
| `Physics` | 70 | 8,427 | 120 B |
| `Animation` | 69 | 13,492 | 196 B |
| everything else (24 groups) | 147 | 63,688 | — |

**`Reflection` + `ScriptVM` = 5,776 of 6,769 functions — 85.3 % by count.**  *(6,769 at GN161 — the R109 batch classified `00180A70` as `Phyre.Rendering.TextureBufferSetup`; corrected 2026-09-14.)*

### What those two groups are

The labels are specific, and they repeat in the thousands:

```
Reflection.PClassDescriptorForType.DeletingDestructor      1,149
Reflection.DataMemberMetadataStaticTeardown                  853
Reflection.ClassDescriptorStaticTeardown                     404
Reflection.PClassDescriptorForType.DestructorThunk           384
Reflection.ObjectTraversalAdapter                            299
Reflection.PClassDescriptorConcrete.StaticInitializer        255
ScriptVM.ObjectPointerAccessor                               323
ScriptVM.ObjectPushAdapter                                   305
ScriptVM.NullableObjectPushAdapter                           299
ScriptVM.ObjectReferenceAccessor                             265
```

Destructors, static teardowns, static initialisers, push adapters, pointer accessors — **one per
reflected type**, which is exactly what the 1,604 classes of section 2 would generate.

**The size distribution corroborates it mechanically.** Reflection averages **92 bytes** and ScriptVM
**168**, against `Middleware` at **511** and `Rendering` at **258**. Thousands of near-identical
functions three to five times smaller than real behaviour is the signature of generated code, and
that is measured, not inferred from the labels alone.

### What this does to the headline

**"20 % of the executable is unexplained middleware" was true but misleading.** By function count,
**85 % of Phyre is generated glue whose pattern is known**, and only about **993 functions** are
engine behaviour — roughly **2.6 % of the image**, not 20 %.

Two cautions, both material:

- **By bytes the split is 64 %, not 85 %.** Glue functions are small. Quote whichever measure you
  mean and never both as one number.
- **Generated is not the same as understood.** Knowing that 1,149 functions are
  `PClassDescriptorForType::~DeletingDestructor` for 1,149 different types explains them *as a
  category* — which is what the mission's "nothing unexplainable" needs — but no individual body is
  read, and the classification is the **GFZ's judgement** (tier 2), corroborated by size, not a
  tier-1 reading.

### AQ-3 partly answered: the boundary is 1,558 functions

Counting Phyre functions with at least one caller **outside** Phyre:

```
1,558 distinct Phyre functions are called from non-Phyre code
```

That is the game/middleware seam — 23 % of Phyre, and a bounded target. It does **not** yet say
*which subsystems* those 1,558 belong to; that split is the remaining half of AQ-3.

### Not changed

The RTTI class map, the namespace sizes, the `VP*` reflection note and the three conflation warnings
all stand. This pass adds the ledger-side view the class-side map could not give.

## 11. Falsification pass 2026-09-02 (second) — AQ-3 finished, and no game subsystem calls Phyre

**Attack chosen.** Pass 10 answered half of AQ-3 — 1,558 Phyre functions have a caller outside
Phyre — and left the split open. Splitting it turned out to matter far less than looking at the
**other end of those edges**.

### The seam by Phyre group

| Phyre group | at the seam | of | share |
|---|---:|---:|---:|
| `Reflection` | 617 | 4,557 | 13.5 % |
| `ScriptVM` | 567 | 1,219 | 46.5 % |
| **`Middleware`** | **218** | **347** | **62.8 %** |
| `Rendering` | 54 | ~~287~~ 288 *(corrected 2026-10-02, OPUS: the 2026-09-14 count above, `00180A70` included)* | 18.8 % |
| `PostProcessing` | 25 | 72 | 34.7 % |
| `Animation` | 16 | 69 | 23.2 % |
| `Framework` | 10 | 19 | 52.6 % |
| `Geometry` | 10 | 14 | 71.4 % |
| **`Physics`** | **3** | **70** | **4.3 %** |

`Middleware` is the most game-facing group; **`Physics` is the least**, by a wide margin.

### Phyre's physics is barely reached from outside Phyre

**Only 3 of 70 `Phyre.Physics` functions have a non-Phyre caller.** That is consistent with FFXII
doing its own movement and clearance work — this database documents a complete
[battle locomotion solver](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)
with its own obstruction tests — rather than delegating to Phyre.

**Consistent with, not proof of.** Phyre could drive its own physics internally from a frame update
the game calls once. What is measured is the *seam*, not total usage. **AQ-6.**

### The finding: no documented game subsystem calls Phyre

Grouping the callers by `PrimaryOwner`:

| caller owner | edges |
|---|---:|
| **(unowned)** | **2,904** |
| `Resource` | 281 |
| `Input` | 33 |
| `Presentation` | 3 |
| `Audio` | 1 |
| `Script_VM_Native_Bridge` | 1 |

**CombatAction, CombatFormula, CombatAI, Movement, Party, UI, ActorEntity, Rewards — none of them
calls Phyre at all.** The only owned subsystem with real traffic is **`Resource`**.

And the unowned callers are not a mystery so much as a known gap:

| their CodeDomain | edges |
|---|---:|
| `NativeRoutine` | 919 |
| `NativeAdapter` | 657 |
| `CompilerGeneratedEH` | 482 |
| `Runtime` | 359 |
| `NativeDispatch` | 232 |
| `CxxObjectLifecycle` | 65 |
| others | ~190 |

Those are the **generic shape classes** — the ~11,836 functions `COVERAGE.md` calls *"accounted for
only"*. About **534** of the 2,904 edges are compiler-generated (`CompilerGeneratedEH` +
`CompilerGeneratedCpp`) and are exception-handling and lifecycle glue rather than intent.

### What that means for the mission

**The game/middleware seam runs entirely through code that is classified but not understood.** The
gameplay systems this database documents in detail do not touch Phyre; generically-labelled routines
sit between them.

> **RETRACTED 2026-09-02 (pass 52).** This section then concluded that *"understand the seam" and
> "understand the generic shape classes" are the same task*. **They are not.** That inference read a
> census of 2,904 **edges** as a census of **functions**. Measured in the other direction, only
> **317 of 15,498** unowned functions in the generic groups are predominantly Phyre-called — **2 %** —
> and the heavily-called helpers producing most of those edges sit *below* Phyre as its own runtime,
> not between Phyre and the game. The seam is real and bounded; the shape classes are a separate and
> much larger problem. See
> [why the unowned code has no owner](../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md).

### AQ-3 closed

Both halves are answered: 1,558 functions at the seam, split by group above, reached almost entirely
from unowned adapter code rather than from any documented game subsystem.

## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)

- **CoreRuntimeScheduling - CLIENT and SERVICE (4 edges).** MainLoop_Draw (`0022B0B0`), MainLoop_UpdateAndRenderFrame (`0022B8C0`) are called by bodies filed to CoreRuntimeScheduling: `0022A580`, `0022A770`, `0022AF50`; MainLoop_UpdateAndRenderFrame (`0022B8C0`) reaches bodies filed to CoreRuntimeScheduling: `00374FD0` - shared machinery across the layer boundary, no shared ownership.
- **Input - SERVICE (9 edges).** MainLoop_UpdateAndRenderFrame (`0022B8C0`) reaches bodies filed to Input: `0017DE60`, `00182D40`, InputGameplay_RebuildFrameSnapshotFromChannelHistory (`002498B0`), `0035AE30` (+5 more) - shared machinery across the layer boundary, no shared ownership.
- **Movement - SERVICE (3 edges).** MainLoop_Draw (`0022B0B0`), MainLoop_UpdateAndRenderFrame (`0022B8C0`) reach bodies filed to Movement: `00263560`, `00357780`, `0037CF00` - shared machinery across the layer boundary, no shared ownership.
- **Party - SERVICE (1 edge).** MainLoop_UpdateAndRenderFrame (`0022B8C0`) reaches bodies filed to Party: PartyFocus_CommitPendingPackedActorHandle_Thunk (`00358BB0`) - shared machinery across the layer boundary, no shared ownership.
- **Presentation - SERVICE (19 edges).** `001E2AF0`, MainLoop_Draw (`0022B0B0`), MainLoop_UpdateAndRenderFrame (`0022B8C0`) reach bodies filed to Presentation: `001ABF50`, `002512B0`, `002528A0`, `002529F0` (+11 more) - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (1 edge).** MainLoop_UpdateAndRenderFrame (`0022B8C0`) reaches bodies filed to Resource: `00324510` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (1 edge).** MainLoop_UpdateAndRenderFrame (`0022B8C0`) reaches bodies filed to WorldAreaField: World_UpdateSimulationTick (`00314020`) - shared machinery across the layer boundary, no shared ownership.
