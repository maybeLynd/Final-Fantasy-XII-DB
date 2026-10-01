---
system: Arm catalogue — slice F, command ids 172–203
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
    verified: 6 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
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

# Arm catalogue — slice F, command ids 172–203

> Slice F of the division in [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md).
> **32 command ids. It says nothing about the other 250.**

## 1. What the player sees

Nothing — a developer tool. Slice F is where the console stops being a bank of sliders and becomes a
**control panel**: three quarters of its commands are switches and mode cycles rather than nudges, a
third ignore the up/down direction entirely, and eight of them read a **second button** that no
earlier slice used at all.

## 2. Does the arm shape hold here? No — and this slice breaks it in four different places

The first question asked of every slice. **Slice F is the least uniform range read so far**: 27 real
arms in **18 distinct body sizes**, from 20 bytes to 149.

| kind | count |
|---|---:|
| boolean toggle | 11 |
| integer cycle / step | 9 |
| float step | 7 |
| unimplemented | 5 |

**And the direction convention is not one convention:**

| direction inputs read | arms |
|---|---:|
| `bl` only (the sign flag every earlier slice used) | 11 |
| **`bl` and `sil` as two separate buttons** | **8** |
| **neither — the command is unconditional** | **8** |

> **Eight of the 27 arms ignore the direction flag completely.** Pressing the command flips the value
> whichever way the caller set argument 2. In slices A–D the flag was universal among stepping arms;
> here a third of the range does not consult it.

## 3. Argument 3 is finally used, and it is used two different ways

Slice B decoded the console prologue and found a third byte argument arriving in `r8b` and living in
`sil`, **with no observed consumer.** Slice F has eight, and they are not all the same:

**As the second half of a two-button pair** — `bl` means down, `sil` means up, neither means do
nothing:

```asm
001D3AE5  test  bl, bl          ; down button
001D3AE7  je    0x1d3aef
001D3AE9  dec   dword ptr [rdi + 0xc38]
001D3AEF  test  sil, sil        ; up button
001D3AF2  je    0x1d3afa
001D3AF4  inc   dword ptr [rdi + 0xc38]
```

**As a gate on one branch** — the toggle happens if `bl` is set, or if `bl` is clear *and* `sil` is
set:

```asm
001D3E7A  test  bl, bl
001D3E7C  jne   0x1d3e87        ; bl set -> toggle
001D3E7E  test  sil, sil
001D3E81  je    0x1d4bfa        ; bl clear and sil clear -> do nothing
001D3E87  cmp   byte ptr [rdi + 0xc70], 0   ; toggle
```

**So `bl` is not "the direction flag" in general — it is argument 2, and what an arm makes of it is
per-arm.** The name is a slice-A generalisation that holds for slices A–D and fails here.

## 4. The catalogue

Row shape per the work order: **field · width · step magnitude · direction mechanism · bound.**
`b` = byte, `d` = dword field of the object at `rdi`; *accessor* = a field of the object returned by
the 16-arm accessor named in §6.

