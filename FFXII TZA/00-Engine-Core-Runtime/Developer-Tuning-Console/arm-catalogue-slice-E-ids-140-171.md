---
system: Arm catalogue — slice E, command ids 140–171
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: CodeDomain — Presentation.Rendering
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

# Arm catalogue — slice E, command ids 140–171

> Slice E of the division in [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md).
> **This document describes 32 command ids.** Where it reports a number over the whole table it says
> so explicitly and gives the population; nothing here is generalised from 32 arms to 282.

## 1. What the player sees

Nothing. This is a developer tool, and slice E is the part of it that tunes **how eyes, skin and hair
catch the light**: specular power and intensity for character eyes and hair, a Fresnel term for
background NPCs, a camera-relative light offset, and subsurface scattering. A developer walked to a
row, held left or right, and watched a face change while the game ran.

## 2. Does the arm shape hold here? No — in three separate ways

The work order asks this first for every slice. Slice A was counters through `rdi`; slices B and C
were floats on globals stepped by one constant. **Slice E is floats, but the arm shape differs in the
direction mechanism, the target's nature, and the presence of a non-tuning arm.**

**First — 21 of the 27 float arms do not use `subss` at all.** Both branches use `addss`, and the
direction is chosen by *which constant is loaded*:

```asm
001D33A2  movss xmm0, [02CB7FF8]        ; the parameter
001D33AA  test  bl, bl                  ; the direction flag
001D33AC  je    0x1d33c3
001D33AE  addss xmm0, [009002F4]        ; -0.01  <- DOWN, a stored NEGATIVE
001D33B6  movss [02CB7FF8], xmm0
001D33BE  jmp   0x1d4bfa
001D33C3  addss xmm0, [008F30E4]        ; +0.01  <- UP
001D33CB  movss [02CB7FF8], xmm0
```

> **A classifier keyed on `subss` finds no decrement in these arms, and a mnemonic-signed one records
> `+0.01` twice.** This is the same class of artifact the parent document was written to correct,
> reappearing in a form that survives the first correction. The magnitude is identical either way;
> **the mechanism is not, and the row shape records the mechanism for exactly this reason.**

Both constants are read from the image: `008F30E4` = `+0.01`, `009002F4` = `-0.01`.

**Second — the targets are not loose globals.** Every `02CBxxxx` address in this slice is a field of
**one statically-constructed C++ object based at `02CB7FD0`** (§6). Slice A could not identify its
settings object; this one is identified, and its constructor supplies a **shipped default for every
row in the table below**.

**Third — one arm in the slice does not tune anything.** Id 166 pushes a mode into a subsystem
through a virtual call (§7), and id 165 is a labelled command whose arm was emptied.

## 3. The catalogue

Row shape per the work order: **field · width · step magnitude · direction mechanism · bound**, with
two columns the work order did not have because slice E could fill them: the **parameter name** (§4)
and the **shipped default** (§6). `b` = byte, `f32` = 4-byte float. The `(+0xNNN)` column is the
field's offset in the object at `02CB7FD0`.

