---
system: Arm catalogue — slice B, command ids 44–75
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
    verified: 1 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
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

# Arm catalogue — slice B, command ids 44–75

> Slice B of the division in [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md).
> **32 command ids. It says nothing about the other 250.**

## 1. What the player sees

Nothing — a developer tool. Slice B is where the console stops being counters and becomes
**continuous tuning**: thirteen of its thirty-two commands walk a floating-point value up or down by
a hundredth, and they address **thirteen consecutive floats in one array** — the shape of a panel of
sliders sitting next to each other in memory because they sat next to each other on screen.

## 2. The console's own signature, read from its prologue

The dispatcher's first eleven instructions settle three things this catalogue depends on:

```asm
001D1660  mov  [rsp+0x10], rbx
001D166F  add  r9d, -0xc              ; command id, rebased so 12 -> 0
001D1673  movzx esi, r8b              ; arg 3 -> sil
001D1677  movzx ebx, dl               ; arg 2 -> bl     <- the direction flag
001D167A  mov  rdi, rcx               ; arg 1 -> rdi    <- the settings object
001D167D  cmp  r9d, 0x119             ; 281
001D1684  ja   0x1D4C09               ; out of range
001D168F  lea  rcx, [rip - 0xb1696]   ; = 0x00120000, the image base
001D16A3  mov  r9d, [rcx + rax*4 + 0xb4c1c]   ; the table at 001D4C1C
001D16AB  add  r9, rcx                ; arm = RVA + image base
001D16AE  jmp  r9
```

- **The direction flag is an argument, not a global.** It arrives in `dl` and lives in `bl`; a
  second byte flag arrives in `r8b` and lives in `sil`. That answers the open item raised with this
  slice: **nothing in the console supplies it — the caller does.** Who calls it is still untraced.
- **The id bound is the code's own:** `cmp r9d, 0x119` after rebasing by 12, so ids 12–293, **282**.
- **The `+ image base` step is explicit**, which is why the table holds RVAs.

## 3. The catalogue

Row shape per the work order: **field · width · step magnitude · direction mechanism · bound.**
`b` = byte, `d` = dword; `rdi` offsets are fields of the settings object, `02CBxxxx` are globals.

| id | arm | kind | target | magnitude | direction mechanism | bound |
|---:|---|---|---|---|---|---|
| 44 | `001D1DB4` | integer step | `d+0xC08` | 1 | `inc`/`dec` | `2`, `0x13` |
| 45 | `001D4AC0` | other | — | — | — | `0` |
| 46 | `001D4ADF` | other | — | — | — | `0` |
| 47 | `001D1E0E` | other | — | — | — | — |
| 48 | `001D1E2A` | other | — | — | — | `0` |
| 49 | `001D1E68` | other | — | — | — | — |
| 50 | `001D1E49` | other | — | — | — | `0` |
| 51 | `001D18CA` | other | — | — | — | — |
| 52 | `001D1F46` | other | — | — | — | — |
| 53 | `001D3988` | integer step | — | 1 | `inc`/`dec` | `2` |
| 54 | `001D39CD` | integer step | `d+0xD08` | 1 | `inc`/`dec` | — |
| 55 | `001D3A2A` | other | — | — | — | — |
| **56** | `001D4BFA` | **unimplemented** | — | — | — | — |
| 57 | `001D3A4A` | other | — | — | — | — |
| **58** | `001D4BFA` | **unimplemented** | — | — | — | — |
| **59** | `001D4BFA` | **unimplemented** | — | — | — | — |
| 60 | `001D1F5A` | integer step | `d+0xC28`, `b+0xC0C` | 1 | `cmov` ±1 | `1` |
| 61 | `001D213D` | other | — | — | — | `0` |
| 62 | `001D2150` | other | `b+0x10D9` | — | — | `0` |
| 63 | `001D2165` | **float step** | `02CB80B0` | **0.01** | `addss`/`subss` pair | — |
| 64 | `001D219B` | **float step** | `02CB80B4` | **0.01** | `addss`/`subss` pair | — |
| 65 | `001D21D1` | **float step** | `02CB80B8` | **0.01** | `addss`/`subss` pair | — |
| 66 | `001D2207` | **float step** | `02CB80BC` | **0.01** | `addss`/`subss` pair | — |
| 67 | `001D223D` | **float step** | `02CB80C0` | **0.001** | `addss`/`subss` pair | — |
| 68 | `001D2273` | **float step** | `02CB80C4` | **0.01** | `addss`/`subss` pair | — |
| 69 | `001D22A9` | **float step** | `02CB80C8` | **0.001** | `addss`/`subss` pair | — |
| 70 | `001D22DF` | **float step** | `02CB80CC` | **0.01** | `addss`/`subss` pair | — |
| 71 | `001D2315` | **float step** | `02CB80D0` | **0.01** | `addss`/`subss` pair | — |
| 72 | `001D234B` | **float step** | `02CB80E8` | **0.01** | `addss`/`subss` pair | — |
| 73 | `001D2381` | **float step** | `02CB80EC` | **0.01** | `addss`/`subss` pair | — |
| 74 | `001D23B7` | **float step** | `02CB80F0` | **0.01** | `addss`/`subss` pair | — |
| 75 | `001D23ED` | **float step** | `02CB80F4` | **0.01** | `addss`/`subss` pair | — |

