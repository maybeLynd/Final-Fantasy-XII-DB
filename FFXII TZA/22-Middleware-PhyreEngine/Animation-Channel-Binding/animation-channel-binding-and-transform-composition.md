---
system: Animation channel binding and transform composition
category: 22-Middleware-PhyreEngine
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS): the ChannelValue slot's remaining 16 bytes (BM-3) answered 2026-09-26; which systems bind channels to shader parameters answered as BM-4 2026-09-22 (none; UQ-278 is SUPERSEDED as its duplicate); whether other semantics get special handling (UQ-277) answered 2026-09-18: no, the other referencing functions are descriptor registration and teardown; the member-flag word (UQ-279) and the member kinds (UQ-281) answered 2026-09-17 (status line current 2026-09-30, SWE2-DATA)
owner_layer: CodeDomain:Phyre.Animation — no PrimaryOwner (middleware)
evidence_tier: 2
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
audit:
  passes: 2
  last_pass: 2026-09-13
  last_pass_kind: audit
  last_pass_state: opus-animation-channel-binding-pass-2 - the composer's arithmetic, the block BOTH earlier passes named as untested. EVERY formula in section 4 is EXACT: the normalize, the quaternion-to-matrix arm, the scale-only arm with its explicit off-diagonal zeroing, the rotation-and-scale arm traced ALL NINE TERMS, the translation row, and the claim that m[3]/m[7]/m[11]/m[15] are never written (no store to +0x0C, +0x1C, +0x2C or +0x3C exists). NEW: 01CEBBA8 has TWO jobs - it is also the 1 in every diagonal term, read at four sites, not just the reciprocal numerator. The non-transform dispatch reproduces and CLOSES A LOOP: the consumer reads kinds 2 and 3 and calls the variadic setter, while pass 1 showed the binder writes only kind 1, so both halves are measured and still do not meet. INSTRUMENT FAILURE AGAIN: a mnemonic scan for sqrt over the whole body returns ZERO because the square root is call 0x861F14, a six-byte import thunk named sqrtf - fourth confident zero this session, and it weakened an implication I drew on the spatial-audio page, which is corrected
  crossref_clean: false
  reopened_count: 0
  falsification_passes: 1
  last_falsification: 2026-09-03
  last_falsification_by: repos-9e
  last_falsification_state: GN158 checkpoint, project GFZ_H9E
  falsification_result: 3 overturned, 6 survived, BM-1 closed - see section 10
---

# Animation channel binding and transform composition

> How a curve in an animation file finds the thing it moves, and how three separate curves —
> rotation, scale and translation — become the single matrix that puts a bone where you see it.

## 1. What the player sees

When Vaan swings a sword, the animation is not one thing. It is a bundle of separate curves,
each one steering a single named property of a single bone: *this shoulder's rotation*, *this
hand's position*, *this bone's size*. Every frame, the engine reads a value off each curve and
writes it into the skeleton, and the result is the pose you see.

Two consequences of how this is wired are visible in ordinary play.

The first is that **rotation, scale and position are handled separately and then combined**. An
animation that only steers rotation leaves the character's size and position exactly where the
previous system put them. This is why a character can be scaled up by an effect and still play
all their normal attack animations correctly — the animation is not fighting the scale, it never
touches it.

The second is that **an animation can drive things that are not bones at all**. ~~The same~~
~~machinery that moves a shoulder can drive a number inside a material — a shader parameter — which~~
~~is how effects that pulse, fade or shift colour in time with an animation stay in sync with it.~~
~~They are not a separate timed effect running alongside the animation; they are channels in the~~
~~same animation, bound to a different kind of target.~~ *(Corrected 2026-09-30, SWE2-DATA, from `BM-4`: the machinery can bind a channel to a shader parameter or any reflected property, but no shipped asset does. The shipped game has four channel targets, in two map assets, and each drives `setVisibilityFromAnimation` on one named node: a node that appears and disappears with the animation. No shipped effect is kept in sync with an animation this way.)*

If this system broke, you would not see a character freeze. You would see them come apart:
limbs at the wrong scale, a weapon translating without rotating~~, or an effect's glow stuck at~~
~~whatever value it held when the binding failed~~ *(struck 2026-09-30, SWE2-DATA: no shipped binding drives a glow, `BM-4`)*.

## 2. Native mechanism

There are two phases, and they happen at very different times. **Binding** happens once, when the
animation is attached to its target. **Composition** happens every frame.

### Binding — resolving a name to an address

