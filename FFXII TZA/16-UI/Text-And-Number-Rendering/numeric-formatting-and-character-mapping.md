---
system: Numeric formatting and glyph advance layout
category: 16-UI
status: DOCUMENTED — on-screen column parity (AC-10, answered 2026-09-17 - digits are monospaced by construction) and the written fields' meanings (UQ-173, answered 2026-09-26 - all seven placed, the counters count characters) are answered, re-read 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13) (was — on-screen column parity and the written fields' meanings (UQ-173) are open); the cluster (UQ-383) answered 2026-09-18: the message and selection window's text engine, its Audio doors the row draw and the animation; the 61-loop dispatch (UQ-170) answered 2026-09-17; recursion termination (UQ-172) answered 2026-09-18: cursor progress and span cutting, no depth counter; the 0x14 counter and the +0x1102 flag (UQ-168) answered 2026-09-18: glyphs per draw packet, and the measurer's top-level latch; the 00916560 table (UQ-176) answered 2026-09-18: the `9` escape's translation bytes, authored by no shipped text; the Audio-entry box ticked on its 2026-09-15 answer (owner re-status 2026-10-01, OPUS; documented_rule READY)
owner_layer: none yet — every function here is in the unresolved residual
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `001E9D20`, `002A4430`, `002A4830`, `002AF960`, `002AFDC0`, `002B2DF0`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# Numeric formatting and character mapping

> How the game turns a number into characters, and maps each one before it is measured.

> **The original subtitle — *"why the digits never jitter"* — was withdrawn on 2026-09-02.**
> That story was wrong; see section 10. The retraction is kept visible because the claim was
> this document's headline and a reader may have carried it away.

**This document is ~~`PARTIAL`~~ `DOCUMENTED` *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`)* and is the first system recovered from
[the unresolved residual](../../99-Unresolved-Residual/the-unresolved-158.md).** Four of the
thirteen functions in its cluster have been read. The mechanism below is evidenced; the boundaries
of the system are not yet drawn.
*Note 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13): every member of the cluster now has a reading, and its doors are
traced (UQ-383 answered 2026-09-18, §7); what is still open on this page is listed in §15.*

## 1. What the player sees

Every number the game draws: damage and healing figures, HP and MP, gil, item quantities, License
Points, timers. They appear constantly and nobody thinks about them — which is the point.

> **Withdrawn 2026-09-02.** This section previously claimed digits are laid out at the fixed width
> of the character `0`, so that counting numbers do not jitter. **Disassembly disproves it** — the
> table involved holds character *codes*, not advance widths, and the `'0'` lookup happens *inside*
> the per-character loop. See section 10. Nothing has been put in its place, because nothing about
> on-screen digit spacing has been established.

What *is* established is upstream of pixels: the game converts a number into characters by repeated
subtraction of powers of ten, pads it to a minimum width, and maps each resulting character through
a translation table before handing it on to be measured and drawn. Whether that produces even digit
columns on screen is **not known** — the measuring happens in a function this document has not
read.

## 2. Native mechanism

### Step 1 — the number becomes digits

`002AE610` converts an integer to characters by **repeated subtraction of powers of ten**, using a
table of exactly that at `00916520`:

```
00916520:  1  10  100  1000  10000  100000  1000000  10000000  100000000
```

```c
if (POW10[*param_4] <= v) {
    do {
        v -= POW10[*param_4];
        ...
    } while (POW10[*param_4] <= v);
}
```

`*param_4` carries the **digit position**, and is clamped to a minimum:

```c
if ((int)uVar10 < (int)((char)param_1[0x13] + 1)) uVar10 = (char)param_1[0x13] + 1;
*param_4 = uVar10;
```

so `param_1[0x13]` — a **qword index**, byte offset `+0x98` (`002AE89C movsx eax, byte [rdi+0x98]`) — is a **minimum field width** — the setting behind leading zeros and fixed-width
counters. The digits land in a **16-byte stack buffer** (`char local_b8[16]`), formatted through
`003EFD00(buffer, param_1+0x54, digitCount, flags)`.

### Step 2 — each character is mapped to a character code

The buffer is walked one character at a time, each indexing a **16-bit translation table**:

```
002AE926  movsx rax, byte ptr [r12]        ; ch = *p
002AE92B  sub  rax, 0x20                   ; ch - 0x20
002AE931  movzx ecx, word ptr [r9+rax*2]   ; code = TABLE[ch - 0x20]
002AE936  test cx, cx / jne
002AE956  lea  eax, [rcx-0x20] / cmp ax, 0xDF / ja
002AE95F  mov  byte ptr [rsp+0x30], cl     ; store ONE byte  ...
002AE96D  mov  word ptr [rsp+0x30], cx     ; ... or TWO
```

The table is indexed by `character - 0x20` with `ushort` entries, and entry 0 is the space
character — that much was right. **But the value is not an advance width.** It is stored back out as
**character data** into a small stack buffer, NUL-terminated, and the buffer's address is then
passed to `002A9F00`:

```
002AE998  lea  rax, [rsp+0x30]
002AE9A6  mov  qword ptr [rsp+0x60], rax
002AE9FC  call 0x2a9f00                    ; <- the buffer goes here
```

The `cmp ax, 0xDF / ja` test chooses a one-byte or two-byte store, which is the shape of a
**multi-byte character encoding** decision, not of a width lookup.

### Step 3 — the `'0'` entry is a padding character, not a width

```
002AE97A  dec  bl                          ; counter--
002AE97C  cmp  al, 1        / jne  skip
002AE980  cmp  bl, dl       / jg   skip
002AE984  movzx eax, word ptr [r9+0x20]    ; the entry for '0'
002AE989  mov  word ptr [rsp+0x30], ax     ; OVERWRITE the output buffer
```

The arithmetic identifying the entry still holds: byte offset `0x20` is entry 16, character
`0x20 + 16 = 0x30` — `'0'`. But what the code does with it is **overwrite the character being
emitted**, under a condition involving a decrementing counter `bl` and a threshold `dl`. That is
**digit padding** — substituting the character `'0'` — and it is consistent with the minimum-width
clamp in step 1.

**It is not hoisted out of any loop.** `002AEA96 jl 0x2ae920` jumps back to `002AE920`: the read at
`002AE984` is *inside* the per-character loop body.

### Step 3 — the fixed-digit-width trick

Immediately before the walk, the routine reads **one specific entry**:

```c
local_1d8._0_3_ = (uint3)*(ushort *)(glyphTable + 0x20);
```

Byte offset `0x20` is entry `0x20 / 2 = 16`, which is character `0x20 + 16 = 0x30` — **the digit
`0`**. It is fetched once, outside the per-character loop, and used as the advance for digits
instead of each digit's own entry.

**That single lookup is why numbers do not jitter.**

### Step 4 — the pen advances in floats

Advances accumulate into a caller-supplied float array:

```
002AEA4C  addss xmm6, xmm8
002AEA51  movaps xmm1, xmm8
002AEA55  addss xmm1, dword ptr [rsi]
002AEA59  movss dword ptr [rsi], xmm1      ; pen += xmm8
```

The accumulated quantity is `xmm8`, produced **after** the call to `002A9F00` — so the per-character
advance comes from that callee, not from the translation table.

`param_3` is four floats — `param_3[0..3]` are all read — consistent with a pen position plus
extent, though only `[0]` is confirmed as the accumulator. The measured result is written back to
the state block at `param_1 + 0x14`:

```c
*(float *)((longlong)param_1 + 0x14) = fVar20 - fVar19;
```

### The shared 208-byte state block

Every function so far read in this cluster begins by copying **the same 26-quadword (208-byte)
structure** out of its first argument onto the stack — `002AE610` and `002B2DF0` both copy
`param_1[0]` through `param_1[0x19]`. Known fields:

| Offset | Type | Role |
|---|---|---|
| `+0x98` (byte) | `char` | **minimum digit count** — field width, less one (`param_1[0x13]` in the qword-indexed pseudocode; corrected 2026-09-18, SWE2-STRUCT) |
| `+0x14` | `float` | measured extent, written back |
| `+0x44` | `uint` | flags; **bit 11** selects a target via `0039C4A0` |
| `+0x54` | `undefined4` | format argument passed to `003EFD00` |
| `+0xA1`, `+0xA2` | `byte` | a pair compared against each other to gate a branch |
| `+0x9F` | `byte` | the glyph-command nibble source **when `+0xB0` bit 21 is CLEAR** (`002AA191`) — *added 2026-09-15 (OPUS)* |
| `+0xA7` | `char` **signed** | index into the `00916560` byte table **when `+0xB0` bit 21 is SET** (`002AA197`). **This is the cell §10 calls `state[+7]`** — *added 2026-09-15 (OPUS)* |
| `+0xB0` | `uint` | low byte is a **mode**, switched on in `002ABF70`. Labels are **0, 1, 2, 3, 4, 5, 7** — seven, with no `default` (corrected 2026-09-02). **And its low byte is not all of it: bit 21 is a ONE-SHOT FLAG.** `002AA188`–`002AA1AB` loads the dword, tests bit 21 with `bt ecx, 0x15`, and **clears it with `btr ecx, 0x15` before storing back**, so the bit selects the `00916560` path once and then disarms itself *(added 2026-09-15 (OPUS))* |

**The 208-byte block and the drawer-kind state are the same structure — 2026-09-15 (FABLE).** The two
were documented separately, from opposite ends: this section from functions that *copy* the block, §7
from functions that *build* one and stamp a kind on it. Four independent joins say they are one thing.

| join | here | §7 |
|---|---|---|
| **size** | 26 quadwords = **208 bytes** | `002B1FB0` zero-fills `mov r8d, 0xD0` = **208** (`002B1FE7` → `00861EC0`), and `002A4830` copies `0xD0` from `[window + 0xD0]` |
| **`+0x44` bit 11** | *"flags; bit 11 selects a target via `0039C4A0`"* | `002B3400` does exactly that — `002B343D` `or [rdi+0x44], 0x800`, then `0039C4A0`, then `002B3452` `mov [rdi+0x60], rax`. **So `+0x60` is where that target is stored**, which this table did not have |
| **`+0x54`** | *"format argument passed to `003EFD00`"* | `002A4830` writes it at `002A49D9` from the record field `+0x1C` |
| **`+0x9F` / `+0xB0`** | added by OPUS from `002A9F00` | `002A9F00` is **slot 2 of kind 0** in the same table §7 decodes |

**Eight more fields, each with a writer and, where stated, a reader.** All sites read from the shipping
image; nothing below is named from adjacency.

| Offset | Type | Role |
|---|---|---|
| `+0x04` | `float` | written from an integer accumulator — `002A4A0D` `movss [rbx+4], xmm0`, `xmm0 = cvtdq2ps(esi)`, and `esi` advances by the record field `+0x24` each iteration |
| `+0x20` | pointer | `002A4950` `mov [rbx+0x20], r13`; `002D861C` `mov [rbp+0x20], rax` where `rax` is the block `003659F0`/`00397910` just filled. **The glyph-run page independently reads `state + 0x20` as the 4×4 transform pointer, null-checked before use** |
| `+0x28` | pointer | **the string.** Written by every initialiser — `002B3C39` (`002B3C30`), `002B3460` (`002B3400`), `002A4A4D` / `002A4A5B` (`002A4830`) — and **read as the `ex`-prefix test's argument** at `002D8720` and `002D8860`, which load `[r9 + 0x28]` and pass it to `00364980` |
| `+0x30` | `dword` | a **modulated 4-byte tuple**: bytes `[font+0x90..0x92]` each scaled by `word [font+0x5A]` and `>> 7`, byte `[font+0x93]` scaled by `word [font+0x58]`, packed into one dword and stored to **both** `[font+0x94]` and here. Two bodies compute it identically — `002A4967`–`002A49BF` and `002D857D`–`002D85D4`. **Three components by one scalar and the fourth by another is the shape of a colour with separate alpha**, though nothing read here shows it reaching a vertex |
| `+0x60` | pointer | the `0039C4A0` target selected by `+0x44` bit 11 — `002B3452`; `002A4830` instead takes it from the record at `002A4A09` |
| `+0x8C` | `word` | set to **`0x7D00` (32,000)** by two initialisers — `002A49C2` and `002B3469`. **This is the field both column-1 dispatchers publish**: `002ABF20` and `002ABEC0` `movsx` it and store it into `[0209CC40] + 0x10D8` before tail-jumping |
| `+0xA3` | `char` **signed** | **the drawer kind** — §7 |
| `+0xA6` | `byte` | written by both initialisers — `002A49E5` from the record field `+0x20`, `002B3425` from `0039BAD0`'s return. **`002B3434` compares it against `7`**, so 7 is a distinguished value; what it means is not read *(read 2026-09-30, DD batch 13, §15 N1: the byte is the glyph sheet's slot, 1–7, in the seven-slot font registry `02AEE810`, and 7 is the alternate sheet `fontVariant[7]`, which installs the alternate pointer `[02AEE808]` and sets `+0x44` bit 11)* |
| `+0xB8` | `qword` | `002D860E` `mov qword [rbp+0xB8], 0x3001` — one literal, set immediately before the slot-2 dispatch; what it selects is not read *(read 2026-09-30, DD batch 13, §15 N2: it is the glyph run's pixel-test word, emitted as the data of command code `0x47`; the three helpers write `0x3001`, the initialisers `0x30000`)* |

~~**`UQ-164` is `PARTIAL`, not answered.** What the block is *called* is still unknown,~~ **`UQ-164` is CLOSED
(2026-09-18, SWE2-STRUCT): the map is complete and the name is unrecoverable, §7** *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13))*, and the census of
the remaining bytes is mechanical work that belongs to `SWE2-STRUCT`, not here — filed as
`FABLE-REQ-SWE2-STRUCT-TEXT-STATE-208-FIELD-MAP`. What this section now supplies is the thing that
made the census hard: **the readers and writers are in two families that looked unrelated**, the
`002Axxxx` / `002Bxxxx` initialisers and dispatchers and the `002D8xxx` draw helpers, and they are
working on one structure embedded in its owner at `+0xC0` (`00227EE0`), `+0xD0` (`002A4830`,
`002A1B00`) or `+0xE0` (`0057C480`).

## 3. Key addresses

Every one of these is currently **unresolved** in the GFZ ledger — no owner, no final-no, no code
domain. That is the significance of this document: a player-facing system was sitting in the
residual.

| Address | Size | Role |
|---|---:|---|
| `002AE610` | 1,281 B | **number → digits → glyph advances**; the routine documented above |
| `002AC5F0` | 7,489 B | the largest body in the game while it was residual — classified at GN162 as `UI.Text.ControlCodeInterpreter`; calls `002AE610` (`UI.Text.NumberToGlyphAdvances`) twice and submits render work |
| `002B2150` | 861 B | cluster hub; `(object, byte*, float*, float*)`; resolves authored-data pointers |
| `002B2DF0` | 598 B | 7-bit-masked walk of a NUL-terminated buffer, two float accumulators |
| `002ABF70` | 577 B | per-tick state machine over mode `+0xB0`; accumulator `+0x9B += +0x9C`, fires at 30 |
| `003EFD00` | 236 B | formats digits into the 16-byte buffer |
| `003FFC60` | 115 B | **not a resource accessor** — a six-parameter field decoder over a three-byte record; returns the constant `3` (**AC-8**, §7) |
| `0039C4A0` | 24 B | flag bit 11 → target selection |
| `00916520` | — | **the power-of-ten table** (`.rdata`) |
| `003A1DB0` | — | `RenderCommand_SubmitCurrentBufferAndSwap` — the Presentation exit |
| `002A6190` | — | object message handler; **9 labels: 1, 2, 3, 4, 10, 12, 15, 18, 21** + `default`. Case 1 registers, **case 4 updates** and enters the cluster |
| `0209C4D0` | — | **8-slot registry of live message windows** (`.data`), `0209C4D0`–`0209C50F`, the bound taken from `002A28E7` — *corrected from “actor registry” 2026-09-15 (FABLE), §7*; read by the four `InputGameplay_GetActorStateAwareRemappedMask*` |

## 4. Data structures and formulas

```
POW10[9] = { 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000 }   @ 00916520

charCode(ch)     = *(u16 *)(mapTable + (ch - 0x20) * 2)    // a CHARACTER CODE, not a width
                                                            // 1 byte if code-0x20 <= 0xDF, else 2
padCode          = *(u16 *)(mapTable + 0x20)                // the code for '0'; substituted
                                                            // in-loop when bl <= dl

digitCount       = max(naturalDigits, state[0x98] + 1)   // qword index 0x13 in the pseudocode
penX            += advance                              // float accumulation
state[0x14]      = measuredExtent
```

## 5. Call chain

```
Presentation.Rendering.ShaderMaterial (002B0280)  -.
Runtime.RealFunctionPointerOrVtableMember          |
Boundary.Audio.NativeSupport (002A6190, 005742D0) -+-> cluster doors
                                                   |
   002AC5F0  (7,489 B)  <====>  002B2150  (hub)  <-'
      |  \
      |   `-> 002B2DF0
      v
   002AE610 --> 003FFC60   three-byte record field decoder (NOT glyph metrics -- AC-8)
             -> 003EFD00   format digits
             -> POW10 @ 00916520
   002AC5F0  -> 003A1DB0   RenderCommand_SubmitCurrentBufferAndSwap
             -> Boundary.StoryEvent.NativeSupport x2
```

The cluster is entered from **Audio**, **ShaderMaterial** and **vtable dispatch**, and exits into
**Presentation** and **StoryEvent**. It is a cross-subsystem service, which is consistent with it
having no single `PrimaryOwner` — and is likely part of why it resisted classification.

**The two `Boundary.Audio.NativeSupport` doors are object message handlers**, not audio data paths.
Both have the signature `undefined8 f(longlong object, undefined4 *message)` and switch on
`*message`. `002A6190` enters the cluster from **case 4**, its per-frame update:

```c
case 4:
    flags = *(uint *)(object + 1000);
    if (((flags >> 0xB & 1) == 0) && ((flags >> 0xD & 1) == 0)) {
        if ((flags & 0x700) == 0)  FUN_002a4430(...);   // update path A
        else                       FUN_002a4830(object, ...);   // update path B
    }
```

So `002A4430` and `002A4830` are **two alternative per-frame update paths** chosen by flag bits 11,
13 and the `0x700` group. This is why an "Audio"-tagged function reaches a text-layout cluster: the
tag describes the handler's boundary, not the work it dispatches to.

## 6. Modding notes

- **The table at `r9` is a character-code map, not a font metric table.** `ushort` per character,
  indexed from `0x20`; a replacement must cover the same range in the same order. Entries above
  `0x20 + 0xDF` are emitted as two bytes, so it carries a multi-byte encoding.
- **Entry 16 (`'0'`) is the padding character.** Change it and padded numbers pad with something
  else — this affects the emitted *characters*, not their spacing.
- **Advance widths are not in this function.** They come from `002A9F00`, ~~which is unread~~ which §14 reads (AC-9
  answered 2026-09-12) *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13))*.
- `state[0x98] + 1` is the minimum digit count. It is where fixed-width counters come from.
- **Do not assume this is the only text path.** Only 4 of the cluster's 13 functions are read, and
  the cluster's other doors come from Audio, which this document does not explain. *(2026-09-30, DD batch 13: every
  member is now read and the Audio doors are the message window's row draw and its animation, UQ-383, §7.)*

## 7. What is not known

- [x] What the other nine functions in the cluster do. See **`UQ-383`** — *re-pointed 2026-09-15 (FABLE); this cited `AC-6`, which in the register is the unrelated census question.*
      ***ANSWERED 2026-09-18 (FABLE) — the cluster is the message and selection window's text engine, and the two Audio doors are that window's per-frame draw and its animation.** Every member now has a reading: six on 2026-09-03, five more placed on 2026-09-15, and the two doors read today. `002A4830` (1,701 B) **draws the window's rows**: for each of the `+0x3C2` records of the `0x28`-byte array at `0209C700` (the store's `TextLayoutRecord`) it copies the window's `+0xD0` draw block to the stack, scales the window's RGBA bytes `+0x90`..`+0x93` by the fade words `+0x58` / `+0x5A` (`imul`, `sar 7`; `002A4954`..`002A49B8`), takes the record's fields — `+0x08` to state `+0x60`, `+0x18` into flag `0x800`, `+0x1C` to `+0x54`, `+0x20` to `+0xA6` — lays the row at the pen y accumulated from each record's `+0x24` row height (`002A4A0D`, `002A4A12`), and draws its `+0x22` runs through `002B2930` / `002B2880` (`002A4A21`..`002A4A62`); the row whose index equals `+0x3C0` is the **cursor row** and takes the special arm at `002A4A67` (its `+0x10` text is what `0209C980` publishes). `002A4430` (1,020 B) is the **open / close / scroll animation** path: it tests the window word `+0xB0` for `0x20000000`, `0x40000000` and `0x100000`, steps with ~~the timing constants~~ `01E0CDAC` / `01E0CDB0` / `01E0CDB4` / `01E0CDBC` / `01E0CDC0` *(corrected 2026-09-27, FABLE, Claude Opus 5.5: not timing constants but the layout keys `MessageLineWordCount`, `MsgWinLogCursorOffsetX` / `Y`, `MsgWinSelectCursorOffsetY` and `FontBaseWidth`, which place the message-log cursor and the select pointer; Y-1, [`y1-layout-key-uses.tsv`](../../_index/candidates/y1-layout-key-uses/y1-layout-key-uses.tsv))* through `00244070` / `002B2D60` / `00368360`, and fills the line scratch `0209C630`. `002A6190`'s case 4 chooses between them by the flag bits §5 names. The four-field group is the window's list state, named by its writers: **`+0x3BE`** (word) the scroll offset `002A5020` returns (stored at `002A5E50` and `002A599B`, copied to `0209C61C` on every cursor move, `002A6132`); **`+0x3C0`** the cursor row — `002A5F40` moves it down or up on the input bits, bounded by `+0x3C1 − 1` (`002A60B6`..`002A6102`), and `002A5CC0` resets it to the last row (`002A5E2C`..`002A5E31`); **`+0x3C1`** the row total, `002A5CC0` summing each record's `+0x22` over the `+0x3C2` records plus one (`002A5DF3`..`002A5E1C`); **`+0x3C2`** the record count (`002A3250` increments it per added record, `002A2720` and `002A2C00` zero it, `00241D40` fixes it at 4); and **`+0x3C5`** the input-wait flag (`0x80` by `002A3730`, 0 by `002A38C0`, read by the four `InputGameplay_GetA*` getters and `002A6190`). So in player terms: a text window with selectable rows — the choice lists and menus built from text records — redrawn every frame with its fade and its highlighted cursor row, scrolled by the offset, animated open and closed, and moved by the pad. Static: the two door bodies, the field-group sweep (every access at `+0x3BE`..`+0x3C5`), the record array's uses.*