**29 real arms and 3 unimplemented** (56, 58, 59).

### The thirteen float commands address one array

Their targets are consecutive 4-byte floats:

```
02CB80B0 B4 B8 BC C0 C4 C8 CC D0   <- ids 63..71, nine in an unbroken run
        ... D4 D8 DC E0 E4 not reached by this slice (5 slots, 0x18 bytes) ...
02CB80E8 EC F0 F4                  <- ids 72..75
```

**Nine consecutive floats, a five-slot gap, then four more.** The gap is a fact about the layout and
**not** evidence that the skipped slots are unused — no id in this slice reaches them, and slices C–I
have not been read.

> **Resolved by slice C, 2026-09-03.** Ids 90–94 own exactly those five slots, and ids 95–98 own four
> more below `02CB80B0`. **Ids 63–98 map one-to-one onto 36 consecutive floats from `02CB80A0` to
> `02CB812C` with no gap larger than 4 bytes** — see
> [slice C](arm-catalogue-slice-C-ids-76-107.md) §4. The array was never sparse; the id order simply
> does not follow the address order. **Two corrections to this document fall out:** the gap is five
> slots, not six — `(0x02CB80E8 − 0x02CB80D0) / 4 − 1 = 5`, an off-by-one between the 0x18-byte
> distance and the count of slots strictly inside it — and the run of nine is not the array's start.

Two of the thirteen step by `0.001` (ids 67 and 69) where the other eleven step
by `0.01`; those two sit at `02CB80C0` and `02CB80C8`, which are **not** adjacent, so the finer step
does not correspond to a contiguous sub-range.

### Every stepping arm carries both directions

No arm in this slice has "a step". Each has a magnitude and a mechanism that applies it in either
direction:

```asm
movss xmm0, [02CB80B0]        ; the parameter
test  bl, bl                  ; the direction flag, from arg 2
subss xmm0, [+0.01]           ; one path
addss xmm0, [+0.01]           ; the other path, same constant
```

**All 13 float arms have the `addss`/`subss` pair on the same constant**, and the integer arms use
`inc`/`dec` or `cmov` between `+1` and `-1`. So **the command id names the parameter, never the
direction** — which is why a per-arm "step" column cannot be signed, and why this catalogue records
magnitude and mechanism separately.

## 4. Modding notes

- **`02CB80B0`–`02CB80F4` is the slider bank.** One hook there sees thirteen tuning values that a
  developer adjusted by hand; the array is in `.data` BSS, so it holds no value in the file.
- **The direction is the caller's**, not the console's. Driving this console externally means
  supplying arg 2, not finding a global to flip.