An animation channel does not store the address of the thing it drives; a shipped animation file
cannot know where an object will live in memory. It stores a **name**, and the name is a dotted
path through the engine's own reflection data — the same class-descriptor system documented in
[`../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md).

`005C0820` walks that path. For each binding descriptor it splits the name on `'.'` (`strchr(name,
0x2e)`), looks each segment up as a member of the current class descriptor, and accumulates a byte
offset as it descends. When the path runs out, it has an address and a size, and it writes them
into a **target record** that the per-frame code will use without ever touching a string again.

That is the important structural point for a modder: **the cost of name resolution is paid once at
bind time, and the per-frame path is a raw pointer write.** It also means a mistyped or renamed
member does not crash — it silently fails to bind, and the channel simply does nothing. *(Anchored 2026-09-30, SWE2-DATA: when the per-segment member lookup returns null (`005C0983`), the binder only releases and jumps past its one kind store (`005C0AF4`) without calling the log routine the out-of-range refusal calls; `_index/candidates/dd-data-2-0930/anim_checks.py` A1, A2, control C1.)*

The binder handles array members too. If the resolved member is an array, the descriptor carries an
index, and the binder bounds-checks it before computing `base + index * elementSize`. When the index
is out of range it refuses the binding and logs it — this is the engine telling you, in its own
words, that a channel was dropped:

```
Not binding %s:%s because array index (%d) exceeds array size (%d)
```

A binding can resolve to one of four kinds, recorded in the target record's first field. Kind 0 is
an unbound channel — nothing resolved, and the per-frame code skips it entirely. Kind 1 is a direct
memory write. Kinds 2 and 3 route the value through a reflected **setter** rather than writing
memory, which is how a target that needs to react to being changed (recompute something, mark itself
dirty) gets the chance to.

### Composition — turning channels into a matrix

`005C72A0` runs the per-frame half. It walks the animation's channel list and, for each channel,
identifies *what the channel means* — and it does this by **pointer identity, not string comparison**.

Each channel carries a pointer to a shared 24-byte **semantic descriptor**. There is exactly one
descriptor object per semantic in the whole image, so the test is a pointer compare against three
known globals: `Rotation`, `Translation`, `Scale`. This is fast, and it is also why a semantic is not
something authored data can invent — it must be one of the descriptors the engine ships.

Channels are grouped by target. The walk gathers every channel that feeds the *same* target, folding
each one into a set of local accumulators and setting a bit to record which semantics were actually
present. Only when the group ends does it compose:

- If the group contained a **rotation**, the quaternion is normalized and expanded into a 3×3 basis.
- If it contained a **scale**, each row of that basis is multiplied by the matching scale component.
- If it contained a **translation**, it is written into the matrix's fourth row.

The bit-per-semantic accumulator is what makes partial animations work correctly. A channel group
with only a translation writes **only** the translation row and leaves the basis untouched — it does
not helpfully write an identity rotation over whatever was there. That is the behaviour described in
§1: an animation that does not mention scale genuinely does not disturb scale.

Channels whose semantic is **not** one of the three transform semantics skip the matrix path
entirely and are dispatched straight to the target by kind, as a memcpy or a setter call.

**That set is much larger than a shader parameter (§10).** The shipped table also carries
**light colour, intensity and falloff**, **camera field of view, near plane, far plane and
orthographic size**, **morph target weight** — the channel that drives facial expression — and four
**user attribute** types. A single animation file can therefore pull the camera's FOV, dim a light
and change a face in the same bundle of curves that moves the skeleton, staying in sync for the
reason §1 gives: they are channels in the same animation, not separate timed effects. *(Qualified 2026-09-30, OPUS:
this is what the table and the binders allow. ~~The shipped data uses it four times, all for node visibility (`BM-4`,
the section below), so no shipped light, camera, face or material is animated this way.~~)* The shipped Phyre
cluster data uses it four times, all for node visibility (`BM-4`, the section below), so no light, camera, face or
material is animated through the authored channel-target route. A binding built natively at run time would not
appear in that census. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-dd-anim-0930/REVIEW.md) correction wording)*

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `005C72A0` | `AnimationTargetBlender_ApplyChannelsToTargets` | 1,674 B | per-frame: classify each channel by semantic, group by target, compose the TRS matrix, dispatch non-transform channels |
| `005C0820` | `AnimationChannelTargetBind_ResolveDataMemberPath` | 827 B | bind-time: resolve a dotted reflection path to `{address, size}`, bounds-check array indices, emit the target record |
| `005C6020` | `AnimationAdditiveBlender_MarkContributedSlots` | 323 B | mark which output slots this controller contributes to — **additive** rule |
| `005C61A0` | `AnimationWeightedBlender_MarkContributedSlots` | 288 B | same, **weighted** rule |
| `005A7E90` | `AnimationTarget_InvokeReflectedSetter` | 61 B | kind 2/3 dispatch: virtual call through the target object's setter |

Addresses are Ghidra image base `0x00120000`. **Every row above is a function**, and its body size is
an exact-current body extent (`body_end - body_start + 1`).

### Data addresses cited by this document

These are **data, not functions**, and carry no body extent. They are listed separately so that a
cross-reference audit does not read them as functions that have gone missing.

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01F2CE40` | `ChannelSemantic_Rotation` | 24-byte descriptor | `{"Rotation", 0, 4}` |
| `01F2CE58` | `ChannelSemantic_Translation` | 24-byte descriptor | `{"Translation", 0, 3}` |
| `01F2CE70` | `ChannelSemantic_Scale` | 24-byte descriptor | `{"Scale", 0, 3}` |
| `01F2CE88` | `ChannelSemantic_ShaderParameterF4` | 24-byte descriptor | `{"ShaderParameterF4", 0, 4}` |
| `01F2CEA0` | `ChannelSemantic_ShaderParameterF3` | 24-byte descriptor | `{"ShaderParameterF3", 0, 3}` |
| `01F2CEB8` | `ShaderParameterF2` | 24-byte descriptor | component count 2; **name read 2026-09-03, BM-1 CLOSED** — was `ChannelSemantic_(unread)` |
| `01CEBBA8` | `kOne` | `f32` constant | `0x3F800000` = `1.0f`, the reciprocal numerator in the quaternion normalize |

## 4. Data structures and formulas

### Channel semantic descriptor — 24 B

One shared, immutable instance per semantic. Channels point *at* these; identity is the pointer.

```
ChannelSemantic
  +0x00  ptr  name            const char*, e.g. "Rotation"
  +0x08  ptr  (always 0 in the shipped table)
  +0x10  u32  componentCount  floats this semantic consumes
```

Shipped table, contiguous at `0x01F2CE40`, stride `0x18`:

| Address | Name | Components |
|---|---|---:|
| `01F2CE40` | `Rotation` | 4 |
| `01F2CE58` | `Translation` | 3 |
| `01F2CE70` | `Scale` | 3 |
| `01F2CE88` | `ShaderParameterF4` | 4 |
| `01F2CEA0` | `ShaderParameterF3` | 3 |
| `01F2CEB8` | `ShaderParameterF2` | 2 |
| `01F2CED0` | `ShaderParameterF1` | 1 |
| `01F2CEE8` | `LightColor` | 4 |
| `01F2CF00` | `LightIntensity` | 1 |
| `01F2CF18` | `LightFalloffAndPenumbra` | 2 |
| `01F2CF30` | `CameraFov` | 1 |
| `01F2CF48` | `CameraZNear` | 1 |
| `01F2CF60` | `CameraZFar` | 1 |
| `01F2CF78` | `CameraOrthographicSize` | 1 |
| `01F2CF90` | `MorphTargetWeight` | 1 |
| `01F2CFA8` | `UserAttributeBool` | 1 |
| `01F2CFC0` | `UserAttributeInt` | 1 |
| `01F2CFD8` | `UserAttributeFloat` | 1 |
| `01F2CFF0` | `UserAttributeVector` | 1 |

> **Corrected 2026-09-03 by falsification pass 1 (§10).** This table listed **six** rows and stopped
> at an *(unread)* entry. The run is **nineteen** entries, ends at `01F2D008` where the name pointer
> is `0`, and **every one of the nineteen is referenced from `.text`.**

### Channel value slot — 40 B (`0x28`), indexed by channel index

```
ChannelValue
  +0x00  f32  c0
  +0x04  f32  c1
  +0x08  f32  c2
  +0x0C  f32  c3
  +0x10  ptr  semantic       -> ChannelSemantic, or 0 for an inactive channel
  +0x18  ...  (remaining 16 B not read by 005C72A0)   <- corrected 2026-10-02, OPUS - answered 2026-09-26: +0x18 u16 and +0x1C dword from the bind-time writer 005BF290, +0x20..+0x27 an uninterpreted tail
```

### Target record — 48 B (`0x30`), indexed by target index

Written by the binder (`005C0820`), consumed by the composer (`005C72A0`).

```
AnimationTarget
  +0x00  u32  kind      0 = unbound (skip), 1 = direct memory, 2 = setter+context, 3 = setter
  +0x08  ptr  dest      kind 1: destination address (also the matrix base)
  +0x10  u32  size      kind 1: bytes to copy, CLAMPED to <= 0x10
  +0x18  ptr  context   kind 2: second argument to the setter      [consumer-only]
  +0x20  ptr  object    kind 2: object whose setter is invoked     [consumer-only]
  +0x28  ptr  object    kind 3: object whose setter is invoked     [consumer-only]
```

> **Which half of this is producer-confirmed (audit pass 1, section 11).** `005C0820` writes
> **only** `+0x00`, `+0x08` and `+0x10`, and the value it writes at `+0x00` is the **literal
> constant 1** (`mov dword ptr [rax], 1` at `005C0AF4`). It never stores to `+0x18`, `+0x20` or
> `+0x28`. The last three rows are read off the **consumer** (`005C72A0`) alone: their *physical
> access* by the consumer is proven, their *production* is not. ~~Whatever writes a kind-2 or kind-3~~
> ~~record is still unidentified - that is section 7's last open item, and it is now a measured gap~~
> ~~rather than a suspicion.~~ *(Corrected 2026-09-30, SWE2-DATA: `BM-6` answered 2026-09-14. The binder is a virtual family: `…BindMethod` writes kind 2 and `…BindFunction` kind 3, each reached only through its vtable.)*

The size clamp is literal and unconditional:

```c
if (0x10 < size) size = 0x10;   // a channel can never write more than 16 bytes
```

### Binding descriptor — 56 B (`0x38`), the binder's input

Only descriptors whose kind field equals 2 are treated as data-member binds:

```c
if (*(int *)(descriptor + 0x20) == 2)   // else: leave the target record unbound
```

Descriptor fields the binder reads, relative to the record base:

```
AnimationBindDescriptor
  +0x00  ptr  ownerObject    matched against the animation's object chain (walked via +0x78)
  +0x08  ptr  fallbackObject used when the animation supplies no explicit root
  +0x20  u32  kind           must be 2
  +0x28  ptr  path           dotted member path, MSVC short-string: low bit of the first
                             byte set means the pointer itself is inline storage
  +0x30  u32  arrayIndex     element index when the resolved member is an array
```

### Reflection path resolution

Per path segment, with `member` the resolved class-descriptor member:

```c
offset += (int)member[9] - *(int *)(member[3] + 0xF4);   // member offset - owning class base
```

Array element address:

```c
elementSize = *(u32 *)(arrayType + 0x38);
address     = arrayBase(target) + arrayIndex * elementSize;
// refused, with a log line, when:  arrayIndex >= arraySize
```

### Bound size - element size, the override to 8, and the clamp

The `size` written at `+0x10` is **not** simply the member's element size. Three things happen to
it, in order (`005C0A8F`..`005C0B09`):

```c
size = *(u32 *)(memberType + 0x38);            // the type's element size

// override, scalar path only:
u32 f = *(u32 *)(member + 0x28);               // member flags
bool isRef = (typeObject && typeObject->kind_0x5c == 2);
if ( ((~(f >> 6)) & isRef & 1) | ((f >> 1) & 1) )  size = 8;   // a pointer, not the pointee

if (0x10 < size) size = 0x10;                  // the clamp, literal and unconditional
```

**The override's second disjunct cannot fire on the path it sits on.** This branch is entered only
when the member type's `+0x5C` kind field read **zero**; the code then re-issues the *same* virtual
call on the *same* object and compares `+0x5C` against **2**. Unless that virtual returns a
different object on its second call within one iteration, `isRef` is always false here and the
override reduces to **`size = 8` when member-flag bit 1 is set**. The compiler declined to reuse the
first result, so it did not treat the call as pure; nothing in these bodies says whether it is *(answered: see UQ-280, 2026-09-14 - it is pure; 2026-10-02, OPUS)*.

### Member type kinds - `+0x5C`, and the refusal above 4

The path walk classifies the resolved member by its type object's `+0x5C`:

| `+0x5C` | route |
|---:|---|
| 0 (or no type object) | scalar path - element size, the override above, the clamp |
| 1, 2, 3, 4 | the bounds-checked **array** path: `arrayIndex` vs `count`, then `base + index * elementSize` - 1 fixed-size C array, 2 dynamic array through a pointer, 3 `PArray`, 4 `PSharray` (UQ-281, 2026-09-17) |
| >= 5 | **the binding is abandoned** - `dec eax; cmp eax, 3; ja` leaves the target record untouched; no constructor produces such a value, so this arm never runs (UQ-281, 2026-09-17) |

Section 2 says *"if the resolved member is an array"*. There are **four** array-ish kinds, and there
is an explicit refusal above them that is neither an array nor a scalar and produces **no log line
at all** - unlike the out-of-range index, which does.

### Semantic accumulator bits

Set as each channel in a target group is folded in:

```
bit 0 (0x1)  Rotation     seen
bit 1 (0x2)  Scale        seen
bit 2 (0x4)  Translation  seen
```

Composition is selected by `flags & 3`, and runs **only** when `target->kind == 1`:

```c
switch (flags & 3) {
  case 1: rotation only;
  case 2: scale only;
  case 3: rotation and scale;
  case 0: neither — basis left untouched;
}
if (flags & 4) write translation row;
```

### Quaternion normalize

With the channel's four floats as `(x, y, z, w)`:

```c
s = 1.0f / sqrtf(x*x + y*y + z*z + w*w);   // 1.0f is DAT_01CEBBA8 = 0x3F800000
X = x * s;  Y = y * s;  Z = z * s;  W = w * s;
```

### Quaternion to matrix — `flags & 3 == 1`

The destination is a 4×4 float matrix at `target->dest`, written as a **row-vector (row-major)**
basis. Indices are float indices; `m[3]`, `m[7]`, `m[11]`, `m[15]` are **never written** by this
function and must already hold `0,0,0,1`.

```c
m[0]  = 1 - 2*Y*Y - 2*Z*Z;    m[1]  = 2*X*Y + 2*Z*W;      m[2]  = 2*X*Z - 2*Y*W;
m[4]  = 2*X*Y - 2*Z*W;        m[5]  = 1 - 2*X*X - 2*Z*Z;  m[6]  = 2*Y*Z + 2*W*X;
m[8]  = 2*X*Z + 2*Y*W;        m[9]  = 2*Y*Z - 2*W*X;      m[10] = 1 - 2*X*X - 2*Y*Y;
```

### Scale only — `flags & 3 == 2`

A pure diagonal. Note the off-diagonals **are** explicitly zeroed here, unlike the `flags & 3 == 0`
case:

```c
m[0] = Sx;  m[1] = 0;   m[2]  = 0;
m[4] = 0;   m[5] = Sy;  m[6]  = 0;
m[8] = 0;   m[9] = 0;   m[10] = Sz;
```

### Rotation and scale — `flags & 3 == 3`

The rotation basis with **each row scaled by the matching component** — scale is applied in the
rotated frame, not the world frame:

```c
m[0]  = Sx * (1 - 2*Y*Y - 2*Z*Z);  m[1]  = Sx * (2*X*Y + 2*Z*W);  m[2]  = Sx * (2*X*Z - 2*Y*W);
m[4]  = Sy * (2*X*Y - 2*Z*W);      m[5]  = Sy * (1 - 2*X*X - 2*Z*Z); m[6] = Sy * (2*Y*Z + 2*W*X);
m[8]  = Sz * (2*X*Z + 2*Y*W);      m[9]  = Sz * (2*Y*Z - 2*W*X);  m[10] = Sz * (1 - 2*X*X - 2*Y*Y);
```

### Translation — `flags & 4`

```c
m[12] = Tx;  m[13] = Ty;  m[14] = Tz;
```

### Non-transform channel dispatch

Any channel whose semantic pointer is non-null and is none of the three transform descriptors:

```c
switch (target->kind) {
  case 1: memcpy(target->dest, &value, target->size);            break;  // size <= 0x10
  case 2: InvokeReflectedSetter(target->obj_0x20, target->ctx_0x18, &value); break;
  case 3: InvokeReflectedSetter(target->obj_0x28, 0,               &value); break;
}
```

`005A7E90` performs the call as a virtual through the object's member at `+0x28`, slot `+0x10` -
and it is a **variadic forwarder**, which the shape above hides:

```c
// signature: f(object, context, ...)   <- two fixed parameters, then varargs
void f(void *object, void *context, ...)
{
    // MSVC variadic prologue: spill arg2/arg3/arg4 to their home slots
    va_list ap = &home(arg3);                    // lea rax, [r11+0x18]
    void *handler = *(void **)(object + 0x28);
    if (handler)
        (*(code **)(*handler + 0x10))(handler, context, 0, 0, &ap);   // 5 args; &ap is stack arg 5
}
```

The value does **not** travel as `&value` in a fixed parameter. It is spilled into the variadic home
area, and the callee receives a **pointer to a `va_list`** in its fifth (stack) argument, two levels
of indirection from the value. The two zeros in `r8`/`r9` are the callee's own third and fourth
fixed parameters, not placeholders for the payload. This matters for a modder writing a setter: the
count of floats delivered is **not** fixed by this function, and the callee must walk the list.

### Slot contribution marking — additive vs weighted

Both controllers mark a byte array `mark[]` with which output slots they contribute to, reading a
parallel weight array at `controller + 0x30`:

```c
// WEIGHTED (005C61A0) — a zero weight contributes nothing
for (i = 0; i < count; i++)
    if (weight[i] != 0.0f) mark[slot[i]] = 1;

// ADDITIVE (005C6020) — slot 0 is marked UNCONDITIONALLY, weight ignored
if (count != 0) {
    mark[slot[0]] = 1;
    for (i = 1; i < count; i++)
        if (weight[i] != 0.0f) mark[slot[i]] = 1;
}
```

That single unconditional first write is the whole difference between the two, and it is the
correct behaviour for an additive blend: the base pose must always be present for the additive
layers to be added *to*, even when every layer's weight is zero.

Both loops are compiler-unrolled ×4 with a scalar remainder; the unrolling carries no semantics.

## 5. Call chain

```
animation asset bound to a scene object
  -> AnimationChannelTargetBind_ResolveDataMemberPath  005C0820        [BIND, once]
     -> Phyre reflection class-descriptor lookup (FUN_00597220)
        -> writes AnimationTarget records {kind, dest, size}

per-frame animation update
  -> blender controller evaluates channels into ChannelValue slots
     -> AnimationAdditiveBlender_MarkContributedSlots  005C6020        [which slots are live]
     -> AnimationWeightedBlender_MarkContributedSlots  005C61A0
  -> AnimationTargetBlender_ApplyChannelsToTargets     005C72A0        [APPLY, every frame]
     -> memcpy into a bone/scene matrix                               (kind 1)
     -> AnimationTarget_InvokeReflectedSetter  005A7E90               (kind 2/3)
        -> the target object's own setter
```

**Upstream (who causes this):** the animation system's per-frame evaluation. The **owner
transition** into this system is the bind at `005C0820` — before it, targets are names; after it,
they are addresses. Everything downstream of the bind is Phyre middleware with no FFXII
`PrimaryOwner`.

**Downstream (what this causes):** bone matrices consumed by skinning and by
[`../../17-Presentation-Rendering/Character-Rendering/character-render-object.md`](../../17-Presentation-Rendering/Character-Rendering/character-render-object.md);
and, through kinds 2/3, arbitrary reflected properties ~~including shader parameters~~; shader parameters go through kind 1 *(corrected 2026-10-02, OPUS: `PAnimationChannelTargetBindShaderParameter`'s binder `005C1160` writes kind 1 at `005C1274` and the destination at `005C127A`)*.

**Do not confuse with:**

- **`PAnimationBlenderController` slot 12 (`005C9F30`) is not this function.** It resizes a pointer
  array (count at `+0x18` with bit 31 as an ownership flag, data at `+0x20`). It shares a *slot
  number* with `PAnimationTargetBlenderController` slot 12 (`005C72A0`), and nothing else. RTTI slot
  indices are **per-vtable**; equal slot numbers in two classes are not the same virtual unless the
  classes share the base that declares it. That has not been established here.
- The `ShaderParameterF4` / `F3` semantics are *bound and dispatched* by this system but are not
  transform channels and never reach the matrix composition.

## 6. Modding notes

- **Best intervention point:** the target record produced by `005C0820`. Changing `kind` from 1 to 0
  disables one channel cleanly, with no per-frame cost and no risk of a partially-written matrix.
  Changing `dest` retargets a channel wholesale. Both are single writes to a stable record.
- **Regenerates itself:** the matrix at `target->dest` is fully derived — it is rewritten from the
  channel values every frame a channel group touches it. Writing it directly is pointless unless no
  animation drives it. The `flags` accumulator is per-group and local; it does not persist.
- **Breaks if:**
  - `m[3]`, `m[7]`, `m[11]`, `m[15]` are not pre-initialized to `0,0,0,1`. This function never
    writes them and a fresh allocation of garbage will produce a visibly broken transform.
  - A kind-1 `size` above `0x10` is expected to work. It cannot — the binder clamps it to 16 bytes,
    silently.
  - A channel's semantic pointer is set to a *copy* of a descriptor rather than the shipped
    instance. The comparison is pointer identity; a byte-identical copy at a different address will
    fall through to the generic dispatch and never compose a matrix.
- **Multiplayer / XIIOnline:** everything here is **local derived presentation state**. Bone
  matrices are recomputed on every client from that client's own animation evaluation. They are
  never authoritative and must never be replicated — the authoritative state is the animation
  selection and its time, upstream of this system. Replicating matrices would be both enormous and
  wrong.
- **Mod compatibility:** the dotted member paths in animation assets are authored data and are a
  legitimate thing for another mod to change. Because an unresolvable path fails silently, two mods
  that rename the same member do not crash — they produce a character that quietly stops moving one
  bone, which is far harder to diagnose. Prefer adding channels over renaming targets.

## 7. What is not known

- [x] ~~The name string of the 2-component channel semantic at `01F2CEB8`, and whether the semantic
      table ends there or continues.~~ **ANSWERED 2026-09-03, §10** — it is `ShaderParameterF2`, and
      the table continues to **nineteen** entries. **BM-1 closes.**
- [x] **UQ-277.** Whether any semantic beyond the three transform ones receives special handling elsewhere;
      only `005C72A0`'s treatment has been read.
      ***ANSWERED 2026-09-18 (FABLE) — no: beyond the transform three, no semantic receives special handling, and the two functions the 2026-09-14 sweep read as such are static-lifetime infrastructure.** Re-swept today for every rip-relative reference to the nineteen entries at their `0x18` stride *and* at their `+0x08` field: the referencing functions are `005C72A0` (the composer, the three), `005C6F20` (builds the list `{0x10, 0, &Rotation, &Scale, &Translation}`, the three again), the nineteen stride-`0x40` getters `00160BF0`–`00161070`, `005C5C80` and `005CB150` — and the last three are registration, not handling. Each getter registers its descriptor once: it takes the running count at `02CACF18`, writes it into the entry's `+0x14` as the registration index, stores `&entry` at `02CACF20[index]` and bumps the count (`00160DF0`, `00160E01`..`00160E16`). `005C5C80` is the static initialiser: nineteen constructor calls, then a name-compare walk of the list headed at `02CAFCD8` against the entry's name pointer (`005C5D8A`..`005C5DBF`) before linking. `005CB150` is the teardown: it frees the object at `02CAD030`, zeroes the count `02CACF1C`, unlinks `Rotation`, `Translation`, `Scale` and the four `ShaderParameterF*` from that list *inline*, walking nodes through their `+0x08` link and matching `node+8 == &entry+8` (`005CB1F7`..`005CB22B`, `005CB3CB`..`005CB40B`) — which is why the shipped table's `+0x08` is 0: it is the runtime link, not a dead field — and removes the other twelve through the helper `005BFED0(&entry)` (`005CB40F`..). So `005CB150` references **all nineteen**, the seven at `+0x08` (the earlier sweep matched only the entry's first byte and saw twelve), and the 7 / 12 split is a code-generation difference between inline-linked and helper-removed descriptors, not a runtime grouping. The composer's dispatch of non-transform channels by target kind (memcpy or setter) stays the only treatment they get. Static: the bodies and the two reference sweeps.*
- [x] **BM-3.** The remaining 16 bytes of the 40-byte `ChannelValue` slot (`+0x18`..`+0x27`), untouched by
      `005C72A0`.
      **Narrowed 2026-09-18 (FABLE), at the two holes the 2026-09-14 pass named.* (1) The running-pointer walk: every listed body that steps a non-stack register by `0x28` (`add` / `sub` / `lea +0x28`) and touches that register's `+0x20` or `+0x24` together with its `+0x10` — 82 functions image-wide — and none of them is the slot array: the in-region ones build other 40-byte records (`005C62C0` a `{vtable, 0, 0, -1}` header, `005C22B0` a `0x40`-byte node with self-links, `005C6F20` the three-semantic list), the rest are outside the animation layer. (2) The `n × 0x28` size idiom (`lea r, [r + r*4]` then `× 8`, since no `imul` by `0x28` exists): `005BFE70` copies `n` slots whole through the `memcpy` thunk `00861EBA` (`005BFE86`..`005BFE8E`) — so the last eight bytes *are* propagated by a copier that never interprets them — and the only `n × 0x28` allocation in the region, `005C35A0` through `0017D260`, initialises self-linked list nodes (`005C360C`..`005C3617`), a different record. The slot array itself is therefore allocated through a shared element-size path this sweep cannot see, and `+0x20`..`+0x27` still has a writer (the copy) but no reader that gives it meaning; the bytes stay open only as “padding or an unread field”.*
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5), from the measurements already on this page and the register (no new measurement):** the sixteen bytes are two bind-time values and an eight-byte tail nothing interprets.
      - `+0x18` is a `u16` from the binding record's `+0x02`, zero-extended.
      - `+0x1C` is a dword copied from the source entry's `+0x0C`.
      - Both are written by the bind-time writer `005BF290` (OPUS, 2026-09-14) and never read by the composer.
      - `+0x20`..`+0x27` are moved only by the whole-slot copier `005BFE70` (`memcpy` through `00861EBA`), which never interprets them. The OPUS ×40 index census, the running-pointer sweep and the `n × 0x28` size sweep find no reader.
      So the layout is complete. `+0x20`..`+0x27` are a propagated tail with no consumer in this build, whether padding or an unread field; which of the two is intent, and it is not claimed.