- [x] **UQ-164 — the map is complete; the name is unrecoverable.** What the 208-byte state block is
      called and what its remaining bytes hold. **2026-09-18 (SWE2-STRUCT): the full census is
      `text-draw-state-accesses.tsv`** — 1,022 sites across 52 bodies, seeded from the four
      initialisers, four dispatchers, five drawers, the draw helpers (block in `rcx` **or `r9`**),
      the three owner-embedding functions (`+0xC0`/`+0xD0`/`+0xE0`) and the stack-copy builders.
      Every byte of the `0xD0` extent is observed; `+0xC4..+0xCF` is copy-only tail. The type is
      declared **`TextDrawState`** (65 field rows) — a database name, not a recovered one: the
      initialisers memset and store fields but never install a vtable, so no RTTI/ctor name exists
      to recover. `FABLE-REQ-SWE2-STRUCT-TEXT-STATE-208-FIELD-MAP` is discharged.
- [x] Why **Audio** enters this cluster. *(Ticked 2026-10-01, OPUS: the box's own 2026-09-15 answer below closes it - the cluster carries text layout and the input layer's four getters ask it which button dismisses what is on screen.)* **ANSWERED IN PART 2026-09-02 — and the premise was
      wrong.** Both "Audio" callers are **object message handlers** (`switch (*param_2)` on an
      opcode), and they enter the cluster from their **per-frame update** case, not from anything
      audio-shaped. `002A6190` registers its object into an **8-slot registry** at `0209C4D0` — an
      array whose other readers are named `InputGameplay_GetActorStateAwareRemappedMask04/08/0C/10`.
      ~~So the cluster carries **actor per-frame update logic** as well as the text/number layout
      documented here. What remains open is how those two roles relate.~~

      **ANSWERED 2026-09-15 (FABLE): they are not two roles.** The cluster carries text layout; the
      **input** layer asks it a question. `002A28E0` — 89 bytes, and its three siblings are identical
      but for one tail call — reads as follows:

      ```asm
      002A28E0  lea   rcx, [rip + 0x1DF9BE9]        ; rcx = 0209C4D0, the registry
      002A28E7  lea   rdx, [rip + 0x1DF9C22]        ; rdx = 0209C510, the END - so the array is
      002A28F0  mov   rax, [rcx]                    ;   exactly 8 qwords and 0209C510 is the bound
      002A28F3  test  rax, rax / je                 ; empty slot -> next
      002A28F8  test  byte [rax + 0x40], 0x10 / je
      002A28FE  test  dword [rax + 0x3E8], 0x700    ; <-- the SAME field and mask as case 4
      002A2908  jne   002A2921                      ; -> xor eax, eax / ret      RETURN ZERO
      002A290A  cmp   byte [rax + 0x3C5], 0 / jl    ; -> 0x4000 or 0x2000 on [01FD4A64]
      002A2913  add   rcx, 8 / cmp rcx, rdx / jl    ; next slot
      002A291C  jmp   0036FF70                      ; none matched -> the ordinary remapped mask
      ```

      **So the four getters walk the registry of live message windows before returning a button
      mask.** The fallback `0036FF70`–`0036FFA0` family is `movzx eax, word [02AD9E04 + k×0x14]`, the
      plain remapped mask for that slot; the four differ from one another *only* in which of those
      they tail-call.

      **And what the `0x4000` / `0x2000` pair is — it is the confirm button.** The tail at `002A2924`
      is `cmp dword [01FD4A64], 0` / `mov eax, 0x4000` / `mov ecx, 0x2000` / `cmove eax, ecx`, so the
      getter returns `0x2000` when that flag is clear and `0x4000` when it is set. `0022A4F0`, in
      `Input`, is where those two values come from, and it was re-derived here rather than taken from
      the page that documents it:

      ```asm
      0022A4FB  mov   r8d, 0x4000
      0022A503  mov   ecx, 0x2000
      0022A50B  setne dl                       ; dl = (0017E210() != 0)
      0022A510  mov   [rip+…], edx             ; 01FD4A64  <- the cached swap flag
      0022A516  cmove ax, cx                   ; flag 0 -> ax = 0x2000
      0022A51A  cmove cx, r8w                  ; flag 0 -> cx = 0x4000
      0022A51F  mov   [rip+…], cx              ; 01E0C2A4
      0022A526  mov   [rip+…], ax              ; 01E0C2A0
      ```

      `01E0C2A0` is the **confirm** mask and `01E0C2A4` the **cancel** mask — established twice over, by
      [the keymap document](../../15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md)
      and by [the shared dialog widgets](../Shared-Dialogs/the-shared-dialog-widgets.md), where a hit on
      `01E0C2A0` posts `0x8001` and a hit on `01E0C2A4` posts `0x8002`. **`002A28E0`'s `cmove` produces
      exactly `ax`, which is `01E0C2A0`** — so the four getters answer *"which button confirms, given
      the player's current swap setting"*.

      **Which makes the whole family readable in one line.** Each getter answers **"what dismisses what
      is on screen right now"**: *nothing* (`0`) while a window with the `0x700` group is up, the
      **confirm** button while one has `byte [+0x3C5] < 0`, and otherwise the slot's ordinary remapped
      mask.

      **And what sets `+0x3C5`, which turns out to reach further than this subsystem — 2026-09-15
      (FABLE).** The byte is written at exactly **two** sites image-wide, out of eleven accesses
      (byte-width census through a non-`rip` base over all 34,270 listed bodies; the other nine are
      the four getters, `002A3565`, three in `002A5CC0` and one in `002A6190`):

      | site | writes | guard |
      |---|---|---|
      | `002A3781` in `002A3730` | **`0x80`** | `[window + 0x44] & 0x180000 == 0x180000` — *both* bits 19 and 20 |
      | `002A3928` in `002A38C0` | **`0`** | the same `0x180000` test, re-derived at `002A3915`–`002A391B` |

      **So it is a two-state byte, `0` or `0x80`**, which is why every reader tests its *sign*.

      **`002A38C0` is a sweep, not a per-window call.** It walks the whole registry — `002A38E7`
      `lea rbx, 0209C4D0`, `002A38EE` `lea rsi, 0209C510` as the bound — and for each live slot either
      calls `002A3730` to arm or writes `0` to disarm, on one `int` argument. It also caches that
      argument to `0209C62C` and calls `003EC830` when non-zero or `003EC810` when zero (18 bytes
      each). **Every live message window is switched together.**

      **And what decides it comes from the world tick.** `002A38C0`'s only caller is `002E09A0`, whose
      only caller is `00314020`; `002E09A0` opens by polling five slots and passes 1 if any answers
      non-zero:

      ```asm
      002E09C0  mov  ecx, ebx                  ; ebx = 0..4
      002E09C2  call 00267310                  ; movzx eax, byte [02099011 + ebx*0x288]
      002E09CE  jne  002E09DB                  ; any non-zero -> ecx = 1
      002E09D2  cmp  ebx, 5 / jl
      002E09D7  xor  ecx, ecx                  ; none -> 0
      002E09DD  call 002A38C0
      ```

      `00267310` and that byte are **already documented elsewhere**:
      [the world tick and the field frame](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
      reads `02099011 + slot × 0x288` as **`+0x201` of the actor-manager slot array, the sub-step
      opt-in** — the byte by which a slot asks to be simulated up to sixteen times in one frame, set by
      two ScriptVM commands.

      **So the chain is exact and it crosses three layers:** *any actor-manager slot opting into
      sub-stepping* → *every live message window marked `+0x3C5 = 0x80`* → *the four input getters
      return the confirm mask instead of the slot's ordinary one.*

      > **What is established is the coupling, not its purpose.** Every link above is a read
      > instruction or a call edge. **Why the sub-step opt-in should govern whether windows accept the
      > confirm button is not established here**, and the guard makes it narrower still: a window only
      > changes state at all when `[+0x44] & 0x180000` has *both* bits. Naming this *"fast-forward"*
      > would be reading the tick page's phrasing into a coupling that has not been watched run.
      > *2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13): runtime-only. Every link of the coupling is static; its
      > purpose is a design question, and watching a window while a slot sub-steps is what would show it.*

      **One duplication worth recording rather than tidying.** `0022A4F0` *stores* the confirm mask to
      `01E0C2A0`; `002A28E0` *recomputes* it from `01FD4A64` with the same `cmove` shape instead of
      reading it. **There are two sources of truth for which button confirms**, and they agree only
      while both sides keep reading the same flag. Nothing here is wrong — this is a note for whoever
      changes either one.

      **And the flag group is the one this document already knows.** `002A28FE` tests
      `[window + 0x3E8] & 0x700`; `002A631B`, in `002A6190`'s own case-4 update, tests the same field
      with the same mask to choose `002A4830` — the **kind-3** drawer — over `002A4430`. **One flag
      group, two consequences: a different text drawer, and a button mask of zero.** That is the whole
      relationship, and it runs one way: the window publishes its existence, and input reads it.

      **Consequence for the registry's name.** The objects in it are the ones `002A6190` stores, which
      are its own — `002A6236` `mov [rsi + rax*8 + 0x1F7C4D0], rdi` — and they are read here through
      `+0x40`, `+0x3E8` and `+0x3C5`, all message-window fields. **It is an 8-slot registry of live
      message windows**, not of actors; *"ActorStateAware"* is the input side's word for *aware of what
      is on screen*, and what it is aware of is a window. The array's extent is now exact rather than
      inferred from the scan: `0209C4D0` to `0209C50F`, bounded by the `lea` at `002A28E7`.

      **There are two eight-entry tables here, not one, and the cross-reference list hides it.**
      Fourteen bodies take the address of `0209C510`, and **they do not mean the same thing by it.**

      | use | sites | what `0209C510` is |
      |---|---|---|
      | as a **bound** | `002A28E7`, `002A2947`, `002A29A7`, `002A2A07`, `002A3F57` | the end of the window registry: `cmp rcx, rdx / jl` after `add rcx, 8` |
      | as a **base** | `002A3609`, `002A366D`, `002A385D`, `002A38EE`, `002A700E`, `002A7651`, `002A7962`, `002A79E6`, `002A7A43` | the start of a **different** array, indexed `shl rax, 5` — **32-byte records** |

      **`002A79E0` settles both sizes in one body**, and it is the subsystem's reset:
      `002A79F3` `memset(0209C510, 0, 0x100)` — **`0x100` = 256 = 8 × 32**, so the record array is also
      eight entries — followed by eight individual `mov [rip+…], rax` stores that zero
      `0209C4D0`, `…C4D8`, `…C4E0`, `…C4E8`, `…C4F0`, `…C4F8`, `…C500`, `…C508` (`002A79FA`–`002A7A2B`).
      **That is an independent second instrument on the registry's extent**: the walk bound said eight
      slots, and the reset zeroes exactly those eight and no ninth.

      **What the 32-byte records hold, from their two simplest users.** `002A7A40` clears bit 0 of
      `[rec + 0]` and passes `[rec + 8]` on to `0024A680`; `002A3600` looks a string up by id through
      `001814F0` and **copies it byte-by-byte into `[rec + 8]`**, guarded by `[rec + 8] != 0`. So
      `+0x00` is a flag word and **`+0x08` is a `char *` destination buffer**.

      **`002A3650` and `002A3830` bind a shared record to an owner's own slot**, and the two bases are
      worth keeping apart because the listing runs them together. The owner's slot is
      `r11 = [owner + 0x3F8] + idx × 0x60` (`002A384B`–`002A3856`, `lea r11,[rax+rax*2]` then
      `shl r11, 5`); the shared record is `rax = 0209C510 + k × 0x20` (`002A3864`–`002A3868`). Only one
      store crosses between them — `002A386B` `mov [r11], rax`, **the owner's record taking the shared
      record's address**. Every other write in those two bodies (`+0x14`, `+0x16`, `+0x08`, `+0x2F`,
      `+0x30`) is on **`r11`, the owner's `0x60`-byte slot**, not on the 32-byte shared record.

      **Stated as a limit rather than left implied:** neither indexer bounds-checks. `002A7A40` and
      `002A3600` both do `movsxd` then `shl …, 5` on a caller-supplied `int` with no comparison against
      8, so the eight-entry extent is a property of the callers, not of these bodies. And the record's
      field meanings above are read from two small users, **not censused** — the structure belongs with
      the 208-byte text state in `SWE2-STRUCT`'s queue, not in a reading.
- [x] **UQ-165 — ANSWERED 2026-09-18 (SWE2-STRUCT): pen confirmed; components [2] and [3] are
      carried-but-unread float4 payload.**
      Whether `param_3`'s four floats are pen-position-plus-extent or a rectangle.
      **Settled 2026-09-15 (FABLE): it is a pen.** Three uses in `002AE610` decide it, and a rectangle
      explains none of them.

      1. **`[0]` is advanced in place.** `002AEA4C`–`002AEA59`: `addss xmm1, [rsi]` then
         `movss [rsi], xmm1`, where `xmm1` began as `xmm8`, the per-character advance — so
         `param_3[0] += advance`, written back through the caller's pointer. A second path adds a
         further term at `002AEA67`–`002AEA7E`. **A rectangle's field is not incremented by a glyph
         advance.**
      2. **The function snapshots the whole float4 on entry and then differences against it.**
         `002AE993`–`002AE9C6` copy `[rsi+0]`, `[rsi+4]`, `[rsi+8]`, `[rsi+0xC]` into
         `[rbp+0x40]`, `[rbp+0x44]`, `[rbp+0x48]`, `[rbp+0x4C]` — in order, same stride, so it is one
         value object. Then `002AEA10` reloads the **entry** `[0]` and `002AEA1A` the **live** one and
         `002AEA1E` subtracts. **Differencing a start against an end is what you do to a pen**, not to
         a rectangle you were handed.
      3. **The two deltas go where the measurement goes.** `[rdi+0x18]` receives `entry[0] - live[0]`,
         the total advance (`002AEA3D`); `[rdi+0x14]` — this document's *measured extent, written
         back* — receives `[rsi+4] - xmm7` (`002AEA34`–`002AEA47`).

      **Components [2] and [3] are carried-but-unread payload — now proven end to end
      (2026-09-18, SWE2-STRUCT).** The one escape this body cannot see through was the snapshot's
      own address: `002AE9EE` `lea r8, [rbp+0x40]` hands the whole local to **`002A9F00`** — the
      glyph-quad emitter — where it lands in `r15`. Every `r15` access in `002A9F00` is `[r15]`
      or `[r15+4]` (`002AA0DA`/`002AA4A5` x-reads, `002AA0E8`/`002AA742` x-writebacks,
      `002AA34C`/`002AA4E9` y-reads); **`[r15+8]` and `[r15+0xC]` are never touched**. The local's
      `[rbp+0x48]`/`[rbp+0x4C]` slots are written and never read. Upstream, all three `002AE610`
      call sites (`002AD8EB`, `002ADBC9`, `002B19A2`) pass `rbp+0x60` — a stack float4 copied
      wholesale from `[r12]` — and the dispatcher chain `002A9F00 -> 002AC5F0 -> 002AE610`
      (`002AA69D` `mov r8, r15`) forwards the same pointer unchanged. Combined with the block
      census finding `+0x08`/`+0x0C` copy-only in all 52 bodies, **no reachable path consumes
      components [2] or [3]**: the pen is a four-float value for alignment/SIMD convenience of
      which only x (`[0]`) and y (`[1]`) carry meaning in this image.

      **A fourth fact, which belongs to §7 rather than here:** the whole writeback block is skipped
      when the kind byte is 3 — `002AEA26` `cmp byte [rdi+0xA3], 3` / `je`. **So on the message
      window's kind-3 path this function measures and records nothing**, which is consistent with kind
      3's row being slot 2 only: no numeric formatting, no text drawing, and now no measurement
      writeback either.
- [x] ~~The identity of the resource that `003FFC60` returns — described here as "glyph metrics",
      which section 10 shows was never established. **AC-8.**~~
      **Mirrored in the register 2026-09-13, in the commit that ticked this box.** The box was held
      unticked for most of a day because `OPEN-QUESTIONS.md` still called `AC-8` OPEN while
      `SWE2-DATA` held the file under `DATA-FMT-PS2IMG-TAIL`, and ticking it alone turns
      `check_questions` red and aborts every publisher's chain (raised by FABLE, 2026-09-13; ticked
      in `3dd52ed3` and unticked again here). That lock was ruled unenforceable and unexercised —
      `OPUS-ADJ-INDEX-LOCK-SCOPE` — and the row and the box moved together.
      **ANSWERED 2026-09-13 (OPUS): it returns no resource at all. `003FFC60` is a FIELD DECODER
      over a three-byte record, and it returns the constant `3`.** §10 was right to doubt the
      description — *"yields the glyph metrics table from the resource handle"* is wrong in both
      halves: no handle is dereferenced and no table is produced.

      **Six parameters — four in registers and two on the stack** — each an optional out-pointer
      that is written only when non-null:

      | out | written | source |
      |---|---|---|
      | `rdx` | `byte` | `record[1] & 0x7F` — a 7-bit value |
      | `r8` | `byte` | `record[2] & 0x0F`, **clamped to 8** (`cmp cl, 8` / `cmova`) |
      | `r9` | `dword` | `(record[2] >> 6) & 1` |
      | `[rsp+0x28]` | `dword` | `(record[2] >> 5) & 1` |
      | `[rsp+0x30]` | `dword` | `(record[2] >> 4) & 1` |

      **So the record is three bytes**: byte 1 a 7-bit field, byte 2 a packed `{4-bit value, three
      single-bit flags}`, and the function ends `mov eax, 3 / ret` — **a constant return, almost
      certainly the record's own size** rather than a count or a pointer. Every write is guarded, so
      a caller may ask for any subset of the five fields.
      **Not established:** what the fields *mean*. The shape is now exact and the semantics are not —
      naming byte 2's three flags needs a consumer, and none is read here.
      *2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13): the consumers are now named. `003FFC60` is the payload parser
      of the `.` and `-` escapes ([the text control-code language](the-text-control-code-language.md), the escape
      table), and the number formatter `002AE610` calls it at `002AE760`. What each of the five outputs means there is
      proposed row P5 (§15).*
      *Answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15, §15b P5):* byte 1 selects the argument (`0x7F` is the state's own number),
      byte 2's low nibble is the field width, bit 5 the pad character and bit 4 the second character map; bit 6 is
      unread.
      **Worth one note for the ABI recovery page.** This is a clean worked example of the
      stack-argument caveat recorded there: four register parameters and two more at `[rsp+0x28]`
      and `[rsp+0x30]`, so any liveness-derived arity would cap at 4 and miss a third of the
      signature. `003FFC60` is not in `derived-call-signatures.tsv` — nor is that page's own named
      example `002465F0` — so the 562 rows are **a sample of the image, not a census of it.**
- [x] ~~What `002A9F00` (2,304 B) does with the mapped character. It is where the per-character
      advance actually comes from, and it is unread.~~ **AC-9 ANSWERED 2026-09-12 (FABLE) — and the
      advance is not a glyph metric.** The function is the one
      [the glyph-run page](../../99-Unresolved-Residual/Glyph-Run-Rendering/drawing-a-line-character-by-character.md)
      reads as *drawing a line character by character*; with the mapped character it: decodes it
      (`002AC2F0` → a glyph index `ebx`), takes the glyph's 8-byte descriptor from the font's table
      (`ImageAddress_ResolveRuntimePointer([font + 0xC])`, `[table + index × 8]`, `002AA0F8`–`002AA117`),
      packs the descriptor's bit fields into two 64-bit render commands written to the command
      stream at `[0209CC50]` (`002AA1AE`–`002AA28F`), lays the quad's corners at `pen.x`,
      `pen.x + scale` and `pen.x + w × scale` (`0209CC60` is the scale, `002AA498`–`002AA4E4`),
      and hands a 160-byte glyph record to `0017F7C0`. **The pen is advanced only by the spacing
      globals**: `pen.x += [0209CC6C]` before the glyph (`002AA0D2`–`002AA0E8`) and
      `pen.x += [0209CC68]` after it (`002AA734`–`002AA747`, the loop tail, also after a control code);
      the glyph's own width `w` shapes the quad and never enters the pen. `0209CC68` / `0209CC6C`
      are a caller-owned pair (written as one qword by the callers — this formatter zeroes both on
      its early-out at `002AE848` and at `002AEAC2`, then stores its running total into `0209CC68`
      at `002AEAC9`; `002B0280`, `002AF340`, `002AE450`, `002AEB20`, `002AAE40`, `002AF960`,
      `002B2150` and the control-code interpreter `002AC5F0` set them on their paths), and this
      formatter reads the pair once as its per-digit step (`xmm8` at `002AE7DC`–`002AE7EA`). So the
      per-character advance is **fixed pitch per call, set by the caller**, which is the mechanism
      behind even digit columns (`AC-10`'s observation still unmeasured). *(Qualified 2026-09-30, SWE2-CONTRACT for
      OPUS, DD batch 13: this holds for the number formatter, which derives the step once. The general loop `002A9F00`
      re-derives `0209CC68` from each glyph through `002AC2F0`, so ordinary text is not fixed pitch, §15 N3.)* The descriptor's bit
      layout and the two render commands are transcribed, not decoded, on the glyph-run page.
- [x] ~~Whether digit columns are in fact even on screen. The mechanism believed to cause it
      does not exist; the observation itself was never measured.~~ **AC-10.**
      **ANSWERED 2026-09-17 (FABLE) - from the bodies, and no screen is needed.** The row asked about an observation; the property it wanted is a fact of the code. **Within one formatting call the digit step is one register loaded once.** `002AE610` decodes ONE reference character before its digit loop - the 16-bit code at `+0x20` of the map table, which this page already identifies as the entry for `'0'` (`002AE7B7`, `002AE7D7 call 002AC2F0`) - and `002AC2F0` writes the whole 16-byte spacing block from that glyph (`movaps [0209CC60]` at `002AC56A`/`002AC59F`, then `[0209CC68]` from the signed advance byte `[rdi+0xA9]` at `002AC5C3`). The formatter then loads `xmm8 = [0209CC68] + [0209CC6C]` at `002AE7DC`/`002AE7EA` and advances its pen by `xmm8` per digit at `002AEA4C`; `xmm8` is written nowhere else between the load and the epilogue restore at `002AEAF7`, and the digit loop `002AE920`–`002AEA96` contains no reload. So every digit of one number advances by the `'0'` glyph's pitch - **monospaced by construction**, whatever the drawn digit is. **Across calls the same holds whenever the font and scale are the same**, because the step is derived from `'0'` each time, not carried over: on exit the formatter overwrites the block (`002AEABB`/`002AEAC2` zero it, `002AEAC9` stores the number's total advance into `0209CC68`) and the next call re-derives it. Two numbers drawn with the same font and scale therefore share their pitch; column alignment then depends only on the caller's starting pen, which is authored layout, not a mechanism. *(The question this row leaves open below, one pitch per line or per character in `002A9F00`, is answered 2026-09-30 in §15 N3: per character. SWE2-CONTRACT for OPUS, DD batch 13.)* **The row's premise is withdrawn:** *the mechanism believed to cause them does not exist* was true of the per-glyph-metric belief `AC-9` refuted, and `AC-9`'s own answer names the mechanism that does exist. **What this does not settle, and is not this row:** whether the general glyph loop `002A9F00` keeps one pitch per line or lets the control-code interpreter `002AC5F0` re-set `0209CC68` per character (it writes it at 14 sites) - that is the 2026-09-14 note on this page, about text, not digits. Static, body read; the `xmm8` liveness is re-checkable in one listing.
