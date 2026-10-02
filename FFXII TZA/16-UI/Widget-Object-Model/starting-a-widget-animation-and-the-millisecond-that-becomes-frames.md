---
system: Starting a widget animation — and the millisecond that becomes frames
category: 16-UI
status: AUDITED — the state nibble's alphabet 0..4 (UQ-183) and the +0x48 record as two transition halves (UQ-184) answered 2026-09-17
owner_layer: none — the operation carries no ledger owner
evidence_tier: 1
level: L1
readiness: SEMANTICALLY IDENTIFIED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 67 addresses cited - 7 data, 23 entry, 36 interior, 1 literal, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-widget-anim-start-pass-1 - all 330 bytes re-read and every section 3 and section 7 figure exact including the 148 call sites; CORRECTED: the 0x200 'mark started' bit goes into +0x40, not +0x7C; NEW: 0208F570 has 149 references image-wide of which exactly 6 are writes - one re-base on MESSAGE 18 - corrected 2026-09-13, this note said 14 - and five adds of a rate-compensated step of 1 or 2, so the frame reading rests on the writers; the 'receiving-side argument against teardown-ish' built on that arm IS WITHDRAWN, because a message-18 act constrains nothing about message 14; and 01E0C0E0 has exactly one reference in the image
  crossref_clean: false
  reopened_count: 0
---

# Starting a widget animation — and the millisecond that becomes frames

## 1. What the player sees

A menu panel slides in, an icon pulses, a bar fills. **Whoever authored that motion wrote its length
in milliseconds**, and the engine converts it — once, at the moment the motion starts — into a
count of frames **at sixty frames a second**, and then counts down in frames.

So the duration a designer typed is a wall-clock duration, and what the game actually runs is a
frame count derived from it by a fixed 60.

## 2. Where it sits

`00246AD0` (321 B) is called from **148 sites — 142 `E8` and 6 `E9`**, controls positive for both
instruments. **No document in this database had cited it.** The index found it by asking for the
highest-connectivity callee with a real body that nothing cites.

**The object arrives in `rdx`, not `rcx`**, and a null one returns immediately — the function's first
instruction is `test rdx, rdx`.

## 3. What it does, in order

```c
void Widget_StartAnimation(void *unused_rcx, Widget *w)      /* 00246AD0 */
{
    if (!w) return;
    w->flags_40 &= ~0x40;

    if (w->_0x10 == 0)            { w->flags_40 |= 2; FUN_00248220(); }
    else if (w->flags_40 & 0x20)  { w->flags_40 |= 2; FUN_002473F0(w, 1); }
    else                          { w->flags_40 |= 2; }

    w->rate_B8 = 1.0f;                                  /* 01CEBBA8 */
    if (FUN_00229DF0() && FUN_00229EA0() == 2)
        w->rate_B8 = 1.0f / FUN_00229E70();             /* a mode-2 adaptation */

    int state = (int32_t)(w->word_7C << 28) >> 28;      /* the SIGNED low nibble of +0x7C */
    ...
}
```

**`+0x7C`'s low four bits are a signed state**, extracted with `shl 28 / sar 28`. Negative states and
states other than `0`, `1` and `4` fall straight through to the dispatch at the end.

### The rate is 1.0 unless a mode says 2

`w->rate_B8` is set to **`1.0f`** unconditionally, then **divided into 1.0 by whatever `00229E70`
returns** — but only when `00229DF0()` is non-zero **and** `00229EA0()` returns exactly **2**. All
three callees are unread; what is proven is the shape: **a rate of 1.0 that one specific mode
replaces with a reciprocal.**

### State 0 or 1 — start: milliseconds become frames

```asm
00246B95  or   dword [rbx+0x40], 0x200          ; mark started - the FLAGS word, not +0x7C (§9)
00246B9C  lea  rcx, [00915198]                  ; the default source, if flags & 0x8000
00246BAC  mov  rcx, [rbx+0x48]                  ; otherwise the widget's own
00246BB0  mov  [rbx+0x68], rcx                  ; remember it
00246BB4  mov  eax, [0208F570]  ; mov [rbx+0x74], eax     ; START STAMP
00246BBD  mov  dword [rbx+0x78], 0
00246BC4  movzx eax, word [rcx+2]               ; the authored duration
00246BC8  bt   edx, 0xA / jae                   ; bit 10 of +0x7C overrides it
00246BD0  btr  eax, 0xA ; mov [rbx+0x7C], eax
00246BD7  shr  eax, 0xC ; and eax, 0x3FF        ; ...with bits 12..21, 10 bits
00246BDF  imul ecx, eax, 0x3C                   ; x 60
00246BE2  mov  eax, 0x10624DD3 ; mul ecx ; shr edx, 6    ; / 1000
00246BEC  mov  [rbx+0x70], edx                  ; the duration IN FRAMES
```

