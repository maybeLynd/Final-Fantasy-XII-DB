---
system: Arm catalogue — slice D, command ids 108–139
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: CodeDomain — mixed; no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: console-join-repos-55
  crossref_clean: false
  reopened_count: 0
---

# Arm catalogue — slice D, command ids 108–139

> Slice D of the division in [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md).
> **32 command ids. It says nothing about the other 250.**

## 1. What the player sees

Nothing — a developer tool. Slice D is the first range whose commands mostly **do not** tune the
console's own settings blob. **Thirteen of them fetch a live engine object and adjust a field of it**,
which makes these the first tuned values in the catalogue with a provenance outside the console.

## 2. Does the arm shape hold here? No — the dominant encoding is different

The first question asked of every slice. **Slice D answers it more sharply than A, B or C.**

| shape | slice D |
|---|---:|
| one constant, `subss K` down / `addss K` up | **6** |
| **signed pair**, `addss (−K)` down / `addss (+K)` up | **25** |
| integer step | 1 |
| unimplemented | **0** |

```asm
; the shape slices B and C are made of        ; the shape slice D is mostly made of
subss xmm0, [K]     ; down                    addss xmm6, [-K]    ; down
addss xmm0, [K]     ; up                      addss xmm6, [+K]    ; up
```

**Both are symmetric and both have a well-defined magnitude** — every signed pair in this slice is an
exact negative pair, so up and down cancel exactly. The difference is purely how the compiler encoded
the choice, and it matters only because **a classifier keyed on `subss` sees 25 of these 32 arms as
one-directional.** Slice D has 56 `addss` against 6 `subss`; that ratio is the shape, not an anomaly.

**This is the fourth slice and the fourth distinct shape profile** — A counters, B floats, C floats
plus a multiplicative arm and a re-seeder, D signed pairs through an engine accessor. **It is also the
first slice with no unimplemented ids at all.**

## 3. The catalogue

Row shape per the work order: **field · width · step magnitude · direction mechanism · bound.**
All targets are `f32` unless noted. `rax+…` is a field of the object returned by the engine accessor
described in §4; `02CBxxxx`, `01DFxxxx`, `01F82xxx` are globals.

| id | arm | target | magnitude | direction mechanism | bound |
|---:|---|---|---|---|---|
| 108 | `001D1FE6` | `02CB8130` | 0.02 | one constant, `subss`/`addss` | — |
| 109 | `001D201C` | `02CB8134` | 0.02 | one constant, `subss`/`addss` | — |
| 110 | `001D284B` | `02CB8138` | 0.02 | one constant, `subss`/`addss` | — |
| 111 | `001D2881` | `01DFE194` | 0.02 | one constant, `subss`/`addss` | — |
| 112 | `001D28B7` | `01F82ED0` | 0.02 | one constant, `subss`/`addss` | — |
| 113 | `001D28ED` | `02CB8144` | 0.02 | one constant, `subss`/`addss` | — |
| **114** | `001D2E18` | **`rax+0x2D0`** | 0.05 | signed pair `addss ±K` **+ clamp** | **`[0.0, 1.0]`** |
| **115** | `001D2E61` | **`rax+0x2D4`** | 0.05 | signed pair `addss ±K` **+ clamp** | **`[0.0, 10.0]`** |
| 116 | `001D2EAA` | **`rax+0x2D8`** | 0.05 | signed pair `addss ±K` | — |
| 117 | `001D38C8` | **`rax+0x2DC`** | 0.05 | signed pair `addss ±K` | — |
| 118 | `001D390D` | **`rax+0x2E0`** | 0.05 | signed pair `addss ±K` | — |
| 119 | `001D3952` | `02CB806C` | 0.05 | signed pair `addss ±K` | — |
| 120 | `001D2EEF` | `02CB8044` | 0.05 | signed pair `addss ±K` | — |
| 121 | `001D2F25` | `02CB8048` | 0.05 | signed pair `addss ±K` | — |
| 122 | `001D2F91` | `02CB8050` | 1.0 | signed pair `addss ±K` | — |
| 123 | `001D2FC7` | `02CB8054` | 0.03 | signed pair `addss ±K` | — |
| 124 | `001D2FFD` | `02CB8058` | 0.03 | signed pair `addss ±K` | — |
| 125 | `001D3033` | `02CB805C` | 0.01 | signed pair `addss ±K` | — |
| 126 | `001D3069` | `02CB8060` | 0.03 | signed pair `addss ±K` | — |
| 127 | `001D309F` | **`rax+0x2E8`** | 0.02 | signed pair `addss ±K` | — |
| 128 | `001D30E4` | **`rax+0x2EC`** | 0.02 | signed pair `addss ±K` | — |
| 129 | `001D3129` | **`rax+0x2F0`** | 0.001 | signed pair `addss ±K` | — |
| 130 | `001D316E` | **`rax+0x2F4`** | 0.5 | signed pair `addss ±K` | — |
| 131 | `001D31B3` | **`rax+0x2FC`** | 1.0 | signed pair `addss ±K` | — |
| 132 | `001D31F8` | **`rax+0x300`** | 0.01 | signed pair `addss ±K` | — |
| 133 | `001D323D` | **`rax+0x304`** | 0.02 | signed pair `addss ±K` | — |
| **134** | `001D3282` | **`[01F82D20] + 0x40`**, dword | 1 | `inc` / `cmov` pair | **wraps, 2 states** |
| 135 | `001D2F5B` | `02CB804C` | 0.01 | signed pair `addss ±K` | — |
| 136 | `001D32CA` | `02CB7FE8` | 0.01 | signed pair `addss ±K` | — |
| 137 | `001D3300` | `02CB7FEC` | 0.01 | signed pair `addss ±K` | — |
| 138 | `001D3336` | `02CB7FF0` | 0.01 | signed pair `addss ±K` | — |
| 139 | `001D336C` | `02CB7FF4` | 0.01 | signed pair `addss ±K` | — |

