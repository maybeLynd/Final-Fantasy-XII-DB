---
system: Arm catalogue — slice A, command ids 12–43
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: CodeDomain — mixed; no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 2 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: console-join-repos-55
  crossref_clean: false
  reopened_count: 0
---

# Arm catalogue — slice A, command ids 12–43

> Slice A of the division in [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md).
> **This document describes 32 command ids. It says nothing about the other 250** — the console's
> distribution is measured in [the parent document](the-282-command-parameter-console.md) and is not
> re-derived, generalised or contradicted here.

## 1. What the player sees

Nothing — this is a developer tool. What a *developer* saw was a list of named settings they could
walk up and down with two buttons while the game ran. Slice A is the first 32 entries of that list,
and it is almost entirely **counters, toggles and mode cycles**: a value that steps by one, a flag
that flips, a mode that advances and wraps back to zero.

## 2. What an arm is

Each id indexes a table of image-relative offsets; the arm is a short run of instructions inside the
console function itself, not a separate function. **Almost every arm in this slice reads and writes a
field of one settings object through `rdi`**, and takes its direction from a register the dispatcher
has already set:

```asm
or      ecx, 0xffffffff        ; -1
mov     ebp, 1                 ; +1
test    bl, bl                 ; the direction flag
cmovne  ebp, ecx               ; step = bl ? -1 : +1
add     dword ptr [rdi + 0xda0], ebp
cmp     dword ptr [rdi + 0xda0], 0x12      ; and then a bound
```

So a row's useful content is **which field, how wide, what step, and what bound** — and the bound is
where the authored intent shows, because it is the range somebody decided the value should stay in.

**The settings object is not identified.** `rdi` is the console's own context pointer; nothing in
this slice names it or its type. Field offsets are therefore the strongest target identity available
here, and rows below give offset and width rather than a name. **That is an honest unknown, not an
omission.**

## 3. The catalogue

**Re-run 2026-09-03 under the corrected row shape** — `field · width · step magnitude · direction
mechanism · bound` — and with the arm-extent fix described in §8. The first version bounded each arm
at its first `jmp 001D4BFA`; that address is **both the unimplemented-id target and the common tail
most real arms jump to**, so the first version read only one branch of every two-branch arm and
recorded `inc` where the arm has `inc`/`dec`. **Every stepping row below gained its second
direction.** No target, bound or unimplemented id changed.

`b` = byte field, `d` = dword field; offsets are from `rdi`. Rows not marked *integer step* touch a
field or a helper without stepping.

