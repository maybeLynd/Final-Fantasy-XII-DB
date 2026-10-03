---
system: The context-switch axes and the shader-variant key
category: 22-Middleware-PhyreEngine
status: DOCUMENTED
owner_layer: CodeDomain:Phyre.Rendering; no PrimaryOwner
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: offline disassembly of the shipping EXE with capstone; function boundaries and
    code-domain tags from the GN162 export at work/graph/functions.tsv, whose functions.parent.json
    stamps parent_gzf_sha256 59629b9b9a2f482e602f16fd... = GN162; every object address,
    vtable slot, switch name and literal read from the image, none from a decompiler comment.
    members/context-switch-family.tsv is generated from the EXE by its own script and prints
    the authority sha256 on every run
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-30
  last_pass_kind: falsification
  last_pass_state: opus-context-switch-falsification-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The context-switch axes and the shader-variant key

> **FFXII TZA does not ship one shader per material. It ships a family of compiled
> permutations per material, and eight named switches decide which one a draw call gets.**
> The switches are ordinary C++ objects with names you can read out of the executable —
> `NUM_LIGHTS`, `SKINNING_ENABLED`, `LOD_BLEND` — and each one knows two things: how to look
> at the draw that is about to happen and write down its own answer, and how to turn that
> answer back into the `-D` preprocessor define the shader was compiled with.

## 1. What this is, in one paragraph

Before Phyre can draw a mesh it has to pick which *build* of the material's shader to use: the
one compiled for four lights and skinning, or the one for no lights and static geometry, and so
on. It does that by asking a small ordered list of **context switches** — one per axis of
variation the material was authored against — to each write a number into a scratch buffer. The
concatenated numbers are the **context-variant key**. The key is looked up in a sorted table the
material carries, and the table entry's index selects the compiled variant. Everything in this
page is that mechanism: the nine switch classes, what each one actually reads, how the key is
built and searched, and how the same switches reproduce the compiler command line.

## 2. The nine classes and the eight singletons

Nine classes exist: the base `Phyre::PRendering::PContextSwitch` and eight subclasses. Each of the
eight subclasses has **exactly one instance in the shipping image**, a static object constructed
before `main` — the class names come from the vtable/class map, the switch names come from the
objects' own `.data`, and the two agree one-to-one:

| class | object | switch name | key words |
|---|---|---|---:|
| `PContextSwitchLights` | `01F2EBC8` | `NUM_LIGHTS` | 3 |
| `PContextSwitchLODBlend` | `01F2EBF0` | `LOD_BLEND` | 1 |
| `PContextSwitchInstancing` | `01F2EC18` | `INSTANCING_ENABLED` | 1 |
| `PContextSwitchShaderLODLevel` | `01F2EC40` | `SHADER_LOD_LEVEL` | 1 |
| `PContextSwitchShaderOrthoCamera` | `01F2EC68` | `ORTHO_CAMERA` | 1 |
| `PContextSwitchShader16BitIndices` | `01F2EC90` | `INDICES_16BIT` | 1 |
| `PContextSwitchShaderSkinned` | `01F2ECB8` | `SKINNING_ENABLED` | 1 |
| `PContextSwitchLowResParticles` | `01F2ECE0` | `LOW_RES_PARTICLES` | 1 |
| `PContextSwitch` (base) | *no static instance* | from the asset | 1 |

Full per-variant detail — vtable, installer, CRT initializer slot, teardown stub and all four
virtual slots — is in [`members/context-switch-family.tsv`](members/context-switch-family.tsv),
regenerated from the EXE by [`members/gen_context_switch_family.py`](members/gen_context_switch_family.py).

**The object is `0x28` bytes and says so itself**: every deleting destructor in the family passes
`0x28` to `free`. The layout, read from the constructor, the registrar and the evaluators:

| offset | what |
|---|---|
| `+0x00` | vtable — the base's is `00D80EA8`, each subclass installs its own |
| `+0x08` | the switch name, a plain `char*` |
| `+0x10` | next in the global registry, single-linked |
| `+0x18` | non-zero when the object is pool-owned (set only by the runtime constructor) |
| `+0x20` | how many `u32` key words this switch contributes |
| `+0x24` | the base class's value byte — read by the base evaluator, by nothing else |

## 3. Registration, and the budget that is not the key length

Each of the eight lives in the CRT dynamic-initializer table (`008C43E8`–`008C4420`), and each
installer does the same four things: hand the object to the by-name registrar `006B8D20`,
add its word count to the image-wide total `02E522E0`, install its own vtable over the base one
the `.data` image carries, and tail-jump to the MSVC `atexit` wrapper with its teardown stub.

`006B8D20(switch)` is **registration by name, and name-unique by construction**: it walks the
list head `02E522D0` comparing `+0x08` strings, returns `0x11` when the object has no name at
all, returns `0x12` on a duplicate name without linking it, and otherwise links the object at the
head and returns `0`. *The installer only adds to the budget when that return is zero* — a
duplicate name would cost a switch both its place in the registry and its words in the budget,
and nothing would report it.

**`02E522E0` ends static initialization at 10** — `3` for `NUM_LIGHTS` and `1` for each of the
other seven — and it is easy to read that as the
key length. It is not. `00606A20` uses it **only to size its stack scratch buffer**; the key a
given material produces is as long as *its own* switch list makes it, and `PContextSwitchLights`
alone emits between one and three words depending on the effect. The counter is a worst-case
bound, and the actual length is measured after the fact from how far the cursor moved.

The two teardown paths are symmetric and both subtract: each static object's `atexit` stub
unlinks it and subtracts its `+0x20` from the budget, and the base destructor `006B85F0` does the
same for a runtime-created one.

## 4. What each switch actually looks at

Every evaluator is vtable slot 2 and has the same shape: it is handed the effect, objects
describing the draw, and a **cursor** — a pointer to a pointer into the key buffer. It writes its
words at the cursor, advances the cursor by four per word, and returns 0.

> **Corrected 2026-09-22 (FABLE): there are SEVEN arguments, and the cursor is the FIFTH, not the
> last.** *This sentence previously read "three objects describing the draw, and a cursor", which
> both puts the cursor last and leaves out an argument entirely.* The per-switch readings below are
> unaffected — "the last argument" is still the last argument, because the cursor is not it. **§4b
> derives the full signature from the call site and from all seven bodies.**

The effect is identified, not assumed: `NUM_LIGHTS` reads `+0x00`, `+0x04` and `+0x70` of that
argument and `SHADER_LOD_LEVEL` reads `+0x74`, and those are exactly `m_supportedLightMask`,
`m_supportedShadowCasterMask`, `m_maxLightCount` and `m_numSupportedShaderLODLevels` in the
registered `VPEffect` schema — four independent offsets agreeing with the reflection data, each
used for the thing its name says. This page does not otherwise assume the file layout equals the
runtime layout; here the agreement is the evidence.

- **`NUM_LIGHTS`** — evaluated by `006B9120` (`PRendering::PContextSwitchLights`, vtable `00D80ED0` slot 2). The only non-trivial one. It walks the light list on the draw
  argument (`+0x10` count, `+0x18` array), keeps a light only when its light type's mask
  intersects the effect's `m_supportedLightMask`, and for each kept light looks up its
  shadow-caster type and keeps that only when *its* mask intersects `m_supportedShadowCasterMask`.
  Each survivor becomes a 10-bit code, `(shadowTypeIndex << 5) | lightTypeIndex`. **All survivors are
  sorted** — an introsort over 16-byte elements with a strict-less comparator on that code — and only
  then is the count taken as `min(kept, m_maxLightCount)`, so the key is independent of the order the
  lights arrived in and, when there are more lights than the effect supports, it is the
  lowest-numbered light types that survive, deterministically. The result is
  **bit-packed**: 4 bits of count followed by 10 bits per light, into
  `((10·n + 35) >> 5) << 2` bytes. With the registered budget of three words that tops out at
  nine lights. The kept count is also written back to the caller's record at `+0x20`.
- **`LOD_BLEND` — `006B90A0`.** Reads the geometry argument's `+0x40` container and the draw
  argument's `+0x20`/`+0x30`; indexes a three-float stride by `+0x30` and takes the first float.
  **It emits 1 only when that weight is strictly between 0 and 1** — a mesh sitting exactly on an
  LOD (weight 0.0 or 1.0) takes the cheap non-blending variant, and only a mesh mid-crossfade pays
  for the blend shader.
- **`INSTANCING_ENABLED` — `006B9070`.** One test: the last argument exists and its `+0x30` is
  non-null. Instance data present, instanced variant.
- **`SHADER_LOD_LEVEL` — `006B93D0`.** Takes a level from the geometry argument
  (`+0x40` → `[0]` → `+0x38`) and clamps it to `m_numSupportedShaderLODLevels - 1`, or to 0 when
  the effect declares none. This is the one switch whose value is not a flag.