| id | arm | parameter | field | w | default | magnitude | direction mechanism | bound |
|---:|---|---|---|---|---|---|---|---|
| 140 | `001D33A2` | Map Eye Specular Intensity After Clamp Modifier | `02CB7FF8` (+0x028) | f32 | **1.1** | 0.01 | **`addss`/`addss`, two constants** | — |
| 141 | `001D33D8` | Map Eye Specular Intensity After Clamp Eye Camera Distance Factor | `02CB7FFC` (+0x02C) | f32 | **0.05** | 0.01 | **`addss`/`addss`, two constants** | — |
| 142 | `001D340E` | Map Eye CubeMap Intensity Modifier | `02CB8000` (+0x030) | f32 | **0.5** | 0.01 | **`addss`/`addss`, two constants** | — |
| 143 | `001D3444` | Map Eye Specular Blend Modifier | `02CB8004` (+0x034) | f32 | **1.3** | 0.01 | **`addss`/`addss`, two constants** | — |
| 144 | `001D347A` | Map Eye Diffuse Modifier | `02CB8014` (+0x044) | f32 | **1.3** | 0.01 | **`addss`/`addss`, two constants** | — |
| **145** | `001D34B0` | Map Eye Ambient Modifier | `02CB8018` (+0x048) | f32 | **0.0** | 0.01 | `subss`/`addss`, one constant **+ clamp** | **`[0.0, 1.0]`** |
| **146** | `001D34F9` | Map Eye Ambient Bound | `02CB801C` (+0x04C) | f32 | **0.6** | 0.01 | `subss`/`addss`, one constant **+ clamp** | **`[0.0, 1.0]`** |
| 147 | `001D3542` | Map BGNPC Fresnel Enabled | `02CB7FD0` (+0x000) | b | **1** | — | `cmp`/`sete` flip | — |
| 148 | `001D3555` | Map BGNPC Fresnel Intensity | `02CB7FD4` (+0x004) | f32 | **3.9** | 0.01 | **`addss`/`addss`, two constants** | — |
| 149 | `001D358B` | Map BGNPC Fresnel Power | `02CB7FD8` (+0x008) | f32 | **2.7** | 0.01 | **`addss`/`addss`, two constants** | — |
| 150 | `001D35C1` | Map BGNPC Fresnel Clamp Value | `02CB7FDC` (+0x00C) | f32 | **−0.8** | 0.01 | **`addss`/`addss`, two constants** | — |
| 151 | `001D35F7` | Map BGNPC Fresnel Skin Intensity | `02CB7FE0` (+0x010) | f32 | **2.0** | 0.01 | **`addss`/`addss`, two constants** | — |
| 152 | `001D362D` | Map Camera Light Enabled | `02CB7FE4` (+0x014) | b | **1** | — | `cmp`/`sete` flip | — |
| 153 | `001D3640` | Map Eye Camera Light X Modifier | `02CB8008` (+0x038) | f32 | **0.0** | 0.01 | **`addss`/`addss`, two constants** | — |
| 154 | `001D3676` | Map Eye Camera Light Y Modifier | `02CB800C` (+0x03C) | f32 | **0.43** | 0.01 | **`addss`/`addss`, two constants** | — |
| 155 | `001D36AC` | Map Eye Camera Light Z Modifier | `02CB8010` (+0x040) | f32 | **0.0** | 0.01 | **`addss`/`addss`, two constants** | — |
| 156 | `001D36E2` | Map Hair Specular Power Modifier | `02CB8020` (+0x050) | f32 | **1.5** | 0.01 | **`addss`/`addss`, two constants** | — |
| 157 | `001D3718` | Map Hair Specular Power Eye Camera Distance Factor | `02CB8024` (+0x054) | f32 | **0.03** | 0.01 | **`addss`/`addss`, two constants** | — |
| 158 | `001D374E` | Map Hair Specular Intensity Before Clamp Modifier | `02CB8028` (+0x058) | f32 | **1.8** | 0.01 | **`addss`/`addss`, two constants** | — |
| 159 | `001D3784` | Map Hair Specular Intensity Before Clamp Eye Camera Distance Factor | `02CB802C` (+0x05C) | f32 | **0.5** | 0.01 | **`addss`/`addss`, two constants** | — |
| 160 | `001D37BA` | Map Hair Specular Intensity After Clamp Modifier | `02CB8030` (+0x060) | f32 | **0.31** | 0.01 | **`addss`/`addss`, two constants** | — |
| 161 | `001D37F0` | Map Hair Specular Intensity After Clamp Eye Camera Distance Factor | `02CB8034` (+0x064) | f32 | **0.04** | 0.01 | **`addss`/`addss`, two constants** | — |
| 162 | `001D3826` | Map Hair Camera Light X Modifier | `02CB8038` (+0x068) | f32 | **0.0** | 0.01 | **`addss`/`addss`, two constants** | — |
| 163 | `001D385C` | Map Hair Camera Light Y Modifier | `02CB803C` (+0x06C) | f32 | **−0.13** | 0.01 | **`addss`/`addss`, two constants** | — |
| 164 | `001D3892` | Map Hair Camera Light Z Modifier | `02CB8040` (+0x070) | f32 | **0.0** | 0.01 | **`addss`/`addss`, two constants** | — |
| **165** | `001D4BFA` | Re-read soft particle config | — | — | — | — | **do-nothing** | — |
| **166** | `001D2923` | Use soft particle | — | — | — | — | **virtual call, §7** | — |
| 167 | `001D2983` | SSS enable | `02CB8434` (+0x464) | b | **1** | — | `cmp`/`sete` flip | — |
| 168 | `001D2996` | SSS Width | `02CB8438` (+0x468) | f32 | **7.0** | 0.1 | `subss`/`addss`, one constant | — |
| 169 | `001D29CC` | SSS Diffuse a | `01DFE1AC` | f32 | **1.0** | 0.1 | `subss`/`addss`, one constant | — |
| 170 | `001D2A02` | SSS Diffuse b | `01F82EE4` | f32 | unknown | 0.1 | `subss`/`addss`, one constant | — |
| 171 | `001D2A38` | SSS Blur | `+0x1EC` of the object returned by the accessor called at `001D2A38` | f32 | unknown | 0.1 | `subss`/`addss`, one constant | — |