| id | arm | kind | target | magnitude | direction mechanism | bound |
|---:|---|---|---|---|---|---|
| 172 | `001D1E9D` | int cycle | accessor `+0x19C` | 1 | `cmove` ±1 (`bl`) | **wraps, 4 states** |
| 173 | `001D1ED4` | float step | accessor `+0x1A0` | 0.005 | **signed pair into a register** | — |
| 174 | `001D1F0D` | float step | accessor `+0x1A4` | 0.005 | **signed pair into a register** | — |
| 175 | `001D2A7D` | int cycle + apply | `d+0xD78` | 1 | `cmovne` ±1 (`bl`) | **wraps, 3 states**; then dispatches on the result |
| 176 | `001D2BEF` | boolean toggle | `b+0xAC6` | — | **none** | 0/1; then one call |
| 177 | `001D2C25` | int cycle | `d+0xAC8`, tracks `d+0xACC` | 1 | branch ±1 (`bl`) | **bound read from `d+0xAD0`** |
| 178 | `001D2C91` | int cycle | `d+0xAC8`, `d+0xACC` | 1 | branch ±1 (`bl`) | **bound read from `d+0xAD0`**; then one call |
| 179 | `001D2964` | boolean toggle | accessor `+0x4A0` | — | **none** | 0/1 |
| 180 | `001D2CFC` | int cycle | `d+0xAD4`, `d+0xAD8` | 1 | branch ±1 (`bl`) | **bound read from `d+0xADC`** |
| 181 | `001D2D68` | int cycle | `d+0xAD4`, `d+0xAD8` | 1 | branch ±1 (`bl`) | **bound read from `d+0xADC`**; then one call |
| 182 | `001D2DD3` | int step | `d+0xAE0` | 1 | branch ±1 (`bl`) | **clamped `[0, 8]`, does not wrap**; then one call with value−1 |
| 183 | `001D2E04` | boolean toggle | **no field** — read and written by a call pair | — | **none** | 0/1 |
| **184** | `001D4BFA` | **unimplemented** | — | — | — | — |
| 185 | `001D3A91` | boolean toggle | `b+0xC34` | — | **none** | 0/1 |
| 186 | `001D3AE5` | int cycle | `d+0xC38` | 1 | **two-button** (`bl` down, `sil` up) | **wraps mod 4** |
| 187 | `001D3AA6` | boolean toggle | `b+0xC35` | — | **none** | 0/1 |
| 188 | `001D3ABB` | boolean toggle | `b+0xC3C` | — | **none** | 0/1 |
| 189 | `001D3C3C` | float step | via a getter/setter pair | 0.01 | one constant, `subss`/`addss` (`bl`) | — |
| 190 | `001D3CBD` | float step | via a getter/setter pair | **0.002, scaled** | **two-button** | — |
| 191 | `001D3D17` | float step | via a getter/setter pair | **0.002, scaled** | **two-button** | — |
| 192 | `001D3D84` | float step | via a getter/setter pair | **0.002, scaled** | **two-button** | — |
| 193 | `001D3DE5` | float step | via a getter/setter pair | **0.1, scaled** | **two-button** | **refused outside `[15.9, 48.0]`** |
| **194** | `001D4BFA` | **unimplemented** | — | — | — | — |
| **195** | `001D4BFA` | **unimplemented** | — | — | — | — |
| 196 | `001D454A` | int cycle | `d+0xD90` | 1 | **two-button** | **wraps, 3 states** |
| 197 | `001D3E7A` | boolean toggle | `b+0xC70` | — | **`sil` gates the `bl`-clear path** | 0/1 |
| **198** | `001D4BFA` | **unimplemented** | — | — | — | — |
| 199 | `001D3E9C` | boolean toggle | `b+0xCEC` | — | **none** | 0/1; preceded by one call — **`Debug_SetGilToMaximum` (`003058B0`), the command itself** ("Set gill to max"; corrected 2026-09-13) |
| 200 | `001D3EB6` | boolean toggle | `b+0xCED` | — | **none** | 0/1; preceded by one call — **`00305A00`: stores LP `+0x190 = 99,999` (`0x1869F`, `00305A87`) for each party member the nine-slot walk `BattleStats_GetByMappedBattleSlot(i, 3)`, `i < 9`, finds (roster kept at `022C1740`), then `00316C60`** ("Set LP to max"; corrected 2026-09-13) |
| 201 | `001D3ED0` | boolean toggle | `b+0xCEE` | — | **none** | 0/1; preceded by two calls — **`00305960`: `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth(member, 99, 0)` (`003059CB`) for each party member the nine-slot walk `BattleStats_GetByMappedBattleSlot(i, 3)`, `i < 9`, finds (roster kept at `022C1740`) — the ordinary growth path with its notification; then `003058C0`: a raw store of experience `+0x18C = 99,999,999` (`0x5F5E0FF`, `00305927`) for the same members** ("Set level to max"; corrected 2026-09-13 on `OPUS-CONSOLE-ID201-CALLS`) |
| 202 | `001D3C77` | boolean toggle | `b+0xC3E` | — | **`sil` gates the `bl`-clear path** | 0/1 |
| **203** | `001D4BFA` | **unimplemented** | — | — | — | — |

