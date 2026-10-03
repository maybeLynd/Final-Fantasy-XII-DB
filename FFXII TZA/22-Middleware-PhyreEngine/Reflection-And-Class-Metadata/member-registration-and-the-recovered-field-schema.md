---
system: Phyre member registration and the recovered field schema
category: 22-Middleware-PhyreEngine
status: AUDITED
owner_layer: CodeDomain:Phyre.Reflection
evidence_tier: 1
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
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 0
---

# Phyre member registration and the recovered field schema

> The engine writes down its own field list — name, byte offset and type, for every field it
> exposes. This document reads that list back out: **680 fully-resolved field records over 246 classes**,
> with real struct offsets a modder can use directly. It also answers **BJ-4**, whose premise was
> wrong: there is no type-id constant.
>
> **Updated 2026-09-02, second pass (BL-4 closed):** every argument at **680 of the 682** call
> sites is now resolved - class, field name, offset, type and attributes - across **246 named
> classes**. The two that are not are the two that also sit outside a one-time-init guard.

## 1. What the player sees

Nothing directly — but almost everything indirectly.

When you save your game, FFXII has to write out a living scene: where every object is, which mesh
it is using, how bright each light is, what the physics body weighs. When you load it back, all of
that has to land in the right place. When an animation moves a character's hand, something has to
know that "the hand's world matrix" is a specific 8 bytes at a specific place inside a specific
object. When a script asks for a property by name, something has to turn that name into a memory
address.

All of that runs on one thing: **the engine keeps a written description of its own data.** For
each kind of object it knows about, it records the list of fields — the field's name as the
programmer wrote it (`m_intensity`, `m_localToWorldMatrix`, `m_mass`), exactly how far into the
object that field sits, and what type it is. Nothing in the game reads a field "directly"; the
save system, the resource binder, the animation binder and the script bridge all walk this list.

That list is normally invisible. It is not in a data file you can open — it is assembled in memory
by code, the first time each kind of object is touched. **This document recovers it.** The result
is a real field map: for example, a light's brightness is a 4-byte float 0x30 bytes into the
light object, its outer cone angle is the float just before it at 0x2C, and the matrix that places
it in the world is a pointer at 0x10.

For anyone editing the game, that is the difference between guessing at an offset and knowing it.

No addresses in this section beyond those — everything below is exact.

## 2. Native mechanism

### One call per field

Every reflected field is registered by a single call to `00632960`, which builds one
`PClassDataMember` record and attaches it to the owning class descriptor:

```c
FUN_00632960(&record, &classDescriptor, memberType, "m_animationSet", 0x20, 0x12, 0, ctx);
//            ^        ^                 ^           ^                 ^      ^
//            record   owning class      PType*      field name        offset attributes
```

There are **682 such call sites** in the binary. **680 of them resolve completely** - field name,
byte offset, attribute word, owning class and field type - over **246 named classes** and **109
distinct field types**. The two that do not are `BL-3`.

**The fifth argument is a byte offset, not a size** — see §8, this is the correction that answers
BJ-4. **The sixth is an attribute bitfield, not a type id.** The field's type is the third
argument, a pointer.

### The type of a field is a pointer, not an enum

Phyre has no type-code enum. A field's type is a pointer to a `PType` object:

- **primitive fields** point at a `PTypeDefault<T>` singleton, where `T` is a C++ primitive. The
  RTTI names carry the MSVC mangling code for `T`, so the primitive set reads straight out:

  | code | C++ type | fields |
  |---|---|---:|
  | `I` | `unsigned int` | 224 |
  | `M` | `float` | 96 |
  | `E` | `unsigned char` | 29 |
  | `H` | `int` | 26 |
  | `G` | `unsigned short` | 19 |
  | `_N` | `bool` | 16 |
  | `F` | `short` | 1 |
  | | **total primitive fields** | **411** |

- **object fields** point at the class descriptor of the field's own type — `VPWorldMatrix`,
  `PScene::VPNode`, `PPhysics::VPPhysicsMaterial` — so the schema is self-describing and
  navigable.

Only **109 distinct type objects** serve all 682 fields, because the primitives are shared
singletons: 411 of the fields are primitives drawn from just seven `PTypeDefault<T>` objects.

### It is built lazily, and that is not a detail

**680 of the 682 registration calls sit inside a one-time-initialisation guarded region** — the
compiler's C++11 "magic static" block. 246 of the 248 functions that register fields are lazy
holders. So a class's field list does not exist when the game launches; it is assembled the first
time anything asks that class about itself.

This is the consumer side of the machinery documented in
[`../../24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md`](../../24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md),
and it is *why* that machinery exists at this scale: three quarters of the engine's 1,681 lazy
statics are reflection metadata. It also means the field list is not readable from the file image
— you must run the game to the point where the type has been touched, or read the registration
code as this document does.

**The two calls that are not inside a guarded region** are the honest exception and are recorded
in §7.

### The record it builds

`00632960` fills a `PClassDataMember`, then hands it to the class descriptor through a virtual
call. The shared base constructor `00632FB0` does the intrusive-list and name work:

```c
longlong FUN_00632fb0(longlong self, void *owner, char *name, uint attrs) {
    *(longlong *)(self)        = self;          // intrusive list node, self-linked = empty
    *(longlong *)(self + 0x08) = self;
    *(void **)  (self + 0x10)  = owner;         // the owning class descriptor
    *(char **)  (self + 0x18)  = name;
    *(uint *)   (self + 0x20)  = attrs;
    if (attrs & 1) {                            // bit 0: the name is not a literal
        n = strlen(name + 1);
        p = alloc(n + 2, 1);
        if (p) memcpy(p, name, n + 2);
        *(char **)(self + 0x18) = p;            // own a private copy
    }
    return self;
}
```

**Bit 0 of the attribute word means "the name string was heap-copied; free it on teardown."** That
closes a loop with the sibling document, which reached the same bit from the opposite end: its
teardown helper `00633240` tests `(*(byte *)(self + 5) & 1)` — byte offset 0x28 of the member
record, which is exactly `self + 8 + 0x20` here — before releasing the string. Construction and
destruction agree, derived independently.

**Bit 0 is never set at any of the 680 sites where the attribute word resolves**, because every
field name in this binary is a string literal in `.rdata`.

### The container: a class descriptor's six lists, and what four of them hold

A class descriptor owns **six** intrusive lists. The authoritative layout is its constructor
`00632D80`, which sets every field in one place — this is the derivation that should be trusted
over any transcription:

```c
PClassDescriptor *ctor(PClassDescriptor *p, void *registry, const char *name,
                       u32 instanceSize, u32 alignment, void *baseChain, u32) {
    selflink(p + 0x50);                       // list: this descriptor's own registry node
    selflink3(p + 0x08);                      // a three-pointer head at +0x08/+0x10/+0x18
    *(u32 *)(p + 0x20) = 0;
    *(void **)(p + 0x28) = 0;
    *(u32 *)(p + 0x3C) = alignment;
    *(const char **)(p + 0x30) = name;        // THE CLASS NAME
    *(u32 *)(p + 0x38) = instanceSize;        // the storage budget AttachMember checks
    *(void **)(p + 0x40) = 0;  *(void **)(p + 0x48) = 0;
    selflink(p + 0x60);                       // list: unidentified
    *(void **)p = Phyre::PClassDescriptor::vftable;
    *(void **)(p + 0x70) = registry;
    *(void **)(p + 0x78) = baseChain;         // the base-class chain
    selflink(p + 0x80);                       // list: FIELDS
    selflink(p + 0x90);                       // list: METHODS
    selflink(p + 0xA0);                       // list: SCRIPT BRIDGE
    selflink(p + 0xB0);                       // list: unidentified
    ...
}
```

`005A7ED0` calls it as
`ctor(this, registry, "PAnimatableComponent", 0x108, 8, &DAT_02e4e720, 8)` — so the class name and
the instance size arrive as plain arguments, and `0x108` is what `AttachMember` later compares a
field's offset against.

**`+0x50` — this descriptor's own node in a global registry of class descriptors.** Not a list the
descriptor owns, but the link by which it is *held*. Proved by `0063D640`, which unlinks
`cls+0x50` and elsewhere converts a node back to its descriptor by **subtracting 0x50**.

**`+0x80` — the fields.** The 682 registrations of this document.

**`+0x90` — the methods.** The same `PClassDataMemberBase` record shape carries methods, and there
are **220 such constructions that are not field registrations, 216 with a recovered name**. The
names settle it without ambiguity: `playOnce`, `playLooping`, `playOnceByName`, `stop`,
`getAnimationTime`, `hasOneShotAnimationFinished`, `setSpeedForSlot`, `getTargetName`, `GetTime`.
187 of the 220 come from `Phyre.Reflection.GeneratedMetadataRoutine` functions. The insert was
traced instruction by instruction in `005AD8F0`, immediately after the record is built:

```
call 00632FB0                 ; build the record for "playOnce"
mov  rcx, [rip+...]           ; the owning descriptor
lea  rdi, [rcx + 0x90]        ; head  <- the METHOD list
mov  rax, [rdi + 8]           ; tail
mov  [rip+...], rdi           ; record.next = head
mov  [rip+...], rax           ; record.prev = tail
mov  [rax], r14               ; tail->next = record
mov  [rdi + 8], r14           ; head.tail = record
```

**`+0xA0` — the script bridge.** The remaining 31 record constructions come from
`Phyre.ScriptVM.ReflectionBridge` functions, and `005B2860` builds one named `"GetGlobalTime"` and
links it into `descriptor + 0xA0` by the same idiom. So the engine keeps *two* callable lists: the
reflected C++ methods, and the subset published to the script VM.

A writer census over the whole binary corroborates the two traced lists — **but only those two,
and only by domain composition.** Scanning for the insert idiom (a `lea` materialising `[base + H]`
followed by a store through that register at `+8`, excluding the empty-list self-link a
constructor emits) gives:

| head | writers found | dominated by | usable? |
|---|---:|---|---|
| `+0x80` | 5 | **`0062EFD0` AttachMember** — the positive control | yes |
| `+0x90` | 52 | **47 `Phyre.Reflection.*`**, led by `GeneratedMetadataRoutine` | yes |
| `+0xA0` | 10 | **`Phyre.ScriptVM.ReflectionBridge`**, five of the eight Phyre writers | yes |
| `+0x50`, `+0x60`, `+0xB0` | 7, 4, 2 | — | **no — see below** |

**The scan has no descriptor specificity, and the last row is noise.** It matches *any* structure
with a self-linked pair at that displacement. All six candidates it offered for `+0x50`, `+0x60`
and `+0xB0` were opened and none is a class descriptor: an EASTL list container constructor
(`"EASTL list"`), two Steam callback registrars (`CCallback<CSteamAchievements,…>`), a
`PPFX::CTinyEffect` constructor, and a `Phyre::VTS::ScreenState*` constructor. The `+0x90` and
`+0xA0` rows survive **only** because their domain composition points at Phyre reflection *and*
each has a direct instruction-level trace behind it; without the trace they would carry no more
weight than the discarded rows.

> **THE POPULATION, NAMED — 2026-09-22 (FABLE), on
> `OPUS-REQ-FABLE-NAME-THE-POPULATION-BEHIND-BL8-WRITER-CENSUS`.** OPUS could not rebuild this table
> and asked what it ran over. **It ran over the whole binary — every listed body — and the filter is
> the INSERT IDIOM described above, not a tag and not a bare displacement.** The tag columns are a
> *description of what the survivors turned out to be*; they were never a filter. **That is why
> restricting to `Phyre.Reflection`/`Phyre.ScriptVM`-tagged bodies and then looking for writes
> returns zero** — the generated routines that register methods do not themselves write `+0x90`;
> the idiom does, in the body that links the record.
>
> **Reproduced 2026-09-22 in shape and domain composition, but NOT to the exact counts, and the
> prose above is why.** Scanning for `lea <reg>, [base + H]` followed by a qword store through that
> register at `+8`, skipping the self-link, over all listed bodies:
>
> | head | published | rebuilt | composition of the rebuilt set |
> |---|---:|---:|---|
> | `+0x50` | 7 | 10 | untagged 9 |
> | `+0x60` | 4 | 5 | untagged 5 |
> | `+0x80` | 5 | 7 | untagged 6 |
> | `+0x90` | **52** | **47** | **`Phyre.Reflection.*` 39**, `Phyre.ScriptVM.*` 4 |
> | `+0xA0` | **10** | **9** | **`Phyre.ScriptVM.*` 6**, `Phyre.Reflection.*` 2 |
> | `+0xB0` | 2 | 1 | untagged 1 |
>
> **The character reproduces exactly — `+0x90` dominated by Phyre reflection, `+0xA0` by the script
> bridge, the other four small and untagged — and the counts do not.** The difference is the
> instruction window between the `lea` and the store, which the description above does not state; a
> tight window (stopping at the first call) collapses `+0x90` to 3. **So the instrument is
> recoverable in kind and not in detail, and that is a defect in this paragraph rather than in the
> finding**: `+0x90` and `+0xA0` rest on the instruction-level traces at `005AD8F0` and `005B2860`,
> which is what the table below already says, and those are unaffected.
>
> **And the census has ALREADY been pointed at `+0x60` and `+0xB0` — that is the next paragraph, and
> the answer is negative.** The rebuilt sets name them: `+0x60` is `001D9400`, `002E3110`,
> `003649A0`, `00474710`, `0078B9D0`; `+0xB0` is `00201EB0`. Two were opened as a check and neither
> is a class descriptor or a metadata routine — `001D9400` is an 878-byte body owned by `Resource`
> and `00201EB0` is 1,955 bytes and untagged, both far outside the `0063…` descriptor band. *So the
> instrument OPUS wanted to build for those two lists exists, has been run, and does not isolate
> them.*

~~**`+0x60` and `+0xB0` are still not identified** (BL-8)~~ *(2026-09-25, FABLE, Claude Opus 5.5: `+0x60` is the
`PAnnotatable` base, i.e. the annotation list. `+0xB0` is still unnamed, with no insert found. See the
[descriptor contract](CONTRACT-phyre-class-descriptor.md) §14 item 1.)* One useful negative was established
about them. Every function appearing in any slot of a class-descriptor vtable was scanned for a
reference to `[this + 0x50]`, `[this + 0x60]` or `[this + 0xB0]`: **none touches any of them.**
That query has a passing control — the identical scan for `[this + 0x80]` returns slot 8,
`AttachMember`, plus two neighbours. So whatever fills those two lists does so through
**non-virtual code**, not through the descriptor's own interface, which is how the field, method
and script lists are all reached.

A second attempt anchored on real descriptor *objects* — every rip-relative reference into the
interior of a known class-descriptor global at each list offset — returns 8 functions for `+0x60`
and 8 for `+0xB0`, dominated by `Phyre.Reflection.*`. **Those lists are not reported here as an
answer**, because reading the candidates shows the instrument's own false-positive mode: two of
them (`00630340`, `00630490`) are magic-static accessors for unrelated `PType` singletons that
happen to live at an address coinciding with some descriptor's `D + offset`. Descriptors are ~~about~~
~~0x110 bytes~~ `0x100` bytes *(corrected 2026-10-02, OPUS: 90 pairs of static descriptors sit exactly `0x100` apart; `0x140` is `PClassDescriptorDynamic`, CONTRACT-phyre-class-descriptor.md PCD-3)* and packed in `.data`, so an interior address can be the *start* of a different
global, and this scan cannot tell the two apart. `+0x60` is cleared at destruction by the generic
list-unlink helper; `+0xB0` is unlinked by the destructor's fourth walk. Neither has a writer this
document can name.

**How the destructor treats them tells you which records are heap-allocated.** The `+0x90` and
`+0xA0` walks free each node — and the free is gated on **attribute bit 0** of that node, the same
"the name was heap-copied" bit as fields:

```c
for (node in list) {
    if (node->attrs & 1) {                    // a dynamically-created record
        unlink(node);
        if (node->attrs & 1) aligned_free(node->name);
        aligned_free(node);
    }
}
```

Statically-registered records have bit 0 clear and are only unlinked, never freed. ~~That is why the~~
~~field list at `+0x80` is unlinked without a single free: **every one of the 682 field records is a~~
~~static object.**~~ *(Qualified 2026-09-27 (FABLE, Claude Opus 5.5), on
`ASTRA-RETURN-FABLE-DESCRIPTOR-MEMBERSHIP-PROVENANCE`.)*
- *A free proves heap ownership, which is what the `+0x90`/`+0xA0` reading below uses. An unlink without a free
  proves only that the destructor does not own the node.*
- *Static, external, pool or arena storage all fit that. So the `+0x80` walk's lack of a free does not show that the
  682 field records are static objects.*
- *Where those records live rests on how they are registered, not on the teardown; this paragraph does not re-read
  that. After the drains every node is unlinked, so none stays in the list either way.*

### An independent check on the offsets: the default-value constructor

Descriptor virtual slot `+0x50` builds a default-initialised instance of the class. For
`PRendering::VPLight` that is `006BE990`, and every value it writes lands on an offset this
document recovered from the registration side — a function with no connection to registration
agreeing field for field:

```c
p[0x00..0x0F] = 0.5f, 0.5f, 0.5f, 1.0f     // the base-class part, below the first reflected field
p[0x10] = 0;  p[0x18] = 0;                 // m_localToWorldMatrix, m_shadowCaster  -> null pointers
p[0x20] = &PTR_vftable_01f2ed48;           // m_lightType
p[0x28] = 0.0f;                            // m_innerConeAngle
p[0x2C] = 0x3EC90FDB;                      // m_outerConeAngle  = 0.3926991 rad = 22.5 degrees
p[0x30] = 1.0f;                            // m_intensity
p[0x34] = 0.0f;                            // m_innerRange
p[0x38] = 0x7F7FFFFF;                      // m_outerRange      = FLT_MAX
p[0x3C] = 0.0f;                            // m_scatteringIntensity
```

Every one of those is semantically right for the field this document names at that offset: a cone
angle that is a real angle, an intensity of 1, a range of FLT_MAX, and null object pointers. **A
wrong offset table would not produce sensible defaults at every slot.** It is still static
evidence, so it does not close BL-7 — but it is a second derivation from an independent function,
which is worth more than another reading of the same one.

### How the engine uses the record — the attach path

The last thing `00632960` does is call virtual slot `+0x40` on the owning descriptor. **1,186 of
the 1,187 class-descriptor vtables carry the same function there, `0062EFD0`**, so this is the
single attach path:

```c
int AttachMember(PClassDescriptor *cls, PClassDataMember *rec, void *ctx) {
    int capacity   = *(int *)(cls + 0x38);      // the class's storage budget
    int used       = *(int *)(cls + 0xF8);
    int baseOffset = *(int *)(cls + 0xF4);      // where this class's own fields start
    int fieldOff   = *(int *)(rec + 0x48);      // THE FIELD OFFSET
    int width      = FieldStorageWidth(rec, ctx);

    if (capacity < (fieldOff - baseOffset) + width + used) return 5;     // does not fit
    if (*(void **)(rec + 0x20) == NULL)                    return 0x15;  // no name
    if (FindMemberByName(cls, name) != NULL)               return 0x12;  // duplicate name

    // link rec+0x08 into the circular list whose head is at cls+0x80, tail at cls+0x88
    head = *(void **)(cls + 0x88);
    node = rec + 0x08;
    *(void **)(rec + 0x10) = head;
    *(void **)node         = cls + 0x80;
    *head                  = node;
    *(void **)(cls + 0x88) = node;
    return 0;
}
```

Three things fall out of that, none of which needed a new assumption.

**It arithmetically validates the offset.** `capacity < (fieldOff - baseOffset) + width + used`
subtracts a base offset from the fifth argument and compares the result against a byte budget.
**A size cannot be used that way** — this is independent confirmation of the BJ-4 answer, from a
function that has nothing to do with registration.

**It confirms bit 1 means "pointer".** `FieldStorageWidth` (`0063C0C0`) reads the attribute word
at `rec+0x28` and, when **bit 1** is set, yields **8** — a pointer — instead of the type's own
inline size. The type's inline size is read from the type object at `type+0x38`, or from its
virtual slot `+0x08` when it has a dynamic size:

```c
int FieldStorageWidth(PClassDataMember *rec, void *ctx) {   // 0063C0C0
    PType *t     = *(PType **)(rec + 0x30);
    uint   attrs = *(uint *)(rec + 0x28);
    int inlineWidth = t->vslot08() ? ctx->vslot10(t->vslot08()) : *(int *)(t + 0x38);
    int ptrWidth    = ctx->vslot08();          // NOT a literal 8 - the CONTEXT states it
    void *d         = rec->vslot08();          // the RECORD's virtual, not the type's
    int  isDynamic  = (d != NULL) && (*(int *)((char *)d + 0x5C) == 2);
    if ((attrs >> 1 & 1) | (~(attrs >> 6) & isDynamic)) return ptrWidth;
    return inlineWidth;
}
```

**Corrected 2026-09-19 (OPUS).** The earlier transcription of this body said `return /* pointer
width */ 8` and left `isDynamic` undefined. Both are now read off `0063C0C0` directly, and both
corrections matter:

* the pointer width is **`ctx->vslot08()`**, supplied by the context the query is made against
  (`0063C106: call qword ptr [rax+8]` with `rcx = rdx = ctx`)~~, not a constant in this function~~, and a literal 8 when `ctx` is null *(corrected 2026-10-02, OPUS: `0063C0D3` jumps to `0063C14C`, which loads `mov eax, 8` at `0063C17D`)*.
  So this function answers "how wide is this field **in that context**", and a context is free to
  answer 4. It is therefore **not** on its own an authority for the in-memory layout;
* `isDynamic` is `rec->vslot08() != NULL && that->[0x5C] == 2` — a virtual on the **record**
  (`0063C10F: call qword ptr [rdx+8]` with `rcx = rbx = rec`), not on the type.

**And the second clause is inert for every field in this schema.** All 680 registrations call
`00632960`, which installs member vtable `00D580B0`, whose slot `+0x08` is `005C5230:
xor eax,eax ; ret` — it returns NULL, so `isDynamic` is always 0 and the width reduces to
`bit 1 ? ptrWidth : inlineWidth`. Only the *derived* member class can trigger it: constructor
`00632A10` installs vtable `00D58100`, whose slot `+0x08` is `0016D680: mov rax,rcx ; ret`, and
stores its arg7 at `+0x5C` — the value compared against 2. **No row in this schema is built by
that constructor**, so no field here is dynamic-width. That is a measured negative, not an
assumption, and it is what makes the bit-1 rule safe to apply wholesale.

**It does not read bits 3–4 at all.** That rules out the most attractive remaining hypothesis for
`BL-1` — that those bits select which of the descriptor's lists a field is attached to. They are
not consulted on the attach path.

**And the member list is at `cls+0x80`, not where the sibling document's table implies.** The
duplicate-name check `00597220` walks that same list and follows the base-class chain at
`cls+0x78`, comparing names byte by byte — so a class inherits its bases' fields, and a
duplicate name anywhere in the chain is rejected with `0x12`. The reset helper `0063D550`
re-initialises **six** intrusive lists, at `cls+0x50`, `+0x60`, `+0x80`, `+0x90`, `+0xA0` and
`+0xB0`. See §8 for what that means for the sibling document's layout table.

Return codes, for anyone instrumenting this: `0` attached · `5` would exceed the class's storage
budget · `0x12` a field of that name already exists in the class or a base · `0x15` no name.

### The record's second list, and the class descriptor's other five

A `PClassDataMember` carries **two** intrusive lists. The first, at `+0x08`/`+0x10`, is the class's
member list: `AttachMember` links it in, descriptor virtual slot `+0x48` (`0062F080`) is the exact
inverse and unlinks it, and the member's own teardown `00633240` calls that slot on its owner when
it finds itself still linked:

```c
void ~PClassDataMember(PClassDataMember *self) {
    self->vftable = Phyre::PClassDataMember::vftable;
    if (*(void **)(self + 0x08) != self + 0x08) {          // still attached?
        PClassDescriptor *owner = *(void **)(self + 0x18);
        owner->vslot[0x48](owner, self);                   // DetachMember
    }
    ListClear(self + 0x38);                                // <- the SECOND list
    if (*(byte *)(self + 0x28) & 1)                        // attribute bit 0
        aligned_free(*(void **)(self + 0x20));             // the heap-copied name
}
```

That single body confirms three things derived separately elsewhere in this document — the owner
pointer at `+0x18`, the name at `+0x20`, and attribute bit 0 meaning "free the name" — and it is
the whole of what is currently proven about the second list:

- it is **self-linked empty at construction** (`00632960`),
- it is **never touched by attach or detach**,
- it is **owned**: the destructor clears it through `006B6700`, a generic list-unlink loop, and
  **nine** reflection teardown helpers do the same, one per member-record kind,
- and **nothing in the registration path adds to it** — `00632960` returns the record, and that
  return value is used at ~~**2 of 682**~~ **0 of 682** call sites.
  *(Corrected 2026-09-15 (OPUS). Re-measured with `work/OPUS/ret_used.py`: a byte-level rel32 scan
  finds **682** call sites, matching this page; every one lies inside a listed body and decodes at an
  instruction boundary — 0 unparsed, 0 outside a body — and in none of them is `rax` read before it
  is overwritten or the function returns, over an 80-instruction window. The two sites in `005983E0`
  are typical: `call 00632960` at `0059846E` and `005984E1` is followed each time by
  `lea rcx, [rip+…]` and another call. **Positive control:** the same reader, over 13,993 sampled
  call sites elsewhere in `.text`, finds 4,375 where the next instruction alone reads `rax`, so a
  zero here is a property of these call sites and not of the reader.)*

~~What it holds is **not established** (BL-5). Whether anything in this binary ever puts a node in
it is also not established: the scan built to answer that failed its own positive control, and is
recorded as a failure in §10 rather than as a result.~~ **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): `+0x38`
is the member's annotation list, and every annotation in the image is one `WriteMask`.** Static; details under
`BL-5` in the question list below.

> **BL-5 narrowed, 2026-09-15 (OPUS) — who could possibly fill it.** A node can only be added to a
> member record's `+0x38` by code that holds a pointer to that record. The registration path does not:
> the constructor's return is discarded at **all 682** call sites, measured above. So the only holders
> in this binary are (a) the attach path, which the body above shows touches `+0x08`/`+0x10` and never
> `+0x38`, (b) the destructor and the nine per-kind teardown helpers, which only CLEAR it through
> `006B6700`, and (c) anything that walks the class descriptor's `+0x80` member list and reaches a
> node's `+0x38`. **(c) is the whole remaining search space, and it is not searched here.** *(answered: see the ANSWERED 2026-09-25 block above; 2026-10-02, OPUS)* The row
> stays OPEN: this removes the registration path as a candidate, it does not establish what the list
> holds.

The class descriptor likewise has **six** intrusive lists, at `+0x50`, `+0x60`, `+0x80`, `+0x90`,
`+0xA0` and `+0xB0` — the reset helper `0063D550` re-initialises all six, while the destructor
`00633390` walks only four (`+0x80`, `+0x90`, `+0xA0`, `+0xB0`) and clears `+0x60` through the same
list-unlink helper. Only `+0x80` is identified *(answered: see BL-8 - four of six identified, `+0x60` 2026-09-25; 2026-10-02, OPUS)*. The type's **name** is a plain `char *` at `+0x30`,
read by `006388C0`.

### Types are found by name, and the name hash collides safely

`006388C0` turns a type's name into a hash and looks it up in an ordered tree:

```c
unsigned h = 0x7B5;                       // 1973
for (const unsigned char *p = name; *p; ++p)
    h = h * 0x21 + (*p & 0x1F);           // 0x21 = 33
```

Only the low five bits of each character contribute, so `'a'` (0x61) and `'A'` (0x41) hash
identically — **the registry is case-insensitive for ASCII letters by construction**, and any two
names differing only in bit 5 or bit 6 of a character collide.

That collision is handled, and the handling is visible in the lookup `006311D0`: it walks a
red-black tree comparing the **hash first**, and when two hashes are equal it falls through to a
**byte-by-byte string comparison** and only returns a hit on a full match. The hash is a fast
ordering key, never the identity. This answers **BK-9**.

### What the recovered schema looks like

`PRendering::VPLight`, complete as registered — nine fields, every offset exact:

| offset | field | type | attrs |
|---|---|---|---|
| `+0x10` | `m_localToWorldMatrix` | `VPWorldMatrix` * | `0x12` |
| `+0x18` | `m_shadowCaster` | `PRendering::VPShadowCaster` * | `0x12` |
| `+0x20` | `m_lightType` | `PRendering::VPLightType` * | `0x12` |
| `+0x28` | `m_innerConeAngle` | `float` | `0x10` |
| `+0x2C` | `m_outerConeAngle` | `float` | `0x10` |
| `+0x30` | `m_intensity` | `float` | `0x10` |
| `+0x34` | `m_innerRange` | `float` | `0x10` |
| `+0x38` | `m_outerRange` | `float` | `0x10` |
| `+0x3C` | `m_scatteringIntensity` | `float` | `0x10` |

The floats are exactly 4 bytes apart and the pointers exactly 8; the layout is internally
consistent with no gaps, which is the structural proof that argument five is an offset.

`PRendering::VPMeshInstance`, 17 fields — this is the object behind every piece of visible
geometry:

| offset | field | type | attrs |
|---|---|---|---|
| `+0x08` | `m_localToWorldMatrix` | `VPWorldMatrix` * | `0x0A` |
| `+0x20` | `m_materialSet` | `PGeometry::VPMaterialSet` * | `0x0A` |
| `+0x28` | `m_instanceSegment` | `PGeometry::VPMeshSegment` * | `0x0A` |
| `+0x30` | `m_dynamicMeshInstance` | `PRendering::VPDynamicMeshInstance` * | `0x0A` |
| `+0x38` | `m_bounds` | `PRendering::VPMeshInstanceBounds` * | `0x0A` |
| `+0x40` | `m_lodLevel` | `PLOD::VPLODLevel` * | `0x0A` |
| `+0x58` | `m_flags` | `unsigned int` | `0x08` |
| `+0x5C` | `m_extraFlag` | `unsigned int` | `0x08` |
| `+0x60` | `m_extraZBias` | `int` | `0x08` |
| `+0x64` | `m_farPlane` | `float` | `0x08` |
| `+0x68` | `m_specularIntensity` | `float` | `0x08` |
| `+0x6C` | `m_cubeMapIntensity` | `float` | `0x08` |
| `+0x70` | `m_cubeMapFactor` | `float` | `0x08` |
| `+0x74` | `m_alphaThreshold` | `float` | `0x08` |
| `+0x78` | `m_specialRenderOrder` | `int` | `0x08` |
| `+0x7C` | `m_specialTextureWrapType` | `int` | `0x08` |
| `+0x80` | `m_name` | `VPString` | `0x08` |

`PPhysics::VPPhysicsRigidBodyBase`, 19 fields, including `m_mass` as a `float` at `+0xE4`,
`m_collisionGroup` as an `unsigned char` at `+0xE0`, `m_rigidBodyType` at `+0xE8` and `m_enabled`
as a `bool` at `+0xE9` — two single-byte fields in adjacent bytes, which no accidental reading
would produce.

The full table for all 682 records is `Tools/work/h94/phyre_schema.tsv`.

---

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00632960` | `PClassDataMember_Register` | 165 B | the one registration entry point; **682** call sites |
| `00632FB0` | `PClassDataMemberBase_Construct` | — | intrusive list, owner, name, attribute word; owns the name copy |
| `006388C0` | `PType_FindOrRegisterByName` | 254 B | the name hash |
| `006311D0` | `PType_LookupByHashThenString` | — | red-black walk; hash first, full `strcmp` on a tie |
| `00637440` | registry root accessor | — | supplies the tree root to the lookup |
| `00633240` | `PClassDataMember` teardown helper | — | tests attribute bit 0 before freeing the name |
| `0062EFD0` | `PClassDescriptor::AttachMember` | — | descriptor virtual slot `+0x40` on **1,186 of 1,187** descriptor vtables; validates the offset, links the record |
| `0063C0C0` | `FieldStorageWidth` | — | ~~returns 8 when attribute bit 1 is set, else the type's inline size from `type+0x38`~~ when bit 1 is set returns `ctx->vslot08()`, or a literal 8 when `ctx` is null, else the inline width *(corrected 2026-10-02, OPUS: `0063C100`-`0063C106` and `0063C137`; null context `0063C0D3` → `0063C17D`)* |
| `00597220` | `FindMemberByName` | — | walks `cls+0x80` and the base chain at `cls+0x78`, comparing names |
| `0063D550` | descriptor list reset | — | re-initialises **six** intrusive lists at `cls+0x50/0x60/0x80/0x90/0xA0/0xB0` |
| `00639290` | attach wrapper | — | the one descriptor whose slot `+0x40` differs; skips a `PClassDataMemberDynamicDefault*` sentinel |
| `00633390` | `PClassDescriptor` base destructor | 500 B | the descriptor layout, read in the sibling document |
| `005AD8F0` | heaviest registration function | 5,580 B | 28 guarded statics, registers `m_animationSet` and its siblings |
| `005E5400` | heaviest registration function | 4,088 B | 28 guarded statics |
| `008092FC` | `_Init_thread_header` | 103 B | the guard 680 of the 682 registrations sit behind |
| `0080929C` | `_Init_thread_footer` | 96 B | closes that guard |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02CAD140` | a class descriptor singleton | `.data` object | the worked example's owning class |
| `02CB0A98` | its one-time-init guard | `int` in `.data` | gates the registration block in `005AD8F0` |
| `02CAE660` | a member type object | `.data` object | the `PType*` passed as argument three |

---

## 4. Data structures and formulas

### The registration call

```c
PClassDataMember *PClassDataMember_Register(
        PClassDataMember *record,      // rcx  - storage for this field's record
        PClassDescriptor *owner,       // rdx  - the class the field belongs to
        PType            *memberType,  // r8   - the field's type object
        const char       *name,        // r9   - the field name, a .rdata literal
        uint32_t          offset,      // [rsp+0x20] - BYTE OFFSET of the field in the object
        uint32_t          attrs,       // [rsp+0x28] - attribute bitfield
        int               flag2,       // [rsp+0x30]
        void             *ctx);        // [rsp+0x38]
```

body, exactly:

```c
{
    PClassDataMemberBase_Construct(record + 8, owner, name, attrs);
    record[0x30] = memberType;
    record[0x38] = &record[0x38];  record[0x40] = &record[0x38];   // second empty list
    record[0x00] = Phyre::PClassDataMember::vftable;
    *(uint32_t *)&record[0x48] = offset;
    record[0x50] = 0;
    saved = *(uint32_t *)&record[0x28];
    if (flag2 == 2) *(uint32_t *)&record[0x28] = saved | 2;
    (*(void (**)(...))(*(void **)owner + 0x40))(owner, record, ctx);  // descriptor vslot +0x40
    *(uint32_t *)&record[0x28] = saved;                               // restored afterwards
    return record;
}
```

### `PClassDataMember` layout, from the constructor

```
PClassDataMember
  +0x00  ptr    vftable  = Phyre::PClassDataMember::vftable
  +0x08  ptr    intrusive list node  (self-linked when empty)
  +0x10  ptr    intrusive list node
  +0x18  ptr    owning PClassDescriptor
  +0x20  ptr    name pointer (heap copy iff attrs bit 0)
  +0x28  u32    attribute bitfield
  +0x30  ptr    PType * - the field's type
  +0x38  ptr    second intrusive list, self-linked
  +0x40  ptr    "
  +0x48  u32    FIELD OFFSET inside the owning object
  +0x50  ptr    0
```

### The attribute bitfield

Six values occur across the 680 sites where it resolves:

```
0x00 196     0x02  36     0x08 123     0x0A  39     0x10 207     0x12  79
```

so exactly three bits are ever used (mask `0x1A`), and they split into two independent parts:

```
bit 0  (0x01)   the name is heap-allocated; copy it in, free it on teardown
                -> never set here: all 682 names are .rdata literals
bit 1  (0x02)   the field is stored as a POINTER to another reflected object
                -> never set on a primitive-typed field, at any of the 680 sites
                -> CONFIRMED FROM THE CONSUMER: the attach helper 0063C0C0 returns a
                   storage size of literally 8 when this bit is set, and the type's own   <- corrected 2026-10-02, OPUS - 8 only with a null context (0063C0D3 -> 0063C17D); with one it is ctx->vslot08() (0063C106)
                   inline size otherwise (see "How the engine uses the record" below)
bits 3-4 (0x18) a near-per-CLASS constant: 0x00, 0x08 or 0x10
                -> constant across every field of the class in 243 of 246 classes;
                   three classes mix 0x00 with 0x08, named in section 7
                -> NOT determined by the descriptor template (tested and refuted)
                -> NOT read by the attach path at all
                -> meaning not established, see BL-1
```

The minimal pair that proves bit 1, both fields of `PScene::VPNode`, both matrices:

```
+0x18  m_worldMatrix   attrs 0x12   next field at +0x20   ->  8 bytes  -> a pointer
+0x20  m_localMatrix   attrs 0x10   next field at +0x60   -> 64 bytes  -> stored inline
```

### The type-name hash and its lookup

```c
unsigned hash(const char *name) {
    unsigned h = 0x7B5;
    for (const unsigned char *p = (const unsigned char *)name; *p; ++p)
        h = h * 0x21 + (*p & 0x1F);
    return h;
}
```

```c
// 006311D0, ordered-tree lookup keyed on the hash, exact on the string
node = root;
while (node != end) {
    if      (key->hash < node->hash) go left;
    else if (node->hash < key->hash) go right;
    else {                                  // hash collision or a genuine hit
        cmp = strcmp(key->name, node->name);
        if (cmp == 0) return node;          // only a full string match is a hit
        go (cmp < 0) ? left : right;
    }
}
return NULL;
```

---

## 5. Call chain

```
anything asks a class about itself for the first time
  -> the class's registration function (248 of them; 246 are lazy-static holders)
     -> _Init_thread_header(&guard)                   008092FC
        -> for each field:
             PType *t = <the field type's own lazy accessor>()      <- a nested lazy static
             PClassDataMember_Register(&rec, &classDesc, t, "m_x", offset, attrs, ...)  00632960
               -> PClassDataMemberBase_Construct(...)               00632FB0
                  -> (attrs & 1) ? heap-copy the name : keep the literal
               -> classDesc->vslot[+0x40](classDesc, &rec, ctx)     attach to the class
        -> _Init_thread_footer(&guard)                0080929C
  -> the field list now exists for the process lifetime

consumers, all of which walk the same list:
  -> binary serialisation  (PSerialization::PBinary::*)
  -> the animation channel binder, resolving dotted member paths
  -> the Lua/script property bridge
  -> resource binding
```

**Upstream (who causes this):** the 248 registration functions. The field type of each member is
itself fetched through another lazy accessor, so touching one class can cascade into constructing
the descriptors of every type it mentions.

**Downstream (what this causes):** the class descriptor's member lists, which are what
[`../Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`](../Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md)
resolves dotted member paths against — that document is the consumer side of this schema — and
what the serialiser walks.

**Do not confuse with:**

- **The class descriptor's own construction.** Descriptor singletons are built by generated CRT
  initializers at process start; that is the subject of
  [`class-descriptor-and-metadata-system.md`](class-descriptor-and-metadata-system.md). **The field
  lists inside them are not** — those are lazy, and §8 records that as a correction.
- **`PNamedSemanticDescriptorForType`.** A distinct type family used for enum-like semantics
  (`VPLightType`, `VPInputKeySemantic`); it appears as a member *type* here but registers through
  its own path.
- **RTTI.** MSVC RTTI names the C++ classes; this system is Phyre's own parallel description and
  carries what RTTI does not — field names, offsets and types.

---

## 6. Modding notes

- **Best intervention point: the field offsets themselves.** The tables in §2 and
  `Tools/work/h94/phyre_schema.tsv` give exact byte offsets inside live engine objects. Once you
  have a `VPLight *`, its intensity is a `float` at `+0x30` and needs no reflection call at all.
  That is the fastest and least invasive way to read or change engine state.