**32 real arms, none unimplemented.** Magnitudes among the 31 float arms: `0.02` ×9, `0.05` ×8,
`0.01` ×7, `0.03` ×3, `1.0` ×2, `0.001` ×1, `0.5` ×1.

## 4. Twelve float fields of a live engine object

Thirteen arms do not touch the console's settings blob at all. They **call an engine accessor, take
the returned pointer, and step a float field of it** — then call the accessor a *second* time to store
the result:

```asm
001D2EAA  call  <engine accessor>
001D2EAF  movss xmm6, [rax + 0x2d8]
001D2EB7  test  bl, bl
001D2EB9  je    0x1d2ed5
001D2EBB  addss xmm6, [-0.05]
001D2EC3  call  <engine accessor>        ; fetched again rather than kept
001D2EC8  movss [rax + 0x2d8], xmm6
```

The field map this slice establishes:

> **Flagged 2026-09-08, unresolved.** The paragraph above says **thirteen** arms; the table below
> maps **twelve** arm ids — 114-118 and 127-133. Its fourteen rows are fourteen consecutive dword
> offsets `+0x2D0`-`+0x304`, of which `+0x2E4` and `+0x2F8` carry **no** arm, so *"twelve float
> fields"* in the heading is the count of arm-driven fields and is consistent. **Thirteen is not**
> — either a thirteenth arm is missing from this table or the sentence overcounts. Not resolved
> here: it needs the arm bodies re-read, not a number changed to make the page agree with itself.
> Surfaced by `check_counts.py`; see `EC-5`.

| offset | id | magnitude | bound |
|---|---:|---|---|
| `+0x2D0` | 114 | 0.05 | `[0.0, 1.0]` |
| `+0x2D4` | 115 | 0.05 | `[0.0, 10.0]` |
| `+0x2D8` | 116 | 0.05 | — |
| `+0x2DC` | 117 | 0.05 | — |
| `+0x2E0` | 118 | 0.05 | — |
| `+0x2E4` | — | — | **not reached by this slice** |
| `+0x2E8` | 127 | 0.02 | — |
| `+0x2EC` | 128 | 0.02 | — |
| `+0x2F0` | 129 | 0.001 | — |
| `+0x2F4` | 130 | 0.5 | — |
| `+0x2F8` | — | — | **not reached by this slice** |
| `+0x2FC` | 131 | 1.0 | — |
| `+0x300` | 132 | 0.01 | — |
| `+0x304` | 133 | 0.02 | — |

> **`+0x2E4` and `+0x2F8` are recorded as unreached, not as unused.** Slice C settled that question
> for slice B by finding the ids that owned its gap in a later range. **The same caution applies here
> and for the same reason:** ids 140–293 are unread *(answered: see slices E to I, delivered; 2026-10-02, OPUS)*, and nothing in this slice licenses a claim about
> those two slots.

**Ids 114 and 115 are the only bounded arms here, and their ceilings differ** — `1.0` and `10.0`,
both floored at `0`. The clamp is `comiss` against the ceiling, `ja` to store the ceiling, otherwise
`xorps`/`maxss` for the floor.