**Shape census, this slice:** 27 float steps, 3 toggles, 1 call arm, 1 do-nothing. **Direction
mechanism:** 21 `addss`/`addss`, 6 `subss`/`addss`. **Bounds:** 2 of 32 (ids 145 and 146).

**Only ids 169, 170 and 171 leave the object.** Three of the five SSS parameters live elsewhere — one
in initialised `.data`, one in the zero-filled tail, one behind an accessor — while `SSS enable` and
`SSS Width` are fields of the same object as the rest of the slice. **A parameter group is not
evidence that its storage is grouped.**

## 4. The parameters are named — the console labels itself

Slices A–D reported their targets as bare addresses because nothing in an arm names its field. **The
names were in the image the whole time, one table away.** The console's row renderer prints

```asm
001CEA5A  cvtps2pd xmm0, xmm0
001CEA63  mov  rax, [r15 + r13*8 + 0x130]      ; <- the row's label, indexed by command id
001CEA6B  lea  r8,  [009000A8]                 ; "%s%s%f"
```

`r13` is the command id and `r15` the console context object, so **`ctx + 0x130 + 8·id` is a
`char*` label per row.** `FUN_001d0390` fills that array literally — `lea rax,[rip+str]` followed by
`mov [rdi+disp], rax` — so `id = (disp − 0x130) / 8`.

**Extraction result: 293 labels for ids 1–294, zero collisions, zero stores that did not fit the
pattern.** Every one of the 282 ids that has an action arm has a label; the single unlabelled id (2)
has no arm.

### Why the id alignment is proven rather than assumed

A label table is worthless if it is off by one, and an off-by-one would still look plausible. Four
independent checks, none of which relies on the others:

1. **The dispatcher's own arithmetic.** `001D1660` begins `add r9d, -0xC` / `cmp r9d, 0x119` / `ja` —
   so the action table holds 282 entries for ids **12–293**, and the id base of 12 is read from the
   code, not assumed. The renderer's is `lea eax,[r13-1]` / `cmp eax, 0x125` — ids **1–294**.
2. **Behaviour matches meaning.** Id 103's label is **"Camera Over Write (O to capture)"** and slice C
   found that arm captures three values from live engine state into the fields ids 104, 105 and 106
   tune — whose labels are **FOV**, **Aspect Ratio** and **Camera scale**. The one of the three that
   steps by *ratio* rather than by addition is "Camera scale".
3. **Structure matches structure.** Ids 92/93 are the only clamped pair in slice C and are labelled
   "Eye A and B Ambient **Scale**/**Bound**"; ids 145/146 are the only clamped pair in slice E and are
   labelled "Map Eye Ambient **Modifier**/**Bound**". Every `cmp`/`sete` arm in both slices carries a
   label ending in "enable" or "Enabled".