- **`ORTHO_CAMERA` — `006B9410`.** Emits 1 when a float at `+0x6C` of the last argument's first
  member is at least `0.01`.
- **`INDICES_16BIT` — `006B93A0`.** Emits 1 when a byte at `+0x4C` of the last argument's `+0x38`
  object equals `0x0C` — a single format code, compared for equality, not a width test.
- **`SKINNING_ENABLED` — `006B9450`.** The composite one. With no binding object present it is
  just "the geometry argument has a `+0x18`". With one present it additionally requires that
  object's masked count at `+0x08` to be **`<= 0x78` (120)** *and* a runtime-keyed lookup to
  succeed — so a mesh whose bone palette is too large for the skinned variant silently falls back
  to the unskinned one rather than failing.
- **`LOW_RES_PARTICLES` — no evaluator of its own.** It inherits the base slot 2, which emits
  `+0x24 != 0`. See §7.

### 4a. The light list is `PLight`, named from reflection rather than from the callers (FABLE, 2026-09-22)

`GD-1` proposed recovering the draw-side classes from the render-item body's callers. That route is
wide — the key builder `00606A20` has exactly one caller, the submission body `0060B980`, and *that*
has **27**, spread across the `UQ-289` bodies and the `0065…` rendering group. **The narrower route
is the one §4 already used to identify the effect**: read the offsets and match them against the
recovered schema. It names the element class outright.

**The `NUM_LIGHTS` evaluator, `006B9120`, reads exactly three offsets per light, and all three agree with
`PLight`.**

```asm
006B91A0  mov rax, [r14 + 0x18]     ; the array          (r14 = the draw argument)
006B91A4  mov rdx, [r9 + rax]       ; rdx = one element
006B91A8  mov r10, [rdx + 0x20]     ; PLight::m_lightType      +0x20
006B91AC  test [r10 + 0x18], r15d   ; ... against PEffect::m_supportedLightMask
006B91B2  mov rax, [rdx + 0x18]     ; PLight::m_shadowCaster   +0x18
006B91BB  mov rax, [rax + 8]        ; PShadowCaster::m_shadowCasterType  +0x08
```

| offset read | schema member | class |
|---|---|---|
| element `+0x18` | `m_shadowCaster` → `PRendering::VPShadowCaster` | `PLight` |
| element `+0x20` | `m_lightType` → `PRendering::VPLightType` | `PLight` |
| that object `+0x08` | `m_shadowCasterType` → `PRendering::VPShadowCasterType` | `PShadowCaster` |

*Three independent offsets, each used for the thing its name says, and the second one's type is the
class the third offset then reads — that chain is the evidence, not any single hit.* The same check
re-identifies the effect from this body alone: `006B9154` reads `+0x00`, `006B915B` reads `+0x04`
and `006B91F3` reads `+0x70`, which are `m_supportedLightMask`, `m_supportedShadowCasterMask` and
`m_maxLightCount`. **So the draw argument holds an array of `PLight`.**

**The draw argument itself is an array holder in the engine's own convention**, not a reflected
member list: the count is at `+0x10` with **bit 31 used as a flag and cleared before use**
(`006B9157 btr esi, 0x1f`), and the pointer at `+0x18`. The submission body clears the same bit on a
different count at `0060BA1F`, so the convention is the engine's rather than this switch's. **Its
class is still not named** — no class in the recovered 183 carries an array of `PLight`.

**`PLightType` and `PShadowCasterType` are not among the recovered 183 either**, so their fields are
read positionally and named here only by role: **`+0x18` is a mask and `+0x1C` is an index**, the
same two offsets in both, which is why one 10-bit code can be built from a light type and a shadow
type without either class being known. *Recorded as the shape, not as field names — the schema does
not contain them and this page does not invent them.*

> **And one mechanism worth stating unambiguously, because §4's wording can be read the other way.**
> A light whose shadow-caster is **absent**, or whose shadow-caster type's mask **misses**
> `m_supportedShadowCasterMask`, is **still kept**. `006B91CF xor eax, eax` supplies a shadow index
> of **0** and execution falls into the same store at `006B91E1`/`006B91E5` that a matching light
> takes. **Only the shadow half of the code is zeroed; the light is not dropped.** The mask that can
> drop a light is the *light-type* one at `006B91AC`, which jumps clear over the store. So
> `(shadowTypeIndex << 5) | lightTypeIndex` has a well-defined meaning for a shadowless light —
> index 0 — and a variant key cannot distinguish it from a light whose shadow type genuinely is
> index 0.


### 4b. The evaluator signature, from the call site and from all seven bodies (FABLE, 2026-09-22)

§4's summary sentence was wrong about the argument list, and the error hid a whole parameter. The
signature is **seven arguments**, and both ends of the call agree on it independently.

**The caller.** The key builder `00606A20` makes the indirect call at `00606ADF
call qword ptr [rax + 0x10]` — vtable slot 2 — having set up:

```asm
00606AB7  mov rcx, [rax + rbx*8]    ; arg1  the switch object itself
00606ADC  mov rdx, rdi              ; arg2  = 00606A20's arg1, the effect
00606AD4  mov r8,  r13              ; arg3  = 00606A20's arg2
00606ACC  mov r9,  r12              ; arg4  = 00606A20's arg3
00606AD7  mov [rsp+0x20], rdx       ; arg5  lea rdx,[rbp+8] -- THE CURSOR
00606ACF  mov [rsp+0x28], r15       ; arg6  = 00606A20's arg4
00606AC7  mov [rsp+0x30], r14       ; arg7  = 00606A20's arg5   (r14 = [rbp+0x70])
```

*A caller's `[rsp+0x20]` is the fifth argument, `[rsp+0x28]` the sixth and `[rsp+0x30]` the seventh,
the first `0x20` being the shadow space.* So `00606A20` itself takes five arguments and forwards all
of them, inserting its own cursor between the third and the fourth.

**The callees, independently.** In a callee with no prologue adjustment the same three land at
`[rsp+0x28]`, `[rsp+0x30]` and `[rsp+0x38]`, the return address having shifted everything by 8.
Five of the seven evaluators adjust nothing, so they can be read directly; the other two shift, and
**their shift is confirmed rather than assumed**:

| evaluator | prologue | cursor (arg5) | arg6 | arg7 |
|---|---|---|---|---|
| `006B9070` `006B93A0` `006B93D0` `006B9410` `006B90A0` | none | `[rsp+0x28]` | `[rsp+0x30]` | `[rsp+0x38]` |
| `006B9450` `SKINNING` | `sub rsp,0x28` | `[rsp+0x50]` | `[rsp+0x58]` | `[rsp+0x60]` |
| `006B9120` (evaluator of key `NUM_LIGHTS`) | 5 pushes + `sub rsp,0x30`, `rbp = rsp+0x20` | `[rbp+0x60]` | `[rbp+0x68]` | `[rbp+0x70]` |

> **The control is the cursor idiom, and it is what makes the shifted rows trustworthy.** Writing
> through a pointer-to-pointer and advancing it — `mov rax,[rcx]` / `mov [rax],edx` /
> `add [rcx],4` — has a shape nothing else in these bodies has. *It appears in all seven evaluators,
> and in every one of them it lands on the slot this arithmetic calls **arg5**, whatever the
> prologue.* **A wrong shift would have put the cursor somewhere different in the two adjusting
> bodies than in the five flat ones.**

So the signature is:

| | argument | what it is |
|--:|---|---|
| 1 | `rcx` | the switch object |
| 2 | `rdx` | **the effect** — `SHADER_LOD_LEVEL` reads `[rdx+0x74]`, `m_numSupportedShaderLODLevels` |
| 3 | `r8` | **the geometry argument** — `[r8+0x40]` in `LOD_BLEND` and `SHADER_LOD_LEVEL`, `[r8+0x18]` in `SKINNING` |
| 4 | `r9` | **the draw/light argument** — `[r9+0x10]` count and `[r9+0x18]` array in `NUM_LIGHTS`, `[r9+0x20]`/`[r9+0x30]` in `LOD_BLEND` |
| 5 | stack | **the cursor** |
| 6 | stack | **an output record — see below. Read by `NUM_LIGHTS` alone.** |
| 7 | stack | **the trailing record** — `+0x00` the camera (§5a), `+0x30` instance data, `+0x38` the geometry descriptor |

#### The sixth argument is an output parameter, and it was missing from `GD-1`'s inventory (FABLE, 2026-09-22)

`GD-1` lists four draw-side objects. **There are five**, and the fifth is written, not read.
`NUM_LIGHTS` is the only evaluator that touches it, and it uses it twice:

```asm
006B92BE  mov r15, [rbp+0x68]       ; arg6
006B92D6  lea r15, [r15 + 8]        ; ... once per kept light
006B92E0  mov [r15 - 8], rcx        ;     store the PLight pointer
006B935C  mov rax, [rbp+0x68]
006B9360  mov [rax + 0x20], r12d    ; the kept count
```

**So the switch does not merely measure the lights — it hands back the filtered, sorted list.** The
surviving `PLight` pointers are copied consecutively from arg6 `+0x00`, and the count
`min(kept, m_maxLightCount)` is written to arg6 `+0x20`. *§4's remark that "the kept count is also
written back to the caller's record at `+0x20`" saw the second write without placing it: it is not
the trailing record, it is this separate sixth argument.*

> **That makes `NUM_LIGHTS` the one switch with a side effect, and it changes what it is for.** The
> other seven are pure: they read, they emit key words, they return 0. This one also populates the
> light set the draw will use. **A reimplementation that treats the context switches as a pure key
> function will silently produce an empty light list**, because the filtering and the sorting happen
> nowhere else — `006B83C0`'s introsort over the 16-byte survivor records is inside this evaluator.


### 4c. Two of the draw-side “objects” have no class, because the caller builds them on its stack (FABLE, 2026-09-22)

§4a named the light **element** and said the three containers were still unnamed. **Two of them are
not classes at all.** The key builder `00606A20` has exactly one caller, `0060B980`, and reading
that one call site settles it — a narrower route than §4a's rejected “render-item body's callers”,
because it is a single body rather than 27.

**`0060B980` uses a frame pointer**, `0060B991 lea rbp, [rsp + 0x50]`, with its stack cookie at
`[rbp + 0x1B0]` — so every `[rbp + N]` below is a **local of this function**, not a field of an
object. The call at `0060BDEF` sets up `00606A20`'s five arguments:

```asm
0060BDD5  lea rax, [rbp + 0x60]     ; arg5  -> a LOCAL   (the evaluators' arg7, the trailing record)
0060BDD9  mov [rsp + 0x20], rax
0060BDDE  lea r9,  [rbp + 0x100]    ; arg4  -> a LOCAL   (the evaluators' arg6, the light-list output)
0060BDE5  mov r8,  [r14 + 0x20]     ; arg3  = param1 + 0x20
0060BDE9  mov rdx, r12              ; arg2  = param2, passed straight through
0060BDEC  mov rcx, [r15]            ; arg1  = the effect
0060BDEF  call 0x606a20
```

*The argument numbering is §4b's: `00606A20` takes five and forwards them, so its arg4 is the
evaluators' arg6 and its arg5 is their arg7.*

> **So `GD-1`'s request to recover the classes of the trailing record and the output record is
> mis-posed: they are caller-allocated stack scratch and have no class to recover.** That is why no
> class in the recovered 183 fits them — not because the recovery is incomplete.

#### The light-list record is allocated as four pointers and a count — which settles `GD-5`'s structural half (FABLE, 2026-09-22)

`0060B980` zero-fills the output record in place before the call:

```asm
0060BA99  xor eax, eax
0060BA9B  mov qword ptr [rbp + 0x100], rax   ; record +0x00
0060BAA2  mov qword ptr [rbp + 0x108], rax   ; record +0x08
0060BAA9  mov qword ptr [rbp + 0x110], rax   ; record +0x10
0060BAB0  mov qword ptr [rbp + 0x118], rax   ; record +0x18
0060BAB7  mov dword ptr [rbp + 0x120], eax   ; record +0x20  <- the count
```

**Exactly four pointer slots and then the count** — and §4b showed `NUM_LIGHTS` storing `PLight`
pointers consecutively from `+0x00` and the count to `+0x20`. `GD-5` put the two readings as a
disjunction: *either* the record is a four-pointer array followed by the count *or* a five-light
effect corrupts its own count. **The allocation picks the first branch.** The caller reserves four
slots, so a fifth kept light would write its pointer over the count field — the collision is real,
and the structure is not a bug but a four-light bound the caller and the callee agree on.

> **This is independent of `GD-5`'s answer.** That one is about *this build* — `m_maxLightCount` is
> `0` in all 93 shipped effects, so no pointer is ever written. **This is about the contract**, and
> it is what a port has to honour: the record is `PLight*[4]` followed by a `u32` count.

#### The trailing record is a descriptor the caller assembles from its first parameter (FABLE, 2026-09-22)

The record at `[rbp + 0x60]` is built field by field immediately after, and **this is where the
first parameter's tail offsets go**:

| record | built from | instruction |
|---|---|---|
| `+0x00` | the **value** at `param1 + 0xA8` | `0060BABD` / `0060BAC4` |
| `+0x08` | the **address** `param1 + 0xB0` | `0060BAC8` / `0060BACF` |
| `+0x10` | the **address** `param1 + 0xF0` | `0060BAD3` / `0060BADA` |
| `+0x18` | `0` | `0060BADE` |
| `+0x20` | `param2` — the same object passed as the evaluators' arg3 | `0060BAE5` |
| `+0x28` | a pointer set earlier in the body; **which of two `lea`s is live needs flow analysis and is not established** | `0060BAEC` |
| `+0x30` | `param4` | `0060BB1E` |
| `+0x38`, `+0x40`, `+0x48` | `0`, then `+0x38` = a `0xC0`-stride geometry entry and `+0x40` = `esi` *(corrected 2026-10-02, OPUS: `0060BC46` and `0060BC4D` overwrite the zeros before the key call at `0060BDEF`)* | `0060BAF3`, `0060BAFE`, `0060BB08` |

**That explains the reads `§4a` could not place.** `0060B980` touches its first parameter at
`+0x00`, `+0x20`, `+0x28`, `+0x30`, `+0x38`, `+0xA8`, `+0xB0` and `+0xF0`; the last three are not
read for their own sake but **gathered into this descriptor**, which is then handed to every
evaluator as arg7.

#### What is still open, and the route that did NOT work (FABLE, 2026-09-22)

**The first parameter itself is still unnamed, and a set match will not name it.** Matching its
eight read offsets against the recovered field schema returns **no class above 5 of 8**, and the
tie is four unrelated classes — `PClusterHeaderBase`, `PLight`, `PMeshInstance`, `POctree` — while
`+0xA8`, `+0xB0` and `+0xF0` are matched by **none** of the 183.

> **The control is what makes that negative worth stating.** The same matcher, given the three
> offsets §4a used for the effect (`+0x00`, `+0x04`, `+0x70`), puts **`PEffect` first at 3 of 3 and
> reproduces `m_supportedLightMask`, `m_supportedShadowCasterMask` and `m_maxLightCount` by name.**
> So the matcher works and the parent genuinely is not among the recovered classes. **An offset-set
> match is a candidate generator, not a proof** — §4a's identification rested on a *chain*
> (offset → the member's declared type → that type's own offset), and no such chain is available
> here. Naming this object needs its constructor or its RTTI, not more offsets.

**Answered 2026-09-26 (FABLE, Claude Opus 5.5): both exist, and they name it `Phyre::PRendering::PRenderer`.** Control: [`gd1_first_parameter.py`](../../_index/candidates/gd1-first-parameter/gd1_first_parameter.py).
- **It is an RTTI class, not a reflected one.** That is why the schema matcher could not see it: it has a vtable and
  no member registrations. `0060B980` uses it polymorphically. It calls vtable slot 2 through the object. It also
  refuses unless bit 0 of dword `+0x08` is set and `+0x80` is non-null. Neither offset was in the eight above.
- **The vtables.** RTTI names three renderer vtables of three slots each: `PRenderer`, `PRendererBase` and
  `PRendererForJobs`. The first two share slot 2.
- **The constructor.** `PRenderer`'s constructor `005DC2F0` is the only installer of its vtable. It stores exactly
  the fields the body reads (`+0x08`, `+0x20`, `+0x28`–`+0x38`, `+0x80`, `+0xA8`), plus `+0x220`.
- **Where it lives.** Its one caller is the `PFramework::PApplication` constructor, which builds it at the
  application's `+0xE8`.
- **One path traced end to end, with the carrying register checked for writes at every hop.** The application
  hands `+0xE8` to the render singleton's builder, which stores it at the singleton's `+8`. A draw routine loads
  that `+8` and passes it down two levels to the caller of `0060B980`. That caller sets the object's `+0x80`,
  reads its `+0x220` (a field only this constructor initialises), and passes it as the first argument.
- **Scope.** The body's other callers pass the object through, and their roots are not traced. On a job path the
  dynamic type could be `PRendererForJobs`, which shares the `PRendererBase` layout and has its own slot 2.
- **Not read here:** what the renderer holds at `+0xA8`, `+0xB0` and `+0xF0`. The constructor zeroes `+0xA8` and
  does not touch `+0xB0` onward.

