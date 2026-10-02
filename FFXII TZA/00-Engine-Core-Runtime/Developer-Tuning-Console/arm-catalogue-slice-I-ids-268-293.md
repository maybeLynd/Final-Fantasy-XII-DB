---
system: Arm catalogue — slice I, command ids 268–293
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
    verified: 2 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
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

# Arm catalogue — slice I, command ids 268–293

> Slice I of the division in [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md).
> **26 command ids — the last and shortest slice. It says nothing about the other 256.**

## 1. What the player sees

Nothing — a developer tool. Slice I is where the console stops touching its own memory and starts
**driving an engine object through a property interface**: fifteen of its twenty-two live commands
dereference one shared pointer, read a field, and hand the new value to a setter **along with a
property number**.

## 2. Does the arm shape hold here? No — these commands do not write anything themselves

| kind | count |
|---|---:|
| **property write through a setter** | **13** |
| boolean toggle on a local field | 4 |
| integer step / cycle on a local field | 4 |
| step through a getter/setter pair | 3 |
| **unimplemented** | **4** (282, 286, 289, 290) |

**22 real arms.** Almost none of them stores to the object it is editing. They compute a value and
call, which makes this the only slice whose commands could be replayed without touching memory at all.

## 3. The property id is the field's dword index

This is the slice's main result. Every one of these arms loads the pointer at `01F82D20`, reads a
field of the object behind it, and calls a three-argument setter — `rcx` the object, `edx` a property
number, `r8d` the value:

```asm
001D4B49  mov    rcx, qword ptr [01F82D20]
001D4B52  cmp    dword ptr [rcx + 0x34], 1     ; the field
001D4B56  lea    edx, [rsi + 0xd]              ; the property number, rsi = 0  -> 13
001D4B59  setne  sil                           ; value = (field != 1)
001D4B60  call   <setter>                      ; (object, 13, value)
```

**`0x34 / 4 = 13`.** Across every arm in this slice where both the field offset and the property
number are visible in the instruction stream:

| field | property | field / 4 | id |
|---|---:|---:|---|
| `+0x0C` | 3 | 3 | 281 (second write) |
| `+0x10` | 4 | 4 | 272 |
| `+0x14` | 5 | 5 | 273 |
| `+0x18` | 6 | 6 | 274 |
| `+0x1C` | 7 | 7 | 275 |
| `+0x24` | 9 | 9 | 278 |
| `+0x28` | 10 | 10 | 279 |
| `+0x30` | 12 | 12 | 280 |
| `+0x34` | 13 | 13 | 281 |
| `+0x3C` | 15 | 15 | 276 |
| `+0x44` | 17 | 17 | 284 |
| `+0x48` | 18 | 18 | 285 |
| `+0x58` | 22 | 22 | 271 |

**Thirteen pairs, thirteen agreements, no disagreement.** The count is of pairs where *both* halves are
readable; arms whose field read uses an addressing form this extraction did not capture were resolved
by hand rather than left in the denominator, because **a ratio that mixes "contradicts" with "not
measured" is not a measurement.**

> **So the object behind `01F82D20` is addressed as a property bag whose numbering is just its dword
> layout.** Slice D established that this pointer is dereferenced by 18 arms and never nudged; slice I
> holds fifteen of them and says what they do with it.

**The gaps in that table — properties 11, 14, 16, 19, 20, 21 — are unreached, not absent.** Slice H
(ids 236–267) is unread, and it is precisely the range that could hold them.

> **Tested by [slice H](arm-catalogue-slice-H-ids-236-267.md) §8, and the prediction failed on its
> locations while confirming its rule.** H holds none of the six. Properties **14** and **16** are
> reached from slices **E** and **D** — both extracted *before* this rule existed — and both obey
> `offset/4`, which is two slices agreeing on a numbering rule neither derived from the other. The
> census over all 282 ids stands at **14 agreements, 0 disagreements**. Properties **11, 19, 20 and 21
> are reached by no arm anywhere**: they are numeric settings, and §6 shows the console cycles
> enumerations.

## 4. Fourteen arms in the table jump into another arm's body