**27 real arms and 5 unimplemented** (184, 194, 195, 198, 203). *(2026-09-13: in ids 199–201 the boolean is the least of it — the preceding calls are the command, as the rows now say. None of the three is among the 16 ids the retail image can issue ([the parameter console](the-282-command-parameter-console.md)), so all three are debug-only.)*

## 5. Four mechanisms this slice adds to the catalogue

### 5.1 A step constant that never appears as a memory operand

Ids 173 and 174 load the signed constant **into a register** and then add register to register:

```asm
001D1ED4  test  bl, bl
001D1ED8  movss xmm7, [-0.005]      ; one direction
001D1EE2  movss xmm7, [+0.005]      ; the other
001D1EEA  call  <accessor>
001D1EEF  movss xmm6, [rax + 0x1a0]
001D1EF7  addss xmm6, xmm7          ; <- no constant in this instruction
```

**An extractor that reads the memory operand of `addss` finds nothing here.** This is a third distinct
encoding of the same idea, after the one-constant `subss`/`addss` of slices B and C and the
two-memory-constant signed pair of slice D. The magnitude is `0.005` and the pair is exact.

### 5.2 A bound that is data, not a literal

Ids 177, 178, 180 and 181 do not compare against a constant. They compare against **another field of
the same object**:

```asm
001D2C5D  mov   ecx, dword ptr [rdi + 0xad0]   ; the limit, read at run time
001D2C63  cmp   ecx, eax
001D2C65  jle   0x1d2c71
001D2C67  inc   eax
```

Wrapping down from zero loads that same field as the new value, so the pair `0xAC8`/`0xAD0` is
**cursor and count**, and `0xACC` is a second cursor the arm keeps from exceeding the first.

> **Every bound in slices A–D was a literal — a number somebody chose.** These four are the first
> whose authored intent is *"as many as there are"*, and a catalogue that recorded only literals would
> have shown them as unbounded.

### 5.3 A step that scales with a selector

Ids 190–193 all read the **same** field, `rdi+0xC58`, and use it to scale their own step:

```asm
001D3CBD  mov   ecx, dword ptr [rdi + 0xc58]   ; the selector
001D3CC3  movss xmm6, [0.002]                  ; the base step
001D3CCB  cmp   ecx, 0x14
001D3CCE  jle   0x1d3cee                       ; <= 20: use the base step
001D3CD0  mov   eax, 0x66666667                ; > 20: divide the selector by 5
001D3CD5  imul  ecx
001D3CD7  sar   edx, 1
001D3CE7  mulss xmm0, xmm6                     ; step = (selector / 5) * base
```

**Below a selector of 20 the step is the base; above it the step grows with the selector.** The
`0x66666667` / `sar 1` sequence is the standard signed divide-by-five. **A per-arm magnitude census
records one number for these arms; the arm has two behaviours.**

### 5.4 A bound that refuses instead of clamping

Id 193 checks the *result* and, if it would cross the limit, **does not step at all**:

```asm
001D3E20  movss xmm1, [48.0]
001D3E28  addss xmm0, xmm6
001D3E2C  comiss xmm1, xmm0
001D3E2F  jb    0x1d3e60          ; would exceed 48.0 -> skip the write entirely
...
001D3E45  subss xmm0, xmm6
001D3E49  comiss xmm0, [15.9]
001D3E50  jb    0x1d3e60          ; would fall below 15.9 -> skip
```