The accessor is a hub — **47 caller functions image-wide** — so it is named by role and
**deliberately not made an address citation here**, per the rule for shared singletons. The field map
above does not depend on its identity.

## 5. Two corrections to the frame, both fully re-derived

### 5.1 `01F82D20` is a pointer slot and is never nudged

The frame records it as *the hottest single address, nudged by 18 different commands*. Scanning
**every one of the 227 arms** for references to it:

```
24 references, ALL of them `mov <reg>, qword ptr [01F82D20]`, in 18 distinct arms
0  references that read or write it as a 4-byte float
```

**The count of 18 is right; the operation is not.** It is an 8-byte **pointer** that 18 arms
dereference in order to reach fields of the object behind it — id 134 here loads it and steps the
dword at `+0x40`. A `data_touched` column cannot separate an 8-byte pointer load from a 4-byte float
nudge, which is how a pointer became the most-nudged address in the binary.

*Control:* the same scan does report `movss`-shaped float references elsewhere — id 112's
`01F82ED0`, ~~sixteen bytes further~~ `0x1B0` (432) bytes further *(corrected 2026-10-02, OPUS: `0x01F82ED0 − 0x01F82D20`)* into the same region, is read and written as a float by this very
slice. So the zero above is a measurement, not a silent non-match.

### 5.2 The hub figures 45 and 33 are call sites, not arms

The frame's rule for shared singletons cites *"`001A9930` is used by 45 arms, `00193D50` by 33"*.
Counted over all 282 ids and all 227 arms:

| accessor | ids | distinct arms | call sites inside arms |
|---|---:|---:|---:|
| `001A9930` | 14 | **14** | **45** |
| `00193D50` | 16 | **16** | **33** |

**The numbers 45 and 33 reproduce exactly — as call sites.** The arms call these accessors two, three
or four times each, because **each arm re-fetches the object instead of keeping the pointer**, which
is visible in the fragment in §4. The two accessors are also reached from **outside** the dispatch:
nine Presentation-layer bodies call `00193D50` (`001CD0E0`, `001C7940`, `0018B1B0`…) and eleven call
`001A9930` (`001CD0E0`, `001C3D50`, `001BF8B0`…), and `001D1660`'s own callees include the
Presentation-owned materializers `001D5120`/`001C7360`/`001C7520` — 23 edges in all. The arms and
their accessors sit on the render path, not behind it. The catalogue's other crossings are the
expected glue: `007980A0` — the `GameSettingConfig` singleton's allocator (§9's construction
note) — calls **platform**/online init (`008655E0`, `007A0C60`, `0020CD80`, `0020CD30`,
`0019A510`, `007979B0`, `0079E520`, 11 edges across platform and input), the dispatcher reaches
**audio** `002DEBA0`/`001DBB00` and **resource** `002EEEE0`, and `00193D50` is called by resource
`001A7A50` — code that resets or re-inits parts of the engine necessarily leaves the console's own
layer.

> This does not weaken the "name it, do not cite it" rule — it **tightens** it. The neighbourhood a
> citation would commit a row to is 14 arms, not 45, and a rule is easier to apply when its number
> means what it says.

## 6. Data structures and formulas

```c
/* the 25 signed-pair arms */
v = *param;
*param = v + (direction ? -K : +K);     /* two constants, exact negatives */

/* the 6 one-constant arms — the slice B/C shape */
*param = direction ? v - K : v + K;

/* ids 114 and 115 */
t = v + (direction ? -0.05f : +0.05f);
*param = (t > CEIL) ? CEIL : max(0.0f, t);   /* CEIL = 1.0f (114), 10.0f (115) */

/* id 134, a two-state cycle on an int field reached through a pointer */
n = obj->f40;
n = direction ? (n - 1 >= 0 ? n - 1 : 1)      /* down from 0 wraps to 1 */
              : (n + 1 >  1 ? 0     : n + 1); /* up   from 1 wraps to 0 */
```

## 7. Call chain

```
console dispatch  001D1660   (arg1 rcx = settings object -> rdi, arg2 dl = direction -> bl)
  -> table 001D4C1C + (id - 12)*4  -> + 0x00120000 -> the arm
     ids 108..113, 119..126, 135..139 : a float global (02CBxxxx / 01DFE194 / 01F82ED0)
     ids 114..118, 127..133           : call the engine accessor, step [rax + 0x2D0..0x304],
                                        call it again to store
     id  134                          : load the pointer at 01F82D20, cycle the dword at +0x40,
                                        then two further calls carrying the new value
  -> jmp 001D4BFA   the shared tail
```

Id 134's two follow-up calls have **15** and **2** callers image-wide respectively; neither is
characterised here, and what they do with the new value is open.