Ids 276 and 280 are 21 and 18 bytes — far too short to contain a setter call. They set up the field
comparison and the property number, then:

```asm
001D4A38  jmp   0x1d4b59        ; id 276 -> into the middle of id 281's arm
001D4B47  jmp   0x1d4b59        ; id 280 -> the same place
```

**They enter id 281's body partway in**: the `setne`, the value move and the call. Measured over all
227 arms with the same rule — a `jmp` that is not the common tail, not inside the arm's own extent,
and not to another arm's *start*:

```
14 of 227 arms end by jumping into another arm's interior
21 jump SITES, because ids 177 and 180 carry three each and 190, 192, 279 two each
```

**Both numbers are right and they count different things** — arms, and jumps. A whole-table pass and
this slice's pass disagreed until the populations were named, which is usually what a disagreement
between two careful counts turns out to be.

**And `001D4B59` is not a shared tail — it is id 281 entered at three different offsets** (`4B59`
compute the flag and call, `4B60` call only, `4B65` do the property-3 call and exit), by **nine ids
across slices D, E and I**. This document originally generalised "a second shared tail" from the two
examples in front of it. **An arm with three entry points is not a tail**, and the corrected fact is
the more useful one: it means a single arm body is the implementation of nine commands at three
different granularities.

> **This is a limit of the model every slice in this catalogue has used.** Bounding an arm at the next
> arm's start address extracts the right *instructions* — but for these fourteen the *behaviour*
> continues inside a neighbour. It is the same lesson as the `001D4BFA` truncation one level further
> in: **the first stop rule was "do not stop at the shared tail"; this one is "the arm's extent is not
> always the arm's behaviour."**

Both arms here were caught because their byte counts were implausible for what they had to do. That is
the check worth carrying: **a body too small for its job is a jump you have not followed.**

## 5. The catalogue

`b` = byte, `d` = dword field of the object at `rdi`; `*ptr+N` = field `N` of the object behind
`01F82D20`, with its property number in brackets.

| id | arm | kind | target | direction mechanism | bound |
|---:|---|---|---|---|---|
| 268 | `001D4731` | int step via a getter/setter pair | mirrors to `d+0x10C4` | `bl` ±1 | — |
| 269 | `001D47FD` | int step via a getter/setter pair | mirrors to `d+0x10CC` | `bl` ±1 | — |
| 270 | `001D4832` | int step via a getter/setter pair | mirrors to `d+0x10D0` | `bl` ±1 | — |
| 271 | `001D47B5` | property write | `*ptr+0x58` **[22]** | `sete` — value becomes `field == 0` | 0/1 |
| 272 | `001D4867` | property write | `*ptr+0x10` **[4]** | `bl` ±1 | **clamped `[0, 100]`** |
| 273 | `001D48AD` | property write | `*ptr+0x14` **[5]** | `bl` ±1 | **wraps, 3 states** |
| 274 | `001D4972` | property write | `*ptr+0x18` **[6]** | `bl` ±1 | bounded at 4 |
| 275 | `001D49C1` | property write | `*ptr+0x1C` **[7]** | `bl` ±1 | bounded at 2 |
| 276 | `001D4A28` | property write | `*ptr+0x3C` **[15]** | `setne` — `field != 1` | 0/1; **tail shared with 281** |
| 277 | `001D4A3D` | property write, different gateway | `*ptr+0x20` | `setne` | 0/1; then two further calls |
| 278 | `001D4A8A` | property write | `*ptr+0x24` **[9]** | `bl` | bounded at 1 |
| 279 | `001D4B03` | property write ×2 | `*ptr+0x28` **[10]**, also property **[8]** | `bl` ±1 | bounded at 2 |
| 280 | `001D4B37` | property write | `*ptr+0x30` **[12]** | `setne` | 0/1; **tail shared with 281** |
| 281 | `001D4B49` | property write ×2 | `*ptr+0x34` **[13]**, then property **[3]** = 3 | `setne` | 0/1 |
| **282** | `001D4BFA` | **unimplemented** | — | — | — |
| 283 | `001D4B7D` | int cycle | `*ptr+0x0C` | `bl` ±1 | bounded at 2 |
| 284 | `001D4907` | property write | `*ptr+0x44` **[17]** | `setne` | 0/1; then a vtable call |
| 285 | `001D494F` | property write | `*ptr+0x48` **[18]** | `setne` | 0/1 |
| **286** | `001D4BFA` | **unimplemented** | — | — | — |
| 287 | `001D47EA` | boolean toggle | global `01E02801` | none | 0/1 |
| 288 | `001D479B` | int step | `d+0x10D4` | two-button | **none — unbounded** |
| **289** | `001D4BFA` | **unimplemented** | — | — | — |
| **290** | `001D4BFA` | **unimplemented** | — | — | — |
| 291 | `001D4BB7` | int cycle | `d+0x10DC` | two-button | **wraps, 4 states** |
| 292 | `001D4BEA` | boolean toggle | `b+0x10E0` | none | 0/1 |
| 293 | `001D3AD0` | boolean toggle | `b+0xC3D` | none | 0/1 |

