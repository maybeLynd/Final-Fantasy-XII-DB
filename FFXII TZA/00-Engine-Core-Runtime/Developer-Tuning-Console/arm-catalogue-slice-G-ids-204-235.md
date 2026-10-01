---
system: Arm catalogue — slice G, command ids 204–235
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

# Arm catalogue — slice G, command ids 204–235

> Slice G of the division in [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md).
> **32 command ids. It says nothing about the other 250.**

## 1. What the player sees

Nothing — a developer tool. Slice G contains the console's **numeric entry fields**: three commands
that are not sliders or switches at all but **multi-digit editors**, where a cursor selects one digit
of a number and the two buttons roll that digit 0–9 while the whole value is recomposed. One of them
counts in **sixties**.

It is also **the emptiest range in the table**: seventeen of its thirty-two ids do nothing.

## 2. Does the arm shape hold here? No — and half the slice is not there at all

| kind | count |
|---|---:|
| **unimplemented** | **17** |
| boolean toggle | 7 |
| **numeric entry editor** | **3** |
| float step | 3 |
| integer step / cycle | 2 |

**Seventeen unimplemented ids — 204, 209–216, 221–224, 232–235 — including a run of eight
consecutive.** No earlier slice exceeded five. Slice D had none.

The fifteen real arms occupy **nine distinct body sizes from 21 to 276 bytes**, and the three largest
are a kind of command no previous slice contains.

## 3. The catalogue

Row shape per the work order: **field · width · step magnitude · direction mechanism · bound.**
`b` = byte, `d` = dword field of the object at `rdi`.

| id | arm | kind | target | magnitude | direction mechanism | bound |
|---:|---|---|---|---|---|---|
| **204** | `001D4BFA` | **unimplemented** | — | — | — | — |
| 205 | `001D3EEF` | boolean toggle | `b+0xCF9` | — | `sil` gates the `bl`-clear path | 0/1; then one call |
| 206 | `001D3F1E` | boolean toggle | `b+0xCFA` | — | `sil` gates the `bl`-clear path | 0/1; then one call |
| 207 | `001D3F4D` | boolean toggle | `b+0xCFB` | — | `sil` gates the `bl`-clear path | 0/1; then one call |
| 208 | `001D3C99` | boolean toggle | `b+0xD07` | — | `sil` gates the `bl`-clear path | 0/1 |
| **209–216** | `001D4BFA` | **unimplemented** (8 consecutive) | — | — | — | — |
| 217 | `001D4006` | float step | via a getter/setter pair | 0.1 | signed pair, two constants | — |
| 218 | `001D3F7C` | float step | accessor `+0x4664` | 0.1 | one constant, `subss`/`addss` | — |
| 219 | `001D3FC1` | float step | accessor `+0x4668` | 0.1 | one constant, `subss`/`addss` | — |
| 220 | `001D4033` | int step via call | **no field** — passes ±1 to a call | 1 | two-button | — |
| **221–224** | `001D4BFA` | **unimplemented** (4 consecutive) | — | — | — | — |
| **225** | `001D405C` | **8-digit numeric entry** | digits `d+0xDB8`…`+0xDD4`, cursor `d+0xDD8`, value `d+0xDB4` | 1 | two-button, on the selected digit | **each digit mod 10** |
| **226** | `001D4155` | **8-digit numeric entry** | digits `d+0xDE4`…`+0xE00`, cursor `d+0xE04`, value `d+0xDE0` | 1 | two-button, on the selected digit | **each digit mod 10** |
| **227** | `001D424E` | **sexagesimal entry** | sub-field selected by `d+0xE14`, value `d+0xE0C` | 1 | two-button, on the selected sub-field | **each sub-field mod 60** |
| 228 | `001D3B1C` | boolean toggle | `b+0xE1C` | — | none | 0/1 |
| 229 | `001D3B31` | boolean toggle | `b+0xE1D` | — | none | 0/1 |
| 230 | `001D3B46` | boolean toggle | `b+0xE1E` | — | none | 0/1 |
| **231** | `001D4362` | int cycle | `d+0xE2C` | **1 or 10** — selected by `b+0xE30` | two-button | **wraps mod 311** |
| **232–235** | `001D4BFA` | **unimplemented** (4 consecutive) | — | — | — | — |

