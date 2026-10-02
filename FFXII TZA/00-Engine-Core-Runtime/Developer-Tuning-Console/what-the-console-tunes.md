---
system: What the developer console tunes — the render settings block
category: 00-Engine-Core-Runtime
status: DOCUMENTED — the rate at which PhyreEngine invokes slot 8 answered from the framework's own update (once per frame, PA-5); the 144-vs-29 disjointness verified; the integer word at block +0xB4 is the last-applied MSAA sample count (RC-7, answered: 0 = off); the cascade count stays 3 (RC-8, answered); owner read 2026-09-30 (OPUS, `_index/candidates/dd-owner-read-b1-0930/` round 3)
owner_layer: none — the block is shared engine state, no single PrimaryOwner
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
last_reviewed: 2026-09-03
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-what-the-console-tunes-pass-1
  crossref_clean: false
  reopened_count: 0
---

# What the developer console tunes

> The console's 86 hottest addresses sit in one 1,132-byte block, and ~~25 functions read it~~ 28 functions reference
> it, 24 of them accessing it *(corrected 2026-09-30, SWE2-CONTRACT; §8)*. This
> document identifies what the block **is**: FFXII: The Zodiac Age's **render settings** — ambient
> occlusion, depth of field, shadows, image-based lighting, and the post-processing layer as a whole.
> **§4 now names 29 of its offsets**, and shows that the range is really two disjoint things: a
> console-tunable settings area and an eight-entry uniform array the console cannot reach.

## 1. What the player sees

**The settings screen Square Enix kept for themselves.**

The remaster added effects the PlayStation 2 original could not have: soft focus that blurs the
background behind a speaker, ambient shadowing where surfaces meet, smoother edges, a warmer
graded image. None of those has a switch in the retail options menu. They are on, tuned to values
somebody chose, and the player never sees the dial.

**The dials exist.** They sit in a 1,132-byte block of memory the developer console can nudge one
step at a time, and the names the engine uses for them are in the executable: `EnableAO`,
`EnableDof`, `EnableShadow`, `EnableIBL`, `EnableYebis`, `ShadowBias`, `AODepthFullRes`. Somebody
sat in front of the running game with a controller, walked a menu, and moved these until the game
looked the way it ships.

**What makes this a tuning console rather than a debug readout** is that the same block is read by
the code that actually draws the frame. The console is not showing you numbers; it is editing the
values the renderer is about to use.

## 2. Native mechanism

### The block

```
02CB7FD0 .. 02CB8438      1,132 bytes, as delimited by the console arms
86 distinct addresses touched by console arms, 81 of the 85 gaps exactly 4 bytes
.data past the raw image - but NOT uninitialised: a C++ static object, see below
```

> **Corrected 2026-09-03: "uninitialised, built at run time, no file image" was wrong.** The block
> is a **C++ static object** with a constructor and an `atexit` destructor, and its defaults are
> immediates in `.text`. `00162410` is the static initializer, verified from its bytes:
>
> ```asm
> 00162414  48 8D 0D B5 5B B5 02   lea  rcx, [rip+0x2B55BB5]   ; -> 02CB7FD0, the block
> 0016241B  E8 00 A3 47 00         call 005DC720               ; the constructor
> 00162420  48 8D 0D 99 93 74 00   lea  rcx, [rip+0x749399]    ; -> 008AB7C0, the destructor
> 0016242A  E9 60 67 6A 00         jmp  atexit
> ```
>
> **The object is far larger than the block** — `005DC720` initialises fields out to `+0x1020`. The
> 1,132 bytes are only the part console arms happen to touch.

A densely packed array of 4-byte values. The console arms step them with `addss`/`subss`; the
consumers read them with `movss`.

**It is not one array.** §4 splits the range into a console-tunable settings area at `+000..+18C`
and an eight-entry uniform array at `+190..+38C` that no console arm touches — the two populations
are disjoint.

### Who reads it — and this is the identification

Scanning `.text` for every RIP-relative access into the block, **with the SSE scalar-float forms
included** (an integer-only form list finds almost nothing here — see §8), gives ~~**25 referencing
functions**~~ **28 referencing functions, 24 of which access the block and 4 only take its address** *(corrected
2026-09-30, SWE2-CONTRACT: re-measured over `[02CB7FD0, 02CB843C)` by [`rip_refs.py`](../../_index/candidates/swe2contract-ddres-b1-0930/rip_refs.py) (output `rip_refs_block.out`); the four `lea`-only functions
are `00162410`, `001BC9D0`, `00607F00` and `008AB7C0`; OPUS's falsification pass 1 in §8 measured the same 28 and 24 on
2026-09-12)*. Five carry enough strings to name themselves:

> **Site counts corrected 2026-09-03** — `001D1660` read 337 and `001CD0E0` read 158 on first
> publication. The scan was double-counting prefixed instructions; see §8. **The function count of
> 25, and every identification below, are unaffected.**

| function | body | sites | what its strings say it is |
|---|---:|---:|---|
| `001D1660` | 13,753 B | 254 | the console itself — `"Screen Mode Change by Debug Menu !!!"` |
| `001CD0E0` | 11,276 B | 79 | the debug **menu renderer** — `"%s NOT EDITABLE"`, `"(EMPTY)"`, `"%s with skybox"`, `" steps (O to capture)"` |
| `001F0AD0` | 2,738 B | 154 | no strings; **144 of its 154 accesses are `movss` stores** — it writes the block wholesale. **The second-heaviest consumer** |
| `001C7940` | 11,445 B | 30 | **`EnableYebis`, `EnableAO`, `EnableIBL`, `EnableMapNormalMap`, `AODepthFullRes`, `ShadowBias`, `ShadowValueB`, `ShadowValueG`** |
| `001C3D50` | 4,607 B | 19 | the same family plus **`EnableDof`**, **`EnableShadow`** |

and three more identify the neighbourhood:

| function | strings |
|---|---|
| `00187950` | `"Post Process : color correction"`, `"update shadowmap"`, `"resolve render targets as default"`, `"render debug menu"`, `"output capture 4k images"` — a **render pass list** |
| `00186410` | `"PhyreScene::enableMsaaInternal()"` |
| `00186130` | `"PhyreScene::disableMsaaInternal()"` |

**`EnableYebis` names the middleware.** YEBIS is the post-processing layer this database elsewhere
tags `ThirdParty.Rendering.PPFX` / `Yebis`, and whose 325 shader techniques are catalogued in
[the post-processing effect catalogue](../../17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md).
**So one of the console's dials turns the entire post-processing layer on and off.**

### The loop this closes

`001C3D50` and `001C7940` are **the same two functions** that reference `mDofFocusDistance` and
`mDofApertureFnumber` — the two keys the cutscene sidecar reads out of
`JsonData/CutScenes/<name>.json`
([cutscene name slots](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)).

So the same code reads depth-of-field parameters from **two sources**:

```
a developer nudging the console        ->  02CB7FD0..02CB8438  ->  001C3D50 / 001C7940
a scene author editing a JSON sidecar  ->  mDofFocusDistance   ->  001C3D50 / 001C7940
                                                                      |
                                                        fParam_FocusDistance (a shader uniform)
```

**Three authoring routes — a console, a per-cutscene text file, and a shader parameter table — meet
in two functions.** That is the useful shape: a modder changing depth of field has to know which of
the three they are editing, and that the console's value is the default the JSON overrides per scene.

> **Stated at its evidence.** The two-source reading rests on **the same two functions referencing
> both** — a shared-consumer argument, not a traced dataflow. No code path was followed from either
> source to `fParam_FocusDistance`. §8 records what that does and does not support.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `001D1660` | `DevConsole_DispatchCommand` | 13,753 B | the console dispatcher; the 282 command arms are the targets it jumps to, and live inside the same body |
| `001CD0E0` | `DebugMenu_Render` | 11,276 B | draws the menu; reads the block to display current values |
| `001F0AD0` | — | 2,738 B | writes the block wholesale — 144 `movss` stores, no strings |
| `001C7940` | — | 11,445 B | render-feature settings: `EnableYebis`, `EnableAO`, `EnableIBL`, shadows |
| `001C3D50` | — | 4,607 B | the same, plus `EnableDof`; also reads the cutscene DoF JSON keys |
| `00187950` | — | 3,311 B | the render pass list |
| `00186410` | — | 497 B | `PhyreScene::enableMsaaInternal()` |
| `00186130` | — | 250 B | `PhyreScene::disableMsaaInternal()` |
| `006084B0` | — | 1,419 B | 7 sites, mixed `lea`/`movss` |
| `00186CD0` | — | 1,240 B | 7 integer-form sites |
| `001FF740` | `EASTL_LookupByCString` | 300 B | adapts the C-string key and delegates; the find itself is two levels down |
| `001FF6B0` | — | 130 B | ensures the variant is a map, then **tail-jumps** to `001FF4F0` |
| `001C51D0` | — | — | the preset-aware wrapper `001C3D50` uses instead |
| `00200B50` | `Variant_ReadFloat` | 41 B | tag 2 → `cvtpd2ps`, tag 1 → `cvtdq2ps`, else `0.0f` |
| `00200B80` | `Variant_ReadInt` | 31 B | tag 1 → `mov`, tag 2 → `cvttsd2si`, else `0` |
| `00200BE0` | `Variant_IsAbsent` | **7 B** | `cmp dword [rcx], 6` / `sete al` / `ret` — the tag is at offset **0**, no displacement. Selects the global default map. *(was stated as 8 B; corrected 2026-09-07, see the pass at the end)* |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02CB7FD0`–`02CB8438` | the tuning block | `.data`, uninitialised | 1,132 B; 86 console-touched addresses, 4-byte stride |
| `01F82D20` | — | `.data` | the console's hottest single address — see §7, ~~**not identified**~~ the `GameSettingConfig` singleton pointer (answered in §7 2026-09-14; cell updated 2026-09-30, SWE2-CONTRACT) |
| `01F813C8` | — | `.data` | the global default settings map, used when a key is absent from the scene's |
| `01F81300` | — | `.data` | the settings object most of the 153 settings are stored into, not the block |
| `01F82ED8`–`01F82F08` | — | `.data` | a second run of 11 named settings; see §4 |

Addresses are Ghidra image base `0x00120000`.

## 4. Data structures and formulas

### The block is two different things sharing one address range

The extent came from the console arms, so the first reading of it was "one packed array of settings".
Following the writers says otherwise. **Two disjoint populations occupy the range, and no address
belongs to both.**

```
+000 .. +18F   console-tunable settings    84 arm-touched addresses; 21 now named below
+190 .. +38F   8 x 64 B shadow matrices    001F0AD0; NO console arm touches it
+390 .. +44F   shadow scalars and counts   001F0AD0; includes the four mMapShadow* names below
+450 .. +470   copied separately           two of these are arm-touched and unnamed
```

**The whole range is one shader constant buffer, staged in CPU memory.** `006084B0` copies every
part of it into one destination object: `+000..+18F` sixteen bytes at a time into `dest+0x110`,
then `+190..+44F` in one 704-byte call to `005DEC50` into `dest+0x2A0`, then `+450..+470` field by
field. Nothing is left out and nothing else is interleaved.

> **The staging object is a snapshot, not the GPU layout (2026-09-27, OPUS).** `006084B0`'s destination is `00604750`'s local `rbp+0x270`, a
> 0x598-byte snapshot that is change-checked and double-buffered. It is not the compiled constant buffer. `00604750`
> then writes the shipped shaders' `SceneWideParameterConstantBuffer` (0x5F0 B) field by field from it, reordered in
> places. So a block offset plus 0x110 is a snapshot offset, **not** a cbuffer offset. The per-variable map is
> [members/scenewide-cbuffer-map.tsv](members/scenewide-cbuffer-map.tsv) (`UQ-22`).

**`001F0AD0` writes 144 addresses and exactly none of them is touched by a console arm.** That is
the load-bearing measurement: the function this document previously called "the wholesale writer of
the block" writes a region the console cannot reach, and never touches one the console can.

### The 8-entry array at `+190` — eight shadow-map matrices

`001F0AD0`'s 144 stores are field-by-field copies out of one live render object, and 128 of them
fall into a perfectly uniform pattern:

```
block+190 + n*0x40   <-  object+0x1C0 + n*0xD8      for n = 0 .. 7
  each entry: 64 contiguous bytes, 16 floats
