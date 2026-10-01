---
system: The return-value adapter family — 403 identical generated trampolines over 409 classes
category: 24-Compiler-And-CRT-Runtime
status: AUDITED
owner_layer: CodeDomain:CompilerGenerated.Adapters; no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 18 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  project: work/headless_gn160/GFZ_GN160, CHECKPOINT VERIFIED 2026-09-07
last_reviewed: 2026-09-08
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-return-value-adapter-family-pass-1
  last_pass_kind: falsification
  crossref_clean: true
  reopened_count: 0
function_families:
  - "return-value adapters (DF-4) | C | members/df4-return-value-adapters.tsv | 402 | PhyreEngine reflection template, not FFXII code: the generated slot-5 accessor adapter of PClassDescriptorForType / Abstract / Concrete<T>. Members = every .text match of the 26-byte template 40 53 48 83 EC 20 48 8B CA 49 8B D8 E8 rel32 48 89 03 48 83 C4 20 5B C3 (members/select_generated_adapters.py) - 403 matches, all 26-byte census entries, 403 distinct call targets; members/vtable_slots.py places every member only at slot 5 of RTTI PClassDescriptor vtables (1185 appearances: 367 x3, 34 x2, one x6, one x10). Boundary: the adapter bodies only (move arg2 into rcx, call, store rax through arg3); their 403 call targets, the per-class accessors, are NOT covered, and the shared adapters 006B2950 / 006B2970 serve several vector and matrix classes (sec.9)"
  - "owned-buffer reset adapters (DF-1) | C | members/df1-owned-buffer-reset-adapters.tsv | 46 | PhyreEngine reflection template, not FFXII code: descriptor slot 11, release an array instance's owned buffer. Members = the 59-byte body group at slot 11 of RTTI PClassDescriptor vtables (members/descriptor_slot_census.py 11 OUT 59; slot 11 holds 59 distinct body shapes, this is the 46-member one), each member present three times at slot 11 only (138 appearances), every member's single call is 00584730 _aligned_free: if the header dword +0 has bit 31 clear and +8 is non-null, free it, zero +8 and +0, return true (DF-1). Boundary: the 46 bodies; 00584730 and the other slot-11 shapes are NOT covered"
---

# The return-value adapter family

> **409 of this category's functions are one generated idiom, and ~~351~~ → **403** of them are
> byte-for-byte the same shape in 26 bytes** (shape census, 2026-09-13; `351` was a *tag* count).
> They are the seam between PhyreEngine's reflection system and the real functions it calls.
>
> **They cover exactly 409 classes, one adapter each, and every one of their 1,185 vtable
> appearances is slot 5.**
>
> **Anyone counting how much code FFXII contains should know that 403 of the count is one template.**

## 1. What the player sees

Nothing — this is compiler output, not game behaviour.

But it changes what a *count* means. FFXII's executable has tens of thousands of functions, and a
reader naturally treats that as a measure of how much the game does. **A large block of those
functions are not things the game does at all**: they are a few lines the compiler wrote out once per
class, so that a generic system could call a specific function without knowing its shape.

For anyone hooking the engine, they matter for the opposite reason: **these tiny functions are
exactly where a generic call becomes a specific one**, which is the most useful place to stand.

## 2. Native mechanism

### The family

**409 functions carry a `Runtime.Callback` code-domain tag, totalling 13,254 bytes** — an average of
**32 bytes each**. They divide as:

| tag | functions |
|---|---:|
| `Runtime.Callback.ReturnValueAdapter` | **351** |
| `Runtime.Callback.OwnedBufferResetAdapter` | 46 |
| `Lua.Runtime.CallbackAdapter` | 3 |
| nine one-off dispatchers (`LinkedListFirstSuccessDispatch`, `FourSlotDeferredInvocationDrain`, `DoubleBufferedPointerDrainAndFlip`, …) | 9 |

### The shape — all 403 are exactly 26 bytes

```asm
push rbx
sub  rsp, 0x20
mov  rcx, rdx        ; drop argument 1, shift argument 2 into place
mov  rbx, r8         ; argument 3 is an out-pointer
call <target>        ; the only field that differs between the 351
mov  [rbx], rax      ; store the callee's return value through the pointer
add  rsp, 0x20
pop  rbx
ret
```