- [x] **`BM-4`** *(this box carried `UQ-278`, which the register marks SUPERSEDED as a duplicate — corrected 2026-09-22)*.
      ~~Which concrete FFXII systems bind animation channels to shader parameters, and to what
      material properties.~~ **ANSWERED 2026-09-22 (FABLE): none do.** Over all 35,984 shipped
      clusters there are **2 clusters and 4 channel targets**, both map assets, and every one names
      **`setVisibilityFromAnimation`** on a single node — not a material property. See the section
      above.
- [x] The full vtable layouts of `PAnimationTargetBlenderController` and
      `PAnimationBlenderController`, needed to say whether their slot 12s share a declaring base. **BM-5.**
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BM-5): they do not. Each class declares its
  own slot 12.* Read from the RTTI-named vtables:

  | slot | `PAnimationController` `00D314E0` | `PAnimationBlenderController` `00D315B0` | `PAnimationTargetBlenderController` `00D31768` |
  |---:|---|---|---|
  | 0 | `005ACB00` | `005AC9B0` | `005ACDE0` |
  | 1 | `005C5230` | `005C3A20` | `0053DD10` |
  | 2 | `005C5230` | `005C52B0` | `005C52E0` |
  | 3 | `005CB5A0` | `005CB4F0` | `005CB6A0` |
  | 4 | `005C5230` | `00861EC6` | `005C5230` |
  | 5 | `005C4D30` | `005C5230` | `005C5230` |
  | 6 | `005C5040` | `00861EC6` | `005C5230` |
  | 7 | `005C5230` | `005C5230` | `005C5230` |
  | 8 | `005C4F30` | `005C5230` | `005C5230` |
  | 9 | `005C6170` | `005C6170` | `005C6170` |
  | 10 | `005C6D90` | `00861EC6` | `005C5230` |
  | 11 | `005C5190` | `00861EC6` | `005C5230` |
  | 12 | — | **`005C9F30`** | **`005C72A0`** |

  - **The shared base ends at slot 11.** All three classes have the identical base chain `PAnimationDataSource` :
    `PAnimationHierarchyNode` : `PBase` : `PMemoryBase`. `PAnimationController`, which derives from that same chain, has
    **12 slots (0–11)**.
  - **Slot 12 is therefore not declared by any common base.** Each blender controller introduces its own, and the
    shared index 12 is a coincidence of both adding one virtual after the same base. That confirms reading `005C72A0`
    (channel apply) and `005C9F30` (array resize) as unrelated methods.
  - **Where the shared base shows.** Slot 9, `005C6170`, is common to all three.