```

**Eight entries, block stride 64 bytes, object stride 216 bytes, both exact across all eight.**

> **Correction — this first read here as "a vec4 then a 3×4 matrix", and that was emission order
> mistaken for layout.** The compiler emits each entry's last twelve dwords before its first four.
> Re-merging the 144 stores by *constant delta and destination contiguity*, with emission order
> discarded, collapses the sixteen dwords into **one 64-byte run** in both spaces. Sixteen
> contiguous floats on a 64-byte stride is a 4×4 matrix, not a vec4 beside a smaller one — and the
> mistake is the same one §8 records for names: **instruction order read as structure.**

**They are shadow-map matrices, and the call site says so without an inference.** `001F0AD0`'s only
caller is `00187950`, the render pass list, and the call sits inside a named scope:

```c
FUN_001D5630(marker, ctx, "update shadowmap");     // scope OPEN — the name is an argument
  if (flag == 0)  FUN_001F0AD0(src, ctx, param_1 + 0x690);
  else          { FUN_001F0AD0(src, ctx, param_1 + 0x358); flag = 0; }
FUN_001D5620(marker, ctx);                         // scope CLOSE
```

`001F0AD0` is the **only** call between the open and the close, in either arm. This is the same
construct the glyph document uses for `"display : draw Font"` — a name passed as an argument to a
scope-open, not a string that happens to be nearby.

**Where the matrices come from.** `001F0AD0` calls `001EF6D0` immediately before the copies, and
`001EF6D0` walks the same array:

```c
plVar25 = (longlong *)(object + 0x148);            // entry 0
do {
    ...                                            // frustum maths
    *(float *)(plVar25 + 0x18) = ...;  (**(code **)(*plVar25 + 8))(plVar25);   // set, recompute
    *(float *)(plVar25 + 0x19) = ...;  (**(code **)(*plVar25 + 8))(plVar25);
    FUN_0018A120((longlong)i * 0xD8 + 0x150 + object);
    i++;  plVar25 = plVar25 + 0x1B;                // 0x1B qwords = 0xD8
} while (i < *(int *)(object + 0x13C));
```

Each entry is an **object with a vtable**: vtable at `+0x00`, the 64-byte matrix at `+0x78`,
parameters at `+0xC0`, `+0xC4`, `+0xC8`, `+0xD0`, total `0xD8`. A float is written and a virtual
slot is called to recompute — the shape of a camera or frustum being retargeted per shadow slot.

**Eight slots, and a live count.** The copy into the block is unrolled eight times with no guard, so
all eight slots are always copied. How many are *in use* is `object+0x13C` — the same field that
bounds the loop above — and `001F0AD0` copies it to **`block+0x3E4`**.

**The names corroborate the structure from the other side.** The four `mMapShadow*` settings bound
below sit at `+438..+444`, inside the `+190..+44F` run that `005DEC50` copies in one call together
with the eight matrices. A shadow-fade setting sharing a copy unit with the shadow matrices is
agreement between two independent routes — the config loader's dataflow and the constant-buffer
copier's extent.

**The source object is the global at `01F82EA8`** (`001F0850` returns it; Ghidra types that function
`void` and shows an empty body, which is the third signature gap in this pass). It sits in the same
uninitialised `.data` neighbourhood as the second settings run below — which is a coincidence of
allocation, not evidence, and is not used as any.

### Name-to-offset binding — 29 settings

Both `001C7940` and `001C3D50` load settings out of a string-keyed map and store them. The idiom is
identical in both, and it is what makes a name and an offset meet:

```c
node = Lookup(sceneMap, "mMapAmbientColorR");     // 001FF740
if (TypeTag(node) == 6)          sourceMap = &DAT_01F813C8;   // 6 == absent -> the global defaults
else                             sourceMap = sceneMap;
node = Lookup(sourceMap, "mMapAmbientColorR");
DAT_02CB8070 = ReadFloat(node);                   // 00200B50 -> xmm0
```

`00200B50` and `00200B80` are the typed readers, confirmed from their bytes rather than from
Ghidra's signature (`00200B50` decompiles as `void` because the decompiler does not model its `xmm0`
return):

```
00200B50   tag==2 -> movsd + cvtpd2ps | tag==1 -> movd + cvtdq2ps | else xorps    -> float
00200B80   tag==1 -> mov eax          | tag==2 -> cvttsd2si       | else 0        -> int
00200BE0   tag==6                                                                 -> "absent"
```

**All 29 block settings are read through the float reader, so all 29 are floats.**

### Amendment 2026-09-03 — the key strings are individual, not a table

The setting names live in a packed run of NUL-terminated C strings at **`008FA700`–`008FAB00`**
(`mSAOFadeoutScale`, `mMapAmbientColorR`, `mMapFarPlane`, `ShadowValueR/G/B`, `EnableYebis`,
`EnableIBL`, the `lightShaft*` family, and more). A census of every reference into that region:

| | |
|---|---|
| references | **93** |
| landing exactly on a string start | **93** |
| landing mid-string | **0** |
| pointer arrays into the region, anywhere in the image | **0** |
| split by function | **84 in `001C7940`, 9 in `001C3D50`** — the two loaders this section already names |

> **The region cannot be indexed and nothing indexes it.** The strings are variable-length and packed,
> so there is no stride; and no pointer table exists to index them. **Every reference is a `lea` to one
> specific key** — so an instruction pointing into this region names a parameter outright, and an
> address here that looks like a table base is a specific datum.

**A name may be referenced more than once.** `ShadowValueB` (`008FA928`) has **three** references —
one in `001C3D50` and two in `001C7940` — so a census of a *name* counts lookups, not settings.

**No console arm references this region.** The same attribution run across all 227 dispatch arms
returned one hit, and reading it showed printable bytes (`ff~A`) that are not a name. **The console is
a consumer of the same authored data these loaders read, not the owner of a parallel naming scheme**
— its own row labels are a separate table, established in
[the slice-E catalogue](arm-catalogue-slice-E-ids-140-171.md) §4.

**Correction, recorded because the number was quoted before it was checked.** This amendment first
reported *"all 93 from `001C3D50`"*. That came from reading an **owner-column** count of
`{'(none)': 93}` as a function count, with only the first eight rows printed — and all eight happened
to be in `001C3D50`. The true split is **84 / 9**.

> **A summary line that aggregates one column will be read as aggregating the column you had in mind.**
> The fix is the same one that has worked all night: print the discriminator you intend to claim, and
> read more rows than the ones that agree with you.

| offset | address | setting | named by | console arm |
|---|---|---|---|---|
| `+028` | `02CB7FF8` | `mEyeMapSpecularIntensityAfterClampModifier` | both | yes |
| `+074` | `02CB8044` | `mDebugRefractionFactor` | both | yes |
| `+078` | `02CB8048` | `mDebugWaterSpecFactor` | both | yes |
| `+07C` | `02CB804C` | `mDebugWaterTexBlendFactor` | both | yes |
| `+080` | `02CB8050` | `mDebugWaterExtraFactorTwo` | both | yes |
| `+084` | `02CB8054` | `mDebugWaterCubemapFactor` | both | yes |
| `+088` | `02CB8058` | `mDebugWaterRoughnessFactor` | both | yes |
| `+08C` | `02CB805C` | `mDebugWaterParallaxFactor` | both | yes |
| `+090` | `02CB8060` | `mDebugWaterFresnelFactor` | both | yes |
| `+098` | `02CB8068` | `mWaterBias` | `001C7940` | no |
| `+09C` | `02CB806C` | `mMapIrrCubemapIntensity` | `001C7940` | yes |
| `+0A0` | `02CB8070` | `mMapAmbientColorR` | `001C7940` | no |
| `+0A4` | `02CB8074` | `mMapAmbientColorG` | `001C7940` | no |
| `+0A8` | `02CB8078` | `mMapAmbientColorB` | `001C7940` | no |
| `+0B0` | `02CB8080` | `mMapAmbientColorCutPercent` | `001C7940` | yes |
| `+0D0` | `02CB80A0` | `chrFresnelSpecularIntensity` | both | yes |
| `+0D4` | `02CB80A4` | `chrFresnelSpecularPower` | both | yes |
| `+0D8` | `02CB80A8` | `chrFresnelSpecularClampValue` | both | yes |
| `+0DC` | `02CB80AC` | `chrFresnelSpecularSkinIntensity` | both | yes |
| `+104` | `02CB80D4` | `mEyeABCubeMapBlendFactor` | both | yes |
| `+108` | `02CB80D8` | `mEyeABSpecularBlendModifier` | both | yes |
| `+114` | `02CB80E4` | `mEyeABSpecularShadowModifier` | both | yes |
| `+134` | `02CB8104` | `mEyeASpecularIntensityAfterClampModifier` | both | yes |
| `+158` | `02CB8128` | `mEyeBSpecularIntensityAfterClampModifier` | both | yes |
| `+168` | `02CB8138` | `mCubemapIntensity` | both | yes |
| `+438` | `02CB8408` | `mMapShadowFadeSpeed` | `001C7940` | no |
| `+43C` | `02CB840C` | `mMapShadowFadeRange` | `001C7940` | no |
| `+440` | `02CB8410` | `mMapShadowFlyingFadeSpeed` | `001C7940` | no |
| `+444` | `02CB8414` | `mMapShadowFlyingFadeRange` | `001C7940` | no |

**21 of the 86 console-arm addresses now carry a name.** The other 8 named offsets are loaded from
config but have no console arm — the console does not expose everything the loader sets.

> **The lookup is one step further down than the name correction at the end of this document says.**
> That note settles `001FF740` and places the find in `001FF6B0`. `001FF6B0` does not return — it
> **tail-jumps**:
>
> ```
> 001FF6B0 ends   48 8b 4b 08 …  E9 BE FD FF FF   jmp 001FF4F0     (E9, not E8 + RET)
> 001FF740 ends   48 8b c3  C3                    mov rax, rbx / ret
> ```
>
> So `001FF4F0` is the find, `001FF6B0` is the "ensure this variant is a map, then find" wrapper, and
> `001FF740` is the C-string adapter over both. **Ghidra types `001FF6B0` as `void`**, because it
> does not model a value returned through a tail call — the same modelling gap that types `00200B50`
> as `void`. Taking either signature at face value hides the value every setting is read from.

### Where the defaults come from — and why no scan in this document could see them

`005DC720` calls two field-setters, and the argument of each is fixed by the bytes, not inferred:

```asm
005DC742  48 8B F9              mov  rdi, rcx          ; rcx is still the block base
005DC745  E8 36 FE FF FF        call 005DC580          ; -> 005DC580(block + 0x000)
005DC74A  48 8D 8F D0 00 00 00  lea  rcx, [rdi+0xD0]
005DC751  E8 DA FC FF FF        call 005DC430          ; -> 005DC430(block + 0x0D0)
```

Between them, plus `005DC720`'s own stores, the chain writes **107 distinct block offsets** —
`005DC580` covering `+000..+0C4`, `005DC430` covering `+0D0..+180`, `005DC720` the tail at
`+42C..+468`.

> **Every RIP-relative scan in this document is blind to all of it.** The constructor writes through
> `this`, so every store is `[rcx+disp]` and carries no absolute address for a scan to match. A
> widened store scan over the 65 unnamed arm addresses — with a passing known-positive control —
> found **131 stores, all from `001D1660`, and nothing else in the image.** That absence was real
> for the instrument and false about the program. **The hole was not a missing instruction form; it
> was the addressing mode itself.**

**They are not two copies of one struct.** The first three values `005DC430` writes match
`005DC580`'s second, third and fourth — which invites reading the second range as the same struct
shifted. Tested across all fields at every 4-byte shift: the best is **4 of 38 overlapping fields**,
and at shift 0 it is **0 of 37**. Rejected. **Three consecutive values agreeing at the head of a
sequence is not a shifted copy.**

### The constructor's defaults, and what they say about the binding

**27 of the 29 named offsets have a default**, and they read as their names:

| offset | setting | default |
|---|---|---:|
| `+028` | `mEyeMapSpecularIntensityAfterClampModifier` | 1.1 |
| `+074` | `mDebugRefractionFactor` | 2 |
| `+078` | `mDebugWaterSpecFactor` | 3.59 |
| `+07C` | `mDebugWaterTexBlendFactor` | 1 |
| `+080` | `mDebugWaterExtraFactorTwo` | 1 |
| `+084` | `mDebugWaterCubemapFactor` | 0.88 |
| `+088` | `mDebugWaterRoughnessFactor` | 1 |
| `+08C` | `mDebugWaterParallaxFactor` | 0.04 |
| `+090` | `mDebugWaterFresnelFactor` | 3.81 |
| `+098` | `mWaterBias` | 0 |
| `+09C` | `mMapIrrCubemapIntensity` | 2 |
| `+0A0` `+0A4` `+0A8` | `mMapAmbientColor` **R G B** | **1 · 1 · 1** |
| `+0B0` | `mMapAmbientColorCutPercent` | 0.3 |
| `+0D0` | `chrFresnelSpecularIntensity` | 3.9 |
| `+0D4` | `chrFresnelSpecularPower` | 2.7 |
| `+0D8` | `chrFresnelSpecularClampValue` | −0.8 |
| `+0DC` | `chrFresnelSpecularSkinIntensity` | 2 |
| `+104` | `mEyeABCubeMapBlendFactor` | 0.5 |
| `+108` | `mEyeABSpecularBlendModifier` | 1 |
| `+114` | `mEyeABSpecularShadowModifier` | 1.15 |
| `+134` | `mEyeASpecularIntensityAfterClampModifier` | 0.66 |
| `+158` | `mEyeBSpecularIntensityAfterClampModifier` | 0.66 |
| `+168` | `mCubemapIntensity` | 0.6 |
| `+438` `+440` | `mMapShadowFadeSpeed`, `…FlyingFadeSpeed` | 0 |
| `+43C` `+444` | `mMapShadowFadeRange`, `…FlyingFadeRange` | — |

**This is a third, independent check on the binding, and it is semantic.** `005DC580` carries no
strings and knows nothing about names.

- **`mMapAmbientColor` R/G/B defaults to 1 · 1 · 1 — white.** Under the adjacency binding §8 rejects,
  the same three names would read **2 · 1 · 1**, which is not a colour anybody defaults to. **The
  defaults discriminate the two bindings, and they pick the one dataflow picked.**
- **`mEyeA…` and `mEyeB…` both default to 0.66** — an A/B pair sharing a value. Checked and reported
  because it is the obvious second control, but it **does not** discriminate: under the adjacency
  binding both would read 0.02, equal as well. **A control that agrees with you is not a control
  unless the alternative would have disagreed.**

### A second, smaller settings run outside the block

The same two loaders write thirteen more named settings to a separate run of globals. This is not
part of the tuning block and no console arm touches it:

| address | setting |
|---|---|
| `01DFE198` / `01DFE19C` | `mMapChrUpwardDirLightAngleThres` / `…ColorIntensity` |
| `01F82ED8` `01F82EDC` `01F82EE0` | `mMapChrAmbientIntensity` **R G B** |
| `01F82EE8` `01F82EEC` `01F82EF0` | `mMapChrAmbientOffset` **R G B** |
| `01F82EF4` | `mChrShadowSlopeOffset` |
| `01F82EF8` `01F82EFC` `01F82F00` | `mMapChrDirLightColorIntensity` **R G B** |
| `01F82F08` | `mChrShadowDepthBias` |

`01F82EE4` and `01F82F04` fall inside the run and are not named by either loader.

> **This does not identify `01F82D20`.** It is 0x1B8 bytes below this run in the same uninitialised
> `.data`, and proximity in uninitialised `.data` is not evidence of anything — §7 leaves it open.

### Where the other settings go

`001C7940` loads **153** distinct settings and `001C3D50` **97**, sharing 92. Only 29 reach the
tuning block. The rest are stored into a settings object held in `DAT_01F81300` — `ShadowBias`,
`ShadowValueR/G/B`, `EnableAO` and `AODepthFullRes` all land there, some through one-line setters
(`00193F70` writes `+0x1E9`, `00194300` writes `+0xF0`) — and into the second run above. **Naming
the block did not name most of the settings, because most of the settings are not in it.**

## 5. Call chain

```
game loads a scene's render config
  -> 001C7940 / 001C3D50   Lookup(name) -> typed read -> store
     -> 29 of the settings land in 02CB7FD0..02CB8438; the rest in the object at DAT_01F81300