## 5. The key, the search, and the variant

`00606A20(effect, …)` is the whole key path. A raw `E8`/`E9` index over `.text` finds **one call
site**, and an aligned sweep of the data sections finds **no pointer to it**, so its only entry is
the render-item body `0060B980`:

1. If the effect's variant count (`+0x58`, masked) is zero it returns **−1** at once.
2. It `alloca`s `02E522E0 × 4` bytes and sets the cursor to the start.
3. It walks the effect's own switch array (`+0x50`, `+0x48` entries — the reflected
   `PArray<PContextSwitch const *>`), calling slot 2 on each, and stops early on a non-zero return.
4. It measures the key: `(cursor − start) / 4` words.
5. It **binary-searches** the effect's table at `+0x60`, whose entries are 16-byte
   `{count, words*}` descriptors, comparing first the word count and then the words themselves,
   and returns the index of the matching entry, or **−1** when the search closes without one.

`0060B980` treats that index as an offset into a 64-byte-per-entry table (`index << 6`) and, on a
negative result, leaves the slot null. **So the switches do not select a shader directly — they
build a key, and the key is a lookup into the variant list the material was compiled with.** If
the combination of light set, skinning and LOD a draw asks for was never compiled, the search
fails and the caller falls through; nothing is compiled on demand at this point.

That is also what the adjacent reflected type is for: `PContextVariantFoldingTable` registers
`m_contextVariantIndex` beside `m_contextVariantVpIndex` / `FpIndex` / `GsIndex` / `CsIndex` — one
resolved context-variant index mapping to a program index per pipeline stage.

### 5a. `GD-2` answered — the threshold is the projection matrix's bottom-right element (FABLE, 2026-09-22)

`GD-2` asked what the `ORTHO_CAMERA` evaluator's `+0x6C` field is, on the grounds that *"the constant
is meaningless until it is"* established. **It is element `[3][3]` of `PCamera::m_projectionMatrix`,
and the constant is an epsilon against zero.** The arithmetic is exact:

| | |
|---|---|
| `PCamera::m_projectionMatrix` | a `VMatrix4` at **`+0x30`** — four `Vector4` columns, **64 bytes**, so `+0x30`…`+0x6F` |
| the field read | **`+0x6C`** — `0x6C − 0x30 = 0x3C` = float **15** of 16, the matrix's **last** float |
| in a column-major `Matrix4` | float 15 is `col3.w`, i.e. **`M[3][3]`** |
| the next member | `m_viewProjectionMatrix` at `+0x70` — so `+0x6C` is the last float before it, and the read is inside the matrix rather than past it |

**`M[3][3]` is the standard discriminator between the two projections**: an orthographic matrix
carries **1** there and a perspective matrix carries **0**, because perspective puts its `−1` in the
`w` row instead. *So `006B9410` is not comparing a width or an inverse against a tolerance — it is
asking "is the `w` term non-zero", and `0.01` is simply a float-zero epsilon.*

> **Three independent things agree, which is why this is an answer and not a guess.** The switch is
> **named** `ORTHO_CAMERA`; the offset lands **exactly** on the one matrix element that separates
> orthographic from perspective; and the constant is the shape of an epsilon rather than of a
> threshold. *Any one alone would be suggestive; a wrong reading would have to get all three right by
> chance.*
>
> **What is assumed, stated so it can be attacked:** that the object at `*(arg7)` is a `PCamera`.
> *(Labelled `arg5` when this section was first published; §4b establishes that the trailing
> record is the **seventh** argument and the fifth is the cursor. The body read is unchanged —
> `006B9410` loads it from `[rsp+0x38]` either way.)*
> This is not proven here — what is shown is that **if** it is, `+0x6C` is `M[3][3]`, and that the
> name and the constant both fit that reading. *`GD-1` is the question that would settle the class
> outright, and it remains open.* *(2026-09-26 (FABLE, Claude Opus 5.5): `GD-1` now names the parent, a `PRenderer`. The
> trailing record's first slot is the value at the renderer's `+0xA8`, which its constructor zeroes and which is
> not read, so this `PCamera` assumption stands as stated; see §4c.)*

**The consequence for the variant key** is that the axis is a genuine either/or with no middle: the
evaluator emits `1` when the element is at least `0.01` and `0` otherwise, and a projection matrix
holds either `1` or `0` there. **A camera with a partly-perspective matrix is not a state this axis
can express** — and a reimplementation that derives the flag from a camera *mode* enum rather than
from the matrix will agree everywhere until something writes a matrix the enum does not describe.


### 5b. `GD-4` answered — one variant per effect, and the switches materials carry are MATERIAL switches (FABLE, 2026-09-22)

`GD-4` set its own success condition: *"turn 'the mechanism supports nine lights' into 'this build
ships N variants and uses at most M lights'"*. Read from the 93 shipped `PEffect` clusters through
the instance layout of §8b:

> ## **N = 1. M = 0.**
> **Every one of the 93 effects ships exactly one variant** (`m_effectVariants.m_count` = 1 in
> 93 / 93), and **every one authors `m_maxLightCount` = 0** (§8b). *The mechanism supports nine
> lights; this build asks for none, and offers the search exactly one thing to find.*

#### The switches a material carries are `PMaterialSwitch`, counted 93 / 93 (FABLE, 2026-09-22)

`PEffectVariant` carries `m_switches` at file `+0x01`. **It is the material-switch list, not a
context-switch list**, and the evidence is a count that matches per file rather than an argument
from position:

| `m_switches.m_count` | effects | `PMaterialSwitch` instances in the same cluster |
|--:|--:|--:|
| 0 | 13 | *no such list at all* |
| 2 | 3 | 2 |
| 3 | 20 | 3 |
| 4 | 30 | 4 |
| 5 | 20 | 5 |
| 6 | 6 | 6 |
| 7 | 1 | 7 |

**Compared cluster by cluster, not histogram against histogram: equal in 93 of 93, zero
mismatches**, the 13 zero rows being clusters that carry neither. *Histograms can agree by
coincidence; a per-file equality over 93 files cannot.*

> **This upgrades §8a's reading of `SKINNING_ENABLED` from positional to counted.** §8a argued the
> string was a material switch because it sat outside the namespace block beside eight names that
> are not context switches. **The count says the same thing without relying on where the bytes
> are**: `PhyreChrShader`'s variant declares `m_switches.m_count` = 5 and its cluster holds exactly
> 5 `PMaterialSwitch` objects — and `PMaterialSwitch` is `{ m_name, m_value }`, the `-D NAME=VALUE`
> pair. *The five names §8a printed are those five objects.*

#### How big the variant tables actually are (FABLE, 2026-09-22)

| | |
|---|---|
| `m_sceneRenderPasses.m_count` | **1 … 23**; **63 of 93** carry 23, 17 carry 15, the rest 1–7 |
| `m_largestShaderPassCount` | **1** (13 effects), **2** (63), **6** (17) |
| `m_tweakableShaderParameterDefinitions.m_count` | 3 … **89**; the bulk at 87 (28), 89 (20) and 88 (9) |

**So the breadth in this build is in render passes and shader parameters, not in context
variants.** *An effect with 23 scene render passes and 89 tweakable parameters still ships one
variant.*

> **What this does NOT establish, stated because §5 step 3 invites the inference.** §5 has
> `00606A20` walking the effect's switch array at runtime `+0x48`/`+0x50` and binary-searching the
> table at `+0x60`. **Which file member feeds that pair is still unestablished** (§8b), so this
> section does *not* claim the runtime loop iterates zero times. What is measured is the authored
> side: **no context switch is authored anywhere, one variant is, and the light cap is zero.**

## 6. The same switches write the compiler's command line

Vtable slot 3 is the inverse of slot 2. The base implementation `006B94C0` **reads one word back
off the cursor**, and when it is non-zero appends `-D`, the switch's own `+0x08` name, `=` and the
decimal value to a string being built. A zero contributes nothing, which is why
`INSTANCING_ENABLED=0` never appears on a command line: absence *is* the off state.

`NUM_LIGHTS` overrides it (`006B9630`) and emits per-light defines from two further literals,
`-DLIGHTTYPE_` and `-DSHADOWTYPE_`; `SHADER_LOD_LEVEL` overrides it too (`006B9A20`). **These
strings are the reason the reading is not an inference:** an object that names itself
`NUM_LIGHTS` and emits `-DLIGHTTYPE_…` is a shader preprocessor axis and nothing else. The ledger
agrees from a direction this page did not use — `006B9630` carries the code-domain tag
`Presentation.Rendering.ShaderPermutation`.