| id | arm | kind | target | magnitude | direction mechanism | bound |
|---:|---|---|---|---|---|---|
| 12 | `001D16B1` | — | `0` | writes the global `01DF6E48` |
| **13** | `001D4BFA` | — | — | **do-nothing** |
| 14 | `001D16C4` | integer step | `d+0xC20` | 1 | `inc`/`dec` | `3` — wraps |
| 15 | `001D17D8` | integer step | `d+0xAA8` | 1 | `inc` / `add 0xC7` (≡ −1) | `200` — wraps: signed modulo 200 through the `0x51EB851F` reciprocal (`001D17EE`–`001D180D`); corrected 2026-09-13 on `OPUS-CONSOLE-ID15-BOUND` |
| **16** | `001D4BFA` | — | — | **do-nothing** |
| **17** | `001D4BFA` | — | — | **do-nothing** |
| **18** | `001D4BFA` | — | — | **do-nothing** |
| 19 | `001D1740` | integer step | `d+0xDA0` | 1 | `cmov` ±1 | `0x12` |
| 20 | `001D170E` | `d+0xC40` | — | one helper call |
| 21 | `001D177E` | integer step | `d+0xC44` | 1 | `cmov` ±1 | `0` — floor |
| 22 | `001D17AB` | integer step | `d+0xC48`, `d+0xC44` | 1 | `cmov` ±1 | `0` |
| **23** | `001D4BFA` | — | — | **do-nothing** |
| 24 | `001D1818` | `d+0xAB8` | — | two helper calls |
| 25 | `001D1830` | integer step | — | 1 | `cmov` ±1 + `inc`/`dec` | `4` |
| 26 | `001D1867` | `d+0xCF4` | — | **the only float arm in this slice**: constants `1` and `-1` |
| 27 | `001D1893` | integer step | — | 1 | `cmov` ±1 | `3` |
| 28 | `001D18E0` | **toggles `b+0xC72`**; saves/restores `f32+0xC74`, `+0xC78`, `+0xC7C`, `b+0xC80`, `+0xC81`, `+0xC82`, `f32+0xC88`, `+0xC8C`, `+0xC90`, `b+0xC94`, `+0xC95`, `f32+0xC98` | `0` | **a save/zero/restore group, not nine settings** — see the correction below |
| 29 | `001D1B11` | `b+0xC71` | `0` | `cmp` / `sete` / `mov` — **a boolean toggle** |
| 30 | `001D1B26` | — | `0` | writes the global `02CB8148` |
| 31 | `001D1B39` | — | — | writes the global `02CB8150` |
| 32 | `001D1B50` | integer step | `d+0xC2C` | 1 | `inc`/`dec` | `4`, `0` |
| 33 | `001D1BBA` | `b+0xCF0` | `0` | boolean toggle |
| 34 | `001D1BCF` | `b+0xABC` | `0` | boolean, then two helper calls |
| 35 | `001D1C0B` | `b+0xABD` | `0` | boolean, then two helper calls |
| 36 | `001D2ADE` | — | `0` | helper call only — the **largest** displacement in this slice, not the only one: `001D2ADE` sits 3,460 B past the run's top (`001D1D5A`), but the run is only loosely address-ordered (ids 20/19 and 15-after-22 are already swapped, and id 51's arm `001D18CA` lies inside it). Same-function block placement inside `001D1660`–`001D4C19`, not a property of the arm — id 39 below is also helper-call-only and sits in the run |
| 37 | `001D1C47` | `b+0xABE` | `0` | boolean, then two helper calls |
| 38 | `001D1C83` | integer step | `d+0xAC0` | 1 | `inc` only — no direction test; then `0018B0A0(obj, value != 0)` | `3` — wraps: modulo 3 through `0x55555556` (`001D1C83`–`001D1C9E`); corrected 2026-09-13, found by the same scan |
| 39 | `001D1CCE` | — | `0` | helper call only |
| 40 | `001D1CE9` | `b+0xAC4` | `0` | boolean, then a helper call |
| 41 | `001D1D17` | — | `0` | calls the ~~33-arm~~ 33-call-site shared helper *(corrected 2026-10-02, OPUS: 33 direct calls to `00193D50` in `001D1660`)* |
| 42 | `001D1D36` | — | `0` | calls the ~~33-arm~~ 33-call-site shared helper and one other *(corrected 2026-10-02, OPUS: 33 direct calls to `00193D50` in `001D1660`)* |
| 43 | `001D1D5A` | integer step | `d+0xC04` | 1 | `inc`/`dec` | `2`, `0x13` |

**27 real arms and 5 do-nothing ids** (13, 16, 17, 18, 23), touching **26 distinct fields** of the
settings object.

### Correction 2026-09-03 — id 28 is a save/zero/restore, and `02CB8130` is a float

**The first version of this row read as if `02CB8130` were one of the things id 28 toggles.** It is
not, and a cross-document join flagged the apparent conflict: `02CB8130` is bound to a **boolean**
here and to a **float** — id 108, "Diffuse intensity", stepped by `0.02` — in
[slice D](arm-catalogue-slice-D-ids-108-139.md). **A boolean and a float cannot share an address.**

**Re-read from the image: there is no conflict in the data, only in this row's phrasing.**

```asm
001D18E0  cmp   byte ptr [rdi + 0xc72], 0    ; THE toggle — a byte field of the settings object
001D18E7  sete  al
001D18EA  mov   byte ptr [rdi + 0xc72], al
001D18F8  movss xmm0, [02CB8130]             ; on the ON edge: SAVE three floats...
001D1900  movss [rdi + 0xc74], xmm0
001D194F  mov   qword ptr [02CB8130], 0      ; ...then zero them
001D1A5D  movss [02CB8130], xmm0             ; on the OFF edge: restore from the saved copy
```

**`02CB8130` is read and written with `movss` on both edges — it is a float in this arm too.** Id 28
toggles `b+0xC72` and uses the twelve `rdi` fields as a **save area**, so the row's "nine fields"
reading was wrong twice: they are not nine settings, and there are twelve.