developer presses a direction on a console row
  -> 001D1660              one of 282 command arms
     -> addss/subss on a 4-byte value in 02CB7FD0..02CB8438

meanwhile, every frame:
  001C7940 / 001C3D50      read the same block through movss
  00187950                 runs the render passes named by its strings
  001CD0E0                 draws the menu, showing the current values
```

**Do not confuse with:** the console's own scratch state. The point of this document is that the
block is **not** scratch — ~~25 functions read it, 24 of them outside the console~~ 24 functions access it, 23 of
them outside the console dispatcher `001D1660` and 22 outside both of the console's functions (the dispatcher and the
menu renderer `001CD0E0`) *(corrected 2026-09-30, SWE2-CONTRACT, from the re-measured accessor list in §8)*, so the
values are live engine settings rather than a display buffer.

## 6. Modding notes

- **The defaults *are* in the file, and they are patchable.** Corrected: this document previously
  said the block is uninitialised and there is nothing to patch. The defaults are immediates in
  `005DC580` (`+000..+0C4`), `005DC430` (`+0D0..+180`) and `005DC720` (`+42C..+468`) — §4 lists the
  27 that belong to named settings. **That, not `001F0AD0`, is where a default comes from.**
- **`EnableYebis` is the master switch for post-processing.** Turning it off removes the whole layer
  catalogued in the PPFX document, not one effect.
- **Depth of field has two authorities and the JSON is the later one.** A per-cutscene sidecar
  overrides for that scene; the block is what the rest of the game uses.
- **Twenty-nine dials now have names** (§4), including the eight `mDebugWater*` factors at
  `+074..+090`, the four `chrFresnelSpecular*` at `+0D0..+0DC`, and `mMapAmbientColor` **R/G/B** at
  `+0A0/+0A4/+0A8`. Those are the ones worth patching; they are floats, defaulted by the
  constructor and overwritten from config at scene load. **Nothing else writes them afterwards
  except `mCubemapIntensity` at `+168`**, which `001846B0` and `001846F0` each also store once.
- **Do not patch `+190..+434`.** `001F0AD0` rewrites all 144 of those addresses out of a live render
  object, so a value written there is gone by the next time it runs.
- **The console is reachable in a retail build** in the sense that the arms are present and the
  block is live — but nothing here establishes *how* it is opened, and this document does not claim
  a route to it.

## 7. What is not known

- [x] **Which offset in the block is which setting** — **29 named in §4**, 21 of them console-arm
      addresses. Done by dataflow through the config loaders, not by adjacency, which is wrong 26
      times out of 30 here (§8).
- [x] **The other 65 console-arm addresses** — **57 of them are set by the block's constructor
      chain**, through `this`, which no absolute-address scan can see (§4). The console is then
      their only writer.
- [x] ~~**Eight arm addresses with no writer found at all**: `+038`, `+040`, `+048`, `+068`, `+0E0`,
      `+0E8`, `+10C`, `+16C`. `005DC720` also contains a bulk fill Ghidra renders as an empty
      `do {} while` at `this+0xA1D`, which is the obvious place to look before concluding anything.~~
      **ANSWERED 2026-09-13 (OPUS): they are never written because they never need to be — the block
      is a static in the uninitialised tail of `.data`, so the loader zeroes it, and the constructor
      chain simply has no override for these eight. Zero IS their default.**
      **The block is `02CB7FD0`.** `00162410` is its static-init wrapper: `lea rcx, [02CB7FD0]`,
      `call 005DC720`, then `lea rcx, [008AB7C0]` and `jmp 00808B90` — the `atexit` registration of
      its teardown. `.data` has virtual extent `01DF0000`–`02F97530` but **raw size ends at
      `01F7E400`**, so `02CB7FD0` — and the whole object out to at least `+0x1020` — **has no file
      image and is loader-zeroed before any constructor runs.**
      **Every writer in the chain was tested per-offset, with the base translation applied**, which
      is the step that makes the test mean anything: `005DC720` calls `005DC580` with `rcx = this`
      (`005DC745`) but calls `005DC430` with **`rcx = this + 0xD0`** (`005DC74A`), so that setter's
      own displacements are **not** block offsets. Translated: `+0E0`, `+0E8`, `+10C`, `+16C` would
      need raw `0x10`, `0x18`, `0x3C`, `0x9C` in `005DC430`, and `+038`, `+040`, `+048`, `+068` would
      need those displacements in `005DC580`. **`005DC580` writes 43 offsets and `005DC430` writes 39;
      none of the eight appears in either.**
      **THE BULK FILL IS ELIMINATED BY CONSTRUCTION, not by inspection.** The `this+0xA1D` loop is not
      a memset — it re-invokes the same two setters at a stride and writes a record inline:
      `lea rbx, [rdi+0xA1D]`, then each iteration calls `005DC580` at `rbx-0x42D` and `005DC430` at
      `rbx-0x35D`, writes `[rbx-1]` through `[rbx+0x3B]`, and ends with
      **`lea rbx, [rbx + 0x598]`** / `sub rsi, 1` / `jne`. **`rbx` only advances.** Its first and
      lowest setter base is `this + 0x5F0` and its lowest direct write is `this + 0xA1C`, so
      **no iteration can reach any offset at or below `+0x16C`** — and all eight are between `+0x38`
      and `+0x16C`.
      **So "no writer found at all" was exactly right, and now it is explained rather than
      outstanding:** these eight are loader-zeroed fields with no constructor default, which leaves
      the console arms as their first and only writers — the same conclusion the bullet above reaches
      for the other 57, by a different route.
- [x] **What the eight entries at `+190` are** — **eight shadow-map matrices**, 64 contiguous bytes
      each, written inside the `"update shadowmap"` scope, built by `001EF6D0` from an array of
      vtable-bearing frustum objects at `object+0x148` stride `0xD8`, with the live count at
      `block+0x3E4`. See §4.
- [x] **UQ-24.** **Whether the eight slots are lights, casters or cascades** — **cascades**, answered on
      the register row (FABLE, 2026-09-16). Constructor `001EF2D0` builds eight `0xD8`-byte elements at
      `object+0x148` through `eh_vector_constructor_iterator`, and the live count at `+0x13C` is the
      **literal 3** — the "runtime value" premise is falsified. The same constructor authors ascending
      split distances `5.0`/`10.0`/`30.0` at `+0x808`–`+0x810` paired with growing depth biases
      `0.008`/`0.016`/`0.035` at `+0x870`–`+0x878`, plus two square 1024 shadow resolutions — a cascaded
      shadow map's shape, inconsistent with one-per-light. Eight built, three used; whether the five
      unfilled elements are dead capacity or reserved for an unentered mode is not settled.
      *Narrowed (2026-09-30 pointer, SWE2-CONTRACT):* no authored route raises the count. The cascade partitions are
      read into a 3 × 3 matrix whose sink `001A9B00` rejects either index `>= 3`, and `mCascadeNumber` is read by
      nothing and is `3` in all 284 sections that author it (W-9, ANSWERED 2026-09-15, on
      [the reflected render parameters page](../../17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md)).
      UQ-24's own bound stands: sixty dword writes to some `+0x13C` exist image-wide and only the constructor's is shown
      to be on this object.
- [x] **RC-8.** Whether the shadow object's cascade elements 3–7 (of the eight `0xD8`-byte elements at `+0x148`)
  can ever be used: whether any of the other image-wide `+0x13C` writes stores this object's live count, or whether
  the count stays at the constructor's literal 3. Registered 2026-09-30 (SWE2-CONTRACT); static.
  **ANSWERED 2026-09-30 (static; SWE2-CONTRACT on FABLE's record `rc789-fable-0930` (commit `8bdf31fcb`)): only the constructor writes it, so the count stays 3
  and elements 3–7 are built but never counted in.** The object is a `0xB08`-byte singleton with no vtable, published
  at `01F82EA8` (stores in the getters `001F0810` / `001F0850` / `001F1590` / `001F1600`, the last two at the
  inlined-creator sites `001F15D7` / `001F1650`) and copied once into `01F812C8` by `0015CC00`. *(Wording corrected
  2026-10-01 on SWE2-AUDIT-SPEC's [`auditspec-review-ddres-b3-0930`](../../_index/candidates/auditspec-review-ddres-b3-0930/REVIEW.md)
  narrowing 2 and FABLE's restatement at `a8aed6ca9`; `01F812C8`'s readers `001C3D50` / `001C7940` write other
  fields of the object, not `+0x13C`.)* Intersecting the functions that hold that pointer (widened through direct callees to 1 and 3 hops)
  with every non-stack store covering dword `+0x13C` leaves only the constructor's `001EF389` at 1 hop; the three extra
  functions at 3 hops each write a different, freshly allocated object. Tier 1. *Limit:* a pointer carried through an
  indirect call or a bulk copy is outside the census.
  *Corrected in part and corroborated 2026-09-30 by ORACLE's record [`rc8-cascade-count-0930`](../../_index/candidates/rc8-cascade-count-0930/README.md)
  (commit `b6d40efbd`): `01F82EA8` is not the object's only published location — a second cell, `01F812C8`, is filled by the
  static initializer `0015CC00` from `001F0850` and read by the scene-config loaders `001C3D50` and `001C7940`, and
  three getters return the pointer (`0015CC00`, `001AC7C0`, `001FB310`). ORACLE's flow, not bounded by hop count,
  follows that cell and those getters and **still finds only the constructor writing `+0x13C`**, so the conclusion
  stands. Its stated assumption: code given an element pointer does not write at a negative offset from it.*
- [x] **`01F82D20`, the console's hottest single address** — 18 commands touch it. It has **61
      referencing functions** spanning the console, the debug menu, `InputManager_*`, and a large
      cluster in the `0079xxxx`–`007Axxxx` audio-driver range, and every access found is a `MOV r32`
      read. **It is not part of the tuning block and it is not identified here** — a global read by
      audio, input and UI alike is not a render setting, and guessing further would be exactly the
      inference this database bans.
      **Answered 2026-09-14 (FABLE): it is the `GameSettingConfig` singleton pointer**, written once at `00798261` by `007980A0`
      ([the game-setting contract](../../19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md)); its 31 `u32`
      settings sit at `+4 × index` ([settings page](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md) §2).
      The 16 readers in `0079xxxx`–`007Axxxx` run from `00795DC0` to `007A3D50`. That is the platform layer: the constructor
      `007980A0`, the window-position store `0079EBA0`, the Steam language query `007A0C60`, and the code around `WinMain`
      `007A3770`. All of it sits below the SEAD sound library, so none of these readers is the audio driver. Settings of this kind are read by input, UI and platform code
      alike, which is why its readers span those subsystems.
- [x] ~~**When `001F0AD0` runs.** *What* it writes is now resolved — 144 field copies out of one live
      render object, none of them console-reachable — but nothing here establishes its cadence, and
      "per frame" is an assumption this document does not make.~~
      **ANSWERED IN SHAPE 2026-09-13 (OPUS): its cadence is set inside PhyreEngine, and nothing in
      the game can call it. That is not a failure to find the route — it is the route.**

      **The chain is complete and each link has exactly one predecessor:**

      ```
      001F0AD0  <- 00187950  <- 0017D090  =  GameApplication vtable slot 8  (008C5760 + 0x40)
       2,738 B      3,311 B       37 B        0 direct callers; one qword in .rdata, the vtable
      ```

      **Slot 8 is a framework callback, not a game entry point.** `PApplication`'s own slot 8 is
      `005C5230`, the **3-byte `xor eax,eax ; ret` stub** that
      [the framework-boundary page](../../22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md)
      already names as the shared empty override — **the same standing as slot 4, the frame tick**,
      whose base is that identical stub. The middleware calls the game.

      **And the game demonstrably cannot call it.** The application is the **static object at
      `01F7E350`** (constructed by `0015BC40`: base ctor `00792350`, then the vtable store at
      `0015BC61`). **All four references to that address in the whole image are construction or
      destruction**, and there are no others:

      | site | what it is |
      |---|---|
      | `0015BC40` ×2 | the static constructor — the base ctor, then `007A1190(this, 0x9CA5)`, a 7-byte setter writing `this+0x10D0` |
      | `008A6970` | the `atexit` teardown |
      | `00896280` | a **12-byte thunk**, `lea rcx,[01F7E350] ; jmp 00793250` — and `00793250` re-installs the `PApplication` vtable at `[rcx]`, so it is the base destructor |

      > **NOTHING IN `.data`, `.rdata` OR ANY OTHER SECTION HOLDS A QWORD EQUAL TO `01F7E350`.**
      > Scanned every non-`.text` section: zero. **No game code can obtain `this`, so no game-side
      > caller of slot 8 exists or could exist** — which is why no static route to "when" was ever
      > going to be found on this side of the boundary.

      **What remains, stated as a bounded residue rather than an unknown:** the *rate* at which
      PhyreEngine invokes slot 8. That is middleware-internal.
      *Answered since (2026-09-30 pointer, SWE2-CONTRACT): once per framework frame.* The middleware is in the image,
      and its per-frame update is the inherited slot 28 `0079C140`, run by the loop `00796490` (`00796613`). In order it
      calls slot 7 (input), slot 4 (animate), each viewport's render and then slot 8 (render, `0079C655`), logging
      `"App failed during render"` on a non-zero result; a non-zero result from any slot ends the frame, and the quit
      byte `+0x69` stops the update before any slot (PA-5 and PA-2 on
      [the Phyre application page](../../22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md),
      tier 1). The game's slot 8 then returns at once until the readiness latch `+0x113C` is set (PA-3). So
      `001F0AD0` runs once per rendered frame after readiness; how many frames per second that is follows the frame
      limit, not this chain. **A co-occurrence test does not
      settle it** — 115 functions issue a `call [reg+0x40]`, twelve of them alongside `+0x20`,
      `+0x30` or `+0x38`, and every one inspected is an unrelated object with members at those
      offsets. **`+0x40` is a displacement, not a signature**, which is the negative already recorded
      as 13ax.

      **Byproduct, recorded once:** `00896280` is **not in the function list** — one concrete,
      named member of the ~1,308 unlisted code blocks the progress denominator excludes.
- [x] Whether the 4-byte values are all floats — **the 29 named ones are**, each read through
      `00200B50`, which returns `xmm0`. The integer-form accesses in `00186CD0` and `00188DA0` fall
      outside the named set and are still unexplained.
      *Narrowed 2026-09-30 (SWE2-CONTRACT), static:* every one of them addresses one dword, block `+0xB4`
      (`02CB8084`), and it is the render path's **last-applied copy of the MSAA setting word at `01DF0900`**. An
      image-wide rip-relative census finds sixteen references in six functions: `00186CD0` stores it three times
      (`00186D31`, `00186D62`, `00186D7A`) and reads it four times; `00188DA0` reads it four times (`00188DC0`–`00188E04`);
      `PhyreScene::enableMsaaInternal()` `00186410` compares it with `[01DF0900]` (`00186453`) and, after rebuilding,
      stores `[01DF0900]` into it (`001865C6`); `PhyreScene::disableMsaaInternal()` `00186130` stores 0 (`001861F3`);
      and the render pass list `00187950` makes the same compare-then-store (`00187A9D`, `00187B92`). The function names
      are the strings each body logs (§2). That offset is not among the 29 named settings, not among the console's 97
      addresses and not in the shader-constant map. Census
      [`rip_refs.py`](../../_index/candidates/swe2contract-ddres-b1-0930/rip_refs.py), output `rip_refs_02CB8084.out`,
      tier 1 (access) + 2 (the logged names).
- [x] **RC-7.** What the MSAA setting word at `01DF0900` holds — the value the render path copies into block `+0xB4`
  (`02CB8084`) when it re-applies MSAA (`00186410`, `00187950`) and that `00186130` replaces with 0 when MSAA is
  disabled: a sample count, a quality index or an enable. Registered 2026-09-30 (SWE2-CONTRACT); static.
  **ANSWERED 2026-09-30 (static; SWE2-CONTRACT on FABLE's record `rc789-fable-0930` (commit `8bdf31fcb`)): the D3D11 multisample count, 0 = off.** It ships
  as 4. The settings path `00186CD0` derives it from the framework setting `[00796E20() + 0xD3C]`: 0 and 1 give 0 (MSAA
  flag `+0xDBA` cleared), any other n gives n. `enableMsaaInternal` passes it through render commands to byte `+9` of
  the render target (`00189110`), and the texture creator `0061FDA0` reads that byte into the descriptor's
  `SampleDesc.Count` (`rsp + 0x5C`): when the flag at `rsp + 0x24` is set, the descriptor is copied to `rsp + 0x78`,
  the primary is reset to `{1, 0}` and created at `006200E5`, and the multisampled copy is created at `00620188`;
  otherwise the multisampled descriptor is created at `006200E5`; 7 and 9 are remapped to count 4 / 8 with
  quality 16 *(restated 2026-10-01 on FABLE's record at `a8aed6ca9`, auditsem-review-takebacks2-0930 §7 N2)*. Tier 1.
  *Not claimed:* which values the shipped options menu writes to the framework setting.
  *Corroborated and extended 2026-09-30 by ORACLE's record [`rc7-msaa-word-0930`](../../_index/candidates/rc7-msaa-word-0930/README.md)
  (commit `b6d40efbd`): the framework `+0xD3C` writer is the boot store `0079856F` (through a `+0xD20` base, which a `+0xD3C`
  displacement census misses), and the `+0xDC8` source of the render pass list's store is `00189520`, fed only by the
  console arms; 2, 4 and 8 are MSAA 2x/4x/8x and 9 is the one coded mode (8 samples, quality 16). Which value a machine
  ends up with depends on `GameSetting.ini` and the capability mask.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The block spans `02CB7FD0`–`02CB8438`, 1,132 B, 4-byte stride | the console arm extraction in `console_arms.tsv`, reproduced here; measured exactly by falsification pass 1 (`HI − LO = 1128` + 4, 283 entries at a 4-byte stride) | ~~3~~ 1 *(corrected 2026-09-30, SWE2-CONTRACT)* |
| ~~25 functions reference it~~ 28 functions reference it; 24 access it, 4 only take its address | full RIP-relative scan of `.text` including SSE scalar forms; re-measured 2026-09-30 by [`rip_refs.py`](../../_index/candidates/swe2contract-ddres-b1-0930/rip_refs.py) (output `rip_refs_block.out`) — accessors `001846B0` `001846F0` `00186130` `00186410` `00186CD0` `00187950` `00188DA0` `001A2130` `001A5B00` `001A97F0` `001BD9D0` `001C3D50` `001C7940` `001CD0E0` `001D1660` `001E2AF0` `001EF6D0` `001F08A0` `001F0AD0` `001F1600` `001F3740` `001FA820` `001FB310` `006084B0`; `lea`-only `00162410` `001BC9D0` `00607F00` `008AB7C0` *(corrected 2026-09-30, SWE2-CONTRACT)* | 1 |
| `001C7940` / `001C3D50` reference `EnableYebis`, `EnableAO`, `EnableDof`, `ShadowBias` … | authored `.rdata` strings LEA'd from their bodies | 2 |
| `001CD0E0` is the menu renderer | its own UI strings | 2 |
| `00187950` is a render pass list | its own strings | 2 |
| `001C3D50` also references `mDofFocusDistance` | the same scan; independently found in the cutscene block | 2 |
| `001F0AD0` writes the block | 144 `movss` stores of its 154 accesses | 1 |
| 29 offsets carry the names in §4 | dataflow from the keyed lookup through the typed reader to the store, in the decompiled bodies of both loaders | 1 |
| `00200B50` returns a float, `00200B80` an int, `00200BE0` tests "absent" | their raw bytes, decoded; Ghidra types `00200B50` as `void` | 1 |
| `001F0AD0`'s 144 addresses are disjoint from the 29 named ones | set intersection, empty | 1 |
| The `+190` region is 8 entries of 64 contiguous bytes | 128 field copies re-merged by constant delta and destination contiguity, emission order discarded | 1 |
| They are shadow-map matrices | `001F0AD0` is the only call inside the `"update shadowmap"` scope opened by `001D5630` with that literal as an argument | 1 |
| Each entry is a vtable-bearing object of `0xD8` bytes with the matrix at `+0x78` | `001EF6D0`'s loop: `plVar25 + 0x1B` per iteration, virtual slot `+8` called after each parameter write | 1 |
| `block+0x3E4` is the live entry count | `object+0x13C` bounds `001EF6D0`'s loop and is copied there by `001F0AD0` | 1 |
| The whole block is one shader constant buffer | `006084B0` copies every part of it into one destination, `005DEC50` moving `+190..+44F` in a single 704-byte call | 1 |
| The block is a C++ static object, not uninitialised data | `00162410`'s four instructions: `lea rcx, block` / `call 005DC720` / `lea rcx, 008AB7C0` / `jmp atexit` | 1 |
| Its defaults come from `005DC580`, `005DC430`, `005DC720` | argument set-up read from bytes (`mov rdi,rcx` / `call`; `lea rcx,[rdi+0xD0]` / `call`); 107 distinct block offsets written | 1 |
| `mMapAmbientColor` R/G/B defaults to 1·1·1 | the constructor's immediates, from a function with no strings | 1 |
| The two default-setters are not the same struct shifted | all fields tested at every 4-byte shift: best 4 of 38, shift 0 gives 0 of 37 | 1 |
| Only the console writes the other 65 | widened store scan (RMW, INC/DEC and SSE forms included) with a passing control: 131 stores, all `001D1660` — **bounded by the `this`-relative hole above** | 2 |
| A second settings run at `01F82ED8`–`01F82F08` | the same dataflow, same two loaders | 1 |

### The instrument, and the control that made it trustworthy

**An integer-only form list finds almost nothing in this block**, because the values are floats and
every consumer touches them with `movss`/`movups`. The scan used here carries the SSE scalar forms
(`F3 0F 10/11/58/5C/59/5E`, `0F 28/10/2E/2F`) alongside the integer ones, and one REX-prefix
variant of each.

*Control:* the console arms listed in `console_arms.tsv` as touching this span — **91 arms** — must
appear. They all live inside one function, `001D1660`, and the scan finds it. **PASS.** A form list
missing the float accesses would still have found the console (its arms use `addss`) while missing
the consumers entirely, and **would have supported the opposite conclusion — that the block is
console scratch.**

### An over-count in my own scan, and why a known-positive control could not catch it

**The site counts first published here were inflated.** `F3 0F 10 05 …` (`movss`) matched my
`MOVSS load` form at the `F3` byte *and* my `MOVUPS` form at the `0F` byte, computing the **same
target** from two different site addresses; REX-prefixed integer forms did the same at the `48` and
the opcode byte. Corrected by advancing the scan past each matched instruction instead of by one
byte:

| function | published | correct |
|---|---:|---:|
| `001D1660` | 337 | **254** |
| `001CD0E0` | 158 | **79** |
| `006084B0` | 14 | **7** |
| `00186CD0` | 9 | **7** |
| `001F0AD0`, `001C7940`, `001C3D50` | 154 / 30 / 19 | unchanged |

**The console's own getter crosses layers the way every tuned-state accessor does** (Pass 22
2026-09-14): `00265020` — ~~the console-side fetch the arms share~~ the actor world-position getter *(corrected 2026-10-02, OPUS: `00265020` is the actor world-position getter: it copies three dwords from `[actor+0xB8]` to its three out pointers, `00265020+0x1A`–`+0x2E`; the force-fight flag reader is `00253B90`, `[01E0C2B8] == 0`)* — is called from
**combat-action** (`00307300`, `002F8060`, `00320E10`), **spawn** (`00234DA0`, `002350C0`,
`00234AF0`), **gameplay** (`0031ADB0`, `00339630`), **rewards** (`002FB150`, `00312280`) and
**combat-formula** (`00384F40`) — 11 caller edges — while `00792350` (the `01F7E350` base ctor)
calls **platform** `005CD0A0` and `001CD0E0` reaches **achievements** `003166F0`. The console
tunes state the whole engine reads; its accessors inherit that spread, they do not create it.

**The function counts — 25 here and 61 for `01F82D20` — were never affected**, because a doubled
site still names the same function. Nor is any identification in §2, which rests on strings.

> **This is a different species from the three matcher defects recorded elsewhere in this database,
> and it defeats the guard that caught those.** Those were *absences* — a form the scan could not
> see — and a known-positive control catches them, because the scan fails to find something you know
> is there. **An over-count finds the positive perfectly.** No control drawn from a document would
> have fired.
>
> **What caught it was internal consistency between categories:** `MOVSS load` and `MOVUPS` reported
> **82 and 82** in one function and **78 and 78** in another, and **5/5** and **1/1** elsewhere. Two
> independent instruction forms do not land on identical counts four times. **For an inflation
> defect the tell is a suspicious agreement inside your own output, not a disagreement with the
> world.**

### Where my count disagrees with the handoff

The work order states **28** functions reference the span; this scan finds **25**. The difference is
not reconciled. *Measured since (2026-09-30 pointer, SWE2-CONTRACT): OPUS's falsification pass 1 below counts
**28** functions with any rip-relative reference into the block (the work order's figure, reproduced) and **24** that
access it, the other 4 taking only its address. The 25 is this scan's floor, as the next sentence says; it is not a
property of the image.* My form list is certainly not exhaustive — three of my scans this session were too
narrow — and an access through a register loaded by an earlier `lea` is invisible to it entirely.
**Take 25 as a floor**, and the qualitative claim — that the great majority of readers are outside
the console — is unaffected either way.

### How many instances the central claim rests on

**The identification of the block as render settings rests on two functions**, `001C7940` and
`001C3D50`, and it now rests on a resolved name-to-offset binding rather than on their string tables
alone. It is strong because those two are also the block's third and fourth heaviest consumers and
because three further functions in the same set name render passes and MSAA — but it is **five
functions, not twenty-five**, and the other twenty carry no strings at all. *(The set is 24 accessors, not 25 — §8's
corrected row; the argument is unchanged: five of them carry strings. 2026-09-30, SWE2-CONTRACT.)*

**The binding in §4 rests on 48 store sites across the two loaders**, resolving to 29 distinct
offsets, 19 of which both functions bind identically. The `+190` array rests on **128 field copies**
in one function. **The whole of §4 is one function's decompilation for the array and two for the
names** — it is not corroborated by any consumer, because no consumer of these addresses carries a
string that names one.

### The binding method, and the adjacency rule it replaced

**The obvious way to bind a name to an offset is to take the string nearest the store. It is wrong
26 times out of 30 here, and it fails silently.**

The compiler schedules the next setting's `lea rdx, "name"` *before* the current setting's store, so
the string physically nearest a `movss` into the block is usually the **following** setting's name.
Adjacency therefore produces a table shifted by one — and a shifted table reads perfectly plausibly:
it puts `chrFresnelSpecularPower` at `+0D0` and `chrFresnelSpecularClampValue` at `+0D4`, one slot
off, in a run where every name is a `chrFresnelSpecular*`.

The binding published above instead follows the decompiler's dataflow: the variable a `Map_Find`
returns, the typed reader that consumes that variable, and the store that consumes the reader's
result. Measured against it:

| function | adjacency agrees | adjacency wrong |
|---|---:|---:|
| `001C7940` | 4 | **26** |
| `001C3D50` | **19** | 0 |

> **`001C3D50` would have validated the adjacency rule completely.** Nineteen of nineteen. A session
> that checked its method on that function and then applied it to `001C7940` would have published
> twenty-six wrong rows with a passing control behind it. **A heuristic verified on one function is
> verified on one function** — the two differ only in how the compiler scheduled them, which is not
> a property anything in the method can see.

**The control that catches it is semantic, not statistical.** Four RGB triples appear across the two
loaders — `mMapAmbientColor`, `mMapChrAmbientIntensity`, `mMapChrAmbientOffset`,
`mMapChrDirLightColorIntensity`. A colour triple must land on three consecutive slots in R, G, B
order. The dataflow binding puts all four in R, G, B order; adjacency puts `mMapAmbientColorB` at
**both** `+0A0` and `+0A4` and drops R entirely. The parse never saw the letters.

This is a third species of instrument defect, after the absences and the over-count recorded above:

> **An absence disagrees with the world; an over-count agrees suspiciously with itself; a
> mis-binding does neither — it produces a complete, plausible, well-formed answer.** What catches
> it is a fact about the subject matter that the instrument had no access to.

### Whether the two loaders are independent

`001C7940` and `001C3D50` agree on all 19 offsets they both bind, with zero disagreements. **They
are not clones** — 153 settings against 97, 61 names unique to the first, 5 to the second, different
order, and different lookup wrappers (`001FF740` direct against `001C51D0`, which walks a preset
chain first). So the agreement is real corroboration that the extraction is not a parser artifact.

**It is weaker corroboration of the binding itself**, because both were written by the same authors
against the same setting names; if the source got a name wrong, both would carry it. The independent
check on the binding is `001F0AD0`: its 144 addresses and these 29 are **perfectly disjoint**, and a
mis-assigned address set has no reason to be disjoint from an unrelated function's write set.

## 9. Related

- [`ARM-CATALOGUE-WORK-DIVISION.md`](ARM-CATALOGUE-WORK-DIVISION.md) — the extraction this builds on,
  including its own warning that the TSV's `step` column is unreliable.
- [`the-282-command-parameter-console.md`](the-282-command-parameter-console.md) — the console itself.
- [`../../17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md`](../../17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md)
  — what `EnableYebis` switches on: 325 shader techniques.
- [`../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)
  — the per-scene depth-of-field override that lands in the same two functions.


