---
system: CharacterRenderObject — the 1,640-byte object that draws a character
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: CodeDomain — Presentation.CharacterRenderObject
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
last_reviewed: 2026-09-02
audit:
  passes: 3
  last_pass: 2026-09-02
  last_pass_state: falsification-pass-1-repos-46
  crossref_clean: true
---

# CharacterRenderObject

**The first game class read out of the new vtable index.** `CharacterRenderObject` is the largest
FFXII-specific class recovered by RTTI — **31 vtable slots, 11,879 bytes of method code, a
1,640-byte object** — and it is what stands between a character existing and a character being drawn.

## 1. What the player sees

Vaan on screen. A Rabanastre guard. A Malboro.

**This is the object that draws a character**, and it is the layer where a character's *appearance*
is decided separately from their *existence*: ~~the material overrides that tint a body when a status~~
~~lands,~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5, BB-1: slot 24 writes the four refraction parameters, not a status tint)* the transform palette that puts a sword in the right hand, the fade mode that dissolves a
model in and out.

**A character can exist and not draw.** The class carries a single byte — `+0x4B4` — that the
constructor clears and the setup method sets when construction finishes. **Twelve of its thirty-one
methods check it as the first thing they do**, and a thirteenth consults it deep inside a
submission loop. Until it is set, update, submit~~, material propagation and transform propagation~~ and material propagation *(corrected 2026-10-02, OPUS: slot 26 `001FAA10`, transform propagation, never reads `+0x4B4`; §5's 2026-09-27 note)*
all return immediately. That is the mechanism behind a model that is present in the world but not
yet visible.

## 2. Native mechanism

**One construction site in the entire binary**, and the allocation size sits immediately above it:

```asm
001BD527  mov  ecx, 0x668          ; 1,640 bytes
001BD52C  call FUN_00210ec0        ; allocate
001BD531  mov  [rsp + 0x50], rax
001BD536  test rax, rax
001BD539  je   0x1bd548            ; allocation failed -> skip construction
001BD53B  mov  rcx, rax
001BD53E  call CharacterRenderObject_Construct   ; 001F4DA0
```

`CharacterRenderObject_Construct` (`001F4DA0`, 516 B) is one of only **two** functions in the image
that reference the vtable at `00903B68`; the other is `FUN_001F51E0`.

### The ready flag at `+0x4B4`

The single most-touched field in the class, and its access pattern is asymmetric in a way that
settles what it is:

```
accesses to +0x4B4 across the 31 vtable methods : 14
  writes                                        :  1   <- slot 2, at +2233 of a 2,328-byte
  reads                                         : 13         method: the END of setup
reads within the first 12 instructions of their method : 12 of 13
```

plus **one further write outside the vtable**, in the constructor:

```asm
001F4DDF  xor  esi, esi                        ; CharacterRenderObject_Construct
...                                            ; rsi is not reloaded before:
001F4EC9  mov  byte ptr [rdi + 0x4b4], sil     ; = 0
001F7729  mov  byte ptr [r8  + 0x4b4], 1       ; slot 2, +2233 of 2,328 bytes
```

**Cleared at construction, set at the end of setup, and never written again.** Nothing in the class
clears it back — `CharacterRenderObject_ResetState` only reads it — so after setup the byte is a
one-way latch. It is a ready flag, and the explicit zero at construction is better evidence for
that than the allocator's zero-fill would have been.

*(Restated 2026-09-26: the image-wide count is sixteen readers — thirteen entry gates, one plain getter, one late
gate and slot 16's per-element term. See the [contract](../CONTRACT-character-render-object.md) R-4. The two
sentences below count only the vtable's thirteen, and among those the "twelve" includes slot 27's getter, which does
not gate.)*
**Twelve of the thirteen readers check it at method entry**; the thirteenth does not. Slot 16
reads it at **instruction 118**, inside a submission loop, as one term of a per-element filter:

```asm
001FA5B2  cmp   dword ptr [r14 + 0x4a4], 0
001FA5BA  jne   0x1fa61e                       ; -> next element
001FA5BC  cmp   qword ptr [rbp + 0x18], 2
001FA5C1  je    0x1fa5e4
001FA5C3  movzx eax, byte ptr [r14 + 0x4b4]    ; the ready flag, as a loop-body condition
001FA5CD  je    0x1fa61e                       ; -> next element
```

So the byte is consulted two different ways: as an **entry precondition** in twelve methods, and as
**one condition among several in a per-element skip test** in the thirteenth.

Slot 8 shows the read shape:

```asm
001F9B48  movzx eax, byte ptr [rcx + 0x4b4]
001F9B58  test  al, al
001F9B5A  je    0x1f9fb6              ; not ready -> straight to the epilogue
```

## 3. Key addresses

| | |
|---|---|
| vtable | `0x00903B68` |
| constructor | `0x001F4DA0` `CharacterRenderObject_Construct` (516 B) |
| sole construction site | `0x001BD527` inside `FUN_001BD4A0` |
| allocator called | `0x00210EC0` |
| **object size** | **`0x668` = 1,640 bytes** |
| ready flag | `this + 0x4B4` (byte) |

**The full 31-slot vtable:**

| slot | address | size | identity | interior |
|---:|---|---:|---|---|
| 0 | `001F52F0` | 52 | scalar deleting destructor | |
| 1 | `001F89B0` | 42 | appends the `+0x28` child to `[01F7F5E0]`: `0018B4E0` lookup then tail-jump `0018AFF0` (a push_back, `0018B006`–`0018B013`); removal is slot 3's `0018B0B0` | `001F89BF` |
| 2 | `001F6E70` | 2328 | **setup — the only writer of the ready flag** | `001F6E7A` |
| 3 | `001F6D60` | 149 | ready-gated teardown: clears `+0x490`, calls `001F86F0`/`0018B4E0` | `001F6D7A` |
| 4 | `001FB070` | 7 | setter `+0x498` — two instructions, store then `ret` | `001FB076` |
| 5 | `001F86E0` | 8 | getter `+0x498` — two instructions | `001F86E7` |
| 6 | `001F9FF0` | 161 | `== 2` test via `008C2CC8`, the `api-ms-win-crt-math` `_fdtest` import — zeroes NaN inputs; touches `+0x3B0`/`+0x3B4`/`+0x3B8` | `001FA01E` |
| 7 | `001FB080` | 147 | touches `+0x3B0`/`+0x3B4`/`+0x3B8` | `001FB0DB` (interior — `call 001EF060`) |
| 8 | `001F9B20` | 1211 | **`CharacterRenderObject_UpdateViewParameters`** | |
| 9 | `001F9A80` | 159 | ready-gated float setter: `008C5B40` is one 255.0 divisor; the clamp range on `arg+0xC` is [0, 1.0] | `001F9AA3` |
| 10 | `001F8C00` | 97 | SIMD state | `001F8C17` |
| 11 | `001F8BE0` | 27 | SIMD state mutation: `mulss` against `008C5B34` (1/128; `008C5B2C` holds 0.001), flag `+0x4A4` | `001F8BE8` |
| 12 | `001F8C70` | 160 | bitfield state | `001F8C8A` |
| 13 | `001FB120` | 496 | ready-gated indexed access: `arg` selects a stride-`0x318` record under `+0x58` | `001FB14A` |
| 14 | `001FA0A0` | 60 | SIMD state | `001FA0B3` |
| 15 | `001F9A60` | 7 | setter `+0x49C` | |
| 16 | `001FA3D0` | 1073 | **`CharacterRenderObject_SubmitMaterialsWithFadeMode`** | `001FA3FF` |
| 17 | `001F5C10` | 15 | snapshots `[+0x390]` into `[+0x398]` | `001F5C17` |
| 18 | `001FAFB0` | 188 | gathers `[r9]`/`[r10]`/`[r11]` pointers into out-slots beside `this+0x390` | `001FAFE7` |
| 19 | `001F8D10` | 3397 | **`RenderPartMaterialParameterBinding`** — the largest method | `001F8D25` |
| 20 | `001FA0E0` | 189 | ready-gated list walk: packs `r8b<<16|r9b` into a tag and scans `[+0x488]+0x28` | `001FA111` |
| 21 | `001FA810` | 7 | setter `+0x4B6` — two instructions | `001FA816` |
| 22 | `001F9FE0` | 9 | float setter `movss [+0x4B8], xmm1` | `001F9FE0` |
| 23 | `001F9A70` | 9 | setter `+0x4BC` — two instructions | `001F9A78` |
| 24 | `001FA1A0` | 547 | **`MaterialOverrideParameterPropagation`** | `001FA1BD` |
| 25 | `001FAD40` | 7 | setter `+0x4B0` — two instructions | `001FAD46` |
| 26 | `001FAA10` | 812 | **`NamedTransformPalettePropagation`** | `001FAA29` |
| 27 | `001F86D0` | 8 | getter `+0x4B4` (the ready flag) — two instructions | `001F86D7` |
| 28 | `001F6E50` | 14 | indexed record locator: `return [+0x58] + idx*0x318` | `001F6E52` |
| 29 | `00848340` | 5 | member address accessor | |
| 30 | `001FA820` | 488 | ready-gated range walk over the `[rdx]..[rdx+8]` pointer pair | `001FA840` |

*(2026-09-14 — NOCALLER-INSTALLERS: the 26 vtable members that have no direct caller are
bound above. They dispatch through the `00903B68` vtable only; the `interior` column cites one
instruction inside each body so the slot-to-code binding can be checked without trusting the
table row.)*

The three descriptive names in bold-italic come from the GFZ's own `CodeDomain` tags, which exist for
**exactly three functions in the whole binary** — all three of them here.

## 4. Data structures and formulas

### Object layout, as far as it is established

```
+0x000  vtable pointer
+0x008, +0x010, +0x018   vec16 vector (begin/end/capacity, element stride 0x10),
                       allocator object at +0x020 — dtor frees begin via [alloc.vt+0x18]
                       (001F52BE–001F52D9)
+0x028  ctorBoundRef — ctor arg, cleared first in teardown (001F51FC)
+0x030, +0x038, +0x040   materialPtrVec vector (begin/end/capacity, element stride 8 —
                       a pointer array iterated by SubmitMaterialsWithFadeMode,
                       001FAA10, 001FB080), allocator object at +0x048
+0x050  boundSubobjectRef — ctor-seeded, read as a call receiver (001FB0F2)
+0x058, +0x060, +0x068   recordArray vector (begin/end/capacity, element stride 0x318),
                       allocator object at +0x070
+0x0C .. +0x74    early scalar block (slots 2, 13 read; not characterised)   <- corrected 2026-10-02, OPUS - no such block: the constructor fills +0x08..+0x77 as the three vectors, their allocator objects and the two refs above (001F4DA0+0x41..+0x95), and slot 13's only read in this range is the +0x58 vector (001FB120+0x3C)
+0x100, +0x108    slot 2
+0x2C8 .. +0x2E0  slot 24 — material override propagation working set
+0x2E8 .. +0x310  slot 30 — a second 8-byte-strided run
                  [corrected 2026-09-27, FABLE, Claude Opus 5.5, BB-1: these two runs are offsets inside each 0x318 record
                   of the recordArray (record = [+0x58] + i*0x318, 001FA262/001FA8C2),
                   not fields of this object]
+0x390, +0x398, +0x3A0   auxVec36 vector (begin/end/capacity, element stride 0x24),
                       allocator object at +0x3A8; ResetState clears it end=begin
+0x3B0, +0x3B4, +0x3B8, +0x3BC   submitInVec — slots 6 and 7 write the first
                       three floats; +0x3B0 is passed to 001ABF50 in r9
                       (001FA423–001FA438, +0x3C0/+0x3D0 at 16-byte stride)
                       [corrected 2026-09-27, FABLE BB-1, verified SWE2-STRUCT:
                        an INPUT vec4, not an out-param — 001ABF50 only reads it
                        (subss at 001AC075/7B/E6/EC)]
+0x3C0, +0x3D0    submitOutVecB / submitOutVecC — the actual out-params (r8,
                       rdx): 001ABF50 head-fills +0x3C0 with zeros and +0x3D0
                       with 4s, then indexed-stores into both (001ABF6E/74,
                       001AC33C, 001AC350/354)
+0x3E0           embedded object destructed by 006336E0 (extent unproven)
+0x480 .. +0x498  slots 2, 3, 19, 20
+0x498  scalar, dedicated getter (slot 5) and setter (slot 4)
+0x49C  scalar, setter slot 15
+0x4A8  float,  written by UpdateViewParameters
+0x4AC  int,    written by UpdateViewParameters
                  [corrected 2026-09-27, FABLE, Claude Opus 5.5, BB-1: a float - 1.0f from the ctor, compared
                   with 0.9 by slot 16 at 001FA5A4]
+0x4B0  scalar, setter slot 25
+0x4B4  BYTE — the ready flag; getter slot 27
+0x4B6  scalar, setter slot 21
+0x4B8  scalar, setter slot 22
+0x4BC  scalar, setter slot 23
+0x644, +0x654    slot 9
+0x664            highest offset observed
                  ---- allocation ends at 0x668 ----
```

**The highest field observed is `+0x664` and the allocation is `0x668`.** Those were measured
independently — the offsets from disassembling all 31 methods, the size from the allocation site.
`+0x664` is written as a **dword** (`mov dword ptr [rdi + 0x664], r14d`, slot 24), so it ends at
`+0x668`: the last field is **flush with the end of the allocation**, with no slack. That is the
confirmation that the layout scan reached the end of the object rather than stopping early.

The size is confirmed a second, independent way. Exactly three sites in the binary load the
immediate `0x668` into a register: the allocation at `001BD527`, an unwind funclet (banned as
evidence, and irrelevant), and **`001F5309` in slot 0** — the scalar deleting destructor passing
`0x668` as the size argument to a sized `operator delete`. **Allocation and deallocation agree.**

### `UpdateViewParameters` (slot 8)

Takes a parameter block in `rdx` and copies a reduced form into the object:

```asm
mov   r15d, dword ptr [rbx + 0xd0]     ; rbx = the parameter block
movups xmm0, xmmword ptr [rbx + 0xc0]  ; a 4-float vector
mov   eax,  dword ptr [rbx + 0xcc]
movss dword ptr [r14 + 0x4a8], xmm6    ; -> this
mov   dword ptr [r14 + 0x4ac], eax     ; -> this
```

It calls **`tan` and `sqrtf`**, which is the shape of a projection or field-of-view derivation rather
than a copy. ~~**The formula itself is not established** — the constants are RIP-relative floats that
have not been read out.~~ **BB-2 answered 2026-09-12 (FABLE): not a projection — it is the
character's map-lighting fix-up, and the "constants" are the console's `mMapChr*` settings.**
`CharacterRenderObject_UpdateViewParameters(this, param, f /*xmm2*/)`, guarded by `this+0x4B4`:

- `this+0x4A8` ← the float argument `f` (`001F9B4F` / `001F9B8B`); `this+0x4AC` ← `param+0xCC`
  (`001F9C0A`–`001F9C1E`); ~~`param+0xD0` is the light count.~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5, BB-1: `param+0xD0` is a light index,
  range-tested as x + 1 <= 6 at `001F9F08` and stored into the material's `sunIndex` parameter at `001F9F15`, a handle
  `001F7790` binds.)*