> **`0x10624DD3` with a 32×32→64 multiply and `shr edx, 6` is the compiler's unsigned divide by
> 1000.** So the stored duration is
>
> ```
> frames = (milliseconds * 60) / 1000
> ```
>
> **A millisecond duration, converted at a hard-coded sixty frames per second.** The `60` is an
> immediate in the instruction stream; there is no frame-rate variable anywhere in this function.

**Two sources for the duration.** Normally a `u16` at `+2` of the record at `w->_0x48`; but if
**bit 10 of `+0x7C`** is set, the function clears that bit, writes `+0x7C` back, and takes a
**10-bit value from bits 12–21 of `+0x7C` itself** instead — an inline override that consumes itself.

### State 4 — reflect

```asm
00246B72  test dword [rbx+0x40], 0x8000 / je
00246B7B  mov  dword [rbx+0x70], 0
00246B82  mov  eax, [0208F570] ; add eax, eax
00246B8A  sub  eax, [rbx+0x70] ; sub eax, [rbx+0x74]
00246B90  mov  [rbx+0x74], eax
```

`start' = 2 * now - duration - start` — **a reflection of the start stamp about the current frame**,
which is how a motion is made to run backwards from where it currently is. **The duration is zeroed
first when `flags & 0x8000`.**

### Then, always

```asm
00246BEF  and  dword [rbx+0x7C], 0xFFFFFFD2     ; clear bits 0,2,3,5
00246BF3  or   dword [rbx+0x7C], 0x12           ; set bits 1 and 4
00246BF7  mov  rax, [rbx] ; test rax,rax ; je
00246BFF  lea  rdx, [01E0C0E0]                  ; -> dword 0x0000000E
00246C09  call rax                              ; obj->fn(obj, msg)
```

**The state nibble becomes `2`** and bit 4 is set. Then the object's **first qword** is called with a
message whose first dword is **`0x0E` = 14**.

## 4. Two things this settles elsewhere

### `0208F570` is a frame counter — corroborated from a second, independent function

[The blinking icon](../../99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md) uses
`0208F570` in `sinf(DAT_0208F570 * pi / 30)` and is careful to say: *"that it counts frames is the
reading, not a measurement."*

> **This function uses it as a start timestamp** — stored into `+0x74` at the moment a motion
> begins, and reflected about in the state-4 arm — **immediately beside a duration the same function
> computes in frames.** A value stamped as "now" next to a frame count, and reflected as
> `2*now - span - start`, is a frame counter being used as one. **Two unrelated functions, one
> reading**; it is corroboration, not proof, and the other document's caution stands.

### Message 14 is sent by a START, which is evidence against "teardown-ish"

[The widget message protocol](the-widget-message-protocol.md) records id **14** with **48 handlers,
22.7 %**, described as *"teardown-ish"*, and `DL-1` lists 14 among the **23 of 32 ids whose meaning
is unrecovered**.

> **Here id 14 is the last thing a start does.** It is dispatched after the rate is reset, the
> duration converted and the state set to `2` — the opposite end of a lifetime from teardown.
> **That does not name id 14**, and one sender is not a census. It is a constraint on `DL-1`, and it
> points the other way.

## 5. Modding notes

- **Authored durations are milliseconds and the conversion is fixed at 60.** Changing the game's
  frame rate does not change how many frames a widget animation runs for — the `60` is an immediate.
  **And that is consistent rather than a bug**: the counter the duration is spent against advances
  by **1 or 2 per UI tick**, doubling its step when the tick rate halves, so it stays in 60 Hz
  units (§9).
- **The duration field is 16 bits from the record, or 10 bits from `+0x7C` when bit 10 is set** —
  and taking the second path **clears the bit**, so the override fires once.
- **State 4 reflects rather than restarts.** Calling it twice does not double anything; it mirrors
  about the current frame each time.
- **The object is passed in `rdx`.** A hook written for the usual `rcx` convention will read the
  wrong register.

## 6. What is not known