- [x] Whether kinds 2 and 3 are ever produced by a binder other than `005C0820` — this document
      only read the kind-1 producer. **Sharpened by section 11:** `005C0820` writes the literal `1`
      and never touches `+0x18`/`+0x20`/`+0x28`, so a second producer must exist for the consumer's
      kind-2/3 arms to be reachable at all, and it has not been found.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BM-6): yes. The binder is a virtual family, and
  kinds 2 and 3 have their own producers.* `005C0820` is slot 1 of one subclass among four. Every subclass derives from
  `Phyre::PAnimation::PAnimationChannelTargetBind` (vtable `00D317D8`, slot 1 = `_purecall` `00861EC6`), and none of
  the binders has a direct caller; each is reached only through its vtable slot, which is why the earlier census saw
  one.

  | subclass (RTTI) | vtable | slot 1 | kind it writes |
  |---|---|---|---|
  | `PAnimationChannelTargetBindDataMember` | `00D317F0` | `005C0820` | **1** (`005C0AF4`) |
  | `PAnimationChannelTargetBindShaderParameter` | `00D31808` | `005C1160` | **1**, dest at `+0x08` (`005C1274`–`005C127A`) |
  | `PAnimationChannelTargetBindMethod` | `00D31838` | `005C0C90` | **2**, with `+0x20` and `+0x18` (`005C0DA1`–`005C0DAB`) |
  | `PAnimationChannelTargetBindFunction` | `00D31820` | `005C0B60` | **3**, with `+0x28` = the resolved function object (`005C0C43`–`005C0C49`) |

  - **The function binder** accepts only channels whose type byte is 4. It resolves the named function through
    `005A7AB0` and logs *"Bound function %s does not take a single const Vectormath::Aos::Vector4 * parameter…"*
    (`00D31EA0`) when the signature does not match.
  - **The method binder** logs its own diagnostic, `00D31F30`, beside its store.

  **So all three consumer arms have producers**, and the shader-parameter binder is a second kind-1 producer. It is the
  animation-to-material route `BM-4` asks about.
- [x] ~~**UQ-279.** The member-flag word at `member + 0x28`. Bit 1 forces the bound size to 8 (section 4); bit 6~~
      participates in a conjunct that is unreachable on the path it sits on. Neither bit's meaning
      has been read from the class-descriptor side.
      ***ANSWERED 2026-09-17 (FABLE): bit 1 marks a member whose storage is a pointer to the value, and bit 6 is set by nothing in this build.** The flags word is the fourth argument of the member constructor `PClassDataMember` `00632960`, stored at `member + 0x28` by its name-initialiser `00632FB0` (`00632FCF`); bit 0 makes that initialiser copy the name (length loop `00632FF0`, allocation `0017D260`, copy `00861EBA`, pointer to `+0x18` of the node at member `+0x08`, so member `+0x20` *(corrected 2026-10-02, OPUS: `00632998` passes `rcx = member+8`; member `+0x18` is the owning class, `005C0999`)*). Bit 1 is read by three descriptor walkers: `0063AD90` (`0063ADC4`) and `0063C910` (`0063CA2E`) descend into the member as an embedded instance of its type only when bit 1 is clear, and `0063C4A0` (`0063C4B9`) sends the same member address to the type descriptor's slot `0x28` when bit 1 is set and to slot `0x18` when it is not. The constructor itself raises bit 1 for the duration of the descriptor's registration call (slot `0x40`, `006329CB`..`006329F1`) when the array kind it is passed is 2, the dynamic array whose storage is a pointer. The census agrees: of the 682 construction sites in the descriptor builders, 484 pass an immediate flags word, and the values are `0x10` (207), `0x12` (79), `0x8` (123), `0xA` (39) and `0x2` (36); every bit-1 site names a pointer or reference member (`m_texture`, `m_dataBlock`, `m_parent`, `m_next`, `m_prev`, `m_animationSet`, `m_material`, `m_localToWorldMatrix`, `m_targetNode`, `m_unusedPointer`), every bit-1-clear site a value member (`m_elementCount`, `m_width`, `m_height`, `m_mass`, `m_radius`, `m_offset`, `m_flags`). So the binder's override reads: a pointer member binds as its 8-byte pointer, not as the pointee's size. The `0x8` and `0x10` families never mix inside one builder (32 builders use `0x8`, 95 use `0x10`), so that pair is a per-class property, not read further here. No site passes bit 6, and the four static member instances in `.data` (file offsets `0x1E0C550`, `0x1E0C600`, `0x1E0C660`, `0x1E0C6E0`, flags 0 or 2) do not carry it either, so the conjunct that tests it is dead on both counts. Static, constructor and reader bodies read, immediate census over every construction site.*
- [x] ~~**UQ-280.** Whether the virtual at the member's vtable slot 1 is pure. The size override's second
      disjunct is dead if it is, live if it is not, and `005C0820` calls it twice per iteration
      rather than reusing the result.~~ **Answered 2026-09-14 (FABLE): it is pure, and the second disjunct is dead.**
      - **The census.** Every `.rdata` vtable was walked through its RTTI complete-object locator. Every vtable whose
        class is a data member has one of two leaves in slot 1:
        - **`005C5230`** (`xor eax, eax / ret`): `PClassDataMember`, `PClassDataMemberEnum` and `PClassDataMemberDynamic`;
        - **`0016D680`** (`mov rax, rcx / ret`): every array member, meaning `PClassDataMemberArray`, `…ArrayFixedSize`, and each
          `PClassDataMemberPhyreArray<…>`, `PClassDataMemberPhyreSharray<…>` and `PClassDataMemberArrayDynamic<…>` instantiation
          (well over a hundred).
      - **So slot 1 is an *as-array* accessor.** It returns the member itself when the member is an array and null otherwise.
        That is why `005C0820` reads the array kind `+0x5C` only through its result. Both leaves are side-effect-free and
        ignore every argument, so the second call returns exactly what the first did.
      - **Not members.** The `PClassDataMemberDynamicType<…>` adaptors use different slot-1 bodies that take an argument
        (`0063BB60`, `00677A80`), and their interface's slot 1 is `_purecall`. They are type adaptors, not entries of a class's
        member list. This census does not show that one can never appear where `005C0820` looks.
- [x] ~~**UQ-281.** What member type kinds **5 and above** are, and why a member of such a kind is dropped~~
      silently while an out-of-range array index is logged.
      ***ANSWERED 2026-09-17 (FABLE): the kinds are the four array member classes, and no kind above 4 exists in this build, so the refusal is a range guard that never fires.** The field at `+0x5C` belongs to the array member object itself, the value slot 1 returns, not to a separate type object: the base constructor `PClassDataMemberArray` `00632A10` stores its sixth argument there (`00632A4D`) beside the element size at `+0x58` (`00632A5F`), and `PClassDataMemberArrayFixedSize` `00632A70` overwrites it with 1 (`00632AFD`) and adds the fixed element count at `+0x60` (`00632B16`). Every one of the 124 direct callers of `00632A10` passes an immediate, and there are only three: 2 from every `PClassDataMemberArrayDynamic<…>` instantiation (the `PArray`/`PSharray`-of-pointer dynamic arrays and the `PAnnotationWithValue` arrays), 3 from every `PClassDataMemberPhyreArray<…>` and 4 from every `PClassDataMemberPhyreSharray<…>`. So kind 1 is a fixed-size C array, 2 a dynamic array held through a pointer, 3 a `PArray` and 4 a `PSharray`; the binder's `dec eax; cmp eax, 3; ja` at `005C0A10`..`005C0A15` is the guard over that four-value enumeration, and since nothing constructs a fifth value the silent arm is unreachable, which is why it has no log line: it is the compiler's out-of-range fall-through, not a policy. All four kinds then take one path (`005C0A17`..`005C0A29`, count from slot `0x20`, index check, base plus index times element size). Static, constructor bodies read, immediate census over every call site.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `005C0820` is the animation channel binder, not generic reflection traversal | authored format string in its own body: `"Not binding %s:%s because array index (%d) exceeds array size (%d)\n"` | 2 |
| The three transform semantics are `Rotation`, `Translation`, `Scale` | strings read at `00D2B870`, `00D2B928`, `00D2B934`, reached from the descriptor pointers compared in `005C72A0` | 2 |
| Component counts 4 / 3 / 3 (and 4 / 3 / 2 for the next three) | raw read of `01F2CE40`..`01F2CEC0`, field `+0x10` | 1 |
| `1.0f` is the normalize numerator | raw read of `01CEBBA8` = `0000803F`; independently, a second decompile rendered the constant inline as `1.0` | 1 |
| Quaternion→matrix formula, scale row-scaling, translation row | complete exact-current body of `005C72A0`, decompiled twice independently (headless `DecompileAddressFileBounded` and the live MCP decompiler) with identical arithmetic | 1 |
| Target record `+0x00`/`+0x08`/`+0x10` and the 16-byte size clamp | complete exact-current bodies of `005C0820` (producer) and `005C72A0` (consumer), **both** storing and reading these three offsets; stride `0x30` confirmed from the producer's own `add rbx, 0x30` | 1 |
| Target record `+0x18`/`+0x20`/`+0x28` | **`005C72A0` only.** `005C0820` never writes them. Corrected by audit pass 1 (section 11) - the earlier row claimed producer/consumer agreement on all six offsets | 2 |
| Additive marks slot 0 unconditionally; weighted does not | complete exact-current bodies of `005C6020` and `005C61A0` | 1 |
| Class identity of each address | MSVC RTTI, restricted to the **unique-class** subset — every address here appears against exactly one class in `Tools/work/rtti/methods.tsv` | 4 |
| `005C9F30` is an array resize, not a second apply | complete exact-current body of `005C9F30` | 1 |