### Name corrected 2026-09-03 — `DevConsole_DispatchCommand`, not `DebugConsole_CommandArms`

This document named `001D1660` after its **arms**; its sibling names it after what it **does**. Two
documents in one folder disagreeing about one address, caught by `check_consistency`.

**The prologue settles it, re-read from the image:**

```
001D1673  41 0f b6 f0        movzx esi, r8b    ; arg 3 -> sil
001D1677  0f b6 da           movzx ebx, dl     ; arg 2 -> bl   (the direction flag)
001D167A  48 8b f9           mov  rdi, rcx     ; arg 1 -> rdi  (the settings object)
001D167D  41 81 f9 19 01..   cmp  r9d, 0x119   ; ids 12..293
001D16A3                     mov  r9d, [table + id*4]
001D16AB                     add  r9, rcx      ; RVA -> VA, then jmp
```

**Rebase the id, save three arguments, bounds-check, index a table, jump. That is a dispatcher**, and
the arms are what it jumps *to*.

> **Naming a dispatcher after its callees names the function after the thing it is not.** The arms do
> live inside the same body — which is what made the wrong name plausible — but "every command arm
> lives inside it" is a fact about the *layout*, not about what the function is.

Adopted the sibling's name, which also carries the signature the prologue confirms:
`(void *ctx, u8 direction, u8, int id)`.