4. **A second table agrees.** The renderer draws ids 247–258 with
   `lea eax,[r13-0xF7]` into a stride-12 array — twelve consecutive slots from id 247, whose labels
   are exactly twelve character stats (Level, HP, MP, ATPOW … SPD).

### Positive control against the engine's own names

[what-the-console-tunes.md](what-the-console-tunes.md) named 21 offsets from an unrelated source: the
string-keyed config map the scene loader reads. **Twenty of those 21 have a console arm, and on all
twenty the menu label and the config key denote the same parameter.** The strongest single case is
exact:

```
config key    mEyeMapSpecularIntensityAfterClampModifier      (+0x028)
menu label    "Map Eye Specular Intensity After Clamp Modifier"   (id 140)
```

Eleven of the twenty are token-subsets outright; the rest differ only by convention or abbreviation
(`m`/`chr`/`Debug` prefixes, `Spec`→"Specular", `AB`→"A and B", `Cubemap`→"Cube map"). **Two differ in
wording while denoting the same slot** — `mDebugWaterTexBlendFactor` ↔ "Water Texture Reflection
Factor" and `mMapIrrCubemapIntensity` ↔ "Map IBL Diffuse Intensity". **No pair names two different
things.** Population: 20; contradictions: 0.

> The two naming sources are not redundant. The config key is what a *scene file* sets; the label is
> what a *developer* read. **They agree, and where they differ the difference is vocabulary, not
> referent.**

### What the label table is not authority for

**A label names the row. It does not describe the arm, and in at least one place it is misleading
about it.** [Slice H](arm-catalogue-slice-H-ids-236-267.md) §6 found three adjacent rows labelled
"Enable 100% successful steal / poach / drop" whose arms are not booleans at all: they cycle
**four, three and five** states respectively, over ranges that include `−1`.

> **Where the label and the disassembly disagree, the arm wins.** The label is evidence of what
> someone *called* a field, which is why it names targets an arm cannot — but it is not evidence of
> the field's type, range, or semantics, and "Enable" in a label does not make a row a toggle.

This bounds the instrument rather than weakening it. Everything §4 claims — 293 labels, the index
formula, the four alignment proofs, the 20-pair control — is about **which row a name belongs to**,
and none of it was ever a claim about what the row's arm does. **Use the label to name the target;
read the arm for everything else.** The positive control above is strong precisely because it
compares a name with another *name*, not a name with a behaviour.

## 5. What the label table changes about the do-nothing arms — a whole-table measurement

This is measured over **all 294 ids, not over slice E**, and is recorded here because the instrument
that makes it possible is in §4. It belongs in the parent document; it is reported, not owned, here.

The 56 ids whose action arm is `001D4BFA` are all labelled, and the console has **two** tables: the
action table (282 entries, base 12) and the renderer's (294 entries, base 1). Crossing them:

| action arm | how the row draws | count |
|---|---|---:|
| has an arm | a value row | 226 |
| **do-nothing** | **still a value row** | **38** |
| **do-nothing** | label only, no value | **12** |
| **do-nothing** | `"  (EMPTY)  "` | **6** |

**Only six rows of 282 are blank in the menu** — ids 211–216, the debug menu's own text-rendering
offsets, which fall to the renderer's default arm at `001CFC86` and print the literal `"  (EMPTY)  "`
instead of their label. **Thirty-eight still display a live value** and have simply become read-outs:
"Current LP", "Count of battle", and the twelve character stats at ids 247–258, whose renderer arm
reads the real stat array. **Twelve are labelled buttons** whose action was removed — "Unlock All
license: Press Circle", "Reset Parameter: Press Circle", "Re-read soft particle config" (id 165, in
this slice).

> **"56 do-nothing arms" is one number covering three different authored outcomes, and the action
> table alone cannot tell them apart** — because being unreachable from one table says nothing about
> how the other table draws you.

## 6. The object at `02CB7FD0`, and where the defaults come from