- [x] **What `00229DF0`, `00229EA0` and `00229E70` are**, and what "mode 2" means for the rate.
      Unread. `EK-1`.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (EK-1): while the game-speed feature is on
      and the frame dispatcher runs the field frame, the rate becomes 1 ÷ the number of simulation steps this frame.*
      - **`00229DF0`** returns the byte `02064AD2`. The field frame `0022A770` stores `00358550()` there each frame
        (`0022AD02`–`0022AD07`; `00358550` is `byte [022C7F9A] == 0x1F`). The keymap page names it the game-speed
        feature enable: when it is 0 the speed scalar `02064AC4` is forced to `1.0`, otherwise it takes 1 / 2 / 4 from
        `00908BA8` by speed mode (`0022AAA6`–`0022AAC7`).
      - **`00229EA0`** returns the signed frame-dispatcher mode byte `02064AD3`. **Mode 2** is the dispatcher's field frame
        `0022A770` ([the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §5).
        Modes 3 and 5 are the "ATEL CONTROL" frames.
      - **`00229E70`** returns the float `01E02820` (and rewrites it to `1.0` if it does not compare above 0: zero, −0 and negatives reset, while a NaN is kept, because the unordered `comiss` takes the keep branch; qualified 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's rate-normalizer-domain). *(qualified 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's return-domain qualifiers: the NaN is kept only when the `comiss` completes. With the invalid exception masked, the unordered result sets CF and takes the `jb`. Unmasked, a QNaN or SNaN operand raises #XM, the flags are not written, and what follows is the handler's. The game's MXCSR at this site is not established)*
        - The field frame keeps a step accumulator at `02064AC0`. After each frame it adds `02064AC8` (1.0, written
          `0022A1C8`) × the speed scalar (`0022AE18`–`0022AE34`).
        - It runs one simulation step, subtracting 1 (`0022AC87`, floored at 0), while the accumulator is ≥ 1
          (`0022AD66`).
        - `01E02820` is the accumulator's value **before** the step loop (`0022AAF0`–`0022AAF8`): the number of steps
          this frame. That is 1 at normal speed and about 2 or 4 under the speed-up.
      - **So "mode 2" is not a widget mode.** Animations started during field play under 2× or 4× get rate 0.5 or
        0.25 instead of 1.0. That keeps them at wall-clock speed if the widget tick runs once per simulation step. That
        condition is the evident purpose, and was not traced through the widget tick.
- [x] ~~**UQ-183.** **What states 2, 3 and 5–7 do** — the nibble is signed and four-bit; only `0`, `1` and `4`~~
      have arms.
      ***ANSWERED 2026-09-17 (FABLE): the nibble's alphabet is 0..4, five transition states, and 5..7 and every negative value have no writer in the image.** The writers, from a census of every store into `+0x7C` in the UI ranges (14 immediate sites, 60 register stores, the register stores all preserving the low nibble under masks `0x3FF`, `0x3FF000`, `0x3FF7FF` and `bts`/`btr` of bits 10 and 11): the constructor `002465F0` (`002466D8`) and the release `002482E0` (`002483BE`) clear it to **0**; the forward starter `00246AD0` sets **2** (`and 0xFFFFFFD2; or 0x12`, `00246BEF`); the stepper `00246C20`, when a run completes, sets **3** with message 19 (`0024701B`..`00247039`) when its step is positive and **1** with message 20 (`0024704D`..`0024706B`) when it is not, [the message page](the-widget-message-protocol.md)'s *transition finished forward / backward*; the backward starter `00244DD0` sets **1** outright when `+0x40` bit 0 is ~~set~~ clear (`00244E1F`..`00244E23`) *(corrected 2026-10-02, OPUS: `00244DD0+0x4A` `test dl, 1` / `00244DD0+0x4D` `jne` skip to the arms when bit 0 is set; the state-1 store at `00244DD0+0x4F` runs only when it is clear)* and otherwise **4** (`00244ED7`..`00244EDB`) after its arms: from 0 or 3 it starts the backward run at the record's second half (`00244E47`..`00244EA0`), from 2 it reflects the run about the current frame (`00244E62`..`00244E7E`, the reflection §2 reads), and from 1 or 4 it does nothing (`00244E3E`..`00244E41`). So: 0 constructed and never run, 1 at the start (a backward run finished), 2 running forward, 3 at the end (a forward run finished), 4 running backward. The readers agree: `00244980` tears the widget down when the nibble is 1 and `+0x40` bit 6 is set (`002449B2`..`002449C6`), the forward starter's arms are 0, 1 and 4, the backward starter's are 0, 2 and 3. The `shl 28 / sar 28` read is the compiler's signed-bitfield idiom, not a sign the data uses. Static, image-wide store census and the five bodies read.*
- [x] ~~**UQ-184.** **What `+0x48`'s record is**, beyond carrying a `u16` duration at `+2`.~~
      ***NARROWED 2026-09-17 (FABLE):** the record's consumed layout - `u8 +0` mode (unless `+0x7C` bit 6 supplies one), `u16 +2` duration, `u8 +0xA`/`+0xB`/`+0xC` per-channel selectors (read minus one), `f32 +0x10` - is on the widget constructor page under `UQ-187`, from the evaluator `00244A20` and the starter; the default `00915198` is all zeros in those fields, a no-op; its two `u32 1` words at `+4`/`+0x18` have no reader found.*
      ***ANSWERED 2026-09-17 (FABLE): `+0x48` points at the widget's transition descriptor, two `0x14`-byte halves, the forward transition at `+0` and the backward one at `+0x14`.** The forward starter `00246AD0` binds `+0x68` to the record itself (`00246B9C` for the default), and the backward starter `00244DD0` binds it to the record plus `0x14` (`00244E80`..`00244E88`, or the default's `009151AC` = `00915198 + 0x14`) and reads the duration word at `+2` of that half (`00244E9C`); every consumer then reads through `+0x68`, so the layout [the constructor page](the-widget-constructor-and-object-sizes.md) lists under `UQ-187` (`u8 +0` mode, `u16 +2` duration in milliseconds, `u8 +0xA`/`+0xB`/`+0xC` per-channel selectors, `f32 +0x10`) is the layout of **each half**. That is why the default record carries `u32 1` at both `+4` and `+0x18`: the same field of the two halves. That word is read by nothing found; the stepper's curve kind comes from the property word `+0x80` bits 10..13 (`00246C89`, `00246CD5`..`00246CD8`), not from the record. Static, both starters and the stepper read.*
- [x] **UQ-185 ANSWERED 2026-09-15 (OPUS) — the arms are *attach if unparented, otherwise
      switch on*, and every test in §2's pseudocode is a field one of the two callees writes.**
      - **`00248220` (190 B) attaches the widget into the tree.** *(Size corrected from 85 B 2026-09-15 (OPUS): the body runs to the `ret` at `002482DD`, so `0x2DE - 0x220` = 190, matching the function inventory and [the widget contract](CONTRACT-widget-object.md), which had read the body. `check_consistency` flagged the pair.)* With `rcx` the parent and `rdx` the
        child: if `[parent+0x18]` is null the child becomes the **head**, otherwise it walks
        `+0x20` to the end of the sibling chain and links there, setting the predecessor's `+0x20`
        and the child's `+0x28` back-link. It then increments the parent's child count at
        **`+0x30`**, writes the **parent back-pointer to the child's `+0x10`** (`00248267`), and
        propagates the parent's `+0x40` **bit 5** (`00248264`–`0024826F`).
      - **`002473F0` (160 B) sets the object's `+0x40` bit 0 and propagates the change downward.**
        It **requires `+0x40` bit 1** (`test cl, 2` at `00247423`) and **returns without doing
        anything when bit 0 already equals the requested value** (`0024742D`) — it is a
        change-detector, not a setter. Otherwise it flips bit 0 (`00247431`–`0024743A`),
        dispatches an event through the object's own vtable, then **walks the children**:
        `rbx = [obj+0x18]`, calling `00247490(child, state, &code)` and advancing
        `rbx = [rbx+0x20]` (`00247450`–`00247476`).
      - **The event code is 7 for off and 6 for on**, built branchlessly at
        `0024740E`–`00247418`: `neg eax` / `sbb ecx, ecx` / `add ecx, 7`.
      - **The two arms interlock with the two bodies exactly, which is what settles the question.**
        §2 reads `if (w->_0x10 == 0) { flags_40 |= 2; 00248220(); }` — and **`+0x10` is the
        very field `00248220` writes**, so the arm is asking *am I still unparented?*. The other arm
        is `else if (flags_40 & 0x20) { flags_40 |= 2; 002473F0(w, 1); }` — and **`0x20` is the
        bit `00248220` propagates on attach**, while **`|= 2` is precisely the bit-1 gate
        `002473F0` tests before it will act**. Neither call is reached without its own precondition
        having been established by the other path.
      - **And the link they share is the same one.** The `+0x20` sibling pointer `00248220` writes
        is the `+0x20` chain `002473F0` follows: one builds the tree, the other traverses it.
      - **Not claimed:** what `00247490` does with the code beyond receiving it, and what the
        dispatched event means at the far end — that is `UQ-186`'s territory. **UQ-185.**
- [x] **UQ-186 ANSWERED 2026-09-15 (OPUS) — by citation, not by new analysis. Message 14
      is *“opening transition started”*, and it has been answered on
      [the widget message protocol](the-widget-message-protocol.md) §4 since 2026-09-13. The
      answer simply never reached this box, and this box's framing went stale.**
      - **The sending side.** Message 14's **only framework sender** is `00246AD0`: it clears the
        close bit 6, sets `+0x7C` to state 2 with direction `+1`, and sends record `01E0C0E0 = {14}`
        as its **last act** (`00246BEF`–`00246C09`). §6 of this page already established that
        `01E0C0E0` has **exactly one** rip-relative reference in all 38,161 bodies — so it is one
        record and one reference, not a shared constant.
      - **The receiving side, which is what this box said was missing.** The Config brightness row
        `0023B330` answers 14 — its dispatch subtracts 1, 3, 6, 2 and then `cmp ecx, 2`, so the
        arm at `0023B367` is id `1+3+6+2+2 = 14` — and that arm **tail-calls `002470D0`, which
        pushes the widget onto the focus stack**. A receiver taking focus as it opens is exactly what
        an opening-transition notice predicts.
      - **The objection this box was built on is resolved *inside* that entry.** The re-base of
        `0208F570` by `00228130` is **message 18, not 14** — its dispatch subtracts 1, 1 and 2
        before `cmp ecx, 0xE` — which §6 here also found independently. The protocol page
        records the same correction, so the *“one sender that argues against the current
        reading”* framing no longer describes the state of the evidence.
      - **Why this is a citation and not a finding.** I re-derived the `0023B330` arm from bytes
        before noticing it was already written down — under my own earlier task
        `OPUS-DL1-MESSAGE14-RECEIVER`. The re-derivation agrees in every particular and is worth
        nothing beyond confirming it. **What was actually wrong was that the answer had not
        propagated to this page**, which is the defect this commit fixes. **UQ-186.**

## 7. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| 148 call sites | `E8` 142 + `E9` 6, both instruments with a positive control | 1 | PROVEN |
| the object is in `rdx` and null-checked | `test rdx, rdx / je` is the first instruction | 1 | PROVEN |
| `frames = ms * 60 / 1000` | `imul ecx, eax, 0x3C` then the `0x10624DD3` / `shr 6` divide-by-1000 idiom | 1 | PROVEN |
| the rate is `1.0f` unless mode 2 | `01CEBBA8` resolved with a tool; `cmp eax, 2 / jne` guards the reciprocal | 1 | PROVEN |
| the state nibble is signed and 4-bit | `shl eax, 0x1C` / `sar eax, 0x1C` | 1 | PROVEN |
| the duration has an inline override | `bt edx, 0xA` / `btr` / `shr 0xC` / `and 0x3FF` | 1 | PROVEN |
| state 4 reflects about the current frame | `2*[0208F570] - [+0x70] - [+0x74]` | 1 | PROVEN |
| message id 14 is dispatched | `lea rdx, [01E0C0E0]`, whose first dword is `0x0000000E`; `call rax` through `[rbx]` | 1 | PROVEN |
| `0208F570` counts frames | **corroborated, not proven** — see §4 | 2 | PROBABLE |
| what mode 2 is | **not established** | — | UNKNOWN |
| any runtime observation | **none exists** | — | UNKNOWN |

## 8. Related

- [The widget message protocol](the-widget-message-protocol.md) — id 14 and `DL-1`
- [Contract — the widget object](CONTRACT-widget-object.md) — the object this operates on
- [The blinking icon and its atlas](../../99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md) — the other user of `0208F570`

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run on the addresses this pass introduces. Static only: the shipped
image, its function list and a rel32 census. Nothing executed, nothing observed live.)*