- [x] **UQ-166 — ANSWERED: no.** Whether damage numbers specifically route through here. The `StoryEvent`
      callees are evidence of *dialogue* text; nothing yet ties this to combat.
      *Narrowing withdrawn the same day, 2026-09-15 (FABLE).* A narrowing that put this row behind
      `UQ-382` was published and retracted within the hour: slot 2 **is** dispatched, by `002AF960`
      through the image base, so this loop is reachable and the row stands on its own terms again.
      **Narrowed again the same day, and this time from the kind byte rather than from an absence**
      (§7, *Who sets the kind byte*): `002AAE40` is reachable only as slot 2 of **kind 3**; kind 3 is
      written at exactly one site image-wide, `002A49CA` in `002A4830`; and `002A4830` has one route in,
      case 4 of the message-window proc `002A6190`. **So damage numbers do not route through
      `002AAE40`.** ~~What remains open is the rest of the cluster: `002B0280`, `005742D0` and vtable
      dispatch are doors that have not been read, and combat could still enter through one of them.~~

      **Three of the four doors are now traced, and none of them is combat — 2026-09-15 (FABLE).**

      | door | what it is | how it reaches the cluster |
      |---|---|---|
      | `002A6190` | **the message window** | case 4 → `002A4430` / `002A4830` → `002AF960` (§7) |
      | `005742D0` | **a handbook content page** — [the menu screen atlas](../Menu-Screen-Atlas/the-menu-screen-atlas.md) lists it beside `00571A50` and `00579AF0` as handbook content, with dispatch ids 1, 3, 10, 12, 14, 15, 18 | `00573BE0` → `002B5390` → the hub `002B2150`, from **cases 1 and 10** (`005745A6`, `00574672`) |
      | `002B0280` | the ShaderMaterial body, 6,441 B | calls the hub directly; its six callers are `002A86A0` (a message-window helper), `002D8690` / `002D87D0` / `002DD680` (the `002D8xxx` draw-helper family), `003F1530` (`Presentation`) and `00243860` |

      **`005742D0`'s jump table was decoded rather than assumed:** `mov eax, [rdx]` / `dec` /
      `cmp eax, 0x11`, then `lea r8, [rip - 0x4542FE]` → `00120000` and
      `mov ecx, [r8 + rax*4 + 0x45471C]` — the image-base idiom again — giving ids 1, 3, 10, 12, 14,
      15 and 18 against `005746FC` as the default. **Those are the seven ids the atlas already
      records**, derived independently here.

      **What that leaves.** A menu screen and a shader-material body are not combat, so **no traced
      door into this cluster is combat-side**, which is the second independent reason damage numbers do
      not arrive here — the first being that `002AAE40` needs kind 3 and kind 3 needs the message
      window. ~~**The row stays `PARTIAL` because the fourth door is `vtable dispatch`**, and that is not
      a body to read: enumerating it needs a vtable census rather than a call-graph walk.~~ *I checked
      before writing this — `005742D0` reaches the cluster at depth 3 and my first reading, that its
      direct callees contained no cluster function so it was not a door at all, was wrong.*

      **The fourth door is a tag, not a route — `UQ-166` is ANSWERED, and the answer is no.** The census
      it needed turned out to be cheap: scan the whole image for every stored form of each of the
      cluster's twenty members.

      | form scanned | result |
      |---|---|
      | 8-byte pointers, 8-aligned | **only the drawer table** — `009164C0`–`00916518`. Nothing else anywhere |
      | 4-byte absolute VAs | the same seven table slots, plus one `.pdata` entry for `003EFD00` |
      | 4-byte **image-base-relative** (`va - 0x120000`, the form this image's jump tables use) | 23 entries in `.rdata` around `01D6FB68`–`01D70364` |

      **Those 23 are the exception table, and their own shape says so.** Around `002A8C50`:

      ```
      01D70140  00188C50  -> 002A8C50   BeginAddress
      01D70144  00188D44  -> 002A8D44   EndAddress
      01D70148  01C5010C               UnwindInfoAddress
      01D70150  00188C50 / 00188D44 / 01C5010C   the same triple again - a chained entry
      ```

      A `{Begin, End, UnwindData}` triple at a 12-byte stride is `RUNTIME_FUNCTION`, and
      `002A8D44 - 002A8C50` = `0xF4` against the function's own 3,363 bytes, which is a **funclet
      range** and not a call target. **The project bans unwind data as support in any case**, so these
      would not be evidence of a route even if they were not plainly one.

      **So no cluster function is stored in a vtable**, and the fourth "door" is the CodeDomain tag
      `Runtime.RealFunctionPointerOrVtableMember` — a classification, not an observed dispatch.

      **The answer does not rest on the door enumeration.** It rests on the kind-3 chain, which is
      closed independently: `002AAE40` is reachable only as slot 2 of kind 3; kind 3 is written at
      exactly one site image-wide; that body has one route in; and that route is the message window's
      case-4 update. The doors are corroboration — four of four now accounted for, none combat-side.

      **The limit, and it is the only one left.** The kind byte could in principle arrive through a
      **re-based block copy**, which no displacement census can see — the blind spot recorded in §7.
      The three such copies in this cluster all share `0209C630`, and all three of their users have
      `002A6190` as their only caller, so none carries a kind out of the message window. **That is a
      measurement, not an assumption, and it is where a future correction would have to come from.**

### The drawer dispatch table, and a slot nothing reads — 2026-09-15 (FABLE)

**How this loop is reached at all, which this document had not asked.** `002AAE40` has **no `rel32`
caller anywhere in the image**. Its only reference is a single quadword at `00916518`, which is an
entry in a dispatch table immediately before the power-of-ten table §8 already documents.

**The table is three-wide, indexed by a kind byte.** All three dispatchers share one shape —
`movsx rax, byte [rcx + 0xA3]`, `lea rdx, [rax + rax*2]` (× 3), then an indexed load and a tail
`jmp`:

| dispatcher | base | which slot |
|---|---|---|
| `002B3930` (`002B393C`) | `009164C0` | **slot 0** |
| `002ABEC0` (`002ABEFD`) | `009164C8` | **slot 1** |
| `002ABF20` (`002ABF4D`) | `009164C8` | **slot 1** |

So group *k* occupies `009164C0 + 24k`, and the shipped contents are:

| kind | slot 0 | slot 1 | slot 2 |
|---:|---|---|---|
| 0 | `002A9980` | `002A8C50` | `002A9F00` |
| 1 | `002A9980` | `002A8C50` | `002AA800` |
| 2 | *null* | *null* | *null* |
| 3 | *null* | *null* | **`002AAE40`** ← this section's loop |

**No code reads slot 2.** Four instruments, each with a different blind spot, agree:
1. **`rel32` decode** — `002AAE40` and `002AA800` have **zero** call or jump sites; `002A9F00`, the
   third slot-2 entry, has eight, so it is reachable *without* the table and is not evidence for it.
2. **Whole-image pointer search** — one 8-byte pointer to each, at its table slot, and nothing else.
3. **RIP-operand scan over `009164B0`–`00916520`** — exactly the three `lea` sites above. Nothing
   materialises `009164D0`, `009164E8`, `00916500` or `00916518`.
4. **Absolute-immediate search** for `009164B8`, `009164C0`, `009164C8` and `009164D0` — none.
5. **RIP-operand scan over the two functions' own addresses** (`002AAE40`, `002AA800`) — **no
   instruction anywhere materialises either address**, so neither is stored into a struct or a
   runtime-built table by any `lea` the image contains.

**The index is signed, and that was checked rather than assumed.** All three dispatchers widen the
kind with `movsx`, which `UQ-176` already flags as unexplained. A negative kind would read
`009164C0 − 24k`, so the region below the base was dumped: `009164B0` and `009164B8` are zero and
everything below is float and small-integer data with **no `.text` pointer**, and `test rax, rax`
would not reject it. So the table is exactly the four groups above and does not extend backward.

~~**This is "no route found", and it is deliberately not "dead".**~~ **RETRACTED THE SAME DAY,
2026-09-15 (FABLE): slot 2 IS dispatched, and the route was exactly in the blind spot named above.**

The paragraph above hedged on one thing — *"a base computed at run time … would be invisible to
every one of them"* — and that is precisely where the route was. **`002AF960` dispatches slot 2:**

```asm
002AFB6C  lea   rdi, [rip - 0x18FB73]          ; rdi = 00120000, the IMAGE BASE
...
002AFCA5  movsx rax, byte ptr [rbx + 0xA3]     ; kind
002AFCAD  lea   r9, [rax + rax*2]              ; kind x 3
002AFCB1  call  qword ptr [rdi + r9*8 + 0x7F64D0]
```

`0x00120000 + 0x7F64D0` = **`0x009164D0`**, the slot-2 base, so the call is
`[009164D0 + kind * 24]` — slot 2 of group *kind*, the same `kind × 3` shape as the other three
dispatchers. **`002AAE40` (kind 3) and `002AA800` (kind 1) are reachable**, and `kind = 3` is really
set: `002A49CA` writes `mov byte [rbx + 0xA3], 3` in `002A4830`, and `002ACA4B` and `002AEA26` both
test the byte against 3.

**Why five instruments missed it, which is the part worth keeping.** Every one of them looks for the
*target address* — as a `rel32`, a RIP operand, a stored pointer or an absolute immediate. This
idiom never materialises the target: it materialises **the image base** and reaches everything else
by displacement. **That is not rare here — 594 functions in this image do it, over 1,411 accesses,
reaching 971 distinct addresses** that no address-based scan can see. The fault was not in any one
instrument; it was in believing that five instruments sharing one assumption are five instruments.

**What survives from the retracted finding:** the table's shape and contents are unchanged and were
correct — three-wide, `kind × 3`, four groups, with `002B3930` on slot 0 and `002ABEC0` / `002ABF20`
on slot 1. Only the conclusion drawn from their absence was wrong. `UQ-382` is **answered**, and
`UQ-166` returns to its own terms.

### Who sets the kind byte, and where kind 3 comes from — 2026-09-15 (FABLE)

The retraction above left `002AF960` dispatching `[009164D0 + kind × 24]` and said nothing about where
the *kind* comes from. It comes from one place, and getting there required first separating two
different structures that both use offset `0xA3`.

**The instrument.** Every byte-sized memory operand at displacement `0xA3` through a non-`rip` base,
over all 34,270 listed bodies: **21 sites, of which 8 are stores** — the rest are `cmp`, `test`, `and`
and `or`. A second pass then looked for a store of *any* width whose `[disp, disp + size)` covers
`0xA3`: 1,008 sites, 987 of them wider than a byte, but every one of those inside `002A0000`–`002B6000`
is `rsp`- or `rbp`-based stack framing. No wide store reaches the kind byte in this cluster.
**Its limit, stated rather than discovered later:** a block copy that re-bases first —
`lea rcx, [rcx + 0x80]` and then `movups [rcx + 0x20]` — carries a displacement of `0x20`, not `0xA0`,
and a displacement census cannot see it. Three such copies exist here; they are accounted for below.

**Two structures share offset `0xA3`, and merging them would have been the easy mistake.** `002475D0`
and `00247680` write `+0xA3` from a caller's `edx`, then fill `+0xA4`–`+0xAB` from the frame-inset
constants at `01E0C110`–`01E0C11C`; `00245170` and `002455A0` read `+0xA3` back. It looks like the same
field the dispatchers read. It is not — at `00227EE0` the setter and the dispatcher are handed pointers
**`0xC0` apart**:

```asm
00228068  mov  edx, 0xFF
0022806D  mov  rcx, rsi                 ; the widget itself
00228070  call 002475D0                 ; the parametric setter
...
00227F95  lea  rcx, [rsi + 0xC0]        ; the text state embedded in it
00227F9C  call 002ABEC0                 ; the slot-1 dispatcher
```

`002A4830` shows the same relation from the other side: its state is copied out of `[window + 0xD0]`.
So the values the parametric setters carry — `4` and `11` from `002A70B0`, `6` from `002D66D0`, `10`
from `00572600`, and `0xFF` remapped to `1` inside `002475D0` for `00227EE0`, `00241D40` and `003F4330`
— are the **widget's** byte and never index the four-group table. That distinction is load-bearing:
read as drawer kinds, `4`, `6`, `10` and `11` would each have run off the end of a 96-byte table
straight into the power-of-ten data at `00916520`.

**On the text state, the kind map is this:**

| kind | written by | how | slot 2 |
|---:|---|---|---|
| 0 | `002B3C30` (`002B3C40`), `002B3D50` (`002B3D78`) | immediate `0` | `002A9F00` |
| 1 | *no writer returned by the census* | — | `002AA800` |
| 2 | `002B3400` (`002B3470`) | immediate `2` | *null* |
| 3 | `002A4830` (`002A49CA`) | immediate `3` | **`002AAE40`** |

Kind 1 is kind 0 with one substitution: their slots 0 and 1 are the same two functions and only slot 2
differs. **The empty cell is a census result, not a claim that kind 1 is unused** — what is established
is that no byte-sized store of `1` to a text state's `+0xA3` appears in any listed body, and the
re-based-copy blind spot named above is exactly where such a write could still hide.

**Kind 2 is the *draws-nothing* kind, and that is a design rather than a gap.** Its whole row is null,
and the question that makes it meaningful is whether a kind-2 state ever reaches a dispatcher at all —
because if it does not, the null row says nothing. **It does.** `0057C480` hands the *same* object to
the setter and to two dispatchers:

```asm
0057C50D  lea rcx, [rsi + 0xE0]   →  002B3400    ; the initialiser, which ends mov byte [rdi+0xA3], 2
0057C8E0  lea rcx, [rsi + 0xE0]   →  002ABEC0    ; slot 1
0057C9B0  lea rcx, [rsi + 0xE0]   →  002B3930    ; slot 0
```

So both dispatchers load a null and fail their own null test. That also explains why every dispatcher
null-tests: **the test is what makes kind 2 work**, not defensive padding.

**A worked example of kind 2, which refines it** — and it was already in the database under another
name. `0057C480` is **the confirm window**, the generic choice dialog, documented on
[the shared dialog widgets](../Shared-Dialogs/the-shared-dialog-widgets.md), where its id-1 arm is
described as *"measures the caption: `002B3400` / `002B3280` text extents → `+0x120` / `+0x114`"* and
its other arms work on *"the `+0xE0` text block"*. **`+0xE0` is the object above.** So the caption's
text state is stamped kind 2 while its extents are being measured, and **every dispatcher the window
afterwards calls on that same state resolves to a null slot**:

| arm | site | dispatcher | slot | result |
|---|---|---|---:|---|
| id 1, measure | `0057C50D` | `002B3400` stamps the kind | — | `[state + 0xA3] = 2` |
| id 10, input | `0057C9B7` | `002B3930` | 0 | null |
| id 2, reconcile | `0057C8E7` | `002ABEC0` | 1 | null |
| id 4, draw | `0057C92A` → `002D8550` | `002AF960` | 2 | null |

**And the caption is still drawn**, which is what makes the reading precise. Kind 2 does not mean
*nothing happens*; it means **no kind-specific operation is added to the standard ones**. What runs
regardless of kind is everything a dispatcher does *before* dispatching — `002ABEC0` and `002ABF20`
publish `(int16) obj[0x8C]` into `[0209CC40] + 0x10D8` and clear `[0209CC48]` whatever the kind — and
everything a caller does before reaching one: `002D8550` modulates four colour bytes by
`word [font + 0x5A]` and `[font + 0x58]`, calls `00203170` and `00397910`, and sets
`[state + 0xB8] = 0x3001` and `[state + 0x20]`, all before its `002AF960` call at `002D8620`. The
shared-dialog page's own account of the draw arm names `002D8BB0` / `002D8910` as what renders.

**`002B3930` is the clean case, because it has nothing else to do.** At 32 bytes it is the dispatcher
that only dispatches, so on a kind-2 state it really does return having done nothing at all.

**`0057C480` confirms the two-structure split a second time, and independently.** Four instructions
before the `002475D0` call it does `mov rcx, rsi` — the *widget* — while every dispatcher call in the
same body takes `rsi + 0xE0`. At `00227EE0` the same split was `rsi` against `rsi + 0xC0`, and in
`002A4830` the state comes from `[window + 0xD0]`. **Three call sites, three different embed offsets,
never the same pointer**: the text state is a sub-object of the widget and the two `+0xA3` bytes are
different fields. (`0057C480` also shows the parametric setter's value being computed rather than
chosen — `shr edx, 4` masked, with `cmovb edx, 4` on flag bit 13 — which is why its callers produce 4,
6, 10 and 11 and why those are not selectors.)

`002B3400` is worth one more line because it settles the structure question from the inside: before it
writes the kind it writes `word [state + 0x8C] = 0x7D00` — **the same constant at the same offset that
`002A4830` writes at `002A49C2`** — along with `[state + 0x60]`, bit 11 of `[state + 0x44]` and
`[state + 0xA6]`. `002A4830` writes all four of those fields too, at `002A49C2`, `002A4A09`,
`002A49F3`–`002A49FE` and `002A49E5`. Two initialisers of one structure, reached from opposite ends of
the image.

**Putting the four rows together, the table reads as one design.** Slots 0, 1 and 2 are *numeric
formatting*, *text drawing* and *the per-character walk* — the identities
[the dispatch-table page](../../99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md)
establishes for slots 0 and 1 from `002A9980`'s power-of-ten reference and `002A8C50`'s interpreter
call. Read that way the kinds are four combinations of the same three operations:

| kind | numeric | text | char walk | reads as |
|---:|---|---|---|---|
| 0 | `002A9980` | `002A8C50` | `002A9F00` | the ordinary text element — all three operations |
| 1 | `002A9980` | `002A8C50` | `002AA800` | kind 0 with a different walk, and no writer found |
| 2 | *null* | *null* | *null* | laid out, draws nothing |
| 3 | *null* | *null* | `002AAE40` | the walk alone — no numeric formatting, no text drawing |

**This is a reading, and it is offered as one.** Slots 0 and 1 are named from two functions' own
references; slot 2 is named from what `002A9F00` does, which §7 reads in full.

**The kind is not a property of the window. It is a per-draw mode on a state built for one draw** —
which is what makes the question *"what are the four kinds"* answerable in principle at all, and also
what makes it not a question about object types. Two bodies show it side by side, and they are doing
the same thing to the same field of the same window:

| | `002A4830` (kind 3) | `002A1B00` (kind 0, via `002B3C30`) |
|---|---|---|
| source block | `002A4886` `lea rax, [rcx + 0xD0]` | `002A1B2D` `lea r14, [rcx + 0xD0]` |
| copied to | `002A4890` `lea rcx, [rsp + 0x40]` | `002A1B3B` `lea rdx, [rsp + 0x40]` |
| by | a `movups` chain over `0xC0` bytes | the same `movups` chain |
| stamped | `002A49CA` `mov byte [rbx + 0xA3], 3` | `002B3C40` `mov byte [rcx + 0xA3], 0` |

**Same window field, same stack offset, different kind.** So a window does not *have* a kind; each
draw **takes a copy of the window's text block and selects a mode on the copy**. It also explains the
shape of `002A4830`'s other arm: a state whose kind nothing re-stamps keeps whatever the copy brought
with it.

> ~~… and the dispatchers then read that mode.~~
> **Corrected within the day, 2026-09-15 (FABLE): a stamped kind is not necessarily a read kind.**
> That clause was true of the example it was drawn from and not of the other one on the same line.
> **`002A4830`'s kind 3 is read** — it hands the stamped object straight on at `002A4B3B`
> `mov rcx, rbx` / `002A4B3E` `call 002AF960`. **`002A1B00`'s kind 0 is not.** Its `[rsp + 0x40]` is
> referenced exactly twice in the whole body — `002A1B3B` as the copy destination and `002A1C24` as
> `002B3C30`'s argument — and never again; `002A1B00` calls no dispatcher, and `002B3C30`'s own
> callees are `002B2150` and `002B24B0` (→ `002AF340`), none of which is one. **That kind 0 is
> written and never read.**

**Which sharpens the model rather than weakening it.** The kind byte is **a field every initialiser
sets**, and it becomes *a mode* only when the state reaches a dispatcher. `002A1B00`'s state exists to
be measured and is then discarded — the same shape as `002B1FB0` two sections above, which builds a
throwaway state, measures one token and returns bytes consumed. **So the population of states carrying
a kind is larger than the population of dispatches**, and any census of kinds that assumes otherwise
is counting writes as reads. That is the same error as counting instruments that share an assumption,
one level down.

**What is *not* established** is any kind's subject except 3. Kind 2's is named one section below by
the confirm window. For kind 0, `002A1B00` is the nearest thing to a name and it is not one yet:
`002A5590` builds a `{callback, context}` descriptor — `002A5836` `lea rax, 002A1B00` into
`[rbp - 0x60]`, the owner into `[rbp - 0x58]` — hands it to `002D14E0`, and stores the result in
`[owner + 0xC0]`; the same `002A5590` reads `NobuMessageSelectLF` and seeds the selection cursor at
`+0x3B9`, so the surrounding machinery is an **in-window selection list** and `002A1B00` looks like
its per-row callback. **That is a reading of the neighbourhood, not of a call**, and it is left at
that: whether `[owner + 0xC0]` here is the same field the shared-dialog page calls *"the embedded
list child"* on a different class is not established. *(Answered 2026-09-30, DD batch 13, §15 N4: both owners
store the return of `002D14E0`, the `0x150`-byte list widget with procedure `002D2DB0`, at their `+0xC0`. So it is
the same child on two owner classes.)*

