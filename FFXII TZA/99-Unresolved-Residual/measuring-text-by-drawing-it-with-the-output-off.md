---
system: Measuring text by drawing it with the output off
category: 99-Unresolved-Residual
status: AUDITED — every register row is closed (owner re-status 2026-09-30, OPUS; SD-100 answered) — what `002AF340` returns is read (the characters laid out up to the stop string, or -1; §4, 2026-09-30) and every cluster member is read (UQ-383); what the reveal stepper's modes are for is answered (SD-100, 2026-09-30)
owner_layer: CodeDomain:Presentation.Text
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `002A4430`, `002A4830`, `002ABB20`, `002AF960`, `002B2DF0`, `002B5390` and 1 more, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: residual-cluster-1-repos-55
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record residual-cluster-1-repos-55; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# Measuring text by drawing it with the output off

**Residual cluster 1 is the biggest — 13 functions, 21,162 bytes, 11.7 % of the whole residual.**
Two members were already read: `002AC5F0`, the control-code interpreter, and `002AAE40`, the
per-character draw walk. **This adds three more**, and the first of them answers a question the
interpreter's document raised.

## 1. What the player sees

**A message box that knows how big it needs to be before it draws anything**, and a scrolling window
that stops at the end of a paragraph rather than in the middle of one.

**And text that animates in** — a state machine advances a counter ~~every **30 frames**~~ *(corrected 2026-09-30, SWE2-DATA: at a rate counted in thirtieths per stepper call, §5)* and the
displayed line follows behind it, which is the shape of text arriving a piece at a time rather than
all at once.

## 2. Measuring is drawing with the output switched off

`002B2150` runs the **same character walk** as the draw pass and produces a width and a height. The
way it avoids drawing is the finding:

```c
saved_output   = DAT_0209CC48;          // the draw pass's own gate
saved_flags    = ctx[0x10FC], ctx[0x10FF];
saved_pen      = _DAT_0209CC60, _DAT_0209CC68;
saved_font     = FontPainter_GetDescriptor();     // 0017F940

DAT_0209CC48 = 0;                        // <- switch drawing off
ctx[0x10FF]  = 1;                        // <- and say we are measuring
FontPainter_SetDescriptor(0);            // 0017FAE0

...walk the string, accumulating pen advance and max height...

DAT_0209CC48 = saved_output;             // put everything back
FontPainter_SetDescriptor(saved_font);
if (out_w) *out_w = width;
if (out_h) *out_h = height;
```

**Read at instruction level, because the whole document rests on it:**

```asm
002B2256  call  0x0017F940                     ; save the font-painter descriptor
002B226A  mov   qword ptr [rsp + 0x40], rax
002B226F  xor   eax, eax
002B2271  mov   qword ptr [0x0209CC48], rax    ; <- the output pointer, NULLED
002B2278  mov   byte ptr [rcx + 0x10ff], 0x1   ; <- "measuring"
002B2281  mov   qword ptr [0x0209E598], rax
002B2288  call  0x0017FAE0                     ; FontPainter_SetDescriptor(0)
...
002B2416  mov   qword ptr [0x0209CC48], rdi    ; restored from 002B2196
```

> **`DAT_0209CC48 == 0` is the exact condition `002AAE40` returns on at its head.** The measure pass
> does not reimplement the walk — **it nulls the thing the walk checks, runs the walk, and puts the
> pointer back.**

**And `0209CC48` is a pointer, not a flag.** A census finds **39 sites across a dozen functions**,
manipulated as a qword — `cmp qword ptr [0x0209CC48], rdi`, saved into a register and restored.
**It is the current output target**, and measuring is *"aim at nothing"* rather than *"set a bit"*.
**The decompiler renders both the same way**, and the difference matters for anyone hooking it.

**That is the mechanism behind the mutual recursion `repos-78` identified** between the interpreter
and the measure/emit passes: there is only one walk, and *measure* is a mode of it. **A control code
that inserts text gets that text measured by the same machinery currently interpreting it, and
nothing has to be written twice.**