- **Three ids in this range do nothing** — 56, 58 and 59.

## 5. What is not known

- [x] **UQ-8.** ~~**What any of the thirteen floats is.**~~ **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): hair and eye
      lighting tuning values that nothing outside the console reads.**
      - **What they are.** Their own console labels ([console command names](console-command-names.md), ids
        63–75) name them. Ids 63–65 are *Hair Camera Light Direction X/Y/Z Bias*. Ids 66–71 are *Hair Specular
        Power Modifier* and the specular power and intensity *Modifier* / *Eye-Camera Distance Factor*
        pairs; the two distance factors, 67 and 69, are the ones stepped at `0.001`. Ids 72–75 are *Eye Type A
        Camera Light Direction X/Y/Z Bias* and *Eye Type A Specular Power Modifier*.
      - **What they control in this build: nothing outside the console.** Three routes are closed:
        - rip-relative: every access to `02CB80B0`–`02CB80F4` is in the menu renderer `001CD0E0`, which
          prints them, or the console arm `001D1660`, which steps them;
        - a register-held base: no `lea` anywhere in `02CB8000`–`02CB8120`;
        - a stored or image-relative pointer: no 8-byte or 4-byte-RVA value for any address in the block,
          anywhere in the file.

        The scene-config loaders `001C3D50` / `001C7940` write only the neighbouring gap slots `02CB80D4`,
        `02CB80D8` and `02CB80E4`, none of the thirteen. Whatever the shipped renderer uses for hair and
        eye lighting, it is not these cells: the knobs are console-only.
      *Original text:* They are an array of tuning parameters with known step
      sizes and no traced consumer. **None was followed to a reader.**
      **MEASURED 2026-09-16 (FABLE): these slots have no consumer, and the neighbouring slots prove that is a fact about them rather than a tracing failure.** Re-run over **all 38,161 listed bodies** by **overlapping byte ranges**, not exact displacements - so a wide or SSE load covering a float could not hide - across `02CB8000`–`02CB8120`. **68 slots are touched. 41 of them are touched by nothing but the console pair** - the menu renderer `001CD0E0` reads, the arm `001D1660` reads and writes - **and 27 have a genuine outside consumer.** **The consumers are named and concentrated:** `001C3D50` and `001C7940` together take 19 slots (`02CB8044`–`02CB8060`, `02CB80A0`–`02CB80AC`, `02CB80D4`, `02CB80D8`, `02CB80E4`, `02CB8104`), `001A97F0` takes three (`02CB8088`, `02CB8090`, `02CB8094`), `02CB8084` is read by a cluster of five (`00186130`, `00186410`, `00186CD0`, `00187950`, `00188DA0`), and `02CB8064` by `001A2130`/`001A5B00`. *(`001C3D50` is the scene-config loader SWE2-FRONTIER is documenting; these 19 slots are its registration surface.)* **So the block IS consumed - just not here.** `02CB80B0`–`02CB80D0`, which holds this slice's floats including id 67's `02CB80C0` and id 69's `02CB80C8`, falls **entirely inside the console-only set**, while `02CB80D4` and `02CB80D8` immediately after it do not. **That changes what *no traced consumer* means.** It is not that tracing fell short: in a block where 27 slots are read by scene-config loaders, **these are read by nothing but the menu that displays them.** The tracing is exhausted, and no further static work on this image will find a reader. *Bounds.* This is a **rip-relative** census. A consumer reaching these floats through a **register-held base** - `lea rcx, [02CB8000]` then `[rcx + 0xC0]` - would not appear, and that is a real shape, not a theoretical one. So: **no rip-relative consumer exists**, which is stronger than the previous wording and still not the same as *nothing reads them*.
- [x] ~~What occupies `02CB80D4`–`02CB80E4`, the six slots the id run skips.~~ **Closed by slice C:
      five slots, owned by ids 90–94.**