- **Ambient:** unless the flag byte `[001EBA40()] + 0x118` is set, `param+0xC0..+0xC8` (RGB) becomes
  `rgb × mMapChrAmbientIntensity + mMapChrAmbientOffset` per channel — the six settings at
  `01F82ED8`/`EDC`/`EE0` and `01F82EE8`/`EEC`/`EF0` the console page names (`001F9BB0`–`001F9BFE`).
  Those words hold junk in the file image (`0x01C335EC` …) because the scene-config loaders fill
  them at boot, which is why "reading the constants out" of the image could not work.
- **Six directional lights** (`param+0x64`… copied to a local 16-byte-stride array,
  `001F9C30`–`001F9CB9`) are each classified **upward** when `y > 0` and
  `tan(mMapChrUpwardDirLightAngleThres · π/180) · y > sqrt(x² + z²)` — i.e. the direction lies
  within `thres` degrees of straight up (`001F9D3E`–`001F9D99`; `sqrtf` `00861F14`, `tan` `00861F50`,
  π and 180 as doubles at `009042E0` / `009042E8`; the test is skipped when the threshold exceeds
  89°). Default threshold 15° (`01DFE198`).
- Each light's colour is then scaled by **`mMapChrDirLightColorIntensity`** RGB (`01F82EF8`/`EFC`/`F00`)
  and, when the light was classified upward and the `001EC560()` result was zero, additionally by
  **`mMapChrUpwardDirLightColorIntensity`** (`01DFE19C`, default 1.0) (`001F9DAB`–`001F9E4E`).

So the `tan`/`sqrtf` pair is an elevation-angle test on light directions, not a field of view; the
routine applies the map-versus-character lighting settings the developer console exposes.

## 5. Call chain

```
FUN_001BD4A0
   -> allocate 0x668 bytes            (FUN_00210EC0)
   -> CharacterRenderObject_Construct (001F4DA0)
        -> ... slot 2 setup (001F6E70) ...
             -> mov byte [this+0x4B4], 1      <- ready
   then, per frame, guarded on +0x4B4:
        [corrected 2026-09-27, FABLE, Claude Opus 5.5, BB-1: slot 26 never reads +0x4B4]
        slot 8   UpdateViewParameters
        slot 16  SubmitMaterialsWithFadeMode
        slot 19  RenderPartMaterialParameterBinding
        slot 24  MaterialOverrideParameterPropagation
        slot 26  NamedTransformPalettePropagation
```

~~**The ordering within a frame is not established**~~ *(answered: see §7, BB-3 answered 2026-09-26 - the render record's draw fixes the order; 2026-10-02, OPUS)* — the guard tells you these methods refuse to run
before setup, not the sequence in which they run. **BB-3.**

## 6. Modding notes

- **`+0x4B4` is a hard gate.** Anything driving this object externally must respect it: with the byte
  clear, ~~twelve of the class's methods return at their first branch~~ eleven of the class's vtable methods and two non-virtual helpers gate on it at entry *(corrected 2026-10-02, OPUS: slots 3, 8, 9, 10, 12, 13, 14, 19, 20, 24 and 30, plus `001F89E0` and `001FAD50`; slot 16 reads it late and slot 27 returns it; CONTRACT-character-render-object.md R-4)* and no amount of correct
  parameter setting will produce a draw.
- **The object is 1,640 bytes with a single construction site**, so it is cheap to find at runtime by
  the vtable pointer at `+0` (`0x00903B68`) and nothing else needs to be pattern-matched.
- **XIIOnline:** material override propagation (slot 24) and named transform palette propagation
  (slot 26) are the two paths that would carry a remote player's appearance — equipment, tint, and
  the bone palette a weapon hangs from. ~~Neither has been read; both are named only.~~ *(answered: see §1's 2026-09-27 correction - slot 24 is read and writes the four refraction parameters, not a tint; 2026-10-02, OPUS)*

## 7. What is not known

- [x] **UQ-199.** What the class actually renders per method. *(SUPERSEDED in the register 2026-09-26, FABLE, Claude Opus 5.5: a duplicate; the open residue is carried by **BB-1**)* Slots 19, 24, 26 and 30 are named from GFZ tags,
      not from their bodies. **BB-1 - narrowed to a bounded negative, see section 8c:** the 31
      methods' complete one-hop callee set is **46 real functions**, and **not one is a graphics API
      entry point**. Whatever draws, it is not called directly from this class.
      **BB-1 ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5) - the class draws through `001F5D70`, a method outside its
      vtable, reached per frame through the ordered list.**
      - The render record's per-frame update calls slot 1, which appends the object's pooled `CharacterOrderedObject`
        to `[01F7F5E0]`.
      - The application's render pass list walks that list, and each element's slot 1 (`00215320`) jumps to
        `001F5D70`.
      - `001F5D70` calls Phyre's draw submit `0060B980` per mesh instance, in a shadow, alpha or opaque mode.
      Per method: 8 slots upload shader parameters into each material's block, 14 stage state the draw reads, and 9 are
      bookkeeping. [Table and control](../../_index/candidates/bb1-render-object-methods/README.md) (`bb1_methods.py`,
      4 checks). Thirteen statements on this page and its contract are contradicted by the bytes (record, findings): six are
      routed to their authors, and FABLE's own seven are corrected where they stand (§1, §2, §4, §5 and the contract).
- [x] ~~The formula in `UpdateViewParameters` — it calls `tan` and `sqrtf` over RIP-relative float
      constants that have not been read out.~~ **BB-2 ANSWERED 2026-09-12 (FABLE)** — the character
      map-lighting fix-up: ambient `rgb × intensity + offset`, six directional lights classified
      "upward" by an elevation-angle test and scaled by the `mMapChr*` colour-intensity settings (§2).
- [x] The per-frame ordering of the guarded methods. The guard proves precedence over setup, not the
      order among themselves. **BB-3.**
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5), static: the render record's draw fixes the order, and slot 16 fixes the
      order of five more.** The owning render record drives its object through a family of one-line wrappers,
      each forwarding to one slot, from its per-record draw body. The render-command path runs that body once per
      record, and a second time (pass 1) when the record's `+8` bit 0 is set.
      - **In the draw.** In address order, which is execution order (no backward jump re-enters a call), the slots
        run: 11, 1, 1, **8, 9**, 21, 22, 23, **24**, 15, 26, **12**, 17, 6, **16**. Each runs at most once per draw
        and each is conditional. So the latch-gated slots the draw reaches run **8 → 9 → 24 → 12 → 16**.
      - **Inside slot 16.** `CharacterRenderObject_SubmitMaterialsWithFadeMode` calls its own slots once per
        material element, in this order:
        - **14**;
        - **19**;
        - **20**, only for element kinds 2, 5, 10 and 13;
        - **10**;
        - **13**, the transform publish.
      - **Slot 3** runs on pooled objects only: the pool's per-frame update calls it once a released object's
        three-frame countdown ends (see BB-4). **Slot 30** is called from a non-virtual method, not from the draw.

      *Limits:*
      - This is code order within one record's draw. Which records draw first is the render command list's
        order, not read here.
      - The conditions on each call are in the control, not restated.

      Control: [`bb3_slot_order.py`](../../_index/candidates/bb3-render-object-slot-order/bb3_slot_order.py) (5 checks, FAILS 0). Its sensitivity check bounds each wrapper to its own body, so a
      helper wrapper cannot be credited with its neighbour's slot.
