---
system: Arm catalogue — slice C, command ids 76–107
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
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 1 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
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

# Arm catalogue — slice C, command ids 76–107

> Slice C of the division in [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md).
> **32 command ids. It says nothing about the other 250.**

## 1. What the player sees

Nothing — a developer tool. Slice C is the **densest tuning range found so far**: 27 of its 32
commands adjust a floating-point value, and 23 of those address **consecutive slots of one array**.
Together with slice B it completes an **unbroken run of 36 floats, one per command id**, which is the
shape of a panel of sliders a developer scrolled through while the game ran.

## 2. Does the arm shape hold here? Mostly — and the exceptions are the findings

This was the first question asked of the slice, because **slice A was counters and slice B was
floats**. The answer for C:

- **The dominant shape holds.** 26 arms are `movss` / `test bl,bl` / `subss`-or-`addss` on **one
  constant** / `movss` back — the same both-directions-one-magnitude shape established across the
  console.
- **One arm is multiplicative and no additive model describes it.** Id 106 steps by **ratio**, not by
  addition, and it is the only arm in this slice whose two directions use **different constants**.
- **Two arms are clamped** where the other 24 float arms are unbounded.
- **One arm is not a tuning command at all** — id 103 re-seeds three of its neighbours' fields from
  live engine state.

## 3. The catalogue

Row shape per the work order: **field · width · step magnitude · direction mechanism · bound.**
`b` = byte, `d` = dword, `f32` = 4-byte float. `rdi` offsets are fields of the settings object;
`02CBxxxx` and `01DFxxxx` are globals. **No target in this slice is identified by name** *(answered: see UQ-11, ANSWERED 2026-09-25: all 36 named; 2026-10-02, OPUS)* — see §8.

| id | arm | kind | target | width | magnitude | direction mechanism | bound |
|---:|---|---|---|---|---|---|---|
| 76 | `001D2423` | float step | `02CB80F8` | f32 | 0.001 | `addss`/`subss`, one constant | — |
| 77 | `001D2459` | float step | `02CB80FC` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| 78 | `001D248F` | float step | `02CB8100` | f32 | 0.001 | `addss`/`subss`, one constant | — |
| 79 | `001D24C5` | float step | `02CB8104` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| 80 | `001D24FB` | float step | `02CB8108` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| 81 | `001D2531` | float step | `02CB810C` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| 82 | `001D2567` | float step | `02CB8110` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| 83 | `001D259D` | float step | `02CB8114` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| 84 | `001D25D3` | float step | `02CB8118` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| 85 | `001D2609` | float step | `02CB811C` | f32 | 0.001 | `addss`/`subss`, one constant | — |
| 86 | `001D263F` | float step | `02CB8120` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| 87 | `001D2675` | float step | `02CB8124` | f32 | 0.001 | `addss`/`subss`, one constant | — |
| 88 | `001D26AB` | float step | `02CB8128` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| 89 | `001D26E1` | float step | `02CB812C` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| 90 | `001D2717` | float step | `02CB80D4` | f32 | 0.1 | `addss`/`subss`, one constant | — |
| 91 | `001D274D` | float step | `02CB80D8` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| **92** | `001D2783` | float step | `02CB80DC` | f32 | 0.01 | `addss`/`subss` **+ clamp** | **`[0.0, 1.0]`** |
| **93** | `001D27CC` | float step | `02CB80E0` | f32 | 0.01 | `addss`/`subss` **+ clamp** | **`[0.0, 1.0]`** |
| 94 | `001D2815` | float step | `02CB80E4` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| 95 | `001D2065` | float step | `02CB80A0` | f32 | 0.02 | `addss`/`subss`, one constant | — |
| 96 | `001D209B` | float step | `02CB80A4` | f32 | 0.02 | `addss`/`subss`, one constant | — |
| 97 | `001D20D1` | float step | `02CB80A8` | f32 | 0.1 | `addss`/`subss`, one constant | — |
| 98 | `001D2107` | float step | `02CB80AC` | f32 | 0.05 | `addss`/`subss`, one constant | — |
| 99 | `001D2052` | boolean toggle | `01DFE191` | b | — | `cmp`/`sete` | 0/1 |
| **100** | `001D4BFA` | **unimplemented** | — | — | — | — | — |
| **101** | `001D4BFA` | **unimplemented** | — | — | — | — | — |
| **102** | `001D4BFA` | **unimplemented** | — | — | — | — | — |
| **103** | `001D2AFD` | **toggle + re-seed** | `b+0xC0C`; writes `d+0xC10`, `d+0xC14`, `d+0xC18` | b | — | `cmp`/`sete`, then three copies on the **off** edge | 0/1 |
| 104 | `001D2B4D` | float step | `rdi+0xC10` | f32 | **0.00555556** | `addss`/`subss`, one constant | — |
| 105 | `001D2B83` | float step | `rdi+0xC14` | f32 | 0.01 | `addss`/`subss`, one constant | — |
| **106** | `001D2BB9` | **float scale** | `rdi+0xC18` | f32 | **×0.99 / ×1.01** | `mulss` pair, **two different constants** | — |
| 107 | `001D1FB0` | float step | `02CB8140` | f32 | 0.05 | `addss`/`subss`, one constant | — |