### The function re-read whole, and §7's table holds

All ~~330~~ 321 bytes disassembled *(corrected 2026-10-02, OPUS: the last instruction is `00246AD0+0x140` `ret`)*. **148 call sites — 142 `E8`, 6 `E9`** (positive control: the `ret 0` stub
`0016D6A0` at 2,528 + 340 = 2,868 by the same instruments). `test rdx, rdx` is the first instruction.
Every figure in §3 reproduces: `0x3f800000` into `+0xB8`; the reciprocal guarded by `00229DF0()` and
`00229EA0() == 2`, dividing `[01CEBBA8]` by `00229E70()`'s return; `shl eax, 0x1C` / `sar eax, 0x1C`;
`js` for negatives, `cmp 1 / jle` for the start arm, `cmp 4 / jne` for the rest; `imul ecx, eax, 0x3c`
then `0x10624DD3` / `mul` / `shr edx, 6`; `bt edx, 0xA` / `btr` / `shr 0xC` / `and 0x3FF`;
`and 0xFFFFFFD2` clearing bits 0, 2, 3, 5 and `or 0x12` setting 1 and 4, leaving the nibble at **2**;
and `lea rdx, [01E0C0E0]` with `mov rcx, rbx` before `call rax`, the record's first dword **14**.

### ✖ Corrected: the "mark started" bit goes into `+0x40`, not `+0x7C`