Slot 1 completes the picture: `006B9B90` **enumerates the switch's legal values** — it builds an
outer array of two entries, each a one-word array holding `0` and `1` — so a tool can walk the
product of every switch's domain and generate the permutation set. `NUM_LIGHTS` (`006B9CF0`,
1,709 B) and `SHADER_LOD_LEVEL` (`006BA3A0`, 300 B) override it as well; **neither body was read
here**, and the only thing claimed about them is that they occupy the same slot.

## 7. Two findings that fall out of the layout

**`LOW_RES_PARTICLES` is the only class in the family that overrides nothing but its
destructor.** Its vtable is the base vtable in every functional slot, so its value is whatever
`+0x24` holds — and its installer is the only one that writes `+0x24`, setting it to **0** over
the `1` the `.data` image carries. **That write is the only rip-relative access to the byte
anywhere in the image** — the adjacent `+0x20` word, scanned as a positive control, shows the
expected three (the installer's write and the teardown's two reads), so the instrument is sensitive
at that address. In this build the switch exists, occupies a key word, and answers 0 to every draw. A write through a pointer is not excluded — but the only route to the
pointer is the by-name lookup in §8, whose two entry points are one body with no reference
anywhere in the image and one reflection vtable slot. The class's whole purpose is to *be* a
named, default-off axis that assets can be authored against.

**The `PContextSwitch` string at `00D809C8` is a freelist name, not a class registration.** The
initializer at `00167010` declares a pool of `0x100` objects of `0x28` bytes named
`PContextSwitch`, and `001672D0` declares a second pool of `0x100` slots of `0x40` bytes for their
names. This settles the loose end `CL-2` left on
[the file schema against the runtime schema](../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md):
that page found a bare `.rdata` name with no `PClassDescriptor*<T>` and no object accessor and
concluded, correctly for the file schema, that `PContextSwitch` is registered through the type
path rather than the class path. **The runtime class is real** — vtable, constructor, eight
subclasses — and the reason it needs no class descriptor is §8: assets reference a switch *by
name*, and no switch object is ever serialised.

## 8. The ninth variant: the one built at runtime

The base class is not abstract, and it is instantiated — by `006B89C0`, which the image names for
us. On a miss it prints a warning whose format string is
`"PNamedSemanticDynamic::FindOrCreateDynamic : Performance warning - allocating freelist on demand for '%s'."`,
lazily initialises the two pools from §7, copies the name into a name slot, and calls the
constructor `006B8590`, which sets the base vtable, one key word, value `1`, marks the object
pool-owned at `+0x18` and registers it.

Its two entry points are the reflection side: `006B94B0`, a slot in the vtable of
`PNamedSemanticDescriptorForDynamicType<PContextSwitch>`, tail-jumps straight into it, and
`006B8DB0` wraps it with a `0x13` "not found" error and has **no call site and no aligned data
reference anywhere in the image**. A sibling slot, `006B8F70`, fills a caller's array with every registered switch in
registry order. So the load-time story is: **an asset names its switches, and the loader resolves
each name against the registry, manufacturing a plain base-class switch for any name the engine
does not implement.** That is why the eight subclasses can be hard-coded while the vocabulary
stays open.

The pool-owned flag is what shutdown uses: `005FDD40` walks the registry and unlinks **only**
entries whose `+0x18` is set, subtracting each one's word count, then releases both pools — the
eight static switches are left to their own `atexit` stubs.

**Note, stated as what the code does:** the name copy in `006B89C0` is a `strlen`-then-`memcpy`
into a fixed `0x40`-byte pool slot with no length check. Nothing in the shipped data is known to
reach it — the path only runs for a name that no static switch already owns, and this build's
assets have not been surveyed for one. `GD-3`.

### 8a. `GD-3` surveyed — no shipped cluster declares a context switch (FABLE, 2026-09-22)

§8 ends *"this build's assets have not been surveyed for one. `GD-3`."* **They have now.** The corpus
is the extracted game at `D:/FFXII_TZA_extract` — **35,984 `.phyre` clusters**, the nine language
copies of the shipped data — read through the packed-namespace decoding already established in
[the file-side schema page](../Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md).

> **The decoder was checked against a published answer before it was used for anything.** That page's
> header control — `m_phyreMarker` 0, `m_size` 4, `m_packedNamespaceSize` 8, `m_platformID` 12,
> `m_instanceListCount` 16, `m_physicsEngineID` 68 — **reproduces 6 of 6, zero mismatches**, from a
> shipped cluster, and none of those six offsets was used to build the decoder.

#### What the sweep found (FABLE, 2026-09-22)

| | |
|---|--:|
| clusters referencing the type `PContextSwitch` | **2,184** |
| of those, clusters that decode | **2,184** — none undecodable |
| of those, clusters carrying a `PEffect` class | **2,184** — exact correlation, both ways |
| of those, clusters carrying `PArray<PContextSwitch *>` | **2,184** |
| **of those, clusters declaring a `PContextSwitch` class** | **0** |

**A cluster's packed namespace declares every class whose instances the file holds** — that is what
makes the file self-describing. So a cluster that never declares `PContextSwitch` cannot contain a
context-switch object. **No shipped cluster contains one.** Every effect declares the *array of
pointers to* them and not one supplies an element.

#### And the name sweep agrees, including the one apparent counter-example (FABLE, 2026-09-22)

Of the eight switch names, **seven appear in zero clusters of the 35,984**. `SKINNING_ENABLED`
appears in **12**, all under `gamedata/d3d11/artdata/shaders/`, and in every one of them it is
**not a context switch**:

- it lies **outside the packed-namespace block**, in instance data — checked against the block's own
  `[hs, hs+ns)` bounds in each of the 12, and it is outside in all 12;
- it sits in an alphabetically ordered NUL-separated run following the string `PhyreChrShader.fx` or
  `PhyreDefaultLitShader.fx`, beside **eight other names that are not context switches**:
  `DISABLE_ALPHA_BLEND`, `DISABLE_ALPHA_THRESHOLD`, `ENABLE_ALPHA_TO_COVERAGE`, `FORCE_CULLING`,
  `LIGHT_COLOR_STREAM`, `RECEIVE_SHADOWS`, `TEXTURE_ENABLED`, `VERTEX_COLOR_ENABLED`;
- the run differs per variant, which is what a per-variant define list looks like.

*The file's own schema supplies the reading:* it declares `PMaterialSwitch` as exactly
`{ m_name, m_value }` — **the authored half of the same `-D NAME=VALUE` vocabulary §6 shows the
context switches writing at vtable slot 3.** So `SKINNING_ENABLED` is a name **two different classes
can carry**, and finding the string proves nothing about which one wrote it. **Here it is the
material side.**

#### The file-side `PEffect`, which is how any of this is readable (FABLE, 2026-09-22)

The shipped clusters name the class outright — **`PEffect`**, a root class under `PBase` — which
confirms §4's identification from a source §4 did not use. **Its file layout is not its runtime
layout**, and that is worth recording because §4 deliberately declined to assume they were equal:

| member | **file** offset | **runtime** offset | |
|---|--:|--:|---|
| `m_supportedLightMask` | `+0x00` | `+0x00` | agree |
| `m_supportedShadowCasterMask` | `+0x04` | `+0x04` | agree |
| `m_effectFile` | `+0x08` | `+0x08` | agree |
| `m_effectFileFromBasePath` | `+0x09` | `+0x10` | **differ** |
| `m_effectSource` | `+0x23` | `+0x68` | **differ** |
| `m_maxLightCount` | `+0x24` | `+0x70` | **differ** |
| `m_numSupportedShaderLODLevels` | `+0x28` | `+0x74` | **differ** |

> **§4's caution was justified, and narrowly so.** The two fields §4 leans on for the effect's
> identity, `+0x00` and `+0x04`, are the two that happen to agree; the two it also cites, `+0x70` and
> `+0x74`, do **not** agree with the file. *Reading `m_maxLightCount` out of a shipped cluster at
> `+0x70` would silently return the wrong field.*

**The file declares five members the runtime reflection never registers** — `m_effectVariants`,
`m_supportedLightTypes`, `m_supportedShadowCasterTypes`, **`m_contextSwitches`** and
`m_contextVariantSwitches`, each a 5-byte inline `PArray` descriptor of `{ m_count:4, m_els:1 }`.
*`m_contextSwitches` appears nowhere else in this database.* The file record is **gapless**: sorted
by offset the members run `0, 4, 8, 9, 10, 15, 20, 25, 30, 35, 36, 40`, each advancing by exactly
the preceding member's declared width, for 44 bytes total — **an internal control that the offset
and width columns are being read as what they are.**

#### What this settles, and what it does not (FABLE, 2026-09-22)

**Settled: no shipped asset supplies a context switch**, so none can name one the engine does not
implement, and **§8's unbounded `0x40`-byte name copy is not reached by this build's data.** The
vocabulary stays open in the code and is unused by the assets.