**29 real arms and 3 unimplemented** (100, 101, 102). Magnitudes among the 26 additive float arms:
`0.01` ×15, `0.001` ×4, `0.1` ×2, `0.02` ×2, `0.05` ×2, `0.00555556` ×1.

## 4. Ids 63–98 are one unbroken array of 36 floats — and slice C fills slice B's gap

Slice B recorded a gap in its own id run and stated explicitly that the gap was a layout fact and
**not** evidence the skipped slots were unused, because no id in that slice reached them and C–I were
unread. **Slice C reaches them.** Ids 90–94 own exactly the skipped slots:

```
02CB80A0 A4 A8 AC          ids 95..98
02CB80B0 ...        D0     ids 63..71   (slice B)
02CB80D4 D8 DC E0 E4       ids 90..94   <- the slots slice B could not reach
02CB80E8 EC F0 F4          ids 72..75   (slice B)
02CB80F8 FC                ids 76..77
02CB8100 ... 812C          ids 78..89
```

Re-derived from the dispatch table for all 36 ids: **36 ids, 36 distinct targets, 36 slots from
`02CB80A0` to `02CB812C`, and no gap larger than 4 bytes.** The mapping is one-to-one.

> **The array was never sparse — the id order simply does not follow the address order.** Ids 90–98
> sit outside the 63–89 range and fill both the interior gap and four slots below the start.
> **Slice B's caution was the right call and is now discharged.**

**Correction to slice B, from this slice:** slice B called the gap "six slots" and its open question
named `02CB80D4`–`02CB80E4` as six. `(0x02CB80E8 − 0x02CB80D0) / 4 − 1 = 5`. **It is five slots**,
which is exactly what ids 90–94 fill. Slice B has been corrected.

## 5. Id 103 is not a tuning command — it re-seeds ids 104, 105 and 106

```asm
001D2AFD  cmp   byte ptr [rdi + 0xc0c], 0
001D2B04  sete  al                         ; al = (flag was 0)
001D2B07  mov   byte ptr [rdi + 0xc0c], al ; flip it
001D2B0D  test  al, al
001D2B0F  jne   0x1d4bfa                   ; turning ON -> done
001D2B15  call  <engine accessor>          ; turning OFF -> re-seed:
001D2B1A  mov   ecx, [rax + 0xcc4]
001D2B20  mov   [rdi + 0xc10], ecx
          ... [rax+0xcc8] -> [rdi+0xc14],  [rax+0xccc] -> [rdi+0xc18]
```

**The three destinations are exactly the three fields ids 104, 105 and 106 tune.** So ids 103–106 are
one group: a flag plus three parameters, where **clearing the flag reloads all three from live engine
state and setting it does not.** That is the shape of an *override*: while the flag is set the three
tuned values stand; clearing it snaps them back to whatever the engine currently holds.

