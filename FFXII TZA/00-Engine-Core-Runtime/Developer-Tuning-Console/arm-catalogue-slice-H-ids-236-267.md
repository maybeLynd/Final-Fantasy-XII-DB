---
system: Arm catalogue — slice H, command ids 236–267
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
    verified: 7 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
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

# Arm catalogue — slice H, command ids 236–267

> Slice H of the division in [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md).
> **This document describes 32 command ids.** Numbers taken over the whole table say so and give the
> population. Parameter names come from the label table established in
> [slice E](arm-catalogue-slice-E-ids-140-171.md) §4.

## 1. What the player sees

Nothing directly — but this is the slice where a developer looked at **a character**. Fourteen rows
show the selected party member's stats and the game's running counters (battles fought, spells cast,
monsters killed, current LP), and a second group edits those counters, the steal/poach/drop success
behaviour, master volume, and the display and adapter settings.

**Fifteen of those display rows no longer respond to input** (§4), so what a developer saw here in the
shipping build is mostly a read-out.

## 2. Does the arm shape hold here? No — and this slice is barely made of steppers at all

Slice A was counters, B and C floats, D and E floats with a two-constant direction, F getter/setter
pairs, G digit editors. **H has exactly one conventional float step in 32 ids.** Its census:

**18 do-nothing · 8 counter/cycle arms · 5 call arms · 1 float step.**

Four shapes here are not in any earlier slice, and each would be mis-typed by an extractor built for
the last one:

- **The step magnitude is not constant.** Ids 238–242 step by **1 or 10**, chosen at runtime by a
  modifier flag (§5). Every row in every previous slice had a fixed magnitude; **a row that records
  one number for these has recorded half the arm.**
- **The "Enable 100 % successful …" rows are not toggles.** They are cycles of **4, 3 and 5 states**
  over a range that includes `−1` (§6).
- **Id 266 is a nested cursor**, not a stepper: it walks monitors within an adapter and carries into
  the adapter index (§7).
- **Id 260 writes one value to three destinations** — one row, three audio channels.

## 3. The catalogue

Row shape per the work order: **field · width · step magnitude · direction mechanism · bound**, with
the parameter name from the label table. `b` = byte, `d` = dword, `f32` = 4-byte float. `rdi` offsets
are fields of the console context object.

| id | arm | parameter | field | w | magnitude | direction mechanism | bound |
|---:|---|---|---|---|---|---|---|
| 236 | `001D4BFA` | Count of killed monsters | — | — | — | **do-nothing** | — |
| 237 | `001D4BFA` | Current LP | — | — | — | **do-nothing** | — |
| 238 | `001D43C9` | Set count of battle | `rdi+0xE34` | d | **1 or 10** | `test bl`/`test sil`, **magnitude from the flag at `rdi+0xE38`** | **floor 0** |
| 239 | `001D4416` | Set count of magic | `rdi+0xE3C` | d | **1 or 10** | same, flag `rdi+0xE40` | **floor 0** |
| 240 | `001D4463` | Set count of tech | `rdi+0xE44` | d | **1 or 10** | same, flag `rdi+0xE48` | **floor 0** |
| 241 | `001D44B0` | Set count of steal | `rdi+0xE4C` | d | **1 or 10** | same, flag `rdi+0xE50` | **floor 0** |
| 242 | `001D44FD` | Set count of killed monsters | `rdi+0xE54` | d | **1 or 10** | same, flag `rdi+0xE58` | **floor 0** |
| 243 | `001D3B5B` | Enable 100% successful steal | `rdi+0xE5C` | d | 1 | signed mod-4 down, `inc` up | **cycles `−1,0,1,2`** |
| 244 | `001D3BA2` | Enable 100% successful poach | `rdi+0xE60` | d | 1 | signed mod-3 down, `inc` up | **cycles `−1,0,1`** |
| 245 | `001D3BEE` | Enable 100% successful drop | `rdi+0xE64` | d | 1 | signed mod-5 down, `inc` up | **cycles `−1,0,1,2,3`** |
| 246–258 | `001D4BFA` | Chara Name, Level, HP, MP, ATPOW, DFPOW, WDFPOW, EVPOW, MEVPOW, STR, MGC, WPR, SPD | — | — | — | **do-nothing** (still displayed, §4) | — |
| 259 | `001D4BFA` | Reset Parameter: Press Circle | — | — | — | **do-nothing** | — |
| 260 | `001D4590` | Master Volume Ratio | `rdi+0x10B8` | f32 | 0.01 | `subss`/`addss`, one constant | **none** |
| 261 | `001D4BFA` | Set Leather Count to 2: Press Circle | — | — | — | **do-nothing** | — |
| 262 | `001D4BFA` | Print Memory stats: Press Circle | — | — | — | **do-nothing** | — |
| 263 | `001D45E9` | Game Window Mode | `rdi+0x10BC`, mirrored from `[01F82D20]+8` | d | 1 | `test bl` only | **mod 3** |
| 264 | `001D46DD` | Game Display Resolution | via `00182E10` | — | — | `test bl` selects argument `0` or `1` | **only acts when window mode ≤ 1** |
| 265 | `001D4712` | Game Monitor | `+0x60` of an accessor's object | d | — | **neither direction is read** (§7) | — |
| 266 | `001D464B` | System Adapter | `+0x48` / `+0x60` of the same object | d | 1 | `test bl`, **carrying between two fields** | bounded by a runtime count |
| 267 | `001D4766` | Mouse Control Vertical Camera Speed | `+0x1EC`-style getter/setter via `0032E010`/`0032E030` | d | 1 | `test bl`, integer `lea ±1` | — |