**Method note.** The RTTI class map was filtered to addresses that map to exactly one class before
any address was used. Of 4,265 unique-class methods image-wide, 60 are `Phyre::PAnimation`; the
heavily folded stubs (for example `005C5230`, which appears against `GameApplication` and eight
different `PAnimation` classes at nine different slots) were excluded by construction and no claim
here rests on one. This is open question **BA-1**.

**Superseded readings:** ~~none — this is the document's first version.~~ *(Corrected 2026-09-30, SWE2-DATA: three readings on this page are superseded. §10 and §11 list what the falsification and audit passes overturned. The §1 claim that animations keep shader effects in sync was superseded by `BM-4`. The `BM-2` section's "yes, in three other places" was superseded by `UQ-277`: two of the three are registration and teardown.)*

## 9. Related

- [`../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) — the class-descriptor system the binder walks
- [`../Subsystem-Map/phyre-subsystem-map.md`](../Subsystem-Map/phyre-subsystem-map.md) — `PAnimation` is 190 of its 1,604 classes; this document is the first to read `PAnimation` bodies
- [`../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) — the address→class→slot index these addresses were drawn from
- [`../../17-Presentation-Rendering/Character-Rendering/character-render-object.md`](../../17-Presentation-Rendering/Character-Rendering/character-render-object.md) — downstream consumer of the composed bone matrices
- [`../../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md) — moves the actor; this system poses it. Distinct mechanisms that both end in a transform.

## `BM-4` answered from the shipped corpus — none, and the two that exist set VISIBILITY (FABLE, 2026-09-22)

§2 established what the engine's semantic table *can* drive — light colour, camera FOV, morph
weight, user attributes, shader parameters. `BM-4` asks what the **shipped game** actually binds.
**Measured over all 35,984 `.phyre` clusters:**

| | |
|---|--:|
| clusters holding a `PAnimationChannelTarget` | **2** |
| channel targets in the whole corpus | **4** |
| of those, targeting a **shader parameter** | **0** |
| `PEffect` *(control, same pass)* | 2,184 |

The two are **map assets**: `map/bds01/bds0109/bds0109.dae.phyre` and
`map/gil01/gil0102/gil0102.dae.phyre`, two targets each.

### What they name (FABLE, 2026-09-22)

Each cluster's channel-target instance list carries a 26-byte object block and a 46-byte data
region, and that region holds **exactly two strings**:

| cluster | strings |
|---|---|
| `bds0109` | `nodename1608`, **`setVisibilityFromAnimation`** |
| `gil0102` | `nodename118`, **`setVisibilityFromAnimation`** |

**So the one property FFXII drives through this binder is `setVisibilityFromAnimation` — a
visibility setter on a single named node, in each of two maps.** *The setter name is byte-identical
in both, and the only thing that differs is which node it is applied to.*

> **That answers `BM-4` by refusing its framing, which is the honest result.** The question asks
> *“which concrete FFXII systems bind animation channels to **shader parameters**, and to which
> **material properties**”*. **None do.** The mechanism reaches arbitrary reflected properties
> through kinds 2/3 and §2's table is genuinely much larger than a shader parameter — but the
> shipped authored data uses it **four times in total**, always for visibility, never for a
> material.

> **Scope of the claim, stated exactly.** This is the `PAnimationChannelTarget` population of the
> **Phyre cluster corpus**. A binding constructed natively at run time, or carried in one of
> FFXII's own non-Phyre formats, would not appear here. What is measured is that the *authored*
> route — the one §4's descriptor documents — carries no material binding anywhere in the shipped
> game.

## 10. Falsification pass 1 — 2026-09-03, session `repos-9e`

**The first deliberate attempt to destroy this document**, by a session that did not write it,
against the GN158 checkpoint. **Three claims overturned, six survived, and one open question closed
by the attack rather than by a separate pass.**

Every number in §3 is exact. What failed is a **boundary**: the document read six entries of a
nineteen-entry table and described the six as the table.

### Overturned

**1. The semantic table has nineteen entries, not six.** §4 states *"Shipped table, contiguous at
`0x01F2CE40`, stride `0x18`"* and lists six rows. Walking the stride from that base until the
name-pointer pattern breaks:

| # | address | name | components |
|---:|---|---|---:|
| 1–3 | `01F2CE40`/`58`/`70` | `Rotation`, `Translation`, `Scale` | 4, 3, 3 |
| 4–7 | `01F2CE88`…`01F2CED0` | `ShaderParameterF4`, `F3`, **`F2`**, **`F1`** | 4, 3, 2, 1 |
| 8–10 | `01F2CEE8`…`01F2CF18` | **`LightColor`**, **`LightIntensity`**, **`LightFalloffAndPenumbra`** | 4, 1, 2 |
| 11–14 | `01F2CF30`…`01F2CF78` | **`CameraFov`**, **`CameraZNear`**, **`CameraZFar`**, **`CameraOrthographicSize`** | 1, 1, 1, 1 |
| 15 | `01F2CF90` | **`MorphTargetWeight`** | 1 |
| 16–19 | `01F2CFA8`…`01F2CFF0` | **`UserAttributeBool`**, **`Int`**, **`Float`**, **`Vector`** | 1, 1, 1, 1 |

The run ends at `01F2D008`, where the name pointer is `0`. **All nineteen are referenced from
`.text`** — two to five sites each — so none is a vestigial table entry.

**2. `BM-1` is closed, and the document's own component count was right.** §7 asks for *"the name
string of the 2-component channel semantic at `01F2CEB8`, and whether the semantic table ends
there"*. It is **`ShaderParameterF2`**, and the table does not end there. The count of 2 the document
had already recorded is correct, which is a small point in the reading's favour: it measured the
field it could reach and did not guess the one it could not.

**3. §1 and §2 understate what an animation can drive, and this is a player-facing claim.** §1 says
the second visible consequence is that *"an animation can drive things that are not bones at
all — a number inside a material, a shader parameter"*, and §2 gives *"a shader parameter, say"* as
the example of a non-transform semantic. The table says the non-transform set also includes:

- **light colour, intensity, and falloff/penumbra**
- **camera field of view, near plane, far plane, and orthographic size**
- **morph target weight** — the channel type that drives facial expression
- **four user-attribute types**, including a bool and a vector

So a single animation file can pull the camera's FOV, dim a light and change a face, in the same
bundle of curves that moves the skeleton, and they stay in sync for the reason §1 already gives —
**they are channels in the same animation, not separate timed effects.** That is a stronger and more
useful version of the paragraph the document already has; the mechanism section was right and its
example was the narrowest one available.

### Survived — attacked and not broken

| Claim | How attacked | Result |
|---|---|---|
| the five §3 body sizes: 1674 / 827 / 323 / 288 / 61 | re-derived from the certified function list | **all five exact** |
| descriptor layout `+0x00` name, `+0x08` zero, `+0x10` componentCount | unpacked across **all nineteen** entries, not the six cited | **holds for all nineteen**; `+0x08` and `+0x14` are zero throughout |
| the array-index refusal string | byte search | **exact** at `00D31E50`, including a trailing `\n` the quote omits |
| `01CEBBA8` is `1.0f` | read from `.rdata` | **exact** — and independently cited as the same constant by [glyph-run rendering](../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md), two documents agreeing from unrelated directions |
| §2: the composer classifies by *"a pointer compare against three known globals"* | every RIP-relative `LEA` inside `005C72A0`'s 1,674 bytes decoded | **exactly six sites, two each, to `Rotation`/`Translation`/`Scale` and nothing else** |
| §2: *"exactly one descriptor object per semantic in the whole image"* | see below | **holds** |

**The uniqueness test is worth recording because my first one was unfit.** Counting occurrences of
the name bytes gives `Rotation` 2, `Translation` 2 — and **`Scale` 5,167**, because "Scale" is a
common English substring and appears all over the image in unrelated strings. That instrument cannot
answer the question at all.

The right test uses the pointer, not the text: read each descriptor's own name pointer, then find
every 8-byte-aligned qword in the image equal to it. A second descriptor object would have to hold
the same pointer.

```
Rotation     name ptr 00D2B870  ->  1 slot: 01F2CE40 [.data]
Translation  name ptr 00D2B928  ->  1 slot: 01F2CE58 [.data]
Scale        name ptr 00D2B934  ->  1 slot: 01F2CE70 [.data]
```

**One slot each, image-wide.** The claim holds, and it holds on evidence that could have refuted it.

### What this pass did not test

- **§4's formulas** — quaternion normalize, quaternion→matrix, the scale and translation paths, and
  the `flags & 3` / `flags & 4` dispatch. Read for structure only; no constant re-derived from a body.
- **The binder `005C0820`'s path walk** and its four binding kinds.
- **The two `MarkContributedSlots` variants** and the additive-vs-weighted rule.
- **`005A7E90`'s virtual dispatch** and the vtable-layout question in §7.
- The remaining `ChannelValue` bytes `+0x18`..`+0x27`, ~~still open~~ *(answered since: `BM-3`, 2026-09-26; SWE2-DATA 2026-09-30)*.

### The killer observations, named

- *The table claim would be false if the stride pattern continued past the sixth entry.* It does —
  for thirteen more entries, every one code-referenced.
- *The three-way pointer compare would be false if the composer referenced a fourth descriptor.* Every
  `LEA` in its body was decoded; it does not.
- *The uniqueness claim would be false if any second slot held a descriptor's name pointer.* None does
  — but only the pointer test can say so, and the name-string test that looks equivalent cannot.

## 11. Audit pass 1 - 2026-09-13 (OPUS)

*(Static only - complete exact-current bodies of `005C0820`, `005C6020`, `005C61A0` and `005A7E90`
disassembled from the shipping EXE. Nothing executed and no animation played.)*

**This pass deliberately took the half that pass 1 did not.** Section 10 closes with a list of what
it left untested: section 4's formulas, *"the binder `005C0820`'s path walk and its four binding
kinds"*, *"the two `MarkContributedSlots` variants"*, and *"`005A7E90`'s virtual dispatch"*. Those
are the four bodies read here. The semantic table, the six-`lea` census and the descriptor
uniqueness test are **not re-derived** - they were settled on 2026-09-03 and re-running them would
test the earlier pass, not this one.

### The binder reproduces exactly, field for field

Every offset section 4 asserts about `005C0820` was re-derived blind from the disassembly, and
**every one is exact**:

| section 4 claim | instruction |
|---|---|
| descriptor kind must be 2 (`descriptor + 0x20`) | `cmp dword ptr [r13 - 8], 2` at `005C0883` |
| owner chain walked via `+0x78` | `mov rax, [rax + 0x78]` at `005C08A5` |
| fallback object at `descriptor + 0x08` | `mov rbp, [r13 - 0x20]` at `005C08C5` |
| path at `descriptor + 0x28`, MSVC short-string low-bit | `movzx eax, byte [r13]; and eax, 1; mov rsi, [r13]; sub rsi, rax` |
| split on `'.'` | `mov edx, 0x2e` at `005C0919`, then the imported `strchr` |
| `offset += member[9] - *(int *)(member[3] + 0xF4)` | `mov ecx, [r14 + 0x48]; mov rax, [r14 + 0x18]; sub ecx, [rax + 0xF4]` - and **twice**, once per branch |
| `arrayIndex` at `descriptor + 0x30` | `mov ebp, [r13 + 8]` at `005C0A17` |
| refuse when `arrayIndex >= arraySize` | `cmp ebp, eax; jae` at `005C0A29` |
| `elementSize = *(u32 *)(arrayType + 0x38)` | `mov ebx, [rax + 0x38]` at `005C0A36` |
| the clamp `if (0x10 < size) size = 0x10` | `cmp ebx, 0x10; mov ecx, 0x10; cmova ebx, ecx` at `005C0AFE` |
| descriptor stride 56 / target stride 48 | `add r13, 0x38` / `add rbx, 0x30` at `005C0B19` |

**The format string is there, and my first instrument said it was not.** A `lea`-reachable,
eight-character-minimum scan over the body returned nothing, and I nearly wrote that section 8's
tier-2 identity evidence was unsupported. A byte search finds it at **`00D31E50`**, reached by
**exactly one** `lea` image-wide, at **`005C0A7C`** - inside this body. The filter, not the page,
was wrong. This is the third time this session that a reference scan has produced a confident zero
(EVIDENCE-STANDARD 2026-09-13c/d); **a zero from a reference scan is a result about the scan until
a second instrument agrees.**

The call that consumes it is `Log(2, fmt, ownerName, path, index, size)` - `ecx = 2` is a
severity or channel selector, `r8` is `*(ptr *)(*(ptr *)(anim + 8) + 0x30)`, and `r9` is the dotted
path. So the two `%s` are **the owner's name and the failing path**, which the page quotes the
string for without ever saying what fills it.

### Three things the page did not have

1. **`005A7E90` is variadic** (section 4, rewritten). The prologue spills `rdx`/`r8`/`r9` to their
   home slots and builds a `va_list` at `&home(arg3)`; the fifth, stack-passed argument is a
   **pointer to that list**, not `&value`. The rendering `(handler, context, 0, 0, &valuePtr)` is
   the right *shape* and hides a level of indirection and the whole variadic signature. The two
   zeros are the callee's own fixed parameters.
2. **A size override to 8** (section 4, new). The bound size is forced to 8 - a pointer, not the
   pointee - when member-flag bit 1 is set. Its second disjunct tests a type kind that **cannot be
   2 on the branch it sits on**, because the branch is entered only when that same field read 0;
   the compiler re-issued the virtual rather than reusing the result, so it did not treat the call
   as pure. Recorded as dead-unless-impure, with the purity question opened in section 7.
3. **The member type kinds and the silent refusal** (section 4, new). `+0x5C` routes the member:
   0 is scalar, **1 through 4** all take the bounds-checked array path, and **5 and above abandon
   the binding with no log line at all**. Section 2's *"if the resolved member is an array"* covers
   four kinds, not one, and misses a third outcome entirely.

### Corrected: a producer/consumer agreement that does not exist

Section 8 claimed the target-record layout rests on *"complete exact-current bodies of `005C0820`
(producer) and `005C72A0` (consumer) **agreeing on offsets** `0x00/0x08/0x10/0x18/0x20/0x28`"*.
**The producer writes three of those six.** It stores `+0x00` (the literal `1`), `+0x08` and
`+0x10`, and nothing else; `+0x18`, `+0x20` and `+0x28` are read off the consumer alone.

That is not a small bookkeeping fix. It means *(answered: see BM-6, 2026-09-14 - the binder is a virtual family; 2026-10-02, OPUS)* **no code in this document produces a kind-2 or
kind-3 record**, so the consumer's setter arms - and `005A7E90` with them - are reached by a
producer nobody has found. Section 7 already asked the question; it was filed as a caution and is
now a measurement. Both section 4 and section 8 now mark which offsets are producer-confirmed and
which are consumer-only.

### The two blenders survive, exactly as written

| section 4 claim | measured |
|---|---|
| weight array at `controller + 0x30` | `mov rax, [r11 + 0x30]` - and **re-loaded every iteration**, never hoisted |
| WEIGHTED: mark only where `weight[i] != 0.0f` | `ucomiss xmm0, xmm1; jp/je` with `xmm1` zeroed by `xorps` - the `jp` arm makes NaN mark, which is what `!= 0.0f` means in C |
| ADDITIVE: `mark[slot[0]] = 1` unconditionally, then loop from 1 | `mov eax, [r8]; mov byte ptr [rax + rdx], 1` at `005C6041` - **the weight array is not read for element 0**, then `cmp r9d, edi` with `edi = 1` |
| both unrolled x4 with a scalar remainder | both: a four-body loop plus a one-at-a-time tail |
| the unconditional first write is the whole difference | the two bodies are otherwise the same shape; 323 - 288 = 35 bytes, which is that write, the `count != 0` guard and the `edi = 1` start |

**Not claimed and not measured.** The return value (`0` normally, `1` on the null-argument
early-out) is recorded here and nowhere else; section 4's **quaternion normalize, quaternion-to-matrix,
scale and translation formulas are ~~still unverified~~** *(verified since by audit pass 2, §12: every formula in section 4 is exact; SWE2-DATA 2026-09-30)* - this pass read the binder and the blenders,
not the composer's arithmetic, and section 10 did not read them either, so the formulas remain the
largest untested block on the page. The `ChannelValue` bytes `+0x18`..`+0x27` stay unread *(answered: see BM-3, ANSWERED 2026-09-26; 2026-10-02, OPUS)*. Nothing
was executed.

**Snapshot note.** This page's `verified_against` names the **GN158** checkpoint
(`gzf 2ed8aff...`, `snapshot 46f02e2...`) while the current export is GN160. The `exe_sha256` is
unchanged, and this pass read **only** the EXE and the GN160 `functions.tsv`, so nothing here
depends on the stale pair - but the frontmatter still describes the body against an older
checkpoint and that is left visible rather than silently bumped.

## 12. Audit pass 2 - 2026-09-13 (OPUS): the composer's arithmetic

*(Static only - the complete exact-current body of `005C72A0` disassembled and the SSE dataflow
traced register by register. Nothing executed and no animation played.)*

**This is the block both earlier passes named as untested.** Pass 1 (`repos-9e`) wrote *"section 4's
formulas ... read for structure only; no constant re-derived from a body"*, and audit pass 1 said
the formulas *"remain the largest untested block on the page"*. They are now derived from the body.

### Every formula in section 4 is exact

| section 4 claim | result |
|---|---|
| `s = 1.0f / sqrtf(x*x + y*y + z*z + w*w)` | **exact** - `005C745E`-`005C749F`, see the note below |
| quaternion to matrix, `flags & 3 == 1` | **exact**, arm at `005C7752` |
| scale only, `flags & 3 == 2`, off-diagonals explicitly zeroed | **exact**, arm at `005C7720` |
| rotation and scale, `flags & 3 == 3` | **exact, all nine terms**, arm at `005C75E4` |
| translation, `flags & 4` | **exact** - `005C7852`-`005C785C` to `+0x30`/`+0x34`/`+0x38` |
| `m[3]`, `m[7]`, `m[11]`, `m[15]` are never written | **exact** - no store to `+0x0C`, `+0x1C`, `+0x2C` or `+0x3C` anywhere in the body |

The `flags & 3 == 3` arm was traced term by term, since it is the one that carries both the
rotation basis and the row scaling:

```
xmm12 = 1 - 2Y*Y - 2Z*Z     xmm10 = 2X*Y + 2W*Z     xmm11 = 2X*Z - 2W*Y
xmm13 = 2X*Y - 2W*Z         xmm1  = 1 - 2X*X - 2Z*Z xmm2  = 2Y*Z + 2W*X
xmm3  = 2X*Z + 2W*Y         xmm9  = 2Y*Z - 2W*X     xmm0  = 1 - 2X*X - 2Y*Y
```

each multiplied by `Sx`/`Sy`/`Sz` from `[rsp+0x148]`, `[rsp+0x138]` and `[rsp+0x28]` for its row,
then stored to `+0x00/04/08`, `+0x10/14/18`, `+0x20/24/28`. **That is section 4's table, with the
scale applied per row in the rotated frame, reproduced without reading it first.**

### The arm dispatch, which section 4 states as a `switch`

`005C75C6`-`005C75DE`: `and ecx, 3`, then `sub`/`sub`/`cmp` - so **`1` jumps to `005C7752`,
`2` to `005C7720`, `3` falls through to `005C75E4`, and `0` skips to the translation test at
`005C783A`**. The `case 0: neither - basis left untouched` in section 4 is not a written branch at
all; it is the fall-out of three failed comparisons, which is why nothing is written.

> **A control that could have failed and did not.** `xmm10` holds `1.0f` across the loop, and two
> of the three arms clobber it - the `== 3` arm at `005C7656`, the `== 1` arm at `005C7769`. Both
> reach `005C7831`, which reloads it from `01CEBBA8`. The `== 2` arm never touches `xmm10` and
> jumps **past** that reload to `005C783A`. Three arms, two restores, and the one that skips the
> restore is the one with nothing to restore.

### `01CEBBA8` has two jobs, not one

Section 3's data table calls it *"the reciprocal numerator in the quaternion normalize"*. It is
**also the `1` in every `1 - 2Y*Y - 2Z*Z` diagonal term**, and it is read at **four** sites:
`005C7390` (into `xmm10`), `005C7640` (the `== 3` arm), `005C7799` (the `== 1` arm) and `005C7831`
(the restore). One constant, two roles. The description is not wrong; it is half.

### The non-transform dispatch reproduces, and it closes a loop from audit pass 1

`005C7509`-`005C7552`, keyed on `[rbx]` - the target record's `kind`:

```
kind 1 -> memcpy(target->dest, &value, target->size)        005C7545, call 00861EBA
kind 2 -> 005A7E90(obj @ +0x28 ... ctx @ +0x18)             005C7531   <- corrected 2026-10-02, OPUS - kind 2's object is +0x20 (005C753A mov rcx, [rbx+0x20]); +0x28 is kind 3's (005C751F)
kind 3 -> 005A7E90(obj @ +0x28, 0)                          005C751F
```

Audit pass 1 showed the binder writes **only** kind 1. Here is the consumer reading kinds 2 and 3
and calling the variadic setter for them. **Both halves are now measured, and they still do not
meet**: nothing found produces the records these two arms consume. Section 7's open item stands and
is now bounded on both sides.

### The instrument failed again, in the same way, and it reaches off this page

**A mnemonic scan for `sqrt*` over the whole 1,674-byte body returns ZERO.** The square root is
`005C7481 call 0x861F14`, and `00861F14` is a **six-byte import thunk named `sqrtf`**. Section 4's
formula is exactly right and my first instrument said the operation was absent.

That is the fourth confident zero from a reference or mnemonic scan this session
(EVIDENCE-STANDARD 2026-09-13c/d, and the `005C0820` format string in audit pass 1). **An
instruction census cannot see an operation implemented as a call**, and this one is a one-line
thunk that a disassembly-level filter will never match.

> **It also weakens an implication I drew elsewhere, and that page has been corrected.** In
> [the spatial audio object model](../../18-Audio/the-spatial-audio-object-model.md) section 8 I
> reported that `sqrtps` occurs 14 times in exactly six functions, **all** inside the audio
> cluster. That count is still true *of `sqrtps`*. The reading it invited - that packed square root
> belongs to the audio system - does **not** extend to square roots generally: this function takes
> one every time it normalizes a quaternion, through `sqrtf`, and it is animation middleware.
> **A census of one instruction is a claim about that instruction, not about the operation it
> implements.**

**Not claimed.** The `ChannelValue` bytes `+0x18`..`+0x27` stay unread *(answered: see BM-3, ANSWERED 2026-09-26; 2026-10-02, OPUS)*. The `== 1` arm was verified
structurally and on its `m[0]` term rather than all nine, since it is the `== 3` arm with the scale
multiplies removed. Nothing was executed.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**UI — CLIENT.** `FUN_003c80c0`, owned by that layer, calls `0053DD10` on this page. That caller is a 230-byte lazy creator: when `[02B476B0]` is empty it makes a **`0xC8`-byte** object around the `.text` callback `003C5910` and caches it there; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
- **CoreRuntimeScheduling - CLIENT (1 edge).** InputDevice_QueryAvailabilityState_Always1 (`0053DD10`) is called by bodies filed to CoreRuntimeScheduling: `0022B6E0` - shared machinery across the layer boundary, no shared ownership.
- **Input - MECHANICAL (4 edges).** Fan-in on the shared accessor InputDevice_QueryAvailabilityState_Always1 (`0053DD10`). All 4 edges run through it - one accessor’s spread, not a per-caller relationship.
- **Presentation - CLIENT and SERVICE (9 edges).** `0016D680`, InputDevice_QueryAvailabilityState_Always1 (`0053DD10`) are called by bodies filed to Presentation: `00183A00`, `00183C60`, `00183EE0`, Renderer_CreateRandomNoiseTextureFromGraphicsMT19937 (`001946E0`) (+4 more); `0063C910` reaches bodies filed to Presentation: `00639A60` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - MECHANICAL (17 edges).** Fan-in on the shared accessor InputDevice_QueryAvailabilityState_Always1 (`0053DD10`). All 17 edges run through it - one accessor’s spread, not a per-caller relationship.
- **WorldAreaField - CLIENT and SERVICE (2 edges).** InputDevice_QueryAvailabilityState_Always1 (`0053DD10`) is called by bodies filed to WorldAreaField: `003789A0`; `003C80C0` reaches bodies filed to WorldAreaField: WorldTransition_GetActiveOrPendingFieldId (`003148F0`) - shared machinery across the layer boundary, no shared ownership.
- **ActorEntity - MECHANICAL (2 edges).** both edges are actor bodies (`ActorManager_RunFieldRuntimePass` `0025D9E0`, `BattleSlotMap_InitializeMappingClasses` `00329CC0`) calling `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) - accessor fan-in.
- **Audio - MECHANICAL (1 edge).** `00261F90` calls `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) - accessor fan-in.
- **CombatAction - MECHANICAL (2 edges).** both edges are action bodies (`BattleUnit_TryTriggerNearbyAuthoredFieldAction` `002F8060`, `002FA740`) calling `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) - accessor fan-in.
- **Movement - MECHANICAL (3 edges).** all 3 edges are movement bodies (`0033A720`, `003ED190`, `003ED3F0`) calling `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) - accessor fan-in.
- **PlatformOnlineAchievements - MECHANICAL (1 edge).** `003160C0` calls `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) - accessor fan-in.
- **Save_Load_Settings - CLIENT and SERVICE (3 edges).** `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) calls `003148F0`, while `0022B6E0`/`003148F0` reach `SaveRuntime_ResetActiveImageAndRebindState` (`002EF650`) and `SaveImage_GetPersistentPayloadBase` (`002EF2B0`).
- **Spawn_Encounter_Lifecycle - MECHANICAL (1 edge).** `SpawnKeep_RotatePersistenceBanksForAreaTransition` (`00233780`) calls `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) - accessor fan-in.
- **Gameplay - CLIENT and SERVICE (5 edges).** `BattleSystem_ResetRuntimeState` (`00237DF0`) calls `BattleSlotMap_InitializeMappingClasses` (`00329CC0`), while `0025D9E0`/`00329CC0` reach `00234150`, `DefinitionRuntime_ActivateAndApplyConfig` (`00316DF0`), `BattleEncodedId_IsValidForClass` (`00322C50`) and `DefinitionRuntime_DeactivateAndRemoveConfig` (`00323540`).
- **Party - SERVICE (3 edges).** `ActorManager_RunFieldRuntimePass` (`0025D9E0`) reaches `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`), `00329CC0` reaches `PartyFocus_SelectAndRequestDefaultActor` (`00326500`), and `00583D60` reaches `PartyFocus_GetPreferredDefinitionSelector` (`003271D0`).
- **RNG_Random_Selection - SERVICE (4 edges).** `001946E0` twists `GraphicsNoiseMT19937_TwistState` (`0018EE20`); `0022B6E0`, `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (`002F8060`) and `002FA740` all reach `RNG_MT19937_NextU32_Thunk` (`00379CD0`).
- **Status_Periodic_Terminal - CLIENT (1 edge).** `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`) calls `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (`002F8060`).
- **Story_Event_Quest_Hunt - MECHANICAL (15 edges).** all 15 edges are persistent-flag bodies (`PersistentFlag_Query*`/`PersistentFlag_Set*`, the `0032A8A0`-`0032AD60` block) calling `SaveImage_GetPersistentPayloadBase` (`002EF2B0`) - fan-in on the payload-base accessor.
- **CombatAI - MECHANICAL and SERVICE (11 edges).** ten combat-AI/enmity bodies (`AiOrder_EvaluateTargetSelector` `00301AD0`, `BattleEnmity_*` `003215B0`-`00321D30` block) call `BattleEncodedId_IsValidForClass` (`00322C50`) - fan-in on the validity query; `00310DB0` also reaches `BattleEnmity_UpdatePeriodicDecay` (`00321530`).
- **CombatFormula - MECHANICAL and SERVICE (60 edges).** fifty-three edges are combat-formula bodies calling `RNG_MT19937_NextU32_Thunk` (`00379CD0`) - fan-in on the shared RNG thunk; `00310DB0` reaches `BattleStats_ModifyPrimaryResource`/`BattleFormula_*`/`BattleStats_Get*` (`00300CE0`, `003112F0`, `0031E800`, `00320AB0`, `00385F60`), `00237DF0` reaches `BattleStats_InitializeDefinitionRecord` (`0023AC80`).
- **Items_Equipment_Shops_License - MECHANICAL and SERVICE (18 edges).** thirteen item-layer bodies call `BattleEncodedId_IsValidForClass` (`00322C50`) - fan-in on the validity query; `00237DF0` reaches `Inventory_InitializePrimaryStateFromAuthoredTable` (`0023AF50`), `00316DF0` reaches `Inventory_GrantEncodedLootItem` (`00300B80`) and `EquipmentInventory_IncrementSecondaryCountChannel` (`0030BD00`), `00323540` reaches two more.
- **Rewards_Progression_Economy - SERVICE and MECHANICAL (8 edges).** `00310DB0` reaches the loot pool (`002FB150`, `00319830`, `00319A00`) and `00316DF0` reaches `GameState_AddGilClampedAndNotify` (`0030C470` block); two reward-side bodies call `RNG_MT19937_NextU32_Thunk` (`00379CD0`) - accessor fan-in.

