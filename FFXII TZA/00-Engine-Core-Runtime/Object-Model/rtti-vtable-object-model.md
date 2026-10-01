---
system: The RTTI vtable object model
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: none - spans every subsystem
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: Tools/analysis-kit/gfz-scripts/vtable_map.py; MSVC Complete Object Locator at
    vtable[-1], validated by the locator's own pSelf self-reference; capstone sweep of
    every .text function for `lea reg,[rip+vtable]`
  artifact: Tools/work/rtti/vtables.tsv (25,798 rows)
last_reviewed: 2026-09-02
audit:
  passes: 10
  last_pass: 2026-09-02
  last_pass_state: novelty-claims-retracted-corroboration-established
  crossref_clean: true
  reopened_count: 0
---

# The RTTI vtable object model

> **2,286 vtables in this executable carry their class name**, and the name can be recovered exactly
> rather than guessed. That turns **3,784 functions that had no owner and no caller** into methods of
> a named class.
>
> **This recovery was performed twice, independently, and the two agree.** An earlier pass built
> `rtti_recover.py` walking TypeDescriptor -> CompleteObjectLocator -> vtable; this pass built
> `vtable_map.py` walking vtable[-1] -> locator with a `pSelf` self-reference check. **Both find
> exactly 2,286 vtables**, and 6,886 versus 6,883 virtual methods. That agreement is worth more than
> either result alone.

**What this means for a player.** When a character walks into a wall, slides along it, or an attack
checks whether something is in the way, the collision maths is **Bullet Physics** - the same
open-source library many games use - running **underneath Phyre's own physics module**, which wraps
it. Every sound, from a battle voice shout to streamed music, flows through **Square Enix's own sound
engine**, whose class names reach down to individual effect types like `Flanger`, `Compressor` and
`GranularPitchShift`.

> **CORRECTED.** This paragraph first said Bullet was present "not Phyre's". **That is wrong** -
> Bullet is Phyre's *backend*, not an alternative to it. Section 3a has the evidence.

---

## 1. Why this works, and why it is not a heuristic

MSVC places a pointer to a **Complete Object Locator** in the slot immediately *before* a vtable:

```c
vtable[-1] -> _RTTICompleteObjectLocator {
    DWORD signature;         /* 1 on x64                        */
    DWORD offset;            /* this vftable's offset in the object */
    DWORD cdOffset;
    DWORD pTypeDescriptor;   /* RVA -> TypeDescriptor           */
    DWORD pClassDescriptor;  /* RVA                             */
    DWORD pSelf;             /* RVA of this locator             */
};
TypeDescriptor { void *pVFTable; void *spare; char name[]; };   /* ".?AVFoo@Bar@@" */
```

**`pSelf` is what makes this evidence rather than pattern-matching.** A false positive would have to
be a run of bytes that contains its own address as an RVA. Every name below is verified that way.

| | |
|---|---:|
| named vtables recovered | **2,286** |
| vtable slots | 25,798 |
| distinct functions in >= 1 named vtable | 6,883 |
| classes whose constructor was also located | **2,244 of 2,248** |
| functions that write a vtable pointer | 4,664 |

Constructors were found separately, by sweeping every `.text` function for
`lea reg, [rip+<vtable VA>]` - the instruction that stamps the vtable into a fresh object. **Whoever
writes the vtable pointer builds the object**, which is the same discipline this database applies to
any structure: the writers decide.

---

## 2. The ambiguity, stated before the results

A function can appear in several classes' vtables. **It happens to 2,611 of the 6,883 - 37.9 %.**

| appears in | functions |
|---|---:|
| exactly one class | **4,272 (62.1 %)** |
| two classes | 1,019 |
| three classes | 1,356 |
| four or more | 236 (one function appears in **1,349**) |

**This is mostly inheritance, not COMDAT folding.** A derived class's vtable copies every base method
it does not override, so a base method appears once per descendant. Only **14 %** of the multi-class
functions are 16 bytes or smaller, which is the size range where `/OPT:ICF` folds unrelated bodies
together - and this image is known to fold (`0016D6A0`, a bare `ret 0`, is shared by three unrelated
tables).

**Consequence, and it is the number that matters:** attribution is only safe for the **4,272**
functions that appear in exactly one class. Of those, **3,784 were previously unowned**. That is the
real gain, and it is 61 % of the 6,125 unowned zero-caller functions found in named vtables - not
100 %.

The other **3,953 pointer runs in data carry no locator**. They are candidates, not vtables: a jump
table, a callback array and a `/GR-` class all have the same shape. They are counted, never named.

---

## 3. The library layer - already inventoried, now with class hierarchies

### Bullet Physics - 61 classes

The complete stack is present, not a fragment:

| layer | classes |
|---|---|
| world | `btDiscreteDynamicsWorld` (42 slots), `btDynamicsWorld`, `btCollisionWorld` |
| shapes | `btBoxShape`, `btSphereShape`, `btCapsuleShape`, `btCylinderShape`, `btConvexHullShape`, `btCompoundShape`, `btStaticPlaneShape`, `btBvhTriangleMeshShape`, `btTriangleShape` |
| broadphase | `btAxisSweep3`, `btDbvtBroadphase`, `btHashedOverlappingPairCache` |
| solver | `btSequentialImpulseConstraintSolver`, `btConstraintSolver`, `btSimulationIslandManager` |
| queries | `btCollisionWorld::ClosestRayResultCallback`, `ClosestConvexResultCallback`, `btGjkPairDetector`, `btSubsimplexConvexCast`, `btContinuousConvexCollision` |

**Constructors exist** - `btRigidBody` is built by four functions, `btDiscreteDynamicsWorld` and the
shape hierarchy likewise - so this is linked *and instantiated*, not dead weight the linker kept.

### 3a. Bullet is Phyre's physics backend - AS-1 and AQ-6 answered

The first version of this section said the driver was unknown, because a six-hop climb from every
Bullet constructor reached **no owned subsystem at all**. That negative was real but misleading: the
answer is not above Bullet in the call graph, it is beside it, and **the ledger already had it.**

| evidence | |
|---|---|
| `0069FB10` | `Phyre.PPhysics.Bullet.RigidBodyCompoundShapeAndBtRigidBodyMaterialization` - 1,899 B, calls Bullet |
| `006A4A60` | `Phyre.PPhysics.PPhysicsRigidBody.ResetBulletTransformScaleAndActivation` - 965 B |
| `00692AC0` | `Phyre.PPhysics.PPhysicsWorld.DeepCopyAssignment` |
| measured | **23 of 73** `Phyre.*Physics` functions call a Bullet-tagged function directly |
| measured | `006A1A70` (ray) and `006A1DD0` (convex sweep) build Bullet result callbacks and are tagged `Phyre.Middleware.NativeImplementation` |

**`PPhysics` is Phyre's physics module and Bullet is what implements it.** A Phyre class whose GFZ
label contains both `PPhysicsRigidBody` and `btRigidBody` materialisation is not a coincidence of
naming; it is the bridge.

**This answers AQ-6 the other way round.** That question asked why only 3 of 70 `Phyre.Physics`
functions are reached from outside Phyre. Not because physics is unused - because the game reaches
physics through a **narrow Phyre interface**, and everything below that interface is internal:
Phyre's own physics layer down to Bullet. The narrowness of the seam was evidence of encapsulation,
which this pass misread as evidence of disuse.

**Still open:** which *game* subsystem calls that narrow interface. Six hops of direct calls reach no
owned code, and 95 % of Bullet's own methods are virtual-only, so the remaining link is through
vtable dispatch the edge list cannot represent. **AS-1a.**

### Square Enix's sound engine - 254 `SQEX::Sd` classes

`SQEX::Sd` is **SQEX Sound**, and its base object is `SeadObject` - confirming and extending
[sead engine identity and diagnostics](../../18-Audio/sead-engine-identity-and-diagnostics.md), which
identified the name without the class hierarchy.

| subtree | vtables |
|---|---:|
| `SQEX::Sd::Driver` | 49 |
| `SQEX::Sd::ConfigFile` | 40 |
| `SQEX::Sd::AudioBinaryFile` | 35 |
| `SQEX::Sd::MabFile` | 17 |
| `SQEX::Sd::Lay` | 10 |
| `SQEX::Sd::SabFile` | 10 |