**Only one arm in this slice is a plain float step (id 260), and it has no bound** — master volume can
be driven below zero and above one from the menu.

## 4. The eighteen emptied rows are the read-out block — none of them is blank

Applying the two-table cross-tab from [slice E](arm-catalogue-slice-E-ids-140-171.md) §5 to this
slice's 18 do-nothing ids:

| how the row draws | ids | count |
|---|---|---:|
| **still shows a live value** | 236, 237, 246–258 | **15** |
| label only | 259, 261, 262 | 3 |
| `"  (EMPTY)  "` | — | **0** |

**Every display row survived; only the three "Press Circle" buttons went inert.** The twelve stats at
247–258 are drawn from the real stat array — the renderer reads
`[r15 + (id−247) + 12·selected]·4 + 0xE68`, which is also the fourth of the checks that fixed the
label table's id alignment.

> **This is the clearest instance in the catalogue of "do-nothing" meaning three different things.**
> A slice-local count of 18 unimplemented arms would describe a menu page of dead rows. What is
> actually there is a **working character inspector** with its editing removed.

## 5. The step magnitude is a runtime choice — ids 238–242

```asm
001D43C9  mov   ebp, 1
001D43CE  lea   edx, [rbp + 9]           ; 10
001D43D1  test  bl, bl                   ; down?
001D43D5  cmp   byte ptr [rdi + 0xE38], 0    ; the modifier flag
001D43DE  cmovne eax, edx                ; flag set -> step 10, else 1
001D43E1  sub   dword ptr [rdi + 0xE34], eax
...
001D43FC  cmp   dword ptr [rdi + 0xE34], 0
001D4403  jge   0x1d4bfa
001D440B  mov   dword ptr [rdi + 0xE34], esi   ; floor at 0
```

Five identical arms over five **stride-8 value/flag pairs**: `0xE34`/`0xE38`, `0xE3C`/`0xE40`,
`0xE44`/`0xE48`, `0xE4C`/`0xE50`, `0xE54`/`0xE58`. Each has its **own** modifier flag rather than
sharing one, so the coarse/fine choice is per-counter state, not a global shift key.

> **"Magnitude 1" and "magnitude 10" are both wrong for these rows; the honest cell is `1 or 10` plus
> where the choice comes from.** The row shape's insistence on recording the *mechanism* rather than
> the value is what makes that expressible.

The floor at 0 is real and one-sided — there is no ceiling.

## 6. The "100 % successful" rows are multi-state cycles, not booleans

Their labels read like toggles and their arms are not. Each steps a signed integer and wraps to `−1`:

| id | parameter | down | up | wrap | states |
|---:|---|---|---|---|---|
| 243 | steal | `+3` then signed mod 4 | `inc` | `3 → −1` | **`−1, 0, 1, 2`** |
| 244 | poach | `+2` then signed mod 3 | `inc` | `2 → −1` | **`−1, 0, 1`** |
| 245 | drop | `+4` then signed mod 5 | `inc` | `4 → −1` | **`−1, 0, 1, 2, 3`** |