### Name corrected 2026-09-03 — `001FF740` is a lookup wrapper, not a constructor and not the find

Two documents named this address differently and **neither name was right**: `Map_FindByName` in one,
`EASTL_LookupByCString` in the other. Decompiled and settled:

```c
uVar3 = FUN_001edf00(local_res10, "EASTL basic_string", ...);   // named allocator
do { lVar4++; } while (*(char *)(param_2 + lVar4) != '');      // inline strlen of ARG 2
if (uVar2 < 2) { puStack_38 = &DAT_02eba2e0; ... }              // shared empty sentinel
else            puStack_38 = (**(code **)(local_28[0] + 0x10))(...);  // allocate
memmove(...); *puStack_38 = 0;                                  // copy + terminate
uVar3 = FUN_001ff6b0(param_1, &local_40);                       // DELEGATE
(**(code **)(local_28[0] + 0x18))(local_28, local_40, ...);     // FREE
return uVar3;                                                   // return the DELEGATE'S result
```

> **Not a constructor: it destroys the string on the way out and returns another function's result.
> Not the find either: the lookup is `001FF6B0`.** It converts a C string to the container's string
> type, delegates, and cleans up. **20 callers.**

**Each author saw one half of it** — the string construction at the top, or the by-name lookup it
serves — and each named the whole function after the half they were reading.

**The EASTL evidence is unaffected and this is worth stating separately from the name.** The
no-short-string-optimisation claim rests on this body's control flow — **one branch at length 1, the
shared sentinel at `02EBA2E0`, both arms writing the same three pointers** — and every one of those is
visible in the decompilation above. **The reasoning was right; the label on the function was not.**

## Independent re-derivation of `001F0AD0` — 2026-09-03, session `repos-78`

`001F0AD0` sits on the SSE-density list at 50 % with zero loops, **unbracketed by the vendor column and
already read in detail here** — cited only at its entry, so every instrument still reports it as
unopened. **This is the read-but-uncited mode on a list built from instruction counts rather than
citations**, which is why the vendor column cannot clear it: **an interior anchor is what clears a
function from any of these lists.**

