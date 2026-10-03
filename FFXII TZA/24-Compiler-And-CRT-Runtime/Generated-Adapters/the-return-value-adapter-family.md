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
call <target>        ; the only field that differs between the 351   <- corrected 2026-10-02, OPUS - between the 403 (template scan); 351 is the tag count
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
- [x] ~~**Why only 351 of the 747 known accessors have an adapter.**~~ **`DF-4` ANSWERED 2026-09-12 (FABLE):** ~~401 adapters exist (351 tagged, 50 under other tags)~~ 403 adapters exist, 351 of them tagged *(corrected 2026-10-02, OPUS: the 26-byte template scan of `.text` finds 403, all function entries; DF-5's answer, 403 = 401 + 2)*, one per pointer accessor — the split *is* pointer versus reference; see the note under §"351 adapters against 747 accessors".
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
  - **`00186230` (`FourSlotDeferredInvocationDrain`)** — a four-slot deferred-call ring, ~~run by the per-frame pump~~ flushed at most once per call of the title queue pump (see the title-asset page), and only while the dword `01FD4A68` is zero (pump calls are not shown to be frames). It
    advances the slot index at `+0xCB8` modulo 4, calls ~~every~~ the 16-byte `{fn, arg}` entries queued in that slot's vector
    (`+0xC38 + 32k`) up to a snapshot of its write cursor, ~~and empties it~~ then resets the write cursor of the bank the index then names; it frees nothing *(Corrected 2026-10-02, FABLE, on ASTRA's title-queue-pump and title-queue-consumption packets, SWE2-AUDIT-SPEC ACCEPT; [record](../../_index/candidates/astra-returns-title-fable-1002/README.md) F1)*.
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
| ~~Each appears exactly three times in `.rdata`~~ 367 of the 403 appear three times in `.rdata`, 34 twice, one six times and one ten times *(corrected 2026-10-02, OPUS: an 8-byte search of `.rdata` for the 403 template addresses, 1,185 appearances; the 2026-09-13 correction in §2)* | raw 8-byte address search of the data sections | 1 |
| The three are `ForType`/`Abstract`/`Concrete` of one class | walked back from each slot to the RTTI complete-object-locator and read the type descriptor | 1 |
| **409 classes, one adapter each** | the walk applied to **all 403 adapters / 1,185 appearances**, none unresolved | 1 |
| Every appearance is vtable **slot 5** | offset from each vtable's start computed after walking back to its COL — **1,185 of 1,185**, over all 403 adapters | 1 |
| Slot 5 wraps a `ScriptVM.ObjectPointerAccessor` | the adapters' call targets carry that tag, and `005BEC00` calls `00682980`, the `"PhyreObject"` registry lookup | 1 |
| Why not every accessor has an adapter | `DF-4`: the pointer/reference split. ~~**The arithmetic does not close**~~ — 403 adapters over 409 classes against 402 pointer accessors; reopened as `DF-5` *(answered: see DF-5, ANSWERED 2026-09-14 - 403 = 401 + 2; 2026-10-02, OPUS)* | 2 |

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
> unexplained.** `DF-4`. *(answered: see the DF-4 answer just below - 351 was the tag census; 2026-10-02, OPUS)*

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

`00624580` ~~(~32 B)~~ (26 B) — the standard `mov rcx, rdx; mov rbx, r8; call
0061A250` ~~slot-3~~ slot-5 adapter *(corrected 2026-10-02, OPUS: its 26 bytes are the family template; `.rdata` holds it at `00D54AE8` and `00D54B70`, slot 5 after the type pointers `00D54AB8` and `00D54B40`)*
(`00624586`/`00624589`/`0062458C`).

| member | role | interior |
| --- | --- | --- |
| `0061A250` | ~~`PClassDescriptorConcrete` class body~~ the script-VM object-pointer accessor (`Phyre.ScriptVM.ObjectPointerAccessor`) *(corrected 2026-10-02, OPUS: `0061A250+0x15` calls the `PhyreObject` registry check `00682980`, `0061A250+0x55` walks the class chain at `+0x78`, and a mismatch reports through `00812960` at `0061A250+0x96`)* | [`0061A250`](../../_index/ADDRESS-INDEX.md) |

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

## Per-member rows: the getter each return-value adapter calls, and the type it is installed for (OPUS, 2026-10-03)

The DF-4 family (402 members in the frontmatter; 398 get a row here) shares the 26-byte shape of section 2, stated there once and not repeated here: `mov rcx, rdx`, `mov rbx, r8`, one `call`, `mov [rbx], rax`. What differs from member to member is that one `call`: each adapter calls its own getter (no two rows share a target). Each row anchors that call, the member's distinguishing instruction, and states its target and the reflected type T. T is the template argument of every `PClassDescriptor*<T>` vtable that holds the adapter at slot 5 (section 8), read from that vtable's MSVC RTTI type descriptor in the certified image, and every such vtable must agree on T. [`fam_rows.py`](../../_index/candidates/opus-ee-return-value-adapters-1003/fam_rows.py) derives every row from the image and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-return-value-adapters-1003/rows.tsv). A member that is not exactly one direct call fails, and so does a member whose slot-5 vtables disagree on T or whose target or T differs from the row. Two controls are refused: a swapped target and a moved anchor. The getter is given as a bare address, not a citation, because the getters are explained, or not, on their own pages. Only the adapter's anchor counts here, per SWE2-AUDIT-SPEC's ruling `202e59a0a`. Four DF-4 members get no row; they are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-return-value-adapters-1003/excluded.tsv). All four sit in descriptor vtables that do not name one template type T: `0062F0F0` and `0063C000` (a non-template descriptor class beside the template one), and `006B2950` and `006B2970` (several Vectormath types sharing one body). The checker fails if any of them starts deriving. The 46 DF-1 members have no distinguishing instruction (their bodies are identical), so they get no rows.

### All 398 adapters (descriptor slot 5, OPUS)