The accessor is a **117-caller hub**, so it is named by role and **deliberately not made an address
citation here** — citing it would commit these rows to its whole neighbourhood, which this document
has not accounted for. The relationship above does not depend on its identity: the copies land in
fields this slice already owns.

## 6. Id 106 steps by ratio, and its two directions do not cancel

```asm
001D2BC5  mulss xmm0, [008F3110]   ; 0.99   one direction
001D2BDA  mulss xmm0, [009002D0]   ; 1.01   the other
```

Every other stepping arm in this slice applies **one** constant in both directions. Id 106 applies
**two, and they are not reciprocals**: `0.99 × 1.01 = 0.9999`, where `1 / 0.99 = 1.0101…`.

> **Stepping id 106 up and back down does not restore the value** — each round trip multiplies it by
> `0.9999`, a 0.01 % loss. Whether that was intended is not recoverable from the code; that it happens
> is.

**A multiplicative arm is invisible to an `addss`/`subss` classifier**, which is why a per-arm
magnitude census records it as an outlier rather than as a step.

## 7. Data structures and formulas

```c
/* the 26 additive float arms, exactly */
v = *param;
*param = direction ? v - K : v + K;        /* ONE constant K, both directions */

/* ids 92 and 93 additionally clamp, and only on the branch that can exceed the bound */
down: *param = max(0.0f, v - 0.01f);       /* xorps xmm0,xmm0 ; maxss */
up:   *param = min(1.0f, v + 0.01f);       /* minss against the 1.0f constant */

/* id 106 */
*param = direction ? v * 0.99f : v * 1.01f;
```

**The clamp is one-sided per branch** — decrementing checks only the floor and incrementing only the
ceiling, which is correct and is why the bound reads as `[0.0, 1.0]` rather than as two guards.

**Id 104's constant is the literal `0.00555556`, not a computed `1/180`.** The stored float is
`float32(0.00555556)`; `float32(1.0/180.0)` is a different value. Someone typed a six-figure decimal.
`0.00555556` *is* `1/180` rounded to six figures, which is suggestive of a per-degree quantity —
**stated as an observation, not a finding: nothing traces this field to an angle.**

## 8. Call chain

```
console dispatch  001D1660   (arg1 rcx = settings object -> rdi, arg2 dl = direction -> bl)
  -> table 001D4C1C + (id - 12)*4  -> + 0x00120000 -> the arm
     -> ids 76..98, 107 : read/modify/write a float global in 02CBxxxx
     -> ids 104..106    : read/modify/write a float field of the object at rdi
     -> id 103          : toggle a flag; on the OFF edge only, call an engine accessor
                          three times and copy [rax+0xCC4/0xCC8/0xCCC] into +0xC10/+0xC14/+0xC18
     -> jmp 001D4BFA    : shared tail (and the target of ids 100, 101, 102)
```

## 9. Modding notes

- **`02CB80A0`–`02CB812C` is a 36-slot float array with a command per slot.** One hook there sees
  every value this range of the console tunes. It is in the zero-filled tail of `.data`, so it holds
  no value in the file and is built at run time.
- **Ids 92 and 93 are normalised.** A `[0.0, 1.0]` clamp with a `0.01` step is a hundred-position
  slider, and the bound is the part of the row that survives not knowing what the field is.
- **Id 103 is destructive to ids 104–106.** Anything driving this console by id should know that
  toggling 103 off discards whatever 104, 105 and 106 were set to.
- **Ids 100, 101 and 102 do nothing** — shipped behaviour, not a fault.

## 10. What is not known