The sound-type hierarchy is explicit: `Driver::Sound`, `SwitchSound`, `RandomSound`, `OrderSound`,
`VariationSound`, `CycleSound` (48 slots each); the spatial layer `Lay::PointSound`,
`DirectionSound`, `PolygonSound`, `AmbientSound`, `DynamicSound`; music under `Magi::Music`; output
through `Driver::WASAPI::WASAPIDevice`. Individual DSP effects are named -
`Compressor`, `Flanger`, `SurroundReverb`, `HilbertFilter`, `GranularPitchShift`, `SideChainInput`.

**This one is not a lead.** `Audio` is the *owning* subsystem for the constructors: 43 external
callers and 443 vtable-writing functions carry `PrimaryOwner = Audio`. The seam here is real and
attributed.

Above it sits the game's own bank layer, in the global namespace: `AudioBank`, `SepAudioBank`,
`SebAudioBank`, `ShoutAudioBank`, `StreamAudioBank`, `MusicAudioBank`, `MusicStreamingReader`, and
matching `*AudioController` classes - **each constructed by five `Audio`-owned functions**.
`ShoutAudioBank` is its own category, which is consistent with battle voice lines being banked
separately from effects; ~~**that reading is a lead, not a finding.**~~ **CONFIRMED 2026-09-22
(FABLE) from the shipped banks' own sample names — every one is suffixed `at`/`dm`/`crt`/`dead`.
AS-2.**

> **ADVANCED 2026-09-02 — `shout` is voice, on structural evidence.** The game's asset-category path
> directory ([VBF archive](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md)
> section 8) carries **two** shout path tables — `sound\shout\us\shout00.win.sab` and
> `sound\shout\jp\shout00.win.sab` — while sound effects (`sound\se\block\*.seb`) and music
> (`sound\music\*.bgm`) have **one table each**. **Only recorded speech needs a table per
> language**, so the localisation split is the evidence the name alone could not give, and `.sab`
> places it in `SQEX::Sd::SabFile`. **Still open on the narrower point:** *battle* voice specifically,
> versus all character speech.

### Three more - and a retraction

| RTTI namespace | what it is |
|---|---|
| `Yebis::PfxShimD3D11`, `YebisPfxMemoryAllocatorD3D11` | Silicon Studio's YEBIS post-processing middleware |
| `mkvparser::*` (8) - `AudioTrack`, `BlockGroup`, `SimpleBlock`, `IMkvReader` | Matroska/WebM demuxer, the FMV container |
| `JsonBox::*` (3), `eastl::allocator` (2) | JSON parsing; EA's STL |

> **RETRACTED.** This section was first headed *"Libraries this names for the first time"* and the
> summary said these were *"libraries the database had never identified"*. **Both are false.**
> [The third-party middleware inventory](../../23-Third-Party-Libraries/third-party-middleware-inventory.md)
> already documents **thirteen** libraries with versions - PPFX 348, Bullet 120, Lua 90,
> **LibVPX VP8 1.6.0** 73, **zlib 1.2.11** 25, libvorbis 11, **Dear ImGui** 7, JsonBox 4, libxml2 4,
> **Tremor** 4, Yebis 3 - together with the `Yebis` RTTI strings and the `EnableYebis` toggle. The
> ledger itself carries `ThirdParty.Physics.Bullet` on 120 functions.
>
> **What this pass actually adds is the class hierarchy**, not the identification. The failure was
> not checking the database's own contents before claiming novelty - the same error recorded as
> AK-1/AK-2. It is now standard rule 13.

**The RTTI strings are tier-1 measurements. What the libraries *are* is outside knowledge**, recorded
as such per the evidence standard.

---

## 4. The game's own object model

Beyond the libraries, the global namespace holds FFXII's own architecture. A selection, with slot
counts:

| class | slots | |
|---|---:|---|
| `PrimitiveRendererD3D11` | 42 | immediate-mode drawing |
| `CharacterRenderObject` | 31 | |
| `GameApplication` | 30 | the root application object |
| `DynGeoUIInstance`, `DynGeoTextureInstance`, `DynGeo3DInstance` | 21 each | "dynamic geometry" instances |
| `DynGeoFontTextSpecialShadowInstance` (+3 siblings) | 12 each | drop-shadowed text |
| `ChrModel` | - | 8 constructors, `NativeRoutine`-owned |
| `OrderedObject`, `MapOrderedObject`, `CharacterOrderedObject`, `FontBorderOrderedObject` | - | a draw-ordering hierarchy |
| `InputManager`, `AsyncJobManager`, `AssetListManager` | - | |

The `DynGeoFontTextSpecial*` family is a direct lead for
[numeric formatting and character mapping](../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md),
which documents how characters are chosen but not how they are drawn. **AS-3.**

## `AS-3` answered — yes, and the route was already in the database in three pieces (FABLE, 2026-09-22)

**The family is the draw path, and the honest first thing to say is that this database had already
established every leg of the route — on three different pages, never joined to this row.**

| leg | already published by |
|---|---|
| `002AC5F0` (the interpreter) calls `0017F850` at `002AD7AE` and `002AC7EC` — *“draw what the last frame accumulated”* | [painting a line of text](../../99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md) § line 204 |
| `0017F850` opens the profiler scope **`display : draw Font`**, takes the text singleton `001B5FA0()` = `[01F811F8]`, and calls `001E8580`, **whose only caller it is** | [character mapping](../../16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md) lines 1151/1154 |
| the four 12-slot vtables, the slot-10 shared draw `002142A0` and the sibling tail-jumps | [the text/DynGeo contract](../../16-UI/CONTRACT-text-control-codes-and-dyngeo-draw.md) §2–§6 |

### What is measured here, and why it settles the ownership (FABLE, 2026-09-22)

An image-wide reference sweep of the whole four-vtable window `00906DE8`–`00906F88` returns
**exactly six sites, every one of them inside `00213xxx`**:

| site | stamps | role |
|---|---|---|
| `00213AA6`, `00213AD6`, `00213B06` | `00906DE8` | the three slot-2 destructors — the MSVC reset-to-base store |
| `002138F9` | `00906EB8` | constructor, `Final` |
| `00213999` | `00906F20` | constructor, `ShadowFinal` |
| `00213A39` | `00906E50` | constructor, `Shadow` |

**And the only call sites of those three constructors in the whole image are four, all inside
`001E8580`** — each one a textbook `new`: load the heap singleton `[01F7F4C0]`, `call 001A1470`,
then construct.

| call site | allocated | constructor | class | size the contract derived from the destructors |
|---|--:|---|---|--:|
| `001E86BB` | `0x168` | `00213A00` | `Shadow` | `0x168` |
| `001E88C4` | `0x168` | `00213A00` | `Shadow` | `0x168` |
| `001E8A7D` | `0x168` | `00213960` | `ShadowFinal` | `0x168` |
| `001E8F84` | `0x170` | `002138C0` | `Final` | `0x170` |

**The sizes agree 4 of 4 with a figure derived by a different instrument from the other end of the
object's life** — the contract read them off the sized deleting destructors, this reads them off the
allocations. That agreement is the control on the sweep.

> **So the join the contract left open is closed from the construction side.** §6 of the contract is
> careful to say that *“no direct-call route” is a statement about every route the direct-call graph
> contains, **not a proof that the text pipeline never draws through these classes**”, and proposes
> `PROPOSED-OPUS-S37-1` to settle it. **It is settled: the text flush `001E8580` is the sole
> constructor and owner of the `DynGeoFontTextSpecial*` objects anywhere in the image, and the text
> interpreter is the only thing that reaches it.** The family is not merely co-registered with the
> character mapping — it is allocated by the function the mapping's own flush calls, inside a scope
> the original code named `display : draw Font`.

### Two corrections this sweep forces (FABLE, 2026-09-22)

1. **The root calls three of the four classes, not one.** [Painting a line of text](../../99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md)
   marks `00213A00` as *“the one the root calls”*; `001E8580` in fact calls `00213A00` **twice**
   (`001E86BB`, `001E88C4`) and also `00213960` (`001E8A7D`) and `002138C0` (`001E8F84`). The page is
   right that `00213A00` is the root's own `0x168` render object; what it misses is the other three
   sites.
2. **The plain `DynGeoFontTextSpecialInstance` is never constructed.** No constructor anywhere in the
   image stamps `00906DE8`; its only three writers are the destructors resetting to base. The plain
   class exists as a base and a destructor target, and the objects that are actually built are
   `Shadow`, `ShadowFinal` and `Final`.