**The three floats it saves are `02CB8130`, `02CB8134` and `02CB8138` — exactly the targets of slice
D's ids 108, 109 and 110.** So the group is coherent: three tunable floats, plus one toggle that
parks and restores them.

> **One trap worth recording, because the width-from-the-store rule walks straight into it.**
> `001D194F` is `mov qword ptr [02CB8130], 0` — an **8-byte** store. Taken as evidence of field
> width it says `02CB8130` is 8 bytes. It is not: it is one instruction zeroing **two adjacent
> 4-byte floats**, `02CB8130` and `02CB8134`. **A store's width bounds the bytes touched, not the
> width of the field at its base address** — and a compiler merging adjacent zero-stores is the
> ordinary way that gap opens.

### The two shared helpers are named, not cited

Ids 28, 41, 42 and 43 reach helpers the parent document enumerates as hubs — one serving **45** ~~arms~~ call sites,
the other **33** *(corrected 2026-10-02, OPUS: 45 direct calls to `001A9930` and 33 to `00193D50` in `001D1660`)*. They are named here by that role and **deliberately kept out of this document's
address citations**: citing a hub commits these rows to its entire caller neighbourhood, and the
census that would justify that lives in the parent document, not this one.

### Slice A contains no `0.01` step arm

The parent document records `0.01` as the console's most common step constant, referenced 88 times.
**Not one of those references is in slice A.** ~~The only float constants here are `1` and `-1`, in~~
~~id 26~~ The step constants are `1` and `-1`, in id 26; id 28 also reads the Rec.709 weights `0.2126`, `0.7152` and `0.0722` (`008F6D48`, `008F6D4C`, `008F6D44`) *(corrected 2026-10-02, OPUS: `mulss` at `001D1660+0x3D0`, `+0x3C0`, `+0x3D8`)*.

*Control, chosen before the scan:* the extractor must find a float constant where one exists. It
finds id 26's `1` / `-1`, so the zero for `0.01` is a measurement and not a silent non-match. **This
is a statement about slice A only** — where the 88 references do fall is the parent document's
measurement and is not re-derived here.

## 4. Data structures and formulas

The step, exactly as the arms compute it:

```c
step = direction_flag ? -1 : +1;          /* test bl,bl ; cmovne */
field += step;
/* then one of: */
if (field >= BOUND) field = 0;            /* wrap  — id 14, bound 3      */
if (field >  BOUND) field = BOUND;        /* clamp — id 19, bound 0x12   */
if (field <  0)     field = 0;            /* floor — ids 21, 22          */
```

Boolean arms do not step at all:

```c
field = (field == 0);   /* cmp byte [rdi+off],0 ; sete ; mov — ids 29, 33, 34, 35, 37, 40 */
```

## 5. Call chain

```
console dispatch  001D1660
  -> table 001D4C1C + (id - 12)*4        a dword RVA; + 0x00120000 = the arm
     -> the arm: read/modify/write a field of the object at rdi, or call a helper
     -> jmp 001D4BFA                     the shared exit, which 5 of this slice's ids reach directly
```

## 6. Modding notes

- **The bounds are the authored intent.** A mode that wraps at 3 has three states; a counter capped
  at 18 has nineteen. Those numbers were chosen by someone, and they are the part of a row that
  survives not knowing what the field is.
- **Do not infer a field's meaning from its neighbours' offsets.** The offsets are dense but the ids
  are not ordered by subject — `0xABC`–`0xAC4` and `0xC71`–`0xC8C` interleave across the slice.
- **Five ids in this range do nothing at all.** A tool driving this console by id gets silence from
  13, 16, 17, 18 and 23, and that is shipped behaviour, not a fault.

## 7. What is not known