The down path is the compiler's signed-remainder idiom — for id 243 an `and eax, 0x80000003` with a
sign fix-up, for 244 and 245 the `0x55555556` and `0x66666667` reciprocal multiplies.

**Three different state counts for three adjacent rows with near-identical labels.** What the
non-negative states select is not decoded here; **`−1` is the only state the arms distinguish
structurally**, by being the value both directions wrap to.

> A label that reads "Enable X" and an arm that cycles five states disagree, and **the arm wins.**

## 7. The display and adapter arms

**Id 263, "Game Window Mode"** mirrors `[01F82D20] + 8` into `rdi+0x10BC`, cycles it **mod 3**, then
calls a string-taking function and pushes the mode on. Three window modes.

**Id 264, "Game Display Resolution"** reads the same `+8` and **refuses to act unless it is ≤ 1**
(`cmp ecx,1 ; ja` straight to the tail) — so resolution stepping is **conditional on the window mode**,
a dependency between two rows that neither row's label mentions.

**Id 265, "Game Monitor"** reads `+0x60` and writes the same value straight back with a zero flag.
**Neither `bl` nor `sil` is tested** — both directions do the same thing, and the arm re-applies the
current monitor rather than changing it.

**Id 266, "System Adapter"** is a **two-level cursor**: it holds an adapter index at `+0x48` and a
monitor index at `+0x60`, queries a count, and steps the monitor — **carrying into the adapter index**
at either end, re-querying the count after each carry. Stepping "System Adapter" therefore moves
either field depending on where the cursor sits.

**Id 267** is an integer getter/setter step: read through `0032E010`, `lea ±1`, write through
`0032E030` — the integer analogue of the float getter/setter pairs slice F documented.

## 8. The property-numbering prediction — tested, and it failed

Slice I established that for the object at `01F82D20` the **property id is the field's dword index**
(`offset / 4`), and recorded properties **11, 14, 16, 19, 20, 21** as *unreached, not absent*, with H
named as the range that would most likely hold them.

**H holds none of them.** H's only two arms touching that object are ids 263 and 264; both read
`+0x08` (property 2) and neither uses the three-argument property setter at all — they call
`00182DE0` and `00182E10` directly.

Scanning **all 282 ids** rather than one slice:

| | |
|---|---|
| arms referencing `01F82D20` | 18, across slices **D (1), E (1), H (2), I (14)** |
| the rule `offset/4 == property` | **14 agreements, 0 disagreements** |
| properties reached by some arm | 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 22 |
| **of the six: now reached** | **14** (id 166, slice E) and **16** (id 134, slice D) |
| **of the six: reached by no arm at all** | **11, 19, 20, 21** — offsets `+0x2C`, `+0x4C`, `+0x50`, `+0x54` |

**So the prediction is wrong about where, and right about the rule.** Properties 14 and 16 exist and
obey `offset/4`, and both were extracted in slices written *before* slice I's rule existed —
id 166 passes `edx = 0xE` for field `+0x38`, and `0x38/4 = 14`. **Two slices agreeing about a
numbering rule neither derived from the other**, which is what the prediction was really testing.

The remaining four are not a numbering gap. They are **fields of the object that the console does not
expose** — the object has at least 23 dword properties and the menu reaches 17 of them.

> **A prediction that fails on its locations while confirming its rule is more informative than one
> that succeeds**, because the failure is what distinguishes "H has not been read yet" from "no arm
> anywhere touches these."

## 9. The cross-arm check ran here and did not fire

Per the work order's new check, an arm's extent is not always its behaviour. **In slice H, zero arms
jump into a neighbour's interior**; all 16 non-empty arms exit to `001D4BFA`.

Re-derived over the whole table for calibration: **14 of 227 distinct arms** continue inside a
neighbour — **reproducing slice I's count exactly**. My first pass reported 21 because it counted
*jump sites*; five arms contain more than one such jump (ids 177 and 180 have three each). **Same
measurement, different denominator** — 21 sites, 14 arms, 14 ids.

The tail set is also more structured than "`001D4BFA` and `001D4B59`". The arm at **`001D4B49`
(id 281, "Glare") is a three-entry shared epilogue**:

```asm
001D4B49  mov rcx,[01F82D20]   ; id 281 enters here
001D4B52  cmp dword ptr [rcx+0x34], 1
001D4B56  lea edx, [rsi + 0xD]         ; property 13
001D4B59  setne sil                    ; <- ids 276, 280 enter here, having set their own edx
001D4B60  call 0x1df340                ; <- id 279 enters here
001D4B65  mov rcx,[01F82D20]           ; <- ids 134, 166, 274, 275, 277, 278 enter here
001D4B76  call 0x1df340                ; property 3 = 3
```

Ids 276 and 280 are 21 and 18 bytes because they only load the object, compare their field, and set
their property number — **`lea edx,[rsi+0xF]` and `lea edx,[rsi+0xC]`, giving properties 15 and 12,
both matching `offset/4`** — then jump in. **Their property numbers are invisible unless the jump is
followed**, which is exactly what the check is for.

## 10. Data structures and formulas

```
console context (rdi)
  +0x0E34/+0x0E38   count of battle          value / step-modifier flag
  +0x0E3C/+0x0E40   count of magic
  +0x0E44/+0x0E48   count of tech
  +0x0E4C/+0x0E50   count of steal
  +0x0E54/+0x0E58   count of killed monsters      five stride-8 pairs
  +0x0E5C           steal  success state   -1..2
  +0x0E60           poach  success state   -1..1
  +0x0E64           drop   success state   -1..3
  +0x10B8           master volume ratio (f32)
  +0x10BC           window mode, mirrored from [01F82D20]+8
  +0x10C4           mouse vertical camera speed, mirrored from the accessor

01F82D20 -> platform/graphics property object; property id == field offset / 4
```

## 11. Call chain

```
input -> console dispatcher 001D1660 (id-12 -> arm)
  ids 238-245, 260   write console-context fields directly
  id  260            then pushes the same value to audio channels 1, 2 and 3
  ids 263, 264       read [01F82D20]+8, push through 00182DE0 / 00182E10
  ids 265, 266       read and write a display object through its own accessor
  id  267            integer getter/setter pair
row renderer 001CD0E0 draws all 32, including the 18 with no action arm
```

*(Cross-layer context, Pass 22 2026-09-14: this slice's subjects sit on the **presentation** path —
the dispatcher `001D1660` itself calls `00182DE0`/`00182E10` for ids 263–264, and the renderer
`001CD0E0` is called by presentation bodies `001D5260`/`001D0190`; it in turn reaches
**resource** `0020C700`, and `001D1660` reaches `002EEEE0` — 11 edges. A console that draws its
own menu and talks to the video mode lives on the render path, and the resource calls are the
fetch legs of that path.)*

## 12. Modding notes

**The three "100 % successful" rows are the interesting target here**, and they are not on/off: each
has a distinct number of states and a `−1` that both directions wrap to. Setting one of these from
outside the menu means choosing among 3, 4 or 5 values, not writing 1.

**The five counters floor at 0 in the arm only.** A direct write is not floored.

**Master volume has no clamp at all** in its arm (§3).

## 13. What is not known

- **What the non-negative states of ids 243–245 select.** The arms distinguish only `−1`; the
  consumer is not identified here.
- **What ids 265 and 266 address.** The accessor's object is not named, and id 265 not reading either
  direction may be deliberate ("re-apply") or a defect; **this slice cannot tell which.**
- **Why the "Set count of …" rows exist while the matching "Count of …" display rows (232–237) are
  emptied.** The editors survived and their read-outs did not, which is the reverse of the pattern in
  the stat block.
- **Properties 11, 19, 20, 21** of the `01F82D20` object — reached by no arm (§8); what they hold is
  outside the console's reach entirely.

## 14. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The id → arm mapping for all 32 ids | dwords at `001D4C1C + (id−12)×4`, `+ 0x00120000` | 1 |
| Every target, magnitude, mechanism and bound | complete decode of each arm, bounded by the next arm's start | 1 |
| Step magnitude is 1 or 10 by a flag | `mov ebp,1` / `lea edx,[rbp+9]` / `cmovne` in all five arms | 1 |
| The five stride-8 value/flag pairs | offsets read from all five arms | 1 |
| State counts 4, 3, 5 for ids 243–245 | the modulus and the wrap comparison in each arm | 1 |
| 15 of 18 emptied rows still draw a value | renderer jump table walked for those ids | 1 |
| `offset/4 == property`, 14 agreements 0 disagreements | all 282 ids scanned for `01F82D20` references | 1 |
| Properties 11, 19, 20, 21 reached by no arm | same scan; population stated | 1 |
| 14 of 227 arms continue in a neighbour | every arm's terminating jumps resolved against arm extents | 1 |
| `001D4B49` is a three-entry shared epilogue | the three entry addresses and their callers enumerated | 1 |