**The walk here is the same `< 0x10` split** — tokens to `002AC5F0`, characters to `002AC2F0` then
`0020E600` and `0017F8C0` — with **three extra early-outs** the draw pass does not have: a byte of
`0`, a byte of `2`, or a character matching the head of the **stop-set** at `ctx + 0x10C8` ends the
measurement.

## 3. The stop-set is a borrowed global

`ctx + 0x10C8` holds a pointer to a terminator set. **`002ABB20` overrides it and restores it around
each call**:

```c
saved = ctx[0x10C8];
ctx[0x10C8] = &DAT_00916548;      // measure with THIS stop set
... FUN_002AF340(state, text, buf, 1) ...
ctx[0x10C8] = saved;
```

> **A global swapped in and out around one call is a parameter that did not get one.** The measure
> pass reads it, the scroll pass sets it, and **nothing in either function's signature says so** —
> which is why neither could be understood alone.

## 4. Scrolling stops at a boundary, not after N lines

`002ABB20` advances the visible line by the step at `state + 0xA0`, **unless it can find a stopping
point first**:

```c
n = FUN_002af340(state, text, buf, 1);            // lay out from the current line
if (n < 0 || n > current_line + step) {
    current_line += step;                          // no boundary in reach: just advance
} else {
    for (i = 0; i < step; i++) {
        off = FUN_002b20b0(text, current_line + i); // line index -> byte offset
        n   = FUN_002af340(state, text + off, buf, 1);
        if (n < 0) break;
        if (n < 2) { current_line += i + 1; return; }   // <- stop here
    }
    current_line += step;
}
```

**The caller treats the return as a count and stops when it is `< 2`.**

> **CORRECTED after reading `002AF340` (§4b): its own decompilation returns `void`.** The callee
> ends by restoring globals and falling off; **no return value is visible in it at all**, while the
> caller plainly consumes one. This is the *unmodelled return* misdescription class — **~~so what the~~
> ~~value counts is not established from either side~~**, and the earlier wording here, *"returns a
> count"*, asserted more than the code showed.
>
> *(Corrected 2026-09-30, SWE2-DATA: read at instruction level, `002AF340` does return a value; the decompiler dropped it. Its one `ret` leaves `eax` = `r12d` (`002AF927`), or -1 (`002AF922`) when its fourth argument is set, a stop-set is installed at `ctx + 0x10C8` and the walk never met it. `r12d` starts at 0 and gains 1 per character (`002AF51D`, `002AF535`) plus the count the interpreter reports for a token (`002AF79C`). The stop test is `memcmp` of the stop string against the text (`002AF563`), and a match ends the walk. The stop string `002ABB20` installs, `00916548`, is `0F 23`: the `#` page-wait escape. So the value is **the number of characters from the current line to the next page wait**, and `n < 2` stops the scroll on a line that begins at one. Control `_index/candidates/dd-data-3-0930/measure_checks.py` A1–A4.)*

## 4b. `002AF340` measures a block, not a line

**It is the third function to use the same idiom** — save `0209CC48`, `0209E598` and the font
descriptor, null all three, walk, restore. **`002B2150` measures one line and returns a width and a
height; `002AF340` walks the whole string and fills a layout record** at its third argument:

| field | role |
|---|---|
| `+0x10` | the **current line's** width, reset at every break |
| `+0x14` | the current line's height |
| `+0x20` | the **widest line so far** |
| `+0x24` | the **accumulated total height** |
| `+0x30`, `+0x34` | a second pair of maxima, updated from `+0x20` and `+0x24` |
| `+0x1C`, `+0x2C` | reset to `1.0f` at every line break |

**Four byte values are handled before the interpreter is consulted:**

