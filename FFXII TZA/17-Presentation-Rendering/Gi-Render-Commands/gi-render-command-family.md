---
system: The Gi* render command family — PS2 drawing vocabulary in a 2017 remaster
category: 17-Presentation-Rendering
status: AUDITED
evidence_tier: 1
owner_layer: CodeDomain — mixed; no PrimaryOwner
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `001D76A0`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 8
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 1
---

# The `Gi*` render command family

**Eighteen classes carrying the PlayStation 2's drawing vocabulary into a 2017 PC remaster** — and the
naming is not merely nostalgic: **it survives into the code.**

## 1. What the player sees

**The 2D layer.** Sprites, coloured rectangles, screen images, the primitives the UI and effects are
built from. `GiBeginScene` and `GiEndScene` bracket the work; the commands between them stream
vertices to a device.

`Gi` reads as **graphics interface**, and `GiPolyGT4T` is the PS2 Graphics Synthesizer convention —
**G**ouraud, **T**extured, **4** vertices. FFXII was a PlayStation 2 game in 2006; this is its drawing
vocabulary still in place, with the same names, eleven years later.

## 2. Native mechanism

**These are command objects, not owned objects** — submitted and discarded. Sixteen of the eighteen
have **no deleting destructor at all**, which is why the family surfaced as a block in the object-size
census ([vtable method index](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) §10).

**The two-slot contract is `(prepare, execute)`** — not `(destructor, execute)`. Where slot 0 has a
real body it resolves resources; slot 1 runs the command against a device.

### Four shapes, not one

| shape | n | form |
|---|---:|---|
| **A — device-vtable command** | **14** | `execute(this, device)`, streaming through `[dev+…]`, 130–1079 B |
| **B — direct-call command** | 1 | `GiSetTexture`, 17 B: reads three of its **own** fields, tail-jumps to `FUN_00210570`, **ignores the device argument** |
| **C — reset commands** | 2 | `GiResetRenderTargetObj`, `GiResetDefaultRenderTargetObj`: **three slots**, and **the only two that own a deleting destructor** (`0x20`) |
| **D — empty** | 1 | `GiEndEff`: **both slots folded onto `0016D6A0`** (`_guard_check_icall`, body `C2 00 00` = `ret 0`) |

Shape A: `GiBeginEff GiBeginScene GiColorRect GiEndScene GiNormal GiPolyGT4T GiPrim GiScreenImage
GiSetRtForRtSampling GiSprite GiTrans GiTransNz GiVmax GiZNormalOnOff`

**`GiEndEff` is the eighteenth class and it is invisible to the vtable index**: with both slots folded
it owns no unique method, so it appears in no per-class listing. It exists only because the RTTI
recovery names it.

### The device interface, recovered by use

Twenty device vtable slots, from the `Gi*` call sites alone:

```
[dev+0x000] 5   [dev+0x048] 3   [dev+0x0A0] 6   [dev+0x130] 1
[dev+0x008] 5   [dev+0x058] 4   [dev+0x0A8] 6   [dev+0x138] 6
[dev+0x020] 5   [dev+0x078] 8   [dev+0x0B0] 1
[dev+0x030] 3   [dev+0x080] 8   [dev+0x0D0] 1
[dev+0x038] 1   [dev+0x088] 6   [dev+0x0D8] 1
[dev+0x040] 7   [dev+0x098] 8   [dev+0x128] 4
```

`+0x78` / `+0x80` / `+0x98` occur together in eight commands each — a recurring triple.
**`GiBeginScene` → `[dev+0x130]` and `GiEndScene` → `[dev+0x128]` are the scene bracket.**
*(2026-09-26 (FABLE, Claude Opus 5.5), against the device's own vtable `PrimitiveRendererD3D11` `00D86960` (§20e): `+0x80` and `+0x88`
are both a constant stub, `mov eax, 0x17; ret`, so one leg of the triple does nothing on this device. And `+0x128`
is also called by `GiSprite` and `GiPrim`, so it is not only the end of a scene. Control: [`bg56_gi_bodies.py`](../../_index/candidates/bg56-gi-bodies/bg56_gi_bodies.py).)*

**~~`[dev+0x000]` is vertex reservation~~:** *(corrected 2026-09-26 (FABLE, Claude Opus 5.5), `BG-6`: slot 0 reserves nothing and
ignores the count. It returns a fixed staging area of `0x7FE0` bytes (682 vertices of `0x30`) and publishes it. The
count goes to slot 4 (`+0x20`), whose batcher checks it against 682 and flushes.)*

```asm
mov rax, [device]
mov edx, <count>
mov rcx, device
call [rax]              ; returns a write pointer in rax
                        ; the body then streams dwords from its own fields:
                        ; [cmd+0x10] -> [rax], [cmd+0x14] -> [rax+4], ...
```

## 3. Key addresses

| class | slot 1 | reservation count |
|---|---|---|
| `GiPolyGT4T` | `00864860` | **4** — constant |
| `GiSprite` | `00864330` | **4** — constant |
| `GiColorRect` | `00863850` | **4** — constant |
| `GiScreenImage` | `0020E6C0` | **4** — constant |
| `GiPrim` | `00863D80` | **a field** — variable |
| `GiTrans` | `00862D40` | variable |
| `GiTransNz` | `00862EC0` | variable |
| `GiNormal` | `008651A0` | variable |
| `GiResetRenderTargetObj` | `001F3260` | **not a reservation** — see §16 |
| `GiResetDefaultRenderTargetObj` | `001F3210` | **not a reservation** — see §16 |

Also: `GiSetTexture` → `FUN_00210570`; `GiPolyGT4T` slot 0 resolves through `FUN_002D7FA0` /
`FUN_002D7EE0`; shape-C slot 1 calls `FUN_00609710`, `FUN_00600A60`, `FUN_00188730`, `FUN_005FEFD0`.

## 4. Data structures and formulas

### The PS2 naming test — and why the contrast is the proof

`GiPolyGT4T` predicts **four** vertices, and its body passes literal `4` to the reservation call.
**A constant alone would be weak evidence.** The discriminator is what the *other* commands pass:

```
GiPolyGT4T     mov edx, 4              constant
GiSprite       mov edx, 4              constant
GiColorRect    mov edx, 4              constant
GiScreenImage  mov edx, 4              constant
GiPrim         mov edx, [field]        VARIABLE
```

**The one command whose name does not promise a fixed count is exactly the one that reads the count
from a field.** Four fixed-quad commands hardcode 4; the generic primitive does not. **The PS2 drawing
vocabulary survives into the bodies, not just into the symbols.**

> ~~Independent support from a third group: the two shape-C reset commands pass **3**, not 4 — a
> different number for a different sub-family, matching the shape break exactly.~~
> **WITHDRAWN, pass 8.** Neither reset command makes **any** device-vtable call. Their `3` is the
> second argument to a direct `call FUN_00600A60`, a different function reached a different way. It is
> not a reservation count and it is not support, independent or otherwise, for the reservation-count
> discriminator. See §16.

### A retracted reading

> ~~`0x3FFF` / `0xE00` / `0xDFF` in `GiPolyGT4T` are PS2 coordinate masks.~~ **RETRACTED by the
> analyst before publication.** Slot 0 reads `[this+0xF8]`, masks `& 0x3FFF`, compares against
> `0xE00`/`0xDFF`, and uses the result to resolve two pointers into `[this+0xD0]`/`[this+0xD8]`. It is
> a **14-bit resource id lookup**, not geometry.

## 5. Call chain

```
GiBeginScene   -> [dev+0x130]
   ...
   GiPolyGT4T slot 0   resolve a 14-bit resource id -> [this+0xD0] / [this+0xD8]
   GiPolyGT4T slot 1   [dev+0x000] reserve 4 vertices -> write pointer
                       stream [cmd+0x10], [cmd+0x14], ... into it
                       further [dev+...] calls
GiEndScene     -> [dev+0x128]
```

## 6. Modding notes

- **`[dev+0x000]` is the vertex tap for the quad and primitive emitters — but not for the family.**
  **5 of the 14 shape-A commands reach it**: `GiColorRect`, `GiPolyGT4T`, `GiPrim`, `GiScreenImage`,
  `GiSprite`. A hook there sees those five and **misses `GiTrans`, `GiTransNz`, `GiNormal` and
  `GiZNormalOnOff` entirely**, which reach the device only through `+0x78`/`+0x88`/`+0xA0`/`+0xA8`.
  *(Corrected pass 8 — this previously read "every shape-A command", contradicting this document's own
  §2 census, which has always said 5. See §16.)*
- **`GiSetTexture` bypasses the device**, so a device-level hook will not observe texture changes.
- **`GiEndEff` is inert** — both slots folded onto `0016D6A0`, whose body is a bare `ret`. Not a hook
  point. That address is **`_guard_check_icall`**, an `/OPT:ICF` fold carrying many identities (open
  question **BA-1**); it is *not* a CFG guard, and **11 of the 18 `Gi*` classes have slot 0 folded onto
  it**, so "prepare" is a no-op for most of the family.

## 7. What is not known

- [x] ~~The device class is unidentified.~~ ~~**ANSWERED - it is not an RTTI-bearing
      class at all**, established over the complete 16-class candidate set. Section 10.~~
      **RESTATED 2026-09-22 (FABLE), §20e — the class IS RTTI-bearing: `PrimitiveRendererD3D11`,
      vtable `00D86960`, locator `01D380D0`.** The 16-class scan's real result was that the
      **interior subobject** carries no locator of its own, which is true of every embedded member.
      `[dev+0x000]` remains inferred, now tracked separately as **BG-6**. **BG-1.**
- [x] ~~The device vtable is **certainly larger** than 20 slots — these are only what `Gi*` touches.~~
      **ANSWERED 2026-09-22 (FABLE), §20e: it holds exactly 45 slots.** The device is
      `PrimitiveRendererD3D11`, vtable `00D86960` (locator `01D380D0`), 45 entries ending at slot 44
      `006CB540`; the highest slot `Gi*` calls is 39 (`+0x138`), and all twenty recovered offsets
      resolve to that class's methods. **BG-2.**
- [x] Why the two reset commands alone own a destructor, and what their slot 2 does. **BG-3.**
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BG-3): they are a different kind of object — heap
  `OrderedObject`s kept in a list, not ring-arena commands.*
  - **A different base.** RTTI gives both reset classes the single base `OrderedObject` (vtable `009010B8`, 3 slots).
    The other sixteen `Gi*` commands are two-slot `GeometryInstance`s (§18a).
  - **Heap allocation.** The only constructor call for `GiResetDefaultRenderTargetObj` is `0018BFDB` in `0018BFA0`,
    which `malloc`s 0x20 bytes (`0018BFC2`), constructs the command, and appends the pointer to a vector at
    `[rdi+8]`/`[rdi+0x10]`. `0018BFA0` is called from the `GiEndScene` factory `001FBE50` (`001FBEB9`).
  - **Why only they have a destructor.** Slot 0 (`001F2360` / `001F23A0`) runs the base teardown `00212CE0` and, when
    bit 0 is set, frees 0x20 bytes. Arena commands never need one, because the ring overwrites them.
  - **Slot 2 is the order key.** `00879750` is `mov eax, [rcx+0x18] ; ret`, and the constructor stores its `edx` argument
    at `+0x18` (`001F1ADB`). The base constructor `00212CC0` sets `+0x08` = 0 and `+0x10` = 1.
  - **Slot 1 executes.** `001F3210` / `001F3260` reset the render target through the renderer (`00188730` for the default target, `001893C0` for the other) with optional
    begin/end calls around it.

  (The function list's name for the constructor `001F1AC0`, `scheduler_resource_allocation_error`, is a mislabel; the
  body is this constructor.)
- [x] `FUN_00210570`, `GiSetTexture`'s target. **"A global texture-set routine" is a shape, not an
      identification.** **BG-4.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BG-4):* **it registers a texture under its
      PS2 texture id in the global texture-id table that the VIF1 draw path looks up.**
      - **The command.** `GiSetTexture`'s execute slot `00863040` passes the command's `u16` id (`+0x08`), its texture
        pointer (`+0x10`) and a dword (`+0x0C`) to `00210570`. The device is ignored because none is needed.
      - **The table.** `00210570` stores `{pointer, dword}` into entry `id` of the 16-byte-stride table `01F83580` when
        `id < 0x4000` (`00210570`–`0021058C`). ***Corrected 2026-09-24 (FABLE, Claude Opus 5.5): the test is
        signed.*** It is `cmp cx, 0x4000 / jge` followed by `movsx rax, cx`, so ids `0x8000`–`0xFFFF` pass as
        negative and write up to 512 KB **below** the table. Id `0xFFFB` writes the image-address base `01F83530`.
        An original-code replay shows `0020E600` resolving every authored reference through the texture pointer
        afterwards. The id producers read keep ids below `0x4000` at the shipped frame width, so the route is
        undriven, not absent. See the
        [authored-table contract](../../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md)
        §7, "The image-address base: what the image initialises, and what later code could write".
      - **The readers.** There are exactly two, both in the VIF1 layer: `0020F250` and `0020EB60`. Each derives the key
        from a GS `TEX0` register as `(TEX0 >> 37) & 0x3FFF` and copies the entry into the current-texture slot
        `01FD3688`. When `TEX0`'s `0x3F00000` field is below the threshold (`0x300000` / `0x200000`) the slot is cleared
        instead ([the VIF1 / VU1 layer](../Legacy-PS2-GS/the-vif1-vu1-layer.md) §2.1).
      - **So `GiSetTexture` is the PC-side bind** of a PS2 texture id to a real texture, consumed when a converted GS
        packet names that id.
- [x] Six shape-A bodies (`GiColorRect`, `GiScreenImage`, `GiSprite`, `GiPrim`, `GiNormal`,
      `GiBeginEff`) were profiled for device slots and immediates but **not read line by line**.
      **BG-5.** **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): all six are read, against the device's vtable.** Control: [`bg56_gi_bodies.py`](../../_index/candidates/bg56-gi-bodies/bg56_gi_bodies.py)
      (6 checks, FAILS 0). Read line by line by a delegated read-only pass; its anchors are re-checked here.
      - **The quads.** `GiSprite`, `GiColorRect` and `GiScreenImage` each draw one 4-vertex quad through slot 4.
        `GiSprite` reads an 8/7 (512/448) V-scale constant.
      - **`GiPrim`** draws a caller-sized primitive (`[+0x60]` vertices).
      - **`GiNormal`** makes no draw call; it only sets state.
      - **`GiBeginEff`** makes no draw call either.
      - Each body is slot 1 of the vtable its class's RTTI names.

## 8. Evidence

**Tier 1**, and a **two-session result**: analysis by peer session repos-39, re-verified here.

**Re-verified from the image:** 18 `Gi*` classes; the reservation-count discriminator exactly as
reported — `GiPolyGT4T`, `GiSprite`, `GiColorRect`, `GiScreenImage` pass constant **4**, `GiPrim`
passes a field, and the two reset commands pass **3**.

**The one-body generalisation was withdrawn by its author.** An earlier pass read `GiTrans` alone and
called the family uniform. Reading all eighteen showed **four shapes**, with `GiTrans` representing
only the medium device-command group — **a third of the family is not a device command at all.**

**An instrument error, caught and reported.** The device-slot scanner counted `call [vtbl+disp]` but
not **`jmp [vtbl+disp]`**. Several commands reach the device by tail jump, so `GiBeginScene`,
`GiEndScene` and `GiSetRtForRtSampling` were reported as making **no device call**, and three more
were missing a slot. Fixed: **18 slots → 20**, and three "inert" classes became single-call tail
jumps. **It was caught by disassembling a 13-byte body listed as empty** — an argument for reading the
small ones rather than trusting a size column.