- **Prefer the offset to the name lookup.** Going through `PType_FindOrRegisterByName` costs a
  hash, a tree walk and a `strcmp`, and it can only find a type whose descriptor has already been
  built. The offsets are constant for this binary.

- **Regenerates itself:** the member records. Do not write into a `PClassDataMember`; rebuild
  nothing. Changing `+0x48` on a record changes where every consumer thinks the field lives — the
  serialiser included, which will then write your save file wrong.

- **Breaks if:** you read a field list before its class has been touched. It does not exist yet,
  and the descriptor's member lists are empty rather than absent, so the failure is a silent empty
  iteration rather than a crash.

- **The lazy hazard applies here in full.** These registration functions are exactly the ones that
  hold one-time-init guards. A detour inside one that returns early or throws strands the guard at
  `-1` and hangs the process — see the sibling document. **Hook the accessor's caller, not the
  registration function.**

- **XIIOnline.** Of the 707 lazy-static holder functions, **149 of the 150 that carry a subsystem
  owner are Resource-owned** — which is precisely where a shared-world mod wants to hook. Treat
  every Resource-owned hook site as potentially inside a one-time-init region and check before
  placing a detour. (**BK-8**.)

- **Mod compatibility.** No authored data is involved; this is all code-driven. Two mods reading
  offsets cannot conflict. Two mods hooking registration functions can, because they serialise on
  the single one-time-init lock.

---

## 7. What is not known

- [x] **RM-1** — The 186 member registrations the field schema still has not harvested: 140 array-member sites (`00632A10`) outside the 19 classes §20 re-tiled, 25 fixed-size sites (`00632A70`) and 21 enum sites (`00632BE0`). Which store rows do they land on, and which declared gaps do they fill?
  **ANSWERED 2026-09-27 (OPUS):** all 215 registrations of the three constructors are accounted for in the store. Array: 96 on named rows and 69 template self-registrations (`m_els` / `m_u`). Fixed-size: the math templates and `RenderTarget[8]` are carved, and 19 named rows carry element type and count. Enum: the 14 D3D11 fields are carved, and the 7 Phyre enums are 4-byte ints (value type `01F2E550`; a6 is the attribute word). Corrections on the way: three fixed-size widths, three enum rows, and PString `+0` as an 8-byte tagged `m_buffer`. Scripts and records: `_index/candidates/rm1-array-members/`, `rm1-part3-consumer-check.md`, `rm1-close-consumer-check.md`. Opened 2026-09-27 (OPUS), §20.
- [x] **BL-1** — What bits 3–4 of the attribute word (`0x00` / `0x08` / `0x10`) mean. Now
  established *negatively*, which is progress: they are **not** the descriptor template kind
  (tested and refuted), they are **not** read on the attach path at all, and they are **not**
  strictly per-class — 243 of 246 classes are homogeneous and three are not:
  `PGeometry::VPDataBlockD3D11` and `PGeometry::VPIndexDataBlockD3D11`, each pairing an `0x08`
  offset-into-a-buffer field with an `0x00` size field, and `PHierarchy::VPOctreeWorld`, four
  `0x00` value fields against two `0x08` octree pointers.
  *Narrowed 2026-09-26 (FABLE, Claude Opus 5.5): the bits are persisted into every shipped file's schema.* The
  packed namespace's member attribute word `w4` carries the runtime word unchanged for 18,934 of the 19,301 member
  records that join this page's schema by class and member name. That includes every `0x08` and `0x10`. See
  [the file-side schema page](../Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md), whose
  `w4` reading this corrects. So a meaning for bits 3–4 has to hold for the exporter as well as the runtime.
  - The file adds two bits the runtime census never sees. Bit 5 is always paired with bit 4 (`0x30`) and is only on
    enum-typed fields.
  - An image-wide sweep for any mask on a `+0x28` word that covers bit 3 or 4 finds 28 sites, with `0063C0C0`'s
    bit-1 test as the control. 27 are wide masks: twelve `0x7FFFFFFF` count masks, bit clears such as `0xFFFFFFFE` and
    `0xFFFFFCFF`, and `0x7F`/`0x0F` value masks. The one hit in the reflection range, `006361C0`, *clears* bit 0. The
    only narrow test, `test byte [+0x28], 0x10`, is in battle-formula code on another structure.
  - The consumer, if there is one, is therefore not a mask test on the runtime member.
  - *Not claimed:* what the bits mean. ~~*(NO ADMISSIBLE SOURCE (label), reviewed and signed 2026-09-26 by OPUS; see the register row BL-1.)*~~ *OUT OF EVIDENCE BOUNDARY, 2026-09-27 (FABLE, Claude Opus 5.5): FRONTIER's batch-K Extension 2026-09-27f classes an identifier name by its carrier, the unshipped source / `FF12X64.pdb`; OPUS's signature carries. See the register row BL-1.*
- [x] ~~**BL-2** — the `flag2` argument at `[rsp+0x30]`.~~ **ANSWERED for this binary.** `flag2`
  is **`0` at all 680 resolved sites**, so the `if (flag2 == 2)` branch in `00632960` — which
  would set attribute bit 1 for the duration of the attach call and restore it afterwards — is
  **dead code here**. Why the transient set exists at all is a PhyreEngine question, not an
  FFXII one.
- [x] **BL-3** — The two registration calls that are *not* inside a guarded region. They are also
  the only two sites whose arguments do not resolve, which is consistent with their being reached
  differently, but that is not proof.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BL-3): they are not registrations. They are
  the two subclass constructors calling the base constructor with their own parameters.* The two rows of
  `phyre-field-schema.tsv` with every value empty are:
  - **`00632A41` in `00632A10`**, the `Phyre::PClassDataMemberArray` constructor (vtable `00D58100` by RTTI; §6 of the
    sibling page). It has 165 callers.
  - **`00632B89` in `00632B30`**, whose post-call vtable store `00D58358` is RTTI `Phyre::PClassDataMemberDynamic`. It
    has one caller, `0063942C` in `006393A0`.

  Both forward stack arguments straight into `00632960` (for example `00632B53`–`00632B85`) and then install their own
  vtable. The arguments cannot resolve at those sites because they are the constructor's parameters, and no guard
  surrounds them because the guard belongs to their callers. **The laziness claim therefore holds for all 680 true
  registration sites**; the census counted two base-constructor calls as registrations.
- [x] ~~**BL-4** — the 89 sites whose owning class did not resolve and the 53 whose type did not.~~
  **CLOSED.** They were never missing data — they were argument values a backward scan could not
  follow. A forward abstract interpreter resolves **680 of 682 sites completely**, agreeing with
  the earlier pass on every value it had already recovered and adding 491 more. See §8.
- [x] **BL-5** — What the second intrusive list at record `+0x38` holds. **ANSWERED 2026-09-25 (FABLE, Claude
  Opus 5.5): the member's annotation list; the image attaches 70 annotations, all `WriteMask = 0x7FFFFFFF` on an
  `m_count`, and the class's `+0xD0` data mask reads them.**
  - **The type.** The RTTI base-class table of `PClassDataMember` (vtable `00D580B0`) puts `PAnnotatable` at
    `+0x38`, and `PClassDescriptorDynamic` puts it at `+0x60`. `006B6700` drains both.
  - **The filler.** `006B67D0` links an annotation's node (annotation `+8`) into the list in `rcx`. Its 70 calls each
    attach one annotation built by `006B66C0` or `006315B0` (a `PAnnotationWithValue<unsigned>`, vtable `00D32D50`).
    The key is the static `02CF8570`, built by `006B66F0` with the name `"WriteMask"`. The stored value is
    `0x7FFFFFFF`. The census script `members/annot_census.py` prints 69 on members named `m_count`,
    plus one more `0x7FFFFFFF` built in `00635DC0`.
  - **Why the earlier searches found no filler.** The registrars address the static member's `+0x38` RIP-relative
    (`lea rcx, [rip + member+0x38]`, e.g. `005B503E`). They never use the constructor's return and never walk a list,
    and most of them lie outside `0x630000`–`0x670000`.
  - **The reader.** `00639C80` finds the annotation with `006B67F0` (key compare at annotation `+0x18`) and copies its
    value into the class's `+0xD0` mask at the member's bytes. `0xFF` is used when there is none. See the
    [descriptor contract](CONTRACT-phyre-class-descriptor.md) §14b.
  - **So `m_count`'s bit 31 — the "borrowed" flag of a counted buffer — is excluded from the data mask.**

  *History — the earlier state of this item:* **Structurally answered,
  semantically open.** Proven: self-linked empty at construction, never touched by attach or
  detach, and *owned* — the member destructor clears it through the generic list-unlink helper
  `006B6700`, as do nine reflection teardown helpers, one per member-record kind. Not proven: what
  goes in it, or whether anything in this binary ever puts a node in it at all. Nothing on the
  registration path adds to it, and the return value of `00632960` is used at only 2 of 682 sites.
  The scan built to settle it failed its own positive control (§10).
- [x] **BL-8** — The class descriptor's six intrusive lists. **Four of six are now identified:**
  `+0x50` this descriptor's own node in a global registry of class descriptors, `+0x80` the
  fields, `+0x90` the **methods** (220 non-field record constructions, 216 named — `playOnce`,
  `stop`, `getAnimationTime`), `+0xA0` the **script bridge** (31 records from
  `Phyre.ScriptVM.ReflectionBridge`, e.g. `GetGlobalTime`). **`+0x60` and `+0xB0` remain
  unidentified.** Established negatively, with a passing control: **no class-descriptor virtual
  method touches `+0x50`, `+0x60` or `+0xB0`** — the identical query returns `AttachMember` for
  `+0x80` — so whatever fills them does so through non-virtual code rather than the descriptor's
  own interface. Two instruments were built for the positive question and **both were rejected**:
  one had no descriptor specificity at all, the other misattributes unrelated globals that begin
  at a descriptor's interior address.
  **PARTIAL 2026-09-25 (FABLE, Claude Opus 5.5): `+0x60` identified by type rather than by writer.** The RTTI base-class
  table puts `PAnnotatable` at descriptor `+0x60` and at member `+0x38`, and `006B6700` drains both, so `+0x60` is
  the class's **annotation list**. No annotation is ever attached to a descriptor: all 70 calls of the annotation add
  `006B67D0` target members. **`+0xB0` is still unnamed.** No insert into it appears in the register-formed,
  RIP-relative-head or direct-tail-store shapes, which have passing controls. The detail is in the
  [descriptor contract](CONTRACT-phyre-class-descriptor.md) §14 item 1.
  ***Narrowed 2026-09-27 (FABLE, Claude Opus 5.5): nothing reads `+0xB0` either.** An image-wide census of the sentinel-walk idiom (`lea` of the head, load, compare with the head) finds the destructor `00633390` as the only function that walks `+0xB0`, and it only unlinks; the same census finds the name lookups `005A7A40` / `005A7B50` / `00682E30` on `+0x90` and `005A0470` / `005A7AB0` on `+0xA0`, and 22 walkers of `+0x80`. Every other touch is a self-link (the base constructors, the ten per-class constructors in `006316C0`-`00632780`, the reset `0063D550`). So the shipped build constructs, resets and tears the list down but never fills or consults it; what it was meant to hold leaves no trace in the build. [Record](../../_index/candidates/bl8-b0-walkers/README.md).*
  ***CLOSED 2026-09-27: NO ADMISSIBLE SOURCE for what `+0xB0` was meant to hold, REVIEWED AND SIGNED by OPUS (kind b, intent; FABLE, Claude Opus 5.5, author).** OPUS re-ran `bl8_walkers.py` and added two negatives: a sweep for a stored `+0xB0` head address (26 `+0x80` link stores as the positive control, no descriptor base at `+0xB0`) and a receiver-typed census of 315 static descriptors (only the constructor self-link and the destructor touch `+0xB0`). The other five lists are named above; the build neither fills nor reads the sixth, so its intended element type is intent the build does not carry. [Review](../../_index/candidates/bl8-b0-nas-review-opus/README.md).*
- [x] **BL-6** — Whether any two registered type names actually collide under the `& 0x1F` hash.
  The lookup handles collisions correctly either way, so this is a curiosity, not a risk.
  **ANSWERED 2026-09-18 (FABLE) for every name the image itself supplies: none collide.** The descriptor's name is stored at `+0x30` by the two base constructors (`mov [rcx+0x30], r8`, `00632DB0` and `00632CC0`), which have 400 direct call sites between them. 330 load the name as a string literal in the same function; the other 70 sit in 69 template getters, which take the name as their own argument and park it in a `.bss` slot, plus one forwarding constructor whose two callers build descriptors at run time (one with no name, one from loaded cluster data). Following each getter to its callers recovers one name per getter, **399 distinct names** in all ([phyre_name_hash_census.py](members/phyre_name_hash_census.py), [phyre-type-name-hashes.tsv](members/phyre-type-name-hashes.tsv)). Hashed with the routine as read (`0x7B5`, times `0x21`, plus the low five bits, 32-bit wrap): **399 distinct hashes, 0 collisions**. *Control for the hash's own blind spot:* no two names are equal after masking every byte to five bits, so the case-folding the hash performs never merges two of them either. *Bound:* names that arrive only from loaded cluster data are outside the census; the 37 file-side names listed on [the file-schema page](the-file-schema-against-the-runtime-schema.md) were tested as well - 22 are among the 399 and none of the other 15 hashes onto a constructed name. The expectation for 399 names in a 32-bit space is about one collision in fifty thousand such sets, so the result is the ordinary one. Static.
- [x] **BL-7** — **Nothing here is runtime-confirmed.** Every offset is derived from registration *(closed — the register row is WITHDRAWN.)*
  code, never observed in a live process. One Cheat Engine read of `m_intensity` at
  `VPLight +0x30` would lift all 680 rows to tier-10 corroboration.

## 8. Evidence

### The BJ-4 answer: the question's premise was wrong

BJ-4 asked *"what do the `typeId` constants passed to `00632960` mean — `0x12` and the others?"*
It was filed on my own reading of a decompiled call, and that reading was wrong twice.

**There is no type id.** The two constants are an **offset** and an **attribute bitfield**, and
the field's type is a *pointer*, the third argument.

| Claim | Evidence | Tier |
|---|---|---|
| Argument 5 is a byte offset, not a size | struct-layout coherence across 164 classes: `VPLight`'s six floats are exactly 4 apart and its three pointers exactly 8 apart, with no gaps; `VPPhysicsRigidBodyBase` places an `unsigned char` at `+0xE8` and a `bool` at `+0xE9`, adjacent single bytes. A size field cannot produce that. | 1 |
| Argument 6 is an attribute bitfield | only five values occur (`0x02 0x08 0x0A 0x10 0x12`) across 484 resolved sites — three bits, two of them independent | 1 |
| Bit 0 = the name is heap-copied | complete body of `00632FB0`: `if (attrs & 1) { copy the string; store the copy }` | 1 |
| …and the teardown agrees | `00633240` tests byte `+0x28` bit 0 before freeing — the same word, reached independently in the sibling document | 1 |
| Bit 1 = stored as a pointer | never set on a primitive-typed field (0 of 254); set on 154 class-typed fields; and the `VPNode` minimal pair, where `m_worldMatrix` (`0x12`) occupies 8 bytes and `m_localMatrix` (`0x10`), of a matrix type, occupies 64 | 1 |
| Bits 3–4 are per-class, not per-field | constant across every field of a class in **146 of 146** classes; within a function, resolved values differ only in bit 1 (`0x10`/`0x12` or `0x08`/`0x0A`), never `0x08` vs `0x10` | 1 |
| The field's type is a `PType *` | complete body of `00632960`: argument 3 is stored at `record+0x30` with no interpretation | 1 |
| The primitive set | RTTI class names of the `PTypeDefault<T>` singletons, decoded through MSVC mangling: `I`/`M`/`E`/`H`/`G`/`_N`/`F` | 4 |
| 682 registration sites; **680 fully resolved** over **246 named classes** and 109 field types | forward abstract interpretation of all 38,161 bodies: registers and stack slots carry symbolic values, calls clobber the volatiles and put `('ret', callee)` in `rax` | 1 |
| The second pass did not contradict the first | every one of the 484 attribute, 523 offset, 593 class and 629 type values the backward scan had recovered is reproduced **identically**, with **0 disagreements and 0 losses**, plus 491 new values | 1 |
| The offset is validated arithmetically by the consumer | complete body of `0062EFD0`: `capacity < (fieldOff - baseOffset) + width + used` | 1 |
| Attribute bit 1 means "stored as a pointer" — from the consumer | complete body of `0063C0C0`: returns ~~literally `8`~~ the context's pointer width (a literal `8` only for a null context) *(corrected 2026-10-02, OPUS: `0063C106`, `0063C17D`)* when bit 1 is set, else the type's inline size from `type+0x38` | 1 |
| The member list head is `cls+0x80`, tail `cls+0x88`; base chain at `cls+0x78` | complete bodies of `0062EFD0` and `00597220` | 1 |
| A class descriptor has **six** intrusive lists, and the full descriptor layout | complete body of the constructor `00632D80`, which sets every field in one place; `005A7ED0` calls it with `"PAnimatableComponent", 0x108, 8` | 1 |
| The class name is at `+0x30` and the instance size at `+0x38` | the same constructor body, corroborated by `006388C0` loading `[rcx+0x30]` as a string and by `AttachMember` comparing against `[cls+0x38]` | 1 |
| `+0x50` is this descriptor's node in a global registry | `0063D640` unlinks `cls+0x50` and converts a node back to its descriptor by subtracting `0x50` | 1 |
| `+0x90` holds methods | 220 `PClassDataMemberBase` constructions that are not field registrations, 216 with names like `playOnce` / `stop` / `getAnimationTime`; the insert into `[cls+0x90]` traced instruction by instruction in `005AD8F0` | 1 + 2 |
| `+0xA0` holds the script bridge | `005B2860` builds a record named `"GetGlobalTime"` and links it into `[cls+0xA0]`; an independent writer census makes `Phyre.ScriptVM.ReflectionBridge` five of the eight Phyre writers of that head | 1 + 11 |
| Static records are never freed, dynamic ones are | the destructor's `+0x90`/`+0xA0` walks free each node only when its attribute bit 0 is set; the `+0x80` walk contains no free at all | 1 |
| `flag2` is 0 at every resolved site | the same forward pass; the `flag2 == 2` branch is unreachable in this binary | 1 |
| Owning class and field type names | the objects those arguments point at, joined to the independently recovered `Tools/work/rtti/vtables.tsv` through `lea reg,[rip+VFT] ; mov [rip+OBJ], reg` assignments | 4 |
| 680 of 682 registrations are inside a one-time-init guarded region | per-function scan tracking `_Init_thread_header` / `_Init_thread_footer` nesting depth at each registration call | 1 |
| The name hash and its collision handling | complete bodies of `006388C0` and `006311D0` | 1 |

### The killer observation, and what happened when it was sought

**The claim most likely to be false was "argument 5 is an offset."** The killer: a class whose
registered values overlap, or whose spacing contradicts the field widths — two 4-byte floats
2 bytes apart, or two fields at the same value.

Sought across all 164 classes with resolved values. **No class has two fields at the same value**,
and in every fully-resolved class the spacing is consistent with the field widths. It did not
break. Registration order is *not* offset order in 15 of 70 classes with three or more fields —
which is expected (the order is the declaration order in the generated list, not the layout) and
is not a counterexample, because the *set* of values remains a valid layout.

**A second attack, on bit 1.** The killer: a field with bit 1 set whose gap to the next field is
not 8. Eleven exist. They do **not** refute the reading, because a gap is only an upper-bound
proxy — an unregistered field sitting between two registered ones inflates it, and 52 of the 63
measurable gaps are exactly 8 while bit-1-clear fields are gap-8 only 11 times in 196. The
`VPNode` minimal pair settles it independently of gap statistics. The eleven are recorded rather
than dismissed.

**A third attack, on the per-class constancy of bits 3–4.** The killer: the value being an
extraction artefact from constant hoisting — if MSVC emitted the store once and my backward scan
reused it, homogeneity would be manufactured. Tested: **339 of the 484 resolved values come from
"later" registrations, not the first in their function**, so the store is re-emitted per call and
the scan is reading each one. And 39 functions show *two* values that differ only in bit 1, which
a hoisting artefact could not produce.