- [x] **UQ-9.** Why ids 67 and 69 step ten times finer than their neighbours. *(NO ADMISSIBLE SOURCE, reviewed and signed 2026-09-26 by OPUS; see the register row UQ-9.)*
      *Narrowed 2026-09-14 (FABLE), not answered: the fine steps follow the labels.* The two `0.001` arms are exactly the two
      *"Eye-Camera Distance Factor"* parameters in this slice: id 67 *"Hair Specular Power Eye-Camera Distance Factor"*
      (`02CB80C0`) and id 69 *"Hair Specular Intensity Before Clamp Eye-Camera Distance Factor"* (`02CB80C8`). Their `0.01`
      neighbours 66, 68 and 70 are the matching *"Modifier"* parameters ([names](console-command-names.md)). A factor
      multiplied by a camera distance plausibly needs the finer step. That is a reading of the labels; the only traced
      references to `02CB80C0`/`02CB80C8` are console-boundary functions — `001D1660` reads and writes each (the
      set/get arms for ids 67 and 69) and `001CD0E0` reads each — so no consumer outside the console's own input
      boundary was traced to confirm the scale.
- [x] ~~**Who calls the console** and therefore supplies the direction flag and the settings object.~~
      **Answered 2026-09-14 (FABLE), from the parent page's reachability answer:** one way in. `001CD040` sets
      `r8b = (dl == 0)` and tail-jumps to `001D1660` (`001CD049`). Its only call site is `0017DD34` in `0017DB90`, which
      the Config screen's two row procedures call (`0023B3D0`, `0023B84C`), with the object from `001D50D0` and a
      literal id. Only **16** ids are issued that way (`0x86`, `0xA6`, `0x10A`, `0x110`–`0x119`, `0x11B`–`0x11D`),
      and none of this slice's ids (44–75) is among them
      ([the 282-command console](the-282-command-parameter-console.md) §7). `001D50D0` returns it: a `0x10E8`-byte singleton built on first use by `001CCB20` and cached at `01F81428` (`001D50DD`–`001D5106`). The same object carries the console's labels at `+0x130 + 8 × id`, which `001CCB20` clears (`001CCE6F`) before `001D0390` fills them (`001CCEA4`). `001D1660` receives it through `001CD040`'s pass-through `rcx` (the steal page's `FK-3`, [the steal roll](../../08-Combat-Formula/Steal/the-steal-roll.md)).
- [x] **UQ-10.** The 16 "other" arms in this slice, which call helpers without touching an `rdi` field.
      **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): they do touch fields, just not the console object's own.**
      The count comes first: the table above marks **twelve** arms `other`, not sixteen, and nothing here
      reproduces the 16. Each of the twelve was decoded from its table entry to its `jmp` back to the console's
      common tail, and each label comes from [console-command-names](console-command-names.md).

      | id | label | what the arm does |
      |---:|---|---|
      | 45 | HBAO Full Resolution | toggles byte `+0x1E8` of the render-parameter block `00193D50()` (`001D4AC5`–`001D4AD4`) |
      | 46 | HBAO Depth Full Res | reads that block's `+0x1E9` and passes the negation to its setter `00193F70` (`001D4AF9`) |
      | 47 | early AO | `00182FD0(!0017FE10())` — a getter/setter pair (`001D1E0E`–`001D1E20`) |
      | 48 | Post AA enable | toggles the render-parameter block's `+0x3E8` (`001D1E2F`–`001D1E3E`) |
      | 49 | SMAA level | steps the render-parameter block's dword `+0x184` (`001D1E6D`–`001D1E7F`) |
      | 50 | Mask Border | toggles the render-parameter block's `+0x498` (`001D1E4E`–`001D1E5D`) |
      | 51 | Draw Chr Names | `001D5230(001C2F40(), direction bit)` (`001D18CA`–`001D18D6`) |
      | 52 | Draw UI WithOut Scale | `00184660(!001B1620())` — a getter/setter pair (`001D1F46`–`001D1F50`) |
      | 55 | Toggle cube map probes mode | fetches the `001AD440` object and calls the folded `ret` stub `0016D6A0` on it: **does nothing** (`001D3A2A`–`001D3A40`) |
      | 57 | Operate cube map | steps that object's `+0x168` through `001AD4D0` (`001D3A5F`–`001D3A72`) |
      | 61 | Camera Light enable | toggles the global byte `01DFE192` (`001D213D`–`001D2144`) |
      | 62 | After Water fix enable | toggles the console object's **own** `+0x10D9` (`001D2150`–`001D215A`); the table row says so, so it is not an "other" arm |

      So the class is *"acts on another object's field through its getter"*. Five of the twelve reach the
      render-parameter block, which is where [CF-5](../../_index/OPEN-QUESTIONS.md)'s split of the renderer tuning
      lives. One is a retired command.