**And one loose end recorded rather than resolved.** `002A1B00` does not itself call a dispatcher. It
hands its stamped state onward and calls `002D89E0`, **which calls `002B3400`** — the kind-**2**
initialiser. Whether that re-stamps the same state or a different one was not traced, and it is the
next thing to read on this thread. *(Answered 2026-09-30, DD batch 13, §15 N5: a different one. `002D89E0` hands
`002B3400` its own stack block, `lea rcx, [rsp + 0x40]` at `002D8A25`.)*

**Kind 3 has one origin, and the chain closes on it.**

1. `002A49CA` is the only store of `3` to this byte anywhere in the image.
2. `002A4830` has **one** route in, and this time the instruments do not share a blind spot: the
   `rel32` edge set gives `002A6190` alone; a whole-image 8- and 4-byte pointer search returns
   nothing; a RIP-operand and absolute-immediate scan over all 34,270 bodies returns 0 references
   with its control passing; and `work/graph/imagebase_refs.tsv` — the pre-existing image-base table,
   636 functions and 1,076 globals, generated 2026-09-08 and *not* wired into the absence gate, which
   is the real defect the retraction above exposed — lists no reference to `002A4830` either.
3. The call sits at `002A6329`, inside **case 4** of `002A6190`'s jump table. That table is at
   `002A698C` and is itself reached through the image base (`lea rsi, [rip - 0x1861C3]` → `00120000`,
   `mov eax, [rsi + rax*4 + 0x18698C]`, `add rax, rsi`, `jmp rax`); decoded, its 21 entries send ids
   1, 2, 3, 4, 10, 12, 15, 18 and 21 to nine distinct bodies and the other twelve to the `default` at
   `002A6971` — which is where §5's count of nine labels comes from.
4. Inside case 4 the arm is chosen by the window's own flag word: `bt eax, 0xB` returns, `bt eax, 0xD`
   skips the draw, and `test eax, 0x700` then selects `002A4830` over `002A4430`. Both arms end in
   `002AF960`, which is why the kind byte and not the branch decides the drawer.
5. `002A4830` hands the dispatcher the object it has just stamped: `002A4B3B mov rcx, rbx` /
   `002A4B3E call 002AF960`, where `rbx` is the same base that took `mov byte [rbx + 0xA3], 3`.
6. `002A6190` is **the message window**, already established from its layout keys on
   [the message-window layout readers](../Message-Windows/the-message-window-layout-readers.md).
7. The one sideways path a kind byte could take is the `0xC0`-byte copy into the global staging buffer
   `0209C630` — the re-based copy the census cannot see. Its three users are `002A4430`, `002A4830`
   and `002A5F40`, and `002A6190` is the only caller of all three: the same four instruments were run
   against each of them and return no other route in. So the copy cannot carry a kind out of the
   message window either.

So kind 3 is the message window's own variant, and `002AAE40` — slot 2 of kind 3, with no other
reference in the image — is entered from there and from nowhere else.

**What this does to `UQ-166`, which is a narrowing and not an answer.** The row asks whether damage
numbers route through this cluster. One of its doors is now traced end to end and is dialogue-side:
nothing combat reaches `002AAE40`, because reaching it requires kind 3 and kind 3 requires the message
window's case-4 update. The row stays open because **the cluster has other doors** — `002B0280`
(ShaderMaterial), `005742D0` (the second message handler) and vtable dispatch, per §5 — and none of
them has been read. Closing one arm is not closing the question, and the negative here is about
`002AAE40` specifically, not about the cluster. *(UQ-166 was ANSWERED the same day: all four doors are accounted for,
and none is combat, §7. Marked 2026-09-30, SWE2-CONTRACT for OPUS, DD batch 13.)*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `00916520` is a power-of-ten table | read directly from `.rdata` in the authorized EXE: `1, 10, 100, … 100000000` | 1 |
| Digits are produced by repeated subtraction of powers of ten | complete loop in `002AE610` | 1 |
| A `ushort` table indexed at `(ch - 0x20) * 2` yields a **character code**, stored to a buffer and passed to `002A9F00` | disassembly of `002AE610` at `002AE931`–`002AE96D`, `002AE998`, `002AE9FC` | 1 |
| The `'0'` entry (`+0x20`) is a **padding substitution inside the loop** | `002AE984`–`002AE989` overwrite the output buffer; `002AEA96 jl 0x2ae920` proves the loop | 1 |
| ~~The `'0'` entry is hoisted out of the loop and used as a fixed digit advance~~ | **RETRACTED** — see section 10 | — |
| Minimum field width at `state[0x98]` | the clamp in `002AE610` (`002AE89C`) | 1 |
| Shared 208-byte state block | `002AE610` and `002B2DF0` both copy `param_1[0]`–`param_1[0x19]` | 1 |
| Cluster membership, doors and exits | connected-component analysis over `graph/edges.tsv`, joined to `functions.tsv` | 1 |
| These functions are unresolved | `verify/residual_addrs.txt`, the certified residual dump | 3 |
| Kind 2 states really do reach the dispatchers, so the null row is a design | `0057C480` passes `rsi + 0xE0` to `002B3400` (`0057C50D`), to `002ABEC0` (`0057C8E0`) and to `002B3930` (`0057C9B0`) | 1 |
| The widget and the text state are different structures, at two independent call sites | `00227EE0`: `rsi` to `002475D0`, `rsi + 0xC0` to `002ABEC0`. `0057C480`: `rsi` to `002475D0` (`0057C7EB`), `rsi + 0xE0` to all three dispatchers | 1 |
| `002B3400` and `002A4830` initialise the same structure | both write `word [state + 0x8C] = 0x7D00`, `[state + 0x60]`, bit 11 of `[state + 0x44]` and `[state + 0xA6]` | 1 |
| The kind byte `+0xA3` is stored at 8 sites image-wide, and only `002A49CA` stores `3` | byte-width displacement census over all 34,270 listed bodies, plus an any-width pass whose 987 wider stores are all stack framing inside this cluster | 1 |
| The parametric setters `002475D0` / `00247680` act on a different structure from the dispatchers | `00227EE0` passes `rsi` to `002475D0` and `rsi + 0xC0` to `002ABEC0`; `002A4830` takes its state from `[window + 0xD0]` | 1 |
| `002A4830` has exactly one route in | `rel32` edge set; whole-image 8/4-byte pointer search; RIP-operand and absolute-immediate scan (0 of 1, control passing); `work/graph/imagebase_refs.tsv` | 1 |
| The call to `002A4830` is in case 4 of `002A6190` | jump table at `002A698C` decoded from the image; the call at `002A6329` lies between the case-4 and case-2 targets | 1 |
| `002A4830` dispatches the object it stamped | `002A4B3B mov rcx, rbx` / `002A4B3E call 002AF960`, same `rbx` as `002A49CA` | 1 |
| The Audio doors are message handlers, entering from a per-frame update case | complete `switch` and case-4 body of `002A6190`; identical handler signature in `005742D0` | 1 |
| `0209C4D0` is an 8-slot registry of live **message windows**, `0209C4D0`–`0209C50F` | the 8-iteration first-free-slot scan in `002A6190` case 1 stores its own object at `002A6236`; `002A28E0` bounds the walk with `lea rdx, 0209C510` and reads each entry through `+0x40`, `+0x3E8` and `+0x3C5`, which are message-window fields — *“actor” corrected 2026-09-15* | 1 |
| A window with `[+0x40] & 0x10` and `[+0x3E8] & 0x700` makes the four mask getters return **0** | `002A28F8`–`002A2908` in `002A28E0`, and the same shape in `002A2940` / `002A29A0` / `002A2A00` | 1 |
| That is the same flag group `002A6190` uses to select the kind-3 drawer | `002A631B` `test eax, 0x700` on `[rcx+0x3E8]`, against `002A28FE` `test dword [rax+0x3E8], 0x700` | 1 |

**Not evidence, and deliberately excluded:** the three data references to cluster member `002AAE40`
are all **exception-handling metadata** — one `.pdata` `RUNTIME_FUNCTION` entry and two `.rdata`
scope-table RVA pairs. `.pdata`/`.xdata`/unwind data is banned as proof by the evidence standard,
so `002AAE40` is treated as having **no** reference at all.

## 9. Related

- [`../../99-Unresolved-Residual/the-unresolved-158.md`](../../99-Unresolved-Residual/the-unresolved-158.md)
  — where this cluster was found, and the other nine functions
- [`../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`](../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md)

## 10. Falsification pass 2026-09-02 — the headline was wrong

**Attack chosen.** This document's flagship claim is a causal story about something a player can
see: *digits are laid out at the fixed width of `'0'`, which is why counting numbers do not jitter.*
It rested on one decompiler line:

```c
local_1d8._0_3_ = (uint3)*(ushort *)(glyphTable + 0x20);
```

A 16-bit value widened into a **3-byte** field is not the shape an advance width takes, so the line
was re-examined **at instruction level** with a disassembler rather than through the decompiler.

### RETRACTED: the table holds character codes, not advance widths

```
002AE931  movzx ecx, word ptr [r9 + rax*2]   ; code = TABLE[ch - 0x20]
002AE95F  mov   byte ptr [rsp + 0x30], cl    ; stored as CHARACTER data
002AE96D  mov   word ptr [rsp + 0x30], cx    ; one byte or two
002AE998  lea   rax, [rsp + 0x30]
002AE9FC  call  0x2a9f00                     ; the buffer is passed on
```

The loaded value is **written back out as text** into a NUL-terminated stack buffer whose address is
handed to `002A9F00`. A width would be accumulated, not stored as a character. The
`cmp ax, 0xDF / ja` choice between a one-byte and two-byte store is a **multi-byte encoding**
decision.

The real advance is `xmm8`, accumulated **after** that call — so per-character advance comes from
`002A9F00` (2,304 B, ~~unread~~ read in §14 *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13))*), and this function does not compute widths at all.

### RETRACTED: the `'0'` read is not hoisted, and is not a width

```
002AE97A  dec   bl
002AE97C  cmp   al, 1  / jne
002AE980  cmp   bl, dl / jg
002AE984  movzx eax, word ptr [r9 + 0x20]
002AE989  mov   word ptr [rsp + 0x30], ax    ; OVERWRITES the emitted character
```

Two independent errors in one sentence:

1. **It is inside the loop.** `002AEA96 jl 0x2ae920` is a backward jump to the loop head at
   `002AE920`. "Fetched once, outside the per-character loop" is false.
2. **It overwrites the output character**, conditionally, under a decrementing counter `bl` against
   a threshold `dl`. That is **padding** — emitting the character `'0'` — which fits the
   minimum-width clamp in step 1 and has nothing to do with spacing.

The arithmetic identifying entry 16 as `'0'` was correct. Everything built on top of it was not.

### SURVIVED: the power-of-ten table

Re-read from `.rdata`: `1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000`, with the
next word `12047` — so the table is exactly **nine** entries and ends where the document says.

### Why the error happened, and what it costs

The decompiler named a register `glyphTable`, and the document **inherited that name as a fact**.
Every later inference — advance widths, hoisting, anti-jitter, the modding advice about replacing a
font — descends from a variable name. This is the rule the evidence standard already carries,
*a decompiler's symbol is a claim about the bytes*, applied to a symbol that was never checked.

It also cost the most confident sentence in the document: **the player-facing claim was the least
evidenced part of it.** A story that explains something familiar is the one to attack first, not
last. Section 1 now says what is known and explicitly says what is not.

**What remains true:** the number→digits conversion, the power-of-ten table, the minimum-width
clamp, the shared 208-byte state block, and the cluster's membership and doors. Those were argued
from structure and are untouched.

## 11. `002AAE40` opened — 2026-09-03, session `repos-78`

This document cited `002AAE40` **at its entry only**, as did eight others. It is opened here.
**Nothing above is retracted.**

**Extent verified before reading**: 505 instructions, **ends `ret` at `002AB7C7`, no `jmp` leaves the
extent**, so the tail-call rendering hazard does not apply.

### It is a per-item emitter, and the first thing to say is a correction

**A first-pass reading of this function was wrong and is corrected here rather than published.** Counting
statically, the body has **sixteen distinct callees, each appearing exactly once**, with almost no
comparisons — a shape that reads like a linear registrar making sixteen one-time setup calls. It is
not one.

```
002AB67A  jmp/jcc -> 002AAFD2      a backward jump spanning almost the whole body
```

**There are two backward jumps, and the outer one makes nearly the entire function a loop.** Every one
of those sixteen call sites is *inside* it.

> **A count of call sites is not a count of calls.** "Sixteen callees, each called once" was a static
> fact stated as a behavioural one — the same error shape as *45 call sites read as 45 arms*, arrived
> at independently and caught only by looking for loops instead of trusting an instruction histogram.

### What it actually does

The instruction mix is the tell that the histogram-based reading missed:

| | count |
|---|---:|
| `mov` | 131 |
| **`movups`** | **78** |
| **`movss`** | **50** |
| **`movaps`** | **34** |
| `cmp` | 10 |

**162 of 505 instructions are SSE moves.** The low comparison count is not "no branching logic" — it is
float work, which does its selection with `cmov` and arithmetic instead.

Per iteration the loop writes four-component records:

```asm
002AB271  mov   dword ptr [r11 + 0x38], 0x3f800000     ; 1.0f
002AB279  mov   dword ptr [r11 + 0x3c], 0x3f800000     ; 1.0f
002AB281  mov   dword ptr [r11 + 0x18], 0x3f800000
002AB289  mov   dword ptr [r11 + 0x1c], 0x3f800000
...
002AB498  movss dword ptr [rbp + 0x5c], xmm7
002AB49D  movss dword ptr [rbp + 0x60], xmm10
002AB4A3  movss dword ptr [rbp + 0x64], xmm7
002AB4A8  movss dword ptr [rbp + 0x68], xmm10
```

**Constant `1.0f` written into two pairs of slots, and computed pairs written into four consecutive
floats** — the shape of a textured quad's corners, emitted once per loop iteration. The function saves
`xmm9`, `xmm13`, `xmm14` and `xmm15`, which is a register budget no integer formatter needs.

It also keeps a **capped counter**:

```asm
002AB4BA  inc dword ptr [rcx + 0x10d4]
002AB4C0  cmp dword ptr [rcx + 0x10d4], 0x14      ; 20
002AB4C7  jb  ...
```

and a flag at `[rcx+0x1102]` that is cleared before the loop and set after it.

### Two call families

- **`0017F7C0`, `0017F850`, `0017F880`, `0017F8C0`, `0017FA10`, `0017FB00`, `0017FC90`, `0017FD30`** —
  eight small functions, 21 to 133 bytes, all unnamed. A tight API called from inside the loop.
- **`002AC5F0` (7,489 B)** — itself on the *located, never opened* cut, cited by eight documents. **The
  largest thing this function calls is also unread**, so the chain does not bottom out here. *(§12 opens it,
  and the text-control page maps its dispatch, UQ-170 and UQ-177. Marked 2026-09-30, DD batch 13.)*

### What is not established