## 8. Modding notes

- **Thirteen of these commands tune an engine object, not the console.** Hooking the console's own
  settings blob will not see them; they read and write through the accessor every time.
- **Each of those arms fetches the object twice per press.** Anything that intercepts the accessor
  should expect two calls per command, not one.
- **Ids 114 and 115 are the only bounded arms in this range** — `[0, 1]` and `[0, 10]`.
- **Nothing in this range is unimplemented.** Every one of the 32 ids does something, which is not
  true of slices A, B or C.

## 9. What is not known

- [x] **UQ-15.** **What the engine object behind the accessor is**, and therefore what `+0x2D0`–`+0x304` are.
      *Narrowed 2026-09-14 (FABLE), not answered: the object is identified.* The accessor at `001D2EAA` / `001D2EC3` is `001A9930`,
      an 8-byte getter returning `[01F81168]`. That is the `0x520`-byte map-art context built by `001A98B0`
      ([game application](../Application-Root/game-application.md), size corrected the same day), whose `+0x120`–`+0x264` the
      [`.ta` texture-animation page](../../02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md) reads.
      `+0x2D0`–`+0x304` sit in the same object, above those fields. What the twelve floats tune is still open.
      ~~Twelve float fields with step magnitudes and two known bounds, **none traced to a reader.**
      This remains the most promising thread in the catalogue.~~
      **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): two independent sources name every field, and five of them have
      a reader.** The names come from the console's own labels ([console-command-names](console-command-names.md))
      and from the keys the per-map scene-config loader `001C7940` looks up before each store. Each key was taken from
      the `lea` ahead of that store's map lookup `001FF740`; the nearest-`lea` method shifts every key by one, so it was
      not used. The two sources agree field by field.

      | offset | console label (id) | scene-config key (store) | reader outside the console and menu |
      |---|---|---|---|
      | `+0x2D0` | Map Specular Intensity (114) | — | `001E2AF0` copies it into its draw locals (`001E38A3`) |
      | `+0x2D4` | Map CubeMap Intensity (115) | — | `001E2AF0` (`001E38B6`) |
      | `+0x2D8` | Map CubeMap Factor (116) | — | `001E2AF0` (`001E38C9`) |
      | `+0x2DC` | Map IBL Diffuse Factor (117) | `mMapIrrCubemapFactor` (`001CA54C`) | `001A97F0` publishes it to `02CB8088` when `+0x2E4` is set and a resource probe succeeds, else 0 (`001A97FB`–`001A982C`) |
      | `+0x2E0` | Map IBL Diffuse Limit (118) | `mMapIrrCubemapLimit` (`001CA595`) | none found |
      | `+0x2E4` | — (byte) | `EnableIBL` (`001C98B5` / `001C98CA`) | `001A97F0`'s gate |
      | `+0x2E8` | Water texture U Factor (127) | `mDebugWaterUFactor` (`001CA227`) | none found |
      | `+0x2EC` | Water texture V Factor (128) | `mDebugWaterVFactor` (`001CA270`) | none found |
      | `+0x2F0` | Water Min Z (129) | `mDebugWaterMinZ` (`001CA2B9`) | none found |
      | `+0x2F4` | Sample step size (130) | `mDebugWaterStepSize` (`001CA302`) | none found |
      | `+0x2FC` | Total Num of Pixels (131) | `mDebugWaterTotalNumPix` (`001CA34B`) | none found |
      | `+0x300` | Reflection blend (132) | `mDebugWaterRefBldFactor` (`001CA394`) | none found |
      | `+0x304` | Reflection strength (133) | `mDebugWaterRefFactor` (`001CA3DD`) | none found |

      **So the block is the map's lighting and water-reflection parameters, authored per map through the scene
      config and tunable from the console.** The census, [`mapart_readers.py`](members/mapart_readers.py),
      seeded 52 functions: every caller of the getter `001A9930` and every direct load of `01F81168`. Its control is
      the console arm writing `+0x2D0`, which is found. *None found* is scoped to those seeds: a function that
      receives the object pointer from elsewhere, or copies the water block wholesale, would not be seen.
      *Extended 2026-09-26 (FABLE, Claude Opus 5.5): the same loader names eleven more fields of the object.* A
      two-lookup pairing census, `tools/maploader_keys.py` in the FABLE scratch, reads each key's second `lea` (the one
      followed by the default-document fallback `01F813C8`) and the stores after that key's getter. The same seeds
      then give the readers.

      | offset | scene-config key (store) | reader |
      |---|---|---|
      | `+0x2C0`–`+0x2C8` | `mMapLightColorR`/`G`/`B` (`001C93F0`–`001C9401`) | `001E2AF0` uploads a float3 (`001E3AFC`) |
      | `+0x318`, `+0x31C` | `mShadowVertexBlendLowerLimit`/`UpperLimit` (`001C95C1`, `001C960A`) | `001E2AF0`, one float4 with the next pair (`001E3430`–`001E3482`) |
      | `+0x320`, `+0x324` | `mShadowAngleLowerLimit`/`UpperLimit` (`001C9653`, `001C969C`) | the same float4 |
      | `+0x328` (byte) | `mMapObjectShadowFadeEnabled` (`001C96E8`) | `001A97F0` publishes `+0x32C` to `02CB8418` when set, else 1.0 (`001A987B`–`001A98A1`) |
      | `+0x32C` | `mMapObjectShadowFadeRange` (`001C972F`) | the same |
      | `+0x3D9` (byte) | `EnableMapNormalMap` (`001CA4B3`) | `001E2AF0` (`001E337A`), under the console's use-normal-map byte |
      | `+0x43C` (int), `+0x440` | `mMapShadowDepthBias`, `mMapShadowSlopeOffset` (`001C8EA1`, `001C8EE8`) | `001E2AF0` passes both to render command `0x25` (`001E3091`) |

      What the draw body does with them is read on
      [the post-process page](../../22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md)
      (“The span `001E3347`–`001E3514`”). `02CB8418`, the block's `+0x448`, has no reader among rip-relative accesses,
      and none was found in the bodies that take the block base. The same holds for the four map shadow-fade keys at
      `+0x438`–`+0x444` (`02CB8408`–`02CB8414`).