## 6. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The id → arm mapping for all 32 ids | dwords at `001D4C1C + (id−12)×4`, `+0x00120000` | 1 |
| The console's argument roles and the `0x119` id bound | complete decode of the prologue at `001D1660` | 1 |
| Every float arm's target, magnitude and paired mechanism | each arm decoded from its table target to the start of the next arm | 1 |
| 3 unimplemented ids | those entries resolve to `001D4BFA` | 1 |

**Disposition of the `verify_doc_addresses` review flag.** `001D4C1C` is cited as a `.text` address
that is not a function entry. **Confirmed legitimate:** it is the dispatch table — a jump table in
`.text` after the console function, which is the case the checker asks to have confirmed. Every arm
address here is an interior address of that same function for the same reason: switch arms are not
functions.

**Method note.** Each arm is bounded by **the next arm's start address**, not by its first
`jmp 001D4BFA`. `001D4BFA` is both the unimplemented-id target *and* the common tail that most real
arms jump to, so a walk that stops at the first such jump reads only one branch — which is exactly
how a stepping arm loses half of its direction mechanism. The first version of the slice A catalogue
was extracted that way and has been re-run.

## 7. Related

- [the-282-command-parameter-console.md](the-282-command-parameter-console.md) — the frame
- [ARM-CATALOGUE-WORK-DIVISION.md](ARM-CATALOGUE-WORK-DIVISION.md) — the division and its rules
- [arm-catalogue-slice-A-ids-12-43.md](arm-catalogue-slice-A-ids-12-43.md) — ids 12–43, the counter
  and toggle end of the same table

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

**This slice's value in the catalogue is as a control.** It contains **zero** instances of the third
direction mechanism (`addss`/`addss` with a stored negative), against 25 in slice D and 21 in slice E.
**A mechanism found in two slices and absent from a third read by the same method is a property of the
commands, not of the reader** — without B and C clean, D's 25 would have been indistinguishable from
an extractor artefact.