`00246B95` is **`or dword ptr [rbx + 0x40], 0x200`**. §3's block writes `[rbx+0x7C]`, which is the
state word the same arm then reads and rewrites through `edx` — so a reader would look for bit 9 in
the wrong word, and would also see a conflict with the `and 0xFFFFFFD2` / `or 0x12` at the end, which
does own `+0x7C`. The rest of that block is exact, including the sense of the `0x8000` test: when the
flag **is** set the `jne` skips `mov rcx, [rbx+0x48]` and the default source `00915198` stands.

### ✔ New: the frame reading, measured on the **writer** side

§4 corroborates `0208F570` from a second **reader**. The writers settle more. Over all 38,161
function bodies, every rip-relative reference to `0208F570`:

| | |
|---|---:|
| references | **149** |
| reads | **143**, in **109** distinct functions |
| **writes** | **6** |

and the six writes are the whole story:

| site | in | what it does |
|---|---|---|
| `0022819C` | `00228130` | **assigns** it from `[01FD46F4]` — a re-base, on **message 18** (corrected 2026-09-13, was "message 14"; see § below) |
| `00250587` | `00250540` | `add` of `00184950()` = `[01F3DA18]` |
| `002505C9` | `00250540` | `add` of `r14d`, computed just above as **1 or 2** |
| `002506E2` | `002506D0` | `add` of `00184950()` |
| `00250763` | `00250730` | `add` of `eax = 2 / [01DFE0B4]` — **1 at full rate, 2 at half** |
| `00250801` | `002507C0` | `add` of `00184950()` |