- [x] **UQ-16.** What occupies `+0x2E4` and `+0x2F8` — **unreached by this slice, not known to be unused.**
      **Half answered 2026-09-25 (FABLE, Claude Opus 5.5): `+0x2E4` is the `EnableIBL` byte.** The scene-config loader
      stores it under that key (`001C98B5` / `001C98CA`), and `001A97F0` gates the IBL diffuse factor on it (`001A97FB`).
      `+0x2F8` has no console arm and no loader store, and no reader turned up in the UQ-15 census, so it stays open.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): `+0x2F8` is the `WaterQuality` setting, copied when the object is
      built.**
      - **Where it comes from.** The constructor `001A2130` loads the `GameSettingConfig` singleton `[01F82D20]` and
        copies its `+0x40` dword into `+0x2F8` (`001A26FB`–`001A2705`). The same body sets `+0x2F8` to 2 earlier
        (`001A2384`), so the setting overwrites that default.
      - **The byte beside it.** The constructor then sets `+0x2E5` to 1 when the value is non-zero and to 0 otherwise
        (`001A270C`–`001A2719`). Its earlier word store `mov word [+0x2E4], 0x101` (`001A234E`) is what gives
        `EnableIBL` and this byte their default of 1.
      - **Why `+0x40` is WaterQuality.** The game-settings INI page's key table puts `WaterQuality` at `+0x40`
        ([game settings](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md),
        entry 16). This page's arm 134, labelled *Water Quality*, cycles that same field.
      - *Not established:* a reader of `+0x2F8` or `+0x2E5`. The 52-seed census finds neither, and the scene loaders
        do not touch them. The copy is taken once, when the map-art context is built, so a later settings change
        reaches this object only if it is rebuilt.