**22 real arms and 4 unimplemented** (282, 286, 289, 290).

## 6. The object is identified: it is the GameSetting.ini config

**Added 2026-09-03, after the catalogue rows above were written.** The object behind `01F82D20` is the
game's settings block, and it was **already documented** in
[19-Save-Load-Settings/Game-Settings-Config](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
— `0x65C` bytes, 31 dword slots, pointer written exactly once at `00798261`, constructed by
`GameSettingConfig_InitDefaultsAndPath` (`001DE050`). **This slice re-derived that independently and
agrees with it**, including the reference count: 157 instructions reference `01F82D20`, 156 reads and
one write.

**The setter proves the numbering rule from the callee side.** It is four instructions:

```asm
001DF340  movsxd rax, edx            ; the property number
001DF343  mov    [rcx + rax*4], r8d  ; obj->dword[n] = value
001DF347  xor    eax, eax
001DF349  ret
```

**`offset / 4` is not a convention inferred from call sites — it is the whole body of the function.**

**No vtable.** `GameSettingConfig_InitDefaultsAndPath` writes `[rcx+0x658]` and `[rcx+0x44C]` first
and never stores a pointer at `[rcx]`, so the object is plain data. Naming it required the call-site
route; there was no RTTI shortcut.

### What each command in this slice actually sets

Value labels come from the 31 × 9 `char*` table at `01DFD150` documented in that same document.

| id | property | setting, from its value labels | this slice's measured bound | labels |
|---:|---:|---|---|---:|
| 272 | 4 | numeric (no labels) | clamped `[0, 100]` | — |
| 273 | 5 | `Off` / `On` / `Adaptive` | wraps, **3** states | **3** |
| 274 | 6 | `1` / `2` / `4` / `8` / `16` | bounded at **4** | **5** |
| 275 | 7 | `Low` / `Medium` / `High` | bounded at **2** | **3** |
| 278 | 9 | `FXAA` / `SMAA_1x` | bounded at **1** | **2** |
| 279 | 10 | `Off` / `HalfResolution` / `FullResolution` | bounded at **2** | **3** |
| 280 | 12 | `Off` / `On` | 0/1 | 2 |
| 281 | 13 | `Off` / `On` | 0/1 | 2 |
| 276 | 15 | `Off` / `On` | 0/1 | 2 |
| 284 | 17 | `DoubleBuffer` / `TripleBuffer` | 0/1 | 2 |
| 285 | 18 | `30` / `60` | 0/1 | 2 |
| 271 | 22 | `Off` / `On` | 0/1 | 2 |
| 283 | 3 | `VQ_LOW` / `VQ_MEDIUM` / `VQ_HIGH` / `VQ_CUSTOM` | bounded at **2** | **4** |

> **Every bound in this slice was read from arm instructions before the label table was found, and
> every one of them matches the label count.** Two instruments that share no code and no method agree
> on the cardinality of eleven settings.

**The one apparent exception is the finding, not a defect.** Id 283 cycles the quality preset over
**three** values where the table has four — it cannot reach `VQ_CUSTOM`. And id 281, having toggled an
individual setting, **writes exactly `3` to property 3**: selecting Custom is what *happens to you*
when you change an option, never something the preset cycler offers. That is how a PC graphics menu
behaves, and the two halves were measured in different arms.

### What the console does and does not expose

Of the 31 settings, **18 are enumerations and 13 are numeric.** Across all 282 ids — the arm census in
[slice H](arm-catalogue-slice-H-ids-236-267.md) — the console reaches **17** properties: sixteen of the
eighteen enumerations, plus numeric property 4.

**The two enumerations it never touches are property 0, the language (`jp`/`en`/`fr`/`de`/`it`/`es`/
`kr`/`ch`/`cn`), and property 25, the confirm button (`Circle`/`Cross`)** — precisely the two settings
in the block that are not video options.

## 7. Data structures and formulas

```c
/* the property-write family */
v = obj->field[N];                    /* obj = *(void**)0x01F82D20 */
new = <toggle or step of v>;
SetProperty(obj, N/4, new);           /* the property number IS the dword index */

/* the boolean form, which is most of them */
SetProperty(obj, N/4, (obj->field[N] != 1));

/* id 272, the one clamped step */
new = direction ? max(v - 1, 0) : min(v + 1, 100);
```

**Ids 268–270 use their own getter/setter pairs**, not the shared setter, and additionally mirror the
value into a field of the console's own object — a store that is immediately overwritten by the
updated value, so the mirror holds the *new* number, not the old.

## 8. Modding notes

- **`01F82D20` is the console's widest lever.** One pointer, an object addressed by dword index, and
  a setter that takes that index — a hook on the setter sees every one of these commands with its
  property number attached.
- **Most of slice I never writes memory directly.** Patching the object's fields will be undone or
  ignored, because the arms call the setter and the setter is what the engine reacts to.
- **Ids 276 and 280 have no tail of their own** — they run into id 281's. Anything that relocates or
  patches arm 281 breaks all three.
- **Id 288 is unbounded** — it steps a counter with no limit in either direction.
- **Four ids in this range do nothing** — 282, 286, 289, 290.

## 9. What is not known

- [x] ~~What the object behind `01F82D20` is.~~ **Answered — see §6.** It is the `GameSetting.ini`
      config object, already documented in
      [19-Save-Load-Settings](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md);
      this slice re-derived it independently and agrees. Thirteen of the properties this slice reaches
      are now named from their value labels.
- [x] ~~What properties 11, 14, 16, 19, 20 and 21 are — unreached by this slice, not known absent.~~
      **Tested by [slice H](arm-catalogue-slice-H-ids-236-267.md) §8 and the prediction failed on its
      locations while confirming its rule:** H holds none of them; 14 and 16 are reached from slices E
      and D and obey `offset/4`; **11, 19, 20 and 21 are reached by no arm anywhere.** All four are
      numeric settings with no value labels — the console cycles enumerations, and those are not.
- [x] ~~What the second gateway used by id 277 does differently from the shared setter.~~ **Answered 2026-09-14 (FABLE): it
      cycles MSAA modes and skips the ones the GPU does not support.** Id 277 is *"Anti-aliasing"*, and `*ptr+0x20` is
      setting 8, **MSAA**.
      - **The shared setter** `001DF340(cfg, index, value)` is one store: `setting[index] = value`.
      - **The gateway `001DF2C0(cfg, current, up)`** steps `current` by one, modulo 5, in the requested direction
        (`0xCCCCCCCD` divide), then keeps stepping while the mode's bit is clear in `cfg + 0x44C`. It stores the mode it
        lands on at `+0x20` and returns it.
      - **The mask is a capability probe.** `00628690` (called from `00625E7C`) asks the D3D11 device, vtable slot 30
        (`CheckMultisampleQualityLevels`), about `DXGI_FORMAT_R8G8B8A8_UNORM` (`0x1C`) for sample counts 2 to 32. Through
        `0017D9C0` → `001DF2B0` (`bts`) it sets bit 1 for 2×, bit 2 for 4×, bit 3 for 8×, bit 4 when 8× reports more
        than 16 quality levels, and bit 5 for 16×. Bit 0 is the constructor's `1`, so "off" is always available.
      - **Bit 5 cannot be selected.** The cycle is modulo 5, so the 16× mode is probed but can never be chosen.
      - **The two further calls.** The arm stores `result != 0` at `[01F7F598]+0xDBA`, then maps the mode through the
        sample-count table `00900EE8` = {1, 2, 4, 8, 9} (`001DE570`). It hands that count to `00189520`, which stores it
        at `+0xDC8` and raises the dirty byte `+1`.

      What the value `9` for mode 4 selects in the renderer was not read.
- [x] ~~What global `01E02801` (id 287) enables.~~ **Answered 2026-09-14 (FABLE): frame skipping** (label *"FrameSkip Enabled:"*,
      [names](console-command-names.md)). The byte is `1` in the image. Besides the console (`001D47EA` / `001D47F1`) and the menu
      renderer (`001CD60F`), its one reader is `001E05F0`:
      - **at 0:** it stores `-1.0` (`009010A8`) at `01DFDDF8` and `0.0` at `01F82D28`, and returns 0 (never skip);
      - **otherwise:** it runs `001E03F0`, asks `00187540` on the `01F7F598` singleton, calls `001E04F0`, and returns whether
        the accumulated double at `01F82D28` has reached the returned threshold (`comisd` / `setae`, `001E063A`–`001E0648`).

      So clearing the byte turns the skip decision off and resets its accumulator. Who calls `001E05F0` was not traced here.
- [x] **UQ-21.** Whether the fourteen cross-arm jumps are shared tails by design or an artefact of the compiler
      folding identical epilogues. *Answered 2026-09-26 (OPUS): the compiler's tail merging - all 21 jumps land at the maximal common suffix, 8 mid-expression (arguments or flags live across the jump); see the register row UQ-21 and `_index/candidates/uq21-opus-cross-arm-jumps/`.*

## 10. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The id → arm mapping for all 26 ids | dwords at `001D4C1C + (id−12)×4`, `+ 0x00120000`, re-derived from the image | 1 |
| Every target, mechanism and bound | complete decode of each arm, bounded by the next arm's start, **and following each terminal `jmp`** | 1 |
| Property number = field offset / 4 | 13 arms where both halves are readable; **13 agreements, 0 disagreements** | 1 |
| 14 of 227 arms jump into another arm's interior | jump-target classification over all 227 arms | 1 |
| 4 unimplemented ids | those entries resolve to `001D4BFA` | 1 |

**Re-derived, not copied:** 282 table entries, 227 distinct targets, 56 ids at `001D4BFA`. **`step` was
re-derived per arm** rather than taken from `Tools/work/repos-d2/console_arms.tsv`, whose author
correctly labelled that column unverified.

**Controls.** The absence claim is *"no arm in this slice steps a float"*. The same extractor reports
float steps throughout slices B, C, D, F and G and reports the integer and property forms here, so the
zero is a measurement rather than a silent non-match. The property-number rule was tested by pairing
each setter call with the field read live at that call, **not by matching the two lists in aggregate**,
which would have agreed for the wrong reason.

**Address review flags** (`001D4C1C` and every arm address) are dispositioned once for all slices in
[slice A](arm-catalogue-slice-A-ids-12-43.md) §8: the first is the dispatch table in `.text` after the
function, and switch arms are interior addresses of a function, not functions.

## 11. Related

- [the-282-command-parameter-console.md](the-282-command-parameter-console.md) — the frame
- [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md) — the division and its rules
- [arm-catalogue-slice-A-ids-12-43.md](arm-catalogue-slice-A-ids-12-43.md) — ids 12–43
- [arm-catalogue-slice-B-ids-44-75.md](arm-catalogue-slice-B-ids-44-75.md) — ids 44–75
- [arm-catalogue-slice-C-ids-76-107.md](arm-catalogue-slice-C-ids-76-107.md) — ids 76–107
- [arm-catalogue-slice-D-ids-108-139.md](arm-catalogue-slice-D-ids-108-139.md) — ids 108–139;
  **established that `01F82D20` is a pointer and never nudged — this slice says what its 18 arms do**
- [arm-catalogue-slice-F-ids-172-203.md](arm-catalogue-slice-F-ids-172-203.md) — ids 172–203
- [arm-catalogue-slice-G-ids-204-235.md](arm-catalogue-slice-G-ids-204-235.md) — ids 204–235

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

**This slice's central rule was later proved from the other end, by reading the callee.** The setter at
`001DF340` is four instructions:

```asm
movsxd rax, edx
mov    [rcx + rax*4], r8d
xor    eax, eax
ret
```

> **`offset/4 == property` is not a convention inferred from 14 call sites — it is the entire body of
> the function.** A 14-agreement correlation became a definition.

**One claim made here was retracted.** `001D4B59` was reported as a *second shared tail*; it is **id
281 "Glare" entered at three different offsets** (`4B59`, `4B60`, `4B65`), used by nine ids across D,
E and I. **An arm with three entry points is not a tail** — and it means one body implements nine
commands at three granularities.

**A method note kept with the finding:** the property rule's first extraction reported "6 of 11", and
**five of the five failures were an addressing form the extractor had not captured, none contradicting
the rule.** *A denominator that mixes "contradicts" with "not measured" is not a measurement.*


*(Pass 22 adjacency, 2026-09-14: `001DF340` — the arm helper this slice cites — is called by the
**presentation** dispatcher `001D1660`, **online** `007A0C60` and **platform** `001DD170` (3
edges). A helper consumed by platform init and the render path alike is shared plumbing; the
callers cross layers, the helper does not change owners.)*

*(Pass 22 live-graph completion, 2026-09-15: the dispatcher `001D1660` this slice cites calls
`Audio` `002DEBA0`/`001DBB00` and `Resource` `002EEEE0` (3 edges) — the shared fetch legs,
same as the sibling slices.)*
## SWE2-EC7-32 update (2026-09-18) — `001DE570` mod-5 sample-count lookup

`001DE570` (33 B) is the count reader the slice table names:
`[rcx+0x20]` reduced mod 5 (the `0xCCCCCCCD` magic divide, `shr 2`)
indexes the `00900EE8` dword table — `{1, 2, 4, 8, 9}` as the
page already lists — and returns the entry. Interior anchor
`001DE58C` (the `00900EE8` table read).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **Audio — CLIENT and SERVICE (5 edges).** 1 inbound (Audio bodies `00362F70` call page-cited `002DEBA0`); 4 outbound (page-cited `001D1660`, `001DBB00` call Audio bodies `001DBB00`, `002DEBA0`, `002112D0`). Substantive edges include `001D1660` calls `001DBB00`; `001D1660` calls `002DEBA0`; `001DBB00` calls `002112D0`; `002DEBA0` is called by `00362F70`; the remaining edges run through shared helpers the page cites.
- **Resource — SERVICE (3 edges).** 3 outbound (page-cited `002EEEE0`, `001D1660` call Resource bodies `002EEEE0`, `002DF8E0`, `002DF980`). Substantive edges include `001D1660` calls `002EEEE0`; `002EEEE0` calls `002DF8E0`; `002EEEE0` calls `002DF980`.
- **WorldAreaField — CLIENT (1 edge).** 1 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020) call page-cited `002DEBA0`). Substantive edges include `002DEBA0` is called by `World_UpdateSimulationTick` (00314020).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-arm-catalogue-slice-i-ids-268-293-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0017D9C0` | 14 B | tail-jumps `001DF2B0(qword 01F82D20, ecx)` | `0017D9C2`, `0017D9C9` |
| `001DF2B0` | 16 B | sets bit `edx` (modulo 32, via `bts`) of dword `+0x44C` of `rcx` and stores the dword back | `001DF2B6`, `001DF2B9` |
| `001E04F0` | 83 B | calls `0017FE30()` and picks the double 0.01666666667 (`009010A0`) when the unsigned result is a multiple of 10, otherwise 0.01668333333 (`00900378`); returns the signed dword result of `00184950()` converted to double and multiplied by the picked value | `001E04F9`, `001E0511`, `001E0520`, `001E0528`, `001E0535` |