**Every one of the 403 has size 26** — not "about 26"; the size column has a single value across the
whole family, and a byte-template scan of `.text` (the 26 bytes with the `call` displacement
wildcarded) returns **403 matches, 403 distinct call targets, no overlaps, all 403 present in the
function graph at exactly 26 bytes**. **They differ in exactly one thing: the `call` target.**

> Note the leading `40` — a redundant REX prefix on `push rbx` — is what makes the body 26 bytes
> rather than 25.

> **The adapter converts a returning function into a writing one.** A caller that knows only the
> signature *(context, argument, result\*)* can invoke any function that takes one argument and
> returns a value, without knowing what that value is.

### Where they live — the class-descriptor vtables

~~Each adapter appears **exactly three times** in `.rdata`, and the three are the vtables of one
class's descriptor triple.~~ **Corrected 2026-09-13: 367 of the 403 appear three times; 34 appear
twice, one appears six times and one ten.** The three are the vtables of one class's descriptor
triple — see §9 for what the other 36 are. Walking back from each slot to the RTTI complete-object-locator names
them:

```
.?AV?$PClassDescriptorForType@VPTimeScaleOffsetController@PAnimation@Phyre@@@Phyre@@
.?AV?$PClassDescriptorAbstract@VPTimeScaleOffsetController@PAnimation@Phyre@@@Phyre@@
.?AV?$PClassDescriptorConcrete@VPTimeScaleOffsetController@PAnimation@Phyre@@@Phyre@@
```