| byte | effect |
|---|---|
| `0`, or a match against the **stop-set** at `ctx + 0x10C8` | finalise the line and **return** |
| `3` | finalise the line and **continue** — a hard break |
| `2` | **call `002B2150` on the remainder**, take the max of its width and height, then break the line |
| `0xE` | call `002B3E30` and add `DAT_01E0CDE8` to the total height — **a fixed extra gap** |

> **Byte `2` is the interesting one.** The block measurer hands the rest of the string to the *line*
> measurer and uses the result as this line's extent. **Two measure passes, one calling the other**,
> and the outer one had already nulled the output pointer that the inner one nulls again.

**And a negative `uStack_a0._2_1_` — a signed byte of the text state — is subtracted from the line
width at every break**, then reinstated as the starting width when positive *(anchored 2026-09-30, SWE2-DATA: the byte is text-state `+0xAA`, held in `sil`; the three break sites `002AF591`, `002AF6A5` and `002AF832` subtract it only when it is negative, and `002AF75D` stores it as the line width only when it is positive; `_index/candidates/dd-data-3-0930/measure_checks.py` A5)*. That is a hanging
indent: **a negative value widens the first line, a positive one indents every line.**

## 5. The animation stepper

> **JOINED 2026-09-13 (OPUS): `002ABF70` is also documented, independently and in different terms,
> by [the UI request router](../16-UI/Request-Router/ui-request-router.md) §`002ABF70` opened.**
> Neither page cited the other, and `check_consistency` never noticed — it compares stated names and
> sizes, and **two pages describing one function in different prose collide in neither.** Three
> things that page establishes and this one did not:
>
> - **`+0xB0` is one dword carrying a mode *and* flags**, and `002ABF70` reads it whole before taking
>   `cl`. **Bit 22 is read only by state 2** — so a reader treating `+0xB0` as a byte gets the right
>   state and loses the flag entirely.
> - **The clamp is `0x7D00` = 32,000**, applied to `+0x8C` at two separate sites — the *"clamped at
>   32000"* below, with the constant.
> - **There are eight modes and six distinct bodies**, the jump table sits in `.text` after the
>   `ret`, and **mode 6 is a no-op** that jumps straight to the epilogue.
>
> And one thing that travelled the other way: that page called `+0x5A` *"a countdown"*. **It is the
> brightness**, as §5 says below and as [the rectangle primitive](drawing-one-coloured-rectangle.md),
> [the blinking icon](the-blinking-icon-and-its-atlas.md) and
> [the widget-tree draw pass](the-widget-tree-draw-pass.md) all read it — **so state 2 is a fade-out**,
> which answers that page's own open question about what its mode 2 is. The correction is applied there.

`002ABF70` switches on `state[+0xB0] & 0xFF` — **states 0 through 5 and 7** — and steps counters:

| field | role |
|---|---|
| `+0x88` | a **countdown**; states 3 and 7 decrement it and act at zero *(answered: see §7, corrected 2026-09-30: state 3 also steps the target by `+0xA0` on every tick while it is non-zero; 2026-10-02, OPUS)* |
| `+0x8C` | ~~the target line~~ the **head**, in characters *(corrected 2026-09-30, SWE2-DATA, per UQ-173)*, **clamped at 32000** |
| `+0x8E` | the previous value of `+0x8C` |
| `+0x90`, `+0x92` | a **following pair** that trails `+0x8C` by `+0xA0` |
| `+0x9B` | a **frame accumulator**, advanced by `+0x9C` |
| `+0x9D`, `+0x9E` | ~~a value converging on a target by `±0xA0` per step~~ the lag by which the target trails the head, and its bound *(corrected 2026-09-30, SWE2-DATA, per UQ-173)* |
| `+0xA0` | the step size |