- [x] ~~**UQ-167.** What the emitted records are consumed by. The quad shape is read from the stores; **no consumer
      was traced.**~~ **UQ-167 answered 2026-09-15 (FABLE): the consumer is the font painter's
      draw-one-glyph, `001E8070`, reached through the adapter `0017F7C0` — and the answer was already
      on this page, one bullet below the question.**
      - **The record is at `[rbp + 0x30]`, and that is checked the strict way.** The loop finishes the
        quad at `002AB498`–`002AB4A8` (the four corner floats at `rbp+0x5C`–`rbp+0x68`, i.e. record
        `+0x2C`–`+0x38`) and calls `0017F7C0` at `002AB4AE`. The **last write to `rcx` before that
        call** is `lea rcx, [rbp + 0x30]` at `002AB450`, so the record pointer is `rbp + 0x30` and not
        the frame base.
      - **`0017F7C0` copies exactly 160 bytes and forwards.** It copies `[rcx + 0x00]` through
        `[rcx + 0x9F]` in ten `movups` pairs into a stack buffer at `rsp + 0x20`
        (`0017F7CC`–`0017F824`), fetches the painter with `001B5FA0`, and calls `001E8070`.
        **`0xA0` = 160 bytes, which independently confirms the "160-byte record" that
        [the font painter's public API](../../99-Unresolved-Residual/Glyph-Run-Rendering/the-font-painters-public-api.md)
        §2 names** — the size was read there from the painter's side and here from the caller's, and
        they agree.
      - **So the loop is a glyph emitter, not a formatter that happens to touch floats.** Each iteration
        fills one 160-byte glyph record and hands it straight to the painter; the `1.0f` pairs and the
        four computed corners are that record's fields.
      - **Noted because it is a process failure, not a research one.** The adapter table immediately
        below this question already said *"`0017F7C0` → `001E8070` draws one glyph from a 160-byte
        record"*, answered on 2026-09-14 by the same author who left `UQ-167` open. **The consumer was
        named on the page while the row asking for it stayed unticked** — an answer filed *beside* the
        question instead of *into* it. Only the `rcx` check and the copy extent above are new.
- [x] ~~What the eight `0017Fxxx` functions do. All unnamed, all small, all called from the loop.~~ **Answered 2026-09-14
      (FABLE), from a page this section did not cite.** All eight are adapters. Each fetches the font painter
      `001B5FA0()` = `[01F811F8]` and forwards to one of its methods
      ([the font painter's public API](../../99-Unresolved-Residual/Glyph-Run-Rendering/the-font-painters-public-api.md) §2):
      - `0017F7C0` → `001E8070` draws one glyph from a 160-byte record.
      - `0017F850` → `001E8580` flushes and presents, inside the `"display : draw Font"` scope.
      - `0017F880` → `001E93C0` is a metric that falls back to 23.0.
      - `0017F8C0` → `001E9860` maps a codepoint to a glyph index.
      - `0017FA10` → `001E9920` begins a run.
      - `0017FB00` → `001E9C80` sets the 4×4 transform.
      - `0017FC90` → `001E9C40` sets the corner gradient.
      - `0017FD30` → `001E9D20` selects with an owner key.
- [x] **UQ-168.** What the counter capped at `0x14` counts, and what the `[rcx+0x1102]` flag gates.
      ***UQ-168 narrowed 2026-09-15 (FABLE): the counter half is answered; the flag half is not, and the
      row stays open for it.*** *(Both halves are answered 2026-09-18 at the end of this item, where the flag is the
      measurer's top-level latch; the narrowings between keep their history. Marked 2026-09-30, SWE2-CONTRACT for OPUS,
      DD batch 13.)*
      - **The object is the global at `[0209CC40]`, and `+0x10D4` counts items in the current BATCH.**
        Both increment sites load it from that global first — `002AB4B3` in this loop and `002AA455`–
        `002AA45F` in `002A9F00`, which advances a write cursor `[0209CC50]` by **`0x50`** per item
        beforehand. On reaching `0x14` = **20** the code calls `002B4730(1)` and then **writes the
        counter back to 0** (`002AB4DA`). A count that resets the moment it hits a fixed cap, beside a
        cursor that advances per item, is a batch.
      - **`002B4730` is the flush, and its shape says submission record.** It backs the shared write
        cursor `[0209CC50]` up by `0x10`, stores it back, sets `[cursor + 0xC] = 1`, then computes
        `(cursor − [0209E5A0]) >> 4` — **an index in 16-byte units from a second base** — sets **bit 28**
        of it (`bts eax, 0x1c`) and writes that word and a zero to `[0209E5A0]`
        (`002B4736`–`002B476C`). A 16-byte-granular offset carrying a tag bit, written to the head of a
        buffer, is a submission/packet header rather than anything text-specific.
      - **So the cap is not a text limit.** Twenty is how many items this object batches before it
        emits one record; the text loop is simply one of its producers, and `002A9F00` is another.
      - **The flag `+0x1102` is NOT answered. What is established:** this loop clears it before the
        loop (`002AAFE7`) and sets it after (`002AB691`), `002AF340` also clears and sets it, and its
        **only reads are three sites, all inside `002AC5F0`** — the 7,489-byte function this page has
        never opened. Two are branches and one is a value:
        - `002AD2B8` — `cmp byte [rax+0x1102], r15b` then `je`. **`r15d` is zeroed at `002AC622` and is
          not reassigned before this point**, so here the test is *"if the flag is clear, skip"*.
        - `002ADD31` — the same shape, but it sits **after** `002ADA77` (`mov r15d, 1`), so `r15b` is
          path-dependent and **the polarity of this one is not established**. Saying it matches the
          first would be a guess about control flow that was not traced.
        - `002ACA9E` — `movsx ebx, byte [r8+0x1102]`: the flag is taken as a **value**, not a branch,
          immediately before `002A9F00` is called.
        *Bound:* a displacement scan sees `[reg + 0x1102]`; a read through another addressing form
        would not appear.
      *Narrowed 2026-09-14 (FABLE): the counter is answered; the flag is placed but not named.*
      - **The counter** is dword `+0x10D4` of the text context `[0209CC40]`. It counts the **glyphs written into the current
        draw packet**.
        - Each glyph draw (`0017F7C0`) is followed by `inc [ctx+0x10D4]` (`002AB4BA`).
        - At 20 the formatter calls `002B4730(1)` and resets the count (`002AB4C0`–`002AB4DA`).
        - `002B4730` closes the packet: it writes a header whose count is `(cursor − start) / 16` at `[0209E5A0]`,
          appends the terminator records and calls `RenderCommand_SubmitCurrentBufferAndSwap`. With argument 1 it
          opens the next buffer from `02EBEFC0[+[02EBEFF0] × 24]` (`002B4736`–`002B47FD`).
        - So glyphs are submitted in batches of at most twenty. The same `inc` / `cmp 0x14` / reset appears in the
          sibling formatters (`002AA45F`, `002AAD5F`), and another `inc` sits at `002B0CE9`.
      - **The flag** is byte `+0x1102` of the same context.
        - It is cleared before a formatting loop and set after it (`002AAFE7`, `002AB691`; `002AF49C` / `002AF667`).
        - The 7,489-byte formatter saves and restores it around its nested formatter call (`002ACA9E`, `002ACACF`).
        - When it is set, that formatter re-measures through the same `002B2150` → `002B1F20` pair that
          `002AAE40` runs right after setting it (`002AD2B8`–`002AD2E9`). Elsewhere it takes a width from the style
          byte `+0xAA` (`002ADD31`–`002ADD49`).
        - What the set state means is not named.
      ***ANSWERED 2026-09-18 (FABLE) — the counter was placed on 2026-09-14 (glyphs per draw packet, twenty), and the flag is the measurer's top-level latch.** A size-aware sweep of every access at displacement `+0x1102` finds twelve sites, all in the text range: five writers and three readers, no others. The measurer `002AC5F0` sets the byte to 1 on entry (`002AC6DD`); every glyph drawer drops it to 0 for one glyph emit and restores 1 after — `002AAE40` at `002AAFE7` / `002AB691`, `002AF960` at `002AFA6C` (`sil` = 0) / `002AFB32`, `002AF340` at `002AF49C` / `002AF667` — and the pager `002A9F00` clears it at `002AA0ED`; around its own nested pager call the measurer saves the byte into `bl` and restores it (`002ACA9E`, `002ACACF`). The only tests are the two measurer arms whose side effects must not fire when the measurer runs *inside* a draw: the justification arm (`%&'`) stores the selector to `+0x1104` and then calls the width-to-x measurement `002B2150` only when the latch is 1 (`002AD2B8`..`002AD2D3`, `r15b` = 0 there), and the indent arm (`5` / `6`) writes the parsed indent `+0xAA` to its out-parameter only then (`002ADD31`..`002ADD49`; `r15b` is 0 on that path too, the `002ADA77` store of 1 belongs to the other branch). So `+0x1102` reads *“the measurer owns the context at top level”*: 1 while `002AC5F0` is measuring a line, 0 whenever a drawer has re-entered the text machinery to emit a glyph, which is when re-measurement must not recurse. Static: the twelve sites read.*
- [x] ~~`002AC5F0` — 7,489 bytes, unopened, and the natural next target for this document.~~ **Closed 2026-09-14 (FABLE): opened in §12 below** (session `repos-78`, 2026-09-03), which is why this box is stale rather than answered here.

## 12. `002AC5F0` opened — 2026-09-03, session `repos-78`

Section 11 opened `002AAE40` and ended by naming `002AC5F0` — 7,489 bytes, cited by eight documents,
never read — as the point where that chain failed to bottom out. It is opened here.

**Extent verified first**: 1,658 instructions, **no `jmp` leaves the extent**. The function's last
instruction *is* a `jmp`, at `002AE32C`, but its target `002ACFE7` is inside the body — a loop back
edge, not a tail call. **That distinction is the whole of the hazard**, and it is the reason to check
the target rather than the mnemonic.

### The signature, read from the entry and the writes

```c
void FUN_002AC5F0(void *ctx /*rcx*/, char **cursor /*rdx*/, void *arg3 /*r8*/, int *out /*r9*/)
{
    *out = 0;                                   /* 002AC628 */
    if (**cursor == '\0') return;               /* 002AC645 — empty string, nothing to do */
    ...
}
```

Two argument roles are established by how they are written, not by their types:

- **`cursor` is a `char**` that the function advances.** `mov qword ptr [rdi], …` occurs at **six**
  sites. The caller passes a pointer *to* its string pointer and gets it back moved forward.
- **`out` is an `int*` status.** Zeroed at entry, then written at **ten** sites — `1` at five of them,
  computed values at the rest.

> **This is why seven different functions call it.** Each hands over a cursor and a status slot and
> lets this function consume as much of the string as it handles. **It is the shared consumer at the
> bottom of the text path**, and every caller's loop is built around the cursor it returns.

### Callers

`002A8C50` (3,363 B), `002A9F00` (2,304 B), `002AAE40` (2,440 B — section 11), `002AF340` (1,563 B),
`002B1FB0` (246 B), `002B2150` (861 B), `002B5730` (383 B). **Seven, all inside the `002Axxxx` /
`002Bxxxx` text cluster**, and `002A9F00` and `002B2150` are also called *by* `002AAE40`, so the
cluster is mutually recursive rather than layered.

### Shape

| | |
|---|---:|
| instructions | 1,658 |
| distinct callees | **44** (108 call sites) |
| backward jumps | **61** |
| `movups` / `movss` | **212 / 99** |
| string literals referenced | **0** |

**Same profile as `002AAE40`, one order of magnitude larger**: byte-at-a-time character fetches feeding
bulk SSE stores, through the same small `0017Fxxx` render API. The float constants it loads are
`0.25`, `0.5`, `0.65`, `1`, `3`, `-3`, `10`, `15`, `16.6`, `24`, `90`, `100`, `128` — **layout
quantities, not formatting ones**; `1.8446744073709552e19` is the compiler's unsigned-conversion
constant and means nothing here.

### What this is, and what was not read

**Established:** the argument protocol, the empty-string early exit, that the cursor is advanced and
the status is written, the caller set, and the structural profile.

**Not read:** 1,658 instructions were surveyed, not decoded. In particular —
*(2026-09-30, DD batch 13: the dispatch is now mapped arm by arm on [the text control-code
language](the-text-control-code-language.md) §2, UQ-170 and UQ-177, and every item below is answered.)*

- [x] ~~**UQ-169.** **What the status values mean.** `1` at five sites and computed values at five more; no consumer
      was traced.~~ **ANSWERED 2026-09-14 (FABLE), by `UQ-179`:** the value is a character count. Its consumers are
      the emitter (`002AA6B5`–`002AA6FF`), which spends it against the painter's countdowns, and `002AAE40`
      (`002AB5C6`), which adds it to a running count. It is 1 for five arms, the inserted string's count for `.`,
      and 0 otherwise ([the control-code language](the-text-control-code-language.md) §2.6).
- [x] ~~**UQ-170.** **Which characters take which of the 61 loops.** The dispatch structure was not mapped.~~
      **ANSWERED 2026-09-17 (FABLE): the dispatch is mapped on the control-code page, and 48 of the 61 "loops" are not loops.** The dispatch structure is [the text control-code language](the-text-control-code-language.md) §2.2–2.6: one byte selects among fifteen token kinds through the 15-dword table at `002AE334` (`0x0B`/`0x0C`/`0x0D` and everything from `0x10` are ordinary characters), `0x0F` introduces a two-byte escape whose ASCII second byte selects one of **thirty-four** arms (§2.5, §9), and every arm was read (§2.6). The *61* is a count of BACKWARD BRANCHES in `002AC5F0`, re-enumerated today: **48 are the arms' jumps to the shared exits** `002ACFC2` (return 1), `002ACFB4` and `002ACFE7`, which sit *before* the arms in address order, so every arm's *consume and continue* is a backward `jmp` and none of them loops. **Thirteen are loops, and each has an owner:** the outer token loop `002AC940`–`002ACB12` (every byte of the run, `and al, 0x7F` then the kind switch); two in the `0x0A` token arm (`002ACF10`–`002ACF21`, a forward scan for a `0x02` or `0x05` terminator byte, and `002ACF26`–`002ACF8A`, which re-runs the measure after the scan); and **eight NUL-terminated string-length scans, two each, in four escape arms** - `*` (`002AD5A3`, `002AD600`), `.` (`002ADA20`, `002ADA60`), `8` (`002ADE47`, `002ADE82`) and `>` (`002ADF40`, `002ADF80`) - every one the same three instructions, `inc i / cmp byte [base+i], 0 / jne`. So *which characters take which loops*: every character takes the outer loop; the `0x0A` token takes the two terminator loops; the four selectors that insert a string measure it twice; no other arm loops at all. Static; the branch census is one regex over the listing and the arm ranges are the control-code page's addresses.
- [x] ~~**UQ-171.** What `arg3` is. It is stored to `r12` at entry and its uses were not followed.~~
      **ANSWERED 2026-09-14 (FABLE): the caller's pen, x at `+0`, y at `+4`.**
      - The line break `0x02` writes a justified x into `+0` and adds the line height to `+4` (`002AC712`–`002AC796`).
      - The tab `2` reads `+0` as the current x (`002ADC9F`).
      - At a line start, justification `%&'` (`002AD2E9`) and indent `5` (`002ADD49`) write `+0`.
      - The emitter passes its pen record (`r15`, which it advances at `002AA0D2`–`002AA0E8`).
      - `+8` and `+0xC` are read by the `0x0E` and `*` arms and are not named here. *(Proposed row P7, §15, 2026-09-30:
        the two arms copy them into locals at `002AC8A4`/`002AC8BD` and `002AD690`/`002AD69B`.)*
        *Answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15, §15b P7):* the copies feed only `002A9F00`, which reads `+0` and `+4`;
        nothing reads `+8` or `+0xC`.

      See [the control-code language](the-text-control-code-language.md) §2.6.
- [x] ~~What the two globals zeroed at entry (`mov qword ptr [rip + …], rax` with `rax = 0` at
      `002AC62E` and `002AC638`) hold.~~
      **ALREADY ANSWERED BY §5 OF THIS PAGE — ticked 2026-09-13 (OPUS) as a stale checkbox, not as
      new work.** The two stores at `002AC62E` and `002AC638` write **`0209CC60`** and
      **`0209CC68`**, and §5 identifies both while describing the draw loop:
      - **`0209CC60` is the scale** — the quad's corners are laid at `pen.x`, `pen.x + scale` and
        `pen.x + w × scale` (`002AA498`–`002AA4E4`).
      - **`0209CC68` is the post-glyph pen advance** — `pen.x += [0209CC68]` at the loop tail
        (`002AA734`–`002AA747`), paired with `0209CC6C` before the glyph. §5 calls them *"a
        caller-owned pair (written as one qword by the callers)"* and lists this formatter among the
        eight that set them.
      So zeroing them on entry is **this formatter clearing an inherited scale and advance before it
      writes its own** — consistent with §5's note that it zeroes both on its early-out at `002AE848`
      and `002AEAC2` and then stores its running total into `0209CC68` at `002AEAC9`.
      *The question was answered roughly 270 lines above where it is asked.*
- [x] **UQ-172.** Whether the `002Axxxx`/`002Bxxxx` mutual recursion terminates on cursor progress or on a depth
      counter — `002AAE40`'s counter capped at `0x14` is a candidate and was not confirmed.
      *Narrowed 2026-09-14 (FABLE, UQ-168): the candidate is refuted.* The counter capped at `0x14` is the glyph count of
      the current draw packet, and it is reset each time a batch is submitted. It does not count nesting, so it cannot
      bound the recursion. The one nesting-aware store read so far is the save and restore of the `+0x1102` flag around
      the nested formatter call. Termination on cursor progress stays the open reading.
      ***ANSWERED 2026-09-18 (FABLE) — on cursor progress and span cutting; there is no depth counter.** The recursion is one strongly connected component of nine functions in the text range (Tarjan over `edges.tsv` restricted to `002A8000`..`002B5000`): the pager `002A9F00`, the measurer `002AC5F0`, `002AE610`, the draw `002AF340`, `002B2150`, `002B2970`, `002B2DF0`, `002B41F0` and `002B43C0`. Its 29 in-cycle call sites were read, and every one recurses in one of two ways. *Advance:* the callee receives the cursor after the escape being handled has been consumed — `inc rdx` before `002B2150` (`002AC6F0`, `002ACDDB`, `002AF673`) or `add qword [rdi], rax` by the tag's length before the nested call (`002AC871`, `002AD8E5`). *Cut:* the caller bounds a sub-span by overwriting its end byte with 0, recurses on the sub-span, and restores the byte after — eleven cut-and-restore pairs (`002ACA18` / `002ACA1C`, `002AD548` / `002AD54C`, `002AD577` / `002AD57B`, `002AD5B1` / `002AD5B6`, `002AD60E` / `002AD613`, `002ADA36` / `002ADA3B`, `002ADA6E` / `002ADA73`, `002ADE5D` / `002ADE62`, `002ADF56` / `002ADF5B`, `002ADF8E` / `002ADF93`, `002B2F20` / `002B2F26`), so the callee's text is strictly shorter than the caller's. The remaining sites hand the callee a freshly built state block on the caller's stack whose cursor is one of those two. And nothing in the cycle counts nesting: the only two candidates, `+0x10D4` and `+0x1102`, are the packet glyph count (reset at twenty, UQ-168) and the measurer's top-level latch (a save-and-restore byte, not a count); no in-cycle body increments and compares any other field across a call. Finite text plus strictly shorter or strictly advanced input on every recursive edge is the termination argument. Static: the cycle computed from the edge list, the 29 sites read.*

**This document should not be read as saying the text path is now understood.** It says the shared
consumer at its bottom has a name, a signature and a caller set, where before it had an address.

## 13. `002A8C50` opened — the text markup parser, and the tag vocabulary

`002A8C50` (3,363 B) topped the cut's new **bytes-per-line-of-prose** ranking at **1,121 B/line**:
three documents cite it, and between them they spend about three lines on it. **The ranking put the
widest body-to-claim gap first and this was it.**

**Extent checked**: 761 instructions, ends `ret` at `002A9972`, **no `jmp` leaves the extent**.

### The shape is the clue

| | count |
|---|---:|
| `movups` | **208** |
| `cmp` | 63 |
| `jne` | 33 |
| backward jumps | **1** |

**208 sixteen-byte moves with a single loop** is not a processing pass — it is a large structure
snapshotted to the stack, modified, and written back. The destinations confirm it: 76 stores through
the stack copy, 28 back through the argument pointer.

### Text is variable-width, and `0x20` is the discriminator

```asm
002A8D84  movzx ecx, byte ptr [rdi]
002A8D87  cmp   cl, 0xf
002A8D8A  jbe   <control path>
002A8D8C  lea   rax, [rdi + 1]
002A8D90  add   rdi, 2
002A8D94  cmp   cl, 0x20
002A8D97  cmovae rdi, rax        ; >= 0x20 -> advance 1;  < 0x20 -> advance 2
```

**A byte below `0x20` consumes two bytes of the string; `0x20` and above consumes one.** That is the
whole width rule, in one `cmovae`.

### `0x0F` introduces a tag, and the tag character selects a field

Bytes `0x0E` and `0x0F` are the two escape introducers. After `0x0F`, **the next byte is a tag**, and
each tag writes a specific field of the render-state structure:

| tag | char | what it writes |
|---|---|---|
| `0x2D` | `-` | `word [state + 0x8E]` |
| `0x2F` | `/` | a magic-divide result; ~~also sets `byte [state + 0xA0] = 1`~~ a payload above 30 sets `+0x9C = 30` and `+0xA0 = trunc(v / 30)`, halved with a floor of 1 when `00248F20()` returns 1; a payload of at most 30 sets `+0xA0 = 1` *(corrected 2026-10-02, OPUS: `002A8C50+0x5BE`–`002A8C50+0x60D` and `002A8C50+0x75E`)* |
| `0x23` | `#` | `word [state + 0x88]` |
| `0x22` | `"` | `word [state + 0x90]`, reading `[state + 0x9E]` |
| `0x3B` | `;` | a 16-byte `movups` to the stack copy at `+0x40` |
| `0x70` | `p` | `dword [state + 0xB0]` |
| `0x3D` | `=` | `[state + 0xAE]` |

**Seven tags with distinct destinations**, each parsed by the same shape: read the byte after `0x0F`,
compare, write a field, rejoin the walk.

### A lookahead over a 64-bit tag set

```asm
002A9738  movabs r8, 0x4100400000000000
002A9764  cmp    cl, 0x3e
002A9767  ja     0x2a9776
002A9769  movzx  eax, cl
002A976C  bt     r8, rax             ; is the NEXT tag in the set?
002A9776  cmp    cl, 0x70            ; 'p'
002A977B  cmp    cl, 0x40            ; >= '@'
```

**The constant is a character set, addressed by `bt`.** Decoded by evaluating the mask rather than by
eye — its set bits are **46, 56 and 62**, which are **`.` (`0x2E`), `8` (`0x38`) and `>` (`0x3E`)**.
The same constant is loaded at `002A8D67` and `002A9738`, so **one set is consulted twice**.

> **So the parser looks one tag ahead** and treats `.`, `8` and `>` as one class, `p` as a second, and
> anything `>= '@'` as a third. **Three tag characters appear only in this lookahead set** and have no
> field-writing case in the body — they are recognised, not handled, here.

**The full tag vocabulary this function is aware of is therefore ten characters**:
`"` `#` `-` `.` `/` `8` `;` `=` `>` `p`.

### Modding notes

- **Control bytes are two bytes wide, printable characters one.** Any tool measuring FFXII text length
  by counting bytes will over-count every tag.
- **`0x0F` + a tag character is the markup form**, and the seven handled tags each land in a different
  render-state field — so changing one tag's byte changes which field is written, not just its value.
- The state structure is copied to the stack whole and written back whole. **A hook that edits the
  structure mid-call will be overwritten** by the copy-back.

### What is not established

- [x] **UQ-173.** What each written field *means* — `+0x88`, `+0x8E`, `+0x90`, `+0x9E`, `+0xA0`, `+0xAE`, `+0xB0`.
      They are named by offset, not by role. *Narrowed 2026-09-15 (OPUS): **one of the seven is traced end to
      end**, and the other six are not.*
      - **Only `+0xAE` has a tight enough displacement set to trace safely.** A scan over `+0x88`, `+0x9E`
        and `+0xAE` (positive control `0xae:002A8C50:w`, 38,161 bodies) returns **1,020 sites in 691
        functions** for `+0x88` and **316 in 229** for `+0x9E` — generic offsets, where displacement
        identity is not object identity and no conclusion is available. `+0xAE` returns **12 sites in 9
        functions**, almost all in this `002Axxxx`/`002Bxxxx` cluster.
      - **`0xFF` is a reset, applied by four functions.** `002A8F0A`, `002AC262`, `002AFB63` and `002B3DBB`
        each store the literal `0xFF` — read as a signed byte that is **-1, “none”** — before the parse.
      - **The field is an OUT-PARAMETER, not a value the tag writes.** Three of those functions pass its
        *address*: `002A96EE lea rdx, [rsi+0xae]` (and `002AE1DB`, `002B3E07`). At the `=` arm the walker
        does `lea rdx, [rsi+0xae]` / `mov rcx, rdi` / `call 003FFAB0`, then **`add rdi, rax`** — the
        parser's return value advances the cursor, exactly as the `0x0E` arm uses `003FFDF0`.
      - **What lands in it.** `003FFAB0` is one of the eleven `003FFAB0`–`003FFF10` parsers ([the text
        control-code language](the-text-control-code-language.md) § *code lengths are decided by the
        parser*), and its low-three-bits-zero path is already recorded there: `0039BA00(r8b)` returns a
        pointer and the output byte is `[rax]`. So **`+0xAE` receives the first byte of a record looked up
        by a 7-bit id carried in the text**, and the code is **3 bytes** long (`mov eax, 3`). The walker
        then copies it to a frame local at `002A9709`.
      - *(This bullet's `+0xAE` item and the six untouched fields are answered 2026-09-25 and 2026-09-26 below. Marked
        2026-09-30, SWE2-CONTRACT for OPUS, DD batch 13.)*
      - **Still not named:** *what that byte is*. The lookup's table is not identified here, so `+0xAE`'s
        mechanism is traced and its meaning is not. **And six of the seven fields remain untouched** —
        `+0x88`, `+0x8E`, `+0x90`, `+0x9E`, `+0xA0` and `+0xB0`.
      **Narrowed further 2026-09-18 (FABLE), by cross-reference to [the text-control page](the-text-control-code-language.md) (UQ-177):* three of the seven are placed there from their readers. `+0x88` is the page-wait tick count the `#` escape stores; the stepper `002ABF70` decrements it in mode 5 and fires the scroll at zero, and the pager `002A9980` treats 10,000 as wait for the decide button. `+0x90` / `+0x92` are the target-line pair the same stepper advances by `+0xA0`. `+0xB0` is the mode byte with flag bits above it: bit 19 is the waiting flag the parser tests at a page end, bit 21 the one-shot `9` sets, bit 25 the `$` guard, bit 26 set beside 19. ~~`+0x8E`, `+0x9E` and `+0xA0`'s own meanings stay as above.~~*
      **Narrowed 2026-09-25 (FABLE, Claude Opus 5.5): `+0xA0` and `+0x9E` are the reveal stepper's step size and lag
      bound, and `+0x9C` is its rate; `+0x8E` is a written-only snapshot of the head.** Static; the stepper `002ABF70`, the
      initialiser `002AC1E0` and the parser's stores were read. The census covers every access in the text cluster
      `002A8000`–`002B6000` at the fields' own widths. `movups` reads of `+0xA0` are 16-byte block copies, not uses of
      the byte.
      - **Rate `+0x9C`.** Each tick adds it to the accumulator `+0x9B`, and a step fires when that reaches 30
        (`002ABFFC`–`002AC010`, `002AC06B`–`002AC0E3`). So 30 means one step a tick. The default is 30
        (`002AC20D`), and the `/` escape sets 30.
      - **Step `+0xA0`.** A step advances the target `+0x90` (keeping the old value in `+0x92`) and the head `+0x8C`
        by `+0xA0`, with the head capped at `0x7D00` (`002AC031`–`002AC042`, `002AC14A`–`002AC17E`). The default is 1
        (`002AC21D`). `/` sets `trunc(v / 30)`, which is halved with a floor of 1 outside frame-dispatch mode 2.
      - **Lag bound `+0x9E`.** The default is 8 (`002AC232`). The lag counter `+0x9D` moves toward it by `+0xA0` per
        step (`002AC0F0`–`002AC129`), and the target advances only while it trails the head by at least `+0x9D`
        (`002AC12F`–`002AC15B`). So the target trails the head by the lag `+0x9D`, and `+0x9E` bounds the lag. Six other sites read
        it: three in the parser `002A8C50`, and three in bodies of the `002B3xxx` range that were not read here.
        *(Read 2026-09-30, DD batch 13, §15 N6: `002B32D0`, `002B3C30` and `002B3D50` each start the target `+0x90` at
        minus the lag bound, so a reveal begins that far behind the head.)*
      - **Snapshot `+0x8E`.** It takes the head's value at each step (`002AC099`, `002AC0F7`), and target − 1 in the
        parser (`002A91DE`). Its eight accesses in the cluster are all **writes**, so any reader lies outside it.

      *Not established:* the unit these counters count in (the text-control page calls `+0x90` / `+0x92` the
      target-line pair), and who reads `+0x8E`. *(Both answered 2026-09-26 below: characters, and no reader. Marked
      2026-09-30, DD batch 13.)*
      **Narrowed again 2026-09-25 (FABLE, Claude Opus 5.5): `+0xAE` is the `=` escape's parameter, and in this build it
      is decoded, reset and carried but never used — and no shipped text contains the escape.** Static, plus a data
      census.
      - **How it is set.** `0F 3D p1 p2` is decoded by `003FFAB0` into `+0xAE`, through the out-pointer the page records
        above (`002A96EE`, `002AE1DB`, `002B3E07`). When `p1`'s low three bits are non-zero it is the literal `p2 & 0x7F`,
        with bit 7 taken from `p1`'s bit 6. Otherwise it is the first byte of entry `p2 & 0x7F` of the special-character
        translation table (`0039BA00`, `[02AEE870]+1`) — the same decoding `UQ-176` read for `9`.
      - **What else touches it.** Four functions reset it to `0xFF` (none). The parser `002A8C50` reads it once, only to
        copy it into its frame-local state copy at `002A9702`: `[rbp+0x2E]` is the local copy's `+0xAE`, because
        `rbp − 0x80` is that copy's base, which the parser hands to `002AC5F0`. `002A3250` and `002A6C40` store it back
        from their own local copies. Those ten accesses, in bodies from `002A3250` to `002B3D50`, are every access to `+0xAE` in the text
        cluster, and none branches on the byte or computes with it.
      - **The data.** Every `st2e` bank (407) and `hdat` handbook (101) in the full extract was scanned for `0F xx`
        pairs, and `0F 3D` occurs **0** times. *Control:* the same scan counts `0F 2F` (`/`) 302 times, `0F 3C` (`<`)
        1,432 times and `0F 31` (`1`) 1,333 times, and it reproduces the `0` for `0F 39` that `UQ-176` records.
      - So `+0xAE` stays at `0xFF` in shipped play, and what `=` would have selected is not recoverable from its uses.
        Other text formats (bank-format files) were not scanned.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): the counters count characters, and `+0x8E` is written and never
      read in that band — so all seven fields now have their meanings.** Static.
      - **The unit.** The parser `002A8C50` keeps a running count in `r14d` and stops emitting once it reaches the head
        `+0x8C` (`002A974C`). For a character byte above `0x0F` it advances one byte (two for a `0x10`–`0x1F` lead
        byte) and adds exactly 1 (`002A8D84`–`002A8D9B`). A token handled by `002AC5F0` adds what the handler reports:
        1 for each line-break arm (`002ACCE3`, `002ACDD0`, `002ACEF0`), and for an inserted string the nested run's own
        head (`002ADAA4`). So the head, the target pair `+0x90`/`+0x92` (compared with the same count at
        `002A8E03`/`002A8E0C`), the step `+0xA0` and the lag are all in **characters**, and a line break is one
        character.
      - **`+0x8E`.** Every word access to it in the code band 0x280000–0x2D0000 (eight, in six functions) is a write, and no dword
        read at `+0x8C` covers it. Only the 16-byte state copies carry it. So it is a snapshot nothing reads, at least
        within that band.
      - **The seven, in one line each:** `+0x88` page-wait ticks (`#`); `+0x8E` head snapshot (unread); `+0x90` target
        (`+0x92` its previous value); `+0x9E` lag bound; `+0xA0` step; `+0xAE` the `=` parameter (never authored);
        `+0xB0` the mode byte and flags.
- [x] ~~**UQ-174.** What `0x0E` introduces. It has its own branch and was not followed.~~
      **UQ-174 adjudicated 2026-09-15 (FABLE): `0x0E` introduces an IN-TEXT SELECTION LIST — a choice
      prompt embedded in a message.** Two independent ends now agree, and neither was derived from the
      other:
      - **The record's shape says list.** `003FFDF0` decodes a count `n`, a flag byte, an optional
        bitmask of ⌈n/7⌉ bytes carrying **one bit per item**, and then **`n` length-prefixed
        strings** ended by a zero byte. A count, a per-item bit and one string per item is the shape of
        a menu, not of a formatting directive.
      - **The runtime's use says cursor.** `002A5590` stores `n` at `+0x3C7` and seeds `+0x3B9` when it
        is still 0; and both reads of `+0x3B9` in `002A70B0` multiply it by the **font line metric**
        (`0017F880`) to produce a vertical offset. **An index times a line height is a cursor on a
        stack of lines** — which is what a selection list needs and what a formatting code does not.
      **That is enough for the question as asked** — *what does `0x0E` introduce* — and it is the
      reading §above already called "reads as", now carried by the on-screen use as well as the shape.
      - **Residue, carried rather than absorbed: what the per-item mask gates.** One bit per option is
        consistent with enabled/disabled, already-chosen, or visible — the decode shows the bit exists
        and where it lives, and nothing here shows what it *does*. **Asked separately as `UQ-381`
        rather than left as prose**, so it is counted as the open question it is.
        **ANSWERED 2026-09-18 (FABLE): in this build the record's own mask gates nothing - it is decoded only to be stepped over - and the options a list leaves out are chosen by a different mask, one the scripts set.** (1) *The inline mask has no reader.* `003FFDF0` returns the mask pointer through its seventh argument. Each of its three callers points that argument at a stack local and never loads it: `002A5590` (`[rbp-0x50]`), the walker `002A8C50` (`[rsp+0x68]`) and `002AC5F0` (`[rbp-0x80]`). All three frames have `rbp = rsp + 0x100`, and neither spelling of any of the three slots is read; in `002AC5F0` the slot is later reused as the float output of a measuring call. What the bit meant to the code that once read it is not decidable from this executable. (2) *What does leave options out.* The text state's dword `+0x84` is a 32-bit mask, **bit set = option omitted**. `002B2D20` counts the clear bits among the first `n` - that is the visible count `002A5590` stores at `+0x3C8` - `002B2CE0` turns a visible index into the raw index of that clear bit, and `002B2CA0` clamps a visible index to the visible count; all three pass straight through for a list of more than 32. (3) *Where that mask comes from.* The script verb **`setaskselectignore(window, index)`** (`0475`, handler `00348540`) tail-calls `002E20D0(window, 1, index)`, which ORs `1 << index` into the dword at `+0x18` of the window's `0x68`-byte record at `0215F200` (eight windows; a zero second argument would clear the bit instead). The message-window opener `002E16B0` copies that dword into its open request at `+0x24` and zeroes the record's copy, so the mask is **one-shot per ask**; the window builders `002A6C40` and `002A6A80` pass the request's `+0x24` to `002B32D0`, which stores it at the text state's `+0x84`. (4) *In the shipped scripts:* 219 calls, 167 of them passing a loop counter as the index. The one read for shape, in `alc_c01`: the teleport-stone menu walks its 25 destinations, gives each unlocked one its name with `setmesmacro`, and calls `setaskselectignore(0, i)` for each one still locked. So of the three candidate meanings the row offered, the one the game actually implements is **visible / not offered**, and it implements it outside the record. Static plus the decompiled `us` scripts.
      - **An attempt at authored corroboration FAILED, and is recorded so it is not repeated.** The
        record shape validates itself — a correct decode consumes exactly to its own terminator — so a
        scan for real instances looked cheap. Over the 41 `us` and `common` `.bin` banks it returns
        **6 hits, all `n = 1`, all inside `battle_pack.bin` and all plainly byte runs rather than
        text**. Widened to the whole `plan_master` tree it returns hits in **678 files**, concentrated
        in `.ebp` **bytecode** at up to 94 per file. **Both results are noise, and the reason is
        specific: the game's text is not ASCII, so "is this a plausible option string?" cannot be
        answered without decoding the character set** (the `word.bin` / text-bank charset). Until that
        exists, an instance count from this scan would be unfalsifiable, so none is offered.
      *Narrowed 2026-09-14 (FABLE), not answered: the record's shape is read; what it means on screen is not.* The branch
      (`002A8FEE`) passes the cursor to **`003FFDF0`**, which decodes a variable-length record and returns its length
      (`002A9033` adds it):
      - `+1`, `+2`, `+3`: three 7-bit values (`& 0x7F`). The first is a **count `n`**.
      - `+4`: a flag byte. Bit 1 and bit 5 go to optional out-parameters, and bit 0 says a mask follows.
      - If bit 0 is set, a pointer to **⌈n / 7⌉ mask bytes**, seven bits per byte, one bit per item
        (`0x24924925` / `0x92492493` compute the ⌈/7⌉, `003FFE63`–`003FFE9D`). Otherwise the pointer is null.
      - Then a pointer to **a list of length-prefixed strings** (length `& 0x7F`, then that many bytes) ended by a
        zero byte (`003FFEB0`–`003FFED1`).

      Its three callers are the walker here, `002AC5F0` (the 7,489-byte function this page has not opened) and
      `002A5590`. `002A5590` finds the `0x0E` in a string with `xmlStrchr` (`002A56B2`), stores `n` at `+0x3C7`,
      derives `+0x3C8` from it through `002B2D20`, and copies that value into `+0x3B9` when `+0x3B9` is still 0
      (`002A573A`–`002A5753`). The shape reads as **an embedded list of `n` item strings with a per-item bit mask**, and
      `+0x3B9` looks like a selection index. That makes it a selection list inside a text.

      **The on-screen use is now traced, 2026-09-15 (OPUS): `+0x3B9` multiplies the font line
      metric.** A displacement scan over `+0x3B9`/`+0x3C7` (positive control `0x3c7:002A5590:w`,
      38,161 bodies) returns a tight set — **`+0x3B9` has 9 sites in 4 functions and `+0x3C7`
      has 4 in 3**, all inside this `002Axxxx` cluster. Both reads of `+0x3B9` in `002A70B0`
      (`002A7504`, `002A7637`) are the *same five-instruction shape*:

      ```asm
      call 0017F880            ; FontPainter_Metric, the 23.0f-fallback metric (§7)
      movzx ecx, byte [rbx+0x3b9]
      cvttss2si eax, xmm0      ; metric -> int
      imul ecx, eax            ; index x metric
      cvtdq2ps xmm6, xmm6      ; back to float, then 0024ABA0
      ```

      So the selection index becomes **index × line metric**, a vertical displacement in the
      painter's own units — the arithmetic of positioning the *n*-th line. That is what a
      selection list does on screen.

      **And the index is a seeded default, not an input cursor.** `002A2C00` writes it at
      `002A2CC6` from **`[rsi+0x22]` of a source descriptor**, inside a run of plain field copies
      (`[rsi+0x23]` → `+0x3BA`, `[rsi+0x40]` → `+0x1B0`, `[rsi+0x30]` → `+0x1A8`), so it is
      a bulk initialiser rather than an input handler. `002A5590` then overrides it from the
      `0x0E` record **only while it is still 0** (`002A573F`–`002A5753`): a default-then-override
      discipline.

      **Still not claimed, and deliberately:** whether the displacement moves a highlight, a
      cursor or the list itself, and therefore whether this is a “choice window”. Nothing
      read here distinguishes those, and the two consumers `002A6F80` (301 B) and `002A70B0`
      (1,639 B) were not opened beyond these sites.
- [x] ~~**UQ-175.** What `.`, `8` and `>` do. They are in the lookahead set with **no handler in this function**, so
      their handling is elsewhere.~~ **ANSWERED 2026-09-14 (FABLE):** they are handled by the interpreter `002AC5F0`, and
      they are the three codes that insert text ([the control-code language](the-text-control-code-language.md) §2.6).
      `.` inserts argument `n` of the caller's array (a string, or a number through `002AE610`). `8` inserts the name
      for an `i16` id (`002639E0`). `>` inserts the display name of the context's actor (`00263990`).
- [x] ~~Whether the `/` tag's magic divide is the same `0x88888889` family documented elsewhere in this
      database — **the shift was not read, and that constant alone does not fix the divisor.**~~
      *Answered 2026-09-14 (FABLE): same constant, divisor 30.* No register id carries this box, so it is not queued
      (ticked the same day; AUDIT-SEM accepted the wording).
      - **The divide.** The `/` arm `002A91EA` reads the tag's parameter byte `v` through `003FFAB0`. When `v > 30`
        (`cmp al, 0x1e`) it computes `imul 0x88888889; add edx, ecx; sar edx, 4` plus the sign correction
        (`002A9215`–`002A922D`). That is `trunc(v / 30)`, checked exhaustively over every signed byte (`-128..127`, no
        mismatch).
      - **The stores.** It writes 30 to `+0x9C` and the quotient to `+0xA0`. When `00248F20()` returns 1, meaning the frame
        dispatcher is not in mode 2, it halves `+0xA0` with a floor of 1 (`002A9235`–`002A925D`).
      - **The family.** The console's id 227 uses the same constant with `sar edx, 5` for 60
        ([arm catalogue slice G](../../00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-G-ids-204-235.md)).
        With the added `n`, the multiply gives `8n/15`, and the shift divides that by 16 or 32: 30 or 60.

## 14. `002A9F00` opened — where the advance actually comes from

Section 6 states *"advance widths are not in this function; they come from `002A9F00`, which is
unread"*, and files it as an open question. It is read here.

**Extent checked**: 511 instructions, ends `ret` at `002AA7FF`, no `jmp` leaves the extent.

### The answer is a negative, and it is the useful kind

**There is no per-glyph width table.** The pen is advanced from a small set of globals and one scaled
term, chosen by mode:

```asm
002AA0D2  movss xmm0, dword ptr [0209CC6C]     ; a global advance
002AA0DA  addss xmm0, dword ptr [r15]          ; r15 = the pen
...
002AA13A  cmp   byte ptr [rcx + 0x10fc], 2     ; a mode selector
002AA141  jne   skip
002AA143  movss xmm0, dword ptr [rbp - 0x6c]
002AA148  mulss xmm0, xmm14
002AA14D  mulss xmm0, dword ptr [rbp - 0x68]   ; a SCALED advance
002AA152  addss xmm0, dword ptr [r15]
...
002AA734  movss xmm0, dword ptr [0209CC68]     ; a third global advance
002AA742  addss xmm0, dword ptr [r15]
```

**Four spacing globals participate — `0209CC60`, `0209CC64`, `0209CC68`, `0209CC6C` — and every one
of them is in the zero-filled tail of `.data`.** They have **no value in the shipped image** and are
installed at run time, like the other engine tunables this database has found in that region. **A
reader dumping the executable to find the character spacing will find zeros.**

> **So character advance in this game is not metric data attached to glyphs.** It is a handful of
> runtime spacing constants plus a scale factor, and which one applies is decided by a mode byte at
> `context + 0x10FC`.

> **⚠ Corrected 2026-09-14 (FABLE): they are not constants, and one writer derives them from a glyph record.** A RIP
> scan of `0209CC60`–`0209CC6F` finds **121** references: **71 writes in 10 functions** (`002AAE40`, `002AC2F0`,
> `002AC5F0`, `002AE450`, `002AE610`, `002AEB20`, `002AF340`, `002AF960`, `002B0280`, `002B2150`) and 50 reads in 8.
> So the four slots are **run-time layout state that the text functions set before drawing**. They are not
> tunables installed once, and the zeros in the image mean nothing.
> - `002AE450` resolves one character through the font's two-level code map (`[font+0x20] + 0x30`, word tables at
>   `+0x14`) to an 8-byte glyph record. It stores the record's **12-bit width** (`[+4] & 0xFFF`) × scale at
>   `0209CC60` and its **12-bit height** (`[+4] >> 12 & 0xFFF`) × scale at `0209CC64`, then **width × scale + the
>   spacing float `[ctx+0x4C]`** at `0209CC68` (`002AE4E4`–`002AE529`).
> - This does not overturn the per-call pitch recorded at `AC-9` and in §5. `002AE450` measures the one character it
>   is given, and whether callers pass each drawn character or one reference character was not traced. The
>   character dispatcher `002AC5F0`, which this function calls at `002AA6A8` just before reading `0209CC68` at
>   `002AA734`, is among the writers.
>
> What is withdrawn is "constants with no glyph data behind them". Whether the pitch changes from glyph to glyph
> is not settled here.
> *Settled 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13, §15 N3): it does. This loop calls `002AC2F0` for every
> character (`002AA0CD`, inside the loop `002AA050`–`002AA74C`) before reading `0209CC6C` and `0209CC68`, and
> `002AC2F0` rebuilds the spacing block from that glyph's own advance field plus the spacing float `+0x4C`. Text is
> proportional. The number formatter calls it once, for `'0'`, which is why digits alone are monospaced.*