**There is no decrement, no multiply and no other assignment anywhere in the image.** A global that
only ever advances, by a small step taken once per UI tick, is a frame counter being used as one —
and the step is **rate-compensated**: `2 / divisor` and the `1`-or-`2` above both double when the
tick rate halves. So this function's hard-coded `60` is not a bug waiting for a variable frame rate;
the counter it spends against is already in 60 Hz units. **`0208F570` counts frames** is still a
reading rather than a live observation, but it now rests on the six writers and not only on two
readers agreeing.

### ✖ WITHDRAWN: the "receiving-side constraint on `DL-1`" was a constraint on a different message

**FABLE was right and this section's conclusion is withdrawn** (`FABLE-CONTRA-OPUS-REBASE-MSG18`,
2026-09-13). I read `00228156 cmp ecx, 0xE` as "id 14" without accounting for the three subtractions
above it.

```
00228139  mov ecx, [rdx]        ; the message id
0022813B  sub ecx, 1  / je      ; id 1
00228144  sub ecx, 1  / je      ; id 2
0022814D  sub ecx, 2  / je      ; id 4
00228156  cmp ecx, 0xE / je     ; ecx is id-4 here, so 0xE means id 18
```

**`ecx` is `id - 4` by the time of the `cmp`, so the arm is message 18, not 14.** Re-read from the
image on 2026-09-13 and FABLE's reading holds in every particular.

> **What this costs:** the entire argument above. A re-base on message 18 says *nothing* about what
> message 14 is, so there is no receiving-side constraint on `DL-1` here and `§4`'s sending-side
> argument now stands alone. **`DL-1` is weaker than this page claimed**, not stronger.

**What survives, because it was decoded rather than inferred:** `00228130` is a widget procedure by
the protocol page's shape test — it reads `dword [rdx]` first and tail-jumps to `005C5230`
(`00228163`) — and its **message-18** arm calls `00247780`, `00251E80`, `00229510`, `00365980`,
`003601C0(3)`, re-bases `0208F570 = [01FD46F4]` at `0022819C`, and then **clears its own bit 5** at
`002281DE` (`and dword [rbx+0x40], 0xFFFFFFDF`). That last store is the independent check: **ASTRA's
spawn page §22.4 reads the same bit-5 clear as a message-18 act**, from a different direction, and
the two agree.

> **The lesson is narrower than "check the arithmetic".** A `cmp` against a literal in a `sub`
> chain is *never* the id — the chain has been consuming it. I quoted the literal as though the
> comparison were against the original value, and then built a paragraph of argument on top of it.
> **A decode that is used as a premise has to be re-derived, not re-read.**

### ✔ New: the message record is this function's alone

`01E0C0E0` has **exactly one** rip-relative reference in all 38,161 bodies — `00246BFF`, here. It is
not a shared "message 14" constant that several senders point at; it is this function's own record.
So "one sender" in §4 is stronger than it reads: one *record*, one *reference*.

