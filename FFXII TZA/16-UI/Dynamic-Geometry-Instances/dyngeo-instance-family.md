---
system: DynGeo instance family — how UI, text and drop shadows are drawn
category: 16-UI
status: AUDITED
evidence_tier: 1
owner_layer: CodeDomain — mixed NativeDispatch / NativeInline, no PrimaryOwner
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
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: false
  reopened_count: 1
---

# The DynGeo instance family

**Eight classes, three vtable shapes, and one 2×2 variant matrix implemented by tail-call.** This is
the "dynamic geometry" layer — the objects the game builds per frame to draw UI, textures and text.

## 1. What the player sees

**Menu text, item names, damage numbers, and the dark outline behind them.**

The drop shadow under FFXII's UI text is **not a shader effect and not a blur** — it is a *separate
draw*, performed by a separate class, whose method **runs its own small setup and then jumps into the
ordinary text-drawing code**. The shadow and the text are the same drawing routine invoked twice with
different state.

Likewise "Final": there is a variant that ~~**resets the transform to the identity matrix**~~ **loads the identity
rows and then replaces row 0 with an aspect factor** before drawing *(corrected 2026-09-26, §2)*. On a 16:9 display the
factor is 1.0 and the matrix is the identity. This is the shape of an element composited in screen space rather than
positioned in the world.

## 2. Native mechanism

### Three vtable shapes

| shape | classes | slots |
|---|---|---:|
| **21-slot** | `DynGeo3DInstance`, `DynGeoTextureInstance`, `DynGeoUIInstance` | 21 |
| **12-slot** | `DynGeoFontTextSpecialInstance`, `…FinalInstance`, `…ShadowInstance`, `…ShadowFinalInstance` | 12 |
| **3-slot** | `DynGeoFontTextInstance` | 3 |

The three 21-slot classes share a base whose other slots are folded across them; only the slots each
overrides appear as uniquely-owned methods. **Their absence from the per-class list is the folding
filter, not evidence of an empty base** — see [the vtable index](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md).

### The 2×2 matrix: Shadow × Final

The four `FontTextSpecial` classes differ at **four slots — 2, 6, 10 and 11**. Slot 10 carries the
full 2x2 and is the discriminator; the four implementations sit consecutively in `.text`:

> **Corrected, falsification pass 1 (2026-09-02).** This read *"exactly two slots, 10 and 11, and
> nowhere else"*. A slot-by-slot diff of the four 12-slot vtables shows **four** differing slots.
> Slots 2 and 6 were missed, and they change the picture — see §10.

| class | slot 10 | size | ends with |
|---|---|---:|---|
| `…SpecialInstance` | `002142A0` | 306 B | `ret` — **the base implementation** |
| `…SpecialFinalInstance` | `00214210` | 139 B | **`jmp 0x2142A0`** → tail-calls the base |
| `…SpecialShadowInstance` | `00214540` | 82 B | **`jmp 0x2142A0`** → tail-calls the base |
| `…SpecialShadowFinalInstance` | `002143E0` | 352 B | indirect `jmp` — both prefixes, then **its own draw of layer 0 only** (§7, `BC-3`) |

**The variants are prefix code plus a tail-call into one shared body.** Not copies, not templates —
each variant does its own setup and then literally jumps into `SpecialInstance`'s method.

~~**The `Final` prefix resets the transform to identity:**~~ **The `Final` prefix loads the identity rows, then
overwrites row 0 with `(aspect, 0, 0, 0)`:**

```asm
00214220  call  FUN_00182F50           ; a predicate — skip everything if 0
00214227  je    0x214286
00214229  movaps xmm3, [rip -> 008C5FD0]   ; 0 0 0 1
00214230  movaps xmm2, [rip -> 008C5FB0]   ; 0 0 1 0
00214237  movaps xmm1, [rip -> 008C5F90]   ; 0 1 0 0
0021423E  movaps xmm0, [rip -> 008C5F80]   ; 1 0 0 0
          ...stored to a 64-byte stack buffer...
0021425C  call  thunk_FUN_00183280
00214283  call  qword ptr [rax + 0x30]  ; slot 6 of the target object
00214291  jmp   0x2142A0                ; -> the base implementation
```

> **Corrected 2026-09-26 (FABLE, Claude Opus 5.5), on `OPUS-NOTE-FABLE-DYNGEO-FINAL-ASPECT`, which executed the
> prefix (`candidates/s37-opus-replay-text-interpreter/i5_i9_i13.py`, case I10). Re-read here:**
> - **Row 0 is overwritten.** After the four rows are stored to the stack buffer, `0021425C` calls `00229DE0`.
>   `0021426C` stores its float return over row 0's first element, and `00214272` / `0021427B` zero the rest of the
>   row, before slot 6 is called with the buffer (`00214283`).
> - **`00229DE0` takes no argument.** It is `jmp 00183280`, which returns height × K ÷ width, with height and width
>   read from the display object. K is `16/9` (`008C5B38`) unless the `01F82D18` object supplies its own value
>   (`001832A8`–`001832C4`).
> - **So row 0's x is 1.0 at 1920×1080**, where OPUS's replay received the identity, and `1.4222` at 1280×1024. The
>   prefix is a horizontal aspect correction toward 16:9, not a reset.
> - OPUS also measured `ShadowFinal`: it draws layer 0 with primitive 3 (the base draws with 2), unbatched and with no
>   null-source skip, and it passes 10 where `Shadow` passes 9.
> - *Throughout this page, "identity-matrix path" and "identity-matrix prefix" name this prefix. Its pool rows are the
>   identity; the matrix it hands on is not, except at 16:9. The path's reachability (the predicate below, `BC-2`) is
>   unchanged.*

**Those four constants decode to the 4×4 identity matrix** *(the pool rows; row 0 is replaced before use, above)*.
They are read from a shared constant pool
at `008C5F80`, `008C5F90`, `008C5FB0`, `008C5FD0` — note the **uneven spacing**, so this is four rows
selected from a pool of common vectors, **not a contiguous matrix literal**.

**The `Shadow` prefix passes three small constants and makes one virtual call:**

```asm
00214550  mov   r9d, 7
00214556  mov   dword ptr [rsp + 0x30], 9
00214561  mov   dword ptr [rsp + 0x28], 7
00214569  mov   dl, 1
0021456B  mov   dword ptr [rsp + 0x20], 6
00214576  lea   r8d, [r9 - 1]            ; = 6
0021457A  call  qword ptr [rax + 0x78]   ; slot 15 of the target object
0021458D  jmp   0x2142A0                 ; -> the base implementation
```

