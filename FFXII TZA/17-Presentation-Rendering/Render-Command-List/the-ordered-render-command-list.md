---
system: The ordered render command list — how a pass becomes a drawn layer
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: CodeDomain:Presentation — no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 0018EEE0, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-07
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-ordered-render-command-list-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The ordered render command list — how a pass becomes a drawn layer

> Each render pass in the frame is **an object appended to a list**, not a function that draws.
> Every one carries a ~~**draw-order number**, and that number — not the order the frame enqueued~~
> ~~them — decides what ends up in front of what.~~ **class mask**, and the list runs in the order the frame enqueued *(corrected 2026-10-02, OPUS: the walk runs the list in stored order and only ANDs slot 2's value, `0018B100`+0x67 `test dword ptr [rsi + 0x20], eax`)*.

## 1. What the player sees

The picture is built in layers, and you can see the seams. Ambient occlusion darkens the crease
where a wall meets the floor. Water refracts what is behind it, so the riverbed bends. Heat haze
around a Mist-charged character warps whatever was already drawn. Depth of field softens the
distance. And when a full-motion video plays, it covers everything.

None of that works unless the layers happen **in the right order** — refraction has to copy the
screen *after* the world is drawn but *before* the water goes down, and the video has to be last
or it would be blurred by the depth of field.

The engine does not get that order by calling things in sequence. It builds **a list of jobs**,
each stamped with ~~a number saying how late it belongs, and runs the list in number order~~ a class mask, and runs the list in the order the jobs were added *(corrected 2026-10-02, OPUS: `0018B100`+0x67 `test dword ptr [rsi + 0x20], eax`; nothing sorts)*. That
is why turning one effect off never shifts the others out of position, and why the game can
enqueue a pass from anywhere in the frame without worrying about when.

There are thirty-six kinds of job, and the engine names them itself: opaque geometry, mask
border, subsurface scattering, ambient occlusion, post-processing, PS2 depth of field, gaussian
filter, three different "copy the screen so something can refract it" jobs, MSAA on and off,
video, and — with a name that gives away where the studio's tools came from — Razor GPU profile
markers.

## 2. Native mechanism

### 2.1 One list, one idiom, thirty-six kinds of job

The frame's render passes do not draw. Each is a thin wrapper — 30 to 70 bytes — that fetches a
list singleton and calls **an enqueue function**, and every one of those enqueue functions is
the same ~~140-to-150-byte~~ template *(corrected 2026-10-02, OPUS: the 36 builders are 139-253 bytes, 29 of them 140-150 - the falsification pass's table; recount of the 36 callers of `0018AFF0` in the `0018xxxx` range)*:

```c
// the shape of all 18 enqueue functions - 0018C610 shown, 148 B   // <- corrected 2026-10-02, OPUS - 36 builders, not 18 (the 36 `0018xxxx` callers of 0018AFF0; 40 appenders in all)
node = malloc(0x18 | 0x20 | 0x28);      // the command object
node = CommandCtor(node, args);         // a constructor unique to this command class

p = list->end;                          // list = 01F7F5E8, fetched by 0018CA40
if (p < list->capacityEnd) {            // push_back, inline fast path
    list->end = p + 1;
    if (p != NULL) *p = node;
} else {
    FUN_001AB570(list, p, &node);       // grow-and-insert, 318 B
}

FUN_0018AFF0(FUN_0018B4E0(), node);     // push_back onto a SECOND list at 01F7F5E0
```

Two things follow immediately. The wrapper does no drawing — it allocates and appends. And
**every command object is appended to two lists**, the one the caller named and a second global
one; `0018B4E0` returns `01F7F5E0` ~~and asserts it is non-null before doing so~~ *(corrected 2026-10-02, OPUS: `CON-151`: `0018B4E0`+0x6..+0x10 hands the non-null test to the empty `0016D6A0`, a compiled-out assert)*.

The list itself is an **EASTL vector**, and it says so:

```c
// 0018C9E0 - creates the list on first use, 95 B
if (list == NULL && (list = FUN_00210EC0(0x20)) != NULL) {
    list[0] = 0;                                   // begin
    list[1] = 0;                                   // end
    list[2] = 0;                                   // capacityEnd
    FUN_001EDF00(list + 3, "EASTL vector", ...);   // the allocator, named
}
DAT_01F7F5E8 = list;
```

```struct RenderCommandList base=record size=0x20
+0x00  u64   pBegin        first element
+0x08  u64   pEnd          one past the last; the push_back cursor
+0x10  u64   pCapacityEnd  one past the allocation
+0x18  u64   allocator     EASTL allocator, name "EASTL vector"
```

### 2.2 `OrderedObject`: the base class, and the number that decides the layering

Every command constructor calls one base constructor first, and that base constructor stores a
vtable pointer through a **named symbol** — one of the few places in this binary where the
compiler left the class name in the image rather than only in RTTI:

```c
// 00212CC0 - the base constructor, 26 B, called by 42 sites
obj[1]          = 0;                     // +0x08  order value, zero by default
obj[0]          = OrderedObject::vftable;// +0x00  vtable
*(u8*)(obj + 2) = 1;                     // +0x10  enabled, on by default   // <- corrected 2026-10-02, OPUS - not an enable: the flush 0018C8F0 executes an entry only when this byte is 0 (0018C8F0+0x43), and neither walk reads it
```

```struct OrderedObject base=record size=0x18
+0x00  u64  vftable    3 slots: destructor, execute, order key
+0x08  u64  orderValue set to 0 by the base constructor
+0x10  u8   enabled    set to 1 by the base constructor   <- corrected 2026-10-02, OPUS - flushSelector, not an enable: read only by the flush at 0018C8F0+0x43, which executes the entry when it is 0
+0x11  u8[7] unread11  base constructor does not touch it; no reader found — a question, not padding (§7 item 7)
```

`+0x11` to `+0x17` is declared above as one `unread` span, not left out. The base constructor does
not touch it and no reader was found; **that is a question, not padding**, and it is §7 item 7
rather than a named field.

Subclasses that need arguments extend it: `PostProcessObj` stores a mode at `+0x18` (object size
`0x20`), `SetDofObj` stores a float at `+0x1C` (size `0x28`).

**Every class in the block has exactly three vtable slots**, and slot 2 is the interesting one —
in every case its whole body is a single constant return:

```c
001F2880:  return 0x10;    // 6 B
001F28A0:  return 0x80;    // 6 B
0053DD10:  return 1;       // 6 B
```

That is the ~~**draw-order key**~~ **class mask** *(corrected 2026-10-02, OPUS: `0018B100`+0x67 `test dword ptr [rsi + 0x20], eax`, and `0018B1B0` ANDs it too; no comparator runs)*. It is what makes the base class `OrderedObject` an ordered
object, ~~and it is why enqueue order does not determine draw order~~ and enqueue order is the draw order.

| slot | contract | evidence |
|---:|---|---|
| 0 | destructor | unique per class in all 36 |
| 1 | **execute(this, context)** | unique per class; bodies read in §2.4 |
| 2 | **order key** | a constant return in all 36; three distinct values observed *(answered: see §2.5 - nine implementations across the 42 concrete classes, seven constants and two data-driven keys; 2026-10-02, OPUS)* |

Observed keys: `1` for `RazorMarkerPushObj` and `BegineSceneObj` — the jobs that must run
first; `0x10` for ~~the ordinary render passes~~ most ordinary render passes and `0x100` for `RenderOpaqueObj`, `RenderAfterWaterObj`, `RenderMapOpaqueObj` and `RenderMonsterGalleryChara` *(corrected 2026-10-02, OPUS: their shared slot 2 `001F2890` is `mov eax, 0x100`)*; `0x80` for `VideoObj` — the job that must cover
everything.

**`0053DD10` carries the ledger name `InputDevice_QueryAvailabilityState_Always1`.** It has
nothing to do with input devices. It is a 6-byte `return 1` that the linker folded across
unrelated classes — open question **BA-1** — and the name belongs to whichever toucher was
classified first. Here it is a draw-order key of 1.

### 2.3 The complete pass → class map

Every named pass scope in `MainLoop_Draw` resolves through four steps — wrapper, enqueue
function, constructor, stored vtable — to exactly one RTTI class. Each step was read; none is
inferred from a caller or from address adjacency.

| Frame scope name | wrapper | enqueue | ctor | vtable | class |
|---|---|---|---|---|---|
| *(frame open)* | `001EC490` | `0018B540` | `001F1770` | `009030B0` | `ApplyJsonForCutSceneObj` |
| *(frame open)* | `001829A0` | `0018CC60` | `001F1ED0` | `00903090` | `SetScreenIndexToPostProcessManagerObj` |
| *(draw setup)* | `00183120` | `0018CB30` | `001F1E50` | `00903370` | `SetPrimIdEnableObj` |
| *(scene begin)* | `00182220` | `0018B670` | `001F17E0` | `00902FB0` | `BegineSceneObj` |
| pass gate bit 1 | `0017F2F0` | `0018BA20` | `001F1870` | `00903250` | `CopyFrontBufferForChrRefraction` |
| pass gate bit 1 | `0017F070` | `0018C580` | `001F1D90` | `00903150` | `RenderOpaqueObj` |
| `"mask border 0"` / `"mask border 2"` | `0017F670` | `0018C450` | `001F1B20` | `00903190` | `MaskBorderObj` |
| `"AO render"` | `001826E0` | `0018B970` | `001F1840` | `00903050` | `CopyDepthBufferObj` |
| `"AO render"` | `0017ECF0` | `0018C740` | `001F1740` | `009031F0` | `AmbientOcclusionObj` |
| `"Water effect"` | `00180A30` | `0018C2A0` | `001F1D00` | `00903170` | `RenderAfterWaterObj` |
| `"Water effect"` | `0017F330` | `0018BB70` | `001F18E0` | `00903270` | `CopyFrontBufferForWaterRefraction` |
| *(before post-processing)* | `00182A10` | `0018C7D0` | `001F1DC0` | `009031B0` | `RenderSSSObj` |
| `"post-processing render"` | `00182970` | `0018C610` | `001F1B80` | `009031D0` | `PostProcessObj` |
| `"PS2 DOF"` | `001827E0` | `0018C6B0` | `001F1BD0` | `00903070` | `Ps2DofObj` |
| `"Gaussian Filter"` | `0017FD70` | `0018C330` | `001F1A90` | `00903210` | `GaussianFilterObj` |
| *(flush block)* | `00184900` | `0018C860` | `001F1F00` | `009032B0` | `VideoObj` |
| *(scene end)* | `001823B0` | `0018BE70` | `001F19E0` | `00902FD0` | `EndSceneObj` |
| *(draw tail)* | `0017F6B0` | `0018C450` | `001F1B20` | `00903190` | `MaskBorderObj` |
| scope push | `001EB150` | `0018C160` | `001F1C30` | `009032D0` | `RazorMarkerPushObj` |
| scope pop | `001EB110` | `0018C0D0` | `001F1C00` | `009032F0` | `RazorMarkerPopObj` |

Reading that table back tells you what the passes are *for*, and the readings are physically
coherent in a way that a name list is not:

- **`"AO render"` brackets two jobs**: copy the depth buffer, then compute ambient occlusion
  from the copy. Occlusion needs depth, and you cannot read the buffer you are writing.
- **`"Water effect"` brackets two jobs**: draw what goes after water, and copy the front buffer
  for water refraction. Refraction needs a snapshot of the scene behind the surface.
- **`CopyFrontBufferForChrRefraction`** is the third copy — the one that makes heat haze and
  character refraction possible.
- **`VideoObj` carries order key `0x80`**, the highest observed, so full-motion video is
  composited after every other layer including the depth-of-field blur.
  *⚠ Corrected 2026-09-14 (FABLE, UQ-230): the slot-2 value is not a sort key. The walkers run the list in stored order and AND that value as a class mask (`0018B167`, `0018B24A`–`0018B25E`). So `0x80` selects which walks run `VideoObj`; it does not place it after other layers. When video draws relative to the depth-of-field pass is set by insertion order and the render pass's split, not by this key.*

### 2.4 What an execute method actually does

Slot 1 takes `(this, context)`. The bodies share a shape: check a global render enable, open a
profile slot on the context, then read **per-effect switches from a render-parameter block** and
do the work through a second singleton.

```c
// 001F28B0 - AmbientOcclusionObj::Execute, 257 B
params = FUN_00193D50();                       // render-parameter singleton, 66 B getter
if (*(char*)(params + 0x198) != 0 && DAT_01DFE0C4 != 0) {
    if (FUN_00609710(ctx) != 0) FUN_00600A60(ctx, 6);    // profile slot 6
    a = FUN_001867A0(FUN_00189120());
    b = FUN_00186660(FUN_00189120());
    c = FUN_001867C0(FUN_00189120());
    d = FUN_001867B0(FUN_00189120());
    FUN_0018F510(FUN_00193D50(), ctx, d, c, b, a);
    FUN_00188730(FUN_00189120());
    ...
}
```

```c
// 001F3090 - GaussianFilterObj::Execute, 370 B - the gate, exactly
if (*(char*)(FUN_00193D50() + 0x19A) == 0 &&
    *(char*)(FUN_00193D50() + 0x3E8) == 0 &&
    *(char*)(FUN_00193D50() + 0x180) == 0)
        return;                                          // nothing to blur
if (FUN_00609710(ctx) != 0) FUN_00600A60(ctx, 2);        // profile slot 2
if (DAT_01DFE0C4 != 0) { ... }
```

```c
// 001F3300 - PostProcessObj::Execute, 313 B
if (DAT_01DFE0C4 != 0) {
    if (FUN_00609710(ctx) != 0) FUN_00600A60(ctx, 3);    // profile slot 3
    FUN_00194A30(FUN_00193D50());
    isCurrentScreen = (*(int*)(this + 0x18) == DAT_01F82EC0);   // mode == active screen index
    if (FUN_0018E470(FUN_00193D50()) != 0)
        FUN_0018EEE0(FUN_00193D50(), ctx, FUN_00193DA0, 1, isCurrentScreen);
    ...
}
```

```c
// 001F29E0 - BegineSceneObj::Execute, 50 B - the smallest
FUN_00188AC0(FUN_00189120());
FUN_005FEFD0(ctx, *(u32*)(this + 0x18));
```

Three facts a modder can use fall straight out of these:

1. **`DAT_01DFE0C4` is a master render enable.** Clear it and the execute bodies of
   `PostProcessObj`, `GaussianFilterObj` and `AmbientOcclusionObj` all become no-ops while the
   objects are still created and still ordered.
2. **`FUN_00193D50()` returns the render-parameter block**, and single bytes in it are the
   per-effect switches: `+0x198` gates ambient occlusion; any of `+0x19A`, `+0x180` or `+0x3E8`
   enables the gaussian filter. These are byte flags, not floats — on/off, not intensity.
3. **`FUN_00600A60(ctx, n)` opens a numbered profile slot** and the number is per-pass —
   gaussian `2`, post-processing `3`, ambient occlusion `6`. `MainLoop_Draw` passes the same
   small integers to `00332420(0..3)`.

`PostProcessObj` is the only one of these carrying an argument: its mode at `+0x18` is compared
against a global screen index at `01F82EC0`, and its constructor maintains that global —
incrementing it when the mode is non-zero and zeroing it when the mode is zero:

```c
// 001F1B80 - PostProcessObj::PostProcessObj, 68 B
obj->mode = mode;                                     // +0x18
obj->vftable = PostProcessObj::vftable;               // 009031D0
DAT_01F82EC0 = (mode == 0) ? 0 : DAT_01F82EC0 + 1;
```

So the screen index counts post-process commands enqueued this frame, and each command knows
whether it is the current one. That is a split-screen / multi-viewport mechanism, and it is the
only place in this document where one command's behaviour depends on how many of its siblings
exist.

### 2.5 The complete `OrderedObject` slot matrix — all 43 RTTI classes

The RTTI census (FABLE `pub140-scratch/tools/rtti_vtables.py`, regenerated this pass against
`uncovered_frontier.txt`) resolves **43 ~~concrete~~ classes** - 42 concrete and the abstract base *(corrected 2026-10-02, OPUS: `OrderedObject`'s slot 1 is the `_purecall` thunk `00861EC6`; recount of `members/ordered-object-vtable-slots.tsv`, 43 class names)* - deriving from `OrderedObject` —
§2.2's "36" undercounts by the seven RTTI names the pass→class map does not reach
(`ApplyJsonForCutSceneObj`, `MonsterGallerySoftParticleEnable`, `ReadPresetDofForCutSceneObj`,
the `GiReset*Obj` pair, and the three-class `FontBorderOrderedObject` family). Every class's
full slot table with a per-body role and an interior instruction citation is in
[`members/ordered-object-vtable-slots.tsv`](members/ordered-object-vtable-slots.tsv); the
aggregate facts:

- **Slot 0 — destructor.** 41 of 43 are the scalar-deleting shape (`call` the member-dtor,
  `00809950` free gated on `dl & 1`) — 40 route through member-dtor `00212CE0` and
  `CharacterOrderedObject` `001F4A40` through `00215310`. The exceptions:
  `MapOrderedObject` `001E11D0` calls `00212C50`, and `RazorMarkerPushObj` `001F2520`
  first **frees its `[+0x18]` member** (`00809950` with size 1) — the only destructor
  owning a heap child.
- **Slot 1 — execute.** The base class's slot is `00861EC6` = **`jmp _purecall`** — the slot is
  *pure virtual* (`= 0`), so §2.2's constant-return claim for slot 2 holds for the concrete
  classes only, never the base. Every concrete class implements it; the leaf executes forward
  (`MapOrderedObject` `00212C60` → `this[+0x08]` non-null → `001E2AF0`; `CharacterOrderedObject`
  `00215320` → `001F5D70`), the scene bookends tail-call the submission helpers
  (`BegineSceneObj` `001F29E0` → `005FEFD0` scene-begin; `EndSceneObj`/`EndScene0Obj`
  `001F2FA0`/`001F2F90` → `00600A60` profile slot 3), and the pass executes gate on
  `01DFE0C4` (the §2.4 master enable) plus class-parameter bytes in the `00193D50` block.
- **Slot 2 — order key.** Constants: `0x01` ×11 (`0053DD10` — the folded leaf, §2.2's BA-1) for
  the scene bookends, markers, and the MSAA/DoF/PrimId toggles; `0x10` ×18 (`001F2880`) for the
  ordinary passes; `0x20` ×3 (`00212E20`, the FontBorder family); `0x80` ×1 (`001F28A0`,
  VideoObj); `0x100` ×4 (`001F2890` — `RenderMonsterGalleryChara`, `RenderMapOpaqueObj`,
  `RenderOpaqueObj`, `RenderAfterWaterObj`, the monster-gallery/render-opaque band);
  `0x2` (`00290180`, CharacterOrderedObject); `0x4` (`0016EE70`, MapOrderedObject). Two classes
  break the constant convention: the `GiReset*Obj` pair returns **`this[+0x18]`** (`00879750`)
  and `GeometryInstanceOrderedObject` returns **`this[+0x20]`** (`001F49E0`) — data-driven order
  keys, the only two in the family.
- **Slot 3** exists only in the three `FontBorderOrdered*` classes: `00225580`, a 4 B setter
  `mov [rcx+0x18], edx`.

**`001F2520`** (`RazorMarkerPushObj` dtor, 79 B) also re-stamps the `009032D0` vtable before
freeing the child — the standard derived-dtor restore-then-teardown order.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0018CA40` | render command list getter | 8 B | returns `01F7F5E8` |
| `0018C9E0` | create the list on first use | 95 B | allocates 0x20, names the allocator `"EASTL vector"` |
| `0018B4E0` | second command list getter | 33 B | returns `01F7F5E0`~~, asserts non-null~~ *(corrected 2026-10-02, OPUS: `CON-151`: the test goes to the empty `0016D6A0`)* |
| `0018AFF0` | `push_back` onto the second list | 58 B | the shared tail of every enqueue |
| `001AB570` | vector grow-and-insert | 318 B | the slow path when capacity runs out |
| `00212CC0` | **`OrderedObject` base constructor** | 26 B | stores `OrderedObject::vftable`, order 0, ~~enabled 1~~ flush selector 1 *(corrected 2026-10-02, OPUS: `0018C8F0`+0x43 is the byte's only reader and executes the entry when it is 0)* |
| `0018B540` | enqueue `ApplyJsonForCutSceneObj` | 143 B | |
| `0018B670` | enqueue `BegineSceneObj` | 148 B | |
| `0018B970` | enqueue `CopyDepthBufferObj` | 176 B | |
| `0018BA20` | enqueue `CopyFrontBufferForChrRefraction` | 144 B | |
| `0018BB70` | enqueue `CopyFrontBufferForWaterRefraction` | 144 B | |
| `0018BE70` | enqueue `EndSceneObj` | 144 B | |
| `0018C0D0` | enqueue `RazorMarkerPopObj` | 144 B | |
| `0018C160` | enqueue `RazorMarkerPushObj` | 150 B | copies the name into a 0x200-byte buffer |
| `0018C2A0` | enqueue `RenderAfterWaterObj` | 144 B | |
| `0018C330` | enqueue `GaussianFilterObj` | 144 B | |
| `0018C450` | enqueue `MaskBorderObj` | 148 B | |
| `0018C580` | enqueue `RenderOpaqueObj` | 144 B | |
| `0018C610` | enqueue `PostProcessObj` | 148 B | |
| `0018C6B0` | enqueue `Ps2DofObj` | 139 B | |
| `0018C740` | enqueue `AmbientOcclusionObj` | 144 B | |
| `0018C7D0` | enqueue `RenderSSSObj` | 144 B | |
| `0018C860` | enqueue `VideoObj` | 144 B | |
| `0018CB30` | enqueue `SetPrimIdEnableObj` | 143 B | |
| `0018CC60` | enqueue `SetScreenIndexToPostProcessManagerObj` | 143 B | |
| `001F1740` | `AmbientOcclusionObj` constructor | 33 B | |
| `001F1770` | `ApplyJsonForCutSceneObj` constructor | 51 B | |
| `001F17E0` | `BegineSceneObj` constructor | 47 B | ledger name is a fold artefact |
| `001F1840` | `CopyDepthBufferObj` constructor | 33 B | |
| `001F1870` | `CopyFrontBufferForChrRefraction` constructor | 33 B | |
| `001F18E0` | `CopyFrontBufferForWaterRefraction` constructor | 33 B | |
| `001F19E0` | `EndSceneObj` constructor | 33 B | |
| `001F1A90` | `GaussianFilterObj` constructor | 33 B | |
| `001F1B20` | `MaskBorderObj` constructor | 47 B | ledger name is a fold artefact |
| `001F1B80` | `PostProcessObj` constructor | 68 B | maintains the screen-index counter |
| `001F1BD0` | `Ps2DofObj` constructor | 33 B | |
| `001F1C00` | `RazorMarkerPopObj` constructor | 33 B | |
| `001F1C30` | `RazorMarkerPushObj` constructor | 118 B | allocates 0x200 bytes for the name |
| `001F1D00` | `RenderAfterWaterObj` constructor | 33 B | |
| `001F1D90` | `RenderOpaqueObj` constructor | 33 B | |
| `001F1DC0` | `RenderSSSObj` constructor | 33 B | |
| `001F1DF0` | `SetDofObj` constructor | — | stores a float at `+0x1C`; object size `0x28` |
| `001F1E50` | `SetPrimIdEnableObj` constructor | 47 B | ledger name is a fold artefact |
| `001F1ED0` | `SetScreenIndexToPostProcessManagerObj` constructor | 47 B | ledger name is a fold artefact |
| `001F1F00` | `VideoObj` constructor | 33 B | |
| `001F28B0` | `AmbientOcclusionObj::Execute` | 257 B | gated on render params `+0x198` |
| `001F29E0` | `BegineSceneObj::Execute` | 50 B | the smallest execute body |
| `001F3090` | `GaussianFilterObj::Execute` | 370 B | gated on `+0x19A`, `+0x180`, `+0x3E8` |
| `001F32B0` | `MaskBorderObj::Execute` | 46 B | |
| `001F3300` | `PostProcessObj::Execute` | 313 B | compares its mode against the screen index |
| `001F3440` | `Ps2DofObj::Execute` | 154 B | |
| `001F34F0` | `RazorMarkerPushObj::Execute` | 16 B | |
| `001F39E0` | `VideoObj::Execute` | 30 B | |
| `001F2880` | order key `0x10` | 6 B | shared by the ordinary passes |
| `001F28A0` | order key `0x80` | 6 B | `VideoObj` |
| `0053DD10` | order key `1` | 6 B | folded stub; ledger name is unrelated |
| `00193D50` | render-parameter block getter | 66 B | the per-effect switches live behind this |
| `00189120` | render-target manager getter | 8 B | returns `01F7F598` |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01F7F5E8` | the render command list | `.data` | `RenderCommandList`, created on first use |
| `01F7F5E0` | the second command list | `.data` | every command is appended here too |
| `01F7F598` | render-target manager | `.data` | returned by `00189120` |
| `01DFE0C4` | **master render enable** | `.data` | a byte; ~~every execute body checks it~~ most execute bodies check it; `BegineSceneObj`'s `001F29E0` and `ApplyJsonForCutSceneObj`'s `001F29C0` do not *(corrected 2026-10-02, OPUS: both bodies read whole, 50 and 8 bytes, no `01DFE0C4` reference)* |
| `01F82EC0` | active screen index | `.data` | counted up by `PostProcessObj`'s constructor |
| `00902F90`–`009033F0` | the command vtable block | `.rdata` | **36 vtables, stride `0x20`** — corrected 2026-09-11: the range previously read `00902FB0`, which holds only 34. `00902F90` has the same three-code-pointer shape and `00902F70` does not, so the start is bounded on both sides and the page's count of 36 was right all along. Each record is 3 code slots **plus a fourth qword**; for 35 of the 36 that qword points into a `0x80`-stride array (below) |
| `01CEDAD8`–`01CEEBD8` | a per-command descriptor array | `.rdata` | **35 records of `0x80`**, one per vtable that carries a fourth-qword pointer — all 34 gaps are exactly 128 bytes. The 36th vtable's fourth qword is ASCII instead, which is what ends the array. Each record begins `01 00 00 00`, eight zero bytes, then three 32-bit addresses. ~~**What they hold is not established**~~ *(answered: see the falsification pass - each is a class's RTTI Complete Object Locator; checked 2026-10-02: `[00902FB0 - 8]` = `01CEDAD8`, signature 1 and a self RVA that is the record itself; 2026-10-02, OPUS)* |
| `009030B0` | `ApplyJsonForCutSceneObj` vtable | `.rdata` | |
| `00903050` | `CopyDepthBufferObj` vtable | `.rdata` | |
| `00903070` | `Ps2DofObj` vtable | `.rdata` | |
| `00903090` | `SetScreenIndexToPostProcessManagerObj` vtable | `.rdata` | |
| `00903150` | `RenderOpaqueObj` vtable | `.rdata` | |
| `00903170` | `RenderAfterWaterObj` vtable | `.rdata` | |
| `00903190` | `MaskBorderObj` vtable | `.rdata` | |
| `009031B0` | `RenderSSSObj` vtable | `.rdata` | |
| `009031D0` | `PostProcessObj` vtable | `.rdata` | |
| `009031F0` | `AmbientOcclusionObj` vtable | `.rdata` | |
| `00903210` | `GaussianFilterObj` vtable | `.rdata` | |
| `00903250` | `CopyFrontBufferForChrRefraction` vtable | `.rdata` | |
| `00903270` | `CopyFrontBufferForWaterRefraction` vtable | `.rdata` | |
| `009032B0` | `VideoObj` vtable | `.rdata` | |
| `009032D0` | `RazorMarkerPushObj` vtable | `.rdata` | |
| `009032F0` | `RazorMarkerPopObj` vtable | `.rdata` | |
| `00903370` | `SetPrimIdEnableObj` vtable | `.rdata` | |
| `00902FB0` | `BegineSceneObj` vtable | `.rdata` | |
| `00902FD0` | `EndSceneObj` vtable | `.rdata` | |

## 4. Data structures and formulas

### 4.1 The complete command class block

Thirty-six vtables, contiguous, stride `0x20`, three slots each, in address order:

```
00902F90  SetRendererCameraObj
00902FB0  BegineSceneObj                          (spelling is the engine's)
00902FD0  EndSceneObj
00902FF0  BegineScene0Obj
00903010  EndScene0Obj
00903030  CopyBufferObj
00903050  CopyDepthBufferObj
00903070  Ps2DofObj
00903090  SetScreenIndexToPostProcessManagerObj
009030B0  ApplyJsonForCutSceneObj
009030D0  ReadPresetDofForCutSceneObj
009030F0  RenderMonsterGalleryChara
00903110  MonsterGallerySoftParticleEnable
00903130  RenderMapOpaqueObj
00903150  RenderOpaqueObj
00903170  RenderAfterWaterObj
00903190  MaskBorderObj
009031B0  RenderSSSObj
009031D0  PostProcessObj
009031F0  AmbientOcclusionObj
00903210  GaussianFilterObj
00903230  CopyFrontBufferForVFXObj
00903250  CopyFrontBufferForChrRefraction
00903270  CopyFrontBufferForWaterRefraction
00903290  ZBufferObj
009032B0  VideoObj
009032D0  RazorMarkerPushObj
009032F0  RazorMarkerPopObj
00903310  FastClearObj
00903330  DisableMsaaObj
00903350  EnableMsaaObj
00903370  SetPrimIdEnableObj
00903390  EnableDofObj
009033B0  SetDofObj
009033D0  GiResetRenderTargetObj
009033F0  GiResetDefaultRenderTargetObj
```

Two of those names are worth reading twice. **`ApplyJsonForCutSceneObj`** and
**`ReadPresetDofForCutSceneObj`** say the game applies **JSON**-authored render settings, and
depth-of-field presets, per cutscene — and `ApplyJsonForCutSceneObj` is enqueued at frame open
(`001EC490`), every frame, not only during cutscenes. **`RenderMonsterGalleryChara`** and
**`MonsterGallerySoftParticleEnable`** are the Sky Pirate's Den bestiary viewer, which gets two
dedicated render commands of its own.

### 4.2 The push_back, exactly

```c
// inline in every enqueue function; 0018AFF0 is the out-of-line copy, 58 B
p = list->pEnd;
if (p < list->pCapacityEnd) {
    list->pEnd = p + 1;
    if (p != NULL) *p = node;
} else {
    FUN_001AB570(list, p, &node);    // reallocate, move, insert
}
```

The `p != NULL` test inside the fast path is dead in practice — `p` was just compared against
`pCapacityEnd` — and is the signature of a hand-written EASTL `push_back` with a null-guarded
store, not of a compiler-generated one.

### 4.3 The order keys

```c
orderKey(cmd) = cmd->vftable[2]()      // a constant per class
```

| key | classes proven to carry it | consequence |
|---:|---|---|
| `1` | `RazorMarkerPushObj`, `BegineSceneObj` | runs before the render passes |
| `0x10` | `PostProcessObj`, `Ps2DofObj`, `GaussianFilterObj`, `AmbientOcclusionObj`, `MaskBorderObj` and ~~the other ordinary passes~~ most other ordinary passes; `RenderOpaqueObj`, `RenderAfterWaterObj`, `RenderMapOpaqueObj` and `RenderMonsterGalleryChara` carry `0x100` *(corrected 2026-10-02, OPUS: `001F2890`, their shared slot 2, is `mov eax, 0x100`)* | the main body of the frame |
| `0x80` | `VideoObj` | ~~composited last, over everything~~ its mask value; where it draws follows its enqueue position *(corrected 2026-10-02, OPUS: `0018B100`+0x67 `test dword ptr [rsi + 0x20], eax`)* |

Only the three values above were read. ~~The remaining classes in §4.1 were not opened in this~~
~~pass and their keys are unknown; see §7.~~ *(answered: see §7, answered 2026-09-12 - all 36 read, and the §2.5 matrix; 2026-10-02, OPUS)*

### 4.4 The per-effect switches

```c
AmbientOcclusionObj runs   <=>  *(u8*)(renderParams + 0x198) != 0  &&  *(u8*)0x01DFE0C4 != 0
GaussianFilterObj runs     <=>  ( *(u8*)(renderParams + 0x19A) != 0
                               || *(u8*)(renderParams + 0x3E8) != 0
                               || *(u8*)(renderParams + 0x180) != 0 )
PostProcessObj body runs   <=>  *(u8*)0x01DFE0C4 != 0
where renderParams = FUN_00193D50()
```

## 5. Call chain

```
the frame                                   see 22-Middleware-PhyreEngine/The-Frame/
  -> MainLoop_Draw  0022B0B0
     -> pass gate: (022C7F90[drawMode] >> bit) & 1
        -> pass wrapper           e.g. 00182970  (44 B)
           -> 0018CA40            fetch the command list
           -> enqueue fn          e.g. 0018C610  (148 B)   <- HANDOFF, not an owner transition
              -> malloc + constructor  e.g. 001F1B80
                 -> 00212CC0      OrderedObject base
              -> push_back onto 01F7F5E8
              -> push_back onto 01F7F5E0   (via 0018B4E0 / 0018AFF0)
                 ~~~~~ the frame's involvement ends here ~~~~~
                 later: the list is ordered by slot 2 and each slot 1 is executed   <- corrected 2026-10-02, OPUS - nothing orders it: the walk 0018B100 runs it in stored order and ANDs slot 2 with the list's mask (0018B100+0x67)
                    -> execute reads FUN_00193D50() switches and 01DFE0C4
                       -> the GS command stream  (see The-Frame doc §2.5)
```

**Why that row says HANDOFF and not `[OWNER TRANSITION]`, corrected 2026-09-18 (OPUS).** It used to read `<- OWNER TRANSITION: frame -> command list`. Under `CALL-CHAINS.md` rule 6 an owner transition names two owners from the category vocabulary, and **both sides of this hop are 17-Presentation-Rendering** - `0022B0B0`, `00182970`, `0018CA40` and `0018C610` are all this subsystem's own draw path. The handoff is real and the line above it (`the frame's involvement ends here`) is the useful part; what it is not is a crossing between owners. Labelling it `[AUTHORITY 17 -> 17]` would have satisfied a checker and told a reader nothing.

**Upstream (who causes this):** `MainLoop_Draw`, and the frame-open helpers `001EC490` and
`001829A0`. Every producer is a pass wrapper; none of them is more than 70 bytes.

**Downstream (what this causes):** a list of heap-allocated command objects. Nothing is drawn at
enqueue time.

**Do not confuse with:**

- **The GIF command buffer.** The frame also fills a flat, double-buffered array of 16-byte
  `(data, register)` records — no vtables, no allocation, no ordering. That is a different
  structure at `02EBEFC0`, described in
  [what-happens-between-two-frames.md](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)
  §2.5. A command object is an instruction to *do a pass*; a GIF record is one register write.
- **The `Gi*` family.** `GiResetRenderTargetObj` and `GiResetDefaultRenderTargetObj` sit inside
  this vtable block and are `*Obj` classes by name. The other sixteen `Gi*` classes documented in
  [gi-render-command-family.md](../Gi-Render-Commands/gi-render-command-family.md) are **two-slot**
  classes at `00904488`, `009007E8` and `01CCFA00`–`01CCFBA8`, and that document describes them
  executing against a **device vtable**. Every class in *this* block has **three** slots and the
  third is an order key. They are adjacent and they are plainly related, but *"adjacent" is not
  evidence* — whether the `Gi*` objects are appended to this same list was not proven here and
  is recorded in §7.

  **That document reached part of this independently, and it is worth saying which part.** A
  search of it for all 36 class names in §4.1 returns exactly two — the two it owns — which it
  already identifies as **three-slot**, the same contract found here from the other 34. It also
  already cites `GeometryInstanceOrderedObject` (vtable `00903920`), an `OrderedObject` subclass,
  at its §16. So the two documents independently agree on the slot count for the overlap and both
  have touched the `OrderedObject` family. **Its census is correct within its own scope** — the 18
  `Gi*` classes — and the 34 uncovered classes are a scope gap in a neighbouring block, not an
  error in it.
- **`OrderedObject` is not `CharacterRenderObject`.** `CharacterOrderedObject` (`00903940`) and
  `GeometryInstanceOrderedObject` (`00903920`) are three-slot `OrderedObject` subclasses in the
  same neighbourhood, but `CharacterRenderObject` (`00903B68`) is documented separately in
  [character-render-object.md](../Character-Rendering/character-render-object.md) and is a
  different kind of thing.

## 6. Modding notes

- **Best intervention point for turning one effect off:** the byte switches behind
  `FUN_00193D50()` — `+0x198` for ambient occlusion, `+0x19A` / `+0x180` / `+0x3E8` for the
  gaussian filter. These are read fresh on every execute, so a write takes effect the same frame
  and nothing needs invalidating. It is a strictly better seam than the pass-enable bitmask in
  the frame, because it stops the *work* while leaving the command list structurally intact.
- **Best intervention point for turning everything off at once:** `01DFE0C4`. ~~Every execute body~~
  ~~read in this pass checks it.~~ Most execute bodies check it; `001F29E0` (`BegineSceneObj`) and `001F29C0` (`ApplyJsonForCutSceneObj`) do not *(corrected 2026-10-02, OPUS: both read whole)*.
- **Best intervention point for changing layering:** ~~slot 2 of a class's vtable. Returning a~~ the enqueue order *(corrected 2026-10-02, OPUS: `0018B100`+0x67 `test dword ptr [rsi + 0x20], eax`; no comparator runs)*.
  ~~larger constant moves that pass later. This is a 6-byte function per class and it is the only~~
  ~~thing that determines order — the enqueue sequence does not.~~ Slot 2 is ANDed with each walk's mask, so changing it changes which walks run the pass, not its place.
- **Regenerates itself — do not write directly:** the list pointers at `01F7F5E8` / `01F7F5E0`,
  and `01F82EC0`, which `PostProcessObj`'s constructor recomputes from scratch every time a
  post-process command is created.
- **Breaks if:** you free a command object yourself. Each one is appended to **two** lists, so a
  single free leaves a dangling pointer in the other.
- **Breaks if:** you enqueue from a thread other than the one running the frame. The `push_back`
  is unguarded — no lock, no atomic, and a plain grow-and-copy at `001AB570` when capacity runs
  out.
- **Multiplayer / XIIOnline:** every object here is **local presentation state**. Two clients may
  legitimately hold entirely different command lists for the same world state — different
  effects enabled, different screen index, different video overlay. Nothing in this document is
  authoritative world state and none of it should be replicated.
- **Mod compatibility:** `ApplyJsonForCutSceneObj` and `ReadPresetDofForCutSceneObj` indicate
  authored JSON render settings, which is the file-level seam other mods are most likely to touch.
  **The files are now established (§7, UQ-232): `JsonData/init.json` holds the defaults, and
  `JsonData/CutScenes/<scene>.json` (plus a `_2ndScreen` twin) overrides them per cut.** A key absent
  from a sidecar falls back to `init.json`, so editing `init.json` moves every cut that does not
  override it. `JsonData/0.json` is the editor's hot-reload pointer and ships empty.

## 7. What is not known

- [x] ~~**UQ-228.** Where the list is sorted and executed. The producer side is complete; no consumer of `01F7F5E8` or `01F7F5E0` that
      walks `01F7F5E8` or `01F7F5E0` was located in this pass. (`PROPOSED-xiionline-13-7`)~~ **Answered 2026-09-14 (FABLE): it is executed in stored order, and it is not sorted.** The consumer is reached through the getter of `01F7F5E0` (78 raw call sites), which the earlier census did not follow.
      - **The render pass runs it in two parts.** It calls the walker `0018B100(list, part, device)` twice:
        - at `00187D05` with part 1, over entries `[0, split)`;
        - at `00188128` with part 0, over `[split, count)`.
        For each entry the walker calls vtable slot 2 (`+0x10`) and ANDs the result with the list's mask `+0x20`. On a hit it calls slot 1 (`+8`) with the device (`0018B150`–`0018B187`).
      - **The split.** The split `+0x24` is set by `0018B510`, to 0 or to the current count. A clear resets it to 0 (`0018B050`); its call sites are the frame tick `0017CD53`, the end of the render pass `00188204` and `001E05A9`.
      - **Class-filtered walks.** A second walker, `0018B1B0(list, device, classMask, reverse)`, is called from six sites (`001F07C7`, `001F3549`, `001F35D0`, `001F361B`, `001F3689`, `001F370C`) with masks 2, 4 or a computed value. Four of them set `reverse`, which walks from the last entry down. An entry runs only when slot 2 matches both the caller's mask and the list mask (`0018B24A`–`0018B25E`).
      Neither walker sorts. No comparator call was found in the manager methods read (`0018AD00`, `0018B040`, `0018B070`, `0018B100`, `0018B1B0`, `0018B510`).
- [x] **UQ-229.** Why every command is appended to **two** lists, and what distinguishes `01F7F5E8` from
      `01F7F5E0`. (`PROPOSED-xiionline-13-8`)
      **Narrowed 2026-09-14 (FABLE): they are two different kinds of object.**
      - **`01F7F5E0` is the execution manager.** It is a `0x30`-byte object created lazily by `0018B480` through `0018AD00`, which sets the mask `+0x20` = `0xFFFFFFFF` and the split `+0x24`. It holds the entry vector at `+0`/`+8`/`+0x10`, the mask, the split, a flag `+0x28` and a bound `+0x2C`. The walkers above run it.
      - **`01F7F5E8` is an EASTL vector.** It is a `0x20`-byte object created lazily by `0018C9E0`, whose allocator name is the literal `"EASTL vector"` (`008C5F58`).
      - **A producer does both.** `0018B540`, for example, allocates the command, pushes it into the vector its caller passes (`0018B58C`–`0018B5B0`, growing through `001AB570`), then hands it to the manager (`0018B5B5`).
        *Corrected 2026-09-15 (FABLE): the command is not uniformly `0x20` bytes.* The size argument at each builder's
        `0085E730` call is **`0x18` for eleven of the nineteen builders, `0x20` for seven and `0x28` for one** *(scope named 2026-10-02, OPUS: the nineteen of §2.3; over all 36 builders the size is `0x18` x 15, `0x20` x 16, `0x28` x 3 and `0x30` x 2 (`0018B710`+0x37 and `0018B8B0`+0x2E `lea ecx, [rdx + 0x30]`), the last `ecx` write before each `call 0085E730`)*
        (`0018B970`). `0018B540`'s own is `0x20` (`lea ecx, [rdx + 0x20]` at `0018B55F`), which is why the single
        example read as the general case. See `UQ-234` in §7 for what the three sizes say about the layout.
      - ~~**Not established:** whether the caller's vector is always `01F7F5E8`, and why the engine keeps both.~~
        **UQ-229 answered 2026-09-15 (FABLE) — both halves. The vector OWNS the commands; the manager
        SCHEDULES them.**
        - **The caller's vector is always `01F7F5E8`, checked the strict way.** The global has exactly
          **three** accesses in the image: the lazy creator `0018C9E0` tests and stores it, and
          `0018CA40` (8 B) reads it. Nothing takes `0018CA40`'s address — no 8-byte or 4-byte pointer
          to it exists anywhere in the mapped image — so the getter is the only route. At **all 20**
          enqueue call sites, the **last write to `rcx` before the call** is `mov rcx, rax`
          immediately after `call 0018CA40`; proximity was not enough, so each body was decoded in
          order and the definition tracked. No enqueue receives a different container.
        - **Why both: they are cleared differently, and that is the whole reason.** A producer that
          allocates pushes the node into **both** — the same `{begin, end, capacity}` push_back idiom
          at `+0`/`+8`/`+0x10`, inline for the vector (`0018B58C`–`0018B5B0` in `0018B540`) and through
          `0018AFF0` for the manager. What differs is the reset:
          - **`0018B810(vector)` destroys.** It walks `[begin, end)`, and for every non-null node loads
            the vtable and calls **slot 0 with `edx = 1`** (`0018B858`–`0018B860`) — the scalar
            deleting destructor, i.e. *free the object* — then pulls the end pointer back to the begin
            (`0018B88C`–`0018B89F`). Its callers are the frame tick (`0017CD60`) and the end of the
            render pass (`00188211`).
          - **`0018B040(manager)` does not.** It calls `0018B3F0(manager, 0)`, which resizes the entry
            array to zero, and then resets the split `+0x24` to `0` and the bound `+0x2C` to
            `0xFFFFFFFF` (`0018B050`–`0018B057`). **No destructor runs.**
        - **So the split is ownership versus schedule.** `01F7F5E8` is the frame's owner: every
          allocation is registered there and every one is destroyed there, once. `01F7F5E0` is the
          frame's schedule: the same pointers plus the mask `+0x20`, the split `+0x24`, the flag
          `+0x28` and the bound `+0x2C`. That is what lets the render pass re-split the schedule, mask
          it, and run class-filtered and reversed walks over it (§4.3) **without any of that touching
          object lifetime** — and it means dropping a command from the schedule cannot leak it,
          because the vector still owns it.
        - ***Corrected the same day, 2026-09-15 (FABLE): not every appender pushes into both — and
          the exception is the split's strongest evidence.*** The first version of this answer said
          *"each producer pushes the node into both"*. `0018AFF0` is the only append to the manager
          and nothing takes its address, so its callers are the whole population: **40 bodies**, not
          the 19 builders §2.3 tables. Of those:
          - **36 allocate their own node and push it into a vector** — every one calls the allocator
            `0085E730` and carries the grow path `001AB570`.
          - **4 push into no vector at all**, appending to the manager only. *Corrected 2026-09-15
            (FABLE), same day: an earlier wording said all four "allocate nothing", which is true of
            two of them.* **Two allocate nothing** — `001E5270` (31 B; its only callees are
            `0018B4E0` and `0018AFF0`) appends `[this+0x10]`, and `001F89B0` (42 B, same two callees)
            appends `[this+0x28]` when non-null. **Two allocate from a POOL rather than `malloc`** —
            `001F48B0` (149 B) and `001E8580` (3,572 B) both take their storage from `001A1470` on the
            pool at `01F7F4C0`, never from `0085E730` (`malloc`), which is why the `malloc` test put
            them in this bucket. `001E8580` additionally appends sub-objects embedded in its own
            `this`: `this + 0x2300` at `001E8A24` and array elements `this + (idx + 0x9E) × 0x20` at
            `001E866B`. **What holds for all four, and is the load-bearing point, is that none of
            them pushes into the vector.**
          **That is exactly what an ownership/schedule split predicts, and it is a passing
          falsification test.** If the vector were merely a second index, a body registering an object
          it does not own could push to either. Instead **not one** of the four non-allocating
          appenders touches the vector — because the vector destroys what it holds, and these objects
          are embedded in, or owned by, something else. Appending them to the manager schedules them
          for the frame without handing them to a destructor.
        - ~~**Not established:** whether any path clears the manager without the vector also being~~ *(answered: see CONTRACT-render-command-list-and-graphics-handshake.md I-2 - all three clears are followed by a destroy or a flush, `0017CCD0`+0x83/+0x90, `00187950`+0x8B4/+0x8C1, `001E0590`+0x19/+0x26; 2026-10-02, OPUS)*
          destroyed in the same frame. *(The four registered objects' classes are no longer open — they
          are in `UQ-231` below.)*
- [x] ~~The order keys of the 28 classes in §4.1 whose slot 2 was not opened.~~
      (`PROPOSED-xiionline-13-9`) — **ANSWERED 2026-09-12 (OPUS)**: all 36 read, five distinct slot-2
      implementations, in the falsification pass below. A fourth value `0x100` and two classes whose
      key is a per-instance field were found.
- [x] ~~**UQ-230.** **What comparator orders the list, and in which direction.** All 36 key values are now known
      (`1`, `0x10`, `0x80`, `0x100`, and two per-instance), but §4.3's consequence — `VideoObj` at
      `0x80` being "composited last, over everything" — cannot follow from a key that four classes
      exceed with `0x100`. Depends on `-13-7`. (`PROPOSED-xiionline-13-14`)~~ **Answered 2026-09-14 (FABLE): none; the list is not ordered by key.** The slot-2 value is a class **mask**, not a sort key.
      - **How it is used.** Both walkers AND it with the list mask (`0018B167`, `0018B25B`). The second walker also ANDs it with its caller's mask (`0018B24A`).
      - **Who changes the mask.** The list mask starts as all ones, and the only other writer found, `0018B070`, sets or clears bit `0x2`; it is called from the developer console body.
      - **Direction.** Execution is stored order, forward in the render pass's two parts. It is backward only when a class-filtered walk sets `reverse`, which four of its six callers do.
      - **Consequence.** §4.3's *"`VideoObj` at `0x80` composited last"* does not follow. `0x80` selects which walks run the object, not when it runs within one.
- [x] ~~**UQ-231.** Whether the sixteen two-slot `Gi*` classes are appended to this same list. They share the
      vtable neighbourhood and the command-object idiom, but have a different slot count and a
      documented device-vtable execution path. Verified by search, not assumed: of the 36 classes
      in §4.1 that document names **two**, so **34** are uncovered. (`PROPOSED-xiionline-13-10`)~~
      **UQ-231 answered 2026-09-15 (FABLE): no — and the reason is the base class, not the slot count.
      A `GeometryInstance` reaches this list only through an adapter.**
      - **The RTTI settles it.** A base-class census over the complete-object locators finds **18**
        `Gi*` classes. **Sixteen derive from `GeometryInstance`** and have two slots — `GiBeginScene`
        (`00904488`), `GiEndScene` (`009044A0`), `GiVmax` (`009007E8`), `GiSetRtForRtSampling`
        (`00902F28`), `GiScreenImage` (`009068B8`), and eleven more at `01CCFA00`–`01CCFBA8`
        (`GiTrans`, `GiTransNz`, `GiSetTexture`, `GiColorRect`, `GiPrim`, `GiSprite`, `GiPolyGT4T`,
        `GiZNormalOnOff`, `GiBeginEff`, `GiNormal`, `GiEndEff`). **Two derive from `OrderedObject`**
        and have three: `GiResetRenderTargetObj` (`009033D0`) and `GiResetDefaultRenderTargetObj`
        (`009033F0`) — the two §4.1 already owns. **So the sixteen are not `OrderedObject`s at all**,
        and the question of whether they are "appended too" does not arise: they are a different
        hierarchy that happens to be filed nearby.
      - **The adapter, which is the useful half of the answer.** A non-`OrderedObject` host does not
        enter the list; it **registers an `OrderedObject` companion**. Three instances, all found as
        the manager-only appenders of `UQ-229`:
        | host class | slots | base | registrar | what it appends |
        |---|---:|---|---|---|
        | `GeometryInstance` (via its owner) | — | — | `001F48B0` | a pool-allocated `GeometryInstanceOrderedObject` (`00903920`, 3 slots, base `OrderedObject`) |
        | `MapRenderObject` | 2 | `RenderObject` | slot 1 = `001E5270` | `[this+0x10]`, its `MapOrderedObject` |
        | `CharacterRenderObject` | 31 | `RenderObject` | slot 1 = `001F89B0` | `[this+0x28]`, its `CharacterOrderedObject` |
      - **A structural corroboration, offered as such and not as the proof.** Both walkers call
        **slot 2** (`+0x10`) on every entry and AND the result with a mask (§4.3). A two-slot class has
        no slot 2, so a `GeometryInstance` in this list would have its third vtable qword read as a
        function pointer. The base-class census is the evidence; this only says the design is
        consistent with it.
      - **Scope note the old row asked for.** §4.1's "36" and the RTTI's **42** direct `OrderedObject`
        subclasses are both right — §2.5 already reconciles them. The 34 the `Gi*` document does not
        cover were never its scope: it owns the `GeometryInstance` hierarchy, this page owns
        `OrderedObject`, and `GeometryInstanceOrderedObject` is the seam between them.
- [x] ~~**UQ-232.** Which files `ApplyJsonForCutSceneObj` reads, and what the JSON contains.
      (`PROPOSED-xiionline-13-11`)~~ **UQ-232 answered 2026-09-15 (FABLE): it reads no file. It is the
      per-frame *apply* step over a document two other functions load, and the document is a cutscene's
      render-settings sidecar.**
      - **The command carries one integer and ignores the device.** The constructor `001F1770` stores its
        `edx` at `+0x18` and zeroes the byte at `+0x10`; slot 1 (`001F29C0`) is two instructions —
        `mov ecx, [rcx+0x18]` then `jmp 001C3C30` — so the walker's device argument never reaches the body.
        Slot 2 (`001F2880`) returns the constant `0x10`, the class mask §4.1 already records.
      - **Both enqueue sites are in the image and their arguments are literals.** `001EC490` has exactly two
        callers: `0022A5C1` inside `0022A580` with `xor ecx, ecx`, and `0022B120` inside `MainLoop_Draw`
        with `ecx = ebx` under `cmp ebx, 1`. So the frame enqueues the command twice, with **0 and 1**.
      - **The argument selects a screen, not a file.** In the loader `001C6E20` the argument picks the bank
        (`0` → `01F813A8`, `1` → `01F813D8`, anything else → no bank) and gates the name test: for `0` a name
        containing `"2ndScreen"` is **erased**, for `1` a name *not* containing it is erased
        (`001C6FE4`–`001C7041`, needle `008FA3B8`). Bank 0 is therefore the main screen and bank 1 the second.
      - **Which files.** Three, all under `JsonData/`, and none of them named by this command:
        - `001C5930` builds `JsonData/CutScenes/<scene>.json` and `JsonData/CutScenes/<scene>_2ndScreen.json`
          and parses them into the two banks at `001C5D6F` and `001C5D8E`. It reloads only when the scene
          name changes (`001C50C0` against the cached name at `01F812A8`/`01F812B0`, compared by `00861ED2`).
          **These are the files the command's document comes from.**
        - `001C3760`, at boot from `00186CD0` (interior read 2026-09-17, SWE2-FRONTIER: 1,240 B — `"te shadowmap"` string, `001EE040` ×14 + `00182E80`/`00182EB0` ×11 setter pairs, first call [`00186CFB`](../../_index/ADDRESS-INDEX.md)), parses `JsonData/init.json` — and `001C3760` itself reads 2026-09-17 (SWE2-FRONTIER): the `JsonData/init.json`/`JsonData/MonsterGallery.json` literals + `EASTL basic_string` diagnostics in-body, `001EDF00`/`001FF740`/`00200BE0`/`00202880` profile confirmed, first call `001C378E` into `01F813C8` and
          `JsonData/MonsterGallery.json`, and **clears** `01F81328` through `00202880`, which frees the value
          and writes type `6`.
        - `001C6E20`, the body behind `ReadPresetDofForCutSceneObj`, parses `JsonData/0.json` and takes its
          `"ChangedFileName"` member as the sidecar to reload. **`0.json` ships as the two bytes `{}`**, so in
          the shipped data that member is absent, the name is empty, the path degrades to the bare directory
          `"JsonData/CutScenes/"`, and no document is produced by this route. It is an editor hot-reload probe.
      - **A JSON value is 16 bytes and the type tag is at `+0`.** `001FE8B0` writes type `6` with a null
        payload; `00200BE0` is `type == 6`, i.e. *absent*; `00200BA0` returns `[node+8]` for type `0` and
        otherwise the shared empty string at `01F83130`. Each bank is two such values, indexed by the parity
        at `01F813F8`, so a reload never tears a document the frame is reading.
      - **What the JSON contains, and the lookup order.** `001C3D50` (4,607 B) reads **103 distinct key
        names** — 94 through `001C51D0`, six cascade names through `001C52C0`, and `mChrShadowDepthBias`,
        `mChrShadowSlopeOffset`, `mUseSubCameraForShadow` through `001FF740` directly. `001C51D0` is a
        **four-step fallback**: the current `Cut N` section (`001FF6B0` with the name string at `01F812E0`),
        then the document's `"Common"`, then `01F81328`, then `01F813C8`. Since boot clears `01F81328` and
        fills `01F813C8` from `init.json`, the last two steps are *the defaults document*.
      - **Measured against the shipped data** (337 sidecars in `JsonData/CutScenes/`, of which 26 are
        zero-byte `sum_*` files and `evt_t0005.json` is refused by a strict parser for a delimiter, leaving
        310 parsed; 282 carry a `Common` and there are 3,498 `Cut N` sections in all; `init.json` holds 176
        keys): **every one of the 103 keys has a shipped source.** 99 are in `init.json`, 68 are authored in
        at least one sidecar, 64 in both, 4 only in a sidecar
        (`enableLightInfo`, `mCascadePartition0`/`1`/`2`), 35 only in `init.json`, and **none in neither**.
        Seventy-seven of `init.json`'s keys are not read by this applier.
      - **A miss is not free: the lookup helper is a **mutating** `operator[]`.** `001FF740` delegates to
        `001FF6B0`, which, on a node that is not type `3`, destroys it, allocates a `0x38`-byte EASTL map
        (allocator name `"EASTL map"`, `008F4120`) and stores it at `+8`, then indexes it — inserting the key
        when it is absent. So each of the four fallback steps that misses **grows the in-memory document by a
        null entry**; the read still behaves as a fallback because `00200BE0` tests the returned node, and
        `00200B50` yields `0.0f` for any type that is not `1` or `2`. Nothing is written back to disk.
      - **The applier runs only under a gate, and the gate is a conjunction.** `001CC600` (from `0017D6E0`)
        sets `01F81280` to 1 only when `002F1A20`'s flag `022BE7C8` is non-zero **and** `0022A550` is, which
        needs the mode byte `02064AD3` to equal 2 and `00358330(1)` to be non-zero. It first copies the old
        value to `01F81281`, and `001C3C30`'s first-time block runs on the `0`→`1` edge only.
      - **Residue closed 2026-09-15 (FABLE): `ReadPresetDofForCutSceneObj` is not dead — it is
        constructed and enqueued.** This answer left it open because `001F1CB0`'s one caller
        `0018C200` had not been followed. `UQ-229`'s census then found `0018C200` in the list of
        **36** bodies that `malloc` a node and append it to the render manager. The chain, read from
        the bytes: `0034C7E0` → `001EC620`, which sets the current-slot latch `01DFE40C` (`UQ-341`),
        fetches the vector through `0018CA40` and tail-jumps to `0018C200` → `0085E730(0x20)` → ctor
        `001F1CB0` → vtable `009030D0` → pushed into both containers. **Where the trace stops, named:**
        `0034C7E0` has no `rel32` caller — it is reached through a pointer stored at `01EF8B00`, one
        slot of an undocumented **`0x20`-stride registration table** (neighbours at `01EF8AE0` and
        `01EF8B20`, each a function pointer followed by three zero qwords). What registers that table
        is not read here.
      - ~~**Not established:** what `0022A550`'s mode value 2 names — that is `GA-4`.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **GA-4** was answered on 2026-09-17. `02064AD3` is the main loop's frame mode, and 2 is the field/battle frame.*
- [x] **UQ-233.** *(status restated in the register 2026-09-26, FABLE, Claude Opus 5.5: see the row)* What the render-parameter block at `FUN_00193D50()` is as a record. Four byte offsets are
      proven to be effect switches; the block's extent and the rest of its fields are unread.
      (`PROPOSED-xiionline-13-12`)
      *Narrowed 2026-09-14 (FABLE), not answered: the extent is known.* `00193D50` allocates **`0x4A8`** bytes on first use and
      caches them at `01F7F5F0`. It is the post-process parameter context that every one of the twelve post-process passes
      takes as its first argument, and it carries the SMAA quality at `+0x184` and the two AO parameter blocks
      ([post-process passes](../../22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md),
      `EA-2`). The field map beyond those is largely unread.
      ***Five more offsets, 2026-09-15 (FABLE) — the depth-of-field group, and a second name for the object.***
      `00194250` (51 B) is the DOF setter and writes five fields of this record in one call:
      `+0x110` the **enable byte** (`mov [rcx+0x110], dl`), `+0x114` the **focus distance**, `+0x118` the
      **aperture f-number**, `+0x11C` and `+0x120` the two floats its caller passes on the stack. Both of its
      callers read `+0x11C` back **before** the call and hand it straight in, so `+0x11C` is preserved and
      `+0x120` receives the constant `35.0f` at `008F312C`. The ~~two~~ callers are four functions, five sites *(corrected 2026-10-02, OPUS: `001C3D50`+0x499 and +0x551, `001C5750`+0x177, `001C7940`+0x24E, `001F38B0`+0x45)*: `001C3D50`'s PresetDof arm
      (§7, `UQ-232`) and `001C5750`, the `sum_` bank's sidecar reader (`UQ-247`).
      ***Field census done 2026-09-17 (SWE2-STRUCT).*** The block is declared in the type store as
      **`PostProcessParamContext`** (size `0x4A8`, `PTR 0x01F7F5F0`/`0x01F81300`, ctor `0018CD90`), and its
      census is `postprocess-context-accesses.tsv` beside this page — ~~776~~ 777 sites *(corrected 2026-10-02, OPUS: the `+0xEE` section added the global-slot read; recount of the TSV, 777 rows)* over 219 distinct offsets,
      built by tracking the context pointer through argument registers and stack-argument slots into 95
      callee bodies plus the whole constructor chain (`Tools/work/SWE2-STRUCT/uq233_census.py`). The map:
      five intrusive list sentinels at `+0x00`/`+0x10`/`+0x28`/`+0x38`/`+0x88`; a `0067FFB0`-registered block
      at `+0x50`; dword param block `+0xA4`–`+0xE8`; the DOF group `+0x110`–`+0x120`; SMAA quality `+0x184`,
      AO enable `+0x198`, AO implementation `+0x344`; the render size `+0x2E0`/`+0x2E4` (1920×1080 at
      construction); a ~~polymorphic subobject~~ **`PFXAA` (`CON-198`)** `+0x378`–`+0x3E7` (~~two vtable qwords~~ **its vtable `00D625D0` and class descriptor `02D35FA0`**, init `00645DB0`→`006461B0`);
      the SMAA gate bytes `+0x3E8`/`+0x3E9`; two `0x28` param blocks `+0x3F0`/`+0x418` (`00615CD0`→`005DC400`);
      a 64-byte zeroed block `+0x440`; and the tail `+0x480`–`+0x4A3` ending in the PostAA byte.
      **The qword band `+0x200`/`+0x278`–`+0x328` is the bound render-object array** (named
      2026-09-18, `SWE2-STRUCT-PPC-BOUND-OBJECTS`): 23 slots written once by the setup
      `0018D850`/`0018F510` from factory results — `001EE040(renderWidth, renderHeight, descriptor)`
      for the `+0x280`–`+0x2C8` run (descriptors at `02CF7480` and a caller param), `00649C20` for
      `+0x300`/`+0x328` — and read back by the render methods as call receivers; four slots
      (`+0x2E8`/`+0x2F8`/`+0x308`/`+0x310`) are ctor-seeded with the same `rdi` first. `+0x49C` is
      `contextIndex`, a ctor-set signed dword the render methods sign-extend as an index (25 sites).
      96 of the 145 store rows are UNRESOLVED by name — the map is measured, the array's per-slot
      effect identity is not yet claimed.
      **The object has two globals, and they are the same object:** `0015CAF0` is
      `01F81300 = 00193D50()`, so every citation of `[01F81300]` on this page and on the audio page is a
      citation of the `0x4A8` record cached at `01F7F5F0`. The class NAME remains unrecovered (no vtable on
      the outer object, no RTTI) — that residual is `EA-2`'s.
      ***Narrowed again 2026-09-26 (FABLE, Claude Opus 5.5) — what the record IS: the scene's render-parameter set,
      loaded from the shipped per-map and per-cutscene JSON under the fields' own names.*** Static plus the data.
      - **The loaders.** The cutscene-JSON loader `001C3D50` reads keys from `jsondata/cutscenes/*.json` (283 of 337 files
        carry them), and a map-JSON loader reads `jsondata/maps/*.json` (459). Both write this record through small
        setters called on `[01F81300]`.
      - **Fields named from the keys.** Each row below was read at the cutscene loader's call site: the key string's
        `lea`, the getter's result register, and the setter's store.

        | offset | key | setter |
        |---|---|---|
        | `+0xF0` | `mGammaValue` | `00194300` |
        | `+0xF4` / `+0xF8` | `mGlareLuminance` / `mGlareThreshold` | `00194310` |
        | `+0x110` / `+0x114` / `+0x118` | `EnableDof` (== 1) / `mDofFocusDistance` / `mDofApertureFnumber` | `00194250` (the group above) |
        | `+0x188` | cleared to 0 on every call | `00194A00` |
        | `+0x18C` / `+0x190` / `+0x194` | `mUSMBlur` / `mUSMIntensity` / `mUSMThreshold` | `00194A00`; with `EnableUSM` off the loader passes `1.2` / `0.45` / `0.04`, the JSON defaults |
        | `+0x1A8` / `+0x1AC` / `+0x1B0` | `mSAOBiasChr` / `mSAORadiusChr` / `mSAOIntensityChr` | `001949C0` |
        | `+0x1B4` / `+0x1B8` / `+0x1BC` | the same three, `…Sce` | `001949E0` |
        | `+0x1E9` | `AODepthFullRes` (!= 0) | `00193F70` |
        | `+0x330` | `mMotionBlurEnabled` (== 1) | `001944C0` |

      - **By the same instruction pattern, not re-read site by site.** The HBAO pair `00194330` / `00194350` fills
        `+0x1C4`–`+0x1CC` (`mHBAOBias`/`Radius`/`IntensityChr`) and `+0x1D0`–`+0x1D8` (the `…Sce` three).
      - **So the record is not anonymous state.** It is the shipped scene JSON's post-processing, AO, sharpening and
        gamma set, and those keys are the natural names for the store's unresolved rows. The same files also carry
        the scene light (open question `D-4`, answered from them) and the shadow and SSS settings. Those were not
        mapped here.
      - *Still open:* the class name (`EA-2`), the map loader's own call sites (only its setter list was compared,
        and it matches), and the rest of the ~96 unnamed rows.
- [x] ~~**UQ-234.** The 7 bytes at `+0x11` of `OrderedObject`. No reader was found by a displacement census,
      which is not the same as proving them inert. (`PROPOSED-xiionline-13-13`)~~
      **UQ-234 answered 2026-09-15 (FABLE): they are the base class's TAIL PADDING, and the allocation
      sizes prove it rather than a failed search.**
      - **The base ends at `+0x11`.** `00212CC0` (26 B) writes exactly three things: the vtable
        `009010B8` at `+0`, a zero qword at `+8`, and the byte `1` at `+0x10`. That is **`0x11` bytes
        used**.
      - **Eleven of the nineteen command builders allocate `0x18`.** Not one uniform size — the
        allocator argument at each builder's `0085E730` call is `0x18` (eleven builders), `0x20`
        (seven) or `0x28` (one, `0018B970`). For the eleven `0x18` classes, `+0x11`–`+0x17` are the
        object's **last seven bytes and there is no `+0x18` at all**: `0x11` rounded up to the
        allocator's 8-byte granularity is `0x18`. `001F1870` is the worked example — its whole body
        is "call the base, store my vtable, return".
      - **So a derived member cannot land in the gap.** The first offset after the base that is
        8-aligned is `+0x18`, which is exactly where every derived field appears.
      - **The census, over a deliberate superset.** 129 bodies: the 70 that materialise one of the 35
        command vtables, the 75 distinct implementations behind all three slots of those vtables, and
        the 19 enqueue builders. Every memory operand through a non-stack base was counted, **without**
        first proving the base is a command object — so the population over-counts, which only makes
        the result stronger. Offsets touched: `+0x00` (101), `+0x08` (70), `+0x10` (25), `+0x18` (51),
        `+0x1C` (10), `+0x20` (14), plus one stray `+0x01` and one `+0x07` on other bases.
        **`+0x11` through `+0x17`: zero sites.**
      - **Why this is not "no reader found".** The earlier census could only say it had not seen one.
        This says the bytes are unreachable *by construction*: the base's last member is at `+0x10`,
        the type's alignment is 8 because it holds a vtable pointer and a qword, and eleven classes
        ship at `0x18` with nothing after the gap. **Bound:** a body outside the 129 that holds a
        command pointer could still address the gap; nothing reaches these objects except the two
        containers of `UQ-229`, whose walkers call the vtable slots that are in the population.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The list is an EASTL vector of 3 pointers plus an allocator | complete body of `0018C9E0`: allocates `0x20`, zeroes three quadwords, passes the literal string `"EASTL vector"` to the allocator initialiser | 1 + 2 |
| Every enqueue function shares one push_back idiom | complete bodies of all 18 enqueue functions listed in §3 *(scope named 2026-10-02, OPUS: §3's 18; the builders number 36, the falsification pass's table)*, read individually | 1 |
| Every command object is appended to two lists | the tail `FUN_0018AFF0(FUN_0018B4E0(), node)` present in all 18; `0018B4E0`'s complete body returns `01F7F5E0` | 1 |
| `ApplyJsonForCutSceneObj` reads no file | complete bodies of `001F1770` (51 B), `001F29C0` (8 B) and `001F2880` (6 B): the constructor stores one `int` at `+0x18`, slot 1 tail-jumps to `001C3C30` with that field as its only argument, and no file-opening call appears in `001C3C30` or `001C3D50` | 1 |
| The three `JsonData` files | the only rip-relative references to the literals `008F9E38`, `008F9E70` and `008F9E48` in `.text`, by full-image scan: `001C6E20` (`JsonData/0.json`), `001C5930` and `001C5750` and `001C6E20` (`JsonData/CutScenes/`), `001C3760` (`JsonData/init.json`) | 1 + 2 |
| The banks are double-buffered 16-byte JSON values | complete bodies of `001FE8B0`, `00200BA0` and `00200BE0` (type tag at `+0`, payload at `+8`, `6` = absent), and the `shl rcx, 4` indexing of `01F813A8` / `01F813D8` by `01F813F8` at `001C3DA6`, `001C3DCE`, `001C5D64` and `001C7167` | 1 |
| The four-step key fallback | complete body of `001C51D0` (232 B): section, then `"Common"` of the bank the mode selects, then `01F81328`, then `01F813C8`, each guarded by `00200BE0` | 1 |
| 103 key names, and every one has a shipped source | every string literal in the 4,607 bytes of `001C3D50` paired with the reader call that follows it, against a full-depth key census of the 337 files in `JsonData/CutScenes/` and the 176 keys of `JsonData/init.json` (`Tools/work/FABLE/drift5/keys.py`, `uq232_census2.py`, `uq232_final.py`; scratch, git-ignored) | 1 + 9 |
| `JsonData/0.json` ships as `{}` | the shipped file, two bytes, in the full-game extract | 9 |
| The vector owns the commands and the manager does not | complete bodies of `0018B810` (159 B) and `0018B040` (36 B): the first calls vtable slot 0 with `edx = 1` per node then empties itself, the second resizes the entry array to zero and resets `+0x24` / `+0x2C` with no destructor call | 1 |
| The caller's vector is always `01F7F5E8` | three instruments: the global has only 3 rip-relative accesses (creator `0018C9E0`, getter `0018CA40`); no 8- or 4-byte pointer to `0018CA40` exists image-wide; and at all 20 enqueue sites the last write to `rcx` is `mov rcx, rax` after `call 0018CA40`, tracked by decoding each body in order rather than by proximity | 1 + 8 |
| Command objects ship in ~~three~~ four sizes, not one | the last write to `ecx` before the `0085E730` call in ~~all **19** enqueue builders: `0x18` × 11, `0x20` × 7, `0x28` × 1~~ all 36 builders *(corrected 2026-10-02, OPUS: over all 36 builders the size is `0x18` x 15, `0x20` x 16, `0x28` x 3 and `0x30` x 2 (`0018B710`+0x37 and `0018B8B0`+0x2E `lea ecx, [rdx + 0x30]`), the last `ecx` write before each `call 0085E730`)* | 1 |
| `+0x11`–`+0x17` is the base's tail padding | `00212CC0` uses `0x11` bytes; eleven classes allocate `0x18`, so the gap is their last seven bytes; and over a 129-body superset (vtable materialisers, all three slots of 35 vtables, and the 19 builders) **no** memory operand through a non-stack base lands in `0x11`–`0x17` | 1 |
| Only allocating producers push into the vector | `0018AFF0` is the sole append to the manager and is not address-taken, so its **40** caller bodies are the whole population; 36 call the allocator `0085E730` and carry the grow path `001AB570`, and the other 4 (`001E5270`, `001F89B0`, `001F48B0`, `001E8580`) allocate nothing and push into no vector | 1 + 8 |
| The sixteen two-slot `Gi*` classes are not in this list | RTTI base-class census over the complete-object locators: 18 `Gi*` classes, 16 with base `GeometryInstance` and 2 slots, 2 with base `OrderedObject` and 3 slots (`009033D0`, `009033F0`); a `GeometryInstance` reaches the list only through the 3-slot adapter `GeometryInstanceOrderedObject` (`00903920`) | 4 |
| The base class is `OrderedObject` | complete body of `00212CC0`, which stores a vtable pointer through the **named symbol** `OrderedObject::vftable` — a qualified symbol in the image, not an RTTI inference | 1 + 3 |
| The pass → class map, all 20 rows | for each row: the wrapper's call/jump target, that target's call target, and the vtable address that constructor `lea`s, each read from raw instruction bytes; the vtable then looked up in the RTTI recovery | 1 + 4 |
| Every class in the block has exactly 3 slots | vtable recovery over `00902F90`–`009033F0`: 36 classes, 3 slots each, no exceptions | 4 |
| Slot 2 is a constant return | complete bodies of `001F2880`, `001F28A0`, `0053DD10` — 6 bytes each, `mov eax, imm; ret` | 1 |
| `0053DD10`'s ledger name is a fold artefact | 6-byte body shared across unrelated classes; instance of open question BA-1 | 1 |
| The per-effect switch offsets | complete bodies of `001F28B0` and `001F3090`; the gates are explicit byte compares against `FUN_00193D50()` results | 1 |
| `01DFE0C4` is checked by every execute read | complete bodies of `001F3300`, `001F3090`, `001F28B0` | 1 |
| `PostProcessObj` maintains the screen index | complete body of `001F1B80` including the `cmove` that zeroes the counter when the mode is zero | 1 |
| The vtable block layout and stride | `.rdata` addresses `00902F90`–`009033F0` at a uniform `0x20` spacing | 4 |
| Body sizes | taken from a call graph regenerated from this program state, not from an earlier dump | 1 |

**Killer observations named and sought:**

- *"These wrappers are calling device methods, and 'command object' is over-reading a helper."*
  — Sought the vtable store. Every constructor `lea`s a distinct `.rdata` address that the RTTI
  recovery independently identifies as a class vtable, and the base constructor names
  `OrderedObject` through a symbol. A device method does not construct a polymorphic object per
  call. **The claim survived, and it overturned the reading this pass started with.**
- *"Slot 2 is a destructor variant or a type id, not an order key."* — Sought its values. Three
  distinct constants across 36 classes, with `BegineSceneObj` lowest and `VideoObj` highest —
  ordering that matches what the passes must physically do. A type id would be unique per class;
  these are shared by many. **The claim survived**~~, though the sort site itself is still unfound~~ *(answered: see §7 - answered 2026-09-14: the list runs in stored order and is not sorted; 2026-10-02, OPUS)*
  and is recorded in §7 rather than assumed.
- *"The `Gi*` classes are the same family, so this document should merge with theirs."* —
  Sought a distinguishing fact rather than an adjacency argument. The `Gi*` classes carry two
  slots and a documented device-vtable execution path; these carry three and an order key.
  **They are not the same contract**, so the question of whether they share a list is left open
  in §7 instead of being answered by proximity.
- *"The order keys prove the list is sorted."* — **Not sought successfully, and therefore not
  claimed.** A constant-returning virtual is consistent with sorting but does not prove a sort
  happens; ~~no consumer was found~~ *(answered: see §7 - the consumer executes the list in stored order, 2026-09-14; 2026-10-02, OPUS)*. §2.2 states what the values are; the sorting is §7 item 1.

**Crossref audit disposition (2026-09-07, against a graph regenerated from this program state):**

`audit_crossrefs.py` reported **zero** `GHOST ADDRESS` and **zero** `BODY DRIFT` for this
document, and two `UNACCOUNTED NEIGHBOUR` findings.

| Subsystem | Edges | Disposition |
|---|---:|---|
| `Resource` | 2 | **Real, and it sharpens a claim.** `00193D50` — the render-parameter getter this document leans on — is also called from `001A7A50` in Resource code, and `001AB570`, the vector grow, is called from `0019E7B0`. **Neither is exclusive to this system.** `001AB570` is a generic EASTL helper shared across the image, and the render-parameter block is a *shared* accessor, not one this system owns; §6's advice to write its bytes is therefore advice to write state that resource-loading code also reads. That is a genuine caveat and is stated here rather than left implicit. |
| `Movement` | 1 | **Not this document's edge.** `0022B0B0 callee 00357780` belongs to `MainLoop_Draw`, cited here only as the producer that calls the pass wrappers. It is dispositioned in the frame document's §8, where `0022B0B0` is the subject rather than the context. |

**Superseded readings:** none — this document is the first on its subject. It does, however,
correct a reading made earlier in the same pass in the sibling frame document, which had called
`01F7F5E8` "the render device singleton"; that correction is recorded in that document's §8.

## 9. Related

- [`../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md`](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) — the frame that enqueues these commands, and the GIF stream beneath them
- [`../Gi-Render-Commands/gi-render-command-family.md`](../Gi-Render-Commands/gi-render-command-family.md) — the adjacent two-slot command family; see §5 "Do not confuse with"
- [`../Graphics-Thread-Handshake/the-shared-command-state-word.md`](../Graphics-Thread-Handshake/the-shared-command-state-word.md) — the publish-and-account protocol that runs after a frame's commands are enqueued
- [`../Post-Processing/the-post-processing-effect-catalogue.md`](../Post-Processing/the-post-processing-effect-catalogue.md) — what `PostProcessObj` ultimately drives
- [`../Post-Processing/ppfx-function-identification.md`](../Post-Processing/ppfx-function-identification.md) — the Yebis/PPFX layer behind post-processing
- [`../Character-Rendering/character-render-object.md`](../Character-Rendering/character-render-object.md) — `CharacterRenderObject`, a different object in the same neighbourhood
- [`../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) — the RTTI recovery this map was built on, and open question BA-1

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

The frontmatter said this page *"owes an independent falsification pass"*. It gets one here, and the
pass **closes `PROPOSED-xiionline-13-9`**, **corrects two counts in §2.1**, and **finds a fourth order
key and two classes whose key is not a class constant at all**.

| claim | measured |
|---|---|
| 36 vtables, contiguous, stride `0x20`, last at `009033F0` | **exact** |
| the 36 class names | **36 of 36 re-derived from RTTI**, including the engine's own misspelling `BegineSceneObj` |
| `0018C610` 148 B · `0018AFF0` 58 B · `001AB570` 318 B · `0018C9E0` 95 B | **4 of 4 exact** |
| the allocator is named `"EASTL vector"` | the string is at **`008C5F58`**, loaded by `0018CA21 lea rdx` inside `0018C9E0`, after `FUN_00210EC0(0x20)` and three zeroed qwords — §2.1's pseudo-code matches instruction for instruction |
| the dead `p != NULL` inside the push_back fast path | `0018C66E test rdx, rdx` / `je`, after `rdx` was already compared against `[rdi+0x10]` |
| **"all 18 enqueue functions"** | **36, not 18** — see below |
| **"the same 140-to-150-byte template"** | **139–253 bytes**; 29 of the 36 fall in the stated band |

### There are 36 enqueue functions, one per class

Counted by the template's own signature rather than by its size — a function that calls `malloc`,
the grow-and-insert `001AB570`, the second-list getter `0018B4E0` and `0018AFF0`:

**36 functions, contiguous from `0018B540` to `0018CCF0`, every one with a `malloc`.** That is
**one enqueue function per command class**, which is the natural shape and a far better fact than
"18". Their sizes run **139 · 143×3 · 144×14 · 145×2 · 148×7 · 150×3 · 159 · 176 · 177 · 180 · 188 ·
253** — so "the same 140-to-150-byte template" is true of 29 of the 36 and not of the other seven.

*(`0018CA40` is an 8-byte `mov rax, [01F7F5E8]; ret`. It is a getter for the singleton, not part of
the template: `0018C610` receives the list in `rcx` and never calls it.)*

### The block's fourth qword is the next vtable's RTTI locator

§4.1 is right that each class has **three slots** — and the stride is `0x20`, so a reader taking
32 bytes per "vtable" swallows a fourth pointer. It is the **Complete Object Locator of the *next*
class**: each vtable's own locator sits **8 bytes before its listed address**, the ordinary MSVC
layout. That is how all 36 names were recovered here, and it is worth stating because a
reconstruction that lays out 0x20-strided vtables of four slots would be laying out three slots plus
a stray pointer.

### All 36 order keys — closing `PROPOSED-xiionline-13-9`

§4.3 reads `vftable[2]` for eight classes and §7 records the other 28 as unknown. All 36 are opened
here. **Slot 2 has only five distinct implementations across the 36 classes** *(scope named 2026-10-02, OPUS: across all 42 concrete classes it has nine, §2.5)*, while slots 0 and 1
have 36 each — the first two are per-class, the third is a small pool of shared accessors.

| key | impl | count | classes |
|---:|---|---:|---|
| `1` | `0053DD10` | **11** | `BegineSceneObj`, `EndSceneObj`, `BegineScene0Obj`, `EndScene0Obj`, `RazorMarkerPushObj`, `RazorMarkerPopObj`, `DisableMsaaObj`, `EnableMsaaObj`, `SetPrimIdEnableObj`, `EnableDofObj`, `SetDofObj` |
| `0x10` | `001F2880` | **18** | `SetRendererCameraObj`, `CopyBufferObj`, `CopyDepthBufferObj`, `Ps2DofObj`, `SetScreenIndexToPostProcessManagerObj`, `ApplyJsonForCutSceneObj`, `ReadPresetDofForCutSceneObj`, `MonsterGallerySoftParticleEnable`, `MaskBorderObj`, `RenderSSSObj`, `PostProcessObj`, `AmbientOcclusionObj`, `GaussianFilterObj`, `CopyFrontBufferForVFXObj`, `CopyFrontBufferForChrRefraction`, `CopyFrontBufferForWaterRefraction`, `ZBufferObj`, `FastClearObj` |
| **`0x100`** | `001F2890` | **4** | `RenderMonsterGalleryChara`, `RenderMapOpaqueObj`, `RenderOpaqueObj`, `RenderAfterWaterObj` — **a value §4.3's table does not have** |
| `0x80` | `001F28A0` | **1** | `VideoObj` |
| **per-instance** | `00879750` | **2** | `GiResetRenderTargetObj`, `GiResetDefaultRenderTargetObj` |

### Two things §4.3 gets wrong

**"a constant per class" is false for two of the 36.** `00879750` is `mov eax, dword ptr [rcx+0x18];
ret` — it reads an **instance field**, not a constant. The two `GiReset…` classes therefore carry a
**per-object** order key, and a reconstruction implementing §4.3's model literally would give them a
fixed layer they do not have.

**"`VideoObj` … composited last, over everything" does not follow from the key.** Four classes carry
`0x100`, which is **larger than VideoObj's `0x80`**. Whether that puts them in front of or behind the
video depends on the comparator and the sort direction — and `PROPOSED-xiionline-13-7` records that
~~**no consumer that walks either list has been located**, so nobody has read the comparator yet.~~ *(answered: see §7 - the walk was found 2026-09-14 and compares nothing; 2026-10-02, OPUS)* The
key values are now all known; the ordering they produce is not. Opened as
`PROPOSED-xiionline-13-14`.


> **`-13-7` NARROWED 2026-09-13 (OPUS): the consumers were never missing — they call two accessors
> instead of naming the lists, so a search for references to `01F7F5E0` / `01F7F5E8` cannot see
> them.** Every reference to either global in the image belongs to one of four tiny functions:
>
> | function | size | role | callers |
> |---|---:|---|---:|
> | `0018B480` | 85 B | **setter** for `01F7F5E0` (`cmp` / `cmp` / `mov`) | **1** — `00186CD0` |
> | `0018C9E0` | 95 B | **setter** for `01F7F5E8` | **1** — `00186CD0` |
> | `0018B4E0` | 33 B | **accessor** — `mov rax, [01F7F5E0]` | **56 functions, 78 sites** |
> | `0018CA40` | **8 B** | **accessor** — `mov rax, [01F7F5E8]` | **46 functions, 67 sites** |
>
> **So the producer side is one function and the consumer side is about a hundred call sites.**
> `00186CD0` (1,240 B) installs both lists and is the only caller of either setter; everything that
> subsequently reads a list goes through an 8- or 33-byte getter, which is why a rip-relative census
> of the globals reports a producer and nothing else. **The census was right and the conclusion drawn
> from it was not.**
>
> **This does not read the comparator, and it is not claimed to.** What it changes is that the sort
> and execution site is no longer unlocated-in-principle: it is one of the **56 + 46 callers**, a
> finite enumerable set, rather than something that may not exist. The obvious next cut is the
> callers that take a list and then *loop* — `001D1660` (13,753 B, 8 call sites) and `00187950`
> (3,311 B, 4) are the largest and call the getter more than anyone else.
>
> **Nothing above was executed or observed live**, and `-13-7` stays open until a body is read that
> walks a list and compares two keys.

**Not claimed:** nothing here was executed or observed live. ~~The sort and execution site remain~~ *(answered: see §7, 2026-09-14 - executed in stored order, never sorted; 2026-10-02, OPUS)*
unlocated (`-13-7`), so every statement above is about the keys the classes *carry*, not about the
order the frame draws them in. The 36 enqueue functions were counted by signature and their
constructors were not opened individually.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**StoryEvent — SHARED READ-ONLY ACCESSOR (FABLE 2026-09-15, 1 edge).** § 7's UQ-232 answer names `001C50C0`, whose callers include `001ED240` in that layer. It is a 73-byte **getter**: it copies the current scene name out of the string at `01F832C8`/`01F832D0` into a caller-supplied `eastl::string`. The crossing is that both layers read one authored name through one accessor — the cutscene JSON loader `001C5930` uses it to build the sidecar path and to decide whether the scene changed, and StoryEvent uses it for its own purposes — not a shared responsibility and not a write. Neither this page's command list nor its execute methods reach StoryEvent. Read from the shipping bytes.

**Platform — SERVICE.** `00223190` on this page calls `FUN_005cc930`, owned by that layer. What it reaches is a high-resolution counter read: it calls the import at `008C2188` and converts the unsigned 64-bit result to double with the `2^64` fixup at `00D27A68`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 16 edges).** `00225580` is called by eleven Audio bodies
(`00223DA0`/`00224570`/`00223190`/`00222740`/`00224E40`/`00224C40`/`00222F20`/`00224F10`/`002251B0`/
`002252C0`, …) — shared option-state helper; `00186CD0`/`00187950` call `00182E80` (2 edges);
`001D1660` calls `001DBB00`/`002DEBA0`. Generic-helper fan-in, no audio command semantics.

**ActorEntity / Party / Status_Periodic_Terminal — CLIENT (7 edges through `00265680`).**
`0025B600`, `00263660`, `0026C5D0`, `0026DFB0` (ActorEntity), `00358CB0`, `00358F90` (Party) and
`00310DB0` (Status) call `00265680` — the helper this page names in its `001EC57B`/`001EC580`
context; all seven are client consultations of a shared render-list helper, not ownership crossings.
Read from `edges.tsv` 2026-09-17 (SWE2-FRONTIER).
- **CoreRuntimeScheduling - CLIENT and SERVICE (49 edges).** `0017D6E0`, `0017F6B0`, `00182220`, `001823B0` (+16 more) are called by bodies filed to CoreRuntimeScheduling: `0017CCD0`, `0017D6E0`, `001E03F0`, `001E0590` (+8 more); `0017D6E0`, `00187950`, `0018EEE0`, `001BC190` (+5 more) reach bodies filed to CoreRuntimeScheduling: `0017D980`, `001A1460`, `001A1470`, `001DB600` (+16 more) - shared machinery across the layer boundary, no shared ownership.
- **Developer - CLIENT and SERVICE (5 edges).** `001FE8B0`, `00200B50`, `00200BE0`, `00796E20` are called by bodies filed to Developer: `001C2F50`, `001C6320`; `0017D6E0` reaches bodies filed to Developer: `001C2F50` - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (70 edges).** `00225570`, `00265680`, InputDevice_QueryAvailabilityState_Always1 (`0053DD10`), `00584740` (+6 more) are called by bodies filed to Input: `0017DDC0`, `0017DE10`, `0017DE60`, `0017DFC0` (+60 more); `0018E470`, `0022A580` reach bodies filed to Input: `001976E0`, InputControl_QueueWorkerDeadlineAndMarkDirty (`0035E9B0`), `00360080` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (17 edges).** `00265680`, `002E9B60` are called by bodies filed to Movement: `002690D0`, `0026C3E0`; MainLoop_Draw (`0022B0B0`), `002690D0`, `0026C5D0`, PartyControl_ApplyAnalogLocomotionToActor (`00358CB0`) (+1 more) reach bodies filed to Movement: `002640E0`, `00265200`, `00265830`, `002681D0` (+10 more) - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (34 edges).** `00193D50`, `001A0C50`, `001A4BF0`, `001A52A0` (+9 more) are called by bodies filed to Resource: `0019E7B0`, `001A11B0`, `001A7A50`, `001AD130` (+14 more); `0017D6E0`, `0019E7B0`, `001A7A50`, `001CD0E0` (+2 more) reach bodies filed to Resource: `0019EAA0`, `0019EB60`, `001A0A90`, `001A0C50` (+5 more) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (6 edges).** `00225580` is called by bodies filed to Save_Load_Settings: `005812B0`, `005817D0`, `00581930`; `0017D6E0`, `00265920` reach bodies filed to Save_Load_Settings: SaveloadManager_GetSingleton (`001C18E0`), SaveloadManager_ProcessPendingCaptureCopy (`001C1910`), SaveImage_GetPersistentPayloadBase (`002EF2B0`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (32 edges).** `001EC500`, `001EC620`, `00265680`, `00265920` (+5 more) are called by bodies filed to Script_VM_Native_Bridge: `00341840`, `00341F90`, `003423E0`, `00343690` (+27 more); `0034C7E0` reaches bodies filed to Script_VM_Native_Bridge: VMValueStack_PopInt32CoerceFloat32 (`00267E10`) - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT and SERVICE (14 edges).** `00186660`, `001867B0`, `001867C0`, `0018CD90` (+7 more) are called by bodies filed to UI: `0018EEE0`, `00279E20`, `002986E0`, `00299090` (+2 more); `001F3300` reaches bodies filed to UI: `0018EEE0` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (10 edges).** `00263660`, `00265920`, `002DEBA0`, InputDevice_QueryAvailabilityState_Always1 (`0053DD10`) are called by bodies filed to WorldAreaField: World_UpdateSimulationTick (`00314020`), `003789A0`, `00379290`; `001CD0E0`, `001ED240`, `0026C5D0`, BattleUnit_RunPeriodicCombatMaintenance (`00310DB0`) reach bodies filed to WorldAreaField: FieldData_GetVariable0 (`00265270`), WorldTransition_GetTransitionFieldId (`00314910`), `00377700`, FieldData_GetActiveFieldRecordBit15 (`00377C20`) - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - SERVICE and MECHANICAL (4 edges).** `00310DB0` reaches `BattleEnmity_UpdatePeriodicDecay` (`00321530`); three AI bodies (`003014C0`, `00301AD0`, `00305AB0`) call `FieldData_GetActiveFieldRecordBit15` (`00377C20`) - accessor fan-in.
- **CombatFormula - SERVICE (6 edges).** `00310DB0` reaches five formula bodies (`00300CE0`, `003112F0`, `0031E800`, `00320AB0`, `00385F60`); `00300530` also calls `00377C20`.
- **Gameplay - SERVICE and MECHANICAL (5 edges).** `00310DB0` reaches `BattleEncodedId_IsValidForClass` (`00322C50`); four gameplay bodies call `00377C20` - accessor fan-in.
- **Items_Equipment_Shops_License - MECHANICAL (2 edges).** both edges are item bodies (`00309FB0`, `0030FD10`) calling `FieldData_GetActiveFieldRecordBit15` (`00377C20`) - accessor fan-in.
- **Rewards_Progression_Economy - SERVICE and MECHANICAL (4 edges).** `00310DB0` reaches the loot pool (`002FB150`, `00319830`, `00319A00`); `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) calls `00377C20`.
- **Spawn_Encounter_Lifecycle - CLIENT and SERVICE (2 edges).** `Spawn_TrySelectCandidatePosition` (`00234AF0`) calls `00265200`; `BattleStats_ModifyHPAndProcessLethalState` (`00300530`) reaches `SpawnGroup_RecordMemberDeathAndHandleCompletion` (`00306F00`).

## The `001829A0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`001829A0` (~200 B) is the pass-wrapper battery around
`SetScreenIndexToPostProcessManagerObj`: arms fetch the render context
through `0018CA40` (`001829A8`, `00182A14`/`00182A1E`), `001D8210`
(`001829CE`, `00182A44`), `0018B4E0` (`001829F4`) or `00189120` ×2
(`00182A77`/`00182A86`) and tail into `0018CC60` (`001829B7`),
`001D76A0` (`001829E5`), `0018B030` (`00182A00`), `0018C7D0`
(`00182A2A`), `001D85A0` (`00182A50`), or `00186910` followed by a
`byte[rax+8]` gate (`00182A96`).

| member | role | interior |
| --- | --- | --- |
| `0018CC60` (143 B) | the frame-open wrapper — `qword[rsp+0x20] = -2` scope guard (`0018CC66`), `0085E730` resolve stored twice (`0018CC82`/`0018CC87`), member call `001F1ED0` (`0018CC9B`) | [`0018CC82`](../../_index/ADDRESS-INDEX.md) |
| `001F1ED0` (47 B) | `SetScreenIndexToPostProcessManagerObj` constructor — `00212CC0` base init (`001F1EDF`), installs vtable `00903090` (`001F1EE4`/`001F1EF3`), `dword[rdi+0x18] = edx` (`001F1EEB`), returns `rdi` | [`001F1EE4`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0018CA40`, `001D8210`, `0018B4E0`,
`00189120`, `00186910`, `001D76A0`, `0018B030`, `0018C7D0`,
`001D85A0`, `0085E730`, `00212CC0`. The `0018CC60 → 001F1ED0` edge is
member→member — the wrapper constructs the pass object.

## The `001EC490` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`001EC490` (~300 B) is the `ApplyJsonForCutSceneObj` pass-wrapper
battery: context fetches `0018CA40` (`001EC498`), `00193D50`
(`001EC4DF`), `0020A760` (`001EC4B4`) then tails into `0018B540`
(`001EC4A7`), `00214B30` (`001EC4BD`), `00194290` (`001EC4F8`). The
mid-body arms index `dword[01DFE40C]` (bound 4) into the
`01F832B0` dword table (`001EC500`–`001EC513`), store the mode back to
`01DFE40C` (`001EC532`/`001EC552`), and tail `001C5570` with the
`"mDofFocusDistance"`/`"mDofApertureFnumber"` names (`001EC52B`/
`001EC54B`); a compare arm checks `dword[01F832B0 + idx*4]` vs `ebx`
then calls `00265680` (`001EC57B`/`001EC580`).

| member | role | interior |
| --- | --- | --- |
| `0018B540` (143 B) | the frame-open wrapper — `qword[rsp+0x20] = -2` scope guard (`0018B546`), `0085E730` resolve stored twice (`0018B562`/`0018B567`) | [`0018B562`](../../_index/ADDRESS-INDEX.md) |
| `001F1770` (51 B) | `ApplyJsonForCutSceneObj` constructor — `00212CC0` base init (`001F177F`), installs vtable `009030B0` (`001F1784`/`001F1793`), `dword[rdi+0x18] = edx` (`001F178B`), returns `rdi` | [`001F1784`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0018CA40`, `00193D50`, `0020A760`,
`00194290`, `00214B30`, `001C5570`, `00265680`, `0085E730`,
`00212CC0`. The DoF-named `001C5570` arms share the `01DFE40C` mode
index — same register-table machinery as the command arms.

## The `0017ECF0`/`0017FD70`/`001827E0`/`00182A10` exclusive-subtree cluster — all 4 roots bound (SWE2-FRONTIER, followup queue)

Four identical singleton-gated forwarders: `call 0018CA40` (the command-
list singleton getter); when it returns non-null, call it again and
tail-jump to the member method on that object; null returns silently.
Each root's census member is the method it forwards to:

| root | member (forward target) | interior |
| --- | --- | --- |
| `0017ECF0` (36 B) | `0018C740` | [`0017ED0A`](../../_index/ADDRESS-INDEX.md) |
| `0017FD70` (36 B) | `0018C330` | [`0017FD8A`](../../_index/ADDRESS-INDEX.md) |
| `001827E0` (36 B) | `0018C6B0` | [`001827FA`](../../_index/ADDRESS-INDEX.md) |
| `00182A10` (36 B) | `0018C7D0` | [`00182A2A`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0018CA40` (the singleton getter,
called twice per forward). All four bodies are byte-identical in shape —
`test rax; je ret; call again; mov rcx, rax; jmp member` (`0017ECF9`–
`0017ED0A` is the canonical span).

## The `0019E7B0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0019E7B0` (~600 B) — null-gated submit body: `rdx` null → return
(`0019E7B3`); else the `0x158`-frame EH body builds the record.

| member | role | interior |
| --- | --- | --- |
| `001A0C50` | record walk — `dword[rdx] == 0` early-out (`001A0C74`) under EH guard | [`001A0C74`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hubs `00600A60` / `005FEFD0` (2026-09-17, SWE2-EC7)

The profile-slot end (`00600A60`, 197 B) and scene-begin (`005FEFD0`, 190 B) are one idiom over
the same 0x80-stride record ring, read against the shipping image:

- Both gate on bit 0 of `[ctx+8]`, in opposite directions: `005FEFD0` requires it clear then
  **sets** it (`or eax,1` at `005FEFF8`) — the begin; `00600A60` requires it **set**
  (`not eax` + `test al,1` at `00600A74`–`00600A78`, refusing `0x16` when clear) then **clears**
  it (`and ecx,0xFFFFFFFE` store at `00600A8A`) — the end. The busy flag the begin/end pair
  toggles. Both then call `00600B30(ctx, 0, 1)` and, on false, `vcall [ctx]+0x10`.
- The shared tail bumps `[ctx+0x60]` by 0x80 wrapping at `[ctx+0x58]` bound back to `[ctx+0x50]`
  base (ring bump at [`00600AAB`](../../_index/ADDRESS-INDEX.md) /
  [`005FF014`](../../_index/ADDRESS-INDEX.md)); the claimed slot gets `{kind, arg}` — `0x18` for the
  profile end, `0x16` for scene-begin — and links head/tail at `[ctx+0x88]`/`[+0x90]`.
  Full ring returns `0xD`.

So the pair is acquire/release-shaped over one command ring: begin stamps kind 0x16 with the
scene arg, end stamps kind 0x18 with the profile number.


## Interior citation — frontier hub `00200BE0` (2026-09-18, SWE2-EC7)

`00200BE0` — 7 B, 14 callers; the `type == 6` absent-check this page's JSON-bank reads
already name. Interior verified: `cmp dword [rcx], 6; sete al` at
[`00200BE0`–`00200BE3`](../../_index/ADDRESS-INDEX.md) — the whole body, matching the
"payload at `+8`, `6` = absent" layout this page documents.

### Interior citation — frontier hub 00194290 (2026-09-18, SWE2-EC7)

**00194290** (107 B, 4 A-measured callers) — the command-slot byte setter. Compares a byte at `[rsi+rdx]` (`rsi` = the list's record base); if already set, `005CDAA0` (the serialised-commit sibling) runs once, then the slot's dword at `+0x1F0` is re-stamped. This is the write half of the record mutation the list's emission pass performs. In-scope: byte test [`001942B4`](../../_index/ADDRESS-INDEX.md); `005CDAA0` call + `+0x1F0` store [`001942C0`](../../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## SWE2-EC7-18 update (2026-05-15) — `001FE8B0` JSON type-6 writer fragment

`001FE8B0` (18 B) is the type-6 (null) JSON value writer this page describes: `dword[rcx]=6` stamps the tag (`001FE8B0`), `rax=rcx` (`001FE8B6`), `qword[rcx+8]=0` clears the payload (`001FE8B9`), `ret` — a complete `{type=6, payload=0}` record init, matching the double-buffered 16-byte value shape this page's `01F813A8`/`01F813D8` banks carry.
## SWE2-EC7-32 update (2026-09-18) — `00194250` five-field DOF setter + `001AC670` nested-vector getter (via `001E2AF0`)

`00194250` (51 B) is the DOF setter the record description names,
and the bytes match it exactly: `dl -> +0x110` (the enable byte),
`xmm2 -> +0x114`, `xmm3 -> +0x118`, and two stack floats ->
`+0x11C`/`+0x120` — five fields, one call, no guards. Interior
anchor `0019425C` (the `+0x11C` store).

`001AC670` (124 B) — reached through `001E2AF0`, `001BC190`,
`001E6480` and `001F8D10` — is the bounds-checked nested index
the ordered objects run: `[rcx+0xA8] < 0` or `r8d >=`
`([rdx+8] - [rdx]) / 8` returns 0; `00265920()` resolves state,
then the `r8`-th element's own `+0x44`-indexed sub-array
(0x30-stride records) is counted — empty returns 0 — and the
answer is the inner array's `count*2 - 2`-th entry. Interior
anchor `001AC6E3` (the inner `+rcx*8` index).

## SWE2-EC7-33 update (2026-09-19) - `00649C20`

`00649C20` (978 B) is the `+0x280`-`+0x2C8` run builder the list names - `00671B10` plus `00674610`/`00674230`/`00671B30`/`00671690`/`0066F970`/`005CCB80`/`0063A990`. Interior anchor `00649D53` (a `00671B10` call).

## SWE2-EC7-35 update (2026-09-19) - `00224570`

`00224570` (763 B) is the ordered-list builder - 33 calls through the `00225xxx` render-list family plus `005CC930` pair. Interior anchor `002245B1` (a `00225xxx` call).

## SWE2-EC7-37 update (2026-09-19) - `00671B30`

`00671B30` (579 B) is a Phyre render-block helper - `01F44830`, `00616700` pair plus `005FD050`/`00615BC0`/`00624670`/`0017D260`/`00808C40`. Interior anchor `00671BA3` (a `005FD050` call).

## `+0xEE` is 0 on every path out of every writer - the `1` store in each setter is dead (2026-09-19, OPUS)

*`postprocess-context-accesses.tsv` has held all nine writes to `+0xEE` since the sites were
harvested. Read as a list they look like a two-state switch. Read as code they are not: **both
setters store `1` and then overwrite it with `0` seven bytes later**, and the overwrite is not a
branch target, so nothing can reach the `1`.*

The two setters are the same 49-byte shape with the roles of `+0xEC` and `+0xED` swapped:

| | `0018D640` | `001943C0` |
|---|---|---|
| writes the argument to | `+0xED` | `+0xEC` |
| gates on | `+0xEC != 0` | `+0xED != 0` |
| both gates pass | `D653: +0xEE = 1` **then `D65A: +0xEE = 0`** | `1943D3: +0xEE = 1` **then `1943DA: +0xEE = 0`** |
| either gate fails | `D662` / `D669`: `+0xEE = 0` | `1943E2` / `1943E9`: `+0xEE = 0` |

**The overwrite is unreachable as a target.** The branch targets of `0018D640` are exactly
`0018D662` and `0018D669`; of `001943C0`, exactly `001943E2` and `001943E9`. Neither `0018D65A`
nor `001943DA` is among them, so neither is a join point: each follows its `1` store by
fallthrough and unconditionally undoes it. The constructor agrees - `0018CDC1` stores `0`.

**So the field is `0` after construction and `0` after either setter returns, for every argument.**
The shape the code describes is `+0xEE = (+0xEC && +0xED)`, computed and then discarded.

### It is read, exactly once, and the consumer gets 0.0f

`0018F3DF`, in `0018EEE0`:

    movzx eax, byte ptr [rsi + 0xEE]
    movd  xmm0, eax
    cvtdq2ps xmm0, xmm0
    movss dword ptr [rdi + 0x94], xmm0

`rsi` is this singleton and not a lookalike: `0018EFBC` loads it from `01F7F5F0` and `0018EFEC`
stores it back - that body is the lazy-init site itself. The byte is widened to a float and written
to `+0x94` of the receiving parameter block, so **that float is permanently `0.0f`.** This read was
absent from `postprocess-context-accesses.tsv`, whose routes reach the object by call argument; this
one reaches it through the global slot. It is added there now.

**What this changes for a reimplementation.** Implementing `+0xEE` from its name - a switch set when
both enables are on - produces `1.0f` at `+0x94` where the engine produces `0.0f`. The two setters
must be written as the engine has them: store the argument, and leave `+0xEE` zero.

**NOT CLAIMED:** that the `1` is dead in the original source. A dead store of this shape is what a
disabled or short-circuited condition looks like after compilation, and which it was cannot be
recovered from the image. The claim is about the shipped code only, where it is exact.

**NOT CLAIMED:** that `+0xEE` has no other writer. The population is bounded and stated - the seven
bodies that load `01F7F5F0` or `01F81300` plus the three writers the store cites. An offset-only
sweep for `[reg+0xEE]` finds writers across the image, but `0xEE` is an ordinary displacement in
dozens of unrelated types and that population is not evidence about this one. A writer reaching this
object through an indirect call would not appear - the same static limit that bounds every sweep on
this page.

*Related citation defect, corrected in the same change: the `fields.tsv` row for `+0xEE` cited
"byte-fill sites `0018D653-0018D67C`". `0018D67C` is `int3` padding - the body ends at `0018D670`
and the last store is at `0018D669`.*

## SWE2-EC7-38 update (2026-09-19) - `001CC600`

`001CC600` (497 B) is the gated applier the page names - `01F81280`/`01F81358`/`01F81360`, `"EASTL basic_string"`, `001A5760`/`001EDF00` pairs plus `001CC9A0`/`001C3390`/`002F1A20`/`0022A550`. Interior anchor `001CC637` (an `001A5760` call).

## SWE2-EC7-38 update (2026-09-19) - `00674230`

`00674230` (494 B) is a Phyre render-block-binding sibling - `00D69130`/`01F7F5B8`/`01F7F590`, `"Trying to unbind a data block "`, `005CDAA0`/`00673780`/`0062EC70`/`00584730`. Interior anchor `0067424B` (a `005CDAA0` call).

## SWE2-EC7-38 update (2026-09-19) - `001C5570`

`001C5570` (472 B) is the key-string tail the page names - `01F81415`/`01DF6E4C`/`008F6600`, `"EASTL basic_string"`/`"PresetDof "`/`"Common"`, `001EDF00`/`001FF740` pairs plus `001CC9A0`/`001A52A0`/`001FF6B0`/`00200B50`. Interior anchor `001C55AA` (an `001EDF00` call).

## SWE2-EC7-38 update (2026-09-19) - `00674610`

`00674610` (448 B) is a render-list sibling - `01F44830`/`01F7F590`/`01F7F5B8`, `00615BC0`/`00624670`/`00616700`/`0062EB90`/`00808C40`. Interior anchor `006746D6` (a `00615BC0` call).

## SWE2-EC7-42 update (2026-09-19) - `001F3300`

`001F3300` (313 B) is `PostProcessObj::Execute` - `01DFE0C4`/`01F82EC0`, `00609710`/`00600A60`/`00193D50` triple/`0018E470`/`0018EEE0`/`00796E20`. Interior anchor `001F3325` (a `00609710` call).

## SWE2-EC7-42 update (2026-09-19) - `001EE040`

`001EE040` (309 B) is the `(renderWidth, renderH...)` factory-result body the list names - `01F82E50`/`02CB76A0`/`02CBB900`, `00584740`/`00633040`/`0063A990`/`0060DD70`/`00610990`/`006394E0`/`00615C90`. Interior anchor `001EE07F` (a `00584740` call).

## SWE2-EC7-44 update (2026-09-19) - `001F28B0`

`001F28B0` (257 B) is `AmbientOcclusionObj::Execute` - `00186660`/`001867A0`/`001867B0`/`001867C0`/`00188730`/`00189120`/`0018F510`, gated on render params `+0x198` per the page's read. Interior anchor `001F28B9` (an `00186660` call).

## SWE2-EC7-45 update (2026-09-19) - `00224C40`

`00224C40` (243 B) is a body - `0016D6A0`/`00221D10`/`00225570`/`00225580`/`00225590`/`002255A0`/`007A48C0`. Interior anchor `00224C6C` (an `0016D6A0` call).

## SWE2-EC7-46 update (2026-09-19) - `00224F10`

`00224F10` (228 B) is a bank-path sibling - `00221C70`/`00221D60`/`00222050`/`00224C40`/`00225580`/`00225590`/`002256E0`. Interior anchor `00224F39` (a `00221C70` call).

## SWE2-EC7-51 update (2026-09-19) - `0018B970`

`0018B970` (176 B) is a body - `0018B4E0`/`001AB570`/`001F1840`/`0085E730`. Interior anchor `0018B9A2` (an `0018B4E0` call).

## SWE2-EC7-52 update (2026-09-19) - `001E6480`

`001E6480` (1302 B) is the bounds-checked nested index - `006045E0`/`001AD440`/`001ABF50`/`001AC670` plus `01F44830` cookie. Interior anchor `001E6566` (a `006045E0` call).

## SWE2-EC7-53 update (2026-09-19) - `006045E0`

`006045E0` (357 B) is an ordered-render-command-list body - `005FD810` single call plus `008C5F80`-`008C5FD0`/`01CEBBA8` rdata. Interior anchor `00604737` (a `005FD810` call).

## SWE2-EC7-54 update (2026-09-19) - `005FD810`

`005FD810` (1169 B) is a call-free 4x4 transform leaf - `[rax]`/`+0x10`/`+0x20`/`+0x30` rows against the `[rcx]`/`+4`/`+8` vector and `[rdx]` scalar (`006045E0`'s single callee). Interior anchor `005FD863` (the `+0x10` row load).

## SWE2-EC7-55 update (2026-09-19) - `001CC9A0`

`001CC9A0` (282 B) is a presentation command body - `001CCAC0`/`001EDF00`/`00808C40` plus two vcalls, `008F6600`/`008F6D3C` and the `"EASTL basic_string"` literal. Interior anchor `001CC9DA` (a `001CCAC0` call).

## SWE2-EC7-59 update (2026-09-19) - `0018C200`

`0018C200` (159 B) is the body `UQ-229` flagged unfollowed - `0018B4E0`/`001AB570`/`001F1CB0`/`0085E730`. Interior anchor `0018C22A` (a `0085E730` call).

## SWE2-EC7-61 update (2026-09-19) - `001F3440`

`001F3440` (154 B) is the `Ps2DofObj::Execute` row body - `00186660`/`001867B0`/`00188730`/`00189120`/`00191560`/`00193D50`/`005FEFD0`. Interior anchor `001F345A` (a `00609710` call).

## SWE2-EC7-62 update (2026-09-19) - `0018C160`

`0018C160` (150 B) is the `RazorMarkerPushObj` scope-push body - `0018B4E0`/`001AB570`/`001F1C30`/`0085E730`. Interior anchor `0018C183` (a `0085E730` call).


## SWE2-EC7-62 update (2026-09-19) - `001F48B0`

`001F48B0` (149 B) is the `GeometryRenderTargetImmediate` body - `0016D6A0`/`0018B4E0`/`001A1470`/`001F4950` plus `01F7F4C0`. Interior anchor `001F48D6` (a `0016D6A0` call).



## SWE2-EC7-63 update (2026-09-19) - `0018CCF0`

`0018CCF0` (145 B) is a render-command body - `0018B4E0`/`001AB570`/`001F1B50`/`0085E730` (last of the 36 contiguous `malloc` bodies). Interior anchor `0018CD13` (a `0085E730` call).



## SWE2-EC7-63 update (2026-09-19) - `0018CB30`

`0018CB30` (143 B) is the `SetPrimIdEnableObj` draw-setup body - `0018B4E0`/`001AB570`/`001F1E50`/`0085E730`. Interior anchor `0018CB52` (a `0085E730` call).



## SWE2-EC7-64 update (2026-09-19) - `0018C6B0`

`0018C6B0` (139 B) is the `Ps2DofObj` body - `0018B4E0`/`001AB570`/`001F1BD0`/`0085E730`. Interior anchor `0018C6D0` (a `0085E730` call).



## SWE2-EC7-66 update (2026-09-19) - `001C3390`

`001C3390` (131 B) is a render-command body - `001A52A0`/`001B38B0`. Interior anchor `001C33D5` (a `001B38B0` call).


## SWE2-EC7-71 update (2026-09-19) - `001AC720` list-element peek measured

`001AC720` (124 B) is the peek the render-list bodies call: `dword[+0xA8]
< 0` or `edx >= (end - begin) >> 3` over the `[+0xE8]` vector returns 0;
else `00265920()` runs and element `[begin + edx*8]` -> `r8` supplies a
`+0x44` index (x6 stride) into sub-vector `[r8 + idx*24 + 8..+0x10]`; an
empty sub-vector returns 0, otherwise `begin2[(count*2 - 1)]` - the last
pair's tail element.
Interior anchor `001AC76E` (the `[r8 + rdx*8 + 0x10]` sub-vector load).

## SWE2-EC7-80 update (2026-09-20) - `0065E5D0` lazy singleton measured

`0065E5D0` (64 B) is the once-init behind `0018E470`: when
`[02D38540]` is NULL it allocates 0x10 via `00210EC0`, runs
`0065E530` on the block, and stores it back - a lazy 16-byte object
shared by the render callers (also `006253D0`, the NvAPI init).
Interior anchor `0065E5DD` (the `02D38540` load).

## SWE2-EC7-97 update (2026-09-20) - `002E9B60` measured

`002E9B60` (24 B) is the two-hop getter `002690D0` and
`00358CB0` call: `rcx` and `[rcx+0xC0]` non-null yields
`dword[block]`, anything else `-1` - the null-to-sentinel read
the command list's consumers issue.
Interior anchor `002E9B71` (the `dword[rax]` read).

## SWE2-EC7-104 update (2026-09-20) - `00265720` measured

`00265720` (59 B) is the all-populated scan
`00265680` and `00358CB0` call over the
`02098E24 .. 02099ACC` region at `0x288`
stride: for every entry whose flag byte
`[entry - 4]` has bit 0 set, all three of
`[entry + 0 / +1 / +2]` must be nonzero or the
scan returns 0; reaching the end returns 1 -
the "every armed row is fully populated"
invariant the list arms check.
Interior anchor `00265730` (the flag test).

## SWE2-EC7-108 update (2026-09-20) - `002256B0` + `00221E00` measured

`002256B0` (44 B) is the
field-init `00223190` and
`00224570` run: `qword[+0x14] =
-1`, `dword[+0x1C] = 0x7F`,
`dword[+0x20] = 0x40`,
`dword[+0x24] = -1`,
`dword[+0x28] = 0`,
`dword[+0x10] = 2` - the default
record state the command-list arms
share.
Interior anchor `002256B8` (the
`0x7F` write).

`00221E00` (83 B) is the
lookup-or-insert `00224570` and
`002252C0` call: `00222280` probes
both the record's `+8` list and
the `01FD4140` registry, then
`00221E60(rcx, edx)` searches -
a miss tails `00221D60(rcx)` to
insert - the find-or-add the
list arms share.
Interior anchor `00221E31` (the
`00221E60` call).

## SWE2-EC7-110 update (2026-09-20) - `001C5110` measured

`001C5110` (187 B) is the
indexed name fetch `001C5930`
and `001CD0E0` run:
`dword[01DFE40C]` sign-extends
to the index, and `<= 4`
selects a 0x20 record at
`01F832F0 + index * 0x20`;
`001EDF00(rcx + 0x18, rbx +
0x18)` binds the allocator and
`001A4BF0` copies the
`[rbx]`/`[rbx + 8]` byte range
into the caller's three-pointer
string head. An out-of-range
index falls to the
`"EASTL basic_string"` path and
copies the `01CEB638` empty
range instead - every caller
gets a valid empty string, not
null.
Interior anchor `001C512A`
(the `cmp eax, 4` index
bound).

`001B6CE0` (170 B) is the
record constructor `001B72B0`,
`001EE410`, `005D51C0`,
`006497E0` and `0067B180` run:
`[rcx]` stores the `rdx`
parent, `[+0x20]` latches
`rdx + 0x60`, `+8`..`+0x58`
and `+0x74`..`+0xB8` zero,
`+0x5C` arms 4, `+0x7C` and
`+0xC0` latch -1, and
`0060DF70(rcx)` runs the
post-init pass before the
`this` return.
Interior anchor `001B6D0A`
(the `[+0x20] = rdx + 0x60`
parent-subrecord latch).

## SWE2-EC7-111 update (2026-09-20) - `0060DF70` measured

`0060DF70` (1171 B) is the
two-array resize clone
`001B6CE0` calls as its
post-init commit (`001653E0`,
`00169540`, `0064A0E0` and
`0067B180` run it too). Source
`rdx` carries two count fields
- `dword[rdx]` against
`dword[rcx + 0x48]`, and
`dword[rdx + 0x30]` against
`dword[rcx + 0x10]`, each
masked through `btr ,0x1F` so
bit 31 is a capacity tag, not
count. On a count change the
first array reallocs
`count * 0x48` bytes through
`0017D260` and every new
0x48 record is initialised
(zeros plus `-1` at `+0x28`);
the old `[+0x50]` block goes
to `001B70E0` only when the
old tag bit was clear. The
second array reallocs
`count * 0x40` (`shl rcx, 6`)
the same way and frees the old
`[+0x18]` through `00584730`.
The payload copy then moves
`esi` records of 0x40 bytes
from `qword[r15 + 0x38]` to
`[+0x18]` - four records per
0x100-byte pass while
`esi >= 4`, then a
0x40-stride remainder loop.
`[rdi] = r15` and
`[+0x20] = r15 + 0x60` latch
the source link; an alloc
failure with a nonzero count
answers `0xD`.
Interior anchor `0060E0F0`
(the 0x100-byte copy pass).

`0018B3F0` (138 B) is the
8-byte-element vector resize
`0018B040` and `001A8BA0`
run: `edx` counts elements
against `(end - begin) / 8`;
grow goes to `0018ADB0` with
a zeroed temp, shrink memmoves
`begin` up to `begin +
edx * 8` through `008C2A40`
and drops `qword[+8]` by the
removed span.
Interior anchor `0018B452`
(the `008C2A40` memmove).

## SWE2-EC7-112 update (2026-09-20) - `001B70E0` measured

`001B70E0` (130 B) is the
0x48-record array teardown
`0060DF70`'s resize replaces
(`001B6FD0`, `005DE460`,
`00600470`, `0060C630`,
`0060EE90`, `00610350` run it
too): for each of `edx`
records at `rcx + 0x38 +
i * 0x48`, the `dword` tag is
read - bit 31 SET means
not-owned, so when it is
clear AND the masked count
exceeds 1 the sub-block
`qword[+8]` goes to
`00584730`; both fields then
zero. Finally `00584730`
frees the array itself. Null
`rcx` is a no-op. The bit-31
convention matches
`0060DF70`'s `btr ,0x1F`
capacity tags exactly.
Interior anchor `001B7111`
(the per-record tag read).

## SWE2-EC7-119 update (2026-09-21) - `0065E6B0` measured

`0065E6B0` (8 B) is the
two-instruction forwarder
`00193DA0` uses: it loads
`rcx = [rcx]` - peeling the
container to its head
object - then tails
`006CC260`.
Interior anchor `0065E6B3`
(the `jmp`).

## SWE2-EC7-120 update (2026-09-21) - the `00193DA0` thunk family measured

`006CC260` (133 B) is the
vec3 half-extent setter
`0065E6B0` peels into:
`006DB7C0` loads the
`[+8]+0x18` object's
current `+0x68`/`+0x6C`/
`+0x70` triple, `006DB780`
receives the caller's
`xmm1`/`xmm2` with `xmm3 *
0.5` (`01CEBB70`), and the
three floats store back at
`rbx + 0x68`.
Interior anchor `006CC2A3`
(the `006DB7C0` call).

The rest of the `00193DA0`
block are one- or two-step
thunks that load
`rcx = [rcx]` before
tailing the `006CC090`..
`006CC260` cluster:
`0065E6A0` (8 B) jumps
`006CC1F0`; `0065E670`
(37 B) calls `006CC1E0`
with `1.0f` and `r9d = 1`
defaults; `0065E630` (52 B)
runs `006CBD00([rcx], r8d)`
then tails `006CC170` with
the result in `r8d`;
`0065E610` (17 B) shuffles
a stack byte and tails
`006CC090`; `0065E5C0`
(8 B) tails `006CBEA0`;
`0065E5A0` (8 B) tails
`006CBD20`; `0065E5B0`
(11 B) is the odd one out -
a `[[rcx]] != 0` predicate.
Interior anchor `0065E6A3`
(the `006CC1F0` tail);
interior anchor `0065E68B`
(the `006CC1E0` call);
interior anchor `0065E647`
(the `006CBD00` call);
interior anchor `0065E61C`
(the `006CC090` tail);
interior anchor `0065E5C3`
(the `006CBEA0` tail);
interior anchor `0065E5A3`
(the `006CBD20` tail);
interior anchor `0065E5B7`
(the `setne`).

`0065E530` (78 B) is the
ctor `0065E5D0` calls:
`00210EC0(0x78)` allocates,
`006CBAA0` initializes the
record, the pointer stores
at `[rcx]` and `byte +8`
zeroes.
Interior anchor `0065E565`
(the `006CBAA0` call).

## SWE2-EC7-121 update (2026-09-21) - the `006CC090..006CC260` targets measured

The `00193DA0` thunk
block's tail targets are the
`[+8]+0x18` node's parameter
setters:

`006CC1F0` (107 B) is the
transform-block commit
`0065E6A0` jumps to: while
`byte[+0x24]` is clear it
runs `006DB900` then
`006DB8C0` on `[+8]+0x18`,
then copies the 0x40-byte
block `[rdx]` into
`+0x28..+0x58` and clears
`+0x24`.
Interior anchor `006CC215`
(the `006DB900` call).

`006CC1E0` (8 B) loads
`rcx = [rcx]` and tails
`006DB9A0` - the same peel
shape as `0065E6B0` one
level down.
Interior anchor `006CC1E3`
(the `jmp`).

`006CC170` (106 B) runs
`006DC4B0([+8]+0x18, -1)`
then `006DC820` with the
caller's float plus the
`00902EF8` and `009159F8`
constants on the stack.
Interior anchor `006CC1C5`
(the `006DC820` call).

`006CC090` (218 B) is the
projection apply
`0065E610` tails into:
`006DBC20` on `[+8]+0x18`,
then - only while the flag
byte holds - `006DC600`,
`006DC760` with two stack
floats, `006DC700` with the
`008C5F6C`/`008F3134`
constants, `006DC650(-1)`,
and `006DBC60` with
`xmm3 /= 008C5F78`
(1000.0f).
Interior anchor `006CC11C`
(the `006DC700` call).

`006CBEA0` (485 B) is the
three-source descriptor
apply `0065E5C0` tails
into: it pulls the
`+0x90`/`+0x94`/`+0xA0`
fields and the `[+0x38]`
array's `[+0x10]` row out
of each of `rdx`, `r8` and
`r9` under the same
`[+0x30]` btr-31 count
guard, calls `vtable[+0x40]`
on the `r8` row, then runs
`006DD5F0`, `006DD700` and
`006DD570` on `[+8]+0x18`
with those fields before
`006DB660` flushes. The
`00615BC0`/`00624670`/
`0061C2B0`/`00616700` tail
cleans a `[rsp+0x90]` temp
object.
Interior anchor `006CBF2E`
(the `006DD5F0` call).

`006CBD20` (376 B) is the
one-shot feature init
`0065E5A0` tails into:
`01F31F70` gates a
`006DA8F0(02E5BDE0)` +
`006DAA50(00D86C00)`
registration pass;
`006DEF20` produces the
object stored at `[rcx]`;
a seven-qword `-1` table
at `[rsp+0xE0]` and a
`006CBBC0`-filled block
feed `006DAA70` (kinds 3
and 5, `0x780` size,
`0x20001` flags) with the
`"Failed to"` log
`00D899B0` on failure;
`006DB4C0`/`006DC5C0` set
defaults, then
`00210EC0(0x20)` allocates
the `00D899A8`-vtable
object stored at `[rbx+8]`
with its `+0x18` back-link.
Interior anchor `006CBE0A`
(the `006DAA70` call).

`006CBD00` (3 B) is the
`eax = edx` passthrough
`0065E630` calls before
tailing `006CC170`.
Interior anchor `006CBD02`
(the `ret`).

`006CBAA0` (73 B) is the
0x78-record initializer
`0065E530`'s ctor calls:
`+0x10`/`+0x1C` = 1000.0f,
`+0x14`/`+0x68` = 1.0f,
`+0x18` = 10.0f,
`+0x20` = 0.1f,
`+0x24` = 1, `+0x6C` =
`0x461C4000` and `+0x70` =
45.0f.
Interior anchor `006CBAB3`
(the `+0x10` store).

## SWE2-EC7-124 update (2026-09-21) - `0061C2B0` measured

`0061C2B0` (654 B) is the
bulk registration
`006CBEA0` runs on its
object: fifteen
`0061E6B0`/`0061E600`/
`0061E550` triples register
`rbx` into the
`02CEDA20`..`02CF0F20`
static descriptor blocks;
then eight `01F2DExx`
hook pairs are drained
(null-gated: clear then
call); `vtable[+0x18]`
queries an interface whose
`vtable[+0x128]` answers
`0xA000` or not - picking
`0x10`/`0x20` for the final
`vtable[+0x90]` call - and
`01F2DE88` is raised +
`02CED880` reset.
Interior anchor `0061C4DE`
(the `vtable[+0x18]`
query).

## SWE2-EC7-125 update (2026-09-21) - the `0061C2B0` commit's two descriptor-pair helpers measured

`0061E600` (175 B) is the
wider of the two range-commit
helpers `0061C2B0` runs: it
scans the `+0x80`-bounded
8-byte slot run from both
ends - front forward while
entries are null, back
inward while entries are
null - then counts the
surviving non-empty span,
feeds it to `00861EC0`
(count x 8-byte element
size), and finishes by
invoking the container's
tail `vtable[+0]` on the
trimmed range. The result
describes the populated
descriptor window the
commit consumes. Interior anchor `0061E691` (the
tail-vtable call).

`0061E550` (175 B) is the
same helper on the shorter
`+0x40`-bounded window: an
identical front/back null
trim, the same
`00861EC0`-sized span, the
same tail-vtable finish.
The two helpers are a pair;
`0061C2B0` picks the window
that matches the descriptor
slot it is committing.
Interior anchor `0061E5E1`
(the tail-vtable call).

## SWE2-EC7-126 update (2026-09-21) - the 0x48-stride record copy measured

`005D8340` (147 B) is the
record-array copy
`005DE460` and
`005E32F0` run: `r8d`
elements on a 0x48 stride,
each copying 0x30 bytes of
POD head (two `movups`, a
`movsd`, a dword), the
`+0x30` qword, then
`006C5020` deep-copies the
member at `+0x38` from
`rdi+8`. Null destinations
skip. Interior anchor
`005D83B4` (the `006C5020`
member copy).

## SWE2-EC7-127 update (2026-09-21) - record-copy and lock helpers measured

`006C5020` (173 B) is the
buffer-pair move-assign
`005D8340` and `006C4E20` call
for nested record data: it
zeroes `[rcx]`, takes the
source `{count | b31-flag,
ptr}` pair (heap `[rdx+8]`
when count>1, inline
`rdx+8` at 1, null at 0),
copies `count` elements via
`006A8C90`, then releases the
destination's old buffer
through `00584730` only when
it was heap-flagged,
non-null, and distinct from
both the new pointer and the
inline storage; the new count
lands at `[rbx]` and the ptr
at `[rbx+8]` unless it
already aliases the inline
slot.
Interior anchor `006C5060` (the `006A8C90` copy call).

`005CD720` (174 B) is the
recursive-lock enter
`00615BC0` wraps: a
`lock xadd` bumps the waiter
count `[rcx+0x18]`,
GetCurrentThreadId
(`008C21D8`) is compared
against the owner dword
`[rbx+0x20]` and claimed by
`lock cmpxchg` when free;
otherwise it waits on the
`[rbx+8]` event through
`008C20E0`, treating
`WAIT_ABANDONED` (0x80),
`WAIT_TIMEOUT` (0x102) and
`-1` as retry. On success the
recursion depth `[rbx+0x24]`
is bumped, the waiter count
is dropped, and the return is
1.
Interior anchor `005CD763` (the owner `lock cmpxchg`).

## Three corrections from the S-39 contract (OPUS, 2026-09-21)

All three were found by disassembling bodies this page already names, while assembling
[`CONTRACT-render-command-list-and-graphics-handshake.md`](../CONTRACT-render-command-list-and-graphics-handshake.md).
Filed as `CON-149`, `CON-150` and `CON-151`.

**There are two list TYPES, not one type in two globals (`CON-150`).** §2.1 declares one struct —
`RenderCommandList base=record size=0x20`, from `0018C9E0`'s constructor — and §7's UQ-228 answer
then describes the consumer reading `+0x20` (a mask) and `+0x24` (a split) of "the list". A `0x20`
type has no `+0x20`. The sizes are allocation immediates: `0018B4AB` is `lea ecx, [rbx + 0x30]`
into `malloc` for the object at `[01F7F5E0]`, and `0018C9F9` is `mov ecx, 0x20` for the one at
`[01F7F5E8]`. The `0x30` object's constructor `0018AD00` writes four fields the `0x20` object has no
room for — `classMask` at `+0x20` (`0018AD39`), `forwardSplit` at `+0x24`, a zeroed word at `+0x29`
and `reverseMark` at `+0x2C` — and **reserves 5,000 entries** through `0018B320` at `0018AD48`,
which the `0x20` object never does.

**And only one of them owns the command objects.** `0018B810` walks `[01F7F5E8]` and calls every
element's slot 0 with `edx = 1` — the scalar-deleting form, so `free` runs (`0018B850`–`0018B860`).
`0018B040`, the ordered list's clear, calls `0018B3F0(list, 0)`, whose shrink arm at
`0018B43B`–`0018B46B` only moves `pEnd` back to `pBegin` and touches no object. **The teardown order
follows and is identical at ~~both~~ all three sites** *(corrected 2026-10-02, OPUS: the third is the scene teardown, `001E0590`+0x19 clear then +0x26 flush; CONTRACT-render-command-list-and-graphics-handshake.md I-2)*: clear the non-owner first, destroy second — `0017CD53`
then `0017CD60` in the frame tick, `00188204` then `00188211` at the end of the render pass. Both
are now declared in `_types` as `OrderedCommandList` (0x30) and `RenderCommandOwnerList` (0x20).

**`+0x10` is not an `enabled` flag (`CON-149`).** §2.2 names it so; its **one** reader is
~~`0018C934`~~ `0018C933` *(corrected 2026-09-29, OPUS: the instruction starts there)* inside the flush `0018C8F0` — `cmp byte ptr [rdi + 0x10], bpl` with `bpl` zero — and
`0018C937` skips the execute when the byte is **non-zero**, so the flush runs the object precisely
when it is `0`. **Neither walk tests it at all**: the complete bodies of `0018B100` and `0018B1B0`
filter on slot 2 against the masks and on nothing else. The base constructor sets `1` (`00212CD5`)
and exactly four command constructors clear it — `001F1799`, `001F196A`, `001F1CE4`, `001F1E3E`,
whose vtable stores identify them as `009030B0` `ApplyJsonForCutSceneObj`, `00903390`
`EnableDofObj`, `009030D0` `ReadPresetDofForCutSceneObj` and `009033B0` `SetDofObj` — **the JSON and
depth-of-field settings commands, not draw jobs**. So the byte selects whom the flush applies at
teardown, which is why §6's JSON seam takes effect on frames whose class mask excluded those
commands from both walks. Declared as `OrderedObject +0x0010 flushSelector`.

**`0018B4E0` does not assert (`CON-151`).** §3's table says it "asserts non-null". It computes
`cl = ([01F7F5E0] != 0)` at `0018B4E6`–`0018B4ED`, passes it to `0016D6A0` at `0018B4F0`, and then
returns the global unconditionally at `0018B4F5` — and **`0016D6A0` is three bytes, `ret 0`**. It is
the same `/OPT:ICF` fold this database records at `B-2/a`, `AS-5` and `VA-3`, here landing on an
assertion. The same shape is in `0018B480` (`0018B49D`) and in the render pass (`00187CF2`).

**One invariant nobody had recorded: the forward walk can terminate early.** `0018B16C`–`0018B17C`
branches to `0018B192` — the loop's **exit** — when `byte[01DF08FC] == 0` and `byte[01F7F594] != 0`.
`01F7F594` has exactly one reader (that site) and two writers, one of which is
`AmbientOcclusionObj::Execute`: `001F29A3` `mov byte ptr [01F7F594], 1`, reached only when AO
actually ran, since both early-outs at `001F28C5` and `001F28D2` jump past it. The render pass arms
the mechanism immediately before the part-0 walk — `00188103` tests render params `+0x199` and, when
set, zeroes both globals at `0018810C`/`00188113` — and restores `01DF08FC` at `00188144`. Registered
as `GC-1`. **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): it is the developer console's "Display AO Only" view.**
Console command 42 carries that label and is the only byte writer of `+0x199` found. So the walk stops after
ambient occlusion in order to leave the AO result on screen alone. It is a debug view, not a shipped path.
[The render command-list contract](../CONTRACT-render-command-list-and-graphics-handshake.md) I-7 has the
evidence and its domain.

**And two structural facts §2.1 and §4.3 leave out.** The reverse walk `0018B1B0` calls slot 2
**twice per entry**, once against the caller's mask (`0018B247`) and once against the list's
(`0018B258`), reloading the element in between. The ordered list carries a **second** mark,
`reverseMark` at `+0x2C`, independent of the `+0x24` split: `-1` means "walk everything"
(`0018B1EB`, `0018B214`), `0018B030` sets it to the current count, and its only wrapper is
`001829F0`. Both are in the contract's §4 as I-5 and I-8.

`0018ADB0` (562 B) is the call-free insert `0018B3F0` calls: `(end-start)/8` bounds the index `r8d`, the tail shifts down by `008C2A40` (memmove) either from the back or around the insert point, `rep stosq` fills the gap with `r12`, and `[r15+8]` advances - the list's single-element insert.

Interior anchor `0018AE27` (function `0018ADB0`).

`001C2DB0` (323 B) is the two-pass reset `00187950` (the render pass list) runs: `00189120` context thrice, `00186AA0`/`00186A90` fetch pair into `rsi`; when `dword[rbx+0xC]` nonzero it `001EA830`s every 0x230-stride record at `rbx+0x118` (count `dword[rbx+0x4610]`, then zeroes the count), and when `byte[rbx+0x463C]` nonzero repeats over `[rbx+0x4618]+0x108` records (count `+0x4638`) - the pass list's per-frame table clear.

Interior anchor `001C2E2A` (function `001C2DB0`).

`001C3600` (161 B) is the vector-clone `001C3760` runs: `([rdx+8] - [rdx]) >> 4` counts the source's `0x10` records, `001EDF00` initialises the destination and `[[rdi+0x18]]->+0x10` allocates `count*16` bytes, begin/end/capacity land at `[rdi]`/`+8`/`+0x10`, and `001C3590` copies the range with the caller's `+0x60` flag byte

Interior anchor `001C3682` (function `001C3600`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-ordered-render-command-list-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001C3590` | 108 B | stores `r9` at qword `[rcx]`; then, while the source pointer `rdx` differs from `r8`, calls `001FE6B0` with `rcx` = the current qword `[rcx]` and `rdx` = the current source when that qword is non-null, and advances both the source and qword `[rcx]` by `0x10`; returns `rcx` | `001C35AB`, `001C35AE`, `001C35D2`, `001C35EA`, `001C35F1` |
| `001D85A0` | 21 B | stores the dword `0x40C00000` at `+0x8C` of `rcx` and the dword `0x437F0000` at `+0x88`, then returns | `001D85AA` |
| `001E5270` | 31 B | calls `0018B4E0` with `rcx` unchanged and tail-jumps `0018AFF0` with its result as `rcx` and qword `+0x10` of the original `rcx` as `rdx` | `001E5279`, `001E527E`, `001E528A` |
| `001F1B80` | 68 B | calls `00212CC0(rcx)`, stores `edx` at dword `+0x18` and the address `009031D0` at qword `+0x0` of `rcx`; then stores to dword `01F82EC0` its old value plus 1 when `edx` is non-zero, or 0 when `edx` is zero (`cmove`); returns `rcx` | `001F1B8F`, `001F1B9B`, `001F1B9E`, `001F1BB2`, `001F1BB5` |
| `001F1C30` | 118 B | calls `00212CC0(rcx)`, stores the address `009032D0` at qword `+0x0` of `rcx` and zeroes qword `+0x18`; stores `00210EC0(0x200)` at `+0x18`, calls `00861EC0(that buffer, 0, 0x200)`, then calls through the import qword `008C2F70` with (qword `+0x18`, `rdx`, `0x1FF`); returns `rcx` | `001F1C4E`, `001F1C6B`, `001F1C70`, `001F1C7F`, `001F1C91` |
| `001F2520` | 79 B | stores the address `009032D0` at qword `+0x0` of `rcx`, calls `00809950(qword +0x18, 1)` and then `00212CE0(rcx)`; when bit 0 of `edx` is set also calls `00809950(rcx, 0x20)`; returns `rcx` | `001F2533`, `001F2542`, `001F254A`, `001F254F`, `001F255C` |
| `001F29E0` | 50 B | calls `00188AC0(00189120())`, then tail-jumps `005FEFD0` with `rcx` = the incoming `rdx` and `edx` = dword `+0x18` of the incoming `rcx` | `001F29F0`, `001F29F8`, `001F29FD`, `001F2A0D` |
| `001F32B0` | 46 B | tail-jumps `00191130` with `rcx` = `00193D50()`, `rdx` unchanged and `r8d` = dword `+0x18` of the incoming `rcx` | `001F32C0`, `001F32C5`, `001F32D9` |
| `001F39E0` | 30 B | calls `001B7F20` with `rcx` unchanged and tail-jumps `001B7D50` with its result as `rcx` and the incoming `rdx` | `001F39E9`, `001F39F1`, `001F39F9` |
| `0022A550` | 44 B | returns 1 when byte `02064AD3` equals 2 and `00358330(1)` returns non-zero; otherwise returns 0 | `0022A554`, `0022A562`, `0022A56B`, `0022A575` |
| `002640E0` | 30 B | returns float `+0xE0` of the qword `+0xB8` of `rcx` when byte `+3` of `rcx` AND `0xE0` equals `0x60`; otherwise returns 0.0 | `002640E6`, `002640EA`, `002640F5` |