- [x] ~~What the object behind the pointer at `01F82D20` is, and what its `+0x40` two-state field
      selects. **Eighteen arms across the table dereference that pointer**, so it is the widest-shared
      structure the console touches.~~
      **Answered 2026-09-14 (FABLE):** `01F82D20` is the `GameSettingConfig` singleton, allocated by `007980A0` and
      stored at `00798261`, its one writer ([the game-setting contract](../../19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md)).
      Its 31 `u32` settings sit at `+4 × index` (`CameraRevise` = index 22 = `+0x58`, which arm 271 reads the
      same way). So `+0x40` is setting 16, **`WaterQuality`**
      ([the settings page](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md) §2),
      which recovers the name OPUS's narrowing below left open.
      **NARROWED 2026-09-13 (OPUS) — the object is built from a 31-entry × 4-preset defaults table,
      and `+0x40` is entry 16 of it. The setting's NAME is still not recovered.**
      **Construction, one writer in the image.** `007980A0` allocates, and on a non-null result calls
      `001DE050(this, …)` at `00798257`, then stores the pointer at `00798261` —
      `mov [01F82D20], rax`. That single store is the only write to the slot in 34,270 bodies.
      **What the constructor does is copy a defaults block.** `001DE050` sets
      `[this+0x44C] = 1`, `[this+0x658] = 0x101` (word) and `[this+0x65A] = 1` — so **the object is at
      least `0x65C` bytes** — and then runs a 31-iteration loop (`lea ecx, [rdi+0x1E]`,
      `001DE08F`–`001DE0A3`) copying **one dword from every 16 bytes** of the `.rdata` table at
      `00900CE0` into consecutive dwords of the object: source stride 16, destination stride 4.
      **So `00900CE0` is 31 settings × 4 alternative preset columns, and the constructor takes
      column 0.**
      **The table is dimensions and counts, not text.** It holds no string pointers — which is why no
      name is recovered here — but entry 1 is `0x07800438`, and read as two `u16` that is
      **1920 × 1080**. The reading is not a coincidence of one value: the same dword is written as a
      *unit* into another structure at `00553B80` (`mov dword [rbx+0x9C], 0x7800438`, with
      `[rbx+0x98]` cleared immediately after). Other entries are small counts — `0x32` = 50 at
      entry 4, `4` at entries 23 and 24.
      **`+0x40` is entry 16** (`0x40 / 4`), and its default is **`1` in all four preset columns**.
      That is consistent with arm 134's `inc` / `cmov` pair cycling it as a two-state field: a flag
      whose shipped value is on in every preset.
      ~~**WHAT IS STILL NOT KNOWN, AND WHY THE BOX STAYS OPEN.** Entry 16 has no name anywhere in the
      table, and nothing in this pass reads the field for a purpose that would identify it.~~ **Named 2026-09-26
      (FABLE, Claude Opus 5.5): entry 16 is `WaterQuality`.** The game-settings INI page's key table
      places that key at `+0x40`, and arm 134 is labelled *Water Quality*. The map-art context copies it into its `+0x2F8`
      (UQ-16). *The rest of this paragraph is the earlier reasoning, kept as history.* **A
      defaults slot located is not a setting identified** — this narrows the question from *"what is
      this object"* to *"what is entry 16 of its defaults table"*, and only the first half is closed.
- [x] **UQ-17 ANSWERED 2026-09-15 (OPUS) — neither. They are not two arrays, and they are
      not one array: the whole span is a block of *individually addressed* `float` globals, and the
      “gap” between the two named clusters is not empty.**
      - **The separation is not real.** Whole-image census over all ~~89~~ 88 dwords *(corrected 2026-10-02, OPUS: `(0x02CB8144 − 0x02CB7FE8) / 4 + 1` = 88)* from `02CB7FE8` to
        `02CB8144`, stride 4, control `02098E10` returning 61 references so absence is meaningful:
        **85 of the 89 are referenced**, and **44 of the 48 dwords *between* the two named clusters
        are referenced too**, by 10 functions. There is no unused interval to separate them.
      - **Only four dwords in the whole span are unreferenced**, and all four sit inside the
        supposed gap: **`02CB807C`, `02CB808C`, `02CB8098`, `02CB809C`**.
      - **Four functions reach all three regions** — `001C3D50`, `001C7940`, `001CD0E0`,
        `001D1660` — which is what ties the span together as one object rather than two.
      - **It is floats, and it is not indexed.** Of 382 references, **351 are `movss`** (the rest:
        23 `mov`, 4 `cmp`, and one each of `sub`, `sete`, `movzx`, `movsxd`). Every one is an
        absolute RIP-relative access to a *named* slot — `001C3D50` alone writes 19 of them as an
        unrolled run at a uniform `0x1F`-byte instruction spacing (`001C4C6E` onward).
      - ~~**Nothing can walk it as an array, and that is the decisive part.**~~ **`006084B0` walks it from a register base** *(corrected 2026-10-02, OPUS: `006084B0+0x3CE` `lea rdx, [02CB7FD0]`, `+0x3D8` `lea rax, [rdx+0xd0]` (= `02CB80A0`), then 16-byte `movups` loads over `02CB7FD0`–`02CB815F` into the staged shader-constant buffer)*. The census finds
        **zero `lea`** anywhere in the span: ~~**no instruction takes the address of any slot**, so no~~
        ~~pointer into the block can be formed and no `base + index*4` access can exist.~~ but a base below it is formed and offset into it. A computed
        access would not appear in an absolute-reference census — but it would need a `lea` to get
        its base, and there is none.
      - *Re-checkable by anyone: one range census with a stated control. If any `lea` into
        `02CB7FE8`–`02CB8144` exists, this answer is wrong and should be reopened against OPUS.*
      **UQ-17.**