> **Not settled, and it is the reason this narrows `GD-3` rather than closing it.** The sweep proves
> no cluster *declares* a switch class. It does **not** establish whether the `m_contextSwitches`
> arrays are **empty** or carry external references resolved some other way — **an attempt to walk
> the instance lists and read `m_count` did not reproduce a coherent layout and its output is not
> relied on here.** If such a reference exists and carries a name, that name is by construction one
> I cannot enumerate, since `GD-3` asks about switches the engine does *not* implement. **Reading
> `PEffect`'s `m_contextSwitches.m_count` out of the instance data is the step that would close it**,
> and it needs the instance-list layout established first.

### 8b. The instance data read — every shipped effect authors an EMPTY context-switch list (FABLE, 2026-09-22)

§8a left one thing open and named the step that would close it: *"reading `PEffect`'s
`m_contextSwitches.m_count` out of the instance data"*, blocked because **my own attempt to walk the
instance lists produced nonsense.** The defect was the ordering, and it is worth stating because it
is a natural wrong guess:

> **The instance-list headers are CONTIGUOUS, not interleaved with their data.** A cluster is
> `84-byte header | packed namespace | m_instanceListCount × 36-byte PInstanceListHeader | all the
> instance data, in list order`. *Reading each 36-byte header as though its `m_size` bytes followed
> it immediately walks off the end of the file* — which is what §8a reported and did not rely on.
>
> **AMENDED 2026-09-22 (FABLE), and the amendment is against me.** *This layout was already
> established* — `CU-3`'s narrowing of **2026-09-12**, in
> [the cluster-header page](../Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md)
> §'s `CU-3` box, records that `m_totalDataSize` equals the sum of the lists' `m_size` over
> **35,984 / 35,984** files and that **the instance data is one contiguous run in list order**,
> *"walked that way to read the parameter buffers for `CU-2`"*. **§8a's failed walk would not have
> happened had I grepped the register first**, and the controls below are a re-confirmation of a
> known layout on a new class, not a discovery of it.

#### Four controls, none of which was used to build the reading (FABLE, 2026-09-22)

| control | result |
|---|---|
| every `m_classID` resolves to a class in that cluster's own namespace table | **2,184 / 2,184 clusters**, and the ids are **ascending** in every one |
| `m_size == m_objectsSize + m_arraysSize` on every list | **0 violations** |
| `PEffect`'s `m_objectsSize` against the record size derived *independently* from the member offset/width table in §8a | **44 = 44**, in all 93 |
| the bytes immediately after the 44-byte record | begin `ArtData/shaders/PhyreChrShader.fx` — **the effect's own `m_effectFile` string, exactly where the layout says the variable-length data starts** |

*The last one is what settles it:* a wrong offset does not land on the object's own filename. The
layout also generalises — checked on `chr/bg_obj` `.dae.phyre` clusters of 144, 34 and 90 lists with
the same checks clean.

#### What the 93 shipped effects actually author (FABLE, 2026-09-22)

**There are 93 `PEffect` instances in the shipped data, not 2,184.** *That distinction matters and
§8a's figure should be read with it:* 2,184 clusters **declare** the `PEffect` class, because a
cluster declares every class it references, but only the 93 under
`gamedata/d3d11/artdata/shaders/` **hold one**, and each holds exactly one.

| field | value, across all 93 |
|---|---|
| `m_contextSwitches.m_count` | **0** |
| `m_contextVariantSwitches.m_count` | **1** |
| `m_maxLightCount` | **0** |
| `m_supportedLightMask` | **0** |
| `m_numSupportedShaderLODLevels` | **0** |
| `m_effectVariants.m_count` | **1** |

**Not one shipped effect authors a context switch.** The array is empty in the post-process effects
and in the character shaders alike — `PhyreChrShader` and `PhyreDefaultLitShader` author exactly
what `BrightnessShader` does.

#### `GD-3` answered, and `GD-5` answered with it (FABLE, 2026-09-22)

**`GD-3` — no.** No shipped asset names a context switch, so none names one the engine does not
implement. §8a established that no cluster *declares* the class; this establishes that no effect
*asks* for one. **§8's unbounded `0x40`-byte name copy is not reachable from this build's data**,
and the open vocabulary is a property of the code that the assets never exercise.

**`GD-5` — the collision cannot occur in this build.** `GD-5` asked how many lights the sixth
argument's array can hold, because `NUM_LIGHTS` writes `min(kept, m_maxLightCount)` pointers from
`+0x00` and then the count to `+0x20`, and those collide at five. **`m_maxLightCount` is `0` in all
93 shipped effects**, so the written count is `min(kept, 0) = 0` and not one pointer is ever stored.
*The structural question — whether the record is a four-pointer array followed by its count — is
not answered and does not need to be: it is unreachable.* **It survives only as a porting note**: a
reimplementation that authors a fifth light where this build authors none meets a defect the
original never could.

> **Read the authored zeros for what they are, and not for more.** `m_supportedLightMask` is `0` in
> all 93 too, so `NUM_LIGHTS` would keep no light even if a switch asked it to. **This page does not
> claim the RUNTIME arrays are empty.** The loader maps the file record onto a different runtime
> layout — §8a: `m_maxLightCount` is `+0x24` in the file and `+0x70` at runtime — and **which file
> member feeds `00606A20`'s `[rdi+0x48]`/`[rdi+0x50]` pair is not established here.** What is
> established is what the shipped data *says*.

### 8c. `GD-6` answered — the element is a `PNodeContext`, and it is in the file (FABLE, 2026-09-22)

**`GD-6` was wrong where it guessed, and the correction is mine to make.** It said the one
`m_contextVariantSwitches` element *"is not an in-file object"*, reasoning that no cluster declares
a `PContextSwitch` and none holds an instance list of one. **Both of those facts are true and the
conclusion drawn from them is not**, because the array's element type was assumed from the member's
name rather than read.

> **The member record already carries its own type, and that column was decoded ten days ago.**
> `CX-3` (2026-09-12) establishes member `w1` as *a 0-based type-table index when `< nTypes`, else
> `nTypes` plus the class's 1-based id*, resolving **2,192,621 / 2,192,621** records — see
> [the packed-namespace page](../Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md) §8.
> *I re-derived it before looking it up. That is the third time this session, and the rule is the
> same each time: grep the register before building an instrument.*

Read that way, `PEffect`'s two switch members are **different types**:

| member | declared element type | authored count |
|---|---|--:|
| `m_contextSwitches` | `PArray<PContextSwitch *>` | **0** in all 93 |
| `m_contextVariantSwitches` | **`PArray<PNodeContext>`** — *not* a context switch at all | **1** in all 93 |

The same decoding reproduces `m_effectFile` → `PString`, `m_effectVariants` →
`PArray<PEffectVariant *>`, `m_supportedLightTypes` → `PArray<PLightType *>` and
`m_supportedShadowCasterTypes` → `PArray<PShadowCasterType *>` — every one the type its name
implies, which is the control that the column is being read correctly.

#### And the object is there, counted the same way `GD-4` was (FABLE, 2026-09-22)

**`m_contextVariantSwitches.m_count` equals the cluster's `PNodeContext` instance count in 93 of 93
clusters, zero mismatches**, compared per file. So the element is an ordinary in-file object, and
no fixup, registry index or external reference is involved.

**`PNodeContext` has exactly one member: `m_packedSwitches`, 8 bytes at `+0x00`.** *That is the
authored packed switch word — the same shape the evaluators build at run time, stored rather than
computed.* **Its value is `0x0000000000000000` in all 93 effects.**

> **Which closes the authored picture consistently, and that consistency is the point.** Every
> shipped effect authors an empty `m_contextSwitches` (§8b), a zero `m_maxLightCount` (§8b), one
> variant (§5b), and a `m_packedSwitches` of zero. **Four independent fields, four ways of saying
> the same thing: this build authors no context-switch state at all.** *A wrong reading of any one
> of them would have had to agree with the other three by chance.*

## 9. What this closes, and what it does not

This page reads **18 of the 48 functions** that `UQ-289` / `EA-5` say were never read — the eight
installers, the constructor, the base destructor and the eight deleting destructors — plus the
neighbours that make them a mechanism. The other half of that question, *"their share of its
44,758 bytes is not measured"*, is now measured, by an instrument independent of the one that drew
the original line:

| group | functions | bytes | share of 44,758 |
|---|---:|---:|---:|
| reference a shader-parameter or diagnostic string | 13 | 22,733 | 50.8 % |
| reference only a three-byte run that decodes as text | 4 | 258 | 0.6 % |
| **reference no string — `UQ-289`** | **48** | **21,767** | **48.6 %** |