*(Pass 22 adjacency, 2026-09-14: this slice's crossings are the shared dispatcher's, repeated
here because every slice cites `001D1660` — it calls the **presentation** materializers
`001D5120`/`001C7360`/`001C7520`, reaches **audio** `002DEBA0`/`001DBB00`, and fetches
through **resource** `002EEEE0`. The console lives on the render path and pulls its row content
through resource/audio helpers; the edges belong to the dispatcher, not to this slice's arms.)*

*(Pass 22 live-graph completion, 2026-09-15: `001D50D0` is called by `Input` bodies
`00197800`/`00197160`/`00197790` (3), and `001CCB20` calls `Platform` `005CC930` (1) — the
same shared-accessor and arm shape as the sibling slices.)*

*(Pass 22 live-graph sweep 2, 2026-09-15: `005CC930` is called by `Application` `00799980`
(1 edge) — same platform-leg shape as slice A.)*

## SWE2-EC7-49 update (2026-09-19) - `00188DA0`

`00188DA0` (192 B) is a body - `00193D50`/`001EE180`/`001F16C0`/`00610330` plus a `call [rax+0x10]` vcall. Interior anchor `00188DB4` (an `00193D50` call).

## SWE2-EC7-49 update (2026-09-19) - `001A97F0`

`001A97F0` (190 B) is a body - `001867B0`/`00189120`/`001AC720`/`001AD440`. Interior anchor `001A9804` (an `001867B0` call).

## SWE2-EC7-109 update (2026-09-20) - `001EF520` measured

`001EF520` (21 B) is the
flag-plus-pair setter
`001D1660` and `001D5120` call:
`byte[rcx + 0xAFE] = 1`,
`dword[rcx + 0xB00] = edx`,
`dword[rcx + 0xB04] = r8d` -
the three-field arm the tuning
verbs post.
Interior anchor `001EF527` (the
`+0xB00` store).

## SWE2-EC7-110 update (2026-09-20) - `001BD940` measured

`001BD940` (138 B) is the
dual-channel float apply
`001D1660` and `001D5120`
run: `001DE540(01F82D20)`
produces the mod-5 table value
into `xmm6`, then each channel
repeats - `0062BA00(rcx +
0xD0)`, a `dword[+0xEC] >> 7`
bit-0 test that skips the
`[+0xDC] = xmm6` store when
armed, and `0061D9C0(rcx +
0xD0)`; the `+0x80`/`+0x9C`/
`+0x8C` half mirrors it and the
tail `0061D9C0(rcx + 0x80)`
closes. Bit 7 of the channel
flag word is the write
inhibit.
Interior anchor `001BD973`
(the `shr eax, 7` inhibit
test).

## SWE2-EC7-111 update (2026-09-20) - `001A5B00` measured

`001A5B00` (38 B) is the
flag setter `001D1660` and
`001D5120` run:
`dword[+0x2F8] = edx`
always; `edx == 0` clears
`byte[+0x2E5]` and the shared
`02CB8064` byte, nonzero arms
`+0x2E5` to 1 and still
clears `02CB8064` - the
global byte is a one-shot the
setter always consumes.
Interior anchor `001A5B17`
(the `+0x2E5` arm).

`0018AC50` (175 B) is the
two-pass float apply
`001D1660` and `001D5120`
run alongside `001BD940`:
`xmm6` takes the same
`001DE540(01F82D20)` mod-5
value, then two outer passes
(`rbp = rcx + 0x20` and
`rcx + 0x60`) each run the
four-element inner block at
`rsi == 1` - per qword
element `0062BA00`, the
`dword[+0x1C] >> 7` bit-0
inhibit gate skips the
`[+0xC] = xmm6` store when
armed, and `0061D9C0`
closes. Eight elements total,
same write-inhibit convention
as `001BD940`'s channel
pairs.
Interior anchor `0018ACAE`
(the `shr eax, 7` inhibit
test).

`00189520` (11 B) is the
two-field arm `001D1660`
and `001D5120` run:
`byte[rcx + 1] = 1`,
`dword[rcx + 0xDC8] = edx` -
the smallest setter in the
family.
Interior anchor `00189524`
(the `+0xDC8` store).

## SWE2-EC7-112 update (2026-09-20) - `0062BA00` measured

`0062BA00` (47 B) is the
release-and-uninhibit step
`0018AC50` and `001BD940`
run per element (`006104E0`,
`0064AD60`, `0065D2A0` call it
too): a non-null
`qword[+0x20]` object takes
its `call qword[obj + 0x10]`
vtable release, the field
zeroes, and
`dword[+0x1C] &= ~0x80`
clears bit 7 - the same bit
`0018AC50`'s `>>7` test reads
as the float-write inhibit.
The clear is unconditional;
the release only runs when
`+0x20` is live.
Interior anchor `0062BA20`
(the `+0x1C` bit-7 clear).

`00184660` (40 B) is the
`cl`-indexed fan-out
`001D1660` and `0022A0B0`
run: the byte is captured in
`bl`, `001B24B0()` runs first
with its result dropped, then
`0024B120(bl)` and
`00248410(bl)` take the byte
and the tail jumps `0024B100`
- one slot byte driving three
downstream calls.
Interior anchor `00184671`
(the `0024B120` call).
`0022A0B0`'s own fan-out is
mechanical and recorded here:
it reaches the ActorEntity
and RNG_Random_Selection
domains - shared-service
edges, not catalogue
subjects.

`001AC390` (227 B) is the collection index-set the `001D1660` dispatcher runs for index `edx`: over the `([+0xE8]+8 - [+0xE8]) >> 3` records of the pointer vector it clamps each record's element count `(+8 - +0) / 0x18`, writes `edx` into `+0x44` when `0 <= edx < count` (clamped to `0` otherwise), and returns `edx` - or `count - 1` when the index overshoots a record's own bounds

Interior anchor `001AC405` (function `001AC390`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **ActorEntity — SERVICE (1 edge).** 1 outbound (page-cited `0022A0B0` call ActorEntity bodies `BattleStorage_InitializeWorkArrays` (002368D0)). Substantive edges include `0022A0B0` calls `BattleStorage_InitializeWorkArrays` (002368D0).
- **Input — CLIENT and SERVICE (15 edges).** 9 inbound (Input bodies `InputManager_PollAndBuildControlState` (00196FF0), `001E0DA0`, `001E0E70` call page-cited `001D50D0`, `005CC930`, `InputManager_TranslateBindingProfileToControlState` (00197160)); 6 outbound (page-cited `InputManager_TranslateBindingProfileToControlState` (00197160), `0022A0B0` call Input bodies `InputBackend_IsControlCode28To283ActiveForBank` (0079E6A0), `InputBackend_IsControlCode11To27ActiveAnyDevice` (0079E650), `InputBackend_IsPrimaryControlCode1To3Active` (0079E6D0)). Substantive edges include `InputManager_TranslateBindingProfileToControlState` (00197160) is called by `InputManager_PollAndBuildControlState` (00196FF0); `InputManager_TranslateBindingProfileToControlState` (00197160) calls `InputBackend_IsControlCode28To283ActiveForBank` (0079E6A0); `InputManager_TranslateBindingProfileToControlState` (00197160) calls `InputBackend_IsControlCode11To27ActiveAnyDevice` (0079E650); `InputManager_TranslateBindingProfileToControlState` (00197160) calls `InputBackend_IsPrimaryControlCode1To3Active` (0079E6D0).
- **Platform — CLIENT and SERVICE (3 edges).** 1 inbound (Platform bodies `00625830` call page-cited `0061D9C0`); 2 outbound (page-cited `001CCB20`, `00799980` call Platform bodies `005CC930`). Substantive edges include `001CCB20` calls `005CC930`; `0061D9C0` is called by `00625830`; `00799980` calls `005CC930`.
- **PlatformOnlineAchievements — SERVICE (1 edge).** 1 outbound (page-cited `001CD0E0` call PlatformOnlineAchievements bodies `003166F0`). Substantive edges include `001CD0E0` calls `003166F0`.
- **RNG_Random_Selection — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_Seed` (00379CF0)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **UI — CLIENT (1 edge).** 1 inbound (UI bodies `0018EEE0` call page-cited `001867B0`). Substantive edges include `001867B0` is called by `0018EEE0`.
- **World — SERVICE (1 edge).** 1 outbound (page-cited `0022A0B0` call World bodies `00266D10`). Substantive edges include `0022A0B0` calls `00266D10`.
- **WorldAreaField — CLIENT and SERVICE (3 edges).** 1 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020) call page-cited `002DEBA0`); 2 outbound (page-cited `001CD0E0` call WorldAreaField bodies `WorldTransition_GetTransitionFieldId` (00314910), `FieldData_GetVariable0` (00265270)). Substantive edges include `001CD0E0` calls `WorldTransition_GetTransitionFieldId` (00314910); `001CD0E0` calls `FieldData_GetVariable0` (00265270); `002DEBA0` is called by `World_UpdateSimulationTick` (00314020).