## 10. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The id → arm mapping for all 32 ids | dwords at `001D4C1C + (id−12)×4`, `+ 0x00120000`, re-derived from the image | 1 |
| Every target, magnitude, mechanism and bound | complete decode of each arm, bounded by **the next arm's start address** | 1 |
| 25 signed-pair arms, 6 one-constant arms | both constants read from `.rdata` per arm and compared | 1 |
| The `+0x2D0`–`+0x304` field map | the `movss` displacement in each of the 13 accessor arms | 1 |
| `01F82D20` is never a float | all 24 references in all 227 arms are `mov … qword ptr`; positive control on `01F82ED0` | 1 |
| 45 and 33 are call sites in 14 and 16 arms | `call` sites counted over all 282 ids and 227 arms | 1 |

**Re-derived, not copied:** 282 table entries, 227 distinct targets, 56 ids at `001D4BFA` — reproduced
from the image before any row was written. **`step` was re-derived per arm** rather than taken from
`Tools/work/repos-d2/console_arms.tsv`, whose author correctly labelled that column unverified.

**Controls.** The absence claims are *"no unimplemented ids"*, *"only 114 and 115 are bounded"* and
*"`01F82D20` is never a float"*. The same extractor positively detects `001D4BFA` targets in slices A,
B and C, `comiss`/`maxss` in 114 and 115, and float references to `01F82ED0` in this slice — so each
zero is a measurement rather than a silent non-match.

**Address review flags** (`001D4C1C` and every arm address) are dispositioned once for all slices in
[slice A](arm-catalogue-slice-A-ids-12-43.md) §8: the first is the dispatch table in `.text` after the
function, and switch arms are interior addresses of a function, not functions.

## 11. Related

- [the-282-command-parameter-console.md](the-282-command-parameter-console.md) — the frame; **§5
  corrects two figures in it**
- [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md) — the division and its rules
- [arm-catalogue-slice-A-ids-12-43.md](arm-catalogue-slice-A-ids-12-43.md) — ids 12–43
- [arm-catalogue-slice-B-ids-44-75.md](arm-catalogue-slice-B-ids-44-75.md) — ids 44–75
- [arm-catalogue-slice-C-ids-76-107.md](arm-catalogue-slice-C-ids-76-107.md) — ids 76–107; the
  unreached-slot caution reused in §4 is the one slice C discharged for slice B

## Falsification pass — 2026-09-03

**Recorded after the fact, from attacks that actually ran.** The nine slices were cross-checked by a
label table built independently of them, by a whole-table join, and by each other; this section says
what those attacks did to **this** slice. **`passes: 1` here means one pass happened, not that the
document is finished.**

**Attacks run against the whole catalogue, all nine slices included:**

| attack | result |
|---|---|
| duplicate labels — a shifted index read would repeat or garble | **0 of 283** |
| gaps in the action id range | **none** — 12 to 293 continuous, exactly 282 |
| arms outside the dispatcher | none; all 282 lie in `001D16B1`–`001D4BFA` |
| two ids claiming one arm | **56 ids share `001D4BFA`**, the do-nothing tail |
| arm address order vs id order | **29 inversions** — bounding an arm at the next *id* would be wrong 29 times; every slice used address order |
| cross-source control against the config keys | **20 arm-bearing pairs, 0 contradictions** |
| one field claimed by two ids | **1** — `02CB8130`, resolved (see slice A) |

**This slice was the subject of a correction that was itself wrong, and the retraction is the record.**
A census reported that D "needed" the third direction mechanism. **D had it first, and had it as its
headline** — §2 reads `signed pair, addss (−K) down / addss (+K) up : 25`, with 25 catalogue rows
carrying it.

> **The census rediscovered a slice's headline finding and it was relayed back to its author as a
> correction.** Merging it as written would have republished a confirmation as a discovery.

**Corroborated:** id 134 "Water Quality" is **property 16** under slice I's `offset/4` rule — read from
this slice's arm **before that rule existed**.

`001A6FF0` (1045 B) is the arm worker `001BF8B0` runs: `01F81168` supplies the console state, `001EDF00` x4 name lookups with `0017D2E0` x3, `001A9940`, `001A5630`, `00861ED2` x2, `00210EB0`, `001A4BF0` and `00861EC0` build the arm's record - the slice-D catalogue's emit body.

Interior anchor `001A7048` (function `001A6FF0`).