> **The caveat, stated exactly, because it is the same one §6 raises.** Slot 10 — the shared draw
> `002142A0` and its variants — is reached **through the vtable**, and nothing here observes that
> dispatch. What is proven is *construction and ownership*: who allocates these objects, under what
> name, and at whose call. A live capture of the slot-10 call is still the thing that would witness
> the draw itself, and that remains `PROPOSED-OPUS-S37-1`'s business. **This is NATIVE/STATIC
> evidence, not live.**



Vtable-writing functions by owner: `Phyre` 3,248, **`Audio` 443**, **`Input` 402**, then compiler and
lifecycle glue. Audio and Input are the two owned subsystems that are heavily object-oriented.

---

## 4a. Two independent recoveries, and a duplicated tool

**This work was done twice.** `Tools/work/rtti/` already held `classes.tsv`, `methods.tsv` and
`report.md` from `rtti_recover.py`, an earlier pass that walked RTTI in the opposite direction:
TypeDescriptor -> CompleteObjectLocator -> vtable. This pass wrote `vtable_map.py` without checking,
walking vtable[-1] -> locator and validating each locator by its own `pSelf`.

| | `rtti_recover.py` (earlier) | `vtable_map.py` (this pass) |
|---|---:|---:|
| vtables | **2,286** | **2,286** |
| distinct virtual methods | 6,886 | 6,883 |
| classes with a vtable | 2,133 | 2,248 named vtable owners |
| `SQEX` | 212 classes | 218 classes / 254 vtables |
| `Phyre` | 1,604 classes | 1,743 vtables |

**The vtable count agrees exactly and the method counts differ by three.** Two tools written
independently, entering the RTTI graph from opposite ends, is real corroboration - stronger than
either result on its own. The class-versus-vtable difference is expected: multiple inheritance gives
one class several vtables.

**The three-method discrepancy is not explained** and is **AS-7**. It is small enough to be
tempting to ignore and exactly the size where a real defect hides.

**The duplication is a process failure, recorded as such.** The artifacts were on disk and the
earlier pass is in `AUDIT-LOG.md`. Checking would have cost one directory listing.

## 5. Corrections this pass forces

**"7,331 distinct functions appear as pointers in data" was an undercount. The figure is 10,472.**
The earlier scan silently restricted its candidate set to functions carrying a `CodeDomain` tag.
The 65.8 % ratio in
[why the unowned code has no owner](../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md)
is unaffected - both sides of that intersection were drawn from the same restricted population - but
the standalone count was wrong and is corrected there.

**A second measurement error, caught in the same session:** a `collections.defaultdict` used for the
caller index was *read* before the zero-caller set was computed, which inserted empty entries and
silently shrank the population from 10,984 to 10,674. **Reading a `defaultdict` mutates it.** The
figures published here use a plain set built directly from the edge file.

---

## Open questions

- [x] ~~Which game system drives Bullet Physics.~~ **ANSWERED** - Bullet is **Phyre's `PPhysics`
      backend**; 23 of 73 `Phyre.*Physics` functions call Bullet directly. Section 3a. **AS-1.**
- [x] ~~Which *game* subsystem calls Phyre's physics interface.~~ **ANSWERED as far as it can be** -
      there is **no edge to find**: physics is invoked through `PMethodCallerConcrete` reflection
      objects, one generated class per signature. Section 6. **AS-1a.**
- [x] ~~Why the two independent RTTI recoveries differ by three virtual methods.~~ **ANSWERED** -
      all three are **mid-function addresses**, accepted by the earlier tool because it tested only
      the `.text` VA range. **6,883 is correct.** Section 6. **AS-7.**
- [x] ~~Why the two recoveries differ by 191 named slots.~~ **ANSWERED** - a **naming** difference,
      not a data one. By (address, slot) the two agree to within the same three AS-7 entries. This
      tool's demangler doubles the outer namespace on template classes. Section 7. **AS-8.**
- [x] Replace `vtable_map.py`'s `demangle()` with a real MSVC demangler; the current one emits
      `Phyre::Phyre::` and flattens template arguments into the namespace path. Addresses and slots
      are unaffected. **AS-9.**
- [x] ~~Whether Phyre's character controller is used at all.~~ **ANSWERED - no.** Only reflection
      *descriptors* exist for it, never an object vtable; all 18 writers are Phyre; the addresses
      appear in no data section. Section 7. **AS-1b.**
- [x] ~~Whether `ShoutAudioBank` is battle voice lines.~~ **ANSWERED 2026-09-22 (FABLE): battle
      voice specifically — the banks name their own events.** Every sample is `ve`/`vj` + actor +
      index + event, and the events are `at` attack, `dm` damage, `crt` critical, `dead` death.
      Censused over all 132 banks (66 per language, 0 rejected against the `sabf` control): **66
      actor codes and 660 = 10×66 classified samples per language**, dividing exactly as 3×66 `at`,
      3×66 `dm`, 2×66 `crt`, 2×66 `dead`. See [the `.sab` page](../../18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md).
      **AS-2.**
- [x] ~~Whether `DynGeoFontTextSpecial*` is the draw path for the character mapping already documented
      in 16-UI.~~ **ANSWERED 2026-09-22 (FABLE): yes.** The text flush `001E8580` is the **sole
      constructor** of the family anywhere in the image — four `new` sites, sizes agreeing 4/4 with
      the contract's destructor-derived figures — and its only caller `0017F850` is called by the
      interpreter `002AC5F0` inside the scope `display : draw Font`. Section above. **AS-3.**
- [x] ~~What the 3,953 unnamed pointer runs are.~~ **ANSWERED** - **92.1 % are single-slot**
      individual function pointers, not tables. Only ten runs exceed ten slots. Section 8. **AS-4.**
- [x] What the 1,172-slot run at `008C31D8` is - the largest table in the image, 325 slots
      `Input`-owned. **AS-10.**
- [x] The combat formula step table document cites one interpreter site; there are **two**
      (`00385680` and `00385F60`). **AS-11.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (AS-11):* the step-table page now cites both.
      The second site is `BattleFormula_EvaluateTargetPreview` (`003859FF`), the target-preview run of the same recipe with
      a `-1`-terminated count, beside the committed run in `BattleFormula_ResolveTargetResult` (`003863D0`)
      ([combat formula step table](../../08-Combat-Formula/Step-Table/combat-formula-step-table.md)).
- [x] ~~Whether the one function appearing in 1,349 vtables is the folded `ret 0` no-op already
      documented, or a shared destructor.~~ **AS-5 ANSWERED 2026-09-13 (FABLE): neither.** `0016D680` is four bytes, `mov rax, rcx; ret` (`0016D680`–`0016D683`) — it **returns its first argument**. It is not the folded `ret 0`: that is `0016D6A0`, a separate three-byte `ret 0` body. It cannot be a destructor: it writes no memory and calls nothing. In `rtti/methods.tsv` it fills **slot 1 of 1,329 classes** (all `Phyre::PClassDescriptor*` / `PClassDataMember*` descriptor types), **slot 2 of 18** (the `PNamedSemanticDescriptor` family) and **slot 0 of 2** (`eastl::allocator`, `eastl::allocator_memory_log`). In all 1,347 Phyre classes it is never at slot 0. `/OPT:ICF` folds every virtual whose body is *return this / return the first argument* onto this one address, so the address names no single method; which accessor each class declares at that slot is not recovered here. **AS-5.**