- [x] ~~**What the settings object at `rdi` is.** Not identified here, so every field target in this
      slice is an offset rather than a name.~~ **Answered 2026-09-14 (FABLE):** it is the console's own settings object.
      `001D50D0` returns it: a `0x10E8`-byte singleton built on first use by `001CCB20` and cached at `01F81428` (`001D50DD`–`001D5106`). The same object carries the console's labels at `+0x130 + 8 × id`, which `001CCB20` clears (`001CCE6F`) before `001D0390` fills them (`001CCEA4`). `001D1660` receives it through `001CD040`'s pass-through `rcx` (the steal page's `FK-3`, [the steal roll](../../08-Combat-Formula/Steal/the-steal-roll.md)). The fields stay offsets; each arm's label ([console command names](console-command-names.md)) is the
      name the tool gave the value, not a traced consumer.
- [x] **UQ-5.** What each of the 26 fields controls. ~~**No field in this slice was traced to a consumer.**~~
      ***Four of them now are, and the clause is corrected rather than deleted — 2026-09-21 (FABLE), on
      `OPUS-REQ-FABLE-UQ5-CONSUMER-IS-NAMED-SEMANTICS-ARE-YOURS`.***
      - **The renderer is not a consumer, and that is settled on a sibling page.** `001CD0E0` reads every one of this
        slice's offsets **because it prints every row**: each arm ends `mov eax, [obj + disp]` / `mov [rsp+0x28], eax`
        into a `vsnprintf` whose label comes from `[obj + id×8 + 0x130]`. [Slice B](arm-catalogue-slice-B-ids-44-75.md)
        §5 already classifies a slot read only by that renderer and the set/get arm `001D1660` as **having no
        consumer** — 41 of 68 neighbouring slots fell in that class. So *the console pair reading a field is the null
        result, not the answer.*
      - **And a census rooted at the getter cannot settle it either.** Tracking the object from `001D50D0`'s return
        and from the cache cell `01F81428`, with callee-saved registers modelled, finds **nothing in `001CD0E0`** —
        because the renderer receives the object as an **argument**. *That is the control*: an instrument that cannot
        see the one reader everybody agrees about is not measuring the population. Any getter-rooted displacement
        count has the same blind spot.
      - **What that census does find is real, because it is the opposite kind of claim.** Four offsets are read by
        bodies that fetch the singleton **themselves** and are neither the builder nor the console pair:

        | offset | outside reader | what the reader is |
        |---|---|---|
        | `+0xC20` | `0017D470` | a 20-byte getter — `call` the getter, `mov eax, [rax + 0xC20]`, return. The ledger names it `BattleGlobal_GetTargetEligibilityModeC20`, and **the body is the join**: it returns this field and nothing else |
        | `+0xC2C` | `001E2AF0` | a 4,745-byte render body ([the post-process page](../../22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md)'s largest `UQ-289` member) |
        | `+0xC71` | `001BC190`, `001E2AF0`, `001F8D10` | render support and **character-render material-parameter binding** — the offset the renderer reads with a `cmp`, so a branch condition on both sides |
        | `+0xCF4` | `00180090` | a 40-byte float getter returning `[obj + 0xCF4]`, or `0.0` when the singleton does not exist |

      - ***The argument-rooted census now exists, and it classifies eighteen of the thirty offsets — later the same
        day.*** Propagating the object from the getter and the cache cell **through call arguments** to a fixed
        point (three bodies receive it on the first pass, two more on the second) makes the row renderer visible,
        which is the control the getter-rooted version failed. Against the thirty offsets this slice names:
        - **Four have an outside consumer** — the table above.
        - **Fourteen are read by the console and nothing else**: `+0xAA8`, `+0xAB8`, `+0xABC`, `+0xABD`, `+0xABE`,
          `+0xAC0` (the renderer and its sibling `001CD0D0`), `+0xAC4`, `+0xC04`, `+0xC40`, `+0xC44`, `+0xC48`,
          `+0xC72`, `+0xCF0`, `+0xDA0`. By the classification [slice B](arm-catalogue-slice-B-ids-44-75.md) §5
          established, **those fourteen have no consumer** — the tracing is exhausted for them on this image.
        - **Twelve are not reached by the census at all** (`+0xC74`–`+0xC98`), and *that is a statement about the
          instrument, not about them*: the renderer demonstrably prints every row, so a field it does not appear to
          read is one this tracker loses — most likely behind an inner pointer rather than the object's own base.
          **Nothing is claimed for those twelve.**
      - **Neighbour accounting — naming that first reader reaches into `CombatAction`, and the crossing is this
        entry's doing.** The `+0xC20` getter is called from the combat layer, which is the whole point of the row:
        *a developer-console field is read by a battle-side accessor*, so the console is the source and combat the
        client. One edge, one direction, and **nothing about combat's behaviour is claimed here** — only that the
        field leaves the console boundary, which is exactly what `UQ-5`'s blocking clause said had never been shown.
      - **So the better question, and what is still open.** Twenty-two of the twenty-six have no reader outside the
        console *that fetches the object itself*; whether they have one that receives it as an argument is not
        established, and the instrument for that must be rooted at the **argument**, not the getter. The four above
        have named readers whose bodies are the semantic work: `+0xC20` is a battle target-eligibility mode on the
        strength of its getter's ledger name and its one-field body, and `+0xC71` is consulted by the character
        render path. ~~`UQ-5` stays open on the other twenty-two and on what the four *mean* to their readers.~~
      - **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): the engine names every field itself.** The console prints
        each row's label from `[obj + id×8 + 0x130]`, and [console-command-names](console-command-names.md) joins
        all 282, but this box never used them. By arm id they are:
        - `+0xC20` Invincible (14);
        - `+0xAA8` Load ps2 savedata from slot (15);
        - `+0xDA0` Load sample chr (19);
        - `+0xC40` Load chr (20);
        - `+0xC44` Variation (21);
        - `+0xC48` CLUT (22);
        - `+0xAB8` Change cast shadow object (24);
        - `+0xCF4` Debug high model skeleton (26);
        - `+0xC72` and its saved block, Use PS2 lighting (28);
        - `+0xC71` Use normal map (29);
        - `+0xC2C` Display texture density (32);
        - `+0xCF0` Switch diffuse texture (33);
        - `+0xABC` / `+0xABD` / `+0xABE` Enable Map / Character / UI Display (34, 35, 37);
        - `+0xAC0` Enable VFX Display (38);
        - `+0xAC4` Enable Shadow Display (40);
        - `+0xC04` HBAO NumSteps (43).
        **That also says what the four consumed fields mean to their readers.** A receiver-checked census,
        [`console_field_readers.py`](members/console_field_readers.py), traces each access's base register back
        to the getter or the cell; its control reproduces UQ-18's Huge Damage reader and rejects two impostors:
        - **Invincible** is read by `BattleTarget_ComputeUnitEligibilityMask` through `0017D470` (`0030B883`,
          `0030B8B6`). So invincibility is implemented as a target-eligibility mode, which is why the arm cycles
          it through three states. *(narrowed 2026-10-02, FABLE, reviewing ASTRA's `ov42-resource-eligibility-domain`:
          the two reads are separate getter calls. Mode 1 sets bit 0 of the mask's upper WORD when the unit's
          current stats exist and their byte `+5` is 0, and mode 2 sets bit 1. A nonzero upper WORD stops an MP
          decrease in `BattleStats_ModifyPrimaryResource` after its notification attempt. See the OV-42 mode-17
          subsection of `07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`.)*
        - **Use normal map** is read by the render bodies `001BC190`, `001E2AF0` and `001F8D10` (`001F8F96`).
        - **Display texture density** is read by `001E2AF0` (`001E37DC`).
        - **Debug high model skeleton** is a float read through `00180090` by `AddMotion_ApplyBonePose`
          (`00371AF4`).
        The other fields' labels are commands and display switches. The console arms act on them directly (loads,
        the PS2-lighting swap), and the census finds no outside reader that fetches the object itself; the
        argument-rooted blind spot recorded above still applies to them.