**15 real arms and 17 unimplemented.**

## 4. The console has numeric entry fields

Ids 225 and 226 are the same widget twice. A cursor selects one element of an **eight-dword digit
array**; the two buttons roll that digit; the digit is wrapped into 0–9; then the whole number is
recomposed by Horner's method and written to a separate field:

```asm
001D4060  movsxd rax, dword ptr [rdi + 0xdd8]      ; the digit cursor
001D4067  dec    dword ptr [rdi + rax*4 + 0xdb8]   ; bl  -> roll this digit down
001D407A  inc    dword ptr [rdi + rax*4 + 0xdb8]   ; sil -> roll it up
001D408A  add    dword ptr [rdi + rax*4 + 0xdb8], 0xa
          ... magic-divide by 10, subtract 10*quotient ...   ; digit = (digit + 10) mod 10
001D40C7  mov    eax, dword ptr [rdi + 0xdd4]      ; then recompose, most significant first
001D40CD  lea    ecx, [rax + rax*4]
001D40D0  add    ecx, ecx                          ; x10
001D40D8  add    ecx, dword ptr [rdi + 0xdd0]      ; + next digit
          ... six more times ...
001D414A  mov    dword ptr [rdi + 0xdb4], ecx      ; the composed value
```

**The `+10 then mod 10` is how a decrement below zero wraps to nine**, and it is the reason both
buttons can share one wrap step.

Each widget is a contiguous ten-dword block — **value, eight digits, cursor**:

```
0xDB4 value | 0xDB8 .. 0xDD4  eight digits | 0xDD8 cursor      (id 225)
0xDDC  -- not reached by this slice --
0xDE0 value | 0xDE4 .. 0xE00  eight digits | 0xE04 cursor      (id 226)
```

> `0xDDC` sits between the two widgets and **no id in this slice touches it. That is not evidence it
> is unused** — the same caution slice C discharged for slice B, and ids 236–293 are unread.

**Id 227 is the same idea in base 60.** Its selector at `rdi+0xE14` chooses one of three sub-fields,
and each is wrapped with `add 0x3B` (59) then a magic divide whose shift is `sar edx, 5` and whose
multiplier is `imul eax, edx, 0x3c` — **modulo 60, four times in the body.** A three-part field
counting in sixties composed into a single value at `rdi+0xE0C` is the shape of a **time or duration
entry**; that reading is an inference and is not traced to a consumer. **The modulus is the finding.**

## 5. Id 231 has a coarse/fine modifier

```asm
001D4362  mov    ebp, 1
001D4367  lea    edx, [rbp + 9]                    ; = 10
001D436E  cmp    byte ptr [rdi + 0xe30], 0
001D4377  cmovne eax, edx                          ; modifier set -> step 10 instead of 1
001D437A  sub    dword ptr [rdi + 0xe2c], eax
...
001D439B  add    eax, 0x137                        ; then wrap mod 311
```

**The step magnitude is not a property of the arm — it is read from a flag at `b+0xE30`.** Every
magnitude recorded anywhere else in this catalogue is a constant in the instruction stream; this one
is data, and a census of step constants cannot see it.

The wrap is **modulo 311** (`0x137`), verified by evaluating the 64-bit magic multiply
`0x34AE820ED114942B` with its `shr 6` against integer division across sampled values, **with a control
against 312, which fails.**

## 6. Call chain