*Control for the negative.* The same reading **does** find a table read in this function —
`movsx rax, byte ptr [rbp+7]` indexing `00916560` at `002AA1A3` — and follows it: the byte is split
into a **high nibble and a low nibble**, shifted, and OR-ed into a 64-bit **GPU command word** built
across `002AA1B5`–`002AA20E`. **It selects a render mode, not a width, and it never reaches the pen.**
So "no width table" is a conclusion about where the values go, not a failure to find a table.

### A running width budget

```asm
002AA07D  subss xmm1, dword ptr [rbp - 0x50]
002AA086  movss dword ptr [rdx + 0x10e4], xmm1
...
002AA6CD  movss xmm0, dword ptr [rdx + 0x10e4]
002AA6D5  subss xmm0, dword ptr [rbp - 0x50]
002AA6DA  movss dword ptr [rdx + 0x10e4], xmm0
```

**`context + 0x10E4` is a float decremented per character** and read back later — a remaining-width
budget rather than an accumulated total. A `divss` followed by `comiss` against `1.0` at
`002AA4E4`–`002AA4EF` is the only normalised comparison in the body and is the natural candidate for
the wrap decision, **though what it gates was not followed.** *(Followed 2026-09-14 below: a render-strip break
every 1920 units. Marked 2026-09-30, DD batch 13.)*