**This is the third bound mechanism in the catalogue** — after *wrap* (ids 14, 172, 186, 196) and
*clamp/saturate* (ids 92, 93, 114, 115) — and it behaves differently at the limit: a clamped value
rests exactly on the boundary, a refused value stops short of it by up to one step.

## 6. Call chain

```
console dispatch  001D1660   (arg1 rcx -> rdi, arg2 dl -> bl, arg3 r8b -> sil)
  -> table 001D4C1C + (id - 12)*4 -> + 0x00120000 -> the arm
     ids 172..174, 179  : the 16-arm accessor -> fields +0x19C, +0x1A0, +0x1A4, +0x4A0
     ids 189..193       : a getter/setter pair, one call to read and one to write
     ids 175..182, 185..188, 196, 197, 199..202 : fields of the object at rdi
  -> jmp 001D4BFA   the shared tail
```

(16 edges cross into the Presentation layer on this slice alone: `001D1660` itself calls the
Presentation-owned materializers `001D5120`/`001C7360`/`001C7520`; the label-filler `001D0390`
is called by `001CCB20` and calls `001CD0E0`; `001D50D0` — the singleton accessor — is reached
by `001FA3D0`, `001BC190`, `00187950`, `001F8D10`, `001D5650`; and the command bodies
`003058B0`/`003058C0`/`00305960`/`00305A00` are all dispatched *from* `001D1660`. The arms live
on the render path — same shape as slice D's accessors. Past Presentation, the arm bodies reach
the systems they tune: `003058C0`/`00305960`/`00305A00` call **combat-formula** `00320AB0` (3),
`003058B0` calls **economy** `00254EE0` and `00305960` calls `0030C650` (the "Set gill to max" /
rewards plumbing, 2), `00305A00` calls **achievements** `00316C60` → `00316760` (2), and the
dispatcher itself reaches **audio** `002DEBA0`/`001DBB00` and **resource** `002EEEE0` (3).)

The accessor used by ids 172–174 and 179 is the one this catalogue names rather than cites: **16 arms,
33 call sites, 47 caller functions image-wide.** The getter/setter pairs behind ids 189–193 are not
characterised here.

## 7. Modding notes

- **A third of this range ignores the direction argument.** Ids 176, 179, 183, 185, 187, 188 and
  199–201 flip regardless; sending "down" to them is the same as sending "up".
- **Eight commands need argument 3.** A tool that drives the console with argument 3 left at zero
  gets *nothing* from ids 186, 190–193 and 196 in the up direction, and nothing at all from 197 and
  202 unless argument 2 is set.
- **Ids 177/178 and 180/181 are pairs on the same fields** — the second of each pair does what the
  first does and then makes a call. They are not independent settings.
- **Id 193 stops short of its limits rather than resting on them.**
- **Five ids in this range do nothing** — 184, 194, 195, 198, 203.

## 8. What is not known