**`ForType` / `Abstract` / `Concrete` — the same three-descriptor pattern this database already
records** for `PClusterHeaderBase` in
[`../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md).

~~**Sampling 120 of the 351 gives 93 distinct classes** — one or two adapters per class … **11 of
the 120 could not be resolved to a class** and are not counted.~~ **Superseded 2026-09-13 by a full
census (`DF-3`): 409 classes, exactly one adapter each, and every appearance resolved — nothing
unresolved.** Spread across animation, rendering, scene and shader types (`PAnimationEvent`,
`PSceneRenderPass`, `PShaderParameterDefinition`, `PMaterialSwitch`, `PNodeContext`, …).

> **So the family is per-class generated accessors in the reflection system's descriptor vtables** —
> one small function per reflected operation per class, installed into all three descriptors so that
> whichever descriptor a caller holds, the same adapter answers.

## 3. Key addresses

| address | what |
|---|---|
| `005A2B80`, `005A2EA0`, `005A32E0`, `005A3490` | four of the 351, disassembled and compared |
| `00D2A268` | the `PClassDescriptorForType<PTimeScaleOffsetController>` vtable |
| `00D2A4F8` | the `…Abstract<…>` vtable |
| `00D2A5F8` | the `…Concrete<…>` vtable |
| `005C5230` | the folded `xor eax,eax; ret` stub, also present in these vtables |
| `00861EC6` | `_purecall`, likewise |

## 4. Modding notes

- **A function count that includes these is inflated by 409**, and by **403** for one template alone.
  Any "how much of the engine is documented" figure should say whether it counts generated adapters.
- **The adapter is the narrowest possible hook point — for 401 of the 403.** It is 26 bytes, called
  only through a class descriptor, and its `call` target is the real function, so patching the
  target inside one adapter affects exactly one class's one reflected operation. **The exceptions
  matter**: patching `006B2970` changes `PPoint3`, `PQuat`, `PVector2`, `PVector3` **and**
  `PVector4` together, and `006B2950` changes `PMatrix3`, `PMatrix4` and `PPMatrix4` together.
- **Almost none are folded.** `/OPT:ICF` merged other identical bodies in this binary — `005C5230`
  and `0016D6A0` appear under several identities — and 401 of these 403 differ in their `call`
  target and survive as separate functions. ~~They are not folded.~~ **Two are**: `006B2950` and
  `006B2970` each serve several classes at once (§9).
- **Most adapters are installed three times, but 36 are not.** Replacing one vtable slot leaves the
  *others* pointing at the original — **two others** for 367 adapters, **one** for 34, and **five**
  or **nine** for the two shared ones (§9).

## 5. What is not known

- [x] ~~**What the 46 `OwnedBufferResetAdapter` functions do.** A second, smaller generated family in
  the same tag group, **not read**.~~ **`DF-1` ANSWERED 2026-09-12 (FABLE): they are class-descriptor
  vtable slot 11 — "release this instance's owned buffer" — for 46 array types.** All 46 are the
  same 59-byte body (one shape, one size, only the RTTI differs), e.g. `005A4830`:
  `(descriptor, instance)` → read the instance's dword `+0`; if **bit 31 is clear** (the buffer is
  owned, not borrowed) and the pointer at `+8` is non-null, `00584730(ptr)` — `if (p)
  _aligned_free(p)` — then zero both words and return `true`. The instance is a Phyre array
  header `{u32 count | ownership bit 31, T* data}`. Each adapter appears exactly three times, at
  **slot 11** of one class's `ForType` / `Abstract` / `Concrete` descriptor triple (138 slots = 46 × 3),
  where the 351 `ReturnValueAdapter`s of §2 sit at **slot 5**. The 46 classes: forty `PArray<T, N>`
  instantiations — `PArray<unsigned int,4>`, `<float,4>`, `<int,4>`, `<u8,1>`, `<u8,4>`, `<const u8*,8>`,
  `<PQWord,16>`, `<PMatrix4,4>`, `<PTypedObject,8>`, `<const PBase*,8>`, `<PAnimationChannel*,8>`,
  `<PAnimationDataSource*,8>`, `<PAnimationDataSourceListEntry,8>`, `<PAnimationEvent,4>`,
  `<PAnimationNetworkInstanceTarget,8>`, `<PAnimationSlotArray,8>`, `<PAnimationSlotListIndex,8>`,
  `<PEffectVariant*,8>`, `<PModifierNetworkInstance*,8>`, `<PSceneRenderPass*,8>`,
  `<const PContextSwitch*,8>`, `<const PLightType*,8>`, `<const PShadowCasterType*,8>`,
  `<PContextVariantFoldingTable,4>`, `<PShaderParameterCaptureBufferLocation,2>`,
  `<…LocationType,2>`, `<…LocationTypeConstantBuffer,4>`, `<PPostEffectBase*,8>`,
  `<PDynamicSegmentDesc,4>`, `<PSkeletonJointBounds,4>`, `<PSkinBoneRemap,2>`, `<PVertexStream,8>`,
  `<PBitmapFontCharInfo,4>`, `<PModifierNetworkDynamicMeshSegment,8>`, `<PRenderStream,8>`,
  `<PShadowSplit,8>`, `<PModifierNetworkBuffer,8>`, `<PRenderStreamInput,4>`, `<PInputAction*,8>`,
  `<PInputSource*,8>`, `<PInputMap*,8>` — and six array-holding classes: `PAnimationEventList`,
  `PShadowRenderer`, `PForwardShadowRenderer`, `PMorphModifierWeightsUserDataObject`, `PGameConfig`
  and the `PArray<PQWord,16>` holder. So the name was right: the family resets a buffer the
  instance owns, and it is a slot of the reflection descriptor, not a callback trampoline — which
  is why it cannot explain the `402 − 351` accessor gap (`DF-4`).
- [x] ~~What operation the adapter wraps.~~ **`DF-2` ANSWERED — section 8.** It is **descriptor
  virtual slot 5** (120 of 120 appearances), and it wraps a `Phyre.ScriptVM.ObjectPointerAccessor`
  that gates a script-supplied value through the `"PhyreObject"` registry check at `00682980`.
- [x] ~~**Why only 351 of the 747 known accessors have an adapter.**~~ **`DF-4` ANSWERED 2026-09-12 (FABLE):** 401 adapters exist (351 tagged, 50 under other tags), one per pointer accessor — the split *is* pointer versus reference; see the note under §"351 adapters against 747 accessors".
- [x] ~~**The exact class count.** 93 classes from a 120-adapter sample, with 11 unresolved; the
  full 351 have not been mapped, so "one or two per class" is a sample statement.~~ **`DF-3`
  ANSWERED 2026-09-13 (OPUS): 409 classes, exactly one adapter per class.** All 403 adapters and
  all 1,185 appearances were walked back to their complete-object-locator; **none was unresolved**.
  "One or two per class" was a sampling artefact — it is always exactly one. §9.
- [x] **UQ-315.** The nine one-off dispatchers, several of whose tags describe real mechanisms
  (`LinkedFlagGatedNotificationDispatch`, `HierarchyGenerationBitTraversalAndCallbackReconciliation`)
  and none of which is read.
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): all nine are read.** They are the `Runtime.Callback*` rows of the
  ledger left after the 351 return-value adapters, the 46 owned-buffer resets and the 3 Lua adapters. None is an
  adapter in this page's sense; each is a small piece of a real mechanism, and five of the nine already had a reading
  on the page that owns the mechanism.
  - **`0020DA50` / `0020D9F0` (`LinkedListFirstSuccessDispatch`, `LinkedVirtualPredicateFirstSuccessTraversal`)** — one
    first-success walk, twice. Each calls a node's virtual (slot 0 in `0020DA50`, slot 1 in `0020D9F0`) down a next
    chain at `+8`, and returns 1 at the first node that answers true, 0 at the end. Their only callers are the console's
    entry formatters (one of them the Presentation-filed menu renderer; see the crossings at the end), on a stack context
    whose first node's vtable is `AdapterInfos` (RTTI, base `AdapterInfoBase`) ([what the console tunes](../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md)).
  - **`002481C0` (`LinkedFlagGatedNotificationDispatch`)** — the widget layer's input notice during a transition. It walks
    from the focus top `0208EBC0` down `+0x10` while each node's `+0x40` has bits 0 and 3. It then sends `{11}` to the
    top's proc if a node on the chain has bit 9, and `{10}` otherwise
    ([the widget message protocol](../../16-UI/Widget-Object-Model/the-widget-message-protocol.md)).
  - **`002465F0` (`GenerationBoundRecordInitializeAndInitialNotify`)** — the widget initialiser. It clears the record,
    stores the proc at `+0` (the folded stub `005C5230` when none is given), and stamps the current generation into
    `+0x40` bit 17 from `0208ED5C`. Then it sends the proc message `{1}`, construct.
  - **`00248030` (`HierarchyGenerationBitTraversalAndCallbackReconciliation`)** — the generation reconcile. For each node
    whose bit 17 differs from `0208ED5C` (and whose bit 10 is clear) it sets bit 2 and, unless bit 18, sends `{2}`.
    Then it re-stamps bit 17 and walks on.
  - **`00186230` (`FourSlotDeferredInvocationDrain`)** — a four-slot deferred-call ring, run by the per-frame pump. It
    advances the slot index at `+0xCB8` modulo 4, calls every 16-byte `{fn, arg}` entry queued in that slot's vector
    (`+0xC38 + 32k`), and empties it.
  - **`006CC860` (`DoubleBufferedPointerDrainAndFlip`)** — reached only through the member tail-call `0067AB40`
    (`this + 0xA8`), from an application record's per-frame body. It hands each pointer in the current buffer (`[+0xA0]` selects `+0x60` or
    `+0x80`) to the member callback at `+0x58`, empties that buffer and flips `+0xA0`.
  - **`0063DC30` (`Runtime.CallbackAdapter`)** — dispatch with a default. It tail-calls the function at `+0x48` with the
    arguments shifted down one, or returns `0x15` when there is none
    ([the cluster header](../../22-Middleware-PhyreEngine/Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md)).
  - **`0017ECB0` (`Presentation.Runtime.Callback`)** — ten bytes that copy dword `[arg + 0x10]` to `01DF08F8`
    ([the settings page](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)).
  Control: `_index/candidates/uq315-one-off-dispatchers/one_off_dispatchers.py` (9 checks).

## 6. Evidence

| claim | evidence | tier |
|---|---|---|
| 409 functions, 13,254 bytes, tag breakdown | census over the GN160 function table | 1 |
| **All 403 are exactly 26 bytes** | byte-template scan of `.text`: 403 matches, 403 distinct call targets, no overlaps, all in the graph at 26 bytes | 1 |
| The shape, and that only the `call` target differs | four disassembled and compared instruction for instruction | 1 |
| Each appears exactly three times in `.rdata` | raw 8-byte address search of the data sections | 1 |
| The three are `ForType`/`Abstract`/`Concrete` of one class | walked back from each slot to the RTTI complete-object-locator and read the type descriptor | 1 |
| **409 classes, one adapter each** | the walk applied to **all 403 adapters / 1,185 appearances**, none unresolved | 1 |
| Every appearance is vtable **slot 5** | offset from each vtable's start computed after walking back to its COL — **1,185 of 1,185**, over all 403 adapters | 1 |
| Slot 5 wraps a `ScriptVM.ObjectPointerAccessor` | the adapters' call targets carry that tag, and `005BEC00` calls `00682980`, the `"PhyreObject"` registry lookup | 1 |
| Why not every accessor has an adapter | `DF-4`: the pointer/reference split. **The arithmetic does not close** — 403 adapters over 409 classes against 402 pointer accessors; reopened as `DF-5` | 2 |

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

The four named adapters, the three named vtable addresses and the slot number all reproduce exactly.
`005A2B80` appears at `00D2A290`, `00D2A520` and `00D2A620` — **slot 5** of vtables starting
`00D2A268`, `00D2A4F8`, `00D2A5F8`, exactly as §3 states, with the `ForType` / `Abstract` /
`Concrete` names for `PTimeScaleOffsetController`. What changed is that the sampled claims are now
censused, and three of them did not survive the census.

### The family is 403, and the census is complete

Scanning `.text` for the 26 bytes with the `call` displacement wildcarded:

| | |
|---|---:|
| matches | **403** |
| distinct call targets | **403** |
| overlapping matches | 0 |
| present in the function graph, `body_bytes == 26` | **403 / 403** |
| `.rdata`/`.data` appearances of an adapter address | **1,185** |
| appearances at vtable **slot 5** | **1,185** |
| appearances whose vtable start could not be resolved | **0** |

`351` is a *tag* count (`Runtime.Callback.ReturnValueAdapter`), never the family — `DF-4` already said
so and put the family at 401. **By shape it is 403.** The two-function difference is not explained
here; see `DF-5` below.

### `DF-3` answered: 409 classes, exactly one adapter each

Every appearance was walked back qword-by-qword to the first valid complete-object-locator
(`signature == 1`, `pSelf` equal to its own RVA), then through the type descriptor to the class name.

**409 distinct classes, and every class has exactly one slot-5 adapter.** The old "one or two
adapters per class" was a sampling artefact, and the "11 of 120 unresolved" is now zero of 1,185.

> `409` here and the `409` of §2's tag table are **coincidence**, not the same set: one counts
> `Runtime.Callback`-tagged functions, the other counts classes.

### ⚠ Not every adapter is installed three times

| appearances | adapters | which descriptors |
|---:|---:|---|
| 3 | **367** | `ForType`+`Abstract`+`Concrete` 329; +`WithoutDefaultConstructor` 34; +`Header` 3; +`HeaderWithoutDefaultConstructor` 1 |
| 2 | **34** | `ForType`+`Abstract` 19; +`Wrapper` 7; +`WithoutDefaultConstructor` 4; +`Concrete` 2; +`ForClassDescriptor` 1; +`Base` 1 |
| 6 | 1 | `006B2950` |
| 10 | 1 | `006B2970` |

**The invariant is `ForType`, not the triple**: all 409 classes have a `ForType` descriptor with the
adapter at slot 5, and the *other* descriptors vary. The 19 two-appearance `ForType`+`Abstract` cases
are abstract classes — `PAnimationDataSource`, `PRenderTargetBase`, `PParameterBufferBase`,
`PAnimationBlenderController` … — which have no instantiable descriptor to hold a third copy. The
seven `ForType`+`Wrapper` cases are externally-defined structs adopted into the reflection system:
`CD3D11_BLEND_DESC`, `CD3D11_DEPTH_STENCIL_DESC`, `CD3D11_RASTERIZER_DESC`,
`D3D11_DEPTH_STENCILOP_DESC`, `D3D11_RENDER_TARGET_BLEND_DESC` …

### ⚠ Two adapters are shared, and §4's hook advice is wrong for them

| adapter | target | classes it serves |
|---|---|---|
| `006B2950` | `00683B10` | `Vectormath::Scalar::Aos::Matrix3`, `…::Matrix4`, `Phyre::PMatrix4` |
| `006B2970` | `00683BF0` | `Vectormath::Scalar::Aos::Point3`, `…::Quat`, `…::Vector2`, `…::Vector3`, `…::Vector4` |

These are the SIMD vector and matrix types, whose accessors compile to the same code and were folded.
§4 said the adapters "are not folded" and that patching one "affects exactly one class's one
reflected operation, and nothing else". **For these two it affects three and five classes.** A hook
on `006B2970` intended for `PVector3` also fires for `PQuat`, `PPoint3`, `PVector2` and `PVector4`
— and that is the whole vector type set, so the mistake would be easy to make and hard to see.

### The accessor counts reproduce independently

Reading the diagnostic literals straight out of the data sections: **747 occurrences, 747 distinct
strings, `402` in the `T *` form and `345` in the `T &` form, over `412` distinct types** (335 types
carry both forms). That reproduces
[the accessor document](../../22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md)'s
**747 accessors over 412 distinct bound types** and the `402`/`345` split of `DF-4`, by a different
route — the string table rather than the function census. **Two instruments, same numbers.**

### ⚠ `DF-5` — the adapter arithmetic does not close

`DF-4` states the family is **401**, one per pointer accessor bar one. The shape census gives **403**
adapters over **409 classes**, against **402** pointer accessors. Those do not reconcile, and this
pass could **not** reproduce `DF-4`'s filter: no adapter's call target reaches a
`PObjectAccessor<…>::Get` literal by any reference this pass could detect.

> **That last sentence is not evidence.** The control says so: the **409** RTTI descriptor names this
> pass *did* use to identify every vtable — strings that are unquestionably live — are likewise
> reached by **zero** rip-relative references, because RTTI names are reached through 32-bit fields in
> the locator, not by code. **A test that reports zero for strings known to be in use cannot report
> anything about strings suspected not to be.** The reconciliation is therefore *open*, not *negative*.

- [x] **UQ-316.** **`DF-5`: reconcile 403 adapters / 409 classes against 402 pointer accessors and the recorded
  401.** Needs the accessor-to-function binding — how a `PObjectAccessor<T>::Get` literal is tied to
  the function that implements it — which this pass did not find. `DF-4`'s explanation may be right
  in kind and wrong in count; both are left standing until the binding is read.

  **ANSWERED 2026-09-14 (FABLE): the arithmetic closes exactly, and `DF-4`'s 401 is right in count as well as kind.**

  **The binding.** A `PObjectAccessor<T>::Get` literal is the tail of a longer string,
  `Phyre::PScripting::PScriptAccessors::PObjectAccessor<…>::Get`. The code references the **start of that
  qualified string**, not the `PObjectAccessor<` substring the earlier pass searched for. Each accessor's
  failure path loads it together with three other strings:
  - `__FILE__` (`e:\jenkins\…\PhyreScripting.…`, `00D23FF0`);
  - *"Object pointer obtained from script was of type “%s” when an object of type “%s” was
    required"* (`00D24BE0`);
  - *"Unable to obtain object pointer from script - found another type of data instead…"* (`00D24C40`).

  The accessor's own name is the argument that identifies the failing accessor. Resolving every `lea`/`mov
  [rip+…]` in `.text` against the qualified starts:

  | measured | result |
  |---|---:|
  | literals (402 `T *`, 345 `T &`) | 747 |
  | literals referenced by exactly one function | **747** |
  | functions referencing more than one literal | 0 |
  | adapters (26-byte template) / distinct targets | 403 / 403 |
  | adapter targets that reference a `T *` literal | **401** |
  | adapter targets that reference a `T &` literal | 0 |
  | adapter targets that reference no literal | **2** |
  | `T *` literals whose function no adapter wraps | **1** |

  *Control:* a first run that took each string's start from the preceding NUL left two literals
  "unreferenced". Both are in fact referenced two bytes later, at their qualified prefix, so the start was
  wrong, not the binding. With the prefix matched exactly, all 747 bind.

  **So:**
  - **403 adapters = 401 + 2.** The 401 wrap one pointer accessor each. The 2 are the shared adapters of §9,
    `006B2950` → `00683B10` (the three matrix types) and `006B2970` → `00683BF0` (the five vector/quaternion/point
    types). Their 62-byte targets fetch the script value and fall back to a static default (`02E41590`,
    `02E41580`). They have no failure path, so they carry no accessor name.
  - **409 classes = 401 + 3 + 5.** One class per pointer-accessor adapter, plus the classes the two shared adapters
    serve.
  - **402 pointer accessors = 401 + 1.** The unwrapped one is `PObjectAccessor<class Phyre::PClassDescriptor const
    *>::Get` (`006AEF30`). The non-const `PClassDescriptor *` accessor (`00636B80`) is wrapped.
  - **`DF-4`'s "401 adapters, one per pointer accessor bar one" is exact.** The shape census's extra two are not
    accessor adapters, and the "bar one" is the `const` descriptor accessor.

**Not claimed:** what descriptor slot 5 *does* is untouched — `DF-2`'s answer is unchallenged and
unre-derived here. ~~The nine one-off dispatchers are still unread.~~ *Read 2026-09-26 (FABLE, Claude Opus 5.5): `UQ-315`, §5.*
Nothing was executed or observed
live; every statement is static, from the shipped image.

## 7. Related

- [`../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`](../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md)
  — the other reason a function count misleads in this binary.
- [`../Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md`](../Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md)
  — the category's other generated-code families.
- [`../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
  — the descriptor system these vtables belong to.
- [`../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md)
  — where the `ForType`/`Abstract`/`Concrete` triple is already recorded.

## 8. `DF-2` answered — slot 5, and what it wraps

### The adapters are descriptor virtual method #5

For forty adapters, every one of their three `.rdata` appearances was walked back to its vtable start
and the offset computed:

**slot 5, in 120 appearances out of 120.** Not a majority — every one. **Extended 2026-09-13 to all 403 adapters: 1,185 appearances, slot 5 in every one.**

The descriptor kinds those 120 appearances belong to: **`ForType` 40, `Abstract` 40, `Concrete` 37**,
plus **2 `ConcreteWithoutDefaultConstructor`** and **1 `Header`** variant. So the triple is not
always literally *ForType/Abstract/Concrete* — a few classes substitute a variant descriptor, and the
adapter is installed in slot 5 of that one instead.

> **The full census (§9) confirms the shape of that statement and replaces its numbers**, and
corrects one name: the variant template is `PClassDescriptorWithoutDefaultConstructor`, not
`PClassDescriptorConcreteWithoutDefaultConstructor`.

### What slot 5 does — the script-to-native object accessor

The adapters' call targets are ~301-byte functions tagged
**`Phyre.ScriptVM.ObjectPointerAccessor`**, and `005BEC00` — the target of `005A2B80` — begins by
calling **`00682980`**, which
[`../../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`](../../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md)
identifies as the `"PhyreObject"` registry-key lookup that gates every script-supplied userdata.

> **Descriptor slot 5 is "take a script value, check it really is a Phyre object of this class, and
> hand back the pointer".** The 26-byte adapter exists to give that operation a uniform
> *(context, value, result\*)* shape so a generic caller can invoke it for any class.

**This corroborates an existing document rather than discovering something.**
[`../../22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`](../../22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md)
already maps **747 accessors over 412 distinct bound types**, and its table gives
`005BEC00` → `PAnimation::PTimeScaleOffsetController *`. **The RTTI walk here reached
`PTimeScaleOffsetController` for that adapter's descriptor triple independently, from the vtable
side.** Two routes, same class.

### ⚠ 351 adapters against 747 accessors

**Fewer than half the accessors have one of these adapters.** The accessor document counts 747
(402 pointer, 345 reference); this family is 351.

> **So the adapter is not a universal wrapper** — something distinguishes the accessors that get one
> from those that do not. The obvious candidate is the pointer/reference split (402 pointer accessors
> against 351 adapters is close but **not equal**, so it is not simply that), and **that difference is
> unexplained.** `DF-4`.

> **DF-4 answered 2026-09-12 (FABLE): "351" was the tag census, not the family. The family is
> 401 — one 26-byte adapter for every pointer accessor but one — and it *is* the pointer/reference
> split.** An image-wide shape census (every 26-byte function of exactly this instruction
> sequence whose call target references a `PObjectAccessor<…>::Get` diagnostic) finds **401**
> adapters wrapping **401 distinct pointer accessors** (`*>::Get`) and no reference accessor. 351
> carry the `Runtime.Callback.ReturnValueAdapter` tag; the other 50 are the same bytes under other
> tags (33 `NativeAdapter.CallResultStoreQword`, 13 `Phyre.Reflection.TypeInfrastructure`, 4
> `Phyre.Reflection.DescriptorRuntime`) — e.g. `PAnimationClip`'s `005A1680`, `PWorld`'s `0062F770`,
> `CD3D11_BLEND_DESC`'s `00624580`, each at slot 5 of its descriptor triple like the tagged ones.
> What the slot wraps is the class's own `PObjectAccessor<T *>::Get` (the target of
> `PTimeScaleOffsetController`'s adapter `005A2B80` is `005BEC00`, which references exactly that
> string), so **descriptor slot 5 is "fetch a `T*` from the script value"**; the 345 reference
> accessors have no slot because the descriptor takes the pointer form only, and 402 − 401 = 1
> pointer accessor with no adapter is the residue. The `OwnedBufferResetAdapter` family plays no
> part (DF-1: it is slot 11).

~~**The `OwnedBufferResetAdapter` family of 46 is still unread** and may account for part of the
gap.~~ **Stale — struck 2026-09-13.** `DF-1` above read that family in full and states it is
descriptor **slot 11**, so it cannot account for any part of a slot-5 gap; `DF-1` says as much in
its own last sentence. This line was left standing beside the answer that retired it.
## The `00624580` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00624580` (~32 B) — the standard `mov rcx, rdx; mov rbx, r8; call
0061A250` slot-3 adapter
(`00624586`/`00624589`/`0062458C`).

| member | role | interior |
| --- | --- | --- |
| `0061A250` | `PClassDescriptorConcrete` class body | [`0061A250`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-118 update (2026-09-21) - `006828F0` measured

`006828F0` (143 B) is the
`"Matrix"`-typed adapter
`00682AA0` and `00683B10`
call: `00811950(rcx)` gets
the object, `0080FBA0(rcx,
edx)` checks the kind,
`0080FA50` re-registers
under `"Matrix"` with tag
`0xFFF0B9D8`, then
`00810810(rcx, -1, -2)` and
`00811130(rcx, -3)` finish -
returning the object or 0.
Interior anchor `0068292E`
(the `0080FA50` call).

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-26)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2, for the `UQ-315` answer.
Edges are from `edges.tsv`; each sentence rests on the read body named.*

- **CoreRuntimeScheduling — SERVICE.** The widget initialiser `002465F0` and the generation reconcile `00248030` both
  ask the scheduling layer's frame predicate, and use the answer for the widget's frame counter `+0xB4`. The reconcile
  zeroes the counter when the predicate answers non-zero and increments it otherwise (`00248044`–`00248059`). The
  initialiser sets it to 1 only when the predicate answers 0 and a second predicate answers non-zero
  (`0024674A`–`0024675C`).
- **Presentation — CLIENT.** The console's menu renderer, which the ledger files under Presentation, calls the chain walk
  `0020DA50` to turn an entry's value into text (`001CE2BA`). This is the same console use as the entry formatter's two
  calls.
- **UI — CLIENT.** The widget system's set-up, which allocates the `0x7E00`-byte widget pool and the roots and is filed
  under UI, calls the initialiser `002465F0` for the widgets it builds.