**6, 7, 9 and a flag of 1.** What they select is not established — see section 7.

### Slot 11: a flag the plain variant hardcodes off

Both slot-11 overrides are pure tail-jumps into **slot 35** (`+0x118`) of the target object, and they
differ in exactly one argument:

```asm
; Special (00214890, 24 B)
0021489A  xor   r8d, r8d                 ; third argument = 0, always
002148A1  jmp   qword ptr [rax + 0x118]

; Shadow (002148B0, 33 B)
002148B5  test  r8b, r8b
002148C3  setne al
002148C6  movzx r8d, ax                  ; third argument = (incoming != 0)
002148CA  jmp   qword ptr [r9 + 0x118]
```

> **Corrected, falsification pass 1.** This read *"**Both** slot-11 overrides… The shadow variant
> forwards a boolean that the plain variant pins to false. That is the entire difference at this
> slot."* There are **three** slot-11 implementations, not two. The third, `00214860`, is used by
> **both `Final` and `ShadowFinal`** and was not mentioned.

All three are pure tail-jumps into slot 35 (`+0x118`) differing only in the **third argument**, and
that argument is a **three-valued mode, not a boolean**:

```asm
; plain   00214890 (24 B)   xor r8d, r8d                      -> 0
; Shadow  002148B0 (33 B)   test r8b,r8b ; setne al ; movzx   -> 0 or 1
; Final   00214860 (36 B)   neg al ; sbb r8w,r8w ; and r8w,2  -> 0 or 2     (also ShadowFinal)
```

So slot 11 selects a draw mode `{0 plain, 1 shadow, 2 final}` from the same incoming boolean. **At
this slot `ShadowFinal` takes the `Final` value, not the `Shadow` one** — an asymmetry the 2x2
framing hides.

## 3. Key addresses

| address | role |
|---|---|
| `002142A0` | `DynGeoFontTextSpecialInstance` slot 10 — **the shared base implementation**, 306 B |
| `00214210` | `DynGeoFontTextSpecialFinalInstance` slot 10 — identity-matrix prefix, 139 B |
| `00214540` | `DynGeoFontTextSpecialShadowInstance` slot 10 — constant prefix, 82 B |
| `002143E0` | `DynGeoFontTextSpecialShadowFinalInstance` slot 10 — both, inlined, 352 B |
| `00214890` | `DynGeoFontTextSpecialInstance` slot 11 — passes 0 |
| `002148B0` | `DynGeoFontTextSpecialShadowInstance` slot 11 — forwards a boolean |
| `008C5F80` / `008C5F90` / `008C5FB0` / `008C5FD0` | the four rows loaded, from a pool of six +/- axis vectors — see §10 |
| `00213AD0` / `00213AA0` / `00213B00` | slot 2, the sized deleting destructors: `0x160` plain, `0x170` Final, `0x168` Shadow **and** ShadowFinal |
| `00213D10` / `00213B40` | slot 6: shared by plain/Shadow/ShadowFinal (273 B) vs `Final`'s own (460 B) |
| `00214860` | slot 11 for **both** `Final` and `ShadowFinal` — forwards mode 2 |
| `00182F50` | predicate gating the `Final` path |
| `00229DE0` | `thunk_FUN_00183280`: a no-argument float source (height × K ÷ width), whose return replaces row 0's x (`0021426C`). ~~called with the matrix buffer~~ *(corrected 2026-09-26)* |

**Other family members, uniquely owned:**

| class | slot | address | size |
|---|---:|---|---:|
| `DynGeoTextureInstance` | 1, 5, 6, 19 | `001FB8E0`, `001FBA50`, `001FB990`, `001FBB10` | 161/192/191/45 |
| `DynGeoUIInstance` | 5, 6 | `00215AA0`, `00215A30` | 105/109 |
| `DynGeo3DInstance` | 5, 6 | `001FBBE0` (thunk), `001FBBB0` | 5/39 |
| `DynGeoFontTextInstance` | 1 | `00213140` | 644 |

## 4. Data structures and formulas

**The pool's identity rows**, read out of the image rather than assumed *(row 0 is replaced at run time by
`(aspect, 0, 0, 0)`, §2)*:

```
008C5F80   1.0000   0.0000   0.0000   0.0000
008C5F90   0.0000   1.0000   0.0000   0.0000
008C5FB0   0.0000   0.0000   1.0000   0.0000
008C5FD0   0.0000   0.0000   0.0000   1.0000
```

**Field access separates the shadow path from the plain one:**

| variant | fields touched |
|---|---|
| `Special` slot 10 | `+0x50`, `+0xA8` |
| `ShadowFinal` slot 10 | **`+0x58`**, `+0xA8` |

**`+0x50` against `+0x58` — eight bytes apart, with `+0xA8` common to both.** The shadow path reads a
parallel field where the plain path reads its own. **What those two fields hold is not established**;
the pairing is the observation. **BC-3.**

> **Corrected 2026-09-14 (FABLE): there is no plain/shadow pair.** `+0x50` and `+0x58` belong to two different
> ten-entry arrays of one layout, answered under `BC-3` in §7:
> - the shared slot 10 walks ten layers and reads `+0x50` only as layer 9's texture;
> - `ShadowFinal`'s inline slot 10 draws layer 0 alone and reads `+0x58` as layer 0's vertex array.
>
> `Special` slot 10 touches `+0x08`–`+0x50`, `+0x58`–`+0xA0` and `+0xA8`–`+0xCC`, not two fields.

## 5. Call chain

```
…SpecialFinalInstance::slot10          …SpecialShadowInstance::slot10
   predicate FUN_00182F50                  constants 6, 7, 9, flag 1
   load identity matrix                    call [target + 0x78]  (slot 15)
   call thunk_FUN_00183280                        |
   call [target + 0x30]  (slot 6)                 |
        |                                         |
        +----------> 002142A0 <-------------------+
                     …SpecialInstance::slot10
                     the shared body, 306 B, ret
```

`…SpecialShadowFinalInstance::slot10` performs **both** prefixes and does not tail-call — its 352 bytes
contain the work inline, and its callee set is exactly the **union** of the other two prefixes'
(`00182F50`, `00229DE0`, `00861EBA`).