### It shares the markup tag set with the parser

```asm
002A9FD9  movabs rsi, 0x4100400000000000
```

**The same 64-bit character-set constant decoded in section 13** — set bits 46, 56, 62 = `.` `8` `>`.
**Three sites in two functions now load it**, so the tag class is shared between the markup parser and
the per-character emitter rather than being local to either.

The function also opens by copying **~~`0x100`~~ `0xD0` (208) bytes of render state** *(corrected 2026-10-02, OPUS: thirteen 16-byte `movups` loads, `002A9F00+0x29`–`002A9F00+0xC3`)* to its stack frame in unrolled
`movups` pairs — the same snapshot-modify-write-back shape as `002A8C50` and `002AAE40`, and the
reason all three surface together on an SSE-density ranking.

### What is not established

- [x] ~~What the four spacing globals hold at run time, and who writes them.~~ **Answered 2026-09-14 (FABLE):** run-time layout state written 71 times by 10 text layout functions. One of them, `002AE450`, fills them from a glyph record's width and height and the spacing float `[ctx+0x4C]`. See the correction under the "character advance" paragraph above.
- [x] ~~What mode `2` at `context + 0x10FC` selects, and what the other modes do.~~ **Answered 2026-09-14 (FABLE): it is a
      one-byte latch that records the previous glyph's class and inserts a gap when the class changes.** In this function
      the glyph record's first dword `[table + index × 8]` is tested for **bit 31** (`002AA117`–`002AA131`):
      - **Bit set, latch at 2:** before the latch is set to **1**, the pen gains `2.3` (`009166F4`) × `[rbp-0x6C]` ×
        `[rbp-0x68]` (`002AA13A`–`002AA15C`).
      - **Bit set, latch not at 2:** the latch is set to **1** with no gap.
      - **Bit clear:** the latch is set to **2** (`002AA16C`).

      So 2 means "the last glyph lacked bit 31", 1 means "it had it", and 0 is the reset. The character dispatcher
      `002AC5F0` writes 0 in its control-code arms (`002AC6BE`, `002AC6D1`, `002AC7D4`, `002ACD27`), and `002B0280`
      writes 0 at `002B0357`. The same compare-2 / set-1 / set-2 triple recurs in `002AAE40`, `002AF340`, `002B0280`
      and `002B2150`, so every layout path applies the rule. **Which glyphs carry bit 31**, and so which class
      transition earns the gap, was not identified. *(Proposed row P6, §15; it needs the shipped font tables. DD batch
      13, 2026-09-30.)*
      *Answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15, §15b P6):* the Latin glyphs carry it (in `us` and `it`, codes `0x20`–`0x8E`,
      `0x93`–`0x94` and `0x98`–`0xB6`), so the gap goes where a line passes into Latin letters from anything else.
- [x] **UQ-176.** What the `00916560` table's entries mean. Its first bytes are `03` then zeros, then `E0 00`,
      `C0 01`, `A0 02`, `80 03` — **values `0xE0` apart if read as dwords**, which suggests an offset
      table read a byte at a time, **but the index is `movsx`-signed and that is not explained.**
      *Narrowed 2026-09-14 (FABLE), not answered: two tables share the address run.*
      - **The byte table.** Only two sites address `00916560`: `002A9F00` (`002AA19C`) and `002AAE40` (`002AB0C6`). Both read
        **one byte** `[00916560 + (signed byte) state[+7]]`. The drawer splits it: the high nibble plus `0xCBF` and the low
        nibble go into separate bit ranges of the 64-bit command word (`shl 8 / sar 6`, and `shl 0x13`;
        `002AA1B5`–`002AA1E4`). Of the first sixteen bytes only index 0 is non-zero (`03`).
      - **The dword run.** The "0xE0-apart" dwords start 16 bytes in, at `00916570`: `E0, 1C0, 2A0, 380, 460, 540, 620,
        700, 0, E0, …`. No RIP-relative reference addresses `00916570` or any address inside it. They read as a separate
        dword table packed after the byte table, and an index reaching 16 would read into them.
      ***ANSWERED 2026-09-18 (FABLE) — the entries are the `9` escape's translation bytes, and no shipped text ever selects one.** Two things close it. *The tag layout, read from the builder:* the `0F` token's arm is jump-table entry 15 (`002B1BAC` → `002B1134`), which loads the selector from `[r15+1]`, **steps `r15` onto it** (`002B1139`), dispatches on `selector − 0x20` through the byte table `002B1C3C`, and the arms hand that pointer to the parser (`002B1651`..`002B165B`); so `003FFAB0` sees `tag = ['9', p1, p2]` and returns 3 — `p1 & 7 ≠ 0` gives the literal `p2 & 0x7F` with bit 7 copied from `p1` bit 6 (`003FFAC3`..`003FFACA`, `003FFAED`), else the first byte of entry `p2 & 0x7F` of the 5-byte-stride table at `[02AEE870]+1`. A negative index is therefore *authorable* (any `9` tag whose `p1` has bit 6 set and a non-zero low three bits), and it would land in the decimal power-of-ten table and the two function pointers below `00916560`. *The data:* an archive census of every `.bin` / `.dat` under the nine language trees, split by magic, finds **no `0F 39` in any text-format file** — 0 in the 407 `st2e` banks, the 101 `hdat` handbooks and the 53 bank-format files (`47000000`, `0f000000`, `40000000`), against 24,700 `)` escapes in the same files as the control; the only `0F 39` bytes in the language trees sit inside `himg` images. So the `9` escape is authored nowhere, `+0xB0` bit 21 is never raised by shipped text, the three gated readers never index `00916560`, and the table's content (index 0 → `03`, indices 1–15 → `0`, then the `0xE0`-step dword run) is dead data in the shipped game. What the two command-word fields it would feed mean on screen stays with the glyph-run page, and has no shipped exerciser. Static for the layout; DATA for the census.*

      - **`state[+7]` is block `+0xA7`, and the index is gated and one-shot** *(2026-09-15, OPUS)*.
        `rbp` in `002A9F00` is the **frame pointer**, not a state pointer: `002A9F0A lea rbp,
        [r11 - 0x1b8]` with `r11 = rsp` at entry, so `rbp = rsp + 0x100`. The function copies the
        shared 208-byte block to `rsp + 0x60` (§2), which puts `rbp` at **block `+0xA0`**. So
        `[rbp+7]` is **`+0xA7`**, `[rbp-1]` is **`+0x9F`**, and `[rbp+0x10]` is **`+0xB0`** — and
        that last one is the cross-check, because §2 independently records `+0xB0` as a dword of
        this cluster's own.
      - **The table is one of THREE sources, not the only one.** `002AA180`–`002AA1A3`: if the
        preceding test is non-zero the byte is the literal **`0x0E`**; else if `+0xB0` bit 21 is
        **clear** it is **`+0x9F`**; only if that bit is **set** is it `00916560[+0xA7]`. The bit is
        then cleared, so the table path fires at most once per call.
      - **The negative direction is not merely unexplained — it is nonsense, and that is now
        evidence.** Read from the image at `00916560 - 0x40` there is a **decimal power-of-ten
        table**: `1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000` as dwords. Below
        that, at ~~`-0x50` and `-0x80`~~ `-0x48`, `-0x80` and `-0x78` in the order listed *(corrected 2026-10-02, OPUS: the qwords at `00916518`, `009164E0` and `009164E8`; the one at `-0x50` is zero)*, are **function pointers** — `002AAE40`, `002A8C50`,
        `002AA800`. A negative `+0xA7` would take a decimal constant or the low byte of a code
        address and split it into a glyph command's nibbles. **So the `movsx` reflects a field
        declared as a signed `char`, not an intent to index backwards** — which is an inference
        about the source, and is marked as one.
      - ~~**Still open:** what writes `+0xA7`, and therefore its actual range. Nothing in
        `002A9F00`'s 2,304 bytes writes it — the block arrives already populated.~~
      - **THE WRITER AND THE RANGE, 2026-09-17 (FABLE): `+0xA7` is the parameter of the `9` escape, and the table is indexed by it.** SWE2-STRUCT's `text-draw-state-accesses.tsv` carries the one write the displacement scans could not see - `003FFAB0` stores through a pointer (`003FFAE5` / `003FFAF5`) that the run builder `002B0280` forms with `lea rdx, [r14+0xA7]` and passes at `002B165B`, then raises `+0xB0` bit 21 (`002B1660`), the very gate the three table readers test. That call site is **entry 14 of the builder's second dispatch table** (`002B1BE8`, selected through the byte table at `002B1C3C` by `escape byte − 0x20`), and the only selector mapping to 14 is **`'9'`** - the same escape whose arm in the measurer `002AC5F0` the control-code page reads as *sets `+0xB0` bit 21*. So the builder stores the `9` tag's parameter and the measurer only flags it. **The value:** `003FFAB0(tag, out)` (78 B) is a three-byte tag parser with two branches - when `tag[1] & 7` is non-zero, `out` is `tag[2] & 0x7F` with bit 7 taken from `tag[1]` bit 6, an 8-bit literal; when it is zero, `out` is the FIRST BYTE of entry ~~`tag[2] & 0x1FF`~~ `tag[2] & 0x7F` *(corrected 2026-10-02, OPUS: `003FFAB0+0x1A` `and r8b, 0x7f` masks the index before `0039BA00`'s own `and eax, 0x1ff` at `0039BA00+0xA`, so only entries 0–127 are reached)* of the unnamed 5-byte-stride table at `[02AEE870] + 1` (`0039BA00`). So `+0xA7` ranges over `0`–`255` as a literal, and the `movsx` readers treat `0x80`+ as negative (the power-of-ten bytes below the table): an authored `9` tag with byte-1 bit 6 set would do that, which the shipped text must not contain - a DATA check, not made here. **What the entries mean, now:** `00916560[p]` is the per-`9`-parameter byte whose two nibbles the drawer inserts into the glyph command word (`shl 8 / sar 6` on the high nibble plus `0xCBF`, `shl 0x13` on the low), so the table is the `9` escape's translation into render state, with only parameter 0 non-zero (`03`) in its first sixteen bytes. **Still open:** what those two command-word fields are (the glyph-run page transcribes the command, it does not decode it), and therefore what a `9` tag changes on screen. *(Provenance note, 2026-09-21 (FABLE), answering `OPUS-REQ-FABLE-THREE-LIVE-ABSENCE-CLAIMS-BLOCK-THE-GN162-CARRY`: **"unnamed" above governs the 5-byte-stride data table**, which is still unnamed — it is not a claim about a function record. `002AC5F0` is in the residual set at GN158 and GN160 and **out of it at the current parent GN162**, where it carries `UI.Text.ControlCodeInterpreter` — which is what this line already calls it, "the measurer" whose escape arms the control-code page reads. The reading stands as written.)*
- [x] ~~What the `divss` / `comiss 1.0` pair gates.~~ **Answered 2026-09-14 (FABLE): a render-strip break every 1920 units.**
      `xmm15` is loaded with `1920.0` (`008C5B5C`, `002AA01D`). The pair divides a glyph edge built from the pen and
      `0209CC60` (`xmm9`, `002AA498`–`002AA4DB`) by 1920 and compares the result with the running
      boundary at `01E0CDF4`, whose image value is `1.0` (`002AA4E4`–`002AA4EF`). When the edge passes the boundary, the
      drawer runs the painter's seam sequence:
      1. flush and present (`0017F850`);
      2. begin a new run (`0017FA10`);
      3. re-select the render target with the saved pair `0209CC30` / `0209CC34` (`0017FD30`);
      4. re-apply the 4×4 transform (`0017FB00`);
      5. advance `01E0CDF4` by `xmm12` = `1.0` (`002A9FEF`, `002AA565`–`002AA583`).

      So a text run wider than the current 1920-unit strip is split into successive draws, one per strip. The same
      counter is read and advanced by `002AA800`, `002AAE40` and `002B0280`, and `002AF960` and `002B0280` (`002B034D`) also write it. Why
      strips of 1920 (the 1080p width) are needed, whether for a render-target width or a batching limit, was not traced.
      *(Runtime-only, 2026-09-30, DD batch 13: the mechanism is complete, and which limit it serves is shown by the
      painter's render-target size at run time.)*

### Addendum — reconciled against an independent parallel read

`002A9F00` was opened twice in the same tick, from a decompiler and from the image, with no contact
between the readers. **Three findings agreed** — the unrolled state snapshot, the
`movabs 0x4100400000000000` tag class, and `+0x10E4` being touched once per character — **and one
looked like a disagreement.** It is not one.

**`+0x10E4` has two roles in two functions, and each reader saw one of them.** Scanning the whole text
cluster for that displacement:

| function | what it does with `+0x10E4` |
|---|---|
| `002A9F00` | **read, `subss`, written back — decremented only.** No multiply anywhere in the body. |
| `002AC5F0` | **`mulss` at two sites** — a render-state byte is `cvtdq2ps`-converted, multiplied by it, and `comiss`-compared |

> **One field, two roles: this function spends it, the shared consumer scales by it.** The "remaining
> budget" reading and the "scales an output" reading are halves of one lifecycle, and **the
> disagreement was an artefact of each reader seeing one function.**

**The batch counter, with a corrected constant.** The parallel read reported a flush every 20 glyphs
against `0x13`; the comparison is against **`0x14`**:

```asm
002AA45B  add  rcx, 0x50                        ; the per-glyph record stride
002AA45F  inc  dword ptr [rdx + 0x10d4]
002AA465  cmp  dword ptr [rdx + 0x10d4], 0x14
002AA473  jb   skip                             ; below 20 -> keep filling
002AA478  call 0x2b4730                         ; flush
002AA484  mov  dword ptr [rdx + 0x10d4], edi    ; edi = 0
```

**Twenty records of `0x50` = 80 bytes each — a 1,600-byte batch**, flushed when the count *reaches* 20.
`002AAE40` carries the same counter against the same `0x14`, so **the batch rule is shared across the
cluster, not local to this function.**

**The two-path character loop, confirmed:**

```asm
002AA053  cmp  byte ptr [rax], 0xf
002AA056  jbe  0x2aa698          ; <= 0x0F -> the control path
...
002AA6A8  call 0x2ac5f0          ; the shared consumer
002AA6AD  test eax, eax          ; its return is consumed here
```

**Bytes `0x00`–`0x0F` go to the shared consumer and everything else emits a quad.** That is the caller's
view of the `char**` cursor and `int*` status characterised in section 12 from the callee side — **the
two descriptions were derived independently and meet here.**

And the tag lookahead is shared too: immediately after that call, `cmp r8b, 0xf` guards tests against
**`0x3E` (`>`), `0x70` (`p`) and `0x40` (`@`)** — **the same three discriminators section 13 found in
`002A8C50`.** So the markup vocabulary is not per-function; **the parser and the emitter agree on it by
using the same constants.**

**Process note, recorded because it cost work:** this function was taken by two sessions in the same
tick because one of them was not announced. The duplicate produced a genuine independent
corroboration — but it was luck, not design, and the reconciliation above is the only part worth the
second read.

## 15. Residue read statically, 2026-09-30 (SWE2-CONTRACT for OPUS)

DD batch 13 (`OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`). Every item below is pinned by
`_index/candidates/swe2contract-ddres-b13-0930/b13_checks.py` (checks N1–N7, FAILS 0) on the certified image.

- **N1. `+0xA6` is the glyph sheet's font slot.** `002B3400` stores `0039BAD0`'s return there. `0039BAD0` returns the
  slot, 1 to 7, of the seven-slot font registry `02AEE810` whose entry equals the given sheet, or 0 when none does.
  Slot 7 is `fontVariant[7]`, the alternate glyph sheet ([the loader-bound families](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md),
  `fontpack_it`). When `00254A10()` is 0 and the slot is 7, the initialiser sets `+0x44` bit 11 and stores
  `0039C4A0(1)` at `+0x60`, the alternate sheet's pointer `[02AEE808]`. The same compare sits in the run builder
  `002B32D0`. That loader page finds `fontVariant[7]` a sentinel in every shipped file, so in shipped play the slot-7
  branch stays idle.
- **N2. `+0xB8` is the glyph run's pixel-test word.** The drawers pass it to the run begin `0017FA10` (`002AA51A`),
  and the emitters `002AF960` and `002B1D20` write it into the command stream as the data of command code `0x47`, the
  record [the glyph-run page](../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md)
  calls the pixel test setup. The three `002D8xxx` draw helpers write `0x3001`, and the initialiser `002AC1E0` and the
  stack-copy builders write `0x30000`. What each value tests is that page's to name.
- **N3. Ordinary text is proportional; digits are monospaced.** The general glyph loop `002A9F00` calls `002AC2F0`
  for every character (`002AA0CD`, inside the loop `002AA050`–`002AA74C`), before it reads the advances `0209CC6C`
  and `0209CC68`. `002AC2F0` rebuilds the spacing block `0209CC60`–`0209CC6F` from that glyph's own advance field
  (`0017F9C0` on its glyph entry's `+0x1C`, or else bits 32–36 of its 8-byte record), plus the spacing float `+0x4C`,
  scaled by `+0x34`. This is a separate field from the quad width `w` of §7's AC-9 item. A one-shot `+0xA9` can override the advance. The number formatter `002AE610` calls it once, for `'0'`
  (`002AE7D7`), so in player terms a line of text is spaced glyph by glyph and a number's digits are spaced evenly.
- **N4. The `+0xC0` child.** `002D14E0` builds a `0x150`-byte list widget with procedure `002D2DB0`, and both
  `002A5590` and the shared dialog `0057C480` store its return at their own `+0xC0`.
- **N5. `002A1B00`'s onward call stamps a fresh state.** `002D89E0` points `rcx` at its own stack block
  (`002D8A25`) and does not reload it before `002B3400` (`002D8A7B`).
- **N6. The lag bound starts the reveal.** `002B32D0`, `002B3C30` and `002B3D50` each read `+0x9E`, negate it and store
  it in the target `+0x90`. So a text reveal starts behind the head by the lag bound.
- **N7. Register states.** UQ-164 is CLOSED. UQ-166, UQ-168, UQ-173 (2026-09-26), UQ-381, UQ-383, AC-9 and AC-10 are
  ANSWERED. The stale sentences above predate them.

**Proposed register rows, id-less, for SWE2-DATA (SWE2-CONTRACT for OPUS):**

| # | question |
|---|---|
| P5 | What the five outputs of `003FFC60` mean in the `.` and `-` escapes: byte 1's 7-bit field, byte 2's clamped 4-bit field and its three flags, as the number formatter `002AE610` uses them after `002AE760` |
| P6 | Which glyphs of the shipped fonts set bit 31 of their 8-byte glyph record (`002AA117`–`002AA16C`), which decides where the class-change gap (2.3, scaled) is inserted |
| P7 | What the pen components `+8` and `+0xC` carry in `002AC5F0`'s `0x0E` and `*` arms, which copy them into locals at `002AC8A4` / `002AC8BD` and `002AD690` / `002AD69B`. UQ-165 found them unread on `002AE610`'s path |

*Answered 2026-09-30 in §15b (SWE2-CONTRACT for OPUS, DD batch 15): P5–P7 need no register row.*

**Runtime-only (SWE2-CONTRACT for OPUS):** why the sub-step opt-in governs the windows' confirm (the coupling is static
and its purpose needs watching); which limit the 1920-unit render strip serves.

**Boundaries (SWE2-CONTRACT for OPUS):** the kinds' subjects beyond the table in §7 belong to
[the text-element dispatch table](../../99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md);
the glyph descriptor's bit layout, the two render commands and the `9` escape's command-word fields to the glyph-run
pages.

## 15b. Rows P5–P7 answered statically, 2026-09-30 (SWE2-CONTRACT for OPUS)

DD batch 15 (`OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`). Every item below is pinned by
`_index/candidates/swe2contract-ddres-b15-0930/b15_checks.py` (checks D, E and H, FAILS 0) on the certified image and the shipped font packs. None of the three needs a
register row.

- **P5. What the `.` and `-` payload means to the number formatter.** `002AE610` asks `003FFC60` for four of the five
  outputs (`002AE72C`–`002AE760`).
  - **Byte 1's 7-bit field selects the argument.** The `.` escape uses it as the index of a 16-byte entry in the
    caller's argument array (`002AD930`) and hands the formatter a copy whose byte 1 is `0xFF` (`002ADB07`). The
    formatter draws only when the field is `0x7F` (`002AE823`), so `0x7F` means "the number already in the state"
    (`+0x54`); any other value draws nothing (`002AE841`–`002AE851`).
  - **Byte 2's 4-bit field, clamped to 8, is the field width.** The `-` escape writes it to the state's `+0xA1`
    (`002AD8B0`) and the `.` escape to its copy's (`002ADBAC`). The formatter does not ask for it itself; it uses
    `max(+0xA1, +0xA2)` (`002AE7AC`). A width keeps only the low digits (it subtracts 10^width, table `00916520`, while
    the value reaches it) and pads to that width. Width 0 means the natural length, at least `+0x98` + 1.
  - **Bit 5 is the pad character:** `'0'` when set and a space when clear (`003EFD00`, `003EFD59`–`003EFD82`).
  - **Bit 4 selects the font's second character map**, sheet `+0x18` instead of `+0x14` (`002AE856`–`002AE861`), and
    is forced off on the alternate sheet (`+0x44` bit 11). In the shipped `us` sheet the first map sends `'0'`–`'9'`
    to glyph codes `0x85`–`0x8E` and the second to the two-byte codes `0x3010`–`0x3910`, a separate digit set. The bit
    also switches the missing-glyph fallback from code 7 to code 1 and drops the leading class step.
  - **Bit 6 is never read.** The formatter only zeroes its slot and passes the slot's address (`002AE680`,
    `002AE72C`).

  In player terms: the two codes say which number to print, how many digits to show, whether to pad with zeros, and
  which digit style to use.