- [x] Whether one `CharacterRenderObject` exists per visible character, per party member, or per
      model instance. **There is one construction site, which does not by itself settle the
      cardinality.** **BB-4.**
      *Narrowed 2026-09-15 (OPUS) — **the cardinality rule is now read; the row stays open because
      it decides between three options and the rule does not match any of them as worded.***
      - **The construction site is a find-or-create, not a construction.** `001BD4A0` first walks a
        binary search tree — root `[rbp+0x38]`, end sentinel `rbp+0x28`, key `[node+0x20]` —
        looking for the **qword** `[rdi+0x2A0]` (`001BD4EB`–`001BD525`). **Only on a miss**, when
        the cursor is still the sentinel, does it reach `001BD527` and allocate `0x668` bytes.
      - **And the thing it keys on is itself fetched by a lookup.** `rdi = 001BAFF0(id)`, which is
        the same find idiom over a *different* container — root `[rcx+0xC8]`, sentinel `rcx+0xB8`,
        key `[node+0x20]` compared against a **signed int** id (`001BB006`, `001BB022`).
      - **So the rule is: one `CharacterRenderObject` per distinct `[record+0x2A0]`, created lazily
        on first miss and ~~shared thereafter~~.** ~~Two character records carrying the same value share~~
        ~~one object~~, and nothing static bounds how many distinct values there are. *(Corrected (FABLE, Claude Opus 5.5, 2026-09-26):
        not shared. The tree is a per-model **pool of released objects**, and a hit takes the object out of it;
        see the answer below.)*
      - **That rules out two of this row's three options as worded.** It is **not** one per party
        member — that would be a fixed small count, and this is a map keyed on a record field. It
        is **not** unconditionally one per visible character — ~~two visible characters with the same~~
        ~~key share one~~ *(corrected: they do not share; the answer below)*. **“Per model instance” survives only if `+0x2A0` turns out to denote one**,
        which is the step this narrowing does not take.
      - **What `+0x2A0` is, so far:** a **64-bit handle using the all-ones empty convention** —
        `001B9260` stores `0xFFFFFFFFFFFFFFFF` into it (`001B92EB`) and **`001BB2B0` assigns it**
        (`001BB716`, `001BB745`). *A displacement census cannot be trusted further than that here:*
        `+0x2A0` has 155 sites in 113 functions across many unrelated object types, so only the
        writers inside this `001Bxxxx` cluster are attributable to this record.
      - **This also explains the “count — not established” row in § above:** ~~there is no count~~
        ~~to establish~~. The objects are allocated one at a time ~~and held in a tree, not in an array~~,
        which is exactly why the 160-element `0x740`-stride block is a *different* structure.
        *(Corrected (FABLE, Claude Opus 5.5, 2026-09-26): active objects are held in a vector, and only released ones sit in the tree.
        There is a count: one per active render record, below.)*
      **BB-4.**
      **ANSWERED (FABLE, Claude Opus 5.5, 2026-09-26): one `CharacterRenderObject` per active character render record, recycled per
      model; never shared between two records.** Reading `001BD4A0` past its construction, and the release beside
      it, gives the whole life cycle.
      - **Acquire (`001BD4A0`).** It looks up the id's model entry and searches its tree for the entry's `+0x2A0`.
        - On a **hit** it takes the first object off that node's list (`001BD566`–`001BD56A`) and resets it
          (`CharacterRenderObject_ResetState`). It unlinks and frees the list element, and erases the node when
          the list is empty.
        - On a **miss** it constructs a new object and runs slot 2 with the id and entry.
        - Either way the object is appended to the pool's active vector and returned.
      - **Release (`001BD840`).** It finds the object in the active vector and keys it by
        `[[object + 0x488] + 0x2A0]`. It appends `{object, 3}` to that key's list in the tree, creating the node
        if needed, and removes the object from the vector.
      - **Who acquires and releases: the render records.**
        - When a record's `+0x6B8` is null and its model entry is present, the pose update
          `Skeleton_UpdateFinalPoseAndCombatLook` (and one other per-record body) stores
          `+0x6B8 = acquire(+0x6B0)`.
        - `CharacterRenderRecord_TeardownAndReset` releases `+0x6B8` and zeroes it.
      - **What `+0x2A0` is.** The character asset loader `001BB2B0` sets it to `(kind << 32) | index`. The model-id
        decoder produces the pair from the id's letter (bits 16–23) and number (bits 0–15), for example `c1004` →
        kind 14, index 25,100 (`001BB736`–`001BB745`). So the pool key is the **model resource**.

      So of the row's three options, **per model instance** is right, in the sense of one per rendered
      character record:
      - two records showing the same model hold two objects;
      - a record torn down gives its object back to that model's pool, and the next record showing the model reuses
        it after a reset;
      - the live count is the number of records holding one, bounded by the 160 records of §8b, plus the pooled
        objects.

      **Bounds:**
      - the pool singleton's own update also acquires, with id `−1`, for its entries;
      - the pooled element's `3` (a likely expiry count) ~~is not followed here~~ *(answered: see the slot-3 bullet above - the pool's per-frame update calls slot 3 when that three-frame countdown ends; 2026-10-02, OPUS)*.

      Control: [`bb4_render_object_per_model.py`](../../_index/candidates/bb4-render-object-per-model/bb4_render_object_per_model.py) (5 checks, FAILS 0). Its sensitivity check pins the unlink that the "shared" reading
      would lack. See also the [consumer check](../../_index/candidates/bb4-render-object-per-model/consumer-check.md).
- [x] ~~What `FUN_001F51E0` - the only other function referencing the vtable - does.~~
      **BB-5 ANSWERED** - it is the class's **destructor body**. It re-installs the vtable at
      `[rcx]` (standard MSVC destructor behaviour), zeroes `+0x28`, destroys a container at
      `+0x3E0`, then frees the `+0x390`/`+0x3A0`/`+0x3A8` vector at element stride `0x24`
      (corrected 2026-09-17, SWE2-STRUCT: the magic `0xE38E38E38E38E39` is signed /36, and
      `lea r8,[rdx+rdx*8]`/`shl r8,2` reconstructs count×36 = 0x24-byte elements; the earlier
      `0x38` reading was wrong). It has exactly one caller: **slot 0**, the scalar deleting
      destructor. It is not a second construction site.
- [x] ~~**BB-6 (new).** The class's non-virtual methods.~~ **BB-6 ANSWERED 2026-09-14 (OPUS):
      the method inventory is 31 virtual + 17 non-virtual.**
      - **The span is exclusive, and that control comes first.** The class's implementation occupies
        `001F52F0`-`001FB120`. Thirty method rows fall inside it and **every one is
        `CharacterRenderObject`** - no other class's vtable slot is interleaved - which is what makes
        code locality usable here rather than merely suggestive. (Slot 29 lives out at `00848340`.)
      - **17 functions in the span are not vtable slots.** `functions.tsv` lists 47 entries there and
        30 are slots. The seventeen are `001F5330` `001F55F0` `001F57E0` `001F5B80` `001F5C20`
        `001F5D70` `001F68E0` `001F6E00` `001F6E60` `001F7790` `001F86F0` `001F87B0` `001F8860`
        **`001F89E0`** `001F8A70` `001F8B30` `001FAD50` - so the two this row guessed at,
        `001F5D70` and `001FAD50`, are both in.
      - **The caller census splits them three ways.** **Nine are private**, called only from inside
        the span: `001F5330` `001F55F0` `001F57E0` `001F5B80` `001F68E0` `001F7790` `001F86F0`
        `001F87B0` `001FAD50`. **Seven have external callers** and are the public non-virtual
        surface: `001F5D70` `001F6E00` `001F6E60` `001F8860` `001F89E0` `001F8A70` `001F8B30`. **One,
        `001F5C20`, has no caller in the graph at all** and is not explained.
      - **The external callers name the relationship.** `001F4DA0` is
        `CharacterRenderObject_Construct`, so `ResetState` is called by the constructor; `00215320` is
        **`CharacterOrderedObject` slot 1**, a sibling render-object class; the rest are an unowned
        `001BDxxx` group.
      - **Not claimed:** span membership is locality plus an exclusivity control, not a proof that
        each of the seventeen takes `this`. The seven public ones are where a reader should start,
        and `001F5C20`'s absent caller is the loose end.
- [x] **BB-7 (new).** `FUN_001F7790` (3,895 B) is called twice from slot 2 and is larger than every
      vtable method except slot 19. It is the biggest unexamined body in the class's neighbourhood.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BB-7): it is the character material's
      shader-parameter binder. It fills a 0x318-byte binding record with descriptor pointers resolved by name, then writes
      the values and samplers through them.*
      - **Two ways in** (`001F77AF`–`001F783A`).
        - When its fifth argument is non-null, it copies that prebuilt record, `6 × 0x80 + 0x18 = 0x318` bytes, into the
          record `rdi` (`r9`) and skips the lookups.
        - Otherwise it calls `FindShaderParameter` `0018D240(material, name)` **98 times** and stores 92 of the results in
          consecutive 8-byte slots `+0x30`–`+0x310` (`001F783F` onward). That is the `E-10` mechanism
          ([the transform-publish contract](../CONTRACT-character-transform-publish.md), open item 2), extended here to the whole run.
      - **The parameter vocabulary, in lookup order:**
        - `sunIndex`, `lichtDir1`–`6`, `lichtColor1`–`6`, `lichtAmbient`;
        - `AlphaThreshold`, `PS2FogVec`, `clutBank`, `TextureSampler`, `PTAlphaThreshold`, `paletteEnabled`, `indexTex`,
          `palette`;
        - `PS2ZBiasEnabled`, `PS2ZBiasNoGS`, `PS2ZBiasOriginal`, `PS2ZBiasInstance`, `PS2WHMatrix`, `PS2HSMatrix`,
          `InvPS2WHSMatrix`;
        - `fresnelRefEnabled`, `eCameraLightEnabled`, `eTp`;
        - `texAnimEnabled` / `…NormalEnabled` / `…SpecularEnabled`, `origTexBBox1`–`4`, `animTexBBox1`–`4`,
          `animUvMin1`–`4`, `animUvMax1`–`4`, `AnimSampler1`–`4`, `AnimNormalSampler1`–`4`, `AnimSpecularSampler1`–`4`;
        - `NormalMapSampler` / `NormalMapEnabled`, `SpecularSampler` / `specularEnabled`, `cubeMapSampler0`–`3`,
          `cubeMapWeight0`–`3`, `cubeMapEnabled`, `irrCubeMap0`–`3`, `irrCubeMapEnabled`;
        - `RefSampler`, `refractionEnabled`, `refractionPower`, `refractionAlpha`, `RefractionSampler`;
        - `iDebugMode`, `mSpecialShadowFlag`, `m_chrObjHeight`, `m_chrObjFlyingHeight`, `g_txShadow`, `g_txChrAlpha`;
        - and six `…SamplerSampler` names, which are looked up for sampler binding rather than stored.
      - **The write phase** (`001F805D` onward) copies staged values into the material's parameter block (`memcpy`), binds
        the four slots from `+0x1B0` through `001945B0` with a staged value tagged `0xFF` (`001F83FE`–`001F843C`), stores the owner
        at record `+0x00` and clears `+0x08` / `+0x10` (`001F8447`–`001F8452`), then binds the sampler names with values tagged `0x47`.
      - **What it tells a reader.** The character shader is a PS2-emulation material: palette / CLUT textures, the
        PS2 GS matrices and Z-bias, and fog as a PS2 vector. PC additions sit beside them: normal, specular, cube and
        irradiance maps, refraction, and texture animation. Which values each slot receives per frame is not
        followed here.

## 8. Evidence

**Tier 1.** Every claim here is read out of the shipping image.