So the 48 are **40 % of the tag group by count and 48.6 % by bytes** — very close to half the
family, not the long tail of stubs the count alone suggests. The string-carrying body the original
census left unnamed is `001F5D70` (2,924 B); its string is the `EASTL vector` diagnostic.

The remaining 30 are not read here, but they are no longer unclassified — every one was profiled
for callers, callees and data references, and the six groups partition the 48 exactly:

| group | count | bytes | what they are |
|---|---:|---:|---|
| **this page's switch family** | 18 | 1,222 | read here in full |
| the `0065xxxx` material-selector bodies | 11 | 13,651 | the largest single block of the 48. Each is called from exactly one `0065Bxxxx` body and each calls the render-item body `0060B980`; the class map names three of them `PRendering::PMaterialSelectorMaterialSet` / `PMaterialSelectorBase`, and the nine `0065Bxxxx` callers have no call sites of their own — they are vtable slots, one of them `PPostProcessing::PScreenSpaceReflection` slot ~~1~~ 6 *(corrected 2026-10-02, OPUS: `0065B920` sits at `00D626F0`, slot 6 of `00D626C0`; the post-effect page's slot-6 render overrides, so these are post-effect workers)*. A class family with a vtable, sitting directly upstream of this page: a selector picks the effect whose switches then build the key |
| no caller, no data reference | 2 | 4,948 | `001B76E0` and `001E2AF0`, both also callers of `0060B980` |
| single-caller leaf helpers | 9 | 1,349 | `005DBF60`, `005DC0B0`, `005DC2F0`, `0060E9C0`, `00613770`, `0061C250`, `0061CFA0`, `006BEC40`, `006C0FE0` |
| a shared helper | 1 | 139 | `006160B0`, called from 20 sites in 13 different bodies — the only one of the 48 with more than one caller |
| vtable-slot members (reached ~~only~~ through a data qword; `0018D0E0` also has 52 direct call sites *(corrected 2026-10-02, OPUS: the other six have none, CON-200)*) | 7 | 458 | `0018D0E0`, `0018D100`, `0018D130`, `005CE850`, `005D6E00`, `005E2AA0`, `005E2AF0` |

`UQ-289` stays open on those 30.

**Neighbour accounting — the classification above is the only thing on this page that reaches
outside Phyre, and the crossings are this section's doing.** Three of the thirty touch two foreign
layers: the shared helper's call sites include three bodies owned by **Presentation**, one of the
two no-caller bodies calls one **Presentation** function, and the `EASTL vector` body named above
calls one **Resource** function. In every case *this page is naming a function's neighbourhood in
order to classify it, and claims nothing about either layer's behaviour* — no function documented
in §§2–8 calls or is called by anything owned by Presentation or Resource, and the switch family
itself is entirely inside Phyre and the C++ substrate.

The narrowing `UQ-289` now carries is that **the tag group is not one thing**: a fifth of it by
count is this switch family, over half its remaining bytes is a band of render bodies that all
funnel into `0060B980`, and the rest is vtable slots and leaves.

## 10. Open questions

- [x] **`GD-1`.** **What the draw-side arguments are.** *(NARROWED AGAIN 2026-09-22 (FABLE): two of the
  three containers are caller stack scratch and have no class — §4c.)* The evaluators read four distinct objects
  — the effect (identified), a geometry argument, a draw/light argument and a trailing
  record — and this page names them only by what each field does. Their classes are not recovered.
  ~~The route is the render-item body's own callers rather than the switches.~~
  **NARROWED 2026-09-22 (FABLE): the draw argument's ELEMENT class is recovered, and it did not
  need the callers.** See §4a — the route that worked was the one §4 already used for the effect,
  matching the offsets the evaluator reads against `Reflection-And-Class-Metadata/phyre-field-schema.tsv`.
  ~~**The three container classes are still unnamed** and that half of `GD-1` stands.~~
  **NARROWED AGAIN 2026-09-22 (FABLE): two of the three are not classes.** §4c reads the single call
  site `0060BDEF` in `0060B980`, whose `lea rbp, [rsp + 0x50]` frame makes both the trailing record
  (`[rbp + 0x60]`) and the light-list output record (`[rbp + 0x100]`) **locals of the caller**. The
  trailing record is a descriptor assembled from `param1 + 0xA8/+0xB0/+0xF0`, `param2` and `param4`.
  **Only the first parameter is still unnamed**, and a set match will not name it: best coverage is
  5 of 8 across four unrelated classes, against a control that puts `PEffect` first at 3 of 3.
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): the first parameter is Phyre's renderer, a `PRendering::PRenderer` (a
  `PRendererBase`), and on the traced path it is the one built into the application object.** Control: [`gd1_first_parameter.py`](../../_index/candidates/gd1-first-parameter/gd1_first_parameter.py)
  (6 checks, FAILS 0). First read by a delegated read-only pass; every step re-checked.
  Every draw-side object is now accounted for:
  - the effect and the `PLight` elements (§4a);
  - the two stack records (§4c);
  - the parent, the renderer (§4c, "What is still open").
  The renderer's `+0xA8`/`+0xB0`/`+0xF0` contents and `GD-2`'s `PCamera` assumption are not settled by this.
- [x] ~~**`GD-2`.** **The `ORTHO_CAMERA` threshold.** A float at `+0x6C` compared against `0.01`
  decides an orthographic-camera variant. What the field is — a projection term, a width, an
  inverse — is not established, and the constant is meaningless until it is.~~
  **ANSWERED 2026-09-22 (FABLE): it is `M[3][3]` of the camera's projection matrix, and `0.01` is an
  epsilon against float zero.** See §5a.
- [x] **`GD-5`.** **How many lights the sixth argument's array can actually hold.** §4b shows
  `NUM_LIGHTS` writing `min(kept, m_maxLightCount)` `PLight` pointers consecutively from arg6
  `+0x00`, and then the count to arg6 `+0x20`. **Those two writes collide at five lights**: the
  fifth pointer lands on `+0x20` and the count then overwrites it. So either the record holds a
  four-pointer array followed by the count, and shipped effects declare `m_maxLightCount <= 4`, or
  a five-light effect corrupts its own count field. **The key format is not the constraint** —
  `((10n + 35) >> 5) << 2` against the registered three-word budget admits **nine**. Settling it
  needs the authored `m_maxLightCount` values, which is `GD-4`'s data question, not a code one.
  **ANSWERED 2026-09-22 (FABLE): unreachable in this build.** `m_maxLightCount` is **`0` in all 93
  shipped effects**, so `min(kept, 0) = 0` pointers are written and the two writes never meet. The
  structural question is not answered and does not need to be; it survives as a porting note. §8b.

- [x] **`GD-6`.** **What the one `m_contextVariantSwitches` element in every shipped effect
  resolves to.** §8b: `m_contextSwitches` is empty in all 93 effects, but `m_contextVariantSwitches`
  holds **exactly one** element in all 93. No cluster declares a `PContextSwitch` class and **no
  cluster anywhere holds an instance list of one** (checked over all 2,184), so that element is not
  an in-file object; the record's trailing array region is fully accounted for by the two filename
  strings, so no name accompanies it either. **Whether it is a fixup to an external object, an index
  into the registry, or a placeholder resolving to nothing is not established** — and it is the one
  authored reference this subsystem has left.
  **ANSWERED 2026-09-22 (FABLE): it is a `PNodeContext`, and it IS an in-file object — the clause
  above saying otherwise is withdrawn.** The array's declared element type is
  `PArray<PNodeContext>`, not `PArray<PContextSwitch *>`; I had assumed it from the member's name
  instead of reading the member record's type column. `PNodeContext` holds one field,
  `m_packedSwitches` (8 bytes), and it is **zero in all 93**. Counted per file, 93/93. See §8c.

- [x] **`GD-3`.** **Whether any shipped asset names a context switch the engine does not
  implement.** That is the only way the base class is ever constructed, the only way `+0x24`
  can be anything but its authored value, and the only way the unbounded name copy in §8 is
  reachable. It is an authored-data question over the `.phyre` clusters, not an executable one.
  **BOUNDED 2026-09-22 (FABLE): surveyed over 35,984 shipped clusters — none declares a
  `PContextSwitch`.** All 2,184 that reference the type carry `PArray<PContextSwitch *>` and a
  `PEffect`, and not one declares the element class, so no cluster contains a switch object. Seven
  of the eight names appear in zero clusters; `SKINNING_ENABLED` appears in 12 as a **material**
  define, outside the namespace block. **Still open:** whether the `m_contextSwitches` arrays are
  empty, which needs the instance-list layout. See §8a.
  **ANSWERED 2026-09-22 (FABLE): no — and the array question is settled too.** `m_contextSwitches`
  is **empty in all 93 shipped effects**, read from the instance data once the list layout was
  corrected. No asset names a context switch at all, so none names one the engine does not
  implement, and §8's name copy is unreachable from this build's data. See §8b.