- [x] **UQ-11.** ~~**What any of the 36 array slots is.**~~ **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): character
      Fresnel-specular and hair / eye lighting tuning values. All 36 are named, ~~and in this build nothing~~
      ~~outside the console reads any of them~~ and `006084B0` copies all of them into the staged shader-constant buffer.** *(corrected 2026-10-02, OPUS: `006084B0+0x3CE` `lea rdx, [02CB7FD0]`, `+0x3D8` `lea rax, [rdx+0xd0]` (= `02CB80A0`), then 16-byte `movups` loads over `02CB7FD0`–`02CB815F` into the staged shader-constant buffer; the 282-command page's ANSWERED 2026-09-27)*
      - **Named:** every id 63–98 by its console label ([console command names](console-command-names.md)). Nine
        are also named by the scene-config key the loaders store under (the 2026-09-17 narrowing below).
      - ~~**Read by nothing but the console.**~~ **Read by the console and by the staged shader-constant copy.** *(corrected 2026-10-02, FABLE, Claude Opus 5.5: `006084B0` takes the base `02CB7FD0`, below every range these checks covered, and copies the whole block with 16-byte loads into the staged shader constants; the 282-command page's ANSWERED 2026-09-27 maps each slot to a SceneWideParameterConstantBuffer variable)* Over the whole array `02CB80A0`–`02CB812C`, the only rip-relative accesses are:
        - the menu renderer (`DebugMenu_Render`), which prints the values;
        - the console arm `001D1660`, which steps them;
        - **writes** by the scene-config loaders `001C3D50` / `001C7940` to the nine keyed slots.
      - **The routes a rip census would miss are closed.** No `lea` of any address in `02CB8000`–`02CB8140`,
        no stored 8-byte or 4-byte-RVA pointer into it anywhere in the file, and every access in the 32 bytes
        below it is 4 bytes wide~~, so no wide load reaches in~~ - but a register-based wide load does: the copy's 16-byte `movups` loads from `02CB7FD0` cover the whole array.
      - ~~**So even the nine that the scene JSON sets per scene are never read by a renderer.**~~ The bank is
        written and displayed, ~~and nothing consumes it~~ and `006084B0` reads it whole *(corrected 2026-10-02, OPUS: `006084B0+0x3CE` `lea rdx, [02CB7FD0]`, `+0x3D8` `lea rax, [rdx+0xd0]` (= `02CB80A0`), then 16-byte `movups` loads over `02CB7FD0`–`02CB815F` into the staged shader-constant buffer; a register-based walk the rip census does not see)*. UQ-8 is the same finding for the thirteen hair and
        eye slots.
      *Original box follows:* **What any of the 36 array slots is.** Known: their step magnitudes, their bounds where they
      have them, and their one-to-one id mapping. **None was traced to a reader.**
      ***NARROWED 2026-09-17 (FABLE): nine of the 36 are named by the scene-config loaders, and their keys match the arms' labels one for one; the other 27 have neither a key nor a reader outside the console.** The loaders `001C7940` and `001C3D50` store into nine of these slots under string keys (the key whose `lea` precedes the lookup that precedes each store; [the console page's consumers table](members/console-tunables-consumers.tsv)): `02CB80A0` `chrFresnelSpecularIntensity` (id 95), `02CB80A4` `chrFresnelSpecularPower` (96), `02CB80A8` `chrFresnelSpecularClampValue` (97), `02CB80AC` `chrFresnelSpecularSkinIntensity` (98), `02CB80D4` `mEyeABCubeMapBlendFactor` (90), `02CB80D8` `mEyeABSpecularBlendModifier` (91), `02CB80E4` `mEyeABSpecularShadowModifier` (94), `02CB8104` `mEyeASpecularIntensityAfterClampModifier` (79) and `02CB8128` `mEyeBSpecularIntensityAfterClampModifier` (88): the character Fresnel-specular and eye-specular parameters, which the scene JSON overrides per scene and the console nudges. The remaining 27 slots are written by the console and shown by its renderer and reach no rip-relative reader, so their meaning rests on their labels alone. Static.*