- [x] **UQ-18.** **What any of these fields is.** The object at `rdi` is still unidentified, so `+0xAC6`–`+0xD90`
      are offsets, not names. **No field in this slice was traced to a reader.**
      *Narrowed 2026-09-14 (FABLE), not answered: the object is identified.* `001D50D0` returns it: a `0x10E8`-byte singleton built on first use by `001CCB20` and cached at `01F81428` (`001D50DD`–`001D5106`). The same object carries the console's labels at `+0x130 + 8 × id`, which `001CCB20` clears (`001CCE6F`) before `001D0390` fills them (`001CCEA4`). `001D1660` receives it through `001CD040`'s pass-through `rcx` (the steal page's `FK-3`, [the steal roll](../../08-Combat-Formula/Steal/the-steal-roll.md)). The fields still have no
      traced reader.
      **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): each field is named by its own console label, and four have
      readers outside the console.** The labels ([console-command-names](console-command-names.md)) name every
      field in this slice:
      - `+0xAC6` Show Map Hide Group;
      - `+0xAC8`–`+0xAD0` Particle Draw Type Range, start and end with the bound;
      - `+0xAD4`–`+0xADC` Map render DisplayList Id range;
      - `+0xAE0` Fusion Technique Select;
      - `+0xC34` Huge Damage;
      - `+0xC35` Enable mouse control camera;
      - `+0xC38` Camera speed;
      - `+0xC3C` Enable reading key mapping from file;
      - `+0xC3E` File Cache Enable;
      - `+0xC70` 100% Spawn Rare Monster;
      - `+0xCEC`–`+0xCEE` the set-gil / LP / level toggles, whose commands act at once;
      - `+0xD78` Yebis enable;
      - `+0xD90` Procedural texture rotation ratio.

      A getter-seeded census found readers outside the console. It seeds every caller of `001D50D0` and every
      direct load of `01F81428`, and each candidate's receiver was checked to come from the getter:
      - **`+0xC34` Huge Damage.** `0017D360` returns it as a bool. `Battle_ProcessActionTarget` asks it right after
        `BattleFormula_ResolveTargetResult` (`0030757C`) and then tests the source's kind byte.
      - **`+0xC35` mouse camera.** `00197160` gates on it (`001973C8`–`001973D4`).
      - **`+0xC70` rare-monster spawn.** `0017D430` returns it. Its caller `003504B0` is script verb `0x5A9`, which
        hands the flag back to the script, so the zone scripts ask for it.
      - **`+0xD78` Yebis enable.** `00180040` returns the three-state value. `MainLoop_Draw` reads it (`0022B4B0`), and
        so does the effect draw drain (`003A37F0`, which acts only when it is 1).

      Two first-pass candidates were rejected on receiver identity: `00187950` works on a different object in `r14`,
      and `001E2AF0`'s `+0xC34` read is off `00189120()`. The other fields have no reader in this census. Its blind
      spot is the one UQ-5 records: a function handed the object through `rcx`, as the console arm is, is not seen.
- [x] ~~What the selector at `rdi+0xC58` selects, and why 20 is its threshold. **Four commands scale
      their step by it**, so it is the highest-leverage unknown in this slice.~~ **Answered 2026-09-14 (FABLE): in this image it
      selects nothing, because it is always 0.** A census of `+0xC58` accesses in `001C0000`–`001E0000` finds one store,
      the constructor's `mov [rdi+0xC58], ebp` at `001CCC9F`, with `ebp` zeroed at `001CCB45` and callee-saved across the
      intervening calls, and four reads, the ids 190–193 arms. When the value exceeds 20, each arm multiplies its step by
      `sel / 5` (`0x66666667` / `sar 1`, `001D3CCB`–`001D3CEB`). A value that never leaves 0 never takes that path, so the
      threshold is vestigial here.
- [x] ~~What the getter/setter pairs behind ids 189–193 address, and what quantity is bounded to
      `[15.9, 48.0]` with a step that grows past a selector of 20.~~ **Answered 2026-09-14 (FABLE): the track map's placement.**
      The labels are *"Navi Map Scale"*, *"Adjust tracmap center x / y"*, *"… Super Wide Mul"* and *"… Super Wide MidPoint"*
      ([names](console-command-names.md)).
      - **Id 189** steps the float `+0x3AFC` of `[01F811E8]` in ±0.01 steps (`001B1C00` / `001B0F90` get, `001B1FF0` set).
      - **Ids 190–193** use 9-byte accessors on four `.data` floats (image values in brackets):
        - `01E0CE50`, centre x [`0.67`]: `002B6650` / `002B6670`;
        - `01E0CE54`, centre y [`0.6`]: `002B6660` / `002B6680`;
        - `01E0CE58`, super-wide multiplier [`1.0`]: `002B66B0` / `002B6690`;
        - `01E0CE5C`, super-wide midpoint [`21.0`]: `002B66C0` / `002B66A0`.
      - **The `[15.9, 48.0]` bound** (`48.0` at `009002E8`) belongs to the **midpoint**, id 193.
      - **Readers.** Besides the accessors, the four floats are read by `002B6B50` (called three times from the track-map
        page `002B7B80` and the track-map drawer `002B8EE0`), and `01E0CE54` also directly by those two
        ([the map screens](../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md)).