`001A53F0` (272 B) is the per-entry lane sync `001BF8B0` runs over `dword[rdi+0x20]` records: `00189120` yields the row and `byte[rax+0x1C]` picks the `0`/`8` lane inside `[rdi+0x88]`'s pointer pairs; a live `[lane + 0x260]` resolves `001A2F70(rdi+0x448)`, the lane's `+8` takes `[result+0x18]`, and `001E5C40(lane, [result+0x18]+0x20, floats +0x20..+0x38)` republishes the transform block - the arm's record-to-slot refresh.

Interior anchor `001A54CF` (function `001A53F0`).

`001A9CD0` (147 B) is the `+0x448` keyed-record insert `001BF8B0` runs for the arm's records: `001A76D0` resolves `rdi`/`xmm3` into a key, `001A2F70(rbx+0x448)` finds-or-makes the slot (the same `+0x448` map `001A53F0` reads for lane sync), and the returned record takes `+0x18 = rdi`, floats `+0x20`/`+0x24`/`+0x28`/`+0x2C`/`+0x30`/`+0x34` from the stack-passed span and `+0x38` the trailing dword - the per-arm transform-record store the lane refresh republishes from.

Interior anchor `001A9D01` (function `001A9CD0`).

`001A76D0` (114 B) is the key resolver `001A9CD0` calls before the `+0x448` insert: `0016D6A0` with a `(rdx != 0)` flag, a leading `.` on the key is skipped (`rbx + 1`), `0019CE20` hashes it, `0019CA80` resolves the bucket, and on a hit the tail jumps `001A7630` to apply the record; on a miss it returns - the name-to-slot path the arm catalogue's keyed records go through.

Interior anchor `001A7713` (function `001A76D0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **Save_Load_Settings — CLIENT and SERVICE (3 edges).** 1 inbound (Save_Load_Settings bodies `GameSettingConfig_ParseText` (001DE5D0) call page-cited `001A5630`); 2 outbound (page-cited `007980A0` call Save_Load_Settings bodies `GameSettingConfig_LoadOrCreateFile` (001DED50), `GameSettingConfig_InitDefaultsAndPath` (001DE050)). Substantive edges include `001A5630` is called by `GameSettingConfig_ParseText` (001DE5D0); `007980A0` calls `GameSettingConfig_LoadOrCreateFile` (001DED50); `007980A0` calls `GameSettingConfig_InitDefaultsAndPath` (001DE050).
- **WorldAreaField — CLIENT and SERVICE (3 edges).** 1 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020) call page-cited `002DEBA0`); 2 outbound (page-cited `001CD0E0` call WorldAreaField bodies `WorldTransition_GetTransitionFieldId` (00314910), `FieldData_GetVariable0` (00265270)). Substantive edges include `001CD0E0` calls `WorldTransition_GetTransitionFieldId` (00314910); `001CD0E0` calls `FieldData_GetVariable0` (00265270); `002DEBA0` is called by `World_UpdateSimulationTick` (00314020).

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-arm-catalogue-slice-d-ids-108-139-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001C0960` | 299 B | returns at once when `001A9930()` is null; otherwise walks the list headed at `rcx+0x28` (first node qword `+0x30`, next through `0016D6D0`) for the first node whose object (qword `+0x40`) has a non-null qword `+0x100` and whose string (qword `+0x20`) equals the name at `001A9930()` + 0x241; for it, it decrements dword `+0x48`, unlinks the node with `0016DA60(node, rcx+0x28)`, frees the node's string through slot `+0x18` of the allocator at node `+0x38` when it is longer than one byte, frees the 0x48-byte node through slot `+0x18` of the allocator at `rcx+0x50`, calls `001BF8B0(rcx, qword object+0x100, qword object+0x108)` and `00210EB0(qword object+0x100)` when that is non-null, and deletes the 0x118-byte object with `00809950` | `001C097C`, `001C09C3`, `001C09F4`, `001C0A44`, `001C0A58` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-arm-catalogue-slice-d-ids-108-139-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `001A7990` | 113 B | `001BF8B0` + 0x199 | returns 0 when the call at `001A7990` + 0x9 (with `rcx`) returns 0; otherwise, with k that result, walks nodes from qword `rcx+0x460`, remembering a node and following its qword `+8` when its qword `+0x20` is not below k (unsigned) and following its qword `+0` otherwise, until a null link; returns 1 when a node was remembered and k is not below that node's qword `+0x20`, and 0 otherwise (the remembered slot starts as `rcx+0x450`) | Interior anchor `001A79A4`; Interior anchor `001A79D0`; Interior anchor `001A79D9`; Interior anchor `001A79EC`; Interior anchor `001A79F8` |