### The hypothesis that failed

**Bits 3–4 are not the class-descriptor template kind.** The obvious reading — that `0x00`/`0x08`/
`0x10` distinguish `PClassDescriptorConcrete` from `PClassDescriptorWithoutDefaultConstructor`
from `PClassDescriptorHeader` — was tested directly against the recovered class names and
**refuted**: `PClassDescriptorConcrete` classes take all three values (229 / 118 / 21). The bits
remain undecoded and are filed as BL-1 rather than guessed.

### Correction to a sibling document

[`class-descriptor-and-metadata-system.md`](class-descriptor-and-metadata-system.md) §2 says each
reflected class "gets a **global descriptor singleton**, constructed by a generated initializer at
process start". That is right for the *descriptor object*. It is **not** right for the field lists
inside it: **680 of the 682 member registrations execute lazily**, behind a one-time-init guard,
the first time the class is touched. The descriptor exists from startup; its members do not. That
document is owed a note, and the claim it makes about `atexit` pairing and teardown is untouched
by this.

### A unit error in the sibling document's descriptor layout

[`class-descriptor-and-metadata-system.md`](class-descriptor-and-metadata-system.md) §4 gives the
`PClassDescriptor` layout with its four intrusive lists at `+0x10`, `+0x12`, `+0x14`, `+0x16`, the
class name at `+0x0C` and a counter at `+0x1D`. **Those are qword indices, not byte offsets** —
the decompiler prints `param_1[0x10]` on an `undefined8 *`, and the document transcribed the
index. In bytes the four lists are `+0x80`, `+0x90`, `+0xA0`, `+0xB0`, which is exactly where the
attach path links a member (`cls+0x80`, tail `cls+0x88`) and where the reset helper `0063D550`
re-initialises them. There are also **two more lists** that the destructor evidently does not
walk, at `+0x50` and `+0x60`, so the count is six rather than four.

This matters practically: a modder using `+0x0C` as a byte offset reads the wrong memory. The
document is owed a corrected table; the *structure* it describes — four walked lists, an embedded
name string, a sub-object, a counter — is right, and only the unit is wrong.

### Corrections to my own earlier reading

Both in the lazy-static document, which cited this call site as a worked example and got two of
its three constants wrong. It read

> "class X has a field called `m_animationSet`, 32 bytes wide, of type 0x12"

where the truth is **offset `0x20`, attribute word `0x12`, type supplied as a pointer**. The
mis-reading came from taking a decompiler's positional arguments at face value without reading
`00632FB0`, which is where the attribute word's meaning is actually visible. Fixed there, and it
is the reason BJ-4 was filed with a wrong premise in the first place.

## 9. Related

- [`class-descriptor-and-metadata-system.md`](class-descriptor-and-metadata-system.md) — the
  descriptor objects these fields attach to, their layout and their teardown.
- [`../Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`](../Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md) —
  the consumer: it resolves dotted member paths against exactly this schema.
- [`../../24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md`](../../24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md) —
  why this is lazy, and the hang that results from interrupting it.
- [`../Subsystem-Map/phyre-subsystem-map.md`](../Subsystem-Map/phyre-subsystem-map.md) — where
  reflection sits among the Phyre subsystems.
- [`../Script-Object-Accessors/phyre-script-object-accessors.md`](../Script-Object-Accessors/phyre-script-object-accessors.md) —
  the script bridge that type-checks objects before touching them.
- [`../README.md`](../README.md) — category index.

## 10. Falsification pass — 2026-09-02

Against snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`.

**Attacked: "argument 5 is an offset."** Killer named and sought: overlapping or width-inconsistent
values. **Survived** — no class has two fields at the same value, and spacing matches field widths
throughout. Recorded in §8 with the registration-order caveat.

**Attacked: "bit 1 means pointer."** Killer: a bit-1 field whose gap is not 8. **Eleven found, and
they do not break it** — gaps are an upper bound, and the `VPNode` minimal pair proves the reading
without gap statistics. Listed rather than dropped.

**Attacked: "bits 3–4 are per-class."** Killer: an extraction artefact from constant hoisting.
**Survived** — 339 of 484 resolved values come from non-first registrations, and 39 functions show
two values differing only in bit 1.

**Attacked: "bits 3–4 are the descriptor template kind."** **Refuted.** `PClassDescriptorConcrete`
takes all three values. Filed as BL-1 unresolved rather than softened into a plausible sentence.

**Attacked: "the registration is lazy."** Killer: registrations outside a guarded region.
**Two found in 682**, both recorded as BL-3. The claim is stated as 680 of 682, not as "all".

**Attacked: the type names.** Killer: the RTTI join being wrong. The join is
`object -> vftable -> class` through assignments found in code, against a vtable table recovered
by a *different session using a different method*. Its agreement is the check: 629 of 682 type
pointers resolved to a named class, and the resulting names are internally coherent — every
primitive resolves to `PTypeDefault<T>` with a valid MSVC mangling code, and no field type
resolved to something structurally impossible such as a function or a string.

**Attacked, second pass: "the 89 and 53 unresolved sites are unresolvable."** Killer: a value the
forward interpreter also could not follow. **Broke, in the good direction** — 680 of 682 now
resolve. The two that remain are the same two that sit outside a guarded region. Critically, the
new instrument was checked *against the old one* rather than simply believed: **0 disagreements
and 0 losses** across 2,229 previously-resolved values.

**Attacked: "bits 3–4 are constant per class."** Killer: a class with two values. **Broke** — with
the full 680 resolved, 3 of 246 classes mix `0x00` with `0x08`, where the earlier 146-class sample
had none. The claim is now stated as 243 of 246 with the three named. This is the wider
measurement doing its job: the smaller sample had supported a stronger claim than the data did.

**Attacked: "bit 1 means pointer" — again, from the other side.** Killer: the consumer ignoring
the bit. **Survived and strengthened** — `0063C0C0` reads exactly that bit and yields 8.

**Attacked: "the offset reading."** Killer: the consumer treating the value as a size.
**Survived and strengthened** — the attach path subtracts a base offset from it and compares
against a byte budget, which is only meaningful for an offset.

**Attacked: "nothing ever inserts into the member's second list."** Killer: a function performing
the circular-insert idiom with the head at `+0x38`. The scan returned nine candidates — **and its
positive control failed**: the same test, run against the head/tail pair the attach function
demonstrably uses (`+0x80`/`+0x88`), did not return `0062EFD0`. An instrument that cannot find the
case I already know about cannot be trusted on the case I do not, so **the nine hits are discarded
and the question stays open**. The likely cause is that the idiom's `lea` and its tail store do not
share a base register in the compiled form, which my test required.

**Attacked: my own correction to the sibling document.** Killer: the byte offsets being wrong.
**Broke** — I had written that the class name sits at byte `+0x60`, reached by multiplying that
document's qword index by 8. Reading the binary instead: `+0x60` is a sixth intrusive **list**,
cleared by a list-unlink loop, and the type name is a `char *` at **`+0x30`**, loaded by
`006388C0` as `mov rsi,[rcx+0x30]`. The sub-object at `+0x70` and counter at `+0xE8` do check out
directly. Corrected in place, and the failure is instructive: I was warning about arithmetic on a
mislabelled table while doing arithmetic on a mislabelled table.

**Attacked: the recovered offsets, from a fifth direction.** The default-value constructor
`006BE990` writes at exactly the offsets this document assigns for `VPLight`, with values that are
semantically right for each field. **Survived, and independently.**

**Attacked: the list-writer instrument, before using it.** The previous block's version of this
scan failed its own control. Reading `AttachMember` byte by byte showed why: the tail is **never**
touched as `[base + HEAD+8]`. The head is materialised once with `lea rbx,[r14+0x80]` and every
subsequent access goes through `rbx` — `mov rax,[rbx+8]`, `mov [rbx+8],rcx`. My test had assumed
the base register, which never appears again. Rebuilt around the real idiom, **the control passes**
and returns `0062EFD0` for head `0x80`.

**Attacked: the rebuilt instrument's first result.** Killer: the same ten
`ThreadSafeStaticObjectInitializer` functions appeared as writers of *every* head, which is not
what a list-specific writer set looks like. Cause found: `mov [R+8], R` is the empty-list
**self-link** a constructor emits, and my test counted it as an insert. Excluding stores where the
value register is the head register drops those ten from every head and leaves writer sets that
differ per list — `0062EFD0` alone on `+0x80`, `GeneratedMetadataRoutine` on `+0x90`,
`ScriptVM.ReflectionBridge` on `+0xA0`. **Both failures were caught by looking at the shape of the
answer, not by the tool complaining.**

**Attacked: "the descriptor layout" — for the third time.** After being wrong twice on this
structure (unit, then kind), I did not re-derive from the corrected table. Every offset in the
layout above comes from the constructor `00632D80`, which writes all of them in one body. It
independently reproduces the name at `+0x30`, giving that field three separate derivations
(`006388C0`'s load, the constructor's store, and `005A7ED0` passing `"PAnimatableComponent"`).

**Attacked: the writer census this document published one revision earlier.** Killer: a candidate
that is not a class descriptor. **Broke.** All six candidates the unfiltered scan offered for
`+0x50`, `+0x60` and `+0xB0` were opened and **none is a class descriptor** — an EASTL list
container constructor, two Steam callback registrars, a `PPFX::CTinyEffect` constructor and a
`Phyre::VTS::ScreenState*` constructor. The scan matches any structure with a self-linked pair at
that displacement. Its `+0x90`/`+0xA0` rows survive only because their domain composition points
at Phyre reflection *and* each has an instruction-level trace; the rest are retracted in §2.

**Attacked: the replacement instrument, before publishing it.** Anchoring on real descriptor
objects and looking for rip-relative references into their interiors is descriptor-specific by
construction — but reading its candidates found the failure mode anyway: `00630340` and `00630490`
are magic-static accessors for unrelated `PType` singletons that happen to sit at an address equal
to some descriptor's `D + offset`. Descriptors are ~0x110 bytes packed in `.data`, so an interior
address can be another global's start. **Not published as an answer.**

**A negative that does hold, because it has a control.** No function in any slot of a
class-descriptor vtable references `[this+0x50]`, `[this+0x60]` or `[this+0xB0]`; the identical
query for `[this+0x80]` returns slot 8 (`AttachMember`) and two neighbours. Three zeroes with a
passing control are evidence; the same three zeroes without one would not have been.

**Re-checked for banned evidence.** No `.pdata`, `.xdata`, unwind record or EH map appears in any
claim. The RTTI join is tier 4 and is labelled as such; every mechanism claim rests on a complete
body.

**Not attempted, and therefore not claimed:** any runtime confirmation that a recovered offset is
correct in a live process. Every offset here is derived from the registration code, not observed.
A single Cheat Engine read of `m_intensity` on a live light would raise the whole schema to tier
10 corroboration, and that is the obvious next step.

## 11. The registrar level above the field level — 2026-09-03, session `repos-78`

`005E5400` and `005AD8F0` both sat on the *leaned on and never opened* cut, ranked 2nd and 3rd by
bytes-per-line-of-prose. **They are cited by the same three documents, so their rank is one
under-described document counted twice rather than two independent gaps** — they are taken here as a
pair, and the pair turns out to be two members of a set of **315**.

**Extent checked, and this is the first time in this session's run that the tail-call hazard actually
applied.** Both functions' last instruction is `jmp 0x639450`, and **`00639450` is its own 88-byte
function** — a real tail call out of extent, not a loop back edge. The behaviour continues there.

### `00639450` is the shared finaliser of every class registration

**315 functions have `jmp 0x639450` as their final instruction.** It is not a helper called from many
places; it is **the common epilogue of a set of registrar functions**, each of which registers one
class. It marks the descriptor and, conditionally, initialises an empty intrusive list:

```asm
0063945C  mov   rcx, qword ptr [rcx + 0x70]
00639460  call  0x639160
00639465  or    dword ptr [rbx + 0xfc], 0x40000000     ; a "registered" bit
0063946F  test  byte ptr [rbx + 0xfc], 1
00639478  lea   rax, [rbx + 8]
00639481  mov   qword ptr [rax], rax                   ; self-pointers: an empty list head
0063948A  mov   qword ptr [rax + 0x10], rax
0063949D  jmp   0x6388c0
```

### How the 315 relate to this document's 682 — two populations, stated

Section 2 establishes **682 `00632960` call sites over 246 named classes**. That figure is
**independently reproduced here: 682**, counted by disassembling every function body in the ledger.
The registrar set relates to it as follows:

| | |
|---|---:|
| functions tail-calling `00639450` | **315** |
| of those, containing at least one `00632960` call | **173** |
| `00632960` sites **inside** those registrars | **593** |
| `00632960` sites **outside** them | **89** |

> **142 of the 315 registrars register no named field at all**, and **89 of the 682 field
> registrations happen outside any of them.** The two sets overlap heavily and neither contains the
> other — **"315 classes" and "246 named classes" are answers to different questions** and must not be
> reported as one number.

### The schemas, extracted mechanically

Each registrar `lea`s the name strings it registers, so the schema of every class is recoverable in one
pass. Across the 315: **935 distinct name strings, of which 715 begin `m_`.** **112 registrars yield no
strings at all** — consistent with the 142 that register no fields.

**`005E5400` — a dynamic mesh instance**, 20 fields and 8 accessors:

```
m_mesh  m_localToWorldMatrix  m_currentPose  m_materialSet  m_instanceSegment
m_dynamicMeshInstance  m_bounds  m_lodLevel  m_segmentContext  m_flags
m_extraFlag  m_extraZBias  m_farPlane  m_specularIntensity  m_cubeMapIntensity
m_cubeMapFactor  m_alphaThreshold  m_specialRenderOrder  m_specialTextureWrapType  m_name
setVisibilityFromAnimation  getLocalToWorldMatrix  getBounds  setBounds
getMesh  getMaterialSet  getPoseTransform  setPoseTransform
```

**`005AD8F0` — an animation controller**, 5 fields and 24 methods:

```
m_animationSet  m_animationClips  m_animationWeightedBlenderController
m_animationTargetBlenderController  m_animationNetworkInstance
setAnimationSet getAnimationSet setSpeed getSpeedForSlot setSpeedForSlot
playOnce playLooping playOnceByName playLoopingByName stop
playOnceInSlot playLoopingInSlot playOnceByNameInSlot playLoopingByNameInSlot
getAnimationTime getAnimationTimeForSlot hasOneShotAnimationFinished
hasOneShotAnimationFinishedInSlot getWeightForSlot setWeightForSlot
getAnimationClipForSlot setMaximumClipCount getMaximumClipCount  pAk
```

> **That second list is an API, not a field table.** `playOnce`, `playLooping`, `stop`, `setSpeed` and
> their per-slot variants are the animation surface a script or a mod can drive, **with explicit slot
> and weight control** — a blend system exposed by name.

The full extraction for all 315 is in `Tools/work/h78/phyre_class_registrars.json`
(`entry → {size, strings}`), and the census it came from is `Tools/work/h78/sse_loop_census.tsv`.

### Why these two looked like a gap, and what the shape says

Both are **loop-free**: `005E5400` is 770 instructions with **zero** backward jumps, `005AD8F0` is
1,080 with zero. **Nine and a half kilobytes of straight-line code between them.** Each also carries 28
`_Init_thread_header` / `atexit` / `_Init_thread_footer` triples — **28 function-local statics with
thread-safe initialisation apiece**, which is what makes them long rather than complex.

**That is the genuine registrar shape**, and it is worth naming because a shape like it was misread
once in this database's history: *"sixteen callees each called exactly once, almost no comparisons"*
was reported as a registrar and turned out to be **a loop**. **Here the loop count is zero, measured
over the whole body** — the evidence is the absence, not the impression.

### What is not established

- [x] **UQ-290.** **Which class each registrar registers.** The strings give each schema; **the class name itself
      is not among them** for most, and no registrar was traced to its `PClass` descriptor.
      **ANSWERED 2026-09-18 (FABLE): every one of the 315 registrars is joined to the class it registers, by name.** Each of the 315 (the functions ending in `jmp 00639450`) calls `006388C0`, which registers the descriptor in `rcx` under the name at its `+0x30`. The descriptor's name is stored at `+0x30` by the two base constructors (`mov [rcx+0x30], r8`, `00632DB0` and `00632CC0`), which have 400 direct call sites between them. 330 load the name as a string literal in the same function; the other 70 sit in 69 template getters, which take the name as their own argument and park it in a `.bss` slot, plus one forwarding constructor whose two callers build descriptors at run time (one with no name, one from loaded cluster data). Following each getter to its callers recovers one name per getter, **399 distinct names** in all, each tied to its static descriptor. Joining registration site to descriptor to name ([phyre_registrar_classes.py](members/phyre_registrar_classes.py), [phyre-registrar-classes.tsv](members/phyre-registrar-classes.tsv)) names **470 of the 523** registration sites image-wide and **every site of all 315** registrars of the census; 388 of the 409 functions that call the register routine are named at every site. *Control, independent of the join:* the field schema attributes its rows to 246 calling functions by resolving the class argument of the member-registration call, a different route; **242 agree with the class named here and none disagrees** (template names compared up to the `<`), and the remaining 4 are the D3D11 description structs, whose schema callers construct a descriptor but never call the register routine. The join also keeps what the schema's leaf column drops: the 69 template registrars are named by instantiation (`PArray<PUInt32>`, `PArray<PAnimationChannel *>`). *Residue, stated:* 53 sites outside the 315 stay unnamed - 27 on a run of statics at `02CF8270`..`02CF8A80` and one in `.data`, 17 on descriptors returned by accessors the walk does not open, 7 unresolved and 2 registering the caller's own argument; the statics are built by a separate constructor family in the reflection core that stores the name at `+0x30` from a call result rather than a literal (checked for `02CF8470`, whose start-up initialiser hands it to a member of that family with size `0x30`). Static; every hop is a bounded linear backward walk, and an unresolved hop is reported, not guessed.
- [x] **UQ-291.** What the 112 string-less registrars do register.
      **ANSWERED 2026-09-18 (FABLE): one class each, and now by name.** All 112 resolve, and every one registers exactly one descriptor: `PClusterHeader`, `PAnimationNetworkInstanceTarget`, `PAnimationSlotArray`, `PAnimationHierarchyNode`, `PSamplerState`, `PTexture3D` and so on down the TSV (UQ-290). They are string-less because they name no member: the registrar's only work is the lookup-or-insert and the finaliser, and the class name lives in the descriptor's constructor, not in the registrar. Static.
- [x] **UQ-292.** Why 89 field registrations sit outside the 315.
      **ANSWERED 2026-09-18 (FABLE): because the 315 is a selector on how a function ends, and three kinds of function that register fields do not end that way.** Grouping the 89 rows of [phyre-field-schema.tsv](phyre-field-schema.tsv) whose calling function is not one of the 315 gives 75 functions in three groups that sum exactly: **69 sites in 69 template getters** (`PArray<T>` and `PSharray<T>` instantiations, one member each - named by instantiation in [phyre-registrar-classes.tsv](members/phyre-registrar-classes.tsv)); **18 sites in the four D3D11 description-struct builders** (`CD3D11_BLEND_DESC` 2, `CD3D11_DEPTH_STENCIL_DESC` 6, `CD3D11_RASTERIZER_DESC` 8, `D3D11_RENDER_TARGET_BLEND_DESC` 2); and the **2 base-constructor calls** that BL-3 already showed are not registrations. A template getter constructs its descriptor, registers the member, registers the name and then **calls** the finaliser `00639450` (the register call and the finaliser call are the last two calls of the `PArray<PUInt32>` getter, followed by its `ret`) because it must still return the descriptor to its caller; a function that has to return a value cannot end in `jmp 00639450`, which is the 315's defining test. The struct builders likewise call the finaliser as their last call and never call the by-name register routine themselves, so within these four bodies the descriptors are finalised without a by-name registration. So nothing is registered by a different mechanism: the same constructor, member registration and finaliser are used, reached by `call` instead of `jmp`. Counting registrars by the finaliser being *reached* rather than *tail-jumped* would put the population at 315 + 69 + 4. Static; the grouping is a join of two published tables, the two bodies were read at the cited sites.
- [x] **UQ-293.** What `0x40000000` in `+0xFC` gates downstream, and what the list head at `+8` holds.
      ***The list half is ANSWERED 2026-09-21 (FABLE): it is the descriptor's own membership record in a
      global by-name class container, and two of its five fields are not blanks.***

      `006388C0` — the body this finaliser tail-jumps into — takes the descriptor in `rcx`, reads the
      class name from `+0x30` and returns false when it is null, fetches the container with
      `00637440`, and hashes the name: `h = 0x7B5`, then `h = h*0x21 + (c & 0x1F)` per byte
      (`00638920`–`00638932`). It looks that hash up with `006311D0` and returns false if it is
      already there. On a miss it writes

      | store | field | what it is |
      |---|---|---|
      | `00638976` `mov dword ptr [rbp+0x20], edi` | `+0x20` | **the class-name hash** |
      | `0063897C` `mov qword ptr [rbp+0x28], rsi` | `+0x28` | **the class-name pointer**, copied from `+0x30` |

      and then inserts with **`0067F700(container, descriptor + 8)`** (`00638998`), after a second
      check whose failure yields **`0x12`** — the same "already exists" code the member path uses.

      **So the `+0x08` block is a membership record, and the constructor's self-link is its
      *unregistered* state:** `+0x08` is the element head, `+0x10` and `+0x18` are the container
      back-pointers the lookup writes into the element (`006750C0` stores the container at element
      `+8` and `+0x10`), and `+0x20` / `+0x28` are the key and the name. *That is why this page reads
      `+0x20` as a `u32` that is simply zero — zero is what an unregistered descriptor carries.*
      `00639450` restoring all five is **unregistration**, not initialisation.

      The container itself is the same keyed-tree family documented at
      [`where-the-games-memory-comes-from.md`](../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)
      under `UQ-326`: `0067F700` inserts, the lookup converts a node to its element with
      `lea rbx, [rax-8]`, and the sign of a key comparison picks one of two child links. The
      *registry* list — a different list, node at descriptor `+0x50` — and its base-adjacent insert
      are on [the class-descriptor page](class-descriptor-and-metadata-system.md).

      > ***How this was nearly missed, because the tool said no.*** `bf067987a` named the test that
      > would settle this — *an insertion site that adjusts a node pointer by 8* — and I then asked
      > `reach3.py` for `0067F700`'s callers and grepped the answer for this band. It printed **`156`**
      > and listed **twelve**, so the grep returned nothing and I wrote that the descriptor band does
      > not use that family. A separate scan for `lea reg, [reg+8]` followed by a call found
      > `00638998` anyway. Adding `--all` then crashed the tool, because its argv parser reads every
      > argument as a hex address — **a second false zero from the same instrument inside five
      > minutes.** Both are fixed: the elision now names itself and says to re-run before taking a
      > negative off the list. *A truncated listing is exactly where an absence claim comes from.*

      **Not established:** how many classes are registered at any moment, and whether any caller
      depends on the container's order.

      **The `+0xFC` half, unchanged from the 2026-09-14 narrowing:**
      *Narrowed 2026-09-14 (FABLE): the bit is answered; the list is not.* A sweep of `00580000`–`006A0000` for
      displacement `0xFC` finds four touches of bit 30:
      - **Set** by this finaliser (`00639465`) and by a second 552-byte registration body (`006363E0`).
      - **Cleared** by a 621-byte body (`00638D8D`), right after it unlinks a node and re-points it at itself
        (`00638D78`–`00638D89`). That body's only caller is the module walker `005A0840`.
      - **Tested** once, in `PClassDescriptorDynamic`'s vtable slot 12 (`00639A40`, 29 B).
        - It loads the parent descriptor from `+0x78`.
        - While that parent's bit 30 is **clear**, it tail-calls the parent's own slot 12 (`jmp [rax+0x60]`); once the bit
          is set, it returns.
      - **So bit 30 means "this descriptor's registration has run".** Its one reader makes a dynamic class push
        registration up to any base that has not registered yet. The module walker's unlink path withdraws the mark.
      - **Not read:** what the `+8` list holds, and the rest of the 621-byte unlink body.

### Interior anchors for the pair

The claims above are stated against the two functions' entries; these are the addresses that carry
them, so each is checkable rather than asserted — and so the pair stops registering as *cited by entry
only*, which is what put it on the cut in the first place.

| claim | `005E5400` | `005AD8F0` |
|---|---|---|
| tail call to the shared finaliser | `005E63F3` | `005AEEB7` |
| 28 `_Init_thread_header` sites, first / last | `005E5458` / `005E6323` | `005AD951` / `005AEDD3` |
| `00632960` field registrations, first / last | `005E5497` / `005E5D6A` (**18**) | `005AD994` / `005ADB83` (**4**) |
| the first field name `lea` | `005E547B` `"m_mesh"` | `005AD978` `"m_animationSet"` |
| the last field name `lea` | `005E5D4E` `"m_name"` | — |
| a method name `lea` | `005E60D6` `"getMesh"` | `005ADE46` `"playOnce"`, `005AE18C` `"stop"` |

**The field and method counts differ sharply between them and the reason is visible in the anchors:**
`005E5400` makes **18** `00632960` calls across 20 `m_*` names, `005AD8F0` makes **4** across 5.
**Most of the animation registrar's 29 strings are method names, not fields** — so a reader counting
`m_*` strings as "fields registered" would over-count the first by two and the second by one, and a
reader counting registrations would under-count the visible schema in both. **The two numbers measure
different things and both are in the table.**

### The `006349B0` registrar and its eleven teardown thunks — NOCALLER-INSTALLERS, 2026-09-14 (FRONTIER)

`006349B0` is a static-init registrar in the `005A08E0` init cluster (called at `005A094B`). It
inline-builds `PClassDataMember` statics on owner class descriptor `02CF8580` — the field names
(`m_size`, `m_offsetFromParent`, `m_offsetToBase`, `m_offsetToBaseInAllocatedBlock`,
`m_currentMemberCount`, `m_actualSize`, `m_defaultBufferStorage`, `m_validationBufferStorage`,
`m_writeMaskBufferStorage`) are the members of Phyre's serialized **block record** —
and registers each on the owner via `call [owner_vftable+0x40]` (e.g.
`mov rax, [02CF8580]` / `call [rax+0x40]` at `00634AA3`). After each registration it passes the
member's generated teardown thunk to `atexit` (`00808B90`), e.g. `lea rcx, [008AFB90]` /
`call 00808B90` at `00634AAC`–`00634AB3`. The **11 no-caller functions this group binds are those
thunks** — each is the `atexit`-registered destructor of one descriptor static:

| thunk | descriptor static | member registered | interior evidence |
|---|---|---|---|
| `008AFB90` | `02CF9080` | `m_size` (offset `0x38`) | re-stamps vtable `00D580B0`, unlinks lists (`008AFB9D`/`008AFBA4`) |
| `008AF9D0` | `02CF90E0` | `m_offsetFromParent` (`0xF0`) | same ~~96-byte~~ 103-byte *(corrected 2026-10-02, OPUS: `008AF9D0` returns at `008AF9D0+0x66`; the array-member page's 103)* `PClassDataMember` teardown shape |
| `008AFA40` | `02CF9140` | `m_offsetToBase` (`0xF4`) | " |
| `008AFAB0` | `02CF91A0` | `m_offsetToBaseInAllocatedBlock` (`0xF8`) | " |
| `008AF6C0` | `02CF9200` | `m_currentMemberCount` (`0x102`) | " |
| `008AF570` | `02CF9260` | `m_actualSize` (`0x104`) | " |
| `008AF730` | `02CF92C0` | `m_defaultBufferStorage` (`0x108`) | " |
| `008AFD00` | `02CF9330` | `m_validationBufferStorage` | " |
| `008AFD70` | `02CF93A0` | `m_writeMaskBufferStorage` | " |
| `008AFB20` | `01F2E000` | member descriptor built elsewhere (dynamic-type record) | touches `01F2E000`/`+0x18`/`+0x28`/`+0x38` |
| `008AF8F0` | `01F2E060` | " | touches `01F2E060`/`+0x18`/`+0x28`/`+0x38` |

The two `01F2Exxx` records are registered by `006349B0` against the same owner (`lea rdx, [01F2E000]`
at `00634AE7` → `call [rax+0x40]`) but constructed outside this function — hence the different
teardown family (`DescriptorRuntime` per the teardown census) and different `.data` region. Offsets
above are the descriptor `+0x48` stores (`mov dword [block+0x48], imm`); `m_flags` and the
`+0x28`/`+0x30` attribute/type fields are written with register values (`edi`/`rax`) not resolved
here. The sibling registrar `006352A0` (called next in the cluster, `005A093C`) registers the
next block `02CF93E0` (`m_flags`) plus the method members `create`/`deleteObject`/
`deleteInstancesOfType`/`absorb` (each `pAk`-annotated) against a **different** owner,
`02CF8680`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Platform — CLIENT (1 edges, one fan-in).** All 1 edges are Platform bodies reaching `005A08E0` on this page. `FUN_005cc930` is the worked example - it is a high-resolution counter read: it calls the import at `008C2188` and converts the unsigned 64-bit result to double with the `2^64` fixup at `00D27A68`. The crossing is **one shared subject with 1 callers on that layer**, not 1 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT.** `FUN_005c5c80`, owned by that layer, calls `005AD8F0` on this page. That caller is a 920-byte registration sweep - **fifteen calls in fixed order and no branches between them** - each registering one thing with the layer below; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## Interior citation — frontier hub `00632960` (2026-09-17, SWE2-EC7)

`00632960` — 165 B, 11 A-measured callers at census; the member-registration call this page
documents end-to-end. Interior anchor only: `call 00632FB0` base-init first, `[+0x28] = arg3`,
the `+0x38` intrusive list head is self-linked empty at
[`006329A4`](../../_index/ADDRESS-INDEX.md)–`006329AF` exactly as the page describes, the vtable
`00D580B0` installs at `006329B6`, `+0x48`/`+0x50` ~~take the name and context args~~ take the field offset (argument 5) and zero *(corrected 2026-10-02, OPUS: `006329B9`-`006329C0`; the name goes to the node through `00632FB0` and the context only to the attach call)*, `+0x28` bit 1
is set when the mode arg is 2, and the tail `call [descriptor-vtable +0x40]` at `006329EE` is
the descriptor handoff the page counts at 1,186 sites.


## Interior citation — frontier hub `00632FB0` (2026-09-18, SWE2-EC7)

`00632FB0` — 141 B, 51 callers (5 A-measured); the reflected-member node ctor with the
owned-string arm. Interior verified: self-links the node `[rcx]=[rcx+8]=rcx`, installs
`{rdx, r8, r9d}` at `+0x10`/`+0x18`/`+0x20` (`00632FC7`–`00632FCF`); when `r9b & 1` it measures
`r8` with a `strlen` scan (`00632FF0`–`00632FFA`), allocates via `0017D260` (the
`_aligned_malloc` wrapper) at [`00633005`](../../_index/ADDRESS-INDEX.md), `memcpy`s the bytes,
and replaces `[+0x18]` with the owned copy (`00633026`). Bit 0 of the flag word is
"name is owned / copy it" — the field-name storage contract this page's schema relies on.

## SWE2-EC7-47 update (2026-09-19) - `0063C0C0`

`0063C0C0` (210 B) is `FieldStorageWidth` - `call [rax+8]`/`[r8+0x10]`/`[rdx+8]` vcalls, no direct calls; returns ~~8~~ `ctx->vslot08()` *(corrected 2026-10-02, OPUS: `0063C106`; a literal 8 only for a null context, `0063C17D`)* when attribute bit 1 is set, else the type's inline size from `type+0x38`. Interior anchor `0063C0E4` (the first vcall).

## 12. The in-memory accessor path, and why the width question needed it (2026-09-19, OPUS)

`FieldStorageWidth` answers "how wide is this field **to a given context**", and §"How the engine
uses the record" now records that its pointer width is `ctx->vslot08()` rather than a literal.
That makes it the wrong authority, on its own, for the question the type store actually had to
answer: **how many bytes does this member occupy in a live instance?** A serialisation context is
free to answer differently from the runtime.

There is a separate set of functions that does operate on live instances, and it gives the same
answer from the in-memory side.

### The four accessors

Exactly four functions in the image test bit 1 of the attribute word — `0063C4A0`, `0063D300`,
`0063AD90`, `0063C910` — and all four have one shape:

```
0063C4A0   rax = [rcx+0x18]              ; the owning class descriptor (member+8 sub-object +0x10)
           r9d = [rcx+0x48]              ; the member's offset
           r9d -= [rax+0xF4]             ; a base adjustment on the CLASS
           r10  = (long)r9d + r8         ; r8 = the live instance -> r10 = &instance.member
           r9   = [rcx+0x30]             ; the TYPE descriptor
           test byte ptr [rcx+0x28], 2   ; the attribute word
           rcx = r9 ; r8 = r10 ; rax = [r9]
           je   -> jmp qword ptr [rax+0x18]     ; bit CLEAR -> the VALUE handler
               -> jmp qword ptr [rax+0x28]      ; bit SET   -> the REFERENCE handler