- [x] ~~**UQ-6.** What ids 12, 30 and 31 do with the globals `01DF6E48`, `02CB8148` and `02CB8150`.
      *Narrowed 2026-09-14 (FABLE), not answered:*
      - **Id 12, "Read Json Data".** `01DF6E48` is `1` in the image and is tested at the entry of five functions:
        `001C5930` (which also proceeds when `01F81282` is set), `001C5F20`, `001C61F0`, `001C6C00` and `001C7940`. That is the
        family [what the console tunes](what-the-console-tunes.md) links to the JSON sidecar keys.
      - **Ids 30 and 31.** *"Display normal only"* (`02CB8148`, a byte) and *"Use vertex color"* (`02CB8150`, a dword, zero at
        load) meet in one reader, `001E2AF0`. It computes `mode = (02CB8150 == 0) ? 2 : byte 02CB8148` and stores it at
        `[rsp+0x70]` (`001E3395`–`001E33AB`).~~
      ***ANSWERED 2026-09-17 (FABLE): id 12 forces the cutscene JSON sidecar to be parsed, and ids 30 and 31 pick a shading mode for map objects.** *Id 12, `01DF6E48`:* the sidecar parser `001C5930` (1,505 B, the reader of `JsonData/CutScenes/<scene>` on [the cutscene-slots page](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)) tests the byte at its entry and parses when it is set or when `01F81282` is set, and returns otherwise (`001C5958`..`001C5968`); its three siblings `001C5F20`, `001C61F0` and `001C6C00` test the same byte, so the arm's *Read Json Data* re-runs the JSON readers on the next pass. *Ids 30 and 31, `02CB8148` and `02CB8150`:* they are read together in one place, the map ordered-object draw routine `001E2AF0` (4,745 B, reached from `MapOrderedObject` through its `+0x08` object), which folds them into one mode word: 2 unless *Use vertex color* is set, else the *Display normal only* byte (`001E3395`..`001E33AB`, a `cmove`), and stores that word into the object's parameter block (`001E3868`..`001E386C`). So the two toggles select a debug shading mode for the map's drawn objects, and nothing else reads either global ([the consumers table](members/console-tunables-consumers.tsv) on the console page). Static; both readers read at the site.*

      What the five JSON readers skip, and what that draw mode selects downstream, were not read.