## `BM-3` — `+0x18` and `+0x1C` read, and the writer found (OPUS, 2026-09-14)

The page has said three times that the `ChannelValue` bytes `+0x18`..`+0x27` *"stay unread"*, on the
strength of the composer: `005C72A0` takes the four floats and the semantic pointer and nothing else.
**The composer is not the writer.** Read from the shipping image at the authority hash
`73461D08…9721F8`.

### Finding the writer, and the control that says the search was complete

`005C72A0` reaches a slot with the ×40 idiom — `lea rax, [rcx + rcx*4]` then `[r12 + rax*8]`, with
`r12 = qword [arg3]`. Sweeping every listed body for that idiom finds **146 functions**, of which
**51 touch a displacement in `+0x18`..`+0x27`** of some 40-byte array.

**Control: not one function in the image contains an `imul r, 0x28`.** The multiply form is the only
other way to index a 40-byte array, and it is empty — so the sweep covers the indexed population
completely. What it cannot see is a running-pointer walk (`add r, 0x28`), and that hole is named here
rather than left implicit.

Exactly one of the 51 sits in this layer: **`005BF290`**, two functions below the binder.

### What it writes

```
005BF370  movsx  eax, word  [rbx]               ; a SIGNED u16 channel id, from a binding record
005BF373  sub    eax, dword [r12 + 0x0C]        ; minus a base index
005BF378  cmp    eax, dword [r12 + 0x08]        ; bounds-checked against a count
005BF37D  jae    skip                           ; out of range -> this channel is skipped
005BF37F  mov    rdx, qword [r12]               ; the source channel table
005BF383  lea    r10, [rax + rax*4]             ; x5 -> x8 = stride 40  (ChannelValue)
005BF387  movzx  ecx, word  [rbx + 2]           ; an UNSIGNED u16, same binding record
005BF38B  lea    r8,  [rax + rax*2]             ; x3 -> x8 = stride 24  (source entry)
005BF38F  mov    rax, qword [rdx + r8*8]        ; source +0x00 : the semantic pointer
005BF393  mov    r9d, dword [rdx + r8*8 + 0xC]  ; source +0x0C : a dword
005BF398  mov    qword [r15 + r10*8 + 0x10], rax ; -> ChannelValue +0x10
005BF39D  mov    dword [r15 + r10*8 + 0x18], ecx ; -> ChannelValue +0x18
005BF3A2  mov    dword [r15 + r10*8 + 0x1C], r9d ; -> ChannelValue +0x1C
005BF3AC  movups [r15 + r10*8], xmm0             ; -> ChannelValue +0x00..+0x0F
```