## 6. Modding notes

- **The drop shadow is a separate draw with its own object**, so suppressing or restyling it is a
  matter of which class is instantiated, not of a shader uniform.
- **`002142A0` is the single choke point** for all four text variants — one detour there sees every
  `FontTextSpecial` draw regardless of shadow or final state.
- **XIIOnline:** nothing here carries gameplay state. It matters only if remote-player nameplates or
  damage numbers are ever drawn through the same path, which has not been checked.

## 7. What is not known

- [x] What `6`, `7`, `9` select in the `Shadow` prefix, and what slot 15 of the target object does
      with them. The constants are read; their meaning is not. **BC-1.**
      *Narrowed 2026-09-14 (FABLE), not answered: if the target is `PrimitiveRendererD3D11`, the constants are standard
      alpha blending plus ~~a shader constant~~ a CPU-side selector (corrected 2026-09-15, below).* The condition is the Gi
      family's open `BG-11`. *(BG-11 was answered on 2026-09-22, in §20: the device is `02CC1CD0`, `0x18C0` into the magic-static singleton `02CC0410`. Noted 2026-09-26, FABLE, Claude Opus 5.5.)*
      **PARTIAL in the register since 2026-09-15 (OPUS, `7d07899f`):** 6, 7 and slot 15 are answered from the bytes
      (the whole `0061BF40` map is decoded); the last constant is bounded and not named. See the `BC-1` row in
      [the register](../../_index/OPEN-QUESTIONS.md). The box stays open for the unnamed value.
      **ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static:** the selector is one enum with two producers - the GS
      translator's blend-emulation classes 0-5 (from its 81-entry ALPHA-equation table) and these shadow classes (9, 10).
      `{3, 5}` are the two GS blend cases handled outside fixed-function blending, so 9 and 10 take the general path at
      every read. [The BC-1 record](../../_index/candidates/bc1-selector-enum/README.md) (6 checks).
      - **The contract match.** The target was not traced, but every slot these classes call fits that class's primary
        vtable `00D86960` (the Gi page's leading candidate, §13b):

        | slot | `00D86960` implementation | fits the call here |
        |---|---|---|
        | 0 / 1 | `006CA760` ~~begins a batch and~~ *returns the fixed staging area (682 vertices) and* publishes `+0xB8` *(corrected 2026-09-26 (FABLE, Claude Opus 5.5): batching is slot 4's job; the Gi page `BG-6`)*; `006CB5E0` returns `+0xB8` | the memcpy destination |
        | 4 | `006C8C50(type, buffer, count)` → `006DA5A0` | the draw with 2 or 3 |
        | 6 | `006CAF40` copies 16 dwords to `+0x10` and sets dirty `+0x208F3` | `Final`'s identity matrix |
        | 8 | `006CAEB0` stores a texture and its sampler arguments | the layer texture bind |
        | 15 | `006CAB80`, below | the `Shadow` constants |
        | 35 | `006CAC30` stores `dl` at `+0x851` and `r8w` at `+0x852` | slot 11's boolean and mode |

      - **Slot 15 `006CAB80(1, 6, 7, 6, 7, x)`** passes its first five arguments to `00627FF0` on the `+0x208` state
        object. That function zeroes `+0x64`, stores the boolean at `+0x68`, and stores the four blend values at `+0x6C`,
        `+0x70`, `+0x78` and `+0x7C`, each through `0061BF40`. That layout is `D3D11_BLEND_DESC` at `+0x60`
        (`BlendEnable`, `SrcBlend`, `DestBlend`, `SrcBlendAlpha`, `DestBlendAlpha`, skipping `BlendOp` at `+0x74`) — a
        layout match, not a named type.
      - **`0061BF40` maps the engine's blend enum to D3D11's:** 0→1 ZERO, 1→2 ONE, 2→3 SRC_COLOR, 3→4 INV_SRC_COLOR,
        4→9 DEST_COLOR, 5→10 INV_DEST_COLOR, **6→5 SRC_ALPHA**, **7→6 INV_SRC_ALPHA**, 8→7 DEST_ALPHA, 9→8
        INV_DEST_ALPHA, and so on (table `0061BFC4`). **So `(1, 6, 7, 6, 7)` turns on `SRC_ALPHA` / `INV_SRC_ALPHA`
        blending for colour and alpha**, the ordinary blend a drop shadow needs. The engine's own `006C9CD0` calls `00627FF0`
        with the same four values and the boolean 0 (`006CA55D`–`006CA57A`).
      - **The last constant (`9` in `…ShadowInstance`, `10` in `…ShadowFinalInstance`) is not a blend value.** `006CAB80`
        stores it at renderer `+0x7C` and sets dirty `+0x208F1`. It sits inside the 32-dword block `+0x10`–`+0x8C`
        (the matrix is its first 16) that `006C8920` copies to `+0x20868` before a draw~~, so it reaches the shaders as a
        constant~~. `006C8920` runs from `006CB2A0`, which draw slot 4 calls first (`006C8C6F`). Which effect 9 and 10
        select is not read.
        - **Corrected 2026-09-15 (FABLE, accepting `OPUS-CONTRA-DYNGEO-SHADER-CONSTANT`): the value does not reach a
          shader through this block.** The copy is real and complete: `006C8920` stores dword by dword, the last pair being
          `006C8A55` / `006C8A5B` (`+0x8C` → `+0x208E4`). But only the first 64 bytes are uploaded.
          - **The upload.** Both uploads (`006C9335`–`006C934C` and `006C98E9`–`006C98F8`, inside `006C8CA0`) pass
            `+0x20868` to device-context slot 48 with the buffer `[+0xD0]`, subresource 0 and a null box. That fits
            `ID3D11DeviceContext::UpdateSubresource`, where the two `0x40` arguments are row and depth pitches, not a length.
          - **The bound is the buffer.** `[+0xD0]` is created in `006C9CD0` (`006CA476`–`006CA49F`) through device slot 3
            with a description of `ByteWidth 0x40`, `Usage 0`, `BindFlags 4` (constant buffer). A null-box update writes that
            many bytes: `+0x20868`–`+0x208A7`, which is the 4×4 matrix. The constant's mirror `+0x208D4` is `0x6C` past the
            base, outside it.
          - **Its consumer is the CPU.** OPUS's census reads it at five sites, all in `006C8CA0`, all the predicate "value is 3
            or 5". The true arm binds a shader pair from `+0x1C0` / `+0x1D0` (`006C8E74`). So 9 and 10 take the other arm:
            **the value selects a program on the CPU, and which enum it belongs to is unnamed.**
          - **Bound.** The mirror census is by displacement (`0x20860`–`0x208F8` over `.text`). A base rebased through a register
            first would not show. There are no direct calls to `006CAB80`, so the value set cannot be read off call sites.
      - **Slot 35 selects the shader pair.** `006C8920` uses `+0x851` / `+0x852` to load `+0x190` / `+0x198`. When
        `+0x851` is 0 it takes `+0x118` / `+0x110`. Otherwise it takes `+0x148` (mode 1), `+0x140` (mode 2) or `+0x128`
        (other), each with `+0x130` (`006C8AFD`–`006C8BE9`). So slot 11's `{0 plain, 1 shadow, 2 final}` picks a
        program.
- [x] What the `Final` predicate `FUN_00182F50` tests, and therefore when the identity-matrix path is
      taken at all. **BC-2.**
      *Narrowed 2026-09-14 (FABLE), not answered:* **the predicate is "field 0 of the `01F82D18` singleton equals 1".**
      - **The chain.** `00182F50` calls `001DD8C0(001DDAB0())`. `001DDAB0` returns `[01F82D18]`, and `001DD8C0` returns
        `true` only when `dword [obj] == 1` and `005C5230()` returns 0. That second call is the folded `xor eax, eax ;
        ret`, so it always does.
      - **The object.** It is a 0x180-byte singleton built once by `001DDA70` and constructed by `001DC5C0`, which stores
        **`[obj] = 0`** (`001DC5D6`) and copies config fields `+0x68` → `+0x60` and `+0x08` → `+0x18` from
        `[01F82D20]`.
      - **No writer of 1 was found.** Every call site of `001DDAB0` was followed for a store into `dword [rax]`, including
        through one register copy, and none exists. The only other `dword [reg] = 1` near this code (`001DC444`) writes a
        different object. So in the static image the `Final` identity-matrix path is gated off unless field 0 is written
        through a route this search does not follow. **Which route that is, and whether it exists, is the residue.**
      **ANSWERED 2026-09-14 (OPUS, register row `BC-2`), carried here 2026-09-15 by FABLE: no such route exists, so the
      predicate is statically always false and the `Final` identity-matrix path is unreachable in this build.**
      - **Field 0 is written once in the image, with zero** (`001DC5D6`, `edx` zeroed at `001DC5C6`).
      - **The pointer cell `01F82D18` has three `.text` references:** a compare and a store, both in the lazy initialiser,
        and the getter's load. FABLE re-ran this census on 2026-09-15 and got the same three.
      - **None of the 72 direct call sites of the getter `001DDAB0` writes `[ret + 0]`.** None stores the pointer to
        memory either, so no other body can hold it. The 14 other callees that receive it as argument 0 do not write
        field 0.
      - **The bound:** this is an enumeration one call deep from the getter, plus the constructor. That depth covers every
        holder, because the pointer is reachable only through the getter.
- [x] What `+0x50` and `+0x58` hold — the plain/shadow field pair. **BC-3.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BC-3): they are not a pair.* The
      `FontTextSpecial` object holds **ten vertex layers**, each with its own texture, and the four shared slots 4, 5, 6
      and 10 manage them.

      | field | contents | writer / reader |
      |---|---|---|
      | `+0x08 + 8·i` | layer `i`'s texture | slot 4 `00213B30(i, tex)`, bound `i < 10` |
      | `+0x58 + 8·i` | layer `i`'s vertex array, 48-byte vertices | slot 5 `00213F90(i, n)` allocates `n × 0x30` bytes through `001A1470` on `[01F7F4C0]` |
      | `+0xA8 + 4·i` | layer `i`'s vertex count `n` | slot 5 |
      | `+0xD0 + 4·i` | layer `i`'s fill cursor | slot 6 `00213D10(i, src)` appends one vertex and increments it |

      - **Slot 6** maps the source's position from a centre-2048 space to clip space: x = (x − 2048)·2 / (1920 or 512),
        y = (y − 2048)·(−2) / (1080 or 448), with the pair picked by `001B1620`. It stores those at vertex `+0x00`/`+0x04`,
        source `+0x14`–`+0x28` at `+0x08`–`+0x1C` and source `+0x00`/`+0x04` at `+0x20`/`+0x24` (`00213D4C`–`00213E0A`). `Final` has its own slot 6, `00213B40`.
      - **Shared slot 10 `002142A0` draws every layer.** For `i` = 0…9 (`r12 = 10`; `r14 = this+8`, `r15 =
        this+0xA8`), a layer with a texture has it bound through the target's `+0x40`. When the count is
        nonzero, its `[r14+0x50]` array is copied into space returned by the target's slot 0 in chunks of at most **480 vertices**
        (`0x1E0`) and drawn through `[target+0x20]` with first argument **2** (`002142D0`–`002143B4`). **`+0x50` is
        therefore layer 9's texture.**
      - **`ShadowFinal`'s slot 10 `002143E0` is not the shared body inlined.** After its Final and Shadow prefixes it
        binds only layer 0's texture (`+0x08`), copies layer 0's whole array (`+0x58`, `+0xA8` vertices) in one piece,
        and draws with first argument **3**. There is no 480-vertex split, and no null-texture or zero-count check (`00214491`–`0021453C`). **`+0x58` is layer 0's
        vertex array.**
      - **Its Shadow prefix passes 10 as the last constant where `…ShadowInstance` passes 9** (`0021446D` against
        `00214556`), which bears on `BC-1`.
      - **Not established:** what first arguments 2 and 3 select on the target, and whether the layers are pages of a
        glyph atlas.
- [x] The 21-slot base class shared by `DynGeo3DInstance`, `DynGeoTextureInstance` and
      `DynGeoUIInstance`. Its own methods are folded across the three and so are absent from the
      uniquely-owned set. **BC-4.**
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5), from RTTI: the base is `DynGeoUIInstance` itself.** The class
      hierarchy descriptors list it as a base of `DynGeo3DInstance` and `DynGeoTextureInstance`, and its own only
      base is `GeometryInstance`, which has no vtable of its own here. Its methods are the 16 slots all three
      vtables share (0, 3, 4, 7–18, 20). `DynGeo3DInstance` overrides slots 2, 5 and 6, and
      `DynGeoTextureInstance` overrides 1, 2, 5, 6 and 19. Control:
      `_index/candidates/bc4-dyngeo-base/bc4_hierarchy.py`, 5 checks.