Re-derived from the image without reference to the text above, and **every figure agrees**:

| claim above | re-derived | |
|---|---|---|
| **144** `movss` stores | **144** `movss` with a memory destination | ✔ |
| writes `+0x190 … +0x44F` of the `02CB7FD0` block | span **`02CB8160` … `02CB8404`**, and `02CB7FD0 + 0x190 = 02CB8160` | ✔ |
| **8 × 64 B** shadow matrices | **128 stores** inside `02CB8160`–`02CB835F`, **exactly 16 per 64-byte block** | ✔ |
| writes the block wholesale | **150 of 155 gaps between write targets are exactly 4 bytes** | ✔ |

**A population note, since two counts differ and neither is wrong:** this document says *144 of its 154
accesses*; the SSE census says **260**. The census counts **all seven SSE move mnemonics in both
directions** — this body also contains 96 `shufps`, 59 `movaps` and 44 `movups` — while 144 is
specifically **`movss` with a memory destination**. There are also **13 `movss` loads** and 156 distinct
rip-relative write targets in total. **Four different true numbers over four different populations.**

### Interior anchors

**The eight matrices are written by eight unrolled blocks**, sixteen stores each, at a regular code
stride of about `0xE4` — consistent with the zero loops the census reports:

| matrix | destination | first store | last store |
|---:|---|---|---|
| 0 | `02CB8160`–`02CB819F` | `001F0C03` | `001F0CC3` |
| 1 | `02CB81A0`–`02CB81DF` | `001F0CE7` | `001F0DA7` |
| 2 | `02CB81E0`–`02CB821F` | `001F0DCB` | `001F0E8B` |
| 3 | `02CB8220`–`02CB825F` | `001F0EAF` | `001F0F6F` |
| 4 | `02CB8260`–`02CB829F` | `001F0F93` | `001F1053` |
| 5 | `02CB82A0`–`02CB82DF` | `001F1077` | `001F1137` |
| 6 | `02CB82E0`–`02CB831F` | `001F115B` | `001F121B` |
| 7 | `02CB8320`–`02CB835F` | `001F123F` | `001F12FF` |

The remaining **28 writes** land above `02CB835F`, in the scalars-and-counts region, ending at
`001F1543` → `02CB83E8`.

**Nothing above is retracted.** The purpose of this section is that the eight rows are now checkable
line by line rather than as a summary — and that the function stops registering as unread on an
instrument that has no other way to tell.

## Interior anchors for `001EF6D0` and `0018A120` — 2026-09-03, session `repos-78`

Both sit on the SSE-density list (49 % and 48 %) **unbracketed and already described here**, cited only
at their entries — the same read-but-uncited mode as `001F0AD0` above, **three times in one document.**
Re-derived from the image; **every claim this document makes about them is confirmed.**

### `001EF6D0` — four claims, four anchors

| claim above | anchor | |
|---|---|---|
| entries are `0xD8` bytes (`plVar25 + 0x1B` per iteration) | `001F04A8` `imul rcx, rax, 0xd8`; `001F04CE` `add r14, 0xd8` | ✔ |
| the loop is bounded by `object + 0x13C` | `001F04DF` `cmp r13d, dword ptr [rbx + 0x13c]` | ✔ |
| a virtual call at slot `+8` after each parameter write | `001F0470`, `001F0482`, `001F04A2` — `call qword ptr [rax + 8]` | ✔ |
| `FUN_0018A120(i * 0xD8 + 0x150 + object)` | `001F04A8`–`001F04B9`: `imul rcx, rax, 0xd8` / `add rcx, 0x150` / `add rcx, rbx` / `call 0x18a120` | ✔ |

**One refinement:** the document says *"virtual slot `+8` called after each parameter write"* — there
are **three such call sites**, not one, at `001F0470`, `001F0482` and `001F04A2`. **The claim is right
and the count was not stated;** all three go through the same slot.

### `0018A120` — what the per-entry call does

**111 instructions, no loops, and it is a matrix build with a fallback:**

```asm
0018A132  mov    rax, qword ptr [rcx + 0xb0]      ; a source pointer
0018A13C  movaps xmm0, xmmword ptr [rip + …]      ; four constant rows, loaded FIRST
0018A143  movaps xmm1, …
0018A14A  movaps xmm2, …
0018A151  movaps xmm3, …
0018A158  test   rax, rax
0018A15B  je     0x18a1fc                          ; null -> keep the constants
0018A161  movss  xmm0, dword ptr [rax + 0xc]      ; otherwise gather, permuted
0018A166  movss  xmm1, dword ptr [rax + 0x1c]
0018A16B  movss  xmm2, dword ptr [rax + 0x2c]
```

> **The four constant rows are loaded before the null test, not after it.** They are the identity-style
> default, and a source object with a null `+0xB0` yields them unchanged — **so a missing matrix is a
> defined result here, not a skipped write.**

The gather reads `+0x00 +0x04 +0x08 +0x0C +0x10 +0x1C +0x20 +0x2C` and scatters them to non-adjacent
stack slots — **a transpose, not a copy.**

**Nothing above is retracted.** These anchors exist so the rows are checkable individually, and so the
two functions stop registering as unread on an instrument that counts instructions rather than
citations.

## Falsification pass 2026-09-07 — `00200BE0` is 7 bytes, not 8

Raised mechanically by `audit_crossrefs.py` as the only **BODY DRIFT** in the whole database
(374 findings, 373 of them `UNACCOUNTED NEIGHBOUR`). Settled **from the authorized image**, not from
the Ghidra annotation that raised it.

### The bytes