`FUN_00162410` is a compiler-generated static object initializer:

```asm
00162414  lea  rcx, [02CB7FD0]      ; this
0016241B  call 0x5dc720             ; constructor
00162420  lea  rcx, [008AB7C0]
0016242B  jmp  0x808b90             ; atexit(destructor)
```

So **`02CB7FD0` is an object base, not a global**, and every `02CBxxxx` field in this slice is
`this + offset`. `FUN_005dc720` calls a base constructor `FUN_005dc580` with `rcx = this`, then
`FUN_005dc430` with `rcx = this + 0xD0` for a sub-object, then writes its own fields from `+0x42C`.

**The defaults in §3 are read from those constructors**, with two decodings that matter:

- **Width comes from the store.** `+0x000` and `+0x014` are `mov byte ptr [rcx+d], 1` — one byte, so
  ids 147 and 152 default to *enabled*, not to a float. Merging all three constructors into one
  offset map without widths gave "Map BGNPC Fresnel **Enabled** = 3.9", which is how the mistake
  announced itself.
- **`mov qword ptr [rcx+0x34], 0x3fa66666` is two fields, not one.** The compiler merges adjacent
  4-byte fields into one 8-byte store: `+0x34` = `1.3`, `+0x38` = `0.0`. Three such stores cover ids
  143/153, 154/155 and 161/162.

`005DC580` covers `0x00–0xC4` and `005DC720` covers `0x42C–0x4D8`; **the two ranges do not overlap**,
so no field takes a default from an ambiguous source. `005DC430`'s displacements are *not* object
offsets and are excluded — they are the sub-object's, which is where
[what-the-console-tunes.md](what-the-console-tunes.md) places `chrFresnelSpecular*` at `+0xD0`.

**Nothing in this slice has an image-resident default except id 169.** `02CB7FD0` and everything
after it sit past the end of `.data`'s raw bytes — zero-filled at load and set by the constructor at
startup. `01DFE1AC` (id 169, "SSS Diffuse a") *is* in raw `.data`, holding `1.0`.

## 7. Ids 165 and 166 — the two arms that are not tuning

**Id 165, "Re-read soft particle config", is a do-nothing arm.** Its renderer arm is the shared
label-only target, so the row still appears in the menu and does nothing when pressed.

**Id 166, "Use soft particle", is the only call arm in the slice**, and it is the only arm here that
does not return through `001D4BFA`:

```asm
001D2923  mov   rcx, [01F82D20]      ; a subsystem singleton
001D2931  mov   ebx, [rcx + 0x38]
001D2934  cmp   ebx, 1
001D2937  setne sil                  ; flag = (field != 1)
001D293E  call  0x1df340             ; (edx = 0x0E, r8d = flag)
001D2943  mov   rcx, [rdi + 0xa80]   ; a console-held object
001D294D  je    0x1d4b65             ; null -> the other tail
001D2953  mov   rax, [rcx]
001D2959  setne dl                   ; the SAME flag, recomputed
001D295C  call  qword ptr [rax + 0x60]   ; virtual
001D295F  jmp   0x1d4b65
```

It reads a subsystem's current state, derives a boolean from it, and pushes that boolean to **two**
places: a setter and a virtual method on an object the console holds at `rdi + 0xA80`. `001DF340` is
a 10-byte setter with **15 callers across 2 owner subsystems** — small enough to name here; the
`0x0E` is a channel or key selector, not decoded. **The virtual target is not resolved**: the object
at `rdi + 0xA80` has no static type in this slice, so slot `+0x60` names nothing.

## 8. Data structures and formulas