- [x] Whether "Final" means a final composite pass. **The identity matrix is consistent with screen-
      space composition and does not prove it.** **BC-5.**
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): no. `Final` is the in-place text draw, and the composite pass is
      `ShadowFinal`.** The text flush (the `display : draw Font` flush) is the only place these classes are
      constructed. It branches per text record on the "paint offscreen" byte `+0x2348` ([painting a line of text](../../99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md) §4):
      - **Byte zero: draw in place.** The flush constructs the one `Final` object (`0x170` bytes) and pushes no
        render target. It copies its 4×4 matrix at `+0xE30` into the object through slot 3 (`00214710`, which
        fills `+0x11C`–`+0x158`). `Final`'s own slot 6 (`00213B40`) then applies that matrix to every vertex on
        the CPU, with a divide by w, before the GS-to-device mapping that the shared slot 6 (`00213D10`) also does.
      - **Final's shader.** Its slot 11 passes mode 2. The renderer's slot 35 stores that mode at `+0x852`, and the
        renderer's shader selector binds the program at `+0x140` for it. That is the embedded shader `01F38EB8`,
        which is only `saturate(texture × vertex colour)`.
      - **Byte non-zero: paint offscreen, then composite.** `Shadow` objects paint into a ladder render target
        (mode 3). Then the target at flush `+0x2300` is pushed with mode 1, a `ShadowFinal` object is built and
        handed four vertices on layer 0, and the composite method, which has a single call site in the image, is
        called on that object.
        **That is the composite.**
      - **The aspect prefix on `Final`'s slot 10 does not run** in this build (the predicate is statically false,
        `BC-2`).

      So in these names *Final* marks drawing to the destination with the full transform, and *Shadow* marks
      the offscreen stage. `ShadowFinal` is the offscreen result drawn to the destination. That naming is a
      reading; the two arms are read from the code. The flush and renderer addresses are in the control,
      [`bc5_final_is_in_place.py`](../../_index/candidates/bc5-final-is-in-place/bc5_final_is_in_place.py) (6 checks, FAILS 0). Its sensitivity check shows the shader predicate rejects mode 1's
      program.