```

`0063D300` is the same with the pair `+0x20`/`+0x30`. Both sides receive the address of the slot
and differ only in how many bytes they move through it. For `VPWorldMatrix` — type descriptor
`02E404B0`, vtable `00D6DE78`, installed by registrar `00166080`:

```
+0x18 -> 0067E510   mov [rbx],ecx / [rbx+4],ecx / [rbx+8],ecx / [rbx+0xC],ecx …   the INLINE VALUE
+0x28 -> 0067E380   mov qword ptr [rbx], rax ; ret                                ONE POINTER, 8 B
```

So in a live instance, **bit 1 set ⇒ the slot is eight bytes**; clear ⇒ the slot holds the type's
own instance size. This is the engine storing into its own object, not a width reported to a
caller, and it agrees with `FieldStorageWidth` for every field in this schema.

### `classdesc + 0xF4` is zero, and that had to be established

Every one of those accessors subtracts `[classdesc + 0xF4]` from the recorded offset before
touching the instance. A non-zero value would mean **all 680 offsets in this document are shifted**
and unusable as struct offsets — the single assumption capable of invalidating the whole schema at
once. It is zero:

* base constructor `00632D80` stores `r10` at `+0xF4` (`00632E62`) inside a clearing run that also
  zeroes `+0xC0`, `+0xC8`, `+0xD0`, `+0xD8` and `+0xE0` with the same register — `r10` is the zero
  register there;
* the nine sibling constructors at `006316C0`, `00631A60`, `00631C40`, `00631E20`, `00632000`,
  `006321E0`, `006323C0`, `006325A0` and `00632780` each store `rbp` at `+0xF4` after
  `xor ebp, ebp` (e.g. `006327B9` then `006328BE`);
* no other write to a class-descriptor `+0xF4` exists. A sweep of every `mov`-family write with
  displacement `0xF4` in `.text` returns 169 sites, and the only ones inside the descriptor
  machinery are the ten above.

**The recorded offsets are true in-instance offsets.**

### What this settled in the type store

The 201 remaining zero-width rows in `_types/fields.tsv` were filled from this: 153 at 8 bytes
(bit 1 set), 48 at their type's instance size. Two corroborations that were not used to derive the
rule and could each have broken it — 122 of the rows have room for exactly 8 bytes before the next
registered member and **all 122** carry bit 1 (base rate 154 of 680); and all 153 eight-byte rows
sit at **8-aligned offsets**, 153 of 153. Zero-width rows in the store went 269 → 0, with
0 overlapping rows and 0 sum mismatches across 274 sized types.

It also explains a failure recorded there: filling rows by the rule "the ctype names a type, so
use that type's size" produced 23 candidates of which **13 were contradicted by the next field's
offset**. All 13 were bit-1 members whose ctype names the *pointed-to* type.

**Still not established.** That bit 1 means an *owning* pointer — the branch proves the slot is
eight bytes and holds an address, and says nothing about ownership or lifetime. And **bits 3–4
(`BL-1`) remain unexplained**; they are mutually exclusive across all 680 rows (`0x18` never
occurs), which is consistent with a two-valued field, but no consumer has been read and nothing
in the type store depends on them.

## 13. BL-1 answered: bits 3–4 have no consumer in this image (2026-09-19, OPUS)

`BL-1` asked what attribute bits 3–4 (`0x18`) mean. The answer is that **nothing in the shipping
image reads them**. They are written at registration and never consulted. That is a bounded
answer, not a failure to find one, and it is only worth stating because the instruments that
found nothing here do find the bits that *are* consumed.

### The population, and why it is the right one

A body qualifies as handling a `PClassDataMember` if it lies in the reflection block
`0062E000`…`00641000`, **or** if it reads both `+0x30` (the type descriptor) and `+0x48` (the
offset) off one non-`rsp` register — a fingerprint that assumes nothing about the flags. That is
**1,206 bodies** (563 + 643). The word is searched at `+0x28` and at `+0x20`, because it is also
`+0x20` of the sub-object at `member+0x8`, and a load into a register is tracked forward to any
`test`/`and`/`cmp`/`shr`/`bt` on the loaded value.

### Four instruments, all negative, with the controls positive

| instrument | bits 3–4 | control |
|---|---|---|
| direct `test`/`and`/`cmp`/`bt` with an immediate at `+0x28`/`+0x20` | **0** | bit 0 and bit 1 both found |
| the same through a register loaded from the word | **1**, refuted below | bit 0: 47 sites, bit 1: 7 |
| every short function returning the word (image-wide) | **0** | 14 getters found; see below |
| `shr`/`sar` by 3 or 4, or a mask of `0x08`/`0x10`/`0x18`, image-wide | **0** in the block | 138 hits, all elsewhere |

* the single register hit, `005CA79E cmp ebx, 8`, is not the word: `ebx` there is a loop count
  (`lea rax,[rbx*4]`, a stack alloca, then a `movdqa` loop with an 8-element threshold). It is a
  stale-register false positive of the forward tracking;
* the 138 shift hits are `sar rax,3` / `sar rax,4` pointer-difference divisions on unrelated
  structures, none inside the reflection block;
* the `0x1F` sites are a **shift amount or bit index** — bit 31, sign manipulation — not a mask of
  the low five bits.

### The getter makes the absence pointed

Of the 14 short functions in the image that return a dword from `[rcx+0x20]` or `[rcx+0x28]`,
exactly one extracts a bit, and it extracts **bit 1**:

```
0063CB50   mov eax, dword ptr [rcx+0x28] ; shr eax, 1 ; and eax, 1 ; ret
```

It is the derived member class's override of vtable slot `+0x50` (`00D58100+0x50`; the base's
slot `+0x50` is `00633FB0`). The engine publishes an accessor for bit 1 and **publishes none for
bits 3–4**.

### Nor are they copied out

A serialized class tag would fit "near-per-class constant", so the block was checked for the word
being propagated. Within `0062E000`…`00641000` the word is never stored anywhere but back into
`+0x28` itself — the 13 stores are the registration's own temporary `or eax, 2` / restore pair
(`006329F1`, `00632AF5`, `00632C60`, `00635D6A`) and unrelated `+0x3C` alignment writes in the
descriptor constructors. **Bits 3–4 do not reach a buffer, a file image or a callee.**

### The claim, and its limits

**In this image, attribute bits 3–4 are registration-time metadata with no runtime consumer.**
Combined with the prior finding that the attach path does not read them and that they are not
determined by the descriptor template, the remaining live hypothesis is a **build-side or
tool-side annotation** that the runtime carries and ignores — consistent with their being a
near-per-class constant.

Not covered by these instruments, and therefore not claimed as impossible: a comparison against a
**non-immediate register**, a **jump table** indexed by the value, and any consumer in code whose
function bounds were not recovered. None of those would change the layout consequences, which are
nil either way: **no field width, offset or extent in the type store depends on bits 3–4.**

## 14. How a Phyre object is created, and where its unregistered bytes come from (2026-09-19, OPUS)

242 declared gap rows across 142 Phyre types carried an explicit `NO LIFETIME VERDICT`, placed
there because the allocation paths had not been read. They have now been read end to end, and the
answer overturns the obvious assumption: **the bytes no member registration covers are not
untouched, and they are not zeroed by the allocator. They are copied.**

### `PCluster::create`, `0063A990`

```
    test byte [descriptor+0xFC], 8
        -> "Class '%s' has no default constructor and cannot be allocated with
            PCluster::create()"        (00D58750)          so +0xFC bit 3 = not constructible
    size = [descriptor+0x38] * count
    block = 00639510(...)                                   the storage
    for (i = 0; i < count; ++i) {
        0063C910(descriptor, block + i * [descriptor+0x38]) the per-instance initialiser
    }