`00200BE0` lives at file offset `0xE01E0` in `.text` of the authorized EXE
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8` (image base `0x00120000`):

```
83 39 06        cmp   dword ptr [rcx], 6      ; 3 bytes
0F 94 C0        sete  al                      ; 3 bytes
C3              ret                           ; 1 byte
CC CC CC ...                                  ; int3 padding to the next function
```

**3 + 3 + 1 = 7.** The next function begins at `00200BF0`, so the nine bytes between are padding and
not body.

### Why 8 was reachable, which is the part worth keeping

`cmp dword ptr [rcx], 6` and `cmp dword ptr [rcx+8], 6` differ by exactly one byte — the ModRM
`disp8`. The first encodes `83 39 06`; the second `83 79 08 06`. **Hand-encoding the instruction with
a displacement that is not there gives 4 + 3 + 1 = 8**, which is the number this document carried.

> **Every sibling accessor in this family does take a displacement** — `Variant_ReadFloat` and
> `Variant_ReadInt` both read a tag off a field, so the expectation of a `disp8` is the natural one.
> `Variant_IsAbsent` is the one that reads the tag at offset **0**, and that is a fact about the
> structure, not only about the encoding: **the tag is the first member.**

**Anywhere this database states a body size that was counted by hand rather than measured, the same
one-byte slip is available** — and a `disp8`/no-`disp8` confusion silently changes an offset claim as
well as a size claim.

### What survived

The semantic reading is untouched: the function tests `tag == 6` and returns the boolean, which is
what selects the global default map. **Only the size and the operand form were wrong.** The
document's §8 evidence row — *"their raw bytes, decoded"* — is the right method; it was applied to
`00200B50` and `00200B80` correctly and mis-added here.

### Program state

Graph and ledger: GN160 `fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`
(`00200BE0` = 7 B, `NativeLeaf.MemberComparisonPredicate`, no owner). Binary: the authorized EXE
above, read directly. **Both agree; the document was the outlier.**

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### Exact

| claim | measured |
|---|---|
| the block spans `02CB7FD0`–`02CB8438`, **1,132 B**, 4-byte stride | `HI − LO = 1128`, **+4 for the last entry = 1,132**; 283 entries at a 4-byte stride |
| `001F0AD0` writes the block — **144 `movss` stores** | **144**, and they land on **144 distinct addresses** — one store each, no address written twice |
| … **of its 154 accesses** | **154 scalar accesses: 144 `movss` + 10 `mov`.** Two further `movups` bring the raw total to 156, and they are *vector* stores — the page's unit is the scalar form, which is what *"including SSE scalar forms"* signals |

The `154` is a good example of a count that is right and looks wrong: a scan that takes every
reference gets **156**, and the two it adds are the only non-scalar accesses in the function.

### Not reproduced: "25 functions reference it"

Neither natural unit gives 25:

| unit | count |
|---|---:|
| functions with **any** rip-relative reference into the block | **28** |
| of those, functions that only take its **address** (`lea`) — `00162410`, `001BC9D0`, `00607F00`, `008AB7C0` | 4 |
| functions that **access** it | **24** |

**28 referencing, 24 accessing, and the page says 25.** The gap is one either way, which is what a
slightly different scan boundary produces — a body bound differently in `functions.tsv`, or one of the
four `lea`-only functions counted as an accessor. **Recorded rather than adjusted**: with two
candidate units both a step away, choosing one would substitute a preference for a measurement.

### Not checked

*"`001F0AD0`'s 144 addresses are disjoint from the 29 named ones."* The 144 are in hand — one per
`movss`, all distinct. **The 29 named offsets are not in a form this pass could extract
mechanically** from §4, and reconstructing the set by hand would make the intersection a test of my
reading rather than of the claim. Left unverified and said so.
*Verified 2026-09-30 (SWE2-CONTRACT): disjoint.* The 29 were extracted mechanically as the distinct block targets of
the two loaders' stores, not from §4's prose. `block_writer_disjoint.py` reproduces 144 distinct `movss` targets in
`001F0AD0` (C1), 29 distinct loader targets (C2) from 48 `movss` store sites (C3; the loaders' 30 + 19 site column also
counts one integer `mov` at `001C8FB5`, to `+0x43C`), and, as the positive control on the intersection itself, the 29
meet the console dispatcher's block write targets in exactly 21 (C4, §7's "21 of them console-arm addresses"). The
intersection of the 144 and the 29 is **empty**. Control
[`block_writer_disjoint.py`](../../_index/candidates/swe2contract-ddres-b1-0930/block_writer_disjoint.py), tier 1.

**Not claimed:** nothing here was executed or observed live.

## The `001CD0E0` exclusive subtree — the renderer's 28 helpers (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 28 frontier functions to `DebugMenu_Render` (`001CD0E0`).
All signature-swept 2026-09-15 (`bshape.py`):

| cluster | members | role |
|---|---|---|
| `008F6600` record builders | `001C0330` (197 B — `001EDF00` ×4 + `001B3860`/`001A4BF0`, `008F9A70`–`80`), `001C0480` (181 B — `001EDF00` ×3 + `001E3E90`/`001BE660`/`001A4BF0`, `01CEB638`), `001C0540` (234 B — `001EDF00` ×4 + `001A4BF0` ×2 + `001A9930`/`001A74A0`, `01CEB638`), `001A74A0` (338 B — `001A2F70` ×2 + `001EDF00`/`001A4BF0`/`001A9E50`/`001A5760`, `[rax+0x18]` virtual), `001BE660` (`001EDF00`/`001A4BF0`) | the per-row label/value materializers — `008F6600` is their shared format bank |
| `001C08xx` quad | `001C0820`, `001C0870`, `001C08C0`, `001C0910` | four identical 69 B bodies reading `01CEBBA8` — four row kinds differing only in payload |
| `009009xx` format writers | `001DCB90` (404 B — `001A1E40` ×2 + `0020D2B0`/`0020DA50`/`0020D9F0`/`001CD050`, `00900958`/`C0`), `001DCD30` (190 B — `001A1E40` + `008C2810`/`009009A8` + `01F82D20` config), `001DCDF0` (`00900A00`), `001DCE20` (`00900960`/`70`), `001DCE60` (`0090097C`/`88`/`98`) | the `"%s%s%f"`-family emitters — `009009xx` is the format-string bank |
| leaves | `0017E010` (`01DF0010`/`18`), `0017F5E0` (`001AD440` ×2), `0018A790`/`0018A7B0` (17 B twins), `0019C500` (`0019C5D0`, `008F3F60`/`88`), `001AC7A0`, `001C0440`/`001C0630` (60 B pair), `001DC9C0`, `001E3E90`, `0026E0F0` (`0209A6F0`), `002EEED0` (`0215FD40`), `00308E80` (`00D10394`), `003091C0` (100 B — `003272F0`/`0031ABF0`/`00265970`/`00265020`) | fetch and emit steps between the row builders |

The tree is exactly what a 11 KB menu renderer should own: row materializers, format emitters,
and cell readers — no logic the menu's id-table page doesn't already attribute to the console.

**One caveat on "own": the four fetch leaves under `003091C0` are shared accessors, not
console-private.** `00265020` is also called by 16 **Movement**-layer bodies (`0033CA00`,
`00311E20`, `00311F70`, `003B7E20`, `002E45E0`…), `00265970` by four more, `0031ABF0` and
`003272F0` two and three respectively — 25 edges in all. The console *displays* values locomotion
code also reads; the getters belong to the tuned-state surface, not to this menu.

## The `001D1660` exclusive subtree — the dispatcher's 26 helpers (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 26 frontier functions to `DevConsole_DispatchCommand`
(`001D1660`). All signature-swept 2026-09-15 (`bshape.py`):

| cluster | members | role |
|---|---|---|
| `008FAxxx` twin builders | `001C7360`, `001C7520` (446 B each, identical shape: `001FF740` ×4 + `00200BE0`/`001FEE10`/`001EDF00` ×2 + `00202930`, `[rax+0x10]`/`[rax+0x18]` indirect, templates `008FA338`/`008FA350` vs `008FA368`/`008FA388`) | two near-identical record materializers — a command-pair pattern (same builder, adjacent template blocks) |
| command-arm bodies | `001D5120` (257 B — 13-helper chain `001DE5A0`/`00189120`/`001DE4F0`/`0018AC50`/`001BDAB0`/`001BD940`/`001A9930`/`001A5B00`/`001F0850`/`001EF520`/`001DE570`/`00189520`/`00193D50`, `[r8+0x60]` virtual, `01F7E340`/`01F82D20`), `002EEEE0` (295 B — `002ED6F0`/`002DF980`/`002DF8E0`/`0017D280`, `00D0F870`/`B0`/`C0` table), `002112D0` (`007A4380`/`007A4C70`/`007A45C0`/`001243B0` — Phyre calls), `00182E10` (`001DDAB0` ×3/`001DC940`), `001DF2C0` (`01F82D20` config), `001DE4F0` (`00900CC0`/`E0` strings) | the larger arm bodies the 282-case dispatch reaches |
| `0018B0xx` quad | `0018B070`, `0018B080`, `0018B090`, `0018B0A0` | four identical 14 B thunks — one per command entry |
| leaves | `0017E7A0` (`01DF0010`), `00193F80`, `001AC390` (227 B), `001AD4D0`, `001D5230`, `001DBB00` (`00210B30`), `001DD090`, `001EF500`, `002D4F70` (`01E0CF84`), `002D4F90`, `002F1CD0`, `002F4510`, `002F7A00`, `002FBA50` | fourteen 7–295 B bodies — cell reads and forwarders the arms share |

The tree matches the dispatcher's shape: the 282 command arms live *inside* `001D1660` (§90);
the subtree is what those arms call outward to — mostly emit/record helpers, no second
dispatch layer.

*(Pass 22 live-graph completion, 2026-09-15: the tuned-state surface also reaches
`RNG_Random_Selection` — `00234AF0` calls `00328370`, `002F8060` calls `00379CD0` (2) — and
`Story_Event_Quest_Hunt` — `002F8060` calls `0032AD70` (1). Consumers of tuned state include
the random stream and the quest side; same inherited spread.)*

## The `001C7940` exclusive subtree — the loader's 12 store helpers (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the 153-setting loader **12 frontier functions** — the
typed-store layer under the `Lookup(name) -> typed read -> store` idiom of §5. Interior cites are
one instruction inside each declared extent (`interior_cite.py scan`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| settings-object field writers | `00194370` (79 B), `00194400` (109 B), `001C78D0` (106 B) | the multi-field stores: `00194370` writes `+0xA4..+0xC0` (three floats + four dwords from an arg record), `00194400` the wider `+0xC4..+0xE8` float block, `001C78D0` a converted vec pair through `001C4F50` → `001A9930` ×2 | `00194383` / `0019440E` / `001C78DD` |
| change-gated dials | `001A9A70` (45 B), `001A9AA0` (45 B), `001A9AD0` (41 B) | set-if-changed: scale the argument (`divss`/`mulss` constants), compare against the current field (`ucomiss`/`jp`/`je`), store and notify (`jmp 001A7770`) only on a real change — `01CEBC50` referenced | `001A9A88` / `001A9AB8` / `001A9AE7` |
| indexed setters | `001A9B00` (34 B), `001A9B30` (52 B), `001A9D70` (42 B), `001A9DA0` (42 B) | `001A9B00` a bounds-checked 3×3 cell store `+0x350 + (r*3+c)*4`; `001A9B30` a vec3 store `+0x374..+0x37C` with dirty flag `+0x398`; the `001A9Dxx` pair write `+0x344 + i*4` then recount through `00265920` → `001A7E40` | `001A9B09` / `001A9B40` / `001A9D79` / `001A9DA9` |
| flag + global | `001943C0` (49 B), `00182FE0` (7 B) | `001943C0` — `+0xEC` byte set with the `+0xED`/`+0xEE` handshake flags; `00182FE0` — one-line global store `[01F7F504] = ecx` | `001943CA` / `00182FE6` |

This is the write side of the load: `001C7940` resolves each authored name and hands the value
to the matching member — vector stores, dirty-flagged triples, and change-gated dials that
notify (`001A7770`) only when the setting actually moves. The members write the object at
`DAT_01F81300`'s surface, not the `02CB7FD0` block directly — consistent with §4's finding that
most settings land outside the console's range.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** Cited functions are called by `BattleUnit_RunPeriodicCombatMaintenance` (twice), `BattleUnit_RecoverFromTerminalStatusSetIfClear`, `BattleStats_ChangeStatusAndProcessSideEffects` and `BattleFormula_AdvanceStatusTimersAndBuildResult`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (45 edges through 21 of this page's functions).** The ActorEntity layer reaches this page at `002350C0`, `00265020`, `0031ADB0`, `002E45E0` and 17 more. `BattleUnit_GetSlotCount` is the worked example, read in full - it is **seven bytes** returning the global at `[0208E6A0]` - and the storage initialiser sets that global to `0x20`, so the pool is **32 slots**; **10 of the 22 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — SERVICE.** `00307300` on this page calls `BattleEnmity_ApplyActionParameters`, owned by that layer. What it reaches is the parameter pass: `byte[+5] == 0` on the stats record, then `byte[+0x1D]` of the parameter block and `byte[+4]` of the record decide what is written; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — CLIENT (25 edges through 14 of this page's functions).** The Party layer reaches this page at `00265020`, `00311E20`, `0031ABF0`, `002350C0` and 10 more. `FUN_00263750` is the worked example, read in full - it is **23 bytes**: an index of 3 or less into the **four-entry pointer table at `0209A1F0`**, and a null for anything above; **7 of the 14 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio, Presentation, Resource — CLIENT (shared-callee edges, SWE2-EC7-188).** The notify-sweep callee `0016D6D0` is a generic list-visit helper also reached from the audio, presentation and resource layers (`00220550`/`0021D280`/`002206B0` on the audio side; `001BD4A0`/`001BC190`/`001ACF80` on the presentation side; `0020BFA0`/`006761F0`/`0020B840` on the resource side), and the change-gated dials `001A9A70`/`001A9AA0`/`001A9AD0` are additionally driven by presentation caller `001C7940`. The crossing is those layers consulting shared helpers this page happens to name, not shared responsibility. Edge list from `edges.tsv`.
- **Application — CLIENT and SERVICE (5 edges).** 4 inbound (Application bodies `0015BC40`, `001A97F0`, `008A6970` call page-cited `001AD440`, `00792350`, `00793250`); 1 outbound (page-cited `00186CD0` call Application bodies `001A98B0`). Substantive edges include `00186CD0` calls `001A98B0`; `001AD440` is called by `001A97F0`; `00792350` is called by `0015BC40`; `00793250` is called by `008A6970`.
- **Input — CLIENT and SERVICE (25 edges).** 21 inbound (Input bodies `0017DDC0`, `00196710`, `001967D0` call page-cited `00796E20`, `0079EBA0`); 4 outbound (page-cited `0079C140`, `00796490`, `007980A0` call Input bodies `0079A120`, `0079E520`, `0079D010`). Substantive edges include `00796490` calls `0079A120`; `007980A0` calls `0079E520`; `0079C140` calls `0079D010`; `0079C140` calls `0079D920`; the remaining edges run through shared helpers the page cites.
- **RNG_Random_Selection — CLIENT and SERVICE (3 edges).** 1 inbound (RNG_Random_Selection bodies `BattleData_ResolveWeightedId` (00308EC0) call page-cited `RNG_SharedGameplayLCG_NextU32` (00328370)); 2 outbound (page-cited `Spawn_TrySelectCandidatePosition` (00234AF0), `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (002F8060) call RNG_Random_Selection bodies `RNG_SharedGameplayLCG_NextU32` (00328370), `RNG_MT19937_NextU32_Thunk` (00379CD0)). Substantive edges include `Spawn_TrySelectCandidatePosition` (00234AF0) calls `RNG_SharedGameplayLCG_NextU32` (00328370); `RNG_SharedGameplayLCG_NextU32` (00328370) is called by `BattleData_ResolveWeightedId` (00308EC0); the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — CLIENT and SERVICE (8 edges).** 3 inbound (Save_Load_Settings bodies `GameSettingConfig_ParseText` (001DE5D0), `GameSettingConfig_ParseOneSettingValue` (001DF350), `SaveImage_FinalizeHeaderAndChecksum` (00583D60) call page-cited `0017D280`, `003166F0`); 5 outbound (page-cited `007980A0`, `00265920`, `PersistentFlag_SetBank512Low` (0032AD70) call Save_Load_Settings bodies `SaveImage_GetPersistentPayloadBase` (002EF2B0), `GameSettingConfig_LoadOrCreateFile` (001DED50), `GameSettingConfig_InitDefaultsAndPath` (001DE050)). Substantive edges include `003166F0` is called by `SaveImage_FinalizeHeaderAndChecksum` (00583D60); `007980A0` calls `GameSettingConfig_LoadOrCreateFile` (001DED50); `007980A0` calls `GameSettingConfig_InitDefaultsAndPath` (001DE050); `0079EBA0` calls `GameSettingConfig_WriteFile` (001DFD40); the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT (54 edges).** 54 inbound (Script_VM_Native_Bridge bodies `0050D240`, `0050D780`, `0050CE40` call page-cited `0017D280`, `Actor_GetWorldPosition` (00265020), `00265920`). Substantive edges include `00265920` is called by `0050D360`; `00265920` is called by `00356250`; `002ED6F0` is called by `003580C0`; `PersistentFlag_SetBank512Low` (0032AD70) is called by `00353750`; the remaining edges run through shared helpers the page cites.
- **Story_Event_Quest_Hunt — SERVICE (1 edge).** 1 outbound (page-cited `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (002F8060) call Story_Event_Quest_Hunt bodies `PersistentFlag_SetBank512Low` (0032AD70)). Substantive edges include `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (002F8060) calls `PersistentFlag_SetBank512Low` (0032AD70).
- **UI — MECHANICAL (2 edges).** 2 UI-side calls into shared helper(s) the page cites (`Actor_GetWorldPosition` (00265020), `00796E20`) - the helpers' general call surface, not a UI relationship of this page's subjects.
- **WorldAreaField — CLIENT and SERVICE (16 edges).** 5 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020), `00379290`, `00379A10` call page-cited `RNG_MT19937_NextU32_Thunk` (00379CD0), `0017D280`, `00265920`); 11 outbound (page-cited `001CD0E0`, `Spawn_TrySelectCandidatePosition` (00234AF0), `SpawnLifecycle_CheckAndRetireByNativeRange` (002350C0) call WorldAreaField bodies `FieldData_GetActiveFieldRecordBit15` (00313F60), `FieldData_GetActiveFieldRecordBit15` (00377C20), `WorldTransition_GetTransitionFieldId` (00314910)). Substantive edges include `001CD0E0` calls `WorldTransition_GetTransitionFieldId` (00314910); `001CD0E0` calls `FieldData_GetVariable0` (00265270); `Spawn_TrySelectCandidatePosition` (00234AF0) calls `FieldRegion_ContainsWorldPosition` (002374E0); `Spawn_TrySelectCandidatePosition` (00234AF0) calls `003209C0`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT (54 edges).** 54 inbound (Script_VM_Native_Bridge bodies `0050D240`, `0050D780`, `0050CE40` call page-cited `0017D280`, `Actor_GetWorldPosition` (00265020), `00265920`). Substantive edges include `00265920` is called by `0050D360`; `00265920` is called by `00356250`; `002ED6F0` is called by `003580C0`; `PersistentFlag_SetBank512Low` (0032AD70) is called by `00353750`; the remaining edges run through shared helpers the page cites.
## The `001C3D50` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`001C3D50` (4,607 B) is the second scene-config loader §98 names — the one
that also registers `EnableDof`/`EnableShadow`. Its mode byte lands at
`01F81418` (`001C3D86`), it builds the `01F812D0`/`01F813D8`/`01F813A8`/
`01F813F8` registry headers through `00200BE0` (`001C3DB4`–`001C3E84`), and
then runs the registration battery: **94 calls to `001C51D0`, 3 to `001C52C0`,
1 to `001C7850`**, interleaved with `00200B50` ×83 and `00200B80` ×19 row
stores.