```
console context (rdi in an arm, rcx at entry, r15 in the renderer)
  +0x0130  char* label[294]         one per command id  (0x130 + 8*id)
  +0x0A68  byte   initialised
  +0x0A6C  int    cursor row within the page
  +0x0A80  ptr    the object id 166 calls virtually
  +0x0A88  int    page index                 page*22 + row -> command id
  +0x0C56  byte   suppresses the "==>>" cursor
  +0x0E68  int    stat array, stride 12, read by the renderer for ids 247-258
  +0x10A8  int    selected character

rendering settings object, base 02CB7FD0, constructed at startup
  +0x000  byte   Map BGNPC Fresnel Enabled        +0x038..0x040  Map Eye Camera Light XYZ
  +0x004..0x010  Map BGNPC Fresnel params         +0x044..0x04C  Map Eye Diffuse / Ambient
  +0x014  byte   Map Camera Light Enabled         +0x050..0x070  Map Hair params
  +0x018..0x034  Map Eye Specular params          +0x074..0x090  Water params (slice D)
  +0x0D0         sub-object (chrFresnelSpecular*) +0x464..0x468  SSS enable / Width
```

**Row layout:** the renderer computes the selected id as `table[page·22 + row]` from a dword table in
`.rdata`, so the menu is paged **22 rows at a time** and the on-screen order is that table's order,
not id order.

## 9. Call chain

```
input -> console dispatcher 001D1660 (id-12 -> arm)         writes the field
      -> row renderer       001CD0E0 (id-1  -> arm)         reads the field + its label
startup -> 00162410 -> 005DC720 -> 005DC580                 writes every default
scene load -> the config map readers named in what-the-console-tunes.md
```

**Who consumes these values is only partly known.** Within both a function-bounded cross-reference
sweep and a linear `.text` scan that is not bounded by the function list, `SSS Width` has a real
consumer (`006089FF` copies it into an object field), and `Map BGNPC Fresnel Enabled` is read from
several subsystems — but for the 21 `Map Eye` / `Map BGNPC` / `Map Hair` **floats, the only readers
found are the console arm and the row renderer.** That is a measurement over two scans, not a proof
of absence: a value passed by pointer or uploaded as part of a constant-buffer block would not appear
in either. **Recorded as an open question, not as "these do nothing."** One candidate hit was checked
and discarded as a mid-instruction decode artifact.

## 10. Modding notes

Every value in §3 is a live float at a fixed address in a fixed object; the defaults column is what
the game starts with, so a mod that writes these directly is setting the same fields the debug menu
sets. **The two clamped rows (145, 146) clamp in the *arm*, not in the field** — the clamp is the
console's, so a direct write is not bounded by `[0.0, 1.0]` and nothing downstream re-checks it.

## 11. What is not known

- **What the object at `02CB7FD0` is called.** Its constructor and destructor are known and its
  fields are named row by row, but no string or RTTI marker in reach names the type itself.
- **Whether the 21 `Map …` floats have a consumer at all** in the shipping build (§9).
- **The virtual target of id 166** and the meaning of the `0x0E` selector (§7).
- **Defaults for ids 170 and 171** — neither field is written by a constructor found here.
- **`SSS Diffuse a` and `b` do not live together**: `a` is image-initialised at `01DFE1AC`, `b` sits
  in the zero-filled tail at `01F82EE4`. Why the pair is split is not known.

## 12. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The id → arm mapping for all 32 ids | dwords at `001D4C1C + (id−12)×4`, `+ 0x00120000`, re-derived from the image | 1 |
| The id base of 12 and the 282-entry bound | `add r9d, -0xC` / `cmp r9d, 0x119` at `001D166F` | 1 |
| Every target, magnitude, mechanism and bound | complete decode of each arm, bounded by the next arm's start | 1 |
| The two-constant direction mechanism | both branch constants read from `.rdata`: `+0.01` and `−0.01` | 1 |
| 293 labels, ids 1–294, 0 collisions | every `lea`+`mov` pair in `FUN_001d0390` decoded; 0 non-conforming stores | 1 |
| The label index formula | `[r15 + r13*8 + 0x130]` at `001CEA63`; installer displacements match `0x130 + 8·id` | 1 |
| `02CB7FD0` is an object base | `lea rcx,[02CB7FD0]` passed as `this` by the static initializer `00162410` | 1 |
| Every default in §3 | immediate stores in `005DC580` / `005DC720`, decoded with the store's width | 1 |
| The action × render cross-tab (226/38/12/6) | both jump tables walked in full for all 294 ids | 1 |
| Ids 247–258 are twelve stats | `lea eax,[r13-0xF7]` into a stride-12 array at `001CFC47` | 1 |