**The ready flag was established by a write/read asymmetry, not by its name.** All 14 accesses to
`+0x4B4` across the vtable were enumerated: **exactly one is a write**, at offset +2233 of a 2,328-byte
method — the end of setup — and *(corrected 2026-10-02, OPUS: thirteen vtable methods read it, and slot 16 only at its instruction 118 - §8c's overturns)* **all ~~12~~ 13 methods that read it, all but slot 16, do so within their first 12
instructions**. A field with one writer at the end of initialisation and every reader at method entry
is a ready flag; nothing weaker was assumed from the offset or the surrounding names.

**Two independent measurements agree on the object's extent.** Disassembling all 31 methods gives a
highest field offset of `+0x664`; the allocation site gives `0x668`. Neither derived the other.

**The vtable is complete and unambiguous.** All 31 slots come from the
[vtable method index](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md), where an
address is listed only if exactly one class's vtable contains it — so no slot here is a folded body
shared with another class.

**What is deliberately not claimed.** That the class draws characters is inferred from its name, its
GFZ tags (`Presentation.CharacterRenderObject.*`) and its method inventory — **not from reading a draw
call**. ~~No rendering API call has been traced out of these methods~~ *(answered: see §7, BB-1 answered 2026-09-27 - the class draws through `001F5D70`, reached by slot 1 `00215320`+0x4 `jmp`, which calls Phyre's submit at `001F5D70`+0x1C8 `call 0060B980`; 2026-10-02, OPUS)*, and the "what the player sees"
section above should be read as the reading those names support, not as a proven path. **BB-1
tracks exactly this gap.**

**The access census beside this page was widened 2026-09-16** (OPUS-REQ-STRUCT-WIDEN-FOUR-CENSUS-SEED-LISTS).
`character-render-object-accesses.tsv` is regenerated by `Tools/work/STRUCT/cro_census.py`: all 31
vtable slots plus the constructor `001F4DA0` and destructor body `001F51E0` are `this`-taint seeds,
with same-offset register copies only — no `lea`/`add`/`sub` rebasing, matching the committed
generation. The named-function gap was `001F89E0` `CharacterRenderObject_ResetState` (the public
non-slot the BB section already lists): seeded, it contributes 16 rows across `+0x390`–`+0x4B5`, all
writes/clears consistent with a reset. The census ~~is now~~ was then 160 rows *(the TSV now holds 323 rows in 41 functions over 91 offsets - the later `emit_seeded_census.py` generation; recount of `character-render-object-accesses.tsv` 2026-10-02, OPUS)* in 31 functions over 69 distinct
offsets, from 144/30/63. Three committed `cmp` rows were also reclassified write→read — a kind
correction, not a coverage change.

## 8b. Do not confuse with the character render *record array* (2026-09-02)

**A peer pass nearly attached a Movement relationship to this class that does not belong to it.**
The check is recorded here so the next reader does not repeat it, because the two structures are
easy to conflate and the symbol names encourage it.

`Movement_ModifyHeadingSpeedForObjectState` (`00424080`) and `Movement_PublishHeadingState`
(`002E5C10`) both index a large per-character Presentation array whose base pointer the decompiler
renders as `g_pCharacterRenderRecordArray`. **That array is not this class.**

| | `CharacterRenderObject` (this document) | the character render record array |
|---|---|---|
| identity of element | polymorphic object, vtable `00903B68` at `+0` | plain record, `i16` id at `+0` that may be `-1` |
| element size | `0x668` = 1,640 bytes | stride `0x740` = 1,856 bytes |
| allocation | one object at a time via `FUN_00210EC0` | one block of `0x48930` = 297,264 bytes via `FUN_0036A100` |
| allocated by | `FUN_001BD4A0`, the sole construction site | `CharacterRenderSystem_AllocateAndInitialize` (`003325D0`) |
| base pointer | none — objects are held by their owners | `022C6F28` |
| count | not established (**BB-4**) | **exactly 160** — ~~`160 × 0x740 = 0x48830`, the offset at which~~ `160 × 0x740 = 0x48800`, where the tail block starts; `FUN_00426480` writes a trailing dword at `+0x48830` *(corrected 2026-10-02, OPUS: 160 x 1,856 = 296,960 = `0x48800`; the store is `00426480`+0x13 `mov dword ptr [rcx + 0x48830], eax`)* |

**The separating observation, and it is exhaustive.** A memory-operand census over the exact body
extent of all 38,161 functions in the current parent finds:

```
references to the vtable 00903B68 : 2 functions
        CharacterRenderObject_Construct (001F4DA0), FUN_001F51E0
references to the array base 022C6F28 : 636 sites
functions referencing BOTH : none
```

Neither `FUN_001BD4A0` nor `CharacterRenderObject_Construct` touches `022C6F28`, and no writer
anywhere stores a `00903B68`-vtable object into a record of that array. **The intersection is
empty**, so on current evidence the two structures do not meet at all.

That is a *negative*, and it is bounded exactly as stated: it rules out a direct, statically visible
reference in either direction. A pointer stored through an intermediate and read back later would
be invisible to it, exactly as the two-hop limit recorded in audit pass 129. It is not evidence
that the two are unrelated *conceptually* — both plainly serve drawing characters — only that this
class is not the element type of that array.

**Nothing in this document changes.** No claim here rested on the record array, and the amendment
adds no relationship. What the pass did establish, for whoever writes the record array's own
document: its element is `1,856` bytes, there are `160` of them, and the pass dispatcher
`FUN_00332440` selects one of five stages that push authored profiler labels —
**`"display character : preprocessing"`**, **`"display character : shadow"`**,
**`"display character : draw clip"`**, **`"display character : draw objects"`**,
**`"display character : after emission"`** (strings at `00D10A38`, `00D10A60`, `00D10A18`,
`00D10A80`, `00D10AA8`). Those five names are the strongest evidence yet available about what the
character-drawing path actually does per frame, and they are tier 2 — which is one tier better than
anything currently supporting **BB-1**, ~~this document's standing admission that no draw call has~~
~~been traced out of these methods~~ *(answered: see §7 - BB-1 answered 2026-09-27 (`001F5D70` to `0060B980`); 2026-10-02, OPUS)*.

**Status unchanged at `DOCUMENTED`** *(on 2026-09-02; the page's front matter says `status: AUDITED` now - 2026-10-02, OPUS)*. This is a separation check, not a falsification pass; the
document still owes the first named attack on its own claims.

## 8c. Falsification pass 1 - 2026-09-02

**Program state:** parent `2ed8affb...`, snapshot `46f02e26...`, embedded EXE `73461d08...`, ledger
38,161 / 38,003 / 158, verified before any reading.
**Instruments:** the vtable read **directly out of the PE image** by VA to file-offset, not from the
recovered index; capstone disassembly of all 31 method bodies with the extent clamped to the next
function entry and truncated at the first `int3` after a terminator; a displacement scan for
`+0x4B4` across all 38,161 functions; and the call-site census described in
[`../../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md) section 10, including
its measured extent caveat.

### Killer observations named, and hunted

| Claim | What would kill it | Result |
|---|---|---|
| 31 vtable slots | a 32nd slot pointing at a function | **SURVIVED.** Slot 31 reads `7865646E496E7573` - ASCII, not a pointer. The table ends at 31. |
| the 31 addresses and sizes in section 3 | any row disagreeing with the image | **SURVIVED exactly.** 31/31 addresses and 31/31 sizes match. |
| **11,874 bytes of method code** | the sizes summing to something else | **OVERTURNED, it is 11,879.** |
| object is `0x668` = 1,640 bytes | a different allocation size anywhere | **SURVIVED, strengthened.** Confirmed a second time by the sized `operator delete` in slot 0. |
| one construction site in the whole binary | a second caller of the constructor | **SURVIVED.** `001F4DA0` has exactly one call site. |
| exactly two functions reference the vtable | a third | **SURVIVED**, and the second is now identified - BB-5. |
| `+0x4B4`: 14 accesses, 1 write, 13 reads | a different count | **SURVIVED within the vtable**, exactly. |
| **"One writer ... the only method that touches it as a destination"** | a writer outside the vtable | **OVERTURNED.** The constructor writes it too. |
| **"checked at the top of twelve of its thirty-one methods"** | a thirteenth reader | **OVERTURNED.** Thirteen read it. |
| **"reads within the first 12 instructions: 12 of 12"** | a reader deeper in its method | **OVERTURNED, it is 12 of 13.** Slot 16 reads it at instruction 118. |
| highest field `+0x664` | an access at a higher offset off `this` | **SURVIVED** - see the instrument note below. |
| `UpdateViewParameters` calls `tan` and `sqrtf` | either being absent | **SURVIVED.** Both are in its callee set. |
| **BB-1: no draw call has been traced** | finding one | **UPGRADED from an admission to a measured negative.** |

### The three overturns

**11,874 becomes 11,879.** The document's own section 3 table sums to **11,879**; the headline was
short by exactly **5** - the size of slot 29 (`00848340`), the one method that lives outside the
class's `001Fxxxx` cluster. The likeliest cause is that the total was taken over the clustered slots
and the outlier dropped without the exclusion being stated. **The table was right and the headline
was wrong**, which is the same shape as the ScriptVM interpreter's superlative in audit pass 128: a
summary sentence that lost a qualifier its own section carried.

**The ready flag has two writers, not one.** `CharacterRenderObject_Construct` writes `+0x4B4 = 0`
at `001F4EC9` (`sil`, with `esi` zeroed at `001F4DDF` and not reloaded). The census that produced
"one writer" ran **across the vtable**, and the constructor is not in the vtable - so the number was
right for the set it measured and the sentence generalised past it. **The conclusion is unharmed and
the evidence is better:** an explicit zero at construction supports "ready flag" more strongly than
relying on the allocator's zero-fill would, and nothing clears the byte after setup.

**Thirteen readers, not twelve, and one of them is not a gate.** Slot 16
(`SubmitMaterialsWithFadeMode`) reads the flag at instruction **118**, inside a submission loop, as
one condition among several in a per-element skip test. The stated figure "12 of 12" was also
internally inconsistent with the "13 reads" two lines above it in the same block - **the block
disagreed with itself and had stood unchecked**, which the evidence standard already records as its
own tell.

### BB-1, upgraded

The 31 methods call **46 real functions** at one hop. The complete named set is CRT and nothing
else - `memcpy` (15 sites), `memset`, `sqrtf`, `tan`, `free`, `_alloca_probe`,
`__security_check_cookie`, `__report_rangecheckfailure`, `_guard_check_icall`. The remaining 37 are
untagged internal functions, none owned by any subsystem. **No graphics API entry point appears
anywhere in the set.**

That does not prove the class never causes a draw; it bounds the claim precisely: **whatever draws,
it is not reached in one call from these methods.** Section 1 should still be read as the reading
the names support. Where to look next is now specific - the five authored stage labels recorded in
section 8b belong to a *different* structure's dispatcher and are the strongest evidence in reach
about what the character-drawing path actually does per frame.

### What was tried and failed to break it

- **Read the vtable out of the image rather than trusting the recovered index.** All 31 rows
  reproduced, addresses and sizes. The index was not the weak link.
- **Looked for a second construction site three ways** - callers of the constructor, other loads of
  the immediate `0x668`, and other references to the vtable. The only other real-code `0x668` is the
  matching sized delete, which *confirms* the size rather than contradicting it.
- **Tried to find a `+0x4B4` writer outside the class.** The binary-wide scan returns 39 accesses in
  33 functions, but those outside the class are on different structures: seven
  `CharacterRenderRecord_*` functions (the 1,856-byte record array - see section 8b) and four Audio
  functions. One reads `+0x4B4` as a **word** and one writes a **float** there, which is decisive
  that they are different types. **Only the constructor survived as a genuine second writer.**
- **Attacked the layout extent and caught my own instrument first.** A scan for the highest
  displacement on any non-`RIP` base returned **`+0x10D9`**, which would have overturned `+0x664` -
  but it was on `rax`, loaded from a *different* object inside slot 16. Re-run with a bounded
  `this`-tracker (`rcx` at entry, plus registers receiving a direct `mov` from a tracked register,
  invalidated on any other write), the highest displacement is **`+0x664`**, and the next four are
  `+0x654`, `+0x634`, `+0x624`, `+0x614` - a coherent tail. **A scan that is too broad invents a
  finding exactly as readily as one that is too narrow misses one.**
- **Re-checked for banned evidence.** The one unwind funclet that loads `0x668`
  (`Unwind@00897c10`) was noted and **excluded**; no `.pdata`, `.xdata`, unwind record or EH map
  appears in any reasoning here. The RTTI complete-object-locator pointer at `vtable - 8` was read
  but supports no claim.

### Crossref

`audit_crossrefs.py` reports **zero** findings for this document - no `GHOST ADDRESS`, no
`BODY DRIFT`, no `CLASSIFICATION`, no `UNACCOUNTED NEIGHBOUR`.

### Status

Three claims overturned, one sharpened, **BB-5 answered**, **BB-1 narrowed to a measured negative**,
and two new questions opened (**BB-6**, **BB-7**). The headline count, the object size, the
construction uniqueness, the vtable inventory and the layout extent all survived a named attempt to
destroy them. **This document has now had its first falsification pass.**

## 9. Related

- [`../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md)
  — the index this class was selected from; 117 further game-specific classes remain unread.
- [`../Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md`](../Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md)
  — the reflected render parameters that material propagation would carry.
- [`../../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md)
  — §8f there carries the same separation from the other side: the character render *record array*
  it documents is a different structure, and Movement writes into that one, not into this class.

## Slot 13 (`001FB120`) read — the double-buffered transform publish

The slot table above lists `001FB120` with an empty description. It is read here: **105 instructions,
48 of them `movups`, no loops**, ending `ret` at `001FB30F` with no `jmp` leaving the extent.

### Two banks, chosen by a global parity byte

```asm
001FB1AC  call  0x189120                     ; a shared accessor
001FB1B1  cmp   byte ptr [rax + 0x1c], 0
001FB1BA  je    bank_A
```

| | scalars | three 4×4 matrices |
|---|---|---|
| **bank A** (byte == 0) | `entry + 0x08`, `entry + 0x10` | `this + 0x4C4` … `this + 0x583` |
| **bank B** (byte != 0) | `entry + 0x0C`, `entry + 0x14` | `this + 0x584` … `this + 0x643` |

**`0x584 − 0x4C4 = 0xC0` = 192 = exactly three 64-byte matrices**, so the two banks are contiguous,
equal-sized and adjacent — and the two scalar slots are **four bytes apart** in the same pattern.

> **Character transforms are double-buffered, and the bank is chosen by one byte reached through a
> shared accessor.** Everything this slot publishes exists in two copies; **which one is "current"
> is not this object's decision.**

Each matrix is copied with **four `movups`** from a pointer passed on the stack — **three source
pointers, three destinations, twelve 16-byte moves per bank**, fully unrolled.

### An enable gate and a movement flag

```asm
001FB126  movzx eax, byte ptr [rcx + 0x4b4]
001FB138  test  al, al
001FB13A  je    return                       ; publishes nothing at all
```

**`this + 0x4B4` gates the whole function.** With it clear, no matrix and no scalar is written — **the
previous contents of both banks stand.**

```asm
001FB162  ucomiss xmm7, xmm0                 ; xmm0 = 0
001FB170  ucomiss xmm6, xmm0
001FB175  mov     edx, ecx                   ; both zero -> 0
001FB179  mov     edx, 1                     ; otherwise  -> 1
```

**Two float arguments are compared against zero, and a flag is written only if both are zero.** The
`jp` guards mean **a NaN takes the non-zero branch** — an unordered comparison counts as "not zero".
That flag and a second one (`r8d == 0`) are stored through a **double indirection**:
`[entry + 0xE0]` and `[entry + 0xE8]` each yield a pointer whose `word +0x10` is added to a base held
in `r9` — so **the two flags land in a third structure, not in the entry.**

### The entry array

`entry = [this + 0x58] + index * 0x318` — **an array of `0x318`-byte records**, indexed by the second
argument.

### What is not established

- [x] **UQ-200.** What the accessor's `+0x1C` byte counts. It selects the bank and **nothing here
      writes it.** *Narrowed 2026-09-15 (OPUS): **the field is a WORD, it is zero-initialised, and
      the bank test reads only its low byte.***
      - **The accessor is an 8-byte getter for a singleton.** `00189120` is
        `mov rax, [01F7F598]; ret`. A whole-image census of that slot (positive control `022D8EB4`,
        26 references, so absence is meaningful) returns **6 references in 4 functions**: the
        getter, a lazy creator `00189000`, and two readers `001862B0` and `00187950`.
      - **The singleton is `0xDD8` = 3,544 bytes**, allocated at `00189034 mov ecx, 0xdd8` through
        `00210EC0` and constructed by **`00184F20`** (`00189061`).
      - **`+0x1C` IS A WORD, AND THE CONSTRUCTOR ZEROES IT.** `00184F54 xor esi, esi` then
        `00184F56 mov dword ptr [rcx+0x18], esi` and **`00184F59 mov word ptr [rcx+0x1c], si`**. The
        constructor also sets `+0x00` word `0`, `+0x02` byte `0`, `+0x08` = `rdx`, `+0x10` = `r8`.
        **Nothing counts into `+0x1C` at construction — it starts at zero.**
      - **But the bank test reads a BYTE.** `001FB1B1 cmp byte ptr [rax+0x1c], 0`. On a
        little-endian machine that is the low 8 bits of the word, so **a value whose low byte is
        zero but whose high byte is not would select the same bank as a true zero.** The page's
        word *“byte”* describes the read correctly and the field incorrectly.
      - **Still open, and narrower:** what raises it from zero. **No writer other than the
        constructor's zeroing was found** — none of the four functions that reference `01F7F598`
        writes `+0x1C`, so whatever increments it reaches the object through a register obtained
        elsewhere. **A displacement scan is not usable here:** `0x1C` is far too common an offset
        for displacement identity to mean object identity.
      *Narrowed again 2026-09-26 (FABLE, Claude Opus 5.5): a receiver census finds a second writer of `+0x1C`, and it
      also writes zero; the uploader's `+0x1D` is a per-pass copy.* Static.
      - **The census.** It follows the object instead of the displacement: every call made with `rcx` set to the
        getter's result gives 47 functions that receive the singleton as `this`. Each was scanned for a write to its
        own `+0x1C`/`+0x1D`.
      - **The second writer writes 0.** It is a method of the singleton, of 1,083 bytes, called once with it as `this`. It runs
        its body only when the byte is zero (`cmp byte ptr [rcx+0x1c], 0` / `jne` at its entry), and it stores 0 there
        again at the end. ~~Within the census nothing writes a non-zero value. So the writer `001FB120`'s bank test sees
        0 and takes the same arm on every call — unless a writer outside the census, one holding the pointer some
        other way, raises it.~~ *Corrected later the same day (FABLE, Claude Opus 5.5): the census keyed on `call` and missed two
        tail-jump forwarders, and one of them writes 1. See the answer below.*
      - **`+0x1D` is set per pass.** A one-instruction setter (`mov byte ptr [rcx+0x1d], dl`) has a single caller,
        and that caller passes byte `+0x20` of the pass object it received. So the uploader `001FAD50` picks its bank by
        the current pass, ~~while the writer's byte stays 0~~ *(corrected: it does not stay 0; see the answer below)*.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): `+0x1C` counts nothing. It is a two-state pass selector.**
      Control: [`singleton_escape.py`](../../_index/candidates/uq200-singleton-escape/singleton_escape.py) (7 checks,
      FAILS 0). It follows the singleton pointer to a fixpoint, not one hop, and reaches 105 functions. Each binding
      survives copies and spills and dies on redefinition and across calls. It also follows a slot that holds the
      pointer when that slot's address is passed on.
      - **Exactly four instructions write `+0x1C` / `+0x1D`** through the pointer, besides the constructor's zeroing:
        - `00185A1D` writes **1**;
        - `001860E6` writes 0;
        - the method that runs only at 0 writes 0;
        - the per-pass `+0x1D` setter.
      - **The 1 was missed because it is reached by a tail jump.** The forwarder `001821F0` is "if the singleton
        exists, `jmp` to `00185A10`"; that method sets `+0x1C = 1` and enqueues a command built from `this + 0x358`.
        Its sibling `00182340` jumps to `001860E0`, which sets `+0x1C = 0` and enqueues a command built from
        `this + 0x690`. ~~`003829D0` calls the two back to back (`00382B21`, `00382B28`).~~ `003829D0` calls one of the two, chosen on `00259FA0`'s result *(corrected 2026-10-02, OPUS: `003829D0`+0x14D `test eax, eax` and `003829D0`+0x14F `je` to the `00182340` call, else `call 001821F0` and `jmp` past it)*.
      - **Each pass command captures the byte.** The command constructor `001F1E80` reads `+0x1C` (`001F1EB7`) and
        stores it at the command's `+0x20` (`001F1EBB`). That `+0x20` is the byte the per-pass setter copies into
        `+0x1D`. So the uploader's bank is stamped per pass: 1 for the `+0x358` pass and 0 for the `+0x690` pass.
      - **Not established:** when the slot-13 writer, which reads the live `+0x1C`, runs relative to those two
        enqueues. It has no direct caller, so which bank it fills in a given frame is not read here, and is not
        queued.
- [x] **UQ-201.** What the three matrices are. Their **count, size, sources and both destinations** are read; their
      roles are not.
      **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): they are the shader's three PS2 transform parameters, and the
      two scalars are its two Z-bias values.** Only two functions touch the banks. `001FB120` writes them, and `001FAD50`
      reads them into the material's parameter block. For the binding record at `[this + 0x58] + slot × 0x318`,
      `001FAD50` copies each matrix into the parameter the record's slot names. The names come from OPUS's
      [binding-slot table](../Character-Rendering/shader-binding-record-0x318-slots.tsv), which pairs each
      `FindShaderParameter` lookup with its store:

      | bank A | bank B | binding slot | shader parameter |
      |---|---|---|---|
      | `+0x4C4` | `+0x584` | `+0x100` | `PS2WHMatrix` |
      | `+0x504` | `+0x5C4` | `+0x108` | `PS2HSMatrix` |
      | `+0x544` | `+0x604` | `+0x110` | `InvPS2WHSMatrix` |
      | entry `+0x08` | entry `+0x0C` | `+0x0F0` | `PS2ZBiasOriginal` |
      | entry `+0x10` | entry `+0x14` | `+0x0F8` | `PS2ZBiasInstance` |

      *Evidence.* Bank B: `001FADC1`–`001FAE6C`. Bank A: from `001FAEBC`. Each copy goes to
      `paramBlock + word[[slot] + 0x10]`. The uploader chooses the bank by byte `+0x1D` of `00189120()` (`001FAD8B`).
      The writer `001FB120` chooses its own bank by byte `+0x1C` (`001FB1B1`) — two flags, not one. *(Corrected
      2026-09-25, FABLE, Claude Opus 5.5, on `OPUS-NOTE-FABLE-UQ201-WRITER-BANK-BYTE`; this said "as for the writer".)* `001FAD50` publishes nothing while `this + 0x4B4` is clear, the same gate as `001FB120`.

      *What the names mean* is the shader's vocabulary, not a reading of the maths. **WH** and **HS** read as
      *world→homogeneous* and *homogeneous→screen*, the PS2 GS pipeline's two stages, with the third being their
      composite's inverse. That is an interpretation of the names, and no matrix was multiplied out to confirm it.
- [x] **UQ-202.** What the two flags mean, or what structure `r9` bases them in.
      **ANSWERED 2026-09-21 (OPUS).** The flags are the shader parameters **`PS2ZBiasEnabled`**
      (record `+0xE0`) and **`PS2ZBiasNoGS`** (record `+0xE8`), named by pairing each of the
      binder's `FindShaderParameter` lookups with the store that consumes its result — *not* by
      counting §BB-7's vocabulary list, which cannot be done safely because 98 lookups produce
      only 92 stores. Full map: `shader-binding-record-0x318-slots.tsv`.
      **`r9` is the shader's parameter data block**, `*( *(entry + 0x00) + 0x08 )`: `001FB165`
      loads the record's `+0x00` and `001FB168` takes that object's `+0x08`. The record's `+0x00`
      is the binder's **first** argument (`001F8452`), whereas the descriptors resolved against
      its **second** (`mov rcx, r15`) — two different objects. Both call sites `001F70F3` and
      `001F74F6` pass argument 3 as `[arg1 + 8]`, i.e. that same data block. So argument 1 is a
      two-field pair: `+0x00` the shader owning the parameter table, `+0x08` the data the
      descriptors' `word +0x10` offsets index into.
- [x] **UQ-203.** What `this + 0x4B4` represents beyond gating this publish.
      **ANSWERED (negative) 2026-09-21 (OPUS): nothing.** A fixpoint receiver census seeded on
      the vtable reached **45 functions** — wider than the 31 slots §5 enumerated — and returned
      **the same 14 accesses, 1 write and 13 reads** *(scope named 2026-10-02, OPUS: within that census's reach; image-wide the byte accesses at `+0x4B4` are 19 - two writes, `001F4DA0`+0x129 and `001F6E70`+0x8B9, and 17 reads in 16 functions, all in the class's bodies; CONTRACT-character-render-object.md R-3 / R-4)*, so that count now has a second instrument
      behind it. Tracking each load to its first consumer, **12 of the 13 reads are `test al, al`
      into a branch**. The 13th is slot 27's getter `001F86D0`, which returns the byte — and that
      getter has **no direct caller anywhere in the image**, its address appearing exactly once,
      at `00903C40` = vtable + 0xD8 = slot 27. All 18 `call [reg + 0xD8]` sites were enumerated;
      the five in this neighbourhood each pass an argument this zero-argument getter does not
      take (`rdx`, `edx`/`r8d`/`r9`, `xmm1`) or dispatch on a global singleton. **Nothing
      accumulates, stores, forwards or compares the byte.** *Residual:* receiver types at those
      18 sites were not proven, only their argument shapes read.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Resource — CLIENT and SERVICE.** A 129-byte function this page cites is called by Resource bodies of 265, 384 and 683 bytes. A 2,924-byte one calls a 22-byte Resource helper.
- **ActorEntity — CLIENT.** The same 129-byte function is called by `ActorResource_BeginPrimaryPayloadLoad` and a 3,882-byte actor body.
- **Audio - SERVICE (1 edge).** `00187950` reaches bodies filed to Audio: `00182E80` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (6 edges).** `00189000`, `0018B4E0`, `001EC560` are called by bodies filed to CoreRuntimeScheduling: `0017CCD0`, `0017D000`, `001E0590`, `001EC760` (+1 more); `00187950` reaches bodies filed to CoreRuntimeScheduling: `001A1470` - shared machinery across the layer boundary, no shared ownership.
- **Developer - CLIENT (1 edge).** `001EBA40` is called by bodies filed to Developer: `001C6320` - shared machinery across the layer boundary, no shared ownership.
- **Input - MECHANICAL (25 edges).** Fan-in on the shared accessor `0063A990`. All 25 edges run through it - one accessor’s spread, not a per-caller relationship.
- **Movement - CLIENT (2 edges).** Movement_PublishHeadingState (`002E5C10`), Movement_ModifyHeadingSpeedForObjectState (`00424080`) are called by bodies filed to Movement: Movement_ComputeDeltaFromHeadingSpeed (`002E4380`), Movement_UpdateActorFrame (`002E5030`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (2 edges).** `002ED6F0`, `0036A100` are called by bodies filed to Script_VM_Native_Bridge: `003580C0`, `0050D8F0` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (6 edges).** `001EC560`, `0036A100` are called by bodies filed to WorldAreaField: `001EDCD0`, `00267930`, `003319D0`, AreaArd_LoadOrUnloadFieldResource (`003EA820`); `001ED240` reaches bodies filed to WorldAreaField: FieldData_GetVariable0 (`00265270`), WorldTransition_GetTransitionFieldId (`00314910`) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (1 edge).** `00314910` reaches `SaveImage_GetPersistentPayloadBase` (`002EF2B0`).
- **UI - CLIENT (2 edges).** UI bodies `0018EEE0` and `0029C530` call `001A1470` and `00314910`.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Platform — SERVICE.** `0019CC50`, owned by that layer, calls this page's `006336E0` at
**`0019CCC9`**. **The crossing is that the platform layer consults this page's entry, not that
this page owns anything in Platform.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**StoryEvent — CLIENT.** `FUN_001ed240`, owned by that layer, calls `001EC560` on this page. That caller is a 2,192-byte cutscene-override table: it matches the current area id against hard-coded values such as `0xD70` and `0xD48`, the story-progress word selected by `[01DFE40C]` out of `01F832B0` against a step number, the model's name against string literals such as `g0999` and `c1004`, and the animation time against a window, returning a small override index when all four agree; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).


## Interior citations — frontier hubs `0042EF90` / `00426220` (2026-09-17, SWE2-EC7)

- `0042EF90` (`CharacterRenderHierarchy_TraverseIndexDepthFirst`) — 105 B, 43 frontier callers.
  Interior verified: [`0042EFB7`](../../_index/ADDRESS-INDEX.md) is `imul rbx, rax, 0x740` — the
  body is a recursive depth-first walk over the 0x740-stride record table based at
  `[rip+0x1e97f63]` (~~`02095210`~~ `022C6F28` *(corrected 2026-10-02, OPUS: the displacement counts from the next instruction, `0042EF90`+0x35, so the target is the pool pointer `022C6F28`)*): per node it calls the visitor `rsi(record, r8)`, recurses on
  `word[rbx+8]` (first child), and iterates `word[rbx+0xA]` (next sibling); `0xFFFF` terminates
  each link. The `0x740` stride is the character-render record — the walk is over ~~this page's own~~
  ~~table~~ the record array, which §8b shows is not this class *(corrected 2026-10-02, OPUS: §8b, 2026-09-02)*.
- `00426220` — 183 B, 40 frontier callers. Interior verified: [`00426235`](../../_index/ADDRESS-INDEX.md)
  is `test dword [rcx+0x284], 0x4000000` — a pair-eligibility predicate over two records: returns
  1 early when `rcx==rdx` is false while `+0x284` bit 26 is clear and `word[+0x2F8]==0xFFFF`; when
  bit 27 is set it additionally requires `word[+0xCC] < 0x1000` and a nonzero `004232D0` probe;
  otherwise it slides a six-byte window across `[rbx+0x3C..0x41]` against `[rdi+0x3D..0x42]` and
  returns `byte[rdi+0x3C]==0x62` when the records' `+0x3C` kinds differ.

NOT claimed: the meaning of bits 26/27 at `+0x284` or the six-byte comparison's field — the
predicate's truth conditions are measured, its callers' intent is not.

## `+0x78 .. +0x38F` is one 792-byte construction unit (2026-09-18, OPUS)

776 of this type's 894 unknown bytes sit in two spans the store carried as separate gaps,
`unobservedSpan0080` (144 B) and `unobservedSpan0118` (632 B), each annotated *"inside the record
by extent, no censused access"*. **They are not two gaps. They are the interior of one region that
the constructor initialises as a single unit**, and the two named pointers between them are members
of that region rather than its neighbours.

`001F4DA0 CharacterRenderObject_Construct` does this:

```
001F4F00  xor   edx, edx                  ; fill 0
001F4F02  mov   r8d, 0x318                ; 792 bytes
001F4F08  lea   rcx, [rsp + 0x30]
001F4F0D  call  00861EC0                  ; memset(stack buffer, 0, 0x318)
001F4F12  lea   rcx, [rdi + 0x78]         ; destination: this+0x78
001F4F16  lea   rax, [rsp + 0x30]
001F4F1B  lea   r8d, [rsi + 6]            ; 6 iterations - rsi is 0
001F4F20  ...   8 x movups, 0x80 per iteration, jne 001F4F20
001F4F72  ...   tail: movups 0x10 + mov qword 0x8
```

`rsi` is zero: `xor esi, esi` at `001F4DDF` is the **only** write to it anywhere in the body, so
the count is exactly 6. `6 * 0x80 + 0x18 = 0x318 = 792`, which is precisely the size memset into
the staging buffer — the copy neither overruns nor falls short of what was cleared.

Three things follow, and the extent is checkable arithmetic rather than a reading:

| | |
|---|---|
| the region | `this+0x78` through `this+0x38F` |
| its end | `0x78 + 0x318 = 0x390` — exactly `auxVec36Begin`, the next named field |
| its contents | `writeBufferPtr78` 8 + gap `+0x80` 144 + `writeIndexSourcePtr110` 8 + gap `+0x118` 632 = **792**, with nothing left over |

> **IDENTIFIED 2026-09-26 (OPUS): the unit is the object's own `CharacterShaderParamTable`.** The binder
> `001F7790`'s first call site passes `table = object + 0x78` (`001F70DE`-`001F70F3`). So these 792 bytes are the
> same shader-parameter handle table as the `+0x58` vector's elements (slot map:
> [`shader-binding-record-0x318-slots.tsv`](shader-binding-record-0x318-slots.tsv)): `+0x78` is its data-block owner,
> and `+0x110` its `lichtAmbient` handle. The type is declared in `_types`; see
> [`opus-character-shader-param-table.md`](../../_index/candidates/opus-character-shader-param-table.md). The
> paragraph below is kept as written on 2026-09-18.

**What this does NOT establish is what any of the 776 bytes mean.** Zero-initialisation is a
statement about extent and lifetime, and nothing more. The two spans stay `DISCOVERED` / `UNKNOWN`
in the store and the byte count is unchanged. What moves is the shape of the question a reader
inherits: **one owner for one 792-byte block initialised in one operation**, not four unrelated
things between `+0x78` and `+0x390`.

### The regularity that would have manufactured a layout

A `this`-taint scan over the **48 bodies proved to take this object** — the 31 slots of vtable
`00903B68`, the 2 bodies that install that vtable, and 15 more reached by a handoff that passes
`this` itself in `rcx` — reports nine offsets in the `+0x80` span at an exact `0x10` stride:
`+0x88, +0x98, +0xA8, +0xB8, +0xC8, +0xD8, +0xE8, +0xF8, +0x108`.

**Those are not nine fields.** They are the unrolled copy's `movups` displacements off
`rcx = this+0x78`, and reading them as a lattice of 16-byte elements would have written a
completely fictional layout into a type that is 54.5 % unknown — with the stride, the count and the
alignment all looking like corroboration. It is recorded here because the next scan of this region
will produce the same nine numbers.

### How far the negative reaches, and where it stops (amended 2026-09-18)

`BattleUnit`'s equivalent span was closed to *"read by nothing statically reachable"* by six
routes. **This type's negative does not reach that far, and the difference is worth naming rather
than leaving for a reader to assume symmetry.** Both remaining routes were measured:

- **Escaping pointers — closed.** Over the 48 member bodies, an object address is stored to memory
  at five displacements: `+0x000` (`001F4DA3`, `001F6E8C`, `001F8D4F`, `001FA182`), `+0x008`,
  `+0x030`, `+0x058` and `+0x390` (`001F4DD7`, `001F4E05`, `001F4E2D`, `001F4E58`). **Every one is
  a stack store** — the argument home slot in a prologue, ordinary spills, and the constructor's
  repeated `[rsp+0x368]`, which is the same slot rewritten as each sub-object is built, i.e. the
  unwind cursor. None of them puts this object's address into another structure, so there is no
  escape route into the gaps.
- **Indirect dispatch — ~~OPEN, and it is the real limit~~ CLOSED, 2026-09-19.** This class does
  pass `this` to virtual calls, which a register closure stops at. Resolving them was a smaller job
  than it looked and the answer inverts the conclusion: see below.

~~So the correct reading of the six spans is *"unobserved by every direct-call route, with virtual
dispatch not yet followed"* — not *"nothing reads them"*.~~ **Superseded.** Every indirect target
is now resolved, and none of them is a route into the gaps.

**The remaining work is small and enumerable, which is the useful part.** Of the six displacements
with indirect targets, **only `+0x000` passes the object itself**; the other five
(`+0x020`, `+0x048`, `+0x050`, `+0x070`, `+0x3A8`) pass a **sub-object** — the embedded allocators
and vector heads — and every one goes to the same `[rax+0x18]` / `[r9+0x18]`, the allocator's own
slot. A callee that receives `this+0x20` cannot reach `+0x118` through it. So the open set is the
six targets at `+0x000` and nothing else:

```
qword ptr [r10 + 0x98]    qword ptr [rax + 0x50]    qword ptr [rax + 0x68]
qword ptr [rax + 0x70]    qword ptr [rax + 0xa0]    qword ptr [rip + 0x6c8ca4]
```

**One of the six is already disposed of, and not the way it looks.** `[rip+0x6c8ca4]` resolves to
the slot `008C2CC8`, which holds `0000000001CCEFCA` — **not a valid address anywhere in this
image**, so it is an unbound import thunk near the start of `.rdata`, and the three call sites
(`001FA01E`, `001FA039`, `001FA053`, all in `001F9FF0`) are calls out to a DLL. `rcx` still held
`this` there because nothing had overwritten it, **not because it is an argument**.

### The other five are this object calling its own virtual methods (2026-09-19, OPUS)

They are not an open set. **All five live in one function**, `001FA3D0`
`CharacterRenderObject_SubmitMaterialsWithFadeMode`, and every one has the same three-instruction
shape:

```
001FA609  mov  rax, qword ptr [r14]     ; rax = r14's VTABLE
001FA602  mov  rcx, r14                 ; the callee's `this` is r14
001FA614  call qword ptr [rax + 0x70]
```

`r14` is assigned exactly once in the whole 1,073-byte body — `001FA411 mov r14, rcx` — so **`r14`
is this function's own first argument**, the `CharacterRenderObject` itself. The dispatch is
therefore through **this class's own vtable `00903B68`**, and the offsets resolve to slots that are
already the closure's seed:

| call site | operand | slot | target |
|---|---|---|---|
| `001FA706` | `[rax+0x50]` | 10 | `001F8C00` |
| `001FA748` | `[rax+0x68]` | 13 | `001FB120` |
| `001FA614` | `[rax+0x70]` | 14 | `001FA0A0` |
| `001FA6C9` | `[r10+0x98]` | 19 | `001F8D10` |
| `001FA6F3` | `[rax+0xA0]` | 20 | `001FA0E0` |

**Every one of those five bodies is already a member and already scanned** — they are vtable slots,
and the vtable is where the member set starts. So following the dispatch adds nothing to the set
and cannot add an access to the gaps.

**This upgrades the negative rather than qualifying it.** The earlier passage called virtual
dispatch "the real limit" and rated this type's silence weaker than `BattleUnit`'s. That was
over-cautious: the only indirect targets are an unbound import thunk where `rcx` was stale, and
self-dispatch into methods the scan had already read. **The six spans are unobserved on every route
this project can measure — apart from the constructor's block copy into `+0x80`, which the section
above accounts for and which is nine `movups` displacements rather than nine fields.** That is the
same standing `BattleUnit +0x298` has, subject to the same limit: a route computed in a form the
taint does not model, or one that exists only at run time, would look identical.

*(The remaining `[rax+0x18]` / `[r9+0x18]` targets at `+0x020`, `+0x048`, `+0x050`, `+0x070` and
`+0x3A8` are unchanged and were never part of this question: they receive a **sub-object**, not
`this`, so they cannot reach `+0x118` whatever they dispatch to.)*

That is worth stating as a property of the instrument and not just of this row: **a recorded
handoff is an upper bound.** The scan reports any object-tainted value sitting in an argument
register at a call; whether the callee *reads* that register is a separate question. It makes
handoffs safe to use for ruling things **in** and wrong to use for counting.

The member set matters as much as the result. An earlier pass took every listed body in the class's
address neighbourhood `[001F4000, 001FC000)` — 108 of them — and reported hits at `+0x80`, `+0xA8`,
`+0x1C0`, `+0x1E0` and more. **Every one of those was worthless**: most bodies in that range take
some other object in `rcx`, so what they touched was their own first argument. Address adjacency is
not membership; §8b of this page already refuses that inference for the record array, and it is no
better for methods. Against the built set, all six gap spans are **still unobserved** except by the
constructor's block copy — and the scan's control, the known `+0x3B0/+0x3C0/+0x3D0` vector
handoff (`+0x3B0` in, `+0x3C0`/`+0x3D0` out), is rediscovered, so the negative is a measurement
rather than a silence.

## SWE2-EC7-34 update (2026-09-19) - `001F57E0`

`001F57E0` (928 B) is the render-object init - `0x2AAAAAAAAAAAAAAB` divide-by-six magic, a `[rbx+rbx*2]*8` 24-byte stride, `001F4C00`/`00215310`/`001F5B61`/`001F5A24`. Interior anchor `001F58A6` (an `001F4C00` call).

## SWE2-EC7-35 update (2026-09-19) - `001F5330`

`001F5330` (698 B) is a hash-keyed lookup - the `0xa57eb50295fad40b` hash constant, `001F4B30`/`001F4A80` pair. Interior anchor `001F53ED` (an `001F4B30` call).

## `+0x118` holds 632 bytes of heap garbage, and that is a stronger statement than "unknown" (2026-09-19, OPUS)

*A bulk-write sweep across the store established that **93 % of this database's declared-unknown
bytes are zero-initialised** — cleared wholesale by a constructor, a reset or an allocator. The
residue, at most 3,862 bytes, is genuinely **undefined**. **`unobservedSpan0118` is the largest single
piece of it**, and this object is the reason: it is one of the few that is never cleared at all.*

**Four routes, all negative, and together they exhaust the question:**

| route | result |
|---|---|
| the allocator | `001BD527` `mov ecx, 0x668` then `00210EC0`, which is `or r8d, -1` / `xor edx, edx` / `jmp 0085E730` — a tail jump to **Bullet's `malloc`**, not a `calloc`. **The block arrives unzeroed.** |
| the base constructor | `00212C70` is **fourteen bytes**: `lea rax, [rip+...]` / `mov [rcx], rax` / `ret`. It installs a vtable pointer and nothing else. |
| the constructor | `CharacterRenderObject_Construct` (`001F4DA0`, 516 B) initialises **field by field** — `[rdi]`, `+0x8`, `+0x28`, `+0x30` and so on. **No `memset` of `this`.** |
| the whole image | **no `memset` with a literal length of `0x668` exists anywhere in the executable.** Zero sites. |

So the 632 bytes at `+0x118` are **allocated from an unzeroed heap, ~~never cleared~~ then cleared with the rest of `+0x78`..`+0x38F` *(corrected 2026-10-02, OPUS: `001F4DA0`+0x16D `memset(stack buffer, 0, 0x318)` and the copy to `this+0x78` at `001F4DA0`+0x172..+0x1DC, quoted above)*, never written
individually, and never read**. ~~They hold whatever the allocator last left there.~~ They hold zero.

### Why this is worth stating separately from "unknown"

*Unknown* says nobody has read the bytes. *Undefined* says **the engine itself does not care what is
in them** — and that is a licence, not a gap. A reimplementation may put anything at `+0x118`,
including zero, and still match the engine, because the engine's own content there is whatever the
previous occupant of that heap block wrote. **The one thing a reimplementation must NOT do is assume
they are zero**, which is exactly what it would infer from the other 93 % of this database's unknown
space — where the assumption is correct.

**NOT CLAIMED:** that the bytes are unused *forever*. They are unread on every route this corpus has,
which bounds what is observed and not what is possible; a reader reached only through an indirect
call would not appear in any of them. What is claimed is narrower and firmer: **nothing initialises
them**, and that was settled by exhaustion rather than by absence of evidence — the `0x668` sweep
covers the whole image, not a closure.

*The other two `CharacterRenderObject` spans, ~~`+0x80` (144 B) and~~ `+0x420` (96 B) *(corrected 2026-10-02, OPUS: `+0x80` lies inside the block the constructor zeroes at `001F4DA0`+0x172..+0x1DC; `+0x420` lies outside it)*, are in the same
position for the same reasons; `+0x118` is simply the largest.*

## SWE2-EC7-41 update (2026-09-19) - `001F5C20`

`001F5C20` (336 B) is a character-render body - `008C5FE0`/`01F44830`, `00808F10`/`00628570` pair/`00861EBA`/`006215A0`/`00808C40`. Interior anchor `001F5C2E` (an `00808F10` call).

## SWE2-EC7-43 update (2026-09-19) - `001862B0`

`001862B0` (295 B) is one of the two slot readers the page names - `01F44830`/`01F7F598`, `005FEB30`/`00808C40`; `008C5F6C`/`008C5FE0` refs. Interior anchor `0018638E` (a `005FEB30` call).

## SWE2-EC7-50 update (2026-09-19) - `001F8A70`

`001F8A70` (182 B) is a body - `001E3D80`/`001F57E0`/`002152E0`/`00215310`. Interior anchor `001F8AC2` (an `001E3D80` call).

## SWE2-EC7-53 update (2026-09-19) - `001ABF50`

`001ABF50` (1084 B) is the character-render record op the page names (`+0x3C0`/`+0x3D0` at 16-byte stride) - `00861F14` pair, `001AB0F0`, `001AA3D0` plus `001AD470` text target. Interior anchor `001AC08C` (a `00861F14` call).

## SWE2-EC7-54 update (2026-09-19) - `001AB0F0`

`001AB0F0` (462 B) is a character-render record helper - `001EDF00` single call plus three vcalls, `008C2A40` import. Interior anchor `001AB130` (a `001EDF00` call).


## SWE2-EC7-54 update (2026-09-19) - `005FEB30`

`005FEB30` (312 B) is one of the two slot readers the page names - `00600B30` single call plus one vcall. Interior anchor `005FEB8A` (a `00600B30` call).

## SWE2-EC7-55 update (2026-09-19) - `001AA3D0`

`001AA3D0` (281 B) is a character-render record helper - `001AA3D0` self-recursive call plus two vcalls. Interior anchor `001AA4B4` (a `001AA3D0` call).

## SWE2-EC7-56 update (2026-09-19) - `001E3D80`

`001E3D80` (203 B) is an indirect-only `0x18`-stride element move-and-destroy - `[r9+rbx+8]`/`+0x10` triple moves then `call [rax]` per record. Interior anchor `001E3DF8` (the `call [rax]` destroy).


## SWE2-EC7-56 update (2026-09-19) - `001F4B30`

`001F4B30` (195 B) is a call-free `0x80`-stride SIMD record copier - eight `movups` per record, count 6, linked via `[r10]`. Interior anchor `001F4B76` (the first record store).

## SWE2-EC7-58 update (2026-09-19) - `001F4A80`

`001F4A80` (167 B) is a call-free `0x80`-stride record copier - 6-iteration `movups` pairs (`ecx`=6, `sub r9,0x318`). Interior anchor `001F4AC1` (the first `movups` store).



## SWE2-EC7-65 update (2026-09-19) - `001F89E0`

`001F89E0` (137 B) is a call-free record defaults - `+0x498`/`+0x4A4`, `+0x4A8`/`+0x4AC`=1.0f, `+0x4B5`=`0x101`, `+0x3C0`-`+0x3DC` quad fields =4. Interior anchor `001F8A14` (the `+0x4A8` = 1.0f store).



## SWE2-EC7-65 update (2026-09-19) - `006336E0`

`006336E0` (135 B) is the `+0x3E0` embedded-object destructor - `00584730`/`006336E0`-self/`00633790`/`0063A570`/`0063D6B0`/`00680030`. Interior anchor `006336F7` (a `0063A570` call).



## SWE2-EC7-66 update (2026-09-19) - `0063A570`

`0063A570` (512 B) is a character-render body (512 B) - `00584730`/`0063B3E0`/`0063D8B0`/`00680030`/`00680200`/`006803D0` plus `02CF8370`/`02CF8580`. Interior anchor `0063A5FA` (a `0063D8B0` call).



## SWE2-EC7-66 update (2026-09-19) - `0063D6B0`

`0063D6B0` (210 B) is a call-free intrusive-list body - `r9` self-link, `r8` into `[r9+8]`/`[rax]`, `[rdx+0x78]`=0, `[rdx+0x38]` head walk (`006336E0` sibling). Interior anchor `0063D6E5` (the `r9` self-link store).


## SWE2-EC7-69 update (2026-09-19) - `00680030` pool drain measured

`00680030` (78 B) is the embedded-object pool drain the `+0x3E0` destructor
calls: under an EH cookie (`[rsp+0x20] = -2`) it pops each node off the
singly-linked free list at `[rbx+0x10]` (`head = [head]` advance) and calls
`00584730` on it until the list is empty, then writes `[rbx] = 0` - or just
`[rcx] = 0` when the list was already empty. The `00584730` callee is the
shared record free the game-application page names.
Interior anchor `00680057` (the `[rbx+0x10] = [head]` pop).

## SWE2-EC7-79 update (2026-09-20) - `002E98F0` gated bump measured

`002E98F0` (40 B) is the `002ED6F0`-tailed conditional the render
callers run: `002ED6F0(rcx)` executes unconditionally, then
`dword[rdx] == 1` adds `0x33` to `dword[r8]` - a kind-1-only counter
bump after the shared call.
Interior anchor `002E9900` (the `002ED6F0` call).

## SWE2-EC7-109 update (2026-09-20) - `001EE1D0` measured

`001EE1D0` (574 B) is the deep
clone `001A5B30` and `001F6E70`
call: `0063A990(rdx, 1,
02D3A440)` allocates the
duplicate, `001EF1A0` seeds it,
then a `dword[node] & 0x7FFFFFFF`
count walks the pointer table -
`qword[node + 8]` when the count
exceeds 1, inline `node + 8`
otherwise - cloning each element
through `00600120`. Per element
a `word[+0x12] & 0x1FFF` +
`word[+0x10]` sub-record scan
bounds-checks against
`dword[src]`, `00861EBA` copies
each qualifying span, and
`0060DEA0` seals the copy; the
result lands at `[rsi + 0x20]`
(or `[rsi] + 0x60` when the
table was empty).
Interior anchor `001EE2C3` (the
`00600120` element clone).

Mechanical neighbours introduced by
this section's citations: `0063A990`
(the block allocator the clone
calls) carries Input caller fan-in
(25 edges). Those are edges of the
allocator, not of the render object
- noted so the audit accounts for
them.

## SWE2-EC7-121 update (2026-09-21) - `00633790` measured

`00633790` (100 B) is the
`+0x50`-chain release walk
`006336E0` runs: from the
`[+0x10]` head it visits
each linked node - object
`0x50` before the link -
and where `byte[+0xFC] &
1` holds it calls the
node's `vtable[+0x38]`
with `edx = 1` (the
refcounted release).
Interior anchor `006337E1`
(the `vtable[+0x38]`
call).

## SWE2-EC7-122 update (2026-09-21) - `00628570` measured

`00628570` (77 B) is the
`+0x9C0` sub-object's
variant of the
`006285C0` parameter-write
idiom `001890A0`,
`001F5C20` and `00607410`
call: `+0x9EC = 1`; `+0x9F4`
takes `0061C010(r8d)` when
`dl` holds, else 8;
`[+0x9C0] |= 4`.
Interior anchor `0062858A`
(the `0061C010` call).

## SWE2-EC7-124 update (2026-09-21) - `0060DEA0` measured

`0060DEA0` (8 B) is the
two-field setter `001EE1D0`
calls: `+0 = rdx`,
`+8 = r8`, return.
Interior anchor `0060DEA3`
(the `+8` store).

`001EF060` (315 B) is the matrix arm `001E6E70`/`001FB080` call: when `rdx` nonnull it reads the nine floats at `rdx+0`..`+0x34` (rows 0-2 plus `+0x10`,`+0x14`,`+0x20`,`+0x24`,`+0x30`,`+0x38`) into xmm2-xmm11, XORs each against the `0x80000000` sign mask (`01CEBDA0`), and writes the sign-flipped 3x4 to `[[rcx+8]]` (`001EF126`-`001EF166`) - `rdx` is read-only, not modified; when null it loads the `-1`/`+1` identity constants instead - the render object's sign-flip-or-identity 4x3 transform staging (call-free, xmm6-xmm11 preserved). Corrected 2026-09-28 per FABLE BB-1: the flip lands on the out pointer, not in place at `rdx`.

Interior anchor `001EF09B` (function `001EF060`).

`001EF1A0` (213 B) is the small-vector resize `001EE1D0` runs on the render object's `{count, ptr}` pair at `[rcx]`/`[rcx+8]`: `edx == count` returns; bit-31-cleared capacity `> 1` means the `+8` heap buffer else inline storage at `rcx+8`; `ebx > 1` `0017D260`s `ebx*8` bytes and `rep stosq` zeroes them before the repoint - the 8-byte-element grow/shrink

Interior anchor `001EF201` (function `001EF1A0`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-character-render-object-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001890A0` | 97 B | loads qword `+0` and qword `+0x10` of `rcx`, calls `00628570(qword +0, 0, 1)` and `006215A0(qword +0, 1, qword +0x10, qword +0x10 + 0x40)` with stack arguments 0, 4 and 0, then tail-jumps `00628570(qword +0, 1, 1)` | `001890BA`, `001890CD`, `001890E0`, `001890FC` |
| `001AD470` | 20 B | dereferences the pointers at `rdx` and `rcx` and sets `al` to 1 when the float `+0x34` of the `rdx` object is below, equal to or unordered with the float `+0x34` of the `rcx` object, else 0 | `001AD476`, `001AD47B`, `001AD480` |
| `001BD840` | 244 B | scans the qword vector from qword `+0` to qword `+8` of `rcx` (count = byte difference / 8, unsigned index) for `rdx`; when found, passes `rdx` to `001F6E60`, passes `rcx+0x20` and the address of that result to the call at `001BD840` + 0x6B, calls slot `+0x10` of the qword at `+0x10` of the returned node with `rcx` = node+0x10, `edx` = 0x20 and `r8d` = 0, and unless that result plus 0x10 is zero stores 16 stack bytes (qword `rdx`, dword 3, 4 bytes this function does not write) at the result's `+0x10`; it then links the result before the node (result `+0` = node, result `+8` = node `+8`, qword `+0` of the old node `+8` = result, node `+8` = result), copies the vector's last qword into the found slot and adds -8 to qword `+8`; on every path tail-jumps at `001BD840` + 0xEF with `ecx` = 1 when the recomputed count differs from the original, else 0, and `rdx` = "Can't find character object when try to remove it!" (`008F9520`) | `001BD872`, `001BD8C2`, `001BD8CD`, `001BD902`, `001BD92F` |
| `001E6E70` | 220 B | takes the floats `+0x30`, `+0x34` and `+0x38` of `rdx` (zeros when `rdx` is null) and, when any differs from (or is unordered with) the floats `+0x244`, `+0x248`, `+0x24C` of `rcx`, stores them there and byte 1 at `+0x240`; then calls `001EF060(element, rdx)` for each qword from `+0x18` up to `+0x20` of `rcx` (none when `+0x18` is above `+0x20`) | `001E6E97`, `001E6EBA`, `001E6EDB`, `001E6EF3`, `001E6F26` |
| `001F4C00` | 80 B | walks 0x18-byte elements from `rcx` up to `rdx` with a parallel 0x18-byte destination from `r8`, and for each non-null destination stores `009010B8` at its `+0`, copies the source's qword `+8` and byte `+0x10` to the same offsets, then stores `00903940` at `+0`; returns the destination pointer past the last element (`r8` unchanged when `rcx` equals `rdx`) | `001F4C25`, `001F4C2C`, `001F4C34`, `001F4C38`, `001F4C4A` |
| `001F6E60` | 15 B | returns qword `+0x2A0` of the object at qword `+0x488` of `rcx` | `001F6E67` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-character-render-object-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `00186840` | 93 B | `001FA1A0` + 0x104 | calls the site `00186840` + 0xD and, when it returns non-zero, the site + 0x16; then, with i the dword `rcx+0xDD0`, returns qword `rcx+0xB50+i*8` when byte `rcx+0xDBB` is non-zero and the call at + 0x2A returns non-zero, and qword `rcx+0xB48+i*8` otherwise | Interior anchor `0018684D`; Interior anchor `00186856`; Interior anchor `0018685B`; Interior anchor `00186875`; Interior anchor `0018688A` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-character-render-object-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001E5370` | 182 B | computes `n` = (qword `[rcx+8]` minus qword `[rcx]`) / 0x18 (signed); when `edx` is at most `n` (unsigned, 32-bit) it calls `001E3D80(rcx, qword [rcx] + edx*0x18, qword [rcx+8])`; otherwise it calls `001E5370`+0x52 on a stack local, then `001E5370`+0x81 with (`rcx`, qword `[rcx+8]`, `edx` minus `n`, that call's result), then `001E5370`+0x8C on the same local | Interior anchor `001E53A8`; Interior anchor `001E53BB`; Interior anchor `001E53F1`; Interior anchor `001E53FC`; Interior anchor `001E5411` |
| `001F4C50` | 323 B | zeroes qwords `rcx+0`/`+8`/`+0x10` and calls `001EDF00(rcx+0x18, "EASTL vector" 008C5F58)`; then for `B` = `rcx+0x20` and again for `B` = `rcx+0x58` it calls `001EDF00(stack slot, "EASTL set" 008F3CB0)`, zeroes qwords `B+8`..`B+0x20` and dword `B+0x28`, calls `001EDF00(B+0x30, that call's result)`, stores the address `B+8` at qwords `B+8` and `B+0x10` and 0 at qword `B+0x18`, byte `B+0x20` and dword `B+0x28`; then calls `001F8A70(rcx, edx)` and, when `edx` is non-zero, calls `001F4C50`+0x124 `edx` times with (`rcx+0x20`, a pointer to a slot holding `rcx+0x58`, a pointer to a slot holding qword `[rcx]` + `i`*0x18 for `i` = 0, 1, ..., and a byte of the incoming `rdx` home slot, which this body never writes); returns `rcx` | Interior anchor `001F4C88`; Interior anchor `001F4CD2`; Interior anchor `001F4D3D`; Interior anchor `001F4D74`; Interior anchor `001F4D81` |
| `0042E130` | 63 B | calls `00426220(rcx, qword [rdx+8])` and returns its result when it is non-zero; otherwise calls `0042E130`+0x27 with `rcx` only when word `[rcx+0x3fa]` is below `0x1000` (unsigned), then tail-jumps to `0042E130`+0x34 with `rcx` | Interior anchor `0042E13D`; Interior anchor `0042E144`; Interior anchor `0042E14B`; Interior anchor `0042E157`; Interior anchor `0042E164` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, wave h8, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-character-render-object-h8-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `001E2250` | 928 B | `001E5370` + 0x81 | inserts `r8d` copies of the 0x18-byte element at `r9` (qword `+8`, byte `+0x10`) before `rdx` into the array with qwords `B`, `E`, `C` at `rcx`, `rcx+8`, `rcx+0x10`: returns when `r8d` is 0; when `r8d` is at most (`C`-`E`)/0x18 (unsigned, 32-bit) it uses a stack copy (vtable `009010D8`): if `r8d` is below the count `t` of elements from `rdx` to `E` (unsigned) it calls `001E2250` + 0xC6 to construct the last `r8d` at `E` and shifts the rest up by field assignment, else it constructs `r8d`-`t` copies at `E` and calls `001E2250` + 0x19F to construct the `t` tail ones next; advances `E` by `r8d`, assigns the copy's fields to the `r8d` (or `t`) slots from `rdx` and calls `001E2250` + 0x149 or + 0x1E8 on the copy; otherwise it requests 0x18 times max(2*size (1 when size is 0), size+`r8d`) bytes through vtable slot `+0x10` of the object at `rcx+0x18` (`001E2250` + 0x238), constructs there the elements before `rdx`, the copies, the rest, calls vtable slot 0 of each old element with `edx` = 0, frees a non-null `B` through slot `+0x18` (`001E2250` + 0x36A), and stores new `B`, `E`, `C`; own constructions write vtable `009010B8`, the two fields, then vtable `009010D8`, skipping null slots | Interior anchor `001E22A5`; Interior anchor `001E2316`; Interior anchor `001E2488`; Interior anchor `001E2578`; Interior anchor `001E25C2` |
