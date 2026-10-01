# V121 corrected post-CS audit GE persistence seal — 2026-08-31

**Verdict: PERSISTENCE_CERTIFIED**

Latest durable local V121 continuation GZF:
`FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_CORRECTED_POST_CS_AUDIT_GE_99P53_2026-08-31.gzf`

- GZF size: **82,114,676 bytes**
- GZF SHA-256: `caa00eaf03422d6ecb00775954dbb676ea7db1ded5c77313499ee5383b7f6987`
- Internal functions: **38,161**
- Explicitly accounted: **37,983 / 38,161 = 99.53356%**
- Unresolved: **178**
- Cross-layer overlap: **0**
- Pre-GE deterministic snapshot SHA-256: `0b70c83433e1319f80b240a1ac41cf0feca306c245c3220bb5eea73630a53bc1`
- Exact post-GE snapshot SHA-256: `d89e38f53d92495a7992943fa317e4ffdc495b8911687c833e41833a65ffa470`
- Fresh-reopen snapshot SHA-256: `d89e38f53d92495a7992943fa317e4ffdc495b8911687c833e41833a65ffa470` — byte-identical to post-GE
- Fresh residual SHA-256: `917baef493e33453223af183b2529f233bacd41c55815bf3f78162a6262991c8`
- Manifest SHA-256: `b23d4d17b1d5fc7b05762029f1eeec38709eb5f3ce4aff8bd5d8064cc90e9a8d`
- Embedded EXE SHA-256: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8` — exact authorized binary

## GE semantic closure

### 1. `00692AC0` — `Phyre.PPhysics.PPhysicsWorld.DeepCopyAssignment`

The complete current body copies the fixed PPhysicsWorld state and performs owned deep replacement of four dynamic record arrays: one array whose records are 0x24 bytes and three arrays whose records are 0x30 bytes. Where the destination already owns replaceable storage, the routine releases that old allocation before publishing the new deep copy.

Independent class evidence is concrete. Slot 3 of both the real `PClassDescriptorConcrete<Phyre::PPhysics::PPhysicsWorld>` and `PClassDescriptorConcrete<Phyre::PPhysics::PPhysicsWorldBullet>` vtables reaches adapters that first obtain typed object references through authored `PScriptAccessors::PObjectAccessor<... &>::Get` paths and then call `00692AC0(destination, source)`. This proves object assignment/copy semantics for the PPhysicsWorld class-descriptor path rather than generic container adjacency.

### 2. `00626120` — `Phyre.PRendering.PTexture2DD3D11.BufferSlotMipChainMapForCPUWrite`

The complete current body validates a selected PTexture2D buffer slot, bounds its mip count, computes format-aware storage/pitch while halving width and height for each mip, and produces a per-mip pointer/row-pitch descriptor chain. It has two native paths: allocate contiguous CPU backing and partition it across mips, or map each native subresource through the rendering-context map virtual using the texture-selected write/write-discard map mode. Unused descriptor entries are zeroed.

Its direct PTexture2D caller family includes the authored warning `Altering buffer count of PTexture2D whilst bound. Rebind needed.`; the resulting descriptors feed the already-certified PTexture2D update machinery. This resolves the function specifically as the 2D texture CPU-write mip mapping stage.

## Exact-current-body fence

- `00692AC0`: body size **923 bytes**; SHA-256 `e0a920affa2c87d23132d6f84216fa35b19221218c761bd5f69f789a504f7d0f`
- `00626120`: body size **971 bytes**; SHA-256 `d736c2431143272994ee59ea538716aa1d5fa852fd0e6ac844580ebbe829a402`

Both targets were unresolved and uncommented immediately before GE mutation.

## Whole-project mutation proof

Deterministic comparison across all **38,161 functions** from the certified GD-recovery parent state to GE:

- changed functions: **2**
- exact changed entries: `00626120`, `00692AC0`
- comments changed: **2**
- CodeDomain tags added: **2**
- tags removed: **0**
- functions added/removed: **0 / 0**
- immutable changed count: **0**
- body hashes/ranges, names, prototypes, thunk state, external state and every non-target function: unchanged

The ledger changed only from **37,981 explicit / 180 unresolved** to **37,983 explicit / 178 unresolved**.

## Packing / fresh-reopen proof

The GE DomainFile was packed from a separate headless invocation without processing the target program. Pack preconditions reported:

`open=false busy=false changed=false canSave=false`

and the packer emitted explicit `PACK_PASS`, producing **82,114,676 bytes**.

That GZF was copied byte-for-byte into writable scratch and imported into a completely new Ghidra project. The fresh project independently reproduced:

- **38,161 total functions**
- **37,983 explicit**
- **178 unresolved**
- **0 cross-layer overlap**
- executable SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`
- deterministic all-function snapshot byte-identical to post-GE (`d89e38f53d92495a7992943fa317e4ffdc495b8911687c833e41833a65ffa470`)

## Corrected-lineage rule

No PE `.pdata`, `.xdata`, `UNWIND_INFO`, `IPToStateMapEntry`, `_IMAGE_RUNTIME_FUNCTION_ENTRY`, or similar exception metadata was used to classify either GE function. Such references were explicitly rejected during evidence review.

## Next frontier

The exact fresh-reopened GE residual contains **178 unresolved internal functions**. The protected mixed-context functions `002F7380` and `00313A00` remain unresolved and untouched.

The strongest already-researched next family consists of callback-bound legacy Presentation effect helpers `004753B0` and `004EB910`; their complete mechanics are strong, but any next mutation must retain conservative mechanism labels rather than inventing a visual-effect name.