- [x] **`GD-4`.** **Which materials carry which switches, and how big the variant tables are.**
  `00606A20` reads the effect's switch array and key table; their contents are in the shipped
  assets. This would turn "the mechanism supports nine lights" into "this build ships N variants
  and uses at most M lights".
  **ANSWERED 2026-09-22 (FABLE): N = 1, M = 0.** All 93 shipped effects ship exactly one variant
  and author `m_maxLightCount` = 0. The switches a material carries are **`PMaterialSwitch`** —
  `m_switches.m_count` equals the cluster's `PMaterialSwitch` instance count in **93 / 93**, zero
  mismatches. See §5b.

## 11. Evidence

| claim | evidence | tier |
|---|---|---|
| eight static singletons, `0x28` bytes each, one per vtable | `members/context-switch-family.tsv`, generated from the EXE by walking the CRT initializer table | 1 |
| the **class names** attached to those vtables | the GFZ class map, a name oracle — joined to the binary here by vtable slot 0 and by the one-to-one agreement with the objects' own `+0x08` names (`PContextSwitchLights` ↔ `NUM_LIGHTS`, and so on for all eight) | 2 |
| object is `0x28` bytes | every deleting destructor passes `0x28` to `free`; the freelist at `00167010` declares `0x28`-byte elements | 1 |
| registration is by name and name-unique | `006B8D20` read in full: `0x11` on a null name, `0x12` on a duplicate, head insert otherwise | 1 |
| the budget is 10 words and is a buffer bound, not the key length | the eight installers' `add`/`inc` on `02E522E0`; `00606A20`'s `alloca` of `total × 4`; its own `(cursor − start) / 4` measurement | 1 |
| the argument at slot 2's position 2 is the effect | four offsets (`+0x00`, `+0x04`, `+0x70`, `+0x74`) read by two evaluators match the registered `VPEffect` members, each used for the thing its name says | 1 |
| slot 3 writes `-D<NAME>=<value>` | `006B94C0` read in full; the literals `-D`, `=`, `-DLIGHTTYPE_`, `-DSHADOWTYPE_` read from the image | 1 |
| the base class is constructed at runtime by name | `006B89C0`'s own format string names `PNamedSemanticDynamic::FindOrCreateDynamic`; it calls `006B8590` | 1 |
| `LOW_RES_PARTICLES` answers 0 in this build | its vtable is the base vtable in all three functional slots; its installer writes `+0x24 = 0`, and a rip-relative sweep of that one byte finds **that write and nothing else** — positive control on `+0x20`, which returns three accesses | 1 |
| the 48 are 21,767 bytes | independent re-run of the string split over the 65 tagged functions, reproducing the published 17/48 boundary | 1 |


## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Presentation — CLIENT and SERVICE (4 edges).** The shared helper `006160B0`, a 139-byte constructor (it runs a base constructor, zeroes its members and installs one callback pointer), is called by the three render-layer bodies `00183A00`, `00183C60` and `00183EE0`; and `001E2AF0`, one of the two bodies with no caller and no data reference, calls the 1,084-byte presentation body `001ABF50`. The render layer constructs objects through a helper this page's `UQ-289` census profiled, and an uncalled census body reaches a render body; neither edge touches the context-switch key this page decodes.

**Resource — SERVICE, MECHANICAL (1 edge).** `001F5D70`, the 2,924-byte body whose string is the `EASTL vector` diagnostic, calls the 22-byte `(namespace, index)` path resolver `002DF980`. It is one more caller of the engine's generic path lookup, used by value.

## 12. Related

- [The post-process passes and their shader constants](../Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md)
  owns `UQ-289` / `EA-5` and the tag census this page's §9 measures. The twelve passes it documents
  are also the largest group of callers of the render-item body that drives the key lookup.
- [The file schema against the runtime schema](../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md)
  owns `CL-2`. §7 here supplies the cause its answer left open: the bare `.rdata` name is a
  freelist's, and switches are referenced by name rather than serialised.
- [Member registration and the recovered field schema](../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md)
  is where `VPEffect`'s registered members come from — the four offsets §4 uses to identify the
  evaluators' effect argument.

## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives; one detail of §3 narrowed

**Attack.** §2–§4's static claims were turned into checks. The expected values are the page's own prose; nothing was
taken from its generated members table. Every value is re-derived from the image: the object's `.data` name and vtable,
the installer's own instructions, slot 2 of the installed vtable, the deleting destructor's `free` size, the CRT
slots, the registrar's returns, and each evaluator's constants. Script:
`Tools/analysis-kit/gfz-scripts/falsify_context_switch.py`, output `falsify_context_switch.out`, image `73461d08…`,
0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| X1 | §2 eight singletons: `+0x08` names the switch; 3 words for `NUM_LIGHTS`, 1 for the rest | **survives**. All eight names read from `.data`, and each object's `.data` vtable is the base's `00D80EA8`. The word counts are 3 and 1×7, but as the installers write them (X3), not as authored: `.data` holds 0 at `+0x20` |
| X2 | §2 the object is `0x28` bytes | **survives**. All eight deleting destructors (slot 0: `006B8790`, `006B8750`, `006B8710`, `006B8850`, `006B8890`, `006B8810`, `006B88D0`, `006B87D0`) pass `0x28` |
| X3 | §3 the CRT slots and each installer's steps | **survives**. `008C43E8`–`008C4420` hold the eight installers. Each calls `006B8D20`, then, **only on a zero return**, adds its count to `02E522E0` and writes it to `+0x20` (for example `00167104 add [02E522E0], 3` / `0016710B mov [01F2EBE8], 3`). It then stores its vtable over `+0x00` and tail-jumps to the `atexit` wrapper |
| X4 | §3 the registrar's returns | **survives**. `test r10, r10` on `+0x08`, then `lea eax, [r10 + 0x11]` returns `0x11` for no name (`r10` is 0 there); `mov eax, 0x12` on a name match; `02E522D0` is read and written, and the new object is linked at `+0x10` |
| X5 | §3 the budget ends at 10 | **survives** (3 + 7 × 1) |
| X6 | §4 each class's slot-2 evaluator | **survives**. It is `006B9120`, `006B90A0`, `006B9070`, `006B93D0`, `006B9410`, `006B93A0` and `006B9450`. `LOW_RES_PARTICLES` holds the base's `006B9050`, which reads `+0x24` |
| X7 | §4 the evaluators' constants | **survives**. `SKINNING_ENABLED` 0x78; `INDICES_16BIT` `byte [+0x4c] == 0xc`; `ORTHO_CAMERA` reads `+0x6c` against the float `0x3C23D70A` (0.01); `NUM_LIGHTS` reads effect `+0x04` / `+0x70`; `SHADER_LOD_LEVEL` `+0x74`; `LOD_BLEND` `+0x40`, `+0x20`, `+0x30` |
| X8 | §4 `NUM_LIGHTS` packs `((10n + 35) >> 5) << 2` bytes | **survives** at the level of its constants (`0x23`, a right shift and a ×4) |

**Narrowing (X1, X3).** §3 says an installer that gets a non-zero registrar return loses "its place in the registry and
its words in the budget". The bytes add a third loss: the word count at `+0x20` is 0 in the image and is written only
on that same zero branch, so such a switch would also carry 0 at `+0x20`. The teardown subtracts that field. No
shipped switch takes the branch, since all eight names are distinct. Tier 1 (static).

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-context-switch-axes-and-the-variant--ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `006B8D20` | 132 B | returns 0x11 when qword `+8` of `rcx` is null; otherwise it walks the list from qword `02E522D0` through each node's qword `+0x10`, comparing the node's C string at qword `+8` with that of `rcx` byte by byte, and returns 0x12 on an equal string; when no node matches it stores the old head at qword `+0x10` of `rcx`, makes `rcx` the head (qword `02E522D0`) and returns 0 | `006B8D2B`, `006B8D60`, `006B8D77`, `006B8D80`, `006B8D96` |
| `006B8F70` | 222 B | counts the list from qword `02E522D0` through each node's qword `+0x10`; when the count equals dword `[rdx]` it only copies; otherwise, for a non-zero count it allocates count*8 bytes with `0017D260`(count*8, 8), returns 0xD when that is null and zeroes the buffer (`rep stosq`) when it is not; it frees the old qword `[rdx+8]` with `00584730` when that differs from the new buffer, is non-null and dword `[rdx]` has `0x80000000` clear, then stores the new buffer (null for a zero count) at qword `+8` and the count at dword `[rdx]`; it finally writes each node pointer, in list order, to consecutive qwords from qword `[rdx+8]` and returns 0 | `006B8F95`, `006B8FA5`, `006B8FBC`, `006B9005`, `006B9020` |