## 8. Evidence

**Tier 1** — every claim read out of the shipping image.

**The tail-call structure is the load-bearing finding and it is direct.** The last instruction of
`00214210` and of `00214540` is `jmp 0x2142A0`, disassembled, not inferred from proximity or from the
class names. Address adjacency is banned as evidence by
[`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) and is not used here — the
four implementations *are* adjacent in `.text`, and that adjacency is reported as a fact about layout,
never as the reason they are related.

**The identity matrix was decoded, not recognised by shape.** The four RIP-relative `movaps` targets
were resolved and unpacked as floats. **Their spacing is uneven** (`0x10`, `0x20`, `0x20`), which is
itself the evidence that they are pooled constants rather than one matrix object — a contiguous
literal would have been a uniform stride, and reporting it as "a matrix at `008C5F80`" would have been
wrong.

**The slot-11 difference is a two-instruction diff**, quoted in full above, on two methods of 24 and
33 bytes read end to end.

**What is deliberately not claimed.** That these draw UI text is supported by the class names and by
the transform and flag machinery, **not by a traced draw call** — no rendering API entry point has
been followed out of any of these methods. Section 1 should be read as the reading the names support.
**BC-5 tracks the strongest version of that gap.** *(2026-09-26 (FABLE, Claude Opus 5.5): BC-5 is answered in §7. The
`Final`/`Shadow` choice now reaches the device, through the renderer's slot 35 and its shader selector.)*

## 9. Related

- [`../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md)
  — the index these classes were selected from.
- [`../Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`](../Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md)
  — the character mapping and per-glyph advance that feed text drawing.
- [`../../17-Presentation-Rendering/Character-Rendering/character-render-object.md`](../../17-Presentation-Rendering/Character-Rendering/character-render-object.md)
  — the other game class read out of the index in this pass.

## 10. Falsification pass 1 — 2026-09-02, by a session that did not write this document

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`.

### First, the audit record itself was wrong

The front matter said `passes: 1`. **No falsification pass had happened.** `AUDIT-LOG.md` pass 103
is the pass that *created* this document — its own scope line reads *"new document
`16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`"* — and the owed table lists this
document as needing "a first named falsification pass". There was no §10, so by
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s own definition (`AUDITED` = survived a
pass **recorded in §10**) the count had nothing behind it. **The authoring pass was being counted as
an audit pass.** This is that first pass.

### Overturned: the variants differ at four slots, not two

A slot-by-slot diff of the four 12-slot vtables — re-derived from RTTI, not from the vtable index:

| slot | plain | `Final` | `Shadow` | `ShadowFinal` |
|---:|---|---|---|---|
| **2** | `00213AD0` | `00213AA0` | `00213B00` | `00213B00` |
| **6** | `00213D10` | `00213B40` | `00213D10` | `00213D10` |
| **10** | `002142A0` | `00214210` | `00214540` | `002143E0` |
| **11** | `00214890` | `00214860` | `002148B0` | `00214860` |

Slots 0, 1, 3, 4, 5, 7, 8, 9 are identical across all four. **Slots 2 and 6 were missed**, and both
carry real information.

### Slot 2 is a sized deleting destructor — and it breaks the 2x2 at the layout level

```asm
00213AD0  plain        mov edx, 0x160 ; call 0x809950    -> 352 bytes
00213AA0  Final        mov edx, 0x170 ; call 0x809950    -> 368 bytes
00213B00  Shadow AND ShadowFinal      mov edx, 0x168     -> 360 bytes
```

Three object sizes across four classes. **`Shadow` and `ShadowFinal` share one destructor and one
size.** If the family were a clean 2x2 product — plain `0x160`, `Final` +0x10, `Shadow` +0x08 —
`ShadowFinal` would be `0x178`. It is `0x168`, identical to `Shadow`. **So "Shadow x Final" is a
product in behaviour at slot 10 and is not a product in object layout.** Three free-object sizes for
the census, incidentally.

### Slot 6: `Final` alone overrides it

`Final` has its own 460-byte implementation at `00213B40`; plain, `Shadow` and `ShadowFinal` all
share `00213D10` (273 B). So `Final` is the heavier variant at two slots, not one.

### Confirmed, and promoted from a shared source

The eight classes and the three vtable shapes were taken from the vtable index — the same source
this database's object-model document uses. Re-derived here **straight from the EXE's RTTI**
(`.?AV<name>@@` type descriptor → complete-object locator → vtable), with a positive control on a
class proven by that route in another category:

```
DynGeo* type descriptors : 8
21-slot : DynGeo3DInstance, DynGeoTextureInstance, DynGeoUIInstance
12-slot : the four DynGeoFontTextSpecial* variants
 3-slot : DynGeoFontTextInstance