| slot byte | what is written | from |
|---|---|---|
| `+0x00`..`+0x0F` | the four floats | a 16-byte load, source stride `0x58` |
| `+0x10` | the semantic pointer | source entry `+0x00` (stride 24) |
| **`+0x18`** | **a `u16` zero-extended to a dword** | the binding record's `+0x02` |
| **`+0x1C`** | **a dword copied straight through** | source entry `+0x0C` |

**So `+0x18` and `+0x1C` are two dwords written at bind time and never read by the composer.** The
slot is written by one function and consumed by another that ignores half of what the first wrote.

### `+0x20`..`+0x27` — a bounded negative

`005BF290`'s ×40-indexed accesses are `+0x00`, `+0x0C`, `+0x10`, `+0x18`, `+0x1C` and **nothing at
`+0x20` or above**; the composer reads `+0x00` and `+0x10`. So **no known toucher of this array
touches the last eight bytes**, which is consistent with padding to a 40-byte stride and is not proof
of it: the sweep is blind to a running-pointer walk, and a third function reaching the array by a
pointer it was handed would not appear.

### One thing worth noticing about the writer

`005BF290` carries the GFZ tag `Runtime.FunctionAddressReferencedFromCode` — a **shape** class, not a
semantic one. It is plainly the channel binder's inner loop, and it is one of the ~11,800 bodies
`B-1` counts as *"accounted for in the ledger but with no semantic identity"*. Here is one of them,
with an identity, found by chasing a field rather than a name.