- [x] **UQ-7.** *(DISSOLVED in the register 2026-09-26, FABLE, Claude Opus 5.5: the premise was wrong, since id 36 is the largest displacement, not the only one)* Why id 36's arm sits at `001D2ADE`, far outside the contiguous run the other 26 occupy.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The id → arm mapping for all 32 ids | dwords at `001D4C1C + (id−12)×4` read from the image, plus `0x00120000` | 1 |
| Field offsets, widths, steps and bounds | complete decode of each arm from its table target to its exit `jmp` | 1 |
| 5 do-nothing ids in this slice | those entries resolve to `001D4BFA` | 1 |
| No `0.01` in slice A | float-constant extraction over all 27 arms, with a positive control (id 26) | 1 |

**Disposition of the one `verify_doc_addresses` review flag.** `001D4C1C` is cited as a `.text`
address that is not a function entry. **Confirmed legitimate:** it is the dispatch table itself — a
jump table sitting in `.text` immediately after the console function, which is the case the checker
asks to have confirmed rather than a defect. Every arm address cited here is an *interior* address of
that same function for the same reason: switch arms are not functions.

## 9. Related

- [the-282-command-parameter-console.md](the-282-command-parameter-console.md) — the frame: dispatch,
  table extent, arm-kind distribution, step constants, and the hub census this document defers to
- [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md) — the division and its rules

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

**What the join found in this slice, and it was a defect here.** `02CB8130` was bound by this
document to a toggle and by slice D to a float. **A boolean and a float cannot share an address**, and
this slice's row was the wrong one: **id 28's toggle is `b+0xC72`**, and `02CB8130`/`8134`/`8138` are
three floats it **saves, zeroes and restores** — slice D's ids 108/109/110. Corrected to *one toggle
plus a twelve-field save/restore area*.

**And the correction carried a trap worth more than the fix.** `001D194F` is
`mov qword ptr [02CB8130], 0` — **an 8-byte store zeroing two adjacent 4-byte floats.**

> **A store's width bounds the bytes touched, not the width of the field at its base.** The rule
> *"width must come from the store"* would have sized this field at 8 bytes — **it would have
> mis-sized the field it was invented to protect.**

**Corroborated:** id 14, this slice's wrap-at-3 counter, is labelled `Invincible:` — a name that
matches the behaviour read from the arm, from a source that knew nothing about it.