**Shared-source caveat, stated by the analyst.** The class list, slot numbers and folding all come
from `methods.tsv` — **the same source as this database's vtable index** — so "18 classes" is that
source read again, not independent corroboration
([`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md), *agreement between
measurements that share a source*). **The bodies are read from the executable and are independent.**

## 9. Related

- [`../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md)
  — §10, where this family surfaced as the `NEITHER` block of the object-size census.
- [`../../16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`](../../16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md)
  — the `DynGeo*` classes, two of which share this family's destructor-less shape.

## 10. The device is not a C++ class — and the pipeline around it

### BG-1 answered: no RTTI, over the complete candidate set

The device cannot be named from the RTTI index, and that is established **exhaustively rather than by
elimination-by-plausibility.**

**The necessary condition:** `Gi*` calls `[dev+0x138]`, so the vtable must reach **slot 39**. Exactly
**16 classes in the whole RTTI index have a vtable that long.** Slot 0 of all sixteen was read against
the reserve contract — *takes a count in `edx`, returns a buffer the caller writes through*:

| n | slot 0 is | classes |
|---:|---|---|
| 2 | `AddRef` — `inc [rcx+8] ; mov eax,[rcx+8] ; ret` | `PPFX::IGPUDevice`, `PPFX::IGPUEffect` |
| 7 | an adjustor thunk — `add/sub rcx,N ; jmp` | `PrimitiveRendererD3D11`, six `SQEX::Sd::Driver::*Sound` |
| 7 | a destructor prologue | `btDiscreteDynamicsWorld`, six `SQEX::Sd::Lay::*Sound` |

> **THE EXCLUSION BELOW IS WEAKER THAN IT WAS PUBLISHED — see section 12.** It tested **one vtable
> per class**, and **7 of the 16 candidates have more than one.** `PrimitiveRendererD3D11`'s
> `add rcx,-8` was read as "an adjustor thunk, excluded" when it is the signature of a **secondary
> base**, i.e. of the very thing the scan was not testing.

~~**All 16 excluded, none by judgement.**~~ The two obvious candidates were said to fail for concrete
reasons:
`PrimitiveRendererD3D11`'s slot 0 is `add rcx,-8 ; jmp` — a secondary-base thunk — and
`PPFX::IGPUDevice`'s is a COM-style `AddRef` returning an **`int` refcount**, which the `Gi` bodies
would then be using as a write pointer.

**And no second user exists to name it from the other side.** The reserve idiom — `call [vtbl+0]` with
a count in `edx` and an immediate store through the returned pointer — occurs at **exactly 4 sites
image-wide, all `Gi*`.** Nothing outside this family touches the interface.

> **The device layer is either compiled `/GR-` or is a hand-rolled C-style vtable struct. It is not a
> Phyre class and not any class in the index.** The layer sits *below* the C++ object system.

**A caveat the analyst attached, and it is the right one:** the 16-candidate check is only as complete
as its necessary condition. "Slot 39" and "40 slots" assume a contiguous C++ vtable. **Given the
conclusion is that this is not a C++ class, that assumption is self-consistent but not free** — the
negative rules out RTTI-bearing classes, which is what was asked, not every possible dispatch table.

### The triple is a protocol, not three slots

```
GiColorRect  GiNormal  GiPolyGT4T  GiPrim
GiScreenImage  GiSprite  GiTrans  GiTransNz
                          all:  +0x78  ->  +0x98  ->  +0x80
```

**Eight of eight, same order, exactly once each, no exceptions** — re-verified here. Every drawing
command performs the same fixed three-step sequence. It belongs in the interface record as one
protocol rather than three independent entry points.

### Commands are bump-allocated from a shared arena

```asm
mov  rcx, [01F7F4C0]        ; the arena
mov  edx, 0xE0              ; the size  (GiSprite)
call FUN_001A1470
lea  rcx, [01CCFB08]
mov  [rax], rcx             ; install the vtable
```

**This converts last section's inference into a measurement.** The family's missing deleting
destructors were read as "commands submitted and discarded"; **this is the allocator call itself.**
`FUN_001A1470` is **93 bytes with 52 call sites**, and the sizes passed to it span 16 … 360 bytes —
including `0xE0` for `GiSprite`. Objects are never individually allocated with `operator new` and
never freed, which is also **why route B of the object-size census found nothing for them.**

### The display list

```
base   [0x02F8F2F8]
count  [0x02F8F2C6]   (u16)
stride 0x28
```

28 references to the base and 48 to the counter, all inside Presentation emitters at
`0x39D000`–`0x3A1000`, driven from render passes (`VFXSystem_RenderLayerPass`, `FUN_003A2BD0`,
`FUN_003A3740`).

*One emitter read whole 2026-09-19 (FABLE) - the blended point emitter `0039D970`:* what it appends is an entry with
null callback and argument, its own command list at `+0x18`, the projected depth word as the sort key with the pass
nibble `02AEE910` in bits 28-31, and a flag dword; the `GiPrim` it then builds goes onto that entry's list, not the
current one. Effect elements take this route only in a non-zero blend mode -
[the element types 0x00-0x0A](../Effect-File-Formats/the-element-types-00-0a.md), the section dated 2026-09-19 on the
walks of `0x01` and `0x03`.

### What this section does not deliver

- ~~**`[dev+0x000]` is still unread.** Reading its callee needs the device's vtable, which the section
  above says cannot be got statically. **"Reserve n vertices" remains inferred from the call site and
  the streaming that follows it — exactly as unconfirmed as before.**~~ BG-6. *(Answered 2026-09-26 (FABLE, Claude Opus 5.5):
  §20e names the vtable, and slot 0 `006CA760` is read. It overwrites the count register before reading it, and it
  returns this `+ 0x10880` (the index cell `+0x18860` is touched only by its own read and reset). So it is a fixed
  staging area, not a reservation. See the correction in §2.)*
- **The display list's drain was not found.** All 28 references to the base are **reads inside
  emitters**; nothing statically reads it to execute the list. The consumer reaches it through a
  copied pointer — **and that is the one remaining route that could still name the device.** BG-7.
- ~~`FUN_001A1470` was not read.~~ *Read 2026-09-13, see §17: a ring bump allocator that wraps to its base when full.* **"Bump allocator" is from the call shape and the absence of frees**,
  not from the body. BG-8.

## 11. The display list decoded — and a hypothesis of this database's own, disconfirmed

### The drain

`FUN_003A3740` (587 B) reads the count, early-outs at zero, sorts the list with the recursive
merge sort `FUN_003A3A50(0, count-1)`, then walks it with `add rbx, 0x28`.

**The record, 0x28 = 40 bytes:**

| offset | width | role |
|---|---|---|
| `+0x00` | qword | argument, passed as `rcx` to the callback |
| `+0x08` | dword | **the sort key** — `FUN_003A3A50` compares exactly this field (`003A3B53`, `003A3C83`); 24 bits of value with the display-layer nibble from `byte[02AEE910]` in the top byte at `+0x0B` (FABLE, 2026-09-20) |
| `+0x0C` | dword | an appender-supplied count — for the effect-element appender `FUN_00540DB0` it is the length of its chunk table in 16-byte units |
| `+0x10` | qword | **raw function pointer** — if non-null: `mov rcx,[rbx] ; call rax` |
| `+0x18` | qword | 16-byte node (arena-allocated by `FUN_0020E680`), used when `+0x10` is null |
| `+0x20` | byte | flags — bit 1 gates an early branch, bit 2 selects between deferred paths |

The sort copies whole records with `movups / movups / movsd` = **16 + 16 + 8 = 40**, confirming the
stride from the sort side as well as the walk side.

### This database's hypothesis was wrong

> **Predicted:** *"If the drain calls `[cmd_vtable + 8]` on each entry, that names slot 1 as execute
> from the consumer side."*
>
> **It does not.** The call is `call rax` on a **raw function pointer** taken from `+0x10`, with a
> **single argument** — `rcx` only, `rdx` never set. Verified here at `0x003A38C6`.

**So the `(prepare, execute)` contract gets no independent confirmation from the consumer side.** It
was a reasonable hypothesis, it was checkable, and it failed. The contract still stands on the
commands' own side; it simply has one fewer leg than hoped.

### Capacity, and a third leg under the no-destructor result

`FUN_003A3670` — the only writer of the list base — allocates **`0x190000` bytes = 1,638,400 =
exactly 40,960 records**, plus a `0xC8028` sort scratch and a data arena.

`FUN_003A3A00` is the **per-frame reset**: it zeroes the count and rewinds the data-arena pointer
`[0x02F8F2D0]` to its base `[0x02F8F308]`.

**That is the third independent leg under one conclusion.** The family has no deleting destructors
(§2); the commands come from a bump allocator (§10); and **the arena is rewound by a single pointer
store per frame**. Three separate observations, one mechanism: *nothing is freed because everything is
discarded at once.*

### The deferred path, and the default handler

```
record+0x18 (node) -> FUN_0020E630(node, 2) -> FUN_001FB810(node, 0x40)
   -> FUN_001A17F0([0x01F7F4D0], node[0], 0x40)
   -> handler = [global + 8] ; jmp handler->vtable[0](handler, payload, 0x40)
```

`[0x01F7F4D0]` is a **16-byte object installed once** by the CoreRuntimeScheduling installer
`FUN_0017D4C0` — the same function that installs the command arena at `[0x01F7F4C0]` and triggers
[the `0x480000` builder region](../../00-Engine-Core-Runtime/Startup-Data-Construction/generated-float-table-builders.md).

Its constructor `FUN_001A17D0` writes vtable `0x008F5F28` and then `mov [rcx+8], rcx`: **the default
handler is the object itself.** That vtable is **`GeometryRenderTargetImmediate`**, a one-slot class
whose slot 0 is `FUN_001F48B0`.

**An independent cross-check.** The object-size census had already listed
`GeometryRenderTargetImmediate` as `B_ONLY, size 0x10`, recovered from an allocation-site scan **before
any of this chain was traced**. The installer here allocates exactly `0x10`. **Two routes with no
shared derivation, same answer** — which, unlike two readings of one dump, is corroboration.

### BG-1 still does not close, and the reason is specific

**Eliminated:** every hop on the deferred chain passes `(object, payload, mode)`. **No hop carries a
device argument.** The display-list drain does not supply the device, so that route is closed.

**Not established:** that the device is statically unnameable. Two concrete gaps:

- **The Gi emitter writes the command pointer to `node+8`** (`mov [rsi+8], rax`), but the deferred
  path reads **`node+0`** (`mov rdx,[rcx]`). Different fields of the same 16-byte node. **Who reads
  `node+8` was not established** — and that is exactly where a `Gi` command's `execute(this, device)`
  must be invoked. **Unfound, not shown absent.**
- A direct image-wide hunt for the execute contract (`call [vtbl+8]` with a traceable `rdx`) returned
  **96 candidate sites**, none identifiable, and **none was nominated on proximity.**

> **The drain route is eliminated; the device remains *unnameable-so-far* rather than *proven
> unnameable*.** The single remaining question is **who reads `node+8`** — a far narrower target than
> where BG-1 started. **BG-9.**

## 12. Corrections, the execute site, and the device located

### 12a. The BG-1 exclusion was under-tested — and the stated reason for that was also wrong

**The error, confirmed.** §10's scan read **slot 0 of one vtable per class**. A class with multiple
inheritance has more than one vtable, so any such candidate was only partly tested.
`PrimitiveRendererD3D11`'s slot 0 being `add rcx, -8 ; jmp` was published as an adjustor thunk
disqualifying the candidate; **a negative `this`-adjustment is the signature of a *secondary* base**,
which should have prompted looking for the primary rather than closing the case.

**Measured here:** of the **16** classes whose vtable reaches slot 39, **7 have more than one vtable**:

```
PrimitiveRendererD3D11             00D86960  00D86AD0
SQEX::Sd::Driver::Sound            01CB5A30  01CB5B98  01CB5BA8
SQEX::Sd::Driver::CycleSound       01CB8C70  01CB8DD8  01CB8DE8
SQEX::Sd::Driver::OrderSound       01CB8AD8  01CB8C40  01CB8C50
SQEX::Sd::Driver::RandomSound      01CB87A8  01CB8910  01CB8920
SQEX::Sd::Driver::SwitchSound      01CB8E08  01CB8F70  01CB8F80
SQEX::Sd::Driver::VariationSound   01CB8940  01CB8AA8  01CB8AB8
```

**But the reason offered for the gap does not hold.** The correction was reported as *"the RTTI index
records one vtable per class, so the others are invisible to it"*. **It does not and they are not** —
`vtables.tsv` contains **28 classes with more than one vtable**, and it lists **both** of
`PrimitiveRendererD3D11`'s.

> **The flaw was in the scan, not in the index.** That distinction makes the repair far cheaper than
> proposed: it needs **7 classes re-tested against their extra vtables, straight from the index** —
> not an enumeration of every vtable from every constructor. **BG-10.**

**Recorded as two corrections rather than one**, because a right conclusion reached through a wrong
premise will mislead the next reader about what to fix.

### 12b. BG-9 answered — `FUN_001FB840` reads `node+8`

```asm
FUN_001FB840(rcx = node):
    rdx = [node+8]        ; the command
    rcx = [node+8]
    [node] = rcx          ; PROMOTE +8 -> +0
    rax = [rcx]           ; the command's vtable
    jmp [rax]             ; slot 0, this = command, NO device
```

**`node+8` is the staging field and `node+0` is the live field.** That is why the drain only ever
reads `+0` and why nothing appeared to read `+8`.

**Slot 0 = prepare, now confirmed from the consumer side**, and it runs **at emit time**, not at
drain time. `GiBeginScene`'s emitter shows it plainly: allocate **8 bytes** (a bare vtable pointer —
the command has no fields), install the vtable, store to `0x01F83078` = `0x01F83070 + 8`, then call
`FUN_001FB840(0x01F83070)`.

### 12c. The execute site — §11's prediction was right about the contract

```asm
FUN_001F4A10:
    001F4A19  mov rcx, [rcx]
    001F4A1C  call FUN_00624660          ; -> the DEVICE
    001F4A26  mov rcx, [rbx + 0x10]      ; the command
    001F4A2A  mov rdx, rax               ; the device
    001F4A2D  mov r8,  [rcx]             ; the command's vtable
    001F4A35  jmp qword ptr [r8 + 8]     ; EXECUTE(command, device)
```

**Verified here.** §11 recorded the prediction *"if the drain calls `[cmd_vtable+8]`, that names slot 1
as execute from the consumer side"* as **disconfirmed**. It was **right about the contract and wrong
about which consumer performs it** — the drain does not, this callback does. **`(prepare, execute)` is
now confirmed from both sides**, and §11's retraction is itself narrowed rather than reversed: the
drain genuinely does call a raw pointer with one argument.

The full path:

```
emitter -> arena-allocate command -> node+8
   -> FUN_001FB840   promote +8 -> +0, call slot 0            PREPARE
   -> display-list record +0x18
   -> FUN_003A3740   merge sort, walk
   -> FUN_0020E630 -> FUN_001FB810 -> FUN_001A17F0
   -> GeometryRenderTargetImmediate::slot0  (FUN_001F48B0)
   -> FUN_001F4950   wrap in a GeometryInstanceOrderedObject (0x28, vtable 00903920)
   -> its slot 1 (FUN_001F49F0) -> FUN_005FEA50 with callback FUN_001F4A10
   -> FUN_001F4A10   jmp [cmd_vtable+8](command, device)      EXECUTE
```

**A third route to 0x28.** `GeometryInstanceOrderedObject`'s slot 0 is a deleting destructor stating
**`mov edx, 0x28`** — matching the display-list stride recovered from the walk (`add rbx, 0x28`) and
from the sort's `movups/movups/movsd`. **Three independent routes, one number.**

### 12d. The device is located, and deliberately not named

```asm
FUN_00624660:  lea rax, [rcx + 0x18C0] ; ret
```

**The device is an embedded subobject at `+0x18C0` of a containing object** — not a separate
allocation. **That is why it has no RTTI of its own**: an interior subobject's vtable is installed by
its container's constructor, so it never gets a type descriptor.

~~**It is not asserted to be `PrimitiveRendererD3D11`.** That class's primary vtable slot 0 ignores
`edx`, while the `Gi` commands pass a vertex count there — so the primary vtable does not satisfy the
reserve contract either.~~ **THIS DISQUALIFICATION IS WITHDRAWN — see section 13.** The reasoning was
invalid: **a virtual call's parameter belongs to the *interface* contract, and an implementation is
free to ignore it.** "This implementation does not use the count" is not "this is not the
interface".

> **BG-1 is no longer a negative.** The device is `[ctx] + 0x18C0`, reached through a known getter at
> a known execute site. What remains is naming `[ctx]` at `FUN_001F4A10`. **BG-11.**

### 12e. The path has a frame-level queue in it, and BG-11 narrows to one unread body (FABLE, Claude Opus 5, 2026-09-20)

**§12c's diagram is right about every hop and wrong about the tempo of the last three.** `FUN_001F48B0` does not
call the wrapped record; it **appends it to a list** and returns:

```asm
FUN_001F48B0(handler, command, mask):
    001F48E5  001A1470(arena, 0x28)                ; the record
    001F4912  001F4950(record, command, mask)      ; vtable 00903920, +0x18 command, +0x20 mask
    001F4929  0018B4E0()                           ; -> the list in the global 01F7F5E0
    001F4940  jmp 0018AFF0(list, record)           ; push_back
```

`FUN_0018AFF0` is a bare `push_back` on a pointer vector (`[list+8]` cursor against `[list+0x10]` end, grow through
`FUN_001AB570`). The list is an **EASTL vector** — `FUN_0018AD00` names it through `FUN_001EDF00` with the string
`"EASTL vector"` at `008C5F58` — built **once at device init**, `FUN_00186CD0` → `FUN_0018B480`, with `0x1388` = 5,000
entries reserved and its filter word `+0x20` set to `0xFFFFFFFF`.

**The drain is the render pass list.** `FUN_0018B100(list, whole, device)` is called twice from `FUN_00187950` —
the render pass list that is application slot 8's render path
([the game application](../../00-Engine-Core-Runtime/Application-Root/game-application.md) §3) — once with
`whole = 1` at `00187D05` and once with `whole = 0` at `00188128`:

```asm
range = whole ? [0, list+0x24) : [list+0x24, count)      ; 0018B11B-0018B138
per record:  mask = record->vtable[2](record)            ; 0018B164, FUN_001F49E0 returns [rec+0x20]
             if (mask & [list+0x20]) == 0  -> skip       ; 0018B167
             if byte[01DF08FC] == 0 && byte[01F7F594] != 0 -> abandon the rest   ; 0018B16C-0018B17C
             record->vtable[1](record, device)           ; 0018B187, FUN_001F49F0
```

`+0x24` is a watermark set by `FUN_0018B510` (to 0, or to the current count), so the two calls run the prefix and then
the tail. **So the execute site of §12c is reached once per frame from the render pass list, not from the display-list
drain** — `FUN_003A3740` only *files* the record, through `FUN_0020E630`.

**And `FUN_0020E630` encodes a category, not a mode.** It maps `0 → 8`, `1 → 0x20`, `2 → 0x40`, `3 → 0x20` and
anything else to **`0`**, and that value is the record's `+0x20` mask. Since the list's own `+0x20` is `0xFFFFFFFF` at
every one of its three writers (`FUN_0018AD00`, `FUN_00185FB0`, `FUN_00186010`), **nothing is filtered out in the
retail image** — but a submit with a mode of 4 or more would produce a record that can never execute.

**BG-11, narrowed.** `[ctx]` at `FUN_001F4A10` is the **command block `FUN_005FEA50` wrote**, and that producer writes
only three fields of it:

```asm
FUN_005FEA50(target, fn, arg):   ; reserve 0x80 bytes in the ring [target+0x50 .. +0x58], cursor +0x60
    005FEAEE  mov dword ptr [rcx], 0x2F     ; opcode
    005FEAF4  mov [rcx + 8],  fn            ; FUN_001F4A10
    005FEAF8  mov [rcx + 0x10], arg         ; the Gi command
    ; and publishes the pending range in [target+0x88] .. [target+0x90]
```

`FUN_001F4A10` reads **`[block+0]`** and adds `0x18C0` to it, but the producer leaves the opcode dword there.
**So something between the producer and the callback writes the context over `block+0`**, and that something is the
render-thread executor for these `0x80`-byte blocks — **which was not found.** Searched and excluded: every jump table
in the image with 48–64 cases (the opcode vocabulary reaches `0x30`; the only full-width dispatcher, `FUN_007AB5C0`, is
the sound engine's and reads a different record shape), indexed handler tables in `005C0000`–`00630000`, and the
`call [reg+8]` / `mov rax,[reg+8]; call rax` shapes image-wide. What *is* established about the stream: **eight bodies
between `FUN_005FEA50` and `FUN_00600A60` share this exact reserve shape**, each writing its own opcode (`0x2F`, `0x2F`,
`0x16`, `0x17`, `0x13`, `0x10`, `0x03`, `0x18`); `0x2F` means **call `[block+8]` with the block** (its other
producer, `FUN_00610210`, pairs it with `FUN_005FE1A0`, which does `rcx = [block+0x10]; jmp FUN_005CD5E0`), and the
pending range is handed on by `FUN_00600D20` into a 256-slot `0x28`-stride queue at `02CE4720` under a lock, or by
`FUN_00600E30` into an object at `[target+0x130]` followed by an event signal — both thread-hand-off shaped.

> **BG-11 is now one body, not a search.** Find the executor that walks a `[start, end)` range of `0x80`-byte blocks
> and dispatches on the dword at `+0`; whatever it stores into `block+0` before calling `+8` **is** the container whose
> `+0x18C0` is the device.

## 13. Two corrections from the BG-10 repair, and a candidate restored

### 13a. The candidate set survives; the exclusions were aimed at the wrong tables

Re-run grouping by `(class, vtable)` instead of by class:

```
classes with >1 vtable                    : 28
(class, vtable) pairs reaching slot >= 39 : 16
distinct classes among them               : 16   <- unchanged
of those, multi-vtable                    : 7
```

**The extra vtables of the 7 multi-vtable candidates do not reach slot 39**, so the repair adds no
candidates. **But the original scan still read the wrong table for at least one:** for
`PrimitiveRendererD3D11` it read the secondary `00D86AD0`, while the slot-39-reaching table is the
**primary `00D86960`**. Same class, different vtable, different slot 0. **The set was right and the
exclusions were partly aimed at the wrong targets.**

### 13b. `PrimitiveRendererD3D11` is restored as the leading candidate

The disqualification rested on `FUN_006CA760` ignoring `edx`. **That reasoning is invalid** — an
implementation may ignore an interface parameter. And the part that matters **does** match the reserve
contract:

```asm
006CA760  mov   eax, [rcx + 0x18860]     ; batch index
          imul  rdx, rax, 0x7FE0         ; x 32,736-byte stride
          lea   rax, [rcx + 0x10880]     ; buffer base
          mov   dword [rcx + 0x18860], 0 ; reset the index
          add   rax, rdx
          mov   [rcx + 0xB8], rax        ; publish the current pointer
          ret                            ; returns a this-derived buffer
```

**It returns exactly what the `Gi` commands write through** (`mov [rax],ecx ; mov [rax+4],ecx ; …`)
and resets a counter — the shape of *begin a batch*. The multi-buffer stride also accounts for the
class's size.

Supporting, not proving: the `+0x18C0` subobject is constructed by `FUN_006C8750`, whose targets sit
in this class's method range — and that constructor **does** install two vtables:

```asm
006C8761  lea  rax, [rip -> 00D86960] ; 006C8768  mov [rcx],   rax   ; primary at +0
006C876E  lea  rax, [rip -> 00D86AD0] ; 006C877B  mov [rcx+8], rax   ; secondary at +8
```

**Spot checks are consistent but not conclusive**: the protocol triple has `+0x78` and `+0x98` both
entering a `+0x208` subobject, while `+0x80` → `FUN_0060D760` is `mov eax, 0x17 ; ret` — a
constant-returning query rather than a state change. Scene bracket: `+0x130` → `006CA7B0` (sets flags
at `+0x208F0/F3/931`), `+0x128` → `006C9B00`.

> **Still not proven.** Nobody has shown that `[ctx]` at `FUN_001F4A10` is the same container whose
> `+0x18C0` was traced. **That single step is BG-11 and it would close BG-1 properly**, and the
> identification is not asserted until it is done.

### 13c. The operand-role error, reintroduced 110 passes on

A discriminator built for this repair flagged "reads `edx`" by testing whether any operand **named**
`edx`. `FUN_006CA760` contains `imul rdx, rax, 0x7FE0`, which **writes** `rdx`. It was counted as a
read.

**That is the first error this database ever recorded** — *operand position is not access role* —
committed again, by the other session, more than a hundred passes later. Rebuilt with capstone access
roles and a read-before-write test, **the answer inverted: 3 of 16 became 13 of 16.**

**And the corrected instrument is worthless anyway**: consuming `edx` only means "a method with a
second argument". **Reported as a dead instrument rather than as a result** — which is the right
disposal, and the reason the inversion did not become a finding.

## 14. BG-12 — the exclusions redone, and §10 comes out stronger

The suspicion that prompted this was correct: **on the first honest pass, 12 of the 16 exclusions
rested on nothing.**

### A discriminator built so it could fail

Two disqualifications decisive from the caller-side contract
(`rax = vtbl.slot0(dev, n)`, then `mov [rax], r32 ; mov [rax+4], r32 …`):

- **DTOR** — slot 0 is a scalar deleting destructor. Cannot be a reserve.
- **SCALAR** — slot 0 returns an integer. Nothing to write through.

**Everything else reported as `UNKNOWN`** — *the exclusion rests on nothing*. **No
domain-plausibility bucket.** First run: **3 decisive, 12 UNKNOWN.**

### The UNKNOWN bucket fixed the instrument twice

**Round 1.** Reading one of the twelve (`FUN_007E5D30`, `CycleSound`) showed an unmistakable deleting
destructor whose deallocation goes through `FUN_007AD450` rather than a direct `free` — which the
test's enumerated free-entry list missed. Broadened to the **MSVC signature** (vtable restore plus a
`dl & 1` deleting flag), which is deallocator-independent. **That converted 11.**

**Round 2.** One survivor: `SQEX::Sd::Driver::Sound` (`FUN_007BD020`), same shape but **delegating the
vtable restore to its base destructor**, so it failed a test requiring the restore in-body. Relaxed to
the essential pair — **tests `dl & 1` and returns `this`**.

> **That pair cannot false-positive on the reserve contract**: a reserve returns a **buffer**, not
> `this`, and has no deleting flag. **This is an argument rather than a measurement**, and it is
> stated as one.

**Having an `UNKNOWN` bucket at all is what drove both fixes.** A binary excluded/not-excluded verdict
would have kept the under-detection silently.

### Final state — 16 of 16, zero unknown

| verdict | n | classes |
|---|---:|---|
| **DTOR** | 13 | six `SQEX::Sd::Driver::*Sound`, six `SQEX::Sd::Lay::*Sound`, `btDiscreteDynamicsWorld` |
| **SCALAR** | 2 | `PPFX::IGPUDevice`, `PPFX::IGPUEffect` — `AddRef` returns a refcount |
| **COMPATIBLE** | 1 | **`PrimitiveRendererD3D11`** — returns a computed pointer |
| **UNKNOWN** | **0** | |

**§10 is restored and stronger than it was first published**: 15 of 16 excluded on decisive
code-level signatures, **none on domain plausibility**, and each exclusion now aimed at the vtable
that actually reaches slot 39.