- **P6. Bit 31 marks the Latin glyphs.** A single-byte code `c` is glyph `c − 0x20` (`002AC37C`). In the shipped `us`
  and `it` sheets bit 31 is set on codes `0x20`–`0x8E` (A–Z, a–z, the accented letters, ß and the digits
  `0x85`–`0x8E`), `0x93`–`0x94` and `0x98`–`0xB6` (the ASCII punctuation block). It is clear on `0x8F`–`0x92` and
  `0x95`–`0x97` (a few dashes, guillemets and quote marks on the render), on `0xB7`–`0xFF` (the symbol block of
  arrows, brackets and signs, and the second letter set that bit 4's map reaches) and on every two-byte glyph. Every
  printable ASCII character but the space maps to a set glyph. In the `kr`, `cn`, `ch` and `in` sheets bit 31 is the
  minority, one Latin block among the two-byte glyphs. So the step of 2.3 × `+0x34` × `+0x38` goes before a Latin glyph
  that follows a non-Latin one. In player terms: a small gap opens where a line passes from symbols or two-byte
  characters into Latin letters. The code ranges are pinned; the names of the groups come from the decoded glyph render
  (`glyphs_us_20_FF.png` in the record: `x` is bits 0–9 of the record, `y` bits 10–19).
- **P7. The pen's `+8` and `+0xC` carry nothing that is read.** The `0x0E` arm copies them into the local pen at
  `rbp+0x60` (`002AC8A4`–`002AC8E4`) and the `*` arm into the one at `rbp+0x70` (`002AD690`–`002AD6B1`). Each local
  goes only to `002A9F00` (`002ACABD`, `002AD728`), which touches its pen at `+0` and `+4` alone. `002AC5F0` never
  reads those local slots back, its other pen callees `002AE450` and `002AEB20` read only `+0` and `+4`, and UQ-165
  closed `002AE610`'s path. So `+8` and `+0xC` are padding of the four-float pen, copied along and never used. In
  player terms they change nothing on screen.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `002AFDC0` | 1208 | text-record translator on `[rsi+0x20]`/`[r8+0x12]`: `002B4730` x2, `0017FC90`, `002DD860` x2/`002DD8B0`, `00181xxx` accessors (`00181560`/`001819A0`/`00181870`/`00181460`/`001816B0`/`00181910`) |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE.** Cited formatting functions call small core helpers (27 and 7 bytes twice each, and 8, 40 and 93 bytes).
- **Movement — MECHANICAL (20 edges, one fan-in), 2026-09-15 (FABLE).** All 20 are Movement bodies calling `00203170`, newly cited above as one of the calls `002D8550` makes before it reaches `002AF960`. `00203170` is a **44-byte inline SIMD helper with 84 callers image-wide**; `0022EF20`, `00230790`, `0026EB30` and `00334220` are four of them. The crossing is **one shared primitive with 84 callers**, not 20 relationships, and the count says more than any single body would. Tier 2 — `edges.tsv`, the ledger's size and owner columns; no Movement body read for this note.
- **Gameplay — MECHANICAL (1 edge), 2026-09-15 (FABLE).** `00339630` calls the same `00203170`. Same primitive, same reading: an accessor, not a relationship.
- **Party — MECHANICAL (2 edges), 2026-09-15 (FABLE).** `00314020`, newly cited above as the sole caller of `002E09A0`, calls `PartyControl_UpdateControlledActorLocomotion` (`00358C60`, 71 B) and `PartyFocus_UpdatePrimarySecondaryActorProcessing` (`00358EE0`, 175 B). **`00314020` is the world tick's mode switch and has 52 callees**, of which these two are Party's; it is cited here for one edge only — that it calls `002E09A0` — and nothing on this page depends on what else it drives. The crossing is **the tick reaching the party layer on its own account**, not a relationship between party control and text rendering. Tier 2 — `edges.tsv` and the ledger's name, size and owner columns; no Party body read for this note.
- **ActorEntity - CLIENT and SERVICE (13 edges).** `00203170`, `00263990` are called by bodies filed to ActorEntity: `0025C230`, `0025C830`, `00268D10`, `00272CB0` (+2 more); `002E09A0`, World_UpdateSimulationTick (`00314020`), BattleAction_FindApproachGeometryAroundTarget (`00339630`) reach bodies filed to ActorEntity: `0025BFB0`, ActorManager_RunFieldRuntimePass (`0025D9E0`), `00263660`, `00263FF0` (+3 more) - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT and SERVICE (5 edges).** `001EDDA0` is called by bodies filed to Audio: `003B99D0`; `001E8070`, `00241D40`, World_UpdateSimulationTick (`00314020`) reach bodies filed to Audio: `00225690`, `00249CA0`, `002DEBA0`, `00362850` - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (20 edges).** `0017E210`, `0024A680`, `00267310`, `002A38C0` (+1 more) are called by bodies filed to Input: `0022A4F0`, `00291D90`, InputGameplay_GetActorStateAwareRemappedMask04 (`002A28E0`), `002E09A0`; InputGameplay_GetActorStateAwareRemappedMask04 (`002A28E0`), InputGameplay_GetActorStateAwareRemappedMask08 (`002A2940`), InputGameplay_GetActorStateAwareRemappedMask0C (`002A29A0`), InputGameplay_GetActorStateAwareRemappedMask10 (`002A2A00`) (+6 more) reach bodies filed to Input: `001E0A10`, `001E0C10`, `001E0C30`, `001E0E30` (+10 more) - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (4 edges).** `002A7A40`, `00579AF0` reach bodies filed to Resource: `00249580`, `0024A680`, `003933F0`, `00393460` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (67 edges).** `00203170`, `00267310`, `002E16B0`, `002E20D0` (+2 more) are called by bodies filed to Script_VM_Native_Bridge: `0033F330`, `0033F950`, `00340260`, `00340FA0` (+62 more); `00348540` reaches bodies filed to Script_VM_Native_Bridge: VMValueStack_PopInt32CoerceFloat32 (`00267E10`) - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - SERVICE (3 edges).** `00263990`, `002639E0`, `002E16B0` reach bodies filed to Story_Event_Quest_Hunt: PersistentFlag_QueryBank2048 (`0032A930`), PersistentFlag_SetBank2048 (`0032ABF0`) - shared machinery across the layer boundary, no shared ownership.

## The `002AC5F0` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

The control-code interpreter §12 opened (`002AC5F0`, 7,489 B) keeps four helpers
exclusively. The dispatch is `dec eax; cmp eax, 0xE; ja default` over the byte at
the format cursor — a 15-way jump table whose entries sit at `002AE334`, offsets
relative to the image base (`lea rsi, [rip-0x18c6a2]` → `00120000`). The
interpreter callsite context: `[rdi]` is the string cursor, `r12` the float4
pen/output accumulator, `r14` the text context, `[r9]` the out count zeroed at
entry.

| member | role | interior |
| --- | --- | --- |
| `002AB820` (49 B) | emits the pending run — calls `0017FD30` against context `[0209D480]`, then publishes the two arguments into `0209CC30`/`0209CC34` (the queued glyph-run origin cells the page's `+0x10E8` neighbour describes) | [`002AB835`](../../_index/ADDRESS-INDEX.md) |
| `002B1ED0` (75 B) | pen-position refresh — `[ctx + 0x44] & 0x800` selects between the `0017F980`/`0017F960` and `0017F8A0`/`0017F880` getter pairs; either way it stores the pair to `0209CC70`/`0209CC74` | [`002B1EDD`](../../_index/ADDRESS-INDEX.md) |
| `002B2C50` (73 B) | token-width probe — gated on `[ctx + 0xB0] & 0x800000`; scans the string for a `0x05` byte before any `0x00`/`0x02`, and only then returns `2 × dword[01E0CDC0] × [ctx+0x34] × [ctx+0x38]`; otherwise `0.0` | [`002B2C7F`](../../_index/ADDRESS-INDEX.md) |
| `003FFD70` (41 B) | escape-pair decoder — `[rcx+1] & 0x7F` → `word[r9]`, `[rcx+2] & 0x7F` → `word[r8]`, `[rdx] = rcx + 3`, returns `word[r8] + 3` — the two-operand 7-bit escape in the format stream | — |

Shared callees deliberately outside the census: `0017FD30`, `0017F980`,
`0017F960`, `0017F8A0`, `0017F880`, `0017FAE0`, `0017F850`, `0017FA10`,
`0017FB00`, `002B2150`, `002B1F20`, `002B2DF0`, `003FFDF0`, `003A1DB0` — the
emit/hub helpers §5's call chain already names. The 15 jump-table arms are the
control-code handlers themselves and belong to the root, not to this census.

## The `002A8C50` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`002A8C50` (3,363 B) is the element interpreter this page already maps: the
`[01F44830]` handler slot (`002A8C6F`), `xmm6 = 1.0f` (`002A8D54`), the
`003FFAB0` leaf-getter battery (×5: `002A93CA`, `002A94DD`, `002A967C`,
`002A96F8`, plus `002A91FA`), `002B3E90`/`002B43C0` property pairs, the
`002AC5F0` numeric formatter (`002A9726`), the `002B2D20`/`002B2CA0`/
`002B2CE0` emitters (`002A9842`–`002A9891`), `001EDDA0` (`002A990D`), then
the per-tick `002ABF70` (`002A9945`) and `00808C40` cleanup (`002A9951`).

| member | role | interior |
| --- | --- | --- |
| `002ABB20` (918 B) | object-list table walk — iterates `[0209CC40]` elements (`002ABB3B`), loads the `00916548` rodata token pair `0x230F`/`0x350F` (`002ABB4F`), per-element `002AF340` + `002B20B0` (`002ABC90`/`002ABCEC`) with a `002ABE78`/`002ABE80` loop-back | [`002ABB4F`](../../_index/ADDRESS-INDEX.md) |
| `002ABF70` (577 B) | the per-tick state machine — image-base switch (`lea r8, [rip-0x18BF92]` → `00120000`, `jmp rdx` at `002ABF9D`) over the `+0xB0` mode byte's seven labels, `00248F20` (`002AC085`), calls `002ABB20` (`002AC0A7`) | [`002ABF8B`](../../_index/ADDRESS-INDEX.md) |
| `002B35A0` (458 B) | bounded character loop — leaf body, no calls; loop-back `002B3713` (`002B3701`) | [`002B3701`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002B2150`, `002B3E90`, `003FFDF0`,
`003FFC60`, `002B43C0`, `003FFAB0`, `00248F20`, `003FFEE0`, `002AC5F0`,
`002B2D20`, `002B2CA0`, `002B2CE0`, `001EDDA0`, `00808C40`, `002AF340`,
`002B20B0`. `002ABB20` is reached from `002ABF70`, not from the root.

## The `0017F8C0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`0017F8C0` (~230 B) is a battery of context-adapting thunks: each arm
fetches the shared context through `001B5FA0` (or `001B5FB0` at
`0017F9A4`), passes the incoming `ecx`/`ebx` through, and tails into a
`001E9xxx` formatter — `001E9860` (`0017F8D7`), `001E9780`
(`0017F8F2`), `001E9BD0` (`0017F903`), `001E9840` (`0017F939`),
`005C52D0` (`0017F950`), `001E9580` (`0017F970`), `001E9610`
(`0017F990`).

| member | role | interior |
| --- | --- | --- |
| `001E9860` (51 B) | codepoint → glyph index — `r9=[rcx]`, `r8=[rcx+8]`, bound `eax=[r8+8]` vs `edx` (`001E987C`), `edx = dword[[r8] + edx*4]` (`001E9885`), tail `001FDEC0` (`001E988B`) | [`001E9885`](../../_index/ADDRESS-INDEX.md) |
| `001FDEC0` (69 B) | keyed list search — walks `r8=[rcx+0x50]` via `[r8+8]` links, matching `dword[r8+0x20]` against `edx` (`001FDED0`/`001FDEE7`), returns the node | [`001FDED0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001B5FA0`, `001B5FB0`, `001E9780`,
`001E9840`, `001E9580`, `001E9610`, `001E9BD0`, `005C52D0`. The
`001E9860 → 001FDEC0` edge is member→member — the glyph-index lookup
ends in the keyed list search.

## SWE2-EC7-69 update (2026-09-19) - `001B51C0` glyph-map lookup measured

`001B51C0` (69 B) is the ordered-tree lookup the formatting bodies share:
walk the root at `[rcx+0x40]` descending `+0`/`+8` children by
`edx < node[+0x20]`, track the last node whose key was `>= edx`, and return
`node[+0x28]` - the mapped record pointer - or NULL when the search fell off
the `rcx+0x30` sentinel. Call-free; a standard `lower_bound` on the
codepoint-keyed map.
Interior anchor `001B51D0` (the `cmp dword[r8+0x20], edx` key compare).

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-numeric-formatting-and-character-mappin-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `002476E0` | 58 B | `002A70B0` + 0x103 | when `rcx` is non-null and dword `rcx+0x40` has bit 7 set and bit 8 clear, adds bytes `rdx+0`, `rdx+2`, `rdx+4` and `rdx+6` to bytes `+0xA4`, `+0xA5`, `+0xA6` and `+0xA7`; otherwise returns without a write | Interior anchor `002476EA`; Interior anchor `002476EC`; Interior anchor `002476F5`; Interior anchor `00247713` |
| `0028F750` | 88 B | `002A70B0` + 0x129 | with `o` = qword `+0x10F80` of qword `0209BE80`, returns 0 when `o` is null, when byte `o+0x1D39` has bit 0 clear, or when `0028F750` + 0x33(dword `o+0x1D40`) differs from `rcx`; otherwise re-reads qword `+0x10F80` of qword `0209BE80` after the call and returns the zero-extended byte `+0x1D38` of that object | Interior anchor `0028F767`; Interior anchor `0028F774`; Interior anchor `0028F783`; Interior anchor `0028F788`; Interior anchor `0028F79B` |
| `002A4030` | 126 B | `002A70B0` + 0x4A4 | returns without a write when `edx` is 0; otherwise, for `a` = qword `+0x18` of qword `+8` of qword `rcx+0x60`, adds `dx` to word `+0x10` of qword `[qword a+0x60]` and to word `a+0x9C`, and for `b` = qword `+0x18` of qword `[qword rcx+0x60]`, adds `dx` to word `+0x10` of qword `[qword b+0x60]`, to word `+0xC` of qword `+8` of qword `b+0x60`, and to word `b+0x9C`; the null tests on `rcx`, `a` and `b` substitute 0 rather than return, so on those paths the reads and adds fall on absolute low addresses | Interior anchor `002A4032`; Interior anchor `002A405E`; Interior anchor `002A4062`; Interior anchor `002A40A1`; Interior anchor `002A40A6` |
| `002A5520` | 109 B | `002A70B0` + 0x40D | takes `v` = `002A5520` + 0x12(`rcx`), replaced by 0x1C0 (`01E0C1DC`) when negative, and calls `002A5520` + 0x25 with bit 11 of dword `rcx+0x114`; returns the truncated integer of float(`v` minus 5 times the truncated float from `002A5520` + 0x33) minus 38.0 (`00902708`) times the float from `002A5520` + 0x48 | Interior anchor `002A5532`; Interior anchor `002A554C`; Interior anchor `002A555F`; Interior anchor `002A5572`; Interior anchor `002A557E` |
| `004052A0` | 14 B | `003EC810` + 0xD | tail-jumps to `004052A0` + 0x9 with qword `02B62D88` in `rcx` and 0 in `edx` | Interior anchor `004052A7`; Interior anchor `004052A9` |
| `004052B0` | 17 B | `003EC830` + 0xD | tail-jumps to `004052B0` + 0xC with qword `02B62D88` in `rcx` and 1 in `edx` | Interior anchor `004052B7`; Interior anchor `004052BC` |
| `00574770` | 390 B | `005742D0` + 0x10D | takes `r` = `00574770` + 0x1C(`rcx`, a stack block `s`) and, with `d` = qword `rcx+0xD0`, `x` = word `d+0x48` (word `s+0` when that is 0x8000), `y` = word `d+0x4A` (word `s+2` when 0x8000), word `+0x114` = word `d+0x4C` (word `s+4` when 0xFFFF) and `h` = word `r+0xA` times byte `d+0x4E` (byte `s+6` when 0xFF); when qword `+0xE0` is non-null stores `x`, `y`, word `+0x114` plus byte `s+7`, and `h` to its words `+0x98`, `+0x9A`, `+0x9C`, `+0x9E`, and that sum also goes to word `+0x9C` of qword `+0xC0` of `+0xE0` when non-null; when byte `+0x8060` is 5, with `dx` = word `d+0x48` minus word `s+0` and `dy` = word `d+0x4A` minus word `s+2` (each 0 when the `d` word is 0x8000), sets words `+0xC` and `+0xE` of the objects at qwords `+8` and `+0x10` of qword `+0x60` to words `+4` plus `dx` and `+6` plus `dy` of each object's first qword, and word `+0x10` of the `+0x10` object to that qword's word `+8` minus `dx` | Interior anchor `0057478C`; Interior anchor `005747E5`; Interior anchor `00574810`; Interior anchor `00574830`; Interior anchor `005748DD` |
| `005766B0` | 44 B | `00573BE0` + 0x110 | with `o` = qword `+0x110` of qword `02CA9738`, returns qword `o+0xF8` when qword `02CA9738` and `o` are non-null and byte `o+0xC9` is 1, and 0 otherwise | Interior anchor `005766B7`; Interior anchor `005766BC`; Interior anchor `005766CB`; Interior anchor `005766D4` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-numeric-formatting-and-character-mappin-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `00406DD0` | 167 B | `004052A0` + 0x9 | returns without a write when `rcx` is null or when the whole of `edx` equals bit 5 of dword `rcx+0xC8`; otherwise replaces bit 5 of that dword with bit 0 of `edx` and walks the two qwords at `+0xC8` and `+0xD0` of qword `+0xC0` of qword `02B62D88`, calling `00406DD0` + 0x7B with the entry in `rcx` and the incoming `edx` for each entry that is non-null and has bit 4 (0x10) of byte `+0x130` set, skipping it when qword `02B62D88`, its `+0xC0` qword or the entry is null or that bit is clear | Interior anchor `00406DEE`; Interior anchor `00406E0D`; Interior anchor `00406E40`; Interior anchor `00406E4B`; Interior anchor `00406E5E` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-numeric-formatting-and-character-mapping-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003CA530` | 810 B | dispatches on dword `[rdx]`: 1 calls `003CA530`+0x2A2(`rcx+0x50`, qword `+0x28` of qword `0209AC30`, 3, `rcx`), copies the result's words `+4/+6/+8/+0xa` to `rcx+0x98/+0x9a/+0x9c/+0x9e` when `rcx` is non-null, calls `003CA530`+0x2E1(0, local `L`) and, with `Q` = qword `+8` of `[rcx+0x60]`, stores `00272CB0(dword L+8)` at qword `Q+0x18` and `003CA530`+0x306(0) at dword `Q+0x20`; 2 calls `003CA530`+0x63(0, `L`), takes `f` = float `L+0xc`, `i` = (int)`f`, `t` = (int)((`f`-`i`)*10.0); `c` = `003CA530`+0xB1(0) when `f` >= 1.0, else the `003CA530`+0x1C5 blend of the bytes of `003CA530`+0x137(6) and `003CA530`+0x144(0) by (int)(`f`*256.0), bytes 0-2 each times `k` then `>> 7`, byte 3 kept, where `k` = 0x80, or for `f` <= 0 ~~(int)(`003CA530`+0x105((dword `0208F570` - dword `rcx+0xc0`)*pi/30)*64+128)~~ (int)(`003CA530`+0x105((dword `0208F570` - dword `rcx+0xc0`, converted as an unsigned 32-bit value)*pi/30)*64+128) with `0208F570` stored at `+0xc0` when it was 0; then, with `R` = qword `+0x18` of qword `+0x18` of `[rcx+0x60]`, calls `003CA530`+0x23A(`[[R+0x60]]`, 3, 5, `c`, `i`) and `003CA530`+0x268(qword `+0x18` of `[R+0x60]`, 1, 5, `c`, `t`), passing 0 for `R` null; both return 0; other values return `003CA530`+0x32(`rcx`) *(narrowed 2026-10-03, FABLE, on SWE2-AUDIT-SPEC's review: `mov eax, r14d` / `sub eax, ebx` zero-extends `rax`, and `cvtsi2ss xmm0, rax` at `003CA620` converts the 32-bit difference as unsigned)* | Interior anchor `003CA554`; Interior anchor `003CA5DD`; Interior anchor `003CA6F5`; Interior anchor `003CA76A`; Interior anchor `003CA82B` |
| `00404E10` | 264 B | with `g` = qword `02B62D88`, returns without work when `g` or qword `g+0xc0` is null or bit 0 of byte `+0xc2` of the latter is set; otherwise calls `00406DD0(g, 0)`, re-reads `g`, sets that bit 0, and scans the first byte `g+0xe3` entries of the 0x18-byte array at qword `g+0xe8`: when one has dword `+8` greater than 0 (signed) it tail-jumps to `00404E10`+0x99 with `rcx` = qword `g+0xc0`; otherwise, for each of the two qwords at `+0xc8` and `+0xd0` of qword `g+0xc0` (skipping null ones, and re-reading `g` from `02B62D88` after each call), it sets bit `0x8` of that object's dword `+0x130` when its bit `0x10` is set, else calls `00404E10`+0xDD with it; it sets no return value on these paths | Interior anchor `00404E3B`; Interior anchor `00404E48`; Interior anchor `00404E62`; Interior anchor `00404EA9`; Interior anchor `00404EED` |