- [x] ~~What ids 199–201 call before toggling their three adjacent bytes `+0xCEC`, `+0xCED`, `+0xCEE`.~~ **Answered 2026-09-14
      (FABLE):** the labels say it, and the callees agree. Id 199, *"Set gill to max"*, calls `Debug_SetGilToMaximum` `003058B0`
      (`001D3E9C`). Id 200, *"Set LP to max"*, calls `00305A00` (`001D3EB6`), the 170-byte function that walks the party through
      `02EBF190` (see [the console](the-282-command-parameter-console.md) §12). Id 201, *"Set level to max"*, calls `00305960`
      and then `003058C0` (`001D3ED0` / `001D3ED5`), which both walk the `022C1740` table. Each arm then flips its byte; what reads
      those bytes was not traced.
- [x] ~~What id 183 toggles — it has no field at all; both the read and the write are calls.~~ **Answered 2026-09-14 (FABLE):** the
      dword at `022BE950`, *"Print Magic Info"*. `002FBA40` returns it and `002FBA50` stores `(value == 0)` (`001D2E04`–`001D2E0E`).
      Its only other reader is `002FC4A0` at `002FC5D7`, a branch that follows `003EDAD0` (the EFX parser) in the type-1
      EFX context build. The menu renderer reads it through the getter (`001CE9C9`).

## 9. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The id → arm mapping for all 32 ids | dwords at `001D4C1C + (id−12)×4`, `+ 0x00120000`, re-derived from the image | 1 |
| Every target, magnitude, mechanism and bound | complete decode of each arm, bounded by **the next arm's start address** | 1 |
| The direction-input census (11 / 8 / 8) | register reads of `bl` and `sil` counted over all 27 real arms | 1 |
| The register-held signed pair in ids 173, 174 | both `movss` constants read from `.rdata`; the `addss` has no memory operand | 1 |
| Bounds read from `d+0xAD0` and `d+0xADC` | the `cmp` operand is a field load, not an immediate | 1 |
| The divide-by-5 step scaling in ids 190–193 | `0x66666667` / `imul` / `sar 1` decoded in each of the four arms | 1 |
| 5 unimplemented ids | those entries resolve to `001D4BFA` | 1 |

**Re-derived, not copied:** 282 table entries, 227 distinct targets, 56 ids at `001D4BFA` — reproduced
from the image before any row was written. **`step` was re-derived per arm** rather than taken from
`Tools/work/repos-d2/console_arms.tsv`, whose author correctly labelled that column unverified.

**Controls.** The absence claims are *"8 arms read no direction input"* and *"ids 173 and 174 have no
constant in the `addss`"*. The same extractor positively reports `bl` in 19 arms and `sil` in 8, and
reports memory-operand constants for ids 189 and 190–193 in this same slice — so both zeros are
measurements rather than silent non-matches.

**Address review flags** (`001D4C1C` and every arm address) are dispositioned once for all slices in
[slice A](arm-catalogue-slice-A-ids-12-43.md) §8: the first is the dispatch table in `.text` after the
function, and switch arms are interior addresses of a function, not functions.

## 10. Related

- [the-282-command-parameter-console.md](the-282-command-parameter-console.md) — the frame
- [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md) — the division and its rules
- [arm-catalogue-slice-A-ids-12-43.md](arm-catalogue-slice-A-ids-12-43.md) — ids 12–43
- [arm-catalogue-slice-B-ids-44-75.md](arm-catalogue-slice-B-ids-44-75.md) — ids 44–75; **decoded the
  argument this slice is the first to find consumed**