**Two independent routes converge on the sole survivor.** Elimination (15 of 16 disqualified by
slot-0 shape) and the construction trace (`lea rcx,[X+0x18C0]` landing in that class's method range)
**share no derivation**. That is convergence, not corroboration by restatement.

**It is still not an identification.** `COMPATIBLE` means *not disqualified by these two tests*.
It becomes an identification when `[ctx]` at `FUN_001F4A10` is tied to a container whose `+0x18C0` is
that subobject — **BG-11**.

> **Done, 2026-09-22 (FABLE), §20d.** `[ctx]` is the magic-static singleton `02CC0410`, whose sole
> constructor `FUN_00615840` builds the `+0x18C0` subobject. `COMPATIBLE` becomes **identified**.

### What this rests on, stated

- **The DTOR signature is MSVC-specific** and would not transfer to another compiler. Whether anything
  else in *this* image emits `dl&1` + `returns this` for a non-destructor **was not measured**.
- **The candidate set still assumes the device's dispatch table is a contiguous C++ vtable reaching
  slot 39.** If it is a C struct of function pointers, the whole set is beside the point — the same
  caveat attached to BG-1 in §12, unchanged.

*Incidental, verified here:* `SQEX::Sd::Driver::Sound` states **`mov edx, 0x538`** and `CycleSound`
**`mov edx, 0x540`** in their sized-delete branches — two free object sizes for the census.

## 15. The deferred queue, and why BG-11 is being banked

### `FUN_005FEA50` is an enqueue — verified

```asm
005FEAC4  mov qword ptr [rbx + 0x60], rax   ; bump pointer advanced
005FEAD7  mov qword ptr [rbx + 0x88], rcx   ; chain head
005FEAE5  mov qword ptr [rbx + 0x90], rax   ; chain end
005FEAEE  mov dword ptr [rcx], 0x2F         ; <- HARDCODED TAG
005FEAF4  mov qword ptr [rcx + 8],    rdi   ; callback
005FEAF8  mov qword ptr [rcx + 0x10], rsi   ; payload
```

**0x80-byte blocks bump-allocated from a region owned by the first argument**, chained at `+0x88` /
`+0x90`. The tag `0x2F` at `+0` is **identical for all ten callers**.

### The chain is bounded — verified three ways

```
RIP-relative LEA sites targeting FUN_001F4A10 : 1   (at 001F49FA, inside FUN_001F49F0)
8-byte absolute pointers to it in .rdata/.data : 0
direct E8 callers of FUN_001F49F0              : 0
```

**The callback's address is taken exactly once in the entire image and appears in no data table.** So
it is only ever reachable as the `+0x08` of such a block, and **`ctx` at `FUN_001F4A10` is that
block** — `[ctx+0x10]` = the command matches `+0x10` = payload exactly.

### And that is precisely where it breaks

`FUN_001F4A10` reads **`[ctx+0x00]` as a pointer** and adds `0x18C0` to it. But `+0x00` holds the
**hardcoded dword `0x2F`**, and the enqueue never writes a pointer there.

> **Something writes `ctx+0` between enqueue and invocation, and it has not been found.** That is a
> real structural fact, not a gap in the reading: the two ends of this chain are both verified and
> they **do not join**.

`FUN_001F49F0`'s own first argument comes from its vtable (`0x00903920`) with **zero direct callers**,
so the object owning the queue is supplied by a generic ordered-object executor that has not been
located either.

### The question, sharpened

**Not** *"what is `[ctx]`"* **but**: *who writes offset 0 of a queued block between `FUN_005FEA50` and
the callback — equivalently, what invokes `block->callback` at all.* **One findable thing**, and it
decides whether the container is the queue owner, something reachable from it, or a third object.

### Three instruments discarded, and one of them before it produced a result

| test | outcome |
|---|---|
| `mov qword [R], reg ; call [R+8]` — "the consumer overwrites the tag slot" | **3 sites image-wide, none in this subsystem.** Hypothesis unsupported. |
| `cmp` against `0x2F` | **27 sites**, all `'/'` path-character checks or unrelated `0x38`-stride arithmetic. |
| "functions touching both `+0x88` and `+0x90`" | **716 hits — discarded on sight.** Those offsets are far too common in this image to discriminate anything. |

**The third is the one worth recording.** It was built, run, and produced a large clean-looking list
that would have taken an hour to sift and **could never have meant anything** — the same failure class
as the `N=0` span metric and the `u8 < 251` test. **It was discarded at the point of seeing the count,
not after filtering it into a plausible shortlist.** That is the
[abstention rule](../../_index/EVIDENCE-STANDARD.md) working *before* a number gets published rather
than after.

### The call: BG-11 is banked, not abandoned

**Four passes have gone into one name.** The elimination result (§14) is strong, published, and
unaffected by this. The independent confirmation is not, and the remaining step — while well defined —
has now resisted three attacks.

**Against that: 86.5 % of the executable's code bytes are still in functions no document cites.** The
marginal value of one class name does not compete with that surface.

> **BG-11 stays open with its sharpened question recorded**, so it is cheap to resume for anyone who
> encounters the queue executor from another direction. **The caveat that made it worth doing is
> unchanged and still live:** §14's elimination assumes the device's dispatch table is a contiguous
> C++ vtable, and **BG-11 was the only line of attack independent of that assumption.**

## 16. Falsification pass 8 — 2026-09-02, by a session that did not write this document

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`. Claims attacked **in
provenance order — inherited and assumed first, body-derived last.** Seven prior passes had worked
the device identity hard, so this pass deliberately went at the claims *no* pass had touched: the
headline class count (which §8 itself flags as not independently derived), the modding advice, and
the numbers offered as corroboration.

### Three claims overturned

**1. §6: "Every shape-A command reserves through `[dev+0x000]`."** Only **5 of the 14** do —
`GiColorRect`, `GiPolyGT4T`, `GiPrim`, `GiScreenImage`, `GiSprite`. This document's **own §2 census
has always said `[dev+0x000] 5`**; §6 generalised it to the whole shape without checking. It matters
because it is a *modding* claim under "best intervention point": a hook at `[dev+0x000]` sees five
commands and silently misses `GiTrans`, `GiTransNz`, `GiNormal` and `GiZNormalOnOff`, which never
touch that slot.

**2. §3's "reservation count" column and §4's "independent support" for the reset commands.**
Re-derived from the bodies: **neither shape-C reset command makes any device-vtable call at all.**

```asm
001F3260  GiResetRenderTargetObj::slot1
          call 0x609710            ; -> al
          test al, al ; je ...
          mov  edx, 3              ; <-- the "3"
          mov  rcx, rbx
          call 0x600a60            ; a DIRECT call, not [dev+n]
          call 0x189120 ; call 0x1893c0 ; call 0x5fefd0
```

The `3` is the second argument to `FUN_00600A60`. It is not a vertex reservation, and it is not
support — independent or otherwise — for the reservation-count discriminator, which is a claim about
what commands pass to `[dev+0x000]`. Two mechanisms produced two `3`s and the agreement was read as
corroboration. **The document's own device-slot census already implied this**, since neither reset
command contributes a single slot to it.

**3. §10's "the reserve idiom occurs at exactly 4 sites image-wide, all `Gi*`."** Reproduced — and
the reproduction shows why it is 4. Re-run with a **positive control against the five known `Gi*`
reserve sites**, the scan returns **4 of 5**: it misses `GiPrim` at `00863DD1`, a call site *this
document describes in §4* as using the same reserve call with a variable count.

So the true count of `Gi*` sites through `[dev+0x000]` is **5**, and the "exactly 4 image-wide" figure
is the output of a filter with a demonstrated **1-in-5 false-negative rate on its own known-positive
set**. The conclusion it supports — *nothing outside this family touches the interface*, a leg under
**BG-1** — is not thereby refuted, but it is **not established at the strength stated**, because
`EVIDENCE-STANDARD.md` requires an absence claim's positive control to come back and this one comes
back short.

### Two claims confirmed, one of them promoted to independent

**The 18-class set no longer rests on a shared source.** §8 states plainly that "18 classes" comes
from `methods.tsv`, the same source as the vtable index, and is therefore "that source read again,
not independent corroboration". Re-derived here **straight from the EXE's RTTI** — `.?AV<name>@@`
type descriptors → complete-object locators (signature 1) → vtables — with a positive control on a
class proven by that route in another category:

```
Gi* type descriptors        : 18
(class, vtable) pairs       : 18   -> one vtable each, no multiple inheritance
two-slot classes            : 16
three-slot classes          :  2   -> GiResetRenderTargetObj, GiResetDefaultRenderTargetObj
```

Every count matches. **§8's shared-source caveat can be retired**: the class set, the slot counts and
the shape-C three-slot break are now confirmed from a route with no derivation in common with
`methods.tsv`.

**The 20-slot device census reproduces exactly.** All twenty slots, every per-slot count, zero
disagreements — including the four slots recovered by the `jmp` fix §8 records. The
`+0x78 → +0x98 → +0x80` triple holds at 8 of 8.

The reservation-count discriminator also reproduces: `GiColorRect`, `GiPolyGT4T`, `GiScreenImage`,
`GiSprite` each `mov edx, 4`; `GiPrim` `mov edx, dword ptr [r14 + 0x60]`.

### An instrument failure of my own, recorded

My first census regex accepted a vtable displacement only in `0x`-prefixed form. Capstone prints
small displacements bare, so `[rax + 8]` was invisible and the scan returned **19 of 20 slots** with
`+0x008` at zero against the document's 5. **The document was right and my instrument was wrong** —
and the shape of the error is worth keeping: a scan that agrees with its target in 19 places and
disagrees in 1 is far more likely to be broken in that 1 place than to have found something. I chased
the disagreement rather than reporting it, which is the only reason it did not become a false finding
in this section.

### Naming

`0016D6A0` is called "the `_guard_check_icall` stub" and "the CFG stub" in §2 and §6. Both updated to
**`_guard_check_icall`** (**BA-1**) — its body is `C2 00 00` (`ret 0`) and it carries many folded identities,
so it is not a CFG guard here. Related and not previously stated: **11 of the 18 `Gi*` classes have
slot 0 folded onto it**, so the `(prepare, execute)` contract §12b confirms from the consumer side has
a *no-op* prepare for most of the family.

### What I tried that failed to break it

- Attacked the 18-class headline expecting the shared-source caveat to hide an error. It did not;
  the RTTI route agrees exactly, which is the better outcome.
- Attacked the device-slot census expecting the earlier `jmp` instrument bug to have left residue.
  Zero disagreements across 20 slots after my own regex was fixed.
- Attacked the `+0x78 → +0x98 → +0x80` protocol claim by checking order and multiplicity per command
  rather than in aggregate. Eight of eight, same order, once each.
- Read the neighbouring documents that cite these addresses **before** attacking, rather than after:
  `vtable-method-index.md` (13 shared addresses) and `sqex-sd-sound-driver-architecture.md` (6 shared
  vtable addresses). Both agree with this document; the six `SQEX::Sd::Driver::*Sound` vtables are
  cited identically in each.

## 17. The factories, their write-only "current command" globals, and the ring arena (2026-09-13, FABLE; BQ-21, BG-8)

*The `Gi*` factories (BQ-21) and the arena (BG-8). Ledger rows are mirrored separately.*

**One vtable-installing function per class, 18 of 18.** A rip-relative census of every reference to the 18 RTTI vtables
finds exactly one installer per class, and two for each reset class (constructor and deleting destructor). Thirteen
factories sit together at `00862E50`–`00865320`.

| class | factory | arena size (`edx`) | per-class global written |
|---|---|---:|---|
| `GiTrans` / `GiTransNz` | `00862E50` / `00862FD0` | — | `02EAF900` / `02EAF910` |
| `GiSetTexture` | `00863060` | `0x18` | `02EAF920` |
| `GiColorRect` | `00863B40` | `0x70` | `02EB37F8` |
| `GiPrim` / `GiSprite` / `GiPolyGT4T` | `008642A0` / `008647C0` / `00864D10` | `0x68` / `0xE0` / `0x100` | none |
| `GiZNormalOnOff` | `00864E00` | `0x10` | `02EB3828` (two stores) |
| `GiBeginEff` / `GiNormal` / `GiEndEff` | `00865130` / `008652B0` / `00865320` | `0x90` / — / — | `02EB3838` / `02EB3848` / `02EB3858` |
| `GiSetRtForRtSampling` | `001F16C0` | `0x18` | `01F82EB8` |
| `GiBeginScene` / `GiEndScene` | `001FBD80` / `001FBE50` | — | `01F83078` / `01F83088` |
| `GiScreenImage` | `0020E9F0` | `0xC0` | none |
| `GiVmax` | `001DB220` (from `001DB840`) | `0x640` | none |
| `GiResetRenderTargetObj` / `GiResetDefaultRenderTargetObj` | `001F1AF0` / `001F1AC0` | **not arena** — constructed in place on the caller's object | none |

"—" means the size was not a literal immediately before the call.

**Each arena factory follows one shape.** `GiColorRect` (`00863B40`) shows it:
1. `rcx = [01F7F4C0]`, `edx = size`, call `001A1470`;
2. if the result is non-null, store the vtable at `[result]`;
3. store the result, **null or not**, into the per-class global;
4. return `result + 0x10` (the payload) or the object.

**The "singleton" globals are write-only in the retail image.** For all 11 globals in the table, every rip-relative
reference is the factory's own store (ripscan per global). Three further checks found no reference: no data qword,
absolute-32 or RVA constant holds any of them, the image-base displacement bytes of all 11 occur nowhere in `.text`,
and register-tracked `lea`-base searches around `02EAF900` and `02EB37F8` find nothing. **So each global records the
most recently created command of its class, and nothing reads it back.** This reads like a debugging aid kept in the
build; that reading is an inference. **The BQ-21 answer, then:** the `Gi*` "singleton factory" is a per-call arena
factory plus a write-only last-created pointer. No command object is shared or reused between calls.

**The arena `001A1470(arena, size)` is a ring, not a failing bump allocator** (BG-8; `001A1470`–`001A14CC`):
1. The request becomes `(size & ~0xF) + 0x10` (`001A147E`–`001A1489`).
2. If `cursor + request < end` (`[arena+8]`, `[arena+0x10]`), the cursor advances and the old cursor is returned
   (`001A149F`–`001A14A3`, `001A14BE`).
3. **Otherwise the cursor restarts at `base + request` and `base` is returned** (`001A14A5`–`001A14BD`).

The folded `0016D6A0` call (`001A1492`) is a compiled-out size assertion.

- **Consequence:** a frame that allocates more commands than the arena holds does not fail. It overwrites the frame's
  earliest commands in place.
- **Not read:** whether a caller resets the cursor each frame.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `001D76A0` | 885 | table-driven loop over `[r14+0x70..0x80]` + `[rdx+0xA]`: `0018A7D0`, `001D8240`, `001FBE30`/`001FBD80`, `001B1910`, `001B1C00` x11 + `001B22D0`/`001B22E0`/`001B22F0` once each — the `001Bxxxx` command-table family |

## 18. The `GeometryInstance` and `RenderObject` slot matrices — RTTI census (2026-09-14, SWE2-FRONTIER)

*FABLE-REQ-SWE2-FRONTIER-RENDER-VTABLE-SLOTS. Same method as the OrderedObject matrix on
the ordered-render-command-list page: `pub140-scratch/tools/rtti_vtables.py` walked by
**ancestry** (transitive base lists), frontier membership against the current
`frontier_now.txt`.*

### 18a. `GeometryInstance` — 24 classes, 144 slot positions, 68 distinct bodies

The family is exactly **24 classes**: the 16 two-slot `Gi*` commands §14–16 already
censused, plus the `DynGeoUIInstance` subtree — `DynGeoUIInstance`, `DynGeoTextureInstance`,
`DynGeo3DInstance` (21 slots each), `DynGeoFontTextInstance` (3), and the four
`DynGeoFontTextSpecial{,Shadow}{,Final}Instance` classes (12 each). The base
`GeometryInstance` itself has **no vtable in the image** — abstract, no complete-object
locator emitted — so slot semantics are named from the most-derived concrete reads.

The 68 distinct frontier bodies include `0016D6A0` (the folded `ret` stub, already named
in §16) — **67 uncovered**, matching the request's preliminary count exactly. The earlier
"29 classes / 81 bodies" scratch count came from a *name* match, which additionally
catches `GeometryInstanceOrderedObject`, the OrderedObject-based `GiReset*Obj` pair, and
four Phyre `POccluderGeometryInstance` reflection classes — none of which derive from
`.?AVGeometryInstance@@`. Ancestry, not naming, defines the family.

**Slot layout** (named once, from the bodies):

| slot | role | evidence |
|---:|---|---|
| 0 | **prepare** — `0016D6A0` no-op on 11 of the `Gi*` classes (the §12b `(prepare, execute)` contract's first half) | `ret` folded stub |
| 1 | **execute** — the command body proper; every class implements it | e.g. `DynGeoUIInstance` `00215440` → `001EE7C0`/`001EE650` device pair |
| 2 | scalar-deleting destructor — **only on DynGeo classes**; the 16 `Gi*` commands have no slot 2 at all (the §14 no-destructor result, now with the RTTI reason: `GeometryInstance` declares exactly two virtuals) | `00215390`-family `dtor + free` bodies |

`DynGeoUIInstance`'s slots 3–20 are its own interface, not `GeometryInstance`'s:
slots 3–8 read/write the **current segment record** (`movsxd rax,[this+0x1C0]` cursor into
the `this[+0x18]` stride-24 record array — e.g. `00216100` normalises two args into
`[seg+0x20]/[+0x24]`); slots 9/14 are `this[+0x08]`/`[+0x10]` setters (`00213560`,
`00213540`); slots 10–13, 15, 17 call the `001Bxxxx` command-table / text helpers
(`001B1C00`, `001B0FB0`, `001B10D0`, `001B1620`, `005C3A30`, `0019C5D0`, `0018A9E0`);
slot 18 is an `001A1470` arena allocation (`00215790`); slots 19–20 read `arg[0]`.
The four `DynGeoFontTextSpecial*` classes share bodies almost entirely — slots 0–5 and
7–9 are identical across all four (execute `00213FE0`, `+0xF8`/`+0x100` setters
`002146F0`/`002148E0`, `arg[0]` getter `00214830`). The variants differ only at slot 6
(Final `00213B40` vs the others' `00213D10`), slot 10 (four distinct bodies
`00214210`/`002142A0`/`002143E0`/`00214540`), slot 11, and partially slot 2.

Per-class × per-slot rows with interior citations:
[`members/geometry-instance-vtable-slots.tsv`](members/geometry-instance-vtable-slots.tsv)
(144 rows). *Unresolved:* the semantic names of DynGeo slots 3–20 beyond the shapes
above; which caller dispatches each.

### 18b. `RenderObject` — 3 classes, 29 distinct bodies

| class | vtable | slots | frontier |
|---|---|---:|---:|
| `RenderObject` | `00906D10` | 2 | 1 (slot 0 `00212C90`, scalar-deleting dtor; slot 1 shares a covered body) |
| `MapRenderObject` | `009012C0` | 2 | 1 (slot 1 `001E5270` → `0018B4E0`/`0018AFF0`) |
| `CharacterRenderObject` | `00903B68` | 31 | 27 |

`CharacterRenderObject` is the family's real surface: slot 1 `001F89B0` is the same
`0018B4E0`/`0018AFF0` event-pair entry as `MapRenderObject`'s; slot 2 `001F6E70` (2,328 B)
and slot 19 `001F8D10` (3,397 B) are the heavy render paths; the rest are character-state
accessors — byte getters/setters on `+0x498`, `+0x4B4`, `+0x4B6`, dword `+0x49C`/`+0x4B0`,
float `+0x4B8`/`+0x4BC`, pointer `+0x390` (`001F5C10`), and `001F6E50` a 14 B
`mov eax, edx` identity thunk. Slot 30 `001FA820` calls `001F0850` + `001945B0` twice.
Full rows:
[`members/render-object-vtable-slots.tsv`](members/render-object-vtable-slots.tsv).
*Unresolved:* what state `+0x4B4` etc. encode; slot numbers 8/13/29 share covered
bodies and are not frontier.

## 19. Whose ring the `0x2F` block belongs to — BG-11's container gets a named candidate (2026-09-22, FABLE)

§12e left BG-11 as *“find the executor that walks a `[start, end)` range of `0x80`-byte blocks… whatever it
stores into `block+0` **is** the container whose `+0x18C0` is the device.”* This pass did not find that executor.
It did establish **whose ring the block is reserved in**, which constrains the answer, and it **names the object
this document has been calling the device at the walker hop**.

### 19a. The ring's target is the walker's `device` argument (FABLE)

```asm
FUN_001F49F0(record /*rcx*/, device /*rdx*/):      ; the OrderedObject execute slot
  001F49F0  mov r8,  [rcx + 0x18]     ; the Gi command        -> FUN_005FEA50's arg
  001F49F4  mov rax, rdx              ; the device argument
  001F49F7  mov rcx, rax              ;                       -> FUN_005FEA50's TARGET
  001F49FA  lea rdx, [rip + 0xF]      ; = 001F4A10            -> FUN_005FEA50's fn
  001F4A01  jmp 0x5FEA50
```

§12e recorded the three fields `FUN_005FEA50` writes but not **whose** ring it reserves them in. It is the ring
of `FUN_0018B100`'s third argument — `[target+0x50 .. +0x58]`, cursor `+0x60`, pending range `+0x88`/`+0x90`.

### 19b. That argument is `&GameApplication[0xE8]`, a `Phyre::PRendering::PRendererBase` (FABLE)

Each step read from the image, not inferred:

| step | site | what it does |
|---|---|---|
| the address is taken | `0017D04F` | `lea rcx, [rbx + 0xE8]`, `rbx` = the application — the same body whose `0017D074` is *the only writer* of the `+0x113C` latch |
| handed to the creator | `0017D06F` | `call 00189000`, which allocates `0xDD8` into `[01F7F598]` |
| stored in the record | `00184F4C` | `mov [rcx+8], rdx` — the second argument, already recorded as *“`[+8]`/`[+0x10]` take `rdx`/`r8`”* |
| read back | `00187CFF` | `mov r8, [r14+8]`, `r14` = that record |
| passed to the walker | `00187D05` | `FUN_0018B100(list, whole, r8)` |
| handed to the command | `0018B181`–`0018B187` | `mov rdx, r14` then `call [rec_vtable+8]` |

And the subobject's type is stated where its base vtable is installed:

```asm
0079334F  lea rcx, [rsi + 0xE8] ;           call 005DDBA0                   ; base vtable
FUN_005DDBA0:  lea rax, [rip -> 00D498F0] ; mov [rcx], rax ; ret
```

`00D498F0`'s locator `01D091C0` reads `.?AVPRendererBase@PRendering@Phyre@@`, and
[the vtable method index](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) already attributes that
table's slot 0, `005E2C40`, to `PRendering::PRendererBase`. The application object itself is the **static**
`01F7E350` (`0015BC4D`), class `GameApplication` (vtable `008C5760`, 31 slots, `0017D090` at slot 8) over
`Phyre::PFramework::PApplication` (`01CB2508`).

### 19c. So “device” has been naming two objects one hop apart (FABLE)

`00D498F0` runs **three** entries before the next class's locator at `00D49908`; the index carries one row for the
class, slot 0. The `Gi*` bodies call their second argument's table at `+0x138`. **The walker's third argument is
therefore not the table the commands call** — it is the container, and `+0x18C0` of it is the device (§12d, §13b).
Both have been written here as *the device*.

Re-measured from the bodies rather than taken from §2, tracking only calls through the **argument** register
(`mov <r>,[<arg>]` then `call [<r>+d]`), over ten execute slots:

```
+0x000 +0x008 +0x020 +0x030 +0x040 +0x048 +0x058 +0x078 +0x080 +0x088 +0x098 +0x0A0 +0x0A8 +0x128 +0x138
```

— a subset of §2's twenty, the five absent ones belonging to bodies outside this batch; highest `+0x138`, so the
device's table holds **at least 40 slots**. The two shape-C resets reach **zero** offsets, reproducing §16's
withdrawal independently.

### 19d. BG-2 — the device's vtable is not an anonymous array (FABLE)

Every run of consecutive `.text` qwords in `.rdata`: **34,502**, of which **32,216** have no complete-object
locator in front of them. Of those locator-less runs **exactly one** reaches 40 entries — `008C31D8`, 1,172
entries, and **no function in the image takes its address**. §12d's *“an interior subobject never gets a type
descriptor”* is right about the **subobject**, but its **vtable** is still a locator-bearing table: the only way to
reach `+0x138` in this image is one of the sixteen. That leaves §13b's `00D86960` (`PrimitiveRendererD3D11`, 45
slots, installed at `+0x18C0` by `006C8761`) as the sole candidate that both reaches `+0x138` and is installed
where §12d traced. **BG-2 resolves to 45 slots if and only if BG-11 closes on that container — not asserted here.**

### 19e. What BG-11 still needs, with the constraint 19a adds (FABLE)

`FUN_005FEA50` writes `mov dword ptr [rcx], 0x2F` at `005FEAEE` — the **low dword only** — while `FUN_001F4A10`
reads the whole qword `[block]` (`001F4A19`). So the `0x2F` handler must still supply the context. 19a narrows
what it can supply: **the ring belongs to the walker's device**, so if the handler hands the callback its ring's
owner, `[ctx]` is `&GameApplication[0xE8]` and the device is `GameApplication + 0xE8 + 0x18C0`.
**Offered as a prediction with its test, not as a finding** — the test is the handler, still unlocated.

`FUN_001F3A50` is a **second** callback of the same block shape and is worth reading next: same `rbx = rcx`,
`rcx = [rcx]`, `call 00624660`, but it then makes a **device vtable call** of its own
(`001F3A67 mov r8,[rax]` … `movzx edx, byte [rbx+0x18]`). It has no caller in the edge index, so it is installed
the same way `001F4A10` is.

**Recorded as refused.** A peephole for *qword store to `[R+0]`, then a call through `[R+8]`* returned **0 sites**
image-wide. Its planted positive failed, so the zero is **not** offered as evidence of absence — the instrument was
not shown to be able to see the thing it was looking for.
### 19f. Why the executor was never found by searching the image (FABLE)

Three readings, each from the bodies, that together say where BG-11's executor is **not**.

**The producer flushes through the target's own vtable, and that pins the target's class a second
way.** `FUN_005FEA50` begins by testing the ring and, if it must drain first, calls **slot 2 of the
target itself**:

```asm
005FEA8F  mov rax, [rbx]            ; rbx = the target = FUN_0018B100's third argument
005FEA92  mov rcx, rbx
005FEA95  call qword ptr [rax + 0x10]   ; slot 2
005FEA98  mov rax, [rbx + 0x60]     ; ring cursor      } the 0x80-byte bump allocation
005FEA9C  mov r8,  [rbx + 0x58]     ; ring end         } wrapping to [rbx+0x50]
```

Slot 2 of `00D498F0` is `00600D20`, and `00600D20` is exactly the routine that reads `[target+0x88]`
and `[target+0x90]` — the two fields `FUN_005FEA50` itself publishes. **The producer's drain is the
target class's own virtual method**, which is independent confirmation of §19b: the ring's owner is a
`PRendererBase`-family object. The family's three tables differ in exactly the way a class hierarchy
should:

| vtable | class | slot 0 | slot 1 | slot 2 |
|---|---|---|---|---|
| `00D498F0` | `PRendering::PRendererBase` | `005E2C40` | `006105A0` | `00600D20` |
| `00D49910` | `PRendering::PRendererForJobs` | `005E2C90` | `006105A0` | `00600E30` |
| `00D49930` | `PRendering::PRenderer` | `005E2BC0` | `006104E0` | `00600D20` |

**The hand-off does not carry the container.** `FUN_00600D20` writes a three-field entry into the
`0x28`-stride ring at `02CE4720`, wrapping at 256, then signals a per-slot semaphore:

```asm
00600D46  rsi = [target + 0x88]                   ; start
00600D4D  rbp = [target + 0x90]                   ; end
00600DB5  rbx = [target + 0x78]                   ; the completion event
00600DCF  [02CE4720 + i*0x28 + 0x30] = rsi        ; +0x00  start
00600DD4  [02CE4720 + i*0x28 + 0x38] = rbp        ; +0x08  end
00600DD9  [02CE4720 + i*0x28 + 0x50] = rbx        ; +0x20  event
00600DE3  i = (i + 1 == 0x100) ? 0 : i + 1
00600DF9  005CD5E0(&entry + 0x40)                 ; signal
00600E01  0060FA10(target)                        ; reset the ring
```

**`target` itself is never written into the entry.** So the executor cannot recover the container
from the queue, and whatever it stores over `block+0` it must already be holding. That is a real
constraint on BG-11's answer, and it is consistent with — not evidence for — the §19e prediction.

**And nothing that reads the queue is a consumer.** `02CE4720` has **six** rip-relative references in
the whole image: `005FD127`/`005FD154` (the magic-static getter `FUN_005FD0E0`, `gs:[0x58]` guard,
`00808B90` atexit), `00600D6C` and `00600EA5` (the two flushes), and `008ADDF4`/`008ADE8B` (the
teardown, which calls `00610420` and then walks the slots). And all five of the getter's callers sit on the
producing side: `00600C20` (the same reserve shape as `FUN_005FEA50`, and it pumps the Win32
message queue through the registered `[02CB6348]`/`[02CB6340]` pair — `FUN_007989B0`, a
`PeekMessage`/`WM_QUIT` loop — while it waits for a free slot), `00610330` → `FUN_00610210` (the other
`0x2F` producer §12e names), `006104E0` (ring reset), `0079F150` (**creation** — `00607D20(queue)`
at `0079F54E`, its status logged on failure) and `0079EDD0` (**teardown** — `00610420(queue)` at
`0079EFB9`, the same call the atexit body makes, then `[app+0xE8]`'s own slot 1 at `0079EFC8`).
**All five are create, produce, flush or destroy. None consumes.**

> **Nothing that reaches the queue statically consumes it.** Six rip-relative references image-wide,
> five getter callers, and every one of them creates, produces into, flushes or destroys the queue.
> Together with an entry layout that does not carry the container, that puts BG-11's executor across
> the semaphore, on the consuming thread, holding whatever it was handed at thread creation — which
> is why §12e's image-wide searches over dispatcher shapes and handler tables could not have found
> it. **The next search is the thread, not the dispatch**: the body that waits on
> `02CE4720 + i*0x28 + 0x40`, and what its thread is given.

## 20. BG-11 answered — the executor, the context, and the device named (2026-09-22, FABLE)

§13b set the condition exactly: *“it becomes an identification when `[ctx]` at `FUN_001F4A10` is
tied to a container whose `+0x18C0` is that subobject”*. This section does that, and the answer
arrives with the one thing four passes had missed — **the consumer thread**.

### 20a. The consumer is created by the queue itself (FABLE)

`FUN_00607D20`, the body that builds the `02CE4720` block queue, **creates the thread that drains
it**, which is why no static reference to the queue ever led to a consumer:

```asm
00607D3C  edi = 0x100
00607D57  005CD160(queue+0x2840, 0x100, 0x100)   ; CreateSemaphoreA - 256 slots
00607D7A  005CD160(queue+0x2850, 1, 1)           ; CreateSemaphoreA - the one 00600C20 waits on
00607D90  loop x256: 005CD0E0(rbx, 0) ; [rbx+8]=1 ; rbx += 0x28   ; CreateEventA per slot
00607DA8  lea rdx, [rip -> 005FE1F0]             ; THE THREAD PROC
00607DD5  [rsp+0x28] = 0x10000                   ; 64 KB stack
00607DEF  005CD1E0(rcx = queue, rdx = descriptor); CreateThread, parameter = the queue
```

`FUN_005FE1F0` is a five-byte `jmp FUN_006106A0`. So the record layout of §19f is now readable in
full: record `R(i)` = `queue + 0x30 + 0x28*i`, with **`+0x00` start, `+0x08` end, `+0x10` the
per-slot event created above, `+0x20` the completion object `[target+0x78]`**. *(This corrects
§19f, which labelled `+0x20` “the event” and wrote the signal target as `&entry + 0x40`; the event
is `R(i)+0x10`, and `queue + 0x40 + 0x28i` is that field's absolute address.)*

### 20b. The drain loop (FABLE)

```asm
FUN_006106A0(queue):
  00610700  edx = [queue+0x2830]            ; the READ cursor (the write cursor is the global 02CE6F54)
  00610712  rbx = queue + 0x28*i
  00610724  005CD840(rbx+0x40)              ; WaitForSingleObject on R(i)+0x10
  0061073F  005CD500(rbx+0x40)              ; ResetEvent
  00610748  r8  = [rbx+0x38]                ; end
  0061074F  rdx = [rbx+0x30]                ; start
  00610753  0060A410(queue, start, end)     ; THE BLOCK EXECUTOR
  00610774  005CD650([rbx+0x50], 1, 0)      ; ReleaseSemaphore - completion