- [x] ~~Whether Phyre's `Reflection` glue and these RTTI vtables describe the same classes from two
      directions, and whether the 1,604 RTTI classes of the Phyre map are a subset of the 1,743
      `Phyre::*` vtables found here.~~ **AS-6.**
      *Narrowed 2026-09-14 (FABLE): the population half is answered, the glue half is not.*
      **GLUE HALF ANSWERED 2026-09-22 (FABLE): the two do NOT describe the same classes, and the
      reason is a category difference rather than a coverage gap — most of the `Phyre::*` vtables
      ARE the glue.**
      - **The `@Phyre@@` vtable population splits in two, and the split is total.** Of the
        **1,739** rows in `members/rtti-class-vtables.tsv` whose mangled name ends `@Phyre@@`,
        **1,522 (87.5 %)** carry a *mangled* class column — template instantiations whose leaf was
        never demangled — and only **217** are ordinary named classes. **Every one of the 1,522 is
        reflection machinery**, spanned by seventeen template heads with **zero** remainder:

        | template head | vtables | | template head | vtables |
        |---|--:|---|---|--:|
        | `PClassDescriptorForType` | **409** | | `PClassDescriptorWithoutDefaultConstructor` | 38 |
        | `PClassDescriptorAbstract` | 386 | | `PClassDescriptorWrapper` | 15 |
        | `PClassDescriptorConcrete` | 331 | | `PNamedSemanticDescriptorForType` | 14 |
        | `PMethodCallerConcrete` | 156 | | `PTypeDefault` | 12 |
        | `PClassDataMemberArrayDynamic` | 71 | | `PFunctionCallerConcrete` | 11 |
        | `PClassDataMemberPhyreArray` | 59 | | `PClassDataMemberPhyreSharray` | 10 |

      - **So the glue cannot describe them: a descriptor does not reflect itself.** These vtables
        are one per *reflected* type or member — the implementation of reflection, not its
        subjects. Asking whether the glue covers them is asking whether the machinery is its own
        input.
      - **On the 217 that ARE ordinary classes, the reflection names 111 and does not name 106.**
        The registrar artifact carries **399** distinct class names, of which 288 are not among
        those 217 — they sit in the mangled 1,522, or are non-Phyre types the descriptors also
        cover (`CD3D11_BLEND_DESC`, `Matrix3`, `Vector4`).

      > **Two independent numbers corroborate the reading rather than restating it.**
      > `PClassDescriptorForType` comes out at **409**, and `members/phyre-registrar-classes.tsv`
      > states **`registrars 409`** in its own header — one descriptor-for-type vtable per
      > registrar. And `PClassDescriptorWithoutDefaultConstructor` comes out at **38**, the figure
      > §8's own descriptor-kind table already carries. *Neither figure was used to build this
      > census; both were computed from the vtable table and then found to agree.*

      > **Controls, and a defect worth recording.** The pass reproduces the table's **2,286**
      > vtable rows and the registrar file's **399** names. *A first version of this comparison
      > reported “the reflection describes 6.4 % of the Phyre classes” and was wrong twice over:*
      > it split the registrar's `classes` cell on commas when the separator is ` | `, and it
      > compared demangled registrar names against an RTTI column that is mangled in 87.5 % of
      > rows. **The figure looked like a finding about the corpus and was a finding about the
      > parser.** **Static: two published artifacts, no code executed.**
      - **The two figures are one population in two units, not two populations.** Both tools walk the same 2,286-vtable
        RTTI graph (the table above). `rtti_recover.py` counts **classes** (1,604) and `vtable_map.py` counts
        **vtables** (1,743); multiple inheritance gives one class several.
      - **A fresh census confirms the containment.** Counting type-descriptor names whose decorated form ends in
        `@Phyre@@`: **1,802 type descriptors**, of which **1,733 own at least one vtable**, and **no vtable owner lacks a
        type descriptor**.
      - **The 69 descriptors with no vtable** are types named in the RTTI graph without being instantiated with a vtable.
        Examples: `PClassDescriptorAbstract<…>` over `PWorld`, `PClassDescriptor` and `PClassMember`; three
        `PClassDescriptorHeaderWithoutDefaultConstructor<…>`; and `PMethodCallerConcrete<PPhysicsWorld, …>` variants.
      - **Why 1,733 is not 1,604 or 1,743.** The difference is each tool's rule for what "`Phyre::`" means (outermost
        namespace of the decorated name versus the class's own namespace), not a different set of objects.
      - **Still open:** whether Phyre's reflection glue (the descriptor instances) describes exactly these RTTI classes.

## 6. Falsification pass 2026-09-02 (second) - AS-7 settled, and the game is not object-oriented

**Attack chosen.** The three-method discrepancy between the two independent RTTI recoveries. Standard
rule 3 says never characterise a construct from a truncated view; a gap of three in 6,886 is the size
that gets waved away.

### AS-7: the earlier tool over-counted by three

The three methods present in `rtti_recover.py` and absent from `vtable_map.py`:

| address | what it actually is | 16-byte aligned |
|---|---|---|
| `00444F4C` | `FUN_00444340` **+ 0xC0C** - `add ecx, [rsp+0x50]` | no |
| `006C6543` | `FUN_006C6230` **+ 0x313** - `mov rbx, [rsp+0x70]` | no |
| `00755F6D` | `FUN_007558E0` **+ 0x68D** - mid-instruction | no |

**All three point into the middle of a function body.** None is a function entry, none is aligned.
A vtable slot never points mid-function.

The cause is a one-line difference in acceptance: `rtti_recover.py` accepts any qword whose value
falls in the `.text` VA range; `vtable_map.py` requires the value to be a **known function entry**.
The three are qwords past the true end of three vtables - `PUtilityLOD` slot 3,
`VPDeferredLightingBase` slot 16, `PAnimation...PClassDataMemberArrayDynamic` slot 11 - where the
earlier tool's run continued one slot too far.

**The correct count is 6,883**, and the vtable count of **2,286 is confirmed by both.** **AS-7
closed.** A second difference remains: 25,794 named slots here against 25,603 there, 191 apart and
not explained by these three. **AS-8.**

### AS-1a: the missing link is reflection, not a missing edge

Pass 54 left open which game subsystem enters Phyre's physics interface, having found that six hops
of direct calls from every Bullet constructor reach no owned code. The vtable data says why that
search could never have succeeded.

**169 classes with a vtable have a physics type in their name, and their shape is this:**

```
Phyre::PInternal::PCallerImplementation::PCallerImplementation0::M::
        Phyre::PPhysics::VPPhysicsRigidBodyBase::?$PMethodCallerConcrete
Phyre::PInternal::PCallerImplementation::PCallerImplementation3::23::
        PPhysicsRigidBodyBase::W4PCollisionGroup::...::VPPhysicsWorld::?$PMethodCallerConcrete
```

These are **`PMethodCaller` objects** - one generated class per (return type, argument list, target
class) combination, each wrapping one physics method for **generic invocation through Phyre's
reflection system**. The call site does not name the callee; it invokes a caller object.

**So there is no edge to find.** The game reaches Phyre physics the same way it reaches everything
else in Phyre: through reflection. That also explains pass 51's measurement that `Reflection` is the
largest group at the seam with **617** functions - the seam *is* the reflection layer.

**Still open, narrowed:** `Phyre::PPhysics::VPPhysicsCharacterControllerBase` and
`VPPhysicsCharacterCamera` exist as classes with method callers. A character controller is exactly
the component that would move a player capsule through collision - but this database also documents
a complete
[battle locomotion solver](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)
that does its own obstruction tests. **Both cannot be the movement path, and presence is not use.**
**AS-1b.**

### The finding: FFXII's gameplay code is procedural, not object-oriented

Counting **owned** functions that appear in any named vtable:

| owner | virtual methods |
|---|---:|
| **Audio** | **504** |
| **Input** | **125** |
| Resource | 12 |
| Presentation | 5 |
| PlatformOnlineAchievements | 4 |
| CoreRuntimeScheduling | 2 |
| Save_Load_Settings, ActorEntity, RNG_Random_Selection | 1 each |

**CombatAction, CombatFormula, CombatAI, Movement, Party, Rewards, UI, WorldArea, StoryEvent - zero
between them.** `ActorEntity` has exactly one.

The gameplay systems this database documents in detail are **not classes**. They are procedures over
the flat record tables already documented - the
[battle record](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) at
`0x0208E690 + id*0x250`, the
[formula step table](../../08-Combat-Formula/Step-Table/combat-formula-step-table.md), the
[native command tables](../../01-Script-VM-Native-Bridge/Native-Command-Lifecycle/native-command-lifecycle.md).
Only the two subsystems that sit against middleware - **Audio** against SQEX Sound and **Input**
against the device layer - are object-oriented.

**This resolves three earlier observations into one architecture.** Gameplay does not call Phyre
(pass 51), gameplay is fully visible to a direct-call edge list, and the vtable recovery barely
touched gameplay - all three are the same fact. **The engine is C++ with reflection; the game on top
of it is C with tables.**

**Stated as measured.** This is a count of vtable membership, not a claim that no gameplay code uses
a virtual call. A gameplay function calling a middleware object's virtual method is still procedural
code doing so, and would not appear above.