**Not claimed.** Everything in §6 stands: `00229DF0` / `00229EA0` / `00229E70` and what mode 2 is,
states 2, 3, 5–7, the record at `+0x48`, `00248220` / `002473F0`, and what message 14 means. What
`00184950`'s global `[01F3DA18]` and the divisor `[01DFE0B4]` are set to, and by whom — **not
censused**; the step's *shape* is read, its values are not. What `[01FD46F4]` holds. **No runtime
observation exists and none was made.**

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role |
|---|---:|---|
| `00367200` | 1196 | animation tick driver — called by `00250540`/`00250730`/`002507C0`/`003676B0`; whole body is two helper calls (`00367ED0`, `003676D0`) plus its own loop bookkeeping; helper interiors not walked |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT and SERVICE, 66 edges.**
  - Cited widget functions are called by core frame bodies: the 2,001-byte body (17), `MainLoop_UpdateAndRenderFrame` (10), the 463-byte body (9), and bodies of 174 bytes (6) and 163 bytes (5).
  - They call small core helpers (8 and 7 bytes) and larger core bodies (277 and 2,232 bytes).
- **WorldAreaField - CLIENT and SERVICE (9 edges).** `001EC560`, `00306570`, `003065D0` are called by bodies filed to WorldAreaField: `001EDCD0`, BattleSystem_InitializeAreaState (`002342F0`), BattleSystem_RunFieldFrameOrchestrator (`00234590`); `0022A770`, `00280140`, BattleAction_InitializeGlobalSpecialSequenceMode (`00306BD0`), `003C9FD0` reach bodies filed to WorldAreaField: WorldTransition_RequeueCurrentFieldForRestore (`00267C90`), WorldPersistence_ResetBanksAndMarkInitializationState (`00268320`), World_UpdateSimulationTick (`00314020`), WorldTransition_RequestFieldTransition (`00314440`) (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - SERVICE (2 edges).** the field-frame orchestrator `00234590` reaches `BattlePerception_AdvanceCandidateCacheGeneration` (`00325060`) and `BattlePerception_ResetSpatialVisibilityCacheFrameState` (`0032A650`).
- **RNG_Random_Selection - SERVICE (1 edge).** `BattleSystem_InitializeAreaState` (`002342F0`) seeds `RNG_SharedGameplayLCG_SetState` (`00328D80`).
- **Rewards_Progression_Economy - SERVICE (2 edges).** `002342F0`/`00234590` reach `Loot_InitializeWorldPickupPool` (`00319B10`) and `Loot_UpdateWorldPickupLifetimeAndDespawn` (`00319600`) - the init/frame path runs the world-pickup pool.
- **Spawn_Encounter_Lifecycle - SERVICE (3 edges).** `002342F0`/`00234590` reach `SpawnKeep_RotatePersistenceBanksForAreaTransition` (`00233780`), `SpawnGroup_ResetLifecycleLedger` (`00307090`) and `SpawnGroup_DispatchPendingCompletionSignals` (`00307030`).
- **Status_Periodic_Terminal - SERVICE (2 edges).** `002342F0`/`00234590` reach `BattleStats_RemoveStatusMode0` (`0030E990`) and `BattleUnit_ResetActionControlForStatusTransition` (`00300140`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Party — CLIENT.** `VMPartyCommand_RemoveSelector00To06_Async`, owned by that layer, calls `003601C0` on this page. That caller is a 97-byte three-state async command over the caller's `dword[+0]`: state 0 arms it, state 1 runs the removal for `byte[+4]` and takes the `0x13` slot, and state 2 polls for completion before releasing it; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — SERVICE.** `0022A770` on this page calls `FUN_00316930`, owned by that layer. What it reaches is a 287-byte walk of the same `[022C2550]` table against the data at `01EED130`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**SaveLoad — CLIENT.** `FUN_00280140`, owned by that layer, calls `00251E80` on this page. That caller is the save/load screen's message handler: message 1 picks save or load from `(qword[+0x10] & 0x7FFF)` and takes the state block at `[0209AC30] + 0x3F8`, message 2 runs the image operation and records the outcome in that block's `byte[+8]`, and message `0x10` tears the screen down and clears `[0209AC30] + 0xC0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 16 edges).** The widget-animation millisecond-to-frames
path runs inside the frame update: `0022A770` calls `MainLoop_Draw` `0022B0B0`,
`RenderSystem_RunCharacterUpdatePipeline` `003323D0`,
`EffectSystem_ProcessQueuedGraphicsEffectsForPass` `00375500`, the cutscene support `001EC560`,
the transparency-fade update `00256F60`, the camera view-modifier bank `0037D4C0`, `002E65A0` and
`002529F0` (9 callee edges); `00229EA0` is reached by `PresentationEntry_UpdateForCurrentGlobalPhase`,
the effect-font materialization consumer `003E9780`, `RenderModelInstanceContainer_ProcessActiveEntries`
and `002528A0`; `00184950` is reached by `Presentation.CharacterRender.FieldFill` `001D7DD0`. The
animation advance is one of the things the frame update drives — the crossing is the cadence.

**Input — CLIENT and MECHANICAL (SWE2-CONTRACT 2026-09-15, 15 edges).** `00229DF0` is consulted by the three
temporal-gate input testers (`InputGameplay_TestAggregatedMask62Bit1WithTemporalGate`,
`InputGameplay_TestCombinedMaskBit1WithTemporalGate`,
`InputGameplay_TestFilteredMask92Bit0WithTemporalGate`); `0022A770` calls the input-rebuild family
(`InputGameplay_RebuildFrameSnapshotFromChannelHistory`, `InputControl_SetOneShotFrameCallback`,
`InputGameplay_RebuildRemappedTransitionMaskState`, `0035AE30`/`0035AF20`/`0035FF90`/`0017DE60`/
`00250180`/`0036FF70`); `00184950` trades calls with `0035FF90`/`00360080`. Frame-cadence adjacency —
the animation advance and the input rebuild run on the same tick.

**Script_VM_Native_Bridge — MECHANICAL (SWE2-CONTRACT 2026-09-15, 7 edges).** `003601C0` is shared with four
script-bridge bodies (`0034C370`/`003464D0`/`00345140`/`003506A0`); `00247780` with `00510990`/
`00510950`; `00229EA0` with `00354D00`. Shared frame helpers only.

**CombatAction — CLIENT (4 edges).** `00306B10`/`00306BD0` call `0032F6C0`/`0032F6E0`, and
`00306570`/`003065D0` call `00332190` — the widget-animation helpers (`003C9FEF`/`003CA014`/
`003CA020` context) this page names. The combat-action layer starts the same widget animations when
an action needs its UI feedback; fan-in, not shared ownership. Read from `edges.tsv` 2026-09-17
(SWE2-FRONTIER).

## The `00250540` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00250540` (~430 B) — the per-frame UI pump called by the full-menu
and capture frames — runs `001EDE70`, `00181DD0`, member-adjacent
`00184960` (`0025056B`), `0017E4E0`, the `dword[02064AA0]` gate
(`00250579`), `00184950` then `add dword[0208F570], eax`
(`00250587`), the `002481A0`/`00248030`/`00248190`/`002481C0`
drain on `[0208EA48]` (`0025058D`–`002505A3`), `00244970` (the
recursive completion pass), `00250CA0`, tail `003676B0`
(`002505C4`). The `0208F570` arms: `add eax` vs `add r14d` = 1-or-2
(`002505C9`), `dword[020927DC] = 0`, `00229EA0()` vs 5 → member
`002508E0` (`002505EA`); the third arm `003C9FD0(3)`
(`0025060A`), `00254CC0`, `002481A0`, and the three-cell walk on
`0208EA20` (`0025061C`–`00250633`).

| member | role | interior |
| --- | --- | --- |
| `002508E0` (124 B) | the mode-5 drain — `002481A0`, then `00248030` on `0208EA38` **only when its `+0x18` is non-null** (`002508F0`/`002508F5`), then unconditionally on `0208EA40` and `0208EA48` (`002508FC`–`0025090F`). The gate is why the page's own anchor cites `002508F0` | [`002508F0`](../../_index/ADDRESS-INDEX.md) |
| `003C9FD0` (204 B) | mode-gated step — `ecx` vs 3 (`003C9FD4`), `dword[02B47750]`/`dword[02B47748]` vs 1 (`003C9FE1`/`003CA008`), `0032F6E0`/`0032F6C0`/`00332190` (`003C9FEF`/`003CA014`/`003CA020`) | [`003C9FE1`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001EDE70`, `00181DD0`, `00184960`,
`00184950`, `0017E4E0`, `002481A0`, `00248030`, `00248190`,
`002481C0`, `00244970`, `00250CA0`, `003676B0`, `00229EA0`,
`00254CC0`, `0032F6E0`, `0032F6C0`, `00332190`.

## SWE2-EC7-18 update (2026-05-15) — `00247780` message-18 arm callee fragment

`00247780` (22 B) is one of the four callees this page's message-18 arm invokes (`00247780`, `00251E80`, `00229510`, `00365980`) and CONTRACT-sound-request confirms the same `(1)` call shape ahead of `002D7960`/`00249840`: `eax = [0208ED58]`, `edx = (eax ^ ecx) & 1`, `eax ^= edx`, `[0208ED58] = eax` (`00247780`..`0024778F`) — a read-modify-write that sets bit 0 of the `0208ED58` flag dword to the caller's `ecx&1`, the animation/sound enable bit the two pages agree the message-18 arm flips.