~~**The period is 30 frames**~~: `+0x9B += +0x9C` and the work fires when `+0x9B > 0x1D`, or immediately
when `+0x9C` is exactly `0x1E`. *(Corrected 2026-09-30, SWE2-DATA: 30 is the denominator of a rate, not a frame count. `+0x9C` is the step rate in thirtieths per stepper call, and how often the stepper is called per frame is not traced ([the UI request router](../16-UI/Request-Router/ui-request-router.md), FABLE 2026-09-14).)* **State 2 additionally decrements the brightness at `+0x5A`** — the
same field the [rectangle primitive](drawing-one-coloured-rectangle.md) multiplies colours by — **so
state 2 is a fade-out.**

> ~~**Thirty frames again.**~~ The [blinking icon](the-blinking-icon-and-its-atlas.md) pulses on a
> `sinf(frame × π / 30)`, a 60-frame cycle built from the same divisor. **`0x1E` appears here as a
> literal period.** ~~Whether one constant or two is not established — **they are equal, and that is~~
> ~~all this says.**~~ *(Corrected 2026-09-30, SWE2-DATA: they are two quantities. The stepper's `0x1E` divides a per-call rate (§5 above), and the icon's divisor sets a per-frame sine period, so no shared constant is claimed.)*

## 5b. Key addresses (SWE2-DATA, 2026-09-30)

| address | role |
|---|---|
| `002B2150` | the line measurer: nulls the output pointer `0209CC48` and walks one line |
| `002AF340` | the block measurer: fills a layout record and returns the character count to the stop string |
| `002ABB20` | the scroll step: installs the stop-set `00916548` (`0F 23`) and snaps to a page wait |
| `002ABF70` | the reveal stepper: eight modes through the table at `002AC1B4` |
| `002AAE40` | the draw walk, which returns at its head when `0209CC48` is 0 |
| `002AC5F0` | the control-code interpreter the walks share |

## 5c. Call chain (SWE2-DATA, 2026-09-30)

```
002ABF70 reveal stepper (modes 0/1/4)
  -> 002ABB20 scroll step, stop-set 00916548 installed
       -> 002AF340 block measure (arg 4 = 1)
            -> 002AC2F0 character arm; 002AC5F0 interpreter for bytes <= 0x0F
            -> 002B2150 line measure, for byte 2
       -> 002B20B0 line index -> byte offset
```

The edges are the call sites this page cites (`002AC0A7`, `002AF4AD`, `002AF783`), and the pass-22 edge list below.

## 5d. Modding notes (SWE2-DATA, 2026-09-30)

- A page wait (`0F 23`, the `#` escape) is also where a scrolling window stops, because `002ABB20` measures to it. Moving or removing one in authored text changes where scrolling stops as well as where the text pauses.
- Hooking the draw pass sees the measure passes too: measuring calls the same walk with `0209CC48` nulled. A hook that must see only real drawing has to test that pointer.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `DAT_0209CC48` really the draw pass's gate, or two globals that happen to share an address? | `002AAE40` returns at its head on `DAT_0209CC48 == 0`; `002B2150` writes `0` to it at `002B2271`, walks, and restores at `002B2416` from the value saved at `002B2196`. **Same symbol, one writes what the other tests.** |
| Is the zero real, or did the decompiler invent it from a register? | **Checked, because the document rests on it.** `002B226F  xor eax, eax` immediately precedes `002B2271  mov [0x0209CC48], rax`. **The register is provably zero at the store.** |
| Is it a flag or a pointer? | **A pointer** — 39 sites image-wide manipulate it as a qword, several comparing it against a register (`cmp qword ptr [0x0209CC48], r15`). **This document first called it "switched off", which describes a bit; it is nulled.** |
| Could `002B2150` be a separate walk that merely resembles the draw walk? | Same `< 0x10` split, same three callees on the character arm (`002AC2F0`, `0020E600`, `0017F8C0`), same interpreter on the token arm, **and the same `ctx + 0x10FC` two-state tracking with the `× 2.3` adjustment.** |
| Is `+0x9B > 0x1D` really a 30-frame period? | The accumulator is compared against `0x1D` after adding `+0x9C`, and the fast path tests `+0x9C == 0x1E` exactly. **Both constants are 30 or one less.** |
| Is state 2 really a fade? | It decrements `state[+0x5A]` toward zero and clears it outright when flag bit 22 is set. **`+0x5A` is the brightness three other documents multiply by.** |
| Is the stop-set really borrowed rather than owned? | `002ABB20` saves `ctx[0x10C8]`, overwrites it, calls, and restores — **twice, once per call site.** A field a function restores is not its own. |
| Does `002AF340 < 2` really mean a boundary? | *(Answered 2026-09-30, SWE2-DATA: yes. The value counts the characters up to the `#` page-wait escape (§4), so under 2 means the line starts at a page wait; `_index/candidates/dd-data-3-0930/measure_checks.py`.)* ~~**Not established, and now known to be harder than it looked.**~~ `002AF340` has been read (§4b) and **its decompilation carries no return value** while the caller consumes one. The branch in the caller is read correctly; **neither side shows what the number is.** |
| Is `002AF340` really a third instance of the measure idiom, or does it just resemble one? | It saves `0209CC48`, `0209E598` and `0017F940`'s result, nulls all three, and restores all three on **both** exit paths. **Same three globals, same order, same restore.** |