```

### 20c. The block is never handed to the callback — §12e's premise was wrong (FABLE)

§12e reasoned that *“something between the producer and the callback writes the context over
`block+0`”*, because `FUN_005FEA50` leaves the opcode dword there. **Nothing does.** `FUN_0060A410`
walks the range in `0x80` steps (`0060A9D9 sub rsi, -0x80`) and reads `block+0` **as the opcode**:

```asm
0060A5B3  lea rbx, [rsi + 0x70]        ; rsi = the block; the +0x70 bias keeps 8-bit displacements
0060A5C0  mov ecx, dword ptr [rsi]     ; the opcode, still 0x2F
0060A5C4  cmp ecx, 0x2E                ; after dec: a 47-case switch, two-level table at 0060AAD8/0060AAB8
```

The table has **eight arms over 47 opcodes** — `0x01`…`0x06` and `0x2F` are real; **`0x07`–`0x2E`
all fall to the default `0060A9C6`**. The `0x2F` arm **synthesises a three-qword frame on its own
stack** and passes *that*:

```asm
0060A899 (opcode 0x2F):
  0060A8BD  [rbp-0x50] = r14              ; field 0  <- THE CONTEXT
  0060A8C1  [rbp-0x48] = &[rsp+0x50]      ; field 8
  0060A8CA  rax = [rbx-0x60]  (= block+0x10)
  0060A8CE  [rbp-0x40] = rax              ; field 0x10 <- the Gi command
  0060A8D2  rcx = &[rbp-0x50]
  0060A8D6  call [rbx-0x68]   (= block+0x08)   ; the callback
```

which is exactly what `FUN_001F4A10` reads — `[rcx]` is field 0 and `[rbx+0x10]` is field `0x10`.
**`FUN_001F4A10` never sees the block**, so `block+0` never needed overwriting. The four passes
searching for a writer of `block+0` were looking for something that does not exist.

### 20d. `[ctx]`, and therefore the device (FABLE)

`r14` is set once, at `0060A46F`, from `0060A46A call 00624670` — and `FUN_00624670` is
`jmp FUN_005FD050`, a magic-static getter:

```asm
FUN_005FD050:  ... _Init_thread_header guard ...
  005FD097  lea rbx, [rip -> 02CC0410]
  005FD0A1  call 00615840(rbx)        ; the one-time constructor
  005FD0BF  rax = rbx                 ; both exits return 02CC0410
```

and `FUN_00615840` is the body §13b traced:

```asm
00615860  mov rbp, rcx                   ; rbp IS this, restored only at 00615BA9
00615B50  lea rcx, [rbp + 0x18C0]
00615B57  call 006C8750                  ; 006C8761 [rcx]   = 00D86960   (primary)
                                         ; 006C877B [rcx+8] = 00D86AD0   (secondary)
```

> **BG-11 is answered.** `[ctx]` is the magic-static singleton **`02CC0410`**, and the device is
> **`02CC1CD0` = `02CC0410 + 0x18C0`**. The container whose `+0x18C0` §12d traced and the `[ctx]`
> `FUN_001F4A10` reads are **the same object**, because `FUN_005FD050` both returns it and is the
> only caller of the constructor that builds that subobject.

### 20e. BG-2 answered, and BG-1 corrected (FABLE)

`00D86960` carries the locator `01D380D0` = `.?AVPrimitiveRendererD3D11@@`, offset 0, and runs
**exactly 45 slots** — slot 44 at `+0x160` is `006CB540`, and `+0x168` is the locator `01D38180`
for the same class's **secondary** table `00D86AD0` (offset 8, one slot, `006C88A0`).

> **BG-2: the device vtable holds 45 slots.** The highest the `Gi*` family calls is slot 39
> (`+0x138`), so nine slots are never touched by this family.

And the twenty offsets §2 recovered *by use* all land in that class's method range — which is a test
this identification could have failed and did not:

```
+0x000 006CA760   +0x048 006CAE90   +0x0A0 006CABF0   +0x128 006C9B00
+0x008 006CB5E0   +0x058 006CAD90   +0x0A8 006CAC00   +0x130 006CA7B0
+0x020 006C8C50   +0x078 006CAB80   +0x0B0 006CABE0   +0x138 006C9AF0
+0x030 006CAF40   +0x080 0060D760   +0x0D0 006CAC40
+0x038 006CAD30   +0x088 0060D760   +0x0D8 006CAC20
+0x040 006CAEB0   +0x098 006CAB40
```

§13b's three independent spot checks all match: slot 0 is `006CA760`, the reserve body it quoted;
`+0x130` is `006CA7B0` and `+0x128` is `006C9B00`, its scene bracket; `+0x80` is `0060D760`, its
`mov eax, 0x17 ; ret`.

> **BG-1 must be restated.** Its verdict reads *“it is not an RTTI-bearing class at all”*. **The
> device's class is `PrimitiveRendererD3D11`, which is RTTI-bearing.** What is true, and what the
> 16-class scan actually showed, is that **the interior subobject carries no locator of its own** —
> an embedded member's vtable is installed by its container's constructor, so nothing emits a
> descriptor *for the member*. §12d already said this and §14 already recorded the verdict as *“not
> established at the strength stated”*; this section supplies the positive identification that
> settles it.

### 20f. A prediction of mine, refuted (FABLE)

§19e predicted that *“if the handler hands the callback its ring's owner, `[ctx]` is
`&GameApplication[0xE8]`”*. **It does not, and it is not.** The handler passes `r14`, which comes
from an unrelated magic-static singleton `02CC0410`; the ring's owner reaches the executor only as
the `queue` argument of `FUN_0060A410`, and the `0x2F` arm never touches it. The prediction was
stated with its test, and the test refuted it. **The reasoning that produced it — “the ring belongs
to the walker's device, so the device is probably reachable from the ring” — is the error worth
keeping: a value that travels beside another value is not derived from it.** §19a's reading itself
stands; only the inference drawn from it was wrong.

## 21. The block opcode vocabulary, both dispatch levels (2026-09-22, FABLE)

§20c reported that `FUN_0060A410` switches 47 ways with **eight arms**, `0x07`–`0x2E` falling to a
default. **That default is not a discard** — it is a second dispatcher, and this section completes
the vocabulary. Full table:
[`members/render-block-opcode-isa.tsv`](members/render-block-opcode-isa.tsv).

```asm
0060A9C6 (level 1 default):  00607410(queue, context, block, &local)