**Controls.** The absence claims are *"no H arm uses the property setter"*, *"no H arm crosses into a
neighbour"* and *"no H row draws `(EMPTY)`"*. The same instruments positively detect **16 arms
elsewhere that reference `01F82D20`, 14 of them carrying an explicit property number**, cross-arm
jumps in 14 arms elsewhere, and `(EMPTY)` rows at ids 211–216 — so each zero is a measurement, not a
silent non-match.

**An error corrected while producing this document, recorded because it is the fourth of its kind in
this block.** The property scan keyed on `mov edx, imm` and reported ids 276, 280 and 281 as carrying
no property number; they use `lea edx,[rsi+imm]` after `xor esi,esi`. A second pass then still missed
them because `xor esi,esi` registers the name `esi` while the `lea` base reads as `rsi`. Both are the
same failure the block has now seen with `subss`, `movss` and `mov edx`:

> **Check what your classifier requires, not only what it matches.** Every one of these reported an
> absence that was an artifact of the encoding it demanded.

**Address review flags** (`001D4C1C` and every arm address) are dispositioned once for all slices in
[slice A](arm-catalogue-slice-A-ids-12-43.md) §8.

## 15. Related

- [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md) — the slice division and row shape.
- [the-282-command-parameter-console.md](the-282-command-parameter-console.md) — the parent document.
- [slice E](arm-catalogue-slice-E-ids-140-171.md) — the label table (§4), the two-table cross-tab
  (§5), and id 166, which supplies property 14.
- [slice F](arm-catalogue-slice-F-ids-172-203.md) — the getter/setter pairs id 267 mirrors in integer.
- [slice A](arm-catalogue-slice-A-ids-12-43.md) — the address disposition.

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

**This slice tested a published prediction and the prediction failed.** Slice I recorded properties
**11, 14, 16, 19, 20, 21** as *unreached, not absent*, and predicted H would hold them. **H holds none
of the six** — its only two arms touching `01F82D20` never call the property setter.

> **The failure was worth more than the success would have been.** A whole-table scan found 14 and 16
> in slices E and D, and **11/19/20/21 reached by no arm anywhere** — separating *"H has not been read
> yet"* from *"nothing touches these"*. All four are numeric fields the console does not expose.

**And this slice widened the row shape, which nothing had done since it was fixed.** Ids 238–242 step
by **1 or 10** under a per-counter modifier flag: *"magnitude 1" and "magnitude 10" are both wrong
cells.*

**It is also the one place where the label table and the disassembly disagree.** Three adjacent rows
labelled *"Enable 100% successful …"* cycle **four, three and five** states over ranges including `−1`.
**Where they disagree, the arm wins.**


## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **Audio — SERVICE (3 edges).** 3 outbound (page-cited `001D1660`, `001CD0E0` call Audio bodies `002DEBA0`, `001DBB00`). Substantive edges include `001CD0E0` calls `002DEBA0`; `001D1660` calls `001DBB00`; `001D1660` calls `002DEBA0`.
- **Input — CLIENT (1 edge).** 1 inbound (Input bodies `0079C140` call page-cited `00182DE0`). Substantive edges include `00182DE0` is called by `0079C140`.
- **PlatformOnlineAchievements — SERVICE (1 edge).** 1 outbound (page-cited `001CD0E0` call PlatformOnlineAchievements bodies `003166F0`). Substantive edges include `001CD0E0` calls `003166F0`.
- **WorldAreaField — SERVICE (2 edges).** 2 outbound (page-cited `001CD0E0` call WorldAreaField bodies `WorldTransition_GetTransitionFieldId` (00314910), `FieldData_GetVariable0` (00265270)). Substantive edges include `001CD0E0` calls `WorldTransition_GetTransitionFieldId` (00314910); `001CD0E0` calls `FieldData_GetVariable0` (00265270).
- **PlatformOnlineAchievements — SERVICE (1 edge).** 1 outbound (page-cited `001CD0E0` call PlatformOnlineAchievements bodies `003166F0`). Substantive edges include `001CD0E0` calls `003166F0`.