## 7. Falsification pass 2026-09-02 (third) - AS-8 was my own tool, AS-1b is a negative

### AS-8: the 191-slot gap is a naming artifact in `vtable_map.py`

Comparing the two recoveries by **(address, slot)** instead of by (address, class, slot):

| | `rtti_recover.py` | `vtable_map.py` |
|---|---:|---:|
| distinct (address, slot) pairs | 7,081 | 7,078 |
| only in one | **3** (the AS-7 mid-function addresses) | **0** |
| (address, class, slot) triples | 25,603 | 25,794 |

**The underlying data is identical apart from the three already explained.** The 191 extra triples
are entirely **class-name strings**: the same slot attributed under more distinct names.

The cause is this tool's demangler, and the output shows it plainly:

```
Phyre::Phyre::PPhysics::VPPhysicsCharacterControllerBullet::?$PClassDescriptorForType
^^^^^^^^^^^^
```

`demangle()` splits the mangled name on `@` and reverses the segments. For a **template** class the
mangled form nests a second qualified name inside the first, so the outer namespace is emitted twice
and template arguments are flattened into the namespace path. The names are ugly and
over-differentiated; **the addresses and slots they carry are correct**, which is why every count in
this document that is keyed on addresses stands.

**AS-8 closed - no data defect, a cosmetic defect in this pass's own tool.** Recorded rather than
quietly fixed, because the doubled prefix appears verbatim in the class lists above and a reader will
otherwise think there are two `Phyre` namespaces. **AS-9** tracks replacing the demangler with a real
one.

### AS-1b: nothing instantiates Phyre's character controller

Seventeen classes match "CharacterController" or "CharacterCamera". **Sixteen of them are reflection
metadata, not objects:**

| class | vtable | kind |
|---|---|---|
| `VPPhysicsCharacterController::?$PClassDescriptor{ForType,Abstract,Concrete}` | `0xD71600`, `0xD718F0`, `0xD71BE8` | **descriptor** |
| `VPPhysicsCharacterControllerBase::?$PClassDescriptor{...}` | `0xD75F50`, `0xD760B0`, `0xD76258` | **descriptor** |
| `VPPhysicsCharacterControllerBullet::?$PClassDescriptor{...}` | `0xD70770`, `0xD70AB0`, `0xD70DD8` | **descriptor** |
| `VPPhysicsCharacterCamera::?$PClassDescriptor{...}` | `0xD74B58`, `0xD74D60`, `0xD74F20` | **descriptor** |
| `Phyre::PPhysics::PPhysicsCharacterCamera` | `0xD79AE8` | **object** |

**There is no object vtable for `PPhysicsCharacterController` in the named set at all** - only the
three descriptors that register the type with Phyre's reflection system. The one real object vtable
in this family is the *camera*.

Three further measurements:

- **Every function writing any of these vtables is `CodeDomain.Phyre`.** No game code, no unowned
  adapter - 18 writers, all Phyre.
- **None of these vtable addresses appears anywhere in a data section.** They are not stored in a
  table, a factory list or a registry that something else indexes.
- `VPPhysicsCharacterControllerBullet` exists as a type, so Phyre's character controller *has* a
  Bullet-backed implementation - registered, and that is all that can be said for it.

**Reading:** Phyre's character controller is present as **reflection metadata for a type the game
does not instantiate**. Set against the fully documented
[battle locomotion solver](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)
with its own obstruction tests, turn hysteresis and stall timer, the movement path is **the game's
own code, not Phyre's character controller.**

**The limit of that reading, stated plainly.** Reflection-driven instantiation - the mechanism AS-1a
established for physics generally - would be invisible to all three measurements above. This is
therefore **strong absence of evidence, not evidence of absence**, and it is the strongest form
available without running the game. What tips it is not the negative but the positive: the
locomotion solver is documented at tier 1 and does the job. **AS-1b closed on that basis; reopen if
the character controller is ever seen in a reflection registration table.**

## 8. Falsification pass 2026-09-02 (fourth) - AS-4: the unnamed runs are mostly not tables

**3,639 of the 3,953 unnamed runs are a single slot** - 92.1 % of the runs, 58.5 % of the slots.
Another 293 runs are two or three slots.

> **The figures above reproduce exactly and need no correction. The INFERENCE that followed them
> was half wrong, and the half that fails is the `.data` side.** An independent rebuild under this
> section's own definition gave 3,957 runs / 3,643 singletons against 3,953 / 3,639 -- four runs
> apart, both derived percentages identical to the decimal.
>
> This section read a one-slot run as *"an individual stored function pointer - a callback
> registered in a global or a struct field - not a table"*. **Regrouped as arithmetic progressions
> rather than contiguous runs:**
>
> ```
> .rdata  3,202 slots | 1,976 runs / 1,963 single | 1,836 groups / 1,807 single |  92% survive
> .data   3,015 slots | 1,977 runs / 1,678 single |   572 groups /   301 single |  18% survive
> ```
>
> **In `.rdata` the reading holds** -- 92 % of its singletons survive regrouping, because `.rdata`
> genuinely holds arrays of pointers. **In `.data` it fails**: 82 % of its singletons are members
> of arithmetic progressions of three or more. A record with one pointer field puts consecutive
> pointers one *stride* apart, so **every such table shatters into as many "single-slot runs" as
> it has records.** Recovered this way: CombatAction runs at stride `0x18`/`0x30` (96, 48, 37
> slots), the Presentation authored-command table at `01EFFAF0` stride `0x10` (73), and several
> `Script_VM_Native_Bridge` progressions.
>
> **1,533 of the 3,643 (42 %) are not individual stored pointers**, and essentially all of the
> failure is on the `.data` side. This population straddles both sections in almost equal parts --
> 3,202 `.rdata` slots against 3,015 `.data` -- which is why one inference could not cover it.
>
> **Bound, not measurement.** The regrouping is a greedy longest-progression search, which is
> itself a hypothesis: in a dense region it can merge slots from different structures into one
> spurious progression, and two reported `Script_VM_Native_Bridge` progressions (strides `0xC0`
> and `0xA0`) span the `0x20`-stride command tables and are search artifacts. **So 301 is a lower
> bound and the true `.data` singleton count lies between 301 and 1,678.** The direction is not in
> doubt; reporting 301 as exact would repeat, one level down, the defect this check exists to
> find.

**Only ten runs exceed ten slots**, and they hold **1,782 slots between them**. Those are the real
dispatch tables, and the census validates itself on one that was already documented:

| run | slots | what it is |
|---|---:|---|
| `01EFA5C0` | **202** | the [combat formula step table](../../08-Combat-Formula/Step-Table/combat-formula-step-table.md) - **exact match**, independently re-derived |
| `01EEC460` + 3 more | 337 | one table, not four: the [battle action handler table](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md) |
| `008C31D8` | 1,172 | **not a dispatch table** — the C++ initializer table (`__xc_a`..`__xc_z`), already documented in [static initialization order](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md). **AS-10 closed** |
| `01F41E98`, `01CEB070` | 26, 20 | `Audio`-owned |

**The formula step table came back at exactly `0x01EFA5C0` with exactly 202 slots**, and its
interpreter was found at `call qword ptr [rbx + rax*8 + 0x1DDA5C0]` - matching the existing document
to the byte, by a method that knew nothing about it. It also surfaced a **second** interpreter site
the document does not cite: `003859FF` in `00385680` alongside `003863D0` in `00385F60`. **AS-11.**

The 42 no-op slots in that table are `0016D6A0`, which the GFZ labels **`_guard_check_icall`** - the
Control Flow Guard stub, three bytes, folded by `/OPT:ICF` and reused as a placeholder. That is
consistent with the existing document's reading of it as a bare `ret 0`; the name is the folded
label, not a fourth meaning.

**AS-4 answered.** The unnamed runs are overwhelmingly individual function pointers, not tables;
the tables among them are ten, and two of the largest are now documented.

## 9. AS-10 closed — the largest run is not a table

The 1,172-slot run at `008C31D8` is the **C++ dynamic initializer table**, and this database already
documented it. Three measurements identify it without needing that document:

- **All 1,172 targets are distinct.** Every real dispatch table found so far repeats heavily — the
  battle action table is 8 distinct handlers across 341 slots, the formula step table 152 across 202.
  **A table with no repeats is a list, not a switch.**