*(Read by OPUS 2026-09-14. `BM-3` is answered for `+0x18` and `+0x1C` and bounded for
`+0x20`..`+0x27`; ~~it stays open on those eight bytes.~~)* *(Answered since: `BM-3` 2026-09-26 records the eight bytes as a propagated tail with no reader. SWE2-DATA, 2026-09-30.)*

## `BM-2` — yes, and there are three other places (OPUS, 2026-09-14)

`BM-2` asks whether any semantic beyond `Rotation` / `Translation` / `Scale` gets special handling
elsewhere, and records that *"only `005C72A0`'s treatment has been read"*. The table is contiguous at
`01F2CE40`, stride `0x18`, nineteen entries — so every direct reference to it is findable. Swept
across every listed body from the shipping image at the authority hash `73461D08…9721F8`:

**Twenty-three functions reference a `ChannelSemantic` entry directly.** They fall into four groups
and none of them was on this page.

### 1. Nineteen one-per-semantic accessors, `00160BF0`–`00161070`

Stride `0x40`, 54 bytes each, each `lea`-ing **exactly one** semantic and no other. Tagged
`Runtime.StaticLifetimeInfrastructure`. One generated getter per semantic — which is the opposite of
special handling and worth stating, because it is nineteen of the twenty-three hits.

### 2. `005C6F20` — a second place that names exactly the three

252 bytes, tagged `NativeInline.BoundedLoop.NoComputedTransfer`. It builds a descriptor:

```
005C6F53  mov qword [r8],        0x10
005C6F5F  mov qword [r8 + 0x08], 0            ; rsi, zeroed above
005C6F63  mov qword [r8 + 0x10], r14          ; &Rotation
005C6F67  mov qword [r8 + 0x18], r15          ; &Scale
005C6F73  mov qword [r8 + 0x20], r12          ; &Translation
```

**Rotation, Scale, Translation — the same three the composer special-cases, named again, in a
different function, as a list rather than as a dispatch.** It then sizes a buffer from
`dword [rax+0x20]` with the `btr …, 0x1F` inline-or-heap discriminator.

### 3. `005CB150` — the complement, handled as a group

914 bytes, `Phyre.Middleware.RealVtableFunctionMember`. It references **the other twelve** —
`LightColor`, `LightIntensity`, `LightFalloffAndPenumbra`, the four camera semantics,
`MorphTargetWeight` and the four `UserAttribute*` — and **not one of Rotation, Translation, Scale or
the four `ShaderParameterF*`**. Handling exactly the complement of the transform set is itself
special handling, and it is a cleaner split than the page's "every other semantic generically".

> **Corrected 2026-09-18 (FABLE).** `005CB150` references all nineteen, not twelve: the seven it seems to skip are referenced at their `+0x08` field (`lea r11, [01F2CE48]` = `Rotation + 8`, `005CB1F7`; likewise `+0x08` of `Translation`, `Scale` and the four `ShaderParameterF*`), which a sweep matching the entry's first byte cannot see. And it is not handling: it is the static teardown that unlinks those seven from the runtime list at `02CAFCD8` through their `+0x08` link and removes the other twelve through `005BFED0` (UQ-277). The shipped `+0x08 = 0` is the unlinked state of that runtime link, not an unused field.

### 4. `005C5C80` — all nineteen, four of them twice

920 bytes, `Presentation.Rendering.ShaderMaterial`. Every semantic appears, with `Rotation`,
`Translation`, `Scale` and `ShaderParameterF4` referenced **twice** each.

### What this changes

> ~~**`005C72A0` is not the only treatment, and "every other semantic generically" is not what the~~
> ~~image does.** The transform three are named in two places, the remaining twelve are grouped in a~~
> ~~third, and a fourth touches all nineteen with the transform three and `ShaderParameterF4` doubled.~~
> *(Corrected 2026-09-30, SWE2-DATA, from `UQ-277` (FABLE, 2026-09-18): the sweep matched only each entry's first byte. Re-swept at `+0x08` as well, `005CB150` references all nineteen and is the static teardown, and `005C5C80` is the static initialiser. So beyond the transform three, which the composer and `005C6F20` name, no semantic is handled specially.)*

### The control, and what it cannot see

The sweep matches a rip-relative reference whose target lands **on the table at its exact `0x18`
stride** — so it finds every direct `lea`/`mov` of a semantic and cannot produce a false positive
inside the run. What it cannot see is a reference **computed at runtime** as `01F2CE40 + index*0x18`;
such a site would index the table without naming an entry. That hole is the same one the `BM-3` sweep
had, and it is named for the same reason.

*(Read by OPUS 2026-09-14. `BM-2` is answered: ~~yes, in three other places, and the three are named~~
~~above.~~ the answer is no, per the `UQ-277` correction above; SWE2-DATA 2026-09-30.)*

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-animation-channel-binding-and-transform--cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0063BB60` | 58 B | when qword `+0x10` of `rcx` is non-null calls it with `rdx - 8` plus the sign-extended dword `+0x18`, or with that dword alone when `rdx` is null, and returns a non-zero result; when the qword is null or the call returns 0 it returns qword `+0x30` of the object at qword `+8` | `0063BB6D`, `0063BB76`, `0063BB80`, `0063BB84`, `0063BB90` |
| `00677A80` | 46 B | when qword `+0x10` of `rcx` is non-null calls it with `rdx` plus the sign-extended dword `+0x18` and returns a non-zero result; when the qword is null or the call returns 0 it returns qword `+0x30` of the object at qword `+8` | `00677A8D`, `00677A96`, `00677A99`, `00677AA4` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-animation-channel-binding-and-transform--ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `005A7AB0` | 157 B | returns 0 when `rdx` or `rcx` is null; otherwise, for each object in the chain starting at `rcx` and following qword `+0x78`, it walks the list whose sentinel is at the object's `+0xa0` (first element qword `[obj+0xa0]`, next element qword `[elem]`, the sentinel itself ending the walk) and returns the first element whose non-null qword `+0x18` points to a zero-terminated string byte-equal to the one at `rdx`; when the chain ends it returns 0 | `005A7AD0`, `005A7ADD`, `005A7B08`, `005A7B15`, `005A7B29` |
| `005AC9B0` | 132 B | stores `00D315B0` to qword `[rcx]`, calls `00584730` on qword `[rcx+0x20]` when that is non-null and dword `[rcx+0x18]` is not negative, zeroes `[rcx+0x20]` and dword `[rcx+0x18]`, stores `00D312F0` to `[rcx]`, and when bit `0x1` of `edx` is set calls `00584730(rcx)` if bit `0x4` is clear or `0016D6A0(rcx, 0x28)` if it is set; it returns `rcx` | `005AC9D0`, `005AC9E8`, `005AC9FE`, `005ACA10`, `005ACA20` |
| `005C5040` | 212 B | returns 0 when qword `[rcx+0x10]` is null or the low 31 bits of its dword `+0` are zero; otherwise, for each of that many element pointers (read through the qword at `+8` when the count is above 1, and taken from `+8` itself when it is 1), it takes `c` = the low 31 bits of the element's dword `+8` and `b` = 1 when the low 31 bits of its dword `+0x18` are non-zero (else 0), computes ((2`c`+`b`+2) rounded down to even)*16 + 0x1f rounded down to a multiple of 16, plus (6`c`+0x11) rounded down to a multiple of 16, and returns the unsigned maximum of these values | `005C505E`, `005C5099`, `005C50B9`, `005C50D8`, `005C50DD` |
| `005C6D90` | 170 B | reads `s` = qword `[rcx+0x18]` and fills the record at `r8`: dword `+0` = 0x30, qword `+4` = 2, dword `+0xc` = 0, float `+0x30` = the result of the vtable slot `+0x20` of the object qword `[rcx+0x20]` (0.0 when that is null), word `+0x34` = the low 31 bits of dword `[s+8]`, word `+0x36` = the low 31 bits `k` of dword `[s+0x18]`, qword `+0x18` = qword `[s]`, dword `+0x10` = the word at that pointer, qword `+0x28` = qword `[s+0x20]` and dword `+0x20` = `k`*0x58 + 0xf rounded down to a multiple of 16; it returns 0x40 | `005C6DC6`, `005C6DE5`, `005C6DF1`, `005C6E18`, `005C6E26` |
| `005C6F20` | 252 B | writes to the record at `r8` qword 0x10, qword 0 and the pointers `01F2CE40`, `01F2CE70` and `01F2CE58`, then, with `n` = the low 31 bits of dword `+0x20` of `t` = qword `[rcx+0x10]`, walks `n` 0x18-byte entries at qword `[t+0x28]` and appends to the qwords from `r8+0x28` a value from the 0x30-byte record selected by the entry's dword `+0xc` in the array at qword `[rdx+0x20]`: for record type dword 0 it is `02CAEB60` when the record's dword `+0x10` is below 0x80 and 0 otherwise, for type 1 it is the record's qword `+8` when the entry's qword `+0` is one of the three pointers and 0 otherwise, and 0 for any other type; it terminates the list with a zero qword and returns (`n`*8 + 0x2f rounded down to a multiple of 16) + 0x10 | `005C6F53`, `005C6FB1`, `005C6FE4`, `005C6FEB`, `005C7008` |
| `005C9F30` | 186 B | returns 0 when `edx` equals the low 31 bits `c` of dword `[rcx+0x18]`; otherwise, unless `edx` equals the whole dword, it calls `005E3040(edx, qword [rcx+0x20], min(edx, c))` and returns 0xd when that yields null for a non-zero `edx`, else calls `00584730` on the old qword `[rcx+0x20]` when that differs from the new pointer, is non-null and dword `[rcx+0x18]` is not negative, and stores the new pointer and `edx` to `[rcx+0x20]` and `[rcx+0x18]`; when `c` is below `edx` it zeroes the qwords from index `c` to `edx`-1 of the array at `[rcx+0x20]`; it returns 0 | `005C9F52`, `005C9F6F`, `005C9F9F`, `005C9FA8`, `005C9FC8` |
| `005CB4F0` | 165 B | calls the vtable slot `+8` of `rdx` with `rdx` and `rcx` and returns 0 when its byte result is zero; otherwise, for each of the low 31 bits of dword `[rcx+0x18]` qwords in the array at `[rcx+0x20]`, calls the vtable slot `+0x18` of each non-null element with that element, `rdx` and `rcx` and returns 0 when one yields a zero byte; after the loop it calls the vtable slot `+0x18` of `rdx` with `rdx`, `rcx` and `r8`, and returns 1 | `005CB50C`, `005CB534`, `005CB556`, `005CB573`, `005CB591` |