```
console dispatch  001D1660   (arg1 rcx -> rdi, arg2 dl -> bl, arg3 r8b -> sil)
  -> table 001D4C1C + (id - 12)*4 -> + 0x00120000 -> the arm
     ids 205..207     : toggle a byte, then one call carrying the new value and an index
     ids 218, 219     : an accessor -> fields +0x4664, +0x4668
     id  217          : a getter/setter pair
     id  220          : passes -1 or +1 straight to a call; no field of its own
     ids 225..227,231 : widget state in the object at rdi (+0xDB4 .. +0xE30)
  -> jmp 001D4BFA   the shared tail, and the target of 17 of this slice's ids
```

## 7. Modding notes

- **Seventeen of these thirty-two ids do nothing**, including 209–216 in one run. A tool walking this
  id range by number will get silence more often than not, and that is shipped behaviour.
- **Ids 225–227 are widgets, not settings.** Writing the composed value at `+0xDB4`, `+0xDE0` or
  `+0xE0C` directly will be overwritten the next time its command is pressed, because the arm
  recomposes it from the digits every time.
- **The digit arrays are most-significant-first** at the highest offset.
- **Id 231's step depends on a flag** — the same command moves by 1 or 10 depending on `b+0xE30`, and
  nothing in the arm sets that flag.

## 8. What is not known

- [x] ~~**UQ-19.** **What the three numeric entry fields edit.** Two eight-digit decimals and one sexagesimal
      value, with cursors and wrap rules fully read, **and none traced to a consumer.**~~
      **ANSWERED 2026-09-16 (FABLE): NOTHING - and *none traced to a consumer* was not a gap in the tracing.** **What they are nominally for, from the game's own names:** id 225 *"Set clan point:"*, id 226 *"Set step count:"*, id 227 *"Set play time:"* - three save-file statistics. And the sexagesimal field is confirmed a clock by the renderer's own format string rather than by its shape: `001CFA41` loads `"%s%shour:%s%d%s, minute:%s%d%s, second:%s%d%s"` and `001CFA7B` `"%s%shour:%d, minute:%d, second:%d"`. **What they actually reach: nothing.** Exactly **three functions in the whole image** touch three or more of the console object's thirteen distinctive offsets (`+0xDB4`, `+0xDB8`, `+0xDD8`, `+0xDE0`, `+0xDE4`, `+0xE04`, `+0xE0C`, `+0xE14`, `+0xE1C`, `+0xE1D`, `+0xE1E`, `+0xE2C`, `+0xE30`) - the arm `001D1660` hits **13 of 13**, the menu renderer `001CD0E0` **12**, the constructor `001CCB20` **9**. **Nothing else among the 38,161 listed bodies touches even three.** Per offset, in the console range, the pattern is the same for all three values: the constructor initialises, the arm writes, the renderer reads, and there is no fourth party. **Nor do the arms hand the value out by a call.** The three arm bodies `001D405C`, `001D4155` and `001D424E` contain **no call instruction at all** - only internal jumps to the shared tail `001D4BFA` and to `001D42D1`. **So the widget composes a number and the renderer displays it back.** It never reaches clan points, the step counter or the play clock. This is the same shape as `UQ-270`'s *Convert PS2 Savedata*, whose arm is the shared do-nothing tail: **a command named for what it was meant to set, with the wiring absent in this build.** *Three bounds on the negative.* The signature test uses a **3-of-13 threshold**, so a consumer reading exactly one field and touching nothing else would score 1 and fall below it - though it would then have to sit outside `001C0000`–`001E0000` while holding the object, and the per-offset census finds no such reader in range. **An indexed read `[obj + reg]` with a computed displacement is invisible to a displacement census and is not excluded.** A block copy over the region *is* excluded: the sweep matched by overlapping byte ranges, and it caught the constructor's 8-byte `mov qword ptr [rdi + 0xDB0]` against `+0xDB4`.