### Evidence (SWE2-DATA, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| measuring is the draw walk with the output pointer nulled | `002B226F`/`002B2271`, `002AAE40`'s head test | 1 |
| `002AF340` returns the characters up to the page wait, or -1 | `_index/candidates/dd-data-3-0930/measure_checks.py` A1–A4 | 1 |
| the signed indent byte `+0xAA` | `_index/candidates/dd-data-3-0930/measure_checks.py` A5 | 1 |
| the stepper's eight modes and the `+0x88` countdowns | `_index/candidates/dd-data-3-0930/measure_checks.py` A6; the table at `002AC1B4` | 1 |
| the field meanings in §5 | UQ-173 (ANSWERED) | 2 |

*(Evidence table added 2026-09-30, SWE2-DATA.)*

## 7. What this document does not claim

~~What `002AF340` computes or what its return counts.~~ What `002B20B0` maps beyond line index to byte
offset. ~~What `DAT_00916548` contains — it is the stop-set installed during scroll measurement and~~
~~its bytes were **not** read.~~ ~~What states `0`, `1`, `4`, `5` and `7` of §5 distinguish~~ *(answered: see the reveal-stepper row below; 2026-10-02, OPUS)*~~, or what~~
~~`002ABF70`'s object is attached to~~. ~~**Which of the thirteen cluster members drive which.**~~

*(Corrected 2026-09-30, SWE2-DATA: the return and `00916548` are read (§4). The object is the message and selection window, and every cluster member has a reading (UQ-383, ANSWERED). The modes remain, below.)*

- [x] **What the reveal stepper's modes are for.** The bodies are read: modes 0, 1 and 4 share `002AC06B` (step and scroll), 2 is the fade, ~~3 counts `+0x88` down and then resumes stepping~~ 3 steps the target by `+0xA0` on every tick while `+0x88` is non-zero, and at zero primes `+0x9B` = `0x1E` and sets mode 0 *(corrected 2026-09-30 on SWE2-AUDIT-SEM's batch-3 review S3)*, 5 steps the target at the rate, 6 does nothing and 7 counts `+0x88` down to mode 0 (`_index/candidates/dd-data-3-0930/measure_checks.py` A6). Which writer sets each mode, and what the player sees in each, is not traced. **SD-100** (SWE2-DATA, 2026-09-30). *(SD-100 answered 2026-09-30 by OPUS `da3426b96`, [record](../_index/candidates/sd100-reveal-modes-0930/README.md).)*

## 8. Cluster 1 progress