FUN_00607410:
  00607422  mov   eax, [r8]                 ; the same opcode dword
  00607428  add   eax, -7
  00607434  cmp   eax, 0x27                 ; opcodes 0x07..0x2E
  00607446  mov   r10d, [rcx + rax*4 + 0x4E78E4]   ; rva table at 006078E4, rcx = image base
  00607451  jmp   r10
```

**40 opcodes, 40 distinct arms** — every one has its own handler; nothing shares. Each arm reads its
payload from `block+0x08` upward and calls one state setter. Widths vary: `0x0A`–`0x0D` take a single
dword, `0x09` four floats, `0x1C` five, and `0x2A` reads thirteen fields from `+0x08` to `+0x40`.

### 21a. Two streams reuse this block shape, and opcode numbers are not global (FABLE)

**Recorded because it cost this pass a wrong answer.** A first sweep for `mov dword [reg], imm` block
headers attributed 33 opcodes to this vocabulary, including a `0x2E` emitter at `007A46F0`. That body
reserves through `FUN_007AB460`, **the sound engine's ring**, whose own dispatcher §12e already
identified as `FUN_007AB5C0`. The `{u32 opcode, payload}` block shape is shared; the **numbering is
per stream**. An emitter may only be attributed to this ISA by the ring it carves from, never by the
constant it writes.

### 21b. The producer census was bounded by an address range, not by the shape (FABLE)

§12e records *“eight bodies between `FUN_005FEA50` and `FUN_00600A60` share this exact reserve
shape”*. Sweeping for the shape itself — a body that reads the ring triple `[ctx+0x50]`, `[ctx+0x58]`,
`[ctx+0x60]`, forms `lea rdx,[rax+0x80]`, and writes an opcode header — finds **seventeen**, with the
controls that `FUN_005FEA50` is detected, the header-less `FUN_00600C20` is detected as a reserve
helper rather than a producer, and the sound-side `FUN_007A46F0` is not detected at all:

| opcode | producer | | opcode | producer |
|---|---|---|---|---|
| `0x01` | `0060C020` | | `0x18` | `00600A60` |
| `0x02` | `0060C020` | | `0x1B` | `0060CD70` |
| `0x03` | `006007B0` | | `0x21` | `0060DA50` |
| `0x07` | `0060F6B0` | | `0x25` | `0060E810` |
| `0x08` | `0060EB60` | | `0x26` | `0060D3D0` |
| `0x0D` | `0060D320` | | `0x2D` | `00609AC0` |
| `0x10` | `00600070` | | `0x2F` | `005FEA50`, `005FEB30` |
| `0x13` | `005FFF00` | | `0x16` | `005FEFD0` |
| `0x17` | `005FFE40` | | | |

§12e's eight are all here; the other nine sit at `00609AC0`–`0060F6B0`, **past the upper bound its
sentence names**. The original set was right about every body it listed and wrong only about being
complete — *“between X and Y”* is a range, and the shape does not stop at `Y`. Seventeen is itself a
floor: a producer that writes its opcode some other way would not be seen.

> **Corrected the same day, by the sweep that answered `GF-7`: it is nineteen, not seventeen.**
> The detector required the opcode store to be followed by a write to `+0x08`/`+0x0C` within
> **eight** instructions. `FUN_0060D4F0` and `FUN_0060DB50` put theirs further down — `0x0E` at
> `0060D6F6` and `0x0F` at `0060DD17` — and were missed. Widened to forty, the count is stable at
> **19 producers over 19 opcodes**, and the two additions are exactly the pair whose handlers sit
> beside them (`0x0E` → `0060D4A0`, `0x0F` → `0060DB10`). **The stated floor was doing real work
> here** — the number moved, the claim did not. §12e's eight remain a subset of the nineteen.

### 21c. Nine handlers are inert, and one of them is reached (FABLE)

Of the 40 level-2 handlers, **nine end in a body that does nothing**:

| handler | body | opcodes |
|---|---|---|
| `0060D760` | `mov eax, 0x17 ; ret` | `0x1D` `0x1E` `0x1F` `0x25` `0x27` `0x28` `0x29` `0x2B` |
| `005C5230` | `xor eax, eax ; ret` | `0x2E` |

The arms still decode their payload first. `0x1D` is the clearest case — it loads four floats from
`block+0x08`…`+0x14` into `xmm1`–`xmm3` and the stack, calls `0060D760`, and the four values are
discarded:

```asm
006075FE  movss xmm0, [r8 + 0x14] ; 0060760D movss xmm2, [r8 + 0xC]
00607607  movss xmm3, [r8 + 0x10] ; 00607613 movss xmm1, [r8 + 8]
0060761F  call  0060D760          ; mov eax, 0x17 ; ret
```

> **Eight of the nine are dead at both ends** — no producer in this stream emits `0x1D`, `0x1E`,
> `0x1F`, `0x27`, `0x28`, `0x29` or `0x2B`. **`0x25` is not.** `FUN_0060E810` emits it at `0060E8A8`,
> its arm `006076E9` decodes three fields from `+0x08`, `+0x0C` and `+0x10`, and hands them to
> `0060D760`. So exactly one live render command in this build is produced and discarded — and
> `FUN_001E2AF0`, the map render body of §"What `001E2AF0` builds" on the post-process page, is one
> of its callers, twice.

`0060D760` is the same body the device vtable carries at **`+0x80` and `+0x88`** (§13b), so `0x17` is
this family's *“not supported”* answer rather than a value: the same stub answers two device methods
and eight block opcodes.

*Not claimed:* that `0x25`'s three fields are unused elsewhere — only that this consumer discards
them.

> **Producers named 2026-09-26 (FABLE, Claude Opus 5.5): the command carries the authored shadow depth bias.**
> An image-wide raw call scan finds four calls to `FUN_0060E810`, two in each of two draw bodies. In both, a set
> precedes the draw and a clear follows it:
> - **`001E2AF0` (map).** Only on its `MapShadowRender` branch, `001E3091` passes flag 1 with `mMapShadowDepthBias`
>   (an int, converted at `001E307E`) and `mMapShadowSlopeOffset`. Both come from the map-art context's
>   `+0x43C`/`+0x440`, where the map-JSON loader stores them. `001E3CD1` then passes flag 0 and two zeros.
> - **The character draw body (character).** `001F5E9B` passes flag 1 with `mChrShadowDepthBias` and
>   `mChrShadowSlopeOffset` from `01F82F08`/`01F82EF4`, which both scene loaders store. `001F62CC` then passes flag 0
>   and two zeros.
>
> `+0x08` is the flag, `+0x0C` the bias and `+0x10` the slope. That is the shape of D3D11's
> `DepthBias`/`SlopeScaledDepthBias` pair, which the reflected rasterizer description carries. **So the shadow bias the
> scene JSON authors reaches this command, and this consumer drops it.** *Not claimed:* that no other route applies
> a depth bias to the shadow pass. And the level-1 arms `0x01`–`0x06` were read no further than their first call.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Input — MECHANICAL (SWE2-CONTRACT 2026-09-15, 8 edges).** `005C3A30` is called by `001E0A10`/`001E0D80` and
`00879750` is called by six `00873xxx`/`00874xxx` input bodies. Shared helper fan-in only.

**Platform — SERVICE (FABLE 2026-09-22, 3 edges, §19f).** `0079F150` calls `005CC930`, `005CD0A0`
and `006253D0`. Real and expected: `0079F150` is the body that **creates** the `02CE4720` block
queue (`00607D20` at `0079F54E`), and these are the platform synchronisation primitives it builds
the queue's per-slot semaphores from — the same family as the `005CD5E0` signal and `005CD8B0`
wait that §19f cites on the producing side. Cited here only to complete the census of who
references that queue; no render-layer relationship is claimed.

**ActorEntity — ARTEFACT OF AN `/OPT:ICF` FOLD (FABLE 2026-09-22, 4 edges, §21c).** Four ActorEntity
bodies appear to call `005C5230`. **Not a relationship of any kind**, and their addresses are
deliberately not repeated here, because citing them would import their own edge sets in turn.
`005C5230` is `xor eax, eax ; ret` — a two-byte body the linker folded, so every caller of *any*
function with that shape now appears to call this one. It is cited here only as the handler opcode
`0x2E` dispatches to, and the point being made about it is precisely that it does nothing. Its
caller set carries no information about this document's subject, and the same caution applies to
`0016D6A0` and `0060D760` wherever this page names them.

**Save_Load_Settings — SERVICE (SWE2-CONTRACT 2026-09-15, 3 edges, R5-visible).** Startup body
`0017D4C0` calls `SaveloadManager_EnsureSingleton` `001C18A0`,
`SaveloadManager_GetSingleton` `001C18E0` and `SaveloadManager_RefreshDisableAutosaveList`
`001C1710` — initialisation-time singleton wiring, not a render-layer relationship.

**Resource — shared validator leaves (SWE2-EC7 batch-147).** The batch-147 entries' per-lane
probes (`0061DBE0`, `0061DCA0`, `0061DD60`, `0061DE20`, `0061DFE0` - called from the GI record
notifiers `00629AA0`, `00629C70` and `006CA8D0`) are shared leaves that `00686DE0` of that
layer also calls - shared helper fan-in only, not render-layer resource ownership.

**Audio — MECHANICAL (SWE2-EC7 batch-149, 2 edges).** `0061ED00` and `006239C0`, callees the `006225D0` and `0062A0A0` entries cite, each call the Audio-filed `00225690` - two shared issue helpers reaching the same audio leaf; no render-audio relationship is claimed.
- **Application - CLIENT and SERVICE (2 edges).** `005CC930` is called by bodies filed to Application: `00799980`; `00186CD0` reaches bodies filed to Application: `001A98B0` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (43 edges).** `0017D4C0`, `00189000`, `0018A7D0`, `0018B4E0` (+11 more) are called by bodies filed to CoreRuntimeScheduling: `0017CCD0`, `0017D000`, `0017D4C0`, `0017D670` (+4 more); `0017D4C0`, `00187950`, `001D8240`, `001DB220` (+19 more) reach bodies filed to CoreRuntimeScheduling: `0017D270`, `001A1470`, `001A14E0`, `001DB500` (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (6 edges).** `001A1470`, `001E0A10`, `005FEA50`, `005FEFD0` (+1 more) are called by bodies filed to UI: `0018EEE0`, `00284EC0`, `0029B870` - shared machinery across the layer boundary, no shared ownership.

## Interior citation — frontier hub `0020E680` (2026-09-17, SWE2-EC7)

`0020E680` — 50 B, 35 frontier callers at census; the "arena-allocated 16-byte node" helper this
page already names `FUN_0020E680`. Interior verified: `rcx=[01F7F4C0]`, `edx=0x10`,
`call 001A1470` at [`0020E692`](../../_index/ADDRESS-INDEX.md) (the ring bump allocator), then
`rcx=[01F7F4C0]` again, `rdx=rax`, `call 0016D6A0` — the 16-byte arena record is handed to the
init stub (in this build a `ret 0` no-op) on the same `01F7F4C0` arena object before being
returned in `rax`. So the body is alloc-only; any initialisation the node needs happens at the
caller.

NOT claimed: what the `01F7F4C0` object is beyond the arena anchor the call shape implies.

## Interior citation — frontier hub `001FBD80` (2026-09-18, SWE2-EC7)

`001FBD80` — 157 B, 6 A-measured callers; `GiBeginScene` from the table above. Interior
verified: when `00182560()` reports idle and `ecx != 3`, `00182250()` runs and the
`01F83064` dword is armed (`001FBD9B`); `0016D6A0(1)` opens a scope, `001A1470(obj, 8)`
allocates an 8-byte slot whose `[0]` receives the `00904488` handler image pointer, the slot pointer
publishes to `01F83078`, and `001FB840` runs before `0020E630(&01F83070, ecx)` registers the
scene id at [`001FBDEB`](../../_index/ADDRESS-INDEX.md). `ecx != 3` additionally fires `0018CA40()` +
`0018BF00(…, 1)`. The mode dword lands at `01F83068`, the done flag at `01F83060`.


## Interior citation — frontier hub `0018AFF0` (2026-09-18, SWE2-EC7)

`0018AFF0` — 58 B, 40 callers (5 A-measured); the `push_back` behind `MapRenderObject`'s
event-pair entry and every other 8-byte-element command vector. Interior verified:
cursor `[rcx+8]` vs end `[rcx+0x10]` (`0018AFFC`–`0018B004`); on room it stores the arg and
advances 8 ([`0018B006`–`0018B013`](../../_index/ADDRESS-INDEX.md)); on full it delegates to
`001AB570` — the vector-insert grow measured last batch — at [`0018B020`](../../_index/ADDRESS-INDEX.md).
The grow path's `(cur, &arg)` stack repack is the only part callers can't see.


## Interior citation — frontier hub `0018A9E0` (2026-09-18, SWE2-EC7)

`0018A9E0` — 17 B, 16 callers; the `(edx + r8b*4)` table fetch in this family's callee
band. Interior verified: `movsxd rax, edx; lea rax, [rax + r8b*4]` computes the 4-way
sub-index ([`0018A9E4`–`0018A9E7`](../../_index/ADDRESS-INDEX.md)) and
`[rcx + rax*8 + 0x40]` returns the qword slot at [`0018A9EB`](../../_index/ADDRESS-INDEX.md) —
a `+0x40`-based pointer table with a nibble-of-nibble selector.


### Interior citation — frontier hubs `0020E630`, `001FB840` (2026-09-18, SWE2-EC7)

`0020E630` — 63 B, 31 callers: the mode-to-sub-index selector the `record+0x18`
walks above feed. `edx` 0/1/2 map to `edx+8`/`+0x1F`/`+0x3E`; `edx == 3` selects
`0x20`, anything else 0 — then tail `001FB810(node, subindex)`
([`0020E63C`](../../_index/ADDRESS-INDEX.md)). The dispatch the §-flows name.

`001FB840` — 43 B, 16 callers: the §12b body, read in full — `rcx` is reloaded
from a global, `0016D6A0` runs (the ret-0 guard), then `rax = [node+8]` is both
stored back to `[node]` and dereferenced for `jmp qword[rax]`
([`001FB868`](../../_index/ADDRESS-INDEX.md)) — a vtable slot-0 dispatch on the
node's first member.

### Interior citation — frontier hub `005FEA50` (2026-09-18, SWE2-EC7)

`005FEA50` — 209 B, 10 callers: the enqueue §663 names, read in full. Null
`rdx` returns 1. The `00600B30` ring-gate predicate runs first at
[`005FEA86`](../../_index/ADDRESS-INDEX.md) — on refusal it calls the object's
vtable slot `+0x10`; otherwise it commits the ring cursor: `[rbx+0x60]+0x80`
clamped against the `[rbx+0x58]` bound (wrapping to `[rbx+0x50]+0x80` on
overflow), the new cursor stored to `[rbx+0x60]`, and the `[rbx+0x88]` gate
checked before the hand-off. The bounded-slot ring commit behind the
command-list feed.

## SWE2-EC7-28 update (2026-09-18) — `001B22F0` slot-dedup write

`001B22F0` (235 B) is the `001Bxxxx` command-table family's bounded
linear-probe writer: indexes the 64-entry `0x58`-stride table at
`[rcx+0x2328]` by `[rcx+0x3928]`; a free slot (`+0x28 == 0`) takes
`ebx`/`r8d`/`esi`/`r9d`/`ebp`/`edi` into `+0x10..+0x28` marked
`+0x28 = 1`; an occupied slot whose `+0x10`/`+0x14`/`+0x20`/`+0x24`/
`+0x1C` key already matches returns unchanged; otherwise `+0x3928`
advances (`<= 0x3F`), the new slot is zeroed, filled, and its `+0x38`
link mirrors to `+0x40`. Interior anchor `001B2337` (the free-slot
test).
## SWE2-EC7-32 update (2026-09-18) — `001FB810` `01F7F4D0` forward

`001FB810` (18 B) is the two-load forward the command family posts:
`rdx = [rcx]` (the caller's object), `rcx = [01F7F4D0]` (the
command-context singleton), `r8d = edx` — then a tail
`jmp 001A17F0` runs the operation on the context. Interior anchor
`001FB81D` (the `jmp 001A17F0` tail).

## SWE2-EC7-32 update (2026-09-18) — `001E0A10` paired getter

`001E0A10` (42 B) is the getter pair the screens share:
`00198790()` resolves the target object twice — once for
`ebx = 005C3A30(obj)`, once for `001986D0(obj)` — and returns
`ebx`: two reads on the same singleton, the second for its
side effect. Interior anchor `001E0A2D` (the `call 001986D0`).

## SWE2-EC7-34 update (2026-09-19) - `001D76A0`

`001D76A0` (885 B) is a render-record slot walker - 11 `001B1C00` calls plus `001B1620`/`00189120`/`001FBE50`/`001FBE30`/`001FBD80` in a cookie-framed 0x1A0 stack. Interior anchor `001D7705` (an `001D8240` call).

## SWE2-EC7-35 update (2026-09-19) - `0020E6C0`

`0020E6C0` (811 B) is the third sibling beside the `0020E600`/`0020E620` image-pointer pair - the `008C5F80`-`008C5FD0` rdata run, `001EE650`/`0018AA10`/`0016D6A0`/`00808C40`. Interior anchor `0020E6F6` (an `00808C40` call).

## SWE2-EC7-36 update (2026-09-19) - `00188730`

`00188730` (651 B) is a gi-render CRT-formatter body - `0060D4F0`/`005DC190` septuples, `0016D6A0` quintuple plus `0060F6B0`/`0060DB50`/`0060D6B0`. Interior anchor `00188761` (a `0060D4F0` call).

## SWE2-EC7-37 update (2026-09-19) - `00213FE0`

`00213FE0` (547 B) is a gi-render command body - `01F44830`/`008C5FD0`/`008C5FB0`/`008C5F90`, `00189120` pair plus `001EE7C0`/`001EE650`/`00186A90`/`00186AA0`/`00808C40`. Interior anchor `00214055` (an `001EE7C0` call).

## SWE2-EC7-43 update (2026-09-19) - `006CA7B0`

`006CA7B0` (276 B) is the `PrimitiveRendererD3D11` slot-38 body - `01F2DEC0`/`01F2DEC8`/`02CEE3D0`/`02CEF210`/`02CEF250` import calls, `00618740`/`0061E6B0`. Interior anchor `006CA7F2` (a `00618740` call).

## SWE2-EC7-44 update (2026-09-19) - `008651A0`

`008651A0` (271 B) is the `GiNormal` row body - `0016D6A0`/`001EE650`/`00210510`/`00210560`/`00808C40` plus `call [r10+0x78]`/`[rax+0x98]`/`[rax+0x80]`/`[rax+0x88]` vcalls. Interior anchor `008651C0` (an `0016D6A0` call).

## SWE2-EC7-44 update (2026-09-19) - `00862D40`

`00862D40` (269 B) is the `GiTrans` slot-1 row body - `0016D6A0`/`001EE650`/`00210510`/`00210560`/`00808C40` plus `call [rax+0x88]`/`[rax+0xA8]`/`[rax+0xA0]`/`[r10+0x78]` vcalls. Interior anchor `00862D60` (an `0016D6A0` call).

## SWE2-EC7-44 update (2026-09-19) - `00862EC0`

`00862EC0` (267 B) is the `GiTransNz` row body - `0016D6A0`/`001EE650`/`00210510`/`00210560`/`00808C40` plus `call [rax+0x88]`/`[rax+0xA8]`/`[rax+0xA0]`/`[r10+0x78]` vcalls. Interior anchor `00862EE0` (an `0016D6A0` call).

## SWE2-EC7-44 update (2026-09-19) - `001DB220`

`001DB220` (273 B) is a sound-request body - `0016D6A0`/`001A1470`/`00861EC0`. Interior anchor `001DB255` (an `0016D6A0` call).

## SWE2-EC7-57 update (2026-09-19) - `0061E6B0`

`0061E6B0` (175 B) is a gi-render body - `00861EC0` single call plus one vcall. Interior anchor `0061E729` (a `00861EC0` call).

## SWE2-EC7-61 update (2026-09-19) - `008647C0`

`008647C0` (153 B) is the `GiSprite` row body - `0016D6A0`/`001A1470`/`002105C0`/`0024D140` plus `01CCFB08`/`01F7F4C0`. Interior anchor `008647D7` (a `0016D6A0` call).

## SWE2-EC7-62 update (2026-09-19) - `0024D140`

`0024D140` (453 B) is a Gi-render body - `0017FE10`/`003B0940`/`003B33D0`/`00862C40` plus `008F3134`/`01E0C290`/`02092710`/`02F97340`. Interior anchor `0024D155` (a `00862C40` call).



## SWE2-EC7-63 update (2026-09-19) - `00863060`

`00863060` (146 B) is the `GiSetTexture` row body - `0016D6A0`/`001A1470`/`001FB840` plus `01CCFA30`/`01F7F4C0`/`02EAF918`/`02EAF920`. Interior anchor `00863084` (a `0016D6A0` call).

`001E5C40` (1021 B) is the per-record emit `001A53F0` calls once the object validates: gated on `byte[rcx+0x250]`, it walks the `[rcx+0x18]..[+0x20]` pointer span, and for each `r12` whose `[r12+0x20]` header count (`& 0x7FFFFFFF`) is nonzero it loops the embedded elements - `001C0DA0` resolves each slot, up to eight `00861EBA` copies move the payload fields, `001E6040` runs on the staged block, and the element kind selects `0018A9E0` with `edx` 0-3; the `0x47`-tagged out-record takes `[rdi+0x1A8]`'s `+0x10`/`+0x12` words masked `0x1FFF` - the batch that turns one live object into its command stream.

Interior anchor `001E5D14` (function `001E5C40`).

`005CD650` (121 B) is the driver-object query pair: IAT `008C20D8` queries `[rcx]`; on failure `008C20A8` fetches the error, `008C2208` opens the object (flags `0x1300`, `0x400`-byte buffer at `rsp+0x68`), `008C21F8` closes it, and the body returns 0 on the query path or 9 on the open-fail path - the device-capability probe the GI callers share.

Interior anchor `005CD6A9` (function `005CD650`).

`00602760` (724 B) is the GI command-list executor: over each 0x80-stride entry of the `[r9, end)` range with tag 1 or 2 it resolves the `[+0x50]`-indexed sub-object through `[rdi+0x28]`, counts candidates via `00670E00`, scans the 0x88-stride record array for a usable slot, and submits through the entry's vtable `+0x10`; a 0xD result code drops into `005CDAA0` against the `00D4A6F0` table, survivors append to the 0x20-capacity out-list at `r13+0x210`, and leftovers are destroyed by `00662EA0` and freed by `00584730` before the write cursor lands in `r13+8`.

Interior anchor `006028D8` (function `00602760`).

`0061EE30` (576 B) is the device request pair submitter: it rejects a null `rdx`, clears the flag bit of the `[rcx+0x1A0]` count and picks the first entry of the inline-or-table list at `+0x1A8`; that entry is queried through its vtable `+0x50` into a stack property block, then two requests issue on `[rdi+0x108]`'s vtable `+0x28` (kinds 1 and 3, the second carrying flag 0x20000) and a third on `[rdi+0x110]` with size 0x1C - every stage fail-closed on a null handle or negative result.

Interior anchor `0061EEC0` (function `0061EE30`).

`00622BA0` (482 B) is the per-slot command validate-and-issue `00607410` runs: `edx` bit 2 widens the pass count to 2 while `edx & 1` picks the start slot, iterating the `rdi + (r15+0x3A)*24` table; slots whose `+0x18`/`+0x28` fields are both empty are probed by `00620F60` (nonzero aborts the pass with 0), armed slots (`+0xC` bit 1, `+9` byte set, `+8` byte 0) resolve `[rbx]` through `00624270` and - on the `ebp != 1` arm - submit the `00624090`-computed request through `[rdi+0x110]`'s `+0x1C8` vcall, while the sibling arm re-verifies `[rbx+8]` against a nonzero object and vcalls `+0x1B0`; when `[rdi+0xE1]` and the `[rdi+0x630]` record's `+9` byte allow it and `edx` bit 1 is clear the pass closes with `006CA8D0(rdi+0x18C0)`, returning 1 on success.

Interior anchor `00622CB8` (function `00622BA0`).

`00608F20` (390 B) is the ping-pong command-buffer publish `0060A410` feeds: `02CB7FC8` toggles between the two `0x70`-stride slots at `02CBC590`, the fresh slot records `rdx` at `+0x28`, the four-qword block `r8[0..0x1F]` at `+0x38..+0x50`, and `r9` at `+0x20`; when the previous entry `[r14]`'s `+0x28` matches the new `+0x28` a `rol`/`cmove` chain diffs the two 4-qword blocks into a changed-lane mask `r15`, `0060B860` then merges the slot pair, `005C5230`/`00627140` and `00629AA0`/`00629C70` run the record's own passes, and `0060EC80`/`00623180` submit with the mask before `[r14]` receives the slot pointer.

Interior anchor `00608FF9` (function `00608F20`).

`00629C70` (54 B) is the slot rebind the GI publish path `00608F20` and the command runner `00607410` apply to a record's `+0x30` node: `0061DE20` probes the node with key -1, and only on a zero result does `0061D260` install the supplied pointer - an install-if-vacant that leaves an existing binding untouched.

Interior anchor `00629C8E` (function `00629C70`).

`006CA8D0` (613 B) is the validate-and-issue the GI command `00622BA0` runs on its `[rsi+0x848]` render object: it takes the command record's `+8`-gated pointer, builds a stack request block from the record's `+0x28`/`+0x2C` dimensions (converted to float, plus 1.0f and 0 lanes), calls vtable `+0x160`, pushes the `[rsi+0x6B8]` lane key through `0061D180` and issues vtable `+0x108` with the record's `+0x18` payload; it then republishes the `00618740`-filtered object set - `01F2DF08`, `01F2DEC8`, `01F2DE98`, `01F2DEB8`, `01F2DEA8` each storing the record's `+0x178..+0x188` member or clearing to 0 and firing the paired `.data` callback only when the slot changes - republishes the `[rdi+0x30]`-indexed `+0x38`/`+0x18` child through `02CEE3F8`/`02CEE7D0` the same way, appends the `[rsi+0x98]`-rooted block through `0061C8A0`, stamps `01F2DEF8` = 5 with its callback, and closes with vtable `+0x68(4)` on the render object.

Interior anchor `006CAA08` (function `006CA8D0`).

`00629AA0` (463 B) is the four-slot state notifier the GI sync `00608DD0` runs on a record pair: the source's four members are mirrored into the output's `+0x30`/`+0x38`/`+0x40`/`+0x48` (with the source itself at `+0x28`), then each lane - `rsi`, `rdi`, `rbp`, `r14` - that is non-null is validated by its own probe (`0061DFE0`, `0061DD60`, `0061DCA0`, `0061DBE0`); a null lane writes 0 into the matching publish slot `01F2DE98`/`01F2DEB8`/`01F2DEA8`/`01F2DEC8`, a live lane writes the member's `+0x90`/`+0x78` handle, and in both cases the paired `.data` callback fires only when the slot value changed. A nonzero validator return aborts the remaining lanes.

Interior anchor `00629B90` (function `00629AA0`).

`005FDEA0` (356 B) is the GI issue sibling of `005FE010` dispatched through vtable slot `+0x18`: after the `00608DD0` sync it unpacks the command's `[r8+0x30]`, `[r8+0x60]`, `[r8+0x6A]` and `[[r8+0x28]+0x18]` fields; when the target object `[rdi+8]` exists it resolves the `+0x68` id through `00670E00`, sets bit 31 of a stack flag and issues the object's vtable `+0x18` with the assembled block, then - if the flag's high bit came back clear - sweeps `[rdi+0x10]`'s `0x88`-stride array `edx` times through `00662EA0` and frees it via `00584730`. With no target object it dispatches on the remaining fields: `00621F80` with the `[rdi+0x6C]`-derived bank index rounded up, `006224E0` when `rbp` is set, or `00622350` as the final arm.

Interior anchor `005FDF5E` (function `005FDEA0`).

`0061EA80` (338 B) is the GI commit gate `00607410` runs on the frame state: only while the four counters are quiescent (`[rcx+0x1864] == [rcx+0x186C]`, `[+0x1868] == [+0x1870]`, `[+0x185C] == 0`, `[+0x1860] == 0`) does it apply the pending op inline - arg2 bit 0 sweeps the `[rbx+0x648]`-based pointer array `[rbx+0x6D0]` times through vtable `+0x190` on `[rbx+0x110]`, and arg2 bits 1|3 with `[rbx+0x688]` present fire vtable `+0x1A8` carrying `[rbx+0x7D0]`/`[rbx+0x7D4]` and mode bits folded from arg2 - otherwise it defers through `0061E760` with the `[rbx+0x7C0]` state copy, the `[rbx+0x6D0]` count and the `rbx+0xB50` context, returning 1 on the direct arm and the deferred call's result otherwise.

Interior anchor `0061EB31` (function `0061EA80`).

`005FE010` (330 B) is the vtable `+0x20` issue sibling of `005FDEA0`: the same `00608DD0` sync first, the same `[r8+0x30]`/`+0x60`/`+0x6A` field plumbing plus the `+0x70` dword, the same `00670E00` id resolve on the target's `+0x68` word with the bit-31 stack flag, then the target object's vtable `+0x20` call and the same `00662EA0`/`00584730` `0x88`-stride sweep when the flag clears; the no-target arm dispatches `006226D0` (passing `rsi`) or `00622450` on the `[rdi+0x6C]` and `+0x70` fields.

Interior anchor `005FE0C6` (function `005FE010`).

`00608DD0` (324 B) is the GI slot-sync coordinator the issue paths (`005FDEA0`, `005FE010`, `0060A410`) call before their vtable slot fires: when the slot record `[rcx]` is absent it copies the command's `+0x20`/`+0x28`/`+0x30` into `+0x18`/`+0x20`/`+0x28`; otherwise it diffs the old record's `+0x38`/`+0x40`/`+0x48`/`+0x50` against the command's fields into a 4-bit changed-lane mask, applies it via `0060B860`, and when the records differ releases the old one through `005C5230` + `00627140` before the same copy. Both arms then notify the four-slot publish set through `00629AA0`, rebind the `+0x30` node via `00629C70`, validate the changed lanes through `0060EC80`, hand off to `00623180`, and repoint `[rbx]` to the command record.

Interior anchor `00608E71` (function `00608DD0`).

`0060EC80` (280 B) is the per-lane validator `00608DD0` and `00608F20` run on a changed-lane mask: for each set bit of arg4 (lanes 0-3) it calls `00629970` for the lane and `00629CD0` for the lane plus its bit index, lane 3 additionally running `00629CB0` - the first nonzero return aborts the sweep, 0 means every armed lane validated.

Interior anchor `0060ED16` (function `0060EC80`).

`00662EA0` (151 B) is the per-element release the `0x88`-stride array sweeps (`005FDEA0`, `005FE010`, `00602760`) run per element: gated twice on `byte[+0x74]` bit 0 around a `00673780` pass, it then releases the two capacity-flagged buffer members (`+0x20`/`+0x28` and `+8`/`+0x10`) - each freed through `00584730` when its flag word's bit 31 is clear and the masked count exceeds 1, then both fields zeroed

Interior anchor `00662EDB` (function `00662EA0`).

`00627140` (23 B) is the five-qword record clear `0060B860`'s lane pass and `0060B750`'s all-lane run use: zeroes `+0x28`, `+0x30`, `+0x38`, `+0x40` and `+0x48` on the record in `rdx` and returns

Interior anchor `00627152` (function `00627140`).

`00623180` (103 B) is the four-slot conditional fanout `00608DD0`/`00608F20` close with: for each non-null member `+0x30`, `+0x40`, `+0x38`, `+0x48` it calls the matching lane body `006231F0`/`00623050`/`00622F40`/`00622D90` with (record, arg3), returning 0

Interior anchor `006231C6` (function `00623180`).

`00621F80` (27 B) is the one-call thunk `005FDEA0`'s no-target arm and `0060A410` use: calls vtable slot `+0x148` on `[[rcx+0x110]]` and returns 0

Interior anchor `00621F8B` (function `00621F80`).

`0060B860` (280 B) is the changed-lane apply `00608DD0`/`00608F20` run with the 4-bit mask: for each set bit it runs the lane-indexed pair `005C5230` then `00627160` (lane index carried in `r9d`, lane 3 getting an extra `005C5230` tail), and the first nonzero return aborts the sweep - 0 means every armed lane applied

Interior anchor `0060B8E7` (function `0060B860`).

`00629CD0` (373 B) is the per-lane index issuer `0060EC80` calls for each armed lane (`r9d`): for every live member `+0x30`/`+0x38`/`+0x40`/`+0x48` with the record's `[r8+0x28]` table live, it reads the lane's per-slot word pair (`+0x240`/`+0x248`, `+0x260`/`+0x268`, `+0x280`/`+0x288`, `+0x2A0`/`+0x2A8`), expands the index word `<<4` onto the lane's `+0x258`/`+0x278`/`+0x298`/`+0x2B8` base, and hands a three-field request block - pointer, tag word, and the lane's own `.data` tag `02CEDA20`/`02CEE3D0`/`02CEED80`/`02CEF730` - to `0062A0A0`

Interior anchor `00629D8D` (function `00629CD0`).

`00629970` (290 B) is `00629CD0`'s sibling lane pass under `0060EC80`: the same four-member `+0x30..+0x48` sweep and the same per-slot index expansion, but over the `+0x1C0`/`+0x1E0`/`+0x200`/`+0x220` word pairs with `+0x1D8`/`+0x1F8`/`+0x218`/`+0x238` bases and the shared `00628B40` sink instead of `0062A0A0`

Interior anchor `00629A04` (function `00629970`).

`0060B750` (265 B) is the unmasked all-lane variant of `0060B860` `0060A410` runs: lanes 0..3 unconditionally, each through the `005C5230`/`00627160` pair, then a `00627140` record clear and a final `005C5230` - the first nonzero return aborts

Interior anchor `0060B7F1` (function `0060B750`).

`00627640` (258 B) is the bounds-checked element handoff `00607410` runs: it rejects a null `[rcx+0x110]` and any `r9d` lane past the record's `+0x18` count (bit 31 clear, `cmovne` to 1), resolves the `0x28`-stride element's `+0x10` member from either the inline `+0x20` storage or the long-form pointer, and when non-null fires two `vtable+0x220` calls on `[rcx+0x110]` packing the value into stack out-blocks - returning 0 on success and 5 on every rejection

Interior anchor `006276C0` (function `00627640`).

`00627160` (338 B) is the four-lane descriptor submit `0060B750` and `0060B860` share: for each member table at `+0x30`/`+0x38`/`+0x40`/`+0x48`, when both the member and the caller's `+0x28` index table are live it fetches the u16 lane index at `[tbl+rsi*2+0x240/0x260/0x280/0x2A0]`, scales it by 16 into the record array at `tbl+0x258/0x278/0x298/0x2B8`, and hands `006272C0` the matching `.data` descriptor `02CEDA20`/`02CEE3D0`/`02CEED80`/`02CEF730` plus the `+0x248/0x268/0x288/0x2A8` u16 - the per-member lane publish behind the lane-mask walkers

Interior anchor `00627227` (function `00627160`).

`00628B40` (2557 B) is the record-stream copy engine `00629970` sinks into: for each of `u16` records at `r9+4` - `{u16 blob_off, u32 cursor, u8 kind}` against the blob `[rdx+lane*8+0x38]` - kind `0x30` takes a specialised path, kind `0x31` an aligned run (`shr 6`, cap 4), and the default copies `size` bytes from `blob+off` to `[rdi+0x10]+cursor` via `00861EBA`, aborting to `006294EF` when the cursor passes `[rdi+0x28]`

Interior anchor `0062913F` (function `00628B40`).

`0062A0A0` (1648 B) is the GI command-stream interpreter `00629CD0` calls: it walks `u16`-counted `{u16 blob_off, s32 index}` records, pulls each blob head's dword pair at `[r12+off]`, dispatches on the first word minus `0x42` (range `0xA0`) through the `006239C0`..`00624730` issue helpers and `005C5230`/`005CDAA0`, emits the `00D54E38` "read before use as a render target?" misuse diagnostic on three arms, and faults `00D54EF0` "Invalid constant buffer location : %d" on a bad slot

Interior anchor `0062A493` (function `0062A0A0`).

`00622D90` (419 B) is the GI descriptor registrar `00623180`'s caller family runs: six `0061E6B0` registrations of the `.data` descriptors `02CEDA20`/`02CEE3D0`/`02CEED80`/`02CEF730`/`02CF00E0`/`02CF0A90` on the `[rsi+0x110]` device, a vtable `+0x108` kick, then the guarded per-record slot write into the `02CEF730+0x968` ring with `02CF00D8`/`02CF00DC` min/max tracking and a `[rsi+0x168]<0xB000`-gated vtable `+0x220` close

Interior anchor `00622E7D` (function `00622D90`).

`00623050` (303 B) is the `02CEED80` slot writer `00623180` dispatches: the guarded `[rbx+0x2C]!=-1` index write into that table's `+0x968` ring with `02CEF728`/`02CEF72C` bounds tracking, the `01F2DEB8` cached-pointer compare-and-store feeding the `01F2DEB0` indirect call, `006238E0`, and the `01F2DE88`-gated `+0x220` tail

Interior anchor `006230FC` (function `00623050`).

`006231F0` (303 B) is `00623050`'s `02CEDA20` sibling - same guarded slot-write shape with `02CEE3C8`/`02CEE3CC` bounds and the `01F2DE98` cached-pointer store feeding the `01F2DE90` indirect call - and it is the variant that leaves `01F2DE88` set to 1 after its `+0x220` close

Interior anchor `0062329C` (function `006231F0`).

`00622F40` (266 B) is the `02CEE3D0` sibling: it opens with `0061E340` over `rcx+0x30` against `00D55120`, then runs the same slot-write/bounds/cached-pointer shape - `02CEED78`/`02CEED7C` tracking, `01F2DEA8` store feeding `01F2DEA0`, `006238E0`

Interior anchor `00622FDC` (function `00622F40`).

`006226D0` (249 B) is the GI lane issue `005FE010` runs: `0061C1C0` gate early-out, on tag change it stores into `01F2DEF8` and fires the `01F2DEF0` vtable entry, then selects operands by `[rbx+0xC]==8` (`0x39` vs `0x2A`) and `[rbx+0x6C]&1` (indexed 0x48-stride record via `+0x20` vs null), fires device vtable `+0x98`, and closes with a second device call on `[rsi+0x110]`

Interior anchor `00622767` (function `006226D0`).

`006225D0` (248 B) is `006226D0`'s sibling with the cleanup tail - identical `0061C1C0`/`01F2DEF8`/`01F2DEF0` gate and operand select, but after the `+0x98` issue it tests `[rdi+0x20]`, runs `0061ED00` and clears the byte, then closes on the device with `[rdi+8]` as argument

Interior anchor `00622664` (function `006225D0`).

`006238E0` (215 B) is the three-ring flush the `00622D90`/`00622F40`/`00623050`/`006231F0` slot writers share: for each `(used, limit, base)` ring on `rcx` - `+0x9A8`/`+0x9AC` over `+0x968`, `+0x8D8`/`+0x8DC` over `+0x4D8`, `+0x960`/`+0x964` over `+0x8E0` - when `used` reaches `limit` it submits the consumed tail `base + used*8`, count `limit - used + 1`, to `0062C9A0`/`0062CB40`/`0062CA70` (on `rcx+0x490`/`rcx`/`rcx+0x408`, with the caller's `rdx` payload) and rewinds `used` to the ring capacity `8`/`0x80`/`0x10`

Interior anchor `0062395C` (function `006238E0`).

`006272C0` (687 B) is the record-list resolve-and-place dispatcher `00627160`'s four lanes feed: it walks the `u16`-counted `{u16 blob_off, s32 index, ..}` records at `r9+4` (`0x10` stride), resolves each blob as `[rdx+index*8+0x38] + blob_off`, and dispatches the blob head's first dword minus `0x42` (range `0xA0`) through the `00627590`/`00627570` jump tables - arms write resolved objects three ways: min/max-tracked ring slots at `+0x4D8`/`+0x8E0`/`+0x968` with `+0x400`/`+0x80`/`+0x40` cursor pairs, or `006241D0`/`00624220`/`00624180`/`00624730` accessor results into the `r15 + index*8 + 0x30` out array; an unknown kind fires the `00D55060` "Unknown" diagnostic via `005CDAA0` when the caller's flag word is nonzero, and `index == -1` skips

Interior anchor `00627479` (function `006272C0`).

`0061E340` (525 B) is the eight-slot dirty-publish `00622F40` runs: it gathers up to `min(r8d, 8)` pointers from `rdx` starting at index `[rcx+0x6D0]`, diffs the set against the cached row at `+0x690`..`+0x6C8` with the caller's eight `-1` sentinels at `r9`, and on any change - or a `+0x6D4` count mismatch - writes the new set into `+0x690`.. and vtable-calls `[rcx+0x110]->+0x110` with the `+0x648` array, the `edi - [+0x6D0]` delta, and `[+0x688]`; `+0x6D4` is re-seeded with the count afterwards

Interior anchor `0061E454` (function `0061E340`).

`0061EBE0` (234 B) is the indexed record accessor `00607410` runs on `[rcx+0x110]`: index `r9d` must pass under both `([rdx+0x18] & 0x7FFFFFFF) ?: 1` and the raw masked count; the `0x28`-stride record row (inline at `rdx+0x20` when the count is `<= 1`, else through `[rdx+0x20]`) must carry a non-null `+0x10`; then it vtable-calls `[rbx]->+0x198` with that pointer and a four-element `r10d` vector - every rejection returns `5`, success `0`

Interior anchor `0061EC74` (function `0061EBE0`).

`006241D0` (67 B) is the counted 0x58-record accessor `006272C0` and `0062A0A0` share: `edx` must pass under `([rcx+0x30] & 0x7FFFFFFF)`; the row base is inline `rcx+0x38` when the masked count is `<= 1`, else `[rcx+0x38]` - it returns `[base + idx*0x58 + 0x20]`, and `0` on an out-of-range index

Interior anchor `006241F2` (function `006241D0`).

`00624730` (71 B) is the counted 0x48-record accessor `006272C0` and `0062A0A0` share: `edx` must pass under `([rcx+0x20] & 0x7FFFFFFF)` and `+0x74` bit `0` must be set; the row base is inline `rcx+0x28` when the masked count is `<= 1`, else `[rcx+0x28]` - it returns `[base + idx*0x48 + 0x10]`, and `0` otherwise - the `006241D0` shape at the `+0x20`/`+0x28` field pair

Interior anchor `00624754` (function `00624730`).

`006224E0` (225 B) is the submit bridge `005FDEA0` runs: `0061C1C0(edx)` gates the whole body; a changed result publishes the new value to `01F2DEF8` and fires the `01F2DEF0` callback once, then it picks the `0x39`/`0x2A` code on `byte [rbx+0xC] == 8`, resolves a `0x48`-stride table row (`[rbx+0x20]` or inline, indexed by the caller's dword) when `+0x6C` bit `0` is set, and fires two vtable ops on `[rdi+0x110]` - `[vtable+0x98]` with the row, then `[vtable+0x60]` with `esi`

Interior anchor `0062254E` (function `006224E0`).

`0062CB40` (196 B) is the run-collapse helper `006238E0` uses on the `+0x400` slot: it scans a u64 range pair for the first position where `[rbx+i]` stops equal-matching `[r10+i]`, then the symmetric tail scan backwards from `[rdi]`/`[rdx]`, and when a positive gap remains it `00861EBA`-memmoves `count*8` bytes and tail-calls vtable `[rsi+0x400]` with `(rbp, gap_index, rbx, r10)`

Interior anchor `0062CB8E` (function `0062CB40`).

`0062CA70` (196 B) is the same collapse specialised to the `+0x80` slot: identical forward/backward divergence scan over the 8-byte-element ranges, same `00861EBA` compaction, tail-calling `[rsi+0x80]` - the three helpers differ only in which vtable slot ends the move

Interior anchor `0062CABE` (function `0062CA70`).

`0062C9A0` (193 B) is the third sibling ending on `[rsi+0x40]`: the same two-direction equal-run scan and `00861EBA` move as `0062CB40`/`0062CA70`, each covering one dispatch slot of the command-record object `006238E0` drives

Interior anchor `0062C9EE` (function `0062C9A0`).

`0061D260` (190 B) is the three-subcommand flush `00629C70` emits on the `[rdi+0x110]` object: slot `+0x158` is called with `rdx = [rcx+0x170]` when `[rdi+0x9C4] == 2`, else `[rcx+0x168]`; slot `+0x118` is called with a zeroed 16-byte block and `-1` when `[rcx+0x180]` is live; and slot `+0x120` carries byte `[rcx+0x188]` when `[rcx+0x178]` is set - three independently-armed command pieces per record

Interior anchor `0061D2B3` (function `0061D260`).

`0062A920` (183 B) is the marshalled field emit `00607410` runs to fill the `+0x9F8` command block: `dl` lands at `+0x9F8`, two stack bytes at `+0x9FC`/`+0x9FD`, two `0061C010` selector resolves write `+0xA0C` and `+0xA1C`, six `0061C150` marshals write `+0xA00`..`+0xA08` and `+0xA10`..`+0xA18` from the stack argument run, and `[rbx+0x9C0]` then OR's in bit `4` - the commit flag for a fully-staged block

Interior anchor `0062A95A` (function `0062A920`).

`0061ED70` (181 B) is the gated double-emit `00607410` runs for flagged entries: `[r8+8] & 6`, `[rdx+8] & 8`, `[rdx] >= 4` and `[rdx+4] == 4` must all hold, else the return is `5`; passing, `00624180` on the `r8` record and `00623F00` on `rsi` each resolve a payload handed to two virtual emits on the `[rcx+0x110]` object - slot `[rbx+0x188]` first with `[rbp+0x7B8]` as context, slot `[rdi+0x178]` second - the paired command write a flag-armed entry triggers

Interior anchor `0061EDD0` (function `0061ED70`).

`00627E50` (176 B) is the `+0x9C0`-offset adapter `00607410` calls into `00627E60`'s shared two-field writer: `edx` clamps into 1..5 and stamps `[rec+0x74]`, `r8d` clamps the same way into `[rec+0x80]` with `or [rec], 2` armed - the GI record's paired kind-field publish

Interior anchor `00627E9C` (function `00627E50`).

`00626CE0` (175 B) is the narrow-to-wide copy `00607410` calls for the command's string operand: a `strlen` over `rdx`, `0017D260(len*2, 2)` allocates the wide buffer, bytes sign-extend to words until NUL, the buffer then goes through `00584730`, and the body returns 0 (`0xD` when the input pointer is null)

Interior anchor `00626D2D` (function `00626CE0`).

`00628250` (170 B) is the packed-colour unpack `00607410` calls to fill the command record's `+0x7C0` float4: the `edx` dword's four bytes (`>>16`, `>>8`, `+0`, `>>24`) each `cvtsi2ss`-convert (with the `2^32` bias lane compiled in though never taken on a `movzx` byte) and scale by `1/255` (`3B808081` at `00D11104`), writing `+0x7C0`..`+0x7CC`

Interior anchor `0062828A` (function `00628250`).

`00622450` (144 B) is the mode setter `005FE010` calls: with `r9d` and the stack arg both non-null, `0061C1C0(edx)` returns a code compared against cached `01F2DEF8` - a change stores it and fires `01F2DEF0`'s `00616F00`-table callback on `[rdi+0x110]` - then unconditionally calls vtable `+0xA8` on `[rdi+0x110]` with `(esi, stack-arg, ebp)`; returns 1 either way - the compare-then-notify command setter the family records.

Interior anchor `0062249E` (function `00622450`).