- [x] ~~What sets `b+0xE30`, the coarse/fine modifier for id 231, and why its cycle is **311** long.~~ **Answered 2026-09-14
      (FABLE).**
      - **`+0xE30` is only ever 0.** A census of `+0xE30` accesses in `001C0000`–`001E0000` finds one store, the constructor's
        `mov [rdi+0xE30], al` at `001CCDDD`, with `eax` zeroed at `001CCD59` and unchanged through the intervening stores,
        and two reads, both in the arm. So the step is always 1, and the 10-step path is never taken in this image.
      - **The 311 is a table length.** Id 231 is *"Set scenario flag:"* ([names](console-command-names.md)). The index at
        `+0xE2C` is read by only one function besides the arm, the menu renderer `001CD0E0`. At `001CFAF3` it prints
        `"%s%s %d"` (`008FFAF0`) with `dword [01DFC0D0 + index × 4]`. That table holds exactly **311** ascending
        scenario-progress values: `0, 10, 13, 16, 18, 19, 20, …, 7200, 7250, 10000, 11000`, with index 310 = 11000 and
        index 311 already outside it (0). The wrap keeps the index inside the table.

      Which store applies the chosen value to the story flag was not traced here. The console arm itself only moves the
      index.
- [x] **UQ-20.** What occupies `d+0xDDC`, between the two digit widgets — **unreached, not known unused.** *(NO ADMISSIBLE SOURCE, reviewed and signed 2026-09-26 by OPUS; see the register row UQ-20.)*
      **Narrowed 2026-09-25 (FABLE, Claude Opus 5.5): a dword the constructor sets to 17, and nothing reads it.**
      - **The store.** The defaults builder `001CCB20` writes `mov qword ptr [rdi + 0xDDC], 0x11` (`001CCD7D`). That is
        one qword store doing two dword stores: `+0xDDC` = `0x11` (17), and `+0xDE0` = 0, which is id 226's composed value.
      - **No other access.** No other instruction in the three console bodies touches `+0xDDC`: the builder, the
        console arm `001D1660`, and the menu renderer `001CD0E0`, which reads `+0xDD8` and `+0xDE0` but not it. The
        receiver-checked census [`console_field_readers.py`](members/console_field_readers.py) finds no outside
        reader either.
      - **What stays open.** What the 17 means. Nothing in the image consults it, so it may be a leftover field of a
        widget whose use was removed. The argument-rooted blind spot applies.
- [x] ~~What ids 205–207 pass to their call, and what the byte trio `+0xCF9`/`+0xCFA`/`+0xCFB` selects.~~
      **Answered 2026-09-14 (FABLE): three sound-category mutes.** Labels `Music : `, `Voice: ` and `Sound Effect: `
      ([names](console-command-names.md)). Each arm flips its byte when a button is down, then always calls
      `001DBB00(category, byte)`: 205 → category **1**, 206 → **3**, 207 → **2** (`001D3F0F` / `001D3F3E` / `001D3F6D`).
      `001DBB00` goes through the audio registry `00210B30` to `002112D0`, which queues SEAD action type 3 through
      `007A45C0`: volume **1.0** when the byte is non-zero, **0.0** when it is zero, on volume layer element 1 of
      that category with fade 0. The constructor defaults all three to 1 (`001CCEE0`, `001CCEE9`). These are the same
      categories the player's volume options drive through settings commands `0x13`–`0x15`, so a mute here and the
      menu volume write the same layer, and the last write wins
      ([driver architecture](../../18-Audio/sqex-sd-sound-driver-architecture.md) §7, `G-3`). The retail image
      issues none of ids 205–207 ([the 282-command console](the-282-command-parameter-console.md) §7).