*(Pass 22 adjacency, 2026-09-14: this slice's crossings are the shared dispatcher's, repeated
here because every slice cites `001D1660` — it calls the **presentation** materializers
`001D5120`/`001C7360`/`001C7520`, reaches **audio** `002DEBA0`/`001DBB00`, and fetches
through **resource** `002EEEE0`. The console lives on the render path and pulls its row content
through resource/audio helpers; the edges belong to the dispatcher, not to this slice's arms.)*

*(Pass 22 live-graph completion, 2026-09-15: `001D50D0` — the singleton accessor — is called
by `Input` bodies `00197800`/`00197160`/`00197790` (3), and `001CCB20` calls `Platform`
`005CC930` (1). The accessor's consumers include the input layer; the platform call is this
slice's arm reaching platform state.)*

*(Pass 22 live-graph sweep 2, 2026-09-15: the platform callee `005CC930` is itself called by
`Application` `00799980` (1 edge) — the arm's platform leg is reached from application init.)*

`002EEEE0` (295 B) is the ChSEinfo query `001D1660`'s arm runs: `cx` splits into `word` + `byte(eax>>16)` with `edx` adding in; a negative `esi` rescans `00D0F870`..`00D0F8B0` for the byte id (a miss formats `"get char…"` `00D0F8C0` through `0017D280`), and a hit remaps `edi` through `(i+7)&~7 x2` into `dword[r12+rax*4]`; `ebp = edi<<16 | esi` packs the argument and `002ED6F0`/`002DF980`/`002DF8E0` produce the output - the console's character-state-evidence info command.

Interior anchor `002EEF80` (function `002EEEE0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-EC7-169, 2026-09-23)

**ActorEntity — MECHANICAL (SWE2-EC7-169, 1 edge).** `002DF980` — one of the output
primitives the `ChSEinfo` arm `002EEEE0` runs — is called by `0032FCA0`, owned by that
layer: console formatting fan-in, not an actor relationship of the arm catalogue.

**Save_Load_Settings — MECHANICAL (SWE2-EC7-169, 2 edges).** `0017D280` — the arm's
`"get char…"` formatter — is called by `001DE5D0`/`001DF350` of that layer; the same
string helper reused, not a save relationship of the console.

**Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-169, 25 edges).** `0017D280` and
`002ED6F0` are the console's shared output helpers (`0050C670`/`0050C8D0`/`0050C990`,
`003580C0` among 25 edges); script-bridge code calls the same emitters — fan-in.

**WorldAreaField — MECHANICAL (SWE2-EC7-169, 5 edges).** `0017D280`, `002DF980`,
`001CD0E0` and `002DEBA0` reach that layer (`00314020`, `00379A10`, `00265270`,
`00314910` among 5 edges) — the same shared output helpers called from world-area
code; fan-in, not a world relationship of the console.

`001E4F70` (265 B) is the matrix adapter `001E2AF0`'s arm runs: with `[rcx+0x10]` live it scatter-copies the record's twelve floats (`+0xC/+0x1C/+0x2C` columns, `+0/+0x4`, `+0x8/+0x10`, `+0x14/+0x18`, `+0x20`, `+0x24/+0x28`) into a stack 4x4 with the `w` column forced `{0,0,0,1.0f}` before `001854C0` reshapes it; absent the record it copies the caller's `rdx` 0x40 matrix verbatim - either way `001E4B80(rcx, &m)` consumes the result, the transform the arm applies to the render target.

Interior anchor `001E5033` (function `001E4F70`).

`001E4B80` (996 B) is the scale-into-basis composer `001E4F70` hands its staged 4x4 to: the `rcx` scalars (`[+0]`, `[+4]`/`[+8]`, `[+0x18]`/`[+0x1C]`/`[+0x20]`) multiply each `rdx` row's lanes via `shufps 0x55`/`0xAA`/`0xFF` broadcasts into a stack matrix, which `001E25F0` then consumes - the per-axis scale apply the slice-A arm's transform performs.

Interior anchor `001E4F15` (function `001E4B80`).

`001E25F0` (1271 B) is the box-list axis-mask classifier `001E4B80` feeds its staged 4x4 into: a `rdx` centre plus `+0xC` half-extent is compared per axis against the `rcx` box and the `rax` box (`comiss`/`cmova` ladders OR-ing `0x10`/`8`/`4`/`2`/`1` into `edi`), then the walk repeats over the `[r11+0x20]`/`+0x28`/`+0x30`/`+0x38` linked set AND-ing each iteration's mask into the result - a 349-instruction call-free separating-axis sweep returning the surviving axis bits.

Interior anchor `001E26E7` (function `001E25F0`).

`001C0540` (234 B) is the EASTL `basic_string` build the `001CD0E0` dispatcher uses for string results: `byte[rcx+9]` clear or a null `[rcx+0x10]` takes the construct-empty path - `001EDF00` ("EASTL basic_string") on a stack temp, the dst triple zeroed, a second `001EDF00` on `dst+0x18`, then `001A4BF0` - and a set flag with payload copies through the `001A9930` allocator + `001A74A0`; all paths return `rdx`

Interior anchor `001C05CB` (function `001C0540`).

`001A74A0` (338 B) is the string-assign-and-basename helper the `001C0540` result builder uses through the `001A9930` allocator: it runs `001A2F70` twice pairing `r8+0x260` with `rcx+0x448`, zeroes the `rsi` destination triple and `001EDF00`-initialises `rsi+0x18` from the record's `+0x58`, `001A4BF0`-assigns from `[rbx+0x40]`/`[rbx+0x48]`, then walks the string backward for the last `0x2F` to compute a basename offset, `001A9E50`-extracts and `001A5760`-appends that suffix, and frees the temp through its `+0x18` vtable slot

Interior anchor `001A7560` (function `001A74A0`).
- **CombatAction — CLIENT (1 edge).** 1 inbound (CombatAction bodies `BattleTarget_ComputeUnitEligibilityMask` (0030B7F0) call page-cited `BattleGlobal_GetTargetEligibilityModeC20` (0017D470)). Substantive edges include `BattleGlobal_GetTargetEligibilityModeC20` (0017D470) is called by `BattleTarget_ComputeUnitEligibilityMask` (0030B7F0).
- **Input — CLIENT and SERVICE (13 edges).** 8 inbound (Input bodies `InputManager_PollAndBuildControlState` (00196FF0), `001E0DA0`, `001E0E70` call page-cited `001D50D0`, `005CC930`, `InputManager_TranslateBindingProfileToControlState` (00197160)); 5 outbound (page-cited `InputManager_TranslateBindingProfileToControlState` (00197160) call Input bodies `InputBackend_IsControlCode28To283ActiveForBank` (0079E6A0), `InputBackend_IsControlCode11To27ActiveAnyDevice` (0079E650), `InputBackend_IsPrimaryControlCode1To3Active` (0079E6D0)). Substantive edges include `InputManager_TranslateBindingProfileToControlState` (00197160) is called by `InputManager_PollAndBuildControlState` (00196FF0); `InputManager_TranslateBindingProfileToControlState` (00197160) calls `InputBackend_IsControlCode28To283ActiveForBank` (0079E6A0); `InputManager_TranslateBindingProfileToControlState` (00197160) calls `InputBackend_IsControlCode11To27ActiveAnyDevice` (0079E650); `InputManager_TranslateBindingProfileToControlState` (00197160) calls `InputBackend_IsPrimaryControlCode1To3Active` (0079E6D0).
- **Platform — SERVICE (2 edges).** 2 outbound (page-cited `001CCB20`, `00799980` call Platform bodies `005CC930`). Substantive edges include `001CCB20` calls `005CC930`; `00799980` calls `005CC930`.
- **PlatformOnlineAchievements — SERVICE (1 edge).** 1 outbound (page-cited `001CD0E0` call PlatformOnlineAchievements bodies `003166F0`). Substantive edges include `001CD0E0` calls `003166F0`.

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-arm-catalogue-slice-a-ids-12-43-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `001BBF40` | 118 B | `001BC190` + 0x148 | walks the `0x20` qwords starting at `rcx+0xA0` and issues the call at `001BBF40` + 0x2B on each non-null one, then issues the call at `001BBF40` + 0x49 with (`rcx+0xA0`, 0, `0x100`) and tail-jumps at `001BBF40` + 0x71 with (`rcx+0x1A0`, 0, `0x100`) | Interior anchor `001BBF63`; Interior anchor `001BBF6B`; Interior anchor `001BBF74`; Interior anchor `001BBF89`; Interior anchor `001BBFB1` |
| `001DE180` | 116 B | `001DE5D0` + 0x720 | takes the dword `+4` of the table at qword `rcx-0x90` as an offset `d` (read before each of the first two stores), stores the address `00901028` to the qword at `rcx - 0x90 + d` and `d - 0x90` to the dword at `rcx - 0x94 + d`, stores `00900F20` to qword `rcx-0x80`, issues the call at `001DE180` + 0x50 and then the indirect call at `001DE180` + 0x59, both with `rcx-0x80`, and tail-jumps through the indirect jump at `001DE180` + 0x6D with `rcx-0x78` | Interior anchor `001DE19F`; Interior anchor `001DE1C0`; Interior anchor `001DE1C8`; Interior anchor `001DE1D0`; Interior anchor `001DE1ED` |