```

Exact match, one vtable per class. **The shape census no longer depends on the vtable index.**

The slot-10 tail-call structure also reproduces: `00214210` and `00214540` both end in
`jmp 0x2142A0`, and `002143E0` ends in an indirect `jmp`.

### The constant pool — this document was right, and a neighbour is wrong

§2 argued from the uneven spacing (`0x10, 0x20, 0x20`) that `008C5F80…` is *"four rows selected from
a pool of common vectors, not a contiguous matrix literal"*. Reading the bytes shows **why** the
spacing is uneven — the gaps hold the negations:

```
+0x00  008C5F80   1  0  0  0     <- loaded
+0x10  008C5F90   0  1  0  0     <- loaded
+0x20  008C5FA0   0 -1  0  0
+0x30  008C5FB0   0  0  1  0     <- loaded
+0x40  008C5FC0   0  0 -1  0
+0x50  008C5FD0   0  0  0  1     <- loaded
```

Six +/- axis vectors, interleaved. The four the `Final` prefix loads do assemble to the identity, so
that claim stands — but **there is no `float[4]x4` identity object at `008C5F80`**, and the first
`0x40` bytes there are `1000 / 0100 / 0-100 / 0010`, which is not one.

**A neighbour document states otherwise.**
[`../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`](../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md)
lists `008C5F80` as *"`.rdata` float[4]x4 — the 4x4 identity, rows at `+0x00`, `+0x10`, `+0x30`,
`+0x50`"*. Its four offsets are right and its type is not: naming a 64-byte object at that address is
exactly the framing this document's author declined to use. **Flagged for that document's owner, not
edited here.**

### What I tried that failed to break it

- Attacked the eight-class / three-shape census expecting the vtable-index dependency to hide an
  error. It did not; RTTI agrees exactly.
- Attacked the slot-10 tail-call claim by re-reading the terminating instruction of all four
  implementations rather than trusting the table. All four as described.
- Attacked the identity-matrix decode by dumping `0x60` bytes rather than the four cited rows —
  which is what surfaced the +/- pool and the neighbour's error.
- Ran the neighbour check **before** attacking: 15 addresses shared with
  [the vtable index](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md), one each with
  two residual documents. The vtable index agrees throughout.


## 11. The two 21-slot vtables, member by member — 2026-09-14 (NOCALLER-INSTALLERS)

`DynGeoTextureInstance` (`00904328`) and `DynGeo3DInstance` (`009043D8`) share **sixteen of their
twenty-one slots** — the base `DynGeoInstance` method set — and differ at slots 1, 2, 5, 6 and 19,
where each class installs its own override. Thirty-five no-caller rows across the two tables
(18 `TextureInstance` + 17 `3DInstance`, counting each table's rows separately) are
members of these two tables; they dispatch through the vtable only. Both tables carry an RTTI
complete-object locator at `vtable - 8`.

| slot | `TextureInstance` | `3DInstance` | role | interior |
|---:|---|---|---|---|
| 1 | `001FB8E0` | `00215440` | configures from a param block: virtual `arg->+0x100` call, then `00215440` plus `00189120`/`00186A90` lookups | `001FB923` |
| 2 | `001FB8A0` | `001FBB70` | constructor: `lea` of its own vtable, init `+0x30`, tail into `00215380` | `001FB8AA` / `001FBB7A` |
| 5 | `001FBA50` | `001FBBE0` | lock pair `001B1620`/`001B1C00` wrapped around the real body `001FBA9C` | `001FBA73` |
| 6 | `001FB990` | `001FBBB0` | same lock pair around `001FB9CE` / tail into `001FBBF0` | `001FB9A5` / `001FBBCD` |
| 19 | `001FBB10` | `00215E20` | copies the arg's 20 / 16 bytes into `this+0x1E0…0x1F0` — the per-instance draw-state block | `001FBB12` / `00215E22` |

**The shared base slots** (identical qword in both tables):

| slot | address | role | interior |
|---:|---|---|---|
| 0 | `0016D6A0` | shared bare `ret` — the "do nothing" override | |
| 3 | `00216100` | normalized setter: `edx/[rsp+0x28]` into record `+0x20` | `0021612D` |
| 4 | `002160A0` | normalized setter: `arg+0x20` and `+0x24` divided by `+0x28`/`+0x2C` into record `+0x20`/`+0x24` | `002160C6` |
| 7 | `002158B0` | scaled write: `edx` and `+0x148` times the `008C5B34` constant into record `+0x10`/`+0x14` | `002158F7` |
| 8 | `002157C0` | scaled write: `arg+0x10` times `+0x144` times the `008C5B34` constant into record `+0x10` | `002157FC` |
| 9 | `00213560` | base method — not in the no-caller set | |
| 10 | `00215EF0` | record writer: `001B0FB0` on `this+0x10`, args repacked from the stack | `00215F44` |
| 11 | `00216020` | record writer: `001B10D0` on `this+0x10`, same packing shape | `00216067` |
| 12 | `00215F80` | **the CLUT name setter** — formats `"%s_clut_%d"` (`008F8118`) through `0019C5D0` when the flag arg is nonzero, else uses the raw name | `00215FCD` |
| 13 | `00215E50` | dispatches on `arg+0x110`: nonzero → virtual call `+0x50` on `arg+0x170`'s object, else tail-jumps its own `+0x58` | `00215E89` |
| 14 | `00213540` | base method — not in the no-caller set | |
| 15 | `00215CB0` | allocator/lookup: `0018A9E0` on the `[01F7E340]` pool, stored to `arg+0x20` | `00215CE9` |
| 16 | `00216160` | commit check: while `+0x1C0 < +0x1BC` calls virtual slots `+0x30` then `+0x40` | `00216181` |
| 17 | `00215B10` | copies `arg+0x108…0x118` into `+0x130…0x140` and re-derives via `002153C0`/`0019C5D0` | `00215B25` |
| 18 | `00215790` | record-array allocator: `+0x1BC` count times 48 bytes via `001A1470` on `[01F7F4C0]`, stored at `+0x18` | `002157AC` |
| 20 | `002159A0` | copies the arg's nine-dword block into `+0x1F4…0x210` | `002159C3` |

The record array at `+0x18` is 24-byte-stride, indexed by `+0x1C0` against the `+0x1BC` capacity —
slots 3/4/7/8 all write into `record[idx]` fields `+0x10`/`+0x20`, and slot 16 is the bound-checked
commit walk over it. This is the same 48-byte-vertex layer model §4 established for the
FontText family, at the shared base-class level.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Application — CLIENT.** `FUN_0017d6b0`, owned by that layer, calls `001DDA70` on this page. That caller is a 45-byte startup sequencer: six calls in fixed order and a tail-jump into a final one, with no work of its own; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — SERVICE.** `001B10D0` on this page calls `FUN_001b1440`, owned by that layer. What it reaches is a 159-byte path assembly: it formats `"%s%s%s"` into a **`0x100`-byte** stack buffer from two globals and the caller's name, inside a `0x148`-byte frame with a stack cookie; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).
- **CoreRuntimeScheduling - CLIENT and SERVICE (3 edges).** `001B1C00` is called by bodies filed to CoreRuntimeScheduling: `0017D4C0`; `00213F90`, `00215790` reach bodies filed to CoreRuntimeScheduling: `001A1470` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (54 edges).** `00182F50`, `00183280`, `001A1470`, `001B1440` (+13 more) are called by bodies filed to Presentation: `00180E70`, `00181000`, `00181190`, `00181250` (+25 more); `00213140`, `00620F60`, `006C8CA0`, `006C9CD0` reach bodies filed to Presentation: `002133D0`, `0061DE20`, `0061E270`, `0061E2E0` (+1 more) - shared machinery across the layer boundary, no shared ownership.

## SWE2-EC7-34 update (2026-09-19) - `00215440`

`00215440` (845 B) is the dyngeo instance setup - cookie frame, `001EE7C0`/`002155D5`/`002154C2`/`001EE650` plus `00861EBA`. Interior anchor `00215483` (an `001EE7C0` call).

## SWE2-EC7-38 update (2026-09-19) - `00213B40`

`00213B40` (460 B) is `Final`'s own slot-6 body the page names - `00900384`/`008C5B5C`/`008C5B48`, `001B1620` pair. Interior anchor `00213C1B` (an `001B1620` call).


## SWE2-EC7-64 update (2026-09-19) - `00214210`

`00214210` (139 B) is the `DynGeoFontTextSpecialFinalInstance` row body - `00182F50`/`00229DE0` plus `008C5F80`-`008C5FD0` quad and one vcall. Interior anchor `00214220` (a `00182F50` call).



## SWE2-EC7-65 update (2026-09-19) - `006CAEB0`

`006CAEB0` (135 B) is a call-free `PrimitiveRendererD3D11` texture+sampler store - `[rcx+0x1B0]`/`[+0x1A8]` ptrs, `setne`->`+0x68`, byte->float `+0x6C`. Interior anchor `006CAED5` (the `+0x1B0` texture store).


## SWE2-EC7-67 update - `0061BF40`

`0061BF40` (129 B) is the call-free blend-enum -> D3D11 mapper - `cmp ecx,0x12` jump-table at `0x61BFC4`, in-range arms return 1/3/4/5/6/7/8/9/0xA/0xB/0xE/0xF/0x10-0x13, out-of-range returns 2. Interior anchor `0061BF4F` (the `0x61BFC4` jump-table load).

## SWE2-EC7-109 update (2026-09-20) - `00215AA0` measured

`00215AA0` (105 B) is the
indexed vec4 slot write
`001FB990` and `001FBA50` run:
`dword[rcx + 0x1C0]` sign-extends
to the slot index, the element
address is
`qword[rcx + 0x18] + index * 24`,
and `xmm1` / `xmm2` / `xmm3` /
`[rsp + 0x28]` land at `+0` /
`+4` / `+8` / `+0xC` of that
24-byte record - the geometry
instance's per-slot float4
channel write.
Interior anchor `00215ABB` (the
first `movss` slot store).

## SWE2-EC7-116 update (2026-09-21) - `006DA850` / `006CACA0` / `006C9C40` measured

`006DA850` (13 B) is the
field-init `006C9B20` and
`006C9CD0` run:
`dword[+8] = 0`,
`word[+0x8010] = 0` - the
small reset half of the
`+0x8010`-bearing record.
Interior anchor `006DA855`
(the `+0x8010` write).

`006CACA0` (133 B) is the
record install `006C8920`
runs: `0062BA30(rcx +
0x398)` prepares the
sub-object, then three
unrolled `0x80`-byte
`movups` blocks plus a
`0x10` tail copy the
caller-supplied `0x190`
record into `+0x418`.
Interior anchor `006CACB7`
(the `0062BA30` call).

`006C9C40` (133 B) is the
reset `006C9CD0` runs:
`00861EC0` zeroes
`+0x10..+0x8F`, `+0x1A0`/
`+0x1A8`/`+0x1B0`/`+0x1B8`
clear, `+0x208FC = -1`,
`+0x208E8`/`+0x208F7`/
`+0x851` zero, and the
three float defaults land
(`+0x208EC = 0.1`,
`+0x1E8 = 0.00104`,
`+0x1EC = 0.000889`) before
a `vtable[+0x130]` tail.
Interior anchor `006C9C55`
(the memset call).

## SWE2-EC7-122 update (2026-09-21) - the `006C9CD0`/`006CABxx` parameter setters measured

The five bodies the
`006C9CD0`/`006CABxx`
dispatch cluster calls are
the parameter-write idiom -
each stores its field and
raises the record's dirty
bits:

`00628620` (16 B):
`+0x30 = (dl != 0)`,
`[rcx] |= 4`.
Interior anchor `0062862A`
(the `+0x30` store).

`006285C0` (60 B):
`+0x2C = 1`; `+0x34` takes
`0061C010(r8d)` when `dl`
holds, else 8; `[rcx] |= 4`.
Interior anchor `006285D7`
(the `0061C010` call).

`00628520` (73 B): the mode
write - `edx` 0/1/2 stores
`+8 = edx + 1` (clamped to
the 1..3 range), `+0xC = 0`
and `[rcx] |= 1`;
out-of-range `edx` still
sets bit 0 and clears `+0xC`
but leaves `+8` untouched.
Interior anchor `00628532`
(the `+8 = 3` store).

`00628380` (81 B): packs
the four flag bytes into
`+0x84` - each `cmove`
selects between the raw bit
and its `| 2` / `| 4` /
`| 8` variant, so `+0x84`
ends as `b0 | b1<<1 |
b2<<2 | b3<<3` - and sets
`[rcx] |= 2`.
Interior anchor `006283C7`
(the `+0x84` store).

`00627FF0` (90 B):
`+0x64 = 0`, `+0x68 = dl`,
then four `0061BF40` hashes
over `r8d`, `r9d` and the
two stack qwords land at
`+0x6C`/`+0x70`/`+0x78`/
`+0x7C`; `[rcx] |= 2`.
Interior anchor `00628010`
(the first `0061BF40`
call).

## SWE2-EC7-123 update (2026-09-21) - `0061C010`, `00623FA0` and `0061D180` measured

`0061C010` (75 B) is the
clamp the parameter setters
call - not a hash:
`ecx <= 7` jumps an
8-entry table returning
`ecx + 1` (1..8), anything
above returns 8. The
`006285C0`/`00628570` writes
are therefore
`min(level + 1, 8)`.
Interior anchor `0061C01F`
(the jump-table load).

`00623FA0` (67 B) is the
fifth member of the
inline-or-heap getter family
`00620F60`/`00622BA0` drive:
`+0x30` count under `btr
0x1f`, `edx` bound-check,
0x58-stride records on
`+0x38`, returns `+0x10`.
`0062A0A0` and `006C8CA0`
call it for the dyngeo
records.
Interior anchor `00623FC2`
(the `+0x10` fetch).

`0061D180` (221 B) is the
flag-masked resource bind
`006C8CA0`/`006CA8D0` call:
bit 0 of `r8d` binds
`+0x168` (or `+0x170` when
`+0x9C4 == 2`) through
`[+0x110]`'s
`vtable[+0x158]`; bit 1
binds `+0x180` through
`vtable[+0x118]` with a
zeroed 16-byte descriptor
and `-1`; bit 2 binds
`+0x178` through
`vtable[+0x120]` with the
`+0x188` byte. Each arm is
independent and skipped when
the slot or its flag is
absent.
Interior anchor `0061D1DB`
(the `vtable[+0x158]`
bind).

## SWE2-EC7-124 update (2026-09-21) - `0061C8A0` is the dyngeo staged copy

`0061C8A0` (118 B) - the
two-part `vtable[+0x90]`
copy bound to the `02CED880`
cursor - is what
`006C8CA0`/`006CA8D0` run
when streaming dyngeo
parameter blocks; see the
`game-settings-ini` batch-88
section for the full body
read (both calls, the
`02CED990`/`02CED890`
tables, the cursor update).
Interior anchor `0061C8FF`
(the remainder copy).

## The instance is three parallel ten-entry arrays (OPUS, 2026-09-21)

Carved from `002142A0` read whole while assembling
[`CONTRACT-text-control-codes-and-dyngeo-draw.md`](../CONTRACT-text-control-codes-and-dyngeo-draw.md),
and declared in `_types`. **This completes FABLE's 2026-09-14 correction in §4** — that `+0x50` and
`+0x58` belong to two different ten-entry arrays rather than being a plain/shadow field pair — by
giving the arrays their extents and their strides.

`002142A0` sets `r12d = 0xA` (`002142B4`), `r14 = this + 0x08` (`002142C9`) and `r15 = this + 0xA8`
(`002142BA`), and advances `r14 += 8` / `r15 += 4` exactly ten times (`002143A0`–`002143A8`). Per
layer it reads `[r14]` as the source (`002142D0`, tested non-null and handed to the target's slot 8
at `0021432A`), `[r14 + 0x50]` as the vertex base (`00214332`) and `[r15]` as the vertex count
(`0021432D`). So:

```
+0x08 .. +0x57   void*[10]   layerSource      stride 8
+0x58 .. +0xA7   void*[10]   layerVertices    stride 8
+0xA8 .. +0xCF   uint32[10]  layerCount       stride 4
```

and they tile: `0x08 + 10×8 = 0x58`, `0x58 + 10×8 = 0xA8`, `0xA8 + 10×4 = 0xD0`. Nothing in the body
touches anything past `+0xCC`.

**The vertex stride is 48 bytes and the batch ceiling is 480 vertices**, both read rather than
assumed: `0021433A mov r12d, 0x1e0` with the clamp at `0021434B cmovg`, and the source offset
`lea r8, [rcx + rcx*2]` then `shl r8, 4` at `00214356`–`0021435D` — count × 3 × 16. A layer of more
than 480 vertices is drawn in several passes, the loop subtracting at `00214394`.

**A layer with no source, or a count of zero, is skipped whole** (`002142D6`, `00214338`), and
nothing accumulates across layers — so the ten may be drawn in any order without changing the
result.

**One caution for §3's destructor row.** It is right that the sizes are `0x160`, `0x170` and
`0x168` — those are the `free` arguments at `00213AE8`, `00213AB8` and `00213B18`. What the row does
not say is that **all three destructors stamp the same vtable, `00906DE8`**, before freeing
(`00213AE0`, `00213AB0`, `00213B10`). So the vtable a destructor writes does not identify its class;
only the size does, and `Shadow` and `ShadowFinal` share both the body and the size.

**And the four variant vtables were resolved from `.rdata` rather than from the method lists.** They
are contiguous at a `0x68` stride — an RTTI-locator qword plus twelve slots — with bases `00906DE8`
(Special), `00906E50` (Shadow), `00906EB8` (Final) and `00906F20` (ShadowFinal). **Exactly four
columns differ, 2, 6, 10 and 11**, confirming §10's overturn from the bytes; the other eight hold
identical pointers, and slot 0 is `0016D6A0` — the three-byte `ret 0` that `/OPT:ICF` folded every
empty function in this image onto. `DynGeoFontTextInstance`'s table at `00906DC8` is three slots,
confirming the three-shape split in §2.