- [x] ~~What ids 217–219 reach through their accessors, and what id 220 steps — it has no field at all.~~
      **Completed 2026-09-14 (FABLE), second read the same day:**
      - **Id 217, *"3D Sound Behind Ratio"*.** `002DEBA0` / `002DF2A0` get and set the float at `0215EFD0` in ±0.1 steps. The
        audio-options initialiser `002DE360` sets it to `0.3` (`0091523C`). Its other readers are through the getter:
        `0031431A` and `00314324` in the world tick, `00363109`, and the menu renderer (`001CF54E`).
      - **Id 220, *"Extra BGM status"*.** `0017E7A0(±1)` steps the dword `01DF0010` (image value 1) and wraps it into 0..2.
        The labels at `01DF0018` are *"Not forced"*, *"Forced on"* and *"Forced off"*, returned by `0017E010`. The
        query `0017E490` answers 1 for "forced on", 0 for "forced off", and otherwise the byte at `01F7F4E8`.
        Six settings and UI sites call it (`0023D90C`, `0023DD8C`, `0023E7F5`, `002DDB8F`, `002DDCB2`, `002DE12C`).
        `01F7F4E8` has no RIP-relative writer, so its source was not traced.
      - Ids 218 and 219, from the first read: ids 218 and 219 go through `001C2F40`, an 8-byte getter returning `[01F81270]`, the
      `0x4670`-byte **`MultipleDebugDisplay`** (RTTI; [game application](../Application-Root/game-application.md)). They step its `+0x4664` / `+0x4668`
      floats, the last words of the object (`001D3F7C`–`001D3FC6`). Id 217's getter/setter pair and id 220's call were not re-read.

## 9. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The id → arm mapping for all 32 ids | dwords at `001D4C1C + (id−12)×4`, `+ 0x00120000`, re-derived from the image | 1 |
| Every target, magnitude, mechanism and bound | complete decode of each arm, bounded by **the next arm's start address** | 1 |
| 17 unimplemented ids | those entries resolve to `001D4BFA` | 1 |
| The digit-array layout and Horner recomposition | the eight `add ecx, [rdi + …]` operands and the `lea`/`add` ×10 chain, decoded in both arms | 1 |
| Digits wrap mod 10 | magic `0x66666667` with `sar edx, 2` evaluated against integer division | 1 |
| Id 227 wraps mod 60 | `sar edx, 5` with `imul eax, edx, 0x3c`, four times — **the shift is what fixes the divisor**; the magic `0x88888889` alone is consistent with 15, 30, 60 and 120 | 1 |
| Id 231 wraps mod 311 | 64-bit magic `0x34AE820ED114942B` with `shr 6` evaluated against `//311`, **with a failing control against 312** | 1 |
| Id 231's step is 1 or 10 from `b+0xE30` | `lea edx,[rbp+9]` and the `cmovne` on that byte | 1 |

**Re-derived, not copied:** 282 table entries, 227 distinct targets, 56 ids at `001D4BFA` — reproduced
from the image before any row was written. **`step` was re-derived per arm** rather than taken from
`Tools/work/repos-d2/console_arms.tsv`, whose author correctly labelled that column unverified.

**Controls.** The absence claim is *"no arm in this slice tunes a `02CBxxxx` global"*. The same
extractor reports `02CBxxxx` targets throughout slices B, C and D and reports `rdi` and accessor
targets here, so the zero is a measurement rather than a silent non-match. The two divisor claims each
carry their own control, above.

**Address review flags** (`001D4C1C` and every arm address) are dispositioned once for all slices in
[slice A](arm-catalogue-slice-A-ids-12-43.md) §8: the first is the dispatch table in `.text` after the
function, and switch arms are interior addresses of a function, not functions.

## 10. Related

- [the-282-command-parameter-console.md](the-282-command-parameter-console.md) — the frame
- [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md) — the division and its rules
- [arm-catalogue-slice-A-ids-12-43.md](arm-catalogue-slice-A-ids-12-43.md) — ids 12–43
- [arm-catalogue-slice-B-ids-44-75.md](arm-catalogue-slice-B-ids-44-75.md) — ids 44–75
- [arm-catalogue-slice-C-ids-76-107.md](arm-catalogue-slice-C-ids-76-107.md) — ids 76–107
- [arm-catalogue-slice-D-ids-108-139.md](arm-catalogue-slice-D-ids-108-139.md) — ids 108–139
- [arm-catalogue-slice-F-ids-172-203.md](arm-catalogue-slice-F-ids-172-203.md) — ids 172–203; the
  two-button reading of `bl`/`sil` established there is what makes this slice's widgets legible

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