```

### The storage is never cleared

`00639510` reaches `00639750`, which is a **bump allocator inside the cluster arena** — align the
running offset at `[arena+0x14]`, bound it against the capacity at `[arena+0x10]`, return
`[arena+8] + offset`, store the new offset. No write to the returned block at all. When the arena
cannot satisfy the request, `00639780` falls back to `0017D260`, the `_aligned_malloc` wrapper —
which also does not clear. **Whatever a new object's bytes are, the allocator did not put them
there.**

### The initialiser copies the whole instance

`0063C910`, one of the four functions that tests attribute bit 1:

```
    rdx = [descriptor+0xC0]
    if (rdx) { r8d = [descriptor+0x38] ; rcx = instance ; call memcpy }   <-- FULL instance size
    else       call [descriptorvtbl+0x50](descriptor, instance)
```

The length is `[descriptor+0x38]` — the whole object, not a member walk. So every byte of a new
instance, **including every byte this document's member table does not describe**, is a verbatim
copy of the class's *default instance*.

### The default instance is a static object in `.bss`

`0063DC80` is a one-instruction setter, `setDefaultInstance(descriptor, ptr)`, called from **384
sites** — one per class, inside the class's descriptor constructor, e.g. `PClusterHeader`'s
`00597690` passes `02CA9C00`. Of the 246 class descriptors in this schema, **173 had their
constructor located and all 173 register a default instance**, and **all 173 pointers land in the
`.bss` part of `.data`** (virtual size `0x11A7530` against raw size `0x18E400`). So the PE loader
zero-fills that storage and the class's static constructor writes over it during startup.

The full table — class, descriptor, default instance, descriptor constructor, instance size — is
`members/phyre-default-instances.tsv`.

### What this licenses, and what it does not

**Established:** an unregistered span in a `PCluster::create`d object is **deterministic and
identical for every instance of that class**, because every instance is a copy of one static
object.

**Not established: that the value is zero.** An unregistered byte is not an uninitialised one.
Phyre registers what it exposes to serialisation and script, so a private member that the C++
constructor sets is precisely the kind of byte that appears here as a gap. The storage starts
zero-filled, but the static constructor runs over it and `.bss` has no raw bytes in the image, so
the values cannot be read statically at all. That is routed as
`OPUS-REQ-ASTRA-PHYRE-DEFAULT-INSTANCE-BYTES`: one post-startup read of the 173 addresses, about
20 KB, which would convert 236 gap rows from "deterministic but unknown" to actual values and
would independently test the prototype-memcpy model — the bytes at a *registered* member's offset
must agree with what its registration implies.

**Out of scope here:** objects that arrive by cluster **load** rather than `PCluster::create`.
Their bytes come from the file image and are a different question with a different answer.

### Effect on the type store

236 of the 242 gap rows now carry this mechanism as their lifetime, over 138 types. Lifetime
coverage of declared spans went **306/548 → 542/548 (98.9 %)**. The 6 still outstanding belong to
`CD3D11_BLEND_DESC`, `CD3D11_DEPTH_STENCIL_DESC`, `CD3D11_RASTERIZER_DESC` and
`D3D11_RENDER_TARGET_BLEND_DESC` — Direct3D's own structures, which have no Phyre class descriptor
and to which none of this applies.

## 15. The other creation route: a cluster LOAD (2026-09-19, OPUS)

Section 14 covers objects made by `PCluster::create`. An object that arrives by **loading a
cluster** takes a different route, and section 14 deliberately refused to speak for it. It can now
be spoken for, at a stated strength.

### The unpack path

`0059E070` builds a context and calls `0059E300`, which is the unpack: it reads
`m_instanceListCount` from the header at `[cluster+0x10]`, allocates two `instanceListCount * 8`
pointer arrays at `[cluster+0x28]`, and drives the three fixup appliers —

| applier | fixups | diagnostic |
|---|---|---|
| `0059C250` | array | *"Array fixup refers to array '%s::%s' not in current runtime"* |
| `0059C700` | pointer | *"Pointer fixup refers to array '%s::%s' not in current runtime"* |
| `0059CE30` | pointer array | *"Pointer array fixup refers to array '%s::%s' not in current runtime"* |

and `0059E880` resolves them (*"Resolving fixup for '%s' returned NULL pointer"*).

### Three findings, and they agree

1. **The unpack never re-initialises an object.** Neither `0059E300` nor anything it reaches
   within three call levels calls `0063C910` (the default-instance memcpy) or `PCluster::create`.
   A loaded object is therefore *not* given the class's default instance.
2. **Its memsets do not touch object storage.** All three clear the per-list bookkeeping pointer
   arrays at `[cluster+0x28]`, `instanceListCount * 8` bytes each (`0059E3D3`, `0059E3E4`) or a
   similar table (`0059E690`).
3. **Objects are sized at full instance width.** The sizing loop `0059D6A0` computes, per
   instance list, `descriptor[0x38] * m_count` — the whole instance per object, not a member walk
   — then adds `m_arraysSize` and `m_pointersInArraysCount * 8`, aligns by `descriptor[0x3C]`,
   and branches on `descriptor+0xFC` bit 2 to take `m_objectsSize - instanceSize*count` when the
   file's object size differs from the runtime's.

### The verdict for a loaded instance

**The bytes come from the cluster file**, and the only writes into them afterwards are the fixup
appliers patching pointer-sized slots. So, across both routes:

* **created** — a copy of the class's static default instance (§14);
* **loaded** — the bytes authored in the cluster file.

**In neither case is an unregistered span zeroed by the allocator or left as heap residue.** That
is the useful fact for a reconstruction: these bytes are always *someone's* authored value, never
garbage.

### Stated limit

The read of the objects blob out of the stream into the arena has **not** been traced instruction
by instruction. The load-side claim rests on the absence of any re-initialisation, the memsets
being accounted for, and the full-instance-width sizing — not on following the copy itself. That
is enough to rule out "zeroed" and "undefined" and to place the provenance in the file; it is not
enough to describe the copy's exact mechanics, and no row claims otherwise.

### Descriptor fields recovered along the way

`descriptor+0xFC` is a flags word: **bit 2** (`0x04`) the file object size may differ from the
runtime instance size, **bit 3** (`0x08`) not constructible via `PCluster::create`. Bit 1 is
cleared explicitly by some registrars (e.g. `00166080` for `PWorldMatrix`,
`and dword [02E405AC], 0xFFFFFFFD`). `descriptor+0xE0`/`+0xE4` participate in the per-list
footprint as a count and an alignment. `descriptor+0xC0` is the default instance (§14) and
`descriptor+0xF4`/`+0xF8` are the offset adjustments, ~~both zero (§12)~~ sums of `+0xF0` up the parent chain *(corrected 2026-10-02, OPUS: `0063E410`, `0063E416`-`0063E448`; §16 below)*.

## 16. CORRECTION — `classdesc+0xF4` is **not** zero (2026-09-19, OPUS, same day)

Section 12 above asserted that `classdesc+0xF4` is zero and that the recorded member offsets are
therefore true in-instance offsets. **That is wrong, and this section overrides it.**

### How the error was made

The evidence was a sweep of every write to displacement `0xF4` in `.text`, filtered to the
`mov` family. A **running sum uses `add`**, and `0063E410` is exactly a running sum:

```
0063E410  xor  r8d, r8d
          mov  dword [rcx+0xF4], r8d          ; zero it
          lea  r9, [rip -> 02CF8270]          ; the root descriptor
      +-> cmp  rax, r9 / je out               ; stop at the root
      |   mov  ecx, dword [rax+0xF0]
      |   add  dword [rdx+0xF4], ecx          ; <-- ACCUMULATE
      +-- mov  rax, qword [rax+0x78]          ; the parent
```

So `+0xF4` is the sum of `+0xF0` over the descriptor and its ancestors. It is zero only if every
`+0xF0` in the chain is zero — and they are not. `+0xF0` is **arg7** of the descriptor
constructor (`00632D80: mov eax,[rsp+0x38]; mov [rcx+0xF0],eax`), and across all calls to
`00632D80`/`00632C90`: **298 pass 0, 16 pass 8, one passes 1, one passes -2, 69 pass `r15d`** and
one passes `eax`.

This was already recorded. `PCD-5` in `CONTRACT-phyre-class-descriptor.md` — closed by FABLE on
2026-09-14 — describes `0063E410` accumulating `+0xF4` and `+0xF8` down the parent chain. Reading
the contract for this subsystem before asserting a fact about its descriptor would have caught it
immediately. **That is the sixth time this session that the answer was already in the subsystem
directory.**

### What the true value is, per class

Resolving arg7 per class and summing over the parent chain (`+0x78`, stopping at `02CF8270`):

| `+0xF4` | classes |
|---|---|
| `0` | 126 |
| **`0x8`** | **27** |
| unresolved (a register argument somewhere in the chain) | 26 |

The 27 with `0x8` include `PNode`, `PAnimatableComponent`, `PAtmosphericsBase`,
`PDeferredLightingBase`, `PDynamicMesh`, `PDynamicMeshInstance`, `PPhysicsShapeBase`,
`PPhysicsCharacterCamera`, `PPostEffectBase`, `PScriptableComponent`, the whole `PInputSource*`
family and the post-processing bases. Per-class values are in the working table
`f4_per_class.tsv`.

### What is now reopened, and what is not

**REOPENED — `OPUS-PHYRE-F4-OFFSET-ADJUSTMENT`.** The four accessors compute the slot as
`instance + (member.offset - classdesc[0xF4])`. For the 27 classes with `+0xF4 = 8`, the recorded
offset and the in-instance offset therefore **differ by 8 unless the pointer those accessors
receive is itself offset by 8**, which is plausible — `0063C910` performs a *separate* adjustment
using `+0xF8` (`mov eax,[rcx+0xF8]; neg eax; movsxd rbx,eax; add rbx,rdx`), and two compensating
adjustments would cancel. **Which it is has not been determined, and this document does not
guess.** Until it is, offsets for those 27 classes and the 26 unresolved ones are provisional.

**NOT AFFECTED — the widths.** Section 12's width result comes from which handler the attribute
bit selects (`type-vtable +0x28` storing one qword versus `+0x18` copying the value) and does not
reference `+0xF4` anywhere. All 201 width rows stand; each now carries this correction inline and
says so explicitly.

**NOT AFFECTED — the instance sizes**, the default-instance mechanism, or the cluster-load
findings. None of them uses `+0xF4`.

## 17. `+0xF4` resolved: the offsets were right, the reasoning was not (2026-09-19, OPUS)

Section 16 reopened whether the recorded member offsets are in-instance offsets, because the
premise supporting that claim — "`+0xF4` is zero" — turned out to be false. The question is now
closed, and the original **conclusion survives on completely different evidence**.

### The accessor and the initialiser agree on the base

`0063E410` computes two running totals down the parent chain: `+0xF4` as a plain sum of `+0xF0`,
and `+0xF8` as the same sum with each term clamped at zero. Only **one** call in the image passes
a negative `+0xF0` (`-2`, at `005A034A`), so for everything else the two totals are identical —
measured across all 153 classes where both resolve, **`+0xF4 == +0xF8`, zero differences**.

That matters because the two consumers use different ones:

* the four member accessors subtract **`+0xF4`**: `slot = instance + (member.offset − [desc+0xF4])`
* the per-instance initialiser `0063C910` subtracts **`+0xF8`**:
  `mov eax,[rcx+0xF8]; neg eax; movsxd rbx,eax; add rbx,rdx`

Equal values mean both resolve a runtime object pointer to the **same layout base**,
`pointer − F4`. There is no disagreement between them to reconcile.

### The offsets are measured from that layout base

Two checks, and the second is decisive:

* every recorded offset in all **27** classes with `F4 = 8` lies inside `[0, instanceSize)` — 27
  of 27, none negative, none at or past the size;
* **`PNode` has a member recorded at offset `+0x0`.** If the recorded offsets were relative to the
  object pointer and needed 8 subtracted, `PNode`'s first member would sit **8 bytes before the
  object**. It does not.

So the recorded offsets are layout-base-relative, which is exactly what a layout store wants, and
**no field row needs its offset adjusted.** Section 12's conclusion stands; section 12's *reason*
was wrong and section 16 records why.

### What the `+0xF4` machinery actually means for a reconstruction

Only this: for the 27 classes with `F4 = 8`, a **runtime object pointer is `layoutBase + 8`**.
Converting a live pointer to a field address is `(pointer − 8) + offset`, not `pointer + offset`.
For the other 126 the two are the same. Per-class values, including the 26 whose chain contains a
register-valued `arg7` and are therefore **unresolved rather than assumed zero**, are in
`members/phyre-class-f4-offset-adjustment.tsv`.

### The lesson, which is not the one I expected

A false premise supported a true conclusion for most of a session. The conclusion was never
tested on its own — it was inherited from the premise. What finally settled it was a property of
the *data* (`PNode`'s member at `+0x0`, offsets fitting the declared extent) rather than a
property of the code, and that check cost a minute and was available the whole time. **When a
conclusion rests on a single premise, test the conclusion directly as well**; otherwise the day
the premise falls, everything built on it falls with it, and here that would have been 201 rows.

---

## §18. What the reflection metadata does NOT describe — 70.4 % of the bytes (2026-09-19, OPUS)

The schema recovered here is 682 members over 180 classes, and every one of them is a real,
named, typed field taken from the engine's own registrar. **It is also a minority of the object.**

For each of the 177 classes with a known instance size, take the offset of its **first** registered
member. Everything below that offset is instance memory the reflection system never mentions:

```
total instance bytes over 177 sized classes      : 34,780
bytes BELOW each class's first registered member : 24,486   (70.4 %)
```

| class | size | first member | unreflected prefix |
|---|---|---|---:|
| `PDeferredLightingBase` | `0x41D8` | `0x40D0` | **16,592 B** |
| `PMotionBlurBase` | `0xD68` | `0xD10` | 3,344 B |
| `PCameraOrthographic` | `0xD8` | `0xD0` | 208 B |
| `PCameraPerspective` | `0xD8` | `0xD0` | 208 B |
| `PCameraProjection` | `0xD0` | `0xC8` | 200 B |
| `PShadowSplit` | `0xE8` | `0xC8` | 200 B |

### The prefix is the base subobject, and the camera family shows it plainly

`PCameraOrthographic` and `PCameraPerspective` are both `0xD8` with their first member at `0xD0`
— and `0xD0` is exactly `PCameraProjection`'s size. Each registers **its own** members and inherits
the rest. **So a Phyre class descriptor registers the derived class's own fields and says nothing
about its bases**, which is the ordinary C++ reflection arrangement and is worth stating because it
determines what this metadata can and cannot give a reconstruction.

> **AND A SIZE MATCH IS NOT A BASE IDENTIFICATION.** 84 of the 177 prefixes equal *some* class's
> size, but most of those matches are collisions: `PPhysicsTaperedCapsule`'s `0x80` prefix equals
> the size of `PBlendableAnimationSource`, `PDepthOfFieldBase` **and** `PIndexDataBlockD3D11`, none
> of which is plausibly its base. The camera case is convincing because the **names** agree as well
> as the numbers. **The 84 are a lead list, not a hierarchy**, and no base edge is asserted here
> from arithmetic alone.

### What this means for the type store

The store's large Phyre `unobservedSpan0000` rows — `PDeferredLightingBase +0x0000` at 16,592 B,
`PMotionBlurBase +0x0000` at 3,344 B — are now characterised rather than merely open:

> **They are not "nobody has looked".** They are the region the engine's own metadata **does not
> describe by construction**, because the registrar enumerates a class's own members only. A
> reconstruction gets roughly **30 %** of Phyre object bytes free from the reflection data and must
> recover the other 70 % the hard way, from base-class disassembly.

That is a **reconstruction-readiness** figure, not a coverage complaint, and it is the first
measurement of how far this metadata reaches. **No row is renamed and no gap is consumed** — the
spans keep their extents and gain a reason.

### The one class where the descriptor's own RTTI was read

`PDeferredLightingBase`'s registrar `006442E0` installs vtable `00D5A4C8` on the **descriptor**
`02CF9970`, whose RTTI locator `01D18B90` names
`PClassDescriptorAbstract<PPostProcessing::PDeferredLightingBase>` with **12 base classes** —
`PClassDescriptor`, `PType`, `PHashEntryConst`, `PRedBlackTreeNode`, `PMemoryBase`, `PBase`,
`PAnnotatable` and others, at `mdisp` 0, 8, 0x20, 0x30, 0x50, 0x60. **That is the descriptor
object's hierarchy, not the described class's** — a distinction easy to lose, since both are
reachable from the same registrar, and the instance's own hierarchy is not available this way.

*(OPUS 2026-09-19. Measured from `phyre-field-schema.tsv` and `members/phyre-class-instance-sizes.tsv`
as they stand at HEAD; 680 of the schema's 682 rows are already carried in `_types/fields.tsv` at
the exact type and offset, so the schema side of the propagation is complete *(answered: see §20, corrected 2026-09-27 - four more registrations were added; 2026-10-02, OPUS)* and this is about what
the schema never had.)*


## §18a. And everything it DOES describe is already banked — 684 of 684 (2026-09-22, OPUS)

§18 measures what reflection never mentions. The complementary question decides whether any work
is left in the instrument itself: **of the members reflection DOES name, how many has the type
store not absorbed?**

It is answerable exactly, because both artifacts are on disk. For each registered member, take its
offset and find the field row of that type containing it — a **named** row, or an
`unobservedSpan`. A member landing in a gap would be evidence this store harvested and never
absorbed.

```
registered members                                  684 across 182 classes
members whose class has no field rows at all          0
members that land on a row                          684
... of which land on a NAMED row                     684   (100.0 %)
... of which land inside a declared gap                0
```

~~**There is no unfinished harvest anywhere in this category.**~~ **Corrected 2026-09-27 (OPUS), §20: the 684 are the members registered through `00632960` plus four of the 29 `00632A70` sites. 211 further member registrations were never harvested - 165 through the array constructor `00632A10`, 25 more through `00632A70` and 21 through the enum constructor `00632BE0` - so the sentence held for one constructor, not for the category.** Both controls are in those numbers: a
class-name mismatch between the two artifacts would appear as members that cannot be placed, and
there are none; a partially absorbed schema would appear as a named/gap mix, and it is 684 / 0.

### This corrects a steering claim I published the same day (OPUS)

`L2-VERDICTS.md` § "Two thirds of S-49's debt is where reflection cannot see" splits the debt on
`regcalls` and calls the `regcalls > 0` bucket *"the harvest reached the class and stopped"*. That
phrase was a hypothesis dressed as a measurement. The split is a true statement about **how much
reflection said** per class and not about **how much is left to take**, and the answer to the second
question is: nothing.

Read beside §18, the pair says something stronger than either alone — ~~**reflection's entire
contribution to category 22 is banked, and every remaining unexplained byte is one the engine never
reflected.** Re-running any generator here produces exactly nothing, and that holds for all 25,666
bytes rather than two thirds of them.~~ *(Struck 2026-09-27, OPUS: false as worded - 211 member registrations were never harvested; see §20 and `RM-1`.)* *(The verdicts section itself is not amended here: that file
currently carries a peer's uncommitted contract-column rescore, and the correction is filed as
`OPUS-S02-CELL-READY-BUT-THE-VERDICTS-FILE-IS-A-PEERS` alongside the S-02 cell that is waiting on
the same file.)*

## §19. The base class explains 10.6 % of that, not 70.4 % — the chain, and a prediction that failed (2026-09-19, OPUS)

§18 measured that **24,486 bytes — 70.4 % of the reflected Phyre instance bytes — lie below each
class's first registered member**, and the obvious reading is that those bytes are the base class:
Phyre registers only a class's *own* members, so a child's schema should begin where its parent's
instance ends. **The reading is testable and it is mostly wrong.**

### Where the parent actually comes from

The class-descriptor constructor's **6th argument**:

```
00632D80(rcx = descriptor, rdx = sub-object, r8 = name, r9d = size,
         arg5 = alignment, arg6 = PARENT DESCRIPTOR)

  00632DD1  mov  rax, qword ptr [rsp + 0x30]     arg6, as the CALLEE sees it
  00632DD6  mov  qword ptr [rcx + 0x70], rdx
  00632DDA  mov  qword ptr [rcx + 0x78], rax     -> +0x78, the parent slot