| | |
|---|---|
| read | `002AC5F0`, `002AAE40`, `002B2150`, `002ABB20`, `002ABF70`, `002AF340` — **6 of 13** *(on 2026-09-03; all 13 have a reading since 2026-09-18, UQ-383)* |
| unread | `002A4830`, `002AE610`, `002AF960`, `002A4430`, `00573BE0`, `002B5390`, `002B2DF0` *(answered: see the row above: all 13 have a reading since 2026-09-18, UQ-383; 2026-10-02, OPUS)* |
| bytes read | ~13,900 of 21,162 |

**`002B2150` is the cluster's hub** — six neighbours that were residual when surveyed, more than any other member, and it is itself classified at GN162 as `UI.Text.MeasurePass` — and
reading it was worth more than its 861 bytes suggest, because it explains *why* the cluster is one
component: **the measure pass, the draw pass and the interpreter are the same walk under three
settings of two globals.**

*(Pass 22 adjacency, 2026-09-14: the measure pass uses the same scheduler yields as the draw pass —
`002AAE40`, `002AC2F0`, `002AE610` call the `CoreRuntimeScheduling` ~~yield~~ `0020E600` and
`002AC5F0` calls `00229E40` (7 edges) *(corrected 2026-10-02, OPUS: neither is a scheduler yield: `0020E600` is the 10-byte image-address resolver `mov eax, ecx; add rax, [01F83530]; ret` and `00229E40` the 7-byte getter `mov eax, [01E02814]; ret`, so they are not preemption points)*, and `00229E40` is itself called by
`Rewards_Progression_Economy` `00317ED0`. Expected: this page's thesis is that measure and draw
are the same walk under two settings, so the walk's preemption points are shared by
construction.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT and SERVICE, 18 edges.** Cited functions are called by Presentation bodies of 6,441 bytes (6), 2,440 bytes (4), 3,020 and 684 bytes (2 each), and 610 bytes. They call `RenderCommand_SubmitCurrentBufferAndSwap` (2).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Script_VM_Native_Bridge — CLIENT.** `FUN_0033fed0`, owned by that layer, calls `00229E40` on this page. That caller is a 37-byte forwarder that reads the frame-mode getter and **maps the single value `0xA` to zero** before passing it on; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Rewards_Progression_Economy — MECHANICAL, 3 edges.** `00229E40` is called by `EnemyChain_UpdateOnDefeat` (`00317ED0`); `EnemyChain_UpdateOnDefeat` (`00317ED0`) calls `EnemyChain_TryAdvanceRank` (`003183D0`); `EnemyChain_UpdateOnDefeat` (`00317ED0`) is called by `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`).

**UI — MECHANICAL, 43 edges.** `0017FAE0` is called by `002AC5F0`, `002AE610`, `002AF340`, `002AF960` and 1 more; `0017F940` is called by `002AC5F0`, `002AE610`, `002AF340`, `002B2150`; `002AC2F0` is called by `002AE610`, `002AF340`, `002B2150`; `002B2150` is called by `002AC5F0`, `002AF340`, `002AF960`; `0017F8C0` is called by `002AF340`, `002B2150`; `00229E40` is called by `0028AAA0`, `002AC5F0`; `002AAE40` calls `002AC5F0`, `002B2150`; `002AC5F0` calls `002AE610`, `002B2150`; `002AC5F0` is called by `002AF340`, `002B2150`; `002AF340` calls `002AC5F0`, `002B2150`; `002AF960` is called by `002A4430`, `002A4830`; `002A4430` calls `002AF960`; `002A4830` calls `002AF960`; `002ABB20` calls `002AF340`; `002ABB20` is called by `002ABF70`; `002ABF70` calls `002ABB20`; `002AE610` is called by `002AC5F0`; `002AF340` is called by `002ABB20`; `002AF960` calls `002B2150`; `002B20B0` is called by `002ABB20`; `002B2150` calls `002AC5F0`; `002B2DF0` calls `002B2150`; `002B2DF0` is called by `002AC5F0`; `002B3E30` is called by `002AF340`; `002B5390` calls `002B2150`.

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