**This slice broke a claim made about it and about the whole catalogue.** The third direction mechanism
was first reported as confined to slices D and E; **id 217 in this slice uses it**, making the true
distribution `D 25 · E 21 · G 1` — **rarer outside D and E than stated, not absent.** Slice G's float
count moved 2 → 3 in the same correction.

**Amended after delivery, by a second reader, recorded as an amendment rather than folded in:** ids
**225/226 are 8-digit decimal editors** (a digit cursor, mod-10 wrap, Horner recomposition), **227 is
an h:mm:ss editor** whose hours wrap modulo a **runtime** value, and **205–207 respond identically to
both directions** before pushing channels **1, 3, 2** — not menu order. That last is a third
independent retirement of "the direction flag".


*(Pass 22 adjacency, 2026-09-14: this slice's crossings are the shared dispatcher's, repeated
here because every slice cites `001D1660` — it calls the **presentation** materializers
`001D5120`/`001C7360`/`001C7520`, reaches **audio** `002DEBA0`/`001DBB00`, and fetches
through **resource** `002EEEE0`. The console lives on the render path and pulls its row content
through resource/audio helpers; the edges belong to the dispatcher, not to this slice's arms.)*

*(Pass 22 live-graph completion, 2026-09-15: the renderer `001CD0E0` calls
`Platform_Online_Achievements` `003166F0` (1 edge) — the menu draw path can poke the
achievement layer like every other console renderer leg.)*


## Interior citation — frontier hub `0017E490` (2026-09-18, SWE2-EC7)

`0017E490` — 33 B, 6 A-measured callers; the mode-remap leaf. Interior verified:
`[01DF0010]` minus one selects — `0` returns 1, `1` returns 0, anything else returns the
`01F7F4E8` byte verbatim ([`0017E496`–`0017E4A0`](../../_index/ADDRESS-INDEX.md)). A
three-way state fold: two fixed answers, the third delegated to a published byte.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **Platform — SERVICE (1 edge).** 1 outbound (page-cited `001CCB20` call Platform bodies `005CC930`). Substantive edges include `001CCB20` calls `005CC930`.
- **PlatformOnlineAchievements — CLIENT and SERVICE (4 edges).** 3 inbound (PlatformOnlineAchievements bodies `00316760`, `00316A50`, `00315E90` call page-cited `003166F0`); 1 outbound (page-cited `001CD0E0` call PlatformOnlineAchievements bodies `003166F0`). Substantive edges include `001CD0E0` calls `003166F0`; `003166F0` is called by `00316760`; `003166F0` is called by `00316A50`; `003166F0` is called by `00315E90`.
- **Save_Load_Settings — CLIENT (1 edge).** 1 inbound (Save_Load_Settings bodies `SaveImage_FinalizeHeaderAndChecksum` (00583D60) call page-cited `003166F0`). Substantive edges include `003166F0` is called by `SaveImage_FinalizeHeaderAndChecksum` (00583D60).
- **WorldAreaField — CLIENT and SERVICE (3 edges).** 1 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020) call page-cited `002DEBA0`); 2 outbound (page-cited `001CD0E0` call WorldAreaField bodies `WorldTransition_GetTransitionFieldId` (00314910), `FieldData_GetVariable0` (00265270)). Substantive edges include `001CD0E0` calls `WorldTransition_GetTransitionFieldId` (00314910); `001CD0E0` calls `FieldData_GetVariable0` (00265270); `002DEBA0` is called by `World_UpdateSimulationTick` (00314020).
