# The type store

**Two files, and they are the canonical answer to "what is at offset `+0xNN` of a `T`".**

```
types.tsv    one row per type   type, size, category, instance, allocation_site, ctor, dtor,
                                readiness, confidence, level, evidence, documents, route
fields.tsv   one row per field  type, offset, size, name, ctype, meaning, readiness,
                                confidence, evidence
```

## The `OVERLAY` marker — a declared tagged union, added 2026-09-21 (SWE2-STRUCT)

Fields must not overlap, and `types_index.py --validate` errors when one does — with one declared
exception. When two interpretations share the same bytes under a tag (a union), the **overlapping**
row opens its `meaning` cell with the token `OVERLAY `, naming the arm it overlays and the tag field:

    EncodedIdQueryRecord  +0x06  2  id  uint16  OVERLAY rowIndex +0x04..+0x07 (tag: classId +0x00): ...

The marker goes on the row that starts inside an earlier row; the arm it overlays keeps its own
ordinary row. The token is schema-level, not prose mood: a row that overlaps without it is an
accidental overlap and stays an error. Added 2026-09-21 (SWE2-STRUCT,
OPUS-REQ-SWE2-STRUCT-THE-TYPE-STORE-CANNOT-DECLARE-A-UNION).

## Type-name provenance — three kinds, say which (ruling 2026-09-21, SWE2-FRONTIER)

A `types.tsv` name in P-prefixed CamelCase reads to a consumer as an engine RTTI class name.
Three provenances exist and a row must be able to say which it carries:

- **MSVC class RTTI** — a direct `.?AV<Class>@@` descriptor exists in the image.
- **Phyre reflection** — no direct `.?AV`, but the class is named by its descriptor
  machinery: `.?AV?$PClassDescriptorConcrete@V<Leaf>@<Ns>@Phyre@@` template-argument
  RTTI, and/or a constructed file-side name in `phyre-type-name-hashes.tsv`. This IS
  engine-authored — `PRendering::PTextureCubeMapD3D11` is the worked instance: no
  direct `.?AVPTextureCubeMapD3D11` exists, yet the name is in the image twice over
  (descriptor-template RTTI at `00D51E90`, name-hash `FBB759D0` at `006154FA`).
- **Store-assigned** — the fleet invented the name. It must be marked as such in the
  row's evidence (a bare P-prefixed name with no provenance note is what a reader
  mistakes for RTTI; that is the failure this rule exists to prevent).

When a name's provenance is checked, the row's evidence records which kind it is.

A slot whose width is known and whose meaning varies by a tag gets **no special ctype spelling**
(ruling 2026-09-21, OPUS-REQ-STRUCT-NO-SPELLING-FOR-A-KNOWN-WIDTH-VARIANT-SLOT). When the arms are
distinct layouts, each arm is its own row: the later row carries `OVERLAY`, and each row's ctype
spells that arm's storage — `BattleStatsRecord +0x088` is the worked instance, declaring
`gambitBlockParty` ctype `GambitConfig` overlaid by `gambitBlockSpawned` ctype `u8[52]` under tag
`kindByte +0x05`. When one field's meaning varies without distinct named arms, the meaning cell
carries the fact and the ctype spells the storage width. `UNRESOLVED` was only ever a hold for this
missing mechanism — it is not the spelling for a known-width variant slot.

## Alternate occupants of one storage — declare each kind (ruling 2026-09-22, SWE2-FRONTIER)

Two constructions can reach the SAME storage at different times with different sizes and different
handlers. When they differ on all three kind discriminators — extent argument, `+0x00` handler, and
child topology — they are two types alternating on one span, not a mode of one. The worked instance
is `ManagerSub0209BE80_AB30`: `00276650` builds a 0x61F0 widget with handler `00279E20` (the battle
menu family, children = the `0x3010`x2 array at +0xC0), while `002906D0`->`00296940` builds a 0x720
widget with handler `002985D0` whose own +0xC0 chain is a 0x650 child and a 0x4C0 grandchild. Both
write a handler at +0x00 of the same address, so they can never be alive together — this is
**alternate occupancy over time**, which static evidence cannot order.

Each occupant is declared as its own row; the second takes a size-suffixed name
(`ManagerSub0209BE80_AB30_0720` shape) since the bare storage key is taken, and its evidence names
the sibling occupant and states that which is live when is not statically readable. The children
of each occupant are declared under their own parent, never folded up. A smaller second extent does
NOT make it a sub-object of the larger — both start at the same base.

## The `route` column — machine-readable access route

`instance` stays prose; `route` (appended 2026-09-17 under
`FABLE-REQ-SWE2-STRUCT-THE-INSTANCE-COLUMN-IS-PROSE-AND-A-CENSUS-CANNOT-READ-IT`) is the
machine-consumable form of the same information, for the rows that have one. Alternatives are
separated by ` | `. Empty means prose-only — stack locals, caller arguments, heap blocks with no
static anchor, file layouts, and engine-internal objects all have no fixed route, and that is a
property of the type, not a missing cell.

```
STATIC  0xADDR                              one instance at a fixed address
ARRAY   0xADDR stride=0xS count=N [index=E] element i at ADDR + i*S
PTR     0xADDR [+0xOFF]                     instance at *(ADDR) + OFF
PARRAY  0xADDR [+0xOFF] stride=0xS [count]  element i at *(ADDR) + OFF + i*S
SLOTPTR 0xADDR stride=0xS [count=N]         instance i = *(ADDR + i*S), a pointer table
EMBED   Type +0xOFF [stride=0xS] [count=N]  fixed offset inside a parent type
CHAIN   Type +0xOFF [stride=0xS] [count=N]  instance = *(parent + OFF); with stride, the
                                            parent field points at the array base
RELOFF  Type +0xOFF                         instance = parent + *(int32 *)(parent + OFF) — a
                                            RELATIVE reference, not a pointer
PKREF   0xFN Type +0xOFF                    instance = FN(*(uint32 *)(parent + OFF)) — a pack
                                            offset decoded through a resolver (0020E600 =
                                            `rax = ecx + *(0x01F83530)`); the parent may also
                                            be a bare cell (`0x02EBF118`) when the header type
                                            is band-shared
VTABLE  0xADDR                              vtable-only object — each entry of the table at ADDR
                                            is walked with rcx = this; used when no caller ever
                                            holds a nameable `this`
FN      0xADDR +0xOFF [bank=0xD]            base = the getter at ADDR's return + OFF; with
                                            `bank=`, the getter is BANK-GENERIC (its return
                                            type is decided by the bank handed in arg1, not
                                            by the function - 002ED570 reads stride/mask out
                                            of the bank itself), and the seed is gated per
                                            call site: only sites whose rcx was loaded from
                                            a +0xD field qualify, with provenance followed
                                            through register copies and callee argument edges
                                            (classify_slot_resolver_sites.site_slot_map).
                                            A site fed by two different slots - or by anything
                                            unproven - seeds NO type: exclusion is the
                                            documented direction of error
DYNAMIC <free text>                         base is runtime-computed; documented for humans,
                                            not consumable by a fixed-base generator
```

### The empty-route rule, audited 2026-09-20 (OPUS)

**348 of 465 types have an empty route, and every one of them is legitimate.** That figure looks
alarming and is not — it was nearly filed as a 348-row defect before this audit was run, which is
the reason the result is recorded here rather than left as a passing check.

The rule above says an empty route means *prose-only* and lists the cases: stack locals, caller
arguments, heap blocks with no static anchor, file layouts, engine-internal objects. **What the
rule does not cover is a type whose own prose NAMES an address** — there a route would be
recoverable and the empty cell really would be an omission. That is the only question this audit
asked.

| filter | types |
|---|---:|
| empty route | **348** |
| …whose `instance`/`allocation_site` prose names a data address *and* uses static language | 154 |
| …excluding *"the class descriptor is the static at X; the instance itself is created by the engine"* | **1** |
| …and that one reads *"no fixed address and no route … nothing stores it at a stable address"* | **0** |

**The 154 are one uniform false positive.** They are the Phyre reflection-derived types, and their
prose is precise about why it names an address: the static is the **class descriptor**, and the
instance is created by the engine. An address in the prose is not an instance address. The last
survivor, `PaneListWidget0B68`, states its own reason — one per factory call, never stored
anywhere stable.

**So nothing in the store is unlocatable-by-omission**, and the storage-class census agrees from
the other side: of the 348, **153 are `IMAGE/ENGINE`** and 179 declare no class at all, with only
a handful of `CALLER`, `HEAP`, `RESOURCE` and `INTERIOR` rows among them.

**Why this is worth a paragraph.** "75 % of types have no route" is the kind of statistic that
reads as a gap, gets quoted as one, and produces work against a rule that is already right. It is
a **denominator**, not a debt — the same shape as the `32 ids` figure that turned out to be a
count over a 247-handler subset. The number to watch is not how many routes are empty; it is
whether any empty one has a locatable instance, and today that number is **zero**.

`count=` and `index=` may name a symbolic quantity (`slotCountA8`, `recordCount`) when the bound
is a field rather than a constant. `STATIC`/`ARRAY` rows are `gen_static_census.py` targets;
`PTR`/`PARRAY`/`SLOTPTR`/`FN` rows are consumed by `gen_route_seeded_census.py` / the
`field-access-index` sweep — `PARRAY` seeds `*(ADDR)` and strides by `stride`, `SLOTPTR` seeds
`*(ADDR + i*stride)`, `FN` seeds the getter's callers' return registers; `EMBED`/`CHAIN`/`RELOFF`
compose transitively down to a seedable root (a `DYNAMIC` cell whose only caveat is laziness —
the reader-visible path is still `*(ADDR)` — may carry `| PTR 0xADDR` / `| FN 0xGETTER+0x0`
alternatives so the machinery can seed it, as `MapRefImageHeader` and the two command-list
singletons do).

Query and validate with `Database/Tools/analysis-kit/gfz-scripts/types_index.py`:

```bash
python types_index.py --store <db>/_types --validate      # overlaps, overruns, gaps
python types_index.py --store <db>/_types --type PClusterHeaderBase
python types_index.py --store <db>/_types --coverage
```

`types_index.py` checks a type's **field layout**. The columns that say who allocates a type, who
owns it and how it is reached are checked by a second instrument, which also parses this grammar:

```bash
python check_storage_class.py                # routes, anchors, containment, ownership columns
python check_storage_class.py --self-test    # four controls; a silent control refuses the run
```

## `field-access-index.tsv` — the per-type accessor index (added 2026-09-22, SWE2-FRONTIER, F-6)

*"Every writer of this field"* is charter §7's first example query, and `global_refs` cannot answer
it: that table is address-keyed, while `obj->field` is `[reg+disp]` with the object identified only
by dataflow. `field_access_index.py` runs `gen_route_seeded_census.py`'s offset-tracked census over
**every** type whose `route` column parses and writes the union of all per-type `*-accesses.tsv`
artifacts into one store-side index:

```
type    disp    base    kind    function    site    instruction    note
```

- `kind` is `r` / `w` / `rw` / `addr`. **Writers are `w` AND `rw`** — the F-6 query is
  `kind == "w" || kind == "rw"`: 1,734 rows at the 2026-09-24 regeneration are read-modify-write
  (atomic/`lock`-prefixed/`and`/`or`/`xadd`-style stores), and `kind == "w"` alone silently omits
  every one of them. `addr` marks an address taken, not a write.
- `base` is the in-hand object offset at the access: a touch at `disp` reached through
  `[base_reg + x]` with `base != 0` is a **nested** access (a field of a sub-object), not a field of
  this type at `disp`. The flat read dropped this once already and a census had to be withdrawn.
- `note = zeroclear` marks a store of a provably-zero register: the bytes are cleared; nothing
  about field boundaries follows.
- Derived routes (`EMBED`/`CHAIN`/`RELOFF`/`PKREF`, and `SLOTPTR Type +OFF` — a parent-relative
  pointer table, `PTABLE` internally) resolve transitively to a seedable root, walk the
  root once, and emit only the child's own window — `disp`/`base` are child-relative with the
  embed offset already removed, and `base` distinguishes embedded members (offset arithmetic
  from the parent) from pointer members (the parent-relative deref depth). A child whose parent
  chain ends at `DYNAMIC` or an unrouted type resolves to nothing.