- **Zero references into the span**, from code or data. It is walked from *outside* its bounds: the
  CRT holds `__xc_a` at `008C31D0`, the null qword immediately **before** the run, which is why a
  scan of the span itself finds nothing.
- **Not sorted** (51 % ascending) and ordered in owner blocks — link order.

**Correction to section 8.** That section called the ten runs over ten slots "the real dispatch
tables". **The largest of them is not a dispatch table at all**, and the criterion that separates
them is repetition, not length.

## 12. Why the two RTTI tools disagree by 195 rows — and why neither is wrong

`vtable_map.py` emits **25,798** rows; `rtti_recover.py` emits **25,603**. The gap was blamed on the
demangler defect. **It is not caused by that**, and correcting the demangler does not move it — the old
splitter was **injective**, so it produced ugly names but never merged or multiplied a count.

**The real cause, measured:** the two tools enumerate different things.

| | `vtable_map.py` | `rtti_recover.py` |
|---|---|---|
| keyed by | **vtable address** | **class name** |
| distinct keys | **2,286 vtables** | **2,133 classes** |
| rows | 25,798 | 25,603 |

Joining the two outputs on `(target, slot)` — which is name-independent, and therefore immune to the
demangler difference — reconciles the gap **exactly**:

```
(target,slot) pairs with differing multiplicity :  32
sum of positive differences                     : +198
rows present in methods.tsv only                :    3
                                        198 - 3 =  195   <- the entire gap
```

~~**Every surplus row is `/OPT:ICF` COMDAT folding**, and it is concentrated in two places:~~ **PARTLY RETRACTED — the surplus rows ARE folded code, but folding is not what makes the two counts differ. See section 13.** The concentration is real:

```
0067E690 slot 0   123 rows vs 46   Phyre::PInternal::PCallerImplementation
006B4170 slot 0    45 rows vs 12   Phyre::PInternal::PCallerImplementation
005C5230 slot 3    43 rows vs 19   Phyre::PInternal::PCallerImplementation
00865550 slot 0    14 rows vs  9   Steam ?$CCallbackImpl
```

The `PCallerImplementation` vtables sit in a **contiguous array at a 0x30 stride** — `00D34968`,
`00D34998`, `00D349C8`, `00D349F8`, `00D34A28`… — each a **separate template instantiation with its own
vtable**, all sharing **one folded method body**. Six 8-byte slots is exactly 0x30.

~~So an address-keyed tool sees 123 vtables pointing at `0067E690`; a name-keyed tool sees 46 class
names.~~ **WRONG, corrected in section 13.** `vtable_map.py` gives those 123 vtables **123 distinct
class names**, not 46 — it collapses nothing. The 46 is `rtti_recover.py`'s figure, and the reason it
is 46 is **its demangler, not the folding**.

> ~~**This is the `/OPT:ICF` consequence stated generally:** any count keyed on function address will
> come in below a count keyed on type identity, and the difference is not error in either — it is the
> folding.~~ **RETRACTED — section 13.** The generalisation is backwards *and* the arithmetic does not
> work: folding affects **18,720** surplus vtables while the gap is **195**. **The two tools agree on
> 98.8 % of all folded pairs.**

## 13. Correction — the gap is a demangler, not the folding

Section 12's explanation was checked by the peer session that raised it and **does not survive the
arithmetic.** Recorded here in full, because the mechanism it named is real and still gets the wrong
answer.

### The objection that broke it

If an address-keyed count diverged from a type-keyed one *because of folding*, the gap would be the
size of the folding:

```
(target,slot) pairs held by more than one vtable :  2,704
surplus vtables over those pairs                 : 18,720
the gap being explained                          :    195
```

**Two orders of magnitude out.** And the decisive measurement:

```
folded pairs where the two tools AGREE exactly : 2,672 / 2,704   (98.8 %)
folded pairs where they disagree               :    32           (+198 rows)
```

**Both tools handle folding identically almost everywhere.** Folding is a property of the binary that
each tool sees equally; it cannot by itself make them differ.

### They also recover exactly the same vtables

The recall hypothesis dies too — `classes.tsv`'s `vtables` column **sums to 2,286**, the same number
`vtable_map.py` reports:

```
vtable_map.py     2,286 vtables  ->  2,248 distinct class strings
rtti_recover.py   2,286 vtables  ->  2,133 classes
```

**Same 2,286 vtables. Different numbers of names for them.**

### The actual cause: template arguments are dropped

`rtti_recover.py`'s demangler **discards template arguments**, so every instantiation of one template
collapses to a single class string:

```
Phyre::PAnimation::VPAnimatableComponent::?$PMethodCallerConcrete   16 vtables
Phyre::PScene::VPNode::?$PMethodCallerConcrete                      10 vtables
Phyre::PFramework::VPApplication::?$PMethodCallerConcrete            9 vtables
```

`?$PMethodCallerConcrete` with **no argument list** is the signature of the defect — sixteen distinct
types wearing one name. `vtable_map.py` keeps them apart, which is why 2,248 > 2,133.

So at `0067E690` slot 0: **123 vtables, 123 distinct names in `vtable_map.py`, collapsing to 46 classes
under `rtti_recover.py`'s naming.** The 46 was never a count of vtables.

**And the collapse is unrecoverable from the output** — `classes.tsv`'s `mangled` column is **empty on
all 2,133 rows**, so nothing downstream can undo it.

### What is actually true

| | |
|---|---|
| both tools recover | **the same 2,286 vtables** |
| the surplus rows are | genuinely folded code — that part of section 12 stands |
| but the gap is caused by | **`rtti_recover.py` collapsing template instantiations by name** |
| folding's role | it creates the many-vtables-per-target shape the collapse then acts on |

**Folding is the setting, not the cause.** It supplies 18,720 opportunities; the demangler converts 198
of them into a discrepancy, in the 32 cases where the collapsing types share a `(target, slot)`.

> **The rule worth keeping is narrower than section 12's:** before explaining a difference between two
> counts, **check that the proposed mechanism is the right SIZE**. A mechanism that operates on 18,720
> rows is not an explanation for a gap of 195 — it is a mechanism that is present, which is not the
> same thing. **Section 12 named something real and let its reality stand in for a fit.**

## 14. The gap is closed — 195 rows down to 1, and the last 1 is understood

Section 13 identified `rtti_recover.py`'s demangler as the cause. **It has now been fixed and the
prediction held.**

### Three defects, not one

Reading the tool to fix it found the demangler was the *second* of three:

```python
NAME_RE = re.compile(rb'\.\?A[VU][\x21-\x7e]{0,250}?@@')   # BEFORE
```

1. **The harvest regex stopped at the first `@@`.** A type name is **NUL-terminated and contains
   `@@` internally** — a template argument list is itself `@@`-terminated — so **every template name
   was truncated before it reached the demangler.** This is the trap the peer session documented
   while fixing `vtable_map.py`; the same trap was live in this tool.
2. **The demangler dropped the argument list**, collapsing instantiations (section 13).
3. **The 250-character bound was too short.** Exactly **two** real type descriptors in this image are
   **264 and 265 characters** — both `?$PMethodCallerConcrete` on `PPhysicsWorld` — and both were
   silently dropped. That is the missing 2 of 2,286 vtables.

A fourth, in the writer: `classes.tsv`'s **`mangled` column was hardcoded to `''`**. The evidence that
would have exposed the collapse was being discarded on write.

### The two tools now agree

```
                        before        after      vtable_map.py
classes                  2,133        2,248          2,248
vtables                  2,284        2,286          2,286
methods.tsv rows        25,603       25,797         25,798 (vtables.tsv)
the gap                    195            1
max vtables per class       16            3
```

**The validation that proves only the broken half moved** — the check the peer session named, because
it is the one that caught its own error:

```
plain (non-template) class names : 588 before, 588 after
byte-identical                   : 573
differing                        :  15   <- ALL function-local classes
```

The 15 are names like `btCollisionWorld::??objectQuerySingle::?BG::BridgeTriangleConvexcastCallback`,
which dbghelp renders with the enclosing function's real signature. **No ordinary class name changed.**

### The last row, and why it is not a defect

Seven `(target, slot)` pairs still differ, netting **1 row**. Both groups are understood:

| | rows | cause |
|---|---:|---|
| `00444F4C`, `006C6543`, `00755F6D` | **+3** methods-only | **they are inline ASCII strings, not pointers** — see below. `vtable_map.py` requires a known function *entry* and rejects them; `rtti_recover.py` accepts any `.text` address. |
| `007AD440` slots 3, 4, 5, 7 | **−4** vtables-only | **one class with several vtables.** `WASAPIDevice` has **3 vtables and 24 methods**; keyed by `(class, slot)` its secondary vtables collapse — **correctly**, since they are the same class. |

**Neither is a naming defect, and they pull in opposite directions**, which is why the net is 1 rather
than 7. **AS-9a is closed.**

> **The general shape, now that all three defects are known:** every one of them **destroyed
> information at a boundary** — at harvest (`@@`), at decode (arguments), at width (250), at write
> (`mangled`). None corrupted a value; each **discarded** one, and each produced a smaller, tidier,
> entirely plausible number. **A pipeline that loses data silently reports success.**

### The +3 named: a 3-letter field name aliasing as a code pointer

The three false positives are not noise. **Read as little-endian qwords they are inline ASCII**, and
the bytes are in the image:

```
00D85180  4c4f440000000000  504c4f444c6576656c    "LOD"  then  "PLODLevel"
00D5A248  43656c0000000000  507265636f6d707574..  "Cel"  then  "PrecomputeSingleScattering"
00D337A0  6d5f750000000000                        "m_u"
```

**Phyre stores short field names inline in the reflection record** — SSO-style, up to 7 characters
plus a NUL — rather than as a pointer to a string. An inline `"LOD"` **is** the qword
`0x0000000000444F4C`, and that value happens to land inside `.text`'s VA range. So does `"Cel"`, and
so does `"m_u"`.

**That is why there are exactly three and not thirty:** it needs a name of the right length whose
letters, read as a little-endian integer, fall in the code range. The neighbours — `PLODLevel`,
`PrecomputeSingleScattering` — place all three in Phyre's field-descriptor tables.

> **The guard that works is an entry check, not a range check.** "Points into `.text`" admits any
> 3-letter name with the right bytes. **"Is a known function entry"** rejects all three. **Anything
> scanning pointer runs over Phyre `.rdata` needs the stronger test**, because the reflection tables
> are full of inline short strings by construction.

**This is the inverse of the four defects above.** Those *destroyed* information at a boundary; this
one **creates** it — a value that was never a pointer being admitted as one. Both produce a plausible
number and neither raises an error. The asymmetry is that **a discarded value leaves no trace, while
an invented one leaves a decodable byte pattern**, which is why this took one check to explain and the
truncation took three passes.

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This page named `0069FB10` only at its entry. The interior addresses below were read in the
shipping image.

| body | interior cite | what is there |
|---|---|---|
| `0069FB10` | `006A01EA` | `call 0083A3A0` inside a body that also calls `0085E680`, `00833390`, `00852DB0`, `006A2320`, `006A4A60` — a multi-phase construction/registration body |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** `BattleUnit_RunPeriodicCombatMaintenance` calls a function this page cites.
- **Audio — CLIENT (6 edges).** 6 inbound (Audio bodies `00361DE0`, `00363FD0`, `003623C0` call page-cited `0036DD80`, `007AD440`). Substantive edges include `007AD440` is called by `007B6050`; `007AD440` is called by `007F0820`; `007AD440` is called by `007EFB60`; the remaining edges run through shared helpers the page cites.
- **CombatFormula — CLIENT and SERVICE (19 edges).** 3 inbound (CombatFormula bodies `BattleFormula_ResolveTargetResult` (00385F60), `BattleFormula_QueryResolvedScalarPreview` (00308B90), `BattleFormula_EvaluateTargetPreview` (00385680) call page-cited `BattleFormula_UpdateLowHpThresholdStatusMask` (00385B10), `BattleFormula_ResolveTargetResult` (00385F60), `BattleFormula_ApplyPreResolutionTargetGates` (00390AB0)); 16 outbound (page-cited `BattleFormula_EvaluateTargetPreview` (00385680), `BattleFormula_ResolveTargetResult` (00385F60), `BattleFormula_ApplyPreResolutionTargetGates` (00390AB0) call CombatFormula bodies `BattleStats_FindOwningBattleUnit` (0031B860), `BattleFormula_BuildEvaluationContext` (003847C0), `BattleFormula_ResetScratchState` (003849B0)). Substantive edges include `BattleFormula_EvaluateTargetPreview` (00385680) calls `BattleFormula_ApplyPreResolutionTargetGates` (00390AB0); `BattleFormula_EvaluateTargetPreview` (00385680) calls `BattleFormula_BuildEvaluationContext` (003847C0); `BattleFormula_EvaluateTargetPreview` (00385680) calls `BattleFormula_ResetScratchState` (003849B0); `BattleFormula_EvaluateTargetPreview` (00385680) calls `BattleStats_ResolveByActorHandle` (00320A70); the remaining edges run through shared helpers the page cites.
- **Presentation — CLIENT and SERVICE (193 edges).** 181 inbound (Presentation bodies `00438860`, `004355D0`, `004434D0` call page-cited `0020E680`, `0036DD80`, `0039CDC0`); 12 outbound (page-cited `00444340`, `0039F9F0`, `0017F850` call Presentation bodies `001E8580`, `RenderCommand_SubmitCurrentBufferAndSwap` (003A1DB0), `003A3D20`). Substantive edges include `0016D680` is called by `00183C60`; `0016D680` is called by `00183A00`; `0016D680` is called by `003EE2D0`; `0016D680` is called by `003ED8A0`; the remaining edges run through shared helpers the page cites.
- **UI — CLIENT and SERVICE (9 edges).** 7 inbound (UI bodies `002D28E0`, `002AF960`, `002AC5F0` call page-cited `0017F850`, `002AC5F0`, `001A1470`); 2 outbound (page-cited `002AC5F0` call UI bodies `002B2150`, `002AE610`). Substantive edges include `0017F850` is called by `002D28E0`; `0017F850` is called by `002AF960`; `0017F850` is called by `002AC5F0`; `001A1470` is called by `0018EEE0`; the remaining edges run through shared helpers the page cites.
## Zero at load does not mean unreadable — 346 globals named by RTTI (FABLE, 2026-09-16)

**A global in the uninitialised tail of `.data` is zero at load. It does not follow that what lives
there is unknowable**, and the database has been reasoning as if it did. `PH-2` asserted of
`02CAA0A0` that it *"is in `.bss` and is therefore zero at load, so the descriptor is built at
runtime and cannot be read out of the image at all"* — and that global is row 4 of the table below.

**The shape.** A CRT static initializer, running before `main`, constructs the object and then
writes a **link-time constant** into it — the vtable address, in `.rdata`. `00160210` is the worked
example: `lea rcx, [02CAA0A0]` / `call 00597690` / `and dword [02CAA19C], ~2` /
`lea rax, [00D249A8]` / `mov [02CAA0A0], rax` / `jmp atexit` with `008A8150` as the destructor. The
vtable address never varies between runs, so **the object's class is fixed at link time** and the
qword before the vtable is the RTTI Complete Object Locator, which names it.

**The reach, measured.** Over the **1,172 listed functions** in the CRT initializer table
`008C31D8`–`008C5678`, there are **450 writes of an `.rdata` constant into a zero-at-load global**
across **379 distinct initializers**, and **346 of them resolve to an RTTI name**. The census is
[`members/zero-at-load-objects-named-by-rtti.tsv`](members/zero-at-load-objects-named-by-rtti.tsv).

| family | count |
|---|---:|
| `PClassDescriptorConcrete<T>` | 261 |
| `PClassDescriptorWithoutDefaultConstructor<T>` | 38 |
| **SQEX `Sd` sound driver and siblings** | **33** |
| other Phyre | 8 |
| `PClassDescriptorHeader<T>` | 4 |
| other | 2 |

**The 33 SQEX rows are the ones worth noticing** — they are not PhyreEngine at all but Square
Enix's own sound driver, and they carry their element types with them:
`SQEX::Sd::Driver::FixedQueue<0, ACTION*>` at `02EAD010` and `02EAD040`,
`SQEX::Sd::Lay::FixedQueue<2, ACTION*>` at `02EADD70`.