| member | distinguishing instruction | getter called | reflected type T |
|---|---|---|---|
| 00584780 | `0058478C` `call` | 00599CA0 | Phyre::PSerialization::PBinary::PClusterHeaderBase |
| 005849E0 | `005849EC` `call` | 00599DD0 | Phyre::PSerialization::PBinary::PClusterHeaderD3D11 |
| 00584C50 | `00584C5C` `call` | 00599B70 | Phyre::PSerialization::PBinary::PClusterHeader |
| 00584EF0 | `00584EFC` `call` | 00599F00 | Phyre::PSerialization::PBinary::PInternal::PInstanceListHeader |
| 005A0B40 | `005A0B4C` `call` | 005A06E0 | Phyre::PTimer |
| 005A0EA0 | `005A0EAC` `call` | 005BD310 | Phyre::PAnimation::PAnimationController |
| 005A1170 | `005A117C` `call` | 005BE740 | Phyre::PAnimation::PBlendableAnimationSource |
| 005A1350 | `005A135C` `call` | 005BE4E0 | Phyre::PAnimation::PAnimationTargetBlenderController |
| 005A1680 | `005A168C` `call` | 005BCD20 | Phyre::PAnimation::PAnimationClip |
| 005A1850 | `005A185C` `call` | 005BE150 | Phyre::PAnimation::PAnimationSlotFilterDeferredLoad |
| 005A19D0 | `005A19DC` `call` | 005BE9A0 | Phyre::PAnimation::PTimeController |
| 005A1CB0 | `005A1CBC` `call` | 005BC990 | Phyre::PAnimation::PAnimationChannelBase |
| 005A2190 | `005A219C` `call` | 005BEAD0 | Phyre::PAnimation::PTimeIntervalController |
| 005A22D0 | `005A22DC` `call` | 005BC860 | Phyre::PAnimation::PAnimationChannel |
| 005A2410 | `005A241C` `call` | 005BC4D0 | Phyre::PAnimation::PAnimatableComponent |
| 005A2750 | `005A275C` `call` | 005BE020 | Phyre::PAnimation::PAnimationSlotFilter |
| 005A2890 | `005A289C` `call` | 005BD570 | Phyre::PAnimation::PAnimationDataSourceListEntry |
| 005A2B80 | `005A2B8C` `call` | 005BEC00 | Phyre::PAnimation::PTimeScaleOffsetController |
| 005A2EA0 | `005A2EAC` `call` | 005BD1E0 | Phyre::PAnimation::PAnimationConstantChannel |
| 005A32E0 | `005A32EC` `call` | 005BDC90 | Phyre::PAnimation::PAnimationNetworkInstanceTarget |
| 005A3490 | `005A349C` `call` | 005BDDC0 | Phyre::PAnimation::PAnimationSet |
| 005A37F0 | `005A37FC` `call` | 005BC730 | Phyre::PAnimation::PAnimationBlenderController |
| 005A38E0 | `005A38EC` `call` | 005BE280 | Phyre::PAnimation::PAnimationSlotListIndex |
| 005A3A10 | `005A3A1C` `call` | 005BCE50 | Phyre::PAnimation::PAnimationClipBinding |
| 005A3B00 | `005A3B0C` `call` | 005BD6A0 | Phyre::PAnimation::PAnimationEvent |
| 005A3FB0 | `005A3FBC` `call` | 005BE610 | Phyre::PAnimation::PAnimationWeightedBlenderController |
| 005A4110 | `005A411C` `call` | 005BDEF0 | Phyre::PAnimation::PAnimationSlotArray |
| 005A41A0 | `005A41AC` `call` | 005BCF80 | Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingChannelMap |
| 005A4650 | `005A465C` `call` | 005BD440 | Phyre::PAnimation::PAnimationDataSource |
| 005A47B0 | `005A47BC` `call` | 005BD0B0 | Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingDataBlockCache |
| 005A4900 | `005A490C` `call` | 005BD900 | Phyre::PAnimation::PAnimationEventList |
| 005A4A60 | `005A4A6C` `call` | 005BC600 | Phyre::PAnimation::PAnimationAdditiveBlenderController |
| 005A4B10 | `005A4B1C` `call` | 005BCBF0 | Phyre::PAnimation::PAnimationChannelTimes |
| 005A51F0 | `005A51FC` `call` | 005BD7D0 | Phyre::PAnimation::PAnimationEventController |
| 005A5330 | `005A533C` `call` | 005BDB60 | Phyre::PAnimation::PAnimationNetworkInstance |
| 005A5520 | `005A552C` `call` | 005BDA30 | Phyre::PAnimation::PAnimationHierarchyNode |
| 005A5630 | `005A563C` `call` | 005BE3B0 | Phyre::PAnimation::PAnimationSpuTargetBlenderController |
| 005A5980 | `005A598C` `call` | 005BCAC0 | Phyre::PAnimation::PAnimationChannelTarget |
| 005C4D50 | `005C4D5C` `call` | 005BB210 | decorated `V?$PArray@I$03@Phyre@@` |
| 005C4D70 | `005C4D7C` `call` | 005BB350 | decorated `V?$PArray@M$03@Phyre@@` |
| 005C4D90 | `005C4D9C` `call` | 005BB490 | decorated `V?$PArray@PEAVPAnimationChannel@PAnimation@Phyre@@$07@Phyre@@` |
| 005C4DB0 | `005C4DBC` `call` | 005BB5D0 | decorated `V?$PArray@PEAVPAnimationDataSource@PAnimation@Phyre@@$07@Phyre@@` |
| 005C4DD0 | `005C4DDC` `call` | 005BB710 | decorated `V?$PArray@VPAnimationChannelTarget@PAnimation@Phyre@@$07@Phyre@@` |
| 005C4DF0 | `005C4DFC` `call` | 005BB850 | decorated `V?$PArray@VPAnimationConstantChannel@PAnimation@Phyre@@$07@Phyre@@` |
| 005C4E10 | `005C4E1C` `call` | 005BB990 | decorated `V?$PArray@VPAnimationDataSourceListEntry@PAnimation@Phyre@@$07@Phyre@@` |
| 005C4E30 | `005C4E3C` `call` | 005BBAD0 | decorated `V?$PArray@VPAnimationEvent@PAnimation@Phyre@@$03@Phyre@@` |
| 005C4E50 | `005C4E5C` `call` | 005BBC10 | decorated `V?$PArray@VPAnimationNetworkInstanceTarget@PAnimation@Phyre@@$07@Phyre@@` |
| 005C4E70 | `005C4E7C` `call` | 005BBD50 | decorated `V?$PArray@VPAnimationSlotArray@PAnimation@Phyre@@$07@Phyre@@` |
| 005C4E90 | `005C4E9C` `call` | 005BBE90 | decorated `V?$PArray@VPAnimationSlotFilterDeferredLoad@PAnimation@Phyre@@$07@Phyre@@` |
| 005C4EB0 | `005C4EBC` `call` | 005BBFD0 | decorated `V?$PArray@VPAnimationSlotListIndex@PAnimation@Phyre@@$07@Phyre@@` |
| 005C4ED0 | `005C4EDC` `call` | 005BC110 | decorated `V?$PArray@VPBlendableAnimationSource@PAnimation@Phyre@@$07@Phyre@@` |
| 005C4EF0 | `005C4EFC` `call` | 005BC250 | decorated `V?$PArray@VPQWord@Phyre@@$0BA@@Phyre@@` |
| 005C4F10 | `005C4F1C` `call` | 005BC390 | decorated `V?$PSharray@PEAVPAnimationClip@PAnimation@Phyre@@@Phyre@@` |
| 005CDE70 | `005CDE7C` `call` | 005F7AD0 | Phyre::PRendering::PConstantBufferBase |
| 005CDF80 | `005CDF8C` `call` | 005F8CA0 | Phyre::PRendering::PModifierNetworkDynamicMeshInstance |
| 005CE090 | `005CE09C` `call` | 005FB9C0 | Phyre::PRendering::PShaderPassParameterLocationTypesBase |
| 005CE2A0 | `005CE2AC` `call` | 005F93C0 | Phyre::PRendering::PSamplerState |
| 005CE4C0 | `005CE4CC` `call` | 005FBFB0 | Phyre::PRendering::PShaderSource |
| 005CE4E0 | `005CE4EC` `call` | 005F7C00 | Phyre::PRendering::PContextVariantFoldingTable |
| 005CE970 | `005CE97C` `call` | 005FC800 | Phyre::PRendering::PTexture2DBase |
| 005CEB80 | `005CEB8C` `call` | 005FA920 | Phyre::PRendering::PShaderParameterCaptureBufferRWTexture3D |
| 005CED20 | `005CED2C` `call` | 005F8A40 | Phyre::PRendering::PMeshInstanceSegmentContext |
| 005CF290 | `005CF29C` `call` | 005FB3D0 | Phyre::PRendering::PShaderParameterDefinition |
| 005CF2E0 | `005CF2EC` `call` | 005F7F90 | Phyre::PRendering::PEffectVariant |
| 005CF800 | `005CF80C` `call` | 005FC930 | Phyre::PRendering::PTexture3D |
| 005CF950 | `005CF95C` `call` | 005FC5A0 | Phyre::PRendering::PStructuredBufferBase |
| 005CFB80 | `005CFB8C` `call` | 005F9290 | Phyre::PRendering::PRenderTargetBase |
| 005CFD40 | `005CFD4C` `call` | 005FAA50 | Phyre::PRendering::PShaderParameterCaptureBufferSampler |
| 005CFEE0 | `005CFEEC` `call` | 005F9030 | Phyre::PRendering::PParameterBufferBase |
| 005D0280 | `005D028C` `call` | 005FB890 | Phyre::PRendering::PShaderPassParameterLocationTypes |
| 005D05A0 | `005D05AC` `call` | 005FC0E0 | Phyre::PRendering::PShaderStreamDefinition |
| 005D08B0 | `005D08BC` `call` | 005F8DD0 | Phyre::PRendering::PNodeContext |
| 005D08D0 | `005D08DC` `call` | 005FACB0 | Phyre::PRendering::PShaderParameterCaptureBufferStructuredBuffer |
| 005D0E10 | `005D0E1C` `call` | 005FCDF0 | Phyre::PRendering::PTextureCubeMapBase |
| 005D0F00 | `005D0F0C` `call` | 005F8F00 | Phyre::PRendering::PParameterBuffer |
| 005D0F20 | `005D0F2C` `call` | 005FB500 | Phyre::PRendering::PShaderPass |
| 005D0F40 | `005D0F4C` `call` | 005FBE80 | Phyre::PRendering::PShaderProgramParamsAndStreams |
| 005D1240 | `005D124C` `call` | 005FAB80 | Phyre::PRendering::PShaderParameterCaptureBufferStream |
| 005D1370 | `005D137C` `call` | 005F8910 | Phyre::PRendering::PMeshInstanceBounds |
| 005D15C0 | `005D15CC` `call` | 005F79A0 | Phyre::PRendering::PConstantBuffer |
| 005D1970 | `005D197C` `call` | 005FA6C0 | Phyre::PRendering::PShaderParameterCaptureBufferRWStructuredBuffer |
| 005D1DA0 | `005D1DAC` `call` | 005FBAF0 | Phyre::PRendering::PShaderPassParameterLocationTypesConstantBuffer |
| 005D2120 | `005D212C` `call` | 005F9620 | Phyre::PRendering::PSceneRenderPass |
| 005D23A0 | `005D23AC` `call` | 005FBD50 | Phyre::PRendering::PShaderProgramBase |
| 005D2590 | `005D259C` `call` | 005F8580 | Phyre::PRendering::PMaterialSwitch |
| 005D25D0 | `005D25DC` `call` | 005FB040 | Phyre::PRendering::PShaderParameterCaptureBufferTextureBase |
| 005D2A10 | `005D2A1C` `call` | 005F9D40 | Phyre::PRendering::PShaderParameterCaptureBufferByteAddressBuffer |
| 005D2D20 | `005D2D2C` `call` | 005FBC20 | Phyre::PRendering::PShaderPassStateBase |
| 005D2EB0 | `005D2EBC` `call` | 005FC210 | Phyre::PRendering::PShaderVertexProgram |
| 005D30E0 | `005D30EC` `call` | 005F9160 | Phyre::PRendering::PRenderTarget |
| 005D3130 | `005D313C` `call` | 005FC6D0 | Phyre::PRendering::PTexture2D |
| 005D3460 | `005D346C` `call` | 005F9880 | Phyre::PRendering::PShader |
| 005D3920 | `005D392C` `call` | 005FC470 | Phyre::PRendering::PStructuredBuffer |
| 005D3A10 | `005D3A1C` `call` | 005FA0D0 | Phyre::PRendering::PShaderParameterCaptureBufferLocation |
| 005D3A30 | `005D3A3C` `call` | 005FA590 | Phyre::PRendering::PShaderParameterCaptureBufferRWByteAddressBuffer |
| 005D3C90 | `005D3C9C` `call` | 005FC340 | Phyre::PRendering::PShadowRenderer |
| 005D4040 | `005D404C` `call` | 005F9AE0 | Phyre::PRendering::PShaderFragmentProgram |
| 005D4420 | `005D442C` `call` | 005F8450 | Phyre::PRendering::PMaterial |
| 005D46F0 | `005D46FC` `call` | 005FADE0 | Phyre::PRendering::PShaderParameterCaptureBufferTexture2D |
| 005D4830 | `005D483C` `call` | 005F86B0 | Phyre::PRendering::PMeshInstance |
| 005D48A0 | `005D48AC` `call` | 005F7E60 | Phyre::PRendering::PEffect |
| 005D4C10 | `005D4C1C` `call` | 005FB2A0 | Phyre::PRendering::PShaderParameterCaptureConstantBuffer |
| 005D4C30 | `005D4C3C` `call` | 005FA200 | Phyre::PRendering::PShaderParameterCaptureBufferLocationSize |
| 005D4C70 | `005D4C7C` `call` | 005F8320 | Phyre::PRendering::PIndirectArgsBufferBase |
| 005D52A0 | `005D52AC` `call` | 005FCA60 | Phyre::PRendering::PTexture3DBase |
| 005D52C0 | `005D52CC` `call` | 005F80C0 | Phyre::PRendering::PForwardShadowRenderer |
| 005D52E0 | `005D52EC` `call` | 005FB630 | Phyre::PRendering::PShaderPassBase |
| 005D5510 | `005D551C` `call` | 005F94F0 | Phyre::PRendering::PSamplerStateBase |
| 005D5550 | `005D555C` `call` | 005F9C10 | Phyre::PRendering::PShaderGeometryProgram |
| 005D5E20 | `005D5E2C` `call` | 005FAF10 | Phyre::PRendering::PShaderParameterCaptureBufferTexture3D |
| 005D6200 | `005D620C` `call` | 005FCCC0 | Phyre::PRendering::PTextureCubeMap |
| 005D63F0 | `005D63FC` `call` | 005F9E70 | Phyre::PRendering::PShaderParameterCaptureBufferDataBlock |
| 005D6410 | `005D641C` `call` | 005FA330 | Phyre::PRendering::PShaderParameterCaptureBufferLocationType |
| 005D66A0 | `005D66AC` `call` | 005F7D30 | Phyre::PRendering::PDynamicMeshInstance |
| 005D69D0 | `005D69DC` `call` | 005F99B0 | Phyre::PRendering::PShaderComputeProgram |
| 005D6DE0 | `005D6DEC` `call` | 005F9750 | Phyre::PRendering::PSceneWideParameterBuffer |
| 005D6EE0 | `005D6EEC` `call` | 005FB170 | Phyre::PRendering::PShaderParameterCaptureBufferTextureCubeMap |
| 005D70F0 | `005D70FC` `call` | 005F8B70 | Phyre::PRendering::PMeshInstanceSegmentStreamBinding |
| 005D72A0 | `005D72AC` `call` | 005FCB90 | Phyre::PRendering::PTextureCommonBase |
| 005D7430 | `005D743C` `call` | 005F9FA0 | Phyre::PRendering::PShaderParameterCaptureBufferIndexDataBlock |
| 005D74D0 | `005D74DC` `call` | 005FA460 | Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer |
| 005D7910 | `005D791C` `call` | 005F81F0 | Phyre::PRendering::PIndirectArgsBuffer |
| 005D7B40 | `005D7B4C` `call` | 005FB760 | Phyre::PRendering::PShaderPassInfo |
| 005D8120 | `005D812C` `call` | 005FA7F0 | Phyre::PRendering::PShaderParameterCaptureBufferRWTexture2D |
| 005D81B0 | `005D81BC` `call` | 005F87E0 | Phyre::PRendering::PMeshInstanceAttachPoint |
| 00606690 | `0060669C` `call` | 005F5CE0 | decorated `V?$PArray@PEAVPEffectVariant@PRendering@Phyre@@$07@Phyre@@` |
| 006066B0 | `006066BC` `call` | 005F5E20 | decorated `V?$PArray@PEAVPModifierNetworkInstance@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006066D0 | `006066DC` `call` | 005F5F60 | decorated `V?$PArray@PEAVPSceneRenderPass@PRendering@Phyre@@$07@Phyre@@` |
| 006066F0 | `006066FC` `call` | 005F60A0 | decorated `V?$PArray@PEBVPContextSwitch@PRendering@Phyre@@$07@Phyre@@` |
| 00606710 | `0060671C` `call` | 005F61E0 | decorated `V?$PArray@PEBVPLightType@PRendering@Phyre@@$07@Phyre@@` |
| 00606730 | `0060673C` `call` | 005F6320 | decorated `V?$PArray@PEBVPShadowCasterType@PRendering@Phyre@@$07@Phyre@@` |
| 00606750 | `0060675C` `call` | 005F6460 | decorated `V?$PArray@VPContextVariantFoldingTable@PRendering@Phyre@@$03@Phyre@@` |
| 00606770 | `0060677C` `call` | 005F65A0 | decorated `V?$PArray@VPMaterialSwitch@PRendering@Phyre@@$07@Phyre@@` |
| 00606790 | `0060679C` `call` | 005F66E0 | decorated `V?$PArray@VPMatrix4@Phyre@@$03@Phyre@@` |
| 006067B0 | `006067BC` `call` | 005F6820 | decorated `V?$PArray@VPMeshInstanceSegmentContext@PRendering@Phyre@@$07@Phyre@@` |
| 006067D0 | `006067DC` `call` | 005F6960 | decorated `V?$PArray@VPNodeContext@PRendering@Phyre@@$07@Phyre@@` |
| 006067F0 | `006067FC` `call` | 005F6AA0 | decorated `V?$PArray@VPSceneRenderPass@PRendering@Phyre@@$07@Phyre@@` |
| 00606810 | `0060681C` `call` | 005F6BE0 | decorated `V?$PArray@VPShader@PRendering@Phyre@@$07@Phyre@@` |
| 00606830 | `0060683C` `call` | 005F6D20 | decorated `V?$PArray@VPShaderParameterCaptureBufferLocation@PRendering@Phyre@@$01@Phyre@@` |
| 00606850 | `0060685C` `call` | 005F6E60 | decorated `V?$PArray@VPShaderParameterCaptureBufferLocationType@PRendering@Phyre@@$01@Phyre@@` |
| 00606870 | `0060687C` `call` | 005F6FA0 | decorated `V?$PArray@VPShaderParameterCaptureBufferLocationTypeConstantBuffer@PRendering@Phyre@@$03@Phyre@@` |
| 00606890 | `0060689C` `call` | 005F70E0 | decorated `V?$PArray@VPShaderParameterDefinition@PRendering@Phyre@@$07@Phyre@@` |
| 006068B0 | `006068BC` `call` | 005F7220 | decorated `V?$PArray@VPShaderPass@PRendering@Phyre@@$07@Phyre@@` |
| 006068D0 | `006068DC` `call` | 005F7360 | decorated `V?$PArray@VPShaderPassInfo@PRendering@Phyre@@$07@Phyre@@` |
| 006068F0 | `006068FC` `call` | 005F74A0 | decorated `V?$PArray@VPShaderStreamDefinition@PRendering@Phyre@@$07@Phyre@@` |
| 00606910 | `0060691C` `call` | 005F75E0 | decorated `V?$PArray@VPString@Phyre@@$07@Phyre@@` |
| 00606930 | `0060693C` `call` | 005F7720 | decorated `V?$PSharray@I@Phyre@@` |
| 00606950 | `0060695C` `call` | 005F7860 | decorated `V?$PSharray@PEBVPMeshInstanceSegmentStreamBinding@PRendering@Phyre@@@Phyre@@` |
| 00610F60 | `00610F6C` `call` | 0061BCE0 | Phyre::PRendering::PTexture3DD3D11 |
| 00610FF0 | `00610FFC` `call` | 0061B490 | Phyre::PRendering::PShaderPassStateD3D11 |
| 00611160 | `0061116C` `call` | 0061B6F0 | Phyre::PRendering::PShaderVertexProgramD3D11 |
| 006116C0 | `006116CC` `call` | 0061B100 | Phyre::PRendering::PShaderFragmentProgramD3D11 |
| 006117D0 | `006117DC` `call` | 0061B360 | Phyre::PRendering::PShaderPassD3D11 |
| 00611B70 | `00611B7C` `call` | 0061AB10 | Phyre::PRendering::PConstantBufferD3D11 |
| 00611C80 | `00611C8C` `call` | 0061B230 | Phyre::PRendering::PShaderGeometryProgramD3D11 |
| 00612020 | `0061202C` `call` | 0061BBB0 | Phyre::PRendering::PTexture2DD3D11 |
| 006120D0 | `006120DC` `call` | 0061AFD0 | Phyre::PRendering::PShaderComputeProgramD3D11 |
| 00612270 | `0061227C` `call` | 0061AD70 | Phyre::PRendering::PRenderTargetD3D11 |
| 00612420 | `0061242C` `call` | 0061BA80 | Phyre::PRendering::PStructuredBufferD3D11 |
| 006128F0 | `006128FC` `call` | 0061B820 | Phyre::PRendering::PStreamInputDescD3D11 |
| 00612BC0 | `00612BCC` `call` | 0061BE10 | Phyre::PRendering::PTextureCubeMapD3D11 |
| 00612E10 | `00612E1C` `call` | 0061B950 | Phyre::PRendering::PStreamInputLayoutD3D11 |
| 00612FB0 | `00612FBC` `call` | 0061AC40 | Phyre::PRendering::PIndirectArgsBufferD3D11 |
| 00613280 | `0061328C` `call` | 0061B5C0 | Phyre::PRendering::PShaderProgramD3D11 |
| 00613360 | `0061336C` `call` | 0061AEA0 | Phyre::PRendering::PSamplerStateD3D11 |
| 006245A0 | `006245AC` `call` | 0061A390 | CD3D11_DEPTH_STENCIL_DESC |
| 006245C0 | `006245CC` `call` | 0061A4D0 | CD3D11_RASTERIZER_DESC |
| 006245E0 | `006245EC` `call` | 0061A610 | D3D11_DEPTH_STENCILOP_DESC |
| 00624600 | `0062460C` `call` | 0061A750 | D3D11_RENDER_TARGET_BLEND_DESC |
| 00624620 | `0062462C` `call` | 0061A890 | decorated `V?$PArray@E$00@Phyre@@` |
| 00624640 | `0062464C` `call` | 0061A9D0 | decorated `V?$PArray@VPStreamInputDescD3D11@PRendering@Phyre@@$07@Phyre@@` |
| 0062EE30 | `0062EE3C` `call` | 00636F10 | Phyre::PClusterDependencyList |
| 0062F230 | `0062F23C` `call` | 005BE870 | Phyre::PCluster |
| 0062F410 | `0062F41C` `call` | 00636A50 | Phyre::PClassDataMemberDynamic |
| 0062F5D0 | `0062F5DC` `call` | 00637040 | Phyre::PNamespace |
| 0062F770 | `0062F77C` `call` | 00637170 | Phyre::PWorld |
| 0062F990 | `0062F99C` `call` | 00636CB0 | Phyre::PClassDescriptorDynamic |
| 0062F9B0 | `0062F9BC` `call` | 00636DE0 | Phyre::PClassMember |
| 0063BFE0 | `0063BFEC` `call` | 006367E0 | decorated `V?$PSharray@VPString@Phyre@@@Phyre@@` |
| 0063EBB0 | `0063EBBC` `call` | 0064E480 | Phyre::PPostProcessing::PDepthOfField |
| 0063ECE0 | `0063ECEC` `call` | 0064DC30 | Phyre::PPostProcessing::PAtmosphericsD3D11 |
| 0063EDB0 | `0063EDBC` `call` | 00650230 | Phyre::PPostProcessing::PScreenSpaceReflectionBase |
| 0063EF20 | `0063EF2C` `call` | 0064F9E0 | Phyre::PPostProcessing::PMotionBlurD3D11 |
| 0063F0C0 | `0063F0CC` `call` | 0064F2C0 | Phyre::PPostProcessing::PMLAABase |
| 0063F560 | `0063F56C` `call` | 0064E220 | Phyre::PPostProcessing::PDeferredLightingBase |
| 0063F8E0 | `0063F8EC` `call` | 0064ECD0 | Phyre::PPostProcessing::PGlowBase |
| 0063FA90 | `0063FA9C` `call` | 00650360 | Phyre::PPostProcessing::PScreenSpaceReflectionD3D11 |
| 0063FD30 | `0063FD3C` `call` | 0064D9D0 | Phyre::PPostProcessing::PAtmospherics |
| 0063FDE0 | `0063FDEC` `call` | 0064F3F0 | Phyre::PPostProcessing::PMLAAD3D11 |
| 00640020 | `0064002C` `call` | 0064F780 | Phyre::PPostProcessing::PMotionBlur |
| 00640580 | `0064058C` `call` | 0064EF30 | Phyre::PPostProcessing::PGlowGPUBase |
| 00640710 | `0064071C` `call` | 00650100 | Phyre::PPostProcessing::PScreenSpaceReflection |
| 006407E0 | `006407EC` `call` | 0064F060 | Phyre::PPostProcessing::PLowResParticles |
| 006409F0 | `006409FC` `call` | 0064F190 | Phyre::PPostProcessing::PMLAA |
| 00640BA0 | `00640BAC` `call` | 0064FEA0 | Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionBase |
| 00641040 | `0064104C` `call` | 0064E350 | Phyre::PPostProcessing::PDeferredLightingD3D11 |
| 006411C0 | `006411CC` `call` | 0064EE00 | Phyre::PPostProcessing::PGlowD3D11 |
| 00641710 | `0064171C` `call` | 0064F520 | Phyre::PPostProcessing::PMaterialPostEffect |
| 00641730 | `0064173C` `call` | 0064DE90 | Phyre::PPostProcessing::PCelShadingBase |
| 00641960 | `0064196C` `call` | 0064FFD0 | Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionD3D11 |
| 00641E00 | `00641E0C` `call` | 0064EBA0 | Phyre::PPostProcessing::PGlow |
| 00641F90 | `00641F9C` `call` | 0064E0F0 | Phyre::PPostProcessing::PDeferredLighting |
| 00642050 | `0064205C` `call` | 0064DFC0 | Phyre::PPostProcessing::PCelShadingD3D11 |
| 006422E0 | `006422EC` `call` | 0064FD70 | Phyre::PPostProcessing::PScreenSpaceAmbientOcclusion |
| 00642820 | `0064282C` `call` | 0064E940 | Phyre::PPostProcessing::PFXAABase |
| 00642970 | `0064297C` `call` | 0064E5B0 | Phyre::PPostProcessing::PDepthOfFieldBase |
| 00642A00 | `00642A0C` `call` | 0064FC40 | Phyre::PPostProcessing::PPostEffectManager |
| 00642AB0 | `00642ABC` `call` | 0064DD60 | Phyre::PPostProcessing::PCelShading |
| 006431D0 | `006431DC` `call` | 0064F650 | Phyre::PPostProcessing::PMeshParticleSystemBase |
| 00643280 | `0064328C` `call` | 0064EA70 | Phyre::PPostProcessing::PFXAAD3D11 |
| 00643450 | `0064345C` `call` | 0064FB10 | Phyre::PPostProcessing::PPostEffectBase |
| 006438F0 | `006438FC` `call` | 0064E6E0 | Phyre::PPostProcessing::PDepthOfFieldD3D11 |
| 00643A20 | `00643A2C` `call` | 0064E810 | Phyre::PPostProcessing::PFXAA |
| 00643B50 | `00643B5C` `call` | 0064F8B0 | Phyre::PPostProcessing::PMotionBlurBase |
| 00643CD0 | `00643CDC` `call` | 0064DB00 | Phyre::PPostProcessing::PAtmosphericsBase |
| 00653B90 | `00653B9C` `call` | 0064D890 | decorated `V?$PArray@PEAVPPostEffectBase@PPostProcessing@Phyre@@$07@Phyre@@` |
| 0065E8E0 | `0065E8EC` `call` | 0066EB60 | Phyre::PGeometry::PMeshSegmentBase |
| 0065EB30 | `0065EB3C` `call` | 0066E440 | Phyre::PGeometry::PIndexDataBlockBase |
| 0065EDA0 | `0065EDAC` `call` | 0066E900 | Phyre::PGeometry::PMesh |
| 0065F050 | `0065F05C` `call` | 0066EC90 | Phyre::PGeometry::PMeshSegmentD3D11 |
| 0065F070 | `0065F07C` `call` | 0066E570 | Phyre::PGeometry::PIndexDataBlockBufferD3D11 |
| 0065F370 | `0065F37C` `call` | 0066DD20 | Phyre::PGeometry::PDataBlockBufferD3D11 |
| 0065F670 | `0065F67C` `call` | 0066F150 | Phyre::PGeometry::PVertexStream |
| 0065F880 | `0065F88C` `call` | 0066EA30 | Phyre::PGeometry::PMeshSegment |
| 0065FD00 | `0065FD0C` `call` | 0066E0B0 | Phyre::PGeometry::PDynamicMesh |
| 0065FD20 | `0065FD2C` `call` | 0066E6A0 | Phyre::PGeometry::PIndexDataBlockD3D11 |
| 00660050 | `0066005C` `call` | 0066DE50 | Phyre::PGeometry::PDataBlockD3D11 |
| 00660170 | `0066017C` `call` | 0066E1E0 | Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc |
| 006602C0 | `006602CC` `call` | 0066E7D0 | Phyre::PGeometry::PMaterialSet |
| 00660840 | `0066084C` `call` | 0066DBF0 | Phyre::PGeometry::PDataBlockBase |
| 006609C0 | `006609CC` `call` | 0066EEF0 | Phyre::PGeometry::PSkeletonJointBounds |
| 00660B90 | `00660B9C` `call` | 0066E310 | Phyre::PGeometry::PIndexDataBlock |
| 00660D90 | `00660D9C` `call` | 0066EDC0 | Phyre::PGeometry::PShape |
| 00661000 | `0066100C` `call` | 0066DAC0 | Phyre::PGeometry::PDataBlock |
| 00661440 | `0066144C` `call` | 0066F020 | Phyre::PGeometry::PSkinBoneRemap |
| 006616C0 | `006616CC` `call` | 0066DF80 | Phyre::PGeometry::PDynamicDataBlock |
| 00671080 | `0067108C` `call` | 0066CD00 | decorated `V?$PArray@E$03@Phyre@@` |
| 006710A0 | `006710AC` `call` | 0066CE40 | decorated `V?$PArray@H$03@Phyre@@` |
| 006710C0 | `006710CC` `call` | 0066CF80 | decorated `V?$PArray@VPDataBlockD3D11@PGeometry@Phyre@@$07@Phyre@@` |
| 006710E0 | `006710EC` `call` | 0066D0C0 | decorated `V?$PArray@VPDynamicSegmentDesc@PDynamicMesh@PGeometry@Phyre@@$03@Phyre@@` |
| 00671100 | `0067110C` `call` | 0066D200 | decorated `V?$PArray@VPMeshSegment@PGeometry@Phyre@@$07@Phyre@@` |
| 00671120 | `0067112C` `call` | 0066D340 | decorated `V?$PArray@VPSkeletonJointBounds@PGeometry@Phyre@@$03@Phyre@@` |
| 00671140 | `0067114C` `call` | 0066D480 | decorated `V?$PArray@VPSkinBoneRemap@PGeometry@Phyre@@$01@Phyre@@` |
| 00671160 | `0067116C` `call` | 0066D5C0 | decorated `V?$PArray@VPVertexStream@PGeometry@Phyre@@$07@Phyre@@` |
| 00671180 | `0067118C` `call` | 0066D700 | decorated `V?$PSharray@PEAVPMaterial@PRendering@Phyre@@@Phyre@@` |
| 006711A0 | `006711AC` `call` | 0066D840 | decorated `V?$PSharray@VPDataBlockBufferD3D11@PGeometry@Phyre@@@Phyre@@` |
| 006711C0 | `006711CC` `call` | 0066D980 | decorated `V?$PSharray@VPIndexDataBlockBufferD3D11@PGeometry@Phyre@@@Phyre@@` |
| 00674A80 | `00674A8C` `call` | 00676810 | Phyre::PAssetReference |
| 00674D00 | `00674D0C` `call` | 00676940 | Phyre::PAssetReferenceImport |
| 00677FD0 | `00677FDC` `call` | 00678CB0 | Phyre::PCamera |
| 00678220 | `0067822C` `call` | 00678DE0 | Phyre::PCameraProjection |
| 0067C770 | `0067C77C` `call` | 0067DE90 | Phyre::PText::PBitmapFont |
| 0067C9A0 | `0067C9AC` `call` | 0067DFC0 | Phyre::PText::PBitmapFontCharInfo |
| 0067E140 | `0067E14C` `call` | 0067DD50 | decorated `V?$PArray@VPBitmapFontCharInfo@PText@Phyre@@$03@Phyre@@` |
| 0067E380 | `0067E38C` `call` | 0067EDD0 | Phyre::PWorldMatrix |
| 00680470 | `0068047C` `call` | 00683580 | Phyre::PScripting::PClassCallableMethodScript |
| 00680680 | `0068068C` `call` | 00683450 | Phyre::PScripting::PAsyncProcessHeader |
| 00680930 | `0068093C` `call` | 00683910 | Phyre::PScripting::PScriptCallbackHandler |
| 006809B0 | `006809BC` `call` | 006836B0 | Phyre::PScripting::PScheduler |
| 00680B10 | `00680B1C` `call` | 006837E0 | Phyre::PScripting::PScript |
| 00688040 | `0068804C` `call` | 0069C350 | Phyre::PPhysics::PPhysicsCharacterControllerBullet |
| 00688150 | `0068815C` `call` | 0069E230 | Phyre::PPhysics::PPhysicsWorld |
| 006881E0 | `006881EC` `call` | 0069D650 | Phyre::PPhysics::PPhysicsRigidBodyBase |
| 00688490 | `0068849C` `call` | 0069DB10 | Phyre::PPhysics::PPhysicsShapeBullet |
| 00688700 | `0068870C` `call` | 0069CF30 | Phyre::PPhysics::PPhysicsMeshBullet |
| 00688780 | `0068878C` `call` | 0069DFD0 | Phyre::PPhysics::PPhysicsTaperedCapsule |
| 006891B0 | `006891BC` `call` | 0069C0F0 | Phyre::PPhysics::PPhysicsCharacterController |
| 00689260 | `0068926C` `call` | 0069C940 | Phyre::PPhysics::PPhysicsInterfaceBase |
| 00689480 | `0068948C` `call` | 0069D8B0 | Phyre::PPhysics::PPhysicsShape |
| 006894A0 | `006894AC` `call` | 0069CCD0 | Phyre::PPhysics::PPhysicsMesh |
| 00689690 | `0068969C` `call` | 0069D2C0 | Phyre::PPhysics::PPhysicsPlaneBase |
| 00689FA0 | `00689FAC` `call` | 0069E5C0 | Phyre::PPhysics::PRaycastResult |
| 0068A100 | `0068A10C` `call` | 0069D780 | Phyre::PPhysics::PPhysicsRigidBodyBullet |
| 0068A4D0 | `0068A4DC` `call` | 0069DD70 | Phyre::PPhysics::PPhysicsSphereBase |
| 0068A730 | `0068A73C` `call` | 0069C5B0 | Phyre::PPhysics::PPhysicsCylinderBase |
| 0068A750 | `0068A75C` `call` | 0069CA70 | Phyre::PPhysics::PPhysicsInterfaceBullet |
| 0068A7B0 | `0068A7BC` `call` | 0069D3F0 | Phyre::PPhysics::PPhysicsPlaneBullet |
| 0068B2F0 | `0068B2FC` `call` | 0069E360 | Phyre::PPhysics::PPhysicsWorldBase |
| 0068B3A0 | `0068B3AC` `call` | 0069D520 | Phyre::PPhysics::PPhysicsRigidBody |
| 0068B650 | `0068B65C` `call` | 0069DEA0 | Phyre::PPhysics::PPhysicsSphereBullet |
| 0068B670 | `0068B67C` `call` | 0069C810 | Phyre::PPhysics::PPhysicsInterface |
| 0068B7E0 | `0068B7EC` `call` | 0069C6E0 | Phyre::PPhysics::PPhysicsCylinderBullet |
| 0068B800 | `0068B80C` `call` | 0069D190 | Phyre::PPhysics::PPhysicsPlane |
| 0068C500 | `0068C50C` `call` | 0069DC40 | Phyre::PPhysics::PPhysicsSphere |
| 0068C5E0 | `0068C5EC` `call` | 0069D060 | Phyre::PPhysics::PPhysicsModel |
| 0068C600 | `0068C60C` `call` | 0069C480 | Phyre::PPhysics::PPhysicsCylinder |
| 0068CE60 | `0068CE6C` `call` | 0069B8A0 | Phyre::PPhysics::PPhysicsBoxBase |
| 0068CE80 | `0068CE8C` `call` | 0069BD60 | Phyre::PPhysics::PPhysicsCapsuleBase |
| 0068D070 | `0068D07C` `call` | 0069BB00 | Phyre::PPhysics::PPhysicsCallbackData |
| 0068D480 | `0068D48C` `call` | 0069BFC0 | Phyre::PPhysics::PPhysicsCharacterCamera |
| 0068D920 | `0068D92C` `call` | 0069B9D0 | Phyre::PPhysics::PPhysicsBoxBullet |
| 0068D940 | `0068D94C` `call` | 0069BE90 | Phyre::PPhysics::PPhysicsCapsuleBullet |
| 0068DFB0 | `0068DFBC` `call` | 0069CBA0 | Phyre::PPhysics::PPhysicsMaterial |
| 0068DFD0 | `0068DFDC` `call` | 0069E490 | Phyre::PPhysics::PPhysicsWorldBullet |
| 0068E200 | `0068E20C` `call` | 0069B770 | Phyre::PPhysics::PPhysicsBox |
| 0068E220 | `0068E22C` `call` | 0069BC30 | Phyre::PPhysics::PPhysicsCapsule |
| 0068E770 | `0068E77C` `call` | 0069C220 | Phyre::PPhysics::PPhysicsCharacterControllerBase |
| 0068ED80 | `0068ED8C` `call` | 0069CE00 | Phyre::PPhysics::PPhysicsMeshBase |
| 0068EE80 | `0068EE8C` `call` | 0069E100 | Phyre::PPhysics::PPhysicsTaperedCylinder |
| 0068EEA0 | `0068EEAC` `call` | 0069D9E0 | Phyre::PPhysics::PPhysicsShapeBase |
| 006A3D20 | `006A3D2C` `call` | 0069B630 | decorated `V?$PSharray@PEAVPPhysicsShape@PPhysics@Phyre@@@Phyre@@` |
| 006A6F40 | `006A6F4C` `call` | 006A75B0 | Phyre::PString |
| 006A79C0 | `006A79CC` `call` | 006A8B60 | Phyre::PGameplay::PTrigger |
| 006A9160 | `006A916C` `call` | 006A8A20 | decorated `V?$PSharray@PEAVPTriggerReceiverComponent@PGameplay@Phyre@@@Phyre@@` |
| 006A94A0 | `006A94AC` `call` | 006A9AE0 | Phyre::PGameplay::PQuarryComponent |
| 006A9C40 | `006A9C4C` `call` | 006AA050 | Phyre::PTypedObject |
| 006AA720 | `006AA72C` `call` | 006AAF00 | Phyre::PComponent |
| 006AB320 | `006AB32C` `call` | 006AC1D0 | Phyre::PEntity |
| 006ACD90 | `006ACD9C` `call` | 006AD370 | Phyre::PCameraOrthographic |
| 006AD600 | `006AD60C` `call` | 006ADAF0 | Phyre::PCameraPerspective |
| 006ADCA0 | `006ADCAC` `call` | 006AEE00 | Phyre::PInstancesComponent |
| 006AF570 | `006AF57C` `call` | 006AECC0 | decorated `V?$PArray@VPTypedObject@Phyre@@$07@Phyre@@` |
| 006AF9A0 | `006AF9AC` `call` | 006AFF70 | Phyre::PNameComponent |
| 006B0240 | `006B024C` `call` | 006B0630 | Phyre::PRandom::PRandomGenerator |
| 006B39C0 | `006B39CC` `call` | 006B3780 | Phyre::PMatrix4x3 |
| 006B3C10 | `006B3C1C` `call` | 006B5170 | Phyre::PScene::PNode |
| 006B6970 | `006B697C` `call` | 006B8BE0 | Phyre::PRendering::PMeshSegmentContext |
| 006BB480 | `006BB48C` `call` | 006BE020 | Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment |
| 006BB9E0 | `006BB9EC` `call` | 006BDEF0 | Phyre::PDynamicGeometry::PModifierNetworkDynamicMesh |
| 006BE240 | `006BE24C` `call` | 006BDB30 | decorated `V?$PArray@PEBE$07@Phyre@@` |
| 006BE260 | `006BE26C` `call` | 006BDC70 | decorated `V?$PArray@VPModifierNetworkDynamicMeshSegment@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006BE280 | `006BE28C` `call` | 006BDDB0 | decorated `V?$PArray@VPRenderStream@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006BE840 | `006BE84C` `call` | 006BFB10 | Phyre::PRendering::PLight |
| 006C0710 | `006C071C` `call` | 006C20A0 | Phyre::PRendering::PShadowCaster |
| 006C0930 | `006C093C` `call` | 006C21D0 | Phyre::PRendering::PShadowCaster::PShadowSplit |
| 006C25B0 | `006C25BC` `call` | 006C1F60 | decorated `V?$PArray@VPShadowSplit@PShadowCaster@PRendering@Phyre@@$07@Phyre@@` |
| 006C2810 | `006C281C` `call` | 006C41C0 | Phyre::PDynamicGeometry::PModifierNetworkInstanceInput |
| 006C2A40 | `006C2A4C` `call` | 006C42F0 | Phyre::PDynamicGeometry::PModifierNetworkInstancePacketInput |
| 006C2C60 | `006C2C6C` `call` | 006C4090 | Phyre::PDynamicGeometry::PModifierNetworkInstance |
| 006C4490 | `006C449C` `call` | 006C3F50 | decorated `V?$PArray@PEBVPBase@Phyre@@$07@Phyre@@` |
| 006C4900 | `006C490C` `call` | 006C7210 | Phyre::PLOD::PLODLevel |
| 006C4C00 | `006C4C0C` `call` | 006C70E0 | Phyre::PLOD::PLODGroup |
| 006C7820 | `006C782C` `call` | 006C6E60 | decorated `V?$PArray@VPLODLevel@PLOD@Phyre@@$07@Phyre@@` |
| 006C7840 | `006C784C` `call` | 006C6FA0 | decorated `V?$PSharray@PEAVPMeshInstance@PRendering@Phyre@@@Phyre@@` |
| 006C8060 | `006C806C` `call` | 006C8520 | Phyre::POccluderGeometry::POccluderGeometryInstance |
| 006CCE00 | `006CCE0C` `call` | 006CD140 | Phyre::PGameplay::PScriptableComponent |
| 006CD6E0 | `006CD6EC` `call` | 006CDC00 | Phyre::PGameplay::PTriggerReceiverTypeCallbackData |
| 006CDDB0 | `006CDDBC` `call` | 006CE440 | Phyre::PGameplay::PTriggerReceiverComponent |
| 006CE900 | `006CE90C` `call` | 006D4700 | Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_Buffer |
| 006CEB10 | `006CEB1C` `call` | 006D4BC0 | Phyre::PDynamicGeometry::PRenderStreamInput |
| 006CEC30 | `006CEC3C` `call` | 006D45D0 | Phyre::PDynamicGeometry::PModifierNetworkInfoPacket |
| 006CEEF0 | `006CEEFC` `call` | 006D4A90 | Phyre::PDynamicGeometry::PRenderStream |
| 006CF150 | `006CF15C` `call` | 006D44A0 | Phyre::PDynamicGeometry::PModifierNetworkBuffer |
| 006CF3A0 | `006CF3AC` `call` | 006D4240 | Phyre::PDynamicGeometry::PModifierAndInputs |
| 006CF5D0 | `006CF5DC` `call` | 006D4830 | Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierCode |
| 006CF800 | `006CF80C` `call` | 006D4370 | Phyre::PDynamicGeometry::PModifierNetwork |
| 006CF900 | `006CF90C` `call` | 006D4960 | Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierInstance |
| 006D4EC0 | `006D4ECC` `call` | 006D3E80 | decorated `V?$PArray@VPModifierAndInputs@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006D4EE0 | `006D4EEC` `call` | 006D3FC0 | decorated `V?$PArray@VPModifierNetworkBuffer@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006D4F00 | `006D4F0C` `call` | 006D4100 | decorated `V?$PArray@VPRenderStreamInput@PDynamicGeometry@Phyre@@$03@Phyre@@` |
| 006D71A0 | `006D71AC` `call` | 006D90D0 | Phyre::PDynamicGeometry::PMorphModifierWeightsUserDataObject |
| 006D9CE0 | `006D9CEC` `call` | 006DA250 | Phyre::POccluderGeometry::POccluderGeometryObject |
| 00791260 | `0079126C` `call` | 00796BC0 | Phyre::PFramework::PDebugUtils |
| 007914C0 | `007914CC` `call` | 00796960 | Phyre::PFramework::PApplication |
| 00791660 | `0079166C` `call` | 00796A90 | Phyre::PFramework::PApplicationViewport |
| 00791850 | `0079185C` `call` | 00796CF0 | Phyre::PFramework::PInputMapper |
| 00867360 | `0086736C` `call` | 00872DE0 | Phyre::PInputs::PInputSourceVisionTrackerZ |
| 00867410 | `0086741C` `call` | 00871C10 | Phyre::PInputs::PInputSourceMotionQuatW |
| 008674C0 | `008674CC` `call` | 008727F0 | Phyre::PInputs::PInputSourceTouchRotate |
| 00867AD0 | `00867ADC` `call` | 008714F0 | Phyre::PInputs::PInputSourceMotionAngularVelocityX |
| 00867B80 | `00867B8C` `call` | 008726C0 | Phyre::PInputs::PInputSourceTouchPinch |
| 00867FD0 | `00867FDC` `call` | 00870DD0 | Phyre::PInputs::PInputAction |
| 00868080 | `0086808C` `call` | 00871030 | Phyre::PInputs::PInputSource |
| 008681A0 | `008681AC` `call` | 00871620 | Phyre::PInputs::PInputSourceMotionAngularVelocityY |
| 008682E0 | `008682EC` `call` | 00872920 | Phyre::PInputs::PInputSourceTouchTwoFingerDragX |
| 008688E0 | `008688EC` `call` | 008713C0 | Phyre::PInputs::PInputSourceKey |
| 00868A00 | `00868A0C` `call` | 00871750 | Phyre::PInputs::PInputSourceMotionAngularVelocityZ |
| 00868AB0 | `00868ABC` `call` | 00872A50 | Phyre::PInputs::PInputSourceTouchTwoFingerDragY |
| 00869090 | `0086909C` `call` | 00870F00 | Phyre::PInputs::PInputMap |
| 008691B0 | `008691BC` `call` | 00871290 | Phyre::PInputs::PInputSourceJoypadButton |
| 00869280 | `0086928C` `call` | 00871880 | Phyre::PInputs::PInputSourceMotionLinearAccelerationX |
| 00869400 | `0086940C` `call` | 00872460 | Phyre::PInputs::PInputSourceTouchDragX |
| 00869A50 | `00869A5C` `call` | 00871160 | Phyre::PInputs::PInputSourceJoypadAxis |
| 00869B00 | `00869B0C` `call` | 008719B0 | Phyre::PInputs::PInputSourceMotionLinearAccelerationY |
| 00869BB0 | `00869BBC` `call` | 00872590 | Phyre::PInputs::PInputSourceTouchDragY |
| 0086A220 | `0086A22C` `call` | 008720D0 | Phyre::PInputs::PInputSourceMouseButton |
| 0086A2D0 | `0086A2DC` `call` | 00871AE0 | Phyre::PInputs::PInputSourceMotionLinearAccelerationZ |
| 0086A380 | `0086A38C` `call` | 00871D40 | Phyre::PInputs::PInputSourceMotionQuatX |
| 0086A980 | `0086A98C` `call` | 00872B80 | Phyre::PInputs::PInputSourceVisionTrackerX |
| 0086AA80 | `0086AA8C` `call` | 00872200 | Phyre::PInputs::PInputSourceMouseDeltaX |
| 0086AAA0 | `0086AAAC` `call` | 00871E70 | Phyre::PInputs::PInputSourceMotionQuatY |
| 0086B0F0 | `0086B0FC` `call` | 00872CB0 | Phyre::PInputs::PInputSourceVisionTrackerY |
| 0086B1A0 | `0086B1AC` `call` | 00871FA0 | Phyre::PInputs::PInputSourceMotionQuatZ |
| 0086B250 | `0086B25C` `call` | 00872330 | Phyre::PInputs::PInputSourceMouseDeltaY |
| 00873CF0 | `00873CFC` `call` | 00870B50 | decorated `V?$PArray@PEAVPInputAction@PInputs@Phyre@@$07@Phyre@@` |
| 00873D10 | `00873D1C` `call` | 00870C90 | decorated `V?$PArray@PEAVPInputSource@PInputs@Phyre@@$07@Phyre@@` |
| 00874770 | `0087477C` `call` | 00874FD0 | Phyre::PVision::PVisionMoveTrackerBase |
| 00874900 | `0087490C` `call` | 00875100 | Phyre::PVision::PVisionMoveTrackerWin32 |
| 00874A90 | `00874A9C` `call` | 00874EA0 | Phyre::PVision::PVisionMoveTracker |
| 008753E0 | `008753EC` `call` | 00875BB0 | Phyre::PVision::PVisionTrackerBase |
| 00875570 | `0087557C` `call` | 00875CE0 | Phyre::PVision::PVisionTrackerWin32 |
| 00875700 | `0087570C` `call` | 00875A80 | Phyre::PVision::PVisionTracker |
| 00877410 | `0087741C` `call` | 00879000 | Phyre::PHierarchy::POctreeWorld |
| 00877640 | `0087764C` `call` | 00878ED0 | Phyre::PHierarchy::POctreeData |
| 00877890 | `0087789C` `call` | 00878C70 | Phyre::PHierarchy::POctree |
| 00877AF0 | `00877AFC` `call` | 00878DA0 | Phyre::PHierarchy::POctreeChildren |
| 00879830 | `0087983C` `call` | 0087A550 | Phyre::PGame::PGameConfig |
| 0087A6D0 | `0087A6DC` `call` | 0087A410 | decorated `V?$PArray@PEAVPInputMap@PInputs@Phyre@@$07@Phyre@@` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-return-value-adapter-family-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `006B2A60` | 120 B | calls `00683B10(rdx)` and copies the 0x40 bytes at the returned pointer to `r8` as 16 dwords (`+0` through `+0x3c`) | Interior anchor `006B2A6C`; Interior anchor `006B2A74`; Interior anchor `006B2A76`; Interior anchor `006B2ACC`; Interior anchor `006B2ACF` |