**Coverage is stated, not implied.** A type absent from the index means the instrument did not run
on it — never that its fields are unwritten. Latest full run (2026-09-24, committed types/fields
inputs under the direction-repaired classifier — mnemonic tables decide `r`/`w`/`rw` before
capstone's operand flags, which mislabeled 238 rows in the 20,011-row publication): 226 of 596
types swept, 20,150 rows over 150 types with any touch (r 11,549 / w 5,992 / rw 1,734 / addr 875).
Unseeded by route kind: NONE 353, DYNAMIC 2, EMBED-unresolved 4, CHAIN-unresolved 3,
RELOFF-unresolved 2 —
the remaining derived routes fail on parents that are genuinely unrouted or idiom-membership
`DYNAMIC`, not on the derived semantics. The `*(*(slot+8)+8+i*8)` double-deref family resolved:
`ActorStorageRecord` carries `SLOTPTR ActorRecordPool +0x08 stride=0x8` (a derived pointer-table
level — `PTABLE` internally — matching indexed qword loads off a tracked table base, which
propagates through `lea`/copies/indexed-`lea`/`add` and is dropped when a register is rewritten)
alongside `FN 0x00358940+0x0` and `FN 0x003588B0+0x0` (the two record getters — 75 and 180 call
sites — whose return is the observable record path; the walk has no callee→caller return channel,
so `FN` seeds are how getter-mediated objects join the census). It yields 74 declared offsets over
999 accesses with `MovementContext` (61) and `SecondaryContext` (42) resolving transitively through
the record's context pointers; `ActorResourceEntry` (11) and `ActorWaitSlot` (5) likewise.
`SLOTPTR` seeding also gained the biased-table form — bodies that `lea` an enclosing array base and
load `[rB + i*stride + OFF]` — which took `BattleUnit`'s host count 13→21 with identical coverage.

The 2026-09-24 sweep then added the table-behind-a-cell grammar in both shapes. `PTABLE 0xADDR
stride=0xS` seeds a mark on `mov rB,[rip->ADDR]` and yields an element base on any qword load
`[rB + i*S + k]` (the mark can ride either operand, copies through `mov`/`lea`/`add`, and dies on
rewrite or volatile clobber): `Category` resolves 13 offsets / 48 accesses through `PTABLE
0x02EAD008 | FN 0x007AAA20+0x0`, and `AudioParameterRamp` resolves 9 through `CHAIN Category
+0x38/+0x40` transitively. The derived `SLOTPTR Type +0xOFF` form splits on the field's declared
ctype: `X*` reads as an inline table (`[b + i*S + OFF]` loads an element directly — the actor
pool's `recordPtr` shape), while `X**` is a pointer TO a heap table (`pBegin void**` — `mov
t,[b+OFF]` loads the table pointer and elements come only through loads off that proven register).
Provenance tracking (`tptr`/`elems`) crosses block boundaries — the pBegin load and the element
fetch sit in different blocks of every iteration loop — and an element base only emits child rows
when it reached its mark through a slot fetch, which is what keeps a table at mark 0 from
attributing the vector's own fields (`pEnd`, `pCapacityEnd`) to the element type. `OrderedObject`
resolves through `SLOTPTR EastlPointerVector +0x00` (composed transitively over the vector's two
`EMBED` list routes) — 2 offsets, thin because element use is dominated by `call [rax]` virtual
dispatch — and `LegacyPs2GsSourceTextureRecord`/`DerivedSlotRecord`/`ReferenceDescriptor` resolve
through `CHAIN LegacyPs2GsTextureContext +0x150 +0x8 / +0x218 / +0x178` (the two-offset form for the
container-behind-a-pointer shape). Element-relative field loads `[array + i*S + f]` under a derived
run now fold by base mark rather than materialising the element register. `RELOFF` remains
exercised end to end — `MapRefFieldRow`, `MapRefWeatherBlock`, `MapRefWeatherLane` through `PTR
0x02099D88`.

The same-day `PKREF` level then closed the pack-reference family: a dword at `parent+OFF` decoded
through a named resolver (`PKREF 0x0020E600 NavRunStateBlock +0x0C` — the walk marks the dword load
as a rel-offset, and a `call` to the resolver with `rcx` carrying it marks `rax` as the child base).
All five nav-pack arrays resolve — `NavMeshVertex`/`NavMeshTriangle`/`NavPortalRecord`/
`NavRegionRecord`/`NavBroadPhaseHeader`, every emitted offset landing on a declared row — and the
bare-cell form (`PKREF 0x0020E600 0x02EBF118 +0x0C`) resolves `StatusDefinitionRecord`, whose parent
is one registry slot of the band-shared `AuthoredTableHeader` shape. Two supporting changes ride
with it: the two-operand `imul d, s` product is tracked under derived runs (the stride×index fold in
`add ecx, edx`), and `zero` now crosses block boundaries by intersection so a marked register
survives a merge whose other predecessors prove it NULL — the `x ? marked : 0` coalesce that guarded
lookups generate everywhere (sound because the null side's access would be a null-deref, i.e. dead).
That merge fix alone recovered ~2,400 rows across 90 already-swept types and lost none; on the
`ManagerSingleton0209BE80` control the only diff is five stores newly tagged `zeroclear`, which is
the flag now seeing registers zeroed in predecessor blocks.

The `VTABLE` level then closed the vtable-only class: for an object no caller ever names — the
three `DynGeoFontTextSpecial*` variants, whose route text was already `DYNAMIC reached only
through vtable 00906DE8/…EB8/…E50` — the table is read out of the image (consecutive qwords that
are known function entries, to the first non-function qword) and each method body is walked with
`rcx` marked at 0, which is what `call [rax + slot]` dispatch guarantees at entry. Each resolves
27 offsets and every base lands on a declared row; methods shared between the variants contribute
the same accesses to each, which is correct — the vtables genuinely dispatch those bodies, and
the shared-layout overlap is the classes' actual commonality. The remaining two `DYNAMIC` rows
are `LicenseNodeRecord` (an authored file — `license_data.bin` rows have no image address at
all) and `AuthoredTableHeader` (a band-membership idiom: 40 slots across `02EBEF70..02EBF3FC`
share the shape, and membership is by index range, not a nameable cell) — the grammar's honest
tail, not a missing feature.
Absolute statics accessed by direct rip-relative operands (an 8-byte `BootAllocationSlot*` is the
example) produce no rows either: they never establish a base register, and they are `global_refs`'
job — address-keyed is exactly right for them.

The census walk follows the control-flow graph (it is the fixpoint instrument, not the linear
`gen_array_census` walk), propagates the tracked pointer into callees only through argument
registers and named stack slots, and descends to depth 6 — a spilled receiver or a fifth stack
argument ends the trail. A zero for a swept type means *not reached by a tracked displacement from
these routes*, which excludes neither wholesale copies nor routes the tool declines to model.

Two route-grammar extensions shipped with the index: `PTR 0xADDR+0xOFF` now parses (the grammar
always declared `*(ADDR) + OFF`; the loaded pointer carries `-OFF`, the same convention as `FN`'s
return), and `STATIC`/`PTR` tolerate a trailing ` -> note` annotation the way `ARRAY` always did.
`PApplication`'s route was corrected from `STATIC 0x02EA5368` to `PTR 0x02EA5368` — the slot is a
handle, as its own instance column had already adjudicated; `AchievementState` and
`ImageBackedStateBlock` gained the `FN 0x002536A0+…` alternatives their prose already names, because
consumers call the eight-byte getter rather than load the cell — a `PTR` seed walks only the
loader's own body.

```bash
python field_access_index.py        # rebuild the index (one shared host index, ~4 min)
python knowledge_db.py build        # then ingest it as the `field_access` table
python knowledge_db.py query writers-of-field ManagerSingleton0209BE80+80
```

## The `allocation_site` column — one storage class, then the evidence

The column was originally written as if every type has a heap allocation site. **Most of these types
cannot have one**, and `UNRESOLVED` on such a row records a question that cannot be asked rather than
one nobody has answered. Every game-side row now opens with exactly one class:

| class | means | the allocation question |
|---|---|---|
| `IMAGE` | a static object in `.data`/`.rdata`/`.bss` at a named address | none exists |
| `INTERIOR` | a sub-object of a named parent, allocated and released with it | the parent's |
| `CALLER` | a buffer the caller supplies, living in the caller's frame | none exists |
| `HEAP` | a real allocation call, with the instruction that makes it | answered |
| `POOL` | a slot taken from a pre-existing block of fixed-size slots | **the block's**, named alongside |
| `RESOURCE` | a buffer the resource system owns | **open**, and the row says so |
| `MIXED` | more than one of the above, by instance, requested size or stage | per instance |
| `UNRESOLVED` | genuinely unknown | open, and the row must name the question |

> **`POOL` exists because of `BattleUnit`.** Its allocation site named `00234480`, which is a linear
> scan for the first slot whose bit 0 is clear — an *acquire*. The block is allocated somewhere else
> entirely, at `00236924`, through the tagged allocator with the tag `BtlWork`. An acquire recorded as
> an allocation hides the real owner, and the check that finds it is: a row whose `dtor` says the type
> has no storage of its own cannot also have an allocation site.

> **`RESOURCE` and `UNRESOLVED` are counted separately** — *nobody allocates this* and *we have not
> found who allocates this* are different answers, and only the second is a question.

## Access, representation and meaning are three axes (2026-09-25, OPUS, on the user's repair instruction)

A field row carries three different kinds of knowledge. They live in different columns, they are
measured by different instruments, and **none of them implies another.**

| axis | what it says | where it lives | how it is established |
|---|---|---|---|
| **physical access** | which instructions read or write these bytes, at what width | `route`, `field-access-index.tsv`, the evidence cell | censuses, access hooks, executed replays |
| **representation** | offset, width, ctype, extent, layout, stored values | `offset`, `size`, `ctype`, `readiness`, `confidence` | reads of the producer, width tests, tiling, sampled bytes |
| **semantic purpose** | what the field is *for* | `meaning` | a named source (engine strings, registered names), a traced consumer whose effect is understood, or a ruling |

**The rules.**

1. **Readiness never implies meaning.** On a field row, `TYPE RESOLVED` or `SIGNATURE RESOLVED` reports the
   representation of the row or of its type. A row whose `meaning` cell is empty, withdrawn, open or says
   `MEANING NOT CLAIMED` has **no stated purpose**, whatever its readiness, confidence or access proof says.
   `PROVEN` access, `TYPE RESOLVED` and a clean tiled layout **cannot overrule `MEANING NOT CLAIMED`**.
2. **`SEMANTICALLY IDENTIFIED` requires a stated purpose.**
   - A row at that rung whose meaning cell states only a value, a width or an access count is a
     contradiction. The fix is to lower the rung and keep every fact in the cell.
   - Renaming the field is not the fix.
3. **Names are representation labels unless their source is semantic.** `unobservedSpan1538` or `f32One0004`
   label bytes; they do not claim a purpose. **Never rename a field to move a percentage.**
   `TYPE-COVERAGE.md` counts *named* and *meaning stated* separately so a rename cannot.
4. **A sampled value is representation, and a sampled zero proves nothing about writes.**
   - A byte observed as zero cannot distinguish untouched storage from an explicit zero store. Read or run
     the producer.
   - `PDeferredLightingSlot0080`'s eight zero spans are the worked correction; see
     `_index/candidates/s49-opus-replay-lighting-slot-zeros/`.
5. **A known variable-size rule is a known extent.** A type or field whose size is a stated rule, such as a
   construction argument or a count times a stride, is not `UNRESOLVED`.
6. **Keep useful facts and explicit unknowns.** A correction lowers exactly what is contradicted. It keeps
   the measured bytes, the widths and the scope of every observation. It does not downgrade whole types or
   populations indiscriminately.

**The instrument, and its limit.**
- `types_index.py --coverage` reports *meaning stated* from the meaning cell by a lexical rule
  (`meaning_stated()`).
- It detects contradictions such as a `TYPE RESOLVED` row with no stated purpose.
- It does **not** verify that a stated meaning is true. That remains an independent review of the original
  evidence.

## What the readiness column means here, and why it changes the checks

A type recovered from a **sample** of its members — reflection registrations, a handful of accessors
— has gaps by construction. A type whose layout was actually read has gaps that are **findings**.
The validator uses the declared readiness to tell them apart: at `SIGNATURE RESOLVED` and below,
undeclared gaps are expected and not warned about; at `TYPE RESOLVED` and above they are reported.

**A declared numeric size overrides that.** Readiness alone conflated *"we only sampled this type"*
with *"we know its exact extent and half of it is unread"*. `AudioParameterRamp` is
`SIGNATURE RESOLVED` because 24 of its 48 bytes have no reader — but its `0x30` stride is **proven**,
so those gaps are findings and must stay visible. **A type that declares a numeric size has a known
extent; its gaps are reported whatever its readiness says.**

> **Reporting a gap in every sample-derived type would bury the real gaps.** The two hand-read types
> in this store between them own **8 undeclared spans**, including a 1,476-byte tail on
> `ActorStorageRecord`; those are the ones worth closing, and they stay visible because 179 imported
> types produce none.

`size` may be the literal `UNRESOLVED`. That is a legal value: the checks that need a declared size
are skipped rather than a size being invented.

## Sized shells for proven authored extents (2026-09-21, SWE2-STRUCT)

An authored table whose extent is **closed arithmetically** — file size equals header plus count
times stride, or the registry descriptor's measured count times stride — gets a type row even when
no field of its record has been read: one honest `unobservedSpan` for the interior, `DISCOVERED`
readiness, `PROVEN` confidence on the extent, and a `DYNAMIC` route through the registry slot or
file-plus-index (authored data has no image address, so `STATIC` is never right). The store's own
ruling applies: an undeclared type cannot be allocated, indexed, or routed to, so a proven extent
with a declared gap beats absence. Where the arithmetic does **not** close for a given table, the
row takes `UNRESOLVED` size with a lower bound instead — a number that is not proven is worse than
none. `LicenseNodeRecord` is the sized-shell example, `EquipmentDefinitionRecord` the lower-bound
one. A contested count is inherited in the evidence, not smoothed. Ruled on
`OPUS-REQ-STRUCT-SHOULD-30-AUTHORED-TABLES-GET-SIZED-SHELLS`.

## What is in it, as of 2026-09-20

| | types | fields |
|---|---:|---:|
| game-side, read from the binary | **265** | 3,028 |
| imported from Phyre reflection registrations | **182** | 895 |
| **total** | **447** | **3,923** |

> **Re-derived 2026-09-20 (OPUS)**, replacing 97 / 2,347 · 179 / 613 · 276 / 2,960 dated
> 2026-09-19. **That row was correct when it was written and stale within the day** — the store
> held 276 types at the commit that wrote it (`4771de01c`, 03:19) and 440 by the last commit of the
> same date. It is the third time this table has rotted, and the note below has predicted it each
> time.
>
> **One of the two derivations has stopped working, and that is the part worth recording.** The
> 2026-09-19 row rested on two tests agreeing: membership in
> [`phyre-field-schema.tsv`](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/phyre-field-schema.tsv),
> and the `allocation_site` / `ctor` / `dtor` columns being empty. **The second test now finds 6
> rows where it used to find 179**, because 176 imported rows have since been given lifetime prose
> — **173 of them a `dtor` cell and nothing else**, which is the EXP-124 descriptor destroy-slot
> consumption landing exactly where it should. The imported types are no longer *the types with no
> lifetime prose*, so the agreement of 2026-09-19 cannot be re-run and is not claimed here.
> **Only the schema-membership derivation is live**, keyed on `class_leaf`; it returns 182, three
> above the 179 that `types_import_phyre.py` wrote, and whether those three are leaf-name
> collisions or later hand-added rows is **not established**.
>
> Recompute both populations, rather than quoting this table:
>
> ```bash
> python types_index.py --store <db>/_types --coverage      # the total, always current
> ```

> **The row above used to read 4 / 109 game-side and was dated 2026-09-08.** It was not wrong when
> it was written and it was badly wrong by the time anyone read it, which is the failure mode a
> dated snapshot invites. Recount it with `types_index.py --coverage` rather than quoting it.

The 179 are engine types, from
[`phyre-field-schema.tsv`](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/phyre-field-schema.tsv)
via `types_import_phyre.py`. **They are `SIGNATURE RESOLVED`, not `TYPE RESOLVED`** — member names
and offsets are known, the layout is not complete, and each row carries its own measured
completeness in its evidence column.

### Sizes are never derived from offset deltas, and the reason is measured

The obvious derivation is `size[i] = offset[i+1] − offset[i]`. **It is unsound for this source**, and
`types_import_phyre.py` prints the test that shows it on every run. Take only members whose C type is
a genuine primitive — so the true size is known independently — and compare it against the delta to
the next recovered member:

```
tested                        : 245 primitive members that have a next recovered member
delta == the primitive's size : 202  (82.4 %)
delta >  the primitive's size :  43  (17.6 %)   <- an unrecovered member sits in the gap
```

> **A sixth of the time the next recovered member is not the next member.** The reflection table is a
> sample, so a delta measures *distance to the next member anybody recovered*, which is not a size.
> Modal-voting the deltas would have produced confident wrong sizes for exactly the engine types that
> have no other evidence — `sce::Vectormath::…::VVector3` shows deltas of 16, 32 and 36; `VPString`
> shows 8, 24 and 88.
>
> **So size comes from the C primitive table or it stays `UNRESOLVED`.** 344 of 613 imported members
> (56.1 %) have a size on that basis. The other 269 are engine-typed and carry `UNRESOLVED`.

Byte coverage, stated with its denominator: **1,201 of 30,578 bytes (3.9 %)** across the 179 imported
types are covered by a member of known size. That number is a **floor** — it counts only members
whose size is known, so every engine-typed member counts as zero — and it is the honest reason these
types are not `TYPE RESOLVED`. **25 of the 179** have recovered members that fill their own span.

### Two rows are not structs, and say so

The grouping key is the **leaf** class name, which is what a reader wants to see. A template
container has one leaf name and many instantiations, so grouping merges genuinely distinct types:

| leaf name | full class names behind it |
|---|---:|
| `PArray` | **60** |
| `PSharray` | **9** |

> Their members happen to sit at the same offsets in every instantiation, so the merge produced no
> overlap and **the validator saw nothing wrong**. A silent merge that passes validation is exactly
> the kind that survives. Both rows are imported at **`CLASSIFIED`**, not `SIGNATURE RESOLVED`, and
> their evidence column opens with `MERGED LEAF NAME: N distinct full class names share it ... this
> row is NOT one struct.` **177 of the 179 are unambiguous.**

## What is missing

- **Game types.** Every *imported* type is `Phyre::*` engine machinery. The charter's L2 gap is
  *game*-type recovery — actors, party members, battle state — and the store holds **four** of those,
  all hand-read: `GameSettingConfig`, `ActorStorageRecord`, `AudioParameterRamp`, `Widget`.
  **2026-09-08:** the last two were added by acting on
  [the reconstruction roadmap](../_index/RECONSTRUCTION-ROADMAP.md), which had named `16-UI` and
  `18-Audio` as the two categories holding a contract with no type behind it.
  **2026-09-08:** a static attempt on `ActorStorageRecord`'s 1,476-byte tail added **3** fields and
  **narrowed 3 more that were too coarse**, leaving the tail exactly as undeclared as before. The
  measurement is in [the record behind every actor](../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md);
  the conclusion is that this tail needs runtime observation, `DN-1`.
- **A ROW IS NOT A DESCRIPTION, and 215 rows prove it.** Measured 2026-09-13: **832 of the store's
  1,906 field rows have an empty `meaning` column** - an offset, a size, a type, and nothing saying
  what the field is. Read as a single number that badly overstates the gap, so it splits:

  | population | empty | rows | |
  |---|---:|---:|---|
  | Phyre / engine-imported | 613 | 645 | **expected** - reflection gives names and offsets, never prose |
  | **GAME types** | **219** | 1,261 | the real gap |
  | of those, in a CENSUSED type | **215** | 1,003 | **the evidence exists and is unrecorded** |

  Those last 215 are the actionable ones. `CharacterRenderRecord +0x3D1` was one of them until
  2026-09-13: declared `uint8` with an empty meaning, while its census showed `or 0x40` setting bit 6,
  `and 0xBF` clearing it at reset, `test 0x40` reading it and `test 7` testing the low three bits as a
  group. Nothing new had to be discovered to describe it - the accesses had been sitting in the census
  the whole time and no one had written them down.

  **And only a third of those 215 can yield more than a width.** Re-measured 2026-09-13 with the
  shared instruction classifier: of the 188 undescribed rows that still have census accesses, **60
  have INFORMATIVE evidence** - arithmetic, a float operation or a float constant, the classes that
  say what a value IS. The other 128 are touched only by moves and address computations, which give
  a width and nothing else. So the queue is 60 rows that can be described and 128 that can be
  measured, and calling all 188 "describable" would repeat in miniature the error this whole entry
  is about.

  **THESE FOUR FIGURES NOW HAVE AN INSTRUMENT: `gen_description_queue.py`.** They were measured by
  an ad-hoc script that was not kept, which is the same defect retracted in EVIDENCE-STANDARD
  2026-09-13k - a published number nobody can re-derive. Re-measured with the population stated in
  the file, on 2026-09-13 after the day's descriptions landed: **796 empty meanings, 613 of them
  Phyre-imported and expected, 183 in game types, 179 of those in a censused type, 50 INFORMATIVE
  and 128 MEASURABLE ONLY.**

  **This is staleness, not the earlier defect, and the difference matters.** Two of the four
  published figures - 613 and 128 - reproduce exactly; the others moved because rows got described
  between the measurement and now. The mask table retracted the same day reproduced under *no*
  population at all, which is a different kind of wrong. A live queue shrinking is the instrument
  working. What was wrong was only that the figure could not be re-run, and now it can.

  **RE-RUN AGAIN, LATER ON 2026-09-13 — AND TWO OF THE FIVE BUCKETS ARE NOW EMPTY.** Every figure
  below is `gen_description_queue.py` output, not prose:

  | bucket | rows | what it means |
  |---|---:|---|
  | Phyre / engine-imported | **613** | expected, and unchanged through every re-run |
  | INFORMATIVE — describable from the census today | **0** | **closed** |
  | needing research before anything else | **0** | **closed this pass** |
  | MEASURABLE ONLY — moves and address computations | **123** | a width, not a meaning; each annotated with its own access count |
  | in a censused type with NO access at that displacement | **1** | `BattleResultRecord +0x144`, which exists *by the record's 0x148 extent* and says so |

  **So 737 empty `meaning` cells now sit in five named buckets and none of them is "unexamined".**
  613 are a reflection artefact, 123 are honestly measurable-and-no-more, 1 is a declared tail slot
  nothing touches, and the two buckets that represented actual undone work are at zero.

  > **THIS IS NOT "THE TYPES ARE DONE".** 123 rows still have only a width, and a width is not a
  > meaning — that was the whole point of this entry. What closed is narrower and worth stating
  > exactly: **every row whose evidence could already say what the field IS has been described, and
  > every row that needed research before it could even be queued has had it.** The last of those
  > was `NavigationPathState +0x90`, which turned out to be an indexed per-node table of packed
  > `(x, z)` floats — and closing it raised a contradiction rather than settling one, because the
  > type is declared 0x98 bytes and an array indexed by a node index does not fit in it (`OPUS-PUB183`).

  **So "1,906 field rows" is not "1,906 understood fields".** The count is honest about what the store
  holds and silent about what the store says, and those are different questions. The gap is 215 in the
  types that can answer it today, not 832.
- **Sizes for engine types**, which would raise the byte coverage above its 3.9 % floor.
- **The rest of each class.** 25 of 179 classes have members filling their span; the other 154 are
  known to be incomplete and say so.

## Where two censuses claim the same instruction: eight agreeing equations, one of them wrong

`002FF0D3  or dword ptr [rsi + 0x14], ecx` is recorded by three censuses at three displacements —
`BattleStatsRecord +0x38`, `BattleSystemState +0x40`, `SavePayload +0x4E4CC`. `rsi` holds one
address, so either the types nest and all three are views of the same bytes, or at least two
attributions are wrong. `check_census_overlap.py` decides it the only way an access census can:

> If two types nest at a fixed position, the difference between the two recorded displacements is
> the SAME at every shared site, and that difference IS the nesting offset. If it varies, the
> censuses disagree about what the base register holds.

**EIGHT CENSUSES AGREE, ACROSS 11,082 SITES, WITH ZERO DISAGREEMENTS.** Every pair that shares an
instruction shares one offset. Two edges are excluded before the count, because an edge can agree
without being evidence: `ImageBackedStateBlock`/`SavePayload` is **the same census file read at a
shift**, so its offset is the shift returned rather than a measurement, and `BattleUnit`/
`MovementContext` rests on **two** shared sites, where one delta is arithmetic and not agreement.

The eight surviving equations over five bases are mutually consistent — which, being overdetermined,
they did not have to be — and they place, relative to `BattleStatsRecord`:

| offset | type | shared sites carrying it |
|---:|---|---:|
| +0x0 | `BattleStatsRecord` | — |
| +0x0 | `BattleUnit` | **inferred, never measured: these two censuses share NOT ONE instruction** |
| +0x8 | `BattleSystemState` | 313 |
| +0x80 | `SpawnRecord` | 21 |
| +0x4E494 | `SavePayload` | 240 |

**One result is a genuine independent corroboration.** `SavePayload = BattleSystemState + 0x4E48C`
falls out of 990 shared instructions, and the store's two instance expressions — derived separately,
from allocation sites, not from each other — give `0x021B290C - 0x02164480 = 0x4E48C`. Two roads to
one number.

### The finding: one of the eight equations is wrong, and consistency could not see it

`BattleUnit = BattleSystemState - 0x8` rests on 42 sites in 8 functions, and it is **census
contamination, not nesting**. Four discriminators, none of them live:

1. **The route column disagrees with itself.** At every one of the 42, `battle-unit-accesses.tsv`
   records the route as `arg0+0x0` and `battle-state-block-accesses.tsv` records the same argument as
   `arg0+0x8`.
2. **The functions are named for the type they take** — `BattleUnit_DispatchActorPresentationEvent`,
   `BattleUnit_ComputePresentationSuppressionMask`, `BattleUnit_SubmitResultReactionMode`.
3. **The contested instruction names the relationship itself.** `0030ABB8 mov rdx, qword ptr [rdi +
   0x698]` is filed by one census at `BattleUnit +0x698`, which the store independently records as the
   stats-record binding, and by the other at `BattleSystemState +0x6A0`, which is nothing.
4. **The allocation shapes forbid it.** `BattleSystemState` is a singleton at a fixed address
   (`*(void**)0x02EBF190 = 0x021B290C`); `BattleUnit` is `*(char**)0x0208E688 + slot * 0xF50`. **No
   constant offset can relate a singleton to a pooled record across eight functions.** One slot could
   sit 8 bytes from the block by coincidence. Forty-two accesses cannot.

> **WHY MUTUAL CONSISTENCY DID NOT CATCH IT, WHICH IS THE PART WORTH KEEPING.** The bad edge is
> consistent with the good ones *because it borrowed a real offset*. `BattleSystemState +0x008` is
> `statsRecords`, the forty per-combatant `BattleStatsRecord` slots — a genuine +0x8 relationship,
> already declared. The contaminating route admitted `arg0+0x8` and thereby reproduced the true
> nesting offset exactly. **An overdetermined system agreeing with itself is evidence, and it is not
> proof: a wrong equation that reuses a right constant passes every consistency check there is.**

**BLAST RADIUS, MEASURED: small and bounded.** 42 of the state-block census's 1,142 sites (3.7 %),
across 11 displacements, of which **exactly one carries a declared field** — `+0x008 statsRecords`,
and only 5 of its 50 accesses. **No declared `BattleSystemState` field rests on a contested access.**
The other ten displacements — 0xC, 0x18, 0x34, 0x64, 0xD8, 0xE8, 0x164, 0x168, 0x6A0, 0x6A8 — have no
row, so nothing has been built on them. Correcting the census is routed to the area's owner; the
contamination is recorded here because a reader of the field store is the one who would be misled.

## A scalar at an offset its own width does not divide is not a field (2026-09-19, OPUS)

*112 `check_*` scripts, and not one of them tested alignment. It is among the few hard, checkable
facts about a struct MSVC compiled for x64, and it turns out to detect a specific way this store
goes wrong: **a bulk clear read as a field list**.*

**The invariant.** A scalar of width `w` sits at an offset that `w` divides, and a struct's size is
a multiple of its strictest member's alignment so that an array of it keeps every element aligned.
`check_alignment.py` tests both. It takes the width from **`size`**, never from `ctype`, because
this store has a documented convention in which `ctype` can be the width of the *writing
instruction* — testing `ctype` would flag every one of those and the report would be noise.

**Why this is not a cosmetic complaint.** `uint64` at an offset that is `4 mod 8` **cannot be
declared**. Write it in C++ and MSVC aligns it to 8, inserts four bytes of padding, and every
following field moves. A row in that shape is not a description a reimplementation can use; it is a
description that silently produces a different object.

### The first run found 39; 14 of those were the checker's own bug

`elem_align` took the scalar shortcut *before* testing the array form, so every `u8[8]` — size 8,
element alignment **1** — was judged as a qword needing 8-byte alignment. Ten findings, produced by
the one function whose whole purpose was to avoid that class of mistake. The array test now runs
first, and the comment in the source says why.

Of the 28 that survived, **17 sat at `offset % 8 == 4`**. A flat spread across `1..7` would mean
error; a spike that sharp means a convention, and reading the rows found four distinct things:

| what the row actually is | alignment says | action |
|---|---|---|
| **a bulk clear** — a region zeroed with the widest stores available | nothing; these are not fields | **retyped to byte spans** |
| **a declared gap span** — `unobservedSpan*`, "no censused access" | nothing; the width is a span length | **retyped to `u8[n]`** |
| **a pair of floats moved by one qword instruction** | nothing; `uint64` was the instruction | **retyped to `float[2]`** |
| **a taken address** — `subAddr*`, "extent not established" | nothing; size 8 is a placeholder | left; the extent is the open question |

### The bulk clear, proven twice in two unrelated systems

`RenderModelInstance`'s constructor `005049E0`:

    mov qword ptr [rcx + 4],    rbx
    mov qword ptr [rcx + 0xc],  rax
    mov qword ptr [rcx + 0x14], rax
    mov qword ptr [rcx + 0x1c], rax
    mov qword ptr [rcx + 0x24], rax

**Forty bytes in five stores, starting at `+4` because that is where the region begins** — not five
qword fields. The store had them as `qwordSlot04`, `qwordSlot0C`, `qwordSlot14`, `qwordSlot1C`,
`qwordSlot24`, every one evidenced by the words *"qword cleared by init"* and nothing else.

`BootSingleton01F7F598` at `00185038`, in a different system:

    mov byte  ptr [rdi + 0xdb8], al
    mov word  ptr [rdi + 0xdb9], si
    mov qword ptr [rdi + 0xdbc], rsi

**Twelve bytes in three stores of decreasing convenience.** A byte field, a word field and a qword
field is what that looks like if you read the displacements; it is a cleared region if you read the
instructions.

**This is the failure the charter names** — *never consume an unexplained gap merely to make a
layout look complete*. Forty bytes of unknown space became five named fields, and the names made
them look settled. **14 rows retyped; only the `ctype` column changed**, so every offset, size, name
and meaning is exactly as it was, and the misaligned count fell from 28 to 14.

### What is left, and it is not all defect

Fourteen rows remain misaligned and **three types have a size that is not a multiple of their
strictest member alignment** — `ActorDefinitionPayload` (`0x4C`, strictest 8), `EvaluationContext`
(`0x2A`, strictest 8), `FieldRecord` (`0x3`, strictest 2). Each is one of: a record that is packed
on purpose and owes alignment nothing, a size that is a measured extent rather than a compiled
`sizeof`, or a member whose width is the access instruction's. **The check cannot tell those apart
and does not try** — it prints, for each finding, how many of its type's rows are misaligned and
what the type's category is, because a type with many is a packed record and a type with one is a
question.

**NOT CLAIMED:** that the retyped rows are now *understood*. A byte span is an honest statement that
eight bytes are cleared and nobody has read them. It is a weaker claim than `uint64` and that is
the point — the previous claim was not supported, not merely imprecise.

### Second pass: 123 unread spans were claiming to be scalars

The tail-padding check flagged `ActorDefinitionPayload` (`0x4C`, strictest alignment 8). It is not a
violation. **Its entire claim to 8-byte alignment came from `unobservedSpan0018` typed `u64`** — a
span whose own meaning says *"declared gap span — inside the record by extent, no censused access"*.
Nobody has read those eight bytes. The alignment was an artifact of the `ctype`, and it escaped the
first pass only because `0x18` happens to be divisible by 8.

That turned out to be systematic. **123 rows named `unobservedSpan*`, all carrying the same
boilerplate meaning, were typed `u16`/`u32`/`u64`** — while **98 rows with the identical name and
identical boilerplate already used `u8[n]`**. The scalar form claims two things the evidence does
not support: that the bytes are *one value* rather than two halves or eight unrelated bytes, and
that the field is *aligned* to that width.

All 123 are now byte spans. The guard required the name prefix, the exact boilerplate meaning, and
`size` equal to the width the ctype implied — **123 of 123 matched on size, 0 mismatches** — and 53
span rows whose meaning says more than the boilerplate were left alone. Only `ctype` changed.

| | before | after |
|---|--:|--:|
| misaligned rows | 28 | **11** |
| of those, rows nobody has read | 7 | **0** |
| types failing tail padding | 3 | **2** |

**The second line is the one that matters.** Every remaining misaligned row now has a semantic name,
so the check reports only fields that claim to be understood — an unread span can no longer
manufacture an alignment finding.

### The two remaining tail-padding types are both explained, and neither is a defect

**`FieldRecord`, size 3, strictest alignment 2.** Its own instance expression settles it:
`*(void**)0x02ADD100 + 8 + fieldId * 3`. **The stride is 3, read from the indexing arithmetic**, so
this is a packed byte table and half of its records read their `uint16` at an odd address. That is
real engine behaviour on x86, not a layout error, and it is the packed-record class this check was
built to recognise rather than flag.

**`EvaluationContext`, size `0x2A`, strictest alignment 8.** `CALLER` storage — built on the
caller's stack by `BattleFormula_BuildEvaluationContext`. Its last member, `sourceLayerMask u8[16]`,
ends exactly at `0x2A`, so **the recorded size is the measured extent, not a `sizeof`**; a compiler
would pad the type to `0x30`. Worth stating for reconstruction: declaring this struct yields
`sizeof == 0x30`, and the `0x2A` in the store is the span the engine touches.

**Neither needs fixing, and both are recorded here so the next pass does not re-open them.**

### The `subAddr*` rows were a third checker defect, not a store defect

Four rows — `ManagerSub7FB0Record +0x104`, `ManagerSub0209BE80_5380 +0x342`,
`ManagerSub0209BE80_57E0 +0x25F4` and `+0x2654` — have **no `ctype` at all**, a `size` of 8, and a
meaning that reads *"an address taken by `<site>` and passed on; extent not established."* The 8
records that a `lea` happened. It is not a width, and the store never claimed it was one. Reading it
as a qword turned all four into alignment findings about a type nobody asserted. **An empty `ctype`
asserts nothing, so the check now skips those rows.**

### Where the 39 went

| after | misaligned | what changed |
|---|--:|---|
| first run | 39 | — |
| array form tested before the scalar shortcut | 28 | **checker defect** — every `u8[8]` judged as a qword |
| 14 bulk-clear / span / float-pair rows retyped | 14 | **store corrected** |
| 123 unread spans retyped to byte spans | 11 | **store corrected** |
| rows with no `ctype` skipped | **7** | **checker defect** — `size` read as a width it never was |

**Two of the four reductions were my own instrument and two were the store.** That ratio is the
honest summary of this pass, and it is the same ratio every other instrument in this kit has
produced on its first outing.

### The seven that remain are each a real question, and none is retyped on a guess

| row | width | offset | what its own meaning says |
|---|---|---|---|
| `RenderModelInstance +0xB6 packedWordB6` | `uint32` | `2 mod 4` | *"dword initialised to `0x00FF0000` — **a packed byte field**"* |
| `PostProcessParamContext +0x12C doubleSlot12C` | `uint64` | `4 mod 8` | *"8-byte `movsd` store at `001944A8`"* |
| `ActorStorageRecord +0x21 initWord21` | `uint16` | odd | *"word zeroed by the initialiser"* |
| `BattleTargetBuffer +0x01 clearedWord01` | `uint16` | odd | *"word cleared after the whole-buffer fill"* |
| `BattleStatsRecord +0x1C3 tailSentinelWord` | `uint16` | odd | *"initializer-written sentinel `0xFFFF`"* |
| `CharacterRenderRecord +0x40F recordIndex40F` | `uint16` | odd | *"-1-sentinel record index word (`0042C7CD` writes `0xFFFF`)"* |
| `Widget +0xA1 fieldA1` | `uint16` | odd | *"`0xFF80`"* |

**`packedWordB6` is settled and is the pattern for the rest.** Its constructor writes
`mov dword ptr [rcx + 0xb6], 0xff0000` — one dword store at an offset 4 does not divide — and the
row itself already says *a packed byte field*. The width is the instruction's; the fields inside it
are bytes.

**The other six are not settled, and are deliberately left as they are.** Four describe a *clear* or
a *sentinel fill*, which is the same instruction-width signature; but `recordIndex40F` may genuinely
be a `uint16` value at an odd offset inside a large packed record, and x86 permits exactly that. The
two readings need the accessor read, not a rule applied. **Retyping them on the strength of the
pattern is precisely the move this page exists to warn against.**

**What holds for all seven regardless of which reading wins:** *none of them can be declared as
written.* A `uint16` at an odd offset or a `uint32` at `2 mod 4` is not expressible in a plain C++
struct — the compiler inserts padding and moves every following member. A reimplementation must
either pack the containing type or treat these spans as bytes with explicit unaligned access. **That
is a reconstruction constraint and it is independent of the semantics.**

### The accessors were read, and four of the six are settled: nothing reads them at that width

The six were left open above because *"the two readings need the accessor read, not a rule applied."*
They have now been read, with a test whose negative is sound regardless of population: **an
image-wide scan for a word-sized access at each displacement.** A superset that finds nothing proves
the subset finds nothing, so a zero here is conclusive even though a non-zero would not be.

| row | word-sized writes, image-wide | word-sized **reads**, image-wide |
|---|--:|--:|
| `ActorStorageRecord +0x21 initWord21` | 1 — `mov word [rbx+0x21], r13w` | **0** |
| `Widget +0xA1 fieldA1` | 1 — `mov word [rdi+0xa1], 0xff80` | **0** |
| `BattleStatsRecord +0x1C3 tailSentinelWord` | 2 — `r13w`, `0xffff` | **0** |
| `CharacterRenderRecord +0x40F recordIndex40F` | 2 — `di`, `0xffff` | **0** |

**Not one of the four is ever read as a word anywhere in the image.** That settles the question the
table above posed. `recordIndex40F` was the row that might have been a genuine `uint16` at an odd
offset — its meaning calls it a *"-1-sentinel record index word"* — and **nothing consumes a word
there**. The sentinel is written and never read at that width. The same holds for the other three.

So in all four the `uint16` is **the width of the writing instruction**, not a field, and the
decomposition inside those two bytes is unknown. They join the class this page opened with.

**NOT CLAIMED:** that the bytes are never read *individually*. A byte read at `+0x21` or `+0x410`
would appear at a different displacement, and byte displacements that small are shared by hundreds
of unrelated types, so the superset argument gives nothing there — a scan would return thousands of
hits belonging to other objects. What is claimed is exact and is the claim the rows made: **no read
of the declared width exists.**

### `doubleSlot12C`: one write, no read, on every route that can be bound to this type

`PostProcessParamContext +0x12C` has exactly one access in the bounded population — the cited
`movsd qword ptr [rcx + 0x12c], xmm0` at `001944A8`. The seven bodies that load the singleton slots
(`01F7F5F0` / `01F81300`) touch `+0x12C` not at all, and `00194490` itself is **not** among them: it
receives the object as an argument, which is why the slot-loader set alone would have missed the
write.

An image-wide scan does find a `movsd` **read** at `007C0217` — but its body `007BFFA0` never
touches either slot, so it cannot be attributed to this type and is not counted. `0x12C` is an
ordinary displacement. **Written once by a scalar-double move, read on no route that can be bound
to this object.**

*A note for whoever types this row: `movsd` moves a scalar **double**, so `uint64` understates what
the instruction says. Retyping would not remove the alignment problem — a `double` at `4 mod 8` is
no more declarable than a `uint64` — so it is recorded rather than changed.*

**Residue after this pass: `RenderModelInstance +0xB6` settled by its constructor, four settled as
write-only at their declared width, `+0x12C` settled as write-only on all bindable routes. Seven
rows, none now resting on an unread assumption, and none retyped on a pattern.**

### Amendment: the boilerplate has two wordings, and the first patch matched only one

**123 became 128.** The span guard keyed on a meaning starting `declared gap span`. There is a
second, identical class whose boilerplate reads **`declared tail span`** — the same statement about
a span at the *end* of a record rather than between fields — and five of its rows carried a
multi-byte scalar while twenty already used `u8[n]`.

It was found by following one row rather than by re-running anything: `WorldLootPickupNode +0x5C
unobservedTail005C u32`. **The alignment sweep never flagged it**, because `0x5C` is divisible by 4,
so the wrong ctype was invisible to the check that found all the others. A guard written from the
rows it was built on will match the wording those rows happened to use.

*Also noted, and deliberately not changed:* `fields.tsv` carries a **blank line at line 2567**,
between `WorldLootPickupNode` and `SecondaryContextElement`, and the file ends without a trailing
newline. Both predate this work — they are in `HEAD` — and the validator tolerates them (2,960
fields, 0 errors). Recorded rather than tidied, so that the diff of this change stays the change it
claims to be.

### The signature is the run, not the phrase "cleared by init"

**A caution against over-applying the finding above, written because the next reader will be tempted
and so was I.** `RenderModelInstance` has two more rows whose evidence is word-for-word the same as
the five that were retyped:

| row | evidence, in full |
|---|---|
| `+0x30 qwordSlot30 uint64` | `00504A1A mov qword [rcx+0x30],rbx.` |
| `+0x38 qwordSlot38 uint64` | `00504A5A mov qword [rcx+0x38],rbx.` |

One zero store each, no read recorded — the same standard by which the other five were judged not to
be fields. **They were left alone, and the reason is the whole point of the earlier entry.**

What made `+0x04` … `+0x24` a bulk clear was not the phrase *"cleared by init"*. It was the
**shape**: five stores, **contiguous**, on a **stride of 8**, at offsets **8 does not divide**,
emitted **consecutively** — `00504A05`, `A21`, `A28`, `A2C`, `A30`. That is a region being filled,
and no compiler lays out five qword *fields* that way.

`+0x30` and `+0x38` have none of it. They are **8-aligned**, **not contiguous** with that run or
each other, and written far apart — `00504A1A` and `00504A5A`, with a dozen unrelated stores in
between. **An aligned qword zeroed once at construction is the most ordinary thing in a C++ object:
a null-initialised pointer.** Retyping them on the strength of a shared phrase would replace a
well-supported reading with a worse one.

**So the detector is the run, and it is narrow on purpose.** A keyword sweep for *cleared / zeroed /
ctor stores* over rows with no recorded read returns **74 rows**, and that number is not a defect
count — it sweeps in float slots initialised to `1.1f`, sentinels set to `-1`, and ordinary null
pointers. A typed non-zero constant says what a value *is*; a zero says nothing. Only where a zero
fill also has the run's shape does the store's field decomposition rest on nothing.

**What this leaves open, stated rather than counted:** an aligned zero-cleared slot with no reader
found is a *weak* row — it may be a null pointer, or it may be part of a wider clear whose shape the
alignment check cannot see, exactly as `unobservedTail005C u32` hid at `0x5C`. Separating those needs
the reader search, per type and per offset, and small displacements like `0x30` are shared by
hundreds of unrelated objects, so the image-wide negative that settled the seven above is not
available here. **It is recorded as an open question, not resolved by analogy.**

### Answering "does anything read it?" for a record reached through an accessor

The open question left above — *an aligned zero-cleared slot with no reader found is a weak row, and
separating those needs a per-type reader search* — now has an instrument for one route form:
**`reader_search_returned.py`**.

**The bound comes from the store's own `route` column.** `RenderModelInstance` is
`FN 0x003E55B0+0x0`: an accessor RETURNS the record, so every caller holds it in `rax` immediately
after the call and nowhere else does a bare displacement mean this type. The scan walks each caller,
keeps the set of registers currently holding the record, propagates `mov rX, rY`, drops `rax` across
a call and drops any register something else writes.

**This is the alternative to the sweep that cannot work.** An image-wide search for `[reg+0x30]`
returns hundreds of unrelated objects — the same trap that produced a 75-reader false population
earlier in this work. The route column is the only thing that makes the question answerable.

**The first version reported zero at every offset, and that was the instrument, not the answer.** It
stopped tracking at the first branch, and real bodies branch within a few instructions, so the window
was usually empty and the run read as a clean negative. **It was caught by a positive control rather
than by inspection**: `+0xB6`'s own store row names its accessor, so a run that cannot see `+0xB6`
is broken. Walking the whole body — the same-register/same-function technique used elsewhere in this
kit — fixes it.

**Result for `RenderModelInstance`, 31 call sites in 24 bodies:**

| offset | reads | writes | |
|---|--:|--:|---|
| `+0x04` | 0 | 4 | `mov dword [rsi+4], eax` in `0042D050` — **the binder its row already names** |
| `+0xB6` | 0 | 2 | `mov word [rdi+0xb6], ax` in `0042F4C0` — **the function its row already names** |
| `+0x30` | **0** | **0** | nothing on this route |
| `+0x38` | **0** | **0** | nothing on this route |

**The two controls fire in the same population that returns zero for `+0x30` and `+0x38`**, so the
zero is a property of those offsets and not of the scan.

**It still does not settle them, and the rows are unchanged.** `RenderModelInstance` is also reached
by walking the container's chunked array, so this route is one of several; and a record passed into a
callee is not followed, which makes every count a floor. What the run supports is bounded and useful:
**`+0x30` and `+0x38` are untouched on the type's own accessor path, while two neighbouring fields
are not.** That strengthens the weak-row reading without converting it into a retype.

*Reach: four types carry an `FN` route — `RenderModelInstance` and the three save-payload types that
share accessor `0x002EF640`. The other 83 game-side types with a route use `EMBED`, `ARRAY`, `PTR`,
`STATIC` and friends, which need their own seeding and are not covered here.*

### The third generator: a census for the `*(void**)0xADDR` class

The route grammar above ends with a standing note — *"`PTR`/`PARRAY`/`SLOTPTR` rows are the
`*(void**)0xADDR` class no generator consumes yet; they are recorded precisely so that third
generator has a population."* **`gen_ptr_census.py` is that generator**, for the bare `PTR` form.

`gen_static_census.py` handles records AT a fixed address, where every access is RIP-relative.
`record_field_scan.py` handles records reached by a chain from a parent. Neither handles the
commonest singleton shape in this image: **a pointer parked in a global, loaded into a register, and
indexed off.** For `PTR 0xADDR [+0xOFF]` the instance is `*(ADDR) + OFF`, so a `mov rX, [rip -> ADDR]`
seeds the base and every `[rX + OFF + disp]` afterwards is a field.

**The control is an existing census, not a site count.** `PostProcessParamContext` is `PTR 0x01F7F5F0
| PTR 0x01F81300` and already had `postprocess-context-accesses.tsv`, produced by different work
through call-argument routes. Reproducing offsets and instruction text is a far stronger check than
proving the decoder runs.

**The control caught two defects that a count would not have.**

* **Seeding on the load alone returned ZERO accesses through `01F7F5F0`** — for the one body that
  most certainly has them. A lazy singleton's initialiser does not load the instance, it *publishes*
  it: `0018EEE0` reads the slot into `rsi`, finds it null, **reassigns `rsi` from the fresh
  allocation** and stores it back at `0018EFEC`. The load-only seed dropped `rsi` at the
  reassignment. **The value written to the slot is the instance**, so the store seeds too.
* **`nop word ptr [rax + rax]` is not an access.** A multi-byte NOP decodes as a memory operand like
  any other, and unfiltered it produced the run's only *"declared-unread span with a censused
  access"* — a finding that was entirely one alignment instruction.

**Yield — 920 accesses across seven types, five of which had no census at all:**

| type | size | accesses | offsets | |
|---|---|--:|--:|---|
| `BattleSystemState` | `0x7410` | 329 | 39 | **new** |
| `ManagerSingleton0209BE80` | `0x10FD0` | 202 | 42 | **new** |
| `GameSettingConfig` | `0x65C` | 153 | 33 | had a census; not overwritten |
| `CharacterRenderSystemTail` | `0x130` | 141 | 24 | had a census; not overwritten |
| `PostProcessParamContext` | `0x4A8` | 58 | 45 | the control |
| `ImageBackedStateBlock` | `0x4818` | 32 | 8 | **new** |
| `BootSingleton01F7F598` | `0xDD8` | 5 | 3 | **new** |

**On the control type it adds 38 sites the hand census does not have**, every one a read in
`0018EEE0` off the verified `rsi` — a run copying the parameters out of the singleton. The existing
census tracks call arguments and is structurally blind to the global-load route, so **the two methods
are complements, not competitors**: it reproduces only 20 of the control's 777 sites, and that ratio
is the honest measure of same-function tracking, not a defect.

**Two zeros, and both are confirmations rather than failures.** `FieldRecordTable` (`PTR 0x02ADD100`)
returns nothing because **`02ADD100` holds a 32-bit handle, not a pointer** — established
independently by the ctor/dtor ownership audit, and a pointer-shaped scan should find nothing there.
`AchievementState` (`PTR 0x020927C0+0x3844`) returns nothing because a base that deep is reached by
`lea`, not by a displacement this scan follows.

**And the result that matters for the unknown-field frontier: of all 920 accesses, ZERO fall inside a
span the store declares unread.** An independent method, on types that mostly had no census, does not
contradict a single *"no censused access"* claim.

*Limits, stated: same-function only, so every count is a floor; direct seeding only, so an instance
reached through a function pointer is invisible; and it records the instruction without inferring a
type, which is `gen_static_census.py`'s rule and remains the right one.*

### `PARRAY`/`SLOTPTR`: the generator was built, controlled, and is the wrong instrument

`gen_ptr_census.py` finished the `PTR` third of the class. **`gen_parray_census.py` finishes the
other two, and its main result is a negative worth recording so nobody builds it twice.**

Controlled against `CharacterRenderRecord`'s existing census it reproduces 40 sites and **adds 3,
all three verified by hand** — each resolves its `[rip + …]` to `022C6F28` and reads element 0 or
element *i* at a real offset. So the method is sound. It is also **1.5 % of that census's 2,664
sites**, and on types with no census the yield collapses:

| type | accesses |
|---|--:|
| `Widget` | 12 |
| `BattleUnit`, `SpawnRecord` | 2 each |
| `NameBindingEntry`, `NameBindingSubRecord`, `ScheduledTaskRecord`, `FieldRecord`, `EfxCallerTemplate`, `MessageWindowRecord` | **0** |

**The reason is structural, not fixable by more effort.** A singleton is *loaded from its global in
the function that uses it*, which is what makes `PTR` work — 920 accesses across seven types. An
array element is **passed as an argument**, which is exactly why the `CharacterRenderRecord` census
needed route-tracking to reach 2,664 rows. **A same-function scanner is the wrong shape for
`PARRAY`/`SLOTPTR`**, and the route grammar's expectation that one generator would serve all three
forms does not survive measurement.

### And it found a route that says something false to any generator reading the grammar

**`AuthoredTableHeader`'s route was `SLOTPTR 0x02EBEF70 stride=0x8 count=40`.** Under the documented
grammar — `SLOTPTR 0xADDR stride=0xS [count=N]` → instance *i* = `*(ADDR + i*S)` — that means forty
consecutive slots from `02EBEF70`. **Both halves are wrong.** The band is **146** qword slots
(`02EBEF70..02EBF3FC`), and **40 is a membership count, not a table length**.
`CONTRACT-authored-table-row-lookup.md` says so, and warns against exactly the inference the route
invites:

> *"Forty of them are headers of this shape. Not all are: `02EBF190` holds `BattleSystemState`.
> Membership is established by a slot exhibiting the idiom, never by its address falling in the
> band — a distinction that cost a first measurement its extra fields."*

**Unbounded, my scan reached `02EBF190` and booked 1,461 `BattleSystemState` accesses as a 32-byte
header.** Bounding the table by `count` cut that to 381 — and 381 is still wrong, because it scans a
span chosen by *position*, which the contract says is never how membership works.
`MessageWindowRecord` went from 64 accesses to **0**: every one had been contamination.

**The prose was right and the machine-readable column was not** — and the column exists precisely so
a generator can consume it. The row now uses the grammar's own escape hatch, `DYNAMIC <free text>`
(*"documented for humans, not consumable by a fixed-base generator"*), and carries the band extent,
the membership rule and the `BattleSystemState` exception. `check_storage_class.py` still parses 93
route alternatives with 0 hard failures; the store still validates 276 / 2,960 / 0 / 0; and
`gen_parray_census.py` now **refuses the row** instead of producing a confident false census.

**The general lesson, which applies to the other 92 route alternatives:** `count=` is doing two jobs
in this grammar — *how many entries the table has* and *how many of them are this type*. Where those
differ, a consumer of the documented meaning is misled, and only reading the owning contract page
reveals it. **This one was caught because a generator was finally written against the column; the
rest have never been consumed by anything.**

### Two types claiming the same static bytes — `check_static_spans.py`

`check_storage_class.py` checks that an `EMBED` fits its parent and that two `EMBED`s into one
parent do not overlap. **Nothing checked the same thing for static anchors** — an
`ARRAY 0xADDR stride=0xS count=N` claims `N*S` bytes at a fixed address and no instrument asked
whether another type claims the same ones. The `AuthoredTableHeader` route defect above is that
family, so the check now exists.

**A pointer CELL shared by two types is reported and never failed**, because it is usually the
routes agreeing: one type interior to another reads the same cell at two depths. All three the store
has are of that kind — `ImageBackedStateBlock`/`AchievementState` at `020927C0`,
`CharacterRenderRecord`/`CharacterRenderSystemTail` at `022C6F28`, `FieldRecordTable`/`FieldRecord`
at `02ADD100`. A collision between two *data* spans is the one that cannot be right.

**There is exactly one, and it is a duplicated type.**

`ItemClassDescriptor` and `InventoryClassDescriptor` carry **byte-identical routes** —
`ARRAY 0x01EEBCC0 stride=0x58 count=15 index=(itemId>>12)` — the same size, the same category, and
both `PROVEN`. They are the same authored table, described twice by investigations that came at it
from opposite ends: items/equipment (`12-…`) and the save-payload rebase
(`19-…/the-save-payload-field-map.md`).

**Their field maps are complementary, not contradictory**, which is why neither investigation
noticed:

| offset | `ItemClassDescriptor` | `InventoryClassDescriptor` |
|---|---|---|
| `0x00` | *unread span* | `offsetA uint64` |
| `0x08` | `packedCounts void*` | `pointerA void*` |
| `0x10` | `storageElements uint32` | *unread span* |
| `0x18` | *unread span* | `offsetB uint64` |
| `0x20` | `auxBitsetA void*` | `pointerB void*` |
| `0x28` | *unread span* | `offsetC uint64` |
| `0x30` | `auxBitsetB void*` | `pointerC void*` |
| `0x38` | `registryClassId uint32` | *unread span* |
| `0x3C` | `itemCount uint32` | `entryCount uint32` |
| `0x40` | *unread span* | `firstIndex uint32` |
| `0x50` | `queryHandler void*` | *unread tail* |

**Each declares fields the other calls unread, and the three pointer slots agree on being pointers.**
The save-side reading describes the *rebase machinery* — an authored 32-bit offset at `+0x00`,
`+0x18`, `+0x28` that the loader resolves into the pointer beside it — and the items-side reading
describes *what those pointers point at*. Those are two views of one table, not two answers to one
question.

**So this is not a claim to adjudicate but a merge to perform, and it is worth performing**: between
them the two rows cover `0x00`, `0x08`, `0x10`, `0x18`, `0x20`, `0x28`, `0x30`, `0x38`, `0x3C`,
`0x40` and `0x50` — **a materially more complete layout than either shows alone**, for a table that
the encoded-id space and the save payload both depend on.

**NOT MERGED HERE, deliberately.** Four offsets carry a name from each side (`packedCounts`/
`pointerA`, `auxBitsetA`/`pointerB`, `auxBitsetB`/`pointerC`, `itemCount`/`entryCount`), and picking
the surviving name is a semantic judgement with two documented owners. Merging two `PROVEN` rows by
choosing names unilaterally is how a real distinction gets flattened; it is registered as a
contradiction task instead.

### Auditing the other `count=` routes — `check_route_counts.py`

`AuthoredTableHeader`'s route was wrong because `count=` was carrying a *membership* number where
the grammar promises a *table length*. **Twenty-eight routes carry `count=` and exactly one had been
checked.** This puts each route's count beside every count-shaped number in its own document, and
**issues no verdict** — counts legitimately differ between a table, its populated subset and the
slots one function walks. Two rows came back worth reading, and one of them mattered.

### `ScriptNativeDispatchRecord`: I read it wrong first, and the image corrected me

The document's header carries a struck-through base:
*"~~VA `0x01EED720`~~ **VA `0x01EED700`. `0x01EED720` is `tbl + 0x20`**"*, with a key-address row
saying **"count at `+0`, record 0 at `+8`"**. The store's route still says
`ARRAY 0x01EED720 stride=0x20 count=1496 index=callId`.

**My first reading was that the store carried a superseded base and every `callId` resolved one
record high. That reading was wrong, and the measurement is what corrected it.** Counting non-null
`.text` pointers in all four qword slots across all 1,496 records, in both frames:

| frame | `+0` | `+8` | `+16` | `+24` | total |
|---|--:|--:|--:|--:|--:|
| records at **`01EED720`** (the store's route) | **1234** | **276** | **229** | **0** | **1739** |
| records at `01EED708` (base + 8) | 277 | 230 | 0 | 1234 | 1741 |

**CORRECTED 2026-09-19 (OPUS). Everything below this point in the original section was wrong, and
the table above refutes it — I read my own measurement backwards.**

I dismissed the second row as *"incoherent: the third callback always empty and the fourth always
full"*. **That is exactly what the correct frame predicts.** The accessors read
begin `[tbl + 0x20n + 8]`, poll `[tbl + 0x20n + 0x10]` and result `[tbl + 0x20n + 0x20]`, and
**nothing reads `tbl + 0x20n + 0x18`** — so a record based at `tbl + 8` is
**begin `+0`, poll `+8`, UNUSED `+0x10`, result `+0x18`**. An always-empty *third* slot and a
well-populated fourth is the shape of that record, and the `01EED708` row matches it to the count:
277 begins, 230 polls, **0 unused**, 1,234 results.

The `01EED720` row puts the empty slot *fourth*, which no accessor supports.

> **So the census DID discriminate — I just read it against a guess instead of against the
> accessors.** Addendum bv says a census cannot separate two frames that are rotations of each
> other, and that is true of the *column cleanliness* it was run for. It is not true of this
> table, which carries a zero in a named position. **The measurement was sound and the
> interpretation was invented**, which is the worse of the two failures because nothing about the
> output looks wrong.

**Records begin at `01EED708`, not `01EED720`.** `01EED700` holds the count dword `1496` at `+0`,
and `0x01EED720` is **`result(0)`** — the fourth qword of record 0. The store's route string said
`01EED720` and its own four field rows said `+0 begin / +8 poll / +0x10 unused / +0x18 result`,
which is the `01EED708` frame: **the store contradicted itself and the field rows were right.**
Both the route and this section are corrected; the page was restored by FABLE in `6363497c6` and
the contradiction was filed by them as
`FABLE-REQ-OPUS-TYPE-STORE-DISPATCH-RECORD-ROUTE-STRING-CONTRADICTS-ITS-FIELD-ROWS`.

**What is wrong is on the page, and it is self-inconsistent rather than merely stale.** *"Record 0 at
`+8`"* puts `01EED720` at record 0's `+24`, yet the same page calls `01EED720` *"the **result**
callback of record 0"*, which is `+16`. Its family table reports **1,741** callbacks against base
`01EED700` while its certified slot table reports **1,739** against `01EED720` — the two frames,
each with its own total, on one page. Registered as
`OPUS-CON-DISPATCH-TABLE-RECORD-0-AT-PLUS-8` for FABLE, who made the 2026-09-16 relabel, with the
census as the discriminator.

**The lesson is about the instrument, not the page.** A route that disagrees with its document is
not evidence that the *route* is wrong. Here the column was right and the prose was not, and only
measuring both frames against the image could say which — the same discipline that the
`AuthoredTableHeader` row, where the prose was right and the column wrong, required in the opposite
direction.

### Asking the image where a table stops — `check_route_extents.py`

`check_route_counts.py` compares a route's count with the numbers in its own document, which cannot
catch a route whose prose agrees and is also wrong. **This asks the image.** An authored table looks
like records for `count` elements and then stops, so the elements `[0, N)` are scored for
pointer-likeness and compared against the `N` that follow.

**Its first run corroborated nothing and flagged 4 of 4 scorable rows** — the signature every
instrument in this kit has produced on its first outing. The cause: it summed the `.text` and data
pointer fractions, so `ScriptNativeDispatchRecord` — a **callback** table (0.29 text, 0.00 data)
followed by a region of **data** pointers (0.00 text, 0.39 data) — scored as a continuation. That is
the opposite of what those numbers say. **Comparing the categories separately** turns it into:

| type | | inside → after | |
|---|---|---|---|
| `ScriptNativeDispatchRecord` | text | 0.29 → **0.00** | **corroborated** — the callbacks stop exactly at 1,496 |
| `ItemClassDescriptor` / `InventoryClassDescriptor` | text | 0.12 → 0.42 | worth reading |
| `AchievementDescriptor` | — | — | uninformative: no pointer slots to score |

The dispatch corroboration is independent of the census argument recorded above and reaches the same
frame from different evidence.

### The flagged table was fine, and reading it anyway found an undeclared function pointer

`ItemClassDescriptor`'s count of 15 is **correct**: records #13 and #14 carry the class shape, and
#15 onward are a different structure entirely — all slots non-zero, no `.text` pointers, `+0x38` =
8193. The 0.42 after the table belongs to whatever follows it. **A false positive, and worth the
look it prompted.**

Reading all fifteen records slot by slot:

| offset | non-zero in | what the store said |
|---|--:|---|
| `+0x08`, `+0x20`, `+0x30` | **0 of 15** | `packedCounts`, `auxBitsetA`, `auxBitsetB`, all `void*` |
| `+0x00`, `+0x10` | 8 | `+0x00` *unread*, `+0x10` `storageElements` |
| `+0x38` | 15 | `registryClassId` / `itemCount` |
| **`+0x48`** | **12, every one a `.text` pointer** | **inside a 16-byte unread span** |
| `+0x50` | 8, every one a `.text` pointer | `queryHandler` |

**Two findings.** First, the three `void*` slots are **zero in the shipped image**, which is exactly
what the save-side reading predicts — an authored offset at `+0x00`/`+0x18`/`+0x28` and the pointer
resolved into the slot beside it at runtime. That is independent support for the merge registered as
`OPUS-CON-ITEMCLASS-INVENTORYCLASS-SAME-TABLE`, and it says which of the two readings describes the
image: a row declaring a `void*` that is null in every record is describing runtime state.

Second, **`+0x48` holds a per-class function pointer in 12 of 15 records** — six distinct handlers,
`002FD150`/`002FD420`/`002FD530`/`002FD640`/`002FD780`/`002FD880` — a second handler family beside
`queryHandler` at `+0x50`, whose values are the different pair `002FD8D0`/`002FD970`. The store had
those bytes inside `unobservedSpan0040`. The span is split: `+0x40` keeps the name and is now
**measured zero in 15 of 15**, and `+0x48` becomes `classHandler0048`. The three records null at
`+0x48` are the same three null at `+0x50`.

**NOT CLAIMED: what the handler does.** The name records where it sits and what it is; pairing it
semantically with `+0x50` belongs to the page that owns the table. **An unread span that turns out
to hold a function pointer in 80 % of its records is the clearest possible case of *unknown* not
meaning *empty*.**

### Sweeping every unread span whose bytes are in the image — `check_unread_spans_in_image.py`

`classHandler0048` was found by looking at bytes the store said nobody had read. **"Unread" is a
statement about ACCESSES; the content of the span is a different question, and where the storage is
authored data it can simply be read.** So every declared-unread span of every type whose route puts
its bytes inside a section's raw data was swept.

**The reach is the first result, and it is small on purpose.** Only **6** types have bytes in the
shipped image; **77** reach storage that is allocated, relocated or zero-filled at runtime. A `.bss`
address is past its section's raw data and reads as zero, so a zero there is the file saying nothing
— those types are counted, never judged. **The type store is overwhelmingly about runtime objects,
and this question can only be put to a sixteenth of it.**

Within that sixteenth: 8 unread spans, 5 with content, and **no remaining span holds a `.text`
pointer**. `classHandler0048` was the only function pointer hiding in an unread span, and it is now
declared.

### What the sweep did find is a second, independent confirmation of the merge

The non-zero counts line up exactly with the offsets the *other* type declares:

| `ItemClassDescriptor` unread span | non-zero in | what `InventoryClassDescriptor` declares there |
|---|--:|---|
| `+0x00` (8 B) | **8 of 15** | `offsetA uint64` |
| `+0x14` (12 B, straddling `+0x18`) | **1** | `offsetB uint64` |
| `+0x28` (8 B) | **1** | `offsetC uint64` |
| `+0x40` (16 B, was) | 12 | — now `classHandler0048` |

And from the other side, `InventoryClassDescriptor`'s `unobservedTail0044` scores **20 non-zero
slots** — which is exactly `12 + 8`, the two handler families at `+0x48` and `+0x50` that its tail
swallows. The slots are read from `+0x44` and so straddle both pointers, which is why the `.text`
column reads zero there: the halves are non-zero, the qwords are not pointers.

**So each type's "unread" spans are non-zero precisely where the other type declares a field, with
matching counts.** That is no longer an argument from complementary shapes — it is the same bytes
measured twice. Recorded on `OPUS-CON-ITEMCLASS-INVENTORYCLASS-SAME-TABLE`.

### The folded-base blind spot, and the census that fills it — `gen_array_census.py`

**A correction first: I claimed eight `.bss` ARRAY types had no census, and `ActorManagerSlot` has
one.** I had grepped for the type's NAME inside `*-accesses.tsv` files, which do not carry it; its
field evidence names `actor-manager-record-accesses.tsv` outright. Seven of the eight do appear to
have none, checked properly this time — by what their evidence cites, not by a name match.

`gen_static_census.py` censuses a record at a fixed address through RIP-relative operands. Run
against `ActorManagerSlot` with the counts the store's own evidence records, it **failed its control
and refused to write**: `+0x00` wanted 11 and got 60, `+0x12` wanted 1 and got 0. That is the tool
behaving correctly — those counts were gathered through a **base register**, a different population
of the same table.

`gen_array_census.py` is the other half: it seeds a register from a `lea` of the table address,
tracks element pointers through pre-multiplied indices, and records RIP-relative operands landing
inside the table.

**Its control failed too, and the failure was the right answer.** Against the same declared counts it
produced 7, 0 and 0. It should not match them: they belong to the other route. The validation that
means something is the comparison of the two censuses — and they are **entirely disjoint**:

| | sites |
|---|--:|
| `actor-manager-record-accesses.tsv` (existing, base-register route) | 194 |
| this scan (RIP-relative route) | 113 |
| **reproduced** | **0** |
| **added** | **113**, at 10 offsets |

**And one of those offsets is `+0x13`**, whose own evidence says: *"FOLDED-BASE ACCESS … the field
offset is folded into a lea'd link-time constant, so the access carries no displacement a
`[reg+disp]` census can match."* **The store named a blind spot it could not see into, and this is
the instrument that sees into it.** The other added offsets — `+0x10`, `+0x11`, `+0x17`, `+0x48`,
`+0x58`, `+0x60`, `+0x1E0`, `+0x1E4` — are in the same class.

**So a control that fails is not automatically an instrument that is wrong.** Twice now on this
table a control mismatch meant *the populations differ*, which is exactly what the refusal message
in `gen_static_census.py` says it means. The mismatch is informative and the refusal is right; what
would have been wrong is writing a census that quietly disagrees with its own record.

*A record type in this image can be reached three ways — by argument, by a pointer held in a global,
and by an address folded into a link-time constant — and this kit now has one census generator per
route. None of them is a superset of the others, and the `ActorManagerSlot` overlap of zero is the
sharpest available demonstration of that.*

### `SpawnGroupLedger` returned zero through every route, and the instrument was why

A type whose own field evidence cites thirteen access sites came back with **no accesses at all**
from the array census. That is not a gap in the database; it is a gap in the scan, and the
disassembly names it in one line:

    00306EB2  lea ecx, [rdi - 1]            ecx = group - 1
    00306EB8  lea rcx, [rdx + rdx*2]        rcx = 3 * (group - 1)      <-- the multiply
    00306EBC  lea rdx, [rip + ...]          rdx = 02EC13C0, the base
    00306EC3  lea r8,  [rdx + rcx*8]        r8  = base + 24 * (group - 1)
    00306ED7  or qword ptr [r8], rax

**The compiler never multiplies by 24.** It multiplies by **three** with a `lea`, and lets the
addressing mode's scale of 8 supply the rest. A scan that recognised `imul` and `shl` as the ways to
build an index could not see a stride of 24 at all — and 24, 40 and 72 are all built this way, since
`lea [x + x*k]` covers ×3, ×5 and ×9.

Index registers are now tracked by their **multiplier** rather than by "is this a multiple of the
stride", so `mul[rcx] = 3` and `3 × scale 8 = 24` identifies the element pointer.

**The result reproduces the store's own sites**, which is the control that matters here: `00306ED7`
(or-assign), `00306EE2` (and-clear) and `00306EEA` (and-clear at `+8`) are all named in the field
evidence, gathered by different work, and all three come back — with four more the same evidence
mentions in prose.

*The general point is the one this page keeps making from a new direction: **a zero from an
instrument is a statement about the instrument until it is shown otherwise.** Three separate scans
reported nothing for this type, and the type was never the problem.*

### Census coverage, and two files that are one census

**34 `*-accesses.tsv` files exist. 18 are cited by the store's field evidence; 12 were cited by
nothing at all — and all twelve were mine, published this session.** Evidence that nothing points at
is evidence a reader cannot find, so the ten genuinely-new types are now in
`check_census_widths.py`'s map and subject to the same width cross-check as everyone else's.

**Wiring them in produced exactly one disagreement, and it was worth having.**
`WorldLootPickupNode +0x04 state` is declared 4 bytes against a census of `{8: 10, 4: 1}`. All ten
8-byte writes are `Loot_InitializeWorldPickupPool`'s per-slot `mov qword [node+4], rax`, one for
each of the ten pool slots, each covering `+0x04..+0x0B` — **this field together with the first half
of the unread span at `+0x08`**. The single 4-byte access, `cmp dword [rbx+4], ebp`, is the field's
own free-slot test. The declaration is right and the row now carries the checker's
`WIDTH DELIBERATE` exemption with that reason, as `objectHandle` at `+0x58` of the same type already
does. Back to **0 disagreements**.

**A census I should not have published.** `battle-system-state-accesses.tsv` (329 rows) is a
**complete subset** of the existing `battle-state-block-accesses.tsv` (1,109) — 329 shared, **0**
of mine unique. `BattleSystemState` already had a census under a name that does not contain the type
name, and I concluded it had none by searching for the name. Removed. The same test on
`ActorManagerSlot` gives the opposite answer — **0 shared, 113 unique** — which is why that one
stays.

### The family has two schemas, and one file is a second copy of another

| shape | files | `disp` column |
|---|--:|---|
| `function \| name \| site \| disp \| kind \| instruction \| route \| note` | 33 | 4 |
| `word \| site \| kind \| instruction \| function \| name` | 1 | **absent** |

The outlier is `formula-scratch-block-accesses.tsv`, and its `word` column is **not** a word index —
it holds the **absolute address** of the access. Subtracting the base `0x02AEDFB8` turns it into a
displacement, and then:

**All 912 of its `(site, displacement)` pairs are identical to all 912 of
`battle-formula-scratch-accesses.tsv`. Zero rows unique to either.** They are one census stored
twice, in two directories, under two schemas.

**NOT DELETED, deliberately.** The outlier is cited by `the-formula-scratch-block.md`,
`ADDRESS-INDEX.md` and a peer's inbox; removing it would break three live citations, and which copy
survives is its owners' call, not mine. What is recorded here is the measurement: the content is the
same, and **every displacement-keyed instrument in this kit silently skips the 912 rows of the
outlier** because it looks for a `disp` column that is not there. A duplicate that no tool can read
is not harmless — it is a second source that can drift from the first without anything noticing.

### How big the census gap actually is, and how much of it is reachable today

`check_census_widths.py` reports **1,163 declared rows in 243 types outside its reach** for want of a
census mapping. Read as a single number that overstates the gap badly: **179 of those types are
Phyre-imported**, and reflection gives members and offsets but never an access census, so they are
not missing one — they cannot have one from this kind of work.

The figure that matters is the game-side split. Of **97** game-side types, **30** are now in the
width-check map and **67** are not. By the route verb of the 67:

| route verb | unmapped types | a generator exists? |
|---|--:|---|
| `EMBED` | 21 | no — the parent's census covers the bytes, not the child |
| *(none)* | 11 | no — stack locals, caller buffers, file layouts |
| `ARRAY` | 8 | **yes** — `gen_array_census.py` |
| `DYNAMIC` | 7 | no, by definition of the verb |
| `PARRAY` | 5 | **yes** — `gen_parray_census.py` |
| `STATIC` | 4 | **yes** — `gen_static_census.py` |
| `CHAIN` | 3 | **yes** — `record_field_scan.py` |
| `FN` | 2 | partially — `reader_search_returned.py` answers reads, not a full census |
| `RELOFF` | 2 | no |
| `PTR` | 2 | **yes** — `gen_ptr_census.py` |
| `SLOTPTR` | 2 | **yes** — `gen_parray_census.py` |

**Twenty-one game-side types are censusable right now with instruments that already exist**, largest
first: `Mt19937State` (`0x9C4`), `EfxCallerTemplate` (`0x890`), `MessageWindowRecord` (`0x410`),
`AiOrderSet` (`0x170`), `InputBindingRecord` (`0x15C`), `NameBindingSubRecord` (`0x120`),
`RenderModelInstanceContainer` (`0x70`), the two `0x58` class descriptors, `ScheduledTaskRecord`,
`NameBindingEntry`, `AchievementState`, `TextLayoutRecord`, `ScriptNativeDispatchRecord` (1,496
records), `ChunkedSlotBankEntry`, `PartyReadMachineRecord`, `ChunkedSlotEntry`,
`SharedGameplayLcgState`, `FieldRecord`, `Widget`, `FieldRecordTable`.

**The 21 are a worklist, not a promise.** Three of this session's runs returned almost nothing —
`gen_parray_census` on six types, `gen_static_census` on `ActorManagerSlot`, the first
`SpawnGroupLedger` pass — and in two of those three the instrument was at fault rather than the
type. **A route that a generator can parse is not the same as a route the code actually takes**, and
the only way to tell them apart is to run it and read the result against something independent.

*The `EMBED` group is the largest and has no generator by design: a child embedded at a fixed offset
inside a parent is covered by the parent's census, at parent-relative displacements. Making those 21
rows visible is a projection problem — subtract the embed offset from the parent's census — not a
scanning problem, and no instrument here does it yet.*

### `EMBED` needed a projection, not a scanner — `project_embed_census.py`

`EMBED` was the largest group of game-side types without a census, and **none of them needed a new
scan.** A child at `Parent +0xOFF` occupies bytes the parent's census already records; the child's
census is those rows with `OFF` subtracted. Writing a scanner for them would have re-derived
evidence the corpus already holds.

**19 of the 26 `EMBED` types are projectable today** — their parent has a census on disk — and 13 of
those had none of their own. Projected: **371 rows**, largest first: `SecondaryContextElement` 176,
`BattleTargetBuffer` 69, `SpawnKeepImage` 37, `ManagerSub0209BE80_57E0` 27,
`ActorManagerSlotEntry` 26, `NavigationPathState` 16, `GambitConfig` 9, and six more.

**Seven of them project out of a census generated earlier in this same session** — the
`ManagerSub0209BE80_*` family comes from `manager-singleton-0209be80-accesses.tsv`, which
`gen_ptr_census.py` produced for a singleton that had no census at all. One scan of a parent made
seven children visible.

**The projection was checked, not assumed:** every emitted offset must land inside the child's
declared size. **13 of 13 do, 0 past the end** — which is also an independent test of the `EMBED`
offsets and strides in the route column, since a wrong offset would push rows off the end of the
child.

**THEY ARE NOT INDEPENDENT EVIDENCE, and the map says so.** If a parent's census is wrong at a
displacement, the child's is wrong at the same one, and a width check that passes on both has checked
one fact twice. Every projected row carries `embed <Parent>+0xOFF` in its route column so it can
never be mistaken for a scan.

### What the census coverage looks like after all of this

| | at session start | now |
|---|--:|--:|
| types in the width-check map | 20 | **48** |
| declared rows in scope | ~1,300 | **1,956** |
| declared rows outside its reach | 1,163 in 243 types | **1,006 in 228 types** |
| rows whose declared size disagrees with the census | 0 | **0** |

The remaining 1,006 are dominated by Phyre-imported types, which cannot have an access census from
static work, and by the `DYNAMIC`, `RELOFF` and routeless classes where no fixed base exists to scan
from. **The cheap coverage is now taken; what is left needs either a new route form or runtime
evidence.**

### Two routes did not conform to the grammar, and the route checker said nothing

`ChunkedSlotBankEntry` and `ChunkedSlotEntry` carried `ARRAY 0xADDR stride 0x20 count 5` — **without
the `=` the grammar above requires**. Against 38 conforming routes, those two were unparseable by
every generator, which is how they were found: both returned no census because no scan could read
their route at all.

**`check_storage_class.py` reported 93 route alternatives parsed and 0 hard failures both before and
after the fix.** It was accepting them loosely, so the one instrument whose job is to validate this
column did not notice that two of its rows were in a form nothing else could consume. Brought into
the documented form; the parse count is unchanged, which is the point.

*Both types still return zero accesses after the fix, so they are reached some way the array scan
does not cover — a separate question, and now a legible one.*

### The boilerplate makes a checkable claim, and now it is checked — `check_unread_vs_census.py`

Hundreds of rows carry *"declared gap span — inside the record by extent, **no censused access**"*.
That is not vague prose: it is a statement about a specific artefact, the type's access census, and
where the census exists the claim can simply be tested. **Nothing had tested it.**

The check was not worth writing when 20 types had a census. At **48** it is — and 13 of those are
`EMBED` children projected out of their parents, carrying displacements no scan had ever attributed
to the child before.

**188 unread spans in scope; 5 had a censused access; 4 were real.**

| span | what the census holds |
|---|---|
| `ItemClassDescriptor +0x00` | `cmp qword [r8], r11` · `mov eax, dword [r8]` |
| `ItemClassDescriptor +0x14` (at `+0x18`) | `cmp qword [r8+0x18], r11` · `mov eax, dword [r8+0x18]` |
| `ItemClassDescriptor +0x28` | `cmp qword [r8+0x28], r11` · `mov eax, dword [r8+0x28]` |
| `ImageAddressArenaRecord +0xA0` | `mov qword ptr [rax + 0xa0], rdx` |

**The first three are the rebase inputs** — the authored 32-bit offsets `0030B6A0` tests, loads as a
dword, and stores as a qword into the pointer slot beside each. They are read, not unread, and are
now `rebaseOffsetA/B/C`; the `+0x14` span split so its unaccessed first four bytes keep the unread
name. The fourth is `ImageAddressArenaRecord`'s last eight bytes, declared a tail with no access and
**written whole**.

**The fifth was left alone, and it is the reason this check issues no verdict.**
`CharacterRenderRecord +0x6E4` is credited with `lea eax, [rdx - 1]` at `+0x6E7` — arithmetic on a
register, not a memory access at all, filed at a displacement by a census that could not tell the
difference. **A hit is evidence to read, not a defect to fix**, and a projected census inherits
whatever its parent got wrong.

*Store after: 276 types, 2,963 fields, 0 errors, 0 gaps; census width check 0 disagreements over
1,957 rows in 48 types; unread spans with a censused access down from 5 to 1, and the survivor is
the artefact.*

### What the parent says is at the offset its child claims — `check_embed_parent_fields.py`

`check_storage_class.py` checks that an `EMBED` child FITS inside its parent and that two children
do not overlap. **Neither it nor anything else asked what the parent DECLARES at that offset.** The
child row and the parent row describe the same bytes, and nothing had compared them.

26 `EMBED` links checked. **25 exact, 1 an array element, 0 conflicts** — after one correction to
the instrument: it first reported `BattleTargetEntry` inside `BattleTargetBuffer` as a conflict,
because the parent declares `entries BattleTargetEntry[32]` at 512 bytes and the child is its
16-byte element at the same offset. Judged by size alone that reads as a child buried in an
unrelated field; the two rows are the same fact at two granularities and they agree.

### The one real finding removed 1,016 bytes of unknown from `BattleUnit`

`BattleUnit +0x200` declared `navigationPathState` as **152 bytes**. `NavigationPathState`, the type
it names and embeds at exactly that offset, is **0x490 (1,168)**. The remainder sat beside it as
`unobservedSpan0298`, 1,016 bytes of declared-unknown, and the arithmetic is exact:

    152 + 1016 = 1168 = 0x490      0x200 + 0x98 = 0x298      0x298 + 0x3F8 = 0x690 = 0x200 + 0x490

The child's own row had said so all along — *"INTERIOR BattleUnit +0x200 — containment checked,
`0x200 + 0x490 = 0x690` inside the unit's extent."*

**And the child is not a mystery: 1,168 bytes with 8 unread.** `currentNodeIndex`, `pathEndpoints`,
`predecessors u8[128]`, and `nodePositionXZ float[128][2]` — 1,024 bytes on its own. **The parent's
unknown span falls inside `nodePositionXZ`.** The two parent rows are now one field of the full child
extent.

| | before | after |
|---|--:|--:|
| `BattleUnit` declared bytes | 3,920 | 3,920 |
| of those, unread | **1,357 (34.6 %)** | **341 (8.7 %)** |

**No byte changed meaning and nothing new was discovered.** The description already existed one level
down, and the parent was carrying 1,016 bytes as unknown while the store could name every one of
them. That is the cheapest kind of gap there is, and the only reason it survived is that no
instrument compared a parent row with its child's type.

**Pass 2 generalises it and is now permanent**: a field whose `ctype` names a type must have that
type's size, or N times it for an array. **23 such rows, 23 agree, 0 disagree** — the `BattleUnit`
row was the only one, and it is fixed. A delta there is not automatically the field's fault; the
named type's own size can be the wrong one, so the check prints both and decides nothing.

### `CHAIN` and `RELOFF` are parent/child links too, and they are clean

The `EMBED` result asked the obvious next question: the other two linking verbs also name a parent
and an offset, and the parent's row there has to be the right **shape** for the verb.

    CHAIN  Parent +0xOFF   instance = *(parent + OFF)                 -> an 8-byte POINTER
    RELOFF Parent +0xOFF   instance = parent + *(int32*)(parent+OFF)  -> a 4-byte INTEGER

`check_storage_class.py` states it checks the `CHAIN` case, and reports nothing for these routes
either way, so they are now checked explicitly. **8 links, 8 correct, 0 wrong.**

| child | verb | parent row at the offset |
|---|---|---|
| `ActorWaitSlot`, `VmResultEntry` | `CHAIN ActorStorageRecord +0xA8` | `slotsA8 void*` — *"INTERIOR pointer into this same record"* |
| `ActorResourceEntry` | `CHAIN ActorStorageRecord +0xA0` | `slotsA0 void*` |
| `BattleStatsRecord` | `CHAIN BattleUnit +0x698` | `statsRecord BattleStatsRecord*` — **the parent even names the child type** |
| `ActorDefinitionCountedU16Section` | `RELOFF ActorDefinitionPayload +0x14` | `sectionCountedU16 int32` — *"a SELF-RELATIVE section offset"* |
| `AuthoredBlobFixupTable` | `RELOFF AuthoredTableHeader +0x14` | `countPrefixedSubstructRef uint32` — *"the registrar rebases it"* |

**A clean negative is a result here, not an absence of one.** A `CHAIN` meeting an integer would be
a different ABI rather than a typo — that is why the two verbs exist — and every one of the eight
meets the shape its verb requires, with the parent's prose independently describing the same
relationship the route encodes.

**The cross-type graph is now checked end to end: 26 `EMBED` links, 23 fields whose `ctype` names a
type, 8 `CHAIN`/`RELOFF` links. One defect found in 57 links**, and it was worth 1,016 bytes of
`BattleUnit`.

### `DYNAMIC` is free text, but where it names a type it still makes a checkable claim

The grammar calls `DYNAMIC` *"documented for humans, not consumable by a fixed-base generator"*, and
that is true of the base address. It is **not** true of the rest of the sentence: where the text
names a TYPE and an OFFSET, that is a claim about a declared field.

**Three of the eight are checkable, and all three hold:**

| route | the field it dereferences |
|---|---|
| `ActorStorageRecord`: `*(ActorManagerSlot +0x08)` | `recordPool void*` — *"pointer to the actor record pool this manager slot owns"* |
| `StatusDefinitionRecord`: `resolve(*(0x02EBF118)+0x0C)` | `AuthoredTableHeader +0x0C recordArrayRef uint32` — *"base-relative reference to the record array, resolved by 0020E600"* |
| `EquipmentDefinitionRecord`: `... * *(*(0x02EBF0F8)+0x08)` | `AuthoredTableHeader +0x08 recordStride uint16` — *"read at runtime rather than compiled in"* |

**That closes a loop with the registry contract.** `+0x08` and `+0x0C` are exactly the two offsets
`CONTRACT-authored-table-row-lookup.md` uses to define membership by idiom — *"one function reading
the stride at `+0x08` and the reference at `+0x0C`"* — the same pair that made `AuthoredTableHeader`'s
route wrong earlier on this page. Two unrelated authored-table types consume that header through
precisely those fields, which is independent support for the contract's reading.

**Four of the eight say `owner` without naming which type owns them.** `*(owner+0x40)`,
`*(owner+0x218)`, `*(owner+0x178)`, `*(*(owner+0x150)+8)` — unresolvable by any instrument, and by a
reader who has not opened the owning page. **Recorded as a documentation gap, not a defect**: the
information exists, it is simply not in the machine-readable column that was added so a census
generator could consume it.

### The cross-type graph, checked end to end

| pass | links | defects |
|---|--:|--:|
| `EMBED` child against the parent's field rows | 26 | 0 |
| field `ctype` names a type → size must match | 23 | 0 |
| `CHAIN` / `RELOFF` parent row must match the verb | 8 | 0 |
| `DYNAMIC` text naming a type and offset | 2 (+3 by hand) | 0 |

**59 links, one defect** — `BattleUnit +0x200`, worth 1,016 bytes — and four `DYNAMIC` routes whose
owner is unnamed.

### The four unnamed `owner` routes point at an owner the store does not contain

Following the four `DYNAMIC` routes that say `owner` without naming a type: **the reason they do not
name it is that it is not there.** `AudioParameterRamp`'s allocation row says so outright —
*"allocated and released with that owner, **whose type is not declared in this store**"* — and the
three `LegacyPs2Gs*` types share a single undeclared owner between them.

**The store already knows six of that owner's offsets**, scattered across three child rows that each
reach into it:

| offset | what the children require of it |
|---|---|
| `+0x150` | a pointer to the container whose `+8` holds the source-texture bank |
| `+0x174` | the reference-descriptor count |
| `+0x178` | the reference-descriptor array |
| `+0x218` | the derived-slot table |
| `+0x224` | the source-texture record count |
| `+0x228` | the admitted-slot count |

And `texture-mip-local-memory-budget.md` has a section headed **"Owning object"** that documents
`+0x218` and `+0x228` directly. **The document describes the type; the store has no row for it.**

**This is a parent missing under three declared children.** A reimplementation can build a
`LegacyPs2GsDerivedSlotRecord` from the store and still have nowhere to put it, because the thing
that holds the table is undeclared — which is the reconstruction-readiness question in its plainest
form, and it does not show up in any count of unknown *bytes* because the bytes belong to a type
nobody has declared.

**NOT DECLARED HERE.** A type row needs a size and a storage class, and six offsets from its children
give neither; inventing an extent to make the graph look closed is exactly what this page refuses to
do elsewhere. Registered as `OPUS-DECLARE-LEGACYPS2GS-OWNING-OBJECT` with the six offsets as the
starting field map.

### The route as a lossy summary of its own prose — three cases, and no instrument for them

Three rows today had a `route` that recorded less than the `instance` column beside it proved:

| type | the prose | the route said |
|---|---|---|
| `AuthoredTableHeader` | 40 of 146 slots are headers, membership by idiom | `count=40` — read as a table length |
| `AudioParameterRamp` | a `Category` owns **two** ramp arrays, `+0x38` and `+0x40` | only `+0x40` |
| `TextDrawState` | **four** instances: `+0xC0`, `+0xD0`, `+0xE0`, and a stack block | only `EMBED MessageWindowRecord +0xD0` |

The column exists so a consumer does not have to read the prose, and in each case a consumer that
trusted it would have been wrong — a generator scanning the wrong band, a reimplementation allocating
half the ramps, a reader seeing one embedding of three.

`TextDrawState`'s two unnamed owners cannot be written as `EMBED <Type> +0xOFF` because neither is a
declared type; they are identified by the function that handles them, which is what the prose does.
The grammar's own `DYNAMIC <free text>` covers exactly that, so the route gains three alternatives
and keeps the one a generator can consume. **Route alternatives across the store: 93 -> 97.**

### There is no mechanical test for this, and the attempt is worth recording

The obvious proxy is to compare the offsets a row's prose mentions against the alternatives its route
carries. **It does not work.** Applied to all 83 routed types it flags 9, and reading them, **none is
genuine**:

* `LegacyPs2GsDerivedSlotRecord` "array at owner+0x218, admitted-slot count at owner+0x228" — a base
  and a **count**, both already in the single route;
* `SteeringRecord` "2 slots at context +0x120 and +0x1A0" — both covered by `stride=0x80 count=2`;
* `GambitConfig` "+0x88 on party records (kind byte **+0x05** == 0)" — a **condition**, not a location.

`+0x` appears in this prose for counts, conditions, extents and internal fields at least as often as
for instance locations, and no regex separates those from a second embedding. **All three real cases
were found by reading the page the row points at** — `AuthoredTableHeader` from its contract,
`AudioParameterRamp` from `DQ-1`, `TextDrawState` from its own `instance` cell. Recorded so the next
person does not build the proxy and trust its nine.

### A fourth route form: an object that no instruction ever names — `gen_static_tree_census.py`

`RenderModelInstanceContainer` is `STATIC 0x022C7020`, and **no generator here could see a single
access to it**. Measured, not assumed: neither that address nor its cached pointer has one
rip-relative reference in any listed body, so `gen_static_census.py` (RIP operands),
`gen_ptr_census.py` (a `mov` of a slot) and `gen_array_census.py` (a `lea` of the object) are all
blind. The code never names the object:

    lea rsi, [rip -> 022C6F30]     the render resource ROOT
    lea rax, [rsi + 0xF0]          the container, 0x022C7020 -- COMPUTED, never named
    ...  [rax + disp]

So this tracks registers whose **absolute value** is known — seeded by a rip-relative `lea`, carried
through `lea rY,[rX+d]`, `add rX,imm` and `mov rY,rX`, dropped on any other write and on the
volatiles across a call. Nothing is inferred: every tracked value is an address the image states
literally, transformed by constants the instructions state literally.

**And the answer for this type is zero — with a positive control that makes the zero mean something.**

| aimed at | accesses | offsets |
|---|--:|--:|
| the **root** `022C6F30`, window `0x1000` | **121** | 32, all in `root+0xDF0 .. +0xEF0` |
| the **container** `root+0xF0 .. +0x160` | **0** | — |

The six rip-relative `lea`s of the root all feed a different region. **`RenderModelInstanceContainer`
has no statically-trackable access at all**: its 0x70 bytes are reached only through a pointer passed
as an argument, which is exactly how `0041E3A0` gets it — in `rcx`, from its caller.

**That is why the control matters.** Three zeros earlier in this work were instrument failures
(`SpawnGroupLedger`'s stride-24 `lea`, the load-only singleton seed, the first reader search). This
one is a property of the type, and the 121 accesses beside it are what distinguishes the two cases.
**A zero is only evidence when something non-zero comes from the same run.**

### What the tracker found instead at `022C7D20`, and the correction I owe it

The positive control above was aimed at `022C6F30` with a `0x1000` window, and its 121 accesses are
party formation, not rendering: `PartyFollow_SolveFormation` (`00338490`) with 98,
`PartyFollow_LookupDestination` with 1, and `FUN_00336AE0` / `FUN_0033CA00` with 11 each.

**I first wrote that up as "a table of 16-byte vectors at a `0x10` stride". That was wrong**, and it
is wrong by the rule this very page opens with. The eleven `0x10`-spaced reads are not eleven
fields — they are one **unrolled block copy**:

    00336B30  movups xmm0, [rax]          00336B38  movups [rcx],      xmm0
    00336B3B  movups xmm1, [rax + 0x10]   00336B3F  movups [rcx+0x10], xmm1
    00336B43  movups xmm0, [rax + 0x20]   00336B47  movups [rcx+0x20], xmm0
    00336B4B  movups xmm1, [rax + 0x30]   ...

**Load/store pairs alternating `xmm0` / `xmm1`** — the signature this kit documents precisely so that
*"a displacement in such a run is NOT a field"*. The run copies roughly `0xB0` bytes out of
`022C7D20`; it says nothing whatever about element boundaries inside them. And
`PartyFollow_SolveFormation`'s own loop steps `add rdi, 0x60`, so what iteration there exists walks
`0x60`-byte records, not `0x10`-byte ones.

**What survives the correction** is narrow and still worth having: `022C7D20` is an **undeclared
`.bss` region**, block-copied by two functions and read by the party formation solver. Its extent is
unknown, its internal structure is unknown, and a stride cannot be inferred from a copy.

**Its relationship to the render root is also not established.** The tracker reports offsets relative
to whatever base it is given, and being handed `022C6F30` does not make these bytes part of that
object — the root's prose places its subcontainer pointers at `+0xD90` and this region begins at
`+0xDF0`, past them. That framing was a property of my query, not a finding.

**NOT DECLARED**, and now for two reasons rather than one: a type row needs an extent and a storage
class, and the access pattern I would have built a stride from turns out to be a memcpy.

### A new type, and four declared fields confirmed by a consumer nobody had read

Following the `0x60` loop that the block-copy correction pointed at produced a declarable type.
`PartyFollow_SolveFormation` (`00338490`) states every quantity a type row needs, and **base, stride
and count are each confirmed twice**:

| quantity | evidence | corroboration |
|---|---|---|
| base + count | four `mov byte [rip -> X], 0xFF` at exactly `022C7E00 + i*0x60`, i = 0..3 | — |
| count | `inc esi` / `cmp esi, 4` / `jl` | matches the four sentinels |
| stride | `add rdi, 0x60` | `lea rdx,[rax+rax*2]` x3 then `shl rdx,5` x32 = x`0x60` |
| cursors | `lea rdi,[rip->022C7E20]` = elem+0x20 | `lea r13,[rip->022C7E10]` = elem+0x10 |

**`PartyFormationSlot`**, `ARRAY 0x022C7E00 stride=0x60 count=4`, `.bss`, declared to its full `0x60`
with the unmeasured bytes as unread spans: `+0x00` the unit's slot index (`0xFF` = empty),
`+0x10` `float[4]`, `+0x20` a float, `+0x28` a **`BattleUnit*`**.

### The same loop exercises four already-declared fields, and all four hold

| field | what the solver does | the row says |
|---|---|---|
| `BattleStatsRecord +0x3C` | `or edx, [rcx+0x3c]` after `mov edx,[rcx+0x64]` | *"presence is **+0x3C or +0x64**"* |
| `BattleStatsRecord +0x64` | the `mov` above, 4-byte | `statusWord1 uint32` |
| `BattleUnit +0x714` | `cmp word [rbx+0x714], r12w`, `r12d = 0x4021` | `actionId u16` |
| `BattleUnit +0xEA9` | `movzx eax, byte [rbx+0xEA9]` | `slotIndex uint8` |

**The first is the one worth having.** A row that says *"presence is `+0x3C` or `+0x64`"* is an
explicit claim about how two words are combined, and here is a consumer doing exactly that `or` —
written by different work, found by following an unrelated thread. The last one sharpened the new
type: `+0x00` is not an opaque byte, it carries `BattleUnit.slotIndex`.

`BattleUnit +0x698 statsRecord` is read by this same loop at `003385D3`, which independently
exercises the `CHAIN` link checked earlier on this page.

**How this was reached is the method, not luck.** The region was only opened because
`gen_static_tree_census` needed a positive control; the first reading of it was wrong and was caught
by this page's own unrolled-block-copy rule; and the element arithmetic only became legible because
the `lea [x+x*2]` multiply idiom had been added to a generator earlier, for a different type that
had come back with zero accesses.

### And the new type's two float fields name themselves, from the engine's own functions

`PartyFormationSlot`'s `+0x10` and `+0x20` were declared by width alone. The solver's own call
targets supply the rest, with no inference required:

    0033861F  lea r9, [rbp-0x48] / r8,[rbp-0x4c] / rdx,[rbp-0x50]
    0033862B  call 002646C0                     rcx = [rbx+0x10], the unit's transform
    00338630  movaps xmm0, [rbp-0x50]
    0033863F  movups [rdi-0x10], xmm0           -> slot +0x10

    0033865C  call 0033CB70                     Angle_NormalizeRadiansPi
    00338661  comiss xmm7, xmm0
    00338666  addss  xmm0, xmm9                 xmm9 = 6.283185 = 2*pi, from 01CEBC78
    0033866B  movss  [rdi], xmm0                -> slot +0x20

So **`+0x10` is a position vector** staged in the caller's frame and stored whole, and **`+0x20` is
an angle in radians** — normalised by a function the corpus already named
`Angle_NormalizeRadiansPi`, then conditionally advanced by one full turn so the four slots order
monotonically. The loop also skips the party leader: `cmp rbx, rax` against
`BattleUnit_GetPartyLeader` (`003272A0`).

**Four of the six declared fields now carry a meaning taken from a named engine function or a named
declared field**, not from a guess: the slot index comes from `BattleUnit.slotIndex`, the pointer is
a `BattleUnit*` proven by the register that also reads `+0x698`, the angle is named by the function
that normalises it, and 2*pi is read out of `.rdata`.

**NOT CLAIMED:** what the vector's four components are, or what `xmm7` holds at the compare. Those
need `002646C0` read and the caller's frame traced, and neither is done here.

### Both "NOT CLAIMED" items on the new type are now closed, by reading two more things

The published rows for `PartyFormationSlot` said explicitly that the vector's components and the
`xmm7` threshold were **not claimed**. Both fall out of two short reads.

**`002646C0` is a position getter, not a vector builder.** It takes three separate float pointers and
writes `x`, `y`, `z` from `[unit+0xB8] +0x00/+0x04/+0x08`, adding the offset triple at
`+0x40/+0x44/+0x48` when `byte [ctx+0x107]` bit 0 is set. It never touches a fourth component.

**The fourth component is `1.0`, and it arrives before the call.** `00338608` loads
`[rip -> 008C5FD0]`, which reads **`(0.0, 0.0, 0.0, 1.0)`**, and stores it to the stack slot; the
getter then overwrites `x`, `y` and `z`, and all 16 bytes are stored to the field. So `+0x10` is a
**homogeneous position** — the `w = 1` is a constant, not data.

**`xmm7` is zero.** `003384CA` does `xorps xmm7, xmm7` and nothing else writes it before the compare,
so `comiss xmm7, xmm0` tests **0.0 against the angle** and the `jbe` skips the add when the angle is
non-negative. The `+ 2*pi` therefore happens **only for a negative angle**: the field is an angle
**wrapped to `[0, 2*pi)`**, which is a complete statement rather than the "conditionally advanced"
the first pass could support.

*Both rows now carry that, and the `NOT CLAIMED` notes they replaced are gone because the claims are
made.* Five of the six declared fields are now evidenced to a named function, a named field, or a
constant read out of the image; only the tail spans remain unread.

### Reading the whole solver, not just its first loop: three more spans were not unread

The type was declared from the solver's opening loop. `PartyFollow_SolveFormation` is **4,101 bytes**
and that loop is its first third. Tracking absolute addresses across the whole body finds **109
accesses** into the `4 x 0x60` array, and four offsets fall inside spans the type had called unread:

| offset | access | elements |
|---|---|---|
| `+0x24` | 6 writes, `movss dword ptr [rcx], xmm2` | a second float beside the angle |
| `+0x30` | 16 reads, `movaps xmm5, [rcx + 0x30]` | **all four** |
| `+0x40` | 16 reads, `movaps xmm6, [rcx + 0x40]` | **all four** |
| `+0x50` | 16 reads, `movaps xmm7, [rcx + 0x50]` | **all four** |

**The 48-byte tail is three vec4s.** `movaps` requires 16-byte alignment, which a `0x60` stride from
a 16-aligned base provides and arbitrary padding would not — so the alignment is corroboration, not
just a width.

`PartyFormationSlot` now carries **eight evidenced fields and one unread span**, the 15 bytes at
`+0x01`, still declared to exactly `0x60` with no gaps.

**NOT CLAIMED:** what the three vectors hold, or what `xmm2` is at the `+0x24` write. They are
declared by **width and access** — the instruction that touches them and how many elements it
touches — which is what the evidence supports and no more.

*The lesson is the cheap one: the first pass read the loop that built the record and stopped. Four
fields were sitting in the same function, past the point where the interesting part appeared to end.*

### A second consumer re-derives the whole array, independently

`PartyFollow_LookupDestination` (`00339A60`, 390 bytes) touches the array once, and that one access
sits in a loop that confirms every structural claim made from the solver:

    00339A70  call 003272A0                 BattleUnit_GetPartyLeader
    00339A7E  cmp rax, rbx / je             the leader itself has no destination
    00339A87  mov rcx, [rax + 0x698]        the leader's statsRecord -- the CHAIN link again
    00339A9D  movzx edx, byte [rbx + 0xEA9] the unit's slotIndex
    00339AA4  lea rax, [rip -> 022C7E00]    the BASE
    00339AAD  lea r8,  [rip -> 022C7F80]    the END
    00339AB4  cmp byte ptr [rax], dl        match element +0x00 against the slot index
    00339ABA  add rax, 0x60                 the STRIDE
    00339AC7  movaps xmm0, [rip -> 008C5FD0]  the same (0,0,0,1) constant

**`022C7E00 + 4 * 0x60 = 022C7F80` exactly**, so the end pointer is a second, independent derivation
of `count = 4` — from a function that shares no code with the solver's prologue sentinels.

**And `+0x00` is not merely a copy of `BattleUnit.slotIndex`; it is the array's LOOKUP KEY.** This
function searches the four slots by comparing that byte against a unit's `+0xEA9`. The row now says
so.

| claim | from the solver | from the lookup |
|---|---|---|
| base `022C7E00` | four `0xFF` sentinel writes | `lea rax, [rip -> 022C7E00]` |
| count 4 | `cmp esi, 4` | end pointer `022C7F80` |
| stride `0x60` | `add rdi, 0x60` | `add rax, 0x60` |
| `+0x00` | written from `BattleUnit +0xEA9` | compared against `BattleUnit +0xEA9` |

**Four structural facts, each now established twice by independent code.** That is the strongest
footing any row in this store can have, and it came from following the one access a second function
made rather than stopping at the type that already validated.

### Types the corpus describes and the store does not declare — four found in one session

None of these was looked for. Each turned up while following something else, which is the reason to
record them together: **if four surface by accident in one session, the population is not four.**

| what | where it is | what the corpus already knows | what a type row still needs |
|---|---|---|---|
| the `LegacyPs2Gs` owning object | reached as `owner` by three declared types | six of its offsets (`+0x150`, `+0x174`, `+0x178`, `+0x218`, `+0x224`, `+0x228`); its own page has a section headed *"Owning object"* | an extent and a storage class |
| `Category` | `AudioParameterRamp`'s owner | named by `DQ-1` (FABLE, 2026-09-14) with `Category::InitializeRefCategory` at `01CB44B0`; owns **two** ramp arrays at `+0x38`/`+0x40` | everything else |
| `TextDrawState`'s two owner records | `+0xC0` of the record `00227EE0` handles, `+0xE0` of the confirm-window record `0057C480` | the offsets and the handling functions | names, extents |
| the **64-byte activation record** | `0208D480` (party, keyed by stats `+0x04`) and `0208DE80` (keyed by unit `+0xEA9`), stride `0x40` | `BattleRuntime_ResetPersistentStatePrefix` (`00386C10`) zeroes its first 32 bytes; resolver masks at `+0x04`/`+0x08`, attack word at `+0x10`, combo nibble at `+0x12`; discriminated by `kindByte` | the element **count** of either table |

**The last one is the instructive case.** Its page describes the record, its two bases, its stride,
four of its fields and the function that clears it — and the store has no row, so nothing checks it,
no census can be mapped to it, and `check_embed_parent_fields` cannot see the link between it and
the `kindByte` that selects which table to use. **A type documented in prose is not a type the
instruments can reach.**

**This is a gap byte-level metrics cannot show.** Every count of unknown *bytes* in this store is a
count over declared types; bytes belonging to a type nobody declared are in no numerator and no
denominator. The four above are invisible to `engine_explained`, to the census coverage table, and
to the unknown-field figures — and three of them were found only because a route said `owner` and I
asked what `owner` was.

**NOT DECLARED, in all four cases, and for the same reason each time:** a row needs an extent and a
storage class, and prose that names offsets supplies neither. Registered as
`OPUS-DECLARE-LEGACYPS2GS-OWNING-OBJECT`; the other three are named here so the next pass starts
with a list rather than a discovery.

### The 64-byte activation record: still not declared, and why — adjacency is not a measurement

It needs only an element count, and the count did not come.

**What is established.** Both tables are referenced by the same function family — `0208DE80` by 16
sites and `0208D480` by at least 9, among them `BattleRuntime_GetEffectiveActionId`,
`BattleRuntime_ResolveAndCacheEffectiveActionId`, `BattleRuntime_MarkTargetHistoryBit`,
`BattleFormula_RollAndStoreComboCount` and `BattleRuntime_ResetPersistentStatePrefix`. Every one
takes the table's address with a `lea` and indexes it; **none of them walks it with a loop**, so no
site states a bound.

**What is only inferred, and is recorded as inference.** The gap between the two bases is
`0208DE80 - 0208D480 = 0xA00 = 40 x 0x40`, and `0208DE80 + 32 x 0x40 = 0208E680`, eight bytes below
the `BattleUnit` pool pointer at `0208E688`. That would make the tables 40 and 32 elements. **It is
adjacency, not a measurement** — nothing says the first table fills the gap, and a table can be
followed by padding or by an unrelated global. 32 is a recurring unit count in this subsystem
(`BattleTargetResultEntry` is `count=32`), which makes the second figure plausible and still not
evidence.

**So the row is not written.** Every other type declared today had its count stated twice by
instructions; this one has it stated zero times, and a count guessed from spacing would be the one
part of the row a reimplementation cannot check.

*A correction to this section, made before anyone read it: I first wrote that a capstone scan reported **zero** references to `0208D480` while a raw byte scan found nine, and flagged it as an unexplained tooling divergence. **There was no divergence.** The two tables are reported in dict insertion order, `0208D480` first, and I had piped that run through `tail -20` -- which cut its entire block. Re-run untruncated, the capstone scan reports **16 references to each table**, and the byte scan's nine are its `lea r64` subset. Both instruments were right and the reading was mine. It is left here rather than deleted because a caution against a working tool is worse than no caution, and the way it happened -- a shell pipeline quietly discarding the first half of an answer -- will happen again.*

### One of the four is now declared: `LegacyPs2GsTextureContext`

The catalogue above listed it as needing *"an extent and a storage class"*. The allocation chain
supplies both, and every step is an instruction rather than an inference:

    0026E792  mov edx, 0x240      <- THE SIZE
    0026E797  mov ecx, 6             the pool tag
    0026E79E  call 003EC8D0          the allocator: forwards edx to 0036A190, error-handles null
    0026E7B1  call 002F6AB0          the initialiser
    0026E7B9  call 0026E960          which publishes it -- `mov [rip -> 0209A670], rcx` at 0026E966

and `FUN_0026E290` reads it back from that global at `0026E29A` before handing it to `002F7380`,
the function the Legacy-PS2-GS page names as rebuilding the object's `+0x218` / `+0x228`.

**`0x240` = 576 bytes, and the six offsets its three declared children require top out at `+0x22C`.**
They fit — a check the size had to pass and did.

Declared as `PTR 0x0209A670`, `HEAP`, with **seven evidenced fields** and the remaining extent as
unread spans, so it validates with no gaps: `+0x120` a gate dword, `+0x150` the source-texture
container, `+0x174`/`+0x178` the reference-descriptor count and array, `+0x218` the derived-slot
table, `+0x224`/`+0x228` the two counts. **Three previously parentless child types now have a parent
in the store.**

**NOT CLAIMED: a destructor.** `0026E20C` resets the global to null with `xor eax,eax`, which is a
clear and not a release; no deallocation of the `0x240` block was found.

**NOT DONE, deliberately: rewriting the three children's routes to name it.** Those rows say `owner`
and somebody may be mid-way through them; the parent is declared and the correspondence is stated in
its own row, which is the smaller change.

*Method note: an attempt to find the owner by looking for functions touching 3+ of its six
signature offsets returned **75 candidates** — those displacements are common to many unrelated
objects, and offset co-occurrence is not type identity. The chain above came from following the one
function the page named, which is the same lesson the `+0xEE` population taught earlier on this page.*

## Do two routes claim the same bytes? (2026-09-19, OPUS)

`check_route_counts.py` asks whether a `count=` agrees with its own document, and
`check_route_extents.py` asks whether the data stops where the count says. Both consult something
outside the store. Neither asks the question the store can answer alone: **a base, a stride and a
count describe a span of bytes, and two types must not describe the same ones.**

`check_route_collisions.py` does that, and it reads no image — only what the store already asserts.
A finding is therefore a defect by construction, not a reading that might be wrong.

**Result over the 18 routes with a direct base/stride/count: zero partial overlaps.** The one
identical pair is `ItemClassDescriptor` and `InventoryClassDescriptor`, both
`ARRAY 0x01EEBCC0 stride=0x58 count=15` — the already-queued
`OPUS-CON-ITEMCLASS-INVENTORYCLASS-SAME-TABLE`, reported separately so it cannot mask a new one.

### Why the first run of it was wrong, and why that matters

The first version counted `PARRAY` routes as occupying a fixed span and reported two overlaps:
`CharacterRenderRecord` at `022C6F28` appearing to swallow 0x48800 bytes and run through both
`PartyFormationSlot` and `ImageAddressArenaRecord`. Both were artefacts. The grammar at the top of
this file says

    PARRAY  0xADDR [+0xOFF] stride=0xS [count]   element i at *(ADDR) + OFF + i*S

so a `PARRAY` names a **pointer** at `ADDR`; the elements live wherever it leads and the route
claims no fixed span. Only `ARRAY` and `SLOTPTR` are direct, and the checker now says so in a
comment at the regex, because the exclusion is the whole correctness argument.

That failure is also what makes the clean result worth anything. **A check that reported zero on
its first run would tell us nothing about whether it can detect a collision at all**; this one
produced two findings from a wrong premise and none from the right one, so the zero is a measurement
rather than a silence.

## The census trackers dropped the object at the null check (2026-09-19, OPUS)

Every forward register tracker in the kit decided that a register had been overwritten with this
rule:

```
# any write to a held register drops it
if ins.operands and ins.operands[0].type == X86_OP_REG:
    drop(ins.reg_name(ins.operands[0].reg))
```

**The first operand of an x86 instruction is not necessarily written.** `test rbx, rbx`,
`cmp rbx, rax` and `push rbx` all read it and write only flags — capstone's own `regs_access()`
returns `['rflags']` for `test rbx, rbx` and nothing else.

The idiom this breaks on is the commonest one in the image:

```
mov  rbx, qword ptr [rip -> singleton]
test rbx, rbx                              <- tracking stopped HERE
je   bail
cmp  dword ptr [rbx + 0x120], 0            <- never recorded
```

A singleton is loaded and immediately null-checked, so on that path the tracker discarded the object
at the exact instruction *after which every access occurs*, and it did so silently. How much this
cost varies enormously by type and is measured below — it is not a uniform undercount.

`reg_tracking.py` now answers the question properly — `written(ins)` from `regs_access()`, with
sub-registers normalised to their 64-bit parent because `mov eax, 1` zeroes the upper half and
`mov al, 1` destroys the pointer just as thoroughly. `gen_ptr_census.py` and
`gen_ptr_census_depth1.py` both use it.

### The same shortcut mislabelled the output

`kind = "w" if oi == 0 else "r"` called `cmp dword ptr [rbx+0x120], 0` a **write**, because the
memory operand comes first. A consumer trusting that label concludes the engine stores to a field it
only tests. `RT.op_kind()` reads capstone's per-operand access flags instead; on the one type
re-censused so far this moved 5 rows from `w` to `r`.

### What it was worth, measured — and it is not a landslide

Both rules were run over all eleven `PTR`-route types. **926 distinct accesses under the old rule,
995 under the corrected one: +69, a factor of 1.07.** The effect is concentrated, not general:

| type | old acc/offsets | new acc/offsets |
|---|---|---|
| `LegacyPs2GsTextureContext` | 6 / 4 | 16 / 10 |
| `ManagerSingleton0209BE80` | 202 / 42 | 258 / 51 |
| `BattleSystemState` | 329 / 39 | 333 / 41 |
| `CharacterRenderSystemTail` | 141 / 24 | 143 / 24 |
| `GameSettingConfig` | 153 / 33 | **150** / 33 |
| the other six | unchanged | unchanged |

So the honest summary is that two types were materially undercounted and most were not. The earlier
framing here — that the trackers were broadly returning numbers too small to mean anything — was
wider than the measurement supports.

### One count went DOWN, which a "drops less often" rule should not permit

`GameSettingConfig` lost three rows, and the three do not have one explanation.

**One is a false access the old rule should never have recorded.** At `00798584` it reports
`mov eax, dword ptr [rax + 4]` off a singleton in `rax` — but `0079843B mul rcx` had already
overwritten `rax`. `mul` writes `rax` and `rdx` *implicitly*, naming neither as operand zero, so the
old rule could not see the clobber. Removing that row is the fix working.

**Two are real accesses the corrected rule now misses**, and that is a limitation worth stating
plainly:

```
mov rax, qword ptr [rip -> slot]     rax = the singleton
cmp dword ptr [rax + 8], 0
jne  0079C18B                        <- the taken path SKIPS the next instruction
mov  eax, dword ptr [rax + 0x2c]     writes rax, on the fall-through only
0079C18B:
mov  eax, dword ptr [rax + 4]        <- a genuine access at +0x4
```

Correct write-tracking kills `rax` at `+0x2C`, so the scan stops before `+0x4`. On the path that
actually reaches `0079C18B` that write never happened. **The scanners are a linear sweep with no
control flow**, and normalising `eax` to `rax` — which is right in isolation — makes that
approximation bite where the old rule's sloppiness accidentally papered over it.

Neither rule is sound on branching code. The corrected one is right per instruction; both are
floors, and a per-offset absence is still not proof.

## Following a singleton into its callees — `gen_ptr_census_depth1.py`

Every generator here carries the same caveat in its docstring: *same-function only*, *a root passed
as an argument is invisible*. For a singleton that is handed to a worker, that caveat is the whole
result. `0026E290` loads `0209A670`, guards it, and calls `002F7380` with the object in `rcx`; all
the interesting accesses are in the callee.

Pass 2 records, in the same walk, when a tracked register is moved into an argument register and a
**direct** call follows, then re-scans that callee with the matching parameter register seeded.
One level only — a depth-2 walk would need the argument to survive a second frame and nothing here
establishes that. Counts remain floors.

**It also acted as a control on a declaration.** `LegacyPs2GsTextureContext` was declared from its
allocation chain, and six of its seven fields came from the three child types' `owner+0xNNN` routes
on the inference that the pages' `owner` is the `0209A670` singleton. That inference was recorded as
an inference. The depth-1 census independently finds `+0x120`, `+0x150`, `+0x174`, `+0x178`,
`+0x218`, `+0x224` and `+0x228` — **all seven** — inside `002F7380` and its callers. The inference
is now corroborated by instructions.

Eight further offsets fell inside declared gap spans and are now declared by width and access:
`+0x114`, `+0x130`, `+0x138`, `+0x188`, `+0x1A0`, `+0x1C0`, `+0x1D8`, `+0x22C`. One carries more
than a width — `+0x130` is loaded, null-tested and **called** with the context in `rcx` and a
caller dword in `edx`, which is a signature read off the call site. The other bytes remain spans;
nothing was consumed to make the layout look finished.

## The largest gap in the store, measured four ways (2026-09-19, OPUS)

`ManagerSingleton0209BE80` is the biggest type in the store at `0x10FD0`, and one row accounts for
**23,224 of its 25,682 unexplained bytes**: `unobservedSpanB244`. That single span is roughly 40% of
all unexplained bytes in the entire field store, so it is worth knowing whether it is unexplained or
merely unexamined.

**The extent is not in doubt.** `0028F8CA mov ecx, 0x10FD0` then the tagged allocator at
`0028F8CF` — the object really is 69,584 bytes.

Four instruments, in increasing reach:

| instrument | accesses inside the span |
|---|---|
| `gen_ptr_census.py`, load-seeded, old tracker | 0 |
| corrected tracker + store seeding (258 accesses / 51 offsets elsewhere in the object) | 0 |
| one level into callees the singleton is passed to (+18 accesses, 3 new offsets) | 0 |
| indexed operands `[base + index*scale + disp]`, normally discarded | **0 indexed accesses anywhere in the type** |

The constructor `00291750` hands out five interior sub-objects — `lea rcx, [rdi + 0x5380]`,
`+0x7EA0`, `+0x8FA0` twice, `+0x57E0` — and **every one is below the span**. 103 functions
contribute accesses to this object and none of them reaches past `0xB244` until `0x10CFC`.

### An instrument that could not answer it, and why the answer it gave is discarded

A whole-image sweep for any instruction carrying a displacement in `0xB244..0x10CFC` looked
decisive and was not. Its first run reported **zero** — and its controls reported zero too, for
ranges with hundreds of known accesses, because `md.disasm(blob, tva)` halts at the first
undecodable byte: it decoded 4,186 instructions, ending at `00124BFC`, **0.19% of `.text`**. Rerun
with resynchronisation it decodes 2,109,974 instructions and the controls come back 277, 778 and 7.

It then reports **283** instructions with a displacement in the range — and that number settles
nothing, because the sweep cannot tell which object a base register holds. `001D59AD
mov qword ptr [rcx + 0xf738], 0x3f800000` is some other object's field. Only a decisive zero would
have been informative, and it is not zero. **The sweep is recorded as uninformative rather than
as evidence**; the finding rests on the base-aware scans alone.

### What is and is not established

**Established:** no body that holds the `0209BE80` pointer addresses `0xB244..0x10CFC`, by constant
displacement or by index, at the call depth the scans reach.

**One of the alternatives is now CONFIRMED, and it is the bulk one.** The constructor opens with

```
0029175A  xor  edx, edx
0029175C  mov  r8d, 0x10fd0
00291765  call 00861EC0          ; named `memset` in the function list; rcx = the object
```

so all 69,584 bytes — the span included — are zeroed at construction. The region is *initialised*,
by a single wholesale call, and never touched field-by-field afterwards by anything reachable.
That explains the bytes being written without explaining what any of them are, and no field is
declared on the strength of it.

**Credit where it is due: this was not found here first.** The save-payload field map reached the
same conclusion the same day for its own three spans and states the general rule outright — *"a
span with no accessor should be swept for bulk writes before it is described, because the two
questions have different instruments and only one of them had been run"* — and it already cites
this manager's 23,224-byte hole as one of its three examples. The derivation above is an
independent re-derivation, not a discovery, and the rule belongs to that page. What the type store
adds is the propagation: the three `SavePayload` span rows carried no bulk-write evidence at all
until 2026-09-19, and now do.

**Still not excluded:** an interior pointer computed once and stored elsewhere, then re-read; a
chain two or more calls deep; and code in the ~1,308 unlisted blocks, which every scan here skips
because it iterates the function list.

The row stays a declared span. Its evidence is stronger than it was — four instruments rather than
one — and it is still an absence, which is not the same as knowing what the bytes are.

## The two standing alignment reports, adjudicated (2026-09-19, OPUS)

`check_alignment.py` has reported the same two rows for some time: a type whose size is not a
multiple of its strictest member alignment. Its own docstring says it "does not assume every type
is a compiled struct", so these are reports awaiting a judgement rather than defects. Here is the
judgement, so they stop being re-derived.

**`FieldRecord`, size `0x3`, strictest member alignment 2 — NOT a defect.** The type is an element
of `PARRAY 0x02ADD100+0x8 stride=0x3`, and its own evidence records the addressing:
`lea rax, [r8 + rcx*2]` followed by byte accesses at `[rcx + rax + 8]`, `+9` and `+0xA`. Stride 3
means every odd element starts at an odd address, so the `uint16` at `+0x00` is **not 2-aligned on
half the elements** and the engine reads it anyway. This is a packed 3-byte record, its real
alignment is 1, and a size that is not a multiple of 2 is exactly what a packed array of 3-byte
records looks like. The `uint16` row describes the width of the read, not an alignment guarantee.

**`EvaluationContext`, size `0x2A`, strictest member alignment 8 — NOT a defect.** Its storage class
is `CALLER`: it is built on the caller's stack by `BattleFormula_BuildEvaluationContext`
(`003847C0`) and passed by pointer. The `0x2A` is not a `sizeof` — the type row says outright that
it came from reading the builder **to its `ret`**, so it is the observed extent of the writes. A
stack temporary has no tail padding to observe, and the last field `sourceLayerMask` is
`u8[16]` at `+0x1A`, ending exactly at `0x2A`. A compiled `struct` with the same members would be
padded to `0x30`; the store records what the builder writes, which is the honest number and the one
a reconstruction needs to reproduce the frame.

**Neither is changed.** Recording a padded `0x30` for `EvaluationContext` would assert tail bytes
nobody observed, and re-typing `FieldRecord`'s `uint16` would lose the width of the read. The
checker is right to surface both and right not to fail on them.

## A census for `EMBED`, and what it actually returned (2026-09-19, OPUS)

`gen_embed_census_depth1.py` covers the shape no generator did: a sub-object that the parent's
constructor computes once and hands away.

```
002917AA  lea rcx, [rdi + 0x8fa0]     rdi = the singleton, rcx = the sub-object
002917B1  call <initialiser>
```

Two things were needed to see that at all. The parent must be seeded **from the parameter** of the
functions it is passed to, because `00291750` receives the singleton as an argument rather than
loading the slot — without that the `lea` is invisible and the tool found 0 callee pairs for
`_8FA0`. And the `EMBED` chain must be **composed**, not read one level deep: `ManagerSub00A0Entry`
is `+0x20` inside a parent that is `+0xA0` inside the singleton, so the element is at `+0xC0`.

### The result is one offset

| | |
|---|---|
| EMBED types in the store | 26 |
| reachable, one-level resolver | 7 |
| reachable, chain composed | **10** |
| new offsets found across all 10 | **1** |

The one is `+0x24B0` in `ManagerSub0209BE80_57E0` — `lea rdx, [rdi + 0x24b0]` at `003FA5C9` —
declared under the store's existing `subAddr` convention. Everything else the census returned was
already declared. `_5380` returns **0 accesses against a type that already has declared fields**,
and the two array-element types the chain walk newly reached return 0 and 1. **For this family the
instrument is weaker than whatever produced the existing rows**, and it is recorded that way.

### The scope was measured before it was widened, and then not widened again

The 16 `EMBED` types with `ARRAY`/`PARRAY`/`CHAIN`/`DYNAMIC` parents are **deliberately not
handled**. They hold 118 unexplained bytes between them and are already 0–5% unexplained —
`BattleStatsRecord` 3%, `NavigationPathState` 1%, `BattleTargetBuffer` and `TextDrawState` 0%. The
three the chain walk added hold 518 of the 636 bytes at stake, which is why that extension was
worth writing and a further one is not.

**What this says about the remaining mass.** `ManagerSub00A0Entry`, `_7EA0Entry` and `_7FB0Record`
are 94%, 94% and 91% unexplained and are *not* reached from the singleton base at one call level.
Their fields are touched through their own pointers deeper in the call chain. More parent-side
reach will not find them; a depth-2 walk or seeding on their own accessors would be the next
instrument, and neither is built.

*For `ManagerSub00A0Entry` the instrument that answered was neither: re-tiled 2026-09-27 (OPUS) from the entry's own initialiser `003F9390`, its reset `003F00F0` and the list append `003F1290`, which reach it through the parent + 0x20 + (i << 8) pointer they form themselves. That also showed the 2026-09-18 rows `ptr0000` / `ptr0010` were the list HEAD's fields, not the entry's (`_index/candidates/manager-a0-entry-layout/`).*

## The store against the prose it points at — `check_span_propagation.py` (2026-09-19, OPUS)

Every other checker here compares the store to the image, or to itself. None compared it to **the
documents the store itself nominates**, and that turned out to be where the misses were.

`SavePayload`'s three largest spans — 11,940 bytes — said only *"extent-declared gap … width =
declared span, not an instruction access."* Their own `documents` page had a whole section proving
all three sit inside a `0x56690` `memset`, giving them a defined value and a lifetime. The finding
existed. It had simply never crossed into the store.

The checker takes each declared span, reads the owning type's `documents` pages, searches them for
the span's offset in the several spellings this corpus uses, and reports a hit only when the row's
own evidence does not already cite that page. **It is a candidate list, not a defect list** — an
offset is a short string and prose is long, so offsets under three hex digits are skipped as
unsearchable and every hit needs a human to open the page.

**First run: 18 candidates over 1,560 bytes, from 341 declared spans across 70 types.**

### What the candidates turned out to be

**`CharacterRenderObject` — 632 + 144 + 96 + 16 + 4 + 2 bytes, and the opposite of `SavePayload`.**
Its page argues by exhaustion that the object is *never cleared*: allocated at `001BD527`
`mov ecx, 0x668` through `00210EC0`, which is three instructions — `or r8d,-1` / `xor edx,edx` /
`jmp 0085E730`, a tail jump to Bullet's `malloc`, **not** a `calloc`; the base constructor installs
only a vtable; the real constructor initialises field by field with no `memset` of `this`. All
three checks re-verified here, plus the fourth: a sweep of every listed body finds **zero**
`mov r8d, 0x668` sites, so no `memset` of this object's length exists anywhere in the image.

So these bytes are **undefined, not zero** — and for a reconstruction that is a *licence*: any
content matches, including zero. What is unsafe is *assuming* zero, which is correct for ~93% of
this store's unknown bytes and false here. The page names three spans; the argument is object-wide,
so it was propagated to all six with the extension flagged on the three the page does not name.

**`MessageWindowRecord` — three spans had real writers.** `002A2C00` is a source-descriptor copy
run, and `rbx` is a record of this type *by the store's own evidence*, not by assumption: the same
run writes `+0x1A8` at `002A2CE5`, which this type already declares as `openArgPtr1A8`. Four fields
recovered from it — `+0x1B0` (`mov qword ptr [rbx+0x1b0], rax`), `+0x3B9`, `+0x3BA` (also later set
to the literal 5) and `+0x3BC`.

After propagation the sweep reports **15 candidates over 816 bytes**, and the closed rows drop out
of it, which is the check on the checker.

### The checker under-reports, and `BattleUnit` is the proof

`check_span_propagation.py` matches on an **offset**. An object-wide fact has no offset, so the
checker cannot see it.

`BattleUnit` flagged exactly two spans — `+0x120` and `+0xEB4` — because those are the two its page
happens to name in a sentence. Reading that page found something neither the checker nor the store
had: **the whole `0xF50` unit is zeroed on both sides of the pool lifecycle.**

```
BattleUnit_AllocateSlotAndBindActor  00234480
    002344A5  test byte ptr [rbx], 1      ; find a free slot, stride 0xF50
    002344C7  xor  edx, edx
    002344C9  mov  r8d, 0xf50
    002344D2  call 00861EC0               ; memset(unit, 0, 0xF50)
    002344D7  or   dword ptr [rbx], 1     ; then claim it

ActorSystem_ReleaseBattleUnitSlotForActor  00234200
    002342C3  xor  edx, edx
    002342C5  mov  r8d, 0xf50
    002342CE  call 00861EC0               ; and again on release
```

A sweep of every listed body finds **exactly those two** `mov r8d, 0xf50` sites. That is stronger
than the `0x610` partial reset at `00236B28` the page invokes for `+0x298`, which covers only
`+0x80`–`+0x690`: the full clear covers **all thirty** of this type's declared spans, including the
`+0xEB4` tail that sits outside the partial one. All thirty now carry it; the checker had flagged
two.

**The lesson for the instrument:** an offset-keyed search finds offset-keyed prose. Lifetime facts
are usually stated about the *object*, so a span's silence in this checker is not evidence its page
has nothing to say. The 142 spans it skips for having offsets under three hex digits are a second,
separate blind spot. Both are recorded rather than fixed, because the fix is a different matching
rule and this run's value was in the eleven rows it did surface.

## `check_bulk_write_lifetime.py` — asking the question the way the evidence is shaped (2026-09-19, OPUS)

The span-propagation checker matches on an offset, and the `BattleUnit` result showed why that is
the wrong shape: the fact that mattered — *the whole object is cleared* — mentions no offset and
covers every span at once. A lifetime is a property of the **type**, so the instrument now is too.

It finds every `memset`/`memcpy` call in a listed body, recovers the length when it is a literal
`mov r8d, imm`, and matches that against each type's declared size. Then it splits the result in
two, because **a size match is not an attribution**:

* **ATTRIBUTED** — `rcx` traces, in the same body, to the type's own route root.
* **SIZE MATCH ONLY** — the length equals the extent but the destination could not be tied to it.
  Sizes collide; `0x100` alone matches 74 call sites.

### Its first run returned zero, and the control caught it

474 is the real figure. The first run said **0 bulk-write calls in the whole image**, which was
impossible — the `BattleUnit` pair and the `ManagerSingleton` clear were already known to exist,
and knowing that *before* running the tool is what made the zero legible as a bug rather than a
finding. The cause was mine: the clobber loop uses `RT.written()`, which correctly reports that
`mov r8d, 0xf50` **writes r8**, so the literal was erased on the very instruction that set it.
Every seeding branch now `continue`s past the clobber.

### What it found

**474 calls, 139 distinct lengths, 29 types whose declared size matches one.** It independently
rediscovers both known-true positives — `002342CE`/`002344D2` for `BattleUnit` and `00291765` for
`ManagerSingleton0209BE80` — which is the control on the working version.

**One hit was fully attributed and is new:** `ImageBackedStateBlock`, `0x4818`.

```
00253A98  mov  rcx, qword ptr [rip -> 020927C0]   ; the type's OWN PTR route root
00253A9F  xor  edx, edx
00253AA1  mov  r8d, 0x4818                        ; its exact declared size
00253AA7  call 00861EC0                           ; memset
```

in `SaveRuntime_InitializeHeaderAndImageBackedState`. All six of its span rows — 275 bytes —
carried no lifetime note; all six now do. Re-running the checker reports *"all spans already carry
it"*, which is the self-check.

### The honest limit: attribution, not detection

Only **1 of 29** size matches attributed. `rcx` usually arrives as a **parameter**, and this tool
roots registers only from rip-relative loads and `lea`s in the same body — the same boundary that
made `gen_embed_census_depth1.py` need parameter seeding. So the other 28 are candidates, not
findings, and `BattleUnit` itself shows as *"size match only"* even though its clears were
confirmed by hand an hour earlier. **The tool is weaker than the manual check it was built to
generalise.** It narrows 139 lengths to 29 types worth reading; it does not settle them.

### Parameter seeding, and what the lifetime question now answers

The checker's first working run attributed **1 of 29** size matches, because it rooted registers
only from rip-relative loads in the same body — and `rcx` at a `memset` is usually a **parameter**.
That is the same boundary that made `gen_embed_census_depth1.py` useless until it seeded the parent
from the argument, so the same fix applies: record every call that receives a route-rooted object
in an argument slot (**21,428 handoffs**), then re-scan each receiving callee with that parameter
pre-rooted.

Attributed hits went **1 → 3**, and the two additions are the ones that mattered:

| type | site | what it clears | spans propagated |
|---|---|---|---|
| `ManagerSingleton0209BE80` | `00291765`, root `0209BE80` | `0x10FD0`, the whole singleton | **19** |
| `CharacterRenderRecord` | `0041F754`, root `022C6F28` | `0x740`, via `CharacterRenderRecord_ResetDefaults` memsetting its own `rcx` | **42** |

`ManagerSingleton` is the one that counts: its `0xB244` span alone is 23,224 bytes, and the
attribution is now mechanical rather than a hand-read.

**Where the store stands on lifetime**, over 340 declared span rows totalling 55,653 bytes:

* **106 rows / 38,921 bytes (70%) carry a lifetime verdict.**
* 234 rows / 16,732 bytes still carry none.
* The verdicts are not all the same, which is the point: 26,087 bytes are **guaranteed zero** and
  894 bytes are **genuinely undefined** (`CharacterRenderObject`, never cleared). A reconstruction
  that assumed one rule for both would be wrong in one direction or the other.

**`BattleUnit` still reports "size match only"** even though its two clears were verified by hand
earlier — its `rcx` comes from a pool walk with bounds checks, not from a route root, so the tool
cannot tie it. The manual result stands and the tool's silence on it is a known false negative,
recorded here rather than papered over.

### The whole `ManagerSub*` family, settled by containment rather than by eleven more reads

The three largest unattributed size matches were `ManagerSub0209BE80_5380`, `PersistentFlagPayload`
and `ManagerSub0209BE80_57E0ArrayRecord`, and the first and third are the same case as eight
others: **they are interior to `ManagerSingleton0209BE80`**, whose whole `0x10FD0` extent is
memset at construction — a clear now attributed mechanically to the singleton's own `PTR` root.

Eleven types resolve into that object, and the containment is arithmetic rather than assumption:

| type | interior at | ends | inside `0x10FD0` |
|---|---|---|---|
| `ManagerSub0209BE80_00A0` | `+0xA0` | `0x5380` | yes |
| `ManagerSub00A0Entry` | `+0xC0` | `0x40C0` | yes |
| `ManagerSub0209BE80_5380` | `+0x5380` | `0x57E0` | yes |
| `ManagerSub0209BE80_57E0` | `+0x57E0` | `0x7EA0` | yes |
| `ManagerSub0209BE80_57E0ArrayRecord` | `+0x5A50` | `0x7C70` | yes |
| `ManagerSub0209BE80_7EA0` / `ManagerSub7EA0Entry` | `+0x7EA0` / `+0x7ED0` | `0x7FB0` / `0x7F10` | yes |
| `ManagerSub0209BE80_7FB0` / `ManagerSub7FB0Record` | `+0x7FB0` | `0x8FA0` / `0x8610` | yes |
| `ManagerSub0209BE80_8FA0` | `+0x8FA0` | `0xA0D0` | yes |
| `ManagerSub0209BE80_A0D0` | `+0xA0D0` | `0xAA60` | yes |

48 span rows propagated in one step. The guarantee is stated precisely: zero **from the
singleton's construction**, with each sub-object's own initialiser running *after* that clear.

### Where the lifetime question now stands, store-wide

Over **340 declared span rows, 55,653 bytes**:

| verdict | bytes | rows | share |
|---|---|---|---|
| zero-initialised | 50,744 | 148 | **91.2%** |
| genuinely undefined | 894 | 6 | 1.6% |
| no verdict yet | 4,015 | 186 | 7.2% |

**A near-miss worth stating rather than rounding away.** The `CharacterRenderObject` page reached
*"93% of this database's declared-unknown bytes are zero-initialised"* with a residue of *"at most
3,862 bytes"* by its own separate route. This store-side count gives 91.2% and a
not-known-zero residue of 4,909 bytes. The two agree in substance and differ at the margin, which
is what independent counts over slightly different populations and dates should do — quoting them
as the same number would be tidier and wrong.

The remaining 4,015 bytes are now small enough to name individually: `PersistentFlagPayload
+0xCF6` (778), `MessageWindowRecord +0x1B8` (512), `SaveImageHeader +0xC0` (320),
`LegacyPs2GsTextureContext +0x0` (276) and 182 rows under 200 bytes each.

### Three seeding modes, and what each one was worth

The bulk-write checker attributes a clear to a type only when the destination register traces to
that type's own route. It learned to do that three times, and each addition was forced by a
concrete miss rather than designed in advance:

| mode | the miss that forced it | attributed |
|---|---|---|
| rip-relative load/store of a slot, `lea` of a base | — (the starting point) | 1 of 29 |
| **parameter seeding** — record which callee receives a route-rooted object in which argument slot, then re-scan it with that parameter pre-rooted | `rcx` at a `memset` is usually an argument; `ManagerSingleton`'s own clear was invisible | 3 of 29 |
| **call-return rooting** — a call to a route's `FN` accessor roots `rax`, and `lea rY,[rX+imm]` carries a root | `PersistentFlagPayload` is `FN 0x002EF640+0x200` and its clear is `call 002EF640` / `lea rcx,[rax+0x200]` / `memset` — a destination that is a return value | **5 of 29** |

The third mode also found one nobody had looked for: **`BattleSystemState`**, `0x7410`.

```
002370C4  mov  rcx, qword ptr [rip -> 02EBF190]   ; its own PTR route root
002370CD  mov  r8d, 0x7410                        ; its exact declared size
002370D3  call 00861EC0                           ; memset
002370DF  mov  dword ptr [rax], 0x5071901         ; then a marker dword
```

Seven span rows propagated. `PersistentFlagPayload` is the neat case for the mode: route function,
route offset and declared size all three agree in a 38-byte function, so the destination is that
type and not a size coincidence.

**Store-wide: 52,479 of 55,653 declared span bytes (94.3%) now carry a lifetime verdict**, leaving
3,174 bytes in 178 rows. Of the 29 size matches, 24 remain unattributed and are still only a
reading list — including `BattleUnit`, whose clears are confirmed by hand but whose `rcx` comes
from a bounds-checked pool walk that none of the three modes roots.

### The clear no sweep can find: a length held in a register

`MessageWindowRecord` was the largest span left without a verdict, and the bulk-write checker had
nothing to say about it — correctly, and for the reason its own docstring declares: **it recovers
only literal `mov r8d, imm` lengths.** This record's clear passes the length in a register, so no
literal sweep will ever see it, and it had to be followed by reading the allocator.

```
002A2C22  mov  ecx, 0x410
002A2C2E  call 00244F50                 ; the widget allocator
  00244F7D  cmp  ecx, 0x120             ; > 0x120 leaves the widget pool
  00244F83  ja   00244FB0
  00244FB2  call 002497B0               ; tagged alloc (0036C1D0 / 0036A100 / 0036C140)
  00244FCD  call 002465F0               ; the initialiser, rcx = block, edx = size
    0024661D  mov    rdi, rcx
    00246612  movsxd r8, edx            ; THE LENGTH IS THE CALLER'S SIZE ARGUMENT
    00246618  xor    edx, edx
    00246626  call   00861EC0           ; memset(block, 0, size)
```

So the record is zeroed in full at construction, and so is **every widget allocated through
`00244F50`** — the clear belongs to the allocator, not to any one type. 13 span rows propagated.

**This is the honest shape of the remaining residue.** The three seeding modes made the checker
better at *attributing* clears it can see; they did nothing about clears it cannot see at all. A
register-length `memset` is invisible to it by construction, and the only way through is to read
the allocation path. That is a limit on the instrument, not a gap in the engine — and it means a
type reported as "never cleared" by the sweep is a **question**, not an answer, unless its
allocator has also been read. `CharacterRenderObject`'s undefined verdict survives that test
because its allocator *was* read: `00210EC0` tail-jumps to `malloc`, with no initialiser between.

**Store-wide: 53,247 of 55,653 declared span bytes (95.7%) carry a lifetime verdict**, 2,406 bytes
left in 165 rows — none larger than `SaveImageHeader +0xC0` at 320 bytes.

### A second `UNDEFINED` verdict, and the test it had to pass

`LegacyPs2GsTextureContext` is now the second type whose spans are **undefined rather than zero**.
The `MessageWindowRecord` result made that claim harder to earn: a clear can hide behind a
register-held length, so "no literal `memset` of this size" is no longer sufficient. Four checks,
all negative, and the third is the one the widget case added:

1. the allocator `003EC8D0` is tag / alloc / restore / null-check / return — `mov edx, 0xb`,
   `call 0036C1D0`, `call 0036A190`, `call 0036C140` — with no clear;
2. `0036A190` is a 10-byte thunk to `0036A1A0`, and **neither they nor any of their callees one
   level down make a `memset`/`memcpy` call of *any* length** — the check that matters, because
   the widget allocator's clear passes its length in `edx`;
3. the initialiser `002F6AB0`, 2,118 bytes, sets fields one at a time and contains **zero** bulk
   calls;
4. no literal `memset`/`memcpy` of length `0x240` exists anywhere in the listed bodies.

`SaveImageHeader` went the other way and needed no new argument: it is `FN 0x002EF640+0x0`, the
first `0x200` of the buffer at `02164280`, and `0x56690` = that header plus the `0x56490` payload,
so it sits inside the same two clears that cover the `SavePayload` spans — by arithmetic.

### Where this leaves the store

| verdict | bytes | rows |
|---|---|---|
| zero-initialised | 52,691 | 175 |
| genuinely undefined | 1,374 | 18 |
| **no verdict** | **1,588** | 149 |

**97.1% of declared span bytes now answer the lifetime question**, and the residue is 1,588 bytes
whose largest single row is 192. The two verdicts remain opposite and both are now
exhaustion-backed rather than inferred from silence.

### Two lifetimes inside one subsystem, and an object whose address is never formed

**`LegacyPs2GsSourceTextureRecord` is zeroed although its owner is not.** The bank hanging off
`owner+0x150` is allocated and immediately cleared with a register-held length:

```
00467DDD  call 003EC8D0            ; edx = count*0x60 via lea/shl; the allocator does not clear
00467DEB  mov  qword ptr [rbx], rax
00467DE9  xor  edx, edx
00467DF2  mov  rcx, rax            ; the block
00467DEE  lea  r8, [rcx+rcx*2]
00467DF5  shl  r8, 5               ; count * 0x60 - the whole bank
00467DF9  call 00861EC0
```

So inside one subsystem the container is **undefined** and the bank it points at is **zero**. A
reconstruction needs both facts; either one generalised would be wrong.

**`CharacterRenderSystemTail` is the third `UNDEFINED`,** and it is settled by an argument the
earlier cases did not need. The object is real and busy — **155 censused accesses at 27
displacements** — but:

* its containing block is one `0x48930` allocation (`003325E7`) through `0036A100`, and neither
  `003325D0`, nor `0036A100`, nor any callee one level below it makes a bulk call of any length;
* no literal bulk write of `0x48930` exists;
* three literal `0x130` clears exist — one targets a stack buffer (`lea rcx,[rsp+0x30]`), the
  other two clear their own `rcx` **parameter**;
* **and this object can never be that parameter, because its address is never formed.** There is
  no `lea` with displacement `0x48800` and no instruction anywhere carrying `0x48800` as an
  immediate. Every access indexes it directly off the pool base.

That last step is what closes it. "Nothing clears an object" is otherwise very hard to show once
register-length clears are in play, and the usual answer — *check the callers* — is unavailable
when the object is never handed to anyone. Here that unavailability is itself the proof.

Worth noting: the per-record clear does not reach it either. `160 × 0x740 = 0x48800`, which is
exactly where this tail begins.

**97.7% of declared span bytes now carry a lifetime verdict** — 1,674 bytes undefined across 25
rows, 1,288 bytes still unanswered across 142 rows, largest single row 68 bytes.

## `check_clear_exhaustion.py`, and the row it caught me overstating (2026-09-19, OPUS)

Having run the same four-check exhaustion by hand four times, it is written down:

1. the allocator named in `allocation_site` makes no `memset`/`memcpy` — **of any length**;
2. nor any callee one level below it;
3. the `ctor` makes none, nor its callees one level down;
4. no literal bulk write equal to the declared size exists anywhere.

Checks 1–3 are deliberately **length-blind**, because `MessageWindowRecord` proved a clear can hide
behind a register and check 4 alone would miss it.

### The control found two false positives and one real defect — mine

Replaying the five types already settled by hand (`--all-spans` exists for exactly this):

| type | tool says | reading the site |
|---|---|---|
| `BattleUnit`, `MessageWindowRecord` | ZERO | correct |
| `CharacterRenderObject` | ZERO at `001F4F0D` | **false positive** — `lea rcx,[rsp+0x30]`, a 0x318 **stack buffer**, not `this`. Verdict stands. |
| `LegacyPs2GsTextureContext` | ZERO at `003ED43F` | **false positive** — `lea rcx,[rbx-0xf4]` / `mov r8d,0x180`: neither this type's base nor its `0x240` size, followed by `mov dword [rbx-4], 0x3f800000`. Verdict stands. |

**But the second one exposed a real error in what I had already written.** That row's evidence
said the initialiser `002F6AB0` makes no bulk call *"nor do its callees"* — and its callee
`003ED3F0` does. I had checked the initialiser's own body and the *allocator's* callees, and then
written a claim about a route I never examined. The verdict survives because the site turned out
to be unrelated, but it survived by luck, not by the evidence I cited. The row is corrected in
place and says so.

That is what the control was for: a tool that merely agreed with me would have told me nothing.

### The remaining tail, and why it is not worth grinding

46 types still have unanswered spans: **22 candidate UNDEFINED, 11 candidate ZERO, 13 skipped**
because their `allocation_site`/`ctor` columns name no address. Together they are **880 bytes in
120 rows** — 1.6% of declared span bytes, largest single row 68 bytes.

Given the control's demonstrated false-positive rate, each would need its site read individually,
and no candidate may be written to the store without that. The list narrows *which* sites to read;
it settles nothing. Recorded as a bounded remainder rather than worked through, because the
marginal byte here costs as much to establish as the 23,224-byte span did.

## The `SKIPPED` types were not a gap — they were three other answers (2026-09-19, OPUS)

`check_clear_exhaustion.py` skipped 13 types for naming no function address in
`allocation_site`/`ctor`. I first read that as an ownership gap in my own columns. It is not: those
types name no function because they legitimately have none, and their storage class **is** the
answer.

**`IMAGE` in `.bss` → zero at load.** `ActorManagerSlot`, `TextLayoutRecord`,
`ImageAddressArenaRecord`, `WorldLootPickupNode`, `AiOrderSet`, `BattleFormulaScratch`,
`AuthoredTableHeader`. Each address was checked against the PE section table here rather than
taken from the column's prose — all lie beyond their section's `SizeOfRawData`, so the loader
zero-fills them. No allocation call and no `memset` exists or is needed.

**`INTERIOR` → inherit the parent's clear.** Eleven types, once the parents were settled:
`ActorStorageRecord`'s five interiors and their own two, plus `BattleUnit`'s two,
`ImageBackedStateBlock`'s one and `ActorManagerSlot`'s one.

**`IMAGE` inside raw data → the value is *readable*, and that is a third category.**

### The store already knew, again — this time about itself

`ActorStorageRecord` is cleared by a register-length `memset` at `00267A8B`, and **its own
`allocation_site` column already said so**: *"zeroed by 00861EC0 at 00267A8B"*. The fact had never
reached its eleven field rows. The propagation gap this thread began with — page to store — also
runs *inside* the store, from `types.tsv` to `fields.tsv`, and nothing was checking that either.

### `InventoryClassDescriptor` is not a lifetime question at all

Its three spans sit in initialised `.data`, so their bytes can simply be read. They are **not
zero**:

| span | non-zero rows | distinct values |
|---|---|---|
| `+0x10` (8 B) | 8 of 15 | 8 |
| `+0x38` (4 B) | **15 of 15** | **15** |
| `+0x44` (20 B) | 12 of 15 | 7 |

Fifteen distinct values in fifteen rows is authored per-row content, not padding and not slack. So
these spans are a **semantic** gap — real shipped data that nothing in the corpus reads — and that
belongs to FABLE, not to a lifetime sweep. Recorded with the measurement and no meaning claimed. A
reconstruction must carry these bytes; it cannot synthesise them.

**99.3% of declared span bytes now carry a verdict** — 390 bytes in 55 rows left, and they are
genuinely different cases: `CALLER` stack frames (`BattleResultRecord`, `EvaluationContext`,
`EfxCallerTemplate`), `POOL`/`RESOURCE` storage (`SpawnRecord`, `ActorDefinitionPayload`) and
interiors of loaded authored blobs (`StatusDefinitionRecord`, `LegacyPs2GsReferenceDescriptor`).

### `CALLER` storage: the builder is the allocator

A stack frame has no allocator to read, so for the three `CALLER` types the question is whether
the **builder** clears its own frame. It was three different answers.

**`BattleResultRecord` — cleared.** `BattleStats_ChangeStatusAndProcessSideEffects` does
`xor edx,edx` / `lea rcx,[rsp+0x80]` / `mov r8d, 0x148` — the type's exact declared size —
`call 00861EC0`, at `0030E5E1`. The `allocation_site` column already named that fill; it had never
reached the field rows. That is now the third place the same propagation gap has appeared.

**`EfxCallerTemplate` — cleared, and the count is the proof.** Six shipped constructors build the
`0x890` template in their own frames, and a sweep finds **exactly six** literal `0x890` memsets —
`0026FC5B`, `002FC537`, `003B0726`, `003B223D`, `003B2A56`, `003B3972`. Six clears for six
builders, none missing and none left over; a count that matched loosely would have meant much
less. Since `0024B3A0` then copies the whole `0x890` into the heap object, the zero carries.

**`EvaluationContext` — uncleared, and this is a weaker verdict than any so far.**
`BattleFormula_BuildEvaluationContext` makes no bulk call, nor does any callee, and no literal
`0x2A` write exists anywhere. So the bytes are whatever previously occupied that stack region —
**and unlike an uncleared heap block, which is at least stable for the block's lifetime, this
frame is rebuilt on every call.** Two invocations in one run can differ. A reconstruction may put
anything there, but must not assume zero *or* assume consistency.

**99.4% answered** — 335 bytes in 41 rows left, across `POOL`/`RESOURCE` storage and interiors of
loaded authored blobs.

### `POOL` storage has two scopes, and only one of them is zero

`SpawnRecord` is the first type where "is it cleared?" has two different answers depending on
which lifetime you mean.

* **Pool scope — zero.** One `0x9400` heap block (exactly `64 × 0x250`), allocated at `00236957`,
  published to `0208E690` at `0023695E`, zeroed at `0023696E`. Zeroed **again** wholesale on area
  transition: `SpawnKeep_RotatePersistenceBanksForAreaTransition` copies the banks and then does
  `xor edx,edx` / `mov r8d, 0x9400` / `call 00861EC0` at `002339B0`, with `rcx` traced here to a
  load of the pool base.
* **Slot scope — not zero.** There is **no per-slot clear**. The image's only literal `0x250`
  memset (`0036496A`) targets the unrelated static `022CBBB0` — a size coincidence, checked and
  excluded rather than assumed away.

So a slot reused *within* one area carries the previous occupant's bytes in any field the new user
does not write. **`BattleUnit` is the contrast that makes this legible**: it is memset on both
allocate *and* release, which is exactly what makes a pool slot safe across reuse, and
`SpawnRecord` has neither. A reconstruction may rely on zero at pool creation and after each area
transition, and must not rely on it at acquisition.

That is a distinction no sweep would have produced on its own: both types would have been reported
as "cleared somewhere" by any instrument that only asks whether a `memset` of the right size
exists.

### The fourth category: authored file content, whose value is not in the executable

`StatusDefinitionRecord`, `LegacyPs2GsReferenceDescriptor` and `AuthoredBlobFixupTable` are
interiors of **loaded authored blobs** — bytes read from a shipped data file, not produced by the
image or an allocator. The loader does not initialise them either:

```
AreaData_BindAndRebaseSectionDescriptor  003845F0
    003845F4  mov  qword ptr [rcx], rdx     ; store the blob pointer
    00384600  mov  eax, dword ptr [rdx+0xc] ; an embedded offset
    00384608  test eax, eax / je            ; zero means "absent"
    0038460C  add  eax, edx                 ; otherwise ADD THE BLOB BASE
    0038460E  mov  dword ptr [rdx+0xc], eax ; and write it back
```

— and again at `+0x10`, `+0x18`, `+0x1C` and on. It **relocates in place** and contains no
`memset` or `memcpy` at all.

So the lifetime question closes, but with an answer unlike the other three: these bytes are
**neither cleared nor uninitialised — they are file content, valid from the moment of load**. What
does *not* close is the value, and it cannot: **it is not in the executable.** Settling it means
decoding the shipped asset, which is a different instrument from every one used in this thread.

That is worth separating from "unknown". A reconstruction must load the same authored data; it can
neither clear these bytes nor synthesise them, and no amount of further disassembly will reveal
what they contain.

**The four verdicts now in the store**, and they are genuinely different obligations:

| verdict | what a reconstruction must do |
|---|---|
| zero-initialised | clear it, or match the clear's scope (pool vs slot — see `SpawnRecord`) |
| undefined | anything, including zero — but never *assume* zero |
| undefined, uncleared stack | anything, and not even consistent between two calls |
| authored file content | load the same asset; the value is outside the image |

**99.6% of declared span bytes answered** — 244 bytes in 25 rows.

### A type with no single verdict: `BattleStatsRecord`

This is the first type whose lifetime cannot be written as one answer, because it has two storage
homes and they now carry different guarantees. Both are *reached* through `BattleUnit +0x698`, and
neither is stored in `BattleUnit`.

| home | where | verdict |
|---|---|---|
| kind 0 (party) | `BattleSystemState +0x08 + k*0x1C8` — 65 records fit, last ends `0x73D0` inside `0x7410` | **zero**, from the full `0x7410` clear at `002370D3` |
| kind 1 | `SpawnRecord +0x80` — `0x80 + 0x1C8 = 0x248`, inside the `0x250` slot | **zero at pool scope only** — cleared at pool creation and on area transition, never per slot |

So the same field of the same type has different guarantees depending on which home the instance
occupies. Code that relies on zero here is correct for party units and wrong for the other kind,
and a reconstruction that clears one pool but not the other reproduces the engine exactly.

This is the payoff from having settled `SpawnRecord`'s two scopes separately. Had `SpawnRecord`
been recorded as simply "cleared" — which is what every sweep in this kit would have said — this
row would have inherited a guarantee it does not have.

## The lifetime campaign, closed at 99.91% — and what the last 52 bytes are waiting on

Every declared span in this store now answers *"what is in these bytes before anything writes
them?"* except five rows totalling 52 bytes, and those five are **blocked on a named prerequisite
rather than unexamined**:

| rows | bytes | type | blocked on |
|---|---|---|---|
| 2 | 24 | `AudioParameterRamp` | its owner is a **`Category`**, a type this store does not declare. The same gap `check_embed_parent_fields.py` reports as a `DYNAMIC` route naming an undeclared owner. |
| 1 | 4 | `PhyreNamespaceBuffer` | its data is *"allocated by `0017D260` with alignment 4, **or borrowed**"* — the storage is conditional, so there is no single lifetime until the ownership bit is resolved |
| 2 | 24 | `PresentationEntryReference{Container,Node}` | interior to the **render root +0x160**, whose own lifetime is not established; no literal `0xC30` or `0x30` clear exists |

Two late cases are worth keeping because each would have been got wrong by a simpler rule.

**`GameSettingConfig` — the object is cleared, and the span still is not.** Allocated through the
same malloc tail-jump as `CharacterRenderObject`, then initialised by a function that *does*
`memset` — which is why any length-blind check calls it a candidate for zero. But the clear is
`lea rcx,[rsi+0x7c]` / `mov r8d, 0x3cc`, covering `+0x7C..+0x448`, and it is that function's only
one. The span sits at `+0x65B`, outside it, and no `0x65C` clear exists anywhere. **A partial
clear has to be checked by arithmetic, not by its existence.**

**`WidgetMessage` — a second uncleared stack type.** No literal `0x18` clear exists anywhere, so
no builder zeroes one; like `EvaluationContext`, the frame is rebuilt per call and the content can
differ between two sends in one run.

### What the store can now tell a reconstruction

| verdict | rows | obligation |
|---|---|---|
| zero-initialised | most | clear it — and match the **scope** (`SpawnRecord`: pool yes, slot no) |
| undefined | 47+ | anything, including zero; never *assume* zero |
| undefined, uncleared stack | `EvaluationContext`, `WidgetMessage` | anything, and not even consistent between two calls |
| authored — image | `ItemClassDescriptor`, `InventoryClassDescriptor` | carry the table's bytes; they are readable and were read |
| authored — file/resource | the loaded-blob types, `ActorDefinitionPayload` | load the same asset; the value is **not in the executable** |
| differs by home | `BattleStatsRecord`, `GambitConfig` | two answers, one per storage home |

None of these distinctions existed in the store this morning; every span row said only
*"extent-declared gap … no censused access"*.

## `Category` declared — the last undeclared owner, and it paid twice (2026-09-19, OPUS)

`AudioParameterRamp`'s route is `DYNAMIC *(Category+0x38) stride=0x30 count=*(Category+0x78)`, and
`check_embed_parent_fields.py` has reported for weeks that the named owner is a type this store
does not declare. It was the last such route, and the last lifetime rows blocked on a prerequisite.

Everything needed was already in the corpus or one function away. RTTI names the class
**`SQEX::Sd::ConfigFile::Category`**; `Category::InitializeRefCategory` is `007AA320` — the
`01CB44B0` the old row cited is that function's **name string**, not the function. The size is an
instruction: `007AAB32 mov r8d, 0x88`, immediately before the `memset` at `007AAB3B` and the
constructor call at `007AAB43`.

**The constructor is the field map.** `007A96F0` is 98 branchless bytes that install two vtables
and zero the body — and set exactly two things non-zero:

```
007A9743  mov dword ptr [rcx + 0x48], 0x3f800000
007A974A  mov dword ptr [rcx + 0x4c], 0x3f800000
```

`0x3f800000` is float **1.0**, and the audio pages independently name `+0x48` the volume master
and `+0x4C` the pitch master — the two values `007A9F40` and `007A9D30` multiply. A multiplier
initialised to the identity is what "master" predicts, and that agreement is the check.

### It also closed two spans that were never unread

Declaring the owner made the child's initialiser findable, and it is a **per-element loop**, not a
clear:

```
007AA199  lea r14, [rip -> 01CB44A0]        ; .rdata, first qword 007A9820 -> a vtable
007AA1C0  mov qword ptr [rax], r14          ; every element's +0x00
007AA1CE  mov byte  ptr [rax+0x20], bpl     ; rbp = 0
007AA1D5  lea rax, [rax + 0x30]             ; AudioParameterRamp's stride
```

So `unobservedSpan0000` **was never unread** — it is a vtable pointer, written by a loop no census
reached because the array hangs off a pointer the `Category` owns. And byte `+0x20` inside the
tail span is the **active flag** the ramp page already describes as gating the walk: writer and
reader agreed, with the store holding neither.

`AudioParameterRamp` is also the first type recorded as **initialised field by field and not
cleared** — `007AA110` has no `memset` at all, and the `Category`'s own `0x88` clear covers the
*pointers* at `+0x38`/`+0x40`, not the arrays they point at. The bytes the loop skips are
genuinely undefined.

**Store: 97 types, 3,024 field rows. 99.95% of declared span bytes carry a lifetime verdict** —
28 bytes in 3 rows left, all blocked on the render root or the `PhyreNamespaceBuffer` ownership bit.

## Lifetime: complete. 344 span rows, 55,678 bytes, 0 unanswered (2026-09-19, OPUS)

Every declared span in this store now answers *"what is in these bytes before anything writes
them?"* This morning none of them did — each said only *"extent-declared gap … no censused
access."*

The last row was the sharpest. `PhyreNamespaceBuffer +0x04` is 4 bytes, and its two instances are
stack locals of one caller which initialises them **identically and partially**:

```
0059E11F  mov dword ptr [rsp+0x48], r12d    ; descriptor A, +0x00
0059E124  mov qword ptr [rsp+0x50], r12     ; descriptor A, +0x08
                                             ;  +0x04..+0x07 never written
0059E115  mov dword ptr [rsp+0x58], r12d    ; descriptor B, +0x00
0059E11A  mov qword ptr [rsp+0x60], r12     ; descriptor B, +0x08
```

The caller zeroes *around* the span and skips it, twice. That also **precised this type's own
instance column**, which said the locals were "zeroed before the call": they are zeroed in part,
and this dword is the part that is not.

### What was actually learned

The campaign began as propagation — copying findings the subsystem pages already had into the
store. It stopped being that almost immediately. The recurring result was that **"no censused
access" and "uninitialised" are different questions, and only the first had ever been asked**:

* a span with no reader is usually **zeroed wholesale** by something no field census can see —
  a `memset` in a constructor, an allocator, or a pool reset;
* the instruments that find those clears are blind in specific, nameable ways — a literal-length
  sweep cannot see `memset(p, 0, size)`, and an offset-keyed page search cannot see a fact stated
  about the object;
* every negative therefore needed a control, and **three of them failed their control** — the
  first `.text` sweep (0.19% decoded), the first bulk-write run (zero in an image with four known
  clears), and the first span-propagation pass (`BattleUnit`: two rows flagged, thirty true).

Six distinct obligations came out of it, and the differences are not cosmetic: `SpawnRecord` is
zero at pool scope and not at slot scope; `BattleStatsRecord` has two answers by home;
`GameSettingConfig` is cleared everywhere except where the span is; `CharacterRenderObject` must
*not* be assumed zero; and the loaded-blob types have a value that is not in the executable at all.

**A reconstruction can now be told, for every declared gap in this store, what it must put there.**

## Readiness: `infer_field_type.py`, and the same bug for the third time (2026-09-19, OPUS)

With lifetime closed, the store's remaining structural debt is **readiness**: 431 non-span field
rows sat at `DISCOVERED`/`UNKNOWN` — width and access recorded, nothing else. Some of those are
semantic and belong to FABLE. Many are not: **the instructions already fix the representation**,
and a representation is OPUS's to state.

A field read with `movss` is a float whatever it means. A field whose loaded value becomes a
memory base is a pointer. A field read with `movzx` and never `movsx` is unsigned. None of that
claims a purpose, and all of it raises a row off `DISCOVERED` with a citation.

**On `ManagerSingleton0209BE80` the tool's first run found 2 candidates of 27. The corrected run
found 13** — and the difference was my own defect, for the third time in this session:

```
if i.operands and i.operands[0].type == X86_OP_REG \
        and i.reg_name(i.operands[0].reg) == dst:
    dst = None          # `cmp rax, rbx` clears the very value being traced
```

`reg_tracking.written()` exists precisely to prevent that, and I reintroduced the positional
shortcut in a new file anyway. It suppressed 11 of 13 findings. **The lesson is not "be careful" —
it is that this kit needs the write-set helper used by default, and any new tracker that does not
import it should be suspect on sight.**

### What was accepted, and what was refused

Ten rows moved to `TYPE RESOLVED`: seven pointers (`+0x10EF0`, `+0x10F00`, `+0x10F20`, `+0x10F30`,
`+0x10F78`, `+0x10F80`, `+0x10FB0`, each with the load site and the base use cited) and three
signedness fixes from zero-extending loads.

One was **refused and recorded as a question instead**: `+0x10FAC` is declared 4 bytes and its only
censused access is a **two**-byte `movzx`. That may be a 2-byte field with two bytes belonging to
something else, or a wider field read by its low half. The store's convention allows `ctype` to be
the instruction's width, so it is not automatically a defect — but nothing establishes the upper
two bytes, and no row gets widened on the strength of an adjacent gap.

One was **flagged as an anecdote**: `+0x10CFC` has a single `or … 0x40`, and one instruction is not
a bit set.

**Store-wide: `DISCOVERED` 495 → 485, `TYPE RESOLVED` 1,220 → 1,230.** Modest, mechanical, and
repeatable on any type with a census — which is now most of them.

### `add` is not `mov`, and the store's own naming caught it

Run across the other censused types, `infer_field_type.py` reported four candidates for
`LegacyPs2GsTextureContext` — three of them fields **this store already calls `addendXXXX`**,
described in their own rows as *"a qword ADDED to a register"*. The tool was calling them pointers.

It was wrong, and the reasoning is worth keeping:

```
add rcx, qword ptr [rax + 0x188]    ; rcx later used as a memory base
```

That proves `rcx_old + field` is an address. It does **not** prove the field is a pointer — the
other operand may be the base and this the displacement or the size. Only a `mov`-loaded value
that becomes a base establishes a pointer. The tool now separates the two and reports the weaker
case as `addrterm`, with the docstring saying why.

**Those three rows were therefore not upgraded.** They keep their `uint64` ctype, their `addend`
names — both already right — and their `DISCOVERED` readiness, because *knowing a value
participates in an address is not knowing what it is*. Only `+0x1D8`, a genuine `mov`, moved.

It is worth noting what did the catching: not a control, but the **field names the store already
had**. A tool that told me `addend0188` is a pointer was contradicting the row it was annotating,
and that mismatch was visible in the output.

### Readiness, so far

| | session start | now |
|---|---|---|
| non-span rows at `DISCOVERED`/`UNKNOWN` | 431 | **415** |
| `TYPE RESOLVED` | 1,220 | **1,236** |

Fifteen rows moved on citations, two ctype **corrections** (`uint16` → `int16`, where the
instruction sign-extends and the row claimed unsigned), and three refusals recorded as questions
rather than answers. Lifetime remains 344/344.

### The census I was using was the wrong one, and the tool said so in its own docstring

`BootSingleton01F7F598` has 18 weak rows and my `gen_ptr_census_depth1.py` found **3 accesses at 2
offsets** for it. That looked like a coverage problem. It was an instrument-choice problem, and
`member_reach_scan.py` documents this exact type as its worked example:

> *"`BootSingleton01F7F598` has THREE slot loaders against 117 callers of its one-instruction
> accessor, so seeding from its slot sees almost nothing — that is exactly how 160 of its bytes
> sat 'unobserved'."*

Seeded correctly — `--accessor 00189120`, 117 seed callers, **195 proved member bodies** through
`this`-in-`rcx` handoffs — the same offsets report counts up to ×29. My depth-1 census follows one
call level from a *global load*; this follows a reachability closure from an *accessor's return
value*. For a type whose pointer is fetched by a helper rather than loaded inline, the second is
the only one that works.

**Two rows are silent even under that closure, and I misread the silence.** `+0x0D14` and
`+0x0D5C` come back `STILL UNOBSERVED` while their neighbours show ×29 and ×8, and I recorded that
as a question about whether they should be fields at all. They should. Both are **written by the
constructor** — the rows already say so, `ctorFloatD14` holding `0x40A00000` (5.0f) and
`ctorZeroByteD5C` zeroed — and **an accessor-seeded closure cannot contain a constructor**: the
constructor runs before the object can be returned by the accessor, so no caller of the accessor
is it.

The silence is structural, not evidential. **An accessor closure measures USE and never
INITIALISATION**, so its quiet on a ctor-written field says nothing at all. Both rows are
corrected in place and carry that reasoning; the flag I added minutes earlier was wrong and says
so.

**A concrete tool gap, stated rather than worked around:** `member_reach_scan.py` reports access
*counts* per offset, not instruction text, so its richer census cannot currently feed
`infer_field_type.py`. That is what stands between the readiness inference and the types where it
would pay most.

### Closing the gap: the strongest census can now be typed, not just counted

`member_reach_scan.py` proves the largest member sets in the kit and then reported each offset as
a bare tally — so the richest census here could not feed `infer_field_type.py` at all. A tally
cannot say whether a field is a float, a pointer or signed.

It now takes `--census-out`, writing every DIRECT access as `function/name/site/disp/kind/
instruction` — the format the inference already reads. The change is one sink at the single line
where a direct access is recorded, and **the tool's own self-test still passes all five controls**.

On `BootSingleton01F7F598` that turns **3 accesses at 2 offsets** into **539 at 158**, and the
inference immediately returns 6 of its 18 weak rows — including two the store had wrong:

| offset | declared | instruction | corrected to |
|---|---|---|---|
| `+0xCD0` | `uint32` | `00189997 movss xmm0, dword ptr [rcx+0xcd0]` | **`float`** |
| `+0xDAC` | `uint32` | `00187872 movsxd rax, dword ptr [rcx+0xdac]` | **`int32`** |

Both had been typed from the **constructor**, which stores a zero dword — indistinguishable from
`0.0f`, and silent about signedness. **A writer of zero cannot type a field; a reader can.** That
is the general lesson, and it applies to every `ctorZero…` row in the store.

Three more were confirmed rather than changed, and one width question was raised and left open:
`+0xDB9` declares two bytes and its only reader takes one — the row keeps its width, because
nothing establishes the second byte and a row is not narrowed on a single reader.

**Readiness: non-span `DISCOVERED`/`UNKNOWN` 431 → 410; `TYPE RESOLVED` 1,220 → 1,241.**

### The two censuses are complementary, not ordered — and I assumed otherwise

After `member_reach_scan.py` turned `BootSingleton01F7F598` from 3 accesses into 539, I described
it as the stronger instrument. Running both over `ManagerSingleton0209BE80` shows that is wrong as
a general claim:

| | rows | offsets |
|---|---|---|
| `gen_ptr_census_depth1.py` | 276 | 54 |
| `member_reach_scan.py --slot` | 252 | 46 |
| shared | 249 | — |
| **union** | **279** | **55** |

Depth-1 contributes **9 offsets the closure never sees**; the closure contributes **1** that
depth-1 misses. For `BootSingleton` the ratio is the other way round and enormous — 539 against 3.

The reason is that they seed differently and follow different things. Depth-1 seeds on a slot
**load *and store*** and follows the object into a callee **in any argument position**; the
closure seeds on slot loads (or an accessor's callers) and follows only `this`-in-`rcx` at
displacement **0**. So a type whose pointer is fetched by a helper is invisible to the first, and
a type handed to callees as argument 2 or 3 is invisible to the second.

**Neither dominates, the union is cheap, and running one alone is how an offset goes missing.**
The `+0x10FA6` upgrade in this type exists only in the closure census; nine other offsets exist
only in depth-1.

**Readiness: non-span `DISCOVERED`/`UNKNOWN` 431 → 409; `TYPE RESOLVED` 1,220 → 1,242.**

## The Phyre size table closes 177 unresolved extents — 15 of them exactly (2026-09-19, OPUS)

Chasing `PPhysicsRigidBodyBase`'s 14 weak rows hit a wall: its size is `UNRESOLVED`, so no
vtable-seeded closure can bound it. That turned out to be the interesting part. **177 of the
store's 182 `UNRESOLVED` types are in the size table built at the start of this session** from the
class-descriptor constructor's argument list.

### The fit check is a far stronger control than this morning's

Every one of those 177 types already has field rows, derived from the **Phyre reflection member
registrations** — a different method, a different subsystem, and no shared input with the
constructor's `mov r8d, imm`. Comparing them:

* **177 of 177 fit inside the stated size.**
* **0 overflow.** A single field lying past the size would have refuted the table.
* **15 sum to the size EXACTLY, with no remainder.**

This morning's control was 33 exact fits against the same store's own field census. This one is 15
exact fits against an independently derived field map, plus 177 non-violations. Two unrelated
derivations agreeing to the byte is not something a mis-read argument produces.

### What was applied, and what was not

The 15 exact-fit types have their extent set: `PAnimationClipBinding`, `PAnimationEvent`,
`PClusterHeaderBase`, `PInstanceListHeader`, `PPhysicsMaterial`, `PSkinBoneRemap` and nine more.
**Types with a resolved size: 97 → 112, and sum mismatches remain 0.**

The other 162 are **deliberately not applied yet.** Setting their sizes imposes the store's
sum invariant, which would need **465 declared span rows** to satisfy — and every one of those
rows would then be a fresh lifetime question, reopening a metric that just reached 344/344. That
is a real design decision with a measurable consequence, not a mechanical edit, and it should be
made deliberately rather than at the end of a long pass. The distribution is recorded so the cost
is known: 18 types need one span row, 71 need two, 38 need three, 30 need four or more.

## Ruling: the 162 extents are applied, and the lifetime metric drops (2026-09-19, OPUS)

The 162 remaining Phyre extents were held back because setting a size imposes the sum invariant,
costing 465 declared span rows and reopening the lifetime metric that had just reached 344/344.
That is a real cost. It is also the wrong reason to withhold a known fact, and the ruling goes the
other way:

* **A type with `size=UNRESOLVED` cannot be allocated by a reconstruction at all.** A known size
  with honestly declared gaps is strictly more useful than no size.
* **The metric falls because those 162 types genuinely have unestablished lifetimes.** That was
  true before; `UNRESOLVED` was hiding it. **A number that improves by withholding a known fact is
  measuring the wrong thing** — the same reasoning the charter applies to `engine_explained`.
* The extents are not guesses. Each is the constructor's `mov r8d, imm`, and the fit check against
  independently derived reflection field rows is 177/177 with zero overflows.

**Applied: 162 extents, 465 declared gap rows.** Types with a resolved size **97 → 274**; field
rows 3,027 → 3,492; **sum mismatches 0**, dangling refs 0, storage-class failures 0.

What the gap rows claim is narrow and stated on every one: the range lies inside the extent and no
Phyre reflection member registration covers it. That is a fact about the **member table**, not the
engine — Phyre registers what it exposes to serialisation and script, so an unregistered range is
**unexposed, not unused**.

### The lifetime figure, stated honestly

| | rows | bytes |
|---|---|---|
| span rows with a verdict | 344 | 55,678 |
| **without** | **465** | **33,587** |

**344 of 809, down from 344 of 344.** Every one of the 465 is a Phyre engine object's gap whose
allocator has not been read individually, and each row says so rather than carrying a borrowed
verdict.

**A measurement trap worth recording:** the first count after this change reported *809 of 809
answered*. The new rows' evidence contains the phrase *"NO LIFETIME VERDICT"*, and the check was a
substring test for `LIFETIME`. A metric that counts an explicit denial as a confirmation is worse
than no metric; the count now excludes the denial explicitly.

## 90 Phyre classes have no vtable, and that closes a route rather than opening one (2026-09-19, OPUS)

The plan after resolving the extents was `member_reach_scan --vtable` on the Phyre population —
the one seeding mode never exercised, and the only one that reaches a type with neither a
singleton slot nor an accessor. It does not apply, and the reason is a layout fact worth having.

**`PPhysicsRigidBodyBase` has no RTTI type descriptor.** The image contains 14 `.?AV` strings
naming it and every one is for a `PClassDescriptorConcrete<…>`, `PClassDescriptorAbstract<…>`,
`PClassDescriptorForType<…>` or `PMethodCallerConcrete<…>` **wrapper** — never the class. MSVC
emits a type descriptor for every polymorphic class, so its absence is evidence.

**The member schema settles it independently.** Of the 179 classes in the recovered schema, **90
register a member at offset `0x0`** — including `PPhysicsRigidBodyBase`,
`PPhysicsCharacterControllerBase` and `PMeshInstance`. A vtable pointer occupies `+0x00..+0x07`,
so those classes have none.

So **Phyre data classes of this shape are non-polymorphic, and their reflection is entirely
external** — carried by the class descriptor, not by anything inside the object. That is why the
descriptor system exists in the form it does, and it is now recorded on all 90 declared types.

**What it costs and what it is worth.** The `--vtable` route is unavailable for half the Phyre
population: there is nothing to seed from, so the 465 outstanding lifetime rows cannot be attacked
that way. Their allocation runs through the cluster loader and per-subsystem factories instead,
which is a different instrument again.

**Not claimed for the other 89.** A first registered member at `+0x8` or `+0x10` is consistent
with a vtable *and* with several other layouts, and nothing here distinguishes them. Only the 90
are annotated.

## The 465 Phyre gaps cannot be answered as one population, and here is why (2026-09-19, OPUS)

The hope was that Phyre objects all arrive one way — through the cluster loader — so one reading
would settle 465 lifetime rows at once. **The cluster route does have a clean answer, and it is
not enough.**

**The cluster route: allocate unzeroed, copy file bytes in, fix up in place.**

```
0059A48B  call 0017D260      ; _aligned_malloc - 12 bytes, no clear
0059A5A9  call 00861EBA      ; memcpy - the file's bytes into the buffer
```

`0059A3B0` contains **no memset at all**, nor does anything one level below it, and the fixup
tables the cluster header declares (`m_arrayFixupCount`, `m_pointerFixupCount`,
`m_userFixupCount`) are relocation records applied to that buffer. So an object that arrives this
way is **authored file content** — the same category as `StatusDefinitionRecord` — and neither
zero nor undefined.

**Why that does not close the 465.** The store's own `instance` column for these types says the
objects are *"instantiated inside the engine (**cluster object builders or per-subsystem
factories**)"* — two routes, and it does not say which type takes which. A blanket verdict would
be asserting for the factory-built instances something established only for the cluster-built
ones. The population is not homogeneous, and its own row says so.

So the remaining work is **per-type, not per-population**: for each Phyre class, which of the two
routes produces its instances. That is a real answer about the shape of the work, and it is worth
more than a verdict that would be wrong for an unknown fraction of 465 rows.

### An arithmetic slip, and nearly a false accusation

The bulk sweep reported a memcpy at decimal `5875113`. I converted that by hand to `0x59A529`,
disassembled there, found a `jmp`, and was about to record the detector as having produced a false
positive. `5875113` is **`0x59A5A9`**. The tool was right; my hex was wrong.

This session already recorded that *"a caution against a working tool is worse than no caution"*
after the same failure mode. The check that caught it was printing every call in the function
instead of trusting one converted address — and that is the cheaper habit.

## Splitting the Phyre population by instantiation route (2026-09-19, OPUS)

The 465 gap rows could not take one verdict because the store's own `instance` column says these
objects come from *"cluster object builders **or** per-subsystem factories"* without saying which
takes which. The reflection system answers half of that question itself.

**MSVC emits a distinct RTTI type descriptor per template instantiation**, so the image states,
per class, which descriptor wrappers exist. Over the 177 sized Phyre classes:

| | count | meaning |
|---|---|---|
| `Concrete` + `Abstract` + `ForType` | **140** | a **concrete** descriptor exists — the one the reflection system creates instances with, so the cluster loader can build these |
| `Abstract` + `ForType` only | **33** | **no** concrete descriptor — never instantiated as itself |
| no descriptor RTTI at all | 4 | the D3D11 structs; Microsoft types registered for reflection, not Phyre classes |

**The 33 are the more useful half.** `PMeshInstance`, `PMaterial`, `PDynamicMesh`,
`PCameraProjection`, `PInputSource` and 28 others have no concrete descriptor, so **their bytes
exist only as a sub-object inside a derived class** — their lifetime is the derived object's and a
reconstruction must never allocate one standalone. That is an ownership fact, and it is now on all
33 rows.

For the 140, the cluster route is available and its shape is known — `_aligned_malloc` with no
clear, then `memcpy` of the file's bytes, then fixups — so an instance arriving that way holds
authored file content. **What is still not claimed is that every instance arrives that way**; the
factory route remains unquantified, and no row asserts otherwise.

### A note on the instrument

The first sweep for these strings returned **0 of 177** — a regex with an over-escaped `?$`
against a known-present string. Testing the pattern against one literal string first, rather than
trusting a zero over the whole image, is what turned 0 into 918 matches across 334 classes.

## The Phyre hierarchy is shallow: three parents for 177 classes (2026-09-19, OPUS)

To place the 33 abstract-only classes I needed each one's derived class. Two approaches, and the
second is the answer to a different question.

**Naming does not work.** Pairing an abstract base with a larger concrete class sharing its stem
finds candidates for only **5 of 33**, and even those are containment-shaped as often as
inheritance — `PAnimationClipBinding` / `PAnimationClipBindingDataBlockCache` is not obviously a
base and a derived class. Recorded as tried and rejected rather than applied.

**The registrars answer a different and better-evidenced question.** Argument 6 of the descriptor
constructor becomes `+0x78`, the parent pointer that `PObjectAccessor<T>::Get` walks. Tracing
which call's return value reaches that argument, across all 177 registrars:

| parent descriptor | classes | from |
|---|---|---|
| `02CF8270` | **103** | `006372A0` — eight bytes: `lea rax,[rip -> 02CF8270]; ret` |
| `01F2E330` | **70** | `006373D0` — a thread-safe lazy init returning it on the fast path |
| `01F2E550` | **4** | `00630110`, same shape |

**Three distinct parents for 177 classes.** The hierarchy these registrations express is not deep:
the `+0x78` chain the accessor walks is at most a couple of links for these types, which is why
that walk is a short loop rather than a tree descent.

**What the three are is only partly settled.** `01F2E550`'s `+0x30` reads a clean name —
**`PInt32`** — which confirms both the descriptor shape and this morning's `+0x30`-is-the-name
finding from a third direction. `02CF8270` is `.bss`, so zero in the file and written at runtime.
`01F2E330` has its own address at `+0x00`, the self-linked-node shape rather than a vtable, so it
is **not** a descriptor base and is not named here.

**And it does not place the 33.** A shallow hierarchy with three shared roots cannot say which
derived class contains a given abstract base — that relationship is not in these arguments. The
33 keep the ownership statement they have (never instantiated standalone) without a named
container.

### The Phyre class hierarchy is not statically recoverable — three routes tried

Placing the 33 abstract-only classes needs the inheritance graph. Three attempts, all bounded
negatives, recorded so the fourth person does not repeat them:

1. **Naming.** An abstract base paired with a larger concrete class sharing its stem: candidates
   for **5 of 33**, and those are containment-shaped as often as inheritance. Rejected.
2. **The registrars' parent argument.** Argument 6 becomes `+0x78`, the pointer
   `PObjectAccessor<T>::Get` walks — but across 177 registrars it takes only **three** distinct
   values (103 / 70 / 4). A three-valued field cannot encode a hierarchy over 177 classes.
   `02CF8270`, the value 103 of them share, is named by the vtable `00164180` installs
   (`00D582D0` → COL `01D14970` → `.?AVPClassDescriptorBase@Phyre@@`): it is a
   **`PClassDescriptorBase` instance**, so the RTTI names the descriptor's own C++ type, not the
   class it describes.
3. **A base-registration API.** `00163E30` looked like the answer —
   `mov r8d, 0x30` / `lea rdx,[02CF8270]` / `lea rcx,[02CF8470]` / `call 00631C40`, exactly the
   shape of `register_base(derived, base, subobject_offset)`. **`00631C40` is called exactly
   once in the entire image.** It is not a general API, and there is no sweep to do.

**So the hierarchy is not in the static registration data**, and the descriptors that would hold
it at runtime are `.bss` — zero in the file. This is a live/runtime question, not a static one,
and it is routed rather than guessed at. The 33 keep the ownership statement they have — never
instantiated standalone — without a named container.

## 267 zero-width fields, and a defect they created in my own extent-filling (2026-09-19, OPUS)

Found by accident, reading a contaminated census for something else: **269 field rows declared
`size = 0`**, across 117 types — `PPhysicsRigidBodyBase` 14, `PPhysicsCharacterControllerBase` 10,
`PShaderPassD3D11` 9. Their ctypes are real (`VPString`, `VVector3`, `PWorldMatrix`), so these are
reflection-derived rows whose importer had no width and wrote zero.

**The sum invariant cannot see them.** A zero-width row contributes nothing to the total, so the
store reported 0 sum mismatches with 269 such rows present. `check_zero_width_fields.py` now
reports them; it writes nothing, because a width is a measurement.

### The obvious fix is wrong, and the store's own data refutes it

`check_embed_parent_fields.py` PASS 2 says a field whose ctype names a known type must carry that
type's size — which would fill 23 of the 269. **Thirteen of those 23 are refuted outright by the
next field's offset:** `PComponent m_next` has ctype `PComponent` (0x18) with **8 bytes** before
the next member, so it is a *pointer* to one. So a Phyre reflection ctype frequently names the
**pointed-to** type, and a naive PASS 2 fill would have written 13 wrong widths.

Only two were applied — `PShaderPassStateD3D11 m_rasterDesc` and `m_depthDesc`, whose widths come
from the **Microsoft D3D11 headers** (`0x28`, `0x34`), with the offset delta as corroboration
rather than as the derivation.

### And filling them broke the invariant, which exposed a defect in this morning's work

Applying those two widths took the type to 492 bytes against its 400-byte extent — overflowing by
exactly the 92 bytes added. The cause is mine: **the 465 gap rows generated when the 162 Phyre
extents were applied were computed with zero-width fields counted as occupying nothing**, so a gap
covers bytes such a field actually owns. The overlap is invisible until a width is filled in.

`PShaderPassStateD3D11`'s gaps are regenerated and the store is back to 0 mismatches. **The scope
is 117 types and 267 zero-width rows** — every gap row in those types is provisional in exactly
this way, and each will need regenerating as widths are established.

The extents themselves are unaffected: those are the constructor's `mov r8d, imm`, fit-checked
177/177. It is the gap bookkeeping around them that is conditional.

### Resolving zero-width fields from the type's own descriptor registrar

`VVector3` (26 rows) and `VVector4` (8) were the two largest zero-width ctypes after `VPString`.
Their widths are recoverable, and from the same place the 177 extents came from — each reflection
type has its **own class-descriptor registrar**, and argument 4 is the instance size:

```
006B1600 (the VVector3 registrar)
    006B163B  lea  rbx, [rip -> 02E50510]     ; the descriptor
    006B1671  mov  r9d, 0x10                  ; argument 4 -> descriptor +0x38, the SIZE
    006B1677  lea  r8,  [rip -> 00D7F310]     ; argument 3 -> the NAME, reads "Vector3"
    006B1681  call 00632C90
```

The name at argument 3 is the check that the registrar is the right one — `'Vector3'` and
`'Vector4'` — rather than an address that merely looked plausible.

**The method has an external control.** Run against the *initialised* scalar descriptors it gives
`unsigned int` → `01F2E5A0`, name `PUInt32`, size `0x4`, and `float` → `01F2E690`, name `float`,
size `0x4`. Both correct, so the read of `+0x38` is sound.

**One register mistake worth recording:** my first sweep tracked `r8d` and reported `size=0x0` for
both. `r8d` is argument 3, the *name* pointer; the size is `r9d`. The zero was my register, not
the engine's data — the fourth time this session a zero turned out to be the instrument.

**34 rows resolved, all 34 room-checked first** (the previous attempt had 13 of 23 refuted by the
next field's offset, so the check is not ceremonial). Gap rows regenerated for all 17 affected
types — **66 rows** — because of the coupling defect above. Store: 3,462 field rows, **0 sum
mismatches**, zero-width rows **269 → 233**.

### `VPString`: the descriptor names itself through RTTI

`VPString` was the largest zero-width ctype at 32 rows, and the sweep that resolved `VVector3`
found nothing for it. The reason is structural, not a miss: for `VVector3` the `lea` of the
descriptor and the constructor call sit in **one** body, while `PString`'s `lea` is in `00166C90`
and its constructor call is inside `006A7190` — **a different function**, invisible to a
single-body pattern.

Following the object instead of the pattern settles it. `00166C90` installs vtable `00D7B410` on
the descriptor at `02E4D630`, and RTTI reads that vtable:

```
00D7B410 - 8  ->  COL 01D2E9A8  ->  TypeDescriptor
   .?AV?$PClassDescriptorConcrete@VPString@Phyre@@@Phyre@@
```

`Phyre::PClassDescriptorConcrete<Phyre::PString>` — so `02E4D630` is the `PString` descriptor, and
its registrar states the size directly: `006A71D0 mov r9d, 8`, alignment 8 at `006A71C8`, and the
name at argument 3 reads **`'PString'`**. `PString` is a pointer-sized string handle; a `VPString`
member is **8 bytes**.

32 rows resolved, all room-checked, gaps regenerated across 21 types.

**Zero-width rows: 269 → 201 this session** (`VVector3` 26, `VVector4` 8, `VPString` 32, two
D3D11 descs). Store: 3,435 field rows, **0 sum mismatches**, 0 dangling refs.

---

## The last 201 zero-width rows: the engine states the width in a branch

The remaining 201 rows were the hard residue, and the naive rule had already been refuted on
them. Filling a row from its ctype — "the ctype names a type, so use that type's size" — produced
23 candidates of which **13 were contradicted by the next field's offset**, because a Phyre ctype
frequently names the type that is *pointed to* rather than an inline value. The rule could not say
which was which, so it was abandoned rather than applied with a fudge.

What settles it is not a rule at all. It is a branch in the engine.

### The member object, read from its two constructors

A class member is registered by `00632960(member, classdesc, typedesc, name, offset, attrs, …)`,
with `offset` at `[rsp+0x20]` and `attrs` at `[rsp+0x28]` in the caller's frame. That function and
the base constructor `00632FB0` between them fix the layout:

```
member +0x00   vtable
member +0x08   a named base sub-object, built by 00632FB0:
                 +0x10  the owning class descriptor      (632FB0: mov [rcx+0x10], rdx)
                 +0x18  the name                         (632FB0: mov [rcx+0x18], r8)
                 +0x20  THE ATTRS WORD                   (632FB0: mov [rcx+0x20], r9d)
member +0x30   the TYPE descriptor                       (632960: mov [rbx+0x28], rdi, rbx=member+8)
member +0x48   THE OFFSET                                (632960: mov [rsi+0x48], eax  <- arg5)
```

`attrs` is a word of **independent flags, not an enum**, and one of its bits already has a proven
meaning: `00632FB0` does `test r9b, 1`, and when bit 0 is set it strlens the name, allocates, and
memcpys it, storing the copy back at `+0x18`. **Bit 0 = the object owns its name string.** No
member row in this store has it set.

### The branch, and what the two sides write

Exactly **four functions in the entire image** test bit 1 of that word — `0063C4A0`, `0063D300`,
`0063AD90`, `0063C910` — and they are identical in shape:

```
0063C4A0   rax = [rcx+0x18]          ; the owning class descriptor
           r9d = [rcx+0x48]          ; the member's offset
           r9d -= [rax+0xF4]         ; a base adjustment
           r10  = sign_extend(r9d) + r8      ; r8 = the instance -> r10 = &instance.member
           r9   = [rcx+0x30]         ; the TYPE descriptor
           test byte ptr [rcx+0x28], 2
           rcx = r9 ; r8 = r10 ; rax = [r9]
           je   -> jmp qword ptr [rax+0x18]      ; bit CLEAR
               -> jmp qword ptr [rax+0x28]       ; bit SET
```

Both sides are handed the address of the member's slot and differ in exactly one respect — how
many bytes they put in it. For `VPWorldMatrix` (type descriptor `02E404B0`, vtable `00D6DE78`,
installed by registrar `00166080`):

```
+0x18 -> 0067E510   mov [rbx],ecx / [rbx+4],ecx / [rbx+8],ecx / [rbx+0xC],ecx …   INLINE VALUE
+0x28 -> 0067E380   mov qword ptr [rbx], rax ; ret                                ONE POINTER
```

**Bit 1 set ⇒ the slot is 8 bytes.** Clear ⇒ the slot holds the type's own instance size. That is
the engine's answer to the exact question the ctype could not answer, and it explains the 13
refutations: every one of them was a member whose ctype names the pointed-to type.

### The offset adjustment — CORRECTED, see below

> **This subsection was wrong and is kept only so the correction has something to point at.**
> `classdesc+0xF4` is **not** always zero; see *"The `+0xF4` claim was false"* further down.

### The offset adjustment is a no-op, and that had to be checked

`classdesc[0xF4]` is subtracted from every member offset before use, so a non-zero value would
have invalidated all 680 recorded offsets at once. It is zero. The base constructor `00632D80`
stores `r10` there inside a clearing run that also zeroes `+0xC0`…`+0xE0` (`r10` is the zero
register), and the nine sibling constructors at `006316C0`…`00632780` store `rbp` there after
`xor ebp, ebp`. No other write to a class-descriptor `+0xF4` exists in the image. **The recorded
offsets are true in-instance offsets** — a negative result, and the most load-bearing one here.

### Two corroborations from directions that could have disagreed

Neither was used to derive the rule, and either could have broken it:

* **Room.** 122 of the 201 rows have room for exactly 8 bytes before the next registered member,
  and **all 122 carry bit 1**, against a base rate of 154 set out of 680 schema rows.
* **Alignment.** All 153 rows the rule made 8 bytes wide sit at **8-aligned offsets**, 153 of 153.
  A mislabelled bit would have put some at `+0x24` or `+0x4C`.

Three rows whose room exactly equals their type's *inline* size also carry bit 1
(`PAnimationChannel +0x48`, `PAnimationSlotFilter +0x28`, `PEntity +0x8`). They are **not**
counter-examples: room is the distance to the next *registered* member, and unregistered members
leave slack that can coincidentally equal any size. The engine's own store instruction outranks a
coincidence in a derived table.

### Reconciliation: most of this was already on the subsystem page

`22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`
has recorded since **2026-09-02** that attribute bit 1 means "pointer", via a different function -
`FieldStorageWidth` at `0063C0C0` - along with the member record layout and bit 0. **That is the
fifth rediscovery this session and the cause is the same one every time: searching `_types` and
not the subsystem pages.** The rule is now: before deriving anything about a subsystem, grep that
subsystem's directory first. Nothing else has reduced this.

What survives as new, after reading that page:

1. **The in-memory path.** `FieldStorageWidth` reports a width *to a context*, and its pointer
   width is `ctx->vslot08()`, not a literal - so it cannot on its own settle what a live instance
   holds. The four accessors above operate on `instance + offset` and answer the in-memory
   question directly. The page's transcription said `return /* pointer width */ 8`; that has been
   **corrected on the page**.
2. **`classdesc[0xF4] == 0`**, proven, and load-bearing for all 680 offsets.
3. **The second clause of `FieldStorageWidth` is inert here.** Its condition is
   `(attrs>>1 & 1) | (~(attrs>>6) & isDynamic)`, where `isDynamic` is
   `rec->vslot08() != NULL && that->[0x5C] == 2`. All 680 registrations go through `00632960`,
   which installs member vtable `00D580B0`, whose slot `+0x08` is `005C5230: xor eax,eax ; ret` -
   **NULL**, so `isDynamic` is always 0. Only the derived member class can trigger it: ctor
   `00632A10`, vtable `00D58100`, slot `+0x08` = `0016D680: mov rax,rcx ; ret`, arg7 stored at
   `+0x5C` and compared against 2. No schema row uses that constructor. This had to be checked -
   had it been live, some of the 48 inline rows would be 8 bytes instead.

### What is not claimed

That bit 1 means "owning pointer". The branch proves the **slot is eight bytes wide and holds an
address**; whether the target is owned, shared, or a weak handle is a lifetime question this
evidence does not touch, and no row asserts it. **Attrs bits 3 (`0x08`) and 4 (`0x10`) have
since been answered, and the answer is a null**: nothing in the image reads them. Four
instruments over the 1,206 bodies that handle a member record — direct immediate tests at
`+0x28`/`+0x20`, the same through a tracked register, every short function in the image that
returns the word, and any shift by 3/4 or mask of `0x08`/`0x10`/`0x18` — return zero real hits
while finding bit 0 and bit 1, which are known to be consumed. The one apparent hit
(`005CA79E cmp ebx, 8`) is a loop count, and the `0x1F` sites are bit-31 sign manipulation, not
a low-five-bit mask. The word is never stored outside `+0x28` anywhere in the reflection block,
so it does not reach a file image either. The engine publishes a getter for bit 1
(`0063CB50: mov eax,[rcx+0x28]; shr eax,1; and eax,1; ret`) and **none** for bits 3–4. They are
registration-time metadata the runtime carries and ignores. Evidence and the limits of the claim
are in the subsystem page, section 13. **No width, offset or extent in this store depends on
them.**

### Result

201 widths applied — 153 at 8 bytes, 48 inline. Because the earlier gap rows were generated while
these fields occupied nothing, **every one of the 105 touched types had its generated gap rows
deleted and recomputed**: 308 stale rows out, 142 correct ones in. A type carrying any span row
the pipeline did not generate is refused outright rather than silently rewritten; that guard fired
on the first run and was the reason a second marker had to be recognised.

**Zero-width rows: 269 → 201 → 0.** Store: 274 sized types, **0 overlapping rows, 0 sum
mismatches, 0 dangling references, 0 storage-class failures.**

---

## The 242 gap rows that said NO LIFETIME VERDICT now say what the engine does

When the 162 Phyre extents were applied, the declared gap rows they required were given an
explicit denial rather than a guess: *"engine-allocated objects whose allocation paths have not
been read individually, so the row is deliberately left outstanding."* That was the right call at
the time and it was not a placeholder to be quietly upgraded — it was a claim that the work had
not been done. The work has now been done, and the denial was hiding a better answer than
expected.

**The bytes are copied, not left.** `PCluster::create` (`0063A990`) takes storage from a bump
allocator in the cluster arena (`00639750`) falling back to the `_aligned_malloc` wrapper
(`0017D260`) — **neither clears** — and then calls `0063C910` per instance, which does
`rdx = [descriptor+0xC0]; if (rdx) memcpy(instance, rdx, [descriptor+0x38])`. The length is the
**full instance size**, so every byte a member registration does not describe is a verbatim copy
of the class's *default instance*. That object is registered by the one-instruction setter
`0063DC80` (384 call sites); of 246 class descriptors, **173 had their constructor located and all
173 register one, every pointer in the `.bss` part of `.data`** — zero-filled by the loader, then
written by the class's static constructor at startup.

So a gap span is **deterministic and identical for every instance of its class**. That is the
verdict 236 rows over 138 types now carry.

**What the rows deliberately still refuse to say is that the value is zero.** An unregistered
byte is not an uninitialised one — Phyre registers what it exposes to serialisation, so a private
member the constructor sets is exactly the kind of byte that shows up here as a gap. And `.bss`
has no raw bytes, so no static reading can settle it. That is routed as
`OPUS-REQ-ASTRA-PHYRE-DEFAULT-INSTANCE-BYTES` — one post-startup read of the 173 tabulated
addresses, ~20 KB, which would also test the model from the runtime side, since the bytes at a
*registered* member's offset must agree with its registration.

Addresses: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/phyre-default-instances.tsv`.
Mechanism: section 14 of that directory's `member-registration-and-the-recovered-field-schema.md`.

**Lifetime coverage of declared spans: 306/548 → 542/548 (98.9 %).** The 6 outstanding are
`CD3D11_BLEND_DESC`, `CD3D11_DEPTH_STENCIL_DESC`, `CD3D11_RASTERIZER_DESC` and
`D3D11_RENDER_TARGET_BLEND_DESC` — Direct3D's own structures, with no Phyre class descriptor, so
none of this applies to them and they keep the denial honestly.

A note on how this was found, because the route matters. The question was approached as "read 142
allocation paths" and that was the wrong shape: the first useful measurement was that **Phyre class
descriptors have no instance-creation virtual at all** — only 3 and 4 of 246 descriptor vtables
reach an allocator from any of their first 20 slots. That negative is what redirected the search
to `PCluster::create`, and the engine's own error string
(*"Class '%s' has no default constructor and cannot be allocated with PCluster::create()"*) named
the API outright.

### Both creation routes are now answered, and neither leaves garbage

Section 14's verdict covered objects made by `PCluster::create`. The other route - an object that
arrives by **loading a cluster** - was explicitly disclaimed there rather than assumed, and has
now been read.

The unpack `0059E070` -> `0059E300`:

* **never re-initialises an object** - neither it nor anything it reaches within three call levels
  calls `0063C910` (the default-instance memcpy) or `PCluster::create`, so a loaded object does
  *not* get the class default;
* **its memsets do not touch object storage** - all three clear the per-list bookkeeping pointer
  arrays at `[cluster+0x28]`, `instanceListCount * 8` bytes each;
* **sizes objects at full instance width** - `0059D6A0` computes `descriptor[0x38] * m_count` per
  instance list, plus `m_arraysSize` and `m_pointersInArraysCount * 8`, aligned by
  `descriptor[0x3C]`, with a `descriptor+0xFC` bit 2 branch for when the file's `m_objectsSize`
  differs from the runtime size.

The only writes into a loaded object afterwards are the three fixup appliers (`0059C250` array,
`0059C700` pointer, `0059CE30` pointer-array) patching pointer-sized slots.

So the full answer for a Phyre declared gap:

| route | where the gap bytes come from |
|---|---|
| `PCluster::create` | a copy of the class's static default instance in `.bss` |
| cluster load | the bytes authored in the cluster file |

**Neither route zeroes the span and neither leaves heap residue.** For a reconstruction that is
the load-bearing fact: these bytes are always somebody's authored value, never garbage - which is
why the rows say *deterministic* and still refuse to say *zero*.

**Stated limit, carried on all 236 rows:** the read of the objects blob out of the stream into the
arena has not been traced instruction by instruction. The load-side claim rests on the absence of
re-initialisation, the memsets being accounted for, and the full-width sizing - enough to rule out
"zeroed" and "undefined" and to place the provenance in the file, not enough to describe the
copy's mechanics.

---

## The pointer detector was missing the commonest pointer idiom in the engine

`infer_field_type.py` reads *representation* off the access instructions — float, vector,
pointer, signed, unsigned, bitfield — and raises a row from `DISCOVERED` to `TYPE RESOLVED`
without claiming a meaning. Run against `ManagerSingleton0209BE80` it found **2 candidates out of
16 weak rows**, which was the tool being wrong rather than the type being obscure.

Its pointer test asked: *is the loaded value later used as a memory base **in the same body**?*
That proves a dereference, and it is the strongest evidence available — but it misses the idiom
this engine uses most. `+0x10FC0` has fifteen accesses and nearly every read is

```
mov rcx, qword ptr [obj + 0x10FC0]
call <something>
```

The value is **passed**, not dereferenced locally, so the test saw nothing. The same was true of
`+0x10F40`, `+0x10F50`, `+0x10F88` and `+0x10FB8` — all of them null-checked with
`cmp qword ptr [field], 0` and nulled with `mov qword ptr [field], 0`, which is about as
pointer-shaped as code gets.

**The fix follows the value one call level.** When the loaded value is still in an argument
register at a direct call, the callee is asked whether that parameter is dereferenced before the
register is written or another call happens. That converts "it was passed somewhere" into "it was
dereferenced there" — the same proof, one frame out — and the citation records which, `here` or
`callee XXXXXXXX`, rather than blurring them.

Verified end to end on `+0x10F40`: `0028F387 mov rcx,[rcx+0x10F40]` → `call 003F30A0`, and
`003F30A0` does `test rcx,rcx` then `mov rbx, qword ptr [rcx+0x70]`. A real dereference of the
incoming parameter.

**The control that matters passed.** The original defect this tool was built around was treating
`add rcx, [field]` whose sum becomes a base as proof of a pointer — caught because
`LegacyPs2GsTextureContext` has three rows the store itself names `addendXXXX`. After the change
those three still read **`addrterm`, not `pointer`**. The looser reach did not loosen the verdict.
That control now travels with the sweep, so any future change that reintroduces the defect fails
visibly.

`ManagerSingleton0209BE80` went 2 → 5 candidates, three of them pointers. The lesson is the one
already in this file about trackers: **a detector that reports far less than the data obviously
contains is a broken detector, not a quiet dataset.**

### What this instrument cannot reach

Of the **155 types** holding the 378 weak non-span rows, only **46 declare a route** — and a
route is what makes a census possible, which is what the reader needs. The other 109 types are
not blocked on inference at all; they are blocked on **route discovery**, which is a different
and prior piece of OPUS work. Recording that here so the residual is not misread as "the reader
tried and failed" when for most of it the reader was never able to run.

### The trap those widths left behind, and a stale column

Applying the widths created a row shape that is correct and misleading at the same time:

```
PAnimatableComponent  +0x020  size 8  ctype PAnimation::VPAnimationSet
```

Both fields are right — the slot is 8 bytes, and `VPAnimationSet` is the engine's own spelling of
the member's type — but read together they invite exactly the wrong conclusion: that
`VPAnimationSet` is an 8-byte type. It is not. The slot is 8 bytes *because attribute bit 1 is
set*, and the named type is the **pointed-to** type. This is the identical confusion that refuted
13 of 23 candidates when widths were first attempted by the ctype rule, so leaving it unstated in
the row would have let a reconstruction walk into a trap the store already knew about.

The `ctype` is **not** rewritten — the store records engine spellings. The `meaning` column, empty
on every one of these rows, now carries the ABI fact: **153 rows** say the slot is an 8-byte
reference to the named type and must not be read as that type being 8 bytes; **46** say the slot
holds the type inline at its full width. Each cites the branch (`0063C4A0` → type-vtable `+0x28`
storing one qword, versus `+0x18` copying the value).

Separately, all **199** of these rows still said `confidence = UNKNOWN`. That was correct while
their size was 0 and stale the moment the width was measured — an omission in the width pass,
which updated `readiness` and not `confidence`. They are now `HIGH`, the same tier as the 328
sibling reflection rows whose width came from a C primitive; these widths come from reading the
engine's dispatch branch, which is not weaker evidence than that.

This moves 199 rows out of the "weak" count and **that is not why it was done.** The rows were
never weak in readiness — all 199 already said `TYPE RESOLVED` — they were weak in a column I
failed to update. Correcting a stale field is legitimate; relabelling to move a number is not,
and the distinction here is that the evidence column already contained the measurement.

**Weak non-span rows: 378 → 179.**

### And the sweep that measured its own gap instead of the data

Running the improved reader over all 46 routed types returned **"no census" for 38 of them**.
That was not 38 types nothing touches — `gen_ptr_census_depth1.py` handles `PTR` and `FN` only,
while the route grammar also has `ARRAY`, `PARRAY`, `SLOTPTR`, `EMBED`, `CHAIN`, `RELOFF`,
`STATIC` and `DYNAMIC`, and the kit has **separate generators** for several of them. A driver
that calls one generator for every route kind measures the driver.

The same failure shape as the pointer detector, an hour apart, which is worth stating as a rule:
**when a sweep reports that most of its population has no data, suspect the sweep.** The rebuilt
driver dispatches on the route's leading keyword and reports `CHAIN`/`RELOFF`/`STATIC`/`DYNAMIC`
as **unsupported by kind** rather than empty — because "nothing accesses this" and "no tool for
this route kind exists" are different facts and only one of them is about the engine.

### A kit defect that produced empty files while reporting success

With the dispatch fixed, the sweep still returned **0 candidates for 25 of 27 types**. Suspecting
the sweep again was right: `gen_embed_census_depth1.py` was **crashing in its TSV writer**.

```
NameError: name 'parent' is not defined
```

The route tuple unpacks to `slot, emb_off, size, chain, stride, count`; the writer referenced a
`parent` that never existed. The failure shape is the dangerous one:

* the crash is **after** the summary print, so the console shows the accesses being found —
  `ManagerSub0209BE80_8FA0` printed *"TOTAL: 8 access(es) at 4 offset(s), functions
  contributing: 5"* and its eight instructions;
* the writer is guarded by `if a.out and out:`, so the crash only happens **when `--out` is
  given**. Interactive use never hit it.

So a tool that worked perfectly by hand produced a **0-row file every time it was driven by a
script**, and the driver dutifully reported "0 candidates" for every EMBED type. A tool that says
it found something and writes nothing is worse than one that fails loudly.

**Checked for contamination rather than assumed:** because the crash needs `--out`, and because
no field row in the store cites an `embed-d1` census in its evidence (0 matches for `embed-d1`
across `fields.tsv`), no earlier conclusion rests on a truncated embed census. The defect cost
this sweep, not the record.

Fixed to write `slot`, formatted as the summary line already formats it.

---

## The `+0xF4` claim was false, and the check that would have caught it already existed

Earlier today this file and section 12 of the member-registration page asserted that
`classdesc+0xF4` is zero, and used it to conclude that all 680 recorded member offsets are true
in-instance offsets. **It is not zero.**

The evidence was a sweep of every write to displacement `0xF4` in `.text` — **filtered to the
`mov` family**. A running sum uses `add`, and `0063E410` is a running sum: it zeroes `+0xF4` and
then walks the parent chain doing `add dword [rdx+0xF4], [rax+0xF0]`, stopping at the root
descriptor `02CF8270`. `+0xF0` is arg7 of the descriptor constructor, and of the calls to
`00632D80`/`00632C90`, **298 pass 0 but 16 pass 8**, one passes 1, one passes -2, and 69 pass a
register.

Resolved per class: `+0xF4` is `0` for 126, **`0x8` for 27** — `PNode`, `PAnimatableComponent`,
`PAtmosphericsBase`, `PDeferredLightingBase`, `PPhysicsShapeBase`, the `PInputSource*` family and
others — and unresolved for 26.

**It was already written down.** `PCD-5` in `CONTRACT-phyre-class-descriptor.md`, closed by FABLE
on 2026-09-14, describes `0063E410` accumulating `+0xF4` and `+0xF8` down the parent chain. That
is the **sixth** rediscovery-or-collision with the subsystem directory this session, and the first
one where not reading it produced a *false published claim* rather than duplicated effort. The
rule stated earlier — grep the subsystem directory before deriving anything about a subsystem —
was the right rule and I did not follow it.

### Scope of the damage, stated exactly

* **Reopened** as `OPUS-PHYRE-F4-OFFSET-ADJUSTMENT`: whether recorded offsets are in-instance
  offsets for the 27 classes with `+0xF4 = 8` and the 26 unresolved. The accessors compute
  `instance + (member.offset - classdesc[0xF4])`, so they differ by 8 **unless** the pointer the
  accessors receive is itself offset by 8 — plausible, since `0063C910` makes a *separate*
  adjustment using `+0xF8` and two compensating adjustments would cancel. Not determined, not
  guessed.
* **Unaffected: all 201 widths.** The width comes from which handler the attribute bit selects
  and how many bytes it stores; `+0xF4` appears nowhere in that reasoning. Every one of the 201
  rows now carries the correction inline and says the width is unaffected.
* **Unaffected:** the instance sizes, the default-instance mechanism, the cluster-load findings.
  None of them reads `+0xF4`.

### …and resolved: the offsets were right, the reasoning was not

The reopened question is closed, and the original conclusion survives on different evidence.

`0063E410` computes `+0xF4` as a plain sum of `+0xF0` down the parent chain and `+0xF8` as the
same sum with each term clamped at zero. Only one call in the image passes a negative `+0xF0`, so
across all **153 classes where both resolve, `+0xF4 == +0xF8`, zero differences**. The four
accessors subtract `+0xF4`; the per-instance initialiser `0063C910` subtracts `+0xF8`. Equal
values mean **both resolve a runtime object pointer to the same layout base**, `pointer − F4`.

And the offsets are measured from that base, not from the object pointer:

* all 27 classes with `F4 = 8` have every recorded offset inside `[0, instanceSize)`;
* **`PNode` has a member at offset `+0x0`** — were the offsets object-pointer-relative and in need
  of −8, its first member would sit 8 bytes *before* the object.

**No field row needs its offset adjusted.** The only consequence for a reconstruction is that for
those 27 classes a runtime object pointer is `layoutBase + 8`, so a live pointer converts to a
field address as `(pointer − 8) + offset`.

The lesson is not the one I expected. A false premise carried a true conclusion for most of a
session because the conclusion was never tested on its own — it was inherited. What settled it
was a property of the **data** (`PNode`'s `+0x0` member; offsets fitting the declared extents),
available the whole time and costing a minute. **When a conclusion rests on a single premise,
test the conclusion directly too** — otherwise the day the premise falls, 201 rows fall with it.

### The inference line is exhausted, and the residual is now measured rather than guessed

With the dispatch fixed and the EMBED writer repaired, the sweep ran properly over 38 routed
types and produced **13 candidates, of which 8 were accepted**:

* three **pointers** in `ManagerSingleton0209BE80` (`+0x10F40`, `+0x10F88`, `+0x10FC0`), each
  loaded into an argument register and dereferenced inside the callee;
* two **addrterms** in `LegacyPs2GsTextureContext` (`+0x188`, `+0x1A0`) — terms in an address,
  explicitly *not* proven pointers, matching the names the store already gave them;
* three **bitfields** (`ManagerSub0209BE80_57E0 +0x249C` and `+0xC4`, `ManagerSub0209BE80_8FA0
  +0x10FA`).

**Five were refused, and the refusals are the point.** One `unsigned` verdict rested on
`movzx eax, word ptr [field]` against a **four**-byte field — a zero-extending load of the low
half says what one reader does with 16 bits, not that the 32-bit field is unsigned. Four were
single-access; the tool flags an anecdote, and a flag is a reason not to accept, not a reason to.

**One name was refuted by its own accesses.** `ManagerSub0209BE80_57E0 +0x249C` was named
`counter7C7C`, and a counter is arithmetic. Its eighteen accesses contain no arithmetic at all —
`or 8`, `or 1`, `or 4`, `and 0xFFFFFFF7`, `and 0xFFFFFFFE`, `and 0xFFFFFFFB`, `and 0xFFFFFFEF`,
`test 1`, `test 4`, `test 0x10`, an `xor` toggle and a zero reset. Renamed `bits7C7C`.

#### Why so few, measured

Over the swept types, **124 weak rows**, and of those only **31 (25 %) have any access at all in
their type's census**. 93 have none.

That is not thin censuses. Several types have rich ones that simply do not touch the offsets in
question:

| type | weak rows | of those, covered | census rows |
|---|---|---|---|
| `GameSettingConfig` | 1 | **0** | 154 |
| `CharacterRenderSystemTail` | 1 | **0** | 143 |
| `ActorManagerSlot` | 1 | **0** | 113 |
| `SaveImageHeader` | 2 | **0** | 91 |
| `ManagerSingleton0209BE80` | 13 | 13 | 276 |

Where the census reaches a field, inference works — `ManagerSingleton0209BE80` is 13 of 13
covered. Where it does not, the field is not obscure, it is **untouched by any statically
reachable access**, which is a different problem and a different evidence class. Those rows were
found by other means in the first place (names like `ctorZero*` come from a constructor sweep),
and `member_reach_scan` confirms the limit is real rather than a tool gap: on
`BootSingleton01F7F598` it reports *no indirect handoffs and every escape followed to a dead end*
— the closure is **complete** at 5 accesses over 3 offsets, for a `0xDD8` singleton with 14 weak
rows.

**So the next step for these 93 rows is not a better reader.** It is runtime observation or the
writer that created them, and saying so is more useful than another pass that finds nothing.

---

## Reading a field from the site its own evidence cites

The census reader is blocked wherever a route does not reach a field, and that is most of the
residual. But those fields are not undiscovered — something found them, and the row usually says
what: **122 of 140 unreached weak rows carry a hex address in their evidence column.** An address
is an instruction, and an instruction states a width and often a representation. Reading it needs
no route, no census and no closure.

`infer_from_cited_site.py` does that. It **checks the citation before believing it** — the cited
instruction must touch the row's own offset — and classifies only what survives.

**14 rows applied**, every one a full-width access matching the declared size:

* `ManagerSub0209BE80_00A0 +0x0/+0x4/+0x8/+0xC` → **float**. Four consecutive `movss` stores in
  one basic block (`003F8E51/63/6E/73`), so the four rows corroborate each other rather than
  being four anecdotes. `rdi` is confirmed to be the sub-object and not the parent because the
  same block touches `[rdi+0x52C6]`, inside this type's `0x52E0` extent.
* `ManagerSub0209BE80_7EA0 +0x20` (`movss`) and `+0x70` (`addss`) → **float**; `+0x2A`
  (`movzx` of the whole byte) → **unsigned**; `+0x74` (`test byte,1`) → **bitfield**.
* `ManagerSub0209BE80_A0D0 +0x984`, `ManagerSub0209BE80_8FA0 +0x103E` → **bitfield**.
* `ManagerSub0209BE80_57E0ArrayRecord +0x0`, `ImageBackedStateBlock +0x18` → **vector**
  (`movups xmmword`, covering the whole 16-byte extent).
* `ManagerSingleton0209BE80 +0x10FA3`, `ImageBackedStateBlock +0x6` → **unsigned**.

**Weak named fields: 134 → 120.**

### Three tool defects, found by disbelieving the tool

1. **A `lea` is not an access.** Capstone reports an operand size for a `lea`'s memory operand,
   and the width check took it as the field's width — reporting `addrTaken26AE`, a **1-byte**
   field whose only citation is `lea r14, [rsi+0x26AE]`, as "declared 1, accessed qword". A `lea`
   proves the address is taken and states no width. Three of four width disagreements were this.
2. **Embedded types are accessed parent-relative.** A row of `ManagerSub0209BE80_57E0` at
   `+0x192` is reached as `cmp word ptr [rcx+0x5972], 0`, because the sub-object sits at
   `+0x57E0` and the compiler folded the displacements — the row names already carry the folded
   value (`count5972`). Checking only the sub-object offset called **12 correct citations
   mismatches**. Resolving the EMBED chain from `types.tsv` and accepting either dropped it to 5.
3. **"Mismatch" was three different things.** The first version called every non-matching
   citation a defect. It is not: 18 rows cite a **function** (`SaveImageHeader` cites `002EF640`,
   its own FN route base; the D3D11 rows cite `0063C4A0`, the shared Phyre accessor) and 10 cite
   a **`lea` at their own offset** — which is exactly what names like `subAddr0342` mean. Both
   are correct citations that simply state no width.

### The citation audit, which is a store-quality result in its own right

Of the 120 weak named rows: **10** cite nothing, **10** cite a `lea` at their own offset, **18**
cite a function, **5** cite an instruction at a genuinely different offset, and the rest verify.
Five rows worth chasing out of 120 is a good evidence column, and it is now measured rather than
assumed.

### And a defect in my own metric

The residual I have been quoting was wrong. The filter for "non-span" rows matched
`^(unobservedSpan|unread)` — but the store also uses **`unobservedTail`**, and 37 of those were
being counted as named fields. The true figures are **2,658 real named fields**, of which **120**
are weak, and **611 span-like rows**, of which **605 (99.0 %)** carry a lifetime verdict. Every
earlier "weak non-span" number in this file was inflated by those 37.

### The citation audit closed: one questionable row in 120

Chasing the five citations the matcher could not confirm found **no defect in four of them** —
each is a correct citation of a *different kind* of evidence, which the tool now names rather
than flags:

* `BattleResultRecord +0x144` cites `mov r8d, 0x148` — and `0x148` is **exactly this type's
  size**. The row was found in a bulk copy, and the citation is the copy's length.
* `InputBindingRecord +0x140` cites `add rsi, 0x15c` — and `0x15C` is **exactly this type's
  stride**. The citation is the array walk.
* `BattleStatsRecord +0x5C` cites `mov dword ptr [r14 + r12 - 0x60], eax` — an **indexed** access
  whose displacement alone is not comparable to a field offset.
* `SpawnRecord +0x70` cites `movups xmmword ptr [rcx - 0x10], xmm1` — a **negative**
  displacement, reached through a running pointer.

**The fifth is a real finding.** `ImageBackedStateBlock +0x8 vector0008` cited `002DDE76`, which
is `add rax, 8` — a base adjustment, not an access. So the width was not read from the cited
instruction, and the supporting clause *"0x08 + 0x10 == 0x18"* argues a width from the **next
offset**, which this store's convention explicitly forbids.

The real writes are four instructions later and are **rip-relative absolute**, which is precisely
why a displacement matcher cannot see them:

```
002DDE81  mov    qword ptr [0215E6E0], rax      ; +0x00 as EIGHT bytes
002DDE88  movups xmmword ptr [0215E6E8], xmm0   ; +0x08, 16 bytes
002DDE9F  movups xmmword ptr [0215E6F8], xmm1   ; +0x18, 16 bytes
002DDE97  movsd  qword ptr [0215E708], xmm0     ; +0x28, 8 bytes
```

Relative to `0215E6E0` those match `vector0008` (16), `vector0018` (16) and `qword28` (8)
**exactly** — but the type's declared route is `PTR 0x020927C0`, a different slot, and the first
write puts **eight** bytes at `+0x0` where the store declares a four-byte `dword0000`. So either
`0215E6E0` is a second instance this type has no route to and `dword0000` is wrong, or it is a
look-alike and `vector0008` is citing the wrong object. Raised as
`OPUS-IMAGEBACKEDSTATEBLOCK-0215E6E0` and **not guessed**; the 16-byte width is left standing
because two independent `movups` at matching offsets support it, with the row flagged so nobody
mistakes it for something read at `002DDE76`.

**Result: of 120 weak named rows, 10 cite nothing, 110 cite something that checks out, and one
carries a flagged open question.** That is the evidence column measured rather than trusted.

### …and the one open question closed: the citation was wrong, the width was right

`002536A0` turns out to be `ImageBackedStateBlock`'s own getter — `mov rax, qword ptr [020927C0];
ret`. That settles both halves of the question at once.

**`0215E6E0` is not an instance of the type.** In `002DDE60` the getter is called, **8 is added to
the instance pointer, and that address is published**: `mov qword ptr [0215E6E0], rax`. So
`0215E6E0` is a separate structure holding a pointer to `instance+8` in its own `+0x0`, and the
`movups` at `0215E6E8`/`0215E6F8` write *its* fields. `dword0000` was never contradicted and no
route is missing. The concern is **withdrawn rather than confirmed**.

**And `vector0008`'s 16-byte width is right** — it was cited to the wrong instruction. The real
support is in `FUN_00394130`, which calls the same getter and then does:

```
0039422F  call   002536A0                       ; rax = the instance
0039423B  movups xmmword ptr [rax + 8],   xmm0   ; 16 bytes at instance+0x08
00394246  movups xmmword ptr [rax + 0x18], xmm1  ; 16 bytes at instance+0x18
00394252  movsd  qword   ptr [rax + 0x28], xmm0  ;  8 bytes at instance+0x28
```

— a 16-byte store at `instance+0x8` **through the type's declared route**, which is exactly the
evidence the row needed and never had. All three are copied from another object at
`rbx+0xC8/+0xD8/+0xE8`, a `0x28`-byte block transfer. Citation corrected, row raised to
`TYPE RESOLVED`/`HIGH`. What remains true of the original citation is only that the field's
**address is taken** at `002DDE76`.

The pattern is worth keeping: **a row can hold a correct fact on wrong evidence.** Both the
`+0xF4` claim and this one were true conclusions resting on citations that did not support them,
and in both cases the right response was to find the real support rather than either trust the
row or delete it.

---

## The residual, as a taxonomy instead of a number

The residual figure moved three times in one day — 378, then 134, then 120 — and every move was a
**measurement error corrected**, not progress. A number that unreliable should not be the way
this frontier is described, so `classify_weak_rows.py` replaces it with a taxonomy, because
"weak" was hiding five situations that need five different things:

| bucket | rows | what it actually is |
|---|---|---|
| **READABLE** | **69** | real accesses exist; a representation can be read. **This is the outstanding work.** |
| ADDRESS TAKEN ONLY | 10 | the only citation is a `lea` at this offset — the address escapes, so the width needs the callee |
| MECHANISM ONLY | 14 | the citation is a function (an FN route base, a shared accessor) — real evidence about ownership, silent about layout |
| MEASURED ABSENCE | 13 | the evidence says *"no access at this displacement in the family"*. **A result, not a task** — the bytes are proven untouched by the instrument that looked |
| OTHER EVIDENCE KIND | 3 | evidenced by a bulk-copy length, a stride, or an indexed access |
| DECLARED GAP | 1 | exists to satisfy the sum invariant; its name is cosmetic |
| NO CITATION | 2 | genuinely uncited |

Counting the 13 measured absences and the declared gap as outstanding work overstates the
residual by 12 %; they are the *answer* "nothing reads these bytes", which is exactly what a
reconstruction needs to know.

### Seven pointers raised from named to proven

Extending the cited-site reader with the same one-call-level dereference proof the census reader
uses — seeded from the cited site rather than from a census row, so it works where no route
reaches — found seven:

```
ManagerSub0209BE80_00A0 +0x52A0   mov rbx,[rdi+0x52A0] ; test rbx,rbx ; je ; movzx eax,[rbx+0x23C]
ManagerSub0209BE80_5380 +0x420/+0x428/+0x430
ManagerSub0209BE80_8FA0 +0x1030/+0x1058/+0x1078
```

Every one was already *named* `ptrXXXX` — the store believed they were pointers on the shape of
the access. They now carry a **dereference**, which is the difference between `DISCOVERED` and
`TYPE RESOLVED`.

**And the tool's "one site — anecdote" flag does not apply to a pointer verdict.** That flag
guards against a second site contradicting an idiom: one `movzx` says a reader zero-extends, and
a `movsx` elsewhere would refute it. A dereference is different in kind — if an 8-byte value
loaded from a field is used as a memory base, the field held an address, and no second site can
make that false. The flag is right for float, bitfield, signed and unsigned, and wrong for
pointer.

Still not claimed: **ownership**. The slot holds an address; whether the target is owned, shared
or merely observed is a lifetime question none of these citations touch.

**Weak named fields: 120 → 112, of which 69 are the real frontier.**

---

## Where static ABI reading runs out, measured

Three instruments have now been pointed at the READABLE rows — the census reader, the cited-site
reader, and a dereference proof extended to follow a value through callee prologues to depth 2 —
and the yield fell to near zero. Before building a fourth, `profile_readable.py` asks what is
actually in them, because the reason a row resists decides whether any instrument could settle
it.

| what the instructions do | rows | can static reading settle it? |
|---|---|---|
| no census access, cited sites only | 69 | already characterised: the census-reach limit |
| **plain move only** | **16** | **no.** Every access is `mov` in and out. The width is fixed; *no instruction that touches the field fixes its representation* |
| 8-byte plain move, value escapes | 6 | only with an unbounded chase — see below |
| compare-only (`cmp …, 0`) | 3 | no — liveness tests carry no representation |
| idiom present but reader refused | 2 | the refusals are deliberate (a partial read, a single site) |
| bit operations / arithmetic | 1 / 1 | partly |

### The depth-2 chase, and why it still fails on `ptr10F50`

The dereference proof was genuinely improved twice, and both fixes were real defects:

* **it must follow the parameter, not the register.** Callees park arguments in callee-saved
  registers first — `003FA600` opens `mov rbx,[r8+0x2490]; mov rbp, r9; mov r14, rdx; …` — so a
  scan watching only `r9` sees the copy and gives up;
* **try every argument register that carries the value, not one of them.** At the forwarding call
  in `003FA600` the carriers are `{r9, rbp, rdx}`: `r9` is the original parameter and stale,
  `rdx` is the live copy made at `003FA67D mov rdx, rbp`. Taking the first alphabetically took
  `r9` and proved nothing.

With both fixed it still does not crack `ptr10F50`, and the trail says why:
`obj+0x10F50 → r9 → 003FA600 → rbp → rdx → 003FBA80`, and `003FBA80` immediately reassigns `rbp`
as a **frame pointer** and does not visibly consume `rdx` early. **Pointer-ness for that row is
beyond a bounded, sound walk**, and the tool is right to refuse it. The control held throughout:
`LegacyPs2GsTextureContext`'s `addend*` rows still read `addrterm`, never `pointer`.

Four tool iterations for one row is the over-tooling trap, and stopping is the right call — the
row is already *named* `ptr10F50`; what was at stake was a readiness bump, not a layout fact.

### The 19 that are not OPUS's to answer

The 16 "plain move only" and 3 "compare-only" rows are **not waiting for a better tool**. Their
widths and offsets are settled and a reconstruction can already lay them out as opaque storage.
What is missing is what the value is *used for*, and if the purpose is known the representation
usually follows — an index is unsigned, a handle is opaque, a countdown is signed. That is
semantics, so they are routed as `OPUS-REQ-FABLE-REPRESENTATION-UNDECIDABLE-ROWS` rather than
left in the OPUS queue misrepresenting themselves as pending layout work.

**This is the honest edge of the static ABI frontier for this store**, and it is worth stating
plainly: of the original residual, what remains is 69 rows the census cannot reach, 19 that no
instruction can type, 10 whose address merely escapes, 14 evidenced only by a mechanism, 13
measured absences, and a handful of deliberate refusals.

---

## A route is a way in, not the only way in

`AL-8 +0x19` had no writer after four sweeps. A fifth — seeded from the type's declared route
`PARRAY 0x0208E690 stride=0x250`, over all 20 bodies that reference the pool and their one-hop
callees, across five instruction forms — also found none. **It was one step from being recorded
as an established absence.**

The writer exists. `BattleEnmity_UpdatePeriodicDecay` reaches the record through
**`BattleUnit + 0x6A0`**, not through the pool, and writes it through a taken address:

```
00321553  mov   rax, qword ptr [rcx + 0x6A0]   ; unit->pBkei
00321569  lea   rdi, [rax + 0x19]              ; the field's address
003215AC  mov   byte ptr [rdi], cl             ; the write, displacement ZERO
```

Two blind spots, and the first is the general one: **a census seeded from a type's route can
only ever speak for code that enters by that route.** Every absence claim resting on one inherits
that bound, and the store's absence claims do not say so.

### The alternate path was already in the store, and unusable

`BattleUnit +0x6A0` is named `spawnRecord` and its meaning reads *"the owning SpawnRecord
(0x250)"*. Its **ctype was `void*`**. So the pointer graph did not contain the edge, and nothing
that walks ctypes — a census generator, an absence gate, a reconstruction — could follow it. The
knowledge was present and inert.

`check_prose_only_edges.py` looks for exactly that shape: a pointer-sized field with an anonymous
ctype whose name or meaning names a declared type. It found **12 candidates**, and reviewing them
is the reason it writes nothing:

* **5 accepted** — `BattleUnit +0x6A0 → SpawnRecord*`, `BattleUnit +0x10 → ActorStorageRecord*`,
  `ActorStorageRecord +0x30 → BattleUnit*`, `RenderModelInstance +0xF8 →
  CharacterRenderRecord*`, `ManagerSub7FB0Record +0x0 → Widget*`.
* **7 refused** — a **function** pointer (`recordPoolAllocator`), two **interior** pointers into
  the same record, an unobserved span whose meaning mentions a type only to explain an inherited
  clear, two rows where the name appears solely in a *"REBASED from…"* note, and
  `LegacyPs2GsTextureContext +0x150`, which is one indirection away and was already ruled out
  earlier today.
* **2 of the 12 named the wrong target.** The scan matches the longest declared type name in the
  text: at `ActorStorageRecord +0x30` it proposed `ActorManagerSlot` when the prose says
  *"back-pointer to this actor **BattleUnit** pool slot"*, and at `ManagerSub7FB0Record +0x0` it
  proposed `MessageWindowRecord` when the prose says *"a **WIDGET** pointer"* and mentions the
  other type only because its destructor reaches the same free.

Seven of twelve wrong or inapplicable, and two of the five right ones pointing somewhere else —
that is a candidate generator, not a rewriter, and the docstring says so.

**Inbound-pointer graph: 31 → 35 types.** Seven prose-only candidates remain for a later pass.

### What this does not fix

The five edges make those paths followable. It does **not** retroactively validate any absence
claim in the store: each was measured with whatever seeding it had, and the ones seeded from a
route still only speak for that route. Re-testing them is a separate pass, and the honest reading
until then is that a field-level absence claim is bounded by its instrument's entry point — which
is what `AL-8 +0x19` cost four sweeps to demonstrate.

### Re-testing the absence claims, and writing their scope onto them

If a route-seeded census only speaks for code entering by that route, then every field-level
absence claim in the store carries a bound it never stated. There are **14**. They now say what
they cover.

**Two were testable and both hold.** `ImageBackedStateBlock` and `PersistentFlagPayload` are
**embedded** in `SavePayload` (at `+0x8000` and `+0x0`), so an access reaching them through the
parent is written with the *folded* displacement — `0x8004` and `0x1394` — which a census seeded
on the child's own route looks for as `+0x4` and `+0x1394` off a different base and structurally
cannot match. Both folded displacements swept image-wide: **zero access sites.** (The single
`+0x8000` hit is `lea ecx, [r9 + 0x8000]` in `BattleEncodedId_IsValidForClass` — a 32-bit `lea`
doing unrelated arithmetic, not the region.) Those two claims now cover both entry points.

**Twelve have no known second path**, and that is weaker than it sounds, so it is written as a
scope rather than a clean bill: nothing in the store points at `ChunkedSlotBankEntry`,
`ChunkedSlotEntry` or `RenderModelInstanceContainer` — no ctype names them, and, the check AL-8
taught, **no field row anywhere mentions them in prose either**. So no hidden edge of the kind
that made AL-8 unfindable is known to exist, and each row now says: *this absence speaks for code
entering by the declared route; no other entry point is known.*

That is the difference between "I could not find one" and "there is not one" — the distinction
`check_absence_claims.py` was built around for *address* claims, now applied to *field* claims,
which had no gate at all.

Store: 3,260 rows, 274 sized types, 0 overlaps, 0 sum mismatches, 0 zero-width; 609 spans, 602
(98.9 %) with a lifetime verdict.

---

## A control must be chosen to fail if the filter is wrong

An earlier self-audit (2026-09-15) concluded: *"never derive a universal claim from a printed
listing, because a listing is by construction the part that fit."* That remedy stands, and
nothing this session was caused by it. But this session produced a **larger class it does not
cover: predicate errors** — not misreading a truncation, but writing a filter that silently
excludes part of the population.

Five of them, all mine, all found by something other than the sweep that made them:

| the sweep | the predicate | what it excluded |
|---|---|---|
| "`classdesc+0xF4` is zero" | `mov`-family writes only | `0063E410` writes it with **`add`** — it is a running sum |
| the staleness sweep | `assigned_to == "OPUS"` | 22 READY OPUS tasks are **unassigned** |
| the weak-row filter | `^(unobservedSpan\|unread)` | the store also uses **`unobservedTail`** — 37 spans counted as fields |
| the cited-site width check | capstone's operand size | a **`lea`** reads nothing; its operand size is not a field width |
| the merge script | — | counted five enrichments and **wrote none** (mutated the row, appended the original line) |

**The split across the session is clean, and that is the useful part.** Every sweep carrying a
positive control *chosen to fail if the predicate were wrong* came out sound:

* the attrs bit-scan — controls bit 0 (owned-name) and bit 1, both known to be consumed;
* the pointer detector — control: `LegacyPs2Gs` `addend*` rows must stay `addrterm`, never
  `pointer`;
* `phyre_type_widths` — control: `unsigned int` = 4, `float` = 4;
* the step-body five-instrument sweep — control: slots 101 and 118, **known reached**.

**Four with such a control: four sound. Five without: five wrong.**

So the remedy generalises from *"do not eyeball a listing"* to: **a sweep's control must be
chosen to fail if the filter is wrong, not merely to confirm the tool runs.** A control that
exercises only the happy path is decoration.

The sharpest instance is the step-body sweep, where the control came back **negative for a
known-positive case**. That was more informative than any positive result: it proved the
instrument was measuring a *different entry path* than the claim it was testing, which redirected
the whole investigation to the premise that actually failed.

And the earlier audit's deeper point survives unchanged — *"every figure produced by an explicit
counter is right; the single figure produced by eyeballing printed rows is the one that was
wrong"* — because it is the same shape: **the error is never in the arithmetic, it is in what the
arithmetic was run over.**

### The second blind spot has a measured population, and it is 2,372 stores

The AL-8 miss had two causes. The first — *a census seeded from a type's route can only speak for
code that enters by that route* — is recorded above. **The second is the taken address, and it can
be counted.**

Any sweep keyed on a field's displacement is blind to a store through an address a `lea` already
consumed. `check_taken_address_writes.py` walks every body for `lea reg, [base + disp]` with a
struct-sized displacement followed by a `mov [reg], …` at displacement **zero**:

```
lea-taken field addresses written at displacement zero : 2372 sites
distinct displacements involved                        :  262
distinct functions                                     : 1667
of those, guarded by a CMOV like the control's         :   37
POSITIVE CONTROL - the AL-8 write at 003215AC          : FOUND
```

**Every displacement-keyed field sweep in this store is blind to those 2,372 stores**, and the
`SpawnRecord +0x19` case was one of them. The most-taken offsets are `+0x10` (486), `+0x08` (413)
and `+0x80` (226) — ordinary header fields, not exotica.

> **The number is a FLOOR.** The walk is intra-function and stops at a spill, so a taken address
> that leaves its body is not counted.

### The sweep's own control failed first, and the reason was an ABI error

The first run reported **1,966** sites and **did not find `003215AC`** — it missed the case it was
written for. Two mistakes, both mine, both about the calling convention:

- **It killed the chain at every `call`.** `RDI` is **callee-saved** in MS x64, and the AL-8
  address sits in `RDI` across `call 00307CE0`. A call cannot clobber it. Correcting this to kill
  only the *volatile* registers recovered **406 sites**.
- **It killed the chain at `cmove rdi, rsi`.** That is the null-guard idiom — the register still
  holds the taken address on the path where the store happens. 37 sites, including the control,
  reach their store through one.

**A sweep that assumed the ABI instead of applying it understated its own population by 17 %, and
silently.** The only reason this was caught is that the control was chosen to be a case the sweep
*must* find; a run without one would have published 1,966 and the conclusion would have looked the
same.

**This does not settle any individual absence claim** and none is reopened here. What it settles is
the size of the room: an absence claim made with a displacement-keyed instrument is missing a
population of 2,372 known stores unless it says how it handled them.

*(OPUS 2026-09-19, on `OPUS-FINDING-AL8-X19-A-FOURTH-BLIND-SPOT-AND-A-POPULATION-GAP`. The
instrument is in the kit; its control is the AL-8 store itself.)*

### Which of the store's own absence rows the blind spot could account for

The store asserts *no writer* for **28 field rows**. The 2,372-store population above splits them
cleanly, and the split is the actionable part:

| | rows | what it means |
|---|---:|---|
| at an offset where taken-address stores **do** occur | **17** | **a displacement sweep could not have settled these.** Their absence claim is under-evidenced |
| at an offset where **none** occur anywhere in the image | **11** | the blind spot cannot account for them; the absence stands **against this instrument** |

**The 17, most-exposed first** — the count is taken-address stores at that displacement anywhere in
the image:

| type | offset | field | stores at that offset |
|---|---|---|---:|
| `AiOrderRecord` | `+0x02` | `actionParameter` | 39 |
| `ManagerSub0209BE80_7EA0` | `+0x028` | `word7EC8` | 18 |
| `PostProcessParamContext` | `+0x024` | `padDword24` | 10 |
| `SaveImageHeader` | `+0x024` | `slotRosterEntries1to3` | 10 |
| `ManagerSub0209BE80_7EA0` | `+0x024` | `dword7EC4` | 10 |
| `CharacterRenderRecord` | `+0x270` | `externReadDword270` | 6 |
| `RenderModelInstance` | `+0x02C` | `padWord2C` | 6 |
| `ActorManagerSlot` | `+0x013` | `slotByte13` | 5 |
| `RenderModelInstance` | `+0x044` | `padBlock44` | 4 |
| `RenderModelInstance` | `+0x0B4` | `wordSlotB4` | 4 |
| `RenderModelInstance` | `+0x1F0` | `padBlock1F0` | 3 |
| `GameSettingConfig` | `+0x450` | `iniPath` | 2 |
| `PostProcessParamContext` | `+0x084` | `padDword84` | 2 |
| `ActorStorageRecord` | `+0x01C` | `flags1C` | 1 |
| `ActorStorageRecord` | `+0x0DC` | `stateWordDC` | 1 |
| `RenderModelInstance` | `+0x0BC` | `blockBC` | 1 |
| `BootSingleton01F7F598` | `+0x1C` | `bankSelectWord1C` | 1 |

> **THIS REFUTES NOTHING, AND NO ROW IS CHANGED BY IT.** *"A taken-address store exists at this
> displacement"* is not *"one of them writes this type"* — the base register's type is not resolved
> by the sweep, and `+0x024` is a common offset in many structures. **These are seventeen rows whose
> absence claim rests on an instrument that demonstrably cannot see a whole class of store**, which
> is a statement about the evidence, not about the field.

`AiOrderRecord +0x02` is worth naming: its row already says *"NEVER WRITTEN by the rebuild"* — a
claim **scoped to one writer**, which is the right shape and survives this unchanged. The rows most
exposed are the ones phrased as unqualified absence.

**The other 11** — `BattleUnit +0xE68`, `CharacterRenderRecord +0x3B8` and `+0x44C`,
`LegacyPs2GsDerivedSlotRecord +0x21`, `RenderModelInstance +0x0E2` and `+0x224`,
`ManagerSingleton0209BE80 +0xB240` and `+0x10F10`, `ManagerSub0209BE80_7EA0 +0x02A`,
`ManagerSub0209BE80_8FA0 +0x1048`, `BootSingleton01F7F598 +0xC34` — sit at displacements **no**
`lea`-taken store uses anywhere in the image. **Their absence is not explained by this blind spot**,
which is the strongest thing the instrument can say for a negative and is worth recording beside
the rows it cannot help.

*(OPUS 2026-09-19. Queued as `OPUS-RESIDUAL-SEVENTEEN-ABSENCE-ROWS-UNDER-A-BLIND-INSTRUMENT`.)*

### The span-propagation residue, classified — and one span resolved out of it

`check_span_propagation.py` asks a narrow question: *does the type's own page mention this span's
offset while the row cites nothing?* It reported **14 candidates**. They are not 14 propagation
failures, and the breakdown is more useful than the count.

**One was real and is now resolved.** `SecondaryContext +0x148` → **`movementBodyWeight`, f32**.
The page has said since 2026-09-11 that *"the context's `+0x148` is copied into the body as its
weight"* — true, and **unusable**, because it carried no address while its neighbours `+0x14F` and
`+0x151` were propagated with one. Three functions settle it, all reaching the context through the
actor's `+0xC0`:

```
00265950  GET  xmm0 = [ctx + 0x148]          ; 25 B; returns 0.0f on a null context
0026DACC  SET  movss [ctx + 0x148], xmm1
0026861A  PUSH movss [rcx + 8], xmm0         ; rcx = [ctx + 0x138], the movement body
0026DAFE  PUSH the same, from the setter
```

So the weight lives at **`body + 0x08`**, and the setter writes the context then re-pushes. Width
unchanged at 4, so the sum invariant is untouched; the store still reports **0 sum mismatches over
274 sized types and 0 zero-width rows.**

**The other 13 are four kinds of false positive, and each kind is worth recognising:**

| kind | rows | example |
|---|---:|---|
| **a stack displacement** | 1 | `MessageWindowRecord +0x1B8` — the page's hit is `[r11 - 0x1b8]` with `r11 = rsp`. Not a field offset at all |
| **the page RESTATING the gap** | 5 | `BattleUnit +0x120`/`+0xEB4` — *"So do `+0x120` (32 B) and the `+0xEB4` tail (156 B)"*; `SecondaryContext +0x150`/`+0x155`/`+0x17C` — an HTML comment listing untouched ranges. The page names the offset **to say it is unknown** |
| **an argument value, not an offset** | 1 | `CharacterRenderRecord +0x104` — `003E5AD0(record, 0x104)`, where `0x104` is a bone id |
| **the page documenting a COMPLETED propagation** | 1 | `BootSingleton01F7F598 +0xCDC` — the page's own was/now table (*"52 B → 6 declared offsets, 32 B"*). The store already carries those six rows; the checker is reading the record of the fix as evidence of the gap |

**Five remain genuinely open**: `ActorStorageRecord +0x11C`, `BattleSystemState +0x5AA2`,
`CharacterRenderRecord +0x458` and `+0x3D5`, `MessageWindowRecord +0x3C1`. Each has a page sentence
that plausibly covers the span and no citation in the row — the same shape `+0x148` had.

> **The checker is right to be noisy.** Four of its five false-positive kinds are un-fixable
> lexically — a page cannot be stopped from mentioning an offset in order to call it unknown — and
> the one that could be filtered (the stack displacement) would cost a regex that might also drop a
> real field. **14 candidates cost one afternoon and yielded one resolved span and five leads**,
> which is the right trade for a checker whose alternative is not noticing.

*(OPUS 2026-09-19, closing `OPUS-SPAN-PROPAGATION-STORE-VS-ITS-OWN-PAGES`. The residue is explained
rather than driven to zero, which is what that task's completion condition asked for.)*


## Every STATIC and PTR route checked against the bytes (2026-09-19, OPUS)

`STATIC 0xADDR` means the instance is **at** that address and `gen_static_census.py` reads `size`
bytes there. `PTR 0xADDR` means the instance is at `*(ADDR)`. Confuse the two and the census reads
the wrong memory — and for a heap singleton whose slot sits in the `.bss` tail it reads zeros,
reports the type as empty, and prints nothing that says the base was wrong.

Nothing had ever checked the two apart from the prose. `check_static_vs_ptr_routes.py` now does it
from the instruction stream: a real static object is touched at **interior** displacements at
**mixed widths**; a pointer slot is touched at its base only, always eight bytes wide.

### The result over all nineteen routes

| route | type | addr | targets | interior | widths | shape |
|---|---|---|---|---|---|---|
| `PTR` | eleven slots, incl. `ManagerSingleton0209BE80`, `BattleSystemState`, `GameSettingConfig` | — | 1 each | 0 | 8 | pointer slot |
| `PTR` | `RenderModelInstanceContainer` | `022C7CD0` | 0 | 0 | — | not named by any instruction |
| `STATIC` | `BattleFormulaScratch` | `02AEDFB8` | 44 | 43 | 1,2,4 | object |
| `STATIC` | `Mt19937State` | `02EB3870` | 8 | 7 | 4,8 | object |
| `STATIC` | `PartyReadMachineRecord` | `02EBF3D0`, `02EBF3F0` | 9 | 8 | 1,4,8 | object |
| `STATIC` | `SharedGameplayLcgState` | `022C256C` | 1 | 0 | 4 | scalar static |
| `STATIC` | `RenderModelInstanceContainer` | `022C7020` | 0 | 0 | — | not named by any instruction |

Both controls fire — `Mt19937State` reads as an object, `ManagerSingleton0209BE80` as a slot — and
**one row was wrong**.

### `EffectPresetSingleton01F82C80`: `STATIC` corrected to `PTR`

The row's route said `STATIC 0x01F82C80` while the row's own instance cell said
*"`*(void**)0x01F82C80` — a lazily created heap singleton"*. The disassembly settles it without any
census at all: `001D62F7` calls the malloc thunk with `ecx = 0xF778`, **all eleven field writes at
`001D6306`–`001D6341` go through `rax`, the allocation return**, and `rax` only reaches `01F82C80`
at `001D6347`, after them. The eleven offsets are offsets into the heap object. The field rows are
unaffected and correct as written; only the route changes.

The extent is independently impossible: `01F82C80..01F82D28` is a dense run of **nineteen separate
eight-byte globals** — `C88, C90, C98, CA0, CA8, CB0, CB8, CC0, CD0, CD8, CE0, CF0, CF8, D00, D08,
D10, D18, D20` — and `GameSettingConfig`'s own route address `0x01F82D20` lies `0xA0` bytes inside
the `0xF778` extent the row claimed.

> **The tool's first run passed both controls and still got this row wrong**, reporting `OBJECT
> SHAPE` on 185 targets. The discriminator was fine; the **window** was not. A wrong base makes the
> extent an arbitrary stretch of memory and every unrelated global inside it counts as interior.
> Recorded as `EVIDENCE-STANDARD` addendum bx: *a control tests the discriminator, not the window
> it is applied to.* Two guards followed — a `STATIC` extent containing another declared route
> address now has its verdict **withheld**, and `NO REFERENCES` was renamed
> `NOT NAMED BY ANY INSTRUCTION`.

### What the two zeros mean

`RenderModelInstanceContainer` scores zero on **both** its routes and **both are correct**. It is
embedded at `+0xF0` of the static render resource root `022C6F30` and cached as a pointer at
`root+0xDA0`; `0041E3A0` does `lea rax,[rsi+0xF0]` / `mov [rsi+0xDA0], rax` with the root in `rsi`.
The sweep sees RIP-relative operands and the image-base-relative idiom, not `[reg + disp]` off a
root already in a register. The root itself **is** named, by `lea`, in six functions. So an
embedded or chained object should be *expected* to score zero here, and a zero is a statement about
the instrument's reach rather than about the route.

### One thing this found on the way

`FUN_001D68F0` is an index-to-static-address selector: `cmp edx, 0xA` / `ja`, then an
image-base-relative jump table at `00120000 + 0xB6958`, and **six arms** that each do
`lea rax, [<a fixed address>]` / `mov [rcx], rax` — returning the address of one of six consecutive
eight-byte globals at `01F82C88, C90, C98, CA0, CA8, CB0`. Eleven indices, six distinct arms, and a
default that writes null. Those six are neighbours of the effect singleton's slot, **not fields of
it**; they are listed here so the next reader of that neighbourhood does not make the extent
mistake a second time.


## The census could never see a constructor (2026-09-19, OPUS)

`gen_ptr_census.py` and `gen_ptr_census_depth1.py` both begin by finding `mov rX, [rip -> ADDR]`
and tracking `rX`. That seeding is what makes them work. **It is also why neither has ever seen a
lazy singleton's constructor.** The shipped idiom is:

```
cmp  qword ptr [ADDR], 0        the guard
mov  ecx, <size>
call <malloc thunk>             the object arrives in RAX
mov  rcx, rax                   ... and the constructor runs on RAX
call <ctor>
mov  qword ptr [ADDR], rax      only NOW does the object reach the slot
```

**Every field the constructor writes is written before the store, through a register that never
came from the slot.** The constructor is usually the densest writer a type has, and it was
structurally invisible.

### The symptom, which was sitting in the output the whole time

`PostProcessParamContext` censused as **37 accesses that are all reads and no writes**. An object
nothing writes is impossible. That reading was not a small gap in the numbers — it was the
instrument announcing its own blind spot in a form nobody read as one.

### `gen_ptr_census_ctor.py`, and what it measures

It finds the function that **stores a register to the slot** — the creator, by definition — locates
the allocation inside it as the call preceded by `mov ecx, <imm>` where the immediate **is the
type's declared size**, seeds RAX there, and tracks forward through argument-passed callees.

| type | slot-seeded | allocation-seeded |
|---|---|---|
| `BootSingleton01F7F598` (`0xDD8`) | 3 accesses / **2 offsets** | 69 / **52** |
| `PostProcessParamContext` (`0x4A8`) | 37 accesses / **33 offsets**, all reads | 106 / **102** |
| `FrameMarkerSingleton01F82C80` (`0xF778`) | — | 11 / **11**, the known constructor |

**In all three, 0 offsets fall outside the declared extent** — which checks the extent as well as
the gain.

**Two controls, both required, both pass.** `BootSingleton01F7F598` must beat the slot-seeded
census (≥ 40 offsets): 52. And `FrameMarkerSingleton01F82C80`'s constructor is known by hand —
eleven inline writes at `001D6306`–`001D6341` — so the tool must recover *exactly* those eleven:
it returns eleven, and they are the eleven.

### What it does not do, said plainly

**Eight of the thirteen `PTR` rows still yield nothing**, and the tool says why on each: the
creator is found but its allocation is **not a sized call**, so there is no verified point at which
RAX becomes the object and nothing is seeded rather than something being guessed. One row,
`RenderModelInstanceContainer`, has **no creator at all** — consistent with it being embedded at
`+0xF0` of a static root rather than allocated.

It also cannot see an indirect call, a constructor reached through a vtable, or an access at a
computed offset with no literal displacement.

### CORRECTION, same day, before any row was written on it

The paragraph that stood here said this pass produced **"154 newly reachable offsets across two
types"**. **That is wrong, and it was wrong in the published commit `284ae0be8`.** I compared the
new census against the *old census* and called the difference new knowledge, without checking it
against **the store**, which is the thing that decides whether a fact is new. Checked:

| type | census offsets | already NAMED in the store | in a declared gap | outside every row |
|---|---|---|---|---|
| `BootSingleton01F7F598` | 52 | **44** | 8 | **0** |
| `PostProcessParamContext` | 102 | **102** | 0 | **0** |

**146 of the 154 were already in the store**, put there by hand. The genuinely new count is
**eight**, all in `BootSingleton01F7F598`: `+0xB20`, `+0xB40`, `+0xB60`, `+0xB68`, `+0xCB8`,
`+0xDB0`, `+0xDBB`, `+0xDD0`.

> This is the same error as addendum bx.2 — **a boundary I did not measure** — arriving in the
> write-up of the very pass that found bx.2. The census gain is real and the knowledge gain is a
> twentieth of what I claimed.

**What the measurement is actually worth is different, and stronger than a count of new rows.**
The instrument independently reproduced **146 offsets established by careful hand-reads, with zero
offsets falling outside any declared row in either type.** That is a third control and the best
kind — it reproduces a known answer rather than merely firing, so it could have failed by
over-reporting and did not. The right claim is: *`gen_ptr_census_ctor.py` recovers by machine what
this store previously got only by hand, and finds eight offsets the hand-reads missed.*

The eight are written as rows; the remaining declared gaps in both types stay declared.

### The full ledger, after running it over all thirteen `PTR` rows

| | |
|---|---|
| census offsets produced | **162** across three types |
| already named in the store | **154** |
| landing in a declared gap — **the real yield** | **8** |
| falling outside every declared row | **0** |

`GameSettingConfig` adds eight more census offsets and **all eight are inside already-named
settings fields**. Four rows resolve as `TEARDOWN (stores NULL)` — `ManagerSingleton0209BE80`,
`LegacyPs2GsTextureContext`, `FieldRecordTable` — and **the store's `dtor` cells already carry all
of them**, in one case more precisely than the tool: `LegacyPs2GsTextureContext`'s cell says
`0026E20C` *"is a reset and not a release; no deallocation of the 0x240 block was found"*, where
the tool says only `TEARDOWN`.

> **So the honest verdict on a day's instrument work is: eight new offsets.** Everything else it
> found, this database already knew. That is not a failure — an instrument that reproduces **154
> hand-established offsets and four hand-established destructors with zero strays** is validated
> in a way no amount of new output would validate it, and it will now do by machine what
> previously took a careful afternoon per type. But the gain over the *previous instrument* and
> the gain over the *database* are different numbers, and only the second one is knowledge.

### Three defects the tool shipped with, found by checking its labels against the bodies

1. **"Stores to the slot" is not "creates the object" — a destructor stores null.** `FUN_0028F2F0`
   is `ManagerSingleton0209BE80`'s teardown. Seeding from it would have tracked a null pointer's
   displacements as the type's fields. Nothing was censused from it only because the independent
   sized-allocation test failed — **a lucky save, not a designed one.**
2. **A 64-bit register and its 32-bit view are different enums.** The teardown idiom is
   `xor edi, edi` then `mov [slot], rdi`; comparing raw enums missed every one of them.
3. **Whether a store is a null store is a reaching-definitions question, not a neighbouring-
   instruction one.** `FUN_0018D3F0` creates `PostProcessParamContext`, and its *allocation-failure
   arm* does `xor edx, edx` immediately before the shared store. A linear test called the
   constructor a teardown and suppressed its 102 offsets. The rule now collects every definition
   of the stored register and requires **all** of them to be zeroing — under which `0028F2F0`,
   whose only definition of `rdi` is `xor edi, edi`, still reads as a teardown.


### Second pass: the tool took the first storer it found, and a slot usually has several

Running `gen_ptr_census_ctor.py` to the end exposed a fourth defect, and this one cost real
coverage rather than a label. **The tool returned whichever storer it met first while iterating a
dict.** A slot normally has at least two — a creator and a destructor — and it kept picking wrong:

| type | first storer found | the real creator | effect |
|---|---|---|---|
| `ManagerSingleton0209BE80` | `0028F2F0`, the **teardown** | `0028F8B0`, `mov ecx, 0x10FD0` → `00271420` | a 69,584-byte type read as allocation-less |
| `FieldRecordTable` | `00378540`, a **null store** | `00378B80`, the registrar | — |
| `LegacyPs2GsTextureContext` | `0026E1D0`, a **reset** | `0026E960`, which publishes the pointer | — |

The rule now collects **every** storer and prefers one with a sized allocation, then a non-null
store. **Each of the three then agreed with the `allocation_site` cell the store already carried**,
which is the fourth independent agreement between this instrument and the hand-read database.

### `PostProcessParamContext` is created at three addresses, not one

Enumerating the storers found **three** functions that each carry the *complete* lazy-create
inline, agreeing instruction for instruction on everything that matters:

| | size immediate | constructor | publish to `01F7F5F0` |
|---|---|---|---|
| `0018D3F0` (511 B) | `0018D41B` | `0018D432` | `0018D43E` |
| `0018EEE0` (1,581 B) | `0018EFC8` | `0018EFDF` | `0018EFEC` |
| `00193D50` (66 B) | `00193D69` | `00193D80` | `00193D86` |

`00193D50` is the standalone function; the other two are the compiler folding the same
`GetOrCreate` into larger callers. **The store's `allocation_site` cell named only `00193D50`.**

> **The singleton has one logical creator at three addresses.** A reimplementation that hooks or
> replaces only the named one would miss two live creation paths. And `0018D3F0`'s
> allocation-failure arm stores `xor edx, edx` through the shared publish, so **the slot can
> legitimately hold null after a failed create** — a state any consumer must tolerate.


### Third pass: a constructor hands sub-objects their own base, and a control that finally tests it

The tracker followed a callee only when it received the object at **offset zero**.
`ManagerSingleton0209BE80`'s constructor `00291750` does `lea rcx, [rdi + 0x5380]` and calls a
sub-object constructor with it, so the walk stopped at the parent's own writes: **7 offsets for a
69,584-byte type.** Following `base + N` with the offset carried as the callee's origin records
the sub-object's fields at their true offsets in the parent — which is exactly what `EMBED` means.

| type | before | after |
|---|---|---|
| `BootSingleton01F7F598` | 52 offsets | **182** |
| `PostProcessParamContext` | 102 | **127** |
| `ManagerSingleton0209BE80` | 7 | 9 (21 at depth 4) |

**And the new offsets are worth nothing as knowledge, which is the point of checking.** All **309**
offsets across the two big types land in **already-named rows** — 0 in a declared gap, 0 outside
any row. A looser following rule that produced 309 displacements and hit a hand-established field
every single time is validated about as well as a rule can be. It found nothing new.

> **The two existing controls would have passed however badly the new rule behaved.**
> `FrameMarkerSingleton01F82C80`'s constructor is fully inline and hands out no sub-object base at
> all, so the exact-eleven control does not touch the path that changed; `BootSingleton`'s control
> is a lower bound, which a runaway rule satisfies trivially. **A control has to exercise the rule
> it is guarding** — addendum bx's lesson, arriving one rule later. The third control requires the
> four sub-object bases `00291750` hands out, read by hand at `00291788`, `002917C2`, `00291794`
> and `002917AA`.

### Where this leaves the eight `PTR` rows that reported no allocation

Answered, and mostly the answer is that **there is nothing to find**. The store's own
`allocation_site` cells already classify them and the tool's silence agrees:

- **`INTERIOR`** — `BattleSystemState` is `SaveImage_GetActiveRuntimeBuffer() + 0x4E68C`,
  `ImageBackedStateBlock` is `+ 0x8200`, `AchievementState` is interior to *that*, and
  `CharacterRenderSystemTail` is `+0x48800` of one `0x48930` allocation. These are **views into
  image storage in `.bss`; no allocation call exists on any of these paths**, so a tool looking
  for one correctly finds none.
- **`IMAGE`** — `RenderModelInstanceContainer` is storage inside a static `.data` object.
- **`RESOURCE`** — `FieldRecordTable` is the loaded `navimapdata.bin` buffer.
- **`HEAP`, and the tool was simply wrong** — `ManagerSingleton0209BE80`,
  `LegacyPs2GsTextureContext` and `FieldRecordTable`'s registrar, all recovered by the
  all-storers fix above.

So the remaining rows need **no second allocation idiom**. They need the tool to say *"no
allocation exists on this path"* rather than *"not a sized call"*, which reads like a limitation
when it is a fact about the type.


## The store was missing 153 Phyre classes, and declaring them makes a metric worse (2026-09-19, OPUS)

`_types/` carried 177 Phyre classes because that is what `members/phyre-class-instance-sizes.tsv`
covered — and **that table is one registrar shape.** Sweeping every call to the class-descriptor
constructors `00632D80`/`00632C90` image-wide finds **400 sites, 330 named**.

> **CORRECTED, same day: 330 is this sweep's coverage, not the population.** The population is
> **409 reflected classes**, established 2026-09-13 by an independent byte-template scan of the
> adapter family (`AUDIT-LOG`; 1,185 of 1,185 appearances resolved to a slot-5
> complete-object-locator). So the sweep covers **330 of 409, 81 %**, against the old table's
> 43 %. See §19e of the member-registration page.
So **153 classes with a known instance size, a known descriptor address and, for 112 of them, a
known parent were simply absent from the store.** They are 76,391 instance bytes.

Among the absentees are the two layers *above* a class the store already had: the store held
`PDeferredLightingBase` but neither `PDeferredLightingD3D11` (`0x4330`) nor `PDeferredLighting`
(`0x4330`) — the base of a three-level chain, and neither of the classes actually instantiated.
Same shape for `PMotionBlur`, `PTextureCubeMap` and `PShaderPass`. `PApplication` (`0x1130`) and
`PScheduler` (`0x2F8`) are roots and were also missing.

**Declared: 153 types, 194 field rows, 112 of them a `baseClass_<Parent>` row.** Sized types
**275 → 428**. Invariants: 0 zero-width rows, 0 sum or continuity defects, 0 duplicate type names,
route collisions clean.

### The unknown fraction went UP, from 10.4 % to 12.1 %

That is the correct outcome and it is worth stating plainly rather than burying. These classes
were always this unknown; the store was not carrying them, so their unknown bytes were not being
counted. **Declaring a known size with an honest gap makes the ratio worse and the database
better.**

> This is the same ruling made for the 162 Phyre extents earlier the same day, and the same
> reasoning the charter applies to `engine_explained`: **a type with `size=UNRESOLVED` cannot be
> allocated by a reconstruction at all**, and **a number that improves by withholding a known
> fact is measuring the wrong thing.** A reader who wants the old figure can have it by excluding
> the 153; a reader who wants to build something needs the sizes.

**What is NOT claimed:** no member of any of the 153 is named. The reflection schema recovered
none for them, and each field row says so — either `baseClass_<Parent>` plus a remainder that
states "the Phyre reflection schema recovered NO member for this class", or, where no parent
resolved, a single span over the whole instance saying the same. **Lifetime is unestablished for
all 153 and is left unestablished rather than borrowed from a sibling.**


### A sixth control, which only became possible once all 330 were declared

With every Phyre class in the store, the base-class rows can be checked against the store itself
rather than against the table they came from:

> **181 `baseClass_<Parent>` rows. Parents that are not a declared type: 0. Rows whose width
> differs from the parent's own declared `size`: 0.**

That is a closure property, and it is the kind that cannot be satisfied by luck: every row's width
was taken from the parent descriptor's `+0x38` at the *child's* construction site, and every
parent's `size` was taken from `r9d` at the *parent's own* construction site. **Two independent
reads of two different call sites agree on all 181 edges.**

The deferred-lighting chain is what it looks like in the store now:

| type | | |
|---|---|---|
| `PDeferredLighting` (`0x4330`) | `baseClass_PDeferredLightingD3D11`, 17,200 bytes | **adds nothing of its own** — a pure specialization |
| `PDeferredLightingD3D11` (`0x4330`) | `baseClass_PDeferredLightingBase`, 16,856 | + 344 own bytes at `+0x41D8` |
| `PDeferredLightingBase` (`0x41D8`) | `baseClass_PPostEffectBase`, 80 | + the 16,512 still unexplained, then the registered members from `+0x40D0` |

Before today the store had only the middle row's parent and none of the rest.

### The route verb, the storage class and the image must agree, audited 2026-09-20 (OPUS)

The `route` column and the `allocation_site` column can contradict each other, and nothing checked
until now. The two verbs that matter:

| verb | means | compatible storage |
|---|---|---|
| `STATIC` / `ARRAY` | the instance **is at** this image address | `IMAGE` |
| `PTR` / `PARRAY` / `SLOTPTR` | **read a pointer** at this address and go there | `HEAP`, `POOL`, `RESOURCE` |
| `EMBED` / `CHAIN` / `RELOFF` | parent-relative | any - a heap object lives inside a heap parent |

**A dereferencing verb on `IMAGE` storage found four rows.** Three were the same defect and are
corrected under CON-139: `NameBindingEntry`, `NameBindingSubRecord` and `ScheduledTaskRecord` each
carried `PARRAY` while their own `allocation_site` said `IMAGE ... records in the image`. The image
settles such a case by **how it reaches the address** - every reference to those three is a `lea`
and none is a load - and the two censuses agree from opposite directions: as pools they yield zero
accesses, as arrays they yield 13, 62 and 18, every offset inside a declared field. The fourth,
`RenderModelInstanceContainer`, is **routed rather than fixed**: `022C7CD0` has no rip-relative
reference anywhere in the image, so the lea-versus-load test cannot be run on it at all.

**The inverse - a fixed-address verb on `HEAP`/`POOL` storage - found zero, and the zero is
meaningful.** A check that has never fired proves nothing, so it was validated against an injected
defect first: flipping one `HEAP` row's route to `STATIC` in a copy of the store makes it report,
and the real store reports none.

Why this is worth a paragraph rather than a passing gate: a wrong verb is **resolvable and wrong**.
`PARRAY` on an array dereferences the first eight bytes of record 0 and uses them as the base. It
does not fault; it addresses somewhere else. That is the same shape as CON-137, where a route was
one hop short and pointed at a different live object.

Both checks live in `check_storage_class.py` as the `DEREF` and `FIXEDHEAP` notes.

**And the verb is now checked against the image, not only against the other column.** Those two
notes compare `route` against `allocation_site` - both of which are assertions, so their agreement
is consistency rather than truth. `check_route_verb_against_image.py` asks the binary instead: a
`PTR`/`PARRAY`/`SLOTPTR` verb REQUIRES a load at the address, because a pointer must be read before
it can be followed. The converse does **not** hold - a static needs no `lea`, since code addresses
its fields directly - and assuming it did made the first version flag `SharedGameplayLcgState`
(four bytes, read 17 times for its value) and `BattleFormulaScratch` (a 0xA8 block whose 77 loads
reach its fields). A fixed verb is supported by any reference inside `[addr, addr+size)`.

Current result: **59 of the store's address-bearing route alternatives are supported by the image,
0 are contradicted, and 3 are untestable** - `ScriptNativeDispatchRecord`'s table and both
`RenderModelInstanceContainer` addresses have no rip-relative reference at all, so they may be
reached through a computed base that no scan of rip-relative operands can see.

The checker is validated three ways, because a checker nobody tested is an assertion too: it
discriminates (two controls - a known pointer cell and a known array base), it fires (re-injecting
the three CON-139 verbs into a copy of the store reports all three), and it is quiet on the
corrected store.

### And the stride, checked the same way, audited 2026-09-20 (OPUS)

A wrong verb points at the wrong object and a wrong count over- or under-runs. A wrong **stride**
silently misattributes every field of every element while still landing inside the array - it is
the one route field where being wrong looks entirely normal. So it gets the same treatment:
`check_route_stride_against_image.py` compares each `stride=` against the scaling the image
actually performs in a body that references the route's base.

**x86 scales an index three ways, and a checker that knows only one calls the others wrong.**

| form | looks like | strides it can express |
|---|---|---|
| immediate | `imul rcx, rcx, 0x250` | any |
| SIB scale | `[base + idx*8]` | **only** 1, 2, 4, 8 |
| lea chain | `lea rax, [r8+r8*2]` then `*8` | small odd factors - 24 = 3x8 |

A stride of `0x18` therefore appears as a lea chain and **never** as the immediate `0x18`; a
power-of-two stride above 8 appears as a bare `shl`, which the SIB byte cannot encode. The first
version of the check knew only the immediate and the chain, and reported `ChunkedSlotBankEntry`,
`ChunkedSlotEntry` and `ResourceRequestSlot` as unconfirmed - three checker gaps wearing the
costume of store defects.

**Current result: 23 strides confirmed, 5 SIB-scalable (1/2/4/8, which carry no arithmetic to
find), 1 with no reference to its base, and 3 not confirmable host-locally.** That last bucket is
not a defect list and is deliberately not named like one: a host-local test can only see indexing
in a body that names the base, and all three entries hand the base to a callee instead -
`00477EE0` `lea`s the two Chunked tables and passes them as arguments 5 and 6, which the
`RenderModelInstanceContainer` row already states, and `FieldRecord`'s nine bodies load the table
pointer and pass it on. "No scaling found" there means the instrument could not look.

Validated against three known answers: `SpawnRecord` `0x250` by immediate, `AudioBankSlot` `0x18`
by the `lea rax,[r8+r8*2]` chain its own evidence cell documents, and `BattleUnit` `0xF50` by
immediate.

### And the count, which needed two kinds of evidence, audited 2026-09-20 (OPUS)

Count is the last route field, and its failure mode is the most concrete of the three: too large
and a consumer walks off the end of the array into whatever the linker put next.

A count is rarely written down as itself. `check_route_count_against_image.py` looks for the two
forms it does take:

| evidence | looks like | found |
|---|---|---:|
| the **total size** | `mov ecx, 0x9400` before an allocation or memset, where `0x9400 = 64 * 0x250` | 8 |
| a **loop bound** | `cmp eax, 0x7F` / `cmp ecx, 0x80` in a body that walks the array | 15 |

**Current result: 23 of 30 counts confirmed, 3 symbolic, 1 with no reference to its base, and 3
with no bound evidence.** Symbolic counts - `count=slotCount0208E6A0` and two others - name a
global because the bound *is* a global; resolving one means finding what writes it, which is a
different question and is not attempted. The last bucket is absence of evidence, not a defect
list: an array indexed only callee-side shows no bound in any body that names its base.

**The self-test caught a wrong control, which is the point of having one.** `AudioBankSlot`'s count
of 64 was asserted in the checker as "a bound the resolvers compare against". They do not - its
twelve referencing bodies contain no comparison against `0x40` or `0x3F` at all, and it sits in the
no-evidence bucket. Its 64 comes from arithmetic (`0x600 / 0x18`) on its own row, which is weaker
support than either form above and is not therefore wrong. The control was **replaced rather than
relaxed**: a control chosen because it passes is not a control.

## A HEAP row describes the payload, not the block (OPUS)

Added 2026-09-20 (OPUS).

Every allocation from `0036A190` is preceded by a **`0x40`-byte header** - the declared type
`ImageAddressArenaBlockHeader` - and the pointer callers hold is that header's *end*. The release
path proves the offset: `00369860` does `lea rbx, [rcx - 0x40]` on the pointer it is given. The
arena body `0036BC60` works from the other side, holding the block base and returning `base + 0x40`,
and it rounds every request up to a multiple of `0x40` as well, so payload and header share one
granularity.

So for any type whose `allocation_site` begins `HEAP`:

- the declared `size` is the **payload**, and the real block is `size + 0x40`;
- the bytes at `-0x40 .. -0x01` are `ImageAddressArenaBlockHeader`, not that type's storage and not
  padding;
- the block's byte count is already at that header's `payloadLength` (`+0x18`), readable through the
  twelve-byte accessor `0036C100`. **A type does not need its own size field to be measurable at
  runtime**, and some `UNRESOLVED` sizes may be readable this way rather than unknowable -
  `NavRunStateBlock` was the case that showed it;
- the block carries a seven-byte **allocation tag name** at `+0x34`, written by `0036C660` from a
  string literal the allocating call supplies. That tag is a provenance clue for any block whose
  owner is unclear.

**Why no instrument in `Tools/analysis-kit` can see this.** Every census walks *forward* from a base
and records `[reg + disp]`. A field at `-0x28` is not an offset into the object, so the header is
**unreachable** to them rather than merely missed - and symmetrically, the arena's own bodies never
name the user pointer, so scanning them for negative displacements finds nothing either. The two
views are disjoint and the header sits in the gap.

**A caution that cost me thirty-two rows.** Neither of the two objects above was missing: I declared
duplicates of both before checking, and `check_route_count_against_image.py` caught it by printing
two rows with the same base, stride and count. **Before declaring a type at a fixed address, grep
`_types` for that address.** It is one command, and a route audit finding the collision afterwards
is a much later and more expensive place to learn it.