**What is new here is the systematisation, not the technique.** `T-8`, `G-24`, `DK-2`, `PCD-5` and
`UQ-283` were each answered by reading exactly these vtables, one at a time, between 2026-09-14 and
2026-09-16. **Nobody had run it across the image**, which is why a row published on 2026-09-15 could
still carry the unreadability premise for a global that had been nameable all along.
[`Reflection-And-Class-Metadata/members/pclassdescriptor-static-initialisers.tsv`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/pclassdescriptor-static-initialisers.tsv)
lists 254 of the initializer *functions*; this table resolves the *globals* they fill, which that
one does not carry.

**How to use it.** Before writing that a zero-at-load address cannot be read from the image, look it
up. If it is in the table, its class is known and its virtual methods are ordinary readable bodies.

**How much of it is new, measured.** Of the 346, **only 42 are mentioned anywhere in the `.md` corpus at all**, across 21 pages — so **304 of the 346 are objects no page has ever mentioned**. Of the 42 that are mentioned, **17 appear on a page that never carries their class name**, including `02CBB900` `PTexture2D` on `Application-Root/game-application.md` and four SQEX `Sd` containers on `Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`. **That is the work queue this table creates**, and it is why the count matters more than the handful of rows it closes today.

**What the table does not say.** It names the object and fixes its vtable. It says **nothing about
the object's other fields** — whatever the constructor computes at `00597690` and its siblings is
genuinely runtime state, and the 104 writes that did not resolve to an RTTI name are unclassified
here. Names are the **decorated MSVC form, carried verbatim and not demangled**: a demangler that
guesses template arguments invents names, and this is evidence.

## The `00385680`/`00385F60` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

`00385680` (`BattleFormula_EvaluateTargetPreview`, ~1125 B) — `r11 = rsp`
`0xA0` frame (`00385680`/`00385687`).

| member | role | interior |
| --- | --- | --- |
| `00390AB0` | `rbp = r8` eval body (`00390ABF`) | [`00390ABF`](../../_index/ADDRESS-INDEX.md) |

`00385F60` (`BattleFormula_ResolveTargetResult`, ~144 B) —
five-register body (`00385F60`/`00385F65`).

| member | role | interior |
| --- | --- | --- |
| `00385B10` | `rcx` non-null gate; `dword[r8+0x2C]`/`dword[rcx+0x48]` read (`00385B13`/`00385B20`) | [`00385B13`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-36 update (2026-09-19) - `006A1DD0`

`006A1DD0` (676 B) is an RTTI/EH body - `008C5F80`-`008C5FB0` rdata run, `00D7AB50` string, `00861F14`/`0083B580`/`00808C40`/`0069ECE0`. Interior anchor `006A1F76` (an `00861F14` call).

## SWE2-EC7-38 update (2026-09-19) - `006A1A70`

`006A1A70` (498 B) is an RTTI/EH body - `01CEBBA8`/`00D7AB10`, `00861F14`/`0069ECE0`. Interior anchor `006A1BB9` (an `00861F14` call).

## SWE2-EC7-49 update (2026-09-19) - `006A2320`

`006A2320` (194 B) is a body - `0083A3A0` single call. Interior anchor `006A2382` (the `0083A3A0` call).

## SWE2-EC7-78 update (2026-09-20) - `0069ECE0` kind-conditional dual fill measured

`0069ECE0` (111 B) fills `rdx+0x20`/`+0x28` from a `+0x104` kind
test: `byte[rcx+0x104] & 2` makes `+0x20 = [rcx+0x108]` and `+0x28 =
02E48BD0` when that pointer is non-NULL; `[r8+0x104] == 4` does the
same through `[r8+0x108]`/`02E47ED0`. Both fall back to leaving the
fields zeroed - the two-kind capability read.
Interior anchor `0069ED03` (the `+0x108` load).

## SWE2-EC7-91 update (2026-09-20) - `0039F780` + `0039B860` + `00395CF0` measured

`0039F780` (624 B) is the display-record builder sibling of
`0039F9F0`: `0020E680` allocates, `008642A0(4)` and `0039CDC0`
produce the output record, eight `divss` component ratios
([rdi]/[rsi] lanes) land at `+0x00`..`+0x34` of its `+8` block
and 16 byte->float lanes at `+0x00`..`+0x3C` of its `+0x10`
block; `+0x40` = 4, `+0x38`/`+0x48` take the `[r15]` pair,
`0020E670` publishes and the body tails `0020E630`.
Interior anchor `0039F7A4` (the `0020E680` call).

`0039B860` (25 B) is the four-argument forwarder the callers
run: r9 is staged to the stack and `0039B880(rcx, rdx, r8, 4)`
does the work.
Interior anchor `0039B86F` (the `0039B880` call).

`00395CF0` (1,521 B) is the widest of the staged transform
passes: two input vec4s ([rcx] and [r8]) seed the `022D9xxx`
workbench, and each loop iteration advances the source cursor
0x10 bytes, accumulates three-component dot products with
`mulss`/`addss` chains, renormalizes through `00861F14` with a
zero-fallback constant, and `movups`-writes the staged vec4 to
`[rax-0x10]` until the `022D9xxx` watermark pointer matches.
Interior anchor `00396119` (the `00861F14` call).

## SWE2-EC7-91 update (2026-09-20) - `00395780` two-input staged transform measured

`00395780` (1,381 B) is the second widest of the staged transform
passes: two input vec4s ([rcx] and [r8]) seed the `022D9xxx`
workbench, each iteration advances the source 0x10 bytes and
accumulates the dot-product chains, `00861F14` renormalizes with a
zero-fallback, `0036DD80` runs at the tail of each iteration, and
`movups [rax-0x10]` emits each staged vec4 until the watermark
matches.
Interior anchor `00395B7D` (the `00861F14` call).

## SWE2-EC7-92 update (2026-09-20) - `00394DA0` matrix-vector multiply measured

`00394DA0` (171 B) is the pure 4x3 row-major matrix-vector multiply
the `00444340` caller family runs: each output component at `r8` is the
three-term dot `m[row][0]*v[0] + m[row][1]*v[1] + m[row][2]*v[2]`,
computed scalar (`mulss`/`addss`) with no side effects beyond the four
output stores.
Interior anchor `00394DBC` (the first `addss` accumulate).

## SWE2-EC7-113 update (2026-09-21) - `00864210` measured

`00864210` (143 B) is the
triple-buffer initialiser
`008642A0` runs on a fresh
record: `edx << 4` bytes
are allocated three times
through `001A1470` on the
`01F7F4C0` allocator and
stored at `+0x08`, `+0x10`,
`+0x18` - each allocation
immediately handed back to
`0016D6A0` on the same
allocator object - then
`dword[+0x60]` takes the
element count. Three
parallel `n*0x10` arrays
under one record.
Interior anchor `00864291`
(the `+0x60` count store).

## SWE2-EC7-117 update (2026-09-21) - `006A4A60` measured

`006A4A60` (965 B) is the
transform commit
`0069FB10` and `006A4A40`
run on the scene node:
when `qword[+0x118]` is
live it stores the
`+0x78`/`+0x7C`/`+0x80`
vector into `+0x160` and
the `+0x68`/`+0x6C`/`+0x70`
vector into `+0x150`,
builds the matrix from the
`+0x48` quat and
`+0x38..+0x40` scale via
`006A57C0` + `00853FE0`,
and when `dl` is set walks
the `+0xB0`-count `+0xB8`
child list - each child's
`+0x50` vector scales by
`+0x88..+0x90` and goes to
`vtable[+0x28]` through
`[+0x120]`->`+0x28`->
`+0x40 + i*0x20` - then
`vtable[+0x78]` on
`+0x120`. The `+0xE9`
dirty flag wraps a
`+0xC8`->`+0x10`->`+0x60`
`vtable[+0xA0]` pre-call
and a `vtable[+0x130]`
post-call with the `+0xE0`
sub-index bitmask, plus
two `0083A030` clears.
Interior anchor `006A4B85`
(the `006A57C0` call).

## SWE2-EC7-119 update (2026-09-21) - `006A57C0` measured

`006A57C0` (391 B) is the
normalized
quaternion-to-matrix
builder `006A4A60`,
`006A2600`, `0083B580` and
`0084C6B0` call: it computes
`2 / (x*x + y*y + z*z +
w*w)` from `rdx`'s four
floats, multiplies each
component through, then
writes the nine rotation
entries to `rcx` rows at
`+0`/`+0x10`/`+0x20` with
`+0xC`, `+0x1C`, `+0x2C`
zeroed - the scale/rotation
source of the transform
commit.
Interior anchor `006A585A`
(the `divss` normalizer).