**Controls.** The absence claims are *"only ids 145 and 146 are bounded"* and *"only id 166 calls"*.
The same extractor positively detects `maxss`/`minss` in 145 and 146, `cmp`/`sete` in 147, 152 and
167, and `mulss` in slice C's id 106 — so each zero is a measurement, not a silent non-match. The
label table's alignment carries **four independent confirmations** (§4) and one cross-source control
over a population of 20 with zero contradictions.

**Three errors were made and corrected while producing this document**, all recorded because they
shaped the method: merging three constructors into one offset map produced a float default for a
one-byte boolean (§6); a linear `.text` scan produced a consumer for `01DFE1AC` that disassembled as
`jnp`/`rol` from a mid-instruction offset and was discarded (§9); and **the extractor required a
`movss` load before it would call an arm a float step**, which mis-files any arm whose value arrives
as a *function return* and goes back through a setter. **Slice E's census is unchanged by that
correction** — re-run after the fix: 27 float, 3 toggle, 1 call, 1 do-nothing — because no arm in
this slice has that shape. It is disclosed because the corrected extractor produced the whole-table
figures in §5 and §2's per-slice comparison.

> Requiring a `movss` to see a float step is the same mistake as requiring a `subss` to see a
> decrement: **an extractor keyed on the common encoding of a thing, reporting the absence of the
> thing.** Both are in this document. **Check what a classifier requires, not only what it matches.**

**Address review flags** (`001D4C1C` and every arm address) are dispositioned once for all slices in
[slice A](arm-catalogue-slice-A-ids-12-43.md) §8 — the first is the dispatch table in `.text` after
the function, and switch arms are interior addresses of a function, not functions.

## 13. Related

- [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md) — the slice division and row shape.
- [the-282-command-parameter-console.md](the-282-command-parameter-console.md) — the parent document.
- [what-the-console-tunes.md](what-the-console-tunes.md) — the config-key naming route, and the
  positive control in §4.
- [slice C](arm-catalogue-slice-C-ids-76-107.md) — the clamped Ambient pair and the camera group whose
  labels confirm the id alignment.
- [slice D](arm-catalogue-slice-D-ids-108-139.md) — shares the object at `02CB7FD0` and, per the
  measurement in §2, the two-constant direction mechanism.

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

**This slice produced the label table and it also bounds it.** §4's caveat — *a label names the row, it
does not describe the arm* — was written here **before** the propagation pass consumed the table, not
after.

**Corroborated, and this is the catalogue's strongest cross-check:** id 166 "Use soft particle" passes
`edx = 0xE` for field `+0x38`, and `0x38 / 4 = 14`. **That was extracted here before slice I's
numbering rule existed**, so two slices agree about a rule neither derived from the other.

Twenty-one arms in this slice use the third direction mechanism, second only to D.


*(Pass 22 adjacency, 2026-09-14: the shared machinery this slice cites crosses layers — the
renderer `001CD0E0` reaches **audio** `002DEBA0`, **achievements** `003166F0` and **resource**
`0020C700`; the dispatcher `001D1660` reaches `002DEBA0`/`001DBB00` (audio) and `002EEEE0`
(resource); and `001DF340` is called by **online** `007A0C60` and **platform** `001DD170` —
8 edges. Console draw/fetch plumbing is shared with the render path, and `001DF340` is consumed
by platform init, not owned by it.)*

## SWE2-EC7-40 update (2026-09-19) - `005DC580`

`005DC580` (359 B) is the `0x00`-`0xC4` default writer the page names - call-free record initializer, float constants (`0x4079999a`, `0x402ccccd`, `0xbf4ccccd`...) into `rcx` fields plus byte `+0`/`+0x14` flags. Interior anchor `005DC591` (the `0x4079999a` store).