- [x] ~~What the settings object at `rdi` is — unidentified, so `+0xC0C`–`+0xC18` are offsets, not names.~~
      **Answered 2026-09-14 (FABLE):** `001D50D0` returns it: a `0x10E8`-byte singleton built on first use by `001CCB20` and cached at `01F81428` (`001D50DD`–`001D5106`). The same object carries the console's labels at `+0x130 + 8 × id`, which `001CCB20` clears (`001CCE6F`) before `001D0390` fills them (`001CCEA4`). `001D1660` receives it through `001CD040`'s pass-through `rcx` (the steal page's `FK-3`, [the steal roll](../../08-Combat-Formula/Steal/the-steal-roll.md)).
- [x] ~~**UQ-12.** What the engine object behind id 103's accessor is, and what its `+0xCC4`/`+0xCC8`/`+0xCCC`~~
      *Narrowed 2026-09-14 (FABLE), not answered: the accessor is identified.* `001D2B15` calls `00189120`, an 8-byte getter returning
      `[01F7F598]`. That is the unnamed `0xDD8`-byte singleton the per-frame tick pumps three times
      ([game application](../Application-Root/game-application.md)), and `+0xCC4`–`+0xCCC` lie inside it. The fields' meaning is still open.
      fields are. **These are the closest thing in this slice to a name for a tuned value**, and they
      are the most promising thread out of it.
      ***ANSWERED 2026-09-17 (FABLE): the object is the render subsystem's `0xDD8`-byte object, and the three fields are the camera override's FOV, aspect ratio and scale.** `[01F7F598]` is written once, by `00189000`, which allocates `0xDD8` bytes through `00210EC0` and constructs them with `00184F20` (`00189034`..`00189067`); [the game-application page](../Application-Root/game-application.md) lists it as the object pumped three times per tick and its setup `00184F20` as SceneCamera-tagged. The fields are read in one other place, the render pass list `00187950`: when the object's byte `+0xC0C` is set it copies `+0xCC4`, `+0xCC8` and `+0xCCC` into the camera object's `+0xD0`, `+0xC8` and `+0xD4`, calling the camera's vtable slot 1 after each store (`0018821B`..`00188263`). Beside them, ids 104, 105 and 106 (*FOV*, *Aspect Ratio*, *Camera scale*) edit the console's own `+0xC10`, `+0xC14` and `+0xC18`, and id 103 (*Camera Over Write*) toggles the flag and on its OFF edge reseeds those three from `+0xCC4`..`+0xCCC` (this page's own reading). So `+0xC0C` is the camera-override switch and `+0xCC4`, `+0xCC8`, `+0xCCC` are the override's field of view, aspect ratio and camera scale, in the order the neighbouring arms use them. Static; the writer, the pass list and the arm read.*
- [x] ~~**UQ-13.** Whether id 106's non-reciprocal pair is deliberate.~~ **NO ADMISSIBLE SOURCE** (2026-09-14, FABLE;
      EVIDENCE-STANDARD addendum 2026-09-15bk): the pair is read from the image; whether it was meant is intent.
- [x] **UQ-14.** What id 99's byte global `01DFE191` enables. **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): the
      Fresnel reflection render path, as its console label says.** This corrects a register answer of mine
      (2026-09-16) that it "gates the DEBUG MENU". At `001CE623` the menu renderer (`DebugMenu_Render`) compares the byte
      and prints `"%s%s Yes"` (`008FFD28`) or `"%s%s No"` (`008FFD38`) through the shared row tail at
      `001CDD9C`. That displays the row's value; it is not a gate on the menu. The byte's roles:
      - the console **toggles** it (id 99, `001D2052`);
      - map-art processing **sets** it to "a list is non-empty" (`001A5B30`, `001A698E`–`001A699B`);
      - the renderer `001F8D10` **selects a draw path** by it at `001F98CF`. With the flag set and
        `[rbp+0x1A0]` zero, that path passes `1.0f` and requires a count of at least 4.

      Its authored default is 1. What that draw path puts on screen is not read here.
      The narrowing below stands as history.
      *Narrowed 2026-09-14 (FABLE), not answered:* the label is *"Fresnel Reflection enable:"* ([names](console-command-names.md)), and the byte is
      `1` in the image. Outside the console and the menu renderer (`001CE623`) it has one writer and one reader:
      - `001A5B30` sets it to "a list is non-empty" (`sub` / `sar 3` / `setne`, `001A698E`–`001A699B`) while it processes map
        art;
      - `001F8D10` tests it at `001F98CF` before a branch that, when `[rbp+0x1A0]` is 0, reads words `+0x10` / `+0x12` of a
        record.

      What that branch draws was not read.

## 11. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The id → arm mapping for all 32 ids | dwords at `001D4C1C + (id−12)×4`, `+ 0x00120000`, re-derived from the image | 1 |
| Every target, magnitude, mechanism and bound | complete decode of each arm, bounded by **the next arm's start address** | 1 |
| The 36-slot unbroken array | targets re-derived for all of ids 63–98 from the table; max gap 4 bytes | 1 |
| Id 103 writes the fields ids 104–106 tune | both read from the same three `rdi` offsets in the same function | 1 |
| Id 106's constants and their non-reciprocity | the two `.rdata` floats read from the image and multiplied | 1 |
| Id 104's constant is a typed decimal | `float32(0.00555556)` reproduces the stored bits; `float32(1/180)` does not | 1 |
| 3 unimplemented ids | those entries resolve to `001D4BFA` | 1 |

**Independently reproduced from the image before any row was written:** 282 table entries, 227
distinct targets, 56 ids at `001D4BFA`. These agree with the frame document and were re-derived rather
than copied from it.

**Controls.** The absence claims here are *"only ids 92 and 93 are bounded"* and *"only id 106 is
multiplicative"*. The same extractor that reports those zeros positively detects `maxss`/`minss` in
92 and 93, `cmp`/`sete` in 99 and 103, and `mulss` in 106 — so each zero is a measurement and not a
silent non-match. **`step` was re-derived per arm and not taken from
`Tools/work/repos-d2/console_arms.tsv`**, whose author correctly labelled that column unverified;
this slice's magnitudes are read from the `.rdata` operand of each branch.

**Address review flags** (`001D4C1C` and every arm address) are dispositioned once for all slices in
[slice A](arm-catalogue-slice-A-ids-12-43.md) §8 — the first is the dispatch table in `.text` after
the function, and switch arms are interior addresses of a function, not functions.

## 12. Related

- [the-282-command-parameter-console.md](the-282-command-parameter-console.md) — the frame
- [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md) — the division and its rules
- [arm-catalogue-slice-A-ids-12-43.md](arm-catalogue-slice-A-ids-12-43.md) — ids 12–43, counters and toggles
- [arm-catalogue-slice-B-ids-44-75.md](arm-catalogue-slice-B-ids-44-75.md) — ids 44–75; **this slice
  fills the gap that document could only record as unread**

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

**Corroborated from an independent source.** Id 103, this slice's re-seeding arm, is labelled
**`Camera Over Write (O to capture)`**, and ids 104/105/106 are **FOV / Aspect Ratio / Camera scale** —
so **the ratio-stepping arm is the one called "scale"**, which is exactly what a multiplicative step
is for.

> **The label explains a mechanism the disassembly had already produced** — two sources, neither
> derived from the other, agreeing about *why*.

The clamped pairs in this slice were also one of the four independent proofs of the label table's
index alignment.


*(Pass 22 adjacency, 2026-09-14: this slice's crossings are the shared dispatcher's, repeated
here because every slice cites `001D1660` — it calls the **presentation** materializers
`001D5120`/`001C7360`/`001C7520`, reaches **audio** `002DEBA0`/`001DBB00`, and fetches
through **resource** `002EEEE0`. The console lives on the render path and pulls its row content
through resource/audio helpers; the edges belong to the dispatcher, not to this slice's arms.)*

*(Pass 22 live-graph completion, 2026-09-15: `001D50D0` is called by `Input` bodies
`00197800`/`00197160`/`00197790` (3), and `001CCB20` calls `Platform` `005CC930` (1) — the
same shared-accessor and arm shape as the sibling slices.)*

## SWE2-EC7-109 update (2026-09-20) - `001EAD20` measured

`001EAD20` (24 B) is the
two-float setter `001C2980` and
`001D0390` call:
`float[rcx + 0xF0] = xmm1`,
`float[rcx + 0xF4] = xmm2`,
`byte[rcx + 0xE9] = 1` - the
float twin of `001EAA90`'s
dword pair, same dirty latch.
Interior anchor `001EAD28` (the
`+0xF4` store).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **Application — CLIENT (1 edge).** 1 inbound (Application bodies `00799980` call page-cited `005CC930`). Substantive edges include `005CC930` is called by `00799980`.
- **Input — CLIENT and SERVICE (13 edges).** 8 inbound (Input bodies `InputManager_PollAndBuildControlState` (00196FF0), `001E0DA0`, `001E0E70` call page-cited `001D50D0`, `005CC930`, `InputManager_TranslateBindingProfileToControlState` (00197160)); 5 outbound (page-cited `InputManager_TranslateBindingProfileToControlState` (00197160) call Input bodies `InputBackend_IsControlCode28To283ActiveForBank` (0079E6A0), `InputBackend_IsControlCode11To27ActiveAnyDevice` (0079E650), `InputBackend_IsPrimaryControlCode1To3Active` (0079E6D0)). Substantive edges include `InputManager_TranslateBindingProfileToControlState` (00197160) is called by `InputManager_PollAndBuildControlState` (00196FF0); `InputManager_TranslateBindingProfileToControlState` (00197160) calls `InputBackend_IsControlCode28To283ActiveForBank` (0079E6A0); `InputManager_TranslateBindingProfileToControlState` (00197160) calls `InputBackend_IsControlCode11To27ActiveAnyDevice` (0079E650); `InputManager_TranslateBindingProfileToControlState` (00197160) calls `InputBackend_IsPrimaryControlCode1To3Active` (0079E6D0).
- **Platform — SERVICE (1 edge).** 1 outbound (page-cited `001CCB20` call Platform bodies `005CC930`). Substantive edges include `001CCB20` calls `005CC930`.
- **WorldAreaField — CLIENT (1 edge).** 1 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020) call page-cited `002DEBA0`). Substantive edges include `002DEBA0` is called by `World_UpdateSimulationTick` (00314020).

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-arm-catalogue-slice-c-ids-76-107-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `001C2D10` | 61 B | `001C2980` + 0x111 | when `rdx` and `r8` are both non-null, replaces float `[rdx]` with float `rcx+0x4664` times it minus 1.65 (`008F9DD0`) and float `[r8]` with float `rcx+0x4668` times it minus 2.0 (`01CEBC08`); otherwise returns without writing | Interior anchor `001C2D18`; Interior anchor `001C2D26`; Interior anchor `001C2D2E`; Interior anchor `001C2D3F`; Interior anchor `001C2D47` |
| `001C2D50` | 83 B | `001C2980` + 0x23C | when qword `rcx+8` is below qword `rcx+0x10` (unsigned), advances `+8` by 0x230 and, when the old value is non-null, calls `001C2D50` + 0x34 with it in `rcx` and the incoming `rdx`; otherwise tail-jumps (`001C2D50` + 0x49) with `rcx`, qword `+8` in `rdx` and the incoming `rdx` in `r8` | Interior anchor `001C2D64`; Interior anchor `001C2D76`; Interior anchor `001C2D84`; Interior anchor `001C2D99` |
| `001EE5D0` | 123 B | `00187950` + 0x6B | with ints `r8d`, `r9d` and the fifth and sixth (stack) arguments c and d: when `r8d` equals c and `r9d` equals d, stores 0 into dwords `[rdx]` and `[rcx]`; otherwise, when float c divided by float d exceeds float `r8d` divided by float `r9d`, stores the absolute value of (`r8d` minus c) divided by 2 (signed, truncated) into `[rcx]` and 0 into `[rdx]`, else stores 0 into `[rcx]` and the absolute value of (`r9d` minus d) divided by 2 into `[rdx]` | Interior anchor `001EE5DB`; Interior anchor `001EE60B`; Interior anchor `001EE613`; Interior anchor `001EE629`; Interior anchor `001EE647` |