```

`CONTRACT-phyre-class-descriptor.md` already documents `+0x78` as *"the parent descriptor, or
null"*; this reads the value that lands there, which no file carried. **The caller writes arg6 at
`[rsp+0x28]`, not `[rsp+0x30]`** — the call pushes a return address between the two frames, and
reading the callee's offset in the caller finds a parent for 12 registrars by coincidence instead
of 70 by construction.

**The descriptor address is not inside the registrar.** Most registrars take it as their own
parameter — `FUN_005A7ED0` opens `mov [rsp+8], rcx` / `mov rbx, rcx` and passes it straight
through — so a `lea rcx` search inside them recovers **4 of 177**. It is in the registrar's
*callers*, which do `lea rcx,[descriptor]` / `call <registrar>`: sweeping for that pair recovers
**177 of 177 with no ambiguity**. The result is `members/phyre-class-parent-chain.tsv`.

**Both controls pass with no violations, 57 comparable rows each:** no parent is larger than its
child, and no child places a registered member inside its base. Those are the two things that
would have to hold if `+0x78` really is the base class, and they do.

### And then the prediction failed

Before reading the table I wrote down that `PDeferredLightingBase`'s parent should be about
`0x40D0` bytes, because that is where its first member sits and the whole point of the exercise
was that the base explains the prefix.

> **Its parent is `PPostEffectBase`, and `PPostEffectBase` is `0x50` bytes.**

So `0x50`–`0x40D0` — **16,512 bytes** — belongs to neither the base class nor any registered
member. Across the population:

| | bytes | |
|---|---|---|
| below the first registered member, 89 classes | 24,486 | |
| **explained by the base class** | **2,586** | **10.6 %** |
| still unexplained | 21,900 | 89.4 % |

### Where the remainder actually is, which the failure makes visible

It is not spread across the population. **Two classes hold 90 % of it**, and they are siblings:

| class | unexplained prefix | first member | parent |
|---|---|---|---|
| `PDeferredLightingBase` | **16,512** | `0x40D0` | `PPostEffectBase` (`0x50`) |
| `PMotionBlurBase` | **3,264** | `0xD10` | `PPostEffectBase` (`0x50`) |
| everything else, 87 classes | 2,124 | | |

Both are post-effect objects sitting on the same `0x50`-byte base, and both carry a large
unreflected region before their first registered member. That is the shape of **fixed-size buffers
the class owns and does not expose to serialisation** — plausibly light or tile arrays for the
deferred-lighting object — but *plausibly* is the operative word: **no reader of those bytes has
been traced, and nothing here justifies naming them.** The value of the failed prediction is that
it turns a 70.4 % population-wide mystery into a 2,124-byte population-wide residue plus **two
specific objects to go and read**.

`PPostEffectBase` itself has no parent in the recovered set, and the `PPhysics*` family's parents
resolve to descriptors outside the 177 — those rows say so rather than guessing.


### §19a. Propagated into the type store: 57 base-class rows, 35 of them exact

The chain is not just a table. Every one of the 177 classes is a declared type in `_types/`, and
for the 57 with a resolved parent the offset-0 `unobservedSpan0000` row has been **split**:
`[0, parent.instance_size)` becomes `baseClass_<Parent>` and whatever remains stays unobserved.

**For 35 of the 57 the split leaves nothing behind** — the entire offset-0 unknown span is
*exactly* the base class, to the byte. `PAnimationController` is `0x18` of `PAnimationDataSource`
and nothing else below its first member; `PCameraOrthographic` is `0xD0` of `PCameraProjection`;
`PAnimationChannel` is `0x48` of `PAnimationChannelBase`. For the other 22 the row states the
leftover explicitly as *"not the base class … and not a registered member of this class either"*.

**2,586 bytes move from UNKNOWN to a named base subobject**, and the store's overall unknown
fraction is now 10.5 %.

> **What the new rows claim is deliberately narrow: the EXTENT, not the contents.** Those bytes
> are the base subobject and are registered against the parent class, so they are the parent's
> rows to fill. Nothing here invents a field. This is the difference between *"16 unexplained
> bytes"* and *"derive from `PComponent`"* — the second is what a reconstruction needs, and it is
> all that has been established.


### §19b. Five controls, and what the shape of the chain says

Two controls were designed in before the table was built; three more are structural and were run
after, on the table as a graph rather than row by row.

| | | |
|---|---|---|
| 1 | `parent.instance_size <= child.instance_size` | 57 comparable, **0 violations** |
| 2 | child's first registered member `>=` `parent.instance_size` | 57 comparable, **0 violations** |
| 3 | the chain is **acyclic** | **0 cycles** |
| 4 | size is non-increasing along **every whole chain**, not just one hop | **0 violations** |
| 5 | chain depths inside the recovered set | 54 at depth 1, 3 at depth 2 |

The deepest chain is `PAnimationChannel` (`0x68`) → `PAnimationChannelBase` (`0x48`) →
`PAnimationChannelTarget` (`0x38`) — monotone, and each step leaves exactly the room the child's
own members occupy.

**Controls 3 and 4 matter because they cannot be satisfied by accident.** A misread pointer field
would produce cycles or an inversion somewhere across 57 edges; neither appears. Control 5 says
something about the corpus rather than the method: **the registered Phyre hierarchy here is
shallow.** *(answered: see §19c - this reading of control 5 was wrong; 2026-10-02, OPUS)* Almost everything is one step from a root, which is consistent with Phyre exposing leaf
data classes to reflection and keeping deep implementation hierarchies unregistered.

**Of the 177, 70 carry a non-null parent and 57 resolve to a class inside the set.** The other 13
point at descriptors outside it — the `PPhysics*` family — and their rows say
`(descriptor not in this set)` rather than `(no parent / root)`. **The remaining 107 genuinely
record a null parent.** Those three populations are kept apart in the table because collapsing
them would turn "we did not find it" into "there is none".


### §19c. CORRECTION, same session: the population is 330 classes, and the hierarchy is not shallow

§19–§19b were written against the 177 rows of `members/phyre-class-instance-sizes.tsv`, because
that was the table I had. **That table is one registrar shape, not the population.** Sweeping the
image for every call to `00632D80`/`00632C90` and reading the class name out of `r8` finds **400
construction sites, 330 of them named** — and the difference is not cosmetic:

| | against 177 | against 330 |
|---|---|---|
| descriptor addresses recovered | 177 | **330** |
| classes with a non-null parent | 70 | **182** |
| parents resolved to a class in the set | 57 | **181** |
| unresolved parents (`descriptor not in this set`) | 13 | **1** |

The 13 unresolved parents were an artefact of the small population. Twelve resolve immediately:
all eight `PPhysics*Base` classes derive from **`PPhysicsShape`**, `PAnimationDataSource` from
`PAnimationHierarchyNode`, `PShaderProgramD3D11` from `PShaderProgramBase`, and both time
controllers from `PTimeController`. One — `PClassCallableMethodScript`'s parent `02CF8680` —
remains unnamed and its row says so.

> **And §19b's reading of control 5 was wrong.** It said *"the registered Phyre hierarchy here is
> shallow … almost everything is one step from a root, consistent with Phyre exposing leaf data
> classes and keeping deep hierarchies unregistered."* That was a conclusion about the corpus
> drawn from a **subset chosen by a tooling accident**. Over the real population the depths are
> **1:95, 2:46, 3:27, 4:7, 5:6**, and the deepest chain is six levels of physics shape:
>
> `PPhysicsBox` (`0x88`) → `PPhysicsBoxBullet` (`0x88`) → `PPhysicsBoxBase` (`0x80`) →
> `PPhysicsShape` (`0x70`) → `PPhysicsShapeBullet` (`0x70`) → `PPhysicsShapeBase` (`0x68`)
>
> **A statement about a corpus is only as good as the census behind it**, and "almost everything
> is one step from a root" was a statement about my population, not about Phyre.

**All five controls still pass on the larger graph**: 181 comparable for the size test and 69 for
the first-member test, both with 0 violations; 0 cycles; 0 inversions along any whole chain.

The base classes with the most children are `PInputSource` (25), `PPostEffectBase` (13),
`PShaderParameterCaptureBufferTextureBase` (13), `PPhysicsShape` (8), `PComponent` (6) and
`PAnimationDataSource` (6).

**Store propagation, final:** **69 `baseClass_` rows, 3,531 bytes**, of which 42 are exact — the
whole offset-0 span is the base class to the byte. The store's unknown fraction is **10.4 %**.
Nothing else about §19's central result changes: **the base class still explains only about a
tenth of the bytes below first-registered-member**, and `PDeferredLightingBase` and
`PMotionBlurBase` still hold 90 % of the remainder.


### §19d. The whole residue is one family, and it is not the one with the most children

With all 330 classes carrying a size and a parent, the unexplained prefix can be attributed by
base-class family rather than by class. It collapses almost entirely into one:

| base class | size | children | own bytes across the family | **unexplained above the base** |
|---|---|---|---|---|
| **`PPostEffectBase`** | `0x50` | 13 | 34,000 | **19,813** |
| `PComponent` | `0x18` | 6 | 464 | 32 |
| `PInputSource` | `0x28` | **25** | 128 | 48 |
| `PPhysicsShape` | `0x70` | 8 | 136 | 48 |
| `PShaderParameterCaptureBufferTextureBase` | `0x10` | 13 | 144 | **0** |
| `PAnimationDataSource` | `0x18` | 6 | 104 | 16 |

**`PInputSource` has the most children and the least to explain** — 25 subclasses, 128 bytes of
own state between them, 48 unexplained. `PInputSourceJoypadButton`, `PInputSourceKey` and the
mouse-delta pair are `0x40` each with their first registered member at `0x30`; the motion-velocity
classes are `0x28`, exactly the base, with nothing of their own at all. That family is finished.

**`PPostEffectBase`'s 13 children hold 19,813 of the ~21,900 unexplained prefix bytes — 90 %.**
Two of them, `PDeferredLightingBase` (16,512) and `PMotionBlurBase` (3,264), are 90 % of *that*.

> So the residue is not a property of Phyre reflection, and it is not spread thin across the
> engine. **It is one family of post-effect objects that carry large fixed buffers they do not
> expose to reflection**, sitting on a shared `0x50` base. Everything else in the recovered
> hierarchy is explained to within a few dozen bytes per family.

Where that leaves the next reader: the post-effect family's buffers are `.bss`, so they are zero
at load and written at runtime — **the readers, not the contents, are the way in**, and §19c's
default-instance sweep has already shown nothing writes them statically.

## SWE2-EC7-61 update (2026-09-19) - `00597220`

`00597220` (152 B) is the duplicate-name check the member-registration page names - call-free sentinel-list walk at `[r11+0x80]`, per-node string compare on `[r9+0x20]`. Interior anchor `00597260` (the `[r9+0x20]` node-string load).



### §19e. CORRECTION: 330 is my coverage, not the population — the population is 409

§19c said *"the population is 330 classes, not 177"*. **That is wrong, and the right number was
already in the database.** `AUDIT-LOG`, 2026-09-13, from an independent byte-template scan of the
return-value adapter family: **409 distinct reflected classes**, one adapter each, every one of
**1,185 of 1,185** `.rdata`/`.data` appearances walked back to a validated complete-object-locator
at slot 5. `AUDIT-LOG` line 20695 states it plainly — *"409 types are reflected of 2,248 RTTI
classes"*.

So the three numbers are:

| | |
|---|---|
| reflected classes in the image (independent census, 2026-09-13) | **409** |
| class-descriptor construction sites my sweep finds | 400 |
| of those, sites whose class name is readable from `r8` | **330** |
| the size table the store started from | 177 |

**My parent chain covers 330 of 409 — 81 %.** The old table covered 43 %. That is the honest
framing and it is a better one: the work now sits against an independent census instead of
against itself. What it is not is "the population".

The ~79 classes my sweep does not name are those whose construction site does not put a readable
string in `r8` — 70 of the 400 sites are unnamed for exactly that reason, and the remainder are
classes the constructor sweep does not reach at all. **Neither is a claim that they lack a
parent**; they are simply outside what this method sees, and the table says so per row.

> **This is the third correction in one session driven by not reading the audit log** — bx.1 (the
> refutation was in the page the row came from), bz.6 (six type names dispositioned two days
> earlier), and now a population figure established six days earlier. The failure is not the
> method in any of the three cases. It is starting the measurement before searching for whether
> somebody had already made it.

## What slot `+0x60` gives back: the 142 classes this schema does not cover

**2026-09-19 (OPUS).** Every Phyre class's *descriptor* vtable carries the class's member
registrar at slot `+0x60`. That is not asserted from position: followed through its one-target
thunk it reproduces **this file's own `caller` column on 173 of 173 covered classes, with 0
disagreements**, and this file found those callers by walking the member registrar's callers
without ever reading a vtable. Two derivations, no overlap, no conflict. The full table is
[`members/phyre-class-descriptor-vtable.tsv`](members/phyre-class-descriptor-vtable.tsv).

The useful part is the other 142. Of the 315 classes whose descriptor vtable is recovered, 142
have **no rows in this schema at all**, and until now that was an open question — missing work, or
nothing to find? Slot `+0x60` names a registrar for each of them, which makes it countable:
**how many member-registrar calls (`00632960` / `00632A70`) does each of those bodies contain?**

| | |
|---|--:|
| classes with no rows in this schema | **142** |
| ~~whose registrar registers **nothing**~~ whose registrar makes no DIRECT `00632960` / `00632A70` call | **139** ~~— the schema was complete about them~~ *(corrected 2026-09-27, §20: 19 of them register 25 array members; 120 register no data member)* |
| whose registrar registers something | **3**, four members between them |

~~**The 139 are a bounded negative with a working control**~~ *(corrected 2026-09-27, OPUS, §20: the control counted the same two constructors on the covered classes, so it proved the decoder was live, not that those two constructors were the only way to register a member)*: the same count over the 173 covered
classes returns between 1 and 9 for every one of them, so a zero is a real zero and not a decoder
that stopped seeing calls.

### The four members that were missing

Each is read from its own call site with the signature established in §4 — arg2 the owning class
descriptor, arg3 the member's type descriptor, arg4 the name, `[rsp+0x20]` the byte offset,
`[rsp+0x28]` the attributes:

| class | member | offset | type | site | how the type is known |
|---|---|--:|---|---|---|
| `PShaderPassParameterLocationTypesBase` | `m_parameterStart` | `0x0` | `unsigned short` | `005EA16A` | `006300A0()` returns `01F2E500`, which this schema already names `unsigned short` |
| `PShaderPassParameterLocationTypesBase` | `m_parameterCount` | `0x8` | `unsigned short` | `005EA1E3` | same getter |
| `PAnimationConstantChannel` | `m_value` | `0x48` | `float` | `005B0C36` | `006301F0()` returns `01F2E690`, which this schema already names `float` |
| `POctreeChildren` | `m_children` | `0x8` | `POctree` | `008786B5` | `lea 02EB9070`, POctree's descriptor in `phyre-class-parent-chain.tsv` |

**Two arithmetic checks that were not used to find any of this, so they cost nothing and are
worth something.** `PAnimationConstantChannel` is `0x58` and its base `PAnimationChannelBase` is
`0x48`; `m_value` lands at exactly `0x48`, the first byte after the base sub-object, which is
where a derived class's first own member has to be. And `POctreeChildren` is `0x288` with
`POctree` at `0x50`: `0x288 - 8 = 640 = 8 × 0x50`, exactly, with no remainder, in a class named
`OctreeChildren`.

**The count of 8 on `m_children` is arithmetic and is labelled that way in the store.** The
registrar's seventh argument is `8` at that site and agrees, but that argument is not a count —
profiled across the 682 existing sites it reads 3, 4, 2, 1, 6, 8, 0, 32 and 5. The reading it
beats, stated rather than left out, is one `POctree` at `+0x8` followed by 560 unread bytes, which
invents a hole the exact division says is not there.

All three classes carried a store row reading *"the Phyre reflection schema recovered NO..."*.
That sentence was true of the schema and false of the image, and all three are re-tiled.

## SWE2-EC7-80 update (2026-09-20) - `00595EF0` tag-dispatch field decoder measured

`00595EF0` (2,433 B) is the record reader `0059C250`/`0059CE30` run
against the byte stream at `[rbx]`: each element's tag byte splits
`& 7` into a seven-arm jump table at `0059D674`, and a rotated varint
(`ror r9d, 1` after the LEB128 accumulate) seeds every emitted
0x10-byte record at `rdi`. The arms: dense fill with per-record
`+4`/`+8`/`+0xC` varints (bit3 of the tag flags the `+8` field absent);
a count-prefixed run (`r15d < 0x100` takes the short byte form); a
sorted search through `005972C0` with `005971F0` the comparator; a
presence-bitmap arm advancing `rsi` every 8 elements and emitting
only set bits; a callback arm running `0059FF40(rdi, &stream, r12d)`
per record; and a triple-varint header arm whose first value strides
`r9` into the `+4` field. `rbp+0x38` carries the write cursor back.
Interior anchor `00595F50` (the first tag-byte fetch).

## SWE2-EC7-81 update (2026-09-20) - `0059FF40` dual varint read measured

`0059FF40` (122 B) is the per-record callback `00595EF0`'s arm
invokes: `r8b` bit0 skips or reads an LEB128 varint at `[rdx]` into
`dword[rcx]` (`ror r11d, 1` applied - the same rotated encoding as
the parent decoder), bit1 does the same for `dword[rcx+4]` into a
second varint at `[r9]`.
Interior anchor `0059FF60` (the first varint byte fetch).

## SWE2-EC7-120 update (2026-09-21) - `0063BBA0` measured

`0063BBA0` (21 B) is the
trampoline `0059C250`
calls: it loads
`rax = [rcx + 0x30]` as a
result and, when the
`+0x50` object exists,
tails its `vtable[+8]` -
the optional post-step
dispatch.
Interior anchor `0063BBB0`
(the `jmp [rax + 8]`).

## SWE2-EC7-121 update (2026-09-21) - `00632E80` measured

`00632E80` (293 B) is the
member-record ctor
`0059AC00`/`0062FB80`
call. `00632D80` runs the
base init with `rbx`'s
`+0x38` (negated) and
`+0x3C` fields; the vtable
becomes `00D58380`
(`[0] = 0063E2C0`, RTTI
`01D14D30`) and the
`+0x100..+0x130` records
zero with `+0x104` left
holding `rbx+0x38`.
`001C26B0(rdi)` produces
`+0x138`, `+0xFC |= 1`,
and `+0x30` takes the
pointer minus its low bit.
`0063E410` and `0063AE50`
run the resize pair,
`+0xFC` clears bit 31,
`00639A60`/`00639C80`
complete the registration,
and the `+0xC0` walk to
the `02E4E720` sentinel
ends with `rsi` stored at
`[[+0xF8] + rcx + 0x10]`
when `[+0x38] >= 0x18` -
indexed member-table
registration.
Interior anchor `00632F0C`
(the `001C26B0` call).

`005972C0` (319 B) is the varint-driven record emitter `00595EF0` runs per field: a 7-bit varint `ebp` read from cursor `[rdi]` gives the outer repetition count; each iteration reads `esi` — a single byte when `[r15+4] < 0x100`, else a second varint — then emits `esi` records: each writes the 16-byte template `[r12]` into the `[r14]` cursor (stride `0x10`) and calls `r13(rcx=slot, edx=index, r8=cursor, r9d=[r15])`. A final pass covers indices `ebx` up to `[r15+4]` with the same emit — a run-length-expanded list materializer.

Interior anchor `005972F0` (function `005972C0`).

## §20. The array, fixed-size and enum member constructors — 211 registrations the harvest never read (2026-09-27, OPUS)

**What this corrects.** Two claims of mine above were wrong as worded: §18a's "no unfinished harvest anywhere in
this category", and the slot-`+0x60` section's "139 whose registrar registers **nothing**". Both counted member
registrations as direct calls to `00632960` / `00632A70`. ASTRA's sentinel (`_experiments/evidence/phyre-array-registration-sentinel/`)
showed the counterexample: `PMeshInstanceSegmentContext`'s registrar `005E67C0` calls the **array** member constructor
`00632A10` at `005E6860` with name `m_streamBindings` and offset `0x38`; `00632A10` then forwards to `00632960` at `00632A41`,
so the direct count over the registrar is zero.

**The measurement, image-wide rather than from the one example.** Every small body that installs a `PClassDataMember*`
vtable (by RTTI, 147 family vtables) and is *called* rather than tail-jumped, and builds a node (calls the base `00632960` or its name initialiser `00632FB0`), is a member-node constructor. There are five:

| RTTI class installed | constructor | call sites | in `phyre-field-schema.tsv` |
|---|---|--:|--:|
| `PClassDataMember` | `00632960` | 682 | 682 |
| `PClassDataMember` / `PClassDataMemberArrayFixedSize` | `00632A70` | 29 | 4 |
| `PClassDataMemberArray` (template vtable swapped in by the caller) | `00632A10` | 165 | 0 |
| `PClassDataMemberEnum` | `00632BE0` | 21 | 0 |
| `PClassDataMemberDynamic` | `00632B30` | 1 | — |

(The 701 and 194 tail-jumps into `00633240` / `006332A0` are destructor restores, and `00633300`, which installs the dynamic vtable too, is that class's destructor; none is a registration.)

**The 139, recounted wrapper-aware** (`member_nodes`, now a column of
[`members/phyre-class-descriptor-vtable.tsv`](members/phyre-class-descriptor-vtable.tsv); `regcalls` is kept unchanged with its
domain stated): the old count reproduces on all 315 rows; all 176 covered classes stay at one or more; the new count is
never below the old; **19 of the 139 register 25 array members** through `00632A10`; **120 register no data member**, and 8
of those 120 register only reflected *methods* (the caller constructor `00632FB0` with `PMethodCallerConcrete` /
`PFunctionCallerConcrete` vtables, as on the scripting page). No registrar of the 120 reaches a member constructor within
two calls.

**What an array member IS, per instantiation.** The header is read from the member classes' own accessors, which are
shared across every instantiation: all 59 `PClassDataMemberPhyreArray<T>` vtables use `006065E0` / `006045B0`, all 10
`PClassDataMemberPhyreSharray<T>` vtables use `006065E0` / `0063B9B0`.

- `+0x0` u32 element count; bit 31 is stripped by every reader (`btr 0x1f`) and, when set, keeps the buffer from release:
  ~~the resizes `005C8BF0` / `006C7A40` and the adopts `0062A870` / `006A5950` call~~ the resizes and adopts (vtable
  slots 5 and 8, which are per element type - corrected 2026-09-27, OPUS; see the `+0x4` note at the end of this
  section) call `00584730` on the old storage only when
  bit 31 is clear, and an adopted caller buffer is stored with bit 31 set.
- `+0x4` four bytes no accessor touches; the load fix-up zeroes them with the count (see the `+0x4` note below).
- `+0x8` for `PArray<T>` the element-array pointer (`006045B0`: `mov rax,[field+8]`); for `PSharray<T>` the pointer when
  the count is above one, **the single element itself stored inline** when it is one (`0063B9B0` returns the address
  `field+8`), null at zero.
- The field address is `object + member[+0x48] − classdesc[+0xF4]`; for `PMeshInstanceSegmentContext` both chain terms are
  `0` (arg 7 of its descriptor constructor at `005D98AE`, and of `PMeshSegmentContext`'s at `006B850B`), so the member is at
  `+0x38` exactly and fills the class to its `0x48` end.

**`m_streamBindings`, the adjudicated field.** Native `+0x38`, 16 bytes, `PSharray<PMeshInstanceSegmentStreamBinding*>`, in a
`0x48` class whose own bytes run from `+0x28`. The file schema's offset `0` for the same name (ASTRA's `c1004` read) is a
different representation — serialized member order, not the native layout — and is not used here. `+0x28..+0x37` stays a
declared gap: the registrar registers exactly one member.

**The store.** `_types/fields.tsv` carries the 25 members: whole 16-byte rows where a member sat in a declared gap, the
existing count / gap / pointer rows annotated where accessor work had already carved the same header, and one width
corrected — `PInstancesComponent +0x18` was 8 bytes, taken from an accessor that returns the member's *address*
(`006AF560 lea rax,[rcx+0x18]`), and is the 16-byte `PArray<PTypedObject>`. `PString`'s `m_buffer` is an
`ArrayDynamic` member whose accessors call per-member callbacks, so reflection does not give its width and its rows are
unchanged. `PArray` and `PSharray` carry the header; ~~`PSharray`'s size is `0x10`.~~ `PSharray`'s size is not one number (corrected 2026-09-27, OPUS; see the correction at the end of this section).

**Evidence and regression:** `_experiments/evidence/phyre-array-member-registrations-opus/check.py` — the constructor
census, the recount with its controls, the 25 registrations with every argument resolved, the accessor census and bytes,
and mutants that reject "`regcalls` 0 means no member" (dropping `00632A10` from the constructor set reproduces the old
false negative on the sentinel) and "`PInstancesComponent +0x18` is 8 bytes".

**Not claimed.** What the elements mean; whether the guarded registrar runs in any given scene (the registration is
lazy); the `+0x4` dword's purpose; the other 186 unharvested registrations (`RM-1`) *(answered: see RM-1, ANSWERED 2026-09-27 - all 215 registrations of the three constructors are in the store; 2026-10-02, OPUS)*.

**Correction, 2026-09-27 (OPUS): a by-value `PSharray` holds its one element inline, so its size follows the element.**
The shared accessors fix the `PSharray` *header* for every instantiation. They do not fix its *extent*, and the store
had taken the pointer instantiations' `0x10` for all of them (`_index/candidates/psharray-inline-extent/`):

- **Native layout.** At count one the element is stored at `+0x8` itself, so the object is `8 + max(8, sizeof T)`.
  - ~~All nine `PSharray<T>` descriptors fit that: seven are `0x10` (pointer and `uint` elements).~~ **All TEN
    instantiations fit it (corrected 2026-09-28, OPUS).** Eight are `0x10`: the six pointer elements, `uint` and
    `PString`, which is by-value but only 8 bytes. `PSharray<PString>` was missed because its descriptor is built by
    `006316C0` (size `0x10` at `+0x38`), not by `00632D80`. So a by-value element is not automatically wider: a
    fixed-16 rule fails on the D3D11 pair, and a "by-value means wider" rule fails on `PString`.
  - `PSharray<PDataBlockBufferD3D11>` and `PSharray<PIndexDataBlockBufferD3D11>` are `0x50` (`0066A849`, `0066AB99`);
    their element classes are `0x48`.
  - `0066F970` / `0066FAB0` walk those elements at stride `0x48` from the inline address `+0x28` / `+0x20` when the
    count is one.
  - The two `m_buffers` members are therefore 80 bytes. Each ends exactly at the next registered member
    (`m_offsetInVertexBuffer +0x70`, `m_offsetInIndexBuffer +0x68`) and absorbs the 64-byte "unexplained" gap the
    16-byte carve had left behind it.
- **Serialized offsets.** The member address is `object + member[+0x48] − classdesc[+0xF4]` (`0063B9B0`). The file
  schema's member order is another representation and is not used for any width here.
- **The ownership flag.** Bit 31 of the count keeps a buffer from release (adopted storage). The resize `006C7A40`
  also never releases the inline address.
  *Completed 2026-09-28 (OPUS).*
  - **Bit 31 means adopted storage.** The slot-8 setters, which the cluster-load fix-up calls, keep the
    caller's buffer for any count other than one and set bit 31. At count one they copy the element inline
    and store a plain 1.
  - **Resizes own their storage.** A resize allocates owned storage and stores the plain count.
  - **No other count bit is used** by any of the ten bodies.
  - **Element lifetime differs by kind.**
    - Pointer and `uint` elements are copied as values and never owned.
    - D3D11 buffer elements are copied field by field, with no AddRef or Release, and are never destroyed
      by a resize.
    - `PString` elements are deep-copied, and freed only from owned storage.
  - Record: [`psharray_review.py`](../../_index/candidates/psharray-inline-extent/psharray_review.py).
- **Element semantics.** Not claimed. The two walkers hand each element's address to a device call with a
  buffer-description argument; that is the call's argument shape, not a meaning for the element's bytes.

**Not generalised.** `PArray`'s `0x10` is unanimous across its 60 descriptors and has no inline arm, so it is
unchanged. The six pointer members and the one `uint` member keep their 16-byte header (five as one row each,
`PMaterialSet`'s split word by word). The two widened rows keep the absorbed gaps'
evidence verbatim.

**The header `+0x4` dword, and which array functions are shared (OPUS, 2026-09-27;
`_index/candidates/phyre-array-header-plus4/`).**

- **Shared and per element.** The member vtables share slots 4, 6 and 7, the count and element accessors. The resize
  (slot 5) and set-from-buffer (slot 8) are **per element type**:
  - `PArray` has 45 resizes and 21 setters.
  - `PSharray` has five of each. For the two D3D11 buffer elements the setter `00672F30` copies the whole `0x48`-byte
    element inline at count one.
  - `005C8BF0` / `006C7A40` and `0062A870` / `006A5950` above are one family's functions, not the template's.
- **`+0x4` is cleared, never used on its own.**
  - The cluster-load array fix-up `0059C250` stores a zero **qword** at the field (`0059C5E8`). Only then does it call
    the member's slot-8 setter, which writes `+0` and `+8`.
  - A register-offset trace from the field address of all 79 slot entries finds no other `+0x4` access, including their
    tail targets and callees: 636 header accesses. Its controls are the count, the pointer and the inline copy, and a
    seeded `+4` write is reported.
  - An image-wide census of 812 bit-31 count loads agrees.
  - After a load the dword is 0. Alignment padding between the count and the 8-aligned pointer fits every observation;
    that is a reading, not a proof, because indirect accesses and untraced code are outside the reach. On the create
    path the bytes come from each class's default instance and are not read here.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-member-registration-and-the-recovered-fi-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `005A7B50` | 157 B | returns 0 when `rdx` or `rcx` is null; otherwise walks the circular list headed at `rcx + 0x90` (a link equal to the head ends it), skips nodes whose qword `+0x18` is null, byte-compares each node's `+0x18` string with the string at `rdx` up to the terminator and returns the first node that matches; when a list is exhausted it moves to the object at qword `+0x78` and repeats, returning 0 once that qword is null | `005A7B70`, `005A7B86`, `005A7BA3`, `005A7BC9`, `005A7BE4` |
| `006045B0` | 22 B | computes the signed offset dword `+0x48` of `rcx` minus dword `+0xF4` of the object at qword `+0x18` of `rcx`, and returns the qword at `rdx` + that offset + 8 | `006045B4`, `006045B7`, `006045C0` |
| `006065E0` | 24 B | computes the signed offset dword `+0x48` of `rcx` minus dword `+0xF4` of the object at qword `+0x18` of `rcx`, and returns the dword at `rdx` + that offset with bit 31 cleared (`btr 0x1f`) | `006065E4`, `006065E7`, `006065F0`, `006065F3` |
| `0062A870` | 124 B | addresses the record at `rdx` + (dword `+0x48` of `rcx` minus dword `+0xF4` of the object at qword `+0x18` of `rcx`, signed) and returns 5 when `r9d` is negative (signed); otherwise calls `00584730` on the record's qword `+8` when it differs from `r8`, is non-null and bit 31 of the record's dword `+0` is clear, then stores `r8` at qword `+8`, stores `r9d` with bit 31 set (`bts 0x1f`) at dword `+0` and returns 0 | `0062A89B`, `0062A8BD`, `0062A8CB`, `0062A8D0`, `0062A8DF` |
| `0062FB80` | 67 B | when `rdx` is non-null, calls `006373D0` (with `rcx` unchanged) and then `00632E80(rdx, that result, 0, the address 02CF8270)`; on both paths returns with `al` = 1 | `0062FB9E`, `0062FBA0`, `0062FBA8`, `0062FBB5`, `0062FBBB` |
| `0063B9B0` | 48 B | addresses the record at `rdx` + (dword `+0x48` of `rcx` minus dword `+0xF4` of the object at qword `+0x18` of `rcx`, signed) and reads its dword `+0` with bit 31 cleared: above 1 (unsigned) it returns the record's qword `+8`, at 1 it returns the address record + 8, and at 0 it returns 0 | `0063B9C5`, `0063B9CC`, `0063B9CE`, `0063B9D3`, `0063B9DB` |
| `00672F30` | 243 B | returns 5 when `r8d` is negative (signed); otherwise takes the old storage of `rcx` (qword `+8` when dword `+0` with bit 31 cleared is above 1 unsigned, the address `rcx + 8` when it is 1, null when 0); when `r8d` is 1 it copies the `0x48` bytes at `rdx` field by field to `rcx + 8` except that `+0x28` receives the address `00D68DD0` (copy skipped if `rcx + 8` is null), making `rcx + 8` the new storage and 1 the new count, else the new storage is `rdx` and the new count `r8d` with bit 31 set; calls `00584730` on the old storage when it differs from the new storage and from `rcx + 8`, is non-null and bit 31 of dword `+0` is clear; stores the new storage at qword `+8` unless it is `rcx + 8`, stores the new count at dword `+0` and returns 0 | `00672F43`, `00672F6A`, `00672FBD`, `00672FFD`, `00673011` |
| `006B66F0` | 15 B | stores `rdx` at qword `+0` of `rcx`, zeroes qword `+8` and returns `rcx` | `006B66F3`, `006B66F6` |
| `006C7A40` | 176 B | returns 0 at once when `edx` equals the whole dword `+0` of `rcx`; otherwise takes the old storage (qword `+8` when dword `+0` with bit 31 cleared is above 1 unsigned, the address `rcx + 8` when it is 1, null when 0) and calls `006C7450(rcx, edx, old storage, the unsigned minimum of edx and that count)`; when the result is null and `edx` is non-zero it returns 0xD, else it calls `00584730` on the old storage when that differs from the result and from `rcx + 8`, is non-null and bit 31 of dword `+0` is clear, stores the result at qword `+8` unless it is `rcx + 8`, stores `edx` at dword `+0` and returns 0 | `006C7A67`, `006C7A8C`, `006C7A90`, `006C7AC4`, `006C7AD1` |

`0063E010` (33 B, no direct call; slot 0 of the `PTypeDefault<short>` singleton) byte-swaps the 16-bit value at the second argument in place - low byte to high, the arithmetic high byte masked to `0xFF` into the low - and returns 1: the endian fix-up a `short` primitive field gets.

Interior anchor `0063E02D` (function `0063E010`).

`0063E040` (13 B, no direct call; slot 0 of `PTypeDefault<unsigned short>`) byte-swaps the 16-bit value in place with `rol ax, 8` and returns 1.

Interior anchor `0063E047` (function `0063E040`).

`0063E090` (61 B, no direct call; slot 0 of `PTypeDefault<float>`) reverses the four bytes of the 32-bit float at the second argument in place (`AABBCCDD` becomes `DDCCBBAA` through two masked shift pairs) and returns 1 - the same endian fix-up for `float` fields.

Interior anchor `0063E0C6` (function `0063E090`).

`0063CB50` (9 B, no direct call; slot 10 of `PClassDataMemberArray` and its dynamic-array derivatives) returns bit 1 of the member's flag dword `+0x28`.

Interior anchor `0063CB53` (function `0063CB50`).

`0063C4D0` (102 B, no direct call; slot 2 of `PClassDataMemberArray` and its derivatives) asks the member itself for three things through its own vtable - slot 4 (`+0x20`, a 32-bit result, with the object argument), slot 6 (`+0x30`, a pointer, with the same argument) and slot 9 (`+0x48`) - and tail-jumps to `00683A40` with the second argument, the slot-4 value, the pointer and the slot-9 result.

Interior anchor `0063C501` (function `0063C4D0`).

`0063D330` (140 B, no direct call; slot 3 of the same family) is the sibling with a choice: it takes the slot-4 value and a pointer from slot 7 (`+0x38`), then calls slot 10 (`+0x50`, which `0063CB50` answers from flag bit 1) and passes those and the slot-9 result to `006841F0` when that bit is set or to `00683FF0` when it is clear.

Interior anchor `0063D377` (function `0063D330`).

`006065D0` (16 B, no direct call; slot 4 of every `PClassDataMemberArrayDynamic<...>` specialisation - `PArray` of pointers, floats, ints and unsigned values, `PSharray` and `PString`) tail-calls the function pointer stored at the member's `+0x60` with the object argument, and returns nothing when that pointer is NULL.

Interior anchor `006065D9` (function `006065D0`).

`00604580` (36 B, no direct call; slots 6 and 7 of the same specialisations) tail-calls the function pointer at `+0x68` when one is installed; otherwise it returns the qword at the object plus the member's offset (`+0x48`) less the owning class's base offset (`[+0x18]` then `+0xF4`).

Interior anchor `00604596` (function `00604580`).

`0060F3D0` (33 B, no direct call; slot 8 of the same specialisations) forwards to the function pointer at `+0x70` with the object and the next two arguments when one is installed, and otherwise returns `0x15`.

Interior anchor `0060F3EB` (function `0060F3D0`).

## No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)

*No page cited these functions and no census-listed instruction calls or jumps to them: each is reached through data or through code this page documents. Each sentence states what the body does (access and representation, not purpose) and ends with the reference that reaches it; the anchors are instructions inside the body that do it. Handed over by SWE2-EC7 and read whole by FABLE against the certified image; verified by [`apply.py`](../../_index/candidates/fable-noref-member-registration-and-the-recovered-field-schema-data-1003/apply.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic, and every named reference holds or forms the body's address at the bytes.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `008AF490` | 106 B | walks the intrusive list headed at `01F2E340` (link qword `+0x50` of each object, read before the call) and, for each object with bit 0 of byte `+0xFC` set, calls slot 7 (qword `+0x38`) of its vtable with `edx` = 1; its address is formed into `rcx` by `006316C0` + 0x193 for the `00808B90` exit registration at +0x1C4, and 15 other sites form it the same way | Interior anchor `008AF49A`; Interior anchor `008AF4C0`; Interior anchor `008AF4D6`; Interior anchor `008AF4E7` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-member-registration-and-the-recovered-fi-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0063BBC0` | 49 B | calls virtual slot `+8` of the object at qword `rcx+0x30`; when the result is non-null and bit 0 of its byte `+0xfc` is set, returns the address `02CF8580`; otherwise tail-jumps to `00630340` (without reloading `rcx` after the virtual call) | Interior anchor `0063BBC4`; Interior anchor `0063BBCB`; Interior anchor `0063BBD3`; Interior anchor `0063BBDC`; Interior anchor `0063BBEC` |
| `006ABEC0` | 201 B | returns 0 when qword `[rcx]` is null; when the chain from qword `rcx+8` through qword `+0x78` reaches `02E404B0`, the key is qword `[rcx]`; otherwise calls `005A7B50(qword rcx+8, "getLocalToWorldMatrix")` and then the call at `006ABEC0` + 0x50 with (that result, qword `[rcx]`), returning 0 when either gives null, and the key is the second result; it then searches the tree rooted at qword `01F2EB58` with sentinel `01F2EB40`, taking child qword `+0` when node qword `+0x18` is above the key and `+8` when below (unsigned), and returns qword `[node + 0x20]` of the matching node, or 0 when the sentinel is reached | Interior anchor `006ABEE1`; Interior anchor `006ABF00`; Interior anchor `006ABF10`; Interior anchor `006ABF5A`; Interior anchor `006ABF84` |