| member | role | interior |
| --- | --- | --- |
| `001C51D0` (232 B) | the preset-aware registrar — six `001FF740` name/`00200BE0` slot pairs over the `01F813xx`/`01DF6E50` registry, `"Common"` category `008FA3CC` (`001C5233`), gated on `[01F81418]` (`001C51F5`) | [`001C5233`](../../_index/ADDRESS-INDEX.md) |
| `001C52C0` (227 B) | the sibling registrar — same `"Common"` shape, alternate tail at `001C537B`–`001C538F` | [`001C532E`](../../_index/ADDRESS-INDEX.md) |
| `001C7850` (114 B) | the vec4 registrar — `xmm2` constant `008FCCA0` (`{0, 1.0, …}`), four `movss` repack, `001C4F50`, `001F0850`, `001F08A0` (`001C7854`–`001C78B8`) | [`001C78A8`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00200BE0`, `00200B50`, `00200B80`,
`001FF740`, `001FF6B0`, `001C4F50`, `001F0850`, `001F08A0`, `001A9930`,
`001CC9A0`, `001EDF00`, `00194250`, `001A52A0`, `00194A00`, `001949E0`.

## The `008AB7C0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`008AB7C0` (~12 B) — `lea rcx, [02CB7FD0]` then `jmp 005DDDB0`
(`008AB7C0`/`008AB7C7`) — registers the `02CB7FD0` record with the
`005DDDB0` registration body; sibling `008AB7D0` loads `rax` from
`02CBF998`.

| member | role | interior |
| --- | --- | --- |
| `005DDDB0` | the registration body | [`005DDDB0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

`001A7770` (213 B) is the notify sweep the change-gated dials (`001A9A70`/`001A9AA0`/`001A9AD0`) tail-jump to: it walks the `[rcx+0x4A0]` listener list to the `[rcx+0x498]` sentinel via `0016D6D0`, stamps each node `+0x30 = 0`, `+0x28 = +0x484`, `+0x24 = +0x480`, and when `+0x488` float is nonzero adds `(+0x488 * 2 * rand() / 32766.0) - +0x488` to `+0x24` - the dial's random-spread option (`008C3098` is `rand`)

Interior anchor `001A7819` (function `001A7770`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*Functions this page named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`console_interior.py`](../../_index/candidates/opus-console-interior-1001/console_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0015CC00` | 21 B | stores the pointer `001F0850()` returns in qword `01F812C8` | `0015CC09` |
| `0017E010` | 19 B | returns the address of the 8-byte entry `01DF0018 + 8*[dword 01DF0010]` | `0017E017`, `0017E01E` |
| `0017E7A0` | 36 B | adds `ecx` to dword `01DF0010` and stores the sum, except that a negative sum is stored as 2 and a sum above 2 as 0 | `0017E7AA`, `0017E7BA`, `0017E7BD` |
| `0017F5E0` | 38 B | returns dword `+0x168` of the object `001AD440()` returns, or -1 when there is none | `0017F5F3`, `0017F5FE` |
| `00182E10` | 59 B | when `001DDAB0()` is non-null, calls `001DC940(it, cl)`, then tail-jumps to `001DC730` with `001DDAB0()` in `rcx` | `00182E2E`, `00182E40` |
| `001846B0` | 57 B | calls `001E0580` and `001EB940(001EBA40())`, copies float `01F7F53C` to `02CB8138`, then tail-calls `0018CCF0(0018CA40(), 1)` | `001846C1`, `001846CE`, `001846E4` |
| `001846F0` | 75 B | calls `001E0580`, copies float `02CB8138` back to `01F7F53C` and zeroes `02CB8138`, calls `0018CCF0(0018CA40(), 0)`, then tail-calls `001EB7B0(001EBA40(), ecx)` | `00184708`, `00184710`, `00184722`, `00184736` |
| `00189110` | 15 B | copies byte `+8` of the object at qword `+0x10` to byte `+9` of the object that object's first qword points to | `00189117`, `0018911B` |
| `0018A790` | 17 B | returns 1 when bytes `+0` and `+1` are both non-zero, else 0 | `0018A795`, `0018A79B` |
| `0018A7B0` | 17 B | returns 1 when bytes `+0` and `+2` are both non-zero, else 0 | `0018A7B5`, `0018A7BB` |
| `00196710` | 184 B | works on the pointer table at qword `+0xDF8` of `00796E20()`: for entries at offsets `0x118`-`0x148` up to the first null, calls `00861EC0(entry + 0x30, 0, 0x100)`; for each non-null entry at `0x88`-`0x110`, zeroes the 17 bytes at `+0x30`; for the entry at `0x150`, zeroes word `+0x1E0` and byte `+0x1E2` | `0019673B`, `00196741`, `00196782`, `001967B5`, `001967BC` |
| `001AC7A0` | 21 B | returns `rcx + 0x204 + 32*[dword +0x200]` (32-byte records from `+0x204`) | `001AC7A7`, `001AC7AB` |
| `001AC7C0` | 66 B | when byte `+0xA4` is non-zero and dword `+0xA8` is -2, sets `+0xA8` to -1 and, when `001F0850()` is non-null, tail-calls `001EF540(it, 1)` | `001AC7C4`, `001AC7CD`, `001AC7D6`, `001AC7F8` |
| `001AD4D0` | 62 B | stores `edx` modulo the qword count of the vector at `[+0xE8]` in dword `+0x168`, or 0 when that vector is empty | `001AD4E1`, `001AD4F9`, `001AD4FC`, `001AD503` |
| `001BD9D0` | 128 B | takes float `01DFE194` when byte `01DFE190` is set and its magnitude is at least 0.001 (double `008F9558`), else 0.0; stores that in float `02CB8154`, or 0.0 when byte `+0x118` of `001EBA40()` is set | `001BD9EA`, `001BDA0B`, `001BDA19`, `001BDA22`, `001BDA3E` |
| `001BE660` | 86 B | zeroes qwords `+0`, `+8` and `+0x10`, calls `001EDF00(rcx + 0x18, r8)`, then `001A4BF0(rcx, rdx, rdx + strlen(rdx))` for the C string in `rdx`; returns `rcx` | `001BE66F`, `001BE684`, `001BE693`, `001BE6A3` |
| `001C0440` | 60 B | returns float `+0x20` of the record at qword `+0x18` when the count of 40-byte elements in `[+0x58, +0x60)` is non-zero and qword `+0x10` is non-null, else 0.0 | `001C0452`, `001C0455`, `001C046B`, `001C0476` |
| `001C0630` | 60 B | returns float `+0x34` of the record at qword `+0x18` when the count of 40-byte elements in `[+0x58, +0x60)` is non-zero and qword `+0x10` is non-null, else 0.0 | `001C0642`, `001C0657`, `001C0662` |
| `001C4F50` | 237 B | starts a stack vector from the constant (1, 0, 0, 1) at `008FCCA0`; calls `00203170` on a stack block, `00202F70` with the stack (fifth) argument and `00202F00` with `xmm3`, each multiplied by 3.14159 (`008FCC94`) and divided by 180 (`008F3138`), then `00202B70`; stores the result's first float through `rcx`, its second through `rdx` and its third, negated by the sign mask `01CEBDA0`, through `r8` | `001C4F73`, `001C4FA4`, `001C4FB1`, `001C4FF2`, `001C500D` |
| `001D5230` | 46 B | steps dword `+0xC` up when `dl` is non-zero, else down, wrapping 4 to 0 and a negative value to 3 | `001D5234`, `001D5239`, `001D5244`, `001D5256` |
| `001DBB00` | 46 B | tail-calls `002112D0(00210B30(), edx != 0, ecx)` | `001DBB0E`, `001DBB11`, `001DBB29` |
| `001DC940` | 116 B | steps an index up when `dl` is non-zero, else down, with wrap-around: when dword `+8` of `[01F82D20]` is 0, dword `+0x38` modulo `[+0x20]` (plus one slot when the 28-byte entry `[+0x40] + 0x1C*[+0x20]` has non-zero dwords `+0` and `+4`); otherwise dword `+0x24` modulo `[+0x20]` | `001DC947`, `001DC955`, `001DC976`, `001DC99A` |
| `001DC9C0` | 16 B | returns `[+0x78] + 0x140*[dword +0x48]` (320-byte records) | `001DC9C3`, `001DC9C7`, `001DC9CB` |
| `001DD090` | 32 B | returns dword `+0x130` of the 320-byte record `[+0x78] + 0x140*[+0x48]`, or dword `+0x5C` when `[+0x78]` is null | `001DD094`, `001DD0A0`, `001DD0A4`, `001DD0AC` |
| `001E3E90` | 28 B | returns qword `+0x80` of `[[rcx+0x18]]` minus its low bit | `001E3E94`, `001E3EA5`, `001E3EA8` |
| `001EF500` | 32 B | sets dwords `+0x130` and `+0x134` to 6 when `+0x130` was 2, else to 2 | `001EF50A`, `001EF510`, `001EF519` |
| `0020D9F0` | 96 B | calls virtual slot 1 (`[vtable+8]`) on `rcx`, then on each object along the qword `+8` links, until one returns non-zero; returns 1 when one did, else 0 | `0020DA0A`, `0020DA11`, `0020DA25`, `0020DA43` |
| `002112D0` | 105 B | on a stack object: `007A4380`, `007A4C70(r8d)`, then `007A45C0` with float 1.0 (`01CEBBA8`) when `dl` is non-zero, else 0.0, and finally `001243B0` | `002112EF`, `002112FC`, `00211316`, `0021131E`, `00211329` |
| `002D4F90` | 25 B | for `ecx` 1 to 5, stores it in dword `01E0CF88` and zeroes dword `0209E65C`; any other value is ignored | `002D4F93`, `002D4F98`, `002D4F9E` |
| `002F1CD0` | 13 B | stores `ecx` in dword `022BE7D8` and `edx` in dword `01EEBAE0` | `002F1CD6` |
| `002F4510` | 13 B | stores `ecx` in dword `022BE7DC` and `edx` in dword `01EEBAE4` | `002F4516` |
| `00308E80` | 51 B | reads qword entry `ecx` of the table at `022C24E0`; when it is non-null and its byte `+4` is below 6, returns qword entry `[+4]` of the table at `01EEC268`; otherwise returns the string `"Nobody"` at `00D10394` | `00308E8A`, `00308E9B`, `00308EA2`, `00308EAB` |
| `003091C0` | 100 B | calls `0031ABF0(003272F0())`; when that is non-null and `00265970` on it is non-null, calls `00265020(it, rcx, rdx, r8)` | `003091DD`, `003091E4`, `003091F4`, `0030920A` |
| `0050D360` | 59 B | when `00267E10(r9)` is non-zero, tail-calls `0026FAD0(0, 00265920(), byte +0x15 of rdx)`; otherwise tail-calls `0026FE50(0)` | `0050D36C`, `0050D375`, `0050D38A`, `0050D396` |
| `005DDDB0` | 186 B | passes the qword vector at `+0x1010` to `001A5A80` with its capacity in qwords and zeroes its three pointers; then, for the buffers at `+0x4A8` (size dword `+0x4A0`) and `+0x480` (size dword `+0x478`), calls `005F01B0` and `005F03A0` when bit 31 of the size is clear, and zeroes pointer and size | `005DDDEB`, `005DDDF1`, `005DDE0D`, `005DDE18`, `005DDE47` |