- [arm-catalogue-slice-C-ids-76-107.md](arm-catalogue-slice-C-ids-76-107.md) — ids 76–107
- [arm-catalogue-slice-D-ids-108-139.md](arm-catalogue-slice-D-ids-108-139.md) — ids 108–139

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

**An external instrument reported this document wrong, and the document was right.** A float-step
classifier reported slice F as containing **zero** float steppers. **F's own text already had id 189
typed correctly** as *"float step via a getter/setter pair"* — and the true count is **seven** (173,
174, 189, 190, 191, 192, 193).

The classifier required a `movss` load; **190–193 take their value as a function return, step it in a
register and push it back through a setter**, and 173/174 hold the constant in `xmm7` so there is no
memory operand on the arithmetic at all.

> **Requiring a `movss` to recognise a float step is the same mistake as requiring a `subss` to
> recognise a decrement: an extractor keyed on the common encoding of a thing, reporting the absence
> of the thing.**

**The reason this landed as an instrument fault rather than an accusation against this document is
that its author's text was read first.**

*(Pass 22 live-graph completion, 2026-09-15: `00254EE0` — the gill setter the slice names —
is called by nine `Items_Equipment_Shops_License` bodies (`002FEEB0`, `002FD880`, `00310870`
and six more), and `00320AB0` calls `Gameplay` `0031B9F0` (10 edges). An arm that sets gill
is the economy seam between the console and the shop/item layer — the callers are the
item/equipment side reaching the same setter.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT and SERVICE.** One cited function is called by `BattleUnit_RunPeriodicCombatMaintenance`, and another calls `BattleStats_RecomputeDerivedStateAndAutoStatuses`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `002B7B80` on this page calls `Actor_GetWorldPosition`, owned by that layer. What it reaches is the position read, gated on the kind bits: `byte[+3] >> 5` has to be 1 or 3, and then the three floats at `[actor + 0xB8]` `+0`/`+4`/`+8` go to the caller's three out-params - anything else gets zeros rather than an error; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAction — CLIENT.** `BattleAction_RefundReservedExecutionResources`, owned by that layer, calls `00254EE0` on this page. That caller is the refund path: `byte[+5] == 0` on the stats record, and the reservation it gives back is named by `word[+0xDC8]` with `0xFFFF` meaning nothing was held; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## SWE2-EC7-36 update (2026-09-19) - `001D5650`

`001D5650` (660 B) is an arm-catalogue body - `008C5B60`/`00900360`/`01F81830`/`01F81834`, a single `001D50D0` call. Interior anchor `001D5895` (the `001D50D0` call).

## SWE2-EC7-43 update (2026-09-19) - `002B6B50`

`002B6B50` (292 B) is an arm-catalogue body - `008F30EC`/`008F311C`/`00901B3C`/`00902EEC`/`01CEBBA8`/`01E0CE50`-`01E0CE5C`, `0017FFD0` single call. Interior anchor `002B6B5A` (the `0017FFD0` call).

## SWE2-EC7-85 update (2026-09-20) - `00402A40` + `00403130` + `004022D0` measured

`00402A40` (428 B) is the element-array builder the arm callers
run: `003BED70`/`003BE3A0` yield the count, each `0x30`-stride
source byte feeds `003C0890` into `0x10`-stride stack entries,
`004023D0` filters each into `rbx` rows (0xB0-cleared via
`00861EC0`, `004027D0` stored, `+0x98`/`+0xA0` list-linked), and
the head of the built list returns - stack-cookie framed on a
0x14C0 frame.
Interior anchor `00402ADC` (the `003C0890` element call).

`00403130` (79 B) is the scale write the same callers run: for each
`[rcx+0x60]`-linked element with `byte[+2] == 1`,
`word[+0x48]`/`+0x4A` scale by `const/xmm1` into
`word[+0x34]`/`+0x36` - call-free.
Interior anchor `00403138` (the `divss`).

`004022D0` (27 B) is the fixed-record init: `[rcx]` = 0,
`[rcx+4]` = `[rcx+0xC]` = `0x80008`, `[rcx+0x10]` = `0x100` -
call-free.
Interior anchor `004022D2` (the `0x80008` store).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

These paragraphs cover only the edges that the `UQ-18` answer brings in by citing the readers it found. The
gate credits each layer name below for all of that layer's edges into this page; the rest are not dispositioned.

**Input — CLIENT.** `00197160`, the input-side body that gates on the "Enable mouse control camera" byte `+0xC35`,
reads this console field. The page relies only on that one read, not on the body's input-device callees.

**Script_VM_Native_Bridge — CLIENT.** Script verb `0x5A9` (`003504B0`) asks `0017D430` for the "100% Spawn Rare
Monster" byte `+0xC70` and returns it to the calling script. The page relies only on that call.

`004023D0` (186 B) is the order-insensitive key match `00402A40` runs while walking the `+0x98` chain: a record matches when its `+0x80`/`+0x82` word pair equals `rdx`'s `[0]`/`[2]` in either order AND its `+0x84`/`+0x86`/`+0x8C`/`+0x8E` quadruple equals `[rdx+4]`/`[rdx+6]`/`[rdx+0xC]`/`[rdx+0xE]` in either of two rotations - the six-word duplicate check that keeps the arm catalogue from admitting the same record twice

Interior anchor `004023E0` (function `004023D0`).
- **Gameplay — MECHANICAL (2 edges).** 2 calls from page-cited bodies into shared Gameplay plumbing (`BattleEncodedId_IsValidForClass` (00322C50)) - the helpers' general call surface, not a Gameplay relationship of this page's subjects.
- **Items_Equipment_Shops_License — CLIENT and SERVICE (13 edges).** 9 inbound (Items_Equipment_Shops_License bodies `InventoryBundleClass09_ApplyGilAndNestedItems` (002FD530), `Shop_CommitSaleItemAndGil` (00310870), `Shop_CommitPurchaseItemAndGil` (002FEEB0) call page-cited `BattleStats_GetByMappedBattleSlot` (00320AB0), `GameState_SetGil` (00254EE0)); 4 outbound (page-cited `Shop_CommitPurchaseItemAndGil` (002FEEB0), `Shop_CommitSaleItemAndGil` (00310870) call Items_Equipment_Shops_License bodies `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0), `BattleIdClassD_ResetPurchasedEntryAndNestedPrerequisiteState` (0030B180), `BattleIdClassD_RefreshPrerequisiteRuntimeFlags` (0030B270)). Substantive edges include `GameState_SetGil` (00254EE0) is called by `InventoryBundleClass09_ApplyGilAndNestedItems` (002FD530); `GameState_SetGil` (00254EE0) is called by `Shop_CommitSaleItemAndGil` (00310870); `GameState_SetGil` (00254EE0) is called by `Shop_CommitPurchaseItemAndGil` (002FEEB0); `GameState_SetGil` (00254EE0) is called by `InventoryEncodedGilClass0E_ApplyGilDelta` (002FD880); the remaining edges run through shared helpers the page cites.
- **Party — MECHANICAL (1 edge).** 1 Party-side calls into shared helper(s) the page cites (`BattleStats_GetByMappedBattleSlot` (00320AB0)) - the helpers' general call surface, not a Party relationship of this page's subjects.
- **Platform — SERVICE (1 edge).** 1 outbound (page-cited `001CCB20` call Platform bodies `005CC930`). Substantive edges include `001CCB20` calls `005CC930`.
- **UI — CLIENT and SERVICE (5 edges).** 1 inbound (UI bodies `002C7B10` call page-cited `0017FFD0`); 4 outbound (page-cited `002B7B80`, `00402A40` call UI bodies `0035D320`, `002B6DB0`, `004027D0`). Substantive edges include `002B7B80` calls `0035D320`; `002B7B80` calls `002B6DB0`; the remaining edges run through shared helpers the page cites.