## SWE2-EC7-41 update (2026-09-19) - `005DC430`

`005DC430` (325 B) is the call-free `+0xD0..+0x180` defaults writer the page names - 39 literal-offset stores of float/dword constants (`0x4079999a`, `0x402ccccd`, `0xbf4ccccd`, `0x3f800000`...) into the record. Interior anchor `005DC4A5` (a mid-record `mov [rcx+0x44]` store).

## SWE2-EC7-126 update (2026-09-21) - the tuning-record ctor measured

`005DC720` (362 B) is the
ctor `00162410` hands the
`02CB7FD0` tuning block to:
`005DC580` + `005DC430`
init the `+0xD0` member,
then the defaults land -
`+0x448` = 1.0f, `+0x454` =
-0.5f, `+0x458`/`+0x460` =
0.5f, `+0x464` byte = 1,
`+0x468` = 7.0f -
`005CC8A0` runs at `+0x4B0`,
and a 2-iteration loop
repeats the same field
pattern over the 0x598-stride
element array rooted at
`+0xA1D` before `+0x1010`/
`+0x1018`/`+0x1020` are
zeroed. Interior anchor
`005DC807` (the per-element
`005DC580` call).

`001DCB90` (404 B) is the record formatter `001CD0E0` calls: `00861EC0` clears a `0x100` stack buffer, `0020D2B0` builds the text context, `dword[rbx+0x48] * 0x140` selects the `[rbx+0x78] + 0x104` entry, and `0020DA50`/`0020D9F0`/`001A1E40`/`001CD050` fill the line - the console's entry-to-text arm.

Interior anchor `001DCBD4` (function `001DCB90`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-EC7-160)

**Presentation — MECHANICAL (18 edges).** Batch-125's `001DCB90` names its caller `001CD0E0`
(which itself calls `001DCD30` and is called by `001D0190`/`001D5260`) plus `001D0390`; those
console-entry helpers' other neighbours are Presentation-tagged. Shared-helper exchange, not a
console responsibility.

`0020DA50` (94 B) is the predicate chain `001CD0E0`/`001DCB90` call: `call [rax]` on the head's vtable slot 0, and on false advances `rbx = [rbx + 8]` through the linked list until a node's vtable returns true or the list empties - the console's chain-of-responsibility probe.

Interior anchor `0020DA6A` (function `0020DA50`).

`0020D2B0` (59 B) is the context constructor `001CD0E0`/`001DC9D0`/`001DCB90` call: zeroes `[rcx + 0x10..0x2C]`, stores vtable `00906880` at `[rcx]` and `01E02580` at `+8`, then writes `01F83460` into the `01E02588` global - the console entry's initial state.

Interior anchor `0020D2C4` (function `0020D2B0`).

`001CD050` (114 B) is the growth guard the console text helpers share (9 callers): `r8 > 0x1555555555555555` traps, `r8 * 3 * 4 >= 0x1000` then requires `rdx` 0x20-aligned with `[rdx - 8]` a valid block start within 8 bytes, else traps via `008C2DA8` - the CRT vector-expansion bounds check.

Interior anchor `001CD06A` (function `001CD050`).
- **Save_Load_Settings — CLIENT (1 edge).** 1 inbound (Save_Load_Settings bodies `SaveImage_FinalizeHeaderAndChecksum` (00583D60) call page-cited `003166F0`). Substantive edges include `003166F0` is called by `SaveImage_FinalizeHeaderAndChecksum` (00583D60).
- **WorldAreaField — CLIENT and SERVICE (3 edges).** 1 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020) call page-cited `002DEBA0`); 2 outbound (page-cited `001CD0E0` call WorldAreaField bodies `WorldTransition_GetTransitionFieldId` (00314910), `FieldData_GetVariable0` (00265270)). Substantive edges include `001CD0E0` calls `WorldTransition_GetTransitionFieldId` (00314910); `001CD0E0` calls `FieldData_GetVariable0` (00265270); `002DEBA0` is called by `World_UpdateSimulationTick` (00314020).
